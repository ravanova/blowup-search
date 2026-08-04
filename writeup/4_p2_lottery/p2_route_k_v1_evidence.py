"""Phase-2 P2 Route-K v1 (fig40): the L1->L2 certification port, step one.

Ranked item (3), deferred six times, attempted at last. The directive asked for a
Newton-Kantorovich setup on the 2D Boussinesq profile, an honest Y_0, a first Z_1, and a
kill-switch that STOPS rather than hardens. The kill-switch fires before the function space
is reached, and this figure is the mechanism plus the controls that make it a statement
about the object rather than about our instrument.

Rebuild fig40 from committed data:
    .venv/bin/python writeup/4_p2_lottery/p2_route_k_v1_evidence.py
Regenerate the data (deterministic; ~9 min):
    .venv/bin/python -u experiments/p2_route_k_v1_port.py

Six panels: A the relaxation does not converge in TIME (the sup residual limit-cycles and
c_l/c_omega swings across the published value); B it does not converge under REFINEMENT
either -- Route-G's own committed ladder, residual growing 16x while c_omega holds to
0.77%; C where the defect sits, which moves to the wall; D the instrument's controls, so
that "the solve stalled" is not a statement about our GMRES; E THE STALL -- relative linear
residual against Krylov dimension, flat at both seeds, with and without the leading-order
preconditioner; F the radii polynomial, and how far down the chain we got.
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
JSON = DATA / "p2_route_k_v1_port.json"
C = {"bad": "#c1440e", "good": "#2e7d32", "anchor": "#1f4e79",
     "warn": "#e08a1e", "grey": "#888888", "ns": "#7b1fa2"}


def build_figure():
    d = json.loads(JSON.read_text())
    k1 = d["K1_K2_no_fixed_point"]
    k3 = d["K3_instrument_controls"]
    k4 = d["K4_krylov_stall"]
    fig, ax = plt.subplots(2, 3, figsize=(16.8, 9.8))

    # ---- A: no fixed point in time ---------------------------------------
    a0 = ax[0, 0]
    rows = k1["steps_ladder"]
    st = [r["steps"] for r in rows]
    a0.semilogy(st, [r["residual_sup"] for r in rows], "o-", color=C["bad"], lw=1.8, ms=7)
    a0.set_xlabel("relaxation steps")
    a0.set_ylabel("$\\|F\\|_\\infty$", color=C["bad"])
    a0.tick_params(axis="y", labelcolor=C["bad"])
    b0 = a0.twinx()
    b0.plot(st, [r["ratio"] for r in rows], "s--", color=C["anchor"], lw=1.5, ms=6)
    b0.axhline(k1["chen_hou_ratio"], color=C["good"], ls=":", lw=1.4)
    b0.text(0.40, 0.06, "Chen–Hou $c_l/c_\\omega = -2.9206$", transform=b0.transAxes,
            fontsize=7, color=C["good"])
    b0.set_ylabel("$c_l/c_\\omega$", color=C["anchor"])
    b0.tick_params(axis="y", labelcolor=C["anchor"])
    a0.set_title("A  the relaxation LIMIT-CYCLES — it has no fixed point\n"
                 "$\\|F\\|_\\infty$ = " +
                 " → ".join(f"{r['residual_sup']:.3f}" for r in rows) +
                 "; the ratio swings across the published value", fontsize=9)

    # ---- B: nor under refinement -----------------------------------------
    a1 = ax[0, 1]
    gl = [q for q in k1["route_g_resolution_ladder"] if q["r_max"] == 1e5]
    nr = [q["n_r"] for q in gl]
    a1.semilogy(nr, [q["residual"] for q in gl], "o-", color=C["bad"], lw=1.8, ms=8)
    a1.set_xlabel("$n_r$  (Route-G's committed ladder, $r_{max}=10^5$)")
    a1.set_ylabel("steady-state $\\|F\\|_\\infty$", color=C["bad"])
    a1.tick_params(axis="y", labelcolor=C["bad"])
    b1 = a1.twinx()
    b1.plot(nr, [q["c_omega"] for q in gl], "s--", color=C["anchor"], lw=1.5, ms=7)
    b1.set_ylabel("$c_\\omega$", color=C["anchor"])
    b1.tick_params(axis="y", labelcolor=C["anchor"])
    b1.set_ylim(-1.05, -1.00)
    a1.set_title("B  refining makes the residual WORSE, and $c_\\omega$ does not notice\n"
                 f"residual $\\times${k1['route_g_residual_growth_factor']:.0f} while "
                 f"$c_\\omega$ holds to "
                 f"{k1['route_g_c_omega_spread_over_that_ladder']:.2%}", fontsize=9)

    # ---- C: where the defect sits ----------------------------------------
    a2 = ax[0, 2]
    fields = ("omega", "eta", "xi")
    mk = {"omega": "o", "eta": "s", "xi": "^"}
    for f in fields:
        r = [q["argmax"][f]["r"] for q in rows]
        b = [q["argmax"][f]["beta"] for q in rows]
        a2.scatter(r, b, s=[40 + 260 * (i / len(rows)) for i in range(len(rows))],
                   marker=mk[f], facecolors="none",
                   edgecolors=C["anchor"] if f == "omega" else
                   (C["warn"] if f == "eta" else C["ns"]), linewidths=1.6, label=f)
    a2.set_xscale("log")
    a2.axhline(0.0, color=C["bad"], lw=2.5, alpha=0.6)
    a2.text(0.55, 0.10, "the wall $\\beta = 0$", transform=a2.transAxes,
            fontsize=8, color=C["bad"])
    a2.axhline(np.pi / 2, color=C["grey"], ls=":", lw=1.2)
    a2.text(0.03, 0.92, "the axis $\\beta = \\pi/2$", transform=a2.transAxes,
            fontsize=7, color=C["grey"])
    a2.set_xlabel("$r$ of the residual's argmax   (marker grows with step count)")
    a2.set_ylabel("$\\beta$ of the argmax")
    a2.legend(fontsize=7, loc="center right")
    a2.set_title("C  where the defect lives: it migrates to the WALL\n"
                 "early transients sit mid-domain and at the outer edge; "
                 "the survivor is $\\beta \\approx 0$", fontsize=9)

    # ---- D: the instrument's controls ------------------------------------
    a3 = ax[1, 0]
    js = k3["jv_step_study"]
    h = [q["h_rel"] for q in js]
    a3.loglog(h, [q["norm_Jv"] for q in js], "o-", color=C["good"], lw=1.8, ms=7)
    a3.set_xlabel("$h/\\|z\\|$ in the finite-difference $Jv$")
    a3.set_ylabel("$\\|Jv\\|$", color=C["good"])
    a3.tick_params(axis="y", labelcolor=C["good"])
    a3.set_ylim(30, 130)
    a3.invert_xaxis()
    d3 = a3.twinx()
    dr = [(q["h_rel"], q["rel_change_vs_previous_h"]) for q in js
          if "rel_change_vs_previous_h" in q]
    d3.loglog([q[0] for q in dr], [q[1] for q in dr], "s--", color=C["grey"], lw=1.3, ms=6)
    d3.set_ylabel("relative change vs previous $h$", color=C["grey"])
    d3.tick_params(axis="y", labelcolor=C["grey"])
    g = k3["gmres"]
    a3.set_title("D  the instrument, gated before the operator is blamed\n"
                 f"GMRES: {g['well_conditioned']['rel_true']:.0e} in "
                 f"{g['well_conditioned']['k']} its; cond~$10^8$ stalls at "
                 f"{g['cond_1e8']['rel']:.3f}. $Jv$ flat over 5 decades of $h$", fontsize=9)

    # ---- E: THE STALL ----------------------------------------------------
    a4 = ax[1, 1]
    styles = {("cycle_best", "unpreconditioned"): (C["bad"], "o-"),
              ("cycle_best", "preconditioned"): (C["warn"], "s-"),
              ("cycle_worst", "unpreconditioned"): (C["bad"], "o--"),
              ("cycle_worst", "preconditioned"): (C["warn"], "s--")}
    for seed in ("cycle_best", "cycle_worst"):
        for kind in ("unpreconditioned", "preconditioned"):
            col, ls = styles[(seed, kind)]
            rr = k4[seed][kind]
            a4.plot([q["m"] for q in rr], [q["rel_residual"] for q in rr], ls,
                    color=col, lw=1.7, ms=6,
                    label=f"{kind[:6]}, {seed.split('_')[1]} of cycle")
    a4.set_xscale("log")
    a4.set_ylim(0, 0.8)
    a4.axhline(g["cond_1e8"]["rel"], color=C["grey"], ls=":", lw=1.4)
    a4.text(0.03, 0.10, "where mere cond~$10^8$ gets to", transform=a4.transAxes,
            fontsize=7, color=C["grey"])
    a4.set_xlabel("Krylov dimension $m$")
    a4.set_ylabel("relative residual of  $DF\\,x = -F$")
    a4.legend(fontsize=6.5, loc="upper right")
    sb = k4["cycle_best"]["unpreconditioned_stall"]
    a4.set_title("E  $DF$ has no computable inverse — and the curve is FLAT\n"
                 f"$16\\times$ the Krylov work buys "
                 f"{100 * (1 - 1 / sb['residual_gain']):.0f}%: a continuum in the "
                 "spectrum, not conditioning", fontsize=9)

    # ---- F: the chain --------------------------------------------------
    a5 = ax[1, 2]
    a5.axis("off")
    steps = [("(i)   a fixed profile $x^*$ with $F(x^*)=0$", "BLOCKED", C["bad"]),
             ("(ii)  $Y_0 \\geq \\|A\\,F(x^*)\\|$, the defect", "UNDEFINED", C["bad"]),
             ("(iii) $A \\approx DF^{-1}$, $Z_1 = \\|I - A\\,DF\\| < 1$", "NO $A$", C["bad"]),
             ("(iv)  $Z_2 r^2 - (1-Z_1) r + Y_0 \\leq 0$", "NOT REACHED", C["grey"])]
    a5.text(0.0, 0.96, "what a radii-polynomial argument needs, in order:",
            fontsize=9.5, weight="bold", transform=a5.transAxes)
    for i, (txt, tag, col) in enumerate(steps):
        y = 0.80 - 0.13 * i
        a5.text(0.0, y, txt, fontsize=9, transform=a5.transAxes)
        a5.text(0.80, y, tag, fontsize=9, weight="bold", color=col,
                transform=a5.transAxes)
    a5.text(0.0, 0.24,
            "The kill-switch fires at (ii), before the function space is chosen.\n"
            "$Y_0$ is not large — it is not about anything, because there is no\n"
            "profile. $Z_1$ likewise: the stall level depends on which point of\n"
            "the limit cycle you linearize at (0.662 vs 0.245, a $2.7\\times$ spread).\n\n"
            "Named next, in order: a preconditioner covering the Biot–Savart\n"
            "velocity and the wall (the dilation split accounts for about half);\n"
            "then a Newton profile; only then the space, $Y_0$ and $Z_1$.",
            fontsize=8.4, transform=a5.transAxes, va="top")
    a5.set_title("F  the chain, and how far down it we got", fontsize=9)

    fig.suptitle("Route-K v1 — the L1→L2 certification port, step one: there is no object "
                 "to certify yet, and here is the mechanism", fontsize=12, y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    out = FIGS / "fig40_route_k_v1_port.png"
    fig.savefig(out, dpi=150)
    print(f"-> {out}")


if __name__ == "__main__":
    build_figure()
