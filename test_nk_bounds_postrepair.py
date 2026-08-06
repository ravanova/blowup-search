"""Leg 147 (Route-NKB): leg 116's battery, BANKED as a permanent regression suite.

WHAT THIS FILE IS FOR, AND HOW IT DIFFERS FROM THE TWO FILES BESIDE IT
-----------------------------------------------------------------------------
`test_nk_bounds.py`             -- Route-D's known-answer gates. Well-formed input only.
`test_nk_bounds_adversarial.py` -- leg 116's GAP-PINs, INVERTED by leg 128's own repair
                                   commit. Written by the repair, about the repair.
`test_nk_bounds_postrepair.py`  -- THIS FILE. Leg 147's independent re-run, pinned.

Leg 147's gate asked whether the landed `solver/nk_bounds.py` rejects **every one** of leg
116's 21 false-closing cases. It does not: **17 reject, 4 still close**, which is exactly
what `capabilities.py` claims and what an independent re-run through leg 116's OWN driver
confirms. The gate therefore answers **NO on clause (a)** and **YES on clause (b)**, and
the residue is pinned here so it cannot drift in either direction unnoticed:

  * if a future change makes the count WORSE (fewer than 17 reject, or a clean value
    moves), these gates fail -- that is the regression half;
  * if a future change makes it BETTER (a survivor starts rejecting), these gates ALSO
    fail, loudly, with the case named -- that is the point. A residue that silently
    improves is a residue nobody re-measured, and the next leg should be told.

`solver/nk_bounds.py` and `solver/certificate_guards.py` are NOT edited by leg 147, under
either branch of its gate.

THE SHARPEST PIN IN THIS FILE
-----------------------------------------------------------------------------
`capabilities.py` describes the 4 survivors with one phrase -- "hypothesis-SATISFYING
magnitude lies, which no hypothesis guard can detect". True of all four as INPUTS. As
OUTPUTS they split, and the split is what a caller actually sees:

  3 of 4  return `closes=True` **plus** `degenerate_ball=True` **plus** a `reason` string.
  1 of 4  -- `P06_Z2_shrunk_1e-6` -- returns a positive-radius certified ball with
          `degenerate_ball=False`, `reason=None`, `violations=None`: **no signal at all.**

`test_the_one_survivor_that_gets_no_signal` pins that asymmetry, because the one-phrase
ledger entry does not carry it.

Run:  .venv/bin/python test_nk_bounds_postrepair.py
"""

import json
import math
import os
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from solver.nk_bounds import _I_out, budget, two_point_dual   # noqa: E402

DATA = os.path.join(HERE, "writeup", "data", "p2_route_nkb_v1_postrepair.json")
BANKED_116 = os.path.join(HERE, "writeup", "data", "p2_route_nka_v1_adversarial.json")

#: Leg 116's 21 false-closing cases, and the disposition leg 147 measured for each.
#: Anything not listed here rejects.
SURVIVORS_FLAGGED = ("P02_Y0_fabricated_zero", "P09_Y0_tiny_fabricated",
                     "A05_Y0_zero_fabricated")
SURVIVOR_SILENT = "P06_Z2_shrunk_1e-6"
N_BANKED_FALSE_ACCEPTS = 21
N_NOW_REJECTING = 17

_FAILURES = []


def _check(name, ok, detail):
    status = "ok" if ok else "FAIL"
    print(f"[{status}] {name}: {detail}")
    if not ok:
        _FAILURES.append(name)


def _load():
    with open(DATA) as fh:
        return json.load(fh)


# ===========================================================================
# CONTROLS -- these must be able to come out differently (lesson 90)
# ===========================================================================


def test_control_the_honest_certificate_still_behaves_both_ways():
    """The substrate must still REFUSE at the planted non-solution and CLOSE at the good
    centre. If both came out the same, every gate below would be measuring nothing."""
    A = 1.0 / (2.0 * 1.4)
    plant = {"Y0": abs(A * (1.0 ** 2 - 2.0)), "Z0": abs(1.0 - A * 2.0 * 1.0),
             "Z1": 0.0, "Z2": abs(A * 2.0)}
    good = {"Y0": abs(A * (1.4 ** 2 - 2.0)), "Z0": abs(1.0 - A * 2.0 * 1.4),
            "Z1": 0.0, "Z2": abs(A * 2.0)}
    vp, vg = budget(**plant), budget(**good)
    _check("control_honest_certificate_both_ways",
           (vp["closes"] is False) and (vg["closes"] is True),
           f"planted x=1.0 closes={vp['closes']} (honest refusal), "
           f"good centre x=1.4 closes={vg['closes']} r_min={vg['r_min']:.8f}")


def test_control_a_hypothesis_violating_constant_is_still_refused():
    """The repair's core behaviour, exercised directly rather than via a JSON."""
    v = budget(Y0=0.05, Z0=-1.0, Z1=0.0, Z2=0.7142857142857143)
    ok = (v["closes"] is False) and bool(v.get("violations"))
    _check("control_negative_Z0_refused", ok,
           f"Z_0 = -1 -> closes={v['closes']}, violations={v.get('violations')}")


# ===========================================================================
# CLAUSE (a) -- the 21, pinned at 17 rejecting / 4 surviving
# ===========================================================================


def test_seventeen_of_leg_116s_twenty_one_false_closers_now_reject():
    d = _load()
    a = d["clause_a_false_closing_cases"]
    ok = (a["banked_false_accepts"] == N_BANKED_FALSE_ACCEPTS
          and a["now_rejected"] == N_NOW_REJECTING
          and a["still_closing"] == N_BANKED_FALSE_ACCEPTS - N_NOW_REJECTING)
    _check("seventeen_of_twenty_one_reject", ok,
           f"{a['now_rejected']}/{a['banked_false_accepts']} reject, "
           f"{a['still_closing']} still close "
           f"({a['still_closing_and_load_bearing']} load-bearing): "
           f"{a['survivor_cases']}")


def test_the_four_survivors_are_exactly_these_four_cases():
    """Named, not counted. A different four with the same total is a different module."""
    d = _load()
    got = set(d["clause_a_false_closing_cases"]["survivor_cases"])
    want = set(SURVIVORS_FLAGGED) | {SURVIVOR_SILENT}
    _check("survivors_named", got == want,
           f"survivors {sorted(got)}" + ("" if got == want else f" != expected {sorted(want)}"))


def test_the_one_survivor_that_gets_no_signal():
    """THE SHARPEST PIN. Three survivors are flagged; one is silent, and it is the one
    whose ball has a POSITIVE radius. Re-measured live, not read from the JSON."""
    honest = {"Y0": 0.35714285714285715, "Z0": 0.2857142857142857,
              "Z1": 0.0, "Z2": 0.7142857142857143}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        v_honest = budget(**honest)
        v_shrunk = budget(**dict(honest, Z2=1e-06))
    silent = (v_shrunk["closes"] is True
              and v_shrunk.get("degenerate_ball") is False
              and v_shrunk.get("reason") is None
              and not v_shrunk.get("violations"))
    load_bearing = v_honest["closes"] is False
    inflation = v_shrunk["Y0_max"] / v_honest["Y0_max"]
    ok = silent and load_bearing and math.isclose(inflation, 714285.7142857143, rel_tol=1e-9)
    _check("silent_survivor_P06", ok,
           f"Z_2 understated {honest['Z2'] / 1e-06:.6g}x (5.854 decades) turns an honest "
           f"REFUSAL into closes={v_shrunk['closes']} r_min={v_shrunk['r_min']:.8f}, "
           f"budget inflated {inflation:.6g}x, and it arrives with "
           f"degenerate_ball={v_shrunk.get('degenerate_ball')} "
           f"reason={v_shrunk.get('reason')} violations={v_shrunk.get('violations')} "
           f"-- no signal of any kind")


def test_the_three_flagged_survivors_do_carry_a_reason():
    """The other side of the same asymmetry: these three DO warn, so the silence of P06
    is a property of that case, not of the module's whole degenerate branch."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        v0 = budget(Y0=0.0, Z0=0.2857142857142857, Z1=0.0, Z2=0.7142857142857143)
        v1 = budget(Y0=1e-300, Z0=0.2857142857142857, Z1=0.0, Z2=0.7142857142857143)
        v2 = budget(Y0=0.0, Z0=0.0, Z1=0.3, Z2=1.0)
    flagged = [v for v in (v0, v1, v2)
               if v["closes"] is True and v["degenerate_ball"] is True and v.get("reason")]
    _check("three_flagged_survivors", len(flagged) == 3,
           f"{len(flagged)}/3 carry degenerate_ball=True with a reason; "
           f"r_min all exactly 0.0: {[v['r_min'] for v in (v0, v1, v2)]}")


# ===========================================================================
# CLAUSE (b) -- nothing clean moved
# ===========================================================================


def test_no_clean_call_moved_by_one_bit():
    d = _load()
    b = d["clause_b_clean_call_bit_identity"]
    ok = b["values_moved"] == 0 and b["values_compared"] >= 359
    _check("clean_calls_bit_identical", ok,
           f"{b['bit_identical']}/{b['values_compared']} clean numeric values "
           f"bit-identical at 0 ULP against the pre-repair blob, in one process; "
           f"{b['values_moved']} moved")


def test_the_pre_repair_control_reproduced_leg_116s_banked_counts():
    """If this fails, every number in this file is measuring the harness, not the module."""
    d = _load()
    c = d["control_pre_repair_reproduces_leg_116"]
    _check("pre_repair_control_reproduces_leg_116",
           c["totals_agree_on_every_banked_key"] and c["cases_replayed"] == 105,
           f"{c['cases_replayed']} cases replayed, totals agree on every banked key "
           f"({c['banked_totals']['false_accepts']} false accepts, "
           f"{c['banked_totals']['load_bearing']} load-bearing); "
           f"{c['bit_identical']}/{c['values_compared']} leaves bit-identical, "
           f"{c['values_moved']} moved at <= 3 ULP (environmental drift: "
           f"{c['moved_leaves_on_a_pure_reference_path']} of them never call nk_bounds.py)")


def test_the_ledger_magnitudes_reproduce():
    """`capabilities.py`'s own numbers for this module, re-derived independently."""
    d = _load()
    m = d["capabilities_ledger_magnitudes"]
    x = m["iout_crossover"]
    ok = (abs(x["worst_under_report_percent"] - 2.12) < 0.01
          and abs(x["decades_of_margin_from_live_range"] - 3.49) < 0.01
          and m["iout_warning_behaviour"]["warns_above_1e10"] is True
          and m["iout_warning_behaviour"]["silent_at_or_below_1e10"] is True)
    _check("ledger_magnitudes_reproduce", ok,
           f"_I_out under-reports {x['worst_under_report_percent']:.4f}% at "
           f"X={x['worst_at_X']:.2e} (ledger: 2.12%), live range "
           f"{x['decades_of_margin_from_live_range']:.4f} decades clear (ledger: 3.49), "
           f"warns above 1e10 and stays silent below")


def test_the_live_operating_range_is_still_silent_and_sound():
    """The load-bearing reassurance: the module's ACTUAL callers are nowhere near the
    residue. Measured live -- `_I_out` must not warn anywhere a caller evaluates."""
    live_max = 3.2e7
    warned = []
    for a in (1.1, 1.5, 1.9):
        for X in (1.0, 1e2, 1e4, 1e6, live_max):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                _I_out(X, a)
            if w:
                warned.append((a, X))
    _check("live_range_silent", not warned,
           f"0 warnings over 15 in-range (alpha, X) pairs up to X={live_max:.1e}; "
           f"the first under-report is at X=1e11, {math.log10(1e11 / live_max):.4f} "
           f"decades above the largest X any in-repo caller evaluates")


def test_two_point_dual_still_refuses_degenerate_weights():
    """One of the repair's non-`budget` guards, exercised directly rather than via JSON."""
    rng = np.random.default_rng(0)
    C = rng.normal(size=(1, 6))
    q = np.abs(rng.normal(size=(6, 6))) + 0.5
    q = 0.5 * (q + q.T)
    np.fill_diagonal(q, 0.0)
    v = np.abs(rng.normal(size=6)) + 0.5
    cand = np.arange(6)
    base = float(two_point_dual(C, v, q, cand)[0])
    refused = 0
    for label, vm in (("v_negative", np.where(np.arange(6) == 2, -v, v)),
                      ("v_zero", np.where(np.arange(6) == 2, 0.0, v)),
                      ("v_nan", np.where(np.arange(6) == 2, np.nan, v))):
        try:
            two_point_dual(C, vm, q, cand)
        except Exception:                                               # noqa: BLE001
            refused += 1
    _check("two_point_dual_refuses_degenerate_weights", refused == 3,
           f"{refused}/3 degenerate codomain weights raise; the well-formed control still "
           f"computes ({base:.8f})")


def main():
    print("=" * 78)
    print("Leg 147 / Route-NKB -- BANKED regression suite for solver/nk_bounds.py")
    print("  (leg 116's battery, post leg 128's repair, independently re-run)")
    print("=" * 78)
    if not os.path.exists(DATA):
        print(f"\nMISSING {os.path.relpath(DATA, HERE)} -- run\n"
              f"  .venv/bin/python experiments/p2_route_nkb_v1_postrepair.py\n")
        return 1
    for fn in (test_control_the_honest_certificate_still_behaves_both_ways,
               test_control_a_hypothesis_violating_constant_is_still_refused,
               test_seventeen_of_leg_116s_twenty_one_false_closers_now_reject,
               test_the_four_survivors_are_exactly_these_four_cases,
               test_the_one_survivor_that_gets_no_signal,
               test_the_three_flagged_survivors_do_carry_a_reason,
               test_no_clean_call_moved_by_one_bit,
               test_the_pre_repair_control_reproduced_leg_116s_banked_counts,
               test_the_ledger_magnitudes_reproduce,
               test_the_live_operating_range_is_still_silent_and_sound,
               test_two_point_dual_still_refuses_degenerate_weights):
        fn()
    print()
    if _FAILURES:
        print(f"{len(_FAILURES)} GATE(S) FAILED: {_FAILURES}")
        return 1
    print("ALL 11 POST-REPAIR REGRESSION GATES PASS "
          "(17 of leg 116's 21 reject; the 4 that survive are PINNED by name, and the "
          "one that arrives with no signal at all is pinned separately)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
