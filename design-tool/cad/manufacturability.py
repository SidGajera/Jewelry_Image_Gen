#!/usr/bin/env python3
"""
Manufacturability rules + cost estimator for a design-DNA parameter set.

Pure standard-library Python (no deps). This is the "back end" of the pipeline
(layer 5): given a design-DNA JSON it (a) checks castability rules and (b)
estimates cost -> suggested retail. Same logic the web configurator uses.

Usage:
    python manufacturability.py ../examples/lr-0200-duality.json
    python manufacturability.py path/to/design.json --size 6.5
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(HERE, "..", "schema")


def load(name):
    with open(os.path.join(SCHEMA_DIR, name)) as f:
        return json.load(f)


PRICING = load("pricing.json")
RATIOS = load("cut-ratios.json")["cuts"]

# --- castability limits (mm) ---
MIN_WALL_MM = 0.70          # min metal wall for reliable casting in gold
MIN_PRONG_DIA_MM = 0.90     # min prong diameter for security
MIN_BAND_WIDTH_MM = 1.00


def stone_mm(cut, carat, lw):
    """Approximate finished dimensions from carat + ratio (indicative)."""
    if cut == "round":
        d = 6.5 * (carat ** (1 / 3.0))
        return (round(d, 1), round(d, 1))
    L = 5.55 * math.sqrt(carat * lw)
    return (round(L, 1), round(L / lw, 1))


def metal_weight_g(dna):
    band = dna["band"]
    pf = PRICING["band_profile_weight_factor"].get(band["profile"], 1.0)
    wt = pf * (0.7 + band["width_mm"] * 0.52)
    if dna["centre"]["setting"] in ("bezel", "half_bezel"):
        wt += 0.5
    return round(wt, 2)


def estimate(dna):
    m = dna["metal"]
    ppg = PRICING["metal_price_per_g"][m]
    wt = metal_weight_g(dna)
    metal = wt * ppg

    c = dna["centre"]
    stones = c["carat"] * PRICING["stone_price_per_carat_labgrown"][c["cut"]]
    for a in dna.get("accents", []):
        per = PRICING["stone_price_per_carat_labgrown"].get(a["cut"], 500)
        stones += a["carat"] * a["count"] * per
    # composition-implied accents when not spelled out
    comp = dna["composition"]
    if not dna.get("accents"):
        if comp == "toi_et_moi":
            stones += 0.9 * PRICING["stone_price_per_carat_labgrown"]["pear"]
        elif comp == "three_stone":
            stones += 2 * 0.3 * PRICING["stone_price_per_carat_labgrown"]["round"]
        elif comp == "hidden_halo":
            stones += 0.18 * 430

    labour = (PRICING["labour_base"]
              + PRICING["labour_setting"].get(c["setting"], 20)
              + PRICING["labour_composition_add"].get(comp, 0))
    make = metal + stones + labour
    retail = round(make * PRICING["retail_multiplier"] / 10) * 10
    return {
        "metal": round(metal), "stones": round(stones), "labour": round(labour),
        "make": round(make), "retail": int(retail), "metal_weight_g": wt,
    }


def check(dna):
    """Return (list_of_issues). Empty list == passes."""
    issues = []
    c = dna["centre"]

    # ratio vs cut range (drift guard)
    r = RATIOS.get(c["cut"])
    if r and not (r["min"] - 0.05 <= c["lw"] <= r["max"] + 0.05):
        issues.append(("warn", "cut/ratio",
                       f'{c["cut"]} L:W {c["lw"]} outside typical {r["min"]}-{r["max"]}'))

    # setting rules
    if c["setting"] == "prong":
        dia = c.get("prong_dia_mm", 1.2)
        if dia < MIN_PRONG_DIA_MM:
            issues.append(("crit", "prong", f'prong Ø{dia}mm < {MIN_PRONG_DIA_MM}mm min'))
        if c.get("prongs") not in (3, 4, 6):
            issues.append(("crit", "prong", f'prong count {c.get("prongs")} not in (3,4,6)'))
    else:
        wall = c.get("bezel_wall_mm", 0.8)
        if wall < MIN_WALL_MM:
            issues.append(("crit", "bezel", f'bezel wall {wall}mm < {MIN_WALL_MM}mm cast min'))

    if dna["band"]["width_mm"] < MIN_BAND_WIDTH_MM:
        issues.append(("crit", "band", f'band {dna["band"]["width_mm"]}mm < {MIN_BAND_WIDTH_MM}mm min'))

    return issues


def report(path):
    with open(path) as f:
        dna = json.load(f)
    L, W = stone_mm(dna["centre"]["cut"], dna["centre"]["carat"], dna["centre"]["lw"])
    est = estimate(dna)
    issues = check(dna)

    name = dna.get("name") or dna.get("sku") or os.path.basename(path)
    print(f"\n  {name}")
    print(f"  {dna['centre']['cut']} {dna['centre']['carat']}ct  {L}x{W}mm  "
          f"L:W {dna['centre']['lw']}  |  {dna['composition']}  |  {dna['metal']}")
    print("  " + "-" * 46)
    print(f"  metal ({est['metal_weight_g']} g)        ${est['metal']:>7,}")
    print(f"  stones                    ${est['stones']:>7,}")
    print(f"  labour/cast/set           ${est['labour']:>7,}")
    print(f"  make cost                 ${est['make']:>7,}")
    print(f"  SUGGESTED RETAIL          ${est['retail']:>7,}")
    print("  " + "-" * 46)
    if not issues:
        print("  manufacturability: PASS  ✓")
    else:
        for sev, where, msg in issues:
            mark = "✗" if sev == "crit" else "!"
            print(f"  [{sev.upper():4}] {mark} {where}: {msg}")
    print()
    return 1 if any(s == "crit" for s, _, _ in issues) else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(report(sys.argv[1]))
