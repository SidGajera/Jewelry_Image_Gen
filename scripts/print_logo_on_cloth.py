#!/usr/bin/env python3
"""
print_logo_on_cloth.py — Composite the LOCKED Lucent Carat Lab logo onto a
generated studio image so it looks PHYSICALLY PRINTED on the cloth (not a
floating sticker/watermark). 0 credits, logo pixels never repainted.

Policy (see docs/04_LOGO_WORKFLOW.md): the AI never renders the logo. Studio
shots are generated on clean white cloth; this script prints the official logo
onto the fabric locally, so the logo stays pixel-identical to the source asset.

How it stays "printed, not pasted":
  * The ink is blended into the cloth with a MULTIPLY-style operation, so the
    fabric texture and folds remain visible THROUGH the print.
  * The ink is modulated by the cloth's local brightness (it darkens in shadow,
    lightens on highlights) so studio lighting passes over it.
  * Optional displacement warps the print slightly along the cloth's fold map.
  * Placement is OFF-CENTER by default; partial crop/occlusion is fine.

USAGE:
  pip install pillow numpy
  python print_logo_on_cloth.py --image studio.png --logo assets/logo/logo_official_transparent.png \
         --scale 0.42 --pos lower-right --opacity 0.9 --displace 6
  # -> writes PRINTED_studio.png

  # regenerate the transparent logo from the original (non-destructive key):
  python print_logo_on_cloth.py --make-transparent --logo assets/logo/logo_official.png --out assets/logo/logo_official_transparent.png
"""
import argparse, os
import numpy as np
from PIL import Image, ImageFilter


def make_transparent(src, out):
    """Key ONLY the pure-white background to alpha=0. Logo ink pixels untouched."""
    im = Image.open(src).convert("RGB")
    a = np.asarray(im)
    mx = a.max(2).astype(int); mn = a.min(2).astype(int)
    bg = (mn >= 244) & ((mx - mn) <= 8)          # very bright AND near-neutral = cloth/white
    alpha = np.where(bg, 0, 255).astype("uint8")
    Image.fromarray(np.dstack([a, alpha]), "RGBA").save(out)
    print(f"wrote {out}: {(alpha==255).sum()} logo px preserved, {(alpha==0).sum()} keyed")


def resolve_pos(pos, W, H, lw, lh):
    presets = {
        "lower-right":  (0.62, 0.66),
        "lower-center": (0.50, 0.68),
        "lower-left":   (0.10, 0.66),
        "center-right": (0.60, 0.45),
    }
    if "," in pos:
        fx, fy = [float(v) for v in pos.split(",")]
    else:
        fx, fy = presets.get(pos, presets["lower-right"])
    # fx,fy = top-left of the logo as a fraction of the image
    return int(fx * W), int(fy * H)


def print_logo(image_path, logo_path, scale, pos, opacity, displace, out=None):
    base = Image.open(image_path).convert("RGB")
    W, H = base.size
    logo = Image.open(logo_path).convert("RGBA")

    # scale logo to `scale` of image width
    lw = int(W * scale); lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    x, y = resolve_pos(pos, W, H, lw, lh)
    x = max(0, min(x, W - 1)); y = max(0, min(y, H - 1))

    base_arr = np.asarray(base).astype(np.float32)

    # cloth region under the logo (clip to frame -> allows natural cropping)
    x2, y2 = min(x + lw, W), min(y + lh, H)
    lw_c, lh_c = x2 - x, y2 - y
    logo_arr = np.asarray(logo).astype(np.float32)[:lh_c, :lw_c, :]
    ink_rgb = logo_arr[..., :3]
    ink_a = (logo_arr[..., 3:4] / 255.0) * float(opacity)

    region = base_arr[y:y2, x:x2, :].copy()

    # local cloth brightness (0..1): print darkens/lightens with the fabric lighting
    lum = region.mean(2, keepdims=True) / 255.0

    # optional displacement along the cloth fold map (shift ink by local gradient)
    if displace and displace > 0:
        g = np.asarray(Image.fromarray(region.astype("uint8")).convert("L")
                       .filter(ImageFilter.GaussianBlur(3))).astype(np.float32)
        gy, gx = np.gradient(g)
        norm = float(displace) / (np.abs(np.stack([gx, gy])).max() + 1e-6)
        sx = np.clip(np.arange(lw_c)[None, :] + (gx * norm), 0, lw_c - 1).astype(int)
        sy = np.clip(np.arange(lh_c)[:, None] + (gy * norm), 0, lh_c - 1).astype(int)
        ink_rgb = ink_rgb[sy, sx]
        ink_a = ink_a[sy, sx]

    # MULTIPLY-style print: ink tints the cloth, modulated by local brightness so
    # the weave/folds/shadows remain visible through the print (not opaque).
    tint = ink_rgb / 255.0
    printed = region * ((1 - ink_a) + ink_a * tint * (0.55 + 0.45 * lum))
    base_arr[y:y2, x:x2, :] = np.clip(printed, 0, 255)

    out = out or ("PRINTED_" + os.path.basename(image_path))
    Image.fromarray(base_arr.astype("uint8")).save(out)
    print(f"wrote {out}  (logo at {x},{y} size {lw}x{lh}, opacity {opacity}, displace {displace})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--make-transparent", action="store_true")
    ap.add_argument("--image")
    ap.add_argument("--logo", required=True)
    ap.add_argument("--out")
    ap.add_argument("--scale", type=float, default=0.42)
    ap.add_argument("--pos", default="lower-right")
    ap.add_argument("--opacity", type=float, default=0.9)
    ap.add_argument("--displace", type=float, default=6)
    args = ap.parse_args()

    if args.make_transparent:
        make_transparent(args.logo, args.out or "assets/logo/logo_official_transparent.png")
    else:
        if not args.image:
            ap.error("--image is required unless --make-transparent")
        print_logo(args.image, args.logo, args.scale, args.pos,
                   args.opacity, args.displace, args.out)
