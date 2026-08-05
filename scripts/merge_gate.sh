#!/bin/bash
# Executable merge criterion for hands-off integration to main.
#
# The orchestration flow (ORCHESTRATION.md) merges a branch/PR without human
# review IFF this script prints "MERGE GATE: PASS" and exits 0 on the candidate
# branch. It is deliberately targeted, not exhaustive: the always-on tests are
# the drift detector (plan_of_record <-> CONTINUATION_PROMPT <-> CLAY_ROADMAP
# agreement) and the capability index; beyond that it runs only the tests that
# the diff against the base ref actually touches. The full suite is the
# reproducibility agent's job, not a per-merge cost.
#
# Usage:
#   scripts/merge_gate.sh              # gate HEAD against origin/main
#   scripts/merge_gate.sh main         # gate HEAD against local main
#
# Test convention in this repo: every test_*.py is a self-running script
# (`.venv/bin/python test_x.py`, no pytest). A solver/<name>.py change maps to
# test_<name>.py at the repo root when that file exists.

set -u
cd "$(dirname "$0")/.." || exit 1

BASE="${1:-origin/main}"
git rev-parse --verify --quiet "$BASE" >/dev/null || BASE="main"

PY=.venv/bin/python
[ -x "$PY" ] || PY=python3

fail=0
run_test() {
  echo "== $1"
  if ! "$PY" "$1" >/dev/null 2>&1; then
    echo "   FAIL: $1 (re-run without redirection for detail)"
    fail=1
  fi
}

# Always-on: the machine-readable plan must stay coherent, whatever the diff.
run_test test_plan_of_record.py
run_test test_capabilities.py

# Targeted: tests implied by the diff against base.
changed=$(git diff --name-only "$BASE"...HEAD 2>/dev/null)
tests=""
for f in $changed; do
  case "$f" in
    test_*.py)
      [ -f "$f" ] && tests="$tests $f" ;;
    solver/*.py)
      t="test_$(basename "$f")"
      [ -f "$t" ] && tests="$tests $t" ;;
    ga/*.py)
      [ -f test_ga.py ] && tests="$tests test_ga.py" ;;
    win_condition.py)
      tests="$tests test_win_condition.py" ;;
    plan_of_record.py|CONTINUATION_PROMPT.md|CLAY_ROADMAP.md)
      : ;; # already covered by the always-on drift detector
  esac
done

for t in $(echo "$tests" | tr ' ' '\n' | sort -u); do
  case "$t" in
    test_plan_of_record.py|test_capabilities.py) : ;; # already run
    *) run_test "$t" ;;
  esac
done

# Claim-bearing diffs must carry their evidence: a new BLOG_*.md in the
# writeup tree without a TECHNICAL_*.md sibling (or vice versa) is a docs
# contract violation, not a merge candidate.
for f in $changed; do
  case "$f" in
    writeup/*/BLOG_*.md)
      sib="$(dirname "$f")/TECHNICAL_${f##*/BLOG_}"
      if git diff --name-only "$BASE"...HEAD | grep -q "^$sib\$" || [ -f "$sib" ]; then :; else
        echo "   FAIL: $f has no TECHNICAL_ sibling (docs contract, ORCHESTRATION.md)"
        fail=1
      fi ;;
  esac
done

if [ "$fail" -ne 0 ]; then
  echo "MERGE GATE: FAIL"
  exit 1
fi
echo "MERGE GATE: PASS"
exit 0
