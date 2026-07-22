#!/usr/bin/env bash
# Live progress bar for a running stage1_5_sweep.py.
#   ./sweep_progress.sh [logfile] [--once]
# Defaults to the currently-running v2 sweep log. Redraws every 2s until
# the sweep prints its completion line; --once prints one snapshot.

LOG="${1:-/tmp/claude-1001/-home-andy-projects-Unsolved/aa5b8b95-03ed-43bd-96ab-3dfe586f1fde/scratchpad/sweep_v2.log}"
TOTAL=80
WIDTH=36

snapshot() {
    local done pct filled bar eta avg last
    done=$(grep -c '^\[' "$LOG" 2>/dev/null)
    done=${done:-0}
    pct=$((done * 100 / TOTAL))
    filled=$((done * WIDTH / TOTAL))
    bar=$(printf '%*s' "$filled" '' | tr ' ' '#')$(printf '%*s' $((WIDTH - filled)) '' | tr ' ' '-')
    # ETA from the per-bisection durations "(7.7s)" in each progress line
    eta=$(grep '^\[' "$LOG" 2>/dev/null | awk -v total="$TOTAL" '
        match($0, /\(([0-9.]+)s\)$/, m) { sum += m[1]; n++ }
        END { if (n > 0) printf "%d", (total - n) * (sum / n) / 60 }')
    last=$(grep '^\[' "$LOG" 2>/dev/null | tail -1 | sed 's/^\[ *[0-9]*\/[0-9]*\] *//')
    printf '\r\033[K[%s] %2d/%d (%d%%)' "$bar" "$done" "$TOTAL" "$pct"
    [ -n "$eta" ] && [ "$done" -lt "$TOTAL" ] && printf ' ~%sm left' "$eta"
    [ -n "$last" ] && printf ' | %s' "$last"
}

if [ "$2" = "--once" ] || [ "$1" = "--once" ]; then
    [ "$1" = "--once" ] && LOG="/tmp/claude-1001/-home-andy-projects-Unsolved/aa5b8b95-03ed-43bd-96ab-3dfe586f1fde/scratchpad/sweep_v2.log"
    snapshot; echo
    exit 0
fi

while true; do
    snapshot
    if grep -q "Sweep complete" "$LOG" 2>/dev/null; then
        echo; echo "Sweep complete."
        break
    fi
    sleep 2
done
