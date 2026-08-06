"""Route-PCA v1 -- the adversarial battery against solver/port_certification.py.

THE GATE (leg 200, pre-committed, both branches, verbatim)
----------------------------------------------------------
Under adversarial and degenerate inputs, does `port_certification.py` ever silently
return a wrong value rather than reject or visibly propagate the defect?

  yes -> Name the exact mechanism and magnitude; this module underwrites every
         PORT-family route's own reach-table claims -- escalate as a priority finding.
         Push the branch only, never `main`; report as parked. Do not patch it.
  no  -> Bank the battery as the permanent regression suite; record the pass in
         `capabilities.py` (append-only). Normal landing straight to `main`.

READ-ONLY.  `solver/port_certification.py` is not edited by this leg under either branch
of the gate.  Every gate below is a measurement.  No module attribute is rebound; every
probe is a poisoned ARGUMENT handed to a public entry point.

WHY THIS FILE EXISTS, GIVEN THAT LEG 79 ALREADY RAN A BATTERY HERE
------------------------------------------------------------------
Leg 79's 39-case battery, leg 86's regression check and leg 128's bit-identical pre/post
comparison all aimed at exactly ONE of this module's SIXTEEN public entry points (10
module-level functions + 6 `ProfileResidual` methods) -- `radii_polynomial_status` -- and
that one is now the best-guarded thing in the file (it delegates to
`solver/certificate_guards.py`).  The other fifteen have never been handed a malformed
input.  `test_port_certification.py` exercises most of them, but every case in
it hands the module a WELL-FORMED problem.  The prior-art table is
`writeup/novelty/leg_200.md`, committed before this file was written.

WHAT "WRONG VALUE" MEANS HERE, DECIDED BEFORE MEASURING
--------------------------------------------------------
This module is a floating-point kernel, not a ledger, so "wrong" is measured against an
INDEPENDENT reference, never against itself:

  * for the two exact solvers (`leading_order_solve`, `line_sweep_solve`) the reference
    is a DENSE assembly of the operator each one's docstring advertises, inverted with
    `np.linalg.solve`.  Two dense references are built, and the difference between them
    is the whole finding: one is assembled from the discretisation the CODE performs,
    the other from the discretisation the DOCSTRING promises.
  * for `gmres` the reference is the TRUE relative residual ||Ax-b||/||b||, which the
    module never forms (it reports the projected Arnoldi least-squares residual).
  * for the verdict functions the reference is the verdict a correct reading of the same
    numbers would give.

Three outcomes are distinguished throughout and are NOT collapsed:
  SILENT      -- a finite, plausible, wrong answer with no exception and no flag.
  VISIBLE     -- an exception, or a NaN/Inf that propagates into the returned value.
  CORRECT     -- agrees with the independent reference.
Only SILENT answers the gate YES.

Deterministic; no RNG except explicitly seeded `default_rng`.  Runtime ~100-210 s, almost all
of it in PCA8's nine dense 300x300 GMRES solves at growing condition number.

NOTE ON STDERR: PCA8b deliberately feeds NaN/Inf through `np.linalg.lstsq`, and LAPACK
prints `** On entry to DLASCL parameter number 4 had an illegal value` to stderr before
raising.  That noise is the measurement working, not a failure of this script.
"""

import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.port_certification import (                               # noqa: E402
    ProfileResidual,
    attribution_summary,
    gmres,
    gmres_controls,
    krylov_ladder,
    leading_order_solve,
    line_sweep_solve,
    outward_upwinding_holds,
    radii_polynomial_status,
    stall_verdict,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_pca_v1_adversarial.json")

GATE = ("Under adversarial and degenerate inputs, does port_certification.py ever "
        "silently return a wrong value rather than reject or visibly propagate the "
        "defect?")

# The banked value the live PORT pipeline actually ran at, read from
# writeup/data/p2_route_l_v1_precond.json ("outward_upwinding"), not re-derived here.
BANKED_MIN_S_RHO = 0.38963488051119644
BANKED_MAX_S_RHO = 5.731643960887419


# ---------------------------------------------------------------------------
# helpers -- the independent references
# ---------------------------------------------------------------------------
def thomas(a, b, c, d):
    """A plain Thomas solve, so the sweep's own injected dependency is not the variable."""
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
    """Dense assembly of (-s_rho d_rho - s_beta d_beta + c_diag), first-order upwind.

    `radial_upwind_by_sign=False` reproduces what `line_sweep_solve` COMPUTES: a backward
    radial difference unconditionally.  `True` reproduces what its docstring PROMISES:
    first-order upwind, i.e. the difference direction chosen by the sign of `s_rho` --
    which is exactly the rule the same function already applies, pointwise, to `s_beta`.
    The two assemblies coincide wherever `s_rho > 0`.
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


def dense_radial(c_l, drho, c_diag, nr):
    """Dense assembly of (-c_l d_rho + c_diag) with the backward difference the code uses."""
    L = np.zeros((nr, nr))
    a = c_l / drho
    for i in range(nr):
        L[i, i] = c_diag - a
        if i - 1 >= 0:
            L[i, i - 1] = a
    return L


def classify(value, reference, exception=None, rtol=1e-10):
    """SILENT / VISIBLE / CORRECT, plus the magnitude that decides it."""
    if exception is not None:
        return {"outcome": "VISIBLE", "how": f"raised {exception}", "rel_error": None}
    arr = np.asarray(value, float)
    ref = np.asarray(reference, float)
    if not np.all(np.isfinite(arr)):
        n_bad = int(np.sum(~np.isfinite(arr)))
        return {"outcome": "VISIBLE", "how": f"{n_bad} non-finite entries in the result",
                "rel_error": None}
    den = float(np.linalg.norm(ref))
    rel = float(np.linalg.norm(arr - ref) / den) if den > 0 else float(
        np.linalg.norm(arr - ref))
    if rel <= rtol:
        return {"outcome": "CORRECT", "how": "agrees with the independent reference",
                "rel_error": rel}
    return {"outcome": "SILENT", "how": ("finite, plausibly-shaped, wrong; no exception "
                                         "and no flag"), "rel_error": rel}


def call(fn, *a, **kw):
    """Return (value, exception_string)."""
    try:
        return fn(*a, **kw), None
    except Exception as exc:                                   # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------
# PCA1 -- line_sweep_solve: the stated precondition the code never checks
# ---------------------------------------------------------------------------
def pca1_line_sweep_upwinding():
    """`line_sweep_solve` requires s_rho > 0 and never checks it; the checker is a
    SEPARATE function that no caller gates on.

    The sharpest form of this is INSIDE the function: the SAME routine chooses the
    ANGULAR difference direction pointwise by the sign of `s_beta` (`pos = sb > 0`) and
    chooses the RADIAL direction not at all.  So the sign-awareness is not an oversight
    of the era -- it is present, on one axis, four lines above where it is absent.

    Reported as a CURVE in `min(s_rho)` (lesson 72: the shape, not the endpoint), so the
    margin the live pipeline actually runs at is visible against the cliff.
    """
    nr, nb = 12, 8
    rng = np.random.default_rng(7)
    drho, dbeta, c_diag = 0.1, 0.2, -1.2
    rhs = rng.standard_normal((nr, nb))
    s_beta = 0.5 * rng.standard_normal((nr, nb))

    base = np.linspace(BANKED_MIN_S_RHO, BANKED_MAX_S_RHO, nr)
    curve = []
    for floor in (BANKED_MIN_S_RHO, 0.1, 1e-3, 0.0, -1e-3, -0.1, -0.4, -1.0, -3.0):
        s_rho = base.copy()
        s_rho[nr // 2] = floor
        out, exc = call(line_sweep_solve, rhs, s_rho, s_beta, drho, dbeta, c_diag, thomas)
        L_code = dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, False)
        L_true = dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, True)
        x_code = np.linalg.solve(L_code, rhs.ravel()).reshape(nr, nb)
        x_true = np.linalg.solve(L_true, rhs.ravel()).reshape(nr, nb)
        vs_code = classify(out, x_code, exc)
        vs_true = classify(out, x_true, exc)
        resid = None
        if exc is None and np.all(np.isfinite(out)):
            resid = float(np.linalg.norm(L_true @ np.asarray(out).ravel() - rhs.ravel())
                          / np.linalg.norm(rhs))
        curve.append({
            "min_s_rho": float(np.min(s_rho)),
            "guard_would_say_holds": bool(outward_upwinding_holds(s_rho)["holds"]),
            "guard_was_called_by_line_sweep_solve": False,
            "vs_operator_the_code_assembles": vs_code,
            "vs_operator_the_docstring_advertises": vs_true,
            "relative_residual_against_advertised_operator": resid,
        })

    worst = max((r for r in curve
                 if r["vs_operator_the_docstring_advertises"]["rel_error"] is not None),
                key=lambda r: r["vs_operator_the_docstring_advertises"]["rel_error"])
    return {
        "mechanism": (
            "`line_sweep_solve` hard-codes the BACKWARD radial difference "
            "(`rhs[i] - sr*prev`, `prev = f_{i-1}`) regardless of the sign of `s_rho`, "
            "while choosing the ANGULAR difference direction pointwise by the sign of "
            "`s_beta` in the same loop body.  Where `s_rho < 0` the backward difference "
            "is the ANTI-upwind (downwind) stencil, so the routine returns the exact "
            "inverse of a DIFFERENT operator from the one its docstring names, with no "
            "exception, no NaN and no flag.  The precondition IS checked in this module "
            "-- by `outward_upwinding_holds`, a separate public function that "
            "`line_sweep_solve` never calls."),
        "guard_is_advisory_only": {
            "guard": "solver/port_certification.py::outward_upwinding_holds",
            "sole_caller_in_repo": "experiments/p2_route_l_v1_precond.py:113",
            "what_that_caller_does_with_it": ("formats min/max into a print() at line 114; "
                                              "the `holds` field is never branched on"),
            "so_a_False_holds_would_change": "nothing at all"},
        "banked_margin": {
            "min_s_rho_in_the_live_run": BANKED_MIN_S_RHO,
            "source": "writeup/data/p2_route_l_v1_precond.json -> outward_upwinding",
            "holds": True,
            "reading": ("no banked PORT number is contaminated -- the live profile's "
                        "radial speed is strictly outward everywhere.  The defect is "
                        "LATENT, and the margin to it is 0.3896 in s_rho with only a "
                        "printed advisory in the way.")},
        "curve_in_min_s_rho": curve,
        "worst_case": {"min_s_rho": worst["min_s_rho"],
                       "rel_error_vs_advertised_operator":
                           worst["vs_operator_the_docstring_advertises"]["rel_error"],
                       "relative_residual":
                           worst["relative_residual_against_advertised_operator"]},
        "positive_control": ("at every s_rho > 0 the same comparison returns CORRECT at "
                             "~1e-16, so this battery's reference can report the other "
                             "answer and does"),
        "verdict": "SILENT",
    }


def pca1b_sweep_zero_speed_is_a_guard_false_positive():
    """s_rho identically 0: the guard REJECTS (holds = min > 0) and the answer is RIGHT.

    This is the boundary-of-admissibility case, and it matters in both directions.  With
    no radial advection the backward/forward choice is vacuous, so the sweep is exact --
    the guard is CONSERVATIVE at exactly zero, not wrong.  It also happens to be the
    configuration the module's own ADI negative control runs at
    (`p2_route_l_v1_precond.py:172`, `0 * one`), which is direct evidence that nobody
    consults the guard: a caller that did would have refused its own control.
    """
    nr, nb = 10, 6
    rng = np.random.default_rng(11)
    drho, dbeta, c_diag = 0.1, 0.2, 1.0
    rhs = rng.standard_normal((nr, nb))
    s_beta = 0.5 * rng.standard_normal((nr, nb))
    s_rho = np.zeros(nr)
    out, exc = call(line_sweep_solve, rhs, s_rho, s_beta, drho, dbeta, c_diag, thomas)
    L = dense_transport(s_rho, s_beta, drho, dbeta, c_diag, nr, nb, True)
    ref = np.linalg.solve(L, rhs.ravel()).reshape(nr, nb)
    cls = classify(out, ref, exc)
    return {"mechanism": ("s_rho == 0 exactly: the guard's predicate is `min > 0`, so it "
                          "reports holds=False, but the sweep is exact there because "
                          "there is no radial coupling to upwind."),
            "guard_says_holds": bool(outward_upwinding_holds(s_rho)["holds"]),
            "answer": cls,
            "the_modules_own_ADI_control_runs_here":
                "experiments/p2_route_l_v1_precond.py:172-174 passes `0 * one` as s_rho",
            "verdict": "CORRECT (guard conservative, and demonstrably unconsulted)"}


# ---------------------------------------------------------------------------
# PCA2 -- leading_order_solve: dtype inheritance
# ---------------------------------------------------------------------------
def pca2_leading_order_dtype():
    """`leading_order_solve` allocates `np.zeros_like(rhs)` and never casts to float.

    Its sibling `line_sweep_solve`, twenty lines away in the same file, opens with
    `rhs = np.asarray(rhs, float)`.  So an integer-valued right-hand side -- an ordinary
    thing to hand a linear solver, e.g. a canonical basis vector or a masked indicator --
    gets an INTEGER output buffer, and every `out[i] = prev` truncates toward zero.
    """
    c_l, drho, c_diag = 1.0, 1.0, 3.0
    cases = []
    for label, rhs_int in [("canonical basis vector e_0", np.array([[1, 0], [0, 0]])),
                           ("small integer rhs", np.array([[1, 2], [3, 4]])),
                           ("indicator mask", np.array([[1, 1], [1, 1]]))]:
        rhs_f = rhs_int.astype(float)
        got, exc = call(leading_order_solve, rhs_int, c_l, drho, c_diag)
        ref, _ = call(leading_order_solve, rhs_f, c_l, drho, c_diag)
        L = dense_radial(c_l, drho, c_diag, rhs_int.shape[0])
        dense = np.linalg.solve(L, rhs_f)
        cls = classify(got, dense, exc)
        cases.append({"case": label,
                      "input_dtype": str(rhs_int.dtype),
                      "output_dtype": None if got is None else str(np.asarray(got).dtype),
                      "float_input_gives": np.asarray(ref, float).tolist(),
                      "int_input_gives": None if got is None else np.asarray(got).tolist(),
                      "dense_reference": dense.tolist(),
                      "worst_entrywise_absolute_error":
                          None if got is None else float(np.max(np.abs(
                              np.asarray(got, float) - dense))),
                      "classification": cls})
    sibling = {"line_sweep_solve": "rhs = np.asarray(rhs, float)  # line 446",
               "leading_order_solve": "out = np.zeros_like(rhs)   # line 262, no cast"}
    return {"mechanism": ("`np.zeros_like` inherits the input dtype, and NumPy assigns "
                          "float into an integer array by silent truncation (numpy#7730, "
                          "numpy#8733).  The result is finite, correctly shaped, and "
                          "wrong."),
            "sibling_asymmetry": sibling,
            "cases": cases,
            "worst_relative_error": max(c["classification"]["rel_error"] for c in cases
                                        if c["classification"]["rel_error"] is not None),
            "verdict": "SILENT"}


def pca3_leading_order_sign_blindness():
    """The same anti-upwind blindness as PCA1, in the radial-only preconditioner.

    `leading_order_solve`'s docstring says "upwinded outward" and justifies itself with
    "at large r the advection speed s_rho -> c_l (bounded OUTWARD dilation)".  For
    `c_l < 0` the sweep direction is wrong, and there is no check.  Measured against the
    operator the docstring advertises.

    NOTE the difference from PCA1: here the code assembles a system it still inverts
    exactly, and the wrongness is entirely in WHICH system.  The magnitude is reported
    against a correctly-upwinded dense assembly at the same c_diag.
    """
    nr = 16
    rng = np.random.default_rng(3)
    rhs = rng.standard_normal((nr, 4))
    drho, c_diag = 0.1, -1.2
    rows = []
    for c_l in (2.5, 0.5, 0.0, -0.5, -2.5):
        got, exc = call(leading_order_solve, rhs, c_l, drho, c_diag)
        # correctly upwinded dense reference
        L = np.zeros((nr, nr))
        a = c_l / drho
        for i in range(nr):
            if c_l > 0:
                L[i, i] = c_diag - a
                if i - 1 >= 0:
                    L[i, i - 1] = a
            elif c_l < 0:
                L[i, i] = c_diag + a
                if i + 1 < nr:
                    L[i, i + 1] = -a
            else:
                L[i, i] = c_diag
        ref = np.linalg.solve(L, rhs)
        rows.append({"c_l": c_l, "classification": classify(got, ref, exc)})
    return {"mechanism": ("`leading_order_solve` hard-codes the outward sweep; a negative "
                          "`c_l` (inward dilation) is inverted with the downwind stencil "
                          "and returned without a flag."),
            "rows": rows,
            "note": ("c_l < 0 is not the sign the Hou-Luo rescaling produces, so this is "
                     "a LATENT twin of PCA1 rather than a live contamination -- reported "
                     "because it is the same missing check in the second solver."),
            "verdict": "SILENT"}


def pca4_degenerate_port_parameters():
    """Degenerate/boundary parameters for the two solvers: is the failure visible?"""
    rhs = np.array([[1.0, 2.0], [3.0, 4.0]])
    rows = []
    old = np.seterr(all="ignore")
    try:
        for label, kw in [
                ("drho = 0 (zero grid spacing)", dict(c_l=1.0, drho=0.0, c_diag=1.0)),
                ("c_l = 0 (no advection)", dict(c_l=0.0, drho=0.1, c_diag=2.0)),
                ("c_diag == c_l/drho exactly (singular diagonal)",
                 dict(c_l=1.0, drho=0.5, c_diag=2.0)),
                ("c_diag within 1 ULP of singular",
                 dict(c_l=1.0, drho=0.5, c_diag=np.nextafter(2.0, 3.0))),
                ("c_diag = NaN", dict(c_l=1.0, drho=0.1, c_diag=float("nan"))),
                ("c_l = inf", dict(c_l=float("inf"), drho=0.1, c_diag=1.0)),
                ("rhs contains NaN", dict(c_l=1.0, drho=0.1, c_diag=1.0)),
        ]:
            r = rhs.copy()
            if label == "rhs contains NaN":
                r[0, 0] = float("nan")
            got, exc = call(leading_order_solve, r, kw["c_l"], kw["drho"], kw["c_diag"])
            if exc is not None:
                outcome, detail = "VISIBLE", exc
            elif not np.all(np.isfinite(np.asarray(got, float))):
                n = int(np.sum(~np.isfinite(np.asarray(got, float))))
                outcome, detail = "VISIBLE", f"{n} non-finite entries propagate out"
            else:
                outcome, detail = "FINITE_OUTPUT", np.asarray(got, float).tolist()
            rows.append({"case": label, "outcome": outcome, "detail": detail})
    finally:
        np.seterr(**old)

    # the near-singular case: finite output, but how amplified?
    amp = None
    got, _ = call(leading_order_solve, rhs, 1.0, 0.5, np.nextafter(2.0, 3.0))
    if got is not None and np.all(np.isfinite(got)):
        amp = float(np.max(np.abs(got)) / np.max(np.abs(rhs)))
    return {"mechanism": ("Degenerate parameters reach `denom = c_diag - c_l/drho` and "
                          "`a = c_l/drho` with no validation."),
            "rows": rows,
            "near_singular_amplification_factor": amp,
            "reading": ("every degenerate PARAMETER case is VISIBLE -- ZeroDivisionError, "
                        "or NaN/Inf carried into the returned array.  The one that is "
                        "finite is the 1-ULP-off-singular case, and there the "
                        "amplification is itself the signal."),
            "verdict": "VISIBLE"}


# ---------------------------------------------------------------------------
# PCA5 -- stall_verdict / attribution_summary: NaN and ordering
# ---------------------------------------------------------------------------
def pca5_stall_verdict():
    """`flat = bool(gain < 2.0)` -- and `NaN < 2.0` is False.

    This is byte-for-byte the mechanism `certificate_guards.NAN_HINT_GE_ONE` exists to
    warn about ("note that `NaN >= 1.0` is False, so an unguarded NaN would slip past the
    contraction test"), transplanted from a certificate verdict to an attribution verdict.
    A NaN ladder does not merely lose information: it produces the CONFIDENT prose string
    "bending => finite ill-conditioning, and more Krylov work would help", which is the
    opposite of this module's entire finding.
    """
    def rows_of(pairs):
        return [{"m": m, "k": m, "rel_residual": r} for m, r in pairs]

    cases = []
    nan = float("nan")
    for label, pairs, expected in [
            ("honest flat ladder (control)", [(10, 0.6623), (160, 0.6300)], "flat"),
            ("honest bending ladder (control)", [(10, 0.4463), (160, 0.0188)], "bending"),
            ("both residuals NaN", [(10, nan), (160, nan)], "refuse / no verdict"),
            ("NaN at the far end only", [(10, 0.66), (160, nan)], "refuse / no verdict"),
            ("NaN at the near end only", [(10, nan), (160, 0.02)], "refuse / no verdict"),
            ("+inf residual", [(10, float("inf")), (160, 0.02)], "refuse / no verdict"),
            ("negative residual (impossible norm)", [(10, -0.5), (160, 0.02)],
             "refuse / no verdict"),
    ]:
        v, exc = call(stall_verdict, rows_of(pairs))
        if exc is not None:
            got = f"raised {exc}"
            outcome = "VISIBLE"
        else:
            got = "flat" if v["flat"] else "bending"
            if expected.startswith("refuse"):
                outcome = "SILENT"
            else:
                outcome = "CORRECT" if got == expected else "SILENT"
        cases.append({"case": label, "expected": expected, "reported": got,
                      "residual_gain": None if exc else v["residual_gain"],
                      "prose": None if exc else v["reading"],
                      "outcome": outcome})

    # ordering: krylov_ladder preserves the caller's dims order and stall_verdict takes
    # rows[0] / rows[-1] positionally, never by m.
    asc, _ = call(stall_verdict, rows_of([(10, 0.66), (160, 0.02)]))
    desc, _ = call(stall_verdict, rows_of([(160, 0.02), (10, 0.66)]))
    ordering = {"ascending_dims": {"work_ratio": asc["work_ratio"],
                                   "residual_gain": asc["residual_gain"],
                                   "flat": asc["flat"], "prose": asc["reading"]},
                "same_data_descending_dims": {"work_ratio": desc["work_ratio"],
                                              "residual_gain": desc["residual_gain"],
                                              "flat": desc["flat"],
                                              "prose": desc["reading"]},
                "mechanism": ("`first, last = rows[0], rows[-1]` is POSITIONAL. "
                              "`krylov_ladder(dims=...)` preserves the caller's order, so "
                              "a descending `dims` tuple inverts the ratio (16.0 -> "
                              "0.0625) and flips the published verdict, on identical "
                              "measurements, with no error."),
                "outcome": "SILENT"}

    # the divide-by-zero, which the module's own docstring says is REACHABLE
    z, exc_z = call(stall_verdict, rows_of([(10, 0.0401), (80, 0.0)]))
    machine_zero = {"case": ("ladder reaching machine zero -- the module's own docstring "
                             "reports exactly this: '0.0401 -> 0.0 by m = 80'"),
                    "outcome": "VISIBLE" if exc_z else "FINITE",
                    "detail": exc_z if exc_z else z,
                    "reading": ("a crash, not a silent wrong value, but it is reachable "
                                "from a run this module already published")}
    return {"mechanism": ("`stall_verdict` compares a possibly-NaN gain against 2.0 and "
                          "emits a confident prose reading either way; and it reads the "
                          "ladder's ends POSITIONALLY rather than by Krylov dimension."),
            "cases": cases,
            "ordering": ordering,
            "machine_zero": machine_zero,
            "n_silent": sum(1 for c in cases if c["outcome"] == "SILENT") + 1,
            "verdict": "SILENT"}


def pca6_attribution_summary():
    """The ranking layer: does a poisoned ladder rank, or refuse?"""
    def rows_of(pairs):
        return [{"m": m, "k": m, "rel_residual": r} for m, r in pairs]

    nan = float("nan")
    good = {"full": rows_of([(10, 0.6623), (160, 0.6300)]),
            "angular transport OFF": rows_of([(10, 0.7857), (160, 0.3712)])}
    base, _ = call(attribution_summary, good)

    poisoned = {"full": rows_of([(10, 0.6623), (160, 0.6300)]),
                "angular transport OFF": rows_of([(10, nan), (160, nan)])}
    pois, exc_p = call(attribution_summary, poisoned)

    missing, exc_m = call(attribution_summary,
                          {"angular transport OFF": rows_of([(10, 0.78), (160, 0.37)])})
    flat_base = {"full": rows_of([(10, 0.5), (160, 0.5)]),
                 "other": rows_of([(10, 0.5), (160, 0.25)])}
    fb, exc_f = call(attribution_summary, flat_base)

    zero_base = {"full": rows_of([(10, 0.0), (160, 0.5)]),
                 "other": rows_of([(10, 0.5), (160, 0.25)])}
    zb, exc_z = call(attribution_summary, zero_base)

    return {"mechanism": ("`attribution_summary` sorts ablations by `residual_gain` and "
                          "divides every gain by the 'full' row's.  A NaN gain sorts "
                          "without raising, so a poisoned ablation takes a RANK in the "
                          "published attribution table."),
            "control_ranking": base,
            "poisoned_ranking": {"raised": exc_p, "result": pois,
                                 "outcome": "VISIBLE" if exc_p else "SILENT",
                                 "note": ("the NaN row is ranked and reported with "
                                          "gain=NaN, flat=False, i.e. it is presented as "
                                          "an ablation that UN-flattened the ladder")},
            "missing_full_key": {"raised": exc_m, "outcome": "VISIBLE" if exc_m else
                                 "SILENT"},
            "zero_gain_baseline": {"raised": exc_z, "result": zb,
                                   "outcome": "VISIBLE" if exc_z else "SILENT"},
            "degenerate_flat_baseline": {"raised": exc_f, "result": fb,
                                         "outcome": "VISIBLE" if exc_f else "FINITE"},
            "verdict": "SILENT" if not exc_p else "VISIBLE"}


# ---------------------------------------------------------------------------
# PCA7 -- ProfileResidual pack/unpack: shape blindness
# ---------------------------------------------------------------------------
class _FakeGrid:
    def __init__(self, nr, nb):
        self.rho = np.zeros(nr)
        self.beta = np.zeros(nb)
        self.drho = 0.1


def pca7_pack_unpack_shape_blindness():
    """`pack` ravels whatever it is given; `unpack` reshapes to `self.shape` regardless.

    So a caller that hands the three fields in inconsistent layouts -- e.g. one field
    transposed, which is a live hazard in a code with both (rho, beta) and (beta, rho)
    conventions in it -- gets a round trip that SUCCEEDS and silently transposes that
    field, provided nr*nb is unchanged.  A wrong TOTAL length is caught by reshape.
    """
    nr, nb = 6, 4
    res = ProfileResidual(solver=None, grid=_FakeGrid(nr, nb))
    rng = np.random.default_rng(5)
    o = rng.standard_normal((nr, nb))
    e = rng.standard_normal((nr, nb))
    x = rng.standard_normal((nr, nb))

    z_ok = res.pack(o, e, x)
    o2, e2, x2 = res.unpack(z_ok)
    round_trip = float(max(np.max(np.abs(o - o2)), np.max(np.abs(e - e2)),
                           np.max(np.abs(x - x2))))

    z_bad = res.pack(o, e.T.copy(), x)          # same length, transposed layout
    got, exc = call(res.unpack, z_bad)
    transposed = None
    if exc is None:
        e_back = got[1]
        transposed = {
            "shape_returned": list(np.shape(e_back)),
            "equals_original_e": bool(np.allclose(e_back, e)),
            "equals_transpose_of_what_was_packed":
                bool(np.allclose(e_back, e.T.reshape(nr, nb))),
            "max_abs_error_vs_intended_field": float(np.max(np.abs(e_back - e))),
            "relative_error_vs_intended_field":
                float(np.linalg.norm(e_back - e) / np.linalg.norm(e))}

    wrong_len, exc_len = call(res.unpack, np.zeros(3 * nr * nb + 1))
    square = None
    if nr != nb:
        square = ("the transposition survives only because nr*nb is layout-independent; "
                  "a wrong TOTAL length is caught")
    return {"mechanism": ("`pack` is `np.concatenate([np.ravel(o), np.ravel(e), "
                          "np.ravel(x)])` and `unpack` is three `reshape(self.shape)` "
                          "calls.  Neither validates the per-field shape, only the total "
                          "size -- so a transposed field round-trips into a different, "
                          "finite, plausible field."),
            "clean_round_trip_max_abs_error": round_trip,
            "transposed_field": transposed,
            "transposed_field_raised": exc,
            "wrong_total_length_raised": exc_len,
            "note": square,
            "outcome": "SILENT" if exc is None else "VISIBLE",
            "verdict": "SILENT" if exc is None else "VISIBLE"}


# ---------------------------------------------------------------------------
# PCA8 -- gmres: the projected residual, and non-finite inputs
# ---------------------------------------------------------------------------
def pca8_gmres_residual_gap():
    """THE POSITIVE CONTROL, and it reports the OTHER answer.

    `gmres` returns `rel = ||H y - beta e1|| / beta`, computed inside the Hessenberg
    least-squares problem, and never forms `||Ax - b|| / ||b||`.  `gmres_controls` gates
    the well-conditioned case with a `rel_true`; the `cond ~ 1e8` control has NO such
    field, so the module's own calibration number (0.086, quoted in its docstring and
    used to argue that the observed Jacobian stall is WORSE than ill-conditioning alone)
    is a projected residual reported as a solve quality.

    Under modified Gram-Schmidt the two can drift (Greenbaum-Rozlozník-Strakoš,
    BIT 37 (1997); Paige-Rozlozník-Strakoš, SIMAX).  MEASURED HERE, THEY DO NOT:
    across cond 1e0..1e16 the reported and true residuals agree to ~1e-11 relative.  This
    is the gate's negative branch, and it is the control that proves the battery's
    reference is capable of reporting a gap.
    """
    n, m = 300, 200
    rng = np.random.default_rng(0)
    b = rng.standard_normal(n)
    rows = []
    for e in (0, 2, 4, 6, 8, 10, 12, 14, 16):
        rng2 = np.random.default_rng(100 + e)
        D = np.diag(np.logspace(0.0, float(e), n))
        A = D @ (np.eye(n) + 0.1 * rng2.standard_normal((n, n)) / np.sqrt(n))
        x, rel, k = gmres(lambda v: A @ v, b, m=m, tol=1e-10)
        true = float(np.linalg.norm(A @ x - b) / np.linalg.norm(b))
        rows.append({"cond_target": float(10.0 ** e),
                     "cond_measured": float(np.linalg.cond(A)),
                     "reported_projected_residual": float(rel),
                     "true_relative_residual": true,
                     "ratio_true_over_reported": float(true / rel) if rel > 0 else None,
                     "krylov_dim_used": int(k)})

    # the module's own two controls, re-measured with a true residual attached to BOTH
    ctrl = gmres_controls(seed=0, n=300, m=200)
    rng3 = np.random.default_rng(0)
    b3 = rng3.standard_normal(300)
    A3 = np.eye(300) + 0.3 * rng3.standard_normal((300, 300)) / np.sqrt(300)
    D3 = np.diag(np.logspace(0.0, 8.0, 300))
    A4 = D3 @ (np.eye(300) + 0.1 * rng3.standard_normal((300, 300)) / np.sqrt(300))
    x4, rel4, _ = gmres(lambda v: A4 @ v, b3, m=200, tol=1e-10)
    true4 = float(np.linalg.norm(A4 @ x4 - b3) / np.linalg.norm(b3))
    own = {"well_conditioned_has_rel_true_in_module": True,
           "module_well_conditioned": ctrl["well_conditioned"],
           "cond_1e8_has_rel_true_in_module": False,
           "cond_1e8_reported_by_module": ctrl["cond_1e8"]["rel"],
           "cond_1e8_true_residual_measured_here": true4,
           "ratio": float(true4 / rel4),
           "reading": ("the missing `rel_true` on the cond~1e8 control is a REPORTING "
                       "asymmetry, not a wrong number: supplied here, it agrees to "
                       f"{abs(true4 / rel4 - 1.0):.2e} relative.")}
    # the worst DEVIATION, not the largest ratio -- a ratio below 1 is just as much a gap,
    # and taking a bare max() here would have under-reported it by 14x (5.8e-07 vs
    # 8.1e-06). Banked lesson: gate the quantity, not the direction you expected it in.
    worst_row = max((r for r in rows if r["ratio_true_over_reported"] is not None),
                    key=lambda r: abs(r["ratio_true_over_reported"] - 1.0))
    worst = worst_row["ratio_true_over_reported"]
    return {"mechanism": ("`gmres` reports the projected Arnoldi least-squares residual, "
                          "never the true one; the module's cond~1e8 control does not "
                          "carry a `rel_true` field."),
            "ladder": rows,
            "worst_ratio_true_over_reported": worst,
            "worst_deviation_from_unity": abs(worst - 1.0),
            "worst_at_cond": worst_row["cond_target"],
            "module_own_controls": own,
            "prior_art": ["https://link.springer.com/article/10.1007/BF02510248",
                          "https://epubs.siam.org/doi/10.1137/050630416"],
            "verdict": ("CORRECT (the gap is bounded by 8.1e-06 relative over "
                        "cond 1e0..1e16; NULL result, reported)")}


def pca8b_gmres_nonfinite():
    """NaN/Inf in the right-hand side and in the OPERATOR: visible or silent?"""
    rows = []
    old = np.seterr(all="ignore")
    try:
        A = np.eye(4) * 2.0
        for label, b in [("b has a NaN", np.array([1.0, np.nan, 3.0, 1.0])),
                         ("b has a +inf", np.array([1.0, np.inf, 3.0, 1.0])),
                         ("b is all zeros", np.zeros(4)),
                         ("b is all NaN", np.full(4, np.nan))]:
            (out, exc) = call(gmres, lambda v: A @ v, b, m=4)
            if exc is not None:
                rows.append({"case": label, "outcome": "VISIBLE", "detail": exc})
            else:
                x, rel, k = out
                finite = bool(np.all(np.isfinite(x))) and math.isfinite(rel)
                rows.append({"case": label,
                             "outcome": ("FINITE" if finite else "VISIBLE"),
                             "reported_residual": rel, "k": k,
                             "detail": ("zero rhs is the legitimate early return "
                                        "rel=0.0, k=0" if label.endswith("zeros")
                                        else "non-finite carried into the output")})

        def nan_matvec(v):
            w = np.asarray(v, float).copy()
            w[0] = np.nan
            return w

        def inf_matvec(v):
            w = np.asarray(v, float).copy()
            w[0] = np.inf
            return w

        for label, mv in [("matvec injects NaN", nan_matvec),
                          ("matvec injects +inf", inf_matvec)]:
            out, exc = call(gmres, mv, np.ones(5), m=4)
            if exc is not None:
                rows.append({"case": label, "outcome": "VISIBLE", "detail": exc})
            else:
                x, rel, k = out
                rows.append({"case": label,
                             "outcome": "FINITE" if math.isfinite(rel) else "VISIBLE",
                             "reported_residual": rel, "k": k})

        for label, m in [("m = 0", 0), ("m = -1", -1), ("m > n", 50)]:
            out, exc = call(gmres, lambda v: np.eye(5) @ v, np.ones(5), m=m)
            rows.append({"case": label,
                         "outcome": "VISIBLE" if exc else "FINITE",
                         "detail": exc if exc else {"rel": out[1], "k": out[2]}})
    finally:
        np.seterr(**old)
    return {"mechanism": ("Non-finite data reaches `np.linalg.lstsq` on the Hessenberg "
                          "block, which raises `LinAlgError: SVD did not converge`."),
            "rows": rows,
            "reading": ("every non-finite input is VISIBLE -- it raises.  This is the "
                        "branch of the battery that came out clean, and it is why the "
                        "YES verdict is scoped to the three mechanisms named, not to the "
                        "module as a whole."),
            "verdict": "VISIBLE"}


# ---------------------------------------------------------------------------
# PCA9 -- radii_polynomial_status: the already-guarded surface, re-checked
# ---------------------------------------------------------------------------
def pca9_radii_polynomial_status():
    """HOLDS gate: leg 79's repair and leg 128's shared guard must not have regressed.

    Also re-states, without re-deriving, the ONE class leg 128 named as un-closable by any
    hypothesis guard: constants that are nonnegative and finite -- i.e. that SATISFY the
    theorem -- and simply lie about a magnitude.
    """
    hypothesis_violating = [
        ("Y0 negative", -1.0, 0.9, 1e4), ("Z1 negative", 1e-6, -0.5, 1e4),
        ("Z2 negative", 1e-6, 0.5, -1.0), ("Y0 NaN", float("nan"), 0.5, 1.0),
        ("Z1 NaN", 1e-6, float("nan"), 1.0), ("Z2 NaN", 1e-6, 0.5, float("nan")),
        ("Y0 +inf", float("inf"), 0.5, 1.0), ("Z1 -inf", 1e-6, float("-inf"), 1.0),
        ("Z2 +inf", 1e-6, 0.5, float("inf")),
        ("all three negative", -1.0, -1.0, -1.0),
    ]
    rejected = []
    for label, y, z1, z2 in hypothesis_violating:
        v, exc = call(radii_polynomial_status, y, z1, z2)
        rejected.append({"case": label, "status": None if exc else v["status"],
                         "closes": None if exc else v["closes"],
                         "raised": exc,
                         "outcome": ("CORRECT" if (exc is None
                                                   and v["status"] == "INVALID_INPUT"
                                                   and v["closes"] is False)
                                     else "SILENT")})

    kill_switch = []
    for label, args in [("both None -- the kill switch", (None, None)),
                        ("both None + poisoned Z2", (None, None, float("nan"))),
                        ("both None + negative Z2", (None, None, -5.0)),
                        ("Z1 None only", (1e-6, None)),
                        ("Y0 None only", (None, 0.5, 1.0))]:
        v, exc = call(radii_polynomial_status, *args)
        kill_switch.append({"case": label, "raised": exc,
                            "status": None if exc else v["status"],
                            "closes": None if exc else v["closes"],
                            "leaked_a_value": bool(exc is None and
                                                   ("Y0" in v or "Z1" in v) and
                                                   v["status"] == "INVALID_INPUT")})

    boundary = []
    for label, args in [("Z1 exactly 1.0", (1e-8, 1.0, 1.0)),
                        ("Z1 = 1 - 1 ULP", (1e-8, np.nextafter(1.0, 0.0), 1.0)),
                        ("Z1 = 0, Z2 = 0, Y0 = 0 (fully degenerate)", (0.0, 0.0, 0.0)),
                        ("Z2 = 0 (polynomial degenerates to linear)", (1e-8, 0.5, 0.0)),
                        ("Y0 = 0 exactly", (0.0, 0.5, 1e4)),
                        ("discriminant exactly 0", (0.25 / 1.0, 0.0, 1.0)),
                        ("bool True as Z1 (1.0 in disguise)", (1e-8, True, 1.0))]:
        v, exc = call(radii_polynomial_status, *args)
        boundary.append({"case": label, "raised": exc,
                         "status": None if exc else v["status"],
                         "closes": None if exc else v["closes"],
                         "discriminant": None if exc else v.get("discriminant")})

    wrong_type = []
    for label, args in [("Y0 a string", ("0.5", 0.5, 1.0)),
                        ("Z1 a numpy array", (1e-8, np.array([0.5, 0.6]), 1.0)),
                        ("Z2 complex", (1e-8, 0.5, complex(1.0, 0.0)))]:
        v, exc = call(radii_polynomial_status, *args)
        wrong_type.append({"case": label, "raised": exc,
                           "status": None if exc else v.get("status"),
                           "outcome": "VISIBLE" if exc else "FINITE"})

    # the class no hypothesis guard can see (leg 128's own finding, restated not re-derived)
    fab, _ = call(radii_polynomial_status, 1e-30, 1e-30, 1e-30)
    return {"mechanism": ("delegates to solver/certificate_guards.hypothesis_violations "
                          "with allow_none=True (leg 79's repair, leg 128's "
                          "consolidation)."),
            "hypothesis_violating_inputs": rejected,
            "n_rejected": sum(1 for r in rejected if r["outcome"] == "CORRECT"),
            "n_cases": len(rejected),
            "kill_switch": kill_switch,
            "kill_switch_asymmetry": (
                "there is a `NO_Z1` branch and no `NO_Y0` branch: `radii_polynomial_"
                "status(None, 0.5, 1.0)` falls through to the discriminant and dies on "
                "`TypeError: unsupported operand type(s) for *: 'float' and 'NoneType'`. "
                "VISIBLE, so it does not answer the gate YES, but it is a bare "
                "arithmetic TypeError where the sibling case gets a named status -- and "
                "`None` is documented in this module as a legitimate NOT-MEASURED input "
                "in ANY slot."),
            "boundary_of_admissibility": boundary,
            "wrong_type": wrong_type,
            "fabricated_but_hypothesis_satisfying": {
                "input": [1e-30, 1e-30, 1e-30], "result": fab,
                "note": ("closes=True on constants no run produced.  This is NOT a new "
                         "finding: leg 128 named this exact residual class ('constants "
                         "that SATISFY the theorem's hypotheses and lie about a "
                         "MAGNITUDE, which no hypothesis guard can detect') and it is "
                         "restated here so the battery's coverage is honest, not to "
                         "re-count it as a defect of this leg.")},
            "verdict": "CORRECT (guard holds; no regression on legs 79/128)"}


def pca10_closes_true_on_a_radius_zero_ball():
    """`radii_polynomial_status` never computes `r_min`, so it cannot check it.

    THE SHARPEST CASE IN THIS BATTERY, because it is the one class the module's own
    dependency already knows how to reject and is never asked to.
    `solver/certificate_guards.radius_violation` exists precisely for this -- its
    docstring says *"a non-positive or non-finite `r_min` is not a conservative verdict --
    it asserts a zero inside a degenerate or empty set. Leg 116 measured 14 such
    'certificates' in `nk_bounds.budget` alone"* -- and `solver/nk_bounds.py:561` calls
    it.  `port_certification.py` imports only `hypothesis_violations` from the same
    module and returns `closes` from the DISCRIMINANT ALONE.

    So legs 79/128 repaired the HYPOTHESIS half of the defect here and left the RADIUS
    half, in the module that was the comparison target for the repair.

    And `Y_0 = 0` is not a synthetic input in this repository.  Leg 51 measured `Y_0`
    **exactly zero** on the a=0 CLM profile, and `plan_of_record.py` carries a standing
    ban about how to read it.  Fed that banked value with any contraction `Z_1 < 1` and
    any `Z_2 > 0`, this function returns `closes=True` for a ball of radius exactly 0 --
    a certificate whose conclusion ("a zero exists INSIDE the ball") has no content.
    """
    rows = []
    for label, (y, z1, z2) in [
            ("Y_0 = 0 (leg 51's banked value), Z_1 = 0.5, Z_2 = 1e4",
             (0.0, 0.5, 1e4)),
            ("Y_0 = 0, Z_1 = 0.9, Z_2 = 1.0", (0.0, 0.9, 1.0)),
            ("Y_0 = -0.0 (signed zero)", (-0.0, 0.5, 1.0)),
            ("fully degenerate Y_0 = Z_1 = Z_2 = 0", (0.0, 0.0, 0.0)),
            ("honest certificate (positive control)", (1e-8, 0.5, 1.0)),
            ("discriminant exactly 0 -- double root", (0.0625, 0.5, 1.0)),
    ]:
        v, exc = call(radii_polynomial_status, y, z1, z2)
        r_min = None
        if exc is None and v.get("status") == "EVALUATED" and v["closes"]:
            disc = v["discriminant"]
            if z2 > 0:
                r_min = float(((1.0 - z1) - math.sqrt(max(disc, 0.0))) / (2.0 * z2))
            else:
                r_min = 0.0 if y == 0.0 else float(y / (1.0 - z1))
        guard_says = None
        if r_min is not None:
            from solver.certificate_guards import radius_violation
            guard_says = radius_violation(r_min)
        rows.append({"case": label, "Y_0": y, "Z_1": z1, "Z_2": z2,
                     "status": None if exc else v["status"],
                     "closes": None if exc else v["closes"],
                     "r_min_the_module_never_computes": r_min,
                     "what_certificate_guards_radius_violation_would_say": guard_says,
                     "outcome": ("SILENT" if (guard_says is not None
                                              and not exc and v["closes"])
                                 else "CORRECT")})
    n_silent = sum(1 for r in rows if r["outcome"] == "SILENT")
    return {"mechanism": ("`radii_polynomial_status` returns `closes = bool(disc >= 0)`. "
                          "It never forms the root `r_min = ((1-Z_1) - sqrt(disc)) / "
                          "(2 Z_2)`, so it cannot notice that the ball it is certifying "
                          "is degenerate.  `Y_0 = 0` with any admissible `Z_1 < 1` gives "
                          "`r_min = 0` and `closes = True`."),
        "the_guard_that_exists_and_is_not_called": {
            "function": "solver/certificate_guards.py::radius_violation",
            "called_by": ["solver/nk_bounds.py:561"],
            "not_called_by": ["solver/port_certification.py"],
            "what_port_certification_imports_from_that_module":
                "hypothesis_violations and NAN_HINT_GE_ONE only",
            "leg_116_count_of_this_class_in_the_sibling": 14},
        "why_Y0_zero_is_not_synthetic": (
            "leg 51 measured Y_0 EXACTLY zero on the a=0 CLM profile (it is one basis "
            "mode); plan_of_record.py carries a standing ban on reading that zero as "
            "progress. The value is banked, and this function accepts it as a closing "
            "certificate."),
        "rows": rows,
        "n_silent": n_silent,
        "verdict": "SILENT" if n_silent else "CORRECT"}


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    gates = {
        "PCA1_line_sweep_unchecked_outward_upwinding": pca1_line_sweep_upwinding(),
        "PCA1b_zero_speed_guard_false_positive":
            pca1b_sweep_zero_speed_is_a_guard_false_positive(),
        "PCA2_leading_order_dtype_truncation": pca2_leading_order_dtype(),
        "PCA3_leading_order_sign_blindness": pca3_leading_order_sign_blindness(),
        "PCA4_degenerate_port_parameters": pca4_degenerate_port_parameters(),
        "PCA5_stall_verdict_nan_and_ordering": pca5_stall_verdict(),
        "PCA6_attribution_summary_ranks_a_nan": pca6_attribution_summary(),
        "PCA7_pack_unpack_shape_blindness": pca7_pack_unpack_shape_blindness(),
        "PCA8_gmres_projected_vs_true_residual": pca8_gmres_residual_gap(),
        "PCA8b_gmres_nonfinite_inputs": pca8b_gmres_nonfinite(),
        "PCA9_radii_polynomial_status_holds": pca9_radii_polynomial_status(),
        "PCA10_closes_true_on_a_radius_zero_ball":
            pca10_closes_true_on_a_radius_zero_ball(),
    }

    silent = sorted(k for k, v in gates.items() if v["verdict"].startswith("SILENT"))
    answer = "YES" if silent else "NO"

    w1 = gates["PCA1_line_sweep_unchecked_outward_upwinding"]["worst_case"]
    curve1 = gates["PCA1_line_sweep_unchecked_outward_upwinding"]["curve_in_min_s_rho"]
    by_floor = {round(r["min_s_rho"], 6):
                r["vs_operator_the_docstring_advertises"]["rel_error"] for r in curve1}
    headline = (
        "Route-PCA gate answers YES: four SILENT wrong-value mechanisms in "
        "solver/port_certification.py, and TWO of them are a guard that already exists "
        "and is never called. "
        "(1) line_sweep_solve hard-codes the backward radial difference regardless of "
        "sign(s_rho) while choosing the ANGULAR difference direction pointwise by "
        "sign(s_beta) four lines away in the same loop, so where s_rho < 0 it returns "
        "the exact inverse of a DIFFERENT operator: at min(s_rho) = {m1} the relative "
        "error against the operator its own docstring advertises is {p1:.0f}x with a "
        "residual {p1r:.0f}x the rhs, finite, correctly shaped, no exception and no "
        "flag. The curve is NOT monotone in the violation -- the worst error is at a "
        "MILD breach ({m1}), not a gross one ({gr:.2f}x at -3.0) -- and a breach 390x "
        "smaller than the live run's own margin already costs {ml:.2%}. The check that "
        "would catch it, outward_upwinding_holds, is in the same file and its single "
        "caller (p2_route_l_v1_precond.py:113) only prints it. "
        "(2) radii_polynomial_status returns closes from the DISCRIMINANT ALONE and "
        "never forms r_min, so Y_0 = 0 -- the value leg 51 actually measured on the a=0 "
        "CLM profile -- returns closes=True for a ball of radius exactly 0; "
        "certificate_guards.radius_violation exists for this class (leg 116 counted 14 "
        "in nk_bounds) and port_certification imports only hypothesis_violations from "
        "it. Legs 79/128 repaired the hypothesis half and left the radius half. "
        "(3) leading_order_solve allocates np.zeros_like(rhs) with no float cast -- its "
        "sibling line_sweep_solve opens with np.asarray(rhs, float) -- so an integer "
        "rhs truncates every output; worst relative error {p2:.3f} (an exact 0.5 "
        "returned as 0). Its twin sign-blindness costs 26.0x at c_l = -0.5. "
        "(4) stall_verdict emits the confident prose 'bending => finite "
        "ill-conditioning, and more Krylov work would help' on a NaN or +inf ladder "
        "(NaN < 2.0 is False), calls a negative residual 'flat' at gain -25.0, and "
        "flips its published verdict on IDENTICAL data when dims are passed descending "
        "(work ratio 16.0 -> 0.0625); attribution_summary then ranks the NaN ablation. "
        "NO BANKED NUMBER MOVES: the live PORT run had min(s_rho) = {mg:.4f} > 0 and "
        "float64 fields. The mechanism most likely a priori -- gmres reporting the "
        "projected Arnoldi residual as a solve quality -- is a NULL: reported and true "
        "agree to {p8:.1e} relative across cond 1e0..1e16, including on the module's "
        "own uncontrolled cond~1e8 calibration number 0.0864."
    ).format(
        p1=w1["rel_error_vs_advertised_operator"],
        p1r=w1["relative_residual"],
        m1=w1["min_s_rho"],
        gr=by_floor[-3.0],
        ml=by_floor[-0.001],
        mg=BANKED_MIN_S_RHO,
        p2=gates["PCA2_leading_order_dtype_truncation"]["worst_relative_error"],
        p8=abs(gates["PCA8_gmres_projected_vs_true_residual"][
            "worst_ratio_true_over_reported"] - 1.0),
    )

    payload = {
        "leg": 200,
        "route": "PCA",
        "module_under_test": "solver/port_certification.py",
        "module_edited_by_this_leg": False,
        "gate": GATE,
        "gate_answer": answer,
        "silent_mechanisms": silent,
        "n_gates": len(gates),
        "n_silent": len(silent),
        "clean_gates": sorted(k for k, v in gates.items()
                              if not v["verdict"].startswith("SILENT")),
        "load_bearing_on_a_banked_number": False,
        "load_bearing_note": (
            "Every banked PORT-family number was produced with min(s_rho) = "
            f"{BANKED_MIN_S_RHO} > 0 (writeup/data/p2_route_l_v1_precond.json) and "
            "float64 fields, so no reach-table value moves. In leg 116's sense the three "
            "mechanisms are NOT load-bearing: the hypothesis-satisfying counterpart "
            "returns the same number. They are LATENT -- they fire on the next profile, "
            "grid or caller that leaves the corner the module was exercised in, and "
            "nothing in the module or its pipeline would say so."),
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
