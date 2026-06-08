#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SKIP_INSTALL=0
SKIP_PULL=0
BOOT_ARGS=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --skip-install)
      SKIP_INSTALL=1
      ;;
    --skip-pull)
      SKIP_PULL=1
      ;;
    --no-seed|--benchmark)
      BOOT_ARGS="$BOOT_ARGS $1"
      ;;
    *)
      echo "[jarvis] Unknown option: $1"
      echo "Usage: scripts/first_run.sh [--skip-install] [--skip-pull] [--no-seed] [--benchmark]"
      exit 1
      ;;
  esac
  shift
done

echo "[jarvis] First run bootstrap"

if [ "$SKIP_INSTALL" -eq 0 ]; then
  echo "[jarvis] Step 1/3: install host dependencies"
  "$ROOT_DIR/scripts/install_host.sh"
else
  echo "[jarvis] Step 1/3 skipped: install"
fi

if [ "$SKIP_PULL" -eq 0 ]; then
  echo "[jarvis] Step 2/3: pull models"
  "$ROOT_DIR/scripts/pull_models.sh"
else
  echo "[jarvis] Step 2/3 skipped: model pull"
fi

echo "[jarvis] Step 3/3: boot local environment"
# shellcheck disable=SC2086
"$ROOT_DIR/scripts/boot_local.sh" $BOOT_ARGS

echo
echo "[jarvis] First run complete"
echo "Open VS Code with:"
echo "  code \"$ROOT_DIR\""
