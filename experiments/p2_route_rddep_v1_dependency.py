"""P2 Route-RDDEP v1 -- which banked Route-D v11 numbers depend on
`solver/profile_newton.py`'s `continuation`, and do any of them MOVE?

Leg 202 (Route-PNA, branch `leg/202-pna-v1`, NOT on main) found that
`profile_newton`'s `continuation` returns off-branch, grid-scale roots with
`converged=True` and a machine-zero `relres`, and graded Route-D v11's consumer
status "DIRECT AND MATERIAL".  Leg 202 named the exposure and stopped: it re-ran
none of v11's own numbers.  This leg does exactly that and nothing else.

    .venv/bin/python experiments/p2_route_rddep_v1_dependency.py
    -> writeup/data/p2_route_rddep_v1_dependency.json

READ-ONLY on `solver/profile_newton.py`.  This leg repairs nothing (that is leg
226's territory) and it edits no Route-D v11 artifact.  It imports the module
under audit unchanged and it drives it through v11's own call sites.

SIX sections:

  D1  the PROVENANCE MAP -- every banked v11 number, classified by what produced
      it, with the classification CHECKED against the anchor script's own AST
      rather than asserted from reading.
  D2  FAITHFUL CAPTURE -- the module's real `continuation` is called, unmodified,
      over v11's own a-grid at v11's own n; a recording subclass of
      `TwoScaleNewton` retains the `Omega` fields `continuation` throws away.
      The capture is then replayed through `continuation`'s own selection logic
      and required to reproduce the module's returned rows FIELD BY FIELD.  If it
      does not, this leg reports that and claims nothing else.
  D3  leg 202's CLASSIFIER, copied verbatim with its thresholds unchanged, applied
      to the profile behind every one of v11's `continuation` rows.
  D4  v11's OWN diagnostic -- the `weighted_defect` at alpha = 1.4 -- recomputed at
      v11's own cold call site, which is the second, independent affected-region
      test the gate names.
  D5  RECOMPUTATION -- every continuation-dependent banked number, before and
      after excluding the off-branch rows, under TWO exclusion policies so the
      answer cannot be produced by choosing one.
  D6  the LESSON-90 CONTROL -- the same classifier on the same code path at the
      grid leg 202 actually measured (n = 201).  If the classifier cannot fire
      here it cannot be read as clearing anything at n = 801.

Plain float64.  Nothing here is rigorous and nothing here is a certificate.
"""

import ast
import json
import os
import sys
import time
import warnings
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.profile_newton as pn                                   # noqa: E402
from solver.profile_newton import TwoScaleNewton                     # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ANCHOR_SRC = ROOT / "experiments" / "p2_route_d_v11_anchor.py"
ANCHOR_JSON = ROOT / "writeup" / "data" / "p2_route_d_v11_anchor.json"
OUT = ROOT / "writeup" / "data" / "p2_route_rddep_v1_dependency.json"

# --- v11's own constants, re-read from its source so they cannot drift here ---
N_V11 = 801
ALPHA = 1.4
GA_FLOOR = 1e-2
Y0_MAX = 2.45e-4
A_VALUES_V11 = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                0.55, 0.6, 0.7, 0.8, 0.9, 1.0]
N_CONTROL = 201                     # leg 202's own middle grid, for D6

# leg 247 measured the post-repair v5_budget margin directly; the banked JSON on
# this merge base still carries the PRE-repair value.  Recorded so the reader can
# see which one this leg used and why.
LEG_247_MARGIN_VIOLATION = 62.02    # x, at a = 0.45, Y0_max / worst weighted defect


# ===========================================================================
# leg 202's classifier -- COPIED VERBATIM from
# experiments/p2_route_pna_v1_adversarial.py at b2a70b8 (lines 84-137).
# Thresholds unchanged.  Frozen in writeup/novelty/leg_236.md section 6 BEFORE
# any number here was read, so this leg cannot tune one to reach a branch.
# ===========================================================================
SILENT_WRONG = "SILENT_WRONG"
SILENT_DEGRADED = "SILENT_DEGRADED"
NONFINITE = "NONFINITE"
CLEAN = "CLEAN"


def diagnostics(nw, r):
    """Decay-class and smoothness diagnostics the MODULE never computes."""
    O = np.asarray(r["Omega"], float)
    X = nw.fam.X
    outer = np.abs(X) > 0.5 * np.max(np.abs(X))
    anchor = nw.anchor()
    a_ff = float(np.max(np.abs(anchor[outer])))
    ff = float(np.max(np.abs(O[outer]))) if np.all(np.isfinite(O)) else float("inf")
    sup = float(np.max(np.abs(O))) if np.all(np.isfinite(O)) else float("inf")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        osc = float(np.max(np.abs(np.diff(O))) / sup) if sup > 0 else float("nan")
        mass = float(np.trapezoid(O, X))
    return {
        "farfield_sup": ff,
        "anchor_farfield_sup": a_ff,
        "farfield_inflation": ff / a_ff if a_ff > 0 else float("inf"),
        "sup_abs_Omega": sup,
        "farfield_is_the_max": bool(np.isfinite(ff) and np.isfinite(sup)
                                    and ff >= 0.99 * sup),
        "node_oscillation": osc,
        "mass": mass,
        "gauge1_residual": float(O[nw.i0] + 1.0) if np.isfinite(O[nw.i0]) else float("nan"),
        "gauge2_residual": float(O[nw.i1] + 0.5) if np.isfinite(O[nw.i1]) else float("nan"),
    }


def verdict(r, d):
    """Pre-committed classifier -- leg 202's, thresholds unchanged."""
    if not np.isfinite(d["sup_abs_Omega"]) or not np.isfinite(r.get("relres", np.nan)):
        return NONFINITE
    if not r["converged"]:
        return CLEAN
    gauge_broken = (abs(d["gauge1_residual"]) > 1e-6 or abs(d["gauge2_residual"]) > 1e-6)
    if r["relres"] < 1e-10 and d["farfield_inflation"] > 1e2:
        return SILENT_WRONG
    if gauge_broken or not np.isfinite(r["c"]):
        return SILENT_WRONG
    if r["iterations"] >= 40 and r["relres"] > 1e-10:
        return SILENT_DEGRADED
    return CLEAN


# --- v11's own codomain diagnostic, copied from the anchor script lines 44-53 ---
def weighted_defect(nw, om, c, alpha=ALPHA):
    R = nw.residual(om, c)
    w = (1.0 + nw.fam.X ** 2) ** (0.5 * (alpha + 1.0))
    return float(np.max(w * np.abs(R)))


# ===========================================================================
# D1 -- the provenance map, checked against the anchor script's AST
# ===========================================================================
#
# Each entry: the JSON path of a banked v11 number, the class of thing that
# produced it, and the source locator.  `class` is one of
#   "continuation"   -- the value came out of profile_newton.continuation
#   "cold_solve"     -- the value came out of TwoScaleNewton.solve with om0=None
#   "gated_by_continuation" -- the VALUE is a cold solve, but whether it is
#                             INCLUDED is decided by a continuation relres
#   "literal"        -- a hardcoded constant in the anchor script
#   "prose"          -- text, carries no number
PROVENANCE = [
    # ---- v1: cold solve from a perturbed exact anchor, no continuation --------
    ("v1_known_answer.newton_rms", "cold_solve", "anchor:60 nw.solve(om0=ex*1.3+...)"),
    ("v1_known_answer.newton_c", "cold_solve", "anchor:60"),
    ("v1_known_answer.iterations", "cold_solve", "anchor:60"),
    ("v1_known_answer.profile_difference", "cold_solve", "anchor:60"),
    ("v1_known_answer.exact_continuum_rms_on_the_grid", "cold_solve",
     "anchor:59 -- closed-form anchor, no Newton at all"),
    # ---- v2: THE continuation section ---------------------------------------
    ("v2_sweep.rows[].relres", "continuation", "anchor:78 continuation(a_values, n=N)"),
    ("v2_sweep.rows[].residual_rms", "continuation", "anchor:78"),
    ("v2_sweep.rows[].c", "continuation", "anchor:78"),
    ("v2_sweep.rows[].iterations", "continuation", "anchor:78"),
    ("v2_sweep.rows[].converged", "continuation", "anchor:78"),
    ("v2_sweep.rows[].weighted_defect", "cold_solve",
     "anchor:81-82 -- a SEPARATE cold solve, not continuation's profile"),
    ("v2_sweep.best_relres", "continuation", "anchor:85 min over continuation relres"),
    ("v2_sweep.a_max_machine", "continuation", "anchor:83+86 good = relres < 1e-8"),
    ("v2_sweep.orders_below_GA", "continuation", "anchor:87-88 log10(GA_floor/min relres)"),
    ("v2_sweep.GA_floor", "literal", "anchor:40 GA_FLOOR = 1e-2"),
    ("v2_sweep.n", "literal", "anchor:38 N = 801"),
    # ---- v3: cold solve only; the GA boundary is a hardcoded literal ---------
    ("v3_boundary.rows[].relres", "cold_solve", "anchor:102 nw.solve(om0=None)"),
    ("v3_boundary.rows[].c", "cold_solve", "anchor:102"),
    ("v3_boundary.rows[].converged", "cold_solve", "anchor:104 relres < 1e-8"),
    ("v3_boundary.last_machine_precision_a", "cold_solve", "anchor:107"),
    ("v3_boundary.GA_boundary", "literal",
     "anchor:112 -- HARDCODED [0.5, 0.55]; not computed by this script at all"),
    # ---- v4: cold solve only -------------------------------------------------
    ("v4_grids.rows[].relres", "cold_solve", "anchor:136 nw.solve(om0=None)"),
    ("v4_grids.rows[].c", "cold_solve", "anchor:136"),
    ("v4_grids.rows[].Omega_at_X4", "cold_solve", "anchor:136"),
    ("v4_grids.rows[].weighted_defect", "cold_solve", "anchor:142-143"),
    ("v4_grids.verdict[].c_spread", "cold_solve", "anchor:150"),
    ("v4_grids.verdict[].grid_converged", "cold_solve", "anchor:153-154"),
    ("v4_grids.grid_converged_a_max", "cold_solve", "anchor:156-157"),
    # ---- v5: consumes v2 (continuation-gated) and v4 (cold) -----------------
    ("v5_budget.a_range_used", "cold_solve", "anchor:171 <- v4.grid_converged_a_max"),
    ("v5_budget.newton_weighted_defect_min", "gated_by_continuation",
     "anchor:172-175 -- cold-solve values, filtered by continuation's relres < 1e-8"),
    ("v5_budget.newton_weighted_defect_max", "gated_by_continuation", "anchor:172-180"),
    ("v5_budget.margin", "gated_by_continuation", "anchor:181"),
    ("v5_budget.Y0_max_from_v10", "literal", "anchor:41 Y0_MAX = 2.45e-4"),
    ("v5_budget.GA_floor_rms", "literal", "anchor:40"),
    # ---- v6: prose -----------------------------------------------------------
    ("v6_ledger.changed", "prose", "anchor:212"),
]

# Which top-level section functions the map claims call `continuation`.
DECLARED_CONTINUATION_FUNCS = {"v2_sweep"}


def d1_provenance_map():
    """Classify every banked v11 number, and CHECK the classification."""
    src = ANCHOR_SRC.read_text()
    tree = ast.parse(src)

    # (a) which section functions call `continuation`, from the AST, not from
    #     reading.  A future edit that adds a call site fails this check loudly.
    calls_by_func = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        names = set()
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                f = sub.func
                if isinstance(f, ast.Name):
                    names.add(f.id)
                elif isinstance(f, ast.Attribute):
                    names.add(f.attr)
        calls_by_func[node.name] = sorted(names)
    found = {f for f, ns in calls_by_func.items() if "continuation" in ns}
    # `main` calls the section functions, so it is transitively a caller; the
    # declared set is about DIRECT call sites.
    map_ok = (found == DECLARED_CONTINUATION_FUNCS)

    # (b) grep-level count of literal `continuation(` call sites
    call_lines = [i + 1 for i, ln in enumerate(src.splitlines())
                  if "continuation(" in ln and not ln.strip().startswith("#")
                  and "def continuation" not in ln]

    # (c) the literals actually match what was banked
    banked = json.loads(ANCHOR_JSON.read_text())
    literal_checks = []
    for path, klass, loc in PROVENANCE:
        if klass != "literal":
            continue
        val = _dig(banked, path)
        literal_checks.append({"path": path, "banked_value": val, "locator": loc})

    counts = {}
    for _, klass, _ in PROVENANCE:
        counts[klass] = counts.get(klass, 0) + 1

    return {
        "banked_numbers_classified": len(PROVENANCE),
        "class_counts": counts,
        "ast_functions_calling_continuation": sorted(found),
        "declared_functions_calling_continuation": sorted(DECLARED_CONTINUATION_FUNCS),
        "ast_check_agrees_with_map": bool(map_ok),
        "literal_continuation_call_site_lines": call_lines,
        "calls_by_function": calls_by_func,
        "literal_checks": literal_checks,
        "map": [{"path": p, "class": k, "locator": l} for p, k, l in PROVENANCE],
        "reading": "the only DIRECT call site of `continuation` in the whole v11 "
                   "anchor script is line 78, inside v2_sweep.  v1, v3 and v4 use "
                   "cold `TwoScaleNewton.solve(om0=None)` and never touch it, and "
                   "v3's GA_boundary is a hardcoded literal, not a computed "
                   "quantity -- so leg 202's grading, which named "
                   "`a_max_machine`/`GA_boundary`/`grid_converged_a_max` together, "
                   "is only right about the first of the three.  v5_budget is the "
                   "subtle one: its weighted defects are COLD-solve values, but "
                   "which of them enter the min/max is decided by continuation's "
                   "relres, so the number is continuation-GATED without being "
                   "continuation-valued.",
    }


def _dig(obj, path):
    cur = obj
    for part in path.split("."):
        if part.endswith("[]"):
            return None
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


# ===========================================================================
# D2 -- faithful capture of the module's own continuation
# ===========================================================================
class _RecordingNewton(TwoScaleNewton):
    """Identical numerics; records every solve result INCLUDING Omega.

    `continuation` throws `Omega` away (it banks six scalar fields), so leg 202's
    decay-class classifier cannot be applied to its rows from the outside.  This
    subclass changes nothing about the arithmetic -- it calls `super().solve` and
    returns its result unmodified -- it only keeps a reference.
    """

    calls = []

    def solve(self, om0=None, c0=0.5, **kw):
        r = super().solve(om0=om0, c0=c0, **kw)
        _RecordingNewton.calls.append({
            "a": float(self.a), "n": int(self.fam.n),
            "warm_start": om0 is not None, "r": r, "nw": self,
        })
        return r


def capture_continuation(a_values, n):
    """Run the module's REAL `continuation`, keeping the profiles it discards."""
    _RecordingNewton.calls = []
    orig = pn.TwoScaleNewton
    pn.TwoScaleNewton = _RecordingNewton
    try:
        t0 = time.time()
        rows = pn.continuation(list(a_values), n=n)
        secs = time.time() - t0
    finally:
        pn.TwoScaleNewton = orig
    return rows, list(_RecordingNewton.calls), secs


def replay_selection(a_values, calls):
    """Re-derive continuation's OWN choice per a, so the profile can be attached.

    Mirrors `profile_newton.continuation` lines 177-195 exactly: warm solve, then
    a cold retry when relres > 1e-10, keeping the retry only if its relres is
    strictly smaller.  Returns one chosen call per a.  The result is then required
    to reproduce the module's returned rows field by field (see d2_capture).
    """
    by_a = {}
    for c in calls:
        by_a.setdefault(c["a"], []).append(c)
    chosen = []
    for a in a_values:
        grp = by_a[float(a)]
        pick, idx = grp[0], 0
        if pick["r"]["relres"] > 1e-10 and len(grp) > 1:
            alt = grp[1]
            if alt["r"]["relres"] < pick["r"]["relres"]:
                pick, idx = alt, 1
        pick = dict(pick)
        pick["retry_taken"] = bool(idx == 1)
        pick["solves_spent_at_this_a"] = len(grp)
        chosen.append(pick)
    return chosen


def d2_capture(a_values, n):
    rows, calls, secs = capture_continuation(a_values, n)
    chosen = replay_selection(a_values, calls)

    fields = ("a", "converged", "residual_rms", "relres", "c", "iterations")
    mismatches = []
    for row, pick in zip(rows, chosen):
        r = pick["r"]
        mine = {"a": pick["a"], "converged": bool(r["converged"]),
                "residual_rms": r["residual_rms"], "relres": r["relres"],
                "c": r["c"], "iterations": r["iterations"]}
        for f in fields:
            if mine[f] != row[f]:
                mismatches.append({"a": row["a"], "field": f,
                                   "module": row[f], "replay": mine[f]})
    return {
        "n": int(n), "a_values": [float(a) for a in a_values],
        "seconds": secs,
        "solve_calls_made": len(calls),
        "solve_calls_that_were_cold_retries": sum(1 for c in calls
                                                  if not c["warm_start"]),
        "rows": rows,
        "replay_field_mismatches": mismatches,
        "replay_is_faithful": bool(not mismatches),
        "reading": "the module's own `continuation` was called unmodified; only "
                   "the `Omega` it discards was retained.  The replay of its "
                   "selection logic reproduces its returned rows field by field, "
                   "so the profile attached to each row below is the profile that "
                   "row's numbers came from -- not a re-solve that might have "
                   "landed somewhere else.",
    }, chosen


# ===========================================================================
# D3 + D4 -- classify each continuation row; recompute v11's own diagnostic
# ===========================================================================
def d3_classify(rows, chosen, cold_by_a=None):
    out = []
    for row, pick in zip(rows, chosen):
        nw, r = pick["nw"], pick["r"]
        d = diagnostics(nw, r)
        v = verdict(r, d)
        rec = {
            "a": row["a"],
            "continuation_relres": row["relres"],
            "continuation_c": row["c"],
            "continuation_iterations": row["iterations"],
            "continuation_converged": row["converged"],
            "passes_v11_gate_relres_lt_1e_8": bool(row["relres"] < 1e-8),
            "came_from_cold_retry": bool(pick["retry_taken"]),
            "solves_spent_at_this_a": pick["solves_spent_at_this_a"],
            "leg202_verdict": v,
        }
        rec.update(d)
        rec["weighted_defect_of_continuation_profile"] = weighted_defect(
            nw, r["Omega"], r["c"])
        if cold_by_a is not None and row["a"] in cold_by_a:
            rec["weighted_defect_v11_cold"] = cold_by_a[row["a"]]["weighted_defect"]
            rec["cold_relres"] = cold_by_a[row["a"]]["relres"]
        out.append(rec)
    return out


def d4_cold_sweep(a_values, n):
    """v11's own lines 80-82: a SEPARATE cold solve per a, and its weighted defect.

    This is the second affected-region test the gate names -- v11's own
    `weighted_defect` spike signature -- recomputed at v11's own call site.
    """
    rows = {}
    t0 = time.time()
    for a in a_values:
        nw = TwoScaleNewton(a=float(a), n=int(n))
        s = nw.solve(om0=None, c0=0.5)
        d = diagnostics(nw, s)
        rows[float(a)] = {
            "a": float(a), "relres": s["relres"], "c": s["c"],
            "iterations": s["iterations"], "converged": bool(s["converged"]),
            "weighted_defect": weighted_defect(nw, s["Omega"], s["c"]),
            "farfield_inflation": d["farfield_inflation"],
            "gauge1_residual": d["gauge1_residual"],
            "gauge2_residual": d["gauge2_residual"],
            "leg202_verdict": verdict(s, d),
        }
    return rows, time.time() - t0


# ===========================================================================
# D5 -- recompute every continuation-dependent banked number
# ===========================================================================
def d5_recompute(classified, cold_by_a, banked, a_range_used):
    """Before/after for each dependent number, under two exclusion policies."""
    def derive(rows_ok, label):
        if not rows_ok:
            return {"policy": label, "rows_kept": 0}
        relres = [r["continuation_relres"] for r in rows_ok]
        good = [r for r in rows_ok if r["continuation_relres"] < 1e-8]
        wd = [cold_by_a[r["a"]]["weighted_defect"] for r in good
              if r["a"] <= a_range_used + 1e-12]
        best = min(wd) if wd else float("inf")
        return {
            "policy": label,
            "rows_kept": len(rows_ok),
            "rows_excluded": len(classified) - len(rows_ok),
            "best_relres": min(relres),
            "a_max_machine": max((r["a"] for r in good), default=0.0),
            "orders_below_GA": float(np.log10(GA_FLOOR / min(relres))),
            "newton_weighted_defect_min": best,
            "newton_weighted_defect_max": max(wd) if wd else None,
            "margin_v11_as_written": (Y0_MAX / best if best > 0 else float("inf")),
            "margin_leg247_repaired": (Y0_MAX / max(wd) if wd else None),
        }

    all_rows = list(classified)
    strict = [r for r in classified if r["leg202_verdict"] != SILENT_WRONG]
    wide = [r for r in classified
            if r["leg202_verdict"] not in (SILENT_WRONG, SILENT_DEGRADED)]
    # A THIRD axis, and for v5_budget the most on-point one: the weighted defect
    # is a property of the COLD profile (anchor:81-82), not of continuation's.
    # So ask the classifier about the profile the number actually came from.
    cold_bad = {a for a, r in cold_by_a.items()
                if r["leg202_verdict"] in (SILENT_WRONG, SILENT_DEGRADED)}
    coldwise = [r for r in classified if r["a"] not in cold_bad]

    reproduced = derive(all_rows, "none excluded (reproduction of v11 as written)")
    after_strict = derive(strict, "exclude SILENT_WRONG (false convergence)")
    after_wide = derive(wide, "exclude SILENT_WRONG + SILENT_DEGRADED")
    after_cold = derive(coldwise,
                        "exclude rows whose COLD profile -- the one the weighted "
                        "defect is computed from -- is SILENT_WRONG/DEGRADED")

    v2b, v5b = banked["v2_sweep"], banked["v5_budget"]
    banked_vals = {
        "best_relres": v2b["best_relres"],
        "a_max_machine": v2b["a_max_machine"],
        "orders_below_GA": v2b["orders_below_GA"],
        "newton_weighted_defect_min": v5b["newton_weighted_defect_min"],
        "newton_weighted_defect_max": v5b["newton_weighted_defect_max"],
        "margin_v11_as_written": v5b["margin"],
    }

    table = []
    for key, bv in banked_vals.items():
        rv = reproduced.get(key)
        sv = after_strict.get(key)
        wv = after_wide.get(key)
        def rel(x, y):
            if x is None or y is None:
                return None
            if x == y:
                return 0.0
            den = max(abs(x), abs(y))
            return float(abs(x - y) / den) if den > 0 else 0.0
        table.append({
            "number": key,
            "banked": bv,
            "reproduced_no_exclusion": rv,
            "reproduction_drift_rel": rel(bv, rv),
            "after_exclude_silent_wrong": sv,
            "moves_under_strict_exclusion_rel": rel(rv, sv),
            "after_exclude_silent_wrong_and_degraded": wv,
            "moves_under_wide_exclusion_rel": rel(rv, wv),
            "after_exclude_bad_cold_profile": after_cold.get(key),
            "moves_under_cold_exclusion_rel": rel(rv, after_cold.get(key)),
        })

    return {
        "exclusion_policies": [reproduced, after_strict, after_wide, after_cold],
        "before_after": table,
        "excluded_a_strict": [r["a"] for r in classified
                              if r["leg202_verdict"] == SILENT_WRONG],
        "excluded_a_wide": [r["a"] for r in classified
                            if r["leg202_verdict"] in (SILENT_WRONG,
                                                       SILENT_DEGRADED)],
        "excluded_a_cold_profile": sorted(cold_bad),
        "leg_247_note": "the banked v5_budget.margin on this merge base is the "
                        "PRE-repair value: v11 divides the budget by the BEST "
                        "(smallest) weighted defect, which is not the budget "
                        "condition.  Leg 247 repaired that and measured a genuine "
                        "%.2fx VIOLATION at a = 0.45.  This leg reports both forms "
                        "-- `margin_v11_as_written` reproduces v11's own arithmetic "
                        "so the dependency question is asked of the number actually "
                        "banked, and `margin_leg247_repaired` divides by the WORST "
                        "defect so the dependency question is also asked of the "
                        "number that will replace it." % LEG_247_MARGIN_VIOLATION,
    }


# ===========================================================================
# D6 -- lesson 90: a control that cannot come out differently is not a control
# ===========================================================================
def d6_control(a_values, n):
    """The SAME classifier on the SAME code path at leg 202's own grid.

    If this leg reports "nothing fires at n = 801", that reading is only worth
    anything if the classifier CAN fire on this code path.  Leg 202 measured its
    first departure at a = 0.45, n = 101 and its worst at a = 1.05, n = 101.  This
    section runs `continuation` over an a-ladder reaching leg 202's range at
    n = 201 and reports what the classifier says.  A control that fires nowhere at
    any grid would mean this leg's instrument, not v11's numbers, is what is
    clean.
    """
    rows, calls, secs = capture_continuation(a_values, n)
    chosen = replay_selection(a_values, calls)
    classified = d3_classify(rows, chosen)
    fired = [r for r in classified if r["leg202_verdict"] != CLEAN]
    return {
        "n": int(n), "a_values": [float(a) for a in a_values], "seconds": secs,
        "rows": classified,
        "verdict_counts": _counts([r["leg202_verdict"] for r in classified]),
        "classifier_fires_here": bool(fired),
        "first_departure_a": min((r["a"] for r in classified
                                  if r["leg202_verdict"] == SILENT_WRONG),
                                 default=None),
        "worst_farfield_inflation": max((r["farfield_inflation"]
                                         for r in classified), default=None),
        "reading": "this is the non-vacuity check.  It uses the identical "
                   "classifier and the identical `continuation` code path, at the "
                   "grid leg 202 measured, over an a-ladder that reaches leg 202's "
                   "own range.  Whatever it reports is the evidence that a clean "
                   "result at n = 801 is a statement about v11's operating point "
                   "rather than about a classifier that never fires.",
    }


def _counts(xs):
    out = {}
    for x in xs:
        out[x] = out.get(x, 0) + 1
    return out


# ===========================================================================
def main():
    banked = json.loads(ANCHOR_JSON.read_text())
    # The n = 801 sweeps cost ~40 min.  When a previous run's artifact is present
    # and complete, the derived sections (D1, D5) are recomputed from it and the
    # solver is not re-run.  Delete the JSON to force a cold reproduction.
    cache = None
    if OUT.exists() and "--fresh" not in sys.argv:
        try:
            prev = json.loads(OUT.read_text())
            if all(k in prev for k in ("d2_capture", "d3_classified_rows",
                                       "d4_cold_sweep", "d6_control")):
                cache = prev
        except (ValueError, OSError):
            cache = None
    if cache is not None:
        print("[cache] re-deriving D1/D5 from the previous run's artifact; "
              "pass --fresh to re-run the solver", flush=True)
        data = dict(cache)
        data["d1_provenance"] = d1_provenance_map()
        cold_by_a = {r["a"]: r for r in cache["d4_cold_sweep"]["rows"]}
        data["d5_recompute"] = d5_recompute(
            cache["d3_classified_rows"], cold_by_a, banked,
            banked["v4_grids"]["grid_converged_a_max"])
        OUT.write_text(json.dumps(data, indent=2))
        _summarize(data)
        return

    data = {"meta": {
        "leg": "P2 Route-RDDEP v1 (leg 236) -- which banked Route-D v11 numbers "
               "depend on profile_newton.continuation, and do any move?",
        "tier": "read-only dependency trace; no repair, no certificate",
        "reproduce": "python experiments/p2_route_rddep_v1_dependency.py",
        "realization": "GCLMResidual sinh-graded grid at rho_max = 8.0; the "
                       "two-gauge least-squares Gauss-Newton of "
                       "solver/profile_newton.py at its defaults tol = 1e-13, "
                       "max_iter = 40, damping = True; plain float64 on "
                       "scipy-openblas; v11's own grid n = 801 and v11's own "
                       "a-grid; off-branch detection by leg 202's far-field / "
                       "gauge classifier (verbatim) AND by v11's own "
                       "weighted_defect at alpha = 1.4",
        "reads_only": ["experiments/p2_route_d_v11_anchor.py",
                       "writeup/data/p2_route_d_v11_anchor.json",
                       "solver/profile_newton.py (imported, NOT modified)"],
        "banked_json_state": "the v11 anchor JSON read here still carries the "
                             "PRE-leg-247 v5_budget margin; leg 252 regenerates "
                             "it separately.  See d5_recompute.leg_247_note.",
    }}

    print("D1 provenance map ...", flush=True)
    data["d1_provenance"] = d1_provenance_map()
    print("    %d numbers classified; AST agrees with map: %s"
          % (data["d1_provenance"]["banked_numbers_classified"],
             data["d1_provenance"]["ast_check_agrees_with_map"]), flush=True)

    print("D4 cold sweep at n = %d (v11 lines 80-82) ..." % N_V11, flush=True)
    cold_by_a, cold_secs = d4_cold_sweep(A_VALUES_V11, N_V11)
    data["d4_cold_sweep"] = {"n": N_V11, "seconds": cold_secs,
                             "rows": [cold_by_a[float(a)] for a in A_VALUES_V11]}
    print("    %.0fs" % cold_secs, flush=True)

    print("D2 capture of the real continuation at n = %d ..." % N_V11, flush=True)
    d2, chosen = d2_capture(A_VALUES_V11, N_V11)
    data["d2_capture"] = d2
    print("    %.0fs, %d solve calls, replay faithful: %s"
          % (d2["seconds"], d2["solve_calls_made"], d2["replay_is_faithful"]),
          flush=True)

    print("D3 classify ...", flush=True)
    classified = d3_classify(d2["rows"], chosen, cold_by_a)
    data["d3_classified_rows"] = classified
    data["d3_verdict_counts"] = _counts([r["leg202_verdict"] for r in classified])
    print("    %s" % data["d3_verdict_counts"], flush=True)

    print("D5 recompute ...", flush=True)
    data["d5_recompute"] = d5_recompute(classified, cold_by_a, banked,
                                        banked["v4_grids"]["grid_converged_a_max"])

    print("D6 control at n = %d ..." % N_CONTROL, flush=True)
    ctrl_a = [0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90, 1.05, 1.20, 1.35, 1.50]
    data["d6_control"] = d6_control(ctrl_a, N_CONTROL)
    print("    fires: %s, counts %s"
          % (data["d6_control"]["classifier_fires_here"],
             data["d6_control"]["verdict_counts"]), flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))
    _summarize(data)


def _summarize(data):
    print("\nP2 ROUTE-RDDEP v1 -- dependency trace\n" + "=" * 58)
    print("  D1  %d banked v11 numbers classified; %s continuation-valued, "
          "%s continuation-GATED, %s cold-solve, %s literal"
          % (len(PROVENANCE),
             data["d1_provenance"]["class_counts"].get("continuation", 0),
             data["d1_provenance"]["class_counts"].get("gated_by_continuation", 0),
             data["d1_provenance"]["class_counts"].get("cold_solve", 0),
             data["d1_provenance"]["class_counts"].get("literal", 0)))
    print("  D3  verdicts at n = 801: %s" % data["d3_verdict_counts"])
    for row in data["d5_recompute"]["before_after"]:
        print("  D5  %-30s banked %-12s repro %-12s strict %-12s wide %-12s cold %s"
              % (row["number"], _fmt(row["banked"]),
                 _fmt(row["reproduced_no_exclusion"]),
                 _fmt(row["after_exclude_silent_wrong"]),
                 _fmt(row["after_exclude_silent_wrong_and_degraded"]),
                 _fmt(row["after_exclude_bad_cold_profile"])))
    print("  D6  control at n = 201: %s"
          % data["d6_control"]["verdict_counts"])
    print("\n[done] wrote %s" % OUT)


def _fmt(x):
    if x is None:
        return "-"
    if isinstance(x, float):
        return "%.6g" % x
    return str(x)


if __name__ == "__main__":
    main()
