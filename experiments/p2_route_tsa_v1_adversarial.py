"""ROUTE-TSA v1 (leg 208): adversarial audit of `solver/target_selection.py`.

--------------------------------------------------------------------------
THE GATE, PRE-COMMITTED, BOTH BRANCHES
--------------------------------------------------------------------------
"Under adversarial and degenerate inputs, does `target_selection.py` ever silently
return a wrong screening verdict (pass a candidate that should fail the multiplier/shift
predicate, or vice versa) rather than reject or visibly propagate the defect?"

**ANSWERED: YES**, on the arithmetic screen, with six witnesses below.  It is
**escalation-shaped by the dispatch's own rule**, so this module PATCHES NOTHING,
`solver/target_selection.py` is untouched, and no entry is added to `capabilities.py`.

--------------------------------------------------------------------------
THE PREMISE THE DISPATCH CARRIED, CORRECTED BEFORE ANY MEASUREMENT
--------------------------------------------------------------------------
The dispatch names the audit target "leg 63/125's own screening module (the
multiplier/shift predicate that selected the gamma=2 candidate)".  **That code is not in
this file on `main`,** and this leg established it before measuring anything:

  * `git log --follow -- solver/target_selection.py` on `main` -> ONE commit, `2450ddf`,
    "Route-M v1".  Stage `M`, not leg 63.
  * leg 63's screen is `7a58854` on branch `leg/m2-v1`, **parked and unmerged**.  It adds
    `screen_operator`, `multiplier_crossover`, `m2_ledger`, `m2_rank_table`,
    `m2_gate_verdict` -- none of which exist on `main`.
  * `writeup/INDEX.md` line 102: "Route-M2 v1 (leg 63) -- PARKED, NOT LANDED ... No files
    on `main`."  `DIRECTION.md` 636/786 keeps the path off every live territory list.

So `main`'s file and the file leg 63 measured are two different files sharing a path.
Section F below answers the gate's yes-branch question -- "is leg 63's own 'exactly one
candidate passes' finding at risk?" -- against the PARKED predicate, read read-only out
of `git show leg/m2-v1`, because defects in the `main` file cannot answer it.

--------------------------------------------------------------------------
WHAT THIS LEG IS THE SIXTH OF, AND THAT IS THE REAL FINDING
--------------------------------------------------------------------------
`solver/certificate_guards.py` (leg 128) opens: "ONE hypothesis guard for every
radii-polynomial verdict function in this repository."  Its census names three:

    leg  79   port_certification.radii_polynomial_status   11/25 forbidden -> closes
    leg  98   interval_certificate.radii_verdict           12/36, 8 load-bearing
    leg 116   nk_bounds.budget                             21/52, 19 load-bearing

`test_nk_fourier_adversarial.py::test_gap_radii_polynomial_accepts_forbidden_constants`
pins a fourth (`nk_fourier.radii_polynomial`, 9/9) as a known unabsorbed gap.  Four
modules now delegate to the shared guard (`port_certification`, `nk_bounds`,
`interval_certificate`, `chen_inviscid_certificate`).

**`solver/target_selection.py` is a SIXTH verdict function of the same class, and the
string `target_selection` appears NOWHERE in `solver/certificate_guards.py`, nor in
`writeup/novelty/leg_128.md`, nor in `experiments/journal/leg_128.md`.**  It is not an
unrepaired member of the census.  It was never enumerated.  That is what this leg found,
and the arithmetic below is the evidence rather than the point.

--------------------------------------------------------------------------
LESSON 90 -- THE CONTROL, AND WHAT WOULD MAKE IT COME OUT DIFFERENTLY
--------------------------------------------------------------------------
"A control that cannot come out differently is not a control."  Section E feeds the
IDENTICAL forbidden tuples to `certificate_guards.hypothesis_violations`, the repaired
shared predicate.  If it also accepted them, the finding would be about the tuples, not
about `target_selection`, and this leg would have to report that instead.  It does not:
it rejects every one.  The tuples are the same, the constants are the same, and the only
thing that varies is which function reads them -- so the difference IS the guard.

Run: .venv/bin/python experiments/p2_route_tsa_v1_adversarial.py
"""

import json
import os
import subprocess
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.target_selection import (                                 # noqa: E402
    CERTIFICATION_RECORD, TARGET_LEDGER, cost_ratio_vs_certified, gate_verdict,
    radii_polynomial, rank_table, uncertified_targets, unknowns, y0_budget,
)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "writeup", "data", "p2_route_tsa_v1_adversarial.json")

NAN, INF = float("nan"), float("inf")


def _f(x):
    """JSON-safe float: NaN/inf survive as strings rather than as invalid JSON."""
    if x is None or isinstance(x, (bool, str)):
        return x
    x = float(x)
    if np.isnan(x):
        return "nan"
    if np.isinf(x):
        return "inf" if x > 0 else "-inf"
    return x


# ==========================================================================
# A.  y0_budget -- the module's OWN declared reach criterion, and it is
#     blind to the sign of (1 - Z1)
# ==========================================================================
def battery_a_y0_budget_sign_blindness():
    """`y0_budget` squares `1 - Z1`, so Z1 = 1 + x and Z1 = 1 - x are INDISTINGUISHABLE.

    The module's own docstring calls this "the number that makes 'is it within
    interval-arithmetic reach?' a measurement rather than an opinion".  Z1 >= 1 means
    `A` is not an approximate inverse and the true budget is ZERO -- `radii_polynomial`
    says so in its own `Z1 >= 1` branch.  `y0_budget` says otherwise, and says it with a
    finite positive number.
    """
    rows = []
    for Z1 in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0, 3.0, 5.0):
        b = y0_budget(Z1, 1.0)
        rows.append({"Z1": Z1, "Z2": 1.0, "budget_returned": _f(b),
                     "budget_true": 0.0 if Z1 >= 1.0 else _f(b),
                     "outside_theorem": bool(Z1 >= 1.0),
                     "returns_positive_budget_anyway": bool(Z1 >= 1.0 and b > 0.0)})

    # the mirror pairs, exact: y0_budget(1+x) == y0_budget(1-x) bit for bit
    mirrors = []
    for x in (0.1, 0.25, 0.5, 0.75, 0.9):
        lo, hi = y0_budget(1.0 - x, 1.0), y0_budget(1.0 + x, 1.0)
        mirrors.append({"x": x, "Z1_lo": 1.0 - x, "Z1_hi": 1.0 + x,
                        "budget_lo": _f(lo), "budget_hi": _f(hi),
                        "identical_bitwise": bool(lo == hi),
                        "abs_difference": _f(abs(lo - hi))})

    worst = y0_budget(2.0, 1.0)
    perfect = y0_budget(0.0, 1.0)
    return {
        "what": ("y0_budget(Z1, Z2) = (1 - Z1)^2 / (2 Z2) with NO check that Z1 < 1, "
                 "so it is invariant under Z1 -> 2 - Z1"),
        "rows": rows,
        "mirror_pairs": mirrors,
        "n_mirror_pairs": len(mirrors),
        "n_mirror_pairs_bitwise_identical": sum(1 for m in mirrors
                                                if m["identical_bitwise"]),
        "mirror_worst_abs_difference": _f(max(abs(y0_budget(1.0 - x, 1.0)
                                                  - y0_budget(1.0 + x, 1.0))
                                              for x in (0.1, 0.25, 0.5, 0.75, 0.9))),
        "mirror_note": ("3 of 5 agree BIT FOR BIT; the other two (x = 0.1, 0.9) differ "
                        "by <= 1.11e-16, which is the float representation of 0.9/1.1 "
                        "and not a property of the function"),
        "n_outside_theorem": sum(1 for r in rows if r["outside_theorem"]),
        "n_outside_that_return_positive_budget":
            sum(1 for r in rows if r["returns_positive_budget_anyway"]),
        "sharpest_witness": {
            "statement": ("Z1 = 2.0 -- an operator whose ||I - A DF|| is TWICE the "
                          "identity's tolerance, i.e. maximally not an approximate "
                          "inverse -- is assigned EXACTLY the residual budget of "
                          "Z1 = 0.0, a PERFECT inverse"),
            "budget_at_Z1_2": _f(worst), "budget_at_Z1_0": _f(perfect),
            "identical_bitwise": bool(worst == perfect),
            "true_budget_at_Z1_2": 0.0,
            "overstatement": "infinite -- a finite positive budget where the truth is 0",
        },
    }


# ==========================================================================
# B.  radii_polynomial -- forbidden constants that return feasible = True
# ==========================================================================
FORBIDDEN = {
    # label                       (Y0,    Z1,   Z2)   why it is outside the theorem
    "Z2_negative_unit":           (1e-3,  0.5, -1.0),
    "Z2_negative_large":          (1e-3,  0.5, -1e4),
    "Y0_negative_unit":           (-1.0,  0.5,  1.0),
    "Y0_negative_small":          (-1e-6, 0.5,  1.0),
    "Y0_negative_huge":           (-1e6,  0.5,  1.0),
    "Z1_negative_unit":           (1e-3, -1.0,  1.0),
    "Z1_negative_large":          (1e-3, -3.0,  1.0),
    "Y0_and_Z1_negative":         (-1.0, -1.0,  1.0),
    "all_three_negative":         (-1.0, -1.0, -1.0),
}

NAN_INF = {
    "Y0_nan":  (NAN,  0.5, 1.0),
    "Z1_nan":  (1e-3, NAN, 1.0),
    "Z2_nan":  (1e-3, 0.5, NAN),
    "Y0_inf":  (INF,  0.5, 1.0),
    "Z1_ninf": (1e-3, -INF, 1.0),
    "Z2_inf":  (1e-3, 0.5, INF),
}


def battery_b_radii_polynomial_forbidden():
    """Every constant is a NORM (the module's own comment says so), hence >= 0.

    `radii_polynomial` checks `Z1 >= 1` and `disc < 0` and `a <= 0`.  It never checks a
    SIGN.  The `a <= 0` branch is the sharp one: it is reached by `Z2 = 0` AND by every
    `Z2 < 0`, and it reports `reason = "Z2 = 0, affine"` -- a false statement about its
    own input -- together with `feasible = True`.
    """
    rows = []
    for label, args in FORBIDDEN.items():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = radii_polynomial(*args)
        rows.append({
            "label": label, "Y0": _f(args[0]), "Z1": _f(args[1]), "Z2": _f(args[2]),
            "feasible": bool(r["feasible"]), "reason": r["reason"],
            "r_min": _f(r["r_min"]), "r_max": _f(r["r_max"]),
            "Y0_budget": _f(r["Y0_budget"]), "Y0_over_budget": _f(r["Y0_over_budget"]),
            "negative_radius": bool(r["feasible"] and r["r_min"] is not None
                                    and not np.isnan(float(r["r_min"]))
                                    and float(r["r_min"]) < 0.0),
            "reason_contradicts_input": bool("Z2 = 0" in str(r["reason"])
                                             and float(args[2]) != 0.0),
        })

    nan_rows = []
    for label, args in NAN_INF.items():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = radii_polynomial(*args)
        nan_rows.append({"label": label, "feasible": bool(r["feasible"]),
                         "reason": r["reason"], "r_min": _f(r["r_min"])})

    n_close = sum(1 for r in rows if r["feasible"])
    return {
        "what": ("forbidden (Y0, Z1, Z2) triples -- each violates a NONNEGATIVITY "
                 "hypothesis that the module's own comment states by calling the "
                 "quantities ||A F(x)||, ||I - A DF(x)||, ||A(DF(v) - DF(x))||"),
        "rows": rows,
        "n_forbidden": len(rows),
        "n_forbidden_that_return_feasible": n_close,
        "n_with_negative_certified_radius": sum(1 for r in rows if r["negative_radius"]),
        "n_whose_reason_string_contradicts_its_input":
            sum(1 for r in rows if r["reason_contradicts_input"]),
        "nan_inf_rows": nan_rows,
        "nan_inf_all_refused": all(not r["feasible"] for r in nan_rows),
        "nan_inf_note": ("NaN is absorbed into a REFUSAL -- the benign direction -- but "
                         "by accident, not by a guard: `feasible = r_min < min(...)` is "
                         "False because every ordered comparison with NaN is False "
                         "(Goldberg; see writeup/novelty/leg_208.md Q3), and the row "
                         "still carries reason = 'ok' with r_min = nan, and emits a "
                         "RuntimeWarning.  Reported, NOT inflated."),
        "sharpest_witness": {
            "statement": ("radii_polynomial(-1.0, 0.5, 1.0) returns feasible = True "
                          "with r_min = -1.0: a Newton-Kantorovich existence ball of "
                          "NEGATIVE radius, asserting a zero inside an empty set"),
            "r_min": _f(radii_polynomial(-1.0, 0.5, 1.0)["r_min"]),
        },
        "second_witness": {
            "statement": ("radii_polynomial(1e-3, 0.5, -1.0) returns feasible = True "
                          "with reason = 'Z2 = 0, affine' while Z2 = -1.0.  The a <= 0 "
                          "branch swallows every negative Z2 into the Z2 = 0 case and "
                          "then NAMES the wrong one in its own output"),
        },
    }


# ==========================================================================
# C.  the Z1 >= 1 row that radii_polynomial gets RIGHT, and still misreports
# ==========================================================================
def battery_c_budget_leaks_through_a_correct_refusal():
    """`radii_polynomial` refuses at Z1 >= 1 -- and its dict still carries a budget.

    `out` is built BEFORE the `Z1 >= 1` test, so `Y0_budget` and `Y0_over_budget` are
    computed from the sign-blind `y0_budget` and survive into a row whose `feasible` is
    correctly False.  This repository quotes `Y0_over_budget` as a MAGNITUDE (lesson:
    report a magnitude, never a boolean) -- `p2_route_l1_v1_interval.py:115` and
    `p2_route_port_v1_bordered.json` both bank exactly that field.  So the boolean is
    right and the number a reader is told to trust is wrong.
    """
    rows = []
    for Z1 in (1.0, 1.1, 1.5, 2.0, 3.0):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r = radii_polynomial(0.1, Z1, 1.0)
        rows.append({"Y0": 0.1, "Z1": Z1, "Z2": 1.0,
                     "feasible": bool(r["feasible"]),
                     "feasible_is_correct": bool(r["feasible"] is False),
                     "Y0_budget_reported": _f(r["Y0_budget"]),
                     "Y0_over_budget_reported": _f(r["Y0_over_budget"]),
                     "reads_as_headroom": bool(r["Y0_budget"] > 0
                                               and r["Y0_over_budget"] < 1.0)})
    return {
        "what": ("the Z1 >= 1 refusal is CORRECT; the magnitudes shipped alongside it "
                 "are not, because `out` is assembled before the guard runs"),
        "rows": rows,
        "n_correct_refusals": sum(1 for r in rows if r["feasible_is_correct"]),
        "n_that_also_report_spare_headroom":
            sum(1 for r in rows if r["reads_as_headroom"]),
        "sharpest_witness": {
            "statement": ("at Z1 = 2.0, Z2 = 1.0, Y0 = 0.1 the verdict is correctly "
                          "INFEASIBLE while the same dict reports Y0_over_budget = 0.2, "
                          "i.e. 'you are using a fifth of your budget, 5x of headroom', "
                          "for an operator with no budget at all"),
            "Y0_over_budget_at_Z1_2": _f(radii_polynomial(0.1, 2.0, 1.0)["Y0_over_budget"]),
        },
    }


# ==========================================================================
# D.  unknowns / cost_ratio -- the REACH screen, and a silent dimension truncation
# ==========================================================================
def battery_d_unknowns_degenerate_exponent():
    """`unknowns` does `int(n_per_dim) ** int(dim)`: a fractional dim is TRUNCATED.

    The docstring says "Exact unknown count for a spectral/collocation truncation.  No
    fudge factors."  A `dim` of 1.9 -- the shape of a typo, or of a dimension read from a
    float field -- is silently screened as `dim = 1`, and Q2's whole discriminator is the
    unknown count.
    """
    rows = []
    for dim in (1, 1.4, 1.5, 1.9, 1.999999, 2, 2.5, 3):
        u = unknowns(dim, 2, 600, 3)
        rows.append({"dim": dim, "unknowns": _f(u), "dim_used": int(dim),
                     "truncated": bool(int(dim) != dim), "is_int": isinstance(u, int)})
    u19, u2 = unknowns(1.9, 2, 600, 3), unknowns(2, 2, 600, 3)

    # negative dim: returns a FLOAT from a function documented as an exact count
    neg = unknowns(-1, 2, 600, 3)

    # NaN dim is the one degenerate case that is loud
    try:
        unknowns(NAN, 2, 600, 3)
        nan_raises = False
        nan_exc = None
    except Exception as e:                                       # noqa: BLE001
        nan_raises, nan_exc = True, type(e).__name__

    # the reach predicate `ratio <= 1.0` at degenerate resolutions
    ratio_rows = []
    for n in (0, 1, 2, 10, 100, 600, 5000):
        r1 = cost_ratio_vs_certified(1, 2, n, 3)["ratio"]     # ledger rank 1 (1D)
        r3 = cost_ratio_vs_certified(2, 2, n, 3)["ratio"]     # ledger rank 3 (2D)
        ratio_rows.append({"n_per_dim": n, "ratio_1D_rank1": _f(r1),
                           "ratio_2D_rank3": _f(r3),
                           "rank1_passes_reach_screen": bool(r1 <= 1.0),
                           "dimensions_indistinguishable": bool(abs(r1 - r3) < 1e-15)})
    return {
        "what": "the Q2 reach screen: exact unknown count and ratio to the certified object",
        "rows": rows,
        "fractional_dim_understatement_factor": _f(u2 / u19),
        "fractional_dim_note": ("unknowns(1.9, 2, 600, 3) = %d, identical to the dim = 1 "
                                "answer, against %d for dim = 2" % (u19, u2)),
        "negative_dim_returns": _f(neg),
        "negative_dim_is_int": isinstance(neg, int),
        "negative_dim_note": ("unknowns(-1, ...) returns a FLOAT from a function whose "
                              "docstring promises an exact count"),
        "nan_dim_raises": nan_raises, "nan_dim_exception": nan_exc,
        "ratio_rows": ratio_rows,
        "rank_table_docstring_claim": ("'it cancels in the DIMENSION part of the ratio "
                                       "and only sets the scale, so the ranking it "
                                       "produces is insensitive to the choice'"),
        "claim_holds_at_default_600": True,
        "claim_fails_at": ("n_per_dim = 1, where the 1D rank-1 and 2D rank-3 candidates "
                           "have the SAME ratio 1.0 and the dimension is invisible; and "
                           "n_per_dim = 0, where rank 1's ratio is 1.5 > 1 and it FAILS "
                           "the gate's own reach screen"),
        "containment": ("gate_verdict() calls rank_table() with the default and does NOT "
                        "forward n_per_dim, so neither degenerate resolution is "
                        "reachable from the gate.  The containment is real and is why "
                        "this row is LATENT, not contaminating"),
    }


# ==========================================================================
# E.  THE CONTROL (lesson 90) -- same tuples, the repaired shared guard
# ==========================================================================
def battery_e_control_shared_guard():
    """The identical forbidden tuples, fed to `certificate_guards.hypothesis_violations`.

    THIS CONTROL CAN COME OUT THE OTHER WAY.  If the shared guard also accepted these
    triples, the finding would be "the tuples are not really forbidden" and this leg
    would report that instead of a defect in `target_selection`.  What varies between
    the two columns is ONLY which function reads the constants.
    """
    from solver.certificate_guards import hypothesis_violations

    rows = []
    for label, (Y0, Z1, Z2) in FORBIDDEN.items():
        v = hypothesis_violations((("Y_0", Y0), ("Z_1", Z1), ("Z_2", Z2)))
        ts = radii_polynomial(Y0, Z1, Z2)
        rows.append({"label": label,
                     "shared_guard_violations": list(v),
                     "shared_guard_rejects": bool(len(v) > 0),
                     "target_selection_feasible": bool(ts["feasible"])})
    n_guard = sum(1 for r in rows if r["shared_guard_rejects"])
    n_ts = sum(1 for r in rows if r["target_selection_feasible"])

    # the negative half of the control: ADMISSIBLE tuples must pass BOTH
    admissible = [(1e-8, 0.3, 1e3), (1e-12, 0.05, 1.0), (1e-6, 0.9, 1e-2)]
    adm = []
    for Y0, Z1, Z2 in admissible:
        v = hypothesis_violations((("Y_0", Y0), ("Z_1", Z1), ("Z_2", Z2)))
        adm.append({"Y0": Y0, "Z1": Z1, "Z2": Z2,
                    "shared_guard_rejects": bool(len(v) > 0),
                    "target_selection_feasible": bool(radii_polynomial(Y0, Z1, Z2)["feasible"])})
    return {
        "what": "same tuples, two readers; only the reader varies",
        "rows": rows,
        "n_forbidden": len(rows),
        "shared_guard_rejects": n_guard,
        "target_selection_accepts": n_ts,
        "control_is_informative": bool(n_guard != n_ts),
        "admissible_rows": adm,
        "admissible_pass_both": all(not a["shared_guard_rejects"]
                                    and a["target_selection_feasible"] for a in adm),
        "reading": ("%d/%d forbidden triples are REJECTED by the repaired shared guard "
                    "and %d/%d are ACCEPTED by target_selection.  The tuples are "
                    "genuinely outside the theorem; the difference is the guard."
                    % (n_guard, len(rows), n_ts, len(rows))),
    }


# ==========================================================================
# F.  REACHABILITY -- latent, or does it contaminate a banked result?
# ==========================================================================
CALLER_JSONS = ["p2_route_c_pilot_v0.json", "p2_route_l1_v1_interval.json",
                "p2_weight_repairs_v1.json", "p2_weight_repairs_v2.json",
                "p2_route_port_v1_bordered.json", "p2_route_port_v2_reach.json",
                "p2_route_m_v1_targets.json"]


def _walk(o, path, fn):
    if isinstance(o, dict):
        if "Z1" in o:
            fn(o, path)
        for k, v in o.items():
            _walk(v, path + "." + str(k), fn)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _walk(v, path + "[%d]" % i, fn)


def battery_f_reachability():
    """Is any adversarial case REACHABLE from a banked call path, or only theoretical?

    Two independent arguments, and they agree.

    (1) BY CONSTRUCTION.  Every caller builds its constants as maxima of ABSOLUTE
        values -- `weight_search.certificate_constants`, `p2_route_c_pilot_v0`,
        `p2_route_l1_v1_interval`, `p2_route_port_v1_bordered` all compute
        `Y0 = max(w * |A @ Fz|)`, `Z1 = max(w * (|I - A J| @ (1/w)))`,
        `Z2 = 2 * A_norm * B` with `A_norm`, `B` sums of absolute values.  A negative
        Y0, Z1 or Z2 CANNOT arise.  So the whole negative-constant family is latent.

    (2) BY AUDIT OF THE BANKED RECORD.  Every `Z1`-bearing record in every JSON produced
        by a runner that imports `target_selection.y0_budget` or `radii_polynomial` is
        re-read here and checked against `0 <= Z1 < 1`.

    The one regime that IS reachable in principle is `Z1 >= 1` -- `weight_search`'s own
    capability entry records "the admissible band shuts entirely at n ~ 3.2e3 because
    Z_1 is float conditioning", which is exactly Z1 crossing 1.  What stops it is
    measured, not assumed, and it is not `target_selection`: `weight_search.fitness_many`
    RE-IMPLEMENTS the budget inline as
    `np.where(Z1 < 1.0, (1 - Z1)**2 / (2*Z2), -1.0)`, i.e. with the guard the shared
    function lacks, and never calls `y0_budget` on the GA path.  `y0_budget` survives in
    `weight_search.certificate_constants` only as a REPORTING field.
    """
    scanned, offenders = [], []
    for name in CALLER_JSONS:
        p = os.path.join(HERE, "writeup", "data", name)
        if not os.path.exists(p):
            scanned.append({"file": name, "present": False})
            continue
        recs = []

        def fn(o, path, name=name):
            z = o.get("Z1")
            if isinstance(z, (int, float)) and not isinstance(z, bool):
                recs.append((path, float(z)))
        with open(p) as fh:
            _walk(json.load(fh), "", fn)
        bad = [(pa, z) for pa, z in recs if z >= 1.0 or z < 0.0]
        offenders.extend({"file": name, "path": pa, "Z1": _f(z)} for pa, z in bad)
        scanned.append({"file": name, "present": True, "n_Z1_records": len(recs),
                        "n_outside_0_le_Z1_lt_1": len(bad)})

    total = sum(s.get("n_Z1_records", 0) for s in scanned)
    return {
        "question": ("is any adversarial case reachable from a banked call path, the "
                     "way legs 201/204 separated 'latent' from 'contaminates'?"),
        "argument_1_by_construction": (
            "every banked Y0/Z1/Z2 is a max of ABSOLUTE values, so no negative constant "
            "can arise from any call path in this repository"),
        "scanned": scanned,
        "n_Z1_records_across_caller_jsons": total,
        "n_outside_theorem": len(offenders),
        "offenders": offenders,
        "negative_Z1_elsewhere_in_repo": (
            "64 records carry Z1 < 0, and ALL of them live in other legs' deliberate "
            "adversarial batteries -- p2_route_ica_v1 (4), p2_route_nfa_v1 (7), "
            "p2_route_nka_v1 (14), p2_route_nkb_v1 (34), p2_route_nsa_v1 (2), "
            "p2_route_pc_v1 (3) -- fed to the SIBLING functions, never to "
            "target_selection's.  Zero are measurements"),
        "weight_search_containment": (
            "weight_search.fitness_many re-implements the budget inline WITH a "
            "`Z1 < 1.0` guard and never calls y0_budget on the GA path; y0_budget "
            "appears there only as a reporting field of certificate_constants"),
        "verdict": ("LATENT.  %d of %d banked (Y0,Z1,Z2) records across every caller "
                    "lie inside 0 <= Z1 < 1, and no negative constant is constructible. "
                    "NO banked number is contaminated." % (total - len(offenders), total)),
    }


# ==========================================================================
# G.  the LEDGER verdicts -- planted wrong values, and what already catches them
# ==========================================================================
def battery_g_ledger_passthrough():
    """`uncertified_targets` and `gate_verdict` read a TRANSCRIBED field with no cross-check.

    Two plants.  Both propagate silently through the module -- and both are CAUGHT by the
    landed `test_target_selection.py`.  Reporting the guard that exists is the point:
    this leg nearly filed the first as uncaught, and the drift suite catches it by an
    assertion ("the certified reference vanished from the ledger") that is not the one a
    reading of the test's docstring would predict.
    """
    import copy
    import contextlib
    import io
    import importlib

    import solver.target_selection as ts
    T = importlib.import_module("test_target_selection")
    orig = copy.deepcopy(ts.TARGET_LEDGER)
    names = sorted(n for n in dir(T) if n.startswith("test_"))

    def run_suite():
        caught = []
        for n in names:
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    getattr(T, n)()
            except AssertionError as e:
                caught.append({"test": n, "message": str(e)[:160]})
            except Exception as e:                               # noqa: BLE001
                caught.append({"test": n, "message": "ERROR " + type(e).__name__})
        return caught

    base = gate_verdict()

    # P1 -- flip a CAP-certified object to "NO"
    row = next(t for t in ts.TARGET_LEDGER if t["id"] == "Boussinesq_ChenHou")
    row["certified"] = "NO"
    p1_gate, p1_caught = gate_verdict(), run_suite()
    ts.TARGET_LEDGER[:] = copy.deepcopy(orig)

    # P2 -- reorder the ledger so list order != rank order
    ts.TARGET_LEDGER[:] = sorted(copy.deepcopy(orig), key=lambda t: -t["rank"])
    p2_gate, p2_caught = gate_verdict(), run_suite()
    ts.TARGET_LEDGER[:] = copy.deepcopy(orig)

    restored = gate_verdict()
    return {
        "baseline_gate": base,
        "P1_planted_certified_object_marked_NO": {
            "what": ("Boussinesq_ChenHou is CAP-certified (Chen-Hou arXiv:2210.07191 + "
                     "Part II); its `certified` field is flipped to 'NO'"),
            "gate_after": p1_gate,
            "uncertified_count_before": base["uncertified_count"],
            "uncertified_count_after": p1_gate["uncertified_count"],
            "named_target_moved": bool(base["named_target"] != p1_gate["named_target"]),
            "module_propagates_silently": True,
            "caught_by_landed_suite": [c["test"] for c in p1_caught],
            "caught_messages": p1_caught,
        },
        "P2_ledger_reordered": {
            "what": ("`uncertified_targets` docstring says 'in rank order' but does NOT "
                     "sort; `gate_verdict` then takes live[0].  rank_table() DOES sort, "
                     "so the two disagree the moment list order leaves rank order"),
            "gate_after": p2_gate,
            "named_target_before": base["named_target"],
            "named_target_after": p2_gate["named_target"],
            "named_target_moved": bool(base["named_target"] != p2_gate["named_target"]),
            "rank_of_named_after": next(t["rank"] for t in TARGET_LEDGER
                                        if t["id"] == p2_gate["named_target"]),
            "module_propagates_silently": True,
            "caught_by_landed_suite": [c["test"] for c in p2_caught],
        },
        "ledger_restored_identical": bool(restored == base),
        "reading": ("the LEDGER half of the module is unguarded INTERNALLY but covered "
                    "EXTERNALLY: the landed drift suite catches both plants.  The "
                    "ARITHMETIC half has no such cover -- test_target_selection.py "
                    "feeds it four admissible (Z1, Z2) pairs and nothing else"),
    }


# ==========================================================================
# H.  is leg 63's "exactly one candidate passes" at risk?  (the gate's yes-branch)
# ==========================================================================
def battery_h_leg63_exposure():
    """Read leg 63's PARKED predicate read-only and check whether it touches this algebra.

    The gate's yes-branch requires an explicit answer.  `git show leg/m2-v1` is the only
    honest place to get one, because the code is not on `main`.
    """
    try:
        src = subprocess.run(["git", "show", "leg/m2-v1:solver/target_selection.py"],
                             cwd=HERE, capture_output=True, text=True, check=True).stdout
        available = True
    except Exception as e:                                       # noqa: BLE001
        return {"branch_readable": False, "error": str(e)[:200]}

    m2_names = ["screen_operator", "multiplier_crossover", "m2_ledger", "m2_rank_table",
                "m2_gate_verdict", "screen_m_divergence", "fractional_tail_inverse_norm"]
    present_on_branch = {n: ("def " + n) in src for n in m2_names}

    main_src = open(os.path.join(HERE, "solver", "target_selection.py")).read()
    present_on_main = {n: ("def " + n) in main_src for n in m2_names}

    # does leg 63's predicate path consume the defective algebra?
    start = src.find("def screen_operator")
    end = src.find("def m2_gate_verdict")
    predicate_block = src[start:] if start >= 0 else ""
    tail = src[start:end] if 0 <= start < end else predicate_block
    uses = {fn: (fn in tail) for fn in ("y0_budget", "radii_polynomial", "Y0_budget")}

    return {
        "branch_readable": available,
        "branch": "leg/m2-v1",
        "commit": "7a58854 (Leg 63: LEG -- Route-M2 v1)",
        "status_per_writeup_INDEX": "PARKED, NOT LANDED -- No files on main",
        "leg63_functions_present_on_branch": present_on_branch,
        "leg63_functions_present_on_main": present_on_main,
        "n_leg63_functions_on_main": sum(present_on_main.values()),
        "predicate_consumes_defective_algebra": uses,
        "how_the_predicate_actually_decides": (
            "screen_operator reads the SIGN of a K-exponent fitted by decay_exponent to "
            "spectral_certificate tail-inverse norms, and m2_gate_verdict filters rows "
            "on (predicate == MULTIPLIER_SIDE, certified == 'NO', blowup_provable == "
            "'YES').  No Y_0, no Z_1, no Z_2, no budget, no radii polynomial anywhere "
            "on that path"),
        "VERDICT": (
            "leg 63's 'exactly one candidate passes' finding is NOT at risk from any "
            "defect in this audit.  The exposure is zero for a STRUCTURAL reason, not a "
            "lucky one: leg 63's predicate is a disjoint code path that never evaluates "
            "the radii-polynomial algebra, and it is not on `main` at all.  The gamma=2 "
            "line (63/125/174/185/187) is therefore untouched by this leg's YES"),
        "one_thing_worth_recording_for_whoever_unparks_the_branch": (
            "m2_gate_verdict has the SAME unsorted-live[0] shape as main's gate_verdict "
            "(battery G, P2): `top_candidate = live[0]['id']` off an unsorted filter. "
            "On a one-element `live` -- which is exactly what 'exactly one candidate "
            "passes' means -- live[0] is unambiguous, so the finding as stated is safe. "
            "This leg did NOT run the parked branch and makes no measurement of it"),
    }


# ==========================================================================
def main():
    payload = {
        "leg": 208, "route": "TSA", "role": "LEG",
        "target": "solver/target_selection.py",
        "gate": ("Under adversarial and degenerate inputs, does target_selection.py ever "
                 "silently return a wrong screening verdict (pass a candidate that "
                 "should fail the multiplier/shift predicate, or vice versa) rather "
                 "than reject or visibly propagate the defect?"),
        "premise_correction": (
            "the dispatch names this file as leg 63's multiplier/shift screen; it is "
            "not.  main's file is Route-M v1 (commit 2450ddf).  Leg 63's screen is "
            "commit 7a58854 on the PARKED, unmerged branch leg/m2-v1 and adds "
            "screen_operator / multiplier_crossover / m2_gate_verdict, none of which "
            "exist on main"),
        "census_finding": (
            "solver/certificate_guards.py (leg 128) declares itself 'ONE hypothesis "
            "guard for every radii-polynomial verdict function in this repository' and "
            "enumerates three members (legs 79, 98, 116); a fourth (nk_fourier) is "
            "pinned as a known gap.  The string 'target_selection' appears in NONE of "
            "certificate_guards.py, writeup/novelty/leg_128.md or "
            "experiments/journal/leg_128.md.  This module is a sixth verdict function "
            "of the same class that the census never enumerated"),
        "A_y0_budget_sign_blindness": battery_a_y0_budget_sign_blindness(),
        "B_radii_polynomial_forbidden": battery_b_radii_polynomial_forbidden(),
        "C_budget_leaks_through_refusal": battery_c_budget_leaks_through_a_correct_refusal(),
        "D_unknowns_degenerate_exponent": battery_d_unknowns_degenerate_exponent(),
        "E_control_shared_guard": battery_e_control_shared_guard(),
        "F_reachability": battery_f_reachability(),
        "G_ledger_passthrough": battery_g_ledger_passthrough(),
        "H_leg63_exposure": battery_h_leg63_exposure(),
    }

    A, B, C, D = (payload["A_y0_budget_sign_blindness"],
                  payload["B_radii_polynomial_forbidden"],
                  payload["C_budget_leaks_through_refusal"],
                  payload["D_unknowns_degenerate_exponent"])
    E, F = payload["E_control_shared_guard"], payload["F_reachability"]

    payload["gate_verdict"] = {
        "answer": "YES",
        "n_forbidden_triples_returning_feasible": B["n_forbidden_that_return_feasible"],
        "n_forbidden_triples": B["n_forbidden"],
        "n_with_negative_certified_radius": B["n_with_negative_certified_radius"],
        "y0_budget_outside_theorem_returning_positive":
            A["n_outside_that_return_positive_budget"],
        "y0_budget_worst_overstatement": A["sharpest_witness"]["statement"],
        "correct_refusals_that_still_report_headroom":
            C["n_that_also_report_spare_headroom"],
        "fractional_dim_understatement_factor": D["fractional_dim_understatement_factor"],
        "control_informative": E["control_is_informative"],
        "reachability": F["verdict"],
        "leg63_at_risk": False,
        "escalation": ("ESCALATION -- claim-adjacent module, gate answered YES.  Branch "
                       "pushed, main NOT pushed, solver/target_selection.py NOT patched, "
                       "no capabilities.py entry.  Parked for the Decision Maker"),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=2, sort_keys=False)

    g = payload["gate_verdict"]
    print("ROUTE-TSA v1 -- adversarial audit of solver/target_selection.py")
    print("  GATE: %s" % g["answer"])
    print("  A  y0_budget: %d/%d rows outside the theorem return a POSITIVE budget; "
          "y0_budget(2.0,1.0) == y0_budget(0.0,1.0) == %s"
          % (A["n_outside_that_return_positive_budget"], A["n_outside_theorem"],
             A["sharpest_witness"]["budget_at_Z1_2"]))
    print("  B  radii_polynomial: %d/%d forbidden triples return feasible=True, "
          "%d with a NEGATIVE certified radius (worst r_min = %s)"
          % (B["n_forbidden_that_return_feasible"], B["n_forbidden"],
             B["n_with_negative_certified_radius"], B["sharpest_witness"]["r_min"]))
    print("  C  %d/%d correct Z1>=1 refusals still ship Y0_over_budget < 1 "
          "(worst = %s, reads as 5x headroom)"
          % (C["n_that_also_report_spare_headroom"], len(C["rows"]),
             C["sharpest_witness"]["Y0_over_budget_at_Z1_2"]))
    print("  D  unknowns(1.9,...) understates the dim-2 count by %.1fx, silently"
          % D["fractional_dim_understatement_factor"])
    print("  E  CONTROL: shared guard rejects %d/%d, target_selection accepts %d/%d"
          % (E["shared_guard_rejects"], E["n_forbidden"],
             E["target_selection_accepts"], E["n_forbidden"]))
    print("  F  %s" % F["verdict"])
    print("  H  leg 63 at risk: NO -- disjoint code path, and not on main at all")
    print("  ->  %s" % OUT)


if __name__ == "__main__":
    main()
