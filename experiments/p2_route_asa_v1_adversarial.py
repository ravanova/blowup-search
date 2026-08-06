"""Route-ASA v1 -- the adversarial battery against solver/advection_scope.py.

THE GATE (leg 122, quoted verbatim from DIRECTION.md:2782-2785)
---------------------------------------------------------------
Under an adversarial battery of degenerate or poisoned inputs, does
solver/advection_scope.py ever silently return a wrong result instead of flagging the
input?

  yes -> Silent-corruption gap; report the exact failing case; escalate, do not patch.
  no  -> Confirmed robust; bank the battery as a permanent regression test.

READ-ONLY.  `solver/advection_scope.py` is byte-identical to this leg's merge base under
BOTH branches of the gate.  Every probe below is a measurement; the ones that FAIL are
pinned here and in `test_advection_scope_adversarial.py`, not patched.

WHAT "TRUE" MEANS FOR THE FAR-FIELD PROBES, AND WHERE IT COMES FROM
-------------------------------------------------------------------
Not this leg's invention.  `solver/advection_scope.py`'s own docstring labels the keys of
`transport_at` / `stretch_at` as the weighted piece evaluated AT `X = 1e1, 1e2, 1e3, 1e4`
(lines 184-187), and its §1 states the far-field law `U -> (M/pi) log X`, i.e. the
transport piece GROWS without bound.  So "the value at X = 1e4" has a referent only when
the grid reaches 1e4.  On the module's own default construction path it does not: the
family is the sinh grid `X = c sinh(rho)` with `c = 0.5`, `rho_max = 8`
(`solver/gclm_family.py:102-110`), whose last node is `0.5 sinh 8 ~ 745.24`.  Lesson 73 is
the reference behaviour: when a quantity has no referent, say so instead of bounding it.

THE PROBES ARE FROZEN.  `writeup/novelty/leg_122.md` §3 names ten probes (P1..P10) and
three controls (C1..C3) BEFORE any number here was computed, and nothing outside that list
is reported as this leg's finding.

Deterministic; no RNG anywhere.  Plain float64.  Runtime ~4 min (three Newton solves at
n = 801; the profiles are inputs to the battery, not its product).
"""

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.advection_scope import (advection_split,          # noqa: E402
                                    grading_comparison, profile_mass,
                                    stagnation_point, velocity,
                                    velocity_log_rate)
from solver.profile_newton import TwoScaleNewton, derivative_matrix  # noqa: E402

ALPHA = 1.4          # the operating point of v8-v10, and of test_advection_scope.py
N = 801              # nodes; the battery is about guards, not about resolution
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_asa_v1_adversarial.json")


# ---------------------------------------------------------------------------
# helpers -- every probe reports WHAT CAME BACK, never a bare boolean
# ---------------------------------------------------------------------------

def call(fn):
    """Run `fn`, recording the outcome CATEGORY and the value/exception."""
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            v = fn()
        cats = sorted({x.category.__name__ for x in w})
    except Exception as exc:                                   # noqa: BLE001
        return {"outcome": "raised", "exc_type": type(exc).__name__,
                "exc": str(exc)[:160], "warnings": []}
    return {"outcome": "returned", "value": _j(v), "warnings": cats}


def _j(v):
    """JSON-safe, and NaN/Inf kept as strings so they survive a round trip."""
    if isinstance(v, float):
        if np.isnan(v):
            return "nan"
        if np.isinf(v):
            return "inf" if v > 0 else "-inf"
        return v
    if isinstance(v, (np.floating, np.integer)):
        return _j(float(v))
    if v is None or isinstance(v, (bool, int, str)):
        return v
    if isinstance(v, dict):
        return {str(k): _j(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_j(x) for x in v]
    if isinstance(v, np.ndarray):
        return {"array_summary": {"size": int(v.size),
                                  "n_nonfinite": int((~np.isfinite(v)).sum()),
                                  "first": _j(float(v[0])), "last": _j(float(v[-1]))}}
    return str(v)


def solve(a, rho_max):
    t0 = time.time()
    nw = TwoScaleNewton(a=a, n=N, rho_max=rho_max)
    r = nw.solve()
    return {"nw": nw, "fam": nw.fam, "om": r["Omega"], "c": float(r["c"]),
            "D": derivative_matrix(nw.fam), "a": float(a),
            "rho_max": float(rho_max), "converged": bool(r["converged"]),
            "relres": float(r["relres"]), "seconds": round(time.time() - t0, 1),
            "X_max": float(nw.fam.X.max()), "n": int(nw.fam.X.size)}


# ===========================================================================
def main():
    t_all = time.time()
    res = {"leg": 122, "route": "ASA", "module": "solver/advection_scope.py",
           "module_edited_by_this_leg": False, "alpha": ALPHA, "n_nodes": N,
           "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                    "solver/advection_scope.py ever silently return a wrong result "
                    "instead of flagging the input?")}

    # --- the substrate ------------------------------------------------------
    # DEFAULT grid: rho_max = 8, the default of TwoScaleNewton/GCLMResidual.
    # CONTROL grid: rho_max = 12, whose last node is past X = 1e4 (control C2).
    S = {"a03_r8": solve(0.3, 8.0), "a0_r8": solve(0.0, 8.0),
         "a03_r12": solve(0.3, 12.0)}
    res["substrate"] = {k: {kk: v[kk] for kk in
                            ("a", "rho_max", "n", "X_max", "c", "converged",
                             "relres", "seconds")} for k, v in S.items()}

    d8, d0, d12 = S["a03_r8"], S["a0_r8"], S["a03_r12"]

    # =======================================================================
    # P1 -- np.interp CLAMPING past the last grid node, on the DEFAULT path
    # =======================================================================
    sp8 = advection_split(d8["fam"], d8["om"], d8["a"], ALPHA, d8["D"])
    sp12 = advection_split(d12["fam"], d12["om"], d12["a"], ALPHA, d12["D"])
    t8, t12 = sp8["transport_at"], sp12["transport_at"]
    last8 = float(sp8["transport"][-1])
    s8, s12 = sp8["stretch_at"], sp12["stretch_at"]
    lasts8 = float(sp8["stretch"][-1])

    res["P1_interp_clamp"] = {
        "what": ("transport_at / stretch_at are labelled 'the weighted piece at X = q'. "
                 "On the DEFAULT grid (rho_max=8) the last node is X_max, and the keys "
                 "1e3 and 1e4 lie beyond it; np.interp clamps to the last node."),
        "X_max_default_grid": d8["X_max"],
        "keys_beyond_grid": [q for q in (1e1, 1e2, 1e3, 1e4) if q > d8["X_max"]],
        "transport_at_default": {str(k): float(v) for k, v in t8.items()},
        "transport_value_at_last_node": last8,
        "stretch_at_default": {str(k): float(v) for k, v in s8.items()},
        "stretch_value_at_last_node": lasts8,
        # the tell (lesson 90): the two out-of-grid keys are IDENTICAL to each other
        "transport_1e3_minus_1e4": float(t8[1e4] - t8[1e3]),
        "transport_1e4_minus_last_node": float(t8[1e4] - last8),
        "stretch_1e3_minus_1e4": float(s8[1e4] - s8[1e3]),
        "n_fabricated_values_per_call": int(
            sum(q > d8["X_max"] for q in (1e1, 1e2, 1e3, 1e4)) * 2),
    }

    # --- control C2: the same keys on a grid that CONTAINS them -------------
    honest_1e4 = float(t12[1e4])
    honest_1e3 = float(t12[1e3])
    res["C2_control_grid_that_contains_the_keys"] = {
        "what": ("the same two keys on rho_max=12 (X_max past 1e4), where np.interp "
                 "interpolates honestly. If the default-grid value matched this, P1 "
                 "would be arithmetic and not corruption -- this control CAN come out "
                 "either way."),
        "X_max_control_grid": d12["X_max"],
        "keys_beyond_grid": [q for q in (1e1, 1e2, 1e3, 1e4) if q > d12["X_max"]],
        "transport_at_control": {str(k): float(v) for k, v in t12.items()},
        "reported_1e4_default_grid": float(t8[1e4]),
        "honest_1e4_control_grid": honest_1e4,
        "absolute_error_1e4": float(t8[1e4] - honest_1e4),
        "relative_error_1e4": float((t8[1e4] - honest_1e4) / honest_1e4),
        "reported_1e3_default_grid": float(t8[1e3]),
        "honest_1e3_control_grid": honest_1e3,
        "relative_error_1e3": float((t8[1e3] - honest_1e3) / honest_1e3),
        "in_grid_key_1e2_default_vs_control": [float(t8[1e2]), float(t12[1e2])],
        "relative_error_1e2_in_grid": float((t8[1e2] - t12[1e2]) / t12[1e2]),
    }

    # =======================================================================
    # P2 -- the REQUESTED window is reported; the REALIZED window is not
    # =======================================================================
    vlr8 = velocity_log_rate(d8["fam"], d8["om"])          # defaults lo=10, hi=1e3
    X8 = np.asarray(d8["fam"].X, float)
    sel_fit = (X8 > 10.0) & (X8 < 1e3)
    sel_mass = np.abs(X8) <= 1e3
    sp8_win_hi = 1e4                                       # advection_split default
    sel_fit_split = (X8 > 10.0) & (X8 < sp8_win_hi)
    res["P2_window_requested_vs_realized"] = {
        "what": ("velocity_log_rate returns 'window': [lo, hi] -- the REQUESTED pair -- "
                 "and advection_split reports transport_log_rate with no window at all. "
                 "Neither records where the grid actually stopped."),
        "reported_window": [float(x) for x in vlr8["window"]],
        "realized_fit_window": [float(X8[sel_fit].min()), float(X8[sel_fit].max())],
        "requested_upper_over_realized_upper": float(1e3 / X8[sel_fit].max()),
        "n_fit_nodes": int(sel_fit.sum()),
        "advection_split_requested_hi": sp8_win_hi,
        "advection_split_realized_upper": float(X8[sel_fit_split].max()),
        "advection_split_requested_over_realized": float(
            sp8_win_hi / X8[sel_fit_split].max()),
        # the mass window is |X| <= hi -- a DIFFERENT set from the fit window
        "mass_window_is_two_sided": True,
        "n_mass_nodes": int(sel_mass.sum()),
        "n_fit_nodes_for_comparison": int(sel_fit.sum()),
        "mass_window_min_X": float(X8[sel_mass].min()),
        "measured": float(vlr8["measured"]), "predicted": float(vlr8["predicted"]),
        "predicted_full_domain": float(vlr8["predicted_full_domain"]),
        "predicted_minus_full_domain": float(
            vlr8["predicted"] - vlr8["predicted_full_domain"]),
        "note": ("at rho_max=8 the whole grid is inside |X| <= 1e3, so mass_window and "
                 "mass COINCIDE -- the two 'independent' predictors are the same number "
                 "on the default path (lesson 90: a control that cannot come out "
                 "differently)"),
    }

    # =======================================================================
    # P3 / P4 -- NaN- and Inf-poisoned Omega through all six entry points
    # =======================================================================
    def poisoned(kind):
        om = np.asarray(d8["om"], float).copy()
        i = int(om.size // 2) + 40          # an interior node, well inside the core
        om[i] = {"nan": np.nan, "posinf": np.inf, "neginf": -np.inf}[kind]
        fam, D, X, a, c = d8["fam"], d8["D"], d8["fam"].X, d8["a"], d8["c"]
        return {
            "poisoned_index": i, "poisoned_X": float(X[i]),
            "profile_mass": call(lambda: profile_mass(om, X)),
            "velocity": call(lambda: velocity(fam, om)),
            "velocity_log_rate": call(lambda: velocity_log_rate(fam, om)),
            "advection_split_rate": call(
                lambda: advection_split(fam, om, a, ALPHA, D)["transport_log_rate"]),
            "advection_split_at": call(
                lambda: advection_split(fam, om, a, ALPHA, D)["transport_at"]),
            "advection_split_predicted": call(
                lambda: advection_split(fam, om, a, ALPHA, D)[
                    "transport_predicted_rate"]),
            "grading_comparison_one_scale_rate": call(
                lambda: grading_comparison(fam, om, a, ALPHA, D)["one_scale"][
                    "transport_log_rate"]),
            "stagnation_point": call(lambda: stagnation_point(fam, om, c, a)),
        }

    res["P3_nan_poisoned"] = poisoned("nan")
    res["P4_inf_poisoned"] = {"pos": poisoned("posinf"), "neg": poisoned("neginf")}

    # =======================================================================
    # P5 -- stagnation_point and a NaN in U: sign(nan)=nan, and nan != 0 is TRUE
    # =======================================================================
    om_nan_far = np.asarray(d8["om"], float).copy()
    Xf = np.asarray(d8["fam"].X, float)
    true_star = stagnation_point(d8["fam"], d8["om"], d8["c"], d8["a"])
    # poison a node BEYOND the true crossing, and one BEFORE it
    i_after = int(np.searchsorted(Xf, (true_star or 7.0) * 4.0))
    om_after = om_nan_far.copy(); om_after[i_after] = np.nan
    i_before = int(np.searchsorted(Xf, max((true_star or 7.0) * 0.25, Xf[Xf > 0][2])))
    om_before = om_nan_far.copy(); om_before[i_before] = np.nan
    res["P5_stagnation_nan_bracket"] = {
        "what": ("np.sign(nan) is nan and (nan != 0) is True, so the sign-change search "
                 "can bracket a NON-crossing. Does it return a finite plausible X*?"),
        "true_X_star": _j(true_star),
        "nan_beyond_the_crossing": {"index": i_after, "X": float(Xf[i_after]),
                                    "result": call(lambda: stagnation_point(
                                        d8["fam"], om_after, d8["c"], d8["a"]))},
        "nan_before_the_crossing": {"index": i_before, "X": float(Xf[i_before]),
                                    "result": call(lambda: stagnation_point(
                                        d8["fam"], om_before, d8["c"], d8["a"]))},
    }

    # =======================================================================
    # P6 -- one None for physically opposite states
    # =======================================================================
    U8 = velocity(d8["fam"], d8["om"])
    Xpos = d8["fam"].X > 0
    def eff_stats(c, a):
        e = c + a * U8[Xpos]
        return {"c": float(c), "a": float(a),
                "result": _j(stagnation_point(d8["fam"], d8["om"], c, a)),
                "c_eff_min": float(np.min(e)), "c_eff_max": float(np.max(e)),
                "frac_negative": float(np.mean(e < 0))}
    res["P6_none_is_ambiguous"] = {
        "what": ("stagnation_point returns None for 'no crossing'; the docstring "
                 "explains it only for a=0 where c_eff == c > 0. Three physically "
                 "different states below share the same return value."),
        "documented_case_a0_cpos": eff_stats(d8["c"], 0.0),
        "a0_c_negative_reversed_everywhere": eff_stats(-abs(d8["c"]), 0.0),
        "a_nonzero_c_negative": eff_stats(-abs(d8["c"]), 0.3),
        "genuine_crossing_for_contrast": eff_stats(d8["c"], 0.3),
    }

    # =======================================================================
    # P7 -- the hard-coded one_scale "transport_predicted_rate"
    # =======================================================================
    gc8 = grading_comparison(d8["fam"], d8["om"], d8["a"], ALPHA, d8["D"])
    one, two = gc8["one_scale"], gc8["two_scale"]
    res["P7_one_scale_predicted_rate_is_a_constant"] = {
        "what": ("advection_split hard-codes transport_predicted_rate = 0.0 under "
                 "one_scale (lines 182-183) and publishes it under the same key that "
                 "carries a real prediction a|M|alpha/pi under two_scale."),
        "one_scale_reported_predicted": float(one["transport_predicted_rate"]),
        "one_scale_realized_fit": float(one["transport_log_rate"]),
        "one_scale_abs_discrepancy": float(abs(one["transport_log_rate"]
                                               - one["transport_predicted_rate"])),
        "two_scale_reported_predicted": float(two["transport_predicted_rate"]),
        "two_scale_realized_fit": float(two["transport_log_rate"]),
        "two_scale_rel_discrepancy": float(
            abs(two["transport_log_rate"] - two["transport_predicted_rate"])
            / abs(two["transport_predicted_rate"])),
        # lesson 90: what would have to change in the code for 0.0 to be anything else?
        "one_scale_predicted_under_varied_inputs": {
            f"a={a},alpha={al}": float(advection_split(
                d8["fam"], d8["om"], a, al, d8["D"],
                grading="one_scale")["transport_predicted_rate"])
            for a, al in ((0.0, 1.4), (0.3, 1.4), (0.5, 0.5), (0.9, 2.0))},
    }

    # =======================================================================
    # P8 -- boundary-of-validity alpha (header: "DECAYS for alpha < 2")
    # =======================================================================
    res["P8_alpha_boundary"] = {
        "what": ("the module's header says the stretch piece decays 'for alpha < 2, "
                 "which is the whole working range'. What happens AT and PAST 2, and "
                 "at alpha <= 0?"),
        "rows": {str(al): {
            "stretch_log_rate": _j(float(advection_split(
                d8["fam"], d8["om"], d8["a"], al, d8["D"])["stretch_log_rate"])),
            "transport_log_rate": _j(float(advection_split(
                d8["fam"], d8["om"], d8["a"], al, d8["D"])["transport_log_rate"])),
            "transport_predicted_rate": _j(float(advection_split(
                d8["fam"], d8["om"], d8["a"], al, d8["D"])[
                    "transport_predicted_rate"])),
            "warnings": call(lambda al=al: advection_split(
                d8["fam"], d8["om"], d8["a"], al, d8["D"])["weight_exponent"]
            )["warnings"],
        } for al in (0.0, 1.4, 1.99, 2.0, 2.5, -1.0)},
    }

    # =======================================================================
    # P9 -- degenerate / zero-measure fit windows
    # =======================================================================
    fam8, om8 = d8["fam"], d8["om"]
    Xs = np.sort(Xf[Xf > 0])
    lo7, hi7 = float(Xs[-8]), float(Xs[-1]) * 1.001     # exactly 7 interior nodes
    lo8, hi8 = float(Xs[-9]), float(Xs[-1]) * 1.001     # exactly 8
    res["P9_degenerate_windows"] = {
        "what": ("_log_fit refuses with nan when fewer than 8 nodes are selected "
                 "(line 113-114). Is that guard reached on every degenerate path?"),
        "lo_ge_hi": call(lambda: velocity_log_rate(fam8, om8, lo=1e3, hi=10.0)),
        "lo_le_zero": call(lambda: velocity_log_rate(fam8, om8, lo=-5.0, hi=1e3)),
        "lo_exactly_zero": call(lambda: velocity_log_rate(fam8, om8, lo=0.0, hi=1e3)),
        "empty_window_above_grid": call(
            lambda: velocity_log_rate(fam8, om8, lo=1e6, hi=1e7)),
        "seven_nodes": {"lo": lo7, "hi": hi7,
                        "n_sel": int(((Xf > lo7) & (Xf < hi7)).sum()),
                        "result": call(lambda: velocity_log_rate(
                            fam8, om8, lo=lo7, hi=hi7)["measured"])},
        "eight_nodes": {"lo": lo8, "hi": hi8,
                        "n_sel": int(((Xf > lo8) & (Xf < hi8)).sum()),
                        "result": call(lambda: velocity_log_rate(
                            fam8, om8, lo=lo8, hi=hi8)["measured"])},
        "single_point_domain_profile_mass": call(
            lambda: profile_mass(np.array([1.0]), np.array([2.0]))),
        "reversed_X_profile_mass": {
            "forward": float(profile_mass(om8, Xf)),
            "reversed": call(lambda: profile_mass(om8[::-1], Xf[::-1]))},
    }

    # =======================================================================
    # P10 -- planted wrong values in the non-profile arguments
    # =======================================================================
    n8 = int(Xf.size)
    h_nan = np.ones(n8); h_nan[n8 // 2] = np.nan
    res["P10_planted_arguments"] = {
        "what": "wrong-length h, NaN in h, a = nan, and a plausible grading typo.",
        "grading_typo_two_dash_scale": call(lambda: advection_split(
            fam8, om8, 0.3, ALPHA, d8["D"], grading="two-scale")),
        "grading_empty_string": call(lambda: advection_split(
            fam8, om8, 0.3, ALPHA, d8["D"], grading="")),
        "h_wrong_length": call(lambda: advection_split(
            fam8, om8, 0.3, ALPHA, d8["D"], h=np.ones(7))),
        "h_with_nan": call(lambda: advection_split(
            fam8, om8, 0.3, ALPHA, d8["D"], h=h_nan)["transport_log_rate"]),
        "h_with_nan_predicted": call(lambda: advection_split(
            fam8, om8, 0.3, ALPHA, d8["D"], h=h_nan)["transport_predicted_rate"]),
        "a_is_nan": call(lambda: advection_split(
            fam8, om8, np.nan, ALPHA, d8["D"])["transport_log_rate"]),
        "a_is_inf": call(lambda: advection_split(
            fam8, om8, np.inf, ALPHA, d8["D"])["transport_log_rate"]),
        "D_is_identity_wrong_operator": call(lambda: advection_split(
            fam8, om8, 0.3, ALPHA, np.eye(n8))["transport_log_rate"]),
    }

    # =======================================================================
    # C1 -- the a = 0 negative control: both pieces identically zero
    # =======================================================================
    sp0 = advection_split(d0["fam"], d0["om"], 0.0, ALPHA, d0["D"])
    sp0_a = advection_split(d8["fam"], d8["om"], 0.0, ALPHA, d8["D"])
    res["C1_control_a_zero"] = {
        "what": ("at a = 0 both advection pieces are identically zero (module header "
                 "§2, test_advection_scope.py gate 3). If the battery flagged these it "
                 "would be flagging arithmetic, not corruption."),
        "a0_profile_transport_absmax": float(np.max(np.abs(sp0["transport"]))),
        "a0_profile_stretch_absmax": float(np.max(np.abs(sp0["stretch"]))),
        "a0_coefficient_on_a03_profile_transport_absmax": float(
            np.max(np.abs(sp0_a["transport"]))),
        "a0_transport_at": {str(k): float(v) for k, v in sp0["transport_at"].items()},
        "a0_stagnation_point": _j(stagnation_point(d0["fam"], d0["om"], d0["c"], 0.0)),
        "a0_predicted_rate": float(sp0["transport_predicted_rate"]),
    }

    # =======================================================================
    # C3 -- the loud-failure control
    # =======================================================================
    loud = []
    def walk(node, path=""):
        if isinstance(node, dict):
            if node.get("outcome") == "raised":
                loud.append({"probe": path, "exc_type": node["exc_type"]})
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else str(k))
    walk(res)
    res["C3_loud_failure_control"] = {
        "what": ("a battery in which nothing raises has not reached the guards; one in "
                 "which everything raises has not reached the reachable domain."),
        "n_probes_that_raised": len(loud), "which": loud,
    }

    res["runtime_seconds"] = round(time.time() - t_all, 1)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1, sort_keys=False)
    print(f"wrote {OUT}  ({res['runtime_seconds']} s)")
    return res


if __name__ == "__main__":
    main()
