#!/usr/bin/env python3
"""Download completed render URLs into the delivery store.
    python scripts/download_renders.py <SKU>
Reads workspace/golden/<SKU>/urls_<SKU>.json  {slot_filename: rawUrl}  and writes
deliveries/<SKU>/<slot_filename>.png. No pixels are altered; download only."""
import argparse, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("sku"); sku = ap.parse_args().sku
    m = json.loads((ROOT / "workspace" / "golden" / sku / f"urls_{sku}.json").read_text(encoding="utf-8"))
    out = ROOT / "deliveries" / sku; out.mkdir(parents=True, exist_ok=True)
    n = 0
    for name, url in m.items():
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            (out / f"{name}.png").write_bytes(r.read())
        n += 1
    print(f"{sku}: downloaded {n} renders -> deliveries/{sku}/")


if __name__ == "__main__":
    main()
