"""Leg 178 -- ROUTE-WES: does a DIFFERENT SPACE shift the weighted-energy zero-width window?

Runner for the gate in `DIRECTION.md` leg 178, verbatim:

    "For at least one pre-named alternative weighted-energy construction (different from
     leg 111's), is the measured coercivity gap positive and grid-stable across two
     refinements, outside the gamma>3-needs/gamma<3-exists coincidence?"

Everything this driver sweeps -- the four constraint classes, the eleven weights, the
membership probes, the five-clause pass predicate, the four controls and the seven
predictions -- was PRE-NAMED in `writeup/novelty/leg_178.md`, committed at `0ed6bde`
BEFORE `solver/energy_coercivity.py` was appended to and before any number existed.  This
file chooses nothing.  Read that log first; this runner only executes it.

WHAT IS NOT CLAIMABLE, AND THE DRIVER SAYS SO IN ITS OWN OUTPUT
--------------------------------------------------------------
The construction is Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop. 2.1 (`f` odd,
`f'(0) = Hf(0) = 0`, weight `(1+y^2)^2/y^4`, conclusion `<= -1/2` at `a = 0`, on the CLM
model by EGM's own sec 1).  The frame is Xu arXiv:2607.19762 sec 3.1's realization
dichotomy.  Neither is this repository's, and the JSON carries that disclaimer in a field
so it travels with the numbers.  What is measured here is the MEASUREMENT: leg 111's gate
re-asked on a trial space whose vanishing order is not 1.

Run: `.venv/bin/python experiments/p2_route_wes_v1_space.py`
Writes: `writeup/data/p2_route_wes_v1_space.json`
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.energy_coercivity import (  # noqa: E402
    KNOWN_ANSWER_CEILING,
    WES_CONSTRAINT_CLASSES,
    WES_PROBE_VECTORS,
    WES_WEIGHT_FAMILY,
    admissibility,
    coercivity_gap,
    damping_factor_at_origin,
    graded_quadrature,
    weight_values,
    wes_admissibility,
    wes_coercivity_gap,
    wes_coercivity_gap_exact,
    wes_constrained_basis,
    wes_constraint_rows,
    wes_damping_factor,
    wes_form_matrices,
    wes_point_mode_intersection,
    wes_trial_projector,
    wes_vanishing_order,
    wes_weight_values,
)

OUT = ROOT / "writeup" / "data" / "p2_route_wes_v1_space.json"

# ---------------------------------------------------------------------------
# PRE-COMMITTED, from writeup/novelty/leg_178.md sec 7.  Not edited after a run.
# ---------------------------------------------------------------------------
N_LADDER = (32, 64, 128, 256)
GRADE_DEPTHS = (12, 24, 48, 96)
N_QUAD_CHECK = 128
REL_STABILITY_TOL = 0.05        # leg 111's own tolerance, unchanged
QUAD_SPREAD_TOL = 1e-3          # the disqualifier that killed leg 111's A3 at 2.665e-01
ADMISS_TOL = 1e-6
CEILING_SLACK = 1e-9
MU_LADDER = (0.0, 0.5, 1.0, 1.5, 2.0)

# Leg 111's banked modulated gaps at n = 256 (experiments/journal/leg_111.md).
# Control C1: the appended code must not have moved them.
LEG111_BANKED_N256 = {
    ("A", 0.0): -1.499886,
    ("A", 2.0): -0.499924,
    ("B", 0.0): -1.499924,
    ("B", 2.0): -0.499962,
}
C1_TOL = 1e-5


def rel_spread(xs):
    xs = [float(x) for x in xs]
    lo, hi = min(xs), max(xs)
    denom = max(abs(sum(xs) / len(xs)), 1e-300)
    return (hi - lo) / denom


def main():
    out = {
        "leg": 178,
        "route": "ROUTE-WES",
        "gate": ("For at least one pre-named alternative weighted-energy construction "
                 "(different from leg 111's), is the measured coercivity gap positive and "
                 "grid-stable across two refinements, outside the gamma>3-needs/"
                 "gamma<3-exists coincidence?"),
        "not_claimable": (
            "The construction is NOT this repository's. The constrained trial space and "
            "the weight are Elgindi-Ghoul-Masmoudi arXiv:1906.05811 Prop. 2.1 (f odd, "
            "f'(0) = Hf(0) = 0, phi = (1+y^2)^2/y^4, conclusion <= -1/2 at a = 0, on the "
            "CLM model by EGM's own sec 1); the realization dichotomy that frames it is Xu "
            "arXiv:2607.19762 sec 3.1 Prop. 2. Leg 178 claims only the MEASUREMENT, and "
            "prices nothing: EGM buy the origin conditions with two free modulation "
            "parameters, so a gap on a constrained trial space is NOT a certificate."),
        "ceiling": (
            "Plain float64, nothing interval-enclosed. Object is the a = 0 CLM "
            "linearisation (clause S7): a gap measured here bounds HL_S2_nonsymmetric's "
            "difficulty FROM BELOW, never above. No stage claimed, no ban lifted, no link "
            "of the L1 -> L4 chain moved."),
        "pre_committed": {
            "novelty_log": "writeup/novelty/leg_178.md (commit 0ed6bde, before any compute)",
            "n_ladder": list(N_LADDER),
            "grade_depths": list(GRADE_DEPTHS),
            "rel_stability_tol": REL_STABILITY_TOL,
            "quad_spread_tol": QUAD_SPREAD_TOL,
            "admiss_tol": ADMISS_TOL,
            "known_answer_ceiling": KNOWN_ANSWER_CEILING,
            "constraint_classes": [
                {"name": c[0], "constraints": list(c[1]),
                 "declared_vanishing_order": c[2], "gamma_upper": c[3]}
                for c in WES_CONSTRAINT_CLASSES],
            "weights": [{"name": w[0], "family": w[1], "gamma": w[2]}
                        for w in WES_WEIGHT_FAMILY],
            "probes": {k: list(v) for k, v in WES_PROBE_VECTORS.items()},
        },
    }

    # ---------------------------------------------------------------- C1
    # Leg 111's OWN function, untouched, must reproduce its OWN banked numbers.
    print("== control C1: leg 111's banked gaps reproduce through the untouched path")
    c1 = []
    for (fam, gam), banked in sorted(LEG111_BANKED_N256.items()):
        got = coercivity_gap(256, fam, gam, modulate=True)["gap"]
        c1.append({"family": fam, "gamma": gam, "banked": banked, "measured": got,
                   "abs_diff": abs(got - banked), "ok": abs(got - banked) <= C1_TOL})
        print(f"   {fam}{gam:g}: banked {banked:+.6f}  measured {got:+.9f}  "
              f"diff {abs(got - banked):.2e}")
    out["control_C1_reproduction"] = {
        "tol": C1_TOL, "rows": c1, "all_ok": all(r["ok"] for r in c1),
        "note": ("append-only: leg 111's coercivity_gap/weight_values/admissibility are "
                 "byte-identical, so a failure here would mean the append was not "
                 "append-only in effect and the whole run is void")}

    # ---------------------------------------------------------------- P0
    # Is EGM's transported weight literally leg 111's family B at gamma = 4?
    print("== P0: is phi^E / phi^B4 constant?  (predicted: yes, constant 32)")
    th, _ = graded_quadrature(n_unif=128, n_grade=24, order=12)
    interior = (th > 1e-8) & (th < math.pi - 1e-8)
    ratio = wes_weight_values(th[interior], "E", 4.0) / weight_values(th[interior], "B", 4.0)
    p0 = {"ratio_min": float(ratio.min()), "ratio_max": float(ratio.max()),
          "ratio_mean": float(ratio.mean()), "rel_spread": float(rel_spread(ratio)),
          "predicted_constant": 32.0,
          "abs_diff_from_32": float(np.max(np.abs(ratio - 32.0))),
          "n_points": int(interior.sum())}
    p0["holds"] = bool(p0["rel_spread"] < 1e-12 and p0["abs_diff_from_32"] < 1e-9)
    out["P0_egm_weight_is_family_B4"] = p0
    print(f"   ratio in [{p0['ratio_min']:.15g}, {p0['ratio_max']:.15g}], "
          f"rel spread {p0['rel_spread']:.3e}, |ratio - 32| <= {p0['abs_diff_from_32']:.3e}")

    # Damping factor: is it identically -1/2 for B4 and for E?
    dfac = {}
    for name, fam, gam in WES_WEIGHT_FAMILY:
        D = wes_damping_factor(th[interior], fam, gam)
        dfac[name] = {"family": fam, "gamma": gam,
                      "D_at_origin": float(damping_factor_at_origin(fam, gam))
                      if fam in ("A", "B") else
                      float(wes_damping_factor(np.array([1e-12]), fam, gam)[0]),
                      "D_min": float(D.min()), "D_max": float(D.max()),
                      "D_sup": float(D.max()),
                      "max_dev_from_minus_half": float(np.max(np.abs(D + 0.5)))}
    out["damping_factor"] = {
        "rows": dfac,
        "note": ("D_phi is the ENTIRE local part of the form. Damping at the origin needs "
                 "D_phi(0) < 0, i.e. gamma > 3 in family A/B. B4_egm and E_egm are the "
                 "members for which D_phi is CONSTANT -1/2 over the whole interval -- "
                 "written un-simplified in the module so it could report otherwise.")}
    print("   D_phi max deviation from -1/2:  B4_egm "
          f"{dfac['B4_egm']['max_dev_from_minus_half']:.3e}   E_egm "
          f"{dfac['E_egm']['max_dev_from_minus_half']:.3e}   A4_chen_hou "
          f"{dfac['A4_chen_hou']['max_dev_from_minus_half']:.3e}")

    # ------------------------------------------------- vanishing order + P5
    print("== vanishing order (measured, not asserted) and P5 point-mode intersection")
    orders, inters = {}, {}
    for cname, _, _, _ in WES_CONSTRAINT_CLASSES:
        orders[cname] = wes_vanishing_order(cname)
        inters[cname] = wes_point_mode_intersection(cname)
        print(f"   {cname:20s} measured p = {orders[cname]['measured_order']:.6f} "
              f"(declared {orders[cname]['declared_order']:.0f})  "
              f"h'(0) = {orders[cname]['h_prime_at_0']:+.0f}  "
              f"(Hh)(0) = {orders[cname]['H_h_at_0']:+.0f}  "
              f"point-mode dim = {inters[cname]['intersection_dim']}")
    out["vanishing_order"] = orders
    out["P5_point_mode_intersection"] = {
        "rows": inters,
        "prediction": ("T2_egm intersects span{sin th, sin 2th} in dimension 0, i.e. the "
                       "two origin constraints already remove BOTH of Xu's published point "
                       "modes, so modulate=True and modulate=False must agree on T2. This "
                       "is leg 178's own arithmetic, NOT attributed to Xu or EGM.")}

    # ------------------------------------------------------ admissibility
    print("== admissibility: is the CONSTRAINED space in L^2_phi?")
    adm = {}
    for cname, _, _, _ in WES_CONSTRAINT_CLASSES:
        for wname, fam, gam in WES_WEIGHT_FAMILY:
            a = wes_admissibility(cname, fam, gam)
            a["converged"] = bool(abs(a["ratio"] - 1.0) <= ADMISS_TOL
                                  and a["exponent_margin"] > 0)
            adm[f"{cname}|{wname}"] = a
    out["admissibility"] = adm
    for cname, _, _, _ in WES_CONSTRAINT_CLASSES:
        a4 = adm[f"{cname}|A4_chen_hou"]
        print(f"   {cname:20s} gamma=4: margin {a4['exponent_margin']:+.1f}  "
              f"probe ratio {a4['ratio']:.6e}  gram-top ratio {a4['gram_top_ratio']:.6e}  "
              f"converged={a4['converged']}")
    # leg 111's own instrument on its own probe, for the side-by-side
    out["leg111_admissibility_A4"] = admissibility("A", 4.0)

    # ------------------------------------------------ THE INSTRUMENT FINDING
    # Assemble-then-project computes the constrained form as a cancellation
    # between DIVERGENT Gram entries, and the SVD null-space basis leaks ~1e-16
    # into the very direction it is meant to exclude.  The exactly-constrained
    # integer basis has residual 0.0 and contracts pointwise.  Both are run at
    # gamma = 4 so the size of the artifact is a measured magnitude, not a claim.
    print("== instrument: exactly-constrained basis vs assemble-then-project")
    instr = {}
    for cname in ("T1_dprime", "T2_egm"):
        R = wes_constraint_rows(32, cname)
        Vx, Qs = wes_constrained_basis(32, cname), wes_trial_projector(32, cname)
        proj = wes_coercivity_gap(32, cname, "B", 4.0, modulate=False)["gap"]
        exact = wes_coercivity_gap_exact(32, cname, "B", 4.0)["gap"]
        instr[cname] = {
            "exact_basis_constraint_residual": float(np.max(np.abs(R @ Vx))),
            "svd_basis_constraint_residual": float(np.max(np.abs(R @ Qs))),
            "gap_assemble_then_project": proj, "gap_exact_basis": exact,
            "abs_diff": abs(proj - exact)}
        print(f"   {cname:18s} B4 n=32: project {proj:+.6f}  exact {exact:+.6f}  "
              f"diff {abs(proj - exact):.3e}   residual exact "
              f"{instr[cname]['exact_basis_constraint_residual']:.1e} vs svd "
              f"{instr[cname]['svd_basis_constraint_residual']:.2e}")
    out["instrument_exact_vs_projected"] = {
        "rows": instr,
        "note": ("At gamma > 3 the UNCONSTRAINED Gram's own entries are divergent "
                 "(they grow by 1.68e+07 per grading refinement), so restricting AFTER "
                 "assembly cancels divergent numbers and a 1e-16 basis leak is amplified "
                 "by that divergence. Lesson 86. Every gate-answering number below is "
                 "from the exactly-constrained basis, whose constraint residual is "
                 "EXACTLY 0.0.")}

    # -------------------------------------------------------- the gap grid
    print("== the gap ladder on the exactly-constrained basis (mu = 0)")
    gaps = {}
    classes = [c[0] for c in WES_CONSTRAINT_CLASSES]
    for wname, fam, gam in WES_WEIGHT_FAMILY:
        for cname in classes:
            row = [wes_coercivity_gap_exact(n, cname, fam, gam) for n in N_LADDER]
            gaps[f"{cname}|{wname}"] = row
            g = [r["gap"] for r in row]
            print(f"   {cname:20s} {wname:12s} " + "  ".join(f"{x:+.6f}" for x in g)
                  + f"   contam {row[-1]['contamination']:.1e}")
    out["gap_ladder"] = gaps

    # ------------------------------------------- quadrature-depth stability
    print(f"== quadrature-depth stability at n = {N_QUAD_CHECK} "
          f"(leg 111's A3 disqualifier: 2.665e-01)")
    quad = {}
    for wname, fam, gam in WES_WEIGHT_FAMILY:
        for cname in classes:
            rows = [wes_coercivity_gap_exact(N_QUAD_CHECK, cname, fam, gam, n_grade=ng)
                    for ng in GRADE_DEPTHS]
            vals = [r["gap"] for r in rows]
            quad[f"{cname}|{wname}"] = {
                "depths": list(GRADE_DEPTHS), "gaps": vals,
                "contamination": [r["contamination"] for r in rows],
                "rel_spread": rel_spread(vals)}
    out["quadrature_stability"] = quad
    for cname in ("T2_egm", "T3_hilbert_only"):
        r = quad[f"{cname}|B4_egm"]
        print(f"   {cname:20s} B4_egm  rel spread {r['rel_spread']:.4e}  "
              f"contam {max(r['contamination']):.1e}")

    # ------------------------------------------------------ the C3 control
    print("== control C3: mu > 0 must flip the sign ON THE APPENDED PATH")
    c3 = {}
    for cname in ("T0_unconstrained", "T2_egm"):
        vals = [wes_coercivity_gap_exact(128, cname, "A", 0.0, mu=mu)["gap"]
                for mu in MU_LADDER]
        c3[cname] = {"mu": list(MU_LADDER), "gaps": vals,
                     "sign_flips": bool(min(vals) < 0 < max(vals)),
                     "monotone": bool(all(vals[i + 1] > vals[i]
                                          for i in range(len(vals) - 1)))}
        print(f"   {cname:20s} A0_flat  " + "  ".join(f"{v:+.5f}" for v in vals)
              + f"   sign flips: {c3[cname]['sign_flips']}")
    out["control_C3_dissipation"] = {
        "rows": c3,
        "note": ("mu > 0 is a DIFFERENT OPERATOR, not a different realization (leg 165's "
                 "C3 / this leg's C4): NO mu > 0 row answers the gate. Every gate-answering "
                 "row below is at mu = 0 exactly.")}

    # ------------------------------------------- the five-clause predicate
    print("== the pre-committed five-clause pass predicate")
    verdicts = {}
    for cname, _, _, _ in WES_CONSTRAINT_CLASSES:
        for wname, fam, gam in WES_WEIGHT_FAMILY:
            key = f"{cname}|{wname}"
            row = gaps[key]
            g = [r["gap"] for r in row]
            a = adm[key]
            steps = []
            for i in (len(g) - 2, len(g) - 1):
                prev = g[i - 1]
                steps.append(abs(g[i] - prev) / max(abs(prev), 1e-300))
            c_pos = bool(all(x > 0 for x in g))
            c_grid = bool(all(s <= REL_STABILITY_TOL for s in steps))
            c_quad = bool(quad[key]["rel_spread"] <= QUAD_SPREAD_TOL)
            c_adm = bool(a["converged"])
            c_ceil = bool(g[-1] <= KNOWN_ANSWER_CEILING + CEILING_SLACK)
            verdicts[key] = {
                "class": cname, "weight": wname, "family": fam, "gamma": gam,
                "gap_n256": g[-1], "gap_ladder": g,
                "rel_steps_last_two": steps,
                "quad_rel_spread": quad[key]["rel_spread"],
                "admiss_ratio": a["ratio"], "exponent_margin": a["exponent_margin"],
                "clause_positive": c_pos, "clause_grid_stable": c_grid,
                "clause_quad_stable": c_quad, "clause_admissible": c_adm,
                "clause_under_ceiling": c_ceil,
                "contamination_n256": row[-1]["contamination"],
                "max_contamination_quad_sweep": max(quad[key]["contamination"]),
                "PASS": bool(c_pos and c_grid and c_quad and c_adm and c_ceil),
                "local_gap_n256": row[-1]["local_gap"],
                "nonlocal_gap_n256": row[-1]["nonlocal_gap"],
                "byparts_rel_residual_n256": row[-1]["byparts_rel_residual"],
                "cond_G_n256": row[-1]["cond_G"], "dropped_n256": row[-1]["dropped"],
            }
    out["verdicts"] = verdicts
    passing = sorted(k for k, v in verdicts.items() if v["PASS"])
    print(f"   PASSING: {len(passing)} of {len(verdicts)}")
    for k in passing:
        v = verdicts[k]
        print(f"     {k:34s} gap {v['gap_n256']:+.9f}  local {v['local_gap_n256']:+.6f}  "
              f"nonlocal {v['nonlocal_gap_n256']:+.6f}")

    # ------------------------------------------------------ the C2 control
    c2_rows = {k: v for k, v in verdicts.items() if v["class"] == "T3_hilbert_only"}
    c2_pass = sorted(k for k, v in c2_rows.items() if v["PASS"] and v["gamma"] > 3.0)
    out["control_C2_falsification"] = {
        "rows_passing_above_gamma_3": c2_pass,
        "fires_as_designed": bool(not c2_pass),
        "note": ("T3_hilbert_only removes a direction exactly as T1/T2 do but does NOT "
                 "change the vanishing order, so its window stays (3,3) and it must not "
                 "pass at gamma > 3. If it did, the instrument would be measuring "
                 "dimension reduction, not the space, and this leg's result is WITHDRAWN "
                 "rather than shipped (lesson 90).")}
    print(f"== control C2: T3 rows passing at gamma > 3: {len(c2_pass)} "
          f"(designed: 0) -> fires as designed = {not c2_pass}")

    # ------------------------------------------------------- the gate line
    gate_rows = sorted(k for k in passing
                       if verdicts[k]["gamma"] > 3.0
                       and verdicts[k]["class"] in ("T1_dprime", "T2_egm"))
    gate_yes = bool(gate_rows)
    out["gate"] = out["gate"]
    out["gate_answer"] = {
        "answer": "YES" if gate_yes else "NO",
        "qualifying_rows": gate_rows,
        "n_qualifying": len(gate_rows),
        "best_gap": (max(verdicts[k]["gap_n256"] for k in gate_rows)
                     if gate_rows else None),
        "branch_text": (
            "YES -> the zero-width window is a construction artifact, not an operator "
            "fact -- a genuine third-realization revival. ESCALATE to the user; do not "
            "build further under this leg's own authority."
            if gate_yes else
            "NO -> the coincidence persists under a second, independently-chosen "
            "construction, strengthening (not just repeating) leg 111's finding toward an "
            "operator-level fact. Bank it."),
        "controls_ok": {
            "C1_reproduction": out["control_C1_reproduction"]["all_ok"],
            "C2_falsification_fires": out["control_C2_falsification"]["fires_as_designed"],
            "C3_dissipation_sign_flips": all(v["sign_flips"] for v in c3.values()),
            "P0_weight_identity": p0["holds"],
            "P5_point_modes_removed": inters["T2_egm"]["intersection_dim"] == 0,
        },
    }

    # -------------------------------------------------------------- P6
    # Does the gap grow without bound as gamma -> 7?  Predicted NO.
    p6 = []
    for wname, fam, gam in WES_WEIGHT_FAMILY:
        if fam != "A":
            continue
        v = verdicts[f"T2_egm|{wname}"]
        D = wes_damping_factor(th[interior], fam, gam)
        p6.append({"weight": wname, "gamma": gam, "gap_n256": v["gap_n256"],
                   "local_gap_n256": v["local_gap_n256"],
                   "nonlocal_gap_n256": v["nonlocal_gap_n256"],
                   "sup_D_phi": float(D.max()),
                   "local_bound_minus_sup_D": float(-D.max()),
                   "admissible": v["clause_admissible"]})
    out["P6_saturation"] = {
        "rows": p6,
        "prediction": ("the gap does NOT grow without bound as gamma -> 7. sup_theta D_phi "
                       "= (3-gamma)/2 for gamma < 6 and -3/2 for gamma >= 6, so the local "
                       "part alone would allow (gamma-3)/2 capped at 1.5, while Xu's "
                       "ceiling is 0.5. The difference is the nonlocal Hilbert term the "
                       "weight cannot touch, and its size is reported per gamma.")}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print(f"GATE ANSWER: {out['gate_answer']['answer']}  "
          f"({out['gate_answer']['n_qualifying']} qualifying rows, "
          f"best gap {out['gate_answer']['best_gap']})")
    print(f"CONTROLS: {out['gate_answer']['controls_ok']}")


if __name__ == "__main__":
    main()
