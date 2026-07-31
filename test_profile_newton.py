"""Gates for solver/profile_newton.py -- Newton on the two-scale profile.

  (1) THE KNOWN ANSWER.  At a = 0 the continuum solution is exact
      (Omega = -1/(1+X^2), c = 1/2); Newton from a perturbed start must find a
      zero of the DISCRETE system, which is nearby but not identical -- and must
      beat the exact continuum profile ON THAT SYSTEM, since the latter carries
      the discretization error.
  (2) THE DEGENERACY IS REAL.  The a = 0 zero set is a two-parameter family, so
      the one-gauge system is SINGULAR: solved directly it crawls (2e-5 after 40
      iterations).  The module fixes it twice over -- a second gauge AND a
      least-squares solve -- and the gate demonstrates the failure the direct
      one-gauge route actually has, so nobody re-derives it.
  (3) QUADRATIC CONVERGENCE, checked on the residual history.
  (4) THE JACOBIAN is the derivative it claims to be (finite differences).
  (5) CONTINUATION works and the residual stays at machine level well past the
      point where the GA floored at 1e-2.
  (6) FAILURE IS REPORTED.  Past the survival boundary Newton does not converge,
      and `converged` says so rather than returning the last iterate as success.

Run: .venv/bin/python test_profile_newton.py
"""

import numpy as np

from solver.profile_newton import TwoScaleNewton, continuation, derivative_matrix

N = 601


def test_1_known_answer():
    nw = TwoScaleNewton(a=0.0, n=N)
    ex = nw.anchor()
    exact_rms = float(np.sqrt(np.mean(nw.residual(ex, 0.5) ** 2)))
    r = nw.solve(om0=ex * 1.3 + 0.05 * np.exp(-nw.fam.X ** 2), c0=0.4)
    assert r["converged"], r["history"][-3:]
    assert r["residual_rms"] < 1e-12, r["residual_rms"]
    assert r["residual_rms"] < exact_rms, (r["residual_rms"], exact_rms)
    assert np.max(np.abs(r["Omega"] - ex)) < 5e-2
    print("[ok] (1) from a perturbed start Newton finds a DISCRETE zero: rms "
          "%.1e (the exact continuum anchor scores %.1e on the same system, its "
          "discretization error); profiles differ by %.1e, c = %.6f"
          % (r["residual_rms"], exact_rms, np.max(np.abs(r["Omega"] - ex)),
             r["c"]))


def test_2_two_gauges():
    nw = TwoScaleNewton(a=0.0, n=N)
    ex = nw.anchor()
    om0 = ex * 1.3 + 0.05 * np.exp(-nw.fam.X ** 2)
    good = nw.solve(om0=om0, c0=0.4)

    # one gauge, solved DIRECTLY (square system) -- the singular route
    om, c, n = om0.copy(), 0.4, nw.fam.n
    for _ in range(40):
        F = np.concatenate([nw.residual(om, c), [om[nw.i0] + 1.0]])
        J = nw.jacobian(om, c)[:n + 1]
        try:
            step = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            break
        t, base = 1.0, np.max(np.abs(F))
        while t > 1e-4:
            o2, c2 = om + t * step[:n], c + t * step[n]
            if np.max(np.abs(np.concatenate([nw.residual(o2, c2),
                                             [o2[nw.i0] + 1.0]]))) < base:
                break
            t *= 0.5
        om, c = om + t * step[:n], c + t * step[n]
    one = float(np.sqrt(np.mean(nw.residual(om, c) ** 2)))
    assert one > 1e6 * good["residual_rms"], (one, good["residual_rms"])
    print("[ok] (2) the two-parameter degeneracy is real: one gauge solved "
          "directly stalls at %.1e after 40 iterations, while two gauges in "
          "least squares reach %.1e in %d"
          % (one, good["residual_rms"], good["iterations"]))


def test_3_quadratic():
    nw = TwoScaleNewton(a=0.2, n=N)
    r = nw.solve()
    h = [x for x in r["history"] if x > 1e-14]
    ok = any(h[i + 1] < h[i] ** 1.5 for i in range(len(h) - 1))
    assert ok, h
    print("[ok] (3) convergence is quadratic at a = 0.2: %s"
          % " -> ".join("%.0e" % x for x in r["history"][:6]))


def test_4_jacobian():
    nw = TwoScaleNewton(a=0.3, n=201)
    om = nw.anchor() * 0.9
    c = 0.6
    J = nw.jacobian(om, c)
    n = nw.fam.n
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(4):
        h = rng.normal(size=n) * 1e-6 * np.max(np.abs(om))
        fd = (nw.residual(om + h, c) - nw.residual(om - h, c)) / 2.0
        an = J[:n, :n] @ h
        worst = max(worst, np.max(np.abs(fd - an)) / max(np.max(np.abs(fd)), 1e-30))
    dc = 1e-6
    fdc = (nw.residual(om, c + dc) - nw.residual(om, c - dc)) / (2 * dc)
    worst = max(worst, np.max(np.abs(fdc - J[:n, n])) / np.max(np.abs(fdc)))
    assert worst < 1e-6, worst
    print("[ok] (4) the analytic Jacobian matches finite differences to %.1e "
          "(both the Omega block and the c column)" % worst)


def test_5_continuation():
    rows = continuation([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], n=N)
    assert all(r["converged"] for r in rows), rows
    worst = max(r["relres"] for r in rows)
    best = min(r["relres"] for r in rows)
    assert worst < 1e-6, rows
    print("[ok] (5) continuation to a = 0.5: relres between %.1e and %.1e -- the "
          "GA's floor on the same quantity was ~1e-2, i.e. %.0f-%.0f orders of "
          "magnitude below it"
          % (best, worst, np.log10(1e-2 / worst), np.log10(1e-2 / best)))


def test_6_failure_reported():
    rows = continuation([0.0, 0.3, 0.6, 0.9], n=N)
    assert not rows[-1]["converged"], rows[-1]
    assert rows[-1]["relres"] > 1e3 * rows[1]["relres"]
    print("[ok] (6) past the boundary Newton fails and SAYS so: a = 0.9 reports "
          "converged=False with relres %.1e (vs %.1e at a = 0.3)"
          % (rows[-1]["relres"], rows[1]["relres"]))


if __name__ == "__main__":
    test_1_known_answer()
    test_2_two_gauges()
    test_3_quadratic()
    test_4_jacobian()
    test_5_continuation()
    test_6_failure_reported()
    print("\nALL PROFILE-NEWTON TESTS PASSED")
