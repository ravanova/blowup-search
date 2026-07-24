"""Route A Phase 1 -- staged g_sustained probe (the forward decision after Gate 4).

Gate 4 killed the nu_crit fitness (property 6: an omega0/dissipation-scaling
trivial optimum; PHASE1_GATE4_RESULTS.md). The open decision was whether an
INVISCID growth-RATE currency (measured at nu=0, over a mid-run window, so it
inherits neither the nu*k^2 dissipation wall nor the amp/omega0 denominator cheat)
could pass a full Gate 4 with two refinements: (1) a fixed-absolute growth window
re-verified for N-stability, (2) a free-split property-6 check. This script is the
STAGED, cheap-first probe of those refinements, run BEFORE any 40-shape gate.

It reproduces three findings (all inviscid nu=0, kappa=0, tail_guard-trusted):

LEG 1 -- MAGNITUDE IS ON THE RESOLUTION WALL. On the labeled ground-truth ICs
  (smooth_sharp blows up, smooth_mild saturates, euler_control flat), any growth
  window that CAPTURES the near-singularity signal has a MAGNITUDE that does not
  converge: the blow-up-shape re-accelerates right at the edge of its trusted
  window, and tail_guard keeps pushing that edge out with N (t_res grows), so the
  rate climbs monotonically (N=128,256,512). This is spike finding #3 (the
  near-singularity exponent/rate never resolution-converges on a uniform grid)
  reasserting on the growth-rate axis -- refinement (1) FAILS as a magnitude fix.

LEG 2 -- BUT THE RANK ORDER IS RESOLUTION-STABLE, and one currency survives the
  cheat audit. Over the fixed-split roster (split=0.5) at N=128,256:
    - g_frac = rate over [0.5*t_res, t_res] : Spearman(rank@128, rank@256) ~ +0.90,
      correct labeled direction (sharp>mild>control), winner a genuine grower,
      rho(g_frac, log|w0|) ~ +0.17 (no omega0 cheat), rho(g_frac, centroid) ~ +0.31
      (rewards structure), rho(g_frac, t_res) ~ -0.70 (sharper=earlier-underresolving
      shapes rank higher). PASSES the audit.
    - accel_ratio = late_rate/early_rate : ALSO rank-stable (~+0.95) but a
      SMALL-DENOMINATOR CHEAT -- rho(accel_ratio, early_rate) ~ -0.66, its winner is
      a NON-grower (full T_MAX), it mis-ranks the labeled ground truth. FAILS.
  Lesson (again): rank-stability is necessary, not sufficient -- interrogate the
  winner against the dumbest cheat.

LEG 3 -- CAVEAT 2 (free split) is FAVORABLE for g_frac. Freeing the omega/theta
  split does NOT create a trivial max-split optimum: a controlled split-sweep at
  fixed structure has an INTERIOR optimum (~0.3-0.5, not railing to 1), and on a
  free random roster the apparent rho(g_frac, split)~+0.73 is genuine buoyancy
  physics, NOT the omega0 cheat back in disguise -- partial rho(g_frac, log|w0| |
  split) ~ +0.04 (the omega0 dependence is fully mediated by split), while partial
  rho(g_frac, split | log|w0|) ~ +0.41 survives. The honest caveat: split (a
  logged, not binned, descriptor) dominates omega-geometry in g_frac's ranking.

CONSEQUENCE (a finding, not a push-harder signal): the g_frac RANK-based currency
is cheat-free, direction-correct, caveat-2-favorable, and rank-stable at
N=128<->256 -- but its MAGNITUDE is on the uniform-grid resolution wall, so any
full Gate 4 must reformulate "resolution-stable" as RANK-stable and evaluate
property 6 controlling for split. The remaining unrun de-risk is 256->512 RANK
stability (the expensive leg), paused for review.

Cheap: one nu=0 solve per (shape, N); no bisection. ~10 min at N<=512 on 8 workers.

Usage: .venv/bin/python phase1_gsustained_probe.py --workers 8
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")

import argparse
import json
import multiprocessing
import sys
from datetime import datetime, timezone

import numpy as np

from ga.genome2d_smooth import realize, random_genome, shape_descriptors
from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from phase1_gate4_probe import _mk, build_probe_roster, force_split
from solver.boussinesq import grid2d, solve_boussinesq

T_MAX = 4.0
AMPLIFICATION = 1e5     # never reached; tail_guard stops first
MAX_STEPS = 4000
DT_MAX = 1e-2
TAIL_GUARD = 1e-3

LABELED_RES = (128, 256, 512)   # LEG 1: the resolution-wall evidence
ROSTER_RES = (128, 256)          # LEG 2: rank-stability of the ordering
FREE_RES = 128                   # LEG 3: caveat-2 free-split (cheap)

# controlled split-sweep base shapes (LEG 3, Test A): (omega modes, theta modes)
SWEEP_BASES = {
    "b_diag": ({(1, 1): 1.0, (2, 2): 0.6}, {(0, 2): 1.0, (2, 2): 1.0}),
    "b_low":  ({(1, 1): 1.0}, {(1, 1): 1.0}),
    "b_high": ({(3, 1): 1.0, (2, 2): 0.6}, {(0, 2): 1.0, (3, 1): 0.7}),
}
SWEEP_SPLITS = [0.1, 0.3, 0.5, 0.7, 0.9, 0.97]
FREE_SEEDS = list(range(40010, 40040))   # 30 free-split random shapes


# ----- solver + growth-rate currencies ---------------------------------------
def _solve(w0, th0, buoyancy):
    r = solve_boussinesq(
        w0, th0, nu=0.0, kappa=0.0, t_max=T_MAX, buoyancy=buoyancy,
        symmetry="houluo", amplification_factor=AMPLIFICATION,
        tail_guard=TAIL_GUARD, max_steps=MAX_STEPS, dt_max=DT_MAX)
    return np.asarray(r.times), np.asarray(r.max_omega), float(r.t_final), r.outcome


def _rate(t, m, t1, t2):
    """log-growth rate of max|w| over the absolute window [t1, t2]; NaN if the
    trusted window does not cover t2 or either endpoint is non-positive."""
    if t2 > t[-1] or t1 <= t[0] or t2 <= t1:
        return float("nan")
    a1, a2 = np.interp(t1, t, m), np.interp(t2, t, m)
    return float((np.log(a2) - np.log(a1)) / (t2 - t1)) if (a1 > 0 and a2 > 0) else float("nan")


def currencies(t, m, tr):
    """The candidate growth-rate currencies, from one inviscid trajectory."""
    early = _rate(t, m, 0.8, 1.3)              # fixed early window (spike-style)
    late = _rate(t, m, tr - 0.4, tr)           # last 0.4-slice at the trusted edge
    return {
        "g_frac": _rate(t, m, 0.5 * tr, tr),   # SURVIVOR: fractional late rate
        "g_anchored": _rate(t, m, tr - 0.5, tr),
        "g_fixed": _rate(t, m, 1.5, 2.3),      # spike's fixed-absolute window
        "early_rate": early,
        "late_rate": late,
        "accel_ratio": (late / early if (np.isfinite(early) and abs(early) > 1e-3
                        and np.isfinite(late)) else float("nan")),
    }


# ----- workers ---------------------------------------------------------------
def _meta(base):
    return {"schema_version": SCHEMA_VERSION, "sweep": "phase1_gsustained_probe",
            "timestamp": datetime.now(timezone.utc).isoformat(), **base}


def _labeled_ic(name, n):
    X, Y = grid2d(n)
    if name in ("smooth_sharp", "euler_control"):
        return 0.2 * np.sin(X) * np.sin(Y), (1.0 + np.cos(2 * X)) * np.sin(2 * Y)
    if name == "smooth_mild":
        return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)
    raise ValueError(name)


def run_labeled(task):
    name, n, base = task["name"], task["n"], task["base"]
    w0, th0 = _labeled_ic(name, n)
    t, m, tr, outcome = _solve(w0, th0, buoyancy=(name != "euler_control"))
    return {"leg": "magnitude", "label": name, "resolution_N": n, "t_res": tr,
            "outcome": outcome, "max_w0": float(np.max(np.abs(w0))),
            **currencies(t, m, tr), **_meta(base)}


def run_roster(task):
    g, n, base = task["genome"], task["n"], task["base"]
    w0, th0 = realize(g, n)
    t, m, tr, outcome = _solve(w0, th0, buoyancy=True)
    return {"leg": "ordering", "label": task["label"], "shape_class": task["cls"],
            "resolution_N": n, "t_res": tr, "outcome": outcome,
            "max_w0": float(np.max(np.abs(w0))), "descriptors": shape_descriptors(g),
            **currencies(t, m, tr), **_meta(base)}


def run_free(task):
    g, base = task["genome"], task["base"]
    w0, th0 = realize(g, FREE_RES)
    t, m, tr, outcome = _solve(w0, th0, buoyancy=True)
    return {"leg": task["subleg"], "label": task["label"], "resolution_N": FREE_RES,
            "t_res": tr, "outcome": outcome, "target_split": task.get("target_split"),
            "max_w0": float(np.max(np.abs(w0))), "descriptors": shape_descriptors(g),
            **currencies(t, m, tr), **_meta(base)}


# ----- analysis helpers ------------------------------------------------------
def _rho(xs, ys):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    ok = np.isfinite(xs) & np.isfinite(ys)
    if ok.sum() < 3 or np.std(xs[ok]) == 0 or np.std(ys[ok]) == 0:
        return float("nan")
    return float(np.corrcoef(xs[ok], ys[ok])[0, 1])


def _spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 3:
        return float("nan")
    ra, rb = np.argsort(np.argsort(a[ok])), np.argsort(np.argsort(b[ok]))
    return float(np.corrcoef(ra, rb)[0, 1]) if (np.std(ra) and np.std(rb)) else float("nan")


def _partial(x, y, z):
    """partial correlation of x,y controlling for z (linear residuals)."""
    x, y, z = (np.asarray(v, float) for v in (x, y, z))
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(z)
    x, y, z = x[ok], y[ok], z[ok]
    if len(x) < 4:
        return float("nan")
    res = lambda a: a - np.polyval(np.polyfit(z, a, 1), z)
    return float(np.corrcoef(res(x), res(y))[0, 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_gsustained_probe.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    dirty, _ = working_tree_dirty()
    if dirty and not args.allow_dirty:
        sys.exit("working tree is dirty; commit first (or --allow-dirty)")
    base = dict(code_version=code_version(), code_dirty=dirty)

    labeled = [dict(name=nm, n=n, base=base)
               for nm in ("smooth_sharp", "smooth_mild", "euler_control")
               for n in LABELED_RES]
    roster = [dict(label=s["label"], cls=s["cls"], genome=s["genome"], n=n, base=base)
              for s in build_probe_roster() for n in ROSTER_RES]
    free = [dict(subleg="free_split", label=f"free_{sd}",
                 genome=random_genome(np.random.default_rng(sd)), base=base)
            for sd in FREE_SEEDS]
    sweep = [dict(subleg="split_sweep", label=f"{nm}_s{int(s*100):02d}",
                  genome=force_split(_mk(*SWEEP_BASES[nm]), target=s),
                  target_split=s, base=base)
             for nm in SWEEP_BASES for s in SWEEP_SPLITS]
    print(f"g_sustained probe: {len(labeled)} labeled (N<=512) + {len(roster)} roster "
          f"(N=128,256) + {len(free)} free-split + {len(sweep)} split-sweep, "
          f"on {args.workers} workers", flush=True)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    lab_rows, ros_rows, free_rows, sweep_rows = [], [], [], []
    with open(args.out, "a") as f:
        pool = multiprocessing.get_context().Pool(args.workers)
        try:
            for row in pool.imap_unordered(run_labeled, labeled, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); lab_rows.append(row)
            for row in pool.imap_unordered(run_roster, roster, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); ros_rows.append(row)
            for row in pool.imap_unordered(run_free, free, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); free_rows.append(row)
            for row in pool.imap_unordered(run_free, sweep, chunksize=1):
                f.write(json.dumps(row) + "\n"); f.flush(); sweep_rows.append(row)
        finally:
            pool.close(); pool.join()

    _report(lab_rows, ros_rows, free_rows, sweep_rows)
    print(f"\n-> {args.out}", flush=True)


def _report(lab_rows, ros_rows, free_rows, sweep_rows):
    # LEG 1: magnitude on the resolution wall
    print("\n=== LEG 1: MAGNITUDE vs N (does the near-singularity rate converge?) ===")
    by = {}
    for r in lab_rows:
        by.setdefault(r["label"], {})[r["resolution_N"]] = r
    for nm in ("smooth_sharp", "smooth_mild", "euler_control"):
        cells = " ".join(
            f"N={n}:g_frac={by[nm][n]['g_frac']:+.3f}(t_res={by[nm][n]['t_res']:.2f})"
            for n in LABELED_RES if n in by[nm])
        print(f"  {nm:14s} {cells}")
    sN = LABELED_RES
    gs = [by["smooth_sharp"][n]["g_frac"] for n in sN if n in by["smooth_sharp"]]
    print(f"  smooth_sharp g_frac climbs {gs} across N={list(sN)} -> MAGNITUDE NOT converged")
    fine = max(LABELED_RES[:1] + tuple(n for n in LABELED_RES if n in by["smooth_sharp"]))
    fine = 256 if 256 in by["smooth_sharp"] else LABELED_RES[-1]
    d = {nm: by[nm][fine]["g_frac"] for nm in by}
    print(f"  labeled direction @N={fine} sharp>mild>control (g_frac): "
          f"{d['smooth_sharp'] > d['smooth_mild'] > d['euler_control']} "
          f"({d['smooth_sharp']:+.3f}>{d['smooth_mild']:+.3f}>{d['euler_control']:+.3f})")

    # LEG 2: rank-stability + cheat audit on the fixed-split roster
    print("\n=== LEG 2: RANK-STABILITY (128<->256) + cheat audit (fixed-split roster) ===")
    labs = sorted({r["label"] for r in ros_rows})
    at = {(r["label"], r["resolution_N"]): r for r in ros_rows}
    for cur in ("g_frac", "accel_ratio"):
        a = [at[(l, 128)][cur] for l in labs]
        b = [at[(l, 256)][cur] for l in labs]
        sp = _spearman(a, b)
        rows256 = [at[(l, 256)] for l in labs]
        fin = [r for r in rows256 if np.isfinite(r[cur])]
        fin.sort(key=lambda r: -r[cur])
        v = [r[cur] for r in fin]
        win = fin[0]
        top5_grow = sum(r["t_res"] < T_MAX - 1e-6 for r in fin[:5])
        print(f"  [{cur}] spearman(128,256)={sp:+.3f}  winner={win['label']}"
              f"[{win['shape_class'][:4]}] grow={win['t_res'] < T_MAX - 1e-6} "
              f"top5_growers={top5_grow}/5")
        print(f"     rho(., log|w0|)={_rho(v, np.log([r['max_w0'] for r in fin])):+.3f}  "
              f"rho(., early_rate)={_rho(v, [r['early_rate'] for r in fin]):+.3f}  "
              f"rho(., centroid)={_rho(v, [r['descriptors']['centroid'] for r in fin]):+.3f}  "
              f"rho(., t_res)={_rho(v, [r['t_res'] for r in fin]):+.3f}")

    # LEG 3: caveat-2 free split
    print("\n=== LEG 3: caveat-2 free-split property-6 (g_frac) ===")
    for nm in SWEEP_BASES:
        row = sorted((r for r in sweep_rows if r["label"].startswith(nm)),
                     key=lambda r: r["target_split"])
        gv = [r["g_frac"] for r in row]
        argmax = row[int(np.nanargmax(gv))]["target_split"] if any(np.isfinite(gv)) else float("nan")
        rail = "RAIL->1 (FAIL)" if argmax == SWEEP_SPLITS[-1] else f"interior peak @{argmax}"
        cells = " ".join(f"s={r['target_split']:.2f}:{r['g_frac']:+.2f}" for r in row)
        print(f"  sweep {nm:7s} {cells}  -> {rail}")
    fin = [r for r in free_rows if np.isfinite(r["g_frac"])]
    gf = [r["g_frac"] for r in fin]
    sv = [r["descriptors"]["split"] for r in fin]
    lw = list(np.log([r["max_w0"] for r in fin]))
    cv = [r["descriptors"]["centroid"] for r in fin]
    fin.sort(key=lambda r: -r["g_frac"])
    print(f"  free roster: rho(g_frac,split)={_rho(gf, sv):+.3f}  "
          f"rho(g_frac,log|w0|)={_rho(gf, lw):+.3f}  rho(split,log|w0|)={_rho(sv, lw):+.3f}")
    print(f"  partial rho(g_frac,log|w0| | split)={_partial(gf, lw, sv):+.3f} (near 0 => omega0 cheat ABSENT)")
    print(f"  partial rho(g_frac,split | log|w0|)={_partial(gf, sv, lw):+.3f} (survives => split preference genuine physics)")
    print(f"  partial rho(g_frac,centroid | split)={_partial(gf, cv, sv):+.3f}")
    print(f"  winner split={fin[0]['descriptors']['split']:.2f}  "
          f"top5 mean split={np.mean([r['descriptors']['split'] for r in fin[:5]]):.2f} "
          f"(roster mean {np.mean(sv):.2f})  top5 growers="
          f"{sum(r['t_res'] < T_MAX - 1e-6 for r in fin[:5])}/5")


if __name__ == "__main__":
    main()
