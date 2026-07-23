"""Live progress dashboard for the Stage 3.6 fine-N rough-data sweep.

Reads experiments/stage3_6_sweep.jsonl (flush-per-row, so a running sweep's
file is always complete up to the last finished task) and prints:

- an overall progress bar with elapsed time and an ETA from the realized rate,
- the blow-up-rate exponent grid: one block per advection a, rows = data
  Holder exponent h, columns = resolution N, each cell the fitted alpha (with
  '*' = blew but fit below the R^2 floor, '-' = no blow-up / no fit) so you can
  watch, live, whether alpha CONVERGES across N or RAILS at the grid edge,
- the a=0.7 control read (should stay generic alpha~1) and the latest rows.

This is a viewer only; the pre-committed verdict is analyze_stage3_6.py.

Usage:
    .venv/bin/python stage3_6_progress.py                # one snapshot
    .venv/bin/python stage3_6_progress.py --interval 20  # refresh every 20s
"""

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

JSONL = Path(__file__).resolve().parent / "experiments" / "stage3_6_sweep.jsonl"

DEFAULT_TOTAL = 72   # 6 Holder h x 4 a-values x 3 resolutions
BAR_WIDTH = 40
R2_FLOOR = 0.9
CONTROL_A = 0.7


def _read_rows():
    if not JSONL.exists():
        return []
    rows = []
    with open(JSONL) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def _fmt_span(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m{s:02d}s"


def _cell(row):
    if row is None:
        return "."          # not run yet
    if not row["blowup"] or row["estimate"] is None:
        return "-"          # no blow-up / no fittable tail
    a = row["estimate"]["exponent"]
    ok = row["estimate"]["r_squared"] >= R2_FLOOR
    return f"{a:.2f}" + ("" if ok else "*")


def snapshot():
    rows = _read_rows()
    done = len(rows)
    lines = []
    if not rows:
        return ["stage3_6_sweep.jsonl is empty — sweep not started (or just "
                "starting)"]

    total = DEFAULT_TOTAL
    t0 = datetime.fromisoformat(rows[0]["timestamp"])
    t1 = datetime.fromisoformat(rows[-1]["timestamp"])
    elapsed = (datetime.now(timezone.utc) - t0).total_seconds()
    rate = done / max((t1 - t0).total_seconds(), 1.0)
    eta = (total - done) / rate if rate > 0 and done < total else 0.0
    filled = done * BAR_WIDTH // total
    bar = "#" * filled + "-" * (BAR_WIDTH - filled)
    lines.append(f"[{bar}] {done}/{total} ({100 * done // total}%)  "
                 f"elapsed {_fmt_span(elapsed)}"
                 + (f"  ETA ~{_fmt_span(eta)}" if done < total else "  DONE"))

    table = {(r["ic"]["h"], r["fixed"]["a"], r["resolution_N"]): r for r in rows}
    hs = sorted({r["ic"]["h"] for r in rows})
    a_values = sorted({r["fixed"]["a"] for r in rows})
    ns = sorted({r["resolution_N"] for r in rows})

    lines.append("")
    lines.append("fitted blow-up-rate exponent alpha  "
                 "('*'=fit below R^2 floor, '-'=no blow-up, '.'=pending):")
    for a in a_values:
        tag = "  <- CONTROL: want generic alpha~1, stable" \
            if a == CONTROL_A else ""
        lines.append(f"  a = {a:<5g}{tag}")
        lines.append("     " + "h\\N ".rjust(8)
                     + "".join(f"{n:>8d}" for n in ns))
        for h in hs:
            cells = "".join(f"{_cell(table.get((h, a, n))):>8s}" for n in ns)
            lines.append("     " + f"{h:.2f}".rjust(8) + cells)

    lines.append("")
    lines.append("latest:")
    for r in rows[-3:]:
        est = r["estimate"]
        desc = (f"alpha={est['exponent']:.2f} R2={est['r_squared']:.3f}"
                if est else f"{r['outcome']} (no fit)")
        lines.append(f"  {r['ic']['label']:16s} a={r['fixed']['a']:.2f} "
                     f"N={r['resolution_N']:4d} {desc} "
                     f"({r['wall_clock_seconds']:.0f}s)")
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
        print(f"=== Stage 3.6 sweep progress — "
              f"{datetime.now().strftime('%H:%M:%S')} ===")
        print("\n".join(out))
        if not args.interval or any(l.endswith("DONE") for l in out):
            if args.interval:
                print("\nsweep complete.")
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
