"""Leg 69 / Route-IA: the size- and conditioning-matched soundness gates for solver/interval.py.

`test_interval.py` already gates the interval core, but its corpus is small: the largest matrix
is 6x4 and the longest accumulation is 4 terms.  The certificate stack that legs 58 and 61 run
uses K up to 128 -- accumulations of 129 to 258 terms -- against an operator whose tail-block
diagonal is EXACTLY zero, so the rows cancel catastrophically.  This file gates that regime.

READ THIS BEFORE TRUSTING `dot2_matvec`.  Leg 69 measured, against exact rational ground truth,
that the compensated matvec is SOUND in the normal range and UNSOUND in the subnormal range.
Both facts are pinned here, the second one deliberately as a passing "characterization" test
rather than a failing one, so that the boundary cannot move without this file noticing:

  * `test_normal_range_soundness` -- the certificate's own regime.  Enclosures STRICTLY contain
    the exact rational value; no case merely touches an endpoint.
  * `test_subnormal_range_is_KNOWN_UNSOUND` -- below ~1e-140 input scale, `dot2_matvec` and
    `matvec` both return enclosures that EXCLUDE the exact value.  The test asserts the defect's
    two containing properties: the escape is ABSOLUTE (a few units of eta = 2^-1074), never
    relative, and the failure band lies far below anything the live operators reach.
  * `test_dekker_split_overflow_is_KNOWN_SILENT` -- above |entry| = 2^997, Dekker's splitting
    overflows and `dot2_matvec` returns a NaN enclosure WITHOUT RAISING, because the `Interval`
    constructor's `lo <= hi` guard is vacuous on NaN.
  * `test_live_operators_are_far_from_both_bands` -- the quantitative reason the two defects do
    not reach leg 58's or leg 61's numbers.

If a future leg repairs `solver/interval.py` (adding Rump's eta term to the reductions and an
overflow guard to the splitting), the two KNOWN_ defects here are expected to start failing.
That is the intended signal: flip them to soundness assertions at that point.  Do not weaken
them to make a repair look unnecessary.
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


def test_subnormal_range_is_KNOWN_UNSOUND():
    """(3) CHARACTERIZATION OF A KNOWN DEFECT -- see this file's docstring.

    The Ogita-Rump-Oishi bound `u|x.y| + gamma_m^2 |x||y|` that `dot2_matvec` implements is
    purely RELATIVE and carries no absolute term, and the classic `gamma_m` bound behind
    `matvec` is stated for the normal range only.  Rump's underflow-aware restatement (BIT 2012)
    adds an eta term precisely for this.  Neither is present here, so once the accumulation lands
    in the subnormal range both reductions can return an enclosure that EXCLUDES the answer.

    This test asserts the defect is exactly as characterized -- and, critically, that its escape
    is ABSOLUTE (bounded in units of eta) rather than relative, which is what confines it."""
    rng = np.random.default_rng(1074)
    fails = 0
    total = 0
    worst_escape_eta = 0.0
    for e in (-150, -155, -160):
        for _ in range(25):
            M, v = _cancelled(rng, 1, 32, 1.0)
            M = M * (10.0 ** e)
            v = v * (10.0 ** e)
            ex = _exact(M, v)
            r = dot2_matvec(M, v)
            for i in range(M.shape[0]):
                L, H = Fr(float(r.lo[i])), Fr(float(r.hi[i]))
                s = min(ex[i] - L, H - ex[i])
                total += 1
                if s < 0:
                    fails += 1
                    worst_escape_eta = max(worst_escape_eta, float(-s / Fr(ETA)))
    assert fails > 0, ("the subnormal defect did NOT reproduce -- if solver/interval.py was "
                       "repaired, flip this test into a soundness assertion")
    assert worst_escape_eta < 1e3, (
        f"the subnormal escape grew to {worst_escape_eta:.3g} eta; it was characterized at a few "
        "eta and being ABSOLUTE is the whole reason it cannot reach the certificate's regime")
    print(f"    {fails}/{total} false negatives in the subnormal band (input scale 1e-150 to "
          f"1e-160); worst escape {worst_escape_eta:.3g} eta = "
          f"{worst_escape_eta * ETA:.3g} absolute")
    print("[KNOWN DEFECT] dot2_matvec/matvec are UNSOUND below ~1e-140 input scale")


def test_dekker_split_overflow_is_KNOWN_SILENT():
    """(4) CHARACTERIZATION OF A KNOWN DEFECT.  Dekker's splitting multiplies by 2^27+1 before
    splitting, so it overflows for large operands and returns a NaN error term.  `dot2_matvec`
    then produces a NaN enclosure and RAISES NOTHING: `Interval.__init__`'s `np.any(lo > hi)`
    guard is vacuously satisfied by NaN."""
    e_crit = None
    for e in range(900, 1024):
        _, err = _two_product(np.array([2.0 ** e]), np.array([1.0]))
        if not np.isfinite(err[0]):
            e_crit = e
            break
    assert e_crit is not None, "Dekker splitting no longer overflows -- was it guarded?"
    r = dot2_matvec(np.array([[2.0 ** e_crit]]), np.array([1.0]))
    silent = bool(np.isnan(r.lo[0]) and np.isnan(r.hi[0]))
    assert silent, ("dot2_matvec no longer returns a silent NaN -- if an overflow guard was "
                    "added, flip this test into a raises-assertion")
    print(f"    Dekker split loses its error term at |a| >= 2^{e_crit} = {2.0 ** e_crit:.3g}; "
          f"dot2_matvec returns [nan, nan] with no exception")
    print("[KNOWN DEFECT] dot2_matvec NaNs silently above |entry| = 2^997")


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
    test_subnormal_range_is_KNOWN_UNSOUND()
    test_dekker_split_overflow_is_KNOWN_SILENT()
    test_live_operators_are_far_from_both_bands()
    print("\nALL INTERVAL STRESS GATES PASSED "
          "(two KNOWN DEFECTS characterized, not repaired -- see the module docstring)")


if __name__ == "__main__":
    _main()
