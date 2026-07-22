"""Stage 1.5 fitness-signal viability sweep (PLAN.md Stage 1.5).

No GA — a direct sweep over ~20 hand-picked initial conditions, measuring
for each shape both candidate fitness axes by bisection:

- nu_crit: critical viscosity at fixed a=0 (CLM, where smooth-data blow-up
  is proven, so the nu axis is isolated from the advection question).
- a_crit:  critical advection coefficient at nu=0 (the Okamoto-Sakajo-Wunsch
  question: largest a at which the shape still blows up).

Both are measured at two resolutions (N=256, N=512) under ONE fixed t_max
across every run — critical values are horizon-relative (PLAN.md Stage 2),
so a sweep with varying horizons measures nothing.

Bisection-oracle rules (PLAN.md Stage 2, applied here ahead of the GA):
- Blow-up predicate, decided per run in this order:
  1. A run stopped by the amplification threshold (outcome
     "blowup_candidate") IS a blow-up, whatever its tail fit says — it hit
     the blow-up stop condition (max|w| grew 100x at fixed L2 energy).
     This generalizes PLAN.md's InsufficientDataError edge rule, whose
     stated rationale ("it hit the blow-up stop condition") applies equally
     when the fit ran but scored badly: near a=1 the growth is bursty and
     the tail fit can score R^2 << 1 on a run that plainly amplified. Such
     runs carry fit_below_floor=true for auditability.
  2. Otherwise (ran to t_max / decayed): blow-up iff
     estimate_blowup_time(fit_exponent=True) returns an estimate AND its
     held-out R^2 >= R2_FLOOR (0.9) AND the extrapolated T* is within
     T_STAR_CAP_FACTOR * t_max — the forward Tier-1-style extrapolation,
     with a floor loose enough to be robust exactly where fits are marginal
     (the Tier 1 gate 0.98 still decides *candidates*). The T* cap was
     added after the v1 sweep: without it, runs that sat quietly to t_max
     and then fit a zero crossing at T* = 6-11x the horizon (e.g. T*=136
     from a run ending at t=12) were accepted as blow-ups, and whether such
     marginal fits clear the R^2 floor flips with resolution — the entire
     a-axis resolution instability in v1 traced to this. A critical value
     is horizon-relative (PLAN.md); a prediction far beyond the horizon is
     unfalsifiable within the run and cannot count as a measurement.
- "diverged" (NaN) is counted as blow-up but flagged: in this solver NaN
  only arises from explosive growth outrunning the adaptive dt.
- Bracket-edge outcomes are censored data, not measurements
  (bracket_censored "low"/"high"; critical_value is then a range edge).
- Monotonicity cannot be falsified by bisection's own samples, so after
  convergence 2 probe values beyond the critical value on the regular side
  are run; any blow-up there flags the shape's signal as non-monotone.

Every row in the output JSONL is standalone-reproducible: code_version,
root seed, full IC spec (analytic construction + normalization scale),
full solver params, and per-run summaries.

Usage:
    .venv/bin/python stage1_5_sweep.py                  # full sweep
    .venv/bin/python stage1_5_sweep.py --smoke          # tiny shakedown
    .venv/bin/python stage1_5_sweep.py --print-tstars   # analytic CLM T*
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np

from ga.logbook import SCHEMA_VERSION, code_version, working_tree_dirty
from solver.gclm import clm_analytic_blowup_time, solve_gclm
from solver.spectral_utils import energy, grid
from win_condition import InsufficientDataError, estimate_blowup_time

# --- frozen sweep configuration -------------------------------------------

ROOT_SEED = 20260722

# One horizon for every run in the sweep. Analytic CLM T* for 19 of the 20
# normalized ICs lies in [1.0, 6.5] (--print-tstars), so t_max=12 gives
# >=1.8x headroom for critical-slowdown near nu_crit / a_crit while keeping
# no-blow-up runs affordable. bump(kappa=5) (T*_CLM ~ 15.9) is a deliberate
# beyond-horizon control: it should come back censored "low" on both axes,
# demonstrating the horizon-relative censoring machinery on a known case.
T_MAX = 12.0

RESOLUTIONS = (256, 512)
NU_RANGE = (0.0, 1.0)   # nu_crit bisection bracket, at a = 0
A_RANGE = (0.0, 2.0)    # a_crit bisection bracket, at nu = 0
N_BISECT_ITERS = 8      # final bracket width: range / 2^8
R2_FLOOR = 0.9          # held-out R^2 the blow-up predicate requires
T_STAR_CAP_FACTOR = 1.5  # fit-based blow-up requires t* <= this factor * t_max
TAIL_FRACTION = 0.15    # matches the CLM window calibration in test_solver_clm.py
AMPLIFICATION = 100.0   # matches the calibrated tail/amplification pairing
ENERGY_TARGET = float(np.pi) / 2.0  # L2 energy of sin(x): all shapes, one scale

SOLVER_PARAMS = dict(
    dt_max=1e-2,
    c1=0.05,
    c2=0.4,
    max_steps=200_000,
    amplification_factor=AMPLIFICATION,
    early_decay_exit={"fraction": 0.1, "window": 2.0},
)

N_REFERENCE = 2048  # grid for normalization + ic_hash (both resolution-free)

# --- the 20 initial conditions --------------------------------------------
# All odd (sine series / odd bumps), per PLAN.md Stage 1's documented
# symmetry restriction. Each is defined analytically, then rescaled by one
# scalar so its L2 energy equals ENERGY_TARGET — critical values must
# reflect shape, not amplitude (scale covariance).


def _sine_series(pairs):
    def fn(x):
        w = np.zeros_like(x)
        for k, c in pairs:
            w = w + c * np.sin(k * x)
        return w
    return fn


def _bump(kappa):
    # Odd localized bump pair: sin(x) * exp(kappa*(cos(x)-1)); larger kappa
    # concentrates the vorticity into sharper structures.
    return lambda x: np.sin(x) * np.exp(kappa * (np.cos(x) - 1.0))


def _tail(p, k_max=20, alternating=False):
    return [(k, ((-1.0) ** (k + 1) if alternating else 1.0) * k ** (-p))
            for k in range(1, k_max + 1)]


def build_initial_conditions():
    """Returns a list of dicts: {label, family, spec, fn} (unnormalized)."""
    ics = []

    def add(label, family, spec, fn):
        ics.append({"label": label, "family": family, "spec": spec, "fn": fn})

    # Literature / structured profiles (12)
    for label, pairs in [
        ("sin(x)", [(1, 1.0)]),
        ("sin(2x)", [(2, 1.0)]),
        ("sin(x)+0.5sin(2x)", [(1, 1.0), (2, 0.5)]),
        ("sin(x)-0.5sin(2x)", [(1, 1.0), (2, -0.5)]),
        ("sin(x)+0.3sin(3x)", [(1, 1.0), (3, 0.3)]),
        ("sin(x)+0.5sin(4x)", [(1, 1.0), (4, 0.5)]),
    ]:
        add(label, "sine", {"type": "sine", "pairs": pairs}, _sine_series(pairs))

    for kappa in (2.0, 5.0):
        add(f"bump(kappa={kappa:g})", "bump",
            {"type": "bump", "kappa": kappa}, _bump(kappa))

    for p in (1.0, 1.5, 2.0):
        pairs = _tail(p)
        add(f"tail(p={p:g})", "tail",
            {"type": "sine", "pairs": pairs}, _sine_series(pairs))
    pairs = _tail(1.5, alternating=True)
    add("tail(p=1.5,alt)", "tail",
        {"type": "sine", "pairs": pairs}, _sine_series(pairs))

    # Random odd shapes at fixed energy (8): c_k ~ N(0,1) * k^-1.5, k<=16
    for i in range(8):
        rng = np.random.default_rng(np.random.SeedSequence([ROOT_SEED, i]))
        coeffs = rng.standard_normal(16) * np.arange(1, 17) ** (-1.5)
        pairs = [(k + 1, float(c)) for k, c in enumerate(coeffs)]
        add(f"random(seed={i})", "random",
            {"type": "sine", "pairs": pairs, "seed_spawn": [ROOT_SEED, i]},
            _sine_series(pairs))

    # Normalize every IC to ENERGY_TARGET on the reference grid, and attach
    # a resolution-free identity hash of the normalized profile.
    x_ref = grid(N_REFERENCE)
    for ic in ics:
        w_ref = ic["fn"](x_ref)
        e_raw = energy(w_ref)
        scale = float(np.sqrt(ENERGY_TARGET / e_raw))
        base_fn = ic["fn"]
        ic["fn"] = (lambda f, s: (lambda x: s * f(x)))(base_fn, scale)
        ic["spec"]["scale"] = scale
        ic["energy"] = energy(ic["fn"](x_ref))
        ic["ic_hash"] = hashlib.sha256(ic["fn"](x_ref).tobytes()).hexdigest()
    return ics


# --- blow-up predicate (the bisection oracle) ------------------------------


def classify_run(result):
    """Apply the blow-up predicate to one solver run.

    Returns (is_blowup, summary_dict). `via` records which rule decided;
    `fit_below_floor` marks an amplification-stopped run whose tail fit
    failed the floor anyway (bursty growth) — audited in aggregate.
    """
    summary = {
        "outcome": result.outcome,
        "early_exit_reason": result.early_exit_reason,
        "t_final": float(result.t_final),
        "n_timesteps": int(result.n_timesteps),
        "dt_min": float(result.dt_min),
        "conservation_drift": float(result.conservation_drift),
        "wall_clock_seconds": float(result.wall_clock_seconds),
        "t_star": None, "r_squared": None, "exponent": None,
        "fit_below_floor": False,
    }
    if result.outcome == "diverged":
        summary["via"] = "diverged_nan"
        return True, summary
    try:
        est = estimate_blowup_time(
            result.times.tolist(), result.max_omega.tolist(),
            tail_fraction=TAIL_FRACTION, fit_exponent=True,
        )
    except InsufficientDataError:
        if result.outcome == "blowup_candidate":
            summary["via"] = "amplification_insufficient_data"
            return True, summary
        summary["via"] = "insufficient_data_no_amplification"
        return False, summary
    if est is not None:
        summary["t_star"] = float(est.t_star)
        summary["r_squared"] = float(est.r_squared)
        summary["exponent"] = float(est.exponent)
    fit_ok = est is not None and est.r_squared >= R2_FLOOR
    if result.outcome == "blowup_candidate":
        # Rule 1: the amplification stop fired — that is the blow-up stop
        # condition, and it outranks the tail fit (see module docstring).
        summary["via"] = "amplification"
        summary["fit_below_floor"] = not fit_ok
        return True, summary
    within_horizon = (est is not None
                      and est.t_star <= T_STAR_CAP_FACTOR * T_MAX)
    if fit_ok and within_horizon:
        summary["via"] = "fit"
        return True, summary
    summary["via"] = ("fit_beyond_horizon_cap" if fit_ok
                      else "fit_below_floor_or_none")
    return False, summary


# --- bisection with censoring + monotonicity probes ------------------------


def bisect_critical(run_at, lo, hi, n_iters):
    """Bisect the blow-up/no-blow-up boundary in [lo, hi].

    `run_at(param)` -> (is_blowup, run_summary). Assumes blow-up at the lo
    (easy) end and regularity at the hi (hard) end; violations are censored,
    not extrapolated. Returns (critical, censored, bracket, runs)."""
    runs = []

    def evaluate(param):
        blow, summary = run_at(param)
        runs.append({"param": float(param), "blowup": bool(blow), **summary})
        return blow

    if not evaluate(lo):
        return lo, "low", [lo, hi], runs
    if evaluate(hi):
        return hi, "high", [lo, hi], runs
    b_lo, b_hi = lo, hi
    for _ in range(n_iters):
        mid = 0.5 * (b_lo + b_hi)
        if evaluate(mid):
            b_lo = mid
        else:
            b_hi = mid
    return 0.5 * (b_lo + b_hi), None, [b_lo, b_hi], runs


def probe_monotone(run_at, critical, range_hi, runs):
    """Probe 1-2 values beyond `critical` on the regular side; blow-up out
    there means the response is non-monotone (broken fitness signal)."""
    width = range_hi  # both sweep ranges start at 0, so hi == width
    probes = []
    for frac in (0.05, 0.15):
        p = critical + frac * width
        if p >= range_hi:  # already tested at the edge during bracketing
            continue
        blow, summary = run_at(p)
        runs.append({"param": float(p), "blowup": bool(blow), "probe": True,
                     **summary})
        probes.append({"param": float(p), "blowup": bool(blow)})
    monotone = all(not p["blowup"] for p in probes) if probes else None
    return monotone, probes


# --- sweep driver ----------------------------------------------------------


def sweep_one(ic, axis, n_res, out_file, code_ver, code_dirty):
    if axis == "nu":
        lo, hi = NU_RANGE
        fixed = {"a": 0.0}

        def run_at(nu):
            return classify_run(solve_gclm(
                ic["fn"](grid(n_res)), a=0.0, nu=nu, t_max=T_MAX,
                **SOLVER_PARAMS))
    else:
        lo, hi = A_RANGE
        fixed = {"nu": 0.0}

        def run_at(a):
            return classify_run(solve_gclm(
                ic["fn"](grid(n_res)), a=a, nu=0.0, t_max=T_MAX,
                **SOLVER_PARAMS))

    t0 = time.perf_counter()
    critical, censored, bracket, runs = bisect_critical(
        run_at, lo, hi, N_BISECT_ITERS)
    monotone, probes = (None, [])
    if censored is None:
        monotone, probes = probe_monotone(run_at, critical, hi, runs)

    blowup_drifts = [r["conservation_drift"] for r in runs if r["blowup"]]
    row = {
        "schema_version": SCHEMA_VERSION,
        "sweep": "stage1_5",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "code_version": code_ver,
        "code_dirty": code_dirty,
        "root_seed": ROOT_SEED,
        "ic": {
            "label": ic["label"], "family": ic["family"], "spec": ic["spec"],
            "energy": ic["energy"], "ic_hash": ic["ic_hash"],
            "clm_t_star_analytic": ic["clm_t_star_analytic"],
        },
        "axis": axis,
        "fixed": fixed,
        "resolution_N": n_res,
        "t_max": T_MAX,
        "tail_fraction": TAIL_FRACTION,
        "predicate_r2_floor": R2_FLOOR,
        "t_star_cap_factor": T_STAR_CAP_FACTOR,
        "range": [lo, hi],
        "n_bisect_iters": N_BISECT_ITERS,
        "solver_params": SOLVER_PARAMS,
        "critical_value": float(critical),
        "bracket_censored": censored,
        "bracket_final": [float(b) for b in bracket],
        "critical_value_monotone": monotone,
        "monotone_probes": probes,
        "n_runs": len(runs),
        "n_fit_below_floor": sum(r["fit_below_floor"] for r in runs),
        "max_conservation_drift_blowup_runs":
            max(blowup_drifts) if blowup_drifts else None,
        "wall_clock_seconds": time.perf_counter() - t0,
        "runs": runs,
    }
    out_file.write(json.dumps(row) + "\n")
    out_file.flush()
    os.fsync(out_file.fileno())
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="experiments/stage1_5_sweep.jsonl")
    ap.add_argument("--smoke", action="store_true",
                    help="2 ICs, N=128 only, 3 bisection iters — shakedown")
    ap.add_argument("--print-tstars", action="store_true",
                    help="print analytic CLM T* per normalized IC and exit")
    ap.add_argument("--allow-dirty", action="store_true")
    args = ap.parse_args()

    ics = build_initial_conditions()
    for ic in ics:
        t_star = clm_analytic_blowup_time(ic["fn"])
        ic["clm_t_star_analytic"] = float(t_star) if t_star else None

    if args.print_tstars:
        for ic in ics:
            print(f"{ic['label']:28s} T*_CLM = {ic['clm_t_star_analytic']}")
        return

    dirty, _ = working_tree_dirty()
    if dirty and not (args.allow_dirty or args.smoke):
        sys.exit("working tree is dirty; commit first (or --allow-dirty "
                 "to mark rows non-reproducible)")

    global N_BISECT_ITERS  # noqa: PLW0603 — smoke mode only
    resolutions = RESOLUTIONS
    if args.smoke:
        ics = ics[:1] + ics[-1:]
        resolutions = (128,)
        N_BISECT_ITERS = 3

    code_ver = code_version()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    n_total = len(ics) * len(resolutions) * 2
    done = 0
    with open(args.out, "a") as out_file:
        for ic in ics:
            for n_res in resolutions:
                for axis in ("nu", "a"):
                    row = sweep_one(ic, axis, n_res, out_file, code_ver, dirty)
                    done += 1
                    cens = row["bracket_censored"]
                    print(f"[{done:3d}/{n_total}] {ic['label']:28s} "
                          f"N={n_res:4d} {axis}_crit = "
                          f"{row['critical_value']:.4f}"
                          f"{' (censored ' + cens + ')' if cens else ''} "
                          f"monotone={row['critical_value_monotone']} "
                          f"runs={row['n_runs']} "
                          f"({row['wall_clock_seconds']:.1f}s)", flush=True)
    print(f"\nSweep complete: {done} bisections -> {args.out}")


if __name__ == "__main__":
    main()
