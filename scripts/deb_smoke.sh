#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
"$ROOT_DIR/scripts/build_deb.sh" >/dev/null
PACKAGE=$(ls -1 "$ROOT_DIR"/dist/jarvis-local_*.deb | tail -n 1)
TMP_DIR=$(mktemp -d)
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT INT TERM

cd "$TMP_DIR"
ar x "$PACKAGE"

test -f debian-binary
test -f control.tar.gz || test -f control.tar.xz || test -f control.tar.zst
test -f data.tar.gz || test -f data.tar.xz || test -f data.tar.zst

DATA_ARCHIVE=$(ls data.tar.* | head -n 1)
CONTROL_ARCHIVE=$(ls control.tar.* | head -n 1)

tar -tf "$DATA_ARCHIVE" | grep -F './usr/bin/jarvis-local' >/dev/null
tar -tf "$DATA_ARCHIVE" | grep -F './usr/share/applications/jarvis-local.desktop' >/dev/null
tar -tf "$DATA_ARCHIVE" | grep -F './opt/jarvis-local/app/scripts/run_linux_app.sh' >/dev/null
tar -tf "$CONTROL_ARCHIVE" | grep -F './control' >/dev/null

echo "[jarvis-deb] smoke ok: $PACKAGE"
