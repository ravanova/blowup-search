"""STATUS: WORK IN PROGRESS -- DOES NOT CONVERGE YET. NO TEST FILE. DO NOT USE.

Committed only so it is not lost with the container.  A smoke run
(FiniteSupportProfile(a=0.3, K=16, N=800).solve()) reports converged=False with
residual 1.4 after 59 iterations (0.63 at a=0.5), and _hilbert_matrix emits a
RuntimeWarning about invalid values in the log term -- so nothing here is
validated and no number it produces should be quoted.  The X_c it currently
lands on (5.17 at a=0.3, 2.64 at a=0.5) is the right order but is NOT converged;
compare solver/advection_scope.stagnation_point, which measures the same crossing
by an independent route and IS gated (7.16 and 3.10, grid-stable to ~1%).

Before this is used for anything: make it converge, then add test_finite_support.py
with a known-answer gate, then re-run the smoke numbers above.

Original module docstring follows.

The profile on its own support: [0, X_c] with X_c an unknown -- the kill switch.

Route-D v12 found that the a > 0 two-scale profile ENDS at a finite radius X_c
(where E = c + aU crosses zero) with an algebraic zero of order 1/a, and that the
gauged inverse in the decay-graded space DIVERGES with J there.  v13 found why:
not a singularity at X_c -- the mode there vanishes like (X_c - X)^{+1/a} -- but a
mode that GROWS in the far field, h ~ (log(X/X_c))^{1/a}, against a domain space
that is a decay class.  A codimension-1 range obstruction that no refinement
touches, and one that bordering with the speed cannot fix (dilation is a symmetry,
so it supplies kernel, not range).

The repair that remains is to take the far field out of the DOMAIN.  Perturbations
supported in [0, X_c] have residuals supported there too -- every term of
R = Omega H(Omega) - E Omega_X carries a factor of Omega or Omega_X, even though
H(Omega) does not vanish outside -- so the problem closes on the support alone, and
a mode that grows at infinity has nowhere to live.

--------------------------------------------------------------------------
THE FORMULATION
--------------------------------------------------------------------------
Scale by the support radius: X = X_c v, v in [0, 1], and put the known behaviour
into the ansatz rather than asking a grid to resolve it,

    Omega(X) = -(1 - v^2)^p g(v) ,   p = 1/a ,   g even and smooth, g(0) = 1 ,

with g a truncated even Chebyshev series, g(v) = sum_k b_k T_{2k}(v).  The zero
order p is not fitted: v12 derived it from the leading balance with no free
constant and v13 measured it twice.

Everything the residual needs is X_c-free in the scaled variable, which is the
reason this formulation is cheap.  For even f supported in [-1, 1],

    Htilde(v) = (1/pi) p.v. INT_0^1 f(u) [ 1/(v-u) + 1/(v+u) ] du         (X_c cancels)
    Utilde(v) = INT_0^v Htilde ,      U(X_c v) = X_c Utilde(v)
    X_c R     = X_c f Htilde - (c + a X_c Utilde) f'                       (' = d/dv)

so the unknowns are (b, X_c) with c fixed -- fixing c is still what kills the
dilation symmetry, and X_c is now an explicit unknown rather than an output.

The principal value is taken by ONE subtraction, using the exact
p.v. INT_0^1 du/(v-u) = log(v/(1-v)):

    p.v. INT_0^1 f(u)/(v-u) du = INT_0^1 [f(u)-f(v)]/(v-u) du + f(v) log(v/(1-v)) .

The divided difference is smooth in the interior (f is analytic on (-1,1)), so the
only difficulty left is the algebraic endpoint (1-u)^p, which the Chebyshev
substitution u = (1 - cos t)/2 with the periodic trapezoid rule handles at a rate
that improves with p.  Gate 1 checks it against the exact family

    (1/pi) p.v. INT_{-1}^{1} sqrt(1-y^2) U_{n-1}(y) / (x - y) dy = T_n(x) ,

which pins the quadrature, the subtraction and the sign convention at once.

--------------------------------------------------------------------------
WHAT THE ANSWER MEANS (state it before running)
--------------------------------------------------------------------------
The kill switch is ||A|| against K.  Flat: the framing is repaired, the far field
is not needed, and eleven legs of decay grading, resonances and tail bounds were
solving a problem this formulation does not have.  Still divergent: the framing
needs replacing rather than repairing, and the alternative lanes become primary.
Either answer is worth the build; only one of them is worth continuing after.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np


# ---------------------------------------------------------------------------
# basis and quadrature
# ---------------------------------------------------------------------------


def even_cheb(K, v):
    """(T_{2k}(v), d/dv T_{2k}(v)) for k = 0..K-1, shape (len(v), K) each."""
    v = np.atleast_1d(np.asarray(v, float))
    n = 2 * np.arange(K)
    th = np.arccos(np.clip(v, -1.0, 1.0))
    T = np.cos(np.outer(th, n))
    # dT_n/dv = n U_{n-1}(v) = n sin(n th)/sin(th); the removable point v = +-1
    # is never a collocation node, and the limit n^2 is used if it shows up.
    s = np.sin(th)
    with np.errstate(divide="ignore", invalid="ignore"):
        dT = n[None, :] * np.sin(np.outer(th, n)) / s[:, None]
    bad = ~np.isfinite(dT)
    if bad.any():
        dT[bad] = np.broadcast_to((n ** 2).astype(float), dT.shape)[bad]
    return T, dT


def cheb_quad(N):
    """Nodes/weights on [0,1] via u = (1-cos t)/2 and the midpoint rule in t.

    Clusters at both endpoints, which is what an algebraic (1-u)^p factor wants,
    and avoids the endpoints themselves (where the weight vanishes anyway).
    """
    t = np.pi * (np.arange(N) + 0.5) / N
    return 0.5 * (1.0 - np.cos(t)), (np.pi / N) * 0.5 * np.sin(t)


# ---------------------------------------------------------------------------
# the finite-support Hilbert transform
# ---------------------------------------------------------------------------


class FiniteSupportOps:
    """Cached linear maps b -> (f, f', H, U) at a fixed set of evaluation points.

    `p` is the zero order (1/a), `K` the number of even Chebyshev modes, `N` the
    quadrature size.  Everything is assembled once; a Newton solve is then matrix
    algebra.
    """

    def __init__(self, p, K, v_eval, N=2000, n_int=400):
        self.p, self.K, self.N = float(p), int(K), int(N)
        self.v = np.atleast_1d(np.asarray(v_eval, float))
        self.u, self.w = cheb_quad(N)
        # basis on the quadrature grid and at the evaluation points
        Tq, _ = even_cheb(K, self.u)
        self.phi_q = ((1.0 - self.u ** 2) ** self.p)[:, None] * Tq        # (N, K)
        Tv, dTv = even_cheb(K, self.v)
        wv = (1.0 - self.v ** 2) ** self.p
        self.phi_v = wv[:, None] * Tv                                     # (M, K)
        self.dphi_v = (wv[:, None] * dTv
                       - (2.0 * self.p * self.v * (1.0 - self.v ** 2) ** (self.p - 1.0))[:, None] * Tv)
        self.H = self._hilbert_matrix(self.v)
        self.U = self._velocity_matrix(n_int)

    # -- the two integrals -------------------------------------------------
    def _hilbert_matrix(self, v):
        """(len(v), K) matrix of Htilde for each basis function.

        Htilde_k(v) = (1/pi)[ INT (phi_k(u)-phi_k(v))/(v-u) du
                              + phi_k(v) log(v/(1-v))
                              + INT phi_k(u)/(v+u) du ] .
        """
        v = np.atleast_1d(np.asarray(v, float))
        Tv, _ = even_cheb(self.K, v)
        phi_v = ((1.0 - v ** 2) ** self.p)[:, None] * Tv
        d = v[:, None] - self.u[None, :]                     # (M, N)
        d = np.where(np.abs(d) < 1e-300, 1e-300, d)
        reg = (self.phi_q.T[None, :, :] - phi_v.T.transpose(1, 0)[:, :, None])
        # reg[m, k, i] = phi_k(u_i) - phi_k(v_m)
        reg = np.transpose(self.phi_q)[None, :, :] - phi_v[:, :, None]
        near = (reg / d[:, None, :]) @ self.w                # (M, K)
        far = (np.transpose(self.phi_q)[None, :, :]
               / (v[:, None, None] + self.u[None, None, :])) @ self.w
        with np.errstate(divide="ignore", invalid="ignore"):
            lg = np.log(v / (1.0 - v))
        log_term = np.where(phi_v != 0.0, phi_v * lg[:, None], 0.0)
        return (near + log_term + far) / np.pi

    def _velocity_matrix(self, n_int):
        """(len(v), K) matrix of Utilde(v) = INT_0^v Htilde, by cumulative quadrature.

        Integrated on its own fine grid and interpolated to the evaluation points,
        so the accuracy of U does not inherit the spacing of the collocation nodes.
        """
        s = np.linspace(0.0, 1.0, int(n_int) + 1)[1:]        # keep the endpoint v = 1
        Hs = self._hilbert_matrix(s)                         # (n, K)
        grid = np.concatenate([[0.0], s])
        Hg = np.vstack([np.zeros((1, self.K)), Hs])          # Htilde(0) = 0 by parity
        cum = np.concatenate([np.zeros((1, self.K)),
                              np.cumsum(0.5 * (Hg[1:] + Hg[:-1])
                                        * np.diff(grid)[:, None], axis=0)])
        self._U_grid, self._U_cum = grid, cum
        out = np.empty((self.v.size, self.K))
        for k in range(self.K):
            out[:, k] = np.interp(self.v, grid, cum[:, k])
        return out

    def U_edge(self):
        """Utilde(1) = INT_0^1 Htilde, the vector needed by the free-boundary condition."""
        return self._U_cum[-1]

    # -- the equation ------------------------------------------------------
    def fields(self, b):
        """(f, f', H, U) at the evaluation points, for coefficients b."""
        return (-(self.phi_v @ b), -(self.dphi_v @ b),
                -(self.H @ b), -(self.U @ b))

    def residual(self, b, Xc, c):
        """X_c * R at the evaluation points (the X_c scaling is cosmetic)."""
        f, df, H, U = self.fields(b)
        return Xc * f * H - (c + a_times(self, Xc) * U) * df

    def jacobian(self, b, Xc, c):
        """d(X_c R)/d(b, X_c): (M, K+1), analytic."""
        f, df, H, U = self.fields(b)
        aXc = a_times(self, Xc)
        dfdb, ddfdb = -self.phi_v, -self.dphi_v
        dHdb, dUdb = -self.H, -self.U
        Jb = (Xc * (dfdb * H[:, None] + f[:, None] * dHdb)
              - (c + aXc * U)[:, None] * ddfdb
              - (aXc * dUdb) * df[:, None])
        JX = f * H - self.a * U * df
        return np.hstack([Jb, JX[:, None]])


def a_times(ops, Xc):
    """a * X_c, with `a` carried on the ops object (set by FiniteSupportProfile)."""
    return ops.a * Xc


# ---------------------------------------------------------------------------
# the profile
# ---------------------------------------------------------------------------


class FiniteSupportProfile:
    """Newton for (b, X_c) with c fixed, on the profile's own support."""

    def __init__(self, a, K=24, N=2000, c=0.5, n_int=400):
        self.a, self.c, self.K = float(a), float(c), int(K)
        self.p = 1.0 / float(a)
        # K - 1 interior collocation nodes: the residual is DEGENERATE at v = 1
        # (every term carries f or f', both of which vanish there), so a node at
        # the edge carries no information and the edge condition below takes its
        # place.  Counting: K + 1 unknowns (b, X_c) against K - 1 residual rows +
        # the amplitude gauge + the free-boundary condition.
        self.v = 0.5 * (1.0 - np.cos(np.pi * (np.arange(K - 1) + 0.5) / (K - 1)))
        self.ops = FiniteSupportOps(self.p, K, self.v, N=N, n_int=n_int)
        self.ops.a = self.a
        self.U1 = self.ops.U_edge()          # Utilde(1), for the free boundary

    def initial(self, Xc0=None):
        """b for g == 1 (so Omega = -(1-v^2)^p), and a starting radius."""
        b = np.zeros(self.K)
        b[0] = 1.0
        return b, (np.exp(self.c / self.a) if Xc0 is None else float(Xc0))

    def gauge(self, b):
        """g(0) - 1, with g(0) = sum_k b_k T_{2k}(0) = sum_k b_k (-1)^k."""
        return float(np.sum(b * (-1.0) ** np.arange(self.K)) - 1.0)

    def edge_condition(self, b, Xc):
        """E(X_c) = c + a X_c Utilde(1) = 0 -- what makes X_c the FREE BOUNDARY.

        It is not optional and it is not implied by the collocation rows.  Near
        the edge the balance is Omega H(Omega) = E Omega_X with Omega ~ A s^p:
        the left side is O(s^p) and the right is O(E(X_c) s^{p-1}), so a solution
        with an algebraic zero exists only where E vanishes.  Without this row the
        system has a whole family of spurious roots with the support edge in the
        wrong place -- which is exactly what the first draft found (X_c = 3.6, 0.79,
        0.17 at K = 12, 16, 24 instead of the 6.13 two other discretizations agree
        on).
        """
        return self.c + self.a * Xc * float(-(self.U1 @ b))

    def system(self, b, Xc):
        n = self.K - 1
        F = np.empty(self.K + 1)
        F[:n] = self.ops.residual(b, Xc, self.c)
        F[n] = self.gauge(b)
        F[n + 1] = self.edge_condition(b, Xc)
        return F

    def system_jacobian(self, b, Xc):
        n = self.K - 1
        M = np.zeros((self.K + 1, self.K + 1))
        M[:n, :] = self.ops.jacobian(b, Xc, self.c)
        M[n, :self.K] = (-1.0) ** np.arange(self.K)
        M[n + 1, :self.K] = -self.a * Xc * self.U1        # d/db of a X_c Utilde(1)
        M[n + 1, self.K] = self.a * float(-(self.U1 @ b))  # d/dX_c
        return M

    def solve(self, b0=None, Xc0=None, tol=1e-12, max_iter=60):
        b, Xc = self.initial(Xc0)
        if b0 is not None:
            b = np.asarray(b0, float).copy()
        hist = []
        for _ in range(int(max_iter)):
            F = self.system(b, Xc)
            hist.append(float(np.max(np.abs(F))))
            if hist[-1] < tol:
                break
            step = np.linalg.solve(self.system_jacobian(b, Xc), -F)
            t, base = 1.0, hist[-1]
            while t > 1e-6:
                bt, Xt = b + t * step[:self.K], Xc + t * step[self.K]
                if Xt > 0 and np.max(np.abs(self.system(bt, Xt))) < base:
                    break
                t *= 0.5
            b, Xc = b + t * step[:self.K], Xc + t * step[self.K]
        return {"b": b, "Xc": float(Xc), "history": hist,
                "residual": float(np.max(np.abs(self.system(b, Xc)))),
                "converged": bool(hist[-1] < 1e-8), "iterations": len(hist) - 1}

    # -- the kill switch ---------------------------------------------------
    def operator_norm(self, b, Xc):
        """||A||: induced sup-to-sup norm of the inverse of [dR/d(b,Xc) ; gauge].

        The domain is the coefficient vector, so the meaningful sup norm is on the
        FUNCTION it represents: rows are weighted by evaluating the perturbation
        (1-v^2)^p sum db_k T_{2k} on a fixed fine grid, and the X_c slot is
        measured relative to X_c itself.  Nothing here is graded by decay -- there
        is no far field to grade.
        """
        M = self.system_jacobian(b, Xc)
        A = np.linalg.inv(M)
        s = np.linspace(0.0, 1.0, 601)[:-1]
        T, _ = even_cheb(self.K, s)
        E = ((1.0 - s ** 2) ** self.p)[:, None] * T          # coefficients -> values
        img = np.vstack([E @ A[:self.K, :], A[self.K, :][None, :] / Xc])
        return float(np.max(np.abs(img).sum(axis=1)))

    def profile_values(self, b, Xc, n=400):
        v = np.linspace(0.0, 1.0, n)
        T, _ = even_cheb(self.K, v)
        f = -((1.0 - v ** 2) ** self.p) * (T @ b)
        return Xc * v, f
