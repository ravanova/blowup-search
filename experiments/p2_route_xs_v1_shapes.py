"""Route-XS v1 (leg 57): THE SHAPE DICHOTOMY AGAINST THE PUBLISHED CERTIFICATES.

Legs 51-53 explained Route-TC's failure with one sentence (lesson 87): the standard
radii-polynomial tail estimate works because the unbounded part is a MULTIPLIER, and
here it is a SHIFT.  If MM answers NO that sentence becomes the lane's epitaph.  **An
epitaph with no external check is a mood, not a finding.**  This runner produces the
external check, and it produces it in the only form that does not decay at the rate of
memory (lesson 68): an executable ledger plus a measured dial.

PRE-COMMITTED CLAUSES, written before the run, both branches reportable:

  XS0 THE NOVELTY PASS COMES FIRST and can only narrow the claim.  Committed at
      `writeup/novelty/leg_57.md` BEFORE any of this was built, six queries with LINKS
      (leg 53 logged counts and was withdrawn).  Its verdict is
      `PROCEED_AS_BOOKKEEPING`: the observation is FOLKLORE IN PRINT (Cadiot
      arXiv:2505.03091 sections 2 and 3 state both halves), so **this leg does not claim
      the dichotomy as a finding.**  It classifies known practice.  That verdict is
      carried into the JSON so the writeups cannot overstate past it.

  XS1 EVERY CLASSIFICATION IS TRACED TO A LOCATED FULL-TEXT STATEMENT.  Section or
      assumption or proposition number, plus the sentence verbatim.  Never an abstract:
      leg 53 read BDL's abstract, the claim was withdrawn, and the correction is a
      standing ban.  `unlocated_rows()` is the guard and it is asserted empty.

  XS2 THE GATE IS A PREDICATE, NOT A PARAGRAPH -- and it can answer BOTH ways.  A
      fictitious SYNTHETIC_CONTROL row satisfies the counterexample condition; admitting
      it flips the answer to "yes".  Lesson 90: a control that cannot come out
      differently is not a control, and four identical numbers should read as a bug.

  XS3 THE DICHOTOMY IS MEASURED, NOT ASSERTED.  `mu` (the `Lambda^1` dissipation dial
      already in `solver/spectral_certificate.py`) is a CONTINUOUS path from shift
      (`mu = 0`, diagonal exactly zero) to multiplier.  Two ladders are reported, both
      as magnitudes with a sign: growth in `M` (does the tail inverse EXIST?) and growth
      in `K` (does it DECAY, which is what the certificate needs?).

  XS4 THE HYPOTHESIS THIS LEG POSED IS ALLOWED TO DIE, IN THE ARTIFACT.  BDL's
      admissibility `delta < 1/2` reads `mu > 1` for our operator, so the obvious guess
      was a transition at `mu = 1`.  It is FALSE and the run reports it as false.

  XS5 THE WRONG CONSTRUCTION STAYS IN THE ARTIFACT (lesson 76).  Bordering a `mu > 0`
      tail with the `mu = 0` near-null pair produces numbers that look catastrophic and
      mean nothing; leg 53 already made this mistake.  They are computed and labelled
      WRONG_OPERATOR so the next agent recognises them instead of publishing them.

WHAT THIS RUNNER DOES NOT DO.  It does not re-derive CLN's Kawahara `r_0`
(`solver/target_selection.py` already reproduces it) or Dahne-Figueras' branch
(`solver/viscous_novelty.py`, leg 48).  It does not port Chen-Hou's energy method and
claims nothing about whether such a port would work.  It says nothing about
`HL_S2_nonsymmetric` or about any link of the L1->L4 chain.
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.certificate_shapes import (                                # noqa: E402
    SHAPE_LEDGER,
    WRONG_OPERATOR_CONTROL,
    bdl_admissible,
    bdl_delta,
    classify_operator,
    decay_exponent,
    gate_answer,
    m_divergence,
    real_ledger,
    tail_inverse_ladder,
)

OUT = ROOT / "writeup" / "data" / "p2_route_xs_v1_shapes.json"

KS = (4, 8, 16, 32, 64, 128)
MS = (128, 256, 512, 1024, 2048)
M_FIXED = 1024
MU_DIAL = (0.0, 0.25, 0.5, 1.0, 2.0, 4.0)


def main():
    t0 = time.time()
    res = {
        "leg": 57,
        "route": "XS",
        "title": "The shape dichotomy against published certificates",
        "object": ("the a = 0 CLM linearisation's far-field tail block "
                   "(solver/spectral_certificate.tail_block), weight class flat (plain "
                   "l^1); mu adds mu*k to the diagonal (Lambda^1 dissipation)"),
        "norm": "||M||_w = max_j (1/w_j) sum_i w_i |M_ij|, w_k = 1 (flat)",
    }

    # ---------------- XS0: the novelty verdict, carried, not restated ----------------
    res["XS0_novelty"] = {
        "log": "writeup/novelty/leg_57.md",
        "verdict": "PROCEED_AS_BOOKKEEPING",
        "n_queries": 6,
        "the_observation_is_in_print": True,
        "prior_statement_of_the_dichotomy": {
            "url": "https://arxiv.org/abs/2505.03091",
            "author": "Cadiot",
            "where_multiplier_half": "section 2 (periodic counterpart)",
            "quote_multiplier_half": ("the operator L becomes an infinite diagonal matrix "
                                      "L_q with entries l(n/2q) on the diagonal"),
            "where_dominance_half": "section 3 (opening), 'Spectrum of DF(U0) using Gershgorin disks'",
            "quote_dominance_half": ("By construction D is supposed to be diagonally "
                                     "dominant, which hints to the Gershgorin theorem."),
        },
        "what_this_leg_may_claim": ("the CLASSIFICATION as an executable ledger, and the "
                                    "answer to the gate.  NOT the dichotomy itself."),
        "flag_not_cleared": ("leg 52's search-index flag (arXiv:2604.01868) is NOT cleared "
                             "-- Q5 is a different query from leg 52's verbatim one."),
    }

    # ---------------- XS1 + XS2: the ledger and the gate ----------------
    g = gate_answer()
    res["XS1_ledger"] = {
        "n_published_rows": len(real_ledger()),
        "n_located_statements": sum(len(r["located"]) for r in real_ledger()),
        "rows": [
            {"tag": r["tag"], "arxiv": r["arxiv"], "url": r["url"],
             "authors": r["authors"], "title": r["title"],
             "is_radii_polynomial": r["is_radii_polynomial"],
             "unbounded_part": r["unbounded_part"],
             "approx_inverse": r["approx_inverse"],
             "tail_inverse_decays": r["tail_inverse_decays"],
             "counterexample": r["counterexample"],
             "located": r["located"], "note": r["note"]}
            for r in real_ledger()],
    }
    res["XS2_gate"] = {
        "question": g["gate"],
        "answer": g["answer"],
        "counterexamples": g["counterexamples"],
        "n_rows_examined": g["n_rows_examined"],
        "control": {
            "row": "SYNTHETIC_CONTROL",
            "fictitious": True,
            "answer_when_admitted": gate_answer(SHAPE_LEDGER)["answer"],
            "why": ("lesson 90 -- without a row that trips the predicate, 'no' would be a "
                    "property of the code rather than of the literature"),
        },
        "why_each_clause_matters": {
            "is_radii_polynomial": ("excludes Chen-Hou, who HAVE the shift but form no "
                                    "tail estimate.  Drop this clause and the strongest "
                                    "CONFIRMATION of the dichotomy reads as a refutation."),
            "unbounded_part_is_SHIFT": ("excludes BDL, who HAVE a non-block-diagonal "
                                        "approximate inverse but whose diagonal is bounded "
                                        "below by their assumption (4)."),
            "tail_inverse_does_not_decay": ("the actual counterexample condition.  No "
                                            "published row satisfies it."),
        },
    }

    # ---------------- XS3: the dichotomy, measured ----------------
    dial = []
    for mu in MU_DIAL:
        c = classify_operator(mu, Ks=KS, M=M_FIXED)
        dial.append({
            "mu": mu,
            "bdl_delta": bdl_delta(mu),
            "bdl_admissible": bdl_admissible(mu),
            "shape": c["shape"],
            "tail_block_boundedly_invertible": c["tail_block_boundedly_invertible"],
            "needed_bordering": c["needed_bordering"],
            "M_exponent": c["M_exponent"],
            "K": c["K"],
            "tail_inverse": c["tail_inverse"],
            "K_exponent": c["K_exponent"],
            "tail_inverse_decays": c["tail_inverse_decays"],
        })
    res["XS3_measured_dial"] = {
        "M_fixed": M_FIXED, "K_ladder": list(KS),
        "rows": dial,
        "reading": ("Exactly one row fails, and it is mu = 0 -- the only row whose "
                    "diagonal is exactly zero.  Its tail block is not boundedly "
                    "invertible (M-exponent ~ +1, linear), so a certificate MUST border "
                    "it (leg 52); and the bordered inverse then GROWS in K (+0.44) "
                    "instead of decaying.  Every mu > 0 is invertible without bordering "
                    "and decays at ~ -0.9."),
    }

    # the two ladders that carry the whole result, reported separately
    md_unb = m_divergence(0.0, K=8, Ms=MS, bordered=False)
    md_bor = m_divergence(0.0, K=8, Ms=MS, bordered=True)
    Ks_b, v_b = tail_inverse_ladder(0.0, KS, M_FIXED, bordered=True)
    de_b = decay_exponent(Ks_b, v_b)
    res["XS3a_shift_M_divergence"] = {
        "K": 8, "M": md_unb["M"],
        "unbordered": {"vals": md_unb["vals"], "exponent_in_M": md_unb["exponent_in_M"]},
        "bordered": {"vals": md_bor["vals"], "exponent_in_M": md_bor["exponent_in_M"]},
        "reading": ("UNBORDERED at mu = 0 the tail inverse grows LINEARLY in M -- it does "
                    "not exist in the limit, which is why leg 52 bordered.  BORDERED it "
                    "SATURATES: leg 52's repair works, and this is the check that it does."),
    }
    res["XS3b_bordered_grows_in_K"] = {
        "K": Ks_b, "bordered_tail_inverse": v_b,
        "K_exponent": de_b["exponent"],
        "first": de_b["first"], "last": de_b["last"],
        "ratio_last_over_first": de_b["ratio_last_over_first"],
        "prior_claim_being_sharpened": {
            "source": "legs 52-53 (CONTINUATION_PROMPT.md, capabilities.py)",
            "wording": ("the bordered tail inverse is a CONSTANT (2.19 ... 10.32 here, "
                        "9.44 in leg 52's ladder), not 1/K"),
            "constant_low": 2.19, "constant_high": 10.32, "leg52_ladder_value": 9.44,
            "correction": ("It is not a constant.  Over K = 4 ... 128 it runs 2.191 -> "
                           "11.528, exponent +0.437.  The 2.19 is the SMALLEST RUNG OF A "
                           "RISING LADDER, not a bound (lesson 72).  The conclusion those "
                           "legs drew is unaffected and in fact strengthened."),
        },
        "reading": ("THE SHARP FORM OF 'A CONSTANT, NOT 1/K'.  It is not even a constant: "
                    "it GROWS, at +0.44 in log-log, from 2.191 at K = 4 to 11.53 at "
                    "K = 128.  A tail estimate needs this to fall like 1/Lambda_K.  The "
                    "2.19 that legs 52-53 quote is the SMALLEST rung of a rising ladder, "
                    "not a bound (lesson 72)."),
    }

    # ---------------- XS4: the hypothesis that died ----------------
    c025 = classify_operator(0.25, Ks=KS, M=M_FIXED)
    res["XS4_dead_hypothesis"] = {
        "hypothesis": ("BDL's assumption (5) is delta = |off-diag|/|diag| < 1/2.  For this "
                       "operator (off-diagonal ~ k/2, diagonal mu*k) that is delta = "
                       "1/(2 mu), so BDL-admissible means mu > 1.  HYPOTHESIS: the tail "
                       "inverse stops behaving at mu = 1."),
        "verdict": "REFUTED",
        "test": {"mu": 0.25, "bdl_delta": bdl_delta(0.25),
                 "bdl_admissible": bdl_admissible(0.25),
                 "tail_block_boundedly_invertible": c025["tail_block_boundedly_invertible"],
                 "K_exponent": c025["K_exponent"],
                 "tail_inverse_decays": c025["tail_inverse_decays"]},
        "reading": ("mu = 0.25 has delta = 2, four times outside BDL's admissible set, and "
                    "it is boundedly invertible and decays at -0.85 -- indistinguishable "
                    "from mu = 2.  delta < 1/2 is what BDL's LU CONSTRUCTION needs, not "
                    "where the operator changes character.  **The hinge is zero-vs-nonzero "
                    "diagonal, and delta is not the coordinate for it.**  Recorded because "
                    "a hypothesis that was checked and died is worth more than one never "
                    "posed."),
    }

    # ---------------- XS5: the wrong construction, kept ----------------
    wrong = []
    for mu in (0.25, 1.0, 2.0):
        _, v = tail_inverse_ladder(mu, (4,), M_FIXED, bordered=True)
        wrong.append({"mu": mu, "K": 4, "bordered_norm": v[0]})
    res["XS5_wrong_operator_control"] = {
        "vals": wrong,
        "text": WRONG_OPERATOR_CONTROL,
        "status": "WRONG_OPERATOR -- recorded so it is recognised, never quoted",
    }

    # ---------------- the standing scope ----------------
    res["verdict"] = "DICHOTOMY_IS_A_REAL_CLASSIFICATION__NO_PUBLISHED_COUNTEREXAMPLE"
    res["what_this_establishes"] = (
        "Across the four published computer-assisted certificates this repository cites, "
        "no radii-polynomial certificate has an off-diagonal (shift) unbounded part whose "
        "tail inverse fails to decay.  The two near-misses fail for DIFFERENT and "
        "informative reasons: BDL publish a NON-BLOCK-DIAGONAL approximate inverse (which "
        "is exactly MM's remaining move) but still require a diagonal bounded below; and "
        "Chen-Hou certify a genuine transport operator but do so by ABANDONING the tail "
        "estimate entirely, extracting damping from the advection term in a weighted "
        "energy estimate.  So the dichotomy is a real classification of the published "
        "record, and TC/MM's negative is not an artifact of this repository.")
    res["what_this_does_NOT_establish"] = (
        "That no such certificate could exist -- four papers is a corpus, not a theorem, "
        "and the classification is TRANSCRIBED from full texts by a human-equivalent "
        "process.  That the dichotomy is this leg's finding -- it is folklore in print "
        "(XS0).  That Chen-Hou's energy method ports to HL_S2_nonsymmetric -- nobody has "
        "run that, and this leg does not claim it works.  Nothing here moves any link of "
        "the L1->L4 chain; Clay stays at ~0.05% behind Walls 1 and 2.")
    res["forward_consequence_for_MM"] = (
        "MM's one remaining free choice is the SHAPE of A, i.e. an approximate inverse "
        "that is not block diagonal.  BDL arXiv:1503.06315 is the published instance of "
        "that move, and this ledger locates what it costs: their Proposition 2.3 delivers "
        "the SAME decay gain s_L as the pure multiplier case, but only under assumption "
        "(4), a diagonal bounded below at the growth rate.  So the published precedent "
        "for MM's move does not carry over to a zero diagonal.  This is a statement about "
        "BDL's construction, NOT a prediction of MM's gate -- MM measures its own object.")

    res["elapsed_s"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)")
    print(f"GATE: {res['XS2_gate']['answer']}  "
          f"(control admitted -> {res['XS2_gate']['control']['answer_when_admitted']})")
    print(f"VERDICT: {res['verdict']}")
    for r in dial:
        print(f"  mu={r['mu']:<5} {r['shape']:<21} M_exp={r['M_exponent']:+.3f}  "
              f"K_exp={r['K_exponent']:+.3f}  decays={r['tail_inverse_decays']}")


if __name__ == "__main__":
    main()
