"""A sharper pointwise |H(h)| bound -- and the payer rule it exposes.

By v8 the Newton-Kantorovich ledger had seven of ten constants bounded and Z2
complete, so the natural next question changed.  Coverage is nearly done;
SHARPNESS is what the budget now scales with, and the arithmetic is blunt:
||A||'s bracket is ~75x wide (0.85 <= seminorm part <= 63.6) and C_Q's is ~4x,
the budget goes like 1/(||A|| C_Q), so bounding the remaining three constants
cannot buy more than a constant factor each while halving the slack in ||A||
buys more than all of them together.

Almost all of that slack enters through ONE input.  v7's closure reads
T <= F(T) with the feedback carried by |H(h)|, and at the reference point the
Hilbert term supplies 81 of the 93 units in the derivative bound: the closure is
dominated by its own feedback, and the feedback is dominated by v6's bound on
|H(h)|.  That bound was built out of crude majorants (|cot| <= 2/|u|, a 4/3 here
and a 16/15 there, the singular half charged wholesale to the seminorm).  This
module rebuilds it with v8's machinery -- exact kernels, log-graded quadrature,
a pointwise choice of which part of the norm pays -- and finds something that
was not visible in v6's construction.

--------------------------------------------------------------------------
THE BOUND
--------------------------------------------------------------------------
For h EVEN, folding the conjugate-function integral onto (0, pi) gives the exact
kernel

    psi(th) = H(h)(th) = (1/2pi) p.v. int_0^pi h(phi) K_th(phi) dphi ,
    K_th(phi) = 2 sin(th) / (cos phi - cos th)
              = -sin(th) / ( sin((phi+th)/2) sin((phi-th)/2) ) ,          (K)

the second form being the one to evaluate: near the far-field endpoint both
cosines approach -1 and their difference loses every significant digit, which is
how the first draft of this module produced NaNs at X >~ 1e4.  Parameterising by
the OFFSET s = |phi - th| makes sin((phi-th)/2) = sin(+-s/2) exact.

K has the far-field decay built in -- sin(th) -> 0 as th -> pi -- which is the
same structural point v6 made with its even kernel 2X/(X^2-y^2): H of an even
function is odd, and a form that cannot see that cannot see the decay either.

Better, p.v. int_0^pi K_th dphi = 0 exactly (it is the conjugate of the constant
function), with antiderivative -2 log|sin((phi-th)/2) / sin((phi+th)/2)|, which
vanishes at BOTH endpoints.  So the principal value can be handled by the global
subtraction

    psi(th) = (1/2pi) p.v. int_0^pi [h(phi) - h(th)] K_th(phi) dphi

with no band, no matching scale, and no remainder term -- v6 needed all three.
Then |h(phi) - h(th)| gets the same two-route envelope v8 used, and the whole
bound is one log-graded quadrature per side.

--------------------------------------------------------------------------
THE PAYER RULE, AND WHY IT IS NOT FREE
--------------------------------------------------------------------------
At each phi the increment can be charged to the seminorm (T |phi-th|^gamma
cos^{alpha-gamma}) or to the decay envelope (S [cos^alpha(phi/2) +
cos^alpha(th/2)]), and any FIXED rule for choosing gives a valid linear bound
a_sup S + a_semi T.  v8 chose by comparing the two at S = T = 1.  That is the
wrong default here, and the reason is worth stating in general terms:

    the rule should be tuned to the ratio T/S of the answer, not to 1.

In the closure S ~ 5.5 while T ~ 50, so a rule that shifts work onto T to
minimise the S = T = 1 sum is charging the expensive account.  Introducing
rho and choosing the seminorm route iff rho * c_T <= c_S:

    rho     1      3      6     12     25    100
    ||A||  75.2   53.1   47.1   47.6   50.4  57.4     (v6's bound: 69.1)

There is an INTERIOR optimum at rho ~ 6, and the neutral rule rho = 1 is 60%
worse than it -- worse, in fact, than the crude bound it was meant to replace.
Different consumers want different rho: the closure wants ~6 because it is
feeding a large T, while C_Q maximises over the unit simplex where the ratio is
O(1) and wants rho ~ 1.  Each is a separate valid bound; `pointwise_curves`
takes rho as an argument and the caller picks.

--------------------------------------------------------------------------
WHAT THIS IS NOT (carry the caveat)
--------------------------------------------------------------------------
Plain float64.  The theta-sweep is a grid, refined until it stops moving.  The
bound is an honest majorant -- every inequality is pointwise in phi -- but it is
still a bound: `measured_pointwise` supplies the other side of the bracket, and
on the anchor profile the two nearly meet (ratio ~0.98), while on oscillatory
members they do not.

Nothing here is interval-enclosed and nothing is rigorous.

--------------------------------------------------------------------------
THE DOMAIN GUARD (leg 130, repairing leg 106's escalation)
--------------------------------------------------------------------------
Leg 106 measured two configurations on which the returned pair is NOT a
majorant, and escalated rather than patching.  Both are one mechanism.  The
sup-account integrand in d(log s) tends to a NONZERO constant as the offset
s -> 0 (|K| s -> 2 and cS -> 2 cos^alpha(th/2) != 0), so the sup route is
LOGARITHMICALLY DIVERGENT at the endpoint; the only thing that tames it is
cT ~ s^gamma -> 0, which needs gamma > 0 AND needs the payer rule to actually
select the seminorm account on a neighbourhood of s = 0.  When it does not, the
number this module returns is finite only because the quadrature starts at
s = eps*L: it is the eps-truncation of a divergent integral, not a bound.

  (V1) rho non-finite, and rho >= ~1e300: `take_T = rho*cT <= cS` is False on
       the whole quadrature (for NaN by IEEE-754 sec 5.11, for the rest because
       the crossover UNDERFLOWS), so the singularity is charged to the divergent
       account.
  (V2) gamma <= 0: cT no longer vanishes as s -> 0 (at gamma = 0 it tends to
       cos^alpha(th/2), below 0 it blows up), so NO account tames the endpoint.

That gamma > 0 is exactly the hypothesis under which the conjugate operator
preserves Holder classes is the PLEMELJ-PRIVALOV theorem; nothing about the
condition is new here, only its enforcement.  `_head_bound` computes, in closed
form, a rigorous bound on the head the quadrature discards, and the guard's
predicate is threshold-free:

    reject iff that head does not VANISH as eps -> 0,

i.e. iff the asymptotic payer crossover s* = (2 cos^gamma(th/2) / rho)^{1/gamma}
is not a representable positive float, or gamma <= 0, or an argument is
non-finite or outside theta in (0, pi).  Measured over 4,188 shipped
configurations (alpha 1.5, gamma 0.5, rho in {1, 6, 25}), that predicate fires
on ZERO of them, and every accepted value is BIT-IDENTICAL to what this module
returned before the guard.  A bare "the head is positive" predicate was measured
and REJECTED during construction: it fires on 44 of those 4,188 (all at rho = 25
within 1e-7 of theta = pi), where the head is 6.9e-5 of the returned pair
against a measured margin of ~2e-4 -- thin, but not violated.

`on_unsound` selects what happens on a rejected configuration:

  * `"raise"` (default) -- HilbertPointwiseDomainError.  A bound that does not
    dominate must not reach a downstream consumer silently.
  * `"inflate"` -- return a pair that TRULY dominates: the computed pair plus the
    closed-form head, which is (inf, inf) exactly when the head is unbounded.
    Correct, and useless, which is the honest content of V1/V2.
  * `"extrapolate"` -- the pre-repair number, with a warning, so leg 106's
    battery can keep MEASURING the gap instead of deleting the measurement.

Separately, an ACCEPTED configuration whose discarded head is a material
fraction (`HEAD_WARN_TOL`) of the returned pair gets a
HilbertPointwiseTruncationWarning.  It changes no returned value -- that is what
keeps the accepted surface bit-identical -- and it exists because the band
rho ~ 1e6..1e12, which leg 106 never tested, is under-resolved at the default eps
(head 0.164 and 1.376 of the returned pair) while its exact majorant is finite,
so rejecting it would be a claim about a configuration that is merely
under-refined.
"""

import warnings

import numpy as np

TWO_PI = 2.0 * np.pi

#: Relative size of the discarded head at which an ACCEPTED configuration warns.
#: Governs a warning only -- never a rejection, never a returned number.  The
#: worst sound configuration measured sits at 6.9e-5 (14x below); the worst
#: violator this catches sits at 0.164 (164x above).
HEAD_WARN_TOL = 1e-3

_UNSOUND_POLICIES = ("raise", "inflate", "extrapolate")


class HilbertPointwiseDomainError(ValueError):
    """The returned pair would not be a majorant on this configuration."""


class HilbertPointwiseUnsoundWarning(UserWarning):
    """`on_unsound='extrapolate'`: the pre-repair, non-dominating number."""


class HilbertPointwiseTruncationWarning(UserWarning):
    """Accepted, but the discarded inner head is a material share of the value."""


def _head_bound(theta, alpha, gamma, rho, eps):
    """Rigorous bound on the head the quadrature DISCARDS, per account.

    Returns `(head_sup, head_semi, vanishes)`, already divided by `2 pi` so the
    two entries are directly comparable with `pointwise_bound`'s return value.
    `vanishes` is False exactly when `head_sup` fails to tend to 0 as `eps -> 0`,
    which is the guard's predicate.

    On (0, s0) with s0 = eps*L: |K| s <= kappa with kappa computed from the two
    exact monotonicities (sin is concave on (0, pi), s/sin(s/2) is increasing),
    cos(phi/2) and cos(min(phi,theta)/2) lie in [cmin, cmax] = [c -+ s0/2], and
    cS >= 2 cmin^alpha.  Hence
        int_0^{s0} cT |K| s dlog s <= kappa cmax^{alpha-gamma} s0^gamma / gamma
    and the sup account contributes only where the payer rule selects it, i.e.
    on (s*, s0) when the crossover s* -- the root of rho cT = cS -- lies below
    s0, giving kappa * 2 cmax^alpha * log(s0/s*).
    """
    if not (gamma > 0.0):
        return np.inf, np.inf, False
    hS = hT = 0.0
    vanishes = True
    for L, sgn in ((theta, -1.0), (np.pi - theta, 1.0)):
        if L <= 0.0:
            continue
        s0 = eps * L
        c = np.cos(0.5 * theta)
        cmax = min(1.0, c + 0.5 * s0)
        cmin = max(0.0, c - 0.5 * s0)
        edge = min(np.sin(theta), np.sin(theta + sgn * 0.5 * s0))
        if edge <= 0.0:
            return np.inf, np.inf, False
        kappa = 2.0 * (np.sin(theta) / edge) * ((0.5 * s0) / np.sin(0.5 * s0))
        hT += kappa * cmax ** (alpha - gamma) * s0 ** gamma / gamma
        denom = rho * cmax ** (alpha - gamma)
        base = (2.0 * cmin ** alpha / denom) if denom > 0.0 else 0.0
        sstar = base ** (1.0 / gamma) if base > 0.0 else 0.0
        if sstar <= 0.0:
            hS, vanishes = np.inf, False
        elif sstar < s0:
            hS += kappa * 2.0 * cmax ** alpha * np.log(s0 / sstar)
    return hS / TWO_PI, hT / TWO_PI, vanishes


def _audit(theta, alpha, gamma, rho, eps):
    """`(reason or None, head_sup, head_semi)` -- the whole soundness decision."""
    named = (("theta", theta), ("alpha", alpha), ("gamma", gamma),
             ("rho", rho), ("eps", eps))
    bad = [n for n, v in named if not np.isfinite(v)]
    if bad:
        return ("non-finite argument(s) %s: the payer rule `rho*cT <= cS` is then "
                "False on the whole quadrature (IEEE-754 sec 5.11 makes every "
                "comparison against NaN False), so the log-divergent sup account "
                "is charged the singularity and the returned pair is the "
                "eps-truncation of a divergent integral, not a bound"
                % ", ".join(bad), np.inf, np.inf)
    if not (0.0 < theta < np.pi):
        return ("theta = %r is outside (0, pi), the interval the folded kernel is "
                "derived on" % theta, np.inf, np.inf)
    if not (gamma > 0.0):
        return ("gamma = %r <= 0: the seminorm envelope cT ~ s^gamma no longer "
                "vanishes as the offset s -> 0, so NO account tames the kernel's "
                "logarithmic endpoint divergence.  gamma > 0 is the "
                "Plemelj-Privalov hypothesis under which the conjugate operator "
                "preserves the Holder class at all" % gamma, np.inf, np.inf)
    if not (rho > 0.0):
        return ("rho = %r <= 0 is not a payer ratio; the rule it defines is "
                "'always charge the seminorm', which is a different bound"
                % rho, np.inf, np.inf)
    if not (0.0 < eps < 1.0):
        return ("eps = %r is outside (0, 1); the discarded head (0, eps*L) is then "
                "not an inner neighbourhood of the singularity" % eps,
                np.inf, np.inf)
    hS, hT, vanishes = _head_bound(theta, alpha, gamma, rho, eps)
    if not vanishes:
        return ("the payer crossover s* = (2 cos^gamma(theta/2)/rho)^(1/gamma) is "
                "not a representable positive float at rho = %r, so the seminorm "
                "account is never selected on the quadrature and the discarded "
                "head does not vanish as eps -> 0: the returned pair is an "
                "eps-truncation of a divergent integral, not a bound" % rho,
                hS, hT)
    return None, hS, hT


def _side(theta, alpha, gamma, rho, L, sgn, n_quad, eps):
    """One side of the folded integral, returned as (S-coefficient, T-coefficient)."""
    s = np.geomspace(eps * L, L, int(n_quad))
    phi = theta + sgn * s
    # |K| in the offset form: sin((phi-th)/2) = sin(sgn s / 2) exactly.
    Kabs = np.abs(np.sin(theta) / (np.sin(0.5 * (phi + theta)) * np.sin(0.5 * sgn * s)))
    cT = s ** gamma * np.cos(0.5 * np.minimum(phi, theta)) ** (alpha - gamma)
    cS = np.cos(0.5 * phi) ** alpha + np.cos(0.5 * theta) ** alpha
    take_T = rho * cT <= cS
    w = Kabs * s
    ls = np.log(s)
    tz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz      # noqa: NPY201
    return (float(tz(np.where(take_T, 0.0, cS) * w, ls)),
            float(tz(np.where(take_T, cT, 0.0) * w, ls)))


def _raw_bound(theta, alpha, gamma, rho, n_quad, eps):
    """The pre-guard arithmetic, verbatim.  Nothing in here was touched."""
    cS = cT = 0.0
    for L, sgn in ((theta, -1.0), (np.pi - theta, 1.0)):
        if L <= 0.0:
            continue
        a, b = _side(theta, alpha, gamma, rho, L, sgn, n_quad, eps)
        cS += a
        cT += b
    return cS / TWO_PI, cT / TWO_PI


def pointwise_bound(theta, alpha, gamma, rho=1.0, n_quad=400, eps=1e-10,
                    on_unsound="raise"):
    """(a_sup, a_semi) with |H(h)(theta)| <= a_sup S + a_semi T for every even h.

    Guarded since leg 130 -- see the module docstring.  `on_unsound` is one of
    `"raise"` (default), `"inflate"` (a pair that truly dominates) or
    `"extrapolate"` (the pre-repair pair, with a warning).  On every accepted
    configuration the returned pair is bit-identical to the pre-guard module.
    """
    if on_unsound not in _UNSOUND_POLICIES:
        raise ValueError("on_unsound must be one of %r, got %r"
                         % (_UNSOUND_POLICIES, on_unsound))
    theta = float(theta)
    reason, head_S, head_T = _audit(theta, alpha, gamma, rho, eps)
    if reason is not None:
        if on_unsound == "raise":
            raise HilbertPointwiseDomainError(reason)
        if on_unsound == "inflate":
            if not (np.isfinite(head_S) and np.isfinite(head_T)):
                return np.inf, np.inf
            raw = _raw_bound(theta, alpha, gamma, rho, n_quad, eps)
            return raw[0] + head_S, raw[1] + head_T
        warnings.warn("hilbert_pointwise: " + reason + " -- returning the "
                      "pre-repair value anyway because on_unsound='extrapolate'",
                      HilbertPointwiseUnsoundWarning, stacklevel=2)
        return _raw_bound(theta, alpha, gamma, rho, n_quad, eps)
    out = _raw_bound(theta, alpha, gamma, rho, n_quad, eps)
    total = out[0] + out[1]
    if total > 0.0 and head_S > HEAD_WARN_TOL * total:
        warnings.warn("hilbert_pointwise: the quadrature's inner endpoint "
                      "s = eps*L does not resolve the payer crossover at "
                      "theta = %r, rho = %r: the discarded sup-account head is "
                      "%.3g, i.e. %.3g of the returned pair.  The majorant is "
                      "finite here, so this is under-refinement, not a divergence "
                      "-- decrease eps (or use on_unsound='inflate' for a pair "
                      "that dominates as returned)" % (theta, rho, head_S,
                                                       head_S / total),
                      HilbertPointwiseTruncationWarning, stacklevel=2)
    return out


def theta_grid(n_theta=140, lo=1e-8):
    """Angles graded to BOTH ends -- the far field and the origin are both edges."""
    ell = np.geomspace(lo, np.pi / 2.0, int(n_theta) // 2)
    near = np.geomspace(lo, np.pi / 2.0, int(n_theta) - int(n_theta) // 2)
    th = np.unique(np.concatenate([np.pi - ell, near]))
    return th[(th > 0.0) & (th < np.pi)]


def pointwise_curves(alpha, gamma, rho=1.0, n_theta=140, n_quad=400,
                     on_unsound="raise"):
    """(X, a_sup, a_semi) on a graded theta grid -- drop-in for v7's `curves`."""
    th = theta_grid(n_theta)
    ab = np.array([pointwise_bound(t, alpha, gamma, rho=rho, n_quad=n_quad,
                                   on_unsound=on_unsound)
                   for t in th])
    return np.tan(0.5 * th), ab[:, 0], ab[:, 1]


def weighted_sups(curves, alpha):
    """The two sups the downstream constants actually consume.

    `closure` : sup_X (1+X^2)^{(alpha-1)/2} a  -- v7's derivative bound;
    `cq`      : sup_X (1+X^2)^{1/2} a          -- the C_Q sup part.
    """
    Xs, aS, aT = curves
    wk = (1.0 + Xs ** 2) ** (0.5 * (alpha - 1.0))
    w1 = np.sqrt(1.0 + Xs ** 2)
    return {"closure_sup": float(np.max(wk * aS)),
            "closure_semi": float(np.max(wk * aT)),
            "cq_sup": float(np.max(w1 * aS)), "cq_semi": float(np.max(w1 * aT))}


# ---------------------------------------------------------------------------
# the payer rule
# ---------------------------------------------------------------------------


def sweep_rho(alpha, gamma, C_sup, rhos=(1.0, 2.0, 3.0, 4.5, 6.0, 9.0, 12.0, 25.0),
              n_theta=140, n_quad=400, closure_fn=None, on_unsound="raise"):
    """||A|| upper bound as a function of the payer rule's rho.

    `closure_fn(alpha, gamma, C_sup, curves) -> dict with 'A_upper'` is injected
    (solver.nk_seminorm.seminorm_closure with `curves=`), so this module does not
    import the closure and the two stay independently testable.
    """
    if closure_fn is None:                                   # pragma: no cover
        from solver.nk_seminorm import seminorm_closure

        def closure_fn(a, g, cs, cv):
            return seminorm_closure(a, g, cs, curves=cv)
    out = []
    for rho in rhos:
        cv = pointwise_curves(alpha, gamma, rho=rho, n_theta=n_theta,
                              n_quad=n_quad, on_unsound=on_unsound)
        d = closure_fn(alpha, gamma, C_sup, cv)
        w = weighted_sups(cv, alpha)
        out.append({"rho": float(rho), "A_upper": float(d["A_upper"]),
                    "T_upper": float(d["T_upper"]), **w})
    best = min(out, key=lambda r: r["A_upper"])
    return {"rows": out, "best": best,
            "neutral_penalty": next(r for r in out if r["rho"] == 1.0)["A_upper"]
                               / best["A_upper"] if any(r["rho"] == 1.0 for r in out)
                               else None}


# ---------------------------------------------------------------------------
# the other side of the bracket
# ---------------------------------------------------------------------------


def measured_pointwise(profiles, theta, psi_of, norms, alpha, gamma, curves,
                       n_sample=80):
    """max over a family of |psi| / (a_sup S + a_semi T): a LOWER-bound check.

    Returns the worst ratio and where it is attained.  A ratio near 1 says the
    bound is nearly attained on that family (the anchor profile does this); a
    small ratio says the remaining slack is real but unlocated.
    """
    Xs, aS, aT = curves
    idx = np.unique(np.linspace(0, theta.size - 1, int(n_sample)).astype(int))
    lx = np.log(np.clip(np.tan(0.5 * theta[idx]), Xs[0], Xs[-1]))
    a_s = np.interp(lx, np.log(Xs), aS)
    a_m = np.interp(lx, np.log(Xs), aT)
    worst, arg = 0.0, ("", 0.0)
    for name, h in profiles.items():
        S, T = norms.sup_part(h), norms.seminorm(h)
        ratio = np.abs(psi_of(h)[idx]) / (a_s * S + a_m * T)
        i = int(np.argmax(ratio))
        if ratio[i] > worst:
            worst, arg = float(ratio[i]), (name, float(theta[idx][i]))
    return {"worst_ratio": worst, "profile": arg[0], "theta": arg[1]}
