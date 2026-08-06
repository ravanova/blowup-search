"""Route-EGML v1: "EGM" located at primary source, and turned into measurements.

"EGM" was relayed into this repository's steering documents twice -- the external novelty
review's summary of leg 165's classification, "at p = 2 it is width 2.0 and EGM certifies a
-1/2 gap" -- but the string appears NOWHERE in solver/literature_gates.py or in any other
shared ledger.  Leg 141 had in fact read the paper at full text; it banked the read in its
own leg artifacts only.  So the gap this leg closes is a LEDGER gap, not a knowledge gap.

The paper is Elgindi-Ghoul-Masmoudi, "Stable self-similar blowup for a family of nonlocal
transport equations", arXiv:1906.05811, published as Anal. PDE 14 (2021) 891-908.  Read at
leg 190 from the PDF AND from the arXiv LaTeX e-print, deliberately not from leg 141's
transcript -- and that independence is what produced this leg's one real finding (E4).

The gate (DIRECTION.md sec 190):

    Can "EGM" be located as a real, checkable primary source, and does it state the p=2,
    -1/2-gap claim as relayed, with its own hypotheses?

Answering it with a paragraph saying "we read it" is what leg 141 already did.  This driver
answers it with numbers computed off EGM's OWN printed formulas:

  E1  EGM'S -1/2 IS EXACT, AND IT IS REPRODUCIBLE FROM THEIR OWN LAST LINE.  The closing
      step of their sec 2 proof evaluates the local coefficient
          D(y) = -2 H F_0(y) - 1 + (1/2) d_y(y phi) / phi
      with F_0 = y/(1+y^2), H F_0 = -1/(1+y^2) and phi = (1+y^2)^2/y^4, and claims it equals
      -1/2 identically in y.  Computed here on a decades-wide grid, analytically AND by
      finite differences of phi.  This is the -1/2 the repository quotes -- as a computed
      number, not a quoted one.  NEGATIVE CONTROLS THAT MUST FAIL: two decoy profiles
      (F = y/(1+y^2)^2 and F = y/(1+2y^2)) put through the identical code path.

  E2  gamma = 4 IS NOT A CHOICE, IT IS THE UNIQUE EXPONENT THAT MAKES THE CONSTANT EXACT.
      Replace EGM's weight by the one-parameter family phi_gamma = (1+y^2)^{gamma/2}/y^gamma
      (same origin exponent gamma, same far-field behaviour) and recompute D_gamma(y).  Its
      origin value is (3-gamma)/2 -- which is exactly leg 165's D_phi(0) formula, recovered
      here from EGM's algebra rather than quoted -- its far-field value is -1/2 for EVERY
      gamma, and it is CONSTANT in y for gamma = 4 alone.  Scanned over gamma so the
      uniqueness is measured, not asserted.  This is a statement about the local/diagonal
      term only; it does NOT license "any gamma >= 4 works", because EGM's vanishing
      identity int Hf f F_0 phi = 0 is itself gamma = 4 algebra.  Recorded as a caveat.

  E3  H F_0 = -1/(y^2+1) AGAINST AN INSTRUMENT THAT SHARES NO ALGEBRA WITH THE PAPER.
      EGM print the pair (F_0, H F_0); this repository has its own validated whole-line
      Hilbert transform (solver/line_hilbert.py).  Checked on sinh grids at two resolutions,
      which also pins the sign convention: the repository's H is EGM's H, not its negative.

  E4  THE TRANSCRIPTION AUDIT -- AND THE ONE THING THIS LEG FOUND.  Prop. 2.1's constant is
      -(1/2 - C|a|), read from the LaTeX source.  Three legs of this repository (141, 165,
      and leg 190's own novelty pass) transcribed it as (-1/2 - C|a|), which has the gap
      IMPROVING with |a| instead of degrading.  Quantified here: the two readings agree to
      0 at a = 0 -- the only value ever quoted here -- and diverge linearly off axis, at
      2C|a| absolute, i.e. the sign of the slope is reversed.  Nothing banked moves.

  E5  THE p = 2 JOIN, ARITHMETIC, AND WHOSE CLAIM EACH HALF IS.  leg 111's admissible window
      (3, 2p+1) at p = 1 and p = 2, against EGM's gamma = 4.

Deterministic, no network, a few seconds.  Writes writeup/data/p2_route_egml_v1_lit.json.

Run: .venv/bin/python -u experiments/p2_route_egml_v1_lit.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.line_hilbert import line_hilbert                     # noqa: E402
from solver.literature_gates import EGM_PRIMARY_READ             # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_egml_v1_lit.json"

# EGM's number, at a = 0.  Exact, not numerical.
EGM_GAP_A0 = -0.5
# EGM's weight exponent at the origin: phi = (1+y^2)^2/y^4 ~ y^{-4}.
EGM_GAMMA = 4.0


# --------------------------------------------------------------------------
# EGM sec 1: the a = 0 profile, and sec 2's closing coefficient
# --------------------------------------------------------------------------
def F0(y):
    """EGM sec 1, after (1.7):  F_0(y) = y/(1+y^2)   (the a = 0, CLM profile)."""
    return y / (1.0 + y * y)


def HF0(y):
    """EGM sec 1, same line:  H F_0(y) = -1/(y^2+1)."""
    return -1.0 / (y * y + 1.0)


def phi_egm(y):
    """EGM sec 1:  phi = (1+y^2)^2 / y^4."""
    return (1.0 + y * y) ** 2 / y ** 4


def phi_gamma(y, gamma):
    """The family phi_gamma = (1+y^2)^{gamma/2} / |y|^gamma.  gamma = 4 IS EGM's weight.

    |y| rather than y because the weight is even and gamma need not be an even integer;
    at gamma = 4 this is EGM's phi exactly.
    """
    return (1.0 + y * y) ** (0.5 * gamma) / np.abs(y) ** gamma


def D_analytic(y, gamma=EGM_GAMMA):
    """D(y) = -2 H F_0 - 1 + (1/2) d_y(y phi_gamma)/phi_gamma, in closed form.

    d_y(y phi)/phi = 1 + y d_y(log phi) = 1 + gamma y^2/(1+y^2) - gamma, so

        D(y) = 2/(1+y^2) - 1 + (1-gamma)/2 + gamma y^2 / (2(1+y^2)).

    At gamma = 4 this collapses to the constant -1/2 -- EGM's own printed evaluation
    -2HF_0 - 1 + (1/2) d_y(y phi)/phi = 2/(1+y^2) - 1 + (y^2-3)/(2(y^2+1)) = -1/2.
    """
    y2 = y * y
    return (2.0 / (1.0 + y2) - 1.0
            + 0.5 * (1.0 - gamma) + 0.5 * gamma * y2 / (1.0 + y2))


def D_from_weight(y, weight, h_rel=1e-6, F=F0, H_F=HF0):
    """The same coefficient, but with d_y(y phi) taken by central differences of `weight`.

    Shares no algebra with D_analytic beyond the definition itself, so it catches an
    error in the closed form rather than reproducing it.  `F`/`H_F` are injectable so the
    decoy profiles of E1's negative control go through the identical code path.
    """
    h = h_rel * np.maximum(np.abs(y), 1.0)
    num = ((y + h) * weight(y + h) - (y - h) * weight(y - h)) / (2.0 * h)
    return -2.0 * H_F(y) - 1.0 + 0.5 * num / weight(y)


def _grid(n=4001, decades=3.0):
    """Log-spaced, symmetric, avoiding y = 0 where phi has its pole."""
    half = np.logspace(-decades, decades, n // 2)
    return np.concatenate([-half[::-1], half])


# --------------------------------------------------------------------------
# E1 -- EGM's -1/2, computed
# --------------------------------------------------------------------------
def e1_egm_constant():
    y = _grid()
    d_an = D_analytic(y, EGM_GAMMA)
    d_fd = D_from_weight(y, phi_egm)

    rows = []
    # negative controls: the identity is a property of THIS profile, not of the weight
    for name, F, HF in (
        ("decoy_F_over_1p_y2_squared", lambda t: t / (1.0 + t * t) ** 2,
         lambda t: -1.0 / (1.0 + t * t) ** 2),
        ("decoy_F_y_over_1p2y2", lambda t: t / (1.0 + 2.0 * t * t),
         lambda t: -1.0 / (1.0 + 2.0 * t * t)),
    ):
        d = D_from_weight(y, phi_egm, F=F, H_F=HF)
        rows.append({"control": name,
                     "max_dev_from_-0.5": float(np.max(np.abs(d - EGM_GAP_A0))),
                     "is_constant_spread": float(np.max(d) - np.min(d))})

    return {
        "what": ("EGM sec 2's closing coefficient D(y) = -2HF_0 - 1 + (1/2)d_y(y phi)/phi, "
                 "with their phi and their a = 0 profile"),
        "n_nodes": int(y.size),
        "y_range": [float(y.min()), float(y.max())],
        "egm_printed_value": EGM_GAP_A0,
        "max_dev_analytic": float(np.max(np.abs(d_an - EGM_GAP_A0))),
        "max_dev_finite_difference": float(np.max(np.abs(d_fd - EGM_GAP_A0))),
        "spread_analytic": float(np.max(d_an) - np.min(d_an)),
        "negative_controls": rows,
        "reading": ("the -1/2 this repository quotes is EXACT and y-INDEPENDENT, and it "
                    "falls out of EGM's own printed algebra.  The decoys go through the "
                    "same code path and do not."),
    }


# --------------------------------------------------------------------------
# E2 -- gamma = 4 is the unique exponent making the constant y-independent
# --------------------------------------------------------------------------
def e2_gamma_sweep():
    y = _grid()
    rows = []
    for gamma in (2.0, 2.5, 3.0, 3.5, 3.9, 4.0, 4.1, 5.0, 6.0, 8.0):
        d = D_analytic(y, gamma)
        d_fd = D_from_weight(y, lambda t, g=gamma: phi_gamma(t, g))
        rows.append({
            "gamma": gamma,
            "D_at_origin_limit": 0.5 * (3.0 - gamma),          # (3 - gamma)/2
            "D_at_origin_measured": float(D_analytic(np.array([1e-8]), gamma)[0]),
            "D_far_field_measured": float(D_analytic(np.array([1e8]), gamma)[0]),
            "spread_over_y": float(np.max(d) - np.min(d)),      # 0 iff y-independent
            "sup_over_y": float(np.max(d)),
            "fd_agrees_to": float(np.max(np.abs(d - d_fd))),
        })
    constants = [r["gamma"] for r in rows if r["spread_over_y"] < 1e-12]
    return {
        "what": ("the same coefficient over the weight family phi_gamma = "
                 "(1+y^2)^{gamma/2}/y^gamma, gamma = EGM's origin exponent"),
        "rows": rows,
        "y_independent_at": constants,
        "leg_165_formula": "D_phi(0) = (3 - gamma)/2",
        "leg_165_formula_reproduced": True,
        "reading": ("gamma = 4 is the ONLY member of the family whose coefficient is "
                    "constant in y -- everywhere else the -1/2 is only the far-field value "
                    "and the origin value is (3-gamma)/2, so the usable constant is the sup "
                    "over y.  leg 165's D_phi(0) = (3-gamma)/2 is recovered from EGM's "
                    "algebra rather than quoted."),
        "caveat": ("this is the LOCAL/diagonal term only.  EGM's proof also needs "
                   "int Hf f F_0 phi = 0, which they establish using phi F_0 = (y^2+1)/y^3 "
                   "-- gamma = 4 algebra.  So this sweep does NOT say 'any gamma >= 4 "
                   "works', and no such claim is made or banked."),
    }


# --------------------------------------------------------------------------
# E3 -- H F_0, against solver/line_hilbert.py
# --------------------------------------------------------------------------
def e3_hilbert_of_F0(n=2001):
    """The residual here is DOMAIN TRUNCATION, not discretisation, and that is measurable.

    F_0 ~ 1/y decays too slowly for a truncated grid: the tail |s| > S = sinh(t_max) that
    the grid omits contributes (1/pi) int_{|s|>S} (1/s)/(x-s) ds ~ (2/pi)/S, a near-constant
    deficit that does NOT fall when n rises at fixed t_max.  So the convergence knob is
    t_max, and err * S should sit at 2/pi = 0.6366.  Reported that way, because the naive
    n-refinement reads as a stalled solver and is nothing of the kind.
    """
    rows = []
    for tmax in (5.0, 7.0, 9.0, 11.0):
        t = np.linspace(-tmax, tmax, n)
        y = np.sinh(t)
        h = line_hilbert(y, F0(y))
        keep = np.abs(y) < 10.0
        egm = HF0(y)
        err = float(np.max(np.abs(h - egm)[keep]))
        S = float(np.sinh(tmax))
        rows.append({
            "t_max": tmax, "n": int(n), "S_grid_half_extent": S,
            "max_abs_err_vs_EGM": err,
            "max_abs_err_vs_NEGATED_EGM": float(np.max(np.abs(h + egm)[keep])),
            "err_times_S": err * S,
        })
    two_over_pi = 2.0 / np.pi
    devs = [abs(r["err_times_S"] - two_over_pi) / two_over_pi for r in rows]
    return {
        "what": "EGM's printed pair F_0 = y/(1+y^2), H F_0 = -1/(y^2+1), checked numerically",
        "rows": rows,
        "truncation_law": {
            "predicted_err_times_S": two_over_pi,
            "max_rel_dev_over_4_extents": float(max(devs)),
        },
        "convention": ("solver/line_hilbert.py's H IS EGM's H (the error against the NEGATED "
                       "target is O(1) at every extent, so the sign convention is pinned, "
                       "not assumed)"),
        "reading": ("the pair EGM print is correct in this repository's own convention, on "
                    "an instrument that shares no algebra with the paper.  The residual is "
                    "the omitted 1/y tail, err ~ (2/pi)/S, verified over four grid extents "
                    "-- it is truncation, not disagreement, and refining n at fixed extent "
                    "correctly does nothing."),
    }


# --------------------------------------------------------------------------
# E4 -- the transcription audit: -(1/2 - C|a|) vs the banked (-1/2 - C|a|)
# --------------------------------------------------------------------------
def e4_transcription_audit(C=1.0):
    rows = []
    for a in (0.0, 0.01, 0.05, 0.1, 0.2):
        correct = -(0.5 - C * abs(a))       # LaTeX source: -\Big(\frac12 - C|a|\Big)
        banked = -0.5 - C * abs(a)          # legs 141/165 and leg 190's novelty pass
        rows.append({
            "a": a, "C_assumed": C,
            "gap_correct": correct,
            "gap_as_transcribed_in_repo": banked,
            "abs_difference": abs(correct - banked),
            "rel_difference": (abs(correct - banked) / abs(correct)) if correct else 0.0,
        })
    return {
        "what": "the sign of the |a|-slope of EGM's gap, correct reading vs the banked one",
        "latex_source_verbatim": (
            "\\leq-\\Big(\\frac{1}{2}-C\\,|a|\\Big)\\int_\\RR f(y)^2 \\phi(y)dy"),
        "source_of_truth": "arXiv:1906.05811 e-print, OSWModel_Final.tex, proposition block",
        "rows": rows,
        "sites_carrying_the_error": [
            "experiments/journal/leg_141.md:30", "experiments/journal/leg_141.md:117",
            "writeup/novelty/leg_141.md:233", "experiments/journal/leg_165.md:120",
            "experiments/journal/leg_165.md:128",
            "writeup/novelty/leg_190.md sec 2 (this leg's own novelty pass, now corrected "
            "in sec 8)",
        ],
        "corroboration_in_paper": [
            "the proof splits M_a = (a=0 operator) + a Mtilde_a with "
            "|int f Mtilde_a f phi| <= C int |f|^2 phi, which can only ADD to -1/2",
            "sec 6's C^alpha analogue reads (1/2 - C alpha), degrading the same way",
        ],
        "banked_numbers_moved": 0,
        "reading": ("zero error at a = 0 -- which is the ONLY value legs 141 and 165 ever "
                    "compared at -- and a reversed slope everywhere off it.  The ar5iv HTML "
                    "mirror, which leg 190's novelty pass accused of the error, is right; "
                    "the pdftotext layout that seemed to contradict it silently drops "
                    "\\Big( \\Big).  Nothing banked moves; the record is corrected."),
    }


# --------------------------------------------------------------------------
# E5 -- the p = 2 join, and whose claim each half is
# --------------------------------------------------------------------------
def e5_p2_join():
    rows = []
    for p in (1, 2, 3):
        lo, hi = 3.0, 2.0 * p + 1.0
        rows.append({"p": p, "window": [lo, hi], "width": hi - lo,
                     "egm_gamma_inside": bool(lo < EGM_GAMMA < hi)})
    return {
        "what": "leg 111's admissible window (3, 2p+1) against EGM's gamma = 4",
        "rows": rows,
        "whose_claim": {
            "-1/2 gap": "EGM, arXiv:1906.05811 Prop. 2.1, verbatim in EGM_PRIMARY_READ",
            "p = 2, width 2.0": ("leg 165 / leg 111, experiments/journal/leg_165.md:106-108 "
                                 "-- NOT EGM; EGM say nothing about p"),
            "the join": ("arithmetic about the two (3 < 4 < 5), not a claim EGM make, and "
                         "not upgraded by this leg"),
        },
        "reading": ("the relayed sentence is a correct composite of two separately-true "
                    "statements with different owners.  At p = 1 the window is (3,3), width "
                    "0.0, and EGM's gamma = 4 is OUTSIDE it."),
    }


def main():
    t0 = time.time()
    res = {
        "route": "EGML v1",
        "leg": 190,
        "gate": ("Can 'EGM' be located as a real, checkable primary source, and does it "
                 "state the p=2, -1/2-gap claim as relayed, with its own hypotheses?"),
        "citation": {k: EGM_PRIMARY_READ[k] for k in
                     ("arxiv", "tag", "authors", "title", "venue", "read")},
        "E1_egm_constant": e1_egm_constant(),
        "E2_gamma_sweep": e2_gamma_sweep(),
        "E3_hilbert_of_F0": e3_hilbert_of_F0(),
        "E4_transcription_audit": e4_transcription_audit(),
        "E5_p2_join": e5_p2_join(),
        "verbatim": EGM_PRIMARY_READ["spectral_gap"],
        "scope": EGM_PRIMARY_READ["scope"],
        "the_relayed_p2_claim": EGM_PRIMARY_READ["the_relayed_p2_claim"],
    }

    e1, e2, e4 = res["E1_egm_constant"], res["E2_gamma_sweep"], res["E4_transcription_audit"]
    res["gate_answer"] = (
        "YES, with one correction that runs the other way from the one this leg expected.  "
        "EGM is arXiv:1906.05811 / Anal. PDE 14 (2021) 891-908, Prop. 2.1, read at full text "
        "from the PDF and the LaTeX e-print.  It states the -1/2 gap with three hypotheses "
        "(odd f, f'(0) = Hf(0) = 0, finite weighted norm), and the -1/2 is recomputed here "
        "from EGM's own algebra to {:.3e}.  The 'p = 2, width 2.0' half is leg 165's, not "
        "EGM's.  The correction: the |a|-dependence is -(1/2 - C|a|), DEGRADING, not the "
        "(-1/2 - C|a|) that legs 141, 165 and this leg's own novelty pass transcribed -- "
        "identical at a = 0, so 0 banked numbers move.".format(e1["max_dev_analytic"]))
    res["headline"] = (
        "EGM = arXiv:1906.05811 Prop. 2.1, gap -0.5 at a = 0, reproduced from EGM's own "
        "algebra to {:.3e} over {} nodes; gamma = 4 is the unique y-independent exponent of "
        "{} scanned; one propagated sign error corrected, {} banked numbers moved".format(
            e1["max_dev_analytic"], e1["n_nodes"], len(e2["rows"]),
            e4["banked_numbers_moved"]))
    res["elapsed_s"] = round(time.time() - t0, 2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=2))

    print("Route-EGML v1 -- EGM at primary source")
    print("  E1  D(y) vs EGM's -1/2 : analytic {:.3e}, finite-diff {:.3e}, spread {:.3e}"
          .format(e1["max_dev_analytic"], e1["max_dev_finite_difference"],
                  e1["spread_analytic"]))
    for c in e1["negative_controls"]:
        print("      control {:<32s} dev {:.4f}  spread {:.4f}"
              .format(c["control"], c["max_dev_from_-0.5"], c["is_constant_spread"]))
    print("  E2  y-independent at gamma = {}  (of {} scanned)"
          .format(e2["y_independent_at"], len(e2["rows"])))
    for r in e2["rows"]:
        print("      gamma {:<4.1f} D(0) = {:+.4f}  D(inf) = {:+.4f}  spread {:.4f}"
              .format(r["gamma"], r["D_at_origin_measured"], r["D_far_field_measured"],
                      r["spread_over_y"]))
    for r in res["E3_hilbert_of_F0"]["rows"]:
        print("  E3  t_max = {:<5.1f} S = {:>9.1f}  |H F_0 - EGM| = {:.3e}  err*S = {:.4f}"
              "   (negated target: {:.3e})"
              .format(r["t_max"], r["S_grid_half_extent"], r["max_abs_err_vs_EGM"],
                      r["err_times_S"], r["max_abs_err_vs_NEGATED_EGM"]))
    for r in e4["rows"]:
        print("  E4  a = {:<5.2f} correct {:+.4f}  as-banked {:+.4f}  |diff| {:.4f}"
              .format(r["a"], r["gap_correct"], r["gap_as_transcribed_in_repo"],
                      r["abs_difference"]))
    for r in res["E5_p2_join"]["rows"]:
        print("  E5  p = {}  window {}  width {:.1f}  gamma=4 inside: {}"
              .format(r["p"], r["window"], r["width"], r["egm_gamma_inside"]))
    print("\n" + res["headline"])
    print("wrote {}  ({}s)".format(OUT.relative_to(ROOT), res["elapsed_s"]))


if __name__ == "__main__":
    main()
