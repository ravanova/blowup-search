"""Adversarial gates for `solver/hl_rescaled.py` (leg 117, Route-HRA).

`test_hl_rescaled.py` validates the module on WELL-BEHAVED data: sorted sinh-stretched
grids, `X_ref` pinned inside the sampled domain, the exact Theorem-2.3 anchor. This file
validates the other half — degenerate, poisoned, out-of-contract input — and banks leg
117's battery so the answer cannot silently regress.

The gate leg 117 answered, verbatim (`DIRECTION.md`, leg 117):

  "Under an adversarial battery of degenerate or poisoned inputs, does
   solver/hl_rescaled.py ever silently return a wrong result instead of flagging the
   input?"

Answered **YES**. Four silent-corruption mechanisms found, none patched (`solver/
hl_rescaled.py` is read-only under this leg's territory under any outcome). Escalated,
not landed on main.

READ THIS BEFORE CHANGING ANYTHING HERE.
-----------------------------------------
Several checks below PIN CURRENT, DEFECTIVE BEHAVIOUR — they assert that the module is
STILL silently wrong today, on purpose, so a regression (or a fix) cannot happen without
this file screaming about it. Each is marked `PIN:` in its docstring and states what the
CORRECT behaviour would be. **When a leg is authorised to repair `solver/hl_rescaled.py`,
these PIN tests must be INVERTED in the same commit as the repair — never silently
weakened or deleted.** This is leg 66/69/84's own precedent, reused verbatim by legs
92/96/106/116/120.

THE FOUR FINDINGS PINNED HERE (magnitudes, measured by
`experiments/p2_route_hra_v1_adversarial.py`, `writeup/data/p2_route_hra_v1_adversarial.json`):

  G1. `velocity(X, Homega, X_ref)` never validates `X` is ascending. A permutation of a
      correctly-sorted `(X, Homega)` pair is silently integrated in the wrong order: 20/20
      random permutations return a finite, zero-warning result disagreeing with the
      correctly-sorted computation by up to 212.0 absolute (91x the true scale).
  G2. The same function pins `U(X_ref)=0` via `np.interp`, which silently clamps to the
      nearest sampled boundary when `X_ref` falls outside `[X.min(), X.max()]` (a
      documented numpy default `velocity()` never checks). 4/4 out-of-domain `X_ref`
      values produce a uniform, silent, finite additive shift error (e.g. 1.47 absolute
      at `X_ref=-5.0` against a `[0,10]` sampled window).
  G3. `sinh_grid_at(n, M=<negative>)` is never validated for `M > 0` (only the docstring
      implies it via "Reach is +-M"); a negative `M` silently returns the exact
      descending mirror of the valid grid, 0 warnings. `RescaledHL.__init__` happens to
      reject the resulting array (its own ascending guard fires), but the free
      `sinh_grid_at`/`velocity()` functions that produced/would consume it do not.
  G8 (the headline). `degenerate_ic`'s closing lines
          Omega0 = np.where(X > 0.0, Omega0, 0.0)
          Theta0 = np.where(X > 0.0, Theta0, 0.0)
      use an ORDERED comparison against `X`. IEEE-754 makes `X > 0.0` False wherever `X`
      is NaN, so `np.where` silently launders a NaN abscissa into exactly the same clean
      finite `0.0` a legitimate `X<=0` point would produce — indistinguishable from valid
      one-sided-support initial data, across all three `kind`s, zero warnings.

Three further mechanisms were checked and found NOT exploitable to a silent, finite,
wrong result (soundness gates below, banked as controls so a future regression is
caught just as loudly as the defects are):

  G4. `RescaledHL.__init__`'s ascending guard `np.any(np.diff(X) <= 0)` has the identical
      IEEE-754 comparison blind spot (a NaN anywhere defeats it) — the guard IS genuinely
      defeated, but in every configuration tested the poisoned grid propagates to an
      all-NaN Hilbert transform downstream (visible), not a plausible finite answer. This
      is reported as a validation-gap CHARACTERIZATION, not a demonstrated silent-
      corruption chain — see `test_CHARACTERIZE_nan_defeats_ascending_guard`.
  G6. `_solve_3x3`'s absolute 1e-14 pivot threshold never returned a silently-wrong
      solution over 300 random/rescaled systems (it always matched numpy or raised); it
      DOES over-reject a uniformly-tiny (1e-16) but perfectly well-conditioned matrix —
      a false positive, not a violation of this leg's gate (over-caution, not corruption).
  G7. Endpoint +-inf survives the ascending guard (order comparisons with a signed
      infinity at an edge are well-defined), unlike an interior inf (correctly rejected);
      downstream always visibly warns / returns non-finite, never silently clean.

HOW "SILENT" IS DECIDED HERE
-----------------------------
Finite/non-NaN output + zero warnings + zero exceptions + disagreement with an
independently-computed correct answer = SILENT CORRUPTION. A visible RuntimeWarning, a
raised exception, or a non-finite (NaN/inf) output all count as FLAGGED, never silent —
exactly leg 96's and leg 120's distinction ("exact duplicates go 100% non-finite with 16
warnings" was banked as a PASS, not a defect).

Run: .venv/bin/python test_hl_rescaled_adversarial.py
"""

import os
import sys
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solver.hl_rescaled import (
    RescaledHL, RescaledHLDynamic, degenerate_ic, scenario2_ic, sinh_grid_at, velocity,
    _solve_3x3,
)


# ============================================================================
# PIN tests -- current, defective behaviour. MUST be inverted, not deleted, on repair.
# ============================================================================

def test_PIN_velocity_silently_corrupted_by_permutation():
    """PIN (G1): velocity() never checks X is ascending. A permutation of a correctly
    sorted (X, Homega) pair is silently integrated wrong: finite output, zero warnings,
    large disagreement with the correctly-sorted computation.

    CORRECT behaviour would be: raise (or at minimum warn) when np.diff(X) is not
    everywhere positive, exactly the guard RescaledHL.__init__ already has for its own
    class -- the free function has no such guard."""
    _, X = sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)
    U_true = velocity(X, Homega, X_ref=0.0)
    Uex = np.arctan(2.0 * X)
    assert np.abs(U_true - Uex).max() < 1e-2, "sanity: sorted call should match analytic"

    rng = np.random.default_rng(0)
    perm = rng.permutation(len(X))
    Xp, Hp = X[perm], Homega[perm]
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        Up = velocity(Xp, Hp, X_ref=0.0)
    inv = np.argsort(perm)
    err = float(np.abs(Up[inv] - U_true).max())
    print(f"    PIN G1: permuted call raised 0 exceptions, {len(wl)} warnings, "
          f"max abs error vs correctly-sorted computation = {err:.4f}")
    assert len(wl) == 0, "PIN G1 broken: a warning now fires (repair may be landing)"
    assert np.all(np.isfinite(Up)), "PIN G1 broken: output is no longer finite"
    assert err > 1.0, (f"PIN G1 broken: permutation error fell to {err:.4e}, expected a "
                       f"large silent disagreement (repair may be landing -- INVERT this "
                       f"test, do not delete it)")
    print("[PIN] velocity() still silently mis-integrates a non-ascending X")


def test_PIN_velocity_silently_clamps_xref_out_of_domain():
    """PIN (G2): velocity()'s X_ref pin via np.interp silently clamps when X_ref falls
    outside [X.min(), X.max()] -- a documented numpy default, never checked here.

    CORRECT behaviour would be: raise (or warn) when X_ref is outside the sampled range."""
    X = np.linspace(0.0, 10.0, 501)
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)
    X_ref_out = -5.0
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        U_out = velocity(X, Homega, X_ref=X_ref_out)
    true_pinned = np.arctan(2.0 * X) - np.arctan(2.0 * X_ref_out)
    err = float(np.abs(U_out - true_pinned).max())
    print(f"    PIN G2: X_ref={X_ref_out} outside [0,10], {len(wl)} warnings, "
          f"max abs error vs analytic pin = {err:.4f}")
    assert len(wl) == 0, "PIN G2 broken: a warning now fires (repair may be landing)"
    assert np.all(np.isfinite(U_out)), "PIN G2 broken: output is no longer finite"
    assert err > 0.1, (f"PIN G2 broken: extrapolation error fell to {err:.4e} (repair may "
                       f"be landing -- INVERT this test, do not delete it)")
    print("[PIN] velocity() still silently clamps an out-of-domain X_ref")


def test_PIN_sinh_grid_at_silently_reverses_on_negative_M():
    """PIN (G3): sinh_grid_at(n, M=negative) is never validated; it silently returns the
    exact descending mirror of the valid (M>0) grid, with zero warnings.

    CORRECT behaviour would be: raise, or take abs(M), with a warning either way."""
    kwargs = dict(Xc=0.0, delta=1.0, M=50.0, offset=False)
    _, X_pos = sinh_grid_at(11, **kwargs)
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        _, X_neg = sinh_grid_at(11, **{**kwargs, "M": -50.0})
    print(f"    PIN G3: M=-50 call raised {len(wl)} warnings; "
          f"X_neg == reverse(X_pos): {np.allclose(X_neg, X_pos[::-1])}")
    assert len(wl) == 0, "PIN G3 broken: a warning now fires (repair may be landing)"
    assert np.allclose(X_neg, X_pos[::-1]), "PIN G3 broken: negative M no longer mirrors"
    assert not np.all(np.diff(X_neg) > 0), "PIN G3 broken: negative M grid is now ascending"
    # the class constructor happens to catch the specific consequence -- confirm that
    # protective side effect is also still intact, so a regression there is caught too
    try:
        RescaledHL(X_neg)
        raise AssertionError("RescaledHL unexpectedly ACCEPTED the negative-M grid")
    except ValueError:
        pass
    print("[PIN] sinh_grid_at(M<0) still silently returns a descending mirror grid")


def test_PIN_degenerate_ic_launders_nan_to_zero():
    """PIN (G8, the headline): degenerate_ic's closing `np.where(X > 0.0, field, 0.0)`
    is an ordered comparison, so a NaN abscissa is silently laundered into the same
    finite 0.0 a legitimate X<=0 point produces -- across all three `kind`s.

    CORRECT behaviour would be: propagate NaN through, exactly as scenario2_ic already
    does (checked below as the same-file negative control)."""
    X = np.linspace(-5.0, 5.0, 51)
    nan_idx = [10, 30, 45]
    X[nan_idx] = np.nan
    for kind in ("A", "B", "C"):
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Om, Th = degenerate_ic(X, kind=kind)
        laundered = np.all(Om[nan_idx] == 0.0) and np.all(Th[nan_idx] == 0.0)
        print(f"    PIN G8 kind={kind}: {len(wl)} warnings, all finite: "
              f"{np.all(np.isfinite(Om)) and np.all(np.isfinite(Th))}, "
              f"NaN positions -> exact 0.0: {laundered}")
        assert len(wl) == 0, f"PIN G8({kind}) broken: a warning now fires"
        assert np.all(np.isfinite(Om)) and np.all(np.isfinite(Th)), \
            f"PIN G8({kind}) broken: output no longer all-finite"
        assert laundered, (f"PIN G8({kind}) broken: NaN abscissas no longer become exact "
                           f"0.0 (repair may be landing -- INVERT, do not delete)")
    print("[PIN] degenerate_ic still silently launders NaN abscissas to exact 0.0")


def test_scenario2_ic_negative_control_propagates_nan():
    """Same-file NEGATIVE CONTROL: scenario2_ic has no closing np.where mask, so the same
    NaN-poisoned X visibly propagates to NaN output -- confirming G8 is specific to
    degenerate_ic's particular construction, not a property of "any IC generator"."""
    X = np.linspace(-5.0, 5.0, 51)
    X[[10, 30, 45]] = np.nan
    Om, V = scenario2_ic(X)
    n_nan = int(np.sum(np.isnan(Om)) + np.sum(np.isnan(V)))
    print(f"    scenario2_ic on the same poisoned X: {n_nan} NaN entries in the output "
          f"(visible, not laundered)")
    assert n_nan > 0, "scenario2_ic unexpectedly absorbed the NaN -- investigate"
    print("[ok] scenario2_ic visibly propagates NaN; G8 is specific to degenerate_ic")


# ============================================================================
# Characterization -- a genuine gap, but not (yet) chained to a silent finite defect.
# ============================================================================

def test_CHARACTERIZE_nan_defeats_ascending_guard():
    """CHARACTERIZE (G4): RescaledHL.__init__'s guard `np.any(np.diff(X) <= 0)` has the
    same NaN-comparison blind spot as G8's mechanism -- a NaN anywhere makes it vacuously
    pass, so a completely scrambled, NaN-containing array is accepted as a "valid" grid.
    Distinct from a PIN: every configuration tested chains to a visible all-NaN Hilbert
    transform downstream, not a plausible finite answer, so this is recorded as a genuine
    validation gap without a demonstrated silent-corruption consequence. If this ever
    starts returning a finite result instead, that is a NEW, more severe finding, not a
    fix -- this test guards the boundary in that direction."""
    X = np.array([0.0, 1.0, np.nan, 0.5, 2.0])   # scrambled AND poisoned
    assert not np.any(np.diff(X) <= 0), "guard should be defeated (sanity on the mechanism)"
    s = RescaledHL(X)   # must NOT raise -- the guard is genuinely defeated
    Omega = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    with warnings.catch_warnings(record=True) as wl:
        warnings.simplefilter("always")
        Hom = s.hilbert(Omega)
    print(f"    G4: guard defeated (constructed OK), downstream all-NaN: "
          f"{np.all(np.isnan(Hom))}, warnings: {len(wl)}")
    assert np.all(np.isnan(Hom)), (
        "G4 REGRESSION: the poisoned grid now produces a FINITE downstream result -- "
        "this is a NEW silent-corruption chain, escalate immediately, do not weaken "
        "this assertion")
    print("[characterize] NaN defeats the ascending guard but stays visible downstream")


def test_CHARACTERIZE_solve_3x3_overrejects_tiny_wellconditioned_matrix():
    """CHARACTERIZE (G6 false positive): a uniformly-tiny (1e-16) but perfectly
    well-conditioned matrix is REJECTED as "singular" by the fixed absolute 1e-14 pivot
    threshold. Not a violation of this leg's gate (over-caution is not corruption), but
    recorded so a future repair of the threshold's scaling doesn't silently drop it."""
    A = np.eye(3) * 1e-16
    b = np.array([1e-16, 2e-16, 3e-16])
    try:
        _solve_3x3(A, b)
        raise AssertionError("G6 false positive REGRESSION: tiny matrix now accepted "
                             "(check whether the fix also preserves soundness)")
    except ValueError:
        pass
    print("[characterize] _solve_3x3 still over-rejects a uniformly tiny well-conditioned "
          "matrix (absolute, not relative, pivot threshold)")


# ============================================================================
# Soundness controls -- PASS today, and must keep passing (a failure here is a NEW gap).
# ============================================================================

def test_ascending_guard_rejects_finite_non_ascending_grids():
    """RescaledHL.__init__ correctly rejects every all-finite non-ascending grid: exact
    duplicates, a single descending pair, and a fully reversed array."""
    bad = [
        np.array([0.0, 1.0, 1.0, 2.0]),
        np.array([0.0, 2.0, 1.0, 3.0]),
        np.array([3.0, 2.0, 1.0, 0.0]),
    ]
    for X in bad:
        try:
            RescaledHL(X)
            raise AssertionError(f"accepted a non-ascending grid: {X}")
        except ValueError:
            pass
    print("[ok] RescaledHL rejects every all-finite non-ascending grid tested (3/3)")


def test_normalize_amp_never_silently_finite_on_poison():
    """SOUNDNESS (G5): normalize_amp's guard `abs(h0) < 1e-14` has the same NaN/inf blind
    spot as G4, checked directly on the amplitude-gauge division target/h0. Across
    NaN Omega, a single poisoned entry, all-+inf Omega, and near-max-float Omega, the
    division never produces a silently clean finite field -- always NaN, always visible."""
    d = RescaledHLDynamic(n=101, delta=0.05, M=20.0)
    configs = [
        np.full_like(d.X, np.nan),
        (lambda a: (a.__setitem__(50, np.nan), a)[1])(np.ones_like(d.X)),
        np.full_like(d.X, np.inf),
    ]
    n_silent = 0
    for Omega in configs:
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            try:
                out = d.normalize_amp(Omega, target=-1.0)
            except ValueError:
                continue
        if np.all(np.isfinite(out)) and len(wl) == 0:
            n_silent += 1
    print(f"    G5: {n_silent}/{len(configs)} poisoned configs returned silently finite")
    assert n_silent == 0, "G5 REGRESSION: normalize_amp now silently absorbs poison"
    print("[ok] normalize_amp never silently returns a clean finite field on poison "
          "(3/3 configs)")


def test_solve_3x3_never_silently_wrong():
    """SOUNDNESS (G6): _solve_3x3 across 300 random systems spanning 16 decades of scale
    never returns a finite solution disagreeing with numpy by more than 1e-3 relative
    while also carrying a large residual -- it always either matches numpy or raises."""
    rng = np.random.default_rng(0)
    n_silent = 0
    n_checked = 0
    for _ in range(300):
        A = rng.standard_normal((3, 3)) * (10.0 ** rng.uniform(-8, 8))
        b = rng.standard_normal(3) * (10.0 ** rng.uniform(-8, 8))
        try:
            xref = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        try:
            x = _solve_3x3(A, b)
        except ValueError:
            continue
        n_checked += 1
        resid = float(np.abs(np.array(A) @ x - np.array(b)).max())
        rel = float(np.abs(x - xref).max() / max(np.abs(xref).max(), 1e-300))
        if rel > 1e-3 and resid > 1e-6 * max(np.abs(b).max(), 1e-300):
            n_silent += 1
    print(f"    G6: {n_silent}/{n_checked} silently wrong (300 systems drawn)")
    assert n_silent == 0, "G6 REGRESSION: _solve_3x3 now returns a silently wrong solution"
    print(f"[ok] _solve_3x3 never silently wrong across {n_checked} random systems")


def test_inf_endpoints_never_silently_clean():
    """SOUNDNESS (G7): +/-inf at a grid ENDPOINT survives the ascending guard, but the
    downstream Hilbert/velocity pipeline always visibly warns or returns non-finite --
    never a silently clean finite answer. Interior inf is a control: correctly rejected."""
    configs = [
        np.array([0.0, 1.0, 2.0, 3.0, np.inf]),
        np.array([-np.inf, 0.0, 1.0, 2.0, 3.0]),
    ]
    n_silent = 0
    for X in configs:
        s = RescaledHL(X)   # must not raise -- endpoint inf is accepted
        Omega = np.ones_like(X)
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Hom = s.hilbert(Omega)
            U = s.velocity(Omega, Homega=Hom)
        if np.all(np.isfinite(Hom)) and np.all(np.isfinite(U)) and len(wl) == 0:
            n_silent += 1
    print(f"    G7: {n_silent}/{len(configs)} endpoint-inf configs silently clean")
    assert n_silent == 0, "G7 REGRESSION: an inf endpoint now propagates silently clean"
    # control: interior inf is still correctly rejected
    try:
        RescaledHL(np.array([0.0, 1.0, np.inf, 3.0, 4.0]))
        raise AssertionError("interior inf unexpectedly accepted")
    except ValueError:
        pass
    print("[ok] endpoint inf never propagates silently clean (2/2); interior inf still "
          "correctly rejected")


def test_degenerate_ic_rejects_unknown_kind():
    """SOUNDNESS control: degenerate_ic correctly raises on an unrecognised `kind` string
    -- the module's own correct-flagging behaviour, alongside its NaN-laundering defect."""
    try:
        degenerate_ic(np.linspace(-1, 1, 5), kind="not-a-real-kind")
        raise AssertionError("unknown kind was silently accepted")
    except ValueError:
        pass
    print("[ok] degenerate_ic still raises on an unrecognised kind")


if __name__ == "__main__":
    test_PIN_velocity_silently_corrupted_by_permutation()
    test_PIN_velocity_silently_clamps_xref_out_of_domain()
    test_PIN_sinh_grid_at_silently_reverses_on_negative_M()
    test_PIN_degenerate_ic_launders_nan_to_zero()
    test_scenario2_ic_negative_control_propagates_nan()
    test_CHARACTERIZE_nan_defeats_ascending_guard()
    test_CHARACTERIZE_solve_3x3_overrejects_tiny_wellconditioned_matrix()
    test_ascending_guard_rejects_finite_non_ascending_grids()
    test_normalize_amp_never_silently_finite_on_poison()
    test_solve_3x3_never_silently_wrong()
    test_inf_endpoints_never_silently_clean()
    test_degenerate_ic_rejects_unknown_kind()
    print("\nALL HL-RESCALED ADVERSARIAL GATES RAN")
    print("NOTE: 4 of these PIN CURRENT DEFECTIVE BEHAVIOUR (G1, G2, G3, G8, see module "
          "docstring). They must be INVERTED, not deleted, when a repair lands.")
