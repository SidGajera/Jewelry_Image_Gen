#!/usr/bin/env python3
"""DELIVERY PIPELINE SWITCH — turn the whole generation pipeline on or off in one command.

    python scripts/pipeline.py --status              # what is live right now
    python scripts/pipeline.py --list                # every profile
    python scripts/pipeline.py --on                  # Google Flow - Nano Banana 2
    python scripts/pipeline.py --off                 # back to Higgsfield
    python scripts/pipeline.py --use gflow-nb2       # same as --on, by name
    python scripts/pipeline.py --check               # verify the repo agrees with the switch

ONE value decides which pipeline produces delivered pixels: `active` in
config/delivery_profiles.json. This script is the only thing that writes it, and it
rewrites every derived flag in the same pass so the repo can never sit half-switched:

    config/active_engine.json     which engine is selected
    config/engines.json           default engine, catalog_approved, blocked_for/allowed_for
    config/pipeline_versions.json active pipeline version, selectable_as_active
    policy/registry.json          which rule owns `generation.engine` and `format.aspect`

Do NOT hand-edit those four for a pipeline change — they are derived. Edit the profile
in config/delivery_profiles.json and re-run the switch.

Registry mechanics: each profile names the rule that owns each policy key. Switching
promotes that rule to `active` and drops the other to `inactive`. A rule may only claim
`supersedes` on a rule that is not itself active (policy/check.py rule 1b), so an
inactive rule's claims are parked in `_supersedes_when_active` and restored when it is
promoted. Both states leave policy/check.py at 0 STOP, which --check asserts.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "config" / "delivery_profiles.json"
ENGINES = ROOT / "config" / "engines.json"
VERSIONS = ROOT / "config" / "pipeline_versions.json"
ACTIVE_ENGINE = ROOT / "config" / "active_engine.json"
REGISTRY = ROOT / "policy" / "registry.json"

# Purposes that describe a delivered image. They follow the switch — that is the point.
DELIVERY_PURPOSES = ["catalog_stills", "macro", "lifestyle_stills", "any_delivered_image"]


class SwitchError(RuntimeError):
    """The switch refuses rather than leaving the repo half-changed."""


def _read(p):
    return json.loads(p.read_text(encoding="utf-8"))


def _write(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def profiles():
    return _read(PROFILES)


def active_id():
    return profiles()["active"]


def active_profile():
    cfg = profiles()
    return cfg["profiles"][cfg["active"]]


def get_format():
    """The delivered format of the live pipeline. Read by G1_FORMAT — never hard-code
    2048 (or 1536) anywhere else."""
    return active_profile()["format"]


def get_model():
    """The model string of the live pipeline (nano_banana_2 via Higgsfield, NARWHAL via Flow)."""
    prof = active_profile()
    if prof["model_source"] == "config/model.json":
        return _read(ROOT / "config" / "model.json")["model"]
    return prof["model"]


# ---------------------------------------------------------------- derived writers

def _apply_engines(prof, other):
    cfg = _read(ENGINES)
    live, off = prof["engine"], other["engine"]
    cfg["default"] = live
    for eid, rec in cfg["engines"].items():
        delivers = eid == live
        rec["catalog_approved"] = delivers
        allowed = [a for a in rec.get("allowed_for", []) if a not in DELIVERY_PURPOSES]
        blocked = [b for b in rec.get("blocked_for", []) if b not in DELIVERY_PURPOSES]
        if delivers:
            allowed = DELIVERY_PURPOSES + [a for a in allowed if a not in DELIVERY_PURPOSES]
            rec["role"] = "production_default"
        else:
            blocked = DELIVERY_PURPOSES + [b for b in blocked if b not in DELIVERY_PURPOSES]
            rec["role"] = "secondary_optin"
            rec["catalog_block_reason"] = (
                f"Delivery runs on '{live}' while config/delivery_profiles.json active = "
                f"'{prof['pipeline']}'. Switch with: python scripts/pipeline.py --use <profile>.")
        rec["allowed_for"], rec["blocked_for"] = allowed, blocked
    cfg["selection_rules"]["catalog_stills"] = (
        f"'{live}' ONLY (delivery profile '{prof['pipeline']}'). Any other engine id is a hard STOP. "
        f"Change it with scripts/pipeline.py, never by editing this file.")
    cfg["_switched_by"] = "scripts/pipeline.py — derived, do not hand-edit catalog_approved/blocked_for"
    _write(ENGINES, cfg)


def _apply_versions(prof, other):
    cfg = _read(VERSIONS)
    cfg["active"] = prof["pipeline"]
    for name, rec in cfg["versions"].items():
        if name == prof["pipeline"]:
            rec["selectable_as_active"] = True
            rec["status"] = "production"
            rec.pop("why_not_production", None)
        elif name == other["pipeline"]:
            rec["selectable_as_active"] = True
            rec["status"] = "available"
    _write(VERSIONS, cfg)


def _apply_active_engine(prof):
    _write(ACTIVE_ENGINE, {
        "active": prof["engine"],
        "_note": "DERIVED from config/delivery_profiles.json by scripts/pipeline.py. "
                 "Change the pipeline with: python scripts/pipeline.py --use <profile>.",
    })


def _apply_registry(prof, other):
    """Promote the winning rule per policy key, demote the loser, and keep every
    supersedes-claim legal in both directions (policy/check.py rule 1b)."""
    reg = _read(REGISTRY)
    byid = {r["id"]: r for r in reg["rules"]}
    for key, winner in prof["registry_owner"].items():
        loser = other["registry_owner"][key]
        for rid in (winner, loser):
            if rid not in byid:
                raise SwitchError(f"policy/registry.json has no rule '{rid}' for key '{key}'")
        byid[winner]["status"] = "active"
        byid[winner].pop("superseded_by", None)
        byid[loser]["status"] = "inactive"
        byid[loser]["superseded_by"] = winner

    # A rule may claim `supersedes` on an active rule ONLY while it is itself active.
    # Park the illegal claims, restore them on promotion.
    for r in reg["rules"]:
        parked = list(r.get("_supersedes_when_active") or [])
        sup = list(r.get("supersedes") or [])
        if r.get("status") == "active":
            sup += [s for s in parked if s not in sup]
            parked = []
        else:
            keep = []
            for s in sup:
                if byid.get(s, {}).get("status") == "active":
                    if s not in parked:
                        parked.append(s)
                else:
                    keep.append(s)
            sup = keep
        r["supersedes"] = sup
        if parked:
            r["_supersedes_when_active"] = parked
        else:
            r.pop("_supersedes_when_active", None)
    _write(REGISTRY, reg)


def use(pid):
    """Switch the delivery pipeline. Writes every derived file, then verifies."""
    cfg = profiles()
    if pid not in cfg["profiles"]:
        raise SwitchError(
            f"unknown profile '{pid}'. Declared: {', '.join(sorted(cfg['profiles']))}.")
    if len(cfg["profiles"]) != 2:
        raise SwitchError("the switch assumes exactly two profiles; add explicit pairing logic first")
    prof = cfg["profiles"][pid]
    other = cfg["profiles"][next(k for k in cfg["profiles"] if k != pid)]

    cfg["active"] = pid
    _write(PROFILES, cfg)
    _apply_active_engine(prof)
    _apply_engines(prof, other)
    _apply_versions(prof, other)
    _apply_registry(prof, other)
    return prof


def check():
    """Every derived file must agree with the switch. Returns a list of problems."""
    cfg = profiles()
    pid = cfg["active"]
    prof = cfg["profiles"][pid]
    bad = []

    eng = _read(ENGINES)
    if eng["default"] != prof["engine"]:
        bad.append(f"engines.json default='{eng['default']}' but profile '{pid}' wants '{prof['engine']}'")
    approved = sorted(k for k, v in eng["engines"].items() if v["catalog_approved"])
    if approved != [prof["engine"]]:
        bad.append(f"catalog-approved engines {approved}, expected ['{prof['engine']}']")
    for eid, rec in eng["engines"].items():
        delivers = eid == prof["engine"]
        blocked = set(rec.get("blocked_for", [])) & set(DELIVERY_PURPOSES)
        if delivers and blocked:
            bad.append(f"live engine '{eid}' still blocks {sorted(blocked)}")
        if not delivers and blocked != set(DELIVERY_PURPOSES):
            bad.append(f"off engine '{eid}' does not block every delivery purpose")

    ver = _read(VERSIONS)
    if ver["active"] != prof["pipeline"]:
        bad.append(f"pipeline_versions.json active='{ver['active']}', expected '{prof['pipeline']}'")

    if _read(ACTIVE_ENGINE).get("active") != prof["engine"]:
        bad.append("config/active_engine.json disagrees with the profile")

    reg = _read(REGISTRY)
    byid = {r["id"]: r for r in reg["rules"]}
    for key, owner in prof["registry_owner"].items():
        if byid.get(owner, {}).get("status") != "active":
            bad.append(f"registry rule '{owner}' should own '{key}' but is not active")
        live = [r["id"] for r in reg["rules"] if r.get("key") == key and r.get("status") == "active"]
        if live != [owner]:
            bad.append(f"key '{key}' active owners {live}, expected ['{owner}']")

    fmt = prof["format"]
    if fmt["width"] != fmt["height"] or fmt["aspect_ratio"] != "1:1":
        bad.append(f"profile '{pid}' delivers {fmt['width']}x{fmt['height']} — catalog format must stay 1:1")
    return bad


def status_lines():
    cfg = profiles()
    pid = cfg["active"]
    prof = cfg["profiles"][pid]
    fmt = prof["format"]
    other = next(k for k in cfg["profiles"] if k != pid)
    out = [
        f"delivery pipeline : {pid}  ({prof['display']})",
        f"engine            : {prof['engine']}  via {prof['route']}",
        f"model             : {get_model()}",
        f"delivered format  : {fmt['width']}x{fmt['height']} {fmt['aspect_ratio']}"
        f"{' native' if fmt['native'] else ' (upscale+crop)'}",
        f"credits/image     : {prof['credits_per_image']}",
        f"switch off with   : python scripts/pipeline.py --use {other}",
    ]
    if prof.get("requires_mcp"):
        out.append(f"requires MCP      : {prof['requires_mcp']}  ({prof['install']})")
    return out


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        if "--use" in argv or "--on" in argv or "--off" in argv:
            if "--use" in argv:
                target = argv[argv.index("--use") + 1]
            else:
                cfg = profiles()
                nondefault = [k for k in cfg["profiles"] if k != "higgsfield"]
                target = nondefault[0] if "--on" in argv else "higgsfield"
            prof = use(target)
            for line in status_lines():
                print(line)
            bad = check()
            for p in bad:
                print("SWITCH FAIL:", p)
            sys.exit(1 if bad else 0)

        if "--status" in argv:
            print("\n".join(status_lines()))
            sys.exit(0)

        if "--list" in argv:
            cfg = profiles()
            for pid, prof in cfg["profiles"].items():
                mark = "*" if pid == cfg["active"] else " "
                f = prof["format"]
                print(f"{mark} {pid:<12} {prof['display']:<30} "
                      f"{f['width']}x{f['height']}  engine={prof['engine']}")
            print("\n* = live. Switch with: python scripts/pipeline.py --use <id>")
            sys.exit(0)

        if "--check" in argv:
            bad = check()
            for p in bad:
                print("SWITCH FAIL:", p)
            print("pipeline switch OK" if not bad else f"{len(bad)} problem(s)")
            sys.exit(1 if bad else 0)
    except SwitchError as exc:
        sys.exit(f"STOP: {exc}")

    print(__doc__)
