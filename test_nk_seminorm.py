"""Known-answer tests for the derivative-gain closure (solver/nk_seminorm.py).

The module claims an UPPER bound on a quantity six legs failed to bound, so every
gate here is a domination test against an independently computed measurement,
with an ADVERSARY rather than a random family wherever a supremum over a ball is
involved (banked lesson 9), plus the algebraic identities the chain rests on.

Pre-committed predicates:
  (1) THE SPLIT IS A REFACTOR, AND IT DOMINATES: a_sup + a_semi reproduces v6's
      `hilbert_farfield_bound` to rounding, and for unit-ball h on grid-resolved
      nodes the measured |H(h)(X)| stays under a_sup*S + a_semi*T -- which is
      SHARPER than v6's bound whenever S and T are not both 1.
  (2) THE INTERPOLATION INEQUALITY: for alpha >= 1 the measured weighted
      theta-seminorm of a test function never exceeds C(gamma)(P/2)^gamma
      (2S)^{1-gamma}, over smooth, oscillatory and localized profiles and four
      (alpha, gamma) pairs.
  (3) THE CLOSED-FORM MINIMUM: the formula equals a brute-force minimum over
      kappa to the brute force's own grid resolution, and kappa* is where the brute force attains it.
  (4) THE SOLVE-FOR-THE-DERIVATIVE IDENTITY: DF = -diag(X/(1+X^2)) -
      diag(1/(1+X^2)) H - c d/dX exactly, so (P) is a rearrangement and not an
      approximation.
  (5) THE FIXED POINT: the returned T satisfies T = F(T), F is increasing with
      contraction slope < 1 there (uniqueness), the bound is monotone in C_sup,
      and the closure holds for every C_sup tried BECAUSE the gain is sublinear
      (F(2T)/F(T) -> 2^gamma) -- there is no smallness condition for gamma < 1.
  (6) END TO END, AND J-FREE: at three J the measured seminorm part of ||A||
      over an adversarial family stays under the closure bound, the bound does
      not move with J (it has no J in it), and v6's two-point-dual bound on the
      same quantity grows -- i.e. the new route removes the J^gamma.

Run: python test_nk_seminorm.py    (no scipy; ~3 min)
"""

import numpy as np

from solver.decay_collocation import Collocation, C_ANCHOR
from solver.holder_norms import HolderNorm, square_wave_partial_sum
from solver.nk_bounds import hilbert_farfield_bound, seminorm_part_upper
from solver.nk_seminorm import (
    hilbert_split_bound, hilbert_split_curves, interpolation_constant,
    holder_interpolation_bound, derivative_bound, seminorm_closure,
    interpolant_far_field_defect,
)

ALPHA, GAMMA = 1.5, 0.5


def _gauged_inverse(col):
    J = col.J
    M = np.empty((J, J))
    M[0, :] = col.to_coef.sum(axis=0)
    M[1:, :] = col.jacobian_matrix(col.anchor(), C_ANCHOR)[1:, :]
    return np.linalg.inv(M)


def _unit_ball_family(col, alpha, gamma, rng, n_random=6):
    """Adversarial + smooth elements, each normalized to ||.||_{alpha,gamma} = 1.

    ADMISSIBILITY MATTERS HERE.  v6's validation family included raw nodal SIGN
    PATTERNS aligned with a row of H.  Those are not elements of the class: their
    interpolants do not decay (that is v6's own B1), so the far-field envelope
    |h(y)| <= S (1+y^2)^{-alpha/2} -- which every one of these bounds rests on --
    simply does not hold for them.  v6's total-norm bound had enough slack to
    absorb the violation; the split bound is sharper and does not, so the
    aligned adversary is LOW-PASSED to degree J/8 here, which keeps the
    alignment while putting the element back in the space.
    """
    dom = HolderNorm(col.theta, col.X, alpha, gamma)
    env = (1.0 + col.X ** 2) ** (-0.5 * alpha)

    def band(v, D):
        c = col.to_coef @ v
        c[D + 1:] = 0.0
        return col.cos_eval @ c

    raw = [(1.0 + col.X ** 2) ** (-0.5 * a) for a in (alpha, alpha + 0.5, alpha + 1.5)]
    raw += [square_wave_partial_sum(col.theta, m) for m in (16, 64, 256)]
    for frac in (0.5, 0.8, 0.95):
        i = int(frac * (col.J - 1))
        raw.append(band(np.sign(col.H[i]) * env, col.J // 8))
    for _ in range(n_random):
        k = int(rng.integers(1, col.J // 4))
        raw.append(np.cos(k * col.theta) * env)
    return [h / dom(h) for h in raw if dom(h) > 0], dom


def test_split_refactor_and_domination():
    """(1) a_sup + a_semi == v6's bound, and the split dominates measurements."""
    worst_id = 0.0
    for X in (1e-3, 0.3, 1.0, 7.0, 60.0, 1e4):
        a_sup, a_semi = hilbert_split_bound(X, ALPHA, GAMMA)
        ref, _, _ = hilbert_farfield_bound(X, ALPHA, GAMMA)
        worst_id = max(worst_id, abs(a_sup + a_semi - ref) / ref)
    assert worst_id < 1e-13, f"split must reproduce v6's bound, got {worst_id:.2e}"

    col = Collocation(1200)
    rng = np.random.default_rng(7)
    fam, dom = _unit_ball_family(col, ALPHA, GAMMA, rng)
    res = col.X * (np.pi / col.J) <= 1.0
    worst, gain = 0.0, 0.0
    for Xt in (5.0, 20.0, 60.0, 150.0):
        i = int(np.argmin(np.abs(col.X - Xt)))
        assert res[i]
        a_sup, a_semi = hilbert_split_bound(float(col.X[i]), ALPHA, GAMMA)
        ref, _, _ = hilbert_farfield_bound(float(col.X[i]), ALPHA, GAMMA)
        for h in fam:
            S, T = dom.sup_part(h), dom.seminorm(h)
            bnd = a_sup * S + a_semi * T
            meas = abs(float((col.H @ h)[i]))
            assert meas <= bnd, f"X={col.X[i]:.1f}: {meas:.3e} > {bnd:.3e}"
            worst = max(worst, meas / bnd)
            gain = max(gain, ref / bnd)
    assert gain > 1.0, "the split must be sharper than v6's total-norm bound"
    print(f"[ok] (1) split refactor exact to {worst_id:.1e}; dominates measurements "
          f"(worst ratio {worst:.3f}); up to {gain:.2f}x sharper than v6's bound")


def test_interpolation_inequality():
    """(2) the measured seminorm never exceeds C(gamma)(P/2)^g (2S)^{1-g}."""
    col = Collocation(1200)
    worst, cases = 0.0, 0
    for alpha, gamma in ((1.5, 0.5), (1.2, 0.35), (1.8, 0.7), (1.0, 0.5)):
        nrm = HolderNorm(col.theta, col.X, alpha, gamma)
        tests = [(1.0 + col.X ** 2) ** (-0.5 * b)
                 for b in (alpha, alpha + 1.0, 2.0)]
        tests += [np.cos(k * col.theta) * (1.0 + col.X ** 2) ** (-0.5 * alpha)
                  for k in (3, 17, 80)]
        tests += [np.exp(-(col.X - 3.0) ** 2),
                  square_wave_partial_sum(col.theta, 32)
                  * (1.0 + col.X ** 2) ** (-0.5 * alpha)]
        for h in tests:
            S, T = nrm.sup_part(h), nrm.seminorm(h)
            P = float(np.max((1.0 + col.X ** 2) ** (0.5 * (alpha + 1.0))
                             * np.abs(col.transport @ h)))
            bnd, _ = holder_interpolation_bound(S, P, gamma)
            assert T <= bnd * (1 + 1e-12), \
                f"alpha={alpha} gamma={gamma}: T={T:.4f} > bound={bnd:.4f}"
            worst = max(worst, T / bnd)
            cases += 1
    print(f"[ok] (2) interpolation inequality holds on {cases} profiles x 4 "
          f"(alpha,gamma): worst ratio {worst:.4f} <= 1")


def test_closed_form_minimum():
    """(3) the closed form is the brute-force minimum, attained at kappa*."""
    ks = np.geomspace(1e-7, 1e4, 400001)
    worst_v, worst_k = 0.0, 0.0
    for gamma in (0.2, 0.35, 0.5, 0.7, 0.85):
        for S, P in ((1.0, 1.0), (5.55, 182.0), (0.3, 900.0)):
            bnd, kap = holder_interpolation_bound(S, P, gamma)
            f = 0.5 * ks ** (1 - gamma) * P + 2 * S * ks ** (-gamma)
            worst_v = max(worst_v, abs(bnd - f.min()) / f.min())
            worst_k = max(worst_k, abs(kap - ks[f.argmin()]) / kap)
    assert worst_v < 1e-8, f"closed form off by {worst_v:.2e}"
    assert worst_k < 1e-4, f"kappa* off by {worst_k:.2e}"
    assert abs(interpolation_constant(0.5) - 2.0) < 1e-14
    print(f"[ok] (3) closed-form minimum matches brute force to {worst_v:.1e} "
          f"(kappa* to {worst_k:.1e}); C(1/2) = 2 exactly")


def test_derivative_identity():
    """(4) DF = -diag(X/(1+X^2)) - diag(1/(1+X^2)) H - c d/dX, exactly."""
    worst = 0.0
    for J in (300, 900):
        col = Collocation(J)
        DF = col.jacobian_matrix(col.anchor(), C_ANCHOR)
        claim = (-np.diag(col.X / (1.0 + col.X ** 2))
                 - col.H / (1.0 + col.X ** 2)[:, None]
                 - C_ANCHOR * col.transport)
        worst = max(worst, float(np.abs(DF - claim).max()) / float(np.abs(DF).max()))
    assert worst < 1e-14, f"identity relative error {worst:.3e}"
    print(f"[ok] (4) solve-for-the-derivative identity exact to {worst:.1e} "
          f"(relative) -- (P) is a rearrangement, not an approximation")


def test_fixed_point():
    """(5) T = F(T), unique (slope < 1), monotone in C_sup, honest failures."""
    curves = hilbert_split_curves(ALPHA, GAMMA)
    d = seminorm_closure(ALPHA, GAMMA, 5.5543, curves=curves)
    assert d["closes"]
    T = d["T_upper"]
    P = derivative_bound(d["C_sup"], T, ALPHA, GAMMA, curves=curves)
    back, _ = holder_interpolation_bound(d["C_sup"], P, GAMMA)
    assert abs(back - T) / T < 1e-9, f"not a fixed point: {back:.6f} vs {T:.6f}"
    assert 0.0 < d["contraction_slope"] < 1.0, \
        f"slope {d['contraction_slope']:.3f} must lie in (0,1) for uniqueness"

    prev = 0.0
    for C in (1.0, 3.0, 5.5543, 8.0, 5.0e3):
        r = seminorm_closure(ALPHA, GAMMA, C, curves=curves)
        assert r["closes"], f"gamma < 1 must always close (C_sup = {C})"
        assert r["T_upper"] > prev, "the bound must increase with C_sup"
        prev = r["T_upper"]
    # the reason it always closes: the gain is sublinear, F(2T)/F(T) -> 2^gamma
    S = 5.5543
    ratio = [holder_interpolation_bound(
                 S, derivative_bound(S, t, ALPHA, GAMMA, curves=curves), GAMMA)[0]
             for t in (1e4, 2e4)]
    assert abs(ratio[1] / ratio[0] - 2.0 ** GAMMA) < 0.02, \
        f"F must be sublinear (~T^gamma), got ratio {ratio[1]/ratio[0]:.4f}"
    assert seminorm_closure(ALPHA, GAMMA, 5.5543, curves=curves)["A_upper"] > 5.5543
    try:
        seminorm_closure(0.8, GAMMA, 1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("alpha < 1 must be refused")
    print(f"[ok] (5) fixed point T = {T:.3f} (slope {d['contraction_slope']:.3f} "
          f"< 1, unique); monotone in C_sup; closes for C_sup up to 5e3 because "
          f"the gain is sublinear (F(2T)/F(T) = {ratio[1]/ratio[0]:.3f} vs "
          f"2^gamma = {2.0**GAMMA:.3f}); alpha < 1 refused")


def test_end_to_end_j_free():
    """(6) dominates the measured seminorm part, and removes the J^gamma."""
    curves = hilbert_split_curves(ALPHA, GAMMA)
    bnd = seminorm_closure(ALPHA, GAMMA, 5.5543, curves=curves)["T_upper"]
    meas, dual = [], []
    for J in (125, 250, 500):
        col = Collocation(J)
        A = _gauged_inverse(col)
        dom = HolderNorm(col.theta, col.X, ALPHA, GAMMA)
        cod = HolderNorm(col.theta, col.X, ALPHA + 1.0, GAMMA)
        cod.w[0] = 1.0
        B = A / cod.w[None, :]
        rows = np.unique(np.linspace(0, J - 1, 14).astype(int))
        best = 0.0
        for i in rows:                       # adversarial: exact sup extremizers
            for j in rows:
                if i == j:
                    continue
                g = np.sign(B[i] - B[j]) / cod.w
                g[0] = 0.0
                n = cod(g)
                if n > 0:
                    best = max(best, dom.seminorm(A @ g) / n)
        meas.append(best)
        dual.append(seminorm_part_upper(A, dom.pair, cod.w, cod.pair))
    assert max(meas) <= bnd, f"measured {max(meas):.3f} > bound {bnd:.3f}"
    growth = float(np.polyfit(np.log([125, 250, 500]), np.log(dual), 1)[0])
    assert growth > 0.3, f"v6's dual bound should grow like J^gamma, got {growth:.3f}"
    # a defect the discrete norms cannot see: the interpolant's weighted sup
    col = Collocation(400)
    A = _gauged_inverse(col)
    g = np.zeros(col.J)
    g[col.J // 2] = 1.0
    d = interpolant_far_field_defect(col.to_coef, A @ g, ALPHA, col.theta[-1])
    assert d["weighted"][-1] > 1e3 * d["weighted_at_last_node"], \
        "the interpolant's weighted sup must blow up past the last node"
    print(f"[ok] (6) closure bound {bnd:.2f} (J-free) dominates measured "
          f"{max(meas):.3f}; v6's dual on the same quantity grows like "
          f"J^{growth:+.2f}; interpolant defect: w|h| jumps "
          f"{d['weighted_at_last_node']:.1e} -> {d['weighted'][-1]:.1e} past the "
          f"last node")


if __name__ == "__main__":
    test_split_refactor_and_domination()
    test_interpolation_inequality()
    test_closed_form_minimum()
    test_derivative_identity()
    test_fixed_point()
    test_end_to_end_j_free()
    print("\nALL NK-SEMINORM TESTS PASSED")
