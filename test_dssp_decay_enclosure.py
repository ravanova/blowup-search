"""Tests for solver/dssp_decay_enclosure.py — the certified far-field decay enclosure.

Self-running, per this repository's convention:  .venv/bin/python test_dssp_decay_enclosure.py

The tests are organised around the one property that matters and is easy to fake.
An enclosure is only worth anything if it is SOUND (the truth is never outside it)
and NON-VACUOUS (it is not the whole search bracket) and DIRECTION-SENSITIVE (it
says EMPTY on mismatches and does not say EMPTY on knowns).  All three are checked,
plus the adversarial cases where a sloppy implementation would silently lie: a
profile touching zero, an exponent outside the search bracket, a window reaching
below r = 1, and the monotonicity of the tolerance parameter that would otherwise
be a free knob.
"""

import numpy as np

from solver.dssp_decay_enclosure import (
    VERDICT_EMPTY, VERDICT_INCAPACITY, VERDICT_INTERVAL,
    certified_decay_from_cell_enclosures, certified_decay_interval,
    critical_tolerance, ipow_half_integer, isqrt,
    planted_curvature, planted_log_corrected, planted_perturbed,
    planted_power_law, planted_rational_cutoff, planted_two_power,
    radial_field_fn,
)
from solver.interval import Interval

R0, R1 = 10.0, 1000.0


def test_isqrt_and_half_integer_powers_enclose():
    """The one added primitive, and the power it is there to build."""
    x = Interval(np.array([2.0, 9.0, 1e-3]), np.array([2.0, 9.0, 1e-3]))
    s = isqrt(x)
    assert np.all(s.lo <= np.sqrt([2.0, 9.0, 1e-3])), "isqrt lower endpoint is not a bound"
    assert np.all(np.sqrt([2.0, 9.0, 1e-3]) <= s.hi), "isqrt upper endpoint is not a bound"
    for p in (0.0, 0.5, 1.0, 2.5, 3.0, 4.5):
        r = np.array([1.5, 10.0, 733.0])
        got = ipow_half_integer(Interval(r, r), p)
        truth = r ** p
        assert np.all(got.lo <= truth) and np.all(truth <= got.hi), \
            f"ipow_half_integer failed to enclose at p={p}"
    for bad in (0.3, -1.0):
        try:
            ipow_half_integer(Interval(np.array([2.0]), np.array([2.0])), bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"ipow_half_integer accepted p={bad}")
    print("[ok] isqrt and half-integer powers enclose; non-half-integers rejected")


def test_soundness_exact_power_laws_contain_the_truth():
    """SOUNDNESS: for an exact power law the true exponent is inside, always.

    Checked across exponents (including a half-integer, to catch integer snapping),
    across cell counts, and in BOTH modes.  A single miss here would invalidate the
    whole instrument, so it is checked densely rather than once."""
    for C, p0 in [(3.0, 1.0), (1.0, 2.0), (0.25, 2.5), (7.0, 3.0), (1e-3, 0.5)]:
        iv_fn, _ = planted_power_law(C, p0)
        for n in (17, 50, 200, 1000):
            for mode in ("cells", "nodes"):
                r = certified_decay_interval(iv_fn, R0, R1, n, mode=mode)
                assert r["verdict"] == VERDICT_INTERVAL, \
                    f"C={C} p0={p0} N={n} {mode}: verdict {r['verdict']}, expected INTERVAL"
                assert r["p_lo"] <= p0 <= r["p_hi"], \
                    f"C={C} p0={p0} N={n} {mode}: truth outside [{r['p_lo']}, {r['p_hi']}]"
    print("[ok] exact power laws: truth enclosed at every exponent, cell count and mode")


def test_non_vacuous_and_tight():
    """NON-VACUOUS: the enclosure is not the search bracket wearing a hat."""
    iv_fn, _ = planted_power_law(1.0, 2.0)
    r = certified_decay_interval(iv_fn, R0, R1, 1000)
    assert r["p_lo"] > 0.0 and r["p_hi"] < 12.0, "enclosure reaches the search bracket"
    assert r["width"] < 1e-10, f"width {r['width']:.3e} is far above the rounding floor"
    assert r["n_dropped"] < r["n_pairs"], "every constraint pair was dropped"
    print(f"[ok] non-vacuous: width {r['width']:.3e} inside bracket [0, 12], "
          f"{r['n_dropped']}/{r['n_pairs']} pairs dropped")


def test_mismatched_controls_are_certified_empty():
    """DIRECTION SENSITIVITY, half one: mismatches must fire.

    These are leg 382's pre-registered gate controls plus its resolving-power probe.
    An instrument that cannot fail is a tautology (leg 340), so this is the test that
    earns the module its keep."""
    cases = [
        ("two-power mixture", planted_two_power(1.0, 2.0, 0.01, 1.0)),
        ("rational far cutoff", planted_rational_cutoff(1.0, 2.0, 300.0, 4)),
        ("log correction", planted_log_corrected(1.0, 2.0)),
        ("curvature kappa=1e-4", planted_curvature(1.0, 2.0, 1e-4, float(np.log(100.0)))),
    ]
    for name, (iv_fn, _) in cases:
        r = certified_decay_interval(iv_fn, R0, R1, 1000)
        assert r["verdict"] == VERDICT_EMPTY, \
            f"{name}: verdict {r['verdict']}, expected EMPTY — the control did not fire"
        assert r["p_lo"] > r["p_hi"], f"{name}: EMPTY without a contradiction gap"
        print(f"     {name}: EMPTY, contradiction gap {r['p_lo'] - r['p_hi']:.6f}")
    print("[ok] every planted mismatch is certified EMPTY, with a positive gap")


def test_emptiness_is_direction_sensitive():
    """DIRECTION SENSITIVITY, half two: knowns must NOT fire.

    The mirror of the previous test. An instrument that says EMPTY for everything is
    exactly as useless as one that never does."""
    for C, p0 in [(3.0, 1.0), (1.0, 2.0), (0.25, 2.5), (7.0, 3.0)]:
        r = certified_decay_interval(planted_power_law(C, p0)[0], R0, R1, 1000)
        assert r["verdict"] != VERDICT_EMPTY, f"exact power law p0={p0} certified EMPTY"
    print("[ok] no exact power law is certified EMPTY")


def test_zero_tolerance_rejects_any_perturbation():
    """The leg-382 finding, pinned as a regression so it cannot be forgotten.

    At delta = 0 the certified set is EMPTY for ANY perturbation, down to 1e-12.
    This is mathematically correct — a perturbed power law has no exact exponent —
    and it is precisely why the tolerance parameter exists.  If a future change made
    this test pass by returning an INTERVAL, the instrument would have stopped being
    an enclosure of the set it documents."""
    for eps in (1e-12, 1e-9, 1e-3):
        r = certified_decay_interval(planted_perturbed(1.0, 2.0, eps, R1)[0],
                                     R0, R1, 200)
        assert r["verdict"] == VERDICT_EMPTY, \
            f"eps={eps}: verdict {r['verdict']}; the exact set of a perturbed profile is empty"
    print("[ok] zero tolerance rejects every perturbation (1e-12 included), as documented")


def test_tolerance_is_monotone_and_recovers_the_truth():
    """The tolerance must be a bound the caller owes, not a knob that fits anything.

    Two properties make that checkable: widening delta can only ENLARGE the feasible
    set (so widths are non-decreasing and EMPTY is downward-closed), and pairing
    delta to a profile's own perturbation size recovers the truth."""
    iv_fn, _ = planted_power_law(1.0, 2.0)
    widths = []
    for d in (0.0, 1e-9, 1e-6, 1e-3, 1e-2):
        r = certified_decay_interval(iv_fn, R0, R1, 200, rel_tolerance=d)
        assert r["verdict"] == VERDICT_INTERVAL and r["p_lo"] <= 2.0 <= r["p_hi"]
        widths.append(r["width"])
    assert all(b >= a for a, b in zip(widths, widths[1:])), \
        f"certified width is not monotone in the tolerance: {widths}"

    for eps in (1e-9, 1e-6, 1e-3):
        r = certified_decay_interval(planted_perturbed(1.0, 2.0, eps, R1)[0],
                                     R0, R1, 200, rel_tolerance=eps)
        assert r["verdict"] == VERDICT_INTERVAL, f"eps=delta={eps}: {r['verdict']}"
        assert r["p_lo"] <= 2.0 <= r["p_hi"], f"eps=delta={eps}: truth not recovered"

    try:
        certified_decay_interval(iv_fn, R0, R1, 50, rel_tolerance=-1e-9)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative tolerance was accepted")
    print(f"[ok] tolerance monotone {widths[0]:.2e} -> {widths[-1]:.2e}, truth recovered "
          "when delta matches eps, negatives rejected")


def test_critical_tolerance_separates_controls_from_knowns():
    """delta* is the number that makes the instrument reportable: how accurately a
    profile must be known before a given mismatch can still be excluded."""
    lo_c1, _ = critical_tolerance(planted_two_power(1.0, 2.0, 0.01, 1.0)[0], R0, R1, 200, iters=30)
    lo_c2, _ = critical_tolerance(planted_rational_cutoff(1.0, 2.0, 300.0, 4)[0], R0, R1, 200, iters=30)
    lo_k2, hi_k2 = critical_tolerance(planted_power_law(1.0, 2.0)[0], R0, R1, 200, iters=30)
    assert lo_k2 == 0.0 and hi_k2 == 0.0, "an exact power law has a nonzero delta*"
    assert lo_c1 > 1e-2, f"two-power delta* {lo_c1:.4g} is implausibly small"
    assert lo_c2 > lo_c1, "the far cutoff should be easier to exclude than the mixture"
    print(f"[ok] delta*: two-power {lo_c1:.4g}, cutoff {lo_c2:.4g}, exact power law 0")


def test_exponent_outside_the_bracket_is_incapacity_not_empty():
    """The honesty case. A power law at p = 13 is a perfectly good power law; the
    bracket [0, 12] simply cannot see it. Reporting EMPTY there would assert that no
    exponent exists, which is false."""
    iv_fn, _ = planted_power_law(1.0, 13.0)
    r = certified_decay_interval(iv_fn, R0, R1, 200)
    assert r["verdict"] == VERDICT_INCAPACITY, \
        f"p0=13 outside bracket gave {r['verdict']}, expected INCAPACITY"
    assert "NOT a statement that the profile has no power-law exponent" in r["reason"]
    wide = certified_decay_interval(iv_fn, R0, R1, 200, p_bracket=(0.0, 20.0))
    assert wide["verdict"] == VERDICT_INTERVAL and wide["p_lo"] <= 13.0 <= wide["p_hi"], \
        "widening the bracket did not recover the exponent"
    print(f"[ok] p0=13 -> INCAPACITY under [0,12]; recovered as "
          f"[{wide['p_lo']:.12f}, {wide['p_hi']:.12f}] under [0,20]")


def test_adversarial_inputs_are_refused_or_reported_not_silently_wrong():
    """A profile enclosure touching zero, and a window reaching below r = 1."""
    lo = np.array([100.0, 200.0])
    hi = np.array([200.0, 400.0])
    r = certified_decay_from_cell_enclosures(lo, hi, np.array([0.0, 1e-3]),
                                             np.array([1.0, 1e-2]))
    assert r["verdict"] == VERDICT_INCAPACITY and "zero" in r["reason"], \
        "a profile enclosure touching zero was not reported as INCAPACITY"

    try:
        certified_decay_from_cell_enclosures(np.array([0.5]), np.array([2.0]),
                                             np.array([1.0]), np.array([2.0]))
    except ValueError as exc:
        assert "r > 1" in str(exc)
    else:
        raise AssertionError("a window reaching below r = 1 was accepted")

    try:
        certified_decay_interval(planted_power_law(1.0, 2.0)[0], R0, R1, 50, mode="magic")
    except ValueError:
        pass
    else:
        raise AssertionError("an unknown mode was accepted")
    print("[ok] zero-touching enclosure -> INCAPACITY; r<=1 window and bad mode -> ValueError")


def test_cell_entry_point_agrees_with_the_callable_entry_point():
    """The API a future profile-producing unit will actually use must give the same
    answer as the callable path, or the two would drift apart unnoticed."""
    iv_fn, _ = planted_power_law(1.0, 2.0)
    n = 200
    edges = np.geomspace(R0, R1, n + 1)
    F = iv_fn(Interval(edges[:-1], edges[1:]))
    direct = certified_decay_from_cell_enclosures(edges[:-1], edges[1:], F.lo, F.hi)
    through = certified_decay_interval(iv_fn, R0, R1, n, mode="cells")
    assert direct["verdict"] == through["verdict"]
    assert direct["p_lo"] == through["p_lo"] and direct["p_hi"] == through["p_hi"], \
        "the cell-enclosure entry point disagrees with the callable entry point"
    print("[ok] cell-enclosure and callable entry points agree exactly")


def test_radial_field_lift_matches_the_scalar_profile():
    """The fitted and certified columns must be measurements of ONE object."""
    _, float_fn = planted_power_law(2.0, 2.5)
    field = radial_field_fn(float_fn)
    e = np.array([0.4, 0.5, np.sqrt(1.0 - 0.16 - 0.25)])
    e = e / np.linalg.norm(e)
    rs = np.array([11.0, 97.0, 640.0])
    mags = np.linalg.norm(field(rs[:, None] * e[None, :]), axis=-1)
    assert np.allclose(mags, float_fn(rs), rtol=1e-14), \
        "the 3D lift does not reproduce the scalar magnitude"
    print("[ok] the 3D field lift has |V| = f(r) to 1e-14, so fitted and certified "
          "see one profile")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)}/{len(tests)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
