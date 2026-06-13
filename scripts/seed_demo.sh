#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PYTHON_BIN=$("$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx fastapi)

run() {
  PYTHONPATH="$ROOT_DIR/apps/core" "$PYTHON_BIN" -m jarvis.cli memory-action "$@"
}

run set_identity_fact profile.name '"Nikolas"'
run update_preference preferences.editor '"VS Code"'
run update_preference preferences.response_style '"concise and practical"'
run update_constraint constraints.hardware '"CPU only, 16 GB RAM, no dedicated GPU"'
run update_state weight.current_kg 72
run append_workspace_note current_focus '"router + memory service"' --workspace jarvis
run append_workspace_note project_type '"local assistant"' --workspace jarvis

echo "[jarvis] Demo memory seeded."
