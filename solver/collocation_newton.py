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
                      damping=True, relres_tol=1.0):
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

        REPAIR (leg 150, from leg 114's M1/M2).  `converged` used to be read off
        `hist[-1]` alone -- i.e. off the (J-1)-row subsystem Newton actually
        solves -- so it was structurally True for ANY root of that subsystem,
        however large the dropped row's residual and however far the profile is
        from the decay class the Route-D bounds live in.  It now ALSO requires
        `relres`, which this method already computed over all J rows including
        the dropped one and then never consulted, to have a referent and to be
        below `relres_tol` (default 1.0: the residual must be smaller than the
        source term it is supposed to cancel).

        Leg 150's novelty pass measured the two obvious alternatives dead before
        this one was written: an ABSOLUTE clause on `dropped_defect` moves clean
        a-family solves (they legitimately carry 8.5e-05 .. 8.0e-02 there, which
        is the aliasing this module's own docstring is about), and the decay
        predicate |Omega(theta=pi)| closes to 7.4x between a clean a=0.5/J=240
        solve (0.105) and M1's spurious root (0.779).  `relres` separates 249x:
        clean worst 5.05e-02 against 1.257e+01 / 1.322e+01 / 1.314e+01 on the
        three spurious roots.

        The pre-repair flag is NOT discarded -- it is returned unchanged as
        `converged_kept_rows`, so every number leg 114 measured is still readable
        off this dict.  No float this method returns changes value.
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
                # LEG 150: carry the normal path's keys so callers cannot KeyError
                # on the failure branch (leg 114's incomplete-dict gap).
                return {"converged": False, "converged_kept_rows": False,
                        "relres_has_referent": False,
                        "reason": "singular gauged matrix",
                        "Omega": om, "c": float(c), "drop": int(drop),
                        "history": hist, "iterations": max(len(hist) - 1, 0),
                        "kept_sup": float("nan"), "dropped_defect": float("nan"),
                        "relres": float("nan")}
            t, base = 1.0, hist[-1]
            while damping and t > 1e-5:
                if np.max(np.abs(F_of(om + t * step))) < base:
                    break
                t *= 0.5
            om = om + t * step

        R = self.residual_a(om, c)
        src = om * (self.H @ om)
        src_rms = float(np.sqrt(np.mean(src ** 2)))
        # LEG 150.  The old `scale = ... or 1.0` fabricated a referent of exactly
        # 1.0 out of an identically-zero source scale, so a profile with NOTHING
        # to converge to could still report a relative residual.  When a quantity
        # has no referent, say so instead of bounding it.  On every case where the
        # old fallback did NOT fire (src_rms > 0) the expression below is the
        # pre-repair expression unchanged, hence bit-identical.
        has_referent = src_rms > 0.0
        relres = (float(np.sqrt(np.mean(R ** 2)) / src_rms) if has_referent
                  else float("nan"))
        # max_iter=0 left `hist` empty and `hist[-1]` raised IndexError, where the
        # sibling `newton` returns.  Evaluate the residual at the start point.
        kept_last = hist[-1] if hist else float(np.max(np.abs(F_of(om))))
        converged_kept = bool(kept_last < 1e-11)
        full_ok = bool(has_referent and relres < float(relres_tol))
        if not converged_kept:
            reason = "the gauged (J-1)-row subsystem did not converge"
        elif not has_referent:
            reason = ("relres has no referent: the source scale ||Omega H(Omega)|| "
                      "is identically zero, so the residual equation is degenerate")
        elif not full_ok:
            reason = (f"the gauged subsystem converged (kept_sup {kept_last:.3e}) but the "
                      f"FULL residual over all {J} rows does not: relres = {relres:.4e} "
                      f">= relres_tol = {float(relres_tol):.4e}")
        else:
            reason = None
        return {"converged": bool(converged_kept and full_ok),
                "converged_kept_rows": converged_kept,
                "relres_has_referent": bool(has_referent),
                "reason": reason,
                "Omega": om, "c": float(c),
                "drop": int(drop), "history": hist,
                "iterations": max(len(hist) - 1, 0),
                "kept_sup": float(np.max(np.abs(R[rows]))),
                "dropped_defect": float(abs(R[drop])),
                "relres": relres}

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
                # LEG 150: the same shape as the normal return, so `continuation`
                # (which indexes r["relres"] unconditionally) flags the failure
                # instead of dying with KeyError.
                return {"converged": False, "reason": "singular Jacobian",
                        "Omega": om, "c": c, "history": hist,
                        "iterations": max(len(hist) - 1, 0),
                        "residual_rms": float("nan"), "relres": float("inf"),
                        "nodal_sup": float("nan")}
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


def _run_extent(E, i, step):
    """max |E| over the maximal constant-sign run containing index `i`, walking `step`.

    Returns None if the run contains a non-finite value, i.e. "this leg cannot judge
    the magnitude here" -- which is kept distinct from "the magnitude is small".
    """
    s0 = np.sign(E[i])
    j, best = i, 0.0
    while 0 <= j < E.size:
        if not np.isfinite(E[j]):
            return None
        if np.sign(E[j]) != s0:
            break
        best = max(best, abs(float(E[j])))
        j += step
    return best


def critical_radius(X, E, min_rel_depth=1e-2, min_isolation=3):
    """The smallest X > 0 where E changes sign, by linear interpolation (inf if none).

    This is the radius the a-family's own velocity picks out, and it is where the
    profile ends: the leading balance Omega H(Omega) = E Omega_X with E ~ -a h_c
    (X_c - X) forces Omega ~ (X_c - X)^{1/a}, an algebraic ZERO of order 1/a.

    REPAIR (leg 150, from leg 114's M3).  The crossing test used to be the bare
    `np.diff(np.sign(E)) != 0`, which carries no magnitude information at all: an
    E that is 0.5 everywhere with ONE entry dipped to -1e-16 returned
    X_c = 15.025019 where the truth is `inf`, and the answer moved by only 1.0e-04
    across thirteen decades of dip depth.  A crossing is now accepted only if the
    constant-sign excursion on EACH side of it reaches `min_rel_depth * max|E|`
    -- leg 114's own prescription, "a magnitude threshold on the crossing relative
    to |E|".  Both sides, because one side is measurably not enough: a one-point
    dip is rejected on its far side and then readmitted one index later through
    its own re-crossing back up, whose far side is the whole clean field.

    Leg 150 measured the tempting alternative (require the new sign to be
    SUSTAINED for more than one node) dead first: a real crossing at a = 0.15 has
    run length 1, identical to the adversary.  The relative depth separates where
    the run length does not -- worst real field 1.229e-01, worst adversary
    2.0e-03, so the default 1e-2 sits 12.3x below the first and 5.0x above the
    second.  `min_rel_depth=0.0` reproduces the pre-repair answer exactly.

    Non-finite E is NOT swallowed: a crossing whose endpoints are not both finite
    is interpolated as before, so a poisoned field still returns nan rather than
    being quietly reclassified as "no crossing".

    REPAIR 2 (leg 0/BENCH, from leg 166's `pure_sign_noise`).  The relative-depth
    guard above is SCALE-INVARIANT: for `E = (-1)^k` every constant-sign run is
    exactly one node long with `|E| = 1 = max|E|`, so the excursion ratio on both
    sides is exactly 1.0 -- the largest value the test can ever observe.  Leg 166
    measured 0 of 15 thresholds separate that field from all 8 real crossings on
    the relative-depth predicate alone, because the predicate never looks at
    anything but a single crossing's own local magnitude.

    What the relative-depth test cannot see, a purely COMBINATORIAL count does:
    pure alternating-sign noise does not have one candidate crossing, it has one
    on almost every node (799 of 799 possible positions in leg 166's construction),
    while every real crossing this module has ever produced is the ONLY sign
    change anywhere in its field.  `min_isolation` requires that no OTHER sign
    change lie within that many nodes of the candidate -- a test that counts
    nodes, never magnitudes, so it is scale-free in the sense the relative-depth
    guard is not: it does not care what `|E|` equals anywhere.  It is gated the
    same way the magnitude guard is (`thresh > 0.0`, i.e. off at
    `min_rel_depth=0.0`), so the pre-repair reproduction path is untouched, and it
    is checked in addition to the magnitude test, so it can only ever REJECT a
    crossing the magnitude test alone would have accepted -- never re-admit one
    the magnitude test rejected.  Measured: every real crossing in the a-family
    (a in [0.15, 0.5]) is the sole sign change in its field (gap = inf, trivially
    >= any `min_isolation`); leg 114's M3 one-point dip has its two sign changes
    one node apart (gap = 1); pure sign noise has every sign change one node from
    its neighbour (gap = 1 throughout).  The default `min_isolation=3` sits
    comfortably above both adversaries' gap of 1 and below "no other crossing
    anywhere" for every measured real field.
    """
    X = np.asarray(X, float)
    E = np.asarray(E, float)
    o = np.argsort(X)
    X, E = X[o], E[o]
    m = X > 0
    X, E = X[m], E[m]
    sgn = np.sign(E)
    s = np.where(np.diff(sgn) != 0)[0]
    thresh = float(min_rel_depth) * float(np.max(np.abs(E))) if E.size else 0.0
    for pos in range(s.size):
        i = int(s[pos])
        if not (np.isfinite(E[i]) and np.isfinite(E[i + 1])):
            # poison propagates, exactly as pre-repair
            t = -E[i] / (E[i + 1] - E[i])
            return float(X[i] + t * (X[i + 1] - X[i]))
        if thresh > 0.0:
            # BOTH sides must be resolved.  Testing only the far side is not enough
            # and leg 150 measured why: a one-point dip has an unresolved run BELOW
            # the axis, which that test correctly rejects -- and then the field's
            # own re-crossing back UP one index later has a fully resolved far side,
            # so the same artifact is readmitted through the other door.  The
            # excursion on each side of a real crossing reaches `thresh`.
            lo = _run_extent(E, i, -1)
            hi = _run_extent(E, i + 1, +1)
            # a run this leg cannot judge (non-finite) is NOT quietly reclassified
            # as "no crossing" -- the magnitude test simply does not apply to it,
            # and (leg 166's OTHER, separately-tracked known gap) neither does the
            # isolation test below: both stay gated on the SAME "fully resolved"
            # condition, so a poisoned run's fate is exactly what it was before
            # this repair -- untouched, on purpose, out of this repair's territory.
            if lo is not None and hi is not None:
                if min(lo, hi) < thresh:
                    continue                  # unresolved: a roundoff-scale dip
                # REPAIR 2: a genuine crossing is a LOCAL feature -- reject a
                # candidate that has another sign change within `min_isolation`
                # nodes.  This is the predicate outside the relative-depth class
                # leg 166 asked for; see the docstring above.
                if min_isolation > 0 and s.size > 1:
                    gap = np.min(np.abs(np.delete(s, pos) - i))
                    if gap < int(min_isolation):
                        continue              # not isolated: noise, not a crossing
        t = -E[i] / (E[i + 1] - E[i])
        return float(X[i] + t * (X[i + 1] - X[i]))
    return float("inf")


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
