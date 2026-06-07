#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"

if [ ! -x "$VENV_PYTHON" ]; then
  echo "[jarvis] Virtual environment not found. Run scripts/install_host.sh first."
  exit 1
fi

PYTHONPATH="$ROOT_DIR/apps/core" exec "$VENV_PYTHON" -m uvicorn jarvis.main:app --host "$HOST" --port "$PORT"
