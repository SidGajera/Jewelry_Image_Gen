#!/usr/bin/env python3
"""
composite_ring_into_scene.py — FALLBACK 1 of the geometry-immutable workflow
(docs/12 §A3, QUALITY_MEMORY id=geometry-immutable-auto-fallback).

When AI generation drifts the ring geometry, we do NOT ship a redesigned ring.
Instead we preserve the ORIGINAL jewelry exactly: cut the ring pixels out of the
source CAD image (which are byte-identical geometry) and composite them into the
AI-generated scene (clean studio cloth + hot-foil logo), matching scale, position,
contact shadow, and neutral colour. The ring geometry is then 100% identical to
source because these ARE the source pixels — only the scene around it is new.

Because the ring pixels are copied, this is limited to the camera angles the source
provides (typically top / 45 / side). For an angle the source lacks, use Fallback 2
(render that angle from the CAD model), then composite with this same script.

USAGE:
  pip install pillow numpy
  python composite_ring_into_scene.py \
      --scene   ai_scene_clean_cloth.png \
      --ring    source_ring_top.png \
      --scale   0.55 --pos 0.5,0.48 \
      --shadow  0.35 --match-white \
      --out     COMPOSITE_ring.png

Params:
  --scene       AI-generated background scene (clean cloth + logo, NO ring, or ring area free)
  --ring        source CAD image of the ring on a plain/near-white background
  --scale       ring width as a fraction of the scene width (default 0.5)
  --pos         center x,y of the ring as fractions of the scene (default 0.5,0.5)
  --key         background-key threshold 0..255 (near-white -> transparent, default 244)
  --feather     alpha edge feather radius px (default 1.5) — avoids a cut-out look
  --shadow      contact-shadow strength 0..1 (default 0.3); 0 disables
  --match-white neutralise the ring's white balance to the scene's (flag)
  --out         output path (default COMPOSITE_<ring>.png)

This never repaints ring pixels (only keys background, feathers the edge, and — if
--match-white — applies a single global neutral gain). Geometry is untouched.
"""
import argparse, os
import numpy as np
from PIL import Image, ImageFilter


def key_ring(ring_img, key, feather):
    """Alpha = 0 where near-white background, 255 on the ring. Feather the edge."""
    rgb = np.asarray(ring_img.convert("RGB")).astype(np.int32)
    mx = rgb.max(2); mn = rgb.min(2)
    bg = (mn >= key) & ((mx - mn) <= 12)          # bright AND near-neutral = background
    alpha = np.where(bg, 0, 255).astype("uint8")
    a = Image.fromarray(alpha, "L")
    # keep the largest opaque region only would need scipy; instead just feather edges
    if feather and feather > 0:
        a = a.filter(ImageFilter.GaussianBlur(float(feather)))
    return a


def bbox_of_alpha(a):
    arr = np.asarray(a)
    ys, xs = np.where(arr > 24)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1


def neutral_gain(ring_rgba, scene_rgb):
    """Scale ring RGB by a single gain so its bright (metal-highlight/near-white) point
    is neutral like the scene's white cloth. Global, geometry-preserving."""
    r = np.asarray(ring_rgba).astype(np.float32)
    a = r[..., 3] / 255.0
    opaque = a > 0.5
    if opaque.sum() == 0:
        return ring_rgba
    rgb = r[..., :3]
    # per-channel 95th percentile over opaque pixels = the ring's own "white"
    hi = np.array([np.percentile(rgb[..., c][opaque], 95) for c in range(3)]) + 1e-6
    target = hi.mean()                     # neutral grey target = mean of the three
    gain = np.clip(target / hi, 0.85, 1.18)  # gentle, bounded
    rgb2 = np.clip(rgb * gain, 0, 255)
    out = np.dstack([rgb2, r[..., 3]]).astype("uint8")
    return Image.fromarray(out, "RGBA")


def composite(scene_path, ring_path, scale, pos, key, feather, shadow, match_white, out=None):
    scene = Image.open(scene_path).convert("RGB")
    W, H = scene.size
    ring = Image.open(ring_path).convert("RGBA")

    alpha = key_ring(ring, key, feather)
    ring.putalpha(alpha)
    bb = bbox_of_alpha(alpha)
    if bb:
        ring = ring.crop(bb)                       # tight crop to the ring

    # scale ring to `scale` of scene width
    rw = int(W * scale); rh = int(ring.height * rw / ring.width)
    ring = ring.resize((rw, rh), Image.LANCZOS)

    if match_white:
        ring = neutral_gain(ring, np.asarray(scene))

    fx, fy = [float(v) for v in pos.split(",")] if "," in pos else (0.5, 0.5)
    cx, cy = int(fx * W), int(fy * H)
    x, y = cx - rw // 2, cy - rh // 2

    base = scene.convert("RGBA")

    # soft contact shadow under the ring (from its alpha, offset + blurred)
    if shadow and shadow > 0:
        sh = ring.split()[3].filter(ImageFilter.GaussianBlur(max(2, rw // 30)))
        sh = np.asarray(sh).astype(np.float32) * float(shadow)
        shadow_layer = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
        shadow_layer.putalpha(Image.fromarray(sh.astype("uint8"), "L"))
        off = max(2, rh // 40)
        base.alpha_composite(shadow_layer, (x + off // 2, y + off))

    base.alpha_composite(ring, (x, y))

    out = out or ("COMPOSITE_" + os.path.basename(ring_path))
    base.convert("RGB").save(out)
    print(f"wrote {out}  (ring {rw}x{rh} at center {fx},{fy}, shadow {shadow}, "
          f"match_white {match_white}) — geometry copied from source, unchanged")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True)
    ap.add_argument("--ring", required=True)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--pos", default="0.5,0.5")
    ap.add_argument("--key", type=int, default=244)
    ap.add_argument("--feather", type=float, default=1.5)
    ap.add_argument("--shadow", type=float, default=0.3)
    ap.add_argument("--match-white", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()
    composite(args.scene, args.ring, args.scale, args.pos, args.key,
              args.feather, args.shadow, args.match_white, args.out)
