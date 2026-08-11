#!/usr/bin/env bash
# End-to-end test for the Headroom MCP compression server (see docs/HEADROOM.md).
# Drives the real MCP stdio server like Claude Code does and asserts compression +
# retrieval work. Run from anywhere:  ./headroom-test.sh
set -uo pipefail

PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$PROJ/.headroom-venv/bin/python"

if [[ ! -x "$PY" ]]; then
  echo "Headroom venv not found at $PROJ/.headroom-venv" >&2
  echo "Reinstall with: python3 -m venv .headroom-venv && \\" >&2
  echo "  ./.headroom-venv/bin/pip install 'headroom-ai[mcp,proxy]'" >&2
  exit 1
fi

echo "Headroom compression test"
exec "$PY" "$PROJ/tools/headroom_compression_test.py"
