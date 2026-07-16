#!/usr/bin/env python3
"""One-off (LR-0151 side angles): clean re-cut of the source ring from the CAD
render + build a ring-free branded-cloth plate + composite. Geometry = source pixels.
Not part of the permanent pipeline; kept for reproducibility of this fix.
"""
import numpy as np, cv2
from PIL import Image, ImageFilter

GOLD = 'workspace/golden/round-solitaire-pave-yg'
PLATE = 'assets/background/sample_studio_background_with_logo.png'
OUT = 'workspace/output'
import os; os.makedirs(OUT, exist_ok=True)


def recut(src_path, hole_seeds):
    """Return RGBA PIL image: exterior white + finger-hole + CAD drop-shadow removed,
    ring (metal + diamonds) kept. Shadow is dropped by clipping to the ring's own
    metal/bright hull (the neutral-gray floor shadow lies outside that hull)."""
    bgr = cv2.imread(src_path)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    H, W, _ = rgb.shape
    R, G, B = rgb[..., 0].astype(int), rgb[..., 1].astype(int), rgb[..., 2].astype(int)
    mx = rgb.max(2).astype(int); mn = rgb.min(2).astype(int)
    near_white = (mn >= 236) & ((mx - mn) <= 12)

    # ---- exterior + finger hole (near-white connected regions) ----
    nw = near_white.astype('uint8')
    _, labels = cv2.connectedComponents(nw, connectivity=4)
    transparent = np.zeros((H, W), bool)
    border = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    for lb in border:
        if lb != 0:
            transparent |= (labels == lb)
    for (fx, fy) in hole_seeds:
        lb = labels[int(fy * H), int(fx * W)]
        if lb != 0:
            transparent |= (labels == lb)

    # ---- ring body hull from gold-metal | very-bright-diamond (excludes gray shadow) ----
    gold = (R > 90) & (R >= G) & (G >= B) & (R - B > 14)
    vbright = mn >= 228
    body = ((gold | vbright) & ~near_white).astype('uint8')
    body = cv2.morphologyEx(body, cv2.MORPH_CLOSE, np.ones((9, 9), 'uint8'), iterations=2)
    ncc, lab2, stats, _ = cv2.connectedComponentsWithStats(body, connectivity=8)
    if ncc > 1:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        hull = (lab2 == biggest).astype('uint8')
    else:
        hull = body
    # fill interior holes of the hull so dark facets / open basket interior metal stay solid
    ff = hull.copy(); h2, w2 = ff.shape
    m = np.zeros((h2 + 2, w2 + 2), 'uint8')
    cv2.floodFill(ff, m, (0, 0), 1)
    hull_filled = hull | (1 - ff)
    hull_filled = cv2.dilate(hull_filled, np.ones((5, 5), 'uint8'), iterations=1)

    keep = (~transparent) & (hull_filled > 0)
    alpha = np.where(keep, 255, 0).astype('uint8')
    a = Image.fromarray(alpha, 'L').filter(ImageFilter.GaussianBlur(0.8))
    out = np.dstack([rgb, np.asarray(a)]).astype('uint8')
    return Image.fromarray(out, 'RGBA')


def build_plate(plate_path, upscale=2048):
    """Remove the oval halo ring (upper-left) from the sample, keep cloth + logo."""
    bgr = cv2.imread(plate_path)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    H, W, _ = rgb.shape
    # Remove the oval halo ring with a DIFFUSION FILL: only clean cloth colour from the
    # (fully-clean) boundary is diffused inward, so no ring pixel — gold, diamond dispersion,
    # shadow — can be propagated (inpaint produced rainbow streaks; this cannot). Result is a
    # smooth shallow-DoF cloth tone behind the openwork ring. Logo box is hard-protected.
    cx, cy = int(0.37 * W), int(0.42 * H)
    ax, ay = int(0.37 * W), int(0.30 * H)
    mask = np.zeros((H, W), 'uint8')
    cv2.ellipse(mask, (cx, cy), (ax, ay), 0, 0, 360, 255, -1)
    logo = (slice(int(0.60 * H), H), slice(int(0.40 * W), W))   # protect hot-foil logo
    mask[logo] = 0
    m = mask > 0
    fill = rgb.astype(np.float32).copy()
    sigma = max(6, W / 55.0)
    for _ in range(140):                       # harmonic-style fill from clean boundary
        blur = cv2.GaussianBlur(fill, (0, 0), sigma)
        fill[m] = blur[m]
    a = cv2.GaussianBlur(m.astype('float32'), (0, 0), max(10, W / 40.0))
    a = np.clip(a / max(a.max(), 1e-6), 0, 1)[..., None]
    # subtle grain so the fill doesn't read as a dead-flat patch
    rng = np.zeros_like(fill); cv2.randn(rng, 0, 2.5)
    fill = np.clip(fill + rng, 0, 255)
    plate = (fill * a + rgb.astype(np.float32) * (1 - a)).astype('uint8')
    pim = Image.fromarray(plate, 'RGB')
    if upscale:
        pim = pim.resize((upscale, upscale), Image.LANCZOS)
    return pim


def neutral_gain(ring):
    r = np.asarray(ring).astype(np.float32); a = r[..., 3] / 255.0
    op = a > 0.5
    if op.sum() == 0: return ring
    rgb = r[..., :3]
    hi = np.array([np.percentile(rgb[..., c][op], 95) for c in range(3)]) + 1e-6
    gain = np.clip(hi.mean() / hi, 0.9, 1.12)
    rgb2 = np.clip(rgb * gain, 0, 255)
    return Image.fromarray(np.dstack([rgb2, r[..., 3]]).astype('uint8'), 'RGBA')


def composite(plate, ring, scale, pos, shadow, out_path):
    W, Hh = plate.size
    bb = ring.getbbox(); ring = ring.crop(bb)
    ring = neutral_gain(ring)
    rw = int(W * scale); rh = int(ring.height * rw / ring.width)
    ring = ring.resize((rw, rh), Image.LANCZOS)
    fx, fy = pos
    cx, cy = int(fx * W), int(fy * Hh)
    x, y = cx - rw // 2, cy - rh // 2
    base = plate.convert('RGBA')
    if shadow > 0:
        sh = ring.split()[3].filter(ImageFilter.GaussianBlur(max(3, rw // 22)))
        arr = (np.asarray(sh).astype(np.float32) * shadow).astype('uint8')
        layer = Image.new('RGBA', (rw, rh), (30, 26, 20, 0)); layer.putalpha(Image.fromarray(arr, 'L'))
        off = max(3, rh // 34)
        base.alpha_composite(layer, (x + off // 3, y + off))
    base.alpha_composite(ring, (x, y))
    base.convert('RGB').save(out_path, quality=95)
    print('wrote', out_path, 'ring', rw, 'x', rh, 'at', pos)


plate = build_plate(PLATE)
plate.convert('RGB').save(f'{OUT}/_plate_clean.png')

# True 90 side profile (r97_8): band-circle interior seeds
ring_side = recut(f'{GOLD}/r97_8.jpg', hole_seeds=[(0.50, 0.62), (0.50, 0.70), (0.50, 0.55)])
ring_side.save(f'{OUT}/_ring_side_cut.png')
# 45 three-quarter (r97_4): interior of the tilted band
ring_45 = recut(f'{GOLD}/r97_4.jpg', hole_seeds=[(0.55, 0.66), (0.60, 0.70), (0.50, 0.72)])
ring_45.save(f'{OUT}/_ring_45_cut.png')

# Composite onto the branded plate at the sample's proven footprint (logo kept clear)
composite(plate, ring_side, scale=0.46, pos=(0.40, 0.42), shadow=0.30, out_path=f'{OUT}/LR-0151_studio_side_profile.png')
# r97_4 is a tall/narrow standing view (aspect ~1.87); scale smaller so the hero stone
# is fully in-frame and the ring stays clear of the hot-foil logo.
composite(plate, ring_45,   scale=0.32, pos=(0.34, 0.44), shadow=0.30, out_path=f'{OUT}/LR-0151_studio_45.png')
print('DONE')
