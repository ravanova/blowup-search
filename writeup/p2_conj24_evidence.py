"""Phase-2 P2 evidence: the Conjecture-2.4 (Chen-Huang-Li arXiv:2604.01868) relaxation
at POC fidelity -- the LOCAL-attractor test of their asymptotic-stability claim.

Data is produced by the logged experiment harness (which locks the predicate):
    .venv/bin/python experiments/p2_conj24_relax.py --logged   # writes
        writeup/data/p2_conj24_relax.json  (committed; the figure rebuilds from it)
Then:
    .venv/bin/python writeup/p2_conj24_evidence.py             # builds
        writeup/figures/fig13_p2_conj24_relax.png  from the committed JSON
(`--generate` re-runs the harness; normally unnecessary -- the JSON is committed.)

Evidence, three panels:
  A. Gauge trajectories c_l(k), c_omega(k) for the anchor hold and two perturbations ->
     all settle at (2,-1): a local attractor.
  B. Residual vs step (log): the anchor/perturbations DROP ~1-2 decades and plateau at a
     nonzero POC floor (a stable HOLD, not zero-convergence); the generic far degenerate
     IC does NOT relax -- the documented basin boundary.
  C. Endpoint (c_l,c_omega) for every run vs the target (2,-1): hold+perturbations cluster
     on it (same fixed point); generic sits off it.

See ../PHASE2_P2_NOTES.md and writeup/TECHNICAL_P2_CONJ24.md.
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / "data"
FIGS = Path(__file__).resolve().parent / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_conj24_relax.json"


def generate():
    subprocess.run([sys.executable, str(ROOT / "experiments" / "p2_conj24_relax.py"),
                    "--logged"], check=True)


def build_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(JSON.read_text())
    R = d["results"]
    tgt_cl, tgt_cw = d["targets"]["c_l"], d["targets"]["c_omega"]
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    C = {"hold_nu02": "#111827", "pert_plus": "#2563eb", "pert_minus": "#16a34a",
         "hold_nu04": "#a855f7", "generic": "#dc2626"}
    LAB = {"hold_nu02": "anchor hold", "pert_plus": "perturb +", "pert_minus": "perturb −",
           "hold_nu04": "hold (ν=0.04)", "generic": "generic degen. IC"}
    C_REF = "#9ca3af"
    fig, ax = plt.subplots(1, 3, figsize=(13.8, 4.1))

    # panel A: gauge trajectories for hold + two perturbations
    axA = ax[0]
    for name in ("hold_nu02", "pert_plus", "pert_minus"):
        r = R[name]; k = np.array(r["k"])
        axA.plot(k, r["c_l_hist"], color=C[name], lw=1.5, label=LAB[name])
        axA.plot(k, r["c_omega_hist"], color=C[name], lw=1.5, ls="--")
    axA.axhline(tgt_cl, color=C_REF, lw=1.0, ls=":")
    axA.axhline(tgt_cw, color=C_REF, lw=1.0, ls=":")
    axA.text(0.98, tgt_cl + 0.08, r"$c_\ell\to2$", ha="right", fontsize=8,
             transform=axA.get_yaxis_transform())
    axA.text(0.98, tgt_cw + 0.08, r"$c_\omega\to-1$", ha="right", fontsize=8,
             transform=axA.get_yaxis_transform())
    axA.set_xlabel("step k"); axA.set_ylabel(r"gauge constants $c_\ell$ (—), $c_\omega$ (– –)")
    axA.set_title("A. Gauge trajectories → (2, −1)\n(anchor + two perturbations)")
    axA.legend(loc="center right", fontsize=8)

    # panel B: residual vs step (log) for all runs
    axB = ax[1]
    for name in ("hold_nu02", "pert_plus", "pert_minus", "hold_nu04", "generic"):
        r = R[name]; k = np.array(r["k"])
        axB.semilogy(k, np.abs(r["res_hist"]), color=C[name], lw=1.4, label=LAB[name])
    axB.set_xlabel("step k"); axB.set_ylabel(r"$\|\partial_\tau\Omega\|_\infty$")
    axB.set_title("B. Residual: drop-and-plateau (hold/perturb)\n"
                  "vs no relaxation (generic IC)")
    axB.legend(loc="best", fontsize=7.5)

    # panel C: endpoint (c_l,c_omega) scatter vs target
    axC = ax[2]
    for name in ("hold_nu02", "pert_plus", "pert_minus", "hold_nu04", "generic"):
        r = R[name]
        axC.scatter([r["c_l_final"]], [r["c_omega_final"]], s=70, color=C[name],
                    edgecolor="white", zorder=3, label=LAB[name])
    axC.scatter([tgt_cl], [tgt_cw], marker="*", s=320, color="#f59e0b",
                edgecolor="#111827", zorder=4, label="target (2,−1)")
    # 0.15 tolerance box
    axC.add_patch(plt.Rectangle((tgt_cl - 0.15, tgt_cw - 0.15), 0.30, 0.30,
                                fill=False, ls="--", ec=C_REF, lw=1.0))
    axC.set_xlabel(r"$c_\ell$ (final)"); axC.set_ylabel(r"$c_\omega$ (final)")
    axC.set_title("C. Endpoints vs the fixed point\n(hold+perturb cluster; generic off)")
    axC.legend(loc="best", fontsize=7.5)

    checks = d.get("predicate_checks", {})
    npass = sum(bool(v) for v in checks.values())
    fig.suptitle("Phase-2 P2 — Conjecture 2.4 (CHL) at POC fidelity: LOCAL attractor confirmed "
                 f"({npass}/{len(checks)} locked clauses); global basin beyond a fixed-grid POC "
                 "— reproduces a numerical claim, not a proof", fontsize=10.0, y=1.03)
    fig.tight_layout()
    out = FIGS / "fig13_p2_conj24_relax.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    else:
        if not JSON.exists():
            generate()
        build_figure()
