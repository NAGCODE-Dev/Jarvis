#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"
PYTHON_BIN=$($ROOT_DIR/scripts/_resolve_python.sh "$ROOT_DIR" httpx fastapi)

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/obsidian_remember_note.sh <note.md> [workspace]"
  exit 1
fi

NOTE_PATH=$1
shift || true

if [ "$#" -ge 1 ]; then
  PYTHONPATH="$ROOT_DIR/apps/core" exec "$PYTHON_BIN" -m jarvis.cli obsidian-remember "${NOTE_PATH}" --workspace "$1"
else
  PYTHONPATH="$ROOT_DIR/apps/core" exec "$PYTHON_BIN" -m jarvis.cli obsidian-remember "${NOTE_PATH}"
fi
