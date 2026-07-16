"""qc.py — geometry/provenance verification gate for a finished catalog image.

Design honesty (why this is provenance-first, not classical-CV-first):
  Comparing a worn-on-hand AI render to a source-CAD ring on white via edge/shape
  metrics is unreliable and would produce false PASSes — the exact failure the
  operator rejected five times. So the RELIABLE geometry guarantee here comes from
  PROVENANCE: if the ring in the final image is the real source-CAD pixels
  (produced by fallback.composite_ring), geometry is identical to source BY
  CONSTRUCTION and passes. A raw AI render whose ring the model synthesized is
  reported as geometry-UNVERIFIED (never a silent pass) — which is what enforces
  the composite-by-default policy (docs/13 §5/§6, QUALITY_MEMORY
  geometry-immutable-auto-fallback).

  vision_geometry_verdict() is an optional stronger check (Claude vision) that
  degrades to {available: False} when no key/transport is configured — it never
  fabricates a verdict.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# 2K target per manifest generation_settings (resolution "2k"); allow a tolerance.
MIN_EDGE_PX = 1600          # below this = under-resolved warning
SQUARE_TOL = 0.02           # 1:1 aspect tolerance (2%)


@dataclass
class QCVerdict:
    passed: bool
    geometry_guaranteed: bool
    method: str                       # composite-provenance | raw-render-unverified | vision
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checklist: dict[str, str] = field(default_factory=dict)  # item -> pass|fail|unverified

    def as_dict(self) -> dict:
        return {
            "passed": self.passed,
            "geometry_guaranteed": self.geometry_guaranteed,
            "method": self.method,
            "reasons": self.reasons,
            "warnings": self.warnings,
            "checklist": self.checklist,
        }


def _image_sanity(image: Path) -> tuple[list[str], list[str]]:
    """Cheap, real checks: exists, square (1:1), 2K-ish. Returns (fails, warns)."""
    fails: list[str] = []
    warns: list[str] = []
    if not image.exists():
        return [f"image missing: {image}"], warns
    from PIL import Image
    with Image.open(image) as im:
        w, h = im.size
    if w == 0 or h == 0:
        return ["image has zero dimension"], warns
    if abs(w - h) / max(w, h) > SQUARE_TOL:
        fails.append(f"not 1:1 ({w}x{h}) — catalog requires square")
    if min(w, h) < MIN_EDGE_PX:
        warns.append(f"under-resolved ({w}x{h}); target ~2K")
    return fails, warns


# docs/13 §5 checklist items that provenance can settle vs. that need vision/manual.
_GEOMETRY_ITEMS = [
    "silhouette", "halo", "center_stone_shape", "prongs", "band_width",
    "twist_loops", "pave_layout", "stone_count", "gallery", "metal_thickness",
    "symmetry", "worn_scale",
]


def qc_final(
    image: str | Path,
    *,
    shot_type: str,
    from_composite: bool,
    geometry_source: Optional[str | Path] = None,
) -> QCVerdict:
    """Verdict for a finished image.

    from_composite=True means the ring pixels came from fallback.composite_ring
    (geometry_source = the source-CAD file used) → geometry guaranteed.
    from_composite=False (raw AI render) → geometry UNVERIFIED; the gate fails on
    geometry so the pipeline composites instead of shipping the redesign.
    """
    image = Path(image)
    fails, warns = _image_sanity(image)

    if from_composite:
        method = "composite-provenance"
        geometry_ok = True
        reasons = [
            "ring pixels copied from source-CAD "
            f"({Path(geometry_source).name if geometry_source else 'source'}) — "
            "geometry identical to source by construction"
        ]
        checklist = {k: "pass" for k in _GEOMETRY_ITEMS}
    else:
        method = "raw-render-unverified"
        geometry_ok = False
        reasons = [
            "raw AI render — ring geometry NOT verified against source; "
            "per policy do not ship, composite the real source ring (docs/13 §6)"
        ]
        checklist = {k: "unverified" for k in _GEOMETRY_ITEMS}

    passed = geometry_ok and not fails
    return QCVerdict(
        passed=passed,
        geometry_guaranteed=geometry_ok,
        method=method,
        reasons=reasons + [f"sanity fail: {f}" for f in fails],
        warnings=warns,
        checklist=checklist,
    )


def vision_geometry_verdict(render: str | Path, source: str | Path) -> dict:
    """Optional stronger check: ask Claude vision to compare render↔source geometry.

    Requires ANTHROPIC_API_KEY (REST). With the operator on MCP-only, this returns
    {available: False} — the pipeline then relies on composite provenance, which is
    the guarantee anyway. Never fabricates a verdict.
    """
    import config
    if not config.ANTHROPIC_API_KEY:
        return {
            "available": False,
            "reason": "ANTHROPIC_API_KEY not set (MCP-only); rely on composite provenance",
        }
    # Deferred: real Anthropic vision call. Kept out of the default path because the
    # composite guarantees geometry without spending a vision call per image.
    return {
        "available": False,
        "reason": "vision QC not enabled in this build; composite provenance is the guarantee",
    }
