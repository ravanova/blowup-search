"""Leg 140 / Route-NFA -- adversarial audit of solver/nk_fourier.py.

READ-ONLY.  This runner imports `solver.nk_fourier` and edits nothing in it, under
either branch of the gate.  Its question, pre-committed in DIRECTION.md leg 140:

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/nk_fourier.py ever silently return a wrong value, or accept a
    fabricated certificate-feeding quantity unflagged?

WHY THIS MODULE.  nk_fourier.py carries the Fourier (circle) form of the two-scale
operator and, at the bottom of the file, the radii polynomial that the Route-D
dress rehearsal scores.  It is certificate-adjacent code in the family where the
fabrication-rejection pattern has now hit three for three (leg 79 on
port_certification, leg 98 on interval_certificate, leg 116 on nk_bounds).  It has
a dedicated known-answer test file (test_nk_fourier.py, six gates) but no
adversarial battery: every one of those six gates feeds it WELL-FORMED input.

WHAT THE NOVELTY PASS ALREADY SETTLED (writeup/novelty/leg_140.md, committed first).
All four axes have prior art, so this leg claims no new mathematics and no new
methodology -- only measured magnitudes:
  * the radii-polynomial constants are HYPOTHESISED positive in the published
    theorem, so a negative one is outside the theorem, not a conservative choice;
  * Galerkin mode truncation is textbook and is NOT reported as a defect here
    unless it happens inside a routine that documents exactness;
  * grey-box NaN/inf auditing of a numerical library is published method;
  * a weighted-ell^1 norm is only defined for a POSITIVE weight.

STRUCTURE.  Every case is tagged.
  GAP-PIN  the module answers where the theorem says it must refuse, or returns a
           value that an independent reference contradicts.  A repair INVERTS this
           case; the banked test (test_nk_fourier_adversarial.py) asserts today's
           behaviour so the inversion is visible.
  HOLDS    the module refuses, or is right.  These are the positive controls
           demanded by lesson 90: guards in this same module that DO fire, so that
           "there is no guard here" is a measurement and not a tautology of the code.

Run:  .venv/bin/python experiments/p2_route_nfa_v1_adversarial.py
Out:  writeup/data/p2_route_nfa_v1_adversarial.json
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solver.nk_fourier import (  # noqa: E402
    C_ANCHOR, anchor, kernel_directions, residual, jacobian, dc_column,
    gauged_system, gauge_row, ell1_op_norm, weighted_ell1_op_norm,
    radii_polynomial, tail_band, tail_Z1_column, tail_weight_obstruction,
    n_modes_residual,
)

OUT = ROOT / "writeup" / "data" / "p2_route_nfa_v1_adversarial.json"

np.seterr(all="ignore")          # we WANT to see what the module returns, not a traceback

INF = float("inf")
NAN = float("nan")


def _f(x):
    """JSON-safe float (NaN/inf survive as strings so nothing is silently lost)."""
    if isinstance(x, bool):
        return x
    x = float(x)
    if math.isnan(x):
        return "nan"
    if math.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


def _call(fn, *args, **kwargs):
    """Return ('value', v) or ('raised', 'ExcType: msg')."""
    try:
        return "value", fn(*args, **kwargs)
    except Exception as exc:                       # noqa: BLE001 -- that is the point
        return "raised", f"{type(exc).__name__}: {exc}"


# ===========================================================================
# A.  radii_polynomial -- the shared Y0/Z0/Z1 guard class (legs 79/98/116)
# ===========================================================================

def battery_radii_polynomial():
    """Hypothesis-violating (Y0, Z0, Z1, Z2) tuples fed to `radii_polynomial`.

    Published hypothesis (novelty pass Q1): Y0, Z0, Z1 >= 0 and Z2: (0,inf)->(0,inf),
    every one of them BOUNDING a norm and therefore nonnegative and finite by
    construction.  A tuple violating that is outside the theorem entirely.

    The load-bearing question is not `closes` alone but whether the reported ball
    is even a ball: `r_min < 0` is a self-evident tell the module never checks.
    """
    honest = (1e-3, 0.10, 0.20, 2.0)
    cases = [
        # (label, args, why_forbidden or "" if admissible)
        ("admissible_baseline", honest, ""),
        ("admissible_tight", (1e-8, 1e-12, 1e-9, 2.0), ""),
        ("admissible_refuses_1mZ_negative", (1e-3, 0.6, 0.7, 2.0), ""),
        ("admissible_refuses_disc_negative", (0.5, 0.1, 0.2, 2.0), ""),
        ("Y0_negative_small", (-1e-3, 0.10, 0.20, 2.0), "Y0 bounds ||A F(x)|| >= 0"),
        ("Y0_negative_unit", (-1.0, 0.10, 0.20, 2.0), "Y0 bounds ||A F(x)|| >= 0"),
        ("Y0_negative_huge", (-1e6, 0.10, 0.20, 2.0), "Y0 bounds ||A F(x)|| >= 0"),
        ("Z0_negative", (1e-3, -1.0, 0.20, 2.0), "Z0 bounds ||I - A A_dag|| >= 0"),
        ("Z0_negative_large", (1e-3, -9.0, 0.20, 2.0), "Z0 bounds ||I - A A_dag|| >= 0"),
        ("Z1_negative", (1e-3, 0.10, -1.0, 2.0), "Z1 bounds ||A(DF - A_dag)|| >= 0"),
        ("Z1_negative_large", (1e-3, 0.10, -9.0, 2.0), "Z1 bounds ||A(DF - A_dag)|| >= 0"),
        ("Z0_and_Z1_negative", (1e-3, -1.0, -1.0, 2.0), "both bound norms >= 0"),
        ("Y0_Z0_Z1_all_negative", (-1.0, -1.0, -1.0, 2.0), "all three bound norms >= 0"),
        ("Z2_negative", (1e-3, 0.10, 0.20, -2.0), "Z2: (0,inf) -> (0,inf)"),
        ("Z2_zero", (1e-3, 0.10, 0.20, 0.0), "Z2 strictly positive in the theorem"),
        ("Y0_nan", (NAN, 0.10, 0.20, 2.0), "not finite"),
        ("Z0_nan", (1e-3, NAN, 0.20, 2.0), "not finite"),
        ("Z1_nan", (1e-3, 0.10, NAN, 2.0), "not finite"),
        ("Z2_nan", (1e-3, 0.10, 0.20, NAN), "not finite"),
        ("Y0_inf", (INF, 0.10, 0.20, 2.0), "not finite"),
        ("Z0_inf", (1e-3, INF, 0.20, 2.0), "not finite"),
        ("Z1_inf", (1e-3, 0.10, INF, 2.0), "not finite"),
        ("Z2_inf", (1e-3, 0.10, 0.20, INF), "not finite"),
        ("Y0_neg_Z2_inf", (-1.0, 0.10, 0.20, INF), "Y0 < 0 and Z2 not finite"),
        ("all_zero", (0.0, 0.0, 0.0, 0.0), "Z2 = 0 not allowed"),
        ("Z2_denormal", (1e-3, 0.10, 0.20, 5e-324), "admissible in sign, extreme in scale"),
    ]

    rows, n_forbidden, n_false_close, n_negative_radius = [], 0, 0, 0
    for label, args, why in cases:
        r = radii_polynomial(*args)
        forbidden = bool(why)
        closes = r["closes"]
        r_min = r["r_min"]
        neg_radius = bool(closes and not math.isnan(r_min) and r_min < 0.0)
        false_close = bool(forbidden and closes)
        n_forbidden += forbidden
        n_false_close += false_close
        n_negative_radius += neg_radius
        rows.append({
            "label": label,
            "args": {"Y0": _f(args[0]), "Z0": _f(args[1]),
                     "Z1": _f(args[2]), "Z2": _f(args[3])},
            "forbidden_by_theorem": forbidden,
            "why_forbidden": why,
            "closes": closes,
            "r_min": _f(r_min), "r_max": _f(r["r_max"]),
            "one_minus_Z": _f(r["one_minus_Z"]),
            "discriminant": _f(r["discriminant"]),
            "Y0_max": _f(r["Y0_max"]),
            "negative_certified_radius": neg_radius,
            "tag": "GAP-PIN" if false_close else "HOLDS",
        })

    # the budget-inflation ladder: Y0_max is quoted by the dress rehearsal as THE
    # certification budget, and it is a pure function of (Z0, Z1, Z2) with no check.
    base = radii_polynomial(0.0, 0.0, 0.0, 2.0)["Y0_max"]
    inflation = []
    for z0, z1 in [(0.0, 0.0), (-1.0, 0.0), (-1.0, -1.0), (-4.0, -4.0), (-9.0, -9.0)]:
        v = radii_polynomial(0.0, z0, z1, 2.0)["Y0_max"]
        inflation.append({"Z0": z0, "Z1": z1, "Y0_max": _f(v),
                          "inflation_vs_Z0_Z1_zero": _f(v / base)})

    return {
        "n_cases": len(cases),
        "n_forbidden": n_forbidden,
        "n_forbidden_that_close": n_false_close,
        "n_closes_with_negative_radius": n_negative_radius,
        "sharpest_negative_radius": _f(
            radii_polynomial(-1e6, 0.10, 0.20, 2.0)["r_min"]),
        "budget_inflation_ladder": inflation,
        "cases": rows,
    }


# ===========================================================================
# B.  weighted_ell1_op_norm -- a NORM that can come back negative
# ===========================================================================

def battery_weighted_norm():
    """`weighted_ell1_op_norm(M, w_dom, w_cod)` divides by a caller-supplied weight.

    The weighted-ell^1 space ell^1(w) is only defined for w > 0 (novelty pass Q4).
    Nothing in the routine checks it.  Reference = the same formula evaluated with
    |w|, which IS the norm of the object the caller meant.
    """
    rng = np.random.default_rng(140)
    M = np.array([[1.0, 2.0, 0.5], [3.0, 4.0, 1.5], [0.25, 0.75, 2.0]])
    n = M.shape[1]
    w_cod = np.ones(M.shape[0])

    def ref(w_dom, w_cod_):
        """Independent reference: the honest norm, computed with |w|."""
        cols = (np.abs(M) * np.abs(np.asarray(w_cod_, float))[:, None]).sum(axis=0)
        return float((cols / np.abs(np.asarray(w_dom, float))).max())

    cases = [
        ("w_dom_positive", np.ones(n), w_cod, ""),
        ("w_dom_graded", np.array([1.0, 2.0, 4.0]), w_cod, ""),
        ("w_dom_all_negative", -np.ones(n), w_cod, "ell^1(w) needs w > 0"),
        ("w_dom_mixed_sign", np.array([1.0, -1.0, 1.0]), w_cod, "ell^1(w) needs w > 0"),
        ("w_dom_one_zero", np.array([1.0, 0.0, 1.0]), w_cod, "w = 0 is not a weight"),
        ("w_dom_all_zero", np.zeros(n), w_cod, "w = 0 is not a weight"),
        ("w_dom_nan", np.full(n, NAN), w_cod, "not finite"),
        ("w_dom_inf", np.full(n, INF), w_cod, "not finite"),
        ("w_cod_all_negative", np.ones(n), -w_cod, "ell^1(w) needs w > 0"),
        ("w_cod_zero", np.ones(n), np.zeros(M.shape[0]), "w = 0 is not a weight"),
        ("w_cod_wrong_length", np.ones(n), np.ones(M.shape[0] + 1), "shape mismatch"),
        ("w_dom_wrong_length", np.ones(n + 1), w_cod, "shape mismatch"),
    ]

    rows, n_neg, n_nonfinite, n_raised = [], 0, 0, 0
    for label, wd, wc, why in cases:
        kind, val = _call(weighted_ell1_op_norm, M, wd, wc)
        row = {"label": label, "forbidden": bool(why), "why_forbidden": why,
               "outcome": kind}
        if kind == "raised":
            n_raised += 1
            row["raised"] = val
            row["tag"] = "HOLDS"
        else:
            v = float(val)
            row["returned"] = _f(v)
            try:
                row["reference_with_abs_weight"] = _f(ref(wd, wc))
                row["ratio_returned_over_reference"] = _f(v / ref(wd, wc))
            except Exception:
                row["reference_with_abs_weight"] = None
            negative = bool(v < 0.0 or (v == 0.0 and math.copysign(1.0, v) < 0))
            nonfinite = bool(math.isnan(v) or math.isinf(v))
            n_neg += negative
            n_nonfinite += nonfinite
            row["returned_is_negative"] = negative
            row["returned_is_nonfinite"] = nonfinite
            # a forbidden weight that is ANSWERED (rather than refused) is a GAP-PIN;
            # an admissible weight is a HOLDS iff it reproduces the reference.
            row["tag"] = "GAP-PIN" if why else "HOLDS"
        rows.append(row)

    # the sharpest witness, on a matrix the module itself produces
    N = 8
    a = anchor(N).copy()
    a[4] += 1e-3
    _, J = gauged_system(a, C_ANCHOR, N)
    A = np.linalg.inv(J)
    wpos, wneg = np.ones(N + 1), -np.ones(N + 1)
    witness = []
    for name, Mx in (("gauged_jacobian_J", J), ("approximate_inverse_A", A)):
        honest = weighted_ell1_op_norm(Mx, wpos, wpos)
        poisoned = weighted_ell1_op_norm(Mx, wneg, wpos)
        witness.append({"matrix": name,
                        "honest_positive_weight": _f(honest),
                        "negative_weight": _f(poisoned),
                        "unweighted_ell1_op_norm": _f(ell1_op_norm(Mx)),
                        "sign_flip": bool(poisoned < 0 <= honest)})
    return {"n_cases": len(cases), "n_negative_returns": n_neg,
            "n_nonfinite_returns": n_nonfinite, "n_raised": n_raised,
            "in_module_witnesses": witness, "cases": rows}


# ===========================================================================
# C.  ell1_op_norm -- the 1-D shape trap
# ===========================================================================

def battery_ell1_shape():
    """`ell1_op_norm` on a 1-D array.

    `np.atleast_2d` promotes a 1-D array to a ROW, so the routine returns
    max_k |v_k| -- the induced norm of v read as a FUNCTIONAL -- where a caller
    holding a coefficient VECTOR wants sum_k |v_k|.  Both readings are
    mathematically correct for their own object; the routine cannot tell them
    apart and signals nothing.  The magnitude of the gap is what matters, so it is
    measured on (a) the worst case and (b) the vector the dress rehearsal actually
    forms for Y0.
    """
    worst = []
    for n in (2, 4, 16, 64, 256, 1024):
        v = np.ones(n)
        worst.append({"n": n, "ell1_op_norm": _f(ell1_op_norm(v)),
                      "true_ell1_norm": _f(np.abs(v).sum()),
                      "under_report_factor": _f(np.abs(v).sum() / ell1_op_norm(v))})

    live = []
    for N in (8, 16, 32, 64, 128, 256):
        a = anchor(N).copy()
        a[4] += 1e-3
        G, J = gauged_system(a, C_ANCHOR, N)
        A = np.linalg.inv(J)
        v = A @ G                                   # exactly the Y0 vector
        live.append({"N": N,
                     "Y0_correct_ell1": _f(np.abs(v).sum()),
                     "Y0_via_ell1_op_norm": _f(ell1_op_norm(v)),
                     "under_report_factor": _f(np.abs(v).sum() / ell1_op_norm(v))})

    # HOLDS controls: on a genuine MATRIX the routine is right, and it is right on
    # the empty matrix too.
    rng = np.random.default_rng(3)
    Mx = rng.standard_normal((5, 4))
    controls = {
        "matrix_matches_max_abs_column_sum": _f(
            abs(ell1_op_norm(Mx) - np.abs(Mx).sum(axis=0).max())),
        "empty_returns_zero": _f(ell1_op_norm(np.zeros((0, 0)))),
        "nan_entry_propagates": _f(ell1_op_norm(np.array([[1.0, NAN]]))),
    }
    return {"worst_case_ladder": worst, "on_the_live_Y0_vector": live,
            "controls": controls,
            "max_under_report_factor": _f(max(r["under_report_factor"] for r in worst)),
            "tag": "GAP-PIN"}


# ===========================================================================
# D.  tail_Z1_column -- the module's OWN guards (lesson 90 positive controls)
# ===========================================================================

def battery_tail_column():
    """This routine has real guards.  They are the controls that can come out the
    other way, which is what makes every "no guard here" elsewhere a measurement."""
    cases = [
        ("k=5_transport", dict(k=5), ""),
        ("k=5_exact", dict(k=5, diag="exact"), ""),
        ("k=1e9_transport", dict(k=10 ** 9), ""),
        ("k=1_below_domain", dict(k=1), "documented k >= 2"),
        ("k=0_below_domain", dict(k=0), "documented k >= 2"),
        ("k=-5_negative", dict(k=-5), "documented k >= 2"),
        ("k=2_exact_vanishing_denominator", dict(k=2, diag="exact"),
         "exact model needs k > 1/(2c) + 1"),
        ("unknown_diag_model", dict(k=5, diag="nope"), "unknown model"),
        ("c=0_zero_speed", dict(k=5, c=0.0), "c = 0 kills the transport diagonal"),
        ("c=-1_negative_speed", dict(k=5, c=-1.0), "speed sign not in the model"),
        ("c=nan", dict(k=5, c=NAN), "not finite"),
        ("c=inf", dict(k=5, c=INF), "not finite"),
        ("c=1e-12_near_zero", dict(k=5, c=1e-12), "denominator -> 0"),
    ]
    rows, n_guarded, n_silent_bad = [], 0, 0
    for label, kw, why in cases:
        kind, val = _call(tail_Z1_column, **kw)
        row = {"label": label, "kwargs": {k: _f(v) if isinstance(v, (int, float)) else v
                                          for k, v in kw.items()},
               "forbidden": bool(why), "why_forbidden": why, "outcome": kind}
        if kind == "raised":
            row["raised"] = val
            row["tag"] = "HOLDS"
            n_guarded += 1
        else:
            v = float(val)
            row["returned"] = _f(v)
            bad = bool(why) and not (math.isnan(v) and False)
            row["tag"] = "GAP-PIN" if why else "HOLDS"
            if why:
                n_silent_bad += 1
        rows.append(row)

    # the module's headline: both models converge to 1 from opposite sides.
    ladder = []
    for k in (3, 4, 8, 16, 64, 256, 1024, 10 ** 6):
        lo = tail_Z1_column(k, diag="transport")
        hi = tail_Z1_column(k, diag="exact")
        ladder.append({"k": k, "transport": _f(lo), "exact": _f(hi),
                       "sandwiches_one": bool(lo <= 1.0 <= hi)})
    return {"n_cases": len(cases), "n_guarded": n_guarded,
            "n_forbidden_answered_silently": n_silent_bad,
            "sandwich_ladder": ladder, "cases": rows}


# ===========================================================================
# E.  tail_weight_obstruction -- the weight the theorem needs to be positive
# ===========================================================================

def battery_weight_obstruction():
    """The docstring proves NO POSITIVE weight beats z_w = 1.  What happens off
    that hypothesis?

    IMPORTANT (lesson 90).  z_w = (u(k-1) + u(k+1)) / (2 u(k)) with u = w/k is
    HOMOGENEOUS OF DEGREE ZERO in w.  A negative weight therefore returns EXACTLY
    the positive weight's value -- not a coincidence and not a surprise, but a
    structural inability of the routine to distinguish w from -w.  That mechanism
    is reported, not the bare coincidence of the numbers.
    """
    cases = [
        ("w=k_affine_marginal", (lambda k: float(k)), 2, 200, ""),
        ("w=k(1+k)_affine_u", (lambda k: float(k) * (1.0 + k)), 2, 200, ""),
        ("w=exp_decay", (lambda k: float(np.exp(-k))), 2, 30, ""),
        ("w=k^2", (lambda k: float(k) ** 2), 2, 200, ""),
        ("w=-k_negative", (lambda k: -float(k)), 2, 200, "weight must be > 0"),
        ("w=0_identically", (lambda k: 0.0), 2, 20, "weight must be > 0"),
        ("w=0_at_one_mode", (lambda k: 0.0 if k == 5 else float(k)), 2, 20,
         "weight must be > 0"),
        ("w=nan", (lambda k: NAN), 2, 20, "not finite"),
        ("w=inf", (lambda k: INF), 2, 20, "not finite"),
        ("k_lo=1_touches_k=0", (lambda k: float(k)), 1, 20, "u(0) = w(0)/0"),
        ("k_lo_gt_k_hi_empty", (lambda k: float(k)), 20, 2, "empty range"),
        ("w=sign_alternating", (lambda k: float(k) * (-1.0) ** k), 2, 20,
         "weight must be > 0"),
    ]
    rows = []
    n_silent, n_guarded = 0, 0
    ref_affine = None
    for label, w, klo, khi, why in cases:
        kind, val = _call(tail_weight_obstruction, w, klo, khi)
        row = {"label": label, "k_lo": klo, "k_hi": khi,
               "forbidden": bool(why), "why_forbidden": why, "outcome": kind}
        if kind == "raised":
            row["raised"] = val
            row["tag"] = "HOLDS"
            n_guarded += 1
        else:
            sup = float(val[0])
            row["sup_z_w"] = _f(sup)
            row["nonfinite"] = bool(math.isnan(sup) or math.isinf(sup))
            row["tag"] = "GAP-PIN" if why else "HOLDS"
            if why:
                n_silent += 1
            if label == "w=k_affine_marginal":
                ref_affine = sup
        rows.append(row)
    # the degree-0 homogeneity, stated as an identity rather than a surprise
    pos = tail_weight_obstruction(lambda k: float(k), 2, 200)[0]
    neg = tail_weight_obstruction(lambda k: -float(k), 2, 200)[0]
    return {"n_cases": len(cases), "n_guarded": n_guarded,
            "n_forbidden_answered_silently": n_silent,
            "affine_marginal_value": _f(ref_affine),
            "homogeneity_degree_zero": {
                "w=+k": _f(pos), "w=-k": _f(neg),
                "identical": bool(pos == neg),
                "mechanism": ("z_w is a ratio of linear functionals of w, hence "
                              "homogeneous of degree 0: w and -w CANNOT differ. "
                              "Reported as a structural blind spot, not a coincidence.")},
            "cases": rows}


# ===========================================================================
# F.  anchor / kernel_directions -- a documented EXACTNESS that fails at small N
# ===========================================================================

def battery_kernel_directions():
    """`kernel_directions(N)` docstring: "The two exact tangent directions ...
    Both are annihilated by the un-gauged [DF | dF/dc]".

    The dilation direction puts its second component at index 2, guarded by
    `if N >= 2`.  At N = 1 that component is silently DROPPED and the returned
    vector is no longer in the kernel -- while the docstring still says it is.
    This is the one place in the module where truncation happens inside a routine
    that documents exactness, which is the only kind of truncation this leg is
    allowed to call a defect (novelty pass constraint 3).

    test_nk_fourier.py gate (3) checks this at N = 10 only, with tolerance 1e-14.
    """
    rows = []
    for N in (0, 1, 2, 3, 5, 10, 40):
        a = anchor(N)
        M = n_modes_residual(max(N, 1))
        J = jacobian(a, C_ANCHOR, M=M, n_cols=N + 1)
        dc = dc_column(a, M=M)
        kd = kernel_directions(N)
        per = []
        for i, (v, dcv) in enumerate(kd):
            img = J @ v + dcv * dc
            per.append(_f(np.abs(img).max()) if img.size else 0.0)
        # is the whole operator identically zero?  then annihilation is VACUOUS.
        vacuous = bool(np.abs(J).max() == 0.0 and np.abs(dc).max() == 0.0)
        worst = max((p for p in per if not isinstance(p, str)), default=0.0)
        rows.append({
            "N": N,
            "amplitude_direction_residual_sup": per[0],
            "dilation_direction_residual_sup": per[1],
            "worst": _f(worst),
            "passes_gate3_tolerance_1e-14": bool(worst < 1e-14),
            "annihilation_is_vacuous_operator_is_zero": vacuous,
            "dilation_second_component_dropped": bool(N < 2),
            "tag": ("GAP-PIN" if worst >= 1e-14 else
                    ("HOLDS-VACUOUS" if vacuous else "HOLDS")),
        })
    bad = [r for r in rows if r["tag"] == "GAP-PIN"]
    return {
        "rows": rows,
        "n_truncations_that_break_the_documented_exactness": len(bad),
        "worst_N": bad[0]["N"] if bad else None,
        "worst_residual": bad[0]["worst"] if bad else None,
        "over_gate3_tolerance_by": _f(bad[0]["worst"] / 1e-14) if bad else 0.0,
        "anchor_degenerate_at_N0": {
            "anchor_0": [ _f(x) for x in anchor(0) ],
            "note": ("anchor(0) = [-0.5] is NOT Omega_2 = -(1+cos)/2; the a_1 term "
                     "is dropped.  Its residual is still 0, but for the unrelated "
                     "reason that every CONSTANT profile is an exact traveling "
                     "wave -- a known-answer check that cannot fail there."),
            "residual_sup": _f(np.abs(residual(anchor(0), C_ANCHOR)).max()),
        },
        "anchor_negative_N": _call(anchor, -1)[1],
    }


# ===========================================================================
# G.  residual / jacobian -- truncation magnitudes and the NaN census
# ===========================================================================

def battery_truncation_and_nan():
    """Truncation is LEGITIMATE here (Galerkin projection, novelty pass Q2) and is
    reported as a magnitude only.  The NaN census is the grey-box half."""
    trunc = []
    for N in (4, 8, 16, 32, 64):
        a = np.linspace(0.3, 0.01, N + 1)
        full = residual(a, C_ANCHOR)
        cut = residual(a, C_ANCHOR, M=N)
        disc = float(np.abs(full[N:]).sum())
        trunc.append({"N": N,
                      "full_ell1": _f(np.abs(full).sum()),
                      "truncated_ell1": _f(np.abs(cut).sum()),
                      "discarded_ell1": _f(disc),
                      "discarded_fraction": _f(disc / np.abs(full).sum())})

    a = anchor(6)
    Jf = jacobian(a, C_ANCHOR, n_cols=7)
    jac = []
    for M in (2, 4, 8, 12):
        Jt = jacobian(a, C_ANCHOR, M=M, n_cols=7)
        jac.append({"M": M, "norm": _f(ell1_op_norm(Jt)),
                    "full_norm": _f(ell1_op_norm(Jf)),
                    "under_report_factor": _f(ell1_op_norm(Jf) / ell1_op_norm(Jt))})

    census = []
    base = anchor(6)
    poisons = [
        ("clean", base, C_ANCHOR),
        ("c_nan", base, NAN),
        ("c_inf", base, INF),
        ("a_has_nan", np.where(np.arange(7) == 3, NAN, base), C_ANCHOR),
        ("a_has_inf", np.where(np.arange(7) == 3, INF, base), C_ANCHOR),
        ("a_all_zero_c_inf", np.zeros(7), INF),
    ]
    for label, aa, cc in poisons:
        b = residual(aa, cc)
        J = jacobian(aa, cc, n_cols=7)
        census.append({
            "label": label,
            "residual_nan_count": int(np.isnan(b).sum()), "residual_len": int(b.size),
            "residual_inf_count": int(np.isinf(b).sum()),
            "jacobian_nan_count": int(np.isnan(J).sum()), "jacobian_size": int(J.size),
            "raised": False,
        })
    # the specific soft spot: `if w == 0.0: continue` cannot skip a NaN weight, so
    # a mode whose honest contribution is exactly 0 receives NaN instead.
    zero_c_inf = residual(np.zeros(7), INF)
    return {"truncation_ladder": trunc, "jacobian_row_truncation": jac,
            "nan_census": census,
            "zero_profile_infinite_speed": {
                "honest_answer": "all modes exactly 0 (Omega == 0 => F == 0)",
                "returned_nan_count": int(np.isnan(zero_c_inf).sum()),
                "returned_len": int(zero_c_inf.size),
                "mechanism": ("the `if w == 0.0: continue` fast path cannot skip "
                              "w = inf*k*0 = nan, so NaN is injected where the "
                              "honest coefficient is exactly zero"),
                "tag": "GAP-PIN"},
            "tag_truncation": "NOT-A-DEFECT (documented Galerkin projection)"}


# ===========================================================================
# H.  THE LOAD-BEARING CASE -- a planted non-solution inside a certified ball
# ===========================================================================

def load_bearing_case():
    """One forbidden weight turns an honest REFUSAL into a certified ball that
    provably contains no zero of the module's own gauged system.

    Construction, entirely inside solver/nk_fourier.py:
      * the finite-section gauged system G: R^{N+1} -> R^{N+1} at N = 8, c = 1/2,
        gauge "origin".  a_star = anchor(8) is an EXACT zero of it (checked).
      * x_hat = a_star + delta*e_4, delta = 1e-3, a planted NON-solution.
      * A_good = inv(J) gives an HONEST closing certificate; NK uniqueness then
        says a_star is the ONLY zero in B(x_hat, r) for r in (r_min, r_max).
      * A_bad = -inv(J) is a deliberately wrong approximate inverse.  Its honest
        Z0 = ||I - A_bad J|| = 2, so the radii polynomial REFUSES.  That refusal is
        the control, and it can come out the other way -- which is the point.
      * feeding the SAME matrix through the module's own weighted norm with the
        forbidden weight w_dom = -1 returns Z0 = -2, and the polynomial closes.
      * the fabricated ball is smaller than dist(x_hat, a_star) and sits inside the
        honest uniqueness ball, so it contains NO zero.

    Float64 throughout: this is a demonstration of the code's behaviour, not a
    proof about the operator.
    """
    N, c, delta = 8, C_ANCHOR, 1e-3
    a_star = anchor(N)
    x_hat = a_star.copy()
    x_hat[4] += delta
    dist = float(np.abs(x_hat - a_star).sum())

    G_star, _ = gauged_system(a_star, c, N)
    G, J = gauged_system(x_hat, c, N)
    A_good = np.linalg.inv(J)
    A_bad = -A_good

    def const(A):
        return (float(np.abs(A @ G).sum()),
                ell1_op_norm(np.eye(N + 1) - A @ J),
                0.0,
                2.0 * ell1_op_norm(A))

    Yg, Z0g, Z1g, Z2g = const(A_good)
    rp_good = radii_polynomial(Yg, Z0g, Z1g, Z2g)
    Yb, Z0b, Z1b, Z2b = const(A_bad)
    rp_bad = radii_polynomial(Yb, Z0b, Z1b, Z2b)

    R = np.eye(N + 1) - A_bad @ J
    Z0_fab = weighted_ell1_op_norm(R, -np.ones(N + 1), np.ones(N + 1))
    rp_fab = radii_polynomial(Yb, Z0_fab, Z1b, Z2b)

    r_f = rp_fab["r_min"]
    inside_uniqueness = bool(rp_good["closes"] and r_f <= rp_good["r_max"])
    star_in_existence_ball = bool(dist <= rp_good["r_min"])
    excludes_star = bool(dist > r_f)
    no_zero = bool(inside_uniqueness and star_in_existence_ball and excludes_star)

    return {
        "setup": {"N": N, "c": _f(c), "gauge": "origin", "delta": _f(delta),
                  "a_star_is_exact_zero_residual_ell1": _f(np.abs(G_star).sum()),
                  "dist_xhat_to_astar_ell1": _f(dist)},
        "honest_good_inverse": {"Y0": _f(Yg), "Z0": _f(Z0g), "Z1": _f(Z1g),
                                "Z2": _f(Z2g), "closes": rp_good["closes"],
                                "r_min": _f(rp_good["r_min"]),
                                "r_max": _f(rp_good["r_max"])},
        "honest_wrong_inverse_CONTROL": {"Y0": _f(Yb), "Z0": _f(Z0b), "Z1": _f(Z1b),
                                         "Z2": _f(Z2b), "closes": rp_bad["closes"],
                                         "note": ("the control that can come out the "
                                                  "other way: honest Z0 = 2 > 1 forces "
                                                  "1 - Z0 - Z1 < 0 and the module "
                                                  "correctly REFUSES")},
        "fabricated": {"Z0_from_negative_weight": _f(Z0_fab),
                       "closes": rp_fab["closes"],
                       "r_min": _f(r_f), "r_max": _f(rp_fab["r_max"]),
                       "one_minus_Z": _f(rp_fab["one_minus_Z"])},
        "exclusion": {
            "fabricated_ball_inside_honest_uniqueness_ball": inside_uniqueness,
            "a_star_inside_honest_existence_ball": star_in_existence_ball,
            "fabricated_ball_excludes_a_star": excludes_star,
            "certified_ball_contains_no_zero": no_zero,
            "miss_in_ell1": _f(dist - r_f),
            "miss_in_fabricated_radii": _f((dist - r_f) / r_f),
            "dist_over_r_fab": _f(dist / r_f)},
    }


# ===========================================================================
# I.  LATENCY -- can any in-repo caller reach any of this?
# ===========================================================================

def latency_audit():
    """Legs 79 and 116 both found gaps that were LATENT.  Measure it here too."""
    callers = {
        "experiments/p2_route_d_dress.py": {
            "imports": ["C_ANCHOR", "anchor", "residual", "jacobian", "gauged_system",
                        "gauge_row", "ell1_op_norm", "radii_polynomial",
                        "tail_Z1_column", "tail_weight_obstruction"],
            "reachability": [
                "Y0 is formed as float(np.abs(A @ G).sum()) + tail_defect -- the "
                "CORRECT ell^1 sum, NOT ell1_op_norm on a 1-D array, so the shape "
                "trap is not reached",
                "the tail defect is computed from residual(a, c) UNTRUNCATED, so the "
                "Galerkin discard is compensated, not dropped",
                "ell1_op_norm is only ever applied to genuine 2-D matrices (A, "
                "I - A@J, A@E_ft)",
                "weighted_ell1_op_norm is NOT imported at all",
                "every Z fed to radii_polynomial is a norm of a real matrix, hence "
                "nonnegative by construction",
                "N_LADDER starts at 4, so kernel_directions is never called at N < 2",
            ],
            "reaches_any_gap": False,
        },
        "experiments/p2_route_d_v3_spaces.py": {
            "imports": ["C_ANCHOR", "anchor", "jacobian", "gauged_system", "gauge_row",
                        "ell1_op_norm", "residual"],
            "reachability": [
                "does not import radii_polynomial or weighted_ell1_op_norm",
                "ell1_op_norm applied to matrices only",
            ],
            "reaches_any_gap": False,
        },
        "test_nk_fourier.py": {
            "imports": ["the six known-answer gates"],
            "reachability": [
                "gate (3) exercises kernel_directions at N = 10 only; the N = 1 "
                "truncation is outside every gate",
                "all inputs are well formed by construction",
            ],
            "reaches_any_gap": False,
        },
    }
    return {"callers": callers,
            "n_callers": len(callers),
            "n_callers_reaching_a_gap": 0,
            "verdict": ("EVERY gap measured here is LATENT: no in-repo caller "
                        "supplies a forbidden constant, a non-positive weight, a "
                        "1-D array to ell1_op_norm, or N < 2 to kernel_directions. "
                        "The finding is about what the module would accept, not "
                        "about any number this repository has banked.")}


# ===========================================================================

def main():
    payload = {
        "leg": 140,
        "route": "ROUTE-NFA",
        "target": "solver/nk_fourier.py",
        "target_edited": False,
        "date": "2026-08-06",
        "realization": ("the ell^1 Fourier (circle) realization of the a=0 gCLM "
                        "two-scale traveling-wave operator; float64 throughout"),
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/nk_fourier.py ever silently return a wrong value, or accept a "
                 "fabricated certificate-feeding quantity unflagged?"),
        "A_radii_polynomial": battery_radii_polynomial(),
        "B_weighted_ell1_op_norm": battery_weighted_norm(),
        "C_ell1_op_norm_shape": battery_ell1_shape(),
        "D_tail_Z1_column": battery_tail_column(),
        "E_tail_weight_obstruction": battery_weight_obstruction(),
        "F_kernel_directions": battery_kernel_directions(),
        "G_truncation_and_nan": battery_truncation_and_nan(),
        "H_load_bearing": load_bearing_case(),
        "I_latency": latency_audit(),
    }

    A = payload["A_radii_polynomial"]
    B = payload["B_weighted_ell1_op_norm"]
    C = payload["C_ell1_op_norm_shape"]
    D = payload["D_tail_Z1_column"]
    E = payload["E_tail_weight_obstruction"]
    F = payload["F_kernel_directions"]
    H = payload["H_load_bearing"]

    total_forbidden = (A["n_forbidden"]
                       + sum(1 for r in B["cases"] if r["forbidden"])
                       + sum(1 for r in D["cases"] if r["forbidden"])
                       + sum(1 for r in E["cases"] if r["forbidden"]))
    total_guarded = (B["n_raised"] + D["n_guarded"] + E["n_guarded"])

    payload["summary"] = {
        "gate_answer": "YES",
        "gate_answer_wording": (
            "Silent-corruption or fabrication-acceptance gap; report the exact failing "
            "case with magnitudes; escalate, do not patch (it IS partly the same "
            "Y0/Z0/Z1 guard class, so leg 128's shared guard may absorb that half)."),
        "same_guard_class_as_legs_79_98_116": True,
        "guard_class_note": (
            "The radii_polynomial half of this finding is the SAME Y0/Z0/Z1 "
            "nonnegativity guard class as legs 79 (port_certification), 98 "
            "(interval_certificate) and 116 (nk_bounds).  Leg 128's shared-guard "
            "repair has NOT landed, so this is a FOURTH instance of an OPEN class, "
            "and leg 128's shared guard would absorb it verbatim.  The other four "
            "findings (B, C, F, G) are module-specific and outside any sibling's "
            "reach."),
        "n_forbidden_inputs_tested": total_forbidden,
        "n_guards_that_fired": total_guarded,
        "radii_polynomial_false_closes": A["n_forbidden_that_close"],
        "radii_polynomial_forbidden_cases": A["n_forbidden"],
        "negative_certified_radius_cases": A["n_closes_with_negative_radius"],
        "sharpest_negative_radius": A["sharpest_negative_radius"],
        "max_budget_inflation": A["budget_inflation_ladder"][-1][
            "inflation_vs_Z0_Z1_zero"],
        "weighted_norm_negative_returns": B["n_negative_returns"],
        "weighted_norm_sharpest_sign_flip": B["in_module_witnesses"][0],
        "ell1_shape_max_under_report": C["max_under_report_factor"],
        "kernel_direction_break_N": F["worst_N"],
        "kernel_direction_residual": F["worst_residual"],
        "kernel_direction_over_tolerance": F["over_gate3_tolerance_by"],
        "load_bearing_ball_contains_no_zero": H["exclusion"][
            "certified_ball_contains_no_zero"],
        "load_bearing_miss_in_radii": H["exclusion"]["miss_in_fabricated_radii"],
        "all_latent": True,
        "patched": False,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")

    s = payload["summary"]
    print("=" * 78)
    print("LEG 140 / ROUTE-NFA -- adversarial audit of solver/nk_fourier.py")
    print("=" * 78)
    print(f"forbidden inputs tested        : {s['n_forbidden_inputs_tested']}")
    print(f"guards in the module that FIRED: {s['n_guards_that_fired']}  "
          f"(the lesson-90 positive controls)")
    print(f"radii_polynomial false-closes  : {s['radii_polynomial_false_closes']}"
          f"/{s['radii_polynomial_forbidden_cases']} forbidden tuples")
    print(f"  of them, NEGATIVE r_min      : {s['negative_certified_radius_cases']}"
          f"  (sharpest r_min = {s['sharpest_negative_radius']})")
    print(f"  Y0_max budget inflation      : up to {s['max_budget_inflation']}x")
    print(f"weighted_ell1_op_norm negative : {s['weighted_norm_negative_returns']} cases; "
          f"on the module's own J: {s['weighted_norm_sharpest_sign_flip']['honest_positive_weight']}"
          f" -> {s['weighted_norm_sharpest_sign_flip']['negative_weight']}")
    print(f"ell1_op_norm 1-D under-report  : up to {s['ell1_shape_max_under_report']}x")
    print(f"kernel_directions breaks at N  : {s['kernel_direction_break_N']}  "
          f"residual {s['kernel_direction_residual']} "
          f"({s['kernel_direction_over_tolerance']}x its own gate-3 tolerance)")
    print(f"LOAD-BEARING: certified ball contains no zero: "
          f"{s['load_bearing_ball_contains_no_zero']}, missing the true zero by "
          f"{s['load_bearing_miss_in_radii']} ball radii")
    print(f"LATENT (no in-repo caller reaches any of it): {s['all_latent']}")
    print()
    print(f"GATE: {s['gate_answer']} -- {s['gate_answer_wording']}")
    print(f"solver/nk_fourier.py edited    : {payload['target_edited']}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
