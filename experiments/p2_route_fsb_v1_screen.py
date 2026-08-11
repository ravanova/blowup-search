#!/usr/bin/env python3
"""Leg 301 — ROUTE-FSB: the fourth space/basis screen.

THIS SCRIPT BUILDS NOTHING AND CERTIFIES NOTHING.  It imports no `solver/` module.
It assembles no certificate, computes no `Z_0`, `Y_0` or `Z_2`, and does not lift
or argue any ban.  What it does is:

  1. hold the enumerated candidate table for a FOURTH space/basis, each row carrying
     its realization name (lesson 91) and its provenance;
  2. COMPUTE, rather than assert, the three structural scalars the screen turns on
     -- `lmin` (minimum modulus of the unbounded part's diagonal), the growth
     exponent of that diagonal, and the row dominance ratio `delta` -- for every
     candidate whose matrix has a closed form in the literature or in this
     repository's own banked record;
  3. evaluate the three measured death mechanisms as PREDICATES over those fields;
  4. run two controls that report the other answer, and one instrument check
     against a banked number from leg 158.

Run:  python3 experiments/p2_route_fsb_v1_screen.py
Emits: writeup/data/p2_route_fsb_v1_screen.json
"""

from __future__ import annotations

import json
import math
import os
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_fsb_v1_screen.json")

PASS, FAIL, UNRESOLVED, NA = "PASS", "FAIL", "UNRESOLVED", "N/A"


# --------------------------------------------------------------------------
# 1.  The three closed-form matrices the screen actually computes on.
#     None of these is a certificate; each is the UNBOUNDED PART's matrix,
#     read out of a published equation or out of this repository's own
#     banked closed form, and used only for its diagonal/off-diagonal shape.
# --------------------------------------------------------------------------

def mt_differentiation_matrix(n: int) -> Dict[str, complex]:
    """Malmquist-Takenaka differentiation matrix, Iserles & Webb DAMTP NA2019/03 eq. (3.3).

    Read off the displayed matrix, indices n in Z:
        D[n, n]   = i(2n+1)        (diagonal:  ..., -5i, -3i, -i, i, 3i, 5i, ...)
        D[n, n+1] = n+1            (super-diagonal)
        D[n, n-1] = -n             (sub-diagonal)
    """
    return {"sub": complex(-n, 0), "diag": complex(0, 2 * n + 1), "sup": complex(n + 1, 0)}


def incumbent_tail_matrix(k: int) -> Dict[str, complex]:
    """This repository's tail operator, banked closed form (leg 158, verified entrywise
    against `solver/spectral_certificate.tail_block` to max abs discrepancy 0.0 over 58
    modes).  Reproduced here as ARITHMETIC ON THREE PUBLISHED SCALARS, not by importing
    or re-deriving the module -- realization 1's matrix is the negative control.

        lambda_k = 1 - (k-1)/2     (sub-diagonal)
        mu_k     = 0               (diagonal -- identically zero)
        beta_k   = (k+1)/2         (super-diagonal)
    """
    return {"sub": complex(1.0 - (k - 1) / 2.0, 0), "diag": 0j, "sup": complex((k + 1) / 2.0, 0)}


def bdl_admissible_matrix(k: int) -> Dict[str, complex]:
    """Leg 158's synthetic BDL-admissible positive control: mu_k = k, lambda_k = beta_k = 0.2k.
    Every predicate below must report the OTHER answer on this row (lesson 90)."""
    return {"sub": complex(0.2 * k, 0), "diag": complex(float(k), 0), "sup": complex(0.2 * k, 0)}


def scan(matrix_fn, lo: int, hi: int) -> Dict[str, object]:
    """Compute lmin, the diagonal growth exponent, and the dominance ratio delta."""
    diags, deltas = [], []
    for n in range(lo, hi + 1):
        e = matrix_fn(n)
        d = abs(e["diag"])
        offrow = abs(e["sub"]) + abs(e["sup"])
        diags.append((n, d))
        deltas.append((n, math.inf if d == 0.0 else offrow / d))
    finite = [d for _, d in diags]
    lmin = min(finite)
    # growth exponent of |diag| fitted on POSITIVE indices only (for a two-sided index
    # range the symmetric endpoints have equal |n| and the fit is degenerate)
    big = [(n, d) for n, d in diags if d > 0 and n >= max(4, hi // 8)]
    if len(big) >= 2:
        (n1, d1), (n2, d2) = big[0], big[-1]
        exponent = (math.log(d2) - math.log(d1)) / (math.log(abs(n2)) - math.log(abs(n1)))
    else:
        exponent = float("nan")
    finite_deltas = [d for _, d in deltas if math.isfinite(d)]
    return {
        "lmin": lmin,
        "diag_growth_exponent": round(exponent, 6),
        "delta_sup": (math.inf if len(finite_deltas) < len(deltas) else max(finite_deltas)),
        "delta_limit": deltas[-1][1],
        "delta_is_infinite_somewhere": any(not math.isfinite(d) for _, d in deltas),
        "index_range": [lo, hi],
    }


def is_skew_hermitian(matrix_fn, lo: int, hi: int) -> bool:
    """A real self-test: D[n,n+1] must equal -conj(D[n+1,n]) and the diagonal must be
    purely imaginary.  If eq. (3.3) were mis-transcribed this returns False."""
    for n in range(lo, hi):
        a, b = matrix_fn(n), matrix_fn(n + 1)
        if abs(a["sup"] + b["sub"].conjugate()) > 1e-12:
            return False
        if abs(a["diag"].real) > 1e-12:
            return False
    return True


def odd_even_recast_delta(kmax: int) -> Dict[str, float]:
    """Leg 158's compensation, recomputed: pair modes (k, k+1); with mu == 0 the 2x2 block
    diagonal is anti-diagonal, det = -beta_k * lambda_{k+1}, and the two block dominance
    ratios collapse to |lambda_k/beta_k| and |beta_{k+1}/lambda_{k+1}| -- the zero diagonal
    no longer appears.  Instrument check against leg 158's banked delta -> 1.0039."""
    ratios = []
    for k in range(2, kmax, 2):
        lam_k = 1.0 - (k - 1) / 2.0
        beta_k = (k + 1) / 2.0
        lam_k1 = 1.0 - k / 2.0
        beta_k1 = (k + 2) / 2.0
        if beta_k != 0 and lam_k1 != 0:
            ratios.append(max(abs(lam_k / beta_k), abs(beta_k1 / lam_k1)))
    return {"delta_sup": max(ratios), "delta_limit": ratios[-1], "pairs": len(ratios)}


# --------------------------------------------------------------------------
# 2.  The three measured death mechanisms, as predicates.
# --------------------------------------------------------------------------

MECHANISMS = {
    "M1_zero_diagonal_shift": {
        "measured_by": "leg 54 (MM), sharpened by leg 62 (CP) clauses A1_LMIN / A1_GROWTH",
        "realization_it_holds_in": "weighted ell^1 of Fourier coefficients, compactified odd-sine basis",
        "statement": (
            "The unbounded part is a SHIFT, not a multiplier: diagonal exactly 0.0, growth "
            "entirely off-diagonal ~k/2.  Cadiot Assumption 1 needs |l| >= lmin > 0 AND "
            "|l| -> infinity; both fail, the first infinitely.  Best admissible Z_1 = 8.9591 "
            "against the 10.4584 block-diagonal baseline, a 1.167x improvement where >8x was "
            "needed; the required Gershgorin shift |s| grows LINEARLY in the truncation "
            "(63 -> 1023 over M = 128..2048, exponent +1.0051) instead of saturating."
        ),
        "predicate": "PASS iff lmin > 0 and the diagonal growth exponent is > 0",
    },
    "M2_HD_consistency": {
        "measured_by": "leg 56 (TN)",
        "realization_it_holds_in": "collocation / weighted sup norm on a graded line grid",
        "statement": (
            "The stored discrete H (line_hilbert_matrix) and D (natural-cubic-spline slope) "
            "are different discretisations -- H transforms an endpoint-zeroed interpolant -- so "
            "the (H,D) consistency defect does not converge: at n = 801 the derivative defect "
            "is 1.854e+07 tau at order 4.01 and the Hilbert defect is 2.040e+11 tau at order "
            "0.00, against tau = 2.306e-14."
        ),
        "predicate": "PASS iff H and D act EXACTLY on the basis in closed form (no interpolant)",
    },
    "M3_a0_exactness_nontransfer": {
        "measured_by": "legs 163 (O3) / 176 / 182, and leg 260 for the Gaussian-weight family",
        "realization_it_holds_in": "origin-H^2 on the line (Xu), Hardy blocks in the Laguerre basis",
        "statement": (
            "Every usable object is a consequence of Omega being the EXACT a=0 CLM profile, via "
            "the identity H(Omega) - i*Omega = i/(y + i/2) -- an equation satisfied by the "
            "PROFILE, containing no norm, no weight and no index.  HL_S2_nonsymmetric is not a "
            "CLM profile and inherits none of it.  Sibling case: the Gaussian-weighted family, "
            "where the Leray projector leaves L^2(mu) with fitted tail exponent -3.000000 and "
            "the weight/decay mismatch runs 26.6 -> 1.0e5 -> 3.9e20 -> 1.3e83 over shells."
        ),
        "predicate": "PASS iff the basis's usable structure is independent of the profile",
    },
}


def screen(c: Dict) -> Dict[str, str]:
    """Evaluate the three mechanisms as predicates over the candidate's own fields."""
    v = {}

    lmin, expo = c.get("lmin"), c.get("diag_growth_exponent")
    if lmin is None or expo is None:
        v["M1_zero_diagonal_shift"] = UNRESOLVED
    elif lmin > 0.0 and expo > 0.0:
        v["M1_zero_diagonal_shift"] = PASS
    else:
        v["M1_zero_diagonal_shift"] = FAIL

    ex = c.get("operators_exact_on_basis")
    v["M2_HD_consistency"] = UNRESOLVED if ex is None else (PASS if ex else FAIL)

    pd = c.get("profile_dependence")
    if pd is None:
        v["M3_a0_exactness_nontransfer"] = UNRESOLVED
    elif pd == "none":
        v["M3_a0_exactness_nontransfer"] = PASS
    elif pd == "different_object":
        v["M3_a0_exactness_nontransfer"] = UNRESOLVED
    else:
        v["M3_a0_exactness_nontransfer"] = FAIL

    return v


# --------------------------------------------------------------------------
# 3.  The candidate table.
# --------------------------------------------------------------------------

def build_candidates() -> List[Dict]:
    mt = scan(mt_differentiation_matrix, -64, 64)
    inc = scan(incumbent_tail_matrix, 2, 128)

    return [
        {
            "id": "l1_fourier_compactified",
            "name": "weighted ell^1 of Fourier coefficients, compactified odd-sine basis",
            "status_here": "REALIZATION 1 -- BUILT AND DEAD",
            "where": "solver/spectral_certificate.py; legs 51-55, 127; Route-D v3",
            "unbounded_part_shape": "SHIFT",
            "lmin": inc["lmin"],
            "diag_growth_exponent": inc["diag_growth_exponent"],
            "delta_sup": "inf",
            "operators_exact_on_basis": True,
            "profile_dependence": "none",
            "note": (
                "Target margin is finite here (leg 55: +0.394 at s=0, +0.094 at s=0.3), so M3 "
                "passes; the basis dies on M1 alone.  Route-D v3 additionally proves no pair of "
                "diagonally weighted ell^1 spaces can work: min exponent sum 0.98 over the "
                "whole (s,t) family."
            ),
        },
        {
            "id": "collocation_sup_line",
            "name": "collocation / weighted sup norm on a graded line grid",
            "status_here": "REALIZATION 2 -- BUILT AND DEAD",
            "where": "solver/interval_certificate.py, solver/line_hilbert.py; legs 46/50/56",
            "unbounded_part_shape": "N/A (grid, not a coefficient basis)",
            "operators_exact_on_basis": False,
            "profile_dependence": "none",
            "note": "H defect 2.040e+11 tau at order 0.00; D defect 1.854e+07 tau at order 4.01.",
        },
        {
            "id": "origin_h2_laguerre",
            "name": "origin-H^2 on the line (Xu): Hardy blocks H+ (+) H-, Laguerre basis",
            "status_here": "REALIZATION 3 -- BUILT AND DEAD (no transfer)",
            "where": "solver/origin_h2_certificate.py; legs 163/176/182",
            "unbounded_part_shape": "tridiagonal (exactly, rational entries)",
            "operators_exact_on_basis": True,
            "profile_dependence": "a0_exact",
            "note": (
                "sigma_min = 0.0908 truncation-independent, tail inverse 4.026 CONVERGES where "
                "ell^1_w diverged -- the space is real.  It dies on M3: capped at a=0 exactness "
                "(leg 163 O3, FATAL for transfer).  Best Z_1 in leg 54's shape 140.72, ~K^2."
            ),
        },
        {
            "id": "weighted_energy_L2",
            "name": "weighted-energy L^2 (Chen-Hou-shaped) coercivity",
            "status_here": "TRIED -- gate NO",
            "where": "solver/energy_coercivity.py; legs 111/141/178",
            "unbounded_part_shape": "N/A (energy estimate, not an approximate inverse)",
            "operators_exact_on_basis": True,
            "profile_dependence": "a0_exact",
            "note": (
                "Every admissible weight has a NEGATIVE gap -> -(3-gamma)/2; zero-width window "
                "(damping at origin needs gamma>3, basis in L^2_phi only for gamma<3).  Leg 178 "
                "found the zero width is a property of the p=1 odd-sine TRIAL SPACE, escalated."
            ),
        },
        {
            "id": "weighted_holder_routeD",
            "name": "weighted-Holder spaces, two gradings, conformal theta variable",
            "status_here": "TRIED -- no consistent pair",
            "where": "solver/holder_norms.py, solver/nk_bounds.py; Route-D v3-v16",
            "unbounded_part_shape": "SHIFT",
            "lmin": 0.0,
            "diag_growth_exponent": 0.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "none",
            "note": (
                "Route-D v3's conservation law: ||A_N|| ~ N^(1-g) and S_K ~ K^g, the sum is >= 1 "
                "at every gap g and exactly 1 on 0 <= g <= 1; measured minimum 0.98.  Its own "
                "diagnosis -- 'a diagonal weight on Fourier coefficients measures SMOOTHNESS, "
                "not DECAY' -- is the selection criterion this screen inherits."
            ),
        },
        {
            "id": "breden_chu_gaussian_H2mu",
            "name": "Breden-Chu Gaussian-weighted Sobolev H^2(mu), half-Hermite/Laguerre eigenbasis",
            "status_here": "TRIED -- ruled out for the NS target, twice",
            "where": "solver/bc_weighted_sobolev.py; legs 245/255/257, ruled out by leg 260",
            "unbounded_part_shape": "MULTIPLIER (OU operator diagonal in its own eigenbasis)",
            "lmin": 1.0,
            "diag_growth_exponent": 1.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "gaussian_weight_incompatible",
            "note": (
                "Reproduces arXiv:2404.04054 Thm 42 end-to-end.  Killed on transfer, not on "
                "shape: the Leray projector leaves L^2(mu) (algebraic |x|^-4 tail, fitted "
                "exponent -3.000000) and mu ~ exp(|y|^2/4) against a Type-I DSS profile's "
                "algebraic decay -- shells 26.6 -> 1.0e5 -> 3.9e20 -> 1.3e83."
            ),
        },
        {
            "id": "hermite_ou_eigenbasis",
            "name": "Gaussian-weighted L^2_mu / Ornstein-Uhlenbeck eigenbasis (Pineau-Vicol window)",
            "status_here": "NAMED BY LEG 262, NEVER SCREENED -- this screen kills it",
            "where": "named in experiments/journal/leg_262.md; never built",
            "unbounded_part_shape": "MULTIPLIER (OU exactly diagonal, |diag| bounded below by 1)",
            "lmin": 1.0,
            "diag_growth_exponent": 1.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "gaussian_weight_incompatible",
            "note": (
                "Leg 262's M1 argument is correct and survives this screen intact.  But it is "
                "the SAME Gaussian-weight family as breden_chu_gaussian_H2mu, so leg 260's "
                "already-banked measurement transfers verbatim and kills it on M3.  This is the "
                "enumeration doing work no single-candidate leg could: the kill was already in "
                "the repository, two legs away from the proposal."
            ),
        },
        {
            "id": "chebyshev_naive_pairing",
            "name": "global Chebyshev, naive pairing (1-v^2)T_n -> T_m",
            "status_here": "MEASURED, leg 162 realization A -- SHIFT",
            "where": "leg 162 (parked on origin/leg/162-capg-v1); TECHNICAL_P2_PUB1_V1.md 5.2",
            "unbounded_part_shape": "SHIFT",
            "lmin": 0.0,
            "diag_growth_exponent": 0.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "none",
            "note": (
                "The control INSIDE the fourth-space question: same polynomial family as the "
                "row below, bidiagonal, exactly zero diagonal, off-diagonal ~n/2.  It is the "
                "PAIRING that decides the shape, not the family."
            ),
        },
        {
            "id": "chebyshev_airfoil_ultraspherical",
            "name": "global Chebyshev, Olver-Townsend airfoil pairing sqrt(1-v^2)U_{n-1} -> T_m/sqrt(1-v^2)",
            "status_here": "MEASURED AND PARKED -- Z_1 < 1 ACHIEVED, on a different object",
            "where": "leg 162, parked on origin/leg/162-capg-v1, never merged",
            "unbounded_part_shape": "MULTIPLIER (exact diag(-n))",
            "lmin": 1.0,
            "diag_growth_exponent": 1.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "different_object",
            "external_machinery": "arXiv:1507.00596 (Slevinsky-Olver, singular integral equations)",
            "note": (
                "The only place in this repository where Z_1 < 1 has ever been measured: "
                "block_diag 0.2737 / gs_upper 0.0874 at a=0.8, 0.7370 / 0.2287 at a=0.5, moving "
                "0.19% over 8x refinement, target in its own space with margin -0.73.  M3 is "
                "UNRESOLVED, not passed: the object is the a in (0,1) two-scale profile on its "
                "own compact support, NOT the a=0 CLM linearisation and NOT HL_S2_nonsymmetric."
            ),
        },
        {
            "id": "malmquist_takenaka",
            "name": "Malmquist-Takenaka / Christov rational Hardy basis on the line",
            "status_here": "UNTRIED HERE, AND UNUSED IN RIGOROUS NUMERICS ANYWHERE",
            "where": "no file in this repository; grep for malmquist|takenaka|christov returns 0",
            "unbounded_part_shape": "MULTIPLIER (diagonal i(2n+1)) with tridiagonal correction",
            "lmin": mt["lmin"],
            "diag_growth_exponent": mt["diag_growth_exponent"],
            "delta_sup": mt["delta_sup"],
            "delta_limit": mt["delta_limit"],
            "operators_exact_on_basis": True,
            "profile_dependence": "none",
            "external_machinery": (
                "basis+differentiation matrix: Iserles-Webb DAMTP NA2019/03 eq. (3.3); "
                "nearest transferable validated machinery: arXiv:2411.18361 (validated "
                "orthogonal-polynomial transforms), arXiv:2302.12877 (CAP on unbounded domains)"
            ),
            "note": (
                "phi_n(x) = i^n sqrt(2/pi) (1+2ix)^n / (1-2ix)^(n+1), n in Z; complete "
                "orthonormal in L^2(R); n >= 0 spans the Hardy space H^2 of the upper half "
                "plane and n <= -1 its conjugate, so the HILBERT TRANSFORM IS EXACTLY DIAGONAL, "
                "multiplication by -+i, modulus 1.  All phi_n share the uniform bound "
                "|phi_n(x)| = sqrt(2/pi)/sqrt(1+4x^2): the basis carries algebraic decay in its "
                "own functions rather than in a weight, which is the exact repair for Route-D "
                "v3's diagnosed category error."
            ),
        },
        {
            "id": "wavelet_multiresolution",
            "name": "wavelet / multiresolution basis",
            "status_here": "UNTRIED -- and no machinery exists to try it with",
            "where": "no file in this repository; grep for wavelet returns 0",
            "unbounded_part_shape": "almost-diagonal (Calderon-Zygmund), not diagonal",
            "operators_exact_on_basis": False,
            "profile_dependence": "none",
            "note": (
                "The external search found NO interval-arithmetic CAP in a wavelet basis "
                "anywhere: wavelet work supplies a-posteriori error control, not validated "
                "existence.  H is almost-diagonal but not diagonal, and for symmetric wavelets "
                "the diagonal vanishes by parity -- M1's mechanism recurs for the same reason."
            ),
        },
        {
            "id": "fourier_gevrey",
            "name": "Fourier-Gevrey / geometrically weighted Hilbert scale (nu^k)",
            "status_here": "NOT A FOURTH BASIS -- realization 1 with a different weight",
            "where": "the geometric weight class of solver/spectral_certificate.py",
            "unbounded_part_shape": "SHIFT",
            "lmin": 0.0,
            "diag_growth_exponent": 0.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "none",
            "note": (
                "The MATRIX is realization 1's; only the norm changes.  A zero diagonal is a "
                "property of the matrix, not of the norm, so M1 recurs verbatim, and Route-D "
                "v3's no-go covers every diagonal weight.  The geometric class was already "
                "measured: the tail diverges by a factor nu per mode."
            ),
        },
        {
            "id": "ellp_besov_sobolev_interpolants",
            "name": "ell^p_w / Fourier-Lebesgue FL^p_s / Besov / weighted H^s on the circle",
            "status_here": "RULED OUT ON PAPER by leg 182",
            "where": "experiments/journal/leg_182.md",
            "unbounded_part_shape": "SHIFT",
            "lmin": 0.0,
            "diag_growth_exponent": 0.0,
            "operators_exact_on_basis": True,
            "profile_dependence": "none",
            "note": (
                "The whole scale collapses to sigma = s + 1/p: kernel in the space iff sigma<2, "
                "cokernel bounded iff sigma>2, so the admissible window is the single point "
                "sigma=2, where the target's margin is -0.602647 exponent units AT EVERY p.  "
                "Leg 127's mechanism is p-blind (single-row share 0.9999999999998843)."
            ),
        },
        {
            "id": "nakao_plum_fem_eigenvalue",
            "name": "Nakao-Plum FEM projection / explicit eigenvalue bounds",
            "status_here": "NOT A BASIS -- A DIFFERENT TECHNOLOGY, and outside the ban's naming",
            "where": "no file in this repository",
            "unbounded_part_shape": "N/A -- no approximate inverse is built",
            "operators_exact_on_basis": None,
            "profile_dependence": "none",
            "external_machinery": "Nakao, Plum & Watanabe, Springer SSCM 53 (2019)",
            "note": (
                "Plum's half replaces the approximate-inverse bound entirely with explicit "
                "eigenvalue bounds for the linearisation, so M1 has no referent rather than "
                "passing -- lesson 73: when a quantity has no referent, say so instead of "
                "bounding it.  Recorded because the ban names 'ell^1-Fourier/radii-polynomial "
                "machinery', and this is neither; it is NOT proposed as the fourth space, "
                "because a fourth SPACE is what the lift condition asks for."
            ),
        },
    ]


# --------------------------------------------------------------------------
# 4.  Controls (lesson 90: each must be able to report the other answer).
# --------------------------------------------------------------------------

def controls() -> Dict[str, object]:
    inc = scan(incumbent_tail_matrix, 2, 128)
    pos = scan(bdl_admissible_matrix, 2, 128)
    mt = scan(mt_differentiation_matrix, -64, 64)
    recast = odd_even_recast_delta(2048)

    out = {
        "negative_control_incumbent_tail": {
            "what": "this repository's own tail operator, banked closed form",
            "purpose": "the screen must FAIL M1 on the realization that is measured dead",
            "lmin": inc["lmin"],
            "delta_is_infinite_somewhere": inc["delta_is_infinite_somewhere"],
            "m1_verdict": screen({"lmin": inc["lmin"],
                                  "diag_growth_exponent": inc["diag_growth_exponent"]})[
                "M1_zero_diagonal_shift"],
            "reports_other_answer_than_mt": True,
        },
        "positive_control_bdl_admissible": {
            "what": "leg 158's synthetic BDL-admissible operator mu_k=k, lambda_k=beta_k=0.2k",
            "purpose": "the screen must PASS M1, and delta must land below BDL's 1/2",
            "lmin": pos["lmin"],
            "diag_growth_exponent": pos["diag_growth_exponent"],
            "delta_sup": pos["delta_sup"],
            "bdl_admissible": pos["delta_sup"] < 0.5,
            "m1_verdict": screen({"lmin": pos["lmin"],
                                  "diag_growth_exponent": pos["diag_growth_exponent"]})[
                "M1_zero_diagonal_shift"],
        },
        "instrument_check_leg158_recast": {
            "what": "leg 158's odd-even 2x2 recast of the incumbent, recomputed here",
            "banked_by_leg_158": {"delta_sup": 1.667, "delta_limit_as_k_to_inf": 1.0039,
                                  "C1_after_recast": 0.375, "C1_before_recast": 0.0},
            "recomputed_delta_sup": recast["delta_sup"],
            "recomputed_delta_limit": recast["delta_limit"],
            "agrees_with_banked_limit_to_1pct": abs(recast["delta_limit"] - 1.0039) < 0.011,
            "limit_relative_discrepancy": abs(recast["delta_limit"] - 1.0039) / 1.0039,
            "sup_disagrees_and_why": (
                "The k -> infinity LIMIT reproduces leg 158's banked 1.0039 to 0.19%, which is "
                "the part of the instrument check that has content: it is the same wall. The "
                "SUP does not (3.0 recomputed against 1.667 banked) and is not tuned to agree. "
                "The quantities differ by definition: leg 158's delta is a 2x2 BLOCK quantity "
                "(||D_j^-1|| times the off-block mass), this recomputation is the elementwise "
                "ratio max(|lambda_k/beta_k|, |beta_{k+1}/lambda_{k+1}|).  They must agree "
                "asymptotically, where the blocks decouple, and need not agree at the first few "
                "modes, where the border row and the pairing offset both matter.  Named, not "
                "reconciled: nothing in this screen's gate depends on the sup."
            ),
        },
        "self_test_mt_skew_hermitian": {
            "what": "eq. (3.3) transcription check: D must be skew-Hermitian",
            "purpose": "a mis-read of the displayed matrix returns False here",
            "passes": is_skew_hermitian(mt_differentiation_matrix, -64, 63),
        },
        "mt_delta_exactly_one": {
            "what": "the MT dominance ratio, computed not asserted",
            "delta_sup": mt["delta_sup"],
            "delta_limit": mt["delta_limit"],
            "diag_growth_exponent_fitted": mt["diag_growth_exponent"],
            "diag_growth_exponent_closed_form": 1.0,
            "growth_fit_note": (
                "The fitted 0.974588 is a finite-range secant on |2n+1| between n=8 and n=64; "
                "the closed form is exactly linear, so the exponent is +1 and the shortfall is "
                "the additive 1 in 2n+1, not slower growth."
            ),
            "note": (
                "delta = (|n| + |n+1|)/|2n+1| = 1 EXACTLY at every n in Z.  BDL assumption (5) "
                "needs delta < 1/2, so MT lands on the same wall leg 158's recast reached "
                "(1.0039).  This is NOT scored as a death: leg 62's test 14 REFUTED delta as "
                "the coordinate -- mu=0.25 gives delta=2, four times outside BDL, and is "
                "boundedly invertible with K-exponent -0.849.  'The hinge is zero-versus-"
                "nonzero diagonal, and delta is not the coordinate for it.'"
            ),
        },
    }
    return out


# --------------------------------------------------------------------------
# 5.  Gate.
# --------------------------------------------------------------------------

GATE_QUESTION = (
    "Does the screen produce at least one NAMED fourth space/basis with an explicit "
    "structural argument (not a hope) that each of the three death mechanisms cannot "
    "recur in it?"
)


def main() -> int:
    cands = build_candidates()
    for c in cands:
        c["screen"] = screen(c)
        c["passes_all_three"] = all(v == PASS for v in c["screen"].values())

    survivors = [c["id"] for c in cands if c["passes_all_three"]]
    near = [c["id"] for c in cands
            if not c["passes_all_three"]
            and UNRESOLVED in c["screen"].values()
            and FAIL not in c["screen"].values()]

    answer = "YES" if survivors else "NO"

    payload = {
        "leg": 301,
        "route": "ROUTE-FSB",
        "title": "the fourth space/basis screen",
        "date": "2026-08-11",
        "builds_anything": False,
        "lifts_any_ban": False,
        "ban_under_screen": (
            "re-posed 2026-08-06: re-attempting the ell^1-Fourier/radii-polynomial machinery "
            "this repository has measured DEAD in three realizations, on ANY model -- lifted by "
            "never, unless a namable FOURTH space/basis this repository has not yet tried is "
            "proposed, with its own scoping leg establishing it is not subject to the same "
            "three-realization death"
        ),
        "gate_question": GATE_QUESTION,
        "gate_answer": answer,
        "survivors": survivors,
        "unresolved_on_one_mechanism_only": near,
        "n_candidates": len(cands),
        "n_untried_here": sum(1 for c in cands if "UNTRIED" in c["status_here"]),
        "mechanisms": MECHANISMS,
        "candidates": cands,
        "controls": controls(),
        "clay": {
            "odds": "~0.05%",
            "chain_link_moved": False,
            "note": (
                "L1 is the only movable link and it has NOT moved: this leg proposes a space, "
                "it does not certify anything in one.  Ranking this leg high by chain proximity "
                "is a choice of what to try, never a claim about what happened."
            ),
        },
    }

    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2, default=str)

    print(f"ROUTE-FSB screen: {len(cands)} candidates, "
          f"{payload['n_untried_here']} untried here")
    for c in cands:
        marks = " ".join(f"{k.split('_')[0]}={v}" for k, v in c["screen"].items())
        print(f"  {'PASS' if c['passes_all_three'] else '    '}  {c['id']:38s} {marks}")
    print(f"GATE: {answer}   survivors={survivors}   unresolved-on-one={near}")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
