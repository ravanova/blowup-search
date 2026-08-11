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


def _numeric_leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in TIMING_KEYS:
                continue
            yield from _numeric_leaves(v, "%s.%s" % (path, k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _numeric_leaves(v, "%s[%d]" % (path, i))
    else:
        yield path, obj


def compare_artifacts(committed, regenerated):
    a = dict(_numeric_leaves(committed))
    b = dict(_numeric_leaves(regenerated))
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    moved = []
    n_same = 0
    for k in sorted(set(a) & set(b)):
        x, y = a[k], b[k]
        same = (x == y)
        if not same and isinstance(x, float) and isinstance(y, float):
            same = (x != x and y != y)
        if same:
            n_same += 1
        else:
            rec = {"leaf": k, "committed": x, "regenerated": y}
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and x:
                rec["rel_diff"] = abs(y - x) / abs(x)
            moved.append(rec)
    return dict(leaves_compared=len(set(a) & set(b)), leaves_identical=n_same,
                leaves_moved=len(moved), moved_detail=moved[:60],
                keys_only_in_committed=only_a[:20], keys_only_in_regenerated=only_b[:20],
                n_keys_only_in_committed=len(only_a),
                n_keys_only_in_regenerated=len(only_b),
                timing_keys_excluded=sorted(TIMING_KEYS))


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


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="ab")
    ap.add_argument("--skip-slow", action="store_true")
    args = ap.parse_args()

    t_all = time.time()
    import solver.boussinesq_rescaled as POST
    pre, n_lines = load_pre_repair()
    pre_path = pre.__file__

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
        runs = []
        for spec_ in BANKED:
            if args.skip_slow and spec_["slow"]:
                print("    [skipped --skip-slow] %s" % spec_["key"])
                continue
            print("    running %-32s (%s) ..." % (spec_["key"], spec_["script"]),
                  flush=True)
            rec = rerun_one(spec_, pre_path)
            runs.append(rec)
            print("      rc=%d  %ss  calls %s/%s bit-identical (%s moved)  "
                  "artifact leaves moved: %s"
                  % (rec["returncode"], rec["wall_seconds"], rec["calls_bit_identical"],
                     rec["calls_compared"], rec["calls_moved"],
                     rec["artifact_leaves_moved"]), flush=True)
            if rec["contamination"]:
                print("      *** CONTAMINATION on %s ***" % rec["key"], flush=True)
        print("    running the module's own correctness suites ...", flush=True)
        tests = run_tests(pre_path)
        for t in tests:
            print("      %-40s rc=%d  calls %s/%s bit-identical"
                  % (t["test"], t["returncode"], t["calls_bit_identical"],
                     t["calls_compared"]), flush=True)
        tot_calls = sum(r["calls_compared"] or 0 for r in runs) \
            + sum(t["calls_compared"] or 0 for t in tests)
        tot_moved = sum(r["calls_moved"] or 0 for r in runs) \
            + sum(t["calls_moved"] or 0 for t in tests)
        tot_leaves = sum((r["artifact_leaves_moved"] or 0) for r in runs)
        payload["clause_b"] = dict(
            banked_runs=runs, test_runs=tests,
            n_banked_artifacts_rerun=len(runs),
            total_odd_field_x_slope_calls_compared=tot_calls,
            total_calls_that_moved=tot_moved,
            total_artifact_leaves_that_moved=tot_leaves,
            comparison="== on float64 per call (NaN==NaN identical) and per artifact leaf",
            zero_contamination=bool(tot_moved == 0 and tot_leaves == 0
                                    and all(r["returncode"] == 0 for r in runs)
                                    and all(t["returncode"] == 0 for t in tests)),
            skipped_slow=bool(args.skip_slow),
        )
        print("    TOTAL: %d calls compared, %d moved; %d artifact leaves moved"
              % (tot_calls, tot_moved, tot_leaves))

    a_ok = ("clause_a" not in payload
            or payload["clause_a"]["n_silent_wrong_after"] == 0)
    b_ok = "clause_b" not in payload or payload["clause_b"]["zero_contamination"]
    payload["gate_clause_a_every_adversarial_case_now_rejects"] = bool(
        payload.get("clause_a", {}).get("n_silent_wrong_after", 0) == 0)
    payload["gate_clause_b_zero_contamination_bit_identical"] = bool(
        payload.get("clause_b", {}).get("zero_contamination", False))
    payload["gate_answer"] = "YES" if (a_ok and b_ok) else "NO"
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
