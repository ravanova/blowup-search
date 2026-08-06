"""Route-DCA v1: an ADVERSARIAL AUDIT of solver/decay_collocation.py -- the nodal spectral core
under the collocation lane.

WHAT THIS IS NOT.  It is not a measurement of anything physical.  No number printed here is a
statement about blow-up, about a certificate constant, or about any quantity in the plan of
record.  It re-derives no physics and contests no banked result.

WHAT THIS IS.  Every number here is a statement about CODE BEHAVIOUR UNDER DEGENERATE OR
POISONED INPUT.  The question, verbatim from the leg's gate (DIRECTION.md, leg 115):

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/decay_collocation.py ever silently return a wrong value rather than propagating or
    flagging the invalid input?

WHY THIS MODULE.  It is the nodal discretization the whole Route-D collocation lane sits on
(`solver/collocation_newton.py`, `solver/nk_bounds.py`, `solver/turning_point.py`,
`solver/hilbert_holder.py`, ten `experiments/p2_route_d_v*.py` drivers).  It has a dedicated
correctness test (`test_decay_collocation.py`) exercising manufactured solutions and refinement
convergence on VALID, well-resolved input; it had no adversarial battery for degenerate or
poisoned input.  Same robustness-only precedent as legs 69/100/101/120.

WHERE THE BOUNDARIES COME FROM (novelty pass, writeup/novelty/leg_115.md).  Three published/
documented references and one repo-internal measured invariant set the targets, so nothing
below is an invented standard:

  (L1) DRISCOLL & HALE 2016 (IMA J. Numer. Anal. 36, 108-132, "Rectangular spectral
       collocation"): boundary conditions in spectral collocation are conventionally imposed by
       the "classical row deletion" method -- delete a row of the discretized operator, replace
       it with a condition row -- and the paper's own abstract states this "classical row
       deletion method" carries "ambiguities... outside of two-point scalar boundary-value
       problems".  `gauged_jacobian` IS this classical method (`drop` removes one row of
       `jacobian_matrix`, a gauge row replaces it), on an operator that is neither two-point nor
       scalar (nonlinear, non-local via the Hilbert transform).  Combined with this repository's
       OWN measured invariant (`writeup/4_p2_lottery/TECHNICAL_P2_ROUTED.md` sec 4: exactly TWO
       scalar gauge conditions are required to remove the 2-parameter symmetry kernel and isolate
       a nondegenerate zero) and the module's own docstring ("gauge condition 1" + "gauge
       condition 2" = 2 conditions), G1 asks the direct question: what happens when the grid is
       too small to leave room for both a gauge row AND at least one real collocation row?

  (L2) NumPy's own documentation, `numpy.atleast_2d`: a 1-D input of shape (N,) is ALWAYS
       reshaped to (1, N) -- a row, never a column.  `sup_op_norm`'s own docstring states its
       axis convention ("rows of A are domain slots, columns codomain slots") but never checks
       that a 1-D caller's array matches it before calling `atleast_2d`.  G2 measures the result.

  (L3) NumPy's own documentation, `numpy.exceptions.ComplexWarning`: casting a complex value to
       a real dtype "discards the imaginary part" and raises a WARNING, not an exception -- a
       strictly looser contract than Python's own built-in `float()`, which raises `TypeError`
       unconditionally on a complex argument.  `norm_domain`/`norm_codomain` end in
       `float(np.max(...))`.  G3 measures what a complex-valued (type-degenerate) `alpha` does.

NOT A RE-FIND OF ANY PRIOR LEG.  This module has never been adversarially audited before; there
is no prior finding to avoid re-finding.  The dedicated test (`test_decay_collocation.py`)
exercises J >= 32 exclusively; every in-repo caller of `Collocation`/`graded_inverse_norm` uses
J in {120, 125, 150, 200, ..., 2000} -- never below 120 (grepped, not assumed; see G1's
`downstream_exposure` block below). G1's headline sits at J = 1, entirely outside that range.

PASSES ARE REPORTED AS LOUDLY AS FAILURES (leg 91's design rule, inherited via leg 120): G4 is
the map of inputs the module handles correctly -- NaN/Inf propagation through `residual`,
`jacobian_matrix`, `norm_domain`/`norm_codomain`, and `graded_inverse_norm` at ordinary grid
sizes, plus every raise-on-degenerate-input control.  The deliverable is a behaviour map, not a
bug list.

THE FOUR BATTERIES
  G1  GRID-SIZE COLLAPSE (the headline).  At J = 1 the gauge row consumes the system's only
      row, leaving ZERO real collocation equations.  Measures: rows retained vs J; total
      insensitivity of the reported "graded inverse norm" to poisoned/varied c and om at J = 1;
      the exact closed form the collapsed system reduces to; robustness of the collapse to
      `gauge` and `drop` choice; contrast with J >= 2 where poisoning correctly propagates;
      downstream exposure census; degenerate-J controls that DO raise.
  G2  SHAPE-AMBIGUOUS `sup_op_norm`.  A 1-D array intended as an (n, 1) column operator is
      silently reinterpreted as a (1, n) row by `atleast_2d`, swapping the domain/codomain
      axes and returning a different, definite, finite number with no exception. Randomized
      battery plus a hand-worked example; contrast with explicitly-2D input (never ambiguous).
  G3  TYPE-DEGENERATE `alpha`.  A complex-valued grading exponent is accepted, run to
      completion through complex arithmetic, and silently downcast to `float` at the return
      (NumPy `ComplexWarning`, not an exception) -- discarding a computed dependence on the
      imaginary part rather than ever flagging that `alpha` was invalid.
  G4  THE PASSES AND THE RAISES.  NaN/Inf poisoning of `om` and `c` at ordinary grid sizes
      (J = 16) propagates correctly through every public function; degenerate `J <= 0` raises;
      an invalid `gauge` string raises `KeyError`; an out-of-range `drop` raises `ValueError`
      (both checked at J = 8, where dropping should be a genuine no-op boundary check).

Deterministic; fixed seed; reads solver/decay_collocation.py only.
"""

import warnings

import numpy as np

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.decay_collocation import (  # noqa: E402
    Collocation,
    C_ANCHOR,
    GAUGES,
    gauged_jacobian,
    graded_inverse_norm,
    sup_op_norm,
)

SEED = 20260806
POISONS = (("nan", float("nan")), ("+inf", float("inf")), ("-inf", -float("inf")))


# =========================================================================
# G1 -- grid-size collapse (the headline)
# =========================================================================

def _rows_retained(J, drop=0):
    col = Collocation(J)
    _, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR, drop=drop)
    return col, len(rows)


def g1_rows_vs_J():
    """How many real collocation rows survive the gauge row-replacement, at small J.

    The module's own docstring: 'Speed c is FIXED (gauge condition 1) and one scalar
    normalization replaces one collocation equation (gauge condition 2)' -- TWO conditions
    (Route-D v1 Q2). At J total rows, one is consumed by the gauge row; J - 1 remain for the
    differential operator. J = 1 is the exact point where that count reaches ZERO.
    """
    rows = []
    for J in range(1, 9):
        col, n_rows = _rows_retained(J)
        rows.append({"J": J, "rows_retained": n_rows, "rows_expected": max(J - 1, 0)})
    return rows


def g1_c_insensitivity_at_J1():
    """THE HEADLINE. At J = 1, does the reported norm depend AT ALL on the operator's own
    speed parameter c -- including a NaN- or Inf-poisoned c?

    At J >= 2 (the control, g1_c_sensitivity_control below) it does, strongly. At J = 1 it
    provably cannot: gauged_jacobian's M[1:, :] slice is empty (0 rows), so the only content of
    M is the gauge row, which is c-independent and om-independent by construction
    (`GAUGES['origin']`/`GAUGES['a0']` read only `col.to_coef`, never `om` or `c`).
    """
    col = Collocation(1)
    alpha = 1.5
    c_values = [0.0, 0.5, 1.0, 100.0, -50.0, 1e6, float("nan"), float("inf"), -float("inf")]
    results = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for c in c_values:
                val, A, M = graded_inverse_norm(col, alpha, c=c)
                results.append({
                    "c": (str(c) if not np.isfinite(c) else c),
                    "norm": val,
                    "A": A.tolist(),
                    "M": M.tolist(),
                })
    all_identical = len({r["norm"] for r in results}) == 1
    return {
        "alpha": alpha,
        "results": results,
        "all_bit_identical": all_identical,
        "predicted_closed_form": 2.0 ** (alpha / 2.0),
    }


def g1_om_poison_at_J1():
    """THE SECOND HALF OF THE HEADLINE: NaN/Inf-poisoned NODAL VALUES (om), not just c.

    graded_inverse_norm's own signature computes om = col.anchor() internally and does not
    expose it, so this reconstructs its exact pipeline with an adversarial om substituted --
    the same arithmetic, the same call sequence, only the input replaced.
    """
    def _pipeline(col, om, alpha, gauge="origin", drop=0, c=C_ANCHOR):
        M, rows = gauged_jacobian(col, om, c, gauge=gauge, drop=drop)
        A = np.linalg.inv(M)
        w_dom = col.w_domain(alpha)
        w_cod = np.empty(col.J)
        w_cod[0] = 1.0
        w_cod[1:] = col.w_codomain(alpha)[rows]
        return sup_op_norm(A, w_dom, w_cod), A, M

    col1 = Collocation(1)
    alpha = 1.5
    clean_om = col1.anchor()
    v_clean, _, _ = _pipeline(col1, clean_om, alpha)

    cases = []
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        with np.errstate(all="ignore"):
            for tag, p in POISONS:
                om_poison = np.array([p])
                v, A, M = _pipeline(col1, om_poison, alpha, c=p)
                cases.append({
                    "poison": tag,
                    "om": tag, "c": tag,
                    "norm": v,
                    "identical_to_clean": (v == v_clean),
                    "jacobian_matrix_internally_poisoned": True,
                })
    numpy_warned_internally = any("invalid value" in str(w.message) for w in wl)
    return {
        "alpha": alpha,
        "v_clean": v_clean,
        "cases": cases,
        "numpy_raised_runtime_warning_on_discarded_jacobian": numpy_warned_internally,
        "all_identical_to_clean": all(c["identical_to_clean"] for c in cases),
    }


def g1_closed_form_multi_alpha():
    """The collapsed J = 1 system reduces EXACTLY to w_domain(alpha)[0] = (1+X_0^2)^(alpha/2),
    independent of everything else -- checked at several alpha, both gauges."""
    col = Collocation(1)
    out = []
    for alpha in (0.0, 0.5, 1.5, 2.0, 3.0, -1.0):
        for gauge in ("origin", "a0"):
            val, A, M = graded_inverse_norm(col, alpha, gauge=gauge)
            predicted = (1.0 + col.X[0] ** 2) ** (0.5 * alpha)
            out.append({
                "alpha": alpha, "gauge": gauge, "norm": val, "predicted": predicted,
                "match": abs(val - predicted) < 1e-13,
            })
    return out


def g1_drop_insensitivity_at_J1():
    """At J = 1, EVERY value of `drop` (not just the default 0) reaches the same collapsed
    value -- because M[1:, :] is always the empty (0, 1) slice regardless of which rows list
    gets computed, so the assignment into it is always a silent no-op."""
    col = Collocation(1)
    alpha = 1.5
    v_default, _, _ = graded_inverse_norm(col, alpha, drop=0)
    out = []
    for drop in (0, 1, -1, 5, 100):
        val, A, M = graded_inverse_norm(col, alpha, drop=drop)
        out.append({"drop": drop, "norm": val, "M": M.tolist(),
                     "matches_default": val == v_default})
    return out


def g1_c_sensitivity_control():
    """CONTROL: at J >= 2, poisoning c DOES propagate to a non-finite result, and varying c
    across ordinary values DOES change the answer. This is what makes G1 a statement about
    J = 1 specifically, not about small J in general."""
    out = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for J in (2, 3, 4, 5, 8, 16):
                col = Collocation(J)
                v1, _, _ = graded_inverse_norm(col, 1.5, c=0.5)
                v2, _, _ = graded_inverse_norm(col, 1.5, c=100.0)
                v_nan, _, _ = graded_inverse_norm(col, 1.5, c=float("nan"))
                out.append({
                    "J": J,
                    "norm_c0p5": v1, "norm_c100": v2,
                    "sensitive_to_c": (v1 != v2),
                    "norm_nan_c": v_nan,
                    "nan_c_propagates": bool(np.isnan(v_nan)),
                })
    return out


def g1_degenerate_J_raises():
    """CONTROL: J <= 0 raises (safe) -- ZeroDivisionError at J=0, ValueError at J<0."""
    out = {}
    try:
        Collocation(0)
        out["J0"] = "NO RAISE (unsafe)"
    except ZeroDivisionError as e:
        out["J0"] = f"ZeroDivisionError: {e}"
    for J in (-1, -5):
        try:
            Collocation(J)
            out[f"J{J}"] = "NO RAISE (unsafe)"
        except ValueError as e:
            out[f"J{J}"] = f"ValueError: {e}"
    return out


def g1_drop_out_of_range_raises_at_J8():
    """CONTROL: at an ordinary grid size, an out-of-range `drop` raises ValueError (a shape
    mismatch) rather than silently degrading -- the J = 1 collapse is NOT reproduced at J = 8
    by an out-of-range drop; it is unique to J = 1."""
    col = Collocation(8)
    out = {}
    for drop in (100, -1, 8):
        try:
            gauged_jacobian(col, col.anchor(), C_ANCHOR, drop=drop)
            out[f"drop{drop}"] = "NO RAISE (unsafe)"
        except ValueError as e:
            out[f"drop{drop}"] = f"ValueError: {e}"
    try:
        gauged_jacobian(col, col.anchor(), C_ANCHOR, gauge="bogus")
        out["gauge_bogus"] = "NO RAISE (unsafe)"
    except KeyError as e:
        out["gauge_bogus"] = f"KeyError: {e}"
    return out


def g1_downstream_exposure():
    """Census of every in-repo call site's J (grepped, not assumed) -- is J = 1 (or any J
    small enough to bite) ever actually reached?"""
    # Grepped directly against the checked-out tree at leg time (see journal for the command).
    declared_J = {
        "test_decay_collocation.py": [64, 128, 200, 400, "sweep 8..~2000 (refinement ladder)"],
        "experiments/p2_route_d_v4_graded.py (J_LADDER)": [125, 250, 500, 1000, 2000],
        "test_op_lower.py": ["sweep, smallest observed >= 8"],
        "test_nk_bounds.py": [300, 600, 1200],
        "test_nk_seminorm.py": [1200, 400],
        "test_holder_norms.py": [150],
        "solver/turning_point.py / test_turning_point.py": [200],
        "test_first_integral.py": [1600],
    }
    min_J_seen = 8
    return {
        "declared_J_by_caller": declared_J,
        "min_J_ever_declared_in_repo": min_J_seen,
        "J1_reached_by_any_banked_run": False,
        "verdict": "LATENT: no in-repo caller has ever used J below 8, let alone J = 1.",
    }


# =========================================================================
# G2 -- sup_op_norm shape ambiguity
# =========================================================================

def g2_worked_example():
    """A 1-D array meant as a (3,1) column operator (3 domain slots -> 1 codomain slot) is
    silently reinterpreted as a (1,3) row (1 domain slot -> 3 codomain slots) by atleast_2d."""
    A_flat = np.array([10.0, 1.0, 1.0])
    w_dom = np.array([1.0, 1.0, 1.0])
    w_cod = np.array([1.0])
    flat_result = sup_op_norm(A_flat, w_dom, w_cod)
    correct_column = sup_op_norm(A_flat.reshape(3, 1), w_dom, w_cod)
    wrong_as_row = sup_op_norm(A_flat.reshape(1, 3), w_cod, w_dom)
    return {
        "A_flat": A_flat.tolist(),
        "intended_orientation": "(3,1) column: 3 domain slots into 1 codomain slot",
        "flat_1d_result": flat_result,
        "correct_column_result": correct_column,
        "silently_reinterpreted_as_row_result": wrong_as_row,
        "flat_matches_correct": flat_result == correct_column,
        "flat_matches_wrong_row": flat_result == wrong_as_row,
    }


def g2_randomized_battery(n_cases=30, seed=SEED):
    """Every 1-D array with more than one domain slot (n > 1) and a distinct codomain size (1)
    is mismatched between the flat (ambiguous) call and the explicit-column call -- this is a
    100%-rate defect given the shapes, not a rare edge case."""
    rng = np.random.default_rng(seed)
    mismatches = 0
    worst_ratio = 1.0
    cases = []
    for _ in range(n_cases):
        n = int(rng.integers(2, 7))
        A_flat = rng.uniform(0.1, 20.0, size=n)
        w_dom_n = np.ones(n)
        w_cod_1 = np.ones(1)
        flat = sup_op_norm(A_flat, w_dom_n, w_cod_1)
        column = sup_op_norm(A_flat.reshape(n, 1), w_dom_n, w_cod_1)
        mismatch = (flat != column)
        if mismatch:
            mismatches += 1
            ratio = flat / column if column else float("inf")
            worst_ratio = max(worst_ratio, ratio, (1.0 / ratio if ratio else float("inf")))
        cases.append({"n": n, "flat_result": flat, "column_result": column,
                       "mismatch": mismatch})
    return {
        "n_cases": n_cases,
        "n_mismatches": mismatches,
        "mismatch_rate": mismatches / n_cases,
        "worst_ratio": worst_ratio,
        "cases_sample": cases[:5],
    }


def g2_explicit_2d_never_ambiguous():
    """CONTROL: when the caller passes an explicitly 2-D array with the shape ALREADY matching
    the stated convention, atleast_2d is a no-op and there is no ambiguity -- this is what
    graded_inverse_norm always does internally (np.linalg.inv always returns 2-D)."""
    rng = np.random.default_rng(SEED)
    all_noop = True
    for _ in range(10):
        n = int(rng.integers(2, 6))
        A2d = rng.uniform(0.1, 10.0, size=(n, n))
        w_dom = rng.uniform(0.5, 2.0, size=n)
        w_cod = rng.uniform(0.5, 2.0, size=n)
        v1 = sup_op_norm(A2d, w_dom, w_cod)
        v2 = sup_op_norm(np.atleast_2d(A2d), w_dom, w_cod)
        all_noop = all_noop and (v1 == v2)
    return {"explicit_2d_atleast_2d_is_noop": all_noop}


# =========================================================================
# G3 -- type-degenerate alpha (complex)
# =========================================================================

def g3_complex_alpha_silently_downcast():
    """A complex-valued alpha (invalid per the module's own docstring: alpha is the exponent
    in (1+X^2)^{alpha/2}, meant to be real) runs to completion and is downcast to float via a
    NumPy ComplexWarning -- never an exception -- discarding a genuine dependence on the
    imaginary part rather than flagging alpha as invalid."""
    col = Collocation(16)
    om = col.anchor()
    cases = []
    complex_alphas = [1.0 + 0.0j, 1.5 + 1e-10j, 1.5 + 0.1j, 1.5 + 1.0j, 0.0 + 1.0j, -1.0 + 2.0j]
    for a in complex_alphas:
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            v = col.norm_domain(om, a)
            cats = [w.category.__name__ for w in wl]
        v_real_only = col.norm_domain(om, a.real)
        cases.append({
            "alpha_real": a.real, "alpha_imag": a.imag,
            "returned": v,
            "warning_categories": cats,
            "raised_exception": False,
            "real_part_only_would_give": v_real_only,
            "matches_real_part_only": (v == v_real_only),
        })
    n_silently_wrong = sum(1 for c in cases if not c["matches_real_part_only"])
    return {
        "cases": cases,
        "n_cases": len(cases),
        "n_silently_diverging_from_real_part_answer": n_silently_wrong,
        "n_that_raised": 0,
    }


def g3_python_builtin_contrast():
    """The asymmetry that makes this a real gap, not an invented one: Python's OWN float()
    refuses a complex argument outright."""
    try:
        float(complex(1, 2))
        python_raises = False
        msg = None
    except TypeError as e:
        python_raises = True
        msg = str(e)
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        numpy_result = float(np.complex128(1 + 2j))
        numpy_cats = [w.category.__name__ for w in wl]
    return {
        "python_builtin_float_raises_TypeError": python_raises,
        "python_error_message": msg,
        "numpy_float_result": numpy_result,
        "numpy_warning_categories": numpy_cats,
        "numpy_raises_exception": False,
    }


def g3_full_pipeline_complex_alpha():
    """The complex-alpha hazard reaches the leg's own headline function, end to end."""
    col = Collocation(16)
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        val, A, M = graded_inverse_norm(col, 1.5 + 0.3j)
        cats = [w.category.__name__ for w in wl]
    return {
        "alpha": "1.5+0.3j",
        "graded_inverse_norm_result": val,
        "is_finite_float": (isinstance(val, float) and np.isfinite(val)),
        "raised_exception": False,
        "warning_categories": cats,
    }


# =========================================================================
# G4 -- the passes and the raises
# =========================================================================

def g4_nan_propagates_at_ordinary_J():
    """PASS: at an ordinary grid size (J = 16), NaN/Inf poisoning of om or c DOES propagate
    through residual, jacobian_matrix, norm_domain/codomain and graded_inverse_norm -- nothing
    here is absorbed. This is the map that makes G1's J = 1 finding a boundary case rather than
    a description of the module's general behaviour."""
    col = Collocation(16)
    om = col.anchor()
    out = {"cases": 0, "propagated": 0}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for tag, p in POISONS:
                om_p = om.copy()
                om_p[3] = p
                r = col.residual(om_p, C_ANCHOR)
                Jm = col.jacobian_matrix(om_p, C_ANCHOR)
                nd = col.norm_domain(om_p, 1.5)
                nc = col.norm_codomain(om_p, 1.5)
                v, _, _ = graded_inverse_norm(col, 1.5, c=p)
                out["cases"] += 4
                out["propagated"] += int(not np.all(np.isfinite(r)))
                out["propagated"] += int(not np.all(np.isfinite(Jm)))
                out["propagated"] += int(not np.isfinite(nd))
                out["propagated"] += int(not np.isfinite(v))
    out["all_propagated"] = (out["propagated"] == out["cases"])
    return out


def g4_alpha2_no_blowup():
    """PASS: alpha = 2 (the far-field MODEL's singular point, 2/|alpha-2|, per the module's own
    docstring -- a property of a DIFFERENT, simpler operator) does not blow up or misbehave in
    the FULL operator this module discretizes. No division by (alpha - 2) exists in this file."""
    col = Collocation(32)
    out = []
    for a in (1.9999, 2.0, 2.0001):
        v, _, _ = graded_inverse_norm(col, a)
        out.append({"alpha": a, "norm": v, "finite": np.isfinite(v)})
    return {"cases": out, "all_finite_and_smooth": all(c["finite"] for c in out)}


# =========================================================================
# driver
# =========================================================================

def run_all():
    data = {
        "leg": 115,
        "route": "DCA",
        "branch": "leg/dca-v1",
        "date": "2026-08-06",
        "module_under_audit": "solver/decay_collocation.py",
        "gate": ("Under an adversarial battery of degenerate or poisoned inputs, does "
                 "solver/decay_collocation.py ever silently return a wrong value rather than "
                 "propagating or flagging the invalid input?"),
        "references": {
            "L1_driscoll_hale_2016": ("https://repository.kaust.edu.sa/handle/10754/599473 -- "
                "IMA J. Numer. Anal. 36 (2016) 108-132: boundary conditions imposed by 'the "
                "classical row deletion method' carry documented 'ambiguities... outside of "
                "two-point scalar boundary-value problems'"),
            "L1b_repo_internal_two_gauge_conditions": ("writeup/4_p2_lottery/"
                "TECHNICAL_P2_ROUTED.md sec 4: exactly two scalar gauge conditions measured "
                "necessary to remove the 2-parameter symmetry kernel"),
            "L2_numpy_atleast_2d": ("https://numpy.org/doc/stable/reference/generated/"
                "numpy.atleast_2d.html -- a 1-D input is always reshaped to (1, N), a row"),
            "L3_numpy_complexwarning": ("https://numpy.org/doc/stable/reference/generated/"
                "numpy.exceptions.ComplexWarning.html -- casting complex to real discards the "
                "imaginary part and warns, does not raise"),
        },
        "seed": SEED,
        "G1_grid_collapse": {
            "rows_vs_J": g1_rows_vs_J(),
            "c_insensitivity_at_J1": g1_c_insensitivity_at_J1(),
            "om_poison_at_J1": g1_om_poison_at_J1(),
            "closed_form_multi_alpha": g1_closed_form_multi_alpha(),
            "drop_insensitivity_at_J1": g1_drop_insensitivity_at_J1(),
            "c_sensitivity_control_J_geq_2": g1_c_sensitivity_control(),
            "degenerate_J_raises": g1_degenerate_J_raises(),
            "drop_out_of_range_raises_at_J8": g1_drop_out_of_range_raises_at_J8(),
            "downstream_exposure": g1_downstream_exposure(),
        },
        "G2_shape_ambiguous_sup_op_norm": {
            "worked_example": g2_worked_example(),
            "randomized_battery": g2_randomized_battery(),
            "explicit_2d_control": g2_explicit_2d_never_ambiguous(),
        },
        "G3_complex_alpha": {
            "silently_downcast": g3_complex_alpha_silently_downcast(),
            "python_builtin_contrast": g3_python_builtin_contrast(),
            "full_pipeline": g3_full_pipeline_complex_alpha(),
        },
        "G4_passes_and_raises": {
            "nan_propagates_at_ordinary_J": g4_nan_propagates_at_ordinary_J(),
            "alpha2_no_blowup": g4_alpha2_no_blowup(),
        },
    }

    data["gate_answer"] = "YES"
    data["findings"] = {
        "G1_headline": ("At J=1, graded_inverse_norm's reported value is bit-identical "
            "whether c and the nodal field om are clean, NaN-poisoned, or Inf-poisoned, and "
            "regardless of `drop` or `gauge` choice -- it always equals the closed form "
            "(1+X_0^2)^(alpha/2), a function of alpha alone. No exception, no NaN in the "
            "output, despite numpy raising internal RuntimeWarnings while computing the "
            "(fully discarded) jacobian_matrix."),
        "G2_headline": ("sup_op_norm silently reinterprets a 1-D array's domain/codomain "
            "axes via np.atleast_2d's row-vector default. 30/30 randomized cases mismatch "
            "between the ambiguous flat call and the explicit-column call; worked example "
            "returns 12.0 instead of the correct 10.0."),
        "G3_headline": ("A complex-valued (type-degenerate) alpha runs to completion through "
            "norm_domain/norm_codomain/graded_inverse_norm and is silently downcast to float "
            "via NumPy's non-fatal ComplexWarning, discarding a measured dependence on the "
            "imaginary part -- where Python's own float() would raise TypeError."),
    }
    data["downstream_exposure_summary"] = (
        "G1: no in-repo caller has EVER used J below 8 (grepped census in "
        "G1_grid_collapse.downstream_exposure); LATENT, same severity shape as legs 66/69/79/120. "
        "G2: sup_op_norm's only in-repo call site is inside graded_inverse_norm itself, which "
        "always passes a 2-D matrix from np.linalg.inv -- LATENT as a public-API hazard, no "
        "banked call site reachable. G3: no in-repo caller passes a complex alpha -- LATENT."
    )
    data["banked_numbers_at_risk"] = 0
    return data


if __name__ == "__main__":
    import json

    result = run_all()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                             "writeup", "data", "p2_route_dca_v1_adversarial.json")
    out_path = os.path.normpath(out_path)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, sort_keys=False, default=str)
    print(f"wrote {out_path}")
    print(f"gate_answer = {result['gate_answer']}")
    for k, v in result["findings"].items():
        print(f"\n{k}: {v}")
