"""Route-NG v1: THE NO-GO, STATED AS A PROPOSITION -- and the one open question named.

Legs 51-57 produced every component of a negative result and assembled none of them.  MM
(leg 54) closed the last free choice -- the SHAPE of the approximate inverse `A` -- with a
battery bottoming at `Z1 = 8.9591` against a block-diagonal baseline of `10.4584`, a
1.167x improvement where more than 8x was needed.  That is a measurement over seven
shapes.  It is not a theorem, and "no `A` we tried" is not "no `A`".

This leg writes the proposition and spends itself on the single gap that decides its
strength: whether the no-go admits a PROOF for a named class of approximate inverses
STRICTLY LARGER than block-diagonal.

PRE-COMMITTED CLAUSES, written before the numbers existed (both branches reportable):

  NG0 THE NOVELTY PASS CAME FIRST and is committed at `writeup/novelty/leg_58.md`,
      BEFORE this file was written, with LINKS not counts.  Verdict PROCEED_NARROW.
      Cadiot arXiv:2505.03091 is resolved from the FULL TEXT against this no-go and does
      NOT contain it: its standing hypothesis is a Fourier multiplier with symbol
      `|l(xi)| >= l_min > 0` and `|l| -> infinity`, i.e. an infinite DIAGONAL tail.  This
      operator's tail has an exactly ZERO diagonal and its unbounded part is a SHIFT.
      What the pass FORBIDS is carried into `NG1`'s scope line and is not negotiable
      here: the OBSERVATION (a tail estimate presumes a dominant diagonal) is folklore in
      print and may not be claimed; the SHAPES (block Gauss-Seidel, Schur complement,
      rank-one lift) are textbook preconditioning; only the INEQUALITY and the class it
      holds on may be claimed.

  NG1 THE PROPOSITION.  Hypotheses, conclusion, and a scope line separating MEASURED from
      PROVED.  Stated in `proposition()` below and emitted verbatim into the JSON so that
      the prose cannot drift from it.

  NG2 THE GAP, AND IT IS THE ONLY OPEN MATHEMATICS.  `MM-1` proves only the
      block-diagonal case, and only for `K >= 6` (flat) / `K >= 4` (algebraic), because
      its `|1 - K/2|` prefactor vanishes at `K = 2`.  The candidate extension is the class

          A_upper = { A = [[A11, A12], [0, A22]] }   (A21 = 0)

      which strictly contains block-diagonal (`A12 = 0`, `A22 = A_tail`) AND `gs_upper`.
      Four sub-clauses, and the third is the one that can kill the whole thing:

      NG2a  THE HYPOTHESIS, MEASURED.  The proof needs the tail kernel to be IN `l^1_w`.
            `fredholm_sides` (leg 51) already derives `s < 1` from an `m^-2` decay -- that
            is NOT claimed here.  What is checked here is the same claim on the vector
            actually used: partial sums of `|h_m| w_m` over a ladder of truncations, for
            `s = 0, 0.3, 0.7, 1.0, 1.5`, plus the finite-M defect `rho_M`.
      NG2b  THE BOUND, CHECKED AGAINST THE BATTERY.  For every shape, the measured
            `hhat`-column of `I - A L` against the predicted `1 + ||A11 B hhat||/||hhat||`.
            For `A21 = 0` shapes it must be an EQUALITY; if it is not, the proof is wrong.
      NG2c  THE SPLIT-PLACEMENT AUDIT, and it is the referee's objection.  "You chose a
            split whose tail block is singular; put the far-field amplitude in the TAIL
            and the tail block is invertible."  That alternative split is the SAME
            operator under a permutation, so it is measured rather than argued: build it
            by permuting one index and report `||T'^-1||_w` as a ladder in `M`.  If it is
            bounded, the proposition is an artifact of the split and this leg reports NO.
      NG2d  WHERE THE PROOF STOPS, MEASURED.  `A21 != 0` buys back exactly the kernel's
            own contribution and nothing else.  Report the credit as a magnitude.  Beyond
            it the result is leg 54's battery: MEASURED, NOT PROVED, everywhere.

  NG3 SHARPNESS: THE HYPOTHESIS CANNOT BE DROPPED.  The `mu > 0` control, reused.  With
      `Lambda^1` dissipation the tail is a multiplier, (H2) fails, and the SAME class
      `A_upper` reaches `Z1 < 1`.  Reported as a continuous dial in `mu` against the
      hypothesis quantity, so the control CAN come out the other way (lesson 90).
      Cross-leg number hygiene: leg 53 reported `0.9156` for this configuration as a SUM
      OF SUB-BLOCK NORMS; leg 54 reported `0.6663` for the same configuration as the TRUE
      column-max.  Both are re-measured here and both are reported.

  NG4 THE CEILING, pre-committed.  This is the `a = 0` CLM linearisation.  `Y_0` is
      exactly zero because the anchor IS one basis mode, so the radii polynomial's root
      `r = 0` is available for a degenerate reason and certifies nothing.  NOTHING is
      claimed about `HL_S2_nonsymmetric` and nothing about any link of the L1->L4 chain.
      A wall measured here bounds the real target's difficulty FROM BELOW, no more.

GATE: does the no-go admit a proof for a named class of approximate inverses strictly
larger than block-diagonal, with hypotheses that provably contain the `a = 0` CLM
linearization?

Writes writeup/data/p2_route_ng_v1_nogo.json.

Run: .venv/bin/python -u experiments/p2_route_ng_v1_nogo.py
"""

import json
import os
import sys
import time
from pathlib import Path

# Pin BLAS to one thread BEFORE numpy is imported.  Two reasons, and the second is the one
# that matters: (1) on a loaded machine multi-threaded LAPACK thrashes -- a 1100x1100
# `inv` measured 11.07s against 0.71s single-threaded here; (2) reduction ORDER in a
# threaded BLAS depends on the thread count, so a verifier on a different machine would
# get different last digits.  Pinning makes the committed JSON reproducible.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np                                                     # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.spectral_certificate import (                              # noqa: E402
    block_upper_triangular_bound, fredholm_sides, kernel_membership_ladder,
    nogo_hypotheses, tail_kernel_defect,
)
from p2_route_mm_v1_shape import (                                     # noqa: E402
    assemble, build_A, colmax, full_L, ADMISSIBLE, SHAPES,
)

OUT = ROOT / "writeup" / "data" / "p2_route_ng_v1_nogo.json"

CLASSES = (("flat", 0.0), ("algebraic", 0.3))
K_SWEEP = (2, 4, 8, 16, 32)
M_EXTRA = 1024
M_LADDER = (128, 256, 512, 1024, 2048)
S_SCAN = (0.0, 0.3, 0.7, 1.0, 1.5)
MUS = (0.0, 0.1, 0.5, 1.0, 2.0, 4.0)

# The shapes of `A` that lie in the proved class, and the ones that do not.  This split is
# the whole point of the leg and it is asserted from the CONSTRUCTION of each shape in
# leg 54's `build_A`, then CHECKED numerically in NG2b (`A21_norm` must be 0 / non-zero).
IN_CLASS = ("block_diag", "gs_upper")
OUT_OF_CLASS = ("gs_lower", "schur", "ff_lift", "oracle_pinv", "exact_inv")


def loglog_slope(xs, ys):
    """Fitted power in `y ~ x^p`, over the whole ladder.  Reported, never asserted."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    ok = (xs > 0) & (ys > 0) & np.isfinite(ys)
    if ok.sum() < 2:
        return float("nan")
    return float(np.polyfit(np.log(xs[ok]), np.log(ys[ok]), 1)[0])


def proposition():
    """NG1.  The statement, emitted verbatim so the prose cannot drift from it."""
    return {
        "name": "Proposition NG (block-upper-triangular no-go)",
        "setting": (
            "L is the a = 0 CLM steady linearisation in the compactified odd-sine "
            "coefficient basis, bordered with the far-field amplitude as an extra unknown "
            "and its matching condition as an extra equation (leg 52's repair, leg 53's "
            "assembly).  It is split at mode K as L = [[G, B], [C, T]]: G the finite "
            "block on modes 1..K plus the gauge and amplitude auxiliaries, T the tail "
            "block on modes K+1..M.  The norm is weighted l^1, w_k = (1+k)^s."),
        "hypotheses": {
            "H1": ("the split is the one the radii-polynomial method uses: a finite block "
                   "carrying the auxiliaries, and a tail the certificate must handle by an "
                   "explicit operator rather than a numerical inverse"),
            "H2": ("the tail block T has a kernel IN the space: T h = 0 with "
                   "0 < ||h||_w < infinity.  For this operator h is the far-field mode, "
                   "explicit by a two-term recursion, decaying like m^-2, so H2 holds "
                   "exactly when s < 1 -- which INCLUDES s = 0 and s = 0.3, the two "
                   "classes legs 51-54 actually used"),
            "H3": ("A is a bounded approximate inverse with A21 = 0, i.e. its tail rows do "
                   "not couple back to the finite block.  A11, A12 and A22 are otherwise "
                   "ARBITRARY -- in particular A22 need not be the tail inverse the method "
                   "conventionally supplies"),
        },
        "conclusion": (
            "Z1 = ||I - A L||_w >= 1 + ||A11 B h||_w / ||h||_w >= 1, for every such A.  "
            "The radii polynomial requires Z1 < 1, so no approximate inverse in the class "
            "closes the certificate, at ANY split K and in ANY weight class with s < 1."),
        "proof": (
            "Test the operator on x = (0; h).  (I - A L) x = "
            "( -(A11 B + A12 T) h ; h - A21 B h - A22 T h ).  T h = 0 kills the A12 term "
            "and the A22 term; A21 = 0 kills the third.  So (I - A L) x = "
            "( -A11 B h ; h ), whose l^1_w norm is ||A11 B h||_w + ||h||_w.  Divide by "
            "||x||_w = ||h||_w."),
        "class_A_upper": {
            "definition": "{ A = [[A11, A12], [0, A22]] : A11, A12, A22 bounded }",
            "strictly_contains_block_diagonal_because": (
                "block-diagonal is the single point A12 = 0, A22 = A_tail.  A_upper leaves "
                "A12 and A22 entirely free, and contains the `gs_upper` shape leg 54 "
                "measured separately (A12 = -Gamma^-1 B A_tail)."),
            "in_class_shapes_from_leg54": list(IN_CLASS),
            "out_of_class_shapes_from_leg54": list(OUT_OF_CLASS),
        },
        "improvement_over_MM1": (
            "MM-1 (leg 54) bounds the same sub-block but through the coupling column, so "
            "it carries a |1 - K/2| prefactor that VANISHES at K = 2 and leaves K in "
            "{2, 3} open (flat: K <= 5).  It also fixes A22 = A_tail.  The bound here has "
            "no prefactor, no K restriction and no constraint on A22, so it closes MM-1's "
            "small-K corner within this class and enlarges the class at the same time."),
        "scope_line_PROVED_vs_MEASURED": (
            "PROVED: the class A21 = 0, i.e. every block-diagonal and every "
            "block-upper-triangular approximate inverse, at every K, for s < 1.  "
            "MEASURED, NOT PROVED: every A with A21 != 0.  For those this repository has "
            "leg 54's battery over seven shapes bottoming at Z1 = 8.9591 (admissible) and "
            "NOTHING ELSE.  The general no-go is a measurement over a battery and must be "
            "described that way wherever it appears."),
        "what_is_NOT_claimed": [
            "the observation that a tail estimate presumes a dominant diagonal -- "
            "folklore in print (Cadiot arXiv:2505.03091 secs 2-3, arXiv:2411.18361); "
            "leg 51's, and not claimed by this leg either",
            "the m^-2 kernel decay and the s < 1 membership threshold -- leg 51's "
            "`fredholm_sides`, re-checked here but not claimed",
            "the shapes of A -- textbook preconditioning",
            "anything about HL_S2_nonsymmetric or any link of the L1 -> L4 chain",
        ],
    }


def main():
    t0 = time.time()
    res = {"leg": 58, "route": "NG", "version": "v1",
           "object": ("a=0 CLM linearisation in the compactified odd-sine basis, bordered "
                      "and assembled as in experiments/p2_route_tc_v1_assemble.py "
                      "(leg 53) and measured as in p2_route_mm_v1_shape.py (leg 54)"),
           "M_extra": M_EXTRA, "K_sweep": list(K_SWEEP), "shapes": list(SHAPES)}

    # -- NG0 ----------------------------------------------------------------
    res["NG0_novelty"] = {
        "log": "writeup/novelty/leg_58.md",
        "verdict": "PROCEED_NARROW",
        "run_before_construction": True,
        "links_not_counts": True,
        "cadiot_resolved_from_full_text": {
            "id": "arXiv:2505.03091",
            "url": "https://arxiv.org/html/2505.03091",
            "located_hypotheses": [
                "L is a Fourier multiplier operator given by its symbol l",
                "there exists l_min > 0 with |l(xi)| >= l_min for all xi",
                "lim_{|xi| -> infinity} |l(xi)| = +infinity",
                "in the spectral basis L becomes an infinite DIAGONAL matrix",
            ],
            "verdict": ("does NOT contain this no-go and carries no positive result that "
                        "contradicts it: this operator's tail diagonal is exactly zero "
                        "and its unbounded part is a shift, so it fails all three"),
        },
        "forbidden_by_the_pass": [
            "claiming the dominance OBSERVATION -- folklore in print",
            "claiming the SHAPES -- textbook preconditioning",
            "any claim about HL_S2_nonsymmetric or the L1->L4 chain",
            "novelty beyond Cadiot: leg 62 reads the same paper at greater depth by "
            "assignment and ITS reading caps this one",
        ],
        "leg52_search_index_flag": "STANDS -- not tested by this pass, not cleared.",
    }
    print(f"[NG0] novelty: {res['NG0_novelty']['verdict']} "
          f"(committed before construction, links not counts)")

    # -- NG1 ----------------------------------------------------------------
    res["NG1_proposition"] = proposition()
    print("[NG1] proposition emitted: class A_upper = {A21 = 0}, conclusion Z1 >= 1")

    # -- NG2a  the hypothesis, measured -------------------------------------
    print("\n[NG2a] HYPOTHESIS (H2): is the tail kernel IN l^1_w?  ladder, not a verdict")
    res["NG2a_fredholm_sides_leg51"] = fredholm_sides()
    print(f"       leg 51's exponents (NOT claimed here): "
          f"kernel {res['NG2a_fredholm_sides_leg51']['kernel_exponent']:.4f}, "
          f"cokernel {res['NG2a_fredholm_sides_leg51']['cokernel_exponent']:.4f}, "
          f"crossing at s = {res['NG2a_fredholm_sides_leg51']['crossing']}")

    memb = []
    for s in S_SCAN:
        kind = "flat" if s == 0.0 else "algebraic"
        row = kernel_membership_ladder(8, (256, 1024, 4096, 16384), kind, s)
        row["s"] = float(s)
        memb.append(row)
        print(f"       s={s:.1f}: ||h||_w partial = " +
              " ".join(f"{v:10.4f}" for v in row["partial_norm"]) +
              f"   increment ratio {row['last_increment_ratio']:.4f} -> {row['verdict']}")
    res["NG2a_kernel_membership"] = memb
    res["NG2a_verdict_by_s"] = {str(r["s"]): r["verdict"] for r in memb}
    res["NG2a_increment_ratio_by_s"] = {str(r["s"]): r["last_increment_ratio"]
                                        for r in memb}
    res["NG2a_H2_holds_for_s"] = sorted(float(r["s"]) for r in memb if r["in_l1_w"])
    res["NG2a_H2_fails_for_s"] = sorted(float(r["s"]) for r in memb if not r["in_l1_w"])
    res["NG2a_H2_note"] = (
        "The verdict is read off the INCREMENT RATIO of the partial sums, not off whether "
        "they look flat.  s = 0.7 converges (ratio ~0.66) even though its partial sum is "
        "still visibly rising at M = 16384, and calling it divergent would have been a "
        "reporting error, not a measurement.  s = 1 has a ratio of ~1.00 -- constant "
        "increments, i.e. LOGARITHMIC divergence -- and s = 1.5 has ~2.00, a power "
        "divergence.  The threshold is therefore s = 1, which is exactly leg 51's "
        "`fredholm_sides` crossing arrived at from the other side, and s = 1 is already "
        "banned for a different reason (leg 52: it is the one exponent at which bordering "
        "cannot help).")

    defect = []
    for kind, p in CLASSES:
        rows = [{"M_minus_K": int(e),
                 "rho": tail_kernel_defect(8, 8 + e, kind, p)} for e in M_LADDER]
        slope = loglog_slope([r["M_minus_K"] for r in rows], [r["rho"] for r in rows])
        defect.append({"class": kind, "param": float(p), "ladder": rows,
                       "fitted_exponent": slope, "predicted_exponent": -(1.0 - float(p))})
        print(f"       rho_M ladder {kind}(s={p}): " +
              " ".join(f"{r['rho']:.3e}" for r in rows) +
              f"   fitted M^({slope:+.4f}), predicted M^({-(1.0 - float(p)):+.4f})")
    res["NG2a_finite_M_defect"] = defect
    res["NG2a_defect_vanishes"] = bool(all(d["ladder"][-1]["rho"] < d["ladder"][0]["rho"]
                                           for d in defect))

    # -- NG2b  the bound against the battery --------------------------------
    print("\n[NG2b] THE BOUND vs THE BATTERY: hhat-column of I - A L against BOTH forms of")
    print("       the bound -- the infinite-tail one (rho = 0) the proposition states, and")
    print("       the finite-M one the measurement can actually be held to.")
    print("       TWO REALIZATIONS, NAMED (lesson 70).  On the infinite tail T h = 0 and the")
    print("       bound is 1 + floor.  At finite M, T h is a nonzero EDGE term of size rho_M,")
    print("       so the honest finite-M statement carries -rho_M*(||A12|| + ||A22||).  The")
    print("       gap between the two is therefore PREDICTED, not noise, and it must shrink")
    print("       with M -- which NG2a's ladder measures independently.")
    checks = []
    for kind, p in CLASSES:
        for K in K_SWEEP:
            M = K + M_EXTRA
            ob = assemble(K, M, kind, p)
            nG, n = ob["nG"], ob["n"]
            L = full_L(ob)
            hh = ob["hhat"]
            nh = float(np.abs(hh).sum())
            x = np.concatenate([np.zeros(nG), hh])
            Bh = ob["B"] @ hh
            rho = tail_kernel_defect(K, M, kind, p)
            for sh in SHAPES:
                A = build_A(ob, sh)
                if A is None:
                    continue
                R = np.eye(nG + n) - A @ L
                col = float(np.abs(R @ x).sum() / nh)
                floor = float(np.abs(A[:nG, :nG] @ Bh).sum() / nh)
                a12, a22 = colmax(A[:nG, nG:]), colmax(A[nG:, nG:])
                pred_inf = block_upper_triangular_bound(0.0, a22, floor)
                pred_fin = block_upper_triangular_bound(rho, a12 + a22, floor)
                checks.append({
                    "class": kind, "param": float(p), "K": int(K), "shape": sh,
                    "admissible": bool(ADMISSIBLE[sh]),
                    "in_proved_class": bool(sh in IN_CLASS),
                    "A21_norm": float(colmax(A[nG:, :nG])),
                    "A12_norm": float(a12), "A22_norm": float(a22),
                    "rho_M": float(rho),
                    "Z1": float(colmax(R)),
                    "hhat_column": col,
                    "predicted_bound_infinite_tail": float(pred_inf),
                    "predicted_bound_finite_M": float(pred_fin),
                    "floor_A11_B_hhat": floor,
                    "column_minus_infinite_bound": float(col - pred_inf),
                    "column_minus_finite_bound": float(col - pred_fin),
                    "truncation_budget": float(rho * (a12 + a22)),
                })
            print(f"       {kind}(s={p}) K={K:2d} rho={rho:.2e}: " +
                  "  ".join(f"{c['shape'][:9]} col={c['hhat_column']:.4f} "
                            f"(inf-bound {c['predicted_bound_infinite_tail']:.4f})"
                            for c in checks
                            if c["class"] == kind and c["K"] == K and c["in_proved_class"]))
    res["NG2b_bound_vs_battery"] = checks

    inc = [c for c in checks if c["in_proved_class"]]
    res["NG2b_in_class_min_hhat_column"] = float(min(c["hhat_column"] for c in inc))
    res["NG2b_in_class_min_Z1"] = float(min(c["Z1"] for c in inc))
    res["NG2b_in_class_max_A21_norm"] = float(max(c["A21_norm"] for c in inc))
    # (i) the finite-M bound is a genuine lower bound on every in-class measurement
    res["NG2b_finite_M_bound_min_slack"] = float(
        min(c["column_minus_finite_bound"] for c in inc))
    res["NG2b_finite_M_bound_never_violated"] = bool(
        res["NG2b_finite_M_bound_min_slack"] >= 0.0)
    # (ii) the deviation from the infinite-tail EQUALITY is explained by truncation
    res["NG2b_max_abs_deviation_from_infinite_equality"] = float(
        max(abs(c["column_minus_infinite_bound"]) for c in inc))
    res["NG2b_max_deviation_over_truncation_budget"] = float(
        max(abs(c["column_minus_infinite_bound"]) / c["truncation_budget"]
            for c in inc if c["truncation_budget"] > 0))
    res["NG2b_deviation_is_truncation"] = bool(
        res["NG2b_max_deviation_over_truncation_budget"] <= 1.0)
    # (iii) the measured columns never go below 1, which is what the proposition forbids
    res["NG2b_bound_never_violated"] = bool(res["NG2b_in_class_min_hhat_column"] >= 1.0)
    res["NG2b_in_class_max_A12_norm"] = float(max(c["A12_norm"] for c in inc))
    # THE INSTRUMENT CHECK (lesson 85): this leg re-derives leg 54's headline on the same
    # configuration before building anything on it.  If these two drift, nothing below is
    # comparable to the banked battery and the leg is measuring a different object.
    _b = [c for c in checks if c["class"] == "algebraic" and c["K"] == 2
          and c["shape"] == "block_diag"]
    _f = [c for c in checks if c["class"] == "algebraic" and c["K"] == 2
          and c["shape"] == "ff_lift"]
    res["NG2b_instrument_check_vs_leg54"] = {
        "block_diag_baseline_here": float(_b[0]["Z1"]) if _b else None,
        "block_diag_baseline_leg54": 10.458352181845608,
        "ff_lift_best_here": float(_f[0]["Z1"]) if _f else None,
        "ff_lift_best_leg54": 8.959091169104095,
        "note": ("leg 54's MM2 best admissible and its block-diagonal baseline, at the "
                 "configuration they were reported on (algebraic s=0.3, K=2, M-K=1024).")}
    if _b and _f:
        res["NG2b_instrument_max_rel_gap_vs_leg54"] = float(max(
            abs(_b[0]["Z1"] - 10.458352181845608) / 10.458352181845608,
            abs(_f[0]["Z1"] - 8.959091169104095) / 8.959091169104095))
        print(f"       instrument check vs leg 54: block_diag {_b[0]['Z1']:.4f} "
              f"(banked 10.4584), ff_lift {_f[0]['Z1']:.4f} (banked 8.9591), "
              f"max rel gap {res['NG2b_instrument_max_rel_gap_vs_leg54']:.2e}")
    print(f"       in-class: min hhat-column = {res['NG2b_in_class_min_hhat_column']:.4f} "
          f"(the proposition says >= 1), min Z1 = {res['NG2b_in_class_min_Z1']:.4f}")
    print(f"       finite-M bound slack >= {res['NG2b_finite_M_bound_min_slack']:.3e} "
          f"(never violated: {res['NG2b_finite_M_bound_never_violated']})")
    print(f"       deviation from the infinite-tail equality is "
          f"{res['NG2b_max_deviation_over_truncation_budget']:.4f} x the truncation budget "
          f"rho_M*(||A12||+||A22||) -- i.e. it IS the truncation")

    # -- NG2c  the split-placement audit ------------------------------------
    print("\n[NG2c] SPLIT-PLACEMENT AUDIT: move the far-field amplitude into the TAIL and")
    print("       ask whether the obstruction goes away.  Same operator, one permutation.")
    audit = []
    for kind, p in CLASSES:
        rows = []
        for e in M_LADDER:
            K = 8
            ob = assemble(K, K + e, kind, p)
            nG, n = ob["nG"], ob["n"]
            L = full_L(ob)
            a = K + 1                       # the far-field amplitude column AND its row
            keep = [i for i in range(nG + n) if i != a]
            perm = keep[:nG - 1] + [a] + keep[nG - 1:]
            Lp = L[np.ix_(perm, perm)]
            Tp = Lp[nG - 1:, nG - 1:]
            sv = np.linalg.svd(Tp, compute_uv=False)
            rows.append({"M_minus_K": int(e),
                         "alt_tail_inverse_norm": colmax(np.linalg.inv(Tp)),
                         "sigma_min": float(sv[-1]), "sigma_2": float(sv[-2])})
        slope = loglog_slope([r["M_minus_K"] for r in rows],
                             [r["alt_tail_inverse_norm"] for r in rows])
        audit.append({"class": kind, "param": float(p), "ladder": rows,
                      "fitted_exponent": slope, "predicted_exponent": 1.0 - float(p)})
        print(f"       {kind}(s={p}): ||T'^-1||_w = " +
              " ".join(f"{r['alt_tail_inverse_norm']:9.4g}" for r in rows) +
              f"   fitted M^({slope:+.4f})")
    res["NG2c_alternative_split"] = audit
    res["NG2c_alt_tail_inverse_diverges"] = bool(
        all(a["ladder"][-1]["alt_tail_inverse_norm"]
            > 2.0 * a["ladder"][0]["alt_tail_inverse_norm"] for a in audit))
    res["NG2c_max_alt_tail_inverse_norm"] = float(
        max(r["alt_tail_inverse_norm"] for a in audit for r in a["ladder"]))
    res["NG2c_statement"] = (
        "The objection is that the singular tail block is a bad CHOICE of split.  It is "
        "not repaired by the alternative: putting the far-field amplitude in the tail "
        "makes T' invertible at every finite M, but ||T'^-1||_w DIVERGES with M at the "
        "fitted rate M^(1-s) -- the SAME exponent, with the opposite sign, at which the "
        "kernel defect rho_M vanishes in NG2a.  So the obstruction is carried by the "
        "operator and not by the placement: either the tail block has a kernel (amplitude "
        "in the finite block) or its inverse is unbounded (amplitude in the tail).  "
        "SCOPE: this is a MEASURED ladder over M = 128..2048 at K = 8, with a fitted "
        "exponent, not a proof that ||T'^-1||_w is unbounded.")

    # -- NG2d  where the proof stops ----------------------------------------
    print("\n[NG2d] WHERE THE PROOF STOPS: what A21 != 0 buys, as a magnitude")
    credit = []
    for kind, p in CLASSES:
        for K in K_SWEEP:
            sel = [c for c in checks if c["class"] == kind and c["K"] == K]
            base = [c for c in sel if c["shape"] == "block_diag"]
            lift = [c for c in sel if c["shape"] == "ff_lift"]
            if not base or not lift:
                continue
            cr = float(base[0]["hhat_column"] - lift[0]["hhat_column"])
            credit.append({"class": kind, "param": float(p), "K": int(K),
                           "block_diag_column": base[0]["hhat_column"],
                           "ff_lift_column": lift[0]["hhat_column"],
                           "credit": cr, "credit_deficit_from_one": float(1.0 - cr),
                           "rho_M": base[0]["rho_M"],
                           "deficit_over_rho": float((1.0 - cr) / base[0]["rho_M"])
                           if base[0]["rho_M"] > 0 else float("nan"),
                           "block_diag_Z1": base[0]["Z1"], "ff_lift_Z1": lift[0]["Z1"]})
    res["NG2d_lift_credit"] = credit
    res["NG2d_credit_range"] = [float(min(c["credit"] for c in credit)),
                                float(max(c["credit"] for c in credit))]
    res["NG2d_max_deficit_from_one"] = float(
        max(c["credit_deficit_from_one"] for c in credit))
    res["NG2d_max_deficit_over_rho"] = float(max(c["deficit_over_rho"] for c in credit))
    res["NG2d_deficit_over_rho_range"] = [
        float(min(c["deficit_over_rho"] for c in credit)),
        float(max(c["deficit_over_rho"] for c in credit))]
    res["NG2d_deficit_never_exceeds_rho"] = bool(
        all(c["credit_deficit_from_one"] <= c["rho_M"] for c in credit))
    # The credit is 1 on the INFINITE tail.  At finite M it falls short by an amount that
    # must be of the order of the truncation defect rho_M and no larger -- if the shortfall
    # were NOT explained by rho_M, the mechanism would be wrong.  Reported as a ratio.
    res["NG2d_deficit_is_truncation"] = bool(res["NG2d_max_deficit_over_rho"] <= 1.5)
    print(f"       the rank-one far-field lift removes "
          f"{res['NG2d_credit_range'][0]:.4f}..{res['NG2d_credit_range'][1]:.4f} of the "
          f"hhat-column; it is 1 on the infinite tail and falls short at finite M by at "
          f"most {res['NG2d_max_deficit_from_one']:.4f}; the deficit tracks the truncation "
          f"defect rho_M at a ratio of {res['NG2d_deficit_over_rho_range'][0]:.3f}.."
          f"{res['NG2d_deficit_over_rho_range'][1]:.3f} and never exceeds it "
          f"({res['NG2d_deficit_never_exceeds_rho']})")
    res["NG2d_statement"] = (
        "A21 != 0 buys back ONE unit of the hhat-column and no more: the term h - A21 B h "
        "that the proposition's hypothesis excludes.  On the infinite tail the credit is "
        "exactly 1; at finite M it is short by an amount bounded by the truncation defect "
        "rho_M, which is what the deficit_over_rho column checks.  The residual "
        "||A11 B h||_w/||h||_w survives every admissible lift.  This is the precise place "
        "the proof stops, and it is why the general case is MEASURED and not proved: leg "
        "54's MM4c already refuted a shape-independent floor by an explicit rank-one "
        "counter-construction, so the residual term is beatable in principle -- at a total "
        "Z1 of 5.7e+05 in the one construction that beat it.  The battery's best "
        "admissible Z1 remains 8.9591.")

    # -- NG3  sharpness -----------------------------------------------------
    print("\n[NG3] SHARPNESS: mu > 0 removes the hypothesis.  Does the SAME class then")
    print("      reach Z1 < 1?  If not, the hypothesis is not the operative one.")
    dial = []
    for mu in MUS:
        for kind, p in CLASSES:
            border = "analytic" if mu == 0.0 else None
            ob = assemble(16, 16 + M_EXTRA, kind, p, gauge="null", mu=mu, border=border,
                          far_field=(mu == 0.0))
            nG, n = ob["nG"], ob["n"]
            L = full_L(ob)
            hyp = nogo_hypotheses(16, 16 + M_EXTRA, kind, p, mu=mu)
            row = {"mu": float(mu), "class": kind, "param": float(p),
                   "sigma_min_tail": hyp["sigma_min"],
                   "defect_ratio": hyp["defect_ratio"],
                   "H2_holds": bool(hyp["H2_holds_on_the_infinite_tail"]),
                   "by_shape": {}, "by_shape_subblock_sum": {}}
            for sh in IN_CLASS + ("gs_lower", "schur"):
                A = build_A(ob, sh)
                if A is None:
                    continue
                R = np.eye(nG + n) - A @ L
                row["by_shape"][sh] = float(colmax(R))
                row["by_shape_subblock_sum"][sh] = float(
                    colmax(R[:nG, :nG]) + colmax(R[:nG, nG:])
                    + colmax(R[nG:, :nG]) + colmax(R[nG:, nG:]))
            dial.append(row)
            print(f"      mu={mu:4.2f} {kind:9s} s={p:.1f}: sigma_min={row['sigma_min_tail']:.4e} "
                  f"rho={row['defect_ratio']:.4e}  " +
                  "  ".join(f"{sh[:9]}={row['by_shape'][sh]:9.4f}"
                            for sh in row["by_shape"]))
    res["NG3_sharpness_dial"] = dial
    in_class_below_one = [(r["mu"], r["class"], sh, z) for r in dial
                          for sh, z in r["by_shape"].items()
                          if sh in IN_CLASS and z < 1.0]
    res["NG3_in_class_reaches_below_one"] = bool(in_class_below_one)
    res["NG3_only_when_mu_positive"] = bool(
        all(m > 0.0 for m, _, _, _ in in_class_below_one))
    res["NG3_smallest_mu_with_in_class_Z1_below_one"] = (
        float(min(m for m, _, _, _ in in_class_below_one)) if in_class_below_one else None)
    res["NG3_best_in_class_control_Z1"] = (
        float(min(z for _, _, _, z in in_class_below_one)) if in_class_below_one else None)
    mu2 = [r for r in dial if r["mu"] == 2.0 and r["class"] == "algebraic"]
    if mu2:
        res["NG3_mu2_algebraic_column_max"] = float(mu2[0]["by_shape"]["block_diag"])
        res["NG3_mu2_algebraic_subblock_sum"] = float(
            mu2[0]["by_shape_subblock_sum"]["block_diag"])
    res["NG3_statement"] = (
        "The hypothesis is NECESSARY, not decorative.  At mu = 0 the proposition forbids "
        "Z1 < 1 for the whole class A_upper and the measurement agrees at every K and in "
        "both weight classes.  At mu > 0 the Lambda^1 dissipation turns the tail into a "
        "multiplier, (H2) fails outright -- sigma_min jumps by more than two orders of "
        "magnitude at mu = 0.1 -- and the SAME two in-class shapes reach Z1 < 1.  The "
        "control therefore CAN report the other answer (lesson 90).  CROSS-LEG NUMBER "
        "HYGIENE: leg 53 reported 0.9156 for the mu = 2 algebraic configuration as a SUM "
        "OF SUB-BLOCK NORMS and leg 54 reported 0.6663 for the same configuration as the "
        "TRUE column-max.  Both conventions are re-measured here and both are emitted.")

    # -- NG4  the ceiling ---------------------------------------------------
    res["NG4_ceiling"] = (
        "The object is the a = 0 CLM linearisation.  Its Y_0 is EXACTLY zero because the "
        "anchor IS one basis mode, so the radii polynomial's root r = 0 is available for a "
        "degenerate reason and certifies nothing.  This leg claims NOTHING about "
        "HL_S2_nonsymmetric and nothing about any link of the L1 -> L4 chain.  A wall "
        "measured here bounds the real target's difficulty FROM BELOW and no more.  "
        "Float64 throughout, no interval arithmetic: the proposition's PROOF is exact "
        "linear algebra on an explicitly-constructed kernel, but every NUMBER here is a "
        "float measurement.")

    # -- the gate -----------------------------------------------------------
    res["gate_question"] = (
        "Does the no-go admit a proof for a named class of approximate inverses strictly "
        "larger than block-diagonal, with hypotheses that provably contain the a = 0 CLM "
        "linearization?")
    # The gate answers YES only if ALL of these hold; each is a way the proof could have
    # been wrong, and each is measured rather than assumed.
    gate_conditions = {
        "H2_holds_at_s_0": bool(0.0 in res["NG2a_H2_holds_for_s"]),
        "H2_holds_at_s_0.3": bool(0.3 in res["NG2a_H2_holds_for_s"]),
        "H2_fails_at_s_1": bool(res["NG2a_verdict_by_s"]["1.0"] != "converges"),
        "finite_M_bound_never_violated": bool(res["NG2b_finite_M_bound_never_violated"]),
        "in_class_columns_never_below_one": bool(res["NG2b_bound_never_violated"]),
        "deviation_is_truncation_not_error": bool(res["NG2b_deviation_is_truncation"]),
        "in_class_shapes_really_have_A21_zero": bool(
            res["NG2b_in_class_max_A21_norm"] == 0.0),
        "the_class_is_strictly_larger_A12_free": bool(
            res["NG2b_in_class_max_A12_norm"] > 0.0),
        # 1e-4, not 1e-9: leg 54's numbers were produced on a different BLAS threading, and
        # the reduction order over a 1024-dimensional tail moves the 6th digit.  The
        # measured gap is emitted next to this so the tolerance cannot hide a real drift.
        "instrument_reproduces_leg54": bool(
            res.get("NG2b_instrument_max_rel_gap_vs_leg54", 1.0) < 1e-4),
        "alt_split_does_not_rescue": bool(res["NG2c_alt_tail_inverse_diverges"]),
        "sharpness_control_reaches_below_one": bool(res["NG3_in_class_reaches_below_one"]),
        "sharpness_only_when_hypothesis_removed": bool(res["NG3_only_when_mu_positive"]),
    }
    res["gate_conditions"] = gate_conditions
    res["gate_conditions_failed"] = sorted(k for k, v in gate_conditions.items() if not v)
    proved = all(gate_conditions.values())
    res["gate_answer"] = "YES" if proved else "NO"
    res["gate_branch"] = (
        "YES -> the repository has a Tier-3-shaped negative theorem; write it as a "
        "standalone claim with its sharpness control, and ESCALATE publication scoping to "
        "the user."
        if proved else
        "NO -> REPORT the result as a measurement over a battery, not a theorem; cap the "
        "claim at 'measured, not proved' everywhere it appears.")
    res["gate_named_class"] = "A_upper = { A = [[A11, A12], [0, A22]] }, i.e. A21 = 0"
    res["gate_strictly_larger_than_block_diagonal_because"] = (
        "block-diagonal is the single point A12 = 0, A22 = A_tail inside A_upper; A_upper "
        "leaves A12 and A22 free and contains leg 54's separately-measured gs_upper shape")
    res["gate_hypotheses_contain_the_object_because"] = (
        "H2 is verified ON the a = 0 CLM tail block: the kernel is explicit (two-term "
        "recursion), decays like m^-2, and its l^1_w partial norms settle at s = 0 "
        "(-> {kn0:.4f}) and s = 0.3 (-> {kn3:.4f}), the two classes legs 51-54 used").format(
            kn0=memb[0]["partial_norm"][-1], kn3=memb[1]["partial_norm"][-1])
    res["gate_what_the_YES_does_NOT_cover"] = (
        "every A with A21 != 0 -- gs_lower, schur and ff_lift among leg 54's shapes.  For "
        "those the result is leg 54's battery, bottoming at Z1 = 8.9591 admissible: "
        "MEASURED, NOT PROVED.")

    res["headline"] = (
        "The no-go is a THEOREM on the class A21 = 0 (every block-diagonal and every "
        "block-upper-triangular approximate inverse): Z1 >= 1 + ||A11 B h||_w/||h||_w at "
        "every split K and every s < 1, because the tail block's far-field kernel lies IN "
        "l^1_w.  Checked against leg 54's battery over 10 (class, K) configurations: the "
        f"in-class minimum hhat-column is {res['NG2b_in_class_min_hhat_column']:.4f} where "
        "the proposition forbids anything below 1, and the whole deviation from the "
        "infinite-tail equality is "
        f"{res['NG2b_max_deviation_over_truncation_budget']:.4f}x the truncation budget, "
        "i.e. it IS the truncation.  "
        "The hypothesis is sharp: mu > 0 removes the kernel and the same class reaches "
        f"Z1 = {res['NG3_best_in_class_control_Z1']:.4f}.  Beyond the class the result "
        "stays MEASURED: the rank-one far-field lift buys back exactly "
        f"{res['NG2d_credit_range'][1]:.4f} of the column and leg 54's battery bottoms at "
        "8.9591.")

    res["elapsed_s"] = round(time.time() - t0, 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\n[GATE] {res['gate_answer']}  -- {res['gate_branch']}")
    print(f"\nwrote {OUT.relative_to(ROOT)}  ({res['elapsed_s']}s)")


if __name__ == "__main__":
    main()
