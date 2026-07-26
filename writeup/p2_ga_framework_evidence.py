"""Phase-2 P2 (GA framework) evidence: a genetic-algorithm GLOBAL search for
self-similar profiles of the gCLM `a`-family, validated at the a=0 known answer.

This session built the SEARCH INFRASTRUCTURE for the gCLM two-scale<->two-stage
transition probe (solver/gclm_family.py + solver/ga_search.py). It is NOT a new
blowup result -- it is validated tooling plus one instructive finding (the
rescaling gauge is dilation-invariant, so the steady set is a 1-parameter family
and only the invariant A^2/B is a "match"). See PHASE2_P2_NOTES.md section 9 and
writeup/TECHNICAL_P2_GA_FRAMEWORK.md.

Data is produced here (self-contained; no logged-run harness needed since this is
infrastructure validation, not a gate run) and committed as
    writeup/data/p2_ga_framework.json
so the figure rebuilds without recomputing:
    .venv/bin/python writeup/p2_ga_framework_evidence.py            # rebuild fig16
    .venv/bin/python writeup/p2_ga_framework_evidence.py --generate # recompute JSON

Evidence, four panels (fig16):
  A. Residual landscape over the genome (A,B) at a=0: a sharp valley along
     A^2/B = 4 -- the dilation family of the exact CLM profile Omega_0 = -4X/(1+4X^2).
  B. GA convergence: best residual vs generation for several seeds, all reaching
     the ~1e-5 floor; the pinned (B=4) run recovers A=-4.
  C. Recovered profiles: three dilation-family members the GA found (different seeds)
     overlaid, each an exact rescaling of Omega_0 -- same shape, gauge freedom visible.
  D. a-dependence: RMS residual of the a=0 profile as a grows -- advection BREAKS the
     a=0 steady state (residual climbs from ~0), the effect the transition map measures.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
DATA = Path(__file__).resolve().parent / "data"
FIGS = Path(__file__).resolve().parent / "figures"
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_ga_framework.json"


def generate():
    from solver.gclm_family import GCLMResidual, odd_rational, clm_one_scale
    from solver.ga_search import ga_minimize, GAConfig

    R = GCLMResidual(a=0.0, n=601)

    # -- Panel A: residual landscape over (A,B) --
    A_grid = np.linspace(-8.0, -0.5, 70)
    B_grid = np.linspace(0.5, 12.0, 70)
    land = np.zeros((B_grid.size, A_grid.size))
    for j, A in enumerate(A_grid):
        for i, B in enumerate(B_grid):
            land[i, j] = R.residual_norm(odd_rational(R.X, [A, B]))

    # -- Panel B/C: GA runs, several seeds, plus the pinned recovery --
    def fit(g):
        return R.residual_norm(odd_rational(R.X, g))

    seeds = [0, 1, 2]
    ga_runs = []
    for s in seeds:
        cfg = GAConfig(pop_size=40, n_generations=70, seed=s, target_fitness=1e-5)
        r = ga_minimize(fit, [-8.0, 0.5], [-0.5, 12.0], config=cfg)
        A, B = r.best_genome
        ga_runs.append({
            "seed": s, "A": float(A), "B": float(B),
            "invariant": float(A * A / B), "fitness": float(r.best_fitness),
            "history": [float(h) for h in r.history],
            "profile": odd_rational(R.X, r.best_genome).tolist(),
        })

    def fitA(g):
        return R.residual_norm(odd_rational(R.X, [g[0], 4.0]))

    rp = ga_minimize(fitA, [-8.0], [-0.5],
                     GAConfig(pop_size=30, n_generations=60, seed=0, target_fitness=1e-6))
    pinned = {"A": float(rp.best_genome[0]), "fitness": float(rp.best_fitness),
              "history": [float(h) for h in rp.history]}

    # -- Panel D: a-dependence of the a=0 profile residual --
    a_vals = np.linspace(0.0, 1.5, 16)
    a_res = []
    Om0 = clm_one_scale(R.X)
    for a in a_vals:
        Ra = GCLMResidual(a=float(a), n=601)
        res, _, _ = Ra.residual(Om0)
        a_res.append(float(np.sqrt(np.mean(res ** 2))))

    out = {
        "X": R.X.tolist(),
        "anchor_profile": Om0.tolist(),
        "landscape": {"A": A_grid.tolist(), "B": B_grid.tolist(),
                      "logres": np.log10(land + 1e-12).tolist()},
        "ga_runs": ga_runs,
        "pinned": pinned,
        "a_dependence": {"a": a_vals.tolist(), "residual_rms": a_res},
        "meta": {"n": R.n, "anchor": "-4X/(1+4X^2)", "invariant": "A^2/B=4"},
    }
    JSON.write_text(json.dumps(out))
    print(f"wrote {JSON}")


def build_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(JSON.read_text())
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.22, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    X = np.array(d["X"])
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))

    # A: landscape + dilation valley A^2/B=4
    L = d["landscape"]
    A = np.array(L["A"]); B = np.array(L["B"]); Z = np.array(L["logres"])
    pc = ax[0, 0].pcolormesh(A, B, Z, shading="auto", cmap="viridis")
    Bv = np.linspace(0.5, 12, 200)
    ax[0, 0].plot(-np.sqrt(4.0 * Bv), Bv, "w--", lw=1.6, label=r"$A^2/B=4$ (exact family)")
    ax[0, 0].scatter([-4], [4], c="red", s=40, zorder=5, label=r"$\Omega_0$: $(-4,4)$")
    fig.colorbar(pc, ax=ax[0, 0], label=r"$\log_{10}$ residual RMS")
    ax[0, 0].set_xlabel("genome A"); ax[0, 0].set_ylabel("genome B")
    ax[0, 0].set_title("A. a=0 residual landscape: a dilation valley, not a point")
    ax[0, 0].legend(loc="upper left", fontsize=8)

    # B: GA convergence
    for run in d["ga_runs"]:
        ax[0, 1].semilogy(run["history"], lw=1.4,
                          label=f"seed {run['seed']}: $A^2/B$={run['invariant']:.2f}")
    ax[0, 1].semilogy(d["pinned"]["history"], "k--", lw=1.4,
                      label=f"pinned B=4 -> A={d['pinned']['A']:.3f}")
    ax[0, 1].set_xlabel("generation"); ax[0, 1].set_ylabel("best residual RMS")
    ax[0, 1].set_title("B. GA convergence to the steady set (~1e-5 floor)")
    ax[0, 1].legend(fontsize=8)

    # C: recovered profiles vs exact anchor
    core = np.abs(X) < 6
    ax[1, 0].plot(X[core], np.array(d["anchor_profile"])[core], "k", lw=2.4,
                  label=r"exact $\Omega_0=-4X/(1+4X^2)$", zorder=5)
    for run in d["ga_runs"]:
        ax[1, 0].plot(X[core], np.array(run["profile"])[core], lw=1.1, alpha=0.9,
                      label=f"GA seed {run['seed']} (a dilation of $\\Omega_0$)")
    ax[1, 0].set_xlabel("X"); ax[1, 0].set_ylabel(r"$\Omega(X)$")
    ax[1, 0].set_title("C. Recovered profiles: each an exact rescaling of the anchor")
    ax[1, 0].legend(fontsize=8)

    # D: a-dependence
    aD = d["a_dependence"]
    ax[1, 1].plot(aD["a"], aD["residual_rms"], "o-", color="#c1440e", lw=1.6, ms=4)
    ax[1, 1].set_xlabel("advection parameter a"); ax[1, 1].set_ylabel("residual RMS of the a=0 profile")
    ax[1, 1].set_title("D. Advection breaks the a=0 steady state (the map's target)")

    fig.suptitle("Fig 16 — GA global search for gCLM self-similar profiles: a=0 known-answer gate "
                 "(framework validated; no logged blowup result yet)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = FIGS / "fig16_p2_ga_framework.png"
    fig.savefig(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv or not JSON.exists():
        generate()
    build_figure()
