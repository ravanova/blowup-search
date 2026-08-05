"""Leg 69 / Route-IA: the size- and conditioning-matched soundness gates for solver/interval.py.

`test_interval.py` already gates the interval core, but its corpus is small: the largest matrix
is 6x4 and the longest accumulation is 4 terms.  The certificate stack that legs 58 and 61 run
uses K up to 128 -- accumulations of 129 to 258 terms -- against an operator whose tail-block
diagonal is EXACTLY zero, so the rows cancel catastrophically.  This file gates that regime.

READ THIS BEFORE TRUSTING `dot2_matvec`.  Leg 69 measured, against exact rational ground truth,
that the compensated matvec was SOUND in the normal range and UNSOUND in the subnormal range,
and that Dekker's splitting produced a silent NaN enclosure above |entry| = 2^997.  Both defects
were repaired in `solver/interval.py` under `bench/fix-interval-subnormal-nan` (Rump's absolute
eta term added to `isum`/`matvec`/`dot2_matvec`; an OverflowError raised from `_two_product`; the
`Interval` constructor's containment guard made to fail closed on NaN).  As leg 69's technical
note instructed, the two characterization tests below have been FLIPPED into the soundness
assertions they were placeholders for:

  * `test_normal_range_soundness` -- the certificate's own regime.  Enclosures STRICTLY contain
    the exact rational value; no case merely touches an endpoint.
  * `test_subnormal_range_is_SOUND` -- was `test_subnormal_range_is_KNOWN_UNSOUND`.  Across the
    whole band leg 69 measured failing (input scales 1e-150 to 1e-160, where the products straddle
    the normal/subnormal boundary), `dot2_matvec` and `matvec` must now CONTAIN the exact rational
    value in every case: zero false negatives, where leg 69 measured 62 in 1680 with a worst
    escape of 6.58 eta = 3.25e-323.
  * `test_dekker_split_overflow_raises` -- was `test_dekker_split_overflow_is_KNOWN_SILENT`.
    Above |entry| = 2^997 the splitting must RAISE OverflowError, and a NaN endpoint must be
    rejected by the `Interval` constructor rather than passing its guard vacuously.
  * `test_live_operators_are_far_from_both_bands` -- the quantitative reason neither defect ever
    reached leg 58's or leg 61's numbers (the repair is a soundness widening at the extremes,
    bit-for-bit inert in the live operating range of entries 0.5 to 128).

Do not weaken these to make a future change look harmless.
"""

import warnings
from fractions import Fraction as Fr

import numpy as np

from solver.interval import Interval, dot2_matvec, isum, matvec, _two_product

ETA = 2.0 ** -1074

warnings.simplefilter("ignore")


# --------------------------------------------------------------------------

def _cancel_row(row, v):
    """Two exact-float columns that cancel the row's exact dot product to ~1e-32 relative.

    The head/tail (h, l) of the exact rational dot product are themselves exact floats, so
    appending (-h, -l) against v-entries 1.0 keeps ALL data exactly representable -- which is
    what makes the Fraction ground truth exact rather than approximate."""
    S = sum(Fr(row[j]) * Fr(v[j]) for j in range(len(v)))
    h = float(S)
    return np.array([-h, -float(S - Fr(h))], dtype=float)


def _cancelled(rng, n_rows, m, scale):
    M = rng.standard_normal((n_rows, m))
    v = rng.standard_normal(m) * scale
    ext = np.array([_cancel_row(M[i], v) for i in range(n_rows)])
    return np.concatenate([M, ext], axis=1), np.concatenate([v, [1.0, 1.0]])


def _exact(M, v):
    return [sum(Fr(M[i, j]) * Fr(v[j]) for j in range(M.shape[1]))
            for i in range(M.shape[0])]


def _slack(lo, hi, ex):
    """(strictly_contained, relative slack) against the exact rational `ex`."""
    L, H = Fr(float(lo)), Fr(float(hi))
    s = min(ex - L, H - ex)
    w = H - L
    return s > 0, (float(s / w) if w > 0 else 0.0)


# --------------------------------------------------------------------------

def test_normal_range_soundness():
    """(1) At the certificate's own sizes and conditioning, every enclosure STRICTLY dominates
    the exact rational value -- including rows driven to ~1e-32 relative cancellation."""
    rng = np.random.default_rng(69)
    worst = 1.0
    n = 0
    for m in (32, 128, 258):
        for scale in (1e-8, 1.0, 1e8):
            M, v = _cancelled(rng, 4, m, scale)
            ex = _exact(M, v)
            for reduce_name, r in (("dot2_matvec", dot2_matvec(M, v)),
                                   ("matvec", matvec(M, Interval.point(v)))):
                for i in range(M.shape[0]):
                    strict, rel = _slack(r.lo[i], r.hi[i], ex[i])
                    assert strict, (f"{reduce_name} lost the exact value at m={m}, "
                                    f"scale={scale:.0e}, row {i}")
                    worst = min(worst, rel)
                    n += 1
    # accumulation reduction at the same lengths
    for m in (32, 128, 258):
        x = rng.standard_normal(m)
        S = sum(Fr(t) for t in x)
        h = float(S)
        xx = np.concatenate([x, [-h, -float(S - Fr(h))]])
        r = isum(Interval.point(xx))
        strict, rel = _slack(r.lo, r.hi, sum(Fr(t) for t in xx))
        assert strict, f"isum lost the exact value at m={m}"
        worst = min(worst, rel)
        n += 1
    print(f"    {n} normal-range cases, m up to 260; worst relative slack {worst:.4f} "
          f"(0.5 = dead centre, 0 = touching an endpoint)")
    print("[ok] normal range: enclosures strictly dominate the exact rational value")


def test_tail_block_conditioning():
    """(2) The LIVE bordered linearization -- whose tail diagonal is EXACTLY zero, the leg 51-53
    conditioning -- carried through both reductions at K up to 128."""
    from solver.spectral_certificate import bordered_linearization
    rng = np.random.default_rng(51)
    worst = 1.0
    n = 0
    for K in (16, 64, 128):
        M = np.asarray(bordered_linearization(K), dtype=float)
        v = rng.standard_normal(M.shape[1])
        ext = np.array([_cancel_row(M[i], v) for i in range(M.shape[0])])
        M2 = np.concatenate([M, ext], axis=1)
        v2 = np.concatenate([v, [1.0, 1.0]])
        ex = _exact(M2, v2)
        for r in (dot2_matvec(M2, v2), matvec(M2, Interval.point(v2))):
            for i in range(M2.shape[0]):
                strict, rel = _slack(r.lo[i], r.hi[i], ex[i])
                assert strict, f"lost the exact value on the live operator at K={K}, row {i}"
                worst = min(worst, rel)
                n += 1
    print(f"    {n} cases on the live zero-diagonal operator, K in 16..128; "
          f"worst relative slack {worst:.4f}")
    print("[ok] tail-block conditioning: no enclosure loses the answer")


def test_subnormal_range_is_SOUND():
    """(3) SOUNDNESS IN THE SUBNORMAL BAND -- the repaired form of leg 69's defect 1.

    The Ogita-Rump-Oishi bound `u|x.y| + gamma_m^2 |x||y|` that `dot2_matvec` implements is
    purely RELATIVE, and the classic `gamma_m` bound behind `matvec` is stated for the normal
    range only.  Once the products land in the subnormal range those terms underflow to zero
    while the true rounding error stays ABSOLUTE, at a few eta -- leg 69 measured 62 false
    negatives in 1680 cases at scales 1e-150...1e-160, worst escape 6.58 eta.  Rump's
    underflow-aware restatement (BIT Numer. Math. 2012) closes it with an explicit eta term, and
    `solver/interval.py` now carries that term (2 eta per product for the plain reductions, 8 eta
    per product for the compensated one).

    This test sweeps the whole measured failure band, WIDER than the band that failed, through
    BOTH reductions, and requires containment of the exact rational value in every case."""
    rng = np.random.default_rng(1074)
    fails = []
    total = 0
    worst_escape_eta = 0.0
    for e in (-145, -150, -155, -160, -165):
        for _ in range(20):
            M, v = _cancelled(rng, 1, 32, 1.0)
            M = M * (10.0 ** e)
            v = v * (10.0 ** e)
            ex = _exact(M, v)
            for name, r in (("dot2_matvec", dot2_matvec(M, v)),
                            ("matvec", matvec(M, Interval.point(v)))):
                for i in range(M.shape[0]):
                    L, H = Fr(float(r.lo[i])), Fr(float(r.hi[i]))
                    s = min(ex[i] - L, H - ex[i])
                    total += 1
                    if s < 0:
                        fails.append((name, e, float(-s / Fr(ETA))))
                        worst_escape_eta = max(worst_escape_eta, float(-s / Fr(ETA)))
    assert not fails, (
        f"{len(fails)}/{total} subnormal-band false negatives, worst escape "
        f"{worst_escape_eta:.3g} eta -- the absolute (eta) term in solver/interval.py no longer "
        f"dominates the underflow rounding.  First few: {fails[:5]}")
    print(f"    0/{total} false negatives across input scales 1e-145 to 1e-165, both reductions "
          f"(leg 69 measured 62/1680 here, worst escape 6.58 eta = 3.25e-323)")
    print("[ok] subnormal band: the absolute eta term restores containment")


def test_dekker_split_overflow_raises():
    """(4) LOUD FAILURE AT THE DEKKER WALL -- the repaired form of leg 69's defect 2.

    Dekker's splitting multiplies by 2^27+1 before splitting, so it overflows for |operand| >=
    2^997 = 1.34e300 and its error term goes NaN.  That NaN is MANUFACTURED by the module's own
    arithmetic with no rigorous error term behind it, so it must now RAISE.  A NaN that arrives
    in CALLER data instead (interval_certificate.full_interpolant_hilbert_matrix deliberately
    leaves its two endpoint rows NaN and masks them off) must widen to the trivial enclosure
    [-inf, +inf].  Either way a NaN endpoint is never STORED, because both `lo > hi` and
    `lo <= hi` are False on NaN and the old `np.any(lo > hi)` guard was therefore vacuous."""
    e_crit = None
    for e in range(900, 1024):
        try:
            _, err = _two_product(np.array([2.0 ** e]), np.array([1.0]))
        except OverflowError:
            e_crit = e
            break
        assert np.isfinite(err[0]), (f"_two_product returned a non-finite error term at 2^{e} "
                                     "instead of raising")
    assert e_crit is not None, "the Dekker splitting overflow guard never fired below 2^1024"
    assert e_crit == 997, f"the Dekker wall moved to 2^{e_crit}; leg 69 measured it at 2^997"
    try:
        dot2_matvec(np.array([[2.0 ** e_crit]]), np.array([1.0]))
        raise AssertionError("dot2_matvec returned an enclosure at the Dekker wall instead of "
                             "raising -- a silent NaN enclosure passes every containment check")
    except OverflowError:
        pass
    # one decade below the wall the compensated path still works normally
    r = dot2_matvec(np.array([[2.0 ** (e_crit - 1)]]), np.array([1.0]))
    assert np.isfinite(r.lo[0]) and np.isfinite(r.hi[0]) and r.lo[0] <= 2.0 ** 996 <= r.hi[0]
    # and the constructor never STORES a NaN endpoint: it widens to the trivial
    # enclosure, which is useless but valid and cannot be mistaken for a tight bound
    for bad in ((np.nan, np.nan), (np.nan, 1.0), (0.0, np.nan)):
        w = Interval(np.array([bad[0]]), np.array([bad[1]]))
        assert not np.isnan(w.lo[0]) and not np.isnan(w.hi[0]), f"NaN endpoint stored: {bad}"
        assert w.lo[0] == -np.inf and w.hi[0] == np.inf, f"NaN endpoint not widened: {bad}"
        assert bool(w.contains(0.0)) and bool(w.contains(1e300)), "trivial enclosure must contain"
    # a NaN reaching dot2_matvec through CALLER data (interval_certificate's
    # full_interpolant_hilbert_matrix leaves its two endpoint rows NaN on purpose)
    # must widen, not raise -- only a MANUFACTURED overflow raises
    rn = dot2_matvec(np.array([[np.nan, 1.0], [2.0, 3.0]]), np.array([1.0, 1.0]))
    assert rn.lo[0] == -np.inf and rn.hi[0] == np.inf, "NaN input row did not widen"
    assert np.isfinite(rn.lo[1]) and rn.lo[1] <= 5.0 <= rn.hi[1], "clean row was damaged"
    print(f"    |entry| >= 2^{e_crit} = {2.0 ** e_crit:.3g} raises OverflowError from the Dekker "
          f"split; 2^{e_crit - 1} still encloses; NaN endpoints widen to [-inf, +inf], "
          f"never stored, and a NaN input row does not damage its neighbours")
    print("[ok] the Dekker overflow wall fails loudly, not silently")


def test_live_operators_are_far_from_both_bands():
    """(5) The magnitudes that CONFINE the two defects: how far the operators legs 58 and 61
    actually feed to dot2_matvec sit from the subnormal band and from the Dekker overflow."""
    from solver.spectral_certificate import bordered_linearization
    lo_bound = np.inf
    hi_bound = 0.0
    for K in (16, 64, 128):
        A = np.abs(np.asarray(bordered_linearization(K), dtype=float))
        nz = A[A > 0]
        lo_bound = min(lo_bound, float(nz.min()))
        hi_bound = max(hi_bound, float(nz.max()))
    # the subnormal band starts around 1e-140; the Dekker overflow at 1.3e300
    assert lo_bound > 1e-100, f"a live operator entry reached {lo_bound:.3g}, near the eta band"
    assert hi_bound < 1e290, f"a live operator entry reached {hi_bound:.3g}, near the Dekker wall"
    dec_lo = np.log10(lo_bound) - (-140.0)
    dec_hi = np.log10(1.34e300) - np.log10(hi_bound)
    print(f"    live nonzero entries span {lo_bound:.3g} to {hi_bound:.3g}: "
          f"{dec_lo:.0f} decades above the subnormal failure band, "
          f"{dec_hi:.0f} decades below the Dekker overflow wall")
    print("[ok] both known defects are far outside the live certificate regime")


def _main():
    test_normal_range_soundness()
    test_tail_block_conditioning()
    test_subnormal_range_is_SOUND()
    test_dekker_split_overflow_raises()
    test_live_operators_are_far_from_both_bands()
    print("\nALL INTERVAL STRESS GATES PASSED "
          "(leg 69's two defects repaired and now gated as soundness assertions)")


if __name__ == "__main__":
    _main()
