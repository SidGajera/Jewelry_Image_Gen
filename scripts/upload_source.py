#!/usr/bin/env python3
"""Upload a SKU's source CAD renders to Higgsfield via presigned PUT URLs.

    python scripts/upload_source.py <SKU>

Reads  build/<SKU>/upload_urls.json  -> [{"file","media_id","put_url"}...]
       (signed URLs are DATA written to build/ by the tool that produced them;
        they are never typed into a command).
Local source bytes live in workspace/golden/<SKU>/source/<file>.
PUTs each file, then writes build/<SKU>/source_media.json -> [{"file","media_id"}...]
for the caller to pass to media_confirm. No bytes are altered; upload only.
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    sku = sys.argv[1]
    bd = ROOT / "build" / sku
    jobs = json.loads((bd / "upload_urls.json").read_text(encoding="utf-8"))
    src = ROOT / "workspace" / "golden" / sku / "source"
    done = []
    for j in jobs:
        data = (src / j["file"]).read_bytes()
        req = urllib.request.Request(
            j["put_url"], data=data, method="PUT",
            headers={"Content-Type": j.get("content_type", "image/jpeg")})
        with urllib.request.urlopen(req, timeout=180) as r:
            status = r.status
        print(f'{j["file"]}  {j["media_id"]}  HTTP {status}')
        done.append({"file": j["file"], "media_id": j["media_id"], "status": status})
    (bd / "source_media.json").write_text(json.dumps(done, indent=2), encoding="utf-8")
    ok = sum(1 for d in done if d["status"] == 200)
    print(f"{sku}: {ok}/{len(done)} uploaded -> build/{sku}/source_media.json")


if __name__ == "__main__":
    main()
