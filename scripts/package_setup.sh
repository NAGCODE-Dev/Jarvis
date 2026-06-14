#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
PROFILE_MODE="quality"
WITH_INFRA=0
WITH_MODELS=0
DRY_RUN=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --speed)
      PROFILE_MODE="speed"
      ;;
    --quality)
      PROFILE_MODE="quality"
      ;;
    --with-infra)
      WITH_INFRA=1
      ;;
    --with-models)
      WITH_MODELS=1
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
    *)
      echo "[jarvis-setup] Uso: scripts/package_setup.sh [--speed|--quality] [--with-infra] [--with-models] [--dry-run]"
      exit 1
      ;;
  esac
  shift
done

print_plan() {
  echo "[jarvis-setup] Plano de runtime"
  echo "  ROOT_DIR=$ROOT_DIR"
  echo "  PROFILE_MODE=$PROFILE_MODE"
  echo "  WITH_INFRA=$WITH_INFRA"
  echo "  WITH_MODELS=$WITH_MODELS"
  echo "  JARVIS_RUNTIME_HOME=$JARVIS_RUNTIME_HOME"
  echo "  JARVIS_CONFIG_HOME=$JARVIS_CONFIG_HOME"
  echo "  JARVIS_VENV_DIR=$JARVIS_VENV_DIR"
  echo "  JARVIS_ENV_FILE=$JARVIS_ENV_FILE"
  echo "  JARVIS_DATA_DIR=$JARVIS_DATA_DIR"
  echo "  JARVIS_LOG_DIR=$JARVIS_LOG_DIR"
}

print_plan

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[jarvis-setup] Dry-run ativo; nenhuma mudança foi aplicada."
  exit 0
fi

mkdir -p "$JARVIS_RUNTIME_HOME" "$JARVIS_CONFIG_HOME" "$JARVIS_LOG_DIR" "$JARVIS_DATA_DIR"

if [ ! -f "$JARVIS_ENV_FILE" ]; then
  if [ -f "$ROOT_DIR/config/.env.example" ]; then
    cp "$ROOT_DIR/config/.env.example" "$JARVIS_ENV_FILE"
  else
    : > "$JARVIS_ENV_FILE"
  fi
fi

if [ ! -x "$JARVIS_VENV_DIR/bin/python" ]; then
  echo "[jarvis-setup] Criando virtualenv em $JARVIS_VENV_DIR"
  mkdir -p "$(dirname "$JARVIS_VENV_DIR")"
  python3 -m venv "$JARVIS_VENV_DIR"
fi

"$JARVIS_VENV_DIR/bin/python" -m ensurepip --upgrade >/dev/null 2>&1 || true
"$JARVIS_VENV_DIR/bin/python" -m pip install --upgrade pip
"$JARVIS_VENV_DIR/bin/python" -m pip install -e "$ROOT_DIR[dev]"

case "$PROFILE_MODE" in
  quality)
    "$ROOT_DIR/scripts/apply_quality_profile.sh"
    ;;
  speed)
    "$ROOT_DIR/scripts/apply_speed_profile.sh"
    ;;
  *)
    echo "[jarvis-setup] Perfil inválido: $PROFILE_MODE"
    exit 1
    ;;
esac

if [ "$WITH_INFRA" -eq 1 ]; then
  "$ROOT_DIR/scripts/start_infra.sh" || true
fi

if [ "$WITH_MODELS" -eq 1 ]; then
  "$ROOT_DIR/scripts/pull_models.sh" || true
fi

echo "[jarvis-setup] Runtime preparado via scripts/jarvis.sh setup-local"
echo "[jarvis-setup] Próximos passos:"
echo "  1. $ROOT_DIR/scripts/jarvis.sh doctor"
echo "  2. $ROOT_DIR/scripts/jarvis.sh boot --no-seed"
echo "  3. $ROOT_DIR/scripts/verify_local.sh"
