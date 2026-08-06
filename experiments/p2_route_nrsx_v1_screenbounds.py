#!/usr/bin/env python3
"""Leg 253 (Route-NRSX) -- pin the NRS/Tsai exclusion's EXACT hypothesis boundary at full text,
and sweep forward citations for published strengthenings that shrink the survivor space leg 251's
Phase-0 screen assumes.

    .venv/bin/python experiments/p2_route_nrsx_v1_screenbounds.py

THE QUESTION (pre-committed gate, both branches, DIRECTION.md leg 253):

    Does the full-text hypothesis set of NRS + Tsai, plus a forward-citation sweep for published
    strengthenings, leave the survivor classes named in 251's thesis (discretely self-similar;
    unstable-self-similar with finite unstable spectrum; non-self-similar) intact as genuinely
    not-excluded?

    YES -> bank the pinned hypothesis boundary as a checked input to Phase 0/1, with verbatim
           locators. 251's screen stands on read-and-verified footing rather than folklore.
    NO  -> name precisely which survivor class a published result excludes, with the locator.
           ESCALATE -- this narrows or redirects 251's/Phase 1's candidate space and must reach
           leg 251's agent before a candidate is banked. Push BRANCH ONLY, never main.

WHAT THIS IS. A literature leg has no PDE to integrate, so the runner is what keeps the prose
honest (the pattern legs 175/183/189/196/240/242/246 established): every hypothesis, every class
boundary and every count quoted in writeup/novelty/leg_253.md and experiments/journal/leg_253.md
is transcribed here ONCE, from the primary source, with its line locator in a named md5-pinned
extraction; the gate verdict is COMPUTED from that table rather than asserted. Emits
writeup/data/p2_route_nrsx_v1_screenbounds.json.

WHY THE VERDICT IS COMPUTED (lesson 90 -- a control that cannot come out differently is not a
control). The gate's NO branch escalates and parks the leg, so it must be reachable on evidence
that warranted it and not by prose alone. `classify()` takes the survivor-class table and returns
one of

    SURVIVORS_INTACT | SURVIVOR_CLASS_NARROWED_ONLY | SURVIVOR_CLASS_EXCLUDED

and `self_test()` exercises all three on perturbed copies of the evidence, so the actual verdict
is one the classifier could have failed to produce.

THE LIVE-PROBE CONTROL, AND IT IS BIDIRECTIONAL (lesson 90 again). The claim "Tsai 1998 does not
speak to discrete self-similarity, rotation, or the Type I bound" rests on three term counts
coming out ZERO in its extraction. A census that returns zero because it is not measuring
anything is exactly leg 53's failure. So:

  (a) the SAME census, the SAME code, on the LATER extractions must return NON-ZERO on those
      terms -- it returns discretely-self-similar 15 (Chae-Wolf DSS) and 16 (Pineau-Vicol),
      rotated 27 (Pineau-Vicol), Type I 26 (Pineau-Vicol) / 5 (KNSS);
  (b) and the control must FAIL where the candidates succeed, or "each net finds what the other
      misses" is not established: Pineau-Vicol scores local-energy 2 where Tsai scores 13, and
      KNSS scores axi-symmetric 25 where Pineau-Vicol scores 1.

Both directions are enforced by `assert_probe_is_live()`, which fails the run if either stops
being true. Neither set of zeros can then be an artifact of extraction or of the term list.

PROVENANCE. Papers/ is gitignored; every PDF below was pulled during this leg and extracted with
`pdftotext -layout`. `line` fields locate quotes in those extractions.

    Tsai ARMA 143 (1998) 29-51   pdf md5 5fae5eee4e91a570c8ab5ee3d0d71360  txt md5 972807cd94c5674949a9a03d4fd1ebae  1258 lines
    Tsai ARMA 147 (1999) 363     pdf md5 5d7d2a9c4a8830ccaa95d5fc22ced274  txt md5 8e2dd6ef5e99dab00bd2135b489a571f    32 lines  (ERRATUM)
    arXiv:1609.06962 (Chae-Wolf) pdf md5 f55d40788aaadbbd11b099c1a5cb7a43  txt md5 81700c68a6422b4db0b98af7f50b0d14  1332 lines
    arXiv:1610.09464 (Chae-Wolf) pdf md5 f1d14db17f643323cfa1a16ba661eb9d  txt md5 73279aa90ce78c1190d0027000fd1cf2  1002 lines
    arXiv:2607.09619 (Pineau-Vicol) pdf md5 542204791a1ea70b97d4e6414ffb3ba8 txt md5 f48ab020cce1aaffba043f8c32b416ca 1689 lines
    arXiv:0709.3599  (KNSS)      pdf md5 582ff7c7929c36f01aa34ddafa5c97a4  txt md5 ace4e69df8a990821968b4d8cd9929a4  1163 lines
    arXiv:1802.00038 (Bradshaw-Tsai survey) pdf md5 c6438cbf773b5af78c819d0ef60f4c59 txt md5 009690b4f76543b739da251e3b977510 1208 lines
    arXiv:math/0603126 (Hou-Li)  pdf md5 e2e7366c641809a69e51295cda6b7f08                                              (context only)

    NOT OBTAINED: Necas-Ruzicka-Sverak, Acta Math. 176 (1996) 283-294. Four routes returned HTML
    landing pages or 404s (intlpress fulltext path; link.springer.com/content/pdf/10.1007/
    BF02551584.pdf; Project Euclid .full; Project Euclid journalArticle/Download). This matches
    LITERATURE_CHECK.md l.197's standing record. Its hypotheses below are therefore tagged
    `restated_by` with the locator of a full-text primary restatement by a direct party (Tsai,
    Sverak's student, acknowledged as such at tsai-leray.txt l.1145-1146), NEVER `read_at_source`.

NO NETWORK ACCESS at run time; every network result is transcribed as data below. No solver
module is read, imported or edited. No stage is claimed; plan_of_record.py is untouched.

BANS CHECKED BEFORE STARTING (plan_of_record.py output read in full). One could bind and it is
not tripped:
  - "another DSS re-ask, or the DSS lane's expensive entrance" -- NOT TRIPPED. This leg does not
    re-ask whether this repository should enter the DSS lane, and proposes no entrance to it,
    cheap or expensive. It reads what the LITERATURE has published about the DSS class as a
    matter of bibliographic fact, which is the same read-only relationship legs 174/240/242/246
    have to their own banned lanes. The ban stays in force as written; nothing here lifts it, and
    the finding below in fact makes the DSS lane WORSE, not better.
Other bans: no gCLM is measured, no beta is re-measured, no scaling gauge is re-tested, no GA
compute is run, no l1-Fourier/collocation machinery is built, no leg 51 re-claim is made, stage V
is not re-opened, nothing is built at all so "grep capabilities.py first" is vacuous (grepped
anyway: nothing built).
"""

import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "writeup", "data", "p2_route_nrsx_v1_screenbounds.json")


# ---------------------------------------------------------------------------
# N1. THE SCREEN ITSELF, PINNED. Every hypothesis, at full text, with a locator.
#     `strength` orders the hypotheses from most restrictive (hardest to satisfy,
#     therefore weakest theorem) to least restrictive (easiest to satisfy,
#     therefore strongest theorem). This ordering is the whole point: leg 251's
#     one-line paraphrase "under the relevant decay" never named it.
# ---------------------------------------------------------------------------

SCREEN = [
    {
        "id": "NRS96",
        "result": "Necas-Ruzicka-Sverak, Acta Math. 176 (1996) 283-294",
        "ansatz": "exactly backward self-similar (SS), alpha = 0",
        "hypothesis": "U a weak solution of the Leray system (1.3) with U in L^3(R^3)",
        "conclusion": "U == 0",
        "source_status": "restated_by",
        "locator": "tsai-leray.txt l.79-80: 'The main result of [NRS] is that the only weak "
                   "solution of (1.3) belonging to L3(R3) is U == 0'; corroborated at "
                   "survey.txt l.74-75 and rotated.txt l.1657-1658 (ref [44])",
        "read_at_source": False,
    },
    {
        "id": "TSAI98-T1",
        "result": "Tsai, ARMA 143 (1998) 29-51, Theorem 1",
        "ansatz": "exactly backward self-similar (SS), alpha = 0",
        "hypothesis": "U a weak solution of (1.3) with U in L^q(R^3) for some q in (3, infinity]",
        "conclusion": "U constant (hence identically zero if q < infinity)",
        "source_status": "read_at_source",
        "locator": "tsai-leray.txt l.131-133",
        "read_at_source": True,
    },
    {
        "id": "TSAI98-T2",
        "result": "Tsai, ARMA 143 (1998) 29-51, Theorem 2",
        "ansatz": "exactly backward self-similar (SS), alpha = 0",
        "hypothesis": "u a weak solution of (1.1) of the form (1.2)_1 satisfying the LOCAL energy "
                      "estimates (1.4) in Q_1(0,T); explicitly NOT required to be Leray-Hopf, and "
                      "NO boundary condition imposed",
        "conclusion": "u identically zero",
        "source_status": "read_at_source",
        "locator": "tsai-leray.txt l.134-136; the 'not Leray-Hopf / only (i) and (ii)' "
                   "clarification is at l.236-238",
        "read_at_source": True,
    },
    {
        "id": "TSAI98-R53",
        "result": "Tsai, ARMA 143 (1998), Remark 5.3 -- THE SHARPEST FORM, and the one the "
                  "repository's paraphrase never carried",
        "ansatz": "exactly backward self-similar (SS), alpha = 0",
        "hypothesis": "|U(y)| <= b|y| for some b < a and |y| > r_0, together with P(y) = O(|y|^N) "
                      "for some N -- i.e. SUBLINEAR-relative-to-a growth, not decay at all",
        "conclusion": "triviality of U (stated as sufficient, via Lemma 5.1)",
        "source_status": "read_at_source",
        "locator": "tsai-leray.txt l.1121-1126",
        "read_at_source": True,
        "note": "Lemma 5.1 delivers 'Pi is constant' under this hypothesis; the last step from "
                "'Pi constant' to 'U == 0' in the printed proof (l.1104-1118) uses U in L^q or "
                "U -> 0 at infinity. Recorded as Tsai states it, with this caveat attached "
                "rather than silently dropped.",
    },
    {
        "id": "TSAI99-ERR",
        "result": "Tsai, ARMA 147 (1999) 363 -- erratum to the above",
        "ansatz": "n/a",
        "hypothesis": "n/a -- a factor s^{-2} is inserted inside the integral on p.47 line -5",
        "conclusion": "NO HYPOTHESIS CHANGES. 'Everything else remains the same.'",
        "source_status": "read_at_source",
        "locator": "tsai-leray-erratum.txt l.13-19",
        "read_at_source": True,
        "note": "Checked because a hypothesis change in an erratum would have been decisive for "
                "the whole screen. It is a typographical/technical correction only.",
    },
]

# ---------------------------------------------------------------------------
# N2. THE FORWARD SWEEP. Published strengthenings, in publication order.
#     Sweep method: Semantic Scholar forward citations of Tsai 1998
#     (paperId dd415ee4db27b93e0d72a2e95f8f0207ada443c4, DOI 10.1007/S002050050099,
#     citationCount 233), all 233 retrieved, title-filtered on
#     nonexist|non-exist|remov|liouville|triviality|exclud|self-similar|type i|discretely
#     -> 92 of 233 on-topic, read down to full text where the title touched the
#     BACKWARD case. Forward-in-time constructions (the bulk of the 92) are
#     recorded as not-on-question rather than discarded.
# ---------------------------------------------------------------------------

SWEEP_TOTALS = {
    "seed": "Tsai 1998 (S2 paperId dd415ee4db27b93e0d72a2e95f8f0207ada443c4)",
    "citations_retrieved": 233,
    "title_filter_hits": 92,
    "pulled_to_full_text": 5,
    "abstract_only_context": 1,
    "note": "NRS 1996's own forward set was not swept separately: it is a near-superset of the "
            "same community and Tsai 1998 is cited by every backward-case strengthening found "
            "here (verified: NRS96 and TSAI98 appear together in the reference list of every "
            "one of the five full-text sources). Recorded as a KNOWN GAP in the sweep, not as "
            "a completed double sweep.",
}

STRENGTHENINGS = [
    {
        "id": "CW17-LIOUVILLE",
        "result": "Chae & Wolf, arXiv:1609.06962, ARMA 225 (2017) 549-572, Thm 1.2 + Cor 1.4",
        "published": True,
        "class_touched": "SS (alpha = 0)",
        "hypothesis": "(U,P) smooth solution of the Leray system with U in L^{p,infinity}(R^3) "
                      "for SOME p in (3/2, infinity) -- weak-L^p, not L^p",
        "conclusion": "U is a constant function",
        "strengthens": "NRS96 (L^3) and TSAI98-T1 (L^q, q>3) -- the admissible exponent floor "
                       "drops from 3 to 3/2, and the space weakens from L^p to weak-L^p",
        "locator": "cw-liouville.txt l.62-68 (Thm 1.2), l.86-89 (Cor 1.4), l.90-91 ('improves "
                   "the previous results of [7, 8]')",
        "read_at_source": True,
        "also": "Thm 1.5 (l.93-101) additionally removes ASYMPTOTICALLY self-similar blow-up "
                "with a profile satisfying (1.8).",
    },
    {
        "id": "CW17-DSS",
        "result": "Chae & Wolf, arXiv:1610.09464, Comm. PDE 42(9) (2017) 1359-1374, Thm 1.1/1.3 "
                  "+ Remark 1.2",
        "published": True,
        "class_touched": "DSS -- A SURVIVOR CLASS NAMED BY LEG 251",
        "hypothesis": "Thm 1.1: u in C((-inf,0); L^p(R^3)) cap C^inf(Q), lambda-DSS for some "
                      "lambda > 1, 3 <= p < infinity. Thm 1.3: additionally |u| <= C_*/(sqrt(-t)+|x|) "
                      "and lambda in (1, lambda_*) with lambda_* = lambda_*(C_*) > 1.",
        "conclusion": "Thm 1.1: regular on Q minus the origin, and |u| <= C/(sqrt(-t)+|x|) -- i.e. "
                      "every DSS blow-up in this class is TYPE I. Thm 1.3: u == 0. Remark 1.2: "
                      "if u in C((-inf,0);L^3) then u is FULLY REGULAR (via Escauriaza-Seregin-"
                      "Sverak).",
        "strengthens": "first exclusion result inside the DSS class at all",
        "locator": "cw-dss.txt l.79-86 (Thm 1.1 and (1.3)), l.87 (Remark 1.2), l.92-99 (Thm 1.3), "
                   "l.100-101 (Remark 1.4: small C_* alone suffices)",
        "read_at_source": True,
        "magnitude": "lambda_* is NOT explicit anywhere in the paper: it is produced by a "
                     "compactness/contradiction argument and depends on C_*. No numerical value "
                     "is stated. Same for Remark 1.4's smallness threshold on C_*.",
    },
    {
        "id": "PV26-RSS",
        "result": "Pineau & Vicol, arXiv:2607.09619v1 (10 July 2026), Thm 1.4",
        "published": False,
        "class_touched": "RSS -- rotated backward self-similar, a class LEG 251 NEVER NAMED",
        "hypothesis": "u solves 3D NS on R^3 x [-1,0), satisfies the Type I bound "
                      "|u| <= C_{U,0}/(|x| + sqrt(-t)), and is rotated-self-similar with angular "
                      "speed alpha in the self-similar time variable",
        "conclusion": "there exist 0 < alpha_lo(C_{U,0}) << 1 and 1 << alpha_hi(C_{U,0}) < infinity "
                      "with U == 0 whenever |alpha| < alpha_lo or |alpha| > alpha_hi",
        "strengthens": "extends NRS96/TSAI98 off alpha = 0 for the first time; partially answers "
                       "a conjecture of Perelman (Tsai's book Conjecture 8.9; Bradshaw-Tsai Open "
                       "Problem 5.2)",
        "locator": "rotated.txt l.189-195 (Thm 1.4 and the explicit 'leaves open the case "
                   "alpha ~ 1'), l.135-144 (Conjecture 1.1 and its attribution), l.173-188 (why "
                   "it was open: the Bernoulli head-pressure maximum principle is destroyed by "
                   "the rotation terms)",
        "read_at_source": True,
        "magnitude": "alpha_lo and alpha_hi are NOT explicit; both depend on C_{U,0}. The open "
                     "window is stated qualitatively as alpha ~ 1.",
    },
    {
        "id": "PV26-DSS",
        "result": "Pineau & Vicol, arXiv:2607.09619v1, Thm 1.6 and Thm 1.7",
        "published": False,
        "class_touched": "DSS and RDSS -- SURVIVOR CLASSES",
        "hypothesis": "Thm 1.6: Type I bound + lambda-DSS, 1 < lambda < lambda_bar(C_{U,0}). "
                      "Thm 1.7: Type I bound + (alpha,lambda)-RDSS, with either |alpha| <= "
                      "alpha_bar and 1 < lambda < lambda_bar, or |alpha| >= alpha_bar and "
                      "1 < lambda < lambda_bar^{1/(1+alpha^2)}.",
        "conclusion": "U == 0 in each case",
        "strengthens": "recovers CW17-DSS by a quantitative weighted-L^2 method that does NOT "
                       "use the head-pressure maximum principle, and extends it to RDSS",
        "locator": "rotated.txt l.286-290 (Thm 1.6), l.337-344 (Thm 1.7), l.317 (the hierarchy "
                   "SS subset RSS subset DSS subset RDSS)",
        "read_at_source": True,
        "magnitude": "lambda_bar, alpha_bar NOT explicit; both depend on C_{U,0}.",
    },
    {
        "id": "AXI-TYPEI",
        "result": "Chen-Strain-Yau-Tsai, IMRN 2008 art. rnn016; Seregin-Sverak, Comm. PDE 34(2) "
                  "(2009) 171-201; mechanism at Koch-Nadirashvili-Seregin-Sverak, Acta Math. 203 "
                  "(2009) 83-105, Thm 6.1/6.2",
        "published": True,
        "class_touched": "ANY Type I blow-up under axisymmetry -- and DSS blow-up IS Type I "
                         "(CW17-DSS Thm 1.1), so this reaches a survivor class",
        "hypothesis": "u axisymmetric weak solution on R^3 x (0,T), in L^inf on R^3 x (0,T') for "
                      "each T' < T, with |u(x,t)| <= C/sqrt(x_1^2 + x_2^2) (KNSS Thm 6.1) or "
                      "|u| <= C/sqrt(T-t) plus an off-axis bound (KNSS Thm 6.2)",
        "conclusion": "|u| <= M(C): no singularity. Stated as a class fact by Pineau-Vicol: 'In "
                      "the axisymmetric setting, Type I blowup for 3D Navier-Stokes has been "
                      "ruled out [14, 51]; consequently, any putative singularity must be of "
                      "Type II.'",
        "strengthens": "orthogonal to NRS/Tsai -- a SECOND screen, on symmetry rather than decay",
        "locator": "rotated.txt l.160-162 (the class statement and its two references, whose "
                   "full entries are at l.1596-1597 and l.1672-1673); mechanism read at source "
                   "in knss.txt l.896-906 (Thm 6.1) and l.938-951 (Thm 6.2)",
        "read_at_source": True,
        "note": "The step 'DSS is Type I, hence axisymmetric DSS is dead' is a COMPOSITION of "
                "CW17-DSS Thm 1.1 with this result. Pineau-Vicol state the second half as a "
                "class fact; the composition is this leg's inference and is labelled as such. "
                "The bound direction checks out: |x| >= sqrt(x_1^2+x_2^2), so "
                "|u| <= C/(sqrt(-t)+|x|) implies |u| <= C/sqrt(x_1^2+x_2^2).",
    },
    {
        "id": "BT18-SURVEY",
        "result": "Bradshaw & Tsai, arXiv:1802.00038 (survey), section 1",
        "published": True,
        "class_touched": "the survivor space itself, stated by the experts",
        "hypothesis": "n/a -- survey",
        "conclusion": "(i) rotated backward SS do not exist under u in L^inf(-1,0;L^3) 'but this "
                      "is not known under the weaker assumption |u| <= C/(|x|+sqrt(-t)), even "
                      "though this assumption does exclude backward self-similar solutions'; "
                      "(ii) 'backward DSS solutions haven't been ruled out under any condition "
                      "when lambda is significantly larger than one'; (iii) Lorentz-space "
                      "generalizations by Chae-Wolf and by Guevara-Phuc are named as the state "
                      "of the art",
        "strengthens": "n/a -- this is the independent corroboration that the survivor space "
                       "below is the one the field itself recognises",
        "locator": "survey.txt l.72-104",
        "read_at_source": True,
    },
    {
        "id": "CIV26-EULER",
        "result": "Constantin, Ignatova & Vicol, arXiv:2602.17570 (v3, 20 July 2026)",
        "published": False,
        "class_touched": "3D EULER self-similar blow-up, and its liftability to NS",
        "hypothesis": "see abstract",
        "conclusion": "similarity exponent gamma >= 2/5 for finite kinetic energy; gamma >= 1/2 "
                      "under an outgoing property, and gamma >= 1/2 for axisymmetric C^2 profiles",
        "strengthens": "n/a -- adjacent",
        "locator": "abstract page only; the NS-relevant consequence is quoted from a source read "
                   "at full text: rotated.txt l.163-165, 'self-similar solutions of 3D Euler can "
                   "however be shown to not be viable for a lift to 3D Navier-Stokes, under a "
                   "local outgoing property [18]'",
        "read_at_source": False,
        "note": "ABSTRACT-ONLY. Recorded as context, and deliberately given NO weight in the "
                "gate verdict below -- the repository's full-text discipline is not waived, the "
                "read is simply labelled for what it is.",
    },
]

# ---------------------------------------------------------------------------
# N3. THE SURVIVOR CLASSES LEG 251 NAMED, adjudicated against N1+N2.
#     `status` is the only field the classifier reads.
# ---------------------------------------------------------------------------

SURVIVOR_CLASSES = [
    {
        "name": "discretely self-similar (DSS)",
        "as_named_by_251": True,
        "status": "NARROWED",
        "what_is_dead": [
            "lambda in (1, lambda_bar(C_{U,0})) under the Type I bound -- CW17-DSS Thm 1.3, "
            "re-proved quantitatively as PV26-DSS Thm 1.6",
            "any DSS with u in C((-inf,0); L^3(R^3)) -- CW17-DSS Remark 1.2, via "
            "Escauriaza-Seregin-Sverak",
            "AXISYMMETRIC DSS entirely: DSS blow-up in the CW17 class is Type I (CW17-DSS Thm "
            "1.1), and axisymmetric Type I is ruled out (AXI-TYPEI). This is a composition, "
            "flagged as such.",
        ],
        "what_survives": "non-axisymmetric DSS with lambda significantly larger than 1 and a "
                         "profile not in L^inf_t L^3 -- corroborated verbatim at BT18-SURVEY "
                         "(ii): 'backward DSS solutions haven't been ruled out under any "
                         "condition when lambda is significantly larger than one'",
        "quantified": False,
        "quantification_note": "lambda_bar has NO published numerical value. A Phase-0 candidate "
                               "cannot buy safety by picking a lambda and citing these papers.",
    },
    {
        "name": "unstable-self-similar with finite unstable spectrum",
        "as_named_by_251": True,
        "status": "EXCLUDED",
        "what_is_dead": [
            "the class as literally worded, for the unforced backward 3D NS blow-up problem. "
            "The exclusion is STABILITY-BLIND: NRS96/TSAI98-T1 and CW17-LIOUVILLE constrain the "
            "profile U through its integrability alone and say nothing about the spectrum of "
            "the linearisation. Under merely the Type I bound |U| <= C/(1+|y|) the profile lies "
            "in L^p for every p > 3 (stated at rotated.txt l.176-180), so TSAI98-T1 applies and "
            "U == 0 -- however unstable that U would have been."
        ],
        "what_survives": "nothing, under the ansatz as worded. It survives only by LEAVING the "
                         "hypothesis set: forced NS, forward-in-time, non-Type-I (growing) "
                         "profiles, or a rotated ansatz -- and each of those is a different "
                         "class that leg 251 must name explicitly rather than fold into this one.",
        "quantified": True,
        "quantification_note": "The implication Type-I-bound => U in L^p for all p>3 is exact and "
                               "is stated at rotated.txt l.176-180; it needs no constant.",
    },
    {
        "name": "non-self-similar",
        "as_named_by_251": True,
        "status": "INTACT",
        "what_is_dead": [],
        "what_survives": "the whole class, and it is now FORCED rather than merely permitted: "
                         "AXI-TYPEI's consequence as stated by Pineau-Vicol is that any putative "
                         "axisymmetric singularity 'must be of Type II', i.e. must break the "
                         "self-similar rate outright.",
        "quantified": True,
        "quantification_note": "n/a -- an unexcluded class needs no constant.",
    },
    {
        "name": "rotated (discretely) self-similar -- RSS / RDSS",
        "as_named_by_251": False,
        "status": "OPEN_WINDOW_251_DID_NOT_NAME",
        "what_is_dead": [
            "|alpha| << 1 and |alpha| >> 1 under the Type I bound -- PV26-RSS Thm 1.4",
            "the RDSS corners of PV26-DSS Thm 1.7",
        ],
        "what_survives": "alpha ~ 1 for RSS -- stated in as many words at rotated.txt l.195, "
                         "'leaves open the case alpha ~ 1' -- and RDSS outside Thm 1.7's two "
                         "windows. This is an expert-flagged open problem (Perelman, via Tsai's "
                         "book Conjecture 8.9 and Bradshaw-Tsai Open Problem 5.2), NOT a gap "
                         "nobody has looked at.",
        "quantified": False,
        "quantification_note": "alpha_lo, alpha_hi depend on C_{U,0} with no published numbers.",
    },
]

# ---------------------------------------------------------------------------
# N4. THE LIVE-PROBE CONTROL. Term counts, measured once over the pinned
#     extractions and transcribed. Bidirectional, per lesson 90.
# ---------------------------------------------------------------------------

CENSUS = {
    # extraction            dss  rotated  typeI  localenergy  axi-symmetric
    "tsai-leray.txt":      {"discretely self-similar": 0, "rotated": 0, "Type I": 0,
                            "local energy": 13, "axi-symmetric": 0, "Liouville": 5},
    "cw-dss.txt":          {"discretely self-similar": 15, "rotated": 0, "Type I": 0,
                            "local energy": 7, "axi-symmetric": 0, "Liouville": 1},
    "cw-liouville.txt":    {"discretely self-similar": 0, "rotated": 0, "Type I": 3,
                            "local energy": 6, "axi-symmetric": 0, "Liouville": 4},
    "rotated.txt":         {"discretely self-similar": 16, "rotated": 27, "Type I": 26,
                            "local energy": 2, "axi-symmetric": 1, "Liouville": 12},
    "knss.txt":            {"discretely self-similar": 0, "rotated": 0, "Type I": 5,
                            "local energy": 2, "axi-symmetric": 25, "Liouville": 9},
    "survey.txt":          {"discretely self-similar": 9, "rotated": 3, "Type I": 0,
                            "local energy": 19, "axi-symmetric": 0, "Liouville": 1},
}


def assert_probe_is_live(census=CENSUS):
    """Both directions of the control. Raises AssertionError if either fails."""
    # (a) the terms that are ZERO in the 1998 control must be NON-ZERO somewhere later.
    for term, where in (("discretely self-similar", "cw-dss.txt"),
                        ("rotated", "rotated.txt"),
                        ("Type I", "rotated.txt")):
        assert census["tsai-leray.txt"][term] == 0, \
            f"control broken: Tsai 1998 unexpectedly mentions {term!r}"
        assert census[where][term] > 0, \
            f"probe dead: {term!r} scores zero in {where} too -- the census is not measuring"
    # (b) the control must WIN where the later papers lose, or the nets are not distinct.
    assert census["tsai-leray.txt"]["local energy"] > census["rotated.txt"]["local energy"], \
        "probe not discriminating: Tsai 1998 should dominate on 'local energy'"
    assert census["knss.txt"]["axi-symmetric"] > census["rotated.txt"]["axi-symmetric"], \
        "probe not discriminating: KNSS should dominate on 'axi-symmetric'"
    return True


# ---------------------------------------------------------------------------
# N5. THE VERDICT, COMPUTED.
# ---------------------------------------------------------------------------

def classify(classes):
    """SURVIVORS_INTACT | SURVIVOR_CLASS_NARROWED_ONLY | SURVIVOR_CLASS_EXCLUDED.

    Only classes leg 251 actually named can answer the gate; a class 251 did not name
    cannot make its screen wrong, however interesting it is.
    """
    named = [c for c in classes if c["as_named_by_251"]]
    if any(c["status"] == "EXCLUDED" for c in named):
        return "SURVIVOR_CLASS_EXCLUDED"
    if any(c["status"] == "NARROWED" for c in named):
        return "SURVIVOR_CLASS_NARROWED_ONLY"
    return "SURVIVORS_INTACT"


def gate_answer(verdict):
    return "YES" if verdict == "SURVIVORS_INTACT" else "NO"


def self_test():
    """Exercise all three classifier outcomes on perturbed copies of the evidence."""
    import copy
    results = {}

    real = classify(SURVIVOR_CLASSES)
    results["actual"] = real

    # perturbation 1: the excluded class is only narrowed -> NARROWED_ONLY
    p1 = copy.deepcopy(SURVIVOR_CLASSES)
    for c in p1:
        if c["status"] == "EXCLUDED":
            c["status"] = "NARROWED"
    results["if_no_class_were_excluded"] = classify(p1)

    # perturbation 2: nothing found at all -> INTACT (the gate's YES branch, reachable)
    p2 = copy.deepcopy(SURVIVOR_CLASSES)
    for c in p2:
        if c["as_named_by_251"]:
            c["status"] = "INTACT"
    results["if_the_sweep_had_found_nothing"] = classify(p2)

    # perturbation 3: the class 251 never named is excluded, but no named class is
    #                 -> still INTACT. The classifier must not answer the gate with a
    #                 class the gate did not ask about.
    p3 = copy.deepcopy(SURVIVOR_CLASSES)
    for c in p3:
        c["status"] = "INTACT" if c["as_named_by_251"] else "EXCLUDED"
    results["if_only_the_unnamed_class_were_hit"] = classify(p3)

    assert results["actual"] == "SURVIVOR_CLASS_EXCLUDED"
    assert results["if_no_class_were_excluded"] == "SURVIVOR_CLASS_NARROWED_ONLY"
    assert results["if_the_sweep_had_found_nothing"] == "SURVIVORS_INTACT"
    assert results["if_only_the_unnamed_class_were_hit"] == "SURVIVORS_INTACT"
    return results


def main():
    assert_probe_is_live()
    st = self_test()
    verdict = classify(SURVIVOR_CLASSES)
    answer = gate_answer(verdict)

    payload = {
        "leg": 253,
        "route": "NRSX",
        "date": "2026-08-07",
        "question": (
            "Does the full-text hypothesis set of NRS + Tsai, plus a forward-citation sweep "
            "for published strengthenings, leave the survivor classes named in 251's thesis "
            "(discretely self-similar; unstable-self-similar with finite unstable spectrum; "
            "non-self-similar) intact as genuinely not-excluded?"
        ),
        "gate_answer": answer,
        "verdict": verdict,
        "escalate": answer == "NO",
        "screen": SCREEN,
        "sweep_totals": SWEEP_TOTALS,
        "strengthenings": STRENGTHENINGS,
        "survivor_classes": SURVIVOR_CLASSES,
        "census": CENSUS,
        "self_test": st,
        "clay_odds_unchanged": "0.05% -- this leg moves no link of the L1->L4 chain. It removes "
                               "a folklore dependency from a screen and narrows a candidate "
                               "space. That is not movement toward Clay.",
        "honesty": {
            "nrs_not_read_at_source": True,
            "nrs_routes_tried": 4,
            "abstract_only_sources": ["CIV26-EULER"],
            "unpublished_preprints_relied_on": ["PV26-RSS", "PV26-DSS"],
            "inferences_not_published_as_such": [
                "AXI-TYPEI composed with CW17-DSS Thm 1.1 to kill axisymmetric DSS"
            ],
            "known_sweep_gap": SWEEP_TOTALS["note"],
        },
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    print("Leg 253 / Route-NRSX -- NRS/Tsai screen boundary")
    print("-" * 78)
    print(f"  citations swept (Tsai 1998) : {SWEEP_TOTALS['citations_retrieved']}")
    print(f"  on-topic after title filter : {SWEEP_TOTALS['title_filter_hits']}")
    print(f"  pulled to full text         : {SWEEP_TOTALS['pulled_to_full_text']}")
    print(f"  hypotheses pinned           : {len(SCREEN)}  "
          f"({sum(1 for s in SCREEN if s['read_at_source'])} read at source)")
    print(f"  strengthenings recorded     : {len(STRENGTHENINGS)}")
    print()
    for c in SURVIVOR_CLASSES:
        tag = "251-named" if c["as_named_by_251"] else "NOT named by 251"
        print(f"  [{c['status']:<28}] {c['name']}  ({tag})")
    print()
    print(f"  live-probe control          : PASS (bidirectional)")
    print(f"  classifier self-test        : {st}")
    print(f"  VERDICT                     : {verdict}")
    print(f"  GATE ANSWER                 : {answer}  -> "
          f"{'ESCALATE, push branch only' if answer == 'NO' else 'bank, normal landing'}")
    print(f"  wrote {os.path.relpath(OUT, REPO)}")


if __name__ == "__main__":
    main()
