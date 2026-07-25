"""P2 B1 leg -- CHL Scenario 2 (arXiv:2604.01868, their (4.1)/(4.2)) at POC fidelity.

CHL Scenario 2: the modified rescaled HL system (4.1) (extra spatial-shift constant c_r),
normalized at the shifted ORIGIN by (4.2), relaxes generic non-symmetric positive data to
a strictly-POSITIVE REGULAR self-similar profile with contraction exponent
c_l/c_omega = -2.5114 (their Fig 4.2). Reproducing it is a Tier-2 consolidation (NOT novel,
NOT a proof); its value here is the VALIDATED origin-pinned gauge that a future gCLM
two-scale<->two-stage sweep needs to hold regular profiles peaked away from X=1.

The new machinery is RescaledHLScenario2 (origin-pinned 3-constant gauge, hand-rolled 3x3
solve), separately validated as a known-answer test (test_hl_rescaled.py 9/9: the (4.2) solve
nulls d_tau{Omega(0),Omega_X(0),V(0)} to machine precision).

WHAT A FIXED GRID CAN HONESTLY SAY (observed in the pre-run scratch, tau->71):
  * the amplitude-INVARIANT ratio c_l/c_omega converges to -2.524 (~0.5% off -2.5114);
  * the profile is strictly positive, regular, non-symmetric, peaked away from the origin;
  * the residual FLOORS at ~1e-2 (does NOT reach CHL's 1e-6 stopping criterion) and the
    ABSOLUTE (c_l,c_omega,c_r) drift slowly and stay off CHL's raw (1.0636,-0.4235,0.0765)
    -- they are IC-normalization-dependent; only the ratio + shape are gauge-invariant.

PRE-COMMITTED PREDICATE (locked in git before the logged run; gauge-invariant observables):
  S1  RATIO known-answer: from generic non-symmetric positive IC (x0=0.30) the relaxation
      reaches |c_l/c_omega - (-2.5114)| <= 0.05.
  S2  ATTRACTOR (IC-independent): a second IC (x0=0.45, different amplitude/width) reaches
      the same ratio within 0.05 of the first run's ratio.
  S3  REGULAR POSITIVE PROFILE: the converged Omega and V=Theta_X are strictly positive
      (min > 0), smooth (max|Omega_X|/peak(Omega) <= 5, vs ~1061 for the singular anchor),
      and peaked at X* > 0.15 (away from the origin, i.e. genuinely non-symmetric).
  S4  RESIDUAL BOUNDED + FALLING: residual drops >= 50x from its step-0 value and stays
      bounded (no blowup); the floor is REPORTED (not required to reach 1e-6).
  S5  HONEST CEILING (predicted): the residual FLOORS (final > 1e-4, i.e. does NOT meet
      CHL's 1e-6) AND the absolute c_l stays off CHL's raw value (c_l > 1.2 vs their 1.0636)
      -- the fixed-grid + IC-normalization boundary that CHL cross with an adaptive mesh.

Verdict PARTIAL by construction: S1-S4 are what a fixed-grid POC reaches (the invariant
exponent + a genuine attractor + a regular profile); S5 marks the boundary. Do NOT re-run to
chase a clause into a pass.

Run:  python experiments/p2_scenario2_relax.py --logged
Exploratory (short, non-logged):  python experiments/p2_scenario2_relax.py
"""

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.hl_rescaled import RescaledHLScenario2, scenario2_ic  # noqa: E402

RATIO_STAR = -2.5114
CHL_TRIPLE = (1.0636, -0.4235, 0.0765)


def run_relax(s2, Om0, V0, steps, dt_frac=0.3, cfl_every=200, record_every=400):
    """Relax (4.1) with adaptive dt (recompute CFL as the initial transient decays);
    record the gauge-invariant ratio and constant histories."""
    Om = np.array(Om0, dtype=float)
    V = np.array(V0, dtype=float)
    dt = dt_frac * s2.drho / max(s2.max_speed_rho(Om, V), 1e-6)
    tau = 0.0
    cl, cw, cr, rs, ks = [], [], [], [], []
    res0 = None
    c_l = c_omega = c_r = res = np.nan
    for k in range(steps):
        if k % cfl_every == 0 and k > 0:
            dt = dt_frac * s2.drho / max(s2.max_speed_rho(Om, V), 1e-6)
        Om, V, c_l, c_omega, c_r, res = s2.step(Om, V, dt)
        tau += dt
        if res0 is None:
            res0 = res
        if k % record_every == 0 or k == steps - 1:
            cl.append(c_l); cw.append(c_omega); cr.append(c_r); rs.append(res); ks.append(k)
        if not np.isfinite(res) or res > 1e8:
            cl.append(c_l); cw.append(c_omega); cr.append(c_r); rs.append(res); ks.append(k)
            break
    cl, cw, cr, rs, ks = map(np.array, (cl, cw, cr, rs, ks))
    tail = max(1, len(cl) // 5)
    c_l_f = float(np.mean(cl[-tail:])); c_om_f = float(np.mean(cw[-tail:]))
    peak = float(np.max(Om)); xstar = float(s2.X[int(np.argmax(Om))])
    Om_X = s2.dX(Om)
    return {
        "k": ks.tolist(), "c_l_hist": cl.tolist(), "c_omega_hist": cw.tolist(),
        "c_r_hist": cr.tolist(), "res_hist": rs.tolist(), "tau": float(tau),
        "steps_run": int(ks[-1]) + 1, "res0": float(res0), "res_final": float(rs[-1]),
        "c_l_final": c_l_f, "c_omega_final": c_om_f,
        "c_r_final": float(np.mean(cr[-tail:])), "ratio_final": c_l_f / c_om_f,
        "min_Omega": float(np.min(Om)), "min_V": float(np.min(V)),
        "peak_Omega": peak, "xstar": xstar,
        "smoothness": float(np.max(np.abs(Om_X)) / max(peak, 1e-30)),
        "blewup": bool((not np.isfinite(rs[-1])) or rs[-1] > 1e8),
        "Omega": Om.tolist(), "V": V.tolist(), "X": s2.X.tolist(),
    }


def evaluate(res):
    r1, r2 = res["ic_x0_30"], res["ic_x0_45"]
    C = {}
    C["S1_ratio_known_answer"] = abs(r1["ratio_final"] - RATIO_STAR) <= 0.05
    C["S2_attractor_same_ratio"] = abs(r2["ratio_final"] - r1["ratio_final"]) <= 0.05
    C["S3_regular_positive"] = (
        r1["min_Omega"] > 0.0 and r1["min_V"] > 0.0 and
        r1["smoothness"] <= 5.0 and r1["xstar"] > 0.15)
    C["S4_residual_falls_bounded"] = (
        (not r1["blewup"]) and r1["res0"] / max(r1["res_final"], 1e-30) >= 50.0)
    C["S5_honest_ceiling"] = (r1["res_final"] > 1e-4) and (r1["c_l_final"] > 1.2)
    return C


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--logged", action="store_true")
    ap.add_argument("--n", type=int, default=801)
    ap.add_argument("--steps", type=int, default=24000)
    args = ap.parse_args()

    if args.logged:
        import json
        from pathlib import Path
        DATA = Path(__file__).resolve().parent.parent / "writeup" / "data"
        DATA.mkdir(parents=True, exist_ok=True)
        n, steps = args.n, args.steps
        print(f"LOGGED Scenario-2 relaxation: n={n} steps={steps} "
              f"ratio target {RATIO_STAR}", flush=True)
        s2 = RescaledHLScenario2(n=n, c=0.35, rho_max=7.0, nu=0.02)
        results = {}
        print("  [IC x0=0.30] ...", flush=True)
        results["ic_x0_30"] = run_relax(s2, *scenario2_ic(s2.X, x0=0.30), steps)
        print("  [IC x0=0.45] ...", flush=True)
        results["ic_x0_45"] = run_relax(s2, *scenario2_ic(s2.X, x0=0.45, w=1.1), steps)
        checks = evaluate(results)
        payload = {
            "ratio_target": RATIO_STAR, "chl_triple": CHL_TRIPLE,
            "config": {"n": n, "c": 0.35, "rho_max": 7.0, "nu": 0.02,
                       "steps": steps, "dt_frac": 0.3},
            "results": results, "predicate_checks": checks,
        }
        (DATA / "p2_scenario2_relax.json").write_text(json.dumps(payload))
        print("\n--- summary (ratio, c_l, c_omega, c_r, res0->final, xstar, smooth) ---")
        for name, r in results.items():
            print(f"  {name:9s} ratio={r['ratio_final']:+.4f} "
                  f"c_l={r['c_l_final']:+.3f} c_om={r['c_omega_final']:+.3f} "
                  f"c_r={r['c_r_final']:+.3f} res {r['res0']:.1e}->{r['res_final']:.1e} "
                  f"x*={r['xstar']:.2f} smooth={r['smoothness']:.2f} "
                  f"minOm={r['min_Omega']:.2e}", flush=True)
        print("\n--- PRE-COMMITTED PREDICATE ---")
        for k, v in checks.items():
            print(f"    {'PASS' if v else 'FAIL'}  {k}")
        npass = sum(checks.values())
        print(f"\nVERDICT: PARTIAL by construction -- {npass}/{len(checks)} clauses hold "
              f"(S1-S4 = invariant exponent + attractor + regular profile at POC; "
              f"S5 = documented fixed-grid/normalization ceiling).")
        print(f"wrote {DATA/'p2_scenario2_relax.json'}")
    else:
        s2 = RescaledHLScenario2(n=801, c=0.35, rho_max=7.0, nu=0.02)
        r = run_relax(s2, *scenario2_ic(s2.X, x0=0.30), min(args.steps, 3000))
        print(f"EXPLORATORY: ratio={r['ratio_final']:+.4f} c_l={r['c_l_final']:+.3f} "
              f"c_om={r['c_omega_final']:+.3f} res {r['res0']:.1e}->{r['res_final']:.1e} "
              f"x*={r['xstar']:.2f} minOm={r['min_Omega']:.2e}")
