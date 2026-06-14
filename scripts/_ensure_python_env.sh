#!/usr/bin/env sh
set -eu

ROOT_DIR="$1"
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
if ! "$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx >/dev/null 2>&1; then
  echo "[jarvis] Python dependencies are unavailable in the current runtime."
  echo "[jarvis] Repair with:"
  echo "  cd "$ROOT_DIR""
  echo "  $ROOT_DIR/scripts/jarvis.sh setup-local"
  echo "[jarvis] Runtime targets:"
  echo "  JARVIS_VENV_DIR=$JARVIS_VENV_DIR"
  echo "  JARVIS_ENV_FILE=$JARVIS_ENV_FILE"
  exit 1
fi
