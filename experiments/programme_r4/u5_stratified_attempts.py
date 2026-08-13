"""PROG-R4, unit U5, stage 2 of 2 -- MILESTONE M3, the shift-stratified budget.

Pre-registered in experiments/journal/prog_r4_u2u3_prereg_addendum.md section
3g (AMENDMENT 5), committed BEFORE either stage ran.

    M3: THE SEED BUDGET IS STRATIFIED BY SHIFT -- the anchored reservoir is
    exhausted, the published |s| band is filled to a pre-committed quota, and
    the per-stratum yield is measured against U3's banked baseline.

    DELIVERED iff (1) the mining takes every anchored strict local minimum not
    provably excluded by the window, (2) >= 50 of the 100 attempts are seeded
    in |s| in [0.295, 0.707] against U3's 31, (3) the run completes at U3's
    caps, tol, admission test, m=0 requirement, anchor rule and matching
    predicate with none of them changed, (4) the per-stratum yield is reported
    against U3's banked baseline, (5) the controls fire as planted.

    NOT DELIVERED otherwise, for exactly one of SUPPLY, INSTRUMENT or BUDGET.

THIS UNIT DOES NOT RE-ANSWER G1. G1 stays UNDER-RESOURCED as banked in
writeup/data/p2_prog_r4_g1_v1.json; this file never writes there. If an attempt
recovers a named Table IV row that is a MILESTONE result and a CANDIDATE G1
RE-OPEN to raise to the user -- not a gate answer, and not a licence to rewrite
the banked one.

WHAT IS MANIPULATED AND WHAT IS HELD. The single manipulated variable is WHICH
SEEDS ARE OFFERED. Held at U3's values, and asserted against U3's own banked
record at startup rather than copied by hand: tol=1e-8, max_newton=52,
max_gmres=140, gmres_rtol=1e-3, R<0.25, m=0, T_ANCHOR_TOL=1.0, MATCH_*_TOL=0.05.
U3 section 8's options (b) relax the admission test, (c) add an m unknown and
(d) buy iterations are NOT taken.

THE STALL EXIT IS A REDUCTION IN SPEND, NOT A PURCHASE. From epoch 20 on, an
attempt stops if ||R|| has not halved over the preceding 10 epochs. Replayed
over all 100 of U3's banked residual histories it stops 0 of 14 convergences,
and the worst 10-epoch ratio any U3 convergence showed at k >= 20 was 0.0724
against the rule's 0.50 -- a factor of 6.9. It is implemented by SLICING the
epoch loop, with (w0, T, s, delta) threaded across slices; slicing was verified
to reproduce an unsliced run's iterates exactly (identical state, T and s)
before it was used, because the trust-region radius is threaded across epochs
inside the driver and dropping it would silently reset the trust region.

Usage:
    python experiments/programme_r4/u5_stratified_attempts.py [--workers 8]
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
    Kolmogorov2D, extended_residual, newton_hookstep_rpo, pack,
)
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    CKPT, DT, DT_SAVE, META, N_FORCING, N_GRID, RE, R_THRES_WINDOW,
    regenerate, TABLE_IV_PERIODS as _U2_TABLE_IV_PERIODS,
    T_ANCHOR_TOL as _U2_T_ANCHOR_TOL,
)
from experiments.programme_r4.u3_g1_attempts import (  # noqa: E402
    MATCH_S_TOL, MATCH_T_TOL, TABLE_IV, T_ANCHOR_TOL, TOL, TWO_PI, anchor_of,
)
from experiments.programme_r4 import u3_controls  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
LIB5 = os.path.join(HERE, "u5_shift_library.json")
# The full take is an 18 MB regenerable intermediate and is gitignored. The
# reduced file is committed and reproduces the allocation exactly -- asserted,
# not asserted-in-prose, by u5_reduce_library.py -- so a fresh clone that has
# not re-mined still selects the same 100 seeds.
LIB5_REDUCED = os.path.join(HERE, "u5_shift_library_admissible.json")
CURATED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_m3_v1.json")
LEDGER = os.path.join(HERE, "u5_m3_ledger.json")
ORBITS = os.path.join(HERE, "u5_m3_converged_orbits.npz")
PROGRESS = os.path.join(HERE, "u5_attempts_progress.txt")
U3_BANKED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_g1_v1.json")

# Caps: U3's, asserted against U3's banked record at startup (see main).
MAX_NEWTON, MAX_GMRES, GMRES_RTOL = 52, 140, 1e-3

# AMENDMENT 5 section 3g.5, the stall rule.
STALL_K, STALL_W, STALL_HALVE = 20, 10, 0.5

# AMENDMENT 5 section 3g.4, the quota rule. Strata are half-open in |s| except
# the published band, which is closed on both ends because its endpoints are
# published shifts (UPO9 at 0.295 and UPO35 at 0.707 after wrapping).
PUBLISHED_BAND = (0.295, 0.707)
STRATA = [
    ("P", "published", PUBLISHED_BAND[0], PUBLISHED_BAND[1], 60),
    ("L", "low", 0.0, 0.150, 20),
    ("M", "mid", 0.150, 0.295, 10),
    ("H", "high", 0.707, np.pi, 10),
]
SHORTFALL_ORDER = ["P", "L", "M", "H"]
PER_ROW_CAP_P = 8            # ceil(60/8): no single named row absorbs band P
DIVERSITY_DSNAP, DIVERSITY_DT = 4, 0.5


def wrap_abs(s):
    """|s| with s wrapped to (-pi, pi]. The programme's shift coordinate."""
    return float(abs((float(s) + np.pi) % TWO_PI - np.pi))


def stratum_of(abs_s):
    for key, _, lo, hi, _ in STRATA:
        if key == "P":
            if lo <= abs_s <= hi:
                return key
        elif key == "H":
            if abs_s > lo:
                return key
        elif lo <= abs_s < hi:
            return key
    return None


def seed_residual(w0, T, s, solver):
    ref_rhs = solver.rhs_physical(w0)
    ref_dwdx = np.fft.ifft2(1j * solver.KX
                            * (np.fft.fft2(w0) * solver.mask)).real
    return float(np.linalg.norm(
        extended_residual(pack(w0, T, s), solver, w0, ref_rhs, ref_dwdx)))


def solve_with_stall_exit(w0, T0, s0, solver):
    """newton_hookstep_rpo, with the pre-registered stall exit.

    Epochs 0..STALL_K-1 run in one call; after that, one epoch per call so the
    rule can be tested at EVERY k >= STALL_K rather than at slice boundaries
    only. (w0, T, s, delta) are threaded, which is what makes the sliced run
    identical to an unsliced one -- the driver threads the trust-region radius
    across epochs on purpose, and a slice that dropped it would reset the trust
    region and quietly change the algorithm.
    """
    kw = dict(tol=TOL, max_gmres=MAX_GMRES, gmres_rtol=GMRES_RTOL, fd_eps=1e-6)
    hist, ledger = [], []
    n_res = n_jac = 0
    delta = None
    w, T, s = np.array(w0, dtype=float), float(T0), float(s0)
    reason = "max_newton_hit"
    r = float("nan")
    epochs_done = 0
    first = True
    while epochs_done < MAX_NEWTON:
        want = STALL_K if first else 1
        want = min(want, MAX_NEWTON - epochs_done)
        out = newton_hookstep_rpo(w, T, s, solver, max_newton=want,
                                  delta0=delta, **kw)
        first = False
        hist.extend(out["residual_history"])
        for e in out["ledger"]:
            e = dict(e)
            e["iteration"] = epochs_done + e["iteration"]
            ledger.append(e)
        n_res += out["n_residual_evals"]
        n_jac += out["n_jac_evals"]
        w, T, s = out["w0"], out["T"], out["s"]
        r = out["final_residual"]
        reason = out["reason"]
        epochs_done += max(0, len(out["residual_history"])
                           - (1 if out["reason"] == "converged" else 0))
        if out["ledger"]:
            delta = out["ledger"][-1]["delta_after"]
        if reason != "max_newton_hit":
            break
        # THE STALL TEST, at every k >= STALL_K. hist[k] is the residual BEFORE
        # epoch k, so len(hist)-1 is the last index with a value.
        k = len(hist) - 1
        if k >= STALL_K and k - STALL_W >= 0:
            if hist[k] > STALL_HALVE * hist[k - STALL_W]:
                reason = "stalled"
                break
    return dict(success=bool(r < TOL), w0=w, T=T, s=s,
                n_iters=len(hist) - 1, residual_history=[float(v) for v in hist],
                final_residual=float(r), reason=reason, ledger=ledger,
                n_residual_evals=n_res, n_jac_evals=n_jac)


def run_attempt(job):
    idx, w0, T0, s0, meta = job
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    t0 = time.time()
    out = solve_with_stall_exit(w0, T0, s0, solver)
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
        residual_history=out["residual_history"],
        T_converged=out["T"], s_converged=out["s"],
        abs_s_converged=wrap_abs(out["s"]),
        delta_T_from_published=abs(out["T"] - meta["T_published"]),
        delta_s_from_published=float(ds),
        recovered_named_orbit=recovered,
        D_over_Dlam=D / solver.D_lam, I_over_Dlam=I / solver.D_lam,
        n_jac_evals=out["n_jac_evals"], n_residual_evals=out["n_residual_evals"],
        krylov_dims=[e["krylov_dim"] for e in out["ledger"]],
        radius_trials=[e["n_radius_trials"] for e in out["ledger"]],
        wall_seconds=wall)
    rec["_ledger"] = out["ledger"]
    rec["_w0"] = out["w0"]
    return rec


def allocate(lib, n_attempts):
    """The QUOTA RULE of AMENDMENT 5 section 3g.4, and nothing else.

    Filters are U3's, applied in U3's order: in_newton_window (R < 0.25), then
    m == 0, then anchored to a named row. Only the SELECTION off the survivors
    differs -- ranked by R WITHIN stratum instead of globally, which is exactly
    the AMENDMENT 4 move one coordinate over.
    """
    pool = []
    dropped_m = 0
    for c in lib["candidates"]:
        if not c["in_newton_window"]:
            continue
        if c["m"] != 0:
            dropped_m += 1
            continue
        a = anchor_of(c["T"])
        if a is None:
            continue
        abs_s = c.get("abs_s_wrapped")
        abs_s = wrap_abs(c["s"]) if abs_s is None else float(abs_s)
        pool.append(dict(c=c, anchor=a, abs_s=abs_s,
                         stratum=stratum_of(abs_s)))
    supply = {k: [p for p in pool if p["stratum"] == k]
              for k, _, _, _, _ in STRATA}
    for v in supply.values():
        v.sort(key=lambda p: p["c"]["R"])

    def diverse(chosen, p):
        for q in chosen:
            if (abs(q["c"]["snapshot_earlier"] - p["c"]["snapshot_earlier"])
                    <= DIVERSITY_DSNAP
                    and abs(q["c"]["T"] - p["c"]["T"]) <= DIVERSITY_DT):
                return False
        return True

    chosen = []
    skipped = {k: 0 for k, _, _, _, _ in STRATA}
    per_stratum = {k: [] for k, _, _, _, _ in STRATA}
    quotas = {k: q for k, _, _, _, q in STRATA}
    taken = set()  # by identity: two distinct minima can compare equal by value

    # Stratum P is filled per named row first, so no single row can absorb the
    # band's budget, then topped up from the rest of the band by lowest R.
    by_row = {}
    for p in supply["P"]:
        by_row.setdefault(p["anchor"][0], []).append(p)
    for name, _, _, _ in TABLE_IV:
        for p in by_row.get(name, []):
            if len(per_stratum["P"]) >= quotas["P"]:
                break
            if sum(1 for q in per_stratum["P"]
                   if q["anchor"][0] == name) >= PER_ROW_CAP_P:
                break
            if diverse(per_stratum["P"], p):
                per_stratum["P"].append(p)
                taken.add(id(p))
            else:
                skipped["P"] += 1
    for key in ("P", "L", "M", "H"):
        for p in supply[key]:
            if len(per_stratum[key]) >= quotas[key]:
                break
            if id(p) in taken:
                continue
            if diverse(per_stratum[key], p):
                per_stratum[key].append(p)
                taken.add(id(p))
            else:
                skipped[key] += 1

    # SHORTFALL: redistribute P -> L -> M -> H, in that order.
    short = sum(max(0, quotas[k] - len(per_stratum[k]))
                for k, _, _, _, _ in STRATA)
    realised_quota_before_shortfall = {k: len(v) for k, v in per_stratum.items()}
    for key in SHORTFALL_ORDER:
        if short <= 0:
            break
        for p in supply[key]:
            if short <= 0:
                break
            if id(p) in taken:
                continue
            if diverse(per_stratum[key], p):
                per_stratum[key].append(p)
                taken.add(id(p))
                short -= 1
    for k, _, _, _, _ in STRATA:
        chosen.extend(per_stratum[k])
    chosen = chosen[:n_attempts]

    funnel = dict(
        n_candidates=len(lib["candidates"]),
        n_in_newton_window=sum(1 for c in lib["candidates"]
                               if c["in_newton_window"]),
        n_zero_y_shift=sum(1 for c in lib["candidates"]
                           if c["in_newton_window"] and c["m"] == 0),
        n_anchored=len(pool),
        n_requested=n_attempts,
        short_of_requested=max(0, n_attempts - len(chosen)),
        supply_by_stratum={k: len(v) for k, v in supply.items()},
        quota_by_stratum=quotas,
        realised_by_stratum={k: len(v) for k, v in per_stratum.items()},
        realised_before_shortfall=realised_quota_before_shortfall,
        diversity_skips_by_stratum=skipped,
        candidates_dropped_for_nonzero_y_shift=dropped_m,
        per_row_in_band_supply={n: len(by_row.get(n, []))
                                for n, _, _, _ in TABLE_IV})
    return chosen, funnel


def u3_baseline():
    """U3's per-stratum yield, re-derived from banked JSON, never from prose."""
    with open(U3_BANKED) as f:
        u3 = json.load(f)
    rows = []
    for a in u3["attempts"]:
        rows.append((wrap_abs(a["s_seed"]), bool(a["success"]),
                     float(a["R_seed"])))
    out = {}
    for key, _, _, _, _ in STRATA:
        g = [r for r in rows if stratum_of(r[0]) == key]
        out[key] = dict(n=len(g), n_converged=sum(1 for r in g if r[1]),
                        rate=(sum(1 for r in g if r[1]) / len(g)) if g else None,
                        median_seed_R=(float(np.median([r[2] for r in g]))
                                       if g else None))
    band = [r for r in rows if PUBLISHED_BAND[0] <= r[0] <= PUBLISHED_BAND[1]]
    outside = [r for r in rows if not (PUBLISHED_BAND[0] <= r[0]
                                       <= PUBLISHED_BAND[1])]
    return dict(
        source=os.path.relpath(U3_BANKED, ROOT),
        by_stratum=out,
        in_published_band=dict(n=len(band),
                               n_converged=sum(1 for r in band if r[1])),
        outside_published_band=dict(n=len(outside),
                                    n_converged=sum(1 for r in outside if r[1])),
        n_attempts=len(rows),
        n_converged=sum(1 for r in rows if r[1]),
        n_recovered=int(u3["gate"]["n_recovered"]),
        caps=dict(max_newton=u3["resourcing"]["max_newton"],
                  max_gmres=u3["resourcing"]["max_gmres"],
                  gmres_rtol=u3["resourcing"]["gmres_rtol"],
                  tol=u3["resourcing"]["tol"]),
        epochs=sum(len(a["residual_history"]) - 1 for a in u3["attempts"]),
        wall_seconds=u3["magnitudes"]["wall_seconds"],
        workers=u3["magnitudes"]["workers"])


def replay_stall_rule_on_u3():
    """The stall rule's validation, recomputed here rather than quoted.

    A rule fitted on U3's convergences and then applied to U5's is only
    admissible if the fit is re-derivable, so it is re-run against the banked
    histories every time U5 runs.
    """
    with open(U3_BANKED) as f:
        u3 = json.load(f)
    lost, tot, base, worst = 0, 0, 0, 0.0
    for a in u3["attempts"]:
        h = a["residual_history"]
        n = len(h) - 1
        base += n
        stop = n
        for k in range(STALL_K, n + 1):
            if k - STALL_W < 0:
                continue
            ratio = h[k] / h[k - STALL_W]
            if a["success"] and ratio > worst:
                worst = ratio
            if ratio > STALL_HALVE * 1.0:
                stop = k
                break
        tot += stop
        if a["success"] and stop < n:
            lost += 1
    return dict(rule=(f"from epoch {STALL_K}, stop if ||R||_k > "
                      f"{STALL_HALVE} * ||R||_(k-{STALL_W})"),
                u3_epochs_baseline=base, u3_epochs_under_rule=tot,
                fraction_of_u3_epochs=tot / base,
                u3_convergences_lost=lost,
                worst_convergence_ratio_at_k_ge_K=worst,
                margin_factor=(STALL_HALVE / worst) if worst else None,
                admissible=bool(lost == 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-attempts", type=int, default=100)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--lib", default=LIB5 if os.path.exists(LIB5)
                    else LIB5_REDUCED)
    ap.add_argument("--out", default=CURATED)
    ap.add_argument("--ledger-out", default=LEDGER)
    args = ap.parse_args()

    # Drift guards. Two copies of a published table is one more than is safe,
    # and so is a hand-copied cap: both are checked against their sources.
    assert [(n, T) for n, T, _, _ in TABLE_IV] == _U2_TABLE_IV_PERIODS
    assert T_ANCHOR_TOL == _U2_T_ANCHOR_TOL
    base = u3_baseline()
    assert base["caps"] == dict(max_newton=MAX_NEWTON, max_gmres=MAX_GMRES,
                                gmres_rtol=GMRES_RTOL, tol=TOL), (
        "U5's caps do not match U3's BANKED caps -- U5 must not buy or sell "
        "iterations relative to U3 (AMENDMENT 5 section 3g.1(d))")
    stall = replay_stall_rule_on_u3()
    assert stall["admissible"], (
        "the stall rule cuts a U3 convergence -- it is not admissible and the "
        "run must not start (AMENDMENT 5 section 3g.5)")
    print(f"stall rule: {stall['fraction_of_u3_epochs']:.1%} of U3's epochs, "
          f"{stall['u3_convergences_lost']} convergences lost, margin factor "
          f"{stall['margin_factor']:.1f}x", flush=True)

    with open(args.lib) as f:
        lib = json.load(f)
    assert lib["held_fixed_at_U3_values"]["R_thres_window"] == R_THRES_WINDOW

    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    chosen, funnel = allocate(lib, args.n_attempts)
    n_band = sum(1 for p in chosen
                 if PUBLISHED_BAND[0] <= p["abs_s"] <= PUBLISHED_BAND[1])
    print(f"allocated {len(chosen)} attempts; {n_band} in the published band "
          f"(U3 had {base['in_published_band']['n']}); by stratum "
          f"{funnel['realised_by_stratum']}", flush=True)
    if not chosen:
        raise SystemExit("no anchored candidates -- STOP and escalate rather "
                         "than run an unanchored search (Ban 2)")

    with open(META) as f:
        dns_meta = json.load(f)
    ckpt = np.load(CKPT, mmap_mode="r")
    steps_per_snap = int(round(DT_SAVE / DT))
    snaps = regenerate([p["c"]["snapshot_earlier"] for p in chosen], solver,
                       ckpt, steps_per_snap)

    jobs = []
    sign_tally = {"plus": 0, "minus": 0}
    for i, p in enumerate(chosen):
        c, a = p["c"], p["anchor"]
        name, Tp, sp, mp_ = a
        w0 = snaps[c["snapshot_earlier"]]
        # The shift sign is MEASURED, not assumed -- this module cost the repo
        # a real sign bug once (leg 353) and U3 re-measured it at the point of
        # use for the same reason.
        r_plus = seed_residual(w0, c["T"], c["s"], solver)
        r_minus = seed_residual(w0, c["T"], -c["s"], solver)
        s0 = c["s"] if r_plus <= r_minus else -c["s"]
        sign_tally["plus" if r_plus <= r_minus else "minus"] += 1
        jobs.append((i, w0, c["T"], s0,
                     dict(anchor=name, T_published=Tp, s_published=sp,
                          m_published=mp_, R_seed=c["R"], T_seed=c["T"],
                          s_seed=s0, abs_s_seed=p["abs_s"],
                          stratum=p["stratum"],
                          abs_s_published=wrap_abs(sp),
                          seed_residual_plus=r_plus,
                          seed_residual_minus=r_minus,
                          seed_extended_residual=min(r_plus, r_minus),
                          snapshot_earlier=c["snapshot_earlier"])))

    t0 = time.time()
    results = []
    with mp.Pool(args.workers) as pool:
        for rec in pool.imap_unordered(run_attempt, jobs, chunksize=1):
            results.append(rec)
            el = time.time() - t0
            nc = sum(1 for r in results if r["success"])
            nr = sum(1 for r in results if r["recovered_named_orbit"])
            msg = (f"attempts {len(results)}/{len(jobs)}  converged {nc}  "
                   f"recovered_named {nr}  elapsed {el/3600:.2f} h  "
                   f"ETA {el/len(results)*(len(jobs)-len(results))/3600:.2f} h")
            print(msg, flush=True)
            with open(PROGRESS, "w") as f:
                f.write(msg + "\n")
    wall = time.time() - t0
    results.sort(key=lambda r: r["attempt"])

    ledgers = [{"attempt": r["attempt"], "anchor": r["anchor"],
                "stratum": r["stratum"], "ledger": r.pop("_ledger")}
               for r in results]
    orbit_states, saved = {}, {}
    for r in results:
        w = r.pop("_w0")
        if r["success"]:
            orbit_states[r["attempt"]] = w
            saved[f"attempt{r['attempt']:03d}_{r['stratum']}_"
                  f"{r['anchor']}"] = w
    if saved:
        np.savez_compressed(ORBITS, **saved)
        print(f"saved {len(saved)} converged states to {ORBITS}")

    print("running the planted controls ...", flush=True)
    t0 = time.time()
    ctrl_P = u3_controls.control_P(solver, TOL, MAX_NEWTON, MAX_GMRES,
                                   GMRES_RTOL)
    n_w0, n_meta = jobs[0][1], jobs[0][4]
    ctrl_N = u3_controls.control_N(
        solver, n_w0, n_meta["T_published"], n_meta["s_published"], TOL,
        MAX_NEWTON, MAX_GMRES, GMRES_RTOL, MATCH_T_TOL, MATCH_S_TOL, TABLE_IV)
    recovered = [r for r in results if r["recovered_named_orbit"]]
    converged = [r for r in results if r["success"]]
    ctrl_R = None
    if converged:
        best = min(converged, key=lambda r: r["final_residual"])
        ctrl_R = u3_controls.control_R(
            solver, orbit_states[best["attempt"]], best["T_converged"],
            best["s_converged"], best["anchor"], TOL, MAX_NEWTON, MAX_GMRES,
            GMRES_RTOL)
    controls_fired, control_failures = u3_controls.verdict(ctrl_P, ctrl_N,
                                                           ctrl_R)
    controls_wall = time.time() - t0
    print(f"controls: P={ctrl_P['recovered']} N={ctrl_N['recovered']} "
          f"(must be False) R={None if ctrl_R is None else ctrl_R['recovered']}"
          f" -> FIRED AS PLANTED = {controls_fired}", flush=True)

    # ---- per-stratum yield, the measurement M3 clause 4 asks for ----------
    by_stratum = {}
    for key, label, lo, hi, quota in STRATA:
        g = [r for r in results if r["stratum"] == key]
        cv = [r for r in g if r["success"]]
        by_stratum[key] = dict(
            label=label, abs_s_range=[lo, float(hi)], quota=quota,
            n=len(g), n_converged=len(cv),
            rate=(len(cv) / len(g)) if g else None,
            n_recovered=sum(1 for r in g if r["recovered_named_orbit"]),
            median_seed_R=(float(np.median([r["R_seed"] for r in g]))
                           if g else None),
            best_final_residual=(min(r["final_residual"] for r in g)
                                 if g else None),
            u3_baseline=base["by_stratum"][key])
    band_rows = [r for r in results
                 if PUBLISHED_BAND[0] <= r["abs_s_seed"] <= PUBLISHED_BAND[1]]

    # M3's own verdict, by the pre-registered rule and nothing else.
    # Clause 1 is a check on the mining, not a restatement of it: every taken
    # candidate was mined (no truncation), everything taken is below the window
    # threshold, and everything dropped was dropped by the lossless prune alone.
    mr = lib["mining_rule"]
    clause = dict(
        c1_mining_exhaustive=bool(
            mr["n_taken"] == len(lib["candidates"])
            and mr["R_red_max_taken"] < R_THRES_WINDOW
            and mr["n_taken"] > mr["n_taken_by_U2_for_comparison"]),
        c2_band_at_least_50=bool(len(band_rows) >= 50),
        c3_unchanged_settings=True,
        c4_yield_reported=True,
        c5_controls_fired=bool(controls_fired))
    if not clause["c5_controls_fired"] or not clause["c1_mining_exhaustive"]:
        # c1 failing means the mining truncated something it said it took: that
        # is the instrument not doing what it claims, which is INSTRUMENT.
        answer, reason = "NOT DELIVERED", "INSTRUMENT"
    elif not clause["c2_band_at_least_50"]:
        answer, reason = "NOT DELIVERED", "SUPPLY"
    elif len(results) < args.n_attempts:
        answer, reason = "NOT DELIVERED", "BUDGET"
    else:
        answer, reason = "DELIVERED", None

    finals = sorted(r["final_residual"] for r in results)
    epochs = sum(r["n_iters"] for r in results)
    record = dict(
        unit="U5", kind="BUILD (milestone M3)", programme="PROG-R4",
        milestone=dict(
            question=("M3: THE SEED BUDGET IS STRATIFIED BY SHIFT -- the "
                      "anchored reservoir is exhausted, the published |s| band "
                      "is filled to a pre-committed quota, and the per-stratum "
                      "yield is measured against U3's banked baseline"),
            answer=answer, not_delivered_reason=reason, clauses=clause,
            preregistered=("experiments/journal/"
                           "prog_r4_u2u3_prereg_addendum.md section 3g "
                           "(AMENDMENT 5), committed before either stage ran"),
            does_not_reanswer_G1=(
                "G1 stays UNDER-RESOURCED as banked in "
                "writeup/data/p2_prog_r4_g1_v1.json, which this unit does not "
                "write to. n_recovered below is a COUNT, not a gate answer; "
                "n_recovered > 0 would be a CANDIDATE G1 RE-OPEN to raise to "
                "the user, and n_recovered = 0 re-answers nothing and is not "
                "a `no` at G1 -- `no` is still not an available branch there."),
            n_recovered=len(recovered),
            n_converged_to_tol=len(converged),
            n_attempts=len(results),
            n_seeded_in_published_band=len(band_rows),
            ceiling=("TIER 2. No L1-L4 link is moved by this unit and nothing "
                     "in it is movement toward Clay; Clay stays ~0.05%."),
            unverified=("SOLO MODE (ORCHESTRATION.md section 3f): built and "
                        "checked in one session, no fresh session re-derived "
                        "it from banked JSON, so this milestone is UNVERIFIED "
                        "in section 3f's sense. The planted controls, the "
                        "bit-for-bit mining checks, the figure's checks and "
                        "the merge gate are the whole defence.")),
        stratification=dict(
            quota_rule=[dict(stratum=k, label=lab, lo=lo, hi=float(hi),
                             quota=q) for k, lab, lo, hi, q in STRATA],
            per_row_cap_in_band=PER_ROW_CAP_P,
            diversity_rule=dict(d_snapshot=DIVERSITY_DSNAP, d_T=DIVERSITY_DT),
            shortfall_order=SHORTFALL_ORDER,
            by_stratum=by_stratum,
            u3_baseline=base),
        controls=dict(
            preregistered=("addendum section 3, unchanged, plus section 3g.6's "
                           "two structural controls (stratum L positive on the "
                           "pipeline, stratum H against the monotone-in-|s| "
                           "reading)"),
            rule="FIRED AS PLANTED := P recovered AND N did not recover AND "
                 "(R recovered, if R ran)",
            fired_as_planted=controls_fired, failures=control_failures,
            P=ctrl_P, N=ctrl_N,
            R=ctrl_R if ctrl_R is not None else
              "NOT RUN -- nothing converged, so there was no orbit to perturb",
            structural=dict(
                L_positive_on_pipeline=by_stratum["L"],
                H_against_monotone_in_shift=by_stratum["H"]),
            wall_seconds=controls_wall),
        resourcing=dict(
            T_dns=dns_meta["T_recorded"], N=N_GRID, Re=RE,
            globalisation="genuine Newton-GMRES-hookstep trust region (U1)",
            n_attempts=len(results), tol=TOL, max_newton=MAX_NEWTON,
            max_gmres=MAX_GMRES, gmres_rtol=GMRES_RTOL,
            caps_identical_to_U3=True,
            stall_exit=stall,
            epochs_spent=epochs, u3_epochs_spent=base["epochs"],
            workers=args.workers,
            workers_note=("8, not U3's 10: a measured contention probe on this "
                          "6-core machine put throughput at 3.11/3.22/2.91/"
                          "2.75 eval/s at 6/8/10/12 workers, so U3 ran past "
                          "the optimum -- the mechanism erratum (ii) suspected"),
            scheduling=("imap_unordered chunksize=1, which repairs erratum (i) "
                        "(Pool.map chunking left U3's tail worker 12 attempts) "
                        "and is what makes progress reporting possible"),
            seconds_per_epoch_costed_at=95.0,
            options_not_taken=dict(
                b_relax_admission_test="NOT TAKEN -- R_thres_window stays 0.25",
                c_m_unknown_in_residual="NOT TAKEN -- m=0 requirement stands",
                d_buy_iterations=("NOT TAKEN -- caps identical to U3; U5 spends "
                                  "FEWER epochs via the validated stall exit"))),
        seed=dict(
            source="Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV",
            rows=[t[0] for t in TABLE_IV],
            anchor_rule=f"|T_candidate - T_published| <= {T_ANCHOR_TOL}",
            ban1="PASS - no step continues a fixed point into an orbit",
            ban2="PASS - every attempt anchored to a named row; an unanchored "
                 "attempt would STOP and escalate, not report",
            shift_sign_measured_not_assumed=sign_tally,
            seed_supply_funnel=funnel,
            mining=dict(
                rule=lib["mining_rule"],
                regeneration_checks=lib["regeneration"],
                counts=lib["counts"])),
        realization=dict(
            finding=("unchanged from U3: the stepper is a Lie-Trotter split, "
                     "FIRST order in time (measured global ratio 2.00), and "
                     "the extended residual carries a continuous x-shift only, "
                     "so the m != 0 class cannot be expressed as a seed"),
            lesson_91=("any negative this unit reports carries both clauses, "
                       "plus its own: the seed pool is now shift-STRATIFIED "
                       "rather than shift-biased, which is the one thing that "
                       "changed")),
        magnitudes=dict(
            final_residuals_sorted=finals,
            best_final_residual=finals[0] if finals else None,
            median_final_residual=float(np.median(finals)) if finals else None,
            seed_residuals=[r["seed_extended_residual"] for r in results],
            reasons={k: sum(1 for r in results if r["reason"] == k)
                     for k in sorted({r["reason"] for r in results})},
            by_anchor={k: dict(n=sum(1 for r in results if r["anchor"] == k),
                               best=min([r["final_residual"] for r in results
                                         if r["anchor"] == k]))
                       for k in sorted({r["anchor"] for r in results})},
            total_jac_evals=sum(r["n_jac_evals"] for r in results),
            wall_seconds=wall, workers=args.workers),
        open_obligations_carried=[
            "CLAY_OBLIGATIONS section 6, obligation 1 (no method) -- OPEN",
            "CLAY_OBLIGATIONS section 6, obligation 2 (no method) -- OPEN",
            ("CLAY_OBLIGATIONS section 4 -- OPEN and NOT discharged; stays "
             "open in every route-4 gate until leg 386 (ROUTE-DTOL) lands "
             "with a pre-registered delta mode (user ruling, 2026-08-12)"),
        ],
        clay_movement="none -- no L1-L4 link moved by this unit",
        attempts=results,
    )
    with open(args.out, "w") as f:
        json.dump(record, f, indent=2)
    with open(args.ledger_out, "w") as f:
        json.dump(dict(unit="U5", programme="PROG-R4",
                       note="per-Newton-iteration ledger for every attempt",
                       attempts=ledgers), f, indent=2)

    print(f"M3 = {answer}" + (f" ({reason})" if reason else ""))
    print(f"  {len(recovered)} recovered a named row, {len(converged)} "
          f"converged to tol, {len(results)} attempts, {wall/3600:.2f} h, "
          f"{epochs} epochs (U3 spent {base['epochs']})")
    for k, _, _, _, _ in STRATA:
        b = by_stratum[k]
        print(f"  stratum {k} ({b['label']:9s}): {b['n_converged']:3d}/"
              f"{b['n']:3d} converged, {b['n_recovered']} recovered  "
              f"| U3: {b['u3_baseline']['n_converged']}/{b['u3_baseline']['n']}")
    print(f"wrote {args.out} and {args.ledger_out}")


if __name__ == "__main__":
    main()
