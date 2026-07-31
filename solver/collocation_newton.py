"""Newton in the basis the BOUNDS live in -- and the defect the certificate sees.

Route-D v11 put a Newton solve on the two-scale profile equation and killed the
~1e-2 residual floor that five legs had carried as physics: on the Route-A
sinh-rho grid the relative residual falls to ~1e-14 for every a up to the
survival boundary a* ~ 0.5.  That measurement is in the WRONG DISCRETIZATION.
Every Route-D bound -- ||A||, C_Q, Z_1's far-field piece -- lives on the
compactified midpoint theta-grid of solver/decay_collocation.py, where
X = tan(theta/2) and the operator is exact on band-limited functions.  Y_0 is
the defect measured in THAT basis, in the codomain norm of THAT space, and the
two numbers are different objects.  This module carries the profile across.

--------------------------------------------------------------------------
WHAT IS NEW HERE: THE a-TERM IN THE COMPACTIFIED BASIS
--------------------------------------------------------------------------
solver/decay_collocation.py is built at the a = 0 anchor, where the residual is

    F(Omega, c) = Omega H(Omega) - c Omega_X

and every operator in sight (H, d/dtheta, d/dX = (1+cos theta) d/dtheta) is
EXACT on even trigonometric polynomials.  The a-family adds a transport term
built from the velocity

    U(X) = int_0^X H(Omega) dX' ,   R = Omega H(Omega) - c Omega_X - a U Omega_X ,

and U is the one object that is not local in the coefficients.  It has a closed
form.  With Omega = sum_k A_k cos k theta we have H(Omega) = sum_k A_k sin k theta
and dX = dtheta / (1 + cos theta), so U = sum_k A_k I_k(theta) with

    I_k(theta) = int_0^theta sin(k t) / (1 + cos t) dt ,

    I_0 = 0 ,  I_1 = log( 2 / (1 + cos theta) ) = log(1 + X^2) ,
    I_{k+1} = 2 (1 - cos k theta) / k - 2 I_k - I_{k-1} .

(The recursion is 2 sin kt cos t = sin(k+1)t + sin(k-1)t with cos t written as
(1 + cos t) - 1.)  So the velocity is a DENSE MATRIX ON COEFFICIENTS, assembled
once, and -- the part that matters for this leg -- it can be evaluated at ANY
theta, not only at grid nodes.

The recursion's homogeneous solutions are (A + B k)(-1)^k, i.e. it is only
marginally stable, and I_k itself grows like 2 k log(1/(pi-theta)) near the outer
endpoint -- the SAME rate, so relative error stays bounded but absolute error
tracks eps * k^2.  In float64 that is ~1e-7 at J = 1600, which is far too coarse
for a leg whose whole subject is a small defect, so the recursion is run in
longdouble and cast down (gate 1 measures both).

--------------------------------------------------------------------------
THE POINT OF THE MODULE (state it before running anything)
--------------------------------------------------------------------------
A Newton solve drives the residual to zero AT THE NODES.  The certificate does
not ask about the nodes: Y_0 bounds ||A F(bar x)||_X where F is the residual of
the INTERPOLANT as a function on (0, pi).  Those differ, and they differ for a
reason that is structural rather than numerical: Omega H(Omega) is a product of
two degree-<J trigonometric polynomials, hence degree < 2J, and collocation
enforces J conditions on it.  The other half is aliasing, it is invisible to the
Newton solve by construction, and it is exactly what Y_0 is made of.

So `interpolant_residual` evaluates the continuum residual of the Newton profile
at arbitrary theta -- every ingredient exactly, no quadrature and no finite
differences -- and the leg's measurement is its weighted norm.

Plain float64 (longdouble in one assembly).  Nothing here is interval-enclosed
and nothing is rigorous.
"""

import numpy as np

from solver.decay_collocation import Collocation


# ---------------------------------------------------------------------------
# the velocity integrals
# ---------------------------------------------------------------------------


def velocity_integrals(theta, K, dtype=np.longdouble):
    """I_k(theta) = int_0^theta sin(kt)/(1+cos t) dt for k = 0..K-1.

    Shape (len(theta), K).  Assembled in `dtype` (longdouble by default: the
    recursion loses ~eps * k^2 absolute, which in float64 is 1e-7 at K ~ 1600)
    and returned as float64.
    """
    th = np.atleast_1d(np.asarray(theta, dtype=dtype))
    I = np.zeros((th.size, int(K)), dtype=dtype)
    if K > 1:
        I[:, 1] = np.log(dtype(2.0) / (dtype(1.0) + np.cos(th)))
    for k in range(1, int(K) - 1):
        I[:, k + 1] = (dtype(2.0) * (dtype(1.0) - np.cos(k * th)) / dtype(k)
                       - dtype(2.0) * I[:, k] - I[:, k - 1])
    return np.asarray(I, dtype=float)


def eval_matrices(theta_eval, J):
    """(cos_eval, sin_eval, I_eval) for degree-<J even trig polys at any theta.

    These are the three things needed to evaluate the interpolant, its conjugate
    and its velocity OFF the grid -- which is where the defect a certificate sees
    actually lives.
    """
    th = np.atleast_1d(np.asarray(theta_eval, dtype=float))
    k = np.arange(J)
    return (np.cos(np.outer(th, k)), np.sin(np.outer(th, k)),
            velocity_integrals(th, J))


# ---------------------------------------------------------------------------
# the operator with the a-term
# ---------------------------------------------------------------------------


class ACollocation(Collocation):
    """The v4 collocation layer plus the gCLM a-transport, on the same grid.

    `a = 0` reproduces `Collocation` exactly (gate 2 checks it), so the Route-D
    bound layer keeps operating on the same object it always has.
    """

    def __init__(self, J, a=0.0):
        super().__init__(J)
        self.a = float(a)
        # U = V @ Omega, V = I_k(theta_j) @ (coefficients of Omega)
        self.V = velocity_integrals(self.theta, J) @ self.to_coef

    # -- the equation ------------------------------------------------------
    def residual_a(self, om, c):
        """R = Omega H(Omega) - c Omega_X - a U Omega_X, nodal."""
        omX = self.transport @ om
        R = om * (self.H @ om) - c * omX
        if self.a != 0.0:
            R = R - self.a * (self.V @ om) * omX
        return R

    def jacobian_a(self, om, c):
        """dR/dOmega as a dense J x J matrix (exact, no quadrature)."""
        omX = self.transport @ om
        M = (np.diag(self.H @ om) + om[:, None] * self.H
             - c * self.transport)
        if self.a != 0.0:
            M = M - self.a * (omX[:, None] * self.V
                              + (self.V @ om)[:, None] * self.transport)
        return M

    def dc_column_a(self, om):
        return -(self.transport @ om)

    # -- the continuum residual of the interpolant -------------------------
    def interpolant_residual(self, om, c, theta_eval):
        """R evaluated at ARBITRARY theta from the interpolant of `om`.

        Every ingredient is exact: p = sum A_k cos k theta, H p = sum A_k sin k
        theta, p_theta = -sum k A_k sin k theta, p_X = (1+cos theta) p_theta,
        U = sum A_k I_k.  Nothing is quadratured and nothing is differenced, so
        what comes back is the true residual of the true interpolant -- which is
        NOT zero between the nodes even after Newton has zeroed it on them.

        Returns (R, parts) with `parts` the pieces, for attribution.
        """
        A = self.to_coef @ np.asarray(om, dtype=float)
        Cm, Sm, Im = eval_matrices(theta_eval, self.J)
        k = np.arange(self.J)
        th = np.atleast_1d(np.asarray(theta_eval, dtype=float))
        p = Cm @ A
        Hp = Sm @ A
        p_th = -(Sm * k[None, :]) @ A
        p_X = (1.0 + np.cos(th)) * p_th
        U = Im @ A
        R = p * Hp - c * p_X
        if self.a != 0.0:
            R = R - self.a * U * p_X
        return R, {"p": p, "Hp": Hp, "p_X": p_X, "U": U}

    # -- the solve, in the certificate's own coordinates --------------------
    def newton_gauged(self, c=0.5, om0=None, drop=0, tol=1e-14, max_iter=60,
                      damping=True):
        """Newton on EXACTLY the system solver/decay_collocation gauges.

        `gauged_jacobian` builds M = [gauge row ; DF rows except `drop`] with the
        speed c FIXED, and A = M^{-1} is the approximate inverse every Route-D
        bound has been about.  So the Newton iteration for that same square
        system is x <- x - A F(x): the certificate's A IS the Newton matrix, and
        Y_0 = ||A F(bar x)|| is the size of the Newton step at the profile we
        hand over.  Solving it here rather than solving some other version of the
        profile equation is the whole point of the leg.

        Fixing c is what makes the system nonsingular: the zero set carries two
        symmetries at every a -- scaling (Omega, c) -> (lam Omega, lam c) and
        dilation Omega(X) -> Omega(X/mu) with c -> mu c (the a-term is dilation
        invariant because U picks up the mu that Omega_X loses) -- and fixing c
        kills the second while the gauge row kills the first.  Route-D v1 Q2 and
        v11 V0 both paid for finding that count the hard way.

        Returns the profile plus BOTH defects: the rows Newton enforced (machine
        zero, by construction) and the one row it does not see.
        """
        J = self.J
        g0 = self.to_coef.sum(axis=0)                 # evaluation at theta = 0
        rows = [j for j in range(J) if j != drop]
        om = self.anchor().copy() if om0 is None else np.asarray(om0, float).copy()

        def F_of(om):
            F = np.empty(J)
            F[0] = g0 @ om + 1.0
            F[1:] = self.residual_a(om, c)[rows]
            return F

        hist = []
        for _ in range(int(max_iter)):
            F = F_of(om)
            hist.append(float(np.max(np.abs(F))))
            if hist[-1] < tol:
                break
            M = np.empty((J, J))
            M[0, :] = g0
            M[1:, :] = self.jacobian_a(om, c)[rows, :]
            try:
                step = np.linalg.solve(M, -F)
            except np.linalg.LinAlgError:
                return {"converged": False, "reason": "singular gauged matrix",
                        "Omega": om, "c": c, "history": hist}
            t, base = 1.0, hist[-1]
            while damping and t > 1e-5:
                if np.max(np.abs(F_of(om + t * step))) < base:
                    break
                t *= 0.5
            om = om + t * step

        R = self.residual_a(om, c)
        src = om * (self.H @ om)
        scale = float(np.sqrt(np.mean(src ** 2))) or 1.0
        return {"converged": bool(hist[-1] < 1e-11), "Omega": om, "c": float(c),
                "drop": int(drop), "history": hist, "iterations": len(hist) - 1,
                "kept_sup": float(np.max(np.abs(R[rows]))),
                "dropped_defect": float(abs(R[drop])),
                "relres": float(np.sqrt(np.mean(R ** 2)) / scale)}

    def newton(self, om0=None, c0=0.5, tol=1e-13, max_iter=40, damping=True):
        """Newton on (Omega, c) with the TWO gauges the degeneracy demands.

        The zero set carries two symmetries at EVERY a: scaling
        (Omega, c) -> (lam Omega, lam c) and dilation Omega(X) -> Omega(X/mu)
        with c -> mu c (the a-term is dilation invariant because U picks up the
        mu that Omega_X loses).  Route-D v1 Q2 and v11 V0 both paid for finding
        this the hard way: with one gauge the Jacobian is singular and Newton
        crawls.  Two gauge rows against J residual rows and J+1 unknowns is
        overdetermined by one and solved in least squares -- Gauss-Newton, still
        quadratic at a zero residual.

        Gauges: Omega(theta=0) = -1 (spectral, theta=0 is not a node) and
        Omega at the node nearest X = 1 equals -1/2, both satisfied by the exact
        a = 0 anchor.
        """
        J = self.J
        i1 = int(np.argmin(np.abs(self.X - 1.0)))
        g0 = self.to_coef.sum(axis=0)                  # evaluation at theta = 0
        om = self.anchor().copy() if om0 is None else np.asarray(om0, float).copy()
        c = float(c0)
        hist = []

        def full(om, c):
            F = np.empty(J + 2)
            F[:J] = self.residual_a(om, c)
            F[J] = g0 @ om + 1.0
            F[J + 1] = om[i1] + 0.5
            return F

        for _ in range(int(max_iter)):
            F = full(om, c)
            hist.append(float(np.sqrt(np.mean(F[:J] ** 2))))
            if np.max(np.abs(F)) < tol:
                break
            Jm = np.zeros((J + 2, J + 1))
            Jm[:J, :J] = self.jacobian_a(om, c)
            Jm[:J, J] = self.dc_column_a(om)
            Jm[J, :J] = g0
            Jm[J + 1, i1] = 1.0
            try:
                step = np.linalg.lstsq(Jm, -F, rcond=None)[0]
            except np.linalg.LinAlgError:
                return {"converged": False, "reason": "singular Jacobian",
                        "Omega": om, "c": c, "history": hist}
            t, base = 1.0, float(np.max(np.abs(F)))
            while damping and t > 1e-4:
                if np.max(np.abs(full(om + t * step[:J], c + t * step[J]))) < base:
                    break
                t *= 0.5
            om, c = om + t * step[:J], c + t * step[J]

        R = self.residual_a(om, c)
        rms = float(np.sqrt(np.mean(R ** 2)))
        hist.append(rms)
        src = om * (self.H @ om)
        rel = rms / float(np.sqrt(np.mean(src ** 2))) if np.any(src) else np.inf
        return {"converged": bool(rel < 1e-9), "Omega": om, "c": c,
                "residual_rms": rms, "relres": rel, "history": hist,
                "iterations": len(hist) - 1,
                "nodal_sup": float(np.max(np.abs(R)))}


def continuation(a_values, J=400, **kw):
    """Follow the branch in a, warm-starting from the previous solution."""
    out, om, c = [], None, 0.5
    for a in a_values:
        col = ACollocation(J, a=float(a))
        r = col.newton(om0=om, c0=c, **kw)
        if r["relres"] > 1e-10:
            alt = col.newton(om0=None, c0=0.5, **kw)
            if alt["relres"] < r["relres"]:
                r = alt
        out.append({"a": float(a), "converged": r["converged"], "c": r["c"],
                    "relres": r["relres"], "residual_rms": r["residual_rms"],
                    "iterations": r["iterations"], "Omega": r["Omega"]})
        if r["relres"] < 1e-10:
            om, c = r["Omega"], r["c"]
    return out


# ---------------------------------------------------------------------------
# the defect a certificate actually sees
# ---------------------------------------------------------------------------


def effective_speed(X, U, c, a):
    """E(X) = c + a U(X): the coefficient of -Omega_X in the residual.

    At a = 0 this is the constant c and the far field is pure transport at fixed
    speed -- the picture eleven Route-D legs were built on.  At a > 0 it is NOT
    constant, because U = int_0^X H(Omega) inherits the Hilbert transform's
    logarithm: H(Omega) ~ (int Omega)/(pi X) for large X, so U ~ (int Omega/pi)
    log X, and int Omega < 0 for a negative-signed profile.  E therefore DECREASES
    without bound and crosses zero at a finite radius.
    """
    return np.asarray(c, dtype=float) + float(a) * np.asarray(U, dtype=float)


def critical_radius(X, E):
    """The smallest X > 0 where E changes sign, by linear interpolation (inf if none).

    This is the radius the a-family's own velocity picks out, and it is where the
    profile ends: the leading balance Omega H(Omega) = E Omega_X with E ~ -a h_c
    (X_c - X) forces Omega ~ (X_c - X)^{1/a}, an algebraic ZERO of order 1/a.
    """
    X = np.asarray(X, float)
    E = np.asarray(E, float)
    o = np.argsort(X)
    X, E = X[o], E[o]
    m = X > 0
    X, E = X[m], E[m]
    s = np.where(np.diff(np.sign(E)) != 0)[0]
    if s.size == 0:
        return float("inf")
    i = s[0]
    t = -E[i] / (E[i + 1] - E[i])
    return float(X[i] + t * (X[i + 1] - X[i]))


def zero_order(X, om, Xc, lo=0.5, hi=0.97, min_abs=1e-13):
    """Fitted p in |Omega| ~ (Xc - X)^p, over a window just inside Xc.

    The prediction is p = 1/a, from the leading balance alone (no fitting
    parameters).  Returns (p, number of points used).
    """
    X = np.asarray(X, float)
    om = np.asarray(om, float)
    if not np.isfinite(Xc):
        return float("nan"), 0
    m = (X > lo * Xc) & (X < hi * Xc) & (np.abs(om) > min_abs)
    if m.sum() < 5:
        return float("nan"), int(m.sum())
    lx = np.log(Xc - X[m])
    ly = np.log(np.abs(om[m]))
    o = np.argsort(lx)                       # closest to Xc first
    k = max(5, int(0.4 * o.size))
    return float(np.polyfit(lx[o][:k], ly[o][:k], 1)[0]), int(m.sum())


def refined_theta(J, refine=8, endpoint_pad=0.0):
    """A grid `refine` times finer than the J midpoint nodes, EXCLUDING them.

    The nodes are where the residual has been zeroed, so including them only
    dilutes the sup.  `endpoint_pad` (in units of the fine spacing) trims points
    nearest theta = pi, where the interpolant's failure to decay is a separate
    defect (v7 V6) and the codomain weight is unbounded.
    """
    M = int(J) * int(refine)
    th = np.pi * (np.arange(M) + 0.5) / M
    node = np.pi * (np.arange(J) + 0.5) / J
    keep = np.min(np.abs(th[:, None] - node[None, :]), axis=1) > 1e-12
    th = th[keep]
    if endpoint_pad > 0:
        th = th[th < np.pi - endpoint_pad * np.pi / M]
    return th


def weighted_defect(col, om, c, alpha, refine=8, theta_eval=None):
    """(sup_w |R| off the nodes, the argmax theta, the fine grid, R) at weight alpha+1.

    The codomain of the Route-D pair is the decay class X^{-(alpha+1)}, so the
    sup part of ||F||_Y is sup (1+X^2)^{(alpha+1)/2} |R|.
    """
    th = refined_theta(col.J, refine) if theta_eval is None else np.asarray(theta_eval, float)
    R, _ = col.interpolant_residual(om, c, th)
    w = (1.0 + np.tan(0.5 * th) ** 2) ** (0.5 * (alpha + 1.0))
    wr = w * np.abs(R)
    i = int(np.argmax(wr))
    return float(wr[i]), float(th[i]), th, R
