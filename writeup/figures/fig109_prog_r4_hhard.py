"""fig109 -- PROG-R4 unit E: the H-hard diagnostic.

The programme could not tell H-supply (G1 missed because seed supply was thin)
from H-hard (G1 missed because these orbits are hard for THIS realization no
matter how good the seed is). U5 refuted H-supply by repairing the supply and
finding the miss survived. Unit E is the instrument that asks the other half,
in three parts, each with a planted control that has to fire in BOTH
directions before the panel is allowed to mean anything:

  (1) where the converged |s| sits against the |s| the attempt was seeded at,
      over the 200 banked U3+U5 attempts;
  (2) whether the low-|s| solutions are attractors of the hookstep ITERATION
      (unconstrained full Newton steps) or of the trust-region MINIMISATION
      (steps taken on the trust-region boundary);
  (3) whether the eight named Lucas & Kerswell Table IV rows are reachable at
      all when the attempt is planted at their published (T, s).

THE GATE THIS FIGURE REPORTS IS ABOUT THE DIAGNOSTICS RETURNING, NOT ABOUT
CONVERGENCE. A clean non-convergence with working controls is a PASS. The
figure is therefore written to be correct in ALL FOUR pre-committed branches:

  E-i   a published row is recovered -- panel D shows a point inside the
        0.05 x 0.05 matching box, and panel C shows it at tol.
  E-ii  no published row is recovered -- panels C and D show how far each of
        the 16 attempts got and how far from its row it stopped, which is a
        measurement of THIS REALIZATION AT THIS BUDGET, not a verdict about
        the rows.
  E-iii convergence to something else -- panel D shows points at tol far
        outside the box, and panel A shows the |s| pull they landed under.
  E-iv  the instrument limit -- panel C's x axis carries the seed residual a
        field-plus-pinned-(T,s) seed actually starts at, which is the honest
        statement of what a published row does and does not determine.

Every panel plots a magnitude, never a boolean. Panel C carries leg 353's
final-residual band because this unit's prior is that five of these rows were
already attempted and all five failed, and a figure that hid the prior would
be arguing rather than reporting.

THIS FIGURE MAKES NO GATE CLAIM ABOUT G1. G1 stays UNDER-RESOURCED as banked
in p2_prog_r4_g1_v1.json, and it stays UNDER-RESOURCED even in branch E-i: a
hand-placed seed at published coordinates is not a mined seed. Nothing here is
a proof, no L1 -> L4 link moves, Clay stays ~0.05%.

Checks assert the banked JSON supports every claim the panels make: that all
three diagnostics returned, that both controls of each fired in both
directions, that the counts reconcile with the attempt rows one at a time,
that no field was reused across the 16 direct-seed attempts, and that this
unit did not rewrite the G1 record. The script exits non-zero if any fails.

Data: writeup/data/p2_prog_r4_e_v1.json (and p2_prog_r4_g1_v1.json, read only
      as the record this unit must not have touched)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_e_v1.json")
U3 = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
U5 = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_m3_v1.json")
FIG = os.path.join(HERE, "fig109_prog_r4_hhard.png")

TOL = 1e-8
TWO_PI = 2.0 * np.pi
BAND = (0.295, 0.707)          # the |s| band the eight named rows live in
LOW = 0.15                     # the low-|s| shelf U5 sec.9 found
MATCH_TOL = 0.05
LEG353 = (22.5, 29.5)          # the prior: five rows, all five failed
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail
                                                    else ""))
    return bool(ok)


def wrap_abs(s):
    return np.abs((np.asarray(s, float) + np.pi) % TWO_PI - np.pi)


def main():
    with open(DATA) as f:
        d = json.load(f)
    with open(U3) as f:
        u3 = json.load(f)
    with open(U5) as f:
        u5 = json.load(f)

    d1, d2, d3 = d["diagnostic_1"], d["diagnostic_2"], d["diagnostic_3"]
    att = d3["attempts"]

    # The 200 banked attempts of diagnostic (1), re-derived HERE from U3's and
    # U5's own records rather than typed in, exactly as the diagnostic derived
    # them. The panel then has to agree with the banked verdict, which is the
    # next check.
    banked = [a for src in (u3, u5) for a in src["attempts"]]
    seed_abs = wrap_abs([a["s_seed"] for a in banked])
    fin_abs = wrap_abs([a["s_converged"] for a in banked])
    conv = np.array([bool(a["success"]) for a in banked])

    # ---- checks --------------------------------------------------------
    check("all three diagnostics RETURNED a verdict",
          all(k in d for k in ("diagnostic_1", "diagnostic_2",
                               "diagnostic_3"))
          and d1["verdict"] in ("PULL_TO_LOW_S", "NO_PULL")
          and d2["verdict"] in ("MINIMISATION_ATTRACTOR",
                                "ITERATION_ATTRACTOR", "MIXED"),
          f"(1) {d1['verdict']}, (2) {d2['verdict']}, "
          f"(3) {d3['n_attempts']} attempts returned")
    check("diagnostic (1) controls fired BOTH ways",
          d1["controls"]["fired_both_ways"]
          and d1["controls"]["positive"]["verdict"] == "PULL_TO_LOW_S"
          and d1["controls"]["negative"]["verdict"] == "NO_PULL",
          f"planted+ -> {d1['controls']['positive']['verdict']}, "
          f"planted- -> {d1['controls']['negative']['verdict']}")
    check("diagnostic (2) controls fired BOTH ways",
          d2["controls"]["fired_both_ways"]
          and (d2["controls"]["planted_minimisation"]["verdict"]
               == "MINIMISATION_ATTRACTOR")
          and (d2["controls"]["planted_iteration"]["verdict"]
               == "ITERATION_ATTRACTOR"),
          f"planted min -> "
          f"{d2['controls']['planted_minimisation']['verdict']}, "
          f"planted iter -> "
          f"{d2['controls']['planted_iteration']['verdict']}")
    check("diagnostic (3) controls P/N/R fired as planted",
          d3["controls"]["fired_as_planted"],
          "; ".join(d3["controls"]["failures"]) or "no failures")
    check("diagnostic (3) control R shows the harness CAN say YES",
          d3["controls"]["R"]["harness_predicate_says_recovered"],
          "a perturbed banked orbit is matched back by this unit's own "
          "predicate")
    check("panel A's 200 attempts re-derive the banked diagnostic (1) counts",
          len(banked) == d1["n_attempts_total"]
          and int(conv.sum()) == d1["n"]
          and abs(float(np.median((fin_abs - seed_abs)[conv]))
                  - d1["median_drift"]) < 1e-12,
          f"{len(banked)} attempts, {int(conv.sum())} convergences, "
          f"median drift {float(np.median((fin_abs - seed_abs)[conv])):+.6f}")
    check("diagnostic (1) sign counts reconcile with n",
          d1["n_drift_negative"] + d1["n_drift_positive"] == d1["n"],
          f"{d1['n_drift_negative']}- + {d1['n_drift_positive']}+ "
          f"= {d1['n']}")
    check("diagnostic (2) epoch classes partition the epochs",
          d2["n_constrained"] + d2["n_unconstrained"] == d2["n_epochs"],
          f"{d2['n_constrained']} constrained + {d2['n_unconstrained']} "
          f"unconstrained = {d2['n_epochs']}")
    check("diagnostic (3) converged count reconciles row by row",
          sum(1 for a in att if a["success"]) == d3["n_converged"],
          f"{d3['n_converged']} of {d3['n_attempts']} reached tol")
    check("diagnostic (3) recovery counts reconcile row by row",
          sum(1 for a in att if a["recovered_named_orbit"])
          == d3["n_recovered_its_own_row"]
          and sum(1 for a in att if a["recovered_any_named_orbit"])
          == d3["n_recovered_any_named_row"],
          f"{d3['n_recovered_its_own_row']} own row, "
          f"{d3['n_recovered_any_named_row']} any named row")
    check("all eight named rows attempted, both arms, 16 attempts",
          len({a["row"] for a in att}) == 8 and len(att) == 16
          and sorted(a["arm"] for a in att) == ["Q"] * 8 + ["S"] * 8,
          "8 rows x arms {S, Q}")
    check("NO FIELD REUSED across the 16 direct-seed attempts",
          len({a["snapshot_earlier"] for a in att}) == len(att),
          f"{len({a['snapshot_earlier'] for a in att})} distinct snapshots")
    check("every attempt was seeded at the PUBLISHED period exactly",
          all(abs(a["T_seeded"] - a["T_published"]) == 0.0 for a in att),
          "T pinned, not the candidate's quantised period")
    check("every attempt was seeded at +/- the published |s| exactly",
          all(abs(abs(a["s_seeded"]) - a["abs_s_published"]) < 1e-12
              for a in att),
          f"sign MEASURED, tally {d3['sign_tally']}")
    check("the stall rule kills ZERO banked convergence in either unit",
          all(v["n_would_be_killed"] == 0
              for v in d3["resourcing"]["stall_rule_replay"].values()),
          "; ".join(f"{k}: worst 10-epoch ratio "
                    f"{v['worst_10_epoch_ratio_at_k_ge_20']:.3f} vs "
                    f"threshold {v['threshold']}"
                    for k, v in
                    d3["resourcing"]["stall_rule_replay"].items()))
    check("this unit did not rewrite the G1 record",
          u3["gate"]["answer"] == "UNDER-RESOURCED",
          f"G1 still {u3['gate']['answer']}")
    check("no Clay link moved, ceiling TIER 2",
          d["clay_movement"]["links_moved"] == 0
          and d["clay_movement"]["ceiling"] == "TIER 2",
          d["clay_movement"]["clay_odds"])

    # ---- panels --------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(13.5, 10.0))

    # A. diagnostic (1): converged |s| against seed |s|, the 23 convergences
    ax = axes[0][0]
    ax.axhspan(BAND[0], BAND[1], color="#c0392b", alpha=0.08, zorder=0)
    ax.axvspan(BAND[0], BAND[1], color="#c0392b", alpha=0.08, zorder=0)
    lim = (0.0, max(d1["seed_abs_range"][1], d1["conv_abs_range"][1]) * 1.08)
    ax.plot(lim, lim, "-", color="#7f8c8d", lw=1.0,
            label=r"$|s|_{\rm conv} = |s|_{\rm seed}$ (no drift)")
    ax.axhline(LOW, color="#2c3e50", ls=":", lw=1.2,
               label=rf"low-$|s|$ shelf, $|s| = {LOW}$")
    sec = d1["secondary_all_200_attempts"]
    ax.scatter(seed_abs[~conv], fin_abs[~conv], c="#bdc3c7", marker=".",
               s=22, zorder=2,
               label=f"{int((~conv).sum())} attempts that did NOT reach tol "
                     "(secondary)")
    for i in np.flatnonzero(conv):
        ax.plot([seed_abs[i], seed_abs[i]], [seed_abs[i], fin_abs[i]],
                "-", color="#8e44ad", lw=0.8, alpha=0.55, zorder=3)
    ax.scatter(seed_abs[conv], fin_abs[conv], c="#8e44ad", marker="o", s=34,
               edgecolors="k", linewidths=0.5, zorder=4,
               label=f"{int(conv.sum())} convergences (primary), "
                     "line = the drift")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel(r"seed shift $|s|$")
    ax.set_ylabel(r"converged shift $|s|$")
    ax.set_title(
        f"A. diagnostic (1) on {d1['n_attempts_total']} banked attempts: "
        f"{d1['verdict']}\n"
        f"{d1['n_drift_negative']} of {d1['n']} convergences drifted DOWN in "
        f"$|s|$, sign test p = {d1['sign_test_p']:.4f}; "
        f"{100 * d1['frac_converged_below_0p15']:.1f}% finish below "
        f"{LOW}\n(all-200 secondary: {sec['verdict']}, "
        f"{100 * sec['frac_converged_below_0p15']:.1f}% below {LOW})",
        fontsize=9)
    ax.legend(fontsize=7, loc="upper left")
    ax.grid(alpha=0.3)

    # B. diagnostic (2): where the |s| descent actually happens
    ax = axes[0][1]
    labels = [f"trust-region\nCONSTRAINED\nn = {d2['n_constrained']}",
              f"full Newton\nUNCONSTRAINED\nn = {d2['n_unconstrained']}"]
    means = [d2["mean_d_abs_s_constrained"], d2["mean_d_abs_s_unconstrained"]]
    nets = [d2["net_d_abs_s_constrained"], d2["net_d_abs_s_unconstrained"]]
    x = np.arange(2)
    ax.bar(x - 0.19, means, width=0.36, color="#2c3e50",
           label=r"mean per-epoch $d|s|$ (left axis)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel(r"mean per-epoch $d|s|$")
    ax.axhline(0.0, color="k", lw=0.8)
    ax2 = ax.twinx()
    ax2.bar(x + 0.19, nets, width=0.36, color="#c0392b", alpha=0.85,
            label=r"NET $\sum d|s|$ over all epochs (right axis)")
    ax2.set_ylabel(r"net $\sum d|s|$", color="#c0392b")
    ax2.tick_params(axis="y", colors="#c0392b")
    tot = abs(nets[0]) + abs(nets[1])
    frac = abs(nets[0]) / tot if tot > 0 else float("nan")
    # Both axes are given 2.6x headroom below the bars so the reading note has
    # clear white space to sit in rather than covering the magnitudes.
    ax.set_ylim(min(means) * 2.6, max(0.0, max(means)) + abs(min(means)) * 0.1)
    ax2.set_ylim(min(nets) * 2.6, max(0.0, max(nets)) + abs(min(nets)) * 0.1)
    ax.text(0.02, 0.03,
            f"per-epoch RATES are statistically indistinguishable:\n"
            f"observed difference {d2['observed_difference']:+.6f}, "
            f"within-attempt permutation p = {d2['permutation_p']:.4f} "
            f"({d2['n_perm']:,} perms)\n"
            f"but {100 * frac:.1f}% of the total $|s|$ descent happens on "
            f"CONSTRAINED epochs,\nbecause "
            f"{100 * d2['n_constrained'] / d2['n_epochs']:.1f}% of accepted "
            f"steps are constrained at all.\n"
            f"corr(per-epoch $\\Delta\\|R\\|$, $d|s|$) = "
            f"{d2['correlation_dR_vs_dabs_s']:+.4f}",
            transform=ax.transAxes, fontsize=7.5, va="bottom",
            bbox=dict(fc="white", ec="#7f8c8d", alpha=0.9))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7, loc="upper right")
    ax.set_title(
        f"B. diagnostic (2): iteration or minimisation? {d2['verdict']}\n"
        f"{d2['n_epochs']} accepted epochs over "
        f"{d2['coverage']['n_attempts_with_epoch_path']} of "
        f"{d2['coverage']['n_banked_attempts']} banked attempts "
        f"(U3's ledger carries no per-epoch $|s|$)\n"
        f"the seed score itself is monotone in $|s|$: "
        f"Spearman$(|s|, R)$ = {d2['score_bias']['spearman_absS_vs_R']:.4f} "
        f"over {d2['score_bias']['n_m0']} candidates", fontsize=9)
    ax.grid(alpha=0.3, axis="y")

    # C. diagnostic (3): how far each of the 16 direct-seed attempts got
    ax = axes[1][0]
    ax.axhspan(LEG353[0], LEG353[1], color="#7f8c8d", alpha=0.18, zorder=0)
    ax.text(0.015, 0.40,
            f"leg 353's prior: five of these rows attempted, all five failed,\n"
            f"final $\\|R\\|$ in [{LEG353[0]}, {LEG353[1]}] "
            f"(shaded) at reason=line_search_failed",
            transform=ax.transAxes, fontsize=7.5, va="bottom",
            bbox=dict(fc="white", ec="#7f8c8d", alpha=0.9))
    for arm, col, mk in (("S", "#c0392b", "o"), ("Q", "#2c3e50", "s")):
        sub = [a for a in att if a["arm"] == arm]
        ax.scatter([a["seed_extended_residual"] for a in sub],
                   [max(a["final_residual"], TOL / 10) for a in sub],
                   c=col, marker=mk, s=46, alpha=0.85, zorder=3,
                   label=(f"arm {arm} -- "
                          + ("shift-matched field" if arm == "S"
                             else "score-optimal field")
                          + f" ({len(sub)})"))
    lo = min(a["seed_extended_residual"] for a in att)
    hi = max(a["seed_extended_residual"] for a in att)
    ax.plot([lo * 0.9, hi * 1.1], [lo * 0.9, hi * 1.1], "-",
            color="#7f8c8d", lw=1.0, label="no progress at all")
    ax.axhline(TOL, color="#27ae60", ls="--", lw=1.2,
               label=r"$tol = 10^{-8}$")
    for a in att:
        ax.annotate(a["row"].replace("UPO", ""),
                    (a["seed_extended_residual"],
                     max(a["final_residual"], TOL / 10)),
                    fontsize=6, xytext=(3, 3), textcoords="offset points")
    ax.set_yscale("log")
    ax.set_xlabel(r"seed extended residual $\|R\|$ at the "
                  r"field-plus-pinned-$(T, s)$ seed")
    ax.set_ylabel(r"final $\|R\|$ reached")
    ax.set_title(
        f"C. diagnostic (3): {d3['n_attempts']} attempts planted at the "
        f"published $(T, s)$ of the eight named rows\n"
        f"{d3['n_converged']} reached tol; "
        f"{d3['n_recovered_its_own_row']} matched its own row on both $T$ "
        f"and $s$; {d3['n_recovered_any_named_row']} matched any named row\n"
        f"exits: "
        + ", ".join(f"{k} x{v}" for k, v in sorted(d3["reasons"].items())),
        fontsize=9)
    ax.legend(fontsize=7, loc="center right")
    ax.grid(alpha=0.3, which="both")

    # D. diagnostic (3): distance from the published row it was planted at
    ax = axes[1][1]
    FLOOR = 1e-4                      # log axes; exact zeros are drawn here
    ax.add_patch(plt.Rectangle((FLOOR, FLOOR), MATCH_TOL - FLOOR,
                               MATCH_TOL - FLOOR, fc="#27ae60",
                               alpha=0.18, ec="#27ae60", lw=1.4, zorder=1))
    ax.text(FLOOR * 1.3, MATCH_TOL * 0.55,
            "the matching predicate of record:\n"
            r"$|\Delta T| < 0.05$ AND $|\Delta s|_{2\pi} < 0.05$"
            "\nnothing inside this box means no named row was recovered",
            fontsize=7.5, va="top", color="#1e8449")
    for arm, col, mk in (("S", "#c0392b", "o"), ("Q", "#2c3e50", "s")):
        for a in [x for x in att if x["arm"] == arm]:
            ax.scatter([max(a["delta_T_from_published"], FLOOR)],
                       [max(a["delta_s_from_published"], FLOOR)],
                       c=col, marker=mk, s=52 if a["success"] else 30,
                       alpha=0.9 if a["success"] else 0.45,
                       edgecolors="k" if a["success"] else "none",
                       linewidths=0.8, zorder=3)
            ax.annotate(a["row"].replace("UPO", "") + a["arm"],
                        (max(a["delta_T_from_published"], FLOOR),
                         max(a["delta_s_from_published"], FLOOR)),
                        fontsize=6, xytext=(3, 3), textcoords="offset points")
    ax.scatter([], [], c="#c0392b", marker="o", s=52, edgecolors="k",
               linewidths=0.8, label="arm S")
    ax.scatter([], [], c="#2c3e50", marker="s", s=52, edgecolors="k",
               linewidths=0.8, label="arm Q")
    ax.scatter([], [], c="#7f8c8d", marker="o", s=30, alpha=0.45,
               label="did NOT reach tol (open)")
    ax.scatter([], [], c="#7f8c8d", marker="o", s=52, edgecolors="k",
               linewidths=0.8, label="reached tol (outlined)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(FLOOR * 0.7,
                max(max(a["delta_T_from_published"] for a in att),
                    MATCH_TOL) * 2.2)
    ax.set_ylim(FLOOR * 0.7,
                max(max(a["delta_s_from_published"] for a in att),
                    MATCH_TOL) * 2.2)
    ax.set_xlabel(r"$|T_{\rm final} - T_{\rm published}|$")
    ax.set_ylabel(r"$|s_{\rm final} - s_{\rm published}|$ (mod $2\pi$)")
    ca = d3["closest_approach"]
    ax.set_title(
        "D. how far from the row it was planted at each attempt stopped\n"
        f"closest approach: {ca['row']} arm {ca['arm']}, "
        f"$\\Delta T$ = {ca['delta_T_from_published']:.4f}, "
        f"$\\Delta s$ = {ca['delta_s_from_published']:.4f}, "
        f"final $\\|R\\|$ = {ca['final_residual']:.3g}\n"
        f"secondary sign-agnostic $|s|$ matches: "
        f"{d3['n_recovered_abs_secondary']} (NOT the predicate of record)",
        fontsize=9)
    ax.legend(fontsize=7, loc="lower left")
    ax.grid(alpha=0.3, which="both")

    fig.suptitle(
        "fig109  PROG-R4 unit E: the H-hard diagnostic -- all three "
        "diagnostics RETURNED, each with a planted control that fired BOTH "
        "ways.\n"
        f"Re={d['realization']['Re']}, N=24, dt={d['realization']['dt']}, "
        "Lie-Trotter split (globally FIRST order), Newton-GMRES-hookstep, "
        f"{d3['resourcing']['core_hours']:.1f} core-hours.\n"
        "G1 stays UNDER-RESOURCED. This is a measurement of THIS realization "
        "at THIS budget, not a verdict about the published rows.",
        fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    fig.savefig(FIG, dpi=150)
    print(f"wrote {FIG}")

    bad = [n for n, ok_, _ in CHECKS if not ok_]
    print(f"\n{len(CHECKS) - len(bad)}/{len(CHECKS)} checks passed")
    if bad:
        print("FAILED: " + ", ".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
