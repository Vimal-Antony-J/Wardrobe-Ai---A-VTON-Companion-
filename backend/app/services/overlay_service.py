"""
Classical fallback for garments the diffusion pipeline handles poorly -
draped, unstitched garments like sarees, where TryOnPipeline tends to
substitute a Western-style silhouette (see tryon_service.py's docstring
for the AI path).

This does NOT use the fashn_vton model at all. Instead:
  1. MediaPipe's PoseLandmarker finds body landmarks (shoulders, hips,
     ankles, elbows, wrists) and a person segmentation mask.
  2. rembg strips the garment photo's background.
  3. A piecewise-affine warp maps the garment texture onto a body-shaped
     control mesh built from the landmarks.
  4. The warped garment is alpha-composited onto the person, masked to
     their silhouette.
  5. Forearms/hands are redrawn on top so a hands-on-hips pose isn't
     covered by the garment.

Trade-off: this preserves the garment's actual shape/pattern (unlike the
AI path for drape garments), but it will look like a well-fitted decal
rather than a photoreal render - no fabric folds or warp-driven shading.

Requires a MediaPipe pose_landmarker .task model file - see
scripts/download_pose_model.py and POSE_MODEL_PATH in config.py.
"""

import logging
import time
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np
from PIL import Image

logger = logging.getLogger("overlay_service")


@dataclass
class BodyLandmarks:
    """Pixel-space body points used to build the garment warp mesh."""

    left_shoulder: np.ndarray
    right_shoulder: np.ndarray
    left_hip: np.ndarray
    right_hip: np.ndarray
    left_ankle: np.ndarray
    right_ankle: np.ndarray
    left_elbow: np.ndarray
    right_elbow: np.ndarray
    left_wrist: np.ndarray
    right_wrist: np.ndarray


def warp_and_composite(
    person_rgb: np.ndarray,
    garment_rgba: np.ndarray,
    landmarks: BodyLandmarks,
    person_mask: Optional[np.ndarray] = None,
) -> np.ndarray:
    """
    Pure image-processing step (no MediaPipe/rembg calls) - warps the
    background-stripped garment onto the body region defined by
    `landmarks` and composites it onto `person_rgb`. Split out from
    OverlayService.generate() so it can be unit tested with hand-built
    landmark data, independent of the pose model.
    """
    from skimage.transform import PiecewiseAffineTransform, warp

    h, w = person_rgb.shape[:2]

    alpha = garment_rgba[:, :, 3]
    ys, xs = np.where(alpha > 10)
    if len(xs) == 0:
        raise ValueError(
            "Could not isolate the garment from its background - try a photo "
            "with a plainer background."
        )
    gx0, gx1, gy0, gy1 = xs.min(), xs.max(), ys.min(), ys.max()

    # Source control grid: 4 rows x 3 cols across the garment's bbox
    src_pts = np.array(
        [
            [gx0 + (gx1 - gx0) * col / 2, gy0 + (gy1 - gy0) * row / 3]
            for row in range(4)
            for col in range(3)
        ]
    )

    # Target control grid: shoulder / waist / knee / hem lines, widened
    # slightly so the garment has volume instead of hugging the body.
    def widen_pair(a: np.ndarray, b: np.ndarray, factor: float):
        mid = (a + b) / 2
        return mid + (a - mid) * factor, mid + (b - mid) * factor

    l_sh_w, r_sh_w = widen_pair(landmarks.left_shoulder, landmarks.right_shoulder, 1.15)
    l_hip_w, r_hip_w = widen_pair(landmarks.left_hip, landmarks.right_hip, 1.25)
    l_ank_w, r_ank_w = widen_pair(landmarks.left_ankle, landmarks.right_ankle, 1.4)

    def line(a, b):
        return [a, (a + b) / 2, b]

    knee_l = l_hip_w + (l_ank_w - l_hip_w) * 0.55
    knee_r = r_hip_w + (r_ank_w - r_hip_w) * 0.55

    dst_pts = np.array(
        line(l_sh_w, r_sh_w) + line(l_hip_w, r_hip_w) + line(knee_l, knee_r) + line(l_ank_w, r_ank_w)
    )

    # skimage's warp() needs an output->input mapping, so estimate dst -> src.
    # scikit-image >=0.26 prefers the from_estimate() classmethod over the
    # older estimate() instance method (deprecated, removed in 2.2) -
    # support both so this works across versions.
    try:
        if hasattr(PiecewiseAffineTransform, "from_estimate"):
            tform = PiecewiseAffineTransform.from_estimate(dst_pts, src_pts)
        else:
            tform = PiecewiseAffineTransform()
            tform.estimate(dst_pts, src_pts)
    except Exception as exc:
        raise ValueError(f"Could not build the garment warp mesh: {exc}")

    warped_rgba = np.zeros((h, w, 4), dtype=np.uint8)
    for c in range(4):
        warped_rgba[:, :, c] = (
            warp(garment_rgba[:, :, c], tform, output_shape=(h, w), mode="constant", cval=0) * 255
        ).astype(np.uint8)

    garment_alpha = warped_rgba[:, :, 3:4].astype(float) / 255.0
    if person_mask is not None:
        body_mask = (person_mask > 0.5).astype(float)[:, :, None]
        garment_alpha = garment_alpha * body_mask

    composite = (
        person_rgb.astype(float) * (1 - garment_alpha) + warped_rgba[:, :, :3].astype(float) * garment_alpha
    ).astype(np.uint8)

    return _restore_forearms(
        composite,
        person_rgb,
        landmarks.left_elbow,
        landmarks.left_wrist,
        landmarks.right_elbow,
        landmarks.right_wrist,
    )


def _restore_forearms(
    composite: np.ndarray,
    original: np.ndarray,
    l_el: np.ndarray,
    l_wr: np.ndarray,
    r_el: np.ndarray,
    r_wr: np.ndarray,
    thickness_ratio: float = 0.09,
) -> np.ndarray:
    import cv2

    mask = np.zeros(composite.shape[:2], dtype=np.uint8)
    for elbow, wrist in [(l_el, l_wr), (r_el, r_wr)]:
        length = float(np.linalg.norm(wrist - elbow))
        thickness = max(int(length * thickness_ratio), 8)
        cv2.line(
            mask,
            tuple(elbow.astype(int)),
            tuple(wrist.astype(int)),
            color=255,
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )
        cv2.circle(mask, tuple(wrist.astype(int)), thickness, 255, -1)

    keep_original = (mask > 0)[:, :, None]
    return np.where(keep_original, original, composite)


class OverlayService:
    def __init__(self) -> None:
        self._landmarker = None

    def _lazy_init(self) -> None:
        if self._landmarker is not None:
            return

        from mediapipe.tasks.python import BaseOptions, vision
        from mediapipe.tasks.python.vision.core.vision_task_running_mode import (
            VisionTaskRunningMode,
        )

        from app.config import settings

        options = vision.PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=settings.pose_model_path),
            running_mode=VisionTaskRunningMode.IMAGE,
            num_poses=1,
            output_segmentation_masks=True,
        )
        self._landmarker = vision.PoseLandmarker.create_from_options(options)
        logger.info("MediaPipe PoseLandmarker initialized for classical overlay")

    def generate(self, person_image: Image.Image, garment_image: Image.Image) -> Tuple[Image.Image, float]:
        start = time.perf_counter()
        self._lazy_init()

        import mediapipe as mp
        from mediapipe.tasks.python import vision
        from rembg import remove

        person_rgb = np.array(person_image.convert("RGB"))
        h, w = person_rgb.shape[:2]

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=person_rgb)
        result = self._landmarker.detect(mp_image)

        if not result.pose_landmarks:
            raise ValueError("No person detected. Use a clear, front-facing, full-body photo.")

        lm = result.pose_landmarks[0]
        PL = vision.PoseLandmark

        def pt(landmark_id) -> np.ndarray:
            p = lm[landmark_id]
            return np.array([p.x * w, p.y * h])

        landmarks = BodyLandmarks(
            left_shoulder=pt(PL.LEFT_SHOULDER),
            right_shoulder=pt(PL.RIGHT_SHOULDER),
            left_hip=pt(PL.LEFT_HIP),
            right_hip=pt(PL.RIGHT_HIP),
            left_ankle=pt(PL.LEFT_ANKLE),
            right_ankle=pt(PL.RIGHT_ANKLE),
            left_elbow=pt(PL.LEFT_ELBOW),
            right_elbow=pt(PL.RIGHT_ELBOW),
            left_wrist=pt(PL.LEFT_WRIST),
            right_wrist=pt(PL.RIGHT_WRIST),
        )

        person_mask = None
        if result.segmentation_masks:
            person_mask = result.segmentation_masks[0].numpy_view()

        garment_rgba = np.array(remove(garment_image.convert("RGBA")))

        composite = warp_and_composite(person_rgb, garment_rgba, landmarks, person_mask)

        elapsed = time.perf_counter() - start
        return Image.fromarray(composite), elapsed


overlay_service = OverlayService()
