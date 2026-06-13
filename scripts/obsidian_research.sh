#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=$("$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx fastapi)

"$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"

if [ "$#" -lt 1 ]; then
  echo "Usage: scripts/obsidian_research.sh <note.md> [instruction]"
  exit 1
fi

NOTE_PATH=$1
shift || true

PYTHONPATH="$ROOT_DIR/apps/core" "$PYTHON_BIN" -m jarvis.cli obsidian-note "$NOTE_PATH" "${1:-Pesquise usando contexto local e responda em Markdown com referências úteis.}" --model jarvis-pesquisador-safe --append --title "Jarvis Research"
