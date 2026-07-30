"""Gates for solver/holder_norms.py -- the Route-D v5 two-grading layer.

Run:  .venv/bin/python test_holder_norms.py

  1  the Holder seminorm is exact on functions whose modulus of continuity is
     known in closed form (|theta - pi/2|^beta and cos(k theta)).
  2  H does not amplify the seminorm mode by mode ([cos k th] vs [sin k th] stay
     within O(1) of each other, with no growth in k), so the unboundedness of H on
     L^infinity is a summation effect, not a mode-by-mode one.
  3  the conformal identity: the X-weighted far-field Holder seminorm equals
     2^gamma times the plain theta one with weight alpha - gamma (the exponent the
     first draft got wrong, and this check caught).
  4  the algebra inequality ||fg|| <= ||f|| ||g|| holds with constant 1.
  5  the square-wave adversary: sup-norm ratio ||H p_m||/||p_m|| GROWS like log m
     (the v4 obstruction) while the Holder ratio does NOT (the v5 repair).
  6  family_op_norm reproduces the exact sup-to-sup norm when the seminorm is
     switched off, and is monotone in the test family.  (It is NOT a lower bound
     for the sup-to-sup norm -- a stronger codomain norm shrinks the operator norm.)
"""

import numpy as np

from solver.holder_norms import (
    HolderNorm, decay_weight, conformal_check, family_op_norm,
    square_wave_partial_sum, holder_H_constant, jacobian_identity_error,
)
from solver.decay_collocation import Collocation, sup_op_norm


def _grid(J):
    th = np.pi * (np.arange(J) + 0.5) / J
    return th, np.tan(0.5 * th)


def test_seminorm_exact():
    th, X = _grid(400)
    hn = HolderNorm(th, X, 0.0, 0.5, semi_alpha=0.0)   # plain, unweighted
    # |theta - pi/2|^0.5 has Holder-1/2 seminorm exactly 1
    f = np.abs(th - 0.5 * np.pi) ** 0.5
    s = hn.seminorm(f)
    assert 0.94 <= s <= 1.0 + 1e-12, s        # discrete: converges to 1 from below
    # a smooth mode: [cos k th]_gamma <= k^gamma * (Lipschitz scaling); check the
    # exact small-separation behaviour |cos k th - cos k th'| ~ k |dth|
    for k in (1, 4, 16):
        g = np.cos(k * th)
        sk = HolderNorm(th, X, 0.0, 0.5, semi_alpha=0.0).seminorm(g)
        assert 0.5 * k ** 0.5 <= sk <= 2.2 * k ** 0.5, (k, sk)
    print(f"[ok] (1) Holder seminorm exact on closed-form moduli "
          f"(|th-pi/2|^0.5 -> {s:.4f}, target 1)")


def test_H_preserves_mode_seminorm():
    th, X = _grid(600)
    hn = HolderNorm(th, X, 0.0, 0.5, semi_alpha=0.0)
    worst = 0.0
    for k in (1, 2, 5, 11, 30):
        a, b = hn.seminorm(np.cos(k * th)), hn.seminorm(np.sin(k * th))
        worst = max(worst, abs(a - b) / a)
    # not exact: the grid covers (0, pi) only, so the quarter-period shift that
    # takes cos k th to sin k th moves mass across the endpoints.  The claim is
    # that H does not AMPLIFY the seminorm mode by mode -- O(1), not growing in k.
    assert worst < 0.5, worst
    print(f"[ok] (2) H does not amplify the seminorm mode by mode "
          f"([cos k] vs [sin k] within {100 * worst:.0f}%, no growth in k) -- its "
          f"L^inf unboundedness is a SUMMATION effect")


def test_conformal_identity():
    th, X = _grid(4000)
    jerr, xmax = jacobian_identity_error(th)
    assert jerr < 0.02, (jerr, xmax)
    assert xmax > 100.0, xmax
    worst = 0.0
    for gamma in (0.3, 0.5, 0.7):
        r, _ = conformal_check(th, gamma)
        worst = max(worst, r)
    assert worst < 0.02, worst
    print(f"[ok] (3) conformal identity (pointwise, alpha-independent): "
          f"X-weighted far-field seminorm = 2^gamma x the theta one with weight "
          f"alpha-gamma, to {100 * worst:.2f}% out to X={xmax:.0f} "
          f"(Jacobian dX/dth=(1+X^2)/2 to {100 * jerr:.2f}%)")


def test_algebra():
    th, X = _grid(300)
    rng = np.random.default_rng(9)
    worst = 0.0
    for alpha, gamma in ((0.0, 0.5), (1.5, 0.4)):
        base = (1.0 + X ** 2) ** (-0.5 * alpha)
        for _ in range(12):
            f = base * (np.cos(np.outer(th, np.arange(5))) @ rng.standard_normal(5))
            g = base * (np.cos(np.outer(th, np.arange(5))) @ rng.standard_normal(5))
            # the product lives in the alpha-doubled class; compare in the SAME
            # norm with the weight that makes the inequality meaningful (alpha=0)
            h0 = HolderNorm(th, X, 0.0, gamma, semi_alpha=0.0)
            worst = max(worst, h0(f * g) / (h0(f) * h0(g)))
    assert worst <= 1.0 + 1e-9, worst
    print(f"[ok] (4) the norm is an algebra with constant 1 "
          f"(worst ||fg||/(||f|| ||g||) = {worst:.4f})")


def test_adversary_defused():
    """The construction that broke the sup pair must NOT break the Holder pair."""
    th, X = _grid(2000)
    degs = (8, 32, 128, 512)
    sup_ratio, hol_ratio = [], []
    # PLAIN, unweighted: the square wave does not decay, so a decay weight on it
    # would just measure the grid's outer radius.  The question here is purely
    # about the smoothness scale.
    hn = HolderNorm(th, X, 0.0, 0.5, semi_alpha=0.0)
    for m in degs:
        j = np.arange((m - 1) // 2 + 1)
        k = 2 * j + 1
        c = (4.0 / np.pi) * (-1.0) ** j / k
        p = np.cos(np.outer(th, k)) @ c
        Hp = np.sin(np.outer(th, k)) @ c
        sup_ratio.append(float(np.max(np.abs(Hp)) / np.max(np.abs(p))))
        hol_ratio.append(hn(Hp) / hn(p))
    assert sup_ratio[-1] > 2.0 * sup_ratio[0], sup_ratio
    assert hol_ratio[-1] < 1.05 * hol_ratio[0], hol_ratio
    print(f"[ok] (5) the L^inf adversary is DEFUSED: sup ratio "
          f"{sup_ratio[0]:.2f}->{sup_ratio[-1]:.2f} (grows) but Holder ratio "
          f"{hol_ratio[0]:.2f}->{hol_ratio[-1]:.2f} (flat)")


def test_family_norm_consistency():
    """With the seminorm switched off, the family norm must BE the sup-to-sup norm.

    It is NOT a lower bound for the sup-to-sup norm in general: the sign-pattern
    extremizers have huge Holder seminorms, so dividing by the Holder codomain norm
    gives a much smaller ratio.  A stronger codomain norm shrinks the operator norm.
    """
    col = Collocation(150)
    A = np.linalg.inv(np.eye(col.J) + 0.3 * col.H)
    dom_s = HolderNorm(col.theta, col.X, 1.5, 0.5, sup_only=True)
    cod_s = HolderNorm(col.theta, col.X, 2.5, 0.5, sup_only=True)
    fam_s, _ = family_op_norm(A, dom_s, cod_s)
    exact = sup_op_norm(A, dom_s.w, cod_s.w)
    assert abs(fam_s - exact) <= 1e-9 * exact, (fam_s, exact)

    dom = HolderNorm(col.theta, col.X, 1.5, 0.5)
    cod = HolderNorm(col.theta, col.X, 2.5, 0.5)
    fam, _ = family_op_norm(A, dom, cod)
    rng = np.random.default_rng(1)
    extra = [rng.standard_normal(col.J) for _ in range(20)]
    fam2, _ = family_op_norm(A, dom, cod, extra=extra)
    assert fam2 >= fam - 1e-12, (fam, fam2)
    assert fam < exact, (fam, exact)
    print(f"[ok] (6) family_op_norm reproduces the exact sup-to-sup norm when the "
          f"seminorm is off ({fam_s:.4f} vs {exact:.4f}), is monotone in the family "
          f"({fam:.2f} -> {fam2:.2f}), and is SMALLER in the Holder pair (stronger "
          f"codomain norm)")


if __name__ == "__main__":
    test_seminorm_exact()
    test_H_preserves_mode_seminorm()
    test_conformal_identity()
    test_algebra()
    test_adversary_defused()
    test_family_norm_consistency()
    print("\nALL HOLDER-NORM TESTS PASSED")
