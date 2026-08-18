"""Leg 401 L6 -- parallel-efficiency measurement (no artefact, no gate number).

Measures aggregate objective+gradient throughput at 1, 2, 4, 6 worker processes so that the
iteration cap in the ladder run is chosen from a measured throughput, and the wall-clock
cost reported under pre-committed reading (d) is a real number.
"""
import multiprocessing as mp
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2_route_l6_v1 as L6  # noqa: E402

REPS = 6


def work(task):
    Lmax, Nr, Ks = task
    g = L6.Geom(Lmax, Nr, Ks, 2.0)
    rng = np.random.default_rng(9)
    x = L6.normalise(g, rng.standard_normal(g.n_dof) * 0.1, "B")
    L6.objective(g, x, "B")
    t = time.time()
    for _ in range(REPS):
        L6.objective(g, x, "B")
    return (time.time() - t) / REPS


if __name__ == "__main__":
    for (tag, Lmax, Nr, Ks) in [("J0", 2, 8, 1), ("J2", 3, 12, 2), ("J4", 4, 20, 3)]:
        line = [tag]
        for np_ in (1, 6):
            t0 = time.time()
            with mp.get_context("fork").Pool(np_) as pool:
                per = pool.map(work, [(Lmax, Nr, Ks)] * np_)
            wall = time.time() - t0
            per_eval = float(np.mean(per))
            thru = np_ / per_eval
            line.append(f"nproc={np_}: {per_eval:.3f}s/eval  aggregate {thru:.2f} eval/s")
        print("  ".join(line), flush=True)
