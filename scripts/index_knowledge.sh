#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"
PYTHON_BIN=$($ROOT_DIR/scripts/_resolve_python.sh "$ROOT_DIR" httpx fastapi)

PYTHONPATH="$ROOT_DIR/apps/core" exec "$PYTHON_BIN" -m jarvis.cli index-knowledge "$@"
