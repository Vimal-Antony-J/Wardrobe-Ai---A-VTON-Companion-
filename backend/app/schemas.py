from typing import Literal, Optional

from pydantic import BaseModel

Category = Literal["tops", "bottoms", "one-pieces"]


class TryOnResponse(BaseModel):
    success: bool
    image_base64: Optional[str] = None
    category: Optional[str] = None
    processing_time_seconds: Optional[float] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str  # "ok" | "loading" | "error"
    device: str  # "cuda" | "cpu" | "unknown"
    model_loaded: bool
