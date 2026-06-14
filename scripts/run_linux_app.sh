#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"
APP_URL="${JARVIS_APP_URL:-http://${HOST}:${PORT}/app/}"
BOOT_ARGS="${JARVIS_BOOT_ARGS:---no-seed}"
HELP_PAGE="$ROOT_DIR/apps/linux/package_help.html"

is_up() {
  curl -fsS "http://${HOST}:${PORT}/health" >/dev/null 2>&1
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

open_help() {
  target="$1"
  if command -v xdg-open >/dev/null 2>&1; then
    nohup xdg-open "$target" >/dev/null 2>&1 &
    return 0
  fi
  if browser=$(find_browser); then
    nohup "$browser" "$target" >/dev/null 2>&1 &
    return 0
  fi
  echo "[jarvis-linux] Nenhum navegador compatível encontrado. Abra manualmente: $target"
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

show_help_page() {
  echo "[jarvis-linux] Abrindo ajuda local de recuperação..."
  if [ -f "$HELP_PAGE" ]; then
    open_help "file://$HELP_PAGE" || true
  fi
  echo "[jarvis-linux] Diagnóstico rápido:"
  "$ROOT_DIR/scripts/package_doctor.sh" || true
}

start_if_needed() {
  if is_up; then
    return 0
  fi
  echo "[jarvis-linux] Iniciando Jarvis local..."
  if ! "$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"; then
    echo "[jarvis-linux] Ambiente Python indisponível para iniciar o core."
    return 1
  fi
  # shellcheck disable=SC2086
  if ! "$ROOT_DIR/scripts/jarvis.sh" boot $BOOT_ARGS >/dev/null 2>&1; then
    echo "[jarvis-linux] Boot local falhou."
    return 1
  fi
  if ! is_up; then
    echo "[jarvis-linux] Core ainda não está saudável após o boot."
    return 1
  fi
  return 0
}

if ! start_if_needed; then
  show_help_page
  exit 1
fi

open_app
