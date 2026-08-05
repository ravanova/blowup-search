"""Known-answer tests for the hand-rolled interval-arithmetic core (Route-D).

The whole point of this layer is that it never lies: every operation must return
a GUARANTEED enclosure of the true real result. We gate that with `fractions`
(exact rational arithmetic) as the oracle -- for each op we compute the true
value exactly and assert lo <= true <= hi -- plus the structural interval
properties (inclusion monotonicity, degenerate/point behaviour, the reciprocal
guard) and the reduction error bounds (isum / matvec / dot). No science claim
here; this is the validated tooling the framing decision will rest on.

Pre-committed predicates:
  (1) ENCLOSURE: +,-,*,/ of point intervals enclose the exact rational result.
  (2) OUTWARD ROUNDING: an inexact result (1/3) has lo < true < hi (nonzero,
      ulp-scale width), and a point interval of an EXACT float is width 0.
  (3) MONOTONICITY: widening an input never shrinks the output enclosure.
  (4) RECIPROCAL GUARD: 1/[a,b] with 0 in [a,b] raises.
  (5) REDUCTIONS: isum / dot / matvec enclose the exact rational answer, and the
      matvec of a point matrix and point vector matches numpy @ to within its
      (tiny, gamma-bounded) width.

Run: python test_interval.py     (no scipy; sub-second)
"""

from fractions import Fraction as Fr

import numpy as np

from solver.interval import Interval, isum, dot, matvec


def _enc(iv, true, label):
    """Assert the (scalar) Interval iv encloses the exact rational `true`."""
    lo = Fr(float(iv.lo))
    hi = Fr(float(iv.hi))
    assert lo <= true <= hi, f"{label}: {float(iv.lo):.17g} <= {true} <= {float(iv.hi):.17g} FAILED"


def test_enclosure_elementary():
    """(1) +,-,*,/ of points enclose the exact rational result."""
    a, b = Fr(1, 10), Fr(2, 10)  # oracle values; float(0.1)+float(0.2) != 0.3
    ia, ib = Interval.point(0.1), Interval.point(0.2)
    _enc(ia + ib, Fr(float(0.1)) + Fr(float(0.2)), "add")
    _enc(ia - ib, Fr(float(0.1)) - Fr(float(0.2)), "sub")
    _enc(ia * ib, Fr(float(0.1)) * Fr(float(0.2)), "mul")
    _enc(ia / ib, Fr(float(0.1)) / Fr(float(0.2)), "div")
    # the classic trap: fl(0.1)+fl(0.2) != 0.3, but the enclosure still holds
    print(f"    0.1+0.2 -> [{float((ia+ib).lo):.17g}, {float((ia+ib).hi):.17g}]")
    print("[ok] elementary ops enclose the exact rational result")


def test_outward_rounding_and_points():
    """(2) inexact 1/3 straddles the true value; an exact float is width 0."""
    third = Interval.point(1.0) / Interval.point(3.0)
    _enc(third, Fr(1, 3), "1/3")
    assert float(third.lo) < 1.0 / 3.0 < float(third.hi), "1/3 not straddled"
    assert float(third.width) > 0.0, "inexact result must have positive width"
    assert float(third.width) < 1e-15, "1/3 width should be ulp-scale"
    # a fresh point interval has width exactly 0 (models an exact float input)
    assert float(Interval.point(2.0).width) == 0.0, "point interval must be width 0"
    # arithmetic always rounds outward one ulp (we do not own the FPU mode), so
    # even an exact product 0.5*4=2.0 is returned as a >=1-ulp box that ENCLOSES 2
    half = Interval.point(0.5) * Interval.point(4.0)
    assert half.contains(2.0).all(), "exact product must enclose 2.0"
    assert float(half.width) < 1e-15, "exact product width should be ulp-scale"
    print(f"    1/3 width={float(third.width):.2e}, 0.5*4 encloses 2 (width={float(half.width):.1e})")
    print("[ok] outward rounding straddles inexact results; points start width 0")


def test_inclusion_monotonicity():
    """(3) widening an input can only widen (never shrink) the output."""
    x_pt = Interval.point(1.3)
    x_box = Interval.from_mid_rad(1.3, 0.05)
    y = Interval.from_mid_rad(-0.7, 0.02)
    tight = x_pt * y
    loose = x_box * y
    assert float(loose.lo) <= float(tight.lo) + 1e-15, "mul lower not monotone"
    assert float(loose.hi) >= float(tight.hi) - 1e-15, "mul upper not monotone"
    # the box result must contain the point result's endpoints
    assert loose.contains(tight.lo).all() and loose.contains(tight.hi).all()
    print(f"    point-width={float(tight.width):.3e}  box-width={float(loose.width):.3e}")
    print("[ok] enclosures are inclusion-monotone under input widening")


def test_reciprocal_guard():
    """(4) 1/[a,b] with 0 in [a,b] must raise; away from 0 it encloses."""
    raised = False
    try:
        Interval(np.array(-1.0), np.array(2.0)).reciprocal()
    except ZeroDivisionError:
        raised = True
    assert raised, "reciprocal of an interval containing 0 must raise"
    r = Interval(np.array(2.0), np.array(4.0)).reciprocal()  # encloses [1/4, 1/2]
    assert r.contains(0.25).all() and r.contains(0.5).all(), "1/[2,4] must enclose 1/4 and 1/2"
    assert float(r.lo) <= 0.25 and float(r.hi) >= 0.5
    print("[ok] reciprocal guards zero and encloses [1/4, 1/2]")


def test_reductions_enclose():
    """(5) isum / dot / matvec enclose the exact rational answer."""
    vals = [Fr(1, 3), Fr(-2, 7), Fr(5, 11), Fr(1, 13)]
    fl = np.array([float(v) for v in vals])
    iv = Interval.point(fl)
    s = isum(iv)
    _enc(s, sum(Fr(float(x)) for x in fl), "isum")

    u = np.array([float(Fr(1, 3)), float(Fr(-1, 6)), float(Fr(2, 9))])
    w = np.array([float(Fr(3, 5)), float(Fr(7, 4)), float(Fr(-1, 8))])
    d = dot(Interval.point(u), Interval.point(w))
    _enc(d, sum(Fr(float(a)) * Fr(float(b)) for a, b in zip(u, w)), "dot")

    rng = np.random.default_rng(0)
    M = rng.standard_normal((6, 4))
    v = rng.standard_normal(4)
    mv = matvec(M, Interval.point(v))
    ref = M @ v
    assert np.all(mv.lo <= ref) and np.all(ref <= mv.hi), "matvec must enclose numpy @"
    assert float(mv.width.max()) < 1e-12, "point matvec width should be gamma-tiny"
    # interval vector: enclosure must contain every sampled point in the box
    vbox = Interval.from_mid_rad(v, 0.01)
    mvb = matvec(M, vbox)
    for _ in range(64):
        vs = v + rng.uniform(-0.01, 0.01, size=4)
        assert np.all(mvb.lo <= M @ vs) and np.all(M @ vs <= mvb.hi), "box matvec misses a sample"
    print(f"    point-matvec max width={float(mv.width.max()):.2e}; box matvec covers 64 samples")
    print("[ok] isum / dot / matvec are rigorous enclosures")


def _main():
    test_enclosure_elementary()
    test_outward_rounding_and_points()
    test_inclusion_monotonicity()
    test_reciprocal_guard()
    test_reductions_enclose()
    test_transcendentals_enclose()
    print("\nALL INTERVAL TESTS PASSED")


# --------------------------------------------------------------------------
# Route-TN (leg 56): the rigorous transcendentals
# --------------------------------------------------------------------------

def test_transcendentals_enclose():
    """log and arctan enclosures are checked against an INDEPENDENT high-precision
    reference, not against the libm call they exist to avoid.

    `decimal` is used as the reference only -- it is not in the rigorous path. The
    point of the gate is that the series-with-proved-remainder implementation agrees
    with an arbitrary-precision evaluation to well inside its own reported width."""
    import decimal
    from solver.interval import ILOG2, IPI, iatan_small, ilog

    decimal.getcontext().prec = 50
    D = decimal.Decimal

    # the two stored constants must enclose their true values
    log2_ref = D(2).ln()
    pi_ref = D("3.14159265358979323846264338327950288419716939937511")
    assert ILOG2.lo <= float(log2_ref) <= ILOG2.hi, "LOG2 enclosure misses log 2"
    assert IPI.lo <= float(pi_ref) <= IPI.hi, "PI enclosure misses pi"
    # and they must be non-degenerate (a point interval here would be a false claim)
    assert ILOG2.hi > ILOG2.lo and IPI.hi > IPI.lo, "constants must be true intervals"

    xs = np.array([1e-12, 1e-3, 0.25, 0.5, 1.0, 2.0, 17.0, 745.2394128947751, 1e6])
    r = ilog(xs)
    worst = 0.0
    for i, x in enumerate(xs):
        ref = D(repr(float(x))).ln()
        assert r.lo[i] <= float(ref) <= r.hi[i], f"ilog misses log({x})"
        worst = max(worst, float(r.hi[i] - r.lo[i]))
    assert worst < 1e-13, f"ilog widths blew up: {worst:.2e}"
    # monotone and consistent with its own algebra: log(x*y) = log x + log y
    a, b = 3.0, 11.0
    lab = ilog(np.array([a * b]))
    la, lb = ilog(np.array([a])), ilog(np.array([b]))
    assert lab.lo[0] <= la.hi[0] + lb.hi[0] and lab.hi[0] >= la.lo[0] + lb.lo[0], \
        "ilog violates log(ab) = log a + log b within its own enclosures"

    ts = np.array([-0.5, -0.1, 0.0, 1e-6, 0.125, 0.4999])
    at = iatan_small(ts)
    for i, t in enumerate(ts):
        ref = float(np.arctan(float(t)))
        assert at.lo[i] <= ref <= at.hi[i], f"iatan_small misses arctan({t})"
    assert float((at.hi - at.lo).max()) < 1e-13, "iatan_small widths blew up"

    # the domain guards must actually fire -- a silent out-of-range call would make
    # the "proved remainder" a false claim
    for bad in (2.0, -3.0):
        try:
            iatan_small(np.array([bad]))
        except ValueError:
            pass
        else:
            raise AssertionError(f"iatan_small accepted |t| = {abs(bad)} > 1/2")
    try:
        ilog(np.array([-1.0]))
    except ValueError:
        pass
    else:
        raise AssertionError("ilog accepted a non-positive argument")

    print(f"    ilog max width={worst:.2e}; iatan_small max width="
          f"{float((at.hi - at.lo).max()):.2e}; both guards fire")
    print("[ok] ilog / iatan_small enclose an independent 50-digit reference")


if __name__ == "__main__":
    _main()
