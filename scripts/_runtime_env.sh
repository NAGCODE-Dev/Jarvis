#!/usr/bin/env sh
set -eu

ROOT_DIR="$1"
DEFAULT_RUNTIME_HOME="${XDG_DATA_HOME:-$HOME/.local/share}/jarvis-local"
DEFAULT_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}/jarvis-local"

if [ -w "$ROOT_DIR" ]; then
  ROOT_WRITABLE=1
else
  ROOT_WRITABLE=0
fi

RUNTIME_HOME="${JARVIS_RUNTIME_HOME:-$DEFAULT_RUNTIME_HOME}"
CONFIG_HOME="${JARVIS_CONFIG_HOME:-$DEFAULT_CONFIG_HOME}"

if [ -n "${JARVIS_VENV_DIR:-}" ]; then
  VENV_DIR="$JARVIS_VENV_DIR"
elif [ "$ROOT_WRITABLE" -eq 1 ]; then
  VENV_DIR="$ROOT_DIR/.venv"
else
  VENV_DIR="$RUNTIME_HOME/.venv"
fi

if [ -n "${JARVIS_ENV_FILE:-}" ]; then
  ENV_FILE="$JARVIS_ENV_FILE"
elif [ "$ROOT_WRITABLE" -eq 1 ]; then
  ENV_FILE="$ROOT_DIR/.env"
else
  ENV_FILE="$CONFIG_HOME/.env"
fi

if [ -n "${JARVIS_LOG_DIR:-}" ]; then
  LOG_DIR="$JARVIS_LOG_DIR"
elif [ "$ROOT_WRITABLE" -eq 1 ]; then
  LOG_DIR="$ROOT_DIR/logs"
else
  LOG_DIR="$RUNTIME_HOME/logs"
fi

if [ -n "${JARVIS_DATA_DIR:-}" ]; then
  DATA_DIR="$JARVIS_DATA_DIR"
elif [ "$ROOT_WRITABLE" -eq 1 ]; then
  DATA_DIR="$ROOT_DIR/data"
else
  DATA_DIR="$RUNTIME_HOME/data"
fi

printf 'export JARVIS_RUNTIME_HOME=%s
' "$RUNTIME_HOME"
printf 'export JARVIS_CONFIG_HOME=%s
' "$CONFIG_HOME"
printf 'export JARVIS_VENV_DIR=%s
' "$VENV_DIR"
printf 'export JARVIS_ENV_FILE=%s
' "$ENV_FILE"
printf 'export JARVIS_LOG_DIR=%s
' "$LOG_DIR"
printf 'export JARVIS_DATA_DIR=%s
' "$DATA_DIR"
