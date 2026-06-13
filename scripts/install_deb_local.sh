#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REBUILD=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --rebuild)
      REBUILD=1
      ;;
    *)
      echo "[jarvis-deb] Uso: scripts/install_deb_local.sh [--rebuild]"
      exit 1
      ;;
  esac
  shift
done

if [ "$REBUILD" -eq 1 ] || ! ls "$ROOT_DIR"/dist/jarvis-local_*.deb >/dev/null 2>&1; then
  "$ROOT_DIR/scripts/build_deb.sh"
fi

PACKAGE=$(ls -1 "$ROOT_DIR"/dist/jarvis-local_*.deb | tail -n 1)

echo "[jarvis-deb] Pacote selecionado: $PACKAGE"

if command -v sudo >/dev/null 2>&1; then
  exec sudo dpkg -i "$PACKAGE"
fi

if command -v pkexec >/dev/null 2>&1; then
  exec pkexec dpkg -i "$PACKAGE"
fi

echo "[jarvis-deb] sudo/pkexec não disponível. Instale manualmente com:"
echo "  dpkg -i '$PACKAGE'"
exit 1
