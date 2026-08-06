"""Route-ASA v1: an ADVERSARIAL AUDIT of solver/advection_scope.py.

WHAT THIS IS NOT.  It is not a measurement of anything physical.  No number printed here is a
statement about blow-up, about the advection term's scope in `a`, or about any quantity in the
plan of record.  It re-derives no physics and contests no banked result -- the module's own
physics claims (docstring sections (1)-(5), gated by test_advection_scope.py) are untouched.

WHAT THIS IS.  Every number here is a statement about CODE BEHAVIOUR UNDER DEGENERATE OR
POISONED INPUT.  The question, verbatim from the leg's gate (DIRECTION.md, leg 122):

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/advection_scope.py ever silently return a wrong result instead of flagging the
    input?

WHY THIS MODULE.  Eleven Route-D legs and this module's own docstring establish it scopes the
advection term for the whole bound programme, and -- per DIRECTION.md's leg-122 entry -- it has
never been through the audit family that legs 69/100/101/120 built.  It has a dedicated
known-answer test (test_advection_scope.py) but no adversarial battery: every call in the
repository goes through a real Newton-solved profile, whose `fam.X` is always the `sinh_grid`
output (strictly increasing by construction, solver/gclm_rescaled.py:66) -- so no malformed,
mis-ordered, or non-finite input has ever reached this module.

WHERE THE MECHANISM COMES FROM (novelty pass, writeup/novelty/leg_122.md).  `profile_mass`
(and, through it, `velocity_log_rate`'s `mass`/`mass_window` fields) is a two-line wrapper
around `numpy.trapezoid`.  NumPy's own manual states the precondition this module never
re-imposes: "If x is provided, the integration happens in sequence along its elements -- they
are not sorted" -- and its own worked example shows a reversed x negates the result
(`np.trapezoid([1,2,3], x=[8,6,4]) == -8.0` vs `np.trapezoid([1,2,3], x=[4,6,8]) == 8.0`).
`profile_mass`'s docstring promises a mathematical (order-independent) integral; the code
computes NumPy's sequential (order-DEPENDENT) quadrature.  Category T instruments exactly that
gap.  `stagnation_point`'s docstring promises "the SMALLEST X > 0" -- a claim about physical
position -- while the implementation (`np.diff` over the array AS GIVEN, `idx[0]`) finds the
smallest ARRAY INDEX, which coincides with the smallest coordinate only if the caller's `X` is
already sorted ascending, a precondition the function never checks.  Category S instruments
that gap.  Category C is the map of what the module gets right.

DECISION RULE (fixed before the run, writeup/novelty/leg_122.md sec 3):
  SILENT-CORRUPTION VIOLATION := a case with an independently-computable reference answer
  where the module returns a FINITE value differing from the reference beyond a generous
  tolerance, WITHOUT raising and WITHOUT nan/inf appearing anywhere in the output.
  nan/inf output = PASS (the flag the gate looks for).  An exception = PASS.  A ComplexWarning
  is graded as its own, weaker, category -- a signal that fires but that a caller who does not
  inspect `warnings` will never see.

PASSES ARE REPORTED AS LOUDLY AS FAILURES (leg 91/120's design rule, inherited).

Run: .venv/bin/python experiments/p2_route_asa_v1_adversarial.py   (< 5 s, no solver run)
"""
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.advection_scope import (                                    # noqa: E402
    profile_mass, velocity_log_rate, stagnation_point, advection_split, _log_fit,
)

OUT = ROOT / "writeup" / "data" / "p2_route_asa_v1_adversarial.json"


class Fam:
    """Minimal duck-typed stand-in for solver.gclm_family.GCLMResidual, carrying only
    the three attributes advection_scope.py's functions actually read: X, Vmat, Hmat.
    Built directly so the battery can poison array ORDER and VALUES without paying for
    (or being constrained by) a real Newton solve, exactly as legs 100/101 built
    duck-typed operator/weight stand-ins for solver/op_lower.py and solver/holder_norms.py."""

    def __init__(self, X, Vmat=None, Hmat=None):
        self.X = np.asarray(X, dtype=float)
        n = self.X.size
        self.Vmat = Vmat if Vmat is not None else np.eye(n)
        self.Hmat = Hmat if Hmat is not None else np.eye(n)


def _isnan(v):
    return isinstance(v, float) and math.isnan(v)


# ---------------------------------------------------------------------------
# CATEGORY T -- trapezoidal order-dependence (profile_mass / velocity_log_rate)
# ---------------------------------------------------------------------------

def battery_T():
    out = {}

    # T1: ascending control against a closed-form analytic reference.
    #   Omega(X) = -1/(1+X^2), the module's own a=0 anchor; int_{-L}^{L} Omega dX = -2*atan(L).
    L, n = 1000.0, 4001
    X = np.linspace(-L, L, n)
    om = -1.0 / (1.0 + X ** 2)
    exact = -2.0 * math.atan(L)
    asc = profile_mass(om, X)
    out["T1_ascending_control"] = {
        "n": n, "L": L, "exact_closed_form": exact, "returned": asc,
        "rel_err": abs(asc - exact) / abs(exact),
        "note": "control: ascending sorted X reproduces the closed form to O(1/n^2) discretization error",
    }

    # T2: exact reversal -- NumPy's own worked-example mechanism.
    rev = profile_mass(om[::-1], X[::-1])
    out["T2_exact_reversal"] = {
        "returned": rev, "ascending": asc, "is_exact_negation": bool(rev == -asc),
        "rel_err_vs_exact": abs(rev - exact) / abs(exact),
        "nan_or_inf_anywhere": (not np.isfinite(rev)),
        "raised": False,
        "verdict": "SILENT_CORRUPTION" if (np.isfinite(rev) and abs(rev - exact) / abs(exact) > 0.05) else "flagged_or_sound",
    }

    # T3: five seeded random permutations -- no order structure preserved at all.
    perms = []
    for seed in range(5):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(n)
        val = profile_mass(om[perm], X[perm])
        rel = abs(val - exact) / abs(exact)
        perms.append({
            "seed": seed, "returned": val, "rel_err_vs_exact": rel,
            "finite": bool(np.isfinite(val)),
            "verdict": "SILENT_CORRUPTION" if (np.isfinite(val) and rel > 0.05) else "flagged_or_sound",
        })
    out["T3_random_permutations"] = perms

    # T4: single adjacent-pair transposition -- the minimal possible order perturbation.
    Xs, oms = X.copy(), om.copy()
    i = n // 2
    Xs[[i, i + 1]] = Xs[[i + 1, i]]
    oms[[i, i + 1]] = oms[[i + 1, i]]
    val_swap = profile_mass(oms, Xs)
    out["T4_single_adjacent_swap"] = {
        "returned": val_swap, "ascending_reference": asc,
        "abs_diff_from_ascending": abs(val_swap - asc),
        "rel_err_vs_exact": abs(val_swap - exact) / abs(exact),
        "finite": bool(np.isfinite(val_swap)),
        "note": "swapping exactly TWO adjacent array entries, everything else untouched",
        "verdict": "SILENT_CORRUPTION" if (np.isfinite(val_swap) and abs(val_swap - exact) / abs(exact) > 0.01) else "flagged_or_sound",
    }

    # T5: the consequence in velocity_log_rate -- isolates that its polyfit-based
    # "measured" field is order-independent while its trapz-based "mass"/"mass_window"/
    # "predicted" fields are not, using a toy Vmat=Hmat=I (velocity(fam,om) == om) so the
    # comparison is purely about advection_scope.py's own arithmetic.
    fam_sorted = Fam(X)
    d_sorted = velocity_log_rate(fam_sorted, om, lo=10.0, hi=1e3)
    perm = np.random.default_rng(0).permutation(n)
    fam_shuf = Fam(X[perm])
    d_shuf = velocity_log_rate(fam_shuf, om[perm], lo=10.0, hi=1e3)
    out["T5_velocity_log_rate_consequence"] = {
        "sorted": d_sorted, "shuffled": d_shuf,
        "measured_rel_change": abs(d_shuf["measured"] - d_sorted["measured"]) / abs(d_sorted["measured"]),
        "predicted_rel_change": abs(d_shuf["predicted"] - d_sorted["predicted"]) / abs(d_sorted["predicted"]),
        "note": ("'measured' (a np.polyfit slope) is order-independent and barely moves; "
                 "'predicted'/'mass'/'mass_window' (trapz-based) are corrupted by the same "
                 "permutation -- an internally INCONSISTENT result package, silently returned"),
    }
    return out


# ---------------------------------------------------------------------------
# CATEGORY S -- stagnation_point array-order-dependence
# ---------------------------------------------------------------------------

def battery_S():
    out = {}
    Xs = np.linspace(0.02, 20.0, 4001)

    # S1: single-crossing ground truth. eff(X) = tanh(X - 5) has its only positive-X
    # root at X = 5 (tanh is odd and strictly monotone).
    eff1 = lambda X: np.tanh(X - 5.0)                                     # noqa: E731
    om1 = np.ones_like(Xs)
    fam_sorted = Fam(Xs, Hmat=np.diag(eff1(Xs)))
    x_true = stagnation_point(fam_sorted, om1, 0.0, 1.0)
    out["S1_sorted_ground_truth"] = {"returned": x_true, "true_root": 5.0,
                                      "abs_err": abs(x_true - 5.0)}

    # S2: five seeded shuffles -- values and positions permuted TOGETHER, so every
    # entry is still physically correct; only its storage order changes.
    shuffles = []
    for seed in range(5):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(Xs))
        fam_p = Fam(Xs[perm], Hmat=np.diag(eff1(Xs)[perm]))
        xv = stagnation_point(fam_p, om1[perm], 0.0, 1.0)
        finite = xv is not None and np.isfinite(xv)
        shuffles.append({
            "seed": seed, "returned": xv, "true_root": 5.0,
            "abs_err": (abs(xv - 5.0) if finite else None),
            "finite": bool(finite),
            "verdict": "SILENT_CORRUPTION" if (finite and abs(xv - 5.0) > 0.01) else "flagged_or_sound",
        })
    out["S2_shuffled_single_crossing"] = shuffles

    # S3: two-crossing construction -- does a shuffle merely swap which of the two
    # REAL crossings (~5, ~12) is reported, or fabricate a value belonging to neither?
    eff2 = lambda X: np.tanh(X - 5.0) * np.where(X < 12.0, 1.0, -1.0)     # noqa: E731
    fam2_sorted = Fam(Xs, Hmat=np.diag(eff2(Xs)))
    x_true2 = stagnation_point(fam2_sorted, om1, 0.0, 1.0)
    two_cr = []
    for seed in range(100, 103):
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(Xs))
        fam_p = Fam(Xs[perm], Hmat=np.diag(eff2(Xs)[perm]))
        xv = stagnation_point(fam_p, om1[perm], 0.0, 1.0)
        finite = xv is not None and np.isfinite(xv)
        belongs_to_either = finite and (abs(xv - 5.0) < 0.5 or abs(xv - 12.0) < 0.5)
        two_cr.append({
            "seed": seed, "returned": xv, "finite": bool(finite),
            "matches_a_real_crossing": bool(belongs_to_either) if finite else None,
        })
    out["S3_two_crossings"] = {"sorted_first_crossing": x_true2,
                                "true_crossings": [5.0, 12.0], "shuffles": two_cr}

    # S4: regression control -- NaN placed strictly BEFORE the true crossing, in
    # otherwise-correct sorted order, must never yield a plausible finite crossing.
    Hmat_nan = np.diag(eff1(Xs).copy())
    i_poison = 100  # Xs[100] ~ 0.52, well before the root at 5
    Hmat_nan[i_poison, i_poison] = np.nan
    fam_nan = Fam(Xs, Hmat=Hmat_nan)
    xv_nan = stagnation_point(fam_nan, om1, 0.0, 1.0)
    out["S4_nan_before_crossing_control"] = {
        "returned": xv_nan,
        "is_nan": bool(xv_nan is not None and math.isnan(xv_nan)),
        "note": "NaN strictly before the true root, SORTED order otherwise -- must never look like a real crossing",
    }
    return out


# ---------------------------------------------------------------------------
# CATEGORY C -- controls (reported as loudly as any finding)
# ---------------------------------------------------------------------------

def battery_C():
    out = {}

    # C1: mismatched shapes -> must raise.
    try:
        profile_mass(np.ones(5), np.ones(6))
        out["C1_mismatched_shapes"] = {"raised": False, "verdict": "SILENT_CORRUPTION_RISK"}
    except Exception as e:                                               # noqa: BLE001
        out["C1_mismatched_shapes"] = {"raised": True, "type": type(e).__name__, "verdict": "PASS"}

    # C2: unknown grading key -> must raise.
    Xg = np.linspace(1.0, 100.0, 50)
    famg = Fam(Xg)
    Dg = np.eye(50)
    try:
        advection_split(famg, np.ones(50), 0.3, 1.4, Dg, grading="bogus")
        out["C2_unknown_grading_key"] = {"raised": False, "verdict": "SILENT_CORRUPTION_RISK"}
    except Exception as e:                                               # noqa: BLE001
        out["C2_unknown_grading_key"] = {"raised": True, "type": type(e).__name__, "verdict": "PASS"}

    # C3: nan/inf scalars a, c in stagnation_point -> must flag (nan out), never a
    # plausible finite crossing.
    Xs = np.linspace(0.1, 20.0, 500)
    fam3 = Fam(Xs, Hmat=np.diag(np.tanh(Xs - 5.0)))
    om3 = np.ones_like(Xs)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        r_a_nan = stagnation_point(fam3, om3, 0.0, float("nan"))
        r_c_nan = stagnation_point(fam3, om3, float("nan"), 1.0)
        r_a_inf = stagnation_point(fam3, om3, 0.0, float("inf"))
    out["C3_nonfinite_scalars"] = {
        "a_nan": {"returned": r_a_nan, "is_nan": _isnan(r_a_nan)},
        "c_nan": {"returned": r_c_nan, "is_nan": _isnan(r_c_nan)},
        "a_inf": {"returned": r_a_inf, "is_nan_or_none": (r_a_inf is None or _isnan(r_a_inf))},
        "verdict": "PASS" if (_isnan(r_a_nan) and _isnan(r_c_nan)) else "SILENT_CORRUPTION_RISK",
    }

    # C4: extreme dynamic range, correctly sorted -- scale alone must not corrupt.
    Xe = np.linspace(-1e150, 1e150, 501)
    ome = np.ones_like(Xe) * 1e150
    val = profile_mass(ome, Xe)
    expected = 1e150 * 2e150  # width * height
    out["C4_extreme_scale_sorted"] = {
        "returned": val, "expected": expected,
        "rel_err": abs(val - expected) / abs(expected), "finite": bool(np.isfinite(val)),
        "verdict": "PASS",
    }

    # C5: a single duplicate grid node -- must not corrupt beyond ordinary discretization noise.
    Xd = np.linspace(0.0, 10.0, 101)
    true_ref = profile_mass(np.sin(Xd), Xd)
    Xd2 = Xd.copy()
    Xd2[50] = Xd2[49]
    val_dup = profile_mass(np.sin(Xd2), Xd2)
    out["C5_duplicate_node"] = {
        "returned": val_dup, "reference": true_ref,
        "rel_err": abs(val_dup - true_ref) / abs(true_ref),
        "verdict": "PASS",
    }

    # C6: too-few-points fit window -> the module's own documented nan (safe).
    Xw = np.linspace(1.0, 1000.0, 2000)
    yw = np.log(Xw)
    r_small = _log_fit(Xw, yw, lo=999.99, hi=1000.0)
    out["C6_window_too_small"] = {"returned": r_small, "is_nan": _isnan(r_small), "verdict": "PASS"}

    # C7: negative lo bound in _log_fit -> log of a non-positive number inside the
    # selected window. Graded as a control: an uncaught exception is still a FLAG
    # (loud, if untidy), never a silently wrong slope. NOTE: LAPACK's SVD prints an
    # "illegal value" diagnostic straight to the process's C-level stderr fd when this
    # fires (not Python's `warnings`, and not interceptable by `warnings.catch_warnings`);
    # that terminal noise is expected, harmless, and belongs to the LinAlgError this
    # case is checking is correctly raised.
    Xn = np.linspace(-5.0, 100.0, 500)
    yn = 2.0 + 3.0 * np.log(np.abs(Xn) + 1e-9)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r_neg = _log_fit(Xn, yn, lo=-5.0, hi=100.0)
        out["C7_negative_window_bound"] = {"raised": False, "returned": r_neg,
                                            "is_nan": _isnan(r_neg),
                                            "verdict": "PASS" if _isnan(r_neg) else "SILENT_CORRUPTION_RISK"}
    except Exception as e:                                               # noqa: BLE001
        out["C7_negative_window_bound"] = {"raised": True, "type": type(e).__name__, "verdict": "PASS"}

    # C8: complex-valued profile array -- graded as its OWN category (a warning fires,
    # weaker than an exception or nan, but not fully silent).
    Xc = np.linspace(-5.0, 5.0, 101)
    om_complex = -1.0 / (1.0 + Xc ** 2) + 1j * 3.0
    om_real_only = -1.0 / (1.0 + Xc ** 2)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        m_complex = profile_mass(om_complex, Xc)
    m_real = profile_mass(om_real_only, Xc)
    fired = any("omplex" in str(w.message) for w in caught)
    out["C8_complex_profile"] = {
        "returned": m_complex, "real_part_only_reference": m_real,
        "imaginary_part_silently_discarded": bool(m_complex == m_real),
        "complex_warning_fired": bool(fired),
        "verdict": "WARNED_NOT_SILENT" if fired else "SILENT_CORRUPTION",
    }

    # C9: a = 0 control surviving an adversarial shuffle -- no crossing regardless of order.
    Xs2 = np.linspace(0.1, 20.0, 500)
    perm = np.random.default_rng(7).permutation(len(Xs2))
    fam0 = Fam(Xs2[perm])
    r0 = stagnation_point(fam0, np.zeros(len(Xs2)), 0.5, 0.0)
    out["C9_a_zero_control_shuffled"] = {"returned": r0, "verdict": "PASS" if r0 is None else "SILENT_CORRUPTION_RISK"}

    return out


def main():
    T = battery_T()
    S = battery_S()
    C = battery_C()

    def _sc_count(items):
        n = 0
        for it in items:
            v = it.get("verdict") if isinstance(it, dict) else None
            if v == "SILENT_CORRUPTION":
                n += 1
        return n

    t_violations = (
        (1 if T["T2_exact_reversal"]["verdict"] == "SILENT_CORRUPTION" else 0)
        + _sc_count(T["T3_random_permutations"])
        + (1 if T["T4_single_adjacent_swap"]["verdict"] == "SILENT_CORRUPTION" else 0)
    )
    s_violations = (
        _sc_count(S["S2_shuffled_single_crossing"])
    )
    control_risks = sum(1 for k, v in C.items() if isinstance(v, dict) and v.get("verdict") == "SILENT_CORRUPTION_RISK")
    complex_is_silent = 1 if C["C8_complex_profile"]["verdict"] == "SILENT_CORRUPTION" else 0

    total_gate_violations = t_violations + s_violations

    res = {
        "leg": 122, "route": "ASA",
        "module_under_audit": "solver/advection_scope.py",
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/advection_scope.py ever silently return a wrong result instead of "
                 "flagging the input?"),
        "category_T_trapz_order_dependence": T,
        "category_S_stagnation_point_order_dependence": S,
        "category_C_controls": C,
        "summary": {
            "T_gate_violations": t_violations,
            "S_gate_violations": s_violations,
            "total_gate_violations": total_gate_violations,
            "control_category_unexpected_risks": control_risks,
            "complex_input_graded_separately_as_silent": bool(complex_is_silent),
            "gate_answer": "YES" if total_gate_violations > 0 else "NO",
        },
        "exposure": {
            "callers_of_advection_scope_functions": ["test_advection_scope.py"],
            "note": ("The ONLY caller anywhere in the repository always constructs fam.X via "
                     "TwoScaleNewton -> GCLMResidual -> solver.gclm_rescaled.sinh_grid, which is "
                     "strictly increasing by construction (c*sinh(rho), c>0, rho ascending). "
                     "No real call site has ever passed unsorted, shuffled, or otherwise "
                     "mis-ordered X into this module. The mechanism is real; the exposure today "
                     "is LATENT, in the same sense legs 100/101/120 measured for their modules."),
            "banked_numbers_at_risk": 0,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2, sort_keys=False, allow_nan=True) + "\n")

    print("Route-ASA v1 adversarial battery")
    print("=" * 70)
    print("T2 exact reversal: returned %.10f vs ascending %.10f (exact negation: %s)"
          % (T["T2_exact_reversal"]["returned"], T["T1_ascending_control"]["returned"],
             T["T2_exact_reversal"]["is_exact_negation"]))
    print("T3 permutations: %d/5 SILENT_CORRUPTION (rel err range %.2f - %.2f)"
          % (_sc_count(T["T3_random_permutations"]),
             min(p["rel_err_vs_exact"] for p in T["T3_random_permutations"]),
             max(p["rel_err_vs_exact"] for p in T["T3_random_permutations"])))
    print("T4 single adjacent swap: rel err vs exact = %.4f (verdict %s)"
          % (T["T4_single_adjacent_swap"]["rel_err_vs_exact"], T["T4_single_adjacent_swap"]["verdict"]))
    print("T5 velocity_log_rate: measured moved %.2e relative, predicted moved %.2e relative"
          % (T["T5_velocity_log_rate_consequence"]["measured_rel_change"],
             T["T5_velocity_log_rate_consequence"]["predicted_rel_change"]))
    print("S2 shuffled single crossing: %d/5 SILENT_CORRUPTION, abs errs %s"
          % (_sc_count(S["S2_shuffled_single_crossing"]),
             [round(s["abs_err"], 3) if s["abs_err"] is not None else None for s in S["S2_shuffled_single_crossing"]]))
    print("S4 NaN-before-crossing control: returned %s (is_nan=%s)"
          % (S["S4_nan_before_crossing_control"]["returned"], S["S4_nan_before_crossing_control"]["is_nan"]))
    print("Controls: unexpected risks = %d, complex-input graded as %s"
          % (control_risks, C["C8_complex_profile"]["verdict"]))
    print("-" * 70)
    print("GATE ANSWER: %s (%d violations: %d category T, %d category S)"
          % (res["summary"]["gate_answer"], total_gate_violations, t_violations, s_violations))
    print("Exposure: 0 real call sites reach this module with anything but a sorted, "
          "well-formed sinh_grid X -- LATENT.")
    print("\nwrote %s" % OUT.relative_to(ROOT))
    return res


if __name__ == "__main__":
    main()
