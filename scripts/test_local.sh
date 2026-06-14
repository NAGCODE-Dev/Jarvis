#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"
PYTHON_BIN=$("$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" pytest fastapi httpx)

cd "$ROOT_DIR"
PYTHONPATH="$ROOT_DIR/apps/core" exec "$PYTHON_BIN" -m pytest -q tests/test_api.py tests/test_integrations.py
