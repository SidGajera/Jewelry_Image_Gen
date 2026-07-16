"""FastAPI entrypoint for the Lucent Carat Lab catalog dashboard.

Skeleton only — wire the pipeline stages (see tool/README.md) into these routes.
Run: uvicorn server:app --reload
"""
from pathlib import Path

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import config  # loads repo config + secrets
from lib.config.paths import PATHS
from lib.pipeline import pipeline, dispatch
from lib.pipeline import mode as modemod

app = FastAPI(title="Lucent Carat Lab — Catalog Generator")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

PATHS.ensure_dirs()

# in-memory job registry (swap for tool/backend/jobs/<sku>.json persistence)
JOBS: dict[str, dict] = {}


@app.get("/health")
def health():
    return {
        "ok": True,
        "model": config.GEN["model"],
        "images_per_catalog": config.IMAGES_PER_CATALOG,
        "source_parent": config.DRIVE_FOLDERS["source_parent"],
        "paths": PATHS.as_dict(),
        "logo_asset_exists": config.LOGO_ASSET.exists(),
    }


class CompositeRequest(BaseModel):
    scene: str                      # path to the AI scene (cloth/hand/environment)
    source_ring: str                # path to the source-CAD ring image
    out: str                        # output path
    shot_type: str                  # studio | lifestyle | closeup
    sku: str | None = None
    scale: float | None = None
    pos: str | None = None
    shadow: float | None = None
    match_white: bool = True
    print_studio_logo: bool = False


@app.post("/composite")
def composite(req: CompositeRequest):
    """Direct composite (composite-v1): drop the real source ring into an AI scene
    and return the provenance QC verdict. This is what makes the ring identical to
    source — the pipeline, not a prompt."""
    res = pipeline.process_shot(
        req.scene, req.source_ring, req.out,
        shot_type=req.shot_type, sku=req.sku,
        scale=req.scale, pos=req.pos, shadow=req.shadow,
        match_white=req.match_white, print_studio_logo=req.print_studio_logo,
    )
    return res.as_dict()


class GenerateRequest(BaseModel):
    scene_or_render: str            # AI scene (composite) OR an existing legacy render
    source_ring: str
    out: str
    shot_type: str
    sku: str | None = None
    mode: str | None = None         # override the active pipeline (else registry active)


@app.post("/generate")
def generate(req: GenerateRequest):
    """Route through the active pipeline with automatic geometry-safe fallback and
    provenance (safe-versioning rules 4-5)."""
    res = dispatch.generate(
        req.scene_or_render, req.source_ring, req.out,
        shot_type=req.shot_type, sku=req.sku, mode=req.mode,
    )
    return res.as_dict()


class ShadowTestRequest(BaseModel):
    source_ring: str
    scene_for_composite: str
    legacy_render: str
    out_dir: str
    shot_type: str
    sku: str | None = None


@app.post("/shadow-test")
def shadow_test(req: ShadowTestRequest):
    """Compare legacy vs composite-v1 on the same source before any promotion (rule 4)."""
    return dispatch.shadow_test(
        req.source_ring, req.scene_for_composite, req.legacy_render, req.out_dir,
        shot_type=req.shot_type, sku=req.sku,
    )


@app.get("/pipeline")
def pipeline_mode():
    """Current pipeline selection (safe-versioning rules 2-3)."""
    return modemod.summary()


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
