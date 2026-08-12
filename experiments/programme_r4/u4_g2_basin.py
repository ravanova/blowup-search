"""PROG-R4 unit U4 -- CLAIM, gate G2.

  ############################################################
  ##  STATUS 2026-08-12: GATE G2 IS **UNANSWERED**.         ##
  ##  THIS RUNNER HAS NEVER BEEN RUN, NOT EVEN ONCE, NOT    ##
  ##  EVEN ON SYNTHETIC DATA. It is unvalidated code.       ##
  ##  It cannot have been run: its input is an orbit that   ##
  ##  U3 recovers, U3 never ran, and G1 is UNANSWERED. No   ##
  ##  basin radius has been measured by this programme, and ##
  ##  brick B5 clause (c-iii) is NOT a number.              ##
  ##  A successor must treat every line below as untested,  ##
  ##  and must land G1 = YES before this file is even       ##
  ##  eligible to run.                                      ##
  ############################################################

  G2: IS A RADIUS MEASURED WITH A COHERENT (MONOTONE) FAILURE BOUNDARY,
      CONTROL FIRING AS PLANTED?

  YES -> brick B5 clause (c-iii) becomes a number.
  NO  -> report the magnitudes and the mechanism. A NON-BOUNDARY IS THE
         DELIVERABLE, NOT A DEFECT TO TUNE AWAY. No parameter is retuned to
         manufacture a boundary.

  In BOTH branches CLAY_OBLIGATIONS section 4 is OPEN and NOT discharged, and
  stays open in every route-4 gate until leg 386 (ROUTE-DTOL) lands with a
  pre-registered delta mode (user ruling, 2026-08-12).

  Ceiling stays Tier 2. No L1-L4 link moves. Clay stays ~0.05%.

This unit runs ONLY if G1 answered YES: its input is an orbit that U3 actually
recovered. It never runs on a seed of its own devising -- there is no unseeded
search anywhere in it, so Ban 2 has no purchase.

WHAT IS MEASURED
  Take a recovered orbit (w*, T*, s*). Perturb the INITIAL DATA only, by
  eps * ||w*|| along random directions in the dealiased real-field subspace,
  leaving T* and s* as the starting guess. Run the same hookstep-Newton used in
  U3. An attempt SUCCEEDS if it converges to tol AND lands back on the same
  orbit (|T-T*| and shift both within tolerance). Sweep eps over a geometric
  ladder with several directions per rung.

COHERENCE (the thing G2 actually asks)
  A boundary is coherent if the per-rung success fraction p(eps) is monotone
  non-increasing, with a rung where p=1 below and a rung where p=0 above. The
  number of monotonicity violations is reported as a magnitude either way; a
  ragged p(eps) is a real answer about the basin, not a defect.

CONTROLS
  planted-success: eps=0 must converge in ~0 iterations. If it does not, the
                   success test itself is broken and no radius is reported.
  planted-failure: an unrelated turbulent DNS snapshot, handed the SAME (T*,s*)
                   guess, must NOT be scored as landing on the orbit. This is
                   the control on the FAILURE side: it proves the failure
                   verdict can be produced by the harness at all, so that
                   failures at large eps mean something.
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from solver.kolmogorov2d_nkbasin import (  # noqa: E402
    TWO_PI, Kolmogorov2D, newton_hookstep_rpo, optimal_shift_residual)

CURATED_G1 = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
ORBITS = os.path.join(HERE, "u3_g1_recovered_orbits.npz")
CKPT = os.path.join(HERE, "u2_dns_ckpt.npy")
CURATED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g2_v1.json")

N_GRID, RE, N_FORCING, DT = 24, 60.0, 4, 0.01
TOL = 1e-8
MAX_NEWTON, MAX_GMRES, GMRES_RTOL = 40, 200, 1e-3
MATCH_T_TOL = MATCH_S_TOL = 0.05
MATCH_FIELD_TOL = 1e-3      # relative, after optimal x-shift
EPS_MIN, EPS_MAX, N_RUNGS = 1e-4, 1.0, 13
N_DIRECTIONS = 8
RNG_SEED = 20260812


def make_direction(rng, solver):
    """Random real field in the dealiased, zero-mean subspace, unit norm."""
    d = rng.standard_normal((N_GRID, N_GRID))
    dh = np.fft.fft2(d) * solver.mask
    dh[0, 0] = 0.0
    d = np.fft.ifft2(dh).real
    return d / np.linalg.norm(d)


def same_orbit(out, w_star, T_star, s_star):
    if not out["success"]:
        return False, None
    ds = abs(((out["s"] - s_star + np.pi) % TWO_PI) - np.pi)
    _, field_rel = optimal_shift_residual(w_star, out["w0"])
    ok = (abs(out["T"] - T_star) < MATCH_T_TOL and ds < MATCH_S_TOL
          and field_rel < MATCH_FIELD_TOL)
    return bool(ok), float(field_rel)


def run_one(job):
    kind, rung, idx, eps, w_init, T_star, s_star, w_star = job
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    t0 = time.time()
    out = newton_hookstep_rpo(w_init, T_star, s_star, solver, tol=TOL,
                              max_newton=MAX_NEWTON, max_gmres=MAX_GMRES,
                              gmres_rtol=GMRES_RTOL, fd_eps=1e-6)
    ok, field_rel = same_orbit(out, w_star, T_star, s_star)
    return dict(kind=kind, rung=rung, direction=idx, eps=float(eps),
                converged=bool(out["success"]), same_orbit=ok,
                field_rel_after_shift=field_rel,
                final_residual=out["final_residual"], reason=out["reason"],
                n_iters=out["n_iters"], T=out["T"], s=out["s"],
                n_jac_evals=out["n_jac_evals"],
                wall_seconds=time.time() - t0)


def build_jobs(w_star, T_star, s_star, args, solver):
    rng = np.random.default_rng(RNG_SEED)
    scale = float(np.linalg.norm(w_star))
    eps_grid = np.geomspace(args.eps_min, args.eps_max, args.n_rungs)

    jobs = [("planted_success", -1, 0, 0.0, w_star.copy(), T_star, s_star,
             w_star)]

    # planted failure: an unrelated turbulent snapshot handed the same guess.
    ckpt = np.load(CKPT, mmap_mode="r")
    w_far = np.fft.ifft2(np.asarray(ckpt[len(ckpt) // 2])).real
    _, far_rel = optimal_shift_residual(w_star, w_far)
    jobs.append(("planted_failure", -1, 0, float(far_rel), w_far, T_star,
                 s_star, w_star))

    for r, eps in enumerate(eps_grid):
        for k in range(args.n_directions):
            d = make_direction(rng, solver)
            jobs.append(("sweep", r, k, float(eps),
                         w_star + eps * scale * d, T_star, s_star, w_star))
    return jobs, eps_grid, scale, float(far_rel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--n-rungs", type=int, default=N_RUNGS)
    ap.add_argument("--n-directions", type=int, default=N_DIRECTIONS)
    ap.add_argument("--eps-min", type=float, default=EPS_MIN)
    ap.add_argument("--eps-max", type=float, default=EPS_MAX)
    ap.add_argument("--out", default=CURATED)
    args = ap.parse_args()

    with open(CURATED_G1) as f:
        g1 = json.load(f)
    if g1["gate"]["answer"] != "YES":
        raise SystemExit("G1 answered NO -- route 4 stops at U3 and U4 does "
                         "not run. Nothing is retried on DM authority.")

    orb = np.load(ORBITS)
    # the recovered attempt that reached the smallest final residual
    rec = [a for a in g1["attempts"] if a["recovered_named_orbit"]]
    rec.sort(key=lambda a: a["final_residual"])
    best = rec[0]
    key = [k for k in orb.files if k.startswith(f"attempt{best['attempt']:03d}_")]
    w_star = np.asarray(orb[key[0]])
    T_star, s_star = best["T_converged"], best["s_converged"]

    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    jobs, eps_grid, scale, far_rel = build_jobs(w_star, T_star, s_star, args,
                                                solver)
    print(f"orbit {best['anchor']}: T*={T_star:.6f}, s*={s_star:.6f}, "
          f"|R*|={best['final_residual']:.3e}, ||w*||={scale:.6f}")
    print(f"{len(jobs)} runs = 2 controls + {args.n_rungs} rungs x "
          f"{args.n_directions} directions")

    t0 = time.time()
    with mp.Pool(args.workers) as p:
        res = p.map(run_one, jobs)
    wall = time.time() - t0

    ctrl_s = [r for r in res if r["kind"] == "planted_success"][0]
    ctrl_f = [r for r in res if r["kind"] == "planted_failure"][0]
    controls_fired = bool(ctrl_s["same_orbit"] and not ctrl_f["same_orbit"])

    rungs = []
    for r, eps in enumerate(eps_grid):
        rows = [x for x in res if x["kind"] == "sweep" and x["rung"] == r]
        n_ok = sum(1 for x in rows if x["same_orbit"])
        rungs.append(dict(
            rung=r, eps=float(eps), eps_absolute=float(eps * scale),
            n_trials=len(rows), n_same_orbit=n_ok,
            success_fraction=n_ok / len(rows),
            n_converged_elsewhere=sum(1 for x in rows
                                      if x["converged"] and not x["same_orbit"]),
            median_final_residual=float(np.median(
                [x["final_residual"] for x in rows])),
            reasons={k: sum(1 for x in rows if x["reason"] == k)
                     for k in sorted({x["reason"] for x in rows})}))

    p_of_eps = [r["success_fraction"] for r in rungs]
    violations = [dict(rung=i + 1, eps=rungs[i + 1]["eps"],
                       p_prev=p_of_eps[i], p=p_of_eps[i + 1])
                  for i in range(len(p_of_eps) - 1)
                  if p_of_eps[i + 1] > p_of_eps[i] + 1e-12]
    monotone = not violations
    full = [r["eps"] for r in rungs if r["success_fraction"] == 1.0]
    zero = [r["eps"] for r in rungs if r["success_fraction"] == 0.0]
    bracketed = bool(full and zero and max(full) < min(zero))
    coherent = bool(monotone and bracketed and controls_fired)

    record = dict(
        unit="U4", kind="CLAIM (gate G2)", programme="PROG-R4",
        gate=dict(
            question="G2: IS A RADIUS MEASURED WITH A COHERENT (MONOTONE) "
                     "FAILURE BOUNDARY, CONTROL FIRING AS PLANTED?",
            answer="YES" if coherent else "NO",
            monotone=monotone,
            bracketed=bracketed,
            controls_fired_as_planted=controls_fired,
            monotonicity_violations=violations,
            on_NO=("A non-boundary IS the deliverable, not a defect to tune "
                   "away. The magnitudes and the mechanism are reported below; "
                   "no parameter was retuned after seeing this answer.")),
        orbit=dict(anchor=best["anchor"], T=T_star, s=s_star,
                   T_published=best["T_published"],
                   s_published=best["s_published"],
                   final_residual_at_recovery=best["final_residual"],
                   norm_w_star=scale,
                   source="Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV",
                   provenance="recovered by PROG-R4 U3 (gate G1 = YES)"),
        radius=dict(
            largest_eps_with_all_directions_returning=max(full) if full else None,
            smallest_eps_with_no_direction_returning=min(zero) if zero else None,
            absolute_lower=float(max(full) * scale) if full else None,
            absolute_upper=float(min(zero) * scale) if zero else None,
            units="eps is relative to ||w*|| in the grid L2 norm",
            clause_c_iii=("brick B5 clause (c-iii) is a number iff G2 = YES; "
                          "the bracket above is that number's resolution")),
        controls=dict(planted_success=ctrl_s, planted_failure=ctrl_f,
                      planted_failure_distance_from_orbit=far_rel),
        resourcing=dict(N=N_GRID, Re=RE, tol=TOL, max_newton=MAX_NEWTON,
                        max_gmres=MAX_GMRES, gmres_rtol=GMRES_RTOL,
                        n_rungs=args.n_rungs, n_directions=args.n_directions,
                        eps_min=args.eps_min, eps_max=args.eps_max,
                        rng_seed=RNG_SEED, workers=args.workers,
                        wall_seconds=wall,
                        total_jac_evals=sum(r["n_jac_evals"] for r in res)),
        match_criterion=dict(match_T_tol=MATCH_T_TOL, match_s_tol=MATCH_S_TOL,
                             match_field_tol_after_optimal_shift=MATCH_FIELD_TOL),
        rungs=rungs,
        open_obligations_carried=[
            "CLAY_OBLIGATIONS section 6, obligation 1 (no method) -- OPEN",
            "CLAY_OBLIGATIONS section 6, obligation 2 (no method) -- OPEN",
            ("CLAY_OBLIGATIONS section 4 -- OPEN and NOT discharged; stays "
             "open in every route-4 gate until leg 386 (ROUTE-DTOL) lands "
             "with a pre-registered delta mode (user ruling, 2026-08-12)"),
        ],
        ceiling="Tier 2",
        clay_movement="none -- no L1-L4 link moved by this unit",
        runs=res,
    )
    with open(args.out, "w") as f:
        json.dump(record, f, indent=2)

    print(f"G2 = {record['gate']['answer']}  (monotone={monotone}, "
          f"bracketed={bracketed}, controls={controls_fired})")
    for r in rungs:
        print(f"  eps={r['eps']:.3e}  p={r['success_fraction']:.3f}  "
              f"median|R|={r['median_final_residual']:.3e}  {r['reasons']}")
    print(f"radius bracket: {record['radius']}")
    print(f"wrote {args.out}  ({wall/3600:.2f} h)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
