#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"
BUILD_DIR=$(mktemp -d)
PKG_ROOT="$BUILD_DIR/pkg"
APP_ROOT="$PKG_ROOT/opt/jarvis-local/app"
BIN_ROOT="$PKG_ROOT/usr/bin"
DESKTOP_ROOT="$PKG_ROOT/usr/share/applications"
VERSION=$(awk -F'"' '$1 ~ /^version = / { print $2; exit }' "$ROOT_DIR/pyproject.toml")
ARCH=$(dpkg --print-architecture 2>/dev/null || uname -m)
PACKAGE_NAME="jarvis-local"
OUTPUT_PATH="$DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

cleanup() {
  rm -rf "$BUILD_DIR"
}
trap cleanup EXIT INT TERM

mkdir -p "$DIST_DIR" "$APP_ROOT" "$BIN_ROOT" "$DESKTOP_ROOT"

copy_project() {
  tar     --exclude='./.git'     --exclude='./dist'     --exclude='./logs'     --exclude='./.pytest_cache'     --exclude='./__pycache__'     --exclude='./data/sessions/*.json'     -cf - . | (cd "$APP_ROOT" && tar -xf -)
}

write_control() {
  mkdir -p "$BUILD_DIR/control"
  cat > "$BUILD_DIR/control/control" <<EOF
Package: $PACKAGE_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: Jarvis Local
Depends: bash, curl
Description: Jarvis Local Codex-like app shell with local FastAPI, PWA and Linux launcher.
 Instala o Jarvis em /opt/jarvis-local/app e expõe o launcher jarvis-local.
EOF
}

write_launcher() {
  cat > "$BIN_ROOT/jarvis-local" <<'EOF'
#!/usr/bin/env sh
set -eu
exec /opt/jarvis-local/app/scripts/jarvis.sh app "$@"
EOF
  chmod 755 "$BIN_ROOT/jarvis-local"
}

write_desktop() {
  cat > "$DESKTOP_ROOT/jarvis-local.desktop" <<'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Jarvis Local
Comment=Assistente local Jarvis em modo aplicativo Linux
Exec=/usr/bin/jarvis-local
Icon=/opt/jarvis-local/app/apps/web/icon.svg
Terminal=false
Categories=Development;Utility;
StartupNotify=true
StartupWMClass=Jarvis Local
EOF
}

normalize_tree() {
  find "$PKG_ROOT" -type d -exec chmod 755 {} \;
  find "$PKG_ROOT" -type f -exec chmod 644 {} \;
  chmod 755 "$APP_ROOT/scripts"/*.sh "$BIN_ROOT/jarvis-local"
}

build_with_dpkg_deb() {
  dpkg-deb --build "$PKG_ROOT" "$OUTPUT_PATH" >/dev/null
}

build_with_ar() {
  printf '2.0\n' > "$BUILD_DIR/debian-binary"
  tar -C "$BUILD_DIR/control" --owner=0 --group=0 -czf "$BUILD_DIR/control.tar.gz" .
  tar -C "$PKG_ROOT" --owner=0 --group=0 -czf "$BUILD_DIR/data.tar.gz" .
  rm -f "$OUTPUT_PATH"
  ar r "$OUTPUT_PATH" "$BUILD_DIR/debian-binary" "$BUILD_DIR/control.tar.gz" "$BUILD_DIR/data.tar.gz" >/dev/null 2>&1
}

copy_project
write_control
write_launcher
write_desktop
normalize_tree

if command -v dpkg-deb >/dev/null 2>&1; then
  build_with_dpkg_deb
elif command -v ar >/dev/null 2>&1; then
  build_with_ar
else
  echo '[jarvis-deb] Nem dpkg-deb nem ar estão disponíveis para empacotar.' >&2
  exit 1
fi

echo "[jarvis-deb] Pacote gerado: $OUTPUT_PATH"
