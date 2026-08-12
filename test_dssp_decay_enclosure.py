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
    HYP_BOTH, HYP_EXACT_INTERVAL, HYP_MODULUS, HYP_MONOTONE,
    HYP_NODES_ONLY, HYP_UNDECLARED,
    certified_decay_from_cell_enclosures, certified_decay_interval,
    critical_tolerance, cutoff_admissible_delta_window,
    ipow_half_integer, isqrt, predicted_width,
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


# ---------------------------------------------------------------------------
# leg 386 (Route-DTOL) additions — ADDITIVE ONLY.  Nothing above is weakened or
# removed; in particular `test_zero_tolerance_rejects_any_perturbation` is a correct
# pinned finding of leg 382 and must keep passing exactly as written.
# ---------------------------------------------------------------------------

def test_delta_is_recorded_on_every_code_path():
    """Leg 389 consumes these rows.  A row whose tolerance is implicit is a trap, so
    `rel_tolerance` must appear on EVERY return path — including the incapacity paths,
    where leg 382's version silently dropped it."""
    iv_fn, _ = planted_power_law(1.0, 2.0)
    for d in (0.0, 1e-6, 1e-1):
        for mode in ("cells", "nodes"):
            r = certified_decay_interval(iv_fn, R0, R1, 50, mode, (0.0, 12.0), d)
            assert r["rel_tolerance"] == d, f"{mode} at delta={d}: tolerance not recorded"
            assert r["tolerance_mode"] == ("exact" if d == 0.0 else "relative")

    # (a) incapacity by an enclosure that reaches zero
    zero_fn = lambda R: iv_fn(R) - iv_fn(R)          # noqa: E731
    r = certified_decay_interval(zero_fn, R0, R1, 20, "cells", (0.0, 12.0), 3e-3)
    assert r["verdict"] == VERDICT_INCAPACITY and r["rel_tolerance"] == 3e-3, \
        "the zero-crossing INCAPACITY path dropped the tolerance"
    # (b) incapacity by an exponent outside the search bracket
    out_fn, _ = planted_power_law(1.0, 13.0)
    r = certified_decay_interval(out_fn, R0, R1, 50, "cells", (0.0, 12.0), 1e-3)
    assert r["verdict"] == VERDICT_INCAPACITY and r["rel_tolerance"] == 1e-3, \
        "the out-of-bracket INCAPACITY path dropped the tolerance"
    # (c) the EMPTY path
    r = certified_decay_interval(planted_log_corrected(1.0, 2.0)[0], R0, R1, 50,
                                 "cells", (0.0, 12.0), 1e-3)
    assert r["verdict"] == VERDICT_EMPTY and r["rel_tolerance"] == 1e-3, \
        "the EMPTY path dropped the tolerance"
    print("[ok] delta is recorded on every path: interval, empty, and both incapacities")


def test_width_law_matches_the_closed_form_and_is_a_window_property():
    """PRE-REGISTERED (leg 386 PART I §2.1): width = 4 log(1+delta)/log(R1/R0).

    The consequence a consumer must not miss is that the coefficient belongs to the
    WINDOW: halving the log-window in decades DOUBLES the certified width at the same
    tolerance.  Leg 382's measured 0.8686 is 4/log(100), not an instrument constant."""
    iv_fn, _ = planted_power_law(1.0, 2.0)
    for r0, r1 in ((10.0, 1000.0), (10.0, 100.0)):
        for d in (1e-9, 1e-6, 1e-3, 1e-1):
            r = certified_decay_interval(iv_fn, r0, r1, 200, "cells", (0.0, 12.0), d)
            pred = predicted_width(d, r0, r1)
            assert r["verdict"] == VERDICT_INTERVAL
            assert 0.95 <= r["width"] / pred <= 1.05, \
                f"width law off band on [{r0},{r1}] at delta={d}: {r['width']/pred}"
            assert abs(r["predicted_width_exact_power_law"] - pred) < 1e-18
    w_long = certified_decay_interval(iv_fn, 10.0, 1000.0, 200, "cells", (0.0, 12.0), 1e-3)["width"]
    w_short = certified_decay_interval(iv_fn, 10.0, 100.0, 200, "cells", (0.0, 12.0), 1e-3)["width"]
    assert abs(w_short / w_long - 2.0) < 0.01, \
        f"the window-doubling prediction failed: ratio {w_short/w_long}"
    print(f"[ok] width law = 4 log(1+d)/log(R1/R0); shortening the window doubles it "
          f"({w_short/w_long:.6f}x, predicted 2)")


def test_delta_star_matches_the_chebyshev_closed_form():
    """PRE-REGISTERED (leg 386 PART I §2.2): delta* = exp(E_inf(phi)) - 1, with E_inf the
    Chebyshev best-affine error of the profile's departure from a power law in the log-log
    plane.  Measured delta* must sit within 20% and BELOW the continuum value, because the
    cell enclosure is slightly wider than the exact tube."""
    for name, pair, pred in (
            ("two-power", planted_two_power(1.0, 2.0, 0.01, 1.0), 0.318807),
            ("rational cutoff", planted_rational_cutoff(1.0, 2.0, 300.0, 4), 3.454378),
            ("log correction", planted_log_corrected(1.0, 2.0), 0.077025)):
        lo, hi = critical_tolerance(pair[0], R0, R1, 200, "cells", (0.0, 12.0), iters=45)
        assert 0.80 <= lo / pred <= 1.0, f"{name}: delta* {lo} off the closed form {pred}"
    print("[ok] delta* matches exp(E_inf(phi)) - 1 within 20%, and from below")


def test_cutoff_window_is_empty_exactly_when_the_centre_fails_the_threshold():
    """CLAY_OBLIGATIONS §4's composed condition, as a property rather than a table.

    The tolerance buys ZERO headroom on the alpha threshold: the window is non-empty iff
    the realised certified centre exceeds the threshold.  Checked in both directions on a
    profile whose centre is strictly between the two thresholds §4 cares about."""
    iv_fn, _ = planted_log_corrected(1.0, 1.5)          # realised centre ~ 1.2624
    lo = cutoff_admissible_delta_window(iv_fn, R0, R1, 1.0, n_cells=200, iters=35)
    assert lo["admissible"] and lo["width"] > 0.5, \
        f"expected a window above threshold 1: {lo}"
    assert lo["alpha_centre"] > 1.0
    hi = cutoff_admissible_delta_window(iv_fn, R0, R1, 1.5, n_cells=200, iters=35)
    assert not hi["admissible"] and hi["delta_min"] is None, \
        f"expected EMPTY above threshold 3/2: {hi}"
    ac = lo["alpha_centre"]
    just_above = cutoff_admissible_delta_window(iv_fn, R0, R1, ac * (1 + 1e-6),
                                                n_cells=200, iters=35)
    assert not just_above["admissible"], \
        "a threshold just above the realised centre must give an EMPTY window"
    print(f"[ok] cutoff window non-empty iff centre ({ac:.6f}) exceeds the threshold; "
          f"width {lo['width']:.6f} at threshold 1, EMPTY at 3/2")


def test_hypothesis_is_recorded_on_every_code_path():
    """STANDING RULE (DM cycle 11g): every output row carries the hypothesis in force.

    A certificate-without-hypothesis is no certificate -- leg 385's control X3 planted a
    SECRET monotonicity violation and produced a certificate of width
    7.438494264988549e-15, bit-indistinguishable from the true certificate of the genuine
    known K1.  Nothing inside the certificate separates them; only this field does.  So
    it is checked on the SAME four code paths delta is checked on, plus the composed
    window, and an omitted hypothesis must come back UNDECLARED rather than absent."""
    fields = ("hypothesis", "hypothesis_detail", "conditional_on")
    iv_fn, _ = planted_power_law(1.0, 2.0)

    # 1. interval, 2. empty, 3. incapacity (bracket), all via the cells path
    rows = [certified_decay_interval(iv_fn, R0, R1, 100, "cells", (0.0, 12.0), 0.0),
            certified_decay_interval(planted_log_corrected(1.0, 2.0)[0], R0, R1, 100,
                                     "cells", (0.0, 12.0), 0.0),
            certified_decay_interval(iv_fn, R0, R1, 100, "cells", (5.0, 12.0), 0.0)]
    for r in rows:
        for f in fields:
            assert f in r, f"{f} missing from a {r['verdict']} row"
        assert r["hypothesis"] == HYP_EXACT_INTERVAL, r["hypothesis"]
        assert r["conditional_on"] and "DISCHARGED" in r["conditional_on"]

    # 4. the nodes mode must SAY it is nodes-only, in the row and not just the docstring
    nodes = certified_decay_interval(iv_fn, R0, R1, 100, "nodes", (0.0, 12.0), 0.0)
    assert nodes["hypothesis"] == HYP_NODES_ONLY, nodes["hypothesis"]
    assert "NO CELL HYPOTHESIS" in nodes["conditional_on"]

    # 5. the zero-crossing incapacity path, which is the one that dropped rel_tolerance
    zero = certified_decay_from_cell_enclosures([10.0, 20.0], [20.0, 40.0],
                                                [0.0, 1.0], [1.0, 2.0])
    assert zero["verdict"] == VERDICT_INCAPACITY
    assert zero["hypothesis"] == HYP_UNDECLARED, zero["hypothesis"]

    # 6. an omitted hypothesis is recorded as UNDECLARED and SAYS it is not a certificate
    bare = certified_decay_from_cell_enclosures([10.0, 20.0], [20.0, 40.0],
                                                [1.0, 0.25], [1.0, 0.25])
    assert bare["hypothesis"] == HYP_UNDECLARED
    assert "no certificate" in bare["conditional_on"]

    # 7. a declared upstream hypothesis passes through unmodified, detail included
    passed = certified_decay_from_cell_enclosures(
        [10.0, 20.0], [20.0, 40.0], [1.0, 0.25], [1.0, 0.25],
        hypothesis=HYP_BOTH, hypothesis_detail="declared by the adapter under test")
    assert passed["hypothesis"] == HYP_BOTH
    assert "declared by the adapter under test" in passed["conditional_on"]
    assert "NOT verified here" in passed["conditional_on"]

    # 8. the composed window is exactly as conditional as the rows it composes
    win = cutoff_admissible_delta_window(iv_fn, R0, R1, 1.0, n_cells=100, iters=25)
    for f in fields:
        assert f in win, f"{f} missing from a composed-window row"
    assert win["hypothesis"] == HYP_EXACT_INTERVAL
    print("[ok] hypothesis recorded on all 8 paths; omitted -> UNDECLARED, never absent")


def test_hypothesis_strings_match_the_adapter():
    """The MONOTONE / MODULUS / BOTH strings are duplicated from leg 385's samples->cells
    adapter so the dependency points one way (adapter -> enclosure).  Duplication drifts;
    this pins it, and fails loudly if leg 385's module renames one."""
    try:
        from solver import dssp_decay_samples as adapter
    except ImportError:                                  # pragma: no cover
        print("[skip] solver/dssp_decay_samples.py absent; nothing to pin against")
        return
    for ours, theirs in ((HYP_MONOTONE, "HYP_MONOTONE"),
                         (HYP_MODULUS, "HYP_MODULUS"),
                         (HYP_BOTH, "HYP_BOTH")):
        assert ours == getattr(adapter, theirs), \
            f"hypothesis string drift: ours {ours!r} vs adapter's {getattr(adapter, theirs)!r}"
    print("[ok] hypothesis strings byte-identical to the leg-385 adapter's")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"\n{len(tests)}/{len(tests)} passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
