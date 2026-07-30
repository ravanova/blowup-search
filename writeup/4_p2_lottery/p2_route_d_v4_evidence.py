"""Phase-2 P2 Route-D v4 (fig22) evidence: the FULL operator in the decay-graded
pair -- v3's far-field estimate confirmed, and the OTHER half of the space found.

Route-D v3 (fig21) closed the weighted-ell^1 category with a conservation law and
identified decay-graded spaces as the replacement, pricing them on a far-field
MODEL operator.  This leg carries the same measurements to the full gauged
operator, in a third independent discretization (nodal spectral collocation with
weighted sup norms; v1/v2/v3 were all coefficient-space).

Two results, one good and one not:
  * v3's far-field law predicts the FULL inverse norm to within 6% on the useful
    window, and the optimum survives -- the core adds almost nothing.
  * but the decay-graded SUP pair does not control the QUADRATIC, because the
    Hilbert transform is unbounded on L^infinity.  A decay grading alone is not a
    certificate space; a smoothness component is also required.

Level-1 tooling + scoping.  NOT a certificate.  Clay odds unchanged (~0.05%).

Rebuilds fig22 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v4_evidence.py
Regenerate the underlying data (deterministic; ~10 min):
    .venv/bin/python experiments/p2_route_d_v4_graded.py

Four panels (fig22):
  A. THE THIRD BUILD (W1).  ||A|| on a grid ladder, ungraded vs graded, in a
     discretization sharing no code path with v2/v3.  The ungraded norm keeps
     climbing (logarithmically here, linearly in v2's ell^1 build -- different
     norm, milder divergence, same verdict); the graded one settles.
  B. THE CORE COSTS ALMOST NOTHING (W2).  ||A|| against the decay class alpha,
     against v3's far-field law 2/|alpha-2|.  They agree to ~6% across
     alpha = 1.4..1.7, and the full operator has its own interior minimum at
     alpha ~ 1.40: the far-field price rises toward the resonance at alpha = 2,
     the core price rises toward alpha = 1.
  C. THE MISSING HALF (W3).  On the conjugate-extremal family -- the Fourier
     partial sums of a square wave, bounded but with a logarithmically divergent
     conjugate -- the quadratic constant grows without bound.  Random
     perturbations of the same degree do the opposite, which is the methodological
     point: sampling cannot demonstrate unboundedness, only a construction can.
  D. THE PRICE, CONFIRMED (W4).  Z2 and the budget ceiling against alpha, v4
     against v3's far-field-only estimate.  The estimate stands.  The ceiling is
     ~2e-2 and it is a CEILING: Z1 = 0 is assumed and the smoothness component of
     the norm is unpriced.
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
JSON = DATA / "p2_route_d_v4_graded.json"

C = {"grad": "#c1440e", "flat": "#1f4e79", "far": "#888888", "sur": "#2e7d32",
     "warn": "#e08a1e", "v3": "#6a1b9a"}


def build_figure():
    d = json.loads(JSON.read_text())
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.9))

    # -- Panel A: the third build ------------------------------------------
    axA = ax[0, 0]
    w1 = d["w1_reproduction"]
    J = np.array([r["J"] for r in w1["rows"]], float)
    fl = np.array([r["A_norm_ungraded"] for r in w1["rows"]])
    gr = np.array([r["A_norm_graded"] for r in w1["rows"]])
    axA.semilogx(J, fl, "o-", color=C["flat"], lw=2, ms=7,
                 label=r"ungraded ($\alpha=0$): keeps climbing")
    axA.semilogx(J, gr, "s-", color=C["grad"], lw=2, ms=7,
                 label=r"decay-graded ($\alpha=3/2$): settles")
    axA.annotate(f"{fl[0]:.1f} $\\to$ {fl[-1]:.1f}\n(+{np.diff(fl).mean():.2f} per "
                 "doubling)", xy=(J[-2], fl[-2] * 0.93), color=C["flat"], fontsize=8.5,
                 ha="right", va="top")
    axA.annotate(f"{gr[0]:.2f} $\\to$ {gr[-1]:.2f}\n(increments halving)",
                 xy=(J[1], gr[1] + 1.6), color=C["grad"], fontsize=8.5)
    axA.set_xlabel("collocation points J   (far field reaches $X\\sim 4J/\\pi$)")
    axA.set_ylabel(r"$\|A\|_{Y\to X}$")
    axA.set_title("A. Third independent build, same verdict\n"
                  r"ungraded $\sim J^{%.2f}$, graded $\sim J^{%.3f}$"
                  % (w1["growth_exponent_ungraded"], w1["growth_exponent_graded"]),
                  fontsize=10)
    axA.legend(fontsize=8.5, loc="center left"); axA.grid(alpha=0.3, which="both")
    axA.set_ylim(0, max(fl) * 1.15)

    # -- Panel B: the core costs almost nothing -----------------------------
    axB = ax[0, 1]
    w2 = d["w2_resonance"]["rows"]
    al = np.array([r["alpha"] for r in w2])
    An = np.array([r["A_norm"] for r in w2])
    ff = np.array([r["farfield_model_law"] for r in w2])
    axB.plot(al, An, "o-", color=C["grad"], lw=2.2, ms=7,
             label=r"FULL gauged operator $\|A\|$ (this leg)")
    axB.plot(al, ff, "--", color=C["v3"], lw=1.8,
             label=r"v3 far-field model law $2/|\alpha-2|$")
    k = int(np.argmin(An))
    axB.plot([al[k]], [An[k]], "*", color="#c00", ms=16, zorder=5)
    axB.annotate(r"interior minimum $\alpha\approx%.2f$" % al[k],
                 xy=(al[k], An[k]), xytext=(al[k] - 0.36, An[k] - 1.4),
                 fontsize=9, color="#c00")
    good = (al >= 1.4) & (al <= 1.7)
    axB.axvspan(1.4, 1.7, color=C["sur"], alpha=0.10)
    axB.text(1.55, 16.5, "far-field law within\n%.0f%% of the full operator"
             % (100 * np.max(np.abs(An[good] - ff[good]) / An[good])),
             color=C["sur"], fontsize=8.5, ha="center")
    axB.set_yscale("log")
    axB.set_xlabel(r"decay class $\alpha$   ($|h|\lesssim X^{-\alpha}$)")
    axB.set_ylabel(r"$\|A\|_{Y\to X}$")
    axB.set_title("B. The compact core adds almost nothing\n"
                  "the far-field price rises toward the $\\alpha=2$ resonance, "
                  "the core price toward $\\alpha=1$", fontsize=9.8)
    axB.legend(fontsize=8.5, loc="upper left"); axB.grid(alpha=0.3, which="both")

    # -- Panel C: the missing half ------------------------------------------
    axC = ax[1, 0]
    w3 = d["w3_quadratic"]
    deg = np.array(w3[0]["degrees"], float)
    for r, col_, lab in ((w3[0], "#8c6d1f", r"$\alpha=%.2f$" % w3[0]["alpha"]),
                         (w3[5], C["grad"], r"$\alpha=%.2f$" % w3[5]["alpha"]),
                         (w3[-1], C["flat"], r"$\alpha=%.2f$" % w3[-1]["alpha"])):
        axC.semilogx(deg, r["C_Q_per_degree"], "o-", color=col_, lw=2, ms=6,
                     label=lab + " (conjugate-extremal)")
    axC.semilogx(deg, w3[5]["C_Q_per_degree_random"], "^--", color=C["sur"], lw=1.6,
                 ms=6, label=r"$\alpha=1.50$ RANDOM control (falls)")
    axC.set_xlabel("degree m of the perturbation")
    axC.set_ylabel(r"quadratic constant $\|Q(h)\|_Y/\|h\|_X^2$")
    axC.set_title("C. The decay grading does NOT control the quadratic\n"
                  r"$H$ is unbounded on $L^\infty$: $C_Q$ grows like $\log m$ "
                  "(+%.2f per e-fold)" % w3[5]["C_Q_log_slope"], fontsize=9.8)
    axC.legend(fontsize=8, loc="upper left"); axC.grid(alpha=0.3, which="both")
    axC.text(0.97, 0.04, "sampling cannot demonstrate unboundedness --\n"
                         "only the construction can",
             transform=axC.transAxes, fontsize=7.8, ha="right", va="bottom",
             color=C["sur"], bbox=dict(boxstyle="round", fc="#f4f4f4", ec="#bbb"))

    # -- Panel D: the price, confirmed --------------------------------------
    axD = ax[1, 1]
    w4 = d["w4_budget"]["rows"]
    a4 = np.array([r["alpha"] for r in w4])
    Z2 = np.array([r["Z2"] for r in w4])
    Z2v3 = np.array([r["v3_farfield_only_Z2"] for r in w4])
    bud = np.array([r["budget_ceiling"] for r in w4])
    axD.plot(a4, Z2, "o-", color=C["grad"], lw=2.2, ms=7,
             label=r"$Z_2$, full operator (this leg)")
    axD.plot(a4, Z2v3, "--", color=C["v3"], lw=1.8,
             label=r"$Z_2$, v3 far-field-only estimate")
    axD.set_yscale("log")
    axD.set_xlabel(r"decay class $\alpha$")
    axD.set_ylabel(r"$Z_2 = 2\|A\|\,C_Q$")
    axD.grid(alpha=0.3, which="both")
    axD.legend(fontsize=8.5, loc="upper center")
    axD2 = axD.twinx()
    axD2.plot(a4, bud, "d:", color=C["warn"], lw=1.8, ms=6)
    axD2.set_ylabel(r"budget CEILING $1/(4Z_2)$", color=C["warn"])
    axD2.tick_params(axis="y", labelcolor=C["warn"])
    kb = int(np.argmax(bud))
    axD2.axvline(a4[kb], color=C["warn"], ls=":", lw=1.4)
    axD2.annotate(r"$\alpha^\ast=%.2f$, ceiling $%.1e$" % (a4[kb], bud[kb]),
                  xy=(a4[kb], bud[kb]), xytext=(1.52, bud[kb] * 0.55),
                  fontsize=8.5, color=C["warn"])
    axD.set_title("D. v3's estimate stands -- and the ceiling is thin\n"
                  r"$Z_2^{\min}=%.1f$; a CEILING: $Z_1=0$ assumed, smoothness "
                  "component unpriced" % Z2.min(), fontsize=9.8)

    fig.suptitle("P2 Route-D v4 -- the full gauged operator in the decay-graded pair:\n"
                 "the far-field price is confirmed; the space is still missing half "
                 "its structure  (NOT a certificate)", fontsize=11.5, y=0.997)
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    out = FIGS / "fig22_p2_route_d_v4_graded.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"[fig] wrote {out.relative_to(ROOT)}")


def print_summary():
    d = json.loads(JSON.read_text())
    w1, w2 = d["w1_reproduction"], d["w2_resonance"]["rows"]
    w3, w4, w5 = d["w3_quadratic"], d["w4_budget"], d["w5_robustness"]
    print("\nP2 Route-D v4 -- the full operator in the decay-graded pair "
          "(a=0 anchor, plain float64)")
    print(f"  W1 third independent build: ungraded ||A|| ~ J^"
          f"{w1['growth_exponent_ungraded']:.2f} (keeps climbing), graded ~ J^"
          f"{w1['growth_exponent_graded']:.3f} (settles at "
          f"{w1['rows'][-1]['A_norm_graded']:.3f})")
    good = [r for r in w2 if 1.4 <= r["alpha"] <= 1.7]
    err = max(abs(r["core_excess"]) / r["A_norm"] for r in good)
    print(f"  W2 v3's far-field law predicts the FULL inverse norm to "
          f"{100 * err:.1f}% on alpha in [1.4, 1.7]; the full ||A|| has its own "
          f"interior minimum at alpha = {w4['argmin_alpha_of_A_norm']:.2f}")
    r15 = w3[5]
    print(f"  W3 the decay-graded SUP pair does NOT control the quadratic: on the "
          f"conjugate-extremal family C_Q grows +{r15['C_Q_log_slope']:.2f} per "
          f"e-fold of degree ({r15['C_Q_per_degree'][0]:.2f} -> "
          f"{r15['C_Q_per_degree'][-1]:.2f} over m={r15['degrees'][0]}.."
          f"{r15['degrees'][-1]}), while random perturbations FALL")
    print(f"     -> the certificate space needs a smoothness component too "
          f"(H is unbounded on L^inf)")
    print(f"  W4 Z2_min = {w4['best_Z2']:.1f} at alpha = {w4['argmax_alpha']:.2f}; "
          f"budget CEILING {w4['best_budget_ceiling']:.2e} (v3 predicted alpha 1.44, "
          f"Z2 13.3)")
    print(f"  W5 the gauge must replace a CORE equation: spread over core rows "
          f"{w5['spread_core_rows_only']:.2f}x, but replacing a far-field row gives "
          f"{max(r['A_norm'] for r in w5['rows']):.1e}")
    print("  Level-1 tooling + scoping. NOT a certificate; Z1 is quantified but not "
          "bounded. Clay odds unchanged (~0.05%).")


if __name__ == "__main__":
    build_figure()
    print_summary()
