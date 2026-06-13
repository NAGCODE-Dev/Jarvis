#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DESKTOP_TEMPLATE="$ROOT_DIR/apps/linux/jarvis-local.desktop.in"
APPLICATIONS_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
BIN_DIR="$HOME/.local/bin"
DESKTOP_FILE="$APPLICATIONS_DIR/jarvis-local.desktop"
LAUNCHER_LINK="$BIN_DIR/jarvis-local"

mkdir -p "$APPLICATIONS_DIR" "$BIN_DIR"

sed "s#__ROOT_DIR__#$ROOT_DIR#g" "$DESKTOP_TEMPLATE" > "$DESKTOP_FILE"
chmod 755 "$ROOT_DIR/scripts/run_linux_app.sh"
ln -sf "$ROOT_DIR/scripts/run_linux_app.sh" "$LAUNCHER_LINK"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPLICATIONS_DIR" >/dev/null 2>&1 || true
fi

cat <<EOF
[jarvis-linux] Aplicação Linux instalada.
Desktop entry: $DESKTOP_FILE
Launcher: $LAUNCHER_LINK
Abra pelo menu do sistema procurando por: Jarvis Local
Ou execute no terminal: jarvis-local
EOF
