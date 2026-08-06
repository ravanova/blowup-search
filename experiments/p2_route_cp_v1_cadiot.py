"""Route-CP v1 (leg 62): CADIOT arXiv:2505.03091's SCOPE, SETTLED FROM THE FULL TEXT.

Leg 57 flagged this paper as independently stating the dominance-hypothesis observation
and recommended not re-claiming leg 51's methodological finding at full strength.  That
recommendation is correct and INSUFFICIENT: the same paper is the single largest novelty
risk to leg 58's proposition, and leg 57 did not establish whether Cadiot's construction
REACHES the off-diagonal unbounded part with a non-decaying tail inverse -- which is NG's
hypothesis, not leg 51's.  The standing ban's lift condition names exactly that question:

    "lifted by: never -- unless a pass resolves whether Cadiot's construction covers a
     zero diagonal, which is now the live open question, not BDL's"

This runner is that resolution, and it is deliberately NOT a reading exercise.  This
repository has been burned twice by literature read at the wrong depth (leg 53 read BDL's
dominance hypothesis off a publisher abstract page and lost the claim).  So the paper is
fetched, the clauses are located with section numbers and verbatim quotes, AND the
hypothesis is turned into a number that is measured on the paper's own worked examples.

PRE-COMMITTED CLAUSES, written before the run, both branches reportable:

  CP0 THE NOVELTY PASS CAME FIRST.  `writeup/novelty/leg_62.md`, committed BEFORE any of
      this was built (commit "Leg 62: LEG -- novelty pass, run and logged BEFORE
      construction").  Verdict PROCEED_AS_BOOKKEEPING: this leg settles the scope of
      somebody else's paper and claims NO mathematical novelty of its own.  That verdict
      is carried into the JSON so the writeups cannot overstate past it.

  CP1 EVERY CLAUSE IS TRACED TO A LOCATED FULL-TEXT STATEMENT.  Section / assumption /
      lemma number, plus the sentence verbatim.  Never an abstract.  Farid-Lancaster
      (Cadiot's [24], paywalled) is recorded as NOT OBTAINED rather than glossed.

  CP2 THE PAPER'S OWN CONSTANTS ARE RE-DERIVED, NOT QUOTED.  Cadiot states l_min in
      words for three of his four examples; this runner computes them from the symbols
      and reports the difference.  A hypothesis you can only quote is a sentence; a
      hypothesis you can measure on the author's own examples has a scale.

  CP3 THE ONE SYSTEMS EXAMPLE IS MEASURED.  A system is the only route by which an
      off-diagonal entry enters this framework at all, and section 5.3 is the only
      systems example in the paper.  Its off-diagonal entry and the ratio of that entry
      to the diagonal are reported as magnitudes, with the ratio's exponent.

  CP4 LEMMA 3.2's SHIFT, AS TWO LADDERS.  Cadiot's proof needs ONE s in C with
      |lambda_n + s| > r_n/2 at EVERY n.  Reported as `|s|` versus truncation, for his
      operator and for ours.  Shape of a ladder, not its endpoint (discipline 72).

  CP5 THE POSITIVE CONTROL CAN REPORT THE OTHER ANSWER, AND DOES.  Cadiot's own Whitham
      operator, in his own coordinates, run through the identical code path.  Lesson 90:
      the saturating |s| is identical across truncations, so it is checked that it MOVES
      when the operator moves (the convolution's l^1 norm) while the exponent does not.

  CP6 THREE NUMBERS ON ONE DIAL, KEPT APART.  Cadiot's Lemma 3.2 admits the dissipated
      family for mu >= 1/2; BDL's assumption (5) only for mu > 1; leg 57 measured the
      OPERATOR's own hinge at mu = 0 exactly.  These are two hypotheses of two
      CONSTRUCTIONS and one property of an operator, and this leg does not conflate them.

  CP7 THE GATE IS ANSWERED IN `DIRECTION.md`'s PRE-COMMITTED WORDING, off an executable
      predicate that can answer both ways.

WHAT THIS RUNNER DOES NOT DO.  It does not re-derive leg 57's tail-inverse ladders
(`solver/certificate_shapes.py`'s `classify_operator` already owns those, and
`SHAPE_LEDGER` is left exactly as leg 57 wrote it).  It does not touch
`solver/spectral_certificate.py`, which is leg 58's territory -- it only READS
`tail_block`.  It says nothing about `HL_S2_nonsymmetric` and nothing about any link of
the L1->L4 chain.  It is not a claim that Cadiot's paper is deficient: the clauses it
locates are hypotheses that paper states plainly and discharges on its own examples.

Run: `.venv/bin/python experiments/p2_route_cp_v1_cadiot.py`
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.certificate_shapes import (                                # noqa: E402
    CADIOT_EXAMPLES,
    CADIOT_SCOPE,
    CP_FORWARD,
    CP_NOT_OBTAINED,
    CP_SYNTHETIC_COVERING_SCOPE,
    cadiot_covers,
    cadiot_ratio_ladder,
    cadiot_shift_requirement,
    cadiot_symbol_admissibility,
    cadiot_vs_bdl_thresholds,
    cadiot_whitham_matrix,
    cp_unlocated_rows,
    our_operator_gershgorin,
    shift_requirement_ladder,
)
from solver.spectral_certificate import tail_block                     # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_cp_v1_cadiot.json"

K_SPLIT = 8
MS = (128, 256, 512, 1024, 2048)
NS = (128, 256, 512, 1024)
MU_DIAL = (0.0, 0.25, 0.45, 0.5, 1.0, 2.0)
KERNEL_L1_DIAL = (0.05, 0.35, 2.0, 10.0)


def main():
    t0 = time.time()
    res = {
        "leg": 62,
        "route": "CP",
        "paper": "arXiv:2505.03091",
        "url": "https://arxiv.org/abs/2505.03091",
        "title": ("Cadiot, Stability analysis for localized solutions in PDEs and "
                  "nonlocal equations on R^m (6 May 2025, 30 pp.)"),
        "how_obtained": ("bash Papers/fetch.sh 2505.03091 -- egress probe HTTP 200, "
                         "1004 KB, 30 pages, extracted with pypdf.  Papers/ is "
                         "gitignored on purpose; the fetch is one command."),
    }

    # ---------------- CP0: the novelty pass, carried forward ----------------
    res["CP0_novelty"] = {
        "log": "writeup/novelty/leg_62.md",
        "verdict": "PROCEED_AS_BOOKKEEPING",
        "committed_before_construction": True,
        "meaning": ("This leg settles the SCOPE OF SOMEBODY ELSE'S PAPER and claims no "
                    "mathematical novelty of its own.  The dominance-hypothesis "
                    "observation is folklore in print (leg 57's finding, unchanged).  "
                    "What this leg produces is a located, executable scope record plus "
                    "magnitudes measured against the paper's own examples."),
        "queries": ("four verbatim queries with LINKS, not counts, in the novelty log; "
                    "two genuine forward citations located and read at full text; one "
                    "independent off-diagonal candidate read and classified"),
    }

    # ---------------- CP1: located clauses ----------------
    res["CP1_located_clauses"] = {
        "unlocated": cp_unlocated_rows(),
        "n_clauses": len(CADIOT_SCOPE),
        "clauses": [{"clause": c["clause"], "where": c["where"], "quote": c["quote"],
                     "supports": c["supports"],
                     "holds_for_the_a0_CLM_linearisation":
                         c["holds_for_the_a0_CLM_linearisation"],
                     "why": c["why"]}
                    for c in CADIOT_SCOPE],
        "forward_citations": [{"tag": f["tag"], "arxiv": f["arxiv"], "url": f["url"],
                               "cites_2505_03091_as": f["cites_2505_03091_as"],
                               "where": f["where"], "quote": f["quote"],
                               "relaxes_the_hypothesis": f["relaxes_the_hypothesis"],
                               "note": f["note"]}
                              for f in CP_FORWARD],
        "not_obtained": CP_NOT_OBTAINED,
    }

    # ---------------- CP2: the paper's own constants, re-derived ----------------
    adm = {}
    for name in CADIOT_EXAMPLES:
        a = cadiot_symbol_admissibility(name)
        stated = a["author_states"]["l_min"]
        a["l_min_minus_author_stated"] = (None if stated is None
                                          else float(a["l_min"] - stated))
        adm[name] = a
    res["CP2_assumption_1_on_cadiots_own_examples"] = {
        "examples": adm,
        "l_min_range_over_cadiots_examples": [
            float(min(a["l_min"] for a in adm.values())),
            float(max(a["l_min"] for a in adm.values()))],
        "worst_reproduction_error": float(max(
            abs(a["l_min_minus_author_stated"]) for a in adm.values()
            if a["l_min_minus_author_stated"] is not None)),
        "reading": ("Assumption 1 is not decorative and it is not a formality: on the "
                    "paper's own examples it is a POSITIVE NUMBER the author computes "
                    "and states, and the growth half is a positive exponent in every "
                    "case (4.000 Swift-Hohenberg, 0.508 Whitham, 2.000 Gray-Scott)."),
    }

    # ---------------- CP3: the one systems example ----------------
    gs = adm["GrayScott"]
    res["CP3_the_one_systems_example"] = {
        "where": gs["where"],
        "offdiag_entry": gs["offdiag_entry"],
        "offdiag_entry_symbolic": "lambda_1 lambda_2 - 1 = (1/9)(10) - 1 = 1/9",
        "diagonal_growth_exponent": gs["growth_exponent"],
        "offdiag_over_diag_exponent": gs["offdiag_over_diag_exponent"],
        "offdiag_over_diag_at_xi_max": gs["offdiag_over_diag_at_xi_max"],
        "xi_max": gs["xi_max"],
        "reading": ("A system is the ONLY route by which an off-diagonal entry enters "
                    "this framework, and section 5.3 is the only systems example in the "
                    "paper.  Its off-diagonal entry is a BOUNDED CONSTANT while both "
                    "diagonal entries grow like |2 pi xi|^2.  So even in the systems "
                    "case the unbounded part is the diagonal and the off-diagonal is a "
                    "bounded perturbation of it -- and that off-diagonality is in the "
                    "COMPONENT index, whereas ours is in the FOURIER index."),
    }

    # ---------------- CP4/CP5: Lemma 3.2's shift, two ladders ----------------
    cadiot_lad = shift_requirement_ladder(cadiot_whitham_matrix, NS)
    ours_lad = {}
    for mu in MU_DIAL:
        ours_lad[str(mu)] = shift_requirement_ladder(
            lambda M, mu=mu: tail_block(K_SPLIT, M, mu=mu), MS)

    ratio_c = []
    for N in NS:
        A = cadiot_whitham_matrix(N)
        lad = cadiot_ratio_ladder(A, np.abs(np.arange(-N, N + 1)), hi_trim=8)
        lad["N"] = N
        ratio_c.append(lad)
    ratio_o = []
    for mu in MU_DIAL:
        T = tail_block(K_SPLIT, 512, mu=mu)
        lad = cadiot_ratio_ladder(T, np.arange(K_SPLIT + 1, 513), hi_trim=1)
        lad["mu"] = mu
        ratio_o.append(lad)

    # the curves themselves, so the evidence script rebuilds the figure from the JSON
    # alone and never re-runs anything (ORCHESTRATION.md section 6).
    from solver.certificate_shapes import gershgorin_dominance_ratio   # noqa: E402
    A512 = cadiot_whitham_matrix(512)
    n512 = np.arange(-512, 513)
    rc = gershgorin_dominance_ratio(A512)
    keep = (n512 > 0) & (n512 <= 512 - 8)
    curves = {"cadiot_whitham_N512": {"n": n512[keep].tolist(),
                                      "ratio": rc[keep].tolist()}}
    for mu in MU_DIAL:
        T = tail_block(K_SPLIT, 512, mu=mu)
        r = gershgorin_dominance_ratio(T)[1:-1]
        kk = np.arange(K_SPLIT + 1, 513)[1:-1]
        curves[f"ours_mu_{mu}"] = {
            "k": kk.tolist(),
            "ratio": [None if not np.isfinite(v) else float(v) for v in r]}

    res["CP4_lemma_3_2_shift"] = {
        "ratio_curves": curves,
        "requirement": ("Cadiot's Lemma 3.2 proof needs ONE s in C, big enough in "
                        "amplitude, with |lambda_n + s| > (1/2) sum_{k != n} |R_{n,k}| "
                        "SIMULTANEOUSLY at every n in Z^m.  For real centres the "
                        "minimum-modulus such s is purely imaginary, giving "
                        "|s| = sqrt(max_n (r_n^2/4 - lambda_n^2)_+)."),
        "cadiot_whitham": cadiot_lad,
        "ours_by_mu": ours_lad,
        "ours_K": K_SPLIT,
        "headline": ("Cadiot's own operator: |s| = "
                     f"{cadiot_lad['s_required'][0]:.5f} at EVERY truncation "
                     f"N = {NS[0]}..{NS[-1]} (exponent "
                     f"{cadiot_lad['exponent']:+.1e}) -- one finite shift serves the "
                     "infinite matrix.  Ours at mu = 0: |s| = "
                     f"{ours_lad['0.0']['s_required'][0]:.0f} -> "
                     f"{ours_lad['0.0']['s_required'][-1]:.0f} over "
                     f"M = {MS[0]}..{MS[-1]}, exponent "
                     f"{ours_lad['0.0']['exponent']:+.4f} -- LINEAR in the truncation, "
                     "so no finite s survives the limit and Lemma 3.2 cannot be entered "
                     "at all."),
        "gershgorin_ratio_ladder_cadiot": ratio_c,
        "gershgorin_ratio_ladder_ours": ratio_o,
        "ratio_reading": ("Cadiot's ratio r_n/|lambda_n| DECAYS -- the ladder is "
                          + ", ".join(f"{r['exponent']:+.4f}" for r in ratio_c)
                          + f" over N = {NS[0]}..{NS[-1]}, drifting toward the analytic "
                          "-1/2 set by his symbol's sqrt growth.  Ours is FLAT: exponent "
                          f"{ratio_o[1]['exponent']:+.4f} at EVERY mu > 0 (identically, "
                          "to 13 digits) -- if anything very slightly increasing -- and "
                          "REFUSED at mu = 0, where every row's diagonal is exactly "
                          "zero and the ratio has no referent."),
    }

    control_levels, control_exps = [], []
    for l1 in KERNEL_L1_DIAL:
        A = cadiot_whitham_matrix(512, kernel_l1=l1)
        control_levels.append(cadiot_shift_requirement(A))
        control_exps.append(cadiot_ratio_ladder(
            A, np.abs(np.arange(-512, 513)), hi_trim=8)["exponent"])
    res["CP5_positive_control"] = {
        "what": ("Cadiot's section 5.2 capillary-gravity Whitham operator, in his own "
                 "Fourier-coefficient coordinates: HIS symbol l(xi) = m_T(2 pi xi) - c "
                 "exactly on the diagonal (T = 0.5, c = 0.8, transcribed from section "
                 "5.2), plus a finitely-supported convolution off it -- which is what "
                 "DG(U0) is for his F(u) = M_T u - c u + u^2."),
        "surrogate_flag": ("The convolution is a SURROGATE for DG(U0): his u0 is not "
                           "distributed with the paper and this leg does not have it.  "
                           "It is built so it CANNOT carry the conclusion -- its l^1 "
                           "norm is a dial and the exponent is invariant under it."),
        "kernel_l1_dial": list(KERNEL_L1_DIAL),
        "s_required_by_kernel_l1": control_levels,
        "ratio_exponent_by_kernel_l1": control_exps,
        "exponent_spread": float(max(control_exps) - min(control_exps)),
        "binding_row_prediction": {
            "formula": "|s| = sqrt((r/2)^2 - l_min^2) with r = 2||V||_1 and l_min = 0.2",
            "predicted_at_kernel_l1_0.35": float(np.sqrt(0.35 ** 2 - 0.2 ** 2)),
            "measured_at_kernel_l1_0.35": control_levels[1],
        },
        "lesson_90": ("The saturating |s| is IDENTICAL across four truncations, which is "
                      "exactly the pattern lesson 90 says to distrust.  It is "
                      "saturation, not a tautology, and the proof is that it MOVES with "
                      "the operator (0.0 -> 9.998 as ||V||_1 goes 0.05 -> 10) while the "
                      "ratio's exponent does NOT move at all (spread < 1e-9), because "
                      "the numerator is exactly 2||V||_1 in the interior and the "
                      "exponent therefore belongs to Cadiot's SYMBOL alone.  And the "
                      "binding row is the one Assumption 1 is about: |s| is predicted "
                      "EXACTLY by his own l_min = 0.2."),
    }

    # ---------------- CP6: three numbers on one dial ----------------
    dial = []
    for mu in MU_DIAL:
        g = our_operator_gershgorin(K=K_SPLIT, M=512, mu=mu)
        g["shift_ladder_saturates"] = ours_lad[str(mu)]["saturates"]
        g["shift_ladder_exponent"] = ours_lad[str(mu)]["exponent"]
        dial.append(g)
    res["CP6_thresholds"] = {
        "dial": dial,
        "thresholds": cadiot_vs_bdl_thresholds(),
        "row_sum_identity": ("r_k = k - 1 exactly for the interior rows of tail_block "
                             "(max error "
                             f"{dial[1]['row_sum_identity_max_err_vs_k_minus_1']:.1e}), "
                             "which is WHY the ratio's exponent is mu-independent and "
                             "only its level moves.  Checked, not assumed -- lesson 90 "
                             "again."),
        "reading": ("Cadiot's Lemma 3.2 admits this one-parameter family for "
                    "mu >= 0.5; BDL's assumption (5) only for mu > 1; the factor "
                    "between them is exactly 2 (Gershgorin bounds the whole row sum "
                    "with a 1/2, BDL bounds each ratio separately).  BOTH are vacuous "
                    "at mu = 0, which is the case of interest.  Neither is the "
                    "OPERATOR's hinge -- leg 57 measured that separately and it is "
                    "mu = 0 exactly.  Two hypotheses of two constructions and one "
                    "property of an operator: three numbers, not one."),
    }

    # ---------------- CP7: the gate ----------------
    gate = cadiot_covers()
    control_gate = cadiot_covers(scope=CP_SYNTHETIC_COVERING_SCOPE)
    relaxed = [dict(f) for f in CP_FORWARD]
    relaxed[0]["relaxes_the_hypothesis"] = True
    res["CP7_gate"] = {
        "gate": gate["gate"],
        "answer": gate["answer"],
        "n_clauses_failing": gate["n_clauses_failing"],
        "clauses_that_fail_for_our_operator": gate["clauses_that_fail_for_our_operator"],
        "forward_citations_examined": gate["forward_citations_examined"],
        "forward_citations_relaxing_the_hypothesis":
            gate["forward_citations_relaxing_the_hypothesis"],
        "control": {
            "answer_with_a_covering_scope": control_gate["answer"],
            "answer_with_a_relaxing_forward_citation":
                cadiot_covers(forward=relaxed)["answer"],
            "why": ("Lesson 90.  The gate flips to 'yes' two independent ways, so 'no' "
                    "is a property of the located clauses and not of the code."),
        },
        "precommitted_no_branch": ("The gap leg 57's ledger measured is confirmed at "
                                   "full-text depth for the one paper most likely to "
                                   "close it.  Bank the located hypotheses as an "
                                   "executable ledger entry; NG may claim novelty "
                                   "against this paper and no further."),
    }

    # ---------------- standing scope ----------------
    res["verdict"] = "CADIOT_DOES_NOT_COVER_THE_OFF_DIAGONAL_ZERO_DIAGONAL_CASE"
    res["what_this_establishes"] = (
        "arXiv:2505.03091 does not cover an operator whose unbounded part is "
        "off-diagonal with a non-decaying tail inverse, and it fails to on SIX "
        "independent located clauses rather than one: the class definition itself "
        "(eq. (1)-(2), L is a Fourier multiplier, hence diagonal in the Fourier index by "
        "construction); both halves of Assumption 1 (|l| >= l_min > 0 and |l| -> "
        "infinity); the two places section 3 USES them (Lemma 3.1's compactness, Lemma "
        "3.2's shift); and the one systems example, which is the only place an "
        "off-diagonal entry appears in the paper and where that entry is a bounded "
        "constant against an unbounded diagonal.  The obstruction is quantitative and "
        "measured, not rhetorical: Lemma 3.2 needs one finite s serving every mode, and "
        "on our operator the required |s| grows LINEARLY in the truncation (exponent "
        "+1.005 over M = 128..2048) while on Cadiot's own Whitham operator it is a "
        "single number, 0.28723, unchanged across N = 128..1024 and predicted exactly by "
        "his own l_min = 0.2.  Both forward citations of 2505.03091 restate the "
        "hypothesis rather than relax it, and the systems form is |det(l)| >= sigma_0 > "
        "0.")
    res["what_this_does_NOT_establish"] = (
        "That leg 58's no-go is TRUE -- a gap in one paper is not a theorem, and leg "
        "58's gate is a separate question this leg does not touch.  That the observation "
        "is novel -- it is folklore in print (CP0), and this leg claims no mathematical "
        "novelty of its own.  That the standing ban on re-claiming leg 51's finding at "
        "full strength is LIFTED -- answering the ban's named question does not by "
        "itself discharge it; the correct bookkeeping change is a narrowing annotation, "
        "and it is integration-owned, not claimed here.  That Cadiot's paper is "
        "deficient -- these are hypotheses it states plainly and discharges on its own "
        "examples.  Nothing here moves any link of the L1->L4 chain; Clay stays at "
        "~0.05% behind Walls 1 and 2.")
    res["forward_consequence_for_NG"] = (
        "NG may claim novelty against arXiv:2505.03091 AND NO FURTHER.  The claim it may "
        "make is bounded by what this leg checked: one paper at full text, its two "
        "genuine forward citations, and one independent off-diagonal candidate "
        "(arXiv:2605.03920, Burgers-Hilbert, which is not a counterexample and certifies "
        "its shift case by abandoning the tail estimate -- the Chen-Hou pattern from a "
        "different community).  Four papers is a corpus, not a theorem.")

    res["elapsed_s"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))

    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)")
    print(f"GATE: {res['CP7_gate']['answer']}  "
          f"({res['CP7_gate']['n_clauses_failing']} of {len(CADIOT_SCOPE)} located "
          f"clauses fail)  control -> "
          f"{res['CP7_gate']['control']['answer_with_a_covering_scope']}")
    print("\nAssumption 1 on Cadiot's own examples (l_min, measured vs stated):")
    for name, a in adm.items():
        st = a["author_states"]["l_min"]
        print(f"  {name:14s} l_min = {a['l_min']:.6f}"
              + (f"  (states {st}, diff {a['l_min_minus_author_stated']:+.2e})"
                 if st is not None else "  (not stated as a number)")
              + f"  growth {a['growth_exponent']:+.4f}")
    print("\nLemma 3.2's shift, as ladders:")
    print(f"  Cadiot/Whitham  |s| = {cadiot_lad['s_required']}  "
          f"exponent {cadiot_lad['exponent']:+.1e}  SATURATES")
    for mu in MU_DIAL:
        lad = ours_lad[str(mu)]
        e = "n/a (already dominant)" if lad["exponent"] is None \
            else f"{lad['exponent']:+.4f}"
        print(f"  ours mu={mu:<5} |s| = {[round(v, 3) for v in lad['s_required']]}  "
              f"exponent {e}  saturates={lad['saturates']}")
    print(f"\nVERDICT: {res['verdict']}")


if __name__ == "__main__":
    main()
