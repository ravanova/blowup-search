"""3D Biot-Savart recovery of velocity from a Type-I-enveloped vorticity,
realised on the DSSP compactified radial variable. Route-DSSP brick B3
(DSSP-BS).

WHAT THIS MODULE IS FOR
------------------------------------------------------------------------------
Brick B3's gate (TECHNICAL_P2_ROUTEDSSP_V1.md Sec 5.1): does Biot-Savart
recovery of the velocity V from the vorticity Omega stay on the MULTIPLIER
side of the nonlocal-output rule (leg 334's named mechanism -- an algebraic
tail is fatal as a standalone summand, harmless as a bounded multiplier)?
Concretely: are ||V||_inf and ||grad V||_inf finite on a Type-I-enveloped
Omega, and is leg 332's mapping bound

    ||(V.grad)Omega - (Omega.grad)V|| <= ||V||_inf ||grad Omega|| + ||grad V||_inf ||Omega||

non-vacuous (ratio strictly inside (0,1)) in the UNWEIGHTED L^2(R^3) space
brick B1 pinned for vorticity (unlike leg 332's own witness, which worked in
a GAUSSIAN-weighted L^2(mu))?

THE CONSTRUCTION
------------------------------------------------------------------------------
A single closed-form witness vorticity, built to sit exactly on the Type-I
self-similar decay envelope (Chae-Wolf, arXiv:1610.09464 Thm 1.1),
|V(y)| <= C/(1+|y|):

    Omega_B(x) = 2 S(r) (-x_2, x_1, 0),   S(r) = (1+r^2)^{-3/2},  r = |x|,

an axisymmetric-swirl vorticity, exactly divergence-free by construction
(it is the curl of nothing computed here -- it is itself an algebraic,
NOT Gaussian, radial profile, chosen so 2p+s>d with p=2 (L^2), d=3 gives
margin s>-1, i.e. UNWEIGHTED L^2(R^3) already suffices for Omega_B and its
gradient with room to spare -- this is why B3 does not need leg 332's
Gaussian weight at all).

Velocity is recovered by solving the vector Poisson equation -Delta A =
Omega_B in the Coulomb gauge with the same axisymmetric swirl ansatz leg
332 used for its own witness, A = a(r) (x_2, -x_1, 0), which reduces to the
scalar radial ODE

    a''(r) + 4 a'(r)/r = 2 S(r).

Multiplying through by r^4 gives (r^4 a')' = 2 r^4 S(r), so

    a'(r) = 2 G4(r) / r^4,   G4(r) = Int_0^r s^4 S(s) ds.

G4 has the elementary closed form

    G4(r) = -1.5 arcsinh(r) + 0.5 r sqrt(1+r^2) + r/sqrt(1+r^2)

(a difference of terms that are each O(r) as r -> 0, so it loses all
significance there -- leg 302's/leg 318's failure mode -- and a Taylor
series is used below r=0.6 instead; both branches are cross-checked in
test_dssp_biot_savart.py). a(r) itself -- previously computed here by
quadrature/table, both of which turned out to be unnecessary -- has a
SECOND elementary closed form, obtained by integrating a'(r) = 2G4(r)/r^4
once more by parts (using G4'(s) = s^4 S(s) and Int s S(s) ds =
-(1+s^2)^{-1/2}):

    a(r) = -2 G4(r)/(3 r^3) - (2/3)/sqrt(1+r^2),

with a(0) = -2/3 and a(r) -> 0 as r -> infinity (the normalisation a(infinity)
= 0, matching decay). No quadrature or interpolation table appears anywhere
in this module: every field, every derivative, is closed-form algebra.

u_B = curl A is then, exactly as in leg 332's own template,

    u_1 = x_1 x_3 a'/r,  u_2 = x_2 x_3 a'/r,  u_3 = -2a - (a'/r)(x_1^2+x_2^2).

Asymptotically (see test_dssp_biot_savart.py for the numeric confirmation)
a(r) ~ -1/r as r -> infinity, so u_B ~ 1/r -- the Type-I envelope this brick's
gate asks about, arrived at by genuinely SOLVING the vector Poisson equation
for an algebraic source, not assumed.

WHAT THIS MODULE DOES NOT CLAIM
------------------------------------------------------------------------------
This is a single closed-form numerical witness and a mapping-bound
measurement on it. It is not a certificate, not a proof, and it says
nothing about existence of a genuine DSS blow-up profile. CEILING: TIER 2.
"""
from __future__ import annotations

import numpy as np


def S(r: np.ndarray) -> np.ndarray:
    """The algebraic radial vorticity profile, S(r) = (1+r^2)^{-3/2}."""
    r = np.asarray(r, dtype=float)
    return (1.0 + r * r) ** -1.5


def Sprime(r: np.ndarray) -> np.ndarray:
    """dS/dr."""
    r = np.asarray(r, dtype=float)
    return -3.0 * r * (1.0 + r * r) ** -2.5


def _G4_big(r: np.ndarray) -> np.ndarray:
    return -1.5 * np.arcsinh(r) + 0.5 * r * np.sqrt(1.0 + r * r) + r / np.sqrt(1.0 + r * r)


def _G4_small(r: np.ndarray) -> np.ndarray:
    """Taylor series of G4 about r=0, Int_0^r s^4(1+s^2)^{-3/2} ds
    = sum_k C(-1.5,k) r^{5+2k}/(5+2k), 18 terms -- matches _G4_big to
    machine precision on the overlap band (see test module)."""
    out = np.zeros_like(r)
    coef = 1.0
    for k in range(0, 18):
        if k:
            coef = coef * (-1.5 - (k - 1)) / k
        p = 5 + 2 * k
        out = out + coef * r ** p / p
    return out


def G4(r: np.ndarray) -> np.ndarray:
    """Int_0^r s^4 S(s) ds, in closed form. Below r=0.6 the direct formula
    loses all significance to cancellation (leg 302's/318's failure mode:
    two O(r) terms differing at O(r^5)), so a Taylor series is used there
    instead; inputs are clamped into each branch BEFORE evaluation so the
    untaken branch never overflows on the other branch's domain (np.where
    always evaluates both arms)."""
    r = np.asarray(r, dtype=float)
    small = _G4_small(np.minimum(r, 0.599))
    big = _G4_big(np.maximum(r, 0.6))
    return np.where(r < 0.6, small, big)


_R_CEIL = 1e100  # far beyond any physically relevant radius; only guards
                  # against float64 overflow (r**3, r**5, ...) for pathological
                  # out-of-domain inputs (e.g. an X=1-exactly compactified
                  # coordinate mapping to r=inf) -- a(r) is already <1e-100
                  # by r~1e100 so clamping here changes no reported digit.


def _safe_r(r: np.ndarray):
    r = np.asarray(r, dtype=float)
    return r, np.clip(r, 1e-300, _R_CEIL)


def a_prime(r: np.ndarray) -> np.ndarray:
    """a'(r) = 2 G4(r)/r^4. a'(0) = 2/5 (from the small-r series, G4(r) ~
    r^5/5, so 2G4(r)/r^4 -> 2r/5 -> 0; the true limit used at r=0 is the
    next-order coefficient, 2/5, consistent with the ODE a''+4a'/r=2S(r)
    at r=0 requiring a'(r) ~ (2/5) r near the origin)."""
    r, rp = _safe_r(r)
    with np.errstate(invalid="ignore", divide="ignore"):
        val = 2.0 * G4(rp) / rp ** 4
    return np.where(r < 1e-8, 2.0 * r / 5.0, val)


def a_second(r: np.ndarray) -> np.ndarray:
    """a''(r) = 2 S(r) - 8 G4(r)/r^5, directly from the ODE a''+4a'/r=2S(r)."""
    r, rp = _safe_r(r)
    with np.errstate(invalid="ignore", divide="ignore"):
        val = 2.0 * S(rp) - 8.0 * G4(rp) / rp ** 5
    return np.where(r < 1e-8, 2.0 / 5.0, val)


def a_of_r(r: np.ndarray) -> np.ndarray:
    """a(r), IN CLOSED FORM -- no quadrature or interpolation anywhere.

    Integrating a'(s) = 2 G4(s)/s^4 by parts (u=G4(s), dv=2s^-4 ds,
    v=-2/(3s^3), du=G4'(s)ds=s^4 S(s) ds, and Int s S(s) ds =
    -(1+s^2)^{-1/2}) gives the antiderivative

        F(s) = -2 G4(s)/(3 s^3) - (2/3)(1+s^2)^{-1/2},

    which -> 0 as s -> infinity (G4(s) ~ s^2/2 for large s, so the first
    term ~ -1/(3s) -> 0, and the second term -> 0 directly), so with the
    decay normalisation a(infinity)=0,

        a(r) = F(r) - F(infinity) = F(r).

    a(0) = -2/3 exactly (G4(r)/r^3 -> 0 as r -> 0)."""
    r, rp = _safe_r(r)
    with np.errstate(invalid="ignore", divide="ignore"):
        val = -2.0 * G4(rp) / (3.0 * rp ** 3) - (2.0 / 3.0) / np.sqrt(1.0 + rp * rp)
    return np.where(r < 1e-8, -2.0 / 3.0, val)


def field_omegaB(x: np.ndarray) -> np.ndarray:
    """Omega_B(x) = 2 S(r) (-x_2, x_1, 0). Exactly divergence-free (it has
    no x_3 component and no dependence on x_3)."""
    r = np.sqrt(np.sum(x * x, axis=-1))
    Sr = S(r)
    x1, x2 = x[..., 0], x[..., 1]
    out = np.zeros_like(x)
    out[..., 0] = -2.0 * Sr * x2
    out[..., 1] = 2.0 * Sr * x1
    return out


def grad_omegaB(x: np.ndarray) -> np.ndarray:
    """d(Omega_B)_i/dx_j, analytic, shape (...,3,3) as [i,j]."""
    r = np.maximum(np.sqrt(np.sum(x * x, axis=-1)), 1e-300)
    Sr = S(r)
    Spr = Sprime(r)
    x1, x2 = x[..., 0], x[..., 1]
    J = np.zeros(x.shape[:-1] + (3, 3))
    for j in range(3):
        xj = x[..., j]
        J[..., 0, j] = -2.0 * (1.0 if j == 1 else 0.0) * Sr - 2.0 * x2 * Spr * xj / r
        J[..., 1, j] = 2.0 * (1.0 if j == 0 else 0.0) * Sr + 2.0 * x1 * Spr * xj / r
    return J


def field_uB(x: np.ndarray) -> np.ndarray:
    """u_B = curl A = Biot-Savart recovery of the velocity from Omega_B,
    A = a(r)(x_2,-x_1,0).

        u_1 = x_1 x_3 a'/r,  u_2 = x_2 x_3 a'/r,
        u_3 = -2a - (a'/r)(x_1^2+x_2^2)."""
    r = np.maximum(np.sqrt(np.sum(x * x, axis=-1)), 1e-300)
    a = a_of_r(r)
    ap = a_prime(r)
    q = ap / r
    x1, x2, x3 = x[..., 0], x[..., 1], x[..., 2]
    out = np.zeros_like(x)
    out[..., 0] = x1 * x3 * q
    out[..., 1] = x2 * x3 * q
    out[..., 2] = -2.0 * a - q * (x1 * x1 + x2 * x2)
    return out


def grad_uB(x: np.ndarray) -> np.ndarray:
    """d(u_B)_i/dx_j, analytic, shape (...,3,3) as [i,j]. Depends only on
    the closed-form a, a', a'' -- never on a quadrature-derived quantity --
    so div u_B and curl u_B - Omega_B can be checked to machine precision
    with no finite-difference step at all (see test module: an earlier
    finite-difference cross-check of this Jacobian against field_uB looked
    like it disagreed at the ~2e-3 level, which turned out to be an
    artifact of subtracting two nearly-equal large quadrature sums in the
    FD estimate itself, not a bug in this formula -- resolved once a(r)
    became closed-form and the analytic div=0/curl=Omega identities were
    checked directly instead of via FD)."""
    r = np.maximum(np.sqrt(np.sum(x * x, axis=-1)), 1e-300)
    a = a_of_r(r)
    ap = a_prime(r)
    app = a_second(r)
    q = ap / r
    qp = app / r - ap / r ** 2
    x1, x2, x3 = x[..., 0], x[..., 1], x[..., 2]
    rho2 = x1 * x1 + x2 * x2
    J = np.zeros(x.shape[:-1] + (3, 3))
    for j in range(3):
        xj = x[..., j]
        J[..., 0, j] = (
            (1.0 if j == 0 else 0.0) * x3 * q
            + (1.0 if j == 2 else 0.0) * x1 * q
            + x1 * x3 * qp * xj / r
        )
        J[..., 1, j] = (
            (1.0 if j == 1 else 0.0) * x3 * q
            + (1.0 if j == 2 else 0.0) * x2 * q
            + x2 * x3 * qp * xj / r
        )
        J[..., 2, j] = (
            -2.0 * ap * xj / r
            - qp * (xj / r) * rho2
            - 2.0 * q * ((1.0 if j == 0 else 0.0) * x1 + (1.0 if j == 1 else 0.0) * x2)
        )
    return J


def vorticity_nonlinearity(u: np.ndarray, w: np.ndarray, Ju: np.ndarray, Jw: np.ndarray) -> np.ndarray:
    """N = (u.grad)w - (w.grad)u, via einsum on the analytic Jacobians.
    u,w shape (...,3); Ju,Jw shape (...,3,3) as [i,j]=d(field_i)/dx_j."""
    Nuw = np.einsum("...j,...ij->...i", u, Jw)
    Nwu = np.einsum("...j,...ij->...i", w, Ju)
    return Nuw - Nwu
