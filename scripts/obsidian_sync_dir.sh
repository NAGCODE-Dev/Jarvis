#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/obsidian_sync_dir.sh <directory> [workspace]"
  exit 1
fi

TARGET_DIR=$1
shift || true

if [ "$#" -ge 1 ]; then
  PYTHONPATH="$ROOT_DIR/apps/core" "$VENV_PYTHON" -m jarvis.cli obsidian-sync-dir "$TARGET_DIR" --workspace "$1"
else
  PYTHONPATH="$ROOT_DIR/apps/core" "$VENV_PYTHON" -m jarvis.cli obsidian-sync-dir "$TARGET_DIR"
fi
