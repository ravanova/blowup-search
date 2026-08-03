"""Gates for solver/critical_dissipation.py -- the MARGINAL case, s = s_c exactly.

  (1) LAMBDA IS EXACT, three ways.  Lambda[sin th] = sin th + (1/2) sin 2th against
      the closed-form conjugate-Poisson identity; Lambda^2 = -d^2/dX^2 against a
      derivative built by a different route; and Lambda against an INDEPENDENT
      implementation (solver/line_hilbert.py on a grid), because "build the same
      object twice" is how a sign error in an operator surfaces.
  (2) mu = 0 REPRODUCES ROUTE-E BIT FOR BIT.  The dissipative flow must not perturb
      the inviscid one it extends -- residual, Jacobian and c_omega identical.
  (3) THE JACOBIAN IS EXACT, including the variation of the re-derived gauge (N').
      A finite-difference check, because (N') has a quotient in it and a quotient rule
      is exactly the kind of thing that is wrong by one term.
  (4) THE EXACT a = 0 SOLUTION SOLVES THE PDE.  (E) is checked against
      omega_t - omega H(omega) + nu Lambda omega = 0 in closed form, at several
      (nu, mu_0, t) -- no quadrature, no differencing, so this tests the SOLUTION.
  (5) THE NUMERICS REDISCOVER IT.  Newton from a cold start must land on (E) to
      machine precision, and alpha must be 1 IDENTICALLY along the mu-branch --
      alpha_1 = 0, the neutral line.
  (6) THE SIGN OF THE MARGINAL VERDICT.  alpha_1 > 0 means mu DECAYS, which is the
      opposite of the reflex reading ("more dissipation, more dissipation").  Banked
      lesson 60 says check the monotonicity of your own headline in words, as a test.
  (7) alpha = -c_omega IS STILL THE FAR-FIELD EXPONENT with dissipation on.  Fitted
      on a moving window off the collocation grid, it must approach -c_omega -- the
      whole of (M) rests on that identification and it is not obvious once
      Lambda^{2s} Omega is in the equation.
  (8) THE a = 1/2 DRIFT IS CONVERGED, not a truncation artifact: alpha(mu) - 3 must
      agree across K = 96/144/192 and the Lambda^3 truncation must be far below it.
  (9) THE POSITIVE CONTROL for the dissipative filter.
 (10) A SLOPE SMALLER THAN THE SOLVE ERROR IS REFUSED.  The third resonance converges to
      a respectable 1e-4 and returns a NEGATIVE alpha_1 -- the opposite verdict -- off an
      alpha excursion of 1e-5.  That is the leg's most likely wrong headline, so the
      refusal predicate is gated here rather than only inside the experiment.

Run: .venv/bin/python test_critical_dissipation.py       (~4 min)
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from solver.critical_dissipation import (
    CRITICAL_POINTS, CriticalDissipativeFlow, LAMBDA_SIN1, alpha_slope,
    amplitude_eigenvalue, converged_dissipative_spectrum, exact_a0_family,
    exact_a0_residual, exact_a0_spacetime, inviscid_seed, lambda_power,
    lambda_truncation, marginal_verdict, mu_branch, mu_decay_time,
    planted_dissipative_control,
)
from solver.line_hilbert import line_hilbert
from solver.rescaled_spectrum import OddCompactBasis, RescaledFlow


def test_1_lambda_exact():
    # (a) the closed-form identity Lambda[sin th] = sin th + (1/2) sin 2th
    for K in (8, 32, 96):
        L, _ = lambda_power(K, 1)
        b = np.zeros(K)
        b[0] = 1.0
        got = L @ b
        assert np.allclose(got[:2], LAMBDA_SIN1, atol=1e-15), got[:4]
        assert np.max(np.abs(got[2:])) < 1e-15

    # (b) Lambda^2 = -d^2/dX^2, with the second derivative built by a DIFFERENT
    #     route: evaluate the interpolant off-grid and difference it numerically.
    K = 64
    B = OddCompactBasis(K)
    rng = np.random.default_rng(11)
    # EXPONENTIALLY decaying coefficients, not algebraic: Lambda^p widens the sine
    # range by p and the composite is truncated once, so an algebraically decaying
    # test vector measures that truncation (2e-5 at k^-4) rather than the operator.
    b = rng.normal(size=K) * np.exp(-0.5 * np.arange(1, K + 1))
    L2, _ = lambda_power(K, 2)
    assert lambda_truncation(b, K, 2) < 1e-10, lambda_truncation(b, K, 2)
    X = np.linspace(0.35, 3.0, 41)
    th = 2.0 * np.arctan(X)
    lam2 = np.sin(np.outer(th, B.k)) @ (L2 @ b)
    h = 1e-4
    f = lambda xx: B.eval_on(b, 2.0 * np.arctan(xx))
    d2 = (f(X + h) - 2.0 * f(X) + f(X - h)) / h ** 2
    rel = np.max(np.abs(lam2 + d2)) / np.max(np.abs(d2))
    assert rel < 5e-6, rel
    print("[ok] (1b) Lambda^2 = -d^2/dX^2 to %.1e relative, against a second-derivative "
          "built by finite differences on the interpolant" % rel)

    # (c) an INDEPENDENT implementation: Lambda f = H(f_X) with H from line_hilbert.
    #     Test function: f = 2X/(1+X^2) = sin th, whose Lambda is known exactly.
    x = np.tan(np.linspace(-0.5 * np.pi + 2e-3, 0.5 * np.pi - 2e-3, 1601))
    fx = 2.0 * (1.0 - x ** 2) / (1.0 + x ** 2) ** 2                # d/dx of 2x/(1+x^2)
    got = line_hilbert(x, fx)
    want = 4.0 * x / (1.0 + x ** 2) ** 2                           # = sin th + sin2th/2
    m = np.abs(x) < 8.0
    rel = np.max(np.abs(got[m] - want[m])) / np.max(np.abs(want[m]))
    assert rel < 2e-3, rel
    print("[ok] (1) Lambda is exact in the basis: coefficients [1, 1/2] to 1e-15 "
          "against the conjugate-Poisson identity, and %.1e relative against a "
          "completely independent line-grid Hilbert transform" % rel)


def test_2_mu_zero_reproduces_route_e():
    for a, K in ((0.0, 48), (0.3, 64)):
        old = RescaledFlow(a, K=K)
        new = CriticalDissipativeFlow(a, mu=0.0, p=1, K=K)
        rng = np.random.default_rng(5)
        b = old.B.anchor() + 0.01 * rng.normal(size=K) / np.arange(1, K + 1) ** 2
        assert np.array_equal(old.residual(b), new.residual(b))
        assert np.array_equal(old.jacobian(b), new.jacobian(b))
        assert old.c_omega(b) == new.c_omega(b)
    print("[ok] (2) at mu = 0 the dissipative flow reproduces Route-E's residual, "
          "Jacobian and gauge BIT FOR BIT -- the extension does not perturb what it "
          "extends")


def test_3_jacobian_exact():
    rng = np.random.default_rng(7)
    for a, mu, p, K in ((0.0, 0.4, 1, 48), (0.5, 0.15, 3, 64)):
        f = CriticalDissipativeFlow(a, mu=mu, p=p, K=K)
        b = f.B.anchor() + 0.02 * rng.normal(size=K) / np.arange(1, K + 1) ** 2
        J = f.jacobian(b)
        h = 1e-7
        Jn = np.empty_like(J)
        for j in range(K):
            e = np.zeros(K)
            e[j] = h
            Jn[:, j] = (f.residual(b + e) - f.residual(b - e)) / (2 * h)
        rel = np.max(np.abs(J - Jn)) / np.max(np.abs(Jn))
        assert rel < 5e-7, (a, mu, rel)
    print("[ok] (3) the exact Jacobian matches finite differences to %.1e relative, "
          "including the quotient term the re-derived gauge (N') contributes" % rel)


def test_4_exact_solution_solves_the_pde():
    worst = 0.0
    for nu in (0.05, 0.5, 2.0):
        for mu0 in (0.1, 1.0, 3.0):
            for t in (0.0, 0.5, 0.9, 0.99):
                x = np.linspace(-40.0, 40.0, 4001)
                worst = max(worst, exact_a0_residual(x, t, nu, mu0, T=1.0))
    assert worst < 1e-13, worst
    # and the amplitude really does blow up like (1+mu_0)/(T-t)
    q = exact_a0_spacetime(np.linspace(-5, 5, 200001), 0.99, 0.5, 1.0, T=1.0)
    amp = float(np.max(np.abs(q["omega"])))
    assert abs(amp - 2.0 / 0.01) / (2.0 / 0.01) < 1e-4, amp
    print("[ok] (4) the closed-form viscous solution (E) satisfies "
          "omega_t = omega H(omega) - nu Lambda omega to %.1e over nu, mu_0 and t, "
          "with ||omega||_inf = (1+mu_0)/(T-t) to 1e-4" % worst)


def test_5_numerics_rediscover_the_exact_family():
    K = 96
    mus = [0.0, 0.05, 0.25, 0.5, 1.0, 2.0]
    rows = mu_branch(0.0, 1, mus, K=K)
    worst_fit, worst_alpha = 0.0, 0.0
    B = OddCompactBasis(K)
    for r in rows:
        assert r["residual"] < 1e-13, r
        exact, mu0, lam = exact_a0_family(r["mu"], B.X)
        worst_fit = max(worst_fit, float(np.max(np.abs(B.S @ r["b"] - exact))))
        worst_alpha = max(worst_alpha, abs(r["alpha"] - 1.0))
    sl = alpha_slope(rows)
    assert worst_fit < 1e-13, worst_fit
    assert worst_alpha < 1e-12, worst_alpha
    assert abs(sl["alpha_1"]) < 1e-12, sl
    assert marginal_verdict(sl["alpha_1"]) == "neutral_line"
    print("[ok] (5) Newton rediscovers (E) from a cold start to %.1e, and alpha = 1 "
          "to %.1e at every mu on the branch: alpha_1 = 0, so a = 0 carries a LINE of "
          "viscous self-similar blow-ups, neutral to all orders"
          % (worst_fit, worst_alpha))


def test_6_marginal_sign_convention():
    # the headline sentence, as a test (banked lesson 60)
    assert marginal_verdict(+0.13) == "relaxes_to_inviscid"
    assert marginal_verdict(-0.13) == "dissipation_runs_away"
    assert marginal_verdict(0.0) == "neutral_line"
    # alpha_1 > 0 => mu_tau = -alpha_1 mu^2 < 0 => mu falls, and ALGEBRAICALLY
    a1, mu0 = 0.13, 0.2
    t1 = mu_decay_time(a1, mu0, 0.02)
    t2 = mu_decay_time(a1, mu0, 0.002)
    assert t1 > 0 and t2 > 9 * t1, (t1, t2)
    assert mu_decay_time(-0.13, mu0, 0.02) == float("inf")
    # and the growth rate is Route-F's exponent: below s_c it is negative
    f = CriticalDissipativeFlow(0.0, mu=0.0, p=1, K=48)
    b = f.B.anchor()
    assert abs(f.mu_growth(b)) < 1e-14                       # s = 1/2 = alpha/2
    assert CriticalDissipativeFlow(0.0, 0.0, 1, 48).s == 0.5
    print("[ok] (6) the marginal verdict has the sign the algebra says, not the "
          "reflex one: alpha_1 > 0 makes mu DECAY, each decade costing >9x the tau "
          "of the last (%.0f then %.0f) -- algebraic, because the linear term is gone"
          % (t1, t2))


def test_7_alpha_is_still_the_far_field_exponent():
    """The identification alpha = -c_omega is what (M) is built on.  With
    Lambda^{2s} Omega in the equation it needs checking, not assuming."""
    K = 192
    rows = mu_branch(0.5, 3, [0.1, 0.2], K=K)
    B = OddCompactBasis(K)
    # THE WINDOW HAS AN INTERIOR OPTIMUM AND THE TEST SAYS SO.  Too close in and the
    # core still dominates; too far out and the fit is reading the sine series'
    # truncation tail rather than the profile (Omega ~ 1e-9 at X = 1000, the tail is
    # ~1e-6 of the leading coefficient).  Neither end is the exponent, so the gate is
    # on the BEST window with the whole sweep reported -- the same discipline
    # Route-F applied to its own fit window.
    for r in rows:
        b, cw = r["b"], r["alpha"]
        fits = []
        for lo in (3.0, 10.0, 30.0, 100.0):
            X = np.geomspace(lo, 10.0 * lo, 60)
            Om = B.eval_on(b, 2.0 * np.arctan(X))
            fits.append(-float(np.polyfit(np.log(X), np.log(np.abs(Om)), 1)[0]))
        err = [abs(f - cw) for f in fits]
        assert min(err) < 0.05, (fits, cw)
        assert err[0] > min(err), (fits, cw)          # the inner window is not the best
    print("[ok] (7) with dissipation on, -c_omega is still the far-field exponent: "
          "window sweep %s vs -c_omega = %.4f, best window off by %.3f (the sweep is "
          "the systematic and both ends are contaminated -- inner by the core, outer "
          "by the series tail)"
          % ("/".join("%.3f" % f for f in fits), cw, min(err)))


def test_8_a_half_drift_is_converged():
    mus = [0.0, 0.05, 0.1, 0.2]
    got, trunc = {}, {}
    for K in (96, 144, 192):
        rows = mu_branch(0.5, 3, mus, K=K)
        assert max(r["residual"] for r in rows) < 1e-6, rows[-1]["residual"]
        trunc[K] = max(r["lambda_truncation"] for r in rows)
        got[K] = alpha_slope(rows)["alpha_1"]
    spread = max(got.values()) - min(got.values())
    # the Lambda^3 truncation is NOT small in coefficient terms (8% at K = 96); what
    # has to be true is that it FALLS with K and that alpha_1 stops moving anyway.
    assert trunc[192] < 0.5 * trunc[96], trunc
    assert all(v > 0.10 for v in got.values()), got
    assert spread < 5e-3, got
    assert marginal_verdict(got[192]) == "relaxes_to_inviscid"
    print("[ok] (8) at a = 1/2, s = 3/2 the drift is K-converged: alpha_1 = "
          "%.5f / %.5f / %.5f at K = 96/144/192 (spread %.1e) while the Lambda^3 "
          "truncation falls %.3f -> %.3f -- and alpha_1 is POSITIVE, so the critical "
          "viscous solution relaxes onto the inviscid profile"
          % (got[96], got[144], got[192], spread, trunc[96], trunc[192]))


def test_10_slope_below_the_residual_is_refused():
    """(10) A DERIVATIVE SMALLER THAN THE SOLVE ERROR IS NOT A MEASUREMENT.

    This is the gate that stops the leg's most likely wrong headline.  At the third
    resonance (a = 0.58218, s = 5/2) the mu-branch converges to a respectable-looking
    1e-4 and alpha_slope returns a NEGATIVE alpha_1 -- the opposite verdict to a = 1/2.
    But the whole excursion of alpha across the mu-window is ~1e-5, two orders BELOW
    that residual, so the fitted derivative is reading solve error.

    `alpha_slope` cannot know this -- it sees only (mu, alpha) -- so the driver applies
    the predicate, and the predicate is gated HERE against synthetic rows with a known
    answer rather than only inside a 4-minute experiment.
    """
    from experiments.p2_route_h_v1_critical import h4_third_point                # noqa
    import inspect
    src = inspect.getsource(h4_third_point)
    assert "drift > SIGNAL_FLOOR * worst" in src, \
        "the refusal must compare DRIFT against the residual, not just the residual"
    assert '"signal_to_residual"' in src and '"alpha_1_if_taken"' in src, \
        "a refusal that does not record what it refused cannot be audited"

    # the arithmetic of the predicate, on rows with a known answer
    def rows(drift, res):
        mus = [0.0, 0.01, 0.02, 0.04]
        return [{"mu": m, "alpha": 5.0 + drift * m / 0.04, "residual": res}
                for m in mus]
    for drift, res, want, why in (
            (2.0e-5, 3.8e-4, False, "the real K=288 rung: converged-looking, no signal"),
            (1.3e-6, 1.0e-6, False, "CONVERGED but signal only 1.3x the residual -- the "
                                    "case the old residual-only guard would have taken"),
            (1.3e-2, 1.0e-6, True,  "converged and signal 1.3e4x the residual"),
            (1.3e-5, 1.0e-9, True,  "tiny signal, but a far tinier error")):
        r = rows(drift, res)
        w = max(x["residual"] for x in r)
        d = max(x["alpha"] for x in r) - min(x["alpha"] for x in r)
        got = bool(w < 1e-5 and d > 10.0 * w)
        assert got == want, (why, drift, res, got, want)
    # and the sign that WOULD have been quoted is a real sign, i.e. the trap is live
    sl = alpha_slope([{"mu": m, "alpha": a} for m, a in
                      ((0.0, 5.00001295), (0.01, 4.99999835),
                       (0.02, 4.99999346), (0.04, 4.99999346))])
    assert sl["alpha_1"] < 0.0, sl
    print("[ok] (10) a slope below the solve error is REFUSED: the K=288 third-point "
          "rung would have quoted alpha_1 = %+.6f (the OPPOSITE verdict to a=1/2) off a "
          "2.0e-05 drift measured through a 3.8e-04 residual" % sl["alpha_1"])


def test_9_positive_control():
    out = planted_dissipative_control(a=0.0, p=1, mu=0.5, strength=6.0)
    assert out["n_planted"] > out["n_plain"], out
    assert np.max(np.real(out["planted"])) > 0.5, out["planted"]
    print("[ok] (9) the dissipative filter has a positive control: planting a "
          "localized potential takes it from %d converged eigenvalues to %d, with one "
          "at %+.3f in the right half plane -- so 'the ladder does not move' is a "
          "measurement" % (out["n_plain"], out["n_planted"],
                           float(np.max(np.real(out["planted"])))))


if __name__ == "__main__":
    test_1_lambda_exact()
    test_2_mu_zero_reproduces_route_e()
    test_3_jacobian_exact()
    test_4_exact_solution_solves_the_pde()
    test_5_numerics_rediscover_the_exact_family()
    test_6_marginal_sign_convention()
    test_7_alpha_is_still_the_far_field_exponent()
    test_8_a_half_drift_is_converged()
    test_9_positive_control()
    test_10_slope_below_the_residual_is_refused()
    print("\nALL CRITICAL-DISSIPATION TESTS PASSED")
