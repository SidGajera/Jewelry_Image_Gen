#!/usr/bin/env python3
"""Decode all connector download_file_content temp blobs for a SKU to image files.

    python scripts/decode_drive_batch.py <SKU>

Scans the session tool-results dir for mcp-*download_file_content*.txt files
({content: base64, id, mimeType, title}), matches each blob's id against
build/<SKU>/source_ids.json ({filename: drive_id}), and writes the bytes to
workspace/golden/<SKU>/source/<sanitized>.jpg. Validates JPEG/PNG magic.
"""
import base64, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = Path.home() / ".claude" / "projects" / "D--Lucent-Image-generation"


def sanitize(name):
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", name)
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_").lower()
    return stem + ".jpg"


def main():
    sku = sys.argv[1]
    ids = json.loads((ROOT / "build" / sku / "source_ids.json").read_text(encoding="utf-8"))
    id2name = {v: k for k, v in ids.items()}
    out = ROOT / "workspace" / "golden" / sku / "source"
    out.mkdir(parents=True, exist_ok=True)
    blobs = sorted(PROJECT.glob("*/tool-results/*download_file_content*.txt"))
    seen, wrote = set(), 0
    for p in blobs:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        fid = d.get("id")
        if fid not in id2name or fid in seen:
            continue
        raw = base64.b64decode(d["content"])
        if not (raw[:3] == b"\xff\xd8\xff" or raw[:8] == b"\x89PNG\r\n\x1a\n"):
            print(f"SKIP {id2name[fid]}: not a JPEG/PNG ({raw[:4]!r})")
            continue
        fn = sanitize(id2name[fid])
        (out / fn).write_bytes(raw)
        seen.add(fid)
        wrote += 1
        print(f"ok  {fn}  ({len(raw)//1024}KB)  <- {id2name[fid]}")
    missing = [n for i, n in id2name.items() if i not in seen]
    print(f"{sku}: {wrote} images -> workspace/golden/{sku}/source/")
    for n in missing:
        print(f"MISSING {n}")


if __name__ == "__main__":
    main()
