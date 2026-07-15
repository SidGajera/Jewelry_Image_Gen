#!/usr/bin/env bash
# One-command setup for the Lucent Carat Lab catalog generator (macOS/Linux).
# Safe to re-run. Never spends generation credits.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND="$REPO_ROOT/tool/backend"
MISSING=()

echo "== Lucent Carat Lab setup =="

# 1. Required software
if ! command -v python3 >/dev/null 2>&1; then
  MISSING+=("python3 (>=3.10) — install it, then re-run this script")
fi

if [ ${#MISSING[@]} -ne 0 ]; then
  echo "Cannot continue — missing prerequisites:"
  printf '  - %s\n' "${MISSING[@]}"
  exit 1
fi

PY_VER="$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
echo "Using python3 $PY_VER"

# 2. Virtualenv + dependencies
if [ ! -d "$BACKEND/.venv" ]; then
  echo "Creating virtualenv..."
  python3 -m venv "$BACKEND/.venv"
fi
# shellcheck disable=SC1091
source "$BACKEND/.venv/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet -r "$BACKEND/requirements.txt"

# 3. .env
if [ ! -f "$REPO_ROOT/tool/.env" ]; then
  echo "Copying .env.example -> tool/.env (fill in your keys before generating)"
  cp "$BACKEND/.env.example" "$REPO_ROOT/tool/.env"
fi

# 4. Workspace directories (also created by the app at import time; done here for visible feedback)
for d in source reference input output cache temp deliveries; do
  mkdir -p "$REPO_ROOT/workspace/$d"
done
mkdir -p "$BACKEND/jobs"

# 5. Health check (structural only — never calls a provider, never spends credits)
echo ""
python3 "$BACKEND/health_check.py"
STATUS=$?

echo ""
if [ $STATUS -eq 0 ]; then
  echo "Setup complete. Next: add your keys to tool/.env if you haven't, then run:"
  echo "  ./scripts/start.sh"
else
  echo "Setup finished with structural problems above — fix them and re-run setup.sh."
fi
exit $STATUS
