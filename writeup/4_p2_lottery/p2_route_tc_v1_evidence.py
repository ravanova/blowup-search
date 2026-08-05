"""Phase-2 Route-TC v1 (fig48): the four terms in one polynomial, and the term that ran out
is the one that never existed before -- the COUPLING between the finite block and the
bordered tail.

Leg 52 measured the bordered tail's inverse norm in isolation and got a bounded constant
(9.44 at s = 0, 11.37 at s = 0.3). This leg gives the far-field amplitude its own column,
its own matching row and its own place in the radii polynomial, and measures what a
certificate actually has to carry. The tail term is fine. The four sub-blocks of `I - A L`
are not: with `A = Gamma^{-1} (+) A_tail` -- the block-diagonal shape the method requires --
the two OFF-DIAGONAL blocks are 43.2 and 1.39 at their best split and grow like K.

Rebuild fig48 from committed data (no recomputation):
    .venv/bin/python writeup/4_p2_lottery/p2_route_tc_v1_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_tc_v1_assemble.py

Six panels: A the four terms in one polynomial at the best split; B Z_1 by sub-block across
every split and both admissible classes, against the line Z_1 = 1; C the far-field column
that TC-1 had to write down, including the gauge entry that does not converge; D the
positive control -- dissipation brings the same coupling below 1; E the negative controls;
F the ceiling, pre-committed.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
JSON = DATA / "p2_route_tc_v1_assemble.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def clabel(r):
    return "flat" if r["class"] == "flat" else f"s={r['param']:g}"


def build_figure():
    d = json.loads(JSON.read_text())
    sweep = d["TC4_z1_subblocks"]
    polys = d["TC2_polynomial"]
    best = d["TC4_best"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: the four terms, in one polynomial, at the best split ----------
    a = ax[0, 0]
    p = min(polys, key=lambda q: q["Z1"])
    names = [r"$Y_0$" + "\n(exactly 0)", r"$Z_1$ finite" + "\nblock",
             r"$Z_1$[tail$\leftarrow\Gamma$]", r"$Z_1$[$\Gamma\leftarrow$tail]",
             "tail const\n(leg 52)", r"$Z_2$"]
    floor = 1e-16
    vals = [p["Y0"], p["Z1_finite_block_rigorous"], p["Z1_tail_Gamma"],
            p["Z1_Gamma_tail"], p["tail_constant"], p["Z2"]]
    cols = [C["good"], C["good"], C["bad"], C["bad"], C["anchor"], C["warn"]]
    bars = a.bar(range(len(vals)), [max(v, floor) for v in vals], color=cols, alpha=0.9)
    a.set_yscale("log")
    a.axhline(1.0, color="k", ls="--", lw=1.4)
    a.set_xticks(range(len(vals)))
    a.set_xticklabels(names, fontsize=7.6)
    for b, v in zip(bars, vals):
        a.text(b.get_x() + b.get_width() / 2, max(v, floor) * 2.0,
               "0" if v == 0 else f"{v:.3g}", ha="center", fontsize=8.5)
    a.set_ylabel("magnitude (weighted $\\ell^1$)")
    a.set_title(f"A. the four terms in ONE polynomial\n"
                f"({clabel(p)}, K = {p['K']}, the best split in the whole sweep)",
                fontsize=10)
    a.set_ylim(floor / 3, max(vals) * 300)
    a.text(-0.44, 1e-5, r"$Z_1 = 1$ (dashed): above it," + "\nnothing closes",
           fontsize=8.2)
    a.text(-0.44, 1e-9, r"$Y_0$ is exactly 0 because" + "\nthe anchor IS one basis mode",
           fontsize=7.6, color=C["grey"])

    # ---- B: Z_1 by sub-block, every split, both admissible classes --------
    b = ax[0, 1]
    for kind, p_, mk in (("flat", 0.0, "o"), ("algebraic", 0.3, "s")):
        rows = [r for r in sweep if r["class"] == kind and r["param"] == p_
                and r["gauge"] == "null"]
        Ks = [r["K"] for r in rows]
        b.loglog(Ks, [r["Z1_Gamma_tail"] for r in rows], mk + "-", color=C["bad"],
                 lw=2.2, ms=5, label=rf"$Z_1[\Gamma\leftarrow$tail$]$  {clabel(rows[0])}")
        b.loglog(Ks, [r["Z1_tail_Gamma"] for r in rows], mk + "--", color=C["warn"],
                 lw=2.0, ms=5, label=rf"$Z_1[$tail$\leftarrow\Gamma]$  {clabel(rows[0])}")
        b.loglog(Ks, [max(r["Z1_Gamma_Gamma"], 1e-17) for r in rows], mk + ":",
                 color=C["good"], lw=1.6, ms=4,
                 label=rf"$Z_1[\Gamma\Gamma]$  {clabel(rows[0])}")
    b.axhline(1.0, color="k", ls="--", lw=1.4)
    tg = d["term_that_ran_out"]["finite_block_independent_term"]
    b.annotate("min = %.4f: the only finite-block-\nINDEPENDENT sub-block, and it is BELOW 1"
               % tg["min_over_every_split_and_class"],
               xy=(4.1, tg["min_over_every_split_and_class"]), xytext=(5.2, 2e-7),
               fontsize=7.0,
               arrowprops=dict(arrowstyle="->", lw=1.0, color=C["warn"]))
    b.set_xlabel("K   (the split between finite block and tail)")
    b.set_ylabel(r"sub-block norm of $I - AL$")
    b.set_title(r"B. every sub-block, every split: the coupling blocks grow "
                "\n" r"$\times 2$ and $\times 4$ per doubling of $K$; the diagonal ones "
                r"are at $10^{-13}$", fontsize=10)
    b.legend(fontsize=7.2, loc="lower right", ncol=2)

    # ---- C: the far-field column TC-1 had to write down -------------------
    c = ax[0, 2]
    ff = d["TC1_far_field_column"]
    Ks = [r["K"] for r in ff]
    c.loglog(Ks, [r["row_K_entry"] for r in ff], "o-", color=C["anchor"], lw=2.2,
             label=r"row $K$:  $(K{+}1)/2$")
    c.loglog(Ks, [abs(r["row_1_entry"]) for r in ff], "s-", color=C["ours"], lw=2.2,
             label=r"row 1:  $\sum_{m>K}-(-1)^m h_m$")
    c.loglog(Ks, [r["gauge_entry"] for r in ff], "^-", color=C["bad"], lw=2.4,
             label=r"gauge row:  $\sum_{m>K} m\,h_m$  (LOG-DIVERGENT)")
    c.set_xlabel("K")
    c.set_ylabel("entry of the far-field column")
    c.set_title("C. TC-1: the amplitude's column in the finite block\n"
                "— explicit, and one entry of it does not exist", fontsize=10)
    c.legend(fontsize=7.6, loc="upper left")
    c.set_ylim(1.0, 4e4)
    ins = c.inset_axes((0.60, 0.06, 0.37, 0.28))
    gl = d["TC3_border_defect"]["gauge_row_ladder"]
    ins.semilogx([g["M_extra"] for g in gl], [g["gauge_entry"] for g in gl], "o-",
                 color=C["bad"], lw=1.8, ms=4)
    ins.set_title(f"+{d['TC3_border_defect']['gauge_row_growth_per_efold_in_M']:.0f}"
                  " per e-fold in M", fontsize=6.8)
    ins.tick_params(labelsize=6)
    ins.set_xlabel("modes carried past the split", fontsize=6.2, labelpad=1)

    # ---- D: the positive control ------------------------------------------
    e = ax[1, 0]
    ctrl = d["TC5_positive_control"]
    for kind, p_, mk in (("flat", 0.0, "o"), ("algebraic", 0.3, "s")):
        rows = sorted([r for r in ctrl if r["class"] == kind and r["param"] == p_],
                      key=lambda r: r["mu"])
        mus = [max(r["mu"], 0.03) for r in rows]
        e.loglog(mus, [r["Z1_tail_Gamma"] for r in rows], mk + "-", color=C["good"],
                 lw=2.2, ms=5, label=rf"$Z_1[$tail$\leftarrow\Gamma]$  {clabel(rows[0])}")
        e.loglog(mus, [r["Z1_Gamma_tail"] for r in rows], mk + "--", color=C["warn"],
                 lw=2.0, ms=5, label=rf"$Z_1[\Gamma\leftarrow$tail$]$  {clabel(rows[0])}")
    e.axhline(1.0, color="k", ls="--", lw=1.4)
    e.set_xlabel(r"$\mu$   ($\Lambda^1$ dissipation; $\mu=0$ plotted at 0.03)")
    e.set_ylabel("coupling sub-block norm")
    e.set_title("D. positive control: give the operator a DIAGONAL and the\n"
                "same coupling falls below 1 — the instrument can say yes", fontsize=10)
    e.legend(fontsize=7.2, loc="lower left", ncol=2)

    # ---- E: negative controls ---------------------------------------------
    f = ax[1, 1]
    neg = d["TC5b_negative_controls"]
    x = np.arange(len(neg), dtype=float)
    cc = [C["good"] if r["border"] == "analytic" else C["grey"] for r in neg]
    b1 = f.bar(x - 0.19, [r["Z1_tail_Gamma"] for r in neg], width=0.36, color=cc,
               alpha=0.9, label=r"$Z_1[$tail$\leftarrow\Gamma]$")
    b2 = f.bar(x + 0.19, [r["Z1_Gamma_tail"] for r in neg], width=0.36, color=cc,
               alpha=0.55, hatch="//", label=r"$Z_1[\Gamma\leftarrow$tail$]$")
    f.set_yscale("log")
    f.set_xticks(x); f.set_xticklabels([r["border"] for r in neg], fontsize=9)
    f.axhline(1.0, color="k", ls="--", lw=1.4)
    for bb, r in list(zip(b1, neg)):
        f.text(bb.get_x() + bb.get_width() / 2, r["Z1_tail_Gamma"] * 1.6,
               f"{r['Z1_tail_Gamma']:.3g}", ha="center", fontsize=7.2)
    for bb, r in list(zip(b2, neg)):
        f.text(bb.get_x() + bb.get_width() / 2, r["Z1_Gamma_tail"] * 1.6,
               f"{r['Z1_Gamma_tail']:.3g}", ha="center", fontsize=7.2)
    f.set_ylabel("sub-block norm")
    f.set_ylim(0.7, max(r["Z1_Gamma_tail"] for r in neg) * 200)
    f.legend(fontsize=7.6, loc="upper left")
    f.set_title("E. negative controls (s=0.3, K=16), REWIRED so they CAN fail:\n"
                f"analytic/SVD = {d['TC5b_analytic_over_svd']:.4f}; wrong directions up to "
                f"{d['TC5b_worst_over_analytic']:.1g}x worse", fontsize=10)

    # ---- F: the ceiling ---------------------------------------------------
    g = ax[1, 2]
    g.axis("off")
    tt = d["term_that_ran_out"]
    txt = (
        "  GATE: does the radii polynomial close on the a = 0 CLM\n"
        "  object, in a class with s < 0.394, with the far-field\n"
        "  amplitude carried as a real unknown through all four\n"
        "  terms?\n\n"
        "                        ANSWER: NO\n\n"
        f"  TERM THAT RAN OUT: {tt['name']}\n"
        f"  smallest value anywhere in the sweep: "
        f"{tt['min_over_every_split_and_class']:.4g}\n"
        "  (K = 4..64, both admissible classes, both gauges),\n"
        "  and 20.47 over every normalisation ablated in TC-8.\n\n"
        "  SCOPE: this term CONTAINS Gamma^-1 (= 2||Gamma^-1||\n"
        "  under the shipped convention), so what is established\n"
        "  is that the BLOCK-DIAGONAL A the method requires\n"
        "  cannot close it -- NOT that no finite block can. The\n"
        "  finite-block-INDEPENDENT sub-block Z_1[tail<-Gamma]\n"
        "  has minimum 0.9961, BELOW 1. That is why stage MM\n"
        "  is a real question and not a formality.\n\n"
        "  Y_0 = 0 EXACTLY -- including the new matching row --\n"
        "  because the anchor IS one basis mode and has no far\n"
        "  field. So r = 0 is a root for a DEGENERATE reason and\n"
        "  certifies nothing; the reportable quantity is a\n"
        "  POSITIVE interval, which needs Z_1 < 1.\n\n"
        "  The TAIL is not what ran out: leg 52's constant is\n"
        "  2.19-10.3 here and behaves. What ran out did not exist\n"
        "  until the pieces were in the same polynomial.\n\n"
        "  Nothing claimed about HL_S2_nonsymmetric -- on the\n"
        "  gate's own terms that run happens only if this closes.\n"
        "  NO LINK OF THE L1->L4 CHAIN MOVED.  Clay ~0.05%."
    )
    g.text(0.02, 1.0, txt, va="top", ha="left", fontsize=8.4, family="monospace")
    g.set_title("F. the ceiling, pre-committed before the numbers", fontsize=10)

    fig.suptitle("Route-TC v1 — assembling the bordered certificate: the tail term was "
                 "never the binding one, the COUPLING is", fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig48_route_tc_v1_assemble.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
