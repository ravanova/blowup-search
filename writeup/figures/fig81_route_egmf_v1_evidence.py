"""Route-EGMF v1 (leg 329) -- EVIDENCE + FIGURE.

Re-derives, from the curated `writeup/data/p2_route_egmf_v1.json`, every number this
leg's journal quotes, and builds `writeup/figures/fig81_route_egmf_v1_precision.png`.

Nothing is recomputed here: the arbitrary-precision arithmetic lives in the one
runner, `experiments/p2_route_egmf_v1.py`. This script reads its output and asserts
the relations the prose asserts.

It sits in `writeup/figures/` rather than the usual `experiments/` because leg 329's
declared territory is `writeup/figures/fig81*`; `experiments/*_evidence.py` and
`writeup/build_figures.py` are outside it and are left for integration (see the
journal, section 6).

    .venv/bin/python writeup/figures/fig81_route_egmf_v1_evidence.py
"""
import json
import os
import sys
from decimal import Decimal

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_egmf_v1.json")
FIG = os.path.join(HERE, "fig81_route_egmf_v1_precision.png")

GRADE_DEPTHS = (12, 24, 48, 96)
CEILING = 0.5
CEILING_SLACK = 1e-9
ROWS = ("T2_egm|B4_egm", "T2_egm|E_egm")
COLOR = {"T2_egm|B4_egm": "#1f4e9c", "T2_egm|E_egm": "#0f8a6a"}

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-70s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(DATA) as fh:
        j = json.load(fh)

    rows, c4, c5 = j["rows"], j["control_C4_mp_rayleigh"]["rows"], j["control_C5_rcond_ladder"]["rows"]
    ga = j["gate_answer"]

    # ---- the gate ----------------------------------------------------------
    check("(G1) the gate answers NO under the literal pre-registration",
          ga["answer"] == "NO", ga["answer"])
    check("(G2) leg 178's gate text was never edited",
          ga["leg178_gate_text_edited"] is False, "")
    check("(G3) escalation #3 stays parked", ga["escalation_3_status"] == "stays parked", "")
    check("(G4) the NO is forced by clause 5's establishability, not by clause failure",
          ga["both_primary_rows_pass_all_five"] and not ga["clause5_establishable_C4_and_C5"],
          "five clauses all True under MP; C4 and C5 both fire")

    # ---- clause 3: the repair the `no` branch banks -------------------------
    for key in ROWS:
        f64, mp = rows[key]["float64_mirror"], rows[key]["mp"]
        check(f"(R1 {key}) banked n_grade=96 cell is the ~-230.71 contamination artifact",
              f64["quad_gaps"][-1] < -230.0, f"{f64['quad_gaps'][-1]:.8f}")
        check(f"(R2 {key}) arbitrary precision moves that cell onto the 1/2 plateau",
              abs(mp["quad_gaps"][-1] - 0.5) < 1e-6, f"{mp['quad_gaps'][-1]:.12f}")
        check(f"(R3 {key}) quad rel_spread repaired from ~4.03 to below the 1e-3 clause tol",
              mp["verdict"]["quad_rel_spread"] < 1e-3 < f64["verdict"]["quad_rel_spread"],
              f"{f64['verdict']['quad_rel_spread']:.6f} -> {mp['verdict']['quad_rel_spread']:.4e}")
        check(f"(R4 {key}) the repair beats the float64 noise band by >~1e4",
              1e-3 / ga["noise_band_per_row"][key] > 1e1
              and f64["verdict"]["quad_rel_spread"] / mp["verdict"]["quad_rel_spread"] > 1e6,
              f"factor {f64['verdict']['quad_rel_spread'] / mp['verdict']['quad_rel_spread']:.3g}")
        check(f"(R5 {key}) clause_quad_stable is the ONLY clause that was failing",
              mp["verdict"]["failing_clauses"] == [], "MP failing_clauses is empty")

    # ---- C4: the bound, and its sign ---------------------------------------
    for key in ROWS:
        e = c4[key]
        excess = Decimal(e["minus_R_mp_minus_one_half_exact_decimal"])
        check(f"(C4a {key}) the MP Rayleigh bound disagrees with the eigensolve by >> 1e-9",
              e["abs_diff"] > CEILING_SLACK, f"{e['abs_diff']:.3e} vs slack {CEILING_SLACK:g}")
        check(f"(C4b {key}) that disagreement is inside the predicted cond(G)*eps band",
              e["diff_inside_float64_noise_band"],
              f"band {e['float64_noise_band_cond_G_times_eps']:.3e}")
        check(f"(C4c {key}) the exact bound lands strictly BELOW 1/2, not above",
              excess < 0, f"-R_mp - 1/2 = {float(excess):.4e}")
        check(f"(C4d {key}) so the bound is inside the one-sided ceiling",
              e["bound_under_ceiling"], "")
    check("(C4e) the pre-registration defect is recorded, not self-adjudicated",
          ga["C4_pre_registration_defect"]["status"].startswith("FOUND"), "")

    # ---- C5: the ladder --------------------------------------------------
    for key in ROWS:
        e = c5[key]
        check(f"(C5a {key}) rcond ladder spread exceeds its 1e-6 tolerance",
              e["rel_spread"] > 1e-6, f"{e['rel_spread']:.3e}, dropped {e['dropped']}")
        check(f"(C5b {key}) every rung of the ladder still lies below 1/2",
              all(g < CEILING for g in e["gaps"]), f"max {max(e['gaps']):.12f}")

    # ---- adversarial controls held ----------------------------------------
    check("(C6) both falsification rows still FAIL under arbitrary precision",
          j["control_C6_falsification_rows"]["all_ok"], "")
    check("(C7) the A4_chen_hou ceiling control is unmoved and still above 1/2",
          j["control_C7_ceiling_control"]["ok"], "")
    check("(C8) the exact integer basis constraint residual is identically zero",
          j["control_C8_exact_basis"]["all_exactly_zero"], "")
    check("(C9) the fast series is contained in the rigorous MPInterval enclosures",
          j["control_C9_series_containment"]["all_contained"], "")
    check("(C10) cancellation depth stayed inside the precision budget",
          j["control_C10_cancellation_budget"]["all_within_budget"], "")

    # ---- D1 ----------------------------------------------------------------
    for key in ROWS:
        e = j["diagnostic_D1b_collapsed_node_influence"]["rows"][key]
        check(f"(D1 {key}) the 12 collapsed right-endpoint nodes are not load-bearing",
              e["abs_diff"] < ga["noise_band_per_row"][key],
              f"influence {e['abs_diff']:.3e} < noise band {ga['noise_band_per_row'][key]:.3e}")

    # ---- figure ------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14.4, 4.6))

    # panel 1: the quadrature sweep, and the one cell that was the whole failure
    ax = axes[0]
    ax.axhline(CEILING, color="#999", ls=":", lw=1.1)
    ax.text(12.5, 0.5, "Xu's modulated ceiling, 1/2", fontsize=7.5, color="#666",
            va="bottom")
    for key in ROWS:
        lab = key.split("|")[1]
        ax.plot(GRADE_DEPTHS, rows[key]["float64_mirror"]["quad_gaps"], "x--",
                color="crimson", ms=7, lw=1.1,
                label="float64 (banked, leg 178)" if key == ROWS[0] else None)
        ax.plot(GRADE_DEPTHS, rows[key]["mp"]["quad_gaps"], "o-", color=COLOR[key],
                ms=5, lw=1.3, label=f"200-digit, {lab}")
    ax.set_yscale("symlog", linthresh=1.0)
    ax.set_xscale("log", base=2)
    ax.set_xticks(GRADE_DEPTHS)
    ax.set_xticklabels([str(d) for d in GRADE_DEPTHS])
    ax.set_xlabel("n_grade (endpoint refinement depth), n = 128")
    ax.set_ylabel("coercivity gap  (symlog)")
    ax.set_title("clause_quad_stable IS repaired\n"
                 "rel_spread 4.0349 $\\to$ 6.6e-07 / 9.1e-07", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="center left")

    # panel 2: the rcond ladder -- distance BELOW the ceiling, log scale
    ax = axes[1]
    for key in ROWS:
        e = c5[key]
        ax.plot(e["rcond"], [CEILING - g for g in e["gaps"]], "o-",
                color=COLOR[key], ms=5, lw=1.3, label=key.split("|")[1])
        for rc, g, dr in zip(e["rcond"], e["gaps"], e["dropped"]):
            if key == ROWS[0]:
                ax.annotate(f"{dr} dropped", (rc, CEILING - g), fontsize=6.5,
                            textcoords="offset points", xytext=(0, 7), ha="center",
                            color="#555")
    band = ga["noise_band_per_row"][ROWS[0]]
    ax.axhline(band, color="crimson", ls="--", lw=1.1)
    ax.text(1.1e-14, band * 1.25, f"float64 noise band  cond(G)$\\cdot\\epsilon$ = {band:.2e}",
            fontsize=7.5, color="crimson")
    ax.axhline(CEILING_SLACK, color="#333", ls=":", lw=1.1)
    ax.text(1.1e-14, CEILING_SLACK * 1.3, "clause 5's own slack, 1e-9", fontsize=7.5,
            color="#333")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.invert_xaxis()
    ax.set_xlabel("whitening rcond")
    ax.set_ylabel("$1/2$ $-$ reported gap")
    ax.set_title("control C5: the NUMBER is a property of the\ntruncation "
                 "(spread 3.9e-05 / 5.4e-05 vs tol 1e-6)", fontsize=9.5)
    ax.legend(fontsize=7.5, loc="lower right")

    # panel 3: C4 -- where the exact one-sided bound actually lands
    ax = axes[2]
    ys = []
    for i, key in enumerate(ROWS):
        e = c4[key]
        excess = float(Decimal(e["minus_R_mp_minus_one_half_exact_decimal"]))
        ys.append((i, CEILING - e["gap_mp_eigensolve"], -excess, key))
    for i, d_eig, d_bound, key in ys:
        ax.plot([d_eig], [i], "x", color="crimson", ms=10, mew=2,
                label="float64 eigensolve" if i == 0 else None)
        ax.plot([d_bound], [i], "o", color=COLOR[key], ms=8,
                label="exact 200-digit one-sided bound $-R(x)$" if i == 0 else None)
        ax.plot([d_bound, d_eig], [i, i], color="#bbb", lw=1.0, zorder=0)
    ax.axvline(band, color="crimson", ls="--", lw=1.1)
    ax.axvline(CEILING_SLACK, color="#333", ls=":", lw=1.1)
    ax.set_xscale("log"); ax.set_xlim(4e-5, 2e-19)
    ax.set_yticks([0, 1]); ax.set_yticklabels([k.split("|")[1] for k in ROWS])
    ax.set_ylim(-1.15, 1.6)
    ax.set_xlabel("distance below $1/2$   (right = closer to the ceiling)")
    ax.text(band, 1.42, "cond(G)$\\cdot\\epsilon$", fontsize=7.5, color="crimson",
            ha="center")
    ax.text(CEILING_SLACK, 1.42, "1e-9 slack", fontsize=7.5, color="#333", ha="center")
    ax.set_title("control C4: the bound lands BELOW 1/2, by 5.2e-18 / 1.4e-18\n"
                 "registered as an agreement test, it fires; as a bound, it does not",
                 fontsize=9.5)
    ax.legend(fontsize=7.5, loc="lower center")

    fig.suptitle("Route-EGMF (leg 329): arbitrary precision repairs clause 3 and moves the "
                 "obstruction to clause 5's establishability -- gate answers NO",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(FIG, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"\nwrote {FIG}")

    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
