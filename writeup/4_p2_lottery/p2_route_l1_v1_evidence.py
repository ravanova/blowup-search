"""Phase-2 Route-L1 v1 (fig45): the certificate stops being a rehearsal.

Every Y0, Z1, Z2 this project had printed was float64. This leg wires the interval layer
through the bordered residual and computes them as rigorous upper bounds. The radii
polynomial CLOSES at all three rungs on the named target — and the thing that decided it
was not the mathematics but the arithmetic of evaluating a residual that cancels to
5.7e-15 out of terms of size 0.03.

Rebuild fig45 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_l1_v1_evidence.py
Regenerate the data (deterministic, ~12 s):
    .venv/bin/python -u experiments/p2_route_l1_v1_interval.py

Six panels: A the enclosure widths against an exact rational reference; B THE PICTURE —
the two evaluation paths across the resolution ladder, one closing and one not; C the
rigorous constants against their float readings; D the poisoned iterate; E the
known-answer object through the same pipe; F what is certified and what is not.
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
JSON = DATA / "p2_route_l1_v1_interval.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ours": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    ref, lad, nai = d["L1_1_exact_reference"], d["L1_2_ladder"], d["L1_3_naive_path"]
    poison, known = d["L1_4_poison"], d["L1_5_known_answer"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: enclosure widths, checked against exact rationals ------------
    a = ax[0, 0]
    ops = [c["operator"] for c in ref["checks"]]
    xn = np.arange(len(ops))
    a.bar(xn - 0.2, [c["naive_width_max"] for c in ref["checks"]], 0.4,
          color=C["bad"], alpha=0.85, label="naive interval matvec")
    a.bar(xn + 0.2, [c["tight_width_max"] for c in ref["checks"]], 0.4,
          color=C["good"], alpha=0.85, label="compensated (dot2)")
    a.set_yscale("log")
    a.set_xticks(xn)
    a.set_xticklabels(ops)
    a.set_ylabel("max enclosure width")
    for i, c in enumerate(ref["checks"]):
        a.text(i, c["naive_width_max"] * 1.6, f"{c['tightening']:.0f}x",
               ha="center", fontsize=8)
    a.set_ylim(top=6e-11)
    a.legend(fontsize=8, loc="lower left")
    a.set_title("A. every enclosure contains the EXACT rational answer\n"
                "(fractions.Fraction, no floating point) — and one is 10^4 tighter",
                fontsize=10)
    a.grid(alpha=0.3, axis="y")

    # ---- B: THE PICTURE — two paths across the ladder --------------------
    b = ax[0, 1]
    ns = [r["n"] for r in lad]
    yb = [r["verdict"]["Y0_over_budget"] for r in lad]
    yn = [r["verdict"]["Y0_over_budget"] for r in nai]
    yf = [r["float"]["Y0_over_budget"] for r in lad]
    b.plot(ns, yn, "s--", color=C["bad"], label="rigorous, naive evaluation")
    b.plot(ns, yb, "o-", color=C["good"], lw=2, label="rigorous, compensated")
    b.plot(ns, yf, "^:", color=C["grey"], label="float rehearsal (not a bound)")
    b.axhline(1.0, color="k", lw=1.5)
    b.text(ns[0], 1.35, "certificate closes below this line", fontsize=8)
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlabel("resolution $n$")
    b.set_ylabel(r"$Y_0$ / budget")
    b.set_title("B. the same certificate, the same object:\n"
                "the arithmetic decides whether it exists", fontsize=10)
    b.legend(fontsize=8)
    b.grid(alpha=0.3, which="both")

    # ---- C: the constants, rigorous vs float ------------------------------
    c = ax[0, 2]
    labs = [r"$Y_0$", r"$Z_1$"]
    wid = [[r["widening_Y0"] for r in lad], [r["widening_Z1"] for r in lad]]
    xn = np.arange(len(ns))
    c.bar(xn - 0.2, wid[0], 0.4, color=C["ours"], alpha=0.85, label=r"$Y_0$ widening")
    c.bar(xn + 0.2, wid[1], 0.4, color=C["anchor"], alpha=0.85, label=r"$Z_1$ widening")
    c.set_yscale("log")
    c.axhline(1.0, color="k", lw=1)
    c.set_xticks(xn)
    c.set_xticklabels([f"n={n}" for n in ns])
    c.set_ylabel("rigorous / float  ($\\times$)")
    c.legend(fontsize=8)
    c.set_title("C. what rigour costs, per constant\n"
                "the price is paid in $Z_1$, and it is affordable", fontsize=10)
    c.grid(alpha=0.3, axis="y")

    # ---- D: the poisoned iterate ------------------------------------------
    dd = ax[1, 0]
    eps = [p["eps"] for p in poison]
    yov = [p["Y0_over_budget"] for p in poison]
    cols = [C["good"] if p["closes"] else C["bad"] for p in poison]
    dd.bar(range(len(eps)), yov, color=cols, alpha=0.85)
    dd.axhline(1.0, color="k", lw=1.5)
    dd.set_yscale("log")
    dd.set_xticks(range(len(eps)))
    dd.set_xticklabels([f"{e:.0e}" for e in eps])
    dd.set_xlabel("perturbation of the iterate")
    dd.set_ylabel(r"$Y_0$ / budget")
    dd.set_title("D. it rejects a wrong point\n"
                 f"(the certified ball has radius {lad[0]['verdict']['r_max']:.1e})",
                 fontsize=10)
    dd.grid(alpha=0.3, axis="y")

    # ---- E: the known-answer object ---------------------------------------
    e = ax[1, 1]
    kn = [r["n"] for r in known]
    ky = [r["Y0_over_budget"] for r in known]
    kf = [r["float_Y0_over_budget"] for r in known]
    xn = np.arange(len(kn))
    e.bar(xn - 0.2, kf, 0.4, color=C["grey"], alpha=0.85, label="float")
    e.bar(xn + 0.2, ky, 0.4, color=[C["good"] if r["closes"] else C["bad"] for r in known],
          alpha=0.85, label="rigorous")
    e.axhline(1.0, color="k", lw=1.5)
    e.set_yscale("log")
    e.set_xticks(xn)
    e.set_xticklabels([f"CLM n={n}" for n in kn])
    e.set_ylabel(r"$Y_0$ / budget")
    e.legend(fontsize=8)
    e.set_title("E. the known-answer object, same pipe\n"
                "closes at 201, fails at 401 — as leg 49 measured in float", fontsize=10)
    e.grid(alpha=0.3, axis="y")

    # ---- F: what is certified, and what is not ----------------------------
    f = ax[1, 2]
    f.axis("off")
    r0 = lad[0]["verdict"]
    txt = (
        "WHAT CLOSES\n"
        f"  a zero of the FINITE-DIMENSIONAL system\n"
        f"  built from the stored H, D, Uop, on |X| <= {lad[0]['X_max']:.0f}\n"
        f"  within r in [{r0['r_min']:.2e}, {r0['r_max']:.2e}]\n"
        f"  of the stored iterate, weighted sup norm\n\n"
        "WHAT IS NOT BOUNDED HERE\n"
        "  * consistency of (H, D) with the continuum operators\n"
        "  * the far field beyond X_max — leg 46 measured the\n"
        "    truncation gap at 1.55e+08 ball radii, and leg 47\n"
        "    measured that reach makes it WORSE\n\n"
        "SO: step one of L1, not L1. The object still has\n"
        "no proof of any kind, and this is not one yet."
    )
    f.text(0.02, 0.97, txt, va="top", ha="left", fontsize=9.5, family="monospace")
    f.set_title("F. the ceiling, pre-committed before the numbers", fontsize=10)

    fig.suptitle("Route-L1 v1 — the certificate constants become BOUNDS: the radii "
                 "polynomial closes in interval arithmetic on the truncated discrete system",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    out = FIGS / "fig45_route_l1_v1_interval.png"
    fig.savefig(out, dpi=150)
    print(f"wrote {out}")


if __name__ == "__main__":
    build_figure()
