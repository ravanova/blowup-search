"""Gates for solver/fractional_gclm.py -- gCLM with fractional dissipation.

  (1) THE KNOWN ANSWER.  At a = 0, nu = 0 the model is exactly solvable, on the
      CIRCLE as well as the line: z = z_0/(1 - t z_0/2) with z = H(omega) + i omega.
      The solver must reproduce it, and the closed form itself is checked against a
      fine independent RK4 integration -- because "the solver matches my formula" is
      worth nothing if the formula is the thing that is wrong (banked lesson 21:
      build the identity twice, not just the number).
  (2) THE DISSIPATION IS EXACT.  With the nonlinearity switched off, the integrating
      factor must reproduce exp(-nu |k|^{2s} t) mode by mode to machine precision, at
      several s.  This leg is entirely about the SIZE of the dissipation term, so
      that term must not be the one carrying the scheme error.
  (3) THE BLOW-UP TIME formula T = 2/max{H(omega_0) : omega_0 = 0} against the exact
      solution's own singularity, and against the run's self-estimated T.
  (4) THE PREDICTION IS WHAT IT CLAIMS: s_c = alpha/2 and p = 1 - 2s/alpha are
      consistent (p(s_c) = 0), including the Navier-Stokes reading alpha = 2 <=> s = 1.
  (5) THE RELEVANCE EXPONENT is recovered at a = 0, where alpha = 1 exactly, so the
      prediction p = 1 - 2s has no fitted input at all.
  (6) UNDER-RESOLUTION IS REPORTED.  A deliberately starved run must show a spectral
      tail orders larger than a resolved one, so the guard can be used to reject
      results rather than decorate them.

Run: .venv/bin/python test_fractional_gclm.py
"""

import numpy as np

from solver.fractional_gclm import (
    FractionalGCLM, clm_blowup_time, clm_exact, critical_s, estimate_T,
    fit_relevance, relevance_exponent,
)
from solver.spectral_utils import hilbert_hat, wavenumbers

N = 2048


def _w0(n=N):
    x = np.arange(n) * 2.0 * np.pi / n
    return np.sin(x) + 0.4 * np.sin(2.0 * x)


def test_1_known_answer():
    n = N
    w0 = _w0(n)
    k = wavenumbers(n)
    # (a) the closed form against an independent RK4 integration of w_t = w H(w)
    def H(v):
        return np.fft.irfft(hilbert_hat(np.fft.rfft(v), k), n)
    w, t, dt = w0.copy(), 0.0, 2e-5
    for _ in range(int(0.2 / dt)):
        k1 = w * H(w)
        k2 = (w + 0.5 * dt * k1) * H(w + 0.5 * dt * k1)
        k3 = (w + 0.5 * dt * k2) * H(w + 0.5 * dt * k2)
        k4 = (w + dt * k3) * H(w + dt * k3)
        w = w + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        t += dt
    e_formula = float(np.max(np.abs(w - clm_exact(w0, t))))
    # (b) the solver against the closed form, well into the growth
    g = FractionalGCLM(n=n, a=0.0, nu=0.0, s=1.0)
    r = g.run(w0, t_end=2.5, amp_factor=1e12, sample_every=5)
    e_solver = float(np.max(np.abs(r["omega"] - clm_exact(w0, r["t_final"]))))
    assert e_formula < 1e-11, e_formula
    assert e_solver < 1e-7, e_solver
    print("[ok] (1) the closed form z_0/(1 - t z_0/2) matches an independent RK4 to "
          "%.1e on the CIRCLE, and the solver matches the closed form to %.1e at "
          "t = 2.5 (amplitude %.3f)" % (e_formula, e_solver, np.max(np.abs(r["omega"]))))


def test_2_dissipation_exact():
    n = 256
    k = wavenumbers(n)
    worst = 0.0
    for s in (0.25, 0.5, 1.0, 1.5):
        g = FractionalGCLM(n=n, a=0.0, nu=0.05, s=s)
        g._rhs = lambda wh: np.zeros_like(wh)      # nonlinearity off
        w0 = np.sin(g.x) + 0.3 * np.sin(5 * g.x) - 0.2 * np.sin(11 * g.x)
        r = g.run(w0, t_end=0.7, amp_factor=1e12, sample_every=1000)
        want = np.fft.irfft(np.fft.rfft(w0)
                            * np.exp(-0.05 * np.abs(k) ** (2 * s) * r["t_final"]), n)
        worst = max(worst, float(np.max(np.abs(r["omega"] - want))))
    assert worst < 1e-13, worst
    print("[ok] (2) with the nonlinearity off the integrating factor reproduces "
          "exp(-nu|k|^{2s} t) to %.1e, at s = 0.25/0.5/1.0/1.5" % worst)


def test_3_blowup_time():
    n = N
    w0 = _w0(n)
    T = clm_blowup_time(w0)
    # the exact solution really does blow up there and not before
    before = float(np.max(np.abs(clm_exact(w0, T * (1 - 1e-3)))))
    early = float(np.max(np.abs(clm_exact(w0, T * 0.5))))
    assert before > 100 * early, (before, early)
    g = FractionalGCLM(n=n, a=0.0, nu=0.0, s=1.0)
    r = g.run(w0, amp_factor=1000.0, sample_every=5)
    Te = estimate_T(r)
    rel = abs(Te - T) / T
    assert rel < 5e-3, (Te, T, rel)
    print("[ok] (3) T = 2/max{H(w0): w0=0} = %.8f; the exact solution's amplitude "
          "grows %.0fx by T(1-1e-3), and a run recovers its own T to %.1e relative"
          % (T, before / early, rel))


def test_4_prediction_consistent():
    for alpha in (1.0, 1.3345, 2.0, 3.0):
        sc = float(critical_s(alpha))
        assert abs(relevance_exponent(sc, alpha)) < 1e-14
        assert abs(sc - alpha / 2) < 1e-14
    # the Navier-Stokes reading: beta = 1/2 <=> alpha = 2 <=> the Laplacian is critical
    assert abs(float(critical_s(2.0)) - 1.0) < 1e-14
    print("[ok] (4) s_c = alpha/2 and p = 1 - 2s/alpha agree (p(s_c) = 0); "
          "alpha = 2 gives s_c = 1 exactly -- the Laplacian is critical precisely at "
          "the NS scaling beta = 1/2")


def test_5_relevance_recovered():
    n = 4096
    w0 = _w0(n)
    ss = (0.25, 0.45, 0.65)
    ps = []
    for s in ss:
        g = FractionalGCLM(n=n, a=0.0, nu=1e-3, s=s)
        r = g.run(w0, amp_factor=1000.0, sample_every=5)
        ps.append(fit_relevance(r, estimate_T(r))["p"])
    slope = float(np.polyfit(np.array(ss), np.array(ps), 1)[0])
    assert abs(slope + 2.0) < 0.25, (slope, ps)
    for s, p in zip(ss, ps):
        assert abs(p - (1.0 - 2.0 * s)) < 0.15, (s, p)
    print("[ok] (5) at a = 0 (alpha = 1 exactly, nothing fitted) the measured "
          "relevance exponents %s track the prediction %s; slope %+.3f vs -2"
          % (["%+.3f" % p for p in ps], ["%+.3f" % (1 - 2 * s) for s in ss], slope))


def test_6_underresolution_reported():
    w_hi = FractionalGCLM(n=4096, a=0.0, nu=0.0, s=1.0).run(
        _w0(4096), amp_factor=400.0, sample_every=5)
    w_lo = FractionalGCLM(n=64, a=0.0, nu=0.0, s=1.0).run(
        _w0(64), amp_factor=400.0, sample_every=5)
    assert w_lo["max_tail"] > 1e4 * max(w_hi["max_tail"], 1e-30), (w_lo["max_tail"],
                                                                   w_hi["max_tail"])
    print("[ok] (6) the spectral-tail guard separates a starved run from a resolved "
          "one by %.0e (n=64: %.1e, n=4096: %.1e), so it can reject a result"
          % (w_lo["max_tail"] / max(w_hi["max_tail"], 1e-30), w_lo["max_tail"],
             w_hi["max_tail"]))


if __name__ == "__main__":
    test_1_known_answer()
    test_2_dissipation_exact()
    test_3_blowup_time()
    test_4_prediction_consistent()
    test_5_relevance_recovered()
    test_6_underresolution_reported()
    print("\nALL FRACTIONAL-GCLM TESTS PASSED")
