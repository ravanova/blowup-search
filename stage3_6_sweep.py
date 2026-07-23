"""Stage 3.6 — Route A, Phase 0: fine-N rough-data exponent measurement.

This is the second Phase-0 deliverable (PLAN.md Stage 3.6 / CLAY_ROADMAP.md
Route A). Deliverable 1 is the C^{1,alpha} rough-data genome mode in
ga/genome.py (holder_profile / rough_genome), unit-tested in
test_genome_rough.py. This sweep is the measurement that eats it.

Question (pre-committed gate, do NOT soften mid-run): with GENUINE
limited-regularity (Holder-h) vorticity near a=1, does the fitted blow-up
RATE exponent alpha (M ~ (T*-t)^{-alpha}) CONVERGE as the grid refines, or
does it still RAIL at grid scale as it did for smooth/random data at
N in {256,512} in Stage 3.5 (NONGENERICITY_RESULTS.md)?

  - alpha converges to a NON-GENERIC value (|alpha-1| resolvable) near a=1
    -> surprise: gCLM is not exhausted, a novel 1D candidate may be reachable
    -> STOP and re-plan before any 2D solver.
  - alpha still rails / flips / the axis is dead (expected) -> gCLM confirmed
    exhausted for smooth AND rough data at reachable N -> carry the method +
    representation principle into Phase 1 (2D Boussinesq).

Two terminology notes, because both quantities are historically called
"alpha": here `h` is the DATA regularity (Holder exponent of the initial
vorticity, the rough-data knob) and `exponent` is the fitted BLOW-UP RATE
exponent from win_condition (the thing the gate watches). They are unrelated.

Design (mirrors nongenericity_sweep.py, the Stage 3.5 substrate, with the
resolutions pushed to {1024, 2048, 4096} and the roster swapped for true
rough data):
- Roster: the odd C^{0,h} profiles f_h = sign(sin x)|sin x|^h at a spread of
  Holder exponents h (small h = rough, h=1 = smooth sin x control), each
  realized analytically at the target grid N (realize_holder) so refining N
  resolves more of the Holder tail rather than truncating a fixed genome.
- a in {0.7, 0.9, 0.95, 1.0}. a=0.7 is a METHODOLOGICAL CONTROL, not a target:
  Stage 3.5 established it is generic (alpha==1) and resolution-exact for all
  regularity classes, so the fine-N measurement MUST recover alpha~1 stably
  there or the measurement itself is untrustworthy (validate where the answer
  is known, per the roadmap). a in {0.9, 0.95, 1.0} is the De Gregorio edge
  the rough-data bet is about.
- One inviscid (nu=0) run per (h, a, N) to blow-up; record blow-up, the
  held-out fitted exponent (R^2, T*), and the conservation-drift guard.

alpha values are horizon/amplification-relative (t_max=24, amp=1e3) and never
comparable to the Stage 2.6 nu_crit numbers. The gate lives in
analyze_stage3_6.py.

Usage:
    .venv/bin/python stage3_6_sweep.py --workers 10     # full sweep
    .venv/bin/python stage3_6_sweep.py --smoke          # tiny shakedown
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")  # pin BLAS for process parallelism

import argparse
import hashlib
import json
import multiprocessing
import sys
import time
from datetime import datetime, timezone

import numpy as np

from ga.genome import (
    ENERGY_BUDGET,
    holder_profile,
    measure_holder_exponent,
    realize_holder,
)
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.gclm import solve_gclm
from solver.spectral_utils import energy
from win_condition import InsufficientDataError, estimate_blowup_time

# --- frozen sweep configuration --------------------------------------------

H_VALUES = (0.20, 0.35, 0.50, 0.65, 0.80, 1.00)  # data Holder exponent (1=smooth)
A_VALUES = (0.7, 0.9, 0.95, 1.0)                  # 0.7 = control; 0.9-1.0 = target
RESOLUTIONS = (1024, 2048, 4096)
T_MAX = 24.0
TAIL_FRACTION = 0.15
AMPLIFICATION = 1e3            # 3 decades: fittable exponent, matches Stage 3.5

SOLVER_PARAMS = dict(
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    max_steps=200_000,         # cap: non-blow-up runs near a=1 bail here
    amplification_factor=AMPLIFICATION,
    early_decay_exit={"fraction": 0.1, "window": 2.0},
)

N_REFERENCE = 4096  # grid for the identity hash + the reference Holder-exponent


def build_shapes():
    """The rough-data roster: one entry per Holder exponent h. Each carries a
    resolution-free identity hash and its measured real-space Holder exponent
    (the regularity certificate travels with the row)."""
    shapes = []
    for h in H_VALUES:
        w_ref = realize_holder(h, N_REFERENCE)
        shapes.append({
            "label": f"holder(h={h:.2f})",
            "family": "holder_rough",
            "source": "rough_data",
            "spec": {"type": "holder_profile", "h": float(h),
                     "construction": "sign(sin x)*|sin x|^h"},
            "h": float(h),
            "holder_exponent_measured": measure_holder_exponent(holder_profile(h)),
            "energy": float(energy(w_ref)),
            "ic_hash": hashlib.sha256(w_ref.tobytes()).hexdigest(),
        })
    return shapes


def run_task(task):
    """One inviscid (h, a, N) run: blow-up? and the held-out blow-up-rate
    exponent."""
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
            est = None  # amplified too fast to fit -> exponent undefined

    estimate = None if est is None else {
        "t_star": float(est.t_star), "r_squared": float(est.r_squared),
        "exponent": float(est.exponent), "slope": float(est.slope),
        "last_time": float(est.last_time), "n_points": int(est.n_points),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "sweep": "stage3_6",
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
    ap.add_argument("--out", default="experiments/stage3_6_sweep.jsonl")
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--smoke", action="store_true",
                    help="2 h-values, a in {0.7, 1.0}, N=512")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty "
                 "to mark rows non-reproducible)")
    code_ver = code_version()

    shapes = build_shapes()
    a_values, resolutions = A_VALUES, RESOLUTIONS
    if args.smoke:
        shapes = [shapes[0], shapes[-1]]
        a_values, resolutions = (0.7, 1.0), (512,)

    tasks = []
    for shape in shapes:
        meta = {k: shape[k] for k in ("label", "family", "source", "spec",
                                      "h", "holder_exponent_measured",
                                      "energy", "ic_hash")}
        for n_res in resolutions:
            omega0 = realize_holder(shape["h"], n_res)
            for a in a_values:
                tasks.append({"omega0": omega0, "a": a, "n_res": n_res,
                              "meta": meta, "code_version": code_ver,
                              "code_dirty": dirty})

    # Slow runs (non-blow-up near a=1 at fine N) are max_steps-bound; sort the
    # biggest grids first so they start early and do not serialize at the tail.
    tasks.sort(key=lambda t: -t["n_res"])

    print(f"{len(shapes)} rough shapes x {len(a_values)} a-values x "
          f"{len(resolutions)} resolutions = {len(tasks)} inviscid runs "
          f"(alpha @ amp={AMPLIFICATION:g}, N up to {max(resolutions)}) "
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
                est = row["estimate"]
                if not row["blowup"]:
                    desc = f"{row['outcome']:16s} (no blowup)"
                elif est is None:
                    desc = "blew (no fit)"
                else:
                    desc = (f"blew  alpha={est['exponent']:.2f} "
                            f"R2={est['r_squared']:.3f} T*={est['t_star']:.2f}")
                print(f"[{done:3d}/{len(tasks)}] {row['ic']['label']:16s} "
                      f"a={row['fixed']['a']:.2f} N={row['resolution_N']:4d} "
                      f"{desc} drift={row['conservation_drift']:.1e} "
                      f"({row['wall_clock_seconds']:.1f}s)", flush=True)
        finally:
            if pool is not None:
                pool.close()
                pool.join()
    print(f"\nSweep complete: {done} runs in "
          f"{time.perf_counter() - t0:.0f}s -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
