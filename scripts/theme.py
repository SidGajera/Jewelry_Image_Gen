#!/usr/bin/env python3
"""Deterministic per-catalog theme assignment (lifestyle only; studio stays
locked white velvet). theme = pool[sha256(SKU) % len(pool)], then walk forward
to the next theme not used in the last 6 catalogs. Deterministic: a re-run of
the same SKU gets the same theme (the ledger is keyed by SKU). No Date.now in
code — pass the date in when recording.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POOL = ROOT / "config" / "themes.json"
LEDGER = ROOT / "memory" / "theme_ledger.json"


def _pool():
    return json.loads(POOL.read_text(encoding="utf-8"))


def _ledger():
    if LEDGER.exists():
        try:
            return json.loads(LEDGER.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def assign(sku):
    pool = _pool()
    led = _ledger()
    # deterministic: if this SKU already has a theme, reuse it
    for e in led:
        if e["sku"] == sku:
            return next((t for t in pool if t["id"] == e["theme_id"]), pool[0])
    base = int(hashlib.sha256(sku.encode()).hexdigest(), 16) % len(pool)
    last6 = {e["theme_id"] for e in led[-6:]}
    for k in range(len(pool)):
        t = pool[(base + k) % len(pool)]
        if t["id"] not in last6:
            return t
    return pool[base]  # all recently used (pool <=6); fall back to hash pick


def record(sku, theme_id, date, sig=None):
    led = [e for e in _ledger() if e["sku"] != sku]  # keep deterministic on re-run
    led.append({"sku": sku, "theme_id": theme_id, "date": date, "sig": sig})
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(led, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import sys
    print(json.dumps(assign(sys.argv[1] if len(sys.argv) > 1 else "LR-0205"), indent=2))
