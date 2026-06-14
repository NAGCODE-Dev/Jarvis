#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST_DIR="$ROOT_DIR/dist"
TEMPLATE_DIR="$ROOT_DIR/packaging/debian"
BUILD_DIR=$(mktemp -d)
PKG_ROOT="$BUILD_DIR/pkg"
CONTROL_ROOT="$PKG_ROOT/DEBIAN"
APP_ROOT="$PKG_ROOT/opt/jarvis-local/app"
BIN_ROOT="$PKG_ROOT/usr/bin"
DESKTOP_ROOT="$PKG_ROOT/usr/share/applications"
VERSION=$(awk -F'"' '$1 ~ /^version = / { print $2; exit }' "$ROOT_DIR/pyproject.toml")
PACKAGE_NAME="jarvis-local"

map_arch() {
  raw_arch="$1"
  case "$raw_arch" in
    x86_64|amd64)
      printf 'amd64
'
      ;;
    aarch64|arm64)
      printf 'arm64
'
      ;;
    armv7l|armhf)
      printf 'armhf
'
      ;;
    i386|i686)
      printf 'i386
'
      ;;
    *)
      printf '%s
' "$raw_arch"
      ;;
  esac
}

if command -v dpkg >/dev/null 2>&1; then
  ARCH=$(dpkg --print-architecture)
else
  ARCH=$(map_arch "$(uname -m)")
fi
OUTPUT_PATH="$DIST_DIR/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

cleanup() {
  rm -rf "$BUILD_DIR"
}
trap cleanup EXIT INT TERM

mkdir -p "$DIST_DIR" "$CONTROL_ROOT" "$APP_ROOT" "$BIN_ROOT" "$DESKTOP_ROOT"

copy_project() {
  tar     --exclude='./.git'     --exclude='./.venv'     --exclude='./dist'     --exclude='./logs'     --exclude='./.pytest_cache'     --exclude='./.mypy_cache'     --exclude='./node_modules'     --exclude='./.agents'     --exclude='./.codex'     --exclude='*/__pycache__'     --exclude='*.pyc'     --exclude='./data/sessions/*.json'     --exclude='./data/memory/current_context.json'     --exclude='./data/memory/vectors/*.json'     -cf - . | (cd "$APP_ROOT" && tar -xf -)
}

render_template() {
  src="$1"
  dest="$2"
  sed     -e "s#@PACKAGE_NAME@#$PACKAGE_NAME#g"     -e "s#@VERSION@#$VERSION#g"     -e "s#@ARCH@#$ARCH#g"     "$src" > "$dest"
}

write_control() {
  render_template "$TEMPLATE_DIR/control.in" "$CONTROL_ROOT/control"
}

write_maintainer_scripts() {
  cp "$TEMPLATE_DIR/postinst" "$CONTROL_ROOT/postinst"
  cp "$TEMPLATE_DIR/prerm" "$CONTROL_ROOT/prerm"
  chmod 755 "$CONTROL_ROOT/postinst" "$CONTROL_ROOT/prerm"
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
  cp "$TEMPLATE_DIR/jarvis-local.desktop.in" "$DESKTOP_ROOT/jarvis-local.desktop"
}

normalize_tree() {
  find "$PKG_ROOT" -type d -exec chmod 755 {} \;
  find "$PKG_ROOT" -type f -exec chmod 644 {} \;
  chmod 755 "$APP_ROOT/scripts"/*.sh "$BIN_ROOT/jarvis-local" "$CONTROL_ROOT/postinst" "$CONTROL_ROOT/prerm"
}

build_with_dpkg_deb() {
  dpkg-deb --build "$PKG_ROOT" "$OUTPUT_PATH" >/dev/null
}

build_with_ar() {
  printf '2.0
' > "$BUILD_DIR/debian-binary"
  tar -C "$CONTROL_ROOT" --owner=0 --group=0 -czf "$BUILD_DIR/control.tar.gz" .
  tar -C "$PKG_ROOT" --exclude='./DEBIAN' --owner=0 --group=0 -czf "$BUILD_DIR/data.tar.gz" .
  rm -f "$OUTPUT_PATH"
  ar r "$OUTPUT_PATH" "$BUILD_DIR/debian-binary" "$BUILD_DIR/control.tar.gz" "$BUILD_DIR/data.tar.gz" >/dev/null 2>&1
}

copy_project
write_control
write_maintainer_scripts
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
