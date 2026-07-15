#!/usr/bin/env bash
# Standalone health check (macOS/Linux) — never spends generation credits.
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND="$REPO_ROOT/tool/backend"

if [ -x "$BACKEND/.venv/bin/python3" ]; then
  "$BACKEND/.venv/bin/python3" "$BACKEND/health_check.py"
else
  python3 "$BACKEND/health_check.py"
fi
