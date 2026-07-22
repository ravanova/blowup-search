"""Stage 2.6 sweep: oracle v3 + reformulated fitness quantities (PLAN.md
Stage 2.6, the approved Stage 2.5 review outcome).

Two measurement modes over the same 40-shape roster (20 Stage 1.5 ICs + 20
init-prior draws, via stage2_5_sweep.build_shapes), N in {256, 512}:

1. `bisect` — nu_crit under the v3 amplification-only oracle at
   a in {0.0, 0.4, 0.7, 1.0}, t_max = 24 (2x Stage 2: slow growers must
   DEMONSTRATE blow-up by amplifying 100x; v2's extrapolated boundary T*
   at a=0.7 was 17-18, so genuine blow-ups have headroom). Covers
   candidate A' (a > 0), candidate B' (a = 0, also the substrate for
   candidate C = nu_crit * k_eff^2, pure post-processing in the analyzer),
   with the same range ladder as Stage 2.5.
2. `fixed_nu` — candidate D: time-to-amplification at fixed handicap
   nu in {0.01, 0.03}, a = 0, one solver run per evaluation (no
   bisection). fitness = t_max - t_amp; a shape that never amplifies
   within the horizon is censored, not zero-fitness.

The v3 oracle change is exactly one flag (ga.fitness.classify_run's
blowup_predicate="v3_amplification_only"): amplification or divergence is
blow-up, nothing else is; the tail fit is still computed and logged but
never decides. Everything else (100x amplification, early-decay exit, dt
policy, tolerance 1e-3, censoring, monotonicity probes) is unchanged from
Stage 2.5. v3 critical values are horizon-relative to t_max=24 and NEVER
comparable to v2 values.

Usage:
    .venv/bin/python stage2_6_sweep.py --workers 10        # full sweep
    .venv/bin/python stage2_6_sweep.py --smoke             # tiny shakedown
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")  # pin BLAS for process parallelism

import argparse
import json
import multiprocessing
import sys
import time
from datetime import datetime, timezone

import numpy as np

from ga.fitness import bisect_critical, classify_run
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.gclm import solve_gclm
from stage2_5_sweep import (
    BISECTION_BASE,
    N_REFERENCE,
    NU_RANGE_LADDER,
    RESOLUTIONS,
    build_shapes,
    realize_shape,
)

# --- frozen Stage 2.6 configuration ----------------------------------------

T_MAX = 24.0                      # v3 horizon (2x Stage 2/2.5)
A_VALUES_BISECT = (0.0, 0.4, 0.7, 1.0)   # B' at 0.0; A' candidates above
D_FIXED_NUS = (0.01, 0.03)        # candidate D handicaps (Stage 1.5 band)

ORACLE_V3 = {
    "t_max": T_MAX,
    "tail_fraction": BISECTION_BASE["tail_fraction"],
    "predicate_r2_floor": BISECTION_BASE["predicate_r2_floor"],
    "t_star_cap_factor": BISECTION_BASE["t_star_cap_factor"],
    "blowup_predicate": "v3_amplification_only",
}

SOLVER_PARAMS = dict(
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    max_steps=400_000,            # doubled with the horizon
    amplification_factor=100.0,
    early_decay_exit={"fraction": 0.1, "window": 2.0},
)


def _k_eff_sq(shape):
    """Energy-weighted mean-square wavenumber from the reference-grid
    spectrum — the k_eff^2 factor of candidate C."""
    w_ref = realize_shape(shape, N_REFERENCE)
    w_hat = np.fft.rfft(w_ref)
    e_k = np.abs(w_hat[1:]) ** 2
    k = np.arange(1, len(e_k) + 1, dtype=float)
    return float(np.sum(k * k * e_k) / np.sum(e_k))


# --- worker ----------------------------------------------------------------


def run_task(task):
    omega0 = task["omega0"]
    a = float(task["a"])
    t0 = time.perf_counter()

    def run_at(nu):
        return classify_run(
            solve_gclm(omega0, a=a, nu=float(nu), t_max=T_MAX, **SOLVER_PARAMS),
            ORACLE_V3)

    base = {
        "schema_version": SCHEMA_VERSION,
        "sweep": "stage2_6",
        "oracle": "v3_amplification_only",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "ic": task["meta"],
        "fixed": {"a": a},
        "resolution_N": int(task["n_res"]),
        "t_max": T_MAX,
        "solver_params": {k: v for k, v in SOLVER_PARAMS.items()},
    }

    if task["mode"] == "fixed_nu":
        nu = float(task["nu_fixed"])
        blow, summary = run_at(nu)
        return {**base, "mode": "fixed_nu", "nu_fixed": nu,
                "blowup": bool(blow),
                "censored": not blow,
                "t_amp": summary["t_final"] if blow else None,
                "fitness": (T_MAX - summary["t_final"]) if blow else None,
                "via": summary["via"],
                "outcome": summary["outcome"],
                "estimate": summary["estimate"],
                "conservation_drift": summary["conservation_drift"],
                "n_timesteps": summary["n_timesteps"],
                "wall_clock_seconds": time.perf_counter() - t0}

    n_extensions = 0
    for lo, hi in NU_RANGE_LADDER:
        bisection = dict(BISECTION_BASE, range=[lo, hi])
        bis = bisect_critical(run_at, bisection, warm_center=None)
        if bis["bracket_censored"] != "high":
            break
        n_extensions += 1
    runs = bis.pop("runs")
    return {**base, "mode": "bisect",
            "range": [lo, hi],
            "n_range_extensions": n_extensions,
            "tolerance": BISECTION_BASE["tolerance"],
            **{k: bis[k] for k in (
                "critical_value", "bracket_censored", "initial_bracket",
                "n_bracket_expansions", "n_bisection_steps",
                "critical_value_monotone", "monotone_probes")},
            "n_runs": len(runs),
            "wall_clock_seconds": time.perf_counter() - t0,
            "runs": runs}


# --- driver ----------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/stage2_6_sweep.jsonl")
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--smoke", action="store_true",
                    help="2 shapes, a in {0.0, 0.7}, N=128, coarse tol")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty "
                 "to mark rows non-reproducible)")
    code_ver = code_version()

    shapes = build_shapes(None)
    a_values, resolutions, d_nus = A_VALUES_BISECT, RESOLUTIONS, D_FIXED_NUS
    if args.smoke:
        shapes = [shapes[0], shapes[-1]]
        a_values, resolutions, d_nus = (0.0, 0.7), (128,), (0.01,)
        BISECTION_BASE["tolerance"] = 0.0125

    tasks = []
    for shape in shapes:
        meta = {k: shape[k] for k in ("label", "family", "source", "spec",
                                      "energy", "ic_hash", "spectral",
                                      "descriptors")}
        meta["k_eff_sq"] = _k_eff_sq(shape)
        for n_res in resolutions:
            omega0 = realize_shape(shape, n_res)
            common = {"omega0": omega0, "n_res": n_res, "meta": meta,
                      "code_version": code_ver, "code_dirty": dirty}
            for a in a_values:
                tasks.append({**common, "mode": "bisect", "a": a})
            for nu in d_nus:
                tasks.append({**common, "mode": "fixed_nu", "a": 0.0,
                              "nu_fixed": nu})

    n_bisect = sum(t["mode"] == "bisect" for t in tasks)
    print(f"{len(shapes)} shapes: {n_bisect} bisections "
          f"(a in {a_values}, v3, t_max={T_MAX}) + "
          f"{len(tasks) - n_bisect} fixed-nu runs (candidate D) "
          f"on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    t0 = time.perf_counter()
    done = 0
    with open(args.out, "a") as out_file:
        if args.workers > 0:
            pool = multiprocessing.get_context().Pool(args.workers)
            it = pool.imap_unordered(run_task, tasks, chunksize=1)
        else:
            pool = None
            it = map(run_task, tasks)
        try:
            for row in it:
                out_file.write(json.dumps(row) + "\n")
                out_file.flush()
                os.fsync(out_file.fileno())
                done += 1
                if row["mode"] == "fixed_nu":
                    fit = row["fitness"]
                    desc = (f"D(nu={row['nu_fixed']:g}) fitness = "
                            f"{'censored' if fit is None else format(fit, '.3f')}")
                else:
                    cens = row["bracket_censored"]
                    desc = (f"a={row['fixed']['a']:.1f} nu_crit = "
                            f"{row['critical_value']:.4f}"
                            f"{' (censored ' + cens + ')' if cens else ''} "
                            f"mono={row['critical_value_monotone']}")
                print(f"[{done:3d}/{len(tasks)}] {row['ic']['label']:24s} "
                      f"N={row['resolution_N']:4d} {desc} "
                      f"({row['wall_clock_seconds']:.1f}s)", flush=True)
        finally:
            if pool is not None:
                pool.close()
                pool.join()
    print(f"\nSweep complete: {done} tasks in "
          f"{time.perf_counter() - t0:.0f}s -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
