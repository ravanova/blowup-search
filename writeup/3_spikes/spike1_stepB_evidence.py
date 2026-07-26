"""Spike-1 Step-B evidence: the rescaled 2D Boussinesq solver (transport + gradients +
origin reads + the formulation decision).

Matches the writeup convention (committed data so the figure rebuilds with no re-run):

    .venv/bin/python writeup/spike1_stepB_evidence.py --generate   # runs the operators,
        writes writeup/data/spike1_stepB_rescaled.json
    .venv/bin/python writeup/spike1_stepB_evidence.py              # builds
        writeup/figures/fig10_spike1_stepB_rescaled.png from the committed JSON

Three panels tell the Step-B story:
  A. FORMULATION DECISION (user-requested, data-driven): reading theta_xx(0) off eta=theta_x
     (a linear r-slope of one odd mode) is ~2x more accurate + noise-robust than off primitive
     theta (an r^2 curvature of two even modes, contaminated by theta_yy). -> chose (omega,eta,xi).
  B. OPERATOR CONVERGENCE: the 2D upwind transport kernel (~3rd order) and grad_xy (~2nd order),
     validated vs manufactured answers -- convergence, not a lucky single grid.
  C. THE RATIO CANCELLATION: c_l = 2 eta_x(0)/omega_x(0) is recovered orders of magnitude better
     than either slope alone, because the projection quadrature bias cancels in the ratio.
See ../PHASE2_SPIKE1_NOTES.md sec.3 (Step B).
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
DATA.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "spike1_stepB_rescaled.json"


def _rel_linf(a, b, sl):
    return float(np.max(np.abs(a[sl] - b[sl])) / max(np.max(np.abs(b[sl])), 1e-300))


def generate():
    sys.path.insert(0, str(ROOT))
    from solver.boussinesq_velocity import PolarGrid
    from solver.boussinesq_rescaled import transport, grad_xy, odd_field_x_slope
    from experiments.spike1_stepB_decide_formulation import (
        fields as decide_fields, read_eta_slope, read_theta_curv, THXX_TRUE)

    interior = (slice(6, -6), slice(2, -2))

    # (A) formulation decision: eta-slope vs primitive-theta curvature read of theta_xx(0) ---
    decision = []
    for n_r, n_b in [(300, 48), (600, 64), (1200, 96)]:
        g = PolarGrid(n_r=n_r, n_beta=n_b, r_min=1e-3, r_max=20.0)
        _, theta, eta = decide_fields(g)
        e_eta = abs(read_eta_slope(eta, g) - THXX_TRUE) / abs(THXX_TRUE)
        e_th = abs(read_theta_curv(theta, g) - THXX_TRUE) / abs(THXX_TRUE)
        decision.append({"n_r": n_r, "eta_err": e_eta, "theta_err": e_th})

    # (B) operator convergence: 2D transport (dilation+rotation) and grad_xy ---------------
    def manuf(g):
        r, b = g.R, g.B
        e = np.exp(-r)
        f = e * np.sin(2 * b)
        f_r = -e * np.sin(2 * b)
        f_b = 2 * e * np.cos(2 * b)
        f_x = np.cos(b) * f_r - (np.sin(b) / r) * f_b
        f_y = np.sin(b) * f_r + (np.cos(b) / r) * f_b
        return f, f_x, f_y

    transport_conv, grad_conv = [], []
    for s in (1, 2, 4):
        g = PolarGrid(n_r=250 * s, n_beta=32 * s, r_min=1e-2, r_max=30.0)
        f, f_x, f_y = manuf(g)
        Ax, Ay = g.X + g.Y, g.Y - g.X
        t_exact = Ax * f_x + Ay * f_y
        t_num = transport(f, Ax, Ay, g, c_l=0.0)
        transport_conv.append({"n_r": 250 * s, "err": _rel_linf(t_num, t_exact, interior)})
        gx, _ = grad_xy(f, g)
        grad_conv.append({"n_r": 250 * s, "err": _rel_linf(gx, f_x, interior)})

    # (C) ratio cancellation: c_l = 2 eta_x(0)/omega_x(0) vs the individual slope error ------
    g = PolarGrid(n_r=800, n_beta=64, r_min=1e-3, r_max=20.0)
    wx0, ex0 = -2.1, 3.4
    env = np.exp(-(g.R ** 2))
    w_read = odd_field_x_slope(wx0 * g.X * env, g)
    e_read = odd_field_x_slope(ex0 * g.X * env, g)
    cl_true = 2 * ex0 / wx0
    ratio = {
        "slope_err": abs(w_read - wx0) / abs(wx0),
        "cl_err": abs(2 * e_read / w_read - cl_true) / abs(cl_true),
    }

    payload = {
        "meta": {
            "system": "rescaled 2D Boussinesq (omega, eta=theta_x, xi=theta_y), Chen-Hou (2.10)/(2.28)",
            "decision": "theta_xx(0) read: eta-slope (opt2/3) vs primitive-theta curvature (opt1)",
            "targets": {"c_l": 3.00649898, "c_omega": -1.02942516, "alpha": -0.342407},
        },
        "decision": decision,
        "transport_conv": transport_conv,
        "grad_conv": grad_conv,
        "ratio": ratio,
    }
    JSON.write_text(json.dumps(payload))
    print(f"wrote {JSON}")
    print(f"  decision (finest): eta {decision[-1]['eta_err']:.2e} vs theta {decision[-1]['theta_err']:.2e}")
    print(f"  ratio: slope err {ratio['slope_err']:.2e}, c_l err {ratio['cl_err']:.2e}")


def build_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(JSON.read_text())
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    C_ETA, C_TH, C_REF, C_T, C_G = "#2563eb", "#dc2626", "#9ca3af", "#059669", "#7c3aed"
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.0))

    # panel A: formulation decision -- read error vs resolution
    dec = d["decision"]
    n = np.array([c["n_r"] for c in dec], float)
    ee = np.array([c["eta_err"] for c in dec], float)
    et = np.array([c["theta_err"] for c in dec], float)
    ax[0].plot(n, ee * 100, "o-", color=C_ETA, lw=1.7, label="$\\eta$-slope  (chosen: $\\omega,\\eta,\\xi$)")
    ax[0].plot(n, et * 100, "s-", color=C_TH, lw=1.7, label="primitive-$\\theta$ curvature")
    ax[0].set_xlabel("resolution $n_r$"); ax[0].set_ylabel("$\\theta_{xx}(0)$ read error  (%)")
    ax[0].set_title("A. Formulation chosen by DATA:\n$\\eta{=}\\theta_x$ read ~2$\\times$ better")
    ax[0].legend(loc="best", fontsize=8.5)

    # panel B: operator convergence (log-log)
    tc, gc = d["transport_conv"], d["grad_conv"]
    nt = np.array([c["n_r"] for c in tc], float); et2 = np.array([c["err"] for c in tc], float)
    ng = np.array([c["n_r"] for c in gc], float); eg = np.array([c["err"] for c in gc], float)
    ax[1].loglog(nt, et2, "o-", color=C_T, lw=1.6, label="transport $(c_l x{+}u)\\cdot\\nabla$")
    ax[1].loglog(ng, eg, "s-", color=C_G, lw=1.6, label="gradient $\\nabla_{xy}$")
    ax[1].loglog(nt, et2[0] * (nt[0] / nt) ** 3, "--", color=C_REF, lw=1.0, label="slope $-3$")
    ax[1].loglog(ng, eg[0] * (ng[0] / ng) ** 2, ":", color=C_REF, lw=1.0, label="slope $-2$")
    ax[1].set_xlabel("resolution $n_r$"); ax[1].set_ylabel("rel L$\\infty$ error")
    ax[1].set_title("B. Operators converge vs known\nanswers (not lucky single grids)")
    ax[1].legend(loc="best", fontsize=8)

    # panel C: ratio cancellation
    r = d["ratio"]
    labels = ["single slope\n$\\omega_x(0)$", "ratio\n$c_l{=}2\\eta_x(0)/\\omega_x(0)$"]
    vals = [max(r["slope_err"], 1e-17), max(r["cl_err"], 1e-17)]
    bars = ax[2].bar(labels, vals, color=[C_ETA, "#111827"], width=0.6)
    ax[2].set_yscale("log"); ax[2].set_ylabel("relative error")
    ax[2].set_ylim(1e-17, 1e-3)
    for b, v in zip(bars, vals):
        ax[2].text(b.get_x() + b.get_width() / 2, v * 2, f"{v:.0e}", ha="center", fontsize=9)
    ax[2].set_title("C. Bias cancels in the ratio:\n$c_l$ is the best-conditioned quantity")
    ax[2].grid(axis="x", visible=False)

    fig.suptitle("Spike 1 Step B — rescaled 2D Boussinesq solver "
                 "$(\\omega,\\eta{=}\\theta_x,\\xi{=}\\theta_y)$: pieces validated vs known answers",
                 fontsize=11.5, y=1.02)
    fig.tight_layout()
    out = FIGS / "fig10_spike1_stepB_rescaled.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    if not JSON.exists():
        print("no committed JSON; run with --generate first")
        sys.exit(1)
    build_figure()
