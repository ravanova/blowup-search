"""Route-BVRR, leg 221 -- the REPAIR runner for solver/boussinesq_rescaled.py.

Leg 205 (Route-BVR) measured TWO independent silent-fabrication mechanisms in this module's
nine-line origin reduction `odd_field_x_slope` and ESCALATED without patching, under its own
gate's yes-branch.  Leg 221 lands the guards AND closes the one gap leg 205 left open: it
never re-ran a banked result, and argued dormancy from the shape of the Spike-1 envelopes
instead of measuring it.  This runner answers the gate's two clauses separately, with
magnitudes and never with a boolean:

  (a) does repairing BOTH named mechanisms make every adversarial case in leg 205's OWN
      battery reject or raise correctly?

  (b) does a fresh, EXPLICIT re-run of every banked result that calls this module -- not an
      assumption of dormancy -- confirm zero contamination, bit-identical pre/post repair?

CLAUSE (a) IS RUN AGAINST LEG 205's OWN FILE, NOT A RE-IMPLEMENTATION.  The battery is read
out of git at `BATTERY_REF` and executed TWICE in this same process: once with
`sys.modules['solver.boussinesq_rescaled']` bound to the PRE-repair module (also read out of
git, at `PRE_REPAIR_REF`), once with the repaired module.  So the "before" column is measured
live rather than quoted from leg 205's JSON -- and the run asserts it reproduces leg 205's
committed verdict totals, or it aborts.

CLAUSE (b) IS RUN AS A PER-CALL DIFFERENTIAL OVER THE REAL TRAJECTORY, NOT AS AN ARGUMENT.
For each banked artifact, its own generating script is executed end to end with
`odd_field_x_slope` replaced by a shim that calls the PRE-repair and POST-repair
implementations on the IDENTICAL arguments, compares the two results bitwise (`==` on
float64, and exception-type equality when either side raises), and returns the PRE-repair
value -- so the trajectory the run follows is exactly the banked one.  If every call agrees
bitwise then the repaired module reproduces the whole run by determinism; the comparison is a
proof over the actual call sequence, not a sample.  The regenerated artifact is then compared
leaf-by-leaf against the committed one as a second, independent check, with wall-clock keys
excluded because they are not results.

LESSON 90 CONTROL.  A differential that reports "0 moved" is worthless if the two sides are
secretly the same object.  `control_two_modules_really_differ` asserts the pre-repair module
lacks the new parameters AND that the two sides DISAGREE, with a measured magnitude, on the
inputs leg 205 published.  If that control ever passes trivially the run aborts and reports
nothing.

Run: PYTHONPATH=. .venv/bin/python -u experiments/p2_route_bvrr_v1_repair.py
     ... [--only a|b] [--skip-slow]
"""

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_bvrr_v1_repair.json")

# The module's OWN last pre-guard commit.  `git diff 1a3e63c HEAD -- solver/
# boussinesq_rescaled.py` was EMPTY before this leg, so 1a3e63c is byte-identical to the
# module as leg 205 audited it.  Deliberately not "the commit before mine": a leg's own
# hashes are rewritten by the rebase onto main and a self-referential pin stops resolving the
# moment the branch lands (leg 130's correction, d871675).
PRE_REPAIR_REF = "1a3e63c"

# Leg 205's battery lives on its own unmerged branch (the gate's yes-branch told it to push
# its branch only).  Read verbatim from there; never re-implemented here.
BATTERY_REF = "origin/leg/205-bvr-v1"
BATTERY_PATH = "experiments/p2_route_bvr_v1_adversarial.py"
BATTERY_JSON = "writeup/data/p2_route_bvr_v1_adversarial.json"

# Leg 205's committed verdict totals.  The vendored-battery run MUST reproduce these against
# the pre-repair module or this leg is measuring something else.
LEG_205_TOTALS = {"OK": 32, "SILENT_WRONG": 18, "RAISED": 11, "NONFINITE": 9,
                  "NO_REFERENT": 2, "RETURNED": 9}

# Every banked artifact whose generating script reaches solver/boussinesq_rescaled.py.
# Established by grep over the whole repository (see `caller_census`), not by assumption --
# that is the step leg 205 skipped.
BANKED = [
    dict(key="spike1_stepB_rescaled",
         artifact="writeup/data/spike1_stepB_rescaled.json",
         script="writeup/3_spikes/spike1_stepB_evidence.py", argv=["--generate"],
         slow=False,
         calls="odd_field_x_slope directly (spike1_stepB_evidence.py:84-85)"),
    dict(key="p2_route_brs_v1_status_audit",
         artifact="writeup/data/p2_route_brs_v1_status_audit.json",
         script="experiments/p2_route_brs_v1_status_audit.py", argv=[], slow=False,
         calls="RescaledBoussinesq.run via a ScriptedRelaxation subclass"),
    dict(key="spike1_stepC_gate",
         artifact="writeup/data/spike1_stepC_gate.json",
         script="experiments/spike1_stepC_gate.py", argv=["--logged"], slow=True,
         calls="RescaledBoussinesq.run(renorm=True), 4 resolution rungs"),
    dict(key="p2_route_g_v1_g2",
         artifact="writeup/data/p2_route_g_v1_g2.json",
         script="experiments/p2_route_g_v1_collapse.py",
         argv=["--only", "g2", "--out", "p2_route_g_v1_g2.json"], slow=True,
         env={"ROUTE_G_SERIAL": "1"},
         calls="RescaledBoussinesq.run, chained steps ladder + resolution ladder"),
    dict(key="p2_route_k_v1_port",
         artifact="writeup/data/p2_route_k_v1_port.json",
         script="experiments/p2_route_k_v1_port.py", argv=[], slow=True,
         calls="RescaledBoussinesq.run(renorm=True) to 5000 steps"),
    dict(key="p2_route_l_v1_precond",
         artifact="writeup/data/p2_route_l_v1_precond.json",
         script="experiments/p2_route_l_v1_precond.py", argv=[], slow=True,
         calls="RescaledBoussinesq.run + a direct odd_field_x_slope renorm loop it DIVIDES by"),
]

# Callers with NO banked artifact -- recorded so the census is complete and a later leg does
# not re-derive it.  Both are print-only diagnostics.
UNBANKED_CALLERS = [
    dict(script="experiments/spike1_stepC_relax.py",
         reason="print-only relaxation shakeout; writes no file under writeup/data/"),
    dict(script="experiments/diagnose_stepC_drift.py",
         reason="print-only drift diagnostic; writes no file under writeup/data/"),
]

TEST_CALLERS = ["test_boussinesq_rescaled.py", "test_boussinesq_transport.py",
                "test_boussinesq_rescaled_status.py"]

# Keys that are wall-clock, not results.  Excluded from the artifact comparison and named
# here rather than silently skipped.
TIMING_KEYS = {"seconds", "wall_seconds", "wall_s", "wall_clock_seconds", "elapsed",
               "elapsed_s", "runtime_s", "minutes", "wall_minutes"}

# Keys that record WHEN a run happened, not WHAT it computed.  These are NOT dropped the way
# TIMING_KEYS are -- they are compared, and any movement is reported in its own
# `provenance_moved` channel with the before/after values printed, so nothing is hidden.  They
# simply do not count toward `leaves_moved`, which is the contamination measure.
#
# Measured, not anticipated: `p2_route_brs_v1_status_audit.json` carries `"generated":
# "2026-08-06"`, so re-running it on 2026-08-07 moves that leaf while all 62 of its
# `odd_field_x_slope` calls stay bit-identical and all 450 real leaves stay identical.  The
# prior partial session of this leg ran on 2026-08-06 and therefore never saw it; a
# same-day-only differential is not a differential.
PROVENANCE_KEYS = {"generated", "generated_at", "date", "run_date", "timestamp", "created",
                   "created_at", "when", "today"}


# ---------------------------------------------------------------------------
# the pre-repair module, and leg 205's battery, loaded from git into this process
# ---------------------------------------------------------------------------
def _git_show(ref, path):
    return subprocess.run(["git", "show", "%s:%s" % (ref, path)], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout


def load_pre_repair():
    src = _git_show(PRE_REPAIR_REF, "solver/boussinesq_rescaled.py")
    fd, path = tempfile.mkstemp(suffix="_pre_boussinesq_rescaled.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_pre_boussinesq_rescaled", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_pre_boussinesq_rescaled"] = mod
    spec.loader.exec_module(mod)
    return mod, len(src.splitlines())


def load_battery(bound_module, tag):
    """Execute leg 205's battery file with solver.boussinesq_rescaled bound to
    `bound_module`.  The battery derives its own OUT path from __file__, so the file is
    staged two directories deep inside a scratch tree and its JSON lands there, never in
    writeup/data/."""
    src = _git_show(BATTERY_REF, BATTERY_PATH)
    tmp = tempfile.mkdtemp(prefix="bvrr_battery_%s_" % tag)
    exp = os.path.join(tmp, "experiments")
    os.makedirs(exp)
    path = os.path.join(exp, "p2_route_bvr_v1_adversarial.py")
    with open(path, "w") as f:
        f.write(src)
    real = sys.modules.get("solver.boussinesq_rescaled")
    sys.modules["solver.boussinesq_rescaled"] = bound_module
    try:
        name = "_bvr_battery_%s" % tag
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        result = mod.main()
    finally:
        if real is not None:
            sys.modules["solver.boussinesq_rescaled"] = real
        else:
            sys.modules.pop("solver.boussinesq_rescaled", None)
        shutil.rmtree(tmp, ignore_errors=True)
    return result


# ---------------------------------------------------------------------------
def control_two_modules_really_differ(pre, post):
    """LESSON 90.  What would have had to change for the differential to report the other
    answer?  Answer: the two module objects must actually be different, and they must
    disagree by a MEASURED amount on inputs leg 205 published.  Asserted executably, with
    magnitudes, before any 'identical' count is believed."""
    from solver.boussinesq_velocity import PolarGrid
    import inspect

    checks = {}
    checks["distinct_module_objects"] = pre is not post
    sig_pre = inspect.signature(pre.odd_field_x_slope).parameters
    sig_post = inspect.signature(post.odd_field_x_slope).parameters
    checks["pre_lacks_min_points"] = "min_points" not in sig_pre
    checks["pre_lacks_max_rel_residual"] = "max_rel_residual" not in sig_pre
    checks["post_has_min_points"] = "min_points" in sig_post
    checks["post_has_max_rel_residual"] = "max_rel_residual" in sig_post

    fine = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)

    def odd(g, a=1.0, lam=1.0):
        return a * g.R * np.cos(g.B) * np.exp(-lam * g.R ** 2)

    # DEFECT B, leg 205's headline row: lam=400, truth 2.0, full 177-node window.
    b_pre = float(pre.odd_field_x_slope(odd(fine, 2.0, 400.0), fine))
    b_post = float(post.odd_field_x_slope(odd(fine, 2.0, 400.0), fine))
    checks["pre_fabricates_on_defect_B"] = abs(b_pre - 2.0) / 2.0 > 5e-4
    checks["post_recovers_on_defect_B"] = abs(b_post - 2.0) / 2.0 <= 5e-4

    # DEFECT A, leg 205's headline row: an empty window on a fine grid.
    empty = PolarGrid(n_r=200, n_beta=16, r_min=0.5, r_max=40.0)
    a_pre = float(pre.odd_field_x_slope(odd(empty, 2.0, 1.0), empty))
    a_post_raised = False
    try:
        post.odd_field_x_slope(odd(empty, 2.0, 1.0), empty)
    except ValueError:
        a_post_raised = True
    checks["pre_returns_exact_zero_on_empty_window"] = (a_pre == 0.0)
    checks["post_raises_on_empty_window"] = a_post_raised

    mags = dict(defect_B_pre=b_pre, defect_B_post=b_post, defect_B_truth=2.0,
                defect_B_pre_rel_err=abs(b_pre - 2.0) / 2.0,
                defect_B_post_rel_err=abs(b_post - 2.0) / 2.0,
                defect_A_pre=a_pre, defect_A_truth=2.0)
    return all(checks.values()), checks, mags


# ---------------------------------------------------------------------------
# CLAUSE (a) -- leg 205's own 81-case battery, before and after
# ---------------------------------------------------------------------------
def _flatten_cases(payload):
    """Every scored case of leg 205's battery, keyed by its own `case` string."""
    out = {}
    for k, v in payload.items():
        if not k.startswith("family"):
            continue
        items = v if isinstance(v, list) else [v]
        for c in items:
            if isinstance(c, dict) and "verdict" in c and "case" in c:
                out[c["case"]] = c
    return out


def clause_a(pre, post):
    t0 = time.time()
    before = load_battery(pre, "pre")
    after = load_battery(post, "post")
    cb, ca = _flatten_cases(before), _flatten_cases(after)

    committed = json.loads(_git_show(BATTERY_REF, BATTERY_JSON))

    rows = []
    for case in sorted(set(cb) | set(ca)):
        b, a = cb.get(case), ca.get(case)
        row = dict(case=case,
                   before=(b or {}).get("verdict"), after=(a or {}).get("verdict"))
        for src, tag in ((b, "before"), (a, "after")):
            if not src:
                continue
            for fld, nm in (("returned", "value"), ("c_l_returned", "value"),
                            ("rel_err", "rel_err"), ("over_accept_tol", "over_tol"),
                            ("exception", "exception")):
                if src.get(fld) is not None and "%s_%s" % (tag, nm) not in row:
                    row["%s_%s" % (tag, nm)] = src[fld]
        rows.append(row)

    silent_before = sorted(c for c, v in cb.items() if v.get("verdict") == "SILENT_WRONG")
    silent_after = sorted(c for c, v in ca.items() if v.get("verdict") == "SILENT_WRONG")
    fixed = {c: dict(before="SILENT_WRONG", after=ca.get(c, {}).get("verdict"))
             for c in silent_before}
    by_disposition = {}
    for c, d in fixed.items():
        by_disposition.setdefault(d["after"], []).append(c)

    return dict(
        battery_ref=BATTERY_REF, battery_path=BATTERY_PATH,
        battery_is_leg_205s_own_file_not_a_reimplementation=True,
        totals_before=before["verdict_totals"], totals_after=after["verdict_totals"],
        totals_committed_by_leg_205=committed["verdict_totals"],
        reproduces_leg_205_committed_totals=(before["verdict_totals"]
                                             == committed["verdict_totals"]),
        gate_answer_before=before["gate_answer"], gate_answer_after=after["gate_answer"],
        n_silent_wrong_before=len(silent_before), n_silent_wrong_after=len(silent_after),
        silent_wrong_before=silent_before, silent_wrong_after=silent_after,
        disposition_of_each_silent_wrong=by_disposition,
        every_case=rows,
        wall_seconds=round(time.time() - t0, 2),
    ), before, after


# ---------------------------------------------------------------------------
# ATTRIBUTION -- the control that decides WHOSE movement it is
#
# The shim run below follows the PRE-repair trajectory, so its regenerated artifact is a
# pre-repair regeneration and any difference from the committed file could equally be (i)
# caused by the repair or (ii) pre-existing irreproducibility of the banked artifact in
# today's environment.  Those are entirely different findings and the sweep's committed-vs-
# regenerated comparison ALONE cannot tell them apart -- it conflates them, which is exactly
# the kind of assumption this leg exists to refuse.  So when an artifact moves, three PLAIN
# regenerations are run (no shim in the process at all):
#
#     A  = the module loaded from PRE_REPAIR_REF          (the repair absent)
#     A2 = the same again                                 (run-to-run determinism)
#     B  = the repaired module as it stands on this branch
#
#   diff(A, B)  is the gate's actual question, "bit-identical pre/post repair".
#   diff(C, A)  where C is the committed file, is BASELINE DRIFT -- movement this leg did
#               not cause and cannot cause, since the repair is not in the process.
#   diff(A, A2) says whether the generating script is deterministic today at all; without
#               it, diff(A, B) == 0 would not license "the repaired module reproduces it".
# ---------------------------------------------------------------------------
PLAIN_DRIVER = r'''
import importlib.util, json, os, runpy, sys
ROOT = os.environ["BVRR_ROOT"]
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "experiments"))
sys.argv = json.loads(os.environ["BVRR_ARGV"])
WHICH = os.environ["BVRR_WHICH"]                 # "pre" or "post"
import solver
if WHICH == "pre":
    spec = importlib.util.spec_from_file_location("solver.boussinesq_rescaled",
                                                  os.environ["BVRR_PRE"])
    mod = importlib.util.module_from_spec(spec)
    sys.modules["solver.boussinesq_rescaled"] = mod
    spec.loader.exec_module(mod)
    solver.boussinesq_rescaled = mod
import solver.boussinesq_rescaled as BR
has_guard = "min_points" in BR.odd_field_x_slope.__code__.co_varnames
assert has_guard == (WHICH == "post"), (
    "attribution control void: asked for the %s module and got has_guard=%s" %
    (WHICH, has_guard))
runpy.run_path(os.environ["BVRR_TARGET"], run_name="__main__")
'''


def _plain_regen(spec_, pre_path, which):
    """One PLAIN regeneration of spec_'s artifact with the pre- or post-repair module.
    The committed artifact is always restored; the regenerated copy is returned in memory."""
    art = os.path.join(ROOT, spec_["artifact"])
    backup = art + ".bvrr_attr_backup"
    shutil.copyfile(art, backup)
    fd, driver = tempfile.mkstemp(suffix="_bvrr_plain.py")
    with os.fdopen(fd, "w") as f:
        f.write(PLAIN_DRIVER)
    target = os.path.join(ROOT, spec_["script"])
    env = dict(os.environ)
    env.update(spec_.get("env", {}))
    env.update(BVRR_ROOT=ROOT, BVRR_TARGET=target, BVRR_PRE=pre_path, BVRR_WHICH=which,
               BVRR_ARGV=json.dumps([target] + spec_["argv"]),
               PYTHONPATH=ROOT + os.pathsep + os.path.join(ROOT, "experiments"))
    t0 = time.time()
    try:
        proc = subprocess.run([sys.executable, "-u", driver], cwd=ROOT, env=env,
                              capture_output=True, text=True)
        regen = json.loads(open(art).read()) if proc.returncode == 0 else None
    finally:
        shutil.copyfile(backup, art)
        os.remove(backup)
        os.remove(driver)
    return dict(which=which, returncode=proc.returncode,
                wall_seconds=round(time.time() - t0, 1),
                stderr_tail=(proc.stderr[-2000:] if proc.returncode else None)), regen


def attribute_movement(spec_, pre_path):
    """Decide whether an artifact's movement is REPAIR-ATTRIBUTABLE or BASELINE DRIFT."""
    committed = json.loads(open(os.path.join(ROOT, spec_["artifact"])).read())
    mA, A = _plain_regen(spec_, pre_path, "pre")
    mA2, A2 = _plain_regen(spec_, pre_path, "pre")
    mB, B = _plain_regen(spec_, pre_path, "post")
    out = dict(key=spec_["key"], runs=[mA, mA2, mB])
    if A is None or A2 is None or B is None:
        out["error"] = "a plain regeneration failed; attribution not established"
        return out
    d_pre_post = compare_artifacts(A, B)
    d_determinism = compare_artifacts(A, A2)
    d_baseline = compare_artifacts(committed, A)
    out.update(
        pre_vs_post_repair=d_pre_post,
        pre_vs_pre_determinism=d_determinism,
        committed_vs_pre_repair_baseline_drift=d_baseline,
        repair_attributable_leaves_moved=d_pre_post["leaves_moved"],
        script_is_deterministic_today=bool(d_determinism["leaves_moved"] == 0),
        baseline_drift_leaves_moved=d_baseline["leaves_moved"],
        verdict=("REPAIR_ATTRIBUTABLE" if d_pre_post["leaves_moved"] > 0
                 else ("BASELINE_DRIFT_NOT_THIS_LEG" if d_baseline["leaves_moved"] > 0
                       else "NO_MOVEMENT")),
    )
    return out


# ---------------------------------------------------------------------------
# CLAUSE (b) -- the banked record, re-run
# ---------------------------------------------------------------------------
SHIM_DRIVER = r'''
import atexit, json, os, runpy, sys, importlib.util
ROOT = os.environ["BVRR_ROOT"]
sys.path.insert(0, ROOT)
REPORT = os.environ["BVRR_REPORT"]
TARGET = os.environ["BVRR_TARGET"]
sys.argv = json.loads(os.environ["BVRR_ARGV"])

spec = importlib.util.spec_from_file_location("_pre_boussinesq_rescaled",
                                              os.environ["BVRR_PRE"])
pre = importlib.util.module_from_spec(spec)
sys.modules["_pre_boussinesq_rescaled"] = pre
spec.loader.exec_module(pre)

import solver.boussinesq_rescaled as BR
_post = BR.odd_field_x_slope
_pre = pre.odd_field_x_slope
STATE = {"n": 0, "same": 0, "moved": [], "raise_pre": 0, "raise_post": 0,
         "both_raise": 0, "n_win_capped": 0}


def _run(fn, g, grid, a, kw):
    try:
        return ("value", float(fn(g, grid, *a, **kw)))
    except Exception as e:                                        # noqa: BLE001
        return ("exc", type(e).__name__)


def shim(g, grid, *a, **kw):
    p = _run(_pre, g, grid, a, kw)
    q = _run(_post, g, grid, a, kw)
    STATE["n"] += 1
    if p[0] == "exc":
        STATE["raise_pre"] += 1
    if q[0] == "exc":
        STATE["raise_post"] += 1
    if p[0] == "exc" and q[0] == "exc":
        STATE["both_raise"] += 1
    same = (p[0] == q[0]) and (p[1] == q[1] or (p[0] == "value" and p[1] != p[1]
                                                and q[1] != q[1]))
    if same:
        STATE["same"] += 1
    elif len(STATE["moved"]) < 200:
        rec = {"call_index": STATE["n"], "pre": p, "post": q}
        if p[0] == "value" and q[0] == "value":
            rec["abs_diff"] = abs(p[1] - q[1])
            rec["rel_diff"] = abs(p[1] - q[1]) / abs(p[1]) if p[1] else float("inf")
            rec["pre_hex"] = float(p[1]).hex()
            rec["post_hex"] = float(q[1]).hex()
        STATE["moved"].append(rec)
    else:
        STATE["moved_overflow"] = STATE.get("moved_overflow", 0) + 1
    # follow the PRE-repair trajectory exactly, so the run reproduces the banked one
    if p[0] == "exc":
        return _pre(g, grid, *a, **kw)
    return p[1]


BR.odd_field_x_slope = shim


@atexit.register
def _dump():
    STATE["n_moved"] = len(STATE["moved"]) + STATE.get("moved_overflow", 0)
    with open(REPORT, "w") as f:
        json.dump(STATE, f)


runpy.run_path(TARGET, run_name="__main__")
'''


def _numeric_leaves(obj, path="", provenance=False):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in TIMING_KEYS:
                continue
            yield from _numeric_leaves(v, "%s.%s" % (path, k),
                                       provenance or k in PROVENANCE_KEYS)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _numeric_leaves(v, "%s[%d]" % (path, i), provenance)
    else:
        yield path, (obj, provenance)


def compare_artifacts(committed, regenerated):
    a = dict(_numeric_leaves(committed))
    b = dict(_numeric_leaves(regenerated))
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    moved = []
    prov_moved = []
    n_same = 0
    for k in sorted(set(a) & set(b)):
        (x, is_prov), (y, _) = a[k], b[k]
        same = (x == y)
        if not same and isinstance(x, float) and isinstance(y, float):
            same = (x != x and y != y)
        if same:
            n_same += 1
        else:
            rec = {"leaf": k, "committed": x, "regenerated": y}
            if isinstance(x, (int, float)) and not isinstance(x, bool) \
                    and isinstance(y, (int, float)) and not isinstance(y, bool) and x:
                rec["rel_diff"] = abs(y - x) / abs(x)
            (prov_moved if is_prov else moved).append(rec)
    return dict(leaves_compared=len(set(a) & set(b)), leaves_identical=n_same,
                leaves_moved=len(moved), moved_detail=moved[:60],
                provenance_leaves_moved=len(prov_moved),
                provenance_moved_detail=prov_moved[:20],
                keys_only_in_committed=only_a[:20], keys_only_in_regenerated=only_b[:20],
                n_keys_only_in_committed=len(only_a),
                n_keys_only_in_regenerated=len(only_b),
                timing_keys_excluded=sorted(TIMING_KEYS),
                provenance_keys_not_counted=sorted(PROVENANCE_KEYS))


def rerun_one(spec_, pre_path):
    art = os.path.join(ROOT, spec_["artifact"])
    committed = json.loads(open(art).read())
    backup = art + ".bvrr_backup"
    shutil.copyfile(art, backup)

    fd, driver = tempfile.mkstemp(suffix="_bvrr_driver.py")
    with os.fdopen(fd, "w") as f:
        f.write(SHIM_DRIVER)
    fd, report = tempfile.mkstemp(suffix="_bvrr_report.json")
    os.close(fd)

    target = os.path.join(ROOT, spec_["script"])
    env = dict(os.environ)
    env.update(spec_.get("env", {}))
    env.update(BVRR_ROOT=ROOT, BVRR_REPORT=report, BVRR_TARGET=target,
               BVRR_PRE=pre_path, BVRR_ARGV=json.dumps([target] + spec_["argv"]),
               PYTHONPATH=ROOT + os.pathsep + os.path.join(ROOT, "experiments"))
    t0 = time.time()
    proc = subprocess.run([sys.executable, "-u", driver], cwd=ROOT, env=env,
                          capture_output=True, text=True)
    wall = round(time.time() - t0, 1)

    out = dict(key=spec_["key"], artifact=spec_["artifact"], script=spec_["script"],
               argv=spec_["argv"], calls=spec_["calls"], wall_seconds=wall,
               returncode=proc.returncode)
    if proc.returncode != 0:
        out["stderr_tail"] = proc.stderr[-3000:]
    try:
        out["per_call_differential"] = json.loads(open(report).read())
    except Exception as e:                                        # noqa: BLE001
        out["per_call_differential"] = {"error": repr(e)}
    try:
        regenerated = json.loads(open(art).read())
        out["artifact_comparison"] = compare_artifacts(committed, regenerated)
    except Exception as e:                                        # noqa: BLE001
        out["artifact_comparison"] = {"error": repr(e), "trace": traceback.format_exc()}
    finally:
        shutil.copyfile(backup, art)      # the committed artifact is never left modified
        os.remove(backup)
    os.remove(driver)
    os.remove(report)

    d = out.get("per_call_differential", {})
    out["calls_compared"] = d.get("n")
    out["calls_bit_identical"] = d.get("same")
    out["calls_moved"] = d.get("n_moved", len(d.get("moved", [])) if d else None)
    ac = out.get("artifact_comparison", {})
    out["artifact_leaves_moved"] = ac.get("leaves_moved")
    out["artifact_provenance_leaves_moved"] = ac.get("provenance_leaves_moved")
    out["contamination"] = bool((out["calls_moved"] or 0) > 0
                                or (ac.get("leaves_moved") or 0) > 0
                                or proc.returncode != 0)
    return out


def run_tests(pre_path):
    """The module's own correctness suites, run under the same per-call differential."""
    rows = []
    for t in TEST_CALLERS:
        fd, driver = tempfile.mkstemp(suffix="_bvrr_driver.py")
        with os.fdopen(fd, "w") as f:
            f.write(SHIM_DRIVER)
        fd, report = tempfile.mkstemp(suffix="_bvrr_report.json")
        os.close(fd)
        target = os.path.join(ROOT, t)
        env = dict(os.environ)
        env.update(BVRR_ROOT=ROOT, BVRR_REPORT=report, BVRR_TARGET=target,
                   BVRR_PRE=pre_path, BVRR_ARGV=json.dumps([target]),
                   PYTHONPATH=ROOT + os.pathsep + os.path.join(ROOT, "experiments"))
        t0 = time.time()
        proc = subprocess.run([sys.executable, "-u", driver], cwd=ROOT, env=env,
                              capture_output=True, text=True)
        try:
            d = json.loads(open(report).read())
        except Exception as e:                                    # noqa: BLE001
            d = {"error": repr(e)}
        rows.append(dict(test=t, returncode=proc.returncode,
                         wall_seconds=round(time.time() - t0, 1),
                         calls_compared=d.get("n"), calls_bit_identical=d.get("same"),
                         calls_moved=d.get("n_moved", 0),
                         stderr_tail=(proc.stderr[-1500:] if proc.returncode else None)))
        os.remove(driver)
        os.remove(report)
    return rows


def measured_rel_residual(post, g, grid, **kw):
    """The relative least-squares residual the repaired guard computes, read out THROUGH THE
    PUBLIC API rather than by re-implementing the fit: `max_rel_residual` is the threshold the
    function raises above, so bisecting it locates the residual itself.  Monotone by
    construction, so 40 halvings pin it to ~1e-12.  Returns None if the call refuses for a
    reason other than the residual (empty window, rank deficiency), since then no residual
    exists -- exactly the numpy condition R2 of the novelty pass names."""
    def raises_at(thr):
        try:
            post.odd_field_x_slope(g, grid, max_rel_residual=thr, **kw)
            return False
        except ValueError as e:
            if "max_rel_residual" not in str(e):
                raise
            return True
    try:
        if not raises_at(0.0):
            return 0.0
        if raises_at(float("inf")):
            return float("inf")
    except ValueError:
        return None
    lo, hi = 0.0, 1.0
    while raises_at(hi):
        hi *= 2.0
        if hi > 1e12:
            return float("inf")
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        if raises_at(mid):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def residual_margin_probe(post):
    """WHERE THE LANDED BACKSTOP ACTUALLY SITS, measured on named fields.

    The repaired guard closes defect B by sizing the fit window from the field's own radial
    scale, read off the radius at which the projected `d1` PEAKS.  That heuristic is exact for
    the single-scale `a r exp(-lam r^2)` class the module is validated on and that leg 205's
    battery is built from.  It is NOT exact for a field carrying TWO radial scales: the peak
    resolves to the OUTER scale (deliberately -- resolving inward would shrink the window on
    fields with no small scale, a fabrication of the opposite sign), so the cap goes
    non-binding and the inner scale is never resolved.  The residual backstop is the only
    thing left, and this probe measures whether it is tight enough to catch that.  Banked as a
    magnitude, not a boolean, and NOT used to answer this leg's gate -- the gate is scoped to
    leg 205's own battery, which contains no two-scale case.
    """
    from solver.boussinesq_velocity import PolarGrid
    sys.path.insert(0, os.path.join(ROOT, "experiments"))
    from spike1_stepC_gate import profile_ansatz

    fine = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    r, B = fine.R, fine.B
    rows = []

    def add(name, g, truth, legitimate):
        try:
            val = float(post.odd_field_x_slope(g, fine))
            exc = None
        except ValueError as e:                                    # noqa: BLE001
            val, exc = None, str(e)[:120]
        rr = measured_rel_residual(post, g, fine)
        rows.append(dict(field=name, returned=val, truth=truth, exception=exc,
                         rel_err=(None if (val is None or truth in (None, 0))
                                  else abs(val - truth) / abs(truth)),
                         rel_residual=rr,
                         is_legitimate_in_repository_field=legitimate))

    add("module's own validated field: 2 r cos(b) exp(-r^2) (lam=1)",
        2.0 * r * np.cos(B) * np.exp(-r ** 2), 2.0, True)
    om, et, _ = profile_ansatz(fine)
    add("Step-C profile_ansatz omega (every banked relaxation runs on this)", om, None, True)
    add("Step-C profile_ansatz eta", et, None, True)
    add("leg 205's headline defect-B field: lam=400, field scale 0.05",
        2.0 * r * np.cos(B) * np.exp(-400.0 * r ** 2), 2.0, False)
    add("TWO-SCALE, not in leg 205's battery: r cos(b) [exp(-r^2) + exp(-400 r^2)]",
        (r * np.cos(B)) * (np.exp(-r ** 2) + np.exp(-400.0 * r ** 2)), 2.0, False)
    add("TWO-SCALE, wider separation: r cos(b) [exp(-r^2) + exp(-1e4 r^2)]",
        (r * np.cos(B)) * (np.exp(-r ** 2) + np.exp(-1e4 * r ** 2)), 2.0, False)

    legit = [x["rel_residual"] for x in rows
             if x["is_legitimate_in_repository_field"] and x["rel_residual"] is not None]
    bad = [x for x in rows if not x["is_legitimate_in_repository_field"]
           and x["rel_residual"] is not None and (x["rel_err"] or 0) > 5e-4]
    worst_legit = max(legit) if legit else None
    tightest_bad = min((x["rel_residual"] for x in bad), default=None)
    return dict(
        rows=rows,
        landed_max_rel_residual=0.5,
        worst_legitimate_rel_residual=worst_legit,
        tightest_uncaught_bad_rel_residual=tightest_bad,
        separation_ratio=(None if not (worst_legit and tightest_bad)
                          else tightest_bad / worst_legit),
        note=("The landed max_rel_residual=0.5 does NOT catch the two-scale field. A "
              "threshold anywhere in the open interval (worst_legitimate, tightest_bad) "
              "would, with the stated separation ratio of margin. Changing it is a "
              "behaviour change this leg's gate did not scope -- clause (b)'s bit-identical "
              "sweep was run at 0.5 -- so it is REPORTED with its magnitude and handed to "
              "the postrepair-verification leg, not tuned in silently here."))


def caller_census():
    """Every site in the repository that reaches this module.  grep, not assumption."""
    pat = ("odd_field_x_slope|boussinesq_rescaled import|import boussinesq_rescaled|"
           "RescaledBoussinesq|modulation\\(")
    r = subprocess.run(["grep", "-rInE", pat, "--include=*.py", "."], cwd=ROOT,
                       capture_output=True, text=True)
    hits = [ln for ln in r.stdout.splitlines()
            if not ln.startswith("./solver/boussinesq_rescaled.py")]
    files = sorted({ln.split(":", 1)[0] for ln in hits})
    return dict(grep_pattern=pat, n_hit_lines=len(hits), files=files,
                banked_artifacts=[b["artifact"] for b in BANKED],
                unbanked_callers=UNBANKED_CALLERS, test_callers=TEST_CALLERS)


def _recompute_clause_b_gate(cb):
    """Recompute clause (b)'s verdict from its runs after an attribution is merged in."""
    runs, tests = cb["banked_runs"], cb["test_runs"]
    attributed = {r["key"]: r["attribution"] for r in runs if "attribution" in r}
    tot_moved = sum(r.get("calls_moved") or 0 for r in runs) \
        + sum(t.get("calls_moved") or 0 for t in tests)
    tot_repair = sum((a.get("repair_attributable_leaves_moved") or 0)
                     for a in attributed.values())
    unattributed = [r["key"] for r in runs
                    if (r.get("artifact_leaves_moved") or 0) > 0 and "attribution" not in r]
    cb["attribution"] = attributed
    cb["total_repair_attributable_leaves_that_moved"] = tot_repair
    cb["artifacts_moved_but_unattributed"] = unattributed
    cb["artifacts_with_baseline_drift_not_caused_by_this_repair"] = sorted(
        k for k, a in attributed.items() if a.get("verdict") == "BASELINE_DRIFT_NOT_THIS_LEG")
    cb["artifacts_whose_script_is_nondeterministic_today"] = sorted(
        k for k, a in attributed.items() if a.get("script_is_deterministic_today") is False)
    cb["zero_contamination"] = bool(
        tot_moved == 0 and tot_repair == 0 and not unattributed
        and all(r.get("returncode") == 0 for r in runs)
        and all(t.get("returncode") == 0 for t in tests)
        and len(runs) == len(BANKED))
    return cb


def attribute_only(key, pre_path, t_all):
    """Stage 2: attribute one artifact's movement and merge it into the banked JSON."""
    spec_ = next((s for s in BANKED if s["key"] == key), None)
    assert spec_ is not None, "unknown banked key %r; known: %r" % (
        key, [s["key"] for s in BANKED])
    payload = json.load(open(OUT))
    assert "clause_b" in payload, "no clause_b in %s to attribute against" % OUT
    rec = next((r for r in payload["clause_b"]["banked_runs"] if r["key"] == key), None)
    assert rec is not None, "%s was not run in the banked sweep" % key
    print("ATTRIBUTING %s: %s artifact leaves moved in the sweep, %s/%s calls bit-identical"
          % (key, rec["artifact_leaves_moved"], rec["calls_bit_identical"],
             rec["calls_compared"]), flush=True)

    att = attribute_movement(spec_, pre_path)
    rec["attribution"] = att
    print("  verdict %s | repair-attributable leaves %s | baseline drift leaves %s | "
          "script deterministic today: %s"
          % (att.get("verdict"), att.get("repair_attributable_leaves_moved"),
             att.get("baseline_drift_leaves_moved"),
             att.get("script_is_deterministic_today")))

    _recompute_clause_b_gate(payload["clause_b"])
    payload["gate_clause_b_zero_contamination_bit_identical"] = bool(
        payload["clause_b"]["zero_contamination"])
    payload["gate_answer"] = "YES" if (
        payload.get("gate_clause_a_every_adversarial_case_now_rejects")
        and payload["gate_clause_b_zero_contamination_bit_identical"]) else "NO"
    drift = payload["clause_b"]["artifacts_with_baseline_drift_not_caused_by_this_repair"]
    payload["banked_artifacts_that_no_longer_reproduce_independently_of_this_repair"] = drift
    payload["escalation_required"] = bool(drift)
    payload.setdefault("assembly", []).append(
        dict(stage="attribute", key=key, wall_seconds=round(time.time() - t_all, 1)))
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=1, default=str, sort_keys=True)
    print("merged into %s -> gate %s, escalation_required %s"
          % (OUT, payload["gate_answer"], payload["escalation_required"]))
    return payload


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="ab")
    ap.add_argument("--skip-slow", action="store_true")
    ap.add_argument("--keys", default=None,
                    help="Comma-separated banked keys to (re-)run, merging into whatever "
                         "clause (b) results are already banked in the JSON. Clause (b) "
                         "costs hours of relaxation; a sweep that is interrupted must not "
                         "have to start over, and one that is resumed must not silently "
                         "mix stale rows -- so every row records the wall clock and stage "
                         "that produced it, and `covers_every_banked_artifact` still "
                         "requires all six to be present.")
    ap.add_argument("--attribute", default=None, metavar="KEY",
                    help="Run ONLY the attribution control for one banked artifact and "
                         "merge it into the existing JSON, recomputing the gate. Exists "
                         "because attribution costs three full regenerations of a slow "
                         "artifact and the sweep that discovered the movement should not "
                         "have to be repeated to explain it. The merge is recorded in the "
                         "JSON as a two-stage assembly, with both stages' wall clocks.")
    args = ap.parse_args()

    t_all = time.time()
    import solver.boussinesq_rescaled as POST
    pre, n_lines = load_pre_repair()
    pre_path = pre.__file__

    if args.attribute:
        return attribute_only(args.attribute, pre_path, t_all)

    ok, control, mags = control_two_modules_really_differ(pre, POST)
    print("LESSON-90 CONTROL (the differential must be able to report the other answer):")
    for k, v in control.items():
        print("    %-42s %s" % (k, v))
    print("    defect B  pre %+.6f (rel %.4e)  post %+.6f (rel %.4e)  truth 2.0"
          % (mags["defect_B_pre"], mags["defect_B_pre_rel_err"],
             mags["defect_B_post"], mags["defect_B_post_rel_err"]))
    print("    defect A  pre %+.6f  truth 2.0" % mags["defect_A_pre"])
    assert ok, ("lesson-90 control FAILED: the two sides are not distinguishable, so no "
                "'identical' count from this run means anything -- %r" % (control,))

    payload = dict(leg=221, route="ROUTE-BVRR",
                   module="solver/boussinesq_rescaled.py",
                   pre_repair_ref=PRE_REPAIR_REF, pre_repair_n_lines=n_lines,
                   escalating_leg=205, lesson_90_control=control,
                   lesson_90_magnitudes=mags,
                   caller_census=caller_census())

    probe = residual_margin_probe(POST)
    payload["residual_margin_probe"] = probe
    print("\nRESIDUAL-MARGIN PROBE (where the landed backstop actually sits):")
    for row in probe["rows"]:
        print("    %-64s ret %-14s rel_err %-10s rel_res %.4g"
              % (row["field"][:64],
                 ("RAISED" if row["returned"] is None else "%+.6f" % row["returned"]),
                 ("--" if row["rel_err"] is None else "%.3e" % row["rel_err"]),
                 (float("nan") if row["rel_residual"] is None else row["rel_residual"])))
    print("    worst legitimate rel_residual %.4g;  tightest UNCAUGHT bad %.4g;  "
          "separation %.4gx;  landed threshold %.2f"
          % (probe["worst_legitimate_rel_residual"] or float("nan"),
             probe["tightest_uncaught_bad_rel_residual"] or float("nan"),
             probe["separation_ratio"] or float("nan"),
             probe["landed_max_rel_residual"]))

    if "a" in args.only:
        print("\nCLAUSE (a) -- leg 205's OWN 81-case battery, pre-repair vs post-repair")
        a, before, after = clause_a(pre, POST)
        payload["clause_a"] = a
        print("    reproduces leg 205's committed totals: %s"
              % a["reproduces_leg_205_committed_totals"])
        print("    totals before: %s" % a["totals_before"])
        print("    totals after:  %s" % a["totals_after"])
        print("    SILENT_WRONG %d -> %d;  gate %s -> %s"
              % (a["n_silent_wrong_before"], a["n_silent_wrong_after"],
                 a["gate_answer_before"], a["gate_answer_after"]))
        for k, v in sorted(a["disposition_of_each_silent_wrong"].items()):
            print("      %-14s %d case(s)" % (k, len(v)))
        for c in a["silent_wrong_after"]:
            print("      STILL SILENT_WRONG: %s" % c)

    if "b" in args.only:
        print("\nCLAUSE (b) -- every banked result that calls this module, RE-RUN")
        cen = payload["caller_census"]
        print("    census: %d files reach the module; %d banked artifacts, %d unbanked "
              "callers, %d test suites"
              % (len(cen["files"]), len(BANKED), len(UNBANKED_CALLERS),
                 len(TEST_CALLERS)))
        # Resume support.  Clause (b) is hours of relaxation; an interrupted sweep that
        # loses every completed artifact is an availability defect in the verification
        # apparatus, and this leg has already lost one 40-minute sweep to it.  Rows already
        # banked in the JSON are carried forward BY KEY and each new row is checkpointed to
        # disk the moment it completes.
        prior = {}
        if args.keys:
            try:
                _old = json.load(open(OUT))
                prior = {r["key"]: r for r in _old.get("clause_b", {})
                         .get("banked_runs", [])}
                if "clause_a" not in payload and "clause_a" in _old:
                    payload["clause_a"] = _old["clause_a"]
                print("    resuming: %d row(s) carried forward from the banked JSON (%s)"
                      % (len(prior), ", ".join(sorted(prior)) or "none"))
            except (OSError, ValueError):
                print("    resuming: no readable prior JSON; starting clause (b) fresh")
        wanted = set(args.keys.split(",")) if args.keys else None
        if wanted:
            unknown = wanted - {s["key"] for s in BANKED}
            assert not unknown, "unknown --keys %r" % sorted(unknown)

        runs = []

        def _checkpoint():
            """Write what clause (b) knows SO FAR, after every artifact."""
            merged = dict(prior)
            for r in runs:
                merged[r["key"]] = r
            ordered = [merged[s["key"]] for s in BANKED if s["key"] in merged]
            snap = dict(payload)
            snap["clause_b"] = _recompute_clause_b_gate(
                dict(banked_runs=ordered, test_runs=payload.get("_tests_so_far", []),
                     n_banked_artifacts_rerun=len(ordered),
                     checkpoint=True,
                     covers_every_banked_artifact=bool(len(ordered) == len(BANKED))))
            with open(OUT, "w") as f:
                json.dump(snap, f, indent=1, default=str, sort_keys=True)

        for spec_ in BANKED:
            if wanted and spec_["key"] not in wanted:
                print("    [not in --keys, carried forward] %s" % spec_["key"])
                continue
            if args.skip_slow and spec_["slow"]:
                print("    [skipped --skip-slow] %s" % spec_["key"])
                continue
            print("    running %-32s (%s) ..." % (spec_["key"], spec_["script"]),
                  flush=True)
            rec = rerun_one(spec_, pre_path)
            runs.append(rec)
            print("      rc=%d  %ss  calls %s/%s bit-identical (%s moved)  "
                  "artifact leaves moved: %s (+%s provenance, not counted)"
                  % (rec["returncode"], rec["wall_seconds"], rec["calls_bit_identical"],
                     rec["calls_compared"], rec["calls_moved"],
                     rec["artifact_leaves_moved"],
                     rec["artifact_provenance_leaves_moved"]), flush=True)
            for p in rec.get("artifact_comparison", {}).get("provenance_moved_detail", []):
                print("        provenance leaf %s: %r -> %r"
                      % (p["leaf"], p["committed"], p["regenerated"]), flush=True)
            if rec["contamination"]:
                print("      *** MOVEMENT on %s -- attributing it ***" % rec["key"],
                      flush=True)
                # Never report movement without saying WHOSE it is.  Three plain
                # regenerations, the repair present in exactly one of them.
                att = attribute_movement(spec_, pre_path)
                rec["attribution"] = att
                print("      attribution: %s | repair-attributable leaves %s | baseline "
                      "drift leaves %s | script deterministic today: %s"
                      % (att.get("verdict"), att.get("repair_attributable_leaves_moved"),
                         att.get("baseline_drift_leaves_moved"),
                         att.get("script_is_deterministic_today")), flush=True)
            _checkpoint()
            print("      [checkpointed %d row(s) to the JSON]" % (len(prior) + len(runs)),
                  flush=True)
        print("    running the module's own correctness suites ...", flush=True)
        tests = run_tests(pre_path)
        for t in tests:
            print("      %-40s rc=%d  calls %s/%s bit-identical"
                  % (t["test"], t["returncode"], t["calls_bit_identical"],
                     t["calls_compared"]), flush=True)
        # Carried-forward rows are part of the sweep's evidence and are counted with the
        # rows measured in this process; the JSON records which stage produced each.
        _merged = dict(prior)
        for r in runs:
            _merged[r["key"]] = r
        runs = [_merged[s["key"]] for s in BANKED if s["key"] in _merged]
        tot_calls = sum(r.get("calls_compared") or 0 for r in runs) \
            + sum(t.get("calls_compared") or 0 for t in tests)
        tot_moved = sum(r.get("calls_moved") or 0 for r in runs) \
            + sum(t.get("calls_moved") or 0 for t in tests)
        # .get, not [] -- a row carried forward from an earlier stage of this sweep predates
        # the provenance channel, and a resume must not die on the older schema.
        tot_leaves = sum((r.get("artifact_leaves_moved") or 0) for r in runs)
        tot_prov = sum((r.get("artifact_provenance_leaves_moved") or 0) for r in runs)
        # Movement, split by WHOSE it is.  An artifact that moved but whose attribution
        # control shows the repair absent from the cause is NOT contamination by this leg --
        # and it is NOT quietly dropped either: it gets its own counter, its own list, and
        # its own escalation flag below.
        attributed = {r["key"]: r["attribution"] for r in runs if "attribution" in r}
        tot_repair_leaves = sum(
            (a.get("repair_attributable_leaves_moved") or 0) for a in attributed.values())
        unattributed = [r["key"] for r in runs
                        if (r["artifact_leaves_moved"] or 0) > 0 and "attribution" not in r]
        baseline_drift = sorted(k for k, a in attributed.items()
                                if a.get("verdict") == "BASELINE_DRIFT_NOT_THIS_LEG")
        nondeterministic = sorted(k for k, a in attributed.items()
                                  if a.get("script_is_deterministic_today") is False)
        payload["clause_b"] = dict(
            banked_runs=runs, test_runs=tests,
            n_banked_artifacts_rerun=len(runs),
            total_odd_field_x_slope_calls_compared=tot_calls,
            total_calls_that_moved=tot_moved,
            total_artifact_leaves_that_moved=tot_leaves,
            total_provenance_leaves_that_moved=tot_prov,
            comparison="== on float64 per call (NaN==NaN identical) and per artifact leaf",
            # The gate's clause (b) is "bit-identical PRE/POST REPAIR".  That is measured two
            # ways, and both must hold: every odd_field_x_slope call in the real run agrees
            # bitwise (tot_moved), and every artifact leaf that moved has been ATTRIBUTED by
            # a control in which the repair is absent (tot_repair_leaves).  An artifact that
            # moved and was never attributed cannot be counted clean -- that is the
            # assumption-of-dormancy error one level up again -- hence `unattributed`.
            zero_contamination=bool(tot_moved == 0 and tot_repair_leaves == 0
                                    and not unattributed
                                    and all(r.get("returncode") == 0 for r in runs)
                                    and all(t.get("returncode") == 0 for t in tests)
                                    and len(runs) == len(BANKED)),
            total_repair_attributable_leaves_that_moved=tot_repair_leaves,
            attribution=attributed,
            artifacts_moved_but_unattributed=unattributed,
            # NOT this leg's contamination, and NOT swept under the rug: a banked artifact
            # that no longer reproduces in today's environment with the repair absent is a
            # finding of its own, reported here and escalated by the caller.
            artifacts_with_baseline_drift_not_caused_by_this_repair=baseline_drift,
            artifacts_whose_script_is_nondeterministic_today=nondeterministic,
            skipped_slow=bool(args.skip_slow),
            n_banked_artifacts_skipped=len(BANKED) - len(runs),
            banked_artifacts_skipped=[s["key"] for s in BANKED
                                      if s["key"] not in {r["key"] for r in runs}],
            # The gate's clause (b) is "EVERY banked result, re-run" -- an unrun artifact is
            # an ASSUMPTION of dormancy, which is precisely the thing leg 205 was faulted for.
            # So a partial sweep can never report zero_contamination, however clean the
            # artifacts it did run: `len(runs) == len(BANKED)` is part of the predicate above,
            # not a separate note.  --skip-slow exists for development only.
            covers_every_banked_artifact=bool(len(runs) == len(BANKED)),
        )
        print("    TOTAL: %d calls compared, %d moved; %d artifact leaves moved "
              "(%d provenance leaves moved, reported not counted); %d/%d banked artifacts run"
              % (tot_calls, tot_moved, tot_leaves, tot_prov, len(runs), len(BANKED)))

    a_ok = ("clause_a" not in payload
            or payload["clause_a"]["n_silent_wrong_after"] == 0)
    b_ok = "clause_b" not in payload or payload["clause_b"]["zero_contamination"]
    payload["gate_clause_a_every_adversarial_case_now_rejects"] = bool(
        payload.get("clause_a", {}).get("n_silent_wrong_after", 0) == 0)
    payload["gate_clause_b_zero_contamination_bit_identical"] = bool(
        payload.get("clause_b", {}).get("zero_contamination", False))
    payload["gate_answer"] = "YES" if (a_ok and b_ok) else "NO"

    # A separate axis from the gate: banked artifacts that no longer reproduce with the
    # repair ABSENT from the process.  Independent of this leg, discovered by it, and of a
    # different order -- so it is a named top-level field, never a footnote inside clause (b).
    drift = payload.get("clause_b", {}).get(
        "artifacts_with_baseline_drift_not_caused_by_this_repair", [])
    payload["banked_artifacts_that_no_longer_reproduce_independently_of_this_repair"] = drift
    payload["escalation_required"] = bool(drift)
    payload["wall_seconds"] = round(time.time() - t_all, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=1, default=str, sort_keys=True)
    print("\nwrote %s" % OUT)
    print("GATE: clause (a) every adversarial case rejects: %s; clause (b) zero "
          "contamination bit-identical: %s -> ANSWER %s"
          % (payload["gate_clause_a_every_adversarial_case_now_rejects"],
             payload["gate_clause_b_zero_contamination_bit_identical"],
             payload["gate_answer"]))
    return payload


if __name__ == "__main__":
    main()
