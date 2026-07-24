"""One-more-currency probe (user decision after Gate 4): does an INVISCID,
omega0-independent growth-rate currency escape the dissipation-scaling wall that
killed the nu_crit viscosity-resistance fitness (PHASE1_GATE4_RESULTS.md)?

Why this currency. nu_crit is fatally organized by the nu*k^2 dissipation scaling
BECAUSE it is a measure about viscosity -- any viscosity-resistance fitness
inherits that trivial low-k optimum (confirmed raw / fixed-split / normalized).
Two design changes escape both cheats at once:
  - measure INVISCID (nu=0): no nu*k^2 term, so no dissipation-scaling triviality.
  - use a growth RATE (a log-derivative), NOT an amplification ratio: a rate over
    a mid-run window [t1,t2], t1>0, does not divide by max|omega0|, so it cannot
    be gamed by shrinking omega0 (the amp-denominator cheat).
The spike showed the fixed-window inviscid rate is resolution-stable; the axis
screen showed the EARLY-window rate mis-ranks (mild starts fast then saturates).
So the currency is the SUSTAINED (late-window) inviscid growth rate:

  g_sustained = [log max|w|(t_res) - log max|w|(0.5*t_res)] / (0.5*t_res)

measured inside the tail_guard-trusted window [.,t_res]. High for accelerating
(singularity-approaching) shapes, low for saturating ones, ~0 for non-growers.

Three legs (the axis-screen legs PLUS the property-6 leg nu_crit failed):
  A. DIRECTION on the labeled ground-truth ICs: g_sustained must order
     smooth_sharp (blows up) > smooth_mild (saturates) > euler_control (flat).
  B. RESOLUTION-STABILITY across N=128,256 on those ICs.
  C. NON-TRIVIAL OPTIMUM on the fixed-split roster (20 shapes): is the g_sustained
     winner STRUCTURED (not low-(1,1)), with weak rho(g,log|w0|) (omega0-indep by
     construction) and NOT a spectral-trivial (centroid-dominated) landscape?

Cheap: one nu=0 solve per shape (no bisection). ~26 solves at N<=256, minutes.

Usage: .venv/bin/python phase1_currency_probe.py --workers 8
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

from ga.genome2d_smooth import realize, shape_descriptors
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from phase1_gate4_probe import build_probe_roster
from solver.boussinesq import grid2d, solve_boussinesq

TAIL_GUARD = 1e-3
T_MAX = 4.0
AMPLIFICATION = 1e5     # never reached; tail_guard stops first
MAX_STEPS = 4000
DT_MAX = 1e-2
LABELED_RES = (128, 256)
ROSTER_RES = 128


def labeled_ic(name, n):
    """The axis-screen labeled ground-truth ICs (raw, not budget-normalized):
    smooth_sharp blows up, smooth_mild saturates, euler_control is a non-grower."""
    X, Y = grid2d(n)
    if name in ("smooth_sharp", "euler_control"):
        return 0.2 * np.sin(X) * np.sin(Y), (1.0 + np.cos(2 * X)) * np.sin(2 * Y)
    if name == "smooth_mild":
        return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)
    raise ValueError(name)


def _interp(times, values, tq):
    times = np.asarray(times)
    return float("nan") if tq > times[-1] else float(np.interp(tq, times, values))


def growth_rate(times, mom, f_lo, f_hi):
    """Log-growth rate of max|w| over the fractional window [f_lo, f_hi] of
    [0, t_res]. omega0-independent for f_lo > 0 (divides by max|w| at f_lo*t_res,
    not max|w0|)."""
    t_res = float(times[-1])
    t1, t2 = f_lo * t_res, f_hi * t_res
    if t2 <= t1 or t_res <= 0:
        return float("nan")
    a1, a2 = _interp(times, mom, t1), _interp(times, mom, t2)
    if not (a1 > 0 and a2 > 0):
        return float("nan")
    return float((np.log(a2) - np.log(a1)) / (t2 - t1))


def measure(w0, th0, buoyancy=True):
    """One nu=0 solve; return the growth-rate diagnostics over the trusted window."""
    r = solve_boussinesq(
        w0, th0, nu=0.0, kappa=0.0, t_max=T_MAX, buoyancy=buoyancy,
        symmetry="houluo", amplification_factor=AMPLIFICATION,
        tail_guard=TAIL_GUARD, max_steps=MAX_STEPS, dt_max=DT_MAX)
    t, m = r.times, r.max_omega
    return {
        "g_sustained": growth_rate(t, m, 0.5, 1.0),   # the currency
        "g_early": growth_rate(t, m, 0.0, 0.5),        # the known-mis-ranking axis
        "g_full": growth_rate(t, m, 0.1, 1.0),
        "t_res": float(r.t_final),
        "amp_res": float(m[-1] / m[0]),
        "max_w0": float(np.max(np.abs(w0))),
        "outcome": r.outcome,
    }


def run_labeled(task):
    name, n = task["name"], task["n"]
    w0, th0 = labeled_ic(name, n)
    d = measure(w0, th0, buoyancy=(name != "euler_control"))
    return {"leg": "direction", "label": name, "resolution_N": n, **d,
            **_meta(task)}


def run_roster(task):
    g = task["genome"]
    w0, th0 = realize(g, ROSTER_RES)
    d = measure(w0, th0, buoyancy=True)
    return {"leg": "optimum", "label": task["label"], "shape_class": task["cls"],
            "resolution_N": ROSTER_RES, "descriptors": shape_descriptors(g), **d,
            **_meta(task)}


def _meta(task):
    return {"schema_version": SCHEMA_VERSION, "sweep": "phase1_currency_probe",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "code_version": task["code_version"], "code_dirty": task["code_dirty"]}


def _rho(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    ok = np.isfinite(xs) & np.isfinite(ys)
    if ok.sum() < 3 or np.std(xs[ok]) == 0 or np.std(ys[ok]) == 0:
        return float("nan")
    return float(np.corrcoef(xs[ok], ys[ok])[0, 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_currency_probe.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not args.allow_dirty:
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    base = dict(code_version=code_version(), code_dirty=dirty)

    labeled = [dict(name=nm, n=n, **base)
               for nm in ("smooth_sharp", "smooth_mild", "euler_control")
               for n in LABELED_RES]
    roster = [dict(**s, **base) for s in build_probe_roster()]  # split fixed 0.5
    print(f"Currency probe: {len(labeled)} labeled runs + {len(roster)} roster "
          f"runs (inviscid, split-fixed roster) on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    lab_rows, ros_rows = [], []
    with open(args.out, "a") as f:
        pool = multiprocessing.get_context().Pool(args.workers)
        try:
            for row in pool.imap_unordered(run_labeled, labeled, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush()
                lab_rows.append(row)
            for row in pool.imap_unordered(run_roster, roster, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush()
                ros_rows.append(row)
        finally:
            pool.close(); pool.join()

    # --- Leg A/B: direction + resolution stability on labeled ICs ---
    print("\n=== LEG A/B: direction + resolution-stability (labeled ICs, g_sustained) ===")
    by = {}
    for r in lab_rows:
        by.setdefault(r["label"], {})[r["resolution_N"]] = r
    for nm in ("smooth_sharp", "smooth_mild", "euler_control"):
        cols = " ".join(f"N={n}:g_sus={by[nm][n]['g_sustained']:+.3f}"
                        f"(amp={by[nm][n]['amp_res']:.1f},g_early={by[nm][n]['g_early']:+.2f})"
                        for n in LABELED_RES if n in by[nm])
        print(f"  {nm:14s} {cols}")
    gs = {nm: by[nm][LABELED_RES[-1]]['g_sustained'] for nm in by}
    direction_ok = gs['smooth_sharp'] > gs['smooth_mild'] > gs['euler_control']
    print(f"  DIRECTION sharp>mild>control: {direction_ok} "
          f"({gs['smooth_sharp']:+.3f} > {gs['smooth_mild']:+.3f} > {gs['euler_control']:+.3f})")

    # --- Leg C: non-trivial optimum on the split-fixed roster ---
    print("\n=== LEG C: non-trivial optimum (split-fixed roster, g_sustained) ===")
    g = [r for r in ros_rows if np.isfinite(r["g_sustained"])]
    g.sort(key=lambda r: -r["g_sustained"])
    gsus = [r["g_sustained"] for r in g]
    cen = [r["descriptors"]["centroid"] for r in g]
    lw0 = np.log([r["max_w0"] for r in g])
    ani = [r["descriptors"]["anisotropy"] for r in g]
    win = g[0]
    print(f"  winner: {win['label']}[{win['shape_class']}] "
          f"g_sus={win['g_sustained']:+.3f} centroid={win['descriptors']['centroid']:.2f}")
    print(f"  rho(g_sus, log|w0|)   = {_rho(gsus, lw0):+.3f}  (near 0 => omega0-independent, as designed)")
    print(f"  rho(g_sus, centroid)  = {_rho(gsus, cen):+.3f}  (strong NEG => dissipation-scaling-like triviality)")
    print(f"  rho(g_sus, anisotropy)= {_rho(gsus, ani):+.3f}")
    print(f"  top-5: " + ", ".join(f"{r['label']}[{r['shape_class'][:4]}]={r['g_sustained']:+.3f}"
                                    for r in g[:5]))
    print(f"\n-> {args.out}", flush=True)


if __name__ == "__main__":
    main()
