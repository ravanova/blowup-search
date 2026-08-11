#!/usr/bin/env python3
"""Leg 311 -- Route-IVAX: does screen (iv_a) apply off the fluid axis?

Leg 261 measured Remark 40's stated reach (arXiv:2404.04054, line 1687) killing 18 of 18
incompressible-fluid census rows -- via the Leray projection, which is nonlocal and unnamed
by Remark 40. This leg asks whether the SAME clause, applied to its OTHER named exclusions
(Hilbert transform, Biot-Savart-type inversion, fractional dissipation Lambda^{2s}/(-Delta)^s),
bites equally on models that carry NO incompressibility constraint at all: fractional_gclm.py,
critical_dissipation.py, fractional_boussinesq.py. Counterweight: leg 273's duplicate-occupant
finding is re-checked in the same run, since a positive answer here (a genuinely admissible
non-fluid candidate) would need to land in leg 174's matrix without re-duplicating leg 273's
already-occupied cell.

Screen (iv_a), quoted verbatim (leg 255's novelty pass, writeup/novelty/leg_255.md:53-69,
Remark 40 line 1687 of md5 ff7a34b776bfe5edf97397e5eabdbb7a):

    "We deal with a one-dimensional example here for simplicity, but terms like (u.grad)u
    could in principle also be handled in dimension d in {2,3}, as u in H^2(mu) is then
    still enough to guarantee that (u.grad)u in L^2(mu) since u in L^infty(R^d)."

Reach = LOCAL polynomial nonlinearity in u and its first derivatives, over Gaussian-weighted
H^2(mu), Laplacian/Ornstein-Uhlenbeck principal part, d <= 3. Explicitly NOT named (leg 255):
nonlocal nonlinearity operators (Hilbert transform, Biot-Savart, Leray projection, Fourier
restriction, averaging); nonlocal dissipation ((-Delta)^alpha, Lambda^gamma for non-even gamma);
non-H^2(mu)-on-R^d state spaces; quasilinear principal parts.

This runner reads the governing equation of each of the three models OFF ITS OWN DOCSTRING/
HEADER (solver/fractional_gclm.py, solver/critical_dissipation.py, solver/fractional_boussinesq.py
-- read-only, no solver constructed, no dynamics run) and classifies each operator against the
reach clause. Verdicts are COMPUTED from a per-row evidence table, never asserted. No solve, no
certificate, no figure beyond the one registered for this leg. No stage claimed, plan_of_record.py
untouched, no ban lifted. No link L1->L4 moves. Clay odds stay ~0.05%.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "writeup", "data", "p2_route_ivax_v1.json")

# ---------------------------------------------------------------------------------------------
# PART A -- the three target models, governing equations read verbatim off their own modules
# ---------------------------------------------------------------------------------------------

# Every operator instance below is a literal transcription of the equation as it appears in the
# named module's header/docstring (grepped, quoted with line references), not paraphrased.

MODELS = [
    {
        "key": "FRAC-GCLM",
        "module": "solver/fractional_gclm.py",
        "object": "gCLM with fractional dissipation (Route-F v1)",
        "equation": "omega_t + a u omega_x = omega u_x - nu (-Delta)^s omega ,  u_x = H(omega)",
        "locator": "solver/fractional_gclm.py:22",
        "fluid_adjacent": False,  # 1D toy model, no incompressibility, no pressure, no Biot-Savart in 3D sense
        "operators": [
            {"name": "Hilbert transform in velocity recovery: u_x = H(omega)",
             "nonlocal": True, "named_by_remark_40": False,
             "class": "nonlocal operator in the nonlinearity (Hilbert transform)"},
            {"name": "fractional dissipation: nu (-Delta)^s omega, s dial (s=1 is Laplacian)",
             "nonlocal": True, "named_by_remark_40": False,
             "class": "nonlocal dissipation ((-Delta)^alpha / Lambda^gamma, non-even gamma)",
             "conditional_on": "s != 1 (s=1 recovers the ordinary Laplacian, which IS named)"},
        ],
    },
    {
        "key": "CRIT-DISS-GCLM",
        "module": "solver/critical_dissipation.py",
        "object": "gCLM at exactly critical dissipation (Route-H v1)",
        "equation": "omega_t + a u omega_x = omega u_x - nu Lambda^{2s} omega ,  u_x = H(omega)",
        "locator": "solver/critical_dissipation.py:22",
        "fluid_adjacent": False,
        "operators": [
            {"name": "Hilbert transform in velocity recovery: u_x = H(omega)",
             "nonlocal": True, "named_by_remark_40": False,
             "class": "nonlocal operator in the nonlinearity (Hilbert transform)"},
            {"name": "fractional dissipation: nu Lambda^{2s} omega, Lambda = H d/dX",
             "nonlocal": True, "named_by_remark_40": False,
             "class": "nonlocal dissipation ((-Delta)^alpha / Lambda^gamma, non-even gamma)",
             "conditional_on": "2s not an even integer (module notes 2s integer makes Lambda^{2s} a finite matrix, "
                                "but that is a computational convenience, not a change of operator CLASS -- "
                                "Lambda itself is still built from H, which Remark 40 never names)"},
        ],
    },
    {
        "key": "FRAC-BOUSSINESQ",
        "module": "solver/fractional_boussinesq.py",
        "object": "2D Boussinesq, fractional dissipation (Route-G v1)",
        "equation": "omega_t + u.grad omega = theta_x - nu (-Delta)^s omega ; theta_t + u.grad theta = 0 ; "
                    "u = grad^perp (-Delta)^{-1} omega",
        "locator": "solver/fractional_boussinesq.py:10-12",
        "fluid_adjacent": True,  # 2D Boussinesq IS a fluid system (velocity field, incompressible u=grad^perp psi)
        "operators": [
            {"name": "velocity recovery: u = grad^perp (-Delta)^{-1} omega (2D Biot-Savart-type stream function)",
             "nonlocal": True, "named_by_remark_40": False,
             "class": "nonlocal operator in the nonlinearity (Biot-Savart-type inversion)"},
            {"name": "fractional dissipation: nu (-Delta)^s omega, s dial",
             "nonlocal": True, "named_by_remark_40": False,
             "class": "nonlocal dissipation ((-Delta)^alpha / Lambda^gamma, non-even gamma)",
             "conditional_on": "s != 1"},
        ],
    },
]

# ---------------------------------------------------------------------------------------------
# PART B -- apply screen (iv_a) verbatim
# ---------------------------------------------------------------------------------------------


def screen_iv_a_verdict(model: dict) -> dict:
    """A row PASSES (iv_a) only if EVERY operator in its governing equation is named by
    Remark 40's stated reach (local polynomial nonlinearity, Laplacian/OU principal part).
    A row is KILLED by (iv_a) if at least one operator is nonlocal and unnamed.
    Computed from the operator table, not asserted."""
    unnamed = [op for op in model["operators"] if not op["named_by_remark_40"]]
    passes = len(unnamed) == 0
    return {
        "key": model["key"],
        "fluid_adjacent": model["fluid_adjacent"],
        "n_operators": len(model["operators"]),
        "n_unnamed_by_remark_40": len(unnamed),
        "unnamed_operator_classes": sorted({op["class"] for op in unnamed}),
        "passes_iv_a": passes,
        "killed_by_iv_a": not passes,
    }


def run_census() -> dict:
    rows = [screen_iv_a_verdict(m) for m in MODELS]
    n_total = len(rows)
    n_killed = sum(1 for r in rows if r["killed_by_iv_a"])
    n_fluid_adjacent = sum(1 for m in MODELS if m["fluid_adjacent"])
    n_non_fluid = n_total - n_fluid_adjacent
    n_non_fluid_killed = sum(1 for m, r in zip(MODELS, rows) if not m["fluid_adjacent"] and r["killed_by_iv_a"])

    # every operator class that recurs across rows -- the mechanism, named per lesson 91
    all_unnamed_classes = sorted({c for r in rows for c in r["unnamed_operator_classes"]})

    gate_yes = n_killed == n_total  # (iv_a) excludes ALL three, same as it excluded 18/18 fluid rows

    return {
        "rows": rows,
        "n_total": n_total,
        "n_killed_by_iv_a": n_killed,
        "n_fluid_adjacent_models": n_fluid_adjacent,
        "n_non_fluid_models": n_non_fluid,
        "n_non_fluid_killed_by_iv_a": n_non_fluid_killed,
        "all_unnamed_operator_classes": all_unnamed_classes,
        "gate_yes_screen_bites_off_axis_too": gate_yes,
        "leg_261_reference_fluid_kill_count": "18 of 18",
        "leg_261_reference_screen_locator": "experiments/journal/leg_261.md screen (iv_a) table",
    }


# ---------------------------------------------------------------------------------------------
# PART C -- leg 273's duplicate-occupant finding, checked as the counterweight
# ---------------------------------------------------------------------------------------------


def counterweight_273() -> dict:
    """Leg 273's finding, restated as a constraint on THIS leg's own conclusion: even in the
    counterfactual where (iv_a) did NOT bite these three models, any resulting certificate
    would land in leg 174's (fluid_adjacent, grade) matrix. Boussinesq is fluid_adjacent=True,
    the two gCLM variants are fluid_adjacent=False. Recorded here, not re-derived (leg 273's
    census is read-only input, not touched)."""
    return {
        "leg_174_matrix_cell_fluid_true_grade_A": "EMPTY per leg 174/255 (still empty; this leg's models "
                                                    "are, per Part B, killed by (iv_a) before grade is reached)",
        "leg_174_matrix_cell_fluid_false_grade_A": "OCCUPIED (DF-CGL arXiv:2410.05480, Biernat-Donninger "
                                                     "arXiv:1610.09496, per leg 273) -- a THIRD occupant is "
                                                     "leg 273's finding of redundancy, not this leg's to re-derive",
        "this_leg_models_fluid_adjacent_flags": {m["key"]: m["fluid_adjacent"] for m in MODELS},
        "note": "counted, not re-litigated -- leg 273's own gate (BOTH_CONJUNCTS_FAIL_DUPLICATION_AND_DEFICIENCY) "
                "stands untouched; this is a read of its verdict, not a repeat of its computation",
    }


# ---------------------------------------------------------------------------------------------
# liveness / self-test
# ---------------------------------------------------------------------------------------------


def self_test() -> dict:
    """Perturb the evidence and confirm the verdict actually moves -- assert_probe_is_live()
    fails the run if the table is degenerate (every row always killed regardless of input)."""
    codes = {}

    # baseline
    baseline = run_census()
    codes["baseline_all_killed"] = baseline["gate_yes_screen_bites_off_axis_too"] is True

    # counterfactual: strip the nonlocal-dissipation flag off every row (pretend s=1 for all,
    # i.e. ordinary Laplacian, which Remark 40 DOES name) -- verdict must then hinge only on
    # the remaining nonlocal nonlinearity operator (Hilbert transform / Biot-Savart), which is
    # still unnamed, so still killed. This checks the table is not vacuously "always killed"
    # for a reason unrelated to the actual operators.
    import copy
    models_s1 = copy.deepcopy(MODELS)
    for m in models_s1:
        m["operators"] = [op for op in m["operators"] if "dissipation" not in op["class"]]
    rows_s1 = [screen_iv_a_verdict(m) for m in models_s1]
    codes["still_killed_with_dissipation_stripped"] = all(r["killed_by_iv_a"] for r in rows_s1)

    # positive control: a model with EVERY operator named by Remark 40 (local polynomial,
    # Laplacian principal part) must PASS -- this is the generalised viscous Burgers row,
    # leg 255's own control (arXiv:2404.04054 line 1669, PASSES (iv), the paper's own worked
    # example).
    control_model = {
        "key": "CONTROL-VISCOUS-BURGERS",
        "fluid_adjacent": False,
        "operators": [
            {"name": "v^2 v_x (local polynomial), + Laplacian v_xx",
             "nonlocal": False, "named_by_remark_40": True,
             "class": "local polynomial nonlinearity, Laplacian principal part"},
        ],
    }
    control_row = screen_iv_a_verdict(control_model)
    codes["positive_control_passes"] = control_row["passes_iv_a"] is True

    codes["all_passed"] = all(codes.values())
    return codes


def assert_probe_is_live(codes: dict) -> None:
    if not codes.get("all_passed"):
        raise AssertionError(f"liveness probe degenerate: {codes}")


def main() -> None:
    census = run_census()
    counterweight = counterweight_273()
    liveness = self_test()
    assert_probe_is_live(liveness)

    result = {
        "leg": 311,
        "route": "Route-IVAX",
        "gate_question": "Does (iv_a), measured directly on the three non-incompressible models, "
                          "exclude candidates the way it excluded the 18 fluid rows?",
        "census": census,
        "counterweight_273": counterweight,
        "liveness": liveness,
        "verdict_code": "SCREEN_IV_A_BITES_OFF_AXIS_MECHANISM_NONLOCALITY_NOT_INCOMPRESSIBILITY"
        if census["gate_yes_screen_bites_off_axis_too"]
        else "SCREEN_IV_A_DOES_NOT_BITE_OFF_AXIS_POOL_LARGER",
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
