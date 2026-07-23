#!/usr/bin/env python3
"""
trend_engine.py  —  layer 1: aggregate -> tag -> rank -> PROPOSE design-DNA

SCAFFOLD. The scraping/CV/NLP adapters are stubs (marked TODO). What IS real:
the ranking + the propose() step that emits ready-to-build design-DNA parameter
sets from the current "hot" attribute weights. This is the front of the pipeline
that feeds the parametric generator.

Usage:
    python trend_engine.py            # prints a mini trend report + 3 proposed designs
"""
import json, os, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
TAX = json.load(open(os.path.join(HERE, "taxonomy.json")))
# hot_2026 carries a "note" string alongside numeric weights — keep only the weights.
HOT = {k: v for k, v in TAX["hot_2026"].items() if isinstance(v, (int, float))}

# ---------------------------------------------------------------------------
# 1. AGGREGATE (stub) — where real data comes from
# ---------------------------------------------------------------------------
SOURCES = [
    # TODO: implement adapters -> list[dict(attributes, engagement, sold_rank, ts)]
    "pinterest_search", "instagram_hashtags", "etsy_new_arrivals",
    "retailer_new_in (bluenile / brilliantearth / mejuri / vrai)",
    "google_trends", "runway_bridal_shows",
]

def aggregate():
    """TODO: fetch listings/images from SOURCES. For now, return [] and rely on HOT seeds."""
    return []

# ---------------------------------------------------------------------------
# 2. TAG (stub) — CV + NLP normalise each item to taxonomy attributes
# ---------------------------------------------------------------------------
def tag(item):
    """TODO: vision model -> cut/setting/band...; NLP on caption/hashtags/reviews."""
    return item.get("attributes", {})

# ---------------------------------------------------------------------------
# 3. RANK — momentum by attribute (real: count + engagement + sold-rank delta)
# ---------------------------------------------------------------------------
def rank(items):
    if not items:
        return dict(sorted(HOT.items(), key=lambda kv: -kv[1]))
    counts = {}
    for it in items:
        for v in tag(it).values():
            for x in (v if isinstance(v, list) else [v]):
                counts[x] = counts.get(x, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))

# ---------------------------------------------------------------------------
# 4. PROPOSE — turn hot attributes into valid design-DNA (the payoff)
# ---------------------------------------------------------------------------
RATIOS = json.load(open(os.path.join(HERE, "..", "schema", "cut-ratios.json")))["cuts"]

def propose(n=3, existing_catalog=None):
    """Compose the top hot attributes into buildable design-DNA, skipping combos the
    catalog already covers. Deterministic here; the real version samples + scores."""
    existing = set(existing_catalog or [])
    hot_cuts = [c for c in ["hexagon", "oval", "marquise", "pear", "emerald"] if HOT.get(c, 0) >= 0.7]
    hot_comp = [k for k in ["toi_et_moi", "hidden_halo", "three_stone"] if HOT.get(k, 0) >= 0.7]
    settings = ["bezel", "prong"]
    out, seen = [], set()
    for cut, comp, setg in itertools.product(hot_cuts, hot_comp + ["solitaire"], settings):
        key = f"{cut}-{comp}-{setg}"
        if key in existing or key in seen:
            continue
        seen.add(key)
        r = RATIOS[cut]["ideal"]
        dna = {
            "name": f"proposed {cut} {comp.replace('_',' ')}",
            "metal": "18k_yellow_gold",
            "centre": {"cut": cut, "carat": 1.5, "lw": r, "lab_grown": True,
                       "orientation": "east_west" if cut == "oval" else "north_south",
                       "setting": setg, "prongs": None if setg == "bezel" else 6},
            "composition": comp,
            "band": {"profile": "knife_edge", "width_mm": 1.8},
            "provenance": {"source": "trend_engine",
                           "trend_tags": [cut, comp, setg,
                                          "east_west" if cut == "oval" else ""]},
        }
        out.append(dna)
        if len(out) >= n:
            break
    return out


def main():
    items = aggregate()
    ranking = rank(items)
    print("\n  TREND REPORT (momentum by attribute)")
    print("  " + "-" * 40)
    for k, v in list(ranking.items())[:8]:
        bar = "█" * int(round(v * 18))
        print(f"  {k:14} {bar} {v:.2f}")
    # catalog whitespace: single-stone round/hexagon solitaires already done
    existing = ["round-solitaire-prong", "hexagon-solitaire-prong", "hexagon-hidden_halo-prong"]
    print("\n  PROPOSED NEW DESIGNS (whitespace vs current catalog)")
    print("  " + "-" * 40)
    for d in propose(3, existing):
        c = d["centre"]
        print(f"  • {d['name']:34} [{c['cut']} {c['carat']}ct / {d['composition']} / {c['setting']}]")
    print("\n  -> feed these into cad/manufacturability.py and the configurator.\n")


if __name__ == "__main__":
    main()
