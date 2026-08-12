"""PROG-R4, unit U3 -- THE COST PROBE. Not a result. Not evidence on G1.

WHAT THIS IS. The 2026-08-12 wind-down named one blocker for U3: the Newton and
GMRES iteration caps had never been set from a MEASURED per-epoch wall time, and
at the defaults (max_newton=40 x max_gmres=200) the worst case is ~4 h PER
ATTEMPT, which does not fit 100 attempts. This probe supplies the measurement
the CAP RULE consumes. The rule itself is fixed in advance, in
experiments/journal/prog_r4_u2u3_prereg_addendum.md section 2, and this probe
cannot change it.

WHY ITS NUMBERS ARE EVIDENCE ON NOTHING. The seeds here come from a T=2000 DNS.
That is LEG 353'S OWN UNDER-RESOURCED SCALE -- the very length whose null
ORCHESTRATION.md section 3d re-read as UNDER-RESOURCED rather than NO. Whether
anything converges here is therefore not informative about G1 in either
direction, and no count from this file is carried into a gate answer. What IS
transferable is COST: a Jacobian action is one integration over the orbit
period, and it costs the same seconds whichever DNS the seed was mined from.

WHAT IT MEASURES, and why each is needed by the rule:
  - Krylov dimensions actually consumed per epoch, with the rtol=1e-3 early
    exit active. The cap rule requires max_gmres >= 2x their 95th percentile,
    so that GMRES is stopped by its residual test and not by the cap.
  - epochs to convergence-or-stall. The rule requires max_newton >= 2x the
    median.
  - wall seconds per epoch and per Jacobian action, to price the envelope.

IT WRITES NOTHING THE REAL RUN READS. u2_m2_dns_recurrence.py's artefacts live
at fixed module-level paths (CKPT/FEAT/META/LIB). This probe touches none of
them: its DNS is held in memory and its output goes to u3_cost_probe.json.

Usage:
    python experiments/programme_r4/u3_cost_probe.py [--n-seeds 8] [--max-newton 3]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from solver.kolmogorov2d_nkbasin import (  # noqa: E402
    Kolmogorov2D, grid2d, newton_hookstep_rpo,
)
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    CKPT_EVERY, DT, DT_SAVE, N_FORCING, N_GRID, RE, R_THRES_RECORD,
    R_THRES_WINDOW, T_WINDOW, amplitude_index, full_R, regenerate,
)
from experiments.programme_r4.u3_g1_attempts import (  # noqa: E402
    GMRES_RTOL, TOL, anchor_of, seed_residual,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "u3_cost_probe.json")
T_PROBE = 2000.0


def short_dns(T):
    """The same integrator, the same burn-in, the same amplitude features as
    unit U2 -- only shorter, and held in memory."""
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    _, Y = grid2d(N_GRID)
    w_lam = -(RE / N_FORCING) * np.cos(N_FORCING * Y)
    rng = np.random.default_rng(11)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    w_burn, _ = solver.integrate(w_lam + 0.1 * np.linalg.norm(w_lam) * d, 500.0)
    w_hat = np.fft.fft2(w_burn) * solver.mask

    n_snap = int(round(T / DT_SAVE))
    sps = int(round(DT_SAVE / DT))
    ai, aj = amplitude_index(N_GRID)
    ckpt = np.empty(((n_snap + CKPT_EVERY - 1) // CKPT_EVERY,
                     N_GRID, N_GRID), dtype=np.complex128)
    feat = np.empty((n_snap, ai.size), dtype=np.float32)
    t0 = time.time()
    for k in range(n_snap):
        if k % CKPT_EVERY == 0:
            ckpt[k // CKPT_EVERY] = w_hat
        for _ in range(sps):
            w_hat = solver._rk4_step(w_hat, DT)
        feat[k] = np.abs(w_hat[ai, aj]).astype(np.float32)
    return solver, ckpt, feat, n_snap, sps, time.time() - t0


def mine(feat, n_snap, ckpt, solver, sps, n_take):
    """The prefilter and the strict-local-minimum selection of U2's recur
    stage, on the short trajectory."""
    lag_lo = max(1, int(round(T_WINDOW[0] / DT_SAVE)))
    lag_hi = int(round(T_WINDOW[1] / DT_SAVE))
    F = np.asarray(feat[:n_snap], dtype=np.float32)
    den = np.maximum(np.einsum("ij,ij->i", F, F), 1e-30)
    n_t, n_lag = n_snap - lag_hi, lag_hi - lag_lo + 1
    M = np.empty((n_t, n_lag), dtype=np.float32)
    for li, lag in enumerate(range(lag_lo, lag_hi + 1)):
        a, b = F[lag_hi:], F[lag_hi - lag:n_snap - lag]
        M[:, li] = np.einsum("ij,ij->i", a - b, a - b) / den[lag_hi:]
    C = M[1:-1, 1:-1]
    is_min = C < R_THRES_RECORD
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di or dj:
                is_min &= C < M[1 + di:n_t - 1 + di, 1 + dj:n_lag - 1 + dj]
    ii, jj = np.nonzero(is_min)
    order = np.argsort(C[ii, jj])
    chosen = [(float(C[ii[o], jj[o]]), int(ii[o] + 1 + lag_hi),
               int(jj[o] + 1 + lag_lo)) for o in order[:600]]
    need = [i for _, it, lag in chosen for i in (it, it - lag)]
    snaps = regenerate(need, solver, ckpt, sps)
    cands = []
    for _, it, lag in chosen:
        R, s, m = full_R(snaps[it], snaps[it - lag], solver)
        if R < R_THRES_WINDOW and m == 0 and anchor_of(lag * DT_SAVE):
            cands.append(dict(R=R, s=s, T=lag * DT_SAVE,
                              snapshot_earlier=it - lag))
    cands.sort(key=lambda c: c["R"])
    return cands[:n_take], snaps


def probe_attempt(job):
    idx, w0, T0, s0, max_newton, max_gmres = job
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    t0 = time.time()
    out = newton_hookstep_rpo(w0, T0, s0, solver, tol=TOL,
                              max_newton=max_newton, max_gmres=max_gmres,
                              gmres_rtol=GMRES_RTOL, fd_eps=1e-6)
    wall = time.time() - t0
    return dict(idx=idx, wall_seconds=wall, n_epochs=out["n_iters"],
                reason=out["reason"], success=bool(out["success"]),
                final_residual=out["final_residual"],
                n_jac_evals=out["n_jac_evals"],
                n_residual_evals=out["n_residual_evals"],
                krylov_dims=[e["krylov_dim"] for e in out["ledger"]],
                radius_trials=[e["n_radius_trials"] for e in out["ledger"]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-seeds", type=int, default=8)
    ap.add_argument("--max-newton", type=int, default=3)
    ap.add_argument("--max-gmres", type=int, default=200)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    solver, ckpt, feat, n_snap, sps, dns_wall = short_dns(T_PROBE)
    print(f"probe DNS T={T_PROBE} in {dns_wall:.1f}s "
          f"({dns_wall / (n_snap * sps) * 1e3:.4f} ms/step)")

    cands, snaps = mine(feat, n_snap, ckpt, solver, sps, args.n_seeds)
    print(f"{len(cands)} anchored probe seeds (COST ONLY -- T=2000 is leg 353's "
          f"under-resourced scale; not evidence on G1)")
    if not cands:
        raise SystemExit("no anchored probe seeds; cannot price U3")

    jobs = []
    for i, c in enumerate(cands):
        w0 = snaps[c["snapshot_earlier"]]
        rp = seed_residual(w0, c["T"], c["s"], solver)
        rm = seed_residual(w0, c["T"], -c["s"], solver)
        jobs.append((i, w0, c["T"], c["s"] if rp <= rm else -c["s"],
                     args.max_newton, args.max_gmres))

    t0 = time.time()
    with mp.Pool(args.workers) as p:
        res = p.map(probe_attempt, jobs)
    wall = time.time() - t0

    kd = np.array([k for r in res for k in r["krylov_dims"]], dtype=float)
    ep = np.array([r["n_epochs"] for r in res], dtype=float)
    per_epoch = np.array([r["wall_seconds"] / max(r["n_epochs"], 1)
                          for r in res])
    jac = np.array([r["n_jac_evals"] for r in res], dtype=float)
    sec_per_jac = np.array([r["wall_seconds"] / max(r["n_jac_evals"], 1)
                            for r in res])

    rec = dict(
        what="PROG-R4 U3 COST PROBE -- cost measurement only",
        not_evidence=("seeds mined from a T=2000 DNS, which is leg 353's "
                      "under-resourced scale; no count here is evidence on "
                      "gate G1 in either direction, and none is carried into "
                      "a gate answer"),
        cap_rule_source="experiments/journal/prog_r4_u2u3_prereg_addendum.md section 2",
        probe_config=dict(T_dns=T_PROBE, n_seeds=len(cands),
                          max_newton=args.max_newton,
                          max_gmres=args.max_gmres, gmres_rtol=GMRES_RTOL,
                          tol=TOL, workers=args.workers, N=N_GRID, Re=RE),
        dns=dict(wall_seconds=dns_wall,
                 ms_per_step=dns_wall / (n_snap * sps) * 1e3),
        krylov_dims=dict(
            n=int(kd.size), mean=float(kd.mean()), median=float(np.median(kd)),
            p95=float(np.percentile(kd, 95)), max=float(kd.max()),
            hit_cap=int((kd >= args.max_gmres).sum()),
            note=("dimensions actually consumed with the rtol=1e-3 early exit "
                  "active; hit_cap counts epochs stopped by the CAP rather "
                  "than by the residual test")),
        epochs=dict(median=float(np.median(ep)), max=float(ep.max()),
                    reasons={k: sum(1 for r in res if r["reason"] == k)
                             for k in sorted({r["reason"] for r in res})}),
        cost=dict(
            wall_seconds_total=wall,
            seconds_per_epoch_median=float(np.median(per_epoch)),
            seconds_per_epoch_max=float(per_epoch.max()),
            seconds_per_jacobian_action_median=float(np.median(sec_per_jac)),
            jac_evals_median=float(np.median(jac)),
            workers=args.workers,
            parallel_note=("measured with the T=1e5 DNS running concurrently "
                           "on one further core; contention inflates these "
                           "seconds, so pricing from them is conservative")),
        per_seed=res,
        clay_movement="none -- a cost probe moves no link",
    )
    with open(OUT, "w") as f:
        json.dump(rec, f, indent=2)

    print(f"krylov dims: median {np.median(kd):.0f}, p95 "
          f"{np.percentile(kd, 95):.0f}, max {kd.max():.0f}, "
          f"{int((kd >= args.max_gmres).sum())} epochs hit the cap")
    print(f"epochs: median {np.median(ep):.0f}, max {ep.max():.0f}; "
          f"reasons {rec['epochs']['reasons']}")
    print(f"cost: {np.median(per_epoch):.1f} s/epoch median, "
          f"{np.median(sec_per_jac):.2f} s per Jacobian action")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
