"""Spike-1 Step-A evidence: the 2D Boussinesq velocity operator on the stretched grid.

Matches the writeup convention (committed data so the figure rebuilds with no re-run):

    .venv/bin/python writeup/spike1_stepA_evidence.py --generate   # runs the operator,
        writes writeup/data/spike1_stepA_velocity.json
    .venv/bin/python writeup/spike1_stepA_evidence.py              # builds
        writeup/figures/fig9_spike1_stepA_velocity.png from the committed JSON

Evidence: on a log-radial x angular-sine quarter-plane grid, the half-plane Poisson
velocity operator u = grad^perp (-Lap)^{-1} omega recovers a manufactured known
(omega, u, v) to ~1e-5 rel L-inf with 2nd-order radial convergence, and the modulation
origin read u_x(0) to <1e-3. See ../PHASE2_SPIKE1_NOTES.md sec.3 (Step A).
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
JSON = DATA / "spike1_stepA_velocity.json"


def _manufactured(grid, modes=(1, 2)):
    """phi = sum_n R_n(r) sin(2n b), R_1=r^2 e^-r, R_2=r^4 e^-r (regular ~r^{2n}, decaying).
    Verified per-mode radial Laplacian gives omega_1=(5r-r^2)e^-r, omega_2=(9r^3-r^4)e^-r."""
    r, b = grid.R, grid.B
    e = np.exp(-r)
    R = {1: r**2 * e, 2: r**4 * e}
    Rp = {1: (2 * r - r**2) * e, 2: (4 * r**3 - r**4) * e}
    om_radial = {1: (5 * r - r**2) * e, 2: (9 * r**3 - r**4) * e}
    omega = np.zeros_like(r); phi = np.zeros_like(r)
    phi_x = np.zeros_like(r); phi_y = np.zeros_like(r)
    for n in modes:
        s = np.sin(2 * n * b); cc = np.cos(2 * n * b)
        phi += R[n] * s
        omega += om_radial[n] * s
        phi_r = Rp[n] * s
        phi_b = R[n] * (2 * n) * cc
        phi_x += np.cos(b) * phi_r - (np.sin(b) / r) * phi_b
        phi_y += np.sin(b) * phi_r + (np.cos(b) / r) * phi_b
    return omega, phi, -phi_y, phi_x  # omega, phi, u=-phi_y, v=phi_x


def _rel(a, b):
    return float(np.max(np.abs(a - b)) / max(np.max(np.abs(b)), 1e-300))


def generate():
    sys.path.insert(0, str(ROOT))
    from solver.boussinesq_velocity import (
        PolarGrid, velocity_from_vorticity, poisson_solve, u_x_at_origin)

    # (1) convergence under radial refinement (Dirichlet BC isolates the interior) ----
    conv = []
    for n_r in (100, 200, 400, 800, 1600):
        g = PolarGrid(n_r=n_r, n_beta=48, r_min=1e-3, r_max=40.0)
        om, phi_ex, _, _ = _manufactured(g, modes=(1,))
        phi = poisson_solve(om, g, radial_bc="dirichlet", phi_exact=phi_ex)
        conv.append({"n_r": n_r, "phi_err": _rel(phi[3:-3], phi_ex[3:-3])})

    # (2) full velocity recovery (robin far-field), radial cut + error field ----------
    g = PolarGrid(n_r=800, n_beta=48, r_min=1e-3, r_max=40.0)
    om, phi_ex, u_ex, v_ex = _manufactured(g, modes=(1, 2))
    u, v, phi = velocity_from_vorticity(om, g, radial_bc="robin")
    sl = slice(5, -5)
    errs = {"phi": _rel(phi[sl], phi_ex[sl]), "u": _rel(u[sl], u_ex[sl]),
            "v": _rel(v[sl], v_ex[sl])}
    ux0 = u_x_at_origin(phi, g)

    # radial cut of u at beta ~ pi/4
    jcut = int(np.argmin(np.abs(g.beta - np.pi / 4)))
    rmask = g.r < 8.0
    cut = {"beta": float(g.beta[jcut]), "r": g.r[rmask].tolist(),
           "u_exact": u_ex[rmask, jcut].tolist(), "u_num": u[rmask, jcut].tolist()}

    # coarse error field on physical (x,y) for a heatmap (bulk only, |x|,|y|<4)
    err_field = np.abs(u - u_ex) / max(np.abs(u_ex[sl]).max(), 1e-300)
    ri = np.unique(np.linspace(0, g.n_r - 1, 60).astype(int))
    field = {"x": g.X[np.ix_(ri, np.arange(g.n_beta))].tolist(),
             "y": g.Y[np.ix_(ri, np.arange(g.n_beta))].tolist(),
             "log10_relerr": np.log10(np.clip(err_field[np.ix_(ri, np.arange(g.n_beta))],
                                              1e-12, None)).tolist()}

    payload = {
        "meta": {
            "operator": "u = grad^perp (-Lap)^{-1} omega, half-plane, phi=0 on wall",
            "grid": "log-radial r=exp(rho) x angular-sine sin(2n beta), beta in [0,pi/2]",
            "decoupling": "phi_n''(rho) - (2n)^2 phi_n = -r^2 omega_n  (per mode, tridiag)",
            "manufactured": "phi=r^2 e^-r sin2b + r^4 e^-r sin4b (known u,v; u_x(0)=-2)",
        },
        "convergence": conv,
        "velocity_errors": errs,
        "u_x_origin": {"value": ux0, "target": -2.0},
        "radial_cut": cut,
        "error_field": field,
    }
    JSON.write_text(json.dumps(payload))
    print(f"wrote {JSON}")
    print(f"  velocity rel errs {errs}, u_x(0)={ux0:+.4f} (target -2)")


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
    C_EXACT, C_NUM, C_REF = "#111827", "#2563eb", "#9ca3af"
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.0))

    # panel A: radial cut of u, exact vs recovered
    cut = d["radial_cut"]
    r = np.array(cut["r"])
    ax[0].plot(r, cut["u_exact"], color=C_EXACT, lw=3.0, alpha=0.55,
               label="exact $u^*$")
    ax[0].plot(r, cut["u_num"], color=C_NUM, lw=1.4, label="recovered $u$")
    ax[0].set_xlabel("r  (radial cut at $\\beta=\\pi/4$)")
    ax[0].set_ylabel("$u = -\\phi_y$")
    ax[0].set_title("A. Velocity from vorticity on the\nstretched grid (known answer)")
    ax[0].legend(loc="best", fontsize=8.5)

    # panel B: convergence log-log with slope-2 reference
    conv = d["convergence"]
    n = np.array([c["n_r"] for c in conv], float)
    e = np.array([c["phi_err"] for c in conv], float)
    ax[1].loglog(n, e, "o-", color=C_NUM, lw=1.6, label="rel L$\\infty$ error")
    ref = e[0] * (n[0] / n) ** 2
    ax[1].loglog(n, ref, "--", color=C_REF, lw=1.2, label="slope $-2$ (ref)")
    ax[1].set_xlabel("radial points $n_r$"); ax[1].set_ylabel("rel L$\\infty$ error")
    ax[1].set_title("B. 2nd-order radial convergence\n(not a lucky single grid)")
    ax[1].legend(loc="best", fontsize=8.5)

    # panel C: error field heatmap on physical (x,y)
    x = np.array(d["error_field"]["x"]); y = np.array(d["error_field"]["y"])
    z = np.array(d["error_field"]["log10_relerr"])
    m = (x < 4) & (y < 4)
    pc = ax[2].scatter(x[m], y[m], c=z[m], s=8, cmap="viridis", vmin=-6, vmax=-2)
    ax[2].set_xlabel("x"); ax[2].set_ylabel("y")
    ax[2].set_xlim(0, 4); ax[2].set_ylim(0, 4)
    ax[2].set_aspect("equal")
    ax[2].grid(False)
    cb = fig.colorbar(pc, ax=ax[2]); cb.set_label("$\\log_{10}$ rel err in $u$")
    ev = d["velocity_errors"]; ux0 = d["u_x_origin"]["value"]
    ax[2].set_title("C. Error field: $u$ recovered to\n"
                    f"~{ev['u']:.0e}; $u_x(0)$={ux0:+.4f} (target $-2$)")

    fig.suptitle("Spike 1 Step A — 2D Boussinesq velocity operator "
                 "$u=\\nabla^\\perp(-\\Delta)^{-1}\\omega$ on a stretched grid "
                 "(known-answer validation)", fontsize=11.5, y=1.02)
    fig.tight_layout()
    out = FIGS / "fig9_spike1_stepA_velocity.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    if not JSON.exists():
        print("no committed JSON; run with --generate first")
        sys.exit(1)
    build_figure()
