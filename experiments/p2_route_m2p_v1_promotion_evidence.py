#!/usr/bin/env python3
"""fig61 -- Leg 125 (Route-M2P v1): evidence + redraw from curated JSON, no re-run.

writeup/INDEX.md's gap-list item 13 named this route as missing a `*_evidence.py`: fig61
already exists on disk, but it was produced by directly running
`experiments/p2_route_m2p_v1_promotion.py`'s `main()`, which re-solves the Newton iteration
for every panel from scratch (M2-M7) -- a fresh solve, not a rebuild from curated data. This
script closes that debt: it imports NO solver module (`solver.dissipative_profile` is never
imported here) and reads ONLY the already-banked
`writeup/data/p2_route_m2p_v1_promotion.json`.

The one adaptation from the original `build_figure()`: panel (a) there draws a re-solved
Newton profile (a dashed line requiring a fresh `DissipativeProfile.newton()` call, because
the raw coefficient array is not itself banked in the JSON -- only summary scalars are).
That re-solve is exactly the class of re-measurement this evidence script must not do. Panel
(a) here instead plots ONLY Chen's closed form
`Omega(x) = -2 b x / (x^2+b^2)^2` -- evaluating a fixed analytic formula at banked constants
`b`, not solving anything -- and annotates it with the banked Newton-reconstruction numbers
from `M3_newton_reconstruction` (n=1201: c_l -> 0.333333435, abs err 1.02e-07) as text,
rather than as a re-solved curve. Panels (b), (c) and (d) are unchanged from the original:
every number on them was already read straight out of the JSON's `M4_delta_sweep`,
`M5_nu_branch_search`, `M7_gamma2_branch` and `M6_y0_budget` blocks.

    .venv/bin/python experiments/p2_route_m2p_v1_promotion_evidence.py
"""

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_m2p_v1_promotion.json")
FIG = os.path.join(ROOT, "writeup", "figures", "fig61_route_m2p_v1_promotion.png")


def build_figure(payload):
    fig, ax = plt.subplots(2, 2, figsize=(13.5, 9.5))

    # (a) Chen's closed-form profile, evaluated from banked constants only -- no solve.
    b = payload["M1_chen_constants"]["b"]["value"]
    x = np.linspace(-4, 4, 2001)
    omega = -2.0 * b * x / (x ** 2 + b ** 2) ** 2
    ax[0, 0].plot(x, omega, lw=2.4, color="#1b3a6b",
                  label=r"Chen eq (2.2): $\Omega=-2bx/(x^2+b^2)^2$, $b=\sqrt{3/8}$ (closed form)")
    n1201 = next(r for r in payload["M3_newton_reconstruction"] if r["n"] == 1201)
    ax[0, 0].text(0.02, 0.04,
                  "Newton reconstruction (banked, not re-solved here):\n"
                  r"$n=1201$: $c_l\to%.9f$ (abs err %.2e), $H\Omega(0)\to%.9f$ (abs err %.2e)"
                  % (n1201["c_l_measured"], n1201["c_l_abs_err"],
                     n1201["HOmega_at_0_measured"], n1201["shape_sup_err_vs_chen"]),
                  transform=ax[0, 0].transAxes, fontsize=7.5, va="bottom",
                  bbox=dict(boxstyle="round", fc="#f5f0e6", ec="#999"))
    ax[0, 0].set_title("(a) The profile is the INVISCID $a=1/2$ profile\n"
                       r"Chen sec 2.6: '$\nu(t)$ converges to 0 $\Rightarrow$ "
                       "same as the inviscid profile'", fontsize=10)
    ax[0, 0].set_xlabel("$x$"); ax[0, 0].set_ylabel(r"$\Omega$")
    ax[0, 0].legend(fontsize=8); ax[0, 0].grid(alpha=0.3)

    # (b) Delta(a) -- unchanged, read straight off the JSON.
    rows = payload["M4_delta_sweep"]
    aa = [r["a"] for r in rows]; dd = [r["Delta"] for r in rows]
    ax[0, 1].plot(aa, dd, "o-", color="#1b3a6b", lw=2, label=r"$\Delta(a)=2c_l/|c_\omega|-1$")
    ax[0, 1].axhline(0.0, color="#c8102e", lw=2,
                     label=r"$\Delta=0$: the only line where a $\gamma=2$ profile is admissible")
    ax[0, 1].axhline(-1.0 / 3.0, color="#888", ls=":", lw=1.5, label=r"Chen exact $-1/3$")
    ax[0, 1].plot([0.5], [payload["M4_controls"]["chen_exact_1_3"]], "*", ms=16,
                  color="#e8a33d", label=r"$a=1/2$ (Chen's regime): $\Delta=-1/3$")
    astar = payload["M4_a_star"]["a_star_direct_solve_c_l_imposed_one_half"]
    ax[0, 1].plot([astar], [0.0], "P", ms=13, color="#7b1fa2",
                  label=r"$a^*=%.5f$: $\Delta=0$, and it is NOT Chen's $a$" % astar)
    ax[0, 1].set_title(r"(b) The obstruction is measured, not assumed:"
                       "\n" r"$\Delta$ crosses 0 at $a^*=%.5f$, far from $a=1/2$" % astar,
                       fontsize=10)
    ax[0, 1].set_xlabel("advection $a$"); ax[0, 1].set_ylabel(r"$\Delta$")
    ax[0, 1].legend(fontsize=8); ax[0, 1].grid(alpha=0.3)

    # (c) steadiness defect / imposed-Delta=0 branch search -- unchanged.
    rows = payload["M5_nu_branch_search"]
    nn = [max(r["nu"], 1e-5) for r in rows]; ss = [r["steadiness_defect"] for r in rows]
    ax[1, 0].semilogx(nn, ss, "s-", color="#1b3a6b", lw=2,
                      label=r"$|\Delta(\nu)|$ on Chen's $a=1/2$ branch (M5)")
    ax[1, 0].axhline(0.0, color="#c8102e", lw=2,
                     label=r"$\Delta=0$: what a $\gamma=2$ profile needs")
    m7 = payload["M7_gamma2_branch"]
    tr = [r for r in m7 if r["collapsed_to_trivial_null"]]
    ax[1, 0].plot([max(r["nu"], 1e-5) for r in tr], [0.0] * len(tr), "x", ms=13, mew=2.5,
                  color="#7b1fa2",
                  label=r"collapsed to the trivial null $\Omega\equiv 0$ (M7 control)")
    ax[1, 0].set_ylim(-0.05, max(ss) * 1.25 + 0.02)
    ax[1, 0].set_title(r"(c) On Chen's branch the defect only GROWS with $\nu$;"
                       "\n" r"$|\Delta|$ = %.4f at $\nu=0$, %.4f at $\nu=0.3$"
                       % (ss[0], ss[-1]), fontsize=10)
    ax[1, 0].set_xlabel(r"$\nu$ (dilation gauge fixed; $\nu=0$ plotted at $10^{-5}$)")
    ax[1, 0].set_ylabel(r"steadiness defect $|\Delta|$")
    ax[1, 0].legend(fontsize=8); ax[1, 0].grid(alpha=0.3)

    # (d) Y0 vs budget -- unchanged.
    rows = payload["M6_y0_budget"]
    ns = [r["n"] for r in rows]
    y_h = [r["Y0_consistency_honest"] for r in rows]
    y_d = [max(r["Y0_discrete_newton_floor"], 1e-18) for r in rows]
    bmax = [r["budget_Y0_max"] for r in rows]
    ax[1, 1].semilogy(ns, bmax, "^-", color="#2e7d32", lw=2.4,
                      label=r"radii-polynomial budget $Y_{0,\max}$ (leg 53 $Z_1=0.9156$)")
    ax[1, 1].semilogy(ns, y_h, "o-", color="#1b3a6b", lw=2,
                      label=r"$Y_0$ (honest: consistency defect)")
    ax[1, 1].semilogy(ns, y_d, "x--", color="#999", lw=1.4,
                      label=r"$Y_0$ (discrete Newton floor -- a statement about the code)")
    ratios = [r["Y0_over_budget_ratio_honest"] for r in rows]
    ax[1, 1].set_title("(d) $Y_0$ is OVER budget at every resolution, and the gap WIDENS:\n"
                       r"$%.1f\times10^{9}$ at $n=601$ $\to$ $%.1f\times10^{10}$ at $n=1201$"
                       % (ratios[0] / 1e9, ratios[-1] / 1e10), fontsize=10)
    ax[1, 1].set_xlabel("resolution $n$"); ax[1, 1].set_ylabel("sup norm")
    ax[1, 1].legend(fontsize=8); ax[1, 1].grid(alpha=0.3, which="both")

    fig.suptitle("Route-M2P v1 (leg 125) -- Chen arXiv:1908.09385's $\\gamma=2$ gCLM candidate: "
                 "full text, constants, first $Y_0$ (rebuilt from curated JSON, leg 372)",
                 fontsize=12.5)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG, dpi=140)
    plt.close(fig)


def main():
    with open(DATA) as fh:
        payload = json.load(fh)

    # Self-checks before drawing anything.
    assert payload["leg"] == 125 and payload["route"] == "ROUTE-M2P"
    assert payload["no_dynamics_run"] is True
    m6 = payload["M6_y0_budget"]
    assert all(row["closes_with_honest_Y0"] is False for row in m6), \
        "M2P's own gate is NO at every resolution -- this evidence script must not silently pass it"
    assert m6[-1]["Y0_over_budget_ratio_honest"] > m6[0]["Y0_over_budget_ratio_honest"], \
        "the gap must widen under refinement, as the banked TECHNICAL doc states"
    b = payload["M1_chen_constants"]["b"]["value"]
    assert abs(b ** 2 - 0.375) < 1e-12, "Chen's b^2 = 3/8 identity must hold in the banked constants"

    build_figure(payload)
    print(f"wrote {FIG}\nrebuilt from {DATA} alone, no solver import, no re-run")


if __name__ == "__main__":
    main()
