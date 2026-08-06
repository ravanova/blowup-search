"""Route-NKA (leg 116): the fabrication-rejection battery for `solver/nk_bounds.py`.

WHAT THIS ASKS, AND WHY IT IS NOT `test_nk_bounds.py`'s QUESTION
-----------------------------------------------------------------------------
`test_nk_bounds.py` (Route-D, legs v6-v11) gates the COMPLETENESS direction: every
quantity in the module dominates an independently computed measurement, and it does so
against an ADVERSARY rather than a random family.  Every one of those gates hands the
module a WELL-FORMED problem.  This leg asks the SOUNDNESS question, which nothing in
the repository asks of this module: **when the input is not well formed, does it still
report a certified ball -- and can a planted non-solution survive inside it?**

The question is not speculative.  Leg 79 asked it of `port_certification.radii_polynomial_status`
(11/25 hypothesis-violating inputs returned `closes=True`), leg 98 asked it of
`interval_certificate.interval_constants` -> `radii_verdict` (12/36, 8 load-bearing; since
repaired).  `nk_bounds.py` is the third and last certificate-assembly module nobody has
pointed the battery at -- and it differs from both siblings in a way that gives this leg a
second question they could not ask.  Unlike them, `nk_bounds.py` also MANUFACTURES the
constants it feeds to its own verdict, in plain float64, by NUMERICALLY EVALUATING a
supremum and an improper integral.  So two links are audited, not one:

    the verdict            `budget`
    the bound producers    `farfield_modelling_error_bound`, `hilbert_farfield_bound`,
                           `quadratic_constant_upper`, `two_point_dual` / `sup_part_upper`

WHAT COUNTS AS A FAILURE, PRE-COMMITTED
-----------------------------------------------------------------------------
Three hypothesis families, all three established as textbook prior art in
`writeup/novelty/leg_116.md` -- none of them is a finding of this leg:

  (H1) THE THEOREM'S.  `Y_0`, `Z_0`, `Z_1`, `Z_2` are upper bounds on norms, hence FINITE
       and NONNEGATIVE, and the conclusion drawn is existence and uniqueness of a zero
       INSIDE the ball of radius `r_min`.  So a negative constant is not a pessimistic
       input, and a `closes=True` carrying a non-positive `r_min` is not a conservative
       verdict: it asserts a zero inside a degenerate or empty set.
  (H2) THE SUPREMUM'S.  A supremum is not the maximum over a finite, TRUNCATED sample
       grid.  This is the founding premise of interval branch-and-bound.  The module's
       own docstring states the hypothesis under which sampling is legitimate here ("For
       alpha < 2 both terms decay, so the supremum sits at X0"); the only question is
       whether the code ENFORCES it.
  (H3) THE NORM'S.  A weight vector defines a norm, so it is strictly positive and finite,
       and the seminorm kernel `q_cod` is non-negative with zeros ONLY on the diagonal
       (where the suppressed term is genuinely zero).

Outcomes recorded per case; only the first two are failures:

  `false_accept`  `budget` returned closes=True on a hypothesis-violating input   -- UNSOUND
  `false_bound`   a function claiming an UPPER bound returned a value strictly
                  BELOW an independently computed reference                       -- UNSOUND
  `sound`         the value dominates the reference, or the verdict refused       -- sound
  `rejected`      closes=False, for any reason                                    -- sound
  `raised`        an exception propagated -- sound but loud, recorded separately
                  because a caller that catches broadly could turn it into a silent skip

`load_bearing` is recorded separately and is the sharper claim: the hypothesis-SATISFYING
counterpart of the same magnitude does NOT close, so the violation is exactly what bought
the certificate.  `reachable` is recorded per family and is the honest ceiling: a defect no
in-repo caller can reach is reported as LATENT, with the callers named (leg 79's convention).

MAGNITUDES, NOT BOOLEANS (discipline 73)
-----------------------------------------------------------------------------
Every case records the numbers, so the arithmetic can be rechecked from the JSON without
rerunning anything.  A false accept is reported with the certified ball it produced, the
planted point's residual, and the distance from that ball to the nearest true zero measured
IN BALL RADII.  A false bound is reported as a ratio reference/module.

THE INDEPENDENT REFERENCE, AND WHY IT IS NOT THE MODULE
-----------------------------------------------------------------------------
Family B needs a ground truth for an improper integral that the module evaluates by
trapezoid on a log grid.  Using a finer version of the MODULE'S OWN quadrature is not a
reference -- it inherits the same grid floor and the same truncation, and the first draft of
this battery was fooled by exactly that (it reported a 22x "under-report" at alpha=1.99 that
was its own reference over-shooting).  `_I_out_reference` below is built independently:
composite Simpson on a LINEAR grid over [0, 50] where the mass of `(1+y^2)^{-alpha/2}`
actually sits, a log-substituted Simpson beyond it, and an ANALYTIC tail
`2X y^{-(alpha+1)}/(alpha+1)` past the cut, so nothing is discarded.  It is validated
against the sharp asymptote the module's own docstring states -- `I_out -> M_alpha / X` --
and reproduces it to 5 digits at X = 1e8..1e14 (`reference_validation` in the JSON).

CONTROLS (lesson 90 -- a control that cannot come out differently is not a control)
-----------------------------------------------------------------------------
Every judgement instrument in this battery is shown reporting BOTH answers:
  * the planted-point substrate closes honestly at the good centre and refuses honestly at
    the planted one, before any poison is applied;
  * the reference integrator reports `sound` across the whole documented alpha < 2 sweep and
    `false_bound` outside it -- the same instrument, both verdicts;
  * `budget` is shown rejecting NaN and +inf constants, so "nothing closes any more" cannot
    masquerade as robustness.

Run: .venv/bin/python experiments/p2_route_nka_v1_adversarial.py
"""

import json
import math
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import grid                              # noqa: E402
from solver.decay_grading import cos_power_mass                        # noqa: E402
from solver.holder_norms import HolderNorm                             # noqa: E402
from solver.nk_bounds import (                                         # noqa: E402
    _I_out, budget, farfield_modelling_error_bound, hilbert_farfield_bound,
    holder_local_X_constant, quadratic_constant_upper, sup_part_upper, two_point_dual,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_nka_v1_adversarial.json")

# The live operating range, read off the in-repo callers rather than assumed.
# experiments/p2_route_d_v6_bounds.py: X0s = (50 .. 3200), alphas = (1.1 .. 1.8),
# GAMMA = 0.5, and farfield_modelling_error_bound samples out to X0 * 1e4.
LIVE_ALPHAS = (1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8)
LIVE_X0S = (50.0, 100.0, 200.0, 400.0, 800.0, 1600.0, 3200.0)
LIVE_GAMMA = 0.5
LIVE_X_MAX = max(LIVE_X0S) * 1e4          # 3.2e7 -- the largest X any caller evaluates at


# ===========================================================================
# THE INDEPENDENT REFERENCE  (family B's ground truth; NOT the module's quadrature)
# ===========================================================================


def _simpson(f, a, b, n=8000):
    n = n if n % 2 == 0 else n + 1
    x = np.linspace(a, b, n + 1)
    h = (b - a) / n
    y = f(x)
    return float(h / 3.0 * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-2:2].sum()))


def _I_out_reference(X, alpha, Ycut=1e14, n=8000):
    """Independent high-accuracy value of the integral `_I_out` estimates.

    int over y >= 0, |y - X| > X/2, of (1+y^2)^{-alpha/2} |2X/(X^2-y^2)| dy.

    Built so that NOTHING it does resembles what `_I_out` does: the mass region
    y = O(1) is integrated on a LINEAR Simpson grid (the module uses a log grid with a
    floor at 1e-12 X, which is the whole mechanism family B measures), and the outer
    tail past `Ycut` is added ANALYTICALLY using |2X/(X^2-y^2)| <= 2X/y^2 for y >= 3X,
    so the reference is an upper bound on its own truncation rather than a truncation.
    """
    X = float(X)

    def g(y):
        return (1.0 + y ** 2) ** (-0.5 * alpha) * np.abs(2.0 * X / (X * X - y * y))

    total = 0.0
    b1 = min(0.5 * X, 50.0)
    total += _simpson(g, 0.0, b1, n)
    if 0.5 * X > b1:
        total += _simpson(lambda u: g(np.exp(u)) * np.exp(u),
                          math.log(b1), math.log(0.5 * X), n)
    lo, hi = 1.5 * X, max(float(Ycut), 3.0 * X)
    total += _simpson(lambda u: g(np.exp(u)) * np.exp(u), math.log(lo), math.log(hi), n)
    total += 2.0 * X * hi ** (-(alpha + 1.0)) / (alpha + 1.0)
    return total


def _near_part(X, alpha, gamma):
    """The module's near-field half, which is CLOSED FORM and audited by hand.

    Reproduced here rather than imported so the reference does not inherit the module's
    arithmetic.  The derivation is sound: |h(X-t) - h(X+t)| <= S (2t)^gamma with the
    envelope evaluated at min(|y1|,|y2|) >= X/2 (decreasing, hence conservative), and
    |g(X-t) - g(X+t)| <= (16/15) t / X for t <= X/2 with g = 2X/(X+y) <= 4/3 on the band.
    """
    delta = 0.5 * X
    S = float(holder_local_X_constant(alpha, gamma, 0.5 * X))
    env = (1.0 + (0.5 * X) ** 2) ** (-0.5 * alpha)
    return (4.0 / 3.0) * S * (2.0 ** gamma) * delta ** gamma / gamma \
        + (16.0 / 15.0) * env * delta / X


def _hilbert_reference(X, alpha, gamma):
    return (_near_part(X, alpha, gamma) + _I_out_reference(X, alpha)) / np.pi


def _modelling_integrand_reference(X, alpha, gamma):
    """The quantity `farfield_modelling_error_bound` takes the supremum of, from (E)."""
    t1 = 1.0 / (X * np.sqrt(1.0 + X * X))
    t2 = (1.0 + X * X) ** (0.5 * (alpha - 1.0)) * _hilbert_reference(X, alpha, gamma)
    return t1 + t2


def _reference_sup(alpha, gamma, X0, decades=12, n_X=48):
    """sup over the TRUE half-line {X >= X0}, sampled far beyond the module's window.

    Sampling still only bounds a supremum from below -- which is exactly the point: a
    LOWER bound on the truth that EXCEEDS the module's claimed upper bound is already a
    proof that the claimed bound is not one.  No claim is made that this is the sup.
    """
    Xs = np.geomspace(float(X0), float(X0) * 10.0 ** decades, int(n_X))
    vals = np.array([_modelling_integrand_reference(X, alpha, gamma) for X in Xs])
    i = int(vals.argmax())
    return float(vals[i]), float(Xs[i])


# ===========================================================================
# FAMILY P -- THE PLANTED NON-SOLUTION
# ===========================================================================
#
# A fully explicit scalar Newton-Kantorovich instance in which every constant is exact
# and the zero set is known in closed form, so "did a planted non-solution survive inside
# the reported ball" is decidable rather than argued.
#
#     F(x) = x^2 - 2 on R with |.|;   zeros exactly +-sqrt(2)
#     A    = 1 / F'(x_bar) = 1/(2 x_bar)                (the fixed approximate inverse)
#     Y_0(x) = |A F(x)|                                 (the residual bound)
#     Z_0(x) = |1 - A F'(x)|                            (A is only approximate away from x_bar)
#     Z_1    = 0                                        (no unbounded part in this model)
#     Z_2    = sup |A F''| = |1/x_bar|                  (exact; F'' == 2)
#
# The GOOD centre x_bar = 1.4 is a genuine approximate zero.  The PLANTED point x_tilde = 1.0
# is not: |F(1.0)| = 1, and the nearest zero is 0.414... away.  Honest constants at the
# planted point must NOT close -- and they do not.  That refusal is the control.

P_XBAR = 1.4
P_XPLANT = 1.0
P_ROOT = math.sqrt(2.0)


def _p_constants(x):
    A = 1.0 / (2.0 * P_XBAR)
    return {"Y0": abs(A * (x * x - 2.0)), "Z0": abs(1.0 - A * 2.0 * x),
            "Z1": 0.0, "Z2": abs(A * 2.0)}


def _ball_report(x_centre, verdict):
    """How badly did the reported ball miss?  In ball radii, not in adjectives.

    `r_min <= 0` is reported as a DEGENERATE ball rather than silently absolutised: the
    radii polynomial theorem concludes a zero exists inside the ball of radius `r_min`,
    so a non-positive `r_min` asserts a zero inside a point or an empty set, and it
    contains no zero of F either way.
    """
    r = verdict["r_min"]
    if not verdict["closes"] or not np.isfinite(r):
        return {"radius": (None if not np.isfinite(r) else float(r)),
                "degenerate": None, "ball_lo": None, "ball_hi": None,
                "contains_a_zero": None, "gap_to_nearest_zero": None,
                "gap_in_ball_radii": None}
    if r <= 0.0:
        return {"radius": float(r), "degenerate": True, "ball_lo": None, "ball_hi": None,
                "contains_a_zero": False,
                "gap_to_nearest_zero": float(abs(P_ROOT - x_centre)),
                "gap_in_ball_radii": None}
    lo, hi = x_centre - r, x_centre + r
    contains = bool((lo <= P_ROOT <= hi) or (lo <= -P_ROOT <= hi))
    gap = 0.0 if contains else min(abs(P_ROOT - hi), abs(lo - P_ROOT),
                                   abs(-P_ROOT - hi), abs(lo + P_ROOT))
    return {"radius": float(r), "degenerate": False,
            "ball_lo": float(lo), "ball_hi": float(hi), "contains_a_zero": contains,
            "gap_to_nearest_zero": float(gap), "gap_in_ball_radii": float(gap / r)}


def family_P():
    cases = []
    honest_good = _p_constants(P_XBAR)
    honest_plant = _p_constants(P_XPLANT)
    v_good = budget(**honest_good)
    v_plant = budget(**honest_plant)

    # -- the two controls, before any poison ------------------------------------------
    cases.append({"case": "P00_control_honest_good_centre", "family": "P",
                  "hypothesis_violating": False, "centre": P_XBAR,
                  "constants": honest_good, "verdict": v_good,
                  "outcome": "sound" if v_good["closes"] else "control_broken",
                  "ball": _ball_report(P_XBAR, v_good),
                  "note": "the honest certificate must still CLOSE at a genuine approximate zero"})
    cases.append({"case": "P01_control_honest_planted_point", "family": "P",
                  "hypothesis_violating": False, "centre": P_XPLANT,
                  "constants": honest_plant, "verdict": v_plant,
                  "outcome": "rejected" if not v_plant["closes"] else "false_accept",
                  "ball": _ball_report(P_XPLANT, v_plant),
                  "residual_at_planted_point": abs(P_XPLANT ** 2 - 2.0),
                  "distance_to_nearest_zero": abs(P_ROOT - P_XPLANT),
                  "note": "honest constants at the planted non-solution must REFUSE -- they do"})

    # -- the poisons, each a single H1 violation applied to the planted point ----------
    poisons = [
        ("P02_Y0_fabricated_zero", {"Y0": 0.0},
         "a residual reported as exactly zero -- leg 98's A1 case, in this module"),
        ("P03_Y0_sign_flipped", {"Y0": -honest_plant["Y0"]},
         "a signed residual used where its absolute value was meant"),
        ("P04_Z0_negative_unit", {"Z0": -1.0},
         "a negative Z_0: the theorem's contraction budget inflated from 0.71 to 2"),
        ("P05_Z1_negative_unit", {"Z1": -1.0},
         "a negative Z_1, the same inflation through the other slot"),
        ("P06_Z2_shrunk_1e-6", {"Z2": 1e-6},
         "a quadratic constant under-reported by six decades"),
        ("P07_Z2_negative", {"Z2": -0.7142857142857143},
         "a negative Z_2 -- the parabola opens downward"),
        ("P08_Y0_negative_and_Z0_negative", {"Y0": -honest_plant["Y0"], "Z0": -1.0},
         "two violations at once"),
        ("P09_Y0_tiny_fabricated", {"Y0": 1e-300},
         "a denormal-scale fabricated residual, not exactly zero"),
    ]
    for name, patch, note in poisons:
        c = dict(honest_plant); c.update(patch)
        v = budget(**c)
        ball = _ball_report(P_XPLANT, v)
        degenerate = bool(v["closes"] and not (np.isfinite(v["r_min"]) and v["r_min"] > 0.0))
        cases.append({
            "case": name, "family": "P", "hypothesis_violating": True,
            "centre": P_XPLANT, "constants": c, "poison": patch, "verdict": v,
            "outcome": "false_accept" if v["closes"] else "rejected",
            "load_bearing": bool(v["closes"] and not v_plant["closes"]),
            "degenerate_ball": degenerate, "ball": ball,
            "residual_at_planted_point": abs(P_XPLANT ** 2 - 2.0),
            "distance_to_nearest_zero": abs(P_ROOT - P_XPLANT),
            "note": note})
    return cases


# ===========================================================================
# FAMILY A -- `budget`'s DOMAIN VALIDATION
# ===========================================================================
#
# The reference tuple is one that HONESTLY closes; each case violates H1 in one slot, so
# `load_bearing` can be read off directly.  A second reference tuple that honestly does NOT
# close is used for the "does the violation RESCUE a hopeless case" family.

A_OK = {"Y0": 1e-6, "Z0": 0.0, "Z1": 0.3, "Z2": 1.0}          # closes honestly
A_HOPELESS = {"Y0": 1.0, "Z0": 0.0, "Z1": 0.3, "Z2": 1.0}     # cannot close honestly

INF = float("inf")
NAN = float("nan")


def family_A():
    v_ok = budget(**A_OK)
    v_hopeless = budget(**A_HOPELESS)
    cases = [
        {"case": "A00_control_honest_closes", "family": "A", "hypothesis_violating": False,
         "constants": dict(A_OK), "verdict": v_ok,
         "outcome": "sound" if v_ok["closes"] else "control_broken"},
        {"case": "A01_control_honest_hopeless", "family": "A", "hypothesis_violating": False,
         "constants": dict(A_HOPELESS), "verdict": v_hopeless,
         "outcome": "rejected" if not v_hopeless["closes"] else "false_accept"},
    ]
    variants = [
        # name                          base          patch
        ("A02_Y0_negative_unit",        A_HOPELESS, {"Y0": -1.0}),
        ("A03_Y0_negative_tiny",        A_HOPELESS, {"Y0": -1e-12}),
        ("A04_Y0_negative_huge",        A_HOPELESS, {"Y0": -1e12}),
        ("A05_Y0_zero_fabricated",      A_HOPELESS, {"Y0": 0.0}),
        ("A06_Y0_neg_inf",              A_HOPELESS, {"Y0": -INF}),
        ("A07_Y0_pos_inf",              A_HOPELESS, {"Y0": INF}),
        ("A08_Y0_nan",                  A_HOPELESS, {"Y0": NAN}),
        ("A09_Z0_negative_unit",        A_HOPELESS, {"Z0": -1.0}),
        ("A10_Z0_negative_huge",        A_HOPELESS, {"Z0": -1e6}),
        ("A11_Z0_neg_inf",              A_HOPELESS, {"Z0": -INF}),
        ("A12_Z0_nan",                  A_HOPELESS, {"Z0": NAN}),
        ("A13_Z1_negative_unit",        A_HOPELESS, {"Z1": -1.0}),
        ("A14_Z1_negative_huge",        A_HOPELESS, {"Z1": -1e6}),
        ("A15_Z1_neg_inf",              A_HOPELESS, {"Z1": -INF}),
        ("A16_Z1_nan",                  A_HOPELESS, {"Z1": NAN}),
        ("A17_Z2_negative_unit",        A_HOPELESS, {"Z2": -1.0}),
        ("A18_Z2_zero",                 A_HOPELESS, {"Z2": 0.0}),
        ("A19_Z2_nan",                  A_HOPELESS, {"Z2": NAN}),
        ("A20_Z2_pos_inf",              A_HOPELESS, {"Z2": INF}),
        ("A21_Z2_denormal",             A_HOPELESS, {"Z2": 1e-320}),
        ("A22_Y0_neg_Z1_neg",           A_HOPELESS, {"Y0": -1.0, "Z1": -1.0}),
        ("A23_Y0_neg_Z0Z1_sum_above_1", A_HOPELESS, {"Y0": -1.0, "Z0": 0.9, "Z1": 0.9}),
        ("A24_all_four_negative",       A_HOPELESS, {"Y0": -1.0, "Z0": -1.0,
                                                     "Z1": -1.0, "Z2": -1.0}),
        ("A25_Y0_negative_on_closing",  A_OK,       {"Y0": -1e-6}),
        ("A26_Z1_negative_on_closing",  A_OK,       {"Z1": -0.3}),
    ]
    for name, base, patch in variants:
        c = dict(base); c.update(patch)
        base_v = v_hopeless if base is A_HOPELESS else v_ok
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                v = budget(**c)
                outcome = "false_accept" if v["closes"] else "rejected"
                exc = ""
            except Exception as ex:                                     # noqa: BLE001
                v, outcome, exc = None, "raised", f"{type(ex).__name__}: {ex}"
        degenerate = bool(v and v["closes"]
                          and not (np.isfinite(v["r_min"]) and v["r_min"] > 0.0))
        cases.append({"case": name, "family": "A", "hypothesis_violating": True,
                      "constants": c, "poison": patch, "verdict": v, "outcome": outcome,
                      "exception": exc,
                      "load_bearing": bool(v and v["closes"] and not base_v["closes"]),
                      "degenerate_ball": degenerate})
    return cases


# ===========================================================================
# FAMILY B -- THE BOUND PRODUCERS vs THE INDEPENDENT REFERENCE
# ===========================================================================


def family_B(scope_alphas=(1.1, 1.5, 1.9), scope_gammas=(0.15, 0.5, 0.9),
             scope_X0s=(200.0, 3200.0), out_alphas=(2.0, 2.25, 2.5, 3.0)):
    cases = []

    # -- B1  INSIDE the documented alpha < 2 hypothesis (the negative control) ----------
    for a in scope_alphas:
        for g in scope_gammas:
            for X0 in scope_X0s:
                m = farfield_modelling_error_bound(a, g, X0)
                ref, ref_X = _reference_sup(a, g, X0)
                ratio = ref / m["bound"]
                window_end = X0 * 1e4
                cases.append({
                    "case": f"B1_scope_a{a}_g{g}_X0{int(X0)}", "family": "B",
                    "hypothesis_violating": False,
                    "alpha": a, "gamma": g, "X0": X0,
                    "module_bound": m["bound"], "module_argmax_X": m["argmax_X"],
                    "reference_sup_lower_bound": ref, "reference_argmax_X": ref_X,
                    "reference_over_module": ratio,
                    "argmax_at_window_end": bool(
                        abs(m["argmax_X"] - window_end) <= 1e-9 * window_end),
                    "outcome": "false_bound" if ratio > 1.0 else "sound"})

    # -- B2  OUTSIDE it, unenforced (the same instrument, the other answer) ------------
    for a in out_alphas:
        m = farfield_modelling_error_bound(a, LIVE_GAMMA, 1.0)
        ref, ref_X = _reference_sup(a, LIVE_GAMMA, 1.0)
        ratio = ref / m["bound"]
        cases.append({
            "case": f"B2_unguarded_alpha_{a}", "family": "B", "hypothesis_violating": True,
            "alpha": a, "gamma": LIVE_GAMMA, "X0": 1.0,
            "module_bound": m["bound"], "module_argmax_X": m["argmax_X"],
            "reference_sup_lower_bound": ref, "reference_argmax_X": ref_X,
            "reference_over_module": ratio,
            "argmax_at_window_end": bool(abs(m["argmax_X"] - 1e4) <= 1e-9 * 1e4),
            "outcome": "false_bound" if ratio > 1.0 else "sound",
            "note": ("the module docstring states 'For alpha < 2 both terms decay, so the "
                     "supremum sits at X0'; alpha >= 2 is not checked, and the function's "
                     "own argmax_X pins to the window's last sample -- a self-diagnostic "
                     "it computes and discards")})

    # -- B3  `_I_out`: the log-grid floor eps = 1e-12 * max(X,1) ------------------------
    # The mass of (1+y^2)^{-alpha/2} sits at y = O(1); the bulk grid's lower cut crosses
    # y = 1 at EXACTLY X = 1e12, and from there the first trapezoid panel [0, eps]
    # replaces the resolved mass region.
    for a in (1.2, 1.5, 1.9):
        for X in (1.0, 1e2, LIVE_X_MAX, 1e10, 1e11, 1e12, 1e13, 1e14):
            mv = _I_out(X, a)
            rv = _I_out_reference(X, a)
            ratio = rv / mv
            cases.append({
                "case": f"B3_Iout_a{a}_X{X:.0e}", "family": "B",
                "hypothesis_violating": False,
                "alpha": a, "X": X, "module": mv, "reference": rv,
                "reference_over_module": ratio,
                "relative_slack": (mv - rv) / rv,
                "inside_live_range": bool(X <= LIVE_X_MAX),
                "outcome": "false_bound" if ratio > 1.0 else "sound"})

    # -- B4  the quadrature's own resolution (is n=1201 the limiting factor?) -----------
    for a in (1.2, 1.5, 1.9):
        c, f = _I_out(1e3, a, n=1201), _I_out(1e3, a, n=200001)
        cases.append({"case": f"B4_quadrature_resolution_a{a}", "family": "B",
                      "hypothesis_violating": False, "alpha": a, "X": 1e3,
                      "n_default": c, "n_200001": f, "default_over_fine": c / f,
                      "outcome": "sound" if c >= f else "false_bound",
                      "note": "resolution slack, not the mechanism B3 measures"})

    # -- B5  gamma outside the Holder range (0, 1], unenforced -------------------------
    for g in (-0.5, -0.05, 0.0, 1.5, 3.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                b, near, out = hilbert_farfield_bound(10.0, 1.5, g)
                outcome = "false_bound" if (near < 0.0 or b < 0.0) else "sound"
                rec = {"bound": float(b), "near_part": float(near), "out_part": float(out)}
                exc = ""
            except Exception as ex:                                     # noqa: BLE001
                rec, outcome, exc = {}, "raised", f"{type(ex).__name__}: {ex}"
        ref_g = hilbert_farfield_bound(10.0, 1.5, 0.5)[0]
        cases.append({"case": f"B5_gamma_{g}", "family": "B", "hypothesis_violating": True,
                      "alpha": 1.5, "gamma": g, "X": 10.0, **rec, "exception": exc,
                      "gamma_half_reference": float(ref_g), "outcome": outcome,
                      "note": ("gamma is a Holder exponent in (0, 1]; the near-field half "
                               "carries a 1/gamma, so gamma < 0 flips its sign and REDUCES "
                               "the claimed upper bound")})

    # -- B6  alpha <= 1, where the far-field mass integral does not converge ------------
    for a in (0.5, 0.9, 1.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                q = quadratic_constant_upper(a, LIVE_GAMMA, n_X=20, n_quad=401)
                outcome, exc = "sound", ""
                rec = {"C_Q_sup_upper": q["C_Q_sup_upper"], "argmax_X": q["argmax_X"]}
            except Exception as ex:                                     # noqa: BLE001
                rec, outcome, exc = {}, "raised", f"{type(ex).__name__}: {ex}"
        cases.append({"case": f"B6_alpha_{a}_nonintegrable_mass", "family": "B",
                      "hypothesis_violating": True, "alpha": a, **rec, "exception": exc,
                      "outcome": outcome,
                      "note": ("cos_power_mass raises for alpha <= 1, so the far-field "
                               "asymptote M_alpha/(pi X) has no referent -- a refusal, "
                               "which is the sound behaviour (discipline 73)")})

    # -- B7  quadratic_constant_upper's own window: is its argmax interior? -------------
    for a in (1.2, 1.5, 1.9):
        q = quadratic_constant_upper(a, LIVE_GAMMA, n_quad=401)
        wide = quadratic_constant_upper(a, LIVE_GAMMA, X_lo=1e-6, X_hi=1e12,
                                        n_X=240, n_quad=401)
        cases.append({"case": f"B7_CQ_window_a{a}", "family": "B",
                      "hypothesis_violating": False, "alpha": a,
                      "default_window": q["C_Q_sup_upper"], "default_argmax_X": q["argmax_X"],
                      "wide_window": wide["C_Q_sup_upper"], "wide_argmax_X": wide["argmax_X"],
                      "wide_over_default": wide["C_Q_sup_upper"] / q["C_Q_sup_upper"],
                      "outcome": ("false_bound"
                                  if wide["C_Q_sup_upper"] > q["C_Q_sup_upper"] * (1 + 1e-12)
                                  else "sound")})
    return cases


# ===========================================================================
# FAMILY C -- `two_point_dual` / `sup_part_upper` UNDER DEGENERATE WEIGHTS
# ===========================================================================


def family_C(m=6, seed=0):
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(1, m))
    q = np.abs(rng.normal(size=(m, m))) + 0.5
    q = 0.5 * (q + q.T)
    np.fill_diagonal(q, 0.0)
    v = np.abs(rng.normal(size=m)) + 0.5
    cand = np.arange(m)
    base = float(two_point_dual(C, v, q, cand)[0])
    cases = [{"case": "C00_control_wellformed", "family": "C", "hypothesis_violating": False,
              "bound": base, "outcome": "sound",
              "note": "the honest dual bound, against which every poison is measured"}]

    def _case(name, Cm, vm, qm, note):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                b = float(two_point_dual(Cm, vm, qm, cand)[0])
                exc = ""
                outcome = "false_bound" if (b < base * (1 - 1e-12)) else "sound"
                if not np.isfinite(b):
                    outcome = "sound"           # +inf/NaN is a refusal, not a fabrication
            except Exception as ex:                                     # noqa: BLE001
                b, exc, outcome = None, f"{type(ex).__name__}: {ex}", "raised"
        cases.append({"case": name, "family": "C", "hypothesis_violating": True,
                      "bound": b, "honest_bound": base,
                      "honest_over_reported": (base / b if (b and np.isfinite(b) and b > 0)
                                               else None),
                      "exception": exc, "outcome": outcome, "note": note})

    q_col = q.copy(); q_col[:, 2] = 0.0; q_col[2, :] = 0.0
    _case("C01_q_column_zeroed", C, v, q_col,
          "one reference index m0 with an all-zero seminorm column: every |c_m|/q term "
          "for that m0 is honestly +inf, and `1/q if q>0 else 0` makes them all zero, so "
          "that m0 wins the min at a price of |sum c|/v_m0 alone")
    q_neg = q.copy(); q_neg[:, 2] = -2.0; q_neg[2, :] = -2.0
    _case("C02_q_column_negative", C, v, q_neg,
          "the same mask catches NEGATIVE entries too -- q <= 0 is dropped, not flagged")
    q_one = q.copy(); q_one[3, 1] = q_one[1, 3] = 0.0
    _case("C03_q_single_offdiagonal_zero", C, v, q_one,
          "a single off-diagonal zero: dropped, but the min over m0 may already prefer "
          "another reference index, so the poison need not be load-bearing")
    v_neg = v.copy(); v_neg[2] = -v_neg[2]
    _case("C04_v_one_negative", C, v_neg, q,
          "a negative codomain sup weight makes the |sum c|/v_m0 term NEGATIVE, and the "
          "min over m0 selects it -- the claimed upper bound drops below the honest one")
    v_zero = v.copy(); v_zero[2] = 0.0
    _case("C05_v_one_zero", C, v_zero, q,
          "a zero weight divides to +inf, which the min discards -- a refusal, sound")
    v_nan = v.copy(); v_nan[2] = NAN
    _case("C06_v_one_nan", C, v_nan, q, "NaN propagates through min -- recorded, not a lie")
    _case("C07_C_has_nan", np.array([[NAN] + list(C[0, 1:])]), v, q,
          "NaN in the functional row propagates")

    # -- reachability: can HolderNorm, the module's own weight source, produce any of it?
    reach = []
    for J in (125, 250, 500):
        th, X = grid(J)
        for (a, g) in ((1.5, 0.5), (1.1, 0.15), (1.9, 0.9)):
            h = HolderNorm(th, X, a + 1.0, g)
            P = h.pair
            off = ~np.eye(P.shape[0], dtype=bool)
            reach.append({"J": J, "alpha": a, "gamma": g,
                          "min_offdiagonal_pair": float(P[off].min()),
                          "n_offdiagonal_nonpositive": int((P[off] <= 0).sum()),
                          "min_w": float(h.w.min()),
                          "n_w_nonpositive": int((h.w <= 0).sum())})
    return cases, reach


# ===========================================================================
# ASSEMBLY
# ===========================================================================


def _reference_validation():
    """The reference integrator against the sharp asymptote the module's docstring states.

    `_I_out -> M_alpha / X` far out, so `reference * X / M_alpha -> 1`.  Also records the
    reference's own Simpson convergence, so the sub-1e-4 calls in family B can be read as
    signal rather than as the reference's noise.
    """
    rows = []
    for a in (1.2, 1.5, 1.9):
        M = float(cos_power_mass(a))
        for X in (1e8, 1e10, 1e12, 1e14):
            r = _I_out_reference(X, a)
            rows.append({"alpha": a, "X": X, "M_alpha": M, "reference": r,
                         "reference_times_X_over_M": r * X / M})
    conv = []
    for a in (1.2, 1.9):
        for X in (1e11, 1e12):
            r8, r128 = _I_out_reference(X, a, n=8000), _I_out_reference(X, a, n=128000)
            conv.append({"alpha": a, "X": X, "n_8000": r8, "n_128000": r128,
                         "relative_difference": (r8 - r128) / r128})
    return {"asymptote": rows, "self_convergence": conv}


def _crossover_locator(alpha=1.9, lo=1e10, hi=1e13, n=61):
    """Where does `_I_out` stop dominating the truth, and why.

    The integrand's mass sits at y = O(1).  `_I_out` grades its bulk panel
    [0, X/2] logarithmically from `eps = 1e-12 * max(X, 1)`, so the first trapezoid panel
    [0, eps] replaces the resolved mass region the moment `eps` crosses y = 1 -- which is
    at EXACTLY X = 1e12.  This locates the measured crossover against that prediction
    instead of asserting it.
    """
    Xs = np.geomspace(lo, hi, n)
    rows = [{"X": float(X), "eps": 1e-12 * max(float(X), 1.0),
             "module": _I_out(X, alpha), "reference": _I_out_reference(X, alpha)}
            for X in Xs]
    for r in rows:
        r["reference_over_module"] = r["reference"] / r["module"]
    first_bad = next((r for r in rows if r["reference_over_module"] > 1.0), None)
    worst = max(rows, key=lambda r: r["reference_over_module"])
    return {"alpha": alpha, "predicted_crossover_X": 1e12,
            "predicted_mechanism": "eps = 1e-12 * X crosses the mass scale y = O(1)",
            "first_X_where_module_falls_below_truth": (first_bad["X"] if first_bad else None),
            "worst_reference_over_module": worst["reference_over_module"],
            "worst_at_X": worst["X"],
            "worst_under_report_percent": 100.0 * (worst["reference_over_module"] - 1.0),
            "live_range_max_X": LIVE_X_MAX,
            "decades_of_margin_from_live_range": (
                math.log10(first_bad["X"] / LIVE_X_MAX) if first_bad else None),
            "rows": rows}


def run(write=True, verbose=True):
    cases = family_P() + family_A() + family_B()
    cC, reach = family_C()
    cases += cC

    false_accepts = [c for c in cases if c["outcome"] == "false_accept"]
    false_bounds = [c for c in cases if c["outcome"] == "false_bound"]
    raised = [c for c in cases if c["outcome"] == "raised"]
    poisoned = [c for c in cases if c["hypothesis_violating"]]
    load_bearing = [c for c in cases if c.get("load_bearing")]
    degenerate = [c for c in cases if c.get("degenerate_ball")]
    # A PLANTED NON-SOLUTION SURVIVED when the module reported a certified ball centred on
    # it that contains NO zero of F -- the gate's question, decided rather than argued.
    survivors = [c for c in cases
                 if c["outcome"] == "false_accept" and c["family"] == "P"
                 and c["ball"]["contains_a_zero"] is False]

    data = {
        "leg": 116, "route": "NKA", "module": "solver/nk_bounds.py",
        "question": ("Does solver/nk_bounds.py ever report a certified ball that a planted "
                     "non-solution survives?"),
        "substrate_P": {"F": "x^2 - 2 on R", "zeros": [P_ROOT, -P_ROOT],
                        "good_centre": P_XBAR, "planted_point": P_XPLANT,
                        "residual_at_planted_point": abs(P_XPLANT ** 2 - 2.0),
                        "distance_to_nearest_zero": abs(P_ROOT - P_XPLANT),
                        "honest_constants_at_planted_point": _p_constants(P_XPLANT),
                        "honest_verdict_at_planted_point": budget(**_p_constants(P_XPLANT)),
                        "honest_constants_at_good_centre": _p_constants(P_XBAR),
                        "honest_verdict_at_good_centre": budget(**_p_constants(P_XBAR))},
        "live_operating_range": {
            "callers": ["experiments/p2_route_d_v6_bounds.py",
                        "experiments/p2_route_d_v8_quadratic.py",
                        "experiments/p2_route_d_v10_lower.py"],
            "alphas": list(LIVE_ALPHAS), "gamma": LIVE_GAMMA, "X0s": list(LIVE_X0S),
            "largest_X_evaluated": LIVE_X_MAX,
            "Y0_passed_by_every_in_repo_caller": 0.0},
        "reference_validation": _reference_validation(),
        "iout_crossover": _crossover_locator(),
        "holder_norm_reachability": reach,
        "totals": {"cases": len(cases), "hypothesis_violating": len(poisoned),
                   "false_accepts": len(false_accepts), "false_bounds": len(false_bounds),
                   "load_bearing": len(load_bearing),
                   "degenerate_balls": len(degenerate), "raised": len(raised)},
        "false_accept_cases": [c["case"] for c in false_accepts],
        "false_bound_cases": [c["case"] for c in false_bounds],
        "load_bearing_cases": [c["case"] for c in load_bearing],
        "degenerate_ball_cases": [c["case"] for c in degenerate],
        "raised_cases": [c["case"] for c in raised],
        "planted_point_survivor_cases": [c["case"] for c in survivors],
        "cases": cases,
    }

    if write:
        with open(os.path.abspath(OUT), "w") as fh:
            json.dump(data, fh, indent=2, default=float)

    if verbose:
        s = data["substrate_P"]
        print(f"substrate P: F(x)=x^2-2, zeros +-{P_ROOT:.6f}")
        print(f"  good centre  x={P_XBAR}: Y0={s['honest_constants_at_good_centre']['Y0']:.4e}"
              f" -> closes={s['honest_verdict_at_good_centre']['closes']}"
              f" r_min={s['honest_verdict_at_good_centre']['r_min']:.4e}")
        print(f"  planted pt   x={P_XPLANT}: Y0={s['honest_constants_at_planted_point']['Y0']:.4e}"
              f" -> closes={s['honest_verdict_at_planted_point']['closes']}"
              f"   |F|={s['residual_at_planted_point']:.4g}, "
              f"dist to nearest zero {s['distance_to_nearest_zero']:.6f}")
        print()
        for c in cases:
            extra = ""
            if c["family"] == "P" and c.get("ball", {}).get("ball_lo") is not None:
                b = c["ball"]
                gr = b["gap_in_ball_radii"]
                gr_s = "n/a" if gr is None else f"{gr:.3f}"
                extra = (f"  ball=[{b['ball_lo']:.4f},{b['ball_hi']:.4f}] "
                         f"has_zero={b['contains_a_zero']} miss={gr_s} radii")
            if c["family"] == "B" and "reference_over_module" in c:
                extra = f"  ref/module={c['reference_over_module']:.6g}"
            if c["family"] == "C" and c.get("honest_over_reported"):
                extra = f"  honest/reported={c['honest_over_reported']:.4g}"
            lb = "  <-- LOAD-BEARING" if c.get("load_bearing") else ""
            print(f"  {c['case']:34s} {c['outcome']:13s}{extra}{lb}")
        print()
        t = data["totals"]
        print(f"FALSE ACCEPTS: {t['false_accepts']}/{t['hypothesis_violating']} "
              f"hypothesis-violating inputs reported a CLOSING certificate "
              f"({t['load_bearing']} load-bearing, {t['degenerate_balls']} of them a "
              f"degenerate/empty 'ball')")
        print(f"FALSE BOUNDS : {t['false_bounds']} claimed UPPER bounds fell BELOW the "
              f"independent reference")
        print(f"RAISED       : {t['raised']}")
        x = data["iout_crossover"]
        print(f"_I_out crossover: module first falls below the truth at X="
              f"{x['first_X_where_module_falls_below_truth']:.3e} (predicted 1e12 from "
              f"eps=1e-12*X crossing y=O(1)); worst under-report "
              f"{x['worst_under_report_percent']:.3f}% at X={x['worst_at_X']:.3e}; "
              f"the live range tops out at X={LIVE_X_MAX:.3e}, "
              f"{x['decades_of_margin_from_live_range']:.2f} decades below it")
        if data["planted_point_survivor_cases"]:
            print("PLANTED NON-SOLUTION SURVIVED IN: "
                  + ", ".join(data["planted_point_survivor_cases"]))
        if write:
            print(f"\nwrote {os.path.abspath(OUT)}")
    return data


if __name__ == "__main__":
    run()
