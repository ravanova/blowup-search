"""ROUTE-CGR (leg 215) -- the repair of leg 199's M1, and the measurement of its REACH.

WHAT THIS LEG WAS DISPATCHED TO DO
-----------------------------------------------------------------------------
Leg 199 (Route-CGA) audited the shared guard layer and answered its gate YES: 16 silent
accepts across five mechanisms (M1-M5), all LATENT, 0 banked numbers impeached.  It was
forbidden from patching under its own authority and escalated.  This leg lands the ONE
repair leg 199 itself scoped to one line, in the ONE file this leg is allowed to touch:

    "The repair is one line for M1.  `test_gap_m1_localised_...` is the evidence that the
     gamma site is already clean, so an `isinf` test ... closes M1 without touching the
     range logic."  -- experiments/journal/leg_199.md, "For whoever lands the repair"

THE MECHANISM, RESTATED FROM LEG 199 RATHER THAN RE-DERIVED
-----------------------------------------------------------------------------
`unit_range_violation` is the only one of the five exported guards with no `isinf` test; it
delegates non-finiteness to `lo_bad = (f <= lo) if lo_open else (f < lo)`.  `nk_bounds.py:430`
is the ONLY call site in the repository that hands it an INFINITE endpoint
(`lo = -inf, lo_open=False`), so the lower test is `-inf < -inf` = False and `alpha = -inf`
was admissible.  `farfield_modelling_error_bound(-inf, 0.5, 1.0)` then returned
`bound = NaN` with 40/40 window samples NaN and did NOT raise.  `+inf` and `NaN` alphas
already raised `ValueError` at the same site.

THE GATE (pre-committed, both branches, verbatim)
-----------------------------------------------------------------------------
    Does adding the missing `isinf` check to `nk_bounds.py`'s guard (per leg 199's own
    identified mechanism) cause all 16 previously-silently-accepted adversarial cases to
    now raise/reject, while every one of the 8 live call sites (finite alphas in
    [1.1, 1.8]) remains bit-identical to its pre-repair banked value?

    YES -> bank the repair, land straight to main, flag a postrepair-verification leg.
    NO  -> report exactly which case still slips through or which live call site moved;
           escalate rather than declare the repair complete on a partial fix.  Push the
           branch only, never main; report as parked.

**THE GATE ANSWERS NO, AND IT ANSWERS NO STRUCTURALLY, NOT BECAUSE THE REPAIR FAILED.**

The repair does exactly what leg 199 scoped it to do -- but the gate's first clause counts
all 16 of leg 199's hits, and only ONE of those 16 is M1.  The other 15 are M2/M3/M4/M5/M7:
type gates missing from `radius_violation`, `bool` coercion, a negative rational under the
denormal floor, empty containers, an empty rejection sentence.  Every one of them lives in
`solver/certificate_guards.py`, which this leg's declared territory marks READ-ONLY as leg
199's closed ground, and NONE of them is an `isinf` defect -- no `isinf` test at any site
could reject a `Decimal` radius or an empty weight vector.  So the gate as worded cannot be
satisfied by the repair it authorises, and this runner MEASURES that rather than arguing it:
each of the 16 cases is re-driven post-repair and reported individually.

This is the repair-family precedent (legs 150-154) held to: repair the named defect
precisely, do not re-litigate the finding leg's own measurement, and do not widen scope to
make a gate close.

WHAT IS MEASURED
-----------------------------------------------------------------------------
  (1) All 16 of leg 199's gate hits, re-driven at the SAME surface leg 199 used, with its
      banked pre-repair outcome pinned beside the post-repair one.
  (2) The load-bearing regression check: all 8 live call sites (alpha in [1.1, 1.8],
      gamma = 0.5, X0 = 1.0, n_X = 8 -- leg 199's own configuration), compared to their
      pre-repair values BIT-EXACTLY, via `float.hex()` rather than `==`.
  (3) The three non-finite alphas at the real consumer, so the repair's own surface is
      shown to be uniform (-inf, +inf, NaN all refuse, and all with a named ValueError).
  (4) Controls: the guard's admissible range is unchanged for finite alphas at both
      endpoints, and `alpha = -1e300` (leg 199's C1b secondary) is reported unchanged --
      this repair does NOT address it, and says so.

`solver/certificate_guards.py` IS NOT EDITED BY THIS LEG.  `solver/nk_bounds.py` carries
exactly one added guard clause and nothing else.
"""

import json
import os
import sys
from decimal import Decimal
from fractions import Fraction

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import solver.certificate_guards as cg          # noqa: E402
import solver.nk_bounds as nk                   # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_cgr_v1_repair.json")

INF, NAN = float("inf"), float("nan")

LIVE_ALPHAS = (1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8)
LIVE_GAMMA = 0.5
LIVE_X0 = 1.0
LIVE_N_X = 8

# The 8 live call sites, read out of leg 199's own blast-radius row rather than re-derived.
LIVE_CALLERS = (
    "test_nk_bounds.py:192,207 (ALPHA=1.5)",
    "experiments/p2_route_d_v6_bounds.py:170,200,224 (alphas=1.1..1.8)",
    "experiments/p2_route_d_v7_seminorm.py:298 (alphas=1.1..1.8)",
    "experiments/p2_route_d_v8_quadratic.py:306 (alphas=1.1..1.8)",
    "experiments/p2_route_d_v9_sharpen.py:326 (alphas=1.1..1.8)",
    "experiments/p2_route_nka_v1_adversarial.py:408,425 (LIVE_ALPHAS=1.1..1.8)",
    "experiments/p2_route_nkr_v1_repair.py:230",
    "experiments/p2_route_nkb_v1_postrepair.py:150",
)

# PRE-REPAIR banked bounds.  Provenance, both of which agree to the last bit:
#   (a) writeup/data/p2_route_cga_v1_adversarial.json on branch leg/199-cga-v1
#       (blast_radius[0].live_values), and
#   (b) re-measured in this worktree at merge-base 0e22b83 BEFORE the guard clause was
#       added, and printed as float.hex() so the comparison below is bit-exact, not
#       decimal-repr-exact.
PRE_REPAIR_LIVE = {
    1.1: "0x1.341041090b96cp+1",
    1.2: "0x1.37ea44d413ef4p+1",
    1.3: "0x1.3bfda59fe3024p+1",
    1.4: "0x1.404881c4f2c4cp+1",
    1.5: "0x1.44c968d6c2bd3p+1",
    1.6: "0x1.497f47cdc1947p+1",
    1.7: "0x1.4e6959936102ap+1",
    1.8: "0x1.53871ada6f2c8p+1",
}
PRE_REPAIR_LIVE_DECIMAL = {
    1.1: 2.4067460340658524, 1.2: 2.436836818269393, 1.3: 2.468678191251472,
    1.4: 2.502212735334558, 1.5: 2.537396530974982, 1.6: 2.5741967920941167,
    1.7: 2.612590023958565, 1.8: 2.652560574204788,
}


def _call(fn, *a, **k):
    """Run `fn` and classify: ("value", payload) or ("raise", "TypeName: message").

    A RAISE is a REFUSAL and is the behaviour the repair is meant to produce.  A guard that
    RETURNS an admissible verdict on an inadmissible input is the accept under audit.
    """
    try:
        return "value", fn(*a, **k)
    except Exception as e:                                     # noqa: BLE001
        return "raise", f"{type(e).__name__}: {e}"


def _jsonable(x):
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        x = x.item()
    if isinstance(x, float) and (x != x or x in (INF, -INF)):
        return repr(x)
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return repr(x)


# ---------------------------------------------------------------------------
# (1) leg 199's 16 gate hits, re-driven post-repair
# ---------------------------------------------------------------------------

def _accepted_guard_list(k, out):
    return k == "value" and out == []


def _accepted_guard_none(k, out):
    return k == "value" and out is None


def rerun_the_sixteen():
    """Each of leg 199's 16 hits, at the surface leg 199 measured it at.

    `mechanism` and `guard_module` are recorded per case because they are what decides
    whether this leg's ONE-clause repair could possibly have moved the case: a case whose
    surface is a `certificate_guards.py` function this leg may not touch, and whose defect
    is not a finiteness test, is UNREACHABLE by this repair by construction.
    """
    rows = []

    def row(case, mechanism, surface, in_territory, addressed_by_isinf,
            pre_accepted, post_accepted, post_detail, note):
        rows.append({
            "case": case, "mechanism": mechanism, "surface": surface,
            "surface_in_leg_215_territory": in_territory,
            "an_isinf_test_could_address_it": addressed_by_isinf,
            "pre_repair_accepted": pre_accepted,
            "post_repair_accepted": post_accepted,
            "post_repair_outcome": _jsonable(post_detail),
            "now_rejects": bool(pre_accepted and not post_accepted),
            "note": note,
        })

    H, R, P, U = (cg.hypothesis_violations, cg.radius_violation,
                  cg.positive_weight_violations, cg.unit_range_violation)

    # --- M3: bool is numbers.Real (2 cases)
    for lbl, v in [("A1_bool_True", True), ("A1_bool_False", False)]:
        k, out = _call(H, (("Y_0", v),))
        row(lbl, "M3", "certificate_guards.hypothesis_violations", False, False,
            True, _accepted_guard_list(k, out), f"{k}: {_jsonable(out)}",
            "a FLAG coerced to 1.0/0.0; not a finiteness defect and not in this "
            "leg's territory")

    # --- M4: a negative rational under the denormal floor (1 case)
    v = Fraction(-1, 10 ** 400)
    k, out = _call(H, (("Y_0", v),))
    row("A3_fraction_neg_below_denormal", "M4",
        "certificate_guards.hypothesis_violations", False, False,
        True, _accepted_guard_list(k, out), f"{k}: {_jsonable(out)}",
        "float() underflows to -0.0 before the `f < 0.0` test; accepted negatives span "
        "(-5e-324, 0), so <= 1 ULP. Not a finiteness defect")

    # --- M5: empty containers (1 here + 4 in family D)
    k, out = _call(H, ())
    row("A6_empty_constants", "M5", "certificate_guards.hypothesis_violations", False, False,
        True, _accepted_guard_list(k, out), f"{k}: {_jsonable(out)}",
        "0 of 0 constants validated; a vacuous pass, not a finiteness defect")

    # --- M2: no type gate in radius_violation (4 cases)
    for lbl, v in [("B_nonreal_str", "0.5"), ("B_nonreal_bool_True", True),
                   ("B_nonreal_Decimal", Decimal("0.5")),
                   ("B_nonreal_Fraction", Fraction(1, 2))]:
        k, out = _call(R, v)
        row(lbl, "M2", "certificate_guards.radius_violation", False, False,
            True, _accepted_guard_none(k, out), f"{k}: {_jsonable(out)}",
            "a non-Real accepted as an admissible RADIUS; a type gate, not a "
            "finiteness gate")

    # --- M1: THE ONE CASE THIS LEG REPAIRS, at the real consumer site.
    k, out = _call(nk.farfield_modelling_error_bound, -INF, LIVE_GAMMA, LIVE_X0)
    accepted = (k == "value")
    row("C1_alpha_minus_infinity_ACCEPTED", "M1",
        "nk_bounds.farfield_modelling_error_bound (the nk_bounds.py:430 site)", True, True,
        True, accepted, f"{k}: {str(out)[:240]}",
        "THE REPAIR. Pre-repair this returned bound=NaN with 40/40 window samples NaN and "
        "did not raise; post-repair it refuses with the site's own named ValueError")

    # The guard's OWN surface is deliberately unchanged, and that is recorded, not hidden:
    gk, gout = _call(U, "alpha", -INF, -INF, 2.0, lo_open=False, hi_open=True)
    rows.append({
        "case": "C1_at_the_guards_own_surface",
        "mechanism": "M1", "surface": "certificate_guards.unit_range_violation",
        "surface_in_leg_215_territory": False,
        "an_isinf_test_could_address_it": True,
        "pre_repair_accepted": True,
        "post_repair_accepted": _accepted_guard_none(gk, gout),
        "post_repair_outcome": f"{gk}: {_jsonable(gout)}",
        "now_rejects": False,
        "note": "NOT a gate case of its own (leg 199 counted M1 once). Recorded because it "
                "states the repair's shape honestly: the shared guard is byte-identical, "
                "and the missing finiteness test is supplied at the ONE call site in the "
                "repository that gives it an infinite endpoint. A caller that invokes the "
                "guard directly with lo=-inf, lo_open=False still gets None -- there is no "
                "such caller in the repo, and closing it belongs to a leg that owns "
                "certificate_guards.py",
        "counts_toward_the_16": False,
    })

    # --- M3/M2 at the gamma site (2 cases)
    k, out = _call(nk.hilbert_farfield_bound, 1.0, 1.5, True)
    row("C3_gamma_bool", "M3", "nk_bounds.hilbert_farfield_bound (the :392 gamma site)",
        False, False, True, k == "value", f"{k}: {str(out)[:160]}",
        "gamma=True is coerced to the legitimate exponent 1.0 and returns "
        "1.2209630139367613 vs 1.5390840894727127 at gamma=0.5 (1.2605493138651522x "
        "smaller). A missing SIGNAL, not an arithmetic lie; not a finiteness defect")
    # Measured at leg 199's OWN surface -- the GUARD -- not at the consumer.  This
    # distinction is load-bearing and is the reason it is spelled out: at the consumer a
    # str gamma dies of an unnamed `TypeError` from the power operator three lines in, and
    # scoring that crash as a "rejection" would let this leg claim a case it did not
    # repair.  Leg 199 counted the ACCEPT at `unit_range_violation`, which is where the
    # missing type gate is, and that is what is re-driven here.
    gk, gout = _call(U, "gamma", "0.5", 0.0, 1.0, lo_open=True, hi_open=False)
    ck, cout = _call(nk.hilbert_farfield_bound, 1.0, 1.5, "0.5")
    row("C4_gamma_str", "M2", "certificate_guards.unit_range_violation (the :392 gamma site)",
        False, False, True, _accepted_guard_none(gk, gout),
        f"guard {gk}: {_jsonable(gout)} | consumer {ck}: {str(cout)[:110]}",
        "a str gamma passes the exponent guard (guard returns None) and only then dies of "
        "an UNNAMED TypeError at the consumer -- leg 98's B20/B21 shape. A type gate in "
        "certificate_guards.py, not a finiteness gate; this leg neither repairs nor claims "
        "it, and the downstream crash is NOT scored as a rejection")

    # --- M5: the empty weight vector (3 + 1 cases)
    for lbl, vals in [("D1_empty_list", []), ("D1_empty_ndarray", np.array([])),
                      ("D1_exhausted_generator", "GEN")]:
        vv = (x for x in []) if isinstance(vals, str) else vals
        k, out = _call(P, "v_cod", vv)
        row(lbl, "M5", "certificate_guards.positive_weight_violations", False, False,
            True, _accepted_guard_list(k, out), f"{k}: {_jsonable(out)}",
            "0 of 0 entries validated; not a finiteness defect")

    screen_passes_empty = bool(np.all(np.isfinite(np.array([])))
                               and np.all(np.array([]) > 0.0))
    empty = _call(nk.two_point_dual, np.zeros((1, 0)), np.array([], dtype=int),
                  np.zeros((0, 0)), np.array([]))
    row("D1b_empty_at_the_consumer", "M5", "nk_bounds.two_point_dual (the :225 pre-screen)",
        False, False, True, screen_passes_empty,
        f"pre_screen_passes_empty={screen_passes_empty}; "
        f"two_point_dual -> {empty[0]}: {str(empty[1])[:90]}",
        "the caller's own numpy pre-screen passes the empty array too, so the guard is "
        "never consulted; not a finiteness defect")

    # --- M7: the empty rejection sentence (1 case)
    k, out = _call(cg.invalid_input_reason, [])
    row("E_empty_violation_list", "M7", "certificate_guards.invalid_input_reason",
        False, False, True, k == "value",
        f"{k}: {str(out)[:200]}",
        "a rejection sentence naming 0 violated hypotheses; hygiene, not a finiteness "
        "defect")

    return rows


# ---------------------------------------------------------------------------
# (2) the load-bearing regression check: 8 live call sites, BIT-exact
# ---------------------------------------------------------------------------

def live_site_bit_identity():
    rows = []
    for a in LIVE_ALPHAS:
        d = nk.farfield_modelling_error_bound(a, LIVE_GAMMA, LIVE_X0, n_X=LIVE_N_X)
        b = float(d["bound"])
        rows.append({
            "alpha": a,
            "pre_repair_hex": PRE_REPAIR_LIVE[a],
            "post_repair_hex": b.hex(),
            "pre_repair_decimal": PRE_REPAIR_LIVE_DECIMAL[a],
            "post_repair_decimal": b,
            "bit_identical": b.hex() == PRE_REPAIR_LIVE[a],
            "ulps_moved": 0 if b.hex() == PRE_REPAIR_LIVE[a] else None,
            "finite": bool(np.isfinite(b)),
            "argmax_at_window_end": bool(d["argmax_at_window_end"]),
        })
    return rows


# ---------------------------------------------------------------------------
# (3) the repair's own surface: all three non-finite alphas, one vocabulary
# ---------------------------------------------------------------------------

def nonfinite_alpha_uniformity():
    rows = []
    for lbl, v in [("minus_inf", -INF), ("plus_inf", INF), ("nan", NAN)]:
        k, out = _call(nk.farfield_modelling_error_bound, v, LIVE_GAMMA, LIVE_X0)
        rows.append({
            "alpha": repr(v), "label": lbl, "outcome_kind": k,
            "raises_ValueError": bool(k == "raise" and str(out).startswith("ValueError")),
            "message_head": str(out)[:150],
            "pre_repair": ("ACCEPTED, returned bound=NaN, 40/40 window samples NaN"
                           if lbl == "minus_inf" else "already raised ValueError"),
        })
    return rows


# ---------------------------------------------------------------------------
# (4) controls
# ---------------------------------------------------------------------------

def controls():
    rows = []
    # The admissible range is untouched for finite alphas, including both endpoints.
    for lbl, v, should_raise in [("in_range_1p5", 1.5, False),
                                 ("in_range_1p9999", 1.9999, False),
                                 ("upper_endpoint_2p0", 2.0, True),
                                 ("above_2p5", 2.5, True),
                                 ("negative_finite_-3p0", -3.0, False)]:
        k, out = _call(nk.farfield_modelling_error_bound, v, LIVE_GAMMA, LIVE_X0,
                       n_X=LIVE_N_X)
        raised = (k == "raise")
        rows.append({
            "control": f"range_semantics_{lbl}", "alpha": v,
            "should_raise": should_raise, "raised": raised,
            "ok": raised == should_raise,
            "detail": (str(out)[:110] if raised else
                       f"bound={float(out['bound'])!r}"),
            "why": "the repair must move NO finite alpha across the accept/reject line; "
                   "alpha=-3.0 is in the declared range [-inf, 2.0) and must still "
                   "evaluate",
        })

    # Leg 199's C1b secondary, reported unchanged rather than quietly swept in.
    k, out = _call(nk.farfield_modelling_error_bound, -1e300, LIVE_GAMMA, LIVE_X0,
                   n_X=LIVE_N_X)
    rows.append({
        "control": "C1b_alpha_neg1e300_unchanged", "alpha": -1e300,
        "should_raise": None, "raised": k == "raise", "ok": True,
        "detail": f"{k}: {str(out)[:110]}",
        "why": "leg 199 filed this as SECONDARY_NOT_A_GATE_HIT (accepted, then an unnamed "
               "OverflowError from inside the quadrature). It is a FINITE alpha, so the "
               "isinf clause does not touch it and this leg does NOT claim it. Recorded so "
               "the repair's boundary is stated, not implied",
    })

    # The gamma site is clean already (leg 199's own localisation), and stays clean.
    gk, gout = _call(cg.unit_range_violation, "gamma", -INF, 0.0, 1.0,
                     lo_open=True, hi_open=False)
    rows.append({
        "control": "gamma_site_still_refuses_minus_inf",
        "should_raise": None, "raised": None,
        "ok": bool(gk == "value" and gout is not None),
        "detail": f"{gk}: {_jsonable(gout)}",
        "why": "leg 199's localisation: the same guard function refuses -inf at the gamma "
               "site because that lower endpoint is FINITE (0.0, open). Unchanged here",
    })
    return rows


def main():
    sixteen = rerun_the_sixteen()
    counted = [r for r in sixteen if r.get("counts_toward_the_16", True)]
    live = live_site_bit_identity()
    nonfinite = nonfinite_alpha_uniformity()
    ctl = controls()

    now_rejects = [r["case"] for r in counted if r["now_rejects"]]
    still_accepts = [r["case"] for r in counted if not r["now_rejects"]]
    bit_identical = [r for r in live if r["bit_identical"]]

    gate_clause_1 = len(now_rejects) == len(counted)
    gate_clause_2 = len(bit_identical) == len(live)
    gate_answer = "YES" if (gate_clause_1 and gate_clause_2) else "NO"

    payload = {
        "leg": 215,
        "route": "CGR",
        "repairs": "leg 199 (Route-CGA) mechanism M1",
        "file_repaired": "solver/nk_bounds.py (ONE added guard clause at the :430 site)",
        "files_deliberately_untouched": [
            "solver/certificate_guards.py -- leg 199's read-only closed territory",
        ],
        "gate": ("Does adding the missing `isinf` check to `nk_bounds.py`'s guard (per leg "
                 "199's own identified mechanism) cause all 16 previously-silently-accepted "
                 "adversarial cases to now raise/reject, while every one of the 8 live call "
                 "sites (finite alphas in [1.1, 1.8]) remains bit-identical to its "
                 "pre-repair banked value?"),
        "gate_answer": gate_answer,
        "gate_clause_1_all_16_now_reject": gate_clause_1,
        "gate_clause_2_all_8_bit_identical": gate_clause_2,
        "totals": {
            "leg_199_gate_hits_rerun": len(counted),
            "now_reject": len(now_rejects),
            "still_accept": len(still_accepts),
            "live_sites": len(live),
            "live_sites_bit_identical": len(bit_identical),
            "live_sites_moved": len(live) - len(bit_identical),
            "of_the_16_addressable_by_an_isinf_test":
                sum(1 for r in counted if r["an_isinf_test_could_address_it"]),
            "of_the_16_inside_leg_215_territory":
                sum(1 for r in counted if r["surface_in_leg_215_territory"]),
        },
        "why_the_gate_answers_NO": (
            "The repair did what leg 199 scoped it to do: the ONE M1 case "
            "(C1_alpha_minus_infinity_ACCEPTED) now refuses with a named ValueError, and "
            "all 8 live call sites are bit-identical. The gate's first clause counts all 16 "
            "of leg 199's hits, but 15 of the 16 are M2/M3/M4/M5/M7 -- type gates, bool "
            "coercion, a sub-denormal rational, empty containers, an empty rejection "
            "sentence. None of them is a finiteness defect, so no `isinf` test anywhere "
            "could reject them, and every one of their surfaces is inside "
            "solver/certificate_guards.py, which this leg's declared territory marks "
            "read-only. The gate's premise -- that the 16 cases were all the missing-isinf "
            "family -- is what fails, not the repair. Escalated rather than declared "
            "complete, per the NO branch."),
        "still_accepting_cases": still_accepts,
        "now_rejecting_cases": now_rejects,
        "banked_numbers_impeached": 0,
        "banked_numbers_moved_by_the_repair": 0,
        "live_callers": list(LIVE_CALLERS),
        "live_site_config": {"gamma": LIVE_GAMMA, "X0": LIVE_X0, "n_X": LIVE_N_X,
                             "alphas": list(LIVE_ALPHAS)},
        "cases_rerun": sixteen,
        "live_site_bit_identity": live,
        "nonfinite_alpha_uniformity": nonfinite,
        "controls": ctl,
        "controls_failed": [c["control"] for c in ctl if not c["ok"]],
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")

    print("ROUTE-CGR (leg 215) -- repair of leg 199's M1")
    print(f"  gate answer                     {gate_answer}")
    print(f"  leg 199 hits re-driven          {len(counted)}")
    print(f"    now reject                    {len(now_rejects)}  {now_rejects}")
    print(f"    still accept                  {len(still_accepts)}")
    for c in still_accepts:
        r = next(x for x in counted if x["case"] == c)
        print(f"      - {c:36s} {r['mechanism']}  isinf-addressable="
              f"{r['an_isinf_test_could_address_it']}  in-territory="
              f"{r['surface_in_leg_215_territory']}")
    print(f"  live call sites bit-identical   {len(bit_identical)}/{len(live)}")
    for r in live:
        print(f"      alpha={r['alpha']}  {r['pre_repair_hex']} -> {r['post_repair_hex']}  "
              f"{'IDENTICAL' if r['bit_identical'] else 'MOVED'}")
    print("  non-finite alpha uniformity")
    for r in nonfinite:
        print(f"      {r['label']:10s} {r['outcome_kind']:5s} "
              f"ValueError={r['raises_ValueError']}")
    print(f"  controls failed                 {payload['controls_failed']}")
    print(f"  wrote {OUT}")
    return payload


if __name__ == "__main__":
    main()
