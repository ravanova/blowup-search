"""Phase-2 P2 (B1) evidence: CHL Scenario 2 (arXiv:2604.01868, their (4.1)/(4.2))
reproduced -- the regular, strictly-positive self-similar profile and its
amplitude-INVARIANT contraction exponent c_l/c_omega = -2.5114.

Data is produced by the logged experiment harness (which locks the predicate):
    .venv/bin/python experiments/p2_scenario2_relax.py --logged   # writes
        writeup/data/p2_scenario2_relax.json  (committed; the figure rebuilds from it)
Then:
    .venv/bin/python writeup/p2_scenario2_evidence.py             # builds
        writeup/figures/fig15_p2_scenario2.png  from the committed JSON
(`--generate` re-runs the harness; normally unnecessary -- the JSON is committed.)

Evidence, three panels:
  A. Ratio trajectory c_l/c_omega(k) for two distinct non-symmetric positive ICs ->
     both converge to CHL's -2.5114: a genuine IC-independent attractor for the
     amplitude-invariant self-similar exponent.
  B. Residual vs step (log): falls ~2-3 decades then FLOORS at ~2e-2 -- the honest
     fixed-grid ceiling (CHL reach 1e-6 with an adaptive mesh), not zero-convergence.
  C. The converged regular profiles Omega(X), V=Theta_X(X): strictly positive, smooth
     (max|Omega_X|/peak ~ 0.7 vs ~1061 for the singular Stage-2 anchor), non-symmetric,
     peaked away from the origin -- CHL's Scenario-2 / Stage-1 object.

Not novel, not a proof: a Tier-2 reproduction of a published (numerical) result. Its value
is the VALIDATED origin-pinned gauge machinery. See ../PHASE2_P2_NOTES.md (section 8) and
writeup/TECHNICAL_P2_SCENARIO2.md.
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_scenario2_relax.json"


def generate():
    subprocess.run([sys.executable, str(ROOT / "experiments" / "p2_scenario2_relax.py"),
                    "--logged"], check=True)


def build_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(JSON.read_text())
    R = d["results"]
    ratio_star = d["ratio_target"]
    chl = d["chl_triple"]
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    fig, ax = plt.subplots(1, 3, figsize=(14.5, 4.3))
    labels = {"ic_x0_30": "IC $x_0{=}0.30$", "ic_x0_45": "IC $x_0{=}0.45$"}
    colors = {"ic_x0_30": "#1f77b4", "ic_x0_45": "#d62728"}

    # -- A: ratio trajectory --------------------------------------------------
    for name, r in R.items():
        k = np.array(r["k"])
        ratio = np.array(r["c_l_hist"]) / np.array(r["c_omega_hist"])
        ax[0].plot(k, ratio, color=colors[name], lw=1.6, label=labels[name])
    ax[0].axhline(ratio_star, color="k", ls="--", lw=1.2,
                  label=f"CHL Fig 4.2: {ratio_star}")
    ax[0].set_ylim(-3.2, -1.8)
    ax[0].set_xlabel("step $k$")
    ax[0].set_ylabel(r"contraction exponent  $c_l/c_\omega$")
    ax[0].set_title("A. invariant exponent → CHL value\n(IC-independent attractor)")
    ax[0].legend(loc="lower right", fontsize=8.5)

    # -- B: residual vs step (log) --------------------------------------------
    for name, r in R.items():
        k = np.array(r["k"])
        ax[1].semilogy(k, r["res_hist"], color=colors[name], lw=1.6, label=labels[name])
    ax[1].axhline(1e-6, color="gray", ls=":", lw=1.0,
                  label="CHL stop $10^{-6}$ (adaptive mesh)")
    ax[1].set_xlabel("step $k$")
    ax[1].set_ylabel(r"residual  $\max(\|\Omega_\tau\|_\infty,\|V_\tau\|_\infty)$")
    ax[1].set_title("B. residual floors ~$2\\times10^{-2}$\n(honest fixed-grid ceiling)")
    ax[1].legend(loc="upper right", fontsize=8.5)

    # -- C: converged regular profiles ----------------------------------------
    r = R["ic_x0_30"]
    X = np.array(r["X"]); Om = np.array(r["Omega"]); V = np.array(r["V"])
    band = (X > -1.0) & (X < 6.0)
    ax[2].plot(X[band], Om[band], color="#1f77b4", lw=1.8, label=r"$\Omega$")
    ax[2].plot(X[band], V[band], color="#2ca02c", lw=1.8, label=r"$V=\Theta_X$")
    ax[2].axhline(0.0, color="k", lw=0.6)
    ax[2].axvline(r["xstar"], color="#1f77b4", ls=":", lw=1.0)
    ax[2].set_xlabel("$X$")
    ax[2].set_ylabel("profile")
    ax[2].set_title(f"C. regular positive profile\n"
                    f"min $\\Omega$={r['min_Omega']:.1e}>0, "
                    f"smooth={r['smoothness']:.2f}, $X^*$={r['xstar']:.2f}")
    ax[2].legend(loc="upper right", fontsize=9)

    r30, r45 = R["ic_x0_30"], R["ic_x0_45"]
    fig.suptitle(
        f"CHL Scenario 2 reproduced (Tier-2, PARTIAL): both ICs → "
        f"$c_l/c_\\omega$ = {r30['ratio_final']:.4f} / {r45['ratio_final']:.4f} "
        f"(CHL {ratio_star})   |   absolute triple "
        f"$({r30['c_l_final']:.2f},{r30['c_omega_final']:.2f},{r30['c_r_final']:.2f})$ "
        f"off CHL raw $({chl[0]},{chl[1]},{chl[2]})$ — normalization-dependent",
        fontsize=10.5, y=1.02)
    fig.tight_layout()
    out = FIGS / "fig15_p2_scenario2.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    build_figure()
