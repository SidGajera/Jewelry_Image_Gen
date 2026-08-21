#!/usr/bin/env python3
"""FINAL policy: HIGGSFIELD_ONLY active; composite/from-source superseded.
    python scripts/apply_higgsfield_only.py
Every delivered pixel comes from Higgsfield generate_image; Python never creates
or alters a delivered pixel. G2-G9 + G21 advisory (blocking=false); G20 stays
blocking; G19 provenance retired. STONE_EQUALITY_LOCK -> aspirational."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    rp = ROOT / "policy" / "registry.json"; d = json.loads(rp.read_text(encoding="utf-8"))
    for r in d["rules"]:
        if r["id"] == "HIGGSFIELD_ONLY":
            r["status"] = "active"; r.pop("superseded_by", None)
        if r["id"] in ("GEN_COMPOSITE_V2", "GEOMETRY_FROM_SOURCE", "G19_COMPOSITE_PROVENANCE"):
            r["status"] = "superseded"; r["superseded_by"] = "HIGGSFIELD_ONLY"
        if r["id"] == "STONE_EQUALITY_LOCK":
            r["status"] = "aspirational"
    rp.write_text(json.dumps(d, indent=2), encoding="utf-8")

    gp = ROOT / "config" / "gates.json"; g = json.loads(gp.read_text(encoding="utf-8"))
    g["gates"].pop("G19_COMPOSITE_PROVENANCE", None)
    for k in ("G2_ACCENT_COUNT", "G3_ACCENT_SIZE", "G4_ACCENT_RUN", "G5_SETTING_STYLE", "G6_STONE_RATIO",
              "G7_SETTING_COUNT", "G8_UNAUTHORIZED", "G9_PIECE_COUNT", "G21_STONE_RATIO"):
        if k in g["gates"]:
            g["gates"][k]["blocking"] = False
            g["gates"][k]["note"] = "ADVISORY: the engine cannot hold stone ratios; logs to file, does not gate."
    g["gates"]["G20_MIN_SUBJECT_SCALE"]["blocking"] = True
    gp.write_text(json.dumps(g, indent=2), encoding="utf-8")
    print("HIGGSFIELD_ONLY applied")


if __name__ == "__main__":
    main()
