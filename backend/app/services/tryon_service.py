import asyncio
import logging
import time
from typing import Tuple

from PIL import Image
from starlette.concurrency import run_in_threadpool

from app.config import settings

logger = logging.getLogger("tryon_service")


class TryOnService:
    """
    Thin wrapper around fashn_vton.TryOnPipeline.

    Notes on pose detection:
    FASHN-VTON runs DWPose (pose keypoints) and its human parser internally,
    as part of the pipeline() call shown in the reference script. There is no
    separate pose-detection call to make from this backend - passing
    person_image / garment_image / category into the pipeline is enough.

    The pipeline and its weights are loaded ONCE at app startup (see main.py's
    lifespan handler) since loading is expensive. A single pipeline instance
    is then reused across requests.
    """

    def __init__(self) -> None:
        self._pipeline = None
        self._device = "unknown"
        # A single GPU should not run two inferences at once - serialize them.
        self._lock = asyncio.Lock()

    def load(self) -> None:
        from fashn_vton import TryOnPipeline  # imported lazily so config env vars apply first
        import torch

        logger.info("Loading FASHN-VTON pipeline from weights_dir=%s", settings.weights_dir)
        self._pipeline = TryOnPipeline(weights_dir=settings.weights_dir)
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info("FASHN-VTON pipeline loaded. device=%s", self._device)

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None

    @property
    def device(self) -> str:
        return self._device

    async def run_tryon(
        self,
        person_image: Image.Image,
        garment_image: Image.Image,
        category: str,
    ) -> Tuple[Image.Image, float]:
        if not self.is_loaded:
            raise RuntimeError("TryOnPipeline is not loaded yet.")

        async with self._lock:
            start = time.perf_counter()
            result = await run_in_threadpool(
                self._pipeline,
                person_image=person_image,
                garment_image=garment_image,
                category=category,
            )
            elapsed = time.perf_counter() - start

        return result.images[0], elapsed


# Singleton instance shared across the app
tryon_service = TryOnService()
