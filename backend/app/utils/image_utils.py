import base64
import io

from fastapi import HTTPException, UploadFile
from PIL import Image

from app.config import settings


async def load_image_from_upload(upload: UploadFile) -> Image.Image:
    """
    Validates an uploaded file and returns it as an RGB PIL Image,
    matching the .convert("RGB") step used in the reference pipeline script.
    """
    if upload.content_type not in settings.allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{upload.content_type}'. "
            f"Allowed types: {settings.allowed_content_types}",
        )

    contents = await upload.read()
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size is {settings.max_image_size_mb}MB.",
        )

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {exc}")

    return image


def image_to_base64(image: Image.Image, image_format: str = "PNG") -> str:
    """Encodes a PIL Image to a base64 string for embedding in a JSON response."""
    buffer = io.BytesIO()
    image.save(buffer, format=image_format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
