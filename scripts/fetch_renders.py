#!/usr/bin/env python3
"""Download a SKU's completed renders into the delivery store.

    python scripts/fetch_renders.py <SKU> <history_json>

<history_json> is a Higgsfield show_generations dump ({items:[{id,status,results:{rawUrl}}]}).
Maps each manifest job_id -> its rawUrl, writes build/<SKU>/render_urls.json (URLs are
DATA in build/, never typed into a command), then downloads each completed slot to
deliveries/<SKU>/<slot>.png. Pending/failed jobs are skipped and reported. Download only.
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def main():
    sku, hist_path = sys.argv[1], sys.argv[2]
    manifest = json.loads((ROOT / "workspace" / "golden" / sku / f"manifest_{sku}.json").read_text(encoding="utf-8"))
    jobs = manifest["jobs"]  # {slot: job_id}
    hist = json.loads(Path(hist_path).read_text(encoding="utf-8"))
    by_id = {it["id"]: it for it in hist.get("items", [])}

    urls, pending = {}, []
    for slot, jid in jobs.items():
        it = by_id.get(jid)
        if not it or it.get("status") != "completed":
            pending.append((slot, jid, it.get("status") if it else "not_in_history"))
            continue
        url = (it.get("results") or {}).get("rawUrl")
        if url:
            urls[slot] = url
        else:
            pending.append((slot, jid, "no_url"))

    bd = ROOT / "build" / sku
    bd.mkdir(parents=True, exist_ok=True)
    (bd / "render_urls.json").write_text(json.dumps(urls, indent=2), encoding="utf-8")

    out = ROOT / "deliveries" / sku
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for slot, url in urls.items():
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as r:
            (out / f"{slot}.png").write_bytes(r.read())
        n += 1
        print(f"ok  {slot}")
    print(f"{sku}: downloaded {n}/{len(jobs)} -> deliveries/{sku}/")
    if pending:
        for slot, jid, st in pending:
            print(f"PENDING {slot} {jid[:8]} ({st})")


if __name__ == "__main__":
    main()
