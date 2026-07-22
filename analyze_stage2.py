"""Stage 2 acceptance analysis: budget-matched GA vs random baseline.

PLAN.md Stage 2 acceptance criterion: across >=3 independent seeds, the
GA's best-so-far nu_crit plotted against CUMULATIVE EVALUATIONS clearly
dominates the random-search baseline at the same budget (LOGGING.md's
budget-matched design principle — comparing at equal x-values, since the
max of 5000 draws trivially beats the max of 100).

Reads experiments/run_logs/<experiment_id>/events.jsonl for the given
experiment ids (default: all completed nu_crit experiments in
experiments/index.jsonl whose id starts with "stage2"). For each run:

- GA curve: best-so-far over genome_eval events with operator in
  {init, mutation, crossover}, in log order (which is evaluation order),
  censored rows excluded from the running max but counted in the budget.
- Baseline curve: same over operator == baseline_random.
- Literature positive control: best uncensored baseline_literature value.

Both curves are compared at matched evaluation counts; cache hits count on
both axes (they are logged evaluations). Verdict per seed: the final GA
best must exceed the final baseline best by more than the bisection
tolerance, and the GA curve must be >= the baseline curve over the final
half of the budget. Overall PASS requires every seed to pass.

Secondary (reported, not part of the frozen acceptance criterion): a
QD-score comparison at matched budget — the map-building analog of the
best-so-far comparison. Both event streams are replayed through identical
MAP-Elites insertion rules (uncensored + monotone-clean + beats incumbent),
so the question "does the GA build a better shape->resistance MAP than
random sampling at the same budget" is answered with the same honesty rules
as the fitness comparison. Also reported: cross-seed map convergence (cell
overlap and per-cell fitness agreement between independent seeds' final
archives).

Usage:
    .venv/bin/python analyze_stage2.py [experiment_id ...]
"""

import itertools
import json
import sys
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parent / "experiments"

GA_OPERATORS = {"init", "mutation", "crossover"}


def load_events(experiment_id):
    path = EXPERIMENTS / "run_logs" / experiment_id / "events.jsonl"
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def best_so_far_curve(rows):
    """[(cumulative_evals, best_so_far)] over uncensored critical values;
    censored evaluations advance the budget but never the best."""
    curve, best, n = [], None, 0
    for row in rows:
        n += 1
        if row["bracket_censored"] is None:
            v = row["critical_value"]
            if best is None or v > best:
                best = v
        curve.append((n, best))
    return curve


def replay_archive(rows, map_cfg):
    """Replay genome_eval rows through the real Archive insertion rules
    (ga/evolve.py — uncensored, monotone-clean, beats incumbent), returning
    the final archive and a [(n, coverage, qd_score)] curve. Cache hits are
    skipped exactly as the live loop skips them."""
    import numpy as np

    from ga.evolve import Archive
    from ga.genome import Genome

    arch = Archive(map_cfg)
    curve = []
    for row in rows:
        if not row.get("cache_hit"):
            genome = Genome(np.array(row["genome_coeffs"]),
                            row["genome_envelope_p"])
            arch.maybe_insert(row, genome)
        curve.append((len(curve) + 1, arch.coverage(), arch.qd_score()))
    return arch, curve


def map_convergence(arch_a, arch_b):
    """Cross-seed map agreement: Jaccard overlap of filled cells, and mean
    absolute fitness difference over shared cells."""
    cells_a, cells_b = set(arch_a.cells), set(arch_b.cells)
    shared = cells_a & cells_b
    union = cells_a | cells_b
    jaccard = len(shared) / len(union) if union else 0.0
    diffs = [abs(arch_a.cells[c]["fitness"] - arch_b.cells[c]["fitness"])
             for c in shared]
    return {
        "jaccard": jaccard,
        "n_shared": len(shared),
        "n_union": len(union),
        "mean_abs_fitness_diff": (sum(diffs) / len(diffs)) if diffs else None,
    }


def analyze(experiment_id):
    events = [e for e in load_events(experiment_id)
              if e["event"] == "genome_eval"]
    config = json.loads(
        (EXPERIMENTS / "run_logs" / experiment_id / "config.json").read_text())
    tol = config["bisection"]["tolerance"]

    ga = [e for e in events if e["operator"] in GA_OPERATORS]
    rand = [e for e in events if e["operator"] == "baseline_random"]
    lit = [e for e in events if e["operator"] == "baseline_literature"]

    ga_curve = best_so_far_curve(ga)
    rand_curve = best_so_far_curve(rand)
    lit_best = max((e["critical_value"] for e in lit
                    if e["bracket_censored"] is None), default=None)

    budget = min(len(ga_curve), len(rand_curve))
    ga_final = ga_curve[budget - 1][1]
    rand_final = rand_curve[budget - 1][1]
    margin = (ga_final - rand_final
              if ga_final is not None and rand_final is not None else None)

    # Dominance over the final half of the budget (burn-in excluded: early
    # best-so-far is order-statistics noise on both sides).
    half = budget // 2
    dominated = all(
        (g is None and r is None) or (g is not None and (r is None or g >= r))
        for (_, g), (_, r) in zip(ga_curve[half:budget], rand_curve[half:budget])
    )
    passed = (margin is not None and margin > tol and dominated)

    # Secondary: map-building at matched budget, identical insertion rules.
    map_cfg = config["ga_operators"]["map_elites"]
    ga_arch, ga_qd_curve = replay_archive(ga[:budget], map_cfg)
    rand_arch, rand_qd_curve = replay_archive(rand[:budget], map_cfg)
    qd_dominated = all(g[2] >= r[2] for g, r in
                       zip(ga_qd_curve[half:], rand_qd_curve[half:]))

    n_censored = sum(1 for e in ga + rand if e["bracket_censored"] is not None)
    n_nonmono = sum(1 for e in ga + rand
                    if e.get("critical_value_monotone") is False)
    n_cache = sum(1 for e in ga if e.get("cache_hit"))
    return {
        "experiment_id": experiment_id,
        "seed": config["random_seed"],
        "budget": budget,
        "ga_final": ga_final,
        "rand_final": rand_final,
        "margin": margin,
        "margin_over_tol": margin / tol if margin is not None else None,
        "lit_best": lit_best,
        "beats_literature": (ga_final is not None and lit_best is not None
                             and ga_final >= lit_best),
        "dominated_final_half": dominated,
        "n_censored": n_censored,
        "n_nonmonotone": n_nonmono,
        "n_cache_hits": n_cache,
        "passed": passed,
        "ga_curve": ga_curve,
        "rand_curve": rand_curve,
        "ga_archive": ga_arch,
        "rand_archive": rand_arch,
        "ga_qd_final": ga_qd_curve[-1] if ga_qd_curve else None,
        "rand_qd_final": rand_qd_curve[-1] if rand_qd_curve else None,
        "qd_dominated_final_half": qd_dominated,
    }


def default_experiment_ids():
    ids = []
    with open(EXPERIMENTS / "index.jsonl") as f:
        for line in f:
            row = json.loads(line)
            if (row["experiment_id"].startswith("stage2")
                    and row["status"] == "completed"):
                ids.append(row["experiment_id"])
    return ids


def sparkline(curve, width=48):
    pts = [v for _, v in curve if v is not None]
    if not pts:
        return "(no uncensored evals)"
    lo, hi = min(pts), max(pts)
    stride = max(1, len(curve) // width)
    chars = " .:-=+*#%@"
    out = []
    for i in range(0, len(curve), stride):
        v = curve[i][1]
        if v is None:
            out.append(" ")
        else:
            frac = 1.0 if hi == lo else (v - lo) / (hi - lo)
            out.append(chars[min(int(frac * (len(chars) - 1)), len(chars) - 1)])
    return "".join(out)


def main():
    ids = sys.argv[1:] or default_experiment_ids()
    if not ids:
        sys.exit("no stage2 experiments found in index.jsonl")
    results = [analyze(eid) for eid in ids]

    print(f"{'experiment':34s} {'seed':>5s} {'budget':>6s} {'GA best':>9s} "
          f"{'rand best':>9s} {'margin/tol':>10s} {'lit best':>9s} "
          f"{'dom.':>5s} {'pass':>5s}")
    for r in results:
        fmt = lambda v: f"{v:.4f}" if v is not None else "  -   "
        print(f"{r['experiment_id']:34s} {r['seed']:5d} {r['budget']:6d} "
              f"{fmt(r['ga_final']):>9s} {fmt(r['rand_final']):>9s} "
              f"{r['margin_over_tol']:>10.1f} {fmt(r['lit_best']):>9s} "
              f"{str(r['dominated_final_half']):>5s} "
              f"{str(r['passed']):>5s}")
        print(f"  GA   {sparkline(r['ga_curve'])}")
        print(f"  rand {sparkline(r['rand_curve'])}")
        print(f"  censored={r['n_censored']} non-monotone={r['n_nonmonotone']} "
              f"cache_hits={r['n_cache_hits']}")

    print("\n--- secondary: map-building (QD) at matched budget ---")
    print(f"{'experiment':34s} {'GA cov':>7s} {'GA QD':>8s} "
          f"{'rand cov':>8s} {'rand QD':>8s} {'QD dom.':>8s}")
    for r in results:
        _, gcov, gqd = r["ga_qd_final"]
        _, rcov, rqd = r["rand_qd_final"]
        print(f"{r['experiment_id']:34s} {gcov:7.1%} {gqd:8.3f} "
              f"{rcov:8.1%} {rqd:8.3f} "
              f"{str(r['qd_dominated_final_half']):>8s}")

    if len(results) >= 2:
        print("\n--- cross-seed map convergence (final GA archives) ---")
        for a, b in itertools.combinations(results, 2):
            m = map_convergence(a["ga_archive"], b["ga_archive"])
            diff = (f"{m['mean_abs_fitness_diff']:.4f}"
                    if m["mean_abs_fitness_diff"] is not None else "-")
            print(f"{a['experiment_id']} vs {b['experiment_id']}: "
                  f"jaccard {m['jaccard']:.2f} "
                  f"({m['n_shared']}/{m['n_union']} cells), "
                  f"mean |dfitness| on shared cells {diff}")

    n_pass = sum(r["passed"] for r in results)
    overall = n_pass == len(results) and len(results) >= 3
    print(f"\n{n_pass}/{len(results)} seeds pass "
          f"(need every seed, >=3 seeds).")
    print(f"STAGE 2 ACCEPTANCE: {'PASS' if overall else 'NOT MET'}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
