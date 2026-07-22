"""Live progress dashboard for Stage 2 GA runs.

Reads experiments/index.jsonl and each stage2 experiment's events.jsonl
(flush-per-event, so a running experiment's log is always complete up to the
last event) and prints, per experiment:

- generation progress and an ETA from realized per-generation wall clocks,
- best-so-far nu_crit for the GA vs the budget-matched random baseline,
- archive coverage / QD-score,
- health counters (censored, non-monotone, cache hits, bracket expansions),
- a sparkline of both best-so-far curves against cumulative evaluations.

Usage:
    .venv/bin/python stage2_progress.py                # one snapshot
    .venv/bin/python stage2_progress.py --interval 30  # refresh every 30s
    .venv/bin/python stage2_progress.py stage2-seed1   # specific experiment(s)
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parent / "experiments"
GA_OPERATORS = {"init", "mutation", "crossover"}

BARS = " .:-=+*#%@"


def _read_jsonl(path):
    if not path.exists():
        return []
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def _sparkline(curve, width=44):
    vals = [v for v in curve if v is not None]
    if not vals:
        return "(no uncensored evals yet)"
    lo, hi = min(vals), max(vals)
    stride = max(1, len(curve) / width)
    out = []
    i = 0.0
    while int(i) < len(curve):
        v = curve[int(i)]
        if v is None:
            out.append(" ")
        else:
            frac = 1.0 if hi == lo else (v - lo) / (hi - lo)
            out.append(BARS[min(int(frac * (len(BARS) - 1)), len(BARS) - 1)])
        i += stride
    return "".join(out)


def _best_curve(rows):
    curve, best = [], None
    for r in rows:
        if r["bracket_censored"] is None:
            v = r["critical_value"]
            if best is None or v > best:
                best = v
        curve.append(best)
    return curve


def snapshot(experiment_ids=None):
    index = _read_jsonl(EXPERIMENTS / "index.jsonl")
    rows = [r for r in index if r["experiment_id"].startswith("stage2")]
    if experiment_ids:
        rows = [r for r in rows if r["experiment_id"] in experiment_ids]
    if not rows:
        print("no stage2 experiments in index.jsonl")
        return

    now = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"=== Stage 2 progress @ {now} UTC "
          f"({len(rows)} experiment(s)) ===")
    for row in rows:
        eid = row["experiment_id"]
        events = _read_jsonl(EXPERIMENTS / "run_logs" / eid / "events.jsonl")
        config_path = EXPERIMENTS / "run_logs" / eid / "config.json"
        cfg = json.loads(config_path.read_text()) if config_path.exists() else {}
        n_gens = cfg.get("n_generations", "?")

        evals = [e for e in events if e["event"] == "genome_eval"]
        gens = [e for e in events if e["event"] == "generation"]
        ga = [e for e in evals if e["operator"] in GA_OPERATORS]
        rand = [e for e in evals if e["operator"] == "baseline_random"]
        lit = [e for e in evals if e["operator"] == "baseline_literature"]

        ga_curve, rand_curve = _best_curve(ga), _best_curve(rand)
        ga_best = next((v for v in reversed(ga_curve) if v is not None), None)
        rand_best = next((v for v in reversed(rand_curve) if v is not None), None)
        lit_best = max((e["critical_value"] for e in lit
                        if e["bracket_censored"] is None), default=None)

        status = row["status"]
        eta = ""
        if gens and status == "running" and isinstance(n_gens, int):
            per_gen = [g["wall_clock_seconds"] for g in gens]
            remaining = (n_gens - len(gens)) * (sum(per_gen) / len(per_gen))
            eta = f"  ETA ~{remaining / 60:.0f} min"
        cov = gens[-1]["diversity_metric"]["archive_coverage"] if gens else 0.0
        qd = gens[-1]["diversity_metric"]["qd_score"] if gens else 0.0

        fmt = lambda v: f"{v:.4f}" if v is not None else "-"
        print(f"\n{eid}  [{status}]  gen {len(gens)}/{n_gens}{eta}")
        print(f"  best nu_crit: GA {fmt(ga_best)} | random {fmt(rand_best)} "
              f"| literature {fmt(lit_best)}   "
              f"archive: {cov:.0%} filled, QD {qd:.3f}")
        n_censored = sum(1 for e in evals if e["bracket_censored"] is not None)
        n_nonmono = sum(1 for e in evals
                        if e.get("critical_value_monotone") is False)
        n_cache = sum(1 for e in evals if e.get("cache_hit"))
        n_expand = sum(e.get("n_bracket_expansions", 0) for e in ga)
        print(f"  evals: {len(ga)} GA + {len(rand)} random + {len(lit)} lit   "
              f"censored {n_censored}, non-monotone {n_nonmono}, "
              f"cache hits {n_cache}, bracket expansions {n_expand}")
        print(f"  GA   {_sparkline(ga_curve)}")
        print(f"  rand {_sparkline(rand_curve)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment_ids", nargs="*")
    ap.add_argument("--interval", type=float, default=0,
                    help="refresh every N seconds (0 = print once and exit)")
    args = ap.parse_args()
    while True:
        snapshot(args.experiment_ids or None)
        if not args.interval:
            return 0
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
