"""The first integral of the two-scale equation, and the profile on its own support.

Thirteen Route-D legs treated the gCLM two-scale (traveling-wave) profile equation

    R = Omega H(Omega) - c Omega_X - a U Omega_X ,     U(X) = int_0^X H(Omega) dX'

as a nonlinear integro-differential equation to be discretized on the whole line and
inverted.  It is not one.  Write E = c + a U for the effective transport coefficient
that v12 introduced; then E_X = a H(Omega) exactly, so on any interval where Omega
does not vanish

    R = 0   <=>   Omega E_X / a = E Omega_X   <=>   (log|Omega|)_X = (1/a) (log E)_X

and therefore

    |Omega| = C E^{1/a}                                                        (FI)

with C a constant of integration.  The amplitude gauge Omega(0) = -1 fixes it: at
X = 0, U = 0 and E = c, so C = c^{-1/a} and

    Omega(X) = - ( E(X) / c )^{1/a} ,    E = c + a U ,    U_X = H(Omega) .      (FI')

That is an exact first integral of the profile equation, and every structural fact
this project has spent three legs measuring falls out of it in one line:

  * `a -> 0`:  (1 + aU/c)^{1/a} -> exp(U/c), so Omega = -exp(U/c).  On the anchor
    U = -(1/2)log(1+X^2), c = 1/2, giving Omega = -1/(1+X^2) EXACTLY.  The known
    solution is the degenerate limit of (FI'), which is gate 2.
  * THE PROFILE ENDS, and it is forced rather than assumed.  E is decreasing
    (E_X = a H(Omega) < 0 for X > 0 whenever Omega is negative and unimodal), so E
    reaches zero at a finite X_c; beyond it E < 0 and E^{1/a} is not real, so
    Omega == 0.  v12 discovered the support edge by measuring a sign change; here it
    is a consequence of the equation.
  * THE ZERO HAS ORDER 1/a, with the amplitude explicit.  E vanishes linearly at X_c
    (E_X(X_c) = a H(Omega)(X_c) != 0), so Omega ~ -(a|h_c|/c)^{1/a} (X_c - X)^{1/a}.
    v12 derived the exponent from a leading balance; (FI) gives exponent AND constant.
  * THE PROFILE IS ONLY FINITELY SMOOTH.  Omega is C^{floor(1/a)} at X_c and no
    better, so it is a classical solution exactly while a < 1 -- and the regularity
    DEGRADES as a grows, which is why a global spectral basis on the whole line has
    more trouble at large a, not less (see the `a*` note below).

--------------------------------------------------------------------------
THE REDUCED SYSTEM (what this module actually solves)
--------------------------------------------------------------------------
(FI') turns a problem for Omega on the whole line into a scalar problem for E on its
own support.  Scale by the support radius, v = X / X_c, and write e(v) = E(X_c v)/c.
Since the finite Hilbert transform is scale invariant, X_c drops out of H and the
whole system is

    c e'(v) + a X_c Hpv[ e^{1/a} ](v) = 0 ,    e(0) = 1 ,   e(1) = 0 ,          (RS)

    Hpv[w](v) = (1/pi) p.v. int_{-1}^{1} w(|u|) / (v - u) du .

c enters only as a scale (dilation sends X_c -> mu X_c, c -> mu c and leaves e alone),
so the module fixes c = 1 and every radius it reports is the invariant X_c / c.

Two things about (RS) are worth saying out loud, because they are why this converges
where a direct discretization of R did not:

  1. **e(1) = 0 goes in the ANSATZ, not in an extra row.**  e = (1 - v^2) s(v) with s
     an even Chebyshev series.  The support edge is then exact by construction and the
     order-1/a zero of Omega = -e^{1/a} is an OUTPUT, not something a grid has to
     resolve and not something put in by hand.
  2. **The edge row is non-degenerate.**  The raw residual R is identically zero at
     X_c -- every term carries Omega or Omega_X, both of which vanish there -- so a
     collocation row at the edge carries no information and a direct build has to
     append an ad-hoc free-boundary condition.  (RS) has c e'(1) = -a X_c Hpv[w](1)
     with both sides nonzero.  The free boundary is priced by the equation itself.
  solver/finite_support.py is the direct build; it never converged.

--------------------------------------------------------------------------
THE KILL SWITCH (state the meaning before running it)
--------------------------------------------------------------------------
v12 measured that the gauged inverse of the whole-line system DIVERGES with the
discretization at the a > 0 profile (J^+2.86 at a = 0.2) while being flat at the a = 0
anchor, and v13 attributed that to a mode growing like (log X)^{1/a} OUTSIDE X_c,
against a domain space that is a decay class -- a codimension-1 range obstruction that
no refinement and no bordering-with-a-symmetry can touch.  The repair v13 named was to
take the far field out of the DOMAIN.  (RS) does exactly that: its unknowns are
(s, X_c) and its perturbations live on [0, X_c] only, so the growing mode has nowhere
to live.  `operator_norm` measures ||A|| = ||M^{-1}|| against the number of modes.
FLAT means the framing was the problem and the object is fine.  STILL DIVERGENT means
the framing needs replacing.

--------------------------------------------------------------------------
A NOTE ON a* (do not let this get overstated)
--------------------------------------------------------------------------
v11 read a grid-refinement spread at a = 0.8, 1.0 on the whole-line Newton solve as
"the solutions are continuum objects only up to a ~ 0.5", and banked it as a fourth
confirmation of the survival boundary a* ~ 0.5-0.55.  On (RS) the same object is grid
converged to ten significant figures at a = 0.6, 0.8, 1.0 and 1.2.  The spread was the
whole-line basis failing to represent a compactly supported profile whose edge
regularity is C^{1/a} and therefore gets WORSE as a grows -- an instrument artifact of
exactly the family v12's ringing belongs to.  What that retires is v11's argument, not
a*: the other three confirmations are about the two-scale GA problem, which is a
different question, and this module says nothing about them.

--------------------------------------------------------------------------
THE SUPPORT GUARD (added by a bench repair, after leg 107 / Route-FIA)
--------------------------------------------------------------------------
Leg 107 audited this module adversarially and answered its gate **YES, on two
independent sites** (`experiments/journal/leg_107.md`):

  * **Finding A.**  `omega_of` computed `-|e|^{1/a}`, and the `abs` erased the branch cut
    that is the entire reason the profile HAS compact support.  96 of 96 evaluations at
    `v = X/X_c > 1` came back finite, nonzero and inside the profile's own gauge range
    `|Omega| <= 1`, where the docstring twelve lines above says the answer is EXACTLY
    ZERO -- 0 exceptions, 0 NaNs, 0 warnings.  At `a = 0.5`, `omega_of` at twice the
    support radius returned -0.814, i.e. 81% of the peak amplitude.  Worse, a grid
    overshooting `X_c` by 1% got the interior mirror value back to 3-4 significant
    figures, so magnitude alone could not tell a caller it was out of domain.
    Riding along: `even_cheb` clipped `v` into `[-1, 1]` before `arccos`, freezing
    `s(v)` at `s(1)` for every `v > 1`, while `e_of` kept the UNCLIPPED `(1 - v^2)`
    prefactor -- the two halves of `e(v)` described different points, and the result
    overstated the true `|E|` (against this module's own `outer_velocity` quadrature)
    by 1.56x at `v = 1.5` rising to 22.0x at `v = 10`.

  * **Finding B.**  `first_integral_defect`'s default mask was
    `(|Omega| > 1e-11) & (E > 1e-8)`.  Every ordered comparison against NaN is false
    (IEEE-754 §5.11), so a NaN-poisoned point LEFT the sample instead of poisoning the
    answer: **397 of 400 points could be NaN and the identity was still certified to
    1.33e-15**, with the number getting BETTER as the poisoning got worse.  The flag at
    398 was the pre-existing `< 3 survivors` arity guard, not poison detection.

Both were latent -- 0 of 3 `omega_of` and 0 of 2 `first_integral_defect` call sites in
the repo evaluate in the affected region -- so nothing banked was contaminated, and this
repair is required to prove exactly that by leaving every in-support number alone.

The repair follows the template merged earlier this session for the same bug class in
`solver/target_norm.py` (silent domain extrapolation): **a named warning class, a
DYNAMIC threshold, propagation into the returned value, warn-not-raise by default, and a
strict mode.**  Where it departs from that template it is because it can afford to:

  * **The threshold is not a tuned constant.**  `|v| > 1 + 4 eps` and `e < 0` are the
    DEFINITION of leaving the support (`v = X/X_c`, and `E = c(1 - ...)` changes sign at
    `X_c`), not a tolerance anyone picked.  `e == 0` is the support EDGE and is inside:
    the true value there is zero and `-|0|^p` already returns it, so the edge is left
    bit-for-bit alone, including the sign of the zero.
  * **The answer outside is KNOWN, so the guard returns it.**  `target_norm`'s guard can
    only flag, because the out-of-window answer there is unknowable.  Here the module's
    own docstring supplies it: `Omega == 0`.  So `omega_of`'s default is
    `on_outside="zero"` -- the TRUE value, plus a `FirstIntegralSupportWarning` -- and
    not `"nan"`, because NaN would be a refusal to answer a question this module can
    answer.  `e_of` defaults to `"nan"` instead, because `E` outside the support is
    negative and NOT representable by the interior ansatz `e = (1 - v^2) s(v)`: the
    module genuinely does not know it, and says so.
  * **NaN still wins.**  A non-finite `e` (e.g. from a poisoned coefficient) is NEVER
    rewritten to 0.0.  The `e < 0` rule fires only where `e` is finite, so the 20-probe
    NaN-propagation property leg 107 verified is preserved exactly.
  * **`on_outside="extrapolate"`** reproduces the pre-repair arithmetic bit-for-bit,
    still with the warning, so leg 107's own battery can keep MEASURING the gap it
    escalated.  An unconditional raise would have made that audit unrunnable.
  * **`on_outside="raise"`**, or `warnings.simplefilter("error",
    FirstIntegralGuardWarning)`, is the strict mode for callers who want it fatal.
  * **`first_integral_defect` no longer drops what it cannot see.**  Non-finite points
    anywhere in `Omega` or `U` are counted BEFORE any mask is applied, and the default
    `on_nonfinite="nan"` refuses to certify the sample.  `detail=True` returns the full
    census (`n_points`, `n_nonfinite`, `n_used`, `sample_valid`) so a caller can report
    the surviving count rather than a bare number.

**The Newton path is deliberately untouched.**  `residual`, `jacobian`, `solve` and
`operator_norm` still use `|e|^{1/a}`, because where the equation is ENFORCED the `abs`
cannot hide anything: leg 107 measured the residual on a sign-flipped state at 4.5e14x
the clean one, and `solve`'s line search already refuses any step with `min e <= 0`.
Guarding them would change the objective the banked `X_c`, `||A||` and edge exponents
were computed from, which is precisely what a repair of a latent bug must not do.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import warnings

import numpy as np


# ---------------------------------------------------------------------------
# the support guard
# ---------------------------------------------------------------------------

#: `v = X / X_c`, so the support is EXACTLY `|v| <= 1` -- this is a definition, not a
#: tuning knob.  The slack is four ulps, enough to absorb a caller who reached `v = 1`
#: by arithmetic (`1.0 - s` with `s` from a geomspace, `X / Xc` with a rounded `Xc`)
#: and not enough to admit any point a caller meant to be outside.
SUPPORT_TOL = 4.0 * np.finfo(float).eps

_OUTSIDE_POLICIES = ("zero", "nan", "extrapolate", "raise")


class FirstIntegralGuardWarning(UserWarning):
    """Base class for both guards, so one filter catches the whole family."""


class FirstIntegralSupportWarning(FirstIntegralGuardWarning):
    """The profile was evaluated where it does not exist.

    Leg 107 measured what that used to cost: 96 of 96 out-of-support evaluations
    returned a finite, in-gauge-range value where the truth is exactly 0, and within 1%
    of `X_c` the fabricated value agreed with the legitimate mirror value to better than
    5e-2 relative.  The warning does not say the returned number is wrong -- with the
    default policy it is now RIGHT, and equal to zero -- it says the caller asked outside
    the support, which is almost always an off-by-one at the free boundary or an `X_c`
    that moved between a solve and a later evaluation.
    """


class FirstIntegralSampleWarning(FirstIntegralGuardWarning):
    """`first_integral_defect` was handed a sample containing non-finite points.

    Before the repair those points left the sample silently: 397 of 400 could be NaN and
    the identity was still certified to 1.33e-15.
    """


def support_fields(n_outside, n_points, max_abs_v=None):
    """The keys every support-aware return in this module carries, uniformly.

    `support_valid` is True (clean) / False (some point left the support) / None (the
    caller did not supply points, so there is nothing to check).  `None` is FALSY on
    purpose, exactly as in `solver/target_norm.py`'s `domain_fields`: a caller writing
    `if not d["support_valid"]` errs toward distrust rather than toward silence.
    """
    if n_outside is None:
        return {"n_points": int(n_points), "n_outside_support": None,
                "frac_outside_support": None, "support_valid": None,
                "max_abs_v": None}
    n_outside, n_points = int(n_outside), int(n_points)
    return {"n_points": n_points, "n_outside_support": n_outside,
            "frac_outside_support": (float(n_outside) / n_points if n_points else 0.0),
            "support_valid": bool(n_outside == 0),
            "max_abs_v": (None if max_abs_v is None else float(max_abs_v))}


def sample_fields(n_points, n_nonfinite, n_used):
    """The census `first_integral_defect` reports instead of dropping points in silence."""
    n_points, n_nonfinite, n_used = int(n_points), int(n_nonfinite), int(n_used)
    return {"n_points": n_points, "n_nonfinite": n_nonfinite, "n_used": n_used,
            "frac_nonfinite": (float(n_nonfinite) / n_points if n_points else 0.0),
            "sample_valid": bool(n_nonfinite == 0 and n_used >= 3)}


def _check_policy(on_outside, allowed=_OUTSIDE_POLICIES):
    if on_outside not in allowed:
        raise ValueError(f"on_outside must be one of {allowed!r}, got {on_outside!r}")


def _signal_outside(n_outside, n_points, where, on_outside, max_abs_v, why):
    """Raise or warn.  Called ONLY when `n_outside > 0`, so the clean path is untouched.

    That "only" is the zero-regression property in one sentence: with no point outside
    the support this function is never entered, no filter is consulted, and the arithmetic
    below it is the pre-repair arithmetic verbatim.
    """
    msg = (f"first_integral.{where}: {n_outside} of {n_points} evaluation point(s) lie "
           f"OUTSIDE the profile's own compact support ({why}"
           + (f"; max |v| = {max_abs_v:.6g}" if max_abs_v is not None else "")
           + f").  The module's own docstring says Omega == 0 there, so the pre-repair "
             f"answer was wrong by its full magnitude (leg 107: 96/96 such evaluations "
             f"returned a finite in-range value).  Policy on_outside={on_outside!r}.")
    if on_outside == "raise":
        raise ValueError(msg)
    warnings.warn(msg, FirstIntegralSupportWarning, stacklevel=3)


# ---------------------------------------------------------------------------
# quadrature
# ---------------------------------------------------------------------------


def gauss_legendre(n):
    """(nodes, weights) of the n-point Gauss-Legendre rule on [-1, 1].

    Newton on P_n from the standard Chebyshev initial guess.  Hand-rolled because
    the project has no scipy; gated against exact polynomial moments.
    """
    n = int(n)
    x = np.cos(np.pi * (np.arange(1, n + 1) - 0.25) / (n + 0.5))
    for _ in range(100):
        p0, p1 = np.ones_like(x), x.copy()
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1.0)
        dx = -p1 / dp
        x = x + dx
        if np.max(np.abs(dx)) < 1e-15:
            break
    p0, p1 = np.ones_like(x), x.copy()
    for k in range(2, n + 1):
        p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
    dp = n * (x * p1 - p0) / (x * x - 1.0)
    return x, 2.0 / ((1.0 - x * x) * dp * dp)


def graded_grid(levels=20, order=20):
    """Composite Gauss-Legendre on [-1, 1], panels graded geometrically to +-1.

    The integrands here are analytic in (-1, 1) with an algebraic branch point of
    order 1/a at each endpoint, which is precisely what geometric grading is for:
    the error falls like 2^{-levels*(1/a + 1)}.  At the orders this project needs
    (1/a >= 2) that is machine precision by `levels` ~ 8; the default is set by the
    much harsher sqrt endpoint of the exact gate family (test 1).
    """
    xg, wg = gauss_legendre(order)
    br, h = [0.0], 1.0
    for _ in range(int(levels)):
        h *= 0.5
        br.append(1.0 - h)
    br.append(1.0)
    br = np.asarray(br)
    br = np.concatenate([-br[::-1], br[1:]])
    lo, hi = br[:-1], br[1:]
    mid, half = 0.5 * (lo + hi), 0.5 * (hi - lo)
    return ((mid[:, None] + half[:, None] * xg[None, :]).ravel(),
            (half[:, None] * wg[None, :]).ravel())


def _even_cheb_raw(K, v):
    """The pre-repair body, verbatim and unguarded.  Not for direct use.

    Kept as its own function so that the guarded `even_cheb` below is provably ADDITIVE:
    on a clean call it does nothing but forward to this, so no in-support number can move.
    The `np.clip` stays because it has a legitimate job -- the REMOVABLE endpoints
    `v = +-1`, which a caller reaches by arithmetic and where `arccos` of `1 + 2e-16`
    would otherwise be NaN.  What it must not do is stand in for a domain check, which is
    what leg 107 measured it doing.
    """
    v = np.atleast_1d(np.asarray(v, float))
    n = 2 * np.arange(int(K))
    th = np.arccos(np.clip(v, -1.0, 1.0))
    T = np.cos(np.outer(th, n))
    s = np.sin(th)
    with np.errstate(divide="ignore", invalid="ignore"):
        dT = n[None, :] * np.sin(np.outer(th, n)) / s[:, None]
    bad = ~np.isfinite(dT)
    if bad.any():                       # the removable endpoints v = +-1
        dT[bad] = np.broadcast_to((n ** 2).astype(float), dT.shape)[bad]
    return T, dT


def _outside_mask(v):
    """(mask, count, max|v|) for the points that left the scaled support |v| <= 1.

    NaN is NOT outside: `np.abs(nan) > x` is false, so a NaN `v` flows through to a NaN
    result and propagates, which is the behaviour leg 107 verified and this repair keeps.
    """
    out = np.abs(v) > 1.0 + SUPPORT_TOL
    n = int(np.count_nonzero(out))
    mx = float(np.max(np.abs(v))) if v.size else 0.0
    return out, n, mx


def even_cheb(K, v, on_outside="nan"):
    """(T_{2k}(v), d/dv T_{2k}(v)) for k = 0..K-1; shapes (len(v), K).

    Guarded (leg 107, finding A, second half).  The basis is the interior basis of the
    scaled support `|v| <= 1`; for `|v| > 1` the pre-repair code silently evaluated at
    `v = 1` (measured: `max |T_2k(v) - T_2k(1)| = 0.0` over `v` in {1.5, 3, 50}) and
    `e_of` then multiplied that frozen value by an unclipped `(1 - v^2)`.

    `on_outside` is one of:
      * `"nan"` (default) -- rows outside become NaN, and a `FirstIntegralSupportWarning`
        is raised.  NaN and not 0, because `T_2k` is not zero out there; the module simply
        has no business evaluating it there.
      * `"extrapolate"` -- the pre-repair clipped value, still warned about, so leg 107's
        battery can keep measuring the gap.
      * `"zero"` -- rows outside become 0.0 (accepted for signature uniformity with
        `omega_of`; it is the right answer for `Omega`, not for `T`, so prefer `"nan"`).
      * `"raise"` -- ValueError instead of a warning.
    """
    _check_policy(on_outside)
    v = np.atleast_1d(np.asarray(v, float))
    out, n_out, mx = _outside_mask(v)
    if n_out:
        _signal_outside(n_out, v.size, "even_cheb", on_outside, mx,
                        "the even-Chebyshev basis is only the interior basis of "
                        "|v| <= 1, and np.clip would freeze every such point at v = 1")
    T, dT = _even_cheb_raw(K, v)
    if n_out and on_outside in ("nan", "zero"):
        fill = np.nan if on_outside == "nan" else 0.0
        T[out, :] = fill
        dT[out, :] = fill
    return T, dT


def hilbert_pv(u, w, f_u, f_v, v):
    """(1/pi) p.v. int_{-1}^{1} f(u)/(v-u) du by ONE subtraction.

        p.v. int f(u)/(v-u) du = int [f(u) - f(v)]/(v-u) du + f(v) log((1+v)/(1-v))

    using p.v. int_{-1}^{1} du/(v-u) = log((1+v)/(1-v)) exactly.  `f_u` is f at the
    quadrature nodes, `f_v` at the evaluation points.  Linear in f, which is what
    makes the analytic Jacobian below a matrix product rather than a re-quadrature.
    """
    v = np.atleast_1d(np.asarray(v, float))
    d = v[:, None] - u[None, :]
    return ((((f_u[None, :] - f_v[:, None]) / d) @ w)
            + f_v * np.log((1.0 + v) / (1.0 - v))) / np.pi


# ---------------------------------------------------------------------------
# the reduced profile
# ---------------------------------------------------------------------------


class ReducedProfile:
    """(RS) on [0, 1]: unknowns (b, X_c) with e = (1 - v^2) sum_k b_k T_{2k}(v).

    `K` even Chebyshev modes against K collocation nodes plus the amplitude gauge
    s(0) = 1, so the system is square at K + 1.  Everything that does not depend on
    the unknowns is assembled once in __init__; a Newton step is then matrix algebra.
    """

    def __init__(self, a, K=64, levels=20, order=20, c=1.0):
        if not 0.0 < float(a):
            raise ValueError("a must be positive; a = 0 is the degenerate limit "
                             "(Omega = -exp(U/c), X_c = infinity) and has no support")
        self.a, self.K, self.c = float(a), int(K), float(c)
        self.p = 1.0 / float(a)                      # the zero order, an OUTPUT
        self.u, self.w = graded_grid(levels, order)
        # nodes cluster at v = 1, which is where the branch point is
        self.v = np.cos(np.pi * (np.arange(self.K) + 0.5) / (2 * self.K))
        Tu, _ = even_cheb(self.K, self.u)
        self.PHI_u = (1.0 - self.u ** 2)[:, None] * Tu             # de/db at nodes
        Tv, dTv = even_cheb(self.K, self.v)
        self.PHI_v = (1.0 - self.v ** 2)[:, None] * Tv
        self.dPHI_v = (-2.0 * self.v[:, None] * Tv
                       + (1.0 - self.v ** 2)[:, None] * dTv)
        self.L = np.log((1.0 + self.v) / (1.0 - self.v))
        self.W = self.w[None, :] / (self.v[:, None] - self.u[None, :])
        self.Wsum = self.W.sum(axis=1)
        self.g0 = even_cheb(self.K, np.array([0.0]))[0][0]         # T_{2k}(0)

    # -- fields ------------------------------------------------------------
    def _e_raw(self, b, v):
        """e(v) = (1 - v^2) s(v), UNGUARDED.  The pre-repair arithmetic, verbatim."""
        if v is None:
            return self.PHI_v @ b
        T, _ = _even_cheb_raw(self.K, v)
        return (1.0 - np.asarray(v, float) ** 2) * (T @ b)

    def e_of(self, b, v=None, on_outside="nan", detail=False):
        """e(v) = (1 - v^2) s(v); at the collocation nodes when v is None.

        Guarded (leg 107, finding A).  Outside `|v| <= 1` the true `E` is NEGATIVE and
        grows like `(a m / pi) log(X / X_c)` (`solver/turning_point.py`), which the
        interior ansatz cannot represent: leg 107 measured the extrapolated `e`
        overstating the true `|E|` by 1.557x at `v = 1.5` and 22.008x at `v = 10`.  So
        the default is `"nan"` -- the module does not know, and says so -- rather than a
        number.  `on_outside="extrapolate"` returns the pre-repair value with a warning.

        `detail=True` returns `{"e": <array>, **support_fields(...)}` instead of the bare
        array, so a caller can record the provenance of the values it just took.  The
        collocation-node branch (`v is None`) reports `support_valid=None`: those nodes
        are interior by construction, and there is no caller-supplied `v` to check.
        """
        _check_policy(on_outside)
        if v is None:
            e = self.PHI_v @ b
            return ({"e": e, **support_fields(None, e.size)} if detail else e)
        vv = np.atleast_1d(np.asarray(v, float))
        out, n_out, mx = _outside_mask(vv)
        if n_out:
            _signal_outside(n_out, vv.size, "e_of", on_outside, mx,
                            "E < 0 beyond X_c and the interior ansatz e = (1-v^2)s(v) "
                            "does not represent it")
        e = self._e_raw(b, v)
        if n_out and on_outside in ("nan", "zero"):
            e = np.where(out, np.nan if on_outside == "nan" else 0.0, e)
        if detail:
            return {"e": e, **support_fields(n_out, vv.size, mx)}
        return e

    def _outside_support(self, e, out_v):
        """Where the profile does not exist: past the free boundary, or where E < 0.

        Two independent statements of the SAME structural fact, both taken from the
        module's own docstring rather than chosen:

          * `|v| > 1` -- the scaled support radius, by the definition `v = X / X_c`;
          * `e < 0`   -- the branch cut.  `E` decreases and reaches zero at `X_c`;
            beyond it `E^{1/a}` is not real, so `Omega == 0`.

        `e == 0` is the support EDGE and counts as INSIDE: the true value there is zero
        and `-|0|^p` already returns it, so this rule leaves the edge bit-for-bit alone
        (including the sign of the zero, which matters because one banked call site
        samples `v = linspace(0, 1, 401)` and hits `v = 1` exactly).

        A non-finite `e` is never "outside": NaN must propagate, not be rewritten to a
        clean 0.0.  That is why the test is `np.isfinite(e) & (e < 0.0)` and not `~(e >= 0)`.
        """
        return out_v | (np.isfinite(e) & (e < 0.0))

    def omega_of(self, b, v=None, on_outside="zero", detail=False):
        """Omega = -(e)^{1/a} -- the profile itself, on the scaled support.

        Guarded (leg 107, finding A).  The pre-repair body was `-np.abs(e) ** p`, and the
        `abs` erased the branch cut that is the whole reason this profile has compact
        support: past `X_c` it returned a finite, in-range, mirror-plausible number where
        the truth is exactly 0.

        `on_outside`:
          * `"zero"` (default) -- return the TRUE value, `0.0`, and raise a
            `FirstIntegralSupportWarning`.  This module knows the answer outside its
            support; refusing to give it would be a worse repair than giving it.
          * `"nan"` -- refuse instead, for callers who would rather see the poison.
          * `"extrapolate"` -- the pre-repair number, still warned about.
          * `"raise"` -- ValueError.

        `detail=True` returns `{"Omega": <array>, **support_fields(...)}`.
        """
        _check_policy(on_outside)
        if v is None:
            vv, out_v, mx = None, np.zeros(self.K, bool), None
        else:
            vv = np.atleast_1d(np.asarray(v, float))
            out_v, _, mx = _outside_mask(vv)
        e = self._e_raw(b, v)
        om = -np.abs(e) ** self.p
        outside = self._outside_support(e, out_v)
        n_out = int(np.count_nonzero(outside))
        n_pts = int(e.size)
        if n_out:
            _signal_outside(n_out, n_pts, "omega_of", on_outside, mx,
                            "Omega == 0 wherever E <= 0; the pre-repair -|e|^{1/a} "
                            "erased that branch cut")
        if n_out and on_outside in ("zero", "nan"):
            om = np.where(outside, 0.0 if on_outside == "zero" else np.nan, om)
        if detail:
            return {"Omega": om, **support_fields(n_out, n_pts, mx)}
        return om

    def _w_of(self, b, where, on_outside="zero"):
        """|Omega| = e^{1/a} at the quadrature nodes, with the branch cut restored.

        The integrands of `mass` and `outer_velocity` are `|Omega|`, so they carried the
        same erased branch cut as `omega_of`.  On a converged profile `e > 0` at every
        node and this is the pre-repair expression unchanged; on a state that has left the
        support it stops integrating a fabricated `|e|^{1/a}` over a region where the
        profile is zero.
        """
        e = self.PHI_u @ b
        w = np.abs(e) ** self.p
        outside = self._outside_support(e, np.zeros(e.shape, bool))
        n_out = int(np.count_nonzero(outside))
        if n_out:
            _signal_outside(n_out, int(e.size), where, on_outside, None,
                            "e < 0 at quadrature nodes: the profile is identically zero "
                            "there, so |Omega| must not be integrated as |e|^{1/a}")
            if on_outside in ("zero", "nan"):
                w = np.where(outside, 0.0 if on_outside == "zero" else np.nan, w)
        return w

    # -- the system --------------------------------------------------------
    def residual(self, b, Xc):
        """[ c e' + a X_c Hpv[e^{1/a}] at the K nodes ;  s(0) - 1 ]."""
        eu, ev = self.PHI_u @ b, self.PHI_v @ b
        wu, wv = np.abs(eu) ** self.p, np.abs(ev) ** self.p
        F = np.empty(self.K + 1)
        F[:self.K] = (self.c * (self.dPHI_v @ b)
                      + self.a * Xc * hilbert_pv(self.u, self.w, wu, wv, self.v))
        F[self.K] = float(self.g0 @ b) - 1.0
        return F

    def jacobian(self, b, Xc):
        """d(residual)/d(b, X_c), analytic; (K+1, K+1).

        Hpv is linear in its argument, so d Hpv[w] / db = Hpv[ dw/db ] with
        dw/db_k = (1/a) e^{1/a - 1} phi_k -- one matrix product, no re-quadrature.
        """
        eu, ev = self.PHI_u @ b, self.PHI_v @ b
        wu, wv = np.abs(eu) ** self.p, np.abs(ev) ** self.p
        dWu = (self.p * np.abs(eu) ** (self.p - 1.0))[:, None] * self.PHI_u
        dWv = (self.p * np.abs(ev) ** (self.p - 1.0))[:, None] * self.PHI_v
        dH = ((self.W @ dWu) - self.Wsum[:, None] * dWv
              + self.L[:, None] * dWv) / np.pi
        M = np.zeros((self.K + 1, self.K + 1))
        M[:self.K, :self.K] = self.c * self.dPHI_v + self.a * Xc * dH
        M[:self.K, self.K] = self.a * hilbert_pv(self.u, self.w, wu, wv, self.v)
        M[self.K, :self.K] = self.g0
        return M

    def solve(self, Xc0=10.0, b0=None, tol=1e-13, max_iter=80):
        """Newton with backtracking; the line search also refuses e <= 0.

        Cold start (s == 1, any X_c0 of the right order) converges in 6-9 steps at
        every a this project cares about, which is the first sign that the reduced
        formulation is the right one -- the direct build never converged at all.
        """
        b = np.zeros(self.K)
        b[0] = 1.0
        if b0 is not None:
            b = np.asarray(b0, float).copy()
        Xc, hist = float(Xc0), []
        for _ in range(int(max_iter)):
            F = self.residual(b, Xc)
            hist.append(float(np.max(np.abs(F))))
            if hist[-1] < tol:
                break
            try:
                step = np.linalg.solve(self.jacobian(b, Xc), -F)
            except np.linalg.LinAlgError:
                return {"converged": False, "reason": "singular Jacobian",
                        "b": b, "Xc": float(Xc), "history": hist}
            t, base = 1.0, hist[-1]
            while t > 1e-8:
                bt, Xt = b + t * step[:self.K], Xc + t * step[self.K]
                if (Xt > 0.0 and (self.PHI_v @ bt).min() > 0.0
                        and np.max(np.abs(self.residual(bt, Xt))) < base):
                    break
                t *= 0.5
            b, Xc = b + t * step[:self.K], Xc + t * step[self.K]
        res = float(np.max(np.abs(self.residual(b, Xc))))
        return {"b": b, "Xc": float(Xc), "history": hist, "residual": res,
                "converged": bool(res < 1e-10), "iterations": len(hist) - 1}

    # -- derived quantities ------------------------------------------------
    def mass(self, b, Xc, on_outside="zero"):
        """m = int Omega dX over the support (the far field's only free constant).

        Guarded through `_w_of`: identical to the pre-repair value whenever `e > 0` at
        every quadrature node, which is every converged profile this module produces.
        """
        return -float(Xc * np.sum(self.w * self._w_of(b, "mass", on_outside)))

    def edge_amplitude(self, b, Xc):
        """A in Omega ~ -A (X_c - X)^{1/a}, from (FI) with no fitting.

        e ~ 2 s(1) (1 - v) and v = X/X_c, so Omega = -e^{1/a} gives
        A = (2 s(1) / X_c)^{1/a}.
        """
        T, _ = even_cheb(self.K, np.array([1.0]))
        s1 = float(T[0] @ b)
        return float((2.0 * s1 / Xc) ** self.p)

    def outer_velocity(self, b, Xc, y_max=1e7, n=4001, on_outside="zero"):
        """(U_0, m): U(X) - (m/pi) log X -> U_0 as X -> infinity.

        Measured OUTSIDE the support, where Omega == 0 and H(Omega) is a plain
        integral with no principal value -- so this is the profile's own far-field
        constant, not the anchor's.  It is what turns v12's X_c ~ e^{c/a} into a
        prediction with a measured constant:  log X_c = -pi(c/a + U_0)/m.
        """
        m = self.mass(b, Xc, on_outside=on_outside)
        wq = -self._w_of(b, "outer_velocity", on_outside)
        y = np.geomspace(1.0, float(y_max), int(n))
        Hy = ((wq[None, :] / (y[:, None] - self.u[None, :])) @ self.w) / np.pi
        U = (-self.c / self.a
             + Xc * np.concatenate([[0.0],
                                    np.cumsum(0.5 * (Hy[1:] + Hy[:-1]) * np.diff(y))]))
        tail = U - (m / np.pi) * np.log(Xc * y)
        return float(np.mean(tail[-n // 20:])), m

    def predicted_radius(self, b, Xc):
        """X_c/c predicted by the far-field law with the profile's OWN (m, U_0)."""
        U0, m = self.outer_velocity(b, Xc)
        return float(np.exp((-self.c / self.a - U0) * np.pi / m))

    # -- the kill switch ---------------------------------------------------
    def operator_norm(self, b, Xc, n_eval=801, measure="e", alpha=None):
        """||A|| = ||M^{-1}||, sup-to-sup, with the DOMAIN measured as a function.

        The codomain of M is the residual sampled at the nodes (a sup norm on the
        equation).  Its domain is the coefficient vector, which is not a function
        space, so the image of A is pushed through to values: a perturbation
        (db, dX_c) is measured as sup over a fixed fine grid of |de(v)| -- or of
        |dOmega| with `measure="Omega"` -- together with |dX_c| / X_c.

        `alpha` optionally applies the decay grading v3-v11 used on the whole line,
        w_dom = (1+X^2)^{alpha/2} and w_cod = (1+X^2)^{(alpha+1)/2}.  On a COMPACT
        interval every such weight is bounded above and below, so it can change the
        value but not the rate in K -- which is the point of offering it: the
        flatness this measures has to be robust to the choice of norm, or it is
        about the norm rather than the operator.  On the whole line the same weights
        are not equivalent, which is exactly why v12's ladder was graded.
        """
        A = np.linalg.inv(self.jacobian(b, Xc))
        s = np.linspace(0.0, 1.0, int(n_eval))
        T, _ = even_cheb(self.K, s)
        E = (1.0 - s ** 2)[:, None] * T
        if measure == "Omega":
            e = E @ b
            E = (self.p * np.abs(e) ** (self.p - 1.0))[:, None] * E
        img = np.vstack([E @ A[:self.K, :], A[self.K, :][None, :] / Xc])
        if alpha is not None:
            w_dom = np.concatenate([(1.0 + (Xc * s) ** 2) ** (0.5 * alpha), [1.0]])
            w_cod = np.concatenate([(1.0 + (Xc * self.v) ** 2)
                                    ** (0.5 * (alpha + 1.0)), [1.0]])
            img = w_dom[:, None] * img / w_cod[None, :]
        return float(np.max(np.abs(img).sum(axis=1)))


# ---------------------------------------------------------------------------
# the identity, checked against whatever profile you already have
# ---------------------------------------------------------------------------


def first_integral_defect(Omega, U, a, c, mask=None, on_nonfinite="nan", detail=False):
    """max/min - 1 of |Omega| / E^{1/a} -- zero iff (FI) holds on the sample.

    Deliberately takes arrays rather than a solver object, so the same check runs
    against any discretization the project owns.  `mask` selects where the ratio
    is meaningful (Omega away from zero, E positive).

    THE NaN GUARD (leg 107, finding B).  Every ordered comparison against NaN is false
    (IEEE-754 §5.11), so the default mask used to DROP poisoned points rather than be
    poisoned by them: leg 107 measured 397 of 400 points NaN and the identity still
    certified to 1.33e-15, the number improving as the poisoning worsened, with the only
    flag at 398 coming from the pre-existing `< 3 survivors` arity guard.

    The fix is to count non-finite points BEFORE any mask is applied -- a mask cannot
    select what it cannot see -- and to refuse rather than to certify:

      * `on_nonfinite="nan"` (default): any non-finite point in `Omega` or `U` makes the
        sample uncertifiable; return NaN and raise `FirstIntegralSampleWarning`.  The
        rule is over the WHOLE input, including outside a caller-supplied mask, because a
        NaN anywhere means the sample is not the object the caller believes it is.
      * `on_nonfinite="drop"`: the pre-repair behaviour -- exclude them and answer anyway
        -- but the warning still fires and `detail=True` reports how many were dropped.
      * `on_nonfinite="raise"`: ValueError.

    Unchanged, and deliberately: a FINITE poison (leg 107's control -- one doubled point
    gives 1.000, one `inf` gives `inf`) was always caught, and still is; NaN in the
    scalars `a` or `c` still gives NaN; the `< 3 survivors` arity guard still fires.

    `detail=True` returns `{"defect": <float>, "reason": <str|None>, **sample_fields(...)}`
    -- which is the "report the surviving count" half of leg 107's recommendation, so a
    caller can see that a defect of 1.33e-15 was computed from 3 points and not 400.
    """
    if on_nonfinite not in ("nan", "drop", "raise"):
        raise ValueError("on_nonfinite must be 'nan', 'drop' or 'raise', got "
                         f"{on_nonfinite!r}")
    Omega, U = np.asarray(Omega, float), np.asarray(U, float)
    E = float(c) + float(a) * U
    finite = np.isfinite(Omega) & np.isfinite(U)
    n_points = int(finite.size)
    n_nonfinite = int(np.count_nonzero(~finite))
    if mask is None:
        # the default mask now SAYS it is dropping non-finite points instead of doing it
        # by accident, through a comparison that is false for a reason unrelated to the
        # question being asked.
        mask = (np.abs(Omega) > 1e-11) & (E > 1e-8) & finite
    mask = np.asarray(mask, bool)
    n_used = int(np.count_nonzero(mask))

    def _out(val, reason):
        if not detail:
            return val
        return {"defect": val, "reason": reason,
                **sample_fields(n_points, n_nonfinite, n_used)}

    if n_nonfinite:
        msg = (f"first_integral.first_integral_defect: {n_nonfinite} of {n_points} "
               f"sample point(s) are non-finite in Omega or U "
               f"({100.0 * n_nonfinite / max(n_points, 1):.2f}%).  A mask cannot select "
               f"what it cannot see: every ordered comparison against NaN is false, so "
               f"before leg 107's repair these points left the sample instead of "
               f"poisoning the answer (397/400 NaN still certified (FI) to 1.33e-15).  "
               f"Policy on_nonfinite={on_nonfinite!r}.")
        if on_nonfinite == "raise":
            raise ValueError(msg)
        warnings.warn(msg, FirstIntegralSampleWarning, stacklevel=2)
        if on_nonfinite == "nan":
            return _out(np.nan, "non-finite points in the sample")
        mask = mask & finite
        n_used = int(np.count_nonzero(mask))
    if n_used < 3:
        return _out(np.nan, "fewer than 3 usable points")
    r = np.abs(Omega[mask]) / E[mask] ** (1.0 / float(a))
    return _out(float(r.max() / r.min() - 1.0), None)


def anchor_limit(X, c=0.5):
    """The a -> 0 form Omega = -exp(U/c) on the exact anchor -- must BE the anchor.

    U = -(1/2) log(1 + X^2) and c = 1/2, so exp(U/c) = 1/(1+X^2).  Returned as a
    pair so the caller can difference them.
    """
    X = np.asarray(X, float)
    U = -0.5 * np.log(1.0 + X ** 2)
    return -np.exp(U / float(c)), -1.0 / (1.0 + X ** 2)
