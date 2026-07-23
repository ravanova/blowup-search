"""Live progress bar for phase1_resolution_spike.py.

Reads the sweep's JSONL as it is written and renders a progress bar + a
per-(IC, resolution) status grid. Snapshot by default; --watch for a live bar
that refreshes until the sweep completes.

Usage:
    .venv/bin/python phase1_progress.py            # one snapshot
    .venv/bin/python phase1_progress.py --watch    # live until complete
"""

import argparse
import json
import os
import time
from datetime import datetime

from phase1_resolution_spike import RESOLUTIONS, build_ics

IN = "experiments/phase1_resolution_spike.jsonl"
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


_MARK = {"blowup_candidate": "B", "under_resolved": "u", "no_blowup": ".",
         "diverged": "!", "max_steps_hit": "m"}


def _sweep_start(rows):
    """Real sweep start = earliest row timestamp (fallback: JSONL mtime)."""
    stamps = []
    for r in rows:
        try:
            stamps.append(datetime.fromisoformat(r["timestamp"]).timestamp())
        except (KeyError, ValueError):
            pass
    if stamps:
        return min(stamps)
    return os.path.getmtime(IN) if os.path.exists(IN) else time.time()


def render(rows, _unused=None):
    latest = {(r["ic_label"], r["resolution_N"]): r for r in rows}
    done = len(latest)
    lines = []
    lines.append(bar(done, _TOTAL))
    elapsed = time.time() - _sweep_start(rows) if rows else 0.0
    if done and done < _TOTAL:
        eta = elapsed * (_TOTAL - done) / done
        lines.append(f"  elapsed {elapsed:5.0f}s   ~eta {eta:5.0f}s "
                     f"(wall-clock est.; long-tail N=1024 runs dominate)")
    header = "  " + "".join(f"{('N=' + str(n)):>9}" for n in RESOLUTIONS)
    lines.append("")
    lines.append(f"{'IC':<14}{header}   key: B=blowup u=under-resolved .=no-blowup")
    for ic in _ICS:
        cells = []
        for n in RESOLUTIONS:
            r = latest.get((ic, n))
            if r is None:
                cells.append(f"{'·':>9}")
            else:
                g = r["growth_rate_fixed_window"]
                gtxt = "nan" if g != g else f"{g:.2f}"
                cells.append(f"{_MARK.get(r['outcome'], '?')}{gtxt:>8}")
        lines.append(f"{ic:<14}  " + "".join(cells))
    lines.append("")
    lines.append("  cell = <outcome><fixed-window growth-rate g>; g convergence "
                 "across a row is the resolution-stability signal.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--interval", type=float, default=3.0)
    args = ap.parse_args()

    t0 = time.time()
    if not args.watch:
        print(render(load_rows(), t0))
        return
    try:
        while True:
            rows = load_rows()
            os.system("clear")
            print(render(rows, t0))
            if len(rows) >= _TOTAL:
                print("\nspike complete.")
                return
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n(stopped watching; sweep continues in the background)")


if __name__ == "__main__":
    main()
