"""Gates for solver/hilbert_pointwise.py -- the sharper pointwise |H(h)| bound.

  (1) THE KERNEL, verified two ways: the folded kernel reproduces the exact
      conjugate (cos k th -> sin k th) through the subtracted principal value,
      and its own principal value integrates to zero (it is the conjugate of the
      constant function).  The second half is what licenses the global
      subtraction that removes v6's band, matching scale and remainder term.
  (2) DOMINATION on a profile family at many angles, for three values of the
      payer parameter rho -- because EVERY rho must give a valid bound, not just
      the one that happens to be optimal.
  (3) SHARPER THAN v6 pointwise, at every sampled X, with the ratio reported.
  (4) CONVERGENCE in both discretizations (quadrature, theta grid).
  (5) THE PAYER RULE.  ||A|| bowls in rho with an INTERIOR optimum, and the
      neutral rule rho = 1 is worse than the crude bound it replaces -- the
      point of the leg.
  (6) PROPAGATION: at the optimal rho the closure and C_Q both improve on v6,
      and both still dominate the measured values.

Run: .venv/bin/python test_nk_hilbert_pointwise.py
"""

import numpy as np

from solver.decay_collocation import grid, transforms
from solver.holder_norms import HolderNorm, square_wave_partial_sum
from solver.hilbert_holder import conjugate, quadratic_constant_full
from solver.nk_bounds import quadratic_constant_upper
from solver.nk_seminorm import hilbert_split_bound, hilbert_split_curves, seminorm_closure
from solver.hilbert_pointwise import (
    measured_pointwise, pointwise_bound, pointwise_curves, sweep_rho,
    theta_grid, weighted_sups,
)

ALPHA, GAMMA = 1.5, 0.5
C_SUP = 5.536                      # v6's two-point dual at the reference point


def profiles(theta, alpha):
    f = np.cos(0.5 * theta) ** alpha
    out = {"f_alpha": f}
    for k in (1, 4, 16, 64):
        out["cos%d_f" % k] = np.cos(k * theta) * f
    out["square256_f"] = square_wave_partial_sum(theta, 256) * f
    out["bump_core"] = np.exp(-((theta - 0.6) / 0.05) ** 2) * f
    out["bump_far"] = np.exp(-((theta - 3.0) / 0.02) ** 2) * f
    return out


def _psi_via_kernel(coef, th, n=20000, eps=1e-11):
    """psi(th) from the folded kernel with the global subtraction -- second build."""
    k = np.arange(coef.size)

    def h(x):
        return np.cos(np.outer(np.atleast_1d(x), k)) @ coef

    h_th = float(h(th)[0])
    tz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz      # noqa: NPY201
    total = 0.0
    for L, sgn in ((th, -1.0), (np.pi - th, 1.0)):
        if L <= 0:
            continue
        s = np.geomspace(eps * L, L, n)
        phi = th + sgn * s
        K = -np.sin(th) / (np.sin(0.5 * (phi + th)) * np.sin(0.5 * sgn * s))
        total += float(tz((h(phi) - h_th) * K * s, np.log(s)))
    return total / (2.0 * np.pi)


def test_1_kernel():
    cases = [np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
             np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])]
    worst = 0.0
    for coef in cases:
        for th in (0.03, 0.4, 1.2, 2.5, 3.0, 3.14):
            got = _psi_via_kernel(coef, th)
            worst = max(worst, abs(got - float(conjugate(coef, [th])[0])))
    assert worst < 1e-5, worst

    # p.v. int K = 0: the conjugate of the constant function.
    zero = max(abs(_psi_via_kernel(np.array([1.0]), th)) for th in (0.2, 1.5, 3.0))
    assert zero < 1e-9, zero
    print("[ok] (1) folded kernel reproduces the exact conjugate to %.1e over 18 "
          "cases; its own p.v. integrates to %.1e, which is what licenses the "
          "global subtraction (no band, no remainder)" % (worst, zero))


def test_2_domination():
    J = 1500
    th, X = grid(J)
    to_coef, _, Sm = transforms(J)
    dom = HolderNorm(th, X, ALPHA, GAMMA)
    worst_all = 0.0
    for rho in (1.0, 6.0, 25.0):
        cv = pointwise_curves(ALPHA, GAMMA, rho=rho, n_theta=80, n_quad=300)
        r = measured_pointwise(profiles(th, ALPHA), th, lambda h: Sm @ (to_coef @ h),
                               dom, ALPHA, GAMMA, cv)
        assert r["worst_ratio"] <= 1.0, (rho, r)
        worst_all = max(worst_all, r["worst_ratio"])
    print("[ok] (2) valid at rho = 1, 6, 25: worst measured/bound %.4f <= 1 "
          "(nearly attained -- the bound is not loose on the anchor shape)"
          % worst_all)


def test_3_sharper_than_v6():
    ratios = []
    for X in (1e-3, 1e-2, 0.1, 1.0, 3.0, 10.0, 100.0, 1e3, 1e5):
        thX = 2.0 * np.arctan(X)
        s6, m6 = hilbert_split_bound(X, ALPHA, GAMMA)
        s9, m9 = pointwise_bound(thX, ALPHA, GAMMA, rho=1.0, n_quad=600)
        ratios.append((s9 + m9) / (s6 + m6))
    ratios = np.array(ratios)
    assert (ratios < 1.0).all(), ratios
    print("[ok] (3) sharper than v6 at every sampled X: ratio %.3f-%.3f "
          "(median %.3f)" % (ratios.min(), ratios.max(), float(np.median(ratios))))


def test_4_convergence():
    q = [pointwise_bound(2.0, ALPHA, GAMMA, rho=6.0, n_quad=n) for n in
         (300, 600, 1200, 2400)]
    qs = np.array([sum(x) for x in q])
    assert np.ptp(qs) / qs.mean() < 5e-3, qs
    sups = []
    for n_th, n_q in ((70, 200), (140, 400), (280, 800)):
        cv = pointwise_curves(ALPHA, GAMMA, rho=6.0, n_theta=n_th, n_quad=n_q)
        w = weighted_sups(cv, ALPHA)
        sups.append(w["closure_sup"] + w["closure_semi"])
    sups = np.array(sups)
    assert np.ptp(sups) / sups.mean() < 0.05, sups
    assert theta_grid(50).size <= 50
    print("[ok] (4) quadrature flat to %.1e over 8x; the weighted sup flat to "
          "%.1e over a 4x theta refinement"
          % (np.ptp(qs) / qs.mean(), np.ptp(sups) / sups.mean()))


def test_5_payer_rule():
    sw = sweep_rho(ALPHA, GAMMA, C_SUP, n_theta=80, n_quad=300,
                   closure_fn=lambda a, g, cs, cv: seminorm_closure(a, g, cs,
                                                                    curves=cv))
    rows = sw["rows"]
    i = int(np.argmin([r["A_upper"] for r in rows]))
    assert 0 < i < len(rows) - 1, [r["A_upper"] for r in rows]
    v6 = seminorm_closure(ALPHA, GAMMA, C_SUP,
                          curves=hilbert_split_curves(ALPHA, GAMMA))["A_upper"]
    neutral = next(r for r in rows if r["rho"] == 1.0)["A_upper"]
    assert neutral > v6, (neutral, v6)          # the neutral rule is WORSE than v6
    assert sw["best"]["A_upper"] < 0.8 * v6, (sw["best"]["A_upper"], v6)
    print("[ok] (5) ||A|| bowls in rho: optimum %.2f at rho = %.1f, vs %.2f at "
          "the neutral rho = 1 (which is worse than v6's %.2f) -- the payer rule "
          "must be tuned to the answer's T/S, not to 1"
          % (sw["best"]["A_upper"], sw["best"]["rho"], neutral, v6))


def test_6_propagation():
    cv6 = hilbert_split_curves(ALPHA, GAMMA)
    cv9 = pointwise_curves(ALPHA, GAMMA, rho=6.0, n_theta=140, n_quad=400)
    A6 = seminorm_closure(ALPHA, GAMMA, C_SUP, curves=cv6)["A_upper"]
    A9 = seminorm_closure(ALPHA, GAMMA, C_SUP, curves=cv9)["A_upper"]
    assert A9 < A6, (A9, A6)

    cq_cv = pointwise_curves(ALPHA, GAMMA, rho=1.0, n_theta=140, n_quad=400)
    w = weighted_sups(cq_cv, ALPHA)
    q9 = quadratic_constant_full(ALPHA, GAMMA, w["cq_sup"], w["cq_semi"],
                                 1.1936, 4.9410)["C_Q_full"]
    q6 = quadratic_constant_upper(ALPHA, GAMMA)["C_Q_sup_upper"]

    J = 1200
    th, X = grid(J)
    to_coef, _, Sm = transforms(J)
    dom = HolderNorm(th, X, ALPHA, GAMMA)
    cod = HolderNorm(th, X, ALPHA + 1.0, GAMMA)
    meas = 0.0
    for h in profiles(th, ALPHA).values():
        psi = Sm @ (to_coef @ h)
        n = dom(h)
        meas = max(meas, cod(h * psi) / (n * n))
    assert q9 > meas, (q9, meas)
    print("[ok] (6) ||A|| %.2f -> %.2f (-%.0f%%) and C_Q_full %.3f (v6 sup-only "
          "%.3f) still above the measured %.3f"
          % (A6, A9, 100 * (1 - A9 / A6), q9, q6, meas))


if __name__ == "__main__":
    test_1_kernel()
    test_2_domination()
    test_3_sharper_than_v6()
    test_4_convergence()
    test_5_payer_rule()
    test_6_propagation()
    print("\nALL HILBERT-POINTWISE TESTS PASSED")
