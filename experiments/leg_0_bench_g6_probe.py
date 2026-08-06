"""Probe for test_fractional_boussinesq.py G6 -- H1..H5 from the novelty pass.

G6 asserts `p > 0 at s=0.10` on `fit_relevance(r, estimate_T(r))["p"]` at the
module's DEFAULT single window (0.40, 0.94).  It measures p = -0.211.

The module's own docstring says the single-window p is the non-robust quantity and
that the window is "the dominant systematic ... SWEPT, NOT CHOSEN".  So the five
discriminators are:

  H1  window sweep -- does p(s=0.10) cross zero as (lo,hi) moves, while the sign at
      s=1.00 and the ordering p(1.00) < p(0.10) stay put?
  H2  pre-asymptoticity -- fit_rms and the drift of p across sub-windows, s=0.10 vs 1.00
  H3  run comparability -- outcome / steps / samples / wall_seconds for both runs
  H4  entitlement -- does collapse_window_report REFUSE on these two runs too?
  H5  instrument defect -- |adv|/|buo| at the peak and min|drv| along the fit window

Stage 1 runs the two G6 solves ONCE and caches them; stage 2 is pure analysis off the
cache, so the sweep cannot cost another 2 x 240 s of wall clock.

Run: .venv/bin/python experiments/leg_0_bench_g6_probe.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.fractional_boussinesq import (  # noqa: E402
    FractionalBoussinesq, collapse_window_report, estimate_T, fit_collapse,
    fit_relevance, houluo_sharp_ic, relevance_exponent,
)

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "leg_0_bench_g6_runs.npz")
KEYS = ("t", "amp", "ratio", "tail", "Lx", "Ly", "Lgrad", "Lspec")
SCAL = ("outcome", "t_final", "steps", "amp0", "n", "nu", "s", "wall_seconds",
        "max_tail")


def get_runs():
    """The two G6 runs, exactly as gate6_relevance_sign builds them."""
    if os.path.exists(CACHE):
        z = np.load(CACHE, allow_pickle=True)
        return {s: {k: z[f"{s}_{k}"] for k in KEYS}
                | {k: z[f"{s}_{k}"].item() for k in SCAL} for s in ("0.1", "1.0")}
    n = 192
    w0, th0 = houluo_sharp_ic(n)
    out, blob = {}, {}
    for s in (0.10, 1.00):
        solver = FractionalBoussinesq(n=n, nu=1e-3, s=s)
        r = solver.run(w0, th0, amp_factor=1e4, sample_every=20, max_steps=100000,
                       wall_max=240.0)
        key = "0.1" if s == 0.10 else "1.0"
        out[key] = r
        for k in KEYS + SCAL:
            blob[f"{key}_{k}"] = np.asarray(r[k])
    np.savez(CACHE, **blob)
    return out


def main():
    runs = get_runs()
    res = {}

    # -- H3: are the two runs even comparable? ------------------------------
    res["h3_run_shape"] = {
        s: {"outcome": str(r["outcome"]), "steps": int(r["steps"]),
            "n_samples": int(r["amp"].size), "wall_seconds": float(r["wall_seconds"]),
            "t_final": float(r["t_final"]),
            "growth": float(r["amp"][-1] / r["amp0"]),
            "max_tail": float(r["max_tail"]),
            "T_est": float(estimate_T(r))}
        for s, r in runs.items()}

    # -- baseline: the gate's own number ------------------------------------
    res["baseline_default_window"] = {
        s: fit_relevance(r, estimate_T(r)) for s, r in runs.items()}

    # -- H1: the window sweep ----------------------------------------------
    wins = [(0.20, 0.94), (0.30, 0.94), (0.40, 0.94), (0.50, 0.94), (0.60, 0.94),
            (0.70, 0.94), (0.40, 0.70), (0.40, 0.80), (0.55, 0.85), (0.70, 0.98),
            (0.50, 0.98), (0.60, 0.99), (0.75, 0.99), (0.80, 0.99), (0.85, 0.99)]
    sweep = []
    for lo, hi in wins:
        row = {"window": [lo, hi]}
        for s, r in runs.items():
            f = fit_relevance(r, estimate_T(r), lo=lo, hi=hi)
            row[s] = {"p": f["p"], "n": f.get("n_points"),
                      "fit_rms": f.get("fit_rms")}
        row["ordering_holds"] = bool(row["1.0"]["p"] < row["0.1"]["p"])
        sweep.append(row)
    res["h1_window_sweep"] = sweep
    p01 = [w["0.1"]["p"] for w in sweep if np.isfinite(w["0.1"]["p"])]
    p10 = [w["1.0"]["p"] for w in sweep if np.isfinite(w["1.0"]["p"])]
    res["h1_summary"] = {
        "p_s0.10_range": [min(p01), max(p01)],
        "p_s0.10_crosses_zero": bool(min(p01) < 0 < max(p01)),
        "p_s0.10_n_windows_positive": int(sum(1 for p in p01 if p > 0)),
        "p_s0.10_n_windows": len(p01),
        "p_s1.00_range": [min(p10), max(p10)],
        "p_s1.00_always_negative": bool(max(p10) < 0),
        "ordering_always_holds": bool(all(w["ordering_holds"] for w in sweep)),
    }

    # -- H2: sub-window drift and fit quality ------------------------------
    res["h2_fit_quality"] = {
        s: {"fit_rms_default": fit_relevance(r, estimate_T(r)).get("fit_rms"),
            "p_drift_across_thirds": [
                fit_relevance(r, estimate_T(r), lo=lo, hi=hi)["p"]
                for lo, hi in ((0.40, 0.62), (0.58, 0.80), (0.76, 0.98))]}
        for s, r in runs.items()}

    # -- H4: is either run entitled to quote a collapse exponent? ----------
    res["h4_entitlement"] = {
        s: collapse_window_report(r, estimate_T(r)) for s, r in runs.items()}

    # -- the beta_eff arithmetic the novelty pass pre-registered -----------
    res["beta_eff"] = {}
    for s, r in runs.items():
        sv = float(s)
        p = fit_relevance(r, estimate_T(r))["p"]
        fc = fit_collapse(r, estimate_T(r))
        res["beta_eff"][s] = {
            "p": p, "beta_eff_from_p": (1.0 - p) / (2.0 * sv),
            "beta_geometric_Lgrad": fc["Lgrad"], "beta_Lx": fc["Lx"],
            "beta_Ly": fc["Ly"], "amp_exponent": fc["amp_exponent"],
            "p_predicted_from_geometric_beta":
                float(relevance_exponent(sv, fc["Lgrad"]))}

    # -- H5: instrument sanity on these very runs --------------------------
    res["h5_instrument"] = {
        s: {"ratio_min": float(r["ratio"].min()), "ratio_max": float(r["ratio"].max()),
            "ratio_any_nonpositive": bool(np.any(r["ratio"] <= 0)),
            "ratio_first": float(r["ratio"][0]), "ratio_last": float(r["ratio"][-1])}
        for s, r in runs.items()}

    print(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
