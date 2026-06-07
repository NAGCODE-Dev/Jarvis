#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
  echo "[jarvis] Virtual environment not found. Run scripts/install_host.sh first."
  exit 1
fi

run() {
  PYTHONPATH="$ROOT_DIR/apps/core" "$VENV_PYTHON" -m jarvis.cli memory-action "$@"
}

run set_identity_fact profile.name '"Nikolas"'
run update_preference preferences.editor '"VS Code"'
run update_preference preferences.response_style '"concise and practical"'
run update_constraint constraints.hardware '"CPU only, 16 GB RAM, no dedicated GPU"'
run update_state weight.current_kg 72
run append_workspace_note current_focus '"router + memory service"' --workspace jarvis
run append_workspace_note project_type '"local assistant"' --workspace jarvis

echo "[jarvis] Demo memory seeded."
