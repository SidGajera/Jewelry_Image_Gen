"""pipeline.py — default-composite orchestration (the geometry-safe generation path).

Policy (user-locked 2026-07-16, after 5 rejected renders across 4 SKUs): the
composite pipeline is the DEFAULT generation path. The AI generates only the
scene (cloth / hand / environment); the ring is always the REAL source-CAD pixels
composited in, so geometry is identical to source by construction.

  - lifestyle / closeup : ALWAYS composite (never ship a raw worn render).
  - studio              : composite the ring into the clean-cloth scene; optionally
                          print the locked two-tone logo (studio only).

Each finished image passes the provenance QC gate (qc.qc_final). Manual/CLI
compositing (fallback.py) exists only for debugging; this module is the automatic
path. Generation of the scene itself happens in the MCP session (or any upstream);
this pipeline consumes the downloaded scene + the source ring and returns the
geometry-locked final.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from lib.pipeline import fallback, qc
from lib.config.paths import PATHS

# Placement defaults per shot type: (ring width as fraction of scene, center x,y).
# Studio frames the ring large + centered; worn shots sit smaller on the finger.
PLACEMENT_DEFAULTS: dict[str, dict] = {
    "studio":    {"scale": 0.55, "pos": "0.5,0.5",  "shadow": 0.35},
    "lifestyle": {"scale": 0.16, "pos": "0.5,0.55", "shadow": 0.25},
    "closeup":   {"scale": 0.42, "pos": "0.5,0.5",  "shadow": 0.30},
}
ALWAYS_COMPOSITE = {"lifestyle", "closeup"}   # never ship a raw render for these


@dataclass
class ShotResult:
    sku: Optional[str]
    shot_type: str
    out_path: str
    verdict: dict
    provenance: dict
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "sku": self.sku, "shot_type": self.shot_type, "out_path": self.out_path,
            "verdict": self.verdict, "provenance": self.provenance,
            "warnings": self.warnings,
        }


def process_shot(
    scene: str | Path,
    source_ring: str | Path,
    out: str | Path,
    *,
    shot_type: str,
    sku: Optional[str] = None,
    scale: Optional[float] = None,
    pos: Optional[str] = None,
    shadow: Optional[float] = None,
    match_white: bool = True,
    print_studio_logo: bool = False,
    logo_scale: float = 0.42,
    logo_pos: str = "lower-right",
) -> ShotResult:
    """Produce one geometry-locked final image from an AI scene + the source ring.

    Composites the real source-CAD ring into the scene (default path), then runs the
    provenance QC gate. For studio, optionally prints the locked logo afterward.
    Raises ValueError for an unknown shot_type.
    """
    shot_type = shot_type.lower()
    if shot_type not in PLACEMENT_DEFAULTS:
        raise ValueError(f"unknown shot_type {shot_type!r}; expected {list(PLACEMENT_DEFAULTS)}")

    d = PLACEMENT_DEFAULTS[shot_type]
    scale = d["scale"] if scale is None else scale
    pos = d["pos"] if pos is None else pos
    shadow = d["shadow"] if shadow is None else shadow

    out = Path(out)
    comp = fallback.composite_ring(
        scene, source_ring, out,
        scale=scale, pos=pos, shadow=shadow, match_white=match_white,
    )

    # studio-only: stamp the locked two-tone logo into the cloth (in place)
    if print_studio_logo and shot_type == "studio":
        fallback.print_logo(out, out, scale=logo_scale, pos=logo_pos)

    verdict = qc.qc_final(
        out, shot_type=shot_type, from_composite=True,
        geometry_source=comp.geometry_source,
    )

    provenance = {
        "path": "composite",                 # default geometry-safe path
        "geometry_source": comp.geometry_source,
        "ring_px": comp.ring_px,
        "pos": comp.pos,
        "shadow": comp.shadow,
        "match_white": comp.match_white,
        "logo_printed": bool(print_studio_logo and shot_type == "studio"),
    }
    return ShotResult(
        sku=sku, shot_type=shot_type, out_path=str(out),
        verdict=verdict.as_dict(), provenance=provenance, warnings=verdict.warnings,
    )


def evaluate_raw_render(
    render: str | Path, *, shot_type: str, sku: Optional[str] = None,
) -> ShotResult:
    """Gate a RAW AI render (no composite). Always fails the geometry gate for
    ALWAYS_COMPOSITE shots and, per policy, for any shot — the verdict tells the
    caller to composite instead of shipping. Kept for the dashboard's 'why did this
    get composited?' explanation."""
    shot_type = shot_type.lower()
    verdict = qc.qc_final(render, shot_type=shot_type, from_composite=False)
    return ShotResult(
        sku=sku, shot_type=shot_type, out_path=str(render),
        verdict=verdict.as_dict(),
        provenance={"path": "raw", "geometry_source": None},
        warnings=verdict.warnings + (
            ["shot type requires composite"] if shot_type in ALWAYS_COMPOSITE else []
        ),
    )
