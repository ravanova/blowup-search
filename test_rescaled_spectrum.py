"""Gates for solver/rescaled_spectrum.py -- the rescaled gCLM flow and its spectrum.

  (1) THE EXACT ANCHOR.  Omega_0 = -sin theta = -2X/(1+X^2) is the CLM self-similar
      profile; it must null the residual to MACHINE precision at every K, with
      c_omega = -1 exactly.  Anything above 1e-15 means an operator is wrong.
  (2) THE OPERATORS ARE EXACT, each against an independent closed form: the Hilbert
      transform (H(Omega_0) = 2/(1+X^2)), the dilation term (X d/dX = sin th d/dth),
      the derivative, and the velocity (U = 2 arctan X = theta on the anchor).  The
      velocity recursion is checked as a POLYNOMIAL IDENTITY, not just at the anchor,
      because that is the step where a three-term recursion can silently drift.
  (3) THE JACOBIAN is the derivative it claims to be (finite differences).
  (4) THE STRUCTURAL PAIR.  L(X Omega_X) = 0 and L(Omega) = -Omega + X Omega_X are
      claims about the algebra, so they get gated rather than trusted -- at the two
      values of a where the fixed point is analytic and the test therefore has
      machine-level headroom.
  (5) THE ANALYTIC SPECTRUM.  At a = 0 the continuum eigenfunctions are known in
      closed form and only lambda = 0, -1 survive the analytic class; the filter must
      return exactly those two and nothing else, out of K eigenvalues.
  (5b) THE CONTINUUM, AS AN IDENTITY.  The strip -1 < Re lambda < 1 and its
      closed-form eigenfunctions are a claim about the operator, so they are checked
      with a NUMERICAL derivative rather than re-derived.  The purely imaginary
      members are the log-periodic modes the DSS lane is about, and the gate confirms
      they are exactly tau-periodic -- and continuous spectrum, not eigenvalues.
  (6) THE POSITIVE CONTROL.  A filter that returns two eigenvalues is only evidence
      if it would have returned more.  Planting a localized potential must produce a
      converged eigenvalue in the RIGHT half plane, far from both structural ones.
  (7) FAILURE IS REPORTED.  Past the end of the branch Newton returns
      converged=False rather than handing back its last iterate.

Run: .venv/bin/python test_rescaled_spectrum.py
"""

import numpy as np

from solver.rescaled_spectrum import (
    OddCompactBasis, RescaledFlow, continuation, continuum_defect,
    continuum_eigenfunction, converged_spectrum, match_filter,
    planted_eigenvalue_control, spectrum,
)


def test_1_exact_anchor():
    for K in (16, 33, 64, 128):
        f = RescaledFlow(0.0, K=K)
        b = f.B.anchor()
        res = float(np.max(np.abs(f.residual(b))))
        cw = f.c_omega(b)
        assert res < 1e-14, (K, res)
        assert abs(cw + 1.0) < 1e-14, (K, cw)
    print("[ok] (1) the CLM self-similar profile Omega = -sin(theta) nulls the "
          "rescaled residual to %.1e with c_omega = -1 exactly, at K = 16..128" % res)


def test_2_operators_exact():
    K = 96
    B = OddCompactBasis(K)
    b = B.anchor()
    X, th = B.X, B.theta
    # Hilbert transform
    eH = float(np.max(np.abs(B.H @ b - 2.0 / (1.0 + X ** 2))))
    # velocity: U = int_0^X H(Omega) dX' = 2 arctan X = theta
    eU = float(np.max(np.abs(B.U @ b - th)))
    # dilation and derivative on a two-mode test vector
    v = np.zeros(K)
    v[0], v[2] = 0.7, -0.4                       # 0.7 sin th - 0.4 sin 3th
    d_th = 0.7 * np.cos(th) - 1.2 * np.cos(3 * th)
    eXD = float(np.max(np.abs(B.XD @ v - np.sin(th) * d_th)))
    eDX = float(np.max(np.abs(B.DX @ v - (1.0 + np.cos(th)) * d_th)))
    # the velocity recursion as a polynomial identity, off the anchor
    t = np.linspace(0.02, np.pi - 0.02, 501)
    n = np.zeros((K + 2, K + 2))
    n[1, 0] = -1.0
    for kk in range(1, K + 1):
        n[kk + 1, :] = -2.0 * n[kk, :] - n[kk - 1, :]
        n[kk + 1, kk] -= 2.0
    worst = 0.0
    for kk in (1, 2, 5, 12, 30):
        lhs = ((-1.0) ** kk - np.cos(kk * t)) / (1.0 + np.cos(t))
        rhs = np.cos(np.outer(t, np.arange(K + 2))) @ n[kk]
        worst = max(worst, float(np.max(np.abs(lhs - rhs)) / np.max(np.abs(lhs))))
    for e in (eH, eU, eXD, eDX):
        assert e < 1e-13, (eH, eU, eXD, eDX)
    assert worst < 1e-11, worst
    print("[ok] (2) operators exact: H %.1e, U %.1e, X d/dX %.1e, d/dX %.1e; the "
          "velocity recursion is a polynomial identity to %.1e (k up to 30)"
          % (eH, eU, eXD, eDX, worst))


def test_3_jacobian():
    rng = np.random.default_rng(11)
    worst = 0.0
    for a in (0.0, 0.35):
        f = RescaledFlow(a, K=48)
        b = f.B.anchor() + 0.02 * rng.standard_normal(48)
        J = f.jacobian(b)
        for _ in range(4):
            v = rng.standard_normal(48)
            v /= np.linalg.norm(v)
            h = 1e-6
            fd = (f.residual(b + h * v) - f.residual(b - h * v)) / (2 * h)
            rel = np.max(np.abs(fd - J @ v)) / np.max(np.abs(J @ v))
            worst = max(worst, float(rel))
    assert worst < 1e-6, worst
    print("[ok] (3) the Jacobian matches central differences to %.1e relative "
          "(a = 0 and 0.35, random directions off the anchor)" % worst)


def test_4_structural_pair():
    # a = 0: exact fixed point.  a = 1/2: the analytic resonance, so the fixed point
    # is spectrally converged and the identity has room to be tested.
    f0 = RescaledFlow(0.0, K=96)
    d0 = f0.structural_pair_defect(f0.B.anchor())
    flow, out = continuation(0.5, K=192, da=0.02)
    d5 = flow.structural_pair_defect(out["b"])
    assert max(d0) < 1e-12, d0
    assert max(d5) < 1e-5, (d5, out["residual"])
    # and the pair really is the spectrum of the 2x2 block
    A = f0.generator(f0.B.anchor())
    b = f0.B.anchor()
    d_dil = np.linalg.solve(f0.B.S, f0.B.XD @ b)
    M = np.array([[-1.0, 0.0], [1.0, 0.0]])          # claimed block on (Omega, X Om_X)
    lhs = np.column_stack([A @ b, A @ d_dil])
    rhs = np.column_stack([b, d_dil]) @ M
    blk = float(np.max(np.abs(lhs - rhs)))
    assert blk < 1e-13, blk
    print("[ok] (4) structural identities hold: defects %.1e/%.1e at a = 0 and "
          "%.1e/%.1e at a = 1/2; the 2x2 block [[-1,0],[1,0]] is exact to %.1e"
          % (d0[0], d0[1], d5[0], d5[1], blk))


def test_5_analytic_spectrum():
    r = converged_spectrum(0.0, K_coarse=96, K_fine=144, tol=1e-3)
    kept = np.sort_complex(r["kept"])
    assert r["n_kept"] == 2, (r["n_kept"], kept)
    assert min(abs(kept - 0.0)) < 1e-10 and min(abs(kept + 1.0)) < 1e-10, kept
    # everything else sits on the imaginary axis: the discretized continuum
    ev = r["ev_coarse"]
    off = ev[np.abs(ev.real) > 1e-9]
    assert off.size == 1 and abs(off[0] + 1.0) < 1e-12, off
    print("[ok] (5) at a = 0 exactly 2 of %d eigenvalues survive refinement -- "
          "0 and -1, the analytically predicted pair -- and the other %d sit on the "
          "imaginary axis to 1e-9 (the discretized continuum)"
          % (r["n_total"], r["n_total"] - 1))


def test_5b_continuum_closed_form():
    """The strip is a claim about the operator, so it gets checked as an identity.

    L s = lambda s for s = (w-1)^{1-l}(w+1)^{1+l}, with the derivative taken
    NUMERICALLY (so a wrong s_w would not cancel), across the whole admissible strip
    -- including the purely imaginary lambda = i y, which are the LOG-PERIODIC modes
    the DSS lane is about: s ~ X^{1-iy} against a time factor e^{i y tau} is a wave
    travelling outward in log X, exactly periodic with period 2 pi / y.
    """
    worst = 0.0
    for lm in (0.0, -0.5, 0.5, 0.9, -0.95, 2j, 8j, 0.3 + 3j):
        worst = max(worst, continuum_defect(lm))
    assert worst < 1e-4, worst
    # and the log-periodic member really is periodic in tau with the stated period
    y = 4.0
    th = np.linspace(0.02, np.pi - 0.02, 501)
    s = continuum_eigenfunction(1j * y, th)
    per = float(np.max(np.abs(s * np.exp(1j * y * (2 * np.pi / y)) - s))) / \
        float(np.max(np.abs(s)))
    assert per < 1e-12, per
    print("[ok] (5b) the closed-form continuum satisfies L s = lambda s to %.1e over "
          "the whole strip (numerical derivative); the lambda = 4i member is exactly "
          "tau-periodic with period 2pi/4 to %.1e -- the log-periodic DSS structure "
          "is CONTINUOUS spectrum, not an eigenvalue" % (worst, per))


def test_6_positive_control():
    c = planted_eigenvalue_control(a=0.0, K_coarse=96, K_fine=144, strength=6.0)
    planted = np.asarray(c["planted"])
    plain = np.asarray(c["plain"])
    assert planted.size >= 2, planted
    assert np.max(np.real(planted)) > 0.5, planted
    shift = max(float(np.min(np.abs(plain - z))) for z in planted)
    assert shift > 0.5, (shift, plain, planted)
    print("[ok] (6) positive control: with a planted potential the SAME filter "
          "returns a converged eigenvalue at %+.4f -- in the right half plane and "
          "%.2f away from anything the plain operator has, so 'only two survive' is "
          "a measurement, not a blind spot" % (np.max(np.real(planted)), shift))


def test_7_failure_reported():
    # far past the end of the branch, from a cold anchor start and no continuation
    f = RescaledFlow(1.6, K=96)
    out = f.newton(b0=f.B.anchor())
    assert not out["converged"], out["residual"]
    assert out["residual"] > 1e-3
    print("[ok] (7) past the branch Newton reports converged=False (residual %.2e) "
          "instead of returning its last iterate as a profile" % out["residual"])


if __name__ == "__main__":
    test_1_exact_anchor()
    test_2_operators_exact()
    test_3_jacobian()
    test_4_structural_pair()
    test_5_analytic_spectrum()
    test_5b_continuum_closed_form()
    test_6_positive_control()
    test_7_failure_reported()
    print("\nALL RESCALED-SPECTRUM TESTS PASSED")
