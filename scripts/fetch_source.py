#!/usr/bin/env python3
"""Fetch a SKU's source CAD renders from Google Drive to disk (P1 READ_SOURCE).

    python scripts/fetch_source.py <SKU>

Reads build/<SKU>/source_ids.json -> {filename: drive_id} (IDs are DATA, never
typed into a command) and downloads each to workspace/golden/<SKU>/source/.
Redirect-following uc?export=download then thumbnail fallback; validates image
magic bytes. Download only; no bytes altered.
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
MAGIC = (b"\xff\xd8\xff", b"\x89PNG\r\n\x1a\n", b"RIFF", b"GIF8")


def _fetch(drive_id):
    for u in (f"https://drive.usercontent.google.com/download?id={drive_id}&export=download&confirm=t",
              f"https://drive.google.com/uc?export=download&id={drive_id}",
              f"https://drive.google.com/thumbnail?id={drive_id}&sz=w2000"):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except Exception:
            continue
        if data and any(data.startswith(m) for m in MAGIC):
            return data
    return None


def main():
    sku = sys.argv[1]
    ids = json.loads((ROOT / "build" / sku / "source_ids.json").read_text(encoding="utf-8"))
    out = ROOT / "workspace" / "golden" / sku / "source"
    out.mkdir(parents=True, exist_ok=True)
    ok = 0
    for name, fid in ids.items():
        data = _fetch(fid)
        if data:
            (out / name).write_bytes(data)
            ok += 1
            print(f"ok  {name}  {len(data)} bytes")
        else:
            print(f"FAIL {name} ({fid})")
    print(f"{sku}: {ok}/{len(ids)} source files -> workspace/golden/{sku}/source/")


if __name__ == "__main__":
    main()
