#!/usr/bin/env python3
"""Leg 383, Route-ST2G -- the adversarial battery for the DSSP screen's two
new report columns (Tsai 1998 Theorem 2's decay-only route, and the SS/DSS
ansatz check), driven END TO END through screen_candidate().

WHY THIS FILE EXISTS SEPARATELY FROM test_dssp_screen.py
------------------------------------------------------------------------------
Legs 362 and 370 landed the T2 route and the ansatz classifier as functions,
with controls, and those controls all point the SAME way: a planted case that
SHOULD be excluded, and is. That is a fire-direction battery. An instrument
that can only fire is a tautology -- this repository has been burned by exactly
that (leg 340) -- so half of the six controls below exist to make the screen
FAIL to exclude, on fields no theorem in the ledger reaches.

The six controls, and their required directions, were PRE-REGISTERED before any
line of this leg's construction was written, in writeup/novelty/leg_383.md,
committed at 1ca4ce5. They are not renegotiable here. A control that does not
fire is a STOP and a verbatim report, never a widening of the control (leg 361).

  Direction A -- the screen MUST fire:
    C1  Tsai's own headline example (eq 1.5, U ~ A(y/|y|)/|y|)  -> EXCLUDED-BY-T2
    C2  this programme's DSS object (field_uB + periodic lambda>1) -> NOT-REACHED-BY-ANSATZ
    C3  exponent -2 field, L^3 genuinely convergent             -> EXCLUDED-BY-T1
  Direction B -- the screen MUST NOT fire:
    C4  field tending to a NONZERO constant at infinity         -> NOT EXCLUDED
    C5  the C1 field's ansatz column is EXACT-SS (not a catch-all)
    C6  field GROWING like |y|                                  -> NOT EXCLUDED

  Regression R: machine_read_ledger()'s two-positional-argument form still
  returns leg 357's exact shape, and screen_candidate()'s ledger key set is
  unmoved -- the only thing that changes is WHAT the NRS_Tsai row says.

CEILING: TIER 2. Surviving this screen is not evidence for existence.

Convention: self-running script, no pytest -- `.venv/bin/python test_dssp_screen_t2.py`.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver.dssp_biot_savart import field_uB  # noqa: E402
from solver.dssp_screen import (  # noqa: E402
    classify_ss_ansatz,
    l3_norm_ladder,
    lambda_from_trajectory,
    machine_read_ledger,
    screen_candidate,
)

# A short ladder and modest quadrature: this file is a CLASSIFIER battery, not a
# convergence study. Every field below has a closed-form decay rate, so the
# classification does not depend on quadrature refinement -- and C3's L^3
# convergence flag is checked against its own analytic expectation, not assumed.
LADDER = (10.0, 100.0, 1e3, 1e4)
NQ = dict(n_r=120, n_c=24, n_phi=8)


# ---------------------------------------------------------------------------
# The planted fields. C1 reuses leg 362's own planted profile shape verbatim
# rather than inventing a second one.
# ---------------------------------------------------------------------------

def field_c1_tsai_headline(x):
    """U(y) = (y/|y|) * 1/|y| -- Tsai 1998's headline motivating example
    (1.5), "U(y) = A(y/|y|) * 1/|y| + o(1/|y|)", with A(theta) = theta.
    Decay exponent EXACTLY -1. |U|^3 ~ 1/r^3, so the R^3 volume integral is
    LOGARITHMICALLY divergent: outside Theorem 1's hypothesis, inside
    Theorem 2's."""
    x = np.asarray(x, dtype=float)
    r = np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)
    return x / (r * r)


def field_c3_exponent_minus_two(x):
    """U(y) = (y/|y|) * 1/|y|^2, decay exponent EXACTLY -2. |U|^3 ~ 1/r^6
    against the r^2 dr measure, so the L^3 integral genuinely CONVERGES --
    this one lands inside the stricter L^q route."""
    x = np.asarray(x, dtype=float)
    r = np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)
    return x / (r * r * r)


def field_c4_tends_to_nonzero_constant(x):
    """U(y) = e_x * (1 - 1/2 * 1/(1+|y|)) -- magnitude rises monotonically to
    1 and is bounded away from 0. It does NOT tend to zero at infinity, so
    Theorem 2's finishing hypothesis (Tsai 1998 p.49, "U -> 0 at infinity")
    is NOT met and the T2 column must stay silent."""
    x = np.asarray(x, dtype=float)
    r = np.linalg.norm(x, axis=-1)
    out = np.zeros_like(x)
    out[..., 0] = 1.0 - 0.5 / (1.0 + r)
    return out


def field_c6_growing(x):
    """U(y) = y, magnitude GROWING like |y|^{+1}. No theorem in the ledger
    reaches it: L^3 divergent, no decay to zero. Every column must stay
    silent."""
    return np.asarray(x, dtype=float)


def _periodic_dss_trajectory():
    """A genuinely periodic trajectory at lambda > 1 under the rescaled flow,
    using leg 357's own landed period-detector convention S0 = 2*log(lambda)
    -- the same construction leg 362's control 2 uses. This is the operational
    DSS signature: a periodic-in-log-time orbit, NOT a fixed point."""
    S0_true = 2.0
    s = np.linspace(0.0, 3.0, 3001)
    c = 0.5 * np.cos(2.0 * np.pi * s / S0_true) + 0.5000001
    c[0] = 1.0000001
    return s, c


# ---------------------------------------------------------------------------
# Direction A -- the screen MUST fire
# ---------------------------------------------------------------------------

def test_c1_tsai_headline_example_reads_excluded_by_t2():
    """C1, the gate's clause (i). Tsai's own headline example must be REACHED
    by Theorem 2, through the report path, with the deciding clause naming
    Theorem 2's finishing hypothesis and not any L^3 clause."""
    res = screen_candidate(field_c1_tsai_headline, R_hi_ladder=LADDER, **NQ)
    exponent = res["far_field_decay"]["fitted_exponent"]
    row = res["ledger"]["NRS_Tsai"]

    # The source's exponent (Tsai 1998 eq 1.5: exactly -1) against the
    # measurement, reported as a magnitude, not a boolean.
    assert abs(exponent - (-1.0)) < 0.05, f"C1 fitted exponent {exponent!r} is not ~ -1"
    assert res["l3_norm"]["converged"] is False, (
        "C1 must sit OUTSIDE Theorem 1's hypothesis (log-divergent L^3); "
        f"ladder reports converged={res['l3_norm']['converged']!r}")
    assert row["verdict"] == "EXCLUDED-BY-T2", (
        f"C1 FAILED TO FIRE: verdict {row['verdict']!r}, expected EXCLUDED-BY-T2")
    assert row["excludes"] is True
    assert "Theorem 2" in row["deciding_clause"]
    assert "U -> 0 at infinity" in row["deciding_clause"]
    assert res["theorem2_decay_to_zero"]["decays_to_zero"] is True
    print(f"[ok] C1 FIRED: fitted exponent {exponent:.10f} vs Tsai 1998 eq (1.5)'s "
          f"exact -1 (|diff| {abs(exponent + 1.0):.3e}), L^3 rel_change_last_step "
          f"{res['l3_norm']['rel_change_last_step']:.4f} > tol "
          f"{res['l3_norm']['rel_tol']!r} -> EXCLUDED-BY-T2")


def test_c2_repo_dss_object_reads_not_reached_by_ansatz():
    """C2, the gate's clause (ii). This programme's DSS object must read NOT
    REACHED, and the DECIDING CLAUSE recorded must be the exact-SS ansatz
    hypothesis (Tsai 1998 eq (1.2)_1) -- not a decay clause, not an L^3
    clause. If the deciding clause were a decay clause, clause (ii) would be
    answered for the wrong reason."""
    s, c = _periodic_dss_trajectory()
    res = screen_candidate(field_uB, s_vals=s, c_vals=c, R_hi_ladder=LADDER, **NQ)
    row = res["ledger"]["NRS_Tsai"]
    lam = res["lambda"]["lambda"]

    assert res["lambda"]["measured"] is True, (
        "C2's trajectory must be detected as genuinely periodic, else the "
        "object is not being screened as DSS at all")
    assert lam is not None and lam > 1.0, f"C2 measured lambda {lam!r} is not > 1"
    assert res["ss_ansatz"]["ansatz"] == "DSS"
    assert res["ss_ansatz"]["satisfies_theorem_ansatz"] is False
    assert row["verdict"] == "NOT-REACHED-BY-ANSATZ", (
        f"C2 FAILED TO FIRE: verdict {row['verdict']!r}, expected "
        "NOT-REACHED-BY-ANSATZ")
    assert row["excludes"] is False
    assert "(1.2)" in row["deciding_clause"], (
        "C2's deciding clause must be the exact-SS ansatz eq (1.2); got: "
        f"{row['deciding_clause']!r}")
    assert "EXACT" in row["deciding_clause"]
    # The deciding clause must NOT be a decay/integrability clause.
    assert "Theorem 2" not in row["deciding_clause"] or "eq (1.2)" in row["deciding_clause"]
    print(f"[ok] C2 FIRED: measured lambda {lam!r} > 1 (S0 = {res['lambda']['S0']!r} "
          f"= 2*log(lambda)), fitted exponent "
          f"{res['far_field_decay']['fitted_exponent']:.6f} -> NOT-REACHED-BY-ANSATZ, "
          "deciding clause = Tsai 1998 eq (1.2)_1, the exact-SS ansatz")


def test_c3_l3_convergent_field_reads_excluded_by_t1_not_t2():
    """C3. The two columns must be DISTINGUISHABLE -- one flag wearing two
    names would make the gate meaningless. A field decaying at exponent -2 has
    a genuinely convergent L^3 integral and must be caught by the stricter
    L^q route, reported as EXCLUDED-BY-T1, even though it ALSO decays to zero
    (so T2 would have fired had T1 not been checked first)."""
    res = screen_candidate(field_c3_exponent_minus_two, R_hi_ladder=LADDER, **NQ)
    exponent = res["far_field_decay"]["fitted_exponent"]
    row = res["ledger"]["NRS_Tsai"]

    assert abs(exponent - (-2.0)) < 0.05, f"C3 fitted exponent {exponent!r} is not ~ -2"
    assert res["l3_norm"]["converged"] is True, (
        "C3's L^3 ladder must genuinely converge (analytic: |U|^3 ~ r^-6 "
        f"against r^2 dr); got rel_change_last_step "
        f"{res['l3_norm']['rel_change_last_step']!r}")
    assert res["theorem2_decay_to_zero"]["decays_to_zero"] is True, (
        "C3 also decays to zero -- the point of this control is that T1 is "
        "checked FIRST and is the stronger statement")
    assert row["verdict"] == "EXCLUDED-BY-T1", (
        f"C3 FAILED TO FIRE: verdict {row['verdict']!r}, expected EXCLUDED-BY-T1")
    print(f"[ok] C3 FIRED: fitted exponent {exponent:.10f} ~ -2, L^3 norm "
          f"{res['l3_norm']['L3_norm']:.6f} converged (rel_change_last_step "
          f"{res['l3_norm']['rel_change_last_step']:.3e} < tol "
          f"{res['l3_norm']['rel_tol']!r}) -> EXCLUDED-BY-T1, distinct from T2")


# ---------------------------------------------------------------------------
# Direction B -- the screen MUST NOT fire
# ---------------------------------------------------------------------------

def test_c4_nonzero_limit_field_is_not_excluded():
    """C4. THE ANTI-TAUTOLOGY CONTROL. A field whose magnitude tends to a
    NONZERO constant fails Theorem 2's finishing hypothesis outright. If the
    T2 column fired here, it would be excluding everything and measuring
    nothing -- the leg-340 burn."""
    res = screen_candidate(field_c4_tends_to_nonzero_constant, R_hi_ladder=LADDER, **NQ)
    row = res["ledger"]["NRS_Tsai"]
    t2 = res["theorem2_decay_to_zero"]
    mags = res["far_field_decay"]["magnitudes"]

    assert res["l3_norm"]["converged"] is False, (
        "C4 must sit outside Theorem 1's hypothesis too, else this control "
        "tests nothing about T2")
    assert t2["decays_to_zero"] is False, (
        "C4 CONTROL FAILED: the T2 column fired on a field that does not "
        f"decay to zero (first sampled |U| {mags[0]!r}, last {mags[-1]!r})")
    assert row["verdict"] == "NOT EXCLUDED", (
        f"C4 CONTROL FAILED: verdict {row['verdict']!r}, expected NOT EXCLUDED")
    assert row["excludes"] is False
    print(f"[ok] C4 SILENT (as required): |U| runs {mags[0]:.6f} -> {mags[-1]:.6f} "
          f"(rises toward 1, bounded away from 0), fitted exponent "
          f"{res['far_field_decay']['fitted_exponent']:.6f} ~ 0 -> NOT EXCLUDED")


def test_c5_ansatz_column_is_not_a_catch_all():
    """C5. If the ansatz column fired on everything, C2's NOT-REACHED verdict
    would be vacuous. A static, non-periodic exact-SS candidate must be
    classified EXACT-SS and adjudicated on its decay -- NOT deflected to
    NOT-REACHED-BY-ANSATZ."""
    res = screen_candidate(field_c1_tsai_headline, R_hi_ladder=LADDER, **NQ)
    ans = res["ss_ansatz"]
    row = res["ledger"]["NRS_Tsai"]

    assert ans["ansatz"] == "EXACT-SS", (
        f"C5 CONTROL FAILED: static candidate classified {ans['ansatz']!r}")
    assert ans["satisfies_theorem_ansatz"] is True
    assert ans["measured_lambda"] is None
    assert row["verdict"] != "NOT-REACHED-BY-ANSATZ", (
        "C5 CONTROL FAILED: the ansatz clause deflected a non-DSS candidate, "
        "which would make C2's verdict vacuous")
    # And the contrast, in one process: the SAME classifier on a lambda>1
    # trajectory must go the other way.
    s, c = _periodic_dss_trajectory()
    dss = classify_ss_ansatz(lambda_from_trajectory(s, c, return_tol=1e-2))
    assert dss["ansatz"] == "DSS" and dss["satisfies_theorem_ansatz"] is False
    print(f"[ok] C5 SILENT (as required): static candidate -> ansatz EXACT-SS, "
          f"satisfies=True, adjudicated by decay instead (verdict "
          f"{row['verdict']!r}); same classifier on lambda="
          f"{dss['measured_lambda']!r} -> DSS, satisfies=False")


def test_c6_growing_field_fires_nothing():
    """C6. A field growing like |y| is reached by no theorem in the ledger.
    Every column must stay silent and no clause may be claimed."""
    res = screen_candidate(field_c6_growing, R_hi_ladder=LADDER, **NQ)
    row = res["ledger"]["NRS_Tsai"]
    exponent = res["far_field_decay"]["fitted_exponent"]

    assert exponent > 0.5, f"C6 fitted exponent {exponent!r} is not clearly growing"
    assert res["l3_norm"]["converged"] is False
    assert res["theorem2_decay_to_zero"]["decays_to_zero"] is False
    assert res["ss_ansatz"]["satisfies_theorem_ansatz"] is True
    assert row["verdict"] == "NOT EXCLUDED", (
        f"C6 CONTROL FAILED: verdict {row['verdict']!r} on a growing field")
    assert row["excludes"] is False
    assert "deciding_clause" not in row, (
        "C6 CONTROL FAILED: a clause was claimed on a field no theorem reaches")
    print(f"[ok] C6 SILENT (as required): fitted exponent {exponent:.10f} (growth), "
          "L^3 divergent, T2 unmet -> NOT EXCLUDED, no clause claimed")


# ---------------------------------------------------------------------------
# Regression guard and the both-directions meta-check
# ---------------------------------------------------------------------------

def test_regression_machine_read_ledger_default_shape_unmoved():
    """R. This leg rewires screen_candidate() only. machine_read_ledger()'s
    own two-positional-argument form must still reproduce leg 357's shape
    exactly (no Morrey key, binary NRS_Tsai row), so legs 362's and 370's
    backward-compatibility guarantees for direct callers still hold."""
    l3 = l3_norm_ladder(field_uB, R_hi_ladder=LADDER, **NQ)
    lam = {"lambda": None, "S0": None, "measured": False, "reason": "static"}
    led = machine_read_ledger(l3, lam)
    assert set(led.keys()) == {"NRS_Tsai", "Chae_Tsai", "Pineau_Vicol", "reportable"}
    assert set(led["NRS_Tsai"].keys()) == {"excludes", "verdict", "reason"}, (
        "leg 357's binary NRS_Tsai shape moved for direct callers: "
        f"{sorted(led['NRS_Tsai'].keys())}")
    # screen_candidate()'s LEDGER key set is likewise unmoved; what changed is
    # only what the NRS_Tsai row now says, plus two new top-level columns.
    res = screen_candidate(field_uB, R_hi_ladder=LADDER, **NQ)
    assert set(res["ledger"].keys()) == {"NRS_Tsai", "Chae_Tsai", "Pineau_Vicol", "reportable"}
    assert "theorem2_decay_to_zero" in res and "ss_ansatz" in res
    print("[ok] R: machine_read_ledger() two-arg form unmoved (leg 357 shape); "
          "screen_candidate() ledger keys unmoved; two new top-level columns present")


def test_battery_can_fail_in_both_directions():
    """The gate's own qualifier, checked as a property of the battery rather
    than asserted in prose: the same code path, on planted inputs, produces
    BOTH exclusions and non-exclusions. An instrument that could only fire
    would pass every control above except this one."""
    fired = []
    silent = []
    for name, fn, kwargs in (
        ("C1", field_c1_tsai_headline, {}),
        ("C3", field_c3_exponent_minus_two, {}),
        ("C4", field_c4_tends_to_nonzero_constant, {}),
        ("C6", field_c6_growing, {}),
    ):
        v = screen_candidate(fn, R_hi_ladder=LADDER, **NQ, **kwargs)["ledger"]["NRS_Tsai"]
        (fired if v["excludes"] else silent).append((name, v["verdict"]))
    s, c = _periodic_dss_trajectory()
    v2 = screen_candidate(field_uB, s_vals=s, c_vals=c,
                           R_hi_ladder=LADDER, **NQ)["ledger"]["NRS_Tsai"]
    silent.append(("C2", v2["verdict"]))

    assert len(fired) >= 2 and len(silent) >= 2, (
        f"battery is one-directional: fired={fired}, silent={silent}")
    verdicts = {v for _, v in fired + silent}
    assert verdicts >= {"EXCLUDED-BY-T1", "EXCLUDED-BY-T2",
                        "NOT-REACHED-BY-ANSATZ", "NOT EXCLUDED"}, (
        f"not all four verdicts are reachable through the report path: {verdicts}")
    print(f"[ok] both directions reachable: fired={fired}, silent={silent}")


if __name__ == "__main__":
    test_c1_tsai_headline_example_reads_excluded_by_t2()
    test_c2_repo_dss_object_reads_not_reached_by_ansatz()
    test_c3_l3_convergent_field_reads_excluded_by_t1_not_t2()
    test_c4_nonzero_limit_field_is_not_excluded()
    test_c5_ansatz_column_is_not_a_catch_all()
    test_c6_growing_field_fires_nothing()
    test_regression_machine_read_ledger_default_shape_unmoved()
    test_battery_can_fail_in_both_directions()
    print("\nAll 8 checks pass (6 pre-registered controls + regression + "
          "both-directions meta-check). CEILING: TIER 2 -- surviving a screen "
          "is not evidence for existence.")
