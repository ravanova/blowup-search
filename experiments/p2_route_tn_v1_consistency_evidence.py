"""Phase-2 Route-TN v1 (fig51): L1 step one's OTHER named gap, enclosed -- the consistency
of (H, D) with the operators they discretise.

`solver/interval_certificate.py` closes the radii polynomial on `HL_S2_nonsymmetric` and its
own docstring names two reasons that is a statement about a DISCRETE system: the far field
beyond X_max, and the consistency of (H, D). Legs 51-53 attacked the first, in the
coefficient basis. This leg measures the second, in the collocation basis, at FIXED reach --
X_max = 745.24 in every run, so this is not the banned "extend the domain" move.

The certificate can absorb an added residual of at most tau = budget / ||A||_w. At n = 801
that is 2.31e-14. The measured defects are 4.27e-07 (derivative) and 4.70e-03 (Hilbert).
The gate answers NO by seven and eleven orders of magnitude respectively -- and the two
defects fail for DIFFERENT reasons, which is the actual content:

  * the derivative defect converges at the natural-spline order 4 and is simply far too
    large at any reachable n (order 4 from 4.27e-07 to 2.31e-14 needs n ~ 5.2e+04);
  * the Hilbert defect DOES NOT CONVERGE AT ALL -- 1.005x over a 4x refinement -- because
    `line_hilbert_matrix` builds only interior source columns and so silently imposes
    f(+-X_max) = 0 on whatever it is handed.

Rebuild fig51 from committed data (no recomputation):
    .venv/bin/python experiments/p2_route_tn_v1_consistency_evidence.py
Regenerate the data (deterministic):
    .venv/bin/python -u experiments/p2_route_tn_v1_consistency.py

Six panels: A the refinement ladder against the admissible defect tau; B the mechanism
ablation (a control that could have come out the other way, and did not); C the defect as a
curve in the test class's scale, because there is no operator norm to quote; D the two gaps
kept separate; E the budget arithmetic on one axis; F the gate answer and its ceiling.
"""

import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DATA = ROOT / "writeup" / "data"
FIGS = ROOT / "writeup" / "figures"
JSON = DATA / "p2_route_tn_v1_consistency.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def main():
    d = json.loads(JSON.read_text())
    R = d["rates"]
    ns = np.array(R["n"], dtype=float)
    taus = np.array([r["ratios"]["tau"] for r in d["rungs"]])
    dD = np.array(R["defect_D_odd"])
    dH = np.array(R["defect_H_odd"])
    tr = np.array(R["truncation_odd"])
    v = d["verdict"]

    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.6))
    fig.suptitle("Route-TN v1 (leg 56) -- the (H, D) consistency gap of L1 step one, "
                 "enclosed at FIXED reach (X_max = %.1f).  GATE: NO."
                 % d["rungs"][0]["certificate"]["X_max"],
                 fontsize=13, fontweight="bold")

    # -- A: the ladder against the admissible defect -------------------------
    a0 = ax[0, 0]
    a0.loglog(ns, dH, "o-", color=C["bad"], lw=2, label=r"Hilbert defect $\|H_{disc}f-H_Mf\|_w$")
    a0.loglog(ns, dD, "s-", color=C["warn"], lw=2, label=r"derivative defect $\|D_{disc}f-f'\|_w$")
    a0.loglog(ns, taus, "^--", color=C["good"], lw=2,
              label=r"$\tau$ = budget / $\|A\|_w$  (admissible)")
    a0.loglog(ns, dD[0] * (ns / ns[0]) ** -4.0, ":", color=C["grey"], lw=1.5,
              label=r"order 4 (spline)")
    a0.set_xlabel("n"); a0.set_ylabel("weighted sup norm")
    a0.set_title("A. the ladder: both defects sit far above what the\n"
                 "certificate can absorb, and only one of them falls", fontsize=10)
    a0.legend(fontsize=7.5, loc="center left")
    a0.grid(alpha=0.3, which="both")
    a0.annotate(r"$\times$%.1e too big" % v["defect_H_over_tau_at_801"],
                xy=(ns[-1], dH[-1]), xytext=(-118, -22), textcoords="offset points",
                fontsize=8, color=C["bad"], fontweight="bold")

    # -- B: the mechanism ablation -------------------------------------------
    a1 = ax[0, 1]
    ab = d["mechanism_ablation"]
    x = np.arange(len(ab)); w = 0.19
    a1.bar(x - 1.5 * w, [r["defect_H_odd"] for r in ab], w, color=C["bad"], label="H, odd (1/X at cut)")
    a1.bar(x - 0.5 * w, [r["defect_H_even"] for r in ab], w, color=C["bad"], alpha=0.4,
           label=r"H, even (1/X$^2$ at cut)")
    a1.bar(x + 0.5 * w, [r["defect_D_odd"] for r in ab], w, color=C["warn"], label="D, odd")
    a1.bar(x + 1.5 * w, [r["defect_D_even"] for r in ab], w, color=C["warn"], alpha=0.4, label="D, even")
    a1.set_yscale("log"); a1.set_xticks(x); a1.set_xticklabels(["n=%d" % r["n"] for r in ab])
    a1.set_ylabel("weighted sup norm")
    a1.set_title("B. the mechanism, ablated (lesson 90): same interior\n"
                 "smoothness, %.0fx different value AT THE CUT" % (745.24 / 0.5), fontsize=10)
    a1.legend(fontsize=7.5)
    a1.grid(alpha=0.3, axis="y")
    a1.set_xlim(-0.55, len(ab) - 0.45)
    top = max(r["defect_H_odd"] for r in ab)
    a1.set_ylim(top=top * 60.0)
    for i, r in enumerate(ab):
        a1.text(i, top * 12.0,
                "H collapses %.0fx\nD moves %.2fx" % (r["defect_H_collapse"],
                                                      r["defect_D_collapse"]),
                ha="center", va="center", fontsize=8, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=C["grey"], lw=0.8))

    # -- C: the scale curve --------------------------------------------------
    a2 = ax[0, 2]
    sc = d["scale_curve"]
    aa = np.array([s["a"] for s in sc])
    a2.loglog(aa, [s["defect_H_abs"] for s in sc], "o-", color=C["bad"], lw=2, label="Hilbert")
    a2.loglog(aa, [s["defect_D_abs"] for s in sc], "s-", color=C["warn"], lw=2, label="derivative")
    a2.axhline(d["rungs"][-1]["ratios"]["tau"], color=C["good"], ls="--", lw=2, label=r"$\tau$")
    a2.set_xlabel("test-class scale  a"); a2.set_ylabel("weighted sup norm")
    a2.set_title("C. there is no operator norm to quote (lesson 73):\n"
                 "the defect is a CURVE in the class, at n = %d" % d["scale_curve_n"], fontsize=10)
    a2.legend(fontsize=8); a2.grid(alpha=0.3, which="both")

    # -- D: the two gaps kept separate ---------------------------------------
    a3 = ax[1, 0]
    a3.semilogy(ns, tr, "d-", color=C["ours"], lw=2, label="far-field truncation (the OTHER gap)")
    a3.semilogy(ns, dH, "o-", color=C["bad"], lw=2, label="consistency, Hilbert (THIS leg)")
    a3.semilogy(ns, dD, "s-", color=C["warn"], lw=2, label="consistency, derivative (THIS leg)")
    a3.set_xlabel("n"); a3.set_ylabel("weighted sup norm")
    a3.set_title("D. two defects in the same problem are not the same\n"
                 "defect (75): reach is FIXED, only n moves", fontsize=10)
    a3.legend(fontsize=8); a3.grid(alpha=0.3)

    # -- E: the budget arithmetic --------------------------------------------
    a4 = ax[1, 1]
    c8 = d["rungs"][-1]["certificate"]
    ref = d["leg46_reference_as_stored"]
    labels = [r"budget (re-derived)", r"$Y_0$ leg 46, stored", r"$Y_0$ re-derived here",
              r"$\tau$ = budget/$\|A\|$", r"defect $D$", r"defect $H$"]
    vals = [c8["budget"], ref["Y0"], c8["Y0"], c8["tau_admissible_defect"],
            v["defect_D_at_801"], v["defect_H_at_801"]]
    cols = [C["good"], C["anchor"], C["grey"], C["good"], C["warn"], C["bad"]]
    a4.barh(np.arange(len(vals)), vals, color=cols)
    a4.set_xscale("log"); a4.set_yticks(np.arange(len(vals))); a4.set_yticklabels(labels, fontsize=9)
    a4.set_xlabel("weighted sup norm (n = 801)")
    a4.set_title("E. the comparison is through $\\|A\\|_w$ (67); $\\tau$ is the FRIENDLIEST\n"
                 "threshold there is. budget and $\\|A\\|$ re-derive EXACTLY; $Y_0$ does not",
                 fontsize=10)
    a4.grid(alpha=0.3, axis="x")
    for i, val in enumerate(vals):
        a4.text(val * 1.5, i, "%.3g" % val, va="center", fontsize=8)

    # -- F: the gate and the ceiling -----------------------------------------
    a5 = ax[1, 2]; a5.axis("off")
    ex = d["D_only_extrapolation"]
    txt = (
        "GATE (pre-committed)\n"
        "Can the (H, D) consistency defect be enclosed by a\n"
        "rigorous bound smaller than leg 46's $Y_0$ budget at\n"
        "n = 801, with a rate across 201/401/801?\n\n"
        "ANSWER: NO.\n\n"
        r"   admissible  $\tau$ = %.3e" "\n"
        r"   derivative  %.3e   = %.2e $\tau$   order %.2f" "\n"
        r"   Hilbert     %.3e   = %.2e $\tau$   order %.2f" "\n\n"
        "THE TWO FAIL DIFFERENTLY, AND THAT IS THE RESULT.\n"
        "D converges at the spline order and is merely far too\n"
        "large: order 4 would need n ~ %.0f (N = %.0f, dense).\n"
        "H does not converge at all -- %.4fx over a 4x refinement.\n\n"
        "MECHANISM (ablated, not asserted). line_hilbert_matrix\n"
        "builds interior source columns only, so it imposes\n"
        "f(+-X_max) = 0 on its input. A test family that already\n"
        "nearly vanishes there drops H's defect %.0fx and moves\n"
        "D's by %.2fx. The control could have come out otherwise.\n\n"
        "CEILING. Nothing here is a statement about the far-field\n"
        "gap, about HL_S2_nonsymmetric's certification, or about\n"
        "any link of the L1-L4 chain. No link moved. Clay ~0.05%%."
    ) % (v["tau_at_801"],
         v["defect_D_at_801"], v["defect_D_over_tau_at_801"],
         v["D_rate_per_doubling"][-1]["order"],
         v["defect_H_at_801"], v["defect_H_over_tau_at_801"],
         v["H_rate_per_doubling"][-1]["order"],
         ex["n_required"], 2 * ex["n_required"] + 3,
         dH[0] / dH[-1],
         ab[-1]["defect_H_collapse"], ab[-1]["defect_D_collapse"])
    a5.text(0.0, 1.0, txt, va="top", ha="left", fontsize=8.2, family="monospace",
            bbox=dict(boxstyle="round", fc="#fbf7ef", ec=C["bad"], lw=1.6))

    fig.tight_layout(rect=[0, 0, 1, 0.955])
    out = FIGS / "fig51_route_tn_v1_consistency.png"
    fig.savefig(out, dpi=145)
    print("wrote", out)


if __name__ == "__main__":
    main()
