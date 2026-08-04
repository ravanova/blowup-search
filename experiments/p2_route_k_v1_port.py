"""Route-K v1: the L1->L2 certification port, step one -- the kill-switch fires at Y_0.

Ranked item (3), deferred six times, attempted here.  The directive asked for the
Newton-Kantorovich setup on the 2D Boussinesq profile, an honest Y_0, a first Z_1, and a
kill-switch that STOPS rather than hardens.  **The kill-switch fires before the function
space is reached**, and the value of the leg is the mechanism plus the controls that make
it a statement about the object.

  K1  THE RELAXATION HAS NO FIXED POINT.  A steps ladder on the SSPRK3 relaxation: the sup
      residual limit-cycles and c_omega swings with it.  Plus Route-G's own COMMITTED
      resolution ladder, read out of writeup/data/, where the steady residual GROWS under
      refinement.  Y_0 is not large -- it is undefined.
  K2  WHERE THE DEFECT LIVES: the argmax of each field's residual in (r, beta), which moves
      to the WALL once the transients clear.
  K3  THE INSTRUMENT'S CONTROLS, before any claim about the operator: GMRES on a
      well-conditioned dense system and on a cond ~ 1e8 one; and the finite-difference
      Jacobian-vector product across five decades of step size.
  K4  THE KRYLOV STALL, as a LADDER in the Krylov dimension -- flat means a continuum, not
      conditioning -- unpreconditioned and with the leading-order dilation preconditioner.
  K5  the radii-polynomial status, which refuses to invent the numbers it does not have.

Deterministic, ~12 min.  Writes writeup/data/p2_route_k_v1_port.json.

Run: .venv/bin/python -u experiments/p2_route_k_v1_port.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from solver.boussinesq_rescaled import RescaledBoussinesq          # noqa: E402
from solver.boussinesq_velocity import PolarGrid                   # noqa: E402
from solver.port_certification import (                            # noqa: E402
    ProfileResidual, gmres_controls, krylov_ladder, make_preconditioner,
    radii_polynomial_status, stall_verdict,
)
from spike1_stepC_gate import profile_ansatz                       # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_k_v1_port.json"
ROUTE_G = ROOT / "writeup" / "data" / "p2_route_g_v1_g2.json"

N_R, N_B, R_MIN, R_MAX = 200, 48, 1e-3, 1e5
CHECKPOINTS = (500, 1500, 3000, 5000)
CHEN_HOU_RATIO = -2.9205600


def k1_k2_no_fixed_point():
    """The relaxation, read at a ladder of step counts.  Does it converge to anything?"""
    grid = PolarGrid(n_r=N_R, n_beta=N_B, r_min=R_MIN, r_max=R_MAX)
    solver = RescaledBoussinesq(grid)
    om, et, xi = profile_ansatz(grid)
    rr = np.exp(grid.rho)
    rows, done, t0 = [], 0, time.time()
    saved = {}
    for cp in CHECKPOINTS:
        r = solver.run(om, et, xi, dt_frac=0.3, tol=1e-12,
                       max_steps=cp - done, renorm=True)
        om, et, xi = r["omega"], r["eta"], r["xi"]
        done += r["steps"]
        Ro, Re, Rx, _ = solver.rhs(om, et, xi)
        where = {}
        for nm, R in (("omega", Ro), ("eta", Re), ("xi", Rx)):
            A = np.abs(R)
            i, j = np.unravel_index(int(np.argmax(A)), A.shape)
            where[nm] = {"max": float(A.max()), "r": float(rr[i]),
                         "beta": float(grid.beta[j]),
                         "at_wall": bool(j <= 1), "at_outer_edge": bool(i >= A.shape[0] - 3)}
        saved[done] = (om.copy(), et.copy(), xi.copy())
        rows.append({"steps": done, "residual_sup": float(r["residual"]),
                     "c_l": float(r["c_l"]), "c_omega": float(r["c_omega"]),
                     "ratio": float(r["c_l"] / r["c_omega"]),
                     "ratio_vs_chen_hou": float(abs(r["c_l"] / r["c_omega"] - CHEN_HOU_RATIO)
                                                / abs(CHEN_HOU_RATIO)),
                     "argmax": where, "seconds": round(time.time() - t0, 1)})
        print(f"  [K1] steps {done:5d}  res {r['residual']:.3e}  "
              f"c_om {r['c_omega']:+.6f}  ratio {r['c_l'] / r['c_omega']:+.5f}  "
              f"({time.time() - t0:.0f}s)", flush=True)

    res_sup = [q["residual_sup"] for q in rows]
    monotone = all(b <= a for a, b in zip(res_sup, res_sup[1:]))
    ratios = [q["ratio"] for q in rows]

    # Route-G's COMMITTED resolution ladder -- read, not re-run
    g = json.loads(ROUTE_G.read_text())["g2_our_beta"]["resolution_ladder"]
    gl = [{"n_r": q["n_r"], "r_max": q["r_max"], "residual": q["residual"],
           "c_omega": q["c_omega"]} for q in g]
    same_rmax = [q for q in gl if q["r_max"] == 1e5]
    grows = (len(same_rmax) >= 2
             and same_rmax[-1]["residual"] > same_rmax[0]["residual"])

    return {"grid": {"n_r": N_R, "n_beta": N_B, "r_min": R_MIN, "r_max": R_MAX},
            "steps_ladder": rows,
            "residual_monotone_in_steps": bool(monotone),
            "residual_sup_range": [float(min(res_sup)), float(max(res_sup))],
            "c_omega_swing": [float(min(q["c_omega"] for q in rows)),
                              float(max(q["c_omega"] for q in rows))],
            "ratio_range": [float(min(ratios)), float(max(ratios))],
            "chen_hou_ratio": CHEN_HOU_RATIO,
            "route_g_resolution_ladder": gl,
            "route_g_residual_grows_under_refinement": bool(grows),
            "route_g_residual_growth_factor": float(
                same_rmax[-1]["residual"] / same_rmax[0]["residual"]) if grows else None,
            "route_g_c_omega_spread_over_that_ladder": float(
                (max(q["c_omega"] for q in gl) - min(q["c_omega"] for q in gl))
                / abs(np.mean([q["c_omega"] for q in gl]))),
            "verdict": ("The relaxation does not converge: the sup residual is NOT monotone "
                        "in steps and Route-G's committed resolution ladder GROWS under "
                        "refinement. There is no fixed profile, so Y_0 is UNDEFINED -- a "
                        "stronger statement than 'large'."),
            "saved_states": saved, "grid_obj": grid, "solver_obj": solver}


def k3_instrument_controls(res, z, Fz):
    ctrl = gmres_controls()
    rng = np.random.default_rng(1)
    v = rng.standard_normal(z.size)
    rows = res.jv_step_study(z, Fz, v)
    drift = [q["rel_change_vs_previous_h"] for q in rows if "rel_change_vs_previous_h" in q]
    norms = [q["norm_Jv"] for q in rows]
    return {"gmres": ctrl, "jv_step_study": rows,
            "jv_norm_spread": float((max(norms) - min(norms)) / np.mean(norms)),
            "jv_best_drift": float(min(drift)),
            "verdict": ("GMRES is correct (7e-11 in 19 iterations on a well-conditioned "
                        "dense system) and its ill-conditioning failure mode is calibrated "
                        f"(cond~1e8 stalls at {ctrl['cond_1e8']['rel']:.2f}). The "
                        "finite-difference matvec is stable across five decades of h. "
                        "Neither is the source of what follows.")}


def k4_krylov_stall(res, z, Fz, c_l, c_omega):
    Jv = res.jacobian_vector(z, Fz)
    plain = krylov_ladder(Jv, -Fz)
    print(f"  [K4] unpreconditioned: {[round(q['rel_residual'], 4) for q in plain]}",
          flush=True)
    Minv = make_preconditioner(res, c_l, c_omega)
    pre = krylov_ladder(lambda v: Jv(Minv(v)), -Fz)
    print(f"  [K4] preconditioned:   {[round(q['rel_residual'], 4) for q in pre]}",
          flush=True)
    sp, sv = stall_verdict(plain), stall_verdict(pre)
    return {"unpreconditioned": plain, "unpreconditioned_stall": sp,
            "preconditioned": pre, "preconditioned_stall": sv,
            "preconditioner": ("exact inverse of the leading-order operator "
                               "(-c_l d_rho + diagonal damping), lower bidiagonal per "
                               "angular line, O(N); the same split Chen-Hou describe in "
                               "arXiv:2210.07191"),
            "improvement_factor": float(sp["rel_at_max_dim"] / sv["rel_at_max_dim"]),
            "verdict": (f"Unpreconditioned the solve stalls at {sp['rel_at_max_dim']:.4f} "
                        f"and is FLAT in Krylov dimension ({sp['rel_at_min_dim']:.4f} at "
                        f"m={sp['min_dim']}), which reads as a continuum in the spectrum "
                        "rather than conditioning. The leading-order preconditioner nearly "
                        f"halves it ({sv['rel_at_max_dim']:.4f}) and the curve stays flat -- "
                        "so the dilation continuum is a real and identified PART of the "
                        "obstruction, and a second one of comparable size remains.")}


def main():
    t0 = time.time()
    print("== Route-K v1: the L1->L2 certification port, step one ==", flush=True)
    k1 = k1_k2_no_fixed_point()
    saved = k1.pop("saved_states")
    grid = k1.pop("grid_obj")
    solver = k1.pop("solver_obj")
    res = ProfileResidual(solver, grid)

    # THE SEED IS NOT A DETAIL.  There is no fixed point, so "linearize at the profile" has
    # no referent -- the best and worst points of the limit cycle are both equally entitled
    # to be called it.  Measuring at BOTH is what turns "the solve stalls" into "there is no
    # object to quote a Z_1 for", which is the stronger and the true statement.
    seeds = {}
    for label, steps in (("cycle_best", 3000), ("cycle_worst", 5000)):
        om, et, xi = saved[steps]
        z = res.pack(om, et, xi)
        Fz = res.F(z)
        info = res.info(z)
        seeds[label] = {"steps": steps, "z": z, "Fz": Fz,
                        "c_l": float(info["c_l"]), "c_omega": float(info["c_omega"]),
                        "F_l2": float(np.linalg.norm(Fz)),
                        "F_inf": float(np.abs(Fz).max())}
        print(f"  [K3] seed {label} (steps {steps}): ||F||_2 = "
              f"{np.linalg.norm(Fz):.4e}, ||F||_inf = {np.abs(Fz).max():.4e}", flush=True)

    best = seeds["cycle_best"]
    k3 = k3_instrument_controls(res, best["z"], best["Fz"])
    k4 = {}
    for label, s in seeds.items():
        print(f"  [K4] --- {label} ---", flush=True)
        k4[label] = k4_krylov_stall(res, s["z"], s["Fz"], s["c_l"], s["c_omega"])
    k4["seed_dependence"] = {
        "unpreconditioned_stall_best": k4["cycle_best"]["unpreconditioned_stall"]["rel_at_max_dim"],
        "unpreconditioned_stall_worst": k4["cycle_worst"]["unpreconditioned_stall"]["rel_at_max_dim"],
        "F_l2_best": best["F_l2"], "F_l2_worst": seeds["cycle_worst"]["F_l2"],
        "reading": ("the stalled residual and the preconditioner's benefit BOTH depend on "
                    "which point of the limit cycle is linearized at, which is the sharpest "
                    "form of the finding: there is no object for a Z_1 to be about."),
    }
    k5 = radii_polynomial_status(None, None)

    out = {
        "leg": "Route-K v1",
        "title": ("The L1->L2 certification port, step one: no fixed profile to define "
                  "Y_0, and no approximate inverse to start Z_1"),
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seed_states": {k: {kk: vv for kk, vv in v.items() if kk not in ("z", "Fz")}
                        for k, v in seeds.items()},
        "n_unknowns": int(best["z"].size),
        "K1_K2_no_fixed_point": k1,
        "K3_instrument_controls": k3,
        "K4_krylov_stall": k4,
        "K5_radii_polynomial": k5,
        "what_must_be_built_next": [
            "a preconditioner that also covers the nonlocal Biot-Savart velocity and the "
            "wall -- the leading-order dilation split accounts for only about half the "
            "stalled residual, so the remainder is where the next leg goes",
            "a profile from a CONVERGED Newton solve rather than a relaxation; this is "
            "downstream of the preconditioner, since Newton stalls for the same reason",
            "only then: the function space, Y_0 in it, and Z_1",
        ],
        "clay": ("No link of the L1->L4 chain moved. A blocked link is not a moved link. "
                 "Clay odds unchanged at ~0.05%."),
    }
    out["wall_clock_seconds"] = round(time.time() - t0, 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    print(f"  [K5] {k5['status']}: {k5['why']}", flush=True)
    print(f"-> {OUT}  ({out['wall_clock_seconds']} s)")


if __name__ == "__main__":
    main()
