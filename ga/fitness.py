"""Fitness evaluation for Stage 2: nu_crit(t_max, N) by bisection at a=0.

One fitness evaluation = one warm-started bisection of the blow-up /
no-blow-up boundary in nu, using the v2 oracle frozen by Stage 1.5
(STAGE_1_5_RESULTS.md "Predicate lessons"):

  1. A run stopped by the amplification threshold IS a blow-up, whatever
     its tail fit says (bursty near-critical growth scores badly; the stop
     condition itself is the evidence). "diverged" (NaN) likewise, since in
     this solver NaN only arises from explosive growth outrunning dt.
  2. Otherwise blow-up requires estimate_blowup_time(fit_exponent=True) to
     return an estimate with held-out R^2 >= the floor AND extrapolated
     T* <= cap_factor * t_max (uncapped forward extrapolation was the source
     of Stage 1.5 v1's censored-high / resolution-flip anomalies).

Bracket-edge outcomes are censored (critical_value = range edge,
bracket_censored "low"/"high") and must never enter the MAP-Elites archive.
After an uncensored bisection, 1-2 probes beyond the critical value on the
regular side measure critical_value_monotone explicitly — bisection assumes
monotonicity and cannot falsify it from its own samples.

`evaluate_genome(task)` is the multiprocessing worker: it logs one
solver_run event per simulation through the task's EventSink (workers never
touch files — LOGGING.md single-writer principle) and returns the
genome_eval payload for the parent to complete (map_cell) and log.
"""

import time

import numpy as np

from ga.genome import Genome, effective_coeffs, realize, shape_descriptors
from ga.logbook import derive_eval_seed, genome_hash
from solver.gclm import solve_gclm
from solver.spectral_utils import energy
from win_condition import InsufficientDataError, WinTier, classify_candidate, estimate_blowup_time

# Cap on inline series length for candidate genome_evals (LOGGING.md: raw
# series only when it matters; decimation keeps the event a bounded size).
_SERIES_MAX_POINTS = 1500


def classify_run(result, oracle):
    """Apply the frozen v2 blow-up predicate to one solver run.

    `oracle` needs: t_max, tail_fraction, predicate_r2_floor,
    t_star_cap_factor. Returns (is_blowup, summary) where summary carries
    the solver_run event fields plus `via` (which rule decided) and
    `fit_below_floor` (amplification-stopped run whose fit failed anyway)."""
    summary = {
        "outcome": result.outcome,
        "early_exit_reason": result.early_exit_reason,
        "t_final": float(result.t_final),
        "n_timesteps": int(result.n_timesteps),
        "dt_min": float(result.dt_min),
        "conservation_drift": float(result.conservation_drift),
        "wall_clock_seconds": float(result.wall_clock_seconds),
        "estimate": None,
        "fit_below_floor": False,
    }
    if result.outcome == "diverged":
        summary["via"] = "diverged_nan"
        return True, summary
    try:
        est = estimate_blowup_time(
            result.times.tolist(), result.max_omega.tolist(),
            tail_fraction=oracle["tail_fraction"], fit_exponent=True,
        )
    except InsufficientDataError:
        if result.outcome == "blowup_candidate":
            summary["via"] = "amplification_insufficient_data"
            return True, summary
        summary["via"] = "insufficient_data_no_amplification"
        return False, summary
    if est is not None:
        summary["estimate"] = {
            "t_star": float(est.t_star), "r_squared": float(est.r_squared),
            "slope": float(est.slope), "exponent": float(est.exponent),
            "last_time": float(est.last_time), "n_points": int(est.n_points),
        }
    fit_ok = est is not None and est.r_squared >= oracle["predicate_r2_floor"]
    if result.outcome == "blowup_candidate":
        summary["via"] = "amplification"
        summary["fit_below_floor"] = not fit_ok
        return True, summary
    within_horizon = (
        est is not None
        and est.t_star <= oracle["t_star_cap_factor"] * oracle["t_max"]
    )
    if fit_ok and within_horizon:
        summary["via"] = "fit"
        return True, summary
    summary["via"] = ("fit_beyond_horizon_cap" if fit_ok
                      else "fit_below_floor_or_none")
    return False, summary


def bisect_critical(run_at, bisection, warm_center=None):
    """Warm-started bisection of the blow-up boundary.

    `run_at(param) -> (is_blowup, summary)`; `bisection` is the config block
    (range, tolerance, warm_start.margin, probe_fractions, max_iters).
    Assumes blow-up at the low (easy) end and regularity at the high end.

    Warm start (PLAN.md compute plan #2): start from warm_center ± margin.
    A failed edge is not wasted: if the warm low end is regular the true
    critical lies below it, so the bracket becomes [range_lo, warm_lo] (and
    symmetrically for the high end) — each such widening counts in
    n_bracket_expansions.

    Returns a dict with critical_value, bracket_censored, initial_bracket,
    n_bracket_expansions, n_bisection_steps, critical_value_monotone,
    monotone_probes, and the full per-run list."""
    lo_full, hi_full = float(bisection["range"][0]), float(bisection["range"][1])
    tol = float(bisection["tolerance"])
    runs = []
    seen = {}

    def ev(param, probe=False):
        param = float(param)
        if param in seen and not probe:
            return seen[param]
        blow, summary = run_at(param)
        runs.append({"param": param, "blowup": bool(blow), "probe": probe,
                     **summary})
        seen[param] = blow
        return blow

    margin = float(bisection["warm_start"]["margin"])
    if warm_center is not None:
        lo = max(lo_full, float(warm_center) - margin)
        hi = min(hi_full, float(warm_center) + margin)
    else:
        lo, hi = lo_full, hi_full
    initial_bracket = [lo, hi]
    n_expansions = 0

    out = {
        "initial_bracket": initial_bracket,
        "critical_value_monotone": None,
        "monotone_probes": [],
        "runs": runs,
    }

    if not ev(lo):
        if lo > lo_full:  # warm low end regular: critical is below it
            n_expansions += 1
            lo, hi = lo_full, lo
        if lo == lo_full and not ev(lo):
            out.update(critical_value=lo_full, bracket_censored="low",
                       n_bracket_expansions=n_expansions, n_bisection_steps=0)
            return out
    if ev(hi):
        if hi < hi_full:  # warm high end still blows up: critical is above it
            n_expansions += 1
            lo, hi = hi, hi_full
        if hi == hi_full and ev(hi):
            out.update(critical_value=hi_full, bracket_censored="high",
                       n_bracket_expansions=n_expansions, n_bisection_steps=0)
            return out

    n_steps = 0
    max_iters = int(bisection.get("max_iters", 30))
    while hi - lo > tol and n_steps < max_iters:
        mid = 0.5 * (lo + hi)
        if ev(mid):
            lo = mid
        else:
            hi = mid
        n_steps += 1
    critical = 0.5 * (lo + hi)

    probes = []
    for frac in bisection.get("probe_fractions", (0.05, 0.15)):
        p = critical + frac * (hi_full - lo_full)
        if p >= hi_full:  # the edge was already established regular
            continue
        blow = ev(p, probe=True)
        probes.append({"param": float(p), "blowup": bool(blow)})
    monotone = all(not p["blowup"] for p in probes) if probes else None

    out.update(critical_value=float(critical), bracket_censored=None,
               n_bracket_expansions=n_expansions, n_bisection_steps=n_steps,
               critical_value_monotone=monotone, monotone_probes=probes)
    return out


def _decimate(times, max_omega, max_points=_SERIES_MAX_POINTS):
    n = len(times)
    stride = max(1, -(-n // max_points))
    idx = list(range(0, n, stride))
    if idx[-1] != n - 1:
        idx.append(n - 1)
    return {
        "times": [float(times[i]) for i in idx],
        "max_omega": [float(max_omega[i]) for i in idx],
        "n_original": n,
        "decimated": stride > 1,
    }


def evaluate_genome(task):
    """Worker entry point: one full fitness evaluation (nu_crit bisection).

    `task` keys: genome_id, generation_index, coeffs, envelope_p, operator,
    parent_ids, warm_center (parent's uncensored critical value or None),
    config (the frozen experiment config), sink (EventSink; may be None for
    inline/test use). Returns the genome_eval payload (without map_cell,
    which the parent adds from its archive geometry).
    """
    cfg = task["config"]
    sink = task.get("sink")
    genome = Genome(coeffs=np.asarray(task["coeffs"], dtype=float),
                    envelope_p=float(task["envelope_p"]))
    n_res = int(cfg["fitness_resolution_N"])
    stop = cfg["stop_criteria"]
    dt_policy = cfg["solver_params"]["dt_policy"]
    oracle = {
        "t_max": stop["t_max"],
        "tail_fraction": cfg["bisection"]["tail_fraction"],
        "predicate_r2_floor": cfg["bisection"]["predicate_r2_floor"],
        "t_star_cap_factor": cfg["bisection"]["t_star_cap_factor"],
    }
    omega0 = realize(genome, n_res, cfg["energy_budget"],
                     cfg.get("bandwidth_cap"))

    t0 = time.perf_counter()
    best = {"r2": -np.inf, "estimate": None, "series": None}

    def run_at(nu):
        result = solve_gclm(
            omega0, a=float(cfg["gclm_a"]), nu=float(nu),
            t_max=stop["t_max"], max_steps=stop["max_steps"],
            amplification_factor=stop["omega_amplification_factor"],
            early_decay_exit=stop["early_decay_exit"],
            dt_max=dt_policy["dt_max"], c1=dt_policy["c1"], c2=dt_policy["c2"],
        )
        blow, summary = classify_run(result, oracle)
        est = summary["estimate"]
        if blow and est is not None and est["r_squared"] > best["r2"]:
            best.update(r2=est["r_squared"], estimate=est,
                        series=(result.times, result.max_omega))
        if sink is not None:
            sink.append_event("solver_run", {
                "generation_index": task["generation_index"],
                "genome_id": task["genome_id"],
                "a": float(cfg["gclm_a"]), "nu": float(nu),
                "resolution_N": n_res,
                "blowup": bool(blow),
                "via": summary["via"],
                "outcome": summary["outcome"],
                "early_exit_reason": summary["early_exit_reason"],
                "wall_clock_seconds": summary["wall_clock_seconds"],
                "n_timesteps": summary["n_timesteps"],
                "dt_min": summary["dt_min"],
                "conservation_drift": summary["conservation_drift"],
                "estimate": est,
                "fit_below_floor": summary["fit_below_floor"],
                "series_path": None,
            })
        return blow, summary

    bis = bisect_critical(run_at, cfg["bisection"],
                          warm_center=task.get("warm_center"))

    win_tier = WinTier.NONE
    if bis["bracket_censored"] is None and best["estimate"] is not None:
        est = best["estimate"]

        class _E:  # minimal shim for classify_candidate
            r_squared = est["r_squared"]

        win_tier = classify_candidate(_E, cfg["tier1_r2_threshold"])

    payload = {
        "generation_index": task["generation_index"],
        "genome_id": task["genome_id"],
        "parent_ids": task["parent_ids"],
        "operator": task["operator"],
        "genome_hash": genome_hash(genome.coeffs, genome.envelope_p),
        "eval_seed": derive_eval_seed(cfg["random_seed"], task["genome_id"]),
        "cache_hit": False,
        "genome_coeffs": [float(c) for c in genome.coeffs],
        "genome_envelope_p": float(genome.envelope_p),
        "energy": float(energy(omega0)),
        "fitness_resolution_N": n_res,
        "fitness_axis": cfg["fitness_axis"],
        "critical_value": bis["critical_value"],
        "bracket_censored": bis["bracket_censored"],
        "critical_value_monotone": bis["critical_value_monotone"],
        "monotone_probes": bis["monotone_probes"],
        "initial_bracket": bis["initial_bracket"],
        "n_bracket_expansions": bis["n_bracket_expansions"],
        "n_bisection_steps": bis["n_bisection_steps"],
        "n_solver_runs": len(bis["runs"]),
        "n_fit_below_floor": sum(r["fit_below_floor"] for r in bis["runs"]),
        "max_conservation_drift_blowup_runs": max(
            (r["conservation_drift"] for r in bis["runs"] if r["blowup"]),
            default=None),
        "wall_clock_seconds": time.perf_counter() - t0,
        "win_tier": win_tier.value,
        "best_estimate": best["estimate"],
        "shape_descriptors": shape_descriptors(genome, cfg["energy_budget"],
                                               cfg.get("bandwidth_cap")),
    }
    if "label" in task:  # baseline_literature profile name
        payload["label"] = task["label"]
    if win_tier is WinTier.CANDIDATE and best["series"] is not None:
        payload["candidate_series"] = _decimate(*best["series"])
    return payload
