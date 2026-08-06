"""Leg 85 / Route-GRA — permanent adversarial regression test for gclm_rescaled.py's
relaxation loop's CONVERGENCE REPORTING.

Companion to test_gclm_rescaled.py, which checks that the module relaxes to the exact CLM
self-similar fixed point ON WELL-BEHAVED DATA (every trajectory there has f(0) = -4).  This
file asks the complementary question, and it is the gate of leg 85:

    Under an adversarial battery of non-convergent upwind-transport trajectories (sustained
    oscillation, slow drift near a saddle rather than the fixed point), does
    solver/gclm_rescaled.py's relaxation loop ever report having reached the fixed point when
    it has not?

LEG 85'S MEASURED ANSWER: YES, on one specific branch -- 4 of 25 trajectories, all in the
amplitude-gauge family (lambda = 1e-6, 1e-8, 1e-9, 1e-10).

*** THE DEFECT IS NOW REPAIRED (bench repair, `Leg 0: ORCH`), AND THIS FILE IS INVERTED. ***
Leg 85 was forbidden from patching solver/gclm_rescaled.py under its own authority, so its
assertions locked in the defect AS MEASURED, with the instruction: "if this test fails because
the drift is now small, the defect has been REPAIRED: delete this test and assert the repaired
predicate instead.  Do not loosen it."  That is exactly what has been done here.  The repair
makes run()'s stopping test RELATIVE to the frozen gauge -- `res < tol * max(|f(0)|/4, floor)`
-- so it is scale-invariant along the direction the module declares free.

The inversion is exact, in the sense of leg 84's precedent: every magnitude leg 85 measured is
still asserted, at the same threshold, with only the SIGN of the claim flipped.  The two
pinned-defect gates become pinned-repair gates (test_gauge_false_positive_is_repaired,
test_repair_is_resolution_independent); the four ROBUST gates, which the repair was required
not to disturb, are untouched and re-run as regression controls.

Before -> after on leg 85's four false positives (n=601, tol=1e-8, post-stop relative drift over
4000 steps; a genuinely relaxed trajectory scores ~2e-9):

    lambda    steps before -> after     drift before -> after
    1e-06        924 -> 1664            1.216e-03 -> 1.217e-09
    1e-08        670 -> 1664            1.299e-01 -> 1.209e-09
    1e-09          1 -> 1664            1.000e+00 -> 1.209e-09
    1e-10          1 -> 1664            1.000e+00 -> 1.209e-09

NOTE, and it matters for reading the assertions below: post-repair these trajectories still do
NOT land on Omega_0, and their rate is still c_omega = +1.  That is not a residual bug.  A
small-amplitude datum lambda*(-4 exp(-X^2/2)) is NOT the gauge-line member Omega_lambda (whose
peak amplitude is 1 at every lambda); in the small-amplitude limit the equation linearizes to
pure outward advection f_tau = -tanh(rho) f_rho, whose steady state is f == f(0) (measured
non-flatness 5.1e-08) and whose rate is genuinely c_omega = 1 - H Omega(0) -> +1.  So the
returned state IS at rest and the reported rate IS its true rate.  What the repair fixed is the
HONESTY of the `converged` flag -- converged=True now means the state has actually stopped
moving relative to its own amplitude -- not which fixed point a given datum flows to.

THE MECHANISM.  The rescaled CLM fixed point is a ONE-PARAMETER LINE, not a point: the
dilation term X d/dX is scale-invariant, so Omega_lambda(X) = Omega_0(lambda X) is an exact
steady state for every lambda > 0.  The member is selected by the origin slope
f(0) = -4 lambda, which the scheme freezes exactly, and the module's docstring tells callers
"the rescaled initial amplitude is a free gauge".  The residual ||f_tau||_inf scales LINEARLY
in lambda; `tol` is a fixed ABSOLUTE number.  So the stopping test is not scale-invariant
along the one direction the module declares free, and for lambda below ~tol/3 it is satisfied
by the INITIAL DATA -- the loop returns converged=True after ONE step, having relaxed nothing.

THE GAUGE-INVARIANT MEASURE used throughout is post-stop relative drift: how far the RETURNED
state still moves, as a fraction of its own amplitude.  A genuinely relaxed trajectory scores
~2e-9.  The failing trajectory scored 1.0 -- it subsequently changed by its entire amplitude.
It is this measure, not the raw residual, that the repaired gates are scored against, because
it is the one quantity in the file that does not itself carry the gauge.

RUNTIME went 11 s -> ~6 min across the inversion, and that increase is the finding: the four
gauge trajectories used to stop after 1-924 steps on a tolerance their initial data already
met, and now actually relax (1664 steps at n=601).  The cost is the work that was being skipped.

Run: python test_gclm_rescaled_adversarial.py
"""

import numpy as np

from solver.gclm_rescaled import GAUGE_TOL_FLOOR, RescaledCLM, clm_profile

DRIFT_STEPS = 2000


def _gauss(X, lam=1.0):
    """lam * (the validated initial datum). Freezes f(0) = -4*lam, i.e. gauge member lam."""
    return lam * (-4.0 * np.exp(-X ** 2 / 2.0))


def _post_stop_drift(s, r, nsteps=DRIFT_STEPS, dt_frac=0.4):
    """||f(after nsteps more) - f_returned||_inf / ||f_returned||_inf.  Gauge-invariant."""
    f0 = np.asarray(r["f"], dtype=float).copy()
    assert np.all(np.isfinite(f0)), "non-finite state handed to the drift measure"
    scale = float(np.abs(f0).max())
    if scale == 0.0:
        return 0.0
    f = f0.copy()
    dt = dt_frac * s.drho
    for _ in range(nsteps):
        f, _, _ = s.step(f, dt)
    return float(np.abs(f - f0).max() / scale)


def _shape_err(omega, X, radius=5.0):
    exact = clm_profile(X)
    core = np.abs(X) < radius
    core[:3] = False
    core[-3:] = False
    return float(np.abs(omega[core] - exact[core]).max())


def test_gauge_line_is_real():
    """Omega_lambda(X) = Omega_0(lambda X) is an exact steady state for every lambda.

    This is the premise of the whole audit: the fixed point is a LINE.  If this ever fails,
    the rest of this file is asking the wrong question.

    lambda is capped at 2 here for a numerical, not a structural, reason: Omega_lambda has
    width ~1/lambda, so narrow members are under-resolved on a fixed grid and their DISCRETE
    residual grows with lambda (measured: 2.1e-06 at lambda=0.25 rising to 6.9e-03 at
    lambda=4 on n=601).  The gauge line itself is exact at every lambda."""
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)
    for lam in (0.25, 0.5, 1.0, 2.0):
        f = -4.0 * lam / (1.0 + 4.0 * (lam * s.X) ** 2)
        L, c_omega = s.rhs(f)
        res = float(np.abs(L).max())
        print(f"    lambda={lam:5.2f}  ||f_tau||_inf={res:.2e}  c_omega={c_omega:+.5f}")
        assert res < 1e-3, f"Omega_lambda not steady at lambda={lam}: residual {res:.2e}"
        assert abs(c_omega + 1.0) < 2e-2, f"c_omega {c_omega:+.5f} != -1 at lambda={lam}"
    print("[ok] the fixed point is a one-parameter LINE, all members at the exact rate -1")


def test_residual_is_degree_one_in_the_gauge():
    """||f_tau||_inf scales LINEARLY in lambda while tol is a fixed absolute number.

    This is the mechanism of the false positive, measured directly."""
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)
    base = _gauss(s.X)
    ratios = []
    for lam in (1e-3, 1e-6, 1e-9):
        res = float(np.abs(s.rhs(lam * base)[0]).max())
        ratios.append(res / lam)
        print(f"    lambda={lam:8.1e}  residual={res:.4e}  residual/lambda={res / lam:.4f}")
    # the small-lambda limit is the pure linear-advection residual: a lambda-independent constant
    assert abs(ratios[1] - ratios[2]) / ratios[2] < 1e-3, (
        f"residual not asymptotically degree-1 in the gauge: {ratios}")
    assert 2.0 < ratios[-1] < 4.0, f"residual/lambda drifted from its measured 2.94: {ratios[-1]}"
    print(f"[ok] residual = {ratios[-1]:.3f} * lambda -- an ABSOLUTE tol=1e-8 would be met by "
          f"DATA alone for lambda < {1e-8 / ratios[-1]:.2e}; the repaired test is tol*lambda, "
          "which is degree-1 on both sides and so scale-invariant")


def test_validated_gauge_is_honest():
    """CONTROL: at the validated gauge f(0) = -4 the loop's report is trustworthy.

    Nothing already banked in this repository is impugned by this leg, and this test is what
    says so.  Both a relaxed trajectory and a still-drifting one are reported correctly.

    POST-REPAIR this is also the ZERO-REGRESSION gate: at f(0) = -4 the gauge multiplier is
    EXACTLY 1.0, so the repaired stopping test `res < tol * max(|f(0)|/4, floor)` is the same
    float comparison as the old `res < tol`, and every number below is unchanged (independently
    confirmed: test_gclm_rescaled.py's full output is character-identical across the repair)."""
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)

    r = s.run(_gauss(s.X), dt_frac=0.4, tol=1e-8, max_steps=20000)
    assert r["gauge"] == 1.0, f"validated gauge multiplier is {r['gauge']!r}, not exactly 1.0"
    assert r["tol_effective"] == 1e-8, (
        f"tol_effective is {r['tol_effective']!r}, not exactly the requested tol -- the repair "
        "is supposed to be a bit-exact no-op at f(0) = -4")
    drift = _post_stop_drift(s, r)
    err = _shape_err(r["omega"], s.X)
    print(f"    relaxing:  conv={bool(r['converged'])} steps={r['steps']} "
          f"c_omega={r['c_omega']:+.5f} shape_err={err:.2e} post-stop drift={drift:.3e}")
    assert r["converged"], "the validated datum did not converge"
    assert drift < 1e-6, f"reported converged but still drifting by {drift:.3e}"
    assert err < 1e-3, f"shape err {err:.2e} at the validated gauge"
    assert abs(r["c_omega"] + 1.0) < 5e-3, f"rate {r['c_omega']} != -1"

    # a trajectory that is genuinely still drifting IS reported as not converged
    f0 = _gauss(s.X) + 0.5 * np.exp(-(np.abs(s.X) - 40.0) ** 2 / 8.0) * np.sign(s.X)
    r2 = s.run(f0, dt_frac=0.4, tol=1e-8, max_steps=4000)
    print(f"    far bump:  conv={bool(r2['converged'])} steps={r2['steps']} "
          f"residual={r2['residual']:.3e}")
    assert not r2["converged"], "a still-drifting far-field trajectory was reported converged"
    print("[ok] at f(0) = -4 the convergence report is trustworthy in both directions")


def test_nonfinite_is_never_reported_converged():
    """NaN/overflow never sneaks through `res < tol`.  This one is ROBUST -- lock it in."""
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)
    cases = {}
    with np.errstate(all="ignore"):
        cases["past_cfl_limit"] = s.run(_gauss(s.X), dt_frac=3.0, tol=1e-8, max_steps=2000)
        cases["overflow"] = s.run(-4e6 * np.exp(-s.X ** 2 / 2.0), dt_frac=0.4, tol=1e-8,
                                  max_steps=2000)
        seed = _gauss(s.X)
        seed[np.abs(s.X) < 0.1] = np.nan
        cases["nan_seed"] = s.run(seed, dt_frac=0.4, tol=1e-8, max_steps=2000)
    for name, r in cases.items():
        print(f"    {name:16s} residual={r['residual']} converged={bool(r['converged'])}")
        assert not np.isfinite(r["residual"]), f"{name} unexpectedly stayed finite"
        assert not r["converged"], f"{name}: NON-FINITE residual REPORTED CONVERGED"
    print("[ok] non-finite residuals are never reported as convergence (no NaN bypass)")


def test_oscillation_does_not_trip_the_stopping_test():
    """Sustained oscillation / marginal time steps do not produce a premature stop.

    Also ROBUST: up to dt_frac = 1.5 the loop converges to the right answer, and beyond the
    stability limit it goes non-finite and reports not-converged (previous test)."""
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)
    for dtf in (1.0, 1.5):
        r = s.run(_gauss(s.X), dt_frac=dtf, tol=1e-8, max_steps=6000)
        drift = _post_stop_drift(s, r, dt_frac=dtf)
        err = _shape_err(r["omega"], s.X)
        print(f"    dt_frac={dtf:3.1f} conv={bool(r['converged'])} steps={r['steps']} "
              f"shape_err={err:.2e} post-stop drift={drift:.3e}")
        assert r["converged"] and err < 1e-3, f"dt_frac={dtf} did not land on Omega_0"
        assert drift < 1e-6, f"dt_frac={dtf}: reported converged while drifting {drift:.3e}"
    # a high-wavenumber modulation (f(0) = -5.2, i.e. gauge member lambda = 1.3) still lands on
    # a genuine steady state -- the gauge member 1.3, which is 13% from Omega_0 in shape but
    # carries the correct rate.  Honest, and NOT counted as a false positive.
    r = s.run(_gauss(s.X) * (1.0 + 0.3 * np.cos(6.0 * s.rho)), dt_frac=0.4, tol=1e-8,
              max_steps=20000)
    drift = _post_stop_drift(s, r)
    print(f"    mode-6 modulation: conv={bool(r['converged'])} c_omega={r['c_omega']:+.5f} "
          f"shape_err={_shape_err(r['omega'], s.X):.3e} post-stop drift={drift:.3e}")
    assert r["converged"] and drift < 1e-6, "mode-6 datum reported converged while drifting"
    assert abs(r["c_omega"] + 1.0) < 5e-3, "mode-6 datum lost the exact rate"
    print("[ok] oscillation and marginal dt do not trip the stopping test")


def test_gauge_false_positive_is_repaired():
    """*** THE LEG-85 FINDING, INVERTED: all four false positives are closed. ***

    Leg 85's four failing gauges are re-run at leg 85's own settings and scored on leg 85's own
    gauge-invariant measure at leg 85's own threshold (drift < 1e-6, the number
    test_validated_gauge_is_honest already used for a trustworthy report).  Each one previously
    reported converged=True while still moving by up to 100% of its own amplitude.

    The one-step stop is closed at the root: at lambda=1e-10 the INITIAL data has residual
    2.94e-10, which the old absolute test (tol=1e-8) accepted outright; the repaired test
    demands 1e-18, which no unrelaxed state meets."""
    s = RescaledCLM(n=601, c=0.5, rho_max=7.0)

    # the mechanism, checked directly: the initial datum no longer satisfies the stopping test
    res_init = float(np.abs(s.rhs(_gauss(s.X, lam=1e-10))[0]).max())
    print(f"    lambda=1e-10 initial residual={res_init:.4e}  old absolute tol=1.0e-08 "
          f"(ACCEPTED it)  new tol_eff={1e-8 * 1e-10:.1e} (rejects it)")
    assert res_init < 1e-8, "premise moved: the initial residual no longer undercuts tol=1e-8"
    assert res_init > 1e-8 * 1e-10, "the repaired tolerance no longer rejects the initial data"

    seen = []
    for lam, drift_before, steps_before in ((1e-6, 1.216e-3, 924), (1e-8, 1.299e-1, 670),
                                            (1e-9, 1.0, 1), (1e-10, 1.0, 1)):
        r = s.run(_gauss(s.X, lam=lam), dt_frac=0.4, tol=1e-8, max_steps=20000)
        drift = _post_stop_drift(s, r)
        print(f"    lambda={lam:8.1e} converged={bool(r['converged'])} steps={steps_before}->"
              f"{r['steps']} tol_eff={r['tol_effective']:.2e} residual={r['residual']:.3e} "
              f"drift {drift_before:.3e}->{drift:.3e}")
        seen.append((lam, drift))
        assert r["converged"], f"lambda={lam:g} no longer converges at all within 20000 steps"
        # THE REPAIRED PREDICATE: a converged report now means the state has actually stopped
        assert drift < 1e-6, (
            f"lambda={lam:g}: reported converged while still drifting by {drift:.3e} -- "
            "the gauge false positive is BACK.  Do not loosen this; fix the stopping test.")
        # and it did real work rather than stopping on the initial data
        assert r["steps"] > 100, f"lambda={lam:g} stopped after only {r['steps']} steps"
        # the tolerance actually used is the gauge-relative one
        assert abs(r["tol_effective"] - 1e-8 * lam) <= 1e-8 * lam * 1e-12, (
            f"lambda={lam:g}: tol_effective {r['tol_effective']:.3e} is not tol*lambda")

    worst = max(d for _, d in seen)
    assert worst < 1e-6, f"worst post-stop drift {worst:.3e}"
    print(f"[ok] REPAIRED: all 4 of leg 85's false positives closed; worst drift {worst:.3e} "
          f"(was 1.000)")

    # the trivial fixed point f == 0 still reports convergence.  It is EXACTLY at rest
    # (residual identically 0.0, drift 0), so this is a semantic edge case, not a kinematic
    # false positive, and the floor deliberately keeps the tolerance positive so that a state
    # at exact rest is not reported as non-convergent.  Recorded, unchanged by the repair.
    r0 = s.run(np.zeros_like(s.X), dt_frac=0.4, tol=1e-8, max_steps=100)
    print(f"    f==0:         converged={bool(r0['converged'])} residual={r0['residual']:.1e} "
          f"c_omega={r0['c_omega']:+.5f} gauge={r0['gauge']:.1e} (the floor) -- at exact rest, "
          "but not the CLM fixed point")
    assert r0["converged"] and r0["residual"] == 0.0 and r0["c_omega"] > 0.5
    assert r0["gauge"] == GAUGE_TOL_FLOOR, "the degenerate gauge f(0)=0 did not hit the floor"


def test_repair_is_resolution_independent():
    """The repair holds at three resolutions -- as the defect did, it is the stopping test,
    not the discretization.  Step counts scale with the grid (1211/1664/2404) because the time
    step is dt_frac*drho; the drift verdict does not move."""
    seen = []
    for n, rho_max in ((401, 6.0), (601, 7.0), (901, 7.5)):
        s = RescaledCLM(n=n, c=0.5, rho_max=rho_max)
        r = s.run(_gauss(s.X, lam=1e-10), dt_frac=0.4, tol=1e-8, max_steps=20000)
        drift = _post_stop_drift(s, r)
        # the relaxed state is the linear-advection steady state f == f(0), not Omega_0
        f = r["f"]
        nonflat = float(np.abs(f - f[s.i0]).max() / np.abs(f).max())
        seen.append((n, bool(r["converged"]), int(r["steps"]), drift, nonflat))
        print(f"    n={n:4d} converged={bool(r['converged'])} steps={r['steps']} "
              f"c_omega={r['c_omega']:+.5f} post-stop drift={drift:.3e} "
              f"||f-f(0)||/||f||={nonflat:.2e}")
    assert all(c and st > 100 and d < 1e-6 for _, c, st, d, _ in seen), (
        f"the repair is resolution-dependent: {seen}")
    assert all(nf < 1e-6 for *_, nf in seen), (
        f"the small-gauge limit is not the constant-f steady state: {seen}")
    print("[ok] resolution-independent: the stopping test, not the discretization")


def test_reported_residual_is_the_pre_step_value():
    """SECONDARY, minor: step() returns the residual of the state passed IN, not the one it
    returns.  Locked in so a future change to the loop is noticed."""
    s = RescaledCLM(n=401, c=0.5, rho_max=6.0)
    f_pre = _gauss(s.X)
    f_post, _, res_reported = s.step(f_pre, 0.4 * s.drho)
    res_pre = float(np.abs(s.rhs(f_pre)[0]).max())
    res_post = float(np.abs(s.rhs(f_post)[0]).max())
    rel = abs(res_reported - res_post) / res_post
    print(f"    reported={res_reported:.6e}  pre-step={res_pre:.6e}  post-step={res_post:.6e}"
          f"  (reported is off the returned state by {rel * 100:.2f}%)")
    assert abs(res_reported - res_pre) < 1e-12 * max(1.0, res_pre), (
        "step() no longer reports the pre-step residual")
    assert rel > 1e-3, "the pre/post gap vanished; re-derive this test"
    print("[ok] the reported residual describes the PREVIOUS iterate (one step stale)")


if __name__ == "__main__":
    test_gauge_line_is_real()
    test_residual_is_degree_one_in_the_gauge()
    test_validated_gauge_is_honest()
    test_nonfinite_is_never_reported_converged()
    test_oscillation_does_not_trip_the_stopping_test()
    test_gauge_false_positive_is_repaired()
    test_repair_is_resolution_independent()
    test_reported_residual_is_the_pre_step_value()
    print("\nALL GCLM-RESCALED ADVERSARIAL TESTS PASSED "
          "(leg 85's gauge false positive is repaired and pinned closed)")
