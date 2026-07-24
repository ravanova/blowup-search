"""Track live progress of a running Phase-1 experiment (a JSONL append log).

The solver sweeps (phase1_*.py) append one JSON row per completed solve to an
experiments/*.jsonl file and flush immediately, so progress is observable while a
run is in flight. This CLI summarizes that append log AND the live process: wall
time since the run started, solves done vs expected, an in-flight worker count, a
ticking "since last completion", throughput, an approximate ETA, the per-resolution
breakdown, and the most recent completed shapes (g_frac, t_res, outcome).

Because the heavy N=512 solves take minutes each, the completed-solve count can sit
still for a while. So the tracker always shows *moving* signals -- wall-elapsed, a
since-last-completion timer, an in-flight count, and a spinner/refresh clock -- so
`--watch` visibly advances between completions rather than looking frozen.

Read-only. Beyond the common row fields written by ga.logbook + the phase1 runners
(`resolution_N`, `label`, `timestamp`, and when present `g_frac`/`t_res`/`outcome`),
it reads the producer's start time and worker count from /proc (Linux) to report
true wall-elapsed and concurrency; every field degrades gracefully if absent.

Usage:
  .venv/bin/python track.py                       # default: rankcheck log, one shot
  .venv/bin/python track.py --expected 40         # add a progress bar + ETA
  .venv/bin/python track.py FILE.jsonl --watch    # live refresh until the run ends
  .venv/bin/python track.py --watch --expected 40 --interval 5
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
SPINNER = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"  # braille dots


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
    sec = int(max(0, sec))
    if sec < 60:
        return f"{sec}s"
    if sec < 3600:
        return f"{sec // 60}m{sec % 60:02d}s"
    return f"{sec // 3600}h{(sec % 3600) // 60:02d}m"


# ----- /proc introspection: true wall-start + live worker count ---------------
def _comm(pid):
    try:
        with open(f"/proc/{pid}/comm") as f:
            return f.read().strip()
    except (FileNotFoundError, ProcessLookupError):
        return ""


def _pids(needle):
    """PIDs whose command line matches `needle`, restricted to python interpreters
    so shell wrappers / monitors / this tracker that merely mention the script name
    (via `pgrep -f`) are not miscounted as solver workers."""
    if not needle:
        return []
    try:
        out = subprocess.run(["pgrep", "-f", needle], capture_output=True, text=True)
    except FileNotFoundError:
        return []
    if out.returncode != 0:
        return []
    raw = [int(x) for x in out.stdout.split()]
    py = [p for p in raw if _comm(p).startswith("python")]
    if py:
        return py
    # No python matched. Do NOT fall back to raw blindly: `pgrep -f` also matches
    # shell wrappers / monitors / this tracker whose command line merely mentions
    # the script name (a waiter `while pgrep -f 'script.py'` even matches itself),
    # which would falsely report the producer as alive after it exited. Exclude
    # shells/utilities and self so a non-python producer still resolves.
    _SHELL = {"bash", "sh", "dash", "zsh", "fish", "pgrep", "grep", "ps", "sed",
              "awk", "cat", "tail", "nohup", "timeout", "env"}
    return [p for p in raw if _comm(p) not in _SHELL and p != os.getpid()]


def _stat_fields(pid):
    """/proc/<pid>/stat fields from field 3 onward (comm in field 2 may contain spaces)."""
    try:
        with open(f"/proc/{pid}/stat") as f:
            data = f.read()
        return data[data.rindex(")") + 2:].split()
    except (FileNotFoundError, ValueError, ProcessLookupError):
        return None


def _btime():
    try:
        with open("/proc/stat") as f:
            for line in f:
                if line.startswith("btime"):
                    return int(line.split()[1])
    except FileNotFoundError:
        pass
    return None


def _proc_start_epoch(pid):
    fields = _stat_fields(pid)
    bt = _btime()
    if not fields or bt is None:
        return None
    try:
        hz = os.sysconf("SC_CLK_TCK") or 100
        return bt + int(fields[19]) / hz          # field 22 = starttime (ticks)
    except (ValueError, IndexError, OSError):
        return None


def _proc_info(needle):
    """(alive, main_pid, start_epoch, n_workers) for the producer, from /proc."""
    pids = _pids(needle)
    if not pids:
        return False, None, None, 0
    pset = set(pids)
    main = next((p for p in sorted(pids)
                 if (fs := _stat_fields(p)) and len(fs) > 1 and int(fs[1]) not in pset),
                min(pids))
    return True, main, _proc_start_epoch(main), max(0, len(pids) - 1)


def _bar(frac, width=28):
    frac = max(0.0, min(1.0, frac))
    fill = int(round(frac * width))
    return "[" + "#" * fill + "-" * (width - fill) + f"] {frac * 100:5.1f}%"


def render(path, expected, proc):
    rows = _read_rows(path)
    now = datetime.now(timezone.utc)
    n = len(rows)
    alive, _, start_epoch, workers = _proc_info(proc)

    # wall clock: prefer the producer's true start; fall back to first completion
    tss = sorted(t for t in (_parse_ts(r) for r in rows) if t is not None)
    start_dt = (datetime.fromtimestamp(start_epoch, timezone.utc) if start_epoch
                else (tss[0] if tss else None))
    elapsed = (now - start_dt).total_seconds() if start_dt else None
    since_last = (now - tss[-1]).total_seconds() if tss else None

    spin = SPINNER[int(time.time()) % len(SPINNER)]
    status = "RUNNING" if alive else ("done/stopped" if alive is not None else "unknown")
    inflight = f"  ~{workers} in flight" if (alive and workers) else ""

    lines = [f"experiment: {path}",
             f"producer  : {proc}  [{status}]{inflight}",
             f"heartbeat : {spin}  updated {now.astimezone().strftime('%H:%M:%S')}   "
             f"elapsed {_fmt_dur(elapsed)}   since last solve {_fmt_dur(since_last)}"]

    if n == 0:
        lines += ["", f"0 solves completed yet {spin} "
                  "(the first N=512 solve can take a few minutes; the timers above move)"]
        return "\n".join(lines)

    # throughput on WALL time (elapsed/n) -- honest under N-way parallelism, where
    # completions arrive in bursts and a naive inter-completion gap understates cost.
    wall_per = elapsed / n if (elapsed and n) else None
    lines.append("")
    if expected:
        eta = max(0.0, (expected - n) * wall_per) if (wall_per and n < expected) else \
              (0.0 if n >= expected else None)
        lines.append(f"progress  : {n}/{expected}  {_bar(n / expected)}")
        lines.append(f"throughput: {_fmt_dur(wall_per)}/solve (wall)   ETA ~{_fmt_dur(eta)}"
                     f"{'  [ETA is rough: N=256 solves finish faster than N=512]' if expected else ''}")
    else:
        lines.append(f"progress  : {n} solves done   {_fmt_dur(wall_per)}/solve (wall)")

    # per-resolution breakdown, with a mini-bar when the per-N target is knowable
    by_n = {}
    for r in rows:
        by_n.setdefault(r.get("resolution_N", "?"), []).append(r)
    numeric_ns = [k for k in by_n if isinstance(k, (int, float))]
    per_n_target = (expected // len(numeric_ns)) if (expected and numeric_ns and
                                                     expected % len(numeric_ns) == 0) else None
    lines += ["", "by resolution:"]
    for nn in sorted(by_n, key=lambda x: (isinstance(x, str), x)):
        grp = by_n[nn]
        growers = sum(1 for r in grp if isinstance(r.get("t_res"), (int, float))
                      and r["t_res"] < 4.0 - 1e-6)
        tail = f"   {_bar(len(grp) / per_n_target, 14)}" if per_n_target else ""
        cap = f"/{per_n_target}" if per_n_target else ""
        lines.append(f"  N={str(nn):<5} {len(grp):3d}{cap} solves   "
                     f"{growers} growers (t_res<T_MAX){tail}")

    # last few completed
    lines += ["", "recent completions:"]
    for r in rows[-6:]:
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
    ap.add_argument("--interval", type=float, default=5.0, help="--watch refresh seconds")
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
            if _proc_info(args.proc)[0] is False:
                sys.stdout.write("\nproducer has exited -- final snapshot above.\n")
                sys.stdout.flush()
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nstopped watching.")


if __name__ == "__main__":
    main()
