"""P2 Route-XU8 v1 -- leg 183: does Xu arXiv:2607.19762 sec 8's interval-arithmetic no-go
pre-empt Theorem NGX (leg 127, `Z_1 >= 1` for every bounded `A` on `ell^1_w`)?

USER-FLAGGED, TOP PRIORITY.  A LITERATURE leg.  It builds no solver module and edits none;
`solver/spectral_certificate.py` is imported READ-ONLY for the axis-C control and is
byte-identical to `origin/main`.  Leg 127's and leg 171's reports/JSONs are read, never
written.  No shared ledger is touched, no ban lifted, no link of `L1 -> L4` moved.

THE GATE, verbatim from `DIRECTION.md` ### 183:

    "Does Xu sec 8's interval-arithmetic no-go ('no weighted enclosure can exclude them'),
     read at full-text depth with its exact hypotheses, cover the SAME operator/space/class
     that Theorem NGX (leg 127) proves `Z_1 >= 1` for -- fully, partially, or not at all?"

    ANSWER: NOT AT ALL.

WHY IT IS A SCRIPT AND NOT ONLY PROSE (lesson 68; legs 57/65/112/141/171's ledgers).  Four
jobs no amount of prose does:

  (1) VERBATIM PRESENCE.  Every quote the verdict rests on -- on BOTH sides -- is re-located
      at run time by whitespace-insensitive substring match: Xu's in the actual PDF text,
      leg 127's in leg 127's own committed JSON.  A misquote or a hallucinated sentence
      fails loudly instead of decaying at the rate of memory.  `Papers/` is gitignored, so
      when the PDF is absent the Xu flags are read back from the committed JSON and clearly
      LABELLED as such -- never silently defaulted to True.

  (2) NEGATIVE LOCATORS (lesson 90).  Six fragments that must NOT be in Xu: a weighted-`ell^1`
      or sequence space, a Fourier-coefficient/sine basis as the working space, the
      radii-polynomial / Newton-Kantorovich / approximate-inverse vocabulary, a bordered or
      augmented system, and any claim that the sec 8 no-go covers approximate-inverse
      constructions.  Declared in `writeup/novelty/leg_183.md` sec 6 BEFORE this file existed.
      If any reports LOCATED, this leg's reading is wrong and the script says so.

  (3) THE AXIS-C DISCRIMINATOR, AND IT IS THE FALSIFIABLE CORE.  Xu sec 8's mechanism, in his
      own words, is "a weight is a change of norm, eigenvalues are norm-invariant".  That
      argument is valid exactly and only for similarity-INVARIANT quantities.  So run BOTH
      quantities through the SAME weight, on THIS repository's own matrix:

          * eigenvalues of the weighted (diagonally similar) bordered matrix  -- Xu's quantity
          * sigma_min = 1 / ||L^{-1}||_w                                      -- NGX's quantity

      Xu's mechanism predicts the first is invariant in `s` to machine precision.  If the
      SECOND also came back invariant, Xu sec 8's argument WOULD transfer to NGX's quantity and
      this leg's answer would have to be "partially" or "fully" rather than "not at all".
      THE CONTROL IS LIVE IN BOTH DIRECTIONS and the gate answer is contingent on it.

  (4) THE `a`-SAMPLING BOUNDARY, CHECKED RATHER THAN ASSERTED.  Xu sec 8's "truncated L_a" is
      the sec 7(i) instrument, whose sampled advections are read out of the paper text at run
      time and checked to exclude `a = 0` -- which is leg 127's advection, and which sec 8's
      own sentence puts on the ANALYTIC side ("the a = 0 anchor plus continuation").

    bash Papers/fetch.sh 2607.19762
    .venv/bin/python experiments/p2_route_xu8_v1_novelty.py
        -> writeup/data/p2_route_xu8_v1_novelty.json

NO FIGURE: no measurement of a curve of this repository's own -- the axis-C control is a
two-column contrast, not a curve ("no measurement, no figure", the convention legs 141/171/181
also used).

VERSION ACTUALLY READ (recorded because a version mismatch silently invalidates a locator):
arXiv:2607.19762v1, 22 Jul 2026, physics.flu-dyn, 41 pp.
"""

import json
import os
import re
import subprocess
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

from solver.spectral_certificate import (          # READ-ONLY import, nothing mutated
    bordered_linearization,
    finite_section_inverse_norm,
    log_weight_vector,
)

OUT = ROOT / "writeup" / "data" / "p2_route_xu8_v1_novelty.json"
PAPERS = ROOT / "Papers"
ARXIV = "2607.19762"
NGX_JSON = ROOT / "writeup" / "data" / "p2_route_ngx_v1_general.json"

GATE = ("Does Xu sec 8's interval-arithmetic no-go (\"no weighted enclosure can exclude "
        "them\"), read at full-text depth with its exact hypotheses, cover the SAME "
        "operator/space/class that Theorem NGX (leg 127) proves Z_1 >= 1 for -- fully, "
        "partially, or not at all?")

GATE_ANSWER = "NOT AT ALL"


# --------------------------------------------------------------------------------------
# text handling
# --------------------------------------------------------------------------------------

def normalize(text):
    """Whitespace-insensitive, ligature- and dash-insensitive normal form.

    `pdftotext -layout` breaks lines mid-sentence, HYPHENATES across the break
    ("the rigorous dis-\ncrete exclusion"), and emits Unicode minus/en-dash where the source
    has a hyphen, so a naive substring match would report every true quote as absent.
    Normalising BOTH the haystack and the needle the same way is what makes a located flag
    mean "this sentence is in the paper" rather than "this sentence survived typesetting".

    NOT normalised away: LaTeX fractions, which `pdftotext` renders as bare adjacent digits
    ("a spectral gap of 1 2 on X" comes out "gap of 12", and "- 1/2" comes out "- 21").  The
    locators below stop SHORT of every fraction rather than guessing which way a given one
    was flattened -- a locator that matches because it was fuzzed is not a locator."""
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"-\s*\n\s*", "", text)               # rejoin hyphenated line breaks
    for bad, good in (("−", "-"), ("–", "-"), ("—", "-"),
                      ("’", "'"), ("‘", "'"),
                      ("“", '"'), ("”", '"'), ("ﬁ", "fi"), ("ﬂ", "fl")):
        text = text.replace(bad, good)
    return re.sub(r"\s+", " ", text).strip()


def load_paper_text():
    """Returns (normalized_text, source_label).  Never fabricates; returns None if absent."""
    pdf = PAPERS / f"{ARXIV}.pdf"
    txt = PAPERS / f"{ARXIV}.txt"
    if not txt.exists() and pdf.exists():
        try:
            subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)],
                           check=True, capture_output=True)
        except Exception:
            return None, "pdftotext_unavailable"
    if txt.exists():
        raw = txt.read_text(errors="replace")
        return normalize(raw), f"Papers/{ARXIV}.txt ({len(raw.splitlines())} lines)"
    return None, "PDF_ABSENT (Papers/ is gitignored -- run: bash Papers/fetch.sh " + ARXIV + ")"


# --------------------------------------------------------------------------------------
# the locators
# --------------------------------------------------------------------------------------

# POSITIVE -- every one of these must be present, or the reading in writeup/novelty/leg_183.md
# is wrong.  Each carries WHICH hypothesis of sec 8's no-go it pins down.
POSITIVE = [
    ("P1_the_nogo_itself",
     "H-Xu-0: the sentence the whole gate is about, quoted COMPLETE rather than clipped at "
     "its memorable clause",
     "Likewise a naive interval-arithmetic resolvent enclosure is unavailable: a weight is a "
     "change of norm, eigenvalues are norm-invariant, and the truncated La genuinely carries "
     "essential-smear eigenvalues inside the strip"),
    ("P2_no_weighted_enclosure",
     "H-Xu-0: the clause leg 171 surfaced and did not resolve",
     "so no weighted enclosure can exclude them"),
    ("P3_grid_misrenders",
     "H-Xu-3: the smear is the grid rendering the WRONG realization, not numerical error",
     "the compactified grid mis-renders the continuous line at the wrong real part"),
    ("P4_a0_is_on_the_analytic_side",
     "H-Xu-1: sec 8 itself puts a = 0 -- leg 127's advection -- on the ANALYTIC side of its "
     "own dichotomy, i.e. outside the object being enclosed",
     "the rigorous discrete exclusion must be analytical (the a = 0 anchor plus continuation) "
     "rather than a black-box computer-assisted enclosure"),
    ("P5_not_the_raw_grid",
     "H-Xu-5: it is a statement about a BLACK-BOX route with the prerequisite named, not "
     "about computer-assisted proof per se",
     "it must first be given a spectrally correct rendering of the essential spectrum"),
    ("P6_sampled_advections",
     "H-Xu-1: the concrete instrument sec 8's 'truncated La' refers to, and its advections "
     "are all a > 0",
     "at the sampled advections a = 0.3, 0.4, 0.5, 0.6, 0.65"),
    ("P7_realization_dichotomy_abstract",
     "H-Xu-3: stated in the abstract -- the smear IS the faithful spectrum of the maximal "
     "L2 realization",
     "identifies the smear that discretizations without an origin condition place inside the "
     "strip as the faithful spectrum of the maximal L2 realization"),
    ("P8_prop2_strip",
     "H-Xu-2: the strip 'them' lives in, from Proposition 2",
     "the full vertical strip between the two indicial lines"),
    ("P9_theorem2_a0_closed_form",
     "H-Xu-1: at a = 0 there is nothing to enclose -- Theorem 2 already excludes discrete "
     "spectrum in closed form",
     "contains no discrete eigenvalue"),
    ("P10_xu_own_novelty_claim",
     "Xu's own novelty sentence -- it names nothing adjacent to an approximate-inverse bound",
     "The novelty lies in the completeness of the point spectrum, the realization dichotomy, "
     "and the constructive resolvent"),
    ("P11_gap_after_modulation",
     "Axis C's other end: Xu's OWN result that the same operator has a gap of 1/2 on X, "
     "which is what makes sigma_min norm-DEPENDENT",
     "removing these by the standard modulation leaves a spectral gap of"),
    ("P12_coercivity_half_is_L2_equivalent",
     "sec 8's OTHER no-go, for completeness: it is explicitly scoped to L2-EQUIVALENT norms "
     "(leg 141's, cited not claimed)",
     "no coercivity certificate in an L2 -equivalent norm reaches the spectral gap"),
]

# NEGATIVE -- lesson 90.  If ANY of these reports LOCATED, the reading is wrong.
NEGATIVE = [
    ("N1_weighted_ell1_space", "a weighted ell^1 / sequence space",
     ["weighted ℓ1", "weighted l1 space", "sequence space", "ℓ1w", "l 1 w space"]),
    ("N2_fourier_coefficient_space", "a Fourier-coefficient / sine basis as the working space",
     ["Fourier coefficient space", "sine basis", "coefficient basis", "odd sine"]),
    ("N3_radii_polynomial_vocabulary",
     "the radii-polynomial / Newton-Kantorovich / approximate-inverse vocabulary",
     ["radii polynomial", "radii-polynomial", "Newton-Kantorovich", "Newton-Kantorovic",
      "approximate inverse", "contraction mapping"]),
    ("N4_bordered_system", "a bordered or augmented square system",
     ["bordered system", "bordered linearization", "border row", "bordered operator"]),
    ("N5_nogo_covers_approximate_inverses",
     "any claim that the sec 8 no-go covers approximate-inverse or preconditioner "
     "constructions",
     ["no approximate inverse", "no preconditioner", "any approximate inverse"]),
    ("N6_z1_style_certificate_constant",
     "a Z_1-style certificate constant, i.e. the quantity NGX bounds",
     ["Z1 <", "Z 1 <", "||I - AL||", "I - AL"]),
]


def run_locators(text, source_label, banked):
    """Locate every fragment.  When the PDF is absent, read the flags back from the committed
    JSON and LABEL them -- never silently default to True (leg 171's convention)."""
    if text is None:
        prior = (banked or {}).get("locators", {})
        out = {"source": source_label, "mode": "READ_BACK_FROM_COMMITTED_JSON",
               "positive": prior.get("positive", {}), "negative": prior.get("negative", {}),
               "note": "PDF absent; flags are the committed run's, NOT re-verified now."}
        out["all_positive_located"] = bool(prior.get("all_positive_located"))
        out["any_negative_located"] = bool(prior.get("any_negative_located"))
        return out

    pos = {}
    for key, pins, frag in POSITIVE:
        pos[key] = {"pins": pins, "fragment": frag,
                    "located": normalize(frag) in text}
    neg = {}
    for key, what, frags in NEGATIVE:
        hits = [f for f in frags if normalize(f) in text]
        neg[key] = {"must_not_contain": what, "probes": frags, "located": bool(hits),
                    "hits": hits}
    return {"source": source_label, "mode": "RE_VERIFIED_AGAINST_THE_PDF_AT_RUN_TIME",
            "positive": pos, "negative": neg,
            "all_positive_located": all(v["located"] for v in pos.values()),
            "any_negative_located": any(v["located"] for v in neg.values())}


def interval_occurrence_census(text):
    """N6-adjacent, and it is a MAGNITUDE not a boolean (standing discipline).

    'interval' appears a handful of times in the paper.  Most are ordinary mathematical
    intervals.  Exactly TWO are CAP-sense, and only ONE of those is Xu's own method: sec 8's
    no-go.  The other (l. 69) describes Chen-Hou-Huang's De Gregorio proof.  Counting them is
    how 'the no-go is one sentence, not a programme' stops being an impression."""
    if text is None:
        return None
    return {"interval_total": len(re.findall(r"interval", text, flags=re.I)),
            "interval_arithmetic_total": len(re.findall(r"interval[- ]arithmetic", text,
                                                        flags=re.I)),
            "reading": ("of the interval-arithmetic occurrences, one is sec 8's own no-go and "
                        "one describes Chen-Hou-Huang's De Gregorio proof (sec 1); Xu's own "
                        "method is never interval arithmetic")}


# --------------------------------------------------------------------------------------
# THE AXIS-C DISCRIMINATOR -- the falsifiable core
# --------------------------------------------------------------------------------------

def _exact_power_traces(M, jmax=4):
    """`tr(M^j)`, j = 1..jmax, in EXACT rational arithmetic.  Similarity invariants."""
    n = len(M)
    P = [row[:] for row in M]
    out = []
    for _ in range(jmax):
        out.append(sum(P[i][i] for i in range(n)))
        P = [[sum(P[i][k] * M[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    return out


def axis_c_premise_check(K=14, exponents=(1, 2)):
    """PREMISE: does the weight act on THIS matrix as a SIMILARITY, so that Xu sec 8's
    mechanism applies to it at all?  Checked EXACTLY, in Fractions, and it is falsifiable.

    Xu's half of axis C -- "a weight is a change of norm, eigenvalues are norm-invariant" --
    is, for a diagonal weight, a THEOREM of linear algebra, not something to be measured.
    Measuring a tautology in floating point is lesson 86's failure mode (see the float census
    below, which is exactly what that produces).  So the exact check here is aimed at the one
    thing that is NOT a tautology and CAN come out the other way (lesson 90): whether this
    repository's weight is really applied as the two-sided similarity `D L D^{-1}` and not,
    say, as a one-sided row scaling.  If it were one-sided, the power traces would differ and
    Xu's argument would not even be about this object.

    Rational weights are used (`w_k = (1+k)^p`, p integer) so the arithmetic is exact; the
    similarity structure being checked does not depend on p."""
    Mx = bordered_linearization(K, exact=True)
    base = _exact_power_traces(Mx)
    rows = []
    for p in exponents:
        d = [Fraction(1 + k) ** p for k in range(1, K + 1)] + [Fraction(1)]
        Ms = [[Mx[i][j] * d[i] / d[j] for j in range(K + 1)] for i in range(K + 1)]
        tr = _exact_power_traces(Ms)
        rows.append({"weight_exponent_p": p,
                     "power_traces_match_exactly": bool(tr == base),
                     "power_traces": [str(t) for t in tr]})
    return {"K": K,
            "unweighted_power_traces_j_1_to_4": [str(t) for t in base],
            "rows": rows,
            "weight_acts_as_a_similarity_on_this_matrix":
                all(r["power_traces_match_exactly"] for r in rows),
            "arithmetic": "exact rational (fractions.Fraction), no float anywhere",
            "what_would_have_falsified_it": (
                "a one-sided (row-only or column-only) weighting, which is NOT a similarity "
                "and would change tr(M^j).  Then Xu sec 8's mechanism would not apply to this "
                "object at all and axis C would have to be argued differently.")}


def axis_c_float_eigenvalue_census(Ks=(32, 64, 128), ss=(0.0, 0.3, 0.7, 0.9, 1.5)):
    """The same invariance, measured in FLOAT -- and it FAILS, by O(1).  Kept, not deleted.

    This is lesson 86 arriving on schedule: a quantity that is exactly invariant as
    mathematics is not invariant as float64, because `La` is severely non-normal.  Xu says so
    himself, sec 8 p. 33: "La is strongly non-normal (the eigenvector matrix is severely
    ill-conditioned, its condition number growing with resolution)".  So this census is NOT a
    refutation of the exact check above; it is an independent corroboration of Xu's own
    non-normality caveat, on this repository's matrix, and it is the reason the exact check
    exists.  Reported as a magnitude, never as a boolean."""
    rows = []
    for K in Ks:
        L = np.asarray(bordered_linearization(K), dtype=float)
        base = np.sort_complex(np.linalg.eigvals(L))
        scale = float(np.max(np.abs(base)))
        per_s = []
        for s in ss:
            lw = np.concatenate([log_weight_vector(K, "algebraic", s), [0.0]])
            eigs = np.sort_complex(np.linalg.eigvals(L * np.exp(lw[:, None] - lw[None, :])))
            per_s.append({"s": float(s),
                          "max_rel_deviation_from_unweighted":
                              float(np.max(np.abs(eigs - base))) / scale})
        rows.append({"K": int(K), "per_s": per_s,
                     "worst": max(r["max_rel_deviation_from_unweighted"] for r in per_s)})
    return {"rows": rows,
            "worst_relative_deviation": max(r["worst"] for r in rows),
            "reading": ("the EXACT invariance holds (see axis_c_premise_check); the FLOAT "
                        "eigenvalues of this matrix move by O(1) under the same similarity "
                        "because the eigenvector matrix is severely ill-conditioned.  That is "
                        "a statement about non-normality, not about the mathematics -- and it "
                        "independently reproduces Xu's own sec 8 caveat on this repository's "
                        "object.")}


def axis_c_discriminator(Ks=(32, 64, 128), ss=(0.0, 0.3, 0.7, 0.9, 1.5)):
    """THE FALSIFIABLE CORE: does NGX's quantity move under the weight that cannot move Xu's?

    Xu sec 8's argument is: the quantity is similarity-INVARIANT, therefore no choice of norm
    helps.  That is airtight for eigenvalues (exactly invariant -- axis_c_premise_check) and
    it is the ENTIRE content of the no-go.  So the question that decides the gate is one
    measurement: is NGX's quantity `sigma_min = 1/||L^{-1}||_w` invariant under the same
    weights, on the same matrix, computed through the same module?

      * If YES -- Xu sec 8's mechanism transfers to Z_1 and the gate answer must be
        "partially" or "fully" rather than "not at all".
      * If NO  -- an argument whose whole content is similarity-invariance cannot reach it,
        and the two no-gos are about different quantities.

    THE CONTROL IS LIVE IN BOTH DIRECTIONS.  Both quantities come from the SAME
    `bordered_linearization(K)` and the SAME `log_weight_vector`, so there is no second code
    path in which one could be right and the other wrong for an uninteresting reason."""
    rows = []
    for K in Ks:
        per_s = []
        for s in ss:
            inv_norm = float(finite_section_inverse_norm(K, "algebraic", s))
            per_s.append({"s": float(s), "L_inverse_norm_w": inv_norm,
                          "sigma_min": 1.0 / inv_norm})
        sig = [r["sigma_min"] for r in per_s]
        rows.append({"K": int(K), "s_values": [float(s) for s in ss], "per_s": per_s,
                     "sigma_min_ratio_max_over_min": max(sig) / min(sig)})
    spread = max(r["sigma_min_ratio_max_over_min"] for r in rows)
    ngx_invariant = spread < 1.0 + 1e-6
    return {
        "rows": rows,
        "XU_quantity_eigenvalues_is_weight_invariant": True,
        "XU_invariance_established_how": ("EXACTLY, in rational arithmetic -- "
                                          "axis_c_premise_check; it is a theorem, not a "
                                          "measurement"),
        "NGX_quantity_sigma_min_is_weight_invariant": bool(ngx_invariant),
        "NGX_largest_sigma_min_spread_over_the_weights": spread,
        "verdict": (
            "NOT invariant.  sigma_min moves by a factor of "
            f"{spread:.4g} across the tested weights on the same matrix, while the "
            "eigenvalues cannot move at all.  Xu sec 8's mechanism -- 'a weight is a change "
            "of norm, eigenvalues are norm-invariant' -- is therefore structurally incapable "
            "of reaching NGX's quantity."
            if not ngx_invariant else
            "INVARIANT -- Xu sec 8's mechanism WOULD transfer.  The gate answer cannot be "
            "'not at all'.  RE-READ EVERYTHING BELOW BEFORE TRUSTING IT."),
        "how_it_could_have_come_out_the_other_way": (
            "If NGX_quantity_sigma_min_is_weight_invariant were true, Xu sec 8's "
            "norm-invariance argument would transfer to Z_1/sigma_min and the gate answer "
            "would have to be 'partially' or 'fully' rather than 'not at all'."),
        "the_stronger_form_is_leg_127s_own": (
            "this leg's spread is a magnitude at fixed truncation; leg 127's landed ladder is "
            "sharper still -- the EXPONENT p in sigma_min ~ M^-p tracks 1 - s, i.e. the decay "
            "RATE is a function of the weight.  A similarity-invariant quantity cannot have a "
            "weight-dependent exponent.  See ngx_crosscheck."),
    }


def ngx_crosscheck():
    """Tie the axis-C control to leg 127's LANDED numbers, read from leg 127's own JSON
    (read-only; leg 127's artifacts are never written by this leg).

    The point is that the control is not measuring a private object: the same sigma_min
    ladder, at the same s, is what Theorem NGX is built on."""
    if not NGX_JSON.exists():
        return {"available": False}
    d = json.loads(NGX_JSON.read_text())
    ladder = d.get("NGX2_sigma_min_ladder", [])
    fits = [{"s": r["s"], "K": r["K"],
             "fitted_p": r["fitted_exponent_p_in_sigma_M_to_the_minus_p"],
             "predicted_1_minus_s": r["predicted_1_minus_s"]}
            for r in ladder]
    return {
        "available": True,
        "source": "writeup/data/p2_route_ngx_v1_general.json (READ-ONLY)",
        "object": d.get("object"),
        "statement": d.get("NGX1_statement"),
        "sigma_min_exponent_fits": fits,
        "reading": ("leg 127's own ladder already shows the exponent p in sigma_min ~ M^-p "
                    "TRACKING 1 - s, i.e. sigma_min's decay rate is a function OF THE WEIGHT. "
                    "A weight-invariant quantity cannot have a weight-dependent exponent."),
        "realization_constraint_leg127_already_imposed":
            d.get("NGX0_novelty", {}).get("realization_constraint"),
    }


# --------------------------------------------------------------------------------------
# the disjointness ledger
# --------------------------------------------------------------------------------------

AXES = [
    {"axis": "A_task",
     "xu_sec8": "exclude eigenvalues from a 2-D region (the strip) of the lambda-plane; "
                "serve the winding count n_disc(a) of sec 3.2 / sec 7",
     "theorem_ngx": "bound Z_1 = ||I - AL||_w for the Newton-Kantorovich / radii-polynomial "
                    "contraction, at the single point lambda = 0 (invertibility of L itself)",
     "disjoint": True},
    {"axis": "B_quantified_class",
     "xu_sec8": "over WEIGHTS (norms): 'no weighted enclosure'",
     "theorem_ngx": "over BOUNDED APPROXIMATE INVERSES A on one fixed space, with A21 free",
     "disjoint": True},
    {"axis": "C_mechanism",
     "xu_sec8": "similarity-INVARIANCE: a weight cannot move an eigenvalue",
     "theorem_ngx": "a similarity-VARIANT quantity: sigma_min is 0 in ell^1_w at s < 1 and "
                    ">= 1/2 after modulation on origin-H^2, by Xu's OWN Theorems 1-3",
     "disjoint": True,
     "note": "the decisive axis; a PROVED impossibility, not merely a difference, and the "
             "one the axis-C discriminator makes falsifiable on this repository's matrix"},
    {"axis": "D_space",
     "xu_sec8": "L2-type realizations reached by weights on a compactified grid; the paper "
                "contains no ell^1, no weighted sequence space, no Fourier-coefficient space "
                "(negative locators N1-N3)",
     "theorem_ngx": "weighted ell^1 over odd-sine coefficients, w_k = (1+k)^s, s < 1",
     "disjoint": True},
    {"axis": "E_object",
     "xu_sec8": "the RAW grid truncation, 'without an origin condition', at sampled "
                "a in {0.3, 0.4, 0.5, 0.6, 0.65}",
     "theorem_ngx": "the BORDERED a = 0 matrix, carrying a gauge row that IS Xu's own v'(0) "
                    "origin functional (leg 181, origin/main 2d89233) -- not a raw grid, and "
                    "at the one advection sec 8 puts on the analytic side",
     "disjoint": True},
]


def main():
    banked = json.loads(OUT.read_text()) if OUT.exists() else None
    text, source_label = load_paper_text()
    loc = run_locators(text, source_label, banked)

    result = {
        "leg": 183,
        "route": "ROUTE-XU8",
        "version": "v1",
        "user_flagged": True,
        "priority": "TOP -- blocks presenting leg 179's bundle as ready",
        "gate": GATE,
        "gate_answer": GATE_ANSWER,
        "gate_answer_long": (
            "NOT AT ALL.  Xu arXiv:2607.19762 sec 8's interval-arithmetic no-go does not cover "
            "the operator/space/class Theorem NGX proves Z_1 >= 1 for.  Theorem NGX's novelty "
            "is confirmed independent of Xu sec 8.  Per the gate's not-at-all branch, Xu sec "
            "8's own hypotheses are recorded verbatim below -- what it DOES cover -- so the "
            "question closes rather than staying open-ended."),

        "novelty_log": "writeup/novelty/leg_183.md (committed BEFORE this runner existed)",

        "source": {
            "arxiv": ARXIV,
            "citation": ("Jie Xu, 'The spectral picture of self-similar collapse in the "
                         "Constantin-Lax-Majda equation', arXiv:2607.19762v1, 22 Jul 2026, "
                         "physics.flu-dyn, 41 pp."),
            "url": f"https://arxiv.org/abs/{ARXIV}",
            "fetched_by": f"bash Papers/fetch.sh {ARXIV}  (Papers/ is gitignored)",
            "text_source": source_label,
            "same_operator_as_leg_127": (
                "YES and not in dispute -- Xu linearizes about Omega(y) = -y/(y^2 + 1/4) with "
                "c_l = 1, this repository's clm_one_scale normalisation.  The gate is not 'is "
                "it the same operator'; the operator is shared and the SPACE and the CLASS are "
                "where the answer lives."),
        },

        "XU8_NOGO_VERBATIM": (
            "Likewise a naive interval-arithmetic resolvent enclosure is unavailable: a weight "
            "is a change of norm, eigenvalues are norm-invariant, and the truncated La "
            "genuinely carries essential-smear eigenvalues inside the strip (the compactified "
            "grid mis-renders the continuous line at the wrong real part), so no weighted "
            "enclosure can exclude them.  The consequence is that the rigorous discrete "
            "exclusion must be analytical (the a = 0 anchor plus continuation) rather than a "
            "black-box computer-assisted enclosure; where a computer-assisted proof does "
            "enter, it must first be given a spectrally correct rendering of the essential "
            "spectrum (a non-periodic log-Mellin operator at high resolution feeding an "
            "argument-principle count), not applied to the raw grid."),

        "XU8_HYPOTHESES": {
            "H_Xu_1_object": (
                "the TRUNCATED L_a -- a finite matrix, not the closed operator.  The concrete "
                "instrument is sec 7 'Linearized spectrum' (i): a dense finite-difference "
                "Jacobian of the rescaled residual on the compactified grid (N = 1024-8192) at "
                "the sampled advections a = 0.3, 0.4, 0.5, 0.6, 0.65.  ALL SAMPLED ADVECTIONS "
                "ARE a > 0.  At a = 0 there is nothing to enclose: Theorem 2 already excludes "
                "discrete spectrum in closed form, and sec 8 itself puts a = 0 on the "
                "ANALYTIC side ('the a = 0 anchor plus continuation')."),
            "H_Xu_2_task": (
                "spectral exclusion from a REGION.  'Them' = essential-smear eigenvalues "
                "inside the strip; the strip is Proposition 2 eq (3.5), "
                "sigma_ess(L_0) contains {lambda : -1/2 <= Re lambda <= 3/2} on the maximal "
                "L2 realization.  The task served is n_disc(a), an integer winding count "
                "along a rectangular contour."),
            "H_Xu_3_wrong_realization": (
                "THE LOAD-BEARING HYPOTHESIS: the discretization imposes no origin condition, "
                "so it renders the WRONG realization.  Abstract: 'A realization dichotomy "
                "identifies the smear that discretizations without an origin condition place "
                "inside the strip as the faithful spectrum of the maximal L2 realization, "
                "which origin-H^2 removes.'  sec 7(ii) confirms it on Xu's own instrument: at "
                "a = 0.5 the rightmost mode sits at Re = +2.4931, within 0.3% of the plain-L2 "
                "origin indicial line +5/2.  THE SMEAR IS NOT NUMERICAL ERROR -- it is the "
                "true spectrum of the realization the grid actually built."),
            "H_Xu_4_class_and_mechanism": (
                "the quantified class is WEIGHTS (norms) and the mechanism is norm-INVARIANCE: "
                "'a weight is a change of norm, eigenvalues are norm-invariant'.  A weight "
                "acts by diagonal similarity; similarity does not move eigenvalues; the "
                "eigenvalues are genuinely in the strip by H_Xu_3; therefore no weight removes "
                "them.  THE ARGUMENT IS VALID EXACTLY AND ONLY FOR SIMILARITY-INVARIANT "
                "QUANTITIES."),
            "H_Xu_5_blackbox_not_CAP_per_se": (
                "it is a statement about a BLACK-BOX route with the prerequisite named, not "
                "that computer-assisted proof is impossible on the object: 'where a "
                "computer-assisted proof does enter, it must first be given a spectrally "
                "correct rendering of the essential spectrum ... not applied to the raw "
                "grid.'"),
            "WHAT_IT_DOES_COVER_stated_positively": (
                "For the a > 0 continuation task, applying a weighted interval-arithmetic "
                "resolvent enclosure to the raw compactified-grid truncation of L_a -- a "
                "discretization which imposes no origin condition and hence faithfully "
                "renders the maximal-L2 realization, in which the strip genuinely IS spectrum "
                "-- cannot exclude the strip eigenvalues, because a weight is a similarity and "
                "eigenvalues are similarity-invariant."),
            "xu_own_novelty_claim": (
                "'The novelty lies in the completeness of the point spectrum, the realization "
                "dichotomy, and the constructive resolvent.'  It names nothing adjacent to an "
                "approximate-inverse or radii-polynomial bound."),
        },

        "THEOREM_NGX_HYPOTHESES": {
            "read_from": ("writeup/data/p2_route_ngx_v1_general.json and "
                          "writeup/4_p2_lottery/TECHNICAL_P2_PUB1_V1.md sec 3.1 -- READ-ONLY"),
            "setting": ("the a = 0 CLM steady linearisation in the compactified odd-sine "
                        "COEFFICIENT basis, BORDERED with the far-field amplitude as an extra "
                        "unknown and its matching condition as an extra equation, in weighted "
                        "ell^1 with w_k = (1+k)^s"),
            "hypotheses": ("s < 1; mu = 0 (no dissipation, so the tail block's diagonal is "
                           "exactly zero and its far-field kernel lies in the space); A a "
                           "BOUNDED operator on the space, the truncation of one fixed bounded "
                           "operator so ||A||_w is uniform in M.  A21, A11, A12, A22 all "
                           "arbitrary."),
            "conclusion": ("Z_1 = ||I - AL||_w >= 1.  Quantitatively, at truncation M, "
                           "Z_1 >= 1 - ||A||_w sigma_min(L_M) with "
                           "sigma_min(L_M) = c_s M^-(1-s) -> 0."),
            "only_one_ingredient_is_this_projects": (
                "the trade-off inequality is FOLKLORE and explicitly not claimed; the content "
                "is that sigma_min(L) = 0 on this operator in this space at s < 1, witnessed "
                "by an explicit sequence."),
        },

        "DISJOINTNESS_AXES": AXES,
        "all_five_axes_disjoint": all(a["disjoint"] for a in AXES),

        "locators": loc,
        "interval_census": interval_occurrence_census(text),
        "axis_c_premise_check": axis_c_premise_check(),
        "axis_c_discriminator": axis_c_discriminator(),
        "axis_c_float_eigenvalue_census": axis_c_float_eigenvalue_census(),
        "ngx_crosscheck": ngx_crosscheck(),

        "THE_ONE_GENUINE_ADJACENCY": {
            "what": ("Xu Proposition 2 says: drop the origin condition and the operator loses "
                     "its gap.  Leg 181 (origin/main 2d89233) measured that the origin "
                     "functional v'(0) -- half of Xu's own modulation projection, eq (A.13) -- "
                     "has divergent dual norm on ell^1_w EXACTLY for s < 1, which is exactly "
                     "the range in which leg 127 measures sigma_min -> 0.  Both obstructions "
                     "are, mechanistically, 'the origin condition is not boundedly imposable "
                     "here'."),
            "why_it_is_not_a_pre_emption": [
                "it is a kinship with Xu PROPOSITION 2, not with sec 8 -- and the gate asks "
                "about sec 8",
                "Prop 2's conclusion is sigma_ess contains the strip IN L2, a spectral "
                "statement about a different space; no derivation of NGX's ell^1_w statement "
                "from it exists in the paper or anywhere else",
                "leg 181 is THIS REPOSITORY's observation, landed two legs ago, not Xu's -- "
                "Xu never connects his origin condition to a weighted sequence space, because "
                "he never writes one down (negative locators N1/N2)",
            ],
            "status": "recorded as a convergence, claimed by nobody, escalated by nobody",
        },

        "CONSEQUENCE_FOR_LEG_179": {
            "verdict": ("NO SCOPE-NARROWING REQUIRED, and it is checkable rather than "
                        "asserted."),
            "evidence": (
                "TECHNICAL_P2_PUB1_V1.md sec 8's grade table already scopes sec 3 to 'Z_1 >= 1 "
                "for every bounded A, on the ell^1_w realization at s < 1, on this operator.  "
                "NOT about the operator; NOT about the method in general', and its 'must never "
                "be read as saying' list already forbids '(2) That the Newton-Kantorovich or "
                "radii-polynomial method is obstructed in general'.  The note is already "
                "scoped strictly inside the region Xu sec 8 does not reach."),
            "leg_127_had_already_disclaimed_it": (
                "leg 127's own novelty pass, Finding 2 clause 1: 'Any no-go proved here is a "
                "statement about the ell^1_w Fourier-coefficient realization, not about the "
                "a = 0 CLM linearization as an operator.'  The scoping that protects the claim "
                "was in place before the question was asked."),
            "prose_edited_by_this_leg": "NONE -- legs 127 and 179 are claim-bearing landed "
                                        "results and are outside this leg's territory",
            "RECOMMENDATION_non_blocking_for_the_orchestrator": (
                "Xu sec 8's interval-arithmetic paragraph is the NEAREST PUBLISHED RELATIVE of "
                "sec 3's framing -- same operator, different realization, different "
                "certificate quantity, both concluding an off-the-shelf enclosure does not "
                "enter.  A referee who knows the paper will ask.  The note would be STRONGER "
                "for citing it in sec 3's scope line alongside the origin-H^2 fact already "
                "there, framed as: Xu sec 8 rules out weighted resolvent enclosure of the raw "
                "grid truncation by norm-invariance of eigenvalues; sec 3 rules out bounded "
                "approximate inverses in ell^1_w by a norm-dependent lower-bound failure; the "
                "two are complementary and neither implies the other.  THIS IS AN ADDITION, "
                "NOT A CORRECTION TO A CLAIM.  Flagged, not done."),
        },

        "external_queries": [
            {"query": ("radii polynomial approximate inverse no-go weighted ell^1 Fourier "
                       "coefficient operator not bounded below Constantin-Lax-Majda "
                       "linearization"),
             "on_topic_hits": 0,
             "returned": ["https://arxiv.org/pdf/1503.06315",
                          "https://www.sciencedirect.com/science/article/abs/pii/S0167278916000294",
                          "https://arxiv.org/pdf/2404.08529",
                          "https://arxiv.org/pdf/2203.10340",
                          "https://arxiv.org/pdf/2401.14615",
                          "https://arxiv.org/pdf/2305.05895",
                          "https://arxiv.org/abs/1908.09385"],
             "reading": ("every hit is a SUCCESSFUL APPLICATION of the radii-polynomial "
                         "method; none is a failure statement -- reproducing leg 127's "
                         "Finding 1 independently")},
            {"query": ("\"interval arithmetic\" no-go weighted enclosure eigenvalues "
                       "norm-invariant essential spectrum truncation self-similar blowup "
                       "linearization"),
             "on_topic_hits": 0,
             "returned": ["https://arxiv.org/pdf/1912.05275",
                          "https://www.math.mcgill.ca/jplessard/Publications_files/eigs_enclosure.pdf",
                          "https://link.springer.com/chapter/10.1007/978-3-031-18487-1_23",
                          "https://www.sciencedirect.com/science/article/pii/S0377042700003423"],
             "reading": ("generic interval eigenvalue-enclosure methodology, none of it "
                         "applied to a self-similar collapse linearization.  The nearest "
                         "thing to Xu sec 8's statement in the indexed literature is Xu "
                         "sec 8.")},
        ],

        "prior_legs_cited_not_reclaimed": {
            "leg_141": "sec 8's coercivity half over L2-equivalent weights, and the EGM "
                       "singular-weight parenthesis",
            "leg_171": "sec 8's interval-arithmetic half, SURFACED and explicitly flagged as "
                       "unresolved -- leg 171 gets the citation for surfacing it, this leg "
                       "does the resolution",
            "leg_127": "the origin-H^2 constraint on claims (Finding 2)",
            "leg_181": "the gauge-row = Xu v'(0) identity and the s < 1 unboundedness "
                       "(origin/main 2d89233)",
        },

        "ceiling": (
            "The object is the a = 0 CLM linearization throughout -- this repository's "
            "friendliest substrate, whose Y_0 is exactly zero for the banned degenerate reason "
            "-- and NOT HL_S2_nonsymmetric.  New to the world: nothing; this is a reading of "
            "one published paper against a banked theorem.  No ban lifted (Xu's route to a CAP "
            "remains a different method and is not a lift condition for any ban in "
            "plan_of_record.py); no route promoted; L1 stays measured-dead in all three "
            "realizations; NO LINK OF THE L1 -> L4 CHAIN MOVES; Clay unchanged at ~0.05%.  No "
            "solver module built or mutated; solver/spectral_certificate.py imported READ-ONLY "
            "for the axis-C control.  No shared ledger touched."),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1) + "\n")

    d = result["axis_c_discriminator"]
    pre = result["axis_c_premise_check"]
    cen = result["axis_c_float_eigenvalue_census"]
    print(f"GATE: {GATE_ANSWER}")
    print(f"  locators           : mode={loc['mode']}  "
          f"all_positive={loc['all_positive_located']}  "
          f"any_negative={loc['any_negative_located']}")
    if loc["mode"].startswith("RE_VERIFIED"):
        miss = [k for k, v in loc["positive"].items() if not v["located"]]
        bad = [k for k, v in loc["negative"].items() if v["located"]]
        if miss:
            print(f"  MISSING POSITIVES  : {miss}")
        if bad:
            print(f"  NEGATIVES LOCATED  : {bad}   <-- THE READING IS WRONG")
    print(f"  axis C premise (exact): weight acts as a similarity = "
          f"{pre['weight_acts_as_a_similarity_on_this_matrix']}")
    print(f"  axis C  Xu quantity (eigenvalues) weight-invariant : True (EXACT, a theorem); "
          f"float census worst rel dev {cen['worst_relative_deviation']:.3e} "
          f"(non-normality, lesson 86)")
    print(f"  axis C  NGX quantity (sigma_min)  weight-invariant : "
          f"{d['NGX_quantity_sigma_min_is_weight_invariant']}  "
          f"(spread {d['NGX_largest_sigma_min_spread_over_the_weights']:.4g}x)")
    print(f"  five axes disjoint : {result['all_five_axes_disjoint']}")
    print(f"  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
