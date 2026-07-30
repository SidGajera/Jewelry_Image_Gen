#!/usr/bin/env python3
"""Hard preflight guard for tool calls (user-locked 2026-07-30). NOT a guideline.

Wrap every programmatic tool call through preflight(). If the tool name is
banned, raise immediately — do not call, do not warn, do not proceed — and log
the attempt to memory/policy_violations.json so repeat offenders are visible.

Also enforces the Drive listing rule: never the default listing (it pulls every
file's content snippet). Always request minimal fields.

These bans also bind the assistant's own behavior: never invoke a banned tool,
never browse Drive with snippets on.
"""
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIOLATIONS = ROOT / "memory" / "policy_violations.json"

BANNED_TOOLS = {
    "show_generations", "show_marketing_studio_generations",
    "spawn_agent", "background_task",
}
# Any Drive listing MUST restrict fields; the default listing pulls content snippets.
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


def preflight(tool_name, **kwargs):
    """Call before any tool. Raises PolicyViolation on a banned tool or a Drive
    listing without minimal fields. Returns kwargs (possibly normalised)."""
    if tool_name in BANNED_TOOLS:
        _log(tool_name, "banned tool invocation blocked")
        raise PolicyViolation(f"BANNED tool '{tool_name}' — blocked by preflight, not called.")
    if tool_name in DRIVE_TOOLS:
        fields = kwargs.get("fields")
        snippets = kwargs.get("include_snippets") or kwargs.get("excludeContentSnippets") is False
        if snippets or (fields and "snippet" in str(fields).lower()):
            _log(tool_name, "drive listing with content snippets blocked")
            raise PolicyViolation(f"Drive '{tool_name}' must not request content snippets.")
        kwargs.setdefault("fields", DRIVE_REQUIRED_FIELDS)
    return kwargs


if __name__ == "__main__":
    # self-test
    for t in sorted(BANNED_TOOLS):
        try:
            preflight(t)
            print("FAIL not blocked:", t)
        except PolicyViolation:
            print("blocked:", t)
    preflight("search_files")
    print("drive fields default enforced")
