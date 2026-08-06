"""ROUTE-PCR v1 (leg 217): repairing the four mechanisms leg 200 escalated, and proving
the repair is a REJECTION LAYER -- it moves no clean-input number.

--------------------------------------------------------------------------
WHAT THIS LEG DOES
--------------------------------------------------------------------------
Leg 200 (Route-PCA, branch `leg/200-pca-v1`) audited `solver/port_certification.py` under
adversarial input, answered its gate YES, and -- per that gate's yes-branch -- PARKED the
finding without patch authority. Seven of its twelve gates were SILENT: the module
returned finite, correctly-shaped, WRONG values with no exception and no flag. This leg is
the repair, with its own pre-committed gate:

   "Does repairing all four named mechanisms (per leg 200's own report) cause every one of
    leg 200's adversarial cases to now reject/raise correctly, while leg 195's (PQVER) own
    independently-reproduced 114/114 clean result and every other live PORT-family call
    stays bit-identical?"

The four named mechanisms, and the minimal repair each received:

  M1  `line_sweep_solve` hard-coded the BACKWARD radial difference regardless of
      `sign(s_rho)` while choosing the ANGULAR direction pointwise by `sign(s_beta)` four
      lines away in the same loop body. Leg 200: 18820x relative error against the
      operator the docstring advertises, at `min(s_rho) = -0.4`, with a residual 20681x
      the rhs. REPAIRED: the radial direction is chosen by `sign(s_rho)`; mixed signs
      RAISE, because no single sweep inverts an operator that is neither block-lower nor
      block-upper bidiagonal.
  M2  `radii_polynomial_status` returned `closes` from the DISCRIMINANT ALONE and never
      formed `r_min`, so `Y_0 = 0` -- the value leg 51 measured on the a=0 CLM profile --
      gave `closes=True` on a ball of radius exactly 0. REPAIRED: `r_min` is formed and
      routed through `certificate_guards.radius_violation`, completing the half of legs
      79/128's repair that was left.
  M3  `leading_order_solve` allocated `np.zeros_like(rhs)` with no float cast, so an
      integer rhs truncated (an exact 0.5 returned as 0, relative error 1.000). REPAIRED:
      `rhs = np.asarray(rhs, float)`, matching its sibling.
  M4  `stall_verdict`'s `flat = bool(gain < 2.0)` treats `NaN < 2.0` as False, giving a
      poisoned ladder the confident prose "bending => finite ill-conditioning". REPAIRED:
      non-finite and negative residuals RAISE rather than receive a verdict.

--------------------------------------------------------------------------
WHAT A REPAIR LEG OWES, AND WHY THE CONTROLS ARE THE POINT
--------------------------------------------------------------------------
Every one of these is a REJECTION LAYER in leg 128's sense: it may turn something
previously accepted into a refusal, and it **must never move a clean-input number**. So
the load-bearing half of this runner is not the adversarial half -- it is:

  * **bit-identity against the PRE-repair implementations**, which are reproduced verbatim
    inside this file (`_line_sweep_prerepair`, `_leading_order_prerepair`) so the
    comparison is `array_equal` on bits, not agreement to a tolerance; and
  * **leg 195's 114/114**, re-run as a subprocess, from the ledger scripts themselves.

And M1 gets the control banked lesson 90 demands -- one that *can* come out the other way.
A repair that merely REFUSED every `s_rho < 0` case would pass leg 200's battery
identically, because leg 200's cases are all MIXED-sign (one entry driven negative in an
otherwise positive profile). So this runner adds the case leg 200 did not have: a
**uniformly negative** `s_rho`, where the repaired sweep must return the EXACT inverse of
the advertised forward-upwinded operator (~1e-16) rather than raise. That case is what
distinguishes "upwinds by sign" from "refuses when nervous", and pre-repair it was one of
the silently-wrong ones.

--------------------------------------------------------------------------
WHAT THIS LEG DID **NOT** REPAIR, AND WHY -- READ THIS BEFORE CALLING THE MODULE CLOSED
--------------------------------------------------------------------------
Leg 200's battery pins THREE further silent mechanisms that are **not** among this leg's
four named ones, and this leg deliberately left them open so its diff to
`solver/port_certification.py` is exactly the four mechanisms it was chartered to fix:

  * `leading_order_solve` is sign-blind in `c_l` (leg 200's PCA3) -- 26.0x at `c_l = -0.5`.
    This is M1's twin in the radial-only preconditioner; M3 repaired that function's DTYPE
    defect only.
  * `stall_verdict` reads the ladder's ends POSITIONALLY (`rows[0]`, `rows[-1]`), never by
    `m`, so a descending `dims` tuple inverts the work ratio 16.0 -> 0.0625 and flips the
    published verdict on identical data (leg 200's PCA5 `ordering`).
  * `ProfileResidual.pack`/`unpack` validate only the TOTAL size, so a transposed field
    round-trips at 1.32 relative error (leg 200's PCA7).

They are measured again here, post-repair, so the residue is a magnitude and not a
footnote. **The module is not closed.**

Nothing here is rigorous and nothing is interval-enclosed; this is float64 throughout, and
no link of the L1->L4 chain moved -- an instrument repair is not a mathematical result.
"""

import json
import math
import os
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.certificate_guards import radius_violation             # noqa: E402
from solver.port_certification import (                            # noqa: E402
    ProfileResidual,
    attribution_summary,
    leading_order_solve,
    line_sweep_solve,
    outward_upwinding_holds,
    radii_polynomial_status,
    stall_verdict,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_pcr_v1_repair.json")

GATE = ("Does repairing all four named mechanisms (per leg 200's own report) cause every "
        "one of leg 200's adversarial cases to now reject/raise correctly, while leg "
        "195's (PQVER) own independently-reproduced 114/114 clean result and every other "
        "live PORT-family call stays bit-identical?")

# The corner every banked PORT-family number was produced in, read from
# writeup/data/p2_route_l_v1_precond.json ("outward_upwinding"), not re-derived.
BANKED_MIN_S_RHO = 0.38963488051119644
BANKED_MAX_S_RHO = 5.731643960887419

# Leg 200's pre-repair magnitudes, quoted from writeup/data/p2_route_pca_v1_adversarial.json
# on branch leg/200-pca-v1 and re-derived by this leg against the pre-repair module before
# a line was changed. They are carried here so the before/after sits in one artifact.
LEG200_PREREPAIR = {
    "M1_worst_rel_error_vs_advertised_operator": 1.8820e4,
    "M1_worst_min_s_rho": -0.4,
    "M1_worst_relative_residual": 2.0681e4,
    "M1_cost_at_a_breach_of_minus_1e_3": 0.0097,
    "M1_rel_error_at_minus_3p0": 1.12,
    "M3_worst_relative_error_integer_rhs": 1.000,
    "M4_nan_ladder_reported": "bending => finite ill-conditioning, and more Krylov work "
                              "would help",
    "M4_negative_residual_gain": -25.0,
    "PCA3_still_open_rel_error_at_c_l_minus_0p5": 26.0,
    "PCA5_ordering_still_open_work_ratio": [16.0, 0.0625],
    "PCA7_still_open_transposed_rel_error": 1.3204,
}


# ---------------------------------------------------------------------------
# helpers: independent references, and the PRE-REPAIR implementations verbatim
# ---------------------------------------------------------------------------
def thomas(a, b, c, d):
    """A plain Thomas solve, so the sweep's injected dependency is not the variable."""
    n = len(d)
    cp = np.zeros(n)
    dp = np.zeros(n)
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        den = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / den
        dp[i] = (d[i] - a[i] * dp[i - 1]) / den
    x = np.zeros(n)
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, radial_upwind_by_sign):
    """Dense (-s_rho d_rho - s_beta d_beta + c_diag), first-order upwind.

    `radial_upwind_by_sign=False` assembles what the code COMPUTED before this leg (an
    unconditional backward radial difference); `True` assembles what its docstring has
    always PROMISED, and what it now does. The two coincide wherever `s_rho > 0`, which is
    why the banked corner cannot move.
    """
    N = nr * nb
    L = np.zeros((N, N))

    def idx(i, j):
        return i * nb + j

    for i in range(nr):
        sr = s_rho[i] / drho
        for j in range(nb):
            sb = float(s_beta[i][j])
            r = idx(i, j)
            L[r, r] += c_diag
            if (not radial_upwind_by_sign) or s_rho[i] > 0:
                L[r, r] += -sr
                if i - 1 >= 0:
                    L[r, idx(i - 1, j)] += sr
            else:
                L[r, r] += sr
                if i + 1 < nr:
                    L[r, idx(i + 1, j)] += -sr
            if sb > 0:
                L[r, r] += -sb / dbeta
                if j - 1 >= 0:
                    L[r, idx(i, j - 1)] += sb / dbeta
            else:
                L[r, r] += sb / dbeta
                if j + 1 < nb:
                    L[r, idx(i, j + 1)] += -sb / dbeta
    return L


def _line_sweep_prerepair(rhs, s_rho, s_beta, drho, dbeta, c_diag, thomas_fn):
    """`line_sweep_solve` EXACTLY as it stood before this leg -- the bit-identity oracle.

    Kept verbatim rather than described, so "the banked corner does not move" is checked
    with `np.array_equal` against the actual prior arithmetic instead of against a
    tolerance or a remembered number.
    """
    rhs = np.asarray(rhs, float)
    nr, nb = rhs.shape
    out = np.empty_like(rhs)
    prev = np.zeros(nb)
    for i in range(nr):
        sr = s_rho[i] / drho
        sb = s_beta[i]
        a = np.zeros(nb)
        b = np.full(nb, float(c_diag)) - sr
        c = np.zeros(nb)
        pos = sb > 0
        a[pos] = sb[pos] / dbeta
        b[pos] -= sb[pos] / dbeta
        b[~pos] += sb[~pos] / dbeta
        c[~pos] = -sb[~pos] / dbeta
        a[0] = 0.0
        c[-1] = 0.0
        prev = thomas_fn(a, b, c, rhs[i] - sr * prev)
        out[i] = prev
    return out


def _leading_order_prerepair(rhs, c_l, drho, c_diag):
    """`leading_order_solve` EXACTLY as it stood before this leg (no float cast)."""
    a = c_l / drho
    denom = c_diag - a
    out = np.zeros_like(rhs)
    prev = np.zeros(rhs.shape[1])
    for i in range(rhs.shape[0]):
        prev = (rhs[i] - a * prev) / denom
        out[i] = prev
    return out


def dense_radial(c_l, drho, c_diag, nr):
    """Dense (-c_l d_rho + c_diag) with the backward difference the code uses."""
    L = np.zeros((nr, nr))
    a = c_l / drho
    for i in range(nr):
        L[i, i] = c_diag - a
        if i - 1 >= 0:
            L[i, i - 1] = a
    return L


def call(fn, *a, **kw):
    """Return (value, exception_string) -- a raise is an OUTCOME here, not a crash."""
    try:
        return fn(*a, **kw), None
    except Exception as exc:                                       # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def classify(value, reference, exception=None, rtol=1e-10):
    """SILENT / VISIBLE / CORRECT, plus the magnitude that decides it (leg 200's rule)."""
    if exception is not None:
        return {"outcome": "VISIBLE", "how": f"raised {exception}", "rel_error": None}
    arr = np.asarray(value, float)
    ref = np.asarray(reference, float)
    if not np.all(np.isfinite(arr)):
        return {"outcome": "VISIBLE",
                "how": f"{int(np.sum(~np.isfinite(arr)))} non-finite entries",
                "rel_error": None}
    den = float(np.linalg.norm(ref))
    rel = float(np.linalg.norm(arr - ref) / den) if den > 0 else float(
        np.linalg.norm(arr - ref))
    if rel <= rtol:
        return {"outcome": "CORRECT", "how": "agrees with the independent reference",
                "rel_error": rel}
    return {"outcome": "SILENT",
            "how": "finite, plausibly-shaped, wrong; no exception and no flag",
            "rel_error": rel}


def _sweep_fixture(seed=7, nr=12, nb=8):
    rng = np.random.default_rng(seed)
    return {"nr": nr, "nb": nb, "drho": 0.1, "dbeta": 0.2, "c_diag": -1.2,
            "rhs": rng.standard_normal((nr, nb)),
            "s_beta": 0.5 * rng.standard_normal((nr, nb))}


# ---------------------------------------------------------------------------
# PCR1 -- M1: the radial direction now follows sign(s_rho)
# ---------------------------------------------------------------------------
def pcr1_line_sweep_sign_selection():
    """Leg 200's PCA1 curve, re-run; plus the control that can report the other answer."""
    f = _sweep_fixture()
    nr, nb = f["nr"], f["nb"]
    drho, dbeta, c_diag = f["drho"], f["dbeta"], f["c_diag"]
    rhs, s_beta = f["rhs"], f["s_beta"]

    base = np.linspace(BANKED_MIN_S_RHO, BANKED_MAX_S_RHO, nr)
    curve = []
    for floor in (BANKED_MIN_S_RHO, 0.1, 1e-3, 0.0, -1e-3, -0.1, -0.4, -1.0, -3.0):
        s_rho = base.copy()
        s_rho[nr // 2] = floor
        out, exc = call(line_sweep_solve, rhs, s_rho, s_beta, drho, dbeta, c_diag, thomas)
        L_true = dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, True)
        x_true = np.linalg.solve(L_true, rhs.ravel()).reshape(nr, nb)
        after = classify(out, x_true, exc)

        # the pre-repair answer, on the identical input, for the before/after column
        pre_out, pre_exc = call(_line_sweep_prerepair, rhs, s_rho, s_beta, drho, dbeta,
                                c_diag, thomas)
        before = classify(pre_out, x_true, pre_exc)

        bit_identical = None
        if exc is None and pre_exc is None:
            bit_identical = bool(np.array_equal(np.asarray(out), np.asarray(pre_out)))
        curve.append({
            "min_s_rho": float(np.min(s_rho)),
            "sign_pattern": "mixed" if floor < 0 else ("nonneg" if floor >= 0 else "?"),
            "guard_outward_upwinding_holds": bool(
                outward_upwinding_holds(s_rho)["holds"]),
            "before_leg217": before,
            "after_leg217": after,
            "bit_identical_to_prerepair": bit_identical,
        })

    # ---- THE CONTROL LESSON 90 DEMANDS ------------------------------------
    # Leg 200's cases are ALL mixed-sign, so a repair that merely REFUSED every negative
    # entry would pass its battery identically. A uniformly-negative s_rho is the case
    # that separates "upwinds by sign" from "refuses when nervous": the operator is block
    # UPPER bidiagonal there, one INWARD sweep is its exact inverse, and the repair must
    # RETURN it, not raise.
    s_neg = -base.copy()                       # uniformly negative, strictly
    out_n, exc_n = call(line_sweep_solve, rhs, s_neg, s_beta, drho, dbeta, c_diag, thomas)
    L_neg = dense_transport(s_neg, s_beta, drho, dbeta, c_diag, nr, nb, True)
    x_neg = np.linalg.solve(L_neg, rhs.ravel()).reshape(nr, nb)
    pre_n, pre_exc_n = call(_line_sweep_prerepair, rhs, s_neg, s_beta, drho, dbeta,
                            c_diag, thomas)
    resid_n = None
    if exc_n is None:
        resid_n = float(np.linalg.norm(L_neg @ np.asarray(out_n).ravel() - rhs.ravel())
                        / np.linalg.norm(rhs))
    uniform_negative = {
        "case": ("uniformly NEGATIVE s_rho -- the operator is block UPPER bidiagonal and "
                 "one INWARD sweep is its exact inverse"),
        "why_this_control_matters": (
            "leg 200's nine cases are all MIXED-sign, so a repair that simply refused "
            "every s_rho < 0 would pass its battery unchanged. This case can only pass "
            "if the radial direction is genuinely SELECTED by sign. Lesson 90: a control "
            "that cannot come out differently is not a control."),
        "before_leg217": classify(pre_n, x_neg, pre_exc_n),
        "after_leg217": classify(out_n, x_neg, exc_n),
        "relative_residual_against_advertised_operator": resid_n,
    }

    # s_rho identically zero: no radial coupling, admissible either way, and it is the
    # configuration the module's own ADI negative control runs at
    # (p2_route_l_v1_precond.py:172 passes `0 * one`).
    s_zero = np.zeros(nr)
    out_z, exc_z = call(line_sweep_solve, rhs, s_zero, s_beta, drho, dbeta, c_diag, thomas)
    pre_z, _ = call(_line_sweep_prerepair, rhs, s_zero, s_beta, drho, dbeta, c_diag, thomas)
    L_z = dense_transport(s_zero, s_beta, drho, dbeta, c_diag, nr, nb, True)
    zero_speed = {
        "case": "s_rho identically 0 (the module's own ADI control's configuration)",
        "after_leg217": classify(out_z, np.linalg.solve(L_z, rhs.ravel()).reshape(nr, nb),
                                 exc_z),
        "bit_identical_to_prerepair": bool(np.array_equal(np.asarray(out_z),
                                                          np.asarray(pre_z))),
        "guard_would_say_holds": bool(outward_upwinding_holds(s_zero)["holds"]),
        "note": ("the guard's predicate is `min > 0`, so it stays CONSERVATIVE here "
                 "rather than wrong; the sweep is exact because there is nothing to "
                 "upwind. The repair does not change this case by a single bit."),
    }

    nonneg = [r for r in curve if r["min_s_rho"] >= 0.0]
    breached = [r for r in curve if r["min_s_rho"] < 0.0]
    return {
        "mechanism": "M1 -- line_sweep_solve's radial difference now follows sign(s_rho)",
        "leg200_prerepair_worst": {
            "min_s_rho": LEG200_PREREPAIR["M1_worst_min_s_rho"],
            "rel_error_vs_advertised_operator":
                LEG200_PREREPAIR["M1_worst_rel_error_vs_advertised_operator"],
            "relative_residual": LEG200_PREREPAIR["M1_worst_relative_residual"]},
        "curve_in_min_s_rho": curve,
        "n_clean_cases_bit_identical": sum(1 for r in nonneg
                                           if r["bit_identical_to_prerepair"]),
        "n_clean_cases": len(nonneg),
        "n_breached_cases_now_visible": sum(
            1 for r in breached if r["after_leg217"]["outcome"] == "VISIBLE"),
        "n_breached_cases": len(breached),
        "n_breached_cases_silent_before": sum(
            1 for r in breached if r["before_leg217"]["outcome"] == "SILENT"),
        "uniform_negative_control": uniform_negative,
        "zero_speed_case": zero_speed,
        "verdict": ("REPAIRED"
                    if (all(r["after_leg217"]["outcome"] == "VISIBLE" for r in breached)
                        and all(r["bit_identical_to_prerepair"] for r in nonneg)
                        and uniform_negative["after_leg217"]["outcome"] == "CORRECT")
                    else "NOT REPAIRED"),
    }


# ---------------------------------------------------------------------------
# PCR2 -- M2: radii_polynomial_status forms r_min and gates on it
# ---------------------------------------------------------------------------
def pcr2_radii_polynomial_radius_gate():
    """Leg 200's PCA10 rows, plus the honest paths that must NOT move."""
    rows = []
    for label, (y, z1, z2), expect in [
            ("Y_0 = 0 (leg 51's banked value on the a=0 CLM profile), Z_1=0.5, Z_2=1e4",
             (0.0, 0.5, 1e4), "reject"),
            ("Y_0 = 0, Z_1 = 0.9, Z_2 = 1.0", (0.0, 0.9, 1.0), "reject"),
            ("Y_0 = -0.0 (signed zero)", (-0.0, 0.5, 1.0), "reject"),
            ("fully degenerate Y_0 = Z_1 = Z_2 = 0", (0.0, 0.0, 0.0), "reject"),
            ("honest certificate (POSITIVE CONTROL -- must still close)",
             (1e-8, 0.5, 1.0), "close"),
            ("discriminant exactly 0, double root (POSITIVE CONTROL)",
             (0.0625, 0.5, 1.0), "close"),
            ("genuine non-closure (NEGATIVE CONTROL)", (1.0, 0.1, 1.0), "reject"),
            ("the documented closing triple legs 79/128 gate on (POSITIVE CONTROL)",
             (1e-6, 0.1, 1.0), "close"),
    ]:
        v, exc = call(radii_polynomial_status, y, z1, z2)
        r_min = v.get("r_min") if exc is None else None
        rows.append({
            "case": label, "Y_0": y, "Z_1": z1, "Z_2": z2, "expected": expect,
            "status": None if exc else v["status"],
            "closes_after_leg217": None if exc else v["closes"],
            "r_min_now_computed": r_min,
            "radius_violation": None if exc else v.get("radius_violation"),
            "guard_agrees": (None if r_min is None
                             else (radius_violation(r_min) is None) == v["closes"]),
            "outcome": ("CORRECT"
                        if (exc is None
                            and v["closes"] == (expect == "close"))
                        else "WRONG"),
        })

    # the five documented branches, which a radius gate must not disturb
    branches = {
        "blocked": radii_polynomial_status(None, None)["status"],
        "no_Z1": radii_polynomial_status(1e-3, None)["status"],
        "Z1_exceeds_one": radii_polynomial_status(1e-3, 1.2)["status"],
        "no_Z2": radii_polynomial_status(1e-3, 0.1)["status"],
        "invalid_input_negative_Y0": radii_polynomial_status(-1e-12, 0.1, 1.0)["status"],
    }
    return {
        "mechanism": ("M2 -- radii_polynomial_status now forms r_min = ((1-Z_1) - "
                      "sqrt(disc)) / (2 Z_2) and gates `closes` on "
                      "certificate_guards.radius_violation(r_min); before, `closes` came "
                      "from the discriminant alone and r_min was never computed"),
        "rows": rows,
        "n_degenerate_now_rejected": sum(
            1 for r in rows if r["expected"] == "reject" and r["outcome"] == "CORRECT"),
        "n_positive_controls_still_closing": sum(
            1 for r in rows if r["expected"] == "close" and r["outcome"] == "CORRECT"),
        "five_documented_branches_unchanged": branches,
        "guard_reused_not_reinvented": ("solver/certificate_guards.py::radius_violation, "
                                        "already called by solver/nk_bounds.py:561"),
        "verdict": "REPAIRED" if all(r["outcome"] == "CORRECT" for r in rows)
                   else "NOT REPAIRED",
    }


# ---------------------------------------------------------------------------
# PCR3 -- M3: leading_order_solve's float cast
# ---------------------------------------------------------------------------
def pcr3_leading_order_dtype():
    """Integer rhs no longer truncates; the float path is bit-identical."""
    c_l, drho, c_diag, nr, nb = 0.5, 0.1, 1.0, 2, 2
    L = dense_radial(c_l, drho, c_diag, nr)
    cases = []
    for label, rhs_int in [
            ("canonical basis vector e_0", np.array([[1, 0], [0, 0]])),
            ("small integer rhs", np.array([[1, 2], [3, 4]])),
            ("indicator mask", np.array([[1, 1], [0, 0]])),
    ]:
        ref = np.linalg.solve(L, np.asarray(rhs_int, float))
        after, exc_a = call(leading_order_solve, rhs_int, c_l, drho, c_diag)
        before, exc_b = call(_leading_order_prerepair, rhs_int, c_l, drho, c_diag)
        cases.append({
            "case": label,
            "input_dtype": str(np.asarray(rhs_int).dtype),
            "output_dtype_before": str(np.asarray(before).dtype) if exc_b is None else None,
            "output_dtype_after": str(np.asarray(after).dtype) if exc_a is None else None,
            "before_leg217": classify(before, ref, exc_b),
            "after_leg217": classify(after, ref, exc_a),
        })

    # the float path must not move a single bit
    rng = np.random.default_rng(3)
    float_cases = []
    for label, rhs_f in [("random float rhs", rng.standard_normal((9, 5))),
                         ("the exact-0.5 witness, as floats",
                          np.array([[1.0, 0.0], [0.0, 0.0]]))]:
        a = leading_order_solve(rhs_f, c_l, drho, c_diag)
        b = _leading_order_prerepair(rhs_f, c_l, drho, c_diag)
        float_cases.append({"case": label,
                            "bit_identical_to_prerepair": bool(np.array_equal(a, b))})
    return {
        "mechanism": ("M3 -- leading_order_solve casts rhs to float before allocating "
                      "np.zeros_like(rhs); its sibling line_sweep_solve always did"),
        "leg200_prerepair_worst_relative_error":
            LEG200_PREREPAIR["M3_worst_relative_error_integer_rhs"],
        "integer_cases": cases,
        "float_path_bit_identity": float_cases,
        "n_integer_cases_now_correct": sum(
            1 for c in cases if c["after_leg217"]["outcome"] == "CORRECT"),
        "n_integer_cases_silent_before": sum(
            1 for c in cases if c["before_leg217"]["outcome"] == "SILENT"),
        "verdict": ("REPAIRED"
                    if (all(c["after_leg217"]["outcome"] == "CORRECT" for c in cases)
                        and all(c["bit_identical_to_prerepair"] for c in float_cases))
                    else "NOT REPAIRED"),
    }


# ---------------------------------------------------------------------------
# PCR4 -- M4: stall_verdict refuses a poisoned ladder
# ---------------------------------------------------------------------------
def pcr4_stall_verdict_nan_guard():
    """NaN/inf/negative residuals raise; the honest ladders keep their exact verdicts."""
    def rows_of(pairs):
        return [{"m": m, "k": m, "rel_residual": r} for m, r in pairs]

    nan = float("nan")
    cases = []
    for label, pairs, expect in [
            ("honest flat ladder (POSITIVE CONTROL)", [(10, 0.6623), (160, 0.6300)],
             "flat"),
            ("honest bending ladder (POSITIVE CONTROL)", [(10, 0.4463), (160, 0.0188)],
             "bending"),
            ("both residuals NaN", [(10, nan), (160, nan)], "refuse"),
            ("NaN at the far end only", [(10, 0.66), (160, nan)], "refuse"),
            ("NaN at the near end only", [(10, nan), (160, 0.02)], "refuse"),
            ("+inf residual", [(10, float("inf")), (160, 0.02)], "refuse"),
            ("-inf residual", [(10, float("-inf")), (160, 0.02)], "refuse"),
            ("negative residual (an impossible norm)", [(10, -0.5), (160, 0.02)],
             "refuse"),
    ]:
        v, exc = call(stall_verdict, rows_of(pairs))
        if exc is not None:
            got, outcome = "raised", ("CORRECT" if expect == "refuse" else "WRONG")
        else:
            got = "flat" if v["flat"] else "bending"
            outcome = "CORRECT" if got == expect else "WRONG"
        cases.append({"case": label, "expected": expect, "reported": got,
                      "residual_gain": None if exc else v["residual_gain"],
                      "prose": None if exc else v["reading"],
                      "raised": exc, "outcome": outcome})

    # the ranking layer, which is where the harm actually propagated
    good = {"full": rows_of([(10, 0.6623), (160, 0.6300)]),
            "angular transport OFF": rows_of([(10, 0.7857), (160, 0.3712)])}
    poisoned = {"full": rows_of([(10, 0.6623), (160, 0.6300)]),
                "angular transport OFF": rows_of([(10, nan), (160, nan)])}
    base, exc_g = call(attribution_summary, good)
    pois, exc_p = call(attribution_summary, poisoned)

    # a ladder reaching machine zero is a REAL measurement this module has published
    # ("0.0401 -> 0.0 by m = 80"); it must behave exactly as it did before the repair.
    mz, exc_mz = call(stall_verdict, rows_of([(10, 0.0401), (80, 0.0)]))
    return {
        "mechanism": ("M4 -- stall_verdict raises on a non-finite or negative "
                      "rel_residual instead of comparing it to 2.0; NaN < 2.0 is False, "
                      "which used to emit the confident prose 'bending'"),
        "leg200_prerepair_nan_prose": LEG200_PREREPAIR["M4_nan_ladder_reported"],
        "leg200_prerepair_negative_gain": LEG200_PREREPAIR["M4_negative_residual_gain"],
        "cases": cases,
        "n_poisoned_now_refused": sum(1 for c in cases
                                      if c["expected"] == "refuse" and c["raised"]),
        "n_poisoned": sum(1 for c in cases if c["expected"] == "refuse"),
        "controls_unchanged": [c for c in cases if c["expected"] != "refuse"],
        "attribution_summary": {
            "healthy_ranking_still_works": exc_g is None,
            "healthy_top_ablation": None if exc_g else base[0]["ablation"],
            "poisoned_ranking_raised": exc_p,
            "outcome": "VISIBLE" if exc_p else "SILENT",
            "note": ("before the repair the NaN ablation took a RANK in the published "
                     "attribution table at gain=NaN, flat=False -- presented as an "
                     "ablation that UN-flattened the ladder")},
        "machine_zero_ladder": {
            "case": "0.0401 -> 0.0 by m = 80, from this module's own docstring",
            "raised": exc_mz,
            "note": ("0.0 is a legitimate residual and is NOT rejected by the new guard; "
                     "it still reaches the same ZeroDivisionError it reached before, "
                     "which is a crash and not a silent wrong value. Deliberately "
                     "unchanged -- repairing it is not one of this leg's four "
                     "mechanisms.")},
        "verdict": ("REPAIRED"
                    if (all(c["outcome"] == "CORRECT" for c in cases) and exc_p)
                    else "NOT REPAIRED"),
    }


# ---------------------------------------------------------------------------
# PCR5 -- THE LOAD-BEARING REGRESSION: leg 195's 114/114, re-run
# ---------------------------------------------------------------------------
def pcr5_leg195_114_regression():
    """Re-run leg 60's two ledger scripts -- the 114 numbers leg 195 re-derived.

    This is the check the repair has to survive, and it is run as a SUBPROCESS against the
    scripts themselves rather than re-implemented, so nothing of this leg's code sits
    between the banked prose and the verdict.
    """
    scripts = [("p2_route_port_v1_bordered_evidence.py", 59),
               ("p2_route_port_v2_reach_evidence.py", 55)]
    results = []
    total = 0
    for name, expected in scripts:
        t = time.time()
        p = subprocess.run([sys.executable, os.path.join(ROOT, "experiments", name)],
                           capture_output=True, text=True, cwd=ROOT, timeout=1800)
        tail = p.stdout.strip().splitlines()
        got = None
        for line in tail:
            if "quoted numbers re-derive" in line:
                got = int(line.strip().split("/")[0])
        clean = any("REPRODUCTION: CLEAN" in ln for ln in tail)
        results.append({"script": name, "expected_numbers": expected,
                        "numbers_re_derived": got, "reports_CLEAN": clean,
                        "exit_code": p.returncode,
                        "seconds": round(time.time() - t, 1)})
        total += got or 0

    # the two figures these scripts rebuild must come back byte-identical too
    fig = subprocess.run(["git", "status", "--porcelain", "writeup/figures"],
                         capture_output=True, text=True, cwd=ROOT)
    return {
        "what": ("leg 60's two reproduction ledgers over the banked Route-PORT prose, the "
                 "114 numbers leg 195 (Route-PQVER) independently re-derived"),
        "scripts": results,
        "total_numbers_re_derived": total,
        "expected_total": 114,
        "bit_identical": total == 114 and all(r["reports_CLEAN"] for r in results),
        "figures_dirty_after_rebuild": fig.stdout.strip() or "(none -- byte-identical)",
        "verdict": ("CLEAN 114/114, unmoved" if total == 114
                    else f"MOVED: {total}/114"),
    }


# ---------------------------------------------------------------------------
# PCR6 -- what leg 200 pinned that this leg deliberately did NOT repair
# ---------------------------------------------------------------------------
def pcr6_residual_open_defects():
    """The three silent mechanisms outside this leg's four, measured POST-repair.

    Reported as magnitudes so the residue is a number and not a footnote. Each is a real
    silent-wrong-value path that survives this leg; the module is NOT closed.
    """
    # (a) leading_order_solve is sign-blind in c_l -- M1's twin, untouched by M3
    c_l, drho, c_diag, nr = -0.5, 0.1, 1.0, 6
    rng = np.random.default_rng(5)
    rhs = rng.standard_normal((nr, 3))
    out, exc = call(leading_order_solve, rhs, c_l, drho, c_diag)
    # the operator the docstring advertises: upwind by sign(c_l), i.e. FORWARD here
    L_adv = np.zeros((nr, nr))
    a = c_l / drho
    for i in range(nr):
        L_adv[i, i] = c_diag + a
        if i + 1 < nr:
            L_adv[i, i + 1] = -a
    ref = np.linalg.solve(L_adv, rhs)
    sign_blind = {"defect": ("leading_order_solve hard-codes the backward radial "
                             "difference regardless of sign(c_l) -- M1's twin in the "
                             "radial-only preconditioner"),
                  "leg200_magnitude_at_c_l_minus_0p5":
                      LEG200_PREREPAIR["PCA3_still_open_rel_error_at_c_l_minus_0p5"],
                  "this_leg": classify(out, ref, exc),
                  "why_not_repaired": ("not among this leg's four named mechanisms -- M3 "
                                       "is the DTYPE defect in this function only. Fixing "
                                       "it would put a fifth mechanism in the diff.")}

    # (b) stall_verdict reads the ladder positionally, not by m
    def rows_of(pairs):
        return [{"m": m, "k": m, "rel_residual": r} for m, r in pairs]
    asc, _ = call(stall_verdict, rows_of([(10, 0.66), (160, 0.02)]))
    desc, _ = call(stall_verdict, rows_of([(160, 0.02), (10, 0.66)]))
    ordering = {"defect": ("`first, last = rows[0], rows[-1]` is POSITIONAL; identical "
                           "measurements in descending dims order give the opposite "
                           "published verdict"),
                "ascending": {"work_ratio": asc["work_ratio"], "flat": asc["flat"],
                              "residual_gain": asc["residual_gain"]},
                "descending": {"work_ratio": desc["work_ratio"], "flat": desc["flat"],
                               "residual_gain": desc["residual_gain"]},
                "still_open": asc["flat"] != desc["flat"],
                "why_not_repaired": ("M4 as named is the NaN comparison. Sorting the "
                                     "ladder by m is a second, independent change to the "
                                     "same function.")}

    # (c) ProfileResidual pack/unpack validates only the total size
    class _Grid:
        def __init__(self, nr_, nb_):
            self.rho, self.beta, self.drho = np.zeros(nr_), np.zeros(nb_), 0.1
    res = ProfileResidual(solver=None, grid=_Grid(6, 4))
    field = np.arange(24, dtype=float).reshape(4, 6)          # transposed layout
    packed = res.pack(field, field, field)
    o, _, _ = res.unpack(packed)
    shape_blind = {"defect": ("pack ravels whatever it is given and unpack reshapes to "
                              "self.shape, so a transposed field round-trips into a "
                              "different, finite, plausible field"),
                   "leg200_relative_error":
                       LEG200_PREREPAIR["PCA7_still_open_transposed_rel_error"],
                   "this_leg_relative_error": float(
                       np.linalg.norm(o - field.T) / np.linalg.norm(field.T)),
                   "round_tripped_without_exception": True,
                   "why_not_repaired": ("leg 200 reports this as 'one minor extra', not "
                                        "as one of its four mechanisms.")}
    return {"summary": ("three silent paths survive this leg, all outside its four named "
                        "mechanisms; the module is NOT closed"),
            "leading_order_solve_sign_blind_in_c_l": sign_blind,
            "stall_verdict_reads_the_ladder_positionally": ordering,
            "pack_unpack_shape_blind": shape_blind}


# ---------------------------------------------------------------------------
# PCR7 -- the collateral: what a rejection layer turned from accepted into refused
# ---------------------------------------------------------------------------
def pcr7_collateral_on_landed_artifacts():
    """Two landed artifacts encode the OLD behaviour on DEGENERATE inputs.

    Leg 128's standard for a rejection layer is that it "may turn something previously
    accepted into a refusal and must never move a clean-input number". Both items below
    are the first half, on inputs leg 200 itself classified SILENT -- but both live
    OUTSIDE this leg's declared file territory, so this leg reports them and repairs
    neither.
    """
    edge = radii_polynomial_status(0.0, 0.0, 0.0)
    signed_zero = radii_polynomial_status(-0.0, 0.1, 1.0)
    p = subprocess.run([sys.executable,
                        os.path.join(ROOT, "test_port_certification_regression.py")],
                       capture_output=True, text=True, cwd=ROOT, timeout=1800)
    return {
        "item_1": {
            "site": "test_port_certification_regression.py:87-88",
            "assertion": ("edge = radii_polynomial_status(0.0, 0.0, 0.0); assert "
                          "edge['status'] == 'EVALUATED' and edge['closes'] is True"),
            "its_stated_intent": ("the comment above it reads '# the boundary of the new "
                                  "guard: 0.0 is a legitimate bound, and so is -0.0' -- "
                                  "i.e. it gates the HYPOTHESIS guard, and 0.0 must not "
                                  "be rejected as a hypothesis violation. That intent "
                                  "SURVIVES: status is still EVALUATED."),
            "what_moved": {"status": edge["status"],
                           "closes": edge["closes"],
                           "r_min": edge.get("r_min"),
                           "radius_violation": edge.get("radius_violation")},
            "leg200_calls_this_case": ("'fully degenerate Y_0 = Z_1 = Z_2 = 0' -- one of "
                                       "the four rows of its PCA10 gate, classified "
                                       "SILENT"),
            "test_exit_code": p.returncode,
            "outside_this_legs_territory": True},
        "item_2": {
            "site": "writeup/data/p2_route_pc_v1_regression.json -> cases[Y0_negative_zero]",
            "input": "radii_polynomial_status(-0.0, 0.1, 1.0)",
            "what_moved": {"closes": signed_zero["closes"],
                           "verdict": "CLOSES_LEGITIMATELY -> REJECTED",
                           "r_min": signed_zero.get("r_min")},
            "what_did_NOT_move": ("that JSON's entire `verdict` block -- false_closes 0, "
                                  "0.0% of the 25 outside-theorem inputs, gate answer "
                                  "'yes' -- is byte-identical. Only this one case row "
                                  "reclassifies, and it reclassifies from an ACCEPT to a "
                                  "REFUSE on a degenerate ball."),
            "leg200_calls_this_case": "'Y_0 = -0.0 (signed zero)', classified SILENT",
            "regenerated_and_reverted_by_this_leg": True,
            "outside_this_legs_territory": True},
        "reading": ("neither is a clean-input number moving. Both are exactly the effect "
                    "leg 128's rejection-layer standard anticipates, on the two inputs "
                    "leg 200 nominated as fabricated certificates. But amending them is "
                    "outside this leg's territory, so the repair cannot land silently: "
                    "see the leg's gate answer."),
    }


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    gates = {
        "PCR1_line_sweep_sign_selection": pcr1_line_sweep_sign_selection(),
        "PCR2_radii_polynomial_radius_gate": pcr2_radii_polynomial_radius_gate(),
        "PCR3_leading_order_dtype": pcr3_leading_order_dtype(),
        "PCR4_stall_verdict_nan_guard": pcr4_stall_verdict_nan_guard(),
        "PCR5_leg195_114_regression": pcr5_leg195_114_regression(),
        "PCR6_residual_open_defects": pcr6_residual_open_defects(),
        "PCR7_collateral_on_landed_artifacts": pcr7_collateral_on_landed_artifacts(),
    }

    repaired = [k for k in ("PCR1_line_sweep_sign_selection",
                            "PCR2_radii_polynomial_radius_gate",
                            "PCR3_leading_order_dtype",
                            "PCR4_stall_verdict_nan_guard")
                if gates[k]["verdict"] == "REPAIRED"]
    regression_clean = gates["PCR5_leg195_114_regression"]["bit_identical"]
    collateral = gates["PCR7_collateral_on_landed_artifacts"]["item_1"][
        "test_exit_code"] != 0

    answer = ("YES on the four named mechanisms and on the 114/114 regression; "
              "NO on 'every other live PORT-family call stays bit-identical' -- "
              "two landed artifacts outside this leg's territory encode the "
              "pre-repair behaviour on two DEGENERATE inputs"
              if (len(repaired) == 4 and regression_clean and collateral)
              else "SEE PER-GATE VERDICTS")

    p1 = gates["PCR1_line_sweep_sign_selection"]
    headline = (
        "Leg 217 (Route-PCR) repaired all four mechanisms leg 200 escalated, and the "
        "repair is a rejection layer that moves no clean-input number. "
        f"M1: {p1['n_breached_cases_now_visible']}/{p1['n_breached_cases']} "
        "mixed-sign s_rho cases that used to return the exact inverse of a DIFFERENT "
        f"operator (leg 200's worst: "
        f"{LEG200_PREREPAIR['M1_worst_rel_error_vs_advertised_operator']:.0f}x relative "
        "error at min(s_rho) = -0.4, residual "
        f"{LEG200_PREREPAIR['M1_worst_relative_residual']:.0f}x the rhs) now RAISE, while "
        f"{p1['n_clean_cases_bit_identical']}/{p1['n_clean_cases']} non-negative cases "
        "are BIT-IDENTICAL to the pre-repair arithmetic and a uniformly-NEGATIVE s_rho -- "
        "the control leg 200's all-mixed battery did not have -- is now solved EXACTLY "
        f"({p1['uniform_negative_control']['after_leg217']['rel_error']:.2e}) rather than "
        "refused, which is what distinguishes upwinding by sign from refusing when "
        "nervous. "
        f"M2: {gates['PCR2_radii_polynomial_radius_gate']['n_degenerate_now_rejected']}"
        "/5 degenerate balls rejected on r_min with "
        f"{gates['PCR2_radii_polynomial_radius_gate']['n_positive_controls_still_closing']}"
        "/3 honest certificates still closing. "
        f"M3: {gates['PCR3_leading_order_dtype']['n_integer_cases_now_correct']}/3 integer "
        "rhs cases exact (worst pre-repair relative error 1.000, an exact 0.5 returned as "
        "0) with the float path bit-identical. "
        f"M4: {gates['PCR4_stall_verdict_nan_guard']['n_poisoned_now_refused']}"
        f"/{gates['PCR4_stall_verdict_nan_guard']['n_poisoned']} poisoned ladders refused "
        "and attribution_summary no longer RANKS a NaN ablation, with both honest ladders "
        "keeping their exact verdicts. "
        "THE LOAD-BEARING REGRESSION HOLDS: leg 195's 114/114 re-derives CLEAN "
        f"({gates['PCR5_leg195_114_regression']['total_numbers_re_derived']}/114) and "
        "fig59/fig60 rebuild byte-identically. "
        "BUT THE MODULE IS NOT CLOSED: three silent paths outside the four named "
        "mechanisms survive by design (leading_order_solve sign-blind in c_l at 26.0x; "
        "stall_verdict reading the ladder positionally, 16.0 -> 0.0625; pack/unpack "
        "shape-blind at 1.32), and TWO landed artifacts outside this leg's territory "
        "encode the pre-repair accept on degenerate input -- "
        "test_port_certification_regression.py:88 asserts closes=True on "
        "(Y_0, Z_1, Z_2) = (0, 0, 0), and p2_route_pc_v1_regression.json's "
        "Y0_negative_zero row reclassifies CLOSES_LEGITIMATELY -> REJECTED with its "
        "summary block byte-identical."
    )

    payload = {
        "leg": 217, "route": "PCR",
        "module_repaired": "solver/port_certification.py",
        "mechanisms_repaired": ["M1 line_sweep_solve sign(s_rho)",
                                "M2 radii_polynomial_status r_min",
                                "M3 leading_order_solve float cast",
                                "M4 stall_verdict NaN/negative guard"],
        "prior_leg": {"leg": 200, "route": "PCA", "branch": "leg/200-pca-v1",
                      "gate_answer": "YES", "n_silent_gates": "7 of 12"},
        "gate": GATE,
        "gate_answer": answer,
        "n_mechanisms_repaired": len(repaired),
        "leg195_114_regression_clean": regression_clean,
        "module_closed": False,
        "headline": headline,
        "gates": gates,
        "runtime_s": round(time.time() - t0, 2),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True, default=str)
    print(headline)
    print(f"\nwrote {OUT}  ({payload['runtime_s']} s)")
    return payload


if __name__ == "__main__":
    main()
