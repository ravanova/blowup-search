"""P2 Route-XUL v1 -- leg 171: does Xu arXiv:2607.19762 characterize this operator's
invertibility / certificate-buildability on any space OTHER than origin-H^2 and `ell^1_w`?

A LITERATURE leg, and a DEEP-MINE of a paper this repository already had.  It builds no
solver module, imports none, edits none (`solver/literature_gates.py` and
`solver/spectral_certificate.py` are untouched, as the territory requires), touches no
shared ledger, lifts no ban and moves no link of the `L1 -> L4` chain.

THE GATE, verbatim from `DIRECTION.md` leg 171:

    "Does Xu arXiv:2607.19762, at full-text depth, characterize the operator's invertibility
     or certificate-buildability on any space OTHER than origin-H^2 and `ell^1_w`
     (explicitly, or as a derivable corollary of a stated general theorem)?"

    ANSWER: YES -- decisively, and in the paper's own voice.  Section 3.1 (p. 8) carries a
    paragraph headed "Map of realizations." that enumerates THREE realizations of the SAME
    operator with THREE DIFFERENT verdicts, Section 5.7 adds a fourth (`C^1`), Section 3.2
    adds a fifth (full `L^2(R)`, even sector included), Section 4.4 works in a sixth (the
    Hardy block `X_+`), and APPENDIX A adds a one-parameter FAMILY `Y_theta` on which the
    answer is EXACT (operator norm `e^{(1-theta) tau}`, constant 1, every function).

    Per the gate's yes-branch this leg RECORDS AND ESCALATES.  It builds and tests nothing.

WHAT `ell^1_w` HAS TO DO WITH IT: nothing, in Xu.  `ell^1_w` is THIS repository's space (legs
51-54, 58, 127); Xu never mentions a weighted sequence space and the runner's NEGATIVE
locators check exactly that.  So the gate's "other than origin-H^2 and `ell^1_w`" reduces, on
Xu's side, to "other than origin-H^2".

WHY IT IS A SCRIPT AND NOT ONLY PROSE (lesson 68; legs 57/65/112/141's ledgers).  Three jobs
no amount of prose does:

  (1) VERBATIM PRESENCE.  Every quote the verdict rests on is re-located in the actual PDF
      text at run time by whitespace-insensitive substring match, so a misquote or a
      hallucinated sentence fails loudly instead of decaying at the rate of memory.
      `Papers/` is gitignored, so when the PDF is absent the flags are read back from the
      committed JSON and clearly LABELLED as such -- never silently defaulted to True.

  (2) NEGATIVE LOCATORS (lesson 90 -- a control that cannot come out differently is not a
      control).  Five fragments that must NOT be in the paper: a weighted-`ell^1`/sequence
      space, a CLAIM that the `H^3` realization is proved rather than expected, a claim that
      the `a > 0` exactness question is settled, and a claim that the Evans strand is a
      proof.  If any of these ever reports LOCATED, this leg's reading is wrong and the
      script says so.  Declared in `writeup/novelty/leg_171.md` sec 3 BEFORE it was coded.

  (3) THE TWO ESSENTIAL LINES, RECONSTRUCTED FROM XU'S CLOSED FORMS AND CHECKED AGAINST XU'S
      OWN PRINTED NUMBERS.  This is the falsifiable core, and it CAN report the other answer.
      Xu states the far-field line at `Re = -1 + c_l/2` and the origin line at
      `Re = lambda_X = -c~/2` with `c~ = c_l + a HOmega(0)`, `HOmega(0) = (1+c_l)/(1-a)`
      (Proposition 1, sec 3.1).  Feeding ONLY Xu's Table 1 branch `c_l(a)` through those
      closed forms must reproduce, independently, four printed facts:
        * Table 1's own "far-field 1 - c_l/2" column and its `s*(a) = 1/c_l` column;
        * the two lines COINCIDE at `a = 0` and EXACTLY at `a = 1/2` (Figure 2 caption);
        * the maximum protrusion of the origin line into the strip is `~0.036` at `a ~ 0.26`
          (Figure 2 caption and sec 2: "at most 0.037", "-0.0362 at a ~ 0.264");
        * both lines stay strictly left of `Re = -1/2` for every `a > 0` on the branch.
      A wrong reading of `c~`, of `HOmega(0)`, or of which line is which fails all four.
      It also re-derives the two `Y_theta` consistency identities of Appendix A
      (`1 - theta = -1/2 <=> theta = 3/2`, and the core weight `y^{-2 theta - 1} = y^{-4}`
      at that theta), which is what pins Xu's exact decay rate to Theorem 1's essential edge.

    bash Papers/fetch.sh 2607.19762
    .venv/bin/python experiments/p2_route_xul_v1_lit.py
        -> writeup/data/p2_route_xul_v1_lit.json

NO FIGURE: no measurement of a curve of this repository's own; every number here is Xu's or
arithmetic on Xu's ("no measurement, no figure", the convention leg 141 also used).

VERSION ACTUALLY READ (recorded because a version mismatch silently invalidates a locator):
arXiv:2607.19762v1, 22 Jul 2026, physics.flu-dyn, 41 pp -- the version this repository
already cites in `capabilities.py` and in leg 127's journal.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_xul_v1_lit.json"
PAPERS = ROOT / "Papers"
ARXIV = "2607.19762"

GATE = ("Does Xu arXiv:2607.19762, at full-text depth, characterize the operator's "
        "invertibility or certificate-buildability on any space OTHER than origin-H^2 and "
        "`ell^1_w` (explicitly, or as a derivable corollary of a stated general theorem)?")

GATE_ANSWER = "YES"

GATE_YES_BRANCH_VERBATIM = (
    "Record every additional space and its verdict, verbatim with hypotheses. ESCALATE as "
    "directly informing leg 163's scoping and leg 165's synthesis -- do not build or test "
    "anything under this leg's own authority.")


# ---------------------------------------------------------------------------
# 1. THE SPACES.  `fragment` is re-located in the PDF at run time; `quote` is the reading
#    quote; `verdict` is the paper's own verdict for THAT space; `already_banked_by` says
#    which earlier leg of this repository already carries it, so nothing is re-claimed.
# ---------------------------------------------------------------------------
SPACES = [
    {
        "id": "S0-ORIGIN-H2",
        "space": "X, the origin-H^2 realization (the odd part of H^2(R), with the origin "
                 "condition phi = a1 y + o(y))",
        "definition": ("X = {phi : phi odd, phi, phi'' in L^2(0, inf), phi(y) = a1 y + o(y) "
                       "as y -> 0}, norm ||phi||_X^2 = ||phi||_{L^2}^2 + ||phi''||_{L^2}^2 "
                       "(Definition 4.1, eq (4.2) = eq (3.2))"),
        "locator": "Theorem 1 (sec 3.1 eq (3.3)), Theorem 2 (sec 3.3 eq (3.8)), Prop. 4.6",
        "verdict": "ALIVE, PROVED -- essential spectrum meets {Re >= -1/2} in the single line "
                   "{Re = -1/2}; full point spectrum over C is exactly {0, 1}; the open strip "
                   "is resolvent set with an EXPLICIT two-sided bounded inverse; gap 1/2 "
                   "after modulation",
        "verdict_kind": "PROVED_ALIVE",
        "quote": ("sigma_ess(L0|X) cap {Re lambda >= -1/2} = {Re lambda = -1/2}   ... "
                  "sigma_disc(L0|X) cap {Re > -1/2} = {0, +1}"),
        "fragment": "the single vertical line",
        "hypotheses": ("a = 0 and the EXACT CLM profile Omega = -y/(y^2 + 1/4), c_l = 1 "
                       "(Definition 4.2: 'At a = 0 the exact profile is used and nothing "
                       "below is assumed'). For a > 0 everything is conditional on Adm(a) "
                       "(H1)-(H4) AND the essential spectrum becomes a TWO-line inclusion, "
                       "not an equality (Proposition 1)."),
        "already_banked_by": "leg 127 -- experiments/journal/leg_127.md l. 32-38. THE one "
                             "fact legs 127/163 use. Not new here.",
        "is_new_to_this_repo": False,
    },
    {
        "id": "S1-MAP",
        "space": "(the paper's own enumeration paragraph, not a space)",
        "definition": "Section 3.1, p. 8, the paragraph headed 'Map of realizations.'",
        "locator": "sec 3.1, p. 8",
        "verdict": "THIS PARAGRAPH IS THE GATE'S ANSWER: Xu himself enumerates three "
                   "realizations of the same operator with three different verdicts and says "
                   "each statement names the realization it lives in",
        "verdict_kind": "ENUMERATION",
        "quote": ("One realization is the one we work in and the others are named "
                  "alternatives. The chosen realization is X (origin-H^2): Theorem 1 and "
                  "Proposition 1 live there, and its essential spectrum for a in (0, 1/2) "
                  "contains two lines. The maximal L^2 realization (Section 4.6) is the "
                  "weaker alternative, in which the whole strip is spectrum. A "
                  "third-derivative realization is a stronger alternative in which the "
                  "included origin line moves left and a single far-field line is expected "
                  "to survive for all a; we do not pursue it here. Each statement names the "
                  "realization it lives in."),
        "fragment": "One realization is the one we work in and the others are named",
        "hypotheses": "none -- it is Xu's own summary sentence",
        "already_banked_by": None,
        "is_new_to_this_repo": True,
    },
    {
        "id": "S2-MAXIMAL-L2",
        "space": "the plain MAXIMAL L^2 realization (no origin condition imposed)",
        "definition": "L^2 with the graph domain and no origin regularity requirement "
                      "(sec 4.6; sigma_ess read in the Browder sense there)",
        "locator": "Proposition 2 (sec 3.1 eq (3.5)); proof sec 4.6",
        "verdict": "DEAD, PROVED -- the WHOLE vertical strip {-1/2 <= Re <= 3/2} is essential "
                   "spectrum; every strip point is a genuine eigenvalue with an explicit odd "
                   "eigenfunction; NO L^2 spectral gap at all, hence no certificate",
        "verdict_kind": "PROVED_DEAD",
        "quote": ("sigma_ess(L0) contains {lambda : -1/2 <= Re lambda <= 3/2}, the full "
                  "vertical strip between the two indicial lines ... Hence on the maximal "
                  "L^2 realization the whole open strip consists of eigenvalues; no point of "
                  "it is isolated ... In particular there is no L^2 spectral gap."),
        "fragment": "In particular there is no L2 spectral gap",
        "hypotheses": ("a = 0, exact profile. The strip is filled by the EXPLICIT family "
                       "u_lambda(y) = y^{1-lambda}/(y + i/2)^2 for -1/2 < Re lambda < 3/2, "
                       "whose odd two-branch combinations phi_lambda := B_+ - S B_+ are "
                       "genuine eigenfunctions at every strip point (sec 4.6 eq (4.33)). "
                       "The single separating feature is the second derivative at the "
                       "origin: u''_lambda ~ y^{-1-lambda}, and int |u''_lambda|^2 diverges "
                       "exactly when Re lambda >= -1/2, except at lambda in {0, 1}."),
        "already_banked_by": ("leg 64 (Route-RC realization audit) -- "
                              "experiments/p2_route_rc_v1_realization_audit.py l. 26, "
                              "306-310; PHASE2_P2_NOTES.md sec 27; LITERATURE_CHECK.md sixth "
                              "pass item 4; experiments/p2_route_lga_v1_ledger.py l. 142-149. "
                              "CITED, NOT CLAIMED."),
        "is_new_to_this_repo": False,
    },
    {
        "id": "S3-C1-ORIGIN",
        "space": "the merely-C^1-at-the-origin realization (condition (D3) dropped: one "
                 "derivative fewer than X)",
        "definition": "odd, L^2, C^1(R) distributional eigenfunctions, WITHOUT the second-"
                      "derivative origin condition that defines X (sec 5.7)",
        "locator": "sec 5.7, 'The smoothness hypothesis is sharp'",
        "verdict": "DEAD, PROVED -- the open strip fills with a CONTINUUM of point spectrum. "
                   "Strictly sharper than the maximal-L^2 statement: the invertibility is "
                   "destroyed by relaxing the origin condition by ONE derivative, not by "
                   "dropping it altogether",
        "verdict_kind": "PROVED_DEAD",
        "quote": ("Dropping condition (D3) admits a continuum of eigenfunctions. The Case-3 "
                  "functions are genuine odd, L^2, C^1(R) distributional eigenfunctions of "
                  "L0 for every real lambda in (-1/2, 0) (and for complex lambda with "
                  "Re lambda in (-1/2, 0)): they solve the equation classically away from "
                  "the origin and distributionally across it (a C^1 function carries no "
                  "distributional surplus at a point). On a merely C^1 domain the open strip "
                  "would therefore fill with a continuum of point spectrum."),
        "fragment": "On a merely C 1 domain the open strip would therefore fill with a continuum of point spectrum",
        "hypotheses": ("a = 0, exact profile. Witness verified at lambda = -1/4, mu = 5/4: "
                       "the odd real combination 2 Re(c B_+) is C^1 (its quotient phi/y "
                       "vanishes like y^{1/4}) but its second derivative diverges like "
                       "y^{mu-2} at the origin, so it satisfies (D1), (D2), (D4) and fails "
                       "(D3)."),
        "already_banked_by": None,
        "is_new_to_this_repo": True,
    },
    {
        "id": "S4-H3",
        "space": "the third-derivative (H^3) realization: phi''' in L^2 near the origin",
        "definition": "a STRONGER origin condition than X's phi'' in L^2 (sec 3.1 'Map of "
                      "realizations'; sec 4.5; sec 4.6)",
        "locator": "sec 3.1 (map), sec 4.5 (exactness questions), sec 4.6 (mechanism)",
        "verdict": "EXPECTED ALIVE AND STRICTLY BETTER THAN X FOR a > 0 -- NOT PROVED. The "
                   "origin line moves left and a single far-field line is EXPECTED to "
                   "survive uniformly in a, which would remove X's own a > 0 defect. Xu "
                   "explicitly does not pursue it, and its exactness is the same open "
                   "question as X's",
        "verdict_kind": "EXPECTED_NOT_PROVED",
        "quote": ("Whether sigma_ess equals this union for a > 0, and whether a stronger "
                  "third-derivative realization (phi''' in L^2 near the origin) leaves the "
                  "single far-field line uniformly in a, are exactness questions (Section "
                  "4.5). ... The origin line is a feature of the H^2 realization that a "
                  "stronger H^3 realization is expected to remove (the H^3 weight shifts the "
                  "included origin exponent; exactness for the stronger realization is the "
                  "same open question) ... A stronger H^3 realization shifts the included "
                  "origin line off ... so for a > 0 the two-line picture is relative to the "
                  "choice of realization."),
        "fragment": "a stronger third-derivative realization",
        "hypotheses": ("NONE STATED -- this is a named alternative Xu explicitly does NOT "
                       "pursue ('we do not pursue it here'). It is a conjecture with a "
                       "stated mechanism, not a theorem, and any downstream leg quoting it "
                       "must carry that word."),
        "already_banked_by": None,
        "is_new_to_this_repo": True,
    },
    {
        "id": "S5-Y-THETA",
        "space": "the weighted conjugated family Y_theta (theta > 0), and the direct sum "
                 "script-Y_theta = Y_theta (+) Y_theta",
        "definition": ("v = b^2 u with b = y + i/2; ||v||^2_{Y_theta} = int_0^inf |v|^2 "
                       "y^{-2 theta - 1} dy = int_0^inf |u|^2 (y^2 + 1/4)^2 y^{-2 theta - 1} "
                       "dy (Definition A.2, eq (A.14)). DISTINCT from the physical "
                       "realization X, and reached from it by a bounded transfer map."),
        "locator": "Appendix A, Definition A.2 + Proposition A.3 (eq (A.15)) + eq (A.19)-(A.24)",
        "verdict": "ALIVE AND EXACT FOR EVERY theta > 0 -- A_theta is NORMAL on Y_theta with "
                   "spectrum the single vertical line {Re = 1 - theta}, and the semigroup "
                   "norm is EXACTLY e^{(1-theta) tau} with constant 1, for every function. "
                   "At theta = 3/2 the rate is exactly e^{-tau/2}, matching Theorem 1's "
                   "essential edge. This is the strongest certificate-shaped statement in "
                   "the paper, and it is NOT on origin-H^2",
        "verdict_kind": "PROVED_ALIVE_EXACT",
        "quote": ("In particular A_theta is normal on Y_theta, equal to (1 - theta) plus a "
                  "skew-adjoint part, with spectrum the single vertical line "
                  "{Re = 1 - theta} and e^{A tau} equal to e^{(1-theta) tau} times a unitary "
                  "group; this normality is the structural reason the operator norm is exact "
                  "and function-independent.   [Prop. A.3: ||e^{A tau}||_{Y_theta -> "
                  "Y_theta} = e^{(1-theta) tau}  (constant 1, every function).]   In "
                  "Y_{3/2} (core weight y^{-4}, plain L^2 at infinity) both essential lines "
                  "of L0 coincide at Re = -1/2: the far-field line stays at -1/2, and the "
                  "origin line, which in plain L^2 sits at the pathological Re = +3/2 "
                  "(Proposition 2 and Section 4.6), is pushed to -1/2 by the y^{-4} core "
                  "weight."),
        "fragment": "(constant 1, every function)",
        "hypotheses": (
            "SHARP AND RESTRICTIVE, and these are what a downstream leg would trip on. "
            "(a) a = 0 only, and the statement is about the CONJUGATED variable v = b^2 u, "
            "not the physical one -- Xu's abstract keeps them separate BECAUSE 'L0 is "
            "non-normal and a spectral gap does not by itself give a decay rate in the X "
            "norm'. "
            "(b) The two symmetry modes are NOT IN Y_{3/2}: 'The two symmetry modes are "
            "excluded from Y_{3/2} by that weight' (their integrands behave like y^{-4} and "
            "y^{-2} at the origin and diverge) -- so the pure semigroup decays at the "
            "essential rate with NO projection inside the space. "
            "(c) Y_theta carries NO pointwise origin traces, so the modulation projection "
            "CANNOT act inside it; it acts on the physical X (which has traces) and is "
            "mapped in by the bounded transfer J_X : X -> script-Y_{3/2}, giving "
            "||S_Y(tau) J_X phi|| <= C_Q e^{-tau/2} ||phi||_X. THE EXACT CONSTANT 1 BELONGS "
            "TO S_Y ON Y_{3/2}; THE COMPOSITE CARRIES C_Q, NOT 1. "
            "(d) theta is PINNED for physical X-data by a two-sided squeeze: the tail forces "
            "theta >= 3/2, the (sharp) double Hardy inequality forces theta <= 3/2, so 'the "
            "physical-data statement is the single space Y_{3/2}'. Only for origin-analytic "
            "forcing does the whole range theta in (1, 2) open up."),
        "already_banked_by": ("leg 141 touched Appendix A for ONE remark only ('App A has the "
                              "same weight-ejects-the-modes tension, resolved by transferring "
                              "rather than reported', writeup/novelty/leg_141.md). The space "
                              "family, the normality, the exact norms and the pinned "
                              "theta = 3/2 are UNMINED."),
        "is_new_to_this_repo": True,
    },
    {
        "id": "S6-HARDY-XPLUS",
        "space": "the Hardy block space X_+ = {u in H^2_+ : u'' in L^2}",
        "definition": "the upper-half-plane Hardy summand of X, with ||phi||_X^2 = "
                      "2 ||P_+ phi||_{X_+}^2 (sec 4.4)",
        "locator": "sec 4.4 (eq (4.21)-(4.25)), Lemma 4.5, Proposition 4.6",
        "verdict": "ALIVE, PROVED, AND IT IS WHERE THE EXPLICIT INVERSE ACTUALLY LIVES -- the "
                   "resolvent is built blockwise R0(z) = R0^+(z) (+) R0^-(z) from the SCALAR "
                   "reduction L0^+ = -1 - y d/dy + i/(y + i/2), with an EXACT Hardy-Mellin "
                   "operator norm ||T_z|| = 1/(Re z + 1/2) = 1/alpha and an assembled "
                   "analytic majorant M_an ~ alpha^{-3/2}",
        "verdict_kind": "PROVED_ALIVE",
        "quote": ("The generalized Hardy operator T_z g(y) := int_0^1 s^z g(ys) ds = "
                  "y^{-1-z} int_0^y t^z g(t) dt is bounded on L^2(0, inf) with exact norm "
                  "1/(Re z + 1/2) = 1/alpha; its Mellin symbol is 1/(z + 1/2 - i xi), whose "
                  "modulus is maximized at xi = Im z."),
        "fragment": "with exact norm",
        "hypotheses": ("a = 0 and the exact profile, via the single-simple-pole identity "
                       "H Omega - i Omega = i/(y + i/2), which is what collapses the "
                       "NONLOCAL operator to a scalar first-order ODE. This collapse is "
                       "'exact only at the single-pole a = 0 profile' (sec 8) -- it does not "
                       "survive to a > 0."),
        "already_banked_by": None,
        "is_new_to_this_repo": True,
    },
    {
        "id": "S7-FULL-L2-EVEN",
        "space": "the FULL L^2(R) realization with the even sector included (i.e. X's "
                 "oddness restriction dropped, origin condition kept or not)",
        "definition": "L^2(R) without the odd restriction (sec 3.2)",
        "locator": "sec 3.2, eq (3.7)",
        "verdict": "STRICTLY WORSE THAN X, AND FOR a > 0 THE GAP IS DESTROYED -- each of the "
                   "eigenvalues 0 and 1 acquires an EVEN partner, and the translation mode "
                   "phi = Omega' is an exact eigenfunction at eigenvalue "
                   "c~ = (c_l + a)/(1 - a) > 0 for EVERY admissible profile. Oddness is "
                   "load-bearing SEPARATELY from the origin condition",
        "verdict_kind": "DERIVABLE_COROLLARY_DEAD",
        "quote": ("The third produces the even mode phi = Omega', which is an exact "
                  "eigenfunction of L_a for every admissible profile, at eigenvalue "
                  "c~ = c_l + a HOmega(0) = (c_l + a)/(1 - a) ... It reduces to c_l only at "
                  "a = 0, where one checks L0 Omega' = Omega' exactly, with "
                  "Omega' = (y^2 - 1/4)/(y^2 + 1/4)^2 even and O(y^{-2}), so it lies in "
                  "L^2(R) but not in X. Centering the collapse at the origin, which is what "
                  "the odd restriction does, removes this mode. At a = 0 the eigenvalue 0 "
                  "likewise has the even partner y^2/(y^2 + 1/4)^2. So on the full L^2(R) "
                  "the eigenvalues 0 and 1 each carry an even partner, while on the odd "
                  "realization X each eigenspace is one-dimensional."),
        "fragment": "so it lies in L2 (R) but not in X",
        "hypotheses": ("Exact at a = 0; for a > 0 it holds 'for every admissible profile' "
                       "i.e. under Adm(a). This is the gate's 'derivable corollary of a "
                       "stated general theorem' clause: Xu states the eigenpair in general "
                       "form, and the arithmetic below evaluates c~ along his own Table 1 "
                       "branch to show it is positive and GROWING, so the modulation that "
                       "works on X (two modes) does not suffice on full L^2(R) at a > 0."),
        "already_banked_by": None,
        "is_new_to_this_repo": True,
    },
    {
        "id": "S8-EGM-SINGULAR-WEIGHT",
        "space": "the Elgindi-Ghoul-Masmoudi singular-weighted space (phi = (1+y^2)^2/y^4, "
                 "with the origin constraints f odd, f'(0) = H f(0) = 0)",
        "definition": "arXiv:1906.05811 Prop. 2.1's space, as read BY XU in his sec 8 "
                      "parenthesis",
        "locator": "sec 8, the parenthesis after the coercivity no-go",
        "verdict": "ALIVE -- 'a gap is certified' there. Xu classifies it explicitly as "
                   "ANOTHER INSTANCE of his own realization mechanism, not as a "
                   "counterexample, and says it neither contradicts nor supplies the X-gap",
        "verdict_kind": "PROVED_ALIVE",
        "quote": ("(The small-a coercivity estimate of Elgindi, Ghoul, and Masmoudi [15, "
                  "Prop. 2.1], for odd f with f'(0) = Hf(0) = 0 in a singular-weighted "
                  "space, is not a counterexample but an instance of the realization "
                  "mechanism of Section 3.1: the singular weight and origin constraints "
                  "define their own realization, in which a gap is certified; it neither "
                  "contradicts nor supplies the X-gap here.)"),
        "fragment": "define their own realization, in which a gap is certified",
        "hypotheses": "EGM's own: a small, f odd, f'(0) = H f(0) = 0, int |f|^2 phi < inf; "
                      "and two modulation parameters (their sec 3).",
        "already_banked_by": ("leg 141 (Route-WEL) -- writeup/novelty/leg_141.md and "
                              "experiments/p2_route_wel_v1_lit.py. CITED, NOT CLAIMED."),
        "is_new_to_this_repo": False,
    },
    {
        "id": "S9-EVANS-WEIGHTED",
        "space": "the (unnamed) weighted space of the Evans-determinant strand, chosen so "
                 "that the essential line is displaced left of the strip",
        "definition": "sec 3.2 -- a weight used as an INSTRUMENT, to make a winding count "
                      "well defined; no space-level theorem attaches to it",
        "locator": "sec 3.2 (the fourth piece of evidence); sec 7 ('Evans-determinant count')",
        "verdict": "NO VERDICT -- exploratory instrument only. Returns n_disc(a) = 0 for "
                   "a in [0, 0.65], but 'numerical evidence, not proof', diagnostics 'not "
                   "enforced as hard gates', 'run outputs are not retained'",
        "verdict_kind": "INSTRUMENT_NO_VERDICT",
        "quote": ("Splitting L_a against its far field and forming the associated "
                  "determinant on a weighted space in which the essential line is displaced "
                  "left of the strip, the number of eigenvalues inside the strip window "
                  "becomes an integer winding count n_disc(a) along a rectangular contour. "
                  "This strand is exploratory ..."),
        "fragment": "a weighted space in which the essential line is displaced left of the strip",
        "hypotheses": "three explicitly recorded gaps -- see `technique_maturity` below",
        "already_banked_by": None,
        "is_new_to_this_repo": True,
    },
]


# ---------------------------------------------------------------------------
# 2. NEGATIVE LOCATORS -- lesson 90.  These MUST NOT be found.  If any reports LOCATED,
#    this leg's reading is wrong and the runner says so instead of confirming itself.
#    Declared in writeup/novelty/leg_171.md sec 3 before this file was written.
# ---------------------------------------------------------------------------
NEGATIVE_LOCATORS = [
    {"id": "N1-ELL1-W", "fragment": "weighted ell^1",
     "why": "Xu never works in a weighted SEQUENCE space; `ell^1_w` is THIS repository's "
            "space (legs 51-54, 58, 127), not his. If this ever hits, the gate's second "
            "excluded space would have to be re-read."},
    {"id": "N2-SEQUENCE-SPACE", "fragment": "sequence space",
     "why": "same, in the phrasing a radii-polynomial paper would use."},
    {"id": "N3-H3-PROVED", "fragment": "we prove that the third-derivative realization",
     "why": "the H^3 realization is EXPECTED, not proved. If this hits, S4's verdict_kind "
            "must be upgraded from EXPECTED_NOT_PROVED."},
    {"id": "N4-EXACTNESS-SETTLED", "fragment": "the exactness question is settled",
     "why": "the a > 0 exactness question is OPEN (sec 4.5, sec 8). If this hits, the a > 0 "
            "hypotheses recorded above are wrong."},
    {"id": "N5-EVANS-IS-PROOF", "fragment": "the Evans-determinant count is a proof",
     "why": "sec 3.2/sec 7 say the opposite ('numerical evidence, not proof'). If this hits, "
            "the technique-maturity reading below is wrong."},
]


# ---------------------------------------------------------------------------
# 3. XU'S OWN TABLE 1 (sec 2), transcribed.  `c_l` is the only INPUT; the far-field column
#    and s* column are Xu's PRINTED values, kept here as targets to reproduce, not as inputs.
# ---------------------------------------------------------------------------
TABLE1 = [
    # a,     c_l printed, far-field 1 - c_l/2 printed, s* printed
    (0.00, 1.0000, 0.500, 1.000),
    (0.10, 0.8730, 0.564, 1.145),
    (0.20, 0.7474, 0.626, 1.338),
    (0.30, 0.6178, 0.691, 1.619),
    (0.40, 0.4809, 0.760, 2.079),
    (0.50, 0.3333, 0.833, 3.000),
    (0.60, 0.1691, 0.915, 5.914),
    (0.65, 0.0775, 0.961, 12.90),
]

# Xu's own printed anchors that the reconstruction must hit (Figure 2 caption; sec 2).
XU_PRINTED = {
    "lines_coincide_at_a_0": 0.0,
    "lines_coincide_exactly_at_a_half": 0.5,
    "c_l_at_a_half_exact": 1.0 / 3.0,
    "max_protrusion_g_abs": 0.0362,
    "max_protrusion_at_a": 0.264,
    "protrusion_upper_bound_on_branch": 0.037,
    "both_lines_strictly_left_of": -0.5,
    "essential_gap_at_a_0": 0.5,
    "maximal_L2_strip": [-0.5, 1.5],
    "logmellin_rightmost_mode_at_a_half": 2.4931,
    "plain_L2_origin_indicial_line": 2.5,
}


def h_omega_0(a, c_l):
    """HOmega(0) = (1 + c_l)/(1 - a)   -- Proposition 1, sec 3.1."""
    return (1.0 + c_l) / (1.0 - a)


def c_tilde(a, c_l):
    """c~ = c_l + a HOmega(0) = (c_l + a)/(1 - a)   -- Prop. 1 and eq (3.7)."""
    return c_l + a * h_omega_0(a, c_l)


def far_field_line(c_l):
    """Re = -1 + c_l/2   -- Prop. 1 eq (3.4), Lemma 4.3 eq (4.11)."""
    return -1.0 + c_l / 2.0


def origin_line(a, c_l):
    """Re = lambda_X = -c~/2   -- Prop. 1 eq (3.4)."""
    return -c_tilde(a, c_l) / 2.0


def g_of_a(a, c_l):
    """g(a) = 2 c_l - HOmega(0) (1 - 3a/2)   -- Prop. 1.  The protrusion is -g(a)."""
    return 2.0 * c_l - h_omega_0(a, c_l) * (1.0 - 1.5 * a)


def reconstruct_branch():
    """Feed ONLY Xu's c_l column through Xu's closed forms and check four printed facts.

    This is the control that can report the other answer: a wrong reading of c~, of
    HOmega(0), or of which line is which fails all four checks at once.
    """
    rows = []
    for a, c_l, ff_printed, s_printed in TABLE1:
        ff = far_field_line(c_l)
        ol = origin_line(a, c_l)
        rows.append({
            "a": a,
            "c_l_xu_table1": c_l,
            "far_field_line_Re": ff,
            "far_field_distance_recomputed": -ff,
            "far_field_distance_xu_printed": ff_printed,
            "far_field_abs_diff": abs(-ff - ff_printed),
            "s_star_recomputed": 1.0 / c_l if c_l else None,
            "s_star_xu_printed": s_printed,
            "s_star_rel_diff": (abs(1.0 / c_l - s_printed) / s_printed) if c_l else None,
            "h_omega_0": h_omega_0(a, c_l),
            "c_tilde": c_tilde(a, c_l),
            "origin_line_Re": ol,
            "separation_origin_minus_far_field": ol - ff,
            "g_of_a": g_of_a(a, c_l),
            "both_lines_left_of_minus_half": bool(ff < -0.5 and ol < -0.5) if a > 0 else None,
        })
    return rows


def reconstruct_checks(rows):
    """The four printed facts, each as a pass/fail with the magnitude (never a bare boolean)."""
    by_a = {r["a"]: r for r in rows}

    # (i) Table 1's own two derived columns, reproduced from c_l alone.
    ff_worst = max(r["far_field_abs_diff"] for r in rows)
    s_worst = max(r["s_star_rel_diff"] for r in rows if r["s_star_rel_diff"] is not None)

    # (ii) the two lines coincide at a = 0 and EXACTLY at a = 1/2.
    sep0 = by_a[0.00]["separation_origin_minus_far_field"]
    # at a = 1/2 use the EXACT c_l = 1/3, which Xu states is exact ([20]; [4, Thm. 2]);
    # the tabulated 0.3333 is the grid value, so both are reported.
    sep_half_exact = (origin_line(0.5, 1.0 / 3.0) - far_field_line(1.0 / 3.0))
    sep_half_grid = by_a[0.50]["separation_origin_minus_far_field"]

    # (iii) maximum protrusion ~0.036 at a ~ 0.264, by scanning a fine interpolation of the
    #       branch.  c_l is interpolated linearly between Xu's tabulated points -- a coarse
    #       instrument, so the tolerance is stated, not hidden.
    scan = []
    for i in range(len(TABLE1) - 1):
        a0, c0 = TABLE1[i][0], TABLE1[i][1]
        a1, c1 = TABLE1[i + 1][0], TABLE1[i + 1][1]
        n = 200
        for k in range(n):
            t = k / n
            a = a0 + t * (a1 - a0)
            if a > 0.5:
                continue
            c_l = c0 + t * (c1 - c0)
            scan.append((a, origin_line(a, c_l) - far_field_line(c_l)))
    a_max, sep_max = max(scan, key=lambda p: p[1])

    # (iv) both lines strictly left of Re = -1/2 for every a > 0 on the branch.
    left = [r for r in rows if r["a"] > 0]
    worst_ff = max(r["far_field_line_Re"] for r in left)
    worst_ol = max(r["origin_line_Re"] for r in left)

    return {
        "note": ("Every number below is arithmetic on XU's own Table 1 and XU's own closed "
                 "forms. Nothing of this repository's is measured. The point is falsifiability "
                 "of the READING, not new mathematics."),
        "i_table1_columns_reproduced_from_c_l_alone": {
            "far_field_distance_worst_abs_diff": ff_worst,
            "far_field_tolerance": 0.001,
            "far_field_pass": bool(ff_worst <= 0.001),
            "s_star_worst_rel_diff": s_worst,
            "s_star_tolerance": 5e-4,
            "s_star_pass": bool(s_worst <= 5e-4),
            "reading": ("Xu's printed far-field column IS 1 - c_l/2 and his s* column IS "
                        "1/c_l, so the closed forms are read correctly."),
        },
        "ii_two_lines_coincide_at_a_0_and_at_a_half": {
            "separation_at_a_0": sep0,
            "separation_at_a_half_using_exact_c_l_one_third": sep_half_exact,
            "separation_at_a_half_using_table_grid_c_l": sep_half_grid,
            "pass": bool(abs(sep0) < 1e-12 and abs(sep_half_exact) < 1e-12),
            "reading": ("Xu: 'the two lines coincide at a = 0 and, exactly, at a = 1/2 ... "
                        "g(1/2) = (3 c_l - 1)/2 = 0'. Reproduced to machine zero from the "
                        "closed forms at the EXACT c_l = 1/3; the grid value 0.3333 leaves "
                        "the residue below, which is the grid tolerance, not a discrepancy."),
        },
        "iii_max_protrusion": {
            "a_at_max_recomputed": a_max,
            "a_at_max_xu_printed": XU_PRINTED["max_protrusion_at_a"],
            "max_separation_recomputed": sep_max,
            "max_protrusion_xu_printed_abs": XU_PRINTED["max_protrusion_g_abs"],
            "xu_stated_upper_bound_on_branch": XU_PRINTED["protrusion_upper_bound_on_branch"],
            "abs_diff_in_magnitude": abs(sep_max - XU_PRINTED["max_protrusion_g_abs"]),
            "within_xu_stated_upper_bound": bool(sep_max <= XU_PRINTED["protrusion_upper_bound_on_branch"]),
            "interpolation": "piecewise-linear in c_l between Xu's tabulated a values",
            "note_on_within_xu_stated_upper_bound_being_False": (
                "It exceeds Xu's stated 0.037 by 4.5e-05, and that is an artifact of THIS "
                "reconstruction's coarser instrument, not a disagreement with Xu. Xu "
                "interpolates a Delta a = 0.04 Newton branch by degree-6 polynomial; this "
                "check interpolates LINEARLY between his printed Delta a = 0.1 table rows, "
                "which is convex-side and overshoots. Reported rather than tuned away: the "
                "magnitude of the overshoot (4.5e-05) is two orders below the quantity "
                "being checked (0.037) and three below Xu's own two-grid self-consistency "
                "measure (5e-04). The `pass` flag is set on the location and the magnitude, "
                "which is what the reading rests on."),
            "pass": bool(abs(a_max - XU_PRINTED["max_protrusion_at_a"]) < 0.05
                         and abs(sep_max - XU_PRINTED["max_protrusion_g_abs"]) < 0.002),
            "reading": ("Xu's Figure 2 caption: 'the origin line lies at most 0.037 right of "
                        "the far-field line on (0, 1/2) (minimum -0.0362 at a ~ 0.264)'. "
                        "Recovered independently from c_l alone, on a linear interpolation "
                        "-- a coarse instrument that nonetheless lands on both the location "
                        "and the magnitude."),
        },
        "iv_both_lines_strictly_left_of_minus_half_for_a_gt_0": {
            "rightmost_far_field_line": worst_ff,
            "rightmost_origin_line": worst_ol,
            "threshold": XU_PRINTED["both_lines_strictly_left_of"],
            "margin_far_field": XU_PRINTED["both_lines_strictly_left_of"] - worst_ff,
            "margin_origin": XU_PRINTED["both_lines_strictly_left_of"] - worst_ol,
            "pass": bool(worst_ff < -0.5 and worst_ol < -0.5),
            "reading": "Xu: 'Both lines stay strictly left of Re = -1/2 for a > 0.'",
        },
    }


def y_theta_identities():
    """Appendix A's two consistency identities -- what pins Xu's exact decay rate to
    Theorem 1's essential edge, and what makes Y_{3/2} the ONE space where the a = 0 origin
    line stops being pathological."""
    theta = 1.5
    return {
        "note": ("These are the arithmetic joints of Appendix A. They are what makes the "
                 "Y_theta family a statement about THIS operator's certificate-buildability "
                 "rather than a generic weighted-dilation fact."),
        "spectrum_line_of_A_theta": "Re = 1 - theta   (eq (A.19) discussion)",
        "semigroup_norm": "||e^{A tau}||_{Y_theta} = e^{(1 - theta) tau}, constant 1 (Prop. A.3)",
        "theta_that_matches_theorem_1_edge": {
            "theorem_1_essential_edge": -0.5,
            "solve_1_minus_theta_eq_minus_half": 1.0 - theta,
            "theta": theta,
            "match": bool(abs((1.0 - theta) - (-0.5)) < 1e-15),
            "xu_printed": "||e^{A tau}||_{Y_{3/2}} = e^{-tau/2}   (eq (A.20))",
        },
        "core_weight_at_that_theta": {
            "weight_exponent_formula": "y^{-2 theta - 1}",
            "exponent_at_theta_3_2": -(2.0 * theta + 1.0),
            "xu_printed": "core weight y^{-4}",
            "match": bool(abs(-(2.0 * theta + 1.0) - (-4.0)) < 1e-15),
        },
        "what_the_weight_does_to_the_plain_L2_origin_line": {
            "plain_L2_origin_indicial_line": XU_PRINTED["plain_L2_origin_indicial_line"] - 1.0,
            "note_on_the_number": ("Xu writes the plain-L^2 origin line as the pathological "
                                   "Re = +3/2, which is the right edge of the maximal-L^2 "
                                   "strip [-1/2, 3/2] of Prop. 2; the log-Mellin grid at "
                                   "a = 0.5 renders its own rightmost mode at +2.4931 "
                                   "against the a = 0.5 indicial line +5/2 (sec 7), a "
                                   "different a and a different number -- the two must not "
                                   "be conflated."),
            "pushed_to": -0.5,
            "xu_printed": ("the origin line, which in plain L^2 sits at the pathological "
                           "Re = +3/2 ..., is pushed to -1/2 by the y^{-4} core weight"),
            "consequence": ("Y_{3/2} is the ONE member of the family in which BOTH essential "
                            "lines of L0 sit at the same place as Theorem 1's edge, which is "
                            "why the exact rate e^{-tau/2} is the essential rate and not an "
                            "artifact of the weight."),
        },
        "theta_is_pinned_for_physical_data": {
            "tail_forces": "theta >= 3/2",
            "core_forces": "theta <= 3/2 (the double Hardy inequality is sharp there)",
            "window_width_for_physical_X_data": 0.0,
            "window_for_origin_analytic_forcing": [1.0, 2.0],
            "window_width_for_origin_analytic_forcing": 1.0,
            "reading": ("A ZERO-WIDTH window for physical X-data. This repository has seen "
                        "that shape before (leg 111's weighted-energy window, re-read by "
                        "leg 141) and the lesson there was that a zero-width window can be "
                        "an artifact of the trial space. Here it is NOT: Xu derives it from "
                        "a two-sided squeeze and states the widened window that origin-"
                        "analytic data buys. Recorded as a caution for any leg that would "
                        "try to move theta."),
        },
    }


def even_sector_corollary():
    """The gate's 'derivable corollary of a stated general theorem' clause, made numerical.

    Xu states (sec 3.2 eq (3.7)) that the translation mode Omega' is an exact eigenfunction
    of L_a at c~ = (c_l + a)/(1 - a) for EVERY admissible profile, and that it lies in
    L^2(R) but not in X.  Evaluating c~ along Xu's own Table 1 branch turns that stated
    general fact into a verdict about the full-L^2(R) realization at every sampled a.
    """
    rows = []
    for a, c_l, _, _ in TABLE1:
        ct = c_tilde(a, c_l)
        rows.append({
            "a": a, "c_l": c_l, "c_tilde_eigenvalue_of_Omega_prime": ct,
            "is_unstable_direction": bool(ct > 0.0),
            "origin_line_is_minus_half_c_tilde": -ct / 2.0,
        })
    return {
        "statement_source": "Xu sec 3.2 eq (3.7), stated for every admissible profile",
        "rows": rows,
        "min_c_tilde_over_branch": min(r["c_tilde_eigenvalue_of_Omega_prime"] for r in rows),
        "max_c_tilde_over_branch": max(r["c_tilde_eigenvalue_of_Omega_prime"] for r in rows),
        "all_positive": bool(all(r["is_unstable_direction"] for r in rows)),
        "monotone_increasing": bool(all(
            rows[i + 1]["c_tilde_eigenvalue_of_Omega_prime"]
            > rows[i]["c_tilde_eigenvalue_of_Omega_prime"] for i in range(len(rows) - 1))),
        "reading": ("On the full L^2(R) realization the translation mode is an eigenvalue at "
                    "c~ > 0 at EVERY sampled advection, growing from 1.000 at a = 0 to 2.079 "
                    "at a = 0.65, and the eigenvalues 0 and 1 each acquire an even partner "
                    "besides. So the two-mode modulation that produces X's gap 1/2 does NOT "
                    "suffice once oddness is dropped. Oddness is load-bearing SEPARATELY "
                    "from the origin condition -- a second axis of realization-dependence, "
                    "and one this repository had not recorded."),
        "control_that_can_report_otherwise": (
            "At a = 0 the formula must return exactly 1, because Xu states 'one checks "
            "L0 Omega' = Omega' exactly'. It does (c~ = 1.000000). Had the formula been "
            "misread, this anchor would have missed."),
        "anchor_at_a_0": c_tilde(0.0, 1.0),
    }


# ---------------------------------------------------------------------------
# 4. the certification TECHNIQUE, and how mature it is -- the prompt's second ask
# ---------------------------------------------------------------------------
TECHNIQUE_MATURITY = {
    "question": ("Beyond the strict gate: what IS Xu's certification technique, and how "
                 "mature/scalable is it as a lane distinct from ell^1-Fourier?"),
    "layer_1_the_proved_layer_is_not_computer_assisted_at_all": {
        "what": ("Theorems 1-3 are Mellin diagonalization + log-widening singular Weyl "
                 "sequences + an EXPLICIT closed-form resolvent kernel (sec 4.4 eq (4.23)) "
                 "with an exact Hardy-Mellin operator norm (Lemma 4.5) and an assembled "
                 "analytic majorant M_an ~ alpha^{-3/2}."),
        "machine_involvement": ("a twelve-check verification suite -- six exact in sympy (the "
                                "two scalar ODEs for symbolic lambda, the sin(pi(1-lambda)) "
                                "non-degeneracy determinant, the profile identities, the "
                                "origin Taylor coefficients, the two integer modes) and six "
                                "numerical. It confirms identities; it is not a certificate."),
        "consequence": ("'Xu's certification method' is, at the proved layer, ANALYSIS with "
                        "symbolic checking -- not a computer-assisted proof pipeline. Anyone "
                        "porting it is porting a closed-form resolvent, not a solver."),
    },
    "layer_2_the_certification_shaped_strand_is_explicitly_incomplete": {
        "what": ("the Evans-determinant / argument-principle continuation of sec 3.2 and "
                 "sec 7: an integer winding count n_disc(a) on a rectangular contour, in a "
                 "weighted space that displaces the essential line left of the strip."),
        "result": "n_disc(a) = 0 for all computed a in [0, 0.65]",
        "three_gaps_verbatim": ("a uniform large-imaginary-part bound, trace-ideal membership "
                                "of the kernel, and quadrature-error bounds in the trace norm"),
        "xu_on_their_status": ("'which the code computes as diagnostics rather than enforcing "
                               "as interval bounds' ... 'its run outputs are not retained' ... "
                               "'Upgrading any of these would move this strand toward a "
                               "computer-assisted proof.'"),
        "consequence": ("All three items the prompt asked to watch for -- uniform large-"
                        "imaginary-part bounds, trace-ideal membership, quadrature error in "
                        "the trace norm -- are OPEN, by the author's own statement. The "
                        "strand is not a CAP today and Xu does not claim it is."),
    },
    "layer_3_the_architecture_it_must_imitate": {
        "what": ("Hou-Wang-Yang's viscous 3D Navier-Stokes NONUNIQUENESS proof (not a "
                 "singularity result): split the linearization into a coercive part and a "
                 "compact perturbation, approximate the compact part by a finite-rank "
                 "operator to controlled error, and certify invertibility by computer only "
                 "on the finite-rank image."),
        "xu_verbatim": ("'the computer-assisted step certifies invertibility only on a "
                        "finite-rank image, after the continuous spectrum has been carried "
                        "by a coercive part and the remainder rendered compact; our "
                        "spectrally correct essential-line rendering feeding an argument-"
                        "principle count is the same requirement in the gCLM-collapse "
                        "setting.'"),
        "obstruction_named_by_xu": ("for the COLLAPSE linearization the nonlocal term is "
                                    "genuinely non-compact -- 'the Hilbert term Omega H phi "
                                    "is not relatively compact (a coefficient vanishing at "
                                    "both endpoints times an order-zero singular integral is "
                                    "not compact)' -- which is why the closed-form theorems "
                                    "are proved by Mellin diagonalization instead."),
    },
    "two_no_gos_xu_states_in_sec_8": [
        {
            "id": "NOGO-COERCIVITY",
            "quote": ("A weighted-energy/coercivity estimate cannot certify the gap: the far "
                      "field is already coercive in plain L^2 with the sharp edge, but a "
                      "local positive multiplier +phi HOmega near the origin (with "
                      "HOmega(0) > 0) survives every L^2-equivalent weight, so no coercivity "
                      "certificate in an L^2-equivalent norm reaches the spectral gap."),
            "fragment": "no coercivity certificate in an L2 -equivalent norm reaches the spectral gap",
            "already_banked_by": "leg 141 (Route-WEL). CITED, NOT CLAIMED.",
        },
        {
            "id": "NOGO-INTERVAL-ARITHMETIC",
            "quote": ("Likewise a naive interval-arithmetic resolvent enclosure is "
                      "unavailable: a weight is a change of norm, eigenvalues are "
                      "norm-invariant, and the truncated L_a genuinely carries essential-"
                      "smear eigenvalues inside the strip (the compactified grid mis-renders "
                      "the continuous line at the wrong real part), so no weighted enclosure "
                      "can exclude them. The consequence is that the rigorous discrete "
                      "exclusion must be analytical (the a = 0 anchor plus continuation) "
                      "rather than a black-box computer-assisted enclosure; where a computer-"
                      "assisted proof does enter, it must first be given a spectrally correct "
                      "rendering of the essential spectrum (a non-periodic log-Mellin "
                      "operator at high resolution feeding an argument-principle count), not "
                      "applied to the raw grid."),
            "fragment": "a naive interval-arithmetic resolvent enclosure is unavailable",
            "already_banked_by": None,
            "why_it_matters_here": ("NOT banked anywhere in this repository -- leg 141 banked "
                                    "only the coercivity half. This is the maturity answer: "
                                    "Xu's own paper says the naive interval-arithmetic route "
                                    "into his object does not work, and names the "
                                    "prerequisite (a spectrally correct essential-line "
                                    "rendering) before any CAP may enter. Treating 'Xu's "
                                    "certification method' as a mature lane ready to be "
                                    "ported is treating a PROGRAM as a METHOD."),
        },
    ],
    "instrument_honesty_recorded_by_xu": (
        "sec 7: the log-Mellin grid's rightmost mode at a = 0.5 sits at Re = +2.4931 against "
        "the plain-L^2 indicial line +5/2 -- it CORROBORATES Proposition 2 rather than "
        "certifying the far-field edge. A discretization without an origin condition computes "
        "a different operator, faithfully."),
    "scalability_reading": (
        "The closed-form layer does NOT scale off a = 0: the Hardy collapse rests on the "
        "single-simple-pole identity HOmega - i Omega = i/(y + i/2), which Xu says is 'exact "
        "only at the single-pole a = 0 profile'. At a > 0 everything discrete is numerical "
        "evidence at sampled advections, and the essential spectrum is an INCLUSION under "
        "Adm(a), not an equality. So the mature part of the method is a one-point analytic "
        "anchor, and the scalable part is the part that is not yet built."),
}


# ---------------------------------------------------------------------------
# 5. verbatim presence
# ---------------------------------------------------------------------------
def _squash(s):
    """Whitespace-insensitive comparison key.  pdftotext breaks lines mid-sentence and pads
    with -layout columns, so a raw substring test fails on true quotes."""
    return "".join(s.split())


def pdf_text(arxiv_id):
    p = PAPERS / f"{arxiv_id}.pdf"
    if not p.exists():
        return None
    try:
        out = subprocess.run(["pdftotext", "-layout", str(p), "-"],
                             capture_output=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.decode("utf-8", errors="replace")


def relocate(prior):
    """Positive fragments must be LOCATED; negative fragments must NOT be.  When the PDF is
    absent the flags are read back from the committed JSON and labelled -- never defaulted."""
    text = pdf_text(ARXIV)
    hay = _squash(text) if text is not None else None

    prior_pos = {r["id"]: r for r in (prior or {}).get("spaces", [])}
    prior_neg = {r["id"]: r for r in (prior or {}).get("negative_locators", [])}

    pos = []
    for s in SPACES:
        rec = dict(s)
        if hay is None:
            rec["fragment_located"] = prior_pos.get(s["id"], {}).get("fragment_located")
            rec["fragment_source"] = "read back from committed JSON (PDF absent)"
        else:
            rec["fragment_located"] = _squash(s["fragment"]) in hay
            rec["fragment_source"] = f"recomputed from Papers/{ARXIV}.pdf"
        pos.append(rec)

    neg = []
    for n in NEGATIVE_LOCATORS:
        rec = dict(n)
        if hay is None:
            rec["fragment_located"] = prior_neg.get(n["id"], {}).get("fragment_located")
            rec["fragment_source"] = "read back from committed JSON (PDF absent)"
        else:
            rec["fragment_located"] = _squash(n["fragment"]) in hay
            rec["fragment_source"] = f"recomputed from Papers/{ARXIV}.pdf"
        neg.append(rec)

    # the two sec-8 no-go quotes carry fragments too
    nogo = []
    for g in TECHNIQUE_MATURITY["two_no_gos_xu_states_in_sec_8"]:
        rec = dict(g)
        if hay is None:
            rec["fragment_located"] = None
            rec["fragment_source"] = "read back unavailable (PDF absent)"
        else:
            rec["fragment_located"] = _squash(g["fragment"]) in hay
            rec["fragment_source"] = f"recomputed from Papers/{ARXIV}.pdf"
        nogo.append(rec)

    src = (f"recomputed from Papers/{ARXIV}.pdf" if hay is not None
           else "PDF absent -- flags read back from the committed JSON")
    return pos, neg, nogo, src


# ---------------------------------------------------------------------------
def build():
    prior = json.loads(OUT.read_text()) if OUT.exists() else None
    spaces, negs, nogos, src = relocate(prior)
    rows = reconstruct_branch()
    checks = reconstruct_checks(rows)

    other_spaces = [s for s in spaces if s["id"] not in ("S0-ORIGIN-H2", "S1-MAP")]
    new_here = [s["id"] for s in other_spaces if s["is_new_to_this_repo"]]
    already = [s["id"] for s in other_spaces if not s["is_new_to_this_repo"]]

    return {
        "leg": 171,
        "route": "XUL",
        "kind": "literature (deep-mine of an already-accessed paper)",
        "paper": {
            "arxiv": ARXIV,
            "url": f"https://arxiv.org/abs/{ARXIV}",
            "cite": ("Jie Xu (Univ. of Illinois Chicago), The spectral picture of self-similar "
                     "collapse in the Constantin-Lax-Majda equation, arXiv:2607.19762v1, "
                     "22 Jul 2026, physics.flu-dyn, 41 pp."),
            "same_object_as_ours": ("sec 2 eq (2.3): Omega(y) = -y/(y^2 + 1/4), "
                                    "HOmega = (1/2)/(y^2 + 1/4), c_l = 1 -- this "
                                    "repository's `clm_one_scale` normalisation."),
        },
        "gate": GATE,
        "gate_answer": GATE_ANSWER,
        "gate_answer_branch_verbatim": GATE_YES_BRANCH_VERBATIM,
        "headline": (
            "Xu does not speak to one space. He writes an explicit 'Map of realizations' "
            "(sec 3.1) naming three, and the full text carries EIGHT distinct spaces for the "
            "SAME operator with FIVE distinct verdicts: origin-H^2 alive-proved; maximal L^2 "
            "dead-proved (no L^2 gap at all); merely-C^1 dead-proved (one derivative too few "
            "and the strip fills with a continuum); H^3 expected-alive but explicitly not "
            "pursued; the weighted conjugated family Y_theta alive and EXACT for every theta "
            "(normal generator, spectrum the single line Re = 1 - theta, semigroup norm "
            "e^{(1-theta) tau} with constant 1), pinned to theta = 3/2 for physical data; the "
            "Hardy block X_+ alive-proved and the place the explicit inverse actually lives; "
            "full L^2(R) with the even sector dead by a derivable corollary (an extra "
            "eigenvalue c~ = (c_l+a)/(1-a) > 0 at every sampled a); and EGM's singular-"
            "weighted space alive, which Xu classifies as another instance of the same "
            "mechanism."),
        "spaces": spaces,
        "negative_locators": negs,
        "located_source": src,
        "space_accounting": {
            "spaces_other_than_origin_H2_characterized": len(other_spaces),
            "new_to_this_repository": new_here,
            "already_banked_cited_not_claimed": already,
            "ell_1_w_in_xu": ("ABSENT. `ell^1_w` is THIS repository's space (legs 51-54, 58, "
                              "127); Xu never mentions a weighted sequence space, which the "
                              "negative locators N1/N2 check. So the gate's exclusion list "
                              "reduces, on Xu's side, to origin-H^2 alone."),
        },
        "branch_reconstruction": {
            "purpose": ("the falsifiable core: feed ONLY Xu's Table 1 c_l column through Xu's "
                        "own closed forms and reproduce four independently printed facts. A "
                        "wrong reading of c~, of HOmega(0), or of which line is which fails "
                        "all four at once."),
            "closed_forms": {
                "far_field_line": "Re = -1 + c_l/2   (Prop. 1 eq (3.4); Lemma 4.3 eq (4.11))",
                "origin_line": "Re = lambda_X = -c~/2   (Prop. 1 eq (3.4))",
                "c_tilde": "c~ = c_l + a HOmega(0) = (c_l + a)/(1 - a)",
                "h_omega_0": "HOmega(0) = (1 + c_l)/(1 - a)",
                "g_of_a": "g(a) = 2 c_l - HOmega(0)(1 - 3a/2); the protrusion is -g(a)",
                "s_star": "s*(a) = 1/c_l(a)   (sec 6)",
            },
            "rows": rows,
            "checks": checks,
            "all_four_pass": bool(
                checks["i_table1_columns_reproduced_from_c_l_alone"]["far_field_pass"]
                and checks["i_table1_columns_reproduced_from_c_l_alone"]["s_star_pass"]
                and checks["ii_two_lines_coincide_at_a_0_and_at_a_half"]["pass"]
                and checks["iii_max_protrusion"]["pass"]
                and checks["iv_both_lines_strictly_left_of_minus_half_for_a_gt_0"]["pass"]),
        },
        "y_theta_identities": y_theta_identities(),
        "even_sector_corollary": even_sector_corollary(),
        "technique_maturity": TECHNIQUE_MATURITY,
        "what_this_informs": {
            "leg_163_scoping": (
                "163 asks whether origin-H^2 admits a structurally viable CERTIFICATE "
                "formulation, and its thesis says to re-read Xu 'for what it says about the "
                "gap's own limitations'. Four things here bear on it, and none was in 163's "
                "brief: (1) X's gap is NOT uniform in a -- for a in (0, 1/2) X acquires a "
                "SECOND (origin) essential line that protrudes into the strip by up to 0.037, "
                "a defect of the H^2 realization itself which Xu says an H^3 realization is "
                "EXPECTED to remove; (2) the explicit inverse is built on the Hardy block "
                "X_+, not on X directly, via a scalar reduction that is 'exact only at the "
                "single-pole a = 0 profile'; (3) Xu's sec 8 states that a naive interval-"
                "arithmetic resolvent enclosure is unavailable for this object and names the "
                "prerequisite; (4) the certificate-shaped exactness lives on Y_{3/2}, not on "
                "X, and the transfer between them costs the constant (C_Q, not 1)."),
            "leg_165_synthesis": (
                "165 asks whether this repository's banked 'dead' findings are realization-"
                "dependent. Xu supplies a published, theorem-grade instance of exactly that "
                "phenomenon on THIS operator, at eight points rather than two, INCLUDING a "
                "second axis 165's four cases do not cover: the ODD/EVEN sector restriction "
                "is load-bearing independently of the origin condition (sec 3.2's c~ mode). "
                "That is a template for 165's classification, not an answer to it."),
            "user_interest_xu_lane_vs_ell1_fourier": (
                "The honest reading is that Xu's lane is NOT yet a method to port. Its proved "
                "layer is closed-form analysis at a single advection; its CAP-shaped layer "
                "has three open gaps its own author names; and its author states that the "
                "black-box interval-arithmetic entrance is closed for this object. What IS "
                "mature and transferable is the DIAGNOSIS -- name the realization before "
                "reading any spectrum, because the same operator is alive on some spaces and "
                "dead on others."),
        },
        "what_is_NOT_claimed": (
            "No ban is lifted, no route promoted, nothing is built or tested (the gate's "
            "yes-branch forbids it). Everything above is at a = 0, or at a > 0 conditional on "
            "Adm(a) and on open exactness questions, on the CLM linearization -- this "
            "repository's friendliest substrate, whose blow-up is explicit -- and NOT on "
            "HL_S2_nonsymmetric. L1 stays measured-dead in all three realizations. No link of "
            "the L1 -> L4 chain moves. The ~0.05% Clay assessment is untouched. New to the "
            "world: nothing; this is a reading of one published paper."),
        "novelty_log": "writeup/novelty/leg_171.md",
        "journal": "experiments/journal/leg_171.md",
        "figure": "none -- no measurement of a curve of this repository's own "
                  "('no measurement, no figure')",
    }


def main():
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")

    print("P2 Route-XUL v1 -- leg 171: does Xu arXiv:2607.19762 characterize any space")
    print("                            OTHER than origin-H^2 / ell^1_w?")
    print()
    print("GATE:", GATE)
    print("ANSWER:", data["gate_answer"])
    print()
    print("the spaces  (" + data["located_source"] + "):")
    for s in data["spaces"]:
        flag = {True: "LOCATED", False: "NOT FOUND", None: "unknown"}[s["fragment_located"]]
        new = "NEW here" if s["is_new_to_this_repo"] else "banked"
        print(f"  {s['id']:<24} {s['verdict_kind']:<26} {flag:<9} {new}")
    print()
    print("negative locators (these MUST NOT be found -- lesson 90):")
    for n in data["negative_locators"]:
        flag = {True: "*** LOCATED -- READING IS WRONG ***", False: "absent (good)",
                None: "unknown"}[n["fragment_located"]]
        print(f"  {n['id']:<22} {flag}")
    print()
    print("sec 8 no-gos:")
    for g in data["technique_maturity"]["two_no_gos_xu_states_in_sec_8"]:
        print(f"  {g['id']:<28} banked by: {g['already_banked_by'] or 'NOBODY -- new here'}")
    print()
    br = data["branch_reconstruction"]
    print("branch reconstruction from Xu's Table 1 c_l alone (the falsifiable core):")
    print(f"  {'a':>5} {'c_l':>8} {'far-field Re':>13} {'origin Re':>11} "
          f"{'sep':>9} {'c~':>8} {'s*':>8}")
    for r in br["rows"]:
        print(f"  {r['a']:>5.2f} {r['c_l_xu_table1']:>8.4f} {r['far_field_line_Re']:>13.4f} "
              f"{r['origin_line_Re']:>11.4f} {r['separation_origin_minus_far_field']:>9.4f} "
              f"{r['c_tilde']:>8.4f} {r['s_star_recomputed']:>8.3f}")
    print()
    c = br["checks"]
    print("  (i)   Table 1 columns from c_l alone: far-field worst abs diff "
          f"{c['i_table1_columns_reproduced_from_c_l_alone']['far_field_distance_worst_abs_diff']:.2e}"
          f"  (pass {c['i_table1_columns_reproduced_from_c_l_alone']['far_field_pass']}); "
          f"s* worst rel diff "
          f"{c['i_table1_columns_reproduced_from_c_l_alone']['s_star_worst_rel_diff']:.2e}"
          f"  (pass {c['i_table1_columns_reproduced_from_c_l_alone']['s_star_pass']})")
    ii = c["ii_two_lines_coincide_at_a_0_and_at_a_half"]
    print(f"  (ii)  lines coincide: sep(a=0) = {ii['separation_at_a_0']:.3e}, "
          f"sep(a=1/2, exact c_l=1/3) = "
          f"{ii['separation_at_a_half_using_exact_c_l_one_third']:.3e}  (pass {ii['pass']})")
    iii = c["iii_max_protrusion"]
    print(f"  (iii) max protrusion {iii['max_separation_recomputed']:.4f} at "
          f"a = {iii['a_at_max_recomputed']:.3f}   vs Xu's printed "
          f"{iii['max_protrusion_xu_printed_abs']:.4f} at "
          f"a = {iii['a_at_max_xu_printed']:.3f}  (pass {iii['pass']})")
    iv = c["iv_both_lines_strictly_left_of_minus_half_for_a_gt_0"]
    print(f"  (iv)  rightmost far-field {iv['rightmost_far_field_line']:.4f}, rightmost "
          f"origin {iv['rightmost_origin_line']:.4f}, both < -0.5  (pass {iv['pass']})")
    print(f"  ALL FOUR PASS: {br['all_four_pass']}")
    print()
    y = data["y_theta_identities"]
    print("Appendix A's Y_theta joints:")
    print(f"  1 - theta = -1/2  =>  theta = {y['theta_that_matches_theorem_1_edge']['theta']}"
          f"   (match {y['theta_that_matches_theorem_1_edge']['match']})")
    print(f"  core weight y^(-2theta-1) = y^"
          f"({y['core_weight_at_that_theta']['exponent_at_theta_3_2']:.0f})"
          f"   vs Xu's printed y^-4   (match {y['core_weight_at_that_theta']['match']})")
    print(f"  theta window for physical X-data: width "
          f"{y['theta_is_pinned_for_physical_data']['window_width_for_physical_X_data']:.0f} "
          f"(PINNED); for origin-analytic forcing: "
          f"{y['theta_is_pinned_for_physical_data']['window_for_origin_analytic_forcing']}")
    print()
    e = data["even_sector_corollary"]
    print("full-L^2(R) even-sector corollary -- c~ along Xu's branch:")
    print(f"  min {e['min_c_tilde_over_branch']:.4f}  max {e['max_c_tilde_over_branch']:.4f}  "
          f"all positive {e['all_positive']}  monotone {e['monotone_increasing']}  "
          f"anchor c~(a=0) = {e['anchor_at_a_0']:.6f} (must be exactly 1)")
    print()
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
