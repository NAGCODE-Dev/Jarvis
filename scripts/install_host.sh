#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV_DIR="$ROOT_DIR/.venv"

echo "[jarvis] Installing Ubuntu dependencies"
if command -v sudo >/dev/null 2>&1; then
  SUDO="sudo"
else
  SUDO=""
fi

$SUDO apt-get update
$SUDO apt-get install -y \
  python3-venv \
  python3-pip \
  curl \
  ca-certificates \
  build-essential \
  git \
  poppler-utils \
  libreoffice-common

if ! command -v docker >/dev/null 2>&1; then
  echo "[jarvis] Installing Docker"
  curl -fsSL https://get.docker.com | sh
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "[jarvis] Installing Ollama"
  curl -fsSL https://ollama.com/install.sh | sh
fi

echo "[jarvis] Creating Python virtual environment"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -e "$ROOT_DIR[dev]"

if [ ! -f "$ROOT_DIR/.env" ]; then
  cp "$ROOT_DIR/config/.env.example" "$ROOT_DIR/.env"
fi

echo "[jarvis] Done"

