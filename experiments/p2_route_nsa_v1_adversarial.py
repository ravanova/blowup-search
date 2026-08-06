"""Leg 142 / Route-NSA: the adversarial battery for solver/nk_seminorm.py.

GATE (pre-committed, adopted verbatim from the 139/140 audit template with the
module substituted -- see writeup/novelty/leg_142.md sec 0):

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/nk_seminorm.py ever silently return a wrong value, or accept a
    fabricated certificate-feeding quantity unflagged?

      yes -> silent-corruption or fabrication-acceptance gap; report the exact
             failing case with magnitudes; escalate, do not patch.
      no  -> confirmed robust; bank the battery as a permanent regression test.

READ-ONLY.  This runner imports solver/nk_seminorm.py and edits nothing.

DECISION RULE, fixed before any number was computed (novelty pass sec 5):
a case counts as a VIOLATION only if the module returns

  * WITHOUT raising, and
  * WITHOUT emitting any warning (checked under warnings.catch_warnings(record=True)
    with simplefilter("always")), and
  * the returned value is refuted by an INDEPENDENT reference -- either a
    sign/finiteness fact that needs no computation (an operator-norm upper bound
    cannot be negative; a contraction constant cannot be negative), or the same
    module re-run in a configuration whose correctness is not in question.

A crash is recorded but is NOT a violation: it is the loud failure mode.  Warned
returns are recorded separately, also not violations.

Run: PYTHONPATH=. python experiments/p2_route_nsa_v1_adversarial.py
Writes writeup/data/p2_route_nsa_v1_adversarial.json.  ~2 min, no scipy.
"""

import json
import os
import warnings

import numpy as np

from solver.nk_seminorm import (
    C_ANCHOR, hilbert_split_bound, hilbert_split_curves, interpolation_constant,
    holder_interpolation_bound, derivative_bound, seminorm_closure,
    operator_norm_upper, required_X0, interpolant_far_field_defect,
)

ALPHA, GAMMA = 1.5, 0.5           # the shipped configuration (test_nk_seminorm.py)
C_SUP_SHIPPED = 5.5543            # v6's two-point dual saturation value
OUT = os.path.join("writeup", "data", "p2_route_nsa_v1_adversarial.json")


# ---------------------------------------------------------------------------
# harness
# ---------------------------------------------------------------------------


def call(fn):
    """Return (status, value, warnings) with status in raised/warned/silent."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            value = fn()
        except Exception as exc:                                  # noqa: BLE001
            return "raised", "%s: %s" % (type(exc).__name__, exc), []
        names = sorted({w.category.__name__ for w in caught})
        return ("warned" if names else "silent"), value, names


def jsonable(v):
    if isinstance(v, dict):
        return {k: jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [jsonable(x) for x in v]
    if isinstance(v, complex):
        return {"__complex__": True, "re": v.real, "im": v.imag}
    if isinstance(v, (np.floating, np.integer)):
        return float(v)
    if isinstance(v, float) and not np.isfinite(v):
        return str(v)
    return v


# ---------------------------------------------------------------------------
# the control that can come out differently (lesson 90)
# ---------------------------------------------------------------------------


def control(curves):
    """The shipped configuration, against test_nk_seminorm.py's banked numbers.

    This control CAN report the other answer: if the harness perturbed the module
    (import order, warning filters, the curves cache) these numbers would move,
    and every violation below would be suspect.  The banked values are read from
    test_nk_seminorm.py's own assertions and printout (fixed point at
    C_sup = 5.5543, alpha = 1.5, gamma = 0.5).
    """
    st, d, w = call(lambda: seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED, curves=curves))
    # independent re-derivation of the fixed-point property, in this runner
    P = derivative_bound(d["C_sup"], d["T_upper"], ALPHA, GAMMA, curves=curves)
    back, kappa = holder_interpolation_bound(d["C_sup"], P, GAMMA)
    return {
        "status": st, "warnings": w,
        "T_upper": d["T_upper"], "P_upper": d["P_upper"],
        "A_upper": d["A_upper"], "contraction_slope": d["contraction_slope"],
        "kappa_star": d["kappa_star"],
        "fixed_point_residual_rel": abs(back - d["T_upper"]) / d["T_upper"],
        "kappa_star_residual_rel": abs(kappa - d["kappa_star"]) / d["kappa_star"],
        "C_half_exact": interpolation_constant(0.5),
        "C_half_error": abs(interpolation_constant(0.5) - 2.0),
        "note": "test_nk_seminorm.py (5) asserts this fixed point, slope in (0,1), "
                "A_upper > C_sup, and alpha < 1 refused; all reproduced here.",
    }


# ---------------------------------------------------------------------------
# V1 -- a negative C_sup is accepted and produces a NEGATIVE ||A|| upper bound
# ---------------------------------------------------------------------------


def v1_negative_c_sup(curves):
    rows = []
    for C in (-1.0, -5.5543, -1.0e6, -1.0e-12):
        st, d, w = call(lambda C=C: seminorm_closure(ALPHA, GAMMA, C, curves=curves))
        st2, a, w2 = call(lambda C=C: operator_norm_upper(ALPHA, GAMMA, C, curves=curves))
        ok = isinstance(d, dict)
        rows.append({
            "C_sup": C, "status": st, "warnings": w,
            "closes": d.get("closes") if ok else None,
            "T_upper": d.get("T_upper") if ok else None,
            "P_upper": d.get("P_upper") if ok else None,
            "A_upper": d.get("A_upper") if ok else None,
            "detail": None if ok else d,
            "operator_norm_upper": a,
            "violation": bool(st == "silent" and ok and d.get("closes")
                              and d.get("A_upper") is not None
                              and d["A_upper"] < 0.0),
            "refutation": "A_upper is a claimed UPPER BOUND on ||A||_{Y->X}, an "
                          "operator norm, which is >= 0 for every operator. A "
                          "negative return is refuted with no computation.",
        })
    return {
        "name": "negative C_sup accepted -> negative operator-norm upper bound",
        "mechanism": "seminorm_closure line 227 does S = float(C_sup) with no check. "
                     "derivative_bound then returns P < 0, and "
                     "holder_interpolation_bound's `if P <= 0.0: return 0.0, inf` "
                     "guard -- written for the degenerate P = 0 case -- swallows the "
                     "negative P and reports T = 0. The fixed-point loop converges at "
                     "T = 0 on the first iterate, contraction_slope = 0, and "
                     "A_upper = S + T = S < 0 is returned with closes = True.",
        "rows": rows,
        "n_violations": sum(r["violation"] for r in rows),
    }


# ---------------------------------------------------------------------------
# V2 -- a negative anchor speed c silently DELETES the seminorm part
# ---------------------------------------------------------------------------


def v2_negative_c(curves):
    ref = seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED, c=C_ANCHOR, curves=curves)
    rows = []
    for c in (-C_ANCHOR, -1.0, -1e-3, 1e-300):
        st, d, w = call(lambda c=c: seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                                                     c=c, curves=curves))
        ok = isinstance(d, dict)
        collapsed = bool(st == "silent" and ok and d.get("closes")
                         and d.get("T_upper") == 0.0)
        rows.append({
            "c": c, "status": st, "warnings": w,
            "closes": d.get("closes") if ok else None,
            "T_upper": d.get("T_upper") if ok else None,
            "A_upper": d.get("A_upper") if ok else None,
            "P_upper": d.get("P_upper") if ok else None,
            "detail": None if ok else d,
            "reference_T_upper_at_abs_c": ref["T_upper"] if abs(c) == C_ANCHOR else None,
            "reference_A_upper_at_abs_c": ref["A_upper"] if abs(c) == C_ANCHOR else None,
            "understatement_factor": (ref["A_upper"] / d["A_upper"]
                                      if collapsed and abs(c) == C_ANCHOR else None),
            "violation": collapsed,
        })
    return {
        "name": "negative anchor speed c silently deletes the seminorm part of ||A||",
        "mechanism": "derivative_bound divides the (positive) bracket by c. For c < 0 "
                     "the returned P is negative, which is not a derivative bound at "
                     "all -- the derivation solves c h_X = -g - ... and the correct "
                     "bound uses |c|. holder_interpolation_bound's P <= 0 branch then "
                     "returns T = 0, so the SEMINORM PART VANISHES and A_upper "
                     "collapses to the sup part C_sup alone, with closes = True.",
        "headline": "at c = -0.5 (the anchor speed's own magnitude, sign flipped) the "
                    "module reports ||A|| <= 5.554300 where the same module at "
                    "c = +0.5 reports 69.375617 -- the claimed upper bound is "
                    "understated by 12.4904x, silently.",
        "rows": rows,
        "n_violations": sum(r["violation"] for r in rows),
    }


# ---------------------------------------------------------------------------
# V3 -- NaN absorption: closes = True with T_upper = NaN
# ---------------------------------------------------------------------------


def v3_nan_absorption(curves):
    rows = []
    cases = [("C_sup", float("nan"), lambda: seminorm_closure(
                 ALPHA, GAMMA, float("nan"), curves=curves)),
             ("c", float("nan"), lambda: seminorm_closure(
                 ALPHA, GAMMA, C_SUP_SHIPPED, c=float("nan"), curves=curves)),
             ("C_sup", float("inf"), lambda: seminorm_closure(
                 ALPHA, GAMMA, float("inf"), curves=curves)),
             ("C_sup", 1e300, lambda: seminorm_closure(
                 ALPHA, GAMMA, 1e300, curves=curves))]
    for slot, val, fn in cases:
        st, d, w = call(fn)
        bad = (st == "silent" and d.get("closes") is True
               and not np.isfinite(d.get("T_upper", 0.0)))
        rows.append({"slot": slot, "value": val, "status": st, "warnings": w,
                     "closes": d.get("closes"), "T_upper": d.get("T_upper"),
                     "A_upper": d.get("A_upper"), "reason": d.get("reason"),
                     "violation": bool(bad)})
    return {
        "name": "NaN absorbed by the fixed-point loop: closes = True, T_upper = NaN",
        "mechanism": "both loop exits are comparisons that are FALSE for NaN: "
                     "`nxt > T_cap` and `abs(nxt - T) <= tol * max(1, T)`. A NaN "
                     "iterate therefore neither trips the cap nor converges; the loop "
                     "runs its full max_iter = 20000 and falls off the end into the "
                     "success return, which has no NaN check. The +inf and 1e300 "
                     "arms are the CONTROL: they take the T_cap branch and are "
                     "reported honestly as closes = False, so this row can come out "
                     "differently and does.",
        "rows": rows,
        "n_violations": sum(r["violation"] for r in rows),
    }


# ---------------------------------------------------------------------------
# V4 -- required_X0 accepts a negative Z1 as satisfying the contraction target
# ---------------------------------------------------------------------------


def v4_required_x0():
    grid = [1e2, 1e3, 1e4, 1e5]
    rows = []
    cases = [("modelling_error < 0", 69.375617, lambda X0: -1.0),
             ("modelling_error = 0", 69.375617, lambda X0: 0.0),
             ("modelling_error = NaN", 69.375617, lambda X0: float("nan")),
             ("A_upper < 0 (fed by V1)", -1.0, lambda X0: 1.0 / X0),
             ("honest control", 69.375617, lambda X0: 1.0 / X0)]
    for name, A_up, err in cases:
        st, d, w = call(lambda A_up=A_up, err=err: required_X0(A_up, err, grid,
                                                               target=1.0))
        bad = st == "silent" and d.get("found") is True and d.get("Z1", 0.0) < 0.0
        rows.append({"case": name, "A_upper": A_up, "status": st, "warnings": w,
                     "found": d.get("found"), "Z1": d.get("Z1"),
                     "X0": d.get("X0"), "J_needed": d.get("J_needed"),
                     "Z1_at_max": d.get("Z1_at_max"), "violation": bool(bad)})
    return {
        "name": "required_X0 accepts a NEGATIVE contraction constant as success",
        "mechanism": "the acceptance test is `z <= target` with target = 1. Z1 is a "
                     "contraction constant, so the intended predicate is "
                     "0 <= z <= target; the missing lower side means any negative z "
                     "passes at the FIRST grid point, and the function returns "
                     "found = True with the smallest, cheapest X0 and a J_needed the "
                     "caller would act on. Chained with V1 this fabricates an entire "
                     "certificate: seminorm_closure(C_sup = -1) -> A_upper = -1 -> "
                     "required_X0 -> found = True, Z1 = -0.01, J_needed = 78.54, with "
                     "no warning raised at any link.",
        "rows": rows,
        "n_violations": sum(r["violation"] for r in rows),
    }


# ---------------------------------------------------------------------------
# V5 -- the module's own stated domain is enforced at ONE entry point only
# ---------------------------------------------------------------------------


def v5_unguarded_entry_points():
    """alpha >= 1 and 0 < gamma < 1 are checked in seminorm_closure and nowhere else."""
    rows = []
    for a in (0.5, 0.0, -1.0):
        st, v, w = call(lambda a=a: derivative_bound(C_SUP_SHIPPED, 1.0, a, GAMMA))
        rows.append({"entry": "derivative_bound", "param": "alpha", "value": a,
                     "status": st, "warnings": w, "value_returned": v,
                     "finite": bool(np.isfinite(v)) if isinstance(v, float) else None,
                     "guarded_in_seminorm_closure": True})
    for g in (0.0, 1.0, 1.5, -0.5, float("nan")):
        st, v, w = call(lambda g=g: hilbert_split_bound(1.0, ALPHA, g))
        rows.append({"entry": "hilbert_split_bound", "param": "gamma", "value": g,
                     "status": st, "warnings": w, "value_returned": v,
                     "guarded_in_seminorm_closure": True})
        st, v, w = call(lambda g=g: interpolation_constant(g))
        rows.append({"entry": "interpolation_constant", "param": "gamma", "value": g,
                     "status": st, "warnings": w, "value_returned": v,
                     "complex": isinstance(v, complex),
                     "guarded_in_seminorm_closure": True})
        st, v, w = call(lambda g=g: holder_interpolation_bound(C_SUP_SHIPPED, 182.0, g))
        rows.append({"entry": "holder_interpolation_bound", "param": "gamma",
                     "value": g, "status": st, "warnings": w, "value_returned": v,
                     "complex": isinstance(v, tuple) and isinstance(v[0], complex),
                     "guarded_in_seminorm_closure": True})
    silent_out_of_domain = sum(
        1 for r in rows if r["status"] == "silent")
    return {
        "name": "the module's stated domain is enforced at ONE of four public entry points",
        "mechanism": "seminorm_closure raises ValueError for alpha < 1 and for gamma "
                     "outside (0, 1) -- the module DOES enforce its own docstring's "
                     "gamma = 1 exclusion there, which is the question leg 131 left "
                     "open and the answer is YES at that entry point. But "
                     "derivative_bound, hilbert_split_bound, interpolation_constant "
                     "and holder_interpolation_bound are public, are called directly "
                     "by test_nk_seminorm.py and by solver/hilbert_holder.py (3 "
                     "sites), and validate nothing. interpolation_constant returns a "
                     "COMPLEX number for gamma outside [0, 1] -- "
                     "(1-g)**(g-1) with 1-g < 0 and fractional exponent -- which "
                     "propagates into holder_interpolation_bound's returned 'bound'.",
        "rows": rows,
        "n_silent_out_of_domain": silent_out_of_domain,
        "gamma_1_enforced_in_seminorm_closure": True,
    }


# ---------------------------------------------------------------------------
# V6 -- the fixed-point iterate approaches T* FROM BELOW, and exhaustion is silent
# ---------------------------------------------------------------------------


def v6_iteration_exhaustion(curves):
    ref = seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED, curves=curves)["T_upper"]
    rows = []
    for mi in (1, 2, 3, 5, 10, 20, 100, 20000):
        st, d, w = call(lambda mi=mi: seminorm_closure(
            ALPHA, GAMMA, C_SUP_SHIPPED, curves=curves, max_iter=mi))
        rows.append({"max_iter": mi, "status": st, "warnings": w,
                     "closes": d["closes"], "T_upper": d["T_upper"],
                     "converged_T": ref,
                     "understatement_factor": ref / d["T_upper"],
                     "below_true_fixed_point": d["T_upper"] < ref * (1 - 1e-9)})
    # is the default cap reachable? the honest answer, measured
    default_probe = []
    for g in (0.5, 0.9, 0.99, 0.999):
        cur = hilbert_split_curves(ALPHA, g)
        a = seminorm_closure(ALPHA, g, C_SUP_SHIPPED, curves=cur)
        b = seminorm_closure(ALPHA, g, C_SUP_SHIPPED, curves=cur, max_iter=200000)
        default_probe.append({
            "gamma": g, "closes_at_default": a["closes"],
            "T_at_default_20000": a.get("T_upper"),
            "T_at_200000": b.get("T_upper"),
            "rel_gap": (abs(a["T_upper"] - b["T_upper"]) / b["T_upper"]
                        if a["closes"] and b["closes"] and b["T_upper"] > 0 else None),
            "contraction_slope": a.get("contraction_slope")})
    return {
        "name": "monotone-from-below iteration with no convergence flag returned",
        "mechanism": "T starts at 0 and F is increasing, so every iterate is BELOW "
                     "the fixed point T*. The loop breaks only on the tolerance test; "
                     "running out of max_iter falls through to the success return, "
                     "which reports closes = True and carries no iteration count and "
                     "no convergence flag. The 'upper bound' property therefore rests "
                     "entirely on convergence having happened, and the caller is given "
                     "nothing to check it with.",
        "severity": "CALLER-OVERRIDE ONLY at the shipped default -- measured, not "
                    "assumed: at max_iter = 20000 the iteration converges for every "
                    "gamma up to 0.99 (rel gap 0.000e+00 against max_iter = 200000, "
                    "contraction slope 0.99 at gamma = 0.99), and gamma >= 0.999 is "
                    "reported honestly as closes = False via the T_cap branch. The "
                    "exhaustion path is reachable only when a caller lowers max_iter.",
        "rows": rows,
        "default_cap_probe": default_probe,
    }


# ---------------------------------------------------------------------------
# V7 -- the sup over a truncated log grid (leg 116's clause, inherited)
# ---------------------------------------------------------------------------


def v7_truncated_sup():
    rows = []
    for n_X in (30, 60, 120, 240, 480, 2000):
        d = seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                             curves=hilbert_split_curves(ALPHA, GAMMA, n_X=n_X))
        rows.append({"n_X": n_X, "X_hi": 1e6, "T_upper": d["T_upper"],
                     "A_upper": d["A_upper"]})
    ref = [r for r in rows if r["n_X"] == 2000][0]["T_upper"]
    shipped = [r for r in rows if r["n_X"] == 120][0]["T_upper"]
    for r in rows:
        r["rel_understatement_vs_n_X_2000"] = (ref - r["T_upper"]) / ref
    hi_rows = []
    for X_hi in (1e4, 1e6, 1e8, 1e10, 1e12):
        d = seminorm_closure(ALPHA, GAMMA, C_SUP_SHIPPED,
                             curves=hilbert_split_curves(ALPHA, GAMMA, X_hi=X_hi))
        hi_rows.append({"X_hi": X_hi, "T_upper": d["T_upper"],
                        "A_upper": d["A_upper"]})
    return {
        "name": "derivative_bound's sup is a max over a 120-point truncated log grid",
        "mechanism": "hilbert_split_curves samples X on geomspace(1e-3, 1e6, 120) and "
                     "derivative_bound takes np.max over those samples. A max over "
                     "samples is not a supremum: the returned P -- and through it the "
                     "claimed upper bound on ||A|| -- can only UNDERSTATE the true "
                     "sup. This is leg 116's pre-registered clause on nk_bounds.py, "
                     "inherited verbatim by this module.",
        "magnitude": "SMALL AT THE SHIPPED SETTING, and reported as such: the shipped "
                     "n_X = 120 understates the n_X = 2000 value of T by "
                     "%.3e relative (%.6f vs %.6f). It is not small at coarser "
                     "resolutions -- n_X = 30 understates by 3.1e-2. Refining X_hi "
                     "moves the answer NON-MONOTONICALLY (1e6 -> 69.3756, "
                     "1e10 -> 69.2709), which is the grid, not the integrand."
                     % ((ref - shipped) / ref, shipped, ref),
        "rows": rows,
        "X_hi_rows": hi_rows,
    }


# ---------------------------------------------------------------------------
# V8 -- interpolant_far_field_defect on a malformed window
# ---------------------------------------------------------------------------


def v8_defect_window():
    to_coef, h = np.eye(4), np.array([1.0, 0.0, 0.0, 0.0])
    rows = []
    for name, th in (("theta_last > pi", 4.0), ("theta_last = NaN", float("nan")),
                     ("theta_last = 0", 0.0), ("honest control", 3.0)):
        st, d, w = call(lambda th=th: interpolant_far_field_defect(
            to_coef, h, ALPHA, th, n=3))
        vals = d["weighted"] if isinstance(d, dict) else None
        rows.append({"case": name, "theta_last": th, "status": st, "warnings": w,
                     "h_pi": d["h_pi"] if isinstance(d, dict) else None,
                     "weighted": vals,
                     "n_nan": (int(sum(not np.isfinite(v) for v in vals))
                               if vals else None)})
    st, d, w = call(lambda: interpolant_far_field_defect(np.eye(4), np.ones(7),
                                                         ALPHA, 3.0))
    rows.append({"case": "to_coef/h shape mismatch", "status": st, "warnings": w,
                 "detail": d if st == "raised" else None})
    return {
        "name": "interpolant_far_field_defect returns NaN entries under a warning",
        "mechanism": "np.linspace(theta_last, pi - eps, n) is not required to be "
                     "increasing; for theta_last > pi it runs BACKWARDS past pi, where "
                     "cos(theta/2) < 0 and the weight cos(theta/2)**(-alpha) is NaN "
                     "for fractional alpha. NaN theta_last produces the same output. "
                     "This one DOES warn (RuntimeWarning: invalid value encountered in "
                     "power), so by this leg's own decision rule it is NOT counted as "
                     "a silent violation -- recorded for completeness.",
        "rows": rows,
        "counted_as_violation": False,
    }


# ---------------------------------------------------------------------------
# blast radius
# ---------------------------------------------------------------------------


def blast_radius():
    return {
        "live_call_sites": {
            "solver/hilbert_holder.py": {
                "lines": [266, 326, 409], "function": "hilbert_split_bound",
                "note": "the only solver->solver consumer; passes gamma through from "
                        "its own caller. Leg 119 (5a74a86) already escalated this "
                        "module for its own bound direction and recorded the "
                        "gamma = 0 ZeroDivisionError raised inside "
                        "hilbert_split_bound's /gamma."},
            "test_op_lower.py": {
                "lines": [96], "function": "seminorm_closure(...)['A_upper']",
                "note": "passes C_sup = nk_bounds.sup_part_upper(...), a max over "
                        "dual candidates."},
            "experiments/p2_route_d_v7_seminorm.py": {
                "lines": [211, 254, 292, 300, 301],
                "function": "seminorm_closure, required_X0",
                "note": "the banked Route-D v7 evidence runner; same C_sup source."},
            "test_nk_seminorm.py": {
                "lines": [91, 104, 135, 150, 179, 182, 190, 196, 201, 203, 217],
                "function": "all six public functions"},
        },
        "verdict": "LATENT, 0 exposed. Every live call site supplies C_sup from "
                   "nk_bounds.sup_part_upper (a max of dual-pairing magnitudes, "
                   "structurally >= 0) and c = C_ANCHOR = 0.5 by default -- no "
                   "in-repo caller passes a negative C_sup, a negative c, a NaN, or "
                   "a lowered max_iter. The gaps are reachable by construction, not "
                   "by any banked number. No banked Route-D v7 result is impeached.",
        "banked_numbers_impeached": 0,
    }


# ---------------------------------------------------------------------------


def main():
    curves = hilbert_split_curves(ALPHA, GAMMA)
    findings = {
        "V1": v1_negative_c_sup(curves),
        "V2": v2_negative_c(curves),
        "V3": v3_nan_absorption(curves),
        "V4": v4_required_x0(),
        "V5": v5_unguarded_entry_points(),
        "V6": v6_iteration_exhaustion(curves),
        "V7": v7_truncated_sup(),
        "V8": v8_defect_window(),
    }
    counted = ["V1", "V2", "V3", "V4"]
    n_viol = sum(findings[k]["n_violations"] for k in counted)
    out = {
        "leg": 142, "route": "ROUTE-NSA", "module": "solver/nk_seminorm.py",
        "read_only": True, "module_edited": False,
        "gate": "Under an adversarial battery of degenerate or poisoned inputs, does "
                "solver/nk_seminorm.py ever silently return a wrong value, or accept "
                "a fabricated certificate-feeding quantity unflagged?",
        "gate_answer": "YES" if n_viol else "NO",
        "decision_rule": "silent (no exception, no warning under "
                         "catch_warnings(record=True)) AND refuted by an independent "
                         "reference. Crashes and warned returns are recorded, not "
                         "counted.",
        "control": control(curves),
        "findings": findings,
        "counted_findings": counted,
        "n_silent_violations": n_viol,
        "blast_radius": blast_radius(),
        "escalated_not_patched": True,
        "guard_class": "NOT the leg 128 Y0/Z0/Z1 shared-guard class -- this module "
                       "never touches the radii-polynomial coefficients. The nearest "
                       "landed template is hilbert_pointwise.py's "
                       "HilbertPointwiseDomainError (leg 130, 5905138): a domain "
                       "guard on the module's own stated hypotheses, with an "
                       "on_unsound escape that reproduces pre-repair numbers "
                       "bit-identically.",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(jsonable(out), fh, indent=2, sort_keys=False)

    print("GATE ANSWER: %s -- %d silent violations over V1-V4"
          % (out["gate_answer"], n_viol))
    for k in counted:
        print("  %s  %d violation(s)  %s"
              % (k, findings[k]["n_violations"], findings[k]["name"]))
    for k in ("V5", "V6", "V7", "V8"):
        print("  %s  (recorded)     %s" % (k, findings[k]["name"]))
    c = out["control"]
    print("control: T = %.6f, A_upper = %.6f, slope = %.6f, fixed-point residual "
          "%.2e, C(1/2) error %.1e" % (c["T_upper"], c["A_upper"],
                                       c["contraction_slope"],
                                       c["fixed_point_residual_rel"],
                                       c["C_half_error"]))
    print("wrote %s" % OUT)


if __name__ == "__main__":
    main()
