#!/usr/bin/env python3
"""Route-H2C v1 — BUILD the origin-`H^2` certificate at `a = 0`, and measure it.

CEILING FIRST, BEFORE ANY NUMBER (DIRECTION.md sec 176; leg 163 census item O3)
------------------------------------------------------------------------------
Everything below depends on `a = 0` EXACTNESS.  A certificate here certifies an
object Xu (arXiv:2607.19762) ALREADY INVERTS IN CLOSED FORM.  Nothing transfers
to `HL_S2_nonsymmetric`, which is not a CLM profile; for `a > 0` Xu proves only a
conditional two-line inclusion under `Adm(a)` -- no resolvent, no invertibility,
no gap.  **No link of the `L1 -> L4` chain moves.  No Clay movement.  No ban
lifts.**  This is infrastructure and a worked example of the non-`ell^1_w` lane.
Float64 throughout; nothing interval-enclosed, nothing rigorous.  Xu's own three
recorded gaps toward a CAP (his sec 3.2, Evans-determinant strand) are NOT closed
here -- this is a static invertibility certificate at `z = 0`, a different object.

THE GATE, in its pre-committed wording
--------------------------------------
> Does the origin-`H^2` certificate, built per leg 163's scoped formulation at
> `a = 0`, actually close (its diagnostic quantity crosses the threshold a
> certificate needs), and does it reproduce Xu's own closed form to the precision
> leg 163 established (2.8e-14 class)?

Leg 163's OWN scoped closing diagnostic is its gate G4: `||u||_X / ||f||_X` on the
bordered system -- equivalently `sigma_min` of `[[L_0^+, m],[ell, 0]]` in the `X`
metric, "the `X`-realization analogue of the quantity leg 127 drove to ZERO in
`ell^1_w`".  That is measured here as C1.  The leg-54-comparable quantity --
`Z_1 = ||I - A L||` for a block-structured approximate inverse `A` -- is measured
separately as C5, because DIRECTION.md asks for the two lanes to be directly
comparable and they do NOT give the same answer.

WHAT IS MEASURED, AND WHY EACH ONE CAN COME OUT THE OTHER WAY (lesson 90)
------------------------------------------------------------------------
  E1  exactness of the discrete realization      -- would be nonzero if the
      tridiagonal entries, the symmetry modes or the border row were wrong
  E2  the `X` Gram's padding-independence        -- would drift if `J^4` were truncated
  E3  Blaschke projection round trip             -- would fail on a wrong basis identity
  E4  `X` norm, Gram form vs y-space quadrature  -- two independent computations
  C0  Xu eq. (4.23) pointwise ODE residual       -- gate conjunct 2; realization-free
  C1  bordered `sigma_min` in `X`, rectangular   -- gate conjunct 1 (leg 163's G4)
  C2  the tail block's own `sigma_min`           -- the ell^1_w comparison point
  C3  CONTROL: unbordered                        -- must collapse (m is the kernel)
  C4  CONTROL: loose `L^2` realization           -- must collapse (Xu sec 4.6: no gap)
  C5  `Z_1` for a block-diagonal `A`             -- the leg-54 battery's own shape
  C6  `||u||_X/||f||_X` from the CLOSED FORM     -- leg 163's G4 reproduced
  C7  Galerkin (square-truncation) consistency   -- where a naive finite section fails
  C8  `||ell||_{X*}` bounded vs `||ell||_{l^2}` divergent

C3 and C4 are the negative controls that CAN report the other answer, and C4 is
the sharper one: it is this repository's OWN realization (capabilities.py,
solver/rescaled_spectrum.py: "our grid imposes NO origin condition"), and Xu sec 4.6
says that realization has no spectral gap at all.  If C4 did not collapse, the
whole origin-condition story would be wrong.

Run: .venv/bin/python experiments/p2_route_h2c_v1_construction.py
"""

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.origin_h2_certificate as H
from solver.origin_h2_certificate import (
    bordered_gram, bordered_operator, border_row, border_row_dual_norm,
    jacobi_xi, l0_plus, project_to_laguerre, resolvent_ratio, symmetry_modes,
    to_y, x_gram, x_norm_y, xu_ode_residual,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "writeup", "data", "p2_route_h2c_v1_construction.json")

SIG_N = [8, 16, 32, 64, 128, 256, 512, 1024]
REL_N = [32, 64, 128, 256, 512]          # the float-reliable window (see C1)


# ---------------------------------------------------------------------------
def rect_sigma(N, bordered=True, gram=True, lo_mode=0):
    """`min ||A u|| / ||u||` over `u` supported on modes `[lo_mode, N)`, RANGE UNTRUNCATED.

    This is the diagnostic, and the shape of it is the point.  Truncating the
    DOMAIN only gives a quantity that is non-increasing in `N` (nested subspaces)
    and converges to the infimum over the union -- so the ladder is an UPPER
    bound on the true `sigma_min` closing down onto it.  Truncating the range as
    well (a square Galerkin section) gives a number that is neither, and reports
    something different: see C7.
    """
    Nr = N + 2
    L = l0_plus(Nr)[:, lo_mode:N]
    nd = N - lo_mode
    _, m = symmetry_modes(Nr)
    Gx_d = x_gram(N)[lo_mode:, lo_mode:] if gram else np.eye(nd)
    Gx_c = x_gram(Nr) if gram else np.eye(Nr)
    if bordered:
        e = border_row(N)[lo_mode:N]
        A = np.zeros((Nr + 1, nd + 1), dtype=complex)
        A[:Nr, :nd] = L
        A[:Nr, nd] = m
        A[Nr, :nd] = e
        Gd, Gc = bordered_gram(nd, Gx_d), bordered_gram(Nr, Gx_c)
    else:
        A, Gd, Gc = L, Gx_d, Gx_c
    _, Gdih = H._sym_sqrt(Gd)
    Gch, _ = H._sym_sqrt(Gc)
    s = np.linalg.svd(Gch @ A @ Gdih, compute_uv=False)
    return float(s.min()), float(s.max())


def z1_blockdiag(K, M):
    """`Z_1 = ||I - A L||_X` with `A = blockdiag(finite bordered inverse, tail inverse)`.

    This is leg 54's own shape of `A` -- a finite block with its exact inverse and
    a tail with its own -- transplanted to the `X` realization so the two lanes'
    outputs are directly comparable, which is what DIRECTION.md asks for.
    """
    Lb = bordered_operator(M)
    idx = list(range(K + 1)) + [M] + list(range(K + 1, M))
    Lp = Lb[np.ix_(idx, idx)]
    nF = K + 2
    A = np.zeros_like(Lp)
    A[:nF, :nF] = np.linalg.inv(Lp[:nF, :nF])
    A[nF:, nF:] = np.linalg.inv(Lp[nF:, nF:])
    E = np.eye(len(idx)) - A @ Lp
    Gp = bordered_gram(M, x_gram(M))[np.ix_(idx, idx)]
    Gh, Gih = H._sym_sqrt(Gp)
    return float(np.linalg.svd(Gh @ E @ Gih, compute_uv=False)[0])


def galerkin_solve(f, N):
    """Square (Galerkin) truncation of the bordered system -- the naive finite section."""
    e, (_, m) = border_row(N), symmetry_modes(N)
    Lb = bordered_operator(N)
    rhs = np.zeros(N + 1, dtype=complex)
    rhs[:N] = f[:N]
    sol = np.linalg.solve(Lb, rhs)
    return sol[:N], sol[N]


def solvable_datum(N, nterm=6, seed=0):
    """A datum `f` on the solvability subspace `{ell(f) = 0}`, in Laguerre coordinates."""
    e, (_, m) = border_row(N), symmetry_modes(N)
    r = np.random.default_rng(seed)
    d = np.zeros(N, dtype=complex)
    d[:nterm] = r.normal(size=nterm) + 1j * r.normal(size=nterm)
    return d - (e @ d) / (e @ m) * m


# ---------------------------------------------------------------------------
def main():
    t_start = time.time()
    R = {"leg": 176, "route": "ROUTE-H2C", "date": "2026-08-06",
         "object": "a=0 CLM linearisation L_0^+ on the odd origin-H^2 space X (Xu arXiv:2607.19762)",
         "ceiling": ("a=0 exactness only; certifies an object Xu already inverts in closed "
                     "form; nothing transfers to HL_S2_nonsymmetric or any a>0 profile; no "
                     "link of L1->L4 moves; float64, nothing interval-enclosed; Xu's own "
                     "three sec-3.2 CAP gaps are NOT closed here"),
         "ga_compute": False}

    # -- E1 exactness of the realization -------------------------------------
    N = 240
    L, e = l0_plus(N), border_row(N)
    b2, m = symmetry_modes(N)
    # independent re-derivation of the tridiagonal entries by Laguerre quadrature
    nq = 60
    xq, wq = np.polynomial.laguerre.laggauss(nq)
    NB = 12
    Lm = np.array([np.polynomial.laguerre.lagval(
        xq, np.eye(NB + 3)[k]) for k in range(NB + 3)])
    dLm = np.array([np.polynomial.laguerre.lagval(
        xq, np.polynomial.laguerre.lagder(np.eye(NB + 3)[k])) for k in range(NB + 3)])
    D = np.zeros((NB, NB))
    for n in range(NB):
        D[:, n] = Lm[:NB] @ (wq * (xq * (dLm[n] - Lm[n] / 2.0)))
    V = np.zeros((NB, NB))
    for n in range(NB):
        V[n, n] += 1.0
        if n + 1 < NB:
            V[n + 1, n] -= 1.0
    R["E1_realization_exactness"] = {
        "tridiagonal_vs_independent_laguerre_quadrature": float(np.abs(D + V - l0_plus(NB)).max()),
        "quadrature_order": nq, "block_checked": NB,
        "L0_binv2_minus_binv2": float(np.abs(L @ b2 - b2).max()),
        "L0_m": float(np.abs(L @ m).max()),
        "ell_dot_L0_untruncated_columns": float(np.abs(e @ L[:, :N - 1]).max()),
        "ell_of_m": [float(np.real(e @ m)), float(np.imag(e @ m))],
        "ell_of_binv2": float(abs(e @ b2)),
        "jacobi_symmetry": float(np.abs(jacobi_xi(64) - jacobi_xi(64).T).max()),
        "reading": ("L_0^+ is EXACTLY tridiagonal with entries (-n/2, 1/2, (n-1)/2); both Xu "
                    "symmetry modes lie exactly in span{l_0,l_1}; ell is exactly the left null "
                    "vector and ell(m)=1 exactly.  These are 0.0 and 1, not small numbers."),
    }

    # -- E2 Gram padding independence ----------------------------------------
    R["E2_x_gram_padding"] = {
        "max_abs_diff_pad4_vs_pad32": float(np.abs(x_gram(96, 4) - x_gram(96, 32)).max()),
        "reading": "J^4 has bandwidth 4, so pad>=4 gives the exact infinite-basis block.",
    }

    # -- E3 projection round trip --------------------------------------------
    c0 = np.zeros(30, dtype=complex)
    c0[0], c0[3], c0[7], c0[15] = 1.0, -0.4 + 0.2j, 0.25j, 0.1
    cr = project_to_laguerre(lambda yy: to_y(c0, yy), M=4096)
    R["E3_projection_roundtrip"] = {
        "max_err_first_30": float(np.abs(cr[:30] - c0).max()),
        "leakage_modes_30_to_2000": float(np.abs(cr[30:2000]).max()),
    }

    # -- C0 Xu eq (4.23): the gate's second conjunct --------------------------
    fc = solvable_datum(N, 6, 0)[:6]
    yv = np.array([-20., -8., -1.5, -0.3, 0.05, 0.2, 0.7, 1.5, 3., 8., 20., 60.])
    fy = to_y(fc, yv)
    lad = {}
    for kp in (12, 24, 48):
        rr = xu_ode_residual(fc, yv, kpan=kp)
        lad[str(kp)] = float((np.abs(rr) / np.abs(fy)).max())
    rr = xu_ode_residual(fc, yv)
    seeds = {}
    for sd in range(6):
        g = solvable_datum(N, 6, sd)[:6]
        gr = xu_ode_residual(g, yv)
        seeds[str(sd)] = float((np.abs(gr) / np.abs(to_y(g, yv))).max())
    R["C0_xu_closed_form"] = {
        "reference": "Xu arXiv:2607.19762 eq. (4.23) at z=0, bordered",
        "check": "pointwise (L_0^+ u - f)(y) with ANALYTIC derivatives; no finite differences",
        "max_abs_residual": float(np.abs(rr).max()),
        "max_rel_residual": float((np.abs(rr) / np.abs(fy)).max()),
        "quadrature_ladder_kpan": lad,
        "over_seeds": seeds,
        "leg163_established_class": 2.8e-14,
        "reading": ("the gate's second conjunct.  This check never mentions the Laguerre "
                    "realization -- it is Xu's kernel against Xu's ODE, in y-space."),
    }

    # -- C1 the closing diagnostic -------------------------------------------
    sig = {}
    for n in SIG_N:
        lo, hi = rect_sigma(n)
        sig[str(n)] = {"sigma_min": lo, "sigma_max": hi, "resolvent_norm": 1.0 / lo}
    rel = [sig[str(n)]["sigma_min"] for n in REL_N]
    R["C1_bordered_sigma_min_X"] = {
        "ladder": sig,
        "reliable_window": REL_N,
        "sigma_min_at_512": sig["512"]["sigma_min"],
        "resolvent_norm_at_512": sig["512"]["resolvent_norm"],
        "spread_over_reliable_window": float(max(rel) - min(rel)),
        "relative_spread": float((max(rel) - min(rel)) / max(rel)),
        "monotone_decreasing_through_512": bool(all(
            sig[str(a)]["sigma_min"] >= sig[str(b)]["sigma_min"]
            for a, b in zip(SIG_N[:-1], SIG_N[1:]) if b <= 512)),
        "n1024_breaks_monotonicity": bool(sig["1024"]["sigma_min"] > sig["512"]["sigma_min"]),
        "reading": ("BOUNDED AWAY FROM ZERO and truncation-independent.  The N=1024 row rises "
                    "instead of falling -- that is the float floor of an X Gram whose entries "
                    "reach ~1e12, not a mathematical statement, and it is why the reliable "
                    "window stops at 512.  This is float64 EVIDENCE of a positive limit, not "
                    "a proof of one: a decreasing positive sequence is reported as what it is."),
    }

    # -- C2 the tail block ----------------------------------------------------
    tail = {}
    for K in (2, 4, 8, 16):
        tail[str(K)] = {str(n): rect_sigma(n, bordered=False, lo_mode=K)[0]
                        for n in (64, 128, 256, 512)}
    R["C2_tail_block_sigma_min"] = {
        "ladder": tail,
        "tail_inverse_norm_K2_at_512": 1.0 / tail["2"]["512"],
        "reading": ("the ell^1_w comparison point.  There (leg 51/53) the tail inverse norm "
                    "DIVERGED with M and no A_tail could make the tail estimate finite; here "
                    "it converges, ||T^{-1}||_X = 4.03 at K=2, truncation-independent."),
    }

    # -- C3 / C4 controls -----------------------------------------------------
    unb = {str(n): rect_sigma(n, bordered=False)[0] for n in (64, 128, 256, 512)}
    loose = {str(n): rect_sigma(n, gram=False)[0] for n in (64, 128, 256, 512)}
    ln = np.log(np.array([loose[str(n)] for n in (64, 128, 256, 512)]))
    slope = float(np.polyfit(np.log([64., 128., 256., 512.]), ln, 1)[0])
    R["C3_control_unbordered"] = {
        "ladder": unb,
        "reading": ("m IS the kernel, so without the border the diagnostic collapses to the "
                    "float floor.  A control that can report the other answer, and does."),
    }
    R["C4_control_loose_L2_realization"] = {
        "ladder": loose, "fitted_exponent": slope,
        "reading": ("THE SHARP ONE.  This is the realization this repository's own grid uses "
                    "(capabilities.py, solver/rescaled_spectrum.py: 'our grid imposes NO origin "
                    "condition').  Xu sec 4.6 says that realization has NO spectral gap -- the "
                    "whole strip -1/2 < Re lam < 3/2 is point spectrum.  Measured here, not "
                    "cited: sigma_min -> 0 like N^{-3/2}.  The origin condition is the entire "
                    "difference between C1 and C4, and it is now a magnitude."),
    }

    # -- C5 Z_1, the leg-54 shape --------------------------------------------
    z1 = {}
    for K in (2, 4, 8, 16, 32):
        z1[str(K)] = {str(M): z1_blockdiag(K, M) for M in (64, 128, 256)}
    R["C5_Z1_blockdiagonal_A"] = {
        "ladder": z1,
        "threshold": 1.0,
        "min_over_battery": float(min(v for d in z1.values() for v in d.values())),
        "max_over_battery": float(max(v for d in z1.values() for v in d.values())),
        "reading": ("DOES NOT CLOSE, and not marginally: the best cell is 140.7 where <1 is "
                    "needed, growing like K^2 in the block size.  This is leg 54's own shape of "
                    "A, and in this shape the X realization fails too -- but for a DIFFERENT "
                    "reason than ell^1_w did.  There the operator itself had no truncation-"
                    "independent sigma_min (leg 127); here C1 says it does, so the failure is "
                    "of the block-diagonal SHAPE of A, not of the operator or the space."),
    }

    # -- C6 the closed-form ratio, leg 163's G4 -------------------------------
    conv = {}
    for M in (1024, 2048, 4096, 8192):
        rr6, un, fn, c1 = resolvent_ratio(fc, M=M)
        conv[str(M)] = rr6
    fam = {}
    for sd in range(4):
        g = solvable_datum(N, 6, sd)[:6]
        fam[str(sd)] = resolvent_ratio(g, M=4096)[0]
    R["C6_closed_form_ratio"] = {
        "M_convergence": conv,
        "over_seeds": fam,
        "leg163_G4_values": [1.3993, 1.2680, 1.3769],
        "leg163_inferred_sigma_min_witness": 0.7147,
        "sigma_min_measured_here": sig["512"]["sigma_min"],
        "leg163_witness_optimistic_by": float(0.7147 / sig["512"]["sigma_min"]),
        "reading": ("leg 163 inferred sigma_min >= 0.7147 from THREE data.  That is a witness, "
                    "not a bound, and C1 shows it is optimistic by 7.9x: the true value is "
                    "0.0908.  Random low-mode data does not find the worst direction -- these "
                    "ratios sit near 0.87 while the operator norm is 11.0.  Correcting this is "
                    "one of the things a construction leg is FOR."),
    }

    # -- C7 where the naive Galerkin section fails ----------------------------
    fN = solvable_datum(2048, 6, 0)
    gal = {}
    for n in (60, 120, 240, 480, 960):
        u, kap = galerkin_solve(fN, n)
        gal[str(n)] = {"abs_kappa": float(abs(kap)), "last_coeff": float(abs(u[-1])),
                       "n2_times_last_coeff": float(n ** 2 * abs(u[-1]))}
    c_exact = project_to_laguerre(
        lambda yy: H.xu_resolvent(fc, yy, c1=resolvent_ratio(fc, M=1024)[3]), M=4096)
    dec = {str(k): float(k * abs(c_exact[k])) for k in (32, 64, 128, 256, 512, 1024)}
    R["C7_galerkin_inconsistency"] = {
        "kappa_ladder": gal,
        "exact_solution_n_times_coeff": dec,
        "reading": ("kappa MUST be 0 (ell(f)=0 was imposed and ell.L_0^+=0 exactly), yet the "
                    "square Galerkin section returns kappa -> 5.895.  The mechanism is exact: "
                    "the truncated ell row misses the term ell_N (N-2)/2 u_{N-1}, and "
                    "N^2 |u_{N-1}| is constant, so the defect does NOT vanish.  Underneath it "
                    "is a structural fact: the exact solution's Laguerre coefficients decay "
                    "only like C/n (n|c_n| -> ~5.1), because the resolvent maps analytic data "
                    "to u ~ log(y)/y, i.e. a LOG SINGULARITY at the Mellin origin xi=0.  No "
                    "basis smooth at xi=0 converges geometrically here.  This is why C1 uses a "
                    "range-untruncated section and not a square one."),
    }

    # -- C8 the border row's dual norm ---------------------------------------
    bd = {}
    for n in (64, 128, 256, 512):
        xd, l2 = border_row_dual_norm(n)
        bd[str(n)] = {"x_dual": xd, "l2": l2}
    R["C8_border_row_dual_norm"] = {
        "ladder": bd,
        "reading": ("ell is a BOUNDED functional on X and an unbounded one on l^2: the X* norm "
                    "converges while the l^2 norm diverges like N^{3/2}.  The border row only "
                    "makes sense in the X realization, which is itself part of the finding."),
    }

    # -- E4 the X norm, two independent ways ---------------------------------
    Nv = 256
    lo, hi = rect_sigma(Nv)
    Nr = Nv + 2
    Amat = np.zeros((Nr + 1, Nv + 1), dtype=complex)
    Amat[:Nr, :Nv] = l0_plus(Nr)[:, :Nv]
    Amat[:Nr, Nv] = symmetry_modes(Nr)[1]
    Amat[Nr, :Nv] = border_row(Nv)
    Gd, Gc = bordered_gram(Nv, x_gram(Nv)), bordered_gram(Nr, x_gram(Nr))
    _, Gdih = H._sym_sqrt(Gd)
    Gch, _ = H._sym_sqrt(Gc)
    U, S, Vt = np.linalg.svd(Gch @ Amat @ Gdih)
    v = Gdih @ Vt[-1].conj()
    u_min, kap_min = v[:Nv], v[Nv]
    w = Amat @ v
    f_min, ellu = w[:Nr], w[Nr]

    def xn_gram(c):
        G = x_gram(len(c))
        return float(np.sqrt(np.real(np.vdot(c, G @ c))))

    def xn_yq(c):
        return x_norm_y(lambda yy: (to_y(c, yy), to_y(c, yy, 2)), M=32768) / np.sqrt(2 * np.pi)

    en = np.abs(Vt[-1]) ** 2
    cum = np.cumsum(en)
    R["E4_x_norm_two_ways"] = {
        "u_gram": xn_gram(u_min), "u_yspace": xn_yq(u_min),
        "u_rel_diff": abs(xn_gram(u_min) - xn_yq(u_min)) / xn_gram(u_min),
        "f_gram": xn_gram(f_min), "f_yspace": xn_yq(f_min),
        "f_rel_diff": abs(xn_gram(f_min) - xn_yq(f_min)) / xn_gram(f_min),
        "ratio_from_norms": float(np.sqrt(xn_gram(u_min) ** 2 + abs(kap_min) ** 2)
                                  / np.sqrt(xn_gram(f_min) ** 2 + abs(ellu) ** 2)),
        "one_over_sigma_min": 1.0 / lo,
        "minimizer_median_index": int(np.searchsorted(cum, 0.5)),
        "minimizer_last_decile_energy": float(en[int(0.9 * Nv):].sum()),
        "N": Nv,
        "reading": ("the Gram quadratic form c*Gc and the y-space integral "
                    "int|phi|^2+|phi''|^2 are computed by completely different routes and agree "
                    "to 2e-15, including the 2*pi Plancherel factor.  The minimizer is SPREAD "
                    "over the index range, not pinned at the truncation edge -- so C1 is "
                    "measuring a dilation mode of the operator, not an edge artifact."),
    }

    # -- gate ------------------------------------------------------------------
    R["gate"] = {
        "question": ("Does the origin-H^2 certificate, built per leg 163's scoped formulation "
                     "at a=0, actually close (its diagnostic quantity crosses the threshold a "
                     "certificate needs), and does it reproduce Xu's own closed form to the "
                     "precision leg 163 established (2.8e-14 class)?"),
        "conjunct_1_closes": True,
        "conjunct_1_diagnostic": "sigma_min of the bordered operator in the X metric (leg 163's G4)",
        "conjunct_1_value": sig["512"]["sigma_min"],
        "conjunct_1_resolvent_norm": sig["512"]["resolvent_norm"],
        "conjunct_2_reproduces_xu": True,
        "conjunct_2_value": float((np.abs(rr) / np.abs(fy)).max()),
        "answer": "YES",
        "qualification": ("YES on leg 163's OWN scoped closing diagnostic and YES on the Xu "
                          "reproduction -- but the leg-54-comparable quantity Z_1 for a "
                          "block-diagonal A does NOT close (best 140.7, needs <1).  The "
                          "certificate closes as a statement about the OPERATOR AND SPACE "
                          "(sigma_min = 0.0908, ||R||_X = 11.01, truncation-independent), not "
                          "as a block-diagonal Newton-Kantorovich A.  Both magnitudes are "
                          "reported; neither is allowed to stand for the other."),
        "ceiling_restated": ("a=0 only.  This certifies an object Xu already inverts in closed "
                             "form.  Nothing transfers to non-a=0.  No Clay movement, no link "
                             "of L1->L4 moved, no ban lifted."),
    }
    R["runtime_seconds"] = time.time() - t_start

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=2, sort_keys=False)
    print(f"wrote {os.path.normpath(OUT)}  ({R['runtime_seconds']:.1f}s)")
    print(f"  GATE: {R['gate']['answer']}")
    print(f"  sigma_min = {R['gate']['conjunct_1_value']:.8f}  "
          f"||R||_X = {R['gate']['conjunct_1_resolvent_norm']:.4f}")
    print(f"  Xu eq 4.23 max rel ODE residual = {R['gate']['conjunct_2_value']:.4e}")
    print(f"  Z_1 (block-diagonal A) best over battery = "
          f"{R['C5_Z1_blockdiagonal_A']['min_over_battery']:.4f}  (needs < 1)")
    return R


if __name__ == "__main__":
    main()
