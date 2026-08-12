"""PROG-R4, unit U3 -- CLAIM unit, GATE G1.

  ############################################################
  ##  STATUS 2026-08-12: GATE G1 IS **UNANSWERED**.         ##
  ##  THIS RUNNER HAS NEVER BEEN RUN ON REAL DATA.          ##
  ##  The programme was wound down by user instruction      ##
  ##  during unit U2, before the T=1e5 DNS finished, so the ##
  ##  recurrence library this runner consumes DOES NOT      ##
  ##  EXIST. No G1 verdict has been produced by anyone. Do  ##
  ##  not read a number out of this file or infer one from  ##
  ##  its presence. Before any output of this code is       ##
  ##  believed, a successor must: (1) run U2 to completion  ##
  ##  at T=1e5 and land MILESTONE M2 against its own        ##
  ##  checks, (2) fix the iteration caps from a MEASURED    ##
  ##  per-epoch cost, (3) run this end to end. Only the     ##
  ##  seeding/anchoring logic below has been exercised, and ##
  ##  only on a partial 9500-time-unit prefix in a scratch  ##
  ##  dry run whose outputs were discarded.                 ##
  ############################################################

THE GATE, in its pre-committed wording (experiments/journal/prog_r4_prereg.md):

    G1: DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO tol=1e-8?

    yes -> U4 proceeds; CEILING TIER 2; CLAY_OBLIGATIONS section 6's two
    obligations remain OPEN, and section 4 is OPEN and NOT discharged and
    stays open until leg 386 (ROUTE-DTOL) lands with a pre-registered delta
    mode.

    no  -> a RESOURCED null. ORCHESTRATION.md section 3d's stop fires ON
    MEASUREMENT, route 4 stops, per-attempt residuals, condition numbers and
    the comparison are reported as MAGNITUDES, a stop packet goes to the user,
    and nothing is retried on DM authority. Section 6's two obligations remain
    OPEN, and section 4 is OPEN and NOT discharged on the same terms.

This file does not restate, soften or re-scope that. It runs the attempts and
records what happens.

THE COMPLIANT SCALE, pre-registered and not adjusted here: T=1e5 DNS (unit
U2), a genuine hookstep (unit U1), ~100 attempts, N=24. Under the sourced
per-attempt success rates -- Chandler & Kerswell's 4.3% for the nonzero-shift
RPO class at Re=60, Lucas & Kerswell's ~10% at the residuals in play --
P(0 successes in 100) is ~1.2% and ~3e-5 respectively. That is what makes a
null here a RESOURCED null rather than the under-resourced one leg 353's five
attempts could only produce (P(0 in 5) = 59-77%).

THE SEED, carried verbatim from writeup/novelty/prog_r4.md section 1:
  SOURCE: Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV.
  IDENTIFIERS: the five published RPOs leg 353 pre-registered, including
  UPO37 (shift s=0.375), as recorded in writeup/data/p2_route_dsspb5_v1.json.
  WHY NOT A CHEAP-ENTRANCE CONSTRUCTION: obtained by recurrent-flow analysis
  of turbulent DNS trajectories converged with hookstep-Newton, NOT by
  bifurcation off a fixed point of a rescaled flow; and the search here is
  INITIALISED from that published data.

BAN SCREEN, applied to this unit's own steps.
  Ban 1 (cheap entrance): no step below continues a fixed point into an orbit.
  Every attempt starts from a turbulent DNS snapshot mined in U2 and targets a
  published period; there is no continuation parameter anywhere in the unit.
  Ban 2 (expensive entrance): does not apply, because the search is SEEDED and
  the seed is named above. Every attempt is anchored to one of the eight named
  Table IV rows -- candidates are admitted only if their measured period lies
  in the Table IV band, and each is labelled with the row it is anchored to.
  IF ANY ATTEMPT WERE EVER RUN WITHOUT A NAMED ANCHOR, Ban 2 would apply in
  full and this unit would stop and escalate rather than report.

THE SHIFT SIGN IS MEASURED, NOT ASSUMED. optimal_shift_residual(w1, w2)
returns s with shift_x(w2, s) ~ w1, while the RPO residual wants s' with
shift_x(Phi_T(w0), s') = w0. With w0 the EARLIER snapshot those are inverse to
each other, so the seed shift is -s. Rather than trust that derivation, each
seed evaluates the extended residual at BOTH signs and takes the smaller,
recording which won. This module already cost this repo a real sign bug once
(leg 353's FFT cross-correlation peak sits at j=-s, fixed mid-leg, after every
candidate before the fix carried a wrong-signed guess), so the convention is
re-measured at the point of use and the tally is reported.

Usage:
    python experiments/programme_r4/u3_g1_attempts.py [--n-attempts 100]
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
    Kolmogorov2D, extended_residual, newton_hookstep_rpo, pack, shift_x,
)
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    CKPT, DT, DT_SAVE, LIB, META, N_FORCING, N_GRID, RE, regenerate,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
# Two files on purpose. The CURATED one is the unit's landing artefact and is
# what the figure script asserts against; the LEDGER keeps the full
# per-iteration record, which is bulky and is what a successor re-deriving the
# mechanism would need.
CURATED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")
LEDGER = os.path.join(HERE, "u3_g1_ledger.json")
# Converged states for attempts that recovered a named orbit. U4 needs the
# actual field, not a summary of it, and 24x24 floats are small enough to keep
# in the programme's persistent state.
ORBITS = os.path.join(HERE, "u3_g1_recovered_orbits.npz")

# The eight named Lucas & Kerswell Table IV rows, exactly as leg 353
# pre-registered them: (identifier, T_published, s_published, m_published).
TABLE_IV = [
    ("UPO37", 19.334, 0.375, 0), ("UPO35", 18.912, 5.576, 0),
    ("UPO34", 18.878, 0.418, 0), ("UPO32", 18.694, 0.434, 0),
    ("UPO22", 17.160, 0.361, 0), ("UPO20", 16.908, 0.553, 0),
    ("UPO17", 16.753, 0.482, 0), ("UPO9", 14.776, 0.295, 0),
]
# A candidate is anchored to a named row when its measured period is within
# this much of the published one (~5% at T~19). Stated before the run.
T_ANCHOR_TOL = 1.0
TOL = 1e-8
MAX_NEWTON = 40
MAX_GMRES = 200
GMRES_RTOL = 1e-3
# Matching a converged orbit back to a named row, leg 353's own tolerances.
MATCH_T_TOL, MATCH_S_TOL = 0.05, 0.05
TWO_PI = 2.0 * np.pi


def anchor_of(T):
    """Nearest named Table IV row within T_ANCHOR_TOL, else None."""
    best, bd = None, np.inf
    for name, Tp, sp, mp_ in TABLE_IV:
        d = abs(T - Tp)
        if d < bd:
            best, bd = (name, Tp, sp, mp_), d
    return best if bd <= T_ANCHOR_TOL else None


def seed_residual(w0, T, s, solver):
    ref_rhs = solver.rhs_physical(w0)
    ref_dwdx = np.fft.ifft2(1j * solver.KX
                            * (np.fft.fft2(w0) * solver.mask)).real
    return float(np.linalg.norm(
        extended_residual(pack(w0, T, s), solver, w0, ref_rhs, ref_dwdx)))


def run_attempt(job):
    idx, w0, T0, s0, meta = job
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    t0 = time.time()
    out = newton_hookstep_rpo(w0, T0, s0, solver, tol=TOL,
                              max_newton=MAX_NEWTON, max_gmres=MAX_GMRES,
                              gmres_rtol=GMRES_RTOL, fd_eps=1e-6)
    wall = time.time() - t0
    ds = abs(((out["s"] - meta["s_published"] + np.pi) % TWO_PI) - np.pi)
    recovered = bool(out["success"]
                     and abs(out["T"] - meta["T_published"]) < MATCH_T_TOL
                     and ds < MATCH_S_TOL)
    E, D, I = solver.diagnostics(out["w0"])
    rec = dict(meta)
    rec.update(
        attempt=idx, reason=out["reason"], success=bool(out["success"]),
        final_residual=out["final_residual"], n_iters=out["n_iters"],
        residual_history=[float(v) for v in out["residual_history"]],
        T_converged=out["T"], s_converged=out["s"],
        delta_T_from_published=abs(out["T"] - meta["T_published"]),
        delta_s_from_published=float(ds),
        recovered_named_orbit=recovered,
        D_over_Dlam=D / solver.D_lam, I_over_Dlam=I / solver.D_lam,
        n_jac_evals=out["n_jac_evals"],
        n_residual_evals=out["n_residual_evals"],
        krylov_dims=[e["krylov_dim"] for e in out["ledger"]],
        radius_trials=[e["n_radius_trials"] for e in out["ledger"]],
        wall_seconds=wall)
    # Full per-iteration record travels separately: it is what a successor
    # re-deriving the mechanism needs, and it is too bulky for the curated file.
    rec["_ledger"] = out["ledger"]
    rec["_w0"] = out["w0"]
    return rec


def build_jobs(args, solver):
    with open(LIB) as f:
        lib = json.load(f)
    with open(META) as f:
        meta = json.load(f)
    ckpt = np.load(CKPT, mmap_mode="r")
    steps_per_snap = int(round(DT_SAVE / DT))

    pool = []
    dropped_m = 0
    for c in lib["candidates"]:
        if not c["in_newton_window"]:
            continue
        if c["m"] != 0:
            # The extended residual carries a continuous x-shift only, so an
            # m != 0 near-recurrence cannot be represented as a seed for it.
            # Every named Table IV row has m_published = 0, so nothing named is
            # lost; the count is reported rather than silently dropped.
            dropped_m += 1
            continue
        a = anchor_of(c["T"])
        if a is None:
            continue
        pool.append((c, a))
    pool.sort(key=lambda ca: ca[0]["R"])
    pool = pool[:args.n_attempts]

    need = [c["snapshot_earlier"] for c, _ in pool]
    snaps = regenerate(need, solver, ckpt, steps_per_snap)

    jobs = []
    sign_tally = {"plus": 0, "minus": 0}
    for i, (c, a) in enumerate(pool):
        name, Tp, sp, mp_ = a
        # w0 is the EARLIER snapshot: Phi_T carries it to the later one.
        w0 = snaps[c["snapshot_earlier"]]
        r_plus = seed_residual(w0, c["T"], c["s"], solver)
        r_minus = seed_residual(w0, c["T"], -c["s"], solver)
        s0 = c["s"] if r_plus <= r_minus else -c["s"]
        sign_tally["plus" if r_plus <= r_minus else "minus"] += 1
        jobs.append((i, w0, c["T"], s0,
                     dict(anchor=name, T_published=Tp, s_published=sp,
                          m_published=mp_, R_seed=c["R"],
                          T_seed=c["T"], s_seed=s0,
                          seed_residual_plus=r_plus,
                          seed_residual_minus=r_minus,
                          seed_extended_residual=min(r_plus, r_minus),
                          snapshot_earlier=c["snapshot_earlier"])))
    return jobs, dropped_m, sign_tally, lib, meta


def main():
    global MAX_NEWTON, MAX_GMRES
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-attempts", type=int, default=100)
    ap.add_argument("--workers", type=int, default=10)
    ap.add_argument("--out", default=CURATED)
    ap.add_argument("--ledger-out", default=LEDGER)
    # Iteration caps are a COST setting, not part of the pre-registered
    # compliant scale (which is T=1e5 / genuine hookstep / ~100 attempts /
    # N=24). They are fixed from the measured per-epoch wall time BEFORE the
    # attempts are run, never adjusted after seeing an outcome; whatever is
    # used is banked in resourcing{} and reported against Chandler & Kerswell's
    # nominal 75/500.
    ap.add_argument("--max-newton", type=int, default=MAX_NEWTON)
    ap.add_argument("--max-gmres", type=int, default=MAX_GMRES)
    args = ap.parse_args()
    MAX_NEWTON, MAX_GMRES = args.max_newton, args.max_gmres

    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    jobs, dropped_m, sign_tally, lib, dns_meta = build_jobs(args, solver)
    print(f"{len(jobs)} attempts queued ({dropped_m} candidates dropped for "
          f"m != 0); seed shift sign: {sign_tally}")
    if not jobs:
        raise SystemExit("no anchored candidates -- STOP and escalate rather "
                         "than run an unanchored search (Ban 2)")

    t0 = time.time()
    with mp.Pool(args.workers) as p:
        results = p.map(run_attempt, jobs)
    wall = time.time() - t0

    ledgers = [{"attempt": r["attempt"], "anchor": r["anchor"],
                "ledger": r.pop("_ledger")} for r in results]
    saved = {}
    for r in results:
        w = r.pop("_w0")
        if r["recovered_named_orbit"]:
            saved[f"attempt{r['attempt']:03d}_{r['anchor']}"] = w
    if saved:
        np.savez_compressed(ORBITS, **saved)
        print(f"saved {len(saved)} recovered orbit states to {ORBITS}")

    recovered = [r for r in results if r["recovered_named_orbit"]]
    converged = [r for r in results if r["success"]]
    by_anchor = {}
    for r in results:
        by_anchor.setdefault(r["anchor"], []).append(r["final_residual"])
    finals = sorted(r["final_residual"] for r in results)

    record = dict(
        unit="U3", kind="CLAIM (gate G1)", programme="PROG-R4",
        gate=dict(
            question="G1: DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO "
                     "tol=1e-8?",
            answer="YES" if recovered else "NO",
            n_recovered=len(recovered),
            n_converged_to_tol=len(converged),
            n_attempts=len(results)),
        resourcing=dict(
            T_dns=dns_meta["T_recorded"], N=N_GRID, Re=RE,
            globalisation="genuine Newton-GMRES-hookstep trust region (U1)",
            n_attempts=len(results),
            tol=TOL, max_newton=MAX_NEWTON, max_gmres=MAX_GMRES,
            gmres_rtol=GMRES_RTOL,
            limits_note=("Chandler & Kerswell ran max Newton=75, max "
                         "GMRES=500, max hookstep=50, which they call "
                         "'fairly conservative'. This run sits below those on "
                         "Newton and GMRES because one Jacobian action here "
                         "is a full ~19 time-unit integration on CPU; the "
                         "measured Krylov dimensions and Jacobian-action "
                         "counts below say how much of the nominal budget was "
                         "actually used, which is the honest way to report "
                         "the gap rather than quoting the nominal limit"),
            P_zero_in_100_at_ChandlerKerswell_4p3pct=0.012,
            P_zero_in_100_at_LucasKerswell_10pct=3e-05),
        seed=dict(
            source="Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV",
            rows=[t[0] for t in TABLE_IV],
            anchor_rule=f"|T_candidate - T_published| <= {T_ANCHOR_TOL}",
            ban1="PASS - no step continues a fixed point into an orbit",
            ban2="PASS - every attempt anchored to a named row; an unanchored "
                 "attempt would STOP and escalate, not report",
            shift_sign_measured_not_assumed=sign_tally,
            candidates_dropped_for_nonzero_y_shift=dropped_m),
        magnitudes=dict(
            final_residuals_sorted=finals,
            best_final_residual=finals[0] if finals else None,
            median_final_residual=float(np.median(finals)) if finals else None,
            seed_residuals=[r["seed_extended_residual"] for r in results],
            reasons={k: sum(1 for r in results if r["reason"] == k)
                     for k in sorted({r["reason"] for r in results})},
            by_anchor={k: dict(n=len(v), best=min(v)) for k, v in
                       sorted(by_anchor.items())},
            total_jac_evals=sum(r["n_jac_evals"] for r in results),
            wall_seconds=wall,
            workers=args.workers),
        open_obligations_carried=[
            "CLAY_OBLIGATIONS section 6, obligation 1 (no method) -- OPEN",
            "CLAY_OBLIGATIONS section 6, obligation 2 (no method) -- OPEN",
            ("CLAY_OBLIGATIONS section 4 -- OPEN and NOT discharged; stays "
             "open in every route-4 gate until leg 386 (ROUTE-DTOL) lands "
             "with a pre-registered delta mode (user ruling, 2026-08-12)"),
        ],
        escalation_not_assumed=(
            "Lucas & Kerswell's own T=5e6 is ~10.2 GPU-days and the hardware "
            "is not present. It is reported WITH these numbers as a question "
            "for the user, never presumed either way."),
        clay_movement="none -- no L1-L4 link moved by this unit",
        attempts=results,
    )
    with open(args.out, "w") as f:
        json.dump(record, f, indent=2)
    with open(args.ledger_out, "w") as f:
        json.dump(dict(unit="U3", programme="PROG-R4",
                       note=("per-Newton-iteration ledger for every attempt "
                             "in " + os.path.basename(args.out)),
                       attempts=ledgers), f, indent=2)

    print(f"G1 = {record['gate']['answer']}: {len(recovered)} recovered, "
          f"{len(converged)} converged to tol, {len(results)} attempts, "
          f"{wall/3600:.2f} h")
    print(f"best final |R| = {finals[0]:.6e}, median = "
          f"{np.median(finals):.6e}")
    print(f"reasons: {record['magnitudes']['reasons']}")
    print(f"wrote {args.out} and {args.ledger_out}")


if __name__ == "__main__":
    main()
