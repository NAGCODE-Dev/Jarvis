#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
COMMAND=${1:-help}
if [ "$#" -gt 0 ]; then
  shift
fi

python_bin() {
  "$ROOT_DIR/scripts/_ensure_python_env.sh" "$ROOT_DIR"
  "$ROOT_DIR/scripts/_resolve_python.sh" "$ROOT_DIR" httpx fastapi
}

run_cli_chat() {
  mode="$1"
  model="$2"
  shift 2
  PYTHON_BIN=$(python_bin)
  exec env PYTHONPATH="$ROOT_DIR/apps/core" "$PYTHON_BIN" -m jarvis.cli "$mode" --model "$model" "$@"
}

usage() {
  cat <<'EOF'
Jarvis local launcher

Uso:
  scripts/jarvis.sh boot [--no-seed|--benchmark|--speed|--quality]
  scripts/jarvis.sh app
  scripts/jarvis.sh core
  scripts/jarvis.sh stop
  scripts/jarvis.sh status
  scripts/jarvis.sh doctor
  scripts/jarvis.sh setup-local [--speed|--quality] [--with-infra] [--with-models] [--dry-run]
  scripts/jarvis.sh verify [args]
  scripts/jarvis.sh deb-build
  scripts/jarvis.sh deb-install [--rebuild]
  scripts/jarvis.sh chat [prompt...]
  scripts/jarvis.sh code [prompt...]
  scripts/jarvis.sh research [prompt...]
  scripts/jarvis.sh repl
  scripts/jarvis.sh code-repl
  scripts/jarvis.sh research-repl
  scripts/jarvis.sh help
EOF
}

case "$COMMAND" in
  boot)
    exec "$ROOT_DIR/scripts/boot_local.sh" "$@"
    ;;
  app)
    exec "$ROOT_DIR/scripts/run_linux_app.sh" "$@"
    ;;
  core)
    exec "$ROOT_DIR/scripts/run_core.sh" "$@"
    ;;
  stop)
    exec "$ROOT_DIR/scripts/stop_core.sh" "$@"
    ;;
  status)
    exec "$ROOT_DIR/scripts/status.sh" "$@"
    ;;
  doctor)
    exec "$ROOT_DIR/scripts/package_doctor.sh" "$@"
    ;;
  setup-local)
    exec "$ROOT_DIR/scripts/package_setup.sh" "$@"
    ;;
  verify)
    exec "$ROOT_DIR/scripts/verify_local.sh" "$@"
    ;;
  deb-build)
    exec "$ROOT_DIR/scripts/build_deb.sh" "$@"
    ;;
  deb-install)
    exec "$ROOT_DIR/scripts/install_deb_local.sh" "$@"
    ;;
  chat)
    run_cli_chat chat jarvis-safe "$@"
    ;;
  code)
    run_cli_chat chat jarvis-codex "$@"
    ;;
  research)
    run_cli_chat chat jarvis-pesquisador-safe "$@"
    ;;
  repl)
    run_cli_chat repl jarvis-safe "$@"
    ;;
  code-repl)
    run_cli_chat repl jarvis-codex "$@"
    ;;
  research-repl)
    run_cli_chat repl jarvis-pesquisador-safe "$@"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    echo "[jarvis] Comando desconhecido: $COMMAND" >&2
    usage >&2
    exit 1
    ;;
esac
