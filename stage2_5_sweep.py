"""Stage 2.5 fitness-axis redesign sweep (PLAN.md Stage 2.5, candidate A).

Measures nu_crit(t_max=12, N) at FIXED a in {0.4, 0.7, 1.0} — no GA — over:

(a) the Stage 1.5 hand-picked IC set (stage1_5_sweep.build_initial_conditions:
    sines, bumps, spectral tails, seeded k^-1.5 random shapes), and
(b) 20 random genomes drawn from ga/evolve.py's ACTUAL init prior
    (ga.genome.random_genome with the Stage 2 config: N=32 coefficients
    ~ N(0,1), envelope p ~ U[0, 3.5], energy-normalized) — so the
    "non-trivial optimum" property (six-property checklist, property 6) is
    measured against the real prior the GA and baseline_random sample from.

Everything about the oracle is frozen at Stage 2's values (the v2 predicate
from STAGE_1_5_RESULTS.md, implemented in ga.fitness.classify_run):
t_max=12, amplification 100x, tail_fraction 0.15, held-out R^2 floor 0.9,
T* cap 1.5*t_max, early-decay exit (0.1, 2.0), dt policy (1e-2, 0.05, 0.4).
Bisection: ga.fitness.bisect_critical, range [0, 0.1] tolerance 1e-3
(Stage 2's config), cold-started. If a shape is censored HIGH (still blows
up at the top of the range), the range is extended up a ladder
[0, 0.4] -> [0, 1.0] and the extension count recorded — nu_crit at a>0 is
expected BELOW the a=0 band (advection fights growth), so extensions should
be rare; censored LOW (no blow-up even at nu=0) is the live risk near a=1
and is a legitimate sweep outcome (dead axis), detected in 1 run.

Rationale for the a-values (PLAN.md Stage 2.5): at a=1 (De Gregorio) sin(x)
is an equilibrium, so the k=1 refuge that trivialized the a=0 landscape
(STAGE_2_RESULTS.md) should stop paying; a=0.4/0.7 interpolate and keep
most Stage 1.5 shapes alive (their a_crit clustered at 0.85-1.0).
Selection rule: the LARGEST a passing all six properties.

Every row is standalone-reproducible: code_version, seeds, full shape spec
(analytic construction or genome coeffs + envelope p), solver params, and
per-run summaries. Bisections are embarrassingly parallel: each (shape, a,
N) task runs in a worker; the parent is the single JSONL writer.

Usage:
    .venv/bin/python stage2_5_sweep.py --workers 10        # full sweep
    .venv/bin/python stage2_5_sweep.py --smoke             # tiny shakedown
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

from ga.fitness import bisect_critical, classify_run
from ga.genome import (
    ENERGY_BUDGET,
    from_sine_pairs,
    project_to_sines,
    random_genome,
    realize,
    shape_descriptors,
)
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.gclm import solve_gclm
from solver.spectral_utils import energy, grid
from stage1_5_sweep import build_initial_conditions

# --- frozen sweep configuration -------------------------------------------

ROOT_SEED = 20260722          # same project root seed; distinct spawn key below
PRIOR_SPAWN_KEY = 25          # SeedSequence([ROOT_SEED, PRIOR_SPAWN_KEY, i])
N_PRIOR_DRAWS = 20

A_VALUES = (0.4, 0.7, 1.0)
RESOLUTIONS = (256, 512)
T_MAX = 12.0

# Stage 2's frozen genome config (DEFAULT_CONFIG in ga/evolve.py) — the
# init prior must be the GA's real one or property 6 measures nothing.
GENOME_N = 32
ENVELOPE_P_RANGE = (0.0, 3.5)

# Range ladder: start at Stage 2's bisection range; extend only on
# censored-high (unexpected at a>0 — advection weakens blow-up).
NU_RANGE_LADDER = ((0.0, 0.1), (0.0, 0.4), (0.0, 1.0))

# Candidate B (PLAN.md Stage 2.5 fallback): nu_crit at a=0 with the k<=2
# energy fraction capped at normalization. Every shape is represented as a
# length-32 genome (the GA's actual search space) with the cap applied;
# structured profiles with no energy above k=2 are infeasible by
# construction and skipped.
BANDWIDTH_CAP = {"k_max": 2, "max_frac": 0.5}

BISECTION_BASE = {
    "tolerance": 1e-3,
    "tail_fraction": 0.15,
    "predicate_r2_floor": 0.9,
    "t_star_cap_factor": 1.5,
    "warm_start": {"margin": 0.01, "fallback": "full_range"},  # unused (cold)
    "probe_fractions": [0.05, 0.15],
    "max_iters": 30,
}

ORACLE = {
    "t_max": T_MAX,
    "tail_fraction": BISECTION_BASE["tail_fraction"],
    "predicate_r2_floor": BISECTION_BASE["predicate_r2_floor"],
    "t_star_cap_factor": BISECTION_BASE["t_star_cap_factor"],
}

SOLVER_PARAMS = dict(
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    max_steps=200_000,
    amplification_factor=100.0,
    early_decay_exit={"fraction": 0.1, "window": 2.0},
)

N_REFERENCE = 2048  # grid for identity hashes + spectral energy fractions


# --- shape roster ----------------------------------------------------------


def _spectral_fractions(w_ref):
    """k=1, k<=2, and top-4 energy fractions from the reference-grid
    spectrum — the trivially controllable quantities property 6 gates on
    (k=1 dominance for candidate A; pinning at the k<=2 cap boundary for
    candidate B)."""
    w_hat = np.fft.rfft(w_ref)
    e_k = np.abs(w_hat[1:]) ** 2  # k = 1, 2, ...
    total = float(np.sum(e_k))
    e_sorted = np.sort(e_k)[::-1]
    return {
        "energy_k1_frac": float(e_k[0] / total),
        "energy_low2_frac": float((e_k[0] + e_k[1]) / total),
        "energy_top4_frac": float(np.sum(e_sorted[:4]) / total),
    }


def build_shapes(bandwidth_cap=None):
    """Returns a list of shape dicts, each with everything a worker needs
    except the solver grid realization (done per-resolution in the parent,
    since analytic ICs close over lambdas that do not pickle).

    Candidate A (bandwidth_cap None): structured ICs stay analytic.
    Candidate B: EVERY shape becomes a length-GENOME_N genome with the cap
    applied at normalization — the search space the GA would actually run
    in — and cap-infeasible structured profiles are skipped."""
    shapes = []
    x_ref = grid(N_REFERENCE)

    for ic in build_initial_conditions():
        entry = {
            "label": ic["label"],
            "family": ic["family"],
            "source": "stage1_5",
            "spec": ic["spec"],
        }
        if bandwidth_cap is None:
            entry.update(energy=float(ic["energy"]), ic_hash=ic["ic_hash"],
                         spectral=_spectral_fractions(ic["fn"](x_ref)),
                         descriptors=None, _fn=ic["fn"])
        else:
            try:
                if ic["spec"]["type"] == "sine":
                    g = from_sine_pairs(ic["spec"]["pairs"], GENOME_N,
                                        ENERGY_BUDGET, bandwidth_cap)
                else:  # bump
                    g = project_to_sines(ic["fn"], GENOME_N, ENERGY_BUDGET,
                                         bandwidth_cap)
            except ValueError:
                print(f"skipping {ic['label']}: infeasible under bandwidth "
                      "cap (no energy above k=2)", flush=True)
                continue
            w_ref = realize(g, N_REFERENCE, ENERGY_BUDGET, bandwidth_cap)
            entry.update(
                spec=dict(ic["spec"], capped_genome={
                    "coeffs": [float(c) for c in g.coeffs],
                    "envelope_p": float(g.envelope_p)}),
                energy=float(energy(w_ref)),
                ic_hash=hashlib.sha256(w_ref.tobytes()).hexdigest(),
                spectral=_spectral_fractions(w_ref),
                descriptors=shape_descriptors(g, ENERGY_BUDGET, bandwidth_cap),
                _genome=g)
        shapes.append(entry)

    for i in range(N_PRIOR_DRAWS):
        rng = np.random.default_rng(
            np.random.SeedSequence([ROOT_SEED, PRIOR_SPAWN_KEY, i]))
        g = random_genome(rng, GENOME_N, ENVELOPE_P_RANGE, ENERGY_BUDGET,
                          bandwidth_cap)
        w_ref = realize(g, N_REFERENCE, ENERGY_BUDGET, bandwidth_cap)
        shapes.append({
            "label": f"prior(seed={i})",
            "family": "init_prior",
            "source": "init_prior",
            "spec": {
                "type": "genome",
                "coeffs": [float(c) for c in g.coeffs],
                "envelope_p": float(g.envelope_p),
                "seed_spawn": [ROOT_SEED, PRIOR_SPAWN_KEY, i],
            },
            "energy": float(energy(w_ref)),
            "ic_hash": hashlib.sha256(w_ref.tobytes()).hexdigest(),
            "spectral": _spectral_fractions(w_ref),
            "descriptors": shape_descriptors(g, ENERGY_BUDGET, bandwidth_cap),
            "_genome": g,
        })
    return shapes


def realize_shape(shape, n_res, bandwidth_cap=None):
    if "_genome" in shape:
        return realize(shape["_genome"], n_res, ENERGY_BUDGET, bandwidth_cap)
    return shape["_fn"](grid(n_res))


# --- one bisection task (worker) -------------------------------------------


def run_task(task):
    """One (shape, a, N) nu_crit bisection with the range ladder.

    task: {omega0 (ndarray), a, n_res, meta (JSON-safe shape info)}.
    Returns the finished JSONL row (parent writes it)."""
    omega0 = task["omega0"]
    a = float(task["a"])
    t0 = time.perf_counter()

    def run_at(nu):
        return classify_run(
            solve_gclm(omega0, a=a, nu=float(nu), t_max=T_MAX, **SOLVER_PARAMS),
            ORACLE)

    n_extensions = 0
    for lo, hi in NU_RANGE_LADDER:
        bisection = dict(BISECTION_BASE, range=[lo, hi])
        bis = bisect_critical(run_at, bisection, warm_center=None)
        if bis["bracket_censored"] != "high":
            break
        n_extensions += 1
    nu_range = [lo, hi]

    runs = bis.pop("runs")
    blowup_drifts = [r["conservation_drift"] for r in runs if r["blowup"]]
    row = {
        "schema_version": SCHEMA_VERSION,
        "sweep": "stage2_5",
        "candidate": task["candidate"],
        "bandwidth_cap": task["bandwidth_cap"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "root_seed": ROOT_SEED,
        "ic": task["meta"],
        "axis": "nu",
        "fixed": {"a": a},
        "resolution_N": int(task["n_res"]),
        "t_max": T_MAX,
        "range": nu_range,
        "n_range_extensions": n_extensions,
        "range_ladder": [list(r) for r in NU_RANGE_LADDER],
        "tolerance": BISECTION_BASE["tolerance"],
        "tail_fraction": BISECTION_BASE["tail_fraction"],
        "predicate_r2_floor": BISECTION_BASE["predicate_r2_floor"],
        "t_star_cap_factor": BISECTION_BASE["t_star_cap_factor"],
        "solver_params": {k: v for k, v in SOLVER_PARAMS.items()},
        **{k: bis[k] for k in (
            "critical_value", "bracket_censored", "initial_bracket",
            "n_bracket_expansions", "n_bisection_steps",
            "critical_value_monotone", "monotone_probes")},
        "n_runs": len(runs),
        "n_fit_below_floor": sum(r["fit_below_floor"] for r in runs),
        "max_conservation_drift_blowup_runs":
            max(blowup_drifts) if blowup_drifts else None,
        "wall_clock_seconds": time.perf_counter() - t0,
        "runs": runs,
    }
    return row


# --- sweep driver (parent = single writer) ---------------------------------


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--candidate-b", action="store_true",
                    help="fallback axis: nu_crit at a=0 with the k<=2 "
                         "bandwidth cap applied to every shape")
    ap.add_argument("--smoke", action="store_true",
                    help="2 shapes, one a, N=128, coarse tol — shakedown")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty "
                 "to mark rows non-reproducible)")
    code_ver = code_version()

    if args.candidate_b:
        candidate, cap, a_values = "B", BANDWIDTH_CAP, (0.0,)
        out_path = args.out or "experiments/stage2_5_sweep_b.jsonl"
    else:
        candidate, cap, a_values = "A", None, A_VALUES
        out_path = args.out or "experiments/stage2_5_sweep.jsonl"
    shapes = build_shapes(cap)
    resolutions = RESOLUTIONS
    if args.smoke:
        shapes = [shapes[0], shapes[-1]]
        a_values, resolutions = (a_values[-1],), (128,)
        BISECTION_BASE["tolerance"] = 0.0125

    tasks = []
    for shape in shapes:
        meta = {k: shape[k] for k in ("label", "family", "source", "spec",
                                      "energy", "ic_hash", "spectral",
                                      "descriptors")}
        for n_res in resolutions:
            omega0 = realize_shape(shape, n_res, cap)
            for a in a_values:
                tasks.append({"omega0": omega0, "a": a, "n_res": n_res,
                              "meta": meta, "code_version": code_ver,
                              "code_dirty": dirty, "candidate": candidate,
                              "bandwidth_cap": cap})

    # Interleave so slow clusters (one shape at one N across a-values) don't
    # serialize at the tail of the pool.
    print(f"{len(shapes)} shapes x {len(a_values)} a-values x "
          f"{len(resolutions)} resolutions = {len(tasks)} bisections "
          f"on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    t0 = time.perf_counter()
    done = 0
    with open(out_path, "a") as out_file:
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
                cens = row["bracket_censored"]
                print(f"[{done:3d}/{len(tasks)}] "
                      f"{row['ic']['label']:24s} a={row['fixed']['a']:.1f} "
                      f"N={row['resolution_N']:4d} nu_crit = "
                      f"{row['critical_value']:.4f}"
                      f"{' (censored ' + cens + ')' if cens else ''} "
                      f"monotone={row['critical_value_monotone']} "
                      f"runs={row['n_runs']} "
                      f"({row['wall_clock_seconds']:.1f}s)", flush=True)
        finally:
            if pool is not None:
                pool.close()
                pool.join()
    print(f"\nSweep complete: {done} bisections in "
          f"{time.perf_counter() - t0:.0f}s -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
