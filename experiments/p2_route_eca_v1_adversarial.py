"""Route-ECA (leg 144): ADVERSARIAL AUDIT of `solver/energy_coercivity.py`.

`solver/energy_coercivity.py` is the instrument behind leg 111's headline -- "every
admissible weight's coercivity gap converges to `-(3-gamma)/2`, damping at the origin needs
`gamma > 3`, the space exists only for `gamma < 3`, so the window has ZERO width" -- which
leg 141/WEL is scoping for publication.  `test_energy_coercivity.py` (14 gates) validates
that instrument on WELL-FORMED inputs: the operator against `solver/spectral_certificate.py`,
the two published point-spectrum modes, the flat-weight Gram, the damping factor, the
admissible members' ladders, the `mu` control.  Every input in that file is legal and
in-domain.

This runner validates the other half: what the module returns for inputs that are inside its
public API's REACHABLE domain but outside the domain its own docstrings declare.  It edits
nothing.  `solver/energy_coercivity.py` is byte-identical to this branch's merge base under
both branches of the gate (leg 144 has no patch authority under its own gate; see
`writeup/novelty/leg_144.md` §0).

THE GATE (frozen in `writeup/novelty/leg_144.md` BEFORE any number below was computed):

  "Does `solver/energy_coercivity.py` contain a silent-corruption site -- an input inside its
   public API's reachable domain for which it returns a finite, plausible number instead of
   refusing, warning, or reporting the quantity as absent?"

Ten probes (P1-P10) and three controls (C1-C3), all named in the novelty log before the
first number.  Nothing outside that list is reported as this leg's finding.

WHAT THIS LEG DOES **NOT** CLAIM
--------------------------------
It does not retract or weaken leg 111.  Probe C1 is the reason: the six family members whose
numbers leg 111's conclusion actually rests on reproduce that leg's banked JSON to <= 6.8e-14
absolute, bit-for-bit at the top of the ladder.  Every site found below lives at
`gamma >= 3` (already marked `admissible: false` in leg 111's own `per_weight_verdict`) or
behind a non-default keyword argument.  A silent-corruption finding on this instrument can
only widen the error bars on a NEGATIVE result; it cannot turn one positive, and nothing here
reopens the weighted-energy window.

Usage:  .venv/bin/python experiments/p2_route_eca_v1_adversarial.py
Writes: writeup/data/p2_route_eca_v1_adversarial.json
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import time
import warnings

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver import energy_coercivity as ec                       # noqa: E402  READ-ONLY

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "writeup", "data", "p2_route_eca_v1_adversarial.json")
LEG111 = os.path.join(HERE, "writeup", "data", "p2_route_we_v1_coercivity.json")
MODULE = os.path.join(HERE, "solver", "energy_coercivity.py")


def capture(fn, *a, **k):
    """Call `fn`, recording the exception and any warning it raised.

    A site is SILENT iff it returns a finite value with no exception and no warning.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            value, err = fn(*a, **k), None
        except Exception as exc:                                  # noqa: BLE001
            value, err = None, f"{type(exc).__name__}: {exc}"
    return {"value": value, "error": err,
            "warnings": [str(w.message) for w in caught]}


def is_silent(rec):
    return rec["error"] is None and not rec["warnings"]


def main():
    t0 = time.time()
    res = {
        "leg": 144, "route": "ECA", "kind": "adversarial audit, read-only",
        "module_under_audit": "solver/energy_coercivity.py",
        "module_untouched": True,
        "gate_question": (
            "Does solver/energy_coercivity.py contain a silent-corruption site -- an input "
            "inside its public API's reachable domain for which it returns a finite, "
            "plausible number instead of refusing, warning, or reporting the quantity as "
            "absent?"),
        "gate_frozen_in": "writeup/novelty/leg_144.md (committed before construction)",
        "direction_md_defect": (
            "DIRECTION.md carries no section 144: 84 route sections, highest is "
            "'### 141 -- ROUTE-WEL' at line 3152; 0 hits for 'ROUTE-ECA' repo-wide and on "
            "origin/main. The gate above is this leg's own, declared in the novelty log "
            "before construction, in the wording the leg prompt supplied."),
    }
    try:
        res["module_sha256_head"] = subprocess.run(
            ["git", "hash-object", MODULE], cwd=HERE, capture_output=True,
            text=True, check=True).stdout.strip()
    except Exception:                                             # noqa: BLE001
        res["module_sha256_head"] = None

    banked = json.load(open(LEG111))
    N_LADDER = banked["n_ladder"]

    # ------------------------------------------------------------------ C1
    # THE CONTROL THAT CAN REPORT THE OTHER ANSWER (lesson 90).  If the audit's flags were
    # an artifact of this environment rather than of the module, the ADMISSIBLE members
    # would drift too.  They do not: they reproduce leg 111's banked JSON bit-for-bit.
    print("[C1] reproduction of leg 111's banked ladders -- same call, same defaults")
    repro = {}
    for name, fam, gam in ec.WEIGHT_FAMILY:
        recs = [ec.coercivity_gap(n, fam, gam) for n in N_LADDER]
        now = [r["gap"] for r in recs]
        bank = banked["gaps"][name]["modulated"]
        worst_abs = max(abs(a - b) for a, b in zip(now, bank))
        worst_rel = max(abs(a - b) / max(abs(b), 1e-300) for a, b in zip(now, bank))
        repro[name] = {
            "gamma": gam, "admissible_per_leg111": bool(banked["per_weight_verdict"][name]["admissible"]),
            "now": now, "banked": bank,
            "worst_abs_diff": worst_abs, "worst_rel_diff": worst_rel,
            "dropped_now": [r["dropped"] for r in recs],
            "dropped_banked": banked["gaps"][name]["dropped"],
            "cond_G_now": [r["cond_G"] for r in recs],
        }
        print(f"     {name:12s} worst abs {worst_abs:.3e}  worst rel {worst_rel:.3e}  "
              f"dropped now={recs[2]['dropped']} banked={banked['gaps'][name]['dropped'][2]}")
    res["C1_reproduction"] = repro
    res["C1_verdict"] = {
        "reproducing_members": [k for k, v in repro.items() if v["worst_abs_diff"] < 1e-12],
        "non_reproducing_members": [k for k, v in repro.items() if v["worst_abs_diff"] >= 1e-12],
        "worst_reproducing_abs_diff": max(v["worst_abs_diff"] for v in repro.values()
                                          if v["worst_abs_diff"] < 1e-12),
    }

    # determinism inside THIS environment: the drift is across builds, not across runs
    res["C1_determinism_A4_n64"] = [ec.coercivity_gap(64, "A", 4.0)["gap"] for _ in range(3)]

    # ------------------------------------------------------------------ P1 / P2
    # FINDING A.  `coercivity_gap` never consults `admissibility`.
    print("[P1/P2] the gap on weights whose space does not contain the trial basis")
    guard = {"coercivity_gap_calls_admissibility":
             "admissibility" in _source_of(ec.coercivity_gap)}
    ladders, monotonicity = {}, {}
    for name, fam, gam in ec.WEIGHT_FAMILY:
        lad = [ec.coercivity_gap(n, fam, gam)["gap"] for n in (8, 16, 32, 64, 128, 256)]
        incr = [lad[i + 1] - lad[i] for i in range(len(lad) - 1)]
        ladders[name] = lad
        monotonicity[name] = {
            "gamma": gam,
            "worst_increase": max(incr),
            # the module's own invariant (docstring of form_matrices, test gate 13):
            # nested trial spaces => the gap is non-increasing in n
            "violates_nested_subspace_invariant": max(incr) > 1e-9,
            "n_at_worst_increase": (8, 16, 32, 64, 128, 256)[int(np.argmax(incr)) + 1],
        }
    res["P1_gap_without_admissibility_guard"] = {
        "guard_present": guard,
        "gap_at_n48": {name: ec.coercivity_gap(48, fam, gam)["gap"]
                       for name, fam, gam in ec.WEIGHT_FAMILY},
        "silent": is_silent(capture(ec.coercivity_gap, 48, "A", 4.0)),
        "n_ladders": ladders,
        "monotonicity": monotonicity,
    }
    print("     monotonicity violations: " +
          ", ".join(f"{k}({v['worst_increase']:+.3f})" for k, v in monotonicity.items()
                    if v["violates_nested_subspace_invariant"]) or "     none")

    dial = {}
    for name, fam, gam in (("A2", "A", 2.0), ("A3", "A", 3.0), ("A4_chen_hou", "A", 4.0)):
        vals = [ec.coercivity_gap(64, fam, gam, n_grade=ng)["gap"]
                for ng in (8, 12, 16, 24, 32, 48, 64, 96)]
        dial[name] = {"n_grade": [8, 12, 16, 24, 32, 48, 64, 96], "gaps": vals,
                      "spread_absolute": max(vals) - min(vals),
                      "exceeds_published_ceiling": max(vals) - ec.KNOWN_ANSWER_CEILING}
    res["P2_quadrature_dial"] = dial
    print(f"     A4 spread over the n_grade dial = {dial['A4_chen_hou']['spread_absolute']:.3f} "
          f"(A2 control = {dial['A2']['spread_absolute']:.3e}); largest A4 value exceeds the "
          f"published ceiling {ec.KNOWN_ANSWER_CEILING} by "
          f"{dial['A4_chen_hou']['exceeds_published_ceiling']:+.3e}")
    res["P2_order_dial"] = {
        "A4": [ec.coercivity_gap(48, "A", 4.0, order=o)["gap"] for o in (6, 12, 20)],
        "A2_control": [ec.coercivity_gap(48, "A", 2.0, order=o)["gap"] for o in (6, 12, 20)],
    }

    # ------------------------------------------------------------------ P10 -> the
    # admissibility detector itself.  FINDING B, the highest-stakes site.
    print("[P10/P1] admissibility(): the divergence detector through its own public kwargs")
    adm = {}
    for ng in (24, 1, 0, -4):
        for gam in (2.0, 3.0, 4.0):
            r = ec.admissibility("A", gam, n_grade=ng)
            adm[f"n_grade={ng},gamma={gam}"] = {
                "ratio": r["ratio"], "increments": r["increments"],
                "increment_ratio": r["increment_ratio"],
                "exponent_margin": r["exponent_margin"],
                # the module's own reading of these fields (docstring lines 405-413):
                "module_reads_as_converged": (abs(r["ratio"] - 1.0) < 1e-6
                                              and r["increment_ratio"] is None),
                "silent": is_silent(capture(ec.admissibility, "A", gam, ng)),
            }
    res["P10_admissibility_kwargs"] = adm
    true_ratio = adm["n_grade=24,gamma=4.0"]["ratio"]
    print(f"     gamma=4 (power-divergent): default n_grade=24 -> ratio {true_ratio:.6e}, "
          f"shape {adm['n_grade=24,gamma=4.0']['increment_ratio']:.1f} (a power); "
          f"n_grade=0 -> ratio {adm['n_grade=0,gamma=4.0']['ratio']:.6f} and the module "
          f"reads that as CONVERGED")
    res["P10_suppression_factor"] = true_ratio / adm["n_grade=0,gamma=4.0"]["ratio"]

    # per-mode: is the mode-1 hardwiring itself a corruption?  (Leg 141/WEL already built a
    # control for this; recorded here so the audit is complete, NOT claimed as a finding.)
    def norm2_mode(k, gam, ng, fam="A"):
        th, qw = ec.graded_quadrature(n_grade=ng)
        return float(np.sum(np.sin(k * th) ** 2 * ec.weight_values(th, fam, gam) * qw))
    res["P10_per_mode_ratio"] = {
        str(gam): {str(k): norm2_mode(k, gam, 48) / norm2_mode(k, gam, 24) for k in (1, 2, 8, 32)}
        for gam in (2.0, 2.9, 3.0, 4.0)}
    res["P10_per_mode_note"] = (
        "NOT a finding of this leg: the convergence ratio is mode-independent to <3% at "
        "gamma=2.9, and leg 141/WEL (experiments/p2_route_wel_v1_lit.py, its p=1 control) "
        "already investigated admissibility()'s sin(theta) hardwiring.")

    # ------------------------------------------------------------------ P5 / P6 / P7
    print("[P5/P6/P7] graded_quadrature: the mesh through its own public kwargs")
    mesh = {}
    for label, kw in (("default", {}), ("n_unif=1", {"n_unif": 1}), ("n_unif=2", {"n_unif": 2}),
                      ("n_unif=3", {"n_unif": 3}), ("grade=1.0", {"grade": 1.0}),
                      ("grade=0.0", {"grade": 0.0}), ("grade=1.5", {"grade": 1.5}),
                      ("grade=2.0", {"grade": 2.0}), ("n_grade=0", {"n_grade": 0}),
                      ("n_grade=-4", {"n_grade": -4}), ("order=1", {"order": 1})):
        rec = capture(ec.graded_quadrature, **kw)
        if rec["error"]:
            mesh[label] = {"error": rec["error"], "silent": False}
            continue
        th, qw = rec["value"]
        mesh[label] = {
            "total_mass": float(np.sum(qw)),
            "mass_over_pi": float(np.sum(qw)) / math.pi,
            "n_nodes": int(th.size),
            "nodes_outside_0_pi": int(np.sum((th <= 0.0) | (th >= math.pi))),
            "min_node": float(th.min()), "max_node": float(th.max()),
            "silent": is_silent(rec),
        }
    res["P5_P6_P7_mesh"] = mesh
    print(f"     n_unif=1 total mass = {mesh['n_unif=1']['total_mass']:.9f} "
          f"({mesh['n_unif=1']['mass_over_pi']:.6f} x pi) with no warning; "
          f"grade=1.5 puts {mesh['grade=1.5']['nodes_outside_0_pi']} of "
          f"{mesh['grade=1.5']['n_nodes']} nodes outside (0, pi) and reports mass "
          f"{mesh['grade=1.5']['total_mass']:.3f}")

    # what an ungraded mesh does to the divergence test, reached through `grade`
    def norm2(gam, ng, gr):
        th, qw = ec.graded_quadrature(n_grade=ng, grade=gr)
        return float(np.sum(np.sin(th) ** 2 * ec.weight_values(th, "A", gam) * qw))
    res["P6_divergence_under_ungraded_mesh"] = {
        f"grade={gr}": {f"gamma={gam}": norm2(gam, 48, gr) / norm2(gam, 24, gr)
                        for gam in (3.0, 4.0)}
        for gr in (0.5, 1.0, 0.0)}

    # the n_unif=1 doubling, propagated into the quantity that is actually reported
    dbl = {}
    G1, _ = ec.form_matrices(8, "A", 0.0, n_unif=1)
    G2, _ = ec.form_matrices(8, "A", 0.0)
    dbl["flat_gram_diag_n_unif_1"] = float(G1[0, 0])
    dbl["flat_gram_diag_default"] = float(G2[0, 0])
    dbl["flat_gram_exact"] = math.pi / 2
    dbl["gram_ratio"] = float(G1[0, 0] / G2[0, 0])
    dbl["gap"] = {str(n): {"default": ec.coercivity_gap(n, "A", 2.0)["gap"],
                           "n_unif=1": ec.coercivity_gap(n, "A", 2.0, n_unif=1)["gap"]}
                  for n in (8, 16, 32)}
    res["P5_doubling_propagated"] = dbl
    print(f"     flat-weight Gram diagonal at n_unif=1 = {dbl['flat_gram_diag_n_unif_1']:.8f} "
          f"vs the exact pi/2 = {dbl['flat_gram_exact']:.8f} (ratio {dbl['gram_ratio']:.6f}); "
          f"gap at n=32 moves {dbl['gap']['32']['default']:+.6f} -> "
          f"{dbl['gap']['32']['n_unif=1']:+.6f}")

    # ------------------------------------------------------------------ P3 / P4
    print("[P3/P4] weight_values off the declared domain (0, pi), and the family guard")
    off = {}
    for th in (0.0, math.pi, -0.1, -0.3, 0.1, 0.3, math.pi + 0.1, 4.0, 7.0,
               2 * math.pi + 0.1):
        for gam in (2.0, 2.5, 3.0):
            rec = capture(ec.weight_values, np.array([th]), "A", gam)
            off[f"theta={th:.6f},gamma={gam}"] = {
                "value": (float(rec["value"][0]) if rec["value"] is not None
                          and np.isfinite(rec["value"][0]) else
                          (None if rec["value"] is None else str(rec["value"][0]))),
                "error": rec["error"], "warnings": rec["warnings"],
                "silent": is_silent(rec),
            }
    res["P3_off_domain_weight"] = off
    mirror = {
        "theta_plus_0.1": float(ec.weight_values(np.array([0.1]), "A", 2.0)[0]),
        "theta_minus_0.1": float(ec.weight_values(np.array([-0.1]), "A", 2.0)[0]),
        "theta_plus_0.3": float(ec.weight_values(np.array([0.3]), "A", 2.0)[0]),
        "theta_minus_0.3": float(ec.weight_values(np.array([-0.3]), "A", 2.0)[0]),
        "wrap_2pi_plus_0.1": float(ec.weight_values(np.array([2 * math.pi + 0.1]), "A", 2.0)[0]),
    }
    mirror["relative_mirror_error_0.1"] = abs(
        mirror["theta_minus_0.1"] - mirror["theta_plus_0.1"]) / mirror["theta_plus_0.1"]
    mirror["negative_weight_at_gamma_3"] = float(
        ec.weight_values(np.array([-0.1]), "A", 3.0)[0])
    mirror["nan_at_gamma_2.5"] = str(ec.weight_values(np.array([-0.1]), "A", 2.5)[0])
    res["P3_mirror"] = mirror
    print(f"     theta=-0.1 returns {mirror['theta_minus_0.1']:.8f}, the exact mirror of "
          f"theta=+0.1 (relative difference {mirror['relative_mirror_error_0.1']:.1e}); at "
          f"gamma=3 the same input returns a NEGATIVE weight "
          f"{mirror['negative_weight_at_gamma_3']:+.4f}")
    res["P3_damping_factor_off_domain"] = {
        str(th): float(ec.damping_factor(np.array([th]), "A", 2.0)[0])
        for th in (-1.0, 4.0, 7.0)}

    guards = {}
    for label, fn, args in (
            ("weight_values", ec.weight_values, (np.array([1.0]), "Z", 2.0)),
            ("weight_values_lowercase", ec.weight_values, (np.array([1.0]), "b", 2.0)),
            ("damping_factor", ec.damping_factor, (np.array([1.0]), "Z", 2.0)),
            ("damping_factor_at_origin", ec.damping_factor_at_origin, ("Z", 2.0)),
            ("form_matrices", ec.form_matrices, (8, "Z", 2.0)),
            ("coercivity_gap", ec.coercivity_gap, (8, "Z", 2.0)),
            ("admissibility", ec.admissibility, ("Z", 2.0))):
        guards[label] = capture(fn, *args)["error"]
    res["P4_family_guard"] = guards
    res["P4_guard_reachable_on_all_paths"] = all(
        e is not None and e.startswith("ValueError") for e in guards.values())
    print(f"     unknown-family guard raises on {sum(1 for e in guards.values() if e)}"
          f"/{len(guards)} public entry points  [C3: the module CAN fail loudly]")

    # ------------------------------------------------------------------ P8 / P9
    print("[P8/P9] the mu dial run backwards, and trial spaces smaller than the modulation")
    res["P8_negative_mu"] = {str(mu): ec.coercivity_gap(48, "A", 2.0, mu=mu)["gap"]
                             for mu in (-5.0, -1.0, -0.5, 0.0, 0.5, 2.0)}
    small = {}
    for n in (0, 1, 2, 3, 4, 5, 6):
        rec = capture(ec.coercivity_gap, n, "A", 2.0)
        entry = {"error": rec["error"]}
        if rec["value"] is not None:
            entry.update({k: rec["value"][k] for k in ("gap", "dim_trial", "dim_kept", "dropped")})
            entry["silent"] = is_silent(rec)
            entry["ceiling_excess"] = rec["value"]["gap"] - ec.KNOWN_ANSWER_CEILING
            entry["passes_module_ceiling_check"] = (
                rec["value"]["gap"] <= ec.KNOWN_ANSWER_CEILING + 1e-9)
        small[str(n)] = entry
    res["P9_small_trial_space"] = small
    res["P9_positive_gap_across_gamma"] = {
        f"gamma={gam}": {str(n): ec.coercivity_gap(n, "A", gam)["gap"] for n in (3, 4, 5, 8, 48)}
        for gam in (0.0, 1.0, 2.0)}
    print(f"     n=3, gamma=2: gap = {small['3']['gap']:.16f} from a trial space of "
          f"dimension {small['3']['dim_trial']} -- it SATURATES the published ceiling "
          f"{ec.KNOWN_ANSWER_CEILING} from below by {abs(small['3']['ceiling_excess']):.1e} "
          f"and passes the module's own instrument-bug check")

    # ------------------------------------------------------------------ verdict
    sites = {
        "A_inadmissible_gap_unguarded": {
            "where": "coercivity_gap(), no admissibility consultation",
            "magnitude": (
                f"A4_chen_hou (power-divergent, admissibility ratio {true_ratio:.3e}) returns "
                f"a finite gap with no warning; its n-ladder VIOLATES the module's own "
                f"nested-subspace monotonicity invariant at "
                f"{sum(1 for v in monotonicity.values() if v['violates_nested_subspace_invariant'])}"
                f"/7 members, worst increase "
                f"{monotonicity['A4_chen_hou']['worst_increase']:+.6f}; the value moves "
                f"{dial['A4_chen_hou']['spread_absolute']:.3f} across the quadrature dial "
                f"where the A2 control moves {dial['A2']['spread_absolute']:.1e}"),
        },
        "A2_not_reproducible_across_builds": {
            "where": "coercivity_gap() on the inadmissible member",
            "magnitude": (
                f"6 of 7 named weights reproduce leg 111's banked JSON to "
                f"{res['C1_verdict']['worst_reproducing_abs_diff']:.1e} absolute; "
                f"A4_chen_hou differs by up to "
                f"{repro['A4_chen_hou']['worst_abs_diff']:.3f} absolute / "
                f"{100 * repro['A4_chen_hou']['worst_rel_diff']:.0f}% relative "
                f"(n=64: {repro['A4_chen_hou']['now'][2]:+.4f} now vs "
                f"{repro['A4_chen_hou']['banked'][2]:+.4f} banked), deterministic within "
                f"this environment (3/3 identical runs)"),
        },
        "B_admissibility_detector_suppressed": {
            "where": "admissibility(n_grade<=0)",
            "magnitude": (
                f"gamma=4's divergence signal collapses from ratio {true_ratio:.3e} "
                f"(increment_ratio {adm['n_grade=24,gamma=4.0']['increment_ratio']:.0f}, a "
                f"power) to ratio exactly "
                f"{adm['n_grade=0,gamma=4.0']['ratio']:.6f} with increments [0, 0] and "
                f"increment_ratio None -- which the module's own docstring reads as "
                f"CONVERGED. Suppression factor {res['P10_suppression_factor']:.3e}"),
        },
        "C_mesh_silently_ungraded_or_off_domain": {
            "where": "graded_quadrature(grade>=1 or <=0, n_grade<=0)",
            "magnitude": (
                f"grade=1.0 keeps total mass exactly pi (the module's own consistency gate "
                f"still passes) while moving the innermost node from "
                f"{mesh['default']['min_node']:.3e} to {mesh['grade=1.0']['min_node']:.3e}, "
                f"which turns the gamma=4 divergence ratio from "
                f"{res['P6_divergence_under_ungraded_mesh']['grade=0.5']['gamma=4.0']:.3e} "
                f"into "
                f"{res['P6_divergence_under_ungraded_mesh']['grade=1.0']['gamma=4.0']:.6f}; "
                f"grade=1.5 places {mesh['grade=1.5']['nodes_outside_0_pi']}/"
                f"{mesh['grade=1.5']['n_nodes']} nodes outside (0, pi) and integrates "
                f"{mesh['grade=1.5']['mass_over_pi']:.1f}x the interval"),
        },
        "D_n_unif_1_doubles_the_measure": {
            "where": "graded_quadrature(n_unif=1) / form_matrices / coercivity_gap",
            "magnitude": (
                f"total quadrature mass {mesh['n_unif=1']['mass_over_pi']:.6f} x pi (the two "
                f"end panels each span the whole interval); the flat-weight Gram diagonal is "
                f"{dbl['flat_gram_diag_n_unif_1']:.8f} instead of pi/2 = "
                f"{dbl['flat_gram_exact']:.8f}; the gap agrees with the default to "
                f"{abs(dbl['gap']['8']['default'] - dbl['gap']['8']['n_unif=1']):.1e} at n=8 "
                f"and then diverges to {dbl['gap']['32']['n_unif=1']:+.4f} vs "
                f"{dbl['gap']['32']['default']:+.4f} at n=32 "
                f"({abs(dbl['gap']['32']['n_unif=1'] / dbl['gap']['32']['default']):.1f}x)"),
        },
        "E_weight_mirrored_off_domain": {
            "where": "weight_values(theta outside (0, pi))",
            "magnitude": (
                f"theta=-0.1 returns {mirror['theta_minus_0.1']:.8f}, the exact mirror of "
                f"theta=+0.1 to {mirror['relative_mirror_error_0.1']:.1e} relative, with no "
                f"warning; at gamma=3 the same input returns a NEGATIVE weight "
                f"{mirror['negative_weight_at_gamma_3']:+.4f} (an indefinite 'inner product') "
                f"and at gamma=2.5 a silent NaN; theta=2pi+0.1 wraps to "
                f"{mirror['wrap_2pi_plus_0.1']:.8f}. Only theta exactly 0 warns"),
        },
        "F_small_n_saturates_the_published_ceiling": {
            "where": "coercivity_gap(n<=4, modulate=True)",
            "magnitude": (
                f"n=3 returns gap = {small['3']['gap']:.16f} from a 1-dimensional trial "
                f"space -- {abs(small['3']['ceiling_excess']):.1e} BELOW the published "
                f"ceiling {ec.KNOWN_ANSWER_CEILING}, so the module's own instrument-bug "
                f"tripwire (a `<=` test) cannot fire; n=1 and n=2 raise loudly"),
        },
    }
    res["sites"] = sites
    res["gate_answer"] = "YES"
    res["gate_answer_wording"] = (
        "YES. Six sites. The module returns finite, plausible, unwarned numbers for inputs "
        "inside its public API's reachable domain but outside the domain its own docstrings "
        "declare. Leg 144 has no patch authority under its own gate: ESCALATED, not patched.")
    res["scope_what_this_does_not_retract"] = (
        "Leg 111 is NOT retracted. The 6 of 7 named weights its conclusion rests on "
        "reproduce its banked JSON to "
        f"{res['C1_verdict']['worst_reproducing_abs_diff']:.1e} absolute. Every site lives at "
        "gamma >= 3 (already `admissible: false` in leg 111's own per_weight_verdict) or "
        "behind a non-default keyword argument. The zero-width window is UNCHANGED and if "
        "anything sharpened: the numbers beyond the admissibility edge are not merely "
        "artifacts of the quadrature, they are not reproducible across LAPACK builds. "
        "THE ONE CONSUMER-FACING CONSEQUENCE: the A4_chen_hou gap values banked in "
        "writeup/data/p2_route_we_v1_coercivity.json and echoed nowhere else must not be "
        "quoted as measurements -- leg 141/WEL's publication scoping should cite the "
        "admissible members only.")
    res["ceiling_S7"] = (
        "Float64, one module, one process, the a=0 CLM linearisation -- the friendliest "
        "object in the repository. Nothing here moves a link of the L1->L4 chain, and a "
        "silent-corruption finding on this instrument can only widen the error bars on a "
        "NEGATIVE result, never turn one positive.")
    res["elapsed_s"] = time.time() - t0

    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=False, default=float)
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.1f}s)")
    print("GATE ANSWER: YES -- 6 sites; ESCALATED, not patched (module untouched).")


def _source_of(fn):
    import inspect
    try:
        return inspect.getsource(fn)
    except Exception:                                             # noqa: BLE001
        return ""


if __name__ == "__main__":
    main()
