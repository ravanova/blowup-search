"""Route-BVB v1 -- the POST-REPAIR REGRESSION CHECK of solver/boussinesq_velocity.py across
leg 99's FULL original adversarial battery (22 cases, three families), plus an independent
re-run of leg 73's Lamb corner-image benchmark.

THE GATE, verbatim from DIRECTION.md leg 104:

    Post-repair, does solver/boussinesq_velocity.py (a) no longer return -0.0 on any of leg
    99's original failing degenerate-grid cases, and (b) still reproduce leg 73's Lamb
    corner-image benchmark with zero regression?

WHY THIS IS NOT A REPEAT (see writeup/novelty/leg_104.md for the full pass)
----------------------------------------------------------------------------------------------
The bench-repair (commit 26e6bd3, merged as e3bdd9f) re-ran ONE benchmark (leg 73's) and
sampled THREE of leg 99's 22 cases in test_boussinesq_velocity_adversarial.py. Leg 99's own
battery script, experiments/p2_route_bva_v1_adversarial.py, is deliberately frozen against the
UNPATCHED module and confirmed (leg_104.md sec.2) to raise KeyError if called post-repair --
its family_malformed_boundary() only assigns the ascending control's verdict inside a branch
that requires the reversed case to ALSO have returned normally, which is no longer true once the
reversed case is refused at construction. So this runner reimplements the 22 cases fresh,
independently, against the CURRENT module, rather than importing or patching that frozen file.

METHOD
------
1. Re-run leg 99's exact 22 cases (same manufactured field, same grid parameters, same 9-point
   r_min sweep) against the installed solver/boussinesq_velocity.py, classifying each by the
   SAME predicate leg 99 pre-committed:
       RAISED     -- an exception propagates. Robust.
       NONFINITE  -- NaN/Inf reaches the output. Robust (visible).
       SILENT_WRONG := returns normally, all finite, unwarned, and wrong beyond the module's
                       own acceptance tolerance (leg 73: 5e-3 fields, 1e-3 origin read).
       SILENT_EMPTY  -- accepted without complaint, output degenerate in SHAPE. Weak, not a
                        gate decider (unchanged from leg 99: n_beta<=0 was NOT patched).
       FINITE / BASELINE -- returns, finite, inside tolerance.
   Gate (a) is YES iff SILENT_WRONG == 0 over the full 22, not a sample.
2. Independently re-run leg 73's exact 3-level ladder via `run_level`, IMPORTED (never via its
   main(), so its own frozen JSON at writeup/data/p2_route_bv_v1_velocity_benchmark.json is
   never written by this leg) from experiments/p2_route_bv_v1_velocity_benchmark.py, and compare
   P1/P3 finest + observed orders against that banked JSON. A same-code-twice noise floor is
   measured (not assumed) to set the tolerance that separates "reproduces" from floating-point
   BLAS-order jitter.

This runner READS solver/boussinesq_velocity.py and experiments/p2_route_bv_v1_velocity_benchmark.py.
It edits neither, and it writes only its own file, writeup/data/p2_route_bvb_v1_postrepair.json.

Run:  PYTHONPATH=. .venv/bin/python experiments/p2_route_bvb_v1_postrepair.py
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
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_bvb_v1_postrepair.json")
LEG73_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_bv_v1_velocity_benchmark.json")
LEG99_JSON = os.path.join(ROOT, "writeup", "data", "p2_route_bva_v1_adversarial.json")

LEG73_FIELD_TOL = 5e-3
LEG73_ORIGIN_TOL = 1e-3
UX0_TRUTH = -2.0


# --------------------------------------------------------------------------------------
# leg 73's own manufactured field (single angular mode n=1), reused verbatim: no new
# analytic claim is introduced.
# --------------------------------------------------------------------------------------

def manufactured(grid):
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


def _run_capturing(fn):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            return fn(), None, [str(w.message) for w in caught]
        except Exception as exc:  # noqa: BLE001 -- classifying the exception IS the measurement
            return None, f"{type(exc).__name__}: {exc}", [str(w.message) for w in caught]


def _rel_linf(a, b):
    denom = float(np.max(np.abs(b)))
    if denom == 0.0:
        return None
    return float(np.max(np.abs(a - b)) / denom)


# --------------------------------------------------------------------------------------
# FAMILY 1 -- origin singularity at the field-solve level (6 cases, leg 99 sec. "family 1")
# --------------------------------------------------------------------------------------

def family_origin_singularity():
    cases = []

    def field_case(name, what, build):
        def go():
            grid = build()
            omega, _, _, _ = manufactured(grid)
            omega = np.where(np.isfinite(omega), omega, 0.0)
            u, v, phi = velocity_from_vorticity(omega, grid)
            return phi, u
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "degeneracy": what, "exception": exc, "n_warnings": len(warns)}
        if exc is not None:
            rec["verdict"] = "RAISED"
        else:
            phi, u = out
            all_finite_phi = bool(np.isfinite(phi).all())
            rec["all_finite"] = all_finite_phi
            rec["n_nonfinite_phi"] = int((~np.isfinite(phi)).sum())
            rec["verdict"] = "FINITE" if all_finite_phi else "NONFINITE"
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
        rec = {"case": name, "degeneracy": what, "exception": exc, "n_warnings": len(warns)}
        if exc is not None:
            rec["verdict"] = "RAISED"
        else:
            phi, u = out
            all_finite_phi = bool(np.isfinite(phi).all())
            rec["all_finite"] = all_finite_phi
            rec["n_nonfinite_phi"] = int((~np.isfinite(phi)).sum())
            rec["verdict"] = "FINITE" if all_finite_phi else "NONFINITE"
        cases.append(rec)

    poison_case("omega_one_nan", "a single NaN in the vorticity field", (10, 3), np.nan)
    poison_case("omega_one_inf", "a single +Inf in the vorticity field", (10, 3), np.inf)

    return {
        "description": "degeneracies at or across the r=0 origin singularity, field level",
        "cases": cases,
        "n_cases": len(cases),
        "verdicts": {v: sum(1 for c in cases if c["verdict"] == v)
                     for v in sorted({c["verdict"] for c in cases})},
    }


# --------------------------------------------------------------------------------------
# FAMILY 2 -- malformed boundary / malformed grid (7 cases, leg 99 sec. "family 2")
# --------------------------------------------------------------------------------------

def family_malformed_boundary():
    """Rewritten independently of leg 99's frozen script (which KeyErrors post-repair, see
    writeup/novelty/leg_104.md sec.2): every case's verdict is set unconditionally, never
    gated on a sibling case's outcome."""
    cases = []

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
        near = grid.r < 0.05
        rec["drho"] = float(grid.drho)
        rec["rel_linf_global"] = _rel_linf(phi, phi_ex)
        rec["rel_linf_near_origin"] = _rel_linf(phi[near], phi_ex[near]) if near.any() else None
        u_x0, u_exc, _ = _run_capturing(lambda: u_x_at_origin(phi, grid))
        rec["u_x_at_origin"] = float(u_x0) if u_exc is None else None
        rec["u_x_at_origin_exception"] = u_exc
        all_fin = bool(np.isfinite(phi).all())
        rec["all_finite"] = all_fin
        if not all_fin:
            rec["verdict"] = "NONFINITE"
        elif (rec["n_warnings"] == 0 and rec["rel_linf_near_origin"] is not None
              and rec["rel_linf_near_origin"] > LEG73_FIELD_TOL):
            rec["verdict"] = "SILENT_WRONG"
        else:
            rec["verdict"] = "FINITE"
        cases.append(rec)
        return rec

    ok = interval_case("radial_interval_ascending", 1e-3, 40.0)
    ok["verdict"] = "BASELINE"  # the well-posed control, unconditionally labelled
    bad = interval_case("radial_interval_reversed", 40.0, 1e-3)

    interval_analysis = None
    if ok.get("rel_linf_global") is not None:
        interval_analysis = {
            "ascending_rel_linf_global": ok["rel_linf_global"],
            "ascending_rel_linf_near_origin": ok["rel_linf_near_origin"],
            "ascending_inside_leg73_field_tol": bool(ok["rel_linf_near_origin"] < LEG73_FIELD_TOL),
            "reversed_case_verdict": bad["verdict"],
            "reversed_case_exception": bad.get("exception"),
        }

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

    def shape_case(name, shape_fn, bc="robin"):
        def go():
            grid = PolarGrid(n_r=64, n_beta=16, r_min=1e-3, r_max=10.0)
            omega = shape_fn(grid)
            u, v, phi = velocity_from_vorticity(omega, grid, radial_bc=bc)
            return phi
        out, exc, warns = _run_capturing(go)
        rec = {"case": name, "exception": exc, "n_warnings": len(warns)}
        if exc is not None:
            rec["verdict"] = "RAISED"
        else:
            rec["verdict"] = "NONFINITE" if not np.isfinite(out).all() else "FINITE"
        cases.append(rec)

    shape_case("omega_square_wrong_axis", lambda g: np.ones((g.n_beta, g.n_beta)))
    shape_case("omega_single_row", lambda g: np.ones((1, g.n_beta)))
    shape_case("radial_bc_case_typo", lambda g: manufactured(g)[0], bc="Robin")

    return {
        "description": "malformed radial interval, empty angular basis, malformed input shapes",
        "interval_analysis": interval_analysis,
        "cases": cases,
        "n_cases": len(cases),
        "verdicts": {v: sum(1 for c in cases if c["verdict"] == v)
                     for v in sorted({c["verdict"] for c in cases})},
    }


# --------------------------------------------------------------------------------------
# FAMILY 3 -- the origin READ: u_x_at_origin's fit window, the full 9-point sweep
# (leg 99 sec. "family 3" -- THE headline mechanism)
# --------------------------------------------------------------------------------------

def family_origin_read():
    sweep = []
    for r_min in (1e-3, 1e-2, 0.05, 0.09, 0.099, 0.15, 0.5, 1.0, 10.0):
        grid = PolarGrid(n_r=200, n_beta=16, r_min=r_min, r_max=40.0)
        omega, _, _, _ = manufactured(grid)
        _, _, phi = velocity_from_vorticity(omega, grid)
        mask = (grid.r > grid.r[2]) & (grid.r < 0.1)
        out, exc, warns = _run_capturing(lambda: u_x_at_origin(phi, grid))
        # leg 99's OWN predicate for this family (not a tolerance-exceedance test): a
        # design matrix with fewer than 2 in-window nodes is rank-deficient for the
        # two-parameter fit, and SILENT_WRONG is "rank-deficient yet no exception, no
        # warning" -- structural, not accuracy-based, because even the well-posed reads on
        # this coarse (n_r=200) grid sit above leg 73's tight 1e-3 origin tolerance (leg 73
        # itself uses an 800x48 grid for that number) without being a corruption.
        rank_deficient = bool(mask.sum() < 2)
        rec = {"r_min": r_min, "nodes_in_fit_window": int(mask.sum()),
               "design_matrix_rank_deficient": rank_deficient,
               "exception": exc, "n_warnings": len(warns)}
        if exc is None:
            rec["u_x_at_origin"] = float(out)
            rec["abs_error"] = abs(float(out) - UX0_TRUTH)
            rec["rel_error"] = abs(float(out) - UX0_TRUTH) / abs(UX0_TRUTH)
            rec["is_minus_zero"] = bool(out == 0.0 and np.signbit(out))
            if rank_deficient and rec["n_warnings"] == 0:
                rec["verdict"] = "SILENT_WRONG"
            else:
                rec["verdict"] = "FINITE"
        else:
            rec["is_minus_zero"] = False
            rec["verdict"] = "RAISED"
        sweep.append(rec)

    well_posed = sweep[0]
    n_silent_wrong = sum(1 for s in sweep if s["verdict"] == "SILENT_WRONG")
    n_minus_zero = sum(1 for s in sweep if s.get("is_minus_zero"))
    formerly_empty_or_thin = [s for s in sweep if s["r_min"] >= 0.09]  # leg 99's 6 failing points

    return {
        "description": ("u_x_at_origin's least-squares origin extrapolation, full 9-point "
                        "r_min sweep -- leg 99's exact battery, re-run against the patched "
                        "module"),
        "fit_window_default": 0.1,
        "truth_u_x_at_origin": UX0_TRUTH,
        "sweep": sweep,
        "n_cases": len(sweep),
        "well_posed_reference": {"r_min": well_posed["r_min"],
                                  "nodes_in_fit_window": well_posed["nodes_in_fit_window"],
                                  "abs_error": well_posed["abs_error"]},
        "n_silent_wrong": n_silent_wrong,
        "n_returned_minus_zero": n_minus_zero,
        "formerly_failing_points_now": [
            {"r_min": s["r_min"], "nodes": s["nodes_in_fit_window"], "verdict": s["verdict"],
             "exception_type": (s["exception"].split(":")[0] if s.get("exception") else None)}
            for s in formerly_empty_or_thin
        ],
        "verdicts": {v: sum(1 for s in sweep if s["verdict"] == v)
                     for v in sorted({s["verdict"] for s in sweep})},
    }


# --------------------------------------------------------------------------------------
# LEG 73 REPRODUCTION -- independent re-run of the Lamb corner-image ladder
# --------------------------------------------------------------------------------------

def leg73_reproduction():
    """Imports run_level from leg 73's own benchmark module (never calling its main(), so
    its frozen JSON is never written by this leg) and re-runs the exact 3-level ladder,
    twice, to (a) compare against the banked JSON and (b) measure the same-code-twice noise
    floor that separates 'reproduces' from BLAS-order floating-point jitter."""
    import sys
    sys.path.insert(0, ROOT)
    from experiments.p2_route_bv_v1_velocity_benchmark import (  # noqa: E402
        run_level, LADDER, observed_order,
    )

    def one_pass():
        levels = [run_level(n_r, n_beta, "robin") for n_r, n_beta in LADDER]
        p1 = [lv["p1_rel_err_centre_velocity"] for lv in levels]
        p3 = [lv["p3_rel_l2_phi_window"] for lv in levels]
        return p1, p3

    t0 = time.time()
    p1_a, p3_a = one_pass()
    p1_b, p3_b = one_pass()  # same code, same process, twice: the noise floor
    wall = time.time() - t0

    ord1_a, ord3_a = observed_order(p1_a), observed_order(p3_a)
    ord1_b, ord3_b = observed_order(p1_b), observed_order(p3_b)

    noise_p1 = max(abs(a - b) / a for a, b in zip(p1_a, p1_b))
    noise_p3 = max(abs(a - b) / a for a, b in zip(p3_a, p3_b))
    noise_floor = max(noise_p1, noise_p3, 1e-12)  # floor to avoid a zero tolerance

    banked = None
    diff_vs_banked = None
    if os.path.exists(LEG73_JSON):
        with open(LEG73_JSON) as fh:
            banked = json.load(fh)
        bv = banked["verdict"]
        diff_vs_banked = {
            "p1_finest_diff_rel": abs(p1_a[-1] - bv["p1_finest"]) / bv["p1_finest"],
            "p3_finest_diff_rel": abs(p3_a[-1] - bv["p3_finest"]) / bv["p3_finest"],
            "p1_errors_banked": bv["p1_errors"],
            "p1_errors_here": p1_a,
            "p3_errors_banked": bv["p3_errors"],
            "p3_errors_here": p3_a,
        }

    # judge reproduction at a tolerance that is generously above the measured same-code
    # noise floor (10x it, floored at 1e-8) rather than demanding literal bit-identity,
    # which BLAS-order nondeterminism across process runs does not guarantee.
    tol = max(10.0 * noise_floor, 1e-8)
    reproduces = (diff_vs_banked is not None
                  and diff_vs_banked["p1_finest_diff_rel"] < tol
                  and diff_vs_banked["p3_finest_diff_rel"] < tol)

    return {
        "description": ("independent re-run of leg 73's Lamb corner-image ladder via "
                        "run_level(), imported (main() never called; the leg 73 JSON is "
                        "never written by this leg)"),
        "ladder": list(LADDER),
        "p1_errors": p1_a, "p3_errors": p3_a,
        "p1_observed_orders": ord1_a, "p3_observed_orders": ord3_a,
        "p1_finest": p1_a[-1], "p3_finest": p3_a[-1],
        "same_code_twice_noise_floor": {
            "p1_errors_pass_b": p1_b, "p3_errors_pass_b": p3_b,
            "p1_observed_orders_pass_b": ord1_b, "p3_observed_orders_pass_b": ord3_b,
            "max_rel_diff_p1": noise_p1, "max_rel_diff_p3": noise_p3,
            "note": ("the SAME unmodified code run twice in this same process differs at "
                     "this scale purely from BLAS/threading floating-point-order effects; "
                     "the reproduction tolerance below is set 10x above this floor"),
        },
        "banked_json_path": os.path.relpath(LEG73_JSON, ROOT),
        "diff_vs_banked": diff_vs_banked,
        "reproduction_tolerance_used": tol,
        "reproduces_banked_result": bool(reproduces),
        "wall_seconds": wall,
    }


# --------------------------------------------------------------------------------------
# assembly
# --------------------------------------------------------------------------------------

def main():
    t0 = time.time()
    fam1 = family_origin_singularity()
    fam2 = family_malformed_boundary()
    fam3 = family_origin_read()
    leg73 = leg73_reproduction()

    all_verdicts = {}
    for fam in (fam1, fam2, fam3):
        for k, v in fam["verdicts"].items():
            all_verdicts[k] = all_verdicts.get(k, 0) + v

    n_cases_total = fam1["n_cases"] + fam2["n_cases"] + fam3["n_cases"]
    silent_wrong = all_verdicts.get("SILENT_WRONG", 0)
    minus_zero_count = fam3["n_returned_minus_zero"]

    gate_a = "YES" if (silent_wrong == 0 and minus_zero_count == 0) else "NO"
    gate_b = "YES" if leg73["reproduces_banked_result"] else "NO"

    gate = {
        "gate": ("Post-repair, does solver/boussinesq_velocity.py (a) no longer return -0.0 "
                 "on any of leg 99's original failing degenerate-grid cases, and (b) still "
                 "reproduce leg 73's Lamb corner-image benchmark with zero regression?"),
        "n_cases_checked": n_cases_total,
        "n_cases_leg99_original": 22,
        "clause_a_no_silent_wrong": gate_a,
        "clause_a_silent_wrong_count": silent_wrong,
        "clause_a_minus_zero_count": minus_zero_count,
        "clause_b_leg73_reproduces": gate_b,
        "answer": "YES" if (gate_a == "YES" and gate_b == "YES") else "NO",
        "action": ("banked as a permanent regression suite alongside legs 73 and 99"
                   if (gate_a == "YES" and gate_b == "YES")
                   else "escalate: an incomplete fix or a repair regression"),
    }

    data = {
        "leg": 104,
        "route": "BVB",
        "module_under_test": "solver/boussinesq_velocity.py",
        "prior_legs": {
            73: "Route-BV: Lamb corner-image known-answer, 1.76e-4 relative, order 2.00",
            99: ("Route-BVA: adversarial audit, 7/22 SILENT_WRONG found, escalated, then "
                 "bench-repaired (26e6bd3 / e3bdd9f) bundled with the same leg"),
        },
        "repair_commit": "26e6bd3 (merged as e3bdd9f, bench/fix-boussinesq-velocity-origin-fit)",
        "verdict_semantics": {
            "RAISED": "exception propagates -- degeneracy flagged -- robust",
            "NONFINITE": "NaN/Inf reaches the output -- degeneracy visible -- robust",
            "SILENT_WRONG": "finite, unwarned, and wrong beyond the module's own tolerance",
            "SILENT_EMPTY": "accepted without complaint, output degenerate in shape (weak; "
                            "not a gate decider, matches leg 99's own predicate)",
            "FINITE": "finite and within tolerance",
            "BASELINE": "the well-posed control",
        },
        "leg73_tolerances": {"field": LEG73_FIELD_TOL, "origin_read": LEG73_ORIGIN_TOL},
        "origin_singularity": fam1,
        "malformed_boundary": fam2,
        "origin_read": fam3,
        "verdict_totals": all_verdicts,
        "leg73_reproduction": leg73,
        "gate_answer": gate,
        "wall_seconds": time.time() - t0,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=False)

    print(f"[BVB] leg 104 post-repair check of solver/boussinesq_velocity.py, "
          f"{n_cases_total} cases (leg 99 had 22)")
    print(f"[BVB] family 1 (origin singularity): {fam1['verdicts']}")
    print(f"[BVB] family 2 (malformed boundary):  {fam2['verdicts']}")
    print(f"[BVB] family 3 (origin read, 9-pt sweep): {fam3['verdicts']}")
    for s in fam3["formerly_failing_points_now"]:
        print(f"[BVB]   r_min={s['r_min']:<8} nodes={s['nodes']}  now: {s['verdict']}"
              f"{' (' + s['exception_type'] + ')' if s['exception_type'] else ''}")
    print(f"[BVB] SILENT_WRONG total: {silent_wrong} (leg 99 originally measured 7)")
    print(f"[BVB] returned -0.0 anywhere: {minus_zero_count} (leg 99 originally measured 5)")
    print(f"[BVB] leg 73 reproduction: P1 finest {leg73['p1_finest']:.6e}, "
          f"P3 finest {leg73['p3_finest']:.6e}, orders P1 "
          f"{['%.2f' % o for o in leg73['p1_observed_orders']]}, "
          f"reproduces_banked={leg73['reproduces_banked_result']} "
          f"(same-code-twice noise floor {leg73['same_code_twice_noise_floor']['max_rel_diff_p1']:.2e}, "
          f"tol used {leg73['reproduction_tolerance_used']:.2e})")
    print(f"[BVB] GATE: clause (a)={gate['clause_a_no_silent_wrong']}, "
          f"clause (b)={gate['clause_b_leg73_reproduces']} -> {gate['answer']}")
    print(f"[BVB] wrote {OUT}  ({data['wall_seconds']:.1f}s)")


if __name__ == "__main__":
    main()
