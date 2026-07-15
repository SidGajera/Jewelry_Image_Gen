"""Standalone startup validation — run before enabling generation.

Exits 0 only when the repo is structurally sound (required files/assets present,
workspace paths writable, locked asset checksums match). Missing provider secrets
are reported but do NOT fail the exit code — the app can boot; it must simply
refuse to spend credits until they're filled in. No provider call is made here,
so this never spends credits.

Usage: python health_check.py   (from tool/backend/, with the venv active)
"""
import hashlib
import sys

import config
from lib.config.paths import PATHS

FAIL = []
WARN = []
OK = []


def check_required_files():
    for rel in config.MANIFEST.get("required_files", []):
        path = config.REPO_ROOT / rel
        if path.exists():
            OK.append(f"required file present: {rel}")
        else:
            FAIL.append(f"MISSING required file: {rel}")


def check_locked_assets():
    checksums = config.MANIFEST.get("locked_asset_checksums", {})
    for rel, meta in checksums.items():
        path = config.REPO_ROOT / rel
        if not path.exists():
            FAIL.append(f"MISSING locked asset: {rel}")
            continue
        data = path.read_bytes()
        if len(data) != meta.get("bytes"):
            FAIL.append(f"locked asset size mismatch: {rel}")
            continue
        digest = hashlib.sha256(data).hexdigest()
        if digest != meta.get("sha256"):
            FAIL.append(f"locked asset checksum mismatch (asset was modified): {rel}")
        else:
            OK.append(f"locked asset verified: {rel}")


def check_paths_writable():
    try:
        PATHS.ensure_dirs()
    except OSError as e:
        FAIL.append(f"could not create/write workspace directories: {e}")
        return
    for d in PATHS.writable_dirs():
        probe = d / ".health_check_probe"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            OK.append(f"path writable: {d}")
        except OSError as e:
            FAIL.append(f"path NOT writable: {d} ({e})")


def check_secrets():
    secrets = {
        "HIGGSFIELD_API_KEY": config.HIGGSFIELD_API_KEY,
        "ANTHROPIC_API_KEY": config.ANTHROPIC_API_KEY,
        "GOOGLE_APPLICATION_CREDENTIALS": config.GOOGLE_CREDS,
    }
    for name, value in secrets.items():
        if value:
            OK.append(f"secret configured: {name}")
        else:
            WARN.append(f"secret NOT set (generation will be blocked until added to tool/.env): {name}")


def main():
    check_required_files()
    check_locked_assets()
    check_paths_writable()
    check_secrets()

    print("=== Lucent Carat Lab — health check ===")
    for line in OK:
        print(f"  OK   {line}")
    for line in WARN:
        print(f"  WARN {line}")
    for line in FAIL:
        print(f"  FAIL {line}")

    if FAIL:
        print(f"\n{len(FAIL)} structural problem(s) found — fix the items above before starting.")
        sys.exit(1)
    if WARN:
        print(f"\nStructurally OK. {len(WARN)} secret(s) missing — app will start but cannot generate until added.")
    else:
        print("\nAll checks passed. Ready to generate.")
    sys.exit(0)


if __name__ == "__main__":
    main()
