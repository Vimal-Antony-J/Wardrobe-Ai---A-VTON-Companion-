import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central configuration, overridable via environment variables or a .env file.
    """

    # Path where FASHN-VTON weights live (model.safetensors, dwpose/, etc.)
    weights_dir: str = os.getenv("WEIGHTS_DIR", "./weights")

    # HuggingFace cache location (used for the auto-downloaded human parser weights)
    hf_home: str = os.getenv("HF_HOME", "./.cache/huggingface")

    # Frontend origins allowed to call this API
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    max_image_size_mb: int = 10
    allowed_content_types: List[str] = ["image/jpeg", "image/png", "image/webp"]

    class Config:
        env_file = ".env"


settings = Settings()

# Make sure the HF cache dir is honored before any model code imports transformers/etc.
os.environ.setdefault("HF_HOME", settings.hf_home)
