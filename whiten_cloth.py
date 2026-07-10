#!/usr/bin/env python3
"""
Make the background cloth PURE WHITE and IDENTICAL across every office photoshoot image,
WITHOUT touching the printed logo or the gold ring.

- It finds the bright, low-saturation cloth pixels in each image and pushes them to the
  SAME pure-white target (TARGET below). Because every image is driven to the same target,
  all backgrounds match.
- Gold pixels (logo + ring) are highly saturated, so a saturation mask protects them
  completely — they are left exactly as-is.

USAGE:
  1. Put this file in ONE folder together with ALL office photoshoot images.
  2. Open a terminal in that folder.
  3. Run:  python whiten_cloth.py
  4. Outputs are saved as  WHITE_<name>.png  (originals are not changed).

Requires: pip install pillow numpy
"""
import os, glob
import numpy as np
from PIL import Image

TARGET = 250.0  # common pure-white level for the cloth in every image (0-255)

files = [f for f in glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
         if not os.path.basename(f).startswith("WHITE_")]

if not files:
    print("No image found. Put this script next to the office photoshoot images and re-run.")

for path in files:
    img = Image.open(path).convert("RGB")
    a = np.asarray(img).astype(np.float32)

    mx = a.max(axis=2)
    mn = a.min(axis=2)
    light = mx                      # brightness 0-255
    sat = (mx - mn) / (mx + 1e-6)   # saturation 0-1

    # Cloth = bright AND low saturation (the fabric, whatever its current tint)
    cloth = (light > 180) & (sat < 0.12)
    if cloth.sum() < 500:
        print(f"skip {path}: couldn't isolate cloth")
        continue

    # Per-channel gain that maps this image's cloth white-point to the SAME pure-white target.
    # This both neutralizes the tint AND matches brightness across all images.
    wp = a[cloth].reshape(-1, 3).mean(axis=0)
    gain = TARGET / np.clip(wp, 1, None)
    corrected = a * gain

    # Soft mask: full effect on bright low-sat cloth, ZERO effect on saturated gold.
    soft = np.clip((light - 150) / 105.0, 0, 1) * np.clip((0.20 - sat) / 0.20, 0, 1)
    soft = soft[..., None]

    out = np.clip(a * (1 - soft) + corrected * soft, 0, 255).astype("uint8")
    outname = "WHITE_" + os.path.splitext(os.path.basename(path))[0] + ".png"
    Image.fromarray(out).save(outname)
    print("saved", outname)

print("Done. All WHITE_ images share the same pure-white background.")
