"""Gates for solver/collocation_newton.py -- the profile in the bounds' own basis.

  (1) THE VELOCITY INTEGRALS.  I_k(theta) = int_0^theta sin(kt)/(1+cos t) dt is
      computed by a recursion whose homogeneous solutions grow like k, so the
      gate checks it against TWO independent things: the closed forms at k = 0, 1
      and a direct quadrature at larger k -- and measures the float64 error the
      longdouble assembly is there to avoid.
  (2) THE a = 0 REDUCTION + THE OFF-NODE EVALUATOR.  With a = 0 the module must
      reproduce solver/decay_collocation exactly, and the exact anchor -- a
      degree-1 trigonometric polynomial which solves the equation identically --
      must have zero residual not only on the nodes but BETWEEN them.  That is
      the only gate the off-node evaluator gets, and it is a strong one.
  (3) THE JACOBIAN is the derivative it claims to be, WITH the a-term (finite
      differences on a non-anchor profile).
  (4) THE CERTIFICATE'S OWN SYSTEM.  Newton on [gauge row ; DF rows except one]
      with c fixed drives every row it enforces to machine zero, and at a = 0
      returns the exact anchor.
  (5) THE SAME OBJECT, BUILT TWICE (banked lesson 3).  The critical radius and
      the order of the profile's zero there must agree between this compactified
      theta-collocation build and the independent sinh-rho build in
      solver/profile_newton -- compared through the DILATION-INVARIANT X_c / c,
      since the two solves gauge different members of the same family.
  (6) THE DEFECT DOES NOT VANISH WITH THE RESIDUAL.  Zero at the nodes is not
      zero as a function: the interpolant's residual off the nodes, and at the
      one row the gauge displaced, must be reported and must be nonzero at a > 0.

Run: .venv/bin/python test_collocation_newton.py
"""

import numpy as np

from solver.collocation_newton import (ACollocation, critical_radius,
                                       effective_speed, refined_theta,
                                       velocity_integrals, weighted_defect,
                                       zero_order)
from solver.decay_collocation import Collocation

J = 200


def test_1_velocity_integrals():
    th = np.array([0.3, 1.0, 2.0, 3.0])
    I = velocity_integrals(th, 24)
    assert np.allclose(I[:, 0], 0.0)
    assert np.allclose(I[:, 1], np.log(2.0 / (1.0 + np.cos(th))), rtol=1e-14)

    # independent quadrature: dt/(1+cos t) = dX with X = tan(t/2), so
    # I_k = int_0^X sin(2k arctan X') dX' -- no singular integrand anywhere.
    def quad(theta, k, n=400001):
        xs = np.linspace(0.0, np.tan(0.5 * theta), n)
        return float(np.trapezoid(np.sin(2 * k * np.arctan(xs)), xs))

    worst = max(abs(I[j, k] - quad(th[j], k)) / max(1.0, abs(I[j, k]))
                for j in range(4) for k in (2, 5, 11, 23))
    assert worst < 5e-8, worst

    f64 = velocity_integrals(np.array([3.1]), 800, dtype=np.float64)
    f80 = velocity_integrals(np.array([3.1]), 800)
    drift = float(np.max(np.abs(f64 - f80)))
    assert drift < 1e-5 and drift > 1e-12, drift        # real, and worth avoiding
    print("[ok] (1) I_k: closed forms exact, quadrature agrees to %.1e; the "
          "float64 recursion drifts %.1e by k=800 (hence longdouble)"
          % (worst, drift))


def test_2_a0_reduction_and_offnode():
    col, ref = ACollocation(J, a=0.0), Collocation(J)
    om = ref.anchor()
    assert np.allclose(col.residual_a(om, 0.5), ref.residual(om, 0.5), atol=0, rtol=0)
    assert np.allclose(col.jacobian_a(om, 0.5), ref.jacobian_matrix(om, 0.5))

    nodal = float(np.max(np.abs(col.residual_a(om, 0.5))))
    th = refined_theta(J, refine=8)
    R, parts = col.interpolant_residual(om, 0.5, th)
    off = float(np.max(np.abs(R)))
    # the anchor solves the equation identically, so both must be roundoff
    assert nodal < 1e-11 and off < 1e-11, (nodal, off)
    # and the velocity it implies is the exact -log(1+X^2)/2
    Xf = np.tan(0.5 * th)
    assert np.allclose(parts["U"], -0.5 * np.log(1.0 + Xf ** 2), atol=1e-11)
    print("[ok] (2) a=0 reproduces decay_collocation exactly; the exact anchor's "
          "residual is %.1e on the nodes and %.1e BETWEEN them; U matches "
          "-log(1+X^2)/2" % (nodal, off))


def test_3_jacobian():
    col = ACollocation(120, a=0.35)
    om = col.anchor() * (1.0 + 0.3 * np.cos(col.theta))
    c = 0.55
    Jm = col.jacobian_a(om, c)
    rng = np.random.default_rng(3)
    worst = 0.0
    for _ in range(4):
        h = rng.standard_normal(col.J)
        h /= np.max(np.abs(h))
        eps = 1e-7
        fd = (col.residual_a(om + eps * h, c) - col.residual_a(om - eps * h, c)) / (2 * eps)
        worst = max(worst, float(np.max(np.abs(fd - Jm @ h))
                                 / np.max(np.abs(Jm @ h))))
    dc = (col.residual_a(om, c + 1e-7) - col.residual_a(om, c - 1e-7)) / 2e-7
    assert worst < 1e-6, worst
    assert np.max(np.abs(dc - col.dc_column_a(om))) < 1e-8
    print("[ok] (3) analytic Jacobian (a=0.35) matches finite differences to "
          "%.1e; dF/dc exact" % worst)


def test_4_certificate_system():
    col = ACollocation(J, a=0.0)
    r = col.newton_gauged(c=0.5, om0=col.anchor() * 1.2 + 0.02 * np.cos(col.theta))
    assert r["converged"], r["history"][-3:]
    assert r["kept_sup"] < 1e-11, r["kept_sup"]
    assert np.max(np.abs(r["Omega"] - col.anchor())) < 1e-9
    ca = ACollocation(J, a=0.3)
    ra = ca.newton_gauged(c=0.5)
    assert ra["kept_sup"] < 1e-11, ra["kept_sup"]
    print("[ok] (4) the gauged system Newton enforces goes to machine zero: "
          "%.1e (a=0, and it returns the exact anchor to %.1e) / %.1e (a=0.3)"
          % (r["kept_sup"], np.max(np.abs(r["Omega"] - col.anchor())),
             ra["kept_sup"]))


def test_5_two_builds_agree():
    from solver.profile_newton import TwoScaleNewton
    a = 0.3
    col = ACollocation(400, a=a)
    r = col.newton_gauged(c=0.5)
    om, c = r["Omega"], r["c"]
    Xc_theta = critical_radius(col.X, effective_speed(col.X, col.V @ om, c, a))
    p_theta, _ = zero_order(col.X, om, Xc_theta)

    nw = TwoScaleNewton(a=a, n=801)
    s = nw.solve()
    Xc_rho = critical_radius(nw.fam.X, effective_speed(nw.fam.X, nw.VH @ s["Omega"],
                                                       s["c"], a))
    p_rho, _ = zero_order(nw.fam.X, s["Omega"], Xc_rho)

    # X_c / c is the dilation invariant (Omega(X/mu), mu c) once the amplitude
    # gauge Omega(0) = -1 has fixed the scaling; X_c alone is not.
    inv_t, inv_r = Xc_theta / c, Xc_rho / s["c"]
    assert abs(inv_t - inv_r) / inv_r < 0.03, (inv_t, inv_r)
    assert abs(p_theta - 1.0 / a) / (1.0 / a) < 0.15, (p_theta, 1.0 / a)
    assert abs(p_rho - 1.0 / a) / (1.0 / a) < 0.15, (p_rho, 1.0 / a)
    print("[ok] (5) two independent discretizations agree: X_c/c = %.3f "
          "(theta-collocation) vs %.3f (sinh-rho), %.1f%%; zero order %.2f / "
          "%.2f vs the predicted 1/a = %.2f"
          % (inv_t, inv_r, 100 * abs(inv_t - inv_r) / inv_r, p_theta, p_rho, 1 / a))


def test_6_defect_survives_the_solve():
    col = ACollocation(J, a=0.3)
    r = col.newton_gauged(c=0.5)
    wd, th_at, _, _ = weighted_defect(col, r["Omega"], r["c"], alpha=1.4, refine=8)
    ctrl = ACollocation(J, a=0.0)
    wd0, _, _, _ = weighted_defect(ctrl, ctrl.anchor(), 0.5, alpha=1.4, refine=8)
    assert r["kept_sup"] < 1e-11
    assert r["dropped_defect"] > 1e3 * r["kept_sup"], (r["dropped_defect"],
                                                       r["kept_sup"])
    assert wd > 1e3 * wd0, (wd, wd0)
    print("[ok] (6) rows enforced %.1e, row displaced by the gauge %.1e, "
          "weighted off-node defect %.1e at X=%.1f -- against a control (exact "
          "anchor) of %.1e"
          % (r["kept_sup"], r["dropped_defect"], wd, np.tan(0.5 * th_at), wd0))


if __name__ == "__main__":
    for t in (test_1_velocity_integrals, test_2_a0_reduction_and_offnode,
              test_3_jacobian, test_4_certificate_system, test_5_two_builds_agree,
              test_6_defect_survives_the_solve):
        t()
    print("\n6/6 gates passed.")
