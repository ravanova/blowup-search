"""Diagnose the Step-C drift: does the c_l drift RATE scale with a boundary/grid parameter?
Runs short relaxations for a few configs and reports the drift rate (linear fit of c_l over a
mid-run window, skipping the initial transient) + the residual level. If the drift rate scales
with r_min -> the inner (inflow) boundary leak is the culprit; if with r_max -> far field; if it
shrinks under n_r/n_beta refinement -> a truncation error; if invariant -> a genuine mode.
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.boussinesq_velocity import PolarGrid  # noqa: E402
from solver.boussinesq_rescaled import RescaledBoussinesq, CL_STAR  # noqa: E402
from experiments.spike1_stepC_gate import profile_ansatz  # noqa: E402


def run_short(n_r, n_beta, r_min, r_max, steps=1500, dt_frac=0.3, sample=50):
    grid = PolarGrid(n_r=n_r, n_beta=n_beta, r_min=r_min, r_max=r_max)
    om, et, xi = profile_ansatz(grid)
    solver = RescaledBoussinesq(grid)
    cls, ress, ks = [], [], []
    for k in range(steps + 1):
        Ro, Re, Rx, info = solver.rhs(om, et, xi)
        if k % sample == 0:
            cls.append(info["c_l"])
            ress.append(max(np.abs(Ro).max(), np.abs(Re).max(), np.abs(Rx).max()))
            ks.append(k)
        dt = dt_frac / info["cfl_speed"]
        om, et, xi, _, _ = solver.step(om, et, xi, dt)
    ks, cls, ress = np.array(ks), np.array(cls), np.array(ress)
    m = ks >= steps // 3  # skip initial transient
    slope = np.polyfit(ks[m], cls[m], 1)[0]  # dc_l per step
    return dict(drift_per1k=slope * 1000, c_l_start=cls[0], c_l_end=cls[-1],
                res_end=ress[-1], res_min=ress.min())


def report(tag, cfg, r):
    print(f"[{tag:16s}] {cfg:38s} drift/1k={r['drift_per1k']:+.4f}  "
          f"c_l {r['c_l_start']:.3f}->{r['c_l_end']:.3f}  res_end={r['res_end']:.2e}")


if __name__ == "__main__":
    print(f"# target c_l = {CL_STAR:.4f}; a healthy config should have drift/1k ~ 0\n")
    STEPS = int(os.environ.get("STEPS", 1500))

    print("--- vary r_min (inner inflow BC hypothesis), r_max=1e5 n_r=300 n_beta=48 ---")
    for r_min in (1e-3, 1e-4, 1e-5):
        report(f"r_min={r_min:.0e}", f"r_min={r_min:.0e} r_max=1e5 n_r=300",
               run_short(300, 48, r_min, 1e5, STEPS))

    print("\n--- vary r_max (far-field hypothesis), r_min=1e-4 n_r=300 n_beta=48 ---")
    for r_max in (1e4, 1e6):
        report(f"r_max={r_max:.0e}", f"r_min=1e-4 r_max={r_max:.0e} n_r=300",
               run_short(300, 48, 1e-4, r_max, STEPS))

    print("\n--- refine n_r (truncation hypothesis), r_min=1e-4 r_max=1e5 ---")
    for n_r in (450,):
        report(f"n_r={n_r}", f"r_min=1e-4 r_max=1e5 n_r={n_r}",
               run_short(n_r, 48, 1e-4, 1e5, STEPS))
