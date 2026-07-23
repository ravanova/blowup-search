"""Phase 1 fitness-axis discrimination screen (pre-Gate-4 routing check).

The resolution spike (PHASE1_SPIKE_RESULTS.md) left us two LABELED ground-truth
smooth ICs:

  smooth_sharp  -- blows up  (amp > 100) but LOW  windowed growth rate g = 0.61
  smooth_mild   -- saturates (amp ~ 5)   but HIGH windowed growth rate g = 1.24

So the raw windowed growth rate g orders these two BACKWARDS: it rewards
transient early rate, not blow-up PROPENSITY. Before committing a fitness axis to
the full six-property Gate 4 (40 shapes), this cheap screen asks the one routing
question those labeled ICs can answer decisively:

  Which candidate axis orders  smooth_sharp > smooth_mild  (the propensity
  direction) AND stays resolution-stable across N?

This is a SCREEN, not the gate: passing is necessary, not sufficient (full Gate 4
still runs on the survivor over 40 shapes). Failing kills an axis for ~an hour of
compute. If nu_crit ALSO fails the sign test that is a FINDING (stop and re-plan),
not a push-harder signal -- the same discipline as Stages 2.5 / 3.5 / 3.6.

Three axes measured on {smooth_sharp, smooth_mild, euler_control} at N=256, 512:

  1. nu_crit-analog  -- the viscosity at which NET resolved amplification
     amp(nu) = max|w|(t_resolved)/max|w|(0) crosses A_CRIT: "how much viscosity
     it takes to hold the buoyancy-driven amplification below A_CRIT." This uses
     amplification -- the project's actual blow-up currency, the same
     amplification-only predicate as ga.fitness.py's v3 oracle -- NOT an in-window
     slope. (The first draft used "g(nu) crosses zero"; the pre-run smoke showed
     that is contaminated: a net-DECAYING run, amp=0.5, can still have a positive
     in-window slope. Amplification is monotone-decreasing in nu and cannot be
     fooled that way.) Higher nu_crit = harder to kill = more blow-up prone.
     kappa = 0 (confirmed with the user): nu is the single regularizing knob; the
     temperature/density scalar is left undamped so criticality isolates viscous
     regularization of the vorticity growth mechanism itself.

  2. persistence      -- acceleration of the growth over the resolved window
     (late-window rate minus early-window rate) from the SAME nu=0 run, so it is
     free. Sharp accelerates toward the singularity (> 0); mild saturates (<= 0).

  3. g_baseline       -- the raw windowed growth rate, recomputed as the
     known-WRONG-direction control. The screen should reproduce mild > sharp
     here (a sanity check that it faithfully reproduces the spike).

euler_control = smooth_sharp's velocity field with buoyancy OFF (2D Euler + nu):
no theta_x forcing, so max|w| does not grow -> it must sit at the BOTTOM of every
axis (anti-self-deception anchor: the axis must respond to the buoyancy mechanism,
not merely to having a vortex).

Usage:
    .venv/bin/python phase1_axis_screen.py --workers 6
    .venv/bin/python phase1_axis_screen.py --smoke
Then: .venv/bin/python analyze_phase1_axis_screen.py
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

from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.boussinesq import grid2d, solve_boussinesq

RESOLUTIONS = (256, 512)
GROWTH_WINDOW = (1.5, 2.3)     # same fixed trusted window as the spike
PERSIST_START = 1.0            # persistence measured over [PERSIST_START, t_resolved]
TAIL_GUARD = 1e-3             # the spike's under-resolution trust instrument
T_MAX = 4.0                   # enough to cover sharp's resolved window (~3.2 @512)
AMPLIFICATION = 1e5           # never reached; the tail guard stops first
MAX_STEPS = 4000
DT_MAX = 1e-2

# --- pre-committed bisection + predicate constants (frozen before the run) ---
NU_RANGE = (0.0, 1.5)        # low end grows, high end is viscosity-suppressed
NU_TOL = 5e-3                # bisection half-width stop
NU_MAX_ITERS = 12
A_CRIT = 2.0                 # net-amplification boundary: amp >= A_CRIT (a
                            # doubling) or diverged counts as the blow-up side.
                            # A doubling sits clearly above a conserved-vorticity
                            # Euler control (amp ~ 1) and below the growers.


def build_ics():
    """Labeled ground-truth roster (picklable specs; fields built in the worker).
    smooth_sharp/smooth_mild are verbatim the spike's smooth ICs; euler_control
    reuses smooth_sharp's fields with buoyancy off as the non-grower anchor."""
    return [
        {"label": "smooth_sharp", "buoyancy": True},
        {"label": "smooth_mild", "buoyancy": True},
        {"label": "euler_control", "buoyancy": False, "base": "smooth_sharp"},
    ]


def realize_ic(ic, n):
    X, Y = grid2d(n)
    base = ic.get("base", ic["label"])
    if base == "smooth_sharp":
        return 0.2 * np.sin(X) * np.sin(Y), (1.0 + np.cos(2 * X)) * np.sin(2 * Y)
    if base == "smooth_mild":
        return np.sin(X) * np.sin(Y), np.cos(X) * np.sin(Y)
    raise ValueError(f"unknown IC base {base}")


def _interp(times, values, tq):
    times = np.asarray(times)
    if tq > times[-1]:
        return float("nan")
    return float(np.interp(tq, times, values))


def _run(w0, th0, nu, buoyancy):
    return solve_boussinesq(
        w0, th0, nu=float(nu), kappa=0.0, t_max=T_MAX, buoyancy=buoyancy,
        symmetry="houluo", amplification_factor=AMPLIFICATION,
        tail_guard=TAIL_GUARD, max_steps=MAX_STEPS, dt_max=DT_MAX)


def _g_window(times, mom):
    """Fixed-window log-growth rate g over GROWTH_WINDOW, or nan if the run ended
    before the window closes."""
    t1, t2 = GROWTH_WINDOW
    if times[-1] < t2:
        return float("nan")
    a1, a2 = _interp(times, mom, t1), _interp(times, mom, t2)
    return float((np.log(a2) - np.log(a1)) / (t2 - t1))


def _persistence(times, mom):
    """Growth acceleration over [PERSIST_START, t_resolved]: late-window rate
    minus early-window rate. > 0 accelerating (blow-up prone), <= 0 saturating."""
    t_lo, t_hi = PERSIST_START, float(times[-1])
    if t_hi <= t_lo + 0.4:
        return float("nan")
    tm = 0.5 * (t_lo + t_hi)
    m_lo, m_mid, m_hi = (_interp(times, mom, t) for t in (t_lo, tm, t_hi))
    g_early = (np.log(m_mid) - np.log(m_lo)) / (tm - t_lo)
    g_late = (np.log(m_hi) - np.log(m_mid)) / (t_hi - tm)
    return float(g_late - g_early)


def bisect_nu_crit(w0, th0, buoyancy):
    """nu at which net resolved amplification amp(nu) crosses A_CRIT.

    Conceptual reuse of ga.fitness.bisect_critical with its v3 amplification-only
    predicate: blow-up side at the low (nu=0) end, suppression at the high end. A
    run is on the blow-up side iff amp = max|w|_end/max|w|_start >= A_CRIT (or it
    diverged) -- amplification is the project's blow-up currency and is monotone
    in nu, unlike an in-window slope. A non-grower at nu=0 censors low (nu_crit =
    0, the correct bottom for euler_control); a still-growing high end censors
    high."""
    lo, hi = NU_RANGE
    runs = []

    def blew(nu):
        r = _run(w0, th0, nu, buoyancy)
        amp = float(r.max_omega[-1] / r.max_omega[0])
        g = _g_window(r.times, r.max_omega)
        grew = (r.outcome == "diverged") or (amp >= A_CRIT)
        runs.append({"nu": float(nu), "amp": amp,
                     "g": (None if np.isnan(g) else g),
                     "outcome": r.outcome, "t_final": float(r.t_final),
                     "max_tail_fraction": float(r.max_tail_fraction),
                     "growing": bool(grew)})
        return grew

    if not blew(lo):
        return {"nu_crit": lo, "censored": "low", "runs": runs}
    if blew(hi):
        return {"nu_crit": hi, "censored": "high", "runs": runs}
    n_it = 0
    while hi - lo > NU_TOL and n_it < NU_MAX_ITERS:
        mid = 0.5 * (lo + hi)
        if blew(mid):
            lo = mid
        else:
            hi = mid
        n_it += 1
    return {"nu_crit": 0.5 * (lo + hi), "censored": None, "runs": runs}


def run_task(task):
    ic, n = task["ic"], task["n"]
    w0, th0 = realize_ic(ic, n)
    t0 = time.perf_counter()

    # nu=0 baseline run drives both g_baseline and persistence (free).
    r0 = _run(w0, th0, 0.0, ic["buoyancy"])
    g_baseline = _g_window(r0.times, r0.max_omega)
    persistence = _persistence(r0.times, r0.max_omega)

    bis = bisect_nu_crit(w0, th0, ic["buoyancy"])

    return {
        "schema_version": SCHEMA_VERSION,
        "sweep": "phase1_axis_screen",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": task["code_version"],
        "code_dirty": task["code_dirty"],
        "ic_label": ic["label"],
        "buoyancy": ic["buoyancy"],
        "resolution_N": n,
        "nu0_outcome": r0.outcome,
        "nu0_t_resolved": float(r0.t_final),
        "nu0_amp_resolved": float(r0.max_omega[-1] / r0.max_omega[0]),
        "nu0_max_tail_fraction": float(r0.max_tail_fraction),
        # the three candidate axes
        "nu_crit": float(bis["nu_crit"]),
        "nu_crit_censored": bis["censored"],
        "persistence": (None if np.isnan(persistence) else persistence),
        "g_baseline": (None if np.isnan(g_baseline) else g_baseline),
        "n_bisection_runs": len(bis["runs"]),
        "bisection_runs": bis["runs"],
        "wall_clock_seconds": time.perf_counter() - t0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/phase1_axis_screen.jsonl")
    ap.add_argument("--workers", type=int, default=6)
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
        ics, resolutions = ics[:2], (128,)

    tasks = [{"ic": ic, "n": n, "code_version": code_ver, "code_dirty": dirty}
             for ic in ics for n in resolutions]
    tasks.sort(key=lambda t: -t["n"])
    print(f"{len(ics)} ICs x {len(resolutions)} N = {len(tasks)} bisections "
          f"(nu in {NU_RANGE}, tol={NU_TOL:g}, tail_guard={TAIL_GUARD:g}) "
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
                pv = "  nan" if row["persistence"] is None else f"{row['persistence']:+.3f}"
                gv = "  nan" if row["g_baseline"] is None else f"{row['g_baseline']:.3f}"
                cens = row["nu_crit_censored"] or ""
                print(f"[{done}/{len(tasks)}] {row['ic_label']:14s} N={row['resolution_N']:4d} "
                      f"nu_crit={row['nu_crit']:.4f}{cens:>5s} persist={pv} "
                      f"g={gv} (amp={row['nu0_amp_resolved']:6.1f}, "
                      f"{row['n_bisection_runs']} runs, {row['wall_clock_seconds']:.0f}s)",
                      flush=True)
        finally:
            if pool:
                pool.close(); pool.join()
    print(f"\nScreen complete: {done} bisections in {time.perf_counter()-t0:.0f}s "
          f"-> {args.out}\nNext: .venv/bin/python analyze_phase1_axis_screen.py", flush=True)


if __name__ == "__main__":
    main()
