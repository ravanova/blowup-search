"""PROG-R4, unit U2 -- MILESTONE M2: the T=1e5 DNS and its recurrence library.

  ############################################################
  ##  STATUS 2026-08-12: MILESTONE M2 IS **ANSWERED**.      ##
  ##  A previous session was wound down with the DNS at 16% ##
  ##  and that partial run was abandoned. THIS UNIT WAS     ##
  ##  THEN RUN TO COMPLETION, from t=0, at the compliant    ##
  ##  scale: T=1e5, N=24, Re=60, dt=0.01, 400,000 snapshots ##
  ##  at dt_save=0.25, 3.44 h wall, 1.2379 ms/step, and the ##
  ##  trajectory sits on the chaotic attractor              ##
  ##  (D/D_lam = 0.0645 +/- 0.0253).                        ##
  ##                                                        ##
  ##  The recurrence library was mined from it: 95,542,640  ##
  ##  (t, T) pairs scanned, 913,301 strict interior local   ##
  ##  minima of the lossless prefilter, best R = 0.016543   ##
  ##  against leg 353's best of 0.177 for UPO37.            ##
  ##                                                        ##
  ##  M2 IS A MILESTONE, NOT A GATE. It says the instrument ##
  ##  and the data exist at the pre-registered scale. It    ##
  ##  says NOTHING about whether any named Table IV orbit   ##
  ##  recovers -- that is gate G1, unit U3.                 ##
  ##                                                        ##
  ##  UNVERIFIED under ORCHESTRATION.md section 3f: built   ##
  ##  and checked in the same session, with no paired       ##
  ##  verifier. Verification is a fresh session.            ##
  ############################################################

WHAT THIS UNIT IS. A build unit. It supplies the two things gate G1 needs and
leg 353 did not have: a DNS at the length the question is posed at, and a
recurrence-candidate library mined from it with thresholds taken from the
source papers rather than chosen here. No claim is made and no gate is
answered. G1 is unit U3.

WHY T=1e5 AND NOT T=2000. Leg 353 declared DNS length as one of its two
simplifications. Chandler & Kerswell 2013 (arXiv:1207.4682), the origin of
this Re=60 2-D Kolmogorov recurrent-flow search, ran T=1e5 per run at Re=60
(runs e, f, g). That is the SHORTEST sourced length, so it is what
"resourced at the scale the question is posed at" means here. Lucas & Kerswell
2015 ran T=5e6; that escalation is authorised in kind but is ~10.2 GPU-days
and the hardware is not present, so it is reported WITH G1's numbers rather
than assumed. All thresholds below are quoted from
writeup/data/p2_route_rpol_v1.json, which sourced them from the papers.

THE RECURRENCE MEASURE, taken from the source rather than invented. Chandler &
Kerswell eq. (23):

    R(t,T) := min_{0<=s<2pi} min_{m in 0..n-1}
              sum_jl |Omega_jl(t) e^{i alpha j s + 2 i m l pi / n}
                      - Omega_jl(t-T)|^2  /  sum_jl |Omega_jl(t)|^2

Three things about this were checked against the paper text directly, because
each is a place a re-implementation can silently diverge:

  1. R is a SQUARED quantity -- a ratio of sums of squared moduli, NOT
     ||.||/||.||. Leg 353's optimal_shift_residual already returns the squared
     form, so its recorded 0.177-0.263 were in the paper's own units and the
     comparison against the R<0.25 window was apples to apples. (This was
     verified, not assumed; the opposite convention would have meant leg 353's
     seeds were really at R~0.42, outside even the recording threshold, which
     would have changed how its null reads.)
  2. The minimisation runs over a DISCRETE y-shift m as well as the continuous
     x-shift s. Leg 353 minimised over s only. Omitting m can only make R
     larger, so this unit's library is a SUPERSET of what leg 353's measure
     would have found, in the source's own units.
  3. Thresholds at Re=60: recording R_thres = 0.3; the window actually fed to
     Newton in Lucas & Kerswell was R < 0.25 AND 0.5 < T < 60.

THE PREFILTER IS LOSSLESS, AND THAT IS A THEOREM NOT A HOPE. Scanning every
(t, T) pair with the full minimisation is too expensive. So a translation-
invariant proxy is computed first, on mode AMPLITUDES:

    R_red(t,T) := sum_jl (|Omega_jl(t)| - |Omega_jl(t-T)|)^2
                  / sum_jl |Omega_jl(t)|^2

Because |a - b| >= | |a| - |b| | for complex a, b, and because every symmetry
in the minimisation (continuous x-translation, discrete y-translation) acts by
multiplying each coefficient by a unit-modulus phase and so leaves every
|Omega_jl| fixed, we have R_red(t,T) <= R(t,T) POINTWISE. Therefore any pair
with R < theta also has R_red < theta: filtering on R_red at the SAME
threshold discards nothing. The amplitude vector is built from exactly the
dealiasing mask's support (289 retained modes for N=24), with the conjugate
half dropped, so there is no truncation loss either.

Ban screen (plan_of_record.py). This unit runs a DNS and mines it for
near-recurrences; it continues nothing and follows no branch, so Ban 1 does
not apply. Ban 2 does not apply because the search is SEEDED: the library is
mined to supply starting points for the eight NAMED Lucas & Kerswell Table IV
rows carried in writeup/novelty/prog_r4.md section 1, and candidates are
ranked against those published periods. This is re-screened at the point of
use in U3, where the seeds are actually consumed.

Stages (run separately; stage 1 is a multi-hour background job):
    python experiments/programme_r4/u2_m2_dns_recurrence.py --stage dns
    python experiments/programme_r4/u2_m2_dns_recurrence.py --stage recur
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from solver.kolmogorov2d_nkbasin import (  # noqa: E402
    Kolmogorov2D, dealias_mask2d, grid2d, optimal_shift_residual, shift_x,
    wavenumbers2d,
)

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- pre-registered scale and thresholds, all sourced --------------------
T_TOTAL = 1.0e5          # Chandler & Kerswell 2013 runs e,f,g at Re=60
T_BURN = 500.0           # transient discarded before recording
DT_SAVE = 0.25           # snapshot spacing
N_GRID, RE, N_FORCING, DT = 24, 60.0, 4, 0.01
R_THRES_RECORD = 0.30    # C&K recording threshold at Re=60
R_THRES_WINDOW = 0.25    # L&K's window actually fed to Newton
T_WINDOW = (0.5, 60.0)   # L&K's period window

CKPT_EVERY = 100         # snapshots between Fourier-space checkpoints (25 t.u.)

# STORAGE, and why it is not a full snapshot archive. Storing all 400,000
# snapshots as float32 would need ~1.2 GB and this machine has 1.5 GB free, so
# the archive is instead: (a) the amplitude features at every snapshot, which
# the pair scan needs and which are small, and (b) a Fourier-space checkpoint
# every 25 time units. Any snapshot is then regenerated by stepping forward
# from its preceding checkpoint. That is EXACT, not approximate: the
# checkpoints are the full complex128 state, and re-applying the same
# _rk4_step sequence to the same state reproduces the original run bit for
# bit. Cost of the choice is ~250 s of re-integration in the recurrence stage;
# benefit is ~280 MB instead of ~1.2 GB.
CKPT = os.path.join(HERE, "u2_dns_ckpt.npy")
FEAT = os.path.join(HERE, "u2_dns_feat.f32")
META = os.path.join(HERE, "u2_dns_meta.json")
LIB = os.path.join(HERE, "u2_recurrence_library.json")

# The eight named rows of Lucas & Kerswell 2015, arXiv:1406.1820v2, Table IV,
# as pre-registered by leg 353 and banked in writeup/data/p2_route_dsspb5_v1
# .json. Periods only -- the shifts are U3's business, not the library's. Held
# here rather than imported from u3_g1_attempts.py because that module imports
# THIS one; u3 asserts the two lists agree, so they cannot drift apart.
TABLE_IV_PERIODS = [
    ("UPO37", 19.334), ("UPO35", 18.912), ("UPO34", 18.878),
    ("UPO32", 18.694), ("UPO22", 17.160), ("UPO20", 16.908),
    ("UPO17", 16.753), ("UPO9", 14.776),
]
# Same value U3 anchors with (~5% at T~19), stated before the run.
T_ANCHOR_TOL = 1.0
PROGRESS = os.path.join(HERE, "u2_dns_progress.txt")


def amplitude_index(N):
    """Indices of the dealiasing mask's support, conjugate half removed.

    The real field's spectrum obeys Omega(-k) = conj(Omega(k)), so |Omega| on
    the half plane kx > 0, plus the kx == 0 column with ky >= 0, carries every
    independent amplitude exactly once. Keeping the whole mask would only
    double-count and double the scan cost."""
    mask = dealias_mask2d(N)
    KX, KY, _, _ = wavenumbers2d(N)
    keep = mask & ((KX > 0) | ((KX == 0) & (KY >= 0)))
    return np.nonzero(keep)


def run_dns(args):
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    _, Y = grid2d(N_GRID)
    w_lam = -(RE / N_FORCING) * np.cos(N_FORCING * Y)
    rng = np.random.default_rng(11)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    w0 = w_lam + 0.1 * np.linalg.norm(w_lam) * d

    n_snap = int(round(args.T / DT_SAVE))
    steps_per_snap = int(round(DT_SAVE / DT))
    ai, aj = amplitude_index(N_GRID)
    n_modes = ai.size

    n_ckpt = (n_snap + CKPT_EVERY - 1) // CKPT_EVERY
    ckpt = np.lib.format.open_memmap(
        CKPT, mode="w+", dtype=np.complex128, shape=(n_ckpt, N_GRID, N_GRID))
    feat = np.lib.format.open_memmap(
        FEAT, mode="w+", dtype=np.float32, shape=(n_snap, n_modes))

    # burn-in, discarded: the run must start ON the attractor, not on the
    # transient escaping the laminar solution's instability.
    t0 = time.time()
    w_burn, _ = solver.integrate(w0, T_BURN)
    burn_wall = time.time() - t0
    w_hat = np.fft.fft2(w_burn) * solver.mask

    diag_t, diag_D = [], []
    t0 = time.time()
    for k in range(n_snap):
        # The checkpoint is written BEFORE the steps that produce snapshot k,
        # so ckpt[k // CKPT_EVERY] is the state from which snapshot k is
        # reached by (k % CKPT_EVERY + 1) * steps_per_snap steps.
        if k % CKPT_EVERY == 0:
            ckpt[k // CKPT_EVERY] = w_hat
        for _ in range(steps_per_snap):
            w_hat = solver._rk4_step(w_hat, DT)
        feat[k] = np.abs(w_hat[ai, aj]).astype(np.float32)
        if k % 400 == 0:
            _, D, _ = solver.diagnostics(np.fft.ifft2(w_hat).real)
            diag_t.append((k + 1) * DT_SAVE)
            diag_D.append(D / solver.D_lam)
        if k % 4000 == 0:
            el = time.time() - t0
            frac = (k + 1) / n_snap
            with open(PROGRESS, "w") as f:
                f.write(f"snapshot {k+1}/{n_snap}  t={(k+1)*DT_SAVE:.1f}  "
                        f"elapsed {el/3600:.2f} h  "
                        f"eta {el/max(frac,1e-9)*(1-frac)/3600:.2f} h\n")
    dns_wall = time.time() - t0
    ckpt.flush()
    feat.flush()

    Dn = np.array(diag_D)
    meta = dict(
        unit="U2", milestone="M2", programme="PROG-R4",
        N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT,
        T_burn=T_BURN, T_recorded=args.T, dt_save=DT_SAVE, n_snapshots=n_snap,
        n_amplitude_modes=int(n_modes),
        burn_wall_seconds=burn_wall, dns_wall_seconds=dns_wall,
        steps=int(n_snap * steps_per_snap),
        seconds_per_step=dns_wall / (n_snap * steps_per_snap),
        attractor_diagnostics=dict(
            note=("D/D_lam sampled every 100 time units; a sustained value "
                  "well below 1 with fluctuation is the signature of the "
                  "chaotic attractor rather than the laminar solution"),
            D_over_Dlam_mean=float(Dn.mean()), D_over_Dlam_std=float(Dn.std()),
            D_over_Dlam_min=float(Dn.min()), D_over_Dlam_max=float(Dn.max()),
            n_samples=int(Dn.size)),
        sourced_thresholds=dict(
            R_thres_record=R_THRES_RECORD, R_thres_window=R_THRES_WINDOW,
            T_window=list(T_WINDOW),
            source=("Chandler & Kerswell 2013 arXiv:1207.4682 (R_thres=0.3 at "
                    "Re=60, T=1e5 per run) and Lucas & Kerswell 2015 "
                    "arXiv:1406.1820 (R<0.25, 0.5<T<60 fed to Newton); "
                    "quoted via writeup/data/p2_route_rpol_v1.json")),
        clay_movement="none -- no L1-L4 link moved by this unit",
    )
    with open(META, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"DNS done: {n_snap} snapshots, {dns_wall/3600:.2f} h, "
          f"{meta['seconds_per_step']*1000:.4f} ms/step")
    print(f"D/D_lam = {Dn.mean():.4f} +- {Dn.std():.4f} "
          f"(range {Dn.min():.4f}-{Dn.max():.4f})")


def regenerate(indices, solver, ckpt, steps_per_snap):
    """Exact reconstruction of the requested snapshots from the checkpoints.

    Not an approximation: each checkpoint is the full complex128 state, and
    re-applying the identical _rk4_step sequence reproduces the original run
    bit for bit. Indices are visited in sorted order and the walk is only
    restarted when the next one lies in a later checkpoint block, so the total
    re-integration is a small fraction of the original DNS rather than one
    restart per snapshot."""
    out = {}
    cur_block = -1
    w_hat = None
    pos = -1
    for idx in sorted(set(int(i) for i in indices)):
        block = idx // CKPT_EVERY
        if block != cur_block or pos > idx:
            w_hat = np.array(ckpt[block])
            cur_block = block
            pos = block * CKPT_EVERY - 1
        while pos < idx:
            for _ in range(steps_per_snap):
                w_hat = solver._rk4_step(w_hat, DT)
            pos += 1
        out[idx] = np.fft.ifft2(w_hat).real
    return out


def full_R(w1, w2, solver):
    """R of C&K eq. (23): minimise the squared relative difference over the
    continuous x-shift AND the discrete y-shift m in 0..n-1. Returns
    (R, s, m). optimal_shift_residual supplies the x minimisation (and already
    returns the SQUARED relative form); the y minimisation is the explicit
    n_forcing-fold loop the paper's second min sign asks for and leg 353 did
    not run."""
    best = (np.inf, 0.0, 0)
    n = solver.n_forcing
    N = solver.N
    for m in range(n):
        rows = int(round(m * N / n))
        w2m = np.roll(w2, rows, axis=0) if rows else w2
        s, rel = optimal_shift_residual(w1, w2m)
        if rel < best[0]:
            best = (float(rel), float(s), int(m))
    return best


def run_recur(args):
    with open(META) as f:
        meta = json.load(f)
    n_snap = meta["n_snapshots"]
    ckpt = np.load(CKPT, mmap_mode="r")
    feat = np.load(FEAT, mmap_mode="r")
    solver = Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)
    steps_per_snap = int(round(DT_SAVE / DT))

    lag_lo = max(1, int(round(T_WINDOW[0] / DT_SAVE)))
    lag_hi = int(round(T_WINDOW[1] / DT_SAVE))

    t0 = time.time()
    # Lossless prefilter (see module docstring): R_red <= R pointwise, so
    # thresholding R_red at R_THRES_RECORD cannot discard a true recurrence.
    # The whole (t, lag) plane is built, because the SELECTION criterion below
    # is a local-minimum test and that needs neighbours in both directions.
    # Honour the DECLARED snapshot count, not the file length: the feature file
    # is preallocated to its final size, so its tail is zeros until the DNS
    # reaches it. Slicing here makes the stage correct on a partial or resumed
    # trajectory instead of silently differencing against zero rows.
    F = np.asarray(feat[:n_snap], dtype=np.float32)
    den = np.maximum(np.einsum("ij,ij->i", F, F), 1e-30)
    n_t = n_snap - lag_hi
    n_lag = lag_hi - lag_lo + 1
    M = np.empty((n_t, n_lag), dtype=np.float32)
    for li, lag in enumerate(range(lag_lo, lag_hi + 1)):
        a = F[lag_hi:]
        b = F[lag_hi - lag:n_snap - lag]
        M[:, li] = np.einsum("ij,ij->i", a - b, a - b) / den[lag_hi:]
    n_pairs = M.size
    n_below = int((M < R_THRES_RECORD).sum())
    prefilter_wall = time.time() - t0

    # SELECTION: strict local minima of R in the (t, T) plane, which is the
    # papers' own criterion, not a threshold invented here.
    #
    # This matters, and a first version of this unit got it wrong. Ranking the
    # sub-threshold cells by R and taking the best fills the entire budget
    # with T = 0.5 pairs: at the short-T edge the trajectory has barely moved,
    # so R is small for trivial reasons and rises monotonically with T. Those
    # cells are BOUNDARY points of the plane, never interior local minima, so
    # requiring an interior strict local minimum in BOTH t and T removes the
    # trivial band automatically -- no hand-set minimum period, and nothing
    # tuned to taste. It also collapses the smear: one genuine near-recurrence
    # occupies many adjacent cells but contributes exactly one minimum.
    C = M[1:-1, 1:-1]
    is_min = C < R_THRES_RECORD
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            is_min &= C < M[1 + di:n_t - 1 + di, 1 + dj:n_lag - 1 + dj]
    ii, jj = np.nonzero(is_min)
    n_local_minima = ii.size
    order = np.argsort(C[ii, jj])

    def cell(o):
        return (float(C[ii[o], jj[o]]),
                int(ii[o] + 1 + lag_hi),
                int(jj[o] + 1 + lag_lo))

    chosen = [cell(o) for o in order[:args.max_candidates]]
    n_global = len(chosen)

    # STRATIFICATION BY NAMED PERIOD. The global ranking above is the right
    # criterion for "what recurs on this attractor", and it is kept whole. It
    # is the WRONG criterion for U3's question, which is not "what recurs" but
    # "does a NAMED Table IV orbit recover", and the two are not the same
    # budget. Measured on the first full-length pass: of the 400 globally best
    # local minima, 260 fell inside L&K's Newton window, 102 of those had
    # m = 0, and exactly ONE anchored to a named row. The rest sit at
    # T = 1.25-2.5, because short-period near-recurrences are far more numerous
    # and score far lower on R than the T ~ 15-19 band where every named orbit
    # lives. A global top-N therefore starves the only band U3 can use, and
    # "100 attempts" is unreachable for a reason that has nothing to do with
    # the flow.
    #
    # So the budget is also spent PER NAMED PERIOD: the best `per_anchor` local
    # minima within T_ANCHOR_TOL of each published period. This ADDS
    # candidates and removes none; the global list is still recorded in full,
    # and every added candidate faces the same full minimisation, the same
    # R < R_THRES_WINDOW window test and the same m = 0 requirement as any
    # other. It changes which seeds are OFFERED to Newton, never what counts as
    # a recovery, so it cannot move G1 toward `yes` -- Newton still has to
    # converge to tol and still has to land on the published (T, s).
    T_of_lag = (np.asarray(jj, dtype=np.float64) + 1 + lag_lo) * DT_SAVE
    picked = {o: None for o in order[:args.max_candidates]}
    per_anchor_counts = {}
    for name, T_pub in TABLE_IV_PERIODS:
        band = np.abs(T_of_lag[order] - T_pub) <= T_ANCHOR_TOL
        take = [o for o, b in zip(order, band) if b][:args.per_anchor]
        per_anchor_counts[name] = len(take)
        for o in take:
            if o not in picked:
                picked[o] = None
                chosen.append(cell(o))
    n_added = len(chosen) - n_global

    t0 = time.time()
    need = [i for _, it, lag in chosen for i in (it, it - lag)]
    snaps = regenerate(need, solver, ckpt, steps_per_snap)
    regen_wall = time.time() - t0

    t0 = time.time()
    cands = []
    for rred, it, lag in chosen:
        w1 = snaps[it]
        w2 = snaps[it - lag]
        # C&K index R(t,T) with the LATER time t and the earlier t-T, so w1 is
        # the later snapshot and the recovered shift is the one carrying the
        # earlier state onto it.
        R, s, m = full_R(w1, w2, solver)
        cands.append(dict(R=R, R_reduced=rred, s=s, m=m,
                          T=lag * DT_SAVE,
                          t_later=(it + 1) * DT_SAVE,
                          snapshot_later=it, snapshot_earlier=it - lag,
                          in_newton_window=bool(R < R_THRES_WINDOW)))
    full_wall = time.time() - t0
    cands.sort(key=lambda c: c["R"])

    window = [c for c in cands if c["in_newton_window"]]
    nonzero_shift = [c for c in window if abs(c["s"]) > 1e-3]

    lib = dict(
        unit="U2", milestone="M2", programme="PROG-R4",
        thresholds=meta["sourced_thresholds"],
        prefilter=dict(
            statement=("R_red <= R pointwise, because |a-b| >= ||a|-|b|| and "
                       "every symmetry in the minimisation multiplies each "
                       "coefficient by a unit-modulus phase; so thresholding "
                       "the proxy at the same value discards nothing"),
            n_pairs_scanned=int(n_pairs),
            n_pairs_below_R_thres_record=n_below,
            n_strict_local_minima_in_the_t_T_plane=int(n_local_minima),
            n_taken_for_full_minimisation=len(chosen),
            stratification=dict(
                why=("a global top-N ranks short-period near-recurrences "
                     "above the T~15-19 band every named Table IV orbit lives "
                     "in; measured on the first full-length pass, the global "
                     "400 yielded exactly ONE anchored, m=0, in-window seed, "
                     "so U3's pre-registered 100 attempts were unreachable "
                     "for a reason that is about the ranking, not the flow"),
                rule=(f"additionally take the best {args.per_anchor} strict "
                      f"local minima within T_ANCHOR_TOL={T_ANCHOR_TOL} of "
                      "each named published period"),
                adds_only=("the global list is kept whole and nothing is "
                           "removed; added candidates face the same full "
                           "minimisation, the same R<R_THRES_WINDOW test and "
                           "the same m=0 requirement, so this changes which "
                           "seeds are OFFERED and never what counts as a "
                           "recovery"),
                n_from_global_ranking=n_global,
                n_added_by_anchor_bands=n_added,
                per_anchor_available=per_anchor_counts),
            selection=("strict interior local minima of R_red in the (t, T) "
                       "plane, the papers' own criterion; ranking by R "
                       "instead fills the budget with T=0.5 cells where the "
                       "trajectory has barely moved, and those are boundary "
                       "points that can never be interior minima"),
            wall_seconds=prefilter_wall),
        full_minimisation=dict(
            n_evaluated=len(cands), wall_seconds=full_wall,
            regeneration_wall_seconds=regen_wall,
            n_snapshots_regenerated=len(snaps),
            note=("minimised over continuous x-shift s AND discrete y-shift m "
                  "in 0..3, per C&K eq. (23); leg 353 minimised over s only")),
        counts=dict(
            n_candidates=len(cands),
            n_in_newton_window=len(window),
            n_in_window_with_nonzero_shift=len(nonzero_shift),
            best_R=cands[0]["R"] if cands else None),
        leg353_comparison=dict(
            note=("leg 353 mined a T=2000 DNS and its best candidates for the "
                  "eight named Table IV rows sat at R = 0.177-0.263, i.e. at "
                  "or outside the edge of L&K's own R<0.25 Newton window"),
            leg353_best_R_for_UPO37=0.1770795743772855),
        candidates=cands,
        clay_movement="none -- no L1-L4 link moved by this unit",
    )
    with open(LIB, "w") as f:
        json.dump(lib, f, indent=2)
    print(f"scanned {n_pairs} pairs in {prefilter_wall:.1f}s; "
          f"{n_below} below R_thres={R_THRES_RECORD}; "
          f"{n_local_minima} strict local minima; {len(chosen)} taken")
    print(f"full minimisation on {len(cands)} in {full_wall:.1f}s; "
          f"best R = {cands[0]['R']:.6f}" if cands else "no candidates")
    print(f"{len(window)} inside L&K's Newton window R<{R_THRES_WINDOW}, "
          f"{len(nonzero_shift)} of those with nonzero shift (the RPO class)")
    print(f"wrote {LIB}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["dns", "recur"], required=True)
    ap.add_argument("--T", type=float, default=T_TOTAL)
    ap.add_argument("--max-candidates", type=int, default=400)
    # Per named Table IV period, on top of the global budget. 80 x 8 rows,
    # against a measured survival of ~65% through the R < 0.25 window and ~39%
    # through m = 0, is sized to clear the 100 attempts U3's compliant scale
    # asks for.
    ap.add_argument("--per-anchor", type=int, default=80)
    args = ap.parse_args()
    (run_dns if args.stage == "dns" else run_recur)(args)


if __name__ == "__main__":
    main()
