#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP_DIR=$(mktemp -d)
FAKE_HOME="$TMP_DIR/home"
FAKE_BIN="$TMP_DIR/bin"
FAKE_LOG="$TMP_DIR/browser.log"
APPLICATIONS_DIR="$FAKE_HOME/.local/share/applications"
DESKTOP_FILE="$APPLICATIONS_DIR/jarvis-local.desktop"
LAUNCHER_LINK="$FAKE_HOME/.local/bin/jarvis-local"
HOST="${JARVIS_HOST:-127.0.0.1}"
PORT="${JARVIS_PORT:-8000}"
APP_URL="http://${HOST}:${PORT}/app/"

mkdir -p "$FAKE_HOME" "$FAKE_BIN"

cat > "$FAKE_BIN/google-chrome" <<EOF
#!/usr/bin/env sh
echo "\$@" >> "$FAKE_LOG"
exit 0
EOF
chmod +x "$FAKE_BIN/google-chrome"

HOME="$FAKE_HOME" XDG_DATA_HOME="$FAKE_HOME/.local/share" PATH="$FAKE_BIN:$PATH"   "$ROOT_DIR/scripts/install_linux_app.sh" >/dev/null

if [ ! -f "$DESKTOP_FILE" ]; then
  echo "[jarvis-linux] desktop file not installed"
  exit 1
fi

if [ ! -L "$LAUNCHER_LINK" ]; then
  echo "[jarvis-linux] launcher symlink not installed"
  exit 1
fi

HOME="$FAKE_HOME" XDG_DATA_HOME="$FAKE_HOME/.local/share" PATH="$FAKE_BIN:$PATH"   JARVIS_HOST="$HOST" JARVIS_PORT="$PORT" JARVIS_BOOT_ARGS="--no-seed"   "$ROOT_DIR/scripts/run_linux_app.sh"

attempt=0
while [ ! -f "$FAKE_LOG" ] && [ "$attempt" -lt 20 ]; do
  attempt=$((attempt + 1))
  sleep 0.1
done

if [ ! -f "$FAKE_LOG" ]; then
  echo "[jarvis-linux] browser launcher was not called"
  exit 1
fi

if ! grep -F -- "--app=$APP_URL" "$FAKE_LOG" >/dev/null 2>&1; then
  echo "[jarvis-linux] browser did not receive app url"
  cat "$FAKE_LOG"
  exit 1
fi

if ! grep -F -- "$ROOT_DIR/scripts/run_linux_app.sh" "$DESKTOP_FILE" >/dev/null 2>&1; then
  echo "[jarvis-linux] desktop file missing expanded launcher path"
  exit 1
fi

echo "[jarvis-linux] Linux app smoke passed"
echo "[jarvis-linux] desktop: $DESKTOP_FILE"
