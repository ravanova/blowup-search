"""Phase-2 P2 evidence: the rescaled HL system (2.4) has TWO fixed points, and our
existing degenerate-gauge machinery reaches BOTH.

  * hold (from the regularised Thm-2.3 anchor)  -> the SINGULAR profile
        (X-1)^{-1/2} 1_{X>1}, (c_l,c_omega) ~ (2,-1): Chen-Huang-Li's Stage-2 attractor.
  * generic degenerate IC (kind A)              -> a REGULAR, strictly-positive profile,
        smooth, peaked AWAY from X=1: qualitatively CHL's Stage-1 / Scenario-2 object
        ("a non-symmetric regular profile that remains strictly positive throughout",
        their Sec. 4).

This UPGRADES the Conjecture-2.4 logged run's "generic -> different self-similar state"
clause: that state is NOT a POC artifact -- it is the regular fixed point, the first
half of CHL's two-STAGE structure, captured independently.

HONEST SCOPE (do not oversell):
  * Reached with the standard (2.4)+degenerate-gauge, NOT CHL's modified Scenario-2
    formulation (2.9)/(4.1) (which carries a third constant c_r + a different
    normalization). So this is NOT proven identical to their Scenario-2 profile: the
    match is QUALITATIVE (strictly positive, regular, peak off the singular point).
    Raw constants differ (ours c_l~0.5-0.7, c_om~-0.45; theirs 1.0636,-0.4235) as
    expected under a different normalization -- identity needs (4.1) + a shape overlay.
  * Not converged: c_omega drifts, residual plateaus at the POC floor. A regular
    ATTRACTING region, not a pinned fixed point.
  * Not novel, not a proof: reproduces (qualitatively) a CHL object.

The 8000-step generic trajectory (panel C) sharpens the story: under the standard
degenerate gauge the trajectory TRANSITS the CHL Scenario-2 neighborhood (c_l~1.06,
c_om~-0.42 near step 1200) but CANNOT hold it -- our gauge pins c_l=-U(1) (stagnation
at X=1), a MISMATCH for a regular profile peaked at X~0.35 -- and then WANDERS in the
low-c_l regular regime (res floor ~0.12), never approaching the singular anchor c_l=2.
This (a) shows CHL's modified normalization (4.2), which pins behavior at the ORIGIN,
is the right stabilizer -> a clean next brick (implement (4.1)/(4.2), known-answer
(c_l,c_om,c_r)=(1.0636,-0.4235,0.0765)); and (b) shows the Stage-1->Stage-2 transition
is NOT reachable on this fixed grid (it needs the adaptive-mesh rebuild).

Data (committed; the figures rebuild from it without re-running):
    .venv/bin/python writeup/p2_regular_profile_evidence.py --generate  # writes
        writeup/data/p2_regular_profile.json       (two fixed-point fields, ~4 min)
    .venv/bin/python writeup/p2_regular_profile_evidence.py --generate-traj  # writes
        writeup/data/p2_regular_profile_traj.json  (8000-step generic trajectory, ~12 min)
    .venv/bin/python writeup/p2_regular_profile_evidence.py             # builds
        writeup/figures/fig14_p2_regular_profile.png  from the committed JSONs

See ../PHASE2_P2_NOTES.md (Section 7) and writeup/TECHNICAL_P2_CONJ24.md.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(__file__).resolve().parents[1] / "data"
FIGS = Path(__file__).resolve().parents[1] / "figures"
DATA.mkdir(parents=True, exist_ok=True)
FIGS.mkdir(parents=True, exist_ok=True)
JSON = DATA / "p2_regular_profile.json"
TRAJ = DATA / "p2_regular_profile_traj.json"

# CHL Fig 4.2 Scenario-2 limiting constants (their MODIFIED formulation (4.1))
CHL_S2 = {"c_l": 1.0636, "c_omega": -0.4235, "c_r": 0.0765, "c_l_over_c_omega": -2.5114}
PI = np.pi
N, DELTA, M, NU, STEPS = 801, 0.02, 150.0, 0.02, 2500


def _reg_anchor(X, a=0.05, w=0.08):
    Om = np.where(X > 1.0, (np.maximum(X - 1.0, a)) ** (-0.5), 0.0)
    Th = (PI / 2.0) * 0.5 * (1.0 + np.tanh((X - 1.0) / w))
    return Om, Th


def _relax_final(d, Om0, Th0, steps=STEPS, dt_frac=0.15):
    Om = d.normalize_amp(np.array(Om0, float))
    Th = np.array(Th0, float)
    dt = dt_frac * d.ds / max(d.max_speed_s(Om), 1e-6)
    c_l = c_om = res = float("nan")
    for _ in range(steps):
        Om, Th, c_l, c_om, res = d.step(Om, Th, dt)
        Om = d.normalize_amp(Om)
        if not np.isfinite(res) or res > 1e8:
            break
    return Om, Th, float(c_l), float(c_om), float(res)


def _diagnose(d, Om, omega_bar):
    """Regular-vs-singular diagnostics (gauge-invariant shape character)."""
    X = d.X
    band = (X > 0.05) & (X < 12.0)
    Xi, Oi = X[band], Om[band]
    ipk = int(np.argmax(np.abs(Oi)))
    Xpk, Opk = float(Xi[ipk]), float(Oi[ipk])
    frac_pos = float(np.mean((Oi / abs(Opk)) > 0.02))
    frac_neg = float(np.mean((Oi / abs(Opk)) < -0.02))
    slopes = d.dX(Om) / abs(Opk)
    max_slope_near1 = float(np.max(np.abs(slopes[(X > 0.9) & (X < 1.3)])))
    b2 = (X > 1.2) & (X < 6.0)
    ref = omega_bar(X)
    a = np.dot(Om[b2], ref[b2]) / max(np.dot(ref[b2], ref[b2]), 1e-30)
    sing_relL2 = float(np.linalg.norm(Om[b2] - a * ref[b2]) /
                       (np.linalg.norm(a * ref[b2]) + 1e-30))
    return {"Xpk": Xpk, "Opk": Opk, "peak_at_one": bool(abs(Xpk - 1.0) < 0.15),
            "frac_pos": frac_pos, "frac_neg": frac_neg,
            "single_signed": bool(frac_pos < 0.02 or frac_neg < 0.02),
            "max_slope_near1": max_slope_near1, "sing_relL2": sing_relL2}


def generate():
    os.environ.setdefault("OMP_NUM_THREADS", "8")
    sys.path.insert(0, str(ROOT))
    from solver.hl_rescaled import RescaledHLDynamic, omega_bar, degenerate_ic

    d = RescaledHLDynamic(n=N, delta=DELTA, M=M, nu=NU)
    out = {"config": {"n": N, "delta": DELTA, "M": M, "nu": NU, "steps": STEPS},
           "chl_scenario2": CHL_S2, "runs": {}}

    print("[hold -> singular anchor] ...", flush=True)
    Om, Th, cl, cw, r = _relax_final(d, *_reg_anchor(d.X))
    out["runs"]["hold"] = {"X": d.X.tolist(), "Om": Om.tolist(), "Th": Th.tolist(),
                           "c_l": cl, "c_omega": cw, "res": r,
                           **_diagnose(d, Om, omega_bar)}
    print("[generic degenerate IC kind A -> regular] ...", flush=True)
    gOm, gTh = degenerate_ic(d.X, kind="A")
    Om, Th, cl, cw, r = _relax_final(d, gOm, gTh)
    out["runs"]["generic"] = {"X": d.X.tolist(), "Om": Om.tolist(), "Th": Th.tolist(),
                              "c_l": cl, "c_omega": cw, "res": r,
                              **_diagnose(d, Om, omega_bar)}
    JSON.write_text(json.dumps(out))
    print(f"wrote {JSON}")


def generate_traj(steps=8000, record_every=200):
    os.environ.setdefault("OMP_NUM_THREADS", "8")
    sys.path.insert(0, str(ROOT))
    from solver.hl_rescaled import RescaledHLDynamic, degenerate_ic

    d = RescaledHLDynamic(n=N, delta=DELTA, M=M, nu=NU)
    Om, Th = degenerate_ic(d.X, kind="A")
    Om = d.normalize_amp(np.array(Om, float)); Th = np.array(Th, float)
    dt = 0.15 * d.ds / max(d.max_speed_s(Om), 1e-6)
    hist = []
    for k in range(steps):
        Om, Th, c_l, c_om, res = d.step(Om, Th, dt)
        Om = d.normalize_amp(Om)
        if k % record_every == 0 or k == steps - 1:
            hist.append((k, float(c_l), float(c_om), float(res)))
            print(f"step {k:5d} c_l={c_l:+.4f} c_om={c_om:+.4f} res={res:.3e}", flush=True)
        if not np.isfinite(res) or res > 1e8:
            break
    TRAJ.write_text(json.dumps({"hist": hist, "steps": steps}))
    print(f"wrote {TRAJ}")


def build_figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = json.loads(JSON.read_text())
    H, G = d["runs"]["hold"], d["runs"]["generic"]
    s2 = d["chl_scenario2"]
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.25, "axes.axisbelow": True,
        "legend.frameon": False,
    })
    fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.4))

    for a, r, title, col in [
        (ax[0], H, "A. SINGULAR fixed point (Stage 2)\nfrom the regularised Thm-2.3 anchor", "#dc2626"),
        (ax[1], G, "B. REGULAR fixed point (Stage 1?)\nfrom generic degenerate data", "#2563eb")]:
        X = np.array(r["X"]); Om = np.array(r["Om"])
        m = (X > -0.3) & (X < 6.0)
        a.plot(X[m], Om[m], color=col, lw=1.8)
        a.axvline(1.0, color="#9ca3af", ls="--", lw=1.0)
        a.set_xlabel("X"); a.set_ylabel(r"$\Omega$")
        a.set_title(title)
        a.annotate(f"peak at X={r['Xpk']:.2f}\nmax|$\\Omega_X$|/peak≈{r['max_slope_near1']:.0f}\n"
                   f"single-signed: {r['single_signed']}\n"
                   f"$(c_\\ell,c_\\omega)$=({r['c_l']:.2f},{r['c_omega']:.2f})",
                   xy=(0.97, 0.95), xycoords="axes fraction", ha="right", va="top",
                   fontsize=8.5, bbox=dict(boxstyle="round", fc="white", ec="0.8"))
    ax[1].annotate(
        "CHL Scenario 2 (their (4.1), a DIFFERENT normalization):\n"
        f"$(c_\\ell,c_\\omega,c_r)$=({s2['c_l']},{s2['c_omega']},{s2['c_r']}), "
        f"$c_\\ell/c_\\omega$={s2['c_l_over_c_omega']}\n"
        "match here is QUALITATIVE (regular, +ve, peak off X=1)",
        xy=(0.5, -0.34), xycoords="axes fraction", ha="center", va="top", fontsize=8,
        color="#374151")

    # panel C: the 8000-step generic trajectory transits CHL-S2 then wanders (never -> 2)
    axC = ax[2]
    if TRAJ.exists():
        t = json.loads(TRAJ.read_text())
        hist = np.array(t["hist"])
        ks, cl, cw = hist[:, 0], hist[:, 1], hist[:, 2]
        axC.plot(ks, cl, color="#2563eb", lw=1.5, label=r"$c_\ell$")
        axC.plot(ks, cw, color="#16a34a", lw=1.5, label=r"$c_\omega$")
        axC.axhline(s2["c_l"], color="#f59e0b", ls=":", lw=1.2)
        axC.axhline(s2["c_omega"], color="#f59e0b", ls=":", lw=1.2)
        axC.axhline(2.0, color="#dc2626", ls="--", lw=1.0)
        axC.annotate("CHL-S2 $c_\\ell$=1.06 (transited, not held)", xy=(ks[-1], s2["c_l"]),
                     xytext=(ks[-1]*0.35, 1.35), fontsize=8, color="#b45309")
        axC.annotate("singular anchor $c_\\ell$=2 (never approached)", xy=(ks[-1]*0.5, 2.0),
                     xytext=(ks[-1]*0.28, 1.72), fontsize=8, color="#dc2626")
        axC.set_xlabel("step"); axC.set_ylabel(r"gauge constants")
        axC.set_title("C. Generic trajectory (8000 steps):\ntransits CHL-S2, then wanders (regular regime)")
        axC.legend(loc="center right", fontsize=8.5)
    else:
        axC.text(0.5, 0.5, "run --generate-traj for panel C", ha="center", va="center")

    fig.suptitle("Phase-2 P2 — the rescaled HL system (2.4) has TWO fixed points; our degenerate-gauge "
                 "machinery reaches the regular one qualitatively (CHL Stage-1).\nThe logged run's "
                 "'different state' is NOT an artifact. But the gauge can't HOLD it (panel C) → CHL's (4.2) "
                 "origin-normalization is the fix. Not identical to CHL Scenario 2; not novel; not a proof.",
                 fontsize=9.4, y=1.07)
    fig.tight_layout()
    out = FIGS / "fig14_p2_regular_profile.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    if "--generate" in sys.argv:
        generate()
    elif "--generate-traj" in sys.argv:
        generate_traj()
    else:
        if not JSON.exists():
            generate()
        build_figure()
