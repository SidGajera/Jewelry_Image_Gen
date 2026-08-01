#!/usr/bin/env python3
"""Normalize the 'model' field in every specs/<SKU>.json to the locked Nano Banana 2
string from config/model.json (MODEL_LOCK, user 2026-08-01). Removes any banned
inline model string (nano_banana_pro / seedream_v5_pro / ...) from spec configs.

Run-record files (workspace/golden/**/manifest_*.json) are LEFT UNTOUCHED on purpose:
a manifest must record the model ACTUALLY used, and a manifest showing a non-locked
model is the signal that that catalog needs regeneration (rule 5).

    python scripts/normalize_model.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCKED = json.loads((ROOT / "config" / "model.json").read_text(encoding="utf-8"))["model"]

changed = 0
for p in sorted((ROOT / "specs").glob("*.json")):
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    if spec.get("model") != LOCKED:
        spec["model"] = LOCKED
        p.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
        changed += 1
        print(f"fixed {p.name}")
print(f"specs normalized to '{LOCKED}': {changed} changed")
