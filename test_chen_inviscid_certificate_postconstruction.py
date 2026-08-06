"""Leg 193 (Route-M2CV) — the VERIFICATION of leg 187's landed NO, as tests.

Self-running, no pytest — the repo convention (`scripts/merge_gate.sh` line 18):

    .venv/bin/python test_chen_inviscid_certificate_postconstruction.py

Two kinds of test live here, and they are kept apart on purpose:

  * **Re-derivation tests** (§1–§3) recompute the load-bearing claims from scratch, in
    exact bivariate rational arithmetic with the orbit parameter left SYMBOLIC, and check
    leg 187's `solver/chen_inviscid_certificate.py` against them.  They do not read leg
    187's JSON, and they would fail if the landed module were wrong.
  * **Banked-record tests** (§4) difference the curated JSON this leg wrote against the
    curated JSON leg 187 landed, quantity by quantity.

Every clause has a control that CAN come out the other way (lesson 90): perturbed
amplitude, wrong `a`, wrong `c_l`, wrong `c_omega`, a localised bump instead of the orbit
tangent, an `X^-2` profile instead of the `X^-3` one, and — for the one claim that turned
out to be imprecise — a second resolution ladder that CAN disagree with the first, and does.
"""

import json
import os
import sys
from fractions import Fraction as F

import numpy as np

import solver.chen_inviscid_certificate as leg187
from experiments.p2_route_m2cv_v1_postconstruction import (
    RF2, _bordered, _orbit, _tangent, _wnorm, _Z2, decay_and_symbol, exact_block,
    exact_orbit_symbolic, kernel_and_shadow_fresh, operator_consistency,
)
from solver.dissipative_profile import DissipativeProfile, chen_profile

ROOT = os.path.dirname(os.path.abspath(__file__))
OURS = os.path.join(ROOT, "writeup", "data", "p2_route_m2cv_v1_postconstruction.json")
THEIRS = os.path.join(ROOT, "writeup", "data", "p2_route_m2ci_v1_construction.json")

C_L, C_OMEGA, G_CHEN, S = 1.0 / 3.0, -1.0, 3.0 / 8.0, 2.0

FAILURES = []


def check(name, cond, detail=""):
    if cond:
        print("  ok   %s" % name)
    else:
        print("  FAIL %s  %s" % (name, detail))
        FAILURES.append(name)


def _load(path):
    with open(path) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# 1. the exact identity, re-derived symbolically in the orbit parameter
# ---------------------------------------------------------------------------

def test_exact_identity_holds_for_every_orbit_parameter():
    print("test_exact_identity_holds_for_every_orbit_parameter")
    res, df_phi, phi = exact_orbit_symbolic()
    check("orbit residual numerator is the ZERO POLYNOMIAL in Q[X, b], i.e. for every g > 0",
          res.is_zero(), str(res.as_terms()))
    check("DF[orbit tangent] is EXACTLY zero for every g > 0 (leg 187 measured 3.27e-06)",
          df_phi.is_zero(), str(df_phi.as_terms()))
    check("the tangent itself is nonzero, so the kernel argument is not vacuous",
          not phi.is_zero(), str(phi.as_terms()))
    for extra in (F(1, 100), F(-1, 100), F(1), F(-1, 1000)):
        r, d, _ = exact_orbit_symbolic(kappa_extra=extra)
        check("control: amplitude perturbed by %s is NOT a solution" % extra,
              not r.is_zero() and not d.is_zero())
    for a, c_l, c_om, why in ((F(0), F(1, 3), F(-1), "a = 0"), (F(1), F(1, 3), F(-1), "a = 1"),
                              (F(1, 2), F(1, 2), F(-1), "c_l = 1/2"),
                              (F(1, 2), F(1, 3), F(-2), "c_omega = -2")):
        r, _, _ = exact_orbit_symbolic(a=a, c_l=c_l, c_omega=c_om)
        check("control: %s is NOT a solution (identity is specific to Chen's constants)" % why,
              not r.is_zero())


def test_leg187_exact_claims_reproduce():
    print("test_leg187_exact_claims_reproduce")
    eb = exact_block()
    check("leg 187's `orbit_generator` formula equals d(Psi_g)/dg exactly",
          eb["leg187_orbit_generator_formula_matches_d_dg"] is True)
    rows = leg187.exact_orbit_check()
    check("leg 187's own 5 pinned-g rows still all come out zero", len(rows) == 5
          and all(r["exact_zero"] for r in rows))
    check("and all 5 of its perturbed-amplitude controls still come out nonzero",
          all(r["control_is_nonzero"] for r in rows))
    psi = RF2({(1, 3): F(-16, 3)}, 2)
    X = np.linspace(-30.0, 30.0, 1001)
    worst = max(float(np.max(np.abs(psi.evaluate(X, np.sqrt(g)) - leg187.orbit_profile(X, g))))
                for g in (0.1, 3.0 / 8.0, 1.0, 4.0))
    check("the symbolic family and leg 187's float `orbit_profile` are the same function",
          worst < 1e-13, "worst %.3e" % worst)
    Om, _, _ = chen_profile(np.linspace(-40.0, 40.0, 2001))
    d = float(np.max(np.abs(leg187.orbit_profile(np.linspace(-40.0, 40.0, 2001), G_CHEN) - Om)))
    check("the orbit passes exactly through Chen eq (2.2) at g = 3/8", d < 1e-14, "%.3e" % d)


# ---------------------------------------------------------------------------
# 2. does the exact algebra describe the repository's own operator?
# ---------------------------------------------------------------------------

def test_closed_forms_are_the_repositorys_own_H_and_U():
    print("test_closed_forms_are_the_repositorys_own_H_and_U")
    lad = operator_consistency()["ladder"]
    check("H closed form matches dp.H, and the error SHRINKS with resolution",
          lad[0]["rel_err_H_closed_form"] > lad[-1]["rel_err_H_closed_form"]
          and lad[-1]["rel_err_H_closed_form"] < 1e-7,
          "%.3e -> %.3e" % (lad[0]["rel_err_H_closed_form"], lad[-1]["rel_err_H_closed_form"]))
    check("U closed form matches dp.VH to discretisation error",
          lad[-1]["rel_err_U_closed_form"] < 1e-5, "%.3e" % lad[-1]["rel_err_U_closed_form"])
    check("the grid residual on the centre also shrinks (it is discretisation, not defect)",
          lad[0]["grid_residual_sup"] > lad[-1]["grid_residual_sup"],
          "%.3e -> %.3e" % (lad[0]["grid_residual_sup"], lad[-1]["grid_residual_sup"]))


# ---------------------------------------------------------------------------
# 3. the float clauses, recomputed here rather than called from leg 187
# ---------------------------------------------------------------------------

def test_kernel_separates_from_its_control():
    print("test_kernel_separates_from_its_control")
    dp = DissipativeProfile(a=0.5, n=401, rho_max=8.0)
    X = dp.X
    J, _ = _bordered(dp, G_CHEN, S)
    rel_k = _wnorm(X, J @ _tangent(X, G_CHEN), S) / _wnorm(X, _tangent(X, G_CHEN), S)
    bump = X * np.exp(-(X ** 2))
    rel_c = _wnorm(X, J @ bump, S) / _wnorm(X, bump, S)
    rel_p = _wnorm(X, J @ _orbit(X, G_CHEN), S) / _wnorm(X, _orbit(X, G_CHEN), S)
    check("the orbit tangent's relative DF-defect is at the discretisation floor",
          rel_k < 1e-3, "%.3e" % rel_k)
    check("control: a localised bump is NOT in the kernel", rel_c > 0.1, "%.3e" % rel_c)
    check("control: the profile itself is NOT in the kernel", rel_p > 0.1, "%.3e" % rel_p)
    check("kernel and control separate by >1e3", rel_c / rel_k > 1e3, "%.3e" % (rel_c / rel_k))


def test_pinv_shadow_trap_fires_in_both_regimes():
    print("test_pinv_shadow_trap_fires_in_both_regimes")
    k = kernel_and_shadow_fresh(n=401)
    check("numpy's default cutoff sits BELOW sigma_min/sigma_max, so pinv inverts the kernel",
          k["numpy_default_rcond_estimate"] < k["sigma_ratio"],
          "%.3e < %.3e" % (k["numpy_default_rcond_estimate"], k["sigma_ratio"]))
    check("so the default-rcond shadow is spuriously tiny",
          k["float_shadow_pinv_rcond_default"] < 1e-6,
          "%.3e" % k["float_shadow_pinv_rcond_default"])
    check("truncated honestly, the shadow returns to the exact bound 1 FROM BELOW",
          abs(k["float_shadow_pinv_rcond_1e-6"] - 1.0) < 1e-4
          and k["float_shadow_pinv_rcond_1e-6"] < 1.0,
          "%.7f" % k["float_shadow_pinv_rcond_1e-6"])
    check("control: rcond = 1e-8 does NOT truncate at n = 401 (1e-8 < sigma_ratio 1.35e-08), "
          "so it reproduces the un-truncated regime",
          k["float_shadow_pinv_rcond_1e-8"] < 1e-6,
          "%.3e" % k["float_shadow_pinv_rcond_1e-8"])


def test_Z2_growth_is_carried_by_the_derivative_operator():
    print("test_Z2_growth_is_carried_by_the_derivative_operator")
    q1 = _Z2(DissipativeProfile(a=0.5, n=201))
    q2 = _Z2(DissipativeProfile(a=0.5, n=401))
    check("Z_2 grows faster than n^1 between n = 201 and n = 401",
          q2["Z2"] > 4.0 * q1["Z2"], "%.3e -> %.3e" % (q1["Z2"], q2["Z2"]))
    check("||D|| grows with n (it is the derivative the sup norm does not control)",
          q2["norm_D_s"] / q1["norm_D_s"] > 1.5,
          "%.4g -> %.4g" % (q1["norm_D_s"], q2["norm_D_s"]))
    check("control: ||H|| is FLAT in n", abs(q2["norm_H_s"] / q1["norm_H_s"] - 1.0) < 0.05,
          "%.4g -> %.4g" % (q1["norm_H_s"], q2["norm_H_s"]))
    check("control: ||VH|| is FLAT in n", abs(q2["norm_VH_s"] / q1["norm_VH_s"] - 1.0) < 0.05,
          "%.4g -> %.4g" % (q1["norm_VH_s"], q2["norm_VH_s"]))


def test_decay_exponent_and_symbol():
    print("test_decay_exponent_and_symbol")
    decay, symbol = decay_and_symbol(n=401)
    check("the profile's measured decay exponent is 3", abs(decay["exponent"] - 3.0) < 1e-3,
          "%.6f" % decay["exponent"])
    check("the orbit tangent decays at the SAME rate (dilation preserves the exponent)",
          abs(decay["tangent_exponent"] - 3.0) < 1e-3, "%.6f" % decay["tangent_exponent"])
    check("control: an X^-2 profile measures 2, not 3",
          abs(decay["control_slope_on_Xminus2_profile"] + 2.0) < 1e-3,
          "%.6f" % decay["control_slope_on_Xminus2_profile"])
    check("the far-field symbol vanishes at exactly s = 3",
          abs(symbol["symbol_zero_at_s"] - 3.0) < 1e-12)


# ---------------------------------------------------------------------------
# 4. the two banked records, differenced
# ---------------------------------------------------------------------------

def test_banked_records_agree():
    print("test_banked_records_agree")
    if not os.path.exists(OURS):
        check("leg 193's curated JSON exists", False,
              "run experiments/p2_route_m2cv_v1_postconstruction.py first")
        return
    ours, theirs = _load(OURS), _load(THEIRS)
    check("this leg's gate is answered YES against leg 187's landed NO",
          ours["answer"] == "YES" and ours["verifies"]["landed_gate_answer"] == "NO")
    table = ours["reproduction_table"]
    worst = max(r["relative_difference"] for r in table)
    check("all %d quoted quantities reproduce (worst relative difference %.2e)"
          % (len(table), worst), len(table) >= 20 and worst < 1e-9,
          str([r["quantity"] for r in table if r["relative_difference"] >= 1e-9]))
    check("no verdict-changing discrepancy was found",
          ours["discrepancies_found"]["verdict_changing"] == [])
    check("the one precision caveat and the one understatement are on the record",
          len(ours["discrepancies_found"]["precision"]) == 1
          and len(ours["discrepancies_found"]["understatements"]) == 1)
    check("leg 187's own module, re-run unchanged, still answers NO",
          ours["leg187_own_functions_rerun"]["gate_answer_from_module"] == "NO")


def test_Z2_exponent_is_ladder_dependent_but_the_divergence_is_not():
    print("test_Z2_exponent_is_ladder_dependent_but_the_divergence_is_not")
    if not os.path.exists(OURS):
        check("leg 193's curated JSON exists", False, "run the experiment first")
        return
    ours, theirs = _load(OURS), _load(THEIRS)
    hm = ours["headline_magnitudes"]
    check("our Z_2 slope on leg 187's own ladder matches its banked 2.3595",
          abs(hm["Z2_slope_independent"]
              - theirs["headline_magnitudes"]["Z2_slope_in_log_n"]) < 1e-9,
          "%.6f" % hm["Z2_slope_independent"])
    check("BUT the local pairwise slopes CURVE upward, so 2.36 is an average, not an exponent",
          hm["Z2_local_slope_max"] > hm["Z2_local_slope_min"] + 0.2,
          "%.3f .. %.3f" % (hm["Z2_local_slope_min"], hm["Z2_local_slope_max"]))
    check("and a different ladder gives a materially different global slope",
          abs(hm["Z2_slope_on_a_different_ladder"] - hm["Z2_slope_independent"]) > 0.05,
          "%.4f vs %.4f" % (hm["Z2_slope_on_a_different_ladder"], hm["Z2_slope_independent"]))
    check("the H7 failure survives it: every local slope is far above 1",
          hm["Z2_local_slope_min"] > 1.5 and hm["Z2_slope_on_a_different_ladder"] > 1.5,
          "min local %.3f" % hm["Z2_local_slope_min"])
    a = ours["H7_divergence_fresh"]["slopes_in_log_n"]["sigma_ratio"]
    b = hm["sigma_ratio_slope_on_a_different_ladder"]
    check("control that could have been ladder-dependent and is not: sigma_ratio's slope",
          a < -6.0 and b < -6.0 and abs(a - b) / abs(a) < 0.05, "%.4f vs %.4f" % (a, b))


def main():
    for t in (test_exact_identity_holds_for_every_orbit_parameter,
              test_leg187_exact_claims_reproduce,
              test_closed_forms_are_the_repositorys_own_H_and_U,
              test_kernel_separates_from_its_control,
              test_pinv_shadow_trap_fires_in_both_regimes,
              test_Z2_growth_is_carried_by_the_derivative_operator,
              test_decay_exponent_and_symbol,
              test_banked_records_agree,
              test_Z2_exponent_is_ladder_dependent_but_the_divergence_is_not):
        t()
    print()
    if FAILURES:
        print("FAILED (%d): %s" % (len(FAILURES), FAILURES))
        return 1
    print("all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
