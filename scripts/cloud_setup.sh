#!/bin/bash
# Cloud-only environment setup for "Claude Code on the web" (cloud sessions).
#
# Runs at SessionStart via .claude/settings.json. A fresh cloud VM starts from a
# bare clone with no .venv, so this rebuilds the same .venv the project scripts
# expect (all of them invoke `.venv/bin/python ...`). On your laptop the .venv
# already exists, so this script exits immediately and never touches local work.
#
# It is intentionally best-effort: it always exits 0 so a transient install
# failure never blocks the session from starting. If deps are missing, just ask
# Claude to re-run `.venv/bin/pip install -r requirements.txt` mid-session.

# Only do anything inside a cloud session (set to "true" there, unset locally).
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || exit 0

# Build the .venv the project convention relies on, if it isn't there yet.
if [ ! -x .venv/bin/python ]; then
  python3 -m venv .venv || exit 0
fi

# Skip the install if numpy (the core dep) already imports — keeps resumes fast.
if .venv/bin/python -c "import numpy" 2>/dev/null; then
  exit 0
fi

.venv/bin/pip install --quiet --upgrade pip
.venv/bin/pip install --quiet -r requirements.txt

exit 0
