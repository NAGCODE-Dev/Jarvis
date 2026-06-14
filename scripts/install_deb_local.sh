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

PACKAGE=$(ls -1t "$ROOT_DIR"/dist/jarvis-local_*.deb | head -n 1)

echo "[jarvis-deb] Pacote selecionado: $PACKAGE"

install_package() {
  if command -v sudo >/dev/null 2>&1; then
    sudo dpkg -i "$PACKAGE"
    return $?
  fi

  if command -v pkexec >/dev/null 2>&1; then
    pkexec dpkg -i "$PACKAGE"
    return $?
  fi

  echo "[jarvis-deb] sudo/pkexec não disponível. Instale manualmente com:"
  echo "  dpkg -i '$PACKAGE'"
  return 1
}

install_package

echo
echo "[jarvis-deb] Instalação concluída. Próximos passos recomendados:"
echo "  1. /opt/jarvis-local/app/scripts/jarvis.sh setup-local --dry-run"
echo "  2. /opt/jarvis-local/app/scripts/jarvis.sh setup-local"
echo "  3. /opt/jarvis-local/app/scripts/jarvis.sh doctor"
echo "  4. jarvis-local"
