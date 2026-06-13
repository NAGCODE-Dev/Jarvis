#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=$("$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx fastapi)

PYTHONPATH="$ROOT_DIR/apps/core" "$PYTHON_BIN" -m jarvis.cli status
