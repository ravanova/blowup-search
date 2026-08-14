"""Route-T4 (leg 393) -- EVIDENCE.

Every number this leg's journal quotes, re-derived from `writeup/data/p2_route_t4_v1.json`
alone. No network. No .mat decoding. No PDF. This reads the curated JSON the runner
(`experiments/p2_route_t4_v1.py`) produced and checks the prose against it.

Lesson 68: a check that is not executable decays at the rate of memory. **Gate this by the
EXIT CODE, never by reading a printed line.** Exit 0 = every check passed. Exit 1 = at least
one FAILED, and the count is on stderr.

Also builds `writeup/figures/fig110_route_t4_v1.png` (figure number allocated to leg 393 at
dispatch).

    .venv/bin/python experiments/p2_route_t4_v1_evidence.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
FIG = os.path.join(ROOT, "writeup", "figures", "fig110_route_t4_v1.png")

# Pre-committed in the journal's Part I sec 4 (verdict rule V4), BEFORE any number existed.
V4_REPRODUCED = 1e-3
V4_RIGHT_SHAPE_WRONG_INTERVAL = 1e-1

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-72s %s" % ("ok" if ok else "FAIL", name, detail))


def main():
    with open(os.path.join(D, "p2_route_t4_v1.json")) as fh:
        w = json.load(fh)

    rows, ctl = w["rows"], w["controls"]

    # ---- 1. provenance -----------------------------------------------------
    check("target is arXiv:1902.00384", w["target_paper"]["arxiv_id"] == "1902.00384")
    check("external source REACHED, banked positively (arXiv)",
          ctl["C_net"]["evidence"]["arxiv_pdf"]["status"] in ("OK", "ALREADY_PRESENT"),
          ctl["C_net"]["evidence"]["arxiv_pdf"]["status"])
    check("external source REACHED, banked positively (VU code pkg = paper ref [41])",
          ctl["C_net"]["evidence"]["vu_code_zip"]["status"] in ("OK", "ALREADY_PRESENT"),
          ctl["C_net"]["evidence"]["vu_code_zip"]["status"])
    check("no source banked as a zero without HTTP evidence",
          all(e["status"] != "FAILED" for e in w["network_evidence"].values()))

    # ---- 2. the C1 showing for THIS leg's apparatus -------------------------
    ap = w["apparatus_this_leg_used"]
    check("this leg's apparatus constructs NO operator", ap["constructs_an_operator"] is False)
    check("this leg's apparatus constructs NO Y0/Z0/Z1/Z2", ap["constructs_Y0_Z0_Z1_Z2"] is False)
    check("this leg's apparatus constructs NO approximate inverse",
          ap["constructs_an_approximate_inverse"] is False)
    check("this leg's apparatus has NO M-indexed family (NGX exclusion is vacuous on it)",
          ap["has_an_M_indexed_family"] is False)

    # ---- 3. the controls, each two-sided ------------------------------------
    check("control C+ FIRED: the paper's apparatus IS the banned machinery",
          ctl["C_plus"]["fired"] is True)
    check("C+ : all six load-bearing verbatim quotes located in the paper's own text",
          all(ctl["C_plus"]["quotes_found"].values()),
          "%d/6" % sum(ctl["C_plus"]["quotes_found"].values()))
    check("C+ : 'approximate inverse' occurs in the paper",
          ctl["C_plus"]["term_counts"]["approximate inverse"] > 0,
          "n=%d" % ctl["C_plus"]["term_counts"]["approximate inverse"])
    check("C+ : 'Newton-Kantorovich' occurs in the paper",
          ctl["C_plus"]["term_counts"]["newton-kantorovich"] > 0,
          "n=%d" % ctl["C_plus"]["term_counts"]["newton-kantorovich"])
    check("control C- did NOT fire: no self-consistent / a-priori-bounds dynamical closure",
          ctl["C_minus"]["fired"] is False)
    check("C- : every dynamical-closure marker term has count zero",
          all(v == 0 for v in ctl["C_minus"]["term_counts"].values()),
          str(ctl["C_minus"]["term_counts"]))
    check("C- : Zgliczynski appears ONLY as a bibliography entry, never as the method",
          ctl["C_minus"]["zgliczynski_only_in_bibliography"] is True)
    check("control C_3D FIRED: Nx3 = 0 on BOTH certified rows", ctl["C_3D"]["fired"] is True)
    check("control C_dec+ FIRED: decoded extents match Table 1 for BOTH files",
          ctl["C_dec_plus"]["fired"] is True)
    check("control C_dec- FIRED: the two files decode to DIFFERENT shapes",
          ctl["C_dec_minus"]["fired"] is True)
    check("control C_net FIRED", ctl["C_net"]["fired"] is True)

    # ---- 4. verdict --------------------------------------------------------
    check("verdict rule V1 fired (C+ and not C-)", w["verdict_rule_fired"] == "V1_BRANCH_C_STOP",
          w["verdict_rule_fired"])
    check("gate answered STOP under pre-committed branch (c), NOT 'no' and NOT 'yes'",
          w["gate_answer"] == "STOP (pre-committed branch (c))", w["gate_answer"])
    check("the paper's apparatus is recorded as the banned machinery",
          w["paper_apparatus_as_measured"]["is_the_banned_machinery"] is True)
    check("the paper's apparatus is recorded as NOT a Galerkin-plus-tail dynamical closure",
          w["paper_apparatus_as_measured"]["is_a_galerkin_plus_tail_dynamical_closure"] is False)

    # ---- 5. the reproduced rows -------------------------------------------
    for lab, thm in (("p1", "Theorem 5.1"), ("p2", "Theorem 5.2 / Theorem 1.1")):
        r = rows[lab]
        c = r["paper_criterion_4_32"]
        check("%s: is %s" % (lab, thm), r["arxiv_theorem"] == thm, r["arxiv_theorem"])
        check("%s: paper's own criterion (4.32) first half  Z0+Z1 < 1" % lab,
              c["Z0_plus_Z1_lt_1"] is True, "%.6f" % c["Z0_plus_Z1"])
        check("%s: paper's own criterion (4.32) second half 2*Y0*Z2 < (1-(Z0+Z1))^2" % lab,
              c["second_inequality_holds"] is True,
              "%.4e < %.4e" % (c["two_Y0_Z2"], c["one_minus_Z0_Z1_squared"]))
        check("%s: criterion MET, so the row is certified by the paper's own test" % lab,
              c["criterion_met"] is True)
        check("%s: r_min reproduced from published Y0/Z0/Z1/Z2 to < 1e-8 relative" % lab,
              r["r_min"]["rel_dev"] < 1e-8, "rel dev %.3e" % r["r_min"]["rel_dev"])
        check("%s: r_max reproduced from published Y0/Z0/Z1/Z2 to < 1e-8 relative" % lab,
              r["r_max"]["rel_dev"] < 1e-8, "rel dev %.3e" % r["r_max"]["rel_dev"])
        check("%s: r_sol^Omega reproduced EXACTLY as printed in the paper" % lab,
              r["r_sol_Omega"]["rel_dev_vs_printed"] == 0.0,
              "%.5g == %.5g" % (r["r_sol_Omega"]["reproduced"],
                                r["r_sol_Omega"]["printed_in_paper"]))
        check("%s: reproduced r_min lies strictly inside [0, r_max)" % lab,
              0 < r["r_min"]["reproduced"] < r["r_max"]["reproduced"])
        check("%s: authors' own package flags the proof successful" % lab,
              r["authors_success_flags"]["success"] == 1
              and r["authors_success_flags"]["radiisuccess"] == 1)
        # decode controls, per row
        check("%s: package Nrec == Table 1 row" % lab,
              r["table1_agrees_with_package"]["Nrec"] is True, str(r["solshape_Nrec"]))
        check("%s: package N_dagger, N_tilde, eta, nu all == Table 1" % lab,
              all(r["table1_agrees_with_package"][k]
                  for k in ("Ndagger", "Ntilde", "eta", "nu")))
        check("%s: array extents == 2*Nrec+1 on every axis" % lab,
              r["array_shape_matches_Nrec"] is True,
              str(r["dimensionality"]["omega_shape"]))

    # ---- 6. F1 : the pressure enclosure row, against V4's PRE-COMMITTED bands
    r2 = rows["p2"]
    d_norm = r2["norm_u_X"]["rel_dev"]
    check("F1: ||u||_X computed from published data agrees with the value IMPLIED by the "
          "paper's own printed (r_sol^p, r_sol^omega) via Lemma 6.2",
          d_norm < V4_REPRODUCED,
          "delta = %.3e  <  V4 threshold %.0e  (computed %.9f vs implied %.9f)"
          % (d_norm, V4_REPRODUCED, r2["norm_u_X"]["computed_from_published_data"],
             r2["norm_u_X"]["implied_by_printed_radii"]))
    d_p = r2["r_sol_p"]["rel_dev_vs_printed"]
    check("F1: r_sol^p reproduced within V4's REPRODUCED band (<= 1e-3 relative)",
          d_p <= V4_REPRODUCED,
          "delta = %.3e ; repro %.5e vs printed %.5e" % (
              d_p, r2["r_sol_p"]["reproduced"], r2["r_sol_p"]["printed_in_paper"]))
    check("F1: and the sign of the residual gap is the right one -- the reproduction is a "
          "LOWER bound on the authors' radius (their raddevp term can only widen it)",
          r2["r_sol_p"]["reproduced"] <= r2["r_sol_p"]["printed_in_paper"])
    check("F1 is NOT in V4's right-shape-wrong-interval band",
          not (V4_REPRODUCED < d_p <= V4_RIGHT_SHAPE_WRONG_INTERVAL))

    # ---- 7. F2 : the dimensionality of the certified object -----------------
    for lab in ("p1", "p2"):
        dim = rows[lab]["dimensionality"]
        check("F2 %s: x3 mode extent is exactly 1 (the single mode n3 = 0)" % lab,
              dim["x3_mode_extent"] == 1, "extent=%d" % dim["x3_mode_extent"])
        check("F2 %s: max|u^(3)| is EXACTLY zero on the authors' own array" % lab,
              dim["max_abs_u3"] == 0.0, repr(dim["max_abs_u3"]))
        check("F2 %s: max|omega^(1)| and max|omega^(2)| are EXACTLY zero" % lab,
              dim["max_abs_omega1"] == 0.0 and dim["max_abs_omega2"] == 0.0)
        check("F2 %s: omega^(3) is NOT zero (the one live component of a 2D flow) -- "
              "so the zeros above are structure, not an empty array" % lab,
              dim["max_abs_omega3"] > 0.0, "%.4f" % dim["max_abs_omega3"])
        check("F2 %s: the authors' own output labels the setup '2D'" % lab,
              dim["setup_field_in_authors_output"] == "2D",
              dim["setup_field_in_authors_output"])

    # ---- 8. WHY the paper's approximate inverse is bounded (the W6 content) --
    for lab in ("p1", "p2"):
        s = rows[lab]["symbol_modulus"]
        check("W6 %s: inf over ALL nonzero modes of the symbol modulus mu(n) equals nu "
              "EXACTLY -- a floor independent of the truncation" % lab,
              s["inf_mu_equals_nu"] is True,
              "inf mu = %.6f = nu" % s["inf_mu_over_all_nonzero_modes"])
        check("W6 %s: the floor is strictly positive (contrast NGX: sigma_min -> 0)" % lab,
              s["inf_mu_over_all_nonzero_modes"] > 0)
        check("W6 %s: on the tail mu(n) > N_dagger, so the diagonal part of the authors' A "
              "has norm <= 1/N_dagger -- ONE bounded operator on all modes at once" % lab,
              s["min_mu_on_tail"] > s["N_dagger"]
              and s["sup_abs_lambda_on_tail"] <= s["one_over_N_dagger"] * (1 + 1e-9),
              "sup|lambda| = %.6e <= 1/N+ = %.6e"
              % (s["sup_abs_lambda_on_tail"], s["one_over_N_dagger"]))

    # ---- 9. the disclaimers this leg is bound to, made executable -----------
    check("Table 1's own cost for the larger row is recorded (the price of the apparatus)",
          rows["p2"]["table1_row"]["CPU_days"] == 95
          and rows["p2"]["table1_row"]["RAM_GB"] == 110,
          "%d CPU-days, %d GB RAM" % (rows["p2"]["table1_row"]["CPU_days"],
                                      rows["p2"]["table1_row"]["RAM_GB"]))

    build_figure(w)

    n_fail = sum(1 for _, ok_, _ in CHECKS if not ok_)
    print("\n%d/%d checks OK" % (len(CHECKS) - n_fail, len(CHECKS)))
    if n_fail:
        raise SystemExit("%d check(s) FAILED" % n_fail)


def build_figure(w):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    # Fixed categorical order, never cycled. Blue/orange is the strongest CVD-safe pair;
    # status colours (green/red) are reserved for pass/fail and never reused as a series.
    PUBLISHED, REPRODUCED = "#1f4e79", "#c1440e"
    GOOD, BAD, INK = "#2e7d32", "#b3261e", "#3c3c3c"

    rows = w["rows"]
    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.1))

    # ---- Panel A: agreement, one axis, log scale, threshold drawn ----------
    ax = axes[0]
    labels, devs = [], []
    for lab in ("p1", "p2"):
        r = rows[lab]
        labels += ["%s r_min" % lab, "%s r_max" % lab, "%s r_sol$^\\Omega$" % lab]
        devs += [r["r_min"]["rel_dev"], r["r_max"]["rel_dev"],
                 r["r_sol_Omega"]["rel_dev_vs_printed"]]
    labels += ["p2 $\\|u\\|_X$", "p2 r_sol$^p$"]
    devs += [rows["p2"]["norm_u_X"]["rel_dev"], rows["p2"]["r_sol_p"]["rel_dev_vs_printed"]]
    FLOOR = 1e-16                      # an exact match is drawn at the float64 floor
    plotted = [max(d, FLOOR) for d in devs]
    y = np.arange(len(labels))
    ax.barh(y, plotted, color=REPRODUCED, height=0.55, zorder=3)
    # One series only, so no legend box: the reference line is labelled directly.
    ax.axvline(V4_REPRODUCED, color=INK, ls="--", lw=1.4, zorder=4)
    ax.text(V4_REPRODUCED * 0.6, -0.32, "V4 pre-committed threshold $10^{-3}$",
            ha="right", va="center", fontsize=7.8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(FLOOR / 3, 1e-1)
    ax.set_xlabel("relative deviation, reproduced vs published (log)")
    for i, d in enumerate(devs):
        ax.text(max(d, FLOOR) * 1.7, i, "exact" if d == 0.0 else "%.1e" % d,
                va="center", fontsize=8, color=INK)
    ax.grid(axis="x", alpha=0.25, zorder=0)
    ax.set_title("A. Both published rows reproduce\nfrom the authors' own constants",
                 fontsize=10.5)

    # ---- Panel B: the mode support of the certified object -----------------
    ax = axes[1]
    axnames = ["$N_{x_1}$", "$N_{x_2}$", "$N_{x_3}$", "$N_t$"]
    xx = np.arange(4)
    for k, (lab, colour, off) in enumerate((("p1", PUBLISHED, -0.19),
                                            ("p2", REPRODUCED, 0.19))):
        vals = rows[lab]["solshape_Nrec"]
        ax.bar(xx + off, vals, width=0.34, color=colour, zorder=3,
               label="%s  ($\\nu$ = %g)" % (lab, rows[lab]["nu"]))
        for i, v in enumerate(vals):
            ax.text(i + off, v + 0.35, str(v), ha="center", fontsize=9, color=INK)
    ax.axvspan(1.5, 2.5, color=BAD, alpha=0.10, zorder=0)
    ax.text(2.0, 19.3, "$N_{x_3}=0$\non BOTH rows\n$\\max|u^{(3)}|=0$ exactly",
            ha="center", va="top", fontsize=8.5, color=BAD, fontweight="bold")
    ax.set_xticks(xx)
    ax.set_xticklabels(axnames)
    ax.set_ylim(0, 24)
    ax.set_ylabel("Fourier modes retained per axis")
    ax.grid(axis="y", alpha=0.25, zorder=0)
    ax.legend(fontsize=8.5, loc="upper left")
    ax.set_title("B. The certified objects are 2D lifts:\nno $x_3$ dependence at all",
                 fontsize=10.5)

    # ---- Panel C: the gate, stated as a picture ----------------------------
    ax = axes[2]
    ax.axis("off")
    r2 = rows["p2"]
    txt = (
        "GATE (pre-committed, unedited):\n"
        "Reproduce a published enclosure row of\n"
        "arXiv:1902.00384 -- quantity, interval, and\n"
        "the paper's OWN certification criterion --\n"
        "using an apparatus shown C1-compliant?\n\n"
        "ANSWER: STOP (pre-committed branch (c)).\n"
        "NOT 'no'. NOT 'yes'.\n\n"
        "WHY. The paper's apparatus, measured at\n"
        "full text, IS the banned machinery:\n"
        "  Newton-Kantorovich radii-polynomial\n"
        "  contraction, weighted-l1 Fourier space,\n"
        "  ONE bounded approximate inverse A\n"
        "  (sec 2.3) on the whole space at once.\n"
        "C1's scope does NOT reach this paper.\n\n"
        "FURTHEST POINT REACHED (audit only):\n"
        "  criterion (4.32) verified, both rows\n"
        "  r_min  %.6e (rel dev %.1e)\n"
        "  r_max  %.6e (rel dev %.1e)\n"
        "  r_sol^Omega  %.4e  EXACT\n"
        "  r_sol^p  %.4e vs %.4e\n\n"
        "COST of the apparatus, authors' Table 1:\n"
        "  %d CPU-days, %d GB RAM -- for a 2D row."
        % (r2["r_min"]["reproduced"], r2["r_min"]["rel_dev"],
           r2["r_max"]["reproduced"], r2["r_max"]["rel_dev"],
           r2["r_sol_Omega"]["reproduced"],
           r2["r_sol_p"]["reproduced"], r2["r_sol_p"]["printed_in_paper"],
           r2["table1_row"]["CPU_days"], r2["table1_row"]["RAM_GB"]))
    ax.text(0.0, 1.0, txt, va="top", ha="left", fontsize=8.4, family="monospace",
            color=INK)
    ax.set_title("C. The gate", fontsize=10.5)

    fig.suptitle("Route-T4 (leg 393): arXiv:1902.00384 audited row for row -- the rows "
                 "reproduce, and the apparatus is the banned one",
                 fontweight="bold", y=1.02)
    fig.tight_layout()
    os.makedirs(os.path.dirname(FIG), exist_ok=True)
    fig.savefig(FIG, bbox_inches="tight", dpi=140)
    print("wrote %s" % FIG)


if __name__ == "__main__":
    main()
