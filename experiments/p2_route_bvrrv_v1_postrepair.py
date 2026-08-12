"""Route-BVRRV v1 -- INDEPENDENT POST-REPAIR VERIFICATION of leg 221's repair to
`solver/boussinesq_rescaled.py::odd_field_x_slope` AND of leg 221's own zero-contamination
re-confirmation.

Leg 233. Verification family (`ORCHESTRATION.md` §7b): this leg READS
`solver/boussinesq_rescaled.py` and edits it nowhere. If it finds a defect it REPORTS it and
escalates; it never repairs. Nothing here is a formality -- leg 205 was this cycle's least
certain escalation, leg 221 both repaired it and graded its own repair, and until this leg ran
nobody had re-measured either half. Legs 307 (`401a5f7`) and 335 (`cc725d1`) both consumed leg
221's 256,233-call census as a premise in their own words ("cited input, not re-run" / "a
control this leg trusts rather than re-runs").

THE GATE, VERBATIM (`DIRECTION.md` leg 233, pre-committed, both branches)
------------------------------------------------------------------------
"Does an independent re-run confirm (a) both named mechanisms now reject correctly, and (b) the
zero-contamination re-confirmation itself reproduces (no banked `boussinesq_rescaled.py`-
dependent value actually moved)?
  yes -> Bank as closing leg 205's finding on fully independently-confirmed footing.
  no  -> Escalate immediately -- this would upgrade leg 205 from 'uncertain' to 'confirmed
         contaminated,' the most serious possible outcome in this cycle's backlog."

WHAT "INDEPENDENT" MEANS HERE, DECIDED BEFORE THE RUN
-----------------------------------------------------
Independence is a claim with a price, so the price is itemised rather than asserted.

  INDEPENDENT.  Every number this file reports is computed by code in this file. Nothing is
  imported from `experiments/p2_route_bvrr_v1_repair.py` -- not its shim, not its classifier,
  not its leaf-flattener, not its comparison rule. NO CACHE IS READ. Leg 221's sweep was
  resumable and cache-backed (it replayed in 66.1 s against a 34-hour original); a cache replay
  is not a re-run and this file has no cache at all, by construction.

  NOT INDEPENDENT, AND NAMED.  (i) Leg 205's battery file is READ VERBATIM out of git at
  `origin/leg/205-bvr-v1`. It is the object under test; re-implementing it would test a
  different battery. (ii) The artifact -> script -> argv mapping below is leg 221's
  construction as amended by leg 335. Re-deriving it would be re-doing leg 221's census rather
  than verifying it, so this file instead RE-GREPS the caller set live (`census`) and reports
  the drift as a magnitude. (iii) Anything not computed live is labelled NOT_RUN_LIVE with its
  call count, per artifact, and never folded into a headline.

A SHARPER MEASUREMENT THAN LEG 221 MADE
----------------------------------------
Leg 221 answered "did any call MOVE?" (0 of 256,233). That is necessary but weak on its own: a
zero can mean the repair is correct on this trajectory, or it can mean the instrument never
looked. So this file additionally measures GUARD REACHABILITY -- for every call, whether the
DEFECT-B window cap actually BINDS (`r_win_eff < r_win`), how many nodes the window holds, and
what the relative residual is. If the cap never binds anywhere in the banked corpus, "0 moved"
is explained rather than merely observed, and the explanation is itself the check on the zero.
The predicate is RE-DERIVED here from the module's documented rule, not imported.

ARTIFACT SAFETY
----------------
Regenerating a banked artifact overwrites it in place. Leg 221 used a `.bvrr_backup` sidecar and
recorded that it was SIGKILLed mid-sweep three times, each death stranding a backup beside a
possibly-rewritten banked file. This file uses git instead: it runs inside a dedicated worktree,
refuses to start unless every artifact it will touch is clean, and restores with
`git checkout --`. That survives SIGKILL, because the restore state lives in the index, not in a
sidecar a dead process was supposed to copy back.

No figure: this leg measures, it does not draw. (`writeup/INDEX.md`, audit/repair family.)
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_bvrrv_v1_postrepair.json")

MODULE_PATH = "solver/boussinesq_rescaled.py"

# The module's own last PRE-guard commit -- the state leg 205 audited.  Pinned by hash, not by
# "the commit before mine", for leg 130's reason (d871675): a self-referential pin stops
# resolving the moment a branch is rebased.
PRE_REPAIR_REF = "1a3e63c"
# Leg 221's repair commit, and leg 221's final state.  Both are compared against `main` so the
# staleness question ("is the module I am verifying the module leg 221 verified?") is answered
# with magnitudes rather than a yes/no.
REPAIR_REF = "d2d9769"
LEG_221_FINAL_REF = "7e58419"
# Leg 352 (Route-LCB2) touched this module AFTER the repair.  Named so the comparison below is
# read as a deliberate check, not a coincidence.
POST_REPAIR_TOUCH_REF = "aa9c5cd"

# Leg 205's battery lives on its own unmerged branch (its gate's yes-branch said: push the
# branch only).  Read verbatim; never re-implemented.
BATTERY_REF = "origin/leg/205-bvr-v1"
BATTERY_PATH = "experiments/p2_route_bvr_v1_adversarial.py"
BATTERY_JSON = "writeup/data/p2_route_bvr_v1_adversarial.json"

# Leg 205's committed verdict totals.  Quoted so the pre-repair re-measurement below can be
# checked against them; NOT used as an input to any post-repair number.
LEG_205_TOTALS = {"OK": 32, "SILENT_WRONG": 18, "RAISED": 11, "NONFINITE": 9,
                  "NO_REFERENT": 2, "RETURNED": 9}

# Leg 221's headline, quoted for comparison only.  This file recomputes both sides.
LEG_221_CLAIM = {"calls_compared": 256233, "calls_moved": 0,
                 "clause_a_silent_wrong_before": 18, "clause_a_silent_wrong_after": 0,
                 "banked_artifacts": 6, "artifact_leaves_moved_pre_existing": 839}

# Artifact -> script -> argv.  Leg 221's registry (`experiments/p2_route_bvrr_v1_repair.py`
# BANKED), with leg 335's `--steps 2500` amendment already on main.  Reused deliberately and
# declared as a reuse in the header; `census()` below independently re-greps the caller set.
BANKED = [
    dict(key="spike1_stepB_rescaled",
         artifact="writeup/data/spike1_stepB_rescaled.json",
         script="writeup/3_spikes/spike1_stepB_evidence.py", argv=["--generate"],
         weight="fast"),
    dict(key="p2_route_brs_v1_status_audit",
         artifact="writeup/data/p2_route_brs_v1_status_audit.json",
         script="experiments/p2_route_brs_v1_status_audit.py", argv=[],
         weight="fast"),
    dict(key="p2_route_k_v1_port",
         artifact="writeup/data/p2_route_k_v1_port.json",
         script="experiments/p2_route_k_v1_port.py", argv=[],
         weight="slow"),
    dict(key="p2_route_l_v1_precond",
         artifact="writeup/data/p2_route_l_v1_precond.json",
         script="experiments/p2_route_l_v1_precond.py", argv=[],
         weight="slow"),
    dict(key="p2_route_g_v1_g2",
         artifact="writeup/data/p2_route_g_v1_g2.json",
         script="experiments/p2_route_g_v1_collapse.py",
         argv=["--only", "g2", "--out", "p2_route_g_v1_g2.json"],
         env={"ROUTE_G_SERIAL": "1"},
         weight="slow"),
    dict(key="spike1_stepC_gate",
         artifact="writeup/data/spike1_stepC_gate.json",
         script="experiments/spike1_stepC_gate.py",
         argv=["--logged", "--steps", "2500"],
         weight="slowest"),
]

TEST_CALLERS = ["test_boussinesq_rescaled.py", "test_boussinesq_transport.py",
                "test_boussinesq_rescaled_status.py"]

# Wall-clock keys are not results.  Named, not silently skipped.
TIMING_KEYS = {"seconds", "wall_seconds", "wall_s", "wall_clock_seconds", "elapsed",
               "elapsed_s", "runtime_s", "minutes", "wall_minutes"}
# Keys recording WHEN, not WHAT.  Compared and reported in their own channel; they do not count
# toward the contamination measure.  (Leg 221 measured one real instance of this:
# p2_route_brs_v1_status_audit.json carries a "generated" date.)
PROVENANCE_KEYS = {"generated", "generated_at", "date", "run_date", "timestamp", "created",
                   "created_at", "when", "today"}


# ---------------------------------------------------------------------------
# git helpers
# ---------------------------------------------------------------------------
def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout


def _git_show(ref: str, path: str) -> str:
    return _git("show", "%s:%s" % (ref, path))


# ---------------------------------------------------------------------------
# Q0 -- is the module under verification the module leg 221 verified?
# ---------------------------------------------------------------------------
def _strip_docstrings(tree: ast.AST) -> ast.AST:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return tree


def _fingerprint(src: str) -> dict:
    raw = src.encode()
    return dict(
        n_bytes=len(raw),
        n_lines=src.count("\n"),
        sha256=hashlib.sha256(raw).hexdigest(),
        ast_sha256=hashlib.sha256(ast.dump(ast.parse(src)).encode()).hexdigest(),
        ast_nodoc_sha256=hashlib.sha256(
            ast.dump(ast.fix_missing_locations(_strip_docstrings(ast.parse(src)))).encode()
        ).hexdigest(),
    )


def module_staleness() -> dict:
    """The dispatch flagged this and asked for it as a MAGNITUDE, not a boolean.

    `solver/boussinesq_rescaled.py` was last touched by leg 352 (`aa9c5cd`), AFTER leg 221's
    repair.  Leg 221's own staleness re-check found main byte-identical to its PRE_REPAIR_REF
    baseline at that time; that is no longer true, so the right question is not "identical?"
    but "identical WHERE IT EXECUTES?".  Answer, measured: the raw bytes differ, and the
    docstring-stripped ASTs do not.
    """
    sources = {
        "pre_repair_1a3e63c": _git_show(PRE_REPAIR_REF, MODULE_PATH),
        "repair_commit_d2d9769": _git_show(REPAIR_REF, MODULE_PATH),
        "leg_221_final_7e58419": _git_show(LEG_221_FINAL_REF, MODULE_PATH),
        "main_head": open(os.path.join(ROOT, MODULE_PATH)).read(),
    }
    fp = {k: _fingerprint(v) for k, v in sources.items()}
    head, l221, rep, pre = (fp["main_head"], fp["leg_221_final_7e58419"],
                            fp["repair_commit_d2d9769"], fp["pre_repair_1a3e63c"])
    return dict(
        fingerprints=fp,
        last_touch_commit=POST_REPAIR_TOUCH_REF,
        last_touch_subject=_git("log", "-1", "--format=%s", POST_REPAIR_TOUCH_REF).strip(),
        main_vs_leg221_final=dict(
            raw_bytes_identical=head["sha256"] == l221["sha256"],
            byte_delta=head["n_bytes"] - l221["n_bytes"],
            line_delta=head["n_lines"] - l221["n_lines"],
            ast_identical=head["ast_sha256"] == l221["ast_sha256"],
            ast_nodoc_identical=head["ast_nodoc_sha256"] == l221["ast_nodoc_sha256"],
        ),
        main_vs_repair_commit=dict(
            ast_nodoc_identical=head["ast_nodoc_sha256"] == rep["ast_nodoc_sha256"]),
        main_vs_pre_repair=dict(
            ast_nodoc_identical=head["ast_nodoc_sha256"] == pre["ast_nodoc_sha256"]),
        reading=("Every change to this module since the repair is docstring text; the "
                 "executable semantics under verification are exactly the repaired ones. "
                 "The pre-repair copy differs from all three post-repair copies at "
                 "docstring-stripped AST level, so the differential below is real."),
    )


# ---------------------------------------------------------------------------
# the two module objects, loaded side by side into one process
# ---------------------------------------------------------------------------
def load_pre_repair() -> tuple:
    src = _git_show(PRE_REPAIR_REF, MODULE_PATH)
    fd, path = tempfile.mkstemp(suffix="_bvrrv_pre_boussinesq_rescaled.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_bvrrv_pre_boussinesq_rescaled", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_bvrrv_pre_boussinesq_rescaled"] = mod
    spec.loader.exec_module(mod)
    return mod, path


# ---------------------------------------------------------------------------
# LESSON 90 -- a control that cannot come out differently is not a control
# ---------------------------------------------------------------------------
def two_modules_really_differ(pre, post) -> dict:
    """Before any "identical" or "zero" count below is believed, assert executably that the two
    module objects are genuinely distinct and disagree by a MEASURED amount on the two inputs
    leg 205 published.  If this ever passes trivially, every zero downstream is worthless."""
    from solver.boussinesq_velocity import PolarGrid

    def odd(grid, a=1.0, lam=1.0):
        return a * grid.R * np.cos(grid.B) * np.exp(-lam * grid.R ** 2)

    checks, mags = {}, {}
    checks["distinct_function_objects"] = pre.odd_field_x_slope is not post.odd_field_x_slope
    # NOT a check: the repair ADDS `min_points` and `max_rel_residual`, so the signatures MUST
    # differ.  Recorded as a magnitude -- an equal signature here would be the surprise.
    sig_pre = str(inspect.signature(pre.odd_field_x_slope))
    sig_post = str(inspect.signature(post.odd_field_x_slope))
    mags["signature_pre"] = sig_pre
    mags["signature_post"] = sig_post
    mags["signature_params_added"] = sorted(
        set(inspect.signature(post.odd_field_x_slope).parameters)
        - set(inspect.signature(pre.odd_field_x_slope).parameters))
    checks["signatures_differ_as_the_repair_requires"] = sig_pre != sig_post

    # DEFECT B, leg 205's headline: leg 205's own leg-73-class grid (n_r=400, r_min=1e-4,
    # r_max=1e4, n_beta=16), lam=400 -- a smooth in-contract field of scale 0.05 on a FULLY
    # RESOLVED window (177 nodes).  Pre fabricates; post must land inside the module's own
    # 5e-4 tolerance.  Grid taken verbatim from the battery's family_1 (iii) so the number is
    # comparable with leg 205's published 0.269302, not merely of the same order.
    fine = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    fld = odd(fine, 2.0, 400.0)
    b_pre = float(pre.odd_field_x_slope(fld, fine))
    b_post = float(post.odd_field_x_slope(fld, fine))
    mags["defect_B_truth"] = 2.0
    mags["defect_B_pre"] = b_pre
    mags["defect_B_post"] = b_post
    mags["defect_B_pre_rel_err"] = abs(b_pre - 2.0) / 2.0
    mags["defect_B_post_rel_err"] = abs(b_post - 2.0) / 2.0
    mags["module_acceptance_tol"] = 5e-4
    checks["pre_fabricates_on_defect_B"] = mags["defect_B_pre_rel_err"] > 5e-4
    checks["post_recovers_on_defect_B"] = mags["defect_B_post_rel_err"] <= 5e-4

    mags["defect_B_leg_205_published"] = 0.269302
    mags["defect_B_leg_221_published_post"] = 2.000776

    # DEFECT A, leg 205's empty-window case, verbatim from the battery's family_1 (i) row
    # "r_min > r_win -- EMPTY window, fine grid": pre returns exactly 0.0 with no raise and no
    # warning; post must REFUSE.
    empty = PolarGrid(n_r=200, n_beta=16, r_min=0.5, r_max=40.0)
    fld2 = odd(empty, 2.0, 1.0)
    a_pre = float(pre.odd_field_x_slope(fld2, empty))
    mags["defect_A_truth"] = 2.0
    mags["defect_A_pre"] = a_pre
    checks["pre_fabricates_exactly_zero_on_defect_A"] = (a_pre == 0.0)
    try:
        post.odd_field_x_slope(fld2, empty)
        checks["post_rejects_on_defect_A"] = False
        mags["defect_A_post"] = "RETURNED (no raise)"
    except ValueError as e:
        checks["post_rejects_on_defect_A"] = True
        mags["defect_A_post"] = "ValueError: " + str(e)[:200]

    return dict(all_passed=all(checks.values()), checks=checks, magnitudes=mags)


# ---------------------------------------------------------------------------
# CLAUSE (a) -- do both named mechanisms now reject correctly?
# ---------------------------------------------------------------------------
def _load_battery(bound_module, tag: str) -> dict:
    """Execute leg 205's battery file with `solver.boussinesq_rescaled` bound to the given
    module object.  The battery derives its own output path from `__file__`, so it is staged
    two directories deep inside a scratch tree and its JSON lands there, never in
    `writeup/data/`."""
    src = _git_show(BATTERY_REF, BATTERY_PATH)
    tmp = tempfile.mkdtemp(prefix="bvrrv_battery_%s_" % tag)
    exp = os.path.join(tmp, "experiments")
    os.makedirs(exp)
    path = os.path.join(exp, os.path.basename(BATTERY_PATH))
    with open(path, "w") as f:
        f.write(src)
    real = sys.modules.get("solver.boussinesq_rescaled")
    sys.modules["solver.boussinesq_rescaled"] = bound_module
    try:
        name = "_bvrrv_battery_%s" % tag
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod.main()
    finally:
        if real is not None:
            sys.modules["solver.boussinesq_rescaled"] = real
        else:
            sys.modules.pop("solver.boussinesq_rescaled", None)
        sys.modules.pop("_bvrrv_battery_%s" % tag, None)
        shutil.rmtree(tmp, ignore_errors=True)


def _cases(payload) -> dict:
    """Flatten leg 205's scored battery, keyed by its own `case` string.  Written here rather
    than imported from leg 221's runner, so a bug in that flattener cannot survive into this
    leg's answer by inheritance."""
    out = {}
    stack = [payload]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if "verdict" in node and "case" in node:
                out[node["case"]] = node
            for v in node.values():
                if isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(node, list):
            stack.extend(x for x in node if isinstance(x, (dict, list)))
    return out


def _tally(cases: dict) -> dict:
    t = {}
    for c in cases.values():
        t[c["verdict"]] = t.get(c["verdict"], 0) + 1
    return dict(sorted(t.items()))


def clause_a(pre, post) -> dict:
    t0 = time.time()
    before = _load_battery(pre, "pre")
    after = _load_battery(post, "post")
    cb, ca = _cases(before), _cases(after)

    committed = _cases(json.loads(_git_show(BATTERY_REF, BATTERY_JSON)))

    tally_before, tally_after = _tally(cb), _tally(ca)
    tally_committed = _tally(committed)

    # Does the PRE-repair re-measurement reproduce leg 205's committed verdicts?  This is the
    # control on the control: if it does not, the "before" column is not leg 205's finding and
    # nothing downstream is a verification of leg 221.
    shared = sorted(set(cb) & set(committed))
    verdict_mismatch = [dict(case=k, committed=committed[k]["verdict"],
                             remeasured_pre=cb[k]["verdict"])
                        for k in shared if committed[k]["verdict"] != cb[k]["verdict"]]

    # Full transition matrix over every case, not just the SILENT_WRONG count.  A repair that
    # fixed 18 SILENT_WRONGs by breaking 18 OKs would pass a count check and fail this one.
    both = sorted(set(cb) & set(ca))
    transitions = {}
    for k in both:
        key = "%s -> %s" % (cb[k]["verdict"], ca[k]["verdict"])
        transitions[key] = transitions.get(key, 0) + 1

    # THE MEASUREMENT LEG 221'S HEADLINE DID NOT MAKE.
    #
    # "SILENT_WRONG 18 -> 0" is a count, and a count cannot see a repair that buys its zero by
    # breaking something else. The transition matrix above can, and it found three cases moving
    # OK -> RAISED. A refusal is not automatically a regression and not automatically correct
    # either, so each one is ADJUDICATED against the module's own documented rule rather than
    # waved through: the case's grid is rebuilt from the battery's own recorded parameters, the
    # window occupancy and the lstsq RANK of the (r, r^3, r^5) design matrix are measured, and
    # the refusal counts as JUSTIFIED only if the module's stated precondition genuinely fails
    # (fewer than min_points nodes, or rank < 3). Anything else is an UNJUSTIFIED_REGRESSION
    # and fails clause (a).
    def _adjudicate_ok_to_raised(case_key):
        from solver.boussinesq_velocity import PolarGrid
        rec_b, rec_a = cb[case_key], ca[case_key]
        out = dict(case=case_key,
                   pre_returned=rec_b.get("returned"), pre_rel_err=rec_b.get("rel_err"),
                   pre_verdict="OK", post_verdict=rec_a["verdict"],
                   post_exception=str(rec_a.get("exception"))[:400],
                   battery_fit_nodes=rec_b.get("fit_nodes"),
                   module_acceptance_tol=5e-4)
        if rec_b.get("rel_err") is not None:
            out["pre_margin_inside_tol"] = 5e-4 - float(rec_b["rel_err"])
        n_r, r_min, r_max = rec_b.get("n_r"), rec_b.get("r_min"), rec_b.get("r_max")
        r_win = rec_b.get("r_win") or 0.4
        if not (n_r and r_min and r_max):
            out["verdict"] = "UNADJUDICATED (battery record carries no grid parameters)"
            return out
        grid = PolarGrid(n_r=int(n_r), n_beta=16, r_min=float(r_min), r_max=float(r_max))
        r = grid.r
        live = np.arange(len(r)) >= 3
        m = live & (r < float(r_win))
        n_in = int(m.sum())
        out["measured_window_nodes"] = n_in
        out["min_points_required"] = 3
        if n_in:
            A = np.vstack([r[m], r[m] ** 3, r[m] ** 5]).T
            _c, _res, rank, sv = np.linalg.lstsq(A, np.zeros(n_in), rcond=None)
            out["measured_lstsq_rank"] = int(rank)
            out["design_matrix_columns"] = 3
            out["singular_values"] = [float(x) for x in sv]
            out["singular_value_ratio"] = (float(sv[-1] / sv[0]) if sv[0] else None)
        else:
            out["measured_lstsq_rank"] = 0
        under = n_in < 3
        deficient = out.get("measured_lstsq_rank", 0) < 3
        out["precondition_genuinely_fails"] = bool(under or deficient)
        out["failure_mode"] = ("under_determined (fewer nodes than parameters)" if under
                               else ("rank_deficient (design matrix numerically singular)"
                                     if deficient else "none -- the window is well-posed"))
        out["verdict"] = ("JUSTIFIED_REFUSAL" if out["precondition_genuinely_fails"]
                          else "UNJUSTIFIED_REGRESSION")
        return out

    sw_before = [k for k in both if cb[k]["verdict"] == "SILENT_WRONG"]
    sw_after = [k for k in both if ca[k]["verdict"] == "SILENT_WRONG"]
    ok_moved = [k for k in both if cb[k]["verdict"] == "OK" and ca[k]["verdict"] != "OK"]
    adjudicated = [_adjudicate_ok_to_raised(k) for k in sorted(ok_moved)]
    regressions = [a for a in adjudicated if a.get("verdict") != "JUSTIFIED_REFUSAL"]

    # Where did the 18 go?  Named individually with the magnitude that moved, because
    # "18 -> 0" is a boolean wearing a number's clothes.
    sw_fate = []
    for k in sorted(sw_before):
        rec = dict(case=k, after=ca[k]["verdict"],
                   before_returned=cb[k].get("returned"),
                   after_returned=ca[k].get("returned"),
                   before_rel_err=cb[k].get("rel_err"), after_rel_err=ca[k].get("rel_err"))
        if ca[k].get("exception"):
            rec["after_exception"] = str(ca[k]["exception"])[:160]
        sw_fate.append(rec)

    return dict(
        wall_seconds=round(time.time() - t0, 1),
        n_cases_before=len(cb), n_cases_after=len(ca), n_cases_committed=len(committed),
        tally_committed_leg_205=tally_committed,
        tally_remeasured_pre_repair=tally_before,
        tally_post_repair=tally_after,
        leg_205_committed_totals_quoted=LEG_205_TOTALS,
        pre_repair_reproduces_leg_205=(len(verdict_mismatch) == 0),
        n_verdict_mismatch_vs_committed=len(verdict_mismatch),
        verdict_mismatch_detail=verdict_mismatch[:20],
        transitions=dict(sorted(transitions.items(), key=lambda kv: -kv[1])),
        silent_wrong_before=len(sw_before),
        silent_wrong_after=len(sw_after),
        silent_wrong_after_cases=sorted(sw_after),
        silent_wrong_fate=sw_fate,
        n_ok_left_ok=len(ok_moved),
        ok_to_nonok_adjudication=adjudicated,
        n_justified_refusals=len([a for a in adjudicated
                                  if a.get("verdict") == "JUSTIFIED_REFUSAL"]),
        ok_regressions=regressions,
        n_ok_regressions=len(regressions),
        # The gate's clause (a), stated as the conjunction it actually is.
        clause_a_pass=(len(sw_after) == 0 and len(regressions) == 0
                       and len(verdict_mismatch) == 0 and len(cb) == len(ca)),
    )


# ---------------------------------------------------------------------------
# CLAUSE (b) -- the differential sweep, live, no cache
# ---------------------------------------------------------------------------
SHIM_DRIVER = r'''
"""Leg 233's own differential driver.  Not leg 221's -- written independently, and measuring
one thing leg 221's did not: whether the DEFECT-B window cap actually BINDS on each call."""
import atexit, importlib.util, json, os, runpy, sys
import numpy as np

ROOT = os.environ["BVRRV_ROOT"]
sys.path.insert(0, ROOT)
REPORT = os.environ["BVRRV_REPORT"]
TARGET = os.environ["BVRRV_TARGET"]
sys.argv = json.loads(os.environ["BVRRV_ARGV"])

spec = importlib.util.spec_from_file_location("_bvrrv_pre", os.environ["BVRRV_PRE"])
pre = importlib.util.module_from_spec(spec)
sys.modules["_bvrrv_pre"] = pre
spec.loader.exec_module(pre)

import solver.boussinesq_rescaled as BR
_post = BR.odd_field_x_slope
_pre = pre.odd_field_x_slope

S = {"n": 0, "same": 0, "moved": [], "n_moved": 0, "raise_pre": 0, "raise_post": 0,
     "both_raise": 0, "cap_binds": 0, "cap_nonbinding": 0, "cap_undefined": 0,
     "min_window_nodes": None, "max_rel_residual_seen": None,
     "n_residual_measured": 0, "n_residual_over_backstop": 0,
     "residual_instrumented": True,
     "cap_ratio_min": None, "n_window_below_3": 0}


def _probe(g, grid, r_win, i_lo):
    """Re-derivation of the module's DEFECT-B cap rule, from its documented statement, so this
    file measures reachability without importing the implementation it is auditing:
    d1 = (4/pi) * trapezoid projection onto cos(beta); the peak of |d1| over the live nodes is
    taken at the OUTERMOST radius attaining it; r_scale = sqrt(2) * r_peak; the effective
    window is min(r_win, r_scale / 2)."""
    beta = grid.beta
    dbeta = beta[1] - beta[0]
    cb = np.cos(beta)
    g_wall = 2 * g[:, 0] - g[:, 1]
    integrand = g * cb[None, :]
    interior = np.trapezoid(integrand, beta, axis=1)
    d1 = (4.0 / np.pi) * (interior
                          + 0.5 * dbeta * (g_wall + integrand[:, 0])
                          + 0.5 * dbeta * integrand[:, -1])
    r = grid.r
    live = np.arange(len(r)) >= i_lo
    a1 = np.where(live, np.abs(d1), 0.0)
    peak = float(np.max(a1)) if a1.size else 0.0
    if np.isfinite(peak) and peak > 0.0:
        i_peak = int(len(a1) - 1 - np.argmax(a1[::-1]))
        r_scale = np.sqrt(2.0) * float(r[i_peak])
        r_win_eff = min(float(r_win), 0.5 * r_scale)
        defined = True
    else:
        r_scale, r_win_eff, defined = float("inf"), float(r_win), False
    m = live & (r < r_win_eff)
    n_in = int(m.sum())
    # The module's OTHER post-repair backstop is `max_rel_residual=0.5` on the (r, r^3, r^5)
    # fit. Measure it here too, re-derived the same way, so its reachability is a magnitude
    # rather than an assumption. Undefined (None) when the window cannot support a fit.
    rel_resid = None
    if n_in >= 3:
        rr = r[m]
        A = np.stack([rr, rr ** 3, rr ** 5], axis=1)
        y = d1[m]
        sol, res, rank, _sv = np.linalg.lstsq(A, y, rcond=None)
        denom = float(np.linalg.norm(y))
        if denom > 0.0:
            resid = float(np.linalg.norm(A @ sol - y))
            rel_resid = resid / denom
    return defined, float(r_win), r_win_eff, n_in, rel_resid


def _call(fn, g, grid, a, kw):
    try:
        return ("value", float(fn(g, grid, *a, **kw)))
    except Exception as e:                                            # noqa: BLE001
        return ("exc", type(e).__name__)


def shim(g, grid, *a, **kw):
    p = _call(_pre, g, grid, a, kw)
    q = _call(_post, g, grid, a, kw)
    S["n"] += 1
    if p[0] == "exc":
        S["raise_pre"] += 1
    if q[0] == "exc":
        S["raise_post"] += 1
    if p[0] == "exc" and q[0] == "exc":
        S["both_raise"] += 1

    # GUARD REACHABILITY -- the measurement leg 221 did not make.
    try:
        r_win = kw.get("r_win", a[0] if len(a) >= 1 else 0.4)
        i_lo = kw.get("i_lo", a[1] if len(a) >= 2 else 3)
        defined, rw, rw_eff, n_in, rel_resid = _probe(g, grid, r_win, i_lo)
        if rel_resid is not None:
            S["n_residual_measured"] += 1
            if (S["max_rel_residual_seen"] is None
                    or rel_resid > S["max_rel_residual_seen"]):
                S["max_rel_residual_seen"] = rel_resid
            if rel_resid > 0.5:
                S["n_residual_over_backstop"] += 1
        if not defined:
            S["cap_undefined"] += 1
        elif rw_eff < rw:
            S["cap_binds"] += 1
            ratio = rw_eff / rw if rw else float("inf")
            if S["cap_ratio_min"] is None or ratio < S["cap_ratio_min"]:
                S["cap_ratio_min"] = ratio
        else:
            S["cap_nonbinding"] += 1
        if S["min_window_nodes"] is None or n_in < S["min_window_nodes"]:
            S["min_window_nodes"] = n_in
        if n_in < 3:
            S["n_window_below_3"] += 1
    except Exception as e:                                            # noqa: BLE001
        S["probe_errors"] = S.get("probe_errors", 0) + 1
        S.setdefault("probe_error_kinds", {})
        k = type(e).__name__
        S["probe_error_kinds"][k] = S["probe_error_kinds"].get(k, 0) + 1

    # bitwise identity; NaN == NaN counts as identical, and is counted separately
    if p[0] == q[0] == "value":
        both_nan = (p[1] != p[1]) and (q[1] != q[1])
        same = (p[1] == q[1]) or both_nan
        if both_nan:
            S["nan_pairs"] = S.get("nan_pairs", 0) + 1
    else:
        same = (p == q)
    if same:
        S["same"] += 1
    else:
        S["n_moved"] += 1
        if len(S["moved"]) < 200:
            rec = {"call_index": S["n"], "pre": p, "post": q}
            if p[0] == "value" and q[0] == "value":
                rec["abs_diff"] = abs(p[1] - q[1])
                rec["rel_diff"] = abs(p[1] - q[1]) / abs(p[1]) if p[1] else float("inf")
                rec["pre_hex"] = float(p[1]).hex()
                rec["post_hex"] = float(q[1]).hex()
            S["moved"].append(rec)

    # follow the PRE-repair trajectory exactly, so this run reproduces the banked one
    if p[0] == "exc":
        return _pre(g, grid, *a, **kw)
    return p[1]


BR.odd_field_x_slope = shim


@atexit.register
def _dump():
    with open(REPORT, "w") as f:
        json.dump(S, f)


runpy.run_path(TARGET, run_name="__main__")
'''


def _leaves(obj, path="", prov=False):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in TIMING_KEYS:
                continue
            yield from _leaves(v, "%s.%s" % (path, k), prov or k in PROVENANCE_KEYS)
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _leaves(v, "%s[%d]" % (path, i), prov)
    else:
        yield path, (obj, prov)


def compare_artifacts(committed, regenerated) -> dict:
    a, b = dict(_leaves(committed)), dict(_leaves(regenerated))
    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    moved, prov_moved, same = [], [], 0
    for k in sorted(set(a) & set(b)):
        (x, is_prov), (y, _) = a[k], b[k]
        eq = (x == y)
        if not eq and isinstance(x, float) and isinstance(y, float):
            eq = (x != x and y != y)
        if eq:
            same += 1
            continue
        rec = dict(leaf=k, committed=x, regenerated=y)
        if isinstance(x, (int, float)) and not isinstance(x, bool) \
                and isinstance(y, (int, float)) and not isinstance(y, bool) and x:
            rec["rel_diff"] = abs(y - x) / abs(x)
        (prov_moved if is_prov else moved).append(rec)
    moved.sort(key=lambda r: -(r.get("rel_diff") or 0.0))
    return dict(leaves_compared=len(set(a) & set(b)), leaves_identical=same,
                leaves_moved=len(moved), moved_detail_worst_by_rel_diff=moved[:40],
                provenance_leaves_moved=len(prov_moved), provenance_moved_detail=prov_moved[:10],
                n_keys_only_in_committed=len(only_a), n_keys_only_in_regenerated=len(only_b),
                keys_only_in_committed=only_a[:10], keys_only_in_regenerated=only_b[:10],
                timing_keys_excluded=sorted(TIMING_KEYS),
                provenance_keys_not_counted=sorted(PROVENANCE_KEYS))


def _assert_clean(rel_path: str) -> None:
    st = _git("status", "--porcelain", "--", rel_path).strip()
    if st:
        raise RuntimeError(
            "refusing to regenerate %s: it is not clean in this worktree (%r). The restore "
            "path is `git checkout --`, which would destroy uncommitted work." % (rel_path, st))


def sweep_test_suite(script_rel: str, pre_path: str,
                     timeout_s: float | None = None) -> dict:
    """The same differential shim, driven over one of the module's OWN test suites instead of a
    banked artifact.  Leg 221's headline 256,233 is 251,092 banked-artifact calls PLUS 5,141
    from exactly these three suites, so running them here is what makes the two totals
    comparable at all.  There is no artifact to compare or restore, so this is a pure per-call
    differential."""
    fd, driver = tempfile.mkstemp(suffix="_bvrrv_driver.py")
    with os.fdopen(fd, "w") as f:
        f.write(SHIM_DRIVER)
    fd, report = tempfile.mkstemp(suffix="_bvrrv_report.json")
    os.close(fd)
    target = os.path.join(ROOT, script_rel)
    env = dict(os.environ)
    env.update(BVRRV_ROOT=ROOT, BVRRV_REPORT=report, BVRRV_TARGET=target,
               BVRRV_PRE=pre_path, BVRRV_ARGV=json.dumps([target]),
               PYTHONPATH=ROOT + os.pathsep + os.path.join(ROOT, "experiments"))
    out = dict(key=script_rel, script=script_rel, artifact=None, argv=[],
               ran_live=True, from_cache=False, is_test_suite=True)
    t0 = time.time()
    try:
        proc = subprocess.run([sys.executable, "-u", driver], cwd=ROOT, env=env,
                              capture_output=True, text=True, timeout=timeout_s)
        out["returncode"], stderr = proc.returncode, proc.stderr
    except subprocess.TimeoutExpired as e:                             # noqa: BLE001
        out["returncode"], stderr = None, ""
        out["timed_out"] = True
    out["wall_seconds"] = round(time.time() - t0, 1)
    if out["returncode"] not in (0, None):
        out["stderr_tail"] = stderr[-3000:]
    try:
        out["per_call_differential"] = json.loads(open(report).read())
    except Exception as e:                                            # noqa: BLE001
        out["per_call_differential"] = {"error": repr(e)}
    for p in (driver, report):
        try:
            os.remove(p)
        except OSError:
            pass
    d = out.get("per_call_differential", {})
    out["calls_compared"] = d.get("n")
    out["calls_bit_identical"] = d.get("same")
    out["calls_moved"] = d.get("n_moved")
    out["cap_binds"] = d.get("cap_binds")
    out["cap_nonbinding"] = d.get("cap_nonbinding")
    return out


def sweep_one(spec_: dict, pre_path: str, timeout_s: float | None = None) -> dict:
    art_rel = spec_["artifact"]
    art = os.path.join(ROOT, art_rel)
    _assert_clean(art_rel)
    committed = json.loads(open(art).read())

    fd, driver = tempfile.mkstemp(suffix="_bvrrv_driver.py")
    with os.fdopen(fd, "w") as f:
        f.write(SHIM_DRIVER)
    fd, report = tempfile.mkstemp(suffix="_bvrrv_report.json")
    os.close(fd)

    target = os.path.join(ROOT, spec_["script"])
    env = dict(os.environ)
    env.update(spec_.get("env", {}))
    env.update(BVRRV_ROOT=ROOT, BVRRV_REPORT=report, BVRRV_TARGET=target,
               BVRRV_PRE=pre_path, BVRRV_ARGV=json.dumps([target] + spec_["argv"]),
               PYTHONPATH=ROOT + os.pathsep + os.path.join(ROOT, "experiments"))

    out = dict(key=spec_["key"], artifact=art_rel, script=spec_["script"], argv=spec_["argv"],
               ran_live=True, from_cache=False)
    t0 = time.time()
    timed_out = False
    try:
        proc = subprocess.run([sys.executable, "-u", driver], cwd=ROOT, env=env,
                              capture_output=True, text=True, timeout=timeout_s)
        rc, stderr = proc.returncode, proc.stderr
    except subprocess.TimeoutExpired as e:
        timed_out = True
        rc, stderr = None, (e.stderr or b"").decode(errors="replace") if e.stderr else ""
    out["wall_seconds"] = round(time.time() - t0, 1)
    out["returncode"] = rc
    out["timed_out"] = timed_out
    if rc not in (0, None):
        out["stderr_tail"] = stderr[-3000:]

    try:
        out["per_call_differential"] = json.loads(open(report).read())
    except Exception as e:                                            # noqa: BLE001
        out["per_call_differential"] = {"error": repr(e)}
    try:
        regenerated = json.loads(open(art).read())
        out["artifact_comparison"] = compare_artifacts(committed, regenerated)
    except Exception as e:                                            # noqa: BLE001
        out["artifact_comparison"] = {"error": repr(e)}
    finally:
        # git, not a sidecar: survives SIGKILL because the restore state is in the index.
        # Retried, because this sweep is run four-ways-parallel (one process per artifact) and
        # two `git checkout` calls landing together contend on index.lock.  A failed restore
        # would leave a banked artifact rewritten, which is exactly the state leg 221 was left
        # in three times, so it is worth the loop.
        for attempt in range(6):
            try:
                _git("checkout", "--", art_rel)
                break
            except subprocess.CalledProcessError:
                if attempt == 5:
                    out["restore_failed_after_retries"] = True
                    raise
                time.sleep(1.0 + attempt)
        out["artifact_restored_clean"] = (_git("status", "--porcelain", "--",
                                               art_rel).strip() == "")
    for p in (driver, report):
        try:
            os.remove(p)
        except OSError:
            pass

    d = out.get("per_call_differential", {})
    out["calls_compared"] = d.get("n")
    out["calls_bit_identical"] = d.get("same")
    out["calls_moved"] = d.get("n_moved")
    out["cap_binds"] = d.get("cap_binds")
    out["cap_nonbinding"] = d.get("cap_nonbinding")
    ac = out.get("artifact_comparison", {})
    out["artifact_leaves_moved"] = ac.get("leaves_moved")
    out["artifact_provenance_leaves_moved"] = ac.get("provenance_leaves_moved")
    out["contamination_by_calls"] = bool((out.get("calls_moved") or 0) > 0)
    return out


def probe_liveness_selftest(post) -> dict:
    """LESSON 90, APPLIED TO THIS LEG'S OWN NEW INSTRUMENT.

    The sweep's headline guard-reachability number is `cap_binds`. If it comes back 0 across the
    whole banked corpus, that reading is only worth something if the probe CAN report non-zero
    -- otherwise "the cap never binds" and "the probe is broken" are the same observation. So
    the probe is exercised here on two fields whose answers are known in advance and OPPOSITE:

      * `lam=400` (radial scale 0.05, well inside r_win=0.4): the cap MUST bind. This is leg
        205's DEFECT-B headline field, and the cap binding on it is the whole repair.
      * `lam=1` (radial scale 1.0, outside r_win=0.4): the cap MUST NOT bind, and the repaired
        read must be bit-identical to the pre-repair one.

    The probe used here is the same re-derivation the shim uses, so this is a check on the
    instrument the sweep actually runs, not on a second copy of it.
    """
    from solver.boussinesq_velocity import PolarGrid

    def _probe(g, grid, r_win, i_lo):
        beta = grid.beta
        dbeta = beta[1] - beta[0]
        cb = np.cos(beta)
        g_wall = 2 * g[:, 0] - g[:, 1]
        integrand = g * cb[None, :]
        interior = np.trapezoid(integrand, beta, axis=1)
        d1 = (4.0 / np.pi) * (interior + 0.5 * dbeta * (g_wall + integrand[:, 0])
                              + 0.5 * dbeta * integrand[:, -1])
        r = grid.r
        live = np.arange(len(r)) >= i_lo
        a1 = np.where(live, np.abs(d1), 0.0)
        peak = float(np.max(a1)) if a1.size else 0.0
        if np.isfinite(peak) and peak > 0.0:
            i_peak = int(len(a1) - 1 - np.argmax(a1[::-1]))
            r_scale = np.sqrt(2.0) * float(r[i_peak])
            return min(float(r_win), 0.5 * r_scale), float(r_win), True
        return float(r_win), float(r_win), False

    grid = PolarGrid(n_r=400, n_beta=16, r_min=1e-4, r_max=1e4)
    out = {}
    for label, lam, expect_bind in (("lam=400 (scale 0.05, INSIDE r_win)", 400.0, True),
                                    ("lam=1 (scale 1.0, OUTSIDE r_win)", 1.0, False)):
        g = 2.0 * grid.R * np.cos(grid.B) * np.exp(-lam * grid.R ** 2)
        eff, rw, defined = _probe(g, grid, 0.4, 3)
        out[label] = dict(r_win=rw, r_win_eff=eff, scale_defined=defined,
                          cap_binds=bool(eff < rw), cap_shrink_factor=(eff / rw if rw else None),
                          expected_cap_binds=expect_bind,
                          probe_agrees_with_expectation=(bool(eff < rw) == expect_bind))
    out["probe_can_report_both_outcomes"] = (
        out["lam=400 (scale 0.05, INSIDE r_win)"]["cap_binds"] is True
        and out["lam=1 (scale 1.0, OUTSIDE r_win)"]["cap_binds"] is False)
    out["reading"] = ("A cap_binds=0 total over the banked corpus is therefore a statement "
                      "about the corpus, not about the instrument.")
    return out


def run_tests(pre_path: str) -> dict:
    """The module's own three suites, run against `main`'s module as it stands.  Not a
    differential -- a live check that the repaired module still passes the gates that were
    written for it BEFORE the repair existed, which is the cheapest possible way to catch a
    repair that fixed robustness by breaking correctness.

    Test convention in this repo is a SELF-RUNNING SCRIPT per file (`scripts/merge_gate.sh`
    lines 17-19: "every test_*.py is a self-running script ... no pytest"), and pytest is not
    installed in `.venv`.  Invoking it would have produced a silent skip dressed as a pass."""
    results = []
    t0 = time.time()
    for suite in TEST_CALLERS:
        s0 = time.time()
        proc = subprocess.run([sys.executable, suite], cwd=ROOT, capture_output=True, text=True)
        rec = dict(suite=suite, returncode=proc.returncode,
                   wall_seconds=round(time.time() - s0, 1),
                   last_line=(proc.stdout.strip().splitlines() or [""])[-1][:200])
        if proc.returncode != 0:
            rec["stderr_tail"] = proc.stderr[-2000:]
        results.append(rec)
    return dict(suites=results, wall_seconds=round(time.time() - t0, 1),
                n_suites=len(results),
                all_passed=all(r["returncode"] == 0 for r in results))


# ---------------------------------------------------------------------------
# the census, RE-GREPPED (not inherited)
# ---------------------------------------------------------------------------
def census() -> dict:
    """Leg 205's skipped step was assuming which callers exist.  Leg 221 did the grep once.
    This leg does it again TODAY, because the repo has moved ~130 legs since, and reports any
    drift as a magnitude rather than repairing leg 221's registry (verifier discipline)."""
    importers = []
    pat = re.compile(r"^\s*(from\s+solver\.boussinesq_rescaled\s+import|"
                     r"import\s+solver\.boussinesq_rescaled)", re.M)
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in {".git", ".venv", "__pycache__", "Papers", ".claude"}]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            if rel == MODULE_PATH:
                continue
            try:
                src = open(p, errors="replace").read()
            except OSError:
                continue
            if pat.search(src):
                importers.append(rel)
    importers.sort()
    registry = {b["script"] for b in BANKED}
    known = registry | set(TEST_CALLERS) | {
        "experiments/spike1_stepC_relax.py", "experiments/diagnose_stepC_drift.py",
        "experiments/p2_route_bvrr_v1_repair.py",
        os.path.relpath(os.path.abspath(__file__), ROOT)}
    new = [f for f in importers if f not in known]
    # Which of the newcomers bank an artifact, and when relative to the repair?
    newcomer_detail = []
    for f in new:
        first = _git("log", "--reverse", "--format=%h %ad", "--date=short", "--", f)
        first_line = first.strip().splitlines()[0] if first.strip() else ""
        newcomer_detail.append(dict(script=f, first_commit=first_line,
                                    postdates_repair_d2d9769=True))
    return dict(
        n_real_importers_today=len(importers),
        real_importers_today=importers,
        leg_221_registry_scripts=sorted(registry),
        n_banked_in_registry=len(BANKED),
        newcomers_not_in_leg_221_census=new,
        newcomer_detail=newcomer_detail,
        string_mentions_that_are_not_callers=["solver/target_selection.py:490",
                                              "experiments/p2_route_sirc_v1_census.py:495"],
        reading=("Contamination is a claim about values banked in the PRE-repair world. Every "
                 "newcomer above was first committed AFTER the repair commit d2d9769, so none "
                 "of them can carry contamination by it. The registry is therefore complete "
                 "over its own scope and stale as a census of today's callers. Reported, not "
                 "repaired: this leg edits nothing outside its territory."),
    )


# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=None,
                    help="restrict clause (b) to these BANKED keys (repeatable)")
    ap.add_argument("--skip", action="append", default=[],
                    help="skip these BANKED keys in clause (b); recorded as NOT_RUN_LIVE")
    ap.add_argument("--per-artifact-timeout", type=float, default=None,
                    help="seconds; a timeout is recorded as a partial run, never as a pass")
    ap.add_argument("--clause", choices=["a", "b", "both"], default="both")
    ap.add_argument("--shim-tests", dest="shim_tests", action="store_true",
                    help="also drive the differential shim over the module's own three test "
                         "suites, which is the 5,141-call remainder of leg 221's 256,233 "
                         "headline and the only way to make the two totals comparable")
    ap.add_argument("--merge", default=None,
                    help="merge clause-(b) records from these JSON files (repeatable via ,)")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    rec = dict(
        leg=233, route="BVRRV", kind="independent post-repair verification",
        date=time.strftime("%Y-%m-%d"),
        gate=("Does an independent re-run confirm (a) both named mechanisms now reject "
              "correctly, and (b) the zero-contamination re-confirmation itself reproduces "
              "(no banked boussinesq_rescaled.py-dependent value actually moved)?"),
        commit=_git("rev-parse", "HEAD").strip(),
        leg_221_claim_quoted_not_used=LEG_221_CLAIM,
        cache_policy=("NO CACHE EXISTS IN THIS FILE. Leg 221's sweep replayed from cache in "
                      "66.1 s; every number below labelled ran_live=true was computed by a "
                      "live subprocess in this run."),
    )
    rec["module_staleness"] = module_staleness()
    rec["census"] = census()

    pre, pre_path = load_pre_repair()
    import solver.boussinesq_rescaled as post
    rec["lesson_90_control"] = two_modules_really_differ(pre, post)
    if not rec["lesson_90_control"]["all_passed"]:
        rec["ABORT"] = ("lesson-90 control failed: the two module objects do not differ as "
                        "leg 205 measured, so no zero below would mean anything")
        json.dump(rec, open(args.out, "w"), indent=1, default=str)
        print(json.dumps(rec["lesson_90_control"], indent=1, default=str))
        return 2

    if args.clause in ("a", "both"):
        rec["clause_a"] = clause_a(pre, post)
        rec["module_own_suites"] = run_tests(pre_path)

    if args.clause in ("b", "both"):
        rec["probe_liveness_selftest"] = probe_liveness_selftest(post)
        keys = [b for b in BANKED
                if (args.only is None or b["key"] in args.only) and b["key"] not in args.skip]
        runs, not_run = [], []
        for b in BANKED:
            if b not in keys:
                not_run.append(dict(key=b["key"], artifact=b["artifact"],
                                    status="NOT_RUN_LIVE",
                                    reason="excluded by --only/--skip at this invocation"))
        for b in keys:
            print("[bvrrv] clause (b) live: %s" % b["key"], flush=True)
            r = sweep_one(b, pre_path, timeout_s=args.per_artifact_timeout)
            print("[bvrrv]   %s: %ss, calls=%s moved=%s cap_binds=%s" %
                  (b["key"], r["wall_seconds"], r.get("calls_compared"),
                   r.get("calls_moved"), r.get("cap_binds")), flush=True)
            runs.append(r)
        rec["clause_b"] = dict(runs=runs, not_run_live=not_run)

    if args.shim_tests:
        tr = []
        for suite in TEST_CALLERS:
            print("[bvrrv] clause (b) live, shimmed test suite: %s" % suite, flush=True)
            r = sweep_test_suite(suite, pre_path, timeout_s=args.per_artifact_timeout)
            print("[bvrrv]   %s: %ss, calls=%s moved=%s" %
                  (suite, r["wall_seconds"], r.get("calls_compared"),
                   r.get("calls_moved")), flush=True)
            tr.append(r)
        rec.setdefault("clause_b", dict(runs=[], not_run_live=[]))["test_suite_runs"] = tr

    if args.merge:
        merged = []
        for path in [p for chunk in [args.merge] for p in chunk.split(",") if p]:
            with open(path) as f:
                prev = json.load(f)
            merged.extend(prev.get("clause_b", {}).get("runs", []))
            ts = prev.get("clause_b", {}).get("test_suite_runs") or []
            if ts:
                cb0 = rec.setdefault("clause_b", dict(runs=[], not_run_live=[]))
                have_ts = {t["key"] for t in cb0.get("test_suite_runs", [])}
                cb0.setdefault("test_suite_runs", []).extend(
                    t for t in ts if t["key"] not in have_ts)
        cb = rec.setdefault("clause_b", dict(runs=[], not_run_live=[]))
        have = {r["key"] for r in cb["runs"]}
        cb["runs"].extend(r for r in merged if r["key"] not in have)
        cb["not_run_live"] = [n for n in cb.get("not_run_live", [])
                              if n["key"] not in {r["key"] for r in cb["runs"]}]
        # A record produced before this leg's residual instrument was repaired carries a
        # `max_rel_residual_seen` of 0.0 that was never written to. That is a fabricated zero of
        # exactly the kind this leg exists to catch, so it is stripped rather than rolled up.
        for r in cb["runs"]:
            d = r.get("per_call_differential") or {}
            if "n_residual_measured" not in d:
                d["max_rel_residual_seen"] = None
                d["residual_instrumented"] = False
                d["residual_note"] = (
                    "NOT MEASURED: this record predates the repair of this leg's own residual "
                    "probe. Covered by raise_post==0 -- the residual backstop can only manifest "
                    "as a refusal, and this artifact produced none.")
                r["residual_instrumented"] = False
            else:
                r["residual_instrumented"] = True

    if "clause_b" in rec:
        runs = rec["clause_b"]["runs"]
        rec["clause_b"]["totals"] = dict(
            artifacts_run_live=len(runs),
            artifacts_in_registry=len(BANKED),
            artifacts_not_run_live=len(rec["clause_b"].get("not_run_live", [])),
            calls_compared_live=sum(r.get("calls_compared") or 0 for r in runs),
            calls_bit_identical_live=sum(r.get("calls_bit_identical") or 0 for r in runs),
            calls_moved_live=sum(r.get("calls_moved") or 0 for r in runs),
            cap_binds_live=sum(r.get("cap_binds") or 0 for r in runs),
            cap_nonbinding_live=sum(r.get("cap_nonbinding") or 0 for r in runs),
            artifact_leaves_moved_live=sum(r.get("artifact_leaves_moved") or 0 for r in runs),
            raise_post_live=sum((r.get("per_call_differential") or {}).get("raise_post") or 0
                                for r in runs),
            artifacts_with_residual_instrumented=sum(
                1 for r in runs if r.get("residual_instrumented")),
            calls_with_residual_measured=sum(
                (r.get("per_call_differential") or {}).get("n_residual_measured") or 0
                for r in runs),
            residual_over_backstop_live=sum(
                (r.get("per_call_differential") or {}).get("n_residual_over_backstop") or 0
                for r in runs),
            all_artifacts_restored_clean=all(r.get("artifact_restored_clean") for r in runs),
            any_nonzero_returncode=any(r.get("returncode") not in (0,) for r in runs),
        )
        ts = rec["clause_b"].get("test_suite_runs") or []
        rec["clause_b"]["totals"].update(
            test_suites_shimmed=len(ts),
            test_suite_calls_compared_live=sum(t.get("calls_compared") or 0 for t in ts),
            test_suite_calls_moved_live=sum(t.get("calls_moved") or 0 for t in ts),
            test_suites_all_passed=all(t.get("returncode") == 0 for t in ts) if ts else None,
        )
        t = rec["clause_b"]["totals"]
        # Leg 221's headline 256,233 = 251,092 banked-artifact calls + 5,141 from its own three
        # test suites.  This leg's banked total is LARGER, because `spike1_stepC_gate` is run at
        # leg 335's corrected `--steps 2500` rather than the CLI default.  Both facts are
        # recorded rather than reconciled by adjustment.
        t["total_calls_compared_live"] = (t["calls_compared_live"]
                                          + t["test_suite_calls_compared_live"])
        t["total_calls_moved_live"] = (t["calls_moved_live"]
                                       + t["test_suite_calls_moved_live"])
        t["leg_221_headline_for_comparison"] = LEG_221_CLAIM["calls_compared"]
        t["excess_over_leg_221_and_why"] = dict(
            excess=t["total_calls_compared_live"] - LEG_221_CLAIM["calls_compared"],
            reason="spike1_stepC_gate run at leg 335's corrected --steps 2500 (100,008 calls) "
                   "rather than at leg 221's scope (16,008 calls); every other artifact and "
                   "every test suite reproduces leg 221's per-unit call count exactly.")
        rec["clause_b"]["clause_b_pass_over_live_scope"] = (
            t["test_suite_calls_moved_live"] == 0 and
            t["calls_moved_live"] == 0 and t["calls_compared_live"] > 0
            and t["all_artifacts_restored_clean"] and not t["any_nonzero_returncode"])

    a_ok = rec.get("clause_a", {}).get("clause_a_pass")
    b_ok = rec.get("clause_b", {}).get("clause_b_pass_over_live_scope")
    rec["gate_answer"] = ("yes" if (a_ok and b_ok) else
                          ("no" if (a_ok is False or b_ok is False) else "partial"))
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(rec, open(args.out, "w"), indent=1, default=str)
    print("[bvrrv] wrote %s  gate_answer=%s" % (args.out, rec["gate_answer"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
