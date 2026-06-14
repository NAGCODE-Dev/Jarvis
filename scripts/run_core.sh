#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
PYTHON_BIN=$($ROOT_DIR/scripts/_resolve_python.sh "$ROOT_DIR" uvicorn fastapi httpx)
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"

PYTHONPATH="$ROOT_DIR/apps/core" exec "$PYTHON_BIN" -m uvicorn jarvis.main:app --host "$HOST" --port "$PORT"
