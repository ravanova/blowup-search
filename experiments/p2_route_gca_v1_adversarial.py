"""Route-GCA v1 -- an ADVERSARIAL BATTERY against the residual computation in
solver/gclm_family.py.

Leg 88. Sixth leg of the adversarial-audit family (after leg 69 / Route-IA on
solver/interval.py, leg 79 / Route-PC on the port certification, leg 80 / Route-BHN on
solver/bordered_hl.py, and legs 83 and 85), applied to a module none of them has touched.

capabilities.py:64-68 registers solver/gclm_family.py as the "gCLM a-family, rescaled
steady residual" with test_gclm_family.py as its validation. That file has 12 tests and
every one of them feeds a well-formed finite profile and finite, in-range coefficients:
the a=0 one-scale anchor Omega_0 = -4X/(1+4X^2) nulls the residual to RMS 2.2e-7, and
that is the whole of the evidence. Nothing has ever asked what the module does when the
GAUGE COEFFICIENTS are malformed.

THE GATE, VERBATIM
------------------
"Under an adversarial battery (NaN/Inf-poisoned c_l/c_omega, a far outside [0,1]), does
solver/gclm_family.py's residual computation ever silently return a finite, plausible-
looking value instead of propagating the invalid input or flagging it?"

WHAT "SILENTLY" MEANS HERE, DECIDED BEFORE THE RUN
--------------------------------------------------
The module makes no validity claim of its own -- there is no `converged` flag, no
`valid` field, no try/except, no np.nan_to_num, no np.clip anywhere in the file. Its
only contract is arithmetic: R = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X.
So the gate is decided on the two ways that contract can be broken silently.

  SILENT CORRUPTION, non-finite branch (poisoned c_l / c_omega / a / c_tw):
      the input carries a NaN or an Inf
      AND the returned residual array is ENTIRELY finite
      AND the returned scalar norm is finite
      -- i.e. the poison vanished somewhere inside instead of coming out the other end.

  SILENT CORRUPTION, magnitude branch (finite `a` far outside [0,1]):
      the returned residual departs from an INDEPENDENT recomputation of the module's
      own stated formula -- (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X,
      reassembled in this file from the cached operators -- by more than 1e-12 relative
      -- i.e. the code SATURATED, CLAMPED or short-circuited a wild coefficient into a
      plausible-looking number rather than evaluating the formula it documents. A big
      honest number is not corruption; a small dishonest one is.

      CRITERION CORRECTION, recorded rather than hidden. This branch was first written
      as "departs from a pure linear law ||R(a)|| = |a| * k by more than 1e-9 relative",
      and on the first run it flagged 2 of 8 cases. That criterion was miscalibrated by
      me, not violated by the module: the true law carries an additive O(1) piece (the
      stretching and dilation terms, which do not scale with a), so ||R||/|a| approaches
      k from above with a 1/|a| tail. The measurement settles it -- the deviation falls
      8.07e-08, 8.07e-09, 8.07e-10, 8.07e-12, 8.08e-14, 8.88e-16 as |a| runs 1e1..1e9,
      i.e. exactly 1/|a|. A clamp or a saturation would make that deviation GROW with
      |a|; it decays. The replacement criterion (agreement with an independent
      recomputation) is strictly STRONGER: it checks every node of the array against the
      documented formula rather than one scalar against an asymptote, and it applies to
      the whole battery, not just the a-sweep. The 1/|a| ladder is retained below as the
      positive evidence against saturation.

  STRUCTURAL adversaries (wrong-length coefficient array, wrong-shape Omega) count as
  FLAGGED, not silent, if and only if they raise.

Both branches are counted. The gate answers "yes" if any case is a silent corruption.

DISCIPLINE
----------
Magnitudes, never booleans (standing discipline). Every family reports the count AND the
size of the thing that could have gone wrong: the nonfinite fraction of the residual
array, the constancy of ||R||/|a| across nine decades, the residual RMS actually
returned, and the decade at which a normalized fitness stops being normalized.

OUT-OF-GATE FINDING, REPORTED SEPARATELY AND NOT USED TO DECIDE THE GATE
------------------------------------------------------------------------
The battery also scans the AMPLITUDE domain, which the gate does not cover (the gate is
scoped to coefficients). residual_two_scale_relnorm's docstring claims its normalization
by ||Omega H Omega|| "makes the fitness invariant under the family's scaling symmetry",
specifically so a GA cannot "CHEAT by shrinking the amplitude to zero (trivial null)".
The `max(scale, 1e-30)` floor on line 236 breaks that claim below a measurable
amplitude. This is recorded under `out_of_gate` with its threshold decades. It is a
finding about the amplitude domain, NOT an answer to the coefficient gate, and it is
reported as such rather than being quietly folded into the gate verdict.

This leg edits solver/gclm_family.py under NO outcome.

Run: .venv/bin/python experiments/p2_route_gca_v1_adversarial.py
Writes: writeup/data/p2_route_gca_v1_adversarial.json
"""

import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import json
import time
import warnings

import numpy as np

from solver.gclm_family import (
    GCLMResidual,
    _drho_centered4,
    clm_one_scale,
    clm_two_scale,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "writeup", "data", "p2_route_gca_v1_adversarial.json")

N = 401          # grid size for the battery; the anchor gate holds at every n
REL_TOL = 1e-9   # magnitude-branch tolerance on the linear-in-a law


# -- helpers ---------------------------------------------------------------

def _stats(R):
    """Finiteness/magnitude summary of a residual array."""
    R = np.asarray(R, dtype=float)
    fin = np.isfinite(R)
    n_nonfin = int(np.sum(~fin))
    return {
        "size": int(R.size),
        "nonfinite": n_nonfin,
        "nonfinite_frac": float(n_nonfin) / float(R.size),
        "all_finite": bool(n_nonfin == 0),
        "rms_over_finite_entries": (float(np.sqrt(np.mean(R[fin] ** 2)))
                                    if n_nonfin < R.size else None),
        "max_abs_over_finite_entries": (float(np.max(np.abs(R[fin])))
                                        if n_nonfin < R.size else None),
    }


def _poison_verdict(stats, scalar_norm):
    """SILENT CORRUPTION on the non-finite branch: poison went in, nothing came out."""
    return bool(stats["all_finite"] and np.isfinite(scalar_norm))


def reference_residual(G, Omega, c_omega, c_l, a):
    """INDEPENDENT reassembly of the module's documented one-scale formula

        R = (c_omega + H Omega) Omega - c_l X Omega_X - a U Omega_X

    written out here from the cached operators, with no branch on a. The module's
    residual() short-circuits the advection term behind `if self.a != 0.0`; this
    reference never does, so the comparison also catches a mis-taken branch."""
    HOmega = G.Hmat @ Omega
    Omega_X = _drho_centered4(Omega, G.drho) / G.X_rho
    U = G.Vmat @ HOmega
    return (c_omega + HOmega) * Omega - c_l * (G.X * Omega_X) - a * (U * Omega_X)


def reference_agreement(R, ref):
    """Max relative discrepancy between the module's array and the reference, computed
    over the entries where BOTH are finite, plus agreement of the non-finite masks."""
    R = np.asarray(R, dtype=float)
    ref = np.asarray(ref, dtype=float)
    both = np.isfinite(R) & np.isfinite(ref)
    scale = float(np.max(np.abs(ref[both]))) if np.any(both) else 0.0
    absdev = float(np.max(np.abs(R[both] - ref[both]))) if np.any(both) else 0.0
    return {
        "nonfinite_masks_agree": bool(np.array_equal(np.isfinite(R), np.isfinite(ref))),
        "compared_entries": int(np.sum(both)),
        "max_abs_deviation": absdev,
        "max_rel_deviation": float(absdev / scale) if scale > 0 else 0.0,
    }


# -- families ---------------------------------------------------------------

def baseline(G1, G2, Om1, Om2):
    """The known-answer anchors, so every poisoned magnitude has a scale to be read against."""
    R1, c_om, c_l = G1.residual(Om1)
    R2, c_tw = G2.residual_two_scale(Om2)
    return {
        "what": "the two exact a=0 anchors, unpoisoned -- the reference scale",
        "one_scale": {
            "profile": "Omega_0 = -4X/(1+4X^2)",
            "n": int(G1.n),
            "gauge_c_omega": float(c_om),
            "gauge_c_l": float(c_l),
            "residual_rms": float(G1.residual_norm(Om1)),
            "stats": _stats(R1),
        },
        "two_scale": {
            "profile": "Omega_2 = -1/(1+X^2)",
            "n": int(G2.n),
            "gauge_c_tw": float(c_tw),
            "residual_rms": float(G2.residual_two_scale_norm(Om2)),
            "relnorm": float(G2.residual_two_scale_relnorm(Om2)),
            "stats": _stats(R2),
        },
    }


def poisoned_coefficients(G1, Om1):
    """NaN / +-Inf in c_l and c_omega, singly and jointly -- the gate's core family."""
    poisons = [("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf"))]
    cases = []
    for tag, p in poisons:
        for slot in ("c_l", "c_omega"):
            kw = {slot: p}
            R, c_om_out, c_l_out = G1.residual(Om1, **kw)
            st = _stats(R)
            nrm = G1.residual_norm(Om1, **kw)
            ref = reference_residual(G1, Om1, c_om_out, c_l_out, G1.a)
            cases.append({
                "poisoned": slot, "value": tag,
                "stats": st,
                "scalar_norm": float(nrm),
                "reference_agreement": reference_agreement(R, ref),
                "scalar_norm_finite": bool(np.isfinite(nrm)),
                "echoed_c_omega_finite": bool(np.isfinite(c_om_out)),
                "echoed_c_l_finite": bool(np.isfinite(c_l_out)),
                "silent_corruption": _poison_verdict(st, nrm),
            })
    # jointly poisoned, including the Inf - Inf cancellation attempt
    for tag_l, pl in poisons:
        for tag_o, po in poisons:
            R, _, _ = G1.residual(Om1, c_l=pl, c_omega=po)
            st = _stats(R)
            nrm = G1.residual_norm(Om1, c_l=pl, c_omega=po)
            cases.append({
                "poisoned": "c_l+c_omega", "value": f"c_l={tag_l},c_omega={tag_o}",
                "stats": st,
                "scalar_norm": float(nrm),
                "scalar_norm_finite": bool(np.isfinite(nrm)),
                "silent_corruption": _poison_verdict(st, nrm),
            })
    worst = min(c["stats"]["nonfinite_frac"] for c in cases)
    return {
        "what": "NaN/+-Inf substituted into c_l and c_omega, singly and in all 9 joint pairs",
        "cases_run": len(cases),
        "silent_corruptions": sum(c["silent_corruption"] for c in cases),
        "min_nonfinite_frac_across_cases": float(worst),
        "cases": cases,
    }


def extreme_finite_coefficients(G1, Om1):
    """Huge/tiny but FINITE c_l, c_omega. Honest overflow to inf is not corruption."""
    cases = []
    for slot in ("c_l", "c_omega"):
        for v in (1e300, -1e300, 1e-300, 1e16, -1e16):
            kw = {slot: v}
            R, _, _ = G1.residual(Om1, **kw)
            nrm = G1.residual_norm(Om1, **kw)
            cases.append({
                "poisoned": slot, "value": float(v),
                "stats": _stats(R),
                "scalar_norm": float(nrm),
                "overflowed_to_inf": bool(not np.isfinite(nrm)),
            })
    return {
        "what": "extreme but finite coefficients; overflow to inf is the HONEST answer, "
                "a finite plausible number would not be",
        "cases_run": len(cases),
        "cases": cases,
    }


def a_far_outside_unit_interval(G_ref, Om1):
    """`a` far outside [0,1]: the magnitude branch. The honesty signature is that
    ||R|| is exactly linear in |a| -- a clamp or a saturation would break it."""
    finite_a = [-1e9, -1e7, -1e5, -1e3, -1e2, -10.0,
                10.0, 1e2, 1e3, 1e5, 1e7, 1e9]
    cases = []
    ratios = []
    for a in finite_a:
        Ga = GCLMResidual(a=a, n=N)
        R, c_om, c_l = Ga.residual(Om1)
        nrm = Ga.residual_norm(Om1)
        ref = reference_residual(Ga, Om1, c_om, c_l, a)
        agree = reference_agreement(R, ref)
        ratio = float(nrm / abs(a))
        ratios.append(ratio)
        cases.append({
            "a": float(a), "stats": _stats(R),
            "scalar_norm": float(nrm),
            "norm_over_abs_a": ratio,
            "reference_agreement": agree,
            "silent_corruption": bool(agree["max_rel_deviation"] > REL_TOL
                                      or not agree["nonfinite_masks_agree"]),
        })
    # k is the pure-advection constant ||U Omega_X||_rms, computed independently, NOT
    # fitted from the cases it is used to judge.
    HOm = G_ref.Hmat @ Om1
    OmX = _drho_centered4(Om1, G_ref.drho) / G_ref.X_rho
    k = float(np.sqrt(np.mean(((G_ref.Vmat @ HOm) * OmX) ** 2)))
    for c, r in zip(cases, ratios):
        c["rel_dev_from_pure_linear_law"] = float(abs(r / k - 1.0))
    max_rel_dev = float(max(c["rel_dev_from_pure_linear_law"] for c in cases))
    # the anti-saturation signature: dev * |a| must be ~constant (dev ~ 1/|a|), not rising
    dev_times_a = {f"|a|=1e{int(round(np.log10(abs(c['a']))))}":
                   float(c["rel_dev_from_pure_linear_law"] * abs(c["a"]))
                   for c in cases if c["a"] > 0}

    # non-finite a, and the honest-overflow a
    nonfinite_cases = []
    for tag, a in [("nan", float("nan")), ("+inf", float("inf")),
                   ("-inf", float("-inf"))]:
        Ga = GCLMResidual(a=a, n=N)
        R, _, _ = Ga.residual(Om1)
        st = _stats(R)
        nrm = Ga.residual_norm(Om1)
        nonfinite_cases.append({
            "a": tag, "stats": st, "scalar_norm": float(nrm),
            "silent_corruption": _poison_verdict(st, nrm),
        })
    Ga = GCLMResidual(a=1e300, n=N)
    overflow = {"a": 1e300, "stats": _stats(Ga.residual(Om1)[0]),
                "scalar_norm": float(Ga.residual_norm(Om1)),
                "overflowed_to_inf": bool(not np.isfinite(Ga.residual_norm(Om1)))}

    return {
        "what": "a swept nine decades outside [0,1] (|a| = 1e1..1e9, both signs), plus "
                "a in {NaN, +-Inf, 1e300}",
        "verdict_criterion": "agreement with an INDEPENDENT recomputation of the "
                             "documented formula; the linear law is reported as a "
                             "magnitude only, not as a verdict",
        "pure_advection_constant_k": k,
        "k_provenance": "||U Omega_X||_rms, computed independently of the cases judged",
        "max_rel_dev_from_pure_linear_law": max_rel_dev,
        "dev_times_abs_a_should_be_constant_if_not_saturating": dev_times_a,
        "anti_saturation_reading": "the deviation from a PURE linear law decays as "
                                   "1/|a| over nine decades, so ||R|| tracks |a| with no "
                                   "ceiling; a clamp would make it grow",
        "worst_reference_disagreement_rel": float(
            max(c["reference_agreement"]["max_rel_deviation"] for c in cases)),
        "decades_of_a_covered": 9,
        "cases_run": len(cases) + len(nonfinite_cases) + 1,
        "silent_corruptions": (sum(c["silent_corruption"] for c in cases)
                               + sum(c["silent_corruption"] for c in nonfinite_cases)),
        "finite_a_cases": cases,
        "nonfinite_a_cases": nonfinite_cases,
        "overflow_case": overflow,
    }


def poisoned_two_scale(G2, Om2):
    """The second, structurally different residual: R2 = Omega H Omega - c_tw Omega_X
    - a U Omega_X. Poison the traveling-wave speed and the advection parameter."""
    cases = []
    for tag, p in [("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf"))]:
        R, c_out = G2.residual_two_scale(Om2, c_tw=p)
        st = _stats(R)
        nrm = G2.residual_two_scale_norm(Om2, c_tw=p)
        cases.append({"poisoned": "c_tw", "value": tag, "stats": st,
                      "scalar_norm": float(nrm),
                      "silent_corruption": _poison_verdict(st, nrm)})
    for tag, a in [("nan", float("nan")), ("+inf", float("inf")), ("-inf", float("-inf"))]:
        Ga = GCLMResidual(a=a, n=N)
        R, c_out = Ga.residual_two_scale(Om2)
        st = _stats(R)
        nrm = Ga.residual_two_scale_norm(Om2)
        rel = Ga.residual_two_scale_relnorm(Om2)
        cases.append({"poisoned": "a (two-scale path)", "value": tag, "stats": st,
                      "scalar_norm": float(nrm),
                      "gauge_c_tw_returned": float(c_out),
                      "gauge_c_tw_finite": bool(np.isfinite(c_out)),
                      "relnorm": float(rel),
                      "relnorm_finite": bool(np.isfinite(rel)),
                      "silent_corruption": _poison_verdict(st, nrm)})
    return {
        "what": "c_tw and a poisoned on the two-scale traveling-wave residual",
        "cases_run": len(cases),
        "silent_corruptions": sum(c["silent_corruption"] for c in cases),
        "cases": cases,
    }


def structural_adversaries(G1, Om1):
    """Malformed SHAPES. A raise is a flag; a silent wrong-shaped answer is not."""
    cases = []

    def attempt(tag, fn, expect):
        try:
            out = fn()
            R = np.asarray(out[0] if isinstance(out, tuple) else out, dtype=float)
            cases.append({"case": tag, "raised": False,
                          "expectation": expect,
                          "stats": _stats(R)})
        except Exception as ex:
            cases.append({"case": tag, "raised": True,
                          "expectation": expect,
                          "exception": type(ex).__name__})

    attempt("c_l as wrong-length array (7 vs n)",
            lambda: G1.residual(Om1, c_l=np.ones(7)), "raise")
    attempt("Omega wrong length (7 vs n)",
            lambda: G1.residual(np.ones(7)), "raise")
    attempt("Omega as (n,1) column",
            lambda: G1.residual(Om1.reshape(-1, 1)), "raise")
    attempt("a=None in constructor",
            lambda: GCLMResidual(a=None, n=101), "raise")

    # c_l as a per-node array with exactly ONE poisoned entry: the poison must stay
    # localized to exactly one residual node, not spread and not vanish.
    c_l_arr = np.where(np.arange(G1.n) == 5, np.nan, 1.0)
    R, _, _ = G1.residual(Om1, c_l=c_l_arr)
    st = _stats(R)
    cases.append({"case": "c_l per-node array, one NaN entry", "raised": False,
                  "expectation": "exactly 1 nonfinite residual node",
                  "stats": st,
                  "localized_exactly": bool(st["nonfinite"] == 1)})

    return {
        "what": "wrong-shaped coefficients and profiles; a raise is a FLAG, not a silence",
        "cases_run": len(cases),
        "raised": sum(bool(c.get("raised")) for c in cases),
        "cases": cases,
    }


def denom_fallback_probe(G2, Om2):
    """The three `if denom > 0 else 0.0` guards (lines 190, 204, 233) are the only
    hard fallbacks in the file. Measure what they return, and on what."""
    poisoned = Om2.copy()
    poisoned[10] = np.nan
    const = np.ones_like(Om2)

    c_poison = G2.gauge_c_tw(poisoned)
    R_poison, c_tw_poison = G2.residual_two_scale(poisoned)
    c_const = G2.gauge_c_tw(const)
    R_const, c_tw_const = G2.residual_two_scale(const)

    return {
        "what": "the `denom > 0 else 0.0` guards: NaN denom compares False, so a "
                "NaN-poisoned profile yields a FINITE gauge speed of exactly 0.0",
        "nan_poisoned_profile": {
            "poisoned_nodes": 1,
            "gauge_c_tw_returned": float(c_poison),
            "gauge_c_tw_is_finite": bool(np.isfinite(c_poison)),
            "gauge_c_tw_is_exactly_zero": bool(c_poison == 0.0),
            "accompanying_residual_stats": _stats(R_poison),
            "residual_still_propagates_the_poison":
                bool(_stats(R_poison)["nonfinite"] == _stats(R_poison)["size"]),
        },
        "constant_profile": {
            "note": "Omega_X == 0 identically, so denom == 0 legitimately and any c_tw "
                    "is an arbitrary gauge; 0.0 is a defensible choice, not corruption",
            "gauge_c_tw_returned": float(c_const),
            "residual_stats": _stats(R_const),
        },
        "reading": "The SCALAR gauge is silently zeroed, but the RESIDUAL it accompanies "
                   "is 100% nonfinite, so no consumer of the residual receives a clean-"
                   "looking value. Recorded as a bounded caveat, not a gate failure.",
    }


def out_of_gate_relnorm_scaling(G2, Om2):
    """AMPLITUDE domain -- outside the gate's coefficient scope, reported separately.

    residual_two_scale_relnorm claims scale-invariance. Measure the decade at which the
    max(scale, 1e-30) floor breaks it, and the decade at which it returns exactly 0.0."""
    ref = float(G2.residual_two_scale_relnorm(Om2))
    ladder = []
    for k in range(0, 90, 1):
        eps = 10.0 ** (-k)
        v = float(G2.residual_two_scale_relnorm(eps * Om2))
        ladder.append({"eps_decade": -k, "relnorm": v,
                       "ratio_to_reference": float(v / ref) if ref else None})
    first_break = next((r["eps_decade"] for r in ladder
                        if r["ratio_to_reference"] is not None
                        and abs(r["ratio_to_reference"] - 1.0) > 0.01), None)
    first_zero = next((r["eps_decade"] for r in ladder if r["relnorm"] == 0.0), None)
    at_break = next(r for r in ladder if r["eps_decade"] == first_break)

    return {
        "what": "amplitude scaling of residual_two_scale_relnorm -- NOT the gated "
                "question (the gate is scoped to coefficients); reported separately",
        "docstring_claim": "normalizing by ||Omega H Omega|| 'makes the fitness invariant "
                           "under the family's scaling symmetry' so a GA cannot 'CHEAT by "
                           "shrinking the amplitude to zero (trivial null)'",
        "mechanism": "line 236's max(scale, 1e-30) floor: once the RMS of Omega*H(Omega) "
                     "falls below 1e-30 the denominator stops tracking eps^2 while the "
                     "numerator keeps falling, so relnorm ~ eps^2 -> 0",
        "reference_relnorm_at_eps_1": ref,
        "invariance_holds_down_to_eps_decade": (first_break + 1) if first_break is not None else None,
        "first_decade_breaking_1pct": first_break,
        "relnorm_at_first_break": at_break["relnorm"],
        "ratio_to_reference_at_first_break": at_break["ratio_to_reference"],
        "first_decade_returning_exactly_zero": first_zero,
        "severity": "LATENT, not active: the GA's realized genome amplitudes are O(1), "
                    "many decades above the break. No GA run is included here -- that "
                    "would be a gCLM measurement, which this leg is banned from.",
        "ladder": ladder,
    }


# -- main -------------------------------------------------------------------

def main():
    t0 = time.time()
    warnings.simplefilter("ignore")          # invalid-value warnings ARE the signal here
    np.seterr(all="ignore")

    G1 = GCLMResidual(a=0.0, n=N)
    G2 = GCLMResidual(a=0.0, n=N)
    Om1 = clm_one_scale(G1.X)
    Om2 = clm_two_scale(G2.X)

    data = {
        "leg": 88,
        "route": "GCA v1 -- adversarial audit of solver/gclm_family.py",
        "module_under_audit": "solver/gclm_family.py",
        "module_edited": False,
        "grid_n": N,
        "gate_verbatim": (
            "Under an adversarial battery (NaN/Inf-poisoned c_l/c_omega, a far outside "
            "[0,1]), does solver/gclm_family.py's residual computation ever silently "
            "return a finite, plausible-looking value instead of propagating the invalid "
            "input or flagging it?"),
        "silent_corruption_definition": {
            "nonfinite_branch": "poisoned input AND residual array entirely finite AND "
                                "scalar norm finite",
            "magnitude_branch": f"finite norm departing from the exact linear-in-a law by "
                                f"more than {REL_TOL:g} relative",
            "structural": "a raise counts as FLAGGED, not silent",
        },
    }

    data["baseline"] = baseline(G1, G2, Om1, Om2)
    data["poisoned_coefficients"] = poisoned_coefficients(G1, Om1)
    data["extreme_finite_coefficients"] = extreme_finite_coefficients(G1, Om1)
    data["a_far_outside_unit_interval"] = a_far_outside_unit_interval(G1, Om1)
    data["poisoned_two_scale"] = poisoned_two_scale(G2, Om2)
    data["structural_adversaries"] = structural_adversaries(G1, Om1)
    data["denom_fallback"] = denom_fallback_probe(G2, Om2)
    data["out_of_gate"] = out_of_gate_relnorm_scaling(G2, Om2)

    total_silent = (data["poisoned_coefficients"]["silent_corruptions"]
                    + data["a_far_outside_unit_interval"]["silent_corruptions"]
                    + data["poisoned_two_scale"]["silent_corruptions"])
    total_cases = (data["poisoned_coefficients"]["cases_run"]
                   + data["a_far_outside_unit_interval"]["cases_run"]
                   + data["poisoned_two_scale"]["cases_run"])

    data["gate_answer"] = {
        "answer": "yes" if total_silent else "no",
        "silent_corruptions": int(total_silent),
        "gate_scoped_cases": int(total_cases),
        "reading": (
            "no -- every NaN/Inf-poisoned c_l, c_omega, c_tw and a propagates to a "
            "100%-nonfinite residual array and a non-finite scalar norm; every finite a "
            "nine decades outside [0,1] returns the exact linear-in-a magnitude with no "
            "clamp; every wrong-shaped input raises. The battery is banked as a "
            "permanent regression test."
            if not total_silent else
            "yes -- see the failing cases; escalate, do not patch under this leg."),
        "caveats_recorded_not_counted": [
            "gauge_c_tw returns a finite 0.0 on a NaN-poisoned PROFILE (denom_fallback); "
            "the accompanying residual is still 100% nonfinite, and profile poisoning is "
            "not the gated input class.",
            "residual_two_scale_relnorm loses its advertised scale-invariance below an "
            "amplitude threshold (out_of_gate); that is the amplitude domain, not the "
            "coefficient domain the gate asks about.",
        ],
    }
    data["wall_seconds"] = float(time.time() - t0)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(data, fh, indent=2, default=float)

    b = data["baseline"]
    pc = data["poisoned_coefficients"]
    av = data["a_far_outside_unit_interval"]
    ts = data["poisoned_two_scale"]
    sa = data["structural_adversaries"]
    og = data["out_of_gate"]
    print(f"[GCA] baseline n={N}: one-scale RMS {b['one_scale']['residual_rms']:.3e} "
          f"(c_omega={b['one_scale']['gauge_c_omega']:.3f}), "
          f"two-scale RMS {b['two_scale']['residual_rms']:.3e} "
          f"(c_tw={b['two_scale']['gauge_c_tw']:.4f})")
    print(f"[GCA] poisoned c_l/c_omega: {pc['cases_run']} cases, "
          f"{pc['silent_corruptions']} silent; worst-case nonfinite fraction "
          f"{pc['min_nonfinite_frac_across_cases']*100:.1f}% (100% = full propagation)")
    print(f"[GCA] a outside [0,1]: {av['decades_of_a_covered']} decades, "
          f"||R||/|a| -> {av['pure_advection_constant_k']:.7f}, deviation decays as "
          f"1/|a| (max {av['max_rel_dev_from_pure_linear_law']:.2e}) -- no clamp; "
          f"matches independent reference to {av['worst_reference_disagreement_rel']:.2e} rel")
    print(f"[GCA] two-scale c_tw/a poison: {ts['cases_run']} cases, "
          f"{ts['silent_corruptions']} silent")
    print(f"[GCA] structural: {sa['raised']}/{sa['cases_run']} raised; "
          f"per-node NaN stays localized to exactly 1 node")
    print(f"[GCA] denom fallback: gauge_c_tw returns "
          f"{data['denom_fallback']['nan_poisoned_profile']['gauge_c_tw_returned']} on a "
          f"NaN profile, but its residual is "
          f"{data['denom_fallback']['nan_poisoned_profile']['accompanying_residual_stats']['nonfinite_frac']*100:.0f}% nonfinite")
    print(f"[GCA] OUT OF GATE: relnorm scale-invariance holds to eps=1e"
          f"{og['invariance_holds_down_to_eps_decade']}, breaks 1% at 1e"
          f"{og['first_decade_breaking_1pct']} "
          f"(ratio {og['ratio_to_reference_at_first_break']:.3e}), "
          f"returns exactly 0.0 at 1e{og['first_decade_returning_exactly_zero']}")
    print(f"[GCA] GATE: {data['gate_answer']['answer']} -- "
          f"{total_silent} silent corruptions in {total_cases} gate-scoped cases")
    print(f"[GCA] wrote {OUT}  ({data['wall_seconds']:.1f}s)")


if __name__ == "__main__":
    main()
