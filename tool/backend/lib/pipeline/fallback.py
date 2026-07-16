"""fallback.py — the geometry-immutable composite engine (default preservation path).

Five outputs across four SKUs proved that AI generation re-synthesizes the ring
and cannot hold CAD geometry. The only guarantee is to NOT let the model draw the
ring: generate the scene (cloth / hand / environment) with AI, then composite the
REAL source-CAD ring pixels into it. The ring in the final image is then 100%
identical to source by construction — these ARE the source pixels.

This module loads the two locked scripts as importable functions and exposes a
clean API for the pipeline. The scripts remain the single source of truth:
  scripts/composite_ring_into_scene.py  (FALLBACK 1 — exact source ring into scene)
  scripts/print_logo_on_cloth.py        (two-tone hot-foil logo, studio only)

Nothing here repaints ring geometry — it keys the source ring's background,
feathers the edge, scales/places it, adds a contact shadow, and optionally
neutralises white balance. See docs/13_JEWELRY_PRESERVATION_SPEC.md §6.
"""
from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import config  # repo config + canonical SCRIPTS paths
from lib.config.paths import PATHS

_MODCACHE: dict[str, object] = {}


def _load_script(name: str, path: Path):
    """Import a repo script by path once and cache it (keeps scripts authoritative)."""
    if name in _MODCACHE:
        return _MODCACHE[name]
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load script {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    _MODCACHE[name] = mod
    return mod


@dataclass
class CompositeResult:
    out_path: Path
    ring_px: tuple[int, int]          # rendered ring size in px (w, h)
    pos: tuple[float, float]          # center as fractions of the scene
    shadow: float
    match_white: bool
    geometry_source: str              # the source-ring file whose pixels were used
    note: str = "ring geometry copied from source — unchanged"


def composite_ring(
    scene: str | Path,
    ring: str | Path,
    out: str | Path,
    *,
    scale: float = 0.5,
    pos: str = "0.5,0.5",
    key: int = 244,
    feather: float = 1.5,
    shadow: float = 0.3,
    match_white: bool = True,
) -> CompositeResult:
    """Composite the exact source-CAD ring into an AI-generated scene.

    scene       AI scene (cloth/hand/environment) with the ring area free.
    ring        source-CAD ring image on a plain/near-white background.
    out         output path (parents created).
    scale/pos   ring width as a fraction of scene width; center x,y fractions.
    shadow      contact-shadow strength 0..1 (0 disables).
    match_white neutralise the ring's white balance to the scene's.
    Returns a CompositeResult with provenance for QC. Geometry is never repainted.
    """
    mod = _load_script("composite_ring_into_scene", config.SCRIPTS["composite_ring"])
    scene, ring, out = Path(scene), Path(ring), Path(out)
    for p in (scene, ring):
        if not p.exists():
            raise FileNotFoundError(p)
    out.parent.mkdir(parents=True, exist_ok=True)

    mod.composite(  # type: ignore[attr-defined]
        str(scene), str(ring),
        scale=scale, pos=pos, key=key, feather=feather,
        shadow=shadow, match_white=match_white, out=str(out),
    )
    if not out.exists():
        raise RuntimeError(f"composite did not produce {out}")

    # recompute the rendered ring size the same way the script does, for provenance
    from PIL import Image
    with Image.open(scene) as s:
        W = s.size[0]
    rw = int(W * scale)
    fx, fy = (float(v) for v in pos.split(",")) if "," in pos else (0.5, 0.5)
    with Image.open(ring) as r:
        rh = int(r.height * rw / r.width)

    return CompositeResult(
        out_path=out, ring_px=(rw, rh), pos=(fx, fy),
        shadow=shadow, match_white=match_white, geometry_source=str(ring),
    )


def print_logo(
    image: str | Path,
    out: str | Path,
    *,
    logo: Optional[str | Path] = None,
    scale: float = 0.42,
    pos: str = "lower-right",
    opacity: float = 0.9,
    displace: float = 6.0,
    soften: float = 1.0,
    grain: float = 0.06,
) -> Path:
    """Stamp the locked two-tone logo INTO a studio cloth image (studio shots only).

    Delegates to scripts/print_logo_on_cloth.py so the six-point fabric-print
    realism (docs/04 §4) stays authoritative. Lifestyle/close-up shots carry no
    logo — do not call this for them.
    """
    mod = _load_script("print_logo_on_cloth", config.SCRIPTS["print_logo"])
    image, out = Path(image), Path(out)
    logo_path = Path(logo) if logo else (PATHS.logo_dir / "logo_official_transparent.png")
    if not image.exists():
        raise FileNotFoundError(image)
    if not logo_path.exists():
        raise FileNotFoundError(logo_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # print_logo_on_cloth.py:
    #   print_logo(image_path, logo_path, scale, pos, opacity, displace, soften, grain, out)
    fn = getattr(mod, "print_logo", None)
    if fn is None:
        raise AttributeError("print_logo_on_cloth.py has no print_logo entrypoint")
    fn(
        image_path=str(image), logo_path=str(logo_path),
        scale=scale, pos=pos, opacity=opacity,
        displace=displace, soften=soften, grain=grain, out=str(out),
    )
    if not out.exists():
        raise RuntimeError(f"logo print did not produce {out}")
    return out


def _cli() -> None:
    """Manual compositing entrypoint — for DEBUGGING only (per the locked policy,
    the pipeline composites automatically; running this by hand is for inspection)."""
    import argparse
    ap = argparse.ArgumentParser(description="Manual composite (debug). Pipeline does this automatically.")
    ap.add_argument("--scene", required=True)
    ap.add_argument("--ring", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--pos", default="0.5,0.5")
    ap.add_argument("--shadow", type=float, default=0.3)
    ap.add_argument("--feather", type=float, default=1.5)
    ap.add_argument("--key", type=int, default=244)
    ap.add_argument("--no-match-white", action="store_true")
    a = ap.parse_args()
    res = composite_ring(
        a.scene, a.ring, a.out, scale=a.scale, pos=a.pos, key=a.key,
        feather=a.feather, shadow=a.shadow, match_white=not a.no_match_white,
    )
    print(f"OK  {res.out_path}  ring {res.ring_px[0]}x{res.ring_px[1]}  "
          f"geometry_source={Path(res.geometry_source).name}  ({res.note})")


if __name__ == "__main__":
    _cli()
