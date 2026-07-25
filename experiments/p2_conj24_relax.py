"""P2 novelty leg -- Conjecture 2.4 (Chen-Huang-Li arXiv:2604.01868) at POC fidelity.

Conjecture 2.4 (CHL): the singular steady state (Omega_bar, Theta_bar, c_l=2, c_omega=-1)
of the rescaled Hou-Luo system (2.4) is ASYMPTOTICALLY STABLE -- generic smooth degenerate
data converges to it. CHL assert this numerically only; reproducing it is a Tier-2-style
independent confirmation (NOT novel, NOT a proof).

This harness tests what a fixed-grid POC can honestly say. The genuinely new machinery is
the degenerate normalization gauge (CHL (3.2)), separately validated as a known-answer test
(test_hl_rescaled.py 7/7). Here we time-step the dissipation-stabilized dynamics
(RescaledHLDynamic, nu>0 -- required: the non-dissipative scheme rings at the X=1
discontinuity of the singular profile and blows up).

PRE-COMMITTED PREDICATE (locked in git before the logged run; gauge-invariant only):
  P1  fixed-point consistency: initialized at the regularized Thm-2.3 anchor, over the
      final third of the run the gauge constants satisfy |c_l-2|<=0.15 AND |c_omega+1|<=0.15
      and the residual is BOUNDED (final <= initial; no blowup). A stable HOLD at a nonzero
      residual floor -- explicitly NOT convergence-to-zero.
  P2  local stability: two distinct smooth perturbations of the anchor each relax to
      |c_l-2|<=0.15 AND |c_omega+1|<=0.15, ending within 0.06 of the unperturbed endpoint in
      BOTH constants (same fixed point), with residual dropping >=5x from its step-0 value.
  P3  robustness to the stabilizer (not a one-nu artifact): across nu in {0.02, 0.04} the
      held (c_l,c_omega) stay within 0.15 of (2,-1). The residual floor vs nu is REPORTED
      (not a pass/fail).
  P4  HONEST NEGATIVE (predicted): a generic far smooth degenerate IC does NOT reach the
      anchor gauge at this POC fidelity (ends |c_l-2|>0.3) -- the GLOBAL basin (the strong
      form of Conjecture 2.4) is beyond a fixed-grid POC and needs the heavier numerics
      (WENO/adaptive mesh, vanishing viscosity, semi-analytic tail patch) CHL used.

Overall verdict is PARTIAL by construction: P1-P3 are the LOCAL-attractor content that a
POC can reach; P4 marks the boundary. Do NOT re-run to chase a clause into a pass -- report
PARTIAL and locate the cause.

Run:  python experiments/p2_conj24_relax.py --logged
Exploratory (short, non-logged):  python experiments/p2_conj24_relax.py
"""

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.hl_rescaled import (  # noqa: E402
    RescaledHLDynamic, omega_bar, degenerate_ic,
)

PI = np.pi
CL_STAR, COMEGA_STAR = 2.0, -1.0


def reg_anchor(X, a=0.05, w=0.08):
    """Regularised Thm-2.3 anchor: Omega=(X-1)^{-1/2} capped at (X-1)=a near the
    singular point; Theta a tanh step of width w. (The exact anchor is +infinity at
    X=1, so a finite cap is unavoidable on any grid.)"""
    Om = np.where(X > 1.0, (np.maximum(X - 1.0, a)) ** (-0.5), 0.0)
    Th = (PI / 2.0) * 0.5 * (1.0 + np.tanh((X - 1.0) / w))
    return Om, Th


def run_relax(d, Om0, Th0, steps, dt_frac=0.15, record_every=100):
    """Relax with fixed dt (set from the initial CFL); record gauge + residual histories."""
    Om = d.normalize_amp(np.array(Om0, dtype=float))
    Th = np.array(Th0, dtype=float)
    dt = dt_frac * d.ds / max(d.max_speed_s(Om), 1e-6)
    cl, cw, rs, ks = [], [], [], []
    res0 = None
    for k in range(steps):
        Om, Th, c_l, c_omega, res = d.step(Om, Th, dt)
        Om = d.normalize_amp(Om)
        if res0 is None:
            res0 = res
        if k % record_every == 0 or k == steps - 1:
            cl.append(c_l); cw.append(c_omega); rs.append(res); ks.append(k)
        if not np.isfinite(res) or res > 1e8:
            cl.append(c_l); cw.append(c_omega); rs.append(res); ks.append(k)
            break
    cl, cw, rs, ks = map(np.array, (cl, cw, rs, ks))
    tail = max(1, len(cl) // 3)
    return {
        "k": ks.tolist(), "c_l_hist": cl.tolist(), "c_omega_hist": cw.tolist(),
        "res_hist": rs.tolist(), "dt": dt, "steps_run": int(ks[-1]) + 1,
        "res0": float(res0), "res_final": float(rs[-1]),
        "c_l_final": float(np.mean(cl[-tail:])), "c_omega_final": float(np.mean(cw[-tail:])),
        "res_floor": float(np.median(rs[-tail:])),
        "shape_relL2": shape_relL2(d, Om),
        "blewup": bool((not np.isfinite(rs[-1])) or rs[-1] > 1e8),
    }


def shape_relL2(d, Om):
    """Relative L2 distance of the held Omega to the amplitude-matched anchor, on a
    band away from the singular cap and the far tail (where the POC error concentrates)."""
    X = d.X
    band = (X > 1.15) & (X < 6.0)
    ref = omega_bar(X)
    a = np.dot(Om[band], ref[band]) / max(np.dot(ref[band], ref[band]), 1e-30)  # best scale
    num = np.linalg.norm(Om[band] - a * ref[band])
    den = np.linalg.norm(a * ref[band]) + 1e-30
    return float(num / den)


def evaluate(res):
    """Apply the locked predicate to the results dict; return (verdict, checks)."""
    hold = res["hold_nu02"]
    p_a, p_b = res["pert_plus"], res["pert_minus"]
    hold4 = res["hold_nu04"]
    gen = res["generic"]
    C = {}
    # P1
    C["P1_anchor_c_l"] = abs(hold["c_l_final"] - CL_STAR) <= 0.15
    C["P1_anchor_c_omega"] = abs(hold["c_omega_final"] - COMEGA_STAR) <= 0.15
    C["P1_anchor_bounded"] = (not hold["blewup"]) and hold["res_final"] <= hold["res0"]
    # P2
    def relaxed(r):
        return (abs(r["c_l_final"] - CL_STAR) <= 0.15 and
                abs(r["c_omega_final"] - COMEGA_STAR) <= 0.15 and
                r["res0"] / max(r["res_floor"], 1e-30) >= 5.0)
    same = (abs(p_a["c_l_final"] - hold["c_l_final"]) <= 0.06 and
            abs(p_a["c_omega_final"] - hold["c_omega_final"]) <= 0.06 and
            abs(p_b["c_l_final"] - hold["c_l_final"]) <= 0.06 and
            abs(p_b["c_omega_final"] - hold["c_omega_final"]) <= 0.06)
    C["P2_pert_plus_relaxes"] = relaxed(p_a)
    C["P2_pert_minus_relaxes"] = relaxed(p_b)
    C["P2_same_fixed_point"] = same
    # P3
    C["P3_robust_c_l"] = abs(hold4["c_l_final"] - CL_STAR) <= 0.15
    C["P3_robust_c_omega"] = abs(hold4["c_omega_final"] - COMEGA_STAR) <= 0.15
    # P4 (honest negative -- PASS means the predicted negative held)
    C["P4_generic_basin_negative"] = abs(gen["c_l_final"] - CL_STAR) > 0.3
    return C


def make_solver(n, nu):
    return RescaledHLDynamic(n=n, delta=0.02, M=150.0, nu=nu)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--logged", action="store_true")
    ap.add_argument("--n", type=int, default=801)
    ap.add_argument("--steps", type=int, default=2500)
    args = ap.parse_args()

    if args.logged:
        import json
        from pathlib import Path
        DATA = Path(__file__).resolve().parent.parent / "writeup" / "data"
        DATA.mkdir(parents=True, exist_ok=True)
        n, steps = args.n, args.steps
        print(f"LOGGED Conjecture-2.4 relaxation: n={n} steps={steps} "
              f"targets (c_l,c_om)=({CL_STAR},{COMEGA_STAR})", flush=True)

        d2 = make_solver(n, nu=0.02)
        Om0, Th0 = reg_anchor(d2.X)
        pert_p = 0.4 * np.exp(-((d2.X - 1.6) ** 2) / 0.25)
        pert_m = -0.3 * np.exp(-((d2.X - 1.4) ** 2) / 0.20)

        results = {}
        print("  [hold nu=0.02] ...", flush=True)
        results["hold_nu02"] = run_relax(d2, Om0, Th0, steps)
        print("  [pert+ nu=0.02] ...", flush=True)
        results["pert_plus"] = run_relax(d2, Om0 * (1 + pert_p), Th0, steps)
        print("  [pert- nu=0.02] ...", flush=True)
        results["pert_minus"] = run_relax(d2, Om0 * (1 + pert_m), Th0, steps)

        d4 = make_solver(n, nu=0.04)
        print("  [hold nu=0.04] ...", flush=True)
        results["hold_nu04"] = run_relax(d4, *reg_anchor(d4.X), steps)

        print("  [generic degenerate IC nu=0.02] ...", flush=True)
        gOm, gTh = degenerate_ic(d2.X, kind="A")
        results["generic"] = run_relax(d2, gOm, gTh, steps)

        checks = evaluate(results)
        payload = {
            "targets": {"c_l": CL_STAR, "c_omega": COMEGA_STAR},
            "config": {"n": n, "delta": 0.02, "M": 150.0, "steps": steps,
                       "dt_frac": 0.15, "nu_main": 0.02, "nu_robust": 0.04},
            "results": results, "predicate_checks": checks,
        }
        (DATA / "p2_conj24_relax.json").write_text(json.dumps(payload))

        print("\n--- summary (c_l_final, c_omega_final, res0->floor, shape_relL2) ---")
        for name, r in results.items():
            print(f"  {name:11s} c_l={r['c_l_final']:+.3f} c_om={r['c_omega_final']:+.3f} "
                  f"res {r['res0']:.1e}->{r['res_floor']:.1e} shape={r['shape_relL2']:.3f} "
                  f"blewup={r['blewup']}", flush=True)
        print("\n--- PRE-COMMITTED PREDICATE ---")
        for k, v in checks.items():
            print(f"    {'PASS' if v else 'FAIL'}  {k}")
        npass = sum(checks.values())
        print(f"\nVERDICT: PARTIAL by construction -- {npass}/{len(checks)} clauses hold "
              f"(P1-P3 = local attractor at POC; P4 = documented basin boundary).")
        print(f"wrote {DATA/'p2_conj24_relax.json'}")
    else:
        d = make_solver(args.n, nu=0.02)
        r = run_relax(d, *reg_anchor(d.X), min(args.steps, 800))
        print(f"EXPLORATORY hold: c_l={r['c_l_final']:+.3f} c_om={r['c_omega_final']:+.3f} "
              f"res {r['res0']:.1e}->{r['res_floor']:.1e} shape={r['shape_relL2']:.3f}")
