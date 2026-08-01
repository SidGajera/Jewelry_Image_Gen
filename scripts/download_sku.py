#!/usr/bin/env python3
"""Download a SKU's completed renders into the category-wise delivery store.

    python scripts/download_sku.py <SKU> [category]

Reads workspace/golden/<SKU>/manifest_<SKU>.json (slots[] + optional superseded_jobs),
auto-discovers the newest show_generations dump under the session tool-results dir,
maps each job_id -> its render URL + status, writes build/<SKU>/render_urls.json
(URLs are DATA in build/, never typed into a command), then downloads each COMPLETED
slot to deliveries/<category>/<SKU>/<slot>.png. Pending/failed skipped and reported.
Download only; no pixel writes to jewellery.
"""
import json, sys, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = Path.home() / ".claude" / "projects" / "D--Lucent-Image-generation"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
CAT = {"LR": "Rings", "BR": "Bracelets", "NR": "Necklaces", "ER": "Earrings"}


def newest_dump():
    cands = list(PROJECT.glob("*/tool-results/*show_generations*.txt"))
    if not cands:
        sys.exit("FAIL: no show_generations dump found under tool-results/")
    return max(cands, key=lambda p: p.stat().st_mtime)


def result_url(item):
    """Return the RENDER URL from an item's results ONLY.
    Never falls back to params.input_images[].url (that is the SOURCE image, 794x446)."""
    res = item.get("results") or {}
    if isinstance(res, list):
        res = res[0] if res else {}
    for k in ("rawUrl", "raw_url", "url", "image_url", "output_url", "minUrl"):
        v = res.get(k) if isinstance(res, dict) else None
        if isinstance(v, str) and re.match(r"^https?://", v):
            return v
    return None


def main():
    sku = sys.argv[1]
    cat = sys.argv[2] if len(sys.argv) > 2 else CAT.get(sku[:2], "Other")
    man = json.loads((ROOT / "workspace" / "golden" / sku / f"manifest_{sku}.json").read_text(encoding="utf-8"))

    want = {}  # slot_label -> job_id
    for s in man.get("slots", []):
        want[s["slot"]] = s["job"]
    for i, jid in enumerate(man.get("superseded_jobs", {}).get("jobs", []), 1):
        want[f"superseded_{i:02d}_{jid[:8]}"] = jid

    dump = json.loads(newest_dump().read_text(encoding="utf-8"))
    items = dump.get("items", dump if isinstance(dump, list) else [])
    idx = {}
    for it in items:
        jid = it.get("id")
        if jid:
            idx[jid] = (it.get("status"), result_url(it))

    urls, pending = {}, []
    for label, jid in want.items():
        st, url = idx.get(jid, ("not_in_history", None))
        # match on job-id prefix too (dumps sometimes key by full/prefix)
        if url is None and st == "not_in_history":
            for k, (s2, u2) in idx.items():
                if k.startswith(jid[:12]) or jid.startswith(k[:12]):
                    st, url = s2, u2
                    break
        if url and (st in (None, "completed", "success", "done")):
            urls[label] = url
        else:
            pending.append((label, jid[:8], st))

    bd = ROOT / "build" / sku
    bd.mkdir(parents=True, exist_ok=True)
    (bd / "render_urls.json").write_text(json.dumps(urls, indent=2), encoding="utf-8")

    out = ROOT / "deliveries" / cat / sku
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for label, url in urls.items():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                (out / f"{label}.png").write_bytes(r.read())
            n += 1
            print(f"ok  {label}")
        except Exception as e:
            print(f"ERR {label}: {e}")
    print(f"{sku}: downloaded {n}/{len(want)} -> deliveries/{cat}/{sku}/")
    for label, jid, st in pending:
        print(f"PENDING {label} {jid} ({st})")


if __name__ == "__main__":
    main()
