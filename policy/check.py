#!/usr/bin/env python3
"""Load-time policy conflict detection + traceability. Runs before every catalog;
run_catalog refuses to start on any STOP. Registry (policy/registry.json) is the
single source of truth for rules; this validates its integrity and its links to
gates and goldens.

Checks:
  1. Two ACTIVE rules on the same key with different statements -> STOP (print both).
  2. A rule with no enforced_by -> WARN "unenforced, advisory only".
  3. A gate (config/gates.json) with no rule -> WARN "orphan gate".
  4. A failure_case (memory/failures.json) with no rule -> WARN "failure with no policy".
  5. Any prose doc restating a registry rule's literal_banned_in_prose -> STOP "second source of truth".

Traceability (both directions): every active rule should reach a gate, and every
gate should reach >=1 golden case. A rule reaching neither is reported as a wish.

Exit 0 = ok/warn only; 2 = STOP (a hard conflict). Usage: python policy/check.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "policy" / "registry.json"


def _load(p, default=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return default if default is not None else {}


# non-gate enforcers: hard code-enforcers block like a blocking gate; visual = observed
_HARD_NONGATE = {"run_catalog", "refs_preflight", "slot_manifest", "preflight", "regression_suite", "spec_source_read"}
_OBSERVED_NONGATE = {"visual_checklist"}


def classify(rule, gates):
    """ENFORCED = rule -> blocking gate (or hard code-enforcer).
    OBSERVED = rule -> non-blocking gate (G2-G9/G10) or a mandatory visual checklist (L4-L8).
    ADVISORY = rule -> no gate/enforcer."""
    eb = rule.get("enforced_by", [])
    if any(g in gates and gates[g].get("blocking") for g in eb) or any(g in _HARD_NONGATE for g in eb):
        return "enforced"
    if any(g in gates and not gates[g].get("blocking") for g in eb) or any(g in _OBSERVED_NONGATE for g in eb):
        return "observed"
    return "advisory"


def counts():
    reg = _load(ROOT / "policy" / "registry.json").get("rules", [])
    gates = _load(ROOT / "config" / "gates.json", {}).get("gates", {})
    active = [r for r in reg if r.get("status") == "active"]
    c = {"enforced": 0, "observed": 0, "advisory": 0}
    for r in active:
        c[classify(r, gates)] += 1
    return c["enforced"], c["observed"], c["advisory"]


def main():
    reg = _load(REG).get("rules", [])
    active = [r for r in reg if r.get("status") == "active"]
    stops, warns = [], []

    # 1. same-key active conflicts
    bykey = {}
    for r in active:
        bykey.setdefault(r.get("key"), []).append(r)
    for key, rs in bykey.items():
        stmts = {r["statement"] for r in rs}
        if len(stmts) > 1:
            stops.append(f"CONFLICT on key '{key}': " + " || ".join(f"{r['id']}=\"{r['statement']}\"" for r in rs))

    # 2. unenforced active rules
    for r in active:
        if not r.get("enforced_by"):
            warns.append(f"unenforced (advisory only): {r['id']}")

    # 3. orphan gates
    gates = set(_load(ROOT / "config" / "gates.json", {}).get("gates", {}).keys())
    ruled_gates = {g for r in active for g in r.get("enforced_by", [])}
    for g in sorted(gates - ruled_gates):
        warns.append(f"orphan gate (no rule): {g}")

    # 4. failures with no policy
    fails = {f["id"] for f in _load(ROOT / "memory" / "failures.json", {}).get("failures", [])}
    ruled_fails = {fc for r in active for fc in r.get("failure_cases", [])}
    for f in sorted(fails - ruled_fails):
        warns.append(f"failure_case with no rule: {f}")

    # 5. prose doc restating a banned literal (skip the GENERATED projection and archive)
    docs = [d for d in (ROOT / "docs").glob("*.md") if d.name != "POLICY.md"]
    for r in active:
        for lit in r.get("literal_banned_in_prose", []):
            for d in docs:
                if lit.lower() in d.read_text(encoding="utf-8", errors="ignore").lower():
                    stops.append(f"SECOND SOURCE OF TRUTH: '{lit}' (rule {r['id']}) appears in {d.name} -- docs must point to the ID, not restate the value")

    # traceability
    golden_gates = set()
    cases = _load(ROOT / "tests" / "golden" / "cases.json", {}).get("cases", [])
    for c in cases:
        golden_gates.add(str(c.get("gate", "")).split("_")[0])
    for d in (ROOT / "tests" / "golden").glob("pass_*"):
        cj = d / "case.json"
        if cj.exists():
            for k in _load(cj, {}).get("expect", {}):
                golden_gates.add(k.split("_")[0])
    wishes = []
    for r in active:
        eb = r.get("enforced_by", [])
        reaches_gate = any(g in gates for g in eb)
        reaches_golden = any(g.split("_")[0] in golden_gates for g in eb)
        if not reaches_gate and not reaches_golden and not eb:
            wishes.append(r["id"])

    for s in stops:
        print("STOP  " + s)
    for w in warns:
        print("warn  " + w)
    if wishes:
        print(f"wishes (rule reaches no gate+golden): {wishes}")
    e, o, a = counts()
    print(f"\n{len(active)} active rules: {e} enforced, {o} observed, {a} advisory | {len(stops)} STOP, {len(warns)} warn")
    sys.exit(2 if stops else 0)


if __name__ == "__main__":
    main()
