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

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np


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


def even_cheb(K, v):
    """(T_{2k}(v), d/dv T_{2k}(v)) for k = 0..K-1; shapes (len(v), K)."""
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
    def e_of(self, b, v=None):
        """e(v) = (1 - v^2) s(v); at the collocation nodes when v is None."""
        if v is None:
            return self.PHI_v @ b
        T, _ = even_cheb(self.K, v)
        return (1.0 - np.asarray(v, float) ** 2) * (T @ b)

    def omega_of(self, b, v=None):
        """Omega = -(e)^{1/a} -- the profile itself, on the scaled support."""
        return -np.abs(self.e_of(b, v)) ** self.p

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
    def mass(self, b, Xc):
        """m = int Omega dX over the support (the far field's only free constant)."""
        wu = np.abs(self.PHI_u @ b) ** self.p
        return -float(Xc * np.sum(self.w * wu))

    def edge_amplitude(self, b, Xc):
        """A in Omega ~ -A (X_c - X)^{1/a}, from (FI) with no fitting.

        e ~ 2 s(1) (1 - v) and v = X/X_c, so Omega = -e^{1/a} gives
        A = (2 s(1) / X_c)^{1/a}.
        """
        T, _ = even_cheb(self.K, np.array([1.0]))
        s1 = float(T[0] @ b)
        return float((2.0 * s1 / Xc) ** self.p)

    def outer_velocity(self, b, Xc, y_max=1e7, n=4001):
        """(U_0, m): U(X) - (m/pi) log X -> U_0 as X -> infinity.

        Measured OUTSIDE the support, where Omega == 0 and H(Omega) is a plain
        integral with no principal value -- so this is the profile's own far-field
        constant, not the anchor's.  It is what turns v12's X_c ~ e^{c/a} into a
        prediction with a measured constant:  log X_c = -pi(c/a + U_0)/m.
        """
        m = self.mass(b, Xc)
        wq = -np.abs(self.PHI_u @ b) ** self.p
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


def first_integral_defect(Omega, U, a, c, mask=None):
    """max/min - 1 of |Omega| / E^{1/a} -- zero iff (FI) holds on the sample.

    Deliberately takes arrays rather than a solver object, so the same check runs
    against any discretization the project owns.  `mask` selects where the ratio
    is meaningful (Omega away from zero, E positive).
    """
    Omega, U = np.asarray(Omega, float), np.asarray(U, float)
    E = float(c) + float(a) * U
    if mask is None:
        mask = (np.abs(Omega) > 1e-11) & (E > 1e-8)
    if int(np.sum(mask)) < 3:
        return np.nan
    r = np.abs(Omega[mask]) / E[mask] ** (1.0 / float(a))
    return float(r.max() / r.min() - 1.0)


def anchor_limit(X, c=0.5):
    """The a -> 0 form Omega = -exp(U/c) on the exact anchor -- must BE the anchor.

    U = -(1/2) log(1 + X^2) and c = 1/2, so exp(U/c) = 1/(1+X^2).  Returned as a
    pair so the caller can difference them.
    """
    X = np.asarray(X, float)
    U = -0.5 * np.log(1.0 + X ** 2)
    return -np.exp(U / float(c)), -1.0 / (1.0 + X ** 2)
