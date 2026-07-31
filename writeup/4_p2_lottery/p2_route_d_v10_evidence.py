"""Phase-2 P2 Route-D v10 (fig28) evidence: a LOWER bound on ||A|| worth reading.

v9 ended by admitting that every bracket this project quotes has a lower end
that is a maximum over sign patterns -- nearly meaningless -- so "the bound is
50x too big" and "the operator really is that large" could not be told apart,
while implying opposite decisions about the lane.  This leg builds the adversary
and reads the answer.  Level-1 tooling + bounds, NOT a certificate; Clay odds
unchanged.

Rebuilds fig28 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v10_evidence.py
Regenerate the underlying data (deterministic; ~20 min):
    .venv/bin/python experiments/p2_route_d_v10_lower.py

Six panels (fig28):
  A. THE LOWER BOUND vs the sign-pattern baseline over J (W1).  The baseline
     DEGRADES with J -- it was never measuring the operator, it was measuring how
     badly a grid-scale sign pattern is punished by a Holder seminorm.
  B. THE BRACKET AT THE REFERENCE POINT (W1): 50x -> 16x.
  C. THE BRACKET AT THE OPERATING POINT (W2), which is the one that matters:
     2.74 <= ||A|| <= 20.94, a factor of 7.7.
  D. WHAT THE EXTREMIZER IS (W3): a wide, far-field-supported, slowly varying
     shape -- the opposite of a sign pattern, and consistent with everything this
     project has learned about where the difficulty lives.
  E. THE BRACKET ACROSS THE MAP (W4): 8x-16x everywhere, tightest at the optimum.
  F. THE VERDICT (W5).  A perfect upper bound on ||A|| would move the budget from
     2.45e-4 to 1.9e-3 and no further -- the first MEASURED ceiling on what
     sharpening can buy.  Still ~5x below the GA residual floor, not 40x.
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
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_route_d_v10_lower.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "alt": "#7b3294"}


def build_figure():
    d = json.loads(JSON.read_text())
    w1, w2, w3 = d["w1_ladder"], d["w2_operating"], d["w3_shape"]
    w4, w5 = d["w4_map"], d["w5_verdict"]
    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.4))

    a = ax[0, 0]
    L = w1["ladder"]
    Js = [r["J"] for r in L]
    a.plot(Js, [r["lower"] for r in L], "o-", color=C["good"], lw=2.4,
           label="smooth adversary family (NEW)")
    a.plot(Js, [r["sign_patterns"] for r in L], "s--", color=C["bad"], lw=2.0,
           label="sign patterns (every earlier leg)")
    a.set_xscale("log")
    a.set_xlabel("J")
    a.set_ylabel("lower bound on ||A||")
    a.set_title("A. the old baseline was not measuring the operator\n"
                "(it degrades with J; the new family is stable)", fontsize=10)
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    b = ax[0, 1]
    b.plot(Js, [r["bracket_old"] for r in L], "s--", color=C["bad"], lw=2.0,
           label="with sign patterns")
    b.plot(Js, [r["bracket"] for r in L], "o-", color=C["good"], lw=2.4,
           label="with the adversary family")
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlabel("J")
    b.set_ylabel("upper / lower")
    b.set_title("B. the bracket at the reference point (1.5, 0.5)\n"
                "%.0fx -> %.0fx" % (L[1]["bracket_old"], L[1]["bracket"]),
                fontsize=10)
    b.legend(fontsize=8)
    b.grid(alpha=0.3, which="both")

    c = ax[0, 2]
    O = w2["ladder"]
    Jo = [r["J"] for r in O]
    c.fill_between(Jo, [r["lower"] for r in O], [r["upper"] for r in O],
                   color=C["anchor"], alpha=0.18)
    c.plot(Jo, [r["upper"] for r in O], "o-", color=C["anchor"], lw=2.2,
           label="upper bound")
    c.plot(Jo, [r["lower"] for r in O], "o-", color=C["good"], lw=2.2,
           label="lower bound (adversary)")
    c.plot(Jo, [r["sign_patterns"] for r in O], "s--", color=C["bad"], lw=1.6,
           label="lower bound (sign patterns)")
    c.set_xscale("log")
    c.set_yscale("log")
    c.set_xlabel("J")
    c.set_ylabel("||A||")
    c.set_title("C. THE BRACKET THAT MATTERS -- at the operating\n"
                "point (%.1f, %.2f): %.2f <= ||A|| <= %.1f, a factor %.1f"
                % (w2["alpha"], w2["gamma"], O[-1]["lower"], O[-1]["upper"],
                   O[-1]["bracket"]), fontsize=10)
    c.legend(fontsize=7.5)
    c.grid(alpha=0.3, which="both")

    dd = ax[1, 0]
    th = np.array(w3["theta"])
    dd.plot(th, np.array(w3["g"]), color=C["good"], lw=2.2,
            label="the extremizer g (x codomain weight)")
    dd.plot(th, np.array(w3["image"]) / max(1e-30,
            np.max(np.abs(w3["image"]))), color=C["anchor"], lw=1.8, ls="--",
            label="its image A g (x domain weight, scaled)")
    dd.axvline(np.pi, color=C["grey"], ls=":", lw=1.2)
    dd.set_xlabel("theta   (pi = the far field, X = infinity)")
    dd.set_title("D. the extremizer is a WIDE FAR-FIELD shape\n"
                 "(%s) -- the opposite of a sign pattern"
                 % w3["top"][0]["name"], fontsize=10)
    dd.legend(fontsize=7.5)
    dd.grid(alpha=0.3)

    e = ax[1, 1]
    rows = w4["rows"]
    lbl = ["(%.1f,%.2f)" % (r["alpha"], r["gamma"]) for r in rows]
    xs = np.arange(len(rows))
    e.bar(xs - 0.2, [r["bracket"] for r in rows], width=0.4, color=C["good"],
          label="with the adversary family")
    e.bar(xs + 0.2, [r["upper"] / r["sign_patterns"] for r in rows], width=0.4,
          color=C["bad"], label="with sign patterns")
    e.set_xticks(xs)
    e.set_xticklabels(lbl, fontsize=8, rotation=20)
    e.set_yscale("log")
    e.set_ylabel("bracket width (upper / lower)")
    e.set_title("E. across the map: 8x-16x everywhere\n"
                "(tightest at the optimum, leftmost pair)", fontsize=10)
    e.legend(fontsize=8)
    e.grid(alpha=0.3, axis="y", which="both")

    f = ax[1, 2]
    vals = [w5["Y0_now"], w5["Y0_if_A_were_sharp"], w5["GA_residual_floor"]]
    names = ["budget now", "if ||A|| were\nSHARP", "GA residual\nfloor"]
    f.bar(names, vals, color=[C["anchor"], C["good"], C["warn"]], width=0.55)
    for i, v in enumerate(vals):
        f.text(i, v * 1.15, "%.1e" % v, ha="center", fontsize=10)
    f.set_yscale("log")
    f.set_ylabel("conditional budget Y0_max")
    f.set_title("F. THE MEASURED CEILING on sharpening ||A||\n"
                "(%.1fx, and it lands ~5x short of the floor)"
                % (w5["Y0_if_A_were_sharp"] / w5["Y0_now"]), fontsize=10)
    f.grid(alpha=0.3, axis="y", which="both")

    fig.suptitle("Route-D v10 -- a lower bound on ||A|| worth reading: the "
                 "bracket falls 50x -> 8x, and for the first time the project "
                 "can say what sharpening could buy "
                 "(Level-1 tooling + bounds, NOT a certificate)", fontsize=12.5)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig28_route_d_v10_lower.png"
    fig.savefig(out, dpi=145)
    plt.close(fig)
    return out


def summary():
    d = json.loads(JSON.read_text())
    r = d["w1_ladder"]["ladder"][1]
    o = d["w2_operating"]["ladder"][-1]
    v = d["w5_verdict"]
    print("Route-D v10 -- a lower bound worth reading")
    print("  W1  reference: sign patterns %.3f -> adversary %.3f; bracket "
          "%.0fx -> %.0fx" % (r["sign_patterns"], r["lower"], r["bracket_old"],
                              r["bracket"]))
    print("  W2  OPERATING point: %.2f <= ||A|| <= %.2f (%.1fx)"
          % (o["lower"], o["upper"], o["bracket"]))
    print("  W3  extremizer: %s" % d["w3_shape"]["top"][0]["name"])
    print("  W5  budget %.2e; ceiling if ||A|| were sharp %.2e; GA floor %.0e"
          % (v["Y0_now"], v["Y0_if_A_were_sharp"], v["GA_residual_floor"]))


if __name__ == "__main__":
    out = build_figure()
    summary()
    print(f"\n[done] wrote {out.relative_to(ROOT)}")
