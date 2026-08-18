#!/usr/bin/env python3
"""Leg 406, unit `L6-b` -- IS THE STALL THE ANSATZ, OR THE BUDGET?

Pre-registered in `experiments/journal/leg_406.md`.  Gate, final wording, from
`writeup/waves/WAVE7_PLAN.md` AMENDMENT 2 (on `main` before this file existed):

    At FIXED n_dof = 6720, branch B, with the realization, trial space, basis and norm
    UNCHANGED from L6 (as recorded in writeup/data/p2_route_l6_profile_v1.json), run
    three minimisations to an iteration cap of 20,000:
      (i)        from L6's banked J4 minimiser,
      (ii)-(iii) from two fresh independent seeds.
    Answer, WITH NUMBERS: what is the smallest residual reached at 20,000 iterations,
    and is it materially below L6's 1.6138 -- YES or NO?
    Report the residual trajectory against iteration count for each start.

WHAT THIS FILE IS, AND IS NOT.  It is a DRIVER.  Every piece of numerical apparatus --
the geometry, the trial space, the basis, the poloidal-toroidal representation, the
residual field, the load-bearing norm, the objective, its exact gradient, the branch-B
normalisation, the self-tests -- is IMPORTED UNCHANGED from `p2_route_l6_v1.py`, which
this unit MUST NOT and DOES NOT modify.  No new method is built (ORCHESTRATION.md
SS3k rule 3: the exemption is STATED, not assumed).  Nothing here changes n_dof, the
realization, the trial space, the basis or the norm.

CARRIED, NOT REDISCOVERED (leg_401.md SS7.3).  The objective is invariant under
c -> t c because the normalisation is applied INSIDE the tape, so grad J is orthogonal
to c and ||grad J||_inf falls like 1/||c||.  L-BFGS-B stops on ||proj grad||_inf and
therefore FALSELY REPORTS CONVERGENCE while J is still falling.  L6's fix -- renormalise
the iterate onto the normalisation surface (which changes no function value) and restart
the solver with the remaining budget, stopping only when a restart buys less than
REL_STALL relative improvement -- is carried here verbatim, together with L6's
scale-invariant stationarity measure ||x|| ||g|| / |J| (`l6._gscaled`).

THE ONLY DELIBERATE DEVIATIONS FROM `l6._minimise_one`, BOTH NON-NUMERICAL:
  (D1) the trajectory's iteration index is made CUMULATIVE across renormalising
       restarts.  L6's callback counter resets to 0 at each restart; that was latent in
       L6 because all 133 of its starts took exactly one round (restarts == 1 for every
       start in the banked artefact), but this unit runs 25x longer and WILL restart, and
       the gate asks for "the residual trajectory against iteration count".
  (D2) hourly-or-better checkpointing of the trajectory AND the current iterate to a
       TRACKED path, so a kill at hour 6 leaves the partial trajectory in git.
Neither touches the objective, the gradient, the stopping rule or the iterate sequence.

CEILING, DECLARED BEFORE ANY NUMBER EXISTS: TIER 2, float64.  A MEASURED residual at a
larger iteration cap.  Not a bound, not a certificate, not a blow-up, not an infimum.
Scale is not evidence: a bigger budget is not an argument, only the number is.  NO LINK
OF THE L1 -> L4 CHAIN MOVES, whichever way the gate answers.  Clay stays ~0.05%.
BAN C1 stays disengaged and exemplar-free: no Y0/Z0/Z1/Z2, no radii polynomial, no
approximate inverse, no contraction constant, no enclosure, no interval arithmetic --
the apparatus is L6's own L-BFGS-B least-squares minimisation (Byrd, Lu, Nocedal, Zhu,
SIAM J. Sci. Comput. 16(5) (1995) 1190-1208; scipy.optimize.minimize(method="L-BFGS-B")).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
import subprocess
import sys
import time
from pathlib import Path

# Same threading discipline as L6, but 3 worker processes instead of 6, because sibling
# units share this machine: 3 x 2 = 6 cores.  Must be set BEFORE numpy is imported.
_NT = os.environ.setdefault("L6_THREADS", "2")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, _NT)

import numpy as np                                                    # noqa: E402
from scipy.optimize import minimize                                   # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p2_route_l6_v1 as l6                                           # noqa: E402
from p2_route_l6_v1_ad import Var                                     # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
L6_ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"
OUT = ROOT / "writeup" / "data" / "p2_route_l6b_v1.json"
CKPT = ROOT / "experiments" / "route4" / "l6b_ckpt"

L6_SELF_HASH = "6a033004deef39d3"          # the artefact this unit is an answer about
L6_RESIDUAL = 1.613811231995397            # the number the gate compares against
MATERIAL_THRESHOLD = 1.45                  # pre-committed in WAVE7_PLAN.md AMENDMENT 2
BASIN_FLOOR_BAND = (1.55, 1.70)            # "an independent seed reaching ~1.6"

BRANCH = "B"
FRESH_SEEDS = (406, 407)                   # disjoint from L6's SEEDS = [401..405]
CKPT_EVERY = 100                           # iterations between checkpoint writes


# --------------------------------------------------------------------------------------
# 0.  Provenance -- refuse to run if this is not L6's object
# --------------------------------------------------------------------------------------
def load_l6():
    """Read L6's artefact and verify it is the one the gate names.  Never modified."""
    doc = json.loads(L6_ART.read_text())
    body = dict(doc)
    body.pop("self_hash", None)
    recomputed = hashlib.sha256(
        json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    if doc["self_hash"] != L6_SELF_HASH:
        raise SystemExit(f"L6 artefact self_hash is {doc['self_hash']}, "
                         f"gate names {L6_SELF_HASH} -- refusing to run")
    return doc, recomputed


def geometry_from_l6(doc):
    """Build EXACTLY L6's J4 geometry from L6's own banked record.  No parameter of the
    realization, trial space, basis or norm is chosen here."""
    bp = doc["banked_profile"]["B"]
    g = l6.Geom(bp["Lmax"], bp["Nr"], bp["Ks"], bp["Lmap"])
    if int(g.n_dof) != 6720 or int(bp["n_dof"]) != 6720:
        raise SystemExit(f"n_dof is {g.n_dof}, gate fixes 6720 -- refusing to run")
    x = np.array(bp["coefficients"], float)
    if x.size != g.n_dof:
        raise SystemExit("banked coefficient vector does not match the geometry")
    return g, x, bp


# --------------------------------------------------------------------------------------
# 1.  Self-tests: L6's own, plus the same two checks AT THIS UNIT'S STARTING POINT
# --------------------------------------------------------------------------------------
def selftests_at_start(g, x):
    """T_A (div V = 0) and T_D (W vs finite-difference curl R) evaluated on the BANKED
    J4 MINIMISER at n_dof = 6720 -- i.e. at this unit's starting point, not on L6's fixed
    small random field.  If these do not reproduce, we are not on L6's object."""
    aF, aQ = g.unpack(l6.normalise(g, np.asarray(x, float), BRANCH))

    # --- T_A: divergence-free, by finite differences on the synthesised field
    pts = np.array([[0.7, -0.4, 1.1], [1.9, 2.2, -0.8], [-3.1, 0.6, 2.4], [0.2, -5.0, 1.3]])
    h = 1e-5
    div = []
    for p in pts:
        d = 0.0
        for j in range(3):
            e = np.zeros(3)
            e[j] = h
            d += (l6.eval_V_cart(g, aF, aQ, (p + e)[None, :], 0.3)[0, j]
                  - l6.eval_V_cart(g, aF, aQ, (p - e)[None, :], 0.3)[0, j]) / (2 * h)
        div.append(abs(d))
    scale = float(np.max(np.abs(l6.eval_V_cart(g, aF, aQ, pts, 0.3))))
    t_a = float(max(div) / scale)

    # --- T_D: W[V] from the exact-basis route vs a fully finite-difference curl R[V]
    def Rnp(p, s):
        hh = 1e-4 * max(1.0, float(np.linalg.norm(p)))
        V0 = l6.eval_V_cart(g, aF, aQ, p[None, :], s)[0]
        Vs = (l6.eval_V_cart(g, aF, aQ, p[None, :], s + 1e-5)[0]
              - l6.eval_V_cart(g, aF, aQ, p[None, :], s - 1e-5)[0]) / 2e-5
        Jm = np.zeros((3, 3))
        lap = np.zeros(3)
        for j in range(3):
            e = np.zeros(3)
            e[j] = hh
            vp = l6.eval_V_cart(g, aF, aQ, (p + e)[None, :], s)[0]
            vm = l6.eval_V_cart(g, aF, aQ, (p - e)[None, :], s)[0]
            Jm[:, j] = (vp - vm) / (2 * hh)
            lap += (vp - 2 * V0 + vm) / hh ** 2
        return Vs + l6.A_SIM * (V0 + Jm @ p) - lap + Jm @ V0

    Wf, _, _ = l6.residual_field(g, Var(aF), Var(aQ))
    Wg = Wf.v
    errs = []
    for (ii, pp) in [(4, 7), (10, 3), (14, 9)]:
        p = g.r[ii] * g.er[pp]
        sval = g.s[1]
        hh = 3e-4 * max(1.0, float(np.linalg.norm(p)))
        Jm = np.zeros((3, 3))
        for j in range(3):
            e = np.zeros(3)
            e[j] = hh
            Jm[:, j] = (Rnp(p + e, sval) - Rnp(p - e, sval)) / (2 * hh)
        curlR = np.array([Jm[2, 1] - Jm[1, 2], Jm[0, 2] - Jm[2, 0], Jm[1, 0] - Jm[0, 1]])
        ref = Wg[ii, 1, pp]
        errs.append(float(np.max(np.abs(curlR - ref)) / max(1e-9, np.max(np.abs(ref)))))
    t_d = float(max(errs))
    return dict(T_A_div_V_max_abs_over_scale=t_a,
                T_D_W_vs_fd_curlR_max_rel_err=t_d)


# --------------------------------------------------------------------------------------
# 2.  One start: L6's `_minimise_one`, with a cumulative trajectory index and checkpoints
# --------------------------------------------------------------------------------------
def _atomic_write(path: Path, obj):
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(obj, default=float))
    tmp.replace(path)


def l6b_minimise_one(task):
    """One start to `maxiter` iterations.  Numerically identical to `l6._minimise_one`:
    same objective (`l6.objective`), same exact gradient, same normalisation
    (`l6.normalise`), same L-BFGS-B options (ftol=1e-16, gtol=1e-12, maxfun = 2 x
    remaining), same SS7.3 renormalising-restart fix, same REL_STALL, same TRAJ_EVERY
    sampling schedule.  Deviations D1 (cumulative iteration index) and D2 (checkpoints)
    only, both non-numerical.  Top level so it is picklable."""
    Lmax, Nr, Ks, Lmap, branch, name, x0, maxiter, ckpt_dir = task
    g = l6.Geom(Lmax, Nr, Ks, Lmap)
    ts = time.time()
    ck = Path(ckpt_dir) / f"{name}.json"

    traj = []
    state = dict(k=0, base=0)          # D1: `base` carries iterations of earlier rounds

    def _flush(status):
        _atomic_write(ck, dict(
            unit="L6-b", leg=406, start=name, branch=branch, n_dof=int(g.n_dof),
            maxiter=int(maxiter), status=status,
            iterations_done=int(state["base"] + state["k"]),
            seconds=round(time.time() - ts, 1),
            best_J_so_far=(min(t[2] for t in traj) if traj else None),
            trajectory_k_sec_J_ginf_gscaled=traj,
            current_iterate=[float(v) for v in np.asarray(state.get("x", x0), float)],
        ))

    def cb(xk):
        state["k"] += 1
        k = state["k"]
        kk = state["base"] + k
        if k in (1, 2, 5, 10) or k % l6.TRAJ_EVERY == 0:
            f, gr = l6.objective(g, xk, branch)
            traj.append([kk, round(time.time() - ts, 2), f,
                         float(np.max(np.abs(gr))), l6._gscaled(xk, gr, f)])
        if kk % CKPT_EVERY == 0:
            state["x"] = np.asarray(xk, float).copy()
            _flush("RUNNING")

    x = np.asarray(x0, float)
    state["x"] = x.copy()
    _flush("START")
    total_nit = total_nfev = 0
    prev = float("inf")
    rounds, r = [], None
    while total_nit < maxiter:
        x = l6.normalise(g, x, branch)
        state["k"] = 0
        state["base"] = total_nit
        r = minimize(lambda z: l6.objective(g, z, branch), x, jac=True,
                     method="L-BFGS-B", callback=cb,
                     options=dict(maxiter=maxiter - total_nit,
                                  maxfun=2 * (maxiter - total_nit),
                                  ftol=1e-16, gtol=1e-12))
        total_nit += int(r.nit)
        total_nfev += int(r.nfev)
        rounds.append(dict(nit=int(r.nit), fun=float(r.fun), status=int(r.status),
                           message=str(r.message),
                           coeff_norm=float(np.linalg.norm(r.x))))
        x = np.asarray(r.x, float)
        state["x"] = x.copy()
        state["base"] = total_nit
        state["k"] = 0
        _flush("ROUND_END")
        gain = (prev - float(r.fun)) / abs(prev) if np.isfinite(prev) else 1.0
        prev = float(r.fun)
        if int(r.nit) == 0 or gain < l6.REL_STALL:
            break

    x = l6.normalise(g, x, branch)
    fun, jac = l6.objective(g, x, branch)
    gn = float(np.max(np.abs(jac)))
    gs = l6._gscaled(x, jac, fun)
    traj.append([int(total_nit), round(time.time() - ts, 2), float(fun), gn, gs])
    state["x"] = x.copy()
    state["base"], state["k"] = int(total_nit), 0
    _flush("DONE")
    rec = dict(start=name, fun=float(fun), nit=int(total_nit), nfev=int(total_nfev),
               restarts=len(rounds), rounds=rounds,
               max_abs_grad=gn, scale_invariant_grad=gs,
               coeff_norm=float(np.linalg.norm(x)),
               status=int(r.status) if r is not None else -1,
               hit_maxiter=bool(total_nit >= maxiter),
               stalled_before_cap=bool(total_nit < maxiter),
               trajectory_k_sec_J_ginf_gscaled=traj,
               seconds=round(time.time() - ts, 2))
    return rec, x.copy()


# --------------------------------------------------------------------------------------
# 3.  Checkpoint commits during the run (STANDING CLAUSE: not only at the gate)
# --------------------------------------------------------------------------------------
PATHS = ["experiments/route4/l6b_ckpt",
         "experiments/p2_route_l6b_v1.py",
         "experiments/p2_route_l6b_v1_evidence.py",
         "experiments/journal/leg_406.md",
         "writeup/data/p2_route_l6b_v1.json"]


def git_checkpoint(msg):
    """Commit the checkpoint files with EXPLICIT PATHS ONLY.  Never `git add -A`, never
    `git add .`, never `git commit -a`.  Three sibling units share this working tree, so
    the commit is ALSO path-limited (`git commit -- <paths>`), which makes it impossible
    for anything a sibling happened to stage to be swept in.  On index.lock, wait and
    retry."""
    have = [p for p in PATHS if (ROOT / p).exists()]
    for attempt in range(30):
        try:
            subprocess.run(["git", "add", "--"] + have, cwd=ROOT, check=True,
                           capture_output=True, timeout=120)
            r = subprocess.run(["git", "commit", "-m", msg, "--"] + have, cwd=ROOT,
                               capture_output=True, text=True, timeout=180)
            if r.returncode == 0 or "nothing to commit" in (r.stdout + r.stderr):
                print(f"[ckpt] {msg}: rc={r.returncode}", flush=True)
                return True
            if "index.lock" in (r.stdout + r.stderr):
                time.sleep(20)
                continue
            print(f"[ckpt] commit failed: {r.stdout}\n{r.stderr}", flush=True)
            return False
        except subprocess.CalledProcessError as exc:                  # noqa: PERF203
            if b"index.lock" in (exc.stderr or b""):
                time.sleep(20)
                continue
            print(f"[ckpt] add failed: {exc.stderr!r}", flush=True)
            return False
        except subprocess.TimeoutExpired:
            time.sleep(20)
    return False


# --------------------------------------------------------------------------------------
# 4.  Driver
# --------------------------------------------------------------------------------------
def trajectory_digest(traj, every=500):
    """A compact (iteration, J) view for the artefact and the journal."""
    out = []
    for k, _sec, f, _gi, _gs in traj:
        if k <= 10 or k % every == 0:
            out.append([int(k), float(f)])
    if traj and out and out[-1][0] != int(traj[-1][0]):
        out.append([int(traj[-1][0]), float(traj[-1][2])])
    return out


def best_at_cap(traj, K):
    pts = [t for t in traj if t[0] <= K]
    return min((t[2] for t in pts), default=None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxiter", type=int, default=20000)
    ap.add_argument("--nproc", type=int, default=3)
    ap.add_argument("--commit-every", type=float, default=3000.0,
                    help="seconds between tracked checkpoint commits")
    ap.add_argument("--selftests-only", action="store_true")
    ap.add_argument("--no-commit", action="store_true")
    args = ap.parse_args()

    t_start = time.time()
    CKPT.mkdir(parents=True, exist_ok=True)

    doc6, recomputed = load_l6()
    g, x_banked, bp = geometry_from_l6(doc6)
    print(f"L6 artefact self_hash={doc6['self_hash']} (recomputed {recomputed})", flush=True)
    print(f"geometry: Lmax={g.Lmax} Nr={g.Nr} Ks={g.Ks} Lmap={g.Lmap} n_dof={g.n_dof} "
          f"nq_r={g.nq_r} n_theta={g.nth} n_phi={g.nph} n_s={g.ns}", flush=True)

    # --- the starting point must reproduce L6's banked number, or this is not L6's object
    J0_banked, _ = l6.objective(g, x_banked, BRANCH)
    print(f"J(banked J4 minimiser) = {J0_banked!r}  banked = {L6_RESIDUAL!r}  "
          f"delta = {J0_banked - L6_RESIDUAL:.3e}", flush=True)

    # --- self-tests: L6's own suite, and T_A/T_D at THIS unit's starting point
    print("L6 self-tests (its own fixed field):", flush=True)
    st_l6 = l6.selftests(verbose=True)
    print("T_A / T_D at the starting point (n_dof = 6720):", flush=True)
    st_start = selftests_at_start(g, x_banked)
    for k, v in st_start.items():
        print(f"  {k:42s} {v:.3e}", flush=True)

    selftests = dict(
        L6_suite_reproduced=st_l6,
        L6_suite_banked={k: doc6["selftests"][k] for k in doc6["selftests"]},
        at_this_units_starting_point=st_start,
        starting_point_J=float(J0_banked),
        starting_point_J_matches_L6_banked=bool(
            abs(J0_banked - L6_RESIDUAL) <= 1e-12 * abs(L6_RESIDUAL)),
        note=("T_A and T_D are reported twice: reproduced on L6's own fixed self-test "
              "field (so they are comparable digit-for-digit with the banked numbers), "
              "and re-evaluated on the banked J4 minimiser at n_dof = 6720, which is "
              "this unit's actual starting point (i)."),
    )
    ok_TA = st_l6["T_A_div_V_max_abs_over_scale"] < 1e-6
    ok_TD = st_l6["T_D_W_vs_fd_curlR_max_rel_err"] < 2e-3
    ok_TAs = st_start["T_A_div_V_max_abs_over_scale"] < 1e-6
    ok_TDs = st_start["T_D_W_vs_fd_curlR_max_rel_err"] < 2e-3
    selftests["all_pass"] = bool(ok_TA and ok_TD and ok_TAs and ok_TDs
                                 and selftests["starting_point_J_matches_L6_banked"])
    if not selftests["all_pass"]:
        _atomic_write(CKPT / "_selftests_FAILED.json", selftests)
        raise SystemExit("SELFTESTS DID NOT REPRODUCE AT THE STARTING POINT -- STOP. "
                         "This unit is not on L6's object.")
    _atomic_write(CKPT / "_selftests.json", selftests)
    if not args.no_commit:
        git_checkpoint("L6-b leg 406: selftests reproduce at the starting point; run begins")
    if args.selftests_only:
        return 0

    # --- the three starts ---------------------------------------------------------------
    starts = [("banked_J4_minimiser", l6.normalise(g, x_banked.copy(), BRANCH))]
    for sd in FRESH_SEEDS:
        rng = np.random.default_rng(sd)
        starts.append((f"seed{sd}", l6.normalise(g, rng.standard_normal(g.n_dof) * 0.1,
                                                 BRANCH)))
    tasks = [(g.Lmax, g.Nr, g.Ks, g.Lmap, BRANCH, nm, x0, args.maxiter, str(CKPT))
             for nm, x0 in starts]

    ctx = mp.get_context("fork")
    with ctx.Pool(min(args.nproc, len(tasks))) as pool:
        async_res = pool.map_async(l6b_minimise_one, tasks, chunksize=1)
        last = time.time()
        while not async_res.ready():
            async_res.wait(60)
            if not args.no_commit and time.time() - last >= args.commit_every:
                h = (time.time() - t_start) / 3600.0
                git_checkpoint(f"L6-b leg 406: in-run checkpoint at {h:.2f} h "
                               f"(trajectories + current iterates, TRACKED)")
                last = time.time()
        results = async_res.get()

    if not args.no_commit:
        git_checkpoint("L6-b leg 406: all three starts finished; final trajectories")

    # --- the gate answer ----------------------------------------------------------------
    per_start = {}
    for rec, xopt in results:
        traj = rec["trajectory_k_sec_J_ginf_gscaled"]
        per_start[rec["start"]] = dict(
            smallest_residual_at_20000=float(min(t[2] for t in traj) if traj else rec["fun"]),
            final_residual=rec["fun"],
            iterations=rec["nit"], nfev=rec["nfev"], restarts=rec["restarts"],
            rounds=rec["rounds"],
            hit_maxiter=rec["hit_maxiter"], stalled_before_cap=rec["stalled_before_cap"],
            status=rec["status"],
            max_abs_grad=rec["max_abs_grad"],
            scale_invariant_grad=rec["scale_invariant_grad"],
            coeff_norm=rec["coeff_norm"], seconds=rec["seconds"],
            residual_at_iteration_cap={str(K): best_at_cap(traj, K)
                                       for K in (50, 100, 200, 400, 800, 1600, 3200,
                                                 6400, 12800, 20000)},
            trajectory_digest_k_J=trajectory_digest(traj),
            trajectory_k_sec_J_ginf_gscaled=traj,
        )
        _atomic_write(CKPT / f"{rec['start']}_final_iterate.json",
                      dict(start=rec["start"], n_dof=int(g.n_dof),
                           residual=rec["fun"],
                           coefficients=[float(v) for v in xopt]))

    smallest = min(v["smallest_residual_at_20000"] for v in per_start.values())
    seed_bests = {k: v["smallest_residual_at_20000"] for k, v in per_start.items()
                  if k.startswith("seed")}
    any_seed_at_basin = {k: bool(BASIN_FLOOR_BAND[0] <= v <= BASIN_FLOOR_BAND[1])
                         for k, v in seed_bests.items()}

    # --- diagnostics on the best iterate, using L6's own diagnostic code -----------------
    best_name = min(per_start, key=lambda k: per_start[k]["smallest_residual_at_20000"])
    best_x = dict((rec["start"], xo) for rec, xo in results)[best_name]
    diag = l6.diagnostics(g, best_x, BRANCH)

    doc = dict(
        unit="L6-b", leg=406, lane="L", wave=7, route="route 4",
        what=("Is L6's stall the ANSATZ or the OPTIMISER BUDGET?  Three minimisations at "
              "FIXED n_dof = 6720, branch B, L6's realization/trial space/basis/norm "
              "unchanged, iteration cap 20,000: (i) from L6's banked J4 minimiser, "
              "(ii)-(iii) from two fresh independent seeds."),
        gate_source="writeup/waves/WAVE7_PLAN.md AMENDMENT 2 (on main before dispatch)",
        answers_about=dict(artefact="writeup/data/p2_route_l6_profile_v1.json",
                           self_hash=L6_SELF_HASH,
                           self_hash_recomputed_here=recomputed,
                           L6_residual=L6_RESIDUAL,
                           L6_decreases_under_refinement="NO"),
        realization_lesson_91=dict(
            unchanged_from_L6=True,
            n_dof=int(g.n_dof), Lmax=g.Lmax, Nr=g.Nr, Ks=g.Ks, Lmap=g.Lmap,
            nq_r=int(g.nq_r), n_theta=int(g.nth), n_phi=int(g.nph), n_s=int(g.ns),
            branch=BRANCH,
            object=doc6["realization_lesson_91"]["object"],
            trial_space=doc6["realization_lesson_91"]["trial_space"],
            basis=doc6["realization_lesson_91"]["basis"],
            norm_LOAD_BEARING=doc6["realization_lesson_91"]["norms"]["LOAD_BEARING"],
            normalisation_branch_B=doc6["realization_lesson_91"]["normalisations"]["branch_B"],
        ),
        optimiser=dict(method="L-BFGS-B", ftol=1e-16, gtol=1e-12,
                       maxiter=args.maxiter,
                       renormalising_restarts="leg_401.md SS7.3, carried verbatim",
                       REL_STALL=l6.REL_STALL, TRAJ_EVERY=l6.TRAJ_EVERY,
                       fresh_seeds=list(FRESH_SEEDS),
                       L6_seeds=list(l6.SEEDS),
                       apparatus_imported_unchanged_from="experiments/p2_route_l6_v1.py"),
        selftests=selftests,
        gate=dict(
            question=("smallest residual reached at 20,000 iterations, and is it "
                      "materially below L6's 1.6138 -- YES or NO"),
            per_start={k: v["smallest_residual_at_20000"] for k, v in per_start.items()},
            smallest_residual_at_20000=smallest,
            L6_residual_at_800=L6_RESIDUAL,
            absolute_change=smallest - L6_RESIDUAL,
            relative_change=(smallest - L6_RESIDUAL) / L6_RESIDUAL,
            material_threshold=MATERIAL_THRESHOLD,
            materially_below_1_6138="YES" if smallest < MATERIAL_THRESHOLD else "NO",
            independent_seed_best=seed_bests,
            independent_seed_reached_basin_floor=any_seed_at_basin,
            basin_floor_band=list(BASIN_FLOOR_BAND),
            reading_that_fires=(
                "L6's ladder was measuring the OPTIMISER BUDGET, not the ansatz"
                if smallest < MATERIAL_THRESHOLD else
                "no material drop: the stall is the CONSTRUCTION, not the budget, and "
                "route 4's NO hardens"),
        ),
        starts=per_start,
        diagnostics_at_best_iterate=dict(start=best_name, **diag),
        false_convergence_check=dict(
            defect="leg_401.md SS7.3 -- scale-invariant objective, L-BFGS-B stops on "
                   "||proj grad||_inf, which falls like 1/||c||",
            fix_carried="renormalising restarts; stop only when a restart buys < REL_STALL",
            per_start_restarts={k: v["restarts"] for k, v in per_start.items()},
            per_start_hit_maxiter={k: v["hit_maxiter"] for k, v in per_start.items()},
            per_start_scale_invariant_grad={k: v["scale_invariant_grad"]
                                            for k, v in per_start.items()},
            how_a_pre_cap_stop_is_proved_not_the_defect=(
                "a start that stops before the cap has already been renormalised and "
                "restarted; the LAST restart bought < REL_STALL = 1e-10 relative "
                "improvement, at a scale-invariant stationarity measure "
                "||x|| ||grad|| / |J| reported per start.  The per-round record "
                "(starts.<name>.rounds) carries nit, fun, status and message for every "
                "round, so a spurious PGTOL stop is visible as a round with a large "
                "subsequent gain -- there is none if the run stalled genuinely."),
        ),
        chain=dict(L1_to_L4_link_moved="NONE", clay_percent_unchanged=True,
                   this_is_not_a_blowup=True, this_is_not_a_certificate=True,
                   this_is_not_an_infimum=True),
        ceiling=("TIER 2, float64.  A MEASURED residual at a 25x larger iteration cap at "
                 "ONE resolution.  Not a bound, not a certificate, not a blow-up, not an "
                 "infimum, and not a statement about any n_dof other than 6720.  Scale is "
                 "not evidence.  No L1->L4 link moves either way."),
    )
    doc["cost_and_shortfall"] = dict(
        preregistered_maxiter=20000,
        maxiter_actually_used=args.maxiter,
        starts_run=len(results),
        starts_that_hit_the_iteration_cap=sum(1 for v in per_start.values()
                                              if v["hit_maxiter"]),
        starts_that_stalled_before_the_cap=sum(1 for v in per_start.values()
                                               if v["stalled_before_cap"]),
        wall_clock_seconds=round(time.time() - t_start, 1),
        wall_clock_hours=round((time.time() - t_start) / 3600.0, 3),
        processes=min(args.nproc, len(tasks)),
        threads_per_process=int(_NT),
        cores_used=min(args.nproc, len(tasks)) * int(_NT),
        core_hours=round((time.time() - t_start) / 3600.0
                         * min(args.nproc, len(tasks)) * int(_NT), 3),
        L6_price_per_start_800_iterations_seconds=1240.0,
        UNDER_RESOURCED=False,
        under_resourced_note=("the gate's own budget -- 20,000 iterations at fixed "
                              "n_dof = 6720 -- was run in full and not truncated.  What "
                              "is NOT resourced here is a resolution ladder at this cap; "
                              "that is priced in the journal, not attempted."),
    )
    doc.pop("self_hash", None)
    doc["self_hash"] = hashlib.sha256(
        json.dumps(doc, sort_keys=True).encode()).hexdigest()[:16]
    OUT.write_text(json.dumps(doc, indent=1, sort_keys=True))
    print(f"\nwrote {OUT}  self_hash={doc['self_hash']}", flush=True)
    print(f"GATE: smallest residual at 20,000 = {smallest!r}   "
          f"materially below 1.6138 (< {MATERIAL_THRESHOLD}) = "
          f"{doc['gate']['materially_below_1_6138']}", flush=True)
    for k, v in doc["gate"]["per_start"].items():
        print(f"   {k:24s} {v!r}", flush=True)
    if not args.no_commit:
        git_checkpoint("L6-b leg 406: gate answered; artefact written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
