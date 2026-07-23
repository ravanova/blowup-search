"""Phase 1 resolution de-risk spike (reordered before the Gate 3 genome).

THE DOMINANT RISK to a Tier-2 result in 2D Boussinesq: unlike 1D gCLM (fully
resolved at N<=4096), the Hou-Luo singularity is a corner collapse that Luo-Hou
needed adaptive meshing (~1e12 effective resolution) to track. On a uniform grid
the vorticity sharpens below grid scale before T*. So BEFORE building the genome
+ GA, this cheap probe answers the pre-committed question:

  At feasible uniform N, is there a resolution-STABLE fitness signal for
  buoyancy-driven vorticity growth -- i.e. a quantity measured inside the
  trustworthy (tail-resolved) window that CONVERGES as N grows?

  - YES  -> the search has a resolution-stable signal even though the full
            singularity is out of reach; proceed to Gate 3/4 with that fitness.
  - RAILS -> the flow is under-resolved even in its "resolved" window; uniform-
            grid Tier-2 is resolution-starved for this model -> STOP and re-plan
            (coarser honest deliverable, or AMR / Route D) BEFORE the genome.

Trust instrument: solver tail_guard (stop "under_resolved" when enstrophy piles
near the 2/3 dealias cut) -- conservation drift stays tiny under-resolution, the
spectral tail does not. Each run reports the trustworthy window (t_res, amp_res)
and max|w| at fixed probe times common to all resolutions; the fitness proxy is
the log-growth rate over a fixed window inside every resolution's resolved range.

Usage:
    .venv/bin/python phase1_resolution_spike.py --workers 8
    .venv/bin/python phase1_resolution_spike.py --smoke
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import json
import multiprocessing
import sys
import time
from datetime import datetime, timezone

import numpy as np

from ga.genome2d import realize_holder_density_2d, realize_holder_vorticity_2d
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.boussinesq import grid2d, solve_boussinesq
from win_condition import InsufficientDataError, estimate_blowup_time

RESOLUTIONS = (128, 256, 512, 1024)
PROBE_TIMES = (1.0, 1.5, 2.0, 2.3)   # inside the coarsest resolved window (~2.46)
GROWTH_WINDOW = (1.5, 2.3)           # fixed window for the log-growth-rate fitness
TAIL_GUARD = 1e-3
T_MAX = 6.0
AMPLIFICATION = 1e5                   # never reached; the tail guard stops first
MAX_STEPS = 4000
DT_MAX = 1e-2


def build_ics():
    """Roster (picklable specs; fields built in the worker by realize_ic): smooth
    Luo-Hou-type growers (the clean resolvability test) and genuine C^{0,h} rough
    data (harder to resolve on a uniform grid)."""
    return [
        {"label": "smooth_sharp", "kind": "smooth"},
        {"label": "smooth_mild", "kind": "smooth"},
        {"label": "rough_h0.5", "kind": "rough", "h": 0.5},
        {"label": "rough_h0.3", "kind": "rough", "h": 0.3},
    ]


def realize_ic(ic, n):
    if ic["kind"] == "rough":
        return (realize_holder_vorticity_2d(ic["h"], n),
                realize_holder_density_2d(ic["h"], n))
    X, Y = grid2d(n)
    if ic["label"] == "smooth_sharp":
        return 0.2 * np.sin(X) * np.sin(Y), (1.0 + np.cos(2 * X)) * np.sin(2 * Y)
    if ic["label"] == "smooth_mild":
        return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)
    raise ValueError(f"unknown IC {ic['label']}")


def _interp(times, values, tq):
    """max|w| at query time tq (nan if the run ended before tq)."""
    times = np.asarray(times)
    if tq > times[-1]:
        return float("nan")
    return float(np.interp(tq, times, values))


def run_task(task):
    ic, n = task["ic"], task["n"]
    w0, th0 = realize_ic(ic, n)
    t0 = time.perf_counter()
    r = solve_boussinesq(w0, th0, nu=0.0, t_max=T_MAX, buoyancy=True,
                         symmetry="houluo", amplification_factor=AMPLIFICATION,
                         tail_guard=TAIL_GUARD, max_steps=MAX_STEPS, dt_max=DT_MAX)
    times, mom = r.times.tolist(), r.max_omega.tolist()
    m0 = mom[0]
    probes = {f"{tq:.1f}": (_interp(times, mom, tq) / m0) for tq in PROBE_TIMES}
    # Fixed-window log-growth-rate fitness proxy: mean d/dt log max|w| on
    # GROWTH_WINDOW, defined only if the run stayed resolved through it.
    t1, t2 = GROWTH_WINDOW
    if times[-1] >= t2:
        a1, a2 = _interp(times, mom, t1), _interp(times, mom, t2)
        growth_rate = (np.log(a2) - np.log(a1)) / (t2 - t1)
    else:
        growth_rate = float("nan")
    # Exponent estimate over the resolved series (may rail; that is the point).
    est = None
    try:
        e = estimate_blowup_time(times, mom, tail_fraction=0.5, fit_exponent=True)
        if e is not None:
            est = {"t_star": float(e.t_star), "exponent": float(e.exponent),
                   "r_squared": float(e.r_squared)}
    except InsufficientDataError:
        est = None
    return {
        "schema_version": SCHEMA_VERSION,
        "sweep": "phase1_resolution_spike",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "ic_label": ic["label"],
        "ic_kind": ic["kind"],
        "resolution_N": n,
        "outcome": r.outcome,
        "t_resolved": float(r.t_final),
        "amp_resolved": float(mom[-1] / m0),
        "max_tail_fraction": float(r.max_tail_fraction),
        "conservation_drift": float(r.conservation_drift),
        "n_timesteps": int(r.n_timesteps),
        "probe_amp": probes,
        "growth_rate_fixed_window": float(growth_rate),
        "estimate": est,
        "wall_clock_seconds": time.perf_counter() - t0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_resolution_spike.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    code_ver = code_version()

    ics = build_ics()
    resolutions = RESOLUTIONS
    if args.smoke:
        ics, resolutions = ics[:1], (128, 256)

    tasks = [{"ic": ic, "n": n, "code_version": code_ver, "code_dirty": dirty}
             for ic in ics for n in resolutions]
    tasks.sort(key=lambda t: -t["n"])  # biggest grids first
    print(f"{len(ics)} ICs x {len(resolutions)} resolutions = {len(tasks)} runs "
          f"(tail_guard={TAIL_GUARD:g}, N up to {max(resolutions)}) "
          f"on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    t0 = time.perf_counter()
    done = 0
    with open(args.out, "a") as f:
        pool = multiprocessing.get_context().Pool(args.workers) if args.workers > 0 else None
        it = pool.imap_unordered(run_task, tasks, chunksize=1) if pool else map(run_task, tasks)
        try:
            for row in it:
                f.write(json.dumps(row) + "\n"); f.flush(); os.fsync(f.fileno())
                done += 1
                e = row["estimate"]
                edesc = "no-fit" if e is None else f"a={e['exponent']:.2f} T*={e['t_star']:.1f} R2={e['r_squared']:.2f}"
                print(f"[{done:2d}/{len(tasks)}] {row['ic_label']:12s} N={row['resolution_N']:4d} "
                      f"{row['outcome']:14s} t_res={row['t_resolved']:.2f} amp={row['amp_resolved']:7.1f} "
                      f"g={row['growth_rate_fixed_window']:.3f} tail={row['max_tail_fraction']:.1e} "
                      f"[{edesc}] ({row['wall_clock_seconds']:.0f}s)", flush=True)
        finally:
            if pool:
                pool.close(); pool.join()
    print(f"\nSpike complete: {done} runs in {time.perf_counter()-t0:.0f}s -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
