"""Newton on the two-scale profile equation -- the OTHER side of the inequality.

Ten Route-D legs have worked on the constants of the radii polynomial.  v10
finally measured what that can buy: a perfect upper bound on ||A|| multiplies the
conditional budget by 7.7 and no more, C_Q's own slack is ~4x, and the product
only just reaches the residual floor of ~1e-2 with nothing spare.  So the
constants alone cannot close the gap.

The other factor has never been touched.  The budget condition is Y0 <= Y0_max:
Y0 is the DEFECT of the candidate profile -- how badly it fails to solve the
equation -- and every a != 0 profile this project has produced came from a GA
over a small parametric genome, or from fixed-grid dynamic relaxation, both of
which floor around 1e-2 (banked discipline lesson).  Nobody has asked what a
NEWTON solve on the full grid does, and Y0 enters the radii polynomial linearly:
a profile with defect 1e-8 needs no sharpening of any constant at all.

--------------------------------------------------------------------------
THE SYSTEM
--------------------------------------------------------------------------
The two-scale (traveling-wave) residual of the gCLM a-family (PHASE2_P2_NOTES
section 9) is

    R2(Omega, c) = Omega H(Omega) - c Omega_X - a U Omega_X ,   U = int_0^X H(Omega)

with the exact a = 0 anchor Omega = -1/(1+X^2), c = 1/2.  R2 has a one-parameter
SCALING degeneracy -- Omega -> lambda Omega solves with c -> lambda c -- so the
Newton system needs one gauge; the natural one is the amplitude Omega(0) = -1,
which the anchor already satisfies.  Unknowns are then (Omega, c), n + 1 of them,
against n residual equations plus that gauge.

The Jacobian is exact and assembled from the operators the family already caches:

    dR2/dOmega . h = h H(Omega) + Omega H(h) - c h_X
                     - a [ (V H h) Omega_X + (V H Omega) h_X ]
    dR2/dc         = -Omega_X

with V the cached velocity (integration) matrix.  Everything is dense n x n;
n = 1201 solves in a fraction of a second, so a whole a-sweep is cheap.

--------------------------------------------------------------------------
WHAT A NEGATIVE WOULD MEAN (state it before running)
--------------------------------------------------------------------------
Newton has no genome and no relaxation dynamics, so if the residual still floors
at ~1e-2 for a != 0, that floor is a property of the EQUATION on this grid, not
of the search -- which would be a much stronger statement than the GA could make,
and would say the a != 0 traveling wave does not exist rather than that we failed
to find it.  If instead Newton drives the defect to discretization level, the
whole budget arithmetic changes and the constants stop being the bottleneck.
Either way the leg is decisive, which is why it is worth doing before any more
estimate work.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
"""

import numpy as np

from solver.gclm_family import GCLMResidual, _drho_centered4


def derivative_matrix(fam):
    """d/dX as a dense matrix on the family's grid (4th-order centred in rho)."""
    n = fam.n
    D = np.empty((n, n))
    e = np.zeros(n)
    for j in range(n):
        e[:] = 0.0
        e[j] = 1.0
        D[:, j] = _drho_centered4(e, fam.drho) / fam.X_rho
    return D


class TwoScaleNewton:
    """Newton solve of R2(Omega, c) = 0 with the amplitude gauge Omega(0) = -1."""

    def __init__(self, a=0.0, n=1201, rho_max=8.0):
        self.fam = GCLMResidual(a=a, n=n, rho_max=rho_max)
        self.a = float(a)
        self.D = derivative_matrix(self.fam)
        self.H = self.fam.Hmat
        self.VH = self.fam.Vmat @ self.fam.Hmat        # Omega -> U
        self.i0 = self.fam.i0
        # The a = 0 zero set is a TWO-parameter family (every A/(1+B X^2) solves,
        # PHASE2_P2_NOTES section 9), which Route-D v1 Q2 already found the hard
        # way: exactly two gauge conditions isolate a nondegenerate zero.  One
        # gauge leaves the Jacobian singular and Newton crawls (2e-5 after 40
        # iterations instead of machine zero).  Gauge 1 fixes the amplitude at
        # X = 0, gauge 2 the width, via the value at X ~ 1.
        self.i1 = int(np.argmin(np.abs(self.fam.X - 1.0)))

    # -- the objects -------------------------------------------------------
    def anchor(self):
        """The exact a = 0 traveling wave, on this grid."""
        return -1.0 / (1.0 + self.fam.X ** 2)

    def residual(self, om, c):
        R = om * (self.H @ om) - c * (self.D @ om)
        if self.a != 0.0:
            R = R - self.a * (self.VH @ om) * (self.D @ om)
        return R

    def jacobian(self, om, c):
        """(n+1) x (n+1): dR2 rows plus the gauge row, columns (Omega, c)."""
        n = self.fam.n
        omX = self.D @ om
        M = np.diag(self.H @ om) + om[:, None] * self.H - c * self.D
        if self.a != 0.0:
            M = M - self.a * (omX[:, None] * self.VH
                              + (self.VH @ om)[:, None] * self.D)
        Jm = np.zeros((n + 2, n + 1))
        Jm[:n, :n] = M
        Jm[:n, n] = -omX
        Jm[n, self.i0] = 1.0                    # gauge 1: amplitude
        Jm[n + 1, self.i1] = 1.0                # gauge 2: width
        return Jm

    # -- the solve ---------------------------------------------------------
    def solve(self, om0=None, c0=0.5, tol=1e-13, max_iter=40, damping=True):
        """Newton with a simple backtracking line search.

        Returns a dict with the profile, the speed, the residual RMS history and
        `converged`.  A failure is reported, never quietly returned as success.
        """
        om = self.anchor().copy() if om0 is None else np.asarray(om0, float).copy()
        c = float(c0)
        hist = []
        n = self.fam.n
        for _ in range(int(max_iter)):
            R = self.residual(om, c)
            F = np.empty(n + 2)
            F[:n] = R
            F[n] = om[self.i0] + 1.0            # gauge 1: Omega(0) = -1
            F[n + 1] = om[self.i1] + 0.5        # gauge 2: Omega(1) = -1/2
            rms = float(np.sqrt(np.mean(R ** 2)))
            hist.append(rms)
            if np.max(np.abs(F)) < tol:
                break
            try:
                # (n+2) x (n+1): two gauges against n residual rows plus c, so
                # the system is overdetermined by one and solved in least
                # squares.  Gauss-Newton still converges quadratically to a zero
                # residual when one exists, and degrades gracefully when the
                # second gauge is redundant (which it is once a != 0 breaks the
                # dilation symmetry).
                step = np.linalg.lstsq(self.jacobian(om, c), -F, rcond=None)[0]
            except np.linalg.LinAlgError:
                return {"converged": False, "reason": "singular Jacobian",
                        "Omega": om, "c": c, "history": hist}
            t = 1.0
            base = np.max(np.abs(F))
            while damping and t > 1e-4:
                om_t, c_t = om + t * step[:n], c + t * step[n]
                Ft = np.max(np.abs(np.concatenate(
                    [self.residual(om_t, c_t), [om_t[self.i0] + 1.0,
                                                om_t[self.i1] + 0.5]])))
                if Ft < base:
                    break
                t *= 0.5
            om, c = om + t * step[:n], c + t * step[n]
        R = self.residual(om, c)
        rms = float(np.sqrt(np.mean(R ** 2)))
        hist.append(rms)
        src = om * (self.H @ om)
        rel = rms / float(np.sqrt(np.mean(src ** 2))) if np.any(src) else np.inf
        return {"converged": bool(hist[-1] < 1e-6 * max(1.0, hist[0])
                                  or hist[-1] < 1e-9),
                "Omega": om, "c": c, "residual_rms": rms, "relres": rel,
                "history": hist, "iterations": len(hist) - 1}


def continuation(a_values, n=1201, rho_max=8.0, **kw):
    """Sweep `a`, warm-starting each solve from the previous solution.

    Continuation is the point: the a != 0 profile (if it exists) is a deformation
    of the exact a = 0 anchor, so the honest test is to follow it rather than to
    search for it, which is what every earlier leg did.
    """
    out = []
    om, c = None, 0.5
    for a in a_values:
        nw = TwoScaleNewton(a=float(a), n=n, rho_max=rho_max)
        r = nw.solve(om0=om, c0=c, **kw)
        if r["relres"] > 1e-10:
            # The warm start can land in a basin where the line search crawls.
            # Retrying from the exact a = 0 anchor costs one solve and rescues
            # it often enough to be worth doing -- and when BOTH starts stall,
            # that is evidence about the equation rather than about the start.
            alt = nw.solve(om0=None, c0=0.5, **kw)
            if alt["relres"] < r["relres"]:
                r = alt
        out.append({"a": float(a), "converged": r["converged"],
                    "residual_rms": r["residual_rms"], "relres": r["relres"],
                    "c": r["c"], "iterations": r["iterations"]})
        if r["relres"] < 1e-10:
            om, c = r["Omega"], r["c"]
    return out
