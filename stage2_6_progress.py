"""Live progress dashboard for the Stage 2.6 sweep.

Reads experiments/stage2_6_sweep.jsonl (flush-per-row, so a running sweep's
file is always complete up to the last finished task) and prints:

- an overall progress bar with elapsed time and an ETA from the realized
  completion rate,
- a per-candidate table (bisections per a-value, fixed-nu D runs) with
  censoring / non-monotonicity health counters and the value band so far,
- an early read on the two make-or-break questions: does a>0 stay alive
  under the v3 amplification-only oracle, and where do the landscape tops
  sit relative to the init prior (the property-6 gap, computed live), and
- the most recently completed tasks.

Usage:
    .venv/bin/python stage2_6_progress.py                # one snapshot
    .venv/bin/python stage2_6_progress.py --interval 30  # refresh every 30s
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

JSONL = Path(__file__).resolve().parent / "experiments" / "stage2_6_sweep.jsonl"
OUT = Path(__file__).resolve().parent / "experiments" / "stage2_6_sweep.out"

# 40 shapes x 2 resolutions x (4 bisection a-values + 2 fixed-nu handicaps)
DEFAULT_TOTAL = 480
BAR_WIDTH = 40


def _read_rows():
    if not JSONL.exists():
        return []
    rows = []
    with open(JSONL) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _total_tasks():
    try:
        with open(OUT) as f:
            head = f.readline()
        # "40 shapes: 320 bisections (...) + 160 fixed-nu runs on 10 workers"
        n_bis = int(head.split(" bisections")[0].split()[-1])
        n_fix = int(head.split("+ ")[1].split()[0])
        return n_bis + n_fix
    except (OSError, ValueError, IndexError):
        return DEFAULT_TOTAL


def _ts(row):
    return datetime.fromisoformat(row["timestamp"])


def _fmt_span(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"


def _group_line(name, rows, value_key, censored_of):
    done = len(rows)
    cens = sum(1 for r in rows if censored_of(r))
    vals = [r[value_key] for r in rows
            if not censored_of(r) and r[value_key] is not None]
    nonmono = sum(1 for r in rows
                  if r.get("critical_value_monotone") is False)
    band = (f"{min(vals):.4f}-{max(vals):.4f}" if vals else "-")
    extn = sum(r.get("n_range_extensions", 0) for r in rows)
    return (f"  {name:14s} {done:3d} done   censored {cens:3d}   "
            f"nonmono {nonmono:2d}   band {band:>15s}"
            + (f"   range-ext {extn}" if extn else ""))


def _gap_line(rows, value_key, censored_of):
    """Live property-6 read: best init-prior vs best structured value."""
    best = {}
    for r in rows:
        if censored_of(r) or r[value_key] is None:
            continue
        src = r["ic"]["source"]
        best[src] = max(best.get(src, -1e9), r[value_key])
    if "init_prior" in best and "stage1_5" in best:
        gap = best["stage1_5"] - best["init_prior"]
        return (f"best structured {best['stage1_5']:.4f}  "
                f"best prior {best['init_prior']:.4f}  gap {gap:+.4f}")
    return "insufficient uncensored data for a gap estimate yet"


def snapshot():
    rows = _read_rows()
    total = _total_tasks()
    done = len(rows)
    lines = []

    if not rows:
        return ["stage2_6_sweep.jsonl is empty — sweep not started (or just "
                "starting)"]

    t0, t1 = _ts(rows[0]), _ts(rows[-1])
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
    rate = done / max((t1 - t0).total_seconds(), 1.0)
    eta = (total - done) / rate if rate > 0 and done < total else 0.0

    filled = done * BAR_WIDTH // total
    bar = "#" * filled + "-" * (BAR_WIDTH - filled)
    lines.append(f"[{bar}] {done}/{total} ({100 * done // total}%)  "
                 f"elapsed {_fmt_span(elapsed)}"
                 + (f"  ETA ~{_fmt_span(eta)}" if done < total else "  DONE"))
    lines.append("")

    bis = [r for r in rows if r["mode"] == "bisect"]
    fix = [r for r in rows if r["mode"] == "fixed_nu"]
    cens_bis = lambda r: r["bracket_censored"] is not None  # noqa: E731
    cens_fix = lambda r: r["censored"]  # noqa: E731

    lines.append("bisections (nu_crit under v3, t_max=24):")
    for a in sorted({r["fixed"]["a"] for r in bis}):
        sub = [r for r in bis if r["fixed"]["a"] == a]
        name = f"a={a:g}" + (" (B')" if a == 0.0 else " (A')")
        lines.append(_group_line(name, sub, "critical_value", cens_bis))
        lines.append(f"    {'':12s} {_gap_line(sub, 'critical_value', cens_bis)}")
    if fix:
        lines.append("candidate D (t_max - t_amp at fixed nu):")
        for nu in sorted({r["nu_fixed"] for r in fix}):
            sub = [r for r in fix if r["nu_fixed"] == nu]
            lines.append(_group_line(f"nu={nu:g}", sub, "fitness", cens_fix))
            lines.append(f"    {'':12s} {_gap_line(sub, 'fitness', cens_fix)}")

    lines.append("")
    lines.append("latest:")
    for r in rows[-3:]:
        if r["mode"] == "fixed_nu":
            val = ("censored" if r["censored"]
                   else f"fitness={r['fitness']:.3f}")
            desc = f"D(nu={r['nu_fixed']:g}) {val}"
        else:
            c = r["bracket_censored"]
            desc = (f"a={r['fixed']['a']:g} nu_crit={r['critical_value']:.4f}"
                    + (f" (censored {c})" if c else ""))
        lines.append(f"  {r['ic']['label']:24s} N={r['resolution_N']:4d} "
                     f"{desc} ({r['wall_clock_seconds']:.0f}s)")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", type=int, default=0,
                    help="refresh every N seconds (0 = one snapshot)")
    args = ap.parse_args()

    while True:
        out = snapshot()
        if args.interval:
            print("\033[2J\033[H", end="")  # clear screen between refreshes
        print(f"=== Stage 2.6 sweep progress — "
              f"{datetime.now().strftime('%H:%M:%S')} ===")
        print("\n".join(out))
        if not args.interval:
            break
        if any(l.endswith("DONE") for l in out):
            print("\nsweep complete.")
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
