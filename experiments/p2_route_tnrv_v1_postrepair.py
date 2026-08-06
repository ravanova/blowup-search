#!/usr/bin/env python3
"""Leg 230 -- Route-TNRV: INDEPENDENT post-repair verification of leg 220's domain-guard fix.

Leg 220 (landed on `main` at a516ef8) repaired `solver/target_norm.py`'s domain guard to
window on the true data interval [X.min(), X.max()] rather than on |X|.max().  Every number
in leg 220's report was produced by leg 220's own runner.  This runner re-derives the two
load-bearing claims along a path that shares no code with it.

THE GATE (pre-committed, both branches, verbatim):

    "Does an independent re-run confirm the asymmetric-grid extrapolation case is now
     correctly flagged (`n_outside_grid>0`/`domain_valid=False`), with leg 55's own banked
     margins bit-identical?"

PART A -- FLAGGING, against a CLOSED FORM and not against a re-implementation.
---------------------------------------------------------------------------
The module samples the staggered grid  theta_j = -pi + 2 pi (j + 1/2) / M,  j = 0..M-1,
and maps it by  X_j = tan(theta_j / 2).  Since tan(./2) is strictly increasing on (-pi, pi),
X_j lies in the data interval [X_lo, X_hi] iff theta_j lies in [t_lo, t_hi] with
t_lo = 2 arctan(X_lo), t_hi = 2 arctan(X_hi).  Writing u = M (t + pi) / (2 pi) - 1/2 for the
real index at angle t:

    #{j : theta_j < t_lo}  =  clamp( ceil(u_lo),      0, M )      (u_lo = u(t_lo))
    #{j : theta_j > t_hi}  =  clamp( M - 1 - floor(u_hi), 0, M )  (u_hi = u(t_hi))

so the true outside-count is the SUM of two integers obtained from two ceil/floor
evaluations.  No array is built, no module function is called, and the arithmetic is not
the module's.  If the module's reported `n_outside_grid` equals this, the agreement is not
a tautology of shared code.

The pre-repair guard used `|X_t| <= max|X|` instead, i.e. the SYMMETRIC window
[-X_max, +X_max].  The same closed form evaluated on that window gives what leg 220's fix
was supposed to move away from, and is reported alongside as the anti-tautology control:
on a symmetric grid the two windows coincide and the two counts MUST agree; on an
asymmetric grid they must differ.  A control that cannot come out both ways is not a
control (lesson 90).

PART B -- LEG 55'S BANKED MARGINS, re-solved from scratch.
---------------------------------------------------------
Two real bordered Newton solves through leg 55's own `nb5_norms`, compared with `==` on raw
float64 -- never `allclose` -- against the constants read out of
`writeup/data/p2_route_nb_v1_targetnorm.json` by this runner.  All FOUR classes are checked
(leg 220 quoted two), plus the exponent p, plus the independent identity margin = p - s - 1
evaluated in plain Python here.

`solver/target_norm.py` is READ-ONLY to this leg and is not modified.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from solver.target_norm import (                       # noqa: E402
    TargetNormDomainWarning, spectrum, fit_exponent, weighted_partial_sums,
    analytic_tail, norm_verdict, calibration_family,
)

NB_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_nb_v1_targetnorm.json")
OUT_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_tnrv_v1_postrepair.json")

M_PROBE = 16384          # leg 55's headline transform size, so the counts are comparable
C_SINH = 0.5


# ==========================================================================
# PART A helpers -- the closed form.  Deliberately plain Python.
# ==========================================================================
def _real_index_at_angle(t, M):
    """The real j solving theta_j = t, i.e. u = M (t + pi) / (2 pi) - 1/2."""
    return M * (t + math.pi) / (2.0 * math.pi) - 0.5


def closed_form_outside(X_lo, X_hi, M):
    """#{j : X_j < X_lo or X_j > X_hi} on the staggered grid, in closed form.

    Returns (n_below, n_above, n_total).  Never builds an array.
    """
    M = int(M)
    t_lo = 2.0 * math.atan(float(X_lo))
    t_hi = 2.0 * math.atan(float(X_hi))
    u_lo = _real_index_at_angle(t_lo, M)
    u_hi = _real_index_at_angle(t_hi, M)
    n_below = min(max(math.ceil(u_lo), 0), M)
    n_above = min(max(M - 1 - math.floor(u_hi), 0), M)
    return int(n_below), int(n_above), int(n_below + n_above)


def prerepair_closed_form_outside(X_abs_max, M):
    """The SAME closed form on the pre-repair SYMMETRIC window [-max|X|, +max|X|]."""
    return closed_form_outside(-float(X_abs_max), float(X_abs_max), M)


def brute_force_outside(X_lo, X_hi, M):
    """A third, independent, O(M) count.  Guards the closed form's own ceil/floor edges."""
    j = np.arange(int(M))
    th = -np.pi + 2.0 * np.pi * (j + 0.5) / int(M)
    Xt = np.tan(0.5 * th)
    return int(((Xt < float(X_lo)) | (Xt > float(X_hi))).sum())


# ==========================================================================
# PART A -- this leg's OWN asymmetric rungs
# ==========================================================================
# Leg 220's five rungs all held X_hi fixed and walked X_lo.  These differ in KIND:
# a right-truncated rung, a two-sided offset rung, a rung whose data interval does not
# contain zero at all, a tiny window, and a near-symmetric rung with a small count.
# ALPHA is the calibration family's branch order: p = 1 + alpha EXACTLY, so each rung has
# a known answer the fit can be scored against.
ALPHA_CAL = 0.4                                   # exact p = 1.4

RUNGS = [
    # (name,             X_lo,     X_hi,   n_grid, what it probes)
    ("clean_control",   -41000.0, 41000.0,   801,
     "CLEAN CONTROL: wide enough that NO theta sample escapes. Must report 0 outside, "
     "domain_valid=True, 0 warnings. This is the rung that lets the suite come out the "
     "other way (lesson 90) and the over-rejection risk leg 94's suite exists to catch."),
    ("wide_asymmetric", -41000.0,   745.2,   801,
     "THE SHARPEST ANTI-TAUTOLOGY CASE: max|X| = 41000, so the PRE-REPAIR symmetric "
     "window reports 0 -- perfectly clean -- while the true data interval is escaped."),
    ("symmetric_control", -745.2,   745.2,   801,
     "SYMMETRY CONTROL: leg 55's live shape. Both windows coincide exactly, so the "
     "repaired and pre-repair counts MUST agree here (leg 84 banked 14 at X_max=745.2)."),
    ("right_truncated",   -745.2,     3.0,   601,
     "full left arm, right arm cut to X=3: outside is entirely on the RIGHT."),
    ("two_sided_offset",    -2.0,    50.0,   501,
     "both endpoints finite and unequal in magnitude AND sign-spanning."),
    ("excludes_zero",       0.25,   745.2,   601,
     "data interval does NOT contain 0: the pre-repair |X| window is maximally wrong."),
    ("tiny_window",        -0.05,    0.05,   401,
     "both endpoints tiny: almost the whole circle is extrapolated."),
    ("near_symmetric",    -745.2,   744.0,   801,
     "asymmetric by 1.2 in 745: a SMALL count, which is the precision-sensitive case."),
]


def rho_uniform_grid(X_lo, X_hi, n, c=C_SINH):
    """X = c sinh(rho) on a UNIFORM rho grid -- the sampling `compactify` assumes."""
    rho = np.linspace(math.asinh(float(X_lo) / c), math.asinh(float(X_hi) / c), int(n))
    return c * np.sinh(rho)


def part_a():
    rows = []
    for name, X_lo, X_hi, n_grid, probes in RUNGS:
        X = rho_uniform_grid(X_lo, X_hi, n_grid)
        f = calibration_family(X, ALPHA_CAL)

        cf_below, cf_above, cf_total = closed_form_outside(X.min(), X.max(), M_PROBE)
        bf_total = brute_force_outside(X.min(), X.max(), M_PROBE)
        pre_total = prerepair_closed_form_outside(np.abs(X).max(), M_PROBE)[2]

        # `far_field='power'` normalises each side by its OWN endpoint magnitude
        # (`scale = where(above, X_hi, -X_lo)`).  On a data interval lying strictly to one
        # side of zero that scale is NEGATIVE or zero, and the continuation goes non-finite.
        # Leg 220's own code comment claims that outcome is "VISIBLE".  This runner does
        # not dodge it -- it records whether it is visible (a raise) or silent (a number),
        # then falls back to the `clamp` ablation so the guard fields can still be read.
        power_raised = None
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            try:
                sp = spectrum(X, f, M=M_PROBE, far_field="power",
                              tail_exponent=-ALPHA_CAL)
                far_used = "power"
                power_raised = False
            except ValueError as exc:
                power_raised = True
                far_used = "clamp"
                sp = spectrum(X, f, M=M_PROBE, far_field="clamp")
                power_error = str(exc)
            fit = fit_exponent(sp["k"], sp["hk"], 32, 256,
                               n_outside_grid=sp["n_outside_grid"])
            ps = weighted_partial_sums(sp["k"], sp["hk"], 0.0, [16, 256, 4096],
                                       n_outside_grid=sp["n_outside_grid"])
            tl = analytic_tail(fit["p"], fit["C"], 4096, 0.0,
                               n_outside_grid=sp["n_outside_grid"])
            nv = norm_verdict(fit["p"], 0.0, alpha=ALPHA_CAL,
                              n_outside_grid=sp["n_outside_grid"])
        n_warn = sum(1 for w in caught
                     if issubclass(w.category, TargetNormDomainWarning))

        module_n = int(sp["n_outside_grid"])
        rows.append({
            "rung": name,
            "probes": probes,
            "X_lo_requested": float(X_lo), "X_hi_requested": float(X_hi),
            "X_lo_data_reported": float(sp["X_lo_data"]),
            "X_hi_data_reported": float(sp["X_hi_data"]),
            "X_max_data_reported": float(sp["X_max_data"]),
            "n_grid_points": int(n_grid),
            "M": M_PROBE,
            "is_symmetric_grid": bool(float(X.min()) == -float(X.max())),
            "asymmetry_X_lo_plus_X_hi": float(X.min() + X.max()),

            # --- the three independent counts ---
            "closed_form_n_below": cf_below,
            "closed_form_n_above": cf_above,
            "closed_form_n_outside_TRUTH": cf_total,
            "brute_force_n_outside": bf_total,
            "module_n_outside_grid": module_n,
            "module_minus_closed_form": module_n - cf_total,
            "closed_form_minus_brute_force": cf_total - bf_total,
            "MATCHES_TRUTH_EXACTLY": bool(module_n == cf_total == bf_total),

            # --- the anti-tautology control (lesson 90) ---
            "prerepair_symmetric_window_n_outside": pre_total,
            "prerepair_minus_true": pre_total - cf_total,
            "windows_coincide": bool(pre_total == cf_total),

            # --- the verdict fields, on every surface that carries them ---
            "domain_valid_spectrum": sp["domain_valid"],
            "domain_valid_fit_exponent": fit["domain_valid"],
            "domain_valid_weighted_partial_sums": ps[-1]["domain_valid"],
            "domain_valid_analytic_tail": tl["domain_valid"],
            "domain_valid_norm_verdict": nv["domain_valid"],
            "n_domain_warnings_raised": int(n_warn),
            "frac_outside_grid": float(sp["frac_outside_grid"]),

            # --- the far-field branch on a one-sided interval ---
            "far_field_used": far_used,
            "far_field_power_raised_visibly": power_raised,
            "far_field_power_error": (power_error if power_raised else None),

            # --- the damage, so the flag is attached to a magnitude ---
            "p_fitted": float(fit["p"]),
            "p_exact": 1.0 + ALPHA_CAL,
            "p_abs_error": abs(float(fit["p"]) - (1.0 + ALPHA_CAL)),
        })
    return rows


# ==========================================================================
# PART B -- leg 55's banked margins, re-solved from scratch
# ==========================================================================
def part_b():
    banked = json.load(open(NB_JSON))
    nb5_banked = banked["NB5_norms"]
    banked_p = nb5_banked["p"]
    banked_classes = {c["s"]: c for c in nb5_banked["classes"]}

    from experiments.p2_route_nb_v1_targetnorm import nb5_norms   # leg 55's OWN path

    t0 = time.time()
    fresh = nb5_norms(n=nb5_banked["n"], rho_max=nb5_banked["rho_max"])
    wall = time.time() - t0

    rows = []
    for cl in fresh["classes"]:
        s = cl["s"]
        b = banked_classes[s]
        m_fresh = cl["analytic_tail"]["margin"]
        m_bank = b["analytic_tail"]["margin"]
        v_fresh = cl["verdict"]["margin_in_exponent_units"]
        v_bank = b["verdict"]["margin_in_exponent_units"]
        identity = fresh["p"] - s - 1.0            # plain-Python independent identity
        rows.append({
            "s": s,
            "margin_banked_leg55": m_bank,
            "margin_rerun_leg230": m_fresh,
            "difference": m_fresh - m_bank,
            "bit_identical": bool(m_fresh == m_bank),
            "verdict_margin_banked": v_bank,
            "verdict_margin_rerun": v_fresh,
            "verdict_bit_identical": bool(v_fresh == v_bank),
            "independent_identity_p_minus_s_minus_1": identity,
            "identity_minus_rerun_margin": identity - m_fresh,
            "identity_bit_identical": bool(identity == m_fresh),
            "finite_banked": b["analytic_tail"]["finite"],
            "finite_rerun": cl["analytic_tail"]["finite"],
        })

    return {
        "solve_config": {"n": nb5_banked["n"], "rho_max": nb5_banked["rho_max"],
                         "wall_s": wall},
        "p_banked_leg55": banked_p,
        "p_rerun_leg230": fresh["p"],
        "p_difference": fresh["p"] - banked_p,
        "p_bit_identical": bool(fresh["p"] == banked_p),
        "alpha_banked": banked["NB5_norms"].get("alpha"),
        "alpha_rerun": fresh["alpha"],
        "alpha_bit_identical": bool(fresh["alpha"] == banked["NB5_norms"].get("alpha")),
        "classes": rows,
        "n_classes_bit_identical": sum(1 for r in rows if r["bit_identical"]),
        "n_classes": len(rows),
        "comparison_operator": "== on raw float64, never allclose",
    }


# ==========================================================================
def main():
    print("Leg 230 / Route-TNRV -- independent post-repair verification\n")

    print("PART A -- flagging against a closed form")
    a = part_a()
    for r in a:
        print(f"  {r['rung']:>18}  window=[{r['X_lo_data_reported']:.4g}, "
              f"{r['X_hi_data_reported']:.4g}]  truth={r['closed_form_n_outside_TRUTH']:>6}"
              f"  module={r['module_n_outside_grid']:>6}"
              f"  pre-repair={r['prerepair_symmetric_window_n_outside']:>6}"
              f"  domain_valid={str(r['domain_valid_spectrum']):>5}"
              f"  warn={r['n_domain_warnings_raised']}"
              f"  p={r['p_fitted']:+.4f}")

    by_name = {r["rung"]: r for r in a}
    asym = [r for r in a if not r["is_symmetric_grid"]]
    sym = [r for r in a if r["is_symmetric_grid"]]
    clean = by_name["clean_control"]
    # HONEST NOTE: a symmetric grid does NOT imply a zero count -- at X_max = 745.2 the
    # true count is 14 (leg 84 banked exactly that), because the staggered theta grid at
    # M = 16384 reaches past |X| = 745.2.  The symmetric rungs' control property is that
    # the two WINDOWS coincide, not that the count vanishes.  Asserting otherwise was an
    # error in this harness's first draft and is recorded rather than quietly corrected.
    a_summary = {
        "n_rungs": len(a),
        "n_asymmetric_rungs": len(asym),
        "n_symmetric_rungs": len(sym),
        "asymmetric_all_flagged": bool(all(r["module_n_outside_grid"] > 0
                                           and r["domain_valid_spectrum"] is False
                                           for r in asym)),
        "all_counts_match_closed_form_truth": bool(all(r["MATCHES_TRUTH_EXACTLY"]
                                                       for r in a)),
        "n_rungs_matching_truth": sum(1 for r in a if r["MATCHES_TRUTH_EXACTLY"]),
        # the control that can come out the other way
        "clean_control_zero_and_valid": bool(clean["module_n_outside_grid"] == 0
                                             and clean["domain_valid_spectrum"] is True
                                             and clean["n_domain_warnings_raised"] == 0),
        "clean_control_p_abs_error": clean["p_abs_error"],
        # symmetric grids: the two windows must coincide, so the counts must too
        "symmetric_rungs_windows_coincide": bool(all(r["windows_coincide"] for r in sym)),
        "control_can_come_out_both_ways": bool(
            any(r["windows_coincide"] for r in a) and
            any(not r["windows_coincide"] for r in a)),
        "max_prerepair_undercount": max(r["closed_form_n_outside_TRUTH"]
                                        - r["prerepair_symmetric_window_n_outside"]
                                        for r in a),
        "worst_prerepair_false_clean_rung": max(
            a, key=lambda r: (r["prerepair_symmetric_window_n_outside"] == 0,
                              r["closed_form_n_outside_TRUTH"]))["rung"],
        "all_downstream_surfaces_agree": bool(all(
            r["domain_valid_spectrum"] == r["domain_valid_fit_exponent"]
            == r["domain_valid_weighted_partial_sums"]
            == r["domain_valid_analytic_tail"] == r["domain_valid_norm_verdict"]
            for r in a)),
    }
    print("  summary:", json.dumps(a_summary))

    print("\nPART B -- leg 55's banked margins, re-solved from scratch")
    b = part_b()
    print(f"  p  banked={b['p_banked_leg55']!r}  rerun={b['p_rerun_leg230']!r}  "
          f"diff={b['p_difference']!r}  identical={b['p_bit_identical']}")
    for r in b["classes"]:
        print(f"  s={r['s']:<5} banked={r['margin_banked_leg55']!r:>24} "
              f"rerun={r['margin_rerun_leg230']!r:>24} diff={r['difference']!r} "
              f"identical={r['bit_identical']}")

    gate_yes = bool(a_summary["asymmetric_all_flagged"]
                    and a_summary["all_counts_match_closed_form_truth"]
                    and a_summary["clean_control_zero_and_valid"]
                    and a_summary["symmetric_rungs_windows_coincide"]
                    and a_summary["control_can_come_out_both_ways"]
                    and a_summary["all_downstream_surfaces_agree"]
                    and b["p_bit_identical"]
                    and b["n_classes_bit_identical"] == b["n_classes"])

    out = {
        "leg": 230, "route": "TNRV", "version": "v1", "role": "VERIFIER",
        "verifies": {"leg": 220, "route": "TNR", "commit": "a516ef8",
                     "module": "solver/target_norm.py (READ-ONLY to this leg)"},
        "gate": ("Does an independent re-run confirm the asymmetric-grid extrapolation "
                 "case is now correctly flagged (n_outside_grid>0/domain_valid=False), "
                 "with leg 55's own banked margins bit-identical?"),
        "gate_answer": "YES" if gate_yes else "NO",
        "independence": (
            "Part A's truth is a CLOSED FORM (two ceil/floor evaluations, no array), "
            "cross-checked by a separate O(M) brute force; the rungs are this leg's own "
            "and differ in kind from leg 220's five. Part B compares with == on raw "
            "float64 against constants this runner reads out of leg 55's banked JSON, "
            "plus the plain-Python identity margin = p - s - 1. "
            "experiments/p2_route_tnr_v1_repair.py is NEVER imported or executed."),
        "part_a_flagging": {"M": M_PROBE, "calibration_alpha": ALPHA_CAL,
                            "p_exact": 1.0 + ALPHA_CAL,
                            "summary": a_summary, "rungs": a},
        "part_b_banked_margins": b,
        "ceiling": (
            "An audit of an INPUT GUARD's repair. Certifies nothing, moves no bound, "
            "re-measures no physics, touches no link of the L1->L4 chain, extends no "
            "domain. It does NOT make an extrapolated answer right -- leg 220 said it "
            "cannot and that limitation is inherited verbatim. It does NOT address the "
            "six of leg 204's seven mechanisms leg 220 left open, which are a stated "
            "limitation of a landed leg, not a discrepancy."),
    }
    with open(OUT_JSON, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=False)
    print(f"\nGATE: {out['gate_answer']}")
    print(f"wrote {OUT_JSON}")
    return 0 if gate_yes else 1


if __name__ == "__main__":
    sys.exit(main())
