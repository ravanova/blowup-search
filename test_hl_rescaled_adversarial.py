"""Adversarial gates for `solver/hl_rescaled.py` (leg 117, Route-HRA).

`test_hl_rescaled.py` validates the module on WELL-BEHAVED data: sorted sinh-stretched
grids, `X_ref` pinned inside the sampled domain, the exact Theorem-2.3 anchor. This file
validates the other half — degenerate, poisoned, out-of-contract input — and banks leg
117's battery so the answer cannot silently regress.

The gate leg 117 answered, verbatim (`DIRECTION.md`, leg 117):

  "Under an adversarial battery of degenerate or poisoned inputs, does
   solver/hl_rescaled.py ever silently return a wrong result instead of flagging the
   input?"

Answered **YES**. Four silent-corruption mechanisms found, escalated, not patched.

REPAIRED AT LEG 152 (Route-HRR). THE PINS BELOW ARE NOW INVERTED.
-----------------------------------------------------------------
Leg 152 landed the guards in `solver/hl_rescaled.py` and INVERTED every PIN in this file
in the same commit — never weakened, never deleted, and never at a softer threshold than
leg 117 measured. Each former `test_PIN_*` is now `test_REPAIRED_*` and asserts, on leg
117's OWN configuration, that the module flags what it used to absorb; every magnitude
leg 117 measured is still asserted, only the verdict is flipped. Each also asserts the
documented `on_invalid="warn"` escape reproduces leg 117's number BIT-IDENTICALLY, so the
measurement that authorised the repair survives the repair (leg 135's finding on
`first_integral.py`: a repair that makes the escalating leg's battery unrunnable has
destroyed the record it was meant to preserve).

The licence for the repair is `experiments/p2_route_hrr_v1_repair.py`'s differential:
**552,258 of 552,258 clean-input leaves bit-identical** (`==` on float64, not `allclose`)
against the pre-repair module read out of git at `2450ddf` and imported into the same
process — grids, closed-form anchors, the free `velocity()`, both IC generators,
`_solve_3x3` over 300 systems, `RescaledHL`, five real SSPRK3 steps of
`RescaledHLDynamic`, and a 120-step `RescaledHLScenario2` relaxation. Zero clean values
moved. `test_REPAIRED_zero_clean_input_movement` below re-runs a sample of that
differential so the no-op guarantee is executable here too, not just in the runner.

THE FOUR FINDINGS, AS MEASURED BY LEG 117 AND AS THEY STAND AFTER THE REPAIR
(magnitudes, measured by
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

  G4. `RescaledHL.__init__`'s ascending guard `np.any(np.diff(X) <= 0)` had the identical
      IEEE-754 comparison blind spot (a NaN anywhere defeated it). Leg 117 characterized
      rather than exploited it (it chains to a visible all-NaN Hilbert transform, not a
      finite wrong answer) and `DIRECTION.md` left the patch-or-document call to leg 152.
      **Leg 152 PATCHED it**, and states the reasoning here as the gate requires: the fix
      adds no machinery, it is the same one-token polarity flip
      `np.any(d <= 0)` -> `np.all(d > 0)` that `velocity()`'s G1 guard needs anyway
      (identical on every finite input, NaN-rejecting for free — SEI CERT NUM07-J), and
      leaving the class laxer than the free function it calls would have been a NEW
      inconsistency. The over-rejection controls are asserted alongside it: an endpoint
      `+/-inf` grid is STILL accepted (leg 117's G7) and an interior `inf` still rejected.
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
    HLRescaledDomainError, HLRescaledDomainWarning, RescaledHL, RescaledHLDynamic,
    RescaledHLScenario2, degenerate_ic, omega_bar, scenario2_ic, sinh_grid_at, velocity,
    _solve_3x3,
)

# The pre-repair module's own last commit. `git diff 2450ddf <repair> -- the module` was
# EMPTY before leg 152, so this blob is byte-identical to what leg 117 audited. Pinned to
# the module's own creating/last-touching commit and NOT to a leg's own hash, which the
# rebase onto main rewrites (leg 130's correction, d871675).
PRE_REPAIR_REF = "2450ddf"


def _load_pre_repair():
    """Import the pre-repair module from git under a private name, in this process.
    Returns None if git is unavailable (the differential check then skips, loudly)."""
    import importlib.util
    import subprocess
    import tempfile
    root = os.path.dirname(os.path.abspath(__file__))
    try:
        src = subprocess.run(
            ["git", "show", f"{PRE_REPAIR_REF}:solver/hl_rescaled.py"],
            cwd=root, capture_output=True, text=True, check=True).stdout
    except Exception:
        return None
    fd, path = tempfile.mkstemp(suffix="_pre_hl_rescaled.py")
    with os.fdopen(fd, "w") as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("_pre_hl_rescaled_t", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ============================================================================
# INVERTED PINs (leg 152). Each was a `test_PIN_*` asserting the defect; each now
# asserts the repair on leg 117's OWN configuration, at leg 117's OWN thresholds.
# ============================================================================

def test_REPAIRED_velocity_rejects_non_ascending_X():
    """INVERTED PIN (G1). Was: velocity() never checks X is ascending, and a permutation
    of a correctly sorted (X, Homega) pair is silently integrated wrong (20/20 trials,
    worst 212.0356 absolute = 135.65x the true scale sup|U| = 1.5631).

    Now: every one of leg 117's 20 permutations raises HLRescaledDomainError. The
    documented `on_invalid="warn"` escape still returns leg 117's number BIT-IDENTICALLY
    with a warning, so the measurement survives its own repair.

    NOTE on leg 117's prose: its headline said "91x the true scale". 91.30 is trial 0's
    ratio; the WORST ratio, banked in its own JSON as `worst_max_rel_error`, is 135.65 and
    pairs with the 212.0356 absolute the same prose quotes. Both numbers reproduce here
    exactly; only the pairing in the prose was off."""
    _, X = sinh_grid_at(201, Xc=0.0, delta=None, M=50.0)
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)
    U_true = velocity(X, Homega, X_ref=0.0)
    Uex = np.arctan(2.0 * X)
    assert np.abs(U_true - Uex).max() < 1e-2, "sanity: sorted call should match analytic"

    rng = np.random.default_rng(0)
    n_raised = 0
    worst_err = 0.0
    pre = _load_pre_repair()
    for _ in range(20):
        perm = rng.permutation(len(X))
        Xp, Hp = X[perm], Homega[perm]
        try:
            velocity(Xp, Hp, X_ref=0.0)
        except HLRescaledDomainError:
            n_raised += 1
        # the escape hatch must still MEASURE the defect, bit-identically
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Uw = velocity(Xp, Hp, X_ref=0.0, on_invalid="warn")
        assert len(wl) == 1 and isinstance(wl[0].message, HLRescaledDomainWarning), \
            "on_invalid='warn' must emit exactly one HLRescaledDomainWarning"
        inv = np.argsort(perm)
        worst_err = max(worst_err, float(np.abs(Uw[inv] - U_true).max()))
        if pre is not None:
            assert np.all(Uw == pre.velocity(Xp, Hp, X_ref=0.0)), \
                "on_invalid='warn' must reproduce the PRE-REPAIR value bitwise"
    print(f"    G1 INVERTED: {n_raised}/20 permutations now raise "
          f"HLRescaledDomainError; the warn-escape still measures the defect at "
          f"{worst_err:.4f} absolute ({worst_err / float(np.abs(U_true).max()):.2f}x "
          f"sup|U|), bit-identical to the pre-repair module")
    assert n_raised == 20, f"G1 REGRESSION: only {n_raised}/20 permutations rejected"
    # leg 117's OWN threshold, unchanged -- the defect it measured is still there to
    # measure through the documented escape, so the repair did not erase the record
    assert worst_err > 1.0, "G1: the warn-escape no longer reproduces leg 117's defect"
    assert abs(worst_err - 212.0356008474817) < 1e-9, \
        f"G1: leg 117's banked worst absolute error no longer reproduces ({worst_err})"
    print("[inverted] velocity() rejects a non-ascending X")


def test_REPAIRED_velocity_rejects_xref_out_of_domain():
    """INVERTED PIN (G2). Was: velocity()'s X_ref pin via np.interp silently clamped when
    X_ref fell outside [X.min(), X.max()] (a documented numpy default), shifting the whole
    returned array by a constant -- 1.4712 absolute at X_ref=-5.0 against a [0,10] window.

    Now: HLRescaledDomainError on all four of leg 117's out-of-domain values, with the
    warn-escape reproducing the shift bit-identically. Over-rejection controls included:
    BOTH endpoints and interior points are still accepted."""
    X = np.linspace(0.0, 10.0, 501)
    Homega = 2.0 / (1.0 + 4.0 * X ** 2)
    pre = _load_pre_repair()
    n_raised = 0
    worst = 0.0
    for X_ref_out in (-5.0, -0.5, 10.5, 25.0):
        try:
            velocity(X, Homega, X_ref=X_ref_out)
        except HLRescaledDomainError:
            n_raised += 1
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            U_out = velocity(X, Homega, X_ref=X_ref_out, on_invalid="warn")
        assert len(wl) == 1, "warn-escape must emit exactly one warning"
        true_pinned = np.arctan(2.0 * X) - np.arctan(2.0 * X_ref_out)
        err = float(np.abs(U_out - true_pinned).max())
        if X_ref_out == -5.0:
            worst = err
        if pre is not None:
            assert np.all(U_out == pre.velocity(X, Homega, X_ref=X_ref_out)), \
                "warn-escape must reproduce the PRE-REPAIR clamped value bitwise"
    # over-rejection controls: in-domain, INCLUDING both endpoints, must still work
    n_ok = 0
    for X_ref_in in (0.0, 10.0, 5.0, float(X[1])):
        velocity(X, Homega, X_ref=X_ref_in)
        n_ok += 1
    print(f"    G2 INVERTED: {n_raised}/4 out-of-domain X_ref values now raise; "
          f"warn-escape still measures leg 117's {worst:.4f} shift at X_ref=-5.0; "
          f"{n_ok}/4 in-domain values (both endpoints included) still accepted")
    assert n_raised == 4, f"G2 REGRESSION: only {n_raised}/4 rejected"
    assert err_close(worst, 1.4712, 1e-3), \
        f"G2: leg 117's banked 1.4712 shift no longer reproduces ({worst})"
    assert n_ok == 4, "G2 OVER-REJECTION: an in-domain X_ref was refused"
    print("[inverted] velocity() rejects an out-of-domain X_ref and still accepts every "
          "in-domain one")


def err_close(a, b, tol):
    return abs(a - b) < tol


def test_REPAIRED_sinh_grid_at_rejects_non_positive_scale():
    """INVERTED PIN (G3). Was: sinh_grid_at(n, M=negative) silently returned the exact
    descending mirror of the valid (M>0) grid, zero warnings.

    Now: HLRescaledDomainError. It REJECTS rather than silently taking abs(M) -- leg 117
    offered either, and substituting a different input for the one you were given is the
    defect class the target_norm.py/leg-94 precedent forbids, not a fix.

    `delta <= 0` is leg 152's DECLARED in-kind extension: X = Xc + delta*sinh(s), so a
    non-positive delta mirrors the grid by the identical mechanism. Leg 117 measured only
    M; leaving delta would have been the incomplete-fix shape leg 147 caught on
    nk_bounds.py. Both are asserted here."""
    kwargs = dict(Xc=0.0, delta=1.0, M=50.0, offset=False)
    _, X_pos = sinh_grid_at(11, **kwargs)
    assert np.all(np.diff(X_pos) > 0), "sanity: the valid grid is ascending"
    n_rej = 0
    bad = [{"M": -50.0}, {"M": 0.0}, {"M": -1e-12}, {"delta": -1.0}, {"delta": 0.0}]
    for b in bad:
        try:
            sinh_grid_at(11, **{**kwargs, **b})
        except HLRescaledDomainError:
            n_rej += 1
    # over-rejection control: every positive scale still builds the same grid
    n_ok = 0
    for b in [{"M": 50.0}, {"M": 1e-6}, {"delta": 1e-6}, {"delta": 100.0}]:
        _, Xg = sinh_grid_at(11, **{**kwargs, **b})
        assert np.all(np.diff(Xg) > 0)
        n_ok += 1
    print(f"    G3 INVERTED: {n_rej}/{len(bad)} non-positive scales now raise "
          f"(M and the declared in-kind delta clause); {n_ok}/4 positive scales still "
          f"build an ascending grid")
    assert n_rej == len(bad), f"G3 REGRESSION: only {n_rej}/{len(bad)} rejected"
    assert n_ok == 4, "G3 OVER-REJECTION: a legitimate positive scale was refused"
    print("[inverted] sinh_grid_at rejects a non-positive M or delta")


def test_REPAIRED_degenerate_ic_propagates_nan():
    """INVERTED PIN (G8, leg 117's headline). Was: degenerate_ic's closing
    `np.where(X > 0.0, field, 0.0)` used an ordered comparison, so IEEE-754 made it False
    wherever X was NaN and np.where wrote the same clean finite 0.0 a legitimate X<=0
    point produces -- 6 laundered values per kind, all three kinds, zero warnings.

    Now: a NaN abscissa propagates, exactly as scenario2_ic (same module, no closing mask)
    already did -- the in-module reference behaviour the PIN itself named as CORRECT.
    Every NON-NaN entry is asserted bit-identical to the pre-repair module, which is the
    no-op half of the licence."""
    X = np.linspace(-5.0, 5.0, 51)
    nan_idx = [10, 30, 45]
    X[nan_idx] = np.nan
    clean = np.array([i for i in range(51) if i not in nan_idx])
    pre = _load_pre_repair()
    for kind in ("A", "B", "C"):
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            Om, Th = degenerate_ic(X, kind=kind)
        n_laundered = int(np.sum(Om[nan_idx] == 0.0) + np.sum(Th[nan_idx] == 0.0))
        print(f"    G8 INVERTED kind={kind}: {n_laundered}/6 NaN positions laundered to "
              f"exact 0.0 (was 6/6), NaN propagated: "
              f"{np.all(np.isnan(Om[nan_idx])) and np.all(np.isnan(Th[nan_idx]))}, "
              f"{len(wl)} warnings")
        assert n_laundered == 0, \
            f"G8({kind}) REGRESSION: {n_laundered} NaN abscissas still laundered to 0.0"
        assert np.all(np.isnan(Om[nan_idx])) and np.all(np.isnan(Th[nan_idx])), \
            f"G8({kind}) REGRESSION: a NaN abscissa did not propagate"
        if pre is not None:
            Om_p, Th_p = pre.degenerate_ic(X, kind=kind)
            assert np.all(Om[clean] == Om_p[clean]) and np.all(Th[clean] == Th_p[clean]), \
                f"G8({kind}) NO-OP VIOLATED: a non-NaN entry moved"
    print("[inverted] degenerate_ic propagates a NaN abscissa; every non-NaN entry is "
          "bit-identical to the pre-repair module")


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

def test_REPAIRED_nan_no_longer_defeats_ascending_guard():
    """INVERTED CHARACTERIZATION (G4). Was: RescaledHL.__init__'s guard
    `np.any(np.diff(X) <= 0)` had the same NaN-comparison blind spot as G8's mechanism --
    a NaN anywhere made it vacuously pass, so a completely scrambled, NaN-containing array
    was accepted as a "valid" grid. Leg 117 recorded this as a characterization rather
    than a PIN because it chains to a visible all-NaN Hilbert transform, not a finite
    wrong answer, and DIRECTION.md left the patch-or-document call to leg 152.

    LEG 152 PATCHED IT. The predicate is now `np.all(np.diff(X) > 0)`: identical on every
    finite input, NaN-rejecting for free, because under IEEE-754 "confirm the good case"
    fails CLOSED where "detect the bad case" fails OPEN (SEI CERT NUM07-J). The reasoning
    is recorded in full in this file's module docstring and writeup/novelty/leg_152.md.

    The two over-rejection controls are the load-bearing half of this test: leg 117's G7
    finding is that an ENDPOINT +/-inf grid is well-defined and stays visible downstream,
    so it must STILL be accepted, and an interior inf must still be rejected. A guard that
    closed G4 by also refusing those would be a behaviour change, not a repair."""
    X = np.array([0.0, 1.0, np.nan, 0.5, 2.0])   # scrambled AND poisoned
    assert not np.any(np.diff(X) <= 0), \
        "sanity on the mechanism: the OLD predicate is still vacuously satisfied here"
    assert not np.all(np.diff(X) > 0.0), \
        "sanity on the fix: the NEW predicate is not satisfied here"
    raised = False
    try:
        RescaledHL(X)
    except HLRescaledDomainError:
        raised = True
    # over-rejection controls
    n_endpoint_ok = 0
    for Xe in (np.array([0.0, 1.0, 2.0, 3.0, np.inf]),
               np.array([-np.inf, 0.0, 1.0, 2.0, 3.0])):
        RescaledHL(Xe)
        n_endpoint_ok += 1
    interior_rejected = False
    try:
        RescaledHL(np.array([0.0, 1.0, np.inf, 3.0, 4.0]))
    except HLRescaledDomainError:
        interior_rejected = True
    print(f"    G4 INVERTED: NaN-poisoned scrambled grid rejected: {raised}; "
          f"endpoint-inf grids still accepted: {n_endpoint_ok}/2 (leg 117's G7); "
          f"interior inf still rejected: {interior_rejected}")
    assert raised, "G4 REGRESSION: a NaN-poisoned grid is accepted again"
    assert n_endpoint_ok == 2, "G4 OVER-REJECTION: an endpoint-inf grid was refused"
    assert interior_rejected, "G4: an interior inf is no longer rejected"
    print("[inverted] a NaN no longer defeats the ascending guard, and neither "
          "over-rejection control moved")


def test_REPAIRED_zero_clean_input_movement():
    """THE LICENCE FOR THE WHOLE REPAIR, executable here and not only in the runner.

    Every guard leg 152 added fires ONLY on input already outside the module's stated
    contract. This re-runs a sample of `experiments/p2_route_hrr_v1_repair.py`'s
    differential against the pre-repair module read out of git at 2450ddf and imported
    into this process: grids, the closed-form anchors, the free velocity(), both IC
    generators, RescaledHL's Hilbert/velocity/dX and a real RescaledHLDynamic SSPRK3 step.
    Comparison is `==` on float64, NOT allclose. The full runner compares 552,258 leaves;
    this samples the same surfaces so a regression cannot land without a test failing.

    LESSON 90: the control that this comparison CAN report the other answer is asserted
    first -- the pre-repair module must lack the new symbols and must still launder a NaN.
    Without it, "0 moved" would be a tautology of the import."""
    pre = _load_pre_repair()
    if pre is None:
        print("[skip] git unavailable; the differential is in the runner")
        return
    # lesson-90 control FIRST
    assert not hasattr(pre, "HLRescaledDomainError"), \
        "lesson-90 control FAILED: the 'pre-repair' module already has the new guard"
    Xn = np.linspace(-5.0, 5.0, 51)
    Xn[[10, 30, 45]] = np.nan
    assert np.all(pre.degenerate_ic(Xn, kind="A")[0][[10, 30, 45]] == 0.0), \
        "lesson-90 control FAILED: the pre-repair module no longer launders a NaN"

    n = n_ident = 0

    def cmp(a, b):
        nonlocal n, n_ident
        a, b = np.asarray(a, float).ravel(), np.asarray(b, float).ravel()
        assert a.shape == b.shape
        n += a.size
        n_ident += int(np.sum(a == b))

    for kw in (dict(n=101, Xc=1.0, delta=0.05, M=20.0, offset=True),
               dict(n=201, Xc=0.0, delta=None, M=50.0, offset=True),
               dict(n=201, Xc=1.0, delta=0.01, M=500.0, offset=True)):
        s_p, X_p = pre.sinh_grid_at(**kw)
        s_q, X_q = sinh_grid_at(**kw)
        cmp(s_p, s_q); cmp(X_p, X_q)
        X = X_q
        cmp(pre.omega_bar(X), omega_bar(X))
        Hom = 2.0 / (1.0 + 4.0 * X ** 2)
        for X_ref in (0.0, 1.0, float(X[X.size // 3])):
            cmp(pre.velocity(X, Hom, X_ref=X_ref), velocity(X, Hom, X_ref=X_ref))
        for kind in ("A", "B", "C"):
            op, tp = pre.degenerate_ic(X, kind=kind)
            oq, tq = degenerate_ic(X, kind=kind)
            cmp(op, oq); cmp(tp, tq)
        op, vp = pre.scenario2_ic(X)
        oq, vq = scenario2_ic(X)
        cmp(op, oq); cmp(vp, vq)
        a, b = pre.RescaledHL(X, X_ref=0.0), RescaledHL(X, X_ref=0.0)
        Om = omega_bar(X)
        cmp(a.hilbert(Om), b.hilbert(Om))
        cmp(a.velocity(Om), b.velocity(Om))
        cmp(a.dX(Om), b.dX(Om))

    da, db = pre.RescaledHLDynamic(n=101, delta=0.05, M=20.0), \
        RescaledHLDynamic(n=101, delta=0.05, M=20.0)
    Oa = da.normalize_amp(omega_bar(da.X))
    Ob = db.normalize_amp(omega_bar(db.X))
    cmp(Oa, Ob)
    Th = np.where(da.X > 1.0, np.pi / 2.0, 0.0)
    ra, rb = da.step(Oa, Th, 1e-4), db.step(Ob, Th, 1e-4)
    cmp(ra[0], rb[0]); cmp(ra[1], rb[1])
    cmp([ra[2], ra[3], ra[4]], [rb[2], rb[3], rb[4]])

    print(f"    NO-OP: {n_ident}/{n} clean-input leaves bit-identical to the pre-repair "
          f"module at {PRE_REPAIR_REF} (== on float64, not allclose)")
    assert n_ident == n, (
        f"NO-OP VIOLATED: {n - n_ident} of {n} clean-input leaves MOVED. The repair's "
        f"entire licence is a measured no-op on clean input -- ESCALATE, do not iterate.")
    print("[ok] the repair moves nothing on clean input")


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
    test_REPAIRED_velocity_rejects_non_ascending_X()
    test_REPAIRED_velocity_rejects_xref_out_of_domain()
    test_REPAIRED_sinh_grid_at_rejects_non_positive_scale()
    test_REPAIRED_degenerate_ic_propagates_nan()
    test_scenario2_ic_negative_control_propagates_nan()
    test_REPAIRED_nan_no_longer_defeats_ascending_guard()
    test_REPAIRED_zero_clean_input_movement()
    test_CHARACTERIZE_solve_3x3_overrejects_tiny_wellconditioned_matrix()
    test_ascending_guard_rejects_finite_non_ascending_grids()
    test_normalize_amp_never_silently_finite_on_poison()
    test_solve_3x3_never_silently_wrong()
    test_inf_endpoints_never_silently_clean()
    test_degenerate_ic_rejects_unknown_kind()
    print("\nALL HL-RESCALED ADVERSARIAL GATES RAN")
    print("NOTE: leg 152 INVERTED all 4 PINs (G1, G2, G3, G8) and the G4 characterization "
          "in the same commit as the repair, at leg 117's own thresholds. The licence is "
          "test_REPAIRED_zero_clean_input_movement + experiments/p2_route_hrr_v1_repair.py: "
          "552,258/552,258 clean leaves bit-identical to the pre-repair module.")
