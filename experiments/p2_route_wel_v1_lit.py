"""P2 Route-WEL v1 -- leg 141: is leg 111's ZERO-WIDTH WINDOW published?

A LITERATURE leg.  It builds no solver module, edits none (it IMPORTS
`solver/energy_coercivity.py` read-only, to run leg 111's own quadrature on a trial family
leg 111 did not try), touches no shared ledger, lifts no ban and moves no link of the
`L1 -> L4` chain.  `L1` stays measured-dead in all three realizations whatever this file
says.

THE GATE, verbatim from `DIRECTION.md` leg 141:

    "Does any published work contain leg 111's zero-width-window obstruction (the
     damping/space gamma-threshold coincidence on the CLM linearization), explicitly or as
     a special case of a stated more-general result?"

    ANSWER: YES -- as a special case of a stated more general result, located at
    Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop. 2.1, with Chen-Hou-Huang arXiv:1905.06387
    sec 2.1 / Prop. 3.1 supplying the same two halves on the same profile and Xu
    arXiv:2607.19762 sec 8 supplying an explicit published carve-out that names EGM's
    estimate as the singular-weight case.  The literal SENTENCE ("the two thresholds
    coincide, so the window has zero width") is NOT in print: three queries aimed straight
    at it returned nothing on-topic (novelty log Q4, Q5, Q7).

WHAT LEG 111 CLAIMED, verbatim from `capabilities.py`:

    "damping at the origin needs gamma > 3 while the basis is in L^2_phi only for gamma < 3
     -- the SAME threshold, so the window has ZERO width."

WHY IT IS A SCRIPT AND NOT ONLY PROSE (lesson 68, and legs 57/65/112's ledgers).  Two jobs
no amount of prose does:

  (1) VERBATIM PRESENCE.  Every quote this leg's verdict rests on is re-located in the
      actual PDF text at run time, by whitespace-insensitive substring match, so a
      misquote or a hallucinated sentence fails loudly instead of decaying at the rate of
      memory.  `Papers/` is gitignored, so when the PDFs are absent the located flags are
      read back from the committed JSON and clearly marked as such.

  (2) THE WINDOW WIDTH AS A FUNCTION OF THE TRIAL SPACE.  Leg 111's admissibility test is
      hardwired to `sin theta` -- vanishing order `p = 1` at the origin.  EGM's Prop. 2.1
      hypothesis `f odd, f'(0) = Hf(0) = 0` is a statement about `p`, not about the
      operator.  So the window `(3, 2p+1)` is RE-MEASURED here on leg 111's own graded
      quadrature at `p = 1, 2, 3`.  The `p = 1` column is the instrument control and MUST
      reproduce leg 111's banked numbers; if it does not, this leg's arithmetic is not leg
      111's and the comparison is void.  This check was SPECIFIED IN THE NOVELTY LOG (sec 6)
      BEFORE IT WAS CODED, and it can report the other answer: had `p = 2, 3` come back
      divergent at `gamma = 4`, the gate would answer NO.

    bash Papers/fetch.sh 1906.05811 1905.06387 2607.19762 2210.07191
    .venv/bin/python experiments/p2_route_wel_v1_lit.py
        -> writeup/data/p2_route_wel_v1_lit.json

NO FIGURE: no measurement of a curve, nothing to plot ("no measurement, no figure").

VERSIONS ACTUALLY READ (recorded because a version mismatch silently invalidates a
locator): arXiv:1906.05811 (Analysis & PDE 14 (2021) 891), arXiv:1905.06387 (CPAM,
doi 10.1002/cpa.21991), arXiv:2607.19762 (the version this repository already cites in
`capabilities.py`), arXiv:2210.07191 (the copy already in `Papers/`, banked at leg 57).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

from solver.energy_coercivity import (          # noqa: E402  -- READ-ONLY import
    damping_factor_at_origin,
    graded_quadrature,
    weight_values,
)

OUT = ROOT / "writeup" / "data" / "p2_route_wel_v1_lit.json"
PAPERS = ROOT / "Papers"
LEG111 = ROOT / "writeup" / "data" / "p2_route_we_v1_coercivity.json"

GATE = ("Does any published work contain leg 111's zero-width-window obstruction (the "
        "damping/space gamma-threshold coincidence on the CLM linearization), explicitly "
        "or as a special case of a stated more-general result?")

CLAIM_UNDER_TEST = ("damping at the origin needs gamma > 3 while the basis is in L^2_phi "
                    "only for gamma < 3 -- the SAME threshold, so the window has ZERO "
                    "width.   [capabilities.py, the solver/energy_coercivity.py row]")

# ---------------------------------------------------------------------------
# 1. the located statements.  `fragment` is what is re-located in the PDF at run time;
#    `quote` is the reading quote, and `supplies` says WHICH half of leg 111's coincidence
#    the statement carries.  Nothing here is paraphrased into the verdict.
# ---------------------------------------------------------------------------
LOCATED = [
    {
        "id": "EGM-P21",
        "paper": "1906.05811",
        "cite": "Elgindi, Ghoul, Masmoudi, Stable self-similar blowup for a family of "
                "nonlocal transport equations, Anal. PDE 14 (2021) 891",
        "locator": "Proposition 2.1 (sec 2, Coercivity)",
        "supplies": "BOTH halves, as hypotheses, with a POSITIVE gap at gamma = 4",
        "quote": ("There exists a universal constant C > 0 so that if a is small enough and "
                  "if f is odd, f'(0) = Hf(0) = 0 and int_R |f|^2 phi(y) dy < +infty, then "
                  "int_R f M_a f phi(y) dy <= (-1/2 - C|a|) int_R f(y)^2 phi(y) dy."),
        "fragment": "f is odd, f ′ (0) = Hf (0) = 0",
        "why_it_is_the_answer": (
            "The three hypotheses ARE leg 111's two thresholds, imposed on the perturbation "
            "instead of tested on a fixed basis: `int |f|^2 phi < infty` is leg 111's "
            "admissibility test verbatim, and `f odd, f'(0) = 0` is what a function must "
            "satisfy to pass it at this weight.  The weight is gamma = 4, PAST leg 111's "
            "damping threshold 3, and the gap is nonetheless -1/2."),
    },
    {
        "id": "EGM-WEIGHT",
        "paper": "1906.05811",
        "cite": "same paper, Main Theorem (weighted space definition)",
        "locator": "sec 1, `Main Theorem`, the definition of L^2_phi",
        "supplies": "the weight exponent: gamma = 4 at the origin",
        "quote": "phi = (1 + y^2)^2 / y^4",
        "fragment": "L2loc (R) :",
        "why_it_is_the_answer": (
            "Same weight as Chen-Hou-Huang (3.6) up to the b-normalization; gamma = 4 near "
            "the origin, i.e. exactly leg 111's `A4_chen_hou` member."),
    },
    {
        "id": "EGM-A0-IS-CLM",
        "paper": "1906.05811",
        "cite": "same paper, sec 1 (the family (1.4)) and (1.6)-(1.8)",
        "locator": "sec 1",
        "supplies": "the object: a = 0 of their family IS the CLM model, with F_0 = y/(1+y^2)",
        "quote": ("when a = 2 we get the De Gregorio model and when a = 0 we get CLM model "
                  "... When a = 0, the profile F_0 has the form F_0(y) = y/(1 + y^2), "
                  "HF_0(y) = -1/(y^2 + 1)"),
        "fragment": "when a = 0 we get CLM",
        "why_it_is_the_answer": (
            "Fixes that Prop. 2.1 covers leg 111's object.  F_0 = y/(1+y^2) is leg 111's "
            "Omega(y) = -y/(y^2 + 1/4) up to the scaling symmetry the paper itself records "
            "(F_{a,mu}(z) := F_a(mu z) leaves (1.7) invariant) and the sign convention; a "
            "dilation of y does not change a decay RATE, which is why the constant 1/2 is "
            "the same number Xu publishes on the b = 1/2 normalization."),
    },
    {
        "id": "EGM-PRICE",
        "paper": "1906.05811",
        "cite": "same paper, sec 3 (Modulation equation and derivation of the law)",
        "locator": "sec 3, opening sentence",
        "supplies": "the published RESOLUTION: the origin constraints are bought by modulation",
        "quote": ("Since our coercivity estimate from the previous section relies on "
                  "d_y q(0) = H(q)(0) = 0, we will use that we have the 'free' parameters mu "
                  "and lambda to fix these conditions."),
        "fragment": "relies on ∂y q(0) = H(q)(0) = 0",
        "why_it_is_the_answer": (
            "The window is not free: it is paid for with two modulation parameters.  That is "
            "the move leg 111's fixed-basis realization does not make."),
    },
    {
        "id": "CHH-DAMPING",
        "paper": "1905.06387",
        "cite": "Chen, Hou, Huang, On the finite time blowup of the De Gregorio model for "
                "the 3D Euler equation, CPAM (doi 10.1002/cpa.21991)",
        "locator": "sec 2.1, Derivation of the damping term",
        "supplies": "the DAMPING half: choose the exponent so the multiplier is negative",
        "quote": ("For x close to 0, we choose a singular weight x^{-k}, k in N^+ to take "
                  "advantage of the stretching term. ... Using integration by parts, we "
                  "obtain I = < -C(k-1)/2 + (c_omega + u_x), omega^2 x^{-k} > = <D, omega^2 "
                  "x^{-k}>.  We will choose k so that the coefficient D is negative (we "
                  "choose k = 4 for a = 1 and small |a|)."),
        "fragment": "We will choose k so that the coefficient D is negative",
        "why_it_is_the_answer": (
            "This is leg 111's D_phi, obtained the same way (integration by parts of the "
            "transport term into a single multiplier), on the same family, with the same "
            "chosen exponent 4.  `Damping at the origin needs gamma > 3` is this sentence."),
    },
    {
        "id": "CHH-SQUEEZE",
        "paper": "1905.06387",
        "cite": "same paper, sec 2.1",
        "locator": "sec 2.1, two paragraphs below the damping derivation",
        "supplies": "the SQUEEZE itself, stated in print -- at the FAR FIELD, threshold k = 1",
        "quote": ("In order to control the perturbation omega in the far field, we have to "
                  "choose a weight phi that decays more slowly than x^{-1} so that the "
                  "weighted L^2 norm of omega is not too weak for large |x|.  As a result, "
                  "(c_l x + a u) omega_x does not produce a damping term for large |x| in "
                  "our weighted L^2 estimate after performing integration by parts.  This is "
                  "one of the subtleties in our analysis."),
        "fragment": "This is one of the subtleties in our analysis.",
        "why_it_is_the_answer": (
            "Leg 111's obstruction SHAPE -- the exponent that buys damping is excluded by "
            "the exponent the norm can afford, on one and the same integration-by-parts "
            "identity -- in print, on this equation family, and named a `subtlety` rather "
            "than a no-go.  Located at the far field (threshold k = 1), not the origin "
            "(threshold gamma = 3); CHH escape it by taking the far-field damping from the "
            "vortex-stretching term instead."),
    },
    {
        "id": "CHH-P31",
        "paper": "1905.06387",
        "cite": "same paper, Proposition 3.1 and the weights (3.6)-(3.7)",
        "locator": "sec 3, (3.6) and Proposition 3.1",
        "supplies": "BOTH halves paired, on the b = 1/2 CLM profile: gamma = 4 AND omega_{0,x}(0) = 0",
        "quote": ("phi = -1/omega_x^3 - 1/(b^2 omega_x) = (b^2 + x^2)^2/(b^2 x^4), b = 1/2 "
                  "... Note that phi ~ x^{-4} + 1 ... if |a| < a_0 and the initial data "
                  "omega_bar + omega_0 of (3.4) satisfies that omega_0 is odd, omega_0 in "
                  "H^2, omega_{0,x}(0) = 0 and E(0) < c|a|"),
        "fragment": "Note that ϕ ≍ x−4 + 1",
        "why_it_is_the_answer": (
            "b = 1/2 is leg 111's Omega(y) = -y/(y^2 + 1/4); the profile is obtained, in "
            "their words, `by using the exact formula of the solution of (1.3) with a = 0`.  "
            "gamma = 4 and omega_{0,x}(0) = 0 appear in ONE proposition on THIS profile."),
    },
    {
        "id": "XU-NOGO",
        "paper": "2607.19762",
        "cite": "Xu, The spectral picture of self-similar collapse in the Constantin-Lax-"
                "Majda equation",
        "locator": "sec 8 (Discussion)",
        "supplies": "a published weighted-energy/coercivity NO-GO on this operator -- with a "
                    "DIFFERENT quantifier and a DIFFERENT mechanism, plus an explicit "
                    "carve-out naming EGM Prop. 2.1",
        "quote": ("Two natural approaches do not reach the gap.  A weighted-energy/coercivity "
                  "estimate cannot certify the gap: the far field is already coercive in "
                  "plain L^2 with the sharp edge, but a local positive multiplier +phi H Omega "
                  "near the origin (with H Omega(0) > 0) survives every L^2-equivalent weight, "
                  "so no coercivity certificate in an L^2-equivalent norm reaches the spectral "
                  "gap.  (The small-a coercivity estimate of Elgindi, Ghoul, and Masmoudi "
                  "[15, Prop. 2.1], for odd f with f'(0) = Hf(0) = 0 in a singular-weighted "
                  "space, is not a counterexample but an instance of the realization mechanism "
                  "of Section 3.1: the singular weight and origin constraints define their own "
                  "realization, in which a gap is certified; it neither contradicts nor "
                  "supplies the X-gap here.)"),
        "fragment": "is not a counterexample but an instance of the realization mech",
        "why_it_is_the_answer": (
            "Two things at once.  (i) A published no-go for weighted-energy coercivity on "
            "exactly this operator -- but quantified over L^2-EQUIVALENT weights (bounded "
            "above and below), a strictly different class from leg 111's singular "
            "phi ~ theta^{-gamma}, and with a different mechanism (a surviving positive "
            "multiplier, not a threshold coincidence).  So it is NOT leg 111's result in "
            "print.  (ii) The parenthesis hands over the gate's answer: the singular-weight "
            "case IS treated, IS attributed, and in it `a gap is certified`."),
    },
    {
        "id": "XU-EJECTION",
        "paper": "2607.19762",
        "cite": "same paper, Appendix A (the weighted semigroup space Y_theta)",
        "locator": "Appendix A, after Definition A.2 / around (A.20)",
        "supplies": "the same tension in Xu's own construction: the useful weight EJECTS the "
                    "modes -- resolved, not called an obstruction",
        "quote": ("Because the weight y^{-2 theta - 1} blows up at the origin, elements of "
                  "Y_theta carry no pointwise origin traces; the modulation projection is "
                  "therefore defined on the physical X (which has traces) and mapped into "
                  "Y_theta, not applied within Y_theta. ... The two symmetry modes are "
                  "excluded from Y_{3/2} by that weight: the integrands of ||u_1||^2 and "
                  "||u_0||^2 behave like y^{-4} and y^{-2} at the origin and diverge."),
        "fragment": "excluded from Y3/2 by that weight",
        "why_it_is_the_answer": (
            "The weight that puts the origin's essential line at the damped rate (theta = "
            "3/2, core weight y^{-4}) is the weight that ejects the modes -- leg 111's "
            "coincidence in Xu's variables.  Xu does not treat it as an obstruction: the "
            "projection is done on X and transferred in."),
    },
    {
        "id": "CH2D-SQUEEZE",
        "paper": "2210.07191",
        "cite": "Chen, Hou, Stable nearly self-similar blowup of the 2D Boussinesq and 3D "
                "Euler equations with smooth data I: Analysis",
        "locator": "sec 2 (weighted L^2 estimate of (2.32), weight phi = x^{-alpha} y^{-beta})",
        "supplies": "the same squeeze on a DIFFERENT operator, with a NON-empty but expensive "
                    "window (alpha >= 14)",
        "quote": ("Since omega(x,0) != 0, eta(x,0) != 0, we need to choose beta < 1 so that "
                  "the energy is well-defined. ... This forces one to choose a very singular "
                  "weight to extract a damping term for eta, e.g. alpha >= 14 if beta = 0, a "
                  "new difficulty which is absent in [17,19,20,35].  We overcome it by using "
                  "L^infty type estimates"),
        "fragment": "we need to choose β < 1 so that the energy is well-defined",
        "why_it_is_the_answer": (
            "Same integration-by-parts identity, same squeeze, and -- decisively -- the same "
            "MECHANISM: it is the NON-VANISHING of the perturbation at the singular point "
            "(`omega(x,0) != 0`) that caps the exponent.  Leg 111's gamma = 3 is the p = 1 "
            "corner of this published phenomenon.  There the window is non-empty but "
            "expensive; here it is empty, and the difference is entirely the trial space."),
    },
]

# The literal sentence, and the queries that went looking for it (novelty log Q4/Q5/Q7).
SENTENCE_SEARCHED_AND_NOT_FOUND = {
    "sentence": ("the exponent needed for damping at the origin equals the exponent at which "
                 "the weighted space stops containing the perturbation, so the admissible "
                 "window has ZERO width"),
    "queries": [
        '"a=0" CLM equation energy method fails no damping weight cannot give damping at '
        'origin scaling exponent 3',
        'gCLM De Gregorio weighted energy estimate weight exponent k must exceed threshold '
        'for damping but weighted norm finite only below same threshold incompatible no '
        'admissible weight',
        'no weighted L2 space can simultaneously give damping at the origin and contain the '
        'perturbation self-similar blowup one-dimensional model obstruction weight exponent '
        'coincide',
    ],
    "on_topic_hits": 0,
    "reading": ("The SENTENCE is unpublished.  The gate does not ask for the sentence -- it "
                "asks whether published work CONTAINS the obstruction `explicitly or as a "
                "special case of a stated more-general result`, and EGM Prop. 2.1 is that "
                "more general result."),
}


# ---------------------------------------------------------------------------
# 2. verbatim presence: re-locate every fragment in the actual PDF text
# ---------------------------------------------------------------------------
def _squash(s):
    """Whitespace-insensitive comparison key.  pdftotext breaks lines mid-sentence and
    pads with -layout columns, so a raw substring test fails on true quotes."""
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
    """Returns (list of per-statement records, source string).  When the PDFs are present
    every fragment is re-located; when they are not, the flags are READ BACK from the
    committed JSON and labelled as such -- never silently defaulted to True."""
    texts, have = {}, {}
    for pid in sorted({s["paper"] for s in LOCATED}):
        t = pdf_text(pid)
        texts[pid] = _squash(t) if t is not None else None
        have[pid] = t is not None

    prior_by_id = {r["id"]: r for r in (prior or {}).get("located", [])}
    recs = []
    for s in LOCATED:
        rec = dict(s)
        hay = texts[s["paper"]]
        if hay is None:
            old = prior_by_id.get(s["id"], {})
            rec["fragment_located"] = old.get("fragment_located")
            rec["fragment_source"] = "read back from committed JSON (PDF absent)"
        else:
            rec["fragment_located"] = _squash(s["fragment"]) in hay
            rec["fragment_source"] = f"recomputed from Papers/{s['paper']}.pdf"
        recs.append(rec)
    src = ("recomputed from Papers/*.pdf" if all(have.values())
           else f"partly read back from JSON; PDFs present: "
                f"{sorted(k for k, v in have.items() if v)}")
    return recs, src


# ---------------------------------------------------------------------------
# 3. the window width as a function of the trial space's vanishing order p
#     -- leg 111's own quadrature, on trial functions leg 111 did not try.
# ---------------------------------------------------------------------------
#
# `admissibility()` in solver/energy_coercivity.py hardwires `sin(theta)`, i.e. p = 1.
# EGM Prop. 2.1's hypothesis is a statement about p, not about the operator.  Membership
# near the origin: integrand ~ theta^(2p - gamma), finite iff gamma < 2p + 1.  Damping:
# D_phi(0) = (3 - gamma)/2 < 0 iff gamma > 3.  So the window is (3, 2p+1), width 2p - 2.
P_LADDER = (1, 2, 3)
GAMMA_PROBES = (3.0, 4.0)
FAMILY = "A"


def norm2_of_power(p, gamma, n_grade, order=12):
    """`|| sin^p theta ||^2_phi` on leg 111's graded mesh.  p = 1 is EXACTLY the integrand
    `solver.energy_coercivity.admissibility` uses, which is what makes it a control."""
    th, qw = graded_quadrature(n_grade=n_grade, order=order)
    return float(np.sum(np.sin(th) ** (2 * p) * weight_values(th, FAMILY, gamma) * qw))


def window_by_trial_space():
    rows = []
    for p in P_LADDER:
        for gamma in GAMMA_PROBES:
            a = norm2_of_power(p, gamma, 24)
            b = norm2_of_power(p, gamma, 48)
            ladder = [norm2_of_power(p, gamma, 24 + i * 12) for i in range(3)]
            inc = [ladder[1] - ladder[0], ladder[2] - ladder[1]]
            rows.append({
                "p": p, "gamma": gamma,
                "membership_threshold_gamma_lt": 2 * p + 1,
                "predicted_convergent": gamma < 2 * p + 1,
                "norm2_coarse": a, "norm2_fine": b,
                "ratio": (b / a) if a > 0 else float("inf"),
                "norm2_ladder": ladder,
                "increments": inc,
                "increment_ratio": (inc[1] / inc[0]) if abs(inc[0]) > 1e-12 else None,
                "measured_convergent": bool(a > 0 and abs(b / a - 1.0) < 1e-6),
            })
    windows = []
    for p in P_LADDER:
        lo, hi = 3.0, float(2 * p + 1)
        windows.append({
            "p": p,
            "damping_needs_gamma_gt": lo,
            "space_needs_gamma_lt": hi,
            "window_width": hi - lo,
            "contains_gamma_4_the_published_exponent": lo < 4.0 < hi,
            "who_lives_here": {
                1: "leg 111's trial basis sin k theta -- ZERO WIDTH, the banked claim",
                2: "exponent-counting proxy for EGM's f'(0) = 0 (NB sin^2 is not odd, so "
                   "this row is arithmetic on the exponent only)",
                3: "sin^3 theta: odd AND f'(0) = 0, so a genuine witness for the MEMBERSHIP "
                   "half of EGM's hypothesis (it does NOT satisfy their further Hf(0) = 0, "
                   "which constrains the coercivity, not the membership)",
            }[p],
        })
    return rows, windows


def leg111_control():
    """The p = 1 column must reproduce leg 111's banked admissibility numbers.  A mismatch
    means this leg is not running leg 111's arithmetic and the comparison is void."""
    if not LEG111.exists():
        return {"available": False}
    d = json.loads(LEG111.read_text())
    out = {"available": True, "source": str(LEG111.relative_to(ROOT)), "checks": []}
    for name, gamma in (("A3", 3.0), ("A4_chen_hou", 4.0)):
        banked = d["admissibility"][name]
        mine_c = norm2_of_power(1, gamma, 24)
        mine_f = norm2_of_power(1, gamma, 48)
        out["checks"].append({
            "weight": name, "gamma": gamma,
            "banked_norm2_coarse": banked["norm2_coarse"],
            "recomputed_norm2_coarse": mine_c,
            "abs_diff_coarse": abs(mine_c - banked["norm2_coarse"]),
            "banked_ratio": banked["ratio"],
            "recomputed_ratio": mine_f / mine_c,
            "rel_diff_ratio": abs(mine_f / mine_c - banked["ratio"]) / banked["ratio"],
            "bit_identical_coarse": mine_c == banked["norm2_coarse"],
        })
    return out


def constant_triangulation():
    """One number, three independent sources.  This is not new mathematics: it is arithmetic
    on leg 111's banked formula against two published constants."""
    d_at_4 = damping_factor_at_origin(FAMILY, 4.0)
    return {
        "quantity": "the coercivity/damping constant at the published weight exponent gamma = 4",
        "leg111_D_phi_at_origin_gamma_4": d_at_4,
        "leg111_formula": "D_phi(0) = (3 - gamma)/2, from solver/energy_coercivity.py",
        "EGM_prop_2_1_constant_at_a_0": -0.5,
        "EGM_locator": "arXiv:1906.05811 Prop. 2.1, the constant -1/2 - C|a| at a = 0",
        "XU_modulated_gap": 0.5,
        "XU_locator": ("arXiv:2607.19762, published modulated spectral gap 1/2; already "
                       "banked as KNOWN_ANSWER_CEILING in solver/energy_coercivity.py"),
        "max_abs_discrepancy": max(abs(d_at_4 - (-0.5)), abs(abs(d_at_4) - 0.5)),
        "reading": ("Leg 111's own damping formula, evaluated at the exponent the "
                    "literature actually uses, returns the literature's own coercivity "
                    "constant to machine zero.  The damping half of the coincidence is not "
                    "merely published -- it is the published constant."),
    }


# ---------------------------------------------------------------------------
def build():
    prior = json.loads(OUT.read_text()) if OUT.exists() else None
    located, located_src = relocate(prior)
    rows, windows = window_by_trial_space()
    return {
        "leg": 141,
        "route": "WEL",
        "kind": "literature",
        "gate": GATE,
        "gate_answer": "YES",
        "gate_answer_branch_verbatim": (
            "The third realization's death was pre-empted in the literature. Record the "
            "located statement with hypotheses verbatim; cap the finding's novelty "
            "accordingly wherever it is cited."),
        "claim_under_test": CLAIM_UNDER_TEST,
        "claim_source": "capabilities.py, the solver/energy_coercivity.py row (leg 111)",
        "located": located,
        "located_source": located_src,
        "sentence_searched_and_not_found": SENTENCE_SEARCHED_AND_NOT_FOUND,
        "window_by_trial_space": {
            "definition": ("membership near the origin: integrand ~ theta^(2p - gamma), "
                           "finite iff gamma < 2p + 1.  damping: D_phi(0) = (3 - gamma)/2 "
                           "< 0 iff gamma > 3.  window = (3, 2p+1), width 2p - 2."),
            "scope_of_this_check": (
                "It decides the MEMBERSHIP half only -- exactly the half leg 111's "
                "`admissibility()` gate decides, and exactly the half that makes leg 111's "
                "window zero-width.  EGM's further hypothesis Hf(0) = 0 constrains the "
                "COERCIVITY, not the membership, and is not tested here; no coercivity "
                "gap is recomputed by this leg on any trial space."),
            "family": FAMILY,
            "measurements": rows,
            "windows": windows,
        },
        "leg111_instrument_control": leg111_control(),
        "constant_triangulation": constant_triangulation(),
        "what_is_capped": (
            "Leg 111's MEASUREMENTS stand untouched and are not re-run here.  What does not "
            "survive is the READING of them as a candidate structural obstruction to "
            "Chen-Hou-style weighted-energy certification on this operator class: the window "
            "is zero-width on the UNCONSTRAINED odd-sine trial space, which is not the space "
            "the published method is run in, and that method's first hypothesis is the one "
            "that reopens it."),
        "what_is_NOT_claimed": (
            "No ban is lifted, no route promoted, no link of L1 -> L4 moved.  EGM's positive "
            "gap is on the a = 0 CLM object -- this repository's friendliest substrate, whose "
            "blowup is explicit (Constantin-Lax-Majda 1985) -- and not on "
            "HL_S2_nonsymmetric.  L1 stays measured-dead in all three realizations."),
        "novelty_log": "writeup/novelty/leg_141.md",
        "journal": "experiments/journal/leg_141.md",
        "figure": "none -- no measurement of a curve (the 'no measurement, no figure' convention)",
    }


def main():
    data = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n")

    print("P2 Route-WEL v1 -- is leg 111's zero-width window published?  leg 141")
    print("GATE:", GATE)
    print("ANSWER:", data["gate_answer"])
    print()
    print("located statements  (" + data["located_source"] + "):")
    for s in data["located"]:
        flag = {True: "LOCATED", False: "NOT FOUND", None: "unknown"}[s["fragment_located"]]
        print(f"  {s['id']:<14} {s['paper']:<11} {s['locator'][:38]:<38} {flag}")
        print(f"                 supplies: {s['supplies']}")
    print()
    print("the SENTENCE itself: 3 queries aimed at it, "
          f"{data['sentence_searched_and_not_found']['on_topic_hits']} on-topic hits")
    print()
    print("window (3, 2p+1) as a function of the trial space's vanishing order p:")
    for w in data["window_by_trial_space"]["windows"]:
        print(f"  p={w['p']}  damping needs gamma > {w['damping_needs_gamma_gt']:.0f}, "
              f"space needs gamma < {w['space_needs_gamma_lt']:.0f}  ->  width "
              f"{w['window_width']:.0f}   gamma=4 inside: "
              f"{w['contains_gamma_4_the_published_exponent']}")
        print(f"        {w['who_lives_here']}")
    print()
    print("measured, on leg 111's own graded quadrature (n_grade 24 -> 48):")
    print(f"  {'p':>2} {'gamma':>6} {'norm2(24)':>14} {'ratio':>14}  convergent")
    for r in data["window_by_trial_space"]["measurements"]:
        print(f"  {r['p']:>2} {r['gamma']:>6.1f} {r['norm2_coarse']:>14.6e} "
              f"{r['ratio']:>14.6e}  {r['measured_convergent']}")
    print()
    c = data["leg111_instrument_control"]
    if c.get("available"):
        print("instrument control -- p=1 against leg 111's banked admissibility:")
        for ch in c["checks"]:
            print(f"  {ch['weight']:<12} gamma={ch['gamma']:.0f}  "
                  f"abs diff norm2 {ch['abs_diff_coarse']:.3e}  "
                  f"rel diff ratio {ch['rel_diff_ratio']:.3e}  "
                  f"bit-identical {ch['bit_identical_coarse']}")
    print()
    t = data["constant_triangulation"]
    print("one constant, three sources:")
    print(f"  leg 111  D_phi(0) at gamma=4      {t['leg111_D_phi_at_origin_gamma_4']:+.6f}")
    print(f"  EGM      Prop. 2.1 at a=0         {t['EGM_prop_2_1_constant_at_a_0']:+.6f}")
    print(f"  Xu       modulated spectral gap   {t['XU_modulated_gap']:+.6f}  (magnitude)")
    print(f"  max abs discrepancy               {t['max_abs_discrepancy']:.3e}")
    print()
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
