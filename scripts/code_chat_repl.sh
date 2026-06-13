#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=$("$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx fastapi)

"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"

PYTHONPATH="$ROOT_DIR/apps/core" "$PYTHON_BIN" -m jarvis.cli repl --model jarvis-codex "$@"
