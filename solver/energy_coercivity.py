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


# ===========================================================================
# ROUTE-WES (leg 178) -- THE SECOND, INDEPENDENTLY-CHOSEN CONSTRUCTION.
# Appended beside leg 111's.  NOTHING ABOVE THIS LINE IS EDITED: leg 111's
# banked numbers must reproduce bit-for-bit through the functions above, and
# the driver checks that they do (control C1).
# ===========================================================================
#
# WHY THERE IS A SECOND CONSTRUCTION, AND WHOSE IT IS
# ---------------------------------------------------------------------------
# Leg 111 measured a ZERO-WIDTH window on ONE construction: damping at the
# origin needs `gamma > 3` (`D_phi(0) = (3 - gamma)/2`), while the trial space
# `span{sin k theta}` is in `L^2_phi` only for `gamma < 3`.  It swept `gamma`
# over seven weights and held the TRIAL SPACE fixed.  This block moves the
# thing leg 111 held fixed.
#
# THE CONSTRUCTION IS NOT THIS REPOSITORY'S AND MAY NOT BE CLAIMED.  It is
# Elgindi-Ghoul-Masmoudi, arXiv:1906.05811, Prop. 2.1, whose hypotheses are
# `f` odd, `f'(0) = Hf(0) = 0`, `int |f|^2 phi < infinity` with
# `phi(y) = (1 + y^2)^2 / y^4`, and whose conclusion is
# `int f M_a f phi <= (-1/2 - C|a|) int f^2 phi` -- at `a = 0`, by EGM's own
# sec 1 ("when a = 0 we get CLM model"), on THIS object.  The frame is Xu
# arXiv:2607.19762's realization dichotomy (sec 3.1, Prop. 2), also not ours.
# What is measured here -- a coercivity gap over a CONSTRAINED
# finite-dimensional trial space, with admissibility gated and grid-stability
# reported as a magnitude -- is what leg 178's novelty pass could not locate.
#
# THE TWO CONSTRAINTS, EXACT IN THIS BASIS
# ---------------------------------------------------------------------------
# `(sin k theta)'(0) = k` and, from `H(sin k theta) = -cos k theta + (-1)^k`,
# `H(sin k theta)(0) = -1 + (-1)^k` (`0` for even `k`, `-2` for odd `k`).  So
# for `h = sum c_k sin k theta`:
#
#     h'(0)   = sum_k k c_k                   ("dprime")
#     (Hh)(0) = -2 sum_{k odd} c_k            ("hilbert")
#
# Both are exact integer functionals -- no quadrature enters the constraint,
# which is why the constrained subspace is a QUADRATURE-INDEPENDENT object.
#
# VANISHING ORDER, AND WHY IT IS 3 AND NOT LEG 165's 2
# ---------------------------------------------------------------------------
# `sin k theta = k theta - k^3 theta^3/6 + O(theta^5)`, so an odd trigonometric
# polynomial vanishes to ODD order only: `p in {1, 3, 5, ...}`.  `p = 2` is
# unattainable.  Imposing `sum k c_k = 0` kills the `theta^1` coefficient and
# leaves `-(sum c_k k^3) theta^3 / 6`, i.e. `p = 3` generically.  Membership
# then needs `int theta^{2p} theta^{-gamma} < infinity`, i.e.
# `gamma < 2p + 1 = 7`, against damping's `gamma > 3`: a window of WIDTH 4,
# where leg 111's was width 0.  `wes_vanishing_order` MEASURES this from the
# probe vector rather than asserting it.
#
# THE FALSIFICATION CONTROL IS PART OF THE CONSTRUCTION (lesson 90)
# ---------------------------------------------------------------------------
# `T3_hilbert_only` imposes `(Hh)(0) = 0` alone.  It removes a direction from
# the trial space exactly as `T1`/`T2` do, and it does NOT change the vanishing
# order, so its window stays `(3, 3)` and it must NOT pass.  If it passes, the
# instrument is measuring "I deleted some directions" rather than "the space
# changed", and leg 178's result is withdrawn rather than shipped.
#
# THE WEIGHT, AND AN EXACT FACT ABOUT IT
# ---------------------------------------------------------------------------
# Family `E` is EGM's own `(1 + X^2)^2 / X^4` transported into this module's
# compactification `X = tan(theta/2)` with `dX = ((1 + X^2)/2) dtheta`:
#
#     phi^E(theta) = (1 + X^2)^3 / (2 X^4),      X = tan(theta/2)
#
# written from its own closed form in `X` and NOT from family `B`, so that the
# driver's check that `phi^E / phi^B_4` is CONSTANT is a real measurement and
# not an identity of the code.  Both have `D_phi == -1/2` IDENTICALLY in
# `theta` -- family `B` at `gamma = 4` gives
# `(3 - 2) cos^2(th/2) - 3/2 + sin^2(th/2) = -1/2`, and family `E` gives
# `(3/2) cos th + (X^2 - 2)/(1 + X^2) = -1/2` -- which is the exact sense in
# which the published weight is the one that makes the damping factor
# CONSTANT, and the arithmetic reason EGM's constant is `-1/2`.  Both are
# checked numerically by the driver rather than trusted.
#
# THE SPLIT THAT MAKES THE MECHANISM VISIBLE
# ---------------------------------------------------------------------------
# `wes_form_matrices` returns the form's LOCAL and NONLOCAL halves separately,
#
#     <L h, h>_phi  =  int h^2 D_phi phi  -  int sin th * phi * (H h) * h ,
#
# together with the residual of that integration-by-parts identity as measured
# on the actual quadrature.  The identity has boundary terms that vanish only
# if `h^2 sin th phi -> 0` at both ends; on a singular weight and an
# unconstrained `p = 1` trial space they need not, and the residual is
# therefore a MAGNITUDE this construction owes rather than an assumption it
# makes.  The nonlocal half is the part no weight can touch -- Xu's ceiling
# `KNOWN_ANSWER_CEILING = 0.5` is where it caps the total, and reporting it
# separately is what turns "the gap is 0.5" into a mechanism.
#
# CEILING (unchanged from leg 111, and it binds every number below)
# ---------------------------------------------------------------------------
# Plain float64, nothing interval-enclosed.  The object is the `a = 0` CLM
# linearisation (clause S7): a gap measured here bounds `HL_S2_nonsymmetric`'s
# difficulty FROM BELOW, never above.  A gap on a constrained trial space is
# NOT a certificate -- EGM buy the origin conditions with two free modulation
# parameters -- and no link of the `L1 -> L4` chain can move from anything in
# this block.

# (name, constraints, declared vanishing order, admissible gamma upper bound)
# Declared here before any computation; `wes_vanishing_order` measures it.
WES_CONSTRAINT_CLASSES = (
    ("T0_unconstrained", (), 1, 3.0),           # leg 111's own -- reproduction control
    ("T1_dprime", ("dprime",), 3, 7.0),
    ("T2_egm", ("dprime", "hilbert"), 3, 7.0),
    ("T3_hilbert_only", ("hilbert",), 1, 3.0),  # FALSIFICATION control -- must not pass
)

# Eleven weights.  Family A is leg 111's ladder extended past its gamma = 4 stop
# to the new membership threshold 7 and no further; family B adds the member
# leg 111's enumeration excluded; E is EGM's own, from its own closed form.
WES_WEIGHT_FAMILY = (
    ("A0_flat", "A", 0.0),
    ("A2", "A", 2.0),
    ("A3", "A", 3.0),
    ("A4_chen_hou", "A", 4.0),
    ("A5", "A", 5.0),
    ("A6", "A", 6.0),
    ("A7", "A", 7.0),
    ("B0", "B", 0.0),
    ("B2", "B", 2.0),
    ("B4_egm", "B", 4.0),
    ("E_egm", "E", 4.0),
)

# The membership probe for each class: the SHORTEST integer vector satisfying
# that class's constraints, so the probe is reproducible and quadrature-free.
#   T0: sin th                          (leg 111's own probe, unchanged)
#   T1: 2 sin th - sin 2th              h'(0) = 2 - 2 = 0
#   T2: sin th + sin 2th - sin 3th      h'(0) = 1 + 2 - 3 = 0, (Hh)(0) = -2(1 - 1) = 0
#   T3: sin th - sin 3th                (Hh)(0) = -2(1 - 1) = 0, h'(0) = 1 - 3 = -2 != 0
WES_PROBE_VECTORS = {
    "T0_unconstrained": (1.0,),
    "T1_dprime": (2.0, -1.0),
    "T2_egm": (1.0, 1.0, -1.0),
    "T3_hilbert_only": (1.0, 0.0, -1.0),
}

__all__ = __all__ + [
    "WES_CONSTRAINT_CLASSES",
    "WES_PROBE_VECTORS",
    "WES_WEIGHT_FAMILY",
    "wes_admissibility",
    "wes_coercivity_gap",
    "wes_coercivity_gap_exact",
    "wes_constrained_basis",
    "wes_constraint_rows",
    "wes_damping_factor",
    "wes_form_matrices",
    "wes_form_matrices_constrained",
    "wes_point_mode_intersection",
    "wes_trial_projector",
    "wes_vanishing_order",
    "wes_weight_values",
]


def wes_weight_values(theta, family, gamma):
    """`phi(theta)`, extending `weight_values` with family `E`.

    Families `A` and `B` are DELEGATED to leg 111's `weight_values` unchanged, so
    the two constructions cannot silently drift apart.  Family `E` is EGM's
    `(1 + X^2)^2 / X^4` times the Jacobian `(1 + X^2)/2` of `X = tan(theta/2)`,
    evaluated from that closed form and NOT from family `B` -- the driver's
    constancy check on `phi^E / phi^B_4` is then a measurement.
    """
    theta = np.asarray(theta, dtype=float)
    if family in ("A", "B"):
        return weight_values(theta, family, gamma)
    if family == "E":
        X = np.tan(0.5 * theta)
        return (1.0 + X * X) ** 3 / (2.0 * X ** 4)
    raise ValueError(f"unknown weight family {family!r}")


def wes_damping_factor(theta, family, gamma):
    """`D_phi(theta)`, extending `damping_factor` with family `E`.

    For `E`, `(log phi)'(theta) = 3 X - 2 (1 + X^2)/X` and
    `(1/2) sin theta (log phi)' = (X^2 - 2)/(1 + X^2)`, so
    `D = (3/2) cos theta + (X^2 - 2)/(1 + X^2)`, which is `-1/2` identically.
    It is written in the un-simplified form on purpose: a hard-coded `-0.5`
    could not report the other answer (lesson 90).
    """
    theta = np.asarray(theta, dtype=float)
    if family in ("A", "B"):
        return damping_factor(theta, family, gamma)
    if family == "E":
        X = np.tan(0.5 * theta)
        return 1.5 * np.cos(theta) + (X * X - 2.0) / (1.0 + X * X)
    raise ValueError(f"unknown weight family {family!r}")


def wes_constraint_rows(n, class_name):
    """The class's constraint functionals as EXACT integer rows over `c_1..c_n`.

    `dprime`  : `h'(0)   = sum_k k c_k`.
    `hilbert` : `(Hh)(0) = sum_k (-1 + (-1)^k) c_k` (`-2` on odd `k`, `0` on even).

    No quadrature and no weight enters, so the constrained subspace does not
    move when the mesh does.
    """
    n = int(n)
    names = dict((c[0], c[1]) for c in WES_CONSTRAINT_CLASSES)
    if class_name not in names:
        raise ValueError(f"unknown constraint class {class_name!r}")
    rows = []
    for which in names[class_name]:
        if which == "dprime":
            rows.append(np.array([float(k) for k in range(1, n + 1)]))
        elif which == "hilbert":
            rows.append(np.array([-1.0 + (-1.0) ** k for k in range(1, n + 1)]))
        else:
            raise ValueError(f"unknown constraint {which!r}")
    return np.array(rows) if rows else np.zeros((0, n))


def wes_trial_projector(n, class_name, rcond=1e-12):
    """Orthonormal basis of the constrained trial space, as an `(n, d)` matrix.

    The null space of the exact constraint rows, via their SVD.  `d = n - rank`.
    The coercivity gap is a generalized Rayleigh quotient and is therefore
    invariant under any change of basis of this subspace -- only the SPAN is
    load-bearing, which is why an SVD basis is admissible here even though the
    admissibility probe deliberately uses an explicit integer vector instead.
    """
    n = int(n)
    R = wes_constraint_rows(n, class_name)
    if R.shape[0] == 0:
        return np.eye(n)
    _, sv, Vt = np.linalg.svd(R)
    rank = int(np.sum(sv > rcond * max(float(sv[0]), 1.0)))
    return Vt[rank:].T


def wes_vanishing_order(class_name, thetas=(1e-2, 1e-3, 1e-4)):
    """MEASURE the probe's vanishing order at the origin instead of asserting it.

    Returns the probe's values at the given `theta` and the log-log slopes
    between consecutive ones.  A slope of `1` is `p = 1`, a slope of `3` is
    `p = 3`.  Also returns the exact functional values `h'(0)` and `(Hh)(0)`
    evaluated from the integer rows, so the constraint and its consequence are
    reported side by side.
    """
    c = np.array(WES_PROBE_VECTORS[class_name], dtype=float)
    n = len(c)
    th = np.array(thetas, dtype=float)
    vals = np.array([float(np.sum(c * np.sin(np.arange(1, n + 1) * t))) for t in th])
    slopes = [float(math.log(abs(vals[i + 1]) / abs(vals[i]))
                    / math.log(th[i + 1] / th[i])) for i in range(len(th) - 1)]
    dprime = float(np.sum(c * np.arange(1, n + 1)))
    hzero = float(np.sum(c * np.array([-1.0 + (-1.0) ** k for k in range(1, n + 1)])))
    declared = dict((x[0], x[2]) for x in WES_CONSTRAINT_CLASSES)[class_name]
    return {
        "class": class_name, "probe": [float(x) for x in c],
        "thetas": [float(t) for t in th], "values": [float(v) for v in vals],
        "loglog_slopes": slopes,
        "measured_order": slopes[-1],
        "declared_order": float(declared),
        "h_prime_at_0": dprime, "H_h_at_0": hzero,
    }


def wes_point_mode_intersection(class_name, n=8, rcond=1e-12):
    """Dimension of `span{sin th, sin 2th} INTERSECT` the constrained space.

    Prediction P5 of leg 178's novelty log: for `T2_egm` this is `0`, i.e. the
    two origin constraints already remove BOTH of Xu's published point-spectrum
    modes, so `modulate=True` and `modulate=False` must agree on `T2`.  This is
    leg 178's own arithmetic about two functionals on a two-dimensional space --
    it is NOT attributed to Xu (whose sec 3.2 attributes mode removal to
    centering / the odd restriction) and NOT to EGM.
    """
    n = int(n)
    M = np.zeros((n, 2))
    for j, (_, c) in enumerate(known_modes()):
        M[: len(c), j] = c
    R = wes_constraint_rows(n, class_name)
    if R.shape[0] == 0:
        return {"class": class_name, "intersection_dim": 2, "singular_values": []}
    RM = R @ M
    sv = np.linalg.svd(RM, compute_uv=False)
    top = max(float(sv[0]), 1.0)
    rank = int(np.sum(sv > rcond * top))
    return {"class": class_name, "intersection_dim": int(2 - rank),
            "singular_values": [float(s) for s in sv]}


def wes_form_matrices(n, family, gamma, mu=0.0, n_unif=None, n_grade=24, order=12):
    """`(G, B, B_local, B_nonlocal, byparts_rel_residual)`.

    `G` and `B` are exactly leg 111's `form_matrices` quantities, recomputed here
    only so the local/nonlocal split shares one quadrature with them (the driver
    checks the two agree).  In addition:

        `B_local[j,k]    = int e_j e_k D_phi phi`
        `B_nonlocal[j,k] = -(1/2) int sin th phi ((H e_k) e_j + (H e_j) e_k)`

    and `byparts_rel_residual` is `max|Sym(B) - B_local - B_nonlocal|` divided by
    `max|Sym(B)|`.  That identity holds only if the boundary terms of the
    integration by parts vanish; on a singular weight and a `p = 1` trial space
    they need not, so the residual is MEASURED and reported rather than assumed.
    The split is defined only at `mu = 0` (the `Lambda^1` control is a Fourier
    multiplier, not a local factor), and `B_local`/`B_nonlocal` are `None` when
    `mu != 0`.
    """
    n = int(n)
    if n_unif is None:
        n_unif = max(64, 4 * n)
    th, qw = graded_quadrature(n_unif=n_unif, n_grade=n_grade, order=order)
    phi = wes_weight_values(th, family, gamma)
    ks = np.arange(1, n + 1)
    E = np.stack([np.sin(k * th) for k in ks])
    HE = np.stack([-np.cos(k * th) + (-1.0) ** int(k) for k in ks])
    LE = np.stack([clm_linearization_values(th, int(k)) for k in ks])
    if mu:
        LE = LE - mu * np.stack([k * np.sin(k * th) for k in ks])
    pw = phi * qw
    G = (E * pw) @ E.T
    B = (E * pw) @ LE.T
    if mu:
        return G, B, None, None, None
    D = wes_damping_factor(th, family, gamma)
    B_loc = (E * (pw * D)) @ E.T
    sw = pw * np.sin(th)
    M = (E * sw) @ HE.T                      # M[j,k] = int e_j (H e_k) sin th phi
    B_nl = -0.5 * (M + M.T)
    S = 0.5 * (B + B.T)
    scale = float(np.max(np.abs(S))) if S.size else 1.0
    resid = float(np.max(np.abs(S - B_loc - B_nl))) / (scale if scale > 0 else 1.0)
    return G, B, B_loc, B_nl, resid


def wes_coercivity_gap(n, class_name, family, gamma, mu=0.0, n_unif=None,
                       n_grade=24, order=12, modulate=False, rcond=1e-12,
                       precomputed=None):
    """The coercivity gap over the CONSTRAINED trial space, plus its two halves.

    `precomputed` is an optional `(G, B, B_local, B_nonlocal, residual)` tuple from
    `wes_form_matrices` with the SAME `(n, family, gamma, mu, n_grade, order)`.  The
    form matrices do not depend on the trial class or on `modulate` -- only the
    projector does -- so the driver assembles once per weight and reuses across all
    four constraint classes.  This is a pure caching layer: passing `precomputed`
    cannot change any returned number, and the driver checks one row both ways.

    Same estimator as leg 111's `coercivity_gap` -- `gap = -lambda_max(Sym(B), G)`
    by whitening with `G`'s own eigendecomposition and dropping directions below
    `rcond * lambda_max(G)` -- restricted first to `wes_trial_projector`'s
    subspace.  `class_name = "T0_unconstrained"` with `modulate=True` is exactly
    leg 111's computation and must reproduce its banked numbers (control C1).

    `modulate` defaults to **False** here, because on `T2_egm` the constraints
    already remove both published point modes (`wes_point_mode_intersection`);
    the driver reports both settings so that claim is checked, not assumed.

    `local_gap` and `nonlocal_gap` are the same Rayleigh quotient run on
    `B_local` and `B_nonlocal` alone: the local half is what the weight controls,
    the nonlocal half is what it cannot touch.  Every quantity the measurement
    divides by is returned (lesson 67).
    """
    if precomputed is None:
        G, B, B_loc, B_nl, resid = wes_form_matrices(
            n, family, gamma, mu=mu, n_unif=n_unif, n_grade=n_grade, order=order)
    else:
        G, B, B_loc, B_nl, resid = precomputed
    n = int(n)
    Q = wes_trial_projector(n, class_name, rcond=rcond)
    if modulate:
        modes = np.zeros((n, 2))
        for j, (_, c) in enumerate(known_modes()):
            modes[: len(c), j] = c
        C = modes.T @ G @ Q
        if C.shape[1]:
            _, sv, Vt = np.linalg.svd(C)
            rank = int(np.sum(sv > rcond * max(float(sv[0]), 1.0)))
            Q = Q @ Vt[rank:].T

    Gp = Q.T @ G @ Q
    ev, U = np.linalg.eigh(0.5 * (Gp + Gp.T))
    top = float(ev.max()) if ev.size else 0.0
    keep = ev > rcond * top
    dropped = int(np.sum(~keep))
    if not np.any(keep):
        return {"n": n, "class": class_name, "family": family, "gamma": float(gamma),
                "mu": float(mu), "gap": float("nan"), "dim_trial": int(Q.shape[1]),
                "dim_kept": 0, "dropped": dropped, "cond_G": float("inf"),
                "local_gap": None, "nonlocal_gap": None,
                "byparts_rel_residual": resid, "modulate": bool(modulate)}
    W = U[:, keep] / np.sqrt(ev[keep])

    def rayleigh(Mat):
        if Mat is None:
            return None
        Mp = Q.T @ Mat @ Q
        Mh = W.T @ (0.5 * (Mp + Mp.T)) @ W
        return -float(np.linalg.eigvalsh(0.5 * (Mh + Mh.T)).max())

    gap = rayleigh(0.5 * (B + B.T))
    return {
        "n": n, "class": class_name, "family": family, "gamma": float(gamma),
        "mu": float(mu), "n_grade": int(n_grade), "order": int(order),
        "modulate": bool(modulate),
        "gap": gap,
        "lambda_max": -gap,
        "local_gap": rayleigh(B_loc),
        "nonlocal_gap": rayleigh(B_nl),
        "byparts_rel_residual": resid,
        "dim_trial": int(Q.shape[1]),
        "dim_kept": int(np.sum(keep)),
        "dropped": dropped,
        "cond_G": float(top / float(ev[keep].min())),
    }


def wes_constrained_basis(n, class_name):
    """An EXACTLY-constrained INTEGER basis of the constrained space, `(n, d)`.

    WHY THIS EXISTS, AND IT IS THE CENTRAL INSTRUMENT FINDING OF LEG 178.
    `wes_trial_projector`'s SVD null-space basis satisfies the constraint only to
    machine precision -- its leak along the constraint direction is `~1e-16`.  That
    is harmless when everything in sight is finite.  It is NOT harmless here: at
    `gamma > 3` the UNCONSTRAINED Gram's own entries are DIVERGENT
    (`int sin j th sin k th th^-gamma ~ j k int th^{2-gamma}`), so a `1e-16` leak
    multiplies a quantity that grows by `1.68e+07` per grading refinement.
    Assemble-then-project therefore computes the constrained form as a
    cancellation between divergent numbers, and the answer is dominated by its own
    evaluation error (lesson 86: a bound dominated by its evaluation error is a
    statement about the code).

    The basis below is built from INTEGERS whose constraint residual is EXACTLY
    zero in float64 (all products fit well inside `2^53` for `n <= 256`), and
    `wes_form_matrices_constrained` contracts it against the basis functions
    POINTWISE, before any weight is applied -- so the cancellation happens at each
    `theta` at scale `eps * K * theta`, not at the scale of a divergent integral.

        T0 : the identity -- leg 111's own trial space, unchanged.
        T1 : v_j = (j+1) e_j - j e_{j+1},  j = 1..n-1.
             `sum_k k v_j[k] = j(j+1) - (j+1)j = 0` EXACTLY.
        T3 : all even `e_k`, plus differences of consecutive odd `e_k` --
             `sum_{k odd}` is exactly zero on each.
        T2 : `w_m = u_{m+1} v_m - u_m v_{m+1}`, where `u_m = sum_{k odd} v_m[k]`
             equals `m+1` for odd `m` and `-m` for even `m` (never zero), so the
             `n-2` columns are independent and satisfy BOTH constraints exactly.
    """
    n = int(n)
    if class_name == "T0_unconstrained":
        return np.eye(n)
    if class_name == "T1_dprime":
        V = np.zeros((n, n - 1))
        for j in range(1, n):
            V[j - 1, j - 1] = j + 1
            V[j, j - 1] = -j
        return V
    if class_name == "T3_hilbert_only":
        cols = []
        odds = [k for k in range(1, n + 1) if k % 2 == 1]
        for k in range(2, n + 1, 2):
            c = np.zeros(n)
            c[k - 1] = 1.0
            cols.append(c)
        for i in range(len(odds) - 1):
            c = np.zeros(n)
            c[odds[i] - 1] = 1.0
            c[odds[i + 1] - 1] = -1.0
            cols.append(c)
        return np.stack(cols, axis=1) if cols else np.zeros((n, 0))
    if class_name == "T2_egm":
        V1 = wes_constrained_basis(n, "T1_dprime")            # (n, n-1), exact
        odd_mask = np.array([1.0 if k % 2 == 1 else 0.0 for k in range(1, n + 1)])
        u = odd_mask @ V1                                      # (n-1,), exact integers
        cols = []
        for m in range(V1.shape[1] - 1):
            cols.append(u[m + 1] * V1[:, m] - u[m] * V1[:, m + 1])
        return np.stack(cols, axis=1) if cols else np.zeros((n, 0))
    raise ValueError(f"unknown constraint class {class_name!r}")


def wes_form_matrices_constrained(n, class_name, family, gamma, mu=0.0, n_unif=None,
                                  n_grade=24, order=12):
    """Form matrices assembled DIRECTLY in the exactly-constrained basis.

    Returns `(G, B, B_local, B_nonlocal, byparts_rel_residual, contamination)`.

    The constrained basis functions `F_m = sum_k V[k,m] sin k theta` are formed
    POINTWISE (`F = V.T @ E`) before any weight multiplies them, so the
    order-`theta^{2p+1}` cancellation that makes the constrained space integrable
    happens at each quadrature node at scale `eps * K_m * theta` -- rather than as
    a difference of divergent integrals, which is what assemble-then-project does.

    `contamination` is the MEASURED floor of that roundoff, not an assumption: it
    is `max_m int (eps |V|^T |E|)_m^2 phi / int F_m^2 phi`, i.e. the weighted
    energy of a bound on the pointwise cancellation error, relative to the
    weighted energy of the basis function itself.  A value near `1` means the
    grading depth has been pushed past the point where float64 can represent the
    cancellation, and the number the quadrature prints is a statement about the
    code.
    """
    n = int(n)
    if n_unif is None:
        n_unif = max(64, 4 * n)
    V = wes_constrained_basis(n, class_name)
    th, qw = graded_quadrature(n_unif=n_unif, n_grade=n_grade, order=order)
    phi = wes_weight_values(th, family, gamma)
    ks = np.arange(1, n + 1)
    E = np.stack([np.sin(k * th) for k in ks])
    LE = np.stack([clm_linearization_values(th, int(k)) for k in ks])
    if mu:
        LE = LE - mu * np.stack([k * np.sin(k * th) for k in ks])
    HE = np.stack([-np.cos(k * th) + (-1.0) ** int(k) for k in ks])

    F = V.T @ E                     # (d, nq) -- the cancellation, done pointwise
    LF = V.T @ LE
    HF = V.T @ HE
    pw = phi * qw
    G = (F * pw) @ F.T
    B = (F * pw) @ LF.T

    # measured roundoff floor of the pointwise cancellation
    eps = float(np.finfo(float).eps)
    Fabs = np.abs(V).T @ np.abs(E)
    num = ((eps * Fabs) ** 2 * pw).sum(axis=1)
    den = (F ** 2 * pw).sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        contamination = float(np.nanmax(np.where(den > 0, num / den, 0.0)))

    if mu:
        return G, B, None, None, None, contamination
    D = wes_damping_factor(th, family, gamma)
    B_loc = (F * (pw * D)) @ F.T
    sw = pw * np.sin(th)
    M = (F * sw) @ HF.T
    B_nl = -0.5 * (M + M.T)
    S = 0.5 * (B + B.T)
    scale = float(np.max(np.abs(S))) if S.size else 1.0
    resid = float(np.max(np.abs(S - B_loc - B_nl))) / (scale if scale > 0 else 1.0)
    return G, B, B_loc, B_nl, resid, contamination


def wes_coercivity_gap_exact(n, class_name, family, gamma, mu=0.0, n_unif=None,
                             n_grade=24, order=12, rcond=1e-12, precomputed=None):
    """The coercivity gap on the exactly-constrained basis.  THE MEASUREMENT.

    Identical estimator to leg 111's -- `gap = -lambda_max(Sym(B), G)` by whitening
    with `G`'s own eigendecomposition -- but on form matrices that were never
    assembled in the unconstrained basis, so no divergent quantity is ever formed
    and then cancelled.  There is no `modulate` flag: on `T2_egm` the two origin
    constraints already remove BOTH published point modes
    (`wes_point_mode_intersection` returns dimension 0), which is the whole reason
    the resulting gap is comparable with Xu's MODULATED ceiling of `1/2`.  On
    `T1_dprime` one point-mode direction survives (dimension 1), so its raw gap is
    bounded above by `-1` by the published eigenvalue `1` -- an internal
    consistency check, not a defect.
    """
    if precomputed is None:
        G, B, B_loc, B_nl, resid, contam = wes_form_matrices_constrained(
            n, class_name, family, gamma, mu=mu, n_unif=n_unif, n_grade=n_grade,
            order=order)
    else:
        G, B, B_loc, B_nl, resid, contam = precomputed
    ev, U = np.linalg.eigh(0.5 * (G + G.T))
    top = float(ev.max()) if ev.size else 0.0
    keep = ev > rcond * top
    dropped = int(np.sum(~keep))
    if not np.any(keep):
        return {"n": int(n), "class": class_name, "family": family,
                "gamma": float(gamma), "mu": float(mu), "gap": float("nan"),
                "dim_trial": int(G.shape[0]), "dim_kept": 0, "dropped": dropped,
                "cond_G": float("inf"), "local_gap": None, "nonlocal_gap": None,
                "byparts_rel_residual": resid, "contamination": contam}
    W = U[:, keep] / np.sqrt(ev[keep])

    def rayleigh(Mat):
        if Mat is None:
            return None
        Mh = W.T @ (0.5 * (Mat + Mat.T)) @ W
        return -float(np.linalg.eigvalsh(0.5 * (Mh + Mh.T)).max())

    return {
        "n": int(n), "class": class_name, "family": family, "gamma": float(gamma),
        "mu": float(mu), "n_grade": int(n_grade), "order": int(order),
        "gap": rayleigh(0.5 * (B + B.T)),
        "local_gap": rayleigh(B_loc),
        "nonlocal_gap": rayleigh(B_nl),
        "byparts_rel_residual": resid,
        "contamination": contam,
        "dim_trial": int(G.shape[0]),
        "dim_kept": int(np.sum(keep)),
        "dropped": dropped,
        "cond_G": float(top / float(ev[keep].min())),
    }


def wes_admissibility(class_name, family, gamma, n_grade=24, order=12, n_space=32):
    """Is the CONSTRAINED trial space in `L^2_phi`?  Reported two independent ways.

    (a) leg 111's own instrument, on this class's explicit integer probe vector:
        `||h||^2_phi` at two grading depths (`ratio`), plus the equally-spaced
        ladder whose INCREMENTS separate a log divergence (equal increments)
        from a power divergence (geometrically growing increments).  Using an
        explicit vector rather than an SVD basis keeps this reproducible and
        independent of the projector's internals.
    (b) a whole-space check the probe cannot fake: `lambda_max` of the
        constrained Gram `Q^T G Q` at two grading depths, and its ratio.  If any
        direction of the constrained space leaves the weighted space, this ratio
        runs away even when the probe converges.

    `exponent_margin = 2p + 1 - gamma` uses the class's DECLARED order `p`;
    `wes_vanishing_order` reports the measured one alongside.
    """
    c = np.array(WES_PROBE_VECTORS[class_name], dtype=float)
    ks = np.arange(1, len(c) + 1)

    def probe_norm2(ng):
        th, qw = graded_quadrature(n_grade=ng, order=order)
        h = (c[:, None] * np.sin(ks[:, None] * th[None, :])).sum(axis=0)
        return float(np.sum(h ** 2 * wes_weight_values(th, family, gamma) * qw))

    def gram_top(ng, exact):
        """`exact=True` assembles in the exactly-constrained basis; `exact=False`
        is the assemble-then-project route.  Both are reported, because their
        DISAGREEMENT is leg 178's instrument finding, not a nuisance."""
        if exact:
            G = wes_form_matrices_constrained(n_space, class_name, family, gamma,
                                              n_grade=ng, order=order)[0]
        else:
            Gf, _, _, _, _ = wes_form_matrices(n_space, family, gamma, n_grade=ng,
                                               order=order)
            Q = wes_trial_projector(n_space, class_name)
            G = Q.T @ Gf @ Q
        return float(np.linalg.eigvalsh(0.5 * (G + G.T)).max())

    a, b = probe_norm2(n_grade), probe_norm2(2 * n_grade)
    ladder = [probe_norm2(n_grade + i * n_grade // 2) for i in range(3)]
    inc = [ladder[1] - ladder[0], ladder[2] - ladder[1]]
    ga, gb = gram_top(n_grade, True), gram_top(2 * n_grade, True)
    pa, pb = gram_top(n_grade, False), gram_top(2 * n_grade, False)
    p = dict((x[0], x[2]) for x in WES_CONSTRAINT_CLASSES)[class_name]
    return {
        "class": class_name, "family": family, "gamma": float(gamma),
        "vanishing_order": float(p),
        "exponent_margin": float(2 * p + 1) - float(gamma),
        "probe": [float(x) for x in c],
        "norm2_coarse": a, "norm2_fine": b,
        "ratio": b / a if a > 0 else float("inf"),
        "norm2_ladder": ladder, "increments": inc,
        "increment_ratio": (inc[1] / inc[0]
                            if abs(inc[0]) > 1e-12 * max(abs(ladder[0]), 1.0) else None),
        "gram_top_coarse": ga, "gram_top_fine": gb,
        "gram_top_ratio": gb / ga if ga > 0 else float("inf"),
        "projected_gram_top_coarse": pa, "projected_gram_top_fine": pb,
        "projected_gram_top_ratio": pb / pa if pa > 0 else float("inf"),
    }
