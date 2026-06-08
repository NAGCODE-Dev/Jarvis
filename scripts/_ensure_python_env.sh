#!/usr/bin/env sh
set -eu

ROOT_DIR="$1"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"

if [ ! -x "$VENV_PYTHON" ]; then
  echo "[jarvis] Virtual environment not found. Run scripts/install_host.sh first."
  exit 1
fi

if ! "$VENV_PYTHON" -c "import httpx" >/dev/null 2>&1; then
  echo "[jarvis] Python dependencies are missing in .venv."
  echo "[jarvis] Repair with:"
  echo "  cd \"$ROOT_DIR\""
  echo "  ./.venv/bin/python -m ensurepip --upgrade"
  echo "  ./.venv/bin/python -m pip install --upgrade pip"
  echo "  ./.venv/bin/python -m pip install -e \".[dev]\""
  exit 1
fi
