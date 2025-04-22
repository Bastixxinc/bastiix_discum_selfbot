#!/usr/bin/env bash
# ----------------------------------------
# Restart-Skript für Unix/Linux/macOS: startet main.py im DEBUG-Modus
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
exec python3 "$MAIN_PY" DEBUG
