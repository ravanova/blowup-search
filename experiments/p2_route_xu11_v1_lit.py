"""Route-XU11 v1: does Xu arXiv:2607.19762 characterize or bear on a SIGN-CHANGING /
ANTI-DIFFUSIVE viscous branch for this operator class?

Leg 185 measured, at fixed `c_l = 1/2`, `c_omega = -1` (i.e. `Delta = 0`, the gamma = 2
steadiness condition), that the `nu` recovered from the square profile system is POSITIVE
below `a* = 0.3864963972206034` (`nu = +0.01799364` at `a = 0.30`, grid-converged to 6
digits over n = 201..1201 and truncation-insensitive over a 55x domain extension) and
NEGATIVE at and above it, including Chen's own `a = 1/2` (`nu = -0.00818 / -0.00895`).
That is an anti-diffusive branch above a threshold, and it postdates every prior read of Xu.

Xu has been read at full text seven times (legs 127, 163, 171, 173, 181, 183 for the
origin-H^2 citation and the sec 8 no-go; leg 189 for the a_c / alpha(1/2) provenance), and
leg 145 already banked the NUMBER 0.386 out of Xu's Table 1 as a transcription
self-consistency check (`p2_route_lga_v1_ledger.py:568`).  NONE of them asked the sign
question.  Leg 185's own novelty pass reached Xu at search level only and classified him in
one word -- "(inviscid)".  Section 6 was never opened.

This driver opens it.

  X1  THE PASSAGE LEDGER: EVERY PLACE IN XU WHERE THE SIGN OF THE DISSIPATION COEFFICIENT
      IS FIXED, VERBATIM.  Twelve passages -- (6.1), (6.2)/(6.3), the sec 6.1 threshold
      sentence, its two disclaimers, the Table 1 a = 0.4 cross-check cell, the Figure 3
      caption, (A.1), (A.3), Appendix A fact (ii), sec 8 (iii) and sec 8 (iv) -- each with
      the verdict "admits nu <= 0?".  Every quote is RE-VERIFIED against a fresh
      `pdftotext -layout` extraction of the fetched PDF when `Papers/2607.19762.pdf` is
      present, so this is checked text, not transcription from memory.  When the PDF is
      absent (Papers/ is gitignored) the quotes stand as banked constants and the JSON says
      so in `verified_against_pdf`.

  X2  THE COLLOCATION, MEASURED.  Xu states the s = 2 sub/supercritical boundary twice, as
      "a ~ 0.39" (headline) and "the branch inverts to a = 0.386" (parenthetical).  Legs
      125/185 have `a* = 0.3864963972206034` from two independent computations.  Magnitudes
      of agreement, against Xu's printed digits AND against a linear inversion of Xu's own
      Table 1 at c_l = 1/2 -- which is leg 145's instrument, re-used read-only.

  X3  THE MECHANISM IDENTITY, AND A NEGATIVE CONTROL THAT MUST FAIL.  Xu's (6.2) defines
      `gamma := 1 - s c_l`.  This repository's `solver/dissipative_profile.py` defines
      `Delta := 2 c_l / |c_omega| - 1`.  Under Xu's own time normalization (his rescaling
      (T-t)^{-1} W is c_omega = -1), the claim is the EXACT identity `Delta == -gamma` at
      s = 2, on every row.  Checked to machine precision on all 8 Table 1 rows.  NEGATIVE
      CONTROL (lesson 90): the same code path is run against two decoy maps, `1 - c_l` and
      `1 - 4 c_l`, which must NOT reproduce -Delta.  If the control does not fire, X3 is
      not a measurement.

  X4  IS THE COLLOCATION SPECIFIC TO s = 2, OR WOULD ANY s HAVE LANDED THERE?  The boundary
      a(s) solving c_l(a) = 1/s is inverted off Xu's own table for s in 1.8..2.2, and the
      distance to a* is reported for each.  Second control: Xu's OTHER printed special
      a-values (the max-protrusion a ~ 0.264 of sec 3.1 and the branch endpoint 0.6888) are
      run as decoy thresholds and must miss a* by orders more.

  X5  IS THE AGREEMENT RESOLVED, OR MERELY UNCONTRADICTED?  Xu's own declared resolution on
      c_l is a two-grid difference <~ 5e-4, "a self-consistency measure rather than a
      certified continuum error bound".  Propagated through the local slope dc_l/da of his
      own bracket, that is an uncertainty on a.  The observed gap is compared to it.  A
      ratio near 1 means the two numbers CANNOT be told apart at Xu's stated resolution --
      which is the honest reading and is NOT the same as proving they are the same number.

  X6  THE GATE, ANSWERED IN ITS PRE-COMMITTED WORDING, ON BOTH LIMBS SEPARATELY:
      "characterize ... directly", and "bear on ... as a derivable corollary of a stated
      theorem".  The two limbs get different answers and the JSON records both.

This leg does NOT reconcile Xu with leg 185, does NOT build a viscous branch, and does NOT
edit solver/literature_gates.py or any certificate module.  Its gate's yes-branch forbids
all three.

Deterministic, sub-second, no network (the PDF, if used, is already on disk).  Every number
the prose quotes is in the JSON.  Writes writeup/data/p2_route_xu11_v1_lit.json.

Run: .venv/bin/python -u experiments/p2_route_xu11_v1_lit.py
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.literature_gates import XU_TABLE1, LSS_A_C  # read-only, NOT edited

OUT = ROOT / "writeup" / "data" / "p2_route_xu11_v1_lit.json"
PDF = ROOT / "Papers" / "2607.19762.pdf"

# ---------------------------------------------------------------------------
# The two numbers this leg joins, both already banked, neither claimed as new here.
# ---------------------------------------------------------------------------

# legs 125 (Delta(a) sweep at nu = 0, c_l as OUTPUT) and 185 (sign of the recovered nu at
# c_l = 1/2 imposed) -- two independent computations landing on the same a.
REPO_A_STAR = 0.3864963972206034

# Xu's two printed forms of the s = 2 sub/supercritical boundary (sec 6.1 + Fig. 3 caption).
XU_BOUNDARY_HEADLINE = 0.39
XU_BOUNDARY_INVERTED = 0.386

# Xu's own declared resolution on c_l (sec 2 / sec 7): two-grid |c_l(1024) - c_l(2048)|.
XU_TWO_GRID_C_L = 5e-4

# Leg 185's measured nu at the two anchor advections, for magnitude reporting only.
LEG185_NU = {
    "a=0.30": +0.01799364,   # grid-converged n = 1201; truncation-insensitive over 55x
    "a=0.50": -0.00817525,   # Chen's own a; the nu>0.3 start.  Second start: -0.00895316
}

# ---------------------------------------------------------------------------
# X1 -- the passage ledger.  Verbatim, with locators and the sign verdict.
# ---------------------------------------------------------------------------

PASSAGES = [
    {
        "id": "P1",
        "locator": "sec 6, eq (6.1)",
        "quote": "wt + a u wx = ux w − ν Λs w, Λ = (−∂xx )1/2 , ν > 0, s ∈ (0, 2]. (6.1)",
        "why_it_is_here": "the ONLY place Xu writes the dissipative gCLM equation in the "
                          "main text",
        "admits_nu_le_0": False,
        "note": "nu > 0 is a STANDING HYPOTHESIS of the display, not a convention stated "
                "and later relaxed.  Xu never writes a second dissipative equation.",
    },
    {
        "id": "P2",
        "locator": "sec 6.1, eq (6.2)",
        "quote": "∂τ W = −Res[W ] − ν e−γτ Λsy W, γ := 1 − s cl . (6.2)",
        "why_it_is_here": "defines gamma, the quantity that DOES change sign in Xu",
        "admits_nu_le_0": False,
        "note": "What changes sign here is gamma, the EXPONENT of the coefficient, not nu. "
                "nu is carried through unchanged and positive.",
    },
    {
        "id": "P3",
        "locator": "sec 6.1, the sentence after eq (6.3)",
        "quote": "for the ordinary Laplacian s = 2 the sub/supercritical boundary sits at "
                 "a ≈ 0.39 (where cl = 1/2; the branch inverts to a = 0.386).",
        "why_it_is_here": "THE PASSAGE THE GATE TURNS ON -- Xu's stated threshold",
        "admits_nu_le_0": False,
        "note": "States the threshold and its mechanism (c_l = 1/2) and prints 0.386.  Says "
                "nothing about the sign of nu.",
    },
    {
        "id": "P4",
        "locator": "sec 6.1, disclaimer 1",
        "quote": "s∗ is a formal scaling (dissipation-relevance) threshold read off the "
                 "self-similar exponent",
        "why_it_is_here": "downgrades sec 6 from theorem to diagnostic",
        "admits_nu_le_0": False,
        "note": "Decisive for the gate's SECOND limb: sec 6 is declared formal, so nothing "
                "in it is 'a stated theorem' from which a corollary could be derived.",
    },
    {
        "id": "P5",
        "locator": "sec 6.1, disclaimer 2",
        "quote": "and s∗ is not the sharp critical dissipation curve separating blow-up "
                 "from global regularity, which for this family remains unknown.",
        "why_it_is_here": "Xu's own statement of what his threshold is NOT",
        "admits_nu_le_0": False,
        "note": None,
    },
    {
        "id": "P6",
        "locator": "Table 1, a = 0.4 cross-check cell",
        "quote": "(s = 2 boundary at ≈ 0.39, where cl = 1/2)",
        "why_it_is_here": "the same threshold, printed a second time, in the table leg 145 "
                          "transcribed",
        "admits_nu_le_0": False,
        "note": "This is the cell leg 145's s2_boundary_from_table_linear was checked "
                "against.  Its viscous reading was never asked for.",
    },
    {
        "id": "P7",
        "locator": "Figure 3 caption",
        "quote": "and crossing the ordinary-Laplacian value s = 2 at a ≈ 0.39 where cl = "
                 "1/2. This is a formal scaling diagnostic, not a proved persistence "
                 "threshold.",
        "why_it_is_here": "the threshold a third time, with the disclaimer attached to it",
        "admits_nu_le_0": False,
        "note": None,
    },
    {
        "id": "P8",
        "locator": "Appendix A.1, eq (A.1)",
        "quote": "wt = w Hw − ν Λs w, Λ = (−∂xx )1/2 , ν > 0, s ∈ (0, 1), (A.1)",
        "why_it_is_here": "the second and last place Xu writes a dissipative equation",
        "admits_nu_le_0": False,
        "note": "nu > 0 again, and s restricted further to (0,1) -- strictly BELOW s = 2, "
                "so the appendix never even reaches the Laplacian leg 185 works at.",
    },
    {
        "id": "P9",
        "locator": "Appendix A.1, eq (A.3)",
        "quote": "∂τ W = −Res[W ] − ν e−γτ Λsy W, γ = 1 − s cl = 1 − s > 0, (A.3)",
        "why_it_is_here": "gamma's sign fixed POSITIVE by hypothesis in the appendix",
        "admits_nu_le_0": False,
        "note": "The appendix works only on the side gamma > 0.  The other side of Xu's own "
                "threshold is never analyzed.",
    },
    {
        "id": "P10",
        "locator": "Appendix A.1, structural fact (ii), first half",
        "quote": "The dissipative term is dissipative in the flat L2 pairing (its Fourier "
                 "symbol",
        "why_it_is_here": "the sign-definiteness claim",
        "admits_nu_le_0": False,
        "note": None,
    },
    {
        "id": "P11",
        "locator": "Appendix A.1, structural fact (ii), second half (across the page break)",
        "quote": "−νe−γτ |k|s ≤ 0) and carries a coefficient that vanishes as τ → ∞",
        "why_it_is_here": "THE DEPENDENCE MADE EXPLICIT -- the <= 0 is inherited from nu > 0",
        "admits_nu_le_0": False,
        "note": "The symbol is nonpositive BECAUSE nu > 0.  Flip nu and this structural "
                "fact, which the whole persistence program of sec 8 rests on, reverses.  "
                "Xu does not consider that case.",
    },
    {
        "id": "P12",
        "locator": "sec 8, direction (iv)",
        "quote": "the supercritical regime s > s∗ (a), where the dissipation is relevant, "
                 "is outside the present framework.",
        "why_it_is_here": "Xu's own scope exclusion, on the far side of his own threshold",
        "admits_nu_le_0": False,
        "note": "Xu declares the regime beyond his threshold out of scope.  Leg 185's "
                "negative-nu half sits on exactly that side at s = 2.",
    },
]


def x1_passage_ledger():
    """Verbatim ledger, re-verified against a fresh extraction of the fetched PDF."""
    verified = None
    extract_ok = False
    text_norm = ""
    if PDF.exists():
        try:
            raw = subprocess.run(
                ["pdftotext", "-layout", str(PDF), "-"],
                capture_output=True, text=True, timeout=120, check=True).stdout
            text_norm = re.sub(r"\s+", " ", raw)
            extract_ok = True
        except Exception:
            extract_ok = False

    rows = []
    for p in PASSAGES:
        q = re.sub(r"\s+", " ", p["quote"]).strip()
        found = (q in text_norm) if extract_ok else None
        rows.append({**p, "quote_normalized": q, "found_in_pdf": found})

    if extract_ok:
        verified = all(r["found_in_pdf"] for r in rows)

    n_admit = sum(1 for p in PASSAGES if p["admits_nu_le_0"])
    return {
        "pdf_present": PDF.exists(),
        "pdftotext_ok": extract_ok,
        "verified_against_pdf": verified,
        "n_passages": len(rows),
        "n_verbatim_found": (sum(1 for r in rows if r["found_in_pdf"]) if extract_ok
                             else None),
        "n_passages_admitting_nu_le_0": n_admit,
        "xu_ever_admits_nonpositive_nu": bool(n_admit),
        "sign_of_nu_is_a_standing_hypothesis": True,
        "places_the_dissipative_equation_is_written": ["sec 6 eq (6.1)", "App A eq (A.1)"],
        "both_stipulate_nu_positive": True,
        "passages": rows,
    }


# ---------------------------------------------------------------------------
# X2 -- the collocation
# ---------------------------------------------------------------------------

def _invert_table_at(c_target):
    """Linear inversion of Xu's OWN Table 1 for the a at which c_l(a) = c_target.

    This is leg 145's instrument (p2_route_lga_v1_ledger.py:568), re-used read-only so the
    number is comparable to the one already banked.  Returns None if out of bracket.
    """
    for (a0, c0, _), (a1, c1, _) in zip(XU_TABLE1, XU_TABLE1[1:]):
        if (c0 - c_target) * (c1 - c_target) <= 0 and c0 != c1:
            return a0 + (a1 - a0) * (c0 - c_target) / (c0 - c1)
    return None


def x2_collocation():
    a_tab = _invert_table_at(0.5)
    d_head = abs(XU_BOUNDARY_HEADLINE - REPO_A_STAR)
    d_inv = abs(XU_BOUNDARY_INVERTED - REPO_A_STAR)
    d_tab = abs(a_tab - REPO_A_STAR)
    return {
        "repo_a_star": REPO_A_STAR,
        "repo_a_star_provenance": ("leg 125 (Delta(a) sweep at nu = 0, c_l an OUTPUT) and "
                                   "leg 185 (sign of recovered nu at c_l = 1/2 imposed) -- "
                                   "two independent computations, same number"),
        "xu_boundary_headline": XU_BOUNDARY_HEADLINE,
        "xu_boundary_inverted_as_printed": XU_BOUNDARY_INVERTED,
        "xu_boundary_from_table_linear": a_tab,
        "abs_gap_vs_headline": d_head,
        "abs_gap_vs_printed_inverted": d_inv,
        "abs_gap_vs_table_inversion": d_tab,
        "rel_gap_vs_printed_inverted": d_inv / REPO_A_STAR,
        "rel_gap_vs_table_inversion": d_tab / REPO_A_STAR,
        "same_to_printed_digits_of_xu": round(a_tab, 3) == XU_BOUNDARY_INVERTED,
        "leg145_already_banked_this_number": True,
        "leg145_locator": ("experiments/p2_route_lga_v1_ledger.py:568 -> "
                           "test_literature_gates_selfconsistency.py:107-110, as a "
                           "TRANSCRIPTION self-consistency check with no viscous reading"),
    }


# ---------------------------------------------------------------------------
# X3 -- the mechanism identity, with a negative control that must fire
# ---------------------------------------------------------------------------

def _xu_gamma(c_l, s):
    """Xu eq (6.2): gamma := 1 - s c_l."""
    return 1.0 - s * c_l


def _repo_delta(c_l, c_omega=-1.0):
    """solver/dissipative_profile.py lines 35-44: Delta := 2 c_l / |c_omega| - 1."""
    return 2.0 * c_l / abs(c_omega) - 1.0


def x3_mechanism_identity():
    rows, worst = [], 0.0
    for a, c_l, _ in XU_TABLE1:
        g = _xu_gamma(c_l, 2.0)
        d = _repo_delta(c_l)
        dev = abs(d - (-g))
        worst = max(worst, dev)
        rows.append({"a": a, "c_l": c_l, "gamma_xu_at_s2": g, "Delta_repo": d,
                     "abs_dev_from_identity": dev})

    # NEGATIVE CONTROL (lesson 90): decoys that must NOT satisfy the identity.
    decoys = {}
    for name, s_eff in (("gamma_with_s=1", 1.0), ("gamma_with_s=4", 4.0)):
        w = max(abs(_repo_delta(c_l) - (-_xu_gamma(c_l, s_eff)))
                for _, c_l, _ in XU_TABLE1)
        decoys[name] = w
    control_fired = all(w > 1e-6 for w in decoys.values())

    sign_changes = [
        {"between_a": [rows[i]["a"], rows[i + 1]["a"]],
         "gamma": [rows[i]["gamma_xu_at_s2"], rows[i + 1]["gamma_xu_at_s2"]]}
        for i in range(len(rows) - 1)
        if rows[i]["gamma_xu_at_s2"] * rows[i + 1]["gamma_xu_at_s2"] < 0
    ]

    return {
        "identity_claimed": "Delta_repo(c_l, c_omega=-1) == -gamma_Xu(c_l, s=2)",
        "hypothesis": ("Xu's rescaling w = (T-t)^{-1} W (eq 6.1 / A.2) IS c_omega = -1, so "
                       "the identity holds only under Xu's own time normalization"),
        "worst_abs_deviation_over_8_rows": worst,
        "identity_exact_to_machine": worst < 1e-12,
        "decoy_worst_deviations": decoys,
        "negative_control_fired": control_fired,
        "n_sign_changes_of_gamma_on_xu_table": len(sign_changes),
        "gamma_sign_change_bracket": sign_changes,
        "reading": ("Xu's gamma at s = 2 and this repository's Delta are the SAME quantity "
                    "up to sign.  Leg 185 IMPOSED Delta = 0, i.e. it sat exactly on Xu's "
                    "marginal curve gamma = 0, and then let nu float."),
    }


# ---------------------------------------------------------------------------
# X4 -- is the collocation specific to s = 2?
# ---------------------------------------------------------------------------

def x4_specificity_controls():
    s_rows = []
    for s in (1.8, 1.9, 2.0, 2.1, 2.2):
        a_s = _invert_table_at(1.0 / s)
        s_rows.append({"s": s, "c_l_target": 1.0 / s, "a_boundary": a_s,
                       "abs_gap_to_a_star": abs(a_s - REPO_A_STAR)})
    best = min(s_rows, key=lambda r: r["abs_gap_to_a_star"])
    off = [r for r in s_rows if r["s"] != 2.0]
    worst_off = min(r["abs_gap_to_a_star"] for r in off)

    # second control: Xu's OTHER printed special a-values
    decoy_a = {"max_protrusion_a_sec_3_1": 0.264, "branch_endpoint_a_c": 0.6888}
    decoy_gaps = {k: abs(v - REPO_A_STAR) for k, v in decoy_a.items()}

    return {
        "s_scan": s_rows,
        "argmin_s": best["s"],
        "argmin_is_the_ordinary_laplacian": best["s"] == 2.0,
        "gap_at_s2": best["abs_gap_to_a_star"],
        "nearest_off_s2_gap": worst_off,
        "specificity_factor": worst_off / best["abs_gap_to_a_star"],
        "decoy_thresholds_from_xu": decoy_a,
        "decoy_gaps_to_a_star": decoy_gaps,
        "decoy_control_fired": all(g > 100 * best["abs_gap_to_a_star"]
                                   for g in decoy_gaps.values()),
        "reading": ("+-10% in s moves Xu's boundary by ~40x the observed gap, and Xu's "
                    "other printed special advections miss a* by 2-3 orders.  The "
                    "collocation is a property of s = 2 -- leg 185's own gamma = 2 case -- "
                    "not of the inversion being loose."),
    }


# ---------------------------------------------------------------------------
# X5 -- is the agreement RESOLVED, or merely uncontradicted?
# ---------------------------------------------------------------------------

def x5_resolution():
    # local slope of Xu's own branch across the bracket that contains c_l = 1/2
    (a0, c0, _), (a1, c1, _) = XU_TABLE1[3], XU_TABLE1[4]      # a = 0.30, 0.40
    slope = (c1 - c0) / (a1 - a0)
    delta_a = XU_TWO_GRID_C_L / abs(slope)
    gap = abs(_invert_table_at(0.5) - REPO_A_STAR)
    ratio = gap / delta_a
    return {
        "bracket": [a0, a1],
        "local_slope_dcl_da": slope,
        "xu_declared_two_grid_c_l": XU_TWO_GRID_C_L,
        "xu_own_statement": ("'a self-consistency measure rather than a certified continuum "
                             "error bound' (sec 2 / sec 7)"),
        "implied_delta_a": delta_a,
        "observed_gap": gap,
        "observed_over_xu_uncertainty": ratio,
        "resolved_apart": ratio > 3.0,
        "reading": ("The two numbers sit within ~1.2 of Xu's OWN error bar, so they cannot "
                    "be told apart at his stated resolution.  That is agreement in the only "
                    "sense the source supports -- it is NOT a proof that they are the same "
                    "number, and this leg does not claim one."),
    }


# ---------------------------------------------------------------------------
# X6 -- the gate
# ---------------------------------------------------------------------------

def x6_gate(x1, x2, x3, x4, x5):
    limb_direct = x1["xu_ever_admits_nonpositive_nu"]
    # limb 2: a derivable corollary requires a STATED THEOREM.  Xu declares sec 6 formal.
    limb_corollary = False
    bears_on = (x2["same_to_printed_digits_of_xu"]
                and x3["identity_exact_to_machine"]
                and x4["argmin_is_the_ordinary_laplacian"])
    return {
        "gate_wording": ("Does Xu arXiv:2607.19762, at full-text depth, characterize or "
                         "bear on a sign-changing/anti-diffusive viscous branch for this "
                         "operator class (directly, or as a derivable corollary of a stated "
                         "theorem)?"),
        "limb_1_characterizes_directly": limb_direct,
        "limb_1_evidence": ("nu > 0 is stipulated at BOTH places Xu writes a dissipative "
                            "equation, (6.1) and (A.1); the sign-definiteness of the "
                            "dissipative form in App A (ii) is DERIVED from it; and sec 8 "
                            "(iv) puts the far side of his own threshold out of scope.  "
                            "0/12 passages admit nu <= 0."),
        "limb_2_derivable_corollary_of_a_stated_theorem": limb_corollary,
        "limb_2_evidence": ("sec 6 is not a theorem.  Xu declares s* 'a formal scaling "
                            "(dissipation-relevance) threshold' and the Figure 3 caption "
                            "repeats 'a formal scaling diagnostic, not a proved persistence "
                            "threshold'.  The paper's actual theorems (Thm 1, Thm 2, Lemma "
                            "1, Prop 1, Prop 2) are all inviscid spectral statements at or "
                            "near a = 0 and mention no dissipation."),
        "limb_3_bears_on": bears_on,
        "limb_3_evidence": ("Xu STATES the threshold, three times, and prints 0.386; the "
                            "mechanism he gives for it (c_l = 1/2, gamma = 1 - s c_l = 0 at "
                            "s = 2) is exactly this repository's own Delta = 0, the "
                            "condition leg 185 imposed; and the collocation with "
                            "a* = 0.3864963972206034 is specific to s = 2."),
        "answer": "YES" if (limb_direct or limb_corollary or bears_on) else "NO",
        "answer_qualified": ("YES, on the 'bear on' limb only, at DIAGNOSTIC strength.  Xu "
                             "does NOT characterize a sign-changing/anti-diffusive branch "
                             "-- he stipulates nu > 0 throughout -- and the threshold he "
                             "does state is declared by him to be a formal diagnostic, not "
                             "a theorem.  What he supplies is the LOCATION and the "
                             "MECHANISM of leg 185's boundary, from an independent source."),
        "branch": ("ESCALATE as directly informing leg 174's catalog and leg 185's own "
                   "finding.  Do NOT build or attempt to reconcile the two under this "
                   "leg's authority.  Push branch only, never main.  Report as parked."),
        "what_this_leg_explicitly_did_not_do": [
            "did not reconcile Xu's gamma-crossing with leg 185's nu sign change",
            "did not construct or continue any viscous branch",
            "did not edit solver/literature_gates.py or any certificate module",
            "did not claim 0.386 as new (leg 145 banked it -- see novelty pass 2.1)",
            "did not claim a* is PROVED equal to Xu's boundary (X5: not resolved apart)",
        ],
    }


def main():
    t0 = time.time()
    x1 = x1_passage_ledger()
    x2 = x2_collocation()
    x3 = x3_mechanism_identity()
    x4 = x4_specificity_controls()
    x5 = x5_resolution()
    x6 = x6_gate(x1, x2, x3, x4, x5)

    out = {
        "leg": 211,
        "route": "XU11",
        "role": "LIT",
        "source": "arXiv:2607.19762v1 (Xu), read at full text via pdftotext -layout",
        "question": ("does Xu characterize or bear on a sign-changing/anti-diffusive "
                     "viscous branch for this operator class?"),
        "grounded_in": ("leg 185 D5: nu > 0 below a* = 0.3864963972206034, nu < 0 at and "
                        "above it including Chen's a = 1/2"),
        "leg185_nu_anchors": LEG185_NU,
        "X1_passage_ledger": x1,
        "X2_collocation": x2,
        "X3_mechanism_identity": x3,
        "X4_specificity_controls": x4,
        "X5_resolution": x5,
        "X6_gate": x6,
        "gate_answer": x6["answer"],
        "no_dynamics_run": True,
        "claims_no_stage": True,
    }
    out["runtime_s"] = time.time() - t0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=False))

    print("=== Route-XU11 v1: does Xu bear on a sign-changing viscous branch? ===")
    print(f"X1 passage ledger:      {x1['n_passages']} passages where the sign of nu could "
          f"be stated; {x1['n_passages_admitting_nu_le_0']} admit nu <= 0  "
          f"[verbatim-verified against PDF: {x1['verified_against_pdf']}, "
          f"{x1['n_verbatim_found']}/{x1['n_passages']}]")
    print(f"X2 collocation:         Xu prints {x2['xu_boundary_inverted_as_printed']}; his "
          f"own Table 1 inverts to {x2['xu_boundary_from_table_linear']:.6f}; repo a* = "
          f"{x2['repo_a_star']:.10f}  (gap {x2['abs_gap_vs_table_inversion']:.2e} = "
          f"{x2['rel_gap_vs_table_inversion']:.3%})")
    print(f"X3 mechanism identity:  Delta == -gamma(s=2) to "
          f"{x3['worst_abs_deviation_over_8_rows']:.1e} over 8 rows; gamma changes sign "
          f"{x3['n_sign_changes_of_gamma_on_xu_table']}x  "
          f"[control fired: {x3['negative_control_fired']}, decoys miss by "
          f"{min(x3['decoy_worst_deviations'].values()):.3f}]")
    print(f"X4 specificity:         argmin s = {x4['argmin_s']} (the ordinary Laplacian); "
          f"nearest off-s=2 gap is {x4['specificity_factor']:.0f}x larger  "
          f"[decoy control fired: {x4['decoy_control_fired']}]")
    print(f"X5 resolution:          Xu's own 5e-4 on c_l implies delta_a = "
          f"{x5['implied_delta_a']:.2e}; observed/uncertainty = "
          f"{x5['observed_over_xu_uncertainty']:.2f}x  "
          f"[resolved apart: {x5['resolved_apart']}]")
    print()
    print(f"X6 limb 1 (characterizes directly):        "
          f"{x6['limb_1_characterizes_directly']}")
    print(f"X6 limb 2 (corollary of a stated theorem): "
          f"{x6['limb_2_derivable_corollary_of_a_stated_theorem']}")
    print(f"X6 limb 3 (bears on):                      {x6['limb_3_bears_on']}")
    print()
    print(f"GATE: {out['gate_answer']}  -> ESCALATE, park, push branch only")
    print(f"wrote {OUT.relative_to(ROOT)}  ({out['runtime_s']:.2f} s)")


if __name__ == "__main__":
    main()
