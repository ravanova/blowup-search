"""PROG-R4, unit U5, stage 1 of 2 -- the SHIFT-stratified seed pool, supply side.

Pre-registered in experiments/journal/prog_r4_u2u3_prereg_addendum.md section
3g (AMENDMENT 5), committed BEFORE this file was run.

WHAT THIS DOES, AND WHAT IT DELIBERATELY DOES NOT DO.

U3 measured the cause of its miss: the Newton window R < 0.25 is monotone in
|s|, admitting 44% of candidates at |s| < 0.15 and 11% in the published band
|s| in [0.295, 0.707]. AMENDMENT 4 had already fixed the same bug one dimension
over, in PERIOD, by stratifying the mining budget. The obvious move is to
stratify the mining budget by SHIFT too -- and it is not available, because
SHIFT IS NOT OBSERVABLE AT THE PREFILTER. R_red is built from amplitude
spectra and is shift-invariant by construction; that invariance is exactly what
makes the prefilter lossless, and it is what makes period stratifiable at that
stage and shift not.

So the mining does not stratify. It EXHAUSTS:

    take every anchored strict local minimum of R_red with R_red < 0.25

and the stratification happens downstream, in u5_g1_stratified.py, at the only
stage where |s| exists. The R_red < 0.25 cut is LOSSLESS and is not a tuning:
the prefilter's own recorded statement is R_red <= R pointwise, so a cell with
R_red >= 0.25 cannot have R < 0.25 and is provably outside the Newton window
already. With no ranking and no truncation there is no per_anchor and no
researcher degree of freedom left in the take -- which is the one thing
AMENDMENT 4 had to close with a written rule instead.

WHAT IS HELD FIXED AT U2/U3's VALUES, so that "which seeds are offered" is the
only manipulated variable:
  * R_THRES_WINDOW = 0.25            (U3 option (b) NOT taken)
  * the m = 0 requirement            (U3 option (c) NOT taken)
  * T_ANCHOR_TOL = 1.0 and the eight named Table IV periods
  * full_R, the continuous-x/discrete-y minimisation of C&K eq. (23)
  * the stepper, bit for bit -- the snapshots below are the SAME snapshots

COST. The take touches 3,980 of the trajectory's 3,997 checkpoint blocks, i.e.
essentially the whole T=1e5 DNS has to be replayed from its checkpoints. Serial,
that is ~3.3 h. The replay is block-independent by construction -- each block
starts from its own stored complex128 checkpoint and applies a deterministic
step sequence -- so it is done in parallel here, which is a scheduling change
and not a numerical one. AMENDMENT 5 section 3g.6 requires that to be CHECKED
rather than argued: --verify-regen replays a sample of indices through U2's own
serial regenerate() and requires BIT-FOR-BIT equality. A mismatch aborts.

Usage:
    python experiments/programme_r4/u5_shift_mining.py [--workers 8]
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

from solver.kolmogorov2d_nkbasin import Kolmogorov2D  # noqa: E402
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    CKPT, CKPT_EVERY, DT, DT_SAVE, FEAT, META, N_FORCING, N_GRID, RE,
    R_THRES_RECORD, R_THRES_WINDOW, TABLE_IV_PERIODS, T_ANCHOR_TOL, T_WINDOW,
    full_R, regenerate,
)

HERE = os.path.dirname(os.path.abspath(__file__))
LIB5 = os.path.join(HERE, "u5_shift_library.json")
PROGRESS = os.path.join(HERE, "u5_mining_progress.txt")

# Everything below is imported or derived; nothing here is a new threshold.
STEPS_PER_SNAP = int(round(DT_SAVE / DT))

_G = {}


def _init(n_snap):
    """One solver and one memory-mapped checkpoint array per worker."""
    _G["solver"] = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    _G["ckpt"] = np.load(CKPT, mmap_mode="r")
    _G["n_snap"] = n_snap


def _regen_indices(indices):
    """U2's serial regenerate(), restricted to one checkpoint block at a time.

    THE OFF-BY-ONE THIS FUNCTION EXISTS TO GET RIGHT. `ckpt[b]` is the state the
    DNS held BEFORE the steps that produce snapshot `b*CKPT_EVERY` -- run_dns
    writes the checkpoint at the top of the loop body -- so it corresponds to
    index `b*CKPT_EVERY - 1`, and reaching snapshot `k` costs
    `(k % CKPT_EVERY + 1)` snapshot advances, not `k % CKPT_EVERY`. The first
    version of this file started the walk at `b*CKPT_EVERY` and produced
    snapshots one DT_SAVE early; the bit-for-bit check of AMENDMENT 5 section
    3g.6 caught it before a single candidate was mined, which is the only
    reason it is a footnote rather than 75,873 wrong candidates.

    The loop below is U2's, structurally: sorted indices, restart on block
    change, walk forward. Restricting a walk to its own block is a no-op
    against U2 -- U2 restarts on every block change too -- so the two agree by
    construction and not by argument.
    """
    solver, ckpt = _G["solver"], _G["ckpt"]
    out = {}
    cur_block, w_hat, pos = -1, None, -1
    for idx in sorted(set(int(i) for i in indices)):
        block = idx // CKPT_EVERY
        if block != cur_block or pos > idx:
            w_hat = np.array(ckpt[block])
            cur_block = block
            pos = block * CKPT_EVERY - 1
        while pos < idx:
            for _ in range(STEPS_PER_SNAP):
                w_hat = solver._rk4_step(w_hat, DT)
            pos += 1
        out[idx] = np.fft.ifft2(w_hat).real
    return out


def _do_group(job):
    """Full minimisation for a contiguous RUN of checkpoint blocks.

    Each block is replayed FROM ITS OWN CHECKPOINT, exactly as U2's serial
    regenerate() does, rather than by walking across block boundaries. Walking
    across would almost certainly reproduce the next checkpoint bit for bit --
    the DNS did that very walk -- but "almost certainly" is not the standard
    here, and replaying per block makes identity with U2's path true by
    construction instead of by argument.

    A candidate spans at most T_max = 20.334 t.u. = 82 snapshots < CKPT_EVERY =
    100, so a run of B blocks needs B + 1 blocks replayed. Grouping blocks into
    runs is what keeps that boundary overhead at ~1/B instead of 1x. Only
    (R, s, m) travels back: the 98,413 snapshots are discarded per group, which
    is what keeps 75,873 candidates inside memory.
    """
    cands = job
    solver = _G["solver"]
    need = set()
    for _, it, lag in cands:
        need.add(it)
        need.add(it - lag)
    snaps = _regen_indices(need)
    out = []
    for rred, it, lag in cands:
        # C&K index R(t, T) with the LATER time t; w1 is the later snapshot and
        # the recovered shift carries the earlier state onto it. Same
        # convention as U2, and the sign is re-measured at the point of use in
        # the attempts stage exactly as U3 did.
        R, s, m = full_R(snaps[it], snaps[it - lag], solver)
        out.append((float(R), float(rred), float(s), int(m),
                    int(lag), int(it)))
    return out


def prefilter(n_snap):
    """U2's prefilter scan and strict-local-minimum selection, byte for byte.

    Not re-derived and not re-tuned: the plane, the R_THRES_RECORD test and the
    eight-neighbour strict-minimum test are the same code path U2 ran, so the
    913,301 minima below are the same 913,301.
    """
    feat = np.load(FEAT, mmap_mode="r")
    lag_lo = max(1, int(round(T_WINDOW[0] / DT_SAVE)))
    lag_hi = int(round(T_WINDOW[1] / DT_SAVE))
    t0 = time.time()
    F = np.asarray(feat[:n_snap], dtype=np.float32)
    den = np.maximum(np.einsum("ij,ij->i", F, F), 1e-30)
    n_t = n_snap - lag_hi
    n_lag = lag_hi - lag_lo + 1
    M = np.empty((n_t, n_lag), dtype=np.float32)
    for li, lag in enumerate(range(lag_lo, lag_hi + 1)):
        a = F[lag_hi:]
        b = F[lag_hi - lag:n_snap - lag]
        M[:, li] = np.einsum("ij,ij->i", a - b, a - b) / den[lag_hi:]
    C = M[1:-1, 1:-1]
    is_min = C < R_THRES_RECORD
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            is_min &= C < M[1 + di:n_t - 1 + di, 1 + dj:n_lag - 1 + dj]
    ii, jj = np.nonzero(is_min)
    vals = C[ii, jj].astype(np.float64)
    lag_of = jj.astype(np.int64) + 1 + lag_lo
    it_of = ii.astype(np.int64) + 1 + lag_hi
    del M, C, is_min, F, den
    return vals, it_of, lag_of, int(ii.size), time.time() - t0


def check_regen_bitwise(vals, it_of, lag_of, keep, n_sample, seed=0):
    """AMENDMENT 5 section 3g.6: the parallel replay must equal U2's serial one.

    Bit for bit, not to a tolerance. Both walks start from the same stored
    checkpoint and apply the same deterministic step sequence, so any
    difference at all is a defect in the partitioning, and a tolerance would
    hide exactly the off-by-one this check exists to catch.
    """
    rng = np.random.default_rng(seed)
    idx = np.nonzero(keep)[0]
    pick = rng.choice(idx, size=min(n_sample, idx.size), replace=False)
    want = sorted({int(it_of[p]) for p in pick}
                  | {int(it_of[p] - lag_of[p]) for p in pick})
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    ckpt = np.load(CKPT, mmap_mode="r")
    t0 = time.time()
    serial = regenerate(want, solver, ckpt, STEPS_PER_SNAP)
    _init(0)
    # Deliberately regenerated ONE AT A TIME, so each index pays its own
    # restart. That is the worst case for agreement, not the easiest: if the
    # block bookkeeping is wrong anywhere it shows up here.
    par = {}
    for i in want:
        par.update(_regen_indices([i]))
    n_bad = 0
    max_abs = 0.0
    for i in want:
        d = np.abs(serial[i] - par[i]).max()
        max_abs = max(max_abs, float(d))
        if not np.array_equal(serial[i], par[i]):
            n_bad += 1
    return dict(n_indices_checked=len(want), n_candidates_sampled=int(pick.size),
                n_mismatched=n_bad, max_abs_difference=max_abs,
                bit_for_bit=bool(n_bad == 0), wall_seconds=time.time() - t0)


def check_against_banked_library(n_sample, seed=0):
    """Reproduce U2's BANKED (R, s, m) for a sample of its own candidates.

    Stronger than the regeneration check on its own: it exercises the whole
    path -- snapshot indices, block bookkeeping, full_R's continuous-x and
    discrete-y minimisation -- against the landed artefact U2 and U3 actually
    used, rather than against another copy of this file's own logic. Exact
    equality is required for the same reason: same inputs, same operations, no
    tolerance to hide behind.
    """
    with open(os.path.join(HERE, "u2_recurrence_library.json")) as f:
        u2 = json.load(f)
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(u2["candidates"]),
                      size=min(n_sample, len(u2["candidates"])), replace=False)
    _init(0)
    n_bad = 0
    worst = 0.0
    for p in pick:
        c = u2["candidates"][int(p)]
        lag = c["snapshot_later"] - c["snapshot_earlier"]
        got = _do_group([(c["R_reduced"], c["snapshot_later"], lag)])[0]
        if not (got[0] == c["R"] and got[2] == c["s"] and got[3] == c["m"]):
            n_bad += 1
            worst = max(worst, abs(got[0] - c["R"]))
    return dict(n_sampled=int(pick.size), n_mismatched=n_bad,
                worst_abs_R_difference=worst, exact=bool(n_bad == 0),
                source="experiments/programme_r4/u2_recurrence_library.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--verify-sample", type=int, default=40)
    ap.add_argument("--blocks-per-job", type=int, default=8)
    ap.add_argument("--out", default=LIB5)
    args = ap.parse_args()

    with open(META) as f:
        meta = json.load(f)
    n_snap = meta["n_snapshots"]

    vals, it_of, lag_of, n_minima, pre_wall = prefilter(n_snap)
    T_of = lag_of * DT_SAVE
    anchored = np.zeros(vals.size, dtype=bool)
    anchor_name = np.full(vals.size, "", dtype=object)
    best_d = np.full(vals.size, np.inf)
    for name, T_pub in TABLE_IV_PERIODS:
        d = np.abs(T_of - T_pub)
        closer = d < best_d
        best_d = np.where(closer, d, best_d)
        anchor_name[closer] = name
        anchored |= d <= T_ANCHOR_TOL
    # anchor_name is the NEAREST named row; anchored requires it within
    # T_ANCHOR_TOL. Same rule as u3_g1_attempts.anchor_of, and UPO34 drawing
    # zero is a property of the published table's spacing (addendum section
    # 3d), not of this take.
    lossless = vals < R_THRES_WINDOW
    keep = anchored & lossless
    n_anchored_all = int(anchored.sum())
    n_keep = int(keep.sum())
    print(f"prefilter: {n_minima} strict local minima in {pre_wall:.1f}s; "
          f"{n_anchored_all} anchored; {n_keep} with R_red < {R_THRES_WINDOW} "
          f"(lossless prune, R_red <= R pointwise)", flush=True)

    ver = check_regen_bitwise(vals, it_of, lag_of, keep, args.verify_sample)
    print(f"regen check: {ver['n_indices_checked']} snapshots, "
          f"mismatched {ver['n_mismatched']}, max|diff| "
          f"{ver['max_abs_difference']:.3e}, bit_for_bit={ver['bit_for_bit']}",
          flush=True)
    if not ver["bit_for_bit"]:
        raise SystemExit("PARALLEL REGENERATION IS NOT BIT-FOR-BIT IDENTICAL "
                         "TO U2's SERIAL regenerate() -- aborting the mining "
                         "pass rather than mining on states that are not the "
                         "states U2 and U3 used (AMENDMENT 5 section 3g.6)")

    rep = check_against_banked_library(args.verify_sample)
    print(f"banked-library check: {rep['n_sampled']} U2 candidates re-mined, "
          f"mismatched {rep['n_mismatched']}, exact={rep['exact']}", flush=True)
    if not rep["exact"]:
        raise SystemExit("U5's mining path does not reproduce U2's BANKED "
                         "(R, s, m) -- aborting rather than mining a pool "
                         "that is not comparable with U3's")

    sel = np.nonzero(keep)[0]
    groups = {}
    for p in sel:
        it = int(it_of[p])
        groups.setdefault(it // CKPT_EVERY, []).append(
            (float(vals[p]), it, int(lag_of[p])))
    # Contiguous runs of BLOCKS_PER_JOB blocks, so the one-block boundary
    # overhead is amortised (~1/8) instead of paid per block (~1x).
    blocks = sorted(groups)
    jobs = []
    for i in range(0, len(blocks), args.blocks_per_job):
        run = blocks[i:i + args.blocks_per_job]
        job = []
        for b in run:
            job.extend(groups[b])
        jobs.append(job)
    print(f"{len(blocks)} checkpoint blocks to replay in {len(jobs)} runs of "
          f"{args.blocks_per_job}, {n_keep} candidates, {args.workers} workers",
          flush=True)

    t0 = time.time()
    cands = []
    done = 0
    with mp.Pool(args.workers, initializer=_init, initargs=(n_snap,)) as pool:
        for out in pool.imap_unordered(_do_group, jobs, chunksize=1):
            cands.extend(out)
            done += 1
            if done % 20 == 0 or done == len(jobs):
                el = time.time() - t0
                eta = el / done * (len(jobs) - done)
                msg = (f"mining {done}/{len(jobs)} block-runs  "
                       f"{len(cands)} candidates  "
                       f"elapsed {el/60:.1f} min  ETA {eta/60:.1f} min")
                print(msg, flush=True)
                with open(PROGRESS, "w") as f:
                    f.write(msg + "\n")
    mine_wall = time.time() - t0

    TWO_PI = 2.0 * np.pi
    out = []
    for R, rred, s, m, lag, it in cands:
        out.append(dict(R=R, R_reduced=rred, s=s,
                        abs_s_wrapped=float(abs((s + np.pi) % TWO_PI - np.pi)),
                        m=m, T=lag * DT_SAVE,
                        t_later=(it + 1) * DT_SAVE,
                        snapshot_later=it, snapshot_earlier=it - lag,
                        in_newton_window=bool(R < R_THRES_WINDOW)))
    out.sort(key=lambda c: c["R"])

    win = [c for c in out if c["in_newton_window"]]
    win_m0 = [c for c in win if c["m"] == 0]
    band = [c for c in win_m0 if 0.295 <= c["abs_s_wrapped"] <= 0.707]
    lib = dict(
        unit="U5", stage="mining", programme="PROG-R4",
        preregistered=("experiments/journal/prog_r4_u2u3_prereg_addendum.md "
                       "section 3g (AMENDMENT 5), committed before this ran"),
        thresholds=meta["sourced_thresholds"],
        mining_rule=dict(
            statement=("take EVERY anchored strict local minimum of R_red with "
                       "R_red < R_THRES_WINDOW; no ranking, no truncation, no "
                       "per_anchor"),
            why_not_stratified_at_the_prefilter=(
                "R_red is built from amplitude spectra and is shift-invariant "
                "by construction -- the same invariance that makes the "
                "prefilter lossless -- so |s| does not exist at this stage and "
                "cannot be stratified on here. Period can be and was "
                "(AMENDMENT 4); shift is stratified downstream in the budget."),
            lossless_prune=("R_red <= R pointwise (the prefilter's own recorded "
                            "statement), so R_red >= 0.25 provably cannot have "
                            "R < 0.25 and is already outside the Newton "
                            "window. Dropping it discards no admissible seed."),
            n_strict_local_minima=n_minima,
            n_anchored_all_depths=n_anchored_all,
            n_taken=n_keep,
            n_taken_by_U2_for_comparison=1614 + 400,
            R_red_max_taken=float(vals[keep].max()) if n_keep else None),
        regeneration=dict(
            scheme=("block-parallel replay from the stored complex128 "
                    "checkpoints; a scheduling change, not a numerical one"),
            workers=args.workers,
            n_blocks=len(blocks), n_block_runs=len(jobs),
            blocks_per_job=args.blocks_per_job,
            bitwise_check_against_U2_serial_regenerate=ver,
            exactness_check_against_U2_banked_library=rep,
            wall_seconds=mine_wall),
        prefilter=dict(wall_seconds=pre_wall,
                       n_strict_local_minima_in_the_t_T_plane=n_minima),
        counts=dict(
            n_candidates=len(out),
            n_in_newton_window=len(win),
            n_in_window_m0=len(win_m0),
            n_in_window_m0_published_band=len(band),
            best_R=out[0]["R"] if out else None),
        held_fixed_at_U3_values=dict(
            R_thres_window=R_THRES_WINDOW, m_zero_required=True,
            T_anchor_tol=T_ANCHOR_TOL,
            note=("U3 section 8's options (b) relax the admission test and (c) "
                  "add an m unknown are NOT taken by U5")),
        candidates=out,
        clay_movement="none -- no L1-L4 link moved by this stage",
    )
    with open(args.out, "w") as f:
        json.dump(lib, f)
    print(f"mined {len(out)} candidates in {mine_wall/60:.1f} min: "
          f"{len(win)} in window, {len(win_m0)} of those m=0, "
          f"{len(band)} of those in the published |s| band")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
