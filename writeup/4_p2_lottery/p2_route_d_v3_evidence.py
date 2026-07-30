"""Phase-2 P2 Route-D v3 (fig21) evidence: WHICH SPACE PAIR CAN CARRY THE
CERTIFICATE -- a no-go theorem for the whole weighted-ell^1 category, and the
decay-graded pair that replaces it.

Route-D v2 (fig20) ended by proposing a repair: the gauged inverse loses exactly
one power of decay, so grade the codomain by one mode power and ||A|| goes flat at
3.000.  The condition attached to that proposal was that the quadratic term
2 h H(h) must land in the SAME graded codomain.  It cannot: measured over the
whole two-parameter family of diagonal weights, the two requirements are disjoint
by exactly one grading power.  The escape is a pair that is not a weighted-ell^1
pair at all -- decay-graded spaces -- where both hold, at a price with an interior
optimum.  Level-1 tooling + a structural scoping result; NOT a certificate, and
Clay odds are unchanged.

Rebuilds fig21 from committed data WITHOUT re-derivation:
    .venv/bin/python writeup/4_p2_lottery/p2_route_d_v3_evidence.py
Regenerate the underlying data (deterministic; ~1 minute):
    .venv/bin/python experiments/p2_route_d_v3_spaces.py

Four panels (fig21):
  A. THE CONSERVATION LAW (S3).  With domain weight (1+k)^s and codomain weight
     (1+m)^t, both requirements depend only on the GAP g = t - s, and the two
     growth exponents are exact complements: ||A|| grows like N^{1-g} and the
     sharp quadratic constant like K^{g}.  A certificate needs BOTH to be zero;
     their sum is >= 1 everywhere (= 1 on 0 <= g <= 1).  The one power the far
     field loses has to be paid by one bound or the other, and the choice of
     weights only decides WHICH.
  B. THE TWO REGIONS (S3/S4).  The same statement in the (s,t) plane: a bounded
     inverse needs t >= s+1, a bounded quadratic needs t <= s, and the strip
     between them is empty.  The CONTROL -- transport symbol (1+cos) -> 1, nothing
     else changed -- moves the inverse boundary to t >= s-1, i.e. down by exactly
     TWO powers, which is the order to which 1+cos(theta) vanishes at theta = pi.
     A non-degenerate first-order transport GAINS a power; this one loses one; the
     difference of 2 is the degeneracy, measured.  With the control the regions
     overlap on a full unit strip, so the obstruction is the far-field
     degeneracy, not the method.
  C. THE RESONANCE (S5).  In decay-graded sup norms the far-field inverse has norm
     exactly 2/|alpha-2| (measured against a second-order discretization to 0.0%,
     and against the operator-side coefficient c*alpha-1).  The pole sits at
     alpha = 2 because X^{-2} is simultaneously the homogeneous far-field solution
     at c = 1/2 AND the decay of the anchor Omega_2 = -1/(1+X^2).  v2's "loses one
     power" is this resonance seen at integer grading.
  D. THE PRICE (S6).  Detuning to alpha = 2 - eps buys a bounded far-field inverse
     at cost 2/eps, while the quadratic gains one power with constant
     (int f_alpha)/pi, which blows up as alpha -> 1.  The product has an interior
     optimum near alpha ~ 1.44 -- the design parameter for any Route-D v3 build.
     SCOPING ESTIMATE ONLY: leading-order far-field constants, no compact core,
     plain float64, nothing interval-enclosed.
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
JSON = DATA / "p2_route_d_v3_spaces.json"

C = {"inv": "#c1440e", "quad": "#1f4e79", "sur": "#2e7d32", "sum": "#6a1b9a",
     "warn": "#e08a1e", "grey": "#888888"}


def build_figure():
    d = json.loads(JSON.read_text())
    st = d["s3_st_map"]
    gz = st["gap_sweep"][0]
    g = np.array(gz["g"])

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.9))

    # -- Panel A: the conservation law --------------------------------------
    axA = ax[0, 0]
    eA = np.array(gz["A_exponent"])
    eQ = np.array(gz["algebra_exponent"])
    eS = np.array(gz["exponent_sum"])
    axA.plot(g, eA, "o-", color=C["inv"], lw=2, ms=5,
             label=r"$\|A_N\|_{Y\to X}$ growth exponent  ($\to N^{1-g}$)")
    axA.plot(g, eQ, "s-", color=C["quad"], lw=2, ms=5,
             label=r"sharp quadratic constant $S_K$ exponent  ($\to K^{g}$)")
    axA.plot(g, eS, "-", color=C["sum"], lw=2.6,
             label=r"their SUM  $\geq 1$ everywhere")
    axA.plot(g, np.array(gz["A_surrogate_exponent"]), "^--", color=C["sur"],
             lw=1.5, ms=5, label="control: transport symbol $\\equiv 1$")
    axA.axhline(0.0, color="#c00", ls="--", lw=1.6)
    axA.text(-1.72, 0.12, "a certificate needs BOTH exponents here", color="#c00",
             fontsize=8)
    axA.axhspan(-0.06, 0.06, color="#c00", alpha=0.07)
    axA.set_xlabel(r"grading gap $g = t - s$   (codomain power minus domain power)")
    axA.set_ylabel("growth exponent (0 = bounded)")
    axA.set_title("A. The conservation law: the lost power must be paid\n"
                  r"min over ALL diagonal weight pairs of the sum $= %.2f$ "
                  r"(control: %.2f)"
                  % (gz["min_exponent_sum"], gz["min_exponent_sum_surrogate"]),
                  fontsize=10)
    axA.legend(fontsize=8, loc="upper right"); axA.grid(alpha=0.3)
    axA.set_ylim(-0.2, 3.4)
    axA.axvspan(-1.0, 0.0, color=C["sur"], alpha=0.07)
    axA.text(-0.5, 2.15, "control admits\nthis whole strip", color=C["sur"],
             fontsize=8, ha="center")

    # -- Panel B: the two regions in the (s,t) plane -------------------------
    axB = ax[0, 1]
    s_grid = np.array(st["s_grid"])
    axB.fill_between(s_grid, s_grid + 1.0, 3.4, color=C["inv"], alpha=0.16)
    axB.fill_between(s_grid, -1.6, s_grid, color=C["quad"], alpha=0.16)
    axB.fill_between(s_grid, s_grid, s_grid + 1.0, color="#c00", alpha=0.09,
                     hatch="//", edgecolor="#c00", lw=0.0)
    axB.plot(s_grid, s_grid + 1.0, "-", color=C["inv"], lw=2.4,
             label=r"$\|A\|$ bounded: $t \geq s+1$  (measured)")
    axB.plot(s_grid, s_grid, "-", color=C["quad"], lw=2.4,
             label=r"quadratic bounded: $t \leq s$  (measured)")
    bI = [r["t_min_bounded"] for r in st["region_I_boundary"]]
    bII = [r["t_max_algebra"] for r in st["region_II_boundary"]]
    axB.plot(s_grid, bI, "o", color=C["inv"], ms=7, mfc="none", mew=1.6,
             label="scan: first bounded $t$ (0.25 grid)")
    axB.plot(s_grid, bII, "s", color=C["quad"], ms=6, mfc="none", mew=1.6,
             label="scan: last bounded $t$")
    sur_b = [r["t_min_bounded"] for r in d["s4_surrogate_control"]["region_I_boundary"]]
    axB.plot(s_grid, sur_b, "^--", color=C["sur"], lw=1.8, ms=7,
             label="CONTROL (symbol $\\equiv 1$): boundary falls to $t = s-1$")
    axB.fill_between(s_grid, s_grid - 1.0, s_grid, color=C["sur"], alpha=0.13)
    axB.text(0.85, 1.37, "EMPTY\n(gap = 1 power)", color="#c00", fontsize=10,
             ha="center", va="center", rotation=45, fontweight="bold")
    axB.set_xlabel(r"domain weight power $s$   ($u_k = (1+k)^s$)")
    axB.set_ylabel(r"codomain weight power $t$   ($v_m = (1+m)^t$)")
    axB.set_xlim(0, 2.0); axB.set_ylim(-1.4, 3.2)
    axB.set_title("B. No weighted-$\\ell^1$ pair works -- and the control says why\n"
                  "removing the degeneracy moves the boundary down by TWO powers "
                  "(its order of vanishing)", fontsize=9.6)
    axB.legend(fontsize=7.6, loc="upper left"); axB.grid(alpha=0.3)

    # -- Panel C: the far-field resonance -----------------------------------
    axC = ax[1, 0]
    rows = d["s5_resonance"]["inverse_side"]
    al = np.array([r["alpha"] for r in rows])
    nm = np.array([r["inverse_norm_measured"] for r in rows])
    fine = np.linspace(1.02, 3.0, 400)
    fine = fine[np.abs(fine - 2.0) > 0.03]
    axC.plot(fine, 2.0 / np.abs(fine - 2.0), "-", color=C["grey"], lw=1.6,
             label=r"law $2/|\alpha-2|$ (exact ODE)")
    axC.plot(al, nm, "o", color=C["inv"], ms=7,
             label=r"measured $\|L^{-1}\|$ (2nd-order discretization)")
    axC.axvline(2.0, color="#c00", ls="--", lw=1.8)
    axC.annotate("RESONANCE at $\\alpha=2$:\n$X^{-2}$ is the homogeneous\n"
                 "solution at $c=1/2$ AND\nthe decay of the anchor",
                 xy=(2.0, 30), xytext=(2.25, 33), fontsize=8, color="#c00",
                 ha="left", va="top")
    axC.axvspan(1.0, 2.0, color=C["sur"], alpha=0.07)
    axC.text(1.5, 1.6, "admissible window", color=C["sur"], fontsize=8, ha="center")
    worst = max(r["rel_err_vs_finite_domain_law"] for r in rows)
    axC.set_yscale("log")
    axC.set_xlabel(r"decay class $\alpha$   ($|h| \lesssim X^{-\alpha}$)")
    axC.set_ylabel(r"$\|L^{-1}\|_{Y\to X}$")
    axC.set_title("C. The far field is resonant at the anchor's own decay rate\n"
                  r"measured vs exact ODE norm: max relative error %.3f%% over 15 values"
                  % (100 * worst), fontsize=10)
    axC.legend(fontsize=8, loc="upper left"); axC.grid(alpha=0.3, which="both")

    # -- Panel D: the price, and where it is cheapest ------------------------
    axD = ax[1, 1]
    dp = d["s6_decay_pair"]
    a6 = np.array([r["alpha"] for r in dp["rows"]])
    far = np.array([r["farfield_inverse_norm"] for r in dp["rows"]])
    cq = np.array([r["quadratic_gain_constant_measured"] for r in dp["rows"]])
    bud = np.array([r["budget_scoping_estimate"] for r in dp["rows"]])
    axD.plot(a6, far, "o-", color=C["inv"], lw=1.8, ms=5,
             label=r"far-field inverse $2/(2-\alpha)$  (wants $\alpha$ small)")
    axD.plot(a6, cq, "s-", color=C["quad"], lw=1.8, ms=5,
             label=r"quadratic constant $(\int f_\alpha)/\pi$  (wants $\alpha$ large)")
    axD.plot(a6, 2.0 * far * cq, "-", color=C["sum"], lw=2.4,
             label=r"$Z_2$ scoping estimate $= 2\|A\|C_Q$")
    axD.set_yscale("log")
    axD.set_xlabel(r"decay class $\alpha$")
    axD.set_ylabel("constant")
    axD.grid(alpha=0.3, which="both")
    axD.legend(fontsize=8, loc="upper center")
    axD2 = axD.twinx()
    axD2.plot(a6, bud, "d--", color=C["warn"], lw=1.8, ms=6)
    axD2.set_ylabel(r"budget $\sim 1/(4 Z_2)$", color=C["warn"])
    axD2.tick_params(axis="y", labelcolor=C["warn"])
    axD2.axvline(dp["argmax_alpha_closed_form"], color=C["warn"], ls=":", lw=1.6)
    axD2.annotate(r"optimum $\alpha^\ast \approx %.2f$" % dp["argmax_alpha_closed_form"],
                  xy=(dp["argmax_alpha_closed_form"], max(bud)),
                  xytext=(1.52, max(bud) * 0.62), fontsize=9, color=C["warn"])
    axD.set_title("D. The decay-graded pair satisfies BOTH -- at a price\n"
                  "interior optimum: profiles $\\sim X^{-1.44}$, residual "
                  "$\\sim X^{-2.44}$  (scoping estimate)", fontsize=10)

    fig.suptitle("P2 Route-D v3 -- the space-pair question: no diagonal weight pair "
                 "can certify (a NO-GO with its control), and what replaces it "
                 "(NOT a certificate)", fontsize=12, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.975])
    out = FIGS / "fig21_p2_route_d_v3_spaces.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"[fig] wrote {out.relative_to(ROOT)}")


def print_summary():
    d = json.loads(JSON.read_text())
    st = d["s3_st_map"]
    gz = st["gap_sweep"][0]
    print("\nP2 Route-D v3 -- the space-pair scoping leg (a=0 anchor, plain float64)")
    print(f"  S1 Q(h)=hH(h) is a pure convolution; independent builds agree to "
          f"{d['s1_quadratic_identity']['max_disagreement_with_independent_build']:.1e}; "
          f"sharp constant M={d['s1_quadratic_identity']['sharp_constant_unweighted']:.2f} "
          f"(2x better than the Wiener bound v2 used)")
    print(f"  S3 over the whole family u=(1+k)^s, v=(1+m)^t: both exponents depend "
          f"only on g=t-s, and they are complements "
          f"(||A|| ~ N^(1-g), S_K ~ K^g)")
    print(f"     -> min over ALL pairs of (exponent sum) = {gz['min_exponent_sum']:.2f}; "
          f"a certificate needs 0. NO diagonal weight pair works.")
    print(f"  S4 CONTROL (symbol 1+cos -> 1): boundary falls from t>=s+1 to t>=s-1 "
          f"(two powers = the order 1+cos vanishes to); min sum = "
          f"{gz['min_exponent_sum_surrogate']:.2f}, regions overlap at "
          f"{len(d['s4_surrogate_control']['overlap'])}/{len(st['s_grid'])} values of s")
    print(f"     -> the obstruction is the far-field degeneracy, not the method")
    worst = max(r["rel_err_vs_finite_domain_law"]
                for r in d["s5_resonance"]["inverse_side"])
    print(f"  S5 far-field inverse norm = the exact ODE norm to {100 * worst:.3f}% "
          f"(15 values); resonance at alpha=2 = anchor decay = homogeneous solution")
    dp = d["s6_decay_pair"]
    print(f"  S6 the DECAY-graded pair satisfies both requirements; interior optimum "
          f"alpha* ~ {dp['argmax_alpha_closed_form']:.2f} "
          f"(Z2 ~ {min(r['Z2_scoping_estimate'] for r in dp['rows']):.1f})")
    print("  Level-1 tooling + a no-go theorem with its numerical face. NOT a "
          "certificate. Clay odds unchanged (~0.05%).")


if __name__ == "__main__":
    build_figure()
    print_summary()
