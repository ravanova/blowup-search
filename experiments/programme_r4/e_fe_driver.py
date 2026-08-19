"""PROG-R4, wave 7 unit E-FE -- THE FIELD ENSEMBLE. Lane R, leg 408.

  ####################################################################
  ##  THIS FILE IS COMMITTED BEFORE THE FIRST ATTEMPT IS RUN.       ##
  ##  The gate, the three counts, the confidence-interval method    ##
  ##  and its TAIL CONVENTION, the planted controls and BOTH        ##
  ##  pre-committed readings are fixed here so that no reading can  ##
  ##  be chosen after a count exists. The commit order is the       ##
  ##  evidence.                                                     ##
  ####################################################################

THE GATE, verbatim from `writeup/waves/WAVE7_PLAN.md` SS B (the BINDING
wording; where the dispatch brief and SS B differ, SS B wins and the artefact
says so):

    Run 160 attempts -- the same 8 rows and 2 arms E used, with 10 independent
    fields per (row, arm) drawn by E's own recorded selection rule from the
    banked artefact of A. Report, with the numbers: how many of the 160
    converge, and how many recover a named row -- and, per (row, arm), the
    recovery rate out of 10 with its exact binomial confidence interval.
    Answer explicitly: does any row recover in ANY of its 10 draws, YES or NO?

PRE-COMMITTED READING, BOTH DIRECTIONS, quoted verbatim from SS B and fixed
before the first attempt returns:

  - "0 of 160 ==> the null is no longer about draws. With 10 draws per arm, a
    per-draw recovery probability above 26% is excluded at 95% for every row.
    That is a statement about the rows in this realization, and it is the
    strongest negative this programme can buy for ~11 h wall. It is not a
    statement about the rows in the published realization -- E-iv's
    realization gap and the N = 24 resolution limit both survive it, and must
    be restated in the artefact."
  - ">= 1 recovery ==> E's null was a draw artefact, M1's comparison changes,
    and Lane R's ranking is re-opened in that integration commit."

THE 26% IS RE-DERIVED HERE, NOT QUOTED, AND THE TAIL CONVENTION IS NAMED.
The interval reported is CLOPPER-PEARSON (Clopper & Pearson 1934, Biometrika
26(4):404-413) -- the exact binomial interval obtained by inverting the
binomial test, computed as Beta quantiles: for k successes in n trials the
two-sided 1-alpha interval is [Beta^-1(alpha/2; k, n-k+1),
Beta^-1(1-alpha/2; k+1, n-k)], with the lower limit 0 at k = 0 and the upper
limit 1 at k = n. Both conventions are computed and BOTH are reported,
because they are different numbers and the plan's own text uses one while its
own instruction ("its exact binomial confidence interval") conventionally
means the other:

    k = 0, n = 10, ONE-SIDED 95% upper bound : 1 - 0.05^(1/10)  = 0.258866
    k = 0, n = 10, TWO-SIDED 95% CP upper    : 1 - 0.025^(1/10) = 0.308497

SS B's "above 26% is excluded at 95%" is the ONE-SIDED number and is correct
under that convention. Under the two-sided exact binomial interval the gate
asks for, the excluded region begins at 30.85%, not 26%. This is recorded as
a defect of ambiguity in SS B, not smoothed over.

WHAT THIS UNIT IS NOT. Not a grinder. 160 attempts at FIXED rows and FIXED
arms, varying ONLY the draw. No new seed supply -- every field comes from the
already-banked seedbank of unit R-bank. No GA and no learned or evolved seed
scoring (leg 349: 0 of 6 properties). No Newton parameter is touched, no
tolerance is adjusted, no row is added and no arm is added. SCALE IS NOT
EVIDENCE: 160 attempts is not 10x more evidence than E's 16, it is 10x more
DRAWS from one realization.

WHAT IS REUSED, NOT REIMPLEMENTED. E's solver, Newton loop, convergence test,
stall rule, matching predicate and per-attempt record are called through
`e_hhard_diagnostic.run_attempt` and `e_hhard_diagnostic.seed_residual`,
imported, never copied. The seed comes through
`r_bank_build.load_seed(row, arm, field_index)`, which re-checks the SHA-256
of the field against R-bank's manifest on every load. The meta dict handed to
`run_attempt` is built exactly as `r_bank_build.demo_attempt` builds it --
that function is this unit's worked example of one attempt end to end and its
call graph is the one followed here.

ONE DELIBERATE MONKEYPATCH, DECLARED. `e_hhard_diagnostic.PARTIAL` points at
`experiments/programme_r4/e_hhard_partial`, which is E's territory and whose
attempt-index keying would collide with E's own 0..15. It is redirected to
`e_fe_partials/pkl` before any attempt runs. This changes NO algorithm, NO
seed, NO tolerance and NO cap -- only where a checkpoint file is written.

PARTIALS ARE TRACKED, NOT GITIGNORED. E's checkpoints were gitignored and died
with a container TWICE. Every finished attempt is written as JSON under
`e_fe_partials/json/` and committed during the run, not only at the gate. A
mid-run commit says in its message that it is NOT a landing and NOT a verdict.

PLANTED CONTROLS, fixed here:
  C-REPRO (16 of them, expected to FIRE, and free): field_index 0 of each
    (row, arm) IS E's original seed. Those 16 attempts are exact re-runs of
    E's 16 and MUST reproduce E's banked record bit for bit. If any does not,
    the run ABORTS and reports -- that is a bigger finding than the gate.
  C-PRED (free, expected to FIRE): E's own `match_named` fed each row's
    published (T, s) with success=True must return that row, and fed a
    nonsense (T, s) must return None. Guards a null produced by a predicate
    that can never say yes.
  C-P, C-N, C-R: u3_controls' positive / negative / conditional-positive,
    imported UNCHANGED, exactly as E ran them, plus E's
    `harness_predicate_says_recovered` check on C-R.

SS3k RULE 3. This unit implements NO published solver, stepper or continuation
method: it re-executes this repository's own committed code. The ONE published
method it uses is the Clopper-Pearson exact binomial interval, cited above and
evaluated through `scipy.stats.beta`, not hand-rolled. `writeup/SOURCES.md` is
OUTSIDE this unit's briefed territory, so the row that rule 1 would require is
recorded as an OWED row in the artefact's `sources_3k` block and flagged as a
defect of the territory grant rather than written.

Usage:
    .venv/bin/python experiments/programme_r4/e_fe_driver.py --run --shards 6
    .venv/bin/python experiments/programme_r4/e_fe_driver.py --gate
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
from collections import Counter

import numpy as np
from scipy.stats import beta as _beta

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

import multiprocessing as mp  # noqa: E402

from solver.kolmogorov2d_nkbasin import Kolmogorov2D  # noqa: E402
from experiments.programme_r4 import e_hhard_diagnostic as E  # noqa: E402
from experiments.programme_r4 import r_bank_build as B  # noqa: E402
from experiments.programme_r4 import u3_controls  # noqa: E402
from experiments.programme_r4.u2_m2_dns_recurrence import (  # noqa: E402
    DT, N_FORCING, N_GRID, RE,
)
from experiments.programme_r4.u5_stratified_attempts import (  # noqa: E402
    GMRES_RTOL, MAX_GMRES, MAX_NEWTON, TOL, wrap_abs,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

PARTIALS = os.path.join(HERE, "e_fe_partials")
PKL_DIR = os.path.join(PARTIALS, "pkl")
JSON_DIR = os.path.join(PARTIALS, "json")
CTRL_DIR = os.path.join(PARTIALS, "controls")
RUNLOG = os.path.join(PARTIALS, "run_meta.json")
ABORT = os.path.join(PARTIALS, "CONTROL_FAILURE.json")
ORBITS = os.path.join(HERE, "e_fe_converged_orbits.npz")
OUT = os.path.join(ROOT, "writeup", "data", "p2_e_fe_v1.json")

E_CURATED = os.path.join(ROOT, "writeup", "data", "p2_prog_r4_e_v1.json")
E_LEDGER = os.path.join(HERE, "e_hhard_ledger.json")

N_TOTAL = 160
N_PER_ARM = 10
ALPHA = 0.05

# The 16 scalar fields r_bank_build.demo_attempt compares. Reused, not
# re-chosen: wall_seconds is excluded because it is a clock, not a result.
REPRO_FIELDS = ["reason", "success", "final_residual", "n_iters",
                "T_converged", "s_converged", "abs_s_converged",
                "matched_row", "recovered_named_orbit",
                "recovered_any_named_orbit", "krylov_dims", "radius_trials",
                "residual_history", "seed_residual_plus",
                "seed_residual_minus", "s_seeded"]

# REDIRECT E's checkpoint directory. Declared in the docstring above.
E.PARTIAL = PKL_DIR


def _canon(x):
    return json.dumps(x, sort_keys=True)


def _same(a, b):
    return _canon(a) == _canon(b)


def _solver():
    return Kolmogorov2D(N=N_GRID, Re=RE, n_forcing=N_FORCING, dt=DT)


# ==========================================================================
# CLOPPER-PEARSON -- both tail conventions, computed, never quoted
# ==========================================================================

def clopper_pearson(k, n, alpha=ALPHA):
    """Exact binomial interval by inversion of the binomial test.

    Returns both the two-sided (1-alpha) interval and the one-sided (1-alpha)
    upper bound, because SS B's 26% figure is the ONE-SIDED number while
    'its exact binomial confidence interval' conventionally means the
    two-sided one. Naming the convention is part of the gate."""
    lo2 = 0.0 if k == 0 else float(_beta.ppf(alpha / 2.0, k, n - k + 1))
    hi2 = 1.0 if k == n else float(_beta.ppf(1.0 - alpha / 2.0, k + 1, n - k))
    hi1 = 1.0 if k == n else float(_beta.ppf(1.0 - alpha, k + 1, n - k))
    lo1 = 0.0 if k == 0 else float(_beta.ppf(alpha, k, n - k + 1))
    return dict(
        k=int(k), n=int(n), point_estimate=k / n if n else None,
        method="Clopper-Pearson exact binomial (Beta-quantile inversion)",
        two_sided_95_lower=lo2, two_sided_95_upper=hi2,
        one_sided_95_upper=hi1, one_sided_95_lower=lo1,
        closed_form_check_upper_at_k0=(
            None if k else 1.0 - (alpha / 2.0) ** (1.0 / n)))


# ==========================================================================
# JOBS
# ==========================================================================

def _meta_for(entry):
    """Exactly r_bank_build.demo_attempt's meta, for any field_index."""
    aps = entry["abs_s_published"]
    return dict(
        row=entry["row"], arm=entry["arm"],
        T_published=entry["T_published"], s_published=entry["s_published"],
        m_published=entry["m_published"], abs_s_published=aps,
        snapshot_earlier=entry["snapshot_index"],
        selection_rule=entry["selection_rule"], R_seed=entry["R_seed"],
        T_candidate=entry["T_candidate"],
        abs_s_candidate=entry["abs_s_candidate"],
        delta_abs_s_candidate_to_published=entry[
            "delta_abs_s_candidate_to_published"],
        delta_T_candidate_to_published=entry[
            "delta_T_candidate_to_published"],
        candidate_in_newton_window=entry["candidate_in_newton_window"],
        n_anchored_m0=entry["n_anchored_m0"],
        n_shift_matched_available=entry["n_shift_matched_available"],
        field_index=entry["field_index"],
        is_E_original=entry["is_E_original"],
        e_attempt_index=entry["e_attempt_index"],
        global_index=entry["global_index"],
        sha256=entry["sha256"],
        T_seeded=entry["T_published"])


def _attempt_job(entry):
    """One ensemble attempt, seeded from the BANK. Runs in a worker.

    The sign of s is MEASURED here exactly as E's stage_3 and R-bank's
    demo_attempt measure it -- both signs evaluated in the extended residual,
    smaller taken -- and it is done in the worker rather than the parent only
    because 160 x 2 flow evaluations is 40 min of serial parent time. Same
    call, same function, same result."""
    idx = entry["global_index"]
    w0, banked = B.load_seed(entry["row"], entry["arm"], entry["field_index"])
    if banked["sha256"] != entry["sha256"]:
        raise SystemExit(f"manifest disagreement at global_index {idx}")
    solver = _solver()
    aps = entry["abs_s_published"]
    r_plus = E.seed_residual(w0, entry["T_published"], aps, solver)
    r_minus = E.seed_residual(w0, entry["T_published"], -aps, solver)
    s0 = aps if r_plus <= r_minus else -aps
    meta = _meta_for(entry)
    meta.update(s_seeded=s0, seed_residual_plus=r_plus,
                seed_residual_minus=r_minus,
                seed_extended_residual=min(r_plus, r_minus))
    rec = E.run_attempt((idx, w0, entry["T_published"], s0, meta))
    return ("attempt", idx, rec)


def _control_job(name):
    solver = _solver()
    if name == "P":
        out = u3_controls.control_P(solver, TOL, MAX_NEWTON, MAX_GMRES,
                                    GMRES_RTOL)
    elif name == "N":
        man, _arr = B.load_bank()
        e0 = man["fields"][0]
        w0, _ = B.load_seed(e0["row"], e0["arm"], 0)
        out = u3_controls.control_N(
            solver, w0, e0["T_published"], e0["s_published"], TOL, MAX_NEWTON,
            MAX_GMRES, GMRES_RTOL, E.MATCH_T_TOL, E.MATCH_S_TOL, E.TABLE_IV)
    else:
        z = np.load(os.path.join(HERE, "u5_m3_converged_orbits.npz"))
        with open(os.path.join(ROOT, "writeup", "data",
                               "p2_prog_r4_m3_v1.json")) as f:
            u5 = json.load(f)["attempts"]
        key = sorted(z.keys())[0]
        a_idx = int(key.split("_")[0].replace("attempt", ""))
        rec = next(a for a in u5 if a["attempt"] == a_idx)
        out = u3_controls.control_R(
            solver, z[key], rec["T_converged"], rec["s_converged"],
            f"U5 {key}", TOL, MAX_NEWTON, MAX_GMRES, GMRES_RTOL)
        ds = abs(((out["delta_s"] + np.pi) % (2 * np.pi)) - np.pi)
        out["harness_predicate_says_recovered"] = bool(
            out["converged_to_tol"] and out["delta_T"] < E.MATCH_T_TOL
            and ds < E.MATCH_S_TOL)
    return ("control", name, out)


def dispatch(job):
    kind, payload = job
    try:
        if kind == "attempt":
            return _attempt_job(payload)
        return _control_job(payload)
    except BaseException as exc:                       # noqa: BLE001
        import traceback
        return ("error", payload if kind == "control"
                else payload.get("global_index"),
                dict(kind=kind, error=repr(exc),
                     traceback=traceback.format_exc()))


# ==========================================================================
# C-PRED -- free, and it runs before anything expensive
# ==========================================================================

def control_pred():
    """E's own matching predicate must be ABLE to return each row, and must
    NOT return one for nonsense. A 0-of-160 from a predicate that can never
    say yes is not a measurement of the physics."""
    hits, misses = [], []
    for name, Tp, sp, _m in E.TABLE_IV:
        hits.append(dict(row=name, returned=E.match_named(Tp, sp, True),
                         ok=bool(E.match_named(Tp, sp, True) == name)))
        misses.append(dict(
            row=name, returned=E.match_named(Tp, sp, False),
            ok=bool(E.match_named(Tp, sp, False) is None),
            why="success=False must never match"))
    far = E.match_named(3.0, 2.9, True)
    return dict(
        control="C-PRED", role="POSITIVE + NEGATIVE, free -- MUST FIRE BOTH",
        n_rows=len(E.TABLE_IV),
        n_positive_ok=sum(1 for h in hits if h["ok"]),
        n_negative_ok=sum(1 for m in misses if m["ok"]),
        nonsense_T_s=(3.0, 2.9), nonsense_returned=far,
        nonsense_ok=bool(far is None),
        fired_as_planted=bool(all(h["ok"] for h in hits)
                              and all(m["ok"] for m in misses)
                              and far is None),
        detail=hits)


# ==========================================================================
# C-REPRO -- the 16 free reproduction controls
# ==========================================================================

def _e_banked():
    with open(E_CURATED) as f:
        cur = {a["attempt"]: a
               for a in json.load(f)["diagnostic_3"]["attempts"]}
    with open(E_LEDGER) as f:
        led = {a["attempt"]: a["ledger"] for a in json.load(f)["attempts"]}
    return cur, led


def compare_to_E(rec, ledger, cur, led):
    ref = cur[rec["e_attempt_index"]]
    rows = [dict(field=k, banked=ref.get(k), reproduced=rec.get(k),
                 exact_equal=_same(rec.get(k), ref.get(k)))
            for k in REPRO_FIELDS]
    n_eq = sum(1 for r in rows if r["exact_equal"])
    old = led[rec["e_attempt_index"]]
    led_eq = _same(ledger, old)
    return dict(
        control="C-REPRO", e_attempt_index=rec["e_attempt_index"],
        row=rec["row"], arm=rec["arm"], global_index=rec["global_index"],
        n_scalar_fields_exact=n_eq, n_scalar_fields_checked=len(rows),
        per_iteration_ledger_exact=bool(led_eq),
        n_iterations_banked=len(old), n_iterations_reproduced=len(ledger),
        n_iterations_byte_equal=sum(1 for a, b in zip(ledger, old)
                                    if _same(a, b)),
        fired_as_planted=bool(led_eq and n_eq == len(rows)),
        mismatches=[r for r in rows if not r["exact_equal"]],
        banked_wall_seconds=ref["wall_seconds"],
        reproduced_wall_seconds=rec["wall_seconds"])


# ==========================================================================
# COMMIT DURING THE RUN -- explicit paths, never -A, never -a
# ==========================================================================

TRACKED = ["experiments/programme_r4/e_fe_partials",
           "experiments/programme_r4/e_fe_driver.py"]


def _git(args, timeout=120):
    return subprocess.run(["git"] + args, cwd=ROOT, capture_output=True,
                          text=True, timeout=timeout)


def commit_partials(tag):
    """Explicit paths only. Failure is logged and never kills the run."""
    for attempt in range(6):
        try:
            a = _git(["add", "--"] + TRACKED)
            if a.returncode != 0:
                time.sleep(20)
                continue
            msg = (f"E-FE leg 408: partials checkpoint {tag} -- "
                   "NOT a landing, NOT a verdict, run still in flight")
            c = _git(["commit", "-m", msg, "--"] + TRACKED)
            if c.returncode == 0 or "nothing to commit" in (
                    c.stdout + c.stderr):
                return True
            time.sleep(20)
        except Exception as exc:                       # noqa: BLE001
            print(f"  [commit] {exc!r}", flush=True)
            time.sleep(20)
    print(f"  [commit] FAILED after retries at {tag}", flush=True)
    return False


class Committer(threading.Thread):
    def __init__(self, every=3300):
        super().__init__(daemon=True)
        self.every, self.stop = every, threading.Event()
        self.n = 0

    def run(self):
        while not self.stop.wait(self.every):
            self.n += 1
            commit_partials(f"#{self.n} t+{self.n * self.every / 3600:.1f}h")


# ==========================================================================
# RUN
# ==========================================================================

def _loadavg():
    with open("/proc/loadavg") as f:
        p = f.read().split()
    return dict(one=float(p[0]), five=float(p[1]), fifteen=float(p[2]),
                raw=" ".join(p[:3]))


def run(args):
    for d in (PARTIALS, PKL_DIR, JSON_DIR, CTRL_DIR):
        os.makedirs(d, exist_ok=True)
    if os.path.exists(ABORT):
        raise SystemExit(f"{ABORT} exists -- a control failed on a previous "
                         "launch. Read it before relaunching.")

    E._assert_table_iv()
    pred = control_pred()
    with open(os.path.join(CTRL_DIR, "C_PRED.json"), "w") as f:
        json.dump(pred, f, indent=1, sort_keys=True)
    print(f"C-PRED fired_as_planted={pred['fired_as_planted']}", flush=True)
    if not pred["fired_as_planted"]:
        raise SystemExit("C-PRED did not fire. The matching predicate cannot "
                         "return a row. STOP -- this is bigger than the gate.")

    man, _arr = B.load_bank()
    fields = man["fields"]
    if len(fields) != N_TOTAL:
        raise SystemExit(f"bank has {len(fields)} fields, expected {N_TOTAL}")
    cur, led = _e_banked()

    originals = [e for e in fields if e["is_E_original"]]
    others = [e for e in fields if not e["is_E_original"]]
    if len(originals) != 16:
        raise SystemExit(f"{len(originals)} originals, expected 16")
    # E's own banked wall time orders the reproduction controls cheapest
    # first, so the C-REPRO verdict arrives in minutes rather than hours.
    originals.sort(key=lambda e: cur[e["e_attempt_index"]]["wall_seconds"])

    jobs = ([("control", "R"), ("control", "P")]
            + [("attempt", e) for e in originals]
            + [("control", "N")]
            + [("attempt", e) for e in others])

    la0 = _loadavg()
    meta = dict(unit="E-FE", leg=408, wave=7, lane="R",
                shards=args.shards, n_jobs=len(jobs), n_attempts=N_TOTAL,
                started_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                          time.gmtime()),
                started_monotonic=time.time(),
                loadavg_at_start=la0, cores=os.cpu_count(),
                briefed_budget_core_hours=91.0,
                briefed_wall_hours_at_6_shards=15.2,
                bank_manifest_sha=man["fields_file_sha256"],
                note=("shards fixed at dispatch and NEVER raised mid-run: a "
                      "unit with a changing shard count cannot report a "
                      "clean per-attempt cost"))
    with open(RUNLOG, "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    print(f"E-FE: {len(jobs)} jobs on {args.shards} shards; "
          f"loadavg {la0['raw']} on {meta['cores']} cores", flush=True)
    commit_partials("t0 (pre-run)")

    committer = Committer(every=args.commit_every)
    committer.start()

    t0 = time.time()
    n_done = 0
    states = {}
    repro = []
    with mp.Pool(args.shards) as pool:
        for kind, key, payload in pool.imap_unordered(dispatch, jobs,
                                                      chunksize=1):
            n_done += 1
            if kind == "error":
                with open(os.path.join(PARTIALS, f"ERROR_{key}.json"),
                          "w") as f:
                    json.dump(payload, f, indent=1, sort_keys=True)
                print(f"  !! ERROR on {key}: {payload['error']}", flush=True)
                continue
            if kind == "control":
                with open(os.path.join(CTRL_DIR, f"C_{key}.json"), "w") as f:
                    json.dump(payload, f, indent=1, sort_keys=True,
                              default=float)
                print(f"  control {key} done", flush=True)
                continue
            rec = payload
            ledger = rec.pop("_ledger")
            w = rec.pop("_w0", None)
            if rec["success"] and w is not None:
                states[f"g{rec['global_index']:03d}_{rec['row']}_"
                       f"{rec['arm']}_f{rec['field_index']}"] = w
            with open(os.path.join(JSON_DIR,
                                   f"g{key:03d}.json"), "w") as f:
                json.dump(dict(rec, _ledger=ledger), f, indent=1,
                          sort_keys=True, default=float)
            if rec["is_E_original"]:
                c = compare_to_E(rec, ledger, cur, led)
                repro.append(c)
                with open(os.path.join(
                        CTRL_DIR,
                        f"C_REPRO_{rec['e_attempt_index']:02d}.json"),
                        "w") as f:
                    json.dump(c, f, indent=1, sort_keys=True, default=float)
                print(f"  C-REPRO E#{rec['e_attempt_index']:2d} "
                      f"{rec['row']:6s} {rec['arm']}: "
                      f"fired={c['fired_as_planted']}", flush=True)
                if not c["fired_as_planted"]:
                    with open(ABORT, "w") as f:
                        json.dump(dict(
                            what="C-REPRO DID NOT FIRE",
                            severity="STOP AND REPORT -- bigger than the gate",
                            control=c), f, indent=1, sort_keys=True,
                            default=float)
                    commit_partials("ABORT: C-REPRO failure")
                    pool.terminate()
                    raise SystemExit(
                        "C-REPRO did not reproduce E's banked attempt "
                        f"{rec['e_attempt_index']} bit for bit. STOPPING.")
            print(f"  [{n_done}/{len(jobs)}] g{key:03d} {rec['row']:6s} "
                  f"{rec['arm']} f{rec['field_index']}: {rec['reason']}, "
                  f"||R||={rec['final_residual']:.4g}, "
                  f"{rec['wall_seconds'] / 3600:.2f} h", flush=True)

    wall = time.time() - t0
    committer.stop.set()
    if states:
        np.savez_compressed(ORBITS, **states)
    meta.update(finished_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                           time.gmtime()),
                wall_seconds=wall, wall_hours=wall / 3600.0,
                core_hours=wall * args.shards / 3600.0,
                loadavg_at_end=_loadavg(),
                n_repro_controls=len(repro),
                n_repro_fired=sum(1 for c in repro if c["fired_as_planted"]),
                commits_during_run=committer.n)
    with open(RUNLOG, "w") as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    commit_partials("final (run complete, gate not yet assembled)")
    print(f"\nrun complete: {wall / 3600:.2f} h wall, "
          f"{wall * args.shards / 3600:.2f} core-hours on {args.shards} "
          f"shards", flush=True)


# ==========================================================================
# GATE
# ==========================================================================

def _load_partials():
    out = {}
    for p in sorted(glob.glob(os.path.join(JSON_DIR, "g*.json"))):
        with open(p) as f:
            r = json.load(f)
        out[r["global_index"]] = r
    return out


def self_hash(doc):
    """Fixed point by construction: the recipe key and the wall-clock keys are
    removed before hashing, so re-hashing the finished file reproduces the
    value. R-bank burned ~19 min learning that a recipe that hashes itself is
    a moving target."""
    d = json.loads(json.dumps(doc, sort_keys=True))
    d.pop("self_hash", None)
    d.pop("self_hash_recipe", None)
    cs = d.get("cost_and_shortfall", {})
    for k in ("wall_seconds", "wall_hours", "core_hours", "started_utc",
              "finished_utc", "started_monotonic", "gate_assembled_utc",
              "per_attempt_wall_seconds", "loadavg_at_start",
              "loadavg_at_end", "seconds_per_attempt_measured"):
        cs.pop(k, None)
    return hashlib.sha256(
        json.dumps(d, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:16]


RECIPE = (
    "sha256 of json.dumps(doc, sort_keys=True, separators=(',',':')) over the "
    "WHOLE artefact after deleting: the key 'self_hash', the key "
    "'self_hash_recipe' (so the recipe is a FIXED POINT and does not move the "
    "hash it describes), and from cost_and_shortfall the wall-clock-valued "
    "keys wall_seconds, wall_hours, core_hours, started_utc, finished_utc, "
    "started_monotonic, gate_assembled_utc, per_attempt_wall_seconds, "
    "seconds_per_attempt_measured, loadavg_at_start, loadavg_at_end. Every "
    "count, every gate answer, every confidence interval and every control "
    "verdict is INSIDE the hash. First 16 hex chars.")


def gate(args):
    recs = _load_partials()
    cur, led = _e_banked()
    with open(RUNLOG) as f:
        meta = json.load(f)
    ctrls = {}
    for p in sorted(glob.glob(os.path.join(CTRL_DIR, "*.json"))):
        with open(p) as f:
            ctrls[os.path.basename(p)[:-5]] = json.load(f)

    n = len(recs)
    vals = list(recs.values())
    n_conv = sum(1 for r in vals if r["success"])
    n_own = sum(1 for r in vals if r["recovered_named_orbit"])
    n_any = sum(1 for r in vals if r["recovered_any_named_orbit"])
    n_abs = sum(1 for r in vals if r["matched_row_abs_secondary"])

    table = []
    for name, _Tp, _sp, _m in E.TABLE_IV:
        for arm in ("S", "Q"):
            g = [r for r in vals if r["row"] == name and r["arm"] == arm]
            k_own = sum(1 for r in g if r["recovered_named_orbit"])
            k_any = sum(1 for r in g if r["recovered_any_named_orbit"])
            table.append(dict(
                row=name, arm=arm, n_draws=len(g),
                n_converged=sum(1 for r in g if r["success"]),
                k_recovered_own_row=k_own, k_recovered_any_row=k_any,
                recovery_rate_out_of_10=f"{k_own}/{len(g)}",
                exact_binomial=clopper_pearson(k_own, len(g)),
                best_final_residual=min((r["final_residual"] for r in g),
                                        default=None),
                min_delta_T_from_published=min(
                    (r["delta_T_from_published"] for r in g), default=None),
                min_delta_abs_s_from_published=min(
                    (r["delta_abs_s_from_published"] for r in g),
                    default=None),
                reasons=dict(Counter(r["reason"] for r in g))))

    per_row = []
    for name, _Tp, _sp, _m in E.TABLE_IV:
        g = [r for r in vals if r["row"] == name]
        k = sum(1 for r in g if r["recovered_named_orbit"])
        per_row.append(dict(row=name, n_draws=len(g), k_recovered_own_row=k,
                            exact_binomial=clopper_pearson(k, len(g))))

    any_yes = bool(n_own > 0)
    doc = dict(
        unit="E-FE", leg=408, wave=7, lane="R", programme="PROG-R4",
        kind="measurement at scale",
        what=("160 direct-seed attempts: E's 8 Table IV rows x 2 arms x 10 "
              "independent banked fields per (row, arm). Rows and arms FIXED; "
              "only the DRAW varies."),
        gate_source=("writeup/waves/WAVE7_PLAN.md SS B, verbatim; SS B is "
                     "BINDING where it and the dispatch brief differ"),
        gate=dict(
            question=("how many of 160 converge; how many recover a named "
                      "row; per (row, arm) the recovery rate out of 10 with "
                      "an exact binomial CI; does ANY row recover in ANY of "
                      "its 10 draws, YES or NO?"),
            n_attempts=n,
            n_converged=n_conv,
            n_recovered_its_own_named_row=n_own,
            n_recovered_any_named_row=n_any,
            n_recovered_abs_secondary=n_abs,
            ANY_ROW_RECOVERS_IN_ANY_DRAW=("YES" if any_yes else "NO"),
            answer_scope=("the primary predicate is E's match_named, "
                          "unchanged: |T - T_pub| < 0.05 AND wrapped "
                          "|s - s_pub| < 0.05 AND success. The |s|-only "
                          "variant is SECONDARY and no verdict rests on it."),
            confidence_interval_method=(
                "Clopper-Pearson exact binomial (Clopper & Pearson 1934, "
                "Biometrika 26(4):404-413), computed by Beta-quantile "
                "inversion via scipy.stats.beta. TAIL CONVENTION: both are "
                "reported. 'two_sided_95_*' is the equal-tailed 95% interval "
                "(alpha/2 in each tail) -- this is what 'its exact binomial "
                "confidence interval' means. 'one_sided_95_upper' is the 95% "
                "upper bound with all 5% in the upper tail -- this is the "
                "convention behind SS B's '26%'."),
            per_row_arm=table,
            per_row_pooled_over_arms_SECONDARY=per_row,
            pooled_over_all_160=clopper_pearson(n_own, n),
            reasons=dict(Counter(r["reason"] for r in vals)),
            closest_approach=min(
                ({k: r[k] for k in ("row", "arm", "global_index",
                                    "field_index", "delta_T_from_published",
                                    "delta_s_from_published",
                                    "delta_abs_s_from_published",
                                    "final_residual", "success")}
                 for r in vals),
                key=lambda d: (d["delta_T_from_published"]
                               + d["delta_abs_s_from_published"]))
            if vals else None),
        controls=ctrls,
        readings=dict(),          # filled by --gate's caller block below
        cost_and_shortfall=dict(),
        ceilings=[], defects_found=[], clay_movement=dict(), sources_3k=dict())
    doc["_run_meta"] = meta
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--shards", type=int, default=6)
    ap.add_argument("--commit-every", type=int, default=3300)
    args = ap.parse_args()
    if args.run:
        run(args)
    elif args.gate:
        d = gate(args)
        print(json.dumps(d["gate"], indent=1, default=float)[:4000])
    else:
        ap.error("one of --run / --gate")


if __name__ == "__main__":
    main()
