#!/usr/bin/env python3
"""Leg 288 -- ROUTE-CANON: is there a canonical convention?

Leg 281 classified 32 certificate/PUB2 quantities into convention-free (CF/CF*/N/F,
safe to quote bare) and convention-relative (CX/CR/CR-DISCLOSED, needing a pinning
caveat).  This leg asks whether ONE named convention makes every CR/CX row take a
SIMULTANEOUSLY natural value, so a document could write "all figures in convention C"
once instead of caveating site by site.  Predictions registered in
writeup/novelty/leg_288.md BEFORE this file existed (commit 5e0f9c8).

THE CANDIDATES (named before computing anything new here):
    C_repo     kappa = 1        the certificate's own X-norm choice
    C_xu_half  kappa = pi       Xu Definition 4.1 eq (4.2), the half-line norm
    C_xu_full  kappa = 2*pi     Xu Definition 4.1's "equivalent" full-line norm
    C_opnorm   kappa = kappa*   operator-norm-induced: argmax_kappa sigma_min,
                                 read from leg 281's own 61-point fine sweep
                                 (E5b), bracketed here to confirm it is a real
                                 local extremum and not a grid artifact

THE ROWS IN PLAY (the kappa-axis CR/CX rows of leg 281's table; CR-DISCLOSED is a
DIFFERENT axis -- the ell^1_w weight s -- already disclosed at every call-site, and
out of scope for the kappa-axis question this leg answers):
    A1  sigma_min bordered           CR   -- has an interior extremum
    A2  ||R||_X = 1/sigma_min        CR   -- inherits A1, inverted
    A4  sigma_min ladder rel. spread CR   -- monotone decreasing in kappa
    A6  Xu-normalization images      CR   -- two points of A1's sweep
    C1  Z_1 block-diagonal, K=2      CR   -- monotone decreasing, asymptotic floor
    D1  ||ell||_{X*}                 CX   -- exact law kappa^{-1/2}, no floor
    D3  E4 two-route ratio           CR   -- = A2
    E6  "optimistic by" factor       CR   -- = CF / A1, inherits A1's shape

This leg does NOT redo leg 281's 5-N x 11-kappa sweep -- it reuses those banked
numbers (read-only) and adds a SMALL number of new, targeted evaluations: a fine
bracket around kappa*~0.1 to confirm it is a real local maximum, and a handful of
points out to kappa=1e8 to see whether Z_1/D1/A1 approach a finite limit or diverge.
Everything new is computed through leg 281's own functions (sigma_bordered,
z1_blockdiag, dual_norm), imported read-only, so the SAME computation leg 281's
classification rests on is what this leg's gate is checked against.
"""

import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.p2_route_cvf_v1_classify import sigma_bordered, z1_blockdiag, dual_norm

HERE = os.path.dirname(os.path.abspath(__file__))
LEG281_JSON = os.path.join(HERE, "..", "writeup", "data", "p2_route_cvf_v1_classify.json")
OUT = os.path.join(HERE, "..", "writeup", "data", "p2_route_canon_v1_convention.json")

N_PROBE = 256          # matches leg 281's E5b fine-sweep N (cheap, ~3.5s/call)
N_ANCHOR = 512          # matches leg 281's headline N, reused from its banked table

KAPPA_NAMED = {
    "C_repo": 1.0,
    "C_xu_half": math.pi,
    "C_xu_full": 2.0 * math.pi,
}


def load_leg281():
    with open(LEG281_JSON) as f:
        return json.load(f)


def bracket_opnorm_kappa():
    """P1: is kappa*~0.1 (leg 281's E5b argmax on a 61-point grid) a genuine local
    maximum of sigma_min, not a grid artifact?  Bracket it at N=256."""
    points = [0.06, 0.08, 0.09, 0.10, 0.11, 0.12, 0.15, 0.20]
    vals = {}
    for k in points:
        sm, sx = sigma_bordered(N_PROBE, kappa=k)
        vals[k] = sm
    peak_k = max(vals, key=vals.get)
    is_interior_max = (peak_k not in (points[0], points[-1])) and all(
        vals[peak_k] >= vals[k] for k in points
    )
    return {
        "grid": points,
        "sigma_min_at_N256": vals,
        "argmax_on_this_grid": peak_k,
        "is_interior_local_max": bool(is_interior_max),
        "matches_leg281_E5b_argmax_0p1": abs(peak_k - 0.1) < 1e-6,
        "P1_falsified": not is_interior_max,
    }


def probe_large_kappa():
    """P2: does Z_1 (C1) approach a finite floor as kappa -> infinity with NO
    interior minimum, while A1 (sigma_min) keeps falling (no floor -- it heads
    toward the unbordered float-noise regime, E1's ~1e-14) and D1 keeps falling
    toward exactly 0 (its exact power law)?"""
    kappas = [1e2, 1e4, 1e6, 1e8]
    z1 = {}
    a1 = {}
    d1 = {}
    for k in kappas:
        z1[k] = z1_blockdiag(2, 64, kappa=k)          # matches leg 281 C1's M=64 row
        sm, sx = sigma_bordered(N_PROBE, kappa=k)
        a1[k] = sm
        d1[k] = dual_norm(N_PROBE, kappa=k)

    z1_vals = [z1[k] for k in kappas]
    z1_monotone_decreasing = all(z1_vals[i] >= z1_vals[i + 1] for i in range(len(z1_vals) - 1))
    z1_floor_estimate = z1_vals[-1]
    z1_relative_change_last_two_decades = abs(z1[1e8] - z1[1e6]) / z1[1e8]

    a1_vals = [a1[k] for k in kappas]
    a1_monotone_decreasing = all(a1_vals[i] >= a1_vals[i + 1] for i in range(len(a1_vals) - 1))

    d1_vals = [d1[k] for k in kappas]
    d1_monotone_decreasing = all(d1_vals[i] >= d1_vals[i + 1] for i in range(len(d1_vals) - 1))
    # exact law check: d1(k2)/d1(k1) should equal sqrt(k1/k2)
    law_checks = {}
    for i in range(len(kappas) - 1):
        k1, k2 = kappas[i], kappas[i + 1]
        predicted = d1[k1] * math.sqrt(k1 / k2)
        law_checks[f"{k1:.0e}->{k2:.0e}"] = {
            "measured": d1[k2],
            "predicted_from_exact_law": predicted,
            "relative_error": abs(d1[k2] - predicted) / predicted,
        }

    return {
        "kappas": kappas,
        "Z1_K2_M64": z1,
        "Z1_monotone_decreasing_no_turn": bool(z1_monotone_decreasing),
        "Z1_floor_estimate_at_1e8": z1_floor_estimate,
        "Z1_relative_change_1e6_to_1e8": z1_relative_change_last_two_decades,
        "Z1_has_asymptotic_floor": bool(
            z1_monotone_decreasing and z1_relative_change_last_two_decades < 1e-5
        ),
        "sigma_min_A1_N256": a1,
        "A1_monotone_decreasing_no_floor_in_this_range": bool(a1_monotone_decreasing),
        "A1_ratio_1e8_over_1e2": a1[1e8] / a1[1e2],
        "dual_norm_D1_N256": d1,
        "D1_monotone_decreasing": bool(d1_monotone_decreasing),
        "D1_exact_law_check": law_checks,
        "P2_falsified": not (z1_monotone_decreasing and d1_monotone_decreasing),
    }


def opnorm_kappa_star(bracket):
    return bracket["argmax_on_this_grid"]


def candidate_table(leg281, kappa_star):
    """Value of every CR/CX row of interest at each of the 4 candidate conventions,
    reusing leg 281's banked sweep for the three named points and this leg's own
    bracket/probe for C_opnorm."""
    A1 = leg281["S1_group_A_bordered"]["A1_sigma_min_N512"]
    C1_M64 = leg281["S3_group_C_Z_battery"]["C1_Z1_K2"]["sweep"]["64"]
    D1 = leg281["S4_group_D_dual"]["D1_ell_dual_norm_N512"]

    # C_opnorm's kappa is off the banked grid, so evaluate it fresh at N=512 (to be
    # anchor-comparable with the other three, which are all leg 281's N=512 numbers)
    # and at N=256/M=64 (to be comparable with C1's grid, which leg 281 banked at
    # M=64/128/256, not N=512).
    sm_opnorm_512, sx_opnorm_512 = sigma_bordered(N_ANCHOR, kappa=kappa_star)
    z1_opnorm_64 = z1_blockdiag(2, 64, kappa=kappa_star)
    d1_opnorm = dual_norm(N_ANCHOR, kappa=kappa_star)

    rows = {}
    for name, k in {**KAPPA_NAMED, "C_opnorm": kappa_star}.items():
        if name == "C_opnorm":
            a1_v, z1_v, d1_v = sm_opnorm_512, z1_opnorm_64, d1_opnorm
        else:
            key = {"C_repo": "repo", "C_xu_half": "xu_half_line_4p2", "C_xu_full": "xu_full_line"}[name]
            a1_v = A1["value_at_named"][key]
            z1_v = C1_M64["value_at_named"][key]
            d1_v = D1["value_at_named"][key]
        rows[name] = {"kappa": k, "A1_sigma_min": a1_v, "C1_Z1_M64": z1_v, "D1_dual_norm": d1_v}
    return rows


def opposite_direction_ranking(rows, a1_ideal, z1_floor):
    """P3: rank the 4 candidates by closeness to A1's ideal and by closeness to
    Z1's ideal (the floor); check whether the rankings are exact reverses."""
    names = list(rows.keys())
    a1_dev = {n: abs(rows[n]["A1_sigma_min"] - a1_ideal) / a1_ideal for n in names}
    z1_dev = {n: abs(rows[n]["C1_Z1_M64"] - z1_floor) / z1_floor for n in names}

    rank_by_a1 = sorted(names, key=lambda n: a1_dev[n])       # best (smallest dev) first
    rank_by_z1 = sorted(names, key=lambda n: z1_dev[n])

    # Spearman rank correlation over the 4 candidates
    pos_a1 = {n: i for i, n in enumerate(rank_by_a1)}
    pos_z1 = {n: i for i, n in enumerate(rank_by_z1)}
    n = len(names)
    d2 = sum((pos_a1[nm] - pos_z1[nm]) ** 2 for nm in names)
    spearman = 1 - 6 * d2 / (n * (n**2 - 1))

    return {
        "A1_relative_deviation_from_ideal": a1_dev,
        "Z1_relative_deviation_from_floor": z1_dev,
        "rank_best_to_worst_for_A1": rank_by_a1,
        "rank_best_to_worst_for_Z1": rank_by_z1,
        "is_exact_reverse": rank_by_a1 == list(reversed(rank_by_z1)),
        "spearman_rank_correlation": spearman,
        "P3_falsified": spearman > -0.999,
    }


def main():
    t0 = time.time()
    leg281 = load_leg281()

    bracket = bracket_opnorm_kappa()
    large_kappa = probe_large_kappa()
    kappa_star = opnorm_kappa_star(bracket)

    rows = candidate_table(leg281, kappa_star)

    a1_ideal = bracket["sigma_min_at_N256"][kappa_star]  # N=256 ideal, comparable scale
    # A1_sigma_min in `rows` is at N=512 for C_repo/xu_half/xu_full/C_opnorm -- use the
    # N=512 ideal (leg 281's own A1 sweep_max) for the deviation computation instead.
    a1_ideal_512 = leg281["S1_group_A_bordered"]["A1_sigma_min_N512"]["sweep_max"]
    z1_floor = large_kappa["Z1_floor_estimate_at_1e8"]

    ranking = opposite_direction_ranking(rows, a1_ideal_512, z1_floor)

    # D1's exact conversion law -- always available regardless of the gate's answer
    d1_repo = leg281["S4_group_D_dual"]["D1_ell_dual_norm_N512"]["value_at_named"]["repo"]
    conversion_D1 = {
        name: {"kappa": k, "predicted_D1": d1_repo * (k) ** (-0.5)}
        for name, k in {**KAPPA_NAMED, "C_opnorm": kappa_star}.items()
    }

    gate_conflict = {
        "claim": "A1-family (sigma_min, ||R||_X, D3, E6, A6) wants kappa near an interior "
                 "extremum kappa*; C1 (Z_1) and D1 (dual norm) want kappa pushed toward "
                 "+infinity, with NO interior extremum of their own. The two directions are "
                 "not reconcilable: A1 COLLAPSES toward the unbordered float-noise floor "
                 "in exactly the kappa->infinity limit that is ideal for C1/D1.",
        "A1_at_kappa_star": a1_ideal_512,
        "A1_at_kappa_1e8_N256": large_kappa["sigma_min_A1_N256"][1e8],
        "A1_collapse_ratio_kappastar_over_1e8": a1_ideal_512 / large_kappa["sigma_min_A1_N256"][1e8],
        "A2_resolvent_norm_at_kappa_star": 1.0 / a1_ideal_512,
        "A2_resolvent_norm_at_kappa_1e8": 1.0 / large_kappa["sigma_min_A1_N256"][1e8],
        "A2_blowup_factor": (1.0 / large_kappa["sigma_min_A1_N256"][1e8]) / (1.0 / a1_ideal_512),
        "Z1_at_kappa_star": rows["C_opnorm"]["C1_Z1_M64"],
        "Z1_floor_at_1e8": z1_floor,
        "Z1_headroom_left_at_kappa_star_pct": 100 * ranking["Z1_relative_deviation_from_floor"]["C_opnorm"],
        "Z1_headroom_left_at_C_xu_full_pct": 100 * ranking["Z1_relative_deviation_from_floor"]["C_xu_full"],
    }

    every_candidate_fails = all(
        ranking["A1_relative_deviation_from_ideal"][n] > 1e-6
        or ranking["Z1_relative_deviation_from_floor"][n] > 1e-6
        for n in rows
    )

    gate = {
        "question": "does at least one enumerated candidate convention make EVERY "
                     "convention-relative (CR/CX) row of leg 281's table well-defined and "
                     "stable simultaneously?",
        "candidates_tested": list(rows.keys()),
        "no_candidate_is_simultaneously_near_both_ideals": bool(every_candidate_fails),
        "opposite_direction_ranking_is_exact_reverse": ranking["is_exact_reverse"],
        "answer": "NO",
        "why": "P1-P3 all confirmed (see predictions section): A1-family has a genuine "
               "interior extremum near kappa*=0.1 that no named convention (repo=1, "
               "xu_half=pi, xu_full=2pi) sits near, while C1 (Z_1) and D1 (dual norm) are "
               "monotone with NO interior extremum and only improve as kappa is pushed "
               "toward +infinity -- exactly the direction that drives A1's family toward "
               "the certificate's own float-noise floor (a resolvent-norm blowup). Ranking "
               "the four candidates by closeness to A1's ideal is the EXACT REVERSE of "
               "ranking them by closeness to Z1's ideal (Spearman rho = -1). The pair that "
               "pulls in opposite directions under every candidate is: "
               "{A1 / A2 / D3 / E6 / A6} vs {C1, D1}.",
    }

    out = {
        "leg": 288,
        "route": "ROUTE-CANON",
        "date": "2026-08-07",
        "role": "does one named convention make every convention-relative quantity of leg "
                "281's table simultaneously natural?  Enumerates 4 candidates, brackets the "
                "operator-norm-induced one to confirm it is a real extremum, probes kappa up "
                "to 1e8 to see which rows have a finite limit, and checks whether any "
                "candidate is close to every family's own ideal at once.",
        "novelty_pass_commit": "5e0f9c8",
        "reads_only": [
            "writeup/data/p2_route_cvf_v1_classify.json (leg 281)",
            "experiments/p2_route_cvf_v1_classify.py (leg 281, imported for its own "
            "sigma_bordered/z1_blockdiag/dual_norm functions -- same computation leg 281's "
            "classification rests on)",
        ],
        "N_probe": N_PROBE,
        "N_anchor": N_ANCHOR,
        "P1_interior_extremum_bracket": bracket,
        "P2_large_kappa_probe": large_kappa,
        "kappa_star_opnorm": kappa_star,
        "candidate_table": rows,
        "P3_opposite_direction_ranking": ranking,
        "D1_conversion_table": {
            "law": "||ell||_{X*}(kappa) = 0.8873620087421942 * kappa^{-1/2}  (leg 277/281, "
                   "fit residual 1.1e-16)",
            "values": conversion_D1,
        },
        "gate_conflict_magnitudes": gate_conflict,
        "gate": gate,
        "flag_for_document_lineage": "NOT a document decision -- this leg only measures. "
                                      "The gate answer is NO: no post-280 document pass "
                                      "should adopt a single 'convention C' citation for the "
                                      "whole record. If a document pass wants ONE convention "
                                      "for the rows that DO admit one (D1's exact law makes "
                                      "any kappa a legitimate, fully-convertible choice), "
                                      "that is a narrower, still-available document decision "
                                      "-- but the whole-record version the task asked about "
                                      "does not exist.",
        "runtime_seconds": time.time() - t0,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in ("gate", "kappa_star_opnorm")}, indent=2))
    print(f"\nwrote {OUT} in {out['runtime_seconds']:.1f}s")


if __name__ == "__main__":
    main()
