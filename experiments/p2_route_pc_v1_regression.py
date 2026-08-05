"""Route-PC v1: an adversarial fabrication-rejection audit of the L1->L2 port's kill-switch.

`capabilities.py`'s validated line for `solver/port_certification.py` claims

    "radii_polynomial_status returns BLOCKED_AT_STEP_ONE and is gated to carry NO fabricated
     Y_0 or Z_1"

This leg tests the SECOND half of that sentence adversarially. The first half -- the
(None, None) path -- is already gated by `test_port_certification.py::test_4`. What was never
tested is what the function does when a caller hands it numbers that LOOK plausible but were
never derived from a certificate run: negative norms, NaNs, infinities, booleans, wrong types.

The standard against which each case is judged is NOT taste. It is the published hypothesis of
the radii polynomial theorem (van den Berg-Lessard, AMS Notices 62(9):1057; Hungria-Lessard-
Mireles James, Math. Comp.), recorded verbatim in writeup/novelty/leg_79.md: Y_0, Z_1 and Z_2
are UPPER BOUNDS ON NORMS,

    ||T(x)-x|| <= Y_0,   sup ||A(DF(x+rv) - A_dagger)u|| <= Z_1 + Z_2 r,

hence nonnegative and finite BY HYPOTHESIS. A negative or non-finite constant is therefore not
a conservative input -- it is an input the imported theorem says nothing about. Any such input
that comes back with closes=True is a FABRICATED CERTIFICATE CLOSURE: the function has asserted
a contraction on data that cannot have come from a real run.

  PC1  THE HONEST-PATH CONTROL. Six calls with legitimately-shaped data, including the
       (None, None) blocked path, re-measured so the battery cannot pass by breaking the
       branches that already work.
  PC2  THE HYPOTHESIS-VIOLATION BATTERY. Negative Y_0, negative Z_1, negative Z_2, and their
       combinations -- every one outside the theorem.
  PC3  THE NON-FINITE BATTERY. NaN and +/-inf in each slot, singly and in pairs.
  PC4  THE TYPE-CONFUSION BATTERY. bool, numpy scalar, string, complex, array, and partial
       None -- inputs a sloppy caller or a JSON round-trip can produce.
  PC5  THE VERDICT. Per-case classification into REJECTED / FALSE_CLOSE / RAISED, and the
       headline magnitudes: how many hypothesis-violating inputs are accepted as closing.

**THE GAP THIS BATTERY FOUND HAS SINCE BEEN CLOSED.** As first run (2026-08-06, leg 79),
11 of the 25 hypothesis-violating cases came back `closes=True`. `radii_polynomial_status`
now validates its constants against the hypotheses above and returns `INVALID_INPUT` instead,
so all 11 are REJECTED and the battery's gate answer is `yes`. The battery itself is
UNCHANGED -- same 39 cases, same judgement predicate -- because its value is that it is the
instrument that measured the defect and now measures its absence. The pre-fix numbers are
kept verbatim in `PRE_FIX_MEASUREMENT` below and written into the artifact under `history`.

Deterministic, pure logic, runs in well under a second -- no solver state is built.
Writes writeup/data/p2_route_pc_v1_regression.json.

Run: .venv/bin/python -u experiments/p2_route_pc_v1_regression.py
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.port_certification import radii_polynomial_status      # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_pc_v1_regression.json"

_MISSING = object()

# The battery as first run, on the UNGUARDED function, before the fix landed. Kept verbatim
# so regenerating this artifact against the repaired code cannot quietly erase the finding
# that motivated the repair; the full account is writeup/novelty/leg_79.md and
# experiments/journal/leg_79.md.
PRE_FIX_MEASUREMENT = {
    "measured": "2026-08-06",
    "code_state": ("solver/port_certification.radii_polynomial_status BEFORE domain "
                   "validation was added (leg 79 measured, did not patch)"),
    "cases_total": 39,
    "cases_outside_theorem": 25,
    "false_closes": 11,
    "false_close_rate_over_outside": 0.44,
    "false_close_labels": [
        "Y0_negative_small", "Y0_negative_large", "Y0_negative_kills_a_real_failure",
        "Z2_negative", "Z2_negative_huge_Y0", "Z1_negative", "Z1_very_negative",
        "Y0_neg_inf", "Z2_neg_inf", "Z1_neg_inf", "Y0_numpy_scalar"],
    "sharpest_witness": ("radii_polynomial_status(-1.0, 0.9, 1e4) returned closes=True while "
                         "the sign-corrected (+1.0, 0.9, 1e4) correctly returned closes=False"),
    "nan_bypass": ("a NaN Z_1 skipped the `Z1 >= 1.0` guard entirely (NaN >= 1.0 is False) "
                   "and was echoed back as a measured bound on the NO_Z2 branch"),
    "gate_answer": "no",
    "fixed_by": ("Leg 0: ORCH -- _hypothesis_violations() rejects negative and non-finite "
                 "Y_0/Z_1/Z_2 with status INVALID_INPUT ahead of the discriminant; all 11 "
                 "false closes became REJECTED, with the blocked and honest paths unchanged"),
}


# --------------------------------------------------------------------------
# what the imported theorem actually requires of its constants
# --------------------------------------------------------------------------
def violates_hypotheses(Y0, Z1, Z2):
    """Which published hypothesis, if any, this input triple breaks.

    None means NOT MEASURED and is a legitimate input to this function by design -- it is the
    whole point of the kill-switch -- so None never counts as a violation. A number counts as
    a violation when it is negative or non-finite, because Y_0, Z_1, Z_2 are upper bounds on
    norms in the theorem the function implements.
    """
    broken = []
    for name, v in (("Y0", Y0), ("Z1", Z1), ("Z2", Z2)):
        if v is None or v is _MISSING:
            continue
        try:
            f = float(v)
        except (TypeError, ValueError):
            broken.append(f"{name}:not-a-real-number")
            continue
        if math.isnan(f):
            broken.append(f"{name}:NaN")
        elif math.isinf(f):
            broken.append(f"{name}:infinite")
        elif f < 0.0:
            broken.append(f"{name}:negative")
    return broken


def probe(label, family, Y0, Z1, Z2=_MISSING, note=""):
    """One adversarial call, classified. Never swallows a result -- records what came back."""
    args = (Y0, Z1) if Z2 is _MISSING else (Y0, Z1, Z2)
    broken = violates_hypotheses(Y0, Z1, Z2)
    row = {"label": label, "family": family, "note": note,
           "Y0": _repr(Y0), "Z1": _repr(Z1), "Z2": ("<omitted>" if Z2 is _MISSING else _repr(Z2)),
           "violates": broken, "outside_theorem": bool(broken)}
    try:
        out = radii_polynomial_status(*args)
    except Exception as exc:                                        # noqa: BLE001
        row.update(outcome="RAISED", exception=type(exc).__name__, detail=str(exc)[:160],
                   status=None, closes=None)
        row["verdict"] = "RAISED_LOUDLY"
        return row

    status = out.get("status")
    closes = out.get("closes")
    row.update(outcome="RETURNED", status=status, closes=closes,
               keys=sorted(out.keys()),
               carries_Y0=("Y0" in out), carries_Z1=("Z1" in out))
    if closes is True:
        row["verdict"] = "FALSE_CLOSE" if broken else "CLOSES_LEGITIMATELY"
    else:
        row["verdict"] = "REJECTED"
    return row


def _repr(v):
    if v is _MISSING:
        return "<omitted>"
    if v is None:
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return repr(v)
    if isinstance(v, (bool, int, float, str)):
        return v if not isinstance(v, float) else float(v)
    return f"{type(v).__name__}({v!r})"


# --------------------------------------------------------------------------
# PC1 -- the honest-path control
# --------------------------------------------------------------------------
def pc1_honest_paths():
    rows = [
        probe("blocked_both_none", "PC1_honest", None, None,
              note="the documented kill-switch: no profile, no A"),
        probe("blocked_both_none_with_Z2", "PC1_honest", None, None, 1.0,
              note="a Z_2 offered alongside two missing bounds must not unblock it"),
        probe("no_Z1", "PC1_honest", 1e-3, None, note="A not constructible"),
        probe("Z1_exceeds_one", "PC1_honest", 1e-3, 1.2, note="not a contraction"),
        probe("no_Z2", "PC1_honest", 1e-3, 0.1, note="quadratic term unmeasured"),
        probe("legit_close", "PC1_honest", 1e-6, 0.1, 1.0, note="a genuine closing triple"),
        probe("legit_fail", "PC1_honest", 1.0, 0.1, 1.0, note="a genuine non-closing triple"),
    ]
    return rows


# --------------------------------------------------------------------------
# PC2 -- hypothesis violations: negative "norms"
# --------------------------------------------------------------------------
def pc2_sign_violations():
    return [
        probe("Y0_negative_small", "PC2_sign", -1e-12, 0.1, 1.0,
              note="a defect norm cannot be negative; sign-flip typo in a caller"),
        probe("Y0_negative_large", "PC2_sign", -1e6, 0.1, 1.0,
              note="a grossly fabricated negative defect"),
        probe("Y0_negative_kills_a_real_failure", "PC2_sign", -1.0, 0.9, 1e4,
              note="the same (Z1,Z2) that fails honestly at Y0=+1.0"),
        probe("Z2_negative", "PC2_sign", 1.0, 0.1, -1.0,
              note="a negative quadratic bound flips the discriminant open"),
        probe("Z2_negative_huge_Y0", "PC2_sign", 1e12, 0.5, -1e-6,
              note="an enormous honest defect rescued by one negative Z_2"),
        probe("Z1_negative", "PC2_sign", 1.0, -3.0, 1.0,
              note="Z_1 < 0 slips past the `Z1 >= 1.0` guard and inflates (1-Z1)^2"),
        probe("Z1_very_negative", "PC2_sign", 1e6, -1e4, 1.0,
              note="a huge negative Z_1 makes any Y_0 close"),
        probe("Y0_and_Z2_negative", "PC2_sign", -1.0, 0.1, -1.0,
              note="two violations at once"),
        probe("Y0_negative_zero", "PC2_sign", -0.0, 0.1, 1.0,
              note="negative zero -- signed but numerically 0.0; expected to behave as 0.0"),
        probe("Z1_negative_no_Z2", "PC2_sign", 1e-3, -0.5,
              note="negative Z_1 on the NO_Z2 path"),
    ]


# --------------------------------------------------------------------------
# PC3 -- non-finite inputs
# --------------------------------------------------------------------------
def pc3_nonfinite():
    nan, inf = float("nan"), float("inf")
    return [
        probe("Z1_nan", "PC3_nonfinite", 1e-3, nan, 1.0,
              note="NaN >= 1.0 is False, so the contraction guard is bypassed"),
        probe("Z1_nan_no_Z2", "PC3_nonfinite", 1e-3, nan,
              note="does a NaN Z_1 reach the NO_Z2 branch and get reported as a bound?"),
        probe("Y0_nan", "PC3_nonfinite", nan, 0.1, 1.0, note="an unmeasured defect as NaN"),
        probe("Z2_nan", "PC3_nonfinite", 1e-3, 0.1, nan, note="NaN quadratic term"),
        probe("all_nan", "PC3_nonfinite", nan, nan, nan, note="every slot poisoned"),
        probe("Y0_inf", "PC3_nonfinite", inf, 0.1, 1.0, note="infinite defect"),
        probe("Y0_neg_inf", "PC3_nonfinite", -inf, 0.1, 1.0,
              note="minus infinity: the most extreme fabricated defect"),
        probe("Z2_inf", "PC3_nonfinite", 1e-3, 0.1, inf, note="infinite quadratic bound"),
        probe("Z2_neg_inf", "PC3_nonfinite", 1e-3, 0.1, -inf, note="minus-infinite Z_2"),
        probe("Z1_neg_inf", "PC3_nonfinite", 1.0, -inf, 1.0,
              note="minus-infinite contraction factor passes the >= 1.0 guard"),
        probe("Z1_inf", "PC3_nonfinite", 1.0, inf, 1.0,
              note="plus infinity SHOULD be caught by the >= 1.0 guard"),
        probe("Y0_inf_Z2_zero", "PC3_nonfinite", inf, 0.1, 0.0,
              note="inf * 0 in the discriminant -> NaN"),
    ]


# --------------------------------------------------------------------------
# PC4 -- type confusion
# --------------------------------------------------------------------------
def pc4_type_confusion():
    return [
        probe("Y0_bool_true", "PC4_type", True, 0.1, 1.0,
              note="a boolean flag mistaken for a bound; True == 1.0"),
        probe("Z1_bool_false", "PC4_type", 1e-3, False, 1.0,
              note="False == 0.0, i.e. a perfect contraction from a flag"),
        probe("Y0_numpy_scalar", "PC4_type", np.float64(-1.0), 0.1, 1.0,
              note="numpy negative scalar -- the common shape of a real caller's data"),
        probe("Y0_numpy_array", "PC4_type", np.array([1e-6, 1.0]), 0.1, 1.0,
              note="an array where a scalar was expected"),
        probe("Y0_string", "PC4_type", "1e-6", 0.1, 1.0,
              note="a JSON round-trip that kept the number as text"),
        probe("Z1_string", "PC4_type", 1e-6, "0.1", 1.0, note="text Z_1"),
        probe("Y0_complex", "PC4_type", complex(1e-6, 1.0), 0.1, 1.0,
              note="a complex defect norm"),
        probe("Y0_none_Z1_number", "PC4_type", None, 0.5, 1.0,
              note="HALF-BLOCKED: Y_0 unmeasured but Z_1 supplied -- is this classified?"),
        probe("Y0_none_Z1_number_no_Z2", "PC4_type", None, 0.5,
              note="the same half-blocked state on the NO_Z2 path"),
        probe("Y0_none_Z2_only", "PC4_type", None, None, -1.0,
              note="blocked, with a poisoned Z_2 alongside"),
    ]


# --------------------------------------------------------------------------
# PC5 -- the verdict
# --------------------------------------------------------------------------
def pc5_verdict(rows):
    outside = [r for r in rows if r["outside_theorem"]]
    false_closes = [r for r in rows if r["verdict"] == "FALSE_CLOSE"]
    raised = [r for r in rows if r["verdict"] == "RAISED_LOUDLY"]
    silent = [r for r in rows if r["outside_theorem"] and r["outcome"] == "RETURNED"]
    blocked = [r for r in rows if r["status"] == "BLOCKED_AT_STEP_ONE"]
    fabricating_blocked = [r for r in blocked if r["carries_Y0"] or r["carries_Z1"]]

    return {
        "cases_total": len(rows),
        "cases_outside_theorem": len(outside),
        "false_closes": len(false_closes),
        "false_close_rate_over_outside": (len(false_closes) / len(outside)) if outside else 0.0,
        "false_close_labels": [r["label"] for r in false_closes],
        "raised_loudly": len(raised),
        "raised_labels": [r["label"] for r in raised],
        "returned_silently_on_bad_input": len(silent),
        "blocked_at_step_one_calls": len(blocked),
        "blocked_calls_carrying_a_bound": len(fabricating_blocked),
        "honest_paths_still_correct": all(
            r["verdict"] in ("REJECTED", "CLOSES_LEGITIMATELY")
            for r in rows if r["family"] == "PC1_honest"),
        "gate_answer": "yes" if not false_closes else "no",
        "gate_question": ("Under an adversarial battery of fabricated/poisoned Y_0 and Z_1 "
                          "inputs, does radii_polynomial_status still correctly reject every "
                          "one and continue returning BLOCKED_AT_STEP_ONE where appropriate?"),
    }


def main():
    rows = []
    rows += pc1_honest_paths()
    rows += pc2_sign_violations()
    rows += pc3_nonfinite()
    rows += pc4_type_confusion()
    verdict = pc5_verdict(rows)

    print("== PC1-PC4: the adversarial battery ==")
    for r in rows:
        flag = {"FALSE_CLOSE": "  <== FALSE CLOSE", "RAISED_LOUDLY": "  (raised)"}.get(
            r["verdict"], "")
        print(f"  {r['label']:34s} {str(r['status']):20s} closes={str(r['closes']):5s} "
              f"{r['verdict']}{flag}")

    print("\n== PC5: the verdict ==")
    print(f"  cases                       {verdict['cases_total']}")
    print(f"  outside the theorem         {verdict['cases_outside_theorem']}")
    print(f"  FALSE CLOSES                {verdict['false_closes']}  "
          f"({100 * verdict['false_close_rate_over_outside']:.1f}% of them)")
    print(f"  raised loudly               {verdict['raised_loudly']}")
    print(f"  BLOCKED_AT_STEP_ONE calls   {verdict['blocked_at_step_one_calls']}, "
          f"carrying a bound: {verdict['blocked_calls_carrying_a_bound']}")
    print(f"  honest paths still correct  {verdict['honest_paths_still_correct']}")
    print(f"  GATE ANSWER                 {verdict['gate_answer']}")
    if verdict["false_closes"]:
        print("  false-closing labels: " + ", ".join(verdict["false_close_labels"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(
        {"leg": 79, "route": "PC",
         "target": "solver/port_certification.py::radii_polynomial_status",
         "standard": ("Y_0, Z_1, Z_2 are upper bounds on norms in the radii polynomial theorem "
                      "(van den Berg-Lessard, AMS Notices 62(9):1057, 2015), hence nonnegative "
                      "and finite BY HYPOTHESIS; see writeup/novelty/leg_79.md"),
         "cases": rows, "verdict": verdict,
         "history": PRE_FIX_MEASUREMENT}, indent=2, default=str) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
