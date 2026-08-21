#!/usr/bin/env python3
"""
print_logo_on_cloth.py — Composite the LOCKED Lucent Carat Lab logo onto a
generated studio image so it looks PHYSICALLY PRINTED on the cloth (not a
floating sticker/watermark). 0 credits, logo pixels never repainted.

Policy (see docs/04_LOGO_WORKFLOW.md): the AI never renders the logo. Studio
shots are generated on clean white cloth; this script prints the official logo
onto the fabric locally, so the logo stays pixel-identical to the source asset.

How it stays "printed, not pasted" (six-point fabric-print realism standard):
  1. FABRIC INTERACTION — displacement warps the ink along the cloth's fold map
     so lines bend over folds instead of ignoring them.
  2. SOFT EDGES — the ink alpha is slightly blurred so no line is razor-crisp;
     a real print softens where ink meets fibre.
  3. WEAVE-THROUGH — the cloth's high-frequency weave texture is added back ON
     TOP of the ink, so the fabric grain runs visibly through the gold lines.
  4. EMBEDDED DEPTH — a faint inner shadow rings the ink edges (ink pressed into
     the weave) so the print sits IN the cloth, not floating above it.
  5. MATCHED LIGHTING — the ink is modulated by local cloth brightness AND
     clamped so a printed pixel can never be brighter than the cloth beneath it;
     the logo therefore shares the cloth's highlights/shadows, never its own.
  6. INK DIFFUSION — subtle per-pixel grain/opacity variation mimics the tiny
     imperfections of real fabric printing.
  Placement is OFF-CENTER by default; partial crop/occlusion is fine.

USAGE:
  pip install pillow numpy
  python print_logo_on_cloth.py --image studio.png --logo assets/logo/logo_official_transparent.png \
         --scale 0.42 --pos lower-right --opacity 0.9 --displace 6 --soften 1.0 --grain 0.06
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
    # Placements are deliberately EDGE-BIASED. The logo is secondary branding:
    # it should sit at the frame's margin, largely cropped away or lost in the
    # velvet's folds, never centred and never competing with the jewelry.
    presets = {
        # subtle set (default) - most of the lockup falls outside the frame
        # ~80-90% of the lockup falls outside the frame or into the folds
        "edge-lower-right": (0.90, 0.88),
        "edge-lower-left":  (-0.14, 0.88),
        "edge-upper-right": (0.90, -0.14),
        "edge-lower":       (0.34, 0.93),
        # legacy, more visible - only for a deliberate brand plate
        "lower-right":  (0.62, 0.66),
        "lower-center": (0.50, 0.68),
        "lower-left":   (0.10, 0.66),
        "center-right": (0.60, 0.45),
    }
    if "," in pos:
        fx, fy = [float(v) for v in pos.split(",")]
    else:
        fx, fy = presets.get(pos, presets["edge-lower-right"])
    # fx,fy = top-left of the logo as a fraction of the image; may be negative
    # so the lockup starts off-frame and is cropped by the edge (preferred look).
    return int(fx * W), int(fy * H)


def print_logo(image_path, logo_path, scale, pos, opacity, displace,
               soften=1.0, grain=0.06, out=None, fabric="velvet"):
    base = Image.open(image_path).convert("RGB")
    W, H = base.size
    logo = Image.open(logo_path).convert("RGBA")

    # scale logo to `scale` of image width
    lw = int(W * scale); lh = int(logo.height * lw / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    x, y = resolve_pos(pos, W, H, lw, lh)
    # Do NOT clamp a negative origin back into frame - that would pull an
    # intentionally cropped lockup fully into view. Instead crop the logo itself.
    crop_l = max(0, -x); crop_t = max(0, -y)
    x = max(0, x); y = max(0, y)
    x = min(x, W - 1); y = min(y, H - 1)

    base_arr = np.asarray(base).astype(np.float32)

    # cloth region under the logo (clip to frame -> allows natural cropping)
    x2, y2 = min(x + lw, W), min(y + lh, H)
    lw_c, lh_c = x2 - x, y2 - y
    logo_arr = np.asarray(logo).astype(np.float32)[crop_t:crop_t + lh_c, crop_l:crop_l + lw_c, :]
    lh_c, lw_c = logo_arr.shape[0], logo_arr.shape[1]
    x2, y2 = x + lw_c, y + lh_c
    ink_rgb = logo_arr[..., :3]
    ink_a = (logo_arr[..., 3:4] / 255.0) * float(opacity)

    region = base_arr[y:y2, x:x2, :].copy()

    # local cloth brightness (0..1): print darkens/lightens with the fabric lighting
    lum = region.mean(2, keepdims=True) / 255.0

    velvet = (fabric == "velvet")

    # (0) VELVET NAP MAP — velvet's look is driven by pile direction: where the nap
    # lies toward the light it flares bright, where it lies away it goes deep. That
    # sheen field is LOWER frequency than a cotton weave, so it is read from a
    # heavier blur and used to drive how the ink sits in the nap below.
    if velvet:
        nap = np.asarray(Image.fromarray(region.astype("uint8")).convert("L")
                         .filter(ImageFilter.GaussianBlur(9))).astype(np.float32)[..., None] / 255.0
        # normalise the sheen field about its own mean so flat-lit velvet is neutral
        sheen = np.clip(0.5 + (nap - float(nap.mean())) * 1.8, 0.0, 1.0)

    # (1) FABRIC INTERACTION — displacement along the cloth fold map (shift ink by gradient)
    if displace and displace > 0:
        # velvet drapes in softer, broader folds than cotton, so the fold map is read
        # at a coarser scale; otherwise the ink chases pile noise instead of folds.
        g = np.asarray(Image.fromarray(region.astype("uint8")).convert("L")
                       .filter(ImageFilter.GaussianBlur(7 if velvet else 3))).astype(np.float32)
        gy, gx = np.gradient(g)
        norm = float(displace) / (np.abs(np.stack([gx, gy])).max() + 1e-6)
        sx = np.clip(np.arange(lw_c)[None, :] + (gx * norm), 0, lw_c - 1).astype(int)
        sy = np.clip(np.arange(lh_c)[:, None] + (gy * norm), 0, lh_c - 1).astype(int)
        ink_rgb = ink_rgb[sy, sx]
        ink_a = ink_a[sy, sx]

    # (2) SOFT EDGES + (6) INK DIFFUSION — blur the ink alpha so no line is razor
    # crisp, then break it up with subtle per-pixel grain (printing imperfections).
    if soften and soften > 0:
        ink_a = np.asarray(Image.fromarray((ink_a[..., 0] * 255).astype("uint8"))
                           .filter(ImageFilter.GaussianBlur(float(soften)))
                           ).astype(np.float32)[..., None] / 255.0
    if grain and grain > 0:
        rng = np.random.default_rng(42)  # deterministic imperfections
        noise = 1.0 - float(grain) * rng.random((lh_c, lw_c, 1)).astype(np.float32)
        ink_a = ink_a * noise

    # (5) MATCHED LIGHTING — MULTIPLY-style print: ink tints the cloth, modulated by
    # local brightness so the weave/folds/shadows pass through the print.
    tint = ink_rgb / 255.0
    if velvet:
        # INK SITS IN THE NAP, NOT ON IT. Velvet pile absorbs ink far more than a
        # flat cotton weave: the print reads deeper in the nap's shadow side and is
        # allowed only a restrained lift where the pile catches light. The wider
        # coupling range (0.34..1.0 vs cotton's 0.55..1.0) is what stops the logo
        # reading as a decal laid over the fabric.
        printed = region * ((1 - ink_a) + ink_a * tint * (0.34 + 0.66 * lum * (0.55 + 0.45 * sheen)))
    else:
        printed = region * ((1 - ink_a) + ink_a * tint * (0.55 + 0.45 * lum))
    # clamp: a printed pixel can never be BRIGHTER than the cloth beneath it, so the
    # logo shares the cloth's own highlights instead of inventing its own lighting.
    printed = np.minimum(printed, region)

    # (3) TEXTURE-THROUGH — add the cloth's own texture back ON TOP of the ink so the
    # fabric visibly runs through the gold lines. Cotton contributes a crisp weave;
    # velvet contributes finer, softer pile noise, so it is sampled at a tighter
    # radius and pushed harder — on velvet the pile must read THROUGH the print or
    # the logo instantly looks like a sticker.
    blur = np.asarray(Image.fromarray(region.astype("uint8"))
                      .filter(ImageFilter.GaussianBlur(1.2 if velvet else 2))).astype(np.float32)
    hi_freq = region - blur                      # weave (cotton) / pile nap (velvet)
    printed = printed + hi_freq * ink_a * (0.85 if velvet else 0.6)

    # (4) EDGE INK ABSORPTION — a very faint DARKEN-ONLY halo where ink meets fibre
    # (foil settling into the weave). Deliberately darken-only and tiny: NO bright
    # bevel, NO relief, NO emboss/3D extrusion — the foil stays FLAT in the cloth.
    edge = np.asarray(Image.fromarray((ink_a[..., 0] * 255).astype("uint8"))
                      .filter(ImageFilter.FIND_EDGES)
                      .filter(ImageFilter.GaussianBlur(1.6 if velvet else 1))).astype(np.float32)[..., None] / 255.0
    # velvet fibres stand up around a printed edge and shade it slightly more than a
    # flat weave does — still darken-only, still no bevel/relief/emboss.
    printed = printed * (1 - (0.09 if velvet else 0.06) * edge)

    base_arr[y:y2, x:x2, :] = np.clip(printed, 0, 255)

    out = out or ("PRINTED_" + os.path.basename(image_path))
    Image.fromarray(base_arr.astype("uint8")).save(out)
    print(f"wrote {out}  (logo {x},{y} {lw}x{lh}, opacity {opacity}, displace {displace}, "
          f"soften {soften}, grain {grain})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--make-transparent", action="store_true")
    ap.add_argument("--image")
    ap.add_argument("--logo", required=True)
    ap.add_argument("--out")
    ap.add_argument("--fabric", choices=["velvet", "cotton"], default="velvet",
                    help="fabric profile; velvet is the locked default (docs/11)")
    ap.add_argument("--scale", type=float, default=0.24,
                    help="logo width as a fraction of the image; keep small - jewelry is the hero")
    ap.add_argument("--pos", default="edge-lower-right")
    ap.add_argument("--opacity", type=float, default=0.68)
    ap.add_argument("--displace", type=float, default=9)
    ap.add_argument("--soften", type=float, default=1.6, help="ink edge blur radius (px)")
    ap.add_argument("--grain", type=float, default=0.09, help="ink diffusion imperfection 0..1")
    args = ap.parse_args()

    if args.make_transparent:
        make_transparent(args.logo, args.out or "assets/logo/logo_official_transparent.png")
    else:
        if not args.image:
            ap.error("--image is required unless --make-transparent")
        print_logo(args.image, args.logo, args.scale, args.pos,
                   args.opacity, args.displace, args.soften, args.grain, args.out,
                   fabric=args.fabric)
