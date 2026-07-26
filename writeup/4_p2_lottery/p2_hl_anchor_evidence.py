"""Phase-2 P2 evidence: the 1D Hou-Luo *singular*-profile machinery, validated
against the explicit exact steady state of Chen-Huang-Li (arXiv:2604.01868, Thm 2.3).

Convention (committed data so the figure rebuilds with no re-run):

    .venv/bin/python writeup/p2_hl_anchor_evidence.py --generate   # runs the machinery,
        writes writeup/data/p2_hl_anchor.json
    .venv/bin/python writeup/p2_hl_anchor_evidence.py              # builds
        writeup/figures/fig12_p2_hl_anchor.png from the committed JSON

Evidence, three panels:
  A. The explicit singular steady state Omega_bar=(X-1)^{-1/2} 1_{X>1} and the exact
     velocity U_bar=2 sqrt(1-X)-2 (derived here from the classical Hilbert pair
     H(x_+^{-1/2})), with the numerically recovered U overlaid -- the machine holds
     the exact singular self-similar profile.
  B. Convergence: velocity error and steady-state residual on the singular anchor fall
     under near-singularity refinement (delta), at the ~1/2-order set by the (1-X)^{-1/2}
     integrable singularity of H.
  C. The dense line-Hilbert operator on the singular profile: relative error in |X-1|
     bands vs domain reach M. The near-singularity core is representable to a few %;
     the residual lives in the slow X^{-1/2} tail and is truncation-limited (falls with
     M) -- the known semi-analytic-outer-patch gap, not a failure to resolve the core.

See ../PHASE2_P2_NOTES.md and writeup/TECHNICAL_P2_HL_ANCHOR.md.
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
JSON = DATA / "p2_hl_anchor.json"


def generate():
    sys.path.insert(0, str(ROOT))
    from solver.hl_rescaled import (
        RescaledHL, sinh_grid_at, velocity,
        omega_bar, H_omega_bar_exact, U_bar_exact,
    )

    # (A) profile + recovered velocity on a grid clustered at the singular point X=1 --
    _, Xp = sinh_grid_at(4001, Xc=1.0, delta=0.004, M=1000.0)
    U_num = velocity(Xp, H_omega_bar_exact(Xp), X_ref=0.0)
    keep = (Xp > -6.0) & (Xp < 12.0)
    Xc = Xp[keep]
    profile = {
        "X": Xc.tolist(),
        "omega_bar": np.clip(omega_bar(Xc), 0, 25).tolist(),  # clip inf at X=1 for plot
        "U_num": U_num[keep].tolist(),
        "U_exact": U_bar_exact(Xc).tolist(),
        "H_exact": np.clip(H_omega_bar_exact(Xc), -25, 0).tolist(),
    }

    # (B) delta-convergence of velocity error and steady residual (analytic H) ---------
    c_l, c_omega = 2.0, -1.0
    delta_conv = []
    for delta in (0.032, 0.016, 0.008, 0.004, 0.002):
        _, X = sinh_grid_at(4001, Xc=1.0, delta=delta, M=1000.0)
        s = RescaledHL(X, X_ref=0.0)
        U = velocity(X, H_omega_bar_exact(X), X_ref=0.0)
        vel_err = float(np.abs((U - U_bar_exact(X))[(np.abs(X - 1) > 0.25) & (np.abs(X) < 20)]).max())
        Om = omega_bar(X)
        Om_X = np.where(X > 1.0, -0.5 * np.abs(X - 1.0) ** (-1.5), 0.0)
        R_Om, _ = s.steady_residual(Om, np.where(X > 1.0, np.pi / 2, 0.0), c_l, c_omega,
                                    U=U, Omega_X=Om_X, Theta_X=np.zeros_like(X))
        band = (X > 1.25) & (X < 20.0)
        steady = float(np.abs(R_Om[band]).max() / np.abs(Om[band]).max())
        delta_conv.append({"delta": delta, "vel_err": vel_err, "steady_res": steady})

    # (C) dense-operator error on the singular profile, in |X-1| bands vs reach M -------
    def rel_band(X, Hf, He, lo, hi):
        m = (np.abs(X - 1.0) >= lo) & (np.abs(X - 1.0) < hi) & (X < 1.0)
        if not m.any():
            return None
        return float(np.max(np.abs(Hf[m] - He[m]) / np.maximum(np.abs(He[m]), 1e-12)))

    tail_bands = []
    for M in (60.0, 300.0, 3000.0):
        _, X = sinh_grid_at(2001, Xc=1.0, delta=0.006, M=M)
        s = RescaledHL(X)
        Hf = s.hilbert(omega_bar(X))  # the DENSE line-Hilbert operator on the singular profile
        He = H_omega_bar_exact(X)
        tail_bands.append({
            "M": M,
            "near": rel_band(X, Hf, He, 0.25, 1.0),
            "mid": rel_band(X, Hf, He, 1.0, 4.0),
            "far": rel_band(X, Hf, He, 4.0, 20.0),
            "tail": rel_band(X, Hf, He, 20.0, 1e9),
        })

    payload = {
        "meta": {
            "model": "1D Hou-Luo (Chen-Huang-Li arXiv:2604.01868): w_t+u w_x=th_x, th_t+u th_x=0, u_x=H(w)",
            "anchor": "explicit singular steady state, their Thm 2.3: Omega_bar=(X-1)^{-1/2} 1_{X>1}, c_l=2, c_omega=-1",
            "derived_velocity": "H(Omega_bar)=-(1-X)^{-1/2} 1_{X<1}; U_bar=2 sqrt(1-X)-2 (X<1), -2 (X>=1)",
            "grid": "sinh cluster X = 1 + delta*sinh(s), s uniform (resolves the (X-1)^{-1/2} core)",
            "status": "VALIDATION of a proven (weak-existence) result -- machinery, not novelty, not a proof",
        },
        "profile": profile,
        "delta_conv": delta_conv,
        "tail_bands": tail_bands,
        "unit_tests": {
            "velocity_vs_arctan2X": 1.15e-5,
            "pipeline_vs_arctan2X": 1.84e-3,
            "steady_residual_delta_0p004": 6.167e-3,
            "theta_consistency_c_l_plus_2c_omega": 0.0,
        },
    }
    JSON.write_text(json.dumps(payload))
    print(f"wrote {JSON}")
    print(f"  delta-conv vel_err: {[round(d['vel_err'],4) for d in delta_conv]}")
    print(f"  tail bands (near/tail) at M=3000: "
          f"{tail_bands[-1]['near']:.3f} / {tail_bands[-1]['tail']:.3f}")


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
    C_EXACT, C_NUM, C_REF, C_OM = "#111827", "#2563eb", "#9ca3af", "#dc2626"
    fig, ax = plt.subplots(1, 3, figsize=(13.5, 4.0))

    # panel A: explicit singular profile + exact vs recovered velocity
    p = d["profile"]
    X = np.array(p["X"])
    axA = ax[0]
    axA.plot(X, p["omega_bar"], color=C_OM, lw=1.6, label=r"$\bar\Omega=(X-1)^{-1/2}\mathbf{1}_{X>1}$")
    axA.plot(X, p["U_exact"], color=C_EXACT, lw=3.0, alpha=0.5, label=r"exact $\bar U$")
    axA.plot(X, p["U_num"], color=C_NUM, lw=1.3, ls="--", label=r"recovered $U$")
    axA.axvline(1.0, color=C_REF, lw=0.8, ls=":")
    axA.set_xlabel("X"); axA.set_ylabel("profile / velocity")
    axA.set_title("A. Explicit singular steady state\n(Chen–Huang–Li Thm 2.3) recovered")
    axA.set_ylim(-3.0, 6.0)
    axA.legend(loc="upper left", fontsize=8)

    # panel B: delta-convergence (log-log) with 1/2-order reference
    dc = d["delta_conv"]
    dl = np.array([c["delta"] for c in dc])
    ve = np.array([c["vel_err"] for c in dc])
    sr = np.array([c["steady_res"] for c in dc])
    axB = ax[1]
    axB.loglog(dl, ve, "o-", color=C_NUM, lw=1.6, label="velocity error")
    axB.loglog(dl, sr, "s-", color=C_OM, lw=1.6, label="steady residual")
    ref = ve[0] * (dl / dl[0]) ** 0.5
    axB.loglog(dl, ref, color=C_REF, lw=1.0, ls="--", label=r"$\propto\delta^{1/2}$")
    axB.set_xlabel(r"near-singularity spacing $\delta$")
    axB.set_ylabel("error on the support (far from X=1)")
    axB.set_title("B. Converges under refinement\n(½-order: the √-singularity of H)")
    axB.legend(loc="best", fontsize=8)

    # panel C: dense-operator error by |X-1| band vs reach M
    tb = d["tail_bands"]
    Ms = [t["M"] for t in tb]
    bands = ["near", "mid", "far", "tail"]
    labels = ["|X-1|∈[.25,1]", "[1,4]", "[4,20]", ">20 (tail)"]
    colors = ["#16a34a", "#2563eb", "#f59e0b", "#dc2626"]
    axC = ax[2]
    xpos = np.arange(len(Ms))
    w = 0.2
    for k, (b, lab, c) in enumerate(zip(bands, labels, colors)):
        vals = [t[b] for t in tb]
        axC.bar(xpos + (k - 1.5) * w, vals, w, color=c, label=lab)
    axC.set_xticks(xpos); axC.set_xticklabels([f"M={int(m)}" for m in Ms])
    axC.set_ylabel("rel error of dense H(Ω̄)")
    axC.set_title("C. Core representable; tail is\ntruncation-limited (falls with M)")
    axC.legend(loc="upper right", fontsize=7.5, ncol=1)

    fig.suptitle("Phase-2 P2 — 1D Hou–Luo singular-profile machinery, validated against an exact solution "
                 "(reproduces a proven result: validation, not novelty)", fontsize=10.5, y=1.02)
    fig.tight_layout()
    out = FIGS / "fig12_p2_hl_anchor.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    else:
        if not JSON.exists():
            generate()
        build_figure()
