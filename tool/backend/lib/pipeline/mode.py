"""mode.py — pipeline version selection (safe-versioning rule 2/3, docs/15).

The active pipeline is chosen by ONE value, never by editing source:
  1. env PIPELINE_MODE (highest precedence — e.g. shadow testing / CI), else
  2. `active` in config/pipeline_versions.json (what rollback-pipeline.* sets).

This module is the single reader/writer of that registry so the rollback scripts
stay thin wrappers. Setting the active mode only rewrites the `active` field; it
never overwrites a version's stored config (rule 1: never destroy a working
version's settings).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from lib.config.paths import REPO_ROOT

REGISTRY = REPO_ROOT / "config" / "pipeline_versions.json"


def _load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def versions() -> dict:
    return _load()["versions"]


def active_mode() -> str:
    """env PIPELINE_MODE wins; else the registry's `active`. Validated against the
    known versions — an unknown mode falls back to `stable` with no crash."""
    reg = _load()
    env = os.getenv("PIPELINE_MODE")
    mode = env or reg.get("active") or reg.get("stable")
    if mode not in reg["versions"]:
        return reg.get("stable", next(iter(reg["versions"])))
    return mode


def stable_mode() -> str:
    return _load().get("stable", "legacy")


def get_version(mode: str | None = None) -> dict:
    reg = _load()
    mode = mode or active_mode()
    if mode not in reg["versions"]:
        raise KeyError(f"unknown pipeline mode {mode!r}; known: {list(reg['versions'])}")
    v = dict(reg["versions"][mode])
    v["mode"] = mode
    return v


def set_active(mode: str) -> str:
    """Persist the active mode (what rollback does). Only touches `active`."""
    reg = _load()
    if mode not in reg["versions"]:
        raise KeyError(f"unknown pipeline mode {mode!r}; known: {list(reg['versions'])}")
    reg["active"] = mode
    REGISTRY.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
    return mode


def summary() -> dict:
    reg = _load()
    return {
        "active_resolved": active_mode(),
        "active_config": reg.get("active"),
        "env_override": os.getenv("PIPELINE_MODE"),
        "stable": reg.get("stable"),
        "stable_commit": reg.get("stable_commit"),
        "versions": {k: v.get("status", "?") for k, v in reg["versions"].items()},
    }


def verify_pipelines() -> bool:
    """Import every pipeline module so a rollback can confirm both versions are
    usable (rule 1: the stable pipeline must always remain runnable)."""
    import importlib
    for m in ("lib.pipeline.pipeline", "lib.pipeline.qc",
              "lib.pipeline.fallback", "lib.pipeline.mode"):
        importlib.import_module(m)
    return True


def _cli() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Show or set the active pipeline mode (docs/15).")
    ap.add_argument("--set", metavar="MODE", help="set active pipeline (e.g. legacy, composite-v1)")
    ap.add_argument("--verify", action="store_true", help="confirm all pipeline modules import")
    a = ap.parse_args()
    if a.set:
        try:
            set_active(a.set)
        except KeyError:
            import sys
            print(f"error: unknown pipeline mode {a.set!r}; known: {list(versions())}")
            sys.exit(2)
        print(f"active pipeline set -> {a.set}")
    if a.verify:
        verify_pipelines()
        print("  both pipelines import OK")
    s = summary()
    print(f"resolved active : {s['active_resolved']}"
          + (f"  (env PIPELINE_MODE={s['env_override']})" if s["env_override"] else ""))
    print(f"config active   : {s['active_config']}")
    print(f"stable          : {s['stable']}  @ {s['stable_commit'][:9] if s['stable_commit'] else '?'}")
    print(f"versions        : {s['versions']}")


if __name__ == "__main__":
    _cli()
