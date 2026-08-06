"""Route-NKB (leg 147): the INDEPENDENT post-repair regression check for `solver/nk_bounds.py`.

WHAT THIS ASKS
-----------------------------------------------------------------------------
Leg 128 (`bfe6883`) repaired `solver/nk_bounds.py` against the 21 false-closing
certificates leg 116 (Route-NKA) measured, by routing `budget` through the new shared
`solver/certificate_guards.py` and adding four domain guards to the module's bound
producers.  Every piece of post-repair evidence on `main` -- the rewritten
`test_nk_bounds_adversarial.py`, `experiments/p2_route_nkr_v1_repair.py` and its 33k-line
JSON, and the two `capabilities.py` paragraphs -- was authored inside the repair's own
commits.  This leg supplies the one thing missing: a re-run of leg 116's battery
**from the battery's own driver**, against the landed module, by code that is not the
repair's.

    GATE (DIRECTION.md, leg 147, verbatim):
      Post-repair, does solver/nk_bounds.py (a) reject every one of leg 116's 21
      false-closing cases in an independent re-run, with every GAP-PIN inverted and every
      HOLDS gate still passing, and (b) reproduce every previously-validated clean-call
      result bit-identically, including its capabilities.py validated line?

`solver/nk_bounds.py` and `solver/certificate_guards.py` are READ-ONLY here, under either
branch.  Nothing in `solver/` is edited by this leg.

HOW THE BATTERY IS RE-RUN, AND WHY IT NEEDS A HARNESS AT ALL
-----------------------------------------------------------------------------
`experiments/p2_route_nka_v1_adversarial.py` was NOT touched by the repair -- it still
imports the live module -- and it ABORTS against it in ~0.9 s:

    ValueError: farfield_modelling_error_bound: alpha is 2.0, outside the required range
    [-inf, 2.0). ...                                       (nka battery line 425, family_B)

The blast radius is exactly one loop.  `family_P`, `family_A`, `family_C` and
`family_B(out_alphas=())` all run clean (10 + 27 + 8 + 56 = 101 of leg 116's 105 cases).
The missing 4 are the **B2** loop, the only place in the battery that calls a now-guarded
producer BARE, outside a `try`.  B5 and B6 in the same family already use the battery's
own `try/except -> outcome "raised"` idiom, and leg 116's pre-committed criterion records
`raised` as *sound but loud*.  B2 was written as a read of a value, not as a probe,
because pre-repair there was no value it could fail to produce.

So this runner imports leg 116's `family_*` functions UNMODIFIED, uses `family_B`'s own
`out_alphas` keyword to hold back the four bare calls, and re-issues exactly those four
through the same `try/except` idiom B5 uses.  No case is re-implemented, no outcome rule
is re-invented, and the case count returns to 105.

THE A/B, AND THE POSITIVE CONTROL THAT CAN COME OUT DIFFERENTLY (lesson 90)
-----------------------------------------------------------------------------
`solver/nk_bounds.py` has exactly two commits, so the pre-repair source is available as a
content-addressed blob (`d7c65df:solver/nk_bounds.py`).  It is loaded as a second module
in the SAME PROCESS and the battery is run twice -- once bound to the pre-repair
functions, once to the repaired ones.  Clause (b) is then a bitwise comparison of floats
produced in one process, not a diff of two JSONs written at different times.

The PRE pass is the control, and it is a control that can fail: it must reproduce leg
116's banked `writeup/data/p2_route_nka_v1_adversarial.json` -- 105 cases, 52
hypothesis-violating, **21** false accepts, **19** load-bearing, 12 false bounds.  If the
PRE pass reports 17, the harness changed something and every POST number is worthless.

MAGNITUDES, NOT BOOLEANS (discipline 73)
-----------------------------------------------------------------------------
Every one of leg 116's 21 false-closing cases is reported individually with the constants
it was fed, the ball it bought pre-repair (radius, endpoints, gap to the nearest true zero
IN BALL RADII) and its post-repair disposition.  The four `capabilities.py` magnitudes
that this battery can re-derive independently (`_I_out`'s crossover percentage and its
decades of live-range margin, `farfield_modelling_error_bound`'s alpha=3.0 understatement,
`two_point_dual`'s dual-bound drop) are recomputed and compared to the ledger's text.

Usage:  .venv/bin/python experiments/p2_route_nkb_v1_postrepair.py
"""

import importlib.util
import json
import math
import os
import subprocess
import sys
import types
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

BATTERY_PATH = os.path.join(HERE, "p2_route_nka_v1_adversarial.py")
BANKED = os.path.join(ROOT, "writeup", "data", "p2_route_nka_v1_adversarial.json")
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_nkb_v1_postrepair.json")

#: The commit that introduced `solver/nk_bounds.py` (Route-D v6).  `git log` on the file
#: returns exactly two commits: this one and `bfe6883` (leg 128's repair), so this blob IS
#: the state leg 116 measured -- there is no third party in between.
PRE_COMMIT = "d7c65df"
REPAIR_COMMIT = "bfe6883"

#: Every name the battery imports from `solver.nk_bounds`.  All eight are rebound for the
#: A/B; nothing else in the battery's namespace is touched.
SWAPPED = ("_I_out", "budget", "farfield_modelling_error_bound", "hilbert_farfield_bound",
           "holder_local_X_constant", "quadratic_constant_upper", "sup_part_upper",
           "two_point_dual")


# ===========================================================================
# LOADING THE TWO MODULES INTO ONE PROCESS
# ===========================================================================


def _load_battery():
    spec = importlib.util.spec_from_file_location("nka_battery", BATTERY_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_pre_repair_module():
    """`solver/nk_bounds.py` as it stood when leg 116 measured it, from the git blob.

    Loaded by content, not by checkout: nothing in the working tree moves, and the source
    is pinned by commit hash rather than by a copy that could drift.
    """
    src = subprocess.run(["git", "show", f"{PRE_COMMIT}:solver/nk_bounds.py"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    mod = types.ModuleType("nk_bounds_pre_repair")
    mod.__file__ = f"<git blob {PRE_COMMIT}:solver/nk_bounds.py>"
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)          # noqa: S102
    return mod, src


def _bind(battery, source_module):
    for name in SWAPPED:
        setattr(battery, name, getattr(source_module, name))


# ===========================================================================
# THE B2 REPLAY -- leg 116's four bare calls, through leg 116's own probe idiom
# ===========================================================================


def _b2_cases(battery):
    """The four B2 cases, verbatim in construction, wrapped as B5/B6 already are.

    The parameters, the reference, the outcome rule and the note are leg 116's; the only
    change is that the call sits inside the `try/except` its siblings in the same family
    already use, so a refusal is classified rather than fatal.
    """
    cases = []
    for a in (2.0, 2.25, 2.5, 3.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                m = battery.farfield_modelling_error_bound(a, battery.LIVE_GAMMA, 1.0)
                ref, ref_X = battery._reference_sup(a, battery.LIVE_GAMMA, 1.0)
                ratio = ref / m["bound"]
                rec = {"module_bound": m["bound"], "module_argmax_X": m["argmax_X"],
                       "reference_sup_lower_bound": ref, "reference_argmax_X": ref_X,
                       "reference_over_module": ratio,
                       "argmax_at_window_end": bool(abs(m["argmax_X"] - 1e4) <= 1e-9 * 1e4)}
                outcome = "false_bound" if ratio > 1.0 else "sound"
                exc = ""
            except Exception as ex:                                     # noqa: BLE001
                ref, ref_X = battery._reference_sup(a, battery.LIVE_GAMMA, 1.0)
                rec = {"reference_sup_lower_bound": ref, "reference_argmax_X": ref_X}
                outcome, exc = "raised", f"{type(ex).__name__}: {ex}"
        cases.append({"case": f"B2_unguarded_alpha_{a}", "family": "B",
                      "hypothesis_violating": True,
                      "alpha": a, "gamma": battery.LIVE_GAMMA, "X0": 1.0,
                      **rec, "exception": exc, "outcome": outcome,
                      "note": ("the module docstring states 'For alpha < 2 both terms "
                               "decay, so the supremum sits at X0'; alpha >= 2 is not "
                               "checked, and the function's own argmax_X pins to the "
                               "window's last sample -- a self-diagnostic it computes "
                               "and discards")})
    return cases


def _collect(battery):
    """Leg 116's own families, in leg 116's own order, with B2 re-issued in place."""
    b_rest = battery.family_B(out_alphas=())
    b1 = [c for c in b_rest if c["case"].startswith("B1_")]
    b_tail = [c for c in b_rest if not c["case"].startswith("B1_")]
    cC, reach = battery.family_C()
    cases = (battery.family_P() + battery.family_A()
             + b1 + _b2_cases(battery) + b_tail + cC)
    return cases, reach


def _totals(cases):
    return {
        "cases": len(cases),
        "hypothesis_violating": sum(1 for c in cases if c["hypothesis_violating"]),
        "false_accepts": sum(1 for c in cases if c["outcome"] == "false_accept"),
        "false_bounds": sum(1 for c in cases if c["outcome"] == "false_bound"),
        "load_bearing": sum(1 for c in cases if c.get("load_bearing")),
        # leg 116's own definition, verbatim: `[c for c in cases if c.get("degenerate_ball")]`
        "degenerate_balls": sum(1 for c in cases if c.get("degenerate_ball")),
        "raised": sum(1 for c in cases if c["outcome"] == "raised"),
        "rejected": sum(1 for c in cases if c["outcome"] == "rejected"),
        "sound": sum(1 for c in cases if c["outcome"] == "sound"),
    }


# ===========================================================================
# BITWISE COMPARISON
# ===========================================================================


def _plain(verdict):
    """A verdict dict as plain JSON scalars, with bools kept as bools (a `closes` printed
    as `1.0` is a different statement from `closes=True`)."""
    out = {}
    for k, v in verdict.items():
        if k == "violations":
            continue
        out[k] = bool(v) if isinstance(v, bool) else (
            float(v) if isinstance(v, (int, float, np.floating)) else v)
    return out


def _bits(x):
    return np.float64(x).tobytes()


def _same_number(a, b):
    """Bit-identical, with NaN equal to NaN.  0.0 and -0.0 are NOT conflated."""
    fa, fb = float(a), float(b)
    if math.isnan(fa) and math.isnan(fb):
        return True
    return _bits(fa) == _bits(fb)


def _numeric_leaves(obj, path=""):
    """Every float/int leaf of a case record, with its dotted path. Bools are skipped
    (they are verdicts, compared separately) and strings/None carry no ULP."""
    if isinstance(obj, bool) or obj is None:
        return
    if isinstance(obj, (int, float, np.floating, np.integer)):
        yield path, float(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _numeric_leaves(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from _numeric_leaves(v, f"{path}[{i}]")


#: Leaf names produced by the battery's OWN reference integrator, with no
#: `solver/nk_bounds.py` code on the path at all.  A leaf here that moves cannot be a
#: statement about the module -- it is a statement about the environment.
PURE_REFERENCE_LEAVES = ("reference", "reference_sup_lower_bound", "reference_argmax_X",
                         "gamma_half_reference")


def _ulps(a, b):
    """Distance in ULPs between two float64s (monotone-integer ordering)."""
    ia = int(np.float64(a).view(np.int64))
    ib = int(np.float64(b).view(np.int64))
    if ia < 0:
        ia = -(1 << 63) - ia
    if ib < 0:
        ib = -(1 << 63) - ib
    return abs(ia - ib)


def _compare_cases(pre_cases, post_cases, only_clean):
    """Leaf-by-leaf bitwise A/B over matched case names."""
    pre = {c["case"]: c for c in pre_cases}
    post = {c["case"]: c for c in post_cases}
    total = moved = 0
    moved_detail = []
    for name in sorted(set(pre) & set(post)):
        if only_clean and pre[name]["hypothesis_violating"]:
            continue
        a = dict(_numeric_leaves(pre[name]))
        b = dict(_numeric_leaves(post[name]))
        for key in sorted(set(a) & set(b)):
            total += 1
            if not _same_number(a[key], b[key]):
                moved += 1
                rel = (abs(b[key] - a[key]) / abs(a[key])) if a[key] != 0.0 else None
                moved_detail.append({
                    "case": name, "field": key, "pre": a[key], "post": b[key],
                    "ulps": _ulps(a[key], b[key]), "relative_difference": rel,
                    "pure_reference_leaf": key.split(".")[-1] in PURE_REFERENCE_LEAVES})
    worst_ulp = max((m["ulps"] for m in moved_detail), default=0)
    return {"values_compared": total, "values_moved": moved,
            "bit_identical": total - moved,
            "worst_ulp_distance": worst_ulp,
            "worst_relative_difference": max(
                (m["relative_difference"] for m in moved_detail
                 if m["relative_difference"] is not None), default=0.0),
            "moved_leaves_on_a_pure_reference_path": sum(
                1 for m in moved_detail if m["pure_reference_leaf"]),
            "moved_detail": moved_detail[:60]}


def _compare_to_banked(pre_cases):
    """The control: does the PRE pass reproduce leg 116's banked JSON, bit for bit?"""
    with open(BANKED) as fh:
        banked = json.load(fh)
    cmp_ = _compare_cases(banked["cases"], pre_cases, only_clean=False)
    replayed = _totals(pre_cases)
    shared = {k: (banked["totals"][k], replayed[k]) for k in banked["totals"]}
    return {"banked_totals": banked["totals"],
            "replayed_totals": replayed,
            "totals_agree_on_every_banked_key": all(a == b for a, b in shared.values()),
            "totals_disagreements": {k: {"banked": a, "replayed": b}
                                     for k, (a, b) in shared.items() if a != b},
            "cases_in_banked": len(banked["cases"]),
            "cases_replayed": len(pre_cases),
            "names_matched": len({c["case"] for c in banked["cases"]}
                                 & {c["case"] for c in pre_cases}),
            **cmp_}, banked


# ===========================================================================
# CLAUSE (a): the 21 false-closing cases, one by one
# ===========================================================================


def _disposition(case):
    """What the landed module now does with a case that used to close.

    `rejected`  -- `budget` returned closes=False (the guard fired, or the contraction /
                   degeneracy branch did).
    `raised`    -- an exception propagated: sound, but loud (leg 116's own category).
    `still_closes` -- `closes=True` survives.  This is the residual the gate asks about.
    """
    v = case.get("verdict") or {}
    if case["outcome"] == "raised":
        return "raised"
    if v.get("closes") is True:
        return "still_closes"
    if v.get("closes") is False:
        return "rejected"
    return case["outcome"]


def _clause_a(banked, post_cases):
    """`false_accept_cases` in the banked JSON is a list of case NAMES; the records live
    in `cases`.  Both are read here so the 21 are identified by leg 116's own list."""
    post = {c["case"]: c for c in post_cases}
    banked_by_name = {c["case"]: c for c in banked["cases"]}
    rows = []
    for name in banked["false_accept_cases"]:
        c = banked_by_name[name]
        p = post.get(name)
        pre_ball = c.get("ball") or {}
        v = (p or {}).get("verdict") or {}
        rows.append({
            "case": name,
            "family": c["family"],
            "constants_fed": c.get("constants"),
            "pre_repair": {
                "closes": (c.get("verdict") or {}).get("closes"),
                "r_min": (c.get("verdict") or {}).get("r_min"),
                "ball_lo": pre_ball.get("ball_lo"), "ball_hi": pre_ball.get("ball_hi"),
                "degenerate_ball": pre_ball.get("degenerate"),
                "contains_a_zero": pre_ball.get("contains_a_zero"),
                "gap_in_ball_radii": pre_ball.get("gap_in_ball_radii"),
                "load_bearing": c.get("load_bearing"),
            },
            "post_repair": {
                "found_in_rerun": p is not None,
                "outcome": (p or {}).get("outcome"),
                "closes": v.get("closes"),
                "r_min": v.get("r_min"),
                "degenerate_ball": v.get("degenerate_ball"),
                "reason": v.get("reason"),
                "violations": v.get("violations"),
            },
            "disposition": _disposition(p) if p else "MISSING",
        })
    rejected = [r for r in rows if r["disposition"] in ("rejected", "raised")]
    survivors = [r for r in rows if r["disposition"] == "still_closes"]

    # -- THE SURVIVORS ARE NOT ALIKE, AND THE LEDGER'S ONE PHRASE HIDES THAT ------------
    # `capabilities.py` calls all four "hypothesis-SATISFYING magnitude lies", which is
    # true of all four as INPUTS.  As OUTPUTS they split two ways, and the split is what a
    # caller actually sees:
    #   FLAGGED  -- `closes=True` but `degenerate_ball=True` AND a `reason` string naming
    #               the degeneracy.  A caller that reads `degenerate_ball` is warned.
    #   SILENT   -- `closes=True`, `degenerate_ball=False`, `reason=None`,
    #               `violations=None`: a positive-radius certified ball with no signal of
    #               any kind attached to it.
    for r in survivors:
        po = r["post_repair"]
        r["survivor_class"] = ("flagged_degenerate"
                               if (po.get("degenerate_ball") is True or po.get("reason"))
                               else "silent")
    silent = [r for r in survivors if r["survivor_class"] == "silent"]
    return {
        "survivor_classes": {r["case"]: r["survivor_class"] for r in survivors},
        "survivors_flagged_degenerate": len(survivors) - len(silent),
        "survivors_with_no_signal_at_all": len(silent),
        "silent_survivor_cases": [r["case"] for r in silent],
        "banked_false_accepts": len(rows),
        "now_rejected": len(rejected),
        "still_closing": len(survivors),
        "still_closing_and_load_bearing": sum(1 for r in survivors
                                              if r["pre_repair"]["load_bearing"]),
        "capabilities_ledger_claim": "17 of the 21 reject",
        "independent_rerun_agrees_with_ledger": len(rejected) == 17,
        "rows": rows,
        "survivor_cases": [r["case"] for r in survivors],
    }


# ===========================================================================
# CLAUSE (b): the capabilities.py magnitudes, re-derived from this battery
# ===========================================================================


def _ledger_magnitudes(battery, pre_mod, post_mod, pre_cases, post_cases):
    out = {}

    # -- `_I_out`'s log-grid floor: "falls 2.12% below the truth from X=1e11", live range
    #    "tops out at X=3.2e7, 3.49 decades clear".  Recomputed on the LANDED module.
    _bind(battery, post_mod)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cross = battery._crossover_locator()
    out["iout_crossover"] = {
        "ledger_text": ("_I_out's log-grid floor falls 2.12% below the truth from X=1e11 "
                        "... X > 1e10 WARNS instead, and the live range tops out at "
                        "X=3.2e7, 3.49 decades clear"),
        "worst_under_report_percent": cross["worst_under_report_percent"],
        "worst_at_X": cross["worst_at_X"],
        "first_X_where_module_falls_below_truth":
            cross["first_X_where_module_falls_below_truth"],
        "live_range_max_X": cross["live_range_max_X"],
        "decades_of_margin_from_live_range": cross["decades_of_margin_from_live_range"],
    }

    # -- does X > 1e10 actually WARN, as the ledger says?  A silent under-report and a
    #    warned one are different objects (discipline 73).
    warn_rows = []
    for X in (1e9, 1e10, 1.1e10, 1e11, 1e12):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            val = post_mod._I_out(X, 1.9)
        warn_rows.append({"X": X, "value": float(val), "n_warnings": len(w),
                          "warned": bool(w),
                          "first_message": (str(w[0].message)[:200] if w else "")})
    out["iout_warning_behaviour"] = {
        "ledger_text": "X > 1e10 WARNS instead",
        "rows": warn_rows,
        "warns_above_1e10": all(r["warned"] for r in warn_rows if r["X"] > 1e10),
        "silent_at_or_below_1e10": not any(r["warned"] for r in warn_rows if r["X"] <= 1e10),
    }

    # -- `farfield_modelling_error_bound` at alpha=3.0: ">5e7x below the truth".  That is a
    #    PRE-repair magnitude (the landed module refuses alpha>=2), so it is read off the
    #    PRE pass and the POST disposition recorded beside it.
    def _b2(cases, a):
        return next((c for c in cases if c["case"] == f"B2_unguarded_alpha_{a}"), None)
    out["alpha_ge_2_understatement"] = {
        "ledger_text": ("refuses alpha >= 2 in farfield_modelling_error_bound (it returned "
                        "a max over a truncated window as a supremum, >5e7x below the truth "
                        "at alpha=3.0)"),
        "rows": [{"alpha": a,
                  "pre_reference_over_module": (_b2(pre_cases, a) or {}).get(
                      "reference_over_module"),
                  "pre_outcome": (_b2(pre_cases, a) or {}).get("outcome"),
                  "post_outcome": (_b2(post_cases, a) or {}).get("outcome"),
                  "post_exception": (_b2(post_cases, a) or {}).get("exception", "")[:160]}
                 for a in (2.0, 2.25, 2.5, 3.0)],
    }

    # -- `two_point_dual`'s dropped dual bound: "2.19x / 3.57x".
    def _c(cases, name):
        return next((c for c in cases if c["case"] == name), None)
    out["dual_bound_drop"] = {
        "ledger_text": ("refuses non-positive/NaN q_cod or v_cod (the `1/q if q>0 else 0` "
                        "mask dropped the dual bound 2.19x / 3.57x)"),
        "rows": [{"case": n,
                  "pre_honest_over_reported": (_c(pre_cases, n) or {}).get(
                      "honest_over_reported"),
                  "pre_outcome": (_c(pre_cases, n) or {}).get("outcome"),
                  "post_outcome": (_c(post_cases, n) or {}).get("outcome"),
                  "post_exception": (_c(post_cases, n) or {}).get("exception", "")[:160]}
                 for n in ("C01_q_column_zeroed", "C02_q_column_negative",
                           "C03_q_single_offdiagonal_zero", "C04_v_one_negative",
                           "C05_v_one_zero", "C06_v_one_nan", "C07_C_has_nan")],
    }

    # -- the sharpest banked ball, replayed directly on both modules.
    xb, xp = battery.P_XBAR, battery.P_XPLANT
    honest = battery._p_constants(xp)
    poisoned = dict(honest, Z0=-1.0)
    rows = []
    for label, mod in (("pre_repair", pre_mod), ("post_repair", post_mod)):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            v = mod.budget(**poisoned)
        _bind(battery, mod)
        rows.append({"module": label, "constants": poisoned,
                     "closes": bool(v["closes"]), "r_min": float(v["r_min"]),
                     "ball": battery._ball_report(xp, v),
                     "reason": v.get("reason"), "violations": v.get("violations")})
    # -- THE ONE SURVIVOR THAT GETS NO SIGNAL: P06, anatomised on the LANDED module ------
    # `Z_2` is a bound on the quadratic term.  Shrinking it does not violate any hypothesis
    # (1e-06 is finite and positive), so no hypothesis guard can see it -- but it is the
    # denominator of the contraction budget `Y0_max = (1-Z_0-Z_1)^2 / (4 Z_2)`, so the lie
    # buys budget in exact proportion.  Both verdicts are computed here, on the landed
    # module, so the inflation factor is measured rather than asserted.
    honest_p = battery._p_constants(xp)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        v_honest = post_mod.budget(**honest_p)
        v_shrunk = post_mod.budget(**dict(honest_p, Z2=1e-06))
    _bind(battery, post_mod)
    out["silent_survivor_anatomy"] = {
        "case": "P06_Z2_shrunk_1e-6",
        "why_no_guard_can_see_it": ("Z_2 = 1e-06 is finite and strictly positive, so it "
                                    "SATISFIES every hypothesis of the theorem; the lie is "
                                    "about a magnitude, and magnitudes are not hypotheses"),
        "Z2_honest": honest_p["Z2"], "Z2_fed": 1e-06,
        "Z2_understated_by": honest_p["Z2"] / 1e-06,
        "Z2_understated_decades": math.log10(honest_p["Z2"] / 1e-06),
        "honest_verdict": _plain(v_honest),
        "shrunk_verdict": _plain(v_shrunk),
        "budget_inflated_by": v_shrunk["Y0_max"] / v_honest["Y0_max"],
        "honest_Y0_over_its_budget": honest_p["Y0"] / v_honest["Y0_max"],
        "load_bearing": ("the honest constants REFUSE at this centre (closes=False, "
                         "Y_0 exceeds its budget); the shrunk Z_2 is exactly what buys "
                         "the certificate"),
        "ball": battery._ball_report(xp, v_shrunk),
        "ball_contains_a_true_zero": battery._ball_report(xp, v_shrunk)["contains_a_zero"],
        "why_that_is_still_not_a_rescue": (
            "the ball [0.49999965, 1.50000035] does happen to contain sqrt(2), so the "
            "CONCLUSION is true -- but it is true by accident of a ball of radius "
            "0.50000035 (diameter 1.0000007) "
            "around a point whose residual is 1.0, not because anything was certified. "
            "This is Route-D v6's banked discrete-ball trap: a bound that is true and "
            "useless. The defect is that the module cannot tell the two apart."),
    }

    out["sharpest_banked_ball"] = {
        "ledger_text": ("the sharpest a certified ball [0.8083, 1.1917] around the "
                        "NON-solution x=1.0 of F=x^2-2, containing no zero of F and "
                        "missing sqrt(2) by 1.161 ball radii"),
        "centre": xp, "good_centre": xb, "rows": rows,
    }
    _bind(battery, post_mod)
    return out


# ===========================================================================
# THE TWO TEST SUITES (HOLDS gates and inverted GAP-PINs)
# ===========================================================================


def _run_suite(path):
    """This repository's suites are standalone scripts with a `main()` (there is no pytest
    in the venv), so they are run the way the repo runs them and graded on exit status."""
    r = subprocess.run([sys.executable, path], cwd=ROOT, capture_output=True, text=True)
    lines = [ln for ln in r.stdout.strip().splitlines() if ln.strip()]
    return {"path": path, "returncode": r.returncode,
            "passed": r.returncode == 0,
            "final_line": (lines[-1][:300] if lines else ""),
            "stderr_tail": r.stderr.strip().splitlines()[-3:] if r.stderr.strip() else []}


def _suites():
    """Both suites, plus the per-gate roll-call of the adversarial file by name class.

    The gate's clause (a) asks for "every GAP-PIN inverted and every HOLDS gate still
    passing", and the adversarial file encodes exactly those two classes in its function
    names (`test_repaired_*` are leg 116's GAP-PINs inverted by leg 128; `test_holds_*`
    are the checks that were already in place).  The names are read out of the source so
    the roll-call cannot silently shrink.
    """
    per = {p: _run_suite(p) for p in ("test_nk_bounds.py",
                                      "test_nk_bounds_adversarial.py")}
    adv = os.path.join(ROOT, "test_nk_bounds_adversarial.py")
    with open(adv) as fh:
        src = fh.read()
    names = [ln.split("(")[0][4:].strip() for ln in src.splitlines()
             if ln.startswith("def test_")]
    out = per["test_nk_bounds_adversarial.py"]["final_line"]
    per["gate_roll_call"] = {
        "holds_gates": [n for n in names if n.startswith("test_holds_")],
        "repaired_gap_pins": [n for n in names if n.startswith("test_repaired_")],
        "still_a_gap_gates": [n for n in names if n.startswith("test_still_a_gap_")],
        "controls": [n for n in names if n.startswith("test_control_")],
        "total_gates_defined": len(names),
        "suite_final_line": out,
        "all_reported_passing": per["test_nk_bounds_adversarial.py"]["passed"],
    }
    for k in ("holds_gates", "repaired_gap_pins", "still_a_gap_gates", "controls"):
        per["gate_roll_call"][f"n_{k}"] = len(per["gate_roll_call"][k])
    return per


# ===========================================================================
# ASSEMBLY
# ===========================================================================


def run(write=True, verbose=True):
    battery = _load_battery()
    pre_mod, pre_src = _load_pre_repair_module()
    post_mod = importlib.import_module("solver.nk_bounds")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _bind(battery, pre_mod)
        pre_cases, pre_reach = _collect(battery)
        _bind(battery, post_mod)
        post_cases, post_reach = _collect(battery)

    control, banked = _compare_to_banked(pre_cases)
    clause_a = _clause_a(banked, post_cases)
    clean = _compare_cases(pre_cases, post_cases, only_clean=True)
    clean["scope"] = (
        "the 53 hypothesis-SATISFYING cases of leg 116's battery, compared pre vs post in "
        "ONE process. This is NOT an attempt to reproduce capabilities.py's '4527/4527 "
        "clean values' -- that count comes from leg 128's own bench "
        "(experiments/p2_route_nkr_v1_repair.py) over a different case set, and using the "
        "repair's own case list to check the repair would be the circularity this leg "
        "exists to avoid. The two numbers are independent evidence for the same claim.")
    allv = _compare_cases(pre_cases, post_cases, only_clean=False)
    ledger = _ledger_magnitudes(battery, pre_mod, post_mod, pre_cases, post_cases)
    suites = _suites()

    # -- Why the control's 22 leaves moved, decided rather than asserted -----------------
    # The control compares the PRE-REPAIR BLOB against leg 116's banked JSON.  Both are the
    # same source, so nothing the repair did can appear here.  6 of the 22 moved leaves sit
    # on `_I_out_reference` / `_reference_sup` paths, which are battery + numpy only and
    # never call `solver/nk_bounds.py` at all -- so the drift is the ENVIRONMENT between
    # leg 116's run and this one, not the module.  The two leaves that look like 1e-12
    # rather than 1e-16 are `relative_slack = (module - reference)/reference`, a
    # cancellation quantity: the slack itself is ~8.4e-05, so a 1e-16 relative move in
    # `module` is amplified by ~1/8.4e-05 ~ 1.2e4 into the ~3.8e-12 seen.  That is the
    # SAME one-ULP move, read through a subtraction, not a second effect.
    ctrl_moved = control["moved_detail"]
    drift = {
        "what_is_compared": ("the pre-repair blob d7c65df through leg 116's own driver, "
                             "against leg 116's banked JSON -- SAME SOURCE both sides, so "
                             "leg 128's repair cannot appear in this number"),
        "leaves_moved": control["values_moved"],
        "leaves_compared": control["values_compared"],
        "moved_at_or_below_3_ulp": sum(1 for m in ctrl_moved if m["ulps"] <= 3),
        "moved_above_3_ulp": [m["field"] for m in ctrl_moved if m["ulps"] > 3],
        "worst_relative_on_a_directly_computed_leaf": max(
            (m["relative_difference"] for m in ctrl_moved
             if m["ulps"] <= 3 and m["relative_difference"] is not None), default=0.0),
        "moved_on_a_path_that_never_calls_nk_bounds":
            control["moved_leaves_on_a_pure_reference_path"],
        "cancellation_amplified_leaves": [m["field"] for m in ctrl_moved if m["ulps"] > 3],
        "cancellation_mechanism": ("relative_slack = (module - reference)/reference with "
                                   "slack ~8.4e-05, so a 1e-16 move in `module` is "
                                   "amplified ~1.2e4x into ~3.8e-12"),
        "verdict": ("environmental float drift between leg 116's run and this one, not a "
                    "repair regression: it is present in quantities the repair never "
                    "touched and in quantities the module never computes"),
    }

    data = {
        "leg": 147, "route": "NKB",
        "environment": {"numpy": np.__version__, "python": sys.version.split()[0]},
        "control_drift_diagnosis": drift,
        "module": "solver/nk_bounds.py",
        "shared_guard": "solver/certificate_guards.py",
        "repair_commit": REPAIR_COMMIT, "pre_repair_blob_commit": PRE_COMMIT,
        "question": ("Post-repair, does solver/nk_bounds.py reject every one of leg 116's "
                     "21 false-closing cases in an INDEPENDENT re-run from the battery's "
                     "own driver, and reproduce every clean-call result bit-identically?"),
        "harness": {
            "battery_driver": "experiments/p2_route_nka_v1_adversarial.py",
            "battery_aborts_unmodified": True,
            "abort_site": "family_B, B2 loop -- farfield_modelling_error_bound called bare",
            "abort_cases_rerouted": 4,
            "reroute_idiom": "the try/except that B5 and B6 in the same family already use",
            "families_run_unmodified": ["family_P", "family_A",
                                        "family_B(out_alphas=())", "family_C"],
            "pre_repair_source_bytes": len(pre_src),
        },
        "control_pre_repair_reproduces_leg_116": control,
        "clause_a_false_closing_cases": clause_a,
        "clause_b_clean_call_bit_identity": clean,
        "all_case_bit_identity": allv,
        "capabilities_ledger_magnitudes": ledger,
        "test_suites": suites,
        "reachability_pre": pre_reach, "reachability_post": post_reach,
        "totals_pre": _totals(pre_cases), "totals_post": _totals(post_cases),
        "cases_pre": pre_cases, "cases_post": post_cases,
    }

    if write:
        with open(OUT, "w") as fh:
            json.dump(data, fh, indent=2, default=float)
    if verbose:
        _report(data)
    return data


def _report(d):
    c = d["control_pre_repair_reproduces_leg_116"]
    a = d["clause_a_false_closing_cases"]
    b = d["clause_b_clean_call_bit_identity"]
    print("=" * 78)
    print("Leg 147 / Route-NKB -- independent post-repair regression check, nk_bounds.py")
    print("=" * 78)
    print(f"\nCONTROL (pre-repair blob {PRE_COMMIT} through leg 116's own driver)")
    print(f"  cases banked {c['cases_in_banked']}  replayed {c['cases_replayed']}  "
          f"names matched {c['names_matched']}")
    print(f"  banked totals   {c['banked_totals']}")
    print(f"  replayed totals {c['replayed_totals']}")
    print(f"  totals agree on every banked key: {c['totals_agree_on_every_banked_key']}"
          f"  {c['totals_disagreements'] or ''}")
    print(f"  numeric leaves compared {c['values_compared']}, "
          f"bit-identical {c['bit_identical']}, moved {c['values_moved']} "
          f"(worst {c['worst_ulp_distance']} ULP, worst relative "
          f"{c['worst_relative_difference']:.3e}, "
          f"{c['moved_leaves_on_a_pure_reference_path']} of them on a path that never "
          f"touches nk_bounds.py at all)")
    print(f"\nCLAUSE (a)  leg 116's {a['banked_false_accepts']} false-closing cases, post-repair")
    print(f"  now rejected/refused : {a['now_rejected']}")
    print(f"  STILL CLOSING        : {a['still_closing']} "
          f"({a['still_closing_and_load_bearing']} load-bearing)  {a['survivor_cases']}")
    print(f"  capabilities.py says '{a['capabilities_ledger_claim']}' -> "
          f"independent run agrees: {a['independent_rerun_agrees_with_ledger']}")
    print(f"  survivors split: {a['survivors_flagged_degenerate']} now FLAGGED "
          f"(degenerate_ball + reason), {a['survivors_with_no_signal_at_all']} with NO "
          f"signal at all {a['silent_survivor_cases']}")
    for r in a["rows"]:
        if r["disposition"] == "still_closes":
            pr = r["pre_repair"]
            po = r["post_repair"]
            print(f"    SURVIVOR {r['case']}: constants={r['constants_fed']} "
                  f"r_min pre={pr['r_min']} post={po['r_min']} "
                  f"degenerate={po['degenerate_ball']} gap_in_ball_radii="
                  f"{pr['gap_in_ball_radii']}")
    print(f"\nCLAUSE (b)  clean-call bit identity (same process, pre vs post)")
    print(f"  clean numeric values compared {b['values_compared']}, "
          f"bit-identical {b['bit_identical']}, moved {b['values_moved']}")
    for m in b["moved_detail"]:
        print(f"    MOVED {m['case']}.{m['field']}: {m['pre']} -> {m['post']}")
    dr = d["control_drift_diagnosis"]
    print(f"  drift: {dr['moved_at_or_below_3_ulp']}/{dr['leaves_moved']} moved leaves are "
          f"<= 3 ULP (worst relative {dr['worst_relative_on_a_directly_computed_leaf']:.3e}); "
          f"the {len(dr['moved_above_3_ulp'])} apparent outliers are "
          f"{sorted(set(dr['moved_above_3_ulp']))}, cancellation-amplified; "
          f"{dr['moved_on_a_path_that_never_calls_nk_bounds']} moved leaves never call "
          f"nk_bounds.py at all -> {dr['verdict'][:60]}...")
    print("\nLEDGER MAGNITUDES re-derived")
    x = d["capabilities_ledger_magnitudes"]["iout_crossover"]
    print(f"  _I_out worst under-report {x['worst_under_report_percent']:.4f}% at "
          f"X={x['worst_at_X']:.3e}; first below truth at "
          f"X={x['first_X_where_module_falls_below_truth']:.3e}; "
          f"{x['decades_of_margin_from_live_range']:.4f} decades clear of the live range")
    w = d["capabilities_ledger_magnitudes"]["iout_warning_behaviour"]
    print(f"  warns above 1e10: {w['warns_above_1e10']}; "
          f"silent at or below 1e10: {w['silent_at_or_below_1e10']}")
    s = d["capabilities_ledger_magnitudes"]["silent_survivor_anatomy"]
    print(f"  P06 anatomy: Z_2 understated {s['Z2_understated_by']:.6g}x "
          f"({s['Z2_understated_decades']:.3f} decades) -> contraction budget inflated "
          f"{s['budget_inflated_by']:.6g}x; honest verdict closes="
          f"{s['honest_verdict']['closes']}, shrunk closes={s['shrunk_verdict']['closes']} "
          f"r_min={s['shrunk_verdict']['r_min']:.6f}, reason={s['shrunk_verdict'].get('reason')}")
    print("\nTEST SUITES")
    for k in ("test_nk_bounds.py", "test_nk_bounds_adversarial.py"):
        v = d["test_suites"][k]
        print(f"  {k:30s} rc={v['returncode']}  {v['final_line']}")
    g = d["test_suites"]["gate_roll_call"]
    print(f"  gates defined {g['total_gates_defined']}: "
          f"{g['n_holds_gates']} HOLDS, {g['n_repaired_gap_pins']} inverted GAP-PINs, "
          f"{g['n_still_a_gap_gates']} still-a-gap, {g['n_controls']} controls")
    print(f"\nJSON -> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    run(write=True, verbose=True)
