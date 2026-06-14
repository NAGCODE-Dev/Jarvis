#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
VENV_DIR="$JARVIS_VENV_DIR"
ENV_FILE="$JARVIS_ENV_FILE"

echo "[jarvis] Installing Ubuntu dependencies"
if command -v sudo >/dev/null 2>&1; then
  SUDO="sudo"
else
  SUDO=""
fi

$SUDO apt-get update
$SUDO apt-get install -y   python3-venv   python3-pip   curl   ca-certificates   build-essential   git   poppler-utils   libreoffice-common

if ! command -v docker >/dev/null 2>&1; then
  echo "[jarvis] Installing Docker"
  curl -fsSL https://get.docker.com | sh
fi

if ! command -v ollama >/dev/null 2>&1; then
  echo "[jarvis] Installing Ollama"
  curl -fsSL https://ollama.com/install.sh | sh
fi

echo "[jarvis] Creating Python virtual environment at $VENV_DIR"
mkdir -p "$(dirname "$VENV_DIR")" "$(dirname "$ENV_FILE")"
python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -e "$ROOT_DIR[dev]"

if [ ! -f "$ENV_FILE" ]; then
  cp "$ROOT_DIR/config/.env.example" "$ENV_FILE"
fi

"$ROOT_DIR/scripts/apply_quality_profile.sh"

echo "[jarvis] Done"
