import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas import TryOnResponse
from app.services.tryon_service import tryon_service
from app.utils.image_utils import image_to_base64, load_image_from_upload

logger = logging.getLogger("tryon_router")

router = APIRouter()

VALID_CATEGORIES = {"tops", "bottoms", "one-pieces"}


@router.post("/tryon", response_model=TryOnResponse)
async def try_on(
    person_image: UploadFile = File(..., description="Photo of the model/person"),
    garment_image: UploadFile = File(..., description="Photo of the garment (worn or flat-lay)"),
    category: str = Form(..., description="One of: tops | bottoms | one-pieces"),
) -> TryOnResponse:
    """
    Runs the FASHN-VTON pipeline (pose detection + garment transfer happen
    internally) and returns the result image as base64 PNG, ready for the
    dashboard to render as an <img> src.
    """
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"category must be one of {sorted(VALID_CATEGORIES)}, got '{category}'",
        )

    if not tryon_service.is_loaded:
        raise HTTPException(status_code=503, detail="Model is still loading. Try again shortly.")

    person = await load_image_from_upload(person_image)
    garment = await load_image_from_upload(garment_image)

    try:
        result_image, elapsed = await tryon_service.run_tryon(person, garment, category)
    except Exception as exc:
        logger.exception("Inference failed")
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}")

    return TryOnResponse(
        success=True,
        image_base64=image_to_base64(result_image),
        category=category,
        processing_time_seconds=round(elapsed, 2),
    )
