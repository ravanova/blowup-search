"""PROG-R4, unit U1 -- MILESTONE M1: the globalisation layer.

WHAT THIS UNIT IS. A build unit, not a claim unit. It replaces leg 353's
step-halving line search with a genuine Newton-GMRES-hookstep (Viswanath 2007)
trust region, and it discharges exactly one obligation: that the new layer
REPRODUCES leg 353's laminar-fixed-point control THROUGH itself. No claim is
made here and no two-branch question is manufactured for it. The gates are U3
(G1) and U4 (G2); this unit answers neither.

THE CONTROL, replicated from leg 353 verbatim in its parameters. The laminar
profile w_lam = -(Re/n) cos(n y) is an EXACT fixed point of the flow (it is
x-independent, so the nonlinear term vanishes identically and the viscous and
forcing terms cancel by construction). Perturb it by 1% of its own L2 norm in
a fixed random direction (seed 0, the same draw leg 353 used) and hand the
result to the solver with T=1.0, s=0.1. Leg 353 measured a 99.3426310647174%
monotone reduction of ||R|| in 5.657 s. The milestone asks whether the same
control, run through the hookstep layer, still does that.

WHAT A PASS HERE DOES AND DOES NOT MEAN. It means the new globalisation has
not broken the solver on a problem whose answer is known analytically. It does
NOT mean the hookstep helps on RPOs -- that question belongs to U3, is
pre-registered as G1, and is not touched here. The side-by-side line-search
column below is reported as MAGNITUDES for the record, not as a verdict.

BAN SCREEN (plan_of_record.py, Ban 1). The control converges BACK to the
laminar fixed point it was perturbed from. It is a solver control, not a
continuation: there is no parameter being varied, no branch being followed,
and no orbit being produced from a fixed point. This was screened in
writeup/novelty/prog_r4.md section 1b and is re-screened here at the point of
use.

Usage:
    python experiments/programme_r4/u1_m1_globalisation.py [--out PATH]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))

from solver.kolmogorov2d_nkbasin import (  # noqa: E402
    Kolmogorov2D, extended_residual, grid2d, newton_hookstep_rpo,
    newton_krylov_rpo, pack,
)

HERE = os.path.dirname(os.path.abspath(__file__))

# Leg 353's measured baseline, quoted from writeup/data/p2_route_dsspb5_v1.json
# so the comparison is against the recorded number, not a re-run of it.
LEG353_FRACTIONAL_REDUCTION = 0.993426310647174
LEG353_MONOTONE = True


def laminar_start(solver):
    """The perturbed laminar initial condition, reproduced bit-for-bit from
    leg 353's laminar_control(): same profile, same rng seed, same 1% relative
    perturbation, same normalisation order."""
    _, Y = grid2d(solver.N)
    w_lam = -(solver.Re / solver.n_forcing) * np.cos(solver.n_forcing * Y)
    rng = np.random.default_rng(0)
    d = rng.standard_normal(w_lam.shape)
    d /= np.linalg.norm(d)
    return w_lam, w_lam + 0.01 * np.linalg.norm(w_lam) * d


def summarise(hist):
    monotone = all(hist[i + 1] <= hist[i] for i in range(len(hist) - 1))
    reduction = 1.0 - hist[-1] / hist[0] if hist and hist[0] > 0 else 0.0
    return bool(monotone), float(reduction)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "u1_m1_ledger.json"))
    ap.add_argument("--N", type=int, default=24)
    args = ap.parse_args()

    solver = Kolmogorov2D(N=args.N, Re=60.0, n_forcing=4, dt=0.01)
    w_lam, w0_guess = laminar_start(solver)

    # The fixed point is exact to integration error: report the magnitude
    # rather than asserting it, so the control's own premise is measured.
    wT, _ = solver.integrate(w_lam, 1.0)
    fixed_point_drift = float(np.linalg.norm(wT - w_lam)
                              / np.linalg.norm(w_lam))

    # -- the control's own rank deficiency, measured not assumed ------------
    # At an x-independent fixed point BOTH extra unknowns are null directions:
    # Phi_T(w_lam) = w_lam for every T, and shift_x(w_lam, s) = w_lam for
    # every s. So dR/dT and dR/ds vanish identically there and the extended
    # Jacobian is rank-deficient by 2. Neither globalisation can drive ||R||
    # to 1e-8 on this control -- not because the layer is weak, but because
    # the last two columns carry no information. That is measured here rather
    # than assumed, and it is why the milestone is stated as a REDUCTION
    # against leg 353's recorded reduction and not as a convergence.
    x_lam = pack(w_lam, 1.0, 0.1)
    ref_rhs = solver.rhs_physical(w_lam)
    ref_dwdx = np.fft.ifft2(1j * solver.KX
                            * (np.fft.fft2(w_lam) * solver.mask)).real
    F_lam = extended_residual(x_lam, solver, w_lam, ref_rhs, ref_dwdx)
    h = 1e-6
    col_T, col_s = np.zeros_like(x_lam), np.zeros_like(x_lam)
    col_T[-2] = 1.0
    col_s[-1] = 1.0
    dR_dT = (extended_residual(x_lam + h * col_T, solver, w_lam, ref_rhs,
                               ref_dwdx) - F_lam) / h
    dR_ds = (extended_residual(x_lam + h * col_s, solver, w_lam, ref_rhs,
                               ref_dwdx) - F_lam) / h
    rng2 = np.random.default_rng(7)
    v_state = np.zeros_like(x_lam)
    v_state[:-2] = rng2.standard_normal(x_lam.shape[0] - 2)
    v_state[:-2] /= np.linalg.norm(v_state[:-2])
    dR_dstate = (extended_residual(x_lam + h * v_state, solver, w_lam,
                                   ref_rhs, ref_dwdx) - F_lam) / h
    degeneracy = dict(
        note=("directional derivatives of the extended residual at the exact "
              "laminar fixed point; the T and s columns are null by "
              "construction, so the control probes the state block only"),
        norm_dR_dT=float(np.linalg.norm(dR_dT)),
        norm_dR_ds=float(np.linalg.norm(dR_ds)),
        norm_dR_dstate_unit_random_direction=float(np.linalg.norm(dR_dstate)),
        residual_at_exact_fixed_point=float(np.linalg.norm(F_lam)),
    )

    # -- the new layer -----------------------------------------------------
    t0 = time.time()
    hook = newton_hookstep_rpo(w0_guess, 1.0, 0.1, solver, tol=1e-8,
                               max_newton=8, max_gmres=15, fd_eps=1e-6)
    hook_wall = time.time() - t0
    hook_monotone, hook_reduction = summarise(hook["residual_history"])

    # -- leg 353's layer, same inputs, for magnitudes only ------------------
    t0 = time.time()
    line = newton_krylov_rpo(w0_guess, 1.0, 0.1, solver, tol=1e-8,
                             max_newton=8, max_gmres=15, fd_eps=1e-6)
    line_wall = time.time() - t0
    line_monotone, line_reduction = summarise(line["residual_history"])

    record = dict(
        unit="U1",
        milestone="M1",
        kind="MILESTONE (build unit -- no claim, no gate)",
        programme="PROG-R4",
        solver=dict(N=solver.N, Re=solver.Re, n_forcing=solver.n_forcing,
                    dt=solver.dt, state_dim=solver.N * solver.N,
                    unknowns=solver.N * solver.N + 2),
        control=dict(
            description="perturbed laminar fixed point, leg 353's exact setup",
            perturbation_relative=0.01, rng_seed=0,
            T_guess=1.0, s_guess=0.1, tol=1e-8, max_newton=8, max_gmres=15,
            fd_eps=1e-6,
            fixed_point_drift_relative_over_T1=fixed_point_drift,
        ),
        hookstep=dict(
            reason=hook["reason"], success=bool(hook["success"]),
            n_iters=hook["n_iters"],
            residual_history=[float(v) for v in hook["residual_history"]],
            final_residual=float(hook["final_residual"]),
            monotone_decrease=hook_monotone,
            fractional_reduction=hook_reduction,
            T=float(hook["T"]), s=float(hook["s"]),
            n_residual_evals=hook["n_residual_evals"],
            n_jac_evals=hook["n_jac_evals"],
            wall_seconds=hook_wall,
            ledger=hook["ledger"],
        ),
        line_search_reference=dict(
            note=("leg 353's step-halving layer on the SAME inputs. Recorded "
                  "as magnitudes for the ledger; this unit makes no claim "
                  "about which globalisation is better on RPOs -- that is "
                  "gate G1's question and is not answered here."),
            reason=line["reason"], success=bool(line["success"]),
            n_iters=line["n_iters"],
            residual_history=[float(v) for v in line["residual_history"]],
            final_residual=float(line["final_residual"]),
            monotone_decrease=line_monotone,
            fractional_reduction=line_reduction,
            wall_seconds=line_wall,
        ),
        leg353_baseline=dict(
            fractional_reduction=LEG353_FRACTIONAL_REDUCTION,
            monotone_decrease=LEG353_MONOTONE,
            source="writeup/data/p2_route_dsspb5_v1.json (laminar_control)",
        ),
        milestone_check=dict(
            question=("does the laminar-fixed-point control reproduce leg "
                      "353's 99.3% monotone reduction THROUGH the new layer?"),
            hookstep_fractional_reduction=hook_reduction,
            leg353_fractional_reduction=LEG353_FRACTIONAL_REDUCTION,
            reproduced=bool(hook_monotone
                            and hook_reduction >= LEG353_FRACTIONAL_REDUCTION),
        ),
        open_obligations_carried=[
            "CLAY_OBLIGATIONS section 6, obligation 1 (no method) -- OPEN",
            "CLAY_OBLIGATIONS section 6, obligation 2 (no method) -- OPEN",
            ("CLAY_OBLIGATIONS section 4 (finite energy / localisation) -- "
             "OPEN and NOT discharged; stays open in every route-4 gate "
             "until leg 386 (ROUTE-DTOL) lands with a pre-registered delta "
             "mode (user ruling, 2026-08-12)"),
        ],
        degeneracy=degeneracy,
        clay_movement="none -- no L1-L4 link moved by this unit",
    )

    with open(args.out, "w") as f:
        json.dump(record, f, indent=2)

    print(f"fixed-point drift over T=1 : {fixed_point_drift:.3e} (relative)")
    print(f"hookstep    : |R| {hook['residual_history'][0]:.6e} -> "
          f"{hook['final_residual']:.6e}  "
          f"({100 * hook_reduction:.4f}% reduction, "
          f"monotone={hook_monotone}, reason={hook['reason']}, "
          f"iters={hook['n_iters']}, wall={hook_wall:.1f}s)")
    print(f"line search : |R| {line['residual_history'][0]:.6e} -> "
          f"{line['final_residual']:.6e}  "
          f"({100 * line_reduction:.4f}% reduction, "
          f"monotone={line_monotone}, reason={line['reason']}, "
          f"wall={line_wall:.1f}s)")
    print(f"leg 353 recorded baseline  : "
          f"{100 * LEG353_FRACTIONAL_REDUCTION:.4f}% reduction, "
          f"monotone={LEG353_MONOTONE}")
    print(f"M1 reproduced: {record['milestone_check']['reproduced']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
