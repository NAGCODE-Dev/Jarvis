#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/obsidian_chat.sh <note.md> [instruction]"
  exit 1
fi

NOTE_PATH=$1
shift || true

PYTHONPATH="$ROOT_DIR/apps/core" "$VENV_PYTHON" -m jarvis.cli obsidian-note "$NOTE_PATH" "${1:-}" --append --title "Jarvis Chat"
