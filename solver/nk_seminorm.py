"""The domain SEMINORM part of ||A||: a derivative-gain closure, free of J.

This is the sharpest of the three items Route-D v6 left open (see
writeup/4_p2_lottery/TECHNICAL_P2_ROUTED_V6.md, ledger B6).  v6 bounded the
domain SUP part of ||A|| uniformly in J (the two-point dual saturates at 5.55 at
alpha = 1.5, gamma = 0.5) and left the domain SEMINORM part with only a valid but
lossy bound growing like J^gamma.  Three separate computations came back with
that same J^gamma, and v6 attributed it to the discrete-ball direction it was
still pricing.

--------------------------------------------------------------------------
WHY DUALITY CANNOT FIX IT, AND WHAT REPLACES IT
--------------------------------------------------------------------------
The lossy quantity is

    max_{j != k}  p_jk ||A_j. - A_k.||_{Y*} ,   p_jk = min(w_semi) / |dtheta|^gamma ,

and the J^gamma comes from ADJACENT rows: there p_jk ~ J^gamma, and a dual bound
on ||A_j. - A_k.||_{Y*} that treats the two rows separately cannot see that they
nearly cancel.  No sharpening of the dual functional recovers that cancellation,
because the cancellation is not a property of the rows -- it is a property of the
EQUATION: neighbouring rows of an inverse differ by a derivative.

So use the equation.  With Omega = -1/(1+X^2), H(Omega) = -X/(1+X^2), the
linearization at the anchor is

    DF h = -h X/(1+X^2) - H(h)/(1+X^2) - c h_X = g ,

which solves for the derivative,

    c h_X = -g - h X/(1+X^2) - H(h)/(1+X^2) .                            (P)

Every term on the right is already controlled: g by the codomain norm, h by the
sup part (v6's bound), H(h) by the far-field Hilbert bound v6 built for Z1.  So
the DERIVATIVE of the solution is bounded, and a Holder seminorm is bounded by an
interpolation between the sup norm and the derivative.  That interpolation is
where the near-diagonal cancellation enters, and it is J-free because nothing in
it refers to a grid.

--------------------------------------------------------------------------
THE TWO INEQUALITIES
--------------------------------------------------------------------------
Write S = sup_theta w_alpha |h| (the sup part), T = the weighted theta-Holder
seminorm (with weight alpha - gamma, v5's forced exponent), and

    P = sup_theta (1 + X^2)^{(alpha+1)/2} |h_X| .

For a pair theta_1 < theta_2 (so |X_1| < |X_2|, and the seminorm's min-weight is
the one at theta_1) split on the scale delta(theta_1) = kappa (1+X_1^2)^{-1/2},
which is the theta-length of a fixed multiple of the LOCAL X-scale:

  * SEPARATED pairs, |dtheta| > delta.  Use the sup part on each point:
    |h(th_1)| + |h(th_2)| <= 2 S / w_alpha(th_1) (w_alpha increases in |X|), so
    the pair contributes at most 2 S w_{-gamma}(th_1) / delta^gamma = 2 S
    kappa^{-gamma}: the weights cancel EXACTLY, at every scale.

  * NEAR pairs, |dtheta| <= delta.  Use the derivative: |dh| <= |dtheta| max
    |h_theta| with h_theta = (1+X^2) h_X / 2, so |h_theta| <= w_{1-alpha} P / 2,
    which for alpha >= 1 is largest at the smaller |X| -- i.e. at theta_1.  The
    pair then contributes at most (1/2) P w_{alpha-gamma} w_{1-alpha}
    delta^{1-gamma} = (1/2) P kappa^{1-gamma}: again the weights cancel exactly.

Both halves are therefore SCALE-INVARIANT, and

    T  <=  min_kappa [ (1/2) kappa^{1-gamma} P  +  2 S kappa^{-gamma} ]
        =  C(gamma) (P/2)^gamma (2 S)^{1-gamma} ,
    C(gamma) = (1-gamma)^{gamma-1} gamma^{-gamma}   ( = 2 at gamma = 1/2 ) .   (I)

That is the classical Holder interpolation inequality, with the conformal
compactification doing all the far-field bookkeeping -- the same free lunch v5
found for the seminorm itself.

--------------------------------------------------------------------------
THE CLOSURE (and why it is a fixed point, not a formula)
--------------------------------------------------------------------------
(P) bounds P in terms of S and |H(h)|, and |H(h)| depends on T -- so (I) feeds
back into itself.  Splitting v6's Hilbert bound into the part paid by the sup
norm and the part paid by the seminorm (`hilbert_split_bound`, a refactor of
`nk_bounds.hilbert_farfield_bound` that separates the two contributions instead
of charging both to the total norm -- worth ~30% on the final number) gives

    P <= (1/c) [ 1 + S + sup_X (1+X^2)^{(alpha-1)/2} ( a_sup(X) S + a_semi(X) T ) ]

and then (I) reads T <= F(T) with F concave increasing and F(0) > 0.  Such an F
has EXACTLY ONE fixed point T*, and F(T) - T >= 0 precisely on [0, T*], so any a
priori finite T obeying the inequality satisfies T <= T*.  `seminorm_closure`
returns T* by monotone iteration from 0.

AND THE FIXED POINT ALWAYS EXISTS, for a reason worth stating: the feedback is
LINEAR in T (it enters through |H(h)|) while the interpolation gain is
SUBLINEAR, F ~ T^gamma.  So for every gamma < 1 the closure holds no matter how
large the constants are -- there is no smallness condition to verify, and no
contraction to lose.  Only the Lipschitz endpoint gamma = 1 turns this into a
genuine contraction condition (there F ~ P/2 is linear in T and closure needs the
Hilbert feedback coefficient to beat 2c).  That is a third, independent reason
gamma = 1 is excluded, alongside v5's U2 (the Holder-Hilbert constant blows up at
both ends) and the classical failure of H on Lipschitz functions.

--------------------------------------------------------------------------
WHAT THIS IS AND IS NOT (carry the caveat)
--------------------------------------------------------------------------
This is a CONTINUUM estimate.  It bounds the seminorm of the true solution of
DF h = g, conditional on a bound C_sup for its sup part.  The only C_sup we have
is v6's, computed from the DISCRETE gauged inverse (uniform in J, but a statement
about grid nodes).  So the chain is: analytic, J-free, and conditional on a
hypothesis that is currently supported by grid measurements rather than proved.

`interpolant_far_field_defect` measures a second gap in the same joint, and it is
worse than it looks: a band-limited h is a trigonometric polynomial in theta, so
h(pi) != 0 in general, and w_alpha(theta) = sec^alpha(theta/2) diverges there.
The DECAY-GRADED NORM OF THE INTERPOLANT IS THEREFORE INFINITE AT EVERY J -- the
discrete norms of v1..v7 are finite only because the midpoint grid stops one half
step short of theta = pi.  The defect is soft (h(pi) itself falls like J^-2.4)
and the natural repair is to build the decay into the ansatz, h = (1+X^2)^{-
alpha/2} p(theta) with p a trigonometric polynomial, so that the weighted sup
norm becomes the plain sup norm of p.  Nothing here does that yet.

Plain float64.  Nothing in this module is interval-enclosed and nothing is
rigorous.
"""

import numpy as np

from solver.nk_bounds import holder_local_X_constant
from solver.nk_bounds import _I_out as _regular_part_integral   # v6's even-kernel tail

C_ANCHOR = 0.5


# ---------------------------------------------------------------------------
# (1) the Hilbert bound, split by which part of the norm pays for it
# ---------------------------------------------------------------------------


def hilbert_split_bound(X, alpha, gamma, n=1201):
    """(a_sup, a_semi) with |H(h)(X)| <= a_sup * S + a_semi * T for even h.

    S = sup_theta (1+X^2)^{alpha/2}|h| and T = the weighted theta-Holder
    seminorm.  This is exactly v6's `hilbert_farfield_bound` with the two
    contributions kept apart instead of both being charged to ||h|| = S + T:
    the principal-value band [X/2, 3X/2] splits into the increment of h (paid by
    T) and the increment of the even kernel (paid by S), and the rest of the line
    is paid by the decay envelope (S).  Summing the two gives v6's bound back,
    which is the module's first test gate.
    """
    X = float(X)
    delta = 0.5 * X
    env_semi = float(holder_local_X_constant(alpha, gamma, delta))
    env_sup = (1.0 + delta ** 2) ** (-0.5 * alpha)
    a_semi = (4.0 / 3.0) * env_semi * (2.0 ** gamma) * delta ** gamma / gamma
    a_sup = (16.0 / 15.0) * env_sup * delta / X + _regular_part_integral(X, alpha, n=n)
    return a_sup / np.pi, a_semi / np.pi


def hilbert_split_curves(alpha, gamma, X_lo=1e-3, X_hi=1e6, n_X=120, n_quad=801):
    """(X, a_sup, a_semi) sampled on a log grid -- cached input for the closure."""
    Xs = np.geomspace(X_lo, X_hi, int(n_X))
    pairs = [hilbert_split_bound(X, alpha, gamma, n=n_quad) for X in Xs]
    return Xs, np.array([p[0] for p in pairs]), np.array([p[1] for p in pairs])


# ---------------------------------------------------------------------------
# (2) the interpolation inequality
# ---------------------------------------------------------------------------


def interpolation_constant(gamma):
    """C(gamma) = (1-gamma)^{gamma-1} gamma^{-gamma}; C(1/2) = 2."""
    g = float(gamma)
    return (1.0 - g) ** (g - 1.0) * g ** (-g)


def holder_interpolation_bound(S, P, gamma):
    """min_kappa [ kappa^{1-gamma} P / 2 + 2 S kappa^{-gamma} ], in closed form.

    Returns (bound, kappa_star).  Both halves of the split are scale-invariant
    (see the module docstring), so kappa is a free parameter and this is its
    exact optimum: kappa* = 4 gamma S / ((1-gamma) P).
    """
    S, P, g = float(S), float(P), float(gamma)
    if P <= 0.0:
        return 0.0, float("inf")
    kappa = 4.0 * g * S / ((1.0 - g) * P)
    return interpolation_constant(g) * (0.5 * P) ** g * (2.0 * S) ** (1.0 - g), kappa


def derivative_bound(S, T, alpha, gamma, curves=None, c=C_ANCHOR, g_norm=1.0):
    """P <= (1/c)[ ||g||_Y + S + sup_X (1+X^2)^{(alpha-1)/2}(a_sup S + a_semi T) ].

    Straight from (P) of the module docstring: the transport term is the whole
    derivative, the h-term is bounded by S because X (1+X^2)^{-1/2} <= 1, and the
    Hilbert term by the split bound.  `curves` is the output of
    `hilbert_split_curves` (pass it in to avoid recomputing the quadrature).
    """
    if curves is None:
        curves = hilbert_split_curves(alpha, gamma)
    Xs, a_sup, a_semi = curves
    wk = (1.0 + Xs ** 2) ** (0.5 * (alpha - 1.0))
    hil = float(np.max(wk * (a_sup * float(S) + a_semi * float(T))))
    return (float(g_norm) + float(S) + hil) / float(c)


# ---------------------------------------------------------------------------
# (3) the closure
# ---------------------------------------------------------------------------


def seminorm_closure(alpha, gamma, C_sup, c=C_ANCHOR, curves=None,
                     T_cap=1e7, tol=1e-12, max_iter=20000):
    """Least (and only) fixed point of T = interpolation(S = C_sup, P(T)).

    Returns a dict with the seminorm bound, the derivative bound, kappa*, the
    local contraction factor dF/dT at the fixed point, and `closes`.  A missing
    fixed point is reported, never papered over.

    alpha >= 1 is required: the near-pair half uses that w_{1-alpha} decreases in
    |X|, so that the maximum of |h_theta| over the pair's interval sits at its
    inner endpoint.
    """
    alpha, gamma = float(alpha), float(gamma)
    if alpha < 1.0:
        raise ValueError("the near-pair estimate needs alpha >= 1 (got %.3f)" % alpha)
    if not 0.0 < gamma < 1.0:
        raise ValueError("gamma must lie strictly between 0 and 1")
    if curves is None:
        curves = hilbert_split_curves(alpha, gamma)
    S = float(C_sup)

    def F(T):
        P = derivative_bound(S, T, alpha, gamma, curves=curves, c=c)
        b, k = holder_interpolation_bound(S, P, gamma)
        return b, P, k

    T = 0.0
    for _ in range(int(max_iter)):
        nxt = F(T)[0]
        if nxt > T_cap:
            return {"closes": False, "T_upper": float("inf"), "C_sup": S,
                    "alpha": alpha, "gamma": gamma,
                    "reason": "no fixed point: the Hilbert feedback exceeds the "
                              "interpolation gain"}
        if abs(nxt - T) <= tol * max(1.0, T):
            T = nxt
            break
        T = nxt
    b, P, k = F(T)
    dT = max(1e-6, 1e-6 * T)
    slope = (F(T + dT)[0] - b) / dT
    return {"closes": True, "T_upper": float(T), "P_upper": float(P),
            "kappa_star": float(k), "contraction_slope": float(slope),
            "C_sup": S, "alpha": alpha, "gamma": gamma,
            "A_upper": float(S + T)}


def operator_norm_upper(alpha, gamma, C_sup, c=C_ANCHOR, curves=None):
    """||A||_{Y->X} <= C_sup + T_upper (sup part + seminorm part), or inf."""
    d = seminorm_closure(alpha, gamma, C_sup, c=c, curves=curves)
    return d["A_upper"] if d["closes"] else float("inf")


# ---------------------------------------------------------------------------
# (4) what the honest ||A|| costs downstream
# ---------------------------------------------------------------------------


def required_X0(A_upper, modelling_error, X0_grid, target=1.0):
    """Smallest X0 on the grid with A_upper * modelling_error(X0) <= target.

    `modelling_error` is a callable X0 -> the v6 far-field bound.  Also returns
    the collocation size the core would then need: the midpoint grid reaches
    |X| ~ 4J/pi, so covering [0, X0] densely needs J ~ pi X0 / 4, and the dense
    Jacobian is J^2.
    """
    for X0 in X0_grid:
        z = float(A_upper) * float(modelling_error(X0))
        if z <= target:
            J = np.pi * X0 / 4.0
            return {"found": True, "X0": float(X0), "Z1": z, "J_needed": float(J),
                    "dense_entries": float(J * J)}
    X0 = float(X0_grid[-1])
    return {"found": False, "X0_max_tried": X0,
            "Z1_at_max": float(A_upper) * float(modelling_error(X0))}


# ---------------------------------------------------------------------------
# (5) the interpolant's far-field defect
# ---------------------------------------------------------------------------


def interpolant_far_field_defect(to_coef, h, alpha, theta_last, n=9, eps=1e-6):
    """h(pi) and the weighted sup of the interpolant BEYOND the last grid node.

    A nodal vector on the midpoint grid stands for an even trigonometric
    polynomial, which does not vanish at theta = pi, while the decay weight
    w_alpha = sec^alpha(theta/2) diverges there.  So sup_theta w_alpha |h| is
    infinite for every J: the finite discrete norm is an artifact of the grid
    stopping half a step short.  Returns h(pi), the weighted value at the last
    node, and the weighted values on the sliver (theta_last, pi).
    """
    coef = np.asarray(to_coef, dtype=float) @ np.asarray(h, dtype=float)
    k = np.arange(coef.size)
    h_pi = float(coef @ (-1.0) ** k)
    th = np.linspace(float(theta_last), np.pi - float(eps), int(n))
    vals = np.cos(np.outer(th, k)) @ coef
    w = np.cos(0.5 * th) ** (-float(alpha))
    return {"h_pi": h_pi, "theta": th.tolist(),
            "weighted": (w * np.abs(vals)).tolist(),
            "weighted_at_last_node": float((w * np.abs(vals))[0])}
