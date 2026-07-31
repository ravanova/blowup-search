"""Phase-2 P2 Route-D v9 (fig27) evidence: the sharpness leg -- a better |H(h)|
bound, the payer rule it exposes, and where the remaining slack actually is.

By v8 the ledger had seven of ten constants bounded and Z2 complete, so the
question changed from coverage to sharpness: the budget goes like 1/(||A|| C_Q),
and ||A||'s bracket was ~70x wide.  This leg rebuilds the input that dominates
||A|| -- the pointwise bound on |H(h)| -- with exact kernels, and then measures
which input is worth attacking next.  Level-1 tooling + upper bounds, NOT a
certificate; Clay odds unchanged.

Rebuilds fig27 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v9_evidence.py
Regenerate the underlying data (deterministic; ~25 min):
    .venv/bin/python experiments/p2_route_d_v9_sharpen.py

Six panels (fig27):
  A. THE SHARPER BOUND (Y1).  Ratio to v6's bound across eight decades of X:
     0.09 near the origin, 0.65-0.87 through the middle, approaching 1 far out.
     The folded kernel 2 sin(th)/(cos phi - cos th) has the far-field decay
     built in and integrates to zero, so the principal value needs no band, no
     matching scale and no remainder -- v6 needed all three, each with a crude
     constant.
  B. THE PAYER RULE (Y2).  ||A|| against rho, the parameter that says which part
     of the norm pays for each point of the integral.  Every rho is valid; the
     neutral rho = 1 is WORSE than the crude bound it replaces, and the optimum
     at rho ~ 6-9 is 32% better.  C_Q, consuming the same bound where the ratio
     T/S is O(1) rather than ~10, wants a different rho.
  C. THE GAIN DOES NOT TRANSFER (Y2b).  32% at the reference (1.5, 0.5), 11% at
     (1.4, 0.35), 3% at (1.4, 0.25) and ~0% at (1.4, 0.15) -- which is where the
     map's optimum actually sits.  The mechanism is the interpolation exponent:
     T <= C(gamma) (P/2)^gamma (2S)^{1-gamma}, and the |H| bound enters ONLY
     through P, so at gamma = 0.15 a 30% sharpening of P moves T by 4%.
  D. THE COMPLETE Z2 MAP (Y4), re-sharpened.  The optimum stays at (1.4, 0.15)
     for the third leg running.
  E. THE BUDGET (Y5), five legs.  7.6e-2 -> 1.18e-2 -> 2.58e-4 -> 2.39e-4 ->
     2.40e-4: the order-of-magnitude losses stopped two legs ago, and this leg's
     sharpening does not move it either -- for the reason panel C gives.
  F. THE SENSITIVITY (Y6), at both points.  d log||A||/d log C_sup = +0.98 at
     the reference and +1.00 at the operating point -- proportional -- against
     +0.46 and +0.11 for the |H| input this leg just sharpened.  C_sup, v6's
     two-point dual, is the dominant input by an order of magnitude in
     elasticity, and the rest of the bracket cannot be attributed at all until
     there is a better LOWER bound.
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
JSON = DATA / "p2_route_d_v9_sharpen.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "alt": "#7b3294"}


def build_figure():
    d = json.loads(JSON.read_text())
    y1, y2, y3 = d["y1_bound"], d["y2_payer"], d["y3_operator"]
    y4, y5, y6 = d["y4_map"], d["y5_budget"], d["y6_sensitivity"]

    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.4))

    # -- A: sharper than v6 ---------------------------------------------
    a = ax[0, 0]
    X = [r["X"] for r in y1["pointwise_ratio"]]
    a.semilogx(X, [r["ratio"] for r in y1["pointwise_ratio"]], "o-",
               color=C["good"], lw=2.2)
    a.axhline(1.0, color=C["bad"], ls="--", lw=1.5, label="v6's bound")
    a.set_ylim(0, 1.1)
    a.set_xlabel("X")
    a.set_ylabel("new bound / v6's bound")
    a.set_title("A. the exact folded kernel is sharper everywhere\n"
                "(no band, no matching scale, no remainder term)", fontsize=10)
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    # -- B: the payer rule ----------------------------------------------
    b = ax[0, 1]
    rho = [r["rho"] for r in y2["rows"]]
    b.semilogx(rho, [r["A_upper"] for r in y2["rows"]], "o-", color=C["good"],
               lw=2.2, label="||A|| (upper bound)")
    b.axhline(y2["v6_A_upper"], color=C["bad"], ls="--", lw=1.6,
              label="v7/v8 as banked (%.1f)" % y2["v6_A_upper"])
    bA = y2["argmin_A"]
    b.plot([bA["rho"]], [bA["A_upper"]], "*", ms=17, color=C["anchor"],
           zorder=5, label="optimum %.1f at rho=%.0f" % (bA["A_upper"], bA["rho"]))
    b2 = b.twinx()
    b2.semilogx(rho, [r["C_Q_full"] for r in y2["rows"]], "s--", color=C["alt"],
                lw=1.6, label="C_Q (right axis)")
    b2.set_ylabel("C_Q", color=C["alt"], fontsize=9)
    b.set_xlabel("rho  (the payer rule: seminorm pays iff rho c_T <= c_S)")
    b.set_ylabel("||A|| upper bound")
    b.set_title("B. every rho is VALID -- and the neutral one is worst\n"
                "(different consumers want different rho)", fontsize=10)
    h1, l1 = b.get_legend_handles_labels()
    h2, l2 = b2.get_legend_handles_labels()
    b.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="upper center")
    b.grid(alpha=0.3, which="both")

    # -- C: the gain does NOT transfer ----------------------------------
    c = ax[0, 2]
    gp = y2["gain_by_point"]
    lbl = ["(%.1f, %.2f)" % (r["alpha"], r["gamma"]) for r in gp]
    xs = np.arange(len(gp))
    c.bar(xs, [100.0 * r["gain"] for r in gp], color=C["good"], width=0.55)
    for i, r in enumerate(gp):
        c.text(i, 100.0 * r["gain"] + 0.8, "%.0f%%" % (100 * r["gain"]),
               ha="center", fontsize=9)
    c.axhline(0.0, color=C["grey"], lw=1.0)
    c.set_xticks(xs)
    c.set_xticklabels(lbl, fontsize=8)
    c.set_xlabel("(alpha, gamma)   -- rightmost is the map's optimum")
    c.set_ylabel("reduction in ||A|| from the new bound")
    L = y3["ladder"]
    c.set_title("C. THE GAIN DOES NOT TRANSFER\n"
                "(||A|| %.1f -> %.1f at the reference, but ~0 where it matters)"
                % (L[0]["A_upper_v7"], L[0]["A_upper_v9"]), fontsize=10)
    c.grid(alpha=0.3, axis="y")

    # -- D: the map -------------------------------------------------------
    dd = ax[1, 0]
    gam = [x["gamma"] for x in y4["map"][0]["row"]]
    for r in y4["map"]:
        if r["alpha"] not in (1.1, 1.2, 1.4, 1.6, 1.8):
            continue
        dd.plot(gam, [x["Z2"] for x in r["row"]], "o-", ms=4,
                label="alpha = %.1f" % r["alpha"])
    am = y4["argmin_Z2"]
    dd.plot([am["gamma"]], [am["Z2"]], "*", ms=17, color=C["bad"], zorder=5,
            label="optimum (%.1f, %.2f)" % (am["alpha"], am["gamma"]))
    dd.set_xlabel("gamma")
    dd.set_ylabel("Z2 = 2 ||A|| C_Q  (all upper bounds)")
    dd.set_yscale("log")
    dd.set_title("D. the complete Z2 map, re-sharpened\n"
                 "(same optimum for the third leg running)", fontsize=10)
    dd.legend(fontsize=7, ncol=2)
    dd.grid(alpha=0.3, which="both")

    # -- E: the budget ----------------------------------------------------
    e = ax[1, 1]
    hist = y5["history"]
    vals = [h["Y0_max"] for h in hist]
    e.plot(range(len(vals)), vals, "o-", color=C["anchor"], lw=2.4, ms=9)
    for i, (h, v) in enumerate(zip(hist, vals)):
        e.annotate("%.2e" % v, (i, v), textcoords="offset points",
                   xytext=(0, 11), ha="center", fontsize=8.5)
    e.axhline(1e-2, color=C["warn"], ls=":", lw=1.6,
              label="GA residual floor (~1e-2)")
    e.set_xticks(range(len(hist)))
    e.set_xticklabels([h["leg"] for h in hist])
    e.set_yscale("log")
    e.set_ylabel("conditional budget Y0_max")
    e.set_title("E. five legs of budget\n"
                "(the losses stopped; sharpening did not undo them)",
                fontsize=10)
    e.legend(fontsize=8)
    e.grid(alpha=0.3, which="both")

    # -- F: the sensitivity, at both points --------------------------------
    f = ax[1, 2]
    styles = [("-", C["bad"], C["good"]), ("--", "#e06666", "#7fbf7f")]
    for q, (ls, c1, c2) in zip(y6["points"], styles):
        tag = "(%.1f, %.2f)" % (q["alpha"], q["gamma"])
        sc = [r["scale"] for r in q["C_sup_rows"]]
        f.loglog(sc, [r["A_upper"] for r in q["C_sup_rows"]], "o" + ls, color=c1,
                 lw=2.2, label="%s  C_sup   (%+.2f)" % (tag, q["C_sup_elasticity"]))
        f.loglog(sc, [r["A_upper"] for r in q["hilbert_rows"]], "s" + ls,
                 color=c2, lw=2.0,
                 label="%s  |H| bound (%+.2f)" % (tag, q["hilbert_elasticity"]))
    f.axvline(1.0, color=C["grey"], ls=":", lw=1.2)
    f.set_xlabel("factor applied to the input")
    f.set_ylabel("||A|| upper bound")
    f.set_title("F. why: ||A|| is PROPORTIONAL to C_sup, and at the\n"
                "operating point barely sees the |H| bound (+0.11)", fontsize=10)
    f.legend(fontsize=7)
    f.grid(alpha=0.3, which="both")

    fig.suptitle("Route-D v9 -- the sharpness leg: a 32% sharper |H(h)| bound that "
                 "buys ~nothing where it matters, and the elasticity that says why "
                 "(Level-1 tooling + upper bounds, NOT a certificate)",
                 fontsize=12.5)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig27_route_d_v9_sharpen.png"
    fig.savefig(out, dpi=145)
    plt.close(fig)
    return out


def summary():
    d = json.loads(JSON.read_text())
    y1, y2, y3 = d["y1_bound"], d["y2_payer"], d["y3_operator"]
    print("Route-D v9 -- the sharpness leg")
    print("  Y1  pointwise bound / v6: %.3f - %.3f over eight decades of X"
          % (min(r["ratio"] for r in y1["pointwise_ratio"]),
             max(r["ratio"] for r in y1["pointwise_ratio"])))
    print("  Y2  ||A||: v7/v8 %.2f -> neutral rho=1 %.2f -> best %.2f at rho=%.0f"
          % (y2["v6_A_upper"], y2["neutral_A"], y2["argmin_A"]["A_upper"],
             y2["argmin_A"]["rho"]))
    print("  Y3  ||A|| <= %.2f, J^%+.4f" % (y3["ladder"][0]["A_upper_v9"],
                                            y3["A_growth_exponent"]))
    print("  Y4  Z2 optimum %.1f at (%.1f, %.2f)"
          % (d["y4_map"]["argmin_Z2"]["Z2"], d["y4_map"]["argmin_Z2"]["alpha"],
             d["y4_map"]["argmin_Z2"]["gamma"]))
    print("  Y5  budget %s"
          % " -> ".join("%.2e" % h["Y0_max"] for h in d["y5_budget"]["history"]))
    for q in d["y6_sensitivity"]["points"]:
        print("  Y6  (%.1f, %.2f): d log||A||/d log C_sup = %+.2f ; "
              "d log||A||/d log|H| = %+.2f"
              % (q["alpha"], q["gamma"], q["C_sup_elasticity"],
                 q["hilbert_elasticity"]))
    print("  Y2b gain: " + ", ".join(
        "(%.1f,%.2f) %.0f%%" % (r["alpha"], r["gamma"], 100 * r["gain"])
        for r in d["y2_payer"]["gain_by_point"]))


if __name__ == "__main__":
    out = build_figure()
    summary()
    print(f"\n[done] wrote {out.relative_to(ROOT)}")
