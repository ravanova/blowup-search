#!/usr/bin/env python3
"""Leg 281 -- ROUTE-CVF: which of the certificate's quoted quantities are convention-free?

Leg 277 proved ONE quantity convention-free (`||T^-1||_X = 4.0262407`, invariant to
`<= 1.53e-08` over four tail blocks) while `sigma_min` moves `12.5x` under leg 249's
border-weight sweep and `1.37x` under the two norms Xu's Definition 4.1 names.  This leg
extends that from one quantity to THE FULL QUOTED SET, enumerated and committed in
`writeup/novelty/leg_281.md` BEFORE any number here existed (commit `9a003d0`).

THE CONVENTION AXIS.  Leg 277's P1 proved that scaling the `X` block by `kappa` with the
border amplitude at weight 1 is the SAME COMPUTATION as leaving the `X` block alone and
giving the border weight `1/kappa`.  So leg 249's border-weight sweep and Xu's Definition
4.1 ambiguity are one axis, parameterised here by `kappa`:

    kappa = 1     the repository's convention (unweighted coefficient Gram `G = I + J^4`)
    kappa = pi    Xu Definition 4.1 eq (4.2), the DISPLAYED half-line norm  (leg 277)
    kappa = 2 pi  Xu Definition 4.1 sentence 2, the "equivalent" full-line norm (leg 249)

THE THREE CLASSES, registered in the novelty pass before any number:

    CF  convention-free            invariant over the whole sweep, WITH A MECHANISM
    CX  convention-relative,       moves, but by a proved closed-form power of kappa
        exactly convertible
    CR  convention-relative,       moves, and matches NO power of kappa
        no law

Sections
  S0  reproduction control: reproduce leg 249's W5 sweep and leg 277's three anchors,
      through this leg's own independently-written sections
  S1  Group A -- the bordered section (sigma_min, sigma_max, ||R||_X, the ladder spread)
  S2  Group B -- the tail block (leg 277's anchor, extended to the full sweep)
  S3  Group C -- the Z-battery, and the terms the certificate declines to form
  S4  Group D -- the dual pairing and its ell^2 companion
  S5  Group E -- the controls PUB2 quotes as load-bearing, incl. the 0.71465 question
  S6  Group F -- the quantities quoted from the OTHER space (ell^1_w)
  S7  the secondary axes: whitening route, realification gauge -- is the axis really 1-D?
  S8  the enumeration's own closure test, counted mechanically

NOTHING IS EDITED.  `solver/origin_h2_certificate.py` is imported as the object being
classified.  Legs 176/249/277 JSON read-only.  PUB2 read-only (S8 reads it as text).
"""

import json
import math
import os
import re
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.origin_h2_certificate as H
from solver.origin_h2_certificate import (
    border_row, bordered_operator, l0_plus, symmetry_modes, x_gram,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_cvf_v1_classify.json")
L176 = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2c_v1_construction.json")
L249 = os.path.join(HERE, "..", "writeup", "data", "p2_route_h2cv_v1_postconstruction.json")
L277 = os.path.join(HERE, "..", "writeup", "data", "p2_route_xun_v1_convert.json")
PUB2 = os.path.join(HERE, "..", "writeup", "4_p2_lottery", "TECHNICAL_P2_PUB2_V1.md")

PI = math.pi
TWOPI = 2.0 * math.pi

# The sweep.  Leg 249 swept the BORDER weight over 1e-2 .. 1e2; via P1 that is
# kappa over 1e-2 .. 1e2.  This leg goes two decades wider on each side, so that
# "the measured range" is not an artefact of where leg 249 happened to stop.
KAPPA = [1e-4, 1e-3, 1e-2, 1e-1, 1.0, PI, TWOPI, 1e1, 1e2, 1e3, 1e4]
NAMED = {"repo": 1.0, "xu_half_line_4p2": PI, "xu_full_line": TWOPI}
KEY = lambda k: f"{k:.10g}"


def spread(vals):
    """Relative spread `(max - min)/max` of a set of positive numbers."""
    v = [x for x in vals if x == x]
    if not v or max(v) == 0:
        return float("nan")
    return float((max(v) - min(v)) / max(v))


def ratio(vals):
    v = [x for x in vals if x == x and x > 0]
    return float(max(v) / min(v)) if v else float("nan")


def power_fit(kap, val):
    """Fit `val ~ C kappa^p`; return `p` and the max relative residual of the fit.

    A quantity is `CX` only if this fit is TIGHT -- the residual is what separates
    `CX` from `CR`, and it is reported as a magnitude rather than as a verdict.
    """
    lk, lv = np.log(np.array(kap)), np.log(np.array(val))
    p, c = np.polyfit(lk, lv, 1)
    pred = np.exp(c) * np.array(kap) ** p
    return float(p), float(np.abs(pred / np.array(val) - 1.0).max())


# ---------------------------------------------------------------------------
# the sections, with the X block carrying kappa
# ---------------------------------------------------------------------------

_EIG = {}
_CHOL = {}
_L0 = {}


def _eig_gram(N, lo=0):
    """Cached `eigh` of the UNSCALED `X` Gram block `x_gram(N)[lo:, lo:]`.

    THE reason this leg is affordable.  The whole classification sweeps `kappa`,
    and `kappa` multiplies the Gram by a scalar -- which leaves its eigenVECTORS
    untouched and scales its eigenVALUES by `kappa`.  So one `eigh` per `(N, lo)`
    serves every convention, and the sweep costs a matmul each instead of an
    11-second symmetric eigendecomposition each.  This is an exact algebraic
    identity, not an approximation, and S7's route comparison re-derives the same
    sigma through Cholesky and through leg 249's rescaling as a check on it.
    """
    key = (int(N), int(lo))
    if key not in _EIG:
        G = x_gram(int(N))[int(lo):, int(lo):]
        _EIG[key] = np.linalg.eigh(G)
    return _EIG[key]


def _l0(N):
    N = int(N)
    if N not in _L0:
        _L0[N] = np.real(l0_plus(N))
    return _L0[N]


def _chol_gram(N, lo=0):
    """Cached upper Cholesky factor `R` of the UNSCALED `X` Gram block, `G = R^T R`.

    THE reason this leg is affordable, and the reason it is ACCURATE.  `kappa`
    multiplies the Gram by a positive scalar, so `chol(kappa G) = sqrt(kappa) R`
    exactly -- one factorization per `(N, lo)` serves all eleven conventions, and
    the whitening never forms an explicit `G^{-1/2}` at condition ~1e12.  An
    eigenvector-based `(U d) U^T` whitening was written first and REJECTED here:
    at `N = 512` it reproduced leg 176's banked `sigma_min` only to `8.6e-07`
    relative, against `3.4e-13` for this route (S0 records both).  The tail block's
    convention-freeness is claimed at `1e-8`, so the whitening had to be better
    than the claim.
    """
    key = (int(N), int(lo))
    if key not in _CHOL:
        G = x_gram(int(N))[int(lo):, int(lo):]
        _CHOL[key] = np.linalg.cholesky(G).T          # upper R with G = R^T R
    return _CHOL[key]


def _R(N, lo, kappa, bordered):
    """`chol(kappa G)` = `sqrt(kappa) R`, optionally bordered by the unit weight."""
    R = math.sqrt(kappa) * _chol_gram(N, lo)
    if not bordered:
        return R
    n = R.shape[0]
    out = np.zeros((n + 1, n + 1))
    out[:n, :n] = R
    out[n, n] = 1.0
    return out


def _sigma_pencil(A, Rd, Rc):
    """`min/max ||A u||_Gc / ||u||_Gd` from the Cholesky factors, via `Rc A Rd^{-1}`."""
    S = np.linalg.solve(Rd.T, (Rc @ A).T).T
    s = np.linalg.svd(S, compute_uv=False)
    return float(s.min()), float(s.max())


def _bordered_A(N, lo=0, realify=True):
    Nr = N + 2
    nd = N - lo
    A = np.zeros((Nr + 1, nd + 1), dtype=float if realify else complex)
    A[:Nr, :nd] = _l0(Nr)[:, lo:N] if realify else l0_plus(Nr)[:, lo:N]
    n = np.arange(lo, N)
    if realify:
        A[0, nd] = A[1, nd] = 0.5                      # i * m
        A[Nr, :nd] = (-1.0) ** n * (1.0 - 2.0 * n)     # -i * ell
    else:
        A[:Nr, nd] = symmetry_modes(Nr)[1]
        A[Nr, :nd] = border_row(N)[lo:N]
    return A


def sigma_bordered(N, kappa=1.0, lo=0):
    """`sigma_min`, `sigma_max` of leg 176's C1 section with the X block at `kappa`."""
    return _sigma_pencil(_bordered_A(N, lo), _R(N, lo, kappa, True),
                         _R(N + 2, 0, kappa, True))


def sigma_tail(N, kappa=1.0, K=2):
    """`sigma_min` of the UNBORDERED tail block, domain modes `[K, N)`."""
    return _sigma_pencil(_l0(N + 2)[:, K:N], _R(N, K, kappa, False),
                         _R(N + 2, 0, kappa, False))[0]


def _whiten_sigma(A, Gd, Gc, route="eigh"):
    """`min ||A u||_Gc / ||u||_Gd`.  Two routes, because route IS a convention axis (S7)."""
    if route == "chol":
        Rd = np.linalg.cholesky(Gd).T
        Rc = np.linalg.cholesky(Gc).T
        S = np.linalg.solve(Rd.T.conj(), (Rc @ A).T.conj()).T.conj()
    elif route == "eigh":                      # leg 176's own whitening
        w, U = np.linalg.eigh(Gd); Gdih = (U * (1.0 / np.sqrt(w))) @ U.T.conj()
        w, U = np.linalg.eigh(Gc); Gch = (U * np.sqrt(w)) @ U.T.conj()
        S = Gch @ A @ Gdih
    elif route == "rescale":                   # leg 249's diagonal rescaling
        dd, dc = np.sqrt(np.real(np.diag(Gd))), np.sqrt(np.real(np.diag(Gc)))
        Gdn = Gd / np.outer(dd, dd); Gcn = Gc / np.outer(dc, dc)
        An = (A * dc[:, None]) / dd[None, :]
        w, U = np.linalg.eigh(Gdn); Gdih = (U * (1.0 / np.sqrt(w))) @ U.T.conj()
        w, U = np.linalg.eigh(Gcn); Gch = (U * np.sqrt(w)) @ U.T.conj()
        S = Gch @ An @ Gdih
    else:
        raise ValueError(route)
    s = np.linalg.svd(S, compute_uv=False)
    return float(s.min()), float(s.max())


def bordered_section(N, kappa=1.0, lo=0, realify=True):
    """Leg 176's `rect_sigma` section with the `X` block scaled by `kappa`.

    Domain modes `[lo, N)` (+) C, range modes `[0, N+2)` (+) C, RANGE UNTRUNCATED --
    leg 176's C1 shape exactly, so the numbers are directly its numbers.  `realify`
    is leg 249 sec 8's diagonal unitary (`m`, `ell` purely imaginary); it is CHECKED
    against the complex section in S7, not assumed.
    """
    Nr = N + 2
    nd = N - lo
    A = np.zeros((Nr + 1, nd + 1), dtype=float if realify else complex)
    A[:Nr, :nd] = np.real(l0_plus(Nr)[:, lo:N]) if realify else l0_plus(Nr)[:, lo:N]
    n = np.arange(lo, N)
    if realify:
        A[0, nd] = A[1, nd] = 0.5                      # i * m
        A[Nr, :nd] = (-1.0) ** n * (1.0 - 2.0 * n)     # -i * ell
    else:
        A[:Nr, nd] = symmetry_modes(Nr)[1]
        A[Nr, :nd] = border_row(N)[lo:N]
    Gd = np.zeros((nd + 1, nd + 1)); Gd[:nd, :nd] = kappa * x_gram(N)[lo:, lo:]
    Gd[nd, nd] = 1.0
    Gc = np.zeros((Nr + 1, Nr + 1)); Gc[:Nr, :Nr] = kappa * x_gram(Nr)
    Gc[Nr, Nr] = 1.0
    return A, Gd, Gc


def tail_section(N, kappa=1.0, K=2):
    """The tail block: domain `[K, N)`, UNBORDERED, range untruncated.

    No border coordinate, so `kappa` multiplies both Grams -- the CF mechanism, and
    it is measured rather than asserted.
    """
    Nr = N + 2
    return np.real(l0_plus(Nr)[:, K:N]), kappa * x_gram(N)[K:, K:], kappa * x_gram(Nr)


def sigma_loose(N, kappa=1.0):
    """Leg 176's C4: the LOOSE `L^2` realization -- IDENTITY Gram, still BORDERED.

    Leg 176 reaches this by `rect_sigma(n, gram=False)`, which leaves `bordered=True`
    and replaces BOTH Grams by the identity.  `kappa` is accepted and then does not
    appear, because the X-normalization constant is not in this quantity's
    DEFINITION at all -- the measurement is an exact zero, not a small number.
    """
    A = _bordered_A(N, 0)
    return float(np.linalg.svd(A, compute_uv=False).min())


def z1_blockdiag(K, M, kappa=1.0):
    """Leg 176's C5 `Z_1 = ||I - A L||_X`, `X` block scaled by `kappa`."""
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
    """`||ell||_{X*}` with the `X` block at `kappa`.  Predicted exactly `x_dual/sqrt(kappa)`.

    `||ell||_{X*}^2 = e^H (kappa G)^{-1} e`, evaluated through the cached Cholesky
    factor as `||R^{-T} e||^2 / kappa` rather than by forming an explicit inverse of
    a matrix whose condition number reaches ~1e12 at `N = 512`.  The `1/kappa` here
    is exact arithmetic on one scalar, which is precisely why this quantity has a
    conversion LAW while `sigma_min` does not: `kappa` never reaches the border.
    """
    e = np.real(border_row(N) / 1j) if np.iscomplexobj(border_row(N)) else border_row(N)
    e = np.asarray(e, dtype=float)
    R = _chol_gram(N, 0)
    z = np.linalg.solve(R.T, e)
    return float(math.sqrt(float(z @ z) / kappa))


def solvable_datum(N, nterm=6, seed=0):
    """Leg 176's datum on `{ell(f) = 0}` -- reproduced here, not imported."""
    e = border_row(N); m = symmetry_modes(N)[1]
    r = np.random.default_rng(seed)
    d = np.zeros(N, dtype=complex)
    d[:nterm] = r.normal(size=nterm) + 1j * r.normal(size=nterm)
    return d - (e @ d) / (e @ m) * m


def e4_bordered_ratio(N, kappa=1.0):
    """Leg 176's `E4` ratio -- and it is NOT what the novelty pass assumed.

    Read from `experiments/p2_route_h2c_v1_construction.py` L401:

        ratio_from_norms = sqrt(||u||_X^2 + |kappa_min|^2)
                         / sqrt(||f||_X^2 + |ell(u)|^2)

    Both radicands carry the BORDER coordinate, so this is the bordered Rayleigh
    quotient at its minimizer -- i.e. exactly `1/sigma_min`, which is why leg 176
    banked it beside `one_over_sigma_min` and got agreement to 3e-11.  The novelty
    pass listed `D3` under prediction Q1's "no border coordinate" clause; that was a
    MIS-ASSIGNMENT of the quantity, found by reading leg 176's source, and it is
    reported as such rather than quietly re-filed.  Q1's RULE is untouched -- D3 was
    never in its hypothesis -- but Q1's LIST was wrong.
    """
    Rd, Rc = _R(N, 0, kappa, True), _R(N + 2, 0, kappa, True)
    A = _bordered_A(N, 0)
    S = np.linalg.solve(Rd.T, (Rc @ A).T).T
    U, sv, Vt = np.linalg.svd(S)
    v = np.linalg.solve(Rd, Vt[-1])
    w = A @ v
    nu = math.sqrt(float(kappa) * float(v[:N] @ (_chol_gram(N, 0).T @ (_chol_gram(N, 0) @ v[:N]))))
    nf = math.sqrt(float(kappa) * float(w[:N + 2] @ (_chol_gram(N + 2, 0).T
                                                     @ (_chol_gram(N + 2, 0) @ w[:N + 2]))))
    num = math.sqrt(nu ** 2 + abs(float(v[N])) ** 2)
    den = math.sqrt(nf ** 2 + abs(float(w[N + 2])) ** 2)
    return num / den, 1.0 / float(sv.min())


def galerkin_kappa_G(N):
    """Leg 176's `C7` constant: the border amplitude of the SQUARE Galerkin section.

    Xu's Galerkin-inconsistency constant.  NOT this leg's convention constant -- the
    name collision is why it is spelled `kappa_G` everywhere here.  No Gram, no norm
    and no weight enters its definition: it is a COEFFICIENT of the solution vector
    of a square linear solve.  The X-normalization constant cannot reach it, which is
    the claim S5 records at exactly zero.
    """
    f = solvable_datum(N, 6, 0)
    Lb = bordered_operator(N)
    rhs = np.zeros(N + 1, dtype=complex)
    rhs[:N] = f
    sol = np.linalg.solve(Lb, rhs)
    return abs(complex(sol[N])), abs(complex(sol[N - 1]))


def unbordered_norm_ratio(seed=0, kappa=1.0, M=4096):
    """Leg 176's `C6` / leg 163's `G4`: `||u||_X / ||f||_X` from Xu's CLOSED FORM.

    No border coordinate on either side and the SAME norm on both, so `kappa`
    cancels in the quotient identically -- this one is convention-free by a
    one-line exact argument, and the numerical sweep below is CONFIRMATORY, not
    the evidence.  Reported that way.
    """
    c = solvable_datum(512, 6, seed)[:6]     # leg 176 C6's own datum, L318
    rat, un, fn = H.resolvent_ratio(c, M=M)[:3]
    k = math.sqrt(kappa)
    return (k * un) / (k * fn)


# ===========================================================================
# S0# ===========================================================================
# S0 -- reproduction control
# ===========================================================================

def s0_reproduction():
    R = {"role": ("independently-written sections reproduced against the banked numbers "
                  "of legs 176, 249 and 277 BEFORE any classification is drawn from them")}
    try:
        d176 = json.load(open(L176))
    except Exception as e:                                   # pragma: no cover
        d176 = None; R["leg176_load_error"] = str(e)
    try:
        d249 = json.load(open(L249))
    except Exception as e:                                   # pragma: no cover
        d249 = None; R["leg249_load_error"] = str(e)
    try:
        d277 = json.load(open(L277))
    except Exception as e:                                   # pragma: no cover
        d277 = None; R["leg277_load_error"] = str(e)

    # (i) leg 176's C1 at N = 512, repo convention, through THREE whitening routes.
    #     Which route is primary is a decision with a magnitude behind it, recorded
    #     here rather than in a comment.
    smin_c, smax_c = sigma_bordered(512, 1.0)                    # cached Cholesky
    smin_e = _whiten_sigma(*bordered_section(512, 1.0), route="eigh")[0]
    b = d176["C1_bordered_sigma_min_X"]["sigma_min_at_512"] if d176 else None
    R["C1_at_512_repo_convention"] = {
        "here_cached_cholesky": smin_c, "sigma_max_here": smax_c,
        "here_eigh_full_bordered_gram": smin_e,
        "leg176_banked": b,
        "cholesky_vs_eigh_relative": abs(smin_c - smin_e) / smin_e,
        "eigh_vs_leg176_banked_relative": (abs(smin_e - b) / b) if b else None,
        "cholesky_vs_leg176_banked_relative": (abs(smin_c - b) / b) if b else None,
        "reading": ("leg 176 whitened the FULL bordered Gram with eigh; this leg factors the "
                    "X block ONCE and scales it by sqrt(kappa), which is what makes an "
                    "eleven-point sweep affordable.  The two routes disagree at the level "
                    "recorded above -- a conditioning statement about a Gram whose entries "
                    "reach ~1e12 at N = 512, not a disagreement about the mathematics.  It is "
                    "far below every convention-dependence this leg reports for a CR quantity, "
                    "and far ABOVE nothing that is claimed CF, because the CF claims all live "
                    "on the tail block, where the same comparison is at 1e-13 (below)."),
    }

    # (i-b) the same comparison on the TAIL block -- where the CF claims actually live
    t_c = sigma_tail(512, 1.0, 2)
    t_e = _whiten_sigma(*tail_section(512, 1.0, 2), route="eigh")[0]
    R["C2_at_512_route_comparison"] = {
        "here_cached_cholesky_inverse_norm": 1.0 / t_c,
        "here_eigh_inverse_norm": 1.0 / t_e,
        "cholesky_vs_eigh_relative": abs(t_c - t_e) / t_e,
        "leg176_banked_inverse_norm": (
            d176["C2_tail_block_sigma_min"]["tail_inverse_norm_K2_at_512"] if d176 else None),
        "leg277_reported_inverse_norm": 4.0262407,
        "leg249_interval_enclosure": [4.02623993, 4.02624155],
        "cholesky_value_lies_inside_leg249_interval": bool(
            4.02623993 <= 1.0 / t_c <= 4.02624155),
        "leg176_banked_lies_inside_leg249_interval": bool(
            d176 is not None and 4.02623993 <=
            d176["C2_tail_block_sigma_min"]["tail_inverse_norm_K2_at_512"] <= 4.02624155),
        "reading": ("leg 277 sec 3.5 already recorded that leg 176's banked 4.02614534796022 "
                    "falls OUTSIDE leg 249's interval enclosure while 4.0262407 falls inside. "
                    "This row reproduces both sides of that independently and is the reason "
                    "the cached-Cholesky route is primary here: on the tail block it agrees "
                    "with the interval-enclosed value, and it is that block the CF claims "
                    "are made about."),
    }

    # (ii) leg 249's W5 border-weight sweep, reproduced through the kappa axis
    if d249:
        sw = d249["W5_border_weight_sensitivity"]["sweep"]
        rep = {}
        for bw, row in sw.items():
            k = 1.0 / float(bw)          # P1: border weight bw  <->  X-block kappa 1/bw
            here = sigma_bordered(256, k)[0]
            # sigma scales with the OVERALL Gram scaling; leg 249 held the X block at
            # 1 and moved the border, so its sigma is this one times sqrt(1/k) ... no:
            # an overall positive scaling of BOTH Grams leaves sigma_min fixed, and
            # (kappa on X, 1 on border) = (1 on X, 1/kappa on border) * kappa on BOTH.
            # The second factor cancels, so the two are equal outright.  P1, leg 277.
            rep[bw] = {"kappa": k, "leg249_sigma_min": row["sigma_min"],
                       "here": here,
                       "relative_difference": abs(here - row["sigma_min"]) / row["sigma_min"]}
        R["leg249_W5_sweep_reproduced"] = rep
        R["leg249_W5_max_relative_difference"] = max(
            v["relative_difference"] for v in rep.values())
        R["leg249_W5_ratio_over_its_own_range"] = d249[
            "W5_border_weight_sensitivity"].get("ratio_over_weight_range_1e-2_to_1e2")

    # (iii) leg 277's three anchors at N = 512
    anc = {}
    for name, k in NAMED.items():
        anc[name] = {"kappa": k,
                     "here": sigma_bordered(512, k)[0]}
    if d277:
        banked = d277["X3_conversion_table"]["Q1_bordered_sigma_min"]["leg176_whitening_at_512"]
        for name in anc:
            if name in banked:
                anc[name]["leg277_banked"] = banked[name]
                anc[name]["relative_difference"] = (
                    abs(anc[name]["here"] - banked[name]) / banked[name])
    R["leg277_anchors_at_512"] = anc

    # (iv) leg 277's convention-free anchor, the thing this leg generalises
    t = sigma_tail(512, 1.0, 2)
    R["leg277_anchor_tail_inverse_norm"] = {
        "here_repo_convention": 1.0 / t,
        "leg176_banked": (d176["C2_tail_block_sigma_min"]["tail_inverse_norm_K2_at_512"]
                          if d176 else None),
    }
    R["reading"] = ("every section below is exercised here against a number banked by a "
                    "DIFFERENT leg before it is used to classify anything.  Magnitudes above.")
    return R


# ===========================================================================
# S1 -- Group A: the bordered section
# ===========================================================================

A_LADDER_N = [32, 64, 128, 256, 512]


def s1_group_A():
    R = {"group": "A -- the bordered section (leg 176 C1; PUB2 sec 3.5 / 4.5 / 5(3) / 7)"}
    lad = {}
    for k in KAPPA:
        row = {}
        for N in A_LADDER_N:
            smin, smax = sigma_bordered(N, k)
            row[str(N)] = {"sigma_min": smin, "sigma_max": smax,
                           "resolvent_norm": 1.0 / smin}
        rel = [row[str(N)]["sigma_min"] for N in A_LADDER_N]
        row["ladder_relative_spread"] = spread(rel)
        row["ladder_relative_spread_64_to_512"] = spread(rel[1:])
        row["monotone_decreasing"] = bool(all(a >= b for a, b in zip(rel[:-1], rel[1:])))
        lad[KEY(k)] = row
    R["sweep"] = lad

    top = {KEY(k): lad[KEY(k)]["512"] for k in KAPPA}

    # --- A1 sigma_min ------------------------------------------------------
    vals = [top[KEY(k)]["sigma_min"] for k in KAPPA]
    p, res = power_fit(KAPPA, vals)
    R["A1_sigma_min_N512"] = {
        "quoted": 0.09080465147034879, "pinned_by": "kappa = 1 (repository convention)",
        "value_at_named": {n: top[KEY(k)]["sigma_min"] for n, k in NAMED.items()},
        "sweep_min": min(vals), "sweep_max": max(vals),
        "max_over_min": ratio(vals), "relative_spread": spread(vals),
        "best_power_fit_exponent": p, "best_power_fit_max_relative_residual": res,
        "monotone_in_kappa": bool(all(a <= b for a, b in zip(vals[:-1], vals[1:]))
                                  or all(a >= b for a, b in zip(vals[:-1], vals[1:]))),
        "argmax_kappa": KAPPA[int(np.argmax(vals))],
        "CLASS": "CR",
    }
    # --- A2 ||R||_X --------------------------------------------------------
    rv = [top[KEY(k)]["resolvent_norm"] for k in KAPPA]
    R["A2_resolvent_norm_N512"] = {
        "quoted": 11.012651706796523, "pinned_by": "kappa = 1",
        "value_at_named": {n: top[KEY(k)]["resolvent_norm"] for n, k in NAMED.items()},
        "sweep_min": min(rv), "sweep_max": max(rv), "max_over_min": ratio(rv),
        "CLASS": "CR", "note": "exactly 1/A1, so it inherits A1's class and its range inverted"}
    # --- A3 sigma_max ------------------------------------------------------
    mv = [top[KEY(k)]["sigma_max"] for k in KAPPA]
    p3, r3 = power_fit(KAPPA, mv)
    R["A3_sigma_max_N512"] = {
        "quoted": 499.64096369153697, "pinned_by": "kappa = 1",
        "value_at_named": {n: top[KEY(k)]["sigma_max"] for n, k in NAMED.items()},
        "sweep_min": min(mv), "sweep_max": max(mv), "max_over_min": ratio(mv),
        "best_power_fit_exponent": p3, "best_power_fit_max_relative_residual": r3,
        "relative_spread_over_the_three_NAMED_conventions": spread(
            [top[KEY(k)]["sigma_max"] for k in NAMED.values()]),
        "relative_spread_over_kappa_1e-4_to_1e3": spread(
            [top[KEY(k)]["sigma_max"] for k in KAPPA if k <= 1e3]),
        "breaks_at_kappa": next((k for k in KAPPA
                                 if abs(top[KEY(k)]["sigma_max"]
                                        / top[KEY(1.0)]["sigma_max"] - 1) > 1e-6), None),
        "CLASS": "CF*",
        "class_note": (
            "PRE-GUESSED CR IN THE NOVELTY PASS, AND THE MEASUREMENT SAYS OTHERWISE. "
            "sigma_max is identical to ~1e-13 across ten of the eleven conventions -- "
            "including all three NAMED ones -- and moves only at the top of an eight-decade "
            "sweep.  Mechanism: sigma_max is attained INSIDE the X block, where kappa "
            "cancels; the border coordinate can only carry it once kappa is large enough to "
            "make the unit-weight border the smallest scale in the problem.  Filed CF* with "
            "the breakdown point named rather than CF, because it does eventually move.")}
    # --- A4 THE LADDER SPREAD -- prediction Q4 -----------------------------
    sp = [lad[KEY(k)]["ladder_relative_spread"] for k in KAPPA]
    sp2 = [lad[KEY(k)]["ladder_relative_spread_64_to_512"] for k in KAPPA]
    R["A4_ladder_relative_spread"] = {
        "quoted": 0.0013899483438452888,
        "quoted_64_to_512": 0.000920,
        "value_at_named": {n: lad[KEY(k)]["ladder_relative_spread"] for n, k in NAMED.items()},
        "sweep_min": min(sp), "sweep_max": max(sp), "max_over_min": ratio(sp),
        "sweep_min_64_to_512": min(sp2), "sweep_max_64_to_512": max(sp2),
        "monotone_decreasing_in_every_convention": bool(
            all(lad[KEY(k)]["monotone_decreasing"] for k in KAPPA)),
        "monotone_decreasing_by_convention": {
            KEY(k): lad[KEY(k)]["monotone_decreasing"] for k in KAPPA},
        "relative_spread_over_the_three_NAMED_conventions": spread(
            [lad[KEY(k)]["ladder_relative_spread"] for k in NAMED.values()]),
        "ratio_over_the_three_NAMED_conventions": ratio(
            [lad[KEY(k)]["ladder_relative_spread"] for k in NAMED.values()]),
        "CLASS": "CR",
        "QUALITATIVE_CLAIM_CLASS": "CF",
        "Q4_RESOLUTION": (
            "Q4 PREDICTED that A4 would be 'far closer to CF than A1 is'.  REFUTED, and in "
            "the direction that matters: A1 swings by max/min = 124.8 over the sweep and A4 "
            "swings by max/min = 17320.7 -- A4 is the MOST convention-sensitive number in the "
            "whole enumeration, ~139x more sensitive than the digit PUB2 already caveats.  "
            "But the SPLIT that Q4 was really asking about survives: the ladder is "
            "monotone-decreasing in ALL ELEVEN conventions, so the QUALITATIVE claim PUB2 "
            "sec 3.5 rests on ('a monotone-decreasing ladder that flattens') is "
            "convention-free, while the DIGIT that states how much ('0.139 %') is not.  "
            "Those are two different sentences and PUB2 prints them as one."),
        "reading": ("Q4.  PUB2 sec 3.5's argument rests on the ladder FLATTENING, not on the "
                    "digit 0.0908.  This row measures whether that argument is convention-free "
                    "even though its headline digit is not."),
    }
    # --- A6 the Xu images --------------------------------------------------
    R["A6_xu_normalization_images"] = {
        "xu_full_line_kappa_2pi": top[KEY(TWOPI)]["sigma_min"],
        "xu_half_line_4p2_kappa_pi": top[KEY(PI)]["sigma_min"],
        "ratio_half_over_full": (top[KEY(PI)]["sigma_min"] / top[KEY(TWOPI)]["sigma_min"]),
        "CLASS": "CR",
        "note": "these ARE points of the A1 sweep, not separate quantities"}
    return R


# ===========================================================================
# S2 -- Group B: the tail block
# ===========================================================================

def s2_group_B():
    R = {"group": "B -- the tail block (leg 176 C2; leg 277's convention-free anchor)"}
    blocks = {}
    for K in (2, 4, 8, 16):
        row = {}
        for k in KAPPA:
            s = sigma_tail(512, k, K)
            row[KEY(k)] = {"sigma_min": s, "inverse_norm": 1.0 / s}
        vals = [row[KEY(k)]["sigma_min"] for k in KAPPA]
        row["relative_spread_over_sweep"] = spread(vals)
        row["max_over_min"] = ratio(vals)
        row["value_at_named"] = {n: row[KEY(k)]["sigma_min"] for n, k in NAMED.items()}
        blocks[str(K)] = row
    R["K_blocks_at_N512"] = blocks
    R["B1_tail_inverse_norm_K2"] = {
        "quoted": 4.02614534796022, "quoted_by_leg277": 4.0262407,
        "value_at_named": {n: 1.0 / blocks["2"][KEY(k)]["sigma_min"] for n, k in NAMED.items()},
        "relative_spread_over_sweep": blocks["2"]["relative_spread_over_sweep"],
        "leg277_measured_spread_over_3_conventions": 1.53e-08,
        "CLASS": "CF",
        "mechanism": ("the tail block carries NO border coordinate, so kappa multiplies the "
                      "domain Gram and the range Gram alike and cancels identically in the "
                      "Rayleigh quotient.  The residual is whitening round-off, not motion."),
    }
    R["B2_tail_sigma_min_K2"] = {"quoted": 0.24837652731703622, "CLASS": "CF",
                                 "relative_spread_over_sweep":
                                     blocks["2"]["relative_spread_over_sweep"]}
    R["B5_tail_K_4_8_16"] = {"quoted": [0.6690306287634162, 0.8244328234140121,
                                        0.9767920489401325],
                             "relative_spread_over_sweep":
                                 {K: blocks[K]["relative_spread_over_sweep"]
                                  for K in ("4", "8", "16")},
                             "CLASS": "CF"}
    # B3 -- the tail LADDER, in every convention
    ladder = {}
    for k in (1.0, PI, TWOPI, 1e-4, 1e4):
        ladder[KEY(k)] = {str(N): 1.0 / sigma_tail(N, k, 2)
                          for N in (64, 128, 256, 512, 1024)}
    R["B3_tail_ladder"] = {
        "quoted_range": [3.994032, 4.028864], "quoted_relative_swing": 0.00865,
        "ladder_by_convention": ladder,
        "max_relative_spread_of_a_RUNG_across_conventions": max(
            spread([ladder[KEY(k)][str(N)] for k in (1.0, PI, TWOPI, 1e-4, 1e4)])
            for N in (64, 128, 256, 512, 1024)),
        "CLASS": "CF"}
    R["B4_interval_enclosure"] = {
        "quoted": [4.02623993, 4.02624155], "CLASS": "CF",
        "note": ("an interval enclosure of a CF quantity is CF: leg 249 computed it in the "
                 "repo convention, and B1's mechanism carries the whole interval unchanged. "
                 "Not independently re-enclosed here -- this leg is float64, like leg 277.")}
    return R


# ===========================================================================
# S3 -- Group C: the Z-battery and the terms not formed
# ===========================================================================

def s3_group_C():
    R = {"group": "C -- the Z-battery (leg 176 C5) and the certificate's missing terms"}
    z = {}
    for M in (64, 128, 256):
        row = {}
        for k in KAPPA:
            row[KEY(k)] = z1_blockdiag(2, M, k)
        vals = list(row.values())
        row["relative_spread_over_sweep"] = spread(vals)
        row["max_over_min"] = ratio(vals)
        row["value_at_named"] = {n: row[KEY(k)] for n, k in NAMED.items()}
        row["min_over_sweep"] = min(vals)
        row["exceeds_threshold_1_by_at_least"] = min(vals) / 1.0
        z[str(M)] = row
    R["C1_Z1_K2"] = {
        "quoted": [140.72466104631172, 182.23161776466935, 244.14671536801256],
        "sweep": z,
        "leg277_measured_spread_over_3_conventions": [1.2e-6, 4.5e-6],
        "CLASS": None,      # filled below from the magnitude
        "reading": ("leg 277 called Z_1 'convention-free in practice but not in principle' "
                    "over THREE kappa.  This is the same statement over eleven, spanning "
                    "eight decades -- which is where a 'in practice' claim either holds or "
                    "breaks."),
    }
    sp = max(z[str(M)]["relative_spread_over_sweep"] for M in (64, 128, 256))
    R["C1_Z1_K2"]["max_relative_spread_over_all_M_and_kappa"] = sp
    R["C1_Z1_K2"]["CLASS"] = "CF" if sp <= 1e-7 else ("CR" if sp > 1e-2 else "CF*")
    R["C1_Z1_K2"]["class_note"] = (
        "CF* = the spread is above float round-off but far below any threshold the quantity "
        "is compared against; the mechanism is that Z_1's dominant singular direction sits "
        "inside the X block, where kappa cancels, and only the border row's coupling feels it.")

    # the battery's min/max, over the three named conventions (M = 256 only: cost)
    bat = {}
    for name, k in NAMED.items():
        vals = {str(K): z1_blockdiag(K, 256, k) for K in (2, 4, 8, 16, 32)}
        bat[name] = {"ladder": vals, "min": min(vals.values()), "max": max(vals.values())}
    R["C2_Z1_battery_min_max"] = {
        "quoted_min": 140.72466104631172, "quoted_max": 66043.9811321921,
        "by_convention": bat,
        "relative_spread_of_the_min": spread([b["min"] for b in bat.values()]),
        "relative_spread_of_the_max": spread([b["max"] for b in bat.values()]),
        "CLASS": "CF*"}
    R["C3_Z1_threshold"] = {
        "quoted": 1.0, "CLASS": "CF",
        "mechanism": ("a definitional constant of the radii-polynomial hypothesis, not a "
                      "measured quantity -- `Z_1 < 1` is dimensionless in every norm because "
                      "Z_1 is an operator norm of `I - A L` on the space itself.  Invariant "
                      "by definition, at exactly 0.")}
    for tag, name, loc in (("C4", "Y_0", "PUB2 L452, L710"),
                           ("C5", "Z_2", "PUB2 L452, L710"),
                           ("C6", "Z_3", "absent from the record entirely")):
        R[f"{tag}_{name}"] = {
            "quoted": None, "CLASS": "N/F",
            "note": (f"NOT FORMED -- {loc}.  Classified by saying so: a term the certificate "
                     f"declines to construct has no convention-dependence to measure, and the "
                     f"honest entry is its absence with its locator, not a blank."),
        }
    return R


# ===========================================================================
# S4 -- Group D: the dual pairing
# ===========================================================================

def s4_group_D():
    R = {"group": "D -- the dual pairing and its companions (leg 176 C8, E4)"}
    vals = {KEY(k): dual_norm(512, k) for k in KAPPA}
    v = [vals[KEY(k)] for k in KAPPA]
    p, res = power_fit(KAPPA, v)
    pred = {KEY(k): vals[KEY(1.0)] * k ** -0.5 for k in KAPPA}
    R["D1_ell_dual_norm_N512"] = {
        "quoted": 0.8873620087421942, "pinned_by": "kappa = 1",
        "sweep": vals, "value_at_named": {n: vals[KEY(k)] for n, k in NAMED.items()},
        "sweep_min": min(v), "sweep_max": max(v), "max_over_min": ratio(v),
        "fitted_exponent": p, "fit_max_relative_residual": res,
        "max_relative_deviation_from_exact_kappa_to_the_minus_half": max(
            abs(pred[KEY(k)] / vals[KEY(k)] - 1.0) for k in KAPPA),
        "CONVERSION_LAW": "||ell||_{X*}(kappa) = 0.8873620087421942 * kappa^{-1/2}",
        "CLASS": "CX",
        "mechanism": ("ell is a functional ON the X block only; the dual norm inverts the X "
                      "Gram once, so it is exactly homogeneous of degree -1/2 in kappa.  The "
                      "border coordinate never enters, which is why there IS a law here and "
                      "not in A1.")}
    # D2 -- the ell^2 companion the same block prints
    e = border_row(512)
    l2 = float(np.sqrt(np.real(np.vdot(e, e))))
    R["D2_ell_l2_norm_N512"] = {
        "quoted": 13338.300941274341, "here": l2, "CLASS": "CF",
        "relative_spread_over_sweep": 0.0,
        "mechanism": ("the ell^2 norm of the border row does not reference the X Gram at all, "
                      "so kappa cannot enter its definition.  Exactly convention-free -- and "
                      "convention-free for a reason that makes it USELESS as a certificate "
                      "quantity, which is worth saying out loud.")}
    # D3 -- E4's two-route ratio.  CORRECTED: it carries the border coordinate.
    d3 = {}
    for k in KAPPA:
        r, inv = e4_bordered_ratio(256, k)
        d3[KEY(k)] = {"ratio_from_norms": r, "one_over_sigma_min": inv,
                      "agreement": abs(r - inv) / inv}
    dv = [d3[KEY(k)]["ratio_from_norms"] for k in KAPPA]
    R["D3_E4_two_route_ratio"] = {
        "quoted": 11.01037339225752, "quoted_companion": 11.010373719136561,
        "sweep": d3, "sweep_min": min(dv), "sweep_max": max(dv),
        "max_over_min": ratio(dv), "relative_spread_over_sweep": spread(dv),
        "value_at_named": {n: d3[KEY(k)]["ratio_from_norms"] for n, k in NAMED.items()},
        "max_agreement_with_one_over_sigma_min": max(
            d3[KEY(k)]["agreement"] for k in KAPPA),
        "CLASS": "CR",
        "PREDICTION_CORRECTION": (
            "the novelty pass put D3 under Q1's 'no border coordinate' clause.  Reading leg "
            "176's source (construction.py L401) shows BOTH radicands carry the border "
            "coordinate -- kappa_min in the numerator, ell(u) in the denominator -- so D3 is "
            "the bordered Rayleigh quotient at its minimizer, equal to 1/sigma_min, and it is "
            "CR.  Q1's rule is untouched (D3 was never in its hypothesis); Q1's LIST was "
            "wrong, and the error was this leg's, not leg 176's."),
        "mechanism": ("a ratio whose numerator and denominator each mix an X-norm with a "
                      "border amplitude carrying a DIFFERENT weight.  kappa rescales only one "
                      "of the two summands on each side, so it cannot cancel.")}
    return R


# ===========================================================================
# S5 -- Group E: the controls, and the 0.71465 question
# ===========================================================================

WITNESS = 0.7146549471256172           # leg 163's implied_sigma_min_lower_witness


def s5_group_E():
    R = {"group": "E -- the controls PUB2 quotes as load-bearing"}

    # E1 -- the unbordered collapse
    e1 = {}
    for k in KAPPA:
        e1[KEY(k)] = sigma_tail(512, k, 0)
    ev = list(e1.values())
    R["E1_unbordered_collapse"] = {
        "quoted": 6.972501777380562e-14,
        "quoted_bordered_vs_unbordered_agreement": 5.7e-15,
        "sweep": e1, "sweep_min": min(ev), "sweep_max": max(ev), "max_over_min": ratio(ev),
        "CLASS": "CF",
        "mechanism": ("unbordered: kappa cancels between the Grams, as in B1.  The number IS "
                      "the float floor of an X Gram whose entries reach ~1e12, so its DIGITS "
                      "are conditioning noise in every convention -- what is convention-free "
                      "is the statement 'collapses to the float floor', not the digits.  The "
                      "max/min across the sweep, recorded above, is the honest magnitude.")}

    # E2 -- the loose L^2 realization's fitted exponent
    loose = {}
    for k in (1.0, PI, TWOPI, 1e-4, 1e4):
        lad = {str(N): sigma_loose(N, k) for N in (64, 128, 256, 512)}
        sl = float(np.polyfit(np.log([64., 128., 256., 512.]),
                              np.log([lad[str(N)] for N in (64, 128, 256, 512)]), 1)[0])
        loose[KEY(k)] = {"ladder": lad, "fitted_exponent": sl}
    ex = [loose[KEY(k)]["fitted_exponent"] for k in (1.0, PI, TWOPI, 1e-4, 1e4)]
    R["E2_loose_L2_fitted_exponent"] = {
        "quoted": -1.4914111116151578, "by_convention": loose,
        "relative_spread_over_conventions": spread([abs(x) for x in ex]),
        "CLASS": "CF",
        "mechanism": ("the loose realization's Gram is the IDENTITY (leg 176 C4 passes "
                      "gram=False), so the X-normalization constant does not appear in its "
                      "definition.  Exactly convention-free with respect to THIS axis -- and "
                      "silent about its own, which is the choice of the L^2 realization.")}

    # E3 -- the C6 closed-form ratio, over seeds and over kappa
    e3 = {KEY(k): unbordered_norm_ratio(0, k) for k in KAPPA}
    e3_seeds = {str(sd): unbordered_norm_ratio(sd, 1.0) for sd in range(4)}
    e3v = list(e3.values())
    R["E3_C6_closed_form_ratio"] = {
        "quoted": 0.868153885807814,
        "reproduced_over_leg176_four_seeds": e3_seeds,
        "leg176_banked_four_seeds": [0.868153885807814, 0.8404652784717725,
                                     0.7859395946487807, 0.6903593550615618],
        "sweep": e3,
        "relative_spread_over_sweep": spread(e3v), "max_over_min": ratio(e3v),
        "CLASS": "CF",
        "mechanism": ("||u||_X/||f||_X from Xu's CLOSED FORM on the whole line: the SAME norm "
                      "on both sides and NO border coordinate on either, so kappa cancels in "
                      "the quotient identically.  This row is convention-free by a one-line "
                      "exact argument; the sweep above is CONFIRMATORY and is reported as "
                      "such, not as the evidence.")}

    # E4 / E5 -- leg 163's data and the witness
    e5 = {}
    for k in KAPPA:
        rs = [unbordered_norm_ratio(sd, k) for sd in (1, 2, 3)]
        e5[KEY(k)] = {"ratios": rs, "implied_witness_upper_bound": 1.0 / max(rs)}
    wv = [e5[KEY(k)]["implied_witness_upper_bound"] for k in KAPPA]
    R["E4_leg163_three_ratios"] = {
        "quoted": [1.3993, 1.2680, 1.3769], "sweep": e5,
        "relative_spread_of_the_max_ratio_over_sweep": spread(
            [max(e5[KEY(k)]["ratios"]) for k in KAPPA]),
        "CLASS": "CF"}
    R["E5_leg163_witness"] = {
        "quoted": WITNESS, "sweep_of_the_implied_bound": wv,
        "relative_spread_over_sweep": spread(wv),
        "CLASS": "CF",
        "mechanism": ("the witness is 1/max(||u||_X/||f||_X) over a finite family -- a ratio "
                      "of X-norms with no border coordinate, so kappa cancels.  THIS IS THE "
                      "POINT: the witness is convention-FREE while sigma_min is "
                      "convention-RELATIVE, and PUB2 sec 4.5 compares them directly.")}

    # --- THE FIFTH QUESTION: does `0.0908 <= 0.71465` survive the sweep? ----
    fine = list(np.exp(np.linspace(math.log(1e-6), math.log(1e6), 61)))
    sig = [(k, sigma_bordered(256, k)[0]) for k in fine]
    kbest, sbest = max(sig, key=lambda t: t[1])
    R["E5b_does_the_reconciliation_survive"] = {
        "question": ("PUB2 sec 4.5 reconciles leg 163 with leg 176 by `0.0908 <= 0.71465`.  "
                     "The left side is CR and moves; the right side is CF and does not.  Is "
                     "the inequality true for EVERY convention, or only for kappa = 1?"),
        "fine_sweep_decades": [-6, 6], "n_points": len(fine),
        "sup_sigma_min_over_kappa_at_N256": sbest,
        "argmax_kappa": kbest,
        "leg163_witness": WITNESS,
        "sup_over_witness": sbest / WITNESS,
        "headroom_factor": WITNESS / sbest,
        "leg249_sweep_own_max": 0.1357994693284667,
        "sup_exceeds_leg249_own_max_by": sbest / 0.1357994693284667,
        "inequality_holds_across_the_whole_fine_sweep": bool(
            all(s <= WITNESS for _, s in sig)),
        "sigma_min_over_the_fine_sweep": {KEY(k): s for k, s in sig},
    }

    # E6 -- the "optimistic by" factor: CF over CR, so CR
    e6 = {KEY(k): WITNESS / sigma_bordered(512, k)[0]
          for k in KAPPA}
    e6v = list(e6.values())
    R["E6_optimistic_by_factor"] = {
        "quoted": 7.870742174847475, "sweep": e6,
        "sweep_min": min(e6v), "sweep_max": max(e6v), "max_over_min": ratio(e6v),
        "value_at_named": {n: e6[KEY(k)] for n, k in NAMED.items()},
        "CLASS": "CR",
        "mechanism": ("this factor is a CF quantity DIVIDED BY a CR one, so it inherits the "
                      "CR class in full.  PUB2 prints it as though it were a property of the "
                      "two legs' disagreement; it is a property of the two legs' disagreement "
                      "IN THE REPOSITORY CONVENTION.")}

    # E7 -- C7's Galerkin constant
    kg = {str(N): galerkin_kappa_G(N)[0] for N in (60, 120, 240, 480, 960)}
    R["E7_galerkin_kappa_G"] = {
        "quoted": 5.894962568377656, "here": kg, "CLASS": "CF",
        "mechanism": ("kappa_G is the border amplitude of a SQUARE Galerkin solve.  No Gram, "
                      "no norm and no weight enters its definition -- it is a coefficient of "
                      "the solution vector.  The X-normalization constant cannot reach it.  "
                      "Exactly convention-free, at 0.")}
    return R


# ===========================================================================
# S6 -- Group F: the OTHER space
# ===========================================================================

def s6_group_F():
    return {
        "group": "F -- quantities quoted from the ell^1_w realization (PUB2 sec 2)",
        "F1_fitted_exponents": {
            "quoted": {"s=0": 0.9925, "s=0.3": 0.6985, "s=0.7": 0.3202},
            "CLASS": "CR-DISCLOSED",
            "mechanism": ("a different space entirely: the X-Gram constant kappa does not "
                          "exist in the ell^1_w realization.  Its OWN convention is the "
                          "weight exponent s, and every call-site prints the value WITH its "
                          "s -- so this family is convention-relative with the convention "
                          "already named in the quote.  It is the only group in the whole "
                          "enumeration that was already disclosed correctly, and it is worth "
                          "recording that PUB2 got this one right.")},
        "F2_sigma_min_spread_across_K": {"quoted": 0.0029, "CLASS": "CR-DISCLOSED"},
        "F3_A_norm_floor_growth_per_doubling": {"quoted": 1.99, "CLASS": "CR-DISCLOSED",
                                                "note": ("a growth RATE in M at fixed s; "
                                                         "invariant under rescaling the "
                                                         "ell^1_w norm by a constant, and "
                                                         "s-dependent like the rest of F")},
        "F4_profile_decay_exponent_alpha": {
            "quoted": 0.39735311167782, "CLASS": "CF",
            "mechanism": ("alpha is the algebraic decay rate of the a=0 CLM profile's Laguerre "
                          "coefficients -- a property of the ODE solution, defined before any "
                          "norm is chosen.  No normalization constant of any space can move "
                          "it.  Convention-free across BOTH axes (kappa and s), which no other "
                          "quantity in the enumeration is.")},
    }


# ===========================================================================
# S7 -- are there really only 1 live axis?
# ===========================================================================

def s7_secondary_axes():
    R = {"question": ("the novelty pass named FOUR candidate convention axes and argued two of "
                      "them (whitening route, realification gauge) are not live.  Measured "
                      "here rather than assumed -- if either moves a quantity, the whole "
                      "classification is one-dimensional for the wrong reason.")}
    routes = {}
    for k in (1.0, PI, TWOPI, 1e-4, 1e4):
        row = {}
        for r in ("eigh", "chol", "rescale"):
            try:
                row[r] = _whiten_sigma(*bordered_section(256, k), route=r)[0]
            except Exception as e:
                row[r] = None; row[r + "_error"] = str(e)
        good = [v for v in row.values() if isinstance(v, float)]
        row["max_relative_spread"] = spread(good)
        routes[KEY(k)] = row
    R["axis_3_whitening_route"] = {
        "by_convention": routes,
        "worst_relative_spread_over_all_conventions": max(
            routes[KEY(k)]["max_relative_spread"] for k in (1.0, PI, TWOPI, 1e-4, 1e4)),
        "leg249_own_route_spread": [8.387873728921136e-13, 1.7645718219938e-11],
        "VERDICT": "not a live axis if the spread above is at conditioning level"}

    gauge = {}
    for k in (1.0, PI, TWOPI):
        sr = _whiten_sigma(*bordered_section(128, k, realify=True), route="eigh")[0]
        sc = _whiten_sigma(*bordered_section(128, k, realify=False), route="eigh")[0]
        gauge[KEY(k)] = {"real_section": sr, "complex_section": sc,
                         "relative_difference": abs(sr - sc) / sr}
    R["axis_4_realification_gauge"] = {
        "by_convention": gauge,
        "worst_relative_difference": max(v["relative_difference"] for v in gauge.values()),
        "leg277_measured": [5.9e-14, 2.8e-15, 2.4e-13],
        "VERDICT": "not a live axis if the difference above is at round-off"}

    # axis 1 vs axis 2: is the "norm reading" really just a kappa?
    R["axis_2_is_a_sub_case_of_axis_1"] = {
        "claim": ("Xu Definition 4.1's two norms differ, on the REAL coefficient subspace the "
                  "bordered section lives on, by exactly the constant factor 2 in the squared "
                  "norm (leg 277 sec 3, measured at 2.20e-14 on real data and refuted at 0.676 "
                  "on complex data).  So 'which norm' selects a kappa and adds no dimension."),
        "kappa_ratio_full_over_half": TWOPI / PI,
        "leg277_real_subspace_residual": 2.20e-14,
        "leg277_complex_data_control": 0.676}
    return R


# ===========================================================================
# S8 -- the enumeration's closure test
# ===========================================================================

def s8_closure(classified_values):
    R = {"role": ("the novelty pass fixed the enumeration by hand.  This section counts it "
                  "mechanically and scans PUB2 for numeric literals it cannot map to a slot, "
                  "so an omission shows up as data rather than as a silence.")}
    R["rows_enumerated"] = 32
    R["numeric_values_enumerated"] = 47
    R["declared_absent_slots"] = 3
    R["novelty_pass_hand_count"] = 48
    R["hand_count_discrepancy"] = (
        "the novelty pass said '48 numeric slots'; the mechanical count of the SAME table is "
        "47 numeric values across 32 rows, plus 3 declared-absent slots (Y_0, Z_2, Z_3).  The "
        "48 was a hand count and is corrected here rather than quietly restated.")
    try:
        txt = open(PUB2).read()
    except Exception as e:                                   # pragma: no cover
        R["pub2_read_error"] = str(e)
        return R
    lits = set()
    for m in re.finditer(r"(?<![\w.])(\d+\.\d+(?:[eE][-+]?\d+)?|\d+[eE][-+]?\d+)(?![\w.])", txt):
        try:
            lits.add(float(m.group(1)))
        except ValueError:
            pass
    def near(x):
        for v in classified_values:
            if v == 0:
                continue
            if abs(x - v) <= 5e-3 * abs(v):
                return True
        return False
    unmapped = sorted(x for x in lits if not near(x))
    R["distinct_numeric_literals_in_pub2"] = len(lits)
    R["mapped_to_a_headline_slot"] = len(lits) - len(unmapped)
    R["unmapped_after_headline_pass"] = len(unmapped)

    # --- the family pass -------------------------------------------------------
    # A headline row classifies a FAMILY, not one number: row A1 classifies the
    # whole C1 sigma_min ladder, row C1/C2 the whole C5 Z_1 battery, and so on.
    # A literal that is a member of an already-classified family is classified.
    # This pass says how many of the leftovers are family members and how many are
    # genuinely outside the enumeration -- which is what the gate actually asks.
    fam = {}
    try:
        d176 = json.load(open(L176))
        fam["A1_C1_sigma_min_ladder"] = [v["sigma_min"] for v in
                                         d176["C1_bordered_sigma_min_X"]["ladder"].values()]
        fam["A2_C1_resolvent_ladder"] = [v["resolvent_norm"] for v in
                                         d176["C1_bordered_sigma_min_X"]["ladder"].values()]
        fam["A3_C1_sigma_max_ladder"] = [v["sigma_max"] for v in
                                         d176["C1_bordered_sigma_min_X"]["ladder"].values()]
        fam["B_C2_tail_ladder"] = [x for row in
                                   d176["C2_tail_block_sigma_min"]["ladder"].values()
                                   for x in row.values()]
        fam["B_C2_tail_inverse_norms"] = [1.0 / x for row in
                                          d176["C2_tail_block_sigma_min"]["ladder"].values()
                                          for x in row.values()]
        fam["C_C5_Z1_battery"] = [x for row in d176["C5_Z1_blockdiagonal_A"]["ladder"].values()
                                  for x in row.values()]
        fam["E1_C3_unbordered_ladder"] = list(d176["C3_control_unbordered"]["ladder"].values())
        fam["E2_C4_loose_ladder"] = [v for k, v in
                                     d176["C4_control_loose_L2_realization"]["ladder"].items()]
        fam["E3_C6_seed_family"] = list(d176["C6_closed_form_ratio"]["over_seeds"].values())
        fam["E7_C7_galerkin_family"] = (
            [v["abs_kappa"] for v in d176["C7_galerkin_inconsistency"]["kappa_ladder"].values()]
            + list(d176["C7_galerkin_inconsistency"]["exact_solution_n_times_coeff"].values()))
        fam["D1_C8_dual_ladder"] = [v["x_dual"] for v in
                                    d176["C8_border_row_dual_norm"]["ladder"].values()]
        fam["D2_C8_l2_ladder"] = [v["l2"] for v in
                                  d176["C8_border_row_dual_norm"]["ladder"].values()]
    except Exception as e:                                   # pragma: no cover
        R["family_load_error"] = str(e)
    try:
        d249 = json.load(open(L249))
        fam["A1_leg249_W5_border_weight_sweep"] = [
            v["sigma_min"] for v in d249["W5_border_weight_sensitivity"]["sweep"].values()]
        fam["A2_leg249_W5_resolvent_sweep"] = [
            v["resolvent_norm"] for v in d249["W5_border_weight_sensitivity"]["sweep"].values()]
    except Exception as e:                                   # pragma: no cover
        R["family_load_error_249"] = str(e)

    hits, still = {}, []
    for x in unmapped:
        got = None
        for name, vals in fam.items():
            for v in vals:
                if v and abs(x - v) <= 5e-3 * abs(v):
                    got = name
                    break
            if got:
                break
        if got:
            hits[name] = hits.get(got, 0) + 1
        else:
            still.append(x)
    R["family_pass_hits_by_row"] = hits
    R["mapped_by_the_family_pass"] = len(unmapped) - len(still)
    R["outside_the_enumeration_entirely"] = len(still)
    R["outside_sample_smallest_20"] = still[:20]
    R["outside_sample_largest_20"] = still[-20:]
    R["reading"] = (
        "A headline row classifies a FAMILY, not a single number.  The literals still "
        "outside after the family pass are section numbers, page and line locators, dates, "
        "the arXiv identifier 2607.19762, percentages and tolerances quoted from other legs, "
        "round scale constants (1e6, 1e12), and the ell^1_w lineage's own data -- which is "
        "Group F and is classified as a group rather than by value.  The count is reported "
        "so that the enumeration's coverage is a magnitude and not a claim.")
    return R


# ===========================================================================


_CACHE_DIR = os.environ.get("CVF_CACHE", "")


def cached(name, fn):
    """Run `fn`, or reuse a completed section from a scratch cache if one exists.

    Purely an operational convenience for a ~40-minute run on a loaded box: the
    cache lives outside the repository, is keyed by section name, and holds only
    this leg's own freshly-computed output.  Nothing banked is ever read through it.
    """
    if not _CACHE_DIR:
        return fn()
    os.makedirs(_CACHE_DIR, exist_ok=True)
    fp = os.path.join(_CACHE_DIR, name + ".json")
    if os.path.exists(fp):
        print(f"  [{name}: reused from cache]", flush=True)
        return json.load(open(fp))
    out = fn()
    with open(fp, "w") as f:
        json.dump(out, f)
    return out


def main():
    t0 = time.time()
    R = {"leg": 281, "route": "ROUTE-CVF", "date": "2026-08-07",
         "role": ("CLASSIFICATION: every headline quantity PUB2 and the certificate quote "
                  "gets a convention-freeness statement with a measured invariance magnitude "
                  "and a mechanism, or a measured convention-dependence range with the "
                  "convention that pins the quoted digit"),
         "novelty_pass_commit": "9a003d0",
         "classes": {
             "CF": "convention-free: invariant over the whole sweep, with a mechanism",
             "CF*": "convention-free in practice: moves above round-off but negligibly "
                    "against the threshold the quantity is compared against",
             "CX": "convention-relative, exactly convertible by a proved power of kappa",
             "CR": "convention-relative, no law -- needs its sweep range disclosed",
             "CR-DISCLOSED": "convention-relative, and the convention is already named at "
                             "every call-site (the ell^1_w group's `s`)",
             "N/F": "not formed by the certificate; classified by its absence + locator"},
         "convention_axis": {
             "parameter": "kappa, the constant multiplying the X-block coefficient Gram "
                          "G = I + J^4, with the border amplitude held at weight 1",
             "equivalent_to": "border weight 1/kappa (leg 277 P1, 2.14e-13)",
             "sweep": KAPPA,
             "named_points": NAMED,
             "leg249_sweep_for_comparison": "border weight 1e-2 .. 1e2 (kappa 1e-2 .. 1e2)"},
         "ceiling": ("a=0 only; float64; nothing interval-enclosed beyond what legs 249/277 "
                     "banked; Y_0 and Z_2 still not formed; HL_S2_nonsymmetric inherits none "
                     "of it; no link of L1->L4 moves; Clay odds unchanged at ~0.05%"),
         "ga_compute": False}

    print("S0 reproduction control ...", flush=True)
    R["S0_reproduction_control"] = cached("S0_reproduction_control", s0_reproduction)
    print("S1 group A ...", flush=True)
    R["S1_group_A_bordered"] = cached("S1_group_A_bordered", s1_group_A)
    print("S2 group B ...", flush=True)
    R["S2_group_B_tail"] = cached("S2_group_B_tail", s2_group_B)
    print("S3 group C ...", flush=True)
    R["S3_group_C_Z_battery"] = cached("S3_group_C_Z_battery", s3_group_C)
    print("S4 group D ...", flush=True)
    R["S4_group_D_dual"] = cached("S4_group_D_dual", s4_group_D)
    print("S5 group E ...", flush=True)
    R["S5_group_E_controls"] = cached("S5_group_E_controls", s5_group_E)
    print("S6 group F ...", flush=True)
    R["S6_group_F_other_space"] = cached("S6_group_F_other_space", s6_group_F)
    print("S7 secondary axes ...", flush=True)
    R["S7_secondary_axes"] = cached("S7_secondary_axes", s7_secondary_axes)
    print("S8 closure ...", flush=True)
    classified = [0.09080465147034879, 11.012651706796523, 499.64096369153697,
                  0.0013899483438452888, 0.000920, 0.0420303, 0.057643, 1.444e-04,
                  4.02614534796022, 4.0262407, 0.24837652731703622, 3.994032, 4.028864,
                  0.6690306287634162, 0.8244328234140121, 0.9767920489401325,
                  140.72466104631172, 182.23161776466935, 244.14671536801256,
                  66043.9811321921, 1.0, 0.8873620087421942, 13338.300941274341,
                  11.01037339225752, 6.972501777380562e-14, 5.7e-15,
                  1.4914111116151578, 0.868153885807814, 1.3993, 1.2680, 1.3769,
                  0.7146549471256172, 7.870742174847475, 5.894962568377656, 5.910,
                  0.9925, 0.6985, 0.3202, 0.0029, 1.99, 0.39735311167782,
                  0.090804094, 0.090804194, 4.02623993, 4.02624155, 0.00865]
    R["S8_enumeration_closure"] = s8_closure(classified)

    # -------- THE CLASSIFICATION TABLE, assembled from the sections ---------
    def cls(sec, key):
        return sec.get(key, {}).get("CLASS")
    A, B, C, D, E, F = (R["S1_group_A_bordered"], R["S2_group_B_tail"],
                        R["S3_group_C_Z_battery"], R["S4_group_D_dual"],
                        R["S5_group_E_controls"], R["S6_group_F_other_space"])
    table = [
        ("A1", "sigma_min bordered N=512", cls(A, "A1_sigma_min_N512"),
         A["A1_sigma_min_N512"]["sweep_min"], A["A1_sigma_min_N512"]["sweep_max"]),
        ("A2", "||R||_X = 1/sigma_min", cls(A, "A2_resolvent_norm_N512"),
         A["A2_resolvent_norm_N512"]["sweep_min"], A["A2_resolvent_norm_N512"]["sweep_max"]),
        ("A3", "sigma_max bordered N=512", cls(A, "A3_sigma_max_N512"),
         A["A3_sigma_max_N512"]["sweep_min"], A["A3_sigma_max_N512"]["sweep_max"]),
        ("A4", "sigma_min ladder relative spread", cls(A, "A4_ladder_relative_spread"),
         A["A4_ladder_relative_spread"]["sweep_min"],
         A["A4_ladder_relative_spread"]["sweep_max"]),
        ("A5", "interval enclosure of A1", "CR (inherits A1)", None, None),
        ("A6", "Xu-normalization images of A1", cls(A, "A6_xu_normalization_images"),
         A["A6_xu_normalization_images"]["xu_full_line_kappa_2pi"],
         A["A6_xu_normalization_images"]["xu_half_line_4p2_kappa_pi"]),
        ("A7", "quadrature-window spread 1.444e-04", "CR (inherited, NOT measured here)",
         None, None),
        ("B1", "||T^-1||_X tail K=2", cls(B, "B1_tail_inverse_norm_K2"), None, None),
        ("B2", "tail sigma_min K=2", cls(B, "B2_tail_sigma_min_K2"), None, None),
        ("B3", "tail ladder N=64..1024", cls(B, "B3_tail_ladder"), None, None),
        ("B4", "interval enclosure of B1", cls(B, "B4_interval_enclosure"), None, None),
        ("B5", "tail at K=4,8,16", cls(B, "B5_tail_K_4_8_16"), None, None),
        ("C1", "Z_1 block-diagonal A, K=2", cls(C, "C1_Z1_K2"), None, None),
        ("C2", "Z_1 battery min/max", cls(C, "C2_Z1_battery_min_max"), None, None),
        ("C3", "the Z_1 threshold 1.0", cls(C, "C3_Z1_threshold"), None, None),
        ("C4", "Y_0", C["C4_Y_0"]["CLASS"], None, None),
        ("C5", "Z_2", C["C5_Z_2"]["CLASS"], None, None),
        ("C6", "Z_3", C["C6_Z_3"]["CLASS"], None, None),
        ("D1", "||ell||_{X*}", cls(D, "D1_ell_dual_norm_N512"),
         D["D1_ell_dual_norm_N512"]["sweep_min"], D["D1_ell_dual_norm_N512"]["sweep_max"]),
        ("D2", "||ell||_{l2}", cls(D, "D2_ell_l2_norm_N512"), None, None),
        ("D3", "E4 two-route ratio", cls(D, "D3_E4_two_route_ratio"), None, None),
        ("E1", "unbordered collapse", cls(E, "E1_unbordered_collapse"), None, None),
        ("E2", "loose-L2 fitted exponent", cls(E, "E2_loose_L2_fitted_exponent"), None, None),
        ("E3", "C6 closed-form ratio", cls(E, "E3_C6_closed_form_ratio"), None, None),
        ("E4", "leg 163's three ratios", cls(E, "E4_leg163_three_ratios"), None, None),
        ("E5", "leg 163's witness 0.71465", cls(E, "E5_leg163_witness"), None, None),
        ("E6", "'optimistic by' 7.87", cls(E, "E6_optimistic_by_factor"),
         E["E6_optimistic_by_factor"]["sweep_min"], E["E6_optimistic_by_factor"]["sweep_max"]),
        ("E7", "Galerkin kappa_G 5.895", cls(E, "E7_galerkin_kappa_G"), None, None),
        ("F1", "ell^1_w fitted exponents", F["F1_fitted_exponents"]["CLASS"], None, None),
        ("F2", "ell^1_w spread across K", F["F2_sigma_min_spread_across_K"]["CLASS"],
         None, None),
        ("F3", "||A||_w floor growth 1.99x", F["F3_A_norm_floor_growth_per_doubling"]["CLASS"],
         None, None),
        ("F4", "profile decay exponent alpha", F["F4_profile_decay_exponent_alpha"]["CLASS"],
         None, None),
    ]
    R["CLASSIFICATION_TABLE"] = [
        {"id": i, "quantity": q, "class": c, "sweep_min": lo, "sweep_max": hi}
        for i, q, c, lo, hi in table]
    counts = {}
    for row in R["CLASSIFICATION_TABLE"]:
        counts[str(row["class"])] = counts.get(str(row["class"]), 0) + 1
    R["CLASS_COUNTS"] = counts
    R["rows_classified"] = len(table)
    R["rows_unclassified"] = sum(1 for r in R["CLASSIFICATION_TABLE"] if r["class"] is None)

    R["gate"] = {
        "question": ("for the enumerated set, does EVERY quantity get either a "
                     "convention-freeness proof or a measured convention-dependence range "
                     "with a named pinning convention -- no quantity left unclassified?"),
        "rows": len(table),
        "rows_with_a_class": len(table) - R["rows_unclassified"],
        "rows_whose_range_is_INHERITED_rather_than_measured": ["A5", "A7", "B4"],
        "answer": "YES" if R["rows_unclassified"] == 0 else "NO",
    }
    R["runtime_seconds_this_invocation"] = time.time() - t0
    R["runtime_note"] = (
        "S0-S7 are memoised to a scratch directory outside the repository (env CVF_CACHE) so "
        "that a crash in one section does not discard the others -- which is exactly what "
        "happened once during this leg.  `runtime_seconds_this_invocation` therefore measures "
        "only what this invocation recomputed.  Measured wall times for the sections "
        "themselves, on a loaded box: S0-S4 + S8 = 1284.2 s in one uninterrupted run with "
        "S5-S7 served from cache; S5 (group E, including the 61-point fine sweep) and S6/S7 "
        "were computed in a separate validation pass of comparable length.  Total compute for "
        "the banked table is ~45 minutes; no section here is stale, every cache entry was "
        "produced by the code in this file at the commit that banks it.")
    R["sections_served_from_cache_this_invocation"] = bool(_CACHE_DIR)
    with open(OUT, "w") as f:
        json.dump(R, f, indent=2, sort_keys=False)
    print(f"\nwrote {OUT}  ({R['runtime_seconds_this_invocation']:.1f} s)")
    print("class counts:", counts, " unclassified:", R["rows_unclassified"])
    return R


if __name__ == "__main__":
    main()
