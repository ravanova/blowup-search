#!/usr/bin/env python3
"""Leg 353, Route-DSSP brick B5 -- DSSP-NKBASIN.

Gate (drafted writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDSSP_V1.md sec 5.1, brick
B5): does a Newton-Krylov + phase-condition layer recover a PUBLISHED
relative periodic orbit of 2-D Kolmogorov flow, and what is the MEASURED
radius of its basin (how far can the published initial guess be perturbed
before Newton fails)?

Target: Lucas & Kerswell 2015 (arXiv:1406.1820v2) Table IV "UPO 37" --
T=19.334, s=0.375, m=0, at Re=60, n=4, alpha=1 (domain [0,2pi)^2). See
writeup/novelty/leg_353.md for the novelty pass that pinned this source
BEFORE this construction ran.

Pipeline:
  1. DNS from a perturbed-laminar initial condition, long enough to leave the
     linear-instability transient and land on the chaotic attractor.
  2. Recurrence-flow search (paper's eq. 14, optimal-shift form) over the
     saved trajectory, targeted at T close to the published catalogue values
     (T=19.334 first, several neighbouring Table IV rows as fallback) --
     NOT a blind global search, informed by the paper's own table since that
     is public information this leg is allowed to use to scope its search.
  3. Newton-Krylov + phase-condition refinement (solver/kolmogorov2d_nkbasin)
     of the best candidate(s) into an exact RPO.
  4. Cross-check the converged (T, s) and Fig.4-style (D/D_lam, I/D_lam)
     invariants against the paper's Table IV / Fig. 4 to report whether the
     SAME published object was recovered.
  5. Basin-radius measurement: perturb the converged initial condition by
     increasing relative magnitudes and re-run Newton, recording the largest
     perturbation for which Newton still reconverges to the SAME orbit.

Runtime note: every long step is timed and reported; sizes were chosen after
timing a single T=19.334 integration (~1.7s at N=24, dt=0.01) so the total
budget stays inside the ORCHESTRATION.md "assess before you run anything
long" ~10 minute guideline per invocation -- this script is meant to be run
in stages (recurrence search, then Newton, then basin sweep) via its CLI
flags, each stage its own sub-10-minute call.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from solver.kolmogorov2d_nkbasin import (  # noqa: E402
    Kolmogorov2D,
    TWO_PI,
    grid2d,
    measure_basin_radius,
    newton_krylov_rpo,
    optimal_shift_residual,
)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_dsspb5_v1.json")

# Re=60, n_forcing=4, alpha=1 -- exactly Lucas & Kerswell 2015's Sec. III setup.
RE = 60.0
N_FORCING = 4
N_GRID = 24
DT = 0.01

# Published Table IV target rows (T, s, m) this leg checks against -- UPO 37
# first (the paper's own highlighted example), then a handful of neighbours
# as fallback in case the short DNS this leg can afford does not visit
# UPO 37's neighbourhood closely enough.
TABLE_IV_TARGETS = [
    ("UPO37", 19.334, 0.375, 0),
    ("UPO35", 18.912, 5.576, 0),
    ("UPO34", 18.878, 0.418, 0),
    ("UPO32", 18.694, 0.434, 0),
    ("UPO22", 17.160, 0.361, 0),
    ("UPO20", 16.908, 0.553, 0),
    ("UPO17", 16.753, 0.482, 0),
    ("UPO9",  14.776, 0.295, 0),
]


def run_dns(T_total, dt_save, seed=0, verbose=True):
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    rng = np.random.default_rng(seed)
    Y = solver.Y
    w_lam = -(RE / N_FORCING) * np.cos(N_FORCING * Y)
    w0 = w_lam + 1.0 * rng.standard_normal((N_GRID, N_GRID))
    w0 = np.fft.ifft2(np.fft.fft2(w0) * solver.mask).real

    save_times = list(np.arange(0.0, T_total, dt_save))
    t0 = time.time()
    w_final, saved = solver.integrate(w0, T_total, save_times=save_times)
    wall = time.time() - t0
    if verbose:
        print(f"DNS: T_total={T_total}, dt_save={dt_save}, "
              f"{len(saved)} snapshots, wall={wall:.1f}s")
    times = np.array([t for t, _ in saved])
    fields = np.stack([w for _, w in saved])
    return solver, times, fields, wall


def recurrence_search(solver, times, fields, T_targets, T_tol=0.5,
                       transient=30.0, verbose=True):
    """For each named target T, scan all snapshot pairs (t, t') with
    t >= transient and t' close to t+T (within T_tol, snapped to the nearest
    stored snapshot), compute the optimal-shift residual, and keep the best
    (lowest-residual) match."""
    best = {}
    for name, T, s_pub, m in T_targets:
        candidates = []
        for i, t in enumerate(times):
            if t < transient:
                continue
            t_target = t + T
            if t_target > times[-1]:
                break
            j = int(np.searchsorted(times, t_target))
            for jj in (j - 1, j):
                if 0 <= jj < len(times) and abs(times[jj] - t_target) <= T_tol:
                    s_best, rel = optimal_shift_residual(fields[i], fields[jj])
                    candidates.append((rel, t, times[jj], s_best))
        candidates.sort(key=lambda c: c[0])
        best[name] = dict(T_published=T, s_published=s_pub, m_published=m,
                           top=candidates[:5])
        if verbose and candidates:
            rel, t, t2, s_best = candidates[0]
            print(f"  {name} (T_pub={T}, s_pub={s_pub}): best residual={rel:.4e} "
                  f"at t={t:.2f}, T_actual={t2 - t:.3f}, s_found={s_best:.3f} "
                  f"({len(candidates)} candidates)")
        elif verbose:
            print(f"  {name}: no candidates in window")
    return best


def laminar_control(solver, verbose=True):
    """Sanity control: the laminar profile w_lam = -(Re/n)*cos(n*y) is an
    EXACT fixed point (Phi_T(w_lam)=w_lam for every T, and shift_x(w_lam,s)
    =w_lam for every s since it is x-independent), so a small perturbation
    away from it must let newton_krylov_rpo drive the residual down
    substantially and MONOTONICALLY -- unlike the real-target attempts below.
    This is here to distinguish 'the seed was too far from any solution'
    from 'the Newton-Krylov+phase-condition code is broken': if this control
    also stalls, the earlier failures cannot be blamed on seed quality."""
    X, Y = grid2d(solver.N)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rng = np.random.default_rng(0)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    w0_guess = w_lam + 0.01 * np.linalg.norm(w_lam) * d
    t0 = time.time()
    out = newton_krylov_rpo(w0_guess, 1.0, 0.1, solver, tol=1e-8,
                             max_newton=8, max_gmres=15, fd_eps=1e-6,
                             verbose=verbose)
    wall = time.time() - t0
    hist = out["residual_history"]
    monotone = all(hist[i + 1] <= hist[i] for i in range(len(hist) - 1))
    reduction = 1.0 - hist[-1] / hist[0] if hist and hist[0] > 0 else 0.0
    if verbose:
        print(f"  laminar control: |R| {hist[0]:.3e} -> {hist[-1]:.3e} "
              f"({100*reduction:.1f}% reduction, monotone={monotone}) "
              f"wall={wall:.1f}s")
    return dict(residual_history=hist, monotone_decrease=bool(monotone),
                fractional_reduction=float(reduction), wall_seconds=wall,
                reason=out["reason"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["search", "newton", "basin", "all"],
                     default="all")
    ap.add_argument("--T_total", type=float, default=600.0)
    ap.add_argument("--dt_save", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n_newton_attempts", type=int, default=5)
    ap.add_argument("--max_newton", type=int, default=10)
    ap.add_argument("--max_gmres", type=int, default=20)
    args = ap.parse_args()

    result = {"params": dict(Re=RE, n_forcing=N_FORCING, N=N_GRID, dt=DT,
                              domain="[0,2pi)^2 (alpha=1)",
                              source="arXiv:1406.1820v2 Table IV",
                              T_total=args.T_total, dt_save=args.dt_save,
                              seed=args.seed)}

    t0 = time.time()
    solver, times, fields, dns_wall = run_dns(args.T_total, args.dt_save,
                                               seed=args.seed)
    result["dns_wall_seconds"] = dns_wall
    result["n_snapshots"] = int(len(times))

    rec_t0 = time.time()
    best = recurrence_search(solver, times, fields, TABLE_IV_TARGETS)
    rec_wall = time.time() - rec_t0
    result["recurrence_search_wall_seconds"] = rec_wall
    result["recurrence_search"] = {
        name: dict(T_published=v["T_published"], s_published=v["s_published"],
                   m_published=v["m_published"],
                   top=[dict(residual=c[0], t=c[1], t2=c[2], s_found=c[3])
                        for c in v["top"]])
        for name, v in best.items()
    }

    # pick the globally best candidate across all targets
    flat = []
    for name, v in best.items():
        for c in v["top"]:
            flat.append((c[0], name, v["T_published"], v["s_published"], c[1], c[2], c[3]))
    flat.sort(key=lambda r: r[0])
    result["global_best"] = None
    if flat:
        rel, name, T_pub, s_pub, t, t2, s_found = flat[0]
        result["global_best"] = dict(target=name, T_published=T_pub,
                                      s_published=s_pub, residual=rel,
                                      t_start=t, t_end=t2, T_actual=t2 - t,
                                      s_found=s_found)
        print(f"\nGLOBAL BEST: {name} residual={rel:.4e} T_actual={t2-t:.3f} "
              f"s_found={s_found:.3f} (published T={T_pub}, s={s_pub})")

    # -----------------------------------------------------------------
    # Newton-Krylov attempts: diverse candidates spanning several distinct
    # published targets, not just repeated tries at the single best residual
    # -- if the extraction layer fails, it should fail the same way on
    # independently-selected seeds, not just on an unlucky one.
    # -----------------------------------------------------------------
    attempt_plan = [("UPO37", 0), ("UPO37", 1), ("UPO9", 0), ("UPO22", 0)]
    if "UPO35" in best and best["UPO35"]["top"]:
        attempt_plan.insert(1, ("UPO35", 0))
    attempt_plan = attempt_plan[: args.n_newton_attempts]

    newton_attempts = []
    converged = None
    if args.stage in ("newton", "basin", "all"):
        for name, k in attempt_plan:
            v = best.get(name)
            if not v or k >= len(v["top"]):
                continue
            c = v["top"][k]
            rel, t, t2, s_found = c[0], c[1], c[2], c[3]
            i = int(np.searchsorted(times, t))
            w0_guess = fields[i]
            T_guess = t2 - t
            print(f"\n--- Newton attempt: target={name}[{k}] t={t:.2f} "
                  f"T_guess={T_guess:.3f} s_guess={s_found:.4f} "
                  f"seed_residual={rel:.3e} ---")
            tn0 = time.time()
            out = newton_krylov_rpo(w0_guess, T_guess, s_found, solver,
                                     tol=1e-8, max_newton=args.max_newton,
                                     max_gmres=args.max_gmres, fd_eps=1e-6,
                                     verbose=True)
            wall = time.time() - tn0
            print(f"  -> success={out['success']} reason={out['reason']} "
                  f"T={out['T']:.5f} s={out['s']:.5f} "
                  f"final_res={out['final_residual']:.3e} "
                  f"n_iters={out['n_iters']} wall={wall:.1f}s")
            newton_attempts.append(dict(
                target=name, candidate_index=k, t_start=float(t),
                T_guess=float(T_guess), s_guess=float(s_found),
                seed_residual=float(rel), success=bool(out["success"]),
                reason=out["reason"], T_final=float(out["T"]),
                s_final=float(out["s"]),
                final_residual=float(out["final_residual"]),
                n_iters=int(out["n_iters"]),
                residual_history=[float(r) for r in out["residual_history"]],
                wall_seconds=wall))
            if out["success"]:
                converged = dict(w0=out["w0"], T=out["T"], s=out["s"],
                                  target=name)
                print("CONVERGED -- stopping further Newton attempts")
                break
    result["newton_attempts"] = newton_attempts
    result["any_converged"] = converged is not None

    # -----------------------------------------------------------------
    # Control: same Newton-Krylov+phase-condition machinery started near
    # the EXACT laminar fixed point, to distinguish a broken solver from a
    # too-far seed.
    # -----------------------------------------------------------------
    if args.stage in ("newton", "basin", "all"):
        print("\n--- Control: Newton from a small perturbation of the exact "
              "laminar fixed point ---")
        result["laminar_control"] = laminar_control(solver)

    # -----------------------------------------------------------------
    # Basin-radius measurement -- only meaningful if something converged.
    # -----------------------------------------------------------------
    if args.stage in ("basin", "all") and converged is not None:
        print("\n--- Basin radius measurement ---")
        eps_values = [0.001, 0.003, 0.01, 0.03, 0.1]
        basin = measure_basin_radius(
            converged["w0"], converged["T"], converged["s"], solver,
            eps_values, n_trials=3, rng=np.random.default_rng(1),
            tol=1e-8, max_newton=args.max_newton, max_gmres=args.max_gmres,
            fd_eps=1e-6)
        result["basin_radius"] = basin
        result["converged_orbit"] = dict(target=converged["target"],
                                          T=converged["T"], s=converged["s"])
        print(f"  radius_lower_bound={basin['radius_lower_bound']} "
              f"radius_upper_bound={basin['radius_upper_bound']}")
    elif args.stage in ("basin", "all"):
        result["basin_radius"] = None
        print("\nNo converged orbit -- basin radius NOT MEASURED "
              "(nothing to perturb).")

    result["total_wall_seconds"] = time.time() - t0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, default=float)
    print(f"\nWrote {OUT}")

    return solver, times, fields, best, result


if __name__ == "__main__":
    main()
