"""fig64 -- Route-CAPG v1 (leg 162): the compact-support / global-Chebyshev corner.

Rebuilds from writeup/data/p2_route_capg_v1_corner.json ONLY -- no re-run, no solve.

Run:  .venv/bin/python experiments/p2_route_capg_v1_corner_evidence.py
Out:  writeup/figures/fig64_route_capg_v1.png
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "writeup", "data", "p2_route_capg_v1_corner.json")
FIGS = os.path.join(ROOT, "writeup", "figures")
REAL_B = "cheb_compact_support_olver_townsend"
REAL_A = "cheb_compact_support_repo_ansatz"


def main():
    with open(DATA) as fh:
        d = json.load(fh)
    fig, ax = plt.subplots(1, 3, figsize=(16.5, 5.0))

    # -- panel 1: the shape dichotomy, with the control that must disagree ---
    sh = d["CAPG2_shape"]
    names = ["realization A\n(1-v^2)T_n", "realization B\nsqrt(1-v^2)U_{n-1}",
             "CONTROL\ncompactified\nwhole line"]
    rows = [sh["realizations"][REAL_A], sh["realizations"][REAL_B],
            sh["CONTROL_wholeline_compactified"]]
    x = np.arange(3)
    diag = [r["max_abs_diagonal"] for r in rows]
    off = [r["max_abs_offdiagonal"] for r in rows]
    ax[0].bar(x - 0.19, np.maximum(diag, 1e-2), 0.38, label="max |diagonal|",
              color="#2a6f97")
    ax[0].bar(x + 0.19, np.maximum(off, 1e-2), 0.38, label="max |off-diagonal|",
              color="#c1121f")
    ax[0].set_yscale("log")
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(names, fontsize=8.5)
    ax[0].set_ylabel("magnitude of the unbounded part")
    for i, r in enumerate(rows):
        ax[0].text(i, 1.6e-2, r["label"], ha="center", fontsize=9, fontweight="bold",
                   color="#c1121f" if r["label"] == "SHIFT" else "#2a6f97")
    ax[0].axhline(1e-2, color="0.6", lw=0.8, ls=":")
    ax[0].set_title("(a) one classifier, three operators,\nand they DISAGREE (lesson 90)",
                    fontsize=10)
    ax[0].legend(fontsize=8, loc="upper left")

    # -- panel 2: the Z_1 grid, realization B, A21 = 0 ----------------------
    grid = [r for r in d["CAPG4_grid"]
            if r["realization"] == REAL_B and r["shape"] == "block_diag"]
    As = sorted({r["a"] for r in grid})
    cmap = plt.get_cmap("viridis")
    for i, a in enumerate(As):
        rows_a = sorted([r for r in grid if r["a"] == a], key=lambda r: r["s"])
        ax[1].plot([r["s"] for r in rows_a], [r["Z1"] for r in rows_a], "o-",
                   color=cmap(i / max(len(As) - 1, 1)), label=f"a = {a}", ms=4, lw=1.5)
    ax[1].axhline(1.0, color="#c1121f", lw=1.6, ls="--")
    ax[1].text(0.03, 1.12, "Z$_1$ = 1, what a certificate needs to beat",
               color="#c1121f", fontsize=8.5)
    ax[1].set_yscale("log")
    ax[1].set_xlabel("weight exponent  s   (deterministic grid, no search)")
    ax[1].set_ylabel("Z$_1$ = colmax(I - A L),  A21 = 0")
    ax[1].set_title("(b) realization B, block-diagonal A:\nZ$_1$ falls UNDER 1", fontsize=10)
    ax[1].legend(fontsize=7.5, ncol=2)
    ax[1].grid(alpha=0.25)

    # -- panel 3: the two things that could have made it an artifact --------
    lad = d["CAPG5_truncation_ladder"]["rows"]
    Ns = [r["N"] for r in lad]
    ax[2].plot(Ns, [r["block_diag"] for r in lad], "o-", color="#2a6f97",
               label="block_diag")
    ax[2].plot(Ns, [r["gs_upper"] for r in lad], "s-", color="#588157", label="gs_upper")
    ax[2].axhline(1.0, color="#c1121f", lw=1.4, ls="--")
    ax[2].set_xscale("log", base=2)
    ax[2].set_yscale("log")
    ax[2].set_xlabel("truncation N")
    ax[2].set_ylabel("Z$_1$")
    drift = d["CAPG5_truncation_ladder"]["relative_drift_over_8x_refinement"]
    bd = d["CAPG6_border"]
    nb = bd.get("n_gauges_below_1")
    ax[2].set_title(f"(c) not an artifact of truncation\n(8x refinement moves it {drift:.2%})",
                    fontsize=10)
    ax[2].legend(fontsize=8)
    ax[2].grid(alpha=0.25)
    if nb is not None:
        ax[2].text(0.02, 0.03,
                   f"CAVEAT, and it travels with the number:\nZ$_1$ < 1 at {nb} of 4 border "
                   f"gauges\n(worst gauge: {bd['worst_gauge_Z1']:.3g})",
                   transform=ax[2].transAxes, fontsize=7.8, va="bottom",
                   bbox=dict(fc="#fff3cd", ec="#c1121f", lw=0.8, alpha=0.95))

    fig.suptitle("Route-CAPG v1 (leg 162) -- the compact-support / global-Chebyshev corner: "
                 "UNCOVERED by leg 126's enumeration, and its Z$_1$ falls under 1.  "
                 "Z$_1$ is ONE of four constants; this is not a certificate.",
                 fontsize=10.5, fontweight="bold", y=1.02)
    fig.tight_layout()
    os.makedirs(FIGS, exist_ok=True)
    out = os.path.join(FIGS, "fig64_route_capg_v1.png")
    fig.savefig(out, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
