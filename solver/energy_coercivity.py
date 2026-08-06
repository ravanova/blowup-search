"""Route-WE: the WEIGHTED-ENERGY (Chen-Hou-shaped) coercivity form of the `a = 0` CLM
linearisation -- the THIRD realization, measured on the friendliest object in the repository.

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS, AND WHAT IT IS NOT
--------------------------------------------------------------------------
Lesson 87: *a certification method has a SHAPE, and the shape is a property of the
OPERATOR.*  Every `l^1`-Fourier tail estimate assumes the unbounded part of the
linearisation is a diagonal MULTIPLIER; inviscid self-similar transport carries a
SHIFT instead, and `solver/spectral_certificate.py` measured that its diagonal is
EXACTLY zero.  Two realizations of `L1` died on that fact (legs 51-54 coefficient
basis, leg 56 collocation).  The same lesson records what the certified INVISCID
blow-ups in the literature used instead: **weighted energy estimates**
(Chen-Hou-Huang arXiv:1905.06387 for the 1D De Gregorio case, singular weight
`x^{-k}` with `k = 4`; Chen-Hou arXiv:2210.07191 for 2D Boussinesq / 3D Euler).

This module is that third realization, and it computes exactly one kind of number:

    gap(phi, N)  =  - sup { <L h, h>_phi / ||h||^2_phi  :  h in span{sin 1..sin N} }

a **coercivity gap** in a weighted `L^2`.  Positive means the weighted energy is
dissipated; negative means it is not, and the magnitude says by how much.

**IT IS NOT** a radii-polynomial term.  There is no `Y_0`, no `Z_1`, no `Z_2`, no
approximate inverse `A`, no `A_K (+) A_tail` split, no border, and no `l^1_w` norm
anywhere in this file.  The banned repair space of lesson 88 (tuning `s`, the weight
family, the split `K`, or the border direction inside the `Z_1` machinery) shares
**zero quantities** with what is computed here.

--------------------------------------------------------------------------
THE OPERATOR, AND WHY IT IS THE SAME ONE THE OTHER TWO REALIZATIONS DIED ON
--------------------------------------------------------------------------
Compactified variable `X = tan(theta/2)`, odd sine basis, `H(sin k theta) =
-cos k theta + (-1)^k` (this is `solver/rescaled_spectrum.py`'s basis, exact on the
whole line, no domain to truncate).  The `a = 0` CLM anchor is `Omega_0 = -sin theta`,
`c_omega = -1`, `c_l = 1` -- a ONE-MODE exact zero of the rescaled steady residual.
Linearising `R = (c_omega + H Omega) Omega - c_l X Omega_X` at that anchor, and using
`X d/dX = sin theta d/d theta` and `H Omega_0 = cos theta + 1`:

    (L h)(theta)  =  cos theta * h  -  sin theta * (H h)  -  sin theta * h_theta      (*)

`clm_linearization_values` evaluates `(*)` POINTWISE in closed form -- no matrix, no
truncation.  `clm_linearization_matrix` returns the same operator in coefficients, whose
column `k` is

    row k+1 :  1 - k/2         row k-1 :  k/2         row 1 : -(-1)^k

which is character-for-character `solver/spectral_certificate.py`'s
`bordered_linearization` without its gauge row and border column.
`test_energy_coercivity.py` checks the two representations against each other, so the
form below is provably built on the same operator the other two realizations died on and
not on a private re-derivation.

--------------------------------------------------------------------------
THE FORM, DERIVED ONCE SO THE DAMPING FACTOR IS VISIBLE
--------------------------------------------------------------------------
With `<u,v>_phi = int_0^pi u v phi dtheta`, integrating the transport term by parts,

    <L h, h>_phi = int_0^pi h^2 * D_phi(theta) * phi dtheta  -  int_0^pi sin theta * phi * (H h) * h dtheta

    D_phi(theta) = (3/2) cos theta + (1/2) sin theta (log phi)'(theta)                (**)

`D_phi` is the **damping factor**: the entire local part of the form is a MULTIPLIER by
`D_phi`, and choosing `phi` to make it negative is precisely Chen-Hou's move.  The
nonlocal Hilbert term is what the weight cannot touch.  `damping_factor` returns `(**)`
in closed form for the named family, and `damping_factor_at_origin` returns its value at
`theta = 0`, which is the quantity the pre-registered prediction is about.

--------------------------------------------------------------------------
THE WEIGHT FAMILY IS NAMED HERE AND NOWHERE ELSE
--------------------------------------------------------------------------
Fixed in this module before any number was computed, and consumed whole by the driver.
Chen-Hou-Huang's shape is a negative power singular at the ORIGIN; theirs is `k = 4`.

    family A (their shape, ladder around their choice)
        phi^A_gamma(theta) = (2 sin(theta/2))^(-gamma),   gamma = 0,1,2,3,4
        in X: ~ X^(-gamma) as X -> 0,  -> 2^(-gamma) as X -> infinity
        gamma = 0 is the FLAT CONTROL (unweighted L^2(dtheta))

    family B (far-field-weighted variant: the CLM profile decays like 1/X, so a weight
              that grows at infinity is the other thing a person would try)
        phi^B_gamma(theta) = (2 sin(theta/2))^(-gamma) * (2 cos(theta/2))^(-2)
        in X: ~ X^(-gamma) * (1+X^2)/4,   gamma = 0,2

Seven weights.  There is no eighth, and no member of either family is chosen after
seeing a number.

--------------------------------------------------------------------------
ADMISSIBILITY IS MEASURED, NOT ASSERTED
--------------------------------------------------------------------------
`L^2_phi` has to contain the basis at all.  Near `theta = 0`, `sin k theta ~ k theta`, so
the integrand of `||sin theta||^2_phi` is `~ theta^(2-gamma)`: finite iff `gamma < 3`.
`admissibility` reports the exponent margin `3 - gamma` AND the measured ratio of
`||sin theta||^2_phi` between two quadrature resolutions -- a divergent norm shows up as a
ratio far from 1, which is a magnitude, not a boolean.

--------------------------------------------------------------------------
KNOWN-ANSWER WINDOW (lesson 84), EXTERNAL AND PUBLISHED
--------------------------------------------------------------------------
Xu, arXiv:2607.19762, on the odd realisation of exactly this linearisation: the full
point spectrum over C is exactly `{0, 1}` -- the scaling and time-shift symmetry modes,
no embedded eigenvalues -- and the essential spectrum meets `{Re lambda >= -1/2}` in the
single vertical line `{Re lambda = -1/2}`, so removing the two point modes by standard
modulation leaves a spectral gap of `1/2`.  Two consequences used as CONTROLS here:

  (K1) `L sin 2theta = 0` and `L (sin theta + sin 2theta / 2) = sin theta + sin 2theta / 2`
       must hold to machine precision -- checked in the test file.  Both modes live in
       `span{sin theta, sin 2theta}`, so `modulate=True` removes exactly them.
  (K2) The numerical range contains the spectrum, so the MODULATED gap can never exceed
       `1/2` for ANY weight.  A measurement above `1/2` is an instrument bug, not a
       result.  `KNOWN_ANSWER_CEILING` carries the number and the driver checks it.

--------------------------------------------------------------------------
POSITIVE CONTROL THAT CAN REPORT THE OTHER ANSWER (lesson 90)
--------------------------------------------------------------------------
`mu > 0` adds `-mu * Lambda` (`Lambda sin k theta = k sin k theta`, i.e. `Lambda^1`
dissipation -- `solver/fractional_gclm.py`'s dial, and the same control legs 51/53 used).
That turns the unbounded part from a shift into a MULTIPLIER without changing anything
else, and it enters the form through a term that is not proportional to any other, so the
answer genuinely can come out positive.  If this control does not go positive, the
instrument is broken and nothing else in this file means anything.

--------------------------------------------------------------------------
CEILING (pre-committed)
--------------------------------------------------------------------------
Plain float64.  Nothing interval-enclosed.  The object is the `a = 0` CLM linearisation:
one mode, analytic, the friendliest object available.  A wall measured here bounds
`HL_S2_nonsymmetric`'s difficulty FROM BELOW, not above (clause S7).  No link of the
`L1 -> L4` chain can move from anything in this file.
"""

from __future__ import annotations

import math

import numpy as np

__all__ = [
    "KNOWN_ANSWER_CEILING",
    "WEIGHT_FAMILY",
    "admissibility",
    "clm_linearization_matrix",
    "clm_linearization_values",
    "coercivity_gap",
    "damping_factor",
    "damping_factor_at_origin",
    "form_matrices",
    "graded_quadrature",
    "known_modes",
    "weight_values",
]

# Xu arXiv:2607.19762: essential spectrum on {Re lambda = -1/2}, point spectrum exactly
# {0, 1}, modulated spectral gap 1/2.  The numerical range contains the spectrum, so no
# weight can push the modulated coercivity gap above this.
KNOWN_ANSWER_CEILING = 0.5

# The named family.  Fixed before any computation; the driver consumes it whole.
# (name, family, gamma).  gamma = 0 in family A is the flat control.
WEIGHT_FAMILY = (
    ("A0_flat", "A", 0.0),
    ("A1", "A", 1.0),
    ("A2", "A", 2.0),
    ("A3", "A", 3.0),
    ("A4_chen_hou", "A", 4.0),
    ("B0", "B", 0.0),
    ("B2", "B", 2.0),
)


# ---------------------------------------------------------------------------
# the operator
# ---------------------------------------------------------------------------
def clm_linearization_values(theta, k):
    """`(L e_k)(theta)` for `e_k = sin k theta`, in closed form -- eq (*) of the header.

    No truncation and no matrix: this is the operator applied to a basis function and
    evaluated, so a quadrature against it sees the EXACT image including the mode `k+1`
    a finite section would have dropped.
    """
    theta = np.asarray(theta, dtype=float)
    k = int(k)
    s, c = np.sin(theta), np.cos(theta)
    sk, ck = np.sin(k * theta), np.cos(k * theta)
    # cos theta * h            - sin theta * H h                  - sin theta * h'
    return c * sk - s * (-ck + (-1.0) ** k) - k * s * ck


def clm_linearization_matrix(n, mu=0.0):
    """The same operator in coefficients: column `k` has `1 - k/2` on row `k+1`, `k/2` on
    row `k-1`, `-(-1)^k` on row `1`.  Rows/columns `1..n`, so the `k = n` column's
    `k+1` entry falls off the end -- that is the finite SECTION, and it is here only for
    the cross-check against `clm_linearization_values` and against
    `solver/spectral_certificate.py`.  The form matrices below never use it.

    `mu` subtracts the multiplier `mu * k` from the diagonal (`Lambda^1` dissipation).
    """
    n = int(n)
    M = np.zeros((n, n))
    for k in range(1, n + 1):
        if k + 1 <= n:
            M[k, k - 1] += 1.0 - 0.5 * k
        if k - 1 >= 1:
            M[k - 2, k - 1] += 0.5 * k
        M[0, k - 1] -= (-1.0) ** k
        if mu:
            M[k - 1, k - 1] -= mu * k
    return M


def known_modes():
    """The two published point-spectrum modes (Xu arXiv:2607.19762), as coefficient
    vectors over `sin 1 theta, sin 2 theta`, with their eigenvalues.

    Returns `[(lambda, coeffs), ...]`; `coeffs[j]` multiplies `sin (j+1) theta`.
    """
    return [
        (0.0, np.array([0.0, 1.0])),        # scaling mode:    L sin 2theta = 0
        (1.0, np.array([1.0, 0.5])),        # time-shift mode: L (sin th + sin 2th/2) = itself
    ]


# ---------------------------------------------------------------------------
# the weights
# ---------------------------------------------------------------------------
def weight_values(theta, family, gamma):
    """`phi(theta)` for a named family member.  See the header for the definitions."""
    theta = np.asarray(theta, dtype=float)
    half_s = 2.0 * np.sin(0.5 * theta)
    if family == "A":
        return half_s ** (-gamma)
    if family == "B":
        half_c = 2.0 * np.cos(0.5 * theta)
        return half_s ** (-gamma) * half_c ** (-2.0)
    raise ValueError(f"unknown weight family {family!r}")


def damping_factor(theta, family, gamma):
    """`D_phi(theta) = (3/2) cos theta + (1/2) sin theta (log phi)'` -- eq (**), the local
    (multiplier) part of the whole quadratic form, in closed form.

    family A: `(log phi)' = -(gamma/2) cot(theta/2)` so the second term is
              `-(gamma/2) cos^2(theta/2)` and
              `D = (3 - gamma/2) cos^2(theta/2) - 3/2`.
    family B: the extra `(2 cos(theta/2))^(-2)` contributes `+ sin^2(theta/2)`.
    """
    theta = np.asarray(theta, dtype=float)
    cc = np.cos(0.5 * theta) ** 2
    D = (3.0 - 0.5 * gamma) * cc - 1.5
    if family == "B":
        D = D + np.sin(0.5 * theta) ** 2
    elif family != "A":
        raise ValueError(f"unknown weight family {family!r}")
    return D


def damping_factor_at_origin(family, gamma):
    """`D_phi(0)`.  Family A: `(3 - gamma)/2` -- NEGATIVE (i.e. damping at the origin,
    which is where the self-similar profile's singularity sits) iff `gamma > 3`.
    Family B: identical, since `sin^2(0) = 0`."""
    return float(damping_factor(np.array([0.0]), family, gamma)[0])


# ---------------------------------------------------------------------------
# quadrature: graded at BOTH endpoints, because the weights are singular at both
# ---------------------------------------------------------------------------
def graded_quadrature(n_unif=128, n_grade=24, order=12, grade=0.5):
    """Composite Gauss-Legendre on `(0, pi)`: `n_unif` uniform panels, with the first and
    last of them refined geometrically (`n_grade` levels, ratio `grade`) toward the
    endpoints where the weights are singular.

    TWO resolutions, and they answer different questions.  `n_unif` resolves the
    OSCILLATION of `sin k theta` -- a purely geometric mesh fails here, because its coarse
    interior panels are wider than a wavelength and the flat-weight Gram matrix, which is
    exactly `(pi/2) I`, comes back with condition number `1e10`.  `n_grade` resolves the
    SINGULARITY of `phi` at `0` and `pi`; an integral that does not converge under
    `n_grade -> 2 n_grade` is DIVERGENT, and the ratio between the two is the magnitude
    that says so.  Nothing here silently regularises a singularity.
    """
    gl_x, gl_w = np.polynomial.legendre.leggauss(int(order))
    n_unif, n_grade = int(n_unif), int(n_grade)
    h = math.pi / n_unif
    edges = [i * h for i in range(n_unif + 1)]
    inner = edges[1:-1]                       # the uniform panels that are NOT at an end
    panels = [(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]
    for a, b, toward_left in ((0.0, h, True), (math.pi - h, math.pi, False)):
        # geometric refinement of one end panel toward its singular endpoint
        cuts, w = [], b - a
        for _ in range(n_grade):
            w *= grade
            cuts.append(a + w if toward_left else b - w)
        pts = sorted({a, b, *cuts})
        panels += [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    nodes, wts = [], []
    for lo, hi in panels:
        c0, c1 = 0.5 * (hi - lo), 0.5 * (hi + lo)
        nodes.append(c1 + c0 * gl_x)
        wts.append(c0 * gl_w)
    return np.concatenate(nodes), np.concatenate(wts)


# ---------------------------------------------------------------------------
# the form
# ---------------------------------------------------------------------------
def form_matrices(n, family, gamma, mu=0.0, n_unif=None, n_grade=24, order=12):
    """`(G, B)` where `G_jk = <e_j, e_k>_phi` and `B_jk = <L e_k, e_j>_phi`.

    `B` is built from `clm_linearization_values`, i.e. from the operator applied
    POINTWISE, so no mode of `L e_k` is dropped -- the only truncation in the whole
    computation is the trial space `span{e_1..e_n}`, which makes `gap(n)` a Rayleigh
    quotient over a NESTED family of subspaces and therefore monotone in `n`.
    """
    n = int(n)
    if n_unif is None:
        n_unif = max(64, 4 * n)      # >= 2 panels per wavelength of sin(n theta)
    th, qw = graded_quadrature(n_unif=n_unif, n_grade=n_grade, order=order)
    phi = weight_values(th, family, gamma)
    E = np.stack([np.sin(k * th) for k in range(1, n + 1)])          # (n, nq)
    LE = np.stack([clm_linearization_values(th, k) for k in range(1, n + 1)])
    if mu:
        LE = LE - mu * np.stack([k * np.sin(k * th) for k in range(1, n + 1)])
    pw = phi * qw
    G = (E * pw) @ E.T
    B = (E * pw) @ LE.T          # B[j, k] = <e_j, L e_k>_phi
    return G, B


def coercivity_gap(n, family, gamma, mu=0.0, n_unif=None, n_grade=24, order=12,
                   modulate=True, rcond=1e-12):
    """The measured coercivity gap, plus every quantity it was divided by.

    `gap = -lambda_max( Sym(B), G )` over the trial space, where `Sym(B) = (B + B^T)/2`.
    With `modulate=True` the trial space is first restricted to the `G`-orthogonal
    complement of the two PUBLISHED point-spectrum modes (`known_modes`) -- which is the
    modulation Xu's `1/2` refers to and the analogue of Chen-Hou's normalisation
    conditions.  With `modulate=False` nothing is removed, and the gap is then bounded
    above by `-1` for any weight in which the time-shift mode has finite norm.

    Returned dict carries `cond_G` and `dropped` (lesson 67: gate the quantity the
    measurement divides by).  The generalized problem is solved by whitening with `G`'s
    own symmetric eigendecomposition, dropping directions below `rcond * lambda_max(G)`
    rather than pretending an ill-conditioned Gram matrix is invertible.
    """
    G, B = form_matrices(n, family, gamma, mu=mu, n_unif=n_unif, n_grade=n_grade,
                         order=order)
    S = 0.5 * (B + B.T)

    P = np.eye(int(n))
    if modulate:
        modes = np.zeros((int(n), 2))
        for j, (_, c) in enumerate(known_modes()):
            modes[: len(c), j] = c
        # G-orthogonal complement of span(modes): null space of modes^T G
        C = modes.T @ G                                   # (2, n)
        _, sv, Vt = np.linalg.svd(C)
        rank = int(np.sum(sv > rcond * max(sv[0], 1.0)))
        P = Vt[rank:].T                                   # (n, n - rank)

    Gp, Sp = P.T @ G @ P, P.T @ S @ P
    ev, Q = np.linalg.eigh(0.5 * (Gp + Gp.T))
    top = ev.max() if ev.size else 0.0
    keep = ev > rcond * top
    dropped = int(np.sum(~keep))
    W = Q[:, keep] / np.sqrt(ev[keep])
    Shat = W.T @ (0.5 * (Sp + Sp.T)) @ W
    lam = np.linalg.eigvalsh(0.5 * (Shat + Shat.T))
    lam_max = float(lam.max())
    return {
        "n": int(n), "family": family, "gamma": float(gamma), "mu": float(mu),
        "n_grade": int(n_grade), "order": int(order), "modulate": bool(modulate),
        "gap": -lam_max,
        "lambda_max": lam_max,
        "dim_trial": int(P.shape[1]),
        "dim_kept": int(np.sum(keep)),
        "dropped": dropped,
        "cond_G": float(top / ev[keep].min()) if np.any(keep) else float("inf"),
    }


def admissibility(family, gamma, n_grade=24, order=12):
    """Is the basis even IN `L^2_phi`?  Reported as a margin and as a measured ratio.

    `exponent_margin = 3 - gamma`: the integrand of `||sin theta||^2_phi` near the origin
    is `~ theta^(2-gamma)`, finite iff `gamma < 3`.  `ratio` is
    `||sin theta||^2_phi` at `2 * n_grade` over the value at `n_grade`: `~1` means the
    integral converged, a large number means it is divergent and the finite value the
    quadrature printed is a statement about the quadrature (lesson 86).
    """
    def norm2(ng):
        th, qw = graded_quadrature(n_grade=ng, order=order)
        return float(np.sum(np.sin(th) ** 2 * weight_values(th, family, gamma) * qw))

    a, b = norm2(n_grade), norm2(2 * n_grade)
    # EQUALLY SPACED grading depths, which is what separates the two kinds of divergence.
    # Each extra level of grading multiplies the innermost panel by `grade`, so a
    # LOG divergence adds a CONSTANT per level (equal increments) while a POWER divergence
    # multiplies by a constant per level (increments growing geometrically).  The ratio of
    # the two increments is therefore the shape of the divergence, and it does not depend
    # on where the mesh happens to start -- unlike `ratio`, which does.
    ladder = [norm2(n_grade + i * n_grade // 2) for i in range(3)]
    inc = [ladder[1] - ladder[0], ladder[2] - ladder[1]]
    return {
        "family": family, "gamma": float(gamma),
        "exponent_margin": 3.0 - float(gamma),
        "norm2_coarse": a, "norm2_fine": b,
        "ratio": b / a if a > 0 else float("inf"),
        "norm2_ladder": ladder,
        "increments": inc,
        # `None` when the integral has CONVERGED (both increments are zero to rounding),
        # which is the honest report: a divergence shape has no referent there (lesson 73).
        # Kept JSON-valid on purpose -- `float("inf")` does not round-trip.
        "increment_ratio": (inc[1] / inc[0]
                            if abs(inc[0]) > 1e-12 * max(abs(ladder[0]), 1.0) else None),
    }
