"""Route-L v1: the 2D preconditioner. The stall is attributed, and then removed.

Route-K stopped the certification port at step (iii) with the obstruction only half
identified: the leading-order RADIAL split took the Krylov stall 0.6623 -> 0.3596 and the
curve stayed FLAT, so something else of comparable size remained. Route-K named two
candidates -- the nonlocal Biot-Savart velocity, and the wall.

  L1  THE ATTRIBUTION BATTERY. Six ablations of the residual map, each with its own Krylov
      ladder, ranked by how much it un-flattens the curve. BOTH of Route-K's candidates are
      eliminated: freezing the velocity feedback makes the stall WORSE, and the stalled
      residual is not concentrated at the wall for omega or eta.
  L2  WHERE THE STALLED KRYLOV RESIDUAL LIVES, by angular band -- the measurement that
      retires the wall hypothesis rather than merely doubting it.
  L3  THE PRECONDITIONER. The radial upwinding is outward everywhere on this profile, so the
      full transport operator is block lower-bidiagonal with tridiagonal blocks and ONE
      Thomas sweep inverts it exactly. Reported against the unpreconditioned ladder, against
      Route-K's radial-only ladder, and against the ADI composition that does NOT work.
  L4  DOES NEWTON CONVERGE NOW? The question Route-K left downstream.

Deterministic, ~25 min. Writes writeup/data/p2_route_l_v1_precond.json.

Run: .venv/bin/python -u experiments/p2_route_l_v1_precond.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.boussinesq_rescaled import (                            # noqa: E402
    RescaledBoussinesq, _upwind_deriv, advection_speeds, modulation,
)
from solver.boussinesq_velocity import PolarGrid, _thomas           # noqa: E402
from solver.port_certification import (                             # noqa: E402
    ProfileResidual, attribution_summary, gmres, krylov_ladder, leading_order_solve,
    line_sweep_solve, make_preconditioner, outward_upwinding_holds,
    radii_polynomial_status, stall_verdict,
)
from spike1_stepC_gate import profile_ansatz                        # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_l_v1_precond.json"
N_R, N_B, R_MIN, R_MAX, SEED_STEPS = 200, 48, 1e-3, 1e5, 3000
DIMS = (10, 20, 40, 80, 160)


def build_state():
    grid = PolarGrid(n_r=N_R, n_beta=N_B, r_min=R_MIN, r_max=R_MAX)
    solver = RescaledBoussinesq(grid)
    om, et, xi = profile_ansatz(grid)
    r = solver.run(om, et, xi, dt_frac=0.3, tol=1e-12, max_steps=SEED_STEPS, renorm=True)
    return grid, solver, r


def make_residual(res, solver, grid, base, *, angular=True, radial_velocity=True,
                  reaction=True, frozen_velocity=False):
    """The residual map with one term ablated, so each candidate can be tested alone."""
    om, et, _ = base
    dbeta = grid.beta[1] - grid.beta[0]
    u0, v0, phi0, ux0, uy0, vx0 = solver.velocity_and_grads(om)
    cl0, cw0, _, _ = modulation(om, et, phi0, grid)
    rr = np.exp(grid.rho)[:, None]
    cb, sb = np.cos(grid.beta)[None, :], np.sin(grid.beta)[None, :]

    def F(zz):
        o, e, x = res.unpack(zz)
        if frozen_velocity:
            u, v, ux, uy, vx, cl, cw = u0, v0, ux0, uy0, vx0, cl0, cw0
        else:
            u, v, phi, ux, uy, vx = solver.velocity_and_grads(o)
            cl, cw, _, _ = modulation(o, e, phi, grid)
        s_rho = cl + ((u * cb + v * sb) / rr if radial_velocity else 0.0)
        s_beta = ((v * cb - u * sb) / rr) if angular else np.zeros_like(u)

        def T(f):
            out = s_rho * _upwind_deriv(f, grid.drho, s_rho, 0)
            if angular:
                out = out + s_beta * _upwind_deriv(f, dbeta, s_beta, 1)
            return out

        if reaction:
            return res.pack(-T(o) + e + cw * o,
                            -T(e) + (2 * cw - ux) * e - vx * x,
                            -T(x) + (2 * cw + ux) * x - uy * e)
        return res.pack(-T(o), -T(e), -T(x))

    return F


def jv_of(F, z, Fz):
    def Jv(v):
        h = 1e-7 * np.linalg.norm(z) / (np.linalg.norm(v) + 1e-30)
        return (F(z + h * v) - Fz) / h
    return Jv


def main():
    t0 = time.time()
    print("== Route-L v1: attributing the 2D stall, and removing it ==", flush=True)
    grid, solver, r = build_state()
    om, et, xi = r["omega"], r["eta"], r["xi"]
    c_l, c_om = float(r["c_l"]), float(r["c_omega"])
    res = ProfileResidual(solver, grid)
    z = res.pack(om, et, xi)
    Fz = res.F(z)
    dbeta = grid.beta[1] - grid.beta[0]
    s_rho0, s_beta0 = advection_speeds(*solver.velocity_and_grads(om)[:2], grid, c_l)
    up = outward_upwinding_holds(s_rho0)
    print(f"  seed: ||F||_2 {np.linalg.norm(Fz):.4e}  c_l {c_l:.5f}  c_om {c_om:.5f}; "
          f"s_rho in [{up['min_s_rho']:.3f}, {up['max_s_rho']:.3f}]", flush=True)

    # ---- L1: the attribution battery ----------------------------------
    variants = {
        "full": {},
        "velocity feedback OFF": {"frozen_velocity": True},
        "angular transport OFF": {"angular": False},
        "velocity in s_rho OFF": {"radial_velocity": False},
        "reaction terms OFF": {"reaction": False},
        "pure dilation, no angular": {"angular": False, "radial_velocity": False},
    }
    ladders, checks = {}, {}
    for label, kw in variants.items():
        F = make_residual(res, solver, grid, (om, et, xi), **kw)
        Fv = F(z)
        if label == "full":
            checks["full_matches_solver_rhs"] = float(
                np.linalg.norm(Fv - Fz) / np.linalg.norm(Fz))
        ladders[label] = krylov_ladder(jv_of(F, z, Fv), -Fv, dims=DIMS)
        print(f"  [L1] {label:28s} "
              f"{[round(q['rel_residual'], 4) for q in ladders[label]]}", flush=True)
    attrib = attribution_summary(ladders)

    # ---- L2: where the stalled Krylov residual lives -------------------
    x_sol, rel_full, _ = gmres(jv_of(res.F, z, Fz), -Fz, m=160, tol=1e-12)
    rr = jv_of(res.F, z, Fz)(x_sol) + Fz
    bands = {}
    for nm, R in zip(("omega", "eta", "xi"), res.unpack(rr)):
        A = np.abs(R)
        tot = float((A ** 2).sum()) + 1e-300
        bands[nm] = {"wall_first3_frac": float((A[:, :3] ** 2).sum() / tot),
                     "axis_last3_frac": float((A[:, -3:] ** 2).sum() / tot),
                     "outer_last5_frac": float((A[-5:, :] ** 2).sum() / tot)}
    bands["proportional_share_3_of_48"] = 3.0 / N_B
    print(f"  [L2] stalled-residual wall fraction: "
          f"{ {k: round(v['wall_first3_frac'], 3) for k, v in bands.items() if isinstance(v, dict)} }",
          flush=True)

    # ---- L3: the preconditioners ---------------------------------------
    Jv = jv_of(res.F, z, Fz)
    M_radial = make_preconditioner(res, c_l, c_om)

    def M_sweep(v):
        o, e, x = res.unpack(v)
        return res.pack(
            line_sweep_solve(o, s_rho0, s_beta0, grid.drho, dbeta, c_om, _thomas),
            line_sweep_solve(e, s_rho0, s_beta0, grid.drho, dbeta, 2 * c_om, _thomas),
            line_sweep_solve(x, s_rho0, s_beta0, grid.drho, dbeta, 2 * c_om, _thomas))

    def M_adi(v):
        """The composition that does NOT work -- kept because the negative is load-bearing."""
        o, e, x = res.unpack(v)
        o = leading_order_solve(o, c_l, grid.drho, c_om)
        e = leading_order_solve(e, c_l, grid.drho, 2 * c_om)
        x = leading_order_solve(x, c_l, grid.drho, 2 * c_om)
        one = np.ones_like(s_rho0)
        return res.pack(
            line_sweep_solve(o, 0 * one, s_beta0, grid.drho, dbeta, 1.0, _thomas),
            line_sweep_solve(e, 0 * one, s_beta0, grid.drho, dbeta, 1.0, _thomas),
            line_sweep_solve(x, 0 * one, s_beta0, grid.drho, dbeta, 1.0, _thomas))

    pre = {"none": krylov_ladder(Jv, -Fz, dims=DIMS),
           "radial only (Route-K)": krylov_ladder(lambda v: Jv(M_radial(v)), -Fz, dims=DIMS),
           "ADI composition": krylov_ladder(lambda v: Jv(M_adi(v)), -Fz, dims=DIMS),
           "full transport line sweep": krylov_ladder(lambda v: Jv(M_sweep(v)), -Fz, dims=DIMS)}
    deep = krylov_ladder(lambda v: Jv(M_sweep(v)), -Fz, dims=(240, 320))
    for k, v in pre.items():
        print(f"  [L3] {k:28s} {[round(q['rel_residual'], 6) for q in v]}", flush=True)
    print(f"  [L3] {'line sweep, deeper':28s} "
          f"{[round(q['rel_residual'], 9) for q in deep]}", flush=True)

    # ---- L4: does Newton converge now? ---------------------------------
    zz = z.copy()
    newton = []
    for it in range(12):
        Fc = res.F(zz)
        n2, ninf = float(np.linalg.norm(Fc)), float(np.abs(Fc).max())
        newton.append({"iter": it, "F_l2": n2, "F_inf": ninf})
        print(f"  [L4] newton {it:2d}  ||F||_2 {n2:.6e}  ||F||_inf {ninf:.6e}  "
              f"({time.time() - t0:.0f}s)", flush=True)
        if ninf < 1e-11:
            break
        y, rel, k = gmres(lambda v: jv_of(res.F, zz, Fc)(M_sweep(v)), -Fc, m=200, tol=1e-4)
        dz = M_sweep(y)
        lam, ok = 1.0, False
        for _ in range(10):
            if float(np.linalg.norm(res.F(zz + lam * dz))) < n2:
                zz = zz + lam * dz
                ok = True
                break
            lam *= 0.5
        newton[-1].update({"gmres_rel": rel, "gmres_k": k, "step_lambda": lam,
                           "line_search_ok": ok})
        if not ok:
            print("  [L4] line search failed -- stopping and reporting", flush=True)
            break
    F_end = res.F(zz)
    newton_gain = newton[0]["F_l2"] / float(np.linalg.norm(F_end))

    # ---- L5: the gauge hypothesis, tested ------------------------------
    # L4's linear solves SUCCEED (gmres rel ~2e-3, against 1.00 before) and Newton still
    # creeps, with the line search capping at lambda = 1/64 every step.  That is not a
    # spectral failure -- it is the signature of a near-null direction in DF.  The obvious
    # candidate is the SCALING SYMMETRY: `run(renorm=True)` re-pins omega_x(0) and eta_x(0)
    # after every relaxation step, and F does NOT contain that constraint, so Newton is free
    # to wander along it.  The test is to apply the same projection inside Newton and see
    # whether the creep becomes convergence.  If it does, the fix is a bordered system.
    from solver.boussinesq_rescaled import odd_field_x_slope        # noqa: E402
    wx_t = odd_field_x_slope(om, grid)
    ex_t = odd_field_x_slope(et, grid)

    def project(zv):
        o, e, x = res.unpack(zv)
        fo = wx_t / odd_field_x_slope(o, grid)
        fe = ex_t / odd_field_x_slope(e, grid)
        return res.pack(o * fo, e * fe, x * fe)

    zg = project(z.copy())
    gauged = []
    for it in range(12):
        Fc = res.F(zg)
        n2, ninf = float(np.linalg.norm(Fc)), float(np.abs(Fc).max())
        gauged.append({"iter": it, "F_l2": n2, "F_inf": ninf})
        print(f"  [L5] gauged newton {it:2d}  ||F||_2 {n2:.6e}  "
              f"||F||_inf {ninf:.6e}  ({time.time() - t0:.0f}s)", flush=True)
        if ninf < 1e-11:
            break
        y, rel, k = gmres(lambda v: jv_of(res.F, zg, Fc)(M_sweep(v)), -Fc, m=200, tol=1e-4)
        dz = M_sweep(y)
        lam, ok = 1.0, False
        for _ in range(10):
            if float(np.linalg.norm(res.F(project(zg + lam * dz)))) < n2:
                zg = project(zg + lam * dz)
                ok = True
                break
            lam *= 0.5
        gauged[-1].update({"gmres_rel": rel, "step_lambda": lam, "line_search_ok": ok})
        if not ok:
            print("  [L5] line search failed under the gauge projection too", flush=True)
            break
    Fg = res.F(zg)

    out = {
        "leg": "Route-L v1",
        "title": "The 2D preconditioner: the stall attributed, and removed",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "grid": {"n_r": N_R, "n_beta": N_B, "r_min": R_MIN, "r_max": R_MAX,
                 "seed_steps": SEED_STEPS},
        "seed": {"c_l": c_l, "c_omega": c_om, "F_l2": float(np.linalg.norm(Fz)),
                 "F_inf": float(np.abs(Fz).max())},
        "outward_upwinding": up,
        "consistency_checks": checks,
        "L1_attribution": {"ladders": ladders, "ranked": attrib},
        "L2_stalled_residual_bands": bands,
        "L3_preconditioners": {"ladders": pre, "line_sweep_deeper": deep,
                               "stalls": {k: stall_verdict(v) for k, v in pre.items()}},
        "L5_gauge_projected_newton": {
            "iterations": gauged,
            "F_l2_end": float(np.linalg.norm(Fg)),
            "F_inf_end": float(np.abs(Fg).max()),
            "reduction_factor": gauged[0]["F_l2"] / float(np.linalg.norm(Fg)),
            "converged": bool(np.abs(Fg).max() < 1e-11),
            "hypothesis": ("L4's linear solves succeed while Newton creeps with the line "
                           "search capped at 1/64 -- the signature of a near-null direction "
                           "in DF, not of a spectral failure. The scaling symmetry is the "
                           "candidate: run(renorm=True) pins omega_x(0) and eta_x(0) after "
                           "every relaxation step and F does not contain that constraint."),
        },
        "L4_newton": {"iterations": newton,
                      "F_l2_start": newton[0]["F_l2"],
                      "F_l2_end": float(np.linalg.norm(F_end)),
                      "F_inf_end": float(np.abs(F_end).max()),
                      "reduction_factor": newton_gain,
                      "converged": bool(np.abs(F_end).max() < 1e-11)},
        "K5_radii_polynomial": radii_polynomial_status(None, None),
    }
    out["wall_clock_seconds"] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"-> {OUT}  ({out['wall_clock_seconds']} s)")


if __name__ == "__main__":
    main()
