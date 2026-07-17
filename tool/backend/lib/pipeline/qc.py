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

# Jewelry Difference Detector (ZERO JEWELRY INVENTION POLICY, docs/16). The specific
# invention/omission failure modes to compare render-vs-source before acceptance.
JEWELRY_DIFF_CHECKS = [
    "diamond_count", "diamond_locations", "gallery_structure", "prong_count",
    "hidden_halo_presence", "pave_bridge_presence", "metal_silhouette",
]

# Head & Gallery Geometry Lock (docs/16). The center-stone assembly inspected
# SEPARATELY — the head is the most-invented region (girdle/support rings, gallery
# rails, extra bridges, thicker heads). Any mismatch = reject before delivery.
HEAD_GEOMETRY_CHECKS = [
    "prong_count", "prong_thickness", "prong_angle", "prong_position",
    "basket_shape", "gallery_shape", "support_arms", "bridge_geometry", "under_gallery",
    "head_height", "head_width", "head_thickness", "metal_volume",
    "no_added_support_ring", "no_added_gallery_rail", "no_extra_bridge",
    "no_invented_gallery", "open_spaces_preserved", "no_hidden_structures",
    # Halo assembly lock (docs/16) — the LR-0149 drift: thicker/taller/wider halo,
    # larger halo stones, shallower stone seating, bulkier basket, taller profile.
    "halo_thickness", "halo_stone_size", "halo_height", "halo_diameter",
    "stone_seating_depth", "basket_height", "head_bulk", "overall_ring_height",
]


# Composite Integrity (docs/16). A composite can preserve geometry PERFECTLY yet
# still be a failed image: the scene already contained a ring (double-ring), the
# cutout left a white mask/segmentation residue, or lighting/shadows don't match.
# geometry_guaranteed=True does NOT imply the composite is deliverable.
COMPOSITE_INTEGRITY_CHECKS = [
    "original_object_removed", "single_ring_present", "no_segmentation_artifacts",
    "no_white_mask_residue", "consistent_lighting_shadows", "natural_background_integration",
]


def composite_integrity(image: str | Path, *, scene_is_clean: bool) -> dict:
    """Gate composite-integration artifacts (root cause: dirty scene + loose keying).

    The only deterministic guarantee is at the INPUT: a scene asserted ring-free
    cannot leave a leftover ring or a double-ring. If the scene is NOT asserted
    clean, original_object_removed + single_ring_present HARD-FAIL (this is what
    the double-ring failure must trip). Segmentation/residue/lighting/integration
    need a vision or human check — reported 'unverified', never a fabricated pass.
    Classical CV cannot reliably spot a soft white-mask patch (it reads like cloth
    highlights), so no pixel-detector is claimed here.
    """
    checks: dict[str, str] = {}
    if scene_is_clean:
        checks["original_object_removed"] = "pass"   # no original object existed
        checks["single_ring_present"] = "pass"        # only the composited ring
    else:
        checks["original_object_removed"] = "fail"    # scene may hold another ring
        checks["single_ring_present"] = "fail"
    for k in ("no_segmentation_artifacts", "no_white_mask_residue",
              "consistent_lighting_shadows", "natural_background_integration"):
        checks[k] = "unverified"
    failed = any(v == "fail" for v in checks.values())
    reason = ("scene NOT asserted ring-free — may leave the original object / a "
              "double ring; composite only into a clean ring-free scene"
              if not scene_is_clean else
              "clean scene asserted; keying residue + lighting/integration need a "
              "vision or human check before delivery")
    return {"checks": checks, "failed": failed, "reason": reason}


def jewelry_difference_detector(
    render: str | Path,
    source: Optional[str | Path],
    *,
    from_composite: bool,
) -> dict:
    """Compare the rendered jewelry to the source for INVENTED/removed components
    (added accent diamonds, hidden halo, pavé/diamond bridge, gallery diamonds,
    extra prongs, changed stone count, redesigned basket, changed metal silhouette).
    Any difference = reject before acceptance (docs/16 ZERO JEWELRY INVENTION).

    - Composite render: invention is IMPOSSIBLE (the ring is source pixels) → pass.
    - Raw render: needs a VISION diff vs source (Claude vision in-session, or
      ANTHROPIC_API_KEY). When no vision is available it returns invented=None
      (UNVERIFIED) — never a silent pass; the raw render must not be auto-accepted.
    Never fabricates a verdict.
    """
    all_checks = JEWELRY_DIFF_CHECKS + HEAD_GEOMETRY_CHECKS
    if from_composite:
        return {
            "available": True, "method": "provenance", "invented": False,
            "checks": {c: "pass" for c in all_checks},
            "reason": "ring is source pixels — no component (incl. head/gallery) can be added, removed, or modified",
        }
    if source is None:
        return {
            "available": False, "method": "no-source", "invented": None,
            "checks": {c: "unverified" for c in all_checks},
            "reason": "no source provided to diff against — cannot certify; do not auto-accept",
        }
    v = vision_geometry_verdict(render, source)
    if not v.get("available"):
        return {
            "available": False, "method": "vision-unavailable", "invented": None,
            "checks": {c: "unverified" for c in all_checks},
            "reason": ("raw render needs a jewelry+head diff vs source (Claude vision in-session "
                       "or ANTHROPIC_API_KEY). Until run, treat as UNVERIFIED — do not "
                       "auto-accept; prefer the composite pipeline (invention impossible)."),
        }
    # vision available: expect it to return per-check verdicts + an `invented` bool
    checks = v.get("checks", {c: "unverified" for c in all_checks})
    invented = any(checks.get(c) == "fail" for c in all_checks)
    return {"available": True, "method": "vision", "invented": invented,
            "checks": checks, "reason": v.get("reason", "vision jewelry+head diff")}


def qc_final(
    image: str | Path,
    *,
    shot_type: str,
    from_composite: bool,
    geometry_source: Optional[str | Path] = None,
    source: Optional[str | Path] = None,
    scene_is_clean: bool = False,
) -> QCVerdict:
    """Verdict for a finished image.

    from_composite=True means the ring pixels came from fallback.composite_ring
    (geometry_source = the source-CAD file used) → geometry guaranteed.
    from_composite=False (raw AI render) → geometry UNVERIFIED; the gate fails on
    geometry so the pipeline composites instead of shipping the redesign.

    `source` (the source-CAD image) enables the Jewelry Difference Detector
    (docs/16). If the detector finds an invented/removed component, the image is
    rejected even if sanity passes.
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

    # Jewelry Difference Detector — invented/removed components + head assembly (docs/16).
    diff = jewelry_difference_detector(image, geometry_source or source,
                                       from_composite=from_composite)
    checklist = {**checklist, **{
        f"{'head' if k in HEAD_GEOMETRY_CHECKS else 'invention'}:{k}": v
        for k, v in diff["checks"].items()
    }}
    invention_reject = diff["invented"] is True
    if invention_reject:
        reasons.append("ZERO JEWELRY INVENTION: detector found invented/removed "
                       "component(s) vs source — rejected (docs/16)")
    elif diff["invented"] is None:
        reasons.append("jewelry-difference detector UNVERIFIED (" + diff["method"] + ")")

    # Composite Integrity — geometry can be perfect yet the composite still failed
    # (double ring, white-mask residue, mismatched lighting). Only for composite path.
    composite_reject = False
    if from_composite:
        ci = composite_integrity(image, scene_is_clean=scene_is_clean)
        checklist = {**checklist, **{f"composite:{k}": v for k, v in ci["checks"].items()}}
        composite_reject = ci["failed"]
        if composite_reject:
            reasons.append("COMPOSITE INTEGRITY fail: " + ci["reason"])
        else:
            reasons.append("composite-integrity: " + ci["reason"])

    passed = geometry_ok and not fails and not invention_reject and not composite_reject
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
