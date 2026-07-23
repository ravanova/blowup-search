"""Gate 2b: the fine-N exponent measurement, on known-answer controls.

The measurement pipeline for Phase 1 is { run the 2D Boussinesq solver -> take
max|w|(t) -> win_condition.estimate_blowup_time(fit_exponent=True) -> (T*, alpha,
held-out R^2) -> the resolution-convergence gate }. The fitter is the SAME
model-agnostic code Stage 3.6 validated on CLM (known alpha=1) and the a=0.7
control, so only its application to the 2D solver is new. Per the Phase-0
discipline it is validated on known answers BEFORE being trusted on the
ambiguous rough-data cases:

1. POSITIVE (exponent recovery): a synthetic self-similar series M(t)=(T*-t)^-a
   must be inverted back to (a, T*). This certifies the exponent fit in the
   Phase-1 context.

2. NEGATIVE (no false blow-up): 2D Euler (buoyancy off) is globally regular and
   conserves ||w||_inf (Wolibner / Beale-Kato-Majda), so the pipeline must NOT
   certify a resolution-converged (Tier-2) blow-up from it. This is the
   anti-self-deception control unique to the model: a single coarse run can look
   like a candidate (held-out R^2 just over the floor), but the exponent and T*
   rail to opposite grid edges across resolution, so the convergence gate
   rejects it. WIN_CONDITION.md is exactly this discipline.

Run: .venv/bin/python test_phase1_measurement.py
"""

import numpy as np

from ga.genome2d import realize_holder_density_2d, realize_holder_vorticity_2d
from solver.boussinesq import solve_boussinesq
from win_condition import WinTier, classify, estimate_blowup_time


def test_exponent_recovery_synthetic():
    Tstar = 2.0
    for alpha in (1.0, 1.5, 2.5):
        t = np.linspace(0.0, 0.92 * Tstar, 60)
        M = (Tstar - t) ** (-alpha)
        est = estimate_blowup_time(t.tolist(), M.tolist(), tail_fraction=0.6,
                                   fit_exponent=True)
        assert est is not None, alpha
        assert abs(est.exponent - alpha) <= 0.05, (alpha, est.exponent)
        assert abs(est.t_star - Tstar) / Tstar < 0.01, (alpha, est.t_star)
        assert est.r_squared > 0.999, (alpha, est.r_squared)


def _run_euler(n, t_max=2.5):
    """One 2D Euler (buoyancy off) control run in the Hou-Luo subspace."""
    w0 = realize_holder_vorticity_2d(0.5, n)
    th0 = realize_holder_density_2d(0.5, n)
    res = solve_boussinesq(w0, th0, nu=0.0, t_max=t_max, buoyancy=False,
                           symmetry="houluo", amplification_factor=1e6, dt_max=5e-3)
    est = estimate_blowup_time(res.times.tolist(), res.max_omega.tolist(),
                               tail_fraction=0.5, fit_exponent=True)
    growth = float(res.max_omega.max() / res.max_omega[0])
    return res, est, growth


def test_euler_conserves_max_vorticity():
    # 2D Euler conserves ||w||_inf; the small numerical growth must shrink as the
    # rough (h=0.5) initial cusp is better resolved.
    g_coarse = _run_euler(96)[2]
    g_fine = _run_euler(160)[2]
    assert g_coarse < 1.05, g_coarse
    assert g_fine < g_coarse, (g_coarse, g_fine)


def test_euler_gives_no_confirmed_blowup():
    # The pipeline must never reach NUMERICALLY_CONFIRMED on a provably-regular
    # flow. Collect T* across three resolutions and run the real classifier.
    resolutions = (96, 128, 160)
    t_stars = []
    finest_est = None
    for n in resolutions:
        _, est, _ = _run_euler(n)
        finest_est = est
        # A None estimate is already "no blow-up"; record a sentinel that cannot
        # spuriously converge with the others.
        t_stars.append(est.t_star if est is not None else float("inf"))
    tier = classify(finest_est, t_star_by_resolution=t_stars)
    assert tier is not WinTier.NUMERICALLY_CONFIRMED, (tier, t_stars)


if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests passed.")
