#!/usr/bin/env python3
"""Engine resolver — the ONE place that decides which generation engine a call
may use. Engine 1 (higgsfield) is the production default and the only
catalog-approved stills engine; engine 2 (openflow) is opt-in, never automatic.

Nothing here changes how engine 1 is called: `resolve()` with no argument returns
the same frozen Higgsfield constraints the pipeline has always used. The module
exists so a second engine can be named explicitly and refused where it would
degrade delivered output.

Switching engines is one command:
  python scripts/engine.py --use openflow           # exploration/video work
  python scripts/engine.py --use higgsfield         # back to engine 1
  python scripts/engine.py --show                   # what is active right now

The active engine applies to exploration and video ONLY. Catalog stills always
resolve to engine 1 no matter what is active - switching cannot degrade a
delivered image, which is the whole point of keeping the switch cheap.

Usage:
  python scripts/engine.py --list
  python scripts/engine.py --check                 # invariants (used by tests)
  python scripts/engine.py --resolve openflow --purpose video
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINES = ROOT / "config" / "engines.json"
MODEL_CFG = ROOT / "config" / "model.json"
ACTIVE = ROOT / "config" / "active_engine.json"

# Purposes that may NEVER follow the active-engine switch. A delivered still is
# always engine 1; the switch exists for work that never ships.
LOCKED_PURPOSES = {"catalog_stills", "macro", "lifestyle_stills", "any_delivered_image"}


class EngineViolation(RuntimeError):
    """Raised when a call would use an engine that is not allowed for its purpose."""


def _cfg():
    return json.loads(ENGINES.read_text(encoding="utf-8"))


def default_engine():
    return _cfg()["default"]


def active_engine():
    """The engine currently selected for switchable (non-delivery) work.
    Falls back to engine 1 when nothing was ever selected."""
    if ACTIVE.exists():
        try:
            eid = json.loads(ACTIVE.read_text(encoding="utf-8")).get("active")
            if eid in _cfg()["engines"]:
                return eid
        except (ValueError, OSError):
            pass
    return default_engine()


def use(engine):
    """Select the engine for switchable work. Refuses an unknown id so a typo
    cannot silently leave the previous engine selected."""
    cfg = _cfg()
    if engine not in cfg["engines"]:
        raise EngineViolation(
            f"unknown engine '{engine}'. Declared: {', '.join(sorted(cfg['engines']))}.")
    rec = cfg["engines"][engine]
    ACTIVE.write_text(json.dumps({
        "active": engine,
        "_note": "Active engine for exploration/video ONLY. Catalog stills always use "
                 "config/engines.json 'default' (higgsfield) regardless of this file. "
                 "Set with: python scripts/engine.py --use <id>",
    }, indent=2) + "\n", encoding="utf-8")
    return engine, rec["status"]


def list_engines():
    return {k: {"rank": v["rank"], "role": v["role"], "status": v["status"],
                "catalog_approved": v["catalog_approved"]}
            for k, v in sorted(_cfg()["engines"].items(), key=lambda kv: kv[1]["rank"])}


def resolve(engine=None, purpose="catalog_stills"):
    """Return the engine record for `engine` (default: engine 1) after checking
    that it is allowed for `purpose`. Raises EngineViolation otherwise."""
    cfg = _cfg()
    # Locked purposes ignore the switch entirely; everything else follows it.
    if engine is None:
        eid = cfg["default"] if purpose in LOCKED_PURPOSES else active_engine()
    else:
        eid = engine
    if eid not in cfg["engines"]:
        raise EngineViolation(
            f"unknown engine '{eid}'. Declared engines: {', '.join(sorted(cfg['engines']))}.")
    rec = dict(cfg["engines"][eid])
    rec["id"] = eid

    if purpose in rec.get("blocked_for", []):
        raise EngineViolation(
            f"engine '{eid}' is blocked for '{purpose}': "
            f"{rec.get('catalog_block_reason', 'not approved for this purpose')} "
            f"Use engine '{cfg['default']}'.")
    allowed = rec.get("allowed_for", [])
    if allowed and purpose not in allowed:
        raise EngineViolation(
            f"engine '{eid}' is not declared for '{purpose}' (allowed: {', '.join(allowed)}).")
    if purpose == "catalog_stills" and not rec["catalog_approved"]:
        raise EngineViolation(f"engine '{eid}' is not catalog-approved. Catalog stills are engine "
                              f"'{cfg['default']}' only (docs/21, docs/26).")
    if rec["model_source"] == "config/model.json":
        rec["model"] = json.loads(MODEL_CFG.read_text(encoding="utf-8"))["model"]
    return rec


def assert_catalog_engine(engine=None):
    """Hard gate for anything that produces a delivered still."""
    return resolve(engine, purpose="catalog_stills")


def check():
    """Invariants that must hold for the engine lock to mean anything."""
    cfg = _cfg()
    problems = []
    if cfg["default"] != "higgsfield":
        problems.append(f"default engine is '{cfg['default']}', must be 'higgsfield' (docs/21)")
    if cfg.get("auto_fallback") is not False:
        problems.append("auto_fallback must be false (docs/21 §1a)")
    approved = [k for k, v in cfg["engines"].items() if v["catalog_approved"]]
    if approved != ["higgsfield"]:
        problems.append(f"catalog-approved engines = {approved}, must be exactly ['higgsfield']")
    hf = cfg["engines"]["higgsfield"]["call_constraints"]
    if hf["resolution"] != "2k" or hf["aspect_ratio"] != "1:1" or hf["count"] != 1:
        problems.append("engine 1 call constraints drifted from 2k / 1:1 / count 1")
    for eid, rec in cfg["engines"].items():
        if eid == "higgsfield":
            continue
        if "catalog_stills" not in rec.get("blocked_for", []):
            problems.append(f"engine '{eid}' does not block catalog_stills")
    # the active-engine switch must never reach a locked purpose
    saved = active_engine()
    try:
        for eid in cfg["engines"]:
            if eid == cfg["default"]:
                continue
            use(eid)
            got = resolve(purpose="catalog_stills")["id"]
            if got != cfg["default"]:
                problems.append(
                    f"active='{eid}' leaked into catalog_stills (resolved '{got}')")
    except EngineViolation as exc:
        problems.append(f"catalog_stills raised while switched: {exc}")
    finally:
        use(saved)

    # engine 2 must actually refuse a stills call
    for eid in cfg["engines"]:
        if eid == cfg["default"]:
            continue
        try:
            resolve(eid, purpose="catalog_stills")
            problems.append(f"engine '{eid}' resolved for catalog_stills but must not")
        except EngineViolation:
            pass
    return problems


if __name__ == "__main__":
    if "--use" in sys.argv:
        try:
            eid, status = use(sys.argv[sys.argv.index("--use") + 1])
        except EngineViolation as exc:
            sys.exit(f"STOP: {exc}")
        locked = _cfg()["default"]
        print(f"active engine -> {eid} ({status})")
        print(f"catalog stills remain {locked} (switch does not apply to delivered images)")
        sys.exit(0)
    if "--show" in sys.argv:
        cfg = _cfg()
        print(f"active (exploration/video): {active_engine()}")
        print(f"catalog stills (locked)   : {cfg['default']}")
        sys.exit(0)
    if "--list" in sys.argv:
        for eid, rec in list_engines().items():
            print(f"{rec['rank']}. {eid:<12} {rec['role']:<20} {rec['status']:<24} "
                  f"catalog={'yes' if rec['catalog_approved'] else 'NO'}")
        sys.exit(0)
    if "--check" in sys.argv:
        bad = check()
        for p in bad:
            print("ENGINE LOCK FAIL:", p)
        print("engine lock OK" if not bad else f"{len(bad)} problem(s)")
        sys.exit(1 if bad else 0)
    if "--resolve" in sys.argv:
        i = sys.argv.index("--resolve")
        eid = sys.argv[i + 1]
        purpose = "catalog_stills"
        if "--purpose" in sys.argv:
            purpose = sys.argv[sys.argv.index("--purpose") + 1]
        try:
            print(json.dumps(resolve(eid, purpose), indent=2))
        except EngineViolation as e:
            sys.exit(f"STOP: {e}")
        sys.exit(0)
    print(__doc__)
