"""Route-WES v1 (leg 178) — EVIDENCE: every number the BLOG and TECHNICAL write-ups quote,
re-derived from `writeup/data/p2_route_wes_v1_space.json`. Also builds
`writeup/figures/fig66_route_wes_v1_space.png`.

Nothing expensive is recomputed: this reads curated data and asserts the relations the prose
asserts, so a reader can check the prose without re-running the gate.

The one place prose and JSON differ ON PURPOSE is the gate answer. The JSON's
`gate_answer.answer` is `"NO"` — the five-clause predicate as the runner computed it, UNSCOPED.
The user's ruling of 2026-08-07 scopes clause 3 to grading depths whose contamination diagnostic
is below 1, and under that scoping the gate answers YES. This script asserts BOTH: that the
banked field still reads NO, and that the scoped spread passes clause 3's own tolerance. If
either ever stops holding, the prose is wrong.

    .venv/bin/python experiments/p2_route_wes_v1_space_evidence.py
"""

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig66_route_wes_v1_space.png")

ROW = "T2_egm|E_egm"          # the gate-answering row
CONTAM_CUT = 1.0              # the ruling's scope: read a depth only if contamination < 1

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-64s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_wes_v1_space.json")) as fh:
        w = json.load(fh)

    pc = w["pre_committed"]
    V = w["verdicts"][ROW]
    QS = w["quadrature_stability"][ROW]

    # ---- (1) the pre-registration is intact -------------------------------
    check("(1) novelty log pre-dates the compute",
          pc["novelty_log"].startswith("writeup/novelty/leg_178.md"),
          pc["novelty_log"])
    check("(1b) the pre-committed ladders are unchanged",
          pc["n_ladder"] == [32, 64, 128, 256]
          and pc["grade_depths"] == [12, 24, 48, 96]
          and len(pc["weights"]) == 11 and len(pc["constraint_classes"]) == 4,
          "n %s, depths %s, %d weights, %d classes"
          % (pc["n_ladder"], pc["grade_depths"], len(pc["weights"]),
             len(pc["constraint_classes"])))
    check("(1c) the five clause tolerances are the ones the prose quotes",
          pc["rel_stability_tol"] == 0.05 and pc["quad_spread_tol"] == 1e-3
          and pc["admiss_tol"] == 1e-6 and pc["known_answer_ceiling"] == 0.5,
          "rel 5e-2, quad 1e-3, admiss 1e-6, ceiling 0.5")

    # ---- (2) C1: leg 111's banked numbers reproduce -----------------------
    c1 = w["control_C1_reproduction"]
    worst = max(r["abs_diff"] for r in c1["rows"])
    check("(2) C1 reproduction: leg 111's four banked gaps",
          c1["all_ok"] is True and worst <= c1["tol"],
          "worst abs_diff %.4e vs tol %.0e" % (worst, c1["tol"]))

    # ---- (3) P0: EGM's weight IS leg 111's family B at gamma = 4 ----------
    p0 = w["P0_egm_weight_is_family_B4"]
    check("(3) P0 weight identity, ratio is the constant 32",
          p0["holds"] is True and p0["rel_spread"] < 1e-12
          and abs(p0["ratio_mean"] - 32.0) < 1e-9,
          "spread %.4e, |ratio-32| %.4e over %d points"
          % (p0["rel_spread"], p0["abs_diff_from_32"], p0["n_points"]))

    # ---- (4) the vanishing order is MEASURED, and it moved ----------------
    vo = w["vanishing_order"]
    for cls, want in [("T0_unconstrained", 1.0), ("T1_dprime", 3.0),
                      ("T2_egm", 3.0), ("T3_hilbert_only", 1.0)]:
        m = vo[cls]["measured_order"]
        check("(4) measured vanishing order %-16s = %.7f" % (cls, m),
              abs(m - want) < 1e-5 and vo[cls]["declared_order"] == want,
              "declared %.1f" % want)
    check("(4z) T2_egm satisfies BOTH EGM hypotheses exactly",
          vo["T2_egm"]["h_prime_at_0"] == 0.0 and vo["T2_egm"]["H_h_at_0"] == 0.0,
          "h'(0) = 0.0 and Hh(0) = 0.0")

    # ---- (5) the instrument finding: assemble-then-project is invalid -----
    inst = w["instrument_exact_vs_projected"]["rows"]["T2_egm"]
    check("(5) exact basis has EXACTLY zero constraint residual",
          inst["exact_basis_constraint_residual"] == 0.0
          and inst["svd_basis_constraint_residual"] > 1e-15,
          "exact 0.0 vs svd %.4e" % inst["svd_basis_constraint_residual"])
    frac = inst["abs_diff"] / abs(inst["gap_exact_basis"])
    check("(5b) assemble-then-project understates the gap by ~21%",
          abs(inst["abs_diff"] - 0.10325847044710074) < 1e-12 and 0.20 < frac < 0.21,
          "abs_diff %.4e on a value of %.6f -> %.1f%%"
          % (inst["abs_diff"], inst["gap_exact_basis"], 100 * frac))

    # ---- (6) the gate-answering row, clause by clause ---------------------
    check("(6a) clause 1 positive: gap at n=256",
          V["clause_positive"] is True and V["gap_n256"] > 0,
          "%.12f" % V["gap_n256"])
    steps = V["rel_steps_last_two"]
    check("(6b) clause 2 grid-stable across the last two refinements",
          V["clause_grid_stable"] is True and max(steps) <= pc["rel_stability_tol"],
          "%.4e and %.4e vs tol %.0e" % (steps[0], steps[1], pc["rel_stability_tol"]))
    check("(6d) clause 4 admissible on the CONSTRAINED space",
          V["clause_admissible"] is True
          and abs(V["admiss_ratio"] - 1.0) <= pc["admiss_tol"]
          and V["exponent_margin"] > 0,
          "ratio %.6f, exponent margin %+.1f" % (V["admiss_ratio"], V["exponent_margin"]))
    check("(6e) clause 5 under Xu's published ceiling",
          V["clause_under_ceiling"] is True
          and V["gap_n256"] <= pc["known_answer_ceiling"] + 1e-9,
          "%.9f <= 0.5 + 1e-9" % V["gap_n256"])
    check("(6f) the nonlocal Hilbert half is at roundoff; the gap is the LOCAL half",
          abs(V["nonlocal_gap_n256"]) < 1e-12
          and abs(V["local_gap_n256"] - V["gap_n256"]) < 1e-12,
          "local %+.9f, nonlocal %+.4e, by-parts residual %.4e"
          % (V["local_gap_n256"], V["nonlocal_gap_n256"], V["byparts_rel_residual_n256"]))

    # ---- (7) clause 3, and the user's ruling of 2026-08-07 ----------------
    depths = np.array(QS["depths"], dtype=float)
    gaps = np.array(QS["gaps"], dtype=float)
    contam = np.array(QS["contamination"], dtype=float)

    check("(7a) clause 3 FAILS as the runner computed it, unscoped",
          V["clause_quad_stable"] is False
          and abs(QS["rel_spread"] - 4.034902353014096) < 1e-12,
          "spread over all four depths %.6f vs tol %.0e"
          % (QS["rel_spread"], pc["quad_spread_tol"]))
    check("(7b) the banked gate_answer field still reads NO (unscoped predicate)",
          w["gate_answer"]["answer"] == "NO" and w["gate_answer"]["n_qualifying"] == 0,
          "deliberate: the ruling scopes how clause 3 is READ, not what was measured")

    read = contam < CONTAM_CUT
    check("(7c) the ruling's scope cuts exactly one depth, n_grade = 96",
          read.tolist() == [True, True, True, False],
          "contamination %s" % " ".join("%.3e" % c for c in contam))
    check("(7d) the cut is not marginal: the depths straddle 1 by many orders",
          contam[read].max() < 1e-9 and contam[~read].min() > 1e2,
          "largest read %.3e, smallest skipped %.4e" % (contam[read].max(), contam[~read].min()))

    g = gaps[read]
    scoped = (g.max() - g.min()) / abs(g.mean())
    check("(7e) scoped spread over the three read depths = 2.2839e-07",
          abs(scoped - 2.2839e-07) < 1e-11,
          "%.4e" % scoped)
    check("(7f) clause 3 PASSES as ruled, by a factor of ~4.4e+03",
          scoped <= pc["quad_spread_tol"],
          "%.4e vs tol %.0e -> margin %.3e x"
          % (scoped, pc["quad_spread_tol"], pc["quad_spread_tol"] / scoped))
    check("(7g) so all five clauses hold under the ruling -> GATE ANSWERS YES",
          all([V["clause_positive"], V["clause_grid_stable"], V["clause_admissible"],
               V["clause_under_ceiling"], scoped <= pc["quad_spread_tol"]]),
          "user's ruling 2026-08-07; NOT this leg's own call")

    # ---- (8) the controls that let the answer be NO -----------------------
    c2 = w["control_C2_falsification"]
    check("(8a) C2 falsification control fires: T3 passes 0 rows at gamma > 3",
          c2["fires_as_designed"] is True and len(c2["rows_passing_above_gamma_3"]) == 0,
          "the instrument measures the SPACE, not dimension reduction")
    for cls, r in w["control_C3_dissipation"]["rows"].items():
        check("(8b) C3 dissipation sign flips on the APPENDED path: %s" % cls,
              r["sign_flips"] is True and r["monotone"] is True,
              "mu 0->2: %+.5f -> %+.5f" % (r["gaps"][0], r["gaps"][-1]))
    p5 = w["P5_point_mode_intersection"]["rows"]
    check("(8c) P5: T2's two constraints annihilate span{sin th, sin 2th} exactly",
          p5["T2_egm"]["intersection_dim"] == 0
          and p5["T1_dprime"]["intersection_dim"] == 1,
          "T2 dim 0 (so modulate on/off agree); T1 dim 1 forces its gap <= -1")

    # ---- (9) the bound: nothing here is a certificate ---------------------
    check("(9) the leg's own not-claimable line is banked with the data",
          "NOT this repository" in w["not_claimable"],
          "EGM arXiv:1906.05811 Prop 2.1 owns the construction, the weight and the -1/2")
    check("(9b) the object is the a = 0 CLM linearisation (clause S7), float64 only",
          "a = 0 CLM linearisation" in w["ceiling"] and "float64" in w["ceiling"],
          "a gap here bounds HL_S2_nonsymmetric's difficulty FROM BELOW, never above")

    make_figure(w, V, QS, depths, gaps, contam, read, scoped)

    nfail = sum(1 for _, ok, _ in CHECKS if not ok)
    print("\n%d checks, %d failed" % (len(CHECKS), nfail))
    return 1 if nfail else 0


def make_figure(w, V, QS, depths, gaps, contam, read, scoped):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    pc = w["pre_committed"]
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.5))

    # --- panel 1: the window opened because the vanishing order moved ------
    ax = axes[0]
    vo = w["vanishing_order"]
    order = ["T0_unconstrained", "T1_dprime", "T2_egm", "T3_hilbert_only"]
    ps = [vo[c]["measured_order"] for c in order]
    lo, hi = 3.0, [2 * p + 1 for p in ps]
    for i, (c, p, h) in enumerate(zip(order, ps, hi)):
        width = max(h - lo, 0.0)
        ax.barh(i, width, left=lo, height=0.55,
                color="#2a7f62" if width > 0 else "#b03a2e",
                edgecolor="black", linewidth=0.7)
        ax.text(lo + 0.12, i, "p = %.5f   window (%.0f, %.0f) width %.1f"
                % (p, lo, h, width), va="center", fontsize=8.2,
                color="white" if width > 0 else "#b03a2e")
    ax.axvline(3.0, color="#333", lw=1.1, ls="--")
    ax.annotate("damping\nneeds $\\gamma > 3$", xy=(3.0, -0.62), xytext=(3.12, -0.62),
                fontsize=7.6, color="#333", va="center")
    ax.set_yticks(range(4)); ax.set_yticklabels(order, fontsize=8.5)
    ax.set_ylim(-1.0, 3.6)
    ax.set_xlabel("weight exponent $\\gamma$"); ax.set_xlim(2.6, 7.6)
    ax.set_title("The window is a property of the TRIAL SPACE:\n"
                 "membership needs $\\gamma < 2p+1$, and $p$ is MEASURED", fontsize=9.5)
    ax.grid(alpha=0.22, axis="x")

    # --- panel 2: the gap ladder, leg 111's best vs this leg's ------------
    ax = axes[1]
    n = pc["n_ladder"]
    for key, lab, col, mk in [
            ("T2_egm|E_egm", "$T_2^{EGM}$ | EGM's own weight ($\\gamma=4$)", "#2a7f62", "o"),
            ("T2_egm|A4_chen_hou", "$T_2^{EGM}$ | Chen-Hou $\\gamma=4$ (from ABOVE)",
             "#8e44ad", "s"),
            ("T2_egm|A3", "$T_2^{EGM}$ | $\\gamma=3$ (collapsing to 0)", "#e67e22", "d"),
            ("T2_egm|A2", "$T_2^{EGM}$ | $\\gamma=2$ (below damping)", "#b03a2e", "^"),
            ("T0_unconstrained|A2", "leg 111's own $T_0$, $p=1$ | $\\gamma=2$ "
             "(its best admissible)", "#c0392b", "v")]:
        ladder = [r["gap"] for r in w["gap_ladder"][key]]
        assert [r["n"] for r in w["gap_ladder"][key]] == n
        assert all(r["mu"] == 0.0 for r in w["gap_ladder"][key]), "C4: mu = 0 rows only"
        # leg 111's own class is dashed: at gamma = 2 it lies within 3e-4 of the
        # constrained class, and a solid line would hide one under the other.
        ls = "--" if key.startswith("T0_") else "-"
        ax.plot(n, ladder, marker=mk, color=col, lw=1.6, ms=5, ls=ls, label=lab)
    ax.axhline(pc["known_answer_ceiling"], color="#333", lw=1.0, ls=":")
    ax.text(33, 0.545, "Xu's published ceiling $1/2$", fontsize=7.8, color="#333")
    ax.axhline(0.0, color="#333", lw=0.8)
    ax.set_xscale("log", base=2); ax.set_xticks(n)
    ax.set_xticklabels([str(v) for v in n])
    ax.set_xlabel("basis size $n$"); ax.set_ylabel("coercivity gap")
    ax.set_ylim(-1.42, 0.80)
    ax.set_title("Gap at $n=256$: %+.9f\nlast two relative steps %.3e, %.3e"
                 % (V["gap_n256"], V["rel_steps_last_two"][0],
                    V["rel_steps_last_two"][1]), fontsize=9.5)
    ax.legend(fontsize=6.6, loc="lower center", ncol=1, framealpha=0.95)
    ax.grid(alpha=0.22)

    # --- panel 3: clause 3, and the ruling's scope ------------------------
    ax = axes[2]
    ax.semilogy(depths, contam, marker="o", color="#b03a2e", lw=1.5, ms=6,
                label="contamination diagnostic")
    ax.axhline(CONTAM_CUT, color="#333", lw=1.2, ls="--")
    ax.axhspan(CONTAM_CUT, 1e7, color="#b03a2e", alpha=0.07)
    ax.text(13, 3e6, "contamination $\\geq 1$: the leg's own diagnostic\n"
                     "declares the number meaningless — NOT READ",
            fontsize=7.4, color="#b03a2e", va="top")
    for d, c, g, r in zip(depths, contam, gaps, read):
        ax.annotate("gap %+.7f" % g if r else "gap %+.4f" % g,
                    (d, c), textcoords="offset points",
                    xytext=(-11 if not r else 0, -18),
                    ha="right" if not r else "center", fontsize=7.4,
                    color="#2a7f62" if r else "#b03a2e",
                    fontweight="normal" if r else "bold")
    ax.scatter(depths[~read], contam[~read], s=200, facecolors="none",
               edgecolors="#b03a2e", linewidths=1.8, zorder=5,
               label="skipped: roundoff floor exceeds signal 3066x")
    ax.set_ylim(1e-24, 1e8)
    ax.set_xlim(6, 116)
    ax.set_xticks(depths); ax.set_xticklabels([str(int(d)) for d in depths])
    ax.set_xlabel("quadrature grading depth $n_{grade}$")
    ax.set_ylabel("contamination (roundoff / signal)")
    ax.set_title("Clause 3 SCOPED, not overruled (user's ruling 2026-08-07):\n"
                 "spread %.4e over the 3 read depths vs %.0e tol (%.0fx margin);\n"
                 "%.4f over all four" % (scoped, pc["quad_spread_tol"],
                                         pc["quad_spread_tol"] / scoped,
                                         QS["rel_spread"]), fontsize=9.0)
    ax.legend(fontsize=7.0, loc="lower right"); ax.grid(alpha=0.22)

    fig.suptitle("Route-WES (leg 178): leg 111's ZERO-WIDTH window is a property of its "
                 "$p=1$ TRIAL SPACE, not of the operator — constrain the space to $p=3$ and "
                 "the gap is $%+.9f$ (EGM's published $-1/2$, reproduced; NOT a certificate)"
                 % V["gap_n256"], fontweight="bold", y=1.04)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight", dpi=130)
    plt.close(fig)
    print("wrote %s" % FIG)


if __name__ == "__main__":
    sys.exit(main())
