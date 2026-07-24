"""Gate-4 property-6 fix probe: is the failure rescuable by removing the omega0
amplitude cheat, or is the amp-ratio currency itself confounded? (Decides
fix-vs-accept on data, not priors -- same discipline as the axis screen.)

Gate 4 verdict (PHASE1_GATE4_RESULTS.md): nu_crit ~ |omega0|^-2
(rho(nu_crit, log|w0|) = -0.90; two shapes reaching the same ABSOLUTE vorticity
get a 197x nu_crit gap purely from their baseline omega0). The smooth genome's
free omega/theta split lets the "optimum" drive omega0 -> 0, trivially inflating
amp = max|w|/max|w0|, while the undamped theta reservoir (kappa=0) re-forces w
regardless of viscosity. That is the property-6 trivial optimum, in a disguise
the frozen (centroid-based) predicate did not test.

THIS PROBE fixes the split at SPLIT=0.5 (equal omega/theta energy), which pins
omega0's SCALE so it can no longer be driven to zero by the cheat knob, then
re-measures nu_crit on a trivial-vs-structured roster. Two questions:

  Q1 (is the split knob the whole cheat?): with split fixed, is the residual
     rho(nu_crit, log|w0|) now weak? (omega0 still varies with SHAPE at fixed
     energy -- a single concentrated mode peaks higher than a spread one -- so a
     residual amp-currency confound can persist even here.)
  Q2 (is there a genuine STRUCTURE signal?): does nu_crit now discriminate by
     centroid/anisotropy with a NON-trivial optimum (a structured, not a pure
     low-(1,1), winner), and NOT via the centroid dissipation scaling
     (rho(nu_crit, centroid) not strongly negative)?

Outcomes: both good -> constraining split rescues the axis (pursue the fix).
Q1 still confounded or Q2 flat -> the amp-ratio currency itself is the problem
-> deeper redesign or accept-the-negative. Cheap: ~20 shapes at N=128 (resolution
stability already established over 36 shapes in Gate 4), a few minutes.

Usage: .venv/bin/python phase1_gate4_probe.py --workers 8
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

from ga.fitness2d import nu_crit_from_genome
from ga.genome2d_smooth import (
    Genome2D,
    _raw_energies,
    random_genome,
    realize,
    shape_descriptors,
)
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty

SPLIT = 0.5           # frozen: equal omega/theta energy -> pins omega0 scale
N = 128               # resolution-stability already established in Gate 4
RANDOM_ROOT_SEED = 20260724
K = 4


def force_split(genome, target=SPLIT):
    """Rescale a (omega) and b (theta) so their energies are in ratio
    (1-target):target; realize() then joint-normalizes the total to the budget,
    giving E_omega=(1-target)*TOTAL, E_theta=target*TOTAL exactly. Removes the
    genome's free-split omega0-shrinking knob."""
    e_om, e_th = _raw_energies(genome)
    if e_om <= 0 or e_th <= 0:
        raise ValueError("need nonzero omega and theta to fix a split")
    sa = np.sqrt((1.0 - target) / e_om)
    sb = np.sqrt(target / e_th)
    return Genome2D(a=genome.a * sa, b=genome.b * sb)


def _mk(a_modes, b_modes):
    a = np.zeros((K, K)); b = np.zeros((K + 1, K))
    for (j, k), v in a_modes.items():
        a[j - 1, k - 1] = v
    for (j, k), v in b_modes.items():
        b[j, k - 1] = v
    return Genome2D(a=a, b=b)


def build_probe_roster():
    """Trivial (low-(1,1) centroid) vs structured (higher centroid) vs random,
    ALL forced to split=0.5. Tests property 6 with the split-cheat removed."""
    roster = []
    # trivial: omega pure (1,1) (min centroid), varied theta
    for name, th in {
        "triv_th11": {(1, 1): 1.0},
        "triv_th22": {(2, 2): 1.0},
        "triv_th31": {(3, 1): 1.0},
        "triv_sharpth": {(0, 2): 1.0, (2, 2): 1.0},
    }.items():
        roster.append(dict(label=name, cls="trivial",
                           genome=_mk({(1, 1): 1.0}, th)))
    # structured: higher-centroid multi-mode omega
    for name, aa in {
        "struct_diag": {(1, 1): 1.0, (3, 3): 0.8},
        "struct_aniso": {(2, 2): 1.0, (1, 3): 0.7},
        "struct_high": {(3, 1): 1.0, (2, 2): 0.6},
        "struct_33": {(3, 3): 1.0},
    }.items():
        roster.append(dict(label=name, cls="structured",
                           genome=_mk(aa, {(0, 2): 1.0, (2, 2): 1.0})))
    # random spread, filling to 20
    rng = np.random.default_rng(RANDOM_ROOT_SEED)
    while len(roster) < 20:
        i = len([r for r in roster if r["cls"] == "random"])
        roster.append(dict(label=f"rand_{i:02d}", cls="random",
                           genome=random_genome(rng)))
    # force the split on every shape
    for s in roster:
        s["genome"] = force_split(s["genome"])
    return roster


def run_task(task):
    g = task["genome"]
    t0 = time.perf_counter()
    bis = nu_crit_from_genome(g, N, buoyancy=True)
    runs = bis["runs"]
    by_nu = sorted(runs, key=lambda r: r["param"])
    w0 = float(np.max(np.abs(realize(g, N)[0])))
    return {
        "schema_version": SCHEMA_VERSION,
        "sweep": "phase1_gate4_probe",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "label": task["label"],
        "shape_class": task["cls"],
        "split_fixed": SPLIT,
        "resolution_N": N,
        "nu_crit": bis["critical_value"],
        "bracket_censored": bis["bracket_censored"],
        "max_w0": w0,
        "amp_at_nu_lo": by_nu[0].get("amp") if by_nu else None,
        "n_solver_runs": len(runs),
        "descriptors": shape_descriptors(g),
        "wall_clock_seconds": time.perf_counter() - t0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_gate4_probe.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not args.allow_dirty:
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    code_ver = code_version()

    roster = build_probe_roster()
    base = dict(code_version=code_ver, code_dirty=dirty)
    tasks = [dict(**s, **base) for s in roster]
    print(f"Gate-4 probe: {len(roster)} shapes at N={N}, split fixed={SPLIT}, "
          f"on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    rows = []
    with open(args.out, "a") as f:
        pool = multiprocessing.get_context().Pool(args.workers)
        try:
            for row in pool.imap_unordered(run_task, tasks, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); os.fsync(f.fileno())
                rows.append(row)
                cens = row["bracket_censored"] or ""
                d = row["descriptors"]
                print(f"[{len(rows)}/{len(tasks)}] {row['label']:14s} "
                      f"nu_crit={row['nu_crit']:.4f}{cens:>5s} "
                      f"w0={row['max_w0']:.3f} centroid={d['centroid']:.2f} "
                      f"({row['n_solver_runs']} runs, {row['wall_clock_seconds']:.0f}s)",
                      flush=True)
        finally:
            pool.close(); pool.join()

    # --- inline verdict ---
    g = [r for r in rows if r["bracket_censored"] is None]

    def rho(xs, ys):
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        if len(xs) < 3 or np.std(xs) == 0 or np.std(ys) == 0:
            return float("nan")
        return float(np.corrcoef(xs, ys)[0, 1])

    if len(g) >= 3:
        nu = [r["nu_crit"] for r in g]
        lw0 = np.log([r["max_w0"] for r in g])
        cen = [r["descriptors"]["centroid"] for r in g]
        ani = [r["descriptors"]["anisotropy"] for r in g]
        g.sort(key=lambda r: -r["nu_crit"])
        win = g[0]
        band = (max(nu) - min(nu)) / 5e-3
        print(f"\n--- PROBE VERDICT (split fixed at {SPLIT}, {len(g)} growers) ---")
        print(f"  Q1 residual amp cheat: rho(nu_crit, log|w0|) = {rho(nu, lw0):+.3f} "
              f"(Gate 4 was -0.90; near 0 => split knob WAS the cheat)")
        print(f"  Q2 structure signal:   rho(nu_crit, centroid) = {rho(nu, cen):+.3f} "
              f"(strong NEG => still the dissipation-scaling cheat)")
        print(f"                         rho(nu_crit, anisotropy) = {rho(nu, ani):+.3f}")
        print(f"  wide band: {band:.0f}*tol   winner: {win['label']}[{win['shape_class']}] "
              f"nu={win['nu_crit']:.4f} centroid={win['descriptors']['centroid']:.2f}")
        print(f"  top-5: " + ", ".join(
            f"{r['label']}[{r['shape_class'][:4]}]={r['nu_crit']:.3f}" for r in g[:5]))
    print(f"\n-> {args.out}", flush=True)


if __name__ == "__main__":
    main()
