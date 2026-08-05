"""Route-T v1: border the tail with the far field the transport operator cannot invert.

Leg 51 answered `L1`'s gate NO and named the term: the tail operator has zero diagonal and
is not injective, so no weight class holds it.  It also identified the obstruction precisely
enough to attack -- one explicit mode, the |X|^-1 far field.  An operator that fails to be
invertible by a FINITE-DIMENSIONAL kernel is the classic case for BORDERING, which is the
same move that made Route-PORT's finite block work.  This leg measures the repair before
anything is built on it.

PRE-COMMITTED CLAUSES, written before the run (both branches of each are reportable):

  T0  THE NOVELTY PASS COMES FIRST, and it can only narrow the claim, never widen it.  Leg
      51's methodological claim -- an ell^1-Fourier tail estimate needs the unbounded part
      of the operator to be a MULTIPLIER -- is searched against the validated-numerics
      literature, not against memory.  If the observation is known, it is recorded as
      known and the claim drops to a re-derivation.  The ledger and the query log are both
      committed, because leg 42's failure mode was an unrecorded search.
  T1  THE GATE.  Does bordering the tail with ONE row and ONE column give a weighted
      inverse norm that stays BOUNDED as M grows, in a class where the target profile also
      has finite norm (s < alpha = 0.394)?  Report the ladder, not its endpoint (72).
  T2  THE BORDER A CERTIFICATE CAN ACTUALLY WRITE DOWN IS THE ANALYTIC ONE.  The SVD pair
      is the most favourable 1-dimensional bordering that exists; the explicit far-field
      mode is what a proof would use.  Both are run.  If the analytic border is much worse
      than the SVD one, the repair is not usable and that is the finding.
  T3  TWO NEGATIVE CONTROLS, because "bordering fixes it" is only a measurement if
      bordering can also fail: the SECOND singular pair (the wrong direction) and a RANDOM
      pair must both keep diverging.
  T4  THE ALIGNMENT IS THE PHYSICS.  |cos| between the optimal border direction and the
      analytic far-field mode is reported at every rung.  Near 1 means the repair is
      "add the far field as an unknown"; well below 1 would mean the SVD is fixing
      something else and the story is wrong.
  T5  WHICH SIDE OF s = 1 THE OBSTRUCTION IS ON, measured: the kernel decays like m^-2
      (in the space iff s < 1) and the cokernel functional grows like m (bounded iff
      s >= 1).  This predicts, in advance, that bordering helps BELOW s = 1 and not at it
      -- and s = 1 is exactly where leg 51's unbordered curve had its minimum.
  T6  THE CEILING, pre-committed before the numbers exist.  A bounded bordered TAIL is not
      a certificate.  The border is a new unknown; it needs its own Y_0, its own column in
      the finite block, and a matching condition that has not been written here.  Nothing
      is claimed about HL_S2_nonsymmetric.

Writes writeup/data/p2_route_t_v1_border.json.

Run: .venv/bin/python -u experiments/p2_route_t_v1_border.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import (                              # noqa: E402
    bordered_tail_inverse_norm, fredholm_sides, tail_inverse_norm, tail_singular_pair,
)

OUT = ROOT / "writeup" / "data" / "p2_route_t_v1_border.json"

K_TAIL = 64
M_LADDER = (320, 576, 1088, 2112, 3136)
ALPHA_TARGET = 0.394
CLASSES = (("flat", 0.0), ("algebraic", 0.3), ("algebraic", 0.394),
           ("algebraic", 1.0), ("algebraic", 1.5))

# --------------------------------------------------------------------------
# T0 -- the novelty ledger.  Searched 2026-08-05 with WebSearch/WebFetch, in session.
# --------------------------------------------------------------------------
PRECEDENTS = [
    {"id": "arXiv:1503.06315",
     "who": "Breden, Desvillettes, Lessard (2015)",
     "what": ("'Rigorous numerics for nonlinear operators with TRIDIAGONAL DOMINANT linear "
              "part'. States the problem this leg ran into in almost these words -- the "
              "derivative 'does not have an asymptotically diagonal dominant structure', so "
              "the approximate inverse is not straightforward -- and supplies a "
              "construction for A in that setting."),
     "verdict": "ADJACENT_AND_NARROWS_THE_CLAIM",
     "why": ("The general observation is NOT new: the field knows the standard tail "
             "estimate assumes an eventually-diagonal operator, and has already extended it "
             "to tridiagonal DOMINANT ones. Our tail is tridiagonal and NOT dominant -- its "
             "diagonal is exactly zero and it is Fredholm with a kernel. Whether their "
             "construction covers that case was NOT resolved in this pass (the PDF did not "
             "extract); it is recorded as the open question it is.")},
    {"id": "standard ell^1_nu framework",
     "who": "the radii-polynomial literature (Lessard, Mireles James, van den Berg, ...)",
     "what": ("The spectrum of an EVENTUALLY DIAGONAL operator on ell^1_nu is read off the "
              "tail's diagonal entries; tail estimates are built on exactly that."),
     "verdict": "CONFIRMS_THE_ASSUMPTION_IS_STANDARD",
     "why": ("So 'the method assumes a multiplier' is a correct reading of the framework "
             "and not a discovery. What leg 51 measured that this does not cover is the "
             "specific structure of inviscid self-similar transport: zero diagonal, and a "
             "kernel that IS the far field.")},
    {"id": "arXiv:2210.07191 + arXiv:2305.05660",
     "who": "Chen, Hou",
     "what": ("Certified INVISCID self-similar blowup (2D Boussinesq / 3D Euler with "
              "boundary) using weighted L^inf and C^{1/2} norms and WEIGHTED ENERGY "
              "ESTIMATES -- not a radii polynomial in a sequence space."),
     "verdict": "CONFIRMS_LEG_51_PREDICTION",
     "why": ("Leg 51 predicted the shape of the field: certified self-similar blowups using "
             "ell^1-Fourier machinery are dissipative (Dahne-Figueras, CGL), while the "
             "certified inviscid ones use weighted energy instead. The prediction survives "
             "this pass. It is a consistency check, not evidence for our claim.")},
]

SEARCH_LOG = [
    ("radii polynomial validated numerics self-similar blowup transport equation tail "
     "estimate unbounded operator shift", 8),
    ("computer-assisted proof self-similar blowup weighted energy versus radii polynomial "
     "inviscid Euler Boussinesq", 10),
    ("radii polynomial OR Fourier-Taylor validated numerics ell^1 nu weights tail estimate "
     "requires dominant diagonal unbounded domain algebraic decay", 8),
    ("validated numerics rigorous computer-assisted 'not diagonally dominant' tail estimate "
     "sequence space transport operator shift no diagonal fails", 10),
    ("Chen Huang Li 2026 Hou-Luo model non-symmetric self-similar profile blowup proof", 5),
]

# The last query is recorded because of what it did NOT return: the April 2026 CHL
# reference this project's target rests on (arXiv:2604.01868) did not surface, only the
# 2021-2023 Hou-Luo work. That is a search-index observation and NOT evidence about the
# paper; the repo's seventh-pass record stands. Flagged so a later leg re-checks it.
TARGET_REFERENCE_NOT_RESURFACED = True


def novelty_verdict():
    """PROCEED_NARROW when the claim survives only in a narrowed form."""
    if any(p["verdict"].startswith("PRE_EMPTS") for p in PRECEDENTS):
        return "STOP_PRE_EMPTED"
    return "PROCEED_NARROW"


# --------------------------------------------------------------------------
def saturation(ms, vals):
    """The SHAPE of the ladder: successive increments and a fitted exponent.

    A bounded sequence has increments falling to zero; a divergent one does not. Both are
    reported, because a fitted exponent alone cannot tell a slow saturation from a slow
    divergence."""
    ms, vals = np.asarray(ms, float), np.asarray(vals, float)
    inc = np.diff(vals)
    return {"increments": [float(x) for x in inc],
            "increment_ratio": float(inc[-1] / inc[0]) if inc[0] != 0 else None,
            "exponent": float(np.polyfit(np.log(ms), np.log(vals), 1)[0]),
            "last": float(vals[-1]),
            "saturating": bool(inc[-1] < 0.5 * inc[0] and inc[-1] < 0.5)}


def main():
    t0 = time.time()
    res = {"leg": 52, "route": "T", "version": "v1", "K_tail": K_TAIL,
           "target_alpha": ALPHA_TARGET}

    # -- T0 the novelty pass ------------------------------------------------
    res["T0_novelty"] = {"precedents": PRECEDENTS, "search_log": SEARCH_LOG,
                         "verdict": novelty_verdict(),
                         "target_reference_not_resurfaced": TARGET_REFERENCE_NOT_RESURFACED}
    print(f"[T0] novelty: {res['T0_novelty']['verdict']} off {len(SEARCH_LOG)} queries; "
          f"{len(PRECEDENTS)} ledger entries")
    for p in PRECEDENTS:
        print(f"     {p['id']:35s} {p['verdict']}")

    # -- T5 which side of s = 1 (stated before the ladders, because it predicts them) --
    res["T5_fredholm"] = fredholm_sides(K_TAIL, 3136)
    print(f"[T5] kernel ~ m^{res['T5_fredholm']['kernel_exponent']:.3f} (in the space iff "
          f"s < 1); cokernel ~ m^{res['T5_fredholm']['cokernel_exponent']:+.3f} (bounded "
          f"iff s >= 1) -- the two failure modes swap at s = 1")

    # -- T1/T2/T3/T4 the ladders -------------------------------------------
    ladders = []
    for kind, p in CLASSES:
        row = {"class": kind, "param": float(p), "M": list(M_LADDER)}
        for lab in ("analytic", "svd", "second", "random"):
            row[lab] = [bordered_tail_inverse_norm(K_TAIL, M, kind, p, border=lab)
                        for M in M_LADDER]
            row[lab + "_shape"] = saturation(M_LADDER, row[lab])
        row["unbordered"] = [tail_inverse_norm(K_TAIL, M, kind, p) for M in M_LADDER]
        row["unbordered_shape"] = saturation(M_LADDER, row["unbordered"])
        sp = [tail_singular_pair(K_TAIL, M, kind, p) for M in M_LADDER]
        row["sigma_min"] = [s[0] for s in sp]
        row["sigma_2"] = [s[1] for s in sp]
        row["alignment"] = [s[2] for s in sp]
        row["object_has_finite_norm"] = bool(p < ALPHA_TARGET or kind == "flat")
        ladders.append(row)
        print(f"[T1] {kind} {p:.3g}: unbordered {row['unbordered'][0]:.2f} -> "
              f"{row['unbordered'][-1]:.2f}  |  bordered(analytic) {row['analytic'][0]:.2f} "
              f"-> {row['analytic'][-1]:.2f} "
              f"({'SATURATES' if row['analytic_shape']['saturating'] else 'still growing'})"
              f"  | align {row['alignment'][-1]:.4f}")
    res["T1_ladders"] = ladders

    admissible = [r for r in ladders if r["object_has_finite_norm"]]
    gate = all(r["analytic_shape"]["saturating"] for r in admissible)
    controls = all(not r["second_shape"]["saturating"] and not r["random_shape"]["saturating"]
                   for r in ladders)
    res["T2_analytic_vs_svd"] = [
        {"class": r["class"], "param": r["param"],
         "ratio_last": r["analytic"][-1] / r["svd"][-1]} for r in ladders]
    print(f"[T2] analytic/SVD at the top rung: "
          f"{[round(x['ratio_last'], 3) for x in res['T2_analytic_vs_svd']]}")
    res["T3_controls_diverge"] = bool(controls)
    print(f"[T3] negative controls diverge: {controls}")
    res["T4_alignment_top"] = {f"{r['class']}_{r['param']}": r["alignment"][-1]
                               for r in ladders}

    res["T6_ceiling"] = (
        "A bounded bordered TAIL is not a certificate. What is measured here is the "
        "weighted l^1 operator norm of the inverse of the tail block plus one border row "
        "and one border column, as the number of retained modes grows. In a certificate "
        "the border is a NEW UNKNOWN -- the far-field amplitude -- which needs its own "
        "column in the finite block, its own contribution to Y_0, and a matching condition "
        "between the spectral tail and the asymptotic expansion. None of that is written "
        "here. The object is still the a = 0 CLM linearisation, and nothing is claimed "
        "about HL_S2_nonsymmetric.")

    res["gate_admissible_classes_saturate"] = bool(gate)
    res["verdict"] = ("BORDERING_RESTORES_A_BOUNDED_TAIL_IN_THE_ADMISSIBLE_CLASSES"
                      if gate and controls else
                      "BORDERING_DOES_NOT_RESTORE_A_BOUNDED_TAIL")
    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)  VERDICT: {res['verdict']}")


if __name__ == "__main__":
    main()
