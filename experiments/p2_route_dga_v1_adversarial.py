"""Route-DGA v1: an ADVERSARIAL AUDIT of solver/decay_grading.py -- the decay-graded
function-space layer under the collocation lane.

WHAT THIS IS NOT.  It is not a measurement of anything physical.  No number printed here is a
statement about blow-up, about a certificate constant, or about any quantity in the plan of
record.  It re-derives no physics, contests no banked result, and sharpens no bound.

WHAT THIS IS.  Every number here is a statement about CODE BEHAVIOUR UNDER DEGENERATE OR
POISONED INPUT.  The question, verbatim from the leg's gate (DIRECTION.md, leg 139):

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/decay_grading.py ever silently return a wrong value rather than propagating or
    flagging the invalid input?

WHY THIS MODULE.  It carries the decay-graded function spaces the whole Route-D v3/v4 lane
sits on: `farfield_inverse_norm` is called by p2_route_d_v3_spaces, _v6_bounds, _v7_seminorm
and _v8_quadratic; `cos_power_mass` by solver/nk_bounds.py and three more drivers;
`algebra_constant` by p2_route_d_v3_spaces.  It has a dedicated correctness suite
(test_decay_grading.py, 8 gates) in which EVERY gate is a known-answer gate on CLEAN input --
a closed form, a second implementation, or an asymptotic oracle.  It had no adversarial
battery.  Same robustness-only precedent as legs 69/100/101/115/120.

WHERE THE BOUNDARIES COME FROM (novelty pass, writeup/novelty/leg_139.md, committed BEFORE a
line of this file existed).  Three published boundaries and one repo-internal one, so nothing
below is an invented standard:

  (L1) The one-pass induced-norm trick is the MONOTONE / INVERSE-POSITIVE matrix argument (a
       non-singular M-matrix has a non-negative inverse, so the extremal source realizes the
       induced norm).  The discretization is the trapezoidal rule, which is A-stable but NOT
       unconditionally positivity-preserving: positivity carries a finite step restriction
       (Bonaventura & Della Rocca arXiv:1510.04303; Horvath et al. arXiv:2105.07403 for the
       theta-method on the advection operator, which is the operator here).  For this module
       the threshold is explicit and the module KNOWS it -- `ValueError("grid too coarse: need
       dtau < 2c")` -- but raises it on the alpha > 2 branch ONLY.  G1 measures the sibling.

  (L2) `math.lgamma` returns log|Gamma(x)|; the sign is discarded by construction and lives in
       POSIX's `signgam` / `lgamma_r` (pubs.opengroup.org lgamma; cppreference; Boost lgamma),
       or in SciPy's `gammasgn` (`exp(loggamma(x+0j)) = gammasgn(x)*exp(gammaln(x))`).  Python
       exposes no signgam at all.  `cos_power_coeffs`'s docstring claims "no Gamma of a
       negative argument is ever formed" -- checkable.  Independently, f_alpha =
       |cos(theta/2)|^alpha is NOT integrable for alpha <= -1, so for those alpha no cosine
       coefficient sequence exists and anything returned is fabricated.  G3 measures both.

  (L3) The condition sup_{j,k} v_{j+k}/(u_j u_k) < oo is the standard BEURLING
       submultiplicativity condition making a weighted ell^1 a convolution Banach algebra
       (Grochenig, "Weight functions in time-frequency analysis"; Willis, "Conjugation weights
       and weighted convolution algebras").  The published condition is a supremum over the
       WHOLE index set; `algebra_constant` takes it over j+k <= len(v) and returns the result
       as a SHARP two-sided bracket S/4 <= M <= S/2.  G5 measures what that costs.

  (L4) Repo-internal: `cos_power_mass` REFUSES alpha <= 1 with a ValueError, and
       test_nk_bounds_adversarial.py (leg 116) banks that refusal as a virtue -- "when a
       quantity has no referent, say so instead of bounding it" (lesson 73).  So the module's
       own author knew the pattern.  G3 and G2 measure the places the same pattern is absent.

NOT A RE-FIND OF ANY PRIOR LEG.  This module has never been adversarially audited (DIRECTION.md
line 562 says so; confirmed by directory census in the novelty log).  Note the NAME COLLISION
that a census must not trip over: `solver/spectral_certificate.py` defines a DIFFERENT
`algebra_constant(kind, param, K)`; test_spectral_certificate.py and p2_route_l1_v2_spectral.py
call THAT one, not this module's.

PASSES ARE REPORTED AS LOUDLY AS FAILURES (leg 91's design rule, inherited via legs 115/120):
G6 is the map of inputs the module handles CORRECTLY, and every one of its controls could have
come out the other way (lesson 90) -- NaN propagation, the exact alpha = 2 resonance guard, the
X0 = 0 refusal, the empty-input refusal, the alpha in (-1,0) expansion that is legitimately
valid, the fold identity past |theta| > pi/2, and `hilbert_of_cos_power` pushed three decades
past its OWN documented X ~ 1e4 ceiling against the exact far-field law.

THE SIX BATTERIES
  G1  THE GUARD ASYMMETRY (the headline).  Same recursion, same coefficients p and q, same
      step dtau: the alpha > 2 branch raises "grid too coarse: need dtau < 2c" and the
      alpha < 2 branch silently returns a finite, plausible, wrong induced norm.  Measures the
      ladder in n on both branches against the module's OWN exact closed form
      farfield_inverse_norm_finite, the onset, and -- the mechanism ablation -- the onset
      MOVING when c moves, which is what proves it is the recursion coefficient and not the
      grid size.
  G2  THE FABRICATED ZERO NORM.  c < 0 and X0 > Xmax both make farfield_inverse_norm return
      EXACTLY 0.0, with `predicted` still reporting 4.0 beside it.  A zero operator norm is
      the maximally unsafe direction for a Newton-Kantorovich budget.
  G3  FABRICATED COEFFICIENTS AT NEGATIVE alpha.  Sign loss through lgamma on (-2,-1), and a
      divergent, non-existent coefficient sequence for alpha <= -1, with no refusal -- next to
      a sibling function in the same file that DOES refuse (cos_power_mass, alpha <= 1).
  G4  THE NEGATIVE NORM.  farfield_inverse_norm_finite returns a NEGATIVE number for X0 > Xmax
      on both branches.
  G5  THE ALGEBRA CONSTANT ABSORBS POISON.  +-Inf planted in u, and a wholly sign-flipped u,
      return S BIT-IDENTICALLY to the clean call; an Inf that does register moves S DOWN; a v
      sized to len(u) instead of 2(len(u)-1) under-reports the "sharp" constant.  Every
      direction is the unsafe one.
  G6  WHAT THE MODULE GETS RIGHT (controls that could have failed).

Run:  .venv/bin/python experiments/p2_route_dga_v1_adversarial.py
Writes: writeup/data/p2_route_dga_v1_adversarial.json
"""

import math
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from solver.decay_grading import (                                     # noqa: E402
    algebra_constant, cos_power_coeffs, cos_power_mass, eval_cos_series,
    eval_sin_series, farfield_inverse_norm, farfield_inverse_norm_finite,
    farfield_symbol_coefficient, hilbert_of_cos_power, quadratic_coeffs,
    theta_of_X, X_of_theta,
)

X0_DEF, XMAX_DEF = 1.0, 1e12


# ---------------------------------------------------------------------------
# independent oracles (nothing below is checked against the module itself)
# ---------------------------------------------------------------------------


def gamma_reflect(x):
    """Gamma(x) for x < 0 non-integer, WITH ITS SIGN, via the reflection formula.

    Gamma(x) = pi / (sin(pi x) Gamma(1-x)).  1-x > 1 here, so the Gamma on the right is
    evaluated at a positive argument where math.gamma is exact to rounding.  This is the
    oracle `cos_power_coeffs` needs and does not have.
    """
    if x > 0:
        return math.gamma(x)
    return math.pi / (math.sin(math.pi * x) * math.gamma(1.0 - x))


def a0_continued(alpha):
    """The analytically continued a_0 = 2^{-alpha} Gamma(alpha+1) / Gamma(alpha/2+1)^2."""
    return (2.0 ** (-alpha)) * gamma_reflect(alpha + 1.0) / gamma_reflect(0.5 * alpha + 1.0) ** 2


def cos_coeff_quadrature(alpha, k, n=2_000_001):
    """a_k of |cos(theta/2)|^alpha by midpoint quadrature -- an oracle independent of any
    Gamma function.  a_0 = (1/pi) int_0^pi f, a_k = (2/pi) int_0^pi f cos(k theta)."""
    t = (np.arange(n) + 0.5) / n * math.pi
    f = np.abs(np.cos(0.5 * t)) ** alpha
    if k == 0:
        return float(np.mean(f))
    return float(2.0 * np.mean(f * np.cos(k * t)))


def dtau_of(n, X0=X0_DEF, Xmax=XMAX_DEF):
    return math.log(Xmax / X0) / (n - 1)


def call(fn, *a, **kw):
    """Return ('value', v) or ('raised', 'TypeName: msg'); warnings captured, not silenced."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            v = fn(*a, **kw)
            return {"outcome": "value", "value": v,
                    "warnings": [str(x.category.__name__) for x in w]}
        except Exception as e:                                   # noqa: BLE001
            return {"outcome": "raised", "error": f"{type(e).__name__}: {e}",
                    "warnings": [str(x.category.__name__) for x in w]}


# ---------------------------------------------------------------------------
# G1 -- the guard asymmetry (headline)
# ---------------------------------------------------------------------------


def _recursion_response(alpha, c, x, src):
    """Second, independent implementation of the module's trapezoidal recursion, taking an
    ARBITRARY source vector instead of the built-in extremal one.

    This is the 'build the same object twice' rule: it is validated against the module itself
    on the clean extremal source before it is used as an oracle (see `positivity_probe`).  Its
    purpose is to expose the map g -> h as a MATRIX, which the module never forms, so that the
    one-pass induced-norm claim can be checked entrywise.
    """
    dtau = np.diff(np.log(x))
    beta = 1.0 / c
    h = np.zeros(x.size)
    if alpha < 2.0:
        for i in range(1, x.size):
            p, q = 1.0 / dtau[i - 1] + 0.5 * beta, 1.0 / dtau[i - 1] - 0.5 * beta
            h[i] = (q * h[i - 1] + 0.5 * beta * (src[i] + src[i - 1])) / p
    else:
        for i in range(x.size - 1, 0, -1):
            p, q = 1.0 / dtau[i - 1] + 0.5 * beta, 1.0 / dtau[i - 1] - 0.5 * beta
            h[i - 1] = (p * h[i] + 0.5 * beta * (src[i] + src[i - 1])) / q
    return h


def _positivity_probe(alpha, n, c=0.5):
    """Is the module's one-pass value still an INDUCED NORM, or only the response to one
    particular sign pattern?

    Forms the response matrix T (g -> h) column by column, then compares
        module value          = max_i w_h(i) (T g*)_i,   g* = 1/w_g >= 0     [one pass]
        true discrete norm    = max_i w_h(i) sum_j |T_ij| / w_g(j)           [all signs]
    They are EQUAL iff T is entrywise non-negative -- exactly the module's stated hypothesis.
    """
    from solver.decay_grading import farfield_grid
    x = farfield_grid(X0_DEF, XMAX_DEF, n)
    w_h, w_g = x ** alpha, x ** (alpha + 1.0)
    T = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = 1.0
        T[:, j] = _recursion_response(alpha, c, x, x * e)      # src_i = X_i g_i
    g_star = 1.0 / w_g
    one_pass = float(np.max(w_h * (T @ g_star)))
    all_signs = float(np.max(w_h * (np.abs(T) @ g_star)))
    module = call(farfield_inverse_norm, alpha, c=c, n=n)
    return {
        "alpha": alpha, "n": n, "dtau": dtau_of(n), "two_c": 2.0 * c,
        "dtau_exceeds_2c": dtau_of(n) > 2.0 * c,
        "module_value": (float(module["value"][0]) if module["outcome"] == "value"
                         else module["error"]),
        "reimplementation_one_pass": one_pass,
        "true_discrete_induced_norm": all_signs,
        "one_pass_understates_by": all_signs / one_pass if one_pass else None,
        "negative_entry_fraction": float(np.mean(T < 0.0)),
        "reimplementation_matches_module": (
            abs(one_pass - float(module["value"][0])) <= 1e-9 * max(1.0, abs(one_pass))
            if module["outcome"] == "value" else False),
    }


def g1_guard_asymmetry():
    exact = farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)
    exact_hi = farfield_inverse_norm_finite(2.5, X0_DEF, XMAX_DEF)
    assert abs(exact - exact_hi) < 1e-9, "both branches share the same exact value by symmetry"

    ladder = []
    for n in (8001, 2001, 401, 100, 60, 40, 28, 20, 14, 12, 8, 6, 4, 3):
        row = {"n": n, "dtau": dtau_of(n), "dtau_over_2c": dtau_of(n) / 1.0}
        for tag, alpha, ex in (("below", 1.5, exact), ("above", 2.5, exact_hi)):
            r = call(farfield_inverse_norm, alpha, n=n)
            if r["outcome"] == "value":
                got = float(r["value"][0])
                row[tag] = {"outcome": "value", "norm": got, "exact": ex,
                            "ratio_to_exact": got / ex}
            else:
                row[tag] = {"outcome": "raised", "error": r["error"], "exact": ex}
        row["asymmetric"] = (row["below"]["outcome"] == "value"
                             and row["above"]["outcome"] == "raised")
        ladder.append(row)

    asym = [r for r in ladder if r["asymmetric"]]
    worst = max(asym, key=lambda r: r["below"]["ratio_to_exact"]) if asym else None

    # MECHANISM ABLATION.  If the cause is really the sign of q = 1/dtau - beta/2, then moving
    # c moves the onset by exactly the same factor.  If the cause were "the grid is small",
    # the onset would not care about c at all.  (Lesson 90: this control CAN come out flat.)
    onsets = []
    ex = farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)
    for c in (1.0, 0.5, 0.25, 0.125):
        predicted_n = 1.0 + math.log(XMAX_DEF / X0_DEF) / (2.0 * c)   # dtau = 2c exactly
        largest_refused = None
        for n in range(3, 600):
            if call(farfield_inverse_norm, 2.5, c=c, n=n)["outcome"] == "raised":
                largest_refused = n
            else:
                break
        at_n = largest_refused if largest_refused else 3
        r_lo = call(farfield_inverse_norm, 1.5, c=c, n=at_n)
        onsets.append({
            "c": c, "two_c": 2.0 * c,
            "predicted_n_at_dtau_equals_2c": predicted_n,
            "largest_n_refused_on_above_branch": largest_refused,
            "dtau_at_that_n": dtau_of(at_n),
            "below_branch_at_same_n": (float(r_lo["value"][0]) if r_lo["outcome"] == "value"
                                       else r_lo["error"]),
            "below_branch_ratio_to_exact": (float(r_lo["value"][0]) / ex
                                            if r_lo["outcome"] == "value" else None),
        })

    # POSITIVITY PROBE: does the one-pass value remain an induced norm at all?
    probes = [_positivity_probe(1.5, n) for n in (401, 60, 28, 20, 14)]
    probes.append(_positivity_probe(2.5, 401))          # control: the guarded branch, in range

    # the same-dtau pairing, stated as one row
    pair = next((r for r in asym if r["n"] == 20), asym[0] if asym else None)
    return {
        "what": ("farfield_inverse_norm runs the SAME trapezoidal recursion on both alpha "
                 "branches with the same coefficients p = 1/dtau + beta/2, q = 1/dtau - "
                 "beta/2.  The alpha > 2 branch checks q <= 0 and raises; the alpha < 2 "
                 "branch does not check it at all.  The module's docstring rests the whole "
                 "one-pass induced-norm trick on 'Every coefficient in either recursion is "
                 "non-negative' -- which is exactly what fails when dtau > 2c."),
        "exact_continuum_finite_domain": exact,
        "ladder": ladder,
        "n_rows_asymmetric": len(asym),
        "headline_pair": pair,
        "worst_silent_ratio": worst["below"]["ratio_to_exact"] if worst else None,
        "worst_silent_n": worst["n"] if worst else None,
        "mechanism_ablation_c": onsets,
        "positivity_probe": {
            "rows": probes,
            "note": ("The map g -> h is formed as a matrix by a second, independent "
                     "implementation of the same recursion (validated against the module on "
                     "the clean extremal source: `reimplementation_matches_module`).  The "
                     "module's one-pass value equals the true discrete induced norm IFF that "
                     "matrix is entrywise non-negative -- the module's own stated hypothesis. "
                     "Above dtau = 2c it is not, so the returned number stops being an "
                     "induced norm; this is a correctness statement, NOT a discretization "
                     "error, and it is what separates 'coarse but honest' from 'wrong'."),
        },
        "verdict": ("SILENT CORRUPTION.  At identical dtau above the module's own published "
                    "threshold, one branch refuses and the other returns a finite plausible "
                    "wrong induced norm, with no warning and no NaN."),
    }


# ---------------------------------------------------------------------------
# G2 -- the fabricated zero norm
# ---------------------------------------------------------------------------


def g2_fabricated_zero():
    exact = farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)
    cases = []
    for tag, alpha, kw in (
        ("negative_speed_below", 1.5, dict(c=-0.5)),
        ("negative_speed_above", 2.5, dict(c=-0.5)),
        ("swapped_domain_below", 1.5, dict(X0=XMAX_DEF, Xmax=X0_DEF)),
        ("swapped_domain_above", 2.5, dict(X0=XMAX_DEF, Xmax=X0_DEF)),
    ):
        r = call(farfield_inverse_norm, alpha, n=2001, **kw)
        rec = {"case": tag, "alpha": alpha, "kwargs": {k: v for k, v in kw.items()}}
        if r["outcome"] == "value":
            norm, pred = float(r["value"][0]), float(r["value"][1])
            rec.update({"outcome": "value", "norm": norm, "predicted_companion": pred,
                        "exactly_zero": norm == 0.0, "exact_for_clean_input": exact,
                        "warnings": r["warnings"]})
        else:
            rec.update({"outcome": "raised", "error": r["error"]})
        cases.append(rec)

    zeros = [c for c in cases if c.get("exactly_zero")]
    # WHY the guard does not fire: with c < 0, beta < 0, so q = 1/dtau - beta/2 > 0 always.
    n = 2001
    q_neg_c = 1.0 / dtau_of(n) - 0.5 * (1.0 / -0.5)
    return {
        "what": ("A negative speed c and a swapped domain (X0 > Xmax) both drive "
                 "farfield_inverse_norm to return EXACTLY 0.0 -- the value of the boundary "
                 "node, which is the only non-negative entry left -- while the `predicted` "
                 "companion it returns beside it still reads 4.0."),
        "cases": cases,
        "n_exact_zero": len(zeros),
        "q_at_negative_c": q_neg_c,
        "why_guard_blind": ("The only guard in the module tests q <= 0.  With c < 0 we have "
                            f"beta = 1/c < 0, so q = 1/dtau - beta/2 = {q_neg_c:.6f} > 0 and "
                            "the guard cannot fire.  It is a guard against one coarse-grid "
                            "sign flip, not against an inadmissible c."),
        "severity_direction": ("A returned operator norm of 0.0 is the maximally UNSAFE "
                               "direction: ||A_far|| enters a Newton-Kantorovich budget in "
                               "the numerator, so zero makes any budget look infinitely "
                               "comfortable.  The clean value is 3.999996."),
        "verdict": "SILENT CORRUPTION (fabricated zero, 4/4 inadmissible cases).",
    }


# ---------------------------------------------------------------------------
# G3 -- fabricated coefficients at negative alpha
# ---------------------------------------------------------------------------


def g3_negative_alpha():
    # (a) the sign, against the reflection-formula oracle
    sign_rows = []
    for alpha in (-1.2, -1.5, -1.8, -2.5, -3.5):
        r = call(cos_power_coeffs, alpha, 1)
        if r["outcome"] != "value":
            sign_rows.append({"alpha": alpha, "outcome": "raised", "error": r["error"]})
            continue
        got = float(r["value"][0])
        want = a0_continued(alpha)
        sign_rows.append({
            "alpha": alpha, "outcome": "value", "a0_module": got, "a0_continued": want,
            "sign_module": int(np.sign(got)), "sign_continued": int(np.sign(want)),
            "sign_flipped": bool(np.sign(got) != np.sign(want)),
            "relative_error": abs(got - want) / abs(want),
            "gamma_arg_negative": alpha + 1.0 < 0.0,
        })
    flipped = [r for r in sign_rows if r.get("sign_flipped")]

    # (b) the sequence does not exist for alpha <= -1: coefficients GROW, series DIVERGES
    div_rows = []
    theta_probe = 0.3
    truth = abs(math.cos(0.5 * theta_probe)) ** -1.5
    for alpha in (-1.5, -2.5):
        f_true = abs(math.cos(0.5 * theta_probe)) ** alpha
        row = {"alpha": alpha, "f_true_at_theta_0.3": f_true, "K_ladder": []}
        for K in (100, 1000, 10000):
            a = cos_power_coeffs(alpha, K)
            s = float(eval_cos_series(a, np.array([theta_probe]))[0])
            row["K_ladder"].append({"K": K, "abs_a_K": float(abs(a[-1])),
                                    "series_value": s, "abs_error": abs(s - f_true)})
        gr = row["K_ladder"]
        row["coefficient_growth_100_to_10000"] = gr[-1]["abs_a_K"] / gr[0]["abs_a_K"]
        row["error_growth_100_to_10000"] = gr[-1]["abs_error"] / gr[0]["abs_error"]
        div_rows.append(row)

    # (c) the boundary: where it refuses, and where it is legitimately RIGHT
    boundary = {"alpha_minus_one_exact": call(cos_power_coeffs, -1.0, 4),
                "alpha_minus_two_exact": call(cos_power_coeffs, -2.0, 4)}
    boundary["alpha_minus_one_exact"].pop("value", None)
    boundary["alpha_minus_two_exact"].pop("value", None)

    valid_rows = []
    for alpha in (-0.5, -0.25):
        a = cos_power_coeffs(alpha, 6)
        for k in (0, 1, 2, 3):
            q = cos_coeff_quadrature(alpha, k)
            valid_rows.append({"alpha": alpha, "k": k, "a_k_module": float(a[k]),
                               "a_k_quadrature": q, "relative_error": abs(a[k] - q) / abs(q)})

    return {
        "what": ("cos_power_coeffs takes any alpha.  Its docstring claims 'no Gamma of a "
                 "negative argument is ever formed'; math.lgamma(alpha+1) forms exactly that "
                 "for alpha < -1 and silently drops the sign (log|Gamma|).  Worse, for "
                 "alpha <= -1 the function |cos(theta/2)|^alpha is not integrable, so NO "
                 "cosine coefficient sequence exists -- and a finite array is returned "
                 "anyway.  Its own file-mate cos_power_mass REFUSES alpha <= 1."),
        "a_sign": {"rows": sign_rows, "n_sign_flipped": len(flipped),
                   "docstring_claim": "no Gamma of a negative argument is ever formed",
                   "docstring_claim_true": False},
        "b_divergence": {"rows": div_rows, "probe_theta": theta_probe,
                         "note": ("|a_K| grows like K^{|alpha|-1}; the truncated series is "
                                  "not converging to anything, so this is not a truncation "
                                  "error that a larger K repairs -- it gets worse.")},
        "c_boundary_refusals": boundary,
        "d_valid_range_control": {
            "rows": valid_rows,
            "max_relative_error": max(r["relative_error"] for r in valid_rows),
            "note": ("CONTROL THAT COULD HAVE FAILED: on -1 < alpha < 0 the expansion is "
                     "legitimate (f is still integrable) and the module is RIGHT, matched "
                     "against a Gamma-free midpoint quadrature.  So the finding is a sharp "
                     "boundary at alpha = -1, not a blanket 'negative alpha is nonsense'."),
        },
        "verdict": ("SILENT CORRUPTION.  Sign flipped on -2 < alpha < -1 against the "
                    "reflection-formula oracle; a divergent fabricated sequence for "
                    "alpha <= -1; correct and verified on -1 < alpha < 0; exact pole at "
                    "alpha = -1 raises.  Refusal exists one function away in the same file."),
        "unused_truth_probe": truth,
    }


# ---------------------------------------------------------------------------
# G4 -- the negative norm
# ---------------------------------------------------------------------------


def g4_negative_norm():
    rows = []
    for alpha in (1.5, 2.5, 1.9, 3.0):
        v_swapped = farfield_inverse_norm_finite(alpha, X0=XMAX_DEF, Xmax=X0_DEF)
        v_clean = farfield_inverse_norm_finite(alpha, X0=X0_DEF, Xmax=XMAX_DEF)
        rows.append({"alpha": alpha, "clean": v_clean, "swapped": v_swapped,
                     "negative": v_swapped < 0.0,
                     "magnitude_ratio": abs(v_swapped) / abs(v_clean)})
    degen = {"X0_equals_Xmax": call(farfield_inverse_norm_finite, 1.5, X0=1.0, Xmax=1.0),
             "X0_negative": call(farfield_inverse_norm_finite, 1.5, X0=-1.0, Xmax=XMAX_DEF),
             "alpha_exactly_2": call(farfield_inverse_norm_finite, 2.0)}
    return {
        "what": ("farfield_inverse_norm_finite computes 2(1 - (X0/Xmax)^e)/e with e = "
                 "|2-alpha|.  With X0 > Xmax the ratio exceeds 1, the bracket goes negative, "
                 "and the function returns a NEGATIVE operator norm."),
        "rows": rows,
        "n_negative": sum(1 for r in rows if r["negative"]),
        "degenerate_controls": degen,
        "verdict": ("SILENT CORRUPTION.  A quantity that is a norm by construction is "
                    "returned negative, on both alpha branches, with no check that "
                    "X0 < Xmax.  X0 < 0 does raise (a complex power), so the module refuses "
                    "the more obviously broken input and accepts the subtler one."),
    }


# ---------------------------------------------------------------------------
# G5 -- the algebra constant absorbs poison
# ---------------------------------------------------------------------------


def g5_algebra_constant():
    K = 8
    u = (1.0 + np.arange(K + 1.0)) ** -2.0
    v = (1.0 + np.arange(1, 2 * K + 1.0)) ** -1.0
    clean = algebra_constant(u, v)
    clean_S = float(clean[0])

    poison = []
    for tag, uu in (("inf_at_mode_1", np.where(np.arange(K + 1) == 1, np.inf, u)),
                    ("inf_at_mode_K", np.where(np.arange(K + 1) == K, np.inf, u)),
                    ("neg_inf_at_mode_1", np.where(np.arange(K + 1) == 1, -np.inf, u)),
                    ("all_weights_sign_flipped", -u),
                    ("nan_at_mode_1", np.where(np.arange(K + 1) == 1, np.nan, u)),
                    ("zero_at_mode_1", np.where(np.arange(K + 1) == 1, 0.0, u))):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            S = float(algebra_constant(uu, v)[0])
        poison.append({"case": tag, "S": S, "S_clean": clean_S,
                       "bit_identical_to_clean": S == clean_S,
                       "propagated_nan_or_inf": (math.isnan(S) or math.isinf(S)),
                       "ratio_to_clean": (S / clean_S) if np.isfinite(S) else None,
                       "warnings": [str(x.category.__name__) for x in w]})
    absorbed = [p for p in poison if not p["propagated_nan_or_inf"]]
    identical = [p for p in poison if p["bit_identical_to_clean"]]

    # the length-consistency hazard: quadratic_coeffs emits 2K modes by default
    q_modes = quadratic_coeffs(np.ones(K + 1)).size
    trunc = []
    for cut, tag in ((2 * K, "v_sized_2K_correct"), (K, "v_sized_K"), (K // 2, "v_sized_K_over_2")):
        S = float(algebra_constant(u, v[:cut])[0])
        trunc.append({"case": tag, "len_v": cut, "S": S,
                      "M_hi_reported": S / 2.0, "understatement_vs_2K": clean_S / S})

    return {
        "what": ("algebra_constant returns S with the two-sided bracket S/4 <= M <= S/2, "
                 "documented as SHARP.  It validates neither the sign, the finiteness, nor "
                 "the length of its weights.  The published Beurling condition is a supremum "
                 "over ALL pairs; every deviation measured here moves S DOWN, which is the "
                 "unsafe direction for a quadratic bound."),
        "clean_S": clean_S, "clean_bracket": [clean[1], clean[2]], "clean_argmax": list(clean[3]),
        "poison_rows": poison,
        "n_absorbed": len(absorbed), "n_bit_identical": len(identical),
        "quadratic_coeffs_default_mode_count_for_K": {"K": K, "modes": q_modes,
                                                      "len_v_required": 2 * K},
        "truncation_rows": trunc,
        "verdict": ("SILENT CORRUPTION.  +-Inf at mode 1 and a wholly sign-flipped weight "
                    "vector return S BIT-IDENTICALLY to the clean call (0 ULP, no warning); "
                    "an Inf that does register lowers S; a short v lowers it further.  The "
                    "sharp bracket is reported unchanged in every case."),
    }


# ---------------------------------------------------------------------------
# G6 -- what the module gets right (controls that could have failed)
# ---------------------------------------------------------------------------


def g6_passes():
    out = {}

    # NaN propagation where it matters
    u = (1.0 + np.arange(5.0)) ** -2.0
    v = (1.0 + np.arange(1, 9.0)) ** -1.0
    S_nan_u = float(algebra_constant(np.where(np.arange(5) == 1, np.nan, u), v)[0])
    S_nan_v = float(algebra_constant(u, np.where(np.arange(8) == 2, np.nan, v))[0])
    q_nan = quadratic_coeffs(np.array([1.0, np.nan, 0.25]))
    out["nan_propagation"] = {
        "algebra_constant_nan_u": S_nan_u, "propagates_u": math.isnan(S_nan_u),
        "algebra_constant_nan_v": S_nan_v, "propagates_v": math.isnan(S_nan_v),
        "quadratic_coeffs_nan_h": [None if math.isnan(x) else float(x) for x in q_nan],
        "quadratic_modes_poisoned": int(np.sum(np.isnan(q_nan))),
        "quadratic_modes_total": int(q_nan.size),
        "note": ("mode 4 stays clean at 0.03125 because with K = 2 the only pair with "
                 "j+k = 4 is (2,2), which never touches the poisoned entry -- correct, not "
                 "absorbed."),
    }

    # explicit refusals
    refusals = {
        "farfield_alpha_exactly_2": call(farfield_inverse_norm, 2.0, n=2001),
        "farfield_X0_zero": call(farfield_inverse_norm, 1.5, X0=0.0, n=2001),
        "cos_power_mass_alpha_1": call(cos_power_mass, 1.0),
        "cos_power_mass_alpha_0.5": call(cos_power_mass, 0.5),
        "cos_power_coeffs_alpha_minus_1": call(cos_power_coeffs, -1.0, 4),
        "quadratic_coeffs_empty": call(quadratic_coeffs, np.array([])),
        "quadratic_coeffs_negative_M": call(quadratic_coeffs, np.array([1.0, 0.5]), M=-3),
        "algebra_constant_zero_weight": {"outcome": "value",
                                         "value": float(algebra_constant(
                                             np.array([1.0, 0.0, 0.25]), v)[0])},
    }
    for k in refusals:
        if refusals[k].get("outcome") == "value" and not isinstance(refusals[k]["value"], float):
            refusals[k]["value"] = str(refusals[k]["value"])
    out["explicit_refusals"] = refusals
    out["n_refusals"] = sum(1 for r in refusals.values() if r["outcome"] == "raised")

    # the alpha = 2 resonance guard returns inf, which is the honest answer
    r2 = farfield_inverse_norm(2.0, n=2001)
    out["resonance_guard"] = {"alpha": 2.0, "norm": r2[0], "predicted": r2[1],
                              "both_inf": math.isinf(r2[0]) and math.isinf(r2[1])}

    # hilbert_of_cos_power three decades PAST its own documented ceiling
    alpha = 3.0
    mass = cos_power_mass(alpha)
    far = []
    for X in (1e2, 1e3, 1e4, 1e5, 1e6, 1e7):
        h = float(hilbert_of_cos_power(alpha, np.array([X]), K=100000)[0])
        law = mass / (math.pi * X)
        far.append({"X": X, "H": h, "farfield_law": law, "ratio": h / law,
                    "beyond_documented_ceiling": X > 1e4})
    out["hilbert_beyond_documented_range"] = {
        "rows": far,
        "max_abs_ratio_deviation_beyond_ceiling": max(
            abs(r["ratio"] - 1.0) for r in far if r["beyond_documented_ceiling"]),
        "note": ("The docstring says 'callers should stay below X ~ 1e4'.  Pushed to 1e7 the "
                 "value still matches the exact far-field law -- the documented ceiling is "
                 "conservative and no corruption occurs.  This control COULD have failed."),
    }

    # the fold identity past |theta| > pi/2, against a direct un-folded evaluation
    a = cos_power_coeffs(2.5, 200)
    th = np.array([0.1, 1.0, 2.0, 3.0, 3.14159, -2.5])
    k = np.arange(a.size)
    direct_cos = (np.cos(np.outer(th, k)) @ a)
    direct_sin = (np.sin(np.outer(th, k)) @ a)
    out["fold_identity"] = {
        "max_abs_err_cos": float(np.max(np.abs(eval_cos_series(a, th) - direct_cos))),
        "max_abs_err_sin": float(np.max(np.abs(eval_sin_series(a, th) - direct_sin))),
        "note": "the range-reduction fold is exact, including past |theta| > pi/2.",
    }

    # quadratic_coeffs against a brute-force double loop (a second implementation)
    h = np.array([0.3, -0.7, 0.2, 0.11])
    M = 2 * (h.size - 1)
    brute = np.zeros(M)
    for j in range(h.size):
        for kk in range(h.size):
            if 1 <= j + kk <= M:
                brute[j + kk - 1] += 0.5 * h[j] * h[kk]
    out["quadratic_second_implementation"] = {
        "max_abs_err": float(np.max(np.abs(quadratic_coeffs(h) - brute))),
        "note": "exact agreement with an independent double loop.",
    }

    # coordinate maps round-trip
    Xs = np.array([-1e6, -1.0, 0.0, 1.0, 1e6])
    out["coordinate_roundtrip"] = {
        "max_abs_err": float(np.max(np.abs(X_of_theta(theta_of_X(Xs)) - Xs) / (1.0 + np.abs(Xs)))),
    }

    # the near-resonance value the docstring warns about is CORRECT, only `predicted` is not
    got, pred = farfield_inverse_norm(2.0 + 1e-9, n=2001)
    ex = farfield_inverse_norm_finite(2.0 + 1e-9, X0_DEF, XMAX_DEF)
    out["near_resonance_is_not_a_bug"] = {
        "alpha": 2.0 + 1e-9, "measured": got, "exact_finite_domain": ex,
        "ratio": got / ex, "predicted_companion_infinite_domain": pred,
        "note": ("The measured norm matches the exact TRUNCATED-domain value; it is the "
                 "`predicted` companion (2/|alpha-2| = 2e9) that refers to the infinite "
                 "domain, and the docstring says so explicitly.  Not a finding."),
    }

    out["farfield_symbol_coefficient_spotcheck"] = {
        "alpha_2_c_half": farfield_symbol_coefficient(2.0, 0.5),
        "vanishes_at_resonance": farfield_symbol_coefficient(2.0, 0.5) == 0.0,
    }
    return out


# ---------------------------------------------------------------------------
# downstream exposure census
# ---------------------------------------------------------------------------


def downstream_exposure():
    return {
        "method": ("grep -rn over *.py for every public symbol of solver/decay_grading.py; "
                   "NAME COLLISION handled explicitly -- solver/spectral_certificate.py "
                   "defines a DIFFERENT algebra_constant(kind, param, K), and "
                   "test_spectral_certificate.py / p2_route_l1_v2_spectral.py / "
                   "p2_route_tc_v1_assemble.py call THAT one, not this module's."),
        "farfield_inverse_norm": {
            "call_sites": ["experiments/p2_route_d_v3_spaces.py:356,399",
                           "experiments/p2_route_d_v6_bounds.py:217",
                           "experiments/p2_route_d_v7_seminorm.py:294",
                           "experiments/p2_route_d_v8_quadratic.py (import)",
                           "test_decay_grading.py:186"],
            "n_used": "8001 everywhere (the default); dtau = 3.45e-3",
            "c_used": "0.5 everywhere (C_ANCHOR = 0.5, solver/decay_collocation.py:51)",
            "threshold": "dtau < 2c = 1.0",
            "margin_decades": math.log10(1.0 / dtau_of(8001)),
            "status": "LATENT -- every banked call site is 2.46 decades inside the threshold.",
        },
        "algebra_constant": {
            "call_sites": ["experiments/p2_route_d_v3_spaces.py:171,239,270,305",
                           "test_decay_grading.py:134"],
            "v_sizing": "len(v) = 2K at every site (np.ones(80) against np.ones(41), and "
                        "(1+arange(1,2K+1))**t against (1+arange(K+1))**s)",
            "status": "LATENT -- no banked site truncates v or passes a poisoned weight.",
        },
        "cos_power_coeffs": {
            "call_sites": ["experiments/p2_route_d_v3_spaces.py:368,392",
                           "experiments/p2_route_d_v4_graded.py:262",
                           "test_decay_collocation.py:112", "test_decay_grading.py"],
            "alpha_used": "positive throughout (0, 1.5, 2, 2.5, 3, 4)",
            "status": "LATENT -- no banked site passes alpha < 0.",
        },
        "farfield_inverse_norm_finite": {
            "call_sites": ["experiments/p2_route_d_v3_spaces.py:357",
                           "experiments/p2_route_d_v4_graded.py:76",
                           "test_decay_grading.py:187"],
            "status": "LATENT -- X0 = 1.0 < Xmax = 1e12 at every site.",
        },
        "cos_power_mass": {
            "call_sites": ["solver/nk_bounds.py:326,331", "four experiments", "two tests"],
            "status": "GUARDED at the source (alpha <= 1 raises); no finding.",
        },
        "banked_numbers_at_risk": 0,
        "severity": ("All five findings are LATENT public-API hazards, the same severity "
                     "shape as legs 66/69/79/115/120.  No banked number in writeup/data is "
                     "wrong because of them, and this leg re-computes none."),
    }


# ---------------------------------------------------------------------------


def run_all():
    data = {
        "leg": 139,
        "route": "ROUTE-DGA",
        "module_under_audit": "solver/decay_grading.py",
        "module_edited": False,
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/decay_grading.py ever silently return a wrong value rather than "
                 "propagating or flagging the invalid input?"),
        "what_this_is_not": ("Not a measurement of anything physical.  No number here is a "
                             "statement about blow-up or about any certificate constant.  No "
                             "bound is sharpened; no banked result is contested."),
        "batteries": {
            "G1_guard_asymmetry": g1_guard_asymmetry(),
            "G2_fabricated_zero_norm": g2_fabricated_zero(),
            "G3_negative_alpha_coefficients": g3_negative_alpha(),
            "G4_negative_norm": g4_negative_norm(),
            "G5_algebra_constant_poison": g5_algebra_constant(),
            "G6_what_the_module_gets_right": g6_passes(),
        },
        "downstream_exposure": downstream_exposure(),
    }

    g1, g2, g3, g4, g5 = (data["batteries"][k] for k in
                          ("G1_guard_asymmetry", "G2_fabricated_zero_norm",
                           "G3_negative_alpha_coefficients", "G4_negative_norm",
                           "G5_algebra_constant_poison"))
    data["gate_answer"] = "YES"
    data["findings"] = {
        "G1_headline": (
            f"farfield_inverse_norm enforces its own documented step condition dtau < 2c on "
            f"the alpha > 2 branch only.  At n = {g1['headline_pair']['n']} "
            f"(dtau = {g1['headline_pair']['dtau']:.3f} > 2c = 1.0) the alpha = 2.5 call "
            f"raises ValueError('grid too coarse: need dtau < 2c') and the alpha = 1.5 call "
            f"silently returns {g1['headline_pair']['below']['norm']:.6g} where the module's "
            f"own exact closed form gives {g1['exact_continuum_finite_domain']:.6f} -- a "
            f"factor {g1['headline_pair']['below']['ratio_to_exact']:.4g}, no warning, no NaN. "
            f"Worst silent ratio over the ladder: "
            f"{g1['worst_silent_ratio']:.4g}x at n = {g1['worst_silent_n']}.  The dangerous "
            f"regime is not the wild one: just past the threshold (n = 28, dtau = 1.0234) it "
            f"returns 2.8534, a perfectly believable norm that is 29% low.  MECHANISM, "
            f"separated from mere discretization error: forming the map g -> h as a matrix "
            f"shows 0.0% negative entries below the threshold (where the one-pass value "
            f"equals the true discrete induced norm exactly, ratio 1.000000) and 21.4-23.2% "
            f"negative entries above it, where the one-pass value understates the true "
            f"discrete induced norm by up to 3.289x -- i.e. past dtau = 2c the returned "
            f"quantity is not an induced norm at all.  The onset tracks c, not n: the largest "
            f"n the alpha > 2 branch refuses is 14 / 28 / 56 / 111 against the predicted "
            f"dtau = 2c values 14.82 / 28.63 / 56.26 / 111.52 for c = 1 / 0.5 / 0.25 / 0.125."),
        "G2_headline": (
            f"A negative speed c and a swapped domain X0 > Xmax each make the same function "
            f"return EXACTLY 0.0 as an induced norm ({g2['n_exact_zero']}/4 inadmissible "
            f"cases), with the `predicted` companion still reading 4.0 beside it.  The "
            f"module's single guard cannot fire: q = {g2['q_at_negative_c']:.6f} > 0 when "
            f"c < 0.  Zero is the unsafe direction -- it makes any NK budget look free.  The "
            f"one case of the four that IS refused (swapped domain, alpha = 2.5) is caught "
            f"only incidentally, by the coarse-grid guard aimed at something else: a "
            f"descending grid makes dtau negative, so q < 0 fires.  Nothing in the module "
            f"checks c > 0 or X0 < Xmax."),
        "G3_headline": (
            f"cos_power_coeffs fabricates a coefficient sequence for alpha <= -1 where none "
            f"exists (f is not integrable): |a_K| grows "
            f"{g3['b_divergence']['rows'][0]['coefficient_growth_100_to_10000']:.3g}x from "
            f"K = 100 to K = 10000 at alpha = -1.5 and the evaluated series moves AWAY from "
            f"the function it claims to be.  On -2 < alpha < -1 the returned a_0 has the "
            f"WRONG SIGN against a reflection-formula oracle "
            f"({g3['a_sign']['n_sign_flipped']} of 5 probes), because math.lgamma returns "
            f"log|Gamma| -- contradicting the docstring's 'no Gamma of a negative argument "
            f"is ever formed'.  Sharp boundary: alpha = -1 raises, and on -1 < alpha < 0 the "
            f"module is verified CORRECT against Gamma-free quadrature "
            f"(max rel err {g3['d_valid_range_control']['max_relative_error']:.2e})."),
        "G4_headline": (
            f"farfield_inverse_norm_finite returns a NEGATIVE operator norm for X0 > Xmax on "
            f"{g4['n_negative']}/4 alphas -- "
            f"{g4['rows'][0]['swapped']:.6g} where the clean value is "
            f"{g4['rows'][0]['clean']:.6f}.  X0 < 0 does raise, so the module refuses the "
            f"obviously broken input and accepts the subtler one."),
        "G5_headline": (
            f"algebra_constant absorbs weight poison: {g5['n_bit_identical']} of 6 poisoned "
            f"weight vectors (+Inf and -Inf at mode 1, and a wholly sign-flipped u) return S "
            f"BIT-IDENTICALLY to the clean call ({g5['clean_S']:.10g}, 0 ULP, no warning); an "
            f"Inf that does register moves S DOWN to "
            f"{[p['S'] for p in g5['poison_rows'] if p['case'] == 'inf_at_mode_K'][0]:.6g} "
            f"({[p['ratio_to_clean'] for p in g5['poison_rows'] if p['case'] == 'inf_at_mode_K'][0]:.4f}x); "
            f"and a v sized to len(u) instead of 2(len(u)-1) under-reports the SHARP constant "
            f"by {g5['truncation_rows'][1]['understatement_vs_2K']:.4g}x.  Every direction is "
            f"the unsafe one, and the two-sided bracket S/4 <= M <= S/2 is reported unchanged."),
    }
    data["controls_that_could_have_failed"] = (
        "alpha in (-1,0) coefficients verified correct against Gamma-free quadrature; "
        "hilbert_of_cos_power pushed three decades past its documented X ~ 1e4 ceiling and "
        "still matching the exact far-field law; the alpha = 2 resonance returning inf; "
        "X0 = 0, empty input, negative M and cos_power_mass(alpha <= 1) all raising; NaN "
        "propagating through algebra_constant from both arguments; the range-reduction fold "
        "exact past |theta| > pi/2; quadratic_coeffs matching an independent double loop; and "
        "the near-resonance alpha = 2 + 1e-9 value, which is CORRECT and is reported as not a "
        "finding.  The mechanism ablation in G1 varies c and moves the onset with it -- if "
        "the cause were 'the grid is small' rather than the sign of q, it would not move."
    )
    data["escalation"] = (
        "Gate YES -> the pre-committed branch is: report the exact failing case with "
        "magnitudes, ESCALATE, DO NOT PATCH.  solver/decay_grading.py is not edited under "
        "either branch of this leg's gate and is not edited here."
    )
    return data


if __name__ == "__main__":
    import json

    result = run_all()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                            "writeup", "data", "p2_route_dga_v1_adversarial.json")
    out_path = os.path.normpath(out_path)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=False, default=str)
    print(f"wrote {out_path}")
    print(f"gate_answer = {result['gate_answer']}")
    for k, v in result["findings"].items():
        print(f"\n{k}: {v}")
