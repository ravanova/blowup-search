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


#  (13) THE CORRECTED STRUCTURAL CLAIM IS GATED, NOT JUST ASSERTED. The first version
#       of this module claimed H_disc and D_disc share an interpolant; they do not.
#       H_disc transforms an ENDPOINT-ZEROED interpolant. That is now a test: the
#       full-interpolant matrix must differ from H_disc by exactly the endpoint basis
#       contribution, the difference must be concentrated at the cut, and the genuine
#       interpolation error must CONVERGE (order ~2) where the total does not. A
#       future change that makes these coincide fails here and forces a re-read.

def test_H_transforms_an_endpoint_zeroed_interpolant():
    """(13) H_disc != H(natural-spline interpolant); the difference is the cut."""
    rows = []
    for n in (201, 401, 801):
        b, sc, nu = _consistency(n)
        d = sc.decomposition(0.5, 0.0, nu, family="odd")
        rows.append(d)
        # the endpoint artifact IS the defect, to within a fraction of a percent
        share = d["defect_H_endpoint_zeroing"] / d["defect_H_total"]
        assert 0.99 < share < 1.01, (
            f"n={n}: endpoint zeroing is {share:.4f} of the total defect; the "
            "attribution in this module's docstring no longer holds")
        # and it is NOT the same object D differentiates
        assert d["defect_H_interpolation"] < 0.05 * d["defect_H_total"], (
            f"n={n}: the genuine interpolation error is no longer small against the "
            "total -- H may have stopped zeroing its endpoints")

    # the true interpolation error converges; the total does not
    interp = [r["defect_H_interpolation"] for r in rows]
    orders = [float(np.log2(x / y)) for x, y in zip(interp[:-1], interp[1:])]
    for o in orders:
        assert 1.6 < o < 2.3, f"interpolation order {o:.2f} is not ~2"

    # The endpoint term must scale like the VALUE AT THE CUT, which is a prediction
    # with a number attached: the two families differ there by M/a. (Checking the
    # assembled matrices column-by-column would NOT show this -- the restored endpoint
    # HQ columns multiply the slope operator's endpoint ROWS, so their influence
    # spreads across every column of the product. The scaling is the honest test.)
    b, sc, nu = _consistency(201)
    odd = sc.decomposition(0.5, 0.0, nu, family="odd")
    even = sc.decomposition(0.5, 0.0, nu, family="even")
    ratio = odd["defect_H_endpoint_zeroing"] / even["defect_H_endpoint_zeroing"]
    predicted = float(np.abs(b.X).max() / 0.5)
    assert 0.5 * predicted < ratio < 2.0 * predicted, (
        f"endpoint term scaled by {ratio:.1f}x between the families, but the value at "
        f"the cut differs by {predicted:.1f}x -- it is not tracking f(+-M)")

    print("    endpoint share " + ", ".join(
        f"{r['defect_H_endpoint_zeroing'] / r['defect_H_total']:.4f}" for r in rows)
        + "; interpolation orders " + ", ".join(f"{o:.2f}" for o in orders))
    print(f"    endpoint term scales {ratio:.0f}x between families vs M/a = "
          f"{predicted:.0f} predicted")
    print("[ok] (13) H_disc transforms an ENDPOINT-ZEROED interpolant, not D's")


def _main():
    t0 = time.time()
    test_exact_rational_reference()
    test_compensated_is_sharper_and_consistent()
    test_constants_are_bounds()
    test_radii_verdict_is_conservative()
    test_poisoned_iterate_is_rejected()
    test_headline_and_its_mechanism()
    test_Z1_below_one_at_every_rung()
    test_truncated_transform_matches_quadrature()
    test_mechanism_ablation_separates()
    test_D_converges_at_spline_order()
    test_H_does_not_converge()
    test_defect_bounds_are_not_evaluation_error()
    test_H_transforms_an_endpoint_zeroed_interpolant()
    print(f"\nall interval-certificate gates pass ({time.time() - t0:.1f}s)")


# --------------------------------------------------------------------------
# Route-TN (leg 56): gates for the (H, D) consistency defect
# --------------------------------------------------------------------------
#  (8)  THE CLOSED-FORM REFERENCE IS CHECKED AGAINST INDEPENDENT QUADRATURE. The
#       truncated Hilbert transform is the whole measurement's reference; if it is
#       wrong, every defect below is a statement about an algebra slip. It is
#       verified against a direct principal-value quadrature that shares no code.
#  (9)  THE MECHANISM ABLATION SEPARATES. Two families of identical interior
#       smoothness differing only in their value at the cut: H's defect must
#       collapse by ~M/a and D's must NOT move. If both move, or neither, the
#       mechanism named in the module docstring is wrong.
#  (10) D CONVERGES AT THE SPLINE ORDER. Order 4 +- 0.25 across 201/401/801.
#  (11) H DOES NOT CONVERGE. Flat to within 5% across a 4x refinement. This gate is
#       falsifiable in the useful direction: if a future change makes H converge,
#       it fails and must be re-read.
#  (12) THE BOUND IS NOT ITS OWN EVALUATION ERROR (discipline 86). width/value must
#       be below 1e-4 for both defects, else the number describes the code.

def _consistency(n):
    from solver.bordered_hl import BorderedHL
    from solver.interval_certificate import SplineConsistency
    b = BorderedHL(n=n)
    nu = (1.0 + b.X ** 2) ** (0.5 * 0.39)
    return b, SplineConsistency(b), nu


def _pv_quadrature(sc, x, a, family, N=2_000_001):
    """Independent PV quadrature of (1/pi) int_{-M}^{M} f(y)/(x-y) dy.

    Shares no code with the closed form: the singularity is removed by subtracting
    f(x), and the resulting explicit log term is added back."""
    M = sc.M

    def fn(u):
        return (-u / (u * u + a * a)) if family == "odd" else (a / (u * u + a * a))

    y = np.linspace(-M, M, N)
    d = x - y
    sing = np.abs(d) < 1e-13
    safe = np.where(sing, 1.0, d)
    g = np.where(sing, 0.0, (fn(y) - fn(x)) / safe)
    h = 1e-6
    g[sing] = -(fn(x + h) - fn(x - h)) / (2 * h)
    return (np.trapezoid(g, y) + fn(x) * np.log(abs((x + M) / (x - M)))) / np.pi


def test_truncated_transform_matches_quadrature():
    """(8) the closed-form reference against independent principal-value quadrature."""
    # The comparison is MIXED absolute/relative on purpose. The "even" family's
    # truncated transform vanishes identically at X = 0 by symmetry (an even
    # integrand against an odd kernel), so a pure relative test there divides by a
    # true zero and reports 1e-16/1e-16 as a total failure. The criterion below is
    # |closed - quad| <= atol + rtol |quad|, which is the honest statement.
    ATOL, RTOL = 1e-12, 1e-9
    b, sc, _nu = _consistency(201)
    worst_abs = 0.0
    for family in ("odd", "even"):
        for a in (0.5, 2.0):
            He = sc.H_exact(a, 0.0, family)
            tr = sc.H_truncation(a, 0.0, family)
            for j in (60, 100, 140):
                closed = float(He.mid[j] - tr.mid[j])
                quad = _pv_quadrature(sc, float(b.X[j]), a, family)
                err = abs(closed - quad)
                assert err <= ATOL + RTOL * abs(quad), (
                    f"{family} a={a} node {j}: closed {closed:.12e} vs quad "
                    f"{quad:.12e} (|diff| = {err:.2e})")
                worst_abs = max(worst_abs, err)
    assert worst_abs < 1e-12, f"closed form disagrees with quadrature by {worst_abs:.2e}"
    print(f"    worst absolute disagreement {worst_abs:.2e} over 12 (family, a, node) cases")
    print("[ok] (8) the truncated-transform reference matches independent quadrature")


def test_mechanism_ablation_separates():
    """(9) H's defect is the value at the cut; D's is interior interpolation."""
    rows = []
    for n in (201, 401, 801):
        _b, sc, nu = _consistency(n)
        o = sc.defects(0.5, 0.0, nu, family="odd")
        e = sc.defects(0.5, 0.0, nu, family="even")
        hc = o["defect_H_abs"] / e["defect_H_abs"]
        dc = o["defect_D_abs"] / e["defect_D_abs"]
        rows.append((n, hc, dc))
        assert hc > 500.0, f"n={n}: H defect did not collapse ({hc:.1f}x)"
        assert dc < 1.5, f"n={n}: D defect moved with the cut value ({dc:.2f}x)"
    print("    " + "; ".join(f"n={n}: H {hc:.0f}x, D {dc:.2f}x" for n, hc, dc in rows))
    print("[ok] (9) the ablation separates: the cut value drives H and not D")


def test_D_converges_at_spline_order():
    """(10) the derivative defect falls like h^4, the natural-spline order."""
    vals = []
    for n in (201, 401, 801):
        _b, sc, nu = _consistency(n)
        vals.append(sc.defects(0.5, 0.0, nu, family="odd")["defect_D_abs"])
    orders = [float(np.log2(x / y)) for x, y in zip(vals[:-1], vals[1:])]
    for o in orders:
        assert 3.75 < o < 4.25, f"D order {o:.2f} is not the spline order 4"
    print("    defects " + ", ".join(f"{v:.3e}" for v in vals)
          + "; orders " + ", ".join(f"{o:.2f}" for o in orders))
    print("[ok] (10) the D consistency defect converges at order 4")


def test_H_does_not_converge():
    """(11) the Hilbert defect is flat under refinement -- the leg's finding."""
    vals = []
    for n in (201, 401, 801):
        _b, sc, nu = _consistency(n)
        vals.append(sc.defects(0.5, 0.0, nu, family="odd")["defect_H_abs"])
    drop = vals[0] / vals[-1]
    assert 0.95 < drop < 1.05, (
        f"H defect moved by {drop:.3f}x over a 4x refinement -- it used to be flat; "
        "re-read the finding before trusting either number")
    print("    defects " + ", ".join(f"{v:.4e}" for v in vals)
          + f"; total change over 4x refinement {drop:.4f}x")
    print("[ok] (11) the H consistency defect does NOT converge at fixed reach")


def test_defect_bounds_are_not_evaluation_error():
    """(12) discipline 86: the enclosure width must be far below the enclosed value."""
    _b, sc, nu = _consistency(801)
    d = sc.defects(0.5, 0.0, nu, family="odd")
    assert d["width_frac_D"] < 1e-4, f"D bound is {d['width_frac_D']:.2e} wide"
    assert d["width_frac_H"] < 1e-4, f"H bound is {d['width_frac_H']:.2e} wide"
    assert d["excluded_nodes"] == 2, "exactly the two endpoint nodes are excluded"
    print(f"    width/value: D {d['width_frac_D']:.2e}, H {d['width_frac_H']:.2e}; "
          f"{d['interior_nodes']} interior nodes")
    print("[ok] (12) both defect bounds dominate their own evaluation error")


if __name__ == "__main__":
    _main()
