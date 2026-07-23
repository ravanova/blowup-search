"""Live progress bar for phase1_axis_screen.py.

Reads the screen's JSONL as it is written and renders a progress bar + a
per-(IC, N) grid of the three candidate axes. Snapshot by default; --watch for a
live bar that refreshes until all bisections complete.

Usage:
    .venv/bin/python phase1_axis_progress.py            # one snapshot
    .venv/bin/python phase1_axis_progress.py --watch    # live until complete
"""

import argparse
import json
import os
import time

from phase1_axis_screen import RESOLUTIONS, build_ics

IN = "experiments/phase1_axis_screen.jsonl"
_ICS = [ic["label"] for ic in build_ics()]
_TOTAL = len(_ICS) * len(RESOLUTIONS)


def load_rows():
    rows = []
    if os.path.exists(IN):
        with open(IN) as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def bar(done, total, width=40):
    filled = int(width * done / total) if total else 0
    return "[" + "#" * filled + "-" * (width - filled) + f"] {done}/{total}"


def _fmt(v, w=8):
    return " " * (w - 3) + "--" if v is None else f"{v:{w}.4f}"


def render(rows):
    latest = {(r["ic_label"], r["resolution_N"]): r for r in rows}
    done = len(latest)
    lines = [bar(done, _TOTAL), ""]
    hdr = f"  {'IC':14s} {'N':>4s} {'nu_crit':>10s} {'persist':>10s} {'g_base':>9s} {'amp':>7s} {'runs':>5s} {'sec':>6s}"
    lines.append(hdr)
    lines.append("  " + "-" * (len(hdr) - 2))
    for ic in _ICS:
        for N in RESOLUTIONS:
            r = latest.get((ic, N))
            if r is None:
                lines.append(f"  {ic:14s} {N:4d} {'pending':>10s}")
                continue
            cens = f" ({r['nu_crit_censored']})" if r["nu_crit_censored"] else ""
            lines.append(
                f"  {ic:14s} {N:4d} {r['nu_crit']:10.4f}{cens:<5s}"
                f"{_fmt(r['persistence'], 10)} {_fmt(r['g_baseline'], 9)}"
                f" {r['nu0_amp_resolved']:7.1f} {r['n_bisection_runs']:5d}"
                f" {r['wall_clock_seconds']:6.0f}")
    return "\n".join(lines), done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=float, default=5.0)
    args = ap.parse_args()

    if not args.watch:
        text, _ = render(load_rows())
        print(text)
        return
    try:
        while True:
            text, done = render(load_rows())
            print("\033[2J\033[H" + text, flush=True)
            if done >= _TOTAL:
                print("\nAll bisections complete.")
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
