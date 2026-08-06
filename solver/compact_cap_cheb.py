"""ROUTE-CAPG v1 (leg 162): the COMPACT-SUPPORT / GLOBAL-CHEBYSHEV certificate corner,
built explicitly and measured in leg 54's `Z_1` convention.

--------------------------------------------------------------------------
WHY THIS MODULE EXISTS, AND WHAT THE NOVELTY PASS ALREADY CORRECTED
--------------------------------------------------------------------------
`DIRECTION.md` §162's thesis is that every certificate corner this repository has killed
(legs 49, 52, 53, 54, 56, 58, 59, 111, and leg 126's completeness audit over all of them)
worked in a compactified **WHOLE-LINE** representation with algebraic weights, and that
the compact-support / global-Chebyshev corner was never tried here.

**The first half is true; the second half is false, and this module does not pretend
otherwise** (`writeup/novelty/leg_162.md` §0).  `solver/first_integral.py` already reduces
the gCLM profile to its own support in an even-Chebyshev series with the FINITE Hilbert
transform, and `solver/reduced_certificate.py` already assembles `Y_0`, `Z_0`, `Z_2`
there.  What has never been computed -- in this repository, in any basis on a finite
support interval -- is the one number the gate asks for, and
`reduced_certificate.py`'s own item (4) says so verbatim:

    (4) Z_1 IS NOT COMPUTED.  It is the infinite-dimensional tail ... and it is the
        whole content of a real computer-assisted proof.

So this module claims exactly one thing: **a measured `Z_1` for this operator in this
basis, in leg 54's convention, plus its classification against leg 126's enumeration.**

--------------------------------------------------------------------------
THE OBJECT
--------------------------------------------------------------------------
`solver/first_integral.py`'s reduced system (RS), on the profile's OWN support, `v = X/X_c`
in `[-1, 1]`, `c` fixed to 1 by the dilation gauge:

    c e'(v) + a X_c Hpv[ e^{1/a} ](v) = 0 ,   e(0) = 1 ,  e(1) = 0 ,

    Hpv[w](v) = (1/pi) p.v. int_{-1}^{1} w(u) / (v - u) du      <-- (v - u), this repo's sign

linearised in `e` at the profile:

    L h  =  c h'  +  X_c Hpv[ p h ] ,     p(v) = e(v)^{1/a - 1} .            (L)

`c d/dv` is the UNBOUNDED part; `Hpv[p .]` is the bounded part.  The first integral is
what makes the leading coefficient CONSTANT -- on the whole line the same operator's
unbounded part is the degenerate transport `(c_l X + a U) d/dX`, and that degeneracy is
exactly why `solver/finite_support.py`'s direct build never converged.

**HTW's compact-support hypothesis, at the exponent this repository read.**  Leg 112 read
arXiv:2603.25104v2 at full text: Theorem 7.10(3) (p. 45) gives compact support **exactly on
`0 < a < 1`**; `a = 1` is the boundary case where the support edge degenerates to a corner.
`DIRECTION.md` §162's "`a = 1` (De Gregorio)" is therefore the one exponent the theorem
excludes, and every construction here is parameterized on `0 < a < 1`.

--------------------------------------------------------------------------
THE TWO REALIZATIONS -- AND THIS IS THE FINDING, SO READ IT BEFORE THE NUMBERS
--------------------------------------------------------------------------
"Global Chebyshev basis on the support interval" is not one object.  `L` is one operator,
but `Z_1 = ||I - A L||` is a norm on a CHOSEN pair of coordinates, and the compact-support
problem admits two natural pairings that both close under `L` exactly.  This module builds
both, because they classify OPPOSITELY under `solver/certificate_shapes.py`'s vocabulary
and reporting only one of them would be a choice disguised as a measurement (lesson 70:
NAME THE REALIZATION).

  **Realization A -- "repo ansatz"** (`solver/first_integral.py`'s own): domain
  `phi_n = (1 - v^2) T_n(v)`, codomain `T_m(v)`.  The support edge is exact by
  construction.  Both blocks are exact and bidiagonal:

      d/dv[(1-v^2) T_n]  =  ((n-2)/2) T_{n-1}  -  ((n+2)/2) T_{n+1}
      Hpv[(1-v^2) T_n]   =  (T_{n+1} - T_{n-1}) / 2

  The unbounded part is a **SHIFT with EXACTLY ZERO DIAGONAL and off-diagonal ~ n/2** --
  numerically the same shape, and the same `n/2`, as the compactified whole-line tail block
  `solver/spectral_certificate.py::tail_block` (entries `1 - k/2` and `k/2`).

  **Realization B -- "Olver-Townsend"** ([arXiv:1507.00596](https://arxiv.org/abs/1507.00596),
  the well-conditioned pairing for singular integral equations): domain
  `phi_n = sqrt(1-v^2) U_{n-1}(v)`, codomain `psi_m = T_m(v) / sqrt(1-v^2)`.  Here

      d/dv[ sqrt(1-v^2) U_{n-1} ]  =  -n T_n / sqrt(1-v^2)  =  -n psi_n
      Hpv[ sqrt(1-v^2) U_{n-1} ]   =  T_n  =  sqrt(1-v^2) psi_n

  so the unbounded part is an **EXACT MULTIPLIER, diag(-c n)** -- the `MULTIPLIER` row of
  `SHAPE_LEDGER`, the shape in which the standard radii-polynomial tail estimate closes --
  and the bounded part costs one multiplication by `sqrt(1-v^2)`, whose Chebyshev
  coefficients are `O(m^-2)` and whose `l^1` norm is finite (measured below, `4/pi`).

**Why that matters, and it is the whole leg.**  Leg 58's Proposition NG (`Z_1 >= 1` for
every bounded `A` with `A21 = 0`) has THREE hypotheses, and
`spectral_certificate.nogo_hypotheses` names them.  (H2) is *"the tail block has a kernel
in `l^1_w`"*, and the proof puts `x = (0; h)` with `T h = 0`.  In realization A the tail is
a zero-diagonal shift and (H2) holds.  In realization B the tail is `diag(-c n)`, which has
**no kernel at any `n >= 1`** -- (H2) fails outright, exactly the way it fails for `mu > 0`
in leg 58's own dissipative control.  So the theorem does not reach realization B, and
whether `Z_1 < 1` there is a MEASUREMENT, not a corollary.  This module makes it.

--------------------------------------------------------------------------
THE CONTROL THAT CAN COME OUT DIFFERENTLY (lesson 90)
--------------------------------------------------------------------------
`shape_control_wholeline` runs the SAME classifier used on the two Chebyshev tails against
`spectral_certificate.tail_block`, the banked compactified whole-line operator.  It must
report `SHIFT` / zero diagonal.  If the classifier reported `MULTIPLIER` there too, the
Chebyshev result would be a tautology of this file rather than a property of the operator.
Three operators, one code path, and they are required to disagree.

--------------------------------------------------------------------------
WHAT THIS IS NOT
--------------------------------------------------------------------------
* **Not rigorous.**  Float64, no interval arithmetic.  Every number is a measurement of a
  finite matrix, at a stated truncation, with a stated ladder in that truncation.
* **Not a claim about `HL_S2_nonsymmetric` or about any link of the L1->L4 chain.**  The
  object is the gCLM profile on `0 < a < 1`.  `support_transfer_audit` measures, rather
  than assumes, that leg 126's own object (the `a = 0` CLM linearisation) has no support
  interval to put this basis on at all.
* **Not a `Y_0`, `Z_0` or `Z_2`.**  `Z_2` is already measured infinite in the sup setting by
  `solver/reduced_certificate.py` (3a), and this module does not reopen it.  A `Z_1 < 1`
  here is NOT a certificate; it is one of four constants.
* **No GA compute, under any outcome.**  Free parameters move on the pre-named deterministic
  grids `GRID_A` and `GRID_S` (leg 46/59 precedent).
"""

import json
import os

import numpy as np

# read-only imports: this module never edits either file
from solver.spectral_certificate import tail_block as _wholeline_tail_block

# --------------------------------------------------------------------------
# vocabulary, imported by VALUE from solver/certificate_shapes.py so that a
# rename there shows up here as a failure rather than as a silent disagreement
# --------------------------------------------------------------------------
from solver.certificate_shapes import (  # noqa: E402
    MULTIPLIER,
    SHIFT,
    TRIDIAGONAL_DOMINANT,
)

#: the pre-named deterministic grids.  NEVER an evolutionary search (leg 49 ban).
GRID_A = (0.2, 0.3, 0.4, 0.5, 0.6, 0.8)          # HTW compact support holds on 0 < a < 1
GRID_S = (0.0, 0.3, 0.7, 1.0, 1.5)               # leg 126's own `s` axis, verbatim

REAL_A = "cheb_compact_support_repo_ansatz"      # (1-v^2)T_n  ->  T_m
REAL_B = "cheb_compact_support_olver_townsend"   # sqrt(1-v^2)U_{n-1}  ->  T_m/sqrt(1-v^2)


# ==========================================================================
# 1.  exact Chebyshev blocks -- every identity is CHECKED numerically by
#     `verify_identities()`, never trusted from the docstring
# ==========================================================================
def deriv_block(N, realization=REAL_A):
    """The unbounded part of `(L)`: `c d/dv`, `c = 1`, as an `N x N` matrix.

    Rows and columns are indexed `n = 1..N` in both realizations (index 0 carries no
    derivative and is dropped from both bases so the two are comparable index-for-index).
    """
    N = int(N)
    D = np.zeros((N, N))
    if realization == REAL_A:
        # d/dv[(1-v^2) T_n] = ((n-2)/2) T_{n-1} - ((n+2)/2) T_{n+1}
        for n in range(1, N + 1):
            j = n - 1
            if n - 1 >= 1:
                D[n - 2, j] += (n - 2.0) / 2.0
            if n + 1 <= N:
                D[n, j] += -(n + 2.0) / 2.0
        return D
    if realization == REAL_B:
        # d/dv[sqrt(1-v^2) U_{n-1}] = -n T_n / sqrt(1-v^2) = -n psi_n
        return np.diag(-np.arange(1, N + 1, dtype=float))
    raise ValueError(realization)


def sqrt_weight_coeffs(m_max):
    """Chebyshev-`T` coefficients of `sqrt(1-v^2)`, exactly.

        sqrt(1-v^2) = 2/pi - (4/pi) sum_{k>=1} T_{2k}(v) / (4k^2 - 1)

    Returned as `g[0..m_max]` in the plain (non-halved) convention `f = sum_m g_m T_m`.
    The `O(m^-2)` decay is why realization B's bounded block has finite `l^1` norm.
    """
    m_max = int(m_max)
    g = np.zeros(m_max + 1)
    g[0] = 2.0 / np.pi
    for k in range(1, m_max // 2 + 1):
        g[2 * k] = -4.0 / (np.pi * (4.0 * k * k - 1.0))
    return g


def cheb_mult_matrix(g, N):
    """Multiplication by `f = sum_m g_m T_m` in the `T` basis, `T_j T_n = (T_{j+n}+T_{|j-n|})/2`.

    Returned on indices `1..N` (row `m` = coefficient of `T_m`), truncated -- the
    truncation is the honest one: coefficients above `N` are DROPPED, not folded back.
    """
    N = int(N)
    g = np.asarray(g, dtype=float)
    M = np.zeros((N, N))
    for n in range(1, N + 1):
        for j, gj in enumerate(g):
            if gj == 0.0:
                continue
            for m in (j + n, abs(j - n)):
                if 1 <= m <= N:
                    M[m - 1, n - 1] += 0.5 * gj
    return M


def cheb_mult_matrix_U(g, N):
    """Multiplication by `f = sum_j g_j T_j` in the **U** basis, on indices `n = 1..N`.

        T_j U_{k}  =  (U_{k+j} + U_{k-j}) / 2 ,   U_{-1} = 0 ,  U_{-m} = -U_{m-2}

    Realization B's domain is `sqrt(1-v^2) U_{n-1}`, so multiplying the PERTURBATION by the
    profile factor `p` is a `U`-basis product, not a `T`-basis one.  This module's first
    draft used the `T`-basis matrix here; the two differ, and the difference is a wrong
    operator rather than a small error.
    """
    N = int(N)
    g = np.asarray(g, dtype=float)
    M = np.zeros((N, N))
    for n in range(1, N + 1):
        k = n - 1                                   # U index
        for j, gj in enumerate(g):
            if gj == 0.0:
                continue
            for kk, sgn in ((k + j, 1.0), (k - j, 1.0)):
                if kk >= 0:
                    m = kk + 1
                    if 1 <= m <= N:
                        M[m - 1, n - 1] += 0.5 * gj * sgn
                elif kk == -1:
                    continue                        # U_{-1} = 0
                else:
                    m = (-kk - 2) + 1               # U_{-m} = -U_{m-2}
                    if 1 <= m <= N:
                        M[m - 1, n - 1] += -0.5 * gj
    return M


def hilb_projector(basis, N, n_nodes=None, nq=1200):
    """`Hpv` of a whole basis family, projected back onto `T_1..T_N`.  Numerical.

    `basis(u)` returns an `(len(u), N)` array of the `N` domain functions.  The principal
    value is taken by singularity subtraction (see `_hilb_pv`), vectorized across the family,
    and the result is projected by a discrete Chebyshev transform on Chebyshev-Gauss nodes.
    """
    N = int(N)
    n_nodes = int(n_nodes) if n_nodes else max(2 * N, 32)
    xq, wq = _leggauss_cached(int(nq))
    Fq = basis(xq)                                     # (nq, N)
    j = np.arange(n_nodes)
    vs = np.cos((j + 0.5) * np.pi / n_nodes)
    Fv = basis(vs)                                     # (n_nodes, N)
    vals = np.empty((n_nodes, N))
    for i, vi in enumerate(vs):
        d = vi - xq
        safe = np.abs(d) > 1e-14
        num = Fq - Fv[i][None, :]
        g = np.where(safe[:, None], num / np.where(safe, d, 1.0)[:, None], 0.0)
        vals[i] = wq @ g + Fv[i] * np.log(abs((vi + 1.0) / (vi - 1.0)))
    vals /= np.pi
    k = np.arange(N + 1)
    Tk = np.cos(np.outer((j + 0.5) * np.pi / n_nodes, k))     # (n_nodes, N+1)
    coeff = (2.0 / n_nodes) * (Tk.T @ vals)                   # (N+1, N)
    return coeff[1:, :]                                       # drop T_0: index 1..N


def _basis_A(u, N):
    """`phi_n = (1 - u^2) T_n(u)`, `n = 1..N` -- `solver/first_integral.py`'s ansatz."""
    u = np.asarray(u, dtype=float)
    th = np.arccos(np.clip(u, -1.0, 1.0))
    n = np.arange(1, int(N) + 1)
    return (1.0 - u ** 2)[:, None] * np.cos(np.outer(th, n))


def hilb_block(N, realization=REAL_A, sqrt_modes=None, nq=1200, n_nodes=None):
    """The bounded part of `(L)`: the FINITE Hilbert transform, at `p = 1` (the
    shape-carrying caricature).  The profile-dependent `p` enters via `profile_mult_matrix`.

    **Realization B is EXACT and realization A is NOT, and that asymmetry is a finding, not
    an implementation detail.**  The Tricomi pair

        Hpv[ sqrt(1-u^2) U_{n-1} ](v) = T_n(v)          (this repo's `(v-u)` sign)
        Hpv[ T_n / sqrt(1-u^2) ](v)   = -U_{n-1}(v)

    closes on the **airfoil class** `sqrt(1-v^2) x polynomial`.  This repository's own
    compact-support ansatz `(1-v^2) T_n` (`solver/first_integral.py`) is NOT in that class:
    `(1-u^2)T_n = sqrt(1-u^2) [sqrt(1-u^2) T_n]` and the bracket is not a polynomial, so no
    finite closed form exists and the block must be projected numerically.  This module's
    first draft asserted a closed form for it; `verify_identities` measured the error at
    **0.617**, i.e. the assertion was false, and the numerical projector replaced it.
    """
    N = int(N)
    if realization == REAL_A:
        return hilb_projector(lambda u: _basis_A(u, N), N, n_nodes=n_nodes, nq=nq)
    if realization == REAL_B:
        # Hpv[phi_n] = T_n exactly; one multiplication by sqrt(1-v^2) lands it in `psi`
        modes = int(sqrt_modes) if sqrt_modes else max(4 * N, 64)
        return cheb_mult_matrix(sqrt_weight_coeffs(modes), N)
    raise ValueError(realization)


# ==========================================================================
# 2.  the profile, and the multiplication operator it induces
# ==========================================================================
_PROFILE_CACHE = {}


def solved_profile(a, K=48):
    """`ReducedProfile` solved once per `a` and cached -- the same converged object feeds the
    multiplication operator and the border column, so they cannot disagree."""
    key = (float(a), int(K))
    if key not in _PROFILE_CACHE:
        from solver.first_integral import ReducedProfile
        rp = ReducedProfile(a=float(a), K=int(K))
        sol = rp.solve()
        if not sol["converged"]:
            raise RuntimeError(f"ReducedProfile did not converge at a={a}: "
                               f"residual {sol['residual']:.3e}")
        _PROFILE_CACHE[key] = (rp, sol)
    return _PROFILE_CACHE[key]


def profile_p_coeffs(a, n_modes=128, on_outside="nan"):
    """Chebyshev-`T` coefficients of `p(v) = e(v)^{1/a - 1}` for the reduced profile.

    `e` is taken from `solver/first_integral.py`'s landed `ReducedProfile` -- the validated
    compact-support object -- and is evaluated ONLY on `|v| <= 1`, with `even_cheb`'s
    `on_outside` policy passed explicitly (leg 107: the default silently fabricated
    out-of-support values).

    Returns `(g, diag)` with `g` the coefficients and `diag` the magnitudes a caller needs
    to judge whether the multiplication operator is bounded in `l^1`: the coefficient
    `l^1` norm and the measured algebraic decay exponent.
    """
    n_modes = int(n_modes)
    rp, sol = solved_profile(a)
    # Chebyshev-Gauss nodes on [-1, 1]; the profile is even, evaluated on |v| <= 1 only,
    # with `on_outside` passed EXPLICITLY (leg 107: the default fabricated off-support values)
    j = np.arange(n_modes)
    v = np.cos((j + 0.5) * np.pi / n_modes)
    e = rp.e_of(sol["b"], np.abs(v), on_outside=on_outside)
    e = np.clip(np.nan_to_num(e, nan=0.0), 0.0, None)
    expo = 1.0 / float(a) - 1.0
    with np.errstate(divide="ignore", invalid="ignore"):
        p = np.where(e > 0.0, e ** expo, 0.0)
    p = np.nan_to_num(p, nan=0.0, posinf=0.0, neginf=0.0)
    # discrete Chebyshev transform on the Gauss nodes
    k = np.arange(n_modes)
    Tk = np.cos(np.outer((j + 0.5) * np.pi / n_modes, k))
    g = (2.0 / n_modes) * (Tk.T @ p)
    g[0] *= 0.5
    l1 = float(np.sum(np.abs(g)))
    tail = np.abs(g[n_modes // 4:n_modes // 2])
    idx = np.arange(n_modes // 4, n_modes // 2, dtype=float)
    ok = tail > 0
    slope = (float(np.polyfit(np.log(idx[ok]), np.log(tail[ok]), 1)[0])
             if ok.sum() >= 3 else float("nan"))
    return g, {"a": float(a), "expo": expo, "coeff_l1": l1,
               "decay_exponent": slope, "n_modes": n_modes,
               "X_c_over_c": float(sol["Xc"]), "profile_residual": sol["residual"],
               "on_outside": on_outside}


def profile_mult_matrix(a, N, n_modes=128):
    """`M_p`: multiplication by `p(v)` in the `T` basis, on indices `1..N`."""
    g, diag = profile_p_coeffs(a, n_modes=n_modes)
    return cheb_mult_matrix(g, N), diag


# ==========================================================================
# 3.  the assembled operator, the split, and leg 54's Z_1
# ==========================================================================
def weight_vector(N, kind="flat", param=0.0):
    """`w_n`, `n = 1..N` -- the same three classes as `spectral_certificate.weight_vector`."""
    n = np.arange(1, int(N) + 1, dtype=float)
    if kind == "flat":
        return np.ones_like(n)
    if kind == "algebraic":
        return (1.0 + n) ** float(param)
    if kind == "geometric":
        return float(param) ** n
    raise ValueError(f"unknown weight class {kind!r}")


def colmax(Mx):
    """leg 54's norm, verbatim: `||.||_w` operator norm in scaled coordinates."""
    Mx = np.abs(np.asarray(Mx, dtype=float))
    return float(np.max(Mx.sum(0))) if Mx.size else 0.0


def profile_mult_matrix_for(realization, a, N, n_modes=128):
    """`M_p` in the basis the DOMAIN actually uses: `T` for realization A, `U` for B."""
    g, diag = profile_p_coeffs(a, n_modes=n_modes)
    if realization == REAL_B:
        return cheb_mult_matrix_U(g, N), diag
    return cheb_mult_matrix(g, N), diag


def border_column(N, realization, a, n_modes=128, nq=1200):
    """`dR/dX_c`, the FREE-BOUNDARY column -- the term that does not exist until you assemble.

    `(RS)`'s unknowns are `(s, X_c)`: the support radius is not data, it is solved for.  A
    `Z_1` measured on the `s`-block alone is the failure mode lesson 89 names -- legs 51-52
    bounded four terms one at a time and the FIFTH, which only exists after assembly, was
    the one that decided.  On the whole line that fifth term was the far-field amplitude
    column and its block coupling was `K/2` (leg 53).  Here it is this column.

        R(e, X_c) = c e' + a X_c Hpv[e^{1/a}]   ==>   dR/dX_c = a Hpv[e^{1/a}] = -c e'/X_c

    computed from the converged profile, projected onto the codomain, and returned scaled.
    """
    N = int(N)
    rp, sol = solved_profile(a)
    b, Xc = sol["b"], sol["Xc"]

    # dR/dX_c = -c e'/X_c , evaluated on Chebyshev-Gauss nodes and projected onto T_1..T_N
    n_nodes = max(2 * N, 64)
    j = np.arange(n_nodes)
    v = np.cos((j + 0.5) * np.pi / n_nodes)
    h = 1e-6
    ep = (rp.e_of(b, np.abs(np.clip(v + h, -1, 1)), on_outside="nan")
          - rp.e_of(b, np.abs(np.clip(v - h, -1, 1)), on_outside="nan")) / (2 * h)
    ep = np.nan_to_num(ep, nan=0.0)
    vals = -ep / float(Xc)
    if realization == REAL_B:
        # the psi codomain carries an extra 1/sqrt(1-v^2): expand sqrt(1-v^2)*vals in T
        vals = vals * np.sqrt(np.maximum(1.0 - v ** 2, 0.0))
    k = np.arange(N + 1)
    Tk = np.cos(np.outer((j + 0.5) * np.pi / n_nodes, k))
    c = (2.0 / n_nodes) * (Tk.T @ vals)
    return c[1:], {"Xc": float(Xc), "col_l1": float(np.sum(np.abs(c[1:])))}


def gauge_row(N, realization, direction="amplitude"):
    """The border ROW: the functional that pins the gauge `(RS)`'s extra unknown needs.

    Swept over a pre-named set rather than fixed, because leg 53 reported one number for all
    four border directions and it turned out the sub-block never saw the border (lesson 90).
    Here the four directions give DIFFERENT rows by construction, and the runner reports the
    spread.
    """
    N = int(N)
    n = np.arange(1, N + 1)
    if direction == "amplitude":            # h(0)
        return (np.cos(n * np.pi / 2.0) if realization == REAL_A
                else np.sin((n) * np.pi / 2.0) / 1.0)
    if direction == "mass":                 # int h
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where(n % 2 == 0, 2.0 / (1.0 - n ** 2), 0.0)
        return r
    if direction == "edge_slope":           # h'(1)
        return n.astype(float) * (-1.0) ** (n + 1)
    if direction == "first_mode":           # e_1
        r = np.zeros(N)
        r[0] = 1.0
        return r
    raise ValueError(direction)


BORDER_DIRECTIONS = ("amplitude", "mass", "edge_slope", "first_mode")


def assemble(N, K, realization=REAL_A, a=0.3, kind="flat", param=0.0, mu=0.0,
             Xc=None, use_profile=True, n_modes=128, bordered=True,
             border_direction="amplitude"):
    """`L` on `1..N` (+ the free-boundary border), SCALED, split as `[[G, B], [C, T]]` at `K`.

    `mu > 0` adds `-mu * n` to the diagonal: the dissipative dial, the SAME convention as
    `spectral_certificate.tail_block(K, M, mu)`, so the positive control here is comparable
    to leg 58's NG3 / leg 126's BX3.

    `bordered=True` puts the `X_c` unknown in, as its own column and its own matching row,
    inside the FINITE block -- the assembly lesson 89 demands.  `bordered=False` is kept only
    so the runner can report what the border costs.
    """
    N, K = int(N), int(K)
    D = deriv_block(N, realization)
    H = hilb_block(N, realization)
    if use_profile:
        Mp, pdiag = profile_mult_matrix_for(realization, a, N, n_modes=n_modes)
        Hp = H @ Mp
    else:
        Hp, pdiag = H, {"a": float(a), "coeff_l1": 1.0, "note": "p == 1 caricature"}
    xc = float(Xc) if Xc is not None else float(pdiag.get("X_c_over_c", 1.0))
    L = D + xc * Hp
    if mu:
        L = L - float(mu) * np.diag(np.arange(1, N + 1, dtype=float))

    w = weight_vector(N, kind, param)
    Ls = L * (w[:, None] / w[None, :])
    bmeta = None
    if bordered:
        col, bmeta = border_column(N, realization, a, n_modes=n_modes)
        row = gauge_row(N, realization, border_direction)
        # the border unknown joins the FINITE block: modes 1..K, then the X_c column
        aug = np.zeros((N + 1, N + 1))
        aug[:N, :N] = Ls
        aug[:N, N] = col * w                     # scaled column
        aug[N, :N] = row / w                     # scaled row
        # reorder so the border sits at the end of the finite block, not after the tail
        idx = list(range(K)) + [N] + list(range(K, N))
        Ls = aug[np.ix_(idx, idx)]
        nG = K + 1
    else:
        nG = K
    n_tail = Ls.shape[0] - nG
    G, B, C, T = Ls[:nG, :nG], Ls[:nG, nG:], Ls[nG:, :nG], Ls[nG:, nG:]
    return {"L": Ls, "G": G, "B": B, "C": C, "T": T, "nG": nG, "n": n_tail,
            "N": N, "K": K, "realization": realization, "a": float(a),
            "class": kind, "param": float(param), "mu": float(mu), "Xc": xc,
            "bordered": bool(bordered), "border_direction": border_direction,
            "border": bmeta, "profile": pdiag, "w": w}


def tail_approx_inverse(ob, mode="diagonal"):
    """`A22`, built from the TAIL's OWN structure -- never `inv(T)`.

    leg 54's MM3 is the ban this respects: inverting the truncated tail makes `Z_1` a
    statement about `numpy.linalg.inv` rather than about a certificate.  `diagonal` is the
    standard radii-polynomial choice (`A22 = diag(T)^-1`), and it EXISTS only when the tail
    has a nonzero diagonal -- which is precisely the realization A / realization B split.
    """
    T = ob["T"]
    n = T.shape[0]
    if n == 0:
        return np.zeros((0, 0)), {"exists": True, "reason": "empty tail"}
    d = np.diag(T)
    dmin = float(np.min(np.abs(d)))
    if mode == "diagonal":
        if dmin <= 1e-13:
            return None, {"exists": False, "min_abs_diagonal": dmin,
                          "reason": "the tail diagonal has a zero -- no diagonal A22 exists"}
        return np.diag(1.0 / d), {"exists": True, "min_abs_diagonal": dmin,
                                  "norm": float(np.max(np.abs(1.0 / d)))}
    if mode == "identity":       # the block-diagonal convention when no inverse exists
        return np.eye(n), {"exists": True, "reason": "A22 = I (the convention when the "
                                                     "tail cannot be inverted)"}
    raise ValueError(mode)


def build_A(ob, shape):
    """The shapes leg 54 named, restricted to the ones this corner can actually carry."""
    G, B, C = ob["G"], ob["B"], ob["C"]
    nG, n = ob["nG"], ob["n"]
    Gi = np.linalg.inv(G)
    A22, meta = tail_approx_inverse(ob, "diagonal")
    if A22 is None:
        A22, meta = tail_approx_inverse(ob, "identity")
    Z, Zt = np.zeros((nG, n)), np.zeros((n, nG))
    if shape == "block_diag":                       # A21 = 0
        return np.block([[Gi, Z], [Zt, A22]]), meta
    if shape == "gs_upper":                         # A21 = 0, exact inverse of [[G,B],[0,T]]
        return np.block([[Gi, -Gi @ B @ A22], [Zt, A22]]), meta
    if shape == "gs_lower":                         # A21 != 0
        return np.block([[Gi, Z], [-A22 @ C @ Gi, A22]]), meta
    if shape == "exact_inv":                        # INADMISSIBLE control (leg 54 MM3)
        return np.linalg.inv(ob["L"]), meta
    raise ValueError(shape)


#: which shapes are legal evidence, and which are the MM3 control
ADMISSIBLE = {"block_diag": True, "gs_upper": True, "gs_lower": True, "exact_inv": False}
A21_ZERO = {"block_diag": True, "gs_upper": True, "gs_lower": False, "exact_inv": False}


def measure(ob, shape):
    """`Z_1 = colmax(I - A L)` -- leg 54's convention, unchanged, plus its four sub-blocks."""
    A, meta = build_A(ob, shape)
    nG, n = ob["nG"], ob["n"]
    R = np.eye(nG + n) - A @ ob["L"]
    return {"shape": shape, "admissible": ADMISSIBLE[shape], "A21_zero": A21_ZERO[shape],
            "realization": ob["realization"], "N": ob["N"], "K": ob["K"],
            "class": ob["class"], "param": ob["param"], "mu": ob["mu"], "a": ob["a"],
            "Z1": colmax(R),
            "Z1_GG": colmax(R[:nG, :nG]), "Z1_Gt": colmax(R[:nG, nG:]),
            "Z1_tG": colmax(R[nG:, :nG]), "Z1_tt": colmax(R[nG:, nG:]),
            "A_norm": colmax(A), "A22": meta}


# ==========================================================================
# 4.  the shape classifier -- one code path, three operators, required to disagree
# ==========================================================================
def classify_tail(T, name):
    """`MULTIPLIER` / `TRIDIAGONAL_DOMINANT` / `SHIFT`, read off MAGNITUDES of the matrix.

    The rule is `solver/certificate_shapes.py`'s own dichotomy made numeric: compare the
    diagonal against the off-diagonal row mass.  Reported with the magnitudes that produced
    it, never as a bare label.
    """
    T = np.asarray(T, dtype=float)
    n = T.shape[0]
    d = np.abs(np.diag(T))
    off = np.abs(T).sum(1) - d
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(off > 0, d / off, np.inf)
    med = float(np.median(ratio[ratio < np.inf])) if np.any(ratio < np.inf) else float("inf")
    min_d = float(np.min(d))
    if min_d <= 1e-13:
        label = SHIFT
    elif med >= 1.0:
        label = MULTIPLIER
    else:
        label = TRIDIAGONAL_DOMINANT
    # the tail-inverse ladder: 1/Lambda_M for a multiplier, a CONSTANT for a shift
    return {"name": name, "n": n, "label": label,
            "min_abs_diagonal": min_d,
            "max_abs_diagonal": float(np.max(d)),
            "median_diag_over_offdiag": med,
            "diagonal_is_exactly_zero": bool(np.all(d == 0.0)),
            "max_abs_offdiagonal": float(np.max(off)) if n else 0.0}


def shape_control_wholeline(K=8, M=256):
    """THE CONTROL (lesson 90).  Same classifier, run on the BANKED compactified whole-line
    tail block.  It must come back `SHIFT` with an exactly-zero diagonal, or the Chebyshev
    classification is a property of this file rather than of the operators."""
    return classify_tail(_wholeline_tail_block(K, M), "wholeline_compactified_tail_block")


def tail_inverse_ladder(realization, Ks=(8, 16, 32, 64), N=256, a=0.3, kind="flat",
                        param=0.0, mu=0.0, use_profile=False):
    """`||A22||` and `||I - A22 T||` against the split `K`.

    For a MULTIPLIER the first decays like `1/K`; for a SHIFT it does not decay at all --
    that is XS3, measured here in the new basis instead of asserted from the old one.
    """
    rows = []
    for K in Ks:
        ob = assemble(N, K, realization, a=a, kind=kind, param=param, mu=mu,
                      use_profile=use_profile)
        A22, meta = tail_approx_inverse(ob, "diagonal")
        if A22 is None:
            rows.append({"K": int(K), "A22_exists": False, "A22_norm": None,
                         "I_minus_A22T": None, "why": meta["reason"],
                         "min_abs_diagonal": meta.get("min_abs_diagonal")})
            continue
        R = np.eye(ob["n"]) - A22 @ ob["T"]
        rows.append({"K": int(K), "A22_exists": True, "A22_norm": colmax(A22),
                     "I_minus_A22T": colmax(R),
                     "min_abs_diagonal": meta.get("min_abs_diagonal")})
    ok = [r for r in rows if r["A22_exists"]]
    slope = None
    if len(ok) >= 2:
        x = np.log([r["K"] for r in ok])
        y = np.log([max(r["A22_norm"], 1e-300) for r in ok])
        slope = float(np.polyfit(x, y, 1)[0])
    return {"realization": realization, "rows": rows, "decay_exponent_in_K": slope,
            "reading": ("a MULTIPLIER tail gives slope ~ -1 (||A22|| ~ 1/K); a SHIFT tail "
                        "gives no diagonal to invert at all")}


# ==========================================================================
# 5.  does the corner even have a domain on leg 126's own object?
# ==========================================================================
def clm_a0_profile(X):
    """The `a = 0` CLM self-similar profile -- the object leg 126 audited.

        Omega_0(X) = -4X / (1 + 4X^2)

    Whole line, algebraic `1/X` decay.  `a = 0` is OUTSIDE HTW's `0 < a < 1`.
    """
    X = np.asarray(X, dtype=float)
    return -4.0 * X / (1.0 + 4.0 * X * X)


def support_transfer_audit(radii=(1.0, 4.0, 16.0, 64.0, 256.0, 1024.0, 4096.0)):
    """Does HTW's compact-support step transfer to leg 126's own operator?  MEASURED.

    For each pre-named radius `R`, the fraction of `|Omega_0|` mass outside `R`, and the
    measured algebraic decay exponent.  A compact support would show this hitting exactly
    zero at some finite `R`; an algebraic tail never does, and the exponent says how slowly.
    """
    rows = []
    for R in radii:
        X = np.linspace(0.0, 200.0 * float(R), 400001)[1:]
        f = np.abs(clm_a0_profile(X))
        tot = float(np.trapezoid(f, X)) if hasattr(np, "trapezoid") else float(np.trapz(f, X))
        m = X > R
        out = (float(np.trapezoid(f[m], X[m])) if hasattr(np, "trapezoid")
               else float(np.trapz(f[m], X[m])))
        rows.append({"R": float(R), "mass_outside_over_total": out / tot,
                     "abs_Omega_at_R": float(np.abs(clm_a0_profile(R)))})
    Xs = np.array([1e2, 1e3, 1e4, 1e5])
    ys = np.abs(clm_a0_profile(Xs))
    expo = float(np.polyfit(np.log(Xs), np.log(ys), 1)[0])
    return {"object": "a = 0 CLM self-similar profile, Omega_0 = -4X/(1+4X^2) -- the object "
                      "leg 126's audit is written on",
            "rows": rows, "decay_exponent": expo,
            "HTW_compact_support_range": "0 < a < 1 (Thm 7.10(3), read by leg 112)",
            "a_of_this_object": 0.0,
            "reading": ("the corner needs a finite interval to put a global basis on.  "
                        "This profile has none: the mass outside R never reaches zero and "
                        "|Omega_0| ~ |X|^expo with expo measured above")}


# ==========================================================================
# 6.  coverage classification against leg 126 -- READ-ONLY
# ==========================================================================
LEG126_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "writeup", "data", "p2_route_bx_v1_stageb.json")


def leg126_axes(path=LEG126_JSON):
    """Leg 126's declared axes, read from its banked JSON.  This module never writes it."""
    with open(path) as fh:
        d = json.load(fh)
    return {"axes": d["BX1_declared_axes"],
            "n_configurations": d["BX2_n_configurations"],
            "n_uncovered": d["BX2_n_uncovered"],
            "source": d["BX1_declared_axes_source"],
            "gate_answer": d["gate_answer"],
            "object": d["object"]}


def coverage_classification(path=LEG126_JSON):
    """Is this corner inside leg 126's enumeration?  A MEMBERSHIP TEST, not an argument.

    The corner is a value on the `realization` axis.  Leg 126 declared that axis with three
    entries and audited 1,686 configurations over it; `certificate_shapes.py` has no basis
    axis at all -- its vocabulary classifies the SHAPE of the unbounded part, which is a
    consequence of the basis, not the basis itself.
    """
    bk = leg126_axes(path)
    declared = list(bk["axes"]["realization"])
    ours = [REAL_A, REAL_B]
    inside = [r for r in ours if r in declared]
    return {"leg126_realization_axis": declared,
            "this_corner": ours,
            "inside_the_enumeration": inside,
            "uncovered": [r for r in ours if r not in declared],
            "which_axis": "realization (the SPACE degree of freedom of stage B)",
            "leg126_n_configurations": bk["n_configurations"],
            "leg126_n_uncovered": bk["n_uncovered"],
            "certificate_shapes_has_a_basis_axis": False,
            "certificate_shapes_vocabulary": [MULTIPLIER, TRIDIAGONAL_DOMINANT, SHIFT],
            "note": ("`certificate_shapes.py` classifies the SHAPE of the unbounded part "
                     "(MULTIPLIER / TRIDIAGONAL_DOMINANT / SHIFT / NO_UNBOUNDED_PART) and "
                     "the shape of the approximate inverse.  It enumerates no basis and no "
                     "domain, so it cannot cover or fail to cover a basis corner; the "
                     "membership test that CAN be run is against leg 126's realization "
                     "axis, and it is run above.")}


# ==========================================================================
# 6b.  THE OPERATOR'S OWN KNOWN-ANSWER GATE
# ==========================================================================
def operator_known_answer_gate(N=24, realization=REAL_B, a=0.3, seed=0, nq=1500,
                               vs=(-0.62, -0.17, 0.29, 0.74), smoothness=6):
    """Is the assembled matrix the operator it claims to be?  Matrix vs direct evaluation.

    `L h = c h' + X_c Hpv[p h]`, `c = 1`.  A random coefficient vector is pushed through the
    ASSEMBLED matrix and, independently, through a direct pointwise evaluation of the same
    formula (numerical derivative + the verified principal-value quadrature).  The two must
    agree.  Without this gate a `Z_1` is a statement about matrix assembly, not about the
    operator (lesson 85: re-measure the headline, and ablate the MECHANISM).

    **`smoothness` is load-bearing, and this gate's first draft got it wrong.**  The
    comparison is POINTWISE, so the matrix side must reconstruct `sum_m c_m psi_m(v)` from
    `N` terms.  The unbounded part multiplies input coefficients by `-n`, so a probe
    decaying like `n^-2` gives an output series decaying like `n^-1`, whose pointwise
    partial sums converge only like `1/N`.  At `smoothness = 2` this gate reported a `1.1%`
    floor that did NOT move under an 8x refinement of the quadrature -- it was measuring its
    own reconstruction, not the operator.  At `smoothness = 6` the same gate reads `3.4e-4`.
    """
    rng = np.random.default_rng(int(seed))
    N = int(N)
    coef = rng.standard_normal(N) / np.arange(1, N + 1) ** float(smoothness)
    rp, sol = solved_profile(a)
    Xc = float(sol["Xc"])
    expo = 1.0 / float(a) - 1.0

    def p_of(u):
        e = rp.e_of(sol["b"], np.abs(np.clip(u, -1.0, 1.0)), on_outside="nan")
        e = np.clip(np.nan_to_num(np.asarray(e, dtype=float), nan=0.0), 0.0, None)
        return np.where(e > 0.0, e ** expo, 0.0)

    if realization == REAL_B:
        def h_of(u):
            u = np.asarray(u, dtype=float)
            s = np.sqrt(np.maximum(1.0 - u ** 2, 0.0))
            return sum(coef[n - 1] * s * _cheb_U(n - 1, u) for n in range(1, N + 1))
    else:
        def h_of(u):
            u = np.asarray(u, dtype=float)
            return sum(coef[n - 1] * (1.0 - u ** 2) * _cheb_T(n, u) for n in range(1, N + 1))

    v = np.asarray(vs, dtype=float)
    dh = 1e-6
    direct = ((h_of(v + dh) - h_of(v - dh)) / (2 * dh)
              + Xc * _hilb_pv(lambda u: p_of(u) * h_of(u), v, nq))

    ob = assemble(N, N - 1, realization, a=a, kind="flat", use_profile=True, bordered=False)
    out = ob["L"] @ coef
    m = np.arange(1, N + 1)
    Tm = np.cos(np.outer(np.arccos(np.clip(v, -1, 1)), m))
    matrix = Tm @ out
    if realization == REAL_B:
        matrix = matrix / np.sqrt(1.0 - v ** 2)      # psi_m = T_m / sqrt(1-v^2)

    denom = float(np.max(np.abs(direct)))
    return {"realization": realization, "a": float(a), "N": N,
            "smoothness_of_probe": float(smoothness), "sample_points": v.tolist(),
            "direct": direct.tolist(), "matrix": matrix.tolist(),
            "max_abs_err": float(np.max(np.abs(direct - matrix))),
            "max_rel_err": float(np.max(np.abs(direct - matrix)) / denom) if denom else None,
            "scale": denom}


def target_membership(a=0.3, realization=REAL_B, N=192, kind="algebraic", param=1.0):
    """Is the certificate's own TARGET in the certificate's space?  (leg 126 clause SPACE-TARGET)

    The perturbation direction that matters is the profile's own tangent -- here `e` itself,
    the solution the certificate would enclose.  Expanded in this realization's DOMAIN basis,
    with the weighted `l^1` partial sums and the measured coefficient decay.  A configuration
    whose target has infinite norm is **not a legal certificate**, whatever its `Z_1`.
    """
    rp, sol = solved_profile(a)
    N = int(N)
    n_nodes = max(4 * N, 256)
    j = np.arange(n_nodes)
    v = np.cos((j + 0.5) * np.pi / n_nodes)
    e = np.nan_to_num(rp.e_of(sol["b"], np.abs(v), on_outside="nan"), nan=0.0)
    if realization == REAL_B:
        # e = sqrt(1-v^2) * g  =>  expand g in U_{n-1}; U-coefficients via the sine transform
        th = np.arccos(np.clip(v, -1.0, 1.0))
        s = np.sin(th)
        g = np.where(s > 1e-12, e / np.where(s > 1e-12, s, 1.0), 0.0)
        n = np.arange(1, N + 1)
        Un = np.sin(np.outer(th, n)) / np.where(s > 1e-12, s, 1.0)[:, None]
        # discrete projection with the U weight sin^2
        wgt = s ** 2
        coef = (2.0 / np.pi) * (np.pi / n_nodes) * (Un * wgt[:, None]).T @ g * 2.0
    else:
        # e = (1-v^2) s(v)  =>  expand s in T_n
        g = np.where(np.abs(v) < 1.0 - 1e-12, e / np.maximum(1.0 - v ** 2, 1e-300), 0.0)
        k = np.arange(1, N + 1)
        Tk = np.cos(np.outer((j + 0.5) * np.pi / n_nodes, k))
        coef = (2.0 / n_nodes) * (Tk.T @ g)
    w = weight_vector(N, kind, param)
    parts = np.cumsum(np.abs(coef) * w)
    tail = np.abs(coef[N // 4:N // 2])
    idx = np.arange(N // 4, N // 2, dtype=float)
    ok = tail > 0
    slope = (float(np.polyfit(np.log(idx[ok]), np.log(tail[ok]), 1)[0])
             if ok.sum() >= 3 else float("nan"))
    return {"realization": realization, "a": float(a), "class": kind, "param": float(param),
            "N": N, "weighted_l1_partial_sums": [float(parts[m]) for m in
                                                 (N // 8, N // 4, N // 2, N - 1)],
            "coefficient_decay_exponent": slope,
            "weight_growth_exponent": float(param) if kind == "algebraic" else 0.0,
            "converges_iff": "decay_exponent + weight_growth_exponent < -1",
            "margin": (slope + float(param) + 1.0) if kind == "algebraic" else None}


# ==========================================================================
# 7.  self-check: every identity above, verified numerically
# ==========================================================================
def _cheb_T(n, v):
    return np.cos(n * np.arccos(np.clip(v, -1.0, 1.0)))


def _cheb_U(n, v):
    th = np.arccos(np.clip(v, -1.0, 1.0))
    s = np.sin(th)
    out = np.where(np.abs(s) > 1e-12, np.sin((n + 1) * th) / np.where(np.abs(s) > 1e-12, s, 1.0),
                   (n + 1.0) * np.cos(n * np.pi * (v < 0)))
    return out


_LEGGAUSS_CACHE = {}


def _leggauss_cached(n):
    if n not in _LEGGAUSS_CACHE:
        _LEGGAUSS_CACHE[n] = np.polynomial.legendre.leggauss(int(n))
    return _LEGGAUSS_CACHE[n]


def _hilb_pv(f, v, n=20001):
    """`(1/pi) p.v. int_{-1}^{1} f(u)/(v-u) du`, by SINGULARITY SUBTRACTION.

        p.v. int f(u)/(v-u) du  =  int [f(u) - f(v)]/(v-u) du  +  f(v) ln|(v+1)/(v-1)|

    The first integrand is smooth wherever `f` is Lipschitz, so a plain Gauss-Legendre rule
    converges on it; the naive midpoint rule does NOT, because the `1/(v-u)` pole is only
    cancelled when `v` sits exactly halfway between two nodes.  That naive rule was this
    module's first draft and it reported errors of ~4.6 on identities that are exact --
    recorded here because a quadrature that silently misses a principal value is precisely
    lesson 86 ("a bound dominated by its own EVALUATION error is a statement about the
    code").
    """
    x, wq = _leggauss_cached(int(n))
    out = np.empty(np.atleast_1d(v).shape, dtype=float)
    for i, vi in enumerate(np.atleast_1d(v)):
        fv = float(np.atleast_1d(f(np.array([vi])))[0])
        num = f(x) - fv
        with np.errstate(divide="ignore", invalid="ignore"):
            g = np.where(np.abs(vi - x) > 1e-14, num / (vi - x), 0.0)
        reg = float(np.sum(wq * g))
        out.flat[i] = (reg + fv * np.log(abs((vi + 1.0) / (vi - 1.0)))) / np.pi
    return out


def verify_identities(N=6, vs=(-0.71, -0.2, 0.13, 0.55, 0.87), n_quad=200001):
    """Check the four closed forms this module rests on against direct evaluation.

    The Hilbert-transform SIGN is the one that is checked hardest: `Hpv[w](v)` here uses
    `(v - u)` in the denominator (this repository's convention, `solver/first_integral.py`),
    and the textbook Tricomi identities are stated with `(u - v)`.  A sign slip there is
    exactly the failure mode leg 112 was spawned to rule out on the `a`-sign, so it is
    measured rather than asserted.
    """
    vs = np.asarray(vs, dtype=float)
    res = {}

    # (i) d/dv[(1-v^2) T_n] = ((n-2)/2) T_{n-1} - ((n+2)/2) T_{n+1}
    err = 0.0
    for n in range(1, N + 1):
        h = 1e-5
        num = (((1 - (vs + h) ** 2) * _cheb_T(n, vs + h))
               - ((1 - (vs - h) ** 2) * _cheb_T(n, vs - h))) / (2 * h)
        ana = (n - 2.0) / 2.0 * _cheb_T(n - 1, vs) - (n + 2.0) / 2.0 * _cheb_T(n + 1, vs)
        err = max(err, float(np.max(np.abs(num - ana))))
    res["derivA_max_abs_err"] = err

    # (ii) d/dv[sqrt(1-v^2) U_{n-1}] = -n T_n / sqrt(1-v^2)
    err = 0.0
    for n in range(1, N + 1):
        h = 1e-5
        def w(x, n=n):
            return np.sqrt(np.maximum(1 - x ** 2, 0.0)) * _cheb_U(n - 1, x)
        num = (w(vs + h) - w(vs - h)) / (2 * h)
        ana = -n * _cheb_T(n, vs) / np.sqrt(1 - vs ** 2)
        err = max(err, float(np.max(np.abs(num - ana))))
    res["derivB_max_abs_err"] = err

    # (iii) THE PROJECTOR'S KNOWN-ANSWER GATE (lesson 84: a known-answer probe has a WINDOW).
    # `hilb_projector` is the numerical route realization A must use.  Run it on the ONE
    # family whose answer is exact -- the airfoil basis, where Hpv[phi_n] = T_n, i.e. the
    # identity matrix -- and report the max deviation from `I`.  If this is not small the
    # realization-A block is not evidence of anything.
    def _airfoil(u, N=N):
        u = np.asarray(u, dtype=float)
        s = np.sqrt(np.maximum(1.0 - u ** 2, 0.0))
        return np.column_stack([s * _cheb_U(n - 1, u) for n in range(1, N + 1)])

    got = hilb_projector(_airfoil, N, nq=n_quad)
    res["projector_known_answer_max_abs_err_vs_I"] = float(np.max(np.abs(got - np.eye(N))))

    # and the realization-A block itself, for the record: no closed form exists (see
    # `hilb_block`), so what is reported is its magnitude and its bandedness
    HA = hilb_block(N, REAL_A, nq=n_quad)
    res["hilbA_colmax"] = colmax(HA)
    res["hilbA_max_abs_entry"] = float(np.max(np.abs(HA)))
    res["hilbA_has_closed_form"] = False

    # (iv) Hpv[sqrt(1-u^2) U_{n-1}](v) = T_n(v)                    -- realization B
    err = 0.0
    for n in range(1, N + 1):
        got = _hilb_pv(lambda u, n=n: np.sqrt(np.maximum(1 - u ** 2, 0.0)) * _cheb_U(n - 1, u),
                       vs, n_quad)
        ana = _cheb_T(n, vs)
        err = max(err, float(np.max(np.abs(got - ana))))
    res["hilbB_max_abs_err"] = err

    # (v) the sqrt(1-v^2) coefficient list, and its l^1 norm (4/pi for the exact series)
    g = sqrt_weight_coeffs(4096)
    v = np.linspace(-0.999, 0.999, 2001)
    approx = sum(gm * _cheb_T(m, v) for m, gm in enumerate(g) if gm != 0.0)
    res["sqrt_weight_max_abs_err"] = float(np.max(np.abs(approx - np.sqrt(1 - v ** 2))))
    res["sqrt_weight_coeff_l1"] = float(np.sum(np.abs(g)))
    res["sqrt_weight_coeff_l1_exact_4_over_pi"] = 4.0 / np.pi
    res["quadrature_nodes"] = int(n_quad)
    res["convention"] = "Hpv[w](v) = (1/pi) p.v. int_{-1}^{1} w(u)/(v-u) du"
    return res
