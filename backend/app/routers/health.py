from fastapi import APIRouter

from app.schemas import HealthResponse
from app.services.tryon_service import tryon_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Lets the frontend dashboard poll whether the model is ready to serve requests."""
    return HealthResponse(
        status="ok" if tryon_service.is_loaded else "loading",
        device=tryon_service.device,
        model_loaded=tryon_service.is_loaded,
    )
