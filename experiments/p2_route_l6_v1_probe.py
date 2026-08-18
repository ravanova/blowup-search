"""Leg 401, unit L6 -- CONVERGENCE PROBE (not a result-producing script).

Purpose: the pre-registration (leg_401.md SS5) fixes `maxiter = 20000`.  This probe measures
how many L-BFGS-B iterations are actually USED before the pre-registered `ftol = 1e-16` /
`gtol = 1e-12` stopping tests fire, at two rungs of the joint ladder, so that any cap
imposed for wall-clock reasons is chosen from a MEASUREMENT and reported as a cost under
pre-committed reading (d) rather than guessed.

It writes no artefact and produces no gate number.
"""

from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2_route_l6_v1 as L6  # noqa: E402

OUTDIR = Path(__file__).resolve().parents[1] / "experiments" / "_l6_probe"


def one(task):
    tag, Lmax, Nr, Ks, branch, seed, maxiter = task
    g = L6.Geom(Lmax, Nr, Ks, 2.0)
    rng = np.random.default_rng(seed)
    x0 = L6.normalise(g, rng.standard_normal(g.n_dof) * 0.1, branch)
    traj = []
    t0 = time.time()
    state = dict(k=0)

    OUTDIR.mkdir(exist_ok=True)
    live = OUTDIR / f"live_{tag}_{branch}_{seed}.txt"
    live.write_text("")

    def cb(xk):
        state["k"] += 1
        if state["k"] % 25 == 0 or state["k"] <= 5:
            f, gr = L6.objective(g, xk, branch)
            rec = (state["k"], round(time.time() - t0, 1), f,
                   float(np.max(np.abs(gr))))
            traj.append(rec)
            with live.open("a") as fh:   # flush as we go: the plateau must be watchable
                fh.write("%d %.1f %.12e %.6e\n" % rec)

    r = minimize(lambda z: L6.objective(g, z, branch), x0, jac=True, method="L-BFGS-B",
                 callback=cb,
                 options=dict(maxiter=maxiter, maxfun=maxiter * 2, ftol=1e-16, gtol=1e-12))
    out = dict(tag=tag, Lmax=Lmax, Nr=Nr, Ks=Ks, branch=branch, seed=seed,
               n_dof=g.n_dof, maxiter=maxiter, nit=int(r.nit), nfev=int(r.nfev),
               status=int(r.status), message=str(r.message),
               fun=float(r.fun), max_abs_grad=float(np.max(np.abs(r.jac))),
               seconds=round(time.time() - t0, 1),
               sec_per_iter=round((time.time() - t0) / max(1, int(r.nit)), 4),
               trajectory=traj)
    OUTDIR.mkdir(exist_ok=True)
    (OUTDIR / f"probe_{tag}_{branch}_{seed}.json").write_text(json.dumps(out, indent=1))
    print(f"[{tag} {branch}] nit={r.nit} status={r.status} J={r.fun:.6e} "
          f"|g|inf={np.max(np.abs(r.jac)):.2e} {out['seconds']}s "
          f"({out['sec_per_iter']}s/it)  {r.message}", flush=True)
    return out


MAXIT = int(os.environ.get("L6_PROBE_MAXITER", "20000"))
TASKS = [
    ("J0", 2, 8, 1, "B", 401, MAXIT),
    ("J2", 3, 12, 2, "B", 401, MAXIT),
    ("J0", 2, 8, 1, "A", 401, MAXIT),
    ("J2", 3, 12, 2, "A", 401, MAXIT),
]

if __name__ == "__main__":
    OUTDIR.mkdir(exist_ok=True)
    with mp.get_context("fork").Pool(4) as pool:
        res = pool.map(one, TASKS, chunksize=1)
    (OUTDIR / "probe_summary.json").write_text(json.dumps(res, indent=1))
    print("PROBE DONE")
