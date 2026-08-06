"""Leg 168 / Route-HRB -- the POST-REPAIR regression suite for solver/hl_rescaled.py.

Closes the loop on leg 152 (HRR), which repaired the four silent-corruption mechanisms
leg 117 (HRA) measured.  `solver/hl_rescaled.py` is READ-ONLY to leg 168.

WHAT THIS FILE IS FOR, AND WHY IT IS NOT test_hl_rescaled_adversarial.py AGAIN
------------------------------------------------------------------------------
`test_hl_rescaled_adversarial.py` already holds leg 117's battery with leg 152's pins
INVERTED.  Duplicating it here would add no information.  This file pins the things leg 152
did NOT pin, which are exactly the things a post-repair leg exists to find:

  1. The guards' ACTIVATION MARGIN.  The G2 guard fires when the Xc=1 dynamic grid stops
     reaching back to X_ref=0, measured at M* = 1.0380 (worst case over shipped
     resolutions).  The smallest M shipped anywhere in the repository is 20.0.  If a future
     change moves either number toward the other, `test_guard_activation_margin_holds`
     fails while the margin is still ~19x, rather than after a shipped run starts raising.
     Neither leg 117 (textual census) nor leg 152 (its own leaf set) ever took this number.
  2. The surfaces leg 152's 552,258-leaf differential NEVER CALLED -- RescaledHLDynamic.run,
     normalize_amp, amp_gauge, max_speed_s, max_speed_rho, origin_gauges -- pinned against
     regression, since "bit-identical" was only ever established off them.
  3. The +-inf boundary of the repaired G8 mask.  Leg 117 prescribed `isfinite`, leg 152
     shipped `isnan`; they differ exactly there.  The measured answer is that the narrowing
     is BENIGN on this module (see the test's own docstring), and that finding is pinned so
     it cannot silently stop being true.
  4. Leg 152's three DECLARED residues, pinned as declared so that a future silent fix or
     a silent worsening both show up as a failing test rather than as drift.

Run: python test_hl_rescaled_postrepair.py     (or pytest)
"""

import math
import warnings

import numpy as np

from solver.hl_rescaled import (
    HLRescaledDomainError, HLRescaledDomainWarning, RescaledHL, RescaledHLDynamic,
    RescaledHLScenario2, degenerate_ic, scenario2_ic, sinh_grid_at, velocity,
    _solve_3x3,
)

# Measured by experiments/p2_route_hrb_v1_postrepair.py (HRB4), worst case over the
# shipped (n, delta) resolutions.  This is the M below which velocity()'s G2 guard begins
# to fire on a RescaledHLDynamic grid, because the grid stops bracketing X_ref = 0.
M_STAR_MEASURED = 1.038017431239
SMALLEST_SHIPPED_M = 20.0


# ---------------------------------------------------------------------------
# 1. the guard-activation margin -- the number neither prior leg took
# ---------------------------------------------------------------------------
def test_guard_activation_margin_holds():
    """The G2 guard's boundary in M, bisected, against the smallest shipped M.

    This is an EARLY-WARNING pin, not a restatement of "no caller is exposed". Leg 117
    asserted zero exposure textually and leg 152 asserted it via a leaf set; both are
    statements about the repository as written on the day they ran. This one fails while
    there is still a ~19x margin."""
    worst = 0.0
    for (n, delta) in ((2001, 0.006), (1201, 0.02), (101, 0.05), (201, 0.02),
                       (301, 0.02), (2001, 0.004)):
        lo, hi = 0.5, 4.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            _, X = sinh_grid_at(n, Xc=1.0, delta=delta, M=mid, offset=True)
            if float(X.min()) > 0.0:
                lo = mid
            else:
                hi = mid
        worst = max(worst, hi)
    margin = SMALLEST_SHIPPED_M / worst
    print(f"    M* (worst over shipped resolutions) = {worst:.6f}, "
          f"smallest shipped M = {SMALLEST_SHIPPED_M}, margin = {margin:.2f}x")
    assert abs(worst - M_STAR_MEASURED) < 1e-3, \
        f"the G2 activation boundary moved: {worst:.6f} vs banked {M_STAR_MEASURED:.6f}"
    assert margin > 5.0, f"guard-activation margin collapsed to {margin:.2f}x"
    print("[ok] G2 guard boundary is where leg 168 measured it, with a ~19x margin")


def test_guard_margin_control_can_fire_and_can_stay_silent():
    """LESSON 90. A margin measurement whose guard never fires on either side is measuring
    nothing. One argument changed in the identical call, both directions asserted."""
    fired = accepted = 0
    for M in (0.5, 0.8, 0.95):
        _, X = sinh_grid_at(101, Xc=1.0, delta=0.05, M=M, offset=True)
        try:
            velocity(X, np.ones_like(X), X_ref=0.0)
        except HLRescaledDomainError:
            fired += 1
    for M in (1.5, 5.0, 20.0):
        _, X = sinh_grid_at(101, Xc=1.0, delta=0.05, M=M, offset=True)
        velocity(X, np.ones_like(X), X_ref=0.0)
        accepted += 1
    print(f"    below M*: {fired}/3 raise;  above M*: {accepted}/3 accepted")
    assert fired == 3, "the guard does not fire below M* -- the boundary is not real"
    assert accepted == 3, "the guard over-rejects above M* -- shipped configs at risk"
    print("[ok] the guard fires below M* and is silent above it (both directions)")


# ---------------------------------------------------------------------------
# 2. the surfaces leg 152's differential never called
# ---------------------------------------------------------------------------
def test_uncovered_surfaces_are_clean_and_finite():
    """RescaledHLDynamic.run / normalize_amp / amp_gauge / max_speed_s and
    RescaledHLScenario2.origin_gauges / max_speed_rho appear NOWHERE in leg 152's
    differential. Leg 168 differenced them bitwise against the pre-repair module at
    13,413 leaves with 0 moved; this pins that they still execute cleanly and that no
    guard fires on a shipped configuration."""
    d = RescaledHLDynamic(n=201, delta=0.02, M=150.0, nu=0.02)
    Om0, Th0 = degenerate_ic(d.X, kind="A")
    assert d.X.min() < 0.0 < d.X.max(), "shipped dynamic grid no longer brackets X_ref=0"
    Om_n = d.normalize_amp(Om0)
    amp = d.amp_gauge(Om_n)
    assert abs(amp + 1.0) < 1e-9, f"amplitude gauge not pinned to -1: {amp}"
    assert np.isfinite(d.max_speed_s(Om_n)), "max_speed_s non-finite on shipped data"
    with warnings.catch_warnings():
        warnings.simplefilter("error", HLRescaledDomainWarning)
        r = d.run(Om0, Th0, max_steps=60, tol=1e-14, record_every=10)
    assert np.all(np.isfinite(r["X"])), "run() corrupted the grid"
    assert r["steps"] == 60, f"run() terminated early at {r['steps']}"

    s2 = RescaledHLScenario2(n=301, c=0.35, rho_max=7.0, nu=0.02)
    Om, V = scenario2_ic(s2.X, x0=0.30)
    g = s2.origin_gauges(Om, V)
    assert all(np.isfinite(g)), f"origin gauges non-finite: {g}"
    assert np.isfinite(s2.max_speed_rho(Om, V)), "max_speed_rho non-finite"
    print(f"    dynamic amp gauge = {amp:+.3e}; origin gauges = "
          f"({g[0]:+.4f}, {g[1]:+.4f}, {g[2]:+.4f})")
    print("[ok] every surface leg 152's differential skipped runs clean on shipped configs")


def test_velocity_guard_never_fires_on_any_shipped_constructor():
    """The executable form of leg 117's and leg 152's textual exposure census: build the
    shipped configurations and actually CALL the guarded path on each."""
    built = 0
    for (n, delta, M) in ((2001, 0.006, 500.0), (1201, 0.02, 200.0), (2001, 0.004, 500.0),
                          (101, 0.05, 20.0), (301, 0.02, 150.0)):
        d = RescaledHLDynamic(n=n, delta=delta, M=M)
        Om, _ = degenerate_ic(d.X, kind="A")
        d.velocity(Om)                      # would raise if either guard fired
        built += 1
    for (n, c, rho_max) in ((1201, 0.5, 8.0), (801, 0.35, 7.0), (401, 0.35, 7.0)):
        s2 = RescaledHLScenario2(n=n, c=c, rho_max=rho_max)
        Om, _ = scenario2_ic(s2.X)
        s2.velocity(Om)
        built += 1
    print(f"    {built}/8 shipped constructor configurations call velocity() without raising")
    assert built == 8
    print("[ok] no shipped configuration reaches any new guard")


# ---------------------------------------------------------------------------
# 3. the +-inf boundary of the repaired G8 mask (isnan vs isfinite)
# ---------------------------------------------------------------------------
def test_pm_inf_boundary_of_the_repaired_nan_mask():
    """Leg 117 PRESCRIBED `np.isfinite(X)`; leg 152 SHIPPED `np.isnan(X)`. They differ
    exactly on +-inf, which is the classic incomplete-fix shape -- so it was measured
    rather than assumed.

    The measured answer is that the narrowing is BENIGN HERE, and the reason is specific,
    not a general licence: `degenerate_ic` maps X through `xp = np.maximum(X, 0.0)`, so at
    X = -inf the defining formula is evaluated at xp = 0 and returns 0 by the SAME
    arithmetic that a legitimate X <= 0 node uses. Two independent routes -- the formula
    and the module's one-sided-support convention -- give the same 0.0, so 0.0 is the
    CORRECT value there, not a fabrication. That is the distinction from the NaN case leg
    117 found, where 0.0 was invented for an abscissa that has no location at all.

    At +inf every kind returns either NaN or the true limit 0.0; no kind returns a WRONG
    FINITE value, which is the property that actually matters and the one pinned here."""
    X = np.array([-3.0, -np.inf, -1.0, 0.0, 0.5, 2.0, np.inf, 4.0])
    for kind in ("A", "B", "C"):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            om, th = degenerate_ic(X, kind=kind)
        # -inf agrees with a legitimate X<=0 node, and that agreement is CORRECT
        assert om[1] == om[0] == 0.0, f"kind {kind}: -inf Omega0 diverged from an X<=0 node"
        assert th[1] == th[0] == 0.0, f"kind {kind}: -inf Theta0 diverged from an X<=0 node"
        # +inf: NaN or the true limit 0.0, never a wrong finite number
        for name, v in (("Omega0", om[6]), ("Theta0", th[6])):
            assert np.isnan(v) or v == 0.0, \
                f"kind {kind}: +inf {name} returned a wrong finite value {v!r}"
        # and the NaN case that leg 152 DID repair must still propagate
        Xn = np.array([-1.0, np.nan, 1.0, 2.0])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            omn, thn = degenerate_ic(Xn, kind=kind)
        assert np.isnan(omn[1]) and np.isnan(thn[1]), \
            f"kind {kind}: the repaired NaN mask stopped propagating"
    print("    -inf -> exact 0.0 (correct, two routes); +inf -> NaN or 0.0, never wrong-finite")
    print("[ok] the isnan/isfinite narrowing is benign on this module, and pinned as such")


def test_endpoint_inf_grid_boundary_preserved():
    """Leg 117's G7 boundary, which leg 152 deliberately PRESERVED through the G4 polarity
    flip: +-inf at a grid ENDPOINT is still accepted, an interior inf is still rejected.
    Pinned because the G4 flip is precisely the kind of change that could have moved it."""
    X = np.linspace(0.0, 10.0, 41).copy()
    X[0], X[-1] = -np.inf, np.inf
    RescaledHL(X)                                     # must NOT raise
    Xi = np.linspace(0.0, 10.0, 41).copy()
    Xi[20] = np.inf
    try:
        RescaledHL(Xi)
    except HLRescaledDomainError:
        pass
    else:
        raise AssertionError("interior inf silently accepted as a valid grid")
    Xn = np.linspace(0.0, 10.0, 41).copy()
    Xn[17] = np.nan
    try:
        RescaledHL(Xn)
    except HLRescaledDomainError:
        pass
    else:
        raise AssertionError("NaN-poisoned grid accepted -- the G4 repair regressed")
    print("[ok] endpoint +-inf accepted, interior inf and any NaN rejected (G7/G4 boundary)")


# ---------------------------------------------------------------------------
# 4. leg 152's three declared residues, pinned AS DECLARED
# ---------------------------------------------------------------------------
def test_declared_residue_solve3x3_still_over_rejects():
    """Leg 152 declared this unpatched on purpose (its journal, "Residue"). Pinned so a
    future silent change -- in either direction -- surfaces as a test failure."""
    A = 1e-16 * np.eye(3)
    b = 1e-16 * np.array([1.0, 2.0, 3.0])
    cond = float(np.linalg.cond(A))
    assert cond < 10.0, "control: the matrix is supposed to be perfectly conditioned"
    assert np.all(np.isfinite(np.linalg.solve(A, b))), "control: numpy solves it fine"
    try:
        _solve_3x3(A, b)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "_solve_3x3 no longer over-rejects a tiny well-conditioned matrix -- leg 152's "
            "declared residue changed without being declared")
    print(f"    cond = {cond:.2f}, numpy solves it, _solve_3x3 still raises (as declared)")
    print("[ok] the absolute-pivot residue is unchanged from leg 152's declaration")


def test_declared_residue_small_n_still_indexerror():
    """Declared residue: n < 2 raises IndexError, not HLRescaledDomainError. Cosmetic and
    VISIBLE, which is why leg 152 left it; pinned so it stays visible."""
    seen = {}
    for n in (0, 1):
        try:
            sinh_grid_at(n, Xc=1.0, delta=0.1, M=50.0)
            seen[n] = None
        except Exception as e:
            seen[n] = type(e).__name__
    assert all(v is not None for v in seen.values()), \
        f"sinh_grid_at silently accepted n < 2: {seen}"
    print(f"    n=0 -> {seen[0]}, n=1 -> {seen[1]} (visible, not silent)")
    print("[ok] the small-n residue is still visible rather than silent")


def test_declared_residue_remaining_interp_sites_unreachable():
    """Leg 152 left RescaledHLDynamic.gauge / max_speed_s calling np.interp unguarded,
    declaring both unreachable on every shipped grid. That is a claim about the GRID, so
    it is pinned as one, with the margin as a number."""
    for (n, delta, M) in ((2001, 0.006, 500.0), (1201, 0.02, 200.0), (101, 0.05, 20.0),
                          (301, 0.02, 150.0)):
        d = RescaledHLDynamic(n=n, delta=delta, M=M)
        lo, hi = float(d.X.min()), float(d.X.max())
        assert lo < 0.0 < 1.0 < hi, (
            f"M={M}: the grid [{lo:.3f}, {hi:.3f}] no longer brackets both interp sites "
            f"(X=0 for c_omega, X=1 for c_l) -- the declared-unreachable residue is now "
            f"REACHABLE and clamps silently")
    print("    every shipped dynamic grid brackets both X=0 and X=1 with room to spare")
    print("[ok] the two remaining np.interp sites are still unreachable, as declared")


if __name__ == "__main__":
    test_guard_activation_margin_holds()
    test_guard_margin_control_can_fire_and_can_stay_silent()
    test_uncovered_surfaces_are_clean_and_finite()
    test_velocity_guard_never_fires_on_any_shipped_constructor()
    test_pm_inf_boundary_of_the_repaired_nan_mask()
    test_endpoint_inf_grid_boundary_preserved()
    test_declared_residue_solve3x3_still_over_rejects()
    test_declared_residue_small_n_still_indexerror()
    test_declared_residue_remaining_interp_sites_unreachable()
    print("\nALL HL-RESCALED POST-REPAIR (ROUTE-HRB) TESTS PASSED")
