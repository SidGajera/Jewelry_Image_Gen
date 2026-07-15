#!/usr/bin/env bash
# Start the Lucent Carat Lab catalog generator backend (macOS/Linux).
# Run scripts/setup.sh first if you haven't.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND="$REPO_ROOT/tool/backend"

if [ ! -d "$BACKEND/.venv" ]; then
  echo "No virtualenv found — run ./scripts/setup.sh first."
  exit 1
fi

# shellcheck disable=SC1091
source "$BACKEND/.venv/bin/activate"
cd "$BACKEND"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"
echo "Starting server at http://$HOST:$PORT ..."
exec uvicorn server:app --host "$HOST" --port "$PORT"
