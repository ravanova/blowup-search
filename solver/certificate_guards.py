"""ONE hypothesis guard for every radii-polynomial verdict function in this repository.

WHY THIS MODULE EXISTS (read this before adding a fourth copy)
-----------------------------------------------------------------------------
Three legs, three modules, one defect:

  leg 79   `solver/port_certification.py::radii_polynomial_status`
           11 of 25 hypothesis-violating inputs returned `closes=True`.  Repaired in
           place with a private `_hypothesis_violations`.
  leg 98   `solver/interval_certificate.py::radii_verdict`
           12 of 36, 8 load-bearing.  Repaired in place -- by COPYING leg 79's function,
           with a comment saying so:

               "Mirrors solver.port_certification._hypothesis_violations (leg 79's
                repair) so the two pipelines cannot drift apart on what 'outside the
                theorem' means."

  leg 116  `solver/nk_bounds.py::budget`
           21 of 52, 19 load-bearing, and the sharpest case is not a bookkeeping one: a
           single forbidden `Z_0 = -1` turned an honest REFUSAL at the non-solution
           `x = 1.0` of `F(x) = x^2 - 2` into `closes=True` with `r_min = 0.1917` -- a
           certified ball `[0.8083, 1.1917]` containing no zero of `F` at all, missing
           `sqrt(2)` by 1.161 ball radii.  NOT repaired by leg 116, by its own gate.

The third copy is where a copied guard stops being cheaper than an abstraction (the Rule
of Three; see `writeup/novelty/leg_128.md` for the pass, including the WET
counter-argument that constrains the design).  So the predicate lives here once, and the
two existing call sites delegate to it rather than restating it.

WHAT IS SHARED, AND WHAT IS DELIBERATELY NOT
-----------------------------------------------------------------------------
Shared, because it is the SAME imported theorem in all three: `Y_0`, `Z_0`, `Z_1`, `Z_2`
are upper bounds on norms (van den Berg & Lessard, *Rigorous Numerics in Dynamics*,
Notices AMS 62(9):1057, 2015; Hungria-Lessard-Mireles James, Math. Comp.),

    ||T(x)-x|| <= Y_0 ,     sup ||A(DF(x+rv) - A_dagger)u|| <= Z_0 + Z_1 + Z_2 r ,

hence FINITE and NONNEGATIVE by hypothesis, and the conclusion drawn is existence and
uniqueness of a zero INSIDE the ball of radius `r_min`.  Two consequences, both of which
this module encodes and neither of which is a finding of ours:

  * a negative constant is not a conservative input.  It is an input the theorem says
    nothing about, and evaluating a discriminant on it asserts a contraction on data no
    run could have produced.
  * a `closes=True` carrying a non-positive or non-finite `r_min` is not a conservative
    verdict either.  It asserts a zero inside a degenerate or empty set.

NOT shared, because the three call sites genuinely differ and flattening the differences
would be the wrong abstraction (this is the whole risk the novelty pass flagged):

  * `None` POLICY.  `port_certification` accepts `None` in any slot -- `None` means NOT
    MEASURED and is the entire point of its `BLOCKED_AT_STEP_ONE` kill-switch.
    `interval_certificate` and `nk_bounds` have no not-measured branch and must raise.
    Carried by `allow_none`.
  * THE NaN PARENTHETICAL.  The three modules guard the contraction in different senses
    (`Z_1 >= 1.0` rejects, `Z_1 < 1.0` accepts, `Z_0 + Z_1 < 1.0` accepts), so the
    comparison a NaN slips past is a different one in each.  Carried by `nan_hint`, and
    the two existing hints are reproduced BYTE-FOR-BYTE (`NAN_HINT_GE_ONE`,
    `NAN_HINT_LT_ONE`) so that no message any test or artifact quotes moves.
  * THE SLOTS.  `nk_bounds.budget` has a fourth constant, `Z_0`, that the other two do
    not.  Carried by passing the (name, value) pairs in, rather than a fixed signature.

WHAT THIS MODULE MAY AND MAY NOT DO
-----------------------------------------------------------------------------
It is a REJECTION layer.  It may turn something that used to be accepted into a refusal.
It may NEVER change a number that a hypothesis-satisfying input already produced.  That
is not a style preference -- it is leg 128's gate condition, and any clean-input result
moving is a stop-and-escalate.

Plain float64 and pure Python: no numpy, no solver imports, so nothing in the certificate
stack can acquire an import cycle through its own guard.
"""

import math
import numbers

# The NaN parentheticals, verbatim from the two in-place repairs they replace.  They are
# module constants rather than string literals at the call sites precisely so that the
# next person to add a call site has to CHOOSE one, and so that a diff to either is
# visible here rather than buried in a verdict function.
NAN_HINT_GE_ONE = ("note that `NaN >= 1.0` is False, so an unguarded NaN would slip past "
                   "the contraction test")
NAN_HINT_LT_ONE = ("note that `NaN < 1.0` is False, so the contraction guard alone is not "
                   "a hypothesis check")
NAN_HINT_SUM_LT_ONE = ("note that `NaN < 1.0` is False, so the contraction test "
                       "`Z_0 + Z_1 < 1` alone is not a hypothesis check")

#: The sentence every caller prefixes its rejection with, so the three pipelines cannot
#: drift apart on what "outside the theorem" is called either.
INVALID_INPUT_PREFIX = ("INVALID_INPUT: outside the hypotheses of the radii polynomial "
                        "theorem (Y_0, Z_1, Z_2 are upper bounds on norms, hence finite "
                        "and nonnegative): ")


def hypothesis_violations(constants, allow_none=False, nan_hint=NAN_HINT_GE_ONE):
    """Which hypothesis of the radii polynomial theorem each supplied constant breaks.

    `constants` is an ordered iterable of `(name, value)` pairs -- ordered, because the
    returned list is quoted in artifacts and a reordering would look like a change.
    Returns a list of strings naming the offending constant and the hypothesis it breaks;
    an EMPTY list means every constant is admissible.

    `0.0` and `-0.0` are legitimate bounds and are NOT violations.  A zero `Z_2` is a
    DEGENERACY of the polynomial (it stops being a quadratic), which each caller names and
    handles for itself -- it is not a hypothesis failure and is deliberately not one here.

    `allow_none=True` treats `None` as NOT MEASURED and skips it, which is
    `port_certification`'s kill-switch semantics; with `allow_none=False` a `None` reaches
    the type check and raises, which is what the other two callers want.

    Raises `TypeError` on a non-real value: a constant that is not a number is a caller
    bug, not a fabricated bound, and must not be laundered into a `closes=False`.
    """
    bad = []
    for name, v in constants:
        if v is None and allow_none:
            continue
        if not isinstance(v, numbers.Real):
            raise TypeError(f"{name} must be a real number{' or None' if allow_none else ''}"
                            f", got {type(v).__name__}; the radii polynomial's constants "
                            f"are norms.")
        f = float(v)
        if math.isnan(f):
            bad.append(f"{name} is NaN (a norm bound cannot be NaN; {nan_hint})")
        elif math.isinf(f):
            bad.append(f"{name} is {'+' if f > 0 else '-'}infinite (a norm bound is finite "
                       f"by hypothesis)")
        elif f < 0.0:
            bad.append(f"{name} is negative ({f!r}); it is an upper bound on a norm")
    return bad


def invalid_input_reason(violations):
    """The rejection sentence, assembled once so the three pipelines phrase it alike."""
    return INVALID_INPUT_PREFIX + "; ".join(violations) + ". No discriminant is evaluated."


def radius_violation(r_min):
    """Why `r_min` cannot be the radius of a ball the theorem concludes a zero lives in.

    Returns a string, or `None` if `r_min` is an admissible radius.  The theorem's
    conclusion is existence and uniqueness of a zero INSIDE the ball of radius `r_min`, so
    a non-positive or non-finite `r_min` is not a conservative verdict -- it asserts a zero
    inside a degenerate or empty set.  Leg 116 measured 14 such "certificates" in
    `nk_bounds.budget` alone.

    Note what this is NOT: it is not a claim that `r_min = 0` is arithmetically wrong.  It
    is the observation that the CONCLUSION being drawn has no content there, so reporting
    it in the same slot as a real radius is the fabrication.
    """
    f = float(r_min)
    if math.isnan(f):
        return "r_min is NaN, so no ball was established"
    if math.isinf(f):
        return "r_min is infinite, so no finite ball was established"
    if f <= 0.0:
        return (f"r_min is {f!r} <= 0: the theorem concludes a zero INSIDE the ball of "
                f"radius r_min, and a degenerate or empty ball contains none")
    return None


def unit_range_violation(name, value, lo, hi, lo_open=True, hi_open=False):
    """Why `value` is outside the half-open range a Holder-type exponent must live in.

    Returns a string, or `None`.  Shared because two of the three modules carry exponent
    hypotheses in their docstrings that the code did not check -- `nk_bounds`'s
    `gamma in (0, 1]` and `alpha < 2` -- and the failure mode is identical to the constants
    one: the docstring states the hypothesis, the code evaluates anyway.
    """
    f = float(value)
    if math.isnan(f):
        return f"{name} is NaN"
    lo_bad = (f <= lo) if lo_open else (f < lo)
    hi_bad = (f >= hi) if hi_open else (f > hi)
    if lo_bad or hi_bad:
        l, r = ("(" if lo_open else "["), (")" if hi_open else "]")
        return f"{name} is {f!r}, outside the required range {l}{lo}, {hi}{r}"
    return None


def positive_weight_violations(name, values, allow_zero=False):
    """Why a weight/kernel array is not one a norm could have produced.

    Returns a list of strings.  A weight vector DEFINES a norm, so it is strictly positive
    and finite; a seminorm kernel is non-negative with zeros only where the suppressed term
    is genuinely zero.  Leg 116 measured `two_point_dual` silently DROPPING non-positive
    entries (`1/q if q > 0 else 0`), which prices an honestly-infinite contribution at
    zero and dropped the claimed upper bound 2.19x / 3.57x below the honest one.

    Takes any iterable of floats (a flattened array is fine); reports counts and the worst
    offender rather than every index, so the message stays quotable.
    """
    vals = [float(v) for v in values]
    n_nan = sum(1 for v in vals if math.isnan(v))
    n_inf = sum(1 for v in vals if math.isinf(v))
    finite = [v for v in vals if not (math.isnan(v) or math.isinf(v))]
    threshold = 0.0
    n_bad = sum(1 for v in finite if (v < threshold if allow_zero else v <= threshold))
    bad = []
    if n_nan:
        bad.append(f"{name} has {n_nan} NaN entr{'y' if n_nan == 1 else 'ies'}")
    if n_inf:
        bad.append(f"{name} has {n_inf} infinite entr{'y' if n_inf == 1 else 'ies'}")
    if n_bad:
        worst = min(v for v in finite if (v < threshold if allow_zero else v <= threshold))
        rel = "negative" if allow_zero else "non-positive"
        bad.append(f"{name} has {n_bad} {rel} entr{'y' if n_bad == 1 else 'ies'} "
                   f"(worst {worst!r}); a weight defines a norm, so it is strictly "
                   f"positive and finite")
    return bad
