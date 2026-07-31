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
"""

import numpy as np

TWO_PI = 2.0 * np.pi


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


def pointwise_bound(theta, alpha, gamma, rho=1.0, n_quad=400, eps=1e-10):
    """(a_sup, a_semi) with |H(h)(theta)| <= a_sup S + a_semi T for every even h."""
    theta = float(theta)
    cS = cT = 0.0
    for L, sgn in ((theta, -1.0), (np.pi - theta, 1.0)):
        if L <= 0.0:
            continue
        a, b = _side(theta, alpha, gamma, rho, L, sgn, n_quad, eps)
        cS += a
        cT += b
    return cS / TWO_PI, cT / TWO_PI


def theta_grid(n_theta=140, lo=1e-8):
    """Angles graded to BOTH ends -- the far field and the origin are both edges."""
    ell = np.geomspace(lo, np.pi / 2.0, int(n_theta) // 2)
    near = np.geomspace(lo, np.pi / 2.0, int(n_theta) - int(n_theta) // 2)
    th = np.unique(np.concatenate([np.pi - ell, near]))
    return th[(th > 0.0) & (th < np.pi)]


def pointwise_curves(alpha, gamma, rho=1.0, n_theta=140, n_quad=400):
    """(X, a_sup, a_semi) on a graded theta grid -- drop-in for v7's `curves`."""
    th = theta_grid(n_theta)
    ab = np.array([pointwise_bound(t, alpha, gamma, rho=rho, n_quad=n_quad)
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
              n_theta=140, n_quad=400, closure_fn=None):
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
                              n_quad=n_quad)
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
