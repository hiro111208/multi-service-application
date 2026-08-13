#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "=== API unit & integration tests ==="
PYTHON="${ROOT_DIR}/api/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  python3 -m venv "${ROOT_DIR}/api/.venv"
  "$PYTHON" -m pip install -q -r "${ROOT_DIR}/api/requirements-dev.txt"
fi
"$PYTHON" -m pytest "${ROOT_DIR}/api/tests" -q

echo
echo "=== Web unit tests ==="
npm --prefix web ci --silent
npm --prefix web run test

echo
echo "=== All automated tests passed ==="
