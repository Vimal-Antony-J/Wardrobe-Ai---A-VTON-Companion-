import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health, tryon
from app.services.tryon_service import tryon_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the (heavy) pipeline once at startup rather than per-request.
    logger.info("Startup: loading TryOnPipeline ...")
    try:
        tryon_service.load()
    except Exception:
        logger.exception("Failed to load TryOnPipeline - /api/health will report not-ready")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="FASHN-VTON Try-On API",
    description="Backend API wrapping the FASHN-VTON virtual try-on pipeline.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(tryon.router, prefix="/api", tags=["try-on"])
