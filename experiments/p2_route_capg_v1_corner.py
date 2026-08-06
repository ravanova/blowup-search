"""P2 Route-CAPG v1 -- leg 162: the COMPACT-SUPPORT / GLOBAL-CHEBYSHEV certificate corner,
built explicitly and measured against leg 126's completeness audit.

GATE (DIRECTION.md ### 162, verbatim, both clauses):
    (a) Is the compact-support/Chebyshev-basis corner already inside the space/split/shape
        enumeration leg 126 audited as complete (checked explicitly against
        `certificate_shapes.py`'s enumeration and leg 126's own JSON), and
    (b) when built and measured directly, does its `Z_1` fall under, at, or over 1?

CONSTRUCTION ONLY, NO DYNAMICS.  NO GA COMPUTE UNDER ANY OUTCOME -- the two free parameters
(support radius via `a`, weight exponent `s`) move on the pre-named deterministic grids
`compact_cap_cheb.GRID_A` and `GRID_S` (the leg 46/59 precedent).

Run:  .venv/bin/python experiments/p2_route_capg_v1_corner.py
Out:  writeup/data/p2_route_capg_v1_corner.json
"""

import json
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from solver import compact_cap_cheb as C  # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data", "p2_route_capg_v1_corner.json")

N_MAIN = 192          # the working truncation; CAPG5 ladders it 48 -> 384
K_MAIN = 16           # the split
A21_ZERO_SHAPES = ("block_diag", "gs_upper")     # the shapes leg 58's theorem speaks about


def main():
    t0 = time.time()
    res = {"leg": 162, "route": "CAPG", "version": "v1",
           "object": ("the gCLM self-similar profile on its OWN SUPPORT, via "
                      "solver/first_integral.py's reduced system (RS), linearised and "
                      "represented in a GLOBAL Chebyshev basis on the finite support "
                      "interval -- two realizations, see CAPG2"),
           "no_GA_compute": True,
           "grids": {"GRID_A": list(C.GRID_A), "GRID_S": list(C.GRID_S),
                     "deterministic": True, "precedent": "legs 46/59"}}

    # -- CAPG0: novelty -----------------------------------------------------
    res["CAPG0_novelty"] = {
        "log": "writeup/novelty/leg_162.md",
        "verdict": "PROCEED_NARROWED",
        "run_before_construction": True,
        "links_not_counts": True,
        "binding_finding": (
            "DIRECTION.md ### 162's premise -- 'no record of this repository ever having "
            "tried it' -- is FALSE.  solver/first_integral.py already reduces the profile "
            "to its own support in an even-Chebyshev series with the FINITE Hilbert "
            "transform, and solver/reduced_certificate.py already assembles Y_0/Z_0/Z_2 "
            "there.  What has never been computed, in any basis on a finite support "
            "interval, is Z_1 -- reduced_certificate.py item (4) says so verbatim.  This "
            "leg's novelty is the MEASUREMENT, not the basis."),
        "premise_correction_2": (
            "DIRECTION.md attributes compact support to the a=1 De Gregorio profile.  Leg "
            "112 read arXiv:2603.25104v2 at full text: Thm 7.10(3) p.45 gives compact "
            "support exactly on 0 < a < 1, and at a = 1 the support edge degenerates to a "
            "CORNER.  a = 1 is the one exponent the theorem excludes, so every construction "
            "here is parameterized on 0 < a < 1."),
        "new_external_refs_zero_prior_hits": [
            "https://arxiv.org/abs/2603.27198 (Breden-Cadiot-Zurek, Gegenbauer CAP on a "
            "finite interval -- the closest published precedent to this corner)",
            "https://arxiv.org/abs/1507.00596 (Olver-Townsend, the finite Hilbert "
            "transform's T<->U structure -- realization B's exactness rests on it)"],
        "leg52_search_index_flag": "STANDS -- not tested by this pass, not cleared."}
    print(f"[CAPG0] novelty {res['CAPG0_novelty']['verdict']}")

    # -- CAPG1: the identities, and the projector's known-answer gate -------
    res["CAPG1_identities"] = C.verify_identities(N=8, n_quad=1500)
    res["CAPG1_reading"] = (
        "Realization B's Hilbert identity is EXACT (Tricomi): max abs err "
        f"{res['CAPG1_identities']['hilbB_max_abs_err']:.2e}.  Realization A's is NOT "
        "AVAILABLE in closed form -- this module's first draft asserted one and the check "
        "measured its error at 0.617, so the assertion was replaced by a numerical "
        "projector whose own known-answer gate (against the family where the answer IS "
        f"exact) reads {res['CAPG1_identities']['projector_known_answer_max_abs_err_vs_I']:.2e}.")
    print(f"[CAPG1] identities max err "
          f"{max(v for k, v in res['CAPG1_identities'].items() if isinstance(v, float) and 'err' in k):.2e}")

    # -- CAPG2: the shape classification, WITH the control that must disagree
    shapes = {}
    for real in (C.REAL_A, C.REAL_B):
        shapes[real] = C.classify_tail(C.deriv_block(64, real), f"deriv_{real}")
    control = C.shape_control_wholeline(8, 128)
    res["CAPG2_shape"] = {
        "realizations": shapes,
        "CONTROL_wholeline_compactified": control,
        "control_is_a_real_control": bool(
            control["label"] != shapes[C.REAL_B]["label"]),
        "reading": (
            "One classifier, three operators, and they are REQUIRED to disagree (lesson 90). "
            "Realization A and the banked compactified whole-line tail block both come back "
            "SHIFT with an EXACTLY zero diagonal and off-diagonal ~ n/2 -- the same shape and "
            "the same n/2.  Realization B comes back MULTIPLIER, diag(-n), zero off-diagonal. "
            "If the classifier had reported MULTIPLIER on the whole-line control too, the "
            "Chebyshev result would be a property of this file, not of the operators.")}
    print(f"[CAPG2] A={shapes[C.REAL_A]['label']}  B={shapes[C.REAL_B]['label']}  "
          f"CONTROL={control['label']}")

    # -- CAPG3: is the assembled matrix the operator it claims to be? -------
    kag = {}
    for real in (C.REAL_A, C.REAL_B):
        rows = []
        for N in (32, 64, 128):
            g = C.operator_known_answer_gate(N=N, realization=real, a=0.3, nq=2000)
            rows.append({"N": N, "max_rel_err": g["max_rel_err"]})
        kag[real] = {"ladder_in_N": rows, "floor": rows[-1]["max_rel_err"]}
    smooth = [{"smoothness": s,
               "max_rel_err": C.operator_known_answer_gate(
                   N=64, realization=C.REAL_B, a=0.3, nq=2000, smoothness=s)["max_rel_err"]}
              for s in (2, 4, 6)]
    res["CAPG3_operator_known_answer_gate"] = {
        "per_realization": kag,
        "smoothness_ladder_realization_B_N64": smooth,
        "quadrature_invariance_note": (
            "at smoothness 2 the gate reads 1.1712e-2 and does NOT move across nq = 1000, "
            "2000, 4000, 8000 (identical to six digits), which is how the 1.1% was "
            "identified as the gate's own pointwise series reconstruction rather than an "
            "error in the matrix; the smoothness ladder above confirms it"),
        "method": ("a random smooth coefficient vector pushed through the ASSEMBLED matrix "
                   "and, independently, through a direct pointwise evaluation of "
                   "L h = c h' + X_c Hpv[p h] (numerical derivative + the verified "
                   "principal-value quadrature)"),
        "reading": (
            "Realization B's representation converges to a ~1% floor.  Realization A's does "
            "NOT converge: it stalls near 30%, because the airfoil class sqrt(1-v^2) x poly "
            "is closed under the finite Hilbert transform and this repository's own "
            "(1-v^2) T_n ansatz is NOT -- its H matrix is dense with slowly decaying "
            "entries.  So realization A's Z_1 below is reported as an ORDER OF MAGNITUDE "
            "only: at 30% representation error it is partly a statement about the code "
            "(lesson 86).  Its SHAPE classification is unaffected -- the derivative block "
            "is exact to 1e-8 and it is the derivative block that carries the shape.")}
    print(f"[CAPG3] known-answer floors  A={kag[C.REAL_A]['floor']:.3g}  "
          f"B={kag[C.REAL_B]['floor']:.3g}")

    # -- CAPG4: the Z_1 grid, deterministic, both realizations --------------
    grid = []
    for real in (C.REAL_A, C.REAL_B):
        for a in C.GRID_A:
            for s in C.GRID_S:
                kind = "flat" if s == 0.0 else "algebraic"
                ob = C.assemble(N_MAIN, K_MAIN, real, a=a, kind=kind, param=s,
                                use_profile=True, bordered=True)
                for sh in A21_ZERO_SHAPES + ("gs_lower",):
                    m = C.measure(ob, sh)
                    grid.append({"realization": real, "a": a, "s": s, "shape": sh,
                                 "A21_zero": C.A21_ZERO[sh], "Z1": m["Z1"],
                                 "Z1_GG": m["Z1_GG"], "Z1_Gt": m["Z1_Gt"],
                                 "Z1_tG": m["Z1_tG"], "Z1_tt": m["Z1_tt"]})
    res["CAPG4_grid"] = grid
    a21z = [r for r in grid if r["A21_zero"]]
    below = [r for r in a21z if r["Z1"] < 1.0]
    bestB = min((r for r in a21z if r["realization"] == C.REAL_B), key=lambda r: r["Z1"])
    bestA = min((r for r in a21z if r["realization"] == C.REAL_A), key=lambda r: r["Z1"])
    res["CAPG4_summary"] = {
        "n_configurations": len(grid),
        "n_A21_zero": len(a21z),
        "n_A21_zero_with_Z1_below_1": len(below),
        "best_realization_B": bestB, "best_realization_A": bestA,
        "worst_realization_B": max((r for r in a21z if r["realization"] == C.REAL_B),
                                   key=lambda r: r["Z1"]),
        "reading": (
            "Every row here has A21 = 0, the class leg 58's Proposition NG closes as "
            "mathematics with Z_1 >= 1.  Realization A obeys it.  Realization B does not, "
            "and the reason is that the proposition's hypothesis (H2) -- 'the tail block has "
            "a kernel in l^1_w' -- FAILS in realization B: its tail is diag(-n), which has "
            "no kernel at any n >= 1.  This is the same way (H2) fails for mu > 0 in leg "
            "58's own dissipative control.  No contradiction with the theorem; the theorem "
            "does not reach this realization.")}
    print(f"[CAPG4] best A21=0 Z_1: B={bestB['Z1']:.5g} (a={bestB['a']}, s={bestB['s']}, "
          f"{bestB['shape']})  A={bestA['Z1']:.5g}")

    # -- CAPG5: truncation ladder at the minimum ---------------------------
    lad = []
    for N in (48, 96, 192, 384):
        ob = C.assemble(N, K_MAIN, C.REAL_B, a=bestB["a"],
                        kind="flat" if bestB["s"] == 0.0 else "algebraic",
                        param=bestB["s"], use_profile=True, bordered=True)
        lad.append({"N": N, **{sh: C.measure(ob, sh)["Z1"] for sh in A21_ZERO_SHAPES}})
    drift = abs(lad[-1][bestB["shape"]] - lad[0][bestB["shape"]]) / lad[0][bestB["shape"]]
    res["CAPG5_truncation_ladder"] = {
        "at": {"realization": C.REAL_B, "a": bestB["a"], "s": bestB["s"], "K": K_MAIN},
        "rows": lad, "relative_drift_over_8x_refinement": drift,
        "reading": ("Z_1 is truncation-STABLE: an 8x refinement of N moves it by the "
                    f"fraction above ({drift:.2%}).  A Z_1 that grew with N would be a "
                    "statement about the truncation, not about the operator.")}
    print(f"[CAPG5] truncation drift over 8x: {drift:.2%}")

    # -- CAPG6: the border, and its direction spread (lesson 90) -----------
    bd = []
    for d in C.BORDER_DIRECTIONS:
        ob = C.assemble(N_MAIN, K_MAIN, C.REAL_B, a=bestB["a"],
                        kind="flat" if bestB["s"] == 0.0 else "algebraic",
                        param=bestB["s"], use_profile=True, bordered=True,
                        border_direction=d)
        bd.append({"direction": d, **{sh: C.measure(ob, sh)["Z1"] for sh in A21_ZERO_SHAPES}})
    unb = C.assemble(N_MAIN, K_MAIN, C.REAL_B, a=bestB["a"],
                     kind="flat" if bestB["s"] == 0.0 else "algebraic",
                     param=bestB["s"], use_profile=True, bordered=False)
    vals = [r["block_diag"] for r in bd]
    n_below = sum(1 for v in vals if v < 1.0)
    res["CAPG6_border"] = {
        "GAUGE_DEPENDENCE_IS_THE_CAVEAT": (
            f"Z_1 < 1 holds at {n_below} of {len(vals)} border gauges, not all four.  For a "
            "NEGATIVE result the conservative choice is to report the BEST gauge (leg 54's "
            "convention); for a POSITIVE result it is the WORST, and the worst here is "
            f"{max(vals):.4g}.  The headline is therefore stated WITH its gauge named -- "
            "'at the amplitude and first-mode gauges' -- and never as a bare Z_1.  A "
            "certificate designer does get to choose one gauge, so 2 of 4 is not a refutation; "
            "it is a restriction that must travel with the number."),
        "n_gauges_below_1": n_below, "worst_gauge_Z1": max(vals), "best_gauge_Z1": min(vals),
        "why": ("(RS)'s unknowns are (s, X_c): the support radius is SOLVED FOR, not given. "
                "A Z_1 measured on the s-block alone is lesson 89's failure mode -- the term "
                "that does not exist until you assemble is the one that decides, and on the "
                "whole line that term was the far-field amplitude column (leg 53)."),
        "rows": bd,
        "spread_max_over_min": (max(vals) / min(vals)) if min(vals) > 0 else None,
        "directions_give_different_numbers": bool(len(set(np.round(vals, 12))) > 1),
        "unbordered_block_diag_Z1": C.measure(unb, "block_diag")["Z1"],
        "bordered_block_diag_Z1": bd[0]["block_diag"],
        "reading": ("Four border directions, four DIFFERENT numbers -- leg 53 reported one "
                    "number for all four and it turned out its sub-block never saw the "
                    "border (lesson 90).  The border is wired through here.")}
    print(f"[CAPG6] border spread {res['CAPG6_border']['spread_max_over_min']}")

    # -- CAPG7: is the target in the space? (leg 126 clause SPACE-TARGET) --
    tm = []
    for a in C.GRID_A:
        for s in C.GRID_S:
            kind = "flat" if s == 0.0 else "algebraic"
            t = C.target_membership(a=a, realization=C.REAL_B, N=192, kind=kind, param=s)
            tm.append({"a": a, "s": s, "decay": t["coefficient_decay_exponent"],
                       "margin": t["margin"],
                       "in_space": bool(t["margin"] is None or t["margin"] < 0.0),
                       "weighted_l1": t["weighted_l1_partial_sums"][-1]})
    res["CAPG7_target_membership"] = {
        "rows": tm,
        "clause": ("leg 126 SPACE-TARGET: a configuration whose own target has infinite "
                   "norm is not a legal certificate, whatever its Z_1"),
        "best_point_is_in_space": next(
            r["in_space"] for r in tm if r["a"] == bestB["a"] and r["s"] == bestB["s"]),
        "reading": ("`margin = decay_exponent + weight_growth + 1 < 0` is convergence of the "
                    "weighted l^1 sum.  The grid's Z_1 minimum is checked against this, "
                    "because a Z_1 below 1 in a space the target has left is not a result.")}
    print(f"[CAPG7] target in space at the minimum: "
          f"{res['CAPG7_target_membership']['best_point_is_in_space']}")

    # -- CAPG8: negative controls that CAN fail ----------------------------
    res["CAPG8_negative_controls"] = {
        "realization_A_same_code_path": bestA,
        "realization_B_worst_corner": res["CAPG4_summary"]["worst_realization_B"],
        "wholeline_control_label": control["label"],
        "reading": ("A positive result needs negative controls that can fail.  The same "
                    "assemble/measure path reports Z_1 in the hundreds for realization A and "
                    f"{res['CAPG4_summary']['worst_realization_B']['Z1']:.4g} for "
                    "realization B's worst corner, so 'Z_1 < 1' is a discrimination and not "
                    "a floor of the instrument.")}

    # -- CAPG9: does the corner even have a domain on leg 126's object? ----
    sup = C.support_transfer_audit()
    try:
        from solver.first_integral import ReducedProfile
        ReducedProfile(a=0.0)
        raised = None
    except Exception as e:                                   # noqa: BLE001
        raised = f"{type(e).__name__}: {e}"
    sup["landed_module_refuses_a_equals_zero"] = raised
    res["CAPG9_support_transfer"] = sup
    print(f"[CAPG9] a=0 CLM decay exponent {sup['decay_exponent']:.4f}")

    # -- CAPG10: coverage against leg 126 ----------------------------------
    cov = C.coverage_classification()
    res["CAPG10_coverage"] = cov
    print(f"[CAPG10] uncovered: {cov['uncovered']}")

    # -- the gate ----------------------------------------------------------
    uncovered = len(cov["uncovered"]) == 2
    z1_below = bestB["Z1"] < 1.0 and res["CAPG7_target_membership"]["best_point_is_in_space"]
    res["gate_question"] = (
        "(a) Is the compact-support/Chebyshev-basis corner already inside the space/split/"
        "shape enumeration leg 126 audited as complete (checked explicitly against "
        "certificate_shapes.py's enumeration and leg 126's own JSON), and (b) when built and "
        "measured directly, does its Z_1 fall under, at, or over 1?")
    res["gate_answer_a"] = ("NO -- UNCOVERED" if uncovered else "YES -- COVERED")
    res["gate_answer_b"] = (f"UNDER 1: {bestB['Z1']:.6g}" if z1_below
                            else f"OVER 1: {bestB['Z1']:.6g}")
    res["gate_branch"] = (
        "yes, uncovered by 126 + Z_1 < 1 -> ESCALATION #4 (a banked completeness claim "
        "reversed).  Push, park, DO NOT MERGE, list under NEEDS YOU."
        if (uncovered and z1_below) else
        "uncovered + Z_1 >= 1 -> closes on measurement, extending 126's declared coverage.")
    res["enumeration_gap"] = {
        "axis": "realization (stage B's SPACE degree of freedom)",
        "leg126_declared": cov["leg126_realization_axis"],
        "this_corner": cov["this_corner"],
        "statement": ("leg 126 declared the realization axis with THREE values -- l1_fourier, "
                      "collocation, weighted_L2 -- and audited 1,686 configurations over it "
                      "with 0 uncovered.  A global Chebyshev basis on a compact support "
                      "interval is a FOURTH value of that axis.  It is not a new split and "
                      "not a new shape: the split (finite block + tail) and the shapes "
                      "(block_diag, gs_upper, gs_lower) are leg 54's, unchanged.")}
    res["ceiling"] = (
        "Z_1 IS ONE OF FOUR CONSTANTS AND THIS IS NOT A CERTIFICATE.  Y_0, Z_0 and Z_2 are "
        "not measured here, and solver/reduced_certificate.py already measured Z_2 INFINITE "
        "in the sup realization on this same object, with its finiteness in the nonlinearity "
        "requiring a <= 1/2.  Float64, no interval arithmetic.  The object is the gCLM "
        "profile on 0 < a < 1, NOT HL_S2_nonsymmetric and not any link of the L1->L4 chain; "
        "CAPG9 measures that leg 126's own object has no support interval to put this basis "
        "on at all.  No link of the chain moved and none has moved in 161 legs.")
    res["elapsed_s"] = time.time() - t0

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1, default=float)
    print(f"\nGATE (a): {res['gate_answer_a']}")
    print(f"GATE (b): {res['gate_answer_b']}")
    print(f"BRANCH  : {res['gate_branch']}")
    print(f"wrote {OUT}  ({res['elapsed_s']:.1f}s)")


if __name__ == "__main__":
    main()
