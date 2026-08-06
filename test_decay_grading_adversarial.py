"""Adversarial battery for solver/decay_grading.py -- the decay-graded function-space layer
under the collocation lane (leg 139, Route-DGA).

WHY THIS FILE EXISTS, ALONGSIDE `test_decay_grading.py`.  The dedicated file asks the module
eight questions it can fail on its own terms -- a closed form, a second implementation, an
asymptotic oracle -- but every one of them is a KNOWN-ANSWER gate on CLEAN input.  What it does
not do, and was never meant to do, is feed the module degenerate exponents, inadmissible
speeds, swapped domains, poisoned weights or under-resolved grids and ask whether a wrong
answer comes back silently.  Leg 139 does that.

THE GATE (DIRECTION.md, leg 139), answered YES:

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/decay_grading.py ever silently return a wrong value rather than propagating or
    flagging the invalid input?

READ THIS BEFORE CHANGING ANYTHING HERE.  Several checks below PIN CURRENT, DEFECTIVE
BEHAVIOUR.  That is deliberate, and it is legs 66/115/120's precedent: a leg whose territory is
read-only on `solver/` reports defects and pins them rather than fixing them silently, so the
defect cannot drift unnoticed and so the repair has an exact target.  **Every such check is
marked `PIN:` in its docstring and states what the CORRECT behaviour would be.  When the repair
lands, these checks WILL START FAILING -- that is the intended signal, not a regression.**
Update the pin then, in the same commit as the repair.

THE FIVE FINDINGS PINNED HERE (magnitudes measured by
experiments/p2_route_dga_v1_adversarial.py, banked in
writeup/data/p2_route_dga_v1_adversarial.json):

  G1  THE GUARD ASYMMETRY (headline).  `farfield_inverse_norm` runs one trapezoidal recursion
      with coefficients p = 1/dtau + beta/2 and q = 1/dtau - beta/2 on both alpha branches.
      The alpha > 2 branch tests `q <= 0` and raises ValueError("grid too coarse: need
      dtau < 2c"); the alpha < 2 branch never tests it.  The condition is not incidental: the
      module's docstring rests its whole one-pass induced-norm trick on "Every coefficient in
      either recursion is non-negative", and that is the monotone / inverse-positive matrix
      argument, which for the trapezoidal rule carries a finite step restriction (the
      trapezoidal rule is A-stable but not unconditionally positivity-preserving --
      Bonaventura & Della Rocca arXiv:1510.04303; Horvath et al. arXiv:2105.07403).
      MEASURED: at n = 20 (dtau = 1.4543 > 2c = 1.0) alpha = 2.5 raises and alpha = 1.5
      returns 26630.848 against the module's own exact closed form 3.999996 -- 6657.7x, no
      warning, no NaN; worst 1.458e17x at n = 4.  The DANGEROUS case is the quiet one: at
      n = 28 (dtau = 1.0234, barely past the threshold) it returns 2.8534, a believable norm
      29% low.  MECHANISM, separated from ordinary discretization error: forming the map
      g -> h as a matrix gives 0.0% negative entries below the threshold, where the one-pass
      value equals the true discrete induced norm to 1.000000, and 21.4-23.2% negative entries
      above it, where the one-pass value understates the true discrete induced norm by up to
      3.289x -- past dtau = 2c the returned quantity is not an induced norm at all.  The onset
      tracks c, not n: the largest n refused on the alpha > 2 branch is 14 / 28 / 56 / 111 for
      c = 1 / 0.5 / 0.25 / 0.125, against predicted dtau = 2c values 14.82 / 28.63 / 56.26 /
      111.52.

  G2  THE FABRICATED ZERO NORM.  A negative speed c and a swapped domain X0 > Xmax each make
      `farfield_inverse_norm` return EXACTLY 0.0 as an induced norm, with the `predicted`
      companion still reading 4.0 beside it.  MEASURED: 3 of 4 inadmissible cases.  The
      module's only guard cannot fire (c < 0 gives beta < 0, so q = 1/dtau - beta/2 > 0); the
      fourth case is refused only incidentally, because a descending grid makes dtau negative.
      Zero is the maximally unsafe direction: ||A_far|| enters a Newton-Kantorovich budget in
      the numerator.

  G3  FABRICATED COEFFICIENTS AT NEGATIVE alpha.  `math.lgamma` returns log|Gamma(x)| and
      discards the sign, which POSIX keeps in `signgam` and SciPy in `gammasgn`
      (`exp(loggamma(x+0j)) = gammasgn(x)*exp(gammaln(x))`); Python exposes no signgam at all.
      MEASURED: `cos_power_coeffs` returns a_0 with the WRONG SIGN in 4 of 5 negative-alpha
      probes against a reflection-formula oracle, contradicting its own docstring claim that
      "no Gamma of a negative argument is ever formed".  Worse, for alpha <= -1 the function
      |cos(theta/2)|^alpha is not integrable, so NO coefficient sequence exists: |a_K| grows
      10.0x (alpha = -1.5) and 1000.0x (alpha = -2.5) from K = 100 to K = 10000, and the
      evaluated series moves AWAY from the function, error growing 47.6x / 3310.5x.  Sharp
      boundary, and it is what makes this a finding rather than a complaint: alpha = -1 RAISES
      (Gamma pole), and on -1 < alpha < 0 the expansion is legitimate and the module is
      verified CORRECT against a Gamma-free quadrature (max rel err 1.05e-3).  The refusal
      pattern exists one function away in the same file -- `cos_power_mass` refuses alpha <= 1.

  G4  THE NEGATIVE NORM.  `farfield_inverse_norm_finite` returns a NEGATIVE operator norm for
      X0 > Xmax on 4/4 alphas: -3999996.0 where the clean value is 3.999996.  X0 < 0 does
      raise, so the module refuses the obviously broken input and accepts the subtler one.

  G5  THE ALGEBRA CONSTANT ABSORBS POISON.  The condition sup_{j,k} v_{j+k}/(u_j u_k) < oo is
      the standard Beurling submultiplicativity condition, a supremum over ALL pairs;
      `algebra_constant` takes it over j+k <= len(v) and returns a bracket documented as SHARP.
      MEASURED: 3 of 6 poisoned weight vectors (+Inf at mode 1, -Inf at mode 1, and a wholly
      sign-flipped u) return S BIT-IDENTICALLY to the clean call (385.9411764705883, 0 ULP, no
      warning); an Inf that does register moves S DOWN to 273.0667 (0.7075x); a v sized to
      len(u) instead of 2(len(u)-1) under-reports by 5.558x.  Every direction is the unsafe
      one for a quadratic bound, and the bracket S/4 <= M <= S/2 is reported unchanged.

SEVERITY, MEASURED, NOT ASSERTED.  All five are LATENT under current repository usage
(census in the runner's `downstream_exposure`): every in-repo `farfield_inverse_norm` call site
uses the default n = 8001 and c = C_ANCHOR = 0.5, i.e. dtau = 3.45e-3, which is 2.46 decades
inside the threshold; every `algebra_constant` call site sizes v as 2K; no site passes a
negative alpha or X0 > Xmax.  **Banked numbers at risk: 0.**  Same severity shape as legs
66/69/79/115/120.  Note the NAME COLLISION a census must not trip over:
`solver/spectral_certificate.py` defines a DIFFERENT `algebra_constant(kind, param, K)`, and
test_spectral_certificate.py / p2_route_l1_v2_spectral.py call THAT one.

`solver/decay_grading.py` was NOT edited by leg 139, under either branch of its gate.

Run:  .venv/bin/python test_decay_grading_adversarial.py
"""

import math
import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver.decay_grading import (                                      # noqa: E402
    algebra_constant, cos_power_coeffs, cos_power_mass, eval_cos_series,
    eval_sin_series, farfield_grid, farfield_inverse_norm,
    farfield_inverse_norm_finite, hilbert_of_cos_power, quadratic_coeffs,
    theta_of_X, X_of_theta,
)

X0_DEF, XMAX_DEF = 1.0, 1e12


def _dtau(n, X0=X0_DEF, Xmax=XMAX_DEF):
    return math.log(Xmax / X0) / (n - 1)


def _gamma_reflect(x):
    """Gamma(x) WITH ITS SIGN for x < 0 non-integer, by the reflection formula."""
    if x > 0:
        return math.gamma(x)
    return math.pi / (math.sin(math.pi * x) * math.gamma(1.0 - x))


def _a0_continued(alpha):
    return (2.0 ** (-alpha)) * _gamma_reflect(alpha + 1.0) / _gamma_reflect(0.5 * alpha + 1.0) ** 2


def _cos_coeff_quadrature(alpha, k, n=2_000_001):
    """a_k by midpoint quadrature -- an oracle that touches no Gamma function at all."""
    t = (np.arange(n) + 0.5) / n * math.pi
    f = np.abs(np.cos(0.5 * t)) ** alpha
    return float(np.mean(f)) if k == 0 else float(2.0 * np.mean(f * np.cos(k * t)))


def _recursion_response(alpha, c, x, src):
    """Independent second implementation of the module's recursion, arbitrary source."""
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


def _response_matrix(alpha, n, c=0.5):
    x = farfield_grid(X0_DEF, XMAX_DEF, n)
    T = np.zeros((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = 1.0
        T[:, j] = _recursion_response(alpha, c, x, x * e)
    return x, T


# ---------------------------------------------------------------------------
# G1 -- the guard asymmetry
# ---------------------------------------------------------------------------


def check_guard_asymmetry_same_dtau():
    """PIN: at one dtau above the module's own threshold, one branch raises and the other
    returns a finite wrong norm.

    CORRECT behaviour would be for the alpha < 2 branch to apply the SAME `dtau < 2c` check
    the alpha > 2 branch already applies -- the condition is a property of the recursion
    coefficients, not of the branch.
    """
    n = 20
    exact = farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)
    try:
        farfield_inverse_norm(2.5, n=n)
        raise AssertionError("alpha=2.5 no longer refuses a coarse grid -- guard changed")
    except ValueError as e:
        assert "grid too coarse" in str(e), f"unexpected refusal message: {e}"
    got, _ = farfield_inverse_norm(1.5, n=n)
    assert math.isfinite(got), "alpha<2 branch no longer returns a finite value (repaired?)"
    ratio = got / exact
    assert ratio > 1e3, f"PIN BROKEN (repaired?): ratio {ratio} is no longer >1e3"
    return {"n": n, "dtau": _dtau(n), "two_c": 1.0, "below_norm": got, "exact": exact,
            "ratio": ratio, "above_branch": "ValueError"}


def check_guard_asymmetry_quiet_regime():
    """PIN: just past the threshold the wrong value is BELIEVABLE, which is the dangerous
    case -- 2.8534 against an exact 3.999996, 29% low, no warning."""
    n = 28
    exact = farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)
    assert _dtau(n) > 1.0, "n=28 is meant to sit just past dtau = 2c = 1"
    got, _ = farfield_inverse_norm(1.5, n=n)
    rel = abs(got / exact - 1.0)
    assert 0.05 < rel < 0.9, f"PIN BROKEN: relative error {rel} left the quiet band"
    try:
        farfield_inverse_norm(2.5, n=n)
        raise AssertionError("the alpha>2 branch stopped refusing at n=28")
    except ValueError:
        pass
    return {"n": n, "dtau": _dtau(n), "below_norm": got, "exact": exact,
            "relative_error": rel}


def check_positivity_is_the_mechanism():
    """PIN + CONTROL: below the threshold the response matrix is entrywise non-negative and
    the one-pass value IS the induced norm; above it, it is not.

    This is the check that separates the finding from ordinary discretization error, and the
    control half can fail: if the recursion were unconditionally monotone, the negative-entry
    fraction would stay 0 at every n and this check would break.
    """
    out = {}
    for tag, n, expect_neg in (("resolved", 401, False), ("coarse", 20, True)):
        x, T = _response_matrix(1.5, n)
        w_h, w_g = x ** 1.5, x ** 2.5
        g_star = 1.0 / w_g
        one_pass = float(np.max(w_h * (T @ g_star)))
        all_signs = float(np.max(w_h * (np.abs(T) @ g_star)))
        module, _ = farfield_inverse_norm(1.5, n=n)
        assert abs(one_pass - module) <= 1e-9 * max(1.0, abs(one_pass)), (
            f"the second implementation stopped matching the module at n={n}: "
            f"{one_pass} vs {module}")
        frac = float(np.mean(T < 0.0))
        if expect_neg:
            assert frac > 0.1, f"PIN BROKEN: only {frac} negative entries at n={n}"
            assert all_signs / one_pass > 1.5, (
                f"PIN BROKEN: one-pass understates by only {all_signs / one_pass} at n={n}")
        else:
            assert frac == 0.0, f"CONTROL BROKEN: {frac} negative entries at n={n}"
            assert abs(all_signs / one_pass - 1.0) < 1e-12, (
                "CONTROL BROKEN: one-pass is not the induced norm at a resolved grid")
        out[tag] = {"n": n, "negative_entry_fraction": frac,
                    "one_pass": one_pass, "true_induced_norm": all_signs,
                    "understated_by": all_signs / one_pass}
    return {"resolved_neg_frac": out["resolved"]["negative_entry_fraction"],
            "coarse_neg_frac": out["coarse"]["negative_entry_fraction"],
            "coarse_understated_by": out["coarse"]["understated_by"],
            "resolved_understated_by": out["resolved"]["understated_by"]}


def check_threshold_tracks_c_not_n():
    """CONTROL that could have come out flat: the refusal onset moves with c, by the factor
    dtau = 2c predicts, which is what makes the recursion coefficient the mechanism."""
    rows = []
    for c in (1.0, 0.5, 0.25, 0.125):
        predicted = 1.0 + math.log(XMAX_DEF / X0_DEF) / (2.0 * c)
        largest = None
        for n in range(3, 600):
            try:
                farfield_inverse_norm(2.5, c=c, n=n)
                break
            except ValueError:
                largest = n
        assert largest is not None, f"no refusal at all for c={c}"
        assert abs(largest - predicted) <= 1.0, (
            f"onset {largest} does not match dtau=2c prediction {predicted} for c={c}")
        got, _ = farfield_inverse_norm(1.5, c=c, n=largest)
        assert math.isfinite(got), f"alpha<2 branch refused at c={c}, n={largest} (repaired?)"
        rows.append((c, largest, predicted, got))
    return {"onsets": [r[1] for r in rows], "predicted": [round(r[2], 2) for r in rows],
            "below_branch_never_refused": True}


def check_resolved_grid_is_accurate():
    """CONTROL: at the grid every in-repo caller actually uses, the module is right."""
    for alpha in (1.5, 1.9, 2.5, 3.0):
        got, _ = farfield_inverse_norm(alpha, n=8001, Xmax=XMAX_DEF)
        exact = farfield_inverse_norm_finite(alpha, X0_DEF, XMAX_DEF)
        assert abs(got / exact - 1.0) < 5e-4, f"alpha={alpha}: {got} vs {exact}"
    return {"n": 8001, "dtau": _dtau(8001), "max_rel_err": 5e-4, "margin_decades":
            math.log10(1.0 / _dtau(8001))}


# ---------------------------------------------------------------------------
# G2 -- the fabricated zero norm
# ---------------------------------------------------------------------------


def check_negative_speed_returns_zero_norm():
    """PIN: c < 0 returns EXACTLY 0.0 as an induced norm, on both branches.

    CORRECT behaviour would be to refuse c <= 0 -- the module's own far-field derivation fixes
    c = 1/2 > 0 and the homogeneous solution X^{-1/c} has the wrong character otherwise.
    """
    rows = {}
    for alpha in (1.5, 2.5):
        got, pred = farfield_inverse_norm(alpha, c=-0.5, n=2001)
        assert got == 0.0, f"PIN BROKEN (repaired?): alpha={alpha} returned {got}, not 0.0"
        rows[alpha] = (got, pred)
    q = 1.0 / _dtau(2001) - 0.5 * (1.0 / -0.5)
    assert q > 0.0, "the existing q<=0 guard would have fired -- mechanism changed"
    return {"norm_alpha_1.5": rows[1.5][0], "norm_alpha_2.5": rows[2.5][0],
            "predicted_companion": rows[1.5][1], "q_at_negative_c": q,
            "exact_for_clean_input": farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)}


def check_swapped_domain_returns_zero_norm():
    """PIN: X0 > Xmax returns 0.0 on the alpha < 2 branch (the alpha > 2 branch is refused
    only incidentally, by the coarse-grid guard, because dtau goes negative)."""
    got, pred = farfield_inverse_norm(1.5, X0=XMAX_DEF, Xmax=X0_DEF, n=2001)
    assert got == 0.0, f"PIN BROKEN (repaired?): returned {got}, not 0.0"
    try:
        farfield_inverse_norm(2.5, X0=XMAX_DEF, Xmax=X0_DEF, n=2001)
        incidental = "returned"
    except ValueError as e:
        incidental = f"ValueError: {e}"
    return {"below_norm": got, "predicted_companion": pred, "above_branch": incidental}


# ---------------------------------------------------------------------------
# G3 -- fabricated coefficients at negative alpha
# ---------------------------------------------------------------------------


def check_a0_sign_flipped_on_negative_alpha():
    """PIN: a_0 comes back with the wrong sign where Gamma(alpha+1) < 0.

    CORRECT behaviour: refuse alpha <= 0 (the module is a DECAY dictionary), or carry the sign
    the way POSIX signgam / scipy.special.gammasgn do.  The docstring's claim that "no Gamma of
    a negative argument is ever formed" is false for alpha < -1.
    """
    flipped = []
    for alpha in (-1.2, -1.5, -1.8, -2.5, -3.5):
        got = float(cos_power_coeffs(alpha, 1)[0])
        want = _a0_continued(alpha)
        assert abs(abs(got) / abs(want) - 1.0) < 1e-10, (
            f"magnitude changed at alpha={alpha}: |{got}| vs |{want}|")
        if np.sign(got) != np.sign(want):
            flipped.append(alpha)
    assert len(flipped) == 4, f"PIN BROKEN (repaired?): {len(flipped)} sign flips, expected 4"
    return {"n_sign_flipped": len(flipped), "alphas": flipped,
            "docstring_claim_true": False}


def check_coefficients_diverge_below_minus_one():
    """PIN: for alpha <= -1 no coefficient sequence exists and a growing one is returned."""
    rows = {}
    for alpha, want_growth in ((-1.5, 10.0), (-2.5, 1000.0)):
        a100 = abs(cos_power_coeffs(alpha, 100)[-1])
        a10000 = abs(cos_power_coeffs(alpha, 10000)[-1])
        growth = a10000 / a100
        assert growth > 5.0, f"PIN BROKEN (repaired?): growth {growth} at alpha={alpha}"
        assert abs(growth / want_growth - 1.0) < 0.05, (
            f"growth {growth} drifted from the banked {want_growth}")
        f_true = abs(math.cos(0.15)) ** alpha
        errs = [abs(float(eval_cos_series(cos_power_coeffs(alpha, K),
                                          np.array([0.3]))[0]) - f_true)
                for K in (100, 10000)]
        assert errs[1] > errs[0], (
            f"alpha={alpha}: the truncated series stopped diverging -- repaired?")
        rows[alpha] = {"coefficient_growth": growth, "error_growth": errs[1] / errs[0]}
    return {"growth_-1.5": rows[-1.5]["coefficient_growth"],
            "error_growth_-1.5": rows[-1.5]["error_growth"],
            "growth_-2.5": rows[-2.5]["coefficient_growth"],
            "error_growth_-2.5": rows[-2.5]["error_growth"]}


def check_valid_negative_range_is_correct():
    """CONTROL that could have failed: on -1 < alpha < 0 the expansion is legitimate and the
    module agrees with a Gamma-free quadrature.  This is what makes G3 a sharp boundary at
    alpha = -1 rather than a blanket complaint about negative alpha."""
    worst = 0.0
    for alpha in (-0.5, -0.25):
        a = cos_power_coeffs(alpha, 6)
        for k in (0, 1, 2, 3):
            q = _cos_coeff_quadrature(alpha, k)
            worst = max(worst, abs(a[k] - q) / abs(q))
    assert worst < 5e-3, f"CONTROL BROKEN: max relative error {worst}"
    return {"max_relative_error": worst, "range": "-1 < alpha < 0"}


def check_gamma_pole_raises():
    """CONTROL: the exact poles alpha = -1, -2 DO raise -- the module flags the measure-zero
    case and fabricates on the open set beside it."""
    raised = 0
    for alpha in (-1.0, -2.0):
        try:
            cos_power_coeffs(alpha, 4)
        except ValueError:
            raised += 1
    assert raised == 2, f"only {raised}/2 poles raised"
    return {"poles_raised": raised}


def check_cos_power_mass_refuses_alpha_le_1():
    """CONTROL: the refusal pattern EXISTS in this file, one function away (lesson 73)."""
    for alpha in (1.0, 0.5, -1.0):
        try:
            cos_power_mass(alpha)
            raise AssertionError(f"cos_power_mass({alpha}) returned instead of raising")
        except ValueError:
            pass
    return {"refused": 3, "note": "the same module knows the pattern"}


# ---------------------------------------------------------------------------
# G4 -- the negative norm
# ---------------------------------------------------------------------------


def check_finite_norm_goes_negative():
    """PIN: farfield_inverse_norm_finite returns a NEGATIVE norm for X0 > Xmax.

    CORRECT behaviour would be to require X0 < Xmax (or take |log| of the ratio).
    """
    rows = {}
    for alpha in (1.5, 2.5, 1.9, 3.0):
        v = farfield_inverse_norm_finite(alpha, X0=XMAX_DEF, Xmax=X0_DEF)
        assert v < 0.0, f"PIN BROKEN (repaired?): alpha={alpha} returned {v} >= 0"
        rows[alpha] = v
    clean = farfield_inverse_norm_finite(1.5, X0_DEF, XMAX_DEF)
    return {"swapped_alpha_1.5": rows[1.5], "clean": clean,
            "magnitude_ratio": abs(rows[1.5]) / clean, "n_negative": len(rows)}


def check_negative_X0_raises():
    """CONTROL: X0 < 0 DOES raise (a complex power reaches float()) -- the module refuses the
    obviously broken input and accepts the subtler one."""
    try:
        farfield_inverse_norm_finite(1.5, X0=-1.0, Xmax=XMAX_DEF)
        raise AssertionError("X0 < 0 no longer raises")
    except TypeError:
        pass
    return {"raised": "TypeError"}


# ---------------------------------------------------------------------------
# G5 -- the algebra constant absorbs poison
# ---------------------------------------------------------------------------


def _weights(K=8):
    u = (1.0 + np.arange(K + 1.0)) ** -2.0
    v = (1.0 + np.arange(1, 2 * K + 1.0)) ** -1.0
    return u, v


def check_inf_and_sign_poison_bit_identical():
    """PIN: +-Inf at mode 1 and a wholly sign-flipped weight vector return S BIT-IDENTICALLY
    to the clean call -- 0 ULP, no warning, no Inf, no NaN.

    CORRECT behaviour would be to validate that u and v are finite and strictly positive; the
    weights of a Beurling algebra are positive by definition.
    """
    K = 8
    u, v = _weights(K)
    clean = float(algebra_constant(u, v)[0])
    identical = []
    for tag, uu in (("+inf@1", np.where(np.arange(K + 1) == 1, np.inf, u)),
                    ("-inf@1", np.where(np.arange(K + 1) == 1, -np.inf, u)),
                    ("sign_flipped", -u)):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            S = float(algebra_constant(uu, v)[0])
        if S == clean and not w:
            identical.append(tag)
    assert len(identical) == 3, f"PIN BROKEN (repaired?): only {identical} bit-identical"
    return {"clean_S": clean, "bit_identical_cases": identical, "n": len(identical)}


def check_inf_that_registers_moves_S_down():
    """PIN: an Inf at the mode that carried the argmax LOWERS the reported sharp constant --
    the unsafe direction, since M >= S/4 is the lower half of the bracket."""
    K = 8
    u, v = _weights(K)
    clean = float(algebra_constant(u, v)[0])
    S = float(algebra_constant(np.where(np.arange(K + 1) == K, np.inf, u), v)[0])
    assert math.isfinite(S), "PIN BROKEN: the Inf now propagates"
    assert S < clean, f"PIN BROKEN: S went up ({S} vs {clean})"
    return {"clean_S": clean, "poisoned_S": S, "ratio": S / clean}


def check_short_v_understates_sharp_constant():
    """PIN: a v sized to len(u) rather than 2(len(u)-1) under-reports the constant documented
    as sharp, with no length check -- while quadratic_coeffs emits 2K modes by default."""
    K = 8
    u, v = _weights(K)
    full = float(algebra_constant(u, v)[0])
    short = float(algebra_constant(u, v[:K])[0])
    assert short < full, "PIN BROKEN: truncating v no longer lowers S"
    modes = quadratic_coeffs(np.ones(K + 1)).size
    assert modes == 2 * K, f"quadratic_coeffs default mode count changed: {modes}"
    return {"S_full": full, "S_short": short, "understatement": full / short,
            "quadratic_default_modes": modes, "len_v_required": 2 * K}


def check_nan_weights_propagate():
    """CONTROL that could have failed: NaN in either argument DOES reach the output."""
    u, v = _weights(8)
    s_u = float(algebra_constant(np.where(np.arange(9) == 1, np.nan, u), v)[0])
    s_v = float(algebra_constant(u, np.where(np.arange(16) == 2, np.nan, v))[0])
    assert math.isnan(s_u) and math.isnan(s_v), f"NaN absorbed: {s_u}, {s_v}"
    return {"nan_in_u": "nan", "nan_in_v": "nan", "propagates": True}


def check_zero_weight_gives_inf():
    """CONTROL: a zero weight gives +inf, which is the honest answer (and numpy warns)."""
    u, v = _weights(8)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        S = float(algebra_constant(np.where(np.arange(9) == 1, 0.0, u), v)[0])
    assert math.isinf(S), f"zero weight gave {S}, not inf"
    return {"S": S, "warnings": [str(x.category.__name__) for x in w]}


# ---------------------------------------------------------------------------
# G6 -- what the module gets right
# ---------------------------------------------------------------------------


def check_resonance_guard():
    """CONTROL: alpha exactly 2 returns inf on both slots -- honest, not fabricated."""
    got, pred = farfield_inverse_norm(2.0, n=2001)
    assert math.isinf(got) and math.isinf(pred), f"({got}, {pred})"
    return {"norm": got, "predicted": pred}


def check_near_resonance_is_correct():
    """CONTROL: alpha = 2 + 1e-9 is NOT a finding -- the measured norm matches the exact
    truncated-domain value; only the `predicted` companion refers to the infinite domain, and
    the docstring says so."""
    alpha = 2.0 + 1e-9
    got, pred = farfield_inverse_norm(alpha, n=2001)
    exact = farfield_inverse_norm_finite(alpha, X0_DEF, XMAX_DEF)
    assert abs(got / exact - 1.0) < 0.01, f"{got} vs {exact}"
    return {"measured": got, "exact_finite_domain": exact, "ratio": got / exact,
            "predicted_infinite_domain": pred}


def check_hilbert_beyond_documented_ceiling():
    """CONTROL that could have failed: pushed three decades past its own documented X ~ 1e4
    ceiling, hilbert_of_cos_power still matches the exact far-field law."""
    alpha = 3.0
    mass = cos_power_mass(alpha)
    worst = 0.0
    for X in (1e5, 1e6, 1e7):
        h = float(hilbert_of_cos_power(alpha, np.array([X]), K=100000)[0])
        worst = max(worst, abs(h / (mass / (math.pi * X)) - 1.0))
    assert worst < 1e-3, f"deviation {worst} beyond the documented ceiling"
    return {"max_rel_deviation": worst, "documented_ceiling": 1e4, "probed_to": 1e7}


def check_fold_identity_exact():
    """CONTROL: the range-reduction fold is exact, including past |theta| > pi/2."""
    a = cos_power_coeffs(2.5, 200)
    th = np.array([0.1, 1.0, 2.0, 3.0, 3.14159, -2.5])
    k = np.arange(a.size)
    ec = float(np.max(np.abs(eval_cos_series(a, th) - (np.cos(np.outer(th, k)) @ a))))
    es = float(np.max(np.abs(eval_sin_series(a, th) - (np.sin(np.outer(th, k)) @ a))))
    assert ec < 1e-10 and es < 1e-10, f"fold error cos={ec} sin={es}"
    return {"max_abs_err_cos": ec, "max_abs_err_sin": es}


def check_quadratic_matches_double_loop():
    """CONTROL: quadratic_coeffs agrees with an independent double loop; NaN propagates."""
    h = np.array([0.3, -0.7, 0.2, 0.11])
    M = 2 * (h.size - 1)
    brute = np.zeros(M)
    for j in range(h.size):
        for kk in range(h.size):
            if 1 <= j + kk <= M:
                brute[j + kk - 1] += 0.5 * h[j] * h[kk]
    err = float(np.max(np.abs(quadratic_coeffs(h) - brute)))
    assert err < 1e-15, f"disagreement {err}"
    q = quadratic_coeffs(np.array([1.0, np.nan, 0.25]))
    assert int(np.sum(np.isnan(q))) == 3, "NaN no longer reaches the output"
    return {"max_abs_err": err, "nan_modes": 3, "total_modes": int(q.size)}


def check_degenerate_shapes_raise():
    """CONTROL: empty input and a negative mode count DO raise."""
    raised = 0
    for fn, args, kw in ((quadratic_coeffs, (np.array([]),), {}),
                         (quadratic_coeffs, (np.array([1.0, 0.5]),), {"M": -3}),
                         (farfield_inverse_norm, (1.5,), {"X0": 0.0, "n": 501})):
        try:
            fn(*args, **kw)
        except ValueError:
            raised += 1
    assert raised == 3, f"only {raised}/3 degenerate shapes raised"
    return {"raised": raised}


def check_coordinate_roundtrip():
    """CONTROL: X <-> theta round-trips across twelve decades.

    Tolerance 1e-9 relative, not 1e-15: at X = 1e6 the map goes through tan(arctan(X)) where
    theta is within 1e-6 of pi and the derivative is O(X^2), so 2.07e-11 relative is at the
    conditioning limit of the map, not a defect.  Reported as a magnitude, not a boolean.
    """
    Xs = np.array([-1e6, -1.0, 0.0, 1.0, 1e6])
    err = float(np.max(np.abs(X_of_theta(theta_of_X(Xs)) - Xs) / (1.0 + np.abs(Xs))))
    assert err < 1e-9, f"roundtrip error {err}"
    return {"max_rel_err": err}


CHECKS = [
    check_guard_asymmetry_same_dtau,
    check_guard_asymmetry_quiet_regime,
    check_positivity_is_the_mechanism,
    check_threshold_tracks_c_not_n,
    check_resolved_grid_is_accurate,
    check_negative_speed_returns_zero_norm,
    check_swapped_domain_returns_zero_norm,
    check_a0_sign_flipped_on_negative_alpha,
    check_coefficients_diverge_below_minus_one,
    check_valid_negative_range_is_correct,
    check_gamma_pole_raises,
    check_cos_power_mass_refuses_alpha_le_1,
    check_finite_norm_goes_negative,
    check_negative_X0_raises,
    check_inf_and_sign_poison_bit_identical,
    check_inf_that_registers_moves_S_down,
    check_short_v_understates_sharp_constant,
    check_nan_weights_propagate,
    check_zero_weight_gives_inf,
    check_resonance_guard,
    check_near_resonance_is_correct,
    check_hilbert_beyond_documented_ceiling,
    check_fold_identity_exact,
    check_quadratic_matches_double_loop,
    check_degenerate_shapes_raise,
    check_coordinate_roundtrip,
]


def test_guard_asymmetry_same_dtau():
    check_guard_asymmetry_same_dtau()


def test_guard_asymmetry_quiet_regime():
    check_guard_asymmetry_quiet_regime()


def test_positivity_is_the_mechanism():
    check_positivity_is_the_mechanism()


def test_threshold_tracks_c_not_n():
    check_threshold_tracks_c_not_n()


def test_resolved_grid_is_accurate():
    check_resolved_grid_is_accurate()


def test_negative_speed_returns_zero_norm():
    check_negative_speed_returns_zero_norm()


def test_swapped_domain_returns_zero_norm():
    check_swapped_domain_returns_zero_norm()


def test_a0_sign_flipped_on_negative_alpha():
    check_a0_sign_flipped_on_negative_alpha()


def test_coefficients_diverge_below_minus_one():
    check_coefficients_diverge_below_minus_one()


def test_valid_negative_range_is_correct():
    check_valid_negative_range_is_correct()


def test_gamma_pole_raises():
    check_gamma_pole_raises()


def test_cos_power_mass_refuses_alpha_le_1():
    check_cos_power_mass_refuses_alpha_le_1()


def test_finite_norm_goes_negative():
    check_finite_norm_goes_negative()


def test_negative_X0_raises():
    check_negative_X0_raises()


def test_inf_and_sign_poison_bit_identical():
    check_inf_and_sign_poison_bit_identical()


def test_inf_that_registers_moves_S_down():
    check_inf_that_registers_moves_S_down()


def test_short_v_understates_sharp_constant():
    check_short_v_understates_sharp_constant()


def test_nan_weights_propagate():
    check_nan_weights_propagate()


def test_zero_weight_gives_inf():
    check_zero_weight_gives_inf()


def test_resonance_guard():
    check_resonance_guard()


def test_near_resonance_is_correct():
    check_near_resonance_is_correct()


def test_hilbert_beyond_documented_ceiling():
    check_hilbert_beyond_documented_ceiling()


def test_fold_identity_exact():
    check_fold_identity_exact()


def test_quadratic_matches_double_loop():
    check_quadratic_matches_double_loop()


def test_degenerate_shapes_raise():
    check_degenerate_shapes_raise()


def test_coordinate_roundtrip():
    check_coordinate_roundtrip()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.6g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall decay_grading ADVERSARIAL checks passed ({len(CHECKS)} checks)")
    print("NOTE: G1-G5 PIN CURRENT DEFECTIVE BEHAVIOUR (see module docstring).")
    print("They are expected to FAIL once solver/decay_grading.py is repaired -- that is")
    print("the intended signal. Banked magnitudes: writeup/data/p2_route_dga_v1_adversarial.json")
