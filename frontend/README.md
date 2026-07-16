# Fit Room — FASHN-VTON Frontend

A React (Vite) dashboard for the FASHN-VTON FastAPI backend: drag and drop a
person photo and a garment photo, pick a category, and get back the
generated try-on image.

```
src/
├── main.jsx                Entry point
├── App.jsx                 Page layout, wires everything together
├── index.css                 Design tokens + all styling
├── api/
│   └── tryon.js               fetch wrappers for GET /health, POST /tryon
├── components/
│   ├── DropZone.jsx            Drag-and-drop image uploader (click or drop)
│   ├── CategorySelector.jsx     tops / bottoms / one-pieces picker
│   ├── ResultTag.jsx             Generated image card + download button
│   └── StatusBar.jsx             Polls /health, shows backend/model status
└── hooks/
    └── useTryOn.js               State machine: idle → loading → success/error
```

## 1. Install

```bash
cd fashn_vton_frontend
npm install
cp .env.example .env
```

By default `VITE_API_BASE_URL` points at `http://localhost:8000/api`, which
matches the FastAPI backend's default port. Change it in `.env` if your
backend runs elsewhere.

## 2. Run

```bash
npm run dev
```

Open http://localhost:5173. The backend's CORS settings already allow this
origin (`http://localhost:5173`), so no extra config is needed there.

Make sure the backend is running first (`python run.py` in the backend
project) - the status pill in the header will show "Backend unreachable"
until it can reach `GET /api/health`.

## 3. Using it

1. Drag a full-body photo onto the **01 · PERSON** panel (or click it to
   browse).
2. Drag a garment photo onto the **02 · GARMENT** panel.
3. Pick a category - tops, bottoms, or one-pieces - to match the garment.
4. Click **Generate try-on**. The button reads "Stitching…" while the
   backend runs pose detection and garment transfer.
5. The result appears as a tag card below, with the category and render
   time it reported, and a **Download image** button.

## 4. Build for production

```bash
npm run build
```

Outputs static files to `dist/`, which can be served by any static host
(nginx, Vercel, Netlify, etc.) - just make sure `VITE_API_BASE_URL` at build
time points at your deployed backend, and that backend's CORS origins list
includes your frontend's real domain.

## Notes

- Preview thumbnails use `URL.createObjectURL`, revoked on cleanup, so
  there's no upload to the server until you click **Generate try-on**.
- The generated image comes back as base64 in the JSON response and is
  rendered directly as a data URL - no extra request needed to fetch it.
- Uploaders are keyboard accessible (Enter/Space opens the file picker) and
  screen-reader labeled, alongside the drag-and-drop behavior.
