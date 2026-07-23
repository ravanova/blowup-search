"""Non-genericity axis sweep — post-Stage-3 pivot de-risking.

Question this answers (raised on review after Stage 3): the GA's demonstrated
edge lives at a=0.7, where every confirmed blow-up is *generic* CLM-type
(alpha = 1.000, STAGE_3_RESULTS.md). The scientifically novel, Tier-3-provable
target is a *non-generic* (alpha != 1) De Gregorio-type singularity, which the
literature places near a=1 with rough (limited-regularity) data. Do those two
regimes overlap — i.e. is there a searchable, resolution-stable fitness axis
for non-genericity anywhere the GA can climb — or are they disjoint?

This sweep measures the raw ingredients of that axis, with NO GA and NO
bisection: for each roster shape x a in {0.7, 0.9, 1.0} x N in {256, 512}, one
inviscid (nu=0) solver run to blow-up, recording whether it blew up and the
held-out fitted exponent alpha (with its R^2, T*, and conservation drift). The
analyzer (analyze_nongenericity.py) then gates the candidate non-genericity
fitness |alpha - 1| on the same six-property checklist used for Stage 2.5/2.6,
with the single-run property adaptations candidate D established (monotonicity
-> well-definedness; noise floor from cross-resolution |Delta alpha|), and
folds in the "x p-regimes" question by reporting how alpha and blow-up
occurrence vary with the shape's own regularity (envelope p / tail slope) --
the roster's 20 init-prior draws already span p in [0, 3.5].

Frozen at Stage 2.6's solver config (t_max=24, v3-style inviscid amplification
blow-up, early-decay exit, dt policy), EXCEPT amplification raised to 1e3 so
the exponent fit sees three decades (100x gave garbage fits in the marginal
high-a rough regime), and max_steps capped so no-blow-up / near-critical runs
bail as `max_steps_hit` (censored for the alpha axis) instead of burning the
horizon. alpha values are horizon/amplification-relative and never comparable
to the Stage 2.6 nu_crit numbers.

Usage:
    .venv/bin/python nongenericity_sweep.py --workers 10     # full sweep
    .venv/bin/python nongenericity_sweep.py --smoke          # tiny shakedown
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

from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.gclm import solve_gclm
from win_condition import InsufficientDataError, estimate_blowup_time
from stage2_5_sweep import build_shapes, realize_shape

# --- frozen sweep configuration --------------------------------------------

A_VALUES = (0.7, 0.9, 1.0)     # GA-edge regime -> toward De Gregorio
RESOLUTIONS = (256, 512)
T_MAX = 24.0
TAIL_FRACTION = 0.15
AMPLIFICATION = 1e3            # 3 decades: enough to fit alpha, cheaper than 1e4

SOLVER_PARAMS = dict(
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    max_steps=300_000,         # cap: near-critical/no-blow-up runs bail here
    amplification_factor=AMPLIFICATION,
    early_decay_exit={"fraction": 0.1, "window": 2.0},
)


def run_task(task):
    """One inviscid (shape, a, N) run: blow-up? and the held-out exponent."""
    omega0 = task["omega0"]
    a = float(task["a"])
    t0 = time.perf_counter()
    r = solve_gclm(omega0, a=a, nu=0.0, t_max=T_MAX, **SOLVER_PARAMS)
    blew = r.outcome in ("blowup_candidate", "diverged")

    est = None
    if blew:
        try:
            est = estimate_blowup_time(
                r.times.tolist(), r.max_omega.tolist(),
                tail_fraction=TAIL_FRACTION, fit_exponent=True)
        except InsufficientDataError:
            est = None  # amplified too fast to fit -> alpha undefined

    estimate = None if est is None else {
        "t_star": float(est.t_star), "r_squared": float(est.r_squared),
        "exponent": float(est.exponent), "slope": float(est.slope),
        "last_time": float(est.last_time), "n_points": int(est.n_points),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "sweep": "nongenericity",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "ic": task["meta"],
        "fixed": {"a": a, "nu": 0.0},
        "resolution_N": int(task["n_res"]),
        "t_max": T_MAX,
        "amplification_factor": AMPLIFICATION,
        "blowup": bool(blew),
        "outcome": r.outcome,
        "estimate": estimate,
        "conservation_drift": float(r.conservation_drift),
        "n_timesteps": int(r.n_timesteps),
        "solver_params": {k: v for k, v in SOLVER_PARAMS.items()},
        "wall_clock_seconds": time.perf_counter() - t0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/nongenericity_sweep.jsonl")
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--smoke", action="store_true",
                    help="2 shapes, a in {0.7, 1.0}, N=128")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty "
                 "to mark rows non-reproducible)")
    code_ver = code_version()

    shapes = build_shapes(None)
    a_values, resolutions = A_VALUES, RESOLUTIONS
    if args.smoke:
        shapes = [shapes[0], shapes[-1]]
        a_values, resolutions = (0.7, 1.0), (128,)

    tasks = []
    for shape in shapes:
        meta = {k: shape[k] for k in ("label", "family", "source", "spec",
                                      "energy", "ic_hash", "spectral",
                                      "descriptors")}
        for n_res in resolutions:
            omega0 = realize_shape(shape, n_res)
            for a in a_values:
                tasks.append({"omega0": omega0, "a": a, "n_res": n_res,
                              "meta": meta, "code_version": code_ver,
                              "code_dirty": dirty})

    print(f"{len(shapes)} shapes x {len(a_values)} a-values x "
          f"{len(resolutions)} resolutions = {len(tasks)} inviscid runs "
          f"(alpha @ amp={AMPLIFICATION:g}) on {args.workers} workers",
          flush=True)

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
                est = row["estimate"]
                if not row["blowup"]:
                    desc = f"{row['outcome']:14s} (no blowup)"
                elif est is None:
                    desc = "blew (no fit)"
                else:
                    desc = (f"blew  alpha={est['exponent']:.2f} "
                            f"R2={est['r_squared']:.3f} T*={est['t_star']:.2f}")
                print(f"[{done:3d}/{len(tasks)}] {row['ic']['label']:24s} "
                      f"a={row['fixed']['a']:.1f} N={row['resolution_N']:4d} "
                      f"{desc} ({row['wall_clock_seconds']:.1f}s)", flush=True)
        finally:
            if pool is not None:
                pool.close()
                pool.join()
    print(f"\nSweep complete: {done} runs in "
          f"{time.perf_counter() - t0:.0f}s -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
