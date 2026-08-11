"""Route-CADX v1 (leg 304): DOES CADIOT arXiv:2505.03091's CONSTRUCTION COVER A ZERO DIAGONAL?

THE QUESTION IS NOT MINE.  It is the lift condition of a standing ban, verbatim from
`plan_of_record.py`:

    "re-claiming leg 51's methodological finding at full strength ...
     (lifted by: never -- unless a pass resolves whether Cadiot's construction covers a
      zero diagonal, which is now the live open question, not BDL's)"

Leg 57 located the dominance-hypothesis observation in Cadiot's full text and explicitly
did not answer this.  Leg 62 (Route-CP) read the same paper at full text but under a
DIFFERENT pre-committed gate -- leg 58's hypothesis, "an operator whose unbounded part is
OFF-DIAGONAL with a NON-DECAYING TAIL INVERSE".  Those two questions overlap in exactly one
located clause (`A1_LMIN`) and differ everywhere else.  This runner answers the ban's own
wording, from a second independent extraction of the same e-print, and re-derives every
number it reports rather than inheriting it.

NOTHING HERE LIFTS THE BAN.  The ban's lift condition routes through the user; a leg that
answers the named question does not thereby discharge it.  The gate's yes-(i) branch is
"bank at full strength -- the ban stands on measured, quoted footing", and that is the
branch this run lands on.

PRE-COMMITTED CLAUSES, both branches reportable:

  CADX0 THE NOVELTY PASS CAME FIRST.  `writeup/novelty/leg_304.md`, committed before any
        of this was built.  Verdict PROCEED_AS_CONFIRMATION_PLUS_NARROWING: this leg
        claims NO mathematical novelty of its own and says so in the JSON, so no writeup
        can overstate past it.

  CADX1 EVERY CLAUSE IS A LOCATED FULL-TEXT LINE, AND THE QUOTES ARE MACHINE-CHECKED.
        Section / assumption / lemma number, page, and the sentence verbatim -- never an
        abstract, never a restatement.  When the e-print is present (`Papers/` is
        gitignored) each quote is re-extracted from the PDF and matched; when it is
        absent that is reported as NOT_AVAILABLE rather than silently skipped.

  CADX2 THE DISTINCTION THE BAN TURNS ON IS STATED AND MEASURED: a zero EIGENVALUE and a
        zero DIAGONAL are different objects.  Cadiot's construction demonstrably covers
        the first -- it encloses the translation kernel nu_2 = 0 in section 5.2 -- and
        Assumption 1 excludes the second.  Conflating them is how this question could be
        answered wrongly in either direction.

  CADX3 ASSUMPTION 1's CONSTANT IS RE-DERIVED ON ALL FOUR OF THE PAPER'S OWN EXAMPLES,
        against what the author states, and reported as a magnitude with its
        reproduction error.  Reused from leg 62's `solver/certificate_shapes.py`, NOT
        rebuilt (the capabilities ban), and reported as CONFIRMED rather than as new.

  CADX4 THE DIAL FROM COVERED TO UNCOVERED IS THE PAPER'S OWN PARAMETER.  On the paper's
        leading example, Swift-Hohenberg, l_min equals mu exactly; at mu = 0 the symbol
        has a genuine zero on the circle |2 pi xi| = 1.  So the distance from Cadiot's
        two runs to a zero diagonal is measured in his own units: 0.28 and 0.32.

  CADX5 THE METHOD DIES AT A FINITE GAP, NOT AT ZERO.  Remark 5.2 reports an eigenvalue
        at 0.19 that could NOT be enclosed against an essential spectrum starting at 0.2.
        Reported as the two gaps -- 0.04 enclosed, 0.01 not -- because "excluded at
        exactly zero" would be a weaker and less honest statement than the paper's own.

  CADX6 THE GATE PREDICATE CAN ANSWER (ii) AND IS SHOWN DOING SO.  Lesson 90: the same
        code path is run on a synthetic scope with Assumption 1's lower bound removed,
        and on one with a hypothesis-relaxing forward citation, and both return "covers".
        The "does not cover" answer is therefore a property of the located clauses.

  CADX7 THE FORWARD CITATIONS ARE CHECKED FOR A RELAXATION.  Two 2025 citing papers,
        fetched at source and text-extracted; neither weakens the non-vanishing symbol
        hypothesis.  Leg 62's three are disjoint from these two, and that partiality is
        reported rather than hidden.

WHAT THIS RUNNER DOES NOT DO.  It does not rebuild leg 62's symbol code, ledger, or shift
ladders.  It touches no shared ledger.  It says nothing about `HL_S2_nonsymmetric` and
moves no link of the L1->L4 chain: Clay odds stay ~0.05%.  It is not a claim that Cadiot's
paper is deficient -- Assumption 1 is a hypothesis that paper states plainly on its first
page of setup and discharges on every one of its own examples.

Run: `.venv/bin/python experiments/p2_route_cadx_v1_scope.py`
"""

import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                        # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.certificate_shapes import (                                # noqa: E402
    CADIOT_EXAMPLES,
    _sh_symbol,
    _whitham_symbol,
    cadiot_symbol_admissibility,
)

OUT = ROOT / "writeup" / "data" / "p2_route_cadx_v1.json"
FIGS = ROOT / "writeup" / "figures"
FIG = FIGS / "fig67_route_cadx_v1_zero_diagonal.png"
PDF = ROOT / "Papers" / "2505.03091.pdf"
PDF_SHA256 = "0f1bc6181ce0d4375df3a012846d851c366cfc768b73fbfa3e2f7b6631f8081d"

# --------------------------------------------------------------------------
# CADX1 -- THE LOCATED CLAUSES.  `quote` is verbatim; `probe` is the
# whitespace-normalised substring the verifier searches for in the e-print.
# --------------------------------------------------------------------------
CADX_CLAUSES = [
    {
        "clause": "A1_LMIN",
        "where": "Assumption 1, page 6 (section 2.1)",
        "quote": ("Moreover, assume that there exists l_min > 0 such that "
                  "|l(xi)| >= l_min for all xi in R^m and lim_{|xi|_2 -> +infinity} "
                  "|l(xi)| = +infinity."),
        "probe": "|l(ξ)| ≥ lmin for all ξ ∈ Rm and lim |l(ξ)| = +∞.",
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("This is THE line.  L is the linear part and it is a Fourier "
                    "multiplier, so l IS the diagonal.  A zero or vanishing diagonal is "
                    "the case l_min = 0, and Assumption 1 is the hypothesis that "
                    "l_min > 0.  The exclusion is not a corollary, an estimate, or a "
                    "convenience: it is stated as a hypothesis before anything is built."),
    },
    {
        "clause": "SPACE_H",
        "where": "page 6, equation (9) and the sentence introducing it",
        "quote": ("As exposed in [21], Assumption 1 allows to define the Hilbert space H "
                  "as H = {u in L^2, ||u||_H = ||Lu||_2 < infinity}. ... By construction "
                  "L : H -> L^2 is an isometric isomorphism."),
        "probe": "Assumption 1 allows to define the Hilbert space H as",
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("The ambient space is BUILT from the non-vanishing of the diagonal, "
                    "and the paper says so in as many words -- Assumption 1 'allows to "
                    "define' H.  At a zero diagonal L : H -> L^2 is not an isometric "
                    "isomorphism (its inverse is unbounded), so it is not that the "
                    "estimates degrade: the space the whole argument runs in is gone."),
    },
    {
        "clause": "SPACE_XQ",
        "where": "page 6, section 2.2, the definition of X_q",
        "quote": ("X_q = {U = (u_n) : (U,U)_{X_q} < infinity} where "
                  "(U,V)_{X_q} = sum_n u_n v_n |l(n/2q)|^2."),
        "probe": None,
        "read_how": ("read from the rendered page image (page 6), not from text "
                     "extraction -- the summand is a displayed formula that pdftotext "
                     "linearises unreliably"),
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("The Fourier-side space degenerates for the same reason: its norm is "
                    "weighted by |l(n/2q)|^2, so a mode where the diagonal vanishes has "
                    "zero norm and (.,.)_{X_q} is not an inner product.  Both sides of "
                    "the L^2 <-> l^2 correspondence fail together."),
    },
    {
        "clause": "SIGMA_DELTA",
        "where": "page 8, equation (14), with Lemma 2.2",
        "quote": "sigma_delta = {lambda in C, |l(xi) - lambda| > delta for all xi in R^m}.",
        "probe": "|l(ξ) − λ| > δ for all ξ ∈ Rm",
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("The whole eigenvalue machinery lives in sigma_delta, and Lemma 2.2 "
                    "identifies the complement as the essential spectrum, which is the "
                    "range of l.  Put lambda = 0: the origin is inside the workable "
                    "region if and only if |l(xi)| > delta for every xi, i.e. if and only "
                    "if the diagonal is bounded away from zero.  A zero diagonal puts 0 "
                    "IN the essential spectrum, which is the one part of the spectrum "
                    "this framework computes rather than encloses."),
    },
    {
        "clause": "LEMMA_4_1_USES_IT",
        "where": "page 11, Lemma 4.1 and its proof",
        "quote": ("Let delta > 0, let J be a closed Jordan domain in sigma_delta ... "
                  "Then, because lambda in sigma_delta, we know that L - lambda I is "
                  "invertible and therefore u + (L - lambda I)^{-1} DG(u~)u = 0."),
        "probe": "we know that L − λI is invertible",
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("The use site, in the proof rather than the hypothesis list.  Every "
                    "eigenvalue enclosure in the paper is a Neumann/Fredholm argument "
                    "around (L - lambda I)^{-1}.  At lambda = 0 that operator is L^{-1}, "
                    "which exists boundedly exactly when the diagonal does not vanish."),
    },
    {
        "clause": "LEMMA_3_1_USES_IT",
        "where": "page 9, Lemma 3.1's proof",
        "quote": ("Now, we obtain that (L + tI)^{-1} : l^2 -> l^2 is compact thanks to "
                  "Assumption 1."),
        "probe": "is compact thanks to Assumption 1",
        "bears_on_the_zero_diagonal_question": "SUPPORTING",
        "reading": ("Assumption 1 is cited BY NAME inside section 3, the section the ban "
                    "is about.  Compactness of the resolvent -- what makes the spectrum "
                    "of DF(U_0) discrete at all -- is charged directly to it."),
    },
    {
        "clause": "GERSHGORIN_DOMINANCE",
        "where": "page 9, section 3's opening paragraph",
        "quote": ("By construction D is supposed to be diagonally dominant, which hints "
                  "to the Gershgorin theorem."),
        "probe": "is supposed to be diagonally dominant",
        "bears_on_the_zero_diagonal_question": "SUPPORTING",
        "reading": ("Leg 57's located line, re-verified here at second extraction.  It is "
                    "the SECTION-3 half of the picture: the pseudo-diagonalised operator "
                    "is assumed diagonally dominant.  On its own this is about dominance, "
                    "not about vanishing -- which is exactly why leg 57 could not close "
                    "the zero-diagonal question with it, and why A1_LMIN is the answer."),
    },
    {
        "clause": "TAIL_DIAGONAL_IS_THE_SYMBOL",
        "where": "page 10, section 3, the displayed identity for n outside I^N",
        "quote": "lambda_n = (pi_N (L + DG(U_0)) pi_N)_{n,n} = l(n~) + (DG(U_0))_{n,n}.",
        "probe": "λn = (πN (L + DG(U0 ))πN )n,n = l(ñ) + (DG(U0 ))n,n .",
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("This closes the identification for anyone who doubts that 'the "
                    "diagonal' means 'the symbol'.  Outside the numerical truncation the "
                    "Gershgorin CENTRES are literally l(n~) plus a decaying correction.  "
                    "A zero diagonal is a Gershgorin disc centred at the origin, at "
                    "arbitrarily high mode number, for a method whose whole content is "
                    "that those centres separate."),
    },
    {
        "clause": "SYSTEMS_KAPPA",
        "where": "page 26, section 5.3 (the only systems example)",
        "quote": "kappa = sup_{xi in R^2} ||l(xi)^{-1}||_2",
        "probe": "sup kl(ξ)−1 k2",
        "bears_on_the_zero_diagonal_question": "DECISIVE",
        "reading": ("The systems generalisation does not relax the hypothesis, it "
                    "restates it in matrix form: every bound in section 5.3 carries "
                    "kappa = sup ||l(xi)^{-1}||_2, which is +infinity the moment the "
                    "matrix symbol is singular anywhere.  A system is also the only route "
                    "by which an off-diagonal entry enters this framework at all, and "
                    "there it is the bounded constant lambda_1 lambda_2 - 1 = 1/9 against "
                    "diagonal entries growing like |2 pi xi|^2 (leg 62's CP3, confirmed)."),
    },
    {
        "clause": "ZERO_EIGENVALUE_IS_COVERED",
        "where": "page 24, Lemma 5.4's proof (capillary-gravity Whitham)",
        "quote": ("we know that DF(u~) has at least a 1D kernel coming from the "
                  "translation invariance of solutions. This implies that nu_2 = 0."),
        "probe": "kernel coming from the",
        "bears_on_the_zero_diagonal_question": "COUNTER-DIRECTION, AND IT MATTERS",
        "reading": ("The one clause that argues the other way, and it must be reported or "
                    "the answer is dishonest.  Cadiot DOES enclose the eigenvalue zero -- "
                    "the translation kernel, bracketed to [-0.0011, 0.0011] and then "
                    "pinned to exactly 0.  So 'zero is a problem for this framework' is "
                    "FALSE as stated about eigenvalues, and TRUE as stated about the "
                    "diagonal.  The ban's question is about the diagonal."),
    },
    {
        "clause": "FINITE_GAP_FAILURE",
        "where": "page 24, Remark 5.2",
        "quote": ("Numerically, we observe that DF(u~) possesses an eigenvalue around "
                  "0.19, which we were not able to enclose. ... our estimations lead to "
                  "bounds Z_{u,i} in Lemma 4.1 which are too big to obtain "
                  "non-intersecting Gershgorin disks in Theorem 4.3."),
        "probe": "which we were not able to enclose",
        "bears_on_the_zero_diagonal_question": "STRENGTHENING",
        "reading": ("The exclusion is not a knife edge at exactly zero.  With the "
                    "essential spectrum starting at 0.2, the author encloses eigenvalues "
                    "out to 0.16 (gap 0.04) and reports failing at 0.19 (gap 0.01), "
                    "because the constants Z_{u,i} blow up as the eigenvector delocalises "
                    "near the essential spectrum.  So the method degrades at a FINITE "
                    "distance from a vanishing diagonal, which is a stronger statement "
                    "than the hypothesis alone gives -- and it is the author's own."),
    },
    {
        "clause": "SH_MU_POSITIVE",
        "where": "page 19, section 5.1, equation (34) and the symbol below it",
        "quote": ("where mu > 0 ... L = -(I + Delta)^2 - mu I and "
                  "l(xi) = -(1 - |2 pi xi|_2^2)^2 - mu"),
        "probe": "where µ > 0",
        "bears_on_the_zero_diagonal_question": "DECISIVE, AND QUANTITATIVE",
        "reading": ("The paper's leading example carries the hypothesis as an explicit "
                    "parameter restriction on its first line.  At mu = 0 -- classical "
                    "Swift-Hohenberg at onset -- the symbol vanishes identically on the "
                    "circle |2 pi xi|_2 = 1.  That is a genuine zero diagonal, in the "
                    "paper's own leading model, and mu is exactly the distance to it."),
    },
]

#: The two 2025 forward citations, located at source (CADX7).  Leg 62's three (BCF, VDAC,
#: BH) are a disjoint set; the citation index is partial in both directions and that is
#: reported rather than hidden.
CADX_FORWARD = [
    {"arxiv": "2509.17099",
     "url": "https://arxiv.org/abs/2509.17099",
     "title": ("Proving the existence of localized patterns and saddle node bifurcations "
               "in 1D activator-inhibitor type models (2025)"),
     "sha256": "48512493615776b962b5e176663678777c256901a80d502912b2bef7d4377ba7",
     "relaxes_the_non_vanishing_hypothesis": False,
     "how_checked": ("full text extracted and searched for 'vanish', 'lmin', 'l(xi)', "
                     "'Assumption 1'; the only occurrences of 'vanish' are about the "
                     "approximate solution vanishing at the domain edge")},
    {"arxiv": "2509.16693",
     "url": "https://arxiv.org/abs/2509.16693",
     "title": ("Existence and orbital stability proofs of traveling wave solutions on an "
               "infinite strip for the suspension bridge equation (2025), "
               "DOI 10.1016/j.physd.2026.135240"),
     "sha256": "133adc019adf632d5293b93d875d284c1c07ed6e2f6263340dcddb8914a6bb25",
     "relaxes_the_non_vanishing_hypothesis": False,
     "how_checked": ("full text extracted; its symbol is "
                     "l(xi) = |2 pi xi|^4 - c^2 (2 pi xi_1)^2 + 1 and it works with "
                     "sup_xi 1/l(xi), i.e. it USES invertibility of the symbol rather "
                     "than weakening it")},
]

CADX_NOT_OBTAINED = {
    "semanticscholar_keyword_search": ("HTTP 429 rate limit on "
                                       "api.semanticscholar.org/graph/v1/paper/search; "
                                       "recorded as NOT OBTAINED, not glossed"),
    "export_arxiv_api": ("export.arxiv.org is not on this container's egress allowlist "
                         "(arxiv.org is); the API query returned empty"),
    "why_this_does_not_weaken_the_answer": ("the answer is a statement about ONE named "
                                            "paper's own hypotheses, read from its full "
                                            "text, not a claim about the whole literature"),
}


# --------------------------------------------------------------------------
# CADX1 -- machine-checked quotes
# --------------------------------------------------------------------------
def _normalise(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text))


def verify_quotes():
    """Re-extract the e-print and match every probe.  Never silently skips."""
    out = {"pdf": str(PDF.relative_to(ROOT)),
           "expected_sha256": PDF_SHA256,
           "probes": len([c for c in CADX_CLAUSES if c["probe"]])}
    if not PDF.is_file():
        out["status"] = "NOT_AVAILABLE"
        out["note"] = ("Papers/ is gitignored on purpose.  Re-fetch with "
                       "`bash Papers/fetch.sh 2505.03091` and re-run to reproduce the "
                       "quote check; the located clauses stand on the run recorded here.")
        return out
    sha = hashlib.sha256(PDF.read_bytes()).hexdigest()
    out["sha256"] = sha
    out["sha256_matches"] = bool(sha == PDF_SHA256)
    if shutil.which("pdftotext") is None:
        out["status"] = "NO_EXTRACTOR"
        return out
    proc = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          capture_output=True, text=True)
    body = _normalise(proc.stdout)
    hits, misses = [], []
    for c in CADX_CLAUSES:
        if not c["probe"]:
            continue
        (hits if _normalise(c["probe"]) in body else misses).append(c["clause"])
    out["status"] = "VERIFIED" if not misses else "PARTIAL"
    out["verified"] = hits
    out["not_found"] = misses
    out["n_verified"] = len(hits)
    return out


# --------------------------------------------------------------------------
# CADX4 -- the dial from covered to uncovered, in the paper's own parameter
# --------------------------------------------------------------------------
def sh_mu_dial(mus=(0.0, 1e-6, 1e-4, 1e-2, 0.05, 0.1, 0.2, 0.28, 0.32, 0.5, 1.0)):
    """inf_xi |l(xi)| for Swift-Hohenberg, l(xi) = -(1 - |2 pi xi|^2)^2 - mu.

    Analytically inf |l| = mu, attained on the whole circle |2 pi xi| = 1.  Measuring it
    on a grid rather than asserting it is the point: the grid recovers mu, and at mu = 0
    it recovers a genuine zero.
    """
    # dense near the unit circle of 2 pi xi, where the infimum lives
    xi = np.unique(np.concatenate([
        np.linspace(0.0, 2.0, 200001),
        1.0 / (2.0 * np.pi) + np.linspace(-1e-6, 1e-6, 20001)]))
    rows = []
    for mu in mus:
        vals = np.abs(_sh_symbol(xi, mu))
        lmin = float(vals.min())
        rows.append({"mu": float(mu),
                     "l_min_measured": lmin,
                     "l_min_predicted_is_mu": float(mu),
                     "abs_error": float(abs(lmin - mu)),
                     "argmin_2pi_xi": float(2.0 * np.pi * xi[int(np.argmin(vals))]),
                     "assumption_1_holds": bool(lmin > 0.0)})
    return rows


# --------------------------------------------------------------------------
# CADX5 -- the finite-gap failure, as two numbers
# --------------------------------------------------------------------------
def whitham_gap():
    xi = np.concatenate([np.linspace(0.0, 5.0, 200001),
                         np.geomspace(5.0, 1.0e4, 50000)[1:]])
    lmin = float(np.min(_whitham_symbol(xi)))
    return {
        "essential_spectrum_starts_at": lmin,
        "author_states_l_min": 0.2,
        "reproduction_error": float(abs(lmin - 0.2)),
        "enclosed_up_to": 0.16,
        "gap_that_worked": float(lmin - 0.16),
        "eigenvalue_not_enclosable": 0.19,
        "gap_that_failed": float(lmin - 0.19),
        "enclosed_eigenvalues": {"nu1": [0.2691, 0.2704], "nu2": 0.0,
                                 "nu3": [-0.1294, -0.1268]},
        "second_paper_internal_inconsistency": (
            "Lemma 5.4 states 'DF(u~) possesses exactly three eigenvalues in "
            "(-infinity, 0.16]' and then lists nu_1 in [0.2691, 0.2704], which is not in "
            "that interval (and would be embedded in the essential spectrum [0.2, "
            "infinity), where this framework's Jordan-domain-in-sigma_delta machinery "
            "cannot reach).  Most plausibly a sign slip and nu_1 in [-0.2704, -0.2691].  "
            "VERIFIED AGAINST THE RENDERED PAGE IMAGE (page 24), so it is printed that "
            "way and is not an extraction artefact.  Recorded, not resolved: it is not "
            "load-bearing for this leg's question, which turns on Assumption 1."),
        "paper_internal_inconsistency": (
            "Lemma 5.4's proof prints 'we fix delta = 0.4' and, one sentence later, "
            "'sigma_delta = (-infinity, 0.16)'.  With l_min = 0.2 the second forces "
            "delta = 0.04, and Remark 5.2's 'delta < 0.1' likewise has to be delta < 0.01 "
            "to reach the eigenvalue at 0.19.  VERIFIED AGAINST THE RENDERED PAGE IMAGE "
            "(page 24), so it is a factor-of-ten slip in the e-print's delta's, not a "
            "text-extraction artefact.  It does not touch this leg's answer -- the "
            "interval endpoints 0.16, 0.19 and 0.2 are mutually consistent -- and it is "
            "recorded because an unexplained arithmetic mismatch in a source is exactly "
            "what a later reader would trip over."),
    }


# --------------------------------------------------------------------------
# CADX6 -- the gate predicate, which can answer either way
# --------------------------------------------------------------------------
def covers_zero_diagonal(clauses, forward):
    """Does this scope COVER an operator with a zero/vanishing diagonal?

    'Covers' requires BOTH that no located clause decisively excludes it AND that no
    forward citation is needed to rescue it.  Returns a dict, never a bare boolean.
    """
    blocking = [c["clause"] for c in clauses
                if c["bears_on_the_zero_diagonal_question"].startswith("DECISIVE")]
    relaxers = [f["arxiv"] for f in forward
                if f.get("relaxes_the_non_vanishing_hypothesis")]
    covers = (not blocking) or bool(relaxers)
    return {"covers": bool(covers),
            "n_decisive_exclusions": len(blocking),
            "decisive_exclusions": blocking,
            "forward_citations_relaxing": relaxers}


def _synthetic_scope_without_assumption_1():
    """Lesson 90: the same code path, on a scope where the hypothesis is absent."""
    keep = {"GERSHGORIN_DOMINANCE", "ZERO_EIGENVALUE_IS_COVERED"}
    return [c for c in CADX_CLAUSES if c["clause"] in keep]


def make_figure(mu_rows, adm, whit):
    fig, ax = plt.subplots(1, 3, figsize=(16.0, 5.0))

    # (a) the mechanism: the symbol that vanishes, and the two the paper runs
    xi = np.linspace(0.0, 0.42, 4000)
    k = 2.0 * np.pi * xi
    for mu, style in ((0.0, "-"), (0.28, "--"), (0.32, ":")):
        ax[0].plot(k, np.abs(_sh_symbol(xi, mu)), style, lw=2.0,
                   label=f"$\\mu$ = {mu:g}" + ("  (ZERO DIAGONAL)" if mu == 0 else ""))
    ax[0].axhline(0.0, color="k", lw=0.8)
    ax[0].axvline(1.0, color="0.6", lw=0.8)
    ax[0].set_xlabel("$|2\\pi\\xi|$")
    ax[0].set_ylabel("$|l(\\xi)|$")
    ax[0].set_title("(a) Cadiot's leading example, Swift-Hohenberg\n"
                    "$l(\\xi) = -(1-|2\\pi\\xi|^2)^2-\\mu$: $l_{min}=\\mu$ exactly")
    ax[0].legend(fontsize=8)
    ax[0].set_ylim(-0.02, 0.6)

    # (b) Assumption 1's constant on all four worked examples, plus our object at zero
    names = list(adm.keys())
    vals = [adm[n]["l_min"] for n in names]
    ax[1].bar(range(len(names)), vals, color="0.35")
    ax[1].bar([len(names)], [1e-4], color="firebrick")
    ax[1].set_yscale("log")
    ax[1].set_xticks(range(len(names) + 1))
    ax[1].set_xticklabels(names + ["zero diagonal"], rotation=25, ha="right", fontsize=8)
    ax[1].set_ylabel("$l_{min} = \\inf_\\xi \\sigma_{min}(l(\\xi))$")
    ax[1].axhline(1e-4, color="firebrick", ls=":", lw=1.0)
    ax[1].set_title("(b) Assumption 1 on the paper's OWN examples\n"
                    "every one strictly positive; the excluded case is $l_{min}=0$")
    for i, v in enumerate(vals):
        ax[1].text(i, v * 1.15, f"{v:.3g}", ha="center", fontsize=8)
    ax[1].text(len(names), 1.4e-4, "0 (excluded)", ha="center", fontsize=8,
               color="firebrick")

    # (c) the finite-gap failure, on the author's own Whitham spectrum
    ax[2].axvspan(whit["essential_spectrum_starts_at"], 0.45, color="0.85",
                  label="essential spectrum $[0.2,\\infty)$")
    ax[2].axvline(0.16, color="tab:blue", lw=1.5,
                  label="enclosed out to 0.16 (gap 0.04)")
    ax[2].axvline(0.19, color="firebrick", lw=1.5, ls="--",
                  label="0.19 NOT enclosable (gap 0.01)")
    for v in (-0.1281, 0.0):
        ax[2].plot([v], [0.0], "ko", ms=6, zorder=5)
    ax[2].plot([0.26975], [0.0], "kx", ms=7, mew=1.6, zorder=5)
    ax[2].annotate("$\\nu_1$ as printed\n(sign slip? see JSON)", xy=(0.26975, 0.0),
                   xytext=(0.24, -0.55), fontsize=7, ha="center")
    ax[2].plot([0.0], [0.0], "o", ms=11, mfc="none", mec="tab:green", mew=2.0,
               label="$\\nu_2=0$: a zero EIGENVALUE, enclosed")
    ax[2].set_xlim(-0.25, 0.45)
    ax[2].set_ylim(-0.9, 0.9)
    ax[2].set_yticks([])
    ax[2].set_xlabel("$\\lambda$")
    ax[2].set_title("(c) Whitham, section 5.2: the method dies at a\n"
                    "FINITE gap, and a zero eigenvalue is fine")
    ax[2].legend(fontsize=7.5, loc="upper left")

    fig.suptitle("Route-CADX v1 (leg 304) -- Cadiot arXiv:2505.03091 does NOT cover a "
                 "zero diagonal: Assumption 1 is $|l(\\xi)| \\geq l_{min} > 0$",
                 fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=145)
    plt.close(fig)
    return FIG


def main():
    t0 = time.time()
    res = {
        "leg": 304,
        "route": "CADX",
        "title": "Does Cadiot's construction cover a zero diagonal?",
        "paper": "arXiv:2505.03091v1 [math.AP] 6 May 2025, 30 pp.",
        "url": "https://arxiv.org/abs/2505.03091",
        "paper_title": ("Matthieu Cadiot, Stability analysis for localized solutions in "
                        "PDEs and nonlocal equations on R^m"),
        "e_print_sha256": PDF_SHA256,
        "how_obtained": ("bash Papers/fetch.sh 2505.03091 -- egress probe HTTP 200, "
                         "1004 KB; read_at_source, at full text, second independent "
                         "extraction (pdftotext -layout) plus two rendered page images "
                         "(pages 6 and 24) for the two places extraction is unreliable.  "
                         "Papers/ is gitignored on purpose."),
        "read_depth": "read_at_source (NOT restated_by)",
    }

    res["CADX0_novelty"] = {
        "log": "writeup/novelty/leg_304.md",
        "verdict": "PROCEED_AS_CONFIRMATION_PLUS_NARROWING",
        "committed_before_construction": True,
        "prior_art_inside_this_repository": {
            "leg_57": ("located the dominance-hypothesis observation in this paper's full "
                       "text and put the current ban wording in place; explicitly did "
                       "NOT answer the zero-diagonal question"),
            "leg_62": ("Route-CP: read the same paper at full text under a DIFFERENT "
                       "pre-committed gate -- leg 58's off-diagonal / non-decaying tail "
                       "inverse hypothesis.  Overlap with this leg is exactly one "
                       "located clause (A1_LMIN).  Its symbol code is REUSED here, not "
                       "rebuilt."),
        },
        "this_leg_claims_no_mathematical_novelty_of_its_own": True,
    }

    res["CADX1_located_clauses"] = {
        "n_clauses": len(CADX_CLAUSES),
        "n_decisive": len([c for c in CADX_CLAUSES
                           if c["bears_on_the_zero_diagonal_question"]
                           .startswith("DECISIVE")]),
        "clauses": CADX_CLAUSES,
        "quote_verification": verify_quotes(),
    }

    res["CADX2_zero_eigenvalue_vs_zero_diagonal"] = {
        "zero_eigenvalue": ("COVERED, demonstrably.  Section 5.2 encloses the "
                            "translation kernel to [-0.0011, 0.0011] and concludes "
                            "nu_2 = 0 exactly.  Zero is not a forbidden VALUE."),
        "zero_diagonal": ("NOT COVERED.  Assumption 1 requires |l(xi)| >= l_min > 0, and "
                          "l IS the diagonal because L is a Fourier multiplier by the "
                          "class definition (1)-(2)."),
        "why_the_distinction_decides_the_ban": (
            "The ban's question is about the DIAGONAL of the operator -- leg 51's "
            "methodological finding concerns a Fredholm operator whose diagonal part "
            "vanishes, so the approximate inverse cannot be built diagonally.  Read as a "
            "question about eigenvalues the answer would have been 'yes, covered', and "
            "that would have been the wrong answer to the right words."),
    }

    adm = {}
    for name in CADIOT_EXAMPLES:
        a = cadiot_symbol_admissibility(name)
        stated = a["author_states"]["l_min"]
        a["l_min_minus_author_stated"] = (None if stated is None
                                          else float(a["l_min"] - stated))
        adm[name] = a
    res["CADX3_assumption_1_on_the_papers_own_examples"] = {
        "examples": adm,
        "l_min_range": [float(min(a["l_min"] for a in adm.values())),
                        float(max(a["l_min"] for a in adm.values()))],
        "worst_reproduction_error_vs_author": float(max(
            abs(a["l_min_minus_author_stated"]) for a in adm.values()
            if a["l_min_minus_author_stated"] is not None)),
        "status": ("CONFIRMED, second independent run of leg 62's symbol code "
                   "(solver/certificate_shapes.py, REUSED not rebuilt).  Reported as "
                   "confirmation, never as a new measurement."),
        "reading": ("Assumption 1 is not decorative: on every one of the paper's four "
                    "worked examples it is a positive number the author either states or "
                    "can state, and the growth half is a positive exponent every time."),
    }

    mu_rows = sh_mu_dial()
    res["CADX4_the_dial_is_the_papers_own_parameter"] = {
        "example": "planar Swift-Hohenberg, section 5.1",
        "symbol": "l(xi) = -(1 - |2 pi xi|_2^2)^2 - mu",
        "rows": mu_rows,
        "max_abs_error_l_min_vs_mu": float(max(r["abs_error"] for r in mu_rows)),
        "l_min_at_mu_0": float([r for r in mu_rows if r["mu"] == 0.0][0]
                               ["l_min_measured"]),
        "cadiots_two_runs": [0.28, 0.32],
        "reading": ("l_min = mu to grid precision across five orders of magnitude, and "
                    "at mu = 0 it is a genuine zero attained on the entire circle "
                    "|2 pi xi| = 1.  So the paper's leading example is a one-parameter "
                    "family that CROSSES the boundary of its own hypothesis, and Cadiot's "
                    "two published runs sit 0.28 and 0.32 away from the excluded case.  "
                    "The exclusion is measurable in the author's own units, not a "
                    "rhetorical reading of a hypothesis."),
    }

    whit = whitham_gap()
    res["CADX5_the_method_dies_at_a_finite_gap"] = whit

    gate_actual = covers_zero_diagonal(CADX_CLAUSES, CADX_FORWARD)
    gate_no_a1 = covers_zero_diagonal(_synthetic_scope_without_assumption_1(),
                                      CADX_FORWARD)
    relaxing = [dict(f, relaxes_the_non_vanishing_hypothesis=True)
                for f in CADX_FORWARD]
    gate_relaxed = covers_zero_diagonal(CADX_CLAUSES, relaxing)
    res["CADX6_controls_lesson_90"] = {
        "actual": gate_actual,
        "control_scope_without_assumption_1": gate_no_a1,
        "control_with_a_relaxing_forward_citation": gate_relaxed,
        "the_negative_is_a_property_of_the_clauses": bool(
            (not gate_actual["covers"]) and gate_no_a1["covers"]
            and gate_relaxed["covers"]),
        "reading": ("The predicate flips to 'covers' two independent ways, so 'does not "
                    "cover' is a fact about the located hypotheses and not about this "
                    "code."),
    }

    res["CADX7_forward_citations"] = {
        "citations": CADX_FORWARD,
        "n_relaxing_the_hypothesis": 0,
        "leg_62_examined": ["BCF", "VDAC", "BH"],
        "disjointness_note": ("leg 62's three and these two are disjoint sets; the "
                              "citation index is partial in both directions.  Five "
                              "citing papers have now been checked between the two legs "
                              "and none relaxes the non-vanishing symbol hypothesis."),
        "not_obtained": CADX_NOT_OBTAINED,
    }

    fig = make_figure(mu_rows, adm, whit)
    res["figure"] = {
        "path": str(fig.relative_to(ROOT)),
        "number": "fig67 (PROVISIONAL -- fig67 was unclaimed at this leg's merge base; "
                  "renumbering is integration's call if a parallel leg took it)",
        "registered_in": ("writeup/data/p2_route_cadx_v1.json and "
                          "experiments/journal/leg_304.md.  NOT registered in "
                          "writeup/INDEX.md: that file is shared and this leg's declared "
                          "territory excludes it, so the registration is flagged for "
                          "integration rather than taken."),
        "panels": ["(a) the SH symbol at mu = 0 (a genuine zero diagonal) against the "
                   "paper's two runs",
                   "(b) l_min on all four worked examples, log scale, against the "
                   "excluded l_min = 0",
                   "(c) the Whitham spectrum: enclosure works at gap 0.04, fails at "
                   "0.01, and the zero EIGENVALUE is enclosed"],
    }

    # ---------------- the gate, in DIRECTION.md's pre-committed wording ----------
    res["gate"] = {
        "question": ("Does the full text yield a definite answer -- either (i) Cadiot's "
                     "hypotheses exclude a zero/vanishing diagonal (quote the line), or "
                     "(ii) the construction covers it?"),
        "answer": "yes",
        "branch": "(i) -- the hypotheses exclude it",
        "the_line": ("Assumption 1, page 6: 'Moreover, assume that there exists "
                     "l_min > 0 such that |l(xi)| >= l_min for all xi in R^m and "
                     "lim_{|xi|_2 -> +infinity} |l(xi)| = +infinity.'"),
        "ambiguous": False,
        "n_decisive_exclusions": gate_actual["n_decisive_exclusions"],
        "precommitted_yes_i_branch": ("bank at full strength -- the ban stands on "
                                      "measured, quoted footing"),
        "escalation": ("NO.  The escalating branch was yes-(ii) ('the construction covers "
                       "it'), which this run did not reach."),
    }

    res["verdict"] = "CADIOT_DOES_NOT_COVER_A_ZERO_DIAGONAL__HYPOTHESIS_QUOTED"
    res["what_this_establishes"] = (
        "arXiv:2505.03091 excludes a zero/vanishing diagonal by HYPOTHESIS, not by "
        "accident: Assumption 1 states |l(xi)| >= l_min > 0 on page 6, before any "
        "construction, and the exclusion is load-bearing at eight further located places "
        "-- the ambient space H (Assumption 1 'allows to define' it, and L : H -> L^2 is "
        "an isometric isomorphism only if the diagonal is bounded below), the Fourier "
        "space X_q whose norm is weighted by |l(n/2q)|^2, sigma_delta (14) which places "
        "lambda = 0 in the ESSENTIAL spectrum when the diagonal vanishes, Lemma 4.1's "
        "proof which needs L - lambda I invertible, Lemma 3.1's resolvent compactness "
        "'thanks to Assumption 1', the identity lambda_n = l(n~) + (DG(U_0))_{n,n} which "
        "makes the Gershgorin centres literally the symbol, the systems constant "
        "kappa = sup ||l(xi)^{-1}||_2, and the mu > 0 restriction on the leading example. "
        "The magnitude of the exclusion is the paper's own parameter: l_min = mu exactly "
        "for Swift-Hohenberg, and the two published runs sit at 0.28 and 0.32.  The "
        "method moreover fails at a FINITE gap, not at zero -- Remark 5.2 encloses at gap "
        "0.04 and cannot enclose at 0.01.  A zero EIGENVALUE is covered (nu_2 = 0, the "
        "translation kernel, section 5.2), which is the distinction the question turns on."
    )
    res["what_this_does_NOT_establish"] = (
        "That the ban is lifted, narrowed, or discharged -- answering the ban's named "
        "question is not the same act as changing its status, which is the user's call "
        "and integration-owned; this leg's own gate says so in its yes-(i) branch.  That "
        "leg 51's methodological finding is TRUE, or false -- this is a statement about "
        "the coverage of one published construction, not about our operator's "
        "mathematics.  That the observation is novel: it is folklore in print (leg 57) "
        "and half of it was already located by leg 62.  That Cadiot's paper is deficient: "
        "these are hypotheses it states plainly and discharges on all four of its own "
        "examples."
    )
    res["clay_odds"] = ("~0.05%, unmoved.  No link of the L1->L4 chain is touched by a "
                        "literature scope answer.")
    res["elapsed_s"] = float(time.time() - t0)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2) + "\n")

    print(f"[CADX] gate: {res['gate']['answer']} {res['gate']['branch']}")
    print(f"[CADX] decisive exclusions: {gate_actual['n_decisive_exclusions']} "
          f"of {len(CADX_CLAUSES)} located clauses")
    qv = res["CADX1_located_clauses"]["quote_verification"]
    print(f"[CADX] quote check: {qv['status']} "
          f"({qv.get('n_verified')}/{qv['probes']} probes, "
          f"sha256 match {qv.get('sha256_matches')})")
    print(f"[CADX] l_min on Cadiot's own examples: "
          f"{res['CADX3_assumption_1_on_the_papers_own_examples']['l_min_range']}, "
          f"worst reproduction error "
          f"{res['CADX3_assumption_1_on_the_papers_own_examples']['worst_reproduction_error_vs_author']:.3e}")
    print(f"[CADX] SH dial: max |l_min - mu| = "
          f"{res['CADX4_the_dial_is_the_papers_own_parameter']['max_abs_error_l_min_vs_mu']:.3e}, "
          f"l_min at mu=0 = "
          f"{res['CADX4_the_dial_is_the_papers_own_parameter']['l_min_at_mu_0']:.3e}")
    print(f"[CADX] controls: negative is a property of the clauses = "
          f"{res['CADX6_controls_lesson_90']['the_negative_is_a_property_of_the_clauses']}")
    print(f"[CADX] wrote {OUT.relative_to(ROOT)} and {fig.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
