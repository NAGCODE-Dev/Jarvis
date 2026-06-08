#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"

PYTHONPATH="$ROOT_DIR/apps/core" "$VENV_PYTHON" -m jarvis.cli repl --model jarvis-programador-safe "$@"
