"""Spike-0 evidence: generate the committed data JSON and rebuild the figure.

Two entry points, matching the writeup convention (data is committed so the
figure rebuilds with no solver re-run):

    .venv/bin/python writeup/spike0_rescaling_evidence.py --generate   # runs the
        solver (~1-2 min) and writes writeup/data/spike0_rescaling.json
    .venv/bin/python writeup/spike0_rescaling_evidence.py              # builds
        writeup/figures/fig8_spike0_rescaling.png from the committed JSON

The evidence is the Spike-0 known-answer validation: on a sinh-stretched
whole-line grid, CLM (a=0) dynamic self-similar rescaling recovers the exact
profile Omega_0 = -4X/(1+4X^2) and the exact rate c_omega -> -1 from perturbed
initial data, resolution-stable. See ../PHASE2_SPIKE0_NOTES.md.
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).resolve().parent / "data"
FIGS = Path(__file__).resolve().parent / "figures"
DATA.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "spike0_rescaling.json"


def _downsample(x, m=400):
    """Keep ~m points, densest near X=0 (uniform in the sinh coordinate index)."""
    n = len(x)
    if n <= m:
        return np.arange(n)
    return np.unique(np.linspace(0, n - 1, m).astype(int))


def generate():
    sys.path.insert(0, str(ROOT))
    from solver.gclm_rescaled import RescaledCLM, clm_profile
    from solver.line_hilbert import line_hilbert

    def sinh_grid_pts(n, c, rho_max):
        rho = np.linspace(-rho_max, rho_max, n)
        return c * np.sinh(rho)

    # (1) line Hilbert transform known-answer convergence (the crux) --------
    hilbert_conv = []
    for n, rho_max in ((601, 7.0), (1201, 8.5), (2401, 10.0)):
        X = sinh_grid_pts(n, 0.5, rho_max)
        f = -4.0 * X / (1.0 + 4.0 * X ** 2)
        exact = 2.0 / (1.0 + 4.0 * X ** 2)
        Hf = line_hilbert(X, f)
        core = np.abs(X) < 5.0
        core[:3] = core[-3:] = False
        err = float(np.abs(Hf[core] - exact[core]).max())
        hilbert_conv.append({"n": n, "rho_max": rho_max,
                             "M": float(X.max()), "max_abs_err": err})

    # (2) dynamic convergence from a perturbed odd IC ----------------------
    s = RescaledCLM(n=1201, c=0.5, rho_max=8.0)
    X = s.X
    f_init = -4.0 * np.exp(-X ** 2 / 2.0)      # same origin slope -4, wider tail
    omega_init = X * f_init
    r = s.run(f_init, dt_frac=0.4, tol=1e-7, max_steps=80000)
    omega_final = r["omega"]
    omega_exact = clm_profile(X)

    idx = _downsample(X)
    # thin the tau histories to ~300 points
    th = np.unique(np.linspace(0, len(r["tau_hist"]) - 1, 300).astype(int))

    # (3) resolution stability ---------------------------------------------
    res_stability = []
    for n, rho_max in ((901, 7.5), (1801, 8.5)):
        sr = RescaledCLM(n=n, c=0.5, rho_max=rho_max)
        f0 = -4.0 * np.exp(-sr.X ** 2 / 2.0)
        rr = sr.run(f0, dt_frac=0.4, tol=1e-7, max_steps=120000)
        core = np.abs(sr.X) < 5.0
        core[:3] = core[-3:] = False
        shape = float(np.abs(rr["omega"][core] - clm_profile(sr.X)[core]).max()
                      / np.abs(clm_profile(sr.X)).max())
        res_stability.append({"n": n, "c_omega": float(rr["c_omega"]),
                              "shape_err": shape, "steps": int(rr["steps"])})

    payload = {
        "meta": {
            "model": "CLM (a=0) dynamic self-similar rescaling, whole-line sinh grid",
            "target_profile": "Omega_0(X) = -4X/(1+4X^2)",
            "target_rate": "c_omega -> -1  (omega ~ (T-t)^-1)",
            "grid": "X = 0.5*sinh(rho), rho uniform; k=1; 3rd-order upwind + SSPRK3",
        },
        "hilbert_convergence": hilbert_conv,
        "run": {
            "n": s.n, "rho_max": 8.0, "converged": bool(r["converged"]),
            "steps": int(r["steps"]), "tau": float(r["tau"]),
            "c_omega_final": float(r["c_omega"]),
            "shape_err_final": float(
                np.abs(omega_final[np.abs(X) < 5.0][3:-3]
                       - omega_exact[np.abs(X) < 5.0][3:-3]).max()
                / np.abs(omega_exact).max()),
            "X": X[idx].tolist(),
            "omega_init": omega_init[idx].tolist(),
            "omega_final": omega_final[idx].tolist(),
            "omega_exact": omega_exact[idx].tolist(),
            "tau_hist": np.asarray(r["tau_hist"])[th].tolist(),
            "c_hist": np.asarray(r["c_hist"])[th].tolist(),
            "res_hist": np.asarray(r["res_hist"])[th].tolist(),
        },
        "resolution_stability": res_stability,
    }
    JSON.write_text(json.dumps(payload, indent=2))
    print(f"wrote {JSON}")
    print(f"  converged in {r['steps']} steps, c_omega={r['c_omega']:+.5f}, "
          f"shape_err={payload['run']['shape_err_final']:.2e}")


def build_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(JSON.read_text())
    run = d["run"]
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    C_EXACT, C_FINAL, C_INIT, C_RATE = "#111827", "#2563eb", "#9ca3af", "#059669"

    fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.0))

    # panel A: profile overlay
    X = np.array(run["X"])
    m = np.abs(X) < 6
    ax[0].plot(X[m], np.array(run["omega_init"])[m], color=C_INIT, lw=1.4,
               ls="--", label="initial data (perturbed)")
    ax[0].plot(X[m], np.array(run["omega_exact"])[m], color=C_EXACT, lw=3.0,
               alpha=0.55, label=r"exact $\bar\Omega_0=-4X/(1+4X^2)$")
    ax[0].plot(X[m], np.array(run["omega_final"])[m], color=C_FINAL, lw=1.4,
               label="converged (rescaled)")
    ax[0].set_xlabel("X"); ax[0].set_ylabel(r"$\Omega$")
    ax[0].set_title("A. Perturbed data relaxes onto the\nexact CLM profile")
    ax[0].legend(loc="lower right", fontsize=8.5)

    # panel B: rate history c_omega(tau) -> -1
    tau = np.array(run["tau_hist"]); ch = np.array(run["c_hist"])
    ax[1].axhline(-1.0, color=C_EXACT, lw=1.0, ls=":", label="target $c_\\omega=-1$")
    ax[1].plot(tau, ch, color=C_RATE, lw=1.6)
    ax[1].set_xlabel(r"rescaled time $\tau$"); ax[1].set_ylabel(r"$c_\omega$")
    ax[1].set_ylim(-2.6, 0.2)
    ax[1].set_title("B. Self-similar rate converges\n"
                    fr"to $c_\omega=-1$ ($\to${ch[-1]:+.4f})")
    ax[1].legend(loc="lower right", fontsize=8.5)

    # panel C: residual decay + convergence tables
    res = np.array(run["res_hist"])
    ax[2].semilogy(tau, res, color=C_FINAL, lw=1.6)
    ax[2].set_xlabel(r"rescaled time $\tau$")
    ax[2].set_ylabel(r"$\|f_\tau\|_\infty$ (residual)")
    ax[2].set_title("C. Relaxation to a steady\nprofile (residual decay)")
    # annotate the known-answer numbers
    hc = d["hilbert_convergence"]
    lines = ["line-H err vs known pair:"]
    for h in hc:
        lines.append(f"  M={h['M']:.0f}: {h['max_abs_err']:.1e}")
    lines.append(f"final shape err: {run['shape_err_final']:.1e}")
    ax[2].text(0.03, 0.03, "\n".join(lines), transform=ax[2].transAxes,
               fontsize=7.6, va="bottom", ha="left", family="monospace",
               bbox=dict(boxstyle="round", fc="white", ec="#d1d5db", alpha=0.9))

    fig.suptitle("Spike 0 — CLM dynamic rescaling recovers the exact self-similar "
                 "profile and rate (known-answer validation)", fontsize=11.5, y=1.02)
    fig.tight_layout()
    out = FIGS / "fig8_spike0_rescaling.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    if not JSON.exists():
        print("no committed JSON; run with --generate first")
        sys.exit(1)
    build_figure()
