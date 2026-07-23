"""Gate 1b acceptance checks: the Hou-Luo symmetry-wall (PHASE1_PLAN.md).

The wall is imposed by parity symmetry (w odd-x/odd-y, th even-x/odd-y) rather
than a Chebyshev boundary. These checks certify, to machine precision, that the
construction really is a no-flow wall and that the solver's dynamics keep the
symmetry subspace on their own -- i.e. the wall is a genuine invariant of the
equations as discretised, not something enforced by fiat:

1. wall_bc            — for symmetric vorticity, the normal velocity v vanishes
                        on the walls y=0, y=pi and the tangential-axis velocity u
                        vanishes on x=0, x=pi, at machine zero.
2. parity_preserved   — initialise in the subspace and evolve WITHOUT projection;
                        the parity-violating residual must stay at roundoff
                        (the dynamics preserve the wall).
3. parity_enforced    — with symmetry="houluo" the residual is exactly zero and
                        conservation still holds.
4. buoyancy_amplifies — a Luo-Hou-type initial condition drives strong
                        vorticity amplification at the wall while preserving
                        symmetry and conservation (the qualitative mechanism;
                        the quantitative singular growth curve is a separate,
                        resolution-limited study, not this correctness gate).

Rows are appended to experiments/solver_validation.jsonl (same tracked series).
"""

import numpy as np

from ga.logbook import append_solver_validation
from solver.boussinesq import (
    grid2d,
    parity_residual,
    solve_boussinesq,
    velocity_from_vorticity,
    wavenumbers2d,
)


def check_wall_bc(n=128):
    X, Y = grid2d(n)
    KX, KY, Ksq, inv_Ksq = wavenumbers2d(n)
    w = np.sin(X) * np.sin(Y) + 0.3 * np.sin(2 * X) * np.sin(3 * Y)  # odd-x/odd-y
    u, v = velocity_from_vorticity(np.fft.fft2(w), KX, KY, inv_Ksq)
    err = max(
        float(np.max(np.abs(v[:, 0]))),        # v=0 on wall y=0
        float(np.max(np.abs(v[:, n // 2]))),   # v=0 on wall y=pi
        float(np.max(np.abs(u[0, :]))),        # u=0 on axis x=0
        float(np.max(np.abs(u[n // 2, :]))),   # u=0 on axis x=pi
    )
    return [{
        "check": "wall_bc",
        "initial_condition_label": "v on y=0,pi; u on x=0,pi",
        "error_metric": err,
        "passed": bool(err < 1e-12),
    }]


def check_parity_preserved(n=128, t_end=2.0):
    # Symmetric IC, evolved WITHOUT enforcement: the residual measures whether
    # the discrete dynamics leak out of the Hou-Luo subspace.
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y) + 0.3 * np.sin(2 * X) * np.sin(3 * Y)
    th0 = np.cos(X) * np.sin(Y) + 0.2 * np.cos(2 * X) * np.sin(Y)
    res = solve_boussinesq(w0, th0, nu=0.0, t_max=t_end, buoyancy=True,
                           symmetry=None, dt_max=5e-3)
    err = max(parity_residual(res.omega_final, "odd_odd"),
              parity_residual(res.theta_final, "even_odd"))
    return [{
        "check": "parity_preserved",
        "initial_condition_label": "unenforced, buoyancy on",
        "error_metric": err,
        "passed": bool(err < 1e-11 and res.outcome == "no_blowup"),
    }]


def check_parity_enforced(n=128, t_end=2.0):
    X, Y = grid2d(n)
    w0 = np.sin(X) * np.sin(Y) + 0.3 * np.sin(2 * X) * np.sin(3 * Y)
    th0 = np.cos(X) * np.sin(Y) + 0.2 * np.cos(2 * X) * np.sin(Y)
    res = solve_boussinesq(w0, th0, nu=0.0, t_max=t_end, buoyancy=True,
                           symmetry="houluo", dt_max=5e-3)
    err = max(parity_residual(res.omega_final, "odd_odd"),
              parity_residual(res.theta_final, "even_odd"))
    return [{
        "check": "parity_enforced",
        "initial_condition_label": "symmetry=houluo",
        "error_metric": err,
        "passed": bool(err < 1e-13 and res.conservation_drift < 1e-3
                       and res.outcome == "no_blowup"),
    }]


def check_buoyancy_amplifies(n=128, t_end=2.5):
    # Luo-Hou-type data: modest seed vorticity + a strong buoyancy field with a
    # sharp horizontal gradient near the wall. The buoyancy torque th_x amplifies
    # vorticity at the wall; here we require substantial growth with the symmetry
    # and conservation intact (a qualitative mechanism check, not a T* claim).
    X, Y = grid2d(n)
    w0 = 0.2 * np.sin(X) * np.sin(Y)
    th0 = (1.0 + np.cos(2 * X)) * np.sin(2 * Y)  # even-x/odd-y
    res = solve_boussinesq(w0, th0, nu=0.0, t_max=t_end, buoyancy=True,
                           symmetry="houluo", amplification_factor=1e6, dt_max=5e-3)
    ratio = res.max_omega[-1] / res.max_omega[0]
    par = max(parity_residual(res.omega_final, "odd_odd"),
              parity_residual(res.theta_final, "even_odd"))
    passed = (ratio > 10.0 and par < 1e-12 and res.conservation_drift < 1e-3)
    return [{
        "check": "buoyancy_amplifies",
        "initial_condition_label": f"ratio={ratio:.1f}, drift={res.conservation_drift:.1e}",
        "error_metric": float(ratio),
        "passed": bool(passed),
    }]


_CHECKS = (check_wall_bc, check_parity_preserved, check_parity_enforced,
           check_buoyancy_amplifies)


def _run_and_record(check_fn):
    rows = check_fn()
    append_solver_validation(rows)
    for row in rows:
        assert row["passed"], (
            f"{row['check']} failed on {row['initial_condition_label']}: "
            f"error_metric={row['error_metric']:.3e}"
        )
    return rows


def test_wall_bc():
    _run_and_record(check_wall_bc)


def test_parity_preserved():
    _run_and_record(check_parity_preserved)


def test_parity_enforced():
    _run_and_record(check_parity_enforced)


def test_buoyancy_amplifies():
    _run_and_record(check_buoyancy_amplifies)


if __name__ == "__main__":
    all_rows = []
    for check in _CHECKS:
        rows = check()
        all_rows.extend(rows)
        for row in rows:
            status = "PASS" if row["passed"] else "FAIL"
            print(f"{status}: {row['check']} [{row['initial_condition_label']}] "
                  f"metric={row['error_metric']:.3e}")
    append_solver_validation(all_rows)
    n_passed = sum(r["passed"] for r in all_rows)
    print(f"\n{n_passed}/{len(all_rows)} checks passed")
    if n_passed != len(all_rows):
        raise SystemExit(1)
