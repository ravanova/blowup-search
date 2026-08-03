"""Gates for solver/marginal_flow.py -- the marginal flow DRIVEN, not read off a branch.

  (1) THE AUGMENTED FLOW IS THE PREVIOUS LEG'S EQUATION, not a new one.  With mu frozen
      its Omega-part must be Route-H's residual pushed through S^{-1}, and at mu = 0 it
      must be Route-E's inviscid flow -- exactly, not approximately.  A leg whose whole
      claim is "the same equation, integrated instead of solved" has to show the
      equation did not change on the way.
  (2) THE COUPLED JACOBIAN IS EXACT, including the mu row and the mu column.  Newton
      inside an implicit stepper hides a wrong Jacobian as slow convergence rather than
      as a wrong answer, which is the failure mode that ships.
  (3) BDF2 IS SECOND ORDER.  Self-convergence on a dt-halving ladder, because there is
      no exact trajectory to compare against at a = 1/2.
  (4) THE a = 0 NEUTRAL LINE IS A LINE OF FIXED POINTS OF THE AUGMENTED FLOW.  Route-H
      proved alpha == 1 identically there, so mu_tau == 0 for EVERY mu: the integrator
      must sit still on a one-parameter family it was never told about.  This is the
      leg's one exact-answer gate and it tests both equations at once.
  (5) THE GAUGE IS AN INVARIANT AND THE PROJECTION DOES NO WORK.  sum_k k b_k = -1 is
      conserved analytically; the module enforces it numerically.  Both halves are
      gated -- that it holds, and that turning the enforcement OFF moves the headline
      by well under a percent.  A projection doing real work would be a bug wearing a
      fix's clothes.
  (6) lambda_mu = 2s - alpha_0 MEASURED AS A GROWTH RATE.  Route-F's critical exponent
      arrived as the slope of a fitted power law in a periodic pseudo-spectral run;
      here it is d(log mu)/d tau of a compactified steady-basis trajectory.  Four s,
      two signs, prediction from a number this computation never sees.
  (7) alpha_1 DYNAMIC vs STATIC, AT MATCHED K.  The previous leg extrapolated secants of
      a frozen-mu Newton branch; this one takes the slope of 1/mu along a trajectory.
      Nothing is shared but the residual.
  (8) THE STABILITY INVERSION, AND THE CROSSOVER THAT SHOWS IT IS NOT TRUNCATION.
      mu = 0 has ~K unstable directions and any mu > 0 has none; the crossover sits
      where mu K^p ~ max Re, so it moves LEFT with K.  An artifact would not.
  (9) THE NONLINEAR CONTROL.  Eigenvalues of a truncated generator are a claim about a
      matrix; twin trajectories through the nonlinear flow are a claim about the flow.
      The decay rate must match the spectral gap, and the mu = 0 rate must be positive.
 (10) THE REFUSAL PREDICATE, AND THE REASON THE GROWTH RATE IS A LOWER BOUND.  A number
      read off a trajectory is refused unless it exceeds the spread the time step puts
      on it.  And the leading inviscid eigenvalue is 4.55 + 430i, so no integrator with
      a usable dt can realize it -- the measured growth rate is a bound, and the gate
      records the frequency that makes it one.

Run: .venv/bin/python test_marginal_flow.py       (~5 min)
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from solver.critical_dissipation import (
    CriticalDissipativeFlow, alpha_slope, inviscid_seed, marginal_verdict, mu_branch,
)
from solver.marginal_flow import (
    AugmentedFlow, admissible_direction, crossover_mu, dt_ladder,
    dynamic_alpha_1, dynamic_lambda_mu,
    frequency_profile, integrate, perturbation_decay, resolution_guard,
    stability_ladder, stability_verdict, tar_pit_law, unstable_count,
)
from solver.rescaled_spectrum import RescaledFlow


def test_1_reduces_to_the_previous_legs():
    K = 64
    b = inviscid_seed(0.3, K=K)[0]
    rng = np.random.default_rng(0)
    b = b + 1e-3 * rng.standard_normal(K) * np.exp(-0.3 * np.arange(K))

    # (a) mu frozen: the Omega-part is Route-H's residual through S^{-1}
    for mu, p in ((0.0, 1), (0.4, 1), (0.4, 3)):
        A = AugmentedFlow(0.3, p, K=K, gauge_project=False, freeze_mu=True)
        f = CriticalDissipativeFlow(0.3, mu=mu, p=p, K=K)
        got = A.rhs(np.concatenate([b, [mu]]))[:K]
        want = np.linalg.solve(f.B.S, f.residual(b))
        # RELATIVE: the module caches S^{-1} and this builds it by a solve, so the two
        # differ at roundoff times |R|, which is 1e5 here because Lambda^3 weights by k^3
        rel = float(np.max(np.abs(got - want))) / (float(np.max(np.abs(want))) + 1e-300)
        assert rel < 1e-12, (mu, p, rel)

    # (b) mu = 0: Route-E's inviscid flow, untouched
    A = AugmentedFlow(0.3, 3, K=K, gauge_project=False)
    e = RescaledFlow(0.3, K=K)
    got = A.rhs(np.concatenate([b, [0.0]]))
    want = np.linalg.solve(e.B.S, e.residual(b))
    assert np.max(np.abs(got[:K] - want)) / np.max(np.abs(want)) < 1e-12
    assert abs(got[K]) < 1e-300, "mu = 0 must be a fixed point of (M) for any Omega"
    print("  (1) reduction to Route-H (mu frozen) and Route-E (mu = 0): exact  OK")


def test_2_coupled_jacobian_is_exact():
    rng = np.random.default_rng(1)
    for a, p, K, mu in ((0.0, 1, 48, 0.7), (0.5, 3, 64, 0.25), (0.5, 2, 64, 0.05)):
        A = AugmentedFlow(a, p, K=K, gauge_project=False)
        b = inviscid_seed(a, K=K)[0]
        y = np.concatenate([b, [mu]])
        J = A.jacobian(y)
        worst = 0.0
        for _ in range(3):
            v = rng.standard_normal(K + 1)
            v /= np.linalg.norm(v)
            eps = 1e-7
            fd = (A.rhs(y + eps * v) - A.rhs(y - eps * v)) / (2 * eps)
            an = J @ v
            worst = max(worst, float(np.max(np.abs(fd - an)))
                        / (float(np.max(np.abs(an))) + 1e-300))
        assert worst < 1e-7, (a, p, mu, worst)
        print(f"  (2) a={a} p={p} mu={mu}: coupled Jacobian rel err {worst:.2e}  OK")


def test_3_bdf2_is_second_order():
    L = dt_ladder(0.5, 3, 96, 0.3, 60.0, [1.0, 0.5, 0.25, 0.125],
                  mu_max=0.3, n_sample=120)
    assert 1.7 < L["observed_order"] < 2.3, L["observed_order"]
    print(f"  (3) BDF2 self-convergence order {L['observed_order']:.3f} "
          f"(alpha_1 spread {L['spread']:.2e} over dt = 1 .. 1/8)  OK")


def test_4_a0_neutral_line_is_a_line_of_fixed_points():
    K = 96
    rows = mu_branch(0.0, 1, [0.25, 0.5, 1.0, 2.0, 4.0], K=K)
    worst_mu = worst_b = 0.0
    for r in rows:
        A = AugmentedFlow(0.0, 1, K=K)
        rec = integrate(A, r["b"], r["mu"], 40.0, 0.5, n_sample=20)
        worst_mu = max(worst_mu, abs(rec["mu_end"] - r["mu"]))
        worst_b = max(worst_b, float(np.max(np.abs(rec["b_end"] - r["b"]))))
    assert worst_mu < 1e-10, worst_mu
    assert worst_b < 1e-10, worst_b
    print(f"  (4) a = 0 line of viscous blow-ups, mu = 0.25 .. 4 held for tau = 40: "
          f"worst |dmu| {worst_mu:.1e}, worst |dOmega| {worst_b:.1e}  OK")


def test_5_gauge_is_an_invariant_and_the_projection_does_no_work():
    K = 96
    b = mu_branch(0.5, 3, [0.1, 0.2, 0.3], K=K)[-1]["b"]
    on = integrate(AugmentedFlow(0.5, 3, K=K, gauge_project=True),
                   b, 0.3, 60.0, 0.25, n_sample=60)
    off = integrate(AugmentedFlow(0.5, 3, K=K, gauge_project=False),
                    b, 0.3, 60.0, 0.25, n_sample=60)
    rel = abs(on["mu_end"] - off["mu_end"]) / on["mu_end"]
    assert abs(on["gauge_drift"]) < 1e-11, on["gauge_drift"]
    assert abs(off["gauge_drift"]) > 10 * abs(on["gauge_drift"]), "projection is a no-op"
    assert rel < 1e-2, rel
    assert on["gauge_violation"] < 1e-8, on["gauge_violation"]
    print(f"  (5) gauge drift {on['gauge_drift']:+.1e} (projected) vs "
          f"{off['gauge_drift']:+.1e} (not); headline moves {rel * 100:.3f}%; "
          f"worst |cos(db, gauge)| {on['gauge_violation']:.1e}  OK")


def test_6_lambda_mu_is_measured_as_a_growth_rate():
    K, a, alpha_0 = 96, 0.5, 3.0
    worst = 0.0
    for p in (1, 2, 4, 5):
        b = mu_branch(a, p, [2e-3], K=K)[0]["b"]
        rec = integrate(AugmentedFlow(a, p, K=K), b, 2e-3, 3.0, 0.02, n_sample=60)
        got = dynamic_lambda_mu(rec)["lambda_mu"]
        want = p - alpha_0                     # 2s - alpha_0, s = p/2
        worst = max(worst, abs(got - want))
        print(f"  (6) p={p} (s={p / 2}): lambda_mu predicted {want:+.3f}, "
              f"measured {got:+.5f}")
        assert abs(got - want) < 0.02, (p, got, want)
    assert worst < 0.02
    print(f"  (6) worst deviation {worst:.4f} over two signs and four s  OK")


def test_7_alpha_1_dynamic_vs_static():
    K = 96
    mus = [0.0, 0.02, 0.05, 0.1, 0.15, 0.2]
    static = alpha_slope(mu_branch(0.5, 3, mus, K=K))["alpha_1"]
    b = mu_branch(0.5, 3, [0.1, 0.2, 0.3], K=K)[-1]["b"]
    rec = integrate(AugmentedFlow(0.5, 3, K=K), b, 0.3, 120.0, 0.25, n_sample=240)
    dyn = dynamic_alpha_1(rec, mu_max=0.3)["alpha_1"]
    rel = abs(dyn - static) / abs(static)
    assert rel < 5e-3, (dyn, static, rel)
    assert marginal_verdict(dyn) == "relaxes_to_inviscid"
    assert marginal_verdict(static) == "relaxes_to_inviscid"
    # and the closed law is the one that was integrated
    law = tar_pit_law(dyn, 0.3, rec["tau_end"])
    assert abs(law - rec["mu_end"]) / rec["mu_end"] < 5e-3, (law, rec["mu_end"])
    print(f"  (7) alpha_1 static {static:.6f} vs dynamic {dyn:.6f} at K={K}: "
          f"{rel * 100:.3f}% apart; both verdict 'relaxes_to_inviscid'  OK")


def test_8_stability_inversion_and_its_crossover():
    mus = [0.0, 1e-6, 1e-5, 1e-4, 1e-3]
    brackets = {}
    for K in (48, 96):
        rows = stability_ladder(0.5, 3, K, mus)
        inv, vis = rows[0], rows[-1]
        assert inv["n_unstable"] > K // 2, (K, inv["n_unstable"])
        assert vis["n_unstable"] <= 1, (K, vis["n_unstable"])
        assert stability_verdict([inv, vis]) == \
            "dissipation_removes_all_unstable_directions"
        brackets[K] = crossover_mu(rows)
        g = resolution_guard(0.5, 3, K, 1e-3, g=inv["max_re"])
        pred = g["K_required"]
        print(f"  (8) K={K}: mu=0 -> {inv['n_unstable']} unstable (max Re "
              f"{inv['max_re']:+.3f}), mu=1e-3 -> {vis['n_unstable']}; crossover in "
              f"{brackets[K]['bracket']}, (C) predicts "
              f"{inv['max_re'] / K ** 3:.1e}")
        assert pred < K, (K, pred)
    # the crossover MOVES LEFT with K -- an artifact would not
    assert brackets[96]["geometric_mid"] < brackets[48]["geometric_mid"], brackets
    ratio = brackets[48]["geometric_mid"] / brackets[96]["geometric_mid"]
    assert ratio > 2.0, ratio
    print(f"  (8) crossover falls by x{ratio:.1f} from K=48 to K=96 "
          f"((C) predicts x{(96 / 48) ** 3:.0f})  OK")


def test_9_nonlinear_control_matches_the_spectral_gap():
    K = 96
    gap = unstable_count(0.5, 3, K, 0.05)["gap"]
    r = perturbation_decay(0.5, 3, K, 0.05, eps=1e-8, tau_end=6.0, dt=0.01)
    rel = abs(r["rate"] - gap) / abs(gap)
    assert r["rate"] < 0 and rel < 0.05, (r["rate"], gap, rel)
    r0 = perturbation_decay(0.5, 3, K, 0.0, eps=1e-9, tau_end=6.0, dt=0.01)
    assert r0["rate"] > 0.5, r0["rate"]
    assert r0["growth_factor"] > 1e3, r0["growth_factor"]
    print(f"  (9) mu=0.05: twin-trajectory rate {r['rate']:+.4f} vs spectral gap "
          f"{gap:+.4f} ({rel * 100:.1f}%); mu=0: rate {r0['rate']:+.3f}, kick grows "
          f"x{r0['growth_factor']:.1e}  OK")


def test_10_refusal_predicate_and_the_lower_bound():
    # (a) a number is refused unless it beats the discretization spread
    L = dt_ladder(0.5, 3, 96, 0.3, 60.0, [1.0, 0.5, 0.25], mu_max=0.3, n_sample=120)
    assert L["signal_over_discretization"] > 10, L
    thin = dynamic_alpha_1({"tau": [0.0, 1.0], "mu": [0.3, 0.29]})
    assert thin["refused"] and np.isnan(thin["alpha_1"])
    # (b) the leading inviscid eigenvalue is unreachable by any usable dt
    fp = frequency_profile(0.5, 3, 96, 0.0)
    assert abs(fp["im_of_max_re"]) > 100.0, fp["im_of_max_re"]
    assert fp["caps"]["10.0"]["max_re"] < 0.4 * fp["max_re"], fp["caps"]
    r0 = perturbation_decay(0.5, 3, 96, 0.0, eps=1e-9, tau_end=4.0, dt=0.01)
    assert r0["rate"] < fp["max_re"], "the generic rate must not exceed max Re"
    print(f"  (10) signal/discretization {L['signal_over_discretization']:.0f}; "
          f"leading inviscid eigenvalue {fp['max_re']:+.3f} "
          f"{fp['im_of_max_re']:+.1f}i, max Re at |Im|<=10 is only "
          f"{fp['caps']['10.0']['max_re']:+.3f}, measured generic rate "
          f"{r0['rate']:+.3f}  OK")


def test_11_small_is_norm_dependent_and_divergence_is_refused():
    """(11) TWO FAILURES THAT SHIPPED A NaN INTO A FIGURE LEGEND, BOTH GATED.

    (a) "eps = 1e-3" is meaningless until you say IN WHICH NORM.  The off-branch start
        drew a perturbation with a decaying spectrum and scaled it to max|v_k| = 1 --
        small in the COEFFICIENT sup-norm.  But the gauge (N') carries
        b -> (Lambda^p Omega)_X(0), and Lambda^p weights mode k by ~k^p with one more
        power from the derivative at the origin, so that "1e-3" was a ~1e5 RELATIVE
        perturbation of the quantity the flow divides by.  alpha came back 11713 instead
        of 3.04 AT tau = 0.  `admissible_direction` normalizes in that functional, and
        this gate measures the ratio between the two normalizations so the correction
        cannot be quietly dropped.  (Banked lesson 66.)

    (b) A DIVERGED TRAJECTORY MUST BE REFUSED, NOT RETURNED.  `_implicit_step` has a
        stagnation stop and therefore returns steps whose Newton never converged; those
        compound into NaN.  `integrate` now reports `converged`, and the driver records
        a refusal instead of emitting `alpha_1 = nan` -- which it did, into a published
        figure legend, until this gate existed.  (Banked lesson 65.)
    """
    A_CRIT, P_CRIT, K = 0.5, 3, 96
    A = AugmentedFlow(A_CRIT, P_CRIT, K=K)
    b = mu_branch(A_CRIT, P_CRIT, [0.05, 0.1, 0.2, 0.3], K=K)[-1]["b"]
    lam = A.flow.lam_dx0

    # (a) the two normalizations differ by orders of magnitude, and the fix binds
    naive = np.random.default_rng(7).standard_normal(K) * np.exp(-0.25 * np.arange(K))
    naive = naive - (A.kk @ naive) / (A.kk @ A.kk) * A.kk
    naive = naive / np.max(np.abs(naive))
    ratio = abs(float(lam @ naive)) / abs(float(lam @ b))
    assert ratio > 1e3, f"the trap is supposed to be large; got {ratio:.2e}"

    good = admissible_direction(A, b, seed=7)
    assert abs(abs(float(lam @ good)) / abs(float(lam @ b)) - 1.0) < 1e-9, \
        "admissible_direction must normalize IN the gauge functional"
    assert abs(float(A.kk @ good)) < 1e-9 * float(np.max(np.abs(good))), \
        "the gauge direction must still be projected out"

    # alpha at the perturbed state is sane for the admissible direction and absurd for
    # the naive one -- the whole point, measured rather than asserted
    y_good = np.concatenate([b + 1e-3 * good, [0.3]])
    y_bad = np.concatenate([b + 1e-3 * naive, [0.3]])
    a_ref, a_good, a_bad = A.alpha(np.concatenate([b, [0.3]])), A.alpha(y_good), A.alpha(y_bad)
    assert abs(a_good - a_ref) < 0.05 * abs(a_ref), (a_ref, a_good)
    assert abs(a_bad - a_ref) > 100.0 * abs(a_ref), (a_ref, a_bad)

    # (b) a diverged run is flagged, not returned as a number
    bad = integrate(AugmentedFlow(A_CRIT, P_CRIT, K=K), b + 1e-3 * naive, 0.3, 60.0,
                    0.25, n_sample=60)
    assert bad["converged"] is False, "a diverged trajectory must NOT report converged"
    ok = integrate(AugmentedFlow(A_CRIT, P_CRIT, K=K), b, 0.3, 60.0, 0.25, n_sample=60)
    assert ok["converged"] is True and np.isfinite(ok["mu_end"]), ok["mu_end"]
    print(f"  (11a) coefficient-normalized perturbation is {ratio:.1e}x too large in the "
          f"gauge functional: alpha {a_ref:.3f} -> {a_bad:.3e} (naive) vs {a_good:.3f} "
          f"(admissible)")
    print(f"  (11b) the diverged run is REFUSED (converged=False), the on-branch run is "
          f"kept (mu_end={ok['mu_end']:.6f})  OK")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_reduces_to_the_previous_legs,
               test_2_coupled_jacobian_is_exact,
               test_3_bdf2_is_second_order,
               test_4_a0_neutral_line_is_a_line_of_fixed_points,
               test_5_gauge_is_an_invariant_and_the_projection_does_no_work,
               test_6_lambda_mu_is_measured_as_a_growth_rate,
               test_7_alpha_1_dynamic_vs_static,
               test_8_stability_inversion_and_its_crossover,
               test_9_nonlinear_control_matches_the_spectral_gap,
               test_10_refusal_predicate_and_the_lower_bound,
               test_11_small_is_norm_dependent_and_divergence_is_refused):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.0f}s)")
