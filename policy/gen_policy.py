#!/usr/bin/env python3
"""Generate docs/POLICY.md FROM policy/registry.json. The doc is read-only and
must never be hand-edited — edit the registry, then regenerate. This is the fix
for prose drift: the human-readable policy is a projection of the single source
of truth, not a second copy of it.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
reg = json.loads((ROOT / "policy" / "registry.json").read_text(encoding="utf-8"))
rules = reg["rules"]
active = [r for r in rules if r["status"] == "active"]
superseded = [r for r in rules if r["status"] == "superseded"]
enforced = [r for r in active if r.get("enforced_by")]
advisory = [r for r in active if not r.get("enforced_by")]

lines = [
    "# POLICY — GENERATED from policy/registry.json (DO NOT EDIT)",
    "",
    "Read-only projection of the rule registry. Edit `policy/registry.json`, then run "
    "`python policy/gen_policy.py`. `policy/check.py` runs before every catalog and STOPs on conflicts.",
    "",
    f"**{len(active)} rules active** · {len(enforced)} enforced by gates · {len(advisory)} advisory "
    f"(empty enforced_by) · {len(superseded)} superseded (kept for provenance).",
    "",
    "Precedence: 100 source fidelity · 90 platform compliance · 80 physical plausibility · "
    "50 user preference · 10 doc defaults. Higher wins; the loser is superseded, never deleted.",
    "",
    "## Active rules",
    "",
    "| ID | Prec | Statement | Enforced by | Origin |",
    "|---|---|---|---|---|",
]
for r in sorted(active, key=lambda x: (-x["precedence"], x["id"])):
    eb = ", ".join(r.get("enforced_by", [])) or "_advisory_"
    lines.append(f"| `{r['id']}` | {r['precedence']} | {r['statement']} | {eb} | {r['origin']} |")

lines += ["", "## Superseded rules (provenance — never deleted)", "",
          "| ID | Statement | Superseded by |", "|---|---|---|"]
for r in sorted(superseded, key=lambda x: x["id"]):
    lines.append(f"| `{r['id']}` | {r['statement']} | `{r.get('superseded_by','')}` |")

lines += ["", "## Advisory rules (empty enforced_by — not machine-verified)", ""]
lines += ["- `" + r["id"] + "` — " + r["statement"] for r in advisory] or ["- (none)"]

(ROOT / "docs" / "POLICY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote docs/POLICY.md — {len(active)} active, {len(enforced)} enforced, {len(advisory)} advisory")
