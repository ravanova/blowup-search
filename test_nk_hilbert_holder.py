"""Gates for solver/hilbert_holder.py -- the weighted Holder bound on H.

Six gates, in the order they were written (which is the order they caught
things):

  (1) THE DECOMPOSITION, verified against the exact conjugate.  The estimate is
      a majorant of E_N + E_F + G; an inequality test can only ever check the
      majorant step, so the decomposition itself is built a SECOND time with the
      true increments and compared to cos k th -> sin k th.  It caught two sign
      errors that no domination test would have noticed, because a majorant of a
      wrong decomposition is still an inequality about something.
  (2) DOMINATION on a profile family, including the v4 square-wave adversary and
      a far-field bump -- the direction a bound of this shape is most likely to
      miss.
  (3) CONVERGENCE of both discretizations the constant depends on: the pair
      sweep (a grid supremum can only UNDER-report) and the quadrature.
  (4) THE ROUTE ABLATION.  The pointwise route alone -- which is all v6/v7 had
      for this quantity -- is ~240x worse, and the per-pair rule matters: taking
      whichever route has the smaller coefficient SUM inflates b_sup, because at
      a near-tie it trades a large u_sup for a marginal gain.
  (5) THE STRUCTURE IN gamma: the near region charges ~1/gamma and the far
      region ~1/(1-gamma), so both ends rise and C_Q BOWLS -- which is the mechanism that puts an interior
      optimum back into Z2 after v7's map ran off its own grid edge.
  (6) THE ASSEMBLY: the quadratic form's maximum in closed form, and the full
      C_Q bracketing the measured one from above.

Run: .venv/bin/python test_nk_hilbert_holder.py
"""

import numpy as np

from solver.decay_collocation import grid, transforms
from solver.holder_norms import HolderNorm, square_wave_partial_sum
from solver.nk_bounds import quadratic_constant_upper
from solver.hilbert_holder import (
    conjugate, cq_sup_split, decomposition_exact, hilbert_holder_constant,
    increment_pair_bound, near_padding, pointwise_pair_bound,
    quadratic_constant_full, weighted_seminorm, _quadratic_form_max,
)

ALPHA, GAMMA = 1.5, 0.5


def profiles(theta, alpha):
    """A test family in the class: the anchor shape, oscillations, adversaries."""
    f = np.cos(0.5 * theta) ** alpha
    out = {"f_alpha": f}
    for k in (1, 4, 16, 64):
        out["cos%d_f" % k] = np.cos(k * theta) * f
    out["square32_f"] = square_wave_partial_sum(theta, 32) * f
    out["square256_f"] = square_wave_partial_sum(theta, 256) * f
    out["bump_core"] = np.exp(-((theta - 0.6) / 0.05) ** 2) * f
    out["bump_far"] = np.exp(-((theta - 3.0) / 0.02) ** 2) * f
    return out


def test_1_decomposition():
    cases = [np.array([0.0, 1.0]), np.array([0.0, 0.0, 0.0, 1.0]),
             np.array([0.3, 1.0, -0.5, 0.2, 0.1, -0.4])]
    pairs = [(0.7, 0.05), (0.7, -0.3), (2.9, 0.02), (0.02, 0.5), (1.0, 1.5),
             (3.1, -0.001), (0.001, 2.0)]
    worst = 0.0
    for coef in cases:
        for th, sig in pairs:
            got = decomposition_exact(coef, th, sig, n_quad=8000)
            exact = float(conjugate(coef, [th])[0] - conjugate(coef, [th + sig])[0])
            worst = max(worst, abs(got - exact))
    assert worst < 1e-4, worst
    print("[ok] (1) E_N + E_F + G reproduces the exact conjugate to %.1e over "
          "%d pairs x %d profiles (quadrature-limited)"
          % (worst, len(pairs), len(cases)))


def test_2_domination():
    J = 1200
    th, X = grid(J)
    to_coef, _, Sm = transforms(J)
    worst_all = 0.0
    for alpha, gamma in ((ALPHA, GAMMA), (1.2, 0.25)):
        dom = HolderNorm(th, X, alpha, gamma)
        r = hilbert_holder_constant(alpha, gamma, n_theta=40, n_d=22, n_quad=300)
        worst = 0.0
        for h in profiles(th, alpha).values():
            psi = Sm @ (to_coef @ h)
            ub = r["b_sup"] * dom.sup_part(h) + r["b_semi"] * dom.seminorm(h)
            worst = max(worst, weighted_seminorm(psi, th, 1.0 - gamma, gamma) / ub)
        assert worst <= 1.0, (alpha, gamma, worst)
        worst_all = max(worst_all, worst)
    print("[ok] (2) the bound dominates the measured weighted seminorm of H(h) "
          "on 9 profiles x 2 (alpha,gamma); worst ratio %.4f <= 1" % worst_all)


def test_3_convergence():
    levels = [(24, 14), (40, 22), (64, 34), (96, 52)]
    vals = [hilbert_holder_constant(ALPHA, GAMMA, n_theta=nt, n_d=nd, n_quad=300)
            for nt, nd in levels]
    bs = np.array([v["b_sup"] for v in vals])
    bt = np.array([v["b_semi"] for v in vals])
    spread = max(np.ptp(bs) / bs.mean(), np.ptp(bt) / bt.mean())
    assert spread < 0.01, (bs, bt)
    q = [increment_pair_bound(0.0545, -1e-5, ALPHA, GAMMA, n_quad=n)[1]
         for n in (150, 300, 600, 1200)]
    qspread = (max(q) - min(q)) / np.mean(q)
    assert qspread < 0.01, q
    print("[ok] (3) pair sweep converged over 4 grid levels (spread %.2e, "
          "b = (%.4f, %.4f)); quadrature spread %.2e" % (spread, bs[-1], bt[-1], qspread))


def test_4_routes():
    kw = dict(n_theta=40, n_d=22, n_quad=300)
    inc = hilbert_holder_constant(ALPHA, GAMMA, rule="increment", **kw)
    sm = hilbert_holder_constant(ALPHA, GAMMA, rule="sum", **kw)
    pw = hilbert_holder_constant(ALPHA, GAMMA, rule="pointwise", **kw)
    gain = (pw["b_sup"] + pw["b_semi"]) / (inc["b_sup"] + inc["b_semi"])
    assert gain > 100.0, gain
    assert sm["b_sup"] > 1.5 * inc["b_sup"], (sm["b_sup"], inc["b_sup"])
    assert near_padding(0.01) == 2.0 and near_padding(2.5) < 0.3
    assert near_padding(3.0) is None
    wide = increment_pair_bound(1e-4, 2.5, ALPHA, GAMMA, n_quad=600)
    assert np.isfinite(wide).all() and max(wide) < 10.0, wide
    print("[ok] (4) increment route beats the pointwise-only control %.0fx "
          "(%.3f vs %.1f); the min-SUM rule inflates b_sup %.2f -> %.2f; the "
          "shrinking pad keeps wide pairs finite" %
          (gain, inc["b_sup"] + inc["b_semi"], pw["b_sup"] + pw["b_semi"],
           inc["b_sup"], sm["b_sup"]))


def test_5_gamma_structure():
    gs = (0.05, 0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9)
    bt, full, sup_only = [], [], []
    for g in gs:
        r = hilbert_holder_constant(ALPHA, g, n_theta=32, n_d=18, n_quad=300)
        qs, qt = cq_sup_split(ALPHA, g, n_X=60)
        bt.append(r["b_semi"])
        full.append(quadratic_constant_full(ALPHA, g, qs, qt, r["b_sup"],
                                            r["b_semi"])["C_Q_full"])
        sup_only.append(quadratic_constant_upper(ALPHA, g, n_X=60)["C_Q_sup_upper"])
    bt, full, sup_only = np.array(bt), np.array(full), np.array(sup_only)
    rate = bt[0] / bt[1]                              # ~1/gamma over 0.05 -> 0.1
    assert 1.2 < rate < 2.6, rate
    assert bt[-1] > bt[4], bt                          # rises again toward gamma=1
    i = int(full.argmin())
    assert 0 < i < len(gs) - 1, full                   # INTERIOR minimum
    assert sup_only.argmin() >= len(gs) - 2, sup_only  # the omitted term had none
    print("[ok] (5) b_semi rises to %.1f at gamma=0.05 (from %.1f at 0.1) and "
          "again to %.1f at 0.9; C_Q_full bowls with an INTERIOR minimum %.3f at "
          "gamma=%.2f, while the sup-only C_Q is monotone" %
          (bt[0], bt[1], bt[-1], full[i], gs[i]))


def test_6_assembly():
    rng = np.random.default_rng(5)
    worst = 0.0
    for _ in range(200):
        a, b, c = rng.uniform(-3, 6, 3)
        t = np.linspace(0.0, 1.0, 200001)
        brute = float(np.max(a * t ** 2 + b * t * (1 - t) + c * (1 - t) ** 2))
        worst = max(worst, abs(_quadratic_form_max(a, b, c) - brute))
    assert worst < 1e-8, worst

    J = 1000
    th, X = grid(J)
    to_coef, _, Sm = transforms(J)
    dom = HolderNorm(th, X, ALPHA, GAMMA)
    cod = HolderNorm(th, X, ALPHA + 1.0, GAMMA)
    r = hilbert_holder_constant(ALPHA, GAMMA, n_theta=40, n_d=22, n_quad=300)
    qs, qt = cq_sup_split(ALPHA, GAMMA)
    full = quadratic_constant_full(ALPHA, GAMMA, qs, qt, r["b_sup"],
                                   r["b_semi"])["C_Q_full"]
    sup_only = quadratic_constant_upper(ALPHA, GAMMA)["C_Q_sup_upper"]
    assert full > sup_only, (full, sup_only)
    meas = 0.0
    for h in profiles(th, ALPHA).values():
        psi = Sm @ (to_coef @ h)
        n = dom(h)
        meas = max(meas, cod(h * psi) / (n * n))
    assert meas < full, (meas, full)
    print("[ok] (6) closed-form simplex max exact to %.1e; C_Q_full = %.3f "
          "brackets the measured %.3f from above and exceeds v6's sup-only %.3f"
          % (worst, full, meas, sup_only))


if __name__ == "__main__":
    test_1_decomposition()
    test_2_domination()
    test_3_convergence()
    test_4_routes()
    test_5_gamma_structure()
    test_6_assembly()
    print("\nALL HILBERT-HOLDER TESTS PASSED")
