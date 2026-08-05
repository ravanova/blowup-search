"""Phase-2 Route-T v1 (fig47): bordering restores a bounded tail, and it works where
leg 51's failure curve was WORST.

Leg 51 measured a divergent tail term in every weight class and read the minimum of the
divergence curve as "least bad". This leg decomposes that curve by MECHANISM -- the kernel
is in the space iff s < 1, the cokernel functional is bounded iff s >= 1 -- and shows the
minimum is the one exponent where BOTH hold marginally, hence the one place bordering
cannot help. One border row and one border column then bound the tail in the admissible
classes, with the analytic far-field mode achieving the SVD optimum to three digits.

Rebuild fig47 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_t_v1_evidence.py
Regenerate the data (deterministic, ~154 s):
    .venv/bin/python -u experiments/p2_route_t_v1_border.py

Six panels: A THE PICTURE -- the ladders, bordered against unbordered, per class; B the
two Fredholm sides and why the U-curve's minimum was a trap; C the analytic border against
the best one that exists; D the alignment, degrading exactly where the repair does; E the
negative controls; F the ceiling, pre-committed.
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
JSON = DATA / "p2_route_t_v1_border.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def label(r):
    return "flat" if r["class"] == "flat" else f"s={r['param']:g}"


def build_figure():
    d = json.loads(JSON.read_text())
    lad = d["T1_ladders"]
    alpha = d["target_alpha"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: THE PICTURE -- bordered vs unbordered ladders -----------------
    a = ax[0, 0]
    for r in lad:
        adm = r["object_has_finite_norm"]
        col = C["good"] if adm else C["bad"]
        a.loglog(r["M"], r["unbordered"], ":", color=C["grey"], lw=1.2)
        a.loglog(r["M"], r["analytic"], "-o", color=col, ms=4.5,
                 lw=2.4 if adm else 1.4,
                 label=f"{label(r)}{'  (admissible)' if adm else ''}")
    a.loglog([], [], ":", color=C["grey"], label="unbordered (all classes)")
    a.set_xlabel("M   (modes retained before the tail)")
    a.set_ylabel(r"$\|T^{-1}\|_w$   bordered")
    a.set_title("A. THE PICTURE — one border row and one border column.\n"
                "Dotted = unbordered. Green = the object has finite norm there.",
                fontsize=10)
    a.legend(fontsize=8, loc="upper left")
    a.grid(alpha=0.3, which="both")

    # ---- B: the two Fredholm sides ---------------------------------------
    b = ax[0, 1]
    fs = d["T5_fredholm"]
    ss = np.linspace(-0.2, 2.0, 400)
    b.axvspan(-0.2, 1.0, color=C["good"], alpha=0.10)
    b.axvspan(1.0, 2.0, color=C["bad"], alpha=0.10)
    b.axvline(1.0, color="k", lw=1.6)
    b.axvspan(-0.2, alpha, color=C["anchor"], alpha=0.16)
    # the measured unbordered divergence exponent, and the bordered one
    xs = [0.0 if r["class"] == "flat" else r["param"] for r in lad]
    b.plot(xs, [r["unbordered_shape"]["exponent"] for r in lad], "s--",
           color=C["grey"], label="unbordered divergence exponent (leg 51's curve)")
    b.plot(xs, [r["analytic_shape"]["exponent"] for r in lad], "o-",
           color=C["ours"], lw=2.2, label="BORDERED divergence exponent")
    b.axhline(0, color=C["good"], lw=1.2, ls=":")
    b.set_xlim(-0.2, 2.0)
    b.set_xlabel("weight exponent  s   in   $w_k=(1+k)^s$")
    b.set_ylabel("fitted exponent of the growth in M")
    b.set_title(f"B. WHY THE MINIMUM WAS A TRAP.  kernel ~ "
                f"$m^{{{fs['kernel_exponent']:.2f}}}$ (in the space iff s<1);\n"
                f"cokernel ~ $m^{{{fs['cokernel_exponent']:+.2f}}}$ (bounded iff s$\\geq$1)."
                f"  Blue band: object admissible.", fontsize=10)
    b.legend(fontsize=8, loc="upper center")
    b.grid(alpha=0.3)
    b.annotate("both, marginally\n→ irreparable", xy=(1.0, 0.38),
               xytext=(1.28, 0.85), fontsize=8.5, color=C["bad"],
               arrowprops=dict(arrowstyle="->", color=C["bad"], lw=1.2))

    # ---- C: the analytic border vs the best one that exists --------------
    c = ax[0, 2]
    names = [label(r) for r in lad]
    xn = np.arange(len(lad))
    c.bar(xn - 0.2, [r["svd"][-1] for r in lad], 0.4, color=C["grey"],
          label="SVD pair (the optimal 1-D bordering)")
    c.bar(xn + 0.2, [r["analytic"][-1] for r in lad], 0.4, color=C["ours"],
          label="analytic far-field mode (what a proof can write)")
    for i, r in enumerate(lad):
        c.text(i, max(r["svd"][-1], r["analytic"][-1]) + 0.8,
               f"×{r['analytic'][-1] / r['svd'][-1]:.3f}", ha="center", fontsize=8.5)
    c.set_xticks(xn)
    c.set_xticklabels([n + ("\n(admissible)" if r["object_has_finite_norm"] else "")
                       for n, r in zip(names, lad)], fontsize=9)
    for t, r in zip(c.get_xticklabels(), lad):
        if r["object_has_finite_norm"]:
            t.set_color(C["good"])
    c.set_ylabel(r"$\|B^{-1}\|_w$ at M = 3136")
    c.set_title("C. THE BORDER A CERTIFICATE CAN WRITE DOWN\n"
                "achieves the optimum to three digits — where it matters.", fontsize=10)
    c.legend(fontsize=8, loc="upper left")
    c.grid(alpha=0.3, axis="y")

    # ---- D: alignment ----------------------------------------------------
    e = ax[1, 0]
    for r in lad:
        adm = r["object_has_finite_norm"]
        e.semilogx(r["M"], r["alignment"], "-o", ms=4.5,
                   color=C["good"] if adm else C["bad"],
                   lw=2.4 if adm else 1.4, label=label(r))
    e.axhline(1.0, color="k", lw=1.0, ls=":")
    e.set_ylim(0.86, 1.02)
    e.set_xlabel("M")
    e.set_ylabel(r"$|\cos|$  (optimal direction, analytic far field)")
    e.set_title("D. THE ALIGNMENT IS THE PHYSICS.\n"
                "It converges to 1 where the repair works and flatlines at 0.90 where "
                "it does not.", fontsize=10)
    e.legend(fontsize=8, loc="lower right")
    e.grid(alpha=0.3, which="both")

    # ---- E: the negative controls ----------------------------------------
    g = ax[1, 1]
    r0 = lad[0]
    g.loglog(r0["M"], r0["analytic"], "-o", color=C["good"], lw=2.4,
             ms=5, label="analytic border  → SATURATES")
    g.loglog(r0["M"], r0["unbordered"], ":", color=C["grey"], lw=1.8,
             label="no border")
    g.loglog(r0["M"], r0["second"], "-^", color=C["warn"], lw=1.6, ms=5,
             label="CONTROL: second singular pair")
    g.loglog(r0["M"], r0["random"], "-v", color=C["bad"], lw=1.6, ms=5,
             label="CONTROL: random pair")
    g.set_xlabel("M")
    g.set_ylabel(r"$\|B^{-1}\|_w$   (flat class)")
    g.set_title("E. BORDERING CAN ALSO FAIL, WHICH IS WHY THIS IS A MEASUREMENT.\n"
                f"The wrong direction lands on {r0['second'][-1]:.2f} — exactly the "
                "unbordered value.", fontsize=10)
    g.legend(fontsize=8, loc="upper left")
    g.grid(alpha=0.3, which="both")

    # ---- F: the ceiling --------------------------------------------------
    f = ax[1, 2]
    f.axis("off")
    adm = [r for r in lad if r["object_has_finite_norm"]]
    txt = (
        "WHAT THIS LEG ESTABLISHES\n"
        f"  the tail term is BOUNDED in M under one border row\n"
        f"  and one border column, in the classes where the\n"
        f"  target profile also has finite norm (s < alpha = {alpha}):\n"
        + "".join(f"      {label(r):>8s}   {r['analytic'][-1]:6.2f}   "
                 f"(unbordered {r['unbordered'][-1]:6.2f})\n" for r in adm) +
        "\n  and the window leg 51 measured EMPTY by 0.606 in\n"
        "  exponent units is no longer empty.\n\n"
        "WHY IT IS BELIEVABLE\n"
        "  * the failing side was PREDICTED before the ladders\n"
        "    ran, from the Fredholm structure alone, and held;\n"
        "  * the analytic border matches the optimal one to\n"
        f"    {max(x['ratio_last'] for x in d['T2_analytic_vs_svd'][:2]):.3f}x;\n"
        "  * both negative controls keep diverging.\n\n"
        "THE CEILING (pre-committed, clause T6)\n"
        "  A BOUNDED BORDERED TAIL IS NOT A CERTIFICATE.\n"
        "  The border is a NEW UNKNOWN -- the far-field\n"
        "  amplitude. It needs its own column in the finite\n"
        "  block, its own contribution to Y_0, and a matching\n"
        "  condition to the asymptotic expansion. None of that\n"
        "  is written here.\n\n"
        "  The object is still the a = 0 CLM linearisation:\n"
        "  one mode, analytic. A SUCCESS there bounds the real\n"
        "  target FROM BELOW, exactly as leg 51's failure did.\n"
        "  Nothing is claimed about HL_S2_nonsymmetric.\n\n"
        "  NO LINK OF THE L1->L4 CHAIN MOVED.  Clay ~0.05%."
    )
    f.text(0.02, 1.0, txt, va="top", ha="left", fontsize=8.4, family="monospace")
    f.set_title("F. the ceiling, pre-committed before the numbers", fontsize=10)

    fig.suptitle("Route-T v1 — bordering the tail with the far field it cannot invert: "
                 "the repair works exactly where the failure curve looked worst",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig47_route_t_v1_border.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
