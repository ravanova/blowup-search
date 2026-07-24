"""Gate 4 — the NON-NEGOTIABLE six-property viability gate on the nu_crit-analog
fitness, over a ~40-shape roster, BEFORE any GA campaign (PHASE1_PLAN.md Gate 4).

The pre-Gate-4 axis screen (PHASE1_AXIS_SCREEN_RESULTS.md) cleared only two legs
(direction + resolution-stability) on 3 labeled ICs. This gate re-runs the full
inherited six-property checklist (Stage 1.5's five: nonzero, finite, monotone,
resolution-stable, wide-band; plus Stage 2's non-trivial-optimum) on the smooth
2D genome fitness. Pre-committing the predicate + roster is what makes a RAIL a
FINDING, not a push-harder signal -- the same discipline as Stages 2.5 / 3.5 /
3.6 and the axis screen. If property 6 rails as the 1D gCLM nu_crit did (its
optimum collapsed to trivial low-mode concentration; STAGE_2_5_RESULTS.md), STOP.

THE FITNESS (frozen, from the screen): nu_crit = viscosity at which net resolved
amplification amp = max|w|(t_res)/max|w|(0) crosses A_CRIT=2x, kappa=0, inside the
tail_guard-trusted window. Higher nu_crit = harder to kill = more blow-up prone.
Wired through ga/fitness2d.py (reuses ga.fitness.bisect_critical + v3 predicate).

ROSTER (40 shapes) designed to TEST property 6, not dodge it:
  - control (3): a non-buoyant Euler shape (censor-low anchor -- the axis must
    respond to buoyancy, not merely to carrying a vortex) + the two axis-screen
    benchmark growers (sharp, mild) as validated references.
  - trivial (6): omega concentrated at the lowest (1,1) mode (minimum centroid) --
    the 2D analog of the k=1 energy-concentration cheat that killed gCLM. Because
    nu_crit ~ 1/k^2 (dissipation scaling), "dump energy in (1,1)" trivially
    maximizes nu_crit; if these shapes WIN the landscape, property 6 fails.
  - structured (3): higher-centroid multi-mode omega that COULD out-resist the
    trivial concentrations if resistance is more than the dissipation scaling.
  - random (28): random genomes spanning centroid x anisotropy x split, so the
    property-6 correlation rho(nu_crit, centroid) is measurable over a real spread.

RESOLUTION / PERFORMANCE. Every shape at N=256 (cold) AND N=512 -- the full
roster at both, so property 6's verdict rests on nu_crit values that are ALL
resolution-confirmed (especially the high-nu_crit winners it scrutinizes). The
full 40xN=512 would be ~21h of cold bisections; three levers bring it to ~2.5h:
  1. Warm-start each N=512 bisection from that shape's N=256 nu_crit (a stable
     shape converges in ~7 runs not ~11; an UNSTABLE shape fails a bracket edge
     and EXPANDS to find the true value -- so warm-starting is cheap for the
     common case WITHOUT hiding instability, which is exactly the property-4 red
     flag we want to see).
  2. Skip the monotonicity probes at N=512 (property 3 is decided at N=256; N=512
     only needs the critical value for property 4).
  3. 8 workers (top of the 6-8 band for 12 cores at OMP_NUM_THREADS=1).

Single-writer JSONL (workers return payloads; the parent writes), same as the
axis screen. Analysis + the frozen pass/fail predicate: analyze_phase1_gate4.py.

Usage:
    .venv/bin/python phase1_gate4.py --workers 8
    .venv/bin/python phase1_gate4.py --smoke
Then: .venv/bin/python analyze_phase1_gate4.py
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

from ga.fitness2d import FITNESS2D_DEFAULTS, nu_crit_from_genome
from ga.genome2d_smooth import DEFAULT_K, Genome2D, random_genome, shape_descriptors
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty

RESOLUTIONS = (256, 512)      # full roster at both; N=512 warm-started from N=256
SMOKE_RESOLUTIONS = (128,)
WARM_MARGIN = 0.08            # tight bracket for the warm N=512 confirmation
RANDOM_ROOT_SEED = 20260724
K = DEFAULT_K

# The frozen bisection tolerance (also the analysis unit "tol").
NU_TOL = FITNESS2D_DEFAULTS["bisection"]["tolerance"]


def _mk(a_modes, b_modes):
    """Genome2D from explicit modes. a_modes: {(j,k): coeff} for omega sin(jx)sin(ky),
    j,k in 1..K. b_modes: {(j,k): coeff} for theta cos(jx)sin(ky), j in 0..K, k in 1..K."""
    a = np.zeros((K, K))
    b = np.zeros((K + 1, K))
    for (j, k), v in a_modes.items():
        a[j - 1, k - 1] = v
    for (j, k), v in b_modes.items():
        b[j, k - 1] = v
    return Genome2D(a=a, b=b)


# Axis-screen benchmark SHAPES (renormalized to the genome budget in realize()).
_SHARP = ({(1, 1): 0.2}, {(0, 2): 1.0, (2, 2): 1.0})  # w=0.2 sinx siny, th=(1+cos2x)sin2y
_MILD = ({(1, 1): 1.0}, {(1, 1): 1.0})                 # w=sinx siny, th=cosx siny


def build_roster():
    """The frozen 40-shape roster (deterministic). Each entry: label, class,
    buoyancy, Genome2D."""
    roster = []

    # --- controls (3) ---
    roster.append(dict(label="ctrl_euler", cls="control", buoyancy=False,
                       genome=_mk(*_SHARP)))          # buoyancy off: censor-low anchor
    roster.append(dict(label="ctrl_sharp", cls="control", buoyancy=True,
                       genome=_mk(*_SHARP)))
    roster.append(dict(label="ctrl_mild", cls="control", buoyancy=True,
                       genome=_mk(*_MILD)))

    # --- trivial-cheat: omega pure (1,1) (min centroid), varied theta (6) ---
    trivial_thetas = {
        "triv_th11": {(1, 1): 1.0},
        "triv_sharpth": {(0, 2): 1.0, (2, 2): 1.0},
        "triv_lowsplit": {(1, 1): 0.3},
        "triv_th31": {(3, 1): 1.0},
        "triv_th01": {(0, 1): 1.0},
        "triv_th13": {(1, 3): 1.0},
    }
    for name, th in trivial_thetas.items():
        roster.append(dict(label=name, cls="trivial", buoyancy=True,
                           genome=_mk({(1, 1): 1.0}, th)))

    # --- structured: higher-centroid multi-mode omega (3) ---
    roster.append(dict(label="struct_diag", cls="structured", buoyancy=True,
                       genome=_mk({(1, 1): 1.0, (3, 3): 0.8}, {(0, 2): 1.0, (2, 2): 1.0})))
    roster.append(dict(label="struct_aniso", cls="structured", buoyancy=True,
                       genome=_mk({(2, 2): 1.0, (1, 3): 0.7}, {(1, 1): 1.0, (2, 2): 0.5})))
    roster.append(dict(label="struct_high", cls="structured", buoyancy=True,
                       genome=_mk({(3, 1): 1.0, (2, 2): 0.6}, {(0, 2): 1.0, (2, 2): 1.0})))

    # --- random spread, filling to 40 ---
    rng = np.random.default_rng(RANDOM_ROOT_SEED)
    n_random = 40 - len(roster)
    for i in range(n_random):
        roster.append(dict(label=f"rand_{i:02d}", cls="random", buoyancy=True,
                           genome=random_genome(rng)))
    return roster


def run_task(task):
    """Worker: one nu_crit bisection for (shape, resolution). Warm-started at
    N=512 from the shape's N=256 critical value (task['warm_center'])."""
    g = task["genome"]
    n = task["n"]
    t0 = time.perf_counter()
    bis = nu_crit_from_genome(g, n, config=task.get("config"),
                              buoyancy=task["buoyancy"],
                              warm_center=task.get("warm_center"))
    runs = bis["runs"]
    by_nu = sorted(runs, key=lambda r: r["param"])
    amp_lo = by_nu[0].get("amp") if by_nu else None
    amp_hi = by_nu[-1].get("amp") if by_nu else None
    mprobes = bis.get("monotone_probes") or []
    return {
        "schema_version": SCHEMA_VERSION,
        "sweep": "phase1_gate4",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "label": task["label"],
        "shape_class": task["cls"],
        "buoyancy": task["buoyancy"],
        "resolution_N": n,
        "warm_center": task.get("warm_center"),
        "nu_crit": bis["critical_value"],
        "bracket_censored": bis["bracket_censored"],
        "critical_value_monotone": bis["critical_value_monotone"],
        "n_monotone_probes": len(mprobes),
        "n_monotone_violations": int(sum(1 for p in mprobes if p["blowup"])),
        "n_bracket_expansions": bis["n_bracket_expansions"],
        "n_bisection_steps": bis["n_bisection_steps"],
        "n_solver_runs": len(runs),
        "amp_at_nu_lo": amp_lo,
        "amp_at_nu_hi": amp_hi,
        "descriptors": shape_descriptors(g),
        "max_tail_fraction": max((r.get("max_tail_fraction", 0.0) for r in runs),
                                 default=0.0),
        "max_conservation_drift": max((r.get("conservation_drift", 0.0) for r in runs),
                                      default=0.0),
        "wall_clock_seconds": time.perf_counter() - t0,
    }


def _run_phase(tasks, workers, out_f, total, done0):
    """Run one phase of tasks through the pool, writing rows as they return.
    Returns (rows, done_count)."""
    rows = []
    done = done0
    pool = multiprocessing.get_context().Pool(workers) if workers > 0 else None
    it = pool.imap_unordered(run_task, tasks, chunksize=1) if pool else map(run_task, tasks)
    try:
        for row in it:
            out_f.write(json.dumps(row) + "\n"); out_f.flush(); os.fsync(out_f.fileno())
            rows.append(row)
            done += 1
            cens = row["bracket_censored"] or ""
            warm = "" if row["warm_center"] is None else f" warm={row['warm_center']:.4f}"
            amp = row["amp_at_nu_lo"]
            amps = "   nan" if amp is None else f"{amp:6.1f}"
            print(f"[{done}/{total}] {row['label']:16s} N={row['resolution_N']:4d} "
                  f"nu_crit={row['nu_crit']:.4f}{cens:>5s}{warm} "
                  f"(amp@lo={amps}, {row['n_solver_runs']:2d} runs, "
                  f"{row['wall_clock_seconds']:.0f}s)", flush=True)
    finally:
        if pool:
            pool.close(); pool.join()
    return rows, done


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_gate4.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    code_ver = code_version()

    roster = build_roster()
    resolutions = RESOLUTIONS
    if args.smoke:
        # a fast subset that exercises every code path: controls + one trivial,
        # single resolution, no warm phase.
        roster = [s for s in roster if s["cls"] == "control"] + \
                 [s for s in roster if s["label"] == "triv_th11"]
        resolutions = SMOKE_RESOLUTIONS

    base = dict(code_version=code_ver, code_dirty=dirty)
    n1 = resolutions[0]
    tasks1 = [dict(**s, n=n1, warm_center=None, **base) for s in roster]

    total = len(roster) * len(resolutions)
    print(f"Gate 4: {len(roster)} shapes x {len(resolutions)} N = {total} bisections "
          f"(nu in {FITNESS2D_DEFAULTS['bisection']['range']}, tol={NU_TOL:g}, "
          f"A_CRIT={FITNESS2D_DEFAULTS['A_CRIT']}, tail_guard="
          f"{FITNESS2D_DEFAULTS['tail_guard']:g}) on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    t0 = time.perf_counter()
    with open(args.out, "a") as f:
        # Phase 1: cold at the coarse resolution.
        print(f"\n-- phase 1: N={n1} (cold) --", flush=True)
        rows1, done = _run_phase(tasks1, args.workers, f, total, 0)
        # warm centers = each shape's uncensored N-coarse critical value.
        warm = {r["label"]: r["nu_crit"] for r in rows1
                if r["bracket_censored"] is None}

        # Phase 2: warm at the fine resolution (skip in smoke).
        if len(resolutions) > 1:
            n2 = resolutions[1]
            warm_cfg = {"bisection": {"warm_start": {"margin": WARM_MARGIN},
                                      "probe_fractions": []}}
            print(f"\n-- phase 2: N={n2} (warm from N={n1}, margin={WARM_MARGIN}, "
                  f"no probes) --", flush=True)
            tasks2 = [dict(**s, n=n2, warm_center=warm.get(s["label"]),
                           config=warm_cfg, **base) for s in roster]
            _run_phase(tasks2, args.workers, f, total, done)

    print(f"\nGate 4 complete: {total} bisections in {time.perf_counter()-t0:.0f}s "
          f"-> {args.out}\nNext: .venv/bin/python analyze_phase1_gate4.py", flush=True)


if __name__ == "__main__":
    main()
