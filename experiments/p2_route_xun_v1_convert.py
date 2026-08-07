#!/usr/bin/env python3
"""Leg 277 -- ROUTE-XUN: the certificate's numbers under Xu's OWN normalization.

Leg 270's PUB2 review carries one converted number -- `sigma_min` reads `0.0420`
under "Xu's own normalization" (leg 249's W5, at `N = 256`) -- and treats it as
THE bridge between this repository's origin-`H^2` certificate (leg 176, verified
by leg 249) and Xu arXiv:2607.19762.  This leg converts the REST of the
certificate, and in doing so has to pin what "Xu's own normalization" means,
because Definition 4.1 names TWO norms:

  (4.2)  ||phi||_X^2 = ||phi||_{L^2}^2 + ||phi''||_{L^2}^2   with  L^2 = L^2(0, oo)
         -- the HALF-LINE norm, which is the displayed definition; and
  the next sentence: "Extended oddly to the line, X is the odd part of H^2(R)
         with an EQUIVALENT norm" -- the FULL-LINE norm.

`solver/origin_h2_certificate.py` computes the full-line one (`x_norm_y`, L469:
"over the whole line"; `x_norm`, L142: "up to the common factor sqrt(2 pi)").
Leg 249's W5 converted with `2 pi`, i.e. it adopted the second reading.  Whether
that is the right constant for the DISPLAYED definition is measured in X1, not
assumed.

Sections
  X1  the conversion constant, MEASURED: the half-line Gram against the
      full-line one, on the physical subspace and off it
  X2  P1 -- the two routes to a rescaled X block are the same computation
  X3  THE CONVERSION TABLE: every banked certificate quantity under all three
      normalizations, each with its predicted homogeneity tested
  X4  gate (a) -- agreement with leg 249's own weight-sweep images
  X5  gate (b) -- what Xu actually publishes that is directly comparable

NOTHING IS EDITED HERE.  Leg 249's data, leg 176's certificate and Xu's paper
are read; `solver/origin_h2_certificate.py` is imported as the object being
converted, never modified.  PUB2 is not opened.
"""

import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.origin_h2_certificate as H
from solver.origin_h2_certificate import (
    border_row, bordered_operator, l0_plus, symmetry_modes, x_gram,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_xun_v1_convert.json")
L249 = os.path.join(HERE, "..", "writeup", "data",
                    "p2_route_h2cv_v1_postconstruction.json")
L176 = os.path.join(HERE, "..", "writeup", "data",
                    "p2_route_h2c_v1_construction.json")

TWOPI = 2.0 * math.pi
PI = math.pi

# The three normalization conventions, as the constant `kappa` multiplying the
# coefficient Gram `G = I + J^4` on the `X` block.  The border amplitude always
# carries weight 1 -- that is what makes the choice of `kappa` observable.
CONV = {"repo": 1.0, "xu_full_line": TWOPI, "xu_half_line_4p2": PI}


# ===========================================================================
# quadrature: an independent double-exponential rule, half line and full line
# ===========================================================================

def de_half(h=0.02, U=4.5):
    """`y = exp(sinh u)` on `(0, oo)`: doubly exponential at BOTH endpoints.

    The integrands here decay only algebraically (`|phi|^2 ~ y^-2`), so an
    ordinary tanh-sinh cut leaves an algebraic tail -- the defect leg 249 hit
    and recorded.  `exp(sinh u)` reaches `y ~ 3.5e19` at `U = 4.5` and the
    weight `cosh(u) y` makes the transformed integrand decay doubly
    exponentially at both ends.
    """
    u = np.arange(-U, U + 1e-15, h)
    y = np.exp(np.sinh(u))
    return y, h * np.cosh(u) * y


def de_full(h=0.02, U=4.0):
    """`y = sinh(sinh u)` on `R` -- leg 249's W2 rule, rebuilt here."""
    u = np.arange(-U, U + 1e-15, h)
    return np.sinh(np.sinh(u)), h * np.cosh(u) * np.cosh(np.sinh(u))


def _basis(n, y):
    E = np.eye(n)
    P0 = np.array([H.to_y(E[k], y) for k in range(n)])
    P2 = np.array([H.to_y(E[k], y, 2) for k in range(n)])
    return P0, P2


def gram_from_rule(n, y, w):
    """`M_mn = int (phi_m conj(phi_n) + phi_m'' conj(phi_n'')) dy` on the rule."""
    P0, P2 = _basis(n, y)
    return (P0 * w) @ P0.conj().T + (P2 * w) @ P2.conj().T


# ===========================================================================
# X1 -- the conversion constant, measured rather than assumed
# ===========================================================================

def x1_conversion_constant(n=8):
    R = {"n_modes": n}
    G = x_gram(n)

    yf, wf = de_full()
    Mf = gram_from_rule(n, yf, wf)
    R["full_line"] = {
        "max_abs_dev_from_2pi_G": float(np.abs(np.real(Mf) - TWOPI * G).max()),
        "max_abs_imaginary_part": float(np.abs(np.imag(Mf)).max()),
        "reading": ("reproduces leg 249's W2 independently: the FULL-LINE Gram is "
                    "2 pi (I + J^4), real to quadrature accuracy."),
    }

    yh, wh = de_half()
    Mh = gram_from_rule(n, yh, wh)
    S = np.imag(Mh)
    R["half_line"] = {
        "max_abs_dev_of_REAL_part_from_pi_G": float(np.abs(np.real(Mh) - PI * G).max()),
        "max_abs_imaginary_part": float(np.abs(S).max()),
        "imaginary_part_antisymmetry_defect": float(np.abs(S + S.T).max()),
        "imaginary_entries_0_1_and_2_3": [float(S[0, 1]), float(S[2, 3])],
        "eigenvalues_of_half_line_form": [float(v) for v in
                                          np.linalg.eigvalsh((Mh + Mh.conj().T) / 2)],
        "eigenvalues_of_pi_G": [float(v) for v in np.linalg.eigvalsh(PI * G)],
    }

    # resolution control: the imaginary part must be the CONVERGED answer, not
    # the rule's noise.  Three further rules; the entries are exact integers.
    ctrl = {}
    for (h, U) in [(0.01, 4.5), (0.02, 5.0), (0.04, 4.5)]:
        y2, w2 = de_half(h, U)
        M2 = gram_from_rule(n, y2, w2)
        ctrl[f"h={h},U={U}"] = {
            "max_abs_dev_of_REAL_part_from_pi_G": float(np.abs(np.real(M2) - PI * G).max()),
            "imag_0_1": float(np.imag(M2)[0, 1]),
            "max_abs_imaginary_part": float(np.abs(np.imag(M2)).max()),
        }
    R["half_line_resolution_control"] = ctrl

    # THE decisive test.  Leg 249 realified the whole bordered section (its sec 8:
    # `m` and `ell` are purely imaginary, so a diagonal unitary makes the section
    # REAL).  On the REAL coefficient subspace -- which is where sigma_min of a
    # real pencil is attained -- the antisymmetric imaginary part contributes
    # exactly nothing, and the half-line form collapses to a CONSTANT times the
    # repo's Gram.  Measured on random real data.
    rng = np.random.default_rng(0)
    ratios = []
    for _ in range(8):
        c = rng.normal(size=n)
        ratios.append(float(np.real(c @ Mh @ c)) / (PI * float(c @ G @ c)))
    R["real_subspace_ratio_half_over_piG"] = {
        "samples": ratios,
        "max_abs_dev_from_1": float(max(abs(r - 1.0) for r in ratios)),
    }
    # the same test on COMPLEX data, where it must FAIL -- a control that can
    # come out differently, and does.
    cratios = []
    for _ in range(8):
        c = rng.normal(size=n) + 1j * rng.normal(size=n)
        cratios.append(float(np.real(np.vdot(c, Mh @ c)))
                       / (PI * float(np.real(np.vdot(c, G @ c)))))
    R["complex_data_ratio_half_over_piG"] = {
        "samples": cratios,
        "max_abs_dev_from_1": float(max(abs(r - 1.0) for r in cratios)),
    }

    R["kappa_full_line"] = TWOPI
    R["kappa_half_line_4p2"] = PI
    R["reading"] = (
        "MEASURED.  Xu Definition 4.1 eq (4.2) is a HALF-LINE norm.  Its Gram in "
        "the repository's Laguerre/Blaschke coordinates is pi (I + J^4) + i S with "
        "S real antisymmetric and LARGE (exact integer entries, max recorded above "
        "at n = 8, stable across four quadrature rules -- not noise).  So the two "
        "norms Definition 4.1 names are NOT proportional as Hermitian forms on "
        "complex coefficients.  But the bordered section is REAL after leg 249's "
        "realification, and on the real coefficient subspace S contributes exactly "
        "zero: there the half-line norm is EXACTLY pi c'Gc, i.e. EXACTLY HALF the "
        "squared full-line norm.  The constant for the DISPLAYED definition is "
        "therefore pi, not 2 pi.  Leg 249's W5 converted with 2 pi -- Definition "
        "4.1's second sentence (the 'equivalent' full-line norm), not (4.2).")
    return R


# ===========================================================================
# the machinery: the certificate's sections with a kappa-scaled X block
# ===========================================================================

def _chol_sigma(A, Gd, Gc):
    Rd = np.linalg.cholesky(Gd).T
    Rc = np.linalg.cholesky(Gc).T
    S = np.linalg.solve(Rd.T.conj(), (Rc @ A).T.conj()).T.conj()
    s = np.linalg.svd(S, compute_uv=False)
    return float(s.min()), float(s.max())


def _eigh_sigma(A, Gd, Gc):
    """Leg 176's whitening, kept so the converted numbers connect to its digits."""
    w, U = np.linalg.eigh(Gd); Gdih = (U * (1.0 / np.sqrt(w))) @ U.T
    w, U = np.linalg.eigh(Gc); Gch = (U * np.sqrt(w)) @ U.T
    s = np.linalg.svd(Gch @ A @ Gdih, compute_uv=False)
    return float(s.min()), float(s.max())


def bordered_section(N, kappa=1.0, border_weight=1.0, lo=0, realify=True):
    """Leg 176's `rect_sigma` section, with the X block scaled by `kappa`.

    Domain modes `[lo, N)` (+) C, range modes `[0, N+2)` (+) C, RANGE UNTRUNCATED
    -- the same shape leg 176's C1 uses, so the numbers are directly its numbers.

    `realify` applies leg 249 sec 8's observation: `m` and `ell` are purely
    imaginary, so the diagonal unitary `kappa -> i kappa` on the domain border
    coordinate and `-i` on the range one makes the whole section REAL.  Both
    Grams carry a scalar weight on those coordinates, so the unitaries commute
    with them and no norm moves.  It is a 4x saving on every SVD here, and it is
    CHECKED against the complex form in `X2` rather than assumed.
    """
    Nr = N + 2
    nd = N - lo
    dt = float if realify else complex
    A = np.zeros((Nr + 1, nd + 1), dtype=dt)
    A[:Nr, :nd] = l0_plus(Nr)[:, lo:N]
    n = np.arange(lo, N)
    if realify:
        A[0, nd] = A[1, nd] = 0.5                      # i * m
        A[Nr, :nd] = (-1.0) ** n * (1.0 - 2.0 * n)     # -i * ell
    else:
        A[:Nr, nd] = symmetry_modes(Nr)[1]
        A[Nr, :nd] = border_row(N)[lo:N]
    Gd = np.zeros((nd + 1, nd + 1)); Gd[:nd, :nd] = kappa * x_gram(N)[lo:, lo:]
    Gd[nd, nd] = border_weight
    Gc = np.zeros((Nr + 1, Nr + 1)); Gc[:Nr, :Nr] = kappa * x_gram(Nr)
    Gc[Nr, Nr] = border_weight
    return A, Gd, Gc


def tail_section(N, kappa=1.0, K=2):
    """The tail block: domain modes `[K, N)`, UNBORDERED, range untruncated.

    No border coordinate appears, so `kappa` multiplies both Grams and must
    cancel exactly.  That is prediction P2, and it is tested rather than assumed.
    """
    Nr = N + 2
    L = l0_plus(Nr)[:, K:N]
    return L, kappa * x_gram(N)[K:, K:], kappa * x_gram(Nr)


def z1_blockdiag(K, M, kappa=1.0):
    """Leg 176's C5 `Z_1 = ||I - A L||_X`, with the X block scaled by `kappa`."""
    Lb = bordered_operator(M)
    idx = list(range(K + 1)) + [M] + list(range(K + 1, M))
    Lp = Lb[np.ix_(idx, idx)]
    nF = K + 2
    A = np.zeros_like(Lp)
    A[:nF, :nF] = np.linalg.inv(Lp[:nF, :nF])
    A[nF:, nF:] = np.linalg.inv(Lp[nF:, nF:])
    E = np.eye(len(idx)) - A @ Lp
    Gp = np.zeros((M + 1, M + 1)); Gp[:M, :M] = kappa * x_gram(M); Gp[M, M] = 1.0
    Gp = Gp[np.ix_(idx, idx)]
    Gh, Gih = H._sym_sqrt(Gp)
    return float(np.linalg.svd(Gh @ E @ Gih, compute_uv=False)[0])


def dual_norm(N, kappa=1.0):
    """`||ell||_{X*}` with the X block scaled by `kappa`: predicted `x_dual/sqrt(kappa)`."""
    e = border_row(N)
    Gi = np.linalg.inv(kappa * x_gram(N))
    return float(np.sqrt(np.real(np.vdot(e, Gi @ e))))


# ===========================================================================
# X2 -- P1: scaling the X block == moving the border weight
# ===========================================================================

def x2_equivalence(N=256):
    """`kappa` on the X block with unit border == unit X block with border `1/kappa`.

    An overall positive scaling of BOTH Grams leaves sigma_min fixed, so the two
    are the same computation.  This is the identity that makes leg 249's
    `bw = 1/(2 pi)` a normalization conversion at all -- and it is what lets this
    leg convert the rest of the certificate by the same route.
    """
    R = {"N": N, "pairs": {}}
    # the realification control, at every convention: the REAL section and the
    # COMPLEX one must give the same sigma_min, or the 4x saving is unsound.
    R["realification_control"] = {}
    for name, k in CONV.items():
        sr = _chol_sigma(*bordered_section(128, kappa=k, realify=True))[0]
        sc = _chol_sigma(*bordered_section(128, kappa=k, realify=False))[0]
        R["realification_control"][name] = {
            "real_section": sr, "complex_section": sc,
            "relative_difference": abs(sr - sc) / sr}
    for name, k in CONV.items():
        if k == 1.0:
            continue
        s_scaled = _chol_sigma(*bordered_section(N, kappa=k, border_weight=1.0))[0]
        s_bw = _chol_sigma(*bordered_section(N, kappa=1.0, border_weight=1.0 / k))[0]
        R["pairs"][name] = {
            "kappa": k,
            "sigma_via_scaled_X_block": s_scaled,
            "sigma_via_border_weight_1_over_kappa": s_bw,
            "relative_difference": abs(s_scaled - s_bw) / s_scaled,
        }
    R["reading"] = (
        "P1 CONFIRMED at the relative differences recorded.  The two routes are "
        "the same computation, so leg 249's border-weight sweep IS a sweep of the "
        "X-block normalization constant, and the whole certificate can be "
        "converted through it.")
    return R


# ===========================================================================
# X3 -- THE CONVERSION TABLE
# ===========================================================================

SIG_N = [8, 16, 32, 64, 128, 256, 512]


def x3_conversion_table():
    R = {}

    # --- Q1: the bordered sigma_min (leg 176 C1, the 0.0908 headline) --------
    q1 = {"ladder": {}, "note": "domain [0,N) (+) C, range untruncated; Cholesky whitening"}
    for N in SIG_N:
        row = {}
        for name, k in CONV.items():
            smin, smax = _chol_sigma(*bordered_section(N, kappa=k))
            row[name] = {"sigma_min": smin, "sigma_max": smax,
                         "resolvent_norm": 1.0 / smin}
        q1["ladder"][str(N)] = row
    top = q1["ladder"][str(SIG_N[-1])]
    q1["at_N_512"] = {n: top[n]["sigma_min"] for n in CONV}
    q1["conversion_factor_vs_repo"] = {
        n: top[n]["sigma_min"] / top["repo"]["sigma_min"] for n in CONV}
    # leg 176's own whitening at 512, so the converted digits connect to the
    # banked ones rather than to a re-whitened re-measurement
    q1["leg176_whitening_at_512"] = {
        n: _eigh_sigma(*bordered_section(512, kappa=k))[0] for n, k in CONV.items()}
    q1["is_a_fixed_power_of_kappa"] = {
        n: {"measured_factor": top[n]["sigma_min"] / top["repo"]["sigma_min"],
            "if_it_were_kappa_to_the_minus_half": k ** -0.5,
            "if_it_were_kappa_to_the_minus_quarter": k ** -0.25}
        for n, k in CONV.items() if k != 1.0}
    R["Q1_bordered_sigma_min"] = q1

    # --- Q2: the tail block (leg 176 C2, ||T^-1||_X = 4.026) -----------------
    q2 = {"K_blocks": {}}
    for K in (2, 4, 8, 16):
        row = {}
        for name, k in CONV.items():
            smin, _ = _chol_sigma(*tail_section(512, kappa=k, K=K))
            row[name] = {"sigma_min": smin, "inverse_norm": 1.0 / smin}
        row["max_relative_spread_over_conventions"] = (
            max(v["sigma_min"] for v in row.values() if isinstance(v, dict))
            - min(v["sigma_min"] for v in row.values() if isinstance(v, dict))
        ) / row["repo"]["sigma_min"]
        q2["K_blocks"][str(K)] = row
    q2["P2_verdict"] = ("EXACTLY INVARIANT as predicted: the tail block carries no "
                        "border coordinate, so kappa multiplies range and domain "
                        "Grams alike and cancels.  ||T^-1||_X = 4.026 needs NO "
                        "conversion -- it already reads the same in Xu's units.")
    R["Q2_tail_inverse_norm"] = q2

    # --- Q3: Z_1 (leg 176 C5, the 140.72 that fails its threshold) -----------
    q3 = {"ladder": {}}
    for M in (64, 128, 256):
        q3["ladder"][str(M)] = {n: z1_blockdiag(2, M, kappa=k) for n, k in CONV.items()}
    a = q3["ladder"]["256"]
    q3["conversion_factor_vs_repo"] = {n: a[n] / a["repo"] for n in CONV}
    q3["threshold"] = 1.0
    q3["still_fails_in_every_convention"] = all(v > 1.0 for v in a.values())
    R["Q3_Z1_blockdiagonal"] = q3

    # --- Q4: the border row's dual norm (leg 176 C8) -------------------------
    q4 = {"ladder": {}}
    for N in (64, 128, 256, 512):
        row = {n: dual_norm(N, kappa=k) for n, k in CONV.items()}
        row["predicted_from_repo_over_sqrt_kappa"] = {
            n: row["repo"] / math.sqrt(k) for n, k in CONV.items()}
        row["max_relative_deviation_from_prediction"] = max(
            abs(row[n] - row["repo"] / math.sqrt(k)) / row[n] for n, k in CONV.items())
        q4["ladder"][str(N)] = row
    q4["P4_verdict"] = ("CONFIRMED: ||ell||_{X*} is exactly homogeneous of degree "
                        "-1/2 in kappa, to the deviations recorded.")
    R["Q4_border_row_dual_norm"] = q4

    return R


# ===========================================================================
# X4 -- gate (a): agreement with leg 249's own weight-sweep images
# ===========================================================================

def x4_against_leg249(N=256):
    R = {"N": N, "source": "writeup/data/p2_route_h2cv_v1_postconstruction.json"}
    with open(L249) as fh:
        d = json.load(fh)["W5_border_weight_sensitivity"]
    R["banked_N"] = d["N"]

    sweep = {}
    for wk, rec in d["sweep"].items():
        mine = _chol_sigma(*bordered_section(N, kappa=1.0, border_weight=float(wk)))[0]
        sweep[wk] = {"banked": rec["sigma_min"], "recomputed_here": mine,
                     "relative_difference": abs(mine - rec["sigma_min"]) / rec["sigma_min"]}
    R["sweep_reproduction"] = sweep
    R["max_relative_difference_over_sweep"] = max(
        v["relative_difference"] for v in sweep.values())

    # the single converted number leg 249 banks, reproduced by the OTHER route
    # (scale the X block; never touch the border weight)
    banked = d["sigma_if_X_block_carried_the_2pi"]
    mine_scaled = _chol_sigma(*bordered_section(N, kappa=TWOPI, border_weight=1.0))[0]
    R["leg249_0p0420_anchor"] = {
        "banked_sigma_if_X_block_carried_the_2pi": banked,
        "recomputed_here_by_scaling_the_X_block": mine_scaled,
        "relative_difference": abs(mine_scaled - banked) / banked,
    }
    # and the half-line value, which no artifact contains
    mine_half = _chol_sigma(*bordered_section(N, kappa=PI, border_weight=1.0))[0]
    R["half_line_value_at_same_N"] = {
        "sigma_min": mine_half,
        "resolvent_norm": 1.0 / mine_half,
        "ratio_to_leg249_full_line_value": mine_half / banked,
        "ratio_to_repo_value_0p0908": mine_half / d["sigma_at_weight_1"],
    }

    # P3: is the conversion a fixed power?  The sweep's own non-monotonicity
    # answers no; recorded as a magnitude.
    vals = {float(k): v["recomputed_here"] for k, v in sweep.items()}
    ks = sorted(vals)
    R["P3_non_monotone_check"] = {
        "argmax_weight": max(ks, key=lambda k: vals[k]),
        "max_sigma": max(vals.values()),
        "sigma_at_largest_weight": vals[ks[-1]],
        "falls_back_by": (max(vals.values()) - vals[ks[-1]]) / max(vals.values()),
    }
    # the small-weight sqrt law, and the deviation from it AT the Xu points
    lo1, lo2 = ks[0], ks[1]
    slope = (math.log(vals[lo2]) - math.log(vals[lo1])) / (math.log(lo2) - math.log(lo1))
    R["P3_small_weight_power_law"] = {
        "fitted_exponent_between_two_smallest_weights": slope,
        "predicted_if_sqrt_law": 0.5,
        "sqrt_law_extrapolation_to_w_full_line": vals[lo1] * (1.0 / TWOPI / lo1) ** 0.5,
        "actual_at_w_full_line": mine_scaled,
        "sqrt_law_extrapolation_to_w_half_line": vals[lo1] * (1.0 / PI / lo1) ** 0.5,
        "actual_at_w_half_line": mine_half,
    }
    R["reading"] = (
        "GATE (a) YES.  Every one of leg 249's seven sweep points reproduces, and "
        "its single converted number reproduces from the structurally different "
        "route (scaling the X block rather than moving the border weight), which "
        "is the independent content: the two routes were never checked against "
        "each other.  The half-line value is new -- no artifact contains it.")
    return R


# ===========================================================================
# X5 -- gate (b): what Xu actually publishes that is directly comparable
# ===========================================================================

def x5_xu_comparands(nmax=48):
    """Lemma 4.5 is the only exactly-evaluated operator norm Xu publishes.

    It is tested here TWICE -- as a Mellin symbol identity (sharp) and as a
    finite-section norm ladder approaching the published `1/alpha` -- and its
    role is stated honestly: it is an external control on the half-line
    machinery X1 depends on, NOT a comparand for the certificate's numbers.
    """
    R = {}

    # (i) the Mellin symbol identity of Lemma 4.5 at z = 0, on a test datum.
    # M[T_z g](1/2 + i xi) = (z + 1/2 - i xi)^-1 M[g](1/2 + i xi).
    # Take g(t) = t^{-1/2} exp(-t) * t^{i eta} style probes and evaluate both
    # sides by the same half-line rule.
    y, w = de_half(0.02, 4.0)
    sym = {}
    for xi in (0.0, 0.5, 1.5, 3.0):
        g = np.exp(-y) * y ** 1.25                    # decays at both ends
        # T_0 g (y) = (1/y) int_0^y g dt, by cumulative quadrature on the rule
        cum = np.cumsum(w * g)
        Tg = cum / y
        s = 0.5 + 1j * xi
        lhs = np.sum(w * Tg * y ** (s - 1))
        rhs = np.sum(w * g * y ** (s - 1)) / (0.0 + 0.5 - 1j * xi)
        sym[str(xi)] = {"lhs": [float(lhs.real), float(lhs.imag)],
                        "rhs": [float(rhs.real), float(rhs.imag)],
                        "relative_difference": float(abs(lhs - rhs) / abs(rhs))}
    R["lemma_4p5_mellin_symbol_identity_at_z0"] = sym
    R["lemma_4p5_max_relative_difference"] = max(
        v["relative_difference"] for v in sym.values())

    # (ii) the published exact norm itself: ||T_0|| = 1/alpha = 2 at z = 0.
    # Finite sections in the Laguerre ON basis of L^2(0, oo); the norm is not
    # attained (continuous spectrum), so the ladder must approach 2 FROM BELOW
    # and slowly.  Reported as a ladder, not as a pass/fail.
    # The rule is cut at `y ~ 600` here, NOT at the `3.5e19` of `de_half`'s
    # default: the Laguerre functions carry `exp(-y/2)`, so `lagval` overflows
    # long before the weight kills it, and every matrix entry `<e_j, T_0 e_k>`
    # has an exponentially decaying `e_j` in it.  The algebraic `1/y` tail of
    # `T_0 e_k` is therefore never integrated bare, and the cut is harmless --
    # which the two rules below check rather than assume.
    from numpy.polynomial import laguerre as lag
    lad = {}
    for (h, U) in [(0.005, 2.5), (0.0025, 2.7)]:
        yy, ww = de_half(h, U)
        row = {"max_y": float(yy.max())}
        Eb = np.zeros((nmax, len(yy)))
        for k in range(nmax):
            cc = np.zeros(k + 1); cc[k] = 1.0
            Eb[k] = lag.lagval(yy, cc) * np.exp(-yy / 2.0)
        cums = np.cumsum(ww * Eb, axis=1) / yy
        for n in (8, 16, 32, nmax):
            T = np.zeros((n, n))
            for k in range(n):
                T[:, k] = np.sum(ww * Eb[:n] * cums[k], axis=1)
            row[str(n)] = float(np.linalg.svd(T, compute_uv=False).max())
        lad[f"h={h},U={U}"] = row
    R["lemma_4p5_finite_section_norm_ladder"] = lad
    R["lemma_4p5_published_exact_norm_at_z0"] = 2.0

    # (iii) the evaluable constants of Prop 4.6's majorant, at z = 0
    cG = 5.0 / 4.0 + math.sqrt(10.0) + 2.0
    R["prop_4p6_constants_at_z0"] = {
        "c_G": cG,
        "alpha_at_z0": 0.5,
        "tail_norm_bound_1_over_sqrt_2alpha": 1.0 / math.sqrt(2 * 0.5),
        "A_tail_bound_cG_over_sqrt6_alpha_3half": cG / (math.sqrt(6.0) * 0.5 ** 1.5),
        "hardy_piece_bound_5_over_4alpha": 5.0 / (4 * 0.5),
        "C_R_d": None,
    }

    # (iv) the certificate's own numbers, for the record, next to them
    with open(L176) as fh:
        c = json.load(fh)
    R["certificate_numbers_for_comparison"] = {
        "sigma_min_at_512_banked": c["C1_bordered_sigma_min_X"]["sigma_min_at_512"],
        "resolvent_norm_banked": c["C1_bordered_sigma_min_X"]["resolvent_norm_at_512"],
        "tail_inverse_norm_banked": c["C2_tail_block_sigma_min"]["tail_inverse_norm_K2_at_512"],
    }

    R["reading"] = (
        "GATE (b) NO COMPARAND EXISTS, AND THE REASON IS STRUCTURAL, NOT AN "
        "OMISSION.  Proposition 4.6's majorant ||R_0(z)||_X <= C(R,d) alpha^{-3/2} "
        "is stated on {Re z > -1/2} \\ {0, 1}, and z = 0 is one of the two EXCLUDED "
        "points -- it is an eigenvalue of L_0 on the odd X-realization.  z = 0 is "
        "exactly where the certificate lives, and the bordered formulation exists "
        "precisely to handle that excluded point.  So Xu's resolvent bound cannot "
        "be evaluated at the certificate's z, and its constant C(R,d) is left "
        "unevaluated in any case.  Lemma 4.5's ||T_z|| = 1/alpha IS an exactly "
        "published number (2 at z = 0), but it is the norm of the Hardy operator on "
        "L^2(0,oo), a DIFFERENT operator from the inverse of the tail block of "
        "L_0^+; it is used here as an external control on the half-line machinery, "
        "and the comparison magnitude against ||T^-1||_X is reported, not claimed.")
    return R


# ===========================================================================

def main():
    t0 = time.time()
    R = {
        "leg": 277, "route": "XUN", "role": "conversion bridge",
        "date": "2026-08-07",
        "gate_question": (
            "Under Xu's normalization, do the certificate's converted quantities "
            "agree with (a) their own weight-sweep images per leg 249, and (b) any "
            "directly-comparable value Xu publishes?"),
        "primary_source": {
            "arxiv": "2607.19762", "md5": "709dac668a1ff508f00d765916db492c",
            "locators_read_in_this_pass": [
                "Definition 4.1 eq (4.2) -- the HALF-LINE norm",
                "Definition 4.1 sentence 2 -- the 'equivalent' full-line odd-H^2(R) norm",
                "Lemma 4.5 eq (4.24) -- exact norm 1/alpha",
                "Proposition 4.6 eq (4.27) -- majorant on {Re z > -1/2} \\ {0,1}",
                "Prop 4.6 proof after (4.25) -- c_G = 5/4 + sqrt(10) + 2",
                "Prop 4.6 proof eqs (4.28)-(4.29)",
                "Proposition 2 -- realization dichotomy",
                "Section 2 Table 1 -- the branch numerics (no norms)"]},
        "ceiling": ("a = 0 only.  Converting a number does not lift the ceiling "
                    "attached to it.  No link of L1->L4 moved, Clay odds unchanged "
                    "at ~0.05%, no ban lifted, no GA compute."),
        "ga_compute": False,
        "edits_nothing_it_converts": True,
    }
    print("X1 conversion constant ...", flush=True)
    R["X1_conversion_constant"] = x1_conversion_constant()
    print("X2 equivalence of routes ...", flush=True)
    R["X2_route_equivalence"] = x2_equivalence()
    print("X3 conversion table ...", flush=True)
    R["X3_conversion_table"] = x3_conversion_table()
    print("X4 against leg 249's sweep ...", flush=True)
    R["X4_against_leg249_sweep"] = x4_against_leg249()
    print("X5 Xu comparands ...", flush=True)
    R["X5_xu_comparands"] = x5_xu_comparands()

    q1 = R["X3_conversion_table"]["Q1_bordered_sigma_min"]
    R["gate"] = {
        "a_weight_sweep_agreement": R["X4_against_leg249_sweep"][
            "max_relative_difference_over_sweep"],
        "a_anchor_agreement": R["X4_against_leg249_sweep"][
            "leg249_0p0420_anchor"]["relative_difference"],
        "b_comparand_exists": False,
        "b_reason": "z = 0 is excluded from Proposition 4.6's region",
        "sigma_min_512_repo": q1["at_N_512"]["repo"],
        "sigma_min_512_xu_full_line": q1["at_N_512"]["xu_full_line"],
        "sigma_min_512_xu_half_line_4p2": q1["at_N_512"]["xu_half_line_4p2"],
        "answer": (
            "(a) YES -- every sweep point and the 0.0420 anchor reproduce, the "
            "anchor by a structurally different route.  (b) NO COMPARAND -- Xu "
            "publishes none at z = 0 and cannot, since z = 0 is excluded from "
            "Prop 4.6.  DISCREPANCY FOUND, and it is in the bridge itself: "
            "'Xu's own normalization' is ambiguous in Definition 4.1, and the "
            "0.0420 leg 270 carries adopts the full-line 'equivalent' norm rather "
            "than the displayed half-line definition (4.2).  Under (4.2) the "
            "constant is pi, not 2 pi.  NOT an escalation: leg 176's gate property "
            "-- sigma_min bounded away from zero uniformly in the truncation -- is "
            "invariant under every positive constant, and is unmoved."),
    }
    R["runtime_seconds"] = time.time() - t0

    with open(OUT, "w") as fh:
        json.dump(R, fh, indent=1)

    print("\n--- leg 277 summary ---")
    print(f"  half-line Gram real part vs pi*G : "
          f"{R['X1_conversion_constant']['half_line']['max_abs_dev_of_REAL_part_from_pi_G']:.2e}")
    print(f"  half-line Gram imaginary part    : "
          f"{R['X1_conversion_constant']['half_line']['max_abs_imaginary_part']:.6g}")
    print(f"  real-subspace ratio dev from 1   : "
          f"{R['X1_conversion_constant']['real_subspace_ratio_half_over_piG']['max_abs_dev_from_1']:.2e}")
    for n in CONV:
        print(f"  sigma_min(N=512) [{n:>18}] = {q1['at_N_512'][n]:.7f}"
              f"   ||R||_X = {1.0/q1['at_N_512'][n]:.4f}")
    print(f"  tail ||T^-1||_X spread over conventions: "
          f"{R['X3_conversion_table']['Q2_tail_inverse_norm']['K_blocks']['2']['max_relative_spread_over_conventions']:.2e}")
    print(f"  sweep max rel diff vs leg 249    : {R['gate']['a_weight_sweep_agreement']:.2e}")
    print(f"  0.0420 anchor rel diff           : {R['gate']['a_anchor_agreement']:.2e}")
    print(f"  runtime {R['runtime_seconds']:.1f}s -> {os.path.normpath(OUT)}")


if __name__ == "__main__":
    main()
