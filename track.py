"""Track live progress of a running Phase-1 experiment (a JSONL append log).

The solver sweeps (phase1_*.py) append one JSON row per completed solve to an
experiments/*.jsonl file and flush immediately, so progress is observable while a
run is in flight. This CLI summarizes that append log: how many solves are done,
the per-resolution breakdown, throughput, an approximate ETA, and the most recent
completed shapes with their key metrics (g_frac, t_res, outcome).

It is read-only and makes no assumptions beyond the common row fields written by
ga.logbook + the phase1 runners: `resolution_N`, `label`, `timestamp`, and
(when present) `g_frac` / `t_res` / `outcome`. Rows missing a field degrade
gracefully. Whether the producing process is still alive is detected by matching
`--proc` against the process table (default: the rankcheck script).

Usage:
  .venv/bin/python track.py                       # default: rankcheck log, one shot
  .venv/bin/python track.py --expected 40         # add a progress bar + ETA
  .venv/bin/python track.py FILE.jsonl --watch    # live refresh until the run ends
  .venv/bin/python track.py --watch --expected 40 --interval 10
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

DEFAULT_LOG = "experiments/phase1_gsustained_rankcheck.jsonl"
DEFAULT_PROC = "phase1_gsustained_rankcheck.py"


def _read_rows(path):
    rows = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass  # a half-written trailing line during a live flush
    except FileNotFoundError:
        pass
    return rows


def _parse_ts(row):
    ts = row.get("timestamp")
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def _fmt_dur(sec):
    if sec is None or sec != sec:
        return "--"
    sec = int(sec)
    if sec < 60:
        return f"{sec}s"
    if sec < 3600:
        return f"{sec // 60}m{sec % 60:02d}s"
    return f"{sec // 3600}h{(sec % 3600) // 60:02d}m"


def _proc_alive(needle):
    if not needle:
        return None
    try:
        out = subprocess.run(["pgrep", "-f", needle], capture_output=True, text=True)
        return out.returncode == 0 and bool(out.stdout.strip())
    except FileNotFoundError:
        return None


def _bar(frac, width=28):
    frac = max(0.0, min(1.0, frac))
    fill = int(round(frac * width))
    return "[" + "#" * fill + "-" * (width - fill) + f"] {frac * 100:5.1f}%"


def render(path, expected, proc):
    rows = _read_rows(path)
    lines = []
    now = datetime.now(timezone.utc)
    lines.append(f"experiment: {path}")

    alive = _proc_alive(proc)
    status = "RUNNING" if alive else ("done/stopped" if alive is False else "unknown")
    lines.append(f"producer  : {proc}  [{status}]")

    n = len(rows)
    if n == 0:
        lines.append("")
        lines.append("no solves completed yet (first N=512 solve can take a few minutes)")
        return "\n".join(lines)

    # timing from completion timestamps
    tss = sorted(t for t in (_parse_ts(r) for r in rows) if t is not None)
    elapsed = (now - tss[0]).total_seconds() if tss else None
    # mean seconds/solve from consecutive completions (robust to the slow first solve)
    per = None
    if len(tss) >= 2:
        deltas = [(tss[i + 1] - tss[i]).total_seconds() for i in range(len(tss) - 1)]
        per = sum(deltas) / len(deltas)

    # progress line
    if expected:
        eta = (expected - n) * per if (per and n < expected) else (0 if n >= expected else None)
        lines.append("")
        lines.append(f"progress  : {n}/{expected}  {_bar(n / expected)}")
        lines.append(f"throughput: {_fmt_dur(per)}/solve (mean gap)   "
                     f"elapsed {_fmt_dur(elapsed)}   ETA {_fmt_dur(eta)}")
    else:
        lines.append("")
        lines.append(f"progress  : {n} solves done   {_fmt_dur(per)}/solve   "
                     f"elapsed {_fmt_dur(elapsed)}")

    # per-resolution breakdown
    by_n = {}
    for r in rows:
        by_n.setdefault(r.get("resolution_N", "?"), []).append(r)
    lines.append("")
    lines.append("by resolution:")
    for nn in sorted(by_n, key=lambda x: (isinstance(x, str), x)):
        grp = by_n[nn]
        growers = sum(1 for r in grp if isinstance(r.get("t_res"), (int, float))
                      and r["t_res"] < 4.0 - 1e-6)
        lines.append(f"  N={nn:<5} {len(grp):3d} solves   {growers} growers (t_res<T_MAX)")

    # last few completed
    recent = rows[-6:]
    lines.append("")
    lines.append("recent completions:")
    for r in recent:
        g = r.get("g_frac")
        gtxt = f"{g:+.3f}" if isinstance(g, (int, float)) and g == g else "  nan"
        tr = r.get("t_res")
        trtxt = f"{tr:.2f}" if isinstance(tr, (int, float)) else "  ? "
        lines.append(f"  {str(r.get('label', '?')):16s} N={str(r.get('resolution_N', '?')):<5}"
                     f" g_frac={gtxt}  t_res={trtxt}  {r.get('outcome', '')}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log", nargs="?", default=DEFAULT_LOG, help="experiment JSONL path")
    ap.add_argument("--expected", type=int, default=None,
                    help="total solves expected (enables a progress bar + ETA)")
    ap.add_argument("--proc", default=DEFAULT_PROC,
                    help="process-name substring to check liveness (pgrep -f)")
    ap.add_argument("--watch", action="store_true", help="refresh until the producer exits")
    ap.add_argument("--interval", type=float, default=10.0, help="--watch refresh seconds")
    args = ap.parse_args()

    if not args.watch:
        print(render(args.log, args.expected, args.proc))
        return

    try:
        while True:
            frame = render(args.log, args.expected, args.proc)
            sys.stdout.write("\x1b[2J\x1b[H")  # clear screen, home cursor
            sys.stdout.write(frame + "\n")
            sys.stdout.write(f"\n(watching every {args.interval:g}s; Ctrl-C to stop)\n")
            sys.stdout.flush()
            if _proc_alive(args.proc) is False:
                sys.stdout.write("\nproducer has exited — final snapshot above.\n")
                sys.stdout.flush()
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nstopped watching.")


if __name__ == "__main__":
    main()
