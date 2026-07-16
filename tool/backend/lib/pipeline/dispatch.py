"""dispatch.py — route a shot through the active pipeline with automatic fallback
and provenance recording (safe-versioning rules 4-5, docs/15).

Flow per shot:
  1. Resolve the active mode (env PIPELINE_MODE or registry `active`).
  2. Run that pipeline and QC it.
  3. If it fails the geometry gate, fall back to the version's `fallback_to`
     (a raw legacy render → composite-v1, which rescues the real source ring).
  4. Never mark deliverable unless geometry is guaranteed AND sanity passes.
  5. Record which pipeline actually produced the delivered image.

HYBRID POLICY (user-locked 2026-07-16, docs/15 §5): composite-v1 is the DEFAULT.
Legacy is NEVER used automatically (manual experimentation only) — so no version
sets fallback_to any more (both null). If composite cannot produce a shot
faithfully (e.g. a worn angle unavailable from the 2D CAD, or a geometry/integrity
QC fail), the pipeline SKIPS that shot and requests more source material (more CAD
angles / a 3D model) — it never lets AI redraw the jewelry. Missing an image is
preferable to a geometrically incorrect product. `deliverable=False` with
`action_required` set means: do not ship, get more source, do NOT auto-run legacy.

Legacy generation itself happens upstream in the MCP session; for a legacy shot
the caller passes the already-rendered image as `scene_or_render`. A composite
shot treats that same argument as the AI scene to composite the source ring into.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from lib.pipeline import mode as modemod
from lib.pipeline import pipeline, qc


@dataclass
class DispatchResult:
    sku: Optional[str]
    shot_type: str
    requested_mode: str
    delivered_by: Optional[str]      # mode that produced the deliverable (None = none passed)
    fallback_used: bool
    deliverable: bool
    out_path: Optional[str]
    verdict: dict
    action_required: Optional[str] = None   # set when skipped: what to do (never auto-legacy)
    trail: list[dict] = field(default_factory=list)   # every attempt, for the record

    def as_dict(self) -> dict:
        return {
            "sku": self.sku, "shot_type": self.shot_type,
            "requested_mode": self.requested_mode, "delivered_by": self.delivered_by,
            "fallback_used": self.fallback_used, "deliverable": self.deliverable,
            "out_path": self.out_path, "verdict": self.verdict,
            "action_required": self.action_required, "trail": self.trail,
        }


def _run_one(mode: str, shot_type: str, scene_or_render, source_ring, out, sku, **kw):
    """Run a single pipeline version. Returns (verdict_dict, out_path, provenance)."""
    v = modemod.get_version(mode)
    if v["kind"] == "composite":
        res = pipeline.process_shot(
            scene_or_render, source_ring, out,
            shot_type=shot_type, sku=sku,
            print_studio_logo=(shot_type == "studio"), **kw,
        )
        return res.verdict, res.out_path, res.provenance
    # prompt/legacy: the render already exists (produced via MCP upstream); QC only.
    verdict = qc.qc_final(scene_or_render, shot_type=shot_type, from_composite=False)
    return verdict.as_dict(), str(scene_or_render), {"path": "raw", "mode": mode}


def generate(
    scene_or_render: str | Path,
    source_ring: str | Path,
    out: str | Path,
    *,
    shot_type: str,
    sku: Optional[str] = None,
    mode: Optional[str] = None,
    **kw,
) -> DispatchResult:
    """Produce a deliverable image through the active pipeline, auto-falling back to
    the geometry-safe pipeline if the first attempt fails the geometry gate."""
    requested = mode or modemod.active_mode()
    trail: list[dict] = []

    verdict, out_path, prov = _run_one(requested, shot_type, scene_or_render, source_ring, out, sku, **kw)
    deliverable = bool(verdict["passed"] and verdict["geometry_guaranteed"])
    trail.append({"mode": requested, "deliverable": deliverable, "method": verdict["method"],
                  "provenance": prov})

    delivered_by = requested if deliverable else None
    fallback_used = False
    action_required = None

    if not deliverable:
        fb = modemod.get_version(requested).get("fallback_to")
        if fb:
            # (only if a version still declares a fallback_to; hybrid policy sets none)
            v2, out_path, prov2 = _run_one(fb, shot_type, scene_or_render, source_ring, out, sku, **kw)
            deliverable = bool(v2["passed"] and v2["geometry_guaranteed"])
            fallback_used = True
            trail.append({"mode": fb, "deliverable": deliverable, "method": v2["method"],
                          "provenance": prov2})
            if deliverable:
                delivered_by, verdict = fb, v2
        if not deliverable:
            # SKIP, don't invent: never auto-run legacy; get more source material.
            action_required = (
                "SKIP this shot — do NOT ship and do NOT auto-run legacy. Composite could "
                "not produce it faithfully; request more source (additional CAD angles / a 3D "
                "model) or omit the shot. Missing an image is preferable to an incorrect ring."
            )

    return DispatchResult(
        sku=sku, shot_type=shot_type, requested_mode=requested,
        delivered_by=delivered_by, fallback_used=fallback_used,
        deliverable=deliverable, out_path=out_path if deliverable else None,
        verdict=verdict, action_required=action_required, trail=trail,
    )


# fidelity categories a promotion is judged on (docs/15 §4). Geometry-family ones
# are decided automatically by provenance; scene-family ones need a human verdict.
_AUTO_CATEGORIES = ["product_geometry", "stone_shape_size_orientation", "ring_scale",
                    "prongs_gallery", "metal_thickness"]
_HUMAN_CATEGORIES = ["natural_placement", "lighting_shadows", "logo_realism",
                     "overall_photographic_quality"]


def shadow_test(
    source_ring: str | Path,
    scene_for_composite: str | Path,
    legacy_render: str | Path,
    out_dir: str | Path,
    *,
    shot_type: str,
    sku: Optional[str] = None,
) -> dict:
    """Run the SAME source through legacy (existing render) and composite-v1, and
    compare per fidelity category (rule 4). Composite-v1 may only be promoted when
    it is equal-or-better in every category. Geometry-family categories are decided
    here (composite = guaranteed identical; legacy raw = unverified). Scene-family
    categories are returned as 'needs_human' — promotion requires that sign-off, so
    this never auto-promotes on aesthetics alone.
    """
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    comp = pipeline.process_shot(
        scene_for_composite, source_ring, out_dir / f"{sku or 'shadow'}_composite.png",
        shot_type=shot_type, sku=sku, print_studio_logo=(shot_type == "studio"),
    )
    legacy_v = qc.qc_final(legacy_render, shot_type=shot_type, from_composite=False)

    comparison = {c: {"legacy": "unverified", "composite-v1": "guaranteed",
                      "winner": "composite-v1"} for c in _AUTO_CATEGORIES}
    for c in _HUMAN_CATEGORIES:
        comparison[c] = {"legacy": "needs_human", "composite-v1": "needs_human",
                         "winner": "needs_human"}

    auto_regression = any(comparison[c]["winner"] == "legacy" for c in _AUTO_CATEGORIES)
    return {
        "sku": sku, "shot_type": shot_type,
        "legacy": {"render": str(legacy_render), "verdict": legacy_v.as_dict()},
        "composite_v1": {"render": comp.out_path, "verdict": comp.verdict},
        "comparison": comparison,
        "auto_regression": auto_regression,
        "recommendation": (
            "composite-v1 wins/ties every automatic (geometry) category; "
            "human sign-off required on placement/lighting/logo/photographic realism "
            "before promoting composite-v1 to stable (docs/15 §4)."
            if not auto_regression else
            "composite-v1 regresses an automatic category — DO NOT promote."
        ),
    }
