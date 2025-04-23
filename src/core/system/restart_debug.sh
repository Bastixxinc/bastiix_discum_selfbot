#!/usr/bin/env bash
# ----------------------------------------
# \src/core/system/restart_debug.sh
# \author @bastiix
# ----------------------------------------

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v realpath >/dev/null 2>&1; then
  MAIN_PY="$(realpath "$SCRIPT_DIR/../../../main.py")"
elif command -v readlink >/dev/null 2>&1; then
  MAIN_PY="$(readlink -f "$SCRIPT_DIR/../../../main.py")"
else
  MAIN_PY="$SCRIPT_DIR/../../../main.py"
fi
PROJECT_DIR="$(dirname "$(dirname "$(dirname "$SCRIPT_DIR")")")"
VENV_ACT="$PROJECT_DIR/venv/bin/activate"
if [ -f "$VENV_ACT" ]; then
  source "$VENV_ACT"
  PY_CMD=python
else
  if command -v python3 >/dev/null 2>&1; then
    PY_CMD=python3
  elif command -v py >/dev/null 2>&1; then
    PY_CMD=py
  else
    PY_CMD=python
  fi
fi

if ! "$PY_CMD" "$MAIN_PY" DEBUG; then
  echo "ERROR: Failed to restart the script in debug mode." >&2
  exit 1
fi

exit 0
