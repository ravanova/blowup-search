"""Phase-2 P2 Route-D v6 (fig24) evidence: the first genuine UPPER bounds, and the
discrete-ball trap that invalidates the obvious route to them.

Five legs built the space and measured in it; every number was a family-restricted
LOWER bound, and Z1 was never bounded at all.  This leg produces the project's
first upper bounds -- and, on the way, shows that the natural way of computing
them is unsound.  Level-1 tooling + partial upper bounds, NOT a certificate; Clay
odds unchanged.

Rebuilds fig24 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v6_evidence.py
Regenerate the underlying data (deterministic; ~10 min):
    .venv/bin/python experiments/p2_route_d_v6_bounds.py

Four panels (fig24):
  A. THE DISCRETE-BALL TRAP (B1).  Duality over a DISCRETE Holder ball selects a
     grid-scale sign pattern as its extremizer.  That vector's interpolant has a
     continuum norm inflated by 3e3 (J=125) to 5e4 (J=500) -- growing like J^2 --
     while a smooth element of the same class stays faithful to 3%.  The "worst
     direction" is not in the true unit ball, so any unboundedness it reports is
     the instrument's, not the operator's.  Banked lesson (9) in mirror image.
  B. WHAT SURVIVES (B2).  A two-point dual bound built only from inequalities the
     CONTINUUM norm implies is valid.  On the domain SUP part it SATURATES
     (5.536 -> 5.631 over a 13x range in J, exponent +0.006) -- the project's
     first uniform upper bound on any part of ||A||.  On the domain SEMINORM part
     it is valid but lossy, growing like J^gamma.
  C. THE FAR-FIELD Z1 BOUND (B3/B4).  From the exact identity
     DF - L = h/(X(1+X^2)) - H(h)/(1+X^2) (relative error 1e-16) plus a
     Holder-paid bound on |H(h)|, a closed-form bound on the far-field part of Z1
     -- the first bounded piece of Z1 in six legs.  It decays like X0^{alpha-2}
     as predicted and dominates the measured value with 1.1-3.0x headroom.
  D. THE NEW ALPHA TENSION (B5).  Pricing Z1 moves the optimum.  v5's joint
     optimum alpha = 1.8 does NOT close at any X0 tested (Z1 = 2.3-4.3, far above
     the 1 it must beat); the conditional budget peaks at alpha ~ 1.2.
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
JSON = DATA / "p2_route_d_v6_bounds.json"

C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    nb, ff, ten = d["b1_b2_norms"], d["b4_far_field"], d["b5_tension"]

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 10.0))

    # -- A: the discrete-ball trap ------------------------------------------
    axA = ax[0, 0]
    Ji = np.array([x["J"] for x in nb["inflation"]], dtype=float)
    ex = np.array([x["extremizer"]["inflation"] for x in nb["inflation"]])
    sm = np.array([x["smooth_control"]["inflation"] for x in nb["inflation"]])
    axA.loglog(Ji, ex, "o-", color=C["bad"], lw=2, ms=8,
               label="dual extremizer (grid-scale sign pattern)")
    axA.loglog(Ji, ex[0] * (Ji / Ji[0]) ** 2, "--", color=C["grey"], lw=1.2,
               label=r"slope 2  ($\propto J^2$)")
    axA.loglog(Ji, sm, "s-", color=C["good"], lw=2, ms=8,
               label="smooth control (same decay class)")
    axA.axhline(1.0, color=C["good"], ls=":", lw=1.2)
    axA.set_xlabel("truncation J")
    axA.set_ylabel(r"$\|\cdot\|_{\rm continuum}\,/\,\|\cdot\|_{\rm discrete}$")
    axA.set_title("A. The discrete-ball trap\n"
                  r"the extremizer duality picks is inflated $\sim J^{%.2f}$ "
                  "-- it is not in the true ball"
                  % nb["inflation_growth_exponent"], fontsize=10)
    axA.legend(fontsize=8, loc="center left"); axA.grid(alpha=0.3, which="both")

    # -- B: what survives ----------------------------------------------------
    axB = ax[0, 1]
    lad = nb["ladder"]
    J = np.array([r["J"] for r in lad], dtype=float)
    sup = np.array([r["sup_part_upper"] for r in lad])
    semi = np.array([r["seminorm_part_upper"] for r in lad])
    fam = np.array([r["family_lower"] for r in lad])
    ok = np.isfinite(semi)
    axB.semilogx(J, sup, "o-", color=C["good"], lw=2.2, ms=8,
                 label=r"domain SUP part, upper bound $\;\sim J^{%+.3f}$"
                       % nb["sup_part_growth_exponent"])
    axB.semilogx(J[ok], semi[ok], "^-", color=C["bad"], lw=1.8, ms=7,
                 label=r"domain SEMINORM part, upper bound $\;\sim J^{%+.3f}$ (lossy)"
                       % nb["seminorm_part_growth_exponent"])
    axB.semilogx(J, fam, "s--", color=C["grey"], lw=1.5, ms=6,
                 label="v5 family-restricted LOWER bound")
    axB.annotate(f"{sup[0]:.3f} $\\to$ {sup[-1]:.3f}\nover a 13x range in $J$",
                 xy=(J[1], sup[1] + 3), fontsize=8.5, color=C["good"])
    axB.set_xlabel("truncation J"); axB.set_ylabel(r"contribution to $\|A\|$")
    axB.set_title("B. What survives: a dual built from continuum-valid inequalities\n"
                  "the sup part SATURATES -- the first uniform upper bound here",
                  fontsize=10)
    axB.legend(fontsize=8, loc="upper left"); axB.grid(alpha=0.3)

    # -- C: the far-field Z1 bound ------------------------------------------
    axC = ax[1, 0]
    for m in ff["map"]:
        if m["alpha"] not in (1.2, 1.5, 1.8):
            continue
        X0 = [r["X0"] for r in m["row"]]
        b = [r["bound"] for r in m["row"]]
        axC.loglog(X0, b, "o-", lw=2, ms=5,
                   label=r"$\alpha=%.1f$: $X_0^{%+.3f}$ (pred. $%+.1f$)"
                         % (m["alpha"], m["decay_exponent"],
                            m["predicted_exponent"]))
    v = ff["validation"]
    axC.loglog([c["X0"] for c in v], [c["measured"] for c in v], "kx", ms=10, mew=2,
               label="measured (resolved nodes)")
    axC.loglog([c["X0"] for c in v], [c["bound"] for c in v], "k+", ms=11, mew=2,
               label="bound at those $X_0$")
    axC.set_xlabel(r"far-field cut $X_0$")
    axC.set_ylabel(r"$\|DF-L\|_{X\to Y}$ on $\{X\geq X_0\}$")
    axC.set_title("C. The far-field part of $Z_1$, bounded in closed form\n"
                  r"exact identity $DF-L = h/(X(1{+}X^2)) - H(h)/(1{+}X^2)$"
                  " (rel. err 1e-16)", fontsize=10)
    axC.legend(fontsize=7.5, loc="lower left"); axC.grid(alpha=0.3, which="both")

    # -- D: the new alpha tension -------------------------------------------
    axD = ax[1, 1]
    al = np.array([r["alpha"] for r in ten["rows"]])
    styles = [("o-", C["bad"]), ("s-", C["warn"]), ("d-", C["anchor"])]
    for i, (mk, col) in enumerate(styles):
        X0 = ten["rows"][0]["by_X0"][i]["X0"]
        z1 = [r["by_X0"][i]["Z1_farfield"] for r in ten["rows"]]
        axD.semilogy(al, z1, mk, color=col, lw=1.8, ms=6,
                     label=r"$Z_1^{\rm far}$ at $X_0=%d$" % X0)
    axD.axhline(1.0, color="#c00", ls="--", lw=1.8, label=r"the bar: $Z_1 < 1$")
    axD.axvline(1.8, color=C["grey"], ls=":", lw=1.6)
    axD.annotate("v5's joint optimum $\\alpha=1.8$:\n$Z_1 = 2.3-4.3$, fails at every $X_0$",
                 xy=(1.79, 2.4), xytext=(1.30, 2.6), fontsize=8, color="#555555",
                 ha="left", va="center",
                 bbox=dict(boxstyle="round", fc="white", ec="#bbb", alpha=0.9),
                 arrowprops=dict(arrowstyle="->", color=C["grey"], lw=1.2))
    axD.set_xlabel(r"decay grading $\alpha$")
    axD.set_ylabel(r"$Z_1^{\rm far} = \|A\|\cdot\|DF-L\|$")
    axD.grid(alpha=0.3)

    axD2 = axD.twinx()
    y0 = [r["by_X0"][-1]["Y0_max"] for r in ten["rows"]]
    axD2.plot(al, y0, "-", color=C["good"], lw=2.4)
    axD2.fill_between(al, 0, y0, color=C["good"], alpha=0.13)
    axD2.set_ylabel(r"conditional budget $Y_0^{\max}$ at $X_0=3200$",
                    color=C["good"])
    axD2.tick_params(axis="y", labelcolor=C["good"])
    best = ten["argmax_alpha_by_X0"]["3200.0"]
    axD2.annotate(r"optimum moves to $\alpha\approx%.1f$" % best["alpha"] + "\n"
                  + r"$Y_0^{\max}=%.2e$" % best["Y0_max"],
                  xy=(best["alpha"], best["Y0_max"]), xytext=(1.24, 0.0045),
                  fontsize=8.5, color=C["good"],
                  arrowprops=dict(arrowstyle="->", color=C["good"], lw=1.2))
    axD.set_title(r"D. Pricing $Z_1$ moves the optimum"
                  "\nCONDITIONAL: far-field $Z_1$ only; three constants still open",
                  fontsize=10)
    axD.legend(fontsize=7.5, loc="upper left")

    fig.suptitle("P2 Route-D v6 -- the first genuine upper bounds, and the "
                 "discrete-ball trap (NOT a certificate)", fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.975])
    out = FIGS / "fig24_p2_route_d_v6.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"[fig] wrote {out.relative_to(ROOT)}")


def print_summary():
    d = json.loads(JSON.read_text())
    nb, ff, ten = d["b1_b2_norms"], d["b4_far_field"], d["b5_tension"]
    print("\nP2 Route-D v6 -- first genuine upper bounds (plain float64)")
    print(f"  B1 discrete-ball trap: dual extremizer inflated "
          f"{nb['inflation'][0]['extremizer']['inflation']:.1e} -> "
          f"{nb['inflation'][-1]['extremizer']['inflation']:.1e} "
          f"(~J^{nb['inflation_growth_exponent']:.2f}); smooth control "
          f"{nb['inflation'][-1]['smooth_control']['inflation']:.4f}")
    lad = nb["ladder"]
    print(f"  B2 ||A|| sup part: {lad[0]['sup_part_upper']:.3f} -> "
          f"{lad[-1]['sup_part_upper']:.3f} over J={lad[0]['J']}..{lad[-1]['J']} "
          f"(J^{nb['sup_part_growth_exponent']:+.3f}) -- SATURATES; "
          f"seminorm part J^{nb['seminorm_part_growth_exponent']:+.3f} (lossy)")
    print(f"  B4 far-field Z1 bound validated: "
          + ", ".join(f"X0={c['X0']:.0f} x{c['headroom']:.1f}"
                      for c in ff["validation"]))
    b = ten["argmax_alpha_by_X0"]["3200.0"]
    a18 = [r for r in ten["rows"] if r["alpha"] == 1.8][0]
    print(f"  B5 v5's alpha=1.8 gives Z1 = "
          + "/".join(f"{x['Z1_farfield']:.2f}" for x in a18["by_X0"])
          + f" (all > 1, no closure); optimum moves to alpha={b['alpha']:.1f}, "
          f"conditional Y0max = {b['Y0_max']:.2e}")
    print("  Three of eight NK constants moved from MEASURED to BOUNDED; three "
          "remain open. NOT a certificate. Clay odds unchanged (~0.05%).")


if __name__ == "__main__":
    build_figure()
    print_summary()
