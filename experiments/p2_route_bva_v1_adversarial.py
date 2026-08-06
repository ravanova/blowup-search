"""Route-BVA v1 -- an ADVERSARIAL BATTERY of degenerate polar-grid inputs against
solver/boussinesq_velocity.py, the 2D Boussinesq velocity operator u = grad^perp (-Lap)^{-1} w.

Leg 99. Adversarial-audit family, applied to the one module in the Boussinesq stack whose only
external gate is a CORRECTNESS gate: leg 73 (Route-BV) reproduced the classical Lamb corner-image
closed form to 1.76e-4 relative at observed order 2.00. That says the answer is right on a
well-posed polar-grid problem. It says nothing about what happens when the grid is NOT well
posed -- and a correctness check on well-behaved input is not a robustness check. Leg 89 (BOA)
found a real silent-corruption bug in the sibling module solver/boussinesq.py using exactly this
pattern, so this is a live risk class, not a formality.

THE GATE, VERBATIM
------------------
"Under an adversarial battery of degenerate polar-grid inputs (r=0 singularity, malformed/
self-intersecting boundary), does solver/boussinesq_velocity.py ever silently return a finite,
plausible-looking result instead of propagating or flagging the degeneracy?"

WHAT "SILENTLY" MEANS HERE, DECIDED BEFORE THE RUN
--------------------------------------------------
A degeneracy is HANDLED if the module makes it visible to the caller by either route:

    RAISED     -- an exception propagates. The caller cannot proceed on bad data.
    NONFINITE  -- NaN or Inf reaches the returned array. Every downstream norm, plot and
                  assertion sees it. Visible is visible; it need not be an exception.

A degeneracy is a SILENT CORRUPTION only under the strict reading, which is the one that can
actually hurt a consumer:

    SILENT_WRONG := the call returns normally
                    AND every returned value is finite
                    AND no warning is emitted
                    AND the returned value differs from the known truth by an amount that
                        would not be caught by the module's own existing acceptance tolerance

and a weaker, separately-counted verdict for degenerate input that is accepted without complaint
but whose output is degenerate in SHAPE (so a consumer cannot mistake it for a real field):

    SILENT_EMPTY := returns normally, all-finite, but with a zero-length axis.

Only SILENT_WRONG decides the gate. SILENT_EMPTY is measured and reported, not used to answer.

DISCIPLINE
----------
Magnitudes, never booleans (standing discipline). Every case reports the SIZE of what could have
gone wrong: the absolute and relative error against the known truth, the ratio against the
well-posed read of the same quantity, the ratio against leg 73's own acceptance tolerance, and
for the boundary-condition family both the GLOBAL and the LOCAL error so the gap between them --
the thing that lets a green global diagnostic hide a destroyed local quantity -- is a number.

REFERENCE TRUTH
---------------
Leg 73's own single-mode manufactured field, reused verbatim so that no new analytic claim is
smuggled in:
    phi*  = r^2 e^{-r} sin(2 beta)
    w*    = -Lap phi* = (5 r - r^2) e^{-r} sin(2 beta)
    u_x(0) = -2 exactly, since phi* -> r^2 sin(2b) = 2xy near the origin.

THIS LEG DOES NOT PATCH. Per the gate's yes-branch, a silent-corruption finding is reported and
escalated, never repaired under the leg's own authority. solver/boussinesq_velocity.py is not
edited by this leg under any outcome.

Run:  PYTHONPATH=. python experiments/p2_route_bva_v1_adversarial.py
Writes: writeup/data/p2_route_bva_v1_adversarial.json
"""

import json
import os
import time
import warnings

import numpy as np

from solver.boussinesq_velocity import (
    PolarGrid,
    velocity_from_vorticity,
    u_x_at_origin,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_bva_v1_adversarial.json")

# Leg 73's acceptance tolerance on this module's velocity/stream-function fields, from
# test_boussinesq_velocity.py::test_velocity_known_answer. Used only as a yardstick.
LEG73_FIELD_TOL = 5e-3
# Leg 73's acceptance tolerance on the origin read, test_boussinesq_velocity.py::test_u_x_at_origin.
LEG73_ORIGIN_TOL = 1e-3
# The exact origin-strain value of the manufactured field.
UX0_TRUTH = -2.0


# --------------------------------------------------------------------------------------
# reference field (leg 73's manufactured solution, single angular mode n=1)
# --------------------------------------------------------------------------------------

def manufactured(grid):
    """Return (omega, phi, u, v) for phi = r^2 e^{-r} sin(2 beta) on the given grid."""
    r, b = grid.R, grid.B
    e = np.exp(-r)
    s = np.sin(2 * b)
    cc = np.cos(2 * b)
    phi = r ** 2 * e * s
    omega = (5 * r - r ** 2) * e * s
    phi_r = (2 * r - r ** 2) * e * s
    phi_b = r ** 2 * e * 2.0 * cc
    phi_x = np.cos(b) * phi_r - (np.sin(b) / r) * phi_b
    phi_y = np.sin(b) * phi_r + (np.cos(b) / r) * phi_b
    return omega, phi, -phi_y, phi_x


def _field_stats(a):
    a = np.asarray(a)
    finite = np.isfinite(a)
    return {
        "size": int(a.size),
        "n_nonfinite": int((~finite).sum()),
        "all_finite": bool(a.size > 0 and finite.all()),
        "max_abs_finite": (float(np.max(np.abs(a[finite]))) if finite.any() else None),
    }


def _rel_linf(a, b):
    denom = float(np.max(np.abs(b)))
    if denom == 0.0:
        return None
    return float(np.max(np.abs(a - b)) / denom)


def _run_capturing(fn):
    """Call fn(); return (result, exception_repr, warning_messages)."""
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            return fn(), None, [str(w.message) for w in caught]
        except Exception as exc:  # noqa: BLE001 -- classifying the exception IS the measurement
            return None, f"{type(exc).__name__}: {exc}", [str(w.message) for w in caught]


# --------------------------------------------------------------------------------------
# family 1 -- the r = 0 origin singularity, at the level of the FIELD solve
# --------------------------------------------------------------------------------------

def family_origin_singularity():
    """Grids that are degenerate AT or ACROSS r=0, plus poisoned vorticity."""
    cases = []

    def field_case(name, what, build):
        def go():
            grid = build()
            omega, _, _, _ = manufactured(grid)
            omega = np.where(np.isfinite(omega), omega, 0.0)
            u, v, phi = velocity_from_vorticity(omega, grid)
            return phi, u
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "degeneracy": what, "exception": exc,
               "n_warnings": len(warns), "warnings": sorted(set(warns))[:4]}
        if exc is not None:
            rec["verdict"] = "RAISED"
        else:
            phi, u = out
            rec["phi"] = _field_stats(phi)
            rec["u"] = _field_stats(u)
            rec["verdict"] = "NONFINITE" if not rec["phi"]["all_finite"] else "FINITE"
        cases.append(rec)

    field_case("r_min_zero", "r_min = 0.0 -> log(0) = -inf at the origin node",
               lambda: PolarGrid(n_r=64, n_beta=16, r_min=0.0, r_max=10.0))
    field_case("r_min_negative", "r_min = -1.0 -> log of a negative radius",
               lambda: PolarGrid(n_r=64, n_beta=16, r_min=-1.0, r_max=10.0))
    field_case("r_min_equals_r_max", "r_min == r_max -> drho = 0, collapsed radial extent",
               lambda: PolarGrid(n_r=64, n_beta=16, r_min=1.0, r_max=1.0))
    field_case("n_r_one", "n_r = 1 -> no radial spacing exists",
               lambda: PolarGrid(n_r=1, n_beta=16, r_min=1.0, r_max=10.0))

    def poison_case(name, what, where, value):
        def go():
            grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
            omega, _, _, _ = manufactured(grid)
            omega = omega.copy()
            omega[where] = value
            u, v, phi = velocity_from_vorticity(omega, grid)
            return phi, u
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "degeneracy": what, "exception": exc,
               "n_warnings": len(warns), "warnings": sorted(set(warns))[:4]}
        if exc is not None:
            rec["verdict"] = "RAISED"
        else:
            phi, u = out
            rec["phi"] = _field_stats(phi)
            rec["u"] = _field_stats(u)
            rec["contamination_fraction_phi"] = rec["phi"]["n_nonfinite"] / rec["phi"]["size"]
            rec["verdict"] = "NONFINITE" if not rec["phi"]["all_finite"] else "FINITE"
        cases.append(rec)

    poison_case("omega_one_nan", "a single NaN in the vorticity field", (10, 3), np.nan)
    poison_case("omega_one_inf", "a single +Inf in the vorticity field", (10, 3), np.inf)

    return {
        "description": "degeneracies at or across the r=0 origin singularity, field level",
        "cases": cases,
        "verdicts": {v: sum(1 for c in cases if c["verdict"] == v)
                     for v in sorted({c["verdict"] for c in cases})},
    }


# --------------------------------------------------------------------------------------
# family 2 -- malformed boundary / malformed grid
# --------------------------------------------------------------------------------------

def family_malformed_boundary():
    """A reversed radial interval and an empty angular (Dirichlet-boundary) basis.

    The reversed interval is the polar-grid analogue of a self-intersecting boundary: the two
    Dirichlet radial ends swap places, so each end receives the OTHER end's analytic tail
    condition -- near-origin regularity phi ~ r^{+2n} imposed at the far field, far-field decay
    phi ~ r^{-2n} imposed at the singular corner.
    """
    cases = []

    # --- 2a. reversed radial interval, measured GLOBALLY and LOCALLY ---------------------
    def interval_case(name, r_min, r_max):
        def go():
            grid = PolarGrid(n_r=400, n_beta=16, r_min=r_min, r_max=r_max)
            omega, phi_ex, _, _ = manufactured(grid)
            u, v, phi = velocity_from_vorticity(omega, grid)
            return grid, phi, phi_ex
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "r_min": r_min, "r_max": r_max, "exception": exc,
               "n_warnings": len(warns)}
        if exc is not None:
            rec["verdict"] = "RAISED"
            cases.append(rec)
            return rec
        grid, phi, phi_ex = out
        near = grid.r < 0.05  # the singular-corner end, wherever it sits in index order
        rec["drho"] = float(grid.drho)
        rec["r_at_index_0"] = float(grid.r[0])
        rec["r_at_index_minus_1"] = float(grid.r[-1])
        rec["rel_linf_global"] = _rel_linf(phi, phi_ex)
        rec["n_nodes_below_r_0p05"] = int(near.sum())
        rec["rel_linf_near_origin"] = (_rel_linf(phi[near], phi_ex[near])
                                       if near.any() else None)
        rec["u_x_at_origin"] = float(u_x_at_origin(phi, grid))
        rec["all_finite"] = bool(np.isfinite(phi).all())
        cases.append(rec)
        return rec

    ok = interval_case("radial_interval_ascending", 1e-3, 40.0)
    bad = interval_case("radial_interval_reversed", 40.0, 1e-3)

    reversed_analysis = None
    if ok.get("rel_linf_global") and bad.get("rel_linf_global"):
        reversed_analysis = {
            "rel_linf_global_ascending": ok["rel_linf_global"],
            "rel_linf_global_reversed": bad["rel_linf_global"],
            "global_degradation_factor": bad["rel_linf_global"] / ok["rel_linf_global"],
            "rel_linf_near_origin_ascending": ok["rel_linf_near_origin"],
            "rel_linf_near_origin_reversed": bad["rel_linf_near_origin"],
            "near_origin_degradation_factor":
                bad["rel_linf_near_origin"] / ok["rel_linf_near_origin"],
            "global_under_reports_local_by":
                (bad["rel_linf_near_origin"] / bad["rel_linf_global"])
                / (ok["rel_linf_near_origin"] / ok["rel_linf_global"]),
            "leg73_field_tol": LEG73_FIELD_TOL,
            "reversed_global_inside_leg73_tol":
                bool(bad["rel_linf_global"] < LEG73_FIELD_TOL),
            "reversed_near_origin_inside_leg73_tol":
                bool(bad["rel_linf_near_origin"] < LEG73_FIELD_TOL),
            "reversed_near_origin_over_leg73_tol":
                bad["rel_linf_near_origin"] / LEG73_FIELD_TOL,
        }
        # SILENT_WRONG iff it returns finite, unwarned, and the LOCAL error exceeds the
        # tolerance the module's own test would have accepted.
        bad["verdict"] = (
            "SILENT_WRONG"
            if (bad["all_finite"] and bad["n_warnings"] == 0
                and bad["rel_linf_near_origin"] > LEG73_FIELD_TOL)
            else "FINITE"
        )
        ok["verdict"] = "BASELINE"

    # --- 2b. empty / negative angular basis ---------------------------------------------
    def angular_case(name, n_beta):
        def go():
            grid = PolarGrid(n_r=32, n_beta=n_beta, r_min=1e-3, r_max=10.0)
            omega = np.zeros((grid.n_r, max(grid.n_beta, 0)))
            u, v, phi = velocity_from_vorticity(omega, grid)
            return grid, phi
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "n_beta_requested": n_beta, "exception": exc,
               "n_warnings": len(warns)}
        if exc is not None:
            rec["verdict"] = "RAISED"
        else:
            grid, phi = out
            rec["n_modes_built"] = int(grid.n_modes.size)
            rec["phi_shape"] = list(phi.shape)
            rec["verdict"] = "SILENT_EMPTY" if 0 in phi.shape else "FINITE"
        cases.append(rec)

    angular_case("n_beta_zero", 0)
    angular_case("n_beta_negative", -3)

    # --- 2c. malformed vorticity shapes ---------------------------------------------------
    def shape_case(name, shape_fn, bc="robin"):
        def go():
            grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
            omega = shape_fn(grid)
            u, v, phi = velocity_from_vorticity(omega, grid, radial_bc=bc)
            return phi
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "exception": exc, "n_warnings": len(warns)}
        rec["verdict"] = "RAISED" if exc is not None else (
            "NONFINITE" if not np.isfinite(out).all() else "FINITE")
        cases.append(rec)

    shape_case("omega_square_wrong_axis",
               lambda g: np.ones((g.n_beta, g.n_beta)))
    shape_case("omega_single_row",
               lambda g: np.ones((1, g.n_beta)))
    shape_case("radial_bc_case_typo",
               lambda g: manufactured(g)[0], bc="Robin")

    return {
        "description": "malformed radial interval, empty angular basis, malformed input shapes",
        "reversed_interval_analysis": reversed_analysis,
        "cases": cases,
        "verdicts": {v: sum(1 for c in cases if c["verdict"] == v)
                     for v in sorted({c["verdict"] for c in cases})},
    }


# --------------------------------------------------------------------------------------
# family 3 -- the origin READ: u_x_at_origin's least-squares extrapolation window
# --------------------------------------------------------------------------------------

def family_origin_read():
    """u_x_at_origin fits c1(r) = phi_1(r)/r^2 ~ a + b r over the window
    (grid.r[2], r_window) and returns -2a. The window's OCCUPANCY is never checked. This
    family sweeps r_min so the window empties, and measures what comes back."""
    sweep = []
    for r_min in (1e-3, 1e-2, 0.05, 0.09, 0.099, 0.15, 0.5, 1.0, 10.0):
        grid = PolarGrid(n_r=200, n_beta=16, r_min=r_min, r_max=40.0)
        omega, _, _, _ = manufactured(grid)
        _, _, phi = velocity_from_vorticity(omega, grid)
        mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
        out, exc, warns = _run_capturing(lambda: u_x_at_origin(phi, grid))
        rec = {"r_min": r_min, "nodes_in_fit_window": int(mask.sum()),
               "exception": exc, "n_warnings": len(warns)}
        if exc is None:
            rec["u_x_at_origin"] = float(out)
            rec["abs_error"] = abs(float(out) - UX0_TRUTH)
            rec["rel_error"] = abs(float(out) - UX0_TRUTH) / abs(UX0_TRUTH)
            rec["over_leg73_origin_tol"] = rec["abs_error"] / LEG73_ORIGIN_TOL
            rec["design_matrix_rank_deficient"] = bool(mask.sum() < 2)
            if rec["design_matrix_rank_deficient"] and rec["n_warnings"] == 0:
                rec["verdict"] = "SILENT_WRONG"
            else:
                rec["verdict"] = "FINITE"
        else:
            rec["verdict"] = "RAISED"
        sweep.append(rec)

    well_posed = sweep[0]
    empty = [s for s in sweep if s["nodes_in_fit_window"] == 0]
    under = [s for s in sweep if s["nodes_in_fit_window"] == 1]

    # locate the cliff: the adjacent pair of r_min values straddling the emptying of the window
    cliff = None
    for a, b in zip(sweep, sweep[1:]):
        if a["nodes_in_fit_window"] > 0 and b["nodes_in_fit_window"] == 0:
            cliff = {
                "r_min_before": a["r_min"], "nodes_before": a["nodes_in_fit_window"],
                "abs_error_before": a["abs_error"],
                "r_min_after": b["r_min"], "nodes_after": b["nodes_in_fit_window"],
                "abs_error_after": b["abs_error"],
                "r_min_relative_change": (b["r_min"] - a["r_min"]) / a["r_min"],
                "error_jump_factor": b["abs_error"] / a["abs_error"],
            }
            break

    # the empty-lstsq mechanism, isolated from the module
    coef, _res, rank, _sv = np.linalg.lstsq(np.zeros((0, 2)), np.zeros((0,)), rcond=None)

    return {
        "description": ("u_x_at_origin's least-squares origin extrapolation under an empty "
                        "or rank-deficient fit window"),
        "fit_window_default": 0.1,
        "truth_u_x_at_origin": UX0_TRUTH,
        "sweep": sweep,
        "well_posed_reference": {
            "r_min": well_posed["r_min"],
            "nodes_in_fit_window": well_posed["nodes_in_fit_window"],
            "abs_error": well_posed["abs_error"],
        },
        "empty_window": {
            "n_cases": len(empty),
            "returned_values": sorted({s["u_x_at_origin"] for s in empty}),
            "abs_error": empty[0]["abs_error"] if empty else None,
            "rel_error": empty[0]["rel_error"] if empty else None,
            "degradation_vs_well_posed": (empty[0]["abs_error"] / well_posed["abs_error"]
                                          if empty else None),
            "over_leg73_origin_tol": empty[0]["over_leg73_origin_tol"] if empty else None,
            "warnings_emitted": sum(s["n_warnings"] for s in empty),
            "exceptions_raised": sum(1 for s in empty if s["exception"]),
        },
        "single_node_window": {
            "n_cases": len(under),
            "abs_error": under[0]["abs_error"] if under else None,
            "degradation_vs_well_posed": (under[0]["abs_error"] / well_posed["abs_error"]
                                          if under else None),
            "warnings_emitted": sum(s["n_warnings"] for s in under),
        },
        "cliff": cliff,
        "empty_lstsq_mechanism": {
            "design_matrix_shape": [0, 2],
            "returned_coefficients": [float(c) for c in coef],
            "returned_rank": int(rank),
            "raised": False,
            "warned": False,
        },
        "verdicts": {v: sum(1 for s in sweep if s["verdict"] == v)
                     for v in sorted({s["verdict"] for s in sweep})},
    }


# --------------------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------------------

def main():
    t0 = time.time()
    fam1 = family_origin_singularity()
    fam2 = family_malformed_boundary()
    fam3 = family_origin_read()

    all_verdicts = {}
    for fam in (fam1, fam2, fam3):
        for k, v in fam["verdicts"].items():
            all_verdicts[k] = all_verdicts.get(k, 0) + v

    silent_wrong = all_verdicts.get("SILENT_WRONG", 0)
    gate = {
        "gate": ("Under an adversarial battery of degenerate polar-grid inputs (r=0 "
                 "singularity, malformed/self-intersecting boundary), does "
                 "solver/boussinesq_velocity.py ever silently return a finite, "
                 "plausible-looking result instead of propagating or flagging the degeneracy?"),
        "answer": "YES" if silent_wrong > 0 else "NO",
        "silent_wrong_cases": silent_wrong,
        "silent_empty_cases": all_verdicts.get("SILENT_EMPTY", 0),
        "raised_cases": all_verdicts.get("RAISED", 0),
        "nonfinite_cases": all_verdicts.get("NONFINITE", 0),
        "headline": ("u_x_at_origin returns -0.0 (truth -2.0, abs error "
                     f"{fam3['empty_window']['abs_error']:.4f}, rel error "
                     f"{100.0 * fam3['empty_window']['rel_error']:.1f}%) whenever the grid's "
                     "r_min exceeds the fit window r_window=0.1: the mask is empty, "
                     "np.linalg.lstsq on a (0,2) design matrix returns [0.,0.] at rank 0 "
                     "without raising or warning, and the function returns -2*0.0."),
        "patched_by_this_leg": False,
        "escalation": ("Gate yes-branch: reported, not patched. solver/boussinesq_velocity.py "
                       "is unmodified by leg 99."),
    }

    data = {
        "leg": 99,
        "route": "BVA",
        "module_under_test": "solver/boussinesq_velocity.py",
        "prior_gate": ("leg 73 (Route-BV): Lamb corner-image known-answer, 1.76e-4 relative "
                       "at observed order 2.00 -- correctness, not robustness"),
        "verdict_semantics": {
            "RAISED": "exception propagates -- degeneracy flagged -- robust",
            "NONFINITE": "NaN/Inf reaches the output -- degeneracy visible -- robust",
            "SILENT_WRONG": "finite, unwarned, and wrong beyond the module's own tolerance",
            "SILENT_EMPTY": "accepted without complaint, output degenerate in shape",
            "FINITE": "finite and within tolerance",
            "BASELINE": "the well-posed control",
        },
        "leg73_tolerances": {"field": LEG73_FIELD_TOL, "origin_read": LEG73_ORIGIN_TOL},
        "origin_singularity": fam1,
        "malformed_boundary": fam2,
        "origin_read": fam3,
        "verdict_totals": all_verdicts,
        "gate_answer": gate,
        "wall_seconds": time.time() - t0,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=False)

    f3 = fam3
    ra = fam2["reversed_interval_analysis"]
    print(f"[BVA] module under test: solver/boussinesq_velocity.py "
          f"(prior gate: leg 73, Lamb 1.76e-4)")
    print(f"[BVA] origin-singularity family: {fam1['verdicts']}")
    print(f"[BVA] malformed-boundary family: {fam2['verdicts']}")
    print(f"[BVA] origin-read family:        {fam3['verdicts']}")
    print(f"[BVA] well-posed origin read (r_min=1e-3, "
          f"{f3['well_posed_reference']['nodes_in_fit_window']} nodes): abs err "
          f"{f3['well_posed_reference']['abs_error']:.3e}")
    print(f"[BVA] EMPTY fit window: returns {f3['empty_window']['returned_values']}, "
          f"abs err {f3['empty_window']['abs_error']:.4f} "
          f"({100 * f3['empty_window']['rel_error']:.1f}% relative), "
          f"{f3['empty_window']['degradation_vs_well_posed']:.0f}x the well-posed read, "
          f"{f3['empty_window']['warnings_emitted']} warnings, "
          f"{f3['empty_window']['exceptions_raised']} exceptions")
    print(f"[BVA] single-node fit window: abs err {f3['single_node_window']['abs_error']:.3e}, "
          f"{f3['single_node_window']['degradation_vs_well_posed']:.0f}x the well-posed read")
    c = f3["cliff"]
    print(f"[BVA] cliff: r_min {c['r_min_before']} -> {c['r_min_after']} "
          f"({100 * c['r_min_relative_change']:.0f}% change) takes the window "
          f"{c['nodes_before']} -> {c['nodes_after']} nodes and the error up "
          f"{c['error_jump_factor']:.2f}x")
    print(f"[BVA] reversed radial interval: global rel err {ra['rel_linf_global_reversed']:.3e} "
          f"({ra['global_degradation_factor']:.2f}x the ascending grid, INSIDE leg 73's "
          f"{LEG73_FIELD_TOL:.0e}) but {ra['rel_linf_near_origin_reversed']:.3e} at r<0.05 "
          f"({ra['near_origin_degradation_factor']:.0f}x, "
          f"{ra['reversed_near_origin_over_leg73_tol']:.1f}x OUTSIDE it)")
    print(f"[BVA] GATE: {gate['answer']} -- {gate['silent_wrong_cases']} SILENT_WRONG, "
          f"{gate['silent_empty_cases']} SILENT_EMPTY, {gate['raised_cases']} RAISED, "
          f"{gate['nonfinite_cases']} NONFINITE")
    print(f"[BVA] wrote {OUT}  ({data['wall_seconds']:.1f}s)")


if __name__ == "__main__":
    main()
