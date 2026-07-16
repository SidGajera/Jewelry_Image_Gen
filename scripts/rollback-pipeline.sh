#!/usr/bin/env bash
# One-click pipeline rollback / switch (macOS/Linux). Safe-versioning rule 3.
#   ./scripts/rollback-pipeline.sh legacy
#   ./scripts/rollback-pipeline.sh composite-v1
# Sets the active pipeline via config/pipeline_versions.json (env PIPELINE_MODE still
# overrides at runtime), restoring that version's profile, then verifies both
# pipelines import. Never edits source, never deletes a version's config.
set -euo pipefail

MODE="${1:-}"
if [ -z "$MODE" ]; then
  echo "usage: ./scripts/rollback-pipeline.sh <legacy|composite-v1>"
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$REPO_ROOT/tool/backend"
VENV="$BACKEND/.venv/bin/python"
[ -x "$VENV" ] || VENV="$BACKEND/.venv/Scripts/python.exe"   # git-bash on Windows
if [ ! -x "$VENV" ]; then
  echo "No virtualenv — run ./scripts/setup.sh first."
  exit 1
fi

cd "$BACKEND"
"$VENV" -m lib.pipeline.mode --set "$MODE" --verify || { echo "Rollback failed for mode '$MODE' — investigate."; exit 1; }
echo "Active pipeline is now '$MODE'. Restart the server to pick it up: ./scripts/start.sh"
