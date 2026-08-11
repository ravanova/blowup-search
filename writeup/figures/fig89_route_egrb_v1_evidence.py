"""Route-EGRB v1 (leg 340) -- EVIDENCE + FIGURE.

Re-derives, from the curated `writeup/data/p2_route_egrb_v1.json`, every number
leg 340's journal and writeups quote, and builds
`writeup/figures/fig89_route_egrb_v1_ladder.png`.

Nothing is recomputed here: the exact rational-plus-pi arithmetic lives in the
one runner, `experiments/p2_route_egrb_v1.py`. This script reads its output and
asserts the relations the prose asserts -- including the ones that cut AGAINST
the leg's headline (the tautology reading, and the A4 control's failure).

It sits in `writeup/figures/` rather than the usual `experiments/` because leg
340's declared territory is `writeup/figures/fig89*`; `experiments/*_evidence.py`
and `writeup/build_figures.py` are outside it and are left for integration --
the same choice leg 329 made and recorded for `fig81`.

    python3 writeup/figures/fig89_route_egrb_v1_evidence.py
"""
import json
import os
import sys
from decimal import Decimal
from fractions import Fraction

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_egrb_v1.json")
FIG = os.path.join(HERE, "fig89_route_egrb_v1_ladder.png")

CEILING = 0.5
CEILING_SLACK = 1e-9
PRIMARY = ("B4_egm", "E_egm")
COLOR = {"B4_egm": "#1f4e9c", "E_egm": "#0f8a6a", "A4_chen_hou": "#b03030"}

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-64s %s" % ("ok" if ok else "FAIL", name, detail))


def rung_sort_key(k):
    parts = dict(p.split("=") for p in k.split("|"))
    return (int(parts["n"]), int(parts["n_grade"]), float(parts["rcond"]))


def main():
    with open(DATA) as fh:
        d = json.load(fh)
    lad = d["ladder"]
    keys = sorted(lad, key=rung_sort_key)
    ctl = d["controls"]

    # ------------------------------------------------------------------ checks
    check("gate answers yes", d["gate"]["answer"] == "yes", d["gate"]["answer"])
    check("19 ladder rungs evaluated", len(keys) == 19, f"{len(keys)}")

    exact = {lad[k][w]["R_exact_rational"] for k in keys for w in PRIMARY}
    check("every primary rung's exact quotient is the SAME rational",
          exact == {"-1/2"}, str(sorted(exact)))
    check("...and that rational is exactly -1/2",
          all(Fraction(lad[k][w]["R_exact_rational"]) == Fraction(-1, 2)
              for k in keys for w in PRIMARY))
    check("so the bound's dependence on the truncation parameter is exactly 0",
          d["truncation_dependence"]["exact_bound_spread_over_all_rungs"] == "0")

    ceil_d = Decimal(CEILING) + Decimal(CEILING_SLACK)
    check("every primary rung's ENCLOSURE lies at or below 1/2 + 1e-9",
          all(Decimal(lad[k][w]["bound_hi"]) <= ceil_d for k in keys for w in PRIMARY))
    wmax = max(Decimal(lad[k][w]["bound_width"]) for k in keys for w in PRIMARY)
    check("enclosure width << distance to the ceiling (control K7)",
          wmax < Decimal(CEILING_SLACK), f"max width {wmax:.1e} vs 1e-9")

    check("nonlocal term int sin(th) phi (Hh) h dth vanishes EXACTLY, every rung",
          all(lad[k][w]["nonlocal_is_exactly_zero"] for k in keys for w in PRIMARY))
    check("trial vectors satisfy BOTH constraints with exact integer residual 0",
          all(lad[k][w]["trial_vector_dprime_residual"] == 0
              and lad[k][w]["trial_vector_hilbert_residual"] == 0
              for k in keys for w in PRIMARY))

    # controls, including the ones that can cut against
    for cid in ("K1_reproduction", "K1b_mp_quadrature_at_the_same_vector",
                "K2_A4_negative_control", "K3_divergence_control",
                "K4_point_mode", "K5_weight_scaling", "K6_ladder_coverage",
                "K7_enclosure_width", "K8_decimal_crosscheck",
                "K9_byparts_identity", "structural_matrix_identity"):
        check(f"control {cid} passed", ctl[cid]["passed"] is True)

    check("K1 reproduces leg 329's banked C4 to 0.0 exactly",
          all(r["abs_difference"] == 0.0 for r in ctl["K1_reproduction"]["rows"]),
          str([r["abs_difference"] for r in ctl["K1_reproduction"]["rows"]]))
    check("K2: A4_chen_hou is NOT -1/2 at any rung (instrument is not a tautology"
          " of the code)",
          not any(r["equals_half"] for r in ctl["K2_A4_negative_control"]["rows"]))
    check("K9 is two-sided: the by-parts residual is 0 for B4/E and NONZERO for A4",
          ctl["K9_byparts_identity"]["primary_rows_all_zero"]
          and not ctl["K9_byparts_identity"]["A4_rows_all_zero"])
    check("K4: the dprime-only point mode is exactly R = +1 (Xu's spectrum {0,1})",
          ctl["K4_point_mode"]["R_exact"] == "1")

    eig = d["truncation_dependence"]["eigensolve_gap_spread"]
    check("eigensolve gap spread reproduces leg 329's C5 relative spread (B4)",
          abs(eig["B4_egm"]["spread_relative"] - 3.853e-05) < 1e-08,
          f"{eig['B4_egm']['spread_relative']:.4e} vs banked 3.853e-05")
    check("eigensolve gap spread reproduces leg 329's C5 relative spread (E)",
          abs(eig["E_egm"]["spread_relative"] - 5.394e-05) < 1e-08,
          f"{eig['E_egm']['spread_relative']:.4e} vs banked 5.394e-05")

    check("the MANDATORY SECOND READING is present in the banked gate record",
          "TAUTOLOGY" in d["gate"]["MANDATORY_SECOND_READING"])
    check("escalation #3 is recorded as the USER's decision, not this leg's",
          any("escalation #3" in s for s in d["gate"]["what_this_does_NOT_establish"]))

    # ------------------------------------------------------------------ figure
    fig, (ax, ax2) = plt.subplots(
        2, 1, figsize=(11.2, 8.4), gridspec_kw={"height_ratios": [2.15, 1.0]})

    xs = list(range(len(keys)))
    for w in PRIMARY:
        ys = [lad[k][w]["gap_eigensolve"] - CEILING for k in keys]
        ax.plot(xs, ys, "o-", ms=4.5, lw=1.1, color=COLOR[w], alpha=0.9,
                label=w + ": truncated eigensolve, gap$-\\frac{1}{2}$ "
                      "(leg 329's own path)")
    ya4 = [lad[k]["A4_chen_hou"]["gap_eigensolve"] - CEILING for k in keys]
    ax.plot(xs, ya4, "s--", ms=3.6, lw=0.9, color=COLOR["A4_chen_hou"], alpha=0.75,
            label="A4_chen_hou: eigensolve (negative control, above the ceiling)")

    a4_exact = [float(Fraction(lad[k]["A4_chen_hou"]["R_exact_rational"])) * -1
                - CEILING for k in keys]
    ax.plot(xs, a4_exact, "s", ms=7, mfc="none", mew=1.6,
            color=COLOR["A4_chen_hou"],
            label="A4_chen_hou: EXACT bound (control K2 -- fails the ceiling)")

    ax.axhline(0.0, color="#111111", lw=2.4, zorder=5,
               label="EXACT bound, B4 and E, ALL 19 rungs: identically $-R=\\frac{1}{2}$")
    ax.axhline(CEILING_SLACK, color="#888888", ls=":", lw=1.4,
               label="clause 5 ceiling, $\\frac{1}{2}+10^{-9}$ (leg 178's own slack)")

    ax.set_yscale("symlog", linthresh=1e-12)
    ax.set_xticks(xs)
    ax.set_xticklabels([k.replace("|", "\n").replace("n_grade", "ng")
                        for k in keys], fontsize=6.0, rotation=90)
    ax.set_ylabel("value $-\\ \\frac{1}{2}$   (symlog, $\\mathrm{linthresh}=10^{-12}$)")
    ax.grid(alpha=0.25, lw=0.5)
    ax.legend(fontsize=7.6, loc="lower left", framealpha=0.95, ncol=1)
    ax.set_title("Leg 340 (Route-EGRB): the one-sided bound recomputed in EXACT "
                 "rational$+\\pi$ arithmetic at every rung of leg 329's ladder\n"
                 "the truncated eigensolve wanders by $1.9\\times10^{-5}$; the exact "
                 "bound is the flat line, and it is not flat because it converged "
                 "— it never depended on the rung at all",
                 fontsize=9.6, fontweight="bold")

    # -- lower panel: the sensitivity comparison the DM's ruling turned on
    labels = ["leg 329 C4 'margin'\nbelow $\\frac{1}{2}$ (B4)",
              "leg 329 C4 'margin'\nbelow $\\frac{1}{2}$ (E)",
              "leg 329 C5 truncation\nsensitivity (B4)",
              "leg 329 C5 truncation\nsensitivity (E)",
              "clause 5 slack\n$10^{-9}$",
              "THIS LEG: exact bound's\ndependence on truncation"]
    vals = [5.18779822259e-18, 1.42393407007e-18, 3.853e-05, 5.394e-05, 1e-9, 0.0]
    cols = ["#7aa6d6", "#7ac6b0", "#b03030", "#d06a6a", "#888888", "#111111"]
    FLOOR = 1e-22
    plot_vals = [v if v > 0 else FLOOR for v in vals]
    bars = ax2.bar(range(len(vals)), plot_vals, color=cols, alpha=0.9)
    ax2.set_yscale("log")
    ax2.set_ylim(FLOOR, 1e-3)
    ax2.set_xticks(range(len(vals)))
    ax2.set_xticklabels(labels, fontsize=7.0)
    ax2.set_ylabel("magnitude")
    ax2.grid(axis="y", alpha=0.25, lw=0.5)
    for i, (b, v) in enumerate(zip(bars, vals)):
        txt = "EXACTLY 0\n(drawn at the axis floor —\nit has no magnitude)" \
            if v == 0 else f"{v:.3g}"
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() * 1.5, txt,
                 ha="center", va="bottom", fontsize=7.0,
                 fontweight="bold" if v == 0 else "normal")
    ax2.set_title("why leg 329's C4 margin could not carry clause 5, and what "
                  "replaced it: the DM ruled the 5.2e-18 margin sits 13 orders "
                  "BELOW the measured truncation sensitivity", fontsize=8.6)

    fig.text(0.012, 0.005,
             "MANDATORY SECOND READING (pre-registered, novelty pass §7e): the exact "
             "value $-1/2$ is an IDENTITY on $T_{2,\\mathrm{egm}}$ — $\\mathrm{Sym}(B)"
             "=-G/2$ entry by entry — so clause 5 is a TAUTOLOGY on this class and "
             "cannot come out otherwise.\nA flip of leg 178's NO on this clause would "
             "be a flip ON AN IDENTITY, not a measurement of a coercivity gap. "
             "Escalation #3 is the user's decision. Leg 178's gate text is untouched.",
             fontsize=7.4, style="italic", va="bottom")

    fig.tight_layout(rect=(0, 0.055, 1, 1))
    fig.savefig(FIG, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"\nwrote {FIG}")

    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
