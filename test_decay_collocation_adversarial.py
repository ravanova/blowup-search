"""Adversarial battery for solver/decay_collocation.py -- the nodal spectral core under the
collocation lane (leg 115, Route-DCA).

WHY THIS FILE EXISTS, ALONGSIDE `test_decay_collocation.py`.  The dedicated file asks the
module's helpers a question they can fail on their own terms: manufactured solutions and
refinement convergence, on VALID, well-resolved input.  What it does not do -- and was never
meant to do -- is feed the module DEGENERATE grid sizes or POISONED nodal values/parameters and
ask whether a wrong answer comes back silently.  Leg 115 does that.

THE GATE (DIRECTION.md, leg 115), answered YES:

    Under an adversarial battery of degenerate or poisoned inputs, does
    solver/decay_collocation.py ever silently return a wrong value rather than propagating or
    flagging the invalid input?

READ THIS BEFORE CHANGING ANYTHING HERE.  Several checks below PIN CURRENT, DEFECTIVE
BEHAVIOUR.  That is deliberate, and it is legs 66/120's precedent: a leg whose territory is
read-only on `solver/` reports defects and pins them rather than fixing them silently, so the
defect cannot drift unnoticed and so the repair has an exact target.  **Every such check is
marked `PIN:` in its docstring and states what the CORRECT behaviour would be.  When the repair
lands, these checks WILL START FAILING -- that is the intended signal, not a regression.**
Update the pin then, in the same commit as the repair.

THE THREE FINDINGS PINNED HERE (magnitudes, measured by
experiments/p2_route_dca_v1_adversarial.py, banked in
writeup/data/p2_route_dca_v1_adversarial.json):

  G1  GRID-SIZE COLLAPSE.  `gauged_jacobian` implements the "classical row deletion" boundary-
      bordering technique (Driscoll & Hale, IMA J. Numer. Anal. 36 (2016) 108-132), whose own
      abstract flags it as carrying "ambiguities... outside of two-point scalar boundary-value
      problems".  The module's own docstring states TWO scalar gauge conditions are required;
      this repository's own TECHNICAL_P2_ROUTED.md sec 4 independently measures the same count.
      At J = 1 there is exactly one row available and one gauge condition consumes it, leaving
      ZERO rows for the actual differential operator. MEASURED: `graded_inverse_norm(Collocation
      (1), alpha, c=c)` is bit-identical across c in {0, 0.5, 1, 100, -50, 1e6, nan, +inf, -inf}
      and across a NaN/Inf-poisoned nodal field `om`, and across every `drop` value -- always
      exactly `(1+X_0^2)^(alpha/2)`, a function of alpha alone.  No exception; no NaN in the
      output; numpy raises internal RuntimeWarnings while computing the (fully discarded)
      `jacobian_matrix`, and those warnings never reach the return value.

  G2  `sup_op_norm` SHAPE AMBIGUITY.  NumPy's own documentation: `atleast_2d` on a 1-D array of
      shape (N,) always returns shape (1, N) -- a row, never a column.  `sup_op_norm` never
      checks that a 1-D caller's array matches its own stated domain/codomain axis convention
      before calling `atleast_2d`.  MEASURED: 30/30 randomized cases where a 1-D array intended
      as an (n, 1) column mismatches the same array's explicit-column interpretation; a worked
      example returns 12.0 in place of the correct 10.0.

  G3  TYPE-DEGENERATE `alpha`.  NumPy's own documentation: casting complex to a real dtype
      "discards the imaginary part" and raises `ComplexWarning`, a non-fatal `Warning`
      subclass -- looser than Python's own built-in `float()`, which raises `TypeError`
      unconditionally on a complex argument.  `norm_domain`/`norm_codomain` end in
      `float(np.max(...))`.  MEASURED: 4/6 complex-valued alphas (nonzero imaginary part large
      enough to matter) return a value that silently differs from the real-part-only
      computation, with no exception and no signal in the return value.

SEVERITY, MEASURED, NOT ASSERTED: no in-repo caller has EVER used J below 8 for
`Collocation`/`graded_inverse_norm` (census in the runner's `g1_downstream_exposure`); the
`sup_op_norm` shape ambiguity has exactly one in-repo call site (inside `graded_inverse_norm`
itself), which always passes a 2-D matrix from `np.linalg.inv`; no in-repo caller passes a
complex `alpha`.  All three findings are LATENT under the repository's current usage, exactly
the severity shape of legs 66, 69, 79 and 120.  Leg 115's pre-committed yes-branch is "escalate,
do not patch", and this leg edits no solver file.

Test convention (repo-wide): self-running script, also pytest-discoverable.
    .venv/bin/python test_decay_collocation_adversarial.py
"""

import warnings

import numpy as np

from solver.decay_collocation import (
    C_ANCHOR,
    Collocation,
    gauged_jacobian,
    graded_inverse_norm,
    sup_op_norm,
)

SEED = 20260806
POISONS = (("nan", float("nan")), ("+inf", float("inf")), ("-inf", -float("inf")))


# =========================================================================
# G1 -- grid-size collapse
# =========================================================================

def check_rows_retained_hits_zero_at_J1():
    """The row count `gauged_jacobian` retains for the actual differential operator, J - 1 for
    J >= 1 -- hits EXACTLY ZERO at J = 1. This is the mechanism behind every other G1 check."""
    out = {}
    for J in range(1, 6):
        col = Collocation(J)
        _, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR, drop=0)
        out[f"J{J}"] = len(rows)
        assert len(rows) == J - 1, (J, len(rows))
    assert out["J1"] == 0, "PIN G1: J=1 should retain zero collocation rows"
    return out


def check_J1_ignores_poisoned_c():
    """PIN (G1): at J = 1, graded_inverse_norm is bit-identical for ANY c, including NaN/Inf.

    CORRECT BEHAVIOUR: a poisoned c should either raise (the system is degenerate and should
    say so) or propagate to a non-finite result, as it does at every J >= 2 (see the CONTROL
    below). Pinned as: silently ignored, returns the same finite number every time.
    """
    col = Collocation(1)
    alpha = 1.5
    c_values = [0.0, 0.5, 1.0, 100.0, -50.0, 1e6, float("nan"), float("inf"), -float("inf")]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            vals = [graded_inverse_norm(col, alpha, c=c)[0] for c in c_values]
    assert len(set(vals)) == 1, (
        f"PIN G1: expected all {len(c_values)} values of c (including nan/inf) to give the "
        f"IDENTICAL result at J=1, got {set(vals)}. If gauged_jacobian has been repaired to "
        "raise or propagate at J=1, this assertion SHOULD fail -- update the pin."
    )
    predicted = 2.0 ** (alpha / 2.0)
    assert abs(vals[0] - predicted) < 1e-13, (vals[0], predicted)
    assert np.isfinite(vals[0]), "PIN G1: the nan/inf-c result must currently be FINITE"
    return {"n_c_values": len(c_values), "all_identical": True, "value": vals[0],
            "predicted_closed_form": predicted}


def check_J1_ignores_poisoned_om():
    """PIN (G1): the same collapse for a NaN/Inf-poisoned NODAL FIELD, not just c.

    graded_inverse_norm computes om internally, so this reconstructs its exact pipeline with a
    poisoned om substituted -- same arithmetic, same call sequence, only the input replaced.
    """
    def _pipeline(col, om, alpha, c):
        M, rows = gauged_jacobian(col, om, c, gauge="origin", drop=0)
        A = np.linalg.inv(M)
        w_dom = col.w_domain(alpha)
        w_cod = np.empty(col.J)
        w_cod[0] = 1.0
        w_cod[1:] = col.w_codomain(alpha)[rows]
        return sup_op_norm(A, w_dom, w_cod)

    col = Collocation(1)
    alpha = 1.5
    v_clean = _pipeline(col, col.anchor(), alpha, C_ANCHOR)
    out = {"cases": 0, "identical_to_clean": 0}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for tag, p in POISONS:
                v = _pipeline(col, np.array([p]), alpha, p)
                out["cases"] += 1
                out["identical_to_clean"] += int(v == v_clean)
                assert v == v_clean, (
                    f"PIN G1 om={tag}: expected identical to clean ({v_clean}), got {v}. If "
                    "the collapse has been repaired this assertion SHOULD fail."
                )
                assert np.isfinite(v), (tag, v)
    assert out["identical_to_clean"] == out["cases"] == 3, out
    return out


def check_J1_ignores_drop_and_gauge():
    """PIN (G1): the collapse is insensitive to `drop` (any value, in- or out-of-range) and to
    `gauge` choice -- both routes to the same empty (0, J) assignment slot."""
    col = Collocation(1)
    alpha = 1.5
    v0, _, _ = graded_inverse_norm(col, alpha, drop=0)
    out = {"drop_values_tested": 0, "gauge_values_tested": 0}
    for drop in (0, 1, -1, 5, 100):
        v, _, _ = graded_inverse_norm(col, alpha, drop=drop)
        assert v == v0, ("PIN G1", drop, v, v0)
        out["drop_values_tested"] += 1
    for gauge in ("origin", "a0"):
        v, _, _ = graded_inverse_norm(col, alpha, gauge=gauge)
        assert v == v0, ("PIN G1", gauge, v, v0)
        out["gauge_values_tested"] += 1
    return out


def check_J_geq_2_control_c_propagates():
    """CONTROL for G1 (a PASS): at J >= 2, a NaN- or Inf-poisoned c DOES propagate to a
    non-finite result, and varying c across ordinary values DOES change the answer. This is
    what makes G1 a statement about J = 1 specifically, not about small J in general."""
    out = {"J_tested": [], "all_sensitive": True, "all_nan_propagates": True}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for J in (2, 3, 4, 8, 16):
                col = Collocation(J)
                v1, _, _ = graded_inverse_norm(col, 1.5, c=0.5)
                v2, _, _ = graded_inverse_norm(col, 1.5, c=100.0)
                v_nan, _, _ = graded_inverse_norm(col, 1.5, c=float("nan"))
                sensitive = (v1 != v2)
                propagates = bool(np.isnan(v_nan))
                out["J_tested"].append(J)
                out["all_sensitive"] = out["all_sensitive"] and sensitive
                out["all_nan_propagates"] = out["all_nan_propagates"] and propagates
                assert sensitive, ("CONTROL FAILED", J, v1, v2)
                assert propagates, ("CONTROL FAILED", J, v_nan)
    return out


def check_degenerate_J_raises():
    """PASS: J <= 0 raises (ZeroDivisionError at J=0, ValueError at J<0) -- the module does
    refuse SOME degenerate grid sizes, just not J = 1."""
    out = {}
    try:
        Collocation(0)
        raise AssertionError("expected ZeroDivisionError at J=0")
    except ZeroDivisionError:
        out["J0_raises"] = True
    for J in (-1, -5):
        try:
            Collocation(J)
            raise AssertionError(f"expected ValueError at J={J}")
        except ValueError:
            out[f"J{J}_raises"] = True
    return out


def check_drop_out_of_range_raises_at_ordinary_J():
    """PASS: at an ordinary grid size (J = 8), an out-of-range `drop` raises ValueError (a
    shape-mismatch), and an invalid `gauge` string raises KeyError. The J=1 collapse is a
    distinct failure mode from these -- it does NOT raise where these do."""
    col = Collocation(8)
    out = {}
    for drop in (100, -1, 8):
        try:
            gauged_jacobian(col, col.anchor(), C_ANCHOR, drop=drop)
            raise AssertionError(f"expected ValueError at drop={drop}")
        except ValueError:
            out[f"drop{drop}_raises"] = True
    try:
        gauged_jacobian(col, col.anchor(), C_ANCHOR, gauge="bogus")
        raise AssertionError("expected KeyError at gauge='bogus'")
    except KeyError:
        out["gauge_bogus_raises"] = True
    return out


# =========================================================================
# G2 -- sup_op_norm shape ambiguity
# =========================================================================

def check_sup_op_norm_1d_shape_ambiguity():
    """PIN (G2): a 1-D array intended as an (n, 1) column operator is silently reinterpreted
    as a (1, n) row by `np.atleast_2d`, swapping the domain/codomain axes.

    CORRECT BEHAVIOUR: `sup_op_norm` should validate that a 1-D `A`'s length matches exactly
    one of {len(w_dom), len(w_cod)} unambiguously (and raise if it matches both or neither, or
    if w_dom/w_cod disagree with a 2-D A's shape), or simply require 2-D input outright.
    Pinned as: silently accepted, axes swapped whenever len(w_dom) != len(w_cod).
    """
    A_flat = np.array([10.0, 1.0, 1.0])
    w_dom = np.array([1.0, 1.0, 1.0])
    w_cod = np.array([1.0])
    flat_result = sup_op_norm(A_flat, w_dom, w_cod)
    correct_column = sup_op_norm(A_flat.reshape(3, 1), w_dom, w_cod)
    assert correct_column == 10.0, correct_column
    assert flat_result == 12.0, (
        f"PIN G2: expected the pinned mis-interpretation (12.0), got {flat_result}. If "
        "sup_op_norm has been repaired to validate orientation, this assertion SHOULD fail."
    )
    assert flat_result != correct_column, "PIN G2: expected a mismatch"
    return {"flat_result": flat_result, "correct_column_result": correct_column}


def check_sup_op_norm_1d_ambiguity_battery():
    """PIN (G2): the mismatch rate over a randomized battery of shapes -- not a cherry-picked
    single case. Every case with n > 1 domain slots and 1 codomain slot mismatches, because the
    axis swap is deterministic given mismatched lengths."""
    rng = np.random.default_rng(SEED)
    n_cases = 30
    mismatches = 0
    for _ in range(n_cases):
        n = int(rng.integers(2, 7))
        A_flat = rng.uniform(0.1, 20.0, size=n)
        w_dom_n = np.ones(n)
        w_cod_1 = np.ones(1)
        flat = sup_op_norm(A_flat, w_dom_n, w_cod_1)
        column = sup_op_norm(A_flat.reshape(n, 1), w_dom_n, w_cod_1)
        mismatches += int(flat != column)
    assert mismatches == n_cases, (
        f"PIN G2: expected all {n_cases} cases to mismatch, got {mismatches}. If sup_op_norm "
        "has been repaired, this assertion SHOULD fail -- update the pin."
    )
    return {"n_cases": n_cases, "n_mismatches": mismatches}


def check_sup_op_norm_2d_never_ambiguous():
    """CONTROL for G2 (a PASS): explicitly 2-D input -- exactly what `graded_inverse_norm`
    always passes internally, since `np.linalg.inv` always returns 2-D -- is never touched by
    the `atleast_2d` reshape, so this hazard has no live in-repo call site today."""
    rng = np.random.default_rng(SEED)
    for _ in range(10):
        n = int(rng.integers(2, 6))
        A2d = rng.uniform(0.1, 10.0, size=(n, n))
        w_dom = rng.uniform(0.5, 2.0, size=n)
        w_cod = rng.uniform(0.5, 2.0, size=n)
        v1 = sup_op_norm(A2d, w_dom, w_cod)
        v2 = sup_op_norm(np.atleast_2d(A2d), w_dom, w_cod)
        assert v1 == v2, "CONTROL FAILED: 2-D input should be unaffected by atleast_2d"
    return {"explicit_2d_is_never_ambiguous": True}


# =========================================================================
# G3 -- type-degenerate alpha
# =========================================================================

def check_complex_alpha_silently_downcast():
    """PIN (G3): a complex-valued alpha (invalid per the module's own docstring) runs to
    completion and returns an ordinary float, silently differing from the real-part-only
    answer, via NumPy's non-fatal ComplexWarning rather than an exception.

    CORRECT BEHAVIOUR: reject a non-real alpha (raise), or at minimum warn loudly enough that
    a caller notices. Pinned as: silent divergence, no exception ever raised.
    """
    col = Collocation(16)
    om = col.anchor()
    complex_alphas = [1.5 + 0.1j, 1.5 + 1.0j, 0.0 + 1.0j, -1.0 + 2.0j]
    out = {"cases": 0, "diverged_from_real_part": 0, "raised": 0}
    for a in complex_alphas:
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            v = col.norm_domain(om, a)
        v_real_only = col.norm_domain(om, a.real)
        out["cases"] += 1
        if v != v_real_only:
            out["diverged_from_real_part"] += 1
    assert out["diverged_from_real_part"] == out["cases"] == 4, (
        f"PIN G3: expected all {len(complex_alphas)} cases to silently diverge from the "
        f"real-part-only answer, got {out}. If norm_domain has been repaired to reject "
        "non-real alpha, this assertion SHOULD fail -- update the pin."
    )
    assert out["raised"] == 0, "PIN G3: expected no exception to be raised for complex alpha"
    return out


def check_python_builtin_float_refuses_complex():
    """CONTROL for G3 (a PASS, about the language not the module): Python's own float() DOES
    refuse a complex argument, which is exactly the asymmetry that makes NumPy's looser
    ComplexWarning-based silent downcast a real, citable gap rather than ordinary behaviour."""
    try:
        float(complex(1, 2))
        raise AssertionError("expected TypeError")
    except TypeError:
        pass
    return {"python_builtin_float_raises_TypeError": True}


def check_full_pipeline_complex_alpha_no_exception():
    """PIN (G3): the complex-alpha hazard reaches the leg's own headline function end to end
    with no exception."""
    col = Collocation(16)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        val, A, M = graded_inverse_norm(col, 1.5 + 0.3j)
    assert isinstance(val, float) and np.isfinite(val), (
        f"PIN G3: expected graded_inverse_norm to return a plain finite float for a complex "
        f"alpha with no exception, got {val!r}"
    )
    return {"result": val}


# =========================================================================
# THE PASSES -- recorded as loudly as the failures
# =========================================================================

def check_nan_propagates_at_ordinary_J():
    """PASS: at an ordinary grid size (J = 16), NaN/Inf poisoning of om or c PROPAGATES
    through residual, jacobian_matrix, norm_domain/codomain and graded_inverse_norm -- nothing
    here is absorbed. This is the behaviour map that makes G1's J = 1 finding a genuine
    boundary case rather than a description of the module's general behaviour."""
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
                v, _, _ = graded_inverse_norm(col, 1.5, c=p)
                for finite_check in (np.all(np.isfinite(r)), np.all(np.isfinite(Jm)),
                                     np.isfinite(nd), np.isfinite(v)):
                    out["cases"] += 1
                    out["propagated"] += int(not finite_check)
    assert out["propagated"] == out["cases"], out
    return out


def check_alpha2_no_blowup():
    """PASS: alpha = 2 -- the far-field MODEL operator's singular point (2/|alpha-2|, a
    property of a DIFFERENT, simpler operator per the module's own docstring) -- causes no
    blow-up or misbehaviour in the FULL operator this module actually discretizes."""
    col = Collocation(32)
    for a in (1.9999, 2.0, 2.0001):
        v, _, _ = graded_inverse_norm(col, a)
        assert np.isfinite(v), (a, v)
    return {"alpha_near_2_all_finite": True}


CHECKS = [
    check_rows_retained_hits_zero_at_J1,
    check_J1_ignores_poisoned_c,
    check_J1_ignores_poisoned_om,
    check_J1_ignores_drop_and_gauge,
    check_J_geq_2_control_c_propagates,
    check_degenerate_J_raises,
    check_drop_out_of_range_raises_at_ordinary_J,
    check_sup_op_norm_1d_shape_ambiguity,
    check_sup_op_norm_1d_ambiguity_battery,
    check_sup_op_norm_2d_never_ambiguous,
    check_complex_alpha_silently_downcast,
    check_python_builtin_float_refuses_complex,
    check_full_pipeline_complex_alpha_no_exception,
    check_nan_propagates_at_ordinary_J,
    check_alpha2_no_blowup,
]


def test_rows_retained_hits_zero_at_J1():
    check_rows_retained_hits_zero_at_J1()


def test_J1_ignores_poisoned_c():
    check_J1_ignores_poisoned_c()


def test_J1_ignores_poisoned_om():
    check_J1_ignores_poisoned_om()


def test_J1_ignores_drop_and_gauge():
    check_J1_ignores_drop_and_gauge()


def test_J_geq_2_control_c_propagates():
    check_J_geq_2_control_c_propagates()


def test_degenerate_J_raises():
    check_degenerate_J_raises()


def test_drop_out_of_range_raises_at_ordinary_J():
    check_drop_out_of_range_raises_at_ordinary_J()


def test_sup_op_norm_1d_shape_ambiguity():
    check_sup_op_norm_1d_shape_ambiguity()


def test_sup_op_norm_1d_ambiguity_battery():
    check_sup_op_norm_1d_ambiguity_battery()


def test_sup_op_norm_2d_never_ambiguous():
    check_sup_op_norm_2d_never_ambiguous()


def test_complex_alpha_silently_downcast():
    check_complex_alpha_silently_downcast()


def test_python_builtin_float_refuses_complex():
    check_python_builtin_float_refuses_complex()


def test_full_pipeline_complex_alpha_no_exception():
    check_full_pipeline_complex_alpha_no_exception()


def test_nan_propagates_at_ordinary_J():
    check_nan_propagates_at_ordinary_J()


def test_alpha2_no_blowup():
    check_alpha2_no_blowup()


if __name__ == "__main__":
    for fn in CHECKS:
        metrics = fn()
        head = ", ".join(f"{k}={v:.3g}" if isinstance(v, float) else f"{k}={v}"
                         for k, v in list(metrics.items())[:4])
        print(f"PASS {fn.__name__}: {head}")
    print(f"\nall decay_collocation ADVERSARIAL checks passed ({len(CHECKS)} checks)")
    print("NOTE: G1/G2/G3 PIN CURRENT DEFECTIVE BEHAVIOUR (see module docstring).")
    print("They are expected to FAIL once solver/decay_collocation.py is repaired -- that is")
    print("the intended signal. Banked magnitudes: writeup/data/p2_route_dca_v1_adversarial.json")
