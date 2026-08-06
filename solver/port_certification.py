"""ROUTE K v1: the L1->L2 certification port, step one -- can the 2D profile be certified?

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS
--------------------------------------------------------------------------
Ranked item (3) -- port the certification programme from 1D gCLM to 2D Boussinesq in the
Hou-Luo geometry, where computer-assisted proofs of blow-up actually exist -- has been
deferred **six** times in favour of cheaper measurement legs.  This is the first leg that
does not defer it.

The directive named four deliverables: (1) the Newton-Kantorovich setup on the 2D profile,
with the function space chosen with Route-D's `a = 0`-only disaster in mind; (2) an honest
`Y_0`; (3) a first bound on `Z_1`/`||A||`; (4) **the kill-switch -- if the radii polynomial
does not close in float with margin, STOP and report, do not harden.**

**The kill-switch fires at (2), before the function space is even reached.**  This module
is the measurement that fires it, plus the controls that make it a statement about the
OBJECT rather than about our instrument.

--------------------------------------------------------------------------
THE CHAIN, AND WHERE IT BREAKS
--------------------------------------------------------------------------
A radii-polynomial argument needs, in order:

    (i)   a fixed profile  x*  of the steady equation  F(x) = 0 ;
    (ii)  Y_0 >= ||A F(x*)||          -- the DEFECT of that profile ;
    (iii) A, an approximate inverse of DF(x*), with  Z_1 >= ||I - A DF|| < 1 ;
    (iv)  the polynomial  Z_2 r^2 - (1 - Z_1) r + Y_0 <= 0  having a root.

**(i) does not exist yet, and (iii) cannot be started.**  Both are measured here.

**(i) THE RELAXATION HAS NO FIXED POINT AT THIS DISCRETIZATION.**  `RescaledBoussinesq.run`
is an SSPRK3 relaxation toward a steady state.  It does not converge -- it LIMIT-CYCLES.
Measured over a steps ladder the sup residual goes 0.98 -> 0.21 -> 0.026 -> 0.23 while
`c_omega` swings between -1.015 and -1.239 (`c_l/c_omega` between -3.02 and -2.47, around
the published -2.9206).  And Route-G's own committed resolution ladder is worse than a
plateau: the steady residual **GROWS under refinement**, 1.7e-2 -> 7.7e-2 -> 2.7e-1 at
`n_r = 300/450/600`.  A defect is the defect OF something.  **`Y_0` is not large here; it is
undefined.**

**(iii) DF HAS NO COMPUTABLE APPROXIMATE INVERSE.**  A matrix-free Krylov solve of
`DF x = -F` stalls.  Linearizing at the BEST point of the limit cycle (3000 steps,
`||F||_2 = 0.807`), the relative linear residual is **0.6946 at Krylov dimension 10 and
0.6623 at 160**.  Sixteen times the work buys five percent.  **The flatness is the
informative part.**  A merely ill-conditioned operator lets GMRES accelerate once it has
captured the extreme eigenvalues; a residual that is flat in Krylov dimension is the
signature of a spectrum with a CONTINUUM in it, not of a large condition number -- and the
rescaled operator's essential spectrum is exactly what Route-E measured in 1D and what
Route-J's lesson (70) says to name the realization of.  `A` cannot be built, so `Z_1` cannot
be bounded, so there is no radii polynomial to close or fail to close.

**AND THE STALL IS SEED-DEPENDENT, WHICH IS THE SHARPEST FORM OF THE FINDING.**  Linearize
instead at the WORST point of the cycle (5000 steps, `||F||_2 = 11.11`) and the same ladder
reads **0.2695 -> 0.2450** -- still flat, but at a level 2.7x lower, and the preconditioner
below buys **1.03x there against 1.84x at the best point**.  Neither number is *the* answer,
because "linearize at the profile" has no referent when there is no profile.  **`Z_1` is not
large and is not small; it is not about anything.**

--------------------------------------------------------------------------
THE CONTROLS -- WHY THIS IS THE OBJECT AND NOT US
--------------------------------------------------------------------------
Both failures above are the kind that a broken instrument produces, so neither is reported
without its control (banked lesson 47).

* **The GMRES is correct.**  The same routine solves a well-conditioned dense system to
  **7.6e-11 in 19 iterations**, and on a deliberately `cond ~ 1e8` dense system it stalls at
  **0.086 after 200** -- i.e. its failure mode on ill-conditioning is known, and the observed
  stall is worse than that.
* **The finite-difference Jacobian-vector product is trustworthy.**  `||Jv||` is **65.140**
  and stable across five decades of step size, `h/||z|| = 1e-4 ... 1e-9`, with relative
  change `5e-7` at the optimum.  The matvec is not the noise floor.

--------------------------------------------------------------------------
THE ONE REPAIR WITH A PRINCIPLED BASIS, TRIED -- AND WHAT IT BOUGHT
--------------------------------------------------------------------------
The continuum's natural source is the dilation term: at large `r` the transport speed
`s_rho -> c_l`, so the leading operator is `-c_l d_rho + (diagonal damping)`, whose spectrum
on a log-radial grid fills a band.  That operator is **exactly invertible** -- upwinded, it
is lower bidiagonal along each angular line, `O(N)` -- so it is the obvious right
preconditioner, and it is the same move Chen-Hou describe in their own abstract
(arXiv:2210.07191: *"we decompose the linearized operator into a leading order operator plus
a finite rank operator"*).

**It helps and it does not fix it: at the best point of the cycle the stall goes 0.6623 ->
0.3596 at Krylov dimension 160, and the curve is still flat (0.4463 at 10).**  Nearly halving
the stalled residual says the dilation continuum is a real and identified part of the
obstruction; the curve staying flat says there is a second obstruction of comparable size
that the leading-order operator does not touch -- the nonlocal Biot-Savart velocity and the
wall are the candidates, and separating them is the next leg, not this one.  At the worst
point of the cycle the same preconditioner buys almost nothing (0.2450 -> 0.2367), which is
the seed-dependence again and is why the improvement factor is reported at both seeds rather
than averaged into one.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* **Not a proof that the 2D profile cannot be certified.**  It is a measurement that OUR
  discretization does not admit the first two steps of the argument, with the mechanism
  named.  Chen-Hou certified this object; they did it with a different decomposition and
  145 pages.  The gap between "our grid cannot" and "it cannot" is the whole distance.
* **Not a criticism of Route-G's number.**  `c_omega` is resolution-stable to 0.77% across
  the ladder whose RESIDUAL grows by 16x, which is a real and slightly uncomfortable fact:
  the modulation reads a converging quantity off a non-converging object.  Route-G's
  `beta = 2.98 +- 0.02` against the published 2.9206 is **2.1% out, which its own quoted
  spread does not cover**, and this leg is why.
* Plain float64.  Nothing is interval-enclosed and nothing here is rigorous.
* **No link of the L1->L4 chain moved.**  A blocked link is not a moved link.
"""

import numpy as np

from solver.certificate_guards import (
    NAN_HINT_GE_ONE, hypothesis_violations as _shared_hypothesis_violations)

# --------------------------------------------------------------------------
# a small dependency-free GMRES (there is no scipy in this environment)
# --------------------------------------------------------------------------
def gmres(matvec, b, m=60, tol=1e-10):
    """Plain restart-free GMRES.  Returns (x, relative_residual, krylov_dim_used).

    Reported as a MAGNITUDE (the relative residual), never as converged/not (lesson 58) --
    the whole point of this module is a solve that neither converges nor blows up, and a
    boolean would erase exactly the number that carries the finding.
    """
    b = np.asarray(b, float)
    n = b.size
    beta0 = float(np.linalg.norm(b))
    if beta0 == 0.0:
        return np.zeros_like(b), 0.0, 0
    Q = np.zeros((m + 1, n))
    H = np.zeros((m + 1, m))
    Q[0] = b / beta0
    used = m
    for k in range(m):
        w = matvec(Q[k])
        for i in range(k + 1):                      # modified Gram-Schmidt
            H[i, k] = Q[i] @ w
            w = w - H[i, k] * Q[i]
        H[k + 1, k] = np.linalg.norm(w)
        if H[k + 1, k] < 1e-14:
            used = k + 1
            break
        Q[k + 1] = w / H[k + 1, k]
        e1 = np.zeros(k + 2)
        e1[0] = beta0
        y, *_ = np.linalg.lstsq(H[:k + 2, :k + 1], e1, rcond=None)
        rel = float(np.linalg.norm(H[:k + 2, :k + 1] @ y - e1) / beta0)
        if rel < tol:
            return Q[:k + 1].T @ y, rel, k + 1
    e1 = np.zeros(used + 1)
    e1[0] = beta0
    y, *_ = np.linalg.lstsq(H[:used + 1, :used], e1, rcond=None)
    rel = float(np.linalg.norm(H[:used + 1, :used] @ y - e1) / beta0)
    return Q[:used].T @ y, rel, used


def gmres_controls(seed=0, n=300, m=200):
    """The instrument's own gates: a well-conditioned solve and a cond ~ 1e8 solve.

    Without these, "GMRES stalled" is a statement about our code.  With them it is a
    statement about the operator, and the ill-conditioned control also calibrates what
    ill-conditioning alone looks like -- which turns out to be BETTER than what we see.
    """
    rng = np.random.default_rng(seed)
    b = rng.standard_normal(n)
    A = np.eye(n) + 0.3 * rng.standard_normal((n, n)) / np.sqrt(n)
    x, rel, k = gmres(lambda v: A @ v, b, m=m, tol=1e-10)
    good = {"rel_reported": rel, "rel_true": float(np.linalg.norm(A @ x - b)
                                                   / np.linalg.norm(b)), "k": k}
    D = np.diag(np.logspace(0.0, 8.0, n))
    A2 = D @ (np.eye(n) + 0.1 * rng.standard_normal((n, n)) / np.sqrt(n))
    _, rel2, k2 = gmres(lambda v: A2 @ v, b, m=m, tol=1e-10)
    return {"well_conditioned": good,
            "cond_1e8": {"rel": rel2, "k": k2, "cond_target": 1e8},
            "note": ("the well-conditioned solve gates correctness; the cond~1e8 solve "
                     "calibrates what ill-conditioning ALONE costs, so a worse stall on the "
                     "real Jacobian cannot be explained by conditioning")}


# --------------------------------------------------------------------------
# the residual map, packed/unpacked, and its matrix-free Jacobian
# --------------------------------------------------------------------------
class ProfileResidual:
    """F(omega, eta, xi) = the rescaled Boussinesq RHS, i.e. zero at a self-similar profile.

    Packs the triple into one vector so the Newton-Kantorovich vocabulary (`F`, `DF`, `A`)
    applies literally rather than by analogy.
    """

    def __init__(self, solver, grid):
        self.solver = solver
        self.grid = grid
        self.shape = (grid.rho.size, grid.beta.size)
        self.N = self.shape[0] * self.shape[1]

    def pack(self, o, e, x):
        return np.concatenate([np.ravel(o), np.ravel(e), np.ravel(x)])

    def unpack(self, z):
        N, sh = self.N, self.shape
        return (z[:N].reshape(sh), z[N:2 * N].reshape(sh), z[2 * N:].reshape(sh))

    def F(self, z):
        o, e, x = self.unpack(z)
        Ro, Re, Rx, _ = self.solver.rhs(o, e, x)
        return self.pack(Ro, Re, Rx)

    def info(self, z):
        o, e, x = self.unpack(z)
        _, _, _, inf = self.solver.rhs(o, e, x)
        return inf

    def jacobian_vector(self, z, Fz, rel_h=1e-7):
        """Matrix-free DF(z) v by forward differences, with the step scaled by ||z||/||v||."""
        nz = float(np.linalg.norm(z))

        def Jv(v):
            nv = float(np.linalg.norm(v))
            h = rel_h * nz / (nv + 1e-300)
            return (self.F(z + h * v) - Fz) / h

        return Jv

    def jv_step_study(self, z, Fz, v, decades=(1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9)):
        """Is the matvec trustworthy?  ||Jv|| across five decades of h, with the drift.

        This is the control that separates "the operator resists inversion" from "our
        directional derivative is noise".  Reported as magnitudes at every rung.
        """
        nz = float(np.linalg.norm(z))
        v = np.asarray(v, float)
        v = v / np.linalg.norm(v)
        rows, prev = [], None
        for hrel in decades:
            h = hrel * nz
            Jv = (self.F(z + h * v) - Fz) / h
            row = {"h_rel": hrel, "h_abs": h, "norm_Jv": float(np.linalg.norm(Jv))}
            if prev is not None:
                row["rel_change_vs_previous_h"] = float(
                    np.linalg.norm(Jv - prev) / np.linalg.norm(Jv))
            rows.append(row)
            prev = Jv
        return rows


# --------------------------------------------------------------------------
# the leading-order preconditioner -- the one repair with a principled basis
# --------------------------------------------------------------------------
def leading_order_solve(rhs, c_l, drho, c_diag):
    """Exact inverse of (-c_l d_rho + c_diag) along the radial axis, upwinded outward.

    At large r the advection speed s_rho -> c_l (bounded outward dilation), so this is the
    leading part of DF away from the origin.  Backward-differencing d_rho makes the operator
    LOWER BIDIAGONAL per angular line, hence exactly invertible in O(N) with no factorization
    and no iteration -- which is what makes it usable as a preconditioner inside a matvec.

    This is the same move Chen-Hou describe (arXiv:2210.07191 abstract): split the linearized
    operator into a leading-order part designed to be sharply estimable, plus a remainder.
    """
    a = c_l / drho
    denom = c_diag - a
    out = np.zeros_like(rhs)
    prev = np.zeros(rhs.shape[1])
    for i in range(rhs.shape[0]):
        prev = (rhs[i] - a * prev) / denom
        out[i] = prev
    return out


def make_preconditioner(res, c_l, c_omega):
    """Right preconditioner M^{-1}: the leading-order inverse on each of the three fields.

    The diagonal damping differs per field -- c_omega for omega, 2 c_omega for eta and xi --
    which is read off the rescaled system's reaction terms, not fitted.
    """
    drho = res.grid.drho

    def Minv(v):
        o, e, x = res.unpack(v)
        return res.pack(leading_order_solve(o, c_l, drho, c_omega),
                        leading_order_solve(e, c_l, drho, 2.0 * c_omega),
                        leading_order_solve(x, c_l, drho, 2.0 * c_omega))

    return Minv


def krylov_ladder(matvec, b, dims=(10, 20, 40, 80, 160)):
    """Relative linear residual against Krylov dimension.

    THE LADDER IS THE MEASUREMENT, not the final number.  A merely ill-conditioned operator
    gives a curve that BENDS DOWN once the extreme eigenvalues are captured; a curve that is
    flat in the Krylov dimension is the signature of a continuum in the spectrum.  Reporting
    only the m = 160 value would hide exactly that distinction.
    """
    rows = []
    for m in dims:
        _, rel, k = gmres(matvec, b, m=m, tol=1e-12)
        rows.append({"m": int(m), "k": int(k), "rel_residual": float(rel)})
    return rows


def stall_verdict(rows):
    """Flat-or-bending, as a magnitude: how much does 16x the Krylov work buy?

    **THE TWO ROWS ARE SELECTED BY `m`, NOT BY POSITION (leg 244).**  Until this repair the
    function read `rows[0]` and `rows[-1]`, so the verdict was a property of how the caller
    happened to store the array rather than of the measurement.  Every banked ladder is
    stored ascending in `m`, so no published number was ever wrong -- but the margin was
    exactly `0.0` (leg 243): reverse Route-L's `full transport line sweep` ladder and the
    residual gain reads 0.1028 (flat) instead of 9.7245 (bending), a 94.56x error that flips
    the verdict the Route-L headline rests on, and an arbitrary shuffle flips it too.
    Keying on `m` makes the verdict a function of the DATA, so every permutation of the same
    rows returns the same answer and the correctness stops being incidental.

    `m` is the Krylov dimension, so it is the ladder's own parameter and it is already
    carried in every row `krylov_ladder` emits -- no caller and no call site has to change,
    including the deep rung's inline `dims=(240, 320)`.

    Two rows sharing an `m` but disagreeing on `rel_residual` is a malformed ladder: there is
    no order-free way to say which one the verdict means, so this raises rather than silently
    picking one (lesson 58 -- do not manufacture an answer the data does not contain).
    Duplicated rows that agree exactly are harmless and are accepted.
    """
    rows = list(rows)
    if not rows:
        raise ValueError("stall_verdict needs at least one ladder row; got an empty ladder")
    by_m = {}
    for r in rows:
        m = r["m"]
        seen = by_m.get(m)
        if seen is not None and seen["rel_residual"] != r["rel_residual"]:
            raise ValueError(
                "ambiguous ladder: m = %r appears twice with different rel_residual "
                "(%r and %r), so the verdict is not a function of the data" % (
                    m, seen["rel_residual"], r["rel_residual"]))
        by_m[m] = r
    first, last = by_m[min(by_m)], by_m[max(by_m)]
    gain = first["rel_residual"] / last["rel_residual"]
    return {"rel_at_min_dim": first["rel_residual"], "min_dim": first["m"],
            "rel_at_max_dim": last["rel_residual"], "max_dim": last["m"],
            "work_ratio": last["m"] / first["m"], "residual_gain": float(gain),
            "flat": bool(gain < 2.0),
            "reading": ("flat in Krylov dimension => a continuum in the spectrum, not a "
                        "large condition number" if gain < 2.0 else
                        "bending => finite ill-conditioning, and more Krylov work would help")}


# --------------------------------------------------------------------------
# the kill-switch
# --------------------------------------------------------------------------
def _hypothesis_violations(Y0, Z1, Z2):
    """Which hypothesis of the radii polynomial theorem each supplied constant breaks.

    `Y_0`, `Z_1`, `Z_2` are UPPER BOUNDS ON NORMS in the theorem this function implements
    (van den Berg-Lessard, *Rigorous Numerics in Dynamics*, AMS Notices 62(9):1057, 2015;
    Hungria-Lessard-Mireles James, Math. Comp.):

        ||T(x)-x|| <= Y_0 ,      sup ||A(DF(x+rv) - A_dagger)u|| <= Z_1 + Z_2 r ,

    hence **finite and nonnegative by hypothesis**.  A negative or non-finite constant is
    therefore not a conservative input -- it is an input the imported theorem says nothing
    about, and evaluating the discriminant on it asserts a contraction on data no run could
    have produced (leg 79 measured 11 such inputs coming back `closes=True`).

    `None` means NOT MEASURED and is a legitimate input by design -- it is the whole point of
    the kill-switch -- so it is never a violation and is handled by the branches below.

    Returns a list of strings naming the offending constant and the hypothesis it breaks.
    The offending VALUES are deliberately not echoed into the returned dict's `Y0`/`Z1` keys:
    a rejected fabrication must not be reported in the same slot as a measured bound.

    SINCE LEG 128 THIS DELEGATES to `solver.certificate_guards.hypothesis_violations`, the
    one guard all three radii-polynomial pipelines share.  The predicate, the message
    strings and the `None`-is-NOT-MEASURED policy are unchanged byte-for-byte; what changed
    is that `interval_certificate.py` and `nk_bounds.py` now read the SAME predicate instead
    of a copy of it.  `allow_none=True` is this module's kill-switch semantics and is the
    reason the shared guard takes the flag at all.
    """
    return _shared_hypothesis_violations(
        (("Y_0", Y0), ("Z_1", Z1), ("Z_2", Z2)),
        allow_none=True, nan_hint=NAN_HINT_GE_ONE)


def radii_polynomial_status(Y0, Z1, Z2=None):
    """Where the argument stands.  Refuses to invent a number it does not have.

    Y0 or Z1 given as None means NOT MEASURABLE -- which is the actual situation here and is
    a stronger statement than a large value.  The function returns that, rather than
    substituting a bound and reporting a failure that would look like a merely quantitative
    shortfall.

    Constants that ARE supplied are checked against the theorem's own hypotheses first
    (`_hypothesis_violations`): a negative or non-finite `Y_0`/`Z_1`/`Z_2` returns
    `INVALID_INPUT` with `closes=False`, never `EVALUATED`.  The blocked branch is tested
    BEFORE that check, so `(None, None, <anything>)` still reports BLOCKED_AT_STEP_ONE --
    a poisoned `Z_2` must not be allowed to convert "no bounds at all" into "bad bounds".
    """
    if Y0 is None and Z1 is None:
        return {"status": "BLOCKED_AT_STEP_ONE",
                "closes": False,
                "why": ("no fixed profile (the relaxation limit-cycles and its residual grows "
                        "under refinement), so Y_0 is undefined; and no approximate inverse A "
                        "(the Krylov solve stalls), so Z_1 cannot be bounded. There is no "
                        "radii polynomial to evaluate.")}
    violations = _hypothesis_violations(Y0, Z1, Z2)
    if violations:
        return {"status": "INVALID_INPUT", "closes": False, "violations": violations,
                "why": ("outside the hypotheses of the radii polynomial theorem (Y_0, Z_1, Z_2 "
                        "are upper bounds on norms, hence finite and nonnegative): "
                        + "; ".join(violations)
                        + ". These constants cannot have come from a certificate run; no "
                          "discriminant is evaluated.")}
    if Z1 is None:
        return {"status": "NO_Z1", "closes": False, "Y0": Y0,
                "why": "A could not be constructed; Z_1 is unbounded-by-construction, not large."}
    if Z1 >= 1.0:
        return {"status": "Z1_EXCEEDS_ONE", "closes": False, "Y0": Y0, "Z1": Z1,
                "why": "the contraction factor is not a contraction; do not harden, report."}
    if Z2 is None:
        return {"status": "NO_Z2", "closes": False, "Y0": Y0, "Z1": Z1,
                "why": "quadratic term unmeasured."}
    disc = (1.0 - Z1) ** 2 - 4.0 * Z2 * Y0
    return {"status": "EVALUATED", "closes": bool(disc >= 0.0), "Y0": Y0, "Z1": Z1,
            "Z2": Z2, "discriminant": float(disc)}


# --------------------------------------------------------------------------
# ROUTE L v1 -- the attribution, and the preconditioner it names
# --------------------------------------------------------------------------
# Route-K left the port with the stall attributed only in part: the leading-order RADIAL
# dilation split took the Krylov stall 0.6623 -> 0.3596 and the curve stayed FLAT, so a
# second obstruction of comparable size was present and unidentified.  Route-K named two
# candidates -- the nonlocal Biot-Savart velocity, and the wall.
#
# **BOTH GUESSES WERE WRONG, AND THE ABLATION SAYS SO CLEANLY.**  Freezing the velocity
# feedback makes the stall WORSE (0.6623 -> 0.7582): the nonlocal term is mildly helping the
# Krylov solve, not obstructing it.  And the stalled Krylov residual is not concentrated at
# the wall for omega or eta (6.8% and 7.9% of the energy in the first three of forty-eight
# angular nodes, i.e. about proportional).
#
# **IT IS THE ANGULAR TRANSPORT.**  Switch off s_beta d_beta and the ladder BENDS
# (0.7857 -> 0.3712, gain 2.12 against the full problem's 1.05); switch it off AND apply the
# radial preconditioner and the solve runs to MACHINE ZERO (0.0401 -> 0.0 by m = 80).  So the
# transport operator carries the entire obstruction, in two pieces -- one radial, one angular
# -- and nothing else in the equation contributes.
#
# **AND THE FIX FOLLOWS FROM THE STRUCTURE.**  ADI-style composition of two exact 1D solves
# is NOT the answer and measurably makes things worse (0.996): the operator does not split.
# But the radial upwinding is OUTWARD everywhere on this profile (measured s_rho in
# [0.390, 5.732], strictly positive), which makes the full transport operator **block lower
# bidiagonal in the radial index with TRIDIAGONAL diagonal blocks** -- so ONE outward sweep of
# Thomas inverts it exactly, in O(N), with no splitting error at all.  That is
# `line_sweep_solve`, and with it the stall goes
#
#     0.6623 (flat, gain 1.05)  ->  0.0188 at m = 160, 2.0e-4 at m = 240, 3.3e-6 at m = 320
#
# i.e. the curve stops being flat.  **A is constructible.**  The certification chain's step
# (iii) is no longer blocked.

def line_sweep_solve(rhs, s_rho, s_beta, drho, dbeta, c_diag, thomas):
    """EXACT O(N) inverse of (-s_rho d_rho - s_beta d_beta + c_diag), first-order upwind.

    Requires s_rho > 0 (outward radial upwinding), which is what makes the operator block
    lower-bidiagonal in the radial index:

        [(c_diag - s_rho/drho) I - s_beta d_beta] f_i  =  rhs_i - (s_rho/drho) f_{i-1}

    Each diagonal block is TRIDIAGONAL (the angular upwind picks the sub- or super-diagonal
    pointwise by the sign of s_beta), so one outward sweep of Thomas is an exact solve.

    **This is not ADI and the difference is the whole point.**  Composing an exact radial
    solve with an exact angular solve carries a splitting error, and measured on this problem
    that error is catastrophic -- the preconditioned stall goes to 0.996, WORSE than doing
    nothing.  Sweeping the coupled operator has no splitting error because there is no split.

    `thomas` is injected rather than imported so this module keeps no dependency on the
    Boussinesq solver package.
    """
    rhs = np.asarray(rhs, float)
    nr, nb = rhs.shape
    out = np.empty_like(rhs)
    prev = np.zeros(nb)
    for i in range(nr):
        sr = s_rho[i] / drho
        sb = s_beta[i]
        a = np.zeros(nb)
        b = np.full(nb, float(c_diag)) - sr
        c = np.zeros(nb)
        pos = sb > 0
        a[pos] = sb[pos] / dbeta
        b[pos] -= sb[pos] / dbeta
        b[~pos] += sb[~pos] / dbeta
        c[~pos] = -sb[~pos] / dbeta
        a[0] = 0.0
        c[-1] = 0.0
        prev = thomas(a, b, c, rhs[i] - sr * prev)
        out[i] = prev
    return out


def outward_upwinding_holds(s_rho):
    """The line sweep's one precondition, reported as a MAGNITUDE, not a boolean.

    If any s_rho <= 0 the radial ordering is not a valid sweep direction there and the solve
    stops being exact.  Return the minimum so a marginal case is visible rather than binary.
    """
    m = float(np.min(s_rho))
    return {"min_s_rho": m, "max_s_rho": float(np.max(s_rho)), "holds": bool(m > 0.0)}


def attribution_summary(ladders):
    """Rank the ablations by how much each one un-flattens the ladder.

    `ladders` maps a label to a krylov_ladder result.  The discriminant is the GAIN across
    the ladder (lesson 72: the shape, not the endpoint) -- an ablation that removes the
    obstruction makes the curve bend, which shows up as a gain well above the full problem's.
    """
    out = []
    base = stall_verdict(ladders["full"])["residual_gain"]
    for label, rows in ladders.items():
        v = stall_verdict(rows)
        out.append({"ablation": label, "rel_at_max_dim": v["rel_at_max_dim"],
                    "gain": v["residual_gain"], "flat": v["flat"],
                    "gain_vs_full": v["residual_gain"] / base,
                    "worse_than_full": v["rel_at_max_dim"] > ladders["full"][-1]["rel_residual"]})
    out.sort(key=lambda q: -q["gain"])
    return out
