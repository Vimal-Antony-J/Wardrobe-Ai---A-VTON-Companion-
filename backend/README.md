# FASHN-VTON Try-On Backend

FastAPI backend that wraps the FASHN-VTON v1.5 `TryOnPipeline` and exposes it
over HTTP so a frontend dashboard can POST a person photo + garment photo and
get back the try-on result.

## How it fits together

```
app/
├── main.py               FastAPI app, CORS, loads the pipeline once at startup
├── config.py              Env-driven settings (weights dir, HF cache, CORS origins)
├── schemas.py              Pydantic request/response models
├── routers/
│   ├── health.py           GET  /api/health   -> is the model loaded, on cpu/gpu?
│   └── tryon.py             POST /api/tryon    -> run inference, return base64 PNG
├── services/
│   └── tryon_service.py     Wraps TryOnPipeline; serializes GPU calls with a lock
└── utils/
    └── image_utils.py        Upload validation + base64 encoding helpers
run.py                       uvicorn entrypoint
requirements.txt
.env.example
```

### About pose detection

FASHN-VTON runs pose estimation internally: DWPose extracts keypoints for
both the person and garment images, and a human parser segments the person,
all inside the single `pipeline(...)` call. There's no separate pose
endpoint to build - `POST /api/tryon` covers it end to end.

## 1. Install the model

`fashn-vton` isn't on PyPI, so it's installed from source, separately from
this backend's own dependencies:

```bash
git clone https://github.com/fashn-AI/fashn-vton-1.5.git
cd fashn-vton-1.5
pip install -e .
python scripts/download_weights.py --weights-dir ./weights
```

This downloads `model.safetensors` (~2GB) and the DWPose ONNX models. The
human parser weights (~244MB) download automatically on first use to the
HuggingFace cache (configurable via `HF_HOME`).

GPU: an NVIDIA card with 8GB+ VRAM (Ampere or newer recommended) since the
model defaults to bfloat16. CPU-only works but will be much slower - swap
`onnxruntime-gpu` for `onnxruntime` in that case.

## 2. Install this backend

```bash
cd fashn_vton_backend
pip install -r requirements.txt
cp .env.example .env   # then edit WEIGHTS_DIR to point at the fashn-vton-1.5/weights folder
```

## 3. Run it

```bash
python run.py
# or: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs: http://localhost:8000/docs

## Endpoints

### `GET /api/health`
```json
{ "status": "ok", "device": "cuda", "model_loaded": true }
```

### `POST /api/tryon`
`multipart/form-data`:
- `person_image` (file) - photo of the model
- `garment_image` (file) - photo of the garment (worn or flat-lay)
- `category` (string) - `tops` | `bottoms` | `one-pieces`

```json
{
  "success": true,
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "category": "tops",
  "processing_time_seconds": 4.31
}
```

The frontend can render the result directly:
```html
<img src="data:image/png;base64,{{ image_base64 }}" />
```

### Example curl

```bash
curl -X POST http://localhost:8000/api/tryon \
  -F "person_image=@model.webp" \
  -F "garment_image=@garment.webp" \
  -F "category=tops"
```

## Design notes / next steps

- The pipeline is loaded **once** at startup (in `main.py`'s lifespan
  handler), not per-request - loading weights on every call would be far too
  slow.
- Inference calls are serialized with an `asyncio.Lock` in `tryon_service.py`
  so two requests can't hit the GPU at once and OOM it. For real concurrent
  throughput later, consider a task queue (Celery/RQ) with a small pool of
  GPU workers instead.
- Images are returned as base64 JSON rather than raw file streams so the
  dashboard can embed them without a second request; swap to a
  `StreamingResponse` or object storage (S3) if result images get large or
  you want shareable URLs.
- Not yet included, worth adding before production: request auth, rate
  limiting, structured logging/metrics, and a Dockerfile pinned to a CUDA
  base image.
