"""
One-time download of the MediaPipe pose_landmarker model used by the
classical overlay fallback (app/services/overlay_service.py). This is
unrelated to the fashn_vton/DWPose weights - a separate, small (~30MB)
model file.

Usage:
    python scripts/download_pose_model.py
    python scripts/download_pose_model.py --variant lite   # faster, less accurate
    python scripts/download_pose_model.py --variant full   # balanced
    python scripts/download_pose_model.py --variant heavy  # most accurate (default)
"""

import argparse
import os
import urllib.request

MODEL_URLS = {
    "lite": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task",
    "full": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task",
    "heavy": "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=MODEL_URLS.keys(), default="heavy")
    parser.add_argument("--out", default="./weights/mediapipe/pose_landmarker.task")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    url = MODEL_URLS[args.variant]
    print(f"Downloading {args.variant} pose_landmarker model from {url} ...")
    urllib.request.urlretrieve(url, args.out)
    print(f"Saved to {args.out}")
    print("Set POSE_MODEL_PATH in .env if you used a custom --out path.")


if __name__ == "__main__":
    main()
