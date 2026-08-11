"""Enriched compactified basis for the DSSP boundary block. Route-DSSP brick B2.

WHAT THIS MODULE IS FOR
------------------------------------------------------------------------------
Leg 313 (branch leg/313-sdss-v1, read-only here) measured that the log-periodic
far-field block of the DSS search, transposed under the compactification
X = |y|/(1+|y|) into the physical-to-X map, sits at X = 1 as

    (1-X)^{1-i*kappa}

and that a PLAIN Chebyshev basis on X in [0,1] needs O(10^3-10^4) modes per
unit of kappa to resolve it to 1e-6 relative truncation (823 at kappa=1,
14149 at kappa=20; n(kappa) ~ 791*kappa^0.954; smooth-control separation
82.3x at the cheapest kappa != 0 row) -- because a fractional/branch-type
singularity at a Chebyshev endpoint only ever decays ALGEBRAICALLY, no matter
how large N gets. This is brick B2's whole subject: build a basis in which
that same singularity is not a boundary defect at all, measure its cost on
the identical instrument (same target function, same 1e-6 relative-tail
truncation criterion), and report the factor.

THE CONSTRUCTION
------------------------------------------------------------------------------
The map u = -log(1-X) sends X in [0,1) to u in [0, infinity) and carries the
boundary block to

    (1-X)^{1-i*kappa} = exp(-(1-i*kappa) u)  ,

an ENTIRE function of u -- exponential decay times pure oscillation, no
branch point anywhere finite. u is then itself compactified by the standard
Boyd algebraic map v = u/(u+L), u = L*v/(1-v), L > 0 a single fixed length
scale, so v ranges over [0,1) and Chebyshev-in-v is again a basis on a finite
interval. The composite map X -> v is

    v = u/(u+L),  u = -log(1-X)   <=>   X = 1 - exp(-L*v/(1-v))  .

This is a GENERIC construction (it does not depend on kappa beyond the target
function itself) built for one purpose: turn an algebraic/branch boundary
singularity into a function that is smooth (in fact entire) in the interior
of the mapped variable and merely exponentially-flat -- not branched -- at
its new endpoint v=1. It is not a per-kappa fit: L is fixed once (below,
L = 16.0, chosen by the resolution sweep in
experiments/p2_route_dsspb2_v1.py and reused unchanged for every kappa row
so the comparison in the gate is on ONE instrument, not five tuned ones).

WHAT THIS MODULE DOES NOT CLAIM
------------------------------------------------------------------------------
This is a basis-construction and mode-count measurement. It is not a
certificate, not a proof, and it says nothing about existence of a DSS
candidate. CEILING: TIER 2, per the plan's own B2 gate text.
"""
from __future__ import annotations

import numpy as np

# Fixed map scale, shared by every kappa row -- see the module docstring.
DEFAULT_L = 16.0


def cheb_lobatto_nodes(N: int) -> np.ndarray:
    """N+1 Chebyshev-Lobatto nodes on [0,1] (endpoints included, x=1 at k=0)."""
    k = np.arange(N + 1)
    t = np.cos(np.pi * k / N)
    return 0.5 * (t + 1.0)


def cheb_coeffs(fn, N: int) -> np.ndarray:
    """|Chebyshev coefficients| of a (possibly complex) fn on [0,1], via DCT-I/FFT.

    Same instrument as leg 313's own S3 measurement (independently re-derived
    here, not imported, because this is a new solver/ module): N+1
    Chebyshev-Lobatto nodes, coefficients read off a mirrored-sequence FFT.
    """
    nodes = cheb_lobatto_nodes(N)
    val = np.asarray(fn(nodes), dtype=complex)
    ext = np.concatenate([val, val[-2:0:-1]])
    c = np.fft.fft(ext)
    c = c[: N + 1] / N
    c[0] /= 2.0
    c[N] /= 2.0
    return np.abs(c)


def tail_truncation_error(absc: np.ndarray) -> np.ndarray:
    """sum_{n>=m} |a_n| for every m -- the same rigorous-in-form tail bound leg
    313's S3 used, so the truncation criterion below is not a different
    instrument in disguise."""
    return np.cumsum(absc[::-1])[::-1]


def modes_for_rel_tol(fn, N: int, tol: float) -> int:
    """Number of Chebyshev modes needed so the RELATIVE tail sum falls below
    tol. Returns -1 if the tolerance is never reached within N modes (an
    under-resolution signal, never silently returned as a number)."""
    a = cheb_coeffs(fn, N)
    tail = tail_truncation_error(a)
    scale = float(tail[0]) if tail[0] > 0 else 1.0
    rel = tail / scale
    idx = int(np.argmax(rel < tol))
    return idx if rel[idx] < tol else -1


def boundary_block(X: np.ndarray, kappa: float) -> np.ndarray:
    """The DSSP far-field block itself, (1-X)^{1-i*kappa}, on the PLAIN X
    variable -- this is leg 313's target function, reproduced verbatim so the
    baseline measurement below is provably the same object."""
    one_minus_X = np.maximum(1.0 - np.asarray(X, dtype=float), 1e-300)
    return np.exp((1.0 - 1j * kappa) * np.log(one_minus_X))


def v_of_X(X: np.ndarray, L: float = DEFAULT_L) -> np.ndarray:
    """The forward composite map X -> v (diagnostic / inverse-consistency use
    only; the solve itself works in v, calling boundary_block_v)."""
    X = np.asarray(X, dtype=float)
    u = -np.log(np.maximum(1.0 - X, 1e-300))
    return u / (u + L)


def X_of_v(v: np.ndarray, L: float = DEFAULT_L) -> np.ndarray:
    """The inverse composite map v -> X."""
    v = np.asarray(v, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        u = L * v / (1.0 - v)
        X = 1.0 - np.exp(-u)
    return np.where(np.isfinite(X), X, 1.0)


def boundary_block_v(v: np.ndarray, kappa: float, L: float = DEFAULT_L) -> np.ndarray:
    """The SAME target function (1-X)^{1-i*kappa}, expressed directly in the
    enriched variable v so the essential singularity at v=1 never needs to be
    evaluated through a 0/0 in X: (1-X)^{1-i*kappa} = exp(-(1-i*kappa) u),
    u = L*v/(1-v)."""
    v = np.asarray(v, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        u = L * v / (1.0 - v)
        out = np.exp(-(1.0 - 1j * kappa) * u)
    return np.where(np.isfinite(out), out, 0.0)


def smooth_control_v(v: np.ndarray, L: float = DEFAULT_L) -> np.ndarray:
    """leg 313's own asymmetric-entire positive control (exp(2.3X)sin(3X+0.7)),
    carried through the SAME v-map. Used as a falsification control on the
    enrichment itself: a function with no boundary singularity has nothing
    for the map to buy, and a correct instrument must be able to show that
    (see MF-style control in the B2 experiment runner: this function's cost
    goes UP under the v-map, not down)."""
    X = X_of_v(v, L)
    return np.exp(2.3 * X) * np.sin(3.0 * X + 0.7) + 0j


def smooth_control_X(X: np.ndarray) -> np.ndarray:
    """leg 313's own positive control, on the plain X variable."""
    X = np.asarray(X, dtype=float)
    return np.exp(2.3 * X) * np.sin(3.0 * X + 0.7) + 0j
