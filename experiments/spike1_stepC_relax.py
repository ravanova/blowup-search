"""Long background relaxation driver for Spike-1 Step C (exploratory / dev, non-logged).
Steps the rescaled system and logs rich diagnostics every CHUNK steps so the trajectory can
be monitored: residual, c_l drift (should stay pinned at the gauge), c_omega, alpha=c_omega/c_l,
the FAR-FIELD radial exponent (should relax to alpha), and field extrema. Writes to stdout
(capture with run_in_background)."""

import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from solver.boussinesq_velocity import PolarGrid  # noqa: E402
from solver.boussinesq_rescaled import (  # noqa: E402
    RescaledBoussinesq, CL_STAR, COMEGA_STAR, ALPHA_STAR,
)
from experiments.spike1_stepC_gate import profile_ansatz, radial_exponent  # noqa: E402

N_R = int(os.environ.get("N_R", 300))
N_BETA = int(os.environ.get("N_BETA", 48))
R_MAX = float(os.environ.get("R_MAX", 1e5))
MAX_STEPS = int(os.environ.get("MAX_STEPS", 20000))
CHUNK = int(os.environ.get("CHUNK", 500))
DT_FRAC = float(os.environ.get("DT_FRAC", 0.3))
TOL = float(os.environ.get("TOL", 1e-6))

grid = PolarGrid(n_r=N_R, n_beta=N_BETA, r_min=1e-4, r_max=R_MAX)
om, et, xi = profile_ansatz(grid)
solver = RescaledBoussinesq(grid)

print(f"# relax n_r={N_R} n_beta={N_BETA} r_max={R_MAX:.0e} dt_frac={DT_FRAC} "
      f"targets: c_l={CL_STAR:.4f} c_om={COMEGA_STAR:.4f} alpha={ALPHA_STAR:.4f}", flush=True)
print(f"# {'step':>6} {'tau':>8} {'res':>10} {'c_l':>9} {'c_om':>9} {'alpha':>9} "
      f"{'a_far':>9} {'om_min':>10} {'om_max':>10}", flush=True)

t0 = time.time()
tau = 0.0
for step in range(MAX_STEPS + 1):
    Ro, Re, Rx, info0 = solver.rhs(om, et, xi)
    dt = DT_FRAC / info0["cfl_speed"]
    if step % CHUNK == 0:
        a = info0["c_omega"] / info0["c_l"]
        a_far = radial_exponent(om, grid, r_lo=R_MAX ** 0.35, r_hi=R_MAX ** 0.75)
        res = max(np.abs(Ro).max(), np.abs(Re).max(), np.abs(Rx).max())
        print(f"  {step:>6} {tau:>8.2f} {res:>10.2e} {info0['c_l']:>9.5f} "
              f"{info0['c_omega']:>9.5f} {a:>9.5f} {a_far:>9.4f} "
              f"{om.min():>10.3e} {om.max():>10.3e}", flush=True)
        if res < TOL:
            print(f"# CONVERGED at step {step} ({time.time()-t0:.0f}s)", flush=True)
            break
        if not np.isfinite(res) or res > 1e6:
            print(f"# DIVERGED at step {step}", flush=True)
            break
    om, et, xi, _, _ = solver.step(om, et, xi, dt)
    tau += dt

np.savez(os.path.join(os.path.dirname(__file__), "spike1_stepC_state.npz"),
         omega=om, eta=et, xi=xi, r=grid.r, beta=grid.beta, R=grid.R, B=grid.B,
         c_l=info0["c_l"], c_omega=info0["c_omega"], n_r=N_R, n_beta=N_BETA, r_max=R_MAX)
print(f"# done {time.time()-t0:.0f}s, saved state", flush=True)
