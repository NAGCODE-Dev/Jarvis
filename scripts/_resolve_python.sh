#!/usr/bin/env sh
set -eu

ROOT_DIR="$1"
shift || true

eval "$($ROOT_DIR/scripts/_runtime_env.sh "$ROOT_DIR")"
VENV_PYTHON="$JARVIS_VENV_DIR/bin/python"

check_python() {
  python_bin="$1"
  shift || true
  [ -x "$python_bin" ] || command -v "$python_bin" >/dev/null 2>&1 || return 1
  for module in "$@"; do
    if ! "$python_bin" -c "import $module" >/dev/null 2>&1; then
      return 1
    fi
  done
  return 0
}

if [ -x "$VENV_PYTHON" ] && check_python "$VENV_PYTHON" "$@"; then
  printf '%s
' "$VENV_PYTHON"
  exit 0
fi

if check_python "python3" "$@"; then
  printf '%s
' "python3"
  exit 0
fi

echo "[jarvis] No suitable Python interpreter found for modules: $*" >&2
exit 1
