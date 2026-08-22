#!/usr/bin/env python3
"""GENERATION LAW GATE — the hardcoding that makes policy/GENERATION_LAW.md permanent.

    python policy/law_gate.py --check          # STOP=exit 2 if the law is not intact
    python policy/law_gate.py --show           # print the law's clause -> owner -> gate map
    python policy/law_gate.py --restamp        # re-record the law checksum after an AUTHORISED edit
    python policy/law_gate.py --coverage SKU   # LAW-03/04 source-coverage decision for one SKU

run_catalog.py calls check() FIRST, before the policy gate, before the source gate, before
anything. Any failure STOPs the catalog. There is no flag, no env var and no argument that
skips it — that is the point.

What it verifies:
  1. INTEGRITY   — GENERATION_LAW.md matches the SHA-256 recorded in generation_law.json.
                   An unrecorded edit is a STOP, so the law cannot be quietly weakened.
  2. OWNERSHIP   — every law clause resolves to EXACTLY ONE ACTIVE rule in policy/registry.json.
                   Zero owners = an unenforceable clause. Two owners = the duplicate-policy
                   failure the user forbade. Both STOP.
  3. WIRING      — every owner rule names at least one gate/enforcer, and every gate it names
                   exists in config/gates.json or is a known code enforcer.
  4. UNIQUENESS  — no two ACTIVE rules share a topic key (one policy, one rule, one instruction).
  5. SUPREMACY   — the law's own rule and the design rule sit at the top precedence, so nothing
                   in the registry can outrank the jewellery design.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAW_MD = ROOT / "policy" / "GENERATION_LAW.md"
LAW_JSON = ROOT / "policy" / "generation_law.json"
REGISTRY = ROOT / "policy" / "registry.json"
GATES = ROOT / "config" / "gates.json"

# Enforcers that are code, not entries in config/gates.json.
CODE_ENFORCERS = {
    "run_catalog", "run_catalog.budget_check", "refs_preflight", "slot_manifest", "preflight",
    "regression_suite", "spec_source_read", "law_gate", "validate_source", "ENGINE_LOCK_CHECK",
    "visual_checklist",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _law():
    return json.loads(LAW_JSON.read_text(encoding="utf-8"))


def _rules():
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["rules"]


def _gates():
    return json.loads(GATES.read_text(encoding="utf-8")).get("gates", {})


def clause_map():
    """clause id -> {owner rule id, key, gates} resolved live from the registry."""
    out = {}
    active = [r for r in _rules() if r.get("status") == "active"]
    for clause in _law()["clauses"]:
        cid = clause["id"]
        owners = [r for r in active if cid in (r.get("law_clause") or [])]
        out[cid] = {
            "title": clause["title"],
            "declared_owner": clause["owner_rule"],
            "resolved_owners": [r["id"] for r in owners],
            "key": owners[0].get("key") if len(owners) == 1 else None,
            "gates": sorted({g for r in owners for g in (r.get("enforced_by") or [])}),
        }
    return out


def check():
    """Return a list of STOP messages. Empty list = the law is intact."""
    stops = []

    # 1. INTEGRITY
    law = _law()
    actual = sha256(LAW_MD)
    if law.get("law_sha256") != actual:
        stops.append(
            f"LAW TAMPERED: {LAW_MD.name} sha256 {actual[:16]}... does not match the recorded "
            f"{str(law.get('law_sha256'))[:16]}.... An authorised change is applied to the OWNER RULE "
            f"and then re-stamped with: python policy/law_gate.py --restamp")

    rules = _rules()
    active = [r for r in rules if r.get("status") == "active"]
    byid = {r["id"]: r for r in rules}
    gates = _gates()

    # 2. OWNERSHIP + 3. WIRING
    for cid, info in clause_map().items():
        owners = info["resolved_owners"]
        if not owners:
            stops.append(f"{cid} ({info['title']}) has NO active owner rule — the clause is unenforceable.")
            continue
        if len(owners) > 1:
            stops.append(
                f"{cid} ({info['title']}) has {len(owners)} active owners {owners}. "
                f"One policy, one rule, one instruction — supersede, never duplicate.")
            continue
        declared = info["declared_owner"]
        if declared != owners[0]:
            stops.append(
                f"{cid} declares owner '{declared}' but the registry's active owner is '{owners[0]}'.")
        if not info["gates"]:
            stops.append(f"{cid} owner '{owners[0]}' names no gate or enforcer — nothing enforces it.")
        for g in info["gates"]:
            if g not in gates and g not in CODE_ENFORCERS:
                stops.append(f"{cid} owner '{owners[0]}' names gate '{g}', which does not exist.")

    # 4. UNIQUENESS — one active rule per topic key
    bykey = {}
    for r in active:
        bykey.setdefault(r.get("key"), []).append(r["id"])
    for key, ids in sorted(bykey.items()):
        if len(ids) > 1:
            stops.append(f"DUPLICATE POLICY on topic '{key}': {ids}. Exactly one active rule per topic.")

    # 5. SUPREMACY — nothing may outrank the jewellery design or the law itself
    top = law["supremacy"]["top_precedence_rules"]
    ranks = {r["id"]: r.get("precedence", 0) for r in active}
    highest = max(ranks.values()) if ranks else 0
    for rid in top:
        if rid not in ranks:
            stops.append(f"SUPREMACY: '{rid}' must be an active rule and is not.")
        elif ranks[rid] < highest:
            stops.append(
                f"SUPREMACY: '{rid}' sits at precedence {ranks[rid]} while '"
                f"{max(ranks, key=ranks.get)}' holds {highest}. Nothing may outrank the design or the law.")
    return stops


# ---------------------------------------------------------------- LAW-03 / LAW-04

def coverage_decision(sku):
    """LAW-03/LAW-04. Returns (blocking_stops, warnings).

    LAW-03: a missing source read is a STOP — no source, no pixels.
    LAW-04: any slot whose `reveals` (config/angle_matrix.json) are not established by a
    SUPPLIED source view (specs/<SKU>_views.json x config/view_coverage.json) produces a
    NAMED warning demanding SKIP or CONTINUE. Never a silent generation."""
    stops, warns = [], []

    src = ROOT / "workspace" / "golden" / sku / "source"
    if not src.exists() or not any(src.iterdir()):
        stops.append(
            f"LAW-03: no source read for {sku} — {src} is missing or empty. "
            f"Source reading is compulsory; generation is not possible without it.")
        return stops, warns

    spec_path = ROOT / "specs" / f"{sku}.json"
    if not spec_path.exists():
        stops.append(f"LAW-03: no spec at {spec_path} — the source has not been read into a spec yet.")
        return stops, warns
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    views_path = ROOT / "specs" / f"{sku}_views.json"
    if not views_path.exists():
        warns.append(
            f"SOURCE NOT IDENTIFIED FOR ANY ANGLE: {sku} has no specs/{sku}_views.json, so no slot's "
            f"source view is established — SKIP or CONTINUE? "
            f"[SKIP drops the catalog; CONTINUE generates every slot stamped SOURCE_UNVERIFIED]")
        return stops, warns
    views = json.loads(views_path.read_text(encoding="utf-8")).get("views") or []

    coverage = json.loads((ROOT / "config" / "view_coverage.json").read_text(encoding="utf-8"))
    establishes = coverage.get("establishes", {})
    established = set()
    for v in views:
        established |= set(establishes.get(v.get("type"), []))

    matrix = json.loads((ROOT / "config" / "angle_matrix.json").read_text(encoding="utf-8"))
    category = spec.get("category", "ring")
    slots = (matrix.get("categories", {}).get(category) or {}).get("slots") or []
    if not slots:
        warns.append(f"LAW-04: config/angle_matrix.json declares no slots for category '{category}'.")
        return stops, warns

    for sl in slots:
        missing = sorted(set(sl.get("reveals") or []) - established)
        if missing:
            warns.append(
                f"SOURCE NOT IDENTIFIED FOR THIS ANGLE: {sl['slot']} {sl.get('name', '')} "
                f"({sl.get('azimuth')}/{sl.get('elevation')}) — no supplied source view establishes "
                f"{missing} — SKIP or CONTINUE? "
                f"[SKIP drops the slot; CONTINUE generates it stamped SOURCE_UNVERIFIED]")
    return stops, warns


def restamp():
    law = _law()
    law["law_sha256"] = sha256(LAW_MD)
    LAW_JSON.write_text(json.dumps(law, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return law["law_sha256"]


if __name__ == "__main__":
    argv = sys.argv[1:]

    if "--restamp" in argv:
        print(f"law checksum restamped: {restamp()}")
        sys.exit(0)

    if "--coverage" in argv:
        sku = argv[argv.index("--coverage") + 1]
        stops, warns = coverage_decision(sku)
        for w in warns:
            print("WARN ", w)
        for s in stops:
            print("STOP ", s)
        sys.exit(2 if stops else 0)

    if "--show" in argv:
        for cid, info in clause_map().items():
            owner = info["resolved_owners"][0] if len(info["resolved_owners"]) == 1 else info["resolved_owners"]
            print(f"{cid}  {info['title']}")
            print(f"      owner: {owner}   key: {info['key']}")
            print(f"      gates: {', '.join(info['gates']) or '(none)'}")
        sys.exit(0)

    if "--check" in argv:
        bad = check()
        for s in bad:
            print("LAW STOP:", s)
        print("generation law OK" if not bad else f"{len(bad)} law violation(s)")
        sys.exit(2 if bad else 0)

    print(__doc__)
