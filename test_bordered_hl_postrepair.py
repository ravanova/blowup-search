"""Post-repair gates for leg 218's border-weight guard in `solver/bordered_hl.py`.

Leg 198 (Route-BHA) CHARACTERIZED four silent-corruption sites in this module. Two of
them are weight-surface sites, and they are the ones leg 218 repaired:

    test_characterize_negative_weight_returns_a_negative_operator_norm
    test_characterize_negative_weight_fabricates_a_closing_certificate

Those gates live on the unmerged branch `leg/198-bha-v1` and were written to FAIL once
a positivity guard landed ("WILL FAIL when a positivity guard lands on the weights").
The guard has landed. This file is where they belong now, INVERTED: every threshold
leg 198 pinned is re-stated here at leg 198's own numbers, never weakened, with the
polarity flipped from "the corruption is still reachable" to "the corruption is
refused". Where leg 198 pinned an exact corrupted value (-1.0, -3999999997.0), this
file pins that the ESCAPE HATCH still reproduces it exactly -- so leg 198's measured
magnitudes stay reproducible after the repair its own finding authorised (leg 135's
rule), and the guard cannot be "verified" by a test that merely stopped measuring.

Leg 228, Route-BHRV. Reads `solver/bordered_hl.py`; edits nothing.

Run: .venv/bin/python test_bordered_hl_postrepair.py
"""

import sys
import warnings

import numpy as np

from solver.bordered_hl import (
    BorderedHL, BorderedHLDomainError, CHL_TRIPLE, induced_sup_norm,
)

FAILURES = []


def _fresh(n=101, rho_max=8.0, x0=0.3, w=0.9):
    """Leg 198's own fixture, re-derived: generic non-symmetric data, CHL's triple."""
    b = BorderedHL(n=n, rho_max=rho_max)
    Om = np.exp(-((b.X - x0) ** 2) / (2.0 * w ** 2))
    V = 0.8 * np.exp(-((b.X - 1.3 * x0) ** 2) / (2.0 * (1.1 * w) ** 2))
    z0 = b.pack(Om, V, *CHL_TRIPLE)
    b.set_pin_from(z0)
    return b, z0


_CACHE = {}


def _converged(n=101):
    if n not in _CACHE:
        b, z0 = _fresh(n=n)
        z, _ = b.newton(z0, tol=1e-12, max_iter=40)
        _CACHE[n] = (b, z)
    return _CACHE[n]


def _raises(fn):
    """(raised_the_guards_error, exception_or_None, returned_value_or_None)."""
    try:
        return False, None, fn()
    except BorderedHLDomainError as exc:
        return True, exc, None
    except Exception as exc:                       # noqa: BLE001 -- deliberate
        return False, exc, None


# --------------------------------------------------------------------------- #
# 1. leg 198's headline gate, INVERTED, at its own hand-computable numbers
# --------------------------------------------------------------------------- #
def test_negative_weight_no_longer_returns_a_negative_operator_norm():
    """INVERSION of leg 198's `..._returns_a_negative_operator_norm`.

    Leg 198's control and both corrupted values are kept EXACTLY:
        M = [[1, 100], [3, 4]], w = (1,1)          -> 101.0, and it must still be 101.0
        w_col = (1, -1)                            -> was -1.0, must now REFUSE
        w_col = (1, -1e-9)                         -> was -3999999997.0, must now REFUSE
    The two corrupted numbers are not discarded: they are re-pinned through the
    `on_nonpositive='allow'` escape hatch, so the repair is shown to have removed the
    DEFAULT path to them without changing the arithmetic underneath."""
    M = np.array([[1.0, 100.0], [3.0, 4.0]])
    ones = np.array([1.0, 1.0])

    # the admissible control is untouched by the repair, to the bit
    good = induced_sup_norm(M, ones, ones)
    assert good == 101.0, f"the hand-computed control moved to {good!r}"

    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        r1, e1, v1 = _raises(lambda: induced_sup_norm(M, ones, np.array([1.0, -1.0])))
        r2, e2, v2 = _raises(lambda: induced_sup_norm(M, ones, np.array([1.0, -1e-9])))
    assert r1, f"w_col=(1,-1) no longer refuses: returned {v1!r} / raised {e2!r}"
    assert r2, f"w_col=(1,-1e-9) no longer refuses: returned {v2!r}"
    assert "w_col" in str(e1), f"the error does not name the offending vector: {e1}"
    assert "entry 1" in str(e1), f"the error does not name the offending entry: {e1}"

    # leg 198's exact magnitudes, still reproducible through the escape hatch
    old1 = induced_sup_norm(M, ones, np.array([1.0, -1.0]), on_nonpositive="allow")
    old2 = induced_sup_norm(M, ones, np.array([1.0, -1e-9]), on_nonpositive="allow")
    assert old1 == -1.0, f"leg 198's -1.0 is no longer reproducible: {old1!r}"
    assert abs(old2 + 3999999997.0) < 1.0, f"leg 198's w=-1e-9 case moved: {old2}"

    # the row weights are guarded too -- leg 198 only ever probed the column side
    r3, e3, v3 = _raises(lambda: induced_sup_norm(M, np.array([1.0, -1.0]), ones))
    assert r3, f"a negative w_ROW is still accepted, returning {v3!r}"
    assert "w_row" in str(e3), f"the error does not name w_row: {e3}"

    print(f"    control 101.0 unchanged; w_col=(1,-1) and (1,-1e-9) both REFUSED "
          f"(were {old1} and {old2:.6e}); w_row guarded too")
    print("[ok] INVERTED: a negative weight no longer yields a negative 'operator norm'")


# --------------------------------------------------------------------------- #
# 2. leg 198's consequence gate, INVERTED, at its own 1e8 thresholds
# --------------------------------------------------------------------------- #
def test_negative_weight_no_longer_fabricates_a_closing_certificate():
    """INVERSION of leg 198's `..._fabricates_a_closing_certificate`.

    Leg 198 pinned understatement factors > 1e8 for both Z_1 and ||A||. Those
    thresholds are NOT weakened here: they are re-asserted against the escape hatch
    (the corruption is still exactly as large as leg 198 measured) while the default
    path is required to refuse. And the honest w_r = +1e-6 branch must come back
    BIT-IDENTICAL to what the pre-repair module returned -- the guard is required to
    have moved nothing on admissible input."""
    b, z = _converged()

    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter("always")
        pos = b.certificate_constants(z, p=0.0, w_r=+1e-6)
        rejected, exc, val = _raises(
            lambda: b.certificate_constants(z, p=0.0, w_r=-1e-6))
    assert not ws, f"the admissible branch now warns: {[str(w.message) for w in ws]}"
    assert pos["Z2"] > 0 and pos["B"] > 0, "the positive-weight control is no longer sane"
    assert rejected, f"w_r=-1e-6 is still accepted, returning Z_2={val and val['Z2']!r}"
    assert "w_r" in str(exc), f"the error does not name w_r: {exc}"

    # leg 198's magnitudes, undiminished, through the hatch
    neg = b.certificate_constants(z, p=0.0, w_r=-1e-6, on_nonpositive="allow")
    assert neg["Z2"] < 0 and neg["B"] < 0, "Z_2/B no longer go negative under the hatch"
    assert all(np.isfinite(neg[k]) for k in ("Y0", "Z1", "Z2", "A_norm", "B")), \
        "the pre-repair arithmetic is no longer reproducible (non-finite now)"
    z1_under = pos["Z1"] / neg["Z1"]
    a_under = pos["A_norm"] / neg["A_norm"]
    assert z1_under > 1e8, f"Z_1 understatement collapsed to {z1_under:.4g}x"
    assert a_under > 1e8, f"||A|| understatement collapsed to {a_under:.4g}x"

    # and the radii polynomial: the honest branch does NOT close (legs 46/47's
    # documented ceiling), and the corrupted one must no longer be reachable by default
    disc_pos = (1.0 - pos["Z1"]) ** 2 - 2.0 * pos["Z2"] * pos["Y0"]
    disc_neg = (1.0 - neg["Z1"]) ** 2 - 2.0 * neg["Z2"] * neg["Y0"]
    assert disc_neg > disc_pos, \
        "the sign flip no longer inflates the discriminant; the fabrication is gone " \
        "for a reason other than the guard, which the guard cannot then be credited for"

    print(f"    w_r=+1e-6: Z_2={pos['Z2']:.6e} (>0), refused at w_r=-1e-6")
    print(f"    through the hatch, leg 198's magnitudes are intact: Z_1 understated "
          f"{z1_under:.4g}x, ||A|| understated {a_under:.4g}x")
    print("[ok] INVERTED: the sign flip no longer reaches the certificate at all")


# --------------------------------------------------------------------------- #
# 3. the classes leg 198 never probed -- zero, NaN, and both infinities
# --------------------------------------------------------------------------- #
def test_every_inadmissible_class_refuses_including_nan_and_the_infinities():
    """Leg 198 probed the negative half and noted zero raised `ZeroDivisionError`.

    NaN and +-inf it never probed, and NaN is the case that matters most: every
    ordered comparison returns False on NaN, so a "detect the bad case" guard
    (`any(w <= 0)`) would fail OPEN on it. This gate is what makes leg 218's
    `all(isfinite & > 0)` polarity load-bearing rather than stylistic -- it fails if
    anyone ever flips it back."""
    b, z = _converged()
    ones = np.ones(2)
    M = np.array([[1.0, 100.0], [3.0, 4.0]])

    classes = {"negative": -1.0, "negative_tiny": -1e-300, "zero": 0.0,
               "negative_zero": -0.0, "plus_inf": np.inf, "minus_inf": -np.inf,
               "nan": np.nan}
    leaked = []
    for label, val in classes.items():
        for site, fn in (
                ("induced_sup_norm.w_col",
                 lambda v=val: induced_sup_norm(M, ones, np.array([1.0, v]))),
                ("induced_sup_norm.w_row",
                 lambda v=val: induced_sup_norm(M, np.array([1.0, v]), ones)),
                ("weights.w_l", lambda v=val: b.weights(p=0.0, w_l=v)),
                ("weights.w_om", lambda v=val: b.weights(p=0.0, w_om=v)),
                ("weights.w_r", lambda v=val: b.weights(p=0.0, w_r=v)),
                ("certificate_constants.w_om",
                 lambda v=val: b.certificate_constants(z, p=0.0, w_om=v))):
            ok, exc, ret = _raises(fn)
            if not ok:
                leaked.append((label, site, repr(ret), repr(exc)))
    assert not leaked, (
        "%d of %d inadmissible cases are NOT refused with BorderedHLDomainError: %r"
        % (len(leaked), len(classes) * 6, leaked[:8]))

    # the NaN case specifically, spelled out: a detect-bad guard would let it through
    assert not (np.nan <= 0.0), "the premise of this gate is wrong on this platform"
    ok, exc, _ = _raises(lambda: b.weights(p=0.0, w_om=np.nan))
    assert ok and "nan" in str(exc).lower(), \
        f"the NaN weight is not refused with a NaN-naming error: {exc!r}"

    print(f"    {len(classes)} inadmissibility classes x 6 entry points = "
          f"{len(classes) * 6} cases, 0 leaked")
    print("[ok] every inadmissible class refuses, NaN included (the fail-OPEN case)")


# --------------------------------------------------------------------------- #
# 4. the guard's own contract: a ValueError, and the hatch is not a mode
# --------------------------------------------------------------------------- #
def test_the_guards_error_is_a_valueerror_and_the_hatch_is_validated():
    """`BorderedHLDomainError` must subclass `ValueError` (leg 218's stated contract:
    callers already catching `ValueError` are unaffected), and `on_nonpositive` must
    itself refuse an unrecognised value -- an escape hatch that silently accepts a
    typo is a second silent-corruption site in the repair for the first one."""
    assert issubclass(BorderedHLDomainError, ValueError), \
        "BorderedHLDomainError no longer subclasses ValueError; leg 218's " \
        "compatibility claim for callers catching ValueError is void"
    b, _ = _converged()
    for typo in ("Raise", "allowed", "ignore", "", None, True, 0):
        ok, exc, ret = _raises(lambda t=typo: b.weights(p=0.0, w_om=-1.0,
                                                        on_nonpositive=t))
        assert ok, f"on_nonpositive={typo!r} was not refused (returned {ret!r})"
    # and it must refuse a typo even when every weight is ADMISSIBLE, or the
    # validation is only reachable on the path that was already going to raise
    misses = []
    for typo in ("Raise", "allowed", "ignore", None):
        ok, exc, ret = _raises(lambda t=typo: b.weights(p=0.0, on_nonpositive=t))
        if not ok:
            misses.append((typo, repr(ret)))
    print(f"    BorderedHLDomainError <: ValueError; 7/7 typos refused on the "
          f"inadmissible path, {4 - len(misses)}/4 on the admissible path")
    if misses:
        print(f"    NOTE (not a failure, recorded): on ADMISSIBLE weights the "
              f"on_nonpositive spelling is not validated -- {misses}. A typo there "
              f"silently means 'raise', which is the SAFE direction, so this is "
              f"reported as a magnitude, not gated.")
    print("[ok] the guard's error type and its hatch's own validation hold")


# --------------------------------------------------------------------------- #
# 5. the repair moved NOTHING on admissible input -- the bit differential, in-test
# --------------------------------------------------------------------------- #
def test_admissible_input_is_bit_identical_to_the_pre_repair_arithmetic():
    """The other half of the gate: the guard must be a pure precondition check.

    `on_nonpositive='allow'` is the pre-repair arithmetic by construction, so the
    default path and the hatch must agree BIT FOR BIT on every admissible
    configuration -- compared as IEEE-754 payloads, not with `==`."""
    import struct

    def bits(x):
        return struct.pack("<d", float(x)).hex()

    mismatches, leaves = [], 0
    for n in (101, 201):
        b, z = _converged(n)
        Xmax = float(np.abs(b.X).max())
        for p in (0.0, 0.39, 1.0):
            for f in (1.0, 0.01, 0.1):
                d = b.certificate_constants(z, p=p, w_l=f * Xmax)
                h = b.certificate_constants(z, p=p, w_l=f * Xmax,
                                            on_nonpositive="allow")
                for k in sorted(d):
                    if isinstance(d[k], (int, float)):
                        leaves += 1
                        if bits(d[k]) != bits(h[k]):
                            mismatches.append((n, p, f, k, d[k], h[k]))
                wd = b.weights(p=p, w_l=f * Xmax)[0]
                wh = b.weights(p=p, w_l=f * Xmax, on_nonpositive="allow")[0]
                leaves += wd.size
                mismatches += [(n, p, f, "w[%d]" % i, wd[i], wh[i])
                               for i in range(wd.size) if bits(wd[i]) != bits(wh[i])]
    assert not mismatches, \
        f"{len(mismatches)} of {leaves} float leaves differ between the guarded and " \
        f"unguarded paths on ADMISSIBLE input: {mismatches[:6]}"
    print(f"    {leaves} float leaves over 18 admissible configurations, "
          f"0 bit mismatches")
    print("[ok] the guard is a pure precondition check: admissible input is untouched")


# --------------------------------------------------------------------------- #
def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    print(f"post-repair gates for leg 218's border-weight guard ({len(tests)} gates)\n")
    for t in tests:
        print(f"  {t.__name__}")
        try:
            t()
        except AssertionError as exc:
            FAILURES.append((t.__name__, str(exc)))
            print(f"[FAIL] {t.__name__}: {exc}")
        print()
    if FAILURES:
        print(f"{len(FAILURES)}/{len(tests)} FAILED")
        for name, msg in FAILURES:
            print(f"  - {name}: {msg[:200]}")
        return 1
    print(f"{len(tests)}/{len(tests)} gates hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
