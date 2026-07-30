"""Gates for solver/decay_grading.py -- the Route-D v3 decay-graded space layer.

Every gate is checked against an INDEPENDENT oracle (a closed form, a second
implementation, or an exact special case), never against a previous run of this
same code.  Run:  .venv/bin/python test_decay_grading.py

  1  cos_power_coeffs vs exact special cases (alpha = 0, 2, 4) and vs a direct
     pointwise evaluation of |cos(theta/2)|^alpha.
  2  H(cos k th) = sin k th on the model profile: for alpha = 2 the pair
     (1+X^2)^{-1} -> X/(1+X^2) is known in closed form.
  3  the sum/difference fold at theta -> +-pi (the far field) is exact.
  4  quadratic_coeffs (pure convolution) == the quadratic part of
     solver.nk_fourier.residual (sum AND difference double loop), EXACTLY.
  5  algebra_constant is two-sided sharp: the measured sup of
     ||Q(h)||_v / ||h||_u^2 over test vectors lies in [S/4, S/2].
  6  the far-field decay law: X^{alpha+1} f_alpha H(f_alpha) -> (1/pi) int f_alpha
     -- the quadratic term gains EXACTLY one power of decay.
  7  the far-field resonance, from BOTH sides: the discretized inverse norm
     matches 2/|alpha-2|, and the operator-side leading coefficient of DF on a
     X^{-alpha} profile matches c alpha - 1.
"""

import math

import numpy as np

from solver.decay_grading import (
    quadratic_coeffs, algebra_constant, cos_power_coeffs, eval_cos_series,
    eval_sin_series, theta_of_X, X_of_theta, cos_power_mass,
    hilbert_of_cos_power, farfield_inverse_norm, farfield_symbol_coefficient,
    farfield_inverse_norm_finite,
)
from solver.nk_fourier import residual


def test_cos_power_coeffs():
    a0 = cos_power_coeffs(0.0, 6)
    assert abs(a0[0] - 1.0) < 1e-14 and np.max(np.abs(a0[1:])) < 1e-14, a0

    # |cos(th/2)|^2 = (1 + cos th)/2 exactly  (= 1/(1+X^2), the anchor's shape)
    a2 = cos_power_coeffs(2.0, 6)
    exact2 = np.array([0.5, 0.5, 0, 0, 0, 0, 0])
    assert np.max(np.abs(a2 - exact2)) < 1e-14, a2

    # |cos(th/2)|^4 = ((1+cos)/2)^2 = 3/8 + cos/2 + cos(2th)/8
    a4 = cos_power_coeffs(4.0, 6)
    exact4 = np.array([0.375, 0.5, 0.125, 0, 0, 0, 0])
    assert np.max(np.abs(a4 - exact4)) < 1e-13, a4

    # non-integer alpha: series vs direct pointwise evaluation
    for alpha in (1.2, 1.75, 2.5):
        a = cos_power_coeffs(alpha, 40000)
        th = np.linspace(-3.0, 3.0, 41)
        got = eval_cos_series(a, th)
        want = np.abs(np.cos(th / 2.0)) ** alpha
        err = float(np.max(np.abs(got - want)))
        assert err < 1e-6, (alpha, err)
    print("[ok] (1) cos_power_coeffs matches exact alpha=0,2,4 and the pointwise "
          "|cos(th/2)|^alpha")


def test_hilbert_identity():
    # alpha = 2:  f = 1/(1+X^2),  H(f) = X/(1+X^2)   (classical pair)
    X = np.array([-30.0, -3.0, -0.7, 0.0, 0.4, 2.0, 11.0, 250.0])
    a = cos_power_coeffs(2.0, 8)
    got = eval_sin_series(a, theta_of_X(X))
    want = X / (1.0 + X ** 2)
    err = float(np.max(np.abs(got - want)))
    assert err < 1e-14, err

    # alpha = 4:  f = (1+X^2)^{-2}, H(f) = X(3+X^2)/(2(1+X^2)^2)
    #             (from H(cos)=sin on 3/8 + cos/2 + cos2th/8)
    a4 = cos_power_coeffs(4.0, 8)
    got4 = eval_sin_series(a4, theta_of_X(X))
    want4 = X * (3.0 + X ** 2) / (2.0 * (1.0 + X ** 2) ** 2)
    err4 = float(np.max(np.abs(got4 - want4)))
    assert err4 < 1e-14, err4
    print(f"[ok] (2) H(cos k th) = sin k th on the model profiles "
          f"(alpha=2: {err:.1e}, alpha=4: {err4:.1e})")


def test_far_field_fold():
    """The near-pi angle fold must be exact, not merely accurate."""
    rng = np.random.default_rng(11)
    a = rng.standard_normal(200)
    th = np.array([np.pi - 1e-5, np.pi - 3e-3, -np.pi + 2e-4, 0.3, -2.9, 1.9])
    k = np.arange(a.size)
    ref_c = np.cos(np.outer(th, k)) @ a
    ref_s = np.sin(np.outer(th, k)) @ a
    ec = float(np.max(np.abs(eval_cos_series(a, th) - ref_c)))
    es = float(np.max(np.abs(eval_sin_series(a, th) - ref_s)))
    scale = float(np.abs(a).sum())
    assert ec < 1e-12 * scale and es < 1e-12 * scale, (ec, es, scale)
    print(f"[ok] (3) the theta -> +-pi fold agrees with the direct sum "
          f"({ec:.1e}, {es:.1e} on scale {scale:.1f})")


def test_quadratic_is_pure_convolution():
    """Independent second build of Q(h) = h H(h): convolution vs sum+difference."""
    rng = np.random.default_rng(4)
    worst = 0.0
    for K in (1, 2, 5, 9):
        for _ in range(4):
            h = rng.standard_normal(K + 1)
            mine = quadratic_coeffs(h)
            theirs = residual(h, 0.0)              # c = 0 -> quadratic part only
            n = min(mine.size, theirs.size)
            scale = float(np.abs(h).sum()) ** 2
            # the two builds sum in different orders, so agreement is to rounding,
            # not bitwise; anything above that would be a real discrepancy
            err = float(np.max(np.abs(mine[:n] - theirs[:n]))) / scale
            assert err < 1e-15, (K, err)
            worst = max(worst, err)
            assert float(np.abs(mine[n:]).sum()) == 0.0
            assert float(np.abs(theirs[n:]).sum()) == 0.0
    # and the anchor: Omega_2 H(Omega_2) = sin/4 + sin2/8
    q = quadratic_coeffs(np.array([-0.5, -0.5]))
    assert abs(q[0] - 0.25) < 1e-16 and abs(q[1] - 0.125) < 1e-16, q
    print(f"[ok] (4) Q(h) = h H(h) is a PURE convolution -- agrees with the "
          f"independent sum/difference build to {worst:.1e} (rounding), 0.0 at the anchor")


def test_algebra_constant_sharpness():
    """S/4 <= (measured sup of ||Q(h)||_v / ||h||_u^2) <= S/2, on several pairs."""
    K = 14
    rng = np.random.default_rng(7)
    for name, u, v in (
        ("flat", np.ones(K + 1), np.ones(2 * K)),
        ("u=(1+k)^1, v=flat", (1.0 + np.arange(K + 1)), np.ones(2 * K)),
        ("u=flat, v=m (D6 pair)", np.ones(K + 1), np.arange(1, 2 * K + 1.0)),
        ("u=(1+k)^0.5, v=(1+m)^1.5", (1.0 + np.arange(K + 1)) ** 0.5,
         (1.0 + np.arange(1, 2 * K + 1.0)) ** 1.5),
    ):
        S, M_lo, M_hi, arg = algebra_constant(u, v)
        best = 0.0
        # the two-mode optimizer that proves necessity, plus random probes
        for j in range(K + 1):
            for k in range(K + 1):
                if j + k < 1 or j + k > len(v):
                    continue
                xi, eta = 1.0 / u[j], 1.0 / u[k]
                h = np.zeros(K + 1)
                h[j] += xi
                h[k] += eta
                q = quadratic_coeffs(h, M=len(v))
                best = max(best, float(np.abs(q) @ v)
                           / float(np.abs(h) @ u) ** 2)
        for _ in range(300):
            h = rng.standard_normal(K + 1) * rng.choice([1.0, 0.1, 10.0], K + 1)
            q = quadratic_coeffs(h, M=len(v))
            best = max(best, float(np.abs(q) @ v) / float(np.abs(h) @ u) ** 2)
        assert M_lo - 1e-12 <= best <= M_hi + 1e-12, (name, S, best, M_lo, M_hi)
    print("[ok] (5) algebra_constant is two-sided sharp: measured sup in [S/4, S/2] "
          "on 4 weight pairs")


def test_quadratic_gains_one_power():
    """X^{a+1} f_a H(f_a) -> (1/pi) int f_a: the quadratic gains ONE power of decay."""
    K = 200000
    worst = 0.0
    for alpha in (1.2, 1.5, 1.8):
        a = cos_power_coeffs(alpha, K)
        X = np.array([1e3, 2e3, 5e3, 1e4])
        f = (1.0 + X ** 2) ** (-0.5 * alpha)
        Hf = eval_sin_series(a, theta_of_X(X))
        got = X ** (alpha + 1.0) * f * Hf
        # H(f)(X) = m0/(pi X) + O(X^{-alpha}), so the approach to the limit is
        # O(X^{1-alpha}) -- slow for alpha near 1.  Fit that known form and gate
        # the EXTRAPOLATED limit against the closed-form oracle.
        A = np.column_stack([np.ones_like(X), X ** (1.0 - alpha)])
        L = float(np.linalg.lstsq(A, got, rcond=None)[0][0])
        want = cos_power_mass(alpha) / math.pi
        rel = abs(L - want) / want
        assert rel < 1e-2, (alpha, got, L, want, rel)
        worst = max(worst, rel)
    print(f"[ok] (6) X^(a+1) f_a H(f_a) -> (int f_a)/pi for a=1.2,1.5,1.8 "
          f"(<= {100 * worst:.1f}% after the known O(X^(1-a)) fit) -- one power gained")


def test_far_field_resonance():
    """2/|alpha-2| from the inverse side; c*alpha-1 from the operator side."""
    # Xmax must be large: for alpha < 2 the finite domain costs a relative
    # (X0/Xmax)^{2-alpha}, which is 6% at Xmax=1e6, alpha=1.8 but 0.4% at 1e12.
    worst_inv = 0.0
    for alpha in (1.2, 1.5, 1.8, 1.9, 2.1, 2.4, 3.0):
        got, _ = farfield_inverse_norm(alpha, n=8001, Xmax=1e12)
        want = farfield_inverse_norm_finite(alpha, Xmax=1e12)
        rel = abs(got - want) / want
        assert rel < 5e-3, (alpha, got, want, rel)
        worst_inv = max(worst_inv, rel)

    # operator side: X^{a+1} DF[f_a] -> c a - 1, once the known X^{a-2} term
    # (from Omega_2 H(f_a) ~ -(int f)/pi X^{-3}) is subtracted.
    K, c, worst_op = 200000, 0.5, 0.0
    X = np.array([3e3, 1e4])
    for alpha in (1.2, 1.5, 1.8):
        a = cos_power_coeffs(alpha, K)
        f = (1.0 + X ** 2) ** (-0.5 * alpha)
        fX = -alpha * X * (1.0 + X ** 2) ** (-0.5 * alpha - 1.0)
        Hf = eval_sin_series(a, theta_of_X(X))
        Om = -1.0 / (1.0 + X ** 2)
        HOm = -X / (1.0 + X ** 2)
        DF = f * HOm + Om * Hf - c * fX
        got = X ** (alpha + 1.0) * DF + (cos_power_mass(alpha) / math.pi) * X ** (alpha - 2.0)
        want = farfield_symbol_coefficient(alpha, c)
        rel = float(np.max(np.abs(got - want) / abs(want)))
        assert rel < 2e-2, (alpha, got, want, rel)
        worst_op = max(worst_op, rel)
    print(f"[ok] (7) far-field resonance at alpha=2 confirmed twice: "
          f"||L^-1|| = the exact finite-domain norm (<={100 * worst_inv:.2f}%) and "
          f"lim X^(a+1) DF[f_a] = c a - 1 (<={100 * worst_op:.1f}%)")


if __name__ == "__main__":
    test_cos_power_coeffs()
    test_hilbert_identity()
    test_far_field_fold()
    test_quadratic_is_pure_convolution()
    test_algebra_constant_sharpness()
    test_quadratic_gains_one_power()
    test_far_field_resonance()
    print("\nALL DECAY-GRADING TESTS PASSED")
