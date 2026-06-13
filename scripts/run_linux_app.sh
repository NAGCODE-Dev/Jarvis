#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"
APP_URL="${JARVIS_APP_URL:-http://${HOST}:${PORT}/app/}"
BOOT_ARGS="${JARVIS_BOOT_ARGS:---no-seed}"

is_up() {
  curl -fsS "http://${HOST}:${PORT}/health" >/dev/null 2>&1
}

start_if_needed() {
  if is_up; then
    return 0
  fi
  echo "[jarvis-linux] Iniciando Jarvis local..."
  # shellcheck disable=SC2086
  "$ROOT_DIR/scripts/boot_local.sh" $BOOT_ARGS >/dev/null 2>&1
}

find_browser() {
  for candidate in google-chrome chromium chromium-browser brave-browser microsoft-edge-stable microsoft-edge; do
    if command -v "$candidate" >/dev/null 2>&1; then
      printf '%s
' "$candidate"
      return 0
    fi
  done
  return 1
}

open_app() {
  if browser=$(find_browser); then
    nohup "$browser" --app="$APP_URL" >/dev/null 2>&1 &
    return 0
  fi

  if command -v xdg-open >/dev/null 2>&1; then
    nohup xdg-open "$APP_URL" >/dev/null 2>&1 &
    return 0
  fi

  echo "[jarvis-linux] Nenhum navegador compatível encontrado. Abra manualmente: $APP_URL"
  return 1
}

start_if_needed
open_app
