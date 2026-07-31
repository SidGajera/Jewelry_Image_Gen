#!/usr/bin/env python3
"""Register JEWELRY_PRESERVATION policy + G22 ring-scale-on-hand gate.
    python scripts/apply_jewelry_preservation.py"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    gp = ROOT / "config" / "gates.json"; g = json.loads(gp.read_text(encoding="utf-8"))
    g["gates"]["G22_STONE_WITHIN_FINGER"] = {"blocking": True, "kind": "ring_scale_on_hand", "tol": 1.05,
        "measures": "lifestyle: centre-stone width <= finger width (× tol); rejects oversized 'cocktail-huge' diamonds on the hand"}
    gp.write_text(json.dumps(g, indent=2), encoding="utf-8")

    rp = ROOT / "policy" / "registry.json"; d = json.loads(rp.read_text(encoding="utf-8"))
    ids = {r["id"] for r in d["rules"]}
    if "RING_SCALE_ON_HAND" not in ids:
        d["rules"].append({"id": "RING_SCALE_ON_HAND", "key": "plausibility.ring_scale", "precedence": 80,
            "statement": "on every on-hand/lifestyle image the ring is at true real-life scale: the centre stone sits WITHIN the finger's width (stone width <= finger width), never wider/oversized/cocktail-huge; an elongated stone spans ALONG the finger but must not overhang the finger sides. Reject if the diamond looks oversized for the hand.",
            "scope": "global", "enforced_by": ["G22_STONE_WITHIN_FINGER"], "origin": "user 2026-07-31",
            "failure_cases": ["diamond_oversized_on_hand", "stone_wider_than_finger"], "status": "active"})
    if "JEWELRY_PRESERVATION" not in ids:
        d["rules"].append({"id": "JEWELRY_PRESERVATION", "key": "geometry.preservation", "precedence": 100,
            "statement": "Jewellery redesign/redraw PROHIBITED: diamond shape/size/cut/facet/count/placement, prongs/setting/gallery/band and metalwork come ONLY from the source CAD, unchanged (target: D2D pixel-perfect), on EVERY image including lifestyle. Only the camera angle may change. Read ALL source angles before generating; never generate an angle without a source view. Materials must look 100% real (no plastic/CZ/CGI). Aspirational under HIGGSFIELD_ONLY (text-to-image cannot guarantee D2D); kept as the locked target and enforced where measurable (G22 scale, G20 framing, G12 marks, G-INVENT coverage).",
            "scope": "global", "enforced_by": ["G_INVENT", "G20_MIN_SUBJECT_SCALE", "G22_STONE_WITHIN_FINGER"],
            "origin": "user 2026-07-31", "failure_cases": ["jewellery_redrawn", "diamond_shape_changed", "stone_added_or_removed"], "status": "active"})
    rp.write_text(json.dumps(d, indent=2), encoding="utf-8")
    print("JEWELRY_PRESERVATION + G22 applied")


if __name__ == "__main__":
    main()
