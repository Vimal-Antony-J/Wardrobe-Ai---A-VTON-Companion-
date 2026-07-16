import logging

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from app.schemas import TryOnResponse
from app.services.overlay_service import overlay_service
from app.utils.image_utils import image_to_base64, load_image_from_upload

logger = logging.getLogger("overlay_router")

router = APIRouter()


@router.post("/tryon-overlay", response_model=TryOnResponse)
async def try_on_overlay(
    person_image: UploadFile = File(..., description="Full-body, front-facing photo"),
    garment_image: UploadFile = File(..., description="Garment photo, ideally worn/front-facing"),
) -> TryOnResponse:
    """
    Classical (non-AI) fallback for draped garments the diffusion pipeline
    handles poorly - e.g. sarees. See overlay_service.py for the approach.
    Recommended for "one-pieces" category inputs where /api/tryon produces
    an unrelated garment silhouette.
    """
    person = await load_image_from_upload(person_image)
    garment = await load_image_from_upload(garment_image)

    try:
        result_image, elapsed = await run_in_threadpool(
            overlay_service.generate, person, garment
        )
    except ValueError as exc:
        # Expected, user-fixable problems (no person detected, bad garment cutout, etc.)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Classical overlay failed")
        raise HTTPException(status_code=500, detail=f"Overlay generation failed: {exc}")

    return TryOnResponse(
        success=True,
        image_base64=image_to_base64(result_image),
        category="one-pieces",
        processing_time_seconds=round(elapsed, 2),
        method="classical-overlay",
    )
