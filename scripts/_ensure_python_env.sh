#!/usr/bin/env sh
set -eu

ROOT_DIR="$1"
if ! "$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx >/dev/null 2>&1; then
  echo "[jarvis] Python dependencies are unavailable in both .venv and python3."
  echo "[jarvis] Repair with:"
  echo "  cd \"$ROOT_DIR\""
  echo "  ./.venv/bin/python -m ensurepip --upgrade"
  echo "  ./.venv/bin/python -m pip install --upgrade pip"
  echo "  ./.venv/bin/python -m pip install -e \".[dev]\""
  exit 1
fi
