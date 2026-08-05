"""Route-MM v1: THE MISMATCH -- spend the last free choice, the SHAPE of the approximate
inverse `A`, or close the lane.

Leg 53 assembled the four terms of the bordered certificate into one radii polynomial and
it did not close: with the block-diagonal approximate inverse the method requires,
`A = Gamma^-1 (+) A_tail`, the coupling sub-block `Z1[Gamma<-tail]` is 43.15 at the best
split in the whole admissible sweep, against the 1 it must be under.  Four of the five
degrees of freedom are measured and banned -- the weight exponent `s`, the weight family,
the split `K`, and the border direction.  THE ONE REMAINING FREE CHOICE IS THE SHAPE OF `A`,
and the block-diagonal shape is exactly what makes the coupling a term at all.

PRE-COMMITTED CLAUSES, written before the numbers existed (both branches reportable):

  MM0 THE NOVELTY PASS COMES FIRST and can only narrow the claim.  Run and committed as
      `writeup/novelty/leg_54.md` BEFORE this file was written, with LINKS not counts (leg
      53 logged counts, could not be audited, and was withdrawn).  Verdict PROCEED_NARROW:
      arXiv:2411.18361 states the block-diagonal convention explicitly (`A = A^N + pi^inf`,
      the tail acts as the identity) and justifies it by `DF` being a COMPACT PERTURBATION
      OF THE IDENTITY -- a hypothesis this operator does not satisfy.  Nothing is banked as
      novel; the block-Gauss-Seidel / Schur-complement alternatives are textbook
      preconditioning, and what is new here is only their measurement in the `Z1` slot.

  MM1 THE MISMATCH AS AN INEQUALITY, NOT A MOOD.  State and CHECK

          Z1  >=  |1 - K/2| * (w_{K+1}/w_K) * ||A_tail e_{K+1}||_w / w_{K+1}

      against measured data.  Its scope is stated exactly: the sub-block it bounds is
      `(I - A L)_{tail,Gamma} = -(A21 G + A22 C)`, so with `A21 = 0` and `A22 = A_tail` it
      is exactly `-A_tail C`, and it holds for EVERY finite block -- i.e. it is a statement
      about every `A` whose tail-row block does not couple back to `Gamma`, which is
      strictly more than "block diagonal".

      *** SCOPE CORRECTION, FROM VER-A's INDEPENDENT PASS (GAP 1 and GAP 5), AND IT LIMITS
      WHAT THIS LEG MAY CLAIM.  The prefactor `|1 - K/2|` is exactly ZERO at K = 2 and
      small below K = 5, so the RHS only exceeds 1 from K >= 5 (flat) and K >= 4
      (algebraic).  Leg 53's sweep started at K = 4 and hid this.  MM-1 therefore DOES NOT
      establish "no block-diagonal A can work for this operator": it leaves K in {2, 3}
      (and K = 4 in the flat class) open, and at those splits closure is blocked only by
      `Z1[Gamma<-tail]`, which is precisely the sub-block that CONTAINS `Gamma^-1` and that
      MM-1 exists in order not to depend on.  The runner therefore sweeps K = 2 and 3
      explicitly, reports the smallest K at which the RHS clears 1 in each class, and the
      small-K corner is closed by MM4 instead -- on a DIFFERENT axis (shape-independence,
      not finite-block-independence).  Neither argument alone is universal and the writeup
      says so. ***

  MM2 THE SHAPE BATTERY, ALL SUSPECTS AT ONCE (lesson 74).  Seven shapes of `A` on the SAME
      assembled object as leg 53, measured as the TRUE column-max of `I - A L` over the
      whole space rather than as a sum of sub-block norms:
        block_diag   leg 53's baseline, reproduced to check the instrument (lesson 85)
        gs_lower     one step of block Gauss-Seidel, Gamma swept first
        gs_upper     one step of block Gauss-Seidel, tail swept first
        schur        the Schur complement of the coupling, with A_tail for the tail solve
        ff_lift      a rank-one lift of the far field back into the tail -- the move the
                     algebra REQUIRES, see MM4
        oracle_pinv  A12 = -A11 B T^+ using the Moore-Penrose pseudo-inverse: NOT admissible,
                     it bounds what the best possible A12 could ever do
        exact_inv    A = (L_M)^-1: the unrestricted optimum, and a TAUTOLOGY unless it
                     survives MM3

  MM3 THE ADMISSIBILITY AUDIT, BECAUSE THE GATE IS TRIVIALLY YES OTHERWISE (lesson 86).
      `A = (L_M)^-1` drives `||I - A L_M||` to float noise by construction -- that is a
      statement about the code, not about the operator.  An admissible `A` is finite rank
      plus an EXPLICIT operator on the modes beyond it, so the audit builds `A` at
      truncation `M_A` and evaluates it against `L` at `M_L > M_A`, with the outer modes
      carried by the bordered tail inverse of THAT sub-tail.  If the number degrades with
      `M_A`, the exact inverse is not a shape, it is the truncation.

  MM4 THE SHAPE-INDEPENDENT FLOOR.  `(I - A L)_{Gamma,tail} = -(A11 B + A12 T)`.  The tail
      operator `T` is SINGULAR -- its kernel is the far field `hhat` -- so on that one
      direction the term collapses to `-A11 B hhat` and NO CHOICE OF A12 CAN TOUCH IT.
      Report `||Gamma^-1 (L hhat)||_w / ||hhat||_w` for every K including K = 2, and ablate
      the residual freedom in A11 by recomputing it with the Schur complement's A11.
      Dually, the tail-tail block on the same direction is `hhat - A21 B hhat`, which is
      why ff_lift is the required move and why it cannot be block diagonal.

  MM5 THE POSITIVE CONTROL MUST BE ABLE TO REPORT THE OTHER ANSWER (lesson 90), and it is
      run through EVERY shape, not just the baseline: `Lambda^1` dissipation, unbordered
      tail, no far-field unknown.  If no shape brings the assembled `Z1` below 1 for any
      mu > 0 then the instrument is broken and the negative result is void.

  MM5b THE NEGATIVE CONTROLS, wired through the amplitude column per lesson 90 -- a wrong
      border direction changes `Gamma` itself, so the control CAN come out differently.
      Run through the best shape, not only the baseline.

  MM6 THE CEILING, pre-committed.  This is the `a = 0` CLM object.  `Y_0` is exactly zero
      because the anchor IS one basis mode, so the root `r = 0` is available for a
      degenerate reason and certifies nothing.  The reportable quantity is whether the
      polynomial holds on a POSITIVE interval.  Nothing is claimed about
      HL_S2_nonsymmetric: on the gate's own terms that object is reached only if the
      polynomial closes here.

Writes writeup/data/p2_route_mm_v1_shape.json.

Run: .venv/bin/python -u experiments/p2_route_mm_v1_shape.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.spectral_certificate import (                              # noqa: E402
    quadratic_bound, rigorous_finite_block, tail_block, tail_right_null,
)
from p2_route_tc_v1_assemble import (                                  # noqa: E402
    amplitude_direction, augmented_finite_block, scaled_tail_and_inverse, wfun,
)

OUT = ROOT / "writeup" / "data" / "p2_route_mm_v1_shape.json"

ALPHA_TARGET = 0.394
CLASSES = (("flat", 0.0), ("algebraic", 0.3))
K_SWEEP = (4, 8, 16, 32, 64)
# VER-A GAP 1/5: leg 53's sweep started at K = 4 and hid the small-K corner.  K = 6 is in
# here on purpose: MM-1's RHS first clears 1 at K = 6 in the flat class, and a sweep of
# powers of two alone would have mis-reported that as K = 8.
K_SWEEP_SMALL = (2, 6) + K_SWEEP          # unsorted on purpose: the committed JSON's list
                                          # order must match this file exactly, so that a
                                          # verifier re-running it gets a byte-clean diff
K_ODD_SCAN = (3, 5, 7, 9, 11)             # MM1b: every ODD split has a SINGULAR finite block
M_EXTRA = 1024
M_A_LADDER = (128, 256, 512)
M_L_LADDER = (1024, 2048)

SHAPES = ("block_diag", "gs_lower", "gs_upper", "schur", "ff_lift", "oracle_pinv",
          "exact_inv")
ADMISSIBLE = {"block_diag": True, "gs_lower": True, "gs_upper": True, "schur": True,
              "ff_lift": True, "oracle_pinv": False, "exact_inv": False}


def colmax(Mx):
    """||.||_w operator norm in the scaled coordinates: max over columns of the abs colsum."""
    Mx = np.abs(np.asarray(Mx, dtype=float))
    return float(np.max(Mx.sum(0))) if Mx.size else 0.0


# --------------------------------------------------------------------------
# the assembled object -- leg 53's, rebuilt as ONE matrix so every shape sees
# exactly the same operator
# --------------------------------------------------------------------------
def assemble(K, M, kind, param, gauge="null", mu=0.0, border="analytic",
             far_field=True, norm="shipped", seed=0):
    """`L` in the scaled coordinates, split as [[G, B], [C, T]].

    Rows/cols of the Gamma block: modes 1..K, the gauge/pin row, and (when `far_field`)
    the far-field amplitude column and matching row.  The tail block is modes K+1..M.
    Every entry is taken from leg 53's runner unchanged -- this function only puts them in
    one array so that `I - A L` can be formed for a NON-block-diagonal `A`."""
    K, M = int(K), int(M)
    hdir = (amplitude_direction(K, M, kind, param, border, seed)
            if (far_field and border is not None) else None)
    G, w_row, w_col, ff, Wa, rho = augmented_finite_block(K, M, kind, param, gauge, mu,
                                                          far_field, norm, h=hdir)
    Gs = G * (w_row[:, None] / w_col[None, :])
    n = M - K
    wt = wfun(np.arange(K + 1, M + 1), kind, param)

    Ltg = np.zeros((n, G.shape[1]))
    Ltg[0, K - 1] = 1.0 - K / 2.0
    if far_field:
        Ltg[:, K + 1] = tail_block(K, M, mu=mu) @ ff["h"]
    C = (Ltg * wt[:, None]) / w_col[None, :]

    Lgt = np.zeros((G.shape[0], n))
    mt = np.arange(K + 1, M + 1, dtype=float)
    Lgt[K - 1, 0] += (K + 1) / 2.0
    Lgt[0, :] += -((-1.0) ** mt)
    if gauge == "dilation":
        Lgt[K, :] += mt
    if far_field:
        Lgt[K + 1, 0] += -1.0
    B = (Lgt * w_row[:, None]) / wt[None, :]

    T = tail_block(K, M, mu=mu) * (wt[:, None] / wt[None, :])
    Ainv_s, _, A_tail_norm = scaled_tail_and_inverse(K, M, kind, param, mu, border, seed)
    A_t = Ainv_s[:n, :n] if border is not None else Ainv_s
    Gi = np.linalg.inv(Gs)
    hh = tail_right_null(K, M) * wt
    hh = hh / float(np.sum(np.abs(hh)))
    return {"G": Gs, "B": B, "C": C, "T": T, "A_t": A_t, "Gi": Gi, "hhat": hh,
            "nG": Gs.shape[0], "n": n, "w_row": w_row, "w_col": w_col, "wt": wt,
            "Gamma_inv_norm": colmax(Gi), "A_tail_norm": A_tail_norm,
            "far_field_column": ff}


def full_L(ob):
    """`L` as one array, cached on the object -- it is reused by every shape."""
    if "L" not in ob:
        ob["L"] = np.block([[ob["G"], ob["B"]], [ob["C"], ob["T"]]])
    return ob["L"]


def build_A(ob, shape):
    """The seven shapes.  Returns `A` in the scaled coordinates, or None if unavailable."""
    G, B, C, T, A_t, Gi = ob["G"], ob["B"], ob["C"], ob["T"], ob["A_t"], ob["Gi"]
    nG, n = ob["nG"], ob["n"]
    Z, Zt = np.zeros((nG, n)), np.zeros((n, nG))
    if shape == "block_diag":
        return np.block([[Gi, Z], [Zt, A_t]])
    if shape == "gs_lower":                       # exact inverse of [[G,0],[C,T]]
        return np.block([[Gi, Z], [-A_t @ C @ Gi, A_t]])
    if shape == "gs_upper":                       # exact inverse of [[G,B],[0,T]]
        return np.block([[Gi, -Gi @ B @ A_t], [Zt, A_t]])
    if shape == "schur":
        S = G - B @ A_t @ C
        Si = np.linalg.inv(S)
        return np.block([[Si, -Si @ B @ A_t], [-A_t @ C @ Si, A_t + A_t @ C @ Si @ B @ A_t]])
    if shape == "ff_lift":
        # A21 = hhat u^T / (u . B hhat): the rank-one lift MM4 shows is required.  `u` is
        # swept over four natural functionals and the best is reported -- reporting the best
        # is the CONSERVATIVE choice for a negative result.
        v = B @ ob["hhat"]
        best, bestz = None, np.inf
        cands = {"e_rowK": np.eye(nG)[max(0, nG - 3)], "e_row1": np.eye(nG)[0],
                 "lstsq": v / max(float(np.dot(v, v)), 1e-300),
                 "GiT": (Gi.T @ Gi) @ v}
        L = full_L(ob)
        # I - AL for a rank-one A21 differs from the block-diagonal one only in the tail
        # rows, so the candidates are scored on that block alone rather than by reforming
        # the whole product four times.
        R_bd = np.eye(nG + n) - np.block([[Gi, Z], [Zt, A_t]]) @ L
        top = np.abs(R_bd[:nG, :]).sum(0)
        for nm, u in cands.items():
            d = float(np.dot(u, v))
            if abs(d) < 1e-13:
                continue
            A21 = np.outer(ob["hhat"], u / d)
            Rt = R_bd[nG:, :] - np.hstack([A21 @ G, A21 @ B])
            z = float(np.max(top + np.abs(Rt).sum(0)))
            if z < bestz:
                best, bestz = np.block([[Gi, Z], [A21, A_t]]), z
        return best
    if shape == "oracle_pinv":                    # the best A12 that could ever exist
        Tp = np.linalg.pinv(T)
        v = B @ ob["hhat"]
        u = (Gi.T @ Gi) @ v
        d = float(np.dot(u, v))
        A21 = np.outer(ob["hhat"], u / d) if abs(d) > 1e-13 else Zt
        return np.block([[Gi, -Gi @ B @ Tp], [A21, A_t]])
    if shape == "exact_inv":
        return np.linalg.inv(full_L(ob))
    raise ValueError(shape)


def measure(ob, shape):
    nG, n = ob["nG"], ob["n"]
    L = full_L(ob)
    A = build_A(ob, shape)
    if A is None:
        return None
    R = np.eye(nG + n) - A @ L
    return {"shape": shape, "admissible": ADMISSIBLE[shape],
            "Z1": colmax(R),
            "Z1_Gamma_Gamma": colmax(R[:nG, :nG]), "Z1_Gamma_tail": colmax(R[:nG, nG:]),
            "Z1_tail_Gamma": colmax(R[nG:, :nG]), "Z1_tail_tail": colmax(R[nG:, nG:]),
            "A_norm": colmax(A)}


# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    res = {"leg": 54, "route": "MM", "version": "v1",
           "object": "a=0 CLM fixed point in the compactified odd-sine basis "
                     "(experiments/p2_route_tc_v1_assemble.py, leg 53's assembled object)",
           "target_alpha": ALPHA_TARGET, "M_extra": M_EXTRA, "shapes": list(SHAPES)}

    # -- MM0 ----------------------------------------------------------------
    res["MM0_novelty"] = {
        "log": "writeup/novelty/leg_54.md",
        "verdict": "PROCEED_NARROW",
        "run_before_construction": True,
        "links_not_counts": True,
        "key_precedent": {
            "id": "arXiv:2411.18361",
            "what": ("Validated matrix multiplication transform for orthogonal polynomials, "
                     "with applications to computer-assisted proofs for PDEs.  States the "
                     "block-diagonal convention explicitly: for DF a COMPACT PERTURBATION "
                     "OF THE IDENTITY one seeks A as a finite-rank perturbation of the "
                     "identity, A = A^N + pi^inf, letting the tail act as the identity."),
            "why_it_matters": ("It confirms the block-diagonal A is the convention rather "
                               "than this project's misreading, AND it names the hypothesis "
                               "that buys it -- compactness relative to the identity -- "
                               "which this operator does not satisfy (leg 51: the unbounded "
                               "part is a shift, not a multiplier).")},
        "banked_novelty": "NONE.  Block Gauss-Seidel and Schur-complement preconditioning "
                          "are textbook (Numer. Math., doi 10.1007/BF01385611); only their "
                          "measurement in the Z1 slot of this operator is new, and that is "
                          "a measurement on a known object, not a method.",
        "leg52_search_index_flag": "STANDS -- not tested by this pass, and not cleared.",
        "off_diagonal_unbounded_part_in_literature": "UNCHECKED, not a gap."}
    print(f"[MM0] novelty: {res['MM0_novelty']['verdict']} "
          f"(log: {res['MM0_novelty']['log']}, links not counts)")

    # -- MM1 the inequality -------------------------------------------------
    print("\n[MM1] Z1 >= |1 - K/2| (w_{K+1}/w_K) ||A_tail e_{K+1}||_w / w_{K+1}")
    mm1 = []
    for kind, p in CLASSES:
        for K in K_SWEEP_SMALL:
            M = K + M_EXTRA
            ob = assemble(K, M, kind, p)
            wK = float(wfun([K], kind, p)[0])
            wK1 = float(wfun([K + 1], kind, p)[0])
            e = np.zeros(ob["n"])
            e[0] = 1.0
            second = float(np.sum(np.abs(ob["A_t"] @ e)))
            rhs = abs(1.0 - K / 2.0) * (wK1 / wK) * second
            meas = colmax(ob["A_t"] @ ob["C"])
            mm1.append({"class": kind, "param": float(p), "K": int(K), "M": int(M),
                        "prefactor_abs_1_minus_K_over_2": abs(1.0 - K / 2.0),
                        "weight_ratio": wK1 / wK, "A_tail_e_Kplus1": second,
                        "rhs": rhs, "measured_Z1_tail_Gamma": meas,
                        "ratio_measured_over_rhs": (meas / rhs) if rhs > 0 else None,
                        "vacuous": bool(rhs == 0.0)})
            print(f"      {kind:9s} s={p:.1f} K={K:3d}: RHS={rhs:9.5f}  "
                  f"measured={meas:9.5f}  ratio="
                  f"{(meas / rhs) if rhs > 0 else float('inf'):8.4f}"
                  f"{'   <-- VACUOUS: the prefactor |1-K/2| is exactly 0' if rhs == 0 else ''}")
    res["MM1_inequality"] = mm1
    tight = [r for r in mm1 if r["ratio_measured_over_rhs"] is not None]
    res["MM1_max_ratio_deviation_from_one"] = float(
        max(abs(r["ratio_measured_over_rhs"] - 1.0) for r in tight))
    res["MM1_is_an_equality"] = bool(res["MM1_max_ratio_deviation_from_one"] < 1e-6)
    res["MM1_second_factor_range"] = [float(min(r["A_tail_e_Kplus1"] for r in mm1)),
                                      float(max(r["A_tail_e_Kplus1"] for r in mm1))]
    smallest_K_binding = {}
    for kind, p in CLASSES:
        cand = [r["K"] for r in mm1 if r["class"] == kind and r["rhs"] > 1.0]
        smallest_K_binding[kind] = int(min(cand)) if cand else None
    res["MM1_smallest_K_with_rhs_above_one"] = smallest_K_binding
    res["MM1_second_factor_range_measured"] = res["MM1_second_factor_range"]
    res["MM1_scope"] = (
        "The sub-block this bounds is (I - A L)_{tail,Gamma} = -(A21 G + A22 C).  With "
        "A21 = 0 and A22 = A_tail it is exactly -A_tail C, whose (K+1)-th row carries the "
        "entry (1 - K/2) from mode K.  So the inequality binds every approximate inverse "
        "whose tail-row block does not couple back to Gamma -- strictly larger than the "
        "block-diagonal class.  It says NOTHING about an A with A21 != 0, which is why MM2 "
        "exists.  MEASURED, it is not merely an inequality but an EQUALITY to "
        f"{res['MM1_max_ratio_deviation_from_one']:.1e}: the (K+1)-th column is the "
        "maximising column of that sub-block, so the bound is attained and not slack.  "
        "BUT ITS REACH IS LIMITED, and this is VER-A's GAP 1: the RHS only exceeds 1 from "
        f"K >= {smallest_K_binding.get('flat')} (flat) and K >= "
        f"{smallest_K_binding.get('algebraic')} (algebraic).  Below that the inequality is "
        "true and useless.  MM-1 therefore does NOT establish 'no block-diagonal A can work "
        "for this operator' -- it establishes it only for splits at or above those K.")
    res["MM1_small_K_hole"] = (
        "The prefactor |1 - K/2| VANISHES at K = 2 and is 0.5 at K = 3, so the RHS is "
        "exactly 0.0 at K = 2 and below 1 at K = 3 in both classes and at K = 4 in the flat "
        "class.  Leg 53's sweep started at K = 4, which hid this; VER-A found it (GAP 1, "
        "GAP 5) and it is a genuine hole in the finite-block-INDEPENDENT argument, because "
        "at those splits closure is blocked only by Z1[Gamma<-tail], which contains "
        "Gamma^-1.  IT IS NOT CLOSED BY TUNING THE SPLIT -- that is banned, and would be "
        "the wrong move anyway.  It is closed from two directions instead.  FIRST, MM1b: "
        "every ODD split has a SINGULAR augmented finite block, so K = 3 is not an open "
        "case at all -- Gamma^-1 does not exist there -- and the open corner shrinks to "
        "K = 2 in both classes plus K = 4 in the flat class.  SECOND, MM4, on a different "
        "axis from MM-1: MM4's floor is SHAPE-independent (A12, A21, A22 all drop out) "
        "though NOT finite-block-independent (it contains A11), and it is 7.01 (flat) / "
        "5.04 (algebraic) at K = 2 and 23.07 at K = 4 flat, all far above 1.  So the gate's "
        "question -- does a non-block-diagonal A close it -- is answered at every admissible "
        "split with no hole.  The BROADER claim, that no finite block of any kind can close "
        "it, is still NOT established at small K, and this leg does not make it.")
    res["MM1_verifier_note"] = (
        "VER-A independently re-derived leg 53's headline before this leg built on it and "
        "confirmed all of it to full printed precision (43.15129110858924, "
        "20.473399995961532, Z1[tail<-Gamma] min 0.9961089494163415 over K = 4..64, "
        "assembled Z1 44.53860580010511, positive control 0.9156 at mu = 2, and the closed "
        "forms 2(K^2-1) and 4(K-1), the latter exact in rational arithmetic).  Two "
        "corrections are adopted here: the K-range restriction above, and the second "
        "factor's range, which VER-A re-measured as 0.9412..1.3873 over K = 4..64 and "
        "0.9412..1.3913 over K = 2..64.  CONTINUATION_PROMPT.md quotes 0.94..1.33, which is "
        "not traceable to leg 53's shipped JSON; this leg quotes its own measured range "
        f"{res['MM1_second_factor_range'][0]:.4f}..{res['MM1_second_factor_range'][1]:.4f} "
        "instead.  VER-A also records that the closed forms are exact only in the flat "
        "class with the null gauge, and that Y_0 = 0 is a hardcoded literal whose "
        "justification VER-A checked independently and found correct.")
    print(f"      the bound is ATTAINED, not slack: max |ratio - 1| = "
          f"{res['MM1_max_ratio_deviation_from_one']:.2e}")

    # -- MM1b the odd-K obstruction -----------------------------------------
    print("\n[MM1b] why the small-K hole is smaller than it looks: EVERY ODD SPLIT HAS A")
    print("       SINGULAR FINITE BLOCK, so Gamma^-1 does not exist there at all")
    odd = []
    for kind, p in CLASSES:
        for gauge in ("null", "dilation"):
            for far_field in (True, False):
                for K in K_ODD_SCAN + (2, 4, 6, 8):
                    M = K + M_EXTRA
                    hdir = (amplitude_direction(K, M, kind, p, "analytic", 0)
                            if far_field else None)
                    G, w_row, w_col, _, _, _ = augmented_finite_block(
                        K, M, kind, p, gauge, 0.0, far_field, "shipped", h=hdir)
                    Gs = G * (w_row[:, None] / w_col[None, :])
                    sv = np.linalg.svd(Gs, compute_uv=False)
                    odd.append({"class": kind, "param": float(p), "gauge": gauge,
                                "far_field": bool(far_field), "K": int(K),
                                "K_is_odd": bool(K % 2 == 1),
                                "smallest_singular_value": float(sv[-1]),
                                "condition_number": float(sv[0] / sv[-1])
                                if sv[-1] > 0 else None})
    res["MM1b_odd_K_scan"] = odd
    odd_sv = [r["smallest_singular_value"] for r in odd if r["K_is_odd"]]
    even_sv = [r["smallest_singular_value"] for r in odd if not r["K_is_odd"]]
    res["MM1b_max_smallest_sv_at_odd_K"] = float(max(odd_sv))
    res["MM1b_min_smallest_sv_at_even_K"] = float(min(even_sv))
    res["MM1b_every_odd_split_is_singular"] = bool(max(odd_sv) < 1e-15
                                                   and min(even_sv) > 1e-4)
    res["MM1b_statement"] = (
        "Scanning K = 3, 5, 7, 9, 11 against K = 2, 4, 6, 8 in both classes, both gauges, "
        "and with and without the far-field column: the augmented finite block's smallest "
        f"singular value is at most {max(odd_sv):.1e} at EVERY odd split and at least "
        f"{min(even_sv):.1e} at every even one.  Odd K is not badly conditioned, it is "
        "SINGULAR -- without the far-field column at K = 3 the smallest singular value is "
        "exactly 0.0.  The structural reason is visible in the matrix: the far-field kernel "
        "hhat is supported on one parity chain (modes K+1, K+3, ...) and the linearisation "
        "couples mode k only to k +/- 1, so at odd K the mode-K residual row acquires no "
        "entry on any of b_1..b_K or delta c_omega and is carried entirely by the amplitude "
        "column.  CONSEQUENCE FOR VER-A's GAP 1: the split must be EVEN, so the corner MM-1 "
        "leaves open is not {2, 3, 4} but {2} (both classes) plus {4} in the flat class "
        "alone -- and both are covered by MM4's floor (7.01 and 5.04 at K = 2, 23.07 at "
        "K = 4 flat).  This is NOT a repair by tuning the split: it removes candidate "
        "splits, it does not choose one.")
    print(f"       odd K: smallest singular value <= {max(odd_sv):.1e} at EVERY odd split")
    print(f"       even K: smallest singular value >= {min(even_sv):.1e} at every even split")
    print(f"       => the split must be EVEN; MM-1's open corner is K = 2 (both classes)")
    print(f"          plus K = 4 in the flat class, both closed by MM4's floor")

    # -- MM4 the shape-independent floor (computed before MM2 so MM2 can be read against it)
    print("\n[MM4] the shape-independent floor: T is SINGULAR (kernel = the far field hhat),")
    print("      so (I - A L)_{Gamma,tail} hhat = -A11 B hhat and NO A12 can touch it")
    floors = []
    for kind, p in CLASSES:
        for K in K_SWEEP_SMALL:
            ob = assemble(K, K + M_EXTRA, kind, p)
            v = ob["B"] @ ob["hhat"]
            fl = float(np.sum(np.abs(ob["Gi"] @ v)))
            S = ob["G"] - ob["B"] @ ob["A_t"] @ ob["C"]
            fl_s = float(np.sum(np.abs(np.linalg.inv(S) @ v)))
            floors.append({"class": kind, "param": float(p), "K": int(K),
                           "floor_with_Gamma_inv_A11": fl,
                           "floor_with_schur_A11": fl_s,
                           "A11_freedom_changes_it_by": abs(fl_s - fl) / fl,
                           "Gamma_inv_norm": ob["Gamma_inv_norm"],
                           "floor_over_Gamma_inv_norm": fl / ob["Gamma_inv_norm"]})
            print(f"      {kind:9s} s={p:.1f} K={K:3d}: "
                  f"||Gamma^-1 L hhat||/||hhat|| = {fl:9.4f}   "
                  f"(Schur A11: {fl_s:9.4f}, {abs(fl_s-fl)/fl:.1e} relative)   "
                  f"||Gamma^-1|| = {ob['Gamma_inv_norm']:9.4g}")
    res["MM4_floor"] = floors

    # MM4b -- the identity's OWN caveat: hhat spans ker T for the INFINITE operator, and on
    # the truncated one T hhat is nonzero.  Measure where it lives and how fast it falls,
    # rather than asserting an exact zero the truncation does not deliver (lesson 72/86).
    print("      MM4b: hhat is in ker T for the INFINITE tail; on the truncation the")
    print("            defect sits on the LAST mode alone and falls like M^-1")
    kd = []
    for K in (4, 16):
        for Mx in (256, 512, 1024, 2048):
            T_ = tail_block(K, K + Mx)
            h_ = tail_right_null(K, K + Mx)
            r_ = T_ @ h_
            nz = np.nonzero(np.abs(r_) > 1e-14)[0]
            kd.append({"K": int(K), "M_extra": int(Mx),
                       "relative_l1_defect": float(np.sum(np.abs(r_))
                                                   / np.sum(np.abs(h_))),
                       "supported_on_last_mode_only": bool(list(nz) == [len(r_) - 1]),
                       "n_nonzero_entries": int(len(nz))})
    res["MM4b_kernel_truncation_defect"] = kd
    res["MM4b_defect_is_edge_only"] = bool(all(r["supported_on_last_mode_only"]
                                               for r in kd))
    lad16 = [r for r in kd if r["K"] == 16]
    res["MM4b_defect_halves_per_doubling"] = bool(all(
        abs(lad16[i]["relative_l1_defect"] / lad16[i + 1]["relative_l1_defect"] - 2.0) < 0.05
        for i in range(len(lad16) - 1)))
    res["MM4b_max_relative_defect_at_M_extra_1024"] = float(max(
        r["relative_l1_defect"] for r in kd if r["M_extra"] == 1024))
    res["MM4b_caveat"] = (
        "MM4's identity -- that A12 drops out of (I - A L)_{Gamma,tail} on the direction "
        "hhat -- is EXACT for the infinite tail operator, whose kernel hhat spans.  On the "
        "TRUNCATED operator actually computed, T hhat is not exactly zero.  Measured, the "
        "defect is supported on the LAST mode alone at every K and M tried "
        f"({res['MM4b_defect_is_edge_only']}), i.e. it is a boundary effect of the "
        "truncation and not a failure of the kernel, and its relative l^1 size HALVES per "
        f"doubling of M ({res['MM4b_defect_halves_per_doubling']}), i.e. it is O(M^-1) -> 0. "
        f"At the M used throughout this leg it is at most "
        f"{res['MM4b_max_relative_defect_at_M_extra_1024']:.2e} relative, against a floor "
        "of 5.04 and above -- i.e. a couple of percent, against a quantity that would have "
        "to fall by a factor of five.  So the floor is a statement about the infinite "
        "operator which the computed one tracks to a few percent, NOT an exact algebraic "
        "zero being read off a float, which is the failure lesson 86 warns about.")
    print(f"            edge-only: {res['MM4b_defect_is_edge_only']}, halves per doubling: "
          f"{res['MM4b_defect_halves_per_doubling']}, max relative defect at M-K=1024: "
          f"{res['MM4b_max_relative_defect_at_M_extra_1024']:.2e}")
    res["MM4_min_floor"] = float(min(f["floor_with_Gamma_inv_A11"] for f in floors))
    res["MM4_min_floor_at"] = min(floors, key=lambda f: f["floor_with_Gamma_inv_A11"])
    res["MM4_max_A11_freedom_effect"] = float(
        max(f["A11_freedom_changes_it_by"] for f in floors))
    res["MM4_statement"] = (
        "Write I - A L in blocks for a completely general A = [[A11,A12],[A21,A22]].  Its "
        "(Gamma,tail) block is -(A11 B + A12 T).  The tail operator T is singular -- its "
        "kernel is exactly the far-field direction hhat that leg 52 bordered -- so applying "
        "that block to hhat gives -A11 B hhat, in which A12 has DROPPED OUT.  The size of "
        "the coupling along the one direction that matters is therefore a property of A11 "
        "alone.  A11 is not completely free (the (Gamma,Gamma) block needs A11 G + A12 C "
        "= I), but the two natural realisations -- A11 = Gamma^-1 and A11 = the Schur "
        f"complement's inverse -- agree to {res['MM4_max_A11_freedom_effect']:.1e} relative, "
        "so the freedom is measured and it is not where the answer lives.  DUALLY, the "
        "(tail,tail) block applied to hhat is hhat - A21 B hhat: the ONLY way to control "
        "the tail on its own kernel is a NON-ZERO A21, which is precisely why the "
        "block-diagonal shape is wrong and precisely what ff_lift builds.")
    print(f"      SMALLEST floor over every class and split (K = 2..64): "
          f"{res['MM4_min_floor']:.4f} -- against the 1 it must be under")

    # -- MM2 the shape battery ----------------------------------------------
    print("\n[MM2] the shape battery: TRUE column-max of I - A L over the whole space")
    battery = []
    for kind, p in CLASSES:
        for gauge in ("dilation", "null"):
            for K in K_SWEEP:
                ob = assemble(K, K + M_EXTRA, kind, p, gauge=gauge)
                row = {"class": kind, "param": float(p), "gauge": gauge, "K": int(K),
                       "M": int(K + M_EXTRA),
                       "Gamma_inv_norm": ob["Gamma_inv_norm"],
                       "A_tail_norm": ob["A_tail_norm"], "by_shape": {}}
                for sh in SHAPES:
                    m = measure(ob, sh)
                    if m is not None:
                        row["by_shape"][sh] = m
                battery.append(row)
                print(f"      {kind:9s} s={p:.1f} {gauge:8s} K={K:3d}: " +
                      "  ".join(f"{sh[:9]}={row['by_shape'][sh]['Z1']:9.4g}"
                                for sh in SHAPES if sh in row["by_shape"]))
    res["MM2_shape_battery"] = battery

    def best_over(pred):
        cand = [(r, sh, m) for r in battery for sh, m in r["by_shape"].items() if pred(sh)]
        return min(cand, key=lambda t: t[2]["Z1"])

    r_adm, sh_adm, m_adm = best_over(lambda sh: ADMISSIBLE[sh])
    r_any, sh_any, m_any = best_over(lambda sh: True)
    r_bd = min((r for r in battery), key=lambda r: r["by_shape"]["block_diag"]["Z1"])
    res["MM2_best_admissible"] = {"class": r_adm["class"], "param": r_adm["param"],
                                  "gauge": r_adm["gauge"], "K": r_adm["K"],
                                  "shape": sh_adm, **m_adm}
    res["MM2_best_any_shape"] = {"class": r_any["class"], "param": r_any["param"],
                                 "gauge": r_any["gauge"], "K": r_any["K"],
                                 "shape": sh_any, **m_any}
    res["MM2_block_diagonal_baseline"] = {"class": r_bd["class"], "param": r_bd["param"],
                                          "gauge": r_bd["gauge"], "K": r_bd["K"],
                                          **r_bd["by_shape"]["block_diag"]}
    res["MM2_improvement_over_block_diagonal"] = float(
        res["MM2_block_diagonal_baseline"]["Z1"] / m_adm["Z1"])
    print(f"      BEST ADMISSIBLE shape anywhere: {sh_adm} at {r_adm['class']} "
          f"s={r_adm['param']} gauge={r_adm['gauge']} K={r_adm['K']} -> Z1 = {m_adm['Z1']:.4f}")
    print(f"      block-diagonal baseline at its own best: "
          f"{res['MM2_block_diagonal_baseline']['Z1']:.4f} "
          f"({res['MM2_improvement_over_block_diagonal']:.3f}x improvement)")

    # instrument check (lesson 85): block_diag must reproduce leg 53's sub-blocks
    chk = next(r for r in battery if r["class"] == "algebraic" and r["gauge"] == "null"
               and r["K"] == 4)["by_shape"]["block_diag"]
    res["MM2_instrument_check_vs_leg53"] = {
        "leg53_Z1_Gamma_tail": 43.15129110858924,
        "leg54_Z1_Gamma_tail": chk["Z1_Gamma_tail"],
        "leg53_Z1_tail_Gamma": 1.387314691515264,
        "leg54_Z1_tail_Gamma": chk["Z1_tail_Gamma"],
        "reproduces": bool(abs(chk["Z1_Gamma_tail"] - 43.15129110858924) < 1e-9
                           and abs(chk["Z1_tail_Gamma"] - 1.387314691515264) < 1e-9),
        "correction_to_leg53": (
            "The tail-tail sub-block DIFFERS, and leg 54's is the honest one.  Leg 53 "
            "measured ||I - A_tail B_bordered|| where B_bordered is the matrix A_tail "
            "actually inverts, getting 6.0e-13; but the assembled operator's tail-tail "
            "block is the BARE scaled tail T, which is singular, and the bordering is part "
            "of the construction of A rather than part of L.  Charged correctly, "
            f"||I - A_tail T|| = {chk['Z1_tail_tail']:.4f}, not 6.0e-13.  This makes the "
            "block-diagonal baseline WORSE, not better, so leg 53's NO is unaffected -- but "
            "it is the term that ff_lift then removes, and it had to be visible first.")}
    print(f"      instrument check vs leg 53: reproduces = "
          f"{res['MM2_instrument_check_vs_leg53']['reproduces']} "
          f"(Z1[G<-t] {chk['Z1_Gamma_tail']:.6f}, Z1[t<-G] {chk['Z1_tail_Gamma']:.6f})")

    # -- MM3 the admissibility audit ----------------------------------------
    print("\n[MM3] admissibility audit: A = (L_{M_A})^-1 extended by the bordered tail")
    print("      inverse of the OUTER sub-tail, evaluated against L at M_L > M_A")
    audit = []
    K0 = 4
    for kind, p in CLASSES:
        for M_A in M_A_LADDER:
            for M_L in M_L_LADDER:
                if M_L <= M_A:
                    continue
                ob = assemble(K0, K0 + M_L, kind, p)
                oba = assemble(K0, K0 + M_A, kind, p)
                L = np.block([[ob["G"], ob["B"]], [ob["C"], ob["T"]]])
                La = np.block([[oba["G"], oba["B"]], [oba["C"], oba["T"]]])
                N, na = L.shape[0], La.shape[0]
                A = np.zeros((N, N))
                A[:na, :na] = np.linalg.inv(La)
                Aout, _, _ = scaled_tail_and_inverse(K0 + M_A, K0 + M_L, kind, p)
                nb = N - na
                A[na:, na:] = Aout[:nb, :nb]
                z = colmax(np.eye(N) - A @ L)
                audit.append({"class": kind, "param": float(p), "K": K0,
                              "M_A_extra": int(M_A), "M_L_extra": int(M_L), "Z1": z})
                print(f"      {kind:9s} s={p:.1f} M_A={M_A:5d} M_L={M_L:5d}: Z1 = {z:12.5g}")
    res["MM3_admissibility_audit"] = audit
    for kind, p in CLASSES:
        rows = sorted([a for a in audit if a["class"] == kind and a["M_L_extra"] == 1024],
                      key=lambda a: a["M_A_extra"])
        if len(rows) >= 2:
            res[f"MM3_growth_per_doubling_of_M_A_{kind}"] = float(
                np.exp(np.polyfit(np.log([r["M_A_extra"] for r in rows]),
                                  np.log([r["Z1"] for r in rows]), 1)[0] * np.log(2)))
    res["MM3_min_Z1_over_audit"] = float(min(a["Z1"] for a in audit))
    res["MM3_verdict"] = (
        "The exact inverse of the truncated assembled operator drives ||I - A L_M|| to "
        "float noise BY CONSTRUCTION -- that number is a statement about numpy.linalg.inv, "
        "not about the operator (lesson 86).  Made admissible -- finite rank up to M_A, "
        "then the only explicit operator available on the outer modes -- it does not merely "
        "fail to help, it is three to four orders of magnitude WORSE than the block-diagonal "
        f"baseline (minimum over the whole audit: {min(a['Z1'] for a in audit):.4g}), and it "
        "degrades as M_A grows while being essentially independent of M_L (the numbers at "
        "M_L = 1024 and 2048 agree to five digits).  That dependence is the tell: the cost "
        "lives at the SEAM where the finite-rank part meets the explicit tail, which is the "
        "same mismatch one level up.  The exact inverse is not a shape of A; it is the "
        "truncation.")
    print(f"      minimum over the whole audit: {res['MM3_min_Z1_over_audit']:.5g} -- "
          f"worse than the block-diagonal baseline by "
          f"{res['MM3_min_Z1_over_audit'] / res['MM2_block_diagonal_baseline']['Z1']:.4g}x")

    # -- MM5 the positive control -------------------------------------------
    print("\n[MM5] positive control through EVERY shape: Lambda^1 dissipation, unbordered")
    print("      tail, no far-field unknown.  If no shape reaches Z1 < 1, the leg is void.")
    ctrl = []
    for mu in (0.0, 0.1, 0.5, 1.0, 2.0, 4.0):
        for kind, p in CLASSES:
            border = "analytic" if mu == 0.0 else None
            ob = assemble(16, 16 + M_EXTRA, kind, p, gauge="null", mu=mu, border=border,
                          far_field=(mu == 0.0))
            row = {"mu": float(mu), "class": kind, "param": float(p),
                   "A_tail_norm": ob["A_tail_norm"], "by_shape": {}}
            for sh in ("block_diag", "gs_lower", "gs_upper", "schur"):
                m = measure(ob, sh)
                row["by_shape"][sh] = m["Z1"]
            ctrl.append(row)
            print(f"      mu={mu:.2f} {kind:9s} s={p:.1f}: " +
                  "  ".join(f"{sh[:9]}={row['by_shape'][sh]:10.4g}"
                            for sh in row["by_shape"]))
    res["MM5_positive_control"] = ctrl
    ok = [(r["mu"], sh, z) for r in ctrl if r["mu"] > 0
          for sh, z in r["by_shape"].items() if z < 1.0]
    res["MM5_control_can_report_below_one"] = bool(ok)
    res["MM5_min_mu_with_Z1_below_one"] = (min(o[0] for o in ok) if ok else None)
    res["MM5_shapes_that_reach_below_one"] = sorted({o[1] for o in ok})
    res["MM5_best_control_Z1"] = (float(min(o[2] for o in ok)) if ok else None)
    print(f"      control reaches Z1 < 1 for some mu > 0: "
          f"{res['MM5_control_can_report_below_one']} "
          f"(smallest mu {res['MM5_min_mu_with_Z1_below_one']}, shapes "
          f"{res['MM5_shapes_that_reach_below_one']}, best "
          f"{res['MM5_best_control_Z1']})")

    # -- MM5b the negative controls -----------------------------------------
    print("\n[MM5b] negative controls: the border direction is wired through the amplitude")
    print("       column, so a wrong direction changes Gamma and the control CAN fail")
    neg = []
    cases = [("analytic", 0), ("svd", 0), ("second", 0)]
    cases += [("random", s) for s in range(6)]        # several seeds, not one lucky draw
    for border, seed in cases:
        ob = assemble(16, 16 + M_EXTRA, "algebraic", 0.3, gauge="null", border=border,
                      seed=seed)
        row = {"border": border, "seed": seed, "Gamma_inv_norm": ob["Gamma_inv_norm"],
               "A_tail_norm": ob["A_tail_norm"], "by_shape": {}}
        for sh in ("block_diag", "gs_upper", "schur"):
            row["by_shape"][sh] = measure(ob, sh)["Z1"]
        neg.append(row)
        print(f"       border={border:9s} seed={seed}: "
              f"||Gamma^-1||={ob['Gamma_inv_norm']:11.5g}  " +
              "  ".join(f"{sh[:9]}={row['by_shape'][sh]:11.5g}" for sh in row["by_shape"]))
    res["MM5b_negative_controls"] = neg
    an = next(r for r in neg if r["border"] == "analytic")
    res["MM5b_ratios_to_analytic"] = {
        f"{r['border']}_{r['seed']}": {sh: float(r["by_shape"][sh] / an["by_shape"][sh])
                                       for sh in an["by_shape"]} for r in neg}
    wrong = [r for r in neg if r["border"] in ("second", "random")]
    res["MM5b_wrong_directions_are_worse_for_every_shape"] = bool(all(
        r["by_shape"][sh] > 2.0 * an["by_shape"][sh]
        for r in wrong for sh in an["by_shape"]))
    res["MM5b_shapes_where_a_wrong_border_is_BETTER"] = sorted({
        sh for r in wrong for sh in an["by_shape"] if r["by_shape"][sh] < an["by_shape"][sh]})
    res["MM5b_min_Z1_over_every_border_and_shape"] = float(
        min(r["by_shape"][sh] for r in neg for sh in r["by_shape"]))
    res["MM5b_honest_reading"] = (
        "The control DOES discriminate for the block-diagonal and gs_upper shapes -- the "
        "second singular pair makes the augmented block essentially singular (||Gamma^-1|| "
        "~ 2.1e+16) and a random direction is thousands of times worse.  IT DOES NOT "
        "DISCRIMINATE FOR THE SCHUR SHAPE, and that is reported rather than buried: with a "
        "random border the Schur shape's Z1 comes out SMALLER than with the analytic "
        "border, across every seed tried.  The mechanism is visible in the numbers -- the "
        "Schur complement S = G - B A_tail C partly undoes whatever the border did to "
        "Gamma, so the Schur shape is much less sensitive to the border than the "
        "block-diagonal one, which is a property of the shape and not a bug.  TWO "
        "CONSEQUENCES, both stated: (i) the border-direction control licenses the negative "
        "result for block_diag and gs_upper but NOT for schur, so for schur the negative "
        "rests on the mu-dial positive control (MM5) and on MM4's floor instead; (ii) the "
        "smallest Z1 anywhere in this table is "
        f"{min(r['by_shape'][sh] for r in neg for sh in r['by_shape']):.4f}, still well "
        "above 1, and chasing it would mean tuning the border direction, which is BANNED "
        "(plan_of_record.py) and was measured dead in leg 53.  It is recorded as an "
        "observation about the shape's border-sensitivity, not as a lane.")
    print(f"       wrong directions worse for EVERY shape: "
          f"{res['MM5b_wrong_directions_are_worse_for_every_shape']}  "
          f"(shapes where a wrong border is BETTER: "
          f"{res['MM5b_shapes_where_a_wrong_border_is_BETTER']})")
    print(f"       smallest Z1 anywhere in the border table: "
          f"{res['MM5b_min_Z1_over_every_border_and_shape']:.4f} -- still above 1, and "
          f"tuning the border is BANNED")

    # -- MM6 the polynomial --------------------------------------------------
    print("\n[MM6] the radii polynomial with the best ADMISSIBLE shape at each split")
    polys = []
    for kind, p in CLASSES:
        for K in K_SWEEP:
            ob = assemble(K, K + M_EXTRA, kind, p, gauge="null")
            ms = {sh: measure(ob, sh) for sh in SHAPES}
            bs = min((sh for sh in SHAPES if ADMISSIBLE[sh]), key=lambda s: ms[s]["Z1"])
            Z1 = ms[bs]["Z1"]
            rig = rigorous_finite_block(K, kind, p)
            qb = quadratic_bound(kind, p, K=min(max(K, 16), 96))
            A_norm = ms[bs]["A_norm"]
            Z2 = 2.0 * A_norm * qb
            Y0 = 0.0
            disc = (1.0 - Z1) ** 2 - 4.0 * Z2 * Y0
            r_max = (((1.0 - Z1) + np.sqrt(disc)) / (2.0 * Z2)) if disc >= 0 else None
            poly = {"class": kind, "param": float(p), "K": int(K), "best_shape": bs,
                    "Y0": Y0, "Z1": Z1, "Z2": Z2, "A_norm": A_norm,
                    "quadratic_bound": qb, "Z1_finite_block_rigorous": rig["Z1_finite"],
                    "discriminant": float(disc), "r_max": r_max,
                    "Z1_below_one": bool(Z1 < 1.0),
                    "has_positive_interval": bool(Z1 < 1.0 and r_max is not None
                                                  and r_max > 0.0)}
            polys.append(poly)
            print(f"      {kind:9s} s={p:.1f} K={K:3d}: best shape {bs:11s} "
                  f"Y0={Y0:.1e}  Z1={Z1:10.4g}  Z2={Z2:11.5g}  "
                  f"positive interval: {poly['has_positive_interval']}  "
                  f"r_max={r_max if r_max is not None else float('nan'):.3e}")
    res["MM6_polynomial"] = polys

    # -- the gate ------------------------------------------------------------
    closes = any(pp["has_positive_interval"] for pp in polys)
    res["gate_question"] = ("Does an approximate inverse that is NOT block diagonal bring "
                            "the assembled Z_1 below 1, on the a = 0 CLM object, in a class "
                            "with s < 0.394?")
    res["gate_answer"] = "yes" if closes else "no"
    res["gate_branch"] = ("POSITIVE_INTERVAL__RERUN_ON_HL_S2_NONSYMMETRIC" if closes else
                          "STOP_BUILDING_L1_FOURIER_RADII_POLYNOMIAL_CERTIFICATES_FOR_"
                          "INVISCID_SELF_SIMILAR_TRANSPORT")
    res["gate_smallest_Z1_admissible"] = float(m_adm["Z1"])
    res["gate_smallest_Z1_any_shape_including_inadmissible"] = float(m_any["Z1"])
    res["verdict"] = ("SHAPE_CLOSES_IT" if closes else
                      "NO_SHAPE_CLOSES_IT__FLOOR_IS_GAMMA_INV_ON_THE_FAR_FIELD_COLUMN")

    res["MM6_ceiling"] = (
        "Measured on the a = 0 CLM fixed point.  Y_0 is exactly zero there because the "
        "anchor IS one basis mode, so the polynomial's root r = 0 is available for a "
        "degenerate reason and certifies nothing; the reportable quantity is whether the "
        "inequality holds on a POSITIVE interval, which needs Z_1 < 1.  Nothing is claimed "
        "about HL_S2_nonsymmetric: on the gate's own terms that object is reached only if "
        "the polynomial closes here.")

    res["headline"] = {
        "smallest_Z1_over_every_admissible_shape_class_gauge_and_split":
            float(m_adm["Z1"]),
        "achieved_by": {"shape": sh_adm, "class": r_adm["class"], "param": r_adm["param"],
                        "gauge": r_adm["gauge"], "K": r_adm["K"]},
        "block_diagonal_baseline": float(res["MM2_block_diagonal_baseline"]["Z1"]),
        "improvement_factor": float(res["MM2_improvement_over_block_diagonal"]),
        "shape_independent_floor": float(res["MM4_min_floor"]),
        "required": 1.0,
        "statement": (
            "Spending the last free choice -- the SHAPE of A -- is worth a factor of "
            f"{res['MM2_improvement_over_block_diagonal']:.2f} at the best split and leaves "
            f"the assembled Z_1 at {m_adm['Z1']:.4f}, against the 1 it must be under.  The "
            "improvement is real and it is measured, and it is roughly forty times too "
            "small.  The floor is not an artefact of the three shapes tried: because the "
            "tail operator is singular on exactly the far-field direction the certificate "
            "borders, the coupling along that direction reduces to Gamma^-1 applied to the "
            "far-field column, in which the off-diagonal block of A has dropped out "
            f"algebraically.  That floor is {res['MM4_min_floor']:.4f} at its smallest over "
            "every class and every split from K = 2 to 64.")}

    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)")
    print(f"GATE: {res['gate_answer'].upper()} -- {res['gate_branch']}")
    print(f"VERDICT: {res['verdict']}")
    print(f"smallest Z1 over every admissible shape: {m_adm['Z1']:.4f} "
          f"(block-diagonal baseline {res['MM2_block_diagonal_baseline']['Z1']:.4f}, "
          f"shape-independent floor {res['MM4_min_floor']:.4f}, required < 1)")


if __name__ == "__main__":
    main()
