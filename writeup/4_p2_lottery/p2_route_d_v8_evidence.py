"""Phase-2 P2 Route-D v8 (fig26) evidence: the codomain seminorm part of C_Q,
and the first Newton-Kantorovich Z2 in this project with nothing omitted.

v7 closed the domain seminorm part of ||A|| and produced the first (alpha,gamma)
map made entirely of upper bounds -- with one term still missing, and it flagged
the omission as the reason its optimum's LOCATION was provisional.  This leg
bounds that term.  The weight it needs is the leg's first surprise (1 - gamma,
not alpha - gamma: H does not inherit h's decay), and the size of the correction
is its second: after three legs in which honesty cost an order of magnitude
apiece, this one costs 7%.  Level-1 tooling + upper bounds, NOT a certificate;
Clay odds unchanged.

Rebuilds fig26 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v8_evidence.py
Regenerate the underlying data (deterministic; ~12 min):
    .venv/bin/python experiments/p2_route_d_v8_quadratic.py

Six panels (fig26):
  A. THE ESTIMATE CONVERGES (X1).  The pair supremum on four grid levels and the
     quadrature on five: both flat to ~4e-4.  A grid supremum can only
     UNDER-report -- the mirror of v6's discrete-ball trap -- so this is part of
     the measurement, not a nicety.
  B. THE ROUTE ABLATION (X1).  With only the pointwise route (all v6 and v7 had
     for this quantity) the same sweep returns a number 237x larger.  Almost all
     of the constant is the increment estimate; the bookkeeping is the small part.
  C. THE BRACKET (X2).  The bound against the measured weighted seminorm of H(h)
     over ten profiles including v4's square-wave adversary: ratio ~0.22-0.25, so
     the estimate is honest and ~4x lossy -- the same order of slack v7 carried.
  D. THE gamma STRUCTURE (X3).  The new term rises at both ends (1/gamma near,
     1/(1-gamma) far) and so does C_Q_full -- but so did v6's sup-only C_Q at the
     small-gamma end, for the same near-region reason.  The RATIO of the two is
     therefore flat at small gamma and grows toward gamma = 1: the opposite of
     what v7 predicted.
  E. THE COMPLETE Z2 MAP (X4).  Every constant an upper bound, nothing omitted.
     The optimum stays at (1.4, 0.15) and Z2 rises 242 -> 261.
  F. THE BUDGET HISTORY (X5).  7.6e-2 -> 1.18e-2 -> 2.58e-4 -> 2.39e-4.  Three
     order-of-magnitude losses, then one that is not: the trend that made the
     lane look doomed does not continue through this leg.
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
JSON = DATA / "p2_route_d_v8_quadratic.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "alt": "#7b3294"}


def build_figure():
    d = json.loads(JSON.read_text())
    x1, x2, x3 = d["x1_estimate"], d["x2_bracket"], d["x3_gamma"]
    x4, x5 = d["x4_map"], d["x5_budget"]

    fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.4))

    # -- A: the two convergences ----------------------------------------
    a = ax[0, 0]
    npairs = [r["n_theta"] * r["n_d"] for r in x1["grid_ladder"]]
    a.plot(npairs, [r["b_semi"] for r in x1["grid_ladder"]], "o-",
           color=C["good"], lw=2.2, label="b_semi (pair-grid refinement)")
    a.plot(npairs, [r["b_sup"] for r in x1["grid_ladder"]], "s-",
           color=C["anchor"], lw=2.0, label="b_sup  (pair-grid refinement)")
    a2 = a.twiny()
    a2.plot([r["n_quad"] for r in x1["quad_ladder"]],
            [r["b_semi_at_reference_pair"] for r in x1["quad_ladder"]],
            "^--", color=C["warn"], label="one pair, quadrature refinement")
    a2.set_xscale("log")
    a2.set_xlabel("quadrature points per piece", fontsize=8, color=C["warn"])
    a.set_xscale("log")
    a.set_xlabel("pairs swept (n_theta x n_d)")
    a.set_ylabel("coefficient in T_psi <= b_sup S + b_semi T")
    a.set_title("A. both discretizations are converged\n"
                "(a grid supremum can only UNDER-report -- so this is a gate)",
                fontsize=10)
    h1, l1 = a.get_legend_handles_labels()
    h2, l2 = a2.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="center right")
    a.grid(alpha=0.3, which="both")

    # -- B: the route ablation ------------------------------------------
    b = ax[0, 1]
    ab = x1["ablation"]
    bars = [ab["increment_rule"], ab["pointwise_only"]]
    b.bar(["increment estimate\n(this leg)", "pointwise only\n(v6 / v7)"], bars,
          color=[C["good"], C["bad"]], width=0.55)
    b.set_yscale("log")
    b.set_ylabel("b_sup + b_semi")
    for i, v in enumerate(bars):
        b.text(i, v * 1.15, "%.1f" % v, ha="center", fontsize=10)
    b.set_title("B. the estimate IS the result\n"
                "(the only route available before this leg is %.0fx worse)"
                % ab["gain"], fontsize=10)
    b.grid(alpha=0.3, axis="y", which="both")

    # -- C: the bracket --------------------------------------------------
    c = ax[0, 2]
    row = x2["rows"][0]
    names = list(row["per_profile"].keys())
    xs = np.arange(len(names))
    for k, r in enumerate(x2["rows"]):
        c.plot(xs, [r["per_profile"][n] for n in names], "o-", ms=4,
               color=[C["anchor"], C["good"], C["warn"], C["alt"]][k % 4],
               label="alpha=%.1f, gamma=%.2f" % (r["alpha"], r["gamma"]))
    c.axhline(1.0, color=C["bad"], lw=1.6, ls="--", label="the bound (= 1)")
    c.set_xticks(xs)
    c.set_xticklabels(names, rotation=60, ha="right", fontsize=6.5)
    c.set_ylim(0, 1.15)
    c.set_ylabel("measured / bound")
    c.set_title("C. the bracket: valid on every profile,\n"
                "and ~4x lossy (worst ratio %.2f)"
                % max(r["worst_ratio"] for r in x2["rows"]), fontsize=10)
    c.legend(fontsize=7)
    c.grid(alpha=0.3)

    # -- D: the gamma structure ------------------------------------------
    dd = ax[1, 0]
    g = [r["gamma"] for r in x3["rows"]]
    dd.plot(g, [r["b_semi"] for r in x3["rows"]], "o-", color=C["alt"], lw=2.0,
            label="b_semi (NEW term's coefficient)")
    dd.plot(g, [r["C_Q_full"] for r in x3["rows"]], "s-", color=C["good"],
            lw=2.2, label="C_Q complete (this leg)")
    dd.plot(g, [r["C_Q_sup_only_v6"] for r in x3["rows"]], "^--",
            color=C["grey"], lw=1.8, label="C_Q sup part only (v6/v7)")
    dd.set_xlabel("gamma  (alpha = %.1f)" % x3["alpha"])
    dd.set_ylabel("constant")
    dd.set_yscale("log")
    dd.set_title("D. both ends rise -- but so did the OLD term\n"
                 "(C_Q_full bowls at gamma=%.2f; the ratio grows toward 1)"
                 % x3["argmin_C_Q_full"]["gamma"], fontsize=10)
    dd.legend(fontsize=7.5)
    dd.grid(alpha=0.3, which="both")

    # -- E: the complete Z2 map -------------------------------------------
    e = ax[1, 1]
    gam = [x["gamma"] for x in x4["map"][0]["row"]]
    for r in x4["map"]:
        if r["alpha"] not in (1.1, 1.2, 1.4, 1.6, 1.8):
            continue
        e.plot(gam, [x["Z2_full"] for x in r["row"]], "o-", ms=4,
               label="alpha = %.1f" % r["alpha"])
    e.plot(gam, [x["Z2_v7"] for x in x4["map"][3]["row"]], "k--", lw=1.2,
           label="alpha = 1.4, v7 (incomplete)")
    am = x4["argmin_Z2_full"]
    e.plot([am["gamma"]], [am["Z2"]], "*", ms=17, color=C["bad"], zorder=5,
           label="optimum (%.1f, %.2f)" % (am["alpha"], am["gamma"]))
    e.set_xlabel("gamma")
    e.set_ylabel("Z2 = 2 ||A|| C_Q   (all upper bounds)")
    e.set_yscale("log")
    e.set_title("E. the first COMPLETE Z2 map\n"
                "(nothing omitted; the optimum does not move)", fontsize=10)
    e.legend(fontsize=7, ncol=2)
    e.grid(alpha=0.3, which="both")

    # -- F: the budget history ---------------------------------------------
    f = ax[1, 2]
    hist = x5["history"]
    labels = [h["leg"] for h in hist]
    vals = [h["Y0_max"] for h in hist]
    f.plot(range(len(vals)), vals, "o-", color=C["anchor"], lw=2.4, ms=9)
    for i, (lab, v) in enumerate(zip(labels, vals)):
        f.annotate("%.2e" % v, (i, v), textcoords="offset points",
                   xytext=(0, 11), ha="center", fontsize=8.5)
    f.axhline(1e-2, color=C["warn"], ls=":", lw=1.6,
              label="GA residual floor (~1e-2)")
    f.set_xticks(range(len(labels)))
    f.set_xticklabels(labels)
    f.set_yscale("log")
    f.set_ylabel("conditional budget Y0_max")
    f.set_title("F. three order-of-magnitude losses, then one that is not\n"
                "(the last unpriced term costs %.0f%%, not 10x)"
                % (100.0 * (x5["cost_of_the_new_term"]["at_the_optimum"] - 1.0)),
                fontsize=10)
    f.legend(fontsize=8)
    f.grid(alpha=0.3, which="both")

    fig.suptitle("Route-D v8 -- the codomain seminorm part of C_Q: the last "
                 "unpriced constant, and the first complete Z2 "
                 "(Level-1 tooling + upper bounds, NOT a certificate)",
                 fontsize=12.5)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig26_route_d_v8_quadratic.png"
    fig.savefig(out, dpi=145)
    plt.close(fig)
    return out


def summary():
    d = json.loads(JSON.read_text())
    x1, x5 = d["x1_estimate"], d["x5_budget"]
    print("Route-D v8 -- the codomain seminorm part of C_Q")
    print("  X1  b = (%.4f, %.4f); decomposition exact to %.1e; pointwise-only "
          "control %.0fx worse" % (x1["reference"]["b_sup"],
                                   x1["reference"]["b_semi"],
                                   x1["decomposition_max_error"],
                                   x1["ablation"]["gain"]))
    print("  X2  worst measured/bound ratio %.3f (valid, ~4x lossy)"
          % max(r["worst_ratio"] for r in d["x2_bracket"]["rows"]))
    print("  X3  C_Q complete bowls: %.3f at gamma = %.2f"
          % (d["x3_gamma"]["argmin_C_Q_full"]["C_Q_full"],
             d["x3_gamma"]["argmin_C_Q_full"]["gamma"]))
    am, av = d["x4_map"]["argmin_Z2_full"], d["x4_map"]["argmin_Z2_v7_reproduced"]
    print("  X4  complete Z2 %.1f at (%.1f, %.2f); v7's incomplete map said %.1f "
          "at (%.1f, %.2f) -- same location"
          % (am["Z2"], am["alpha"], am["gamma"], av["Z2"], av["alpha"],
             av["gamma"]))
    print("  X5  budget %s"
          % " -> ".join("%.2e" % h["Y0_max"] for h in x5["history"]))
    print("  X6  ledger: %d of %d bounded"
          % (sum("BOUNDED" in r["status"] or r["status"] == "EXACT"
                 for r in d["x6_ledger"]), len(d["x6_ledger"])))


if __name__ == "__main__":
    out = build_figure()
    summary()
    print(f"\n[done] wrote {out.relative_to(ROOT)}")
