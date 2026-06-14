#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
STATUS_URL="http://127.0.0.1:8000/health"

say() { printf '%s
' "$1"; }
check_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    say "[ok] comando disponível: $1"
  else
    say "[warn] comando ausente: $1"
  fi
}

say "[jarvis-doctor] ROOT_DIR=$ROOT_DIR"
say "[jarvis-doctor] JARVIS_VENV_DIR=$JARVIS_VENV_DIR"
say "[jarvis-doctor] JARVIS_ENV_FILE=$JARVIS_ENV_FILE"
say "[jarvis-doctor] JARVIS_DATA_DIR=$JARVIS_DATA_DIR"
say "[jarvis-doctor] JARVIS_LOG_DIR=$JARVIS_LOG_DIR"
check_cmd python3
check_cmd curl
check_cmd ollama
check_cmd docker

if [ -x "$JARVIS_VENV_DIR/bin/python" ]; then
  say "[ok] virtualenv encontrado: $JARVIS_VENV_DIR/bin/python"
else
  say "[warn] virtualenv ausente: $JARVIS_VENV_DIR/bin/python"
fi

if "$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx fastapi uvicorn >/dev/null 2>&1; then
  PYTHON_BIN=$($ROOT_DIR/scripts/_resolve_python.sh "$ROOT_DIR" httpx fastapi uvicorn)
  say "[ok] python operacional: $PYTHON_BIN"
else
  say "[fail] nenhuma runtime Python com httpx/fastapi/uvicorn disponível"
fi

if [ -f "$JARVIS_ENV_FILE" ]; then
  say "[ok] .env encontrado: $JARVIS_ENV_FILE"
else
  say "[warn] .env ausente: $JARVIS_ENV_FILE"
fi

if curl -fsS "$STATUS_URL" >/dev/null 2>&1; then
  say "[ok] core saudável em $STATUS_URL"
else
  say "[warn] core indisponível em $STATUS_URL"
fi

say "[jarvis-doctor] próximos passos sugeridos:"
say "  1. $ROOT_DIR/scripts/jarvis.sh setup-local --dry-run"
say "  2. $ROOT_DIR/scripts/jarvis.sh setup-local"
say "  3. $ROOT_DIR/scripts/jarvis.sh boot --no-seed"
say "  4. $ROOT_DIR/scripts/jarvis.sh status"
say "  5. $ROOT_DIR/scripts/verify_local.sh"
