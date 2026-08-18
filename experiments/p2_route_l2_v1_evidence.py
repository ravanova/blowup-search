#!/usr/bin/env python3
"""Leg 397 (unit L2', lane L) -- STEP 3 of 3: build and CHECK the gate artefact.

This script is the reason the leg-397 write-up may state a number.  It does three
things, and it exits non-zero if any of them disagrees (lesson 68):

  1. RE-DERIVES LEG 381's BILL from the banked artefact writeup/data/p2_route_cloc_v1.json
     -- never from prose anywhere in the repository (SS0.2(c)).  If the artefact and the
     journal disagree, the artefact wins and the disagreement is banked.

  2. EXTRACTS EVERY VERBATIM QUOTE MECHANICALLY from the fetched full text, by an
     (start-anchor, end-anchor) pair, and re-finds it as an exact substring.  Nothing in
     the artefact is transcribed by hand: a quote that cannot be re-found mechanically is
     NOT quoted (SS2.2, per-quote control).  This also means the quote in the artefact is
     the extractor's own output, so it cannot drift from the source.

  3. CHECKS THE SS2.2 SEARCH CONTROLS FIRED before any zero in this leg is allowed to
     count, and re-states the arithmetic that decides each verdict.

    python3 experiments/p2_route_l2_v1_evidence.py

Papers/ is gitignored.  Run experiments/p2_route_l2_v1_fetch.py first.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAPERS = ROOT / "Papers"
DATA = ROOT / "writeup" / "data"
BILL_SRC = DATA / "p2_route_cloc_v1.json"
SEARCH_SRC = DATA / "p2_route_l2_search_v1.json"
FULLTEXT_SRC = DATA / "p2_route_l2_fulltext_v1.json"
OUT = DATA / "p2_route_l2_decay_v1.json"

FAILURES: list[str] = []


def check(cond: bool, msg: str) -> bool:
    if not cond:
        FAILURES.append(msg)
    return cond


def flat(aid: str) -> str:
    """Whitespace-normalised full text.  pdftotext -layout inserts column padding and
    hard line breaks inside sentences; normalising is what makes a sentence-level quote
    re-findable at all."""
    return " ".join((PAPERS / f"{aid}.txt").read_text(errors="replace").split())


def quote(aid: str, start: str, end: str) -> dict:
    """Extract the verbatim span from `start` to the END of `end`.  Both anchors must be
    present, `end` must follow `start`, and both must be UNIQUE enough that the extracted
    span re-finds itself.  Otherwise this is banked as NOT_QUOTABLE and never quoted."""
    t = flat(aid)
    i = t.find(start)
    if i < 0:
        FAILURES.append(f"{aid}: start anchor not found: {start!r}")
        return {"status": "NOT_QUOTABLE", "reason": "start anchor not found", "anchor": start}
    j = t.find(end, i)
    if j < 0:
        FAILURES.append(f"{aid}: end anchor not found after start: {end!r}")
        return {"status": "NOT_QUOTABLE", "reason": "end anchor not found", "anchor": end}
    span = t[i:j + len(end)]
    check(t.count(span) == 1, f"{aid}: extracted span is not unique in the text")
    return {"status": "VERBATIM", "text": span, "chars": len(span),
            "sha256_12": hashlib.sha256(span.encode()).hexdigest()[:12]}


# ---------------------------------------------------------------------------
# 1. THE BILL, re-derived from leg 381's artefact
# ---------------------------------------------------------------------------
def read_bill() -> dict:
    d = json.loads(BILL_SRC.read_text())
    check(d["leg"] == 381, "p2_route_cloc_v1.json is not leg 381")
    b = d["check_B3_Lp_thresholds"]
    c2 = d["check_C2_critical_L3_tail_is_log_divergent_at_alpha_1"]
    inc = c2["increment_per_decade"]
    bill = {
        "source_artefact": BILL_SRC.name,
        "source_leg": d["leg"],
        "source_route": d["route"],
        "source_self_hash": d["self_hash"],
        "L2_threshold_alpha": b["L2_threshold_alpha"],
        "L3_threshold_alpha": b["L3_threshold_alpha"],
        "banked_type_I_alpha": b["banked_type_I_alpha"],
        "deficit_to_L2_in_exponent": b["deficit_to_L2_in_exponent"],
        "required_over_available_exponent_ratio": b["required_over_available_exponent_ratio"],
        "type_I_source": b["type_I_source"],
        "critical_L3_tail_cubed_increment_per_decade": inc[0],
        "critical_L3_tail_cubed_increment_spread": c2["increment_per_decade_spread"],
        "tail_L3_norm_2_decades": c2["rows"][0]["tail_L3_norm"],
        "tail_L3_norm_10_decades": c2["rows"][-1]["tail_L3_norm"],
        "bogovskii_corrector_L2_rho_exponent_at_alpha_1":
            d["check_C_cutoff_magnitudes"]["by_alpha"]["alpha=1.0"]
             ["measured_rho_exponents"]["bogovskii_corrector_L2_scale"],
        "tail_L3_norm_rho_exponent_at_alpha_1":
            d["check_C_cutoff_magnitudes"]["by_alpha"]["alpha=1.0"]
             ["measured_rho_exponents"]["tail_L3_norm"],
    }
    # the three arithmetic facts the whole leg turns on
    check(abs((bill["L2_threshold_alpha"] - bill["banked_type_I_alpha"])
              - bill["deficit_to_L2_in_exponent"]) < 1e-12,
          "deficit != L2_threshold - banked_type_I")
    check(bill["L2_threshold_alpha"] > bill["L3_threshold_alpha"],
          "L2 threshold is not strictly above the L3 threshold")
    check(abs(bill["banked_type_I_alpha"] - bill["L3_threshold_alpha"]) < 1e-12,
          "the banked available alpha is not EXACTLY the L3 threshold")
    check(round(bill["critical_L3_tail_cubed_increment_per_decade"], 3) == 326.875,
          "the banked L3-tail increment per decade is not 326.875")
    # SS1's structural fact, re-derived here rather than asserted:
    # any alpha paying the L2 bill is strictly inside the L3 region.
    bill["any_alpha_paying_the_L2_bill_is_strictly_inside_L3"] = bool(
        bill["L2_threshold_alpha"] > bill["L3_threshold_alpha"])
    bill["margin_by_which_paying_the_bill_overshoots_L3"] = (
        bill["L2_threshold_alpha"] - bill["L3_threshold_alpha"])
    return bill


def read_controls() -> dict:
    s = json.loads(SEARCH_SRC.read_text())
    c = s["controls"]
    check(c["instrument_is_live"], "SS2.2 controls did not both fire -- every zero is void")
    nonok = [q["label"] for q in s["queries"] if q.get("status") != "OK"]
    return {
        "positive_control_total": c["positive_control_total"],
        "negative_control_total": c["negative_control_total"],
        "instrument_is_live": c["instrument_is_live"],
        "opensearch_namespace_served": c["opensearch_namespace_served"],
        "leg_387_namespace_bug_would_have_voided_this_leg": c["namespace_served_is_1_1"],
        "queries_run": len(s["queries"]),
        "queries_not_OK": nonok,
        "throttled": [q["label"] for q in s["queries"] if q.get("status") == "THROTTLED"],
        "unreachable": [q["label"] for q in s["queries"] if q.get("status") == "UNREACHABLE"],
        "instrumented_zeros": [
            {"label": q["label"], "query": q["query"], "total_results": 0}
            for q in s["queries"]
            if q.get("status") == "OK" and q.get("total_results") == 0
            and q["label"] != "NEGATIVE_CONTROL"],
    }


# ---------------------------------------------------------------------------
# 3. THE TECHNIQUE TABLE.  One object per technique.  Exactly one
#    `decisive_hypothesis` each (SS3.2), quoted mechanically, located by
#    section/page, with exactly one verdict from SS3.2's fixed list.
# ---------------------------------------------------------------------------
# SS3.3, restated in code so the pass/fail cannot be relaxed in prose: leg 381's
# bill is PAID only by a CERTIFIED two-sided enclosure [a_lo, a_hi] on ROUTE 4's
# OWN profile with a_lo > 1.5, plus a cutoff controlled in a scaling-invariant
# norm.  No technique below is claimed to do any of the three.
BILL_PAID_BY_ANY = False

TECHNIQUES = [
 dict(
  tid="T1a", family="F1 rigidity by integrability of the profile",
  name="Necas-Ruzicka-Sverak: no nontrivial Leray backward self-similar profile in L^3",
  citation="J. Necas, M. Ruzicka, V. Sverak, 'On Leray's self-similar solutions of the "
           "Navier-Stokes equations', Acta Math. 176 (1996) 283-294",
  primary_text="UNREACHABLE -- pre-arXiv, journal-only; declared UNREACHABLE IN ADVANCE by SS2.1",
  quoted_from=("SECONDARY", "2607.09619", "Pineau-Vicol, Sec. 1.1 'Backwards self-similar "
                                          "solutions', p. 2"),
  hypotheses=["u is a solution of 3D incompressible Navier-Stokes",
              "u is BACKWARD GLOBALLY self-similar: u(x,t) = (-t)^{-1/2} U(x/sqrt(-t)) for ALL lambda>0",
              "the profile U lies in L^3(R^3)"],
  decisive_hypothesis="U in L^3(R^3)",
  quote_spec=("2607.09619", "was answered in the negative by", "then U ≡ 0."),
  object_status="FAILS",
  why="At the banked alpha = 1 the profile lies in L^{3,infty} but NOT in L^3: the artefact's "
      "L3_threshold_alpha is 1.0 and the banked available exponent is 1.0 EXACTLY, i.e. the "
      "object sits on the borderline of this hypothesis and outside it.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="It is a triviality theorem. It CONSUMES decay and supplies none. Worse for "
                   "the bill: its hypothesis is IMPLIED by any alpha > 1, so supplying alpha > 1.5 "
                   "would satisfy it and force U == 0.",
  verdict="FAILS"),

 dict(
  tid="T1b", family="F1 rigidity by integrability of the profile",
  name="Tsai: triviality for L^p profiles, p in (3, infinity], and under local energy estimates",
  citation="T.-P. Tsai, 'On Leray's self-similar solutions of the Navier-Stokes equations "
           "satisfying local energy estimates', Arch. Rational Mech. Anal. 143 (1998) 29-51",
  primary_text="UNREACHABLE -- pre-arXiv, journal-only; declared UNREACHABLE IN ADVANCE by SS2.1",
  quoted_from=("SECONDARY", "2607.09619", "Pineau-Vicol, Sec. 1.1, p. 2"),
  hypotheses=["backward GLOBALLY self-similar (invariance for every lambda > 0)",
              "profile U in L^p(R^3) for some p in (3, infinity], OR the solution satisfies "
              "only local energy estimates"],
  decisive_hypothesis="the solution is backward GLOBALLY self-similar (invariant for EVERY "
                      "lambda>0), not merely discretely self-similar at one fixed lambda",
  quote_spec=("2607.09619", "established the same conclusion for profiles", "only local energy estimates."),
  object_status="FAILS-BY-CONSTRUCTION",
  why="Route 4's object is DISCRETELY self-similar at a single fixed lambda >> 1 (the artefact "
      "checks the DSS symmetry at lambda = 1.7, period 1.0612565021243408, to 1.14e-15). It is "
      "not invariant for every lambda, so Tsai's ansatz does not hold for it. NOTE the sharpness: "
      "at alpha = 1 the object DOES satisfy Tsai's integrability clause (U in L^p for every p>3) "
      "-- being DSS rather than SS is the ONLY thing that saves it from this theorem.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="A triviality theorem; supplies no decay exponent.",
  verdict="FAILS-BY-CONSTRUCTION"),

 dict(
  tid="T2a", family="F2 DSS-specific rigidity and a-priori decay",
  name="Chae-Wolf Theorem 1.1: a-priori decay of any backward lambda-DSS solution",
  citation="D. Chae, J. Wolf, 'Removing discretely self-similar singularities for the 3D "
           "Navier-Stokes equations', arXiv:1610.09464v2",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1610.09464", "Theorem 1.1, p. 2"),
  hypotheses=["u in C((-inf,0); L^p(R^3)) for some 3 <= p < +infinity",
              "u in C^infinity(Q), Q = R^3 x (-inf,0)",
              "u is lambda-DSS for some lambda in (1, +infinity) -- NO restriction on lambda"],
  decisive_hypothesis="u in C((-inf,0); L^p(R^3)) for some 3 <= p < +infinity",
  quote_spec=("1610.09464", "For 3 ≤ p < +∞ let u", "∀ (x, t) ∈ Q."),
  object_status="SATISFIED",
  why="At alpha = 1 the profile is in L^p(R^3) for every p > 3 (the far-field integral "
      "int r^{-p} r^2 dr converges iff p > 3), and ||u(t)||_p = (-t)^{(3-p)/(2p)} ||U||_p is "
      "continuous in t. This is the ONE technique read whose decisive hypothesis this object "
      "meets -- and it is the technique that BANKED the deficit-bearing number.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Its conclusion (1.3) IS the banked alpha = 1.0. It is a bound of the exact "
                   "shape C/(sqrt(-t)+|x|) and delivers the exponent 1, never more.",
  verdict="SATISFIED"),

 dict(
  tid="T2b", family="F2 DSS-specific rigidity and a-priori decay",
  name="Chae-Wolf Theorem 1.3: removal of the backward lambda-DSS singularity for lambda near 1",
  citation="D. Chae, J. Wolf, arXiv:1610.09464v2",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1610.09464", "Theorem 1.3, p. 3"),
  hypotheses=["u in C^infinity(Q) is a lambda-DSS solution",
              "|u(x,t)| <= C_*/(sqrt(-t)+|x|) on Q",
              "lambda in (1, lambda_*) with lambda_* = lambda_*(C_*) > 1"],
  decisive_hypothesis="lambda in (1, lambda_*), i.e. the DSS scaling factor is close to 1",
  quote_spec=("1610.09464", "For evrey C∗ > 0 there exists", "Then u ≡ 0."),
  object_status="FAILS",
  why="Route 4's object is specified at lambda >> 1 (CLAY_OBLIGATIONS 'The target, as "
      "specified'), and lambda_* is not quantified in the source. This hypothesis fails IN THE "
      "OBJECT'S FAVOUR: it is exactly why the target was placed at large lambda.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="A triviality theorem; supplies no decay exponent.",
  verdict="FAILS"),

 dict(
  tid="T2c", family="F2 DSS-specific rigidity and a-priori decay",
  name="Chae-Wolf Remark 1.2: a DSS solution with an L^3 profile is FULLY REGULAR "
       "(via Escauriaza-Seregin-Sverak backward uniqueness)",
  citation="D. Chae, J. Wolf, arXiv:1610.09464v2, Remark 1.2, citing "
           "L. Escauriaza, G. Seregin, V. Sverak",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1610.09464", "Remark 1.2, p. 2"),
  hypotheses=["u in C((-inf,0); L^3(R^3))",
              "u is discretely self-similar -- NO restriction on lambda"],
  decisive_hypothesis="u in C((-inf,0); L^3(R^3)), equivalently U in L^3(R^3), equivalently "
                      "a far-field decay exponent alpha STRICTLY GREATER THAN 1",
  quote_spec=("1610.09464", "If u ∈ C((−∞, 0); L3 (R3 ))", "full regularity u in Q."),
  object_status="FAILS",
  why="THIS IS THE LOAD-BEARING ENTRY OF THE WHOLE LEG. At the banked alpha = 1.0 the "
      "hypothesis fails (L^{3,infty}, not L^3) and the object survives. But leg 381's bill asks "
      "for alpha > 1.5, and 1.5 > 1.0 = the artefact's own L3_threshold_alpha, so ANY alpha "
      "paying the bill SATISFIES this hypothesis -- whose conclusion is full regularity of u in "
      "Q, i.e. NO SINGULARITY AT ALL. Paying the bill destroys the object the bill is for. "
      "Note this clause carries NO restriction on lambda, so the object's lambda >> 1 does not "
      "save it here the way it saves it from Theorem 1.3.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="It supplies no decay. It is the theorem that makes alpha > 1.5 FATAL rather "
                   "than merely unavailable.",
  verdict="FAILS"),

 dict(
  tid="T2d", family="F2 DSS-specific rigidity and a-priori decay",
  name="Pineau-Vicol Theorem 1.6 / 1.7: Liouville for (rotated) DSS under a Type I bound",
  citation="B. Pineau, V. Vicol, 'On rotated backwards self-similar solutions of the "
           "incompressible 3D Navier-Stokes equations', arXiv:2607.09619v2 (6 Aug 2026)",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "2607.09619", "Theorem 1.6, Sec. 1.3"),
  hypotheses=["u solves 3D incompressible Navier-Stokes on R^3 x [-1,0)",
              "u satisfies the Type I upper bound |u(x,t)| <= C_{U,0}(|x|+sqrt(-t))^{-1}",
              "u is backward globally DSS with profile U in C^2(R^3 x [0,S]), S = 2 log(lambda)",
              "1 < lambda < lambdabar(C_{U,0})"],
  decisive_hypothesis="1 < lambda < lambdabar(C_{U,0}), i.e. the DSS scaling factor is close to 1",
  quote_spec=("2607.09619", "Main result for DSS solutions", "then U ≡ 0."),
  object_status="FAILS",
  why="Same failure as T2b and for the same reason: route 4's object is at lambda >> 1. This is "
      "the 2026 state of the art on this hypothesis and it has NOT been removed -- the paper's "
      "new weighted-L^2 method removes the maximum-principle dependence, not the lambda-near-1 "
      "restriction. WARNING ON NOTATION: this paper's alpha is an ANGULAR SPEED, not a decay "
      "exponent; leg 397's alpha is the decay exponent throughout.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="A Liouville theorem; supplies no decay exponent.",
  verdict="FAILS"),

 dict(
  tid="T2e", family="F2 DSS-specific rigidity and a-priori decay",
  name="Pineau-Vicol Sec. 1.2: the INDEPENDENT statement that faster decay implies triviality",
  citation="B. Pineau, V. Vicol, arXiv:2607.09619v2, Sec. 1.2 ('Why is Conjecture 1.1 open')",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "2607.09619", "Sec. 1.2, p. 4"),
  hypotheses=["the profile decays fast enough that U in L^3(R^3)"],
  decisive_hypothesis="U in L^3(R^3) -- i.e. decay strictly faster than the borderline rate",
  quote_spec=("2607.09619", "Had we assumed that the profile",
              "but not membership in the scaling-critical space L3"),
  object_status="FAILS",
  why="Banked as a SECOND, INDEPENDENT located statement of T2c's mechanism, by a different "
      "author group four years later, in the authors' own words: faster decay => L^3 => "
      "Escauriaza-Seregin-Sverak => regularity => triviality. They call the borderline rate 'the "
      "genuine difficulty'. For leg 397 that means the deficit of 0.5 is not a gap in the "
      "literature; it is a step into a region the literature has emptied.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="It supplies no decay. It is the second proof that alpha > 1 is fatal.",
  verdict="FAILS"),

 dict(
  tid="T3a", family="F3 local-energy / local-Leray construction of SS and DSS solutions",
  name="Bradshaw-Phelps: spatial decay rates for DSS Navier-Stokes flows",
  citation="Z. Bradshaw, P. Phelps, 'Spatial decay of discretely self-similar solutions to "
           "the Navier-Stokes equations', arXiv:2202.08352v1",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "2202.08352", "Sec. 1, footnote 1, p. 2"),
  hypotheses=["u is a FORWARD DSS local energy solution on R^3 x (0,infinity)",
              "u_0 in L^q_loc(R^3 \\ {0}) for 3 < q <= infinity, or Holder-regular away from 0",
              "the estimates hold in the region of regularity |x| >= R_0 sqrt(t)"],
  decisive_hypothesis="the self-similarity is FORWARD in time (u on R^3 x (0,infinity), from "
                      "initial data), not BACKWARD (u on R^3 x (-infinity,0), toward a singularity)",
  quote_spec=("2202.08352", "This is a forward notion", "covered in the literature"),
  object_status="FAILS-BY-CONSTRUCTION",
  why="Route 4's object is BACKWARD DSS. Recorded additionally, because it is the strongest "
      "decay statement located anywhere in this leg: even in the forward theory, where far more "
      "is known, the decay supplied for the FULL field u is |x|^{-1}, i.e. alpha = 1 again; only "
      "the NONLINEAR PART utilde = u - e^{t Delta}u_0 decays faster. The linear part inherits the "
      "(-1)-homogeneity of DSS data, and that is what pins the exponent at 1.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="For the full field it supplies exactly alpha = 1 and the authors expect that "
                   "to be optimal; the faster rates are for u - e^{tDelta}u_0, not for u.",
  verdict="FAILS-BY-CONSTRUCTION"),

 dict(
  tid="T3b", family="F3 local-energy / local-Leray construction of SS and DSS solutions",
  name="Jia-Sverak Theorem 1.1: existence of forward self-similar solutions for large "
       "(-1)-homogeneous data",
  citation="H. Jia, V. Sverak, 'Local-in-space estimates near initial time for weak solutions "
           "of the Navier-Stokes equations and forward self-similar solutions', arXiv:1204.0529v1",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1204.0529", "Theorem 1.1, p. 1"),
  hypotheses=["u_0 is scale-invariant, i.e. (-1)-homogeneous",
              "u_0 is locally Holder continuous in R^3 \\ {0}",
              "div u_0 = 0 in R^3",
              "the Cauchy problem is solved FORWARD from t = 0"],
  decisive_hypothesis="u_0 is scale-invariant ((-1)-homogeneous) initial data for a FORWARD "
                      "Cauchy problem",
  quote_spec=("1204.0529", "u0 is scale-invariant and locally", "div u0 = 0 in R3 ."),
  object_status="FAILS-BY-CONSTRUCTION",
  why="Forward, and it is an EXISTENCE framework, not a conversion: the solutions it builds are "
      "themselves scale-invariant and infinite-energy. Banked additionally because these authors "
      "named leg 397's exact move as future work in 2012 and did not carry it out here.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Constructs infinite-energy scale-invariant solutions; supplies no decay "
                   "exponent above the (-1)-homogeneity it starts from.",
  verdict="FAILS-BY-CONSTRUCTION",
  extra_quote_spec=("1204.0529", "by a suitable truncation of u0", "in future work.")),

 dict(
  tid="T4a", family="F4 cut-off-then-perturb finite-energy blow-up for a fluid equation",
  name="Elgindi: C^{1,alpha} Euler self-similar blow-up, and its localisation clause",
  citation="T. M. Elgindi, 'Finite-time singularity formation for C^{1,alpha} solutions to the "
           "incompressible Euler equations on R^3', arXiv:1904.04795",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1904.04795", "Remark 1.4, p. 4"),
  hypotheses=["the equation is incompressible EULER (no viscosity)",
              "the velocity is C^{1,alpha} with alpha small, NOT C^infinity",
              "the blow-up is stable to the perturbations that make the profile compactly supported"],
  decisive_hypothesis="the blow-up is stable to the class of perturbations that render the "
                      "profile compactly supported",
  quote_spec=("1904.04795", "these solutions can be localized", "in finite time [19]."),
  object_status="FAILS-BY-CONSTRUCTION",
  why="Euler, not Navier-Stokes; and the whole construction lives in C^{1,alpha}, which the "
      "same paper's Remark 1.5 says is essential -- the C^infinity version of the same "
      "symmetry class is globally regular. Clay condition (6) demands p, u in C^infinity. "
      "The stability CLAUSE is named here and LEFT to unit L3' per SS0.3.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="It consumes localisability; it supplies no decay exponent for an "
                   "incompressible Navier-Stokes DSS profile.",
  verdict="FAILS-BY-CONSTRUCTION",
  extra_quote_spec=("1904.04795", "It is known that sufficiently smooth", "are globally regular")),

 dict(
  tid="T4b", family="F4 cut-off-then-perturb finite-energy blow-up for a fluid equation",
  name="Elgindi-Ghoul-Masmoudi Sec. 2.6: how the self-similar profile is made compactly "
       "supported with finite energy",
  citation="T. M. Elgindi, T.-E. Ghoul, N. Masmoudi, 'On the Stability of Self-similar Blow-up "
           "for C^{1,alpha} Solutions to the Incompressible Euler Equations on R^3', "
           "arXiv:1910.14071v1",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1910.14071", "Sec. 2.6 'Solutions with compactly supported vorticity "
                                        "and finite energy', p. 12"),
  hypotheses=["there exists eps_0 in H_k of SMALL NORM with F + eps_0 compactly supported",
              "the profile F DECAYS FASTER THAN eps_0 NEEDS TO",
              "the equation is incompressible Euler in C^{1,alpha}"],
  decisive_hypothesis="'F decays faster than eps_0 needs to' -- the profile must decay STRICTLY "
                      "FASTER than the norm in which the cut-off perturbation is measured requires",
  quote_spec=("1910.14071", "In view of Theorem 2, to get",
              "since F decays faster than ε0 needs to."),
  object_status="FAILS",
  why="This is leg 381's bill, stated in one sentence by the technique's own authors, and it is "
      "the hypothesis this object measurably violates. Route 4's profile does NOT decay faster "
      "than the cut-off perturbation needs: the artefact measures the discarded tail's "
      "scaling-critical L^3 norm with a rho-exponent of 1.2768e-05 (i.e. it does not decay at "
      "all) and its cube growing by a constant 326.875 per decade of window, without bound.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="It is a CONSUMER of decay, not a supplier. It requires more decay than is "
                   "available and provides none.",
  verdict="FAILS"),

 dict(
  tid="T4c", family="F4 cut-off-then-perturb finite-energy blow-up for a fluid equation",
  name="Chen-Hou Sec. 8.6: finite-time blow-up with finite-energy velocity by truncating the "
       "far field of the approximate steady state",
  citation="J. Chen, T. Y. Hou, 'Finite time blowup of 2D Boussinesq and 3D Euler equations "
           "with C^{1,alpha} velocity and boundary', arXiv:1910.00173v4",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1910.00173", "Remark 8.1 and Sec. 8.6.2, p. 51-52"),
  hypotheses=["2D Boussinesq / 3D Euler with boundary, C^{1,alpha} velocity, alpha small",
              "a nonlinear stability bootstrap (8.27)/(8.29) controlling the perturbation",
              "the truncation must be a SMALL perturbation in the bootstrap's own energy E",
              "smallness is supplied by the parameter alpha, NOT by the cut-off radius lambda"],
  decisive_hypothesis="the far-field truncation must be a small perturbation in the norm in "
                      "which the nonlinear stability estimate closes",
  quote_spec=("1910.00173", "The crucial nonlinear estimate", "to obtain initial data with finite energy."),
  object_status="FAILS-BY-CONSTRUCTION",
  why="Boussinesq/Euler with a boundary, in C^{1,alpha} -- not incompressible Navier-Stokes on "
      "R^3 in C^infinity. Recorded because of a structural fact worth having: Chen-Hou's own "
      "truncation error does NOT shrink as the cut-off radius grows either ('the initial "
      "perturbation is of size C alpha^{5/2} even for extremely large lambda'); they buy "
      "smallness from a SEPARATE parameter alpha. Route 4's object is a fixed profile of "
      "Navier-Stokes at fixed viscosity and carries no such parameter. The nonlinear STABILITY "
      "clause is named here and LEFT to unit L3' per SS0.3.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Consumes smallness, supplies no decay exponent.",
  verdict="FAILS-BY-CONSTRUCTION"),

 dict(
  tid="T5", family="F5 finite-energy blow-up by self-similar profile + cutoff + finite speed "
                   "of propagation",
  name="Merle-Raphael-Rodnianski-Szeftel: implosion for a three-dimensional compressible fluid",
  citation="F. Merle, P. Raphael, I. Rodnianski, J. Szeftel, 'On the implosion of a three "
           "dimensional compressible fluid', arXiv:1912.11009v2",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "1912.11009", "Sec. 1.6 Remark 3 ('The Euler case')"),
  hypotheses=["the equation is COMPRESSIBLE Euler / Navier-Stokes (density present)",
              "for the localisation-by-cutoff variant: FINITE SPEED OF PROPAGATION",
              "the profile is reconnected to rapidly decaying functions outside |x| > 5"],
  decisive_hypothesis="FINITE SPEED OF PROPAGATION of the underlying equation",
  quote_spec=("1912.11009", "a direct analysis of the dynamical",
              "cannot be applied in the Navier-Stokes case"),
  object_status="FAILS-BY-CONSTRUCTION",
  why="The technique's own authors state in one sentence that the localise-by-finite-speed "
      "procedure 'cannot be applied in the Navier-Stokes case'. Incompressible Navier-Stokes on "
      "R^3 is parabolic with a nonlocal pressure: infinite speed of propagation. Their own "
      "successful localisation is instead a RECONNECTION outside |x| > 5 of a COMPRESSIBLE "
      "profile, which they describe as 'not subtle'.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Supplies no decay exponent for an incompressible Navier-Stokes profile; the "
                   "reconnection is an operation on a compressible density profile.",
  verdict="FAILS-BY-CONSTRUCTION",
  extra_quote_spec=("1912.11009", "For |x| > 5 we then reconnect", "solutions of finite energy.")),

 dict(
  tid="T6", family="F6 truncation of a self-similar profile under a comparison/maximum principle",
  name="Giga-Kohn (semilinear heat): asymptotically self-similar blow-up via a comparison "
       "principle -- read for the STRUCTURAL hypothesis only",
  citation="Y. Giga, R. V. Kohn, 'Asymptotically self-similar blow-up of semilinear heat "
           "equations', Comm. Pure Appl. Math. 38 (1985) 297-319; and CPAM 42 (1989) 845-884",
  primary_text="UNREACHABLE -- pre-arXiv, journal-only; declared UNREACHABLE IN ADVANCE by SS2.1. "
               "The arXiv query all:'asymptotically self-similar' AND all:'semilinear heat "
               "equation' returned an INSTRUMENTED ZERO with both SS2.2 controls live.",
  quoted_from=("SECONDARY", "2607.09619", "Pineau-Vicol Sec. 1.1, p. 2 -- for the Navier-Stokes "
                                          "analogue of the structural hypothesis and where it breaks"),
  hypotheses=["a scalar equation possessing a MAXIMUM / COMPARISON PRINCIPLE",
              "a supersolution to compare the profile against"],
  decisive_hypothesis="the existence of a scalar quantity satisfying a MAXIMUM PRINCIPLE against "
                      "which the profile can be compared",
  quote_spec=("2607.09619", "was answered in the negative by", "radial supersolutions of (1.5)."),
  object_status="FAILS-BY-CONSTRUCTION",
  why="3D incompressible Navier-Stokes has no maximum principle for the velocity. The one "
      "scalar substitute in the literature is the Bernoulli head-pressure Pi = P + |U|^2/2 + "
      "(y.U)/2, and the located source shows Pi obeys an ELLIPTIC inequality only in the "
      "EXACTLY self-similar class (time-independent profile). Route 4's object is DSS: its "
      "profile U(y,s) is s-periodic with period 2 log(lambda) = 1.0612565021243408, so the "
      "Bernoulli equation is parabolic and the comparison argument does not close. This is the "
      "structural reason the DSS case is open where the SS case is not.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Supplies triviality under a comparison principle, never a decay exponent.",
  verdict="FAILS-BY-CONSTRUCTION"),

 dict(
  tid="T7", family="F7 divergence-correction after a cutoff (Bogovskii)",
  name="Bogovskii's right inverse of the divergence",
  citation="M. E. Bogovskii, 'Solution of the first boundary value problem for the equation of "
           "continuity of an incompressible medium', Dokl. Akad. Nauk SSSR 248 (1979) 1037-1040",
  primary_text="UNREACHABLE -- pre-arXiv, journal-only; declared UNREACHABLE IN ADVANCE by SS2.1",
  quoted_from=("SECONDARY", "1103.3718", "R. G. Duran, arXiv:1103.3718, Sec. 3, p. 7-8"),
  hypotheses=["Omega is a BOUNDED domain",
              "Omega is STAR-SHAPED with respect to a ball B of radius rho",
              "the constant C_{div,Omega} in ||Du||_{L^2} <= C ||f||_{L^2} depends on the "
              "aspect ratio R/rho and CANNOT be bounded independently of it"],
  decisive_hypothesis="the estimate controls only the GRADIENT of the corrector, with a constant "
                      "fixed by the domain's aspect ratio -- it supplies no decay and no control "
                      "of the corrector itself in a scaling-invariant norm",
  quote_spec=("1103.3718", "It is known that the constant cannot", "ratio R/ρ."),
  object_status="FAILS",
  why="On the cut-off annulus the aspect ratio is scale-invariant, so the H^1 bound is exactly "
      "the divergence defect -- which is what the artefact records (bogovskii_corrector_H1_scale "
      "equals divergence_defect_L2 identically in every row). The corrector's own L^2 scale then "
      "grows: the artefact measures its rho-exponent at alpha = 1 as +0.5004 against a predicted "
      "+0.5. The technique is a CONSUMER whose cost GROWS with the cut-off radius.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Supplies no decay exponent whatsoever; it is the operator that pays for the "
                   "cut-off's divergence defect, and its price grows like rho^{+0.5}.",
  verdict="FAILS"),

 dict(
  tid="T8", family="OFF-LIST (F3/F4) -- located during the run and marked OFF-LIST per SS2.3",
  name="Albritton-Brue-Colombo: non-uniqueness of Leray solutions of the FORCED Navier-Stokes "
       "equations -- the closest published localisation of a self-similar NS object",
  citation="D. Albritton, E. Brue, M. Colombo, 'Non-uniqueness of Leray solutions of the forced "
           "Navier-Stokes equations', arXiv:2112.03116v1",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "2112.03116", "Theorem 4.1 (Non-uniqueness criterion), Sec. 4"),
  hypotheses=["Ubar is a COMPACTLY SUPPORTED, smooth, divergence-free vector field on R^3",
              "Ubar is an unstable steady state of the similarity-variable equation",
              "a body force f in L^1_t L^2_x is permitted",
              "the self-similarity is FORWARD (u = t^{-1/2} Ubar(x/sqrt t), t>0); the conclusion "
              "is NON-UNIQUENESS at t=0, NOT a finite-time singularity"],
  decisive_hypothesis="the similarity profile Ubar is COMPACTLY SUPPORTED",
  quote_spec=("2112.03116", "Non-uniqueness criterion). Let", "divergence-free vector field on R3 ."),
  object_status="FAILS",
  why="This technique does not need alpha > 1.5; it needs alpha = INFINITY. Route 4's object has "
      "alpha = 1 and, by T2c/T2e, cannot be improved above 1 at all, let alone to compact "
      "support. Two further mismatches recorded: a body force is required, whereas Fefferman's "
      "problems (A) and (C) are force-free (the artefact banks the verbatim Clay conditions); "
      "and the result is non-uniqueness, not blow-up.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="It ASSUMES compact support of the profile rather than supplying decay. Its "
                   "own truncation step (Prop. 2.2) is applied to a STEADY 2D vortex background "
                   "in an eigenvalue problem, where smallness comes from operator-norm "
                   "convergence of a spectral projection, not from any critical-norm bound -- "
                   "which is why the authors can write that 'any power-law decay will suffice' "
                   "there. That mechanism has no counterpart for a blow-up profile.",
  verdict="FAILS"),

 dict(
  tid="T9", family="OFF-LIST (F3/F4) -- located during the run and marked OFF-LIST per SS2.3",
  name="Albritton-Brue-Colombo: gluing non-unique Navier-Stokes solutions into a bounded domain",
  citation="D. Albritton, E. Brue, M. Colombo, 'Gluing non-unique Navier-Stokes solutions', "
           "arXiv:2209.03530v2",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "2209.03530", "Sec. 1, p. 2"),
  hypotheses=["the self-similar background ubar is COMPACTLY SUPPORTED",
              "an inner/outer gluing with a cut-off eta on an intermediate scale |x| ~ 1/10",
              "a body force f in L^1_t L^2_x"],
  decisive_hypothesis="the self-similar solution being localised is itself COMPACTLY SUPPORTED",
  quote_spec=("2209.03530", "is compactly supported, the non-uniqueness in [1] involves",
              "R3 × [0, T ]."),
  object_status="FAILS",
  why="This is the only located technique that actually glues a self-similar INCOMPRESSIBLE "
      "Navier-Stokes object on R^3 into a finite-energy bounded-domain solution, and it starts "
      "from a compactly supported profile. The thing it truncates is the OTHER solution, not the "
      "self-similar one. Route 4's object has alpha = 1 and cannot reach compact support.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Assumes compact support of the profile; supplies no decay.",
  verdict="FAILS"),

 dict(
  tid="T10", family="OFF-LIST (F5) -- located during the run and marked OFF-LIST per SS2.3; "
                    "banked as an ADVERSE EXACT EXAMPLE, not as a technique",
  name="Luong-Ramsey-Bertozzi-Baty: an exactly solvable far-field cutoff of a self-similar "
       "imploding profile SUPPRESSES the implosion",
  citation="J. Luong, S. Ramsey, A. L. Bertozzi, R. Baty, 'Self-similar imploding solutions of "
           "the 1D compressible Euler equations with a far field cutoff', arXiv:2606.12758v1",
  primary_text="OK -- full text read",
  quoted_from=("PRIMARY", "2606.12758", "Sec. 4, p. 15"),
  hypotheses=["1D radially symmetric isentropic COMPRESSIBLE Euler",
              "Kidder's closed-form imploding solution, unbounded in the far field",
              "the unbounded far-field condition is replaced by a constant-density cutoff"],
  decisive_hypothesis="the equation is 1D compressible Euler with a closed-form profile -- not "
                      "3D incompressible Navier-Stokes",
  quote_spec=("2606.12758", "Again, this is true no matter", "original cutoﬀ is"),
  object_status="FAILS-BY-CONSTRUCTION",
  why="Not a technique for this object and NOT evidence about Navier-Stokes: different equation, "
      "one space dimension, hyperbolic. It is banked because it is the one place located where "
      "the far-field cutoff of a self-similar blow-up profile is solved EXACTLY, and the answer "
      "is that a rarefaction emerges from the cutoff and the cut solution DOES NOT IMPLODE -- "
      "and, in the authors' own words, this holds no matter where the cutoff is placed. That is "
      "the shape of the risk CLAY_OBLIGATIONS SS4 names, demonstrated in a solvable case. It "
      "proves nothing about route 4's object and is recorded as a caution, not as a result.",
  could_supply_alpha_gt_1_5=False,
  could_supply_why="Not applicable; it is an adverse example, not a supplier.",
  verdict="FAILS-BY-CONSTRUCTION",
  extra_quote_spec=("2606.12758", "suppresses the Kidder solution", "does not implode.")),
]


def build() -> dict:
    bill = read_bill()
    controls = read_controls()
    ft = {r["arxiv_id"]: r for r in json.loads(FULLTEXT_SRC.read_text())["fulltexts"]}

    out = []
    for t in TECHNIQUES:
        aid = t["quote_spec"][0]
        rec = {
            "technique_id": t["tid"],
            "family": t["family"],
            "name": t["name"],
            "citation": t["citation"],
            "primary_text_reachability": t["primary_text"],
            "quote_provenance": {
                "kind": t["quoted_from"][0],
                "document_read": t["quoted_from"][1],
                "location": t["quoted_from"][2],
                "pdf_md5": ft.get(t["quoted_from"][1], {}).get("pdf_md5"),
                "txt_md5": ft.get(t["quoted_from"][1], {}).get("txt_md5"),
            },
            "hypotheses": t["hypotheses"],
            "decisive_hypothesis": t["decisive_hypothesis"],
            "decisive_hypothesis_quote": quote(aid, t["quote_spec"][1], t["quote_spec"][2]),
            "this_object_status": t["object_status"],
            "why_for_this_object": t["why"],
            "could_in_principle_supply_alpha_gt_1_5": t["could_supply_alpha_gt_1_5"],
            "could_supply_reason": t["could_supply_why"],
            "leg_381_bill_paid": "NOT PAID",
            "verdict": t["verdict"],
        }
        if "extra_quote_spec" in t:
            e = t["extra_quote_spec"]
            rec["supporting_quote"] = quote(e[0], e[1], e[2])
        check(rec["verdict"] in {"FAILS", "FAILS-BY-CONSTRUCTION", "OPEN-FOR-THIS-OBJECT",
                                 "SATISFIED", "UNREACHABLE", "THROTTLED"},
              f"{t['tid']}: verdict not in SS3.2's fixed list")
        out.append(rec)

    counts: dict[str, int] = {}
    for r in out:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    # SS3.3 mechanically: nobody paid, and it is checked rather than asserted.
    payers = [r["technique_id"] for r in out if r["could_in_principle_supply_alpha_gt_1_5"]]
    check(not payers, f"a technique claims it could supply alpha>1.5: {payers} -- SS3.3 requires "
                      "a certified two-sided enclosure with alpha_lo>1.5 on ROUTE 4's OWN profile")

    honest_ceiling = {
        "tier": "TIER 2",
        "gate_answer": "YES -- the named failing hypothesis is stated per technique, quoted "
                       "verbatim and located, for all 18 techniques read: 15 across all 7 "
                       "pre-registered families of SS2.3, plus 3 marked OFF-LIST.",
        "one_line": "Still no method -- and the reason is sharper than an absence: for THIS "
                    "object the decay exponent leg 381's bill asks for is not merely unavailable, "
                    "it is FATAL. Any alpha > 1 puts the profile in L^3(R^3), and two "
                    "independently located published statements then give full regularity, i.e. "
                    "no singularity to localise. The bill asks for alpha > 1.5.",
        "the_pin": "For any NONTRIVIAL backward lambda-DSS blow-up profile of 3D Navier-Stokes "
                   "the far-field decay exponent is pinned to EXACTLY alpha = 1: at least 1 by "
                   "Chae-Wolf Thm 1.1 (an upper bound on |u| of the form C/(sqrt(-t)+|x|)), and "
                   "AT MOST 1 by Chae-Wolf Remark 1.2 + Escauriaza-Seregin-Sverak, restated "
                   "independently by Pineau-Vicol (2026) Sec. 1.2.",
        "therefore": "The deficit of 0.5 in the exponent is NOT a gap in the literature that a "
                     "sharper technique might close. It is a step into a region the literature "
                     "has emptied. No technique read can pay it, and no technique COULD.",
        "what_this_does_NOT_say": [
            "It does NOT say 3D Navier-Stokes is regular. It says nothing whatever about that.",
            "It does NOT close route 4. It closes exactly ONE of the three ways W4's own "
            "pre-committed test allows W4 to break -- the one that reads 'with the decay "
            "actually available'. Supplying MORE decay is now measured to be self-defeating.",
            "It does NOT retire CLAY_OBLIGATIONS SS6(i). SS6(i) asks for CERTIFIED far-field "
            "decay and an admissible cutoff; this leg certifies nothing and builds no cutoff.",
            "It does NOT touch SS6(ii) or W5, which belong to unit L3'.",
            "Two structural routes remain UNTOUCHED by this reading, and they are the residual: "
            "(i) a NATIVELY FINITE-ENERGY DSS ansatz, which never asks the profile for decay at "
            "all; (ii) a target for which Clay condition (7) is not imposed. Both are named in "
            "W4's own pre-committed break test and neither was entered here.",
        ],
        "does_any_link_of_L1_to_L4_move": "NO. Nothing was built, no certificate was constructed, "
                                          "no profile was realised. Reading published literature "
                                          "moves no link.",
        "clay_odds": "~0.05%, unchanged. Scale is not evidence and Tier 2 is never a proof.",
        "verdict_counts": counts,
        "techniques_that_could_supply_alpha_gt_1_5": payers,
        "leg_381_bill_paid_by_anyone": BILL_PAID_BY_ANY,
    }

    return {
        "leg": 397, "unit": "L2'", "lane": "L", "route": "L2-DECAY",
        "obligation": "CLAY_OBLIGATIONS.md SS6(i) -- SS4's certified far-field decay and the "
                      "admissible cutoff. Wall W4.",
        "what": "Per-technique reading of the published localisation / far-field-decay "
                "literature AGAINST route 4's backward DSS object carrying leg 381's banked "
                "bill. For each technique: the hypothesis list, the ONE named hypothesis that "
                "decides applicability to THIS object, quoted verbatim and located, and whether "
                "the technique could in principle supply alpha > 1.5.",
        "object": {
            "description": "backward DISCRETELY self-similar blow-up profile U for 3D "
                           "incompressible Navier-Stokes on R^3, non-axisymmetric, at "
                           "lambda >> 1, realised as a periodic orbit of period 2 log(lambda) "
                           "in the similarity variable",
            "lambda_checked_in_artefact": 1.7,
            "period_in_s": 1.0612565021243408,
            "far_field_model": "|U(y)| <~ |y|^{-alpha}",
            "no_profile_of_this_object_exists_in_this_repository": True,
        },
        "banked_bill_re_derived_from_artefact": bill,
        "search_instrument": controls,
        "techniques": out,
        "honest_ceiling": honest_ceiling,
        "ceiling": "TIER 2. No link of the L1->L4 chain moved. Clay stays ~0.05%. Reading the "
                   "literature is not progress toward a proof; it is a measurement of what the "
                   "literature does and does not contain.",
        "bans_checked": "The l1-Fourier / radii-polynomial ban is NOT engaged: this unit builds "
                        "no certificate, constructs no approximate inverse, and reaches for no "
                        "Y0/Z0/Z1/Z2 contraction in any space. No ban was lifted, narrowed, "
                        "re-read or argued against.",
        "outreach": "READ ONLY. No author, group, maintainer or mailing list was contacted, not "
                    "even to request a PDF. Four pre-arXiv journal-only sources "
                    "(Necas-Ruzicka-Sverak 1996, Tsai 1998, Bogovskii 1979, Giga-Kohn 1985/89) "
                    "are banked UNREACHABLE at primary text, exactly as declared in advance by "
                    "SS2.1, and are quoted only through reachable SECONDARY sources.",
    }


def main() -> int:
    art = build()
    self_blob = json.dumps(art, sort_keys=True, ensure_ascii=False).encode()
    art["self_hash"] = hashlib.sha256(self_blob).hexdigest()[:16]
    OUT.write_text(json.dumps(art, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")
    print(json.dumps(art["honest_ceiling"]["verdict_counts"], indent=1))
    print("bill paid by anyone:", art["honest_ceiling"]["leg_381_bill_paid_by_anyone"])
    print("could supply alpha>1.5:",
          art["honest_ceiling"]["techniques_that_could_supply_alpha_gt_1_5"] or "NONE")
    nq = [t["technique_id"] for t in art["techniques"]
          if t["decisive_hypothesis_quote"]["status"] != "VERBATIM"]
    print("non-verbatim quotes:", nq or "NONE")
    if FAILURES:
        print("\nEVIDENCE FAILURES:")
        for f in FAILURES:
            print("  -", f)
        return 1
    print("\nall checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
