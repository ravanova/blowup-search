"""PROG-R4 U5 (MILESTONE M3) -- EVIDENCE: every number the BLOG and TECHNICAL
write-ups quote, re-derived from the banked JSONs rather than transcribed.

Sources, all committed:
  writeup/data/p2_prog_r4_m3_v1.json                       U5, this unit
  writeup/data/p2_prog_r4_g1_v1.json                       U3, the baseline
  experiments/programme_r4/u5_shift_library_admissible.json the 575 in-window

Nothing expensive is recomputed. No DNS, no mining, no Newton. This file exists
because journal sections 6.3, 6.4 and 9.2 quote a matched-R comparison, a
band-exit table and a distinct-orbits-per-core-hour figure that a reader could
not otherwise re-derive: they are not fields of any banked JSON, they are
computed FROM those JSONs, and until now they were computed in a scratchpad.

The one number here that is not in the journal is section 5 below: how U5's five
distinct solutions overlap U3's eight. It is measured, not asserted, and it is
the sharpest thing the stratification bought.

    .venv/bin/python experiments/p2_prog_r4_m3_evidence.py
"""
import json
import math
import os
import sys
from collections import Counter
from math import comb

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")
LIB = os.path.join(ROOT, "experiments", "programme_r4",
                   "u5_shift_library_admissible.json")

# Lucas & Kerswell 2015 Table IV: the |s| band the eight named rows live in.
BAND = (0.295, 0.707)
# The matching predicate of record (Ban 2): a convergence is a recovery only if
# it matches a named row on BOTH T and s to within this. Reused here as the
# clustering tolerance, so "distinct" is never finer than "recovered".
TOL = 0.05

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-62s %s" % ("ok" if ok else "FAIL", name, detail))


def wrap_abs(s):
    """|s| on the circle: the domain is 2*pi periodic, so |s|=6.18 is 0.10."""
    a = abs(float(s)) % (2.0 * math.pi)
    return min(a, 2.0 * math.pi - a)


def in_band(s):
    return BAND[0] <= s <= BAND[1]


def fisher_two_sided(a, b, c, d):
    """Fisher exact, from scratch -- no scipy dependency added for one number."""
    n = a + b + c + d
    def p(x):
        return comb(a + b, x) * comb(c + d, a + c - x) / comb(n, a + c)
    lo, hi = max(0, a + c - (c + d)), min(a + b, a + c)
    p0 = p(a)
    return sum(p(x) for x in range(lo, hi + 1) if p(x) <= p0 * (1 + 1e-12))


def cluster(attempts):
    """Group convergences into distinct solutions at the matching tolerance."""
    out = []
    for a in sorted(attempts, key=lambda a: a["T_converged"]):
        for c in out:
            if (abs(c[0]["T_converged"] - a["T_converged"]) <= TOL
                    and abs(c[0]["S"] - a["S"]) <= TOL):
                c.append(a)
                break
        else:
            out.append([a])
    return out


def main():
    with open(os.path.join(D, "p2_prog_r4_m3_v1.json")) as fh:
        u5 = json.load(fh)
    with open(os.path.join(D, "p2_prog_r4_g1_v1.json")) as fh:
        u3 = json.load(fh)
    with open(LIB) as fh:
        lib = json.load(fh)

    a5, a3 = u5["attempts"], u3["attempts"]
    for a in a5:
        a["S"] = wrap_abs(a["s_converged"])
        a["S_seed"] = wrap_abs(a["s_seed"])
    for a in a3:
        a["S"] = wrap_abs(a["s_converged"])
        a["S_seed"] = wrap_abs(a["s_seed"])
    ok5 = [a for a in a5 if a["success"]]
    ok3 = [a for a in a3 if a["success"]]

    # ---------------------------------------------------------------- 1. headline
    print("\n=== 1. the headline, as the milestone banked it ===")
    m = u5["milestone"]
    check("M3 = DELIVERED on all five pre-committed clauses",
          m["answer"] == "DELIVERED" and all(m["clauses"].values()),
          f"{sum(m['clauses'].values())}/5")
    check("100 attempts, 9 converged to tol=1e-8, 0 recovered a named row",
          (m["n_attempts"] == 100 and m["n_converged_to_tol"] == 9
           and m["n_recovered"] == 0 and len(a5) == 100
           and len(ok5) == 9 and sum(a["recovered_named_orbit"] for a in a5) == 0),
          f"converged {len(ok5)}, recovered "
          f"{sum(a['recovered_named_orbit'] for a in a5)}")
    check("G1 is not re-answered here",
          "UNDER-RESOURCED" in m["does_not_reanswer_G1"]
          and u3["gate"]["answer"] != "NO",
          f"U3 banked {u3['gate']['answer']!r}")

    # ------------------------------------------------------------ 2. the H fork
    # AMENDMENT 5 named two rival readings of U3's in-band drought and said which
    # observation would kill which. Both are settled below.
    print("\n=== 2. H-supply vs H-hard, the pre-registered fork ===")
    sup = u5["seed"]["seed_supply_funnel"]
    n_ib_seed_5 = sum(1 for a in a5 if in_band(a["S_seed"]))
    n_ib_seed_3 = sum(1 for a in a3 if in_band(a["S_seed"]))
    check("H-supply's premise was repaired: in-band spend 31 -> 60",
          n_ib_seed_3 == 31 and n_ib_seed_5 == 60 == m["n_seeded_in_published_band"],
          f"U3 {n_ib_seed_3}, U5 {n_ib_seed_5} (quota {sup['quota_by_stratum']['P']})")
    check("H-supply is REFUTED: 60 in-band seeds, still 0 recoveries",
          n_ib_seed_5 >= 50 and m["n_recovered"] == 0,
          "more supply did not produce the predicted recovery")

    # The per-stratum table the TECHNICAL quotes, pinned so prose cannot drift
    # from the ledger. Wilson, because 0/10 is not "0%".
    def wilson(k, n, z=1.96):
        if n == 0:
            return 0.0, 0.0
        p, den = k / n, 1 + z * z / n
        c = (p + z * z / (2 * n)) / den
        h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
        return 100 * max(0.0, c - h), 100 * (c + h)

    print(f"    {'stratum':>8} {'U5':>7} {'Wilson 95%':>18} {'median seed R':>15}")
    strat = {}
    for k in "PLMH":
        g = [a for a in a5 if a["stratum"] == k]
        kk = sum(a["success"] for a in g)
        strat[k] = (kk, len(g))
        lo, hi = wilson(kk, len(g))
        print(f"    {k:>8} {kk:3d}/{len(g):<3d} [{lo:7.1f}, {hi:5.1f}] "
              f"{np.median([a['R_seed'] for a in g]):15.4f}")
    check("per-stratum yield P 5/60, L 4/20, M 0/10, H 0/10",
          strat == {"P": (5, 60), "L": (4, 20), "M": (0, 10), "H": (0, 10)},
          "every interval overlaps its U3 counterpart; no stratum resolves at 95%")

    # Raw rates confound "the band is hard" with "these seeds are worse", which is
    # the same shape of confound the whole programme is about. Match on R first.
    pool = [(a["S_seed"], a["R_seed"], bool(a["success"])) for a in a3 + a5]
    edges = np.quantile([p[1] for p in pool], np.linspace(0, 1, 5))
    t_ib = t_ob = c_ib = c_ob = 0
    print(f"    {'R bin (pooled quartile)':>26}   in-band      out-of-band")
    for i, (lo, hi) in enumerate(zip(edges[:-1], edges[1:])):
        # Top bin closed on the right, or the worst-R attempt is silently
        # discarded and the pooled denominators no longer sum to 200.
        last = i == len(edges) - 2
        g = [p for p in pool if lo <= p[1] and (p[1] <= hi if last else p[1] < hi)]
        ib = [p for p in g if in_band(p[0])]
        ob = [p for p in g if not in_band(p[0])]
        t_ib += len(ib); t_ob += len(ob)
        c_ib += sum(p[2] for p in ib); c_ob += sum(p[2] for p in ob)
        print(f"    [{lo:.4f}, {hi:.4f})        "
              f"{sum(p[2] for p in ib):2d}/{len(ib):<3d}      "
              f"{sum(p[2] for p in ob):2d}/{len(ob):<3d}")
    p_fisher = fisher_two_sided(c_ib, t_ib - c_ib, c_ob, t_ob - c_ob)
    check("matched-R pooled yield: in-band 6/91 vs out-of-band 17/109",
          (c_ib, t_ib, c_ob, t_ob) == (6, 91, 17, 109)
          and t_ib + t_ob == 200,
          f"{c_ib}/{t_ib} = {c_ib/t_ib:.1%} vs {c_ob}/{t_ob} = {c_ob/t_ob:.1%}, "
          f"all {t_ib + t_ob} attempts kept")
    check("H-hard is FAVOURED but NOT resolved: Fisher two-sided p = 0.073",
          abs(p_fisher - 0.073) < 0.001 and p_fisher > 0.05,
          f"p = {p_fisher:.4f}, above 0.05 -- this is a lean, not a result")

    # ------------------------------------------------- 3. the band-exit replication
    # Recorded from U3's banked data BEFORE U5 ran (addendum line 525: 13 of 14
    # convergences moved |s| toward zero or stayed). U5 is an independent arm.
    print("\n=== 3. Newton leaves the band (replication, not post-hoc) ===")
    ib_conv = [a for a in ok5 if in_band(a["S_seed"])]
    left = [a for a in ib_conv if not in_band(a["S"])]
    print(f"    {'seed |s|':>10} {'final |s|':>10}   left band?")
    for a in ib_conv:
        print(f"    {a['S_seed']:10.4f} {a['S']:10.4f}   "
              f"{'yes' if not in_band(a['S']) else 'no'}")
    check("4 of 5 in-band convergences left the band",
          len(ib_conv) == 5 and len(left) == 4, f"{len(left)}/{len(ib_conv)}")
    check("8 of 9 convergences finished at |s| < 0.15",
          sum(1 for a in ok5 if a["S"] < 0.15) == 8,
          f"range {min(a['S'] for a in ok5):.4f}-{max(a['S'] for a in ok5):.4f}")
    # The addendum's wording, "13 of 14 moved |s| toward zero or stayed there",
    # is loose: only 9 of 14 decreased. The measured invariant is the ENDPOINT,
    # and on that reading it is 13 of 14 -- exactly the form U5 replicates.
    check("U3's arm agrees on the endpoint: 13 of 14 finished at |s| < 0.15",
          sum(1 for a in ok3 if a["S"] < 0.15) == 13
          and sum(1 for a in ok3 if a["S"] <= a["S_seed"] + 1e-12) == 9,
          "independent 100-attempt arm; note only 9 of 14 strictly decreased, so "
          "the addendum's 'moved toward zero' is the endpoint claim, not a monotone one")

    # --------------------------------------------------------- 4. cost, not bought
    print("\n=== 4. the stall exit spent FEWER epochs, and bought nothing ===")
    r = u5["resourcing"]
    check("2,104 epochs vs U3's 4,629 -- 45.5%, no iterations bought",
          r["epochs_spent"] == 2104 and r["u3_epochs_spent"] == 4629
          and r["epochs_spent"] < r["u3_epochs_spent"],
          f"{r['epochs_spent'] / r['u3_epochs_spent']:.1%}; caps, tol and window "
          "asserted identical to U3")
    st = r["stall_exit"]
    check("stall exit replayed on U3's ledger cuts 0 of 14, margin 6.9x",
          st["u3_convergences_lost"] == 0 and st["margin_factor"] > 6.9,
          f"worst true convergence moved {st['worst_convergence_ratio_at_k_ge_K']:.4f} "
          f"vs the 0.5 threshold")
    n_iters5 = sum(a["n_iters"] for a in a5)
    check("epoch total agrees with the per-attempt ledger", n_iters5 == 2104,
          f"sum of n_iters = {n_iters5}")

    # ------------------------------------------- 5. what the strata actually bought
    # NOT in the journal: the overlap between U5's solutions and U3's. The
    # milestone is DELIVERED with 0 recoveries, so the honest question is whether
    # a stratified budget found anything a globally-ranked one had not.
    print("\n=== 5. U5's solutions against U3's (measured here, new) ===")
    c5, c3 = cluster(ok5), cluster(ok3)
    novel = []
    print(f"    {'T':>9} {'|s|':>8}  found  strata          status")
    for c in c5:
        T, s = c[0]["T_converged"], c[0]["S"]
        hit = [d for d in c3 if abs(d[0]["T_converged"] - T) <= TOL
               and abs(d[0]["S"] - s) <= TOL]
        if not hit:
            novel.append(c)
        print(f"    {T:9.4f} {s:8.4f}  {len(c):5d}  "
              f"{','.join(sorted({a['stratum'] for a in c})):<14s}  "
              f"{'re-find of U3' if hit else 'NEW -- U3 never found it'}"
              f"{'   [IN BAND]' if in_band(s) else ''}")
    check("9 convergences collapse to 5 distinct solutions", len(c5) == 5,
          f"{len(ok5)} convergences, {len(c5)} distinct at tol {TOL}")
    check("U3's 14 collapse to 8 distinct on the same predicate", len(c3) == 8,
          "R0 flags this count as disputed; recomputed here, it is 8")
    check("exactly 1 of U5's 5 is new relative to U3", len(novel) == 1,
          f"T = {novel[0][0]['T_converged']:.4f}, "
          f"|s| = {novel[0][0]['S']:.4f}, stratum {novel[0][0]['stratum']}, "
          f"anchor {novel[0][0]['anchor']}")
    check("the one new solution is the only U5 solution inside the band",
          in_band(novel[0][0]["S"])
          and sum(1 for c in c5 if in_band(c[0]["S"])) == 1,
          "stratifying by shift is what put a seed where it could be found")
    check("4 of 5 are re-finds -- cross-run, not just within-run",
          len(c5) - len(novel) == 4,
          "this is what R2 (deflation) is queued against")

    # R0 fixed the reported metric before this landed: distinct orbits per
    # core-hour, because per-attempt rate counts re-finds as successes.
    ch5 = u5["magnitudes"]["wall_seconds"] * u5["magnitudes"]["workers"] / 3600.0
    ch3 = u3["magnitudes"]["wall_seconds"] * u3["magnitudes"]["workers"] / 3600.0
    check("R0's metric: U5 = 5/57.04 = 0.0877 vs U3 = 8/144.69 = 0.0553",
          abs(ch5 - 57.04) < 0.01 and abs(ch3 - 144.69) < 0.01
          and len(c5) / ch5 > len(c3) / ch3,
          f"U5 {len(c5)/ch5:.4f} vs U3 {len(c3)/ch3:.4f} distinct/core-hour; "
          "R0's own baseline quotes 134.45 core-hours for U3 -- unreconciled")

    # ------------------------------------------------ 6. option (c), priced honestly
    print("\n=== 6. what carrying an m unknown would actually unlock ===")
    cand = lib["candidates"]
    mnz = [x for x in cand if x["m"] != 0]
    mnz_band = [x for x in mnz if in_band(wrap_abs(x["s"]))]
    check("334 of 575 in-window candidates are dropped for m != 0 (58.1%)",
          len(mnz) == 334 == sup["candidates_dropped_for_nonzero_y_shift"]
          and len(cand) == 575,
          f"{len(mnz)}/{len(cand)} = {len(mnz)/len(cand):.1%}")
    check("but only 1 of those 334 is in the published band",
          len(mnz_band) == 1,
          "option (c) is not a band fix, it is the |s| > 0.9 fix")

    # ------------------------------------------------------------- 7. the funnel
    print("\n=== 7. supply, quota and spend ===")
    mine = u5["seed"]["mining"]["rule"]
    check("exhaustive re-mine: 913,301 -> 103,844 anchored -> 75,873 taken",
          (mine["n_strict_local_minima"] == 913301
           and mine["n_anchored_all_depths"] == 103844
           and mine["n_taken"] == 75873),
          f"{mine['n_taken'] / mine['n_taken_by_U2_for_comparison']:.1f}x U2's "
          f"{mine['n_taken_by_U2_for_comparison']}")
    check("the R_red prune is lossless, not a re-ranking",
          mine["R_red_max_taken"] < 0.25, "R_red <= R pointwise, so R_red >= 0.25 "
          "cannot hide an R < 0.25")
    check("every stratum met its quota; no shortfall redistribution fired",
          (sup["realised_by_stratum"] == sup["quota_by_stratum"]
           == sup["realised_before_shortfall"] and sup["short_of_requested"] == 0),
          f"P/L/M/H = {tuple(sup['realised_by_stratum'][k] for k in 'PLMH')} "
          f"from supply {tuple(sup['supply_by_stratum'][k] for k in 'PLMH')}")
    check("one named row supplied nothing in band: UPO34 = 0",
          sup["per_row_in_band_supply"]["UPO34"] == 0,
          "the reservoir is exhausted, so this is a fact about the DNS, not the rule")
    reg = u5["seed"]["mining"]["regeneration_checks"]
    check("block-parallel regeneration reproduced U2's serial one bit for bit",
          (reg["bitwise_check_against_U2_serial_regenerate"]["bit_for_bit"]
           and reg["bitwise_check_against_U2_serial_regenerate"][
               "max_abs_difference"] == 0.0
           and reg["exactness_check_against_U2_banked_library"]["exact"]),
          f"{reg['bitwise_check_against_U2_serial_regenerate']['n_indices_checked']}"
          " indices, max|diff| 0.0")

    # ------------------------------------------------------------- 8. the controls
    print("\n=== 8. controls, planted before the run ===")
    ctl = u5["controls"]
    check("P recovered, N did not, R recovered -- the apparatus can still see",
          (ctl["fired_as_planted"] and not ctl["failures"]
           and ctl["P"]["recovered"] and not ctl["N"]["recovered"]
           and ctl["R"]["recovered"]),
          "a null with a dead control would be uninterpretable")
    print("\n=== 9. reasons, for completeness ===")
    print("    U5:", dict(Counter(a["reason"] for a in a5)))
    print("    U3:", dict(Counter(a["reason"] for a in a3)))

    n_fail = sum(1 for _, ok, _ in CHECKS if not ok)
    print(f"\n{len(CHECKS) - n_fail}/{len(CHECKS)} checks passed")
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
