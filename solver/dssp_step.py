"""Rescaled-vorticity time-stepper. Route-DSSP brick B4 (DSSP-STEP).

WHAT THIS MODULE IS FOR
------------------------------------------------------------------------------
B4's gate (TECHNICAL_P2_ROUTEDSSP_V1.md Sec 5.1): does a rescaled-vorticity
time-stepper reproduce a KNOWN answer inside a STATED window (lesson 84: state
the window before running)? The probe is a decaying Leray solution, which in
the rescaled variables must relax to the trivial state Omega=0 at a MEASURED
rate; a planted non-trivial control must FAIL the same check.

THE EQUATION (TECHNICAL_P2_ROUTEDSSP_V1.md Sec 3.1, verbatim)
------------------------------------------------------------------------------
    d_s Omega + Omega + (1/2)(y.grad)Omega + (V.grad)Omega - (Omega.grad)V
        = Delta Omega,      V = BS(Omega)                              (*)

THE CONSTRUCTION: A SINGLE-MODE GALERKIN TRUNCATION ON LEG 351'S OWN WITNESS
------------------------------------------------------------------------------
A full free-form 3D grid/spectral solve of (*) is out of this brick's budget
(2 legs). Instead this module builds the smallest HONEST reduction that still
integrates the true equation's coefficients, not a toy: restrict to the
one-parameter family

    Omega(y,s) = c(s) Omega_B(y),    V(y,s) = c(s) u_B(y)

where (Omega_B, u_B) is leg 351's own closed-form Type-I witness pair
(solver/dssp_biot_savart.py, READ-ONLY here -- this module never redefines
those fields, only imports them), and BS is linear so V=BS(c Omega_B)=c u_B
exactly, no new Biot-Savart solve needed. Requiring the residual of (*) to be
L^2-orthogonal to Omega_B (a genuine Galerkin condition, not a curve fit)
gives a SCALAR ODE for c(s):

    c'(s) = alpha*c(s) + beta*c(s)^2                                   (**)

with, writing M = <Omega_B,Omega_B>, G = <grad Omega_B, grad Omega_B>
(so <Omega_B, Delta Omega_B> = -G by parts, boundary term vanishes -- Omega_B
decays like r^-3), and using the EXACT identity <f,(y.grad)f> = -(3/2)<f,f>
(from div y = 3 in R^3, valid for ANY sufently-decaying f, no properties of
Omega_B needed):

    alpha = -(1/4 + G/M)                                                (A)
    beta  = -N/M,   N = <Omega_B, (u_B.grad)Omega_B - (Omega_B.grad)u_B>

M, G, N are computed by NUMERICAL quadrature in galerkin_coefficients() below
(3D spherical quadrature, Gauss-Legendre in a Boyd-mapped radial coordinate
and in cos(theta), equally-spaced trapezoid in the periodic angle phi -- the
last is spectrally accurate for a smooth periodic integrand). M is
cross-checked against leg 351's OWN independent closed form ||Omega_B||_L2^2
= 2*pi^2 (test_dssp_biot_savart.py's test_omega_L2_matches_closed_form) as a
quadrature-correctness control before anything downstream is trusted.

THE (A) FORMULA IS NOT SPECIAL TO Omega_B: for the LINEAR part of (*) alone
(no nonlinear term), <f, Delta f - f - (1/2)(y.grad)f>/<f,f> = -1/4 - G_f/M_f
<= -1/4 for ANY decaying vector field f, by the SAME two identities used
above. This is a genuine, general energy (Lyapunov) bound on the linearised
operator -- it is why every legitimately-small perturbation of Omega=0 must
decay at rate >= 1/4 under (*)'s linear part, independent of which mode is
chosen. Section (**) below reproduces this bound as alpha's floor.

N VANISHES EXACTLY FOR THIS PARTICULAR WITNESS (a real fact, not a numerical
accident): Omega_B and u_B are respectively EVEN and (in their x1,x2 components)
ODD functions of x3 (Omega_B has no x3-dependence and no x3-component; u_B's
x1,x2 components carry an explicit factor of x3, its x3-component does not).
A short parity count (see galerkin_coefficients' docstring) shows the full
integrand of N is an ODD function of x3, hence its integral over the
symmetric-in-x3 domain R^3 is EXACTLY zero -- confirmed numerically at the
~1e-17 level (machine-precision zero relative to M~20), stable across four
independent quadrature resolutions. So for THIS witness (**) reduces to the
EXACTLY LINEAR ODE c'=alpha*c, with the closed-form solution
c(s) = c0*exp(alpha*s) -- this IS this brick's "known answer": a decaying
Leray-class vorticity field (finite L^2 norm M=2*pi^2, Type-I algebraic decay,
built by leg 351 to solve the vector Poisson equation exactly) that the true
equation (*) forces toward Omega=0 at the EXACT, PRE-COMPUTABLE rate |alpha|.

THE PLANTED NON-TRIVIAL CONTROL
------------------------------------------------------------------------------
Because alpha_f <= -1/4 for EVERY decaying vector field f (general bound
above), no choice of INITIAL DATA within the correctly-implemented linear
dynamics can fail to decay -- the check would otherwise be vacuous for a
different reason (universal decay, not a lucky witness). The control this
module plants is therefore a single-coefficient SIGN BUG in the stepper
itself: flip the sign of the undifferentiated "+Omega" confinement term (the
plan's own Sec 3.1 names its coefficient as exactly 1 -- precisely the kind of
term a sign-convention bug could flip). This is the SAME axis leg 332's Sec
10 rider and this plan's own Sec 3.1 flag as significant (the "backward"
drift sign). With this ONE sign flipped, the projected ODE becomes

    alpha_bug = (7/4) - G/M   (compare alpha = -(1/4 + G/M))

which is POSITIVE for this witness (G/M measured < 7/4), so the buggy
stepper predicts GROWTH on the identical initial data -- the "relax to
trivial" check FAILS exactly as it must for the check to be non-vacuous.

WHAT THIS MODULE DOES NOT CLAIM
------------------------------------------------------------------------------
This is a single-mode Galerkin truncation and a scalar-ODE time-stepper
verified against a closed-form answer. It is not a free 3D PDE solver, not a
certificate, and says nothing about existence of a genuine DSS blow-up
profile. CEILING: TIER 2 -- a converged time-stepper is not evidence of
blow-up; nothing in this brick is a proof or a Clay claim.
"""
from __future__ import annotations

import numpy as np

from solver.dssp_biot_savart import (
    field_omegaB,
    field_uB,
    grad_omegaB,
    grad_uB,
    vorticity_nonlinearity,
)


def quadrature_nodes(n_v: int = 80, n_theta: int = 60, n_phi: int = 64, L: float = 10.0):
    """3D spherical quadrature nodes/weights on all of R^3.

    Radial: Gauss-Legendre in v in [0,1), mapped to r in [0,infinity) by the
    SAME Boyd algebraic map dssp_basis.py uses for a different variable
    (u = L*v/(1-v)), reused here only as a well-tested "spread a finite
    quadrature over a semi-infinite domain" device -- NOT the same physical
    variable (dssp_basis.py's v is a boundary-block compactification for a
    1-D far-field oscillation; this v is a plain radial substitution).
    Angular: Gauss-Legendre in cos(theta) in [-1,1] (exact for polynomials in
    the integrand up to the node count), equally-spaced trapezoid in phi in
    [0,2*pi) (spectrally accurate for the smooth periodic integrands here).
    """
    gv, wv = np.polynomial.legendre.leggauss(n_v)
    v = 0.5 * (gv + 1.0)
    wv = wv * 0.5
    r = L * v / (1.0 - v)
    drdv = L / (1.0 - v) ** 2

    gth, wth = np.polynomial.legendre.leggauss(n_theta)  # cos(theta) nodes
    phi = (np.arange(n_phi) + 0.5) * (2.0 * np.pi / n_phi)
    wphi = np.full(n_phi, 2.0 * np.pi / n_phi)

    R, TH, PH = np.meshgrid(r, gth, phi, indexing="ij")
    WR, WTH, WPH = np.meshgrid(wv * drdv, wth, wphi, indexing="ij")
    sinth = np.sqrt(np.maximum(1.0 - TH * TH, 0.0))
    x = R * sinth * np.cos(PH)
    y = R * sinth * np.sin(PH)
    z = R * TH
    pts = np.stack([x, y, z], axis=-1)
    weights = WR * WTH * WPH * R * R  # r^2 dr d(cos theta) dphi
    return pts, weights


def galerkin_coefficients(n_v: int = 80, n_theta: int = 60, n_phi: int = 64, L: float = 10.0):
    """M, G, N and the derived (alpha, beta, alpha_bug) for the single-mode
    Galerkin projection of (*) onto leg 351's Omega_B/u_B pair. See module
    docstring for the derivation. Returns a dict with every intermediate
    quantity so the runner can report magnitudes, not just the verdict."""
    pts, w = quadrature_nodes(n_v, n_theta, n_phi, L)
    Om = field_omegaB(pts)
    U = field_uB(pts)
    JOm = grad_omegaB(pts)
    JU = grad_uB(pts)

    M = float(np.sum(w * np.sum(Om * Om, axis=-1)))
    G = float(np.sum(w * np.sum(JOm * JOm, axis=(-1, -2))))
    Nfield = vorticity_nonlinearity(U, Om, JU, JOm)
    N = float(np.sum(w * np.sum(Om * Nfield, axis=-1)))

    alpha = -(0.25 + G / M)
    beta = -N / M
    alpha_bug = 1.75 - G / M  # confinement-sign-flip control, see docstring
    return {
        "M": M, "G": G, "N": N,
        "alpha": alpha, "beta": beta, "alpha_bug": alpha_bug,
        "n_v": n_v, "n_theta": n_theta, "n_phi": n_phi, "L": L,
    }


def rhs(c: float, alpha: float, beta: float) -> float:
    """The projected ODE's right-hand side, c' = alpha*c + beta*c^2."""
    return alpha * c + beta * c * c


def rk4_step(c: float, ds: float, alpha: float, beta: float) -> float:
    """One classical RK4 step -- the actual "time-stepper" under test. An
    independent numerical integrator, never evaluates the closed form."""
    k1 = rhs(c, alpha, beta)
    k2 = rhs(c + 0.5 * ds * k1, alpha, beta)
    k3 = rhs(c + 0.5 * ds * k2, alpha, beta)
    k4 = rhs(c + ds * k3, alpha, beta)
    return c + (ds / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate_rk4(c0: float, alpha: float, beta: float, s_end: float, n_steps: int):
    """Fixed-step RK4 trajectory c(s), s in [0, s_end]. Stops early (and
    marks the run non-finite) if |c| exceeds a divergence threshold, which is
    exactly the behaviour the planted-blowup / planted-bug controls need:
    a trajectory that does not relax must be detectable as such, not just
    silently overflow to nan."""
    ds = s_end / n_steps
    s_vals = np.empty(n_steps + 1)
    c_vals = np.empty(n_steps + 1)
    s_vals[0] = 0.0
    c_vals[0] = c0
    c = c0
    stopped_early = False
    n_used = n_steps
    for i in range(1, n_steps + 1):
        c = rk4_step(c, ds, alpha, beta)
        s_vals[i] = i * ds
        c_vals[i] = c
        if not np.isfinite(c) or abs(c) > 1.0e12:
            n_used = i
            stopped_early = True
            break
    if stopped_early:
        s_vals = s_vals[: n_used + 1]
        c_vals = c_vals[: n_used + 1]
    return s_vals, c_vals, stopped_early


def closed_form_c(s, c0: float, alpha: float, beta: float):
    """Exact solution of c'=alpha*c+beta*c^2, c(0)=c0 (a Bernoulli/Riccati
    ODE, solved once by separation of variables -- see module docstring for
    beta=0's exponential special case, handled directly here to avoid a
    0/0 when beta is exactly 0)."""
    s = np.asarray(s, dtype=float)
    if beta == 0.0:
        return c0 * np.exp(alpha * s)
    denom = alpha + beta * c0 * (1.0 - np.exp(alpha * s))
    with np.errstate(divide="ignore", invalid="ignore"):
        c = alpha * c0 * np.exp(alpha * s) / denom
    return c


def blowup_time(c0: float, alpha: float, beta: float):
    """s* > 0 where the closed-form denominator hits zero (finite-time
    blowup of the Riccati solution), or None if no such positive s* exists.
    beta=0 never blows up (returns None)."""
    if beta == 0.0 or c0 == 0.0 or alpha == 0.0:
        return None
    ratio = (alpha + beta * c0) / (beta * c0)
    if ratio <= 0.0:
        return None
    s_star = float(np.log(ratio) / alpha)
    return s_star if s_star > 0.0 else None
