#!/usr/bin/env python3
"""Measure each render gate against PER-GATE goldens so promotion to BLOCKING is
earned, not guessed. Goldens are per-GATE, not per-image: one render can be
geometrically perfect yet compositionally wrong (e.g. an angle failure), so each
case declares a verdict ONLY for the gates it actually verifies. Gates not listed
in a case are ignored for that case — unverified, never assumed.

Golden layout:
  tests/golden/pass_<sku>_<slot>/<slot>_case.png + case.json
    case.json: {"sku":"LR-0206","slot":"04",
                "expect":{"G6_primary_ratio":"PASS","G2_accent_count":"PASS","G10_angle":"FAIL"}}
  tests/golden/cases.json  (legacy FAIL-case file: {gate, expect} -> one verdict; still read)

Scoring, PER GATE, only over cases that declare a verdict for it:
  TP   declared FAIL and gate fired fail
  FN   declared FAIL and gate did NOT fire
  FP   declared PASS and gate fired fail          (MUST be 0 to promote)
  LOWC declared case where gate was unmeasurable
Promotable when: FP==0 AND FN==0 AND TP>0 AND LOWC/declared < 10%.
Reports only; never edits config/gates.json.

Usage: python scripts/calibrate.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import validate_render as vr  # noqa: E402

GDIR = ROOT / "tests" / "golden"


def _slot(sku, slotid):
    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    spec = json.loads((ROOT / "specs" / f"{sku}.json").read_text(encoding="utf-8"))
    return {s["slot"]: s for s in matrix["categories"][spec["category"]]["slots"]}[slotid]


def _canon_map():
    """Map a golden's gate key (e.g. 'G6_primary_ratio') to the code gate name
    (e.g. 'G6_STONE_RATIO') by the G-number prefix."""
    gates = json.loads((ROOT / "config" / "gates.json").read_text(encoding="utf-8"))["gates"]
    return {g.split("_")[0]: g for g in gates}, gates


def _norm(key, canon):
    return canon.get(key.split("_")[0].upper(), key)


def _gate_status(res, gate):
    hits = [r for r in res if r["gate"] == gate]
    if any(h["status"] == "fail" for h in hits):
        return "fail"
    if hits and not any(h["status"] == "pass" for h in hits) and any(h["status"] == "unmeasurable" for h in hits):
        return "lowc"
    if hits and all(h["status"] in ("pass", "skip") for h in hits):
        return "pass"
    return "skip"


def collect(canon):
    cases = []
    # per-gate PASS/FAIL goldens
    for d in sorted(GDIR.glob("pass_*")):
        cj = d / "case.json"
        imgs = list(d.glob("*_case.png"))
        if not cj.exists() or not imgs:
            continue
        meta = json.loads(cj.read_text(encoding="utf-8"))
        expect = {_norm(k, canon): v.upper() for k, v in meta.get("expect", {}).items()}
        cases.append({"sku": meta["sku"], "slot": meta["slot"], "image": imgs[0], "expect": expect})
    # legacy FAIL-case file -> single-gate verdict
    fc = json.loads((GDIR / "cases.json").read_text(encoding="utf-8")).get("cases", [])
    for c in fc:
        img = GDIR / c["image"] if c.get("image") else None
        if not (img and img.exists()):
            continue
        g = _norm(c["gate"], canon)
        cases.append({"sku": c["sku"], "slot": c["slot"], "image": img,
                      "expect": {g: c.get("expect", "fail").upper()}})
    return cases


def main():
    canon, gates_cfg = _canon_map()
    cases = collect(canon)
    per = {g: {"tp": 0, "fn": 0, "fp": 0, "lowc": 0, "declared": 0} for g in gates_cfg}
    for c in cases:
        res = vr.validate_image(c["sku"], c["image"], _slot(c["sku"], c["slot"]))
        for g, verdict in c["expect"].items():
            if g not in per:
                continue
            st = _gate_status(res, g)
            per[g]["declared"] += 1
            if st == "lowc":
                per[g]["lowc"] += 1
            if verdict == "PASS" and st == "fail":
                per[g]["fp"] += 1
            if verdict == "FAIL":
                per[g]["tp" if st == "fail" else "fn"] += 1

    total_declared = sum(s["declared"] for s in per.values())
    print(f"golden verdicts: {total_declared} across {len(cases)} cases")
    print(f"\n{'gate':<18}{'block':<7}{'decl':<6}{'TP':<5}{'FN':<5}{'FP':<5}{'LOWC%':<7}promotable")
    for g, cfg in gates_cfg.items():
        s = per[g]
        d = s["declared"]
        lowc = (s["lowc"] / d * 100) if d else 0
        has_pass = any(v == "PASS" for c in cases for k, v in c["expect"].items() if _norm(k, canon) == g)
        promotable = (d > 0 and has_pass and s["fp"] == 0 and s["fn"] == 0 and s["tp"] > 0 and lowc < 10)
        flag = "YES" if promotable else ("" if cfg["blocking"] else ("no" if d else "no-data"))
        print(f"{g:<18}{str(cfg['blocking']):<7}{d:<6}{s['tp']:<5}{s['fn']:<5}{s['fp']:<5}{lowc:<7.0f}{flag}")
    print("\nPromote a gate in config/gates.json only when promotable=YES; record its rates in memory/failures.json.")
    print("A gate with no PASS verdict declared cannot be promoted (false-positive rate is unmeasurable).")


if __name__ == "__main__":
    main()
