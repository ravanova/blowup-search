"""P2 Route-PNRV -- INDEPENDENT post-repair verification of leg 226's repair.

Leg 226 repaired `solver/profile_newton.py`'s convergence verdict (it added a
gauge test D2 and a decay-class test D3 to `converged`, and made
`continuation`'s warm/cold choice lexicographic in the decay class) and then
re-derived Route-D v11's four headline numbers against the repaired module.  It
reported that two of them CHANGE:

    a_max_machine             1.0  -> 0.55
    last_machine_precision_a  0.72 -> 0.52
    grid_converged_a_max      0.5  -> 0.5   (via 1.0 on its own pre-repair re-run)
    GA_boundary               [0.5, 0.55] -- a hardcoded literal, cannot move

and that the three `a = 1.50` grids, which pre-repair reported three mutually
contradictory speeds (0.204265 / 0.237174 / 0.972819, 163% relative spread) all
flagged `converged`, are ALL rejected post-repair, leaving no `a = 1.50` value.

Leg 226 never landed.  Its repair lives on branch `leg/226-pnr-v1-resume`.  This
leg is the independent re-derivation that has to happen before either outcome
(headline survives / headline changes) is treated as settled.

--------------------------------------------------------------------------
WHAT MAKES THIS INDEPENDENT, AND WHAT IT DELIBERATELY DOES NOT REUSE
--------------------------------------------------------------------------
* The repaired module is fetched with `git show` off leg 226's branch and
  imported under a private name.  That branch is never checked out and never
  edited; `solver/profile_newton.py` in this working tree is never touched.
* The PRE-repair reference module is fetched the same way at leg 226's own
  pinned commit `6a17ce6`, and this runner asserts it is byte-identical to the
  copy on `main` -- so "pre-repair" means the module the repository actually
  ships, not a private variant.
* v11's own test DEFINITIONS are read out of `experiments/p2_route_d_v11_anchor.py`
  by parsing its AST -- the `a`-ladders, the grid list, the `relres < 1e-8`
  threshold, the `c_spread < 1e-3` / `>= 2 grids` rule and the `GA_boundary`
  literal are extracted from v11's source, never transcribed from leg 226's
  summary.  A transcription error in this leg would otherwise reproduce leg
  226's numbers for the wrong reason.
* Leg 226's REPORTED numbers are likewise read from its banked JSON via
  `git show`, not typed in here.
* Leg 226's runner (`experiments/p2_route_pnr_v1_repair.py`) is NOT imported.
  The measurement is re-implemented from v11's definitions.  The one thing
  taken from that runner is a PROTOCOL input, not a number: the `a`-ladder the
  `a = 1.50` continuation walks, which is leg 226's own choice and has to match
  for the comparison to mean anything.  It is re-derived here as
  `np.arange(0.0, 1.51, 0.15)` and ASSERTED equal to leg 226's literal.

--------------------------------------------------------------------------
ONE MEASUREMENT CONVENTION THAT IS THIS LEG'S OWN, AND WHY
--------------------------------------------------------------------------
v11's V4 computes the grid-convergence verdict as

    cs   = [r["c"] for r in sub]                 # ALL grids at this a
    n_ok = sum(1 for r in sub if r["relres"] < 1e-8)
    grid_converged = (max(cs) - min(cs) < 1e-3) and n_ok >= 2

i.e. the SPREAD is over every grid and the COUNT is over the converged ones.
Leg 226's re-derivation instead takes both over the accepted rows only.  Those
are different statistics and they do not have to agree, so this leg computes
BOTH and reports both.  Reporting only one of them would be reporting a
convention as a measurement.

Plain float64.  Nothing here is interval-enclosed and nothing is rigorous.
This leg applies NO correction to any banked artifact: it is confirm-or-flag
only, by its own pre-committed gate.

Run:  .venv/bin/python experiments/p2_route_pnrv_v1_postrepair.py
Out:  writeup/data/p2_route_pnrv_v1_postrepair.json  (checkpointed per stage)
"""

import ast
import importlib.util
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "writeup" / "data" / "p2_route_pnrv_v1_postrepair.json"

REPAIR_REF = "origin/leg/226-pnr-v1-resume"   # leg 226's repair, never merged
PRE_REF = "6a17ce6"                           # leg 226's own pre-repair pin
V11_SRC = ROOT / "experiments" / "p2_route_d_v11_anchor.py"
V11_BANKED = ROOT / "writeup" / "data" / "p2_route_d_v11_anchor.json"

# Fast mode exists ONLY so the structure of the runner can be exercised without
# paying the full n=1601 bill; it is never the mode the reported numbers come
# from, and the JSON records which mode produced it.
FAST = os.environ.get("PNRV_FAST") == "1"


# ---------------------------------------------------------------------------
# fetching the two modules, without checking anything out
# ---------------------------------------------------------------------------
def git_show(ref_path):
    """`git show <ref>:<path>` as text, from this worktree."""
    return subprocess.run(["git", "show", ref_path], cwd=str(ROOT),
                          capture_output=True, text=True,
                          check=True).stdout


def load_module(name, source_text, tmpdir):
    path = Path(tmpdir) / (name + ".py")
    path.write_text(source_text)
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# v11's own definitions, read out of v11's own source
# ---------------------------------------------------------------------------
def extract_v11_defs():
    """Parse `p2_route_d_v11_anchor.py` for every constant this leg reuses.

    Everything returned here is v11's, structurally extracted.  If v11's source
    ever changes shape this raises instead of silently falling back to a
    remembered value -- a check that is not executable decays at the rate of
    memory (lesson 68).
    """
    src = V11_SRC.read_text()
    tree = ast.parse(src)
    defs = {"source_sha": subprocess.run(
        ["git", "rev-parse", "HEAD:experiments/p2_route_d_v11_anchor.py"],
        cwd=str(ROOT), capture_output=True, text=True).stdout.strip()}

    top = {n.targets[0].id: n.value for n in tree.body
           if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}
    defs["N"] = ast.literal_eval(top["N"])
    defs["ALPHA"] = ast.literal_eval(top["ALPHA"])

    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}

    # V2's a-ladder: the list literal assigned to a_values inside v2_sweep.
    v2_lists = [ast.literal_eval(node.value) for node in ast.walk(funcs["v2_sweep"])
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.List)]
    if len(v2_lists) != 1:
        raise RuntimeError("v2_sweep no longer has exactly one list literal")
    defs["v2_a_values"] = [float(v) for v in v2_lists[0]]

    # V3's ladder: np.round(np.arange(lo, hi, step), 3).
    arange_args = None
    round_nd = None
    for node in ast.walk(funcs["v3_boundary"]):
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "arange":
            arange_args = [ast.literal_eval(a) for a in node.args]
        if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "round":
            round_nd = ast.literal_eval(node.args[1])
    if arange_args is None or round_nd is None:
        raise RuntimeError("v3_boundary's ladder is no longer np.round(np.arange(...))")
    defs["v3_arange"] = arange_args
    defs["v3_a_values"] = [float(v) for v in
                           np.round(np.arange(*arange_args), round_nd)]

    # V3's GA_boundary: a literal in the returned dict, not a computed verdict.
    ga = None
    for node in ast.walk(funcs["v3_boundary"]):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == "GA_boundary":
                    ga = ast.literal_eval(v)
    if ga is None:
        raise RuntimeError("GA_boundary is no longer a literal in v3_boundary")
    defs["GA_boundary_literal"] = ga
    defs["GA_boundary_is_literal"] = True

    # V4's grids and a-values: signature defaults.
    sig = funcs["v4_grids"].args
    kw = dict(zip([a.arg for a in sig.args],
                  [ast.literal_eval(d) for d in sig.defaults]))
    defs["v4_ns"] = [int(v) for v in kw["ns"]]
    defs["v4_a_values"] = [float(v) for v in kw["a_values"]]

    # The thresholds, asserted against v11's literal source text so that a
    # silent change of any of them fails loudly here.
    checks = {
        "relres_threshold_1e-8": 'r["relres"] < 1e-8',
        "c_spread_threshold_1e-3": "max(cs) - min(cs) < 1e-3",
        "min_grids_2": "n_ok >= 2",
        "v4_spread_over_all_rows": 'cs = [r["c"] for r in sub]',
        "v4_count_over_converged": 'n_ok = sum(1 for r in sub if r["relres"] < 1e-8)',
    }
    missing = [k for k, v in checks.items() if v not in src]
    if missing:
        raise RuntimeError("v11 source no longer contains: %s" % missing)
    defs["threshold_expressions_found_verbatim_in_v11_source"] = checks
    defs["relres_threshold"] = 1e-8
    defs["c_spread_threshold"] = 1e-3
    defs["min_grids"] = 2
    return defs


# ---------------------------------------------------------------------------
# the measurement primitives, re-implemented from v11's definitions
# ---------------------------------------------------------------------------
def cold_row(mod, a, n, post_mod):
    """One cold solve, with both verdicts attached.

    v11's V3 and V4 use ONLY cold `solve()`, whose iteration is untouched by the
    repair (the diff changes the returned dict, not the Newton loop).  This leg
    verifies that claim independently rather than assuming it -- see
    `bit_identity_checks` -- and, having verified it, reads the PRE-repair
    verdict off the repaired module's own `residual_converged` field, which is
    the pre-repair `converged` expression verbatim:

        hist[-1] < 1e-6 * max(1.0, hist[0])  or  hist[-1] < 1e-9
    """
    t0 = time.time()
    nw = mod.TwoScaleNewton(a=float(a), n=int(n))
    r = nw.solve(om0=None, c0=0.5)
    X = nw.fam.X
    i4 = int(np.argmin(np.abs(X - 4.0)))
    row = {"a": float(a), "n": int(n), "relres": float(r["relres"]),
           "residual_rms": float(r["residual_rms"]), "c": float(r["c"]),
           "iterations": int(r["iterations"]),
           "Omega_at_X4": float(r["Omega"][i4]),
           "secs": time.time() - t0}
    if mod is post_mod:
        row.update({
            "D3_farfield_inflation": float(r["farfield_inflation"]),
            "D2_gauge_residual": float(r["gauge_residual"]),
            "repaired_converged": bool(r["converged"]),
            "pre_repair_converged": bool(r["residual_converged"]),
            "reason": r.get("reason"),
        })
    else:
        row["pre_repair_converged"] = bool(r["converged"])
    return row


def v2_a_max_machine(mod, defs, post_mod):
    """v11's V2 headline, re-derived: `a_max_machine` off `continuation`.

    `continuation` IS changed by the repair (branch-continuity), so this is run
    against both modules rather than shortcut.
    """
    a_values = defs["v2_a_values"] if not FAST else defs["v2_a_values"][:3]
    n = defs["N"] if not FAST else 101
    rows = mod.continuation(a_values, n=n)
    out = []
    for r in rows:
        row = {"a": float(r["a"]), "relres": float(r["relres"]),
               "c": float(r["c"]), "iterations": int(r["iterations"]),
               "converged": bool(r["converged"])}
        for k in ("on_branch", "gauge_residual", "farfield_inflation", "reason"):
            if k in r:
                row[k] = r[k] if k == "reason" else (
                    bool(r[k]) if k == "on_branch" else float(r[k]))
        out.append(row)
    thr = defs["relres_threshold"]
    v11_ok = [r["a"] for r in out if r["relres"] < thr]
    rep_ok = [r["a"] for r in out if r["relres"] < thr and r["converged"]]
    return {"rows": out, "n": n, "a_values": a_values,
            "a_max_machine_v11_own_test": max(v11_ok, default=0.0),
            "a_max_machine_repaired_verdict": max(rep_ok, default=0.0),
            "best_relres": min(r["relres"] for r in out)}


def v3_last_machine_precision_a(rows, defs):
    thr = defs["relres_threshold"]
    v11_ok = [r["a"] for r in rows if r["relres"] < thr]
    rep_ok = [r["a"] for r in rows
              if r["relres"] < thr and r["repaired_converged"]]
    return {"rows": rows,
            "last_machine_precision_a_v11_own_test": max(v11_ok) if v11_ok else None,
            "last_machine_precision_a_repaired_verdict": (max(rep_ok) if rep_ok
                                                          else None)}


def v4_verdicts(rows, defs, accept):
    """Both spread conventions, side by side (see the module docstring)."""
    out_lit, out_acc = [], []
    for a in defs["v4_a_values"]:
        sub = [r for r in rows if r["a"] == a]
        ok = [r for r in sub if accept(r)]
        cs_all = [r["c"] for r in sub]
        cs_ok = [r["c"] for r in ok]
        # (i) v11's LITERAL convention: spread over all grids, count over the
        #     converged ones.
        out_lit.append({
            "a": float(a), "n_grids_total": len(sub),
            "c_spread_all_grids": (float(max(cs_all) - min(cs_all)) if cs_all
                                   else None),
            "grids_reaching_machine_precision": len(ok),
            "grid_converged": bool(cs_all
                                   and max(cs_all) - min(cs_all)
                                   < defs["c_spread_threshold"]
                                   and len(ok) >= defs["min_grids"])})
        # (ii) leg 226's convention: both statistics over the accepted rows.
        out_acc.append({
            "a": float(a), "cs": cs_ok,
            "c_spread": (float(max(cs_ok) - min(cs_ok)) if cs_ok else None),
            "n_grids": len(ok),
            "grid_converged": bool(len(ok) >= defs["min_grids"]
                                   and max(cs_ok) - min(cs_ok)
                                   < defs["c_spread_threshold"])})
    return {
        "verdict_v11_literal_spread_over_all_grids": out_lit,
        "verdict_accepted_rows_only_leg226_convention": out_acc,
        "grid_converged_a_max_v11_literal": max(
            (v["a"] for v in out_lit if v["grid_converged"]), default=0.0),
        "grid_converged_a_max_accepted_only": max(
            (v["a"] for v in out_acc if v["grid_converged"]), default=0.0),
    }


def safely(fn, *args):
    """Run a COMPARISON and never lose the MEASUREMENT if it raises.

    Every expensive solve is banked into the JSON before any comparison against
    leg 226's table is attempted, and a comparison that raises is recorded as an
    error string rather than taking the run down with it.  A verification leg
    that lost three hours of solves to a zip-length mismatch would have to
    re-run them to say anything at all.
    """
    try:
        return fn(*args)
    except Exception as exc:                                  # pragma: no cover
        return {"comparison_error": "%s: %s" % (type(exc).__name__, exc)}


def rel_err(mine, theirs):
    """Relative error, with the degenerate cases named rather than hidden."""
    if mine is None or theirs is None:
        return None if mine is theirs else float("inf")
    if theirs == 0.0:
        return 0.0 if mine == 0.0 else float("inf")
    return abs(float(mine) - float(theirs)) / abs(float(theirs))


def addendum():
    """M6, run separately after the main arm: the width-gauge substrate finding.

    This costs seconds and reuses the main arm's banked rows, so it is a second
    pass over the existing JSON rather than a reason to re-run three hours of
    solves.  It exists because this leg's own D2 control failed in a way that
    turned out not to be a defect of leg 226's repair at all:

    `i1 = argmin|X - 1|` selects the SAME node at n = 101 and n = 1601 -- the
    rho-grids are nested and no refinement puts a node closer to X = 1 -- so
    gauge 2 pins Omega = -1/2 at X = 0.99594..., while -1/2 is the anchor's
    value at X = 1 exactly.  The discrete a = 0 traveling wave is therefore
    slightly narrower than the continuum anchor and travels at X[i1]/2, not
    1/2, at EVERY resolution.  v11 reads its a = 0 speed as 0.49797 and treats
    the residual spread across grids as discretization; part of it is not.

    Nothing is corrected here.  This leg reports the magnitude and stops.
    """
    from solver.gclm_family import GCLMResidual                      # noqa: E402
    data = json.loads(OUT.read_text())
    grid = []
    for n in (101, 201, 401, 801, 1601):
        f = GCLMResidual(a=0.0, n=int(n))
        X = f.X
        i1 = int(np.argmin(np.abs(X - 1.0)))
        anc = -1.0 / (1.0 + X ** 2)
        grid.append({"n": int(n), "drho": float(f.drho), "i1": i1,
                     "X_at_i1": float(X[i1]),
                     "anchor_gauge2_miss": float(abs(anc[i1] + 0.5)),
                     "predicted_discrete_a0_speed": float(X[i1] / 2.0)})
    xs = sorted({r["X_at_i1"] for r in grid})
    pred = grid[0]["predicted_discrete_a0_speed"]

    # measured a = 0 speeds, taken from the main arm's own V4 rows
    meas = [{"n": r["n"], "c": r["c"],
             "rel_err_vs_X1_over_2": rel_err(r["c"], pred)}
            for r in data.get("m4_v4_grid_converged_a_max", {}).get("rows", [])
            if r["a"] == 0.0]

    # D3 is ONE-SIDED by construction: it rejects fat far fields and never thin
    # ones.  That is leg 226's stated design (the true branch decays FASTER
    # than the anchor), but the magnitude it lets through is worth recording.
    d3 = [r["D3_farfield_inflation"]
          for r in data.get("m4_v4_grid_converged_a_max", {}).get("rows", [])
          if r.get("repaired_converged")]

    data["m6_width_gauge_substrate"] = {
        "grid": grid,
        "gauge_node_is_grid_independent": len(xs) == 1,
        "X_at_i1": xs[0] if len(xs) == 1 else xs,
        "refinement_factor_101_to_1601": grid[0]["drho"] / grid[-1]["drho"],
        "anchor_gauge2_miss": grid[0]["anchor_gauge2_miss"],
        "predicted_discrete_a0_speed_X1_over_2": pred,
        "measured_a0_speeds": meas,
        "D3_on_accepted_rows_min": min(d3) if d3 else None,
        "D3_on_accepted_rows_max": max(d3) if d3 else None,
        "reading": "The width gauge does not move under refinement: X[i1] is "
                   "identical at n = 101 and n = 1601 across a 16x change of "
                   "drho, so the exact anchor misses gauge 2 by 2.033109e-03 "
                   "at EVERY resolution and the discrete a = 0 speed is "
                   "X[i1]/2, not 1/2. Four identical numbers are usually the "
                   "tell for a control that cannot come out differently "
                   "(lesson 90); here the grid-independence IS the finding, "
                   "and it is asserted executably in "
                   "test_profile_newton_postrepair.py. This is a property of "
                   "gclm_family's grid and v11's gauge choice, NOT a defect of "
                   "leg 226's repair, and it does not move this leg's gate. "
                   "D3's one-sidedness is recorded with it: it rejects fat far "
                   "fields only, so a profile whose far field is orders BELOW "
                   "the anchor's passes -- by design (the genuine branch "
                   "decays faster), but the passing magnitudes are banked here "
                   "rather than left implicit.",
    }
    data["meta"]["addendum_completed"] = True
    OUT.write_text(json.dumps(data, indent=2))
    print("[addendum] X[i1] = %.16f at every n (drho 16x), anchor gauge-2 miss "
          "%.6e, predicted a=0 speed %.17f" % (xs[0], grid[0]["anchor_gauge2_miss"],
                                               pred))
    for m in meas:
        print("           measured a=0 c at n=%-5d %.16f  rel err vs X1/2 %.3e"
              % (m["n"], m["c"], m["rel_err_vs_X1_over_2"]))


def main():
    t_start = time.time()
    data = {"meta": {
        "leg": "P2 Route-PNRV v1 (independent post-repair verification of leg "
               "226's profile_newton.py repair and its Route-D v11 re-scoping)",
        "tier": "Level-1 verification; NOT a certificate, nothing rigorous",
        "reproduce": "python experiments/p2_route_pnrv_v1_postrepair.py",
        "repair_ref": REPAIR_REF, "pre_repair_ref": PRE_REF,
        "fast_mode": FAST,
        "numpy": np.__version__, "python": platform.python_version(),
        "applies_no_correction": "This leg reports magnitudes and flags. It "
                                 "edits no banked artifact under either gate "
                                 "branch, by its own pre-committed contract.",
    }}

    def checkpoint(stage):
        data["meta"]["last_stage_completed"] = stage
        data["meta"]["elapsed_s"] = time.time() - t_start
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(data, indent=2))
        print("[checkpoint] %-22s  %.1f s" % (stage, time.time() - t_start),
              flush=True)

    tmpdir = tempfile.mkdtemp(prefix="pnrv_")
    pre_src = git_show("%s:solver/profile_newton.py" % PRE_REF)
    post_src = git_show("%s:solver/profile_newton.py" % REPAIR_REF)
    live_src = (ROOT / "solver" / "profile_newton.py").read_text()

    data["provenance"] = {
        "pre_repair_module_is_byte_identical_to_working_tree": pre_src == live_src,
        "repaired_module_differs_from_working_tree": post_src != live_src,
        "pre_repair_commit": subprocess.run(
            ["git", "rev-parse", PRE_REF], cwd=str(ROOT), capture_output=True,
            text=True).stdout.strip(),
        "repair_commit": subprocess.run(
            ["git", "rev-parse", REPAIR_REF], cwd=str(ROOT),
            capture_output=True, text=True).stdout.strip(),
        "note": "The repaired module is read off leg 226's branch with `git "
                "show`; that branch is never checked out and "
                "solver/profile_newton.py is never edited by this leg.",
    }
    if not data["provenance"]["pre_repair_module_is_byte_identical_to_working_tree"]:
        raise RuntimeError("pre-repair reference %s differs from the working "
                           "tree's solver/profile_newton.py -- the comparison "
                           "would not mean what it says" % PRE_REF)

    pre = load_module("_pnrv_pre_profile_newton", pre_src, tmpdir)
    post = load_module("_pnrv_post_profile_newton", post_src, tmpdir)

    # leg 226's own reported numbers, read from its banked JSON (never typed).
    reported = json.loads(git_show(
        "%s:writeup/data/p2_route_pnr_v1_repair.json" % REPAIR_REF))
    rep_d = reported["arm_d_route_d_v11_rederivation"]
    banked_v11 = json.loads(V11_BANKED.read_text()) if V11_BANKED.exists() else {}

    defs = extract_v11_defs()
    data["v11_definitions_extracted"] = defs
    data["leg226_reported"] = {k: rep_d[k] for k in
                               ("a_max_machine", "last_machine_precision_a",
                                "grid_converged_a_max", "GA_boundary",
                                "a_1p50_three_grids", "bit_identical_check")}
    data["banked_v11_headlines"] = {
        "a_max_machine": banked_v11.get("v2_sweep", {}).get("a_max_machine"),
        "last_machine_precision_a": banked_v11.get("v3_boundary", {}).get(
            "last_machine_precision_a"),
        "grid_converged_a_max": banked_v11.get("v4_grids", {}).get(
            "grid_converged_a_max"),
        "GA_boundary": banked_v11.get("v3_boundary", {}).get("GA_boundary"),
    }
    checkpoint("definitions")

    # -- M0: is the Newton iteration really untouched by the repair? ---------
    # Leg 226 verified this at ONE point (a=0.5, n=801).  A single point is a
    # weak check for a claim the whole measurement shortcut rests on, so this
    # leg checks a spread of points, including the cheap end of every grid.
    pts = [(0.2, 401), (0.5, 801), (0.72, 801), (0.0, 1601)]
    if FAST:
        pts = [(0.2, 101), (0.5, 201)]
    bits = []
    for a, n in pts:
        rp = cold_row(pre, a, n, post)
        rq = cold_row(post, a, n, post)
        bits.append({
            "a": a, "n": n,
            "c_pre": rp["c"], "c_post": rq["c"],
            "c_delta": abs(rp["c"] - rq["c"]),
            "relres_pre": rp["relres"], "relres_post": rq["relres"],
            "relres_delta": abs(rp["relres"] - rq["relres"]),
            "iterations_pre": rp["iterations"],
            "iterations_post": rq["iterations"],
            "bit_identical": (rp["c"] == rq["c"]
                              and rp["relres"] == rq["relres"]
                              and rp["iterations"] == rq["iterations"])})
    data["bit_identity_checks"] = {
        "rows": bits,
        "all_bit_identical": all(b["bit_identical"] for b in bits),
        "leg226_checked_only": {"a": rep_d["bit_identical_check"]["a"],
                                "n": rep_d["bit_identical_check"]["n"]},
        "reading": "The repair changes the returned dict, not the Newton loop. "
                   "If any row here were NOT bit-identical, every 'cold solves "
                   "are unchanged' shortcut -- leg 226's and this leg's -- "
                   "would be invalid, so it is checked at four points spanning "
                   "three grids rather than at one.",
    }
    checkpoint("bit_identity")

    # -- M1: the a = 1.50 three-grid case ------------------------------------
    # The ladder is leg 226's PROTOCOL choice, re-derived here and asserted
    # against its literal rather than copied.
    ladder = [float(v) for v in np.round(np.arange(0.0, 1.51, 0.15), 10)]
    ladder_226 = None
    try:
        rsrc = git_show("%s:experiments/p2_route_pnr_v1_repair.py" % REPAIR_REF)
        for node in ast.walk(ast.parse(rsrc)):
            if (isinstance(node, ast.Assign)
                    and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id == "LADDER_A"):
                ladder_226 = [float(v) for v in ast.literal_eval(node.value)]
    except Exception as exc:                                  # pragma: no cover
        ladder_226 = "unavailable: %s" % exc
    ladder_matches = (isinstance(ladder_226, list)
                      and len(ladder_226) == len(ladder)
                      and all(abs(x - y) < 1e-12
                              for x, y in zip(ladder, ladder_226)))

    grids150 = (101, 201, 301) if not FAST else (101,)
    rows150 = []
    for n in grids150:
        t0 = time.time()
        rp = pre.continuation(ladder, n=n)
        rq = post.continuation(ladder, n=n)
        p = [r for r in rp if abs(r["a"] - 1.5) < 1e-12][0]
        q = [r for r in rq if abs(r["a"] - 1.5) < 1e-12][0]
        rows150.append({
            "n": n,
            "pre_c": float(p["c"]), "pre_converged": bool(p["converged"]),
            "pre_relres": float(p["relres"]),
            "post_c": float(q["c"]), "post_converged": bool(q["converged"]),
            "post_relres": float(q["relres"]),
            "D3": float(q["farfield_inflation"]),
            "D2_gauge_residual": float(q["gauge_residual"]),
            "post_reason": q.get("reason"), "secs": time.time() - t0})
    pre_c150 = [r["pre_c"] for r in rows150]
    acc150 = [r["post_c"] for r in rows150 if r["post_converged"]]
    mine150 = {
        "ladder_rederived": ladder, "ladder_matches_leg226_literal": ladder_matches,
        "rows": rows150, "pre_repair_c_values": pre_c150,
        "pre_repair_relative_spread": ((max(pre_c150) - min(pre_c150))
                                       / abs(float(np.mean(pre_c150)))
                                       if pre_c150 else None),
        "n_grids_accepted_post_repair": len(acc150),
        "post_repair_accepted_c_values": acc150,
    }
    data["m1_a_1p50_three_grids"] = mine150
    checkpoint("a_1p50_rows_measured")
    t150 = rep_d["a_1p50_three_grids"]
    mine150["comparison_to_leg226"] = safely(lambda: {
        "pre_repair_relative_spread": {
            "mine": mine150["pre_repair_relative_spread"],
            "leg226": t150["pre_repair_relative_spread"],
            "rel_err": rel_err(mine150["pre_repair_relative_spread"],
                               t150["pre_repair_relative_spread"])},
        "n_grids_accepted_post_repair": {
            "mine": len(acc150), "leg226": t150["n_grids_accepted_post_repair"]},
        "per_grid": [
            {"n": m["n"],
             "pre_c_mine": m["pre_c"], "pre_c_leg226": t.get("pre_c"),
             "pre_c_rel_err": rel_err(m["pre_c"], t.get("pre_c")),
             "post_c_mine": m["post_c"], "post_c_leg226": t.get("post_c"),
             "post_c_rel_err": rel_err(m["post_c"], t.get("post_c")),
             "D3_mine": m["D3"], "D3_leg226": t.get("D3"),
             "D3_rel_err": rel_err(m["D3"], t.get("D3")),
             "post_converged_mine": m["post_converged"],
             "post_converged_leg226": t.get("post_converged")}
            for m, t in zip(rows150, t150["rows"])],
    })
    checkpoint("a_1p50")

    # -- M2: V3, last_machine_precision_a ------------------------------------
    v3_as = defs["v3_a_values"] if not FAST else defs["v3_a_values"][:2]
    v3_rows = [cold_row(post, a, defs["N"] if not FAST else 201, post)
               for a in v3_as]
    mine3 = v3_last_machine_precision_a(v3_rows, defs)
    data["m2_v3_last_machine_precision_a"] = mine3
    checkpoint("v3_rows_measured")
    t3 = rep_d["last_machine_precision_a"]
    mine3["comparison_to_leg226"] = safely(lambda: {
        "banked": {"mine_reads": data["banked_v11_headlines"][
            "last_machine_precision_a"], "leg226": t3["banked"]},
        "v11_own_test": {"mine": mine3["last_machine_precision_a_v11_own_test"],
                         "leg226": t3["post_repair_v11_own_relres_test"],
                         "rel_err": rel_err(
                             mine3["last_machine_precision_a_v11_own_test"],
                             t3["post_repair_v11_own_relres_test"])},
        "repaired_verdict": {
            "mine": mine3["last_machine_precision_a_repaired_verdict"],
            "leg226": t3["post_repair_repaired_verdict"],
            "rel_err": rel_err(
                mine3["last_machine_precision_a_repaired_verdict"],
                t3["post_repair_repaired_verdict"])},
        "per_row": [
            {"a": m["a"], "relres_mine": m["relres"],
             "relres_leg226": t.get("relres"),
             "relres_rel_err": rel_err(m["relres"], t.get("relres")),
             "c_mine": m["c"], "c_leg226": t.get("c"),
             "c_rel_err": rel_err(m["c"], t.get("c")),
             "D3_mine": m["D3_farfield_inflation"], "D3_leg226": t.get("D3"),
             "D3_rel_err": rel_err(m["D3_farfield_inflation"], t.get("D3")),
             "v11_own_test_mine": m["relres"] < defs["relres_threshold"],
             "v11_own_test_leg226": t.get("v11_own_test"),
             "repaired_verdict_mine": bool(
                 m["relres"] < defs["relres_threshold"]
                 and m["repaired_converged"]),
             "repaired_verdict_leg226": t.get("repaired_verdict")}
            for m, t in zip(v3_rows, t3["rows"])] if not FAST else "skipped(FAST)",
    })
    checkpoint("v3_boundary")

    # -- M3: V2, a_max_machine (continuation -- the function the repair changed)
    v2_pre = v2_a_max_machine(pre, defs, post)
    checkpoint("v2_pre")
    v2_post = v2_a_max_machine(post, defs, post)
    data["m3_v2_a_max_machine"] = {"pre_repair": v2_pre, "post_repair": v2_post}
    checkpoint("v2_rows_measured")
    t2 = rep_d["a_max_machine"]
    data["m3_v2_a_max_machine"]["comparison_to_leg226"] = safely(lambda: {
            "banked": {"mine_reads": data["banked_v11_headlines"]["a_max_machine"],
                       "leg226": t2["banked"]},
            "pre_repair_rerun": {
                "mine": v2_pre["a_max_machine_v11_own_test"],
                "leg226": t2["pre_repair_rerun_here"],
                "rel_err": rel_err(v2_pre["a_max_machine_v11_own_test"],
                                   t2["pre_repair_rerun_here"])},
            "post_repair_v11_own_test": {
                "mine": v2_post["a_max_machine_v11_own_test"],
                "leg226": t2["post_repair_v11_own_relres_test"],
                "rel_err": rel_err(v2_post["a_max_machine_v11_own_test"],
                                   t2["post_repair_v11_own_relres_test"])},
            "post_repair_repaired_verdict": {
                "mine": v2_post["a_max_machine_repaired_verdict"],
                "leg226": t2["post_repair_repaired_verdict"],
                "rel_err": rel_err(v2_post["a_max_machine_repaired_verdict"],
                                   t2["post_repair_repaired_verdict"])},
        })
    checkpoint("v2_post")

    # -- M4: V4, grid_converged_a_max ----------------------------------------
    v4_ns = defs["v4_ns"] if not FAST else [101]
    v4_rows = []
    for n in v4_ns:
        for a in defs["v4_a_values"]:
            v4_rows.append(cold_row(post, a, n, post))
            print("   [v4] n=%d a=%.2f  relres %.3e  c %.16f  %.1f s"
                  % (n, a, v4_rows[-1]["relres"], v4_rows[-1]["c"],
                     v4_rows[-1]["secs"]), flush=True)
        checkpoint("v4_grids_n%d" % n)
    thr = defs["relres_threshold"]
    mine4 = {"rows": v4_rows}
    mine4["v11_own_test"] = v4_verdicts(
        v4_rows, defs, lambda r: r["relres"] < thr)
    mine4["repaired_verdict"] = v4_verdicts(
        v4_rows, defs, lambda r: r["relres"] < thr and r["repaired_converged"])
    data["m4_v4_grid_converged_a_max"] = mine4
    checkpoint("v4_rows_measured")
    t4 = rep_d["grid_converged_a_max"]
    mine4["comparison_to_leg226"] = safely(lambda: {
        "banked": {"mine_reads": data["banked_v11_headlines"][
            "grid_converged_a_max"], "leg226": t4["banked"]},
        "pre_repair_rerun_accepted_only_convention": {
            "mine": mine4["v11_own_test"]["grid_converged_a_max_accepted_only"],
            "leg226": t4["pre_repair_rerun_here"],
            "rel_err": rel_err(
                mine4["v11_own_test"]["grid_converged_a_max_accepted_only"],
                t4["pre_repair_rerun_here"])},
        "post_repair_v11_own_test_accepted_only_convention": {
            "mine": mine4["v11_own_test"]["grid_converged_a_max_accepted_only"],
            "leg226": t4["post_repair_v11_own_relres_test"],
            "rel_err": rel_err(
                mine4["v11_own_test"]["grid_converged_a_max_accepted_only"],
                t4["post_repair_v11_own_relres_test"])},
        "post_repair_repaired_verdict_accepted_only_convention": {
            "mine": mine4["repaired_verdict"][
                "grid_converged_a_max_accepted_only"],
            "leg226": t4["post_repair_repaired_verdict"],
            "rel_err": rel_err(
                mine4["repaired_verdict"]["grid_converged_a_max_accepted_only"],
                t4["post_repair_repaired_verdict"])},
        "v11_LITERAL_convention_not_used_by_leg226": {
            "v11_own_test": mine4["v11_own_test"]["grid_converged_a_max_v11_literal"],
            "repaired_verdict": mine4["repaired_verdict"][
                "grid_converged_a_max_v11_literal"],
            "note": "v11's own code spreads over ALL grids and counts only the "
                    "converged ones; leg 226 took both over the accepted rows. "
                    "Both are reported because they are different statistics."},
        "per_row": [
            {"n": m["n"], "a": m["a"], "relres_mine": m["relres"],
             "relres_leg226": t.get("relres"),
             "relres_rel_err": rel_err(m["relres"], t.get("relres")),
             "c_mine": m["c"], "c_leg226": t.get("c"),
             "c_rel_err": rel_err(m["c"], t.get("c")),
             "D3_mine": m["D3_farfield_inflation"], "D3_leg226": t.get("D3")}
            for m, t in zip(v4_rows, t4["rows"])] if not FAST else "skipped(FAST)",
    })
    checkpoint("v4_grids")

    # -- M5: GA_boundary, the headline that cannot move ----------------------
    data["m5_GA_boundary"] = {
        "v11_literal": defs["GA_boundary_literal"],
        "banked": data["banked_v11_headlines"]["GA_boundary"],
        "leg226_reported": rep_d["GA_boundary"],
        "is_hardcoded_literal_confirmed_by_ast": defs["GA_boundary_is_literal"],
        "profile_newton_mentions_GA_boundary": ("GA_boundary" in post_src
                                                or "GA_boundary" in pre_src),
        "reading": "GA_boundary is a literal in v11's V3 return dict quoting the "
                   "GA's own prior result. No repair to profile_newton.py can "
                   "move it -- confirmed here structurally (AST) and by the "
                   "absence of the string from either module. Reporting it as "
                   "'unchanged' without saying why would be a control that "
                   "cannot come out differently (lesson 90).",
    }
    checkpoint("GA_boundary")

    # -- the gate ------------------------------------------------------------
    headline = {
        "a_max_machine": data["m3_v2_a_max_machine"]["comparison_to_leg226"],
        "last_machine_precision_a": mine3["comparison_to_leg226"],
        "grid_converged_a_max": mine4["comparison_to_leg226"],
        "a_1p50_three_grids": mine150["comparison_to_leg226"],
    }

    def agree(cmp_block, keys):
        out = {}
        for k in keys:
            b = cmp_block.get(k)
            if isinstance(b, dict) and "mine" in b:
                out[k] = {"mine": b["mine"], "leg226": b["leg226"],
                          "rel_err": b.get("rel_err"),
                          "exact": b["mine"] == b["leg226"]}
        return out

    verdict = {
        "a_max_machine": agree(headline["a_max_machine"],
                               ["pre_repair_rerun", "post_repair_v11_own_test",
                                "post_repair_repaired_verdict"]),
        "last_machine_precision_a": agree(
            headline["last_machine_precision_a"],
            ["v11_own_test", "repaired_verdict"]),
        "grid_converged_a_max": agree(
            headline["grid_converged_a_max"],
            ["pre_repair_rerun_accepted_only_convention",
             "post_repair_v11_own_test_accepted_only_convention",
             "post_repair_repaired_verdict_accepted_only_convention"]),
    }
    # An EMPTY comparison block must never read as agreement: if any comparison
    # failed to assemble, the gate is UNANSWERED, not YES (lesson 90's shape --
    # a check that cannot come out differently is not a check).
    expected_keys = {"a_max_machine": 3, "last_machine_precision_a": 2,
                     "grid_converged_a_max": 3}
    complete = all(len(verdict[k]) == n for k, n in expected_keys.items())
    reproduced = complete and all(v["exact"] for blk in verdict.values()
                                  for v in blk.values())
    c150 = mine150.get("comparison_to_leg226", {})
    a150_ok = bool(
        "comparison_error" not in c150
        and mine150["n_grids_accepted_post_repair"]
        == t150["n_grids_accepted_post_repair"]
        and (c150.get("pre_repair_relative_spread", {}).get("rel_err") or 0.0)
        < 1e-9)
    data["gate"] = {
        "question": "Does an independent re-run of leg 226's repaired "
                    "profile_newton.py, applied fresh to Route-D v11's own "
                    "inputs, reproduce leg 226's own reported before/after "
                    "a_max_machine/GA_boundary values (whether unchanged or "
                    "changed), at its own resolution, including the three-grid "
                    "a=1.50 disagreement?",
        "per_headline": verdict,
        "a_1p50_reproduced": a150_ok,
        "bit_identity_verified": data["bit_identity_checks"]["all_bit_identical"],
        "all_comparisons_assembled": complete,
        "answer": ("YES" if (reproduced and a150_ok)
                   else ("NO" if complete else "UNANSWERED (a comparison block "
                         "failed to assemble -- see comparison_error)")),
        "escalation": "Either way this leg applies no correction. A YES routes "
                      "the headline correction to the user/orchestrator "
                      "(ORCHESTRATION.md sec 8); a NO is reported as the "
                      "highest-priority finding in the backlog.",
    }
    checkpoint("gate")

    print("\nP2 ROUTE-PNRV -- independent post-repair verification\n" + "=" * 62)
    for name, blk in verdict.items():
        for k, v in blk.items():
            print("  %-26s %-46s mine %-8s leg226 %-8s %s"
                  % (name, k, v["mine"], v["leg226"],
                     "EXACT" if v["exact"] else "MISMATCH"))
    print("  a=1.50: %d/%d grids accepted post-repair (leg 226: %d); pre-repair "
          "spread %.6f vs %.6f"
          % (mine150["n_grids_accepted_post_repair"], len(rows150),
             t150["n_grids_accepted_post_repair"],
             mine150["pre_repair_relative_spread"],
             t150["pre_repair_relative_spread"]))
    print("  GATE: %s" % data["gate"]["answer"])
    print("\n[done] wrote %s  (%.1f s)" % (OUT, time.time() - t_start))


if __name__ == "__main__":
    if os.environ.get("PNRV_ADDENDUM") == "1":
        addendum()
    else:
        main()
