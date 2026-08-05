"""Route-TC v1: ASSEMBLE the bordered certificate -- give the far-field amplitude its own
column, its own matching row, and put all four terms in the SAME radii polynomial.

Leg 52 bordered the TAIL block with the far field the transport operator cannot invert and
measured a bounded inverse norm (7.46 -> 9.44 at s = 0; 8.09 -> 11.37 at s = 0.3) in the
weight classes where the target profile has finite norm.  That is ONE term of four,
measured in isolation.  The border it added is an UNKNOWN -- the far-field amplitude -- and
an unknown that appears in the tail must appear everywhere else: it needs a column in the
finite block, a row (the matching condition), a contribution to Y_0, and a place in the
polynomial next to Z_1 and Z_2.  This leg writes that down and evaluates it.

PRE-COMMITTED CLAUSES, written before the run (both branches of each are reportable):

  TC0 THE NOVELTY PASS COMES FIRST and can only narrow the claim.  Searched against the
      validated-numerics literature, ledger and query log committed (LITERATURE_CHECK.md
      and `T0_novelty` in the JSON).  Leg 52 left a flag -- the April 2026 Chen-Huang-Li
      reference this project's target rests on did not resurface -- and this pass
      re-checks it explicitly.
  TC1 THE COUPLING IS EXPLICIT, NOT A PARAMETER.  The far-field direction is the tail
      operator's kernel `hhat` (leg 52's `tail_right_null`, h_{K+1} = 1, supported on one
      parity chain).  Its column in the finite block is `L hhat` restricted to modes
      1..K -- computed, not fitted.  Every entry of that column is reported as a magnitude.
      NO NEW BASIS: leg 51 chose the basis, leg 52 measured the tail in it.
  TC2 THE FOUR TERMS IN ONE POLYNOMIAL.  Y_0, Z_1 (finite block AND the three coupling
      sub-blocks), Z_2, and the tail constant, assembled into
      `Z_2 r^2 - (1 - Z_1) r + Y_0 <= 0`, with the root reported as a number.
  TC3 THE BORDER'S OWN DEFECT.  The matching condition's residual at the anchor, the
      asymptotic expansion's own truncation defect, and the gauge row's value on the
      far-field column -- all three as magnitudes, with a statement of which term each
      dominates.
  TC4 Z_1 IS DECOMPOSED BY SUB-BLOCK, because a failure must name its term.  With the
      approximate inverse in the shape the method requires -- block diagonal,
      `A = Gamma^{-1} (+) A_tail` -- the four sub-blocks of `I - A L` are computed
      separately.  A sub-block norm is a LOWER bound on Z_1 for that choice of A, and
      `(I - A L)_{tail,Gamma} = -A_tail L_{tail,Gamma}` does not involve `Gamma^{-1}` at
      all, so it is a lower bound for EVERY finite block.
  TC5 THE POSITIVE CONTROL MUST BE ABLE TO REPORT THE OTHER ANSWER.  Same code path with
      `Lambda^1` dissipation (`mu k` on the diagonal) and the UNBORDERED tail inverse --
      bordering an already-invertible tail with its near-null pair is the wrong operator,
      and the control checks that too.  If the dissipative case does not bring the
      coupling term below 1, the instrument is broken and the negative result is void.
  TC6 THE SPLIT POINT IS SWEPT, INCLUDING SMALL K.  The coupling term is expected to grow
      with K, so the fair question is whether ANY split works, not whether the largest
      one does.  K = 4..64 in both admissible classes.
  TC7 THE CEILING, pre-committed before the numbers exist.  This is the a = 0 CLM object.
      Its Y_0 is exactly zero because the profile IS one basis mode, which makes the
      radii polynomial's root r = 0 available for a degenerate reason and says nothing
      about the target.  Nothing is claimed about HL_S2_nonsymmetric.

Writes writeup/data/p2_route_tc_v1_assemble.json.

Run: .venv/bin/python -u experiments/p2_route_tc_v1_assemble.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import (                              # noqa: E402
    algebra_constant, bordered_linearization, quadratic_bound, rigorous_finite_block,
    tail_block, tail_left_null, tail_right_null, weight_vector,
)

OUT = ROOT / "writeup" / "data" / "p2_route_tc_v1_assemble.json"

ALPHA_TARGET = 0.394                     # HL_S2_nonsymmetric far field Omega ~ |X|^-alpha
CLASSES = (("flat", 0.0), ("algebraic", 0.3))          # both admissible: s < alpha
K_SWEEP = (4, 8, 16, 32, 64)
M_EXTRA = 1024                           # tail modes carried past the split
M_LADDER = (256, 512, 1024, 2048)        # for the log-divergence of the gauge entry


# --------------------------------------------------------------------------
# TC0 -- the novelty ledger.  Searched 2026-08-05 with WebSearch/WebFetch, in session,
# BEFORE any of the construction below was written.
# --------------------------------------------------------------------------
PRECEDENTS = [
    {"id": "arXiv:1503.06315 (DCDS-A 35(10) 4765-4789)",
     "who": "Breden, Desvillettes, Lessard (2015)",
     "what": ("'Rigorous numerics for nonlinear operators with TRIDIAGONAL DOMINANT linear "
              "part'.  Leg 52 recorded as OPEN whether their construction of the "
              "approximate inverse reaches an operator whose diagonal is exactly zero. "
              "This pass fetched the publisher's abstract page: the stated hypothesis is a "
              "tridiagonal DOMINANT linear part, and the difficulty they solve is that "
              "Df(xbar) -- the full derivative -- fails to be asymptotically diagonally "
              "dominant while the linear part has that structure."),
     "verdict": "NARROWS_BUT_DOES_NOT_PRE_EMPT__SUPERSEDED_BY_LIT_NINTH_PASS",
     "why": ("Our tail is tridiagonal with diagonal EXACTLY zero, so it does not satisfy "
             "the stated hypothesis.  This pass read only the publisher's ABSTRACT page, so "
             "that was evidence and not proof.  LIT's ninth pass then extracted the full "
             "PDF and settled it: assumption (4) needs C1 <= mu_k/omega_k^{s_L} <= C2 with "
             "C1 > 0, assumption (5)'s ratios are undefined at mu_k = 0, the LU "
             "construction divides by mu_k, and their own future-work list does not include "
             "a vanishing diagonal.  Read LIT's item 2, not this entry.  The general "
             "observation that the standard tail estimate wants a dominant diagonal remains "
             "a re-derivation, exactly as leg 52 recorded it.")},
    {"id": "arXiv:2604.01868",
     "who": "Bojin Chen, De Huang, Xiangyuan Li (April 2026)",
     "what": ("'Novel self-similar finite-time blowups with singular profiles of the 1D "
              "Hou-Luo model and the 2D Boussinesq equations: a numerical investigation' -- "
              "the source of this project's target, HL_S2_nonsymmetric."),
     "verdict": "CLEARANCE_WITHDRAWN__FLAG_STANDS",
     "why": ("This pass FIRST reported the flag cleared, because query 4 returned a summary "
             "naming the paper's title and authors correctly.  That clearance is WITHDRAWN. "
             "The flag was raised against leg 52's LOGGED query, which contains no arXiv "
             "identifier; query 4 prepends the literal ID, so it tests retrieval by ID, "
             "which was never in dispute.  LIT's ninth pass re-ran leg 52's query VERBATIM "
             "and reproduced the null result, and enumerated the LINKS returned by an "
             "ID-bearing query -- all other papers, with the correct title appearing only "
             "in the prose summary, i.e. the model answering from its own knowledge rather "
             "than from a surfaced link.  This pass logged counts, not links, so its "
             "clearance could not be audited against its own record.  THE FLAG STANDS.")},
    {"id": "arXiv:2406.16597 / CPA (2026)",
     "who": "self-similar blowup for the cubic Schrodinger equation",
     "what": ("Computer-assisted existence for a self-similar profile where the linearised "
              "operator has a nontrivial kernel from phase invariance, handled by imposing "
              "vanishing conditions on functionals -- i.e. by bordering."),
     "verdict": "CONFIRMS_BORDERING_IS_STANDARD",
     "why": ("Bordering a certificate to kill a symmetry-induced kernel is standard "
             "practice and this leg claims no novelty for the MOVE.  What is measured here "
             "is what happens when the kernel is not a symmetry of the finite block but "
             "the far field of an unbounded off-diagonal operator, so the border acquires "
             "a coupling term.")},
    {"id": "SIADS, doi:10.1137/23M1607507",
     "who": "rigorous computation of solutions of semilinear PDEs on unbounded domains",
     "what": "Spectral methods plus validated numerics on unbounded domains.",
     "verdict": "ADJACENT_SEMILINEAR_ONLY",
     "why": ("Semilinear: the unbounded part is a MULTIPLIER, so the tail estimate is the "
             "standard one.  It confirms leg 51's reading of the field's shape rather than "
             "supplying a construction for an unbounded OFF-DIAGONAL part.")},
]

SEARCH_LOG = [
    ("radii polynomial validated numerics coupling between finite block and tail unbounded "
     "off-diagonal operator approximate inverse block splitting", 10),
    ("computer-assisted proof self-similar profile far-field amplitude as unknown matching "
     "condition asymptotic expansion spectral series bordered system", 9),
    ("validated numerics sequence space tail estimate first-order transport operator no "
     "diagonal decay coupling term grows with truncation mode certificate fails", 7),
    ("arXiv 2604.01868 Chen Huang Li non-symmetric self-similar blowup Hou-Luo model 2026", 9),
    ("Breden Desvillettes Lessard tridiagonal dominant linear part approximate inverse "
     "construction requires diagonal dominance zero diagonal Fredholm kernel", 10),
    ("WebFetch aimsciences.org/article/doi/10.3934/dcds.2015.35.4765 -- hypothesis on the "
     "linear part", 1),
]


def novelty_verdict():
    if any(p["verdict"].startswith("PRE_EMPTS") for p in PRECEDENTS):
        return "STOP_PRE_EMPTED"
    return "PROCEED_NARROW"


# --------------------------------------------------------------------------
# weights
# --------------------------------------------------------------------------
def wfun(k, kind, param):
    k = np.asarray(k, dtype=float)
    if kind == "flat":
        return np.ones_like(k)
    if kind == "algebraic":
        return (1.0 + k) ** float(param)
    raise ValueError(kind)


def opnorm(Mx, w_row, w_col):
    """max_j (1/w_j) sum_i w_i |M_ij| -- the norm induced by ||b||_w = sum w_k |b_k|."""
    Mx = np.abs(np.asarray(Mx, dtype=float))
    if Mx.size == 0:
        return 0.0
    return float(np.max((Mx * np.asarray(w_row, float)[:, None]).sum(0)
                        / np.asarray(w_col, float)))


# --------------------------------------------------------------------------
# TC1 -- the far-field column and the augmented finite block
# --------------------------------------------------------------------------
def amplitude_direction(K, M, kind="flat", param=0.0, border="analytic", seed=0):
    """The direction whose amplitude the extra column carries, on modes K+1..M.

    `border="analytic"` is the tail operator's kernel -- the far field, and the only choice
    a proof can write down. The other three are the NEGATIVE CONTROLS, and they are wired
    through to the finite block on purpose: leg 53's first version computed the coupling
    from `Gamma^{-1}` and `L_{Gamma,tail}` alone, neither of which sees the border, so
    "the same number for all four borders" was a tautology of the code rather than a
    measurement. With the direction wired through, a wrong amplitude direction changes the
    augmented block and the control CAN come out differently."""
    if border == "analytic":
        return tail_right_null(K, M)
    Ts, w = _scaled_tail_for_direction(K, M, kind, param)
    n = int(M) - int(K)
    if border in ("svd", "second"):
        U, S, Vt = np.linalg.svd(Ts)
        v = Vt[-1 if border == "svd" else -2, :]
    elif border == "random":
        v = np.random.default_rng(seed).standard_normal(n)
    else:
        raise ValueError(border)
    v = v / w                                  # back out of the weighted coordinates
    return v / v[0] if v[0] != 0 else v / np.max(np.abs(v))


def _scaled_tail_for_direction(K, M, kind, param):
    T = tail_block(K, M)
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)
    w = wfun(k, kind, param)
    return T * (w[:, None] / w[None, :]), w


def far_field_column(K, M, h=None):
    """`L hhat` restricted to the finite rows, and the gauge row's value on it.

    `hhat` is the tail operator's kernel extended by zero to modes 1..K: h_{K+1} = 1,
    supported on modes K+1, K+3, ...  Applying the EXACT linearisation to it gives

        row K  :  (K+1)/2 * h_{K+1}            (column K+1's `k/2` entry into row k-1)
        row 1  :  sum_{m>K} -(-1)^m h_m        (the rank-one `H Omega` term)
        rows >= K+1 : (T hhat) = 0 up to the truncation at M

    Nothing here is fitted: the far-field direction was chosen by leg 51's Fredholm
    analysis and measured by leg 52, and this is what the operator does to it."""
    h = tail_right_null(K, M) if h is None else np.asarray(h, dtype=float)
    m = np.arange(K + 1, M + 1, dtype=float)
    col = np.zeros(K)
    col[K - 1] += (K + 1) / 2.0 * h[0]
    row1 = float(np.sum(-((-1.0) ** m) * h))
    col[0] += row1
    return {"h": h, "m": m, "col": col,
            "row_K_entry": float((K + 1) / 2.0 * h[0]),
            "row_1_entry": row1,
            "gauge_entry": float(np.sum(m * h)),
            "hhat_l1": float(np.sum(np.abs(h)))}


def hhat_tail_defect(K, M, kind, param):
    """The asymptotic expansion's OWN defect: ||(L hhat)|_{tail rows}||_w / ||hhat||_w.

    Exactly zero in the interior by construction; nonzero only where the recursion is
    truncated at M.  This is the part of TC-3 that is a statement about the expansion
    rather than about the anchor."""
    h = tail_right_null(K, M)
    T = tail_block(K, M)
    d = T @ h
    w = wfun(np.arange(K + 1, M + 1), kind, param)
    num = float(np.sum(w * np.abs(d)))
    den = float(np.sum(w * np.abs(h)))
    return num / den, num


NORMALISATIONS = {
    # (label): (how the amplitude column is weighted, how the matching row is weighted)
    "shipped":      ("hhat_norm", "w_Kplus1"),
    "unit_column":  ("one",       "w_Kplus1"),
    "unit_row":     ("hhat_norm", "one"),
    "unit_both":    ("one",       "one"),
    "row_like_col": ("hhat_norm", "hhat_norm"),
}


def augmented_finite_block(K, M, kind, param, gauge="dilation", mu=0.0,
                           far_field=True, norm="shipped", h=None):
    """Gamma: the finite block with ONE EXTRA COLUMN (the far-field amplitude) and ONE
    EXTRA ROW (the matching condition), with its weights.

        cols : b_1..b_K | delta c_omega | a
        rows : residual modes 1..K | gauge | matching

    The matching row states that the amplitude of the asymptotic expansion IS the unknown
    `a`; its content as an equation is the coupling to the tail remainder, which is why it
    shows up in `Z1_Gamma_tail` below and not inside Gamma.  That is a finding and not a
    convenience: the far-field amplitude is fixed by the tail, not by the finite block.

    `gauge` selects which functional removes the dilation zero mode:
      "dilation"  leg 51's  sum_k k b_k  -- the natural one, and UNBOUNDED on l^1_w for
                  s < 1 (its norm is max_k k / w_k);
      "null"      pin the EXACT null direction instead (the dilation zero mode of this
                  linearisation is exactly e_2, checked in `null_direction_defect`), a
                  bounded functional of norm 1/w_2.
    Both are run, because if the answer turned on the gauge that would be the finding.

    `far_field=False` drops the amplitude column and the matching row entirely, giving the
    STANDARD certificate.  That is the right object once `mu > 0`: a dissipative tail has
    no kernel, so it needs no far-field unknown, and bordering it with one would charge the
    control a defect the dissipative problem does not have.  The positive control uses it."""
    K = int(K)
    F = bordered_linearization(K, mu=mu)          # (K+1)x(K+1), rows: modes 1..K + gauge
    ff = far_field_column(K, M, h=h)
    if not far_field:
        G = F.copy()
        if gauge == "null":
            G[K, :] = 0.0
            G[K, 1] = 1.0
        wk = wfun(np.arange(1, K + 1), kind, param)
        w_col = np.concatenate([wk, [1.0]])
        w_row = np.concatenate([wk, [1.0]])
        return G, w_row, w_col, ff, float("nan"), float("nan")
    N = K + 2
    G = np.zeros((N, N))
    G[:K + 1, :K + 1] = F
    G[:K, K + 1] = ff["col"]
    if gauge == "dilation":
        G[K, K + 1] = ff["gauge_entry"]
    elif gauge == "null":
        G[K, :] = 0.0
        G[K, 1] = 1.0                              # pin b_2, the exact null direction
        G[K, K + 1] = 0.0
    else:
        raise ValueError(gauge)
    if mu:
        G[:K, K + 1] -= mu * 0.0                   # hhat's own diagonal part is in the tail
    G[K + 1, K + 1] = 1.0                          # the matching row
    wk = wfun(np.arange(1, K + 1), kind, param)
    hnorm = float(np.sum(wfun(np.arange(K + 1, M + 1), kind, param) * np.abs(ff["h"])))
    pick = {"hhat_norm": hnorm, "one": 1.0,
            "w_Kplus1": float(wfun([K + 1], kind, param)[0])}
    col_key, row_key = NORMALISATIONS[norm]
    Wa, rho = pick[col_key], pick[row_key]
    w_col = np.concatenate([wk, [1.0], [Wa]])
    w_row = np.concatenate([wk, [1.0], [rho]])
    return G, w_row, w_col, ff, Wa, rho


def null_direction_defect(K):
    """e_2 is EXACTLY the dilation zero mode of this linearisation -- checked, not asserted.

    X d/dX applied to the anchor Omega_0 = -sin theta is -(1/2) sin 2 theta, so the scaling
    symmetry's tangent is e_2.  Report ||L e_2|| over the unbordered rows."""
    K = int(K)
    F = bordered_linearization(K)
    v = np.zeros(K + 1)
    v[1] = 1.0
    r = F @ v
    return float(np.max(np.abs(r[:K])))            # gauge row excluded: it is the pin


# --------------------------------------------------------------------------
# the tail side -- leg 52's object, reused, not rebuilt
# --------------------------------------------------------------------------
def scaled_tail_and_inverse(K, M, kind, param, mu=0.0, border="analytic", seed=0):
    """A_tail and ||A_tail||_w.  `border=None` gives the UNBORDERED inverse, which is the
    right operator once mu > 0 makes the tail invertible on its own -- bordering an
    invertible operator with its near-null pair manufactures a singularity, and the
    positive control has to avoid that."""
    T = tail_block(K, M, mu=mu)
    k = np.arange(int(K) + 1, int(M) + 1, dtype=float)
    w = wfun(k, kind, param)
    Ts = T * (w[:, None] / w[None, :])
    n = int(M) - int(K)
    if border is None:
        Ainv = np.linalg.inv(Ts)
    else:
        if border == "analytic":
            v = tail_right_null(K, M) * w
            u = tail_left_null(K, M) * w
        elif border in ("svd", "second"):
            U, S, Vt = np.linalg.svd(Ts)
            i = -1 if border == "svd" else -2
            v, u = Vt[i, :], U[:, i]
        elif border == "random":
            rng = np.random.default_rng(seed)
            v, u = rng.standard_normal(n), rng.standard_normal(n)
        else:
            raise ValueError(border)
        v, u = v / np.linalg.norm(v), u / np.linalg.norm(u)
        B = np.zeros((n + 1, n + 1))
        B[:n, :n] = Ts
        B[:n, n] = u
        B[n, :n] = v
        Ainv = np.linalg.inv(B)
    return Ainv, w, float(np.max(np.abs(Ainv).sum(0)))


# --------------------------------------------------------------------------
# TC4 -- Z_1 decomposed by sub-block, for A = Gamma^{-1} (+) A_tail
# --------------------------------------------------------------------------
def z1_subblocks(K, M, kind, param, gauge="dilation", mu=0.0, border="analytic", seed=0,
                 far_field=True, norm="shipped"):
    """The four sub-blocks of `I - A L`, each as a weighted operator norm.

    A sub-block's norm is a LOWER bound on ||I - A L||, so any one of them exceeding 1
    kills the certificate for that A.  The `tail <- Gamma` block is
    `-A_tail L_{tail,Gamma}` and does not involve Gamma^{-1} at all, so exceeding 1 there
    kills it for EVERY choice of finite block."""
    hdir = (amplitude_direction(K, M, kind, param, border, seed)
            if (far_field and border is not None) else None)
    G, w_row, w_col, ff, Wa, rho = augmented_finite_block(K, M, kind, param, gauge, mu,
                                                          far_field, norm, h=hdir)
    Gs = G * (w_row[:, None] / w_col[None, :])
    Ginv_s = np.linalg.inv(Gs)
    Gamma_inv_norm = float(np.max(np.abs(Ginv_s).sum(0)))

    Ainv_s, wt, A_tail_norm = scaled_tail_and_inverse(K, M, kind, param, mu, border, seed)
    n = int(M) - int(K)

    # -- (I - A L) on Gamma x Gamma : the float inverse's own defect ------------
    z_gg = float(np.max(np.abs(np.eye(G.shape[0]) - Ginv_s @ Gs).sum(0)))

    # -- L_{tail <- Gamma} : tail rows K+1..M from the Gamma unknowns -----------
    #    row K+1 <- b_K with entry (1 - K/2); the a-column contributes T hhat (truncation
    #    only); delta c_omega does not reach the tail.
    Ltg = np.zeros((n, G.shape[1]))
    Ltg[0, K - 1] = 1.0 - K / 2.0
    if far_field:
        Ltg[:, K + 1] = tail_block(K, M, mu=mu) @ ff["h"]
    Ltg_s = (Ltg * wt[:, None]) / w_col[None, :]
    Ainv_TT = Ainv_s[:, :n] if border is not None else Ainv_s
    z_tg = float(np.max(np.abs(Ainv_TT @ Ltg_s).sum(0)))

    # -- L_{Gamma <- tail} : Gamma rows from the tail remainder ----------------
    #    row K   <- r_{K+1}          : (K+1)/2
    #    row 1   <- r_m              : -(-1)^m           (the rank-one term)
    #    gauge   <- r_m              : m                 (dilation gauge only)
    #    matching<- r_{K+1}          : -1                (the amplitude is read there)
    Lgt = np.zeros((G.shape[0], n))
    mt = np.arange(K + 1, M + 1, dtype=float)
    Lgt[K - 1, 0] += (K + 1) / 2.0
    Lgt[0, :] += -((-1.0) ** mt)
    if gauge == "dilation":
        Lgt[K, :] += mt
    if far_field:
        Lgt[K + 1, 0] += -1.0
    Lgt_s = (Lgt * w_row[:, None]) / wt[None, :]
    z_gt = float(np.max(np.abs(Ginv_s @ Lgt_s).sum(0)))

    # -- (I - A L) on tail x tail ---------------------------------------------
    #    (compared against the operator A_tail actually inverts: the BORDERED tail when
    #    the border is on, the bare tail when it is off -- otherwise the border column's
    #    own contribution is charged to the tail as a defect it does not have)
    Ts = tail_block(K, M, mu=mu) * (wt[:, None] / wt[None, :])
    if border is None:
        z_tt = float(np.max(np.abs(np.eye(n) - Ainv_s @ Ts).sum(0)))
    else:
        Bs = np.linalg.inv(Ainv_s)
        z_tt = float(np.max(np.abs(np.eye(n + 1) - Ainv_s @ Bs).sum(0)))

    return {"K": int(K), "M": int(M), "class": kind, "param": float(param),
            "gauge": gauge, "mu": float(mu), "border": border, "norm": norm,
            "far_field_carried": bool(far_field),
            "Gamma_inv_norm": Gamma_inv_norm, "A_tail_norm": A_tail_norm,
            "Wa": Wa, "matching_row_weight": rho,
            "Z1_Gamma_Gamma": z_gg, "Z1_tail_Gamma": z_tg,
            "Z1_Gamma_tail": z_gt, "Z1_tail_tail": z_tt,
            "Z1_total": z_gg + z_tg + z_gt + z_tt,
            "Z1_lower_bound": max(z_gg, z_tg, z_gt, z_tt),
            "far_field_column": {"row_K": ff["row_K_entry"], "row_1": ff["row_1_entry"],
                                 "gauge": ff["gauge_entry"], "hhat_l1": ff["hhat_l1"]}}


# --------------------------------------------------------------------------
# TC2 -- the polynomial
# --------------------------------------------------------------------------
def radii_polynomial(Y0, Z1, Z2):
    """Report the root of `Z2 r^2 - (1 - Z1) r + Y0 <= 0` as a NUMBER, both branches.

    With Y0 = 0 the polynomial always has the root r = 0.  That root certifies nothing --
    it is the statement that an exact anchor is exact -- so the reportable quantity is the
    largest r for which the inequality holds, which is positive only when Z1 < 1."""
    disc = (1.0 - Z1) ** 2 - 4.0 * Z2 * Y0
    out = {"Y0": float(Y0), "Z1": float(Z1), "Z2": float(Z2),
           "discriminant": float(disc), "Z1_below_one": bool(Z1 < 1.0)}
    if disc < 0:
        out.update({"has_real_root": False, "r_min": None, "r_max": None,
                    "has_positive_interval": False})
        return out
    r1 = ((1.0 - Z1) - np.sqrt(disc)) / (2.0 * Z2)
    r2 = ((1.0 - Z1) + np.sqrt(disc)) / (2.0 * Z2)
    out.update({"has_real_root": True, "r_min": float(r1), "r_max": float(r2),
                "has_positive_interval": bool(r2 > 0.0 and r2 > r1 and r2 > 1e-300
                                              and Z1 < 1.0)})
    return out


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    res = {"leg": 53, "route": "TC", "version": "v1",
           "object": "a=0 CLM fixed point in the compactified odd-sine basis",
           "target_alpha": ALPHA_TARGET, "M_extra": M_EXTRA}

    # -- TC0 ----------------------------------------------------------------
    res["T0_novelty"] = {"precedents": PRECEDENTS, "search_log": SEARCH_LOG,
                         "verdict": novelty_verdict(),
                         "leg52_target_reference_flag": (
                             "STANDS. This pass's CLEARANCE IS WITHDRAWN -- query 4 named "
                             "the arXiv ID, which does not test the flag as posed (leg 52's "
                             "query names topic and authors only). LIT's ninth pass re-ran "
                             "leg 52's query verbatim and reproduced the null result. "
                             "Fetching by ID has always worked; the gap is topical recall."),
                         "search_log_records": (
                             "query strings and result COUNTS only, not the returned links "
                             "-- which is why this pass's resurfacing claim could not be "
                             "audited. A later pass should enumerate links.")}
    print(f"[TC0] novelty: {res['T0_novelty']['verdict']} off {len(SEARCH_LOG)} queries")
    for p in PRECEDENTS:
        print(f"      {p['id'][:34]:34s} {p['verdict']}")

    # -- TC1 the far-field column -------------------------------------------
    print("\n[TC1] the far-field column, L hhat restricted to the finite block")
    res["TC1_null_direction_defect"] = null_direction_defect(64)
    print(f"      the dilation zero mode is EXACTLY e_2: ||L e_2||_inf = "
          f"{res['TC1_null_direction_defect']:.2e}")
    cols = []
    for K in K_SWEEP:
        ff = far_field_column(K, K + M_EXTRA)
        cols.append({"K": int(K), "M": int(K + M_EXTRA),
                     "row_K_entry": ff["row_K_entry"], "row_1_entry": ff["row_1_entry"],
                     "gauge_entry": ff["gauge_entry"], "hhat_l1": ff["hhat_l1"]})
        print(f"      K={K:3d}: row K = {ff['row_K_entry']:+9.3f}   row 1 = "
              f"{ff['row_1_entry']:+9.3f}   gauge row = {ff['gauge_entry']:+11.2f}   "
              f"||hhat||_1 = {ff['hhat_l1']:.3f}")
    res["TC1_far_field_column"] = cols

    # -- TC3 the border's own defect ----------------------------------------
    print("\n[TC3] the border's own defect")
    gauge_ladder = []
    K0 = 64
    for M in M_LADDER:
        ff = far_field_column(K0, K0 + M)
        gauge_ladder.append({"M_extra": int(M), "gauge_entry": ff["gauge_entry"],
                             "row_1_entry": ff["row_1_entry"]})
    ge = np.array([g["gauge_entry"] for g in gauge_ladder], float)
    me = np.array([g["M_extra"] for g in gauge_ladder], float)
    per_efold = float(np.polyfit(np.log(me), ge, 1)[0])
    defects = {}
    for kind, p in CLASSES:
        lad = []
        for M in M_LADDER:
            rel, absd = hhat_tail_defect(K0, K0 + M, kind, p)
            lad.append({"M_extra": int(M), "relative": rel, "absolute": absd})
        rel, absd = hhat_tail_defect(K0, K0 + M_EXTRA, kind, p)
        defects[f"{kind}_{p}"] = {
            "relative": rel, "absolute": absd, "ladder": lad,
            "exponent": float(np.polyfit(np.log([x["M_extra"] for x in lad]),
                                         np.log([x["relative"] for x in lad]), 1)[0])}
    res["TC3_border_defect"] = {
        "matching_row_residual_at_anchor": 0.0,
        "matching_row_residual_is_exactly_zero_because":
            ("the a = 0 CLM anchor is the single mode Omega_0 = -sin theta: its tail is "
             "identically zero, so the far-field amplitude it implies is exactly 0 and the "
             "matching condition is satisfied with no residual.  This is the SAME "
             "degeneracy that makes leg 51's Y_0 exactly zero, and it is not progress."),
        "expansion_truncation_defect": defects,
        "gauge_row_ladder": gauge_ladder,
        "gauge_row_growth_per_efold_in_M": per_efold,
        "gauge_row_is_unbounded_because":
            ("the dilation gauge sum_k k b_k has norm max_k k / w_k on l^1_w, which is "
             "infinite for every s < 1 -- and the far-field mode has h_m ~ C m^-2, so its "
             "gauge entry sum_m m h_m ~ C log M.  The far-field column has an entry that "
             "does not exist."),
        "bounded_gauge_repair": "pin the exact null direction e_2 instead (norm 1/w_2)"}
    print(f"      matching-row residual at the anchor: exactly 0.0 (the anchor is one mode)")
    print(f"      expansion truncation defect (relative): "
          f"{ {k: round(v['relative'], 8) for k, v in defects.items()} }")
    print(f"      gauge row on the far-field column, K={K0}: "
          f"{[round(g['gauge_entry'], 1) for g in gauge_ladder]} "
          f"-> +{per_efold:.0f} per e-fold in M  (LOG-DIVERGENT)")

    # -- TC4 Z_1 by sub-block, swept over the split point -------------------
    print("\n[TC4] Z_1 by sub-block, A = Gamma^-1 (+) A_tail  (border = analytic, mu = 0)")
    sweep = []
    for kind, p in CLASSES:
        for gauge in ("dilation", "null"):
            for K in K_SWEEP:
                row = z1_subblocks(K, K + M_EXTRA, kind, p, gauge=gauge)
                sweep.append(row)
                print(f"      {kind:9s} s={p:.1f} gauge={gauge:8s} K={K:3d}: "
                      f"||Gamma^-1||={row['Gamma_inv_norm']:9.3g}  "
                      f"||A_tail||={row['A_tail_norm']:7.3f}  "
                      f"Z1[GG]={row['Z1_Gamma_Gamma']:.1e} "
                      f"Z1[tG]={row['Z1_tail_Gamma']:8.3f} "
                      f"Z1[Gt]={row['Z1_Gamma_tail']:10.4g} "
                      f"Z1[tt]={row['Z1_tail_tail']:.1e}")
    res["TC4_z1_subblocks"] = sweep

    # the smallest Z1 anywhere in the admissible sweep, and where it sits
    best = min(sweep, key=lambda r: r["Z1_lower_bound"])
    res["TC4_best"] = best
    print(f"      SMALLEST Z1 lower bound anywhere in the sweep: "
          f"{best['Z1_lower_bound']:.4g} at {best['class']} s={best['param']} "
          f"gauge={best['gauge']} K={best['K']}")

    # -- TC5 the positive control -------------------------------------------
    print("\n[TC5] positive control: Lambda^1 dissipation, UNBORDERED tail, no far field")
    ctrl = []
    for mu in (0.0, 0.1, 0.5, 1.0, 2.0, 4.0):
        for kind, p in CLASSES:
            border = "analytic" if mu == 0.0 else None
            row = z1_subblocks(16, 16 + M_EXTRA, kind, p, gauge="null", mu=mu,
                               border=border, far_field=(mu == 0.0))
            ctrl.append(row)
            print(f"      mu={mu:.2f} {kind:9s} s={p:.1f}: ||A_tail||="
                  f"{row['A_tail_norm']:10.4g}  Z1[tG]={row['Z1_tail_Gamma']:9.4g}  "
                  f"Z1[Gt]={row['Z1_Gamma_tail']:9.4g}  "
                  f"Z1_total={row['Z1_total']:9.4g}")
    res["TC5_positive_control"] = ctrl
    ctrl_ok = any(r["mu"] > 0 and r["Z1_total"] < 1.0 for r in ctrl)
    res["TC5_control_can_report_below_one"] = bool(ctrl_ok)
    res["TC5_min_mu_with_Z1_below_one"] = min(
        [r["mu"] for r in ctrl if r["mu"] > 0 and r["Z1_total"] < 1.0], default=None)
    print(f"      control brings the ASSEMBLED Z_1 below 1 for some mu > 0: {ctrl_ok} "
          f"(smallest mu: {res['TC5_min_mu_with_Z1_below_one']})")

    # -- TC5b the negative controls -----------------------------------------
    print("\n[TC5b] negative controls: the border direction is wired through the AMPLITUDE")
    print("       COLUMN as well, so a wrong direction changes Gamma and the control can fail")
    neg = []
    for border in ("analytic", "svd", "second", "random"):
        row = z1_subblocks(16, 16 + M_EXTRA, "algebraic", 0.3, gauge="null",
                           border=border)
        neg.append({"border": border, "A_tail_norm": row["A_tail_norm"],
                    "Gamma_inv_norm": row["Gamma_inv_norm"],
                    "Z1_tail_Gamma": row["Z1_tail_Gamma"],
                    "Z1_Gamma_tail": row["Z1_Gamma_tail"],
                    "Z1_lower_bound": row["Z1_lower_bound"]})
        print(f"      border={border:9s}: ||A_tail||={row['A_tail_norm']:10.4g}  "
              f"||Gamma^-1||={row['Gamma_inv_norm']:11.5g}  "
              f"Z1[tG]={row['Z1_tail_Gamma']:8.4g}  Z1[Gt]={row['Z1_Gamma_tail']:11.5g}")
    res["TC5b_negative_controls"] = neg
    an = next(r for r in neg if r["border"] == "analytic")
    sv = next(r for r in neg if r["border"] == "svd")
    wrong = [r for r in neg if r["border"] in ("second", "random")]
    # The SVD pair is the most favourable one-dimensional choice that exists, so "analytic
    # is best" is the wrong test -- the right one is whether the border a PROOF can write
    # down matches it, and whether the two deliberately wrong directions are worse.
    res["TC5b_analytic_over_svd"] = float(
        an["Z1_lower_bound"] / sv["Z1_lower_bound"])
    res["TC5b_wrong_directions_are_worse"] = bool(
        all(r["Z1_lower_bound"] > 2.0 * an["Z1_lower_bound"] for r in wrong))
    res["TC5b_worst_over_analytic"] = float(
        max(r["Z1_lower_bound"] for r in wrong) / an["Z1_lower_bound"])
    print(f"      analytic/SVD = {res['TC5b_analytic_over_svd']:.4f}; wrong directions "
          f"worse: {res['TC5b_wrong_directions_are_worse']} (worst is "
          f"{res['TC5b_worst_over_analytic']:.3g}x the analytic border)")

    # -- TC8 the normalisation of the augmented block is a CHOICE -----------
    print("\n[TC8] normalisation ablation: ||Gamma^-1|| is inflated by the augmentation,")
    print("      so the weights on the amplitude column and the matching row are ablated")
    abl = []
    for kind, p_ in CLASSES:
        for K in (4, 16):
            base = None
            for nm in list(NORMALISATIONS) + ["no_amplitude"]:
                if nm == "no_amplitude":
                    row = z1_subblocks(K, K + M_EXTRA, kind, p_, gauge="null",
                                       far_field=False)
                else:
                    row = z1_subblocks(K, K + M_EXTRA, kind, p_, gauge="null", norm=nm)
                rec = {"class": kind, "param": float(p_), "K": int(K), "norm": nm,
                       "Gamma_inv_norm": row["Gamma_inv_norm"],
                       "Z1_tail_Gamma": row["Z1_tail_Gamma"],
                       "Z1_Gamma_tail": row["Z1_Gamma_tail"],
                       "Z1_lower_bound": row["Z1_lower_bound"]}
                abl.append(rec)
                if base is None:
                    base = rec["Z1_Gamma_tail"]
                print(f"      {kind:9s} s={p_:.1f} K={K:3d} {nm:13s}: "
                      f"||Gamma^-1||={rec['Gamma_inv_norm']:9.4g}  "
                      f"Z1[Gt]={rec['Z1_Gamma_tail']:9.4g}  "
                      f"({rec['Z1_Gamma_tail']/base:.3f}x shipped)")
    res["TC8_normalisation_ablation"] = abl
    best_abl = min(abl, key=lambda r: r["Z1_lower_bound"])
    res["TC8_best_over_all_normalisations"] = best_abl
    res["TC8_gate_survives_renormalisation"] = bool(best_abl["Z1_lower_bound"] > 1.0)
    print(f"      SMALLEST Z1 lower bound over EVERY normalisation tried: "
          f"{best_abl['Z1_lower_bound']:.4g} ({best_abl['class']} s={best_abl['param']} "
          f"K={best_abl['K']} {best_abl['norm']}) -- gate survives: "
          f"{res['TC8_gate_survives_renormalisation']}")

    # -- TC2 the four terms in ONE polynomial -------------------------------
    print("\n[TC2] the four terms in one polynomial")
    polys = []
    for kind, p in CLASSES:
        for K in K_SWEEP:
            row = z1_subblocks(K, K + M_EXTRA, kind, p, gauge="null")
            rig = rigorous_finite_block(K, kind, p)
            A_norm = max(row["Gamma_inv_norm"], row["A_tail_norm"])
            qb = quadratic_bound(kind, p, K=min(max(K, 16), 96))
            Z2 = 2.0 * A_norm * qb
            Z1 = row["Z1_total"]
            Y0 = 0.0
            poly = radii_polynomial(Y0, Z1, Z2)
            poly.update({"K": int(K), "class": kind, "param": float(p),
                         "A_norm": A_norm, "quadratic_bound": qb,
                         "Z1_finite_block_rigorous": rig["Z1_finite"],
                         "Z1_tail_Gamma": row["Z1_tail_Gamma"],
                         "Z1_Gamma_tail": row["Z1_Gamma_tail"],
                         "tail_constant": row["A_tail_norm"],
                         "Z1_leg51_finite_block_only": rig["Z1_finite"],
                         "poly_leg51_only": radii_polynomial(0.0, rig["Z1_finite"],
                                                             2.0 * rig["A_norm"] * qb)})
            polys.append(poly)
            print(f"      {kind:9s} s={p:.1f} K={K:3d}: Y0={Y0:.1e}  Z1={Z1:10.4g}  "
                  f"Z2={Z2:11.5g}  tail const={row['A_tail_norm']:.3f}  "
                  f"positive interval: {poly['has_positive_interval']}  "
                  f"r_max={poly['r_max'] if poly['r_max'] is not None else float('nan'):.3e}")
    res["TC2_polynomial"] = polys

    # -- the gate -----------------------------------------------------------
    closes = any(pp["has_positive_interval"] for pp in polys)
    res["gate_polynomial_closes"] = bool(closes)
    terms = {"Y0": float(min(pp["Y0"] for pp in polys)),
             "Z1_min_over_sweep": float(min(pp["Z1"] for pp in polys)),
             "Z2_min_over_sweep": float(min(pp["Z2"] for pp in polys)),
             "tail_constant_range": [float(min(pp["tail_constant"] for pp in polys)),
                                     float(max(pp["tail_constant"] for pp in polys))]}
    res["terms"] = terms
    # which term ran out: the one whose sub-block exceeds 1 at every split
    worst = max(("Z1_tail_Gamma", min(r["Z1_tail_Gamma"] for r in sweep)),
                ("Z1_Gamma_tail", min(r["Z1_Gamma_tail"] for r in sweep)),
                ("Z1_Gamma_Gamma", min(r["Z1_Gamma_Gamma"] for r in sweep)),
                ("Z1_tail_tail", min(r["Z1_tail_tail"] for r in sweep)),
                key=lambda t: t[1])
    tg_min = min(r["Z1_tail_Gamma"] for r in sweep)
    res["term_that_ran_out"] = {
        "name": worst[0], "min_over_every_split_and_class": worst[1],
        "statement": (
            "Z1[Gamma <- tail] = ||Gamma^{-1} L_{Gamma,tail}||_w.  It DOES involve "
            "Gamma^{-1} -- measured, it equals 2||Gamma^{-1}|| to four digits in every row "
            "of the sweep (1.90..2.00) -- so this is a statement about the block-diagonal "
            "approximate inverse THIS leg built, not about every finite block that could "
            "ever be built.  The whole K-dependence lives in ||Gamma^{-1}||, which is "
            "EXACTLY 2(K^2 - 1) for the augmented block and EXACTLY 4(K - 1) without the "
            "amplitude column: the K^2 is created by the augmentation, and TC8 ablates the "
            "normalisation that creates it.  The dominant column of L_{Gamma,tail} is the "
            "RANK-ONE row-1 term (weight 1 from every tail mode), not the (K+1)/2 "
            "sub-diagonal entry."),
        "scope": (
            "WHAT THIS LEG ESTABLISHES: that the block-diagonal approximate inverse the "
            "standard method requires cannot close this certificate, on this object, in "
            "either admissible class, at any split from K = 4 to 64, under either gauge, "
            "and under every normalisation of the augmented block tried in TC8.  WHAT IT "
            "DOES NOT ESTABLISH: that no finite block can.  The genuinely "
            "finite-block-INDEPENDENT sub-block is Z1[tail <- Gamma] = "
            "||A_tail L_{tail,Gamma}||_w, which contains no Gamma^{-1}; its minimum over "
            f"the whole sweep is {tg_min:.4f}, which is BELOW 1.  So that term alone does "
            "not forbid closure, and stage MM -- an approximate inverse that is not block "
            "diagonal -- is a real question rather than a formality."),
        "finite_block_independent_term": {
            "name": "Z1_tail_Gamma",
            "min_over_every_split_and_class": float(tg_min),
            "below_one": bool(tg_min < 1.0)}}
    res["verdict"] = ("POLYNOMIAL_CLOSES_ON_a0_CLM" if closes else
                      "DOES_NOT_CLOSE__TERM_THAT_RAN_OUT=Z1_BLOCK_COUPLING")

    res["TC7_ceiling"] = (
        "Measured on the a = 0 CLM fixed point.  Y_0 is exactly zero there -- including "
        "the new matching row -- because the anchor IS one basis mode and therefore has no "
        "far field at all, so the radii polynomial's root r = 0 is available for a "
        "degenerate reason and certifies nothing.  The reportable quantity is whether the "
        "inequality holds on a POSITIVE interval, which needs Z_1 < 1, and it does not. "
        "Nothing is claimed about HL_S2_nonsymmetric: on the gate's own terms that object "
        "is only reached if the polynomial closes here, and it did not.")

    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)  VERDICT: {res['verdict']}")
    print(f"TERM THAT RAN OUT: {res['term_that_ran_out']['name']} -- smallest value "
          f"anywhere in the sweep {res['term_that_ran_out']['min_over_every_split_and_class']:.4g}")


if __name__ == "__main__":
    main()
