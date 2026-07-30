#!/usr/bin/env python3
"""Hard preflight guard for tool calls (user-locked 2026-07-30). NOT a guideline.

Wrap every programmatic tool call through preflight(). Retrieval and display are
DIFFERENT things and are treated differently:

- BANNED_DISPLAY: gallery/widget spam + prompt echo. NEVER call. Raise.
- RETRIEVAL_ALLOWED (job_display): allowed EXACTLY ONCE per catalog, only to
  obtain render URLs. Its output is piped to build/<SKU>_urls.json and NEVER
  echoed, NEVER rendered as a widget, NEVER used to view images. A second call
  in the same catalog raises. The count is tracked in build/<SKU>_state.json so
  the limit is enforced, not remembered.
- spawn_agent / background_task: never (subagent ban).

Drive listings must pass minimal fields (no content snippets).
"""
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIOLATIONS = ROOT / "memory" / "policy_violations.json"
BUILD = ROOT / "build"

BANNED_DISPLAY = {"show_generations", "show_marketing_studio_generations"}
RETRIEVAL_ALLOWED = {"job_display"}
BANNED_TOOLS = {"spawn_agent", "background_task"}
DRIVE_TOOLS = {"search_files", "list_recent_files"}
DRIVE_REQUIRED_FIELDS = "files(id,name,mimeType)"


class PolicyViolation(RuntimeError):
    pass


def _log(tool, detail):
    try:
        data = json.loads(VIOLATIONS.read_text(encoding="utf-8")) if VIOLATIONS.exists() else []
    except Exception:
        data = []
    data.append({"ts": int(time.time()), "tool": tool, "detail": detail})
    VIOLATIONS.parent.mkdir(parents=True, exist_ok=True)
    VIOLATIONS.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _state_path(sku):
    return BUILD / f"{sku}_state.json"


def _load_state(sku):
    p = _state_path(sku)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"sku": sku, "job_display_calls": 0}


def _save_state(sku, st):
    BUILD.mkdir(parents=True, exist_ok=True)
    _state_path(sku).write_text(json.dumps(st, indent=2), encoding="utf-8")


def preflight(tool_name, sku=None, **kwargs):
    """Call before any tool. Raises PolicyViolation on a banned tool, a Drive
    listing with snippets, or a second job_display in the same catalog."""
    if tool_name in BANNED_DISPLAY:
        _log(tool_name, "banned DISPLAY tool blocked (widget/echo)")
        raise PolicyViolation(f"BANNED display tool '{tool_name}' — blocked; use job_display for URL retrieval only.")
    if tool_name in BANNED_TOOLS:
        _log(tool_name, "banned tool blocked")
        raise PolicyViolation(f"BANNED tool '{tool_name}' — blocked by preflight.")
    if tool_name in RETRIEVAL_ALLOWED:
        if not sku:
            raise PolicyViolation("job_display requires sku= to enforce the one-call-per-catalog limit.")
        st = _load_state(sku)
        if st.get("job_display_calls", 0) >= 1:
            _log(tool_name, f"second job_display for {sku} blocked")
            raise PolicyViolation(f"job_display already used for {sku} (one per catalog). Reuse build/{sku}_urls.json.")
        st["job_display_calls"] = st.get("job_display_calls", 0) + 1
        _save_state(sku, st)
        return kwargs
    if tool_name in DRIVE_TOOLS:
        if kwargs.get("include_snippets") or kwargs.get("excludeContentSnippets") is False:
            _log(tool_name, "drive listing with snippets blocked")
            raise PolicyViolation(f"Drive '{tool_name}' must not request content snippets.")
        kwargs.setdefault("fields", DRIVE_REQUIRED_FIELDS)
    return kwargs


if __name__ == "__main__":
    for t in sorted(BANNED_DISPLAY | BANNED_TOOLS):
        try:
            preflight(t); print("FAIL not blocked:", t)
        except PolicyViolation:
            print("blocked:", t)
    # job_display: first allowed, second blocked
    import tempfile
    preflight("job_display", sku="_selftest")
    try:
        preflight("job_display", sku="_selftest"); print("FAIL second job_display not blocked")
    except PolicyViolation:
        print("blocked: job_display 2nd call")
    (BUILD / "_selftest_state.json").unlink(missing_ok=True)
    print("preflight OK")
