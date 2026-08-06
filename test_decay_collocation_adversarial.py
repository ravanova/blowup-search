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

**REPAIRED AT LEG 151 (Route-DCR). ALL SEVEN PINS ARE NOW INVERTED.**  Leg 115's territory was
read-only on `solver/`, so it pinned the defective behaviour rather than fixing it silently
(legs 66/120's precedent) and stated beside each pin what the CORRECT behaviour would be.  Leg
151 landed the guards in `solver/decay_collocation.py`, and every `PIN:` check below was
rewritten IN THE SAME COMMIT to assert the corrected behaviour instead -- each one now marked
`INVERTED PIN (leg 151):`, carrying leg 115's original measured magnitude verbatim in its
docstring so the pre-repair number stays auditable from this file.  The eight CONTROL/PASS
checks are unchanged and must keep holding; they are what proves the guards did not overreach.

ONE CORRECTION LEG 151 MADE TO LEG 115'S OWN PRESCRIPTION.  Leg 115's journal prescribed a raise
"when `rows` is empty (i.e. `J <= 1`)".  Measured at `J = 1` over exactly the five `drop` values
`check_J1_ignores_drop_and_gauge` pinned -- `0, 1, -1, 5, 100` -- `rows` is empty for ONE of
them and has length 1 for the other four, while all five returned the identical
`1.681792830507429`.  The mechanism is the assignment target `M[1:, :]`, shape `(0, 1)` at
`J = 1`, into which NumPy broadcasts a `(1, 1)` right-hand side silently.  The guard that landed
is therefore the shape invariant `len(rows) == J - 1 >= 1`, not an emptiness test.

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
complex `alpha`.  All three findings were LATENT under the repository's current usage, exactly
the severity shape of legs 66, 69, 79 and 120 -- which is what made leg 151's repair licensable
as a measured no-op: the guards fire on ZERO shipped configurations, and every clean value is
bit-identical to the pre-repair module (`experiments/p2_route_dcr_v1_repair.py`,
`writeup/data/p2_route_dcr_v1_repair.json`).

Test convention (repo-wide): self-running script, also pytest-discoverable.
    .venv/bin/python test_decay_collocation_adversarial.py
"""

import warnings

import numpy as np

from solver.decay_collocation import (
    C_ANCHOR,
    Collocation,
    DecayCollocationDomainError,
    gauged_jacobian,
    graded_inverse_norm,
    sup_op_norm,
)

# Leg 115's measured pre-repair values, kept as literals so the inverted pins can assert that
# the repaired module NO LONGER produces them.  Sourced from
# writeup/data/p2_route_dca_v1_adversarial.json and leg 115's journal.
PRE_REPAIR_J1_VALUE = 1.681792830507429      # == 2 ** (1.5 / 2), a function of alpha ALONE
PRE_REPAIR_G2_FLAT = 12.0                    # the axis-swapped reading
PRE_REPAIR_G2_COLUMN = 10.0                  # the reading the caller intended

SEED = 20260806
POISONS = (("nan", float("nan")), ("+inf", float("inf")), ("-inf", -float("inf")))


# =========================================================================
# G1 -- grid-size collapse
# =========================================================================

def check_rows_retained_hits_zero_at_J1():
    """INVERTED PIN (leg 151), G1 mechanism. The row count `gauged_jacobian` retains for the
    actual differential operator is J - 1, which hits EXACTLY ZERO at J = 1.

    LEG 115 MEASURED (pre-repair): J = 1 retained 0 collocation rows and `gauged_jacobian`
    returned a gauge-only system without complaint. NOW: J = 1 raises
    DecayCollocationDomainError; J >= 2 is untouched and still retains exactly J - 1.
    """
    out = {}
    try:
        gauged_jacobian(Collocation(1), Collocation(1).anchor(), C_ANCHOR, drop=0)
        raise AssertionError("REGRESSION: J=1 must raise DecayCollocationDomainError")
    except DecayCollocationDomainError as e:
        out["J1_raises"] = True
        assert "J >= 2" in str(e), str(e)
    for J in range(2, 6):
        col = Collocation(J)
        _, rows = gauged_jacobian(col, col.anchor(), C_ANCHOR, drop=0)
        out[f"J{J}"] = len(rows)
        assert len(rows) == J - 1, (J, len(rows))
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
    n_raised = 0
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for c in c_values:
                try:
                    v = graded_inverse_norm(col, alpha, c=c)[0]
                except DecayCollocationDomainError:
                    n_raised += 1
                    continue
                raise AssertionError(
                    "REGRESSION: graded_inverse_norm(Collocation(1), %r, c=%r) returned %r "
                    "instead of raising. Pre-repair this returned %r for EVERY c in this "
                    "list, including nan/inf." % (alpha, c, v, PRE_REPAIR_J1_VALUE)
                )
    assert n_raised == len(c_values), (n_raised, len(c_values))
    return {"n_c_values": len(c_values), "n_raised": n_raised,
            "pre_repair_identical_value": PRE_REPAIR_J1_VALUE,
            "pre_repair_closed_form": 2.0 ** (alpha / 2.0)}


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
    out = {"cases": 0, "raised": 0}
    # The CLEAN J=1 call is refused too -- the collapse was never about the poison, it was
    # about the row count, so the guard is on the grid and not on the values.
    try:
        _pipeline(col, col.anchor(), alpha, C_ANCHOR)
        raise AssertionError("REGRESSION: the clean J=1 pipeline must raise")
    except DecayCollocationDomainError:
        out["clean_raises"] = True
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with np.errstate(all="ignore"):
            for tag, p in POISONS:
                out["cases"] += 1
                try:
                    v = _pipeline(col, np.array([p]), alpha, p)
                except DecayCollocationDomainError:
                    out["raised"] += 1
                    continue
                raise AssertionError(
                    "REGRESSION: om=%s returned %r instead of raising; pre-repair every "
                    "poison returned the clean %r." % (tag, v, PRE_REPAIR_J1_VALUE)
                )
    assert out["raised"] == out["cases"] == 3, out
    return out


def check_J1_ignores_drop_and_gauge():
    """INVERTED PIN (leg 151), G1 -- AND THE CHECK THAT DECIDED THE REPAIR'S PREDICATE.

    LEG 115 MEASURED (pre-repair): every `drop` in {0, 1, -1, 5, 100} and both gauges returned
    the identical 1.681792830507429 at J = 1.

    THE PREDICATE THIS CHECK RULED OUT. Leg 115's journal prescribed raising "when `rows` is
    empty (i.e. J <= 1)". But `rows = [j for j in range(J) if j != drop]` is empty at J = 1 for
    `drop = 0` ONLY; for `drop` in {1, -1, 5, 100} it is `[0]`, length 1 -- non-empty -- and all
    five collapsed identically anyway, because `M[1:, :]` has shape (0, 1) and NumPy broadcasts
    a (1, 1) right-hand side into it silently. An emptiness test would have repaired 1 of these
    5 cases. The landed guard is the shape invariant `len(rows) == J - 1 >= 1`, and the clause
    that catches each case is asserted separately below so neither can be dropped unnoticed.
    """
    col = Collocation(1)
    alpha = 1.5
    out = {"drop_values_tested": 0, "gauge_values_tested": 0,
           "caught_by_J_clause": 0, "would_be_missed_by_emptiness_predicate": 0}
    for drop in (0, 1, -1, 5, 100):
        rows_pre = [j for j in range(1) if j != drop]      # what the pre-repair code computed
        if len(rows_pre) != 0:
            out["would_be_missed_by_emptiness_predicate"] += 1
        try:
            graded_inverse_norm(col, alpha, drop=drop)
            raise AssertionError("REGRESSION: J=1 drop=%r must raise" % (drop,))
        except DecayCollocationDomainError:
            out["drop_values_tested"] += 1
            out["caught_by_J_clause"] += 1
    for gauge in ("origin", "a0"):
        try:
            graded_inverse_norm(col, alpha, gauge=gauge)
            raise AssertionError("REGRESSION: J=1 gauge=%r must raise" % (gauge,))
        except DecayCollocationDomainError:
            out["gauge_values_tested"] += 1
    assert out["would_be_missed_by_emptiness_predicate"] == 4, out
    assert out["drop_values_tested"] == 5 and out["gauge_values_tested"] == 2, out

    # The SECOND clause, isolated at an ordinary grid size where the J clause cannot fire:
    # an out-of-range `drop` must be refused on its own, by name.
    col8 = Collocation(8)
    for drop in (-1, 8, 100, 1.0, None):
        try:
            gauged_jacobian(col8, col8.anchor(), C_ANCHOR, drop=drop)
            raise AssertionError("REGRESSION: J=8 drop=%r must raise" % (drop,))
        except DecayCollocationDomainError:
            out["drop_clause_isolated"] = out.get("drop_clause_isolated", 0) + 1
    assert out["drop_clause_isolated"] == 5, out
    out["pre_repair_identical_value"] = PRE_REPAIR_J1_VALUE
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
    try:
        flat_result = sup_op_norm(A_flat, w_dom, w_cod)
        raise AssertionError(
            "REGRESSION: the ambiguous flat array must raise, got %r (pre-repair: %r)"
            % (flat_result, PRE_REPAIR_G2_FLAT)
        )
    except DecayCollocationDomainError as e:
        assert "(3, 1)" in str(e), str(e)
    # The UNAMBIGUOUS spelling of the same intent still works, and still gives the value the
    # caller meant -- the guard refuses the ambiguity, it does not refuse the computation.
    correct_column = sup_op_norm(A_flat.reshape(3, 1), w_dom, w_cod)
    assert correct_column == PRE_REPAIR_G2_COLUMN, correct_column
    return {"flat_raises": True, "correct_column_result": correct_column,
            "pre_repair_flat_result": PRE_REPAIR_G2_FLAT}


def check_sup_op_norm_1d_ambiguity_battery():
    """PIN (G2): the mismatch rate over a randomized battery of shapes -- not a cherry-picked
    single case. Every case with n > 1 domain slots and 1 codomain slot mismatches, because the
    axis swap is deterministic given mismatched lengths."""
    rng = np.random.default_rng(SEED)
    n_cases = 30
    raised = 0
    for _ in range(n_cases):
        n = int(rng.integers(2, 7))
        A_flat = rng.uniform(0.1, 20.0, size=n)
        w_dom_n = np.ones(n)
        w_cod_1 = np.ones(1)
        try:
            flat = sup_op_norm(A_flat, w_dom_n, w_cod_1)
        except DecayCollocationDomainError:
            raised += 1
            # and the unambiguous spelling of the same array still computes
            column = sup_op_norm(A_flat.reshape(n, 1), w_dom_n, w_cod_1)
            assert column == float(np.max(A_flat)), (column, A_flat)
            continue
        raise AssertionError("REGRESSION: ambiguous flat case returned %r" % (flat,))
    assert raised == n_cases, (raised, n_cases)
    return {"n_cases": n_cases, "n_raised": raised,
            "pre_repair_n_mismatches": n_cases}


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
    """INVERTED PIN (leg 151), G3. A non-real alpha is now REJECTED by norm_domain and
    norm_codomain rather than silently truncated by float() under NumPy's ComplexWarning.

    LEG 115 MEASURED (pre-repair): 4 of 6 complex alphas returned a value silently differing
    from the real-part-only computation, with no exception raised on any of the 6.
    """
    col = Collocation(16)
    om = col.anchor()
    # Leg 115 probed six; the four with an imaginary part large enough to move float64 are
    # the ones it counted as silently divergent. The guard is on the TYPE, not the magnitude,
    # so all six -- including the two leg 115 honestly recorded as non-divergent -- are now
    # refused, which is a strictly wider refusal than the finding required.
    complex_alphas = [1.5 + 0.1j, 1.5 + 1.0j, 0.0 + 1.0j, -1.0 + 2.0j,
                      1.0 + 0.0j, 1.5 + 1e-10j]
    out = {"cases": 0, "raised": 0, "pre_repair_n_silently_diverging": 4}
    for a in complex_alphas:
        out["cases"] += 1
        for fn in (col.norm_domain, col.norm_codomain):
            try:
                v = fn(om, a)
            except DecayCollocationDomainError:
                continue
            raise AssertionError(
                "REGRESSION: %s returned %r for complex alpha %r instead of raising"
                % (fn.__name__, v, a)
            )
        out["raised"] += 1
    assert out["raised"] == out["cases"] == 6, out
    # CONTROL inside the inverted pin: every REAL spelling of alpha still works untouched --
    # Python float, Python int, NumPy scalar -- so the guard tests realness, not type identity.
    for a in (1.5, 2, np.float64(1.5), np.int64(2)):
        assert np.isfinite(col.norm_domain(om, a)), a
    out["real_alphas_still_accepted"] = 4
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
    """INVERTED PIN (leg 151), G3 end to end. The hazard reached the leg's own headline
    function; the guard now stops it there too.

    LEG 115 MEASURED (pre-repair): graded_inverse_norm(Collocation(16), 1.5+0.3j) returned a
    plain finite float with no exception and no signal that alpha was not the real exponent.
    """
    col = Collocation(16)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            val, A, M = graded_inverse_norm(col, 1.5 + 0.3j)
        except DecayCollocationDomainError:
            # and the real spelling of the same call still returns its ordinary finite value
            val_real = graded_inverse_norm(col, 1.5)[0]
            assert np.isfinite(val_real) and val_real > 0.0, val_real
            return {"complex_alpha_raises": True, "real_alpha_still_returns": val_real}
    raise AssertionError(
        "REGRESSION: graded_inverse_norm accepted a complex alpha, returned %r" % (val,))


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
    print("NOTE: REPAIRED at leg 151. G1/G2/G3's 7 pins are INVERTED -- they now assert the")
    print("guards in solver/decay_collocation.py, and the 8 CONTROL/PASS checks are unchanged.")
    print("Pre-repair magnitudes: writeup/data/p2_route_dca_v1_adversarial.json (leg 115).")
    print("Repair evidence:       writeup/data/p2_route_dcr_v1_repair.json (leg 151).")
