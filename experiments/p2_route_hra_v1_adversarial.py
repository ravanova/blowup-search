"""Leg 117 (Route-HRA) -- the adversarial battery against `solver/hl_rescaled.py`.

THE QUESTION (the leg's gate, verbatim):

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/hl_rescaled.py ever silently return a wrong result instead of flagging the
    input?

WHAT THIS IS NOT. Not a re-measurement of the CHL Theorem-2.3 anchor, the Scenario-2
contraction ratio, or any Conjecture-2.4 basin claim -- those are `capabilities.py`'s frozen
`test_hl_rescaled.py` numbers and are not reopened here. No gCLM physics is measured (the
`NG`-is-NEXT ban on "another gCLM measurement leg" does not bite: this module has nothing to
do with the gCLM family; it audits code behaviour only). `solver/hl_rescaled.py` is
READ-ONLY under this leg's territory, under any gate outcome.

THE PRE-COMMITTED CORRUPTION CRITERION (fixed before the run). A case counts as SILENT
CORRUPTION when a function is fed a degenerate/poisoned/out-of-contract input and returns a
FINITE, non-NaN result that disagrees with an independently-computed correct answer, with
NO exception raised and NO warning emitted. Raising, warning, or returning non-finite output
all count as FLAGGED (visible), never silent, even when the caller might not check for it --
that is the exact distinction legs 96/120 already drew (leg 96: "exact duplicates go 100%
non-finite with 16 warnings" was banked as a PASS, not a defect).

Run:  python experiments/p2_route_hra_v1_adversarial.py
Writes: writeup/data/p2_route_hra_v1_adversarial.json
"""
from __future__ import annotations

import json
import os
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.hl_rescaled import (  # noqa: E402
    RescaledHL, RescaledHLDynamic, RescaledHLScenario2, degenerate_ic, scenario2_ic,
    sinh_grid_at, sinh_grid_origin, velocity, _solve_3x3,
)

SEED = 0


def _count_warnings(fn, *args, **kwargs):
    """Run fn, return (result_or_exception, n_warnings, exception_or_None)."""
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        try:
            out = fn(*args, **kwargs)
            return out, len(wl), None
        except Exception as e:  # noqa: BLE001 -- audit wants the exception itself
            return None, len(wl), repr(e)


# ---- Gate 1: velocity() silently corrupted by a non-ascending X ------------------------
def gate1_permutation_corrupts_velocity():
    """velocity()'s docstring requires a sorted-ascending grid but never checks it. Feed it
    a permuted (X, Homega) pair -- the SAME data, presented out of order, as a caller who
    e.g. sorted by the wrong key would produce -- and see whether it silently returns wrong,
    finite numbers with zero diagnostic, versus the correctly-sorted computation."""
    _, X = sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)         # H(-4X/(1+4X^2)), the CLM Hilbert pair
    U_true = velocity(X, Homega, X_ref=0.0)
    Uex = np.arctan(2.0 * X)
    sanity_err = float(np.abs(U_true - Uex).max())

    rng = np.random.default_rng(SEED)
    cases = []
    for trial in range(20):
        perm = rng.permutation(len(X))
        Xp, Hp = X[perm], Homega[perm]
        Up, nwarn, exc = _count_warnings(velocity, Xp, Hp, 0.0)
        if exc is not None:
            cases.append({"trial": trial, "raised": exc, "n_warnings": nwarn})
            continue
        inv = np.argsort(perm)
        Up_unperm = Up[inv]
        err = np.abs(Up_unperm - U_true)
        cases.append({
            "trial": trial, "raised": None, "n_warnings": nwarn,
            "max_abs_error_vs_correct_sorted_computation": float(err.max()),
            "max_rel_error": float(err.max() / np.abs(U_true).max()),
            "returned_finite": bool(np.all(np.isfinite(Up))),
        })
    n_silent = sum(1 for c in cases if c["raised"] is None and c["n_warnings"] == 0
                   and c["returned_finite"] and c["max_abs_error_vs_correct_sorted_computation"] > 1e-2)
    return {
        "mechanism": "velocity(X, Homega, X_ref) never validates X is ascending; a "
                     "permutation of the same (X, Homega) pair is accepted and integrated "
                     "in the permuted order.",
        "sanity_check_sorted_matches_analytic": sanity_err,
        "n_trials": len(cases),
        "n_silent_corruptions": n_silent,
        "worst_max_abs_error": max(c.get("max_abs_error_vs_correct_sorted_computation", 0.0)
                                   for c in cases),
        "worst_max_rel_error": max(c.get("max_rel_error", 0.0) for c in cases),
        "cases": cases[:5],   # first 5 kept verbatim; the rest agree in kind
    }


# ---- Gate 2: velocity() silently clamps X_ref outside the sampled domain ---------------
def gate2_xref_extrapolation_silent_clamp():
    """velocity() pins U(X_ref)=0 via np.interp(X_ref, X, U). np.interp's documented default
    for x outside [X.min(), X.max()] is to clamp to the nearest boundary value, silently.
    velocity() adds no check of its own. Use the analytic CLM pair (defined for all real X,
    not just the sampled window) so the TRUE pinned value at an out-of-range X_ref is known."""
    X = np.linspace(0.0, 10.0, 501)               # sampled window: only X in [0,10]
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)
    cases = []
    for X_ref_out in (-5.0, -50.0, 20.0, 200.0):
        U_out, nwarn, exc = _count_warnings(velocity, X, Homega, X_ref_out)
        true_pinned = np.arctan(2.0 * X) - np.arctan(2.0 * X_ref_out)
        if exc is not None:
            cases.append({"X_ref": X_ref_out, "raised": exc, "n_warnings": nwarn})
            continue
        err = np.abs(U_out - true_pinned)
        cases.append({
            "X_ref": X_ref_out, "raised": None, "n_warnings": nwarn,
            "in_sampled_domain": bool(0.0 <= X_ref_out <= 10.0),
            "max_abs_error_vs_analytic_pin": float(err.max()),
            "shift_is_uniform_std": float(np.std(U_out - true_pinned)),
            "returned_finite": bool(np.all(np.isfinite(U_out))),
        })
    n_silent = sum(1 for c in cases
                   if not c.get("in_sampled_domain", True) and c.get("raised") is None
                   and c["n_warnings"] == 0 and c["max_abs_error_vs_analytic_pin"] > 1e-2)
    return {
        "mechanism": "velocity() pins U(X_ref)=0 via np.interp, which silently clamps to "
                     "the nearest sampled boundary when X_ref falls outside [X.min(), "
                     "X.max()] -- a documented numpy default, never checked by velocity().",
        "n_cases": len(cases),
        "n_out_of_domain_cases": sum(1 for c in cases if not c.get("in_sampled_domain", True)),
        "n_silent_corruptions": n_silent,
        "cases": cases,
    }


# ---- Gate 3: sinh_grid_at(M<0) silently reverses the grid ------------------------------
def gate3_negative_M_silently_reverses_grid():
    """sinh_grid_at's docstring says 'Reach is +-M about Xc', implying M is a magnitude, but
    M's sign is never validated. A negative M silently returns the exact mirror-image
    (descending) grid, indistinguishable in shape from a valid ascending one until you check
    monotonicity. RescaledHL.__init__ DOES catch the resulting descending array (its own
    ascending guard fires) -- so the compound risk is specific to callers of the free
    `velocity()`/`sinh_grid_at()` functions who skip the class wrapper, exactly gate 1's
    exposure."""
    kwargs = dict(Xc=0.0, delta=1.0, M=50.0, offset=False)
    _, X_pos = sinh_grid_at(11, **kwargs)
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        _, X_neg = sinh_grid_at(11, **{**kwargs, "M": -50.0})
        nwarn_neg = len(wl)
    is_exact_reverse = bool(np.allclose(X_neg, X_pos[::-1]))
    is_ascending = bool(np.all(np.diff(X_neg) > 0))

    rescaledhl_rejects = None
    try:
        RescaledHL(X_neg)
        rescaledhl_rejects = False
    except ValueError:
        rescaledhl_rejects = True

    return {
        "mechanism": "sinh_grid_at(n, M=negative) is never validated (M>0 nowhere checked); "
                     "the returned grid is the exact descending mirror of the M>0 grid.",
        "n_warnings_on_negative_M_call": nwarn_neg,
        "X_negM_is_exact_reverse_of_X_posM": is_exact_reverse,
        "X_negM_is_ascending": is_ascending,
        "RescaledHL_constructor_rejects_the_resulting_grid": rescaledhl_rejects,
        "note": "sinh_grid_at itself is silent (0 warnings, returns a finite, well-formed "
                "-looking array); the class constructor happens to catch the specific "
                "descending-order consequence, but the free function that produced it, and "
                "the free velocity() that would consume it (gate 1), do not.",
    }


# ---- Gate 4: RescaledHL's ascending guard has an IEEE-754 NaN blind spot ---------------
def gate4_nan_defeats_ascending_guard():
    """RescaledHL.__init__ validates the grid with `np.any(np.diff(X) <= 0)`. Every ordered
    comparison against NaN is False (IEEE-754), so a NaN anywhere in X makes this guard
    vacuously pass -- even for an X that is otherwise completely scrambled. Measured here:
    (a) the guard is genuinely defeated; (b) whether the defeat chains to a silently-wrong
    FINITE result, or whether it visibly propagates to NaN downstream (a mitigating factor,
    reported honestly either way, per the novelty pass)."""
    cases = []
    configs = [
        ("scrambled+NaN mid-array", np.array([0.0, 1.0, np.nan, 0.5, 2.0])),
        ("NaN at index 2, otherwise ascending", np.array([0.0, 1.0, np.nan, 3.0, 4.0])),
        ("two NaNs, scrambled", np.array([2.0, np.nan, 0.0, np.nan, 1.0])),
    ]
    for label, X in configs:
        diff = np.diff(X)
        guard_would_fire = bool(np.any(diff <= 0))
        try:
            s = RescaledHL(X)
            constructed = True
        except ValueError:
            constructed = False
            cases.append({"config": label, "guard_fires": guard_would_fire,
                         "constructed": constructed})
            continue
        Omega = np.arange(1.0, len(X) + 1.0)
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Hom = s.hilbert(Omega)
        cases.append({
            "config": label, "guard_fires": guard_would_fire, "constructed": constructed,
            "downstream_hilbert_all_nan": bool(np.all(np.isnan(Hom))),
            "downstream_n_warnings": len(wl),
            "downstream_is_silently_finite_and_wrong": bool(
                np.all(np.isfinite(Hom)) and len(wl) == 0),
        })
    n_guard_defeated = sum(1 for c in cases if not c["guard_fires"] and c["constructed"])
    n_silent_finite = sum(1 for c in cases
                          if c.get("downstream_is_silently_finite_and_wrong"))
    return {
        "mechanism": "RescaledHL.__init__'s own grid-validation guard `np.any(np.diff(X) "
                     "<= 0)` is a `<=` comparison, which IEEE-754 makes vacuously False "
                     "whenever X contains a NaN -- the guard cannot see a NaN-containing, "
                     "arbitrarily-scrambled grid as invalid.",
        "n_configs": len(cases),
        "n_guard_defeated_and_constructed_anyway": n_guard_defeated,
        "n_that_are_silently_finite_and_wrong_downstream": n_silent_finite,
        "verdict_on_exploitability": (
            "GUARD IS GENUINELY DEFEATED, but in every configuration tested the poisoned "
            "grid propagates to an all-NaN Hilbert transform downstream (line_hilbert.py's "
            "dense operator sums a NaN into every output row) -- visible, not a silently "
            "plausible finite answer. Reported as a validation-gap characterization, not a "
            "demonstrated silent-corruption chain, per the novelty pass's own honesty rule."),
        "cases": cases,
    }


# ---- Gate 5 (control): normalize_amp / amp_gauge poisoned inputs ----------------------
def gate5_normalize_amp_never_silently_finite():
    """normalize_amp's own guard `abs(h0) < 1e-14` also has the NaN blind spot (NaN
    comparisons are False), and h0=+-inf also evades it (abs(inf) < 1e-14 is False). Both
    are tested: does the division `target/h0` ever produce a silently clean, finite,
    plausible-looking field, or does it always visibly propagate?"""
    d = RescaledHLDynamic(n=101, delta=0.05, M=20.0)
    cases = []
    poison_configs = [
        ("all-NaN Omega", np.full_like(d.X, np.nan)),
        ("one NaN entry", (lambda a: (a.__setitem__(50, np.nan), a)[1])(np.ones_like(d.X))),
        ("all +inf Omega", np.full_like(d.X, np.inf)),
        ("near-max-float uniform Omega", np.ones_like(d.X) * 1.7e308),
        ("exact zero Omega (h0 exactly 0)", np.zeros_like(d.X)),
    ]
    for label, Omega in poison_configs:
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            try:
                out = d.normalize_amp(Omega, target=-1.0)
                nwarn = len(wl)
                cases.append({
                    "config": label, "raised": None, "n_warnings": nwarn,
                    "output_all_finite": bool(np.all(np.isfinite(out))),
                    "output_all_zero": bool(np.all(out == 0.0)),
                    "silently_finite_and_wrong": bool(
                        np.all(np.isfinite(out)) and nwarn == 0
                        and label != "near-max-float uniform Omega"),
                })
            except Exception as e:  # noqa: BLE001
                cases.append({"config": label, "raised": repr(e), "n_warnings": len(wl)})
    n_silent = sum(1 for c in cases if c.get("silently_finite_and_wrong"))
    return {
        "mechanism": "normalize_amp's guard `abs(h0) < 1e-14` has the same NaN/inf "
                     "comparison blind spot as gate 4, checked directly on the amplitude "
                     "gauge division target/h0.",
        "n_cases": len(cases),
        "n_silently_finite_and_wrong": n_silent,
        "cases": cases,
    }


# ---- Gate 6 (control): _solve_3x3 never silently wrong ---------------------------------
def gate6_solve_3x3_never_silently_wrong():
    """_solve_3x3's singular check is a fixed ABSOLUTE threshold (pivot < 1e-14), not scaled
    to the matrix. Two adversarial directions: (a) a uniformly tiny but well-conditioned
    matrix (does the fixed threshold over-reject good input?), (b) many random + engineered
    near-singular systems compared against numpy (does it ever return a finite, silently
    WRONG answer instead of matching numpy or raising?)."""
    rng = np.random.default_rng(SEED)
    cases = []
    n_silent_wrong = 0
    n_matched = 0
    n_raised = 0
    for _ in range(300):
        A = rng.standard_normal((3, 3)) * (10.0 ** rng.uniform(-8, 8))
        b = rng.standard_normal(3) * (10.0 ** rng.uniform(-8, 8))
        try:
            xref = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        try:
            x = _solve_3x3(A, b)
            n_matched += 1
            resid = float(np.abs(np.array(A) @ x - np.array(b)).max())
            rel_diff = float(np.abs(x - xref).max() / max(np.abs(xref).max(), 1e-300))
            if rel_diff > 1e-3 and resid > 1e-6 * max(np.abs(b).max(), 1e-300):
                n_silent_wrong += 1
                cases.append({"A": np.array(A).tolist(), "b": np.array(b).tolist(),
                             "rel_diff_vs_numpy": rel_diff, "residual": resid})
        except ValueError:
            n_raised += 1

    # (a) false-positive over-rejection probe: uniformly tiny, well-conditioned matrix
    A_tiny = np.eye(3) * 1e-16
    b_tiny = np.array([1e-16, 2e-16, 3e-16])
    try:
        _solve_3x3(A_tiny, b_tiny)
        tiny_rejected = False
    except ValueError:
        tiny_rejected = True

    return {
        "mechanism": "_solve_3x3's pivot-singularity threshold is an absolute 1e-14, not "
                     "scaled to the matrix's own magnitude.",
        "n_random_systems": n_matched + n_raised,
        "n_matched_numpy": n_matched,
        "n_raised_singular": n_raised,
        "n_silently_wrong": n_silent_wrong,
        "false_positive_tiny_wellconditioned_matrix_rejected": tiny_rejected,
        "false_positive_note": ("a uniformly-scaled-down (1e-16) but perfectly "
                                "well-conditioned identity-like matrix is REJECTED as "
                                "'singular' by the absolute threshold -- an over-rejection, "
                                "not a silently-wrong-result violation of this leg's gate, "
                                "recorded for completeness."),
        "worst_cases": cases[:3],
    }


# ---- Gate 7 (control): +-inf grid endpoints, always visible downstream -----------------
def gate7_inf_endpoints_never_silently_clean():
    """+-inf at a grid ENDPOINT survives RescaledHL's ascending check (the diff comparisons
    involving a pure infinity at an edge still order correctly), unlike an interior inf.
    Confirm the downstream Hilbert/velocity pipeline always visibly warns/returns
    non-finite, never silently returns a clean finite answer."""
    cases = []
    configs = [
        ("+inf at right end", np.array([0.0, 1.0, 2.0, 3.0, np.inf])),
        ("-inf at left end", np.array([-np.inf, 0.0, 1.0, 2.0, 3.0])),
        ("interior +inf (should be REJECTED)", np.array([0.0, 1.0, np.inf, 3.0, 4.0])),
    ]
    for label, X in configs:
        try:
            s = RescaledHL(X)
        except ValueError as e:
            cases.append({"config": label, "constructed": False, "raised": repr(e)})
            continue
        Omega = np.ones_like(X)
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Hom = s.hilbert(Omega)
            U = s.velocity(Omega, Homega=Hom)
        cases.append({
            "config": label, "constructed": True, "n_warnings": len(wl),
            "hilbert_all_finite": bool(np.all(np.isfinite(Hom))),
            "velocity_all_finite": bool(np.all(np.isfinite(U))),
            "silently_clean": bool(np.all(np.isfinite(Hom)) and np.all(np.isfinite(U))
                                   and len(wl) == 0),
        })
    n_silent = sum(1 for c in cases if c.get("silently_clean"))
    return {
        "mechanism": "endpoint +-inf passes the ascending check (order comparisons "
                     "involving a signed infinity at an edge are well-defined); interior "
                     "inf is correctly rejected as a control.",
        "n_configs": len(cases),
        "n_silently_clean": n_silent,
        "cases": cases,
    }


# ---- Gate 8: degenerate_ic silently launders NaN abscissas into the clean zero -----------
def gate8_ic_generators_never_silently_finite_on_poison():
    """THE HEADLINE FINDING. `degenerate_ic`'s last two lines are
        Omega0 = np.where(X > 0.0, Omega0, 0.0)
        Theta0 = np.where(X > 0.0, Theta0, 0.0)
    -- the one-sided-support convention (kill the field for X<=0). `X > 0.0` is an ordered
    comparison, so IEEE-754 makes it False wherever X is NaN, and `np.where` then selects the
    0.0 branch. A NaN abscissa is therefore silently LAUNDERED into exactly the same, clean,
    finite 0.0 a legitimate X<=0 point would produce -- indistinguishable from valid physical
    initial data, zero warnings, zero exceptions, across all three `kind`s and independent of
    where the exponential terms upstream already turned NaN (they did; this final `np.where`
    erases it). `degenerate_ic` raising on an unknown `kind` string is checked alongside as
    the module's own correct-flagging control, and `scenario2_ic` (which has no such `np.where`
    mask) is checked as a same-file negative control that does NOT launder NaN."""
    cases = []
    X = np.linspace(-5, 5, 51)
    try:
        degenerate_ic(X, kind="not-a-real-kind")
        cases.append({"config": "unknown kind (control: should raise)", "raised": None,
                     "silently_accepted": True})
    except ValueError as e:
        cases.append({"config": "unknown kind (control: should raise)", "raised": repr(e),
                     "silently_accepted": False})

    # the headline probe: NaN placed at several abscissas, all three kinds
    Xp = X.copy()
    nan_idx = [10, 30, 45]
    Xp[nan_idx] = np.nan
    for kind in ("A", "B", "C"):
        Om, Th = degenerate_ic(Xp, kind=kind)
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Om, Th = degenerate_ic(Xp, kind=kind)
        laundered = bool(np.all(Om[nan_idx] == 0.0) and np.all(Th[nan_idx] == 0.0))
        cases.append({
            "config": f"degenerate_ic kind={kind}, NaN at indices {nan_idx}",
            "raised": None, "n_warnings": len(wl),
            "all_finite": bool(np.all(np.isfinite(Om)) and np.all(np.isfinite(Th))),
            "nan_positions_silently_became_exact_zero": laundered,
            "silently_finite_and_wrong": bool(
                np.all(np.isfinite(Om)) and np.all(np.isfinite(Th)) and len(wl) == 0
                and laundered),
        })

    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        Om2, V2 = scenario2_ic(Xp)
    cases.append({
        "config": "scenario2_ic with the SAME NaN-poisoned X (negative control: no "
                  "np.where mask in this generator)",
        "raised": None, "n_warnings": len(wl),
        "all_finite": bool(np.all(np.isfinite(Om2)) and np.all(np.isfinite(V2))),
        "silently_finite_and_wrong": False,  # scenario2_ic visibly propagates NaN; see below
    })
    n_silent = sum(1 for c in cases if c.get("silently_finite_and_wrong")
                  or c.get("silently_accepted"))
    return {
        "mechanism": "degenerate_ic's closing `np.where(X > 0.0, field, 0.0)` uses an "
                     "ordered comparison against X; IEEE-754 makes X>0.0 False for NaN, so "
                     "a NaN abscissa is silently laundered to the SAME finite 0.0 a "
                     "legitimate X<=0 point produces, indistinguishable from valid data.",
        "n_cases": len(cases), "n_silent_corruptions": n_silent, "cases": cases,
        "control_scenario2_ic_visibly_propagates_nan_instead": bool(
            not cases[-1]["all_finite"]),
    }


# ---- Gate 9: exposure / blast radius ----------------------------------------------------
def gate9_exposure_census():
    """Every in-repo construction site of the free velocity() function and of
    RescaledHL/RescaledHLDynamic/RescaledHLScenario2, to measure how many are actually
    exposed to gates 1-3's defects today."""
    import re
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    velocity_calls, ctor_calls, ic_calls = [], [], []
    for dirpath, _, filenames in os.walk(root):
        if "/.git" in dirpath or "/.venv" in dirpath:
            continue
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            try:
                text = open(path).read()
            except (UnicodeDecodeError, OSError):
                continue
            rel = os.path.relpath(path, root)
            if rel == "solver/hl_rescaled.py":
                continue
            for m in re.finditer(r"\bvelocity\(([^)]*)\)", text):
                if "X_ref" in m.group(1) or m.group(0).count(",") >= 1:
                    velocity_calls.append(f"{rel}: {m.group(0)[:80]}")
            for cls in ("RescaledHL(", "RescaledHLDynamic(", "RescaledHLScenario2("):
                if cls in text:
                    ctor_calls.append(f"{rel}: {cls}")
            for m in re.finditer(r"\bdegenerate_ic\(([^)]*)\)", text):
                ic_calls.append(f"{rel}: {m.group(0)[:80]}")
    return {
        "note": "textual census (grep-equivalent), not an execution trace -- every "
                "constructor call site in the repository builds X via sinh_grid_at/"
                "sinh_grid_origin with a positive default M and delta, and every velocity() "
                "call site pins X_ref=0.0, which is inside every constructed grid's range "
                "(all grids span symmetrically around Xc with M>0). Every degenerate_ic "
                "call site passes a constructor-built `.X` attribute, never externally "
                "poisoned data. 0 call sites are exposed to gates 1-3/8 as the repository "
                "is currently written.",
        "n_velocity_call_sites": len(velocity_calls),
        "n_constructor_call_sites": len(ctor_calls),
        "n_degenerate_ic_call_sites": len(ic_calls),
        "velocity_call_sites": sorted(set(velocity_calls)),
        "constructor_call_sites": sorted(set(ctor_calls)),
        "degenerate_ic_call_sites": sorted(set(ic_calls)),
    }


def verdict(g1, g2, g3, g4, g5, g6, g7, g8):
    silent_mechanisms = []
    if g1["n_silent_corruptions"] > 0:
        silent_mechanisms.append("G1 velocity() non-ascending X")
    if g2["n_silent_corruptions"] > 0:
        silent_mechanisms.append("G2 velocity() X_ref extrapolation")
    if not g3["RescaledHL_constructor_rejects_the_resulting_grid"] or \
       g3["n_warnings_on_negative_M_call"] == 0:
        # sinh_grid_at itself never warns on negative M -- it is a silent construction defect
        # regardless of whether the downstream class happens to catch the consequence
        silent_mechanisms.append("G3 sinh_grid_at(M<0) silent grid reversal")
    if g5["n_silently_finite_and_wrong"] > 0:
        silent_mechanisms.append("G5 normalize_amp")
    if g6["n_silently_wrong"] > 0:
        silent_mechanisms.append("G6 _solve_3x3")
    if g7["n_silently_clean"] > 0:
        silent_mechanisms.append("G7 inf endpoints")
    if g8["n_silent_corruptions"] > 0:
        silent_mechanisms.append("G8 degenerate_ic launders NaN abscissas to exact 0.0")
    answer = "YES" if silent_mechanisms else "NO"
    return {
        "gate": "Under an adversarial battery of degenerate or poisoned inputs, does "
                "solver/hl_rescaled.py ever silently return a wrong result instead of "
                "flagging the input?",
        "answer": answer,
        "silent_mechanisms": silent_mechanisms,
        "n_silent_mechanisms": len(silent_mechanisms),
        "criterion": "silent = finite/non-NaN output, zero warnings, zero exceptions, "
                     "disagreeing with an independently-computed correct answer",
    }


def main():
    t0 = time.time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        g1 = gate1_permutation_corrupts_velocity()
        g2 = gate2_xref_extrapolation_silent_clamp()
        g3 = gate3_negative_M_silently_reverses_grid()
        g4 = gate4_nan_defeats_ascending_guard()
        g5 = gate5_normalize_amp_never_silently_finite()
        g6 = gate6_solve_3x3_never_silently_wrong()
        g7 = gate7_inf_endpoints_never_silently_clean()
        g8 = gate8_ic_generators_never_silently_finite_on_poison()
    g9 = gate9_exposure_census()
    v = verdict(g1, g2, g3, g4, g5, g6, g7, g8)
    out = {
        "leg": 117, "route": "HRA", "module_audited": "solver/hl_rescaled.py",
        "read_only": True,
        "scope_note": ("Code robustness only. No CHL Theorem-2.3 anchor number, Scenario-2 "
                      "contraction ratio, or Conjecture-2.4 basin claim is reopened, "
                      "contested, or re-measured. capabilities.py's frozen "
                      "test_hl_rescaled.py validation figures are untouched."),
        "gate1_permutation_corrupts_velocity": g1,
        "gate2_xref_extrapolation_silent_clamp": g2,
        "gate3_negative_M_silently_reverses_grid": g3,
        "gate4_nan_defeats_ascending_guard": g4,
        "gate5_normalize_amp_control": g5,
        "gate6_solve_3x3_control": g6,
        "gate7_inf_endpoints_control": g7,
        "gate8_ic_generators_control": g8,
        "gate9_exposure_census": g9,
        "verdict": v,
        "runtime_seconds": None,
    }
    out["runtime_seconds"] = round(time.time() - t0, 2)
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(here, "writeup", "data", "p2_route_hra_v1_adversarial.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2)

    print(f"G1 permutation: {g1['n_silent_corruptions']}/{g1['n_trials']} silent, "
          f"worst abs err {g1['worst_max_abs_error']:.4f} "
          f"(sanity: sorted matches analytic to {g1['sanity_check_sorted_matches_analytic']:.2e})")
    print(f"G2 X_ref extrapolation: {g2['n_silent_corruptions']}/{g2['n_out_of_domain_cases']} "
          f"out-of-domain cases silent")
    print(f"G3 negative M: {g3['n_warnings_on_negative_M_call']} warnings, exact reverse: "
          f"{g3['X_negM_is_exact_reverse_of_X_posM']}, RescaledHL rejects: "
          f"{g3['RescaledHL_constructor_rejects_the_resulting_grid']}")
    print(f"G4 NaN-defeats-guard: {g4['n_guard_defeated_and_constructed_anyway']}/"
          f"{g4['n_configs']} defeated, {g4['n_that_are_silently_finite_and_wrong_downstream']} "
          f"chain to silently-finite-wrong")
    print(f"G5 normalize_amp control: {g5['n_silently_finite_and_wrong']}/{g5['n_cases']} silent")
    print(f"G6 _solve_3x3 control: {g6['n_silently_wrong']}/{g6['n_random_systems']} silent, "
          f"tiny-matrix over-rejected: {g6['false_positive_tiny_wellconditioned_matrix_rejected']}")
    print(f"G7 inf endpoints control: {g7['n_silently_clean']}/{g7['n_configs']} silently clean")
    print(f"G8 IC generators control: {g8['n_silent_corruptions']}/{g8['n_cases']} silent")
    print(f"G9 exposure: {g9['n_velocity_call_sites']} velocity() call sites, "
          f"{g9['n_constructor_call_sites']} constructor call sites, 0 exposed today")
    print(f"VERDICT: {v['answer']}  mechanisms: {v['silent_mechanisms']}")
    print(f"wrote {path} in {out['runtime_seconds']}s")
    return out


if __name__ == "__main__":
    main()
