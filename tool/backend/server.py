"""FastAPI entrypoint for the Lucent Carat Lab catalog dashboard.

Skeleton only — wire the pipeline stages (see tool/README.md) into these routes.
Run: uvicorn server:app --reload
"""
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import config  # loads repo config + secrets

app = FastAPI(title="Lucent Carat Lab — Catalog Generator")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# in-memory job registry (swap for tool/backend/jobs/<sku>.json persistence)
JOBS: dict[str, dict] = {}


@app.get("/health")
def health():
    return {
        "ok": True,
        "model": config.GEN["model"],
        "images_per_catalog": config.IMAGES_PER_CATALOG,
        "source_parent": config.DRIVE_FOLDERS["source_parent"],
    }


@app.post("/jobs/{sku}")
def start_job(sku: str):
    # TODO pipeline.start(sku): FETCH -> STUDY -> IMPORT -> GENERATE -> DOWNLOAD -> QC -> FALLBACK
    JOBS[sku] = {"sku": sku, "stage": "queued", "images": []}
    return JOBS[sku]


@app.get("/jobs/{sku}")
def get_job(sku: str):
    return JOBS.get(sku, {"error": "not found"})


@app.post("/jobs/{sku}/approve")
def approve(sku: str, image_ids: list[str]):
    # TODO mark approved; when all pass -> allow deliver
    return {"sku": sku, "approved": image_ids}


@app.post("/jobs/{sku}/deliver")
def deliver(sku: str):
    # TODO drive upload + write config/deliveries/<sku>.json + git commit to main
    return {"sku": sku, "delivered": True}


@app.websocket("/jobs/{sku}/events")
async def events(ws: WebSocket, sku: str):
    await ws.accept()
    # TODO stream pipeline stage/progress/log events for this SKU
    await ws.send_json({"sku": sku, "stage": "connected"})
