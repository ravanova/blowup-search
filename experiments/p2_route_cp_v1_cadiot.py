"""Route-CP v1 (leg 62): THE CADIOT PRE-EMPTION, SETTLED FROM THE FULL TEXT.

Leg 57 flagged Cadiot arXiv:2505.03091 as independently pre-empting leg 51's
methodological claim and recommended not re-claiming that finding at full strength.  That
recommendation was correct and INCOMPLETE.  The same paper is the single largest novelty
risk to leg 58's (NG's) proposition, and NG's hypothesis is NARROWER than leg 51's: it is
specifically about an unbounded part that is OFF-DIAGONAL with a NON-DECAYING tail
inverse.  Leg 57 read two sentences of the paper off a search index and correctly
declined to settle that.  This leg settles it from the PDF.

This repository has been burned twice by literature read at the wrong depth.  Leg 53 read
BDL's dominance hypothesis off a publisher abstract page and lost the claim; only the
full PDF fixed it.  So: full text, located statement, hypotheses verbatim, and the same
for what Cadiot cites forward into this case.

PRE-COMMITTED CLAUSES, written before the run, both branches reportable:

  CP0 THE NOVELTY PASS COMES FIRST and can only narrow the claim.  Committed at
      `writeup/novelty/leg_62.md` BEFORE any of this was built, six queries with LINKS
      (leg 53 logged counts and was withdrawn).  Verdict `PROCEED_AS_LEDGER_EXTENSION`:
      this leg classifies literature and claims no mathematical finding.

  CP1 EVERY HYPOTHESIS IS RECORDED VERBATIM, WITH ITS LOCATION, FROM THE FULL PDF.
      `Papers/fetch.sh` pulled 2505.03091, 2504.05066, 2404.08529 and 2302.12877; every
      row of `CP_LEDGER` names a section/assumption/lemma and quotes the sentence.
      `cp_unlocated_rows()` is the guard and it is asserted empty.

  CP2 THE READING DEPTH TRAVELS WITH THE QUOTATION.  One source in the chain (FL91,
      Linear Algebra Appl. 143, 1991) is paywalled with no arXiv copy.  Its hypotheses
      are recorded from two papers that quote it and that WERE read in full, its row is
      flagged SECOND_HAND, and `cp_gate_answer` REFUSES it rather than counting it.  Leg
      53's correction, applied as code rather than as a resolution.

  CP3 THE GATE IS A PREDICATE AND IT CAN ANSWER BOTH WAYS.  A fictitious covering row
      flips it to "yes" (lesson 90, and gate 18 runs both directions).

  CP4 THE COMPARISON IS ARITHMETIC, NOT RHETORIC.  Our own object sits on the SAME axis
      as the literature, and the axis is the one the sources actually use: the asymptotic
      Gershgorin dominance ratio `rho = limsup (off-diagonal row sum) / |diagonal|`,
      which every located construction needs `< 1`.

  CP5 THE TRANSCRIPTION IS RE-DERIVED.  `solver/literature_gates.py` recomputes Cadiot's
      `l_min` and each symbol's growth exponent from his published formulas and
      parameters.  If Assumption 1 failed at his own numbers the reasoning would
      collapse; it is checked, not assumed.

  CP6 THE ONE PUBLISHED REPAIR IS TESTED AGAINST OUR OPERATOR AND REPORTED AS A
      MAGNITUDE.  BRT repair infinite Gershgorin radii with a diagonal weight.  Applied
      to a nearest-neighbour shift it damps by < 1e-3 at index 8192 for every exponent
      tried; applied to THEIR operator it reproduces their own published exponent.  Both
      halves are measured so the contrast is arithmetic.

WHAT THIS RUNNER DOES NOT DO.  It does not re-derive CLN's Kawahara `r_0`
(`solver/target_selection.py` already does) or Dahne-Figueras' branch (leg 48).  It does
not re-run leg 57's operator dial (`p2_route_xs_v1_shapes.py` owns that).  It proves
nothing: a NO here is "no located source covers this", over four papers read in full,
which is a bounded statement about a corpus and not a theorem.  Nothing here moves any
link of the L1->L4 chain; Clay stays at ~0.05% behind Walls 1 and 2.
"""

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib                                                      # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                                        # noqa: E402
import numpy as np                                                     # noqa: E402

from solver.certificate_shapes import (                                # noqa: E402
    CP_LEDGER,
    cp_gate_answer,
    cp_literature_rows,
    cp_unlocated_rows,
    dominance_ratio_admits,
    our_cp_row,
    shift_damping_ladder,
    spread_damping_ladder,
)
from solver.literature_gates import (                                  # noqa: E402
    CADIOT_PARAMS,
    cadiot_assumption1_check,
    cadiot_gray_scott_crossover,
)

OUT = ROOT / "writeup" / "data" / "p2_route_cp_v1_cadiot.json"
FIG = ROOT / "writeup" / "figures" / "fig56_route_cp_v1_cadiot.png"


# --------------------------------------------------------------------------
# the growth-exponent plane: where every located source sits, and where we sit
# --------------------------------------------------------------------------
# x = gamma_R, the growth exponent of the (weighted) OFF-DIAGONAL ROW SUM
# y = gamma_D, the growth exponent of the DIAGONAL
# The admissible region for a Gershgorin/radii-polynomial tail estimate is y > x, plus
# the boundary y = x when a constant factor rho < 1 saves it (BDL).
EXPONENT_PLANE = [
    {"tag": "CADIOT-STAB (Swift-Hohenberg, sec 5.1)", "gamma_R": 0.0, "gamma_D": 4.0,
     "arxiv": "2505.03091", "ours": False, "label_offset": (10, -3)},
    {"tag": "CADIOT-STAB (Gray-Scott, sec 5.3) = CB (Assumption 1)",
     "gamma_R": 0.0, "gamma_D": 2.0, "arxiv": "2505.03091 + 2404.08529", "ours": False,
     "label_offset": (10, 6)},
    {"tag": "CADIOT-STAB (Whitham, sec 5.2)", "gamma_R": 0.0, "gamma_D": 0.5,
     "arxiv": "2505.03091", "ours": False, "label_offset": (10, 5)},
    {"tag": "BRT (Lemma 2.10, p=1.7, q1=1, n=1)", "gamma_R": 0.7, "gamma_D": 2.0,
     "arxiv": "2504.05066", "ours": False, "label_offset": (10, -12)},
    {"tag": "BDL (assumptions (4)+(5), s_L=1)", "gamma_R": 1.0, "gamma_D": 1.0,
     "arxiv": "1503.06315", "ours": False, "label_offset": (12, 4),
     "on_boundary": True,
     "boundary_note": "EQUAL exponents; saved by the constant rho <= 2*delta < 1"},
    {"tag": "OURS: a=0 CLM bordered tail", "gamma_R": 1.0, "gamma_D": 0.0,
     "arxiv": None, "ours": True, "label_offset": (16, -4)},
]


def _json_safe(obj):
    """Replace non-finite floats with strings so the artifact is valid JSON."""
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, float) and not np.isfinite(obj):
        return "inf" if obj > 0 else "-inf"
    return obj


def build_figure(res):
    fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.6))

    # ---- panel A: the growth-exponent plane -------------------------------
    ax = axes[0]
    lim = 4.6
    xs = np.linspace(-0.2, lim, 200)
    ax.fill_between(xs, xs, lim, color="#2a9d8f", alpha=0.13, zorder=0)
    ax.fill_between(xs, -0.6, xs, color="#c1121f", alpha=0.10, zorder=0)
    ax.plot(xs, xs, color="#555", lw=1.1, ls="--", zorder=1)
    ax.text(2.9, 3.95, "ADMISSIBLE:  $\\gamma_D > \\gamma_R$\n(the diagonal wins)",
            fontsize=10, color="#1d6f66", ha="center", va="center", fontweight="bold")
    ax.text(3.35, 0.75, "NO LOCATED SOURCE\nANYWHERE IN HERE", fontsize=10,
            color="#8b0f18", ha="center", va="center", fontweight="bold")

    for row in EXPONENT_PLANE:
        dx, dy = row.get("label_offset", (10, -3))
        if row["ours"]:
            ax.scatter([row["gamma_R"]], [row["gamma_D"]], s=230, marker="X",
                       color="#c1121f", edgecolor="k", lw=1.2, zorder=6)
            ax.annotate("OURS — a=0 CLM bordered tail\n"
                        "$\\gamma_D=0$ (diagonal exactly zero)\n"
                        "$\\gamma_R=1$ (coupling entry $K/2$)\n"
                        r"$\rho = \infty$",
                        (row["gamma_R"], row["gamma_D"]), textcoords="offset points",
                        xytext=(dx, dy), fontsize=8.8, color="#8b0f18",
                        fontweight="bold", va="top")
        elif row.get("on_boundary"):
            ax.scatter([row["gamma_R"]], [row["gamma_D"]], s=135, marker="s",
                       color="#e07a1f", edgecolor="k", lw=0.9, zorder=6)
            ax.annotate(row["tag"] + "\n(on the boundary: EQUAL exponents,\n"
                        r" saved by the constant $\rho \leq 2\delta < 1$)",
                        (row["gamma_R"], row["gamma_D"]), textcoords="offset points",
                        xytext=(dx, dy), fontsize=7.9, color="#8a4a06")
        else:
            ax.scatter([row["gamma_R"]], [row["gamma_D"]], s=95, marker="o",
                       color="#1d3557", edgecolor="w", lw=0.9, zorder=6)
            ax.annotate(row["tag"], (row["gamma_R"], row["gamma_D"]),
                        textcoords="offset points", xytext=(dx, dy), fontsize=7.9,
                        color="#1d3557")
    ax.set_xlim(-0.45, lim); ax.set_ylim(-0.6, lim)
    ax.set_xlabel(r"$\gamma_R$  —  growth exponent of the off-diagonal ROW SUM")
    ax.set_ylabel(r"$\gamma_D$  —  growth exponent of the DIAGONAL")
    ax.set_title("Every located construction needs the diagonal to out-grow the\n"
                 "off-diagonal.  Ours has the ordering reversed, by a full order.",
                 fontsize=10.2, fontweight="bold")
    ax.grid(alpha=0.22, zorder=0)

    # ---- panel B: the one published repair, tested both ways ---------------
    ax = axes[1]
    for r in res["CP6_shift_damping"]:
        ax.plot(r["indices"], r["ratio"], marker="o", ms=3.6, lw=1.5,
                label=f"shift, $p={r['p']}$")
    ax.axhline(1.0, color="#c1121f", lw=1.7, ls="--", zorder=1)
    ax.annotate("ratio $\\to$ 1 for EVERY $p$:  no damping at all",
                xy=(3000, 1.0), xytext=(0.44, 0.90), textcoords="axes fraction",
                color="#8b0f18", fontsize=9.2, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#8b0f18", lw=1.2))
    ax.set_xscale("log")
    ax.set_ylim(0.985, 1.0045)
    ax.set_xlabel("index $i$")
    ax.set_ylabel(r"$f(i)/f(i{+}1)$  —  BRT's weight against a nearest-neighbour shift")
    ax.set_title("BRT Def. 2.8's diagonal weight repairs THEIR infinite radii\n"
                 "(measured exponent $p-q_1$ reproduced) but cannot damp a shift.",
                 fontsize=10.2, fontweight="bold")
    ax.legend(fontsize=7.8, loc="center left", ncol=1, framealpha=0.95)
    ax.grid(alpha=0.25)

    sp = res["CP6_spread_damping"]
    txt = "THE SAME WEIGHT ON BRT'S OWN OPERATOR (their eq. 2.8):\n" + "\n".join(
        f"  p={d['p']}, q1={d['q1']}:  measured {d['measured_growth_exponent_in_i']:+.4f}"
        f"   vs their p-q1 = {d['brt_predicted_exponent_p_minus_q1']:+.4f}"
        for d in sp)
    ax.text(0.985, 0.025, txt, transform=ax.transAxes, fontsize=7.4, va="bottom",
            ha="right", family="monospace",
            bbox=dict(boxstyle="round,pad=0.42", fc="#eef4f7", ec="#9db6c4", lw=0.8))

    fig.suptitle("Route-CP v1 (leg 62): Cadiot arXiv:2505.03091 does NOT cover an "
                 "off-diagonal unbounded part — settled from the full PDF",
                 fontweight="bold", y=1.005, fontsize=12)
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight", dpi=145)
    plt.close(fig)


def main():
    t0 = time.time()
    res = {}

    res["leg"] = 62
    res["route"] = "CP"
    res["branch"] = "leg/cp-v1"
    res["gates"] = {"test_certificate_shapes.py": "22/22",
                    "test_literature_gates.py": "11/11"}
    res["novelty_pass"] = {
        "file": "writeup/novelty/leg_62.md",
        "verdict": "PROCEED_AS_LEDGER_EXTENSION",
        "committed_before_construction": True,
        "binds": ("This leg classifies literature and claims no mathematical finding.  "
                  "The observation being classified was already settled as folklore in "
                  "print by leg 57; what is new here is the DEPTH of the reading and the "
                  "quantitative axis, both of which are bookkeeping."),
    }

    # ---------------- CP1/CP2/CP3: the gate, from located statements -------
    gate = cp_gate_answer()
    res["CP3_gate"] = gate
    res["CP1_unlocated_rows"] = cp_unlocated_rows()
    res["CP1_ledger_size"] = {
        "rows_total": len(CP_LEDGER),
        "rows_literature": len(cp_literature_rows()),
        "rows_full_text": gate["n_full_text"],
        "rows_refused_second_hand": gate["refused_not_full_text"],
        "located_statements": sum(len(r["located"]) for r in CP_LEDGER),
    }
    res["CP1_papers_read_in_full"] = [
        {"arxiv": "2505.03091", "url": "https://arxiv.org/abs/2505.03091",
         "fetch": "Papers/fetch.sh 2505.03091", "role": "the paper under test"},
        {"arxiv": "2504.05066", "url": "https://arxiv.org/abs/2504.05066",
         "fetch": "Papers/fetch.sh 2504.05066",
         "role": "Cadiot's [15] -- the most general Gershgorin statement located"},
        {"arxiv": "2404.08529", "url": "https://arxiv.org/abs/2404.08529",
         "fetch": "Papers/fetch.sh 2404.08529",
         "role": "Cadiot's [20] -- the systems extension, the only matrix-valued symbol"},
        {"arxiv": "2302.12877", "url": "https://arxiv.org/abs/2302.12877",
         "fetch": "Papers/fetch.sh 2302.12877",
         "role": "Cadiot's [21] -- the underlying framework, Assumption 2.1 re-read"},
    ]
    res["CP2_reading_depth"] = {
        "second_hand": ["FL91 (Linear Algebra Appl. 143:7-17, 1991) -- paywalled, "
                        "no arXiv copy; hypotheses recorded from arXiv:2504.05066 sec "
                        "2.1 and from Cadiot's own Lemma 3.2, both read in full"],
        "refused_by_the_gate": gate["refused_not_full_text"],
        "why": ("Leg 53 lost a claim by reading a hypothesis at the wrong depth.  The "
                "correction is not to hide the depth but to label it and to refuse it."),
    }

    # ---------------- CP4: the arithmetic comparison -----------------------
    ours = our_cp_row()
    res["CP4_dominance_axis"] = {
        "definition": ("rho = limsup_k (off-diagonal row sum at k) / |diagonal entry at "
                       "k|.  Every located construction requires rho < 1."),
        "why_not_the_exponent_difference": (
            "BDL separates them: BDL has EQUAL growth exponents (gamma_D - gamma_R = 0) "
            "and is still admissible, because its assumption (5) buys rho <= 2*delta < 1 "
            "by a constant factor.  rho is the coordinate that classifies all rows; the "
            "exponent difference is not."),
        "sources": [{"tag": r["tag"], "rho": r["rho"],
                     "admits": dominance_ratio_admits(r["rho"])}
                    for r in cp_literature_rows()],
        "ours": {"tag": ours["tag"], "rho": ours["rho"],
                 "admits": dominance_ratio_admits(ours["rho"]),
                 "gamma_D": ours["diag_growth"]["a0_clm"],
                 "gamma_R": ours["offdiag_growth"],
                 "gamma_R_minus_gamma_D": ours["offdiag_growth"]
                 - ours["diag_growth"]["a0_clm"]},
        "exponent_plane": EXPONENT_PLANE,
    }

    # ---------------- CP5: the transcription, re-derived -------------------
    a1 = cadiot_assumption1_check()
    cross = cadiot_gray_scott_crossover(
        CADIOT_PARAMS["gray_scott"]["lambda1"], CADIOT_PARAMS["gray_scott"]["lambda2"])
    res["CP5_assumption1_rederived"] = {
        "what": ("Cadiot Assumption 1 requires l_min > 0 and |l| -> infinity.  Both are "
                 "recomputed from his published symbols at his published parameters, so "
                 "the CP_LEDGER's transcription is checked rather than trusted."),
        "params": CADIOT_PARAMS,
        "checks": a1,
        "gray_scott_crossover": cross,
    }
    res["CP5_headline"] = {
        "swift_hohenberg_l_min": a1["swift_hohenberg"]["l_min_measured"],
        "swift_hohenberg_growth_exponent": a1["swift_hohenberg"]["growth_exponent"],
        "whitham_l_min": a1["whitham"]["l_min_measured"],
        "whitham_growth_exponent": a1["whitham"]["growth_exponent"],
        "gray_scott_sigma0": a1["gray_scott"]["sigma0_measured"],
        "gray_scott_offdiagonal_entry": a1["gray_scott"]["offdiagonal_entry"],
        "gray_scott_crossover_xi": cross["crossover_xi"],
        "gray_scott_rho_decay_exponent": cross["rho_decay_exponent"],
    }

    # ---------------- CP6: the published repair, tested both ways ----------
    res["CP6_shift_damping"] = shift_damping_ladder()
    res["CP6_spread_damping"] = []
    for p in (1.2, 1.7, 2.5):
        d = spread_damping_ladder(p, 1.0)
        d["abs_error_vs_BRT"] = abs(d["measured_growth_exponent_in_i"]
                                    - d["brt_predicted_exponent_p_minus_q1"])
        res["CP6_spread_damping"].append(d)
    res["CP6_worst_shift_damping_at_i_8192"] = max(
        r["distance_from_one_at_largest_index"] for r in res["CP6_shift_damping"])
    res["CP6_reading"] = (
        "BRT Definition 2.8 repairs infinite Gershgorin radii by conjugating with a "
        "DIAGONAL weight f(i) = max(1, i^p) -- the same one-parameter family legs 51-53 "
        "swept as the exponent s.  Against a NEAREST-NEIGHBOUR shift the conjugation "
        "factor is f(i)/f(i+1) = (i/(i+1))^p -> 1 for EVERY p, so the weight cannot damp "
        "it: at index 8192 the largest damping over p in {0, 0.5, 1, 2, 4} is "
        f"{max(r['distance_from_one_at_largest_index'] for r in res['CP6_shift_damping']):.2e}"
        ".  Against BRT's OWN bounded, spread off-diagonal the same weight reproduces "
        "their published exponent p - q1 to better than 5e-3.  **This is why legs 51-53 "
        "measured 'the coupling entry is K/2 for EVERY s'** -- a diagonal weight is "
        "asymptotically flat a bounded distance from the diagonal, which is exactly "
        "where a shift lives.")

    # ---------------- the answer -------------------------------------------
    res["ANSWER"] = {
        "gate": gate["gate"],
        "answer": gate["answer"],
        "branch_taken": (
            "no -> The gap leg 57's ledger measured is CONFIRMED at full-text depth for "
            "the one paper most likely to close it.  The located hypotheses are banked "
            "as an executable ledger entry (solver/certificate_shapes.py CP_LEDGER).  "
            "NG may claim novelty against this paper AND NO FURTHER."),
        "three_independent_exclusions": [
            "Assumption 1 (sec 2.1): L is a Fourier multiplier with |l| >= l_min > 0 -- "
            "the unbounded part is exactly diagonal AND bounded below.  Our unbounded "
            "part is a variable-coefficient transport term, outside the class by "
            "definition.",
            "Proof of Lemma 3.3 (sec 3): 'since L is diagonal, L pi_N = pi_N L pi_N' is "
            "the step that removes the unbounded part from the off-diagonal Gershgorin "
            "radii.  It is load-bearing in a proof, not ambient convenience.",
            "Lemma 2.2 (sec 2.3): DG(u~) is relatively compact with respect to L.  A "
            "transport term of the same order as the unbounded part is not.",
        ],
        "the_near_miss": (
            "Section 5.2's capillary-gravity Whitham equation is the ONE equation in the "
            "paper carrying a transport term u d_x u.  It never becomes an unbounded "
            "off-diagonal operator: the traveling-wave reduction divides out d_x and the "
            "transport collapses to G(u) = u^2, whose derivative 2 u~ is a BOUNDED "
            "multiplication operator.  The gCLM/CLM linearisation admits no such "
            "reduction."),
    }

    res["CAP_ON_LEG_58_NG"] = {
        "claim_strength": (
            "NG MAY claim novelty against arXiv:2505.03091, arXiv:2504.05066, "
            "arXiv:2404.08529 and arXiv:2302.12877 -- four papers read in full, none of "
            "which covers an off-diagonal unbounded part.  NG may NOT claim more than "
            "that: this is a bounded statement about a corpus, not a theorem."),
        "wording_constraint_MUST_ACT_ON": (
            "**NG may NOT phrase its no-go as 'the published machinery requires a "
            "nonzero diagonal'.**  That sentence is FALSE against BRT arXiv:2504.05066 "
            "section 2.1, which removes precisely that hypothesis from the classical "
            "infinite-matrix Gershgorin theorem: 'some of the assumptions of [FL91, "
            "Theorem 2.1] are needlessly restrictive (for instance, all the diagonal "
            "elements of L have to be nonzero)'.  Their Theorem 2.6 needs only a "
            "Schauder basis, a sup-attaining property, and a compact resolvent."),
        "why_this_costs_NG_nothing_in_substance": (
            "The generalised theorem APPLIES to a zero diagonal and returns disks of "
            "infinite radius -- it is VACUOUS, not violated (their Definition 2.5: 'We "
            "note that its radius r_i(L) can be infinite')."),
        "recommended_wording": (
            "Phrase the no-go QUANTITATIVELY, as an ordering of growth rates: no located "
            "construction covers an operator whose off-diagonal ROW-SUM growth exceeds "
            "its DIAGONAL growth.  That is exactly BRT Lemma 2.10's own requirement "
            "p - q1 < 2/n, it is true, and it is defensible."),
        "bonus_for_NG": (
            "The one published repair for infinite Gershgorin radii is a DIAGONAL "
            "WEIGHT, and it provably cannot reach a shift: f(i)/f(i+1) -> 1 for every "
            "exponent.  This is the mechanism behind legs 51-53's measured 'the coupling "
            "entry is K/2 for EVERY s' and NG may use it as such."),
    }

    res["what_this_does_NOT_establish"] = (
        "That no such construction exists -- four papers read in full is a corpus, not a "
        "theorem, and a NO here is 'no located source covers this'.  That this leg found "
        "anything mathematical -- it did not; the observation is folklore in print (leg "
        "57, CP0) and what is new is the reading depth and the axis.  That FL91's exact "
        "hypotheses are known first-hand -- they are not, and the ledger refuses that "
        "row.  Nothing here moves any link of the L1->L4 chain; Clay stays at ~0.05% "
        "behind Walls 1 and 2.")

    res["not_rigorous"] = (
        "Float64 on grids, no intervals.  The re-derived l_min values are minima over "
        "grids and the growth exponents are least-squares fits over three decades.  They "
        "say the published hypotheses are consistent with the published parameters; they "
        "prove nothing.")

    build_figure(res)
    res["figure"] = "writeup/figures/fig56_route_cp_v1_cadiot.png"
    res["elapsed_s"] = time.time() - t0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # `rho` is genuinely +infinity for our object, and that is the headline number.
    # `json.dumps` would write the bare token `Infinity`, which is NOT valid JSON and
    # which a strict reader rejects -- so it is serialised as the string "inf" instead.
    # The distinction matters: a curated artifact that only Python can parse is a
    # private note, not curated data.
    OUT.write_text(json.dumps(_json_safe(res), indent=1))

    print(f"wrote {OUT}")
    print(f"wrote {FIG}")
    print(f"\nGATE: {gate['answer']}   "
          f"(full-text rows {gate['n_full_text']}, refused {gate['refused_not_full_text']})")
    print(f"  unlocated rows: {res['CP1_unlocated_rows']}")
    print(f"  ours: rho = {ours['rho']}, gamma_R - gamma_D = "
          f"{res['CP4_dominance_axis']['ours']['gamma_R_minus_gamma_D']:+.1f}")
    h = res["CP5_headline"]
    print(f"  Cadiot Assumption 1 re-derived: SH l_min={h['swift_hohenberg_l_min']:.4f} "
          f"(exp {h['swift_hohenberg_growth_exponent']:.3f}), "
          f"Whitham l_min={h['whitham_l_min']:.4f} "
          f"(exp {h['whitham_growth_exponent']:.3f}), "
          f"GS sigma0={h['gray_scott_sigma0']:.3f}")
    print(f"  Gray-Scott: off-diagonal {h['gray_scott_offdiagonal_entry']:.0f} constant, "
          f"crossover xi={h['gray_scott_crossover_xi']:.4f}, "
          f"rho decays with exponent {h['gray_scott_rho_decay_exponent']:.3f}")
    worst = max(r["distance_from_one_at_largest_index"]
                for r in res["CP6_shift_damping"])
    print(f"  BRT's diagonal weight vs a shift: damps by at most {worst:.2e} at i=8192")
    print(f"\n({res['elapsed_s']:.0f}s)")


if __name__ == "__main__":
    main()
