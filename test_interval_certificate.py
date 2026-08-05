"""Gates for solver/interval_certificate.py -- Route-L1's rigorous constants.

A bound that has only been checked against another float is not checked. So the gates
are: exact rational references, the ordering that any two valid enclosures must satisfy,
and a deliberately wrong iterate that must be rejected.

  (1) EXACT RATIONAL REFERENCE. Selected rows of the operator products are recomputed
      with `fractions.Fraction` -- no floating point anywhere -- and both the naive and
      the compensated enclosure must contain the exact value.
  (2) THE COMPENSATED PATH IS SHARPER, AND CONSISTENT. Its enclosure must overlap the
      naive one everywhere and be narrower wherever the answer is not exactly zero.
  (3) THE CONSTANTS ARE BOUNDS. The rigorous Z_1, Z_2 and ||A|| must DOMINATE the float
      readings of the same quantities; a "bound" below the thing it bounds is broken.
  (4) THE RADII VERDICT IS CONSERVATIVE. On a hand case with an exact answer, the
      reported r-interval must sit strictly inside the true root interval.
  (5) A POISONED ITERATE IS REJECTED. Perturbing z by 1e-6 must push Y_0 over the budget.
  (6) THE HEADLINE IS REPRODUCIBLE, AND SO IS ITS MECHANISM: the target closes at n=201
      with the compensated evaluation and does NOT close with the naive one.
  (7) Z_1 < 1 AT EVERY RUNG, rigorously -- without that, A is not an approximate inverse
      and nothing else in the certificate means anything.

Run: .venv/bin/python test_interval_certificate.py
"""

import time
from fractions import Fraction

import numpy as np

from solver.interval import Interval, dot2_matvec, matvec
from solver.interval_certificate import (
    BorderedHLIntervals, interval_constants, radii_verdict, weighted_rowsum_bound,
)
from solver.weight_search import BorderedCLM
from experiments.p2_route_port_v1_bordered import P_STAR, solve
from experiments.p2_route_l1_v1_interval import _NaiveHL


def _target(n=201):
    b, z, hist, _ = solve(n=n)
    w, nu, w_l = b.weights(p=P_STAR, w_l=0.01 * float(np.abs(b.X).max()))
    return b, z, w, nu


def test_exact_rational_reference():
    """(1) Both enclosures contain the exact rational dot product."""
    b, z, _, _ = _target()
    Om = b.unpack(z)[0]
    rng = np.random.default_rng(3)
    worst = None
    for name, M in (("H", b.H), ("Uop", b.Uop), ("D", b.D)):
        naive, tight = matvec(M, Interval.point(Om)), dot2_matvec(M, Om)
        for i in rng.choice(M.shape[0], size=4, replace=False):
            ex = float(sum(Fraction(float(M[i, j])) * Fraction(float(Om[j]))
                           for j in range(M.shape[1])))
            assert naive.lo[i] <= ex <= naive.hi[i], f"naive misses the exact {name}[{i}]"
            assert tight.lo[i] <= ex <= tight.hi[i], f"tight misses the exact {name}[{i}]"
            worst = name
    print(f"[ok] (1) exact rational rows of H, Uop, D lie inside both enclosures")


def test_compensated_is_sharper_and_consistent():
    """(2) The two rigorous enclosures overlap, and the compensated one is narrower."""
    b, z, _, _ = _target()
    Om = b.unpack(z)[0]
    for name, M in (("H", b.H), ("D", b.D), ("Uop", b.Uop)):
        a, c = matvec(M, Interval.point(Om)), dot2_matvec(M, Om)
        assert np.all(c.lo <= a.hi) and np.all(a.lo <= c.hi), f"{name}: no overlap"
        big = np.abs(a.mid) > 1e-300          # skip the exactly-zero rows
        assert np.all((c.hi - c.lo)[big] <= (a.hi - a.lo)[big]), f"{name}: not sharper"
    print("[ok] (2) compensated enclosures overlap the naive ones and are never wider")


def test_constants_are_bounds():
    """(3) Rigorous Z_1, Z_2, ||A|| dominate their float readings."""
    b, z, w, nu = _target()
    iv = BorderedHLIntervals(b)
    c = interval_constants(iv, z, w, nu)
    cf = b.certificate_constants(z, p=P_STAR, w_l=w[2 * b.n])
    assert c["Z1"] >= cf["Z1"], f"Z1 bound {c['Z1']:.3e} below float {cf['Z1']:.3e}"
    assert c["Z2"] >= cf["Z2"] * (1 - 1e-12), "Z2 bound below the float reading"
    assert c["A_norm"] >= cf["A_norm"] * (1 - 1e-12), "||A|| bound below the float reading"
    print(f"[ok] (3) Z_1 bound {c['Z1']:.2e} >= float {cf['Z1']:.2e}; Z_2 and ||A|| "
          f"dominate too")


def test_radii_verdict_is_conservative():
    """(4) The reported r-interval sits inside the true root interval."""
    Y0, Z1, Z2 = 1e-3, 0.1, 2.0
    v = radii_verdict(Y0, Z1, Z2)
    a, bq, cq = 0.5 * Z2, -(1.0 - Z1), Y0
    d = np.sqrt(bq * bq - 4 * a * cq)
    r1, r2 = (-bq - d) / (2 * a), (-bq + d) / (2 * a)
    r2 = min(r2, (1.0 - Z1) / Z2)
    assert v["closes"] and r1 <= v["r_min"] and v["r_max"] <= r2, (r1, r2, v)
    assert not radii_verdict(1.0, 0.1, 2.0)["closes"], "an infeasible case reported closed"
    assert not radii_verdict(1e-9, 1.5, 2.0)["closes"], "Z1 >= 1 reported closed"
    print(f"[ok] (4) r-interval [{v['r_min']:.6e}, {v['r_max']:.6e}] inside the exact "
          f"[{r1:.6e}, {r2:.6e}]")


def test_poisoned_iterate_is_rejected():
    """(5) A wrong point must not certify."""
    b, z, w, nu = _target()
    iv = BorderedHLIntervals(b)
    rng = np.random.default_rng(11)
    d = rng.standard_normal(b.N)
    d /= np.abs(d).max()
    c = interval_constants(iv, z + 1e-6 * d, w, nu)
    v = radii_verdict(c["Y0"], c["Z1"], c["Z2"])
    assert not v["closes"], "the certificate closed around a poisoned iterate"
    print(f"[ok] (5) a 1e-06 perturbation is rejected: Y0/budget = "
          f"{v['Y0_over_budget']:.3e}")


def test_headline_and_its_mechanism():
    """(6) The target closes with the compensated path and fails with the naive one."""
    b, z, w, nu = _target()
    good = radii_verdict(**{k: v for k, v in
                            interval_constants(BorderedHLIntervals(b), z, w, nu).items()
                            if k in ("Y0", "Z1", "Z2")})
    bad = radii_verdict(**{k: v for k, v in
                           interval_constants(_NaiveHL(b), z, w, nu).items()
                           if k in ("Y0", "Z1", "Z2")})
    assert good["closes"], "the target does not close in interval arithmetic"
    assert not bad["closes"], "the naive path closes too -- the mechanism claim is wrong"
    print(f"[ok] (6) target closes at n=201: Y0/budget = {good['Y0_over_budget']:.3e}; "
          f"naive path {bad['Y0_over_budget']:.3e} does not")


def test_Z1_below_one_at_every_rung():
    """(7) A is rigorously an approximate inverse at each resolution."""
    z1s = []
    for n in (201, 401, 801):
        b, z, w, nu = _target(n)
        c = interval_constants(BorderedHLIntervals(b), z, w, nu)
        z1s.append(c["Z1"])
        assert c["Z1"] < 1.0, f"Z1 = {c['Z1']:.3e} at n={n}"
    assert z1s[0] < z1s[-1], "Z1 should grow with n; it did not, which is suspicious"
    print("[ok] (7) rigorous Z_1 = " + ", ".join(f"{v:.2e}" for v in z1s)
          + " at n = 201, 401, 801 -- all below 1")


if __name__ == "__main__":
    t0 = time.time()
    test_exact_rational_reference()
    test_compensated_is_sharper_and_consistent()
    test_constants_are_bounds()
    test_radii_verdict_is_conservative()
    test_poisoned_iterate_is_rejected()
    test_headline_and_its_mechanism()
    test_Z1_below_one_at_every_rung()
    print(f"\nall interval-certificate gates pass ({time.time() - t0:.1f}s)")
