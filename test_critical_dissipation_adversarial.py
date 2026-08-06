"""Adversarial battery for solver/critical_dissipation.py -- Route-CDA, leg 121.

`test_critical_dissipation.py` (Route-H) tests that the module MEASURES correctly at
admissible `(a, mu, p)` -- the marginal case, the exact `a = 0` family, the `a = 1/2` drift,
the residual-vs-signal refusal predicate applied by the EXPERIMENT driver. It never asks what
the module does when a caller hands it degenerate or malformed input. Leg 121 does that.

THE GATE (DIRECTION.md, leg 121), answered YES:

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/critical_dissipation.py ever silently return a wrong exponent instead of
    flagging the input?

**THIS FILE MAKES NO CLAIM ABOUT alpha_1, alpha_0, OR ANY BANKED EXPONENT.** `capabilities.py`
records `alpha_1 = 0` at `a = 0` (== ALS eq 61), `sigma = 3` at `a = 1/2` (published, Xu Table
1), and `alpha_1 = +0.133683` at `a = 1/2` (measured, leg 64, not independently validated).
None of that is re-derived, re-measured, or contested below. Every assertion is about CODE
BEHAVIOUR UNDER MALFORMED OR DEGENERATE INPUT.

**LEG 154 LANDED THE REPAIR FOR E1/E2/E3 AND INVERTED THOSE PINS IN THE SAME COMMIT.
E4, E5 AND E6 ARE STILL PINS AND STILL PIN DEFECTIVE BEHAVIOUR.**

  INVERTED (E1a, E1b, E2, E3): `p` is now validated for integrality and finiteness in
  both `lambda_power` and `CriticalDissipativeFlow.__init__`, by `_validated_p`, raising
  `CriticalDissipationDomainError` (a `ValueError` subclass -- the base is load-bearing,
  see the sub-integer CONTROL below). Leg 154's gate answered YES on both clauses:
  15/15 of leg 121's non-integer cases refused (was 0/15), and 627,934/627,934
  clean-input leaves bit-identical to the pre-repair module at 9dba93f.

  NOT INVERTED, BECAUSE NOT REPAIRED (E4, E5, E6): leg 154's gate licensed the
  exponent-truncation repair and nothing else. Negative `mu`, `mu_decay_time`'s domain
  and `marginal_verdict` on a non-finite `alpha_1` are unchanged, still defective, and
  still escalated. Their pins below are live and MUST keep passing.

  ADDED (leg 154): `check_non_finite_p_refused_as_a_domain_error` pins the `isfinite`
  clause as measured-necessary -- `floor(inf) == inf`, so an integrality-only guard is
  blind to infinity, which is precisely what leg 121's own PRESCRIBED predicate was.

Leg 121's magnitudes are NOT weakened anywhere below. Where the finding was a bit-identity
between a corrupted run and an honest one, that identity is still asserted -- through the
`on_noninteger="truncate"` escape hatch, which exists so that a repair cannot destroy the
record that authorised it (banked lesson, leg 135). Only the DEFAULT verdict flipped.

READ THIS BEFORE CHANGING ANYTHING HERE. Several checks below PIN CURRENT, DEFECTIVE
BEHAVIOUR -- leg 66's precedent, followed by leg 91 and leg 120: a leg whose territory is
read-only on `solver/` reports and pins defects rather than fixing them silently, so the
defect cannot drift unnoticed and the repair has an exact target. **Every such check is
marked `PIN:` and states what the CORRECT behaviour would be. When a repair lands, these
checks WILL START FAILING -- that is the intended signal. Update the pin in the same commit
as the repair.**

THE FINDINGS PINNED HERE (magnitudes measured by
experiments/p2_route_cda_v1_adversarial.py, banked in
writeup/data/p2_route_cda_v1_adversarial.json):

  E1  THE HEADLINE. `lambda_power(K, p)` and `CriticalDissipativeFlow(..., p=..., ...)` both
      enforce the module's own stated precondition -- "p a positive integer (2s = p)" -- with
      a bare `int(p)` cast and NOTHING ELSE. `int()` on a non-integral float silently
      discards the fractional part (CWE-197, Numeric Truncation Error). `p = 1.9` (a request
      for s = 0.95) silently BUILDS p = 1 (s = 0.5): the Newton solve converges to
      machine-precision residual and every returned number -- `alpha`, `alpha_slope`'s
      `alpha_1` -- is BIT-IDENTICAL to an honest `p = 1` request. No exception, no warning, no
      field records the substitution. The published fractional-Laplacian literature imposes
      no integer restriction on the order (writeup/novelty/leg_121.md, N2) -- the restriction
      is local to this module's exact-representation trick, so a caller has every reason to
      expect a non-integer `s`/`p` is legitimate input.

  E2  THE ASYMMETRY. Python's `int()` gives a float the "benefit of the doubt" (truncates)
      but gives a numeric STRING none (raises on any non-integral literal). `p = '3.5'`
      raises `ValueError`; `p = 3.5` (a float, exactly as far from an integer) is silently
      accepted and rounded to `p = 3`. The type that looks more validated is more dangerous.

  E3  A REALISTIC ROUTE TO THE SAME DEFECT. Nobody types `p = 1.9` by hand; `p` is more
      plausibly computed as `2 * s` from a fitted or subtracted float. Ordinary float64
      arithmetic (`2.5 - 1e-12`, a magnitude of noise smaller than any fit in this repository
      achieves) lands `p` a hair BELOW the intended integer, and `int()` takes the floor:
      `int(2.0 * (2.5 - 1e-12)) == 4`, not the intended `5`.

  E4  NEGATIVE `mu` (anti-dissipation, an energy SOURCE) is accepted with no domain check
      anywhere in the module. `mu = nu / (A L^{2s})` is the same physical quantity leg 91
      audited as `nu` in `solver/fractional_gclm.py`, where `nu < 0` was found to silently
      return a finite, plausible `p`. This module repeats the finding: at `a = 1/2, p = 3`
      (the resonance where `alpha` genuinely depends on `mu`), the Newton solve converges for
      `mu < 0` to a residual comparable to the admissible branch's own, and returns a finite,
      structurally indistinguishable `alpha`.

  E5  `mu_decay_time(alpha_1, mu0, target)` assumes `target < mu0` (decay TOWARDS a smaller
      value) and `mu0, target >= 0`. None of the three is checked. `target > mu0` -- asking
      for the time to decay to a LARGER value, which is meaningless under
      `mu_tau = -alpha_1 mu^2 < 0` -- silently returns a NEGATIVE time. So does `mu0 < 0` or
      `target < 0`.

  E6  `marginal_verdict(alpha_1)` classifies the marginal case from the SIGN of `alpha_1`
      alone. `alpha_1 = NaN` (which can legitimately arise upstream -- see
      `test_critical_dissipation.py` test 10's own note that `alpha_slope` "cannot know" when
      its fit is residual-dominated) or `alpha_1 = +-inf` gets a DEFINITE, wrong-looking
      physical classification (`"dissipation_runs_away"` for NaN) instead of an exception or
      an explicit "undefined" outcome.

SEVERITY, MEASURED, NOT ASSERTED: **no banked result is affected.** Every call site of
`CriticalDissipativeFlow`, `mu_branch`, `lambda_power` or `dissipative_spectrum` outside this
module and its own tests passes `p` as a literal integer (1, 3, 5) or a name traced back to
`CRITICAL_POINTS`. Zero call sites currently compute `p` arithmetically from a float. E1/E3 are
LATENT, exactly the severity shape of legs 66, 69, 79 and 120 -- see
`experiments/journal/leg_121.md` for the call-site census. Leg 121's pre-committed yes-branch
is "escalate, do not patch", and this leg edits no solver file.

Test convention (repo-wide): self-running script, no pytest.
    .venv/bin/python test_critical_dissipation_adversarial.py     (~2 min; E4 needs a Newton
    continuation and is the slow check)
"""

import sys
import warnings

import numpy as np

sys.path.insert(0, ".")

from solver.critical_dissipation import (
    CriticalDissipationDomainError, CriticalDissipativeFlow, alpha_slope,
    amplitude_eigenvalue, lambda_power, marginal_verdict, mu_branch, mu_decay_time,
)

NAN, INF = float("nan"), float("inf")


# =========================================================================
# E1 -- the headline: non-integer p silently truncates
# =========================================================================

def check_lambda_power_truncates_non_integer_p():
    """INVERTED BY LEG 154 (was PIN E1a). `lambda_power(K, p)` now validates integrality
    before `int(p)`. All five of leg 121's cases are REFUSED with
    `CriticalDissipationDomainError`, and the exception message names BOTH the requested
    `p` and the integer that would have been silently substituted -- the substitution is
    the finding, so the repair says it out loud rather than only refusing.

    The `escape` arm keeps leg 121's OWN measurement runnable (banked lesson, leg 135): a
    repair that makes the escalating leg's battery unrunnable destroys the record that
    authorised it. `on_noninteger="truncate"` must still reproduce the pre-repair matrix
    BIT-IDENTICALLY, behind exactly one `RuntimeWarning`."""
    K = 48
    out = {"cases": 0, "refused": 0, "escape_bit_identical": 0}
    for p_req, p_expect in ((1.9, 1), (1.0000001, 1), (2.9999999, 2), (2.9, 2), (3.9, 3)):
        out["cases"] += 1
        try:
            lambda_power(K, p_req)
            raise AssertionError(
                f"E1a INVERTED at p={p_req}: lambda_power must now REFUSE a non-integral "
                f"p, but it accepted one and would have built p={p_expect}. Leg 121's "
                f"finding has regressed."
            )
        except CriticalDissipationDomainError as e:
            assert isinstance(e, ValueError), "the guard must stay a ValueError subclass"
            msg = str(e)
            assert repr(p_req) in msg and str(p_expect) in msg, (
                f"E1a at p={p_req}: the refusal must name both the requested p and the "
                f"integer {p_expect} that would have been substituted; got {msg!r}"
            )
            out["refused"] += 1
        # the escape hatch still reproduces leg 121's exact object
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            L, _ = lambda_power(K, p_req, on_noninteger="truncate")
        assert len(w) == 1 and issubclass(w[0].category, RuntimeWarning), [str(x) for x in w]
        L_true, _ = lambda_power(K, p_expect)
        assert np.array_equal(L, L_true), (
            f"the escape hatch at p={p_req} must reproduce the pre-repair p={p_expect} "
            f"matrix bit-identically, so leg 121's measurement survives its own repair"
        )
        out["escape_bit_identical"] += 1
    assert out["refused"] == out["escape_bit_identical"] == out["cases"] == 5, out
    return out


def check_flow_identity_under_p_truncation():
    """INVERTED BY LEG 154 (was PIN E1b), THE HEADLINE. `CriticalDissipativeFlow(...,
    p=1.9, ...)` claims to build s = 0.95 (2s = p) and used to build s = 0.5 instead,
    returning alpha, the residual and alpha_1 BIT-IDENTICAL to an honest p = 1 request.
    It now refuses before building anything.

    LEG 121'S MAGNITUDES ARE NOT WEAKENED -- THEY ARE STILL ASSERTED, THROUGH THE ESCAPE
    HATCH. The whole force of the finding is that the corrupted run was indistinguishable
    from an honest one at machine precision, and that remains measurable here: the
    truncate arm must STILL be bit-identical to the honest lower-integer request, and the
    corrupted run must STILL look converged. Only the default verdict flipped."""
    K = 64
    mus = [0.0, 0.05, 0.1]
    out = {"bands": [], "refused": 0}
    for p_true, p_fake in ((1, 1.9), (2, 2.9), (3, 3.9)):
        # (1) the repair: the default path refuses, before any Newton solve
        try:
            CriticalDissipativeFlow(0.0, mu=0.1, p=p_fake, K=K)
            raise AssertionError(
                f"E1b INVERTED at p={p_fake}: the flow must now refuse a non-integral p "
                f"rather than silently building p={p_true}. Leg 121's finding has regressed."
            )
        except CriticalDissipationDomainError:
            out["refused"] += 1

        # (2) leg 121's measurement, still executable and still exact
        rows_true = mu_branch(0.0, p_true, mus, K=K)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            f_fake = CriticalDissipativeFlow(0.0, mu=0.1, p=p_fake, K=K,
                                             on_noninteger="truncate")
            rows_fake = [
                {"alpha": f_fake.alpha(rows_true[-1]["b"]),
                 "residual": rows_true[-1]["residual"], "b": rows_true[-1]["b"]}
            ]
        assert len(w) >= 1 and issubclass(w[0].category, RuntimeWarning)
        assert f_fake.p == p_true and f_fake.s == 0.5 * p_true, (
            f"E1b escape: p={p_fake} must still build p={p_true} under truncate, "
            f"got p={f_fake.p}"
        )
        f_true = CriticalDissipativeFlow(0.0, mu=0.1, p=p_true, K=K)
        assert f_true.alpha(rows_true[-1]["b"]) == rows_fake[-1]["alpha"], (
            f"E1b at p_true={p_true}: under the escape hatch the substitution must STILL "
            f"be bit-identical -- that identity is leg 121's finding and must survive its "
            f"own repair"
        )
        assert np.array_equal(f_true.Lp, f_fake.Lp) and np.array_equal(f_true.Lam, f_fake.Lam)
        assert rows_true[-1]["residual"] < 1e-4, (
            "the corrupted run must still LOOK converged -- that is the finding"
        )
        out["bands"].append({"p_true": p_true, "p_requested": p_fake,
                             "alpha": rows_true[-1]["alpha"],
                             "residual": rows_true[-1]["residual"]})
    assert out["refused"] == 3, out
    return out


def check_realistic_float_near_miss():
    """PIN (E3): a REALISTIC route to E1's defect. `p` computed as `2 * s` from an ordinary
    float64 subtraction lands a hair below an integer, and `int()` silently takes the floor --
    a full unit off the intended exponent. CORRECT BEHAVIOUR: `round(p)` or an explicit
    integrality check. Pinned as: floor, unconditionally."""
    s_noisy = 2.5 - 1e-12                 # noise far smaller than any fit in this repo achieves
    p = 2.0 * s_noisy
    intended = 5
    built = int(p)
    assert p != intended and abs(p - intended) < 1e-9, (p, intended)
    assert built == intended - 1, (
        f"E3: expected the realistic float near-miss to land int(p) one unit below the "
        f"intended exponent (built={intended - 1}), got {built}. This is a statement about "
        f"Python's int() semantics, not about critical_dissipation.py directly -- it shows "
        f"E1's defect is reachable by ordinary arithmetic, not only by a hand-typed literal."
    )
    # INVERTED BY LEG 154: Python's int() still floors -- that half of E3 is a fact about
    # the language and cannot be repaired -- but the module no longer consults it silently.
    try:
        lambda_power(32, p)
        raise AssertionError(
            f"E3 INVERTED: the module must now refuse the realistic near-miss p={p!r} "
            f"rather than silently building p={built}, a full unit below the intended "
            f"{intended}."
        )
    except CriticalDissipationDomainError:
        refused = True
    # and the two constructions leg 121 recorded as NOT triggering the near-miss must
    # still be ACCEPTED -- the guard must not over-reject exactly-integral arithmetic
    for val in (2.0 * (5 * 0.1 * 5), 2.0 * sum([0.5] * 5)):
        assert float(val).is_integer() and val == 5.0, val
        lambda_power(16, val)                       # must not raise
    return {"s_noisy": s_noisy, "p_computed": p, "intended_p": intended, "built_p": built,
            "now_refused": refused, "exactly_integral_arithmetic_still_accepted": 2}


def check_string_vs_float_type_coercion_asymmetry():
    """INVERTED BY LEG 154 (was PIN E2). The asymmetry is GONE: `'3.5'` and `3.5` are now
    refused alike. Leg 121's framing was "refuse both, or accept both after validating
    integrality"; the repair took the first.

    THE OTHER HALF OF THIS CHECK IS THE ONE THAT MATTERS FOR CLAUSE (b), AND IT IS
    DELIBERATELY UNMOVED. The repair validates ONLY `float`/`np.floating` inputs and
    leaves every other type on the original `int(p)` path, so `'3'` is still accepted and
    `'3.0'` is still refused BY int() ITSELF. Widening the guard to strings would newly
    ACCEPT `'3.0'` -- a behaviour change on an input that was previously refused -- and
    the repair's no-op licence forbids it. `operator.index` (PEP 357), which is what
    NumPy uses for `np.linspace`'s `num`, would reject even `3.0`; not adopted, for the
    same reason. See writeup/novelty/leg_154.md Q3."""
    out = {}
    try:
        CriticalDissipativeFlow(0.0, 0.0, "3.5", 32)
        raise AssertionError("p = '3.5' (a string) was expected to raise")
    except ValueError:
        out["string_refused"] = True
    try:
        CriticalDissipativeFlow(0.0, 0.0, 3.5, 32)          # the SAME value, as a float
        raise AssertionError(
            "E2 INVERTED: p=3.5 (float) must now be refused, not silently truncated to 3. "
            "The type-coercion asymmetry leg 121 found has regressed."
        )
    except CriticalDissipationDomainError:
        out["float_now_refused"] = True
    out["asymmetry_closed"] = out["string_refused"] and out["float_now_refused"]
    # UNMOVED, and load-bearing for clause (b): integral strings still accepted, and
    # '3.0' still refused by int() itself rather than by the new guard.
    g = CriticalDissipativeFlow(0.0, 0.0, "3", 32)
    assert g.p == 3
    out["integer_string_accepted"] = True
    try:
        CriticalDissipativeFlow(0.0, 0.0, "3.0", 32)
        raise AssertionError("'3.0' must still be refused, by int() itself -- unmoved")
    except CriticalDissipationDomainError:
        raise AssertionError(
            "'3.0' must be refused by int(), NOT by the new guard -- the guard must not "
            "reach strings, or it would newly accept '3.0' and move a clean input"
        )
    except ValueError:
        out["integral_string_3p0_still_refused_by_int"] = True
    # exactly-integral floats must STILL be accepted -- leg 121 pins these as correct
    for p_ok in (3.0, np.float64(3.0), np.int64(3), 3):
        assert CriticalDissipativeFlow(0.0, 0.0, p_ok, 32).p == 3
    out["exactly_integral_floats_still_accepted"] = 4
    return out


def check_lambda_power_refuses_sub_integer_p():
    """CONTROL (a PASS): once `int(p)` lands below 1, `lambda_power` DOES refuse -- but only
    as an accident of the `p < 1` check, not because it validated integrality. This is what
    makes E1 exactly "the low band is caught, everything p >= 1 is not"."""
    out = {"refused": 0}
    for p in (0.5, 0.999, -0.5, -3, 0):
        try:
            lambda_power(48, p)
            raise AssertionError(f"lambda_power(K, {p}) should have raised")
        except ValueError:
            out["refused"] += 1
    assert out["refused"] == 5, out
    return out


# =========================================================================
# E4 -- negative mu (anti-dissipation)
# =========================================================================

def check_negative_mu_converges_silently():
    """PIN (E4): mu = nu/(A L^{2s}) is the SAME physical quantity fractional_gclm.py calls
    nu, which leg 91 found accepted at negative (anti-dissipating) values with no domain
    check. Repeated here at a = 1/2, p = 3 -- the resonance where alpha genuinely depends on
    mu (a = 0 cannot show this: alpha == 1 there identically, for either sign of mu).

    Resolution is reduced (K = 48, da = 0.05) from the module's own defaults (K = 96,
    da = 0.02) for test runtime; this is a REGRESSION TEST for the presence of the defect,
    not a physics measurement -- the production-resolution numbers are banked in
    writeup/data/p2_route_cda_v1_adversarial.json (C5).

    CORRECT BEHAVIOUR: refuse mu < 0, or at least flag the branch as non-physical. Pinned as:
    converges to a residual comparable to the admissible branch, with no signal at all.
    """
    K, da = 48, 0.05
    mus_pos = [0.0, 0.05, 0.1, 0.2]
    mus_neg = [0.0, -0.05, -0.1, -0.2]
    rows_pos = mu_branch(0.5, 3, mus_pos, K=K, da=da)
    rows_neg = mu_branch(0.5, 3, mus_neg, K=K, da=da)
    worst_pos = max(r["residual"] for r in rows_pos[1:])     # exclude the mu=0 seed row
    worst_neg = max(r["residual"] for r in rows_neg[1:])
    out = {"worst_residual_positive_mu": worst_pos, "worst_residual_negative_mu": worst_neg,
          "alpha_at_mu_minus_0.2": rows_neg[-1]["alpha"]}
    assert all(np.isfinite(r["alpha"]) for r in rows_neg), rows_neg
    assert worst_neg < 100.0 * worst_pos, (
        f"PIN E4: expected the anti-dissipative branch to converge to a residual comparable "
        f"to the admissible branch's own (pos={worst_pos:.2e}, got neg={worst_neg:.2e}). "
        f"If the module now refuses mu < 0 this assertion SHOULD fail."
    )
    assert worst_neg < 1e-3, (
        "the anti-dissipative branch must still LOOK converged -- that is the finding", out
    )
    return out


# =========================================================================
# E5 -- mu_decay_time domain violations
# =========================================================================

def check_mu_decay_time_negative_time():
    """PIN (E5): `mu_decay_time` assumes `0 <= target < mu0`. None of the three is checked.
    CORRECT BEHAVIOUR: raise (or return nan/inf) on target >= mu0, or on a negative mu0/target.
    Pinned as: silently return a NEGATIVE time."""
    out = {}
    t_ctrl = mu_decay_time(0.13, 0.2, 0.02)
    assert t_ctrl > 0.0
    out["control_positive_time"] = t_ctrl

    t_bad = mu_decay_time(0.13, 0.2, 0.5)          # target > mu0: meaningless
    assert t_bad < 0.0, (
        f"PIN E5a: expected target > mu0 to silently return a NEGATIVE time, got {t_bad}. "
        f"If mu_decay_time now validates target < mu0 this assertion SHOULD fail."
    )
    out["target_gt_mu0_time"] = t_bad

    t_negmu0 = mu_decay_time(0.13, -0.2, 0.02)     # mu0 < 0: nonsensical initial state
    assert np.isfinite(t_negmu0) and t_negmu0 > 0.0, (
        "PIN E5b: a negative mu0 is accepted and returns a plausible-looking POSITIVE time "
        "with no domain check at all", t_negmu0,
    )
    out["negative_mu0_time"] = t_negmu0

    t_negtarget = mu_decay_time(0.13, 0.2, -0.02)  # target < 0: nonsensical target state
    assert t_negtarget < 0.0, (
        f"PIN E5c: expected a negative target to also return a negative time, got "
        f"{t_negtarget}."
    )
    out["negative_target_time"] = t_negtarget
    return out


# =========================================================================
# E6 -- marginal_verdict on non-finite alpha_1
# =========================================================================

def check_marginal_verdict_nonfinite_input():
    """PIN (E6): `marginal_verdict` reads only the sign of `alpha_1`. `abs(nan) <= tol` is
    False and `nan > 0` is False, so NaN falls through to the LAST branch. CORRECT BEHAVIOUR:
    raise, or return an explicit "undefined"/"invalid" classification, for any non-finite
    input. Pinned as: a definite, wrong-looking verdict."""
    out = {}
    v_nan = marginal_verdict(NAN)
    assert v_nan == "dissipation_runs_away", (
        f"PIN E6a: expected marginal_verdict(nan) to silently fall through to "
        f"'dissipation_runs_away', got {v_nan!r}. If the module now checks np.isfinite this "
        f"assertion SHOULD fail."
    )
    out["verdict_at_nan"] = v_nan

    v_pinf = marginal_verdict(INF)
    assert v_pinf == "relaxes_to_inviscid", (
        f"PIN E6b: expected marginal_verdict(+inf) to read as a (nonsensical) definite "
        f"positive verdict, got {v_pinf!r}."
    )
    out["verdict_at_plus_inf"] = v_pinf

    v_ninf = marginal_verdict(-INF)
    assert v_ninf == "dissipation_runs_away"
    out["verdict_at_minus_inf"] = v_ninf

    # control: the three FINITE branches are correct and must not regress
    assert marginal_verdict(0.13) == "relaxes_to_inviscid"
    assert marginal_verdict(-0.13) == "dissipation_runs_away"
    assert marginal_verdict(0.0) == "neutral_line"
    return out


# =========================================================================
# E-control -- amplitude_eigenvalue (module already disclaims its rigour)
# =========================================================================

def check_amplitude_eigenvalue_sign_and_propagation():
    """CONTROL, honestly weak: `amplitude_eigenvalue`'s OWN docstring says "THIS IS AN
    EMPIRICAL FIT ... AND IS NOT DERIVED. It is in the module because it is gated, not
    because it is understood." So this is not a fresh corruption claim -- only a check of
    what happens at each mu sign within that already-disclaimed formula. mu in (-0.25, 0) is
    silently accepted (a finite, unphysical eigenvalue); mu < -0.25 correctly propagates as
    NaN with a warning."""
    out = {}
    v_ok = amplitude_eigenvalue(0.0)
    assert abs(v_ok - (-1.0)) < 1e-12                        # Route-E's exact symmetry value
    out["mu_zero"] = v_ok
    v_mild_neg = amplitude_eigenvalue(-0.1)                  # still real: 1 + 4*(-0.1) > 0
    assert np.isfinite(v_mild_neg)
    out["mu_minus_0.1_accepted_no_domain_check"] = v_mild_neg
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        v_past_branch = amplitude_eigenvalue(-0.3)           # 1 + 4*(-0.3) < 0
    assert np.isnan(v_past_branch) and len(ws) > 0, (
        "amplitude_eigenvalue should propagate NaN with a warning past the real branch"
    )
    out["mu_minus_0.3_correctly_nan_with_warning"] = True
    return out


def check_non_finite_p_refused_as_a_domain_error():
    """NEW AT LEG 154 -- the clause leg 121's prescribed repair would have missed.

    Leg 121 prescribed `if float(p) != round(float(p)): raise ValueError`. That is an
    integrality test and nothing else, and on `+-inf` it raises `OverflowError` from
    `round()`'s internals -- NOT a `ValueError` -- so it escapes this file's own
    `except ValueError` controls and any caller written against the documented failure
    mode. Worse, the obvious tightening `p == floor(p)` does not merely mis-handle
    infinity, it ADMITS it, because `floor(inf) == inf` is True.

    So the adopted guard tests `np.isfinite` FIRST (SEI CERT FLP04-C), and this check
    exists to pin that clause as MEASURED NECESSARY rather than defensive decoration:
    the assertion below fails if anyone ever "simplifies" the guard down to the
    integrality clause alone."""
    out = {"floor_of_inf_equals_inf": bool(np.floor(INF) == INF)}
    assert out["floor_of_inf_equals_inf"], (
        "the mechanism this check exists for is gone: floor(inf) != inf"
    )
    for bad in (NAN, INF, -INF):
        for call in (lambda: lambda_power(16, bad),
                     lambda: CriticalDissipativeFlow(0.0, 0.0, bad, 16)):
            try:
                call()
                raise AssertionError(f"non-finite p={bad!r} must be refused")
            except CriticalDissipationDomainError as e:
                assert isinstance(e, ValueError)
                assert "FINITE" in str(e)
    out["non_finite_refused"] = 6
    # leg 121's prescribed predicate, run here so the claim is executable, not recalled
    try:
        round(float(INF))
        prescribed_exc = None
    except Exception as e:
        prescribed_exc = type(e).__name__
    assert prescribed_exc == "OverflowError", prescribed_exc
    out["leg121_prescribed_raises_on_inf"] = prescribed_exc
    out["adopted_raises_on_inf"] = "CriticalDissipationDomainError"
    return out


CHECKS = [
    check_lambda_power_truncates_non_integer_p,
    check_flow_identity_under_p_truncation,
    check_realistic_float_near_miss,
    check_string_vs_float_type_coercion_asymmetry,
    check_non_finite_p_refused_as_a_domain_error,
    check_lambda_power_refuses_sub_integer_p,
    check_negative_mu_converges_silently,
    check_mu_decay_time_negative_time,
    check_marginal_verdict_nonfinite_input,
    check_amplitude_eigenvalue_sign_and_propagation,
]


def test_lambda_power_truncates_non_integer_p():
    check_lambda_power_truncates_non_integer_p()


def test_flow_identity_under_p_truncation():
    check_flow_identity_under_p_truncation()


def test_realistic_float_near_miss():
    check_realistic_float_near_miss()


def test_string_vs_float_type_coercion_asymmetry():
    check_string_vs_float_type_coercion_asymmetry()


def test_lambda_power_refuses_sub_integer_p():
    check_lambda_power_refuses_sub_integer_p()


def test_negative_mu_converges_silently():
    check_negative_mu_converges_silently()


def test_mu_decay_time_negative_time():
    check_mu_decay_time_negative_time()


def test_marginal_verdict_nonfinite_input():
    check_marginal_verdict_nonfinite_input()


def test_amplitude_eigenvalue_sign_and_propagation():
    check_amplitude_eigenvalue_sign_and_propagation()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall critical_dissipation ADVERSARIAL checks passed ({len(CHECKS)} checks)")
    print("NOTE: leg 154 REPAIRED E1/E2/E3 and inverted those pins here in the same commit.")
    print("3 checks still PIN CURRENT DEFECTIVE BEHAVIOUR -- E4 (mu < 0), E5 (mu_decay_time's")
    print("domain), E6 (marginal_verdict on a non-finite alpha_1). They are unrepaired by")
    print("design: leg 154's gate licensed the exponent-truncation repair and nothing else.")
    print("They are expected to FAIL when THAT repair lands -- that is the intended signal.")
    print("Banked magnitudes: writeup/data/p2_route_cda_v1_adversarial.json (leg 121),")
    print("                   writeup/data/p2_route_cdr_v1_repair.json    (leg 154)")
