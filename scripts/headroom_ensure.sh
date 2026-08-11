#!/usr/bin/env bash
# Ensure the local Headroom compression proxy is up before Claude Code talks to it.
#
# Wired in as a SessionStart hook (see .claude/settings.local.json). Because that
# same file pins ANTHROPIC_BASE_URL at the proxy, a dead proxy means no API access
# at all for this project — so this script has to be both fast and reliable.
#
# The proxy itself is shared machine-wide (one localhost forwarder serves every
# project), managed by the headroom-proxy.service user unit.
#
# Emits hook JSON on stdout only when it had to do something, so a healthy session
# starts silently. Never exits non-zero: a hook failure must not block the session.
set -uo pipefail

PORT="${HEADROOM_PORT:-8787}"
UNIT="headroom-proxy.service"
BIN="/home/andy/projects/Unsolved/.headroom-venv/bin/headroom"
LIVEZ="http://127.0.0.1:${PORT}/livez"

alive() { curl -sf --max-time 1 -o /dev/null "$LIVEZ"; }

emit() { printf '{"systemMessage":"%s"}\n' "$1"; }

alive && exit 0

# Prefer the managed unit; fall back to a detached process if systemd --user is unavailable.
if systemctl --user list-unit-files "$UNIT" >/dev/null 2>&1 \
   && systemctl --user cat "$UNIT" >/dev/null 2>&1; then
  systemctl --user start "$UNIT" >/dev/null 2>&1
elif [ -x "$BIN" ]; then
  nohup "$BIN" proxy --host 127.0.0.1 --port "$PORT" --mode cache \
    >"${TMPDIR:-/tmp}/headroom-proxy.log" 2>&1 &
  disown 2>/dev/null || true
else
  emit "Headroom: proxy binary missing at ${BIN} — ANTHROPIC_BASE_URL points at a dead port. Run: python3 -m venv .headroom-venv && ./.headroom-venv/bin/pip install 'headroom-ai[mcp,proxy]'"
  exit 0
fi

# Startup is ~3-5s cold. Poll rather than sleeping a fixed worst case.
for _ in $(seq 1 30); do
  alive && { emit "Headroom proxy started on port ${PORT}."; exit 0; }
  sleep 0.5
done

emit "Headroom proxy did NOT come up on port ${PORT} within 15s. Claude Code is routed through it, so requests will fail. Unset ANTHROPIC_BASE_URL in .claude/settings.local.json to bypass, or check: systemctl --user status ${UNIT}"
exit 0
