"""Phase-2 P2 Route-D v2 (fig20) evidence: the FLOAT DRESS REHEARSAL of the
Newton-Kantorovich bounds at the exact a=0 anchor.

The result is a NEGATIVE with a constructive tail: in the plain (unweighted)
Fourier/Wiener space the certification ball does NOT close -- and cannot, at any
truncation, under any gauge -- because the transport term c (1 + cos theta) d_theta
DEGENERATES at theta = +-pi (i.e. at X = infinity).  The same measurements then
identify the repair: the linearized inverse loses EXACTLY one power of decay, and
becomes uniformly bounded (||A|| = 3, flat in N) as soon as the codomain is graded
by one mode power.  Level-1 tooling + a structural scoping result -- NOT a
certificate, and Clay odds are unchanged.

Rebuilds fig20 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_dress_evidence.py
Regenerate the underlying data (deterministic; a few seconds):
    .venv/bin/python experiments/p2_route_d_dress.py

Four panels (fig20):
  A. THE LADDER (D1).  ||A_N||_1 (the ell^1 norm of the gauged finite-section
     inverse) grows like N^0.97 -- one lost power -- while sigma_min falls like
     1/N.  The operator is NOT boundedly invertible in this space, so no
     truncation can ever certify.  All three gauges lie on top of each other (D3),
     which EXONERATES open sub-task G: the gauge choice is not what blocks it.
  B. CAUSAL ISOLATION (D4).  Replace the transport symbol (1 + cos theta) by 1 and
     change nothing else: ||A_N||_1 flattens at exactly 4.0.  The far-field
     degeneracy at theta = +-pi is therefore the CAUSE, not merely the suspect --
     this is open sub-task R, promoted from footnote to blocker.
  C. THE NK BOUNDS (D2/D5).  Z1 (>= N+1 from the truncation coupling alone) never
     comes near the 1 it must beat, so the certification budget
     Y0_max = (1-Z0-Z1)^2/(4 Z2) is identically zero; and the far-field column
     weight -> 1 from BOTH tail models, so the marginality is not a modelling
     artifact.  No positive weight repairs it (D5, inset numbers).
  D. THE REPAIR (D6).  Mode-by-mode amplification ||A e_m||_1 ~ 2m (fitted on the
     interior window m <= N/8; the roll-over near m = N is the finite-section
     edge, where ||A e_N||_1 == 4 exactly at every N) -- exactly the
     one power of X-decay predicted by the far-field ODE -c h_X - h/X = g (mode m
     resolves X ~ m).  Grading the codomain by that one power makes ||A|| = 3.000,
     FLAT in N.  That asymmetric space pair is the specification for the next brick.
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
JSON = DATA / "p2_route_d_dress.json"

C = {"true": "#c1440e", "sur": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    rows = d["d1_d2_ladder"]
    sur = d["d4_surrogate_ladder"]
    graded = d["d6_graded"]
    N = np.array([r["N"] for r in rows], dtype=float)

    fig, ax = plt.subplots(2, 2, figsize=(13.0, 9.8))

    # -- Panel A: the ladder + gauge insensitivity ---------------------------
    axA = ax[0, 0]
    An = np.array([r["A_norm_ell1"] for r in rows])
    sig = np.array([r["sigma_min"] for r in rows])
    axA.loglog(N, An, "o-", color=C["true"], lw=2, ms=7,
               label=r"$\|A_N\|_{\ell^1}$  (finite-section inverse)")
    axA.loglog(N, An[0] * (N / N[0]), "--", color=C["grey"], lw=1.2,
               label="slope 1 (one lost power)")
    axA.loglog(N, sig, "s-", color=C["anchor"], lw=1.6, ms=5,
               label=r"$\sigma_{\min}$")
    for g, style in (("a0", "^"), ("a1", "v")):
        axA.loglog(N, d["d3_gauge_sensitivity"][g]["A_norm_ell1"], style,
                   color=C["warn"], ms=6, mfc="none",
                   label=f"gauge '{g}' (D3)")
    ge = d["d1_growth_exponents"]
    axA.set_xlabel("truncation N"); axA.set_ylabel("value")
    axA.set_title(f"A. The N-ladder: the inverse is UNBOUNDED\n"
                  r"$\|A_N\|_{\ell^1}\sim N^{%.2f}$, $\sigma_{\min}\sim N^{%.2f}$"
                  % (ge["A_norm_ell1"], ge["sigma_min"])
                  + "  -- identical for all 3 gauges", fontsize=10)
    axA.legend(fontsize=8, loc="center left"); axA.grid(alpha=0.3, which="both")

    # -- Panel B: causal isolation ------------------------------------------
    axB = ax[0, 1]
    Asur = np.array([r["A_norm_ell1"] for r in sur])
    axB.loglog(N, An, "o-", color=C["true"], lw=2, ms=7,
               label=r"true transport $c\,(1+\cos\theta)\,\partial_\theta$")
    axB.loglog(N, Asur, "s-", color=C["sur"], lw=2, ms=7,
               label=r"surrogate $c\,\partial_\theta$  (symbol $\equiv 1$)")
    axB.axhline(Asur[-1], color=C["sur"], ls=":", lw=1.2)
    axB.annotate(f"flat at {Asur[-1]:.1f}", xy=(N[-3], Asur[-1] * 1.25),
                 color=C["sur"], fontsize=9)
    axB.annotate(f"{An[-1]:.0f} at N={int(N[-1])}", xy=(N[-4], An[-1] * 0.45),
                 color=C["true"], fontsize=9)
    axB.set_xlabel("truncation N"); axB.set_ylabel(r"$\|A_N\|_{\ell^1}$")
    axB.set_title("B. Causal isolation: it IS the far-field degeneracy\n"
                  r"$1+\cos\theta$ vanishes at $\theta=\pm\pi$ ($X=\infty$); "
                  "remove it and the inverse is bounded", fontsize=10)
    axB.legend(fontsize=8.5, loc="upper left"); axB.grid(alpha=0.3, which="both")

    # -- Panel C: the NK bounds ---------------------------------------------
    axC = ax[1, 0]
    Z1 = np.array([r["Z1"] for r in rows])
    Z1ft = np.array([r["Z1_finite_tail_coupling"] for r in rows])
    Z2 = np.array([r["Z2"] for r in rows])
    axC.loglog(N, Z1, "o-", color=C["true"], lw=2, ms=6, label=r"$Z_1$ (total)")
    axC.loglog(N, Z1ft, "d--", color=C["warn"], lw=1.6, ms=6,
               label=r"$Z_1$ truncation coupling $= N+1$")
    axC.loglog(N, Z2, "s-", color=C["anchor"], lw=1.4, ms=5, label=r"$Z_2 = 2\|A\|$")
    axC.axhline(1.0, color="#c00", ls="--", lw=1.6,
                label=r"the bar: need $Z_0+Z_1 < 1$")
    ff = d["d5_far_field"]
    axC.text(0.03, 0.03,
             "far-field column weight $\\to$ 1 from BOTH tail models:\n"
             f"  k={ff['k'][-1]}: [{ff['z_transport_model'][-1]:.4f}, "
             f"{ff['z_exact_model'][-1]:.4f}]\n"
             "no positive weight beats 1 (best = 1.000000)",
             transform=axC.transAxes, fontsize=7.6, va="bottom",
             bbox=dict(boxstyle="round", fc="#f4f4f4", ec="#bbb"))
    axC.set_xlabel("truncation N"); axC.set_ylabel("bound")
    axC.set_title("C. The radii polynomial never closes\n"
                  r"$Y_0^{\max}=(1-Z_0-Z_1)^2/(4Z_2)\equiv 0$ at every $N$",
                  fontsize=10)
    axC.legend(fontsize=8, loc="upper left"); axC.grid(alpha=0.3, which="both")

    # -- Panel D: the decay-graded repair -----------------------------------
    axD = ax[1, 1]
    big = graded[-1]
    cols = np.array(big["col_l1"])
    m = np.arange(cols.size)
    axD.plot(m[1:], cols[1:], "-", color=C["true"], lw=1.8,
             label=r"$\|A e_m\|_{\ell^1}$ at $N=%d$" % big["N"])
    lin = big["amplification_slope"] * m[1:]
    axD.plot(m[1:], lin, "--", color=C["grey"], lw=1.3,
             label=r"fit $%.2f\,m$ on $m\leq N/8$ (one lost power)"
                   % big["amplification_slope"])
    axD.axvspan(1, big["amplification_window"][1], color=C["grey"], alpha=0.12,
                label="fit window (interior)")
    axD.set_ylim(0, max(cols.max(), lin.max()) * 1.08)
    axD.annotate("roll-over near $m\!=\!N$ is the\nfinite-section EDGE\n"
                 r"($\|Ae_N\|_{\ell^1}=4$ exactly)",
                 xy=(0.60, 0.86), xycoords="axes fraction", fontsize=7.2,
                 color=C["grey"], ha="left", va="top")
    axD.set_xlabel("codomain mode m   (resolves $X \\sim m$)")
    axD.set_ylabel(r"$\|A e_m\|_{\ell^1}$")
    axD.legend(fontsize=8, loc="upper left"); axD.grid(alpha=0.3)

    axD2 = axD.inset_axes([0.56, 0.12, 0.40, 0.36])
    P1 = [g["P1_graded_cod_to_l1_dom"] for g in graded]
    P3 = [g["P3_graded_to_graded"] for g in graded]
    axD2.loglog(N, P1, "o-", color=C["sur"], lw=1.8, ms=4, label="graded $\\to \\ell^1$")
    axD2.loglog(N, P3, "s-", color=C["true"], lw=1.2, ms=3.5, label="graded $\\to$ graded")
    axD2.set_title(r"$\|A\|$ in graded norms", fontsize=7.5)
    axD2.tick_params(labelsize=6.5)
    axD2.legend(fontsize=6, loc="upper left"); axD2.grid(alpha=0.3, which="both")
    axD.set_title(f"D. THE REPAIR: grade the codomain by one power\n"
                  r"$\|A\|_{\rm graded\to\ell^1} = %.3f$, FLAT in $N$ "
                  r"($\sim N^{%.2f}$)"
                  % (P1[-1], d["d6_growth_exponents"]["P1_graded_cod_to_l1_dom"]),
                  fontsize=10)

    fig.suptitle("P2 Route-D v2 -- float dress rehearsal of the NK bounds at the a=0 "
                 "anchor: an HONEST NEGATIVE with a constructive repair "
                 "(NOT a certificate)", fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.975])
    out = FIGS / "fig20_p2_route_d_dress.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"[fig] wrote {out.relative_to(ROOT)}")


def print_summary():
    d = json.loads(JSON.read_text())
    rows = d["d1_d2_ladder"]
    print("\nP2 Route-D v2 -- float dress rehearsal (a=0 anchor, plain float64)")
    print(f"  ladder N = {rows[0]['N']} .. {rows[-1]['N']}; "
          f"the ball CLOSES at NO N ({sum(r['closes'] for r in rows)}/{len(rows)})")
    ge = d["d1_growth_exponents"]
    print(f"  ||A_N||_1 ~ N^{ge['A_norm_ell1']:.2f} (UNBOUNDED); "
          f"sigma_min ~ N^{ge['sigma_min']:.2f}; cond ~ N^{ge['cond']:.2f}")
    print(f"  gauge-independent: "
          + ", ".join(f"{g}: N^{v['growth_exponent_A_norm']:.2f}"
                      for g, v in d["d3_gauge_sensitivity"].items())
          + "   -> sub-task G exonerated")
    print(f"  surrogate transport (symbol == 1): ||A|| flat at "
          f"{d['d4_surrogate_ladder'][-1]['A_norm_ell1']:.1f} "
          f"(N^{d['d4_growth_exponents']['A_norm_ell1']:.2f})"
          f"   -> sub-task R is the CAUSE")
    print(f"  Z1 >= N+1 from truncation coupling alone; Y0_max == 0 at every N")
    print(f"  REPAIR: ||A||_(graded->l1) = "
          f"{d['d6_graded'][-1]['P1_graded_cod_to_l1_dom']:.3f}, flat "
          f"(N^{d['d6_growth_exponents']['P1_graded_cod_to_l1_dom']:.2f}); "
          f"||A e_m||_1 ~ {d['d6_graded'][-1]['amplification_slope']:.2f} m")
    print("  Level-1 tooling + a structural negative. NOT a certificate. "
          "Clay odds unchanged (~0.05%).")


if __name__ == "__main__":
    build_figure()
    print_summary()
