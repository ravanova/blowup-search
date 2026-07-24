"""Tests for the CLM (a=0) dynamic-rescaling integrator (Phase-2 Spike 0).

Pre-committed success predicates (whole-line, local self-similar structure):
  (1) STEADY: Omega_0 = -4X/(1+4X^2) is a numerical steady state (tiny ||f_tau||)
      with c_omega = -1, H Omega(0) = 2.
  (2) FROZEN ORIGIN: the origin slope f(0) = Omega_X(0) = -4 is held exactly.
  (3) DYNAMIC CONVERGENCE: perturbed odd data (same origin slope) relaxes to
      Omega_0 (shape err small) with the correct rate c_omega -> -1.
  (4) RESOLUTION-STABLE: refining the grid, the converged profile and c_omega agree.

NOTE the physical T*=2 is deliberately NOT a predicate here: it belongs to the
global periodic solve (test_solver_clm.py), not the whole-line local rescaling;
the local analogue is the rate c_omega -> -1. Run: python test_gclm_rescaled.py
"""

import numpy as np

from solver.gclm_rescaled import RescaledCLM, clm_profile

PI = np.pi


def _rel_shape_err(omega, X, radius=5.0):
    exact = clm_profile(X)
    core = np.abs(X) < radius
    core[:3] = core[-3:] = False
    return np.abs(omega[core] - exact[core]).max() / np.abs(exact).max()


def test_steady_profile_residual():
    """Omega_0 is a numerical steady state: ||f_tau|| tiny, c_omega=-1, HOmega(0)=2."""
    s = RescaledCLM(n=1201, c=0.5, rho_max=8.0)
    f0 = clm_profile(s.X) / np.where(s.X == 0, 1.0, s.X)
    f0[s.i0] = -4.0  # Omega_0/X at X=0 is the slope -4
    L0, c_omega = s.rhs(f0)
    res = np.abs(L0).max()
    Homega0 = s.hilbert(s.X * f0)[s.i0]
    print(f"    steady residual ||f_tau||={res:.2e}  c_omega={c_omega:+.5f}  HOmega(0)={Homega0:.5f}")
    assert res < 1e-4, f"Omega_0 not steady: residual {res:.2e}"
    assert abs(c_omega + 1.0) < 5e-3, f"c_omega {c_omega} != -1"
    assert abs(Homega0 - 2.0) < 5e-3, f"HOmega(0) {Homega0} != 2"
    print("[ok] Omega_0 is a numerical steady state with the exact rate/HOmega(0)")


def test_origin_slope_frozen():
    """f(0) = Omega_X(0) is frozen exactly by the scheme (advection & source vanish)."""
    s = RescaledCLM(n=801, c=0.5, rho_max=7.0)
    f0 = -4.0 * np.exp(-s.X ** 2 / 2.0)  # f(0) = -4
    f = f0.copy()
    dt = 0.4 * s.drho
    for _ in range(300):
        f, _, _ = s.step(f, dt)
    drift = abs(f[s.i0] - (-4.0))
    print(f"    origin f(0) drift after 300 steps: {drift:.2e}")
    assert drift < 1e-10, f"origin slope drifted by {drift:.2e}"
    print("[ok] origin slope f(0)=-4 held to machine precision")


def test_dynamic_convergence_to_profile():
    """Perturbed odd data relaxes to Omega_0 with c_omega -> -1."""
    s = RescaledCLM(n=1201, c=0.5, rho_max=8.0)
    f0 = -4.0 * np.exp(-s.X ** 2 / 2.0)  # different tail, same origin slope
    r = s.run(f0, dt_frac=0.4, tol=1e-7, max_steps=80000)
    rel = _rel_shape_err(r["omega"], s.X)
    print(f"    converged={r['converged']} steps={r['steps']} tau={r['tau']:.1f} "
          f"c_omega={r['c_omega']:+.5f} shape_err={rel:.2e}")
    assert r["converged"], "did not converge"
    assert rel < 1e-2, f"shape err {rel:.2e} exceeds 1% POC target"
    assert abs(r["c_omega"] + 1.0) < 5e-3, f"rate c_omega {r['c_omega']} != -1"
    print("[ok] perturbed data converges to Omega_0 with correct rate (one-scale is stable!)")


def test_convergence_from_second_perturbation():
    """A differently-shaped perturbation (narrower) also lands on Omega_0."""
    s = RescaledCLM(n=1201, c=0.5, rho_max=8.0)
    # narrower bump: f(0)=-4, sharper than Omega_0
    f0 = -4.0 / (1.0 + 9.0 * s.X ** 2)
    r = s.run(f0, dt_frac=0.4, tol=1e-7, max_steps=80000)
    rel = _rel_shape_err(r["omega"], s.X)
    print(f"    narrower IC: converged={r['converged']} steps={r['steps']} "
          f"c_omega={r['c_omega']:+.5f} shape_err={rel:.2e}")
    assert r["converged"] and rel < 1e-2 and abs(r["c_omega"] + 1.0) < 5e-3
    print("[ok] second (narrower) perturbation also converges to Omega_0")


def test_resolution_stability():
    """Converged profile and rate agree across two grid resolutions."""
    results = []
    for n, rho_max in ((901, 7.5), (1801, 8.5)):
        s = RescaledCLM(n=n, c=0.5, rho_max=rho_max)
        f0 = -4.0 * np.exp(-s.X ** 2 / 2.0)
        r = s.run(f0, dt_frac=0.4, tol=1e-7, max_steps=120000)
        rel = _rel_shape_err(r["omega"], s.X)
        results.append((n, r["c_omega"], rel, r["converged"]))
        print(f"    n={n:5d} c_omega={r['c_omega']:+.6f} shape_err={rel:.2e} conv={r['converged']}")
    (n1, c1, e1, k1), (n2, c2, e2, k2) = results
    assert k1 and k2, "a resolution did not converge"
    assert abs(c1 - c2) < 2e-3, f"c_omega not resolution-stable: {c1} vs {c2}"
    assert e1 < 1e-2 and e2 < 1e-2, "shape err not at POC level"
    assert e2 <= e1 * 1.5, "finer grid not at least as accurate"
    print("[ok] converged rate and profile are resolution-stable")


if __name__ == "__main__":
    test_steady_profile_residual()
    test_origin_slope_frozen()
    test_dynamic_convergence_to_profile()
    test_convergence_from_second_perturbation()
    test_resolution_stability()
    print("\nALL GCLM-RESCALED TESTS PASSED")
