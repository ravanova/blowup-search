"""PROG-R4 unit R0 -- THE METRIC, RE-DERIVED FROM THE ARTEFACTS.

Lane R (WALLS.md W7). This unit exists because two numbers in the programme's
own summary did not survive contact with the artefacts, and because a
*concurrent session then transcribed U5's own numbers into WALLS.md's prose*.
A transcription is not a measurement. ORCHESTRATION.md 3e: re-derive every
number from writeup/data/*.json and the banked ledgers, NEVER from prose.

WHAT THIS SCRIPT MEASURES, independently of U5 and of WALLS.md:

  (i)  CORE-HOURS. WALLS.md first quoted 134.45 for U3, then (commit 5c6d495)
       replaced it with 144.69 and called the first figure a defect to be
       "reconciled against the JSON, not against prose". Both numbers are
       re-derived here from p2_prog_r4_g1_v1.json alone. They are BOTH correct
       and they measure DIFFERENT things.

  (ii) THE DISTINCT COUNT. The equivalence rule is not this script's to choose:
       experiments/p2_prog_r4_m3_evidence.py section 5 is the arbiter, and its
       rule is re-implemented here verbatim (see CLUSTER_RULE below) rather
       than imported, so that agreement is evidence rather than tautology.
       The count is then stressed: three linkage conventions, 20,000 random
       orderings, and a tolerance sweep, because the implemented rule is a
       GREEDY LEADER rule and greedy leader rules are not equivalence
       relations -- whether that matters here is a measurement, not an opinion.

 (iii) SEED OVERLAP between U3 and U5, never previously measured. The metric is
       reported per run; if the two runs share seeds, a per-run count of
       distinct orbits is not a count of distinct orbits the PROGRAMME gained.

NOTHING IS RE-RUN. No DNS, no mining, no Newton step. Read-only against:
  writeup/data/p2_prog_r4_g1_v1.json          (U3, the baseline)
  writeup/data/p2_prog_r4_m3_v1.json          (U5)
  experiments/programme_r4/u5_m3_converged_orbits.npz   (U5's converged states)

CEILING. Nothing here moves an L1->L4 link. A better metric does not make a
Clay statement more likely; it makes the questions affordable, which is a
different and lesser thing. Clay stays ~0.05%.

  .venv/bin/python experiments/programme_r4/r0_metric.py [--write]
"""
import hashlib
import itertools
import json
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "writeup", "data")
U3_JSON = os.path.join(DATA, "p2_prog_r4_g1_v1.json")
U5_JSON = os.path.join(DATA, "p2_prog_r4_m3_v1.json")
NPZ = os.path.join(ROOT, "experiments", "programme_r4",
                   "u5_m3_converged_orbits.npz")
OUT = os.path.join(DATA, "p2_prog_r4_r0r1_v1.json")

# ---------------------------------------------------------------------------
# The equivalence rule, quoted VERBATIM from experiments/p2_prog_r4_m3_evidence.py
# (the arbiter named in this unit's commission). Reproduced as a string so the
# write-ups can quote the rule they were measured under, and re-implemented
# below rather than imported, so that reproducing "8" is a check and not a
# tautology.
CLUSTER_RULE = """\
# experiments/p2_prog_r4_m3_evidence.py, lines 35-53 and 70-81, verbatim:

# Lucas & Kerswell 2015 Table IV: the |s| band the eight named rows live in.
BAND = (0.295, 0.707)
# The matching predicate of record (Ban 2): a convergence is a recovery only if
# it matches a named row on BOTH T and s to within this. Reused here as the
# clustering tolerance, so "distinct" is never finer than "recovered".
TOL = 0.05

def wrap_abs(s):
    \"\"\"|s| on the circle: the domain is 2*pi periodic, so |s|=6.18 is 0.10.\"\"\"
    a = abs(float(s)) % (2.0 * math.pi)
    return min(a, 2.0 * math.pi - a)

def cluster(attempts):
    \"\"\"Group convergences into distinct solutions at the matching tolerance.\"\"\"
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
"""

TOL = 0.05
TWO_PI = 2.0 * math.pi

CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-64s %s" % ("ok" if ok else "FAIL", name, detail))
    return bool(ok)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def wrap_abs(s):
    a = abs(float(s)) % TWO_PI
    return min(a, TWO_PI - a)


# --- the three clusterings -------------------------------------------------
def cluster_leader(pts, tol=TOL, order=None):
    """The implemented rule: greedy, leader-anchored, input sorted by T."""
    seq = sorted(pts, key=lambda a: a["T"]) if order is None else [pts[i] for i in order]
    out = []
    for a in seq:
        for c in out:
            if abs(c[0]["T"] - a["T"]) <= tol and abs(c[0]["S"] - a["S"]) <= tol:
                c.append(a)
                break
        else:
            out.append([a])
    return out


def cluster_single_linkage(pts, tol=TOL):
    """Transitive closure of the same predicate -- the equivalence relation the
    greedy rule is an approximation of."""
    n = len(pts)
    par = list(range(n))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for i in range(n):
        for j in range(i + 1, n):
            if (abs(pts[i]["T"] - pts[j]["T"]) <= tol
                    and abs(pts[i]["S"] - pts[j]["S"]) <= tol):
                par[find(i)] = find(j)
    return len({find(i) for i in range(n)})


def cluster_complete_linkage(pts, tol=TOL):
    """Join only if within tol of EVERY member -- the strictest reading."""
    out = []
    for a in sorted(pts, key=lambda x: x["T"]):
        for c in out:
            if all(abs(b["T"] - a["T"]) <= tol and abs(b["S"] - a["S"]) <= tol
                   for b in c):
                c.append(a)
                break
        else:
            out.append([a])
    return len(out)


def points(cur):
    return [{"att": a["attempt"], "anchor": a["anchor"],
             "T": a["T_converged"], "S": wrap_abs(a["s_converged"]),
             "res": a["final_residual"]}
            for a in cur["attempts"] if a["success"]]


def seed_key(a):
    """A seed's fingerprint. R_seed is a float carried to full precision, so a
    triple match on (T_seed, s_seed, R_seed) identifies the same candidate."""
    return (a["T_seed"], a["s_seed"], a["R_seed"])


def analyse():
    with open(U3_JSON) as fh:
        u3 = json.load(fh)
    with open(U5_JSON) as fh:
        u5 = json.load(fh)

    res = {"unit": "R0", "programme": "PROG-R4", "lane": "R", "wall": "W7"}
    res["cluster_rule_verbatim"] = CLUSTER_RULE
    res["provenance"] = {
        "u3_json": {"path": "writeup/data/p2_prog_r4_g1_v1.json",
                    "sha256": sha256(U3_JSON)},
        "u5_json": {"path": "writeup/data/p2_prog_r4_m3_v1.json",
                    "sha256": sha256(U5_JSON)},
        "u5_npz": {"path": "experiments/programme_r4/u5_m3_converged_orbits.npz",
                   "sha256": sha256(NPZ)},
        "arbiter_of_the_equivalence_rule":
            "experiments/p2_prog_r4_m3_evidence.py section 5",
        "nothing_rerun": "no DNS, no mining, no Newton step; read-only",
    }

    # ------------------------------------------------------ (i) core-hours
    print("\n=== R0(i)  CORE-HOURS, both figures re-derived from the SAME JSON ===")
    ch = {}
    for tag, cur in (("U3", u3), ("U5", u5)):
        stage_s = cur["magnitudes"]["wall_seconds"]
        workers = cur["magnitudes"]["workers"]
        att_s = sum(a["wall_seconds"] for a in cur["attempts"])
        ch[tag] = {
            "stage_elapsed_seconds": stage_s,
            "stage_elapsed_hours": stage_s / 3600.0,
            "workers": workers,
            "pool_reservation_core_hours": stage_s * workers / 3600.0,
            "attempt_cpu_seconds": att_s,
            "attempt_cpu_core_hours": att_s / 3600.0,
            "pool_utilisation": att_s / (stage_s * workers),
            "fields": {
                "pool_reservation":
                    "magnitudes.wall_seconds * magnitudes.workers / 3600",
                "attempt_cpu": "sum(attempts[].wall_seconds) / 3600",
                "elapsed": "magnitudes.wall_seconds / 3600",
            },
        }
        print("  %s: elapsed %.4f h x %d workers = %.4f  |  sum(attempts[].wall_seconds) = %.4f  |  utilisation %.4f"
              % (tag, stage_s / 3600.0, workers, stage_s * workers / 3600.0,
                 att_s / 3600.0, att_s / (stage_s * workers)))
    res["core_hours"] = ch

    check("U3 pool-reservation core-hours reproduce WALLS.md's 144.69",
          abs(ch["U3"]["pool_reservation_core_hours"] - 144.69) < 0.005,
          "%.4f = 52087.95185184479 s x 10 / 3600" % ch["U3"]["pool_reservation_core_hours"])
    check("U3's 134.45 is NOT prose: it is sum(attempts[].wall_seconds)/3600",
          abs(ch["U3"]["attempt_cpu_core_hours"] - 134.45) < 0.005,
          "%.4f core-hours over 100 attempt rows" % ch["U3"]["attempt_cpu_core_hours"])
    check("U5 pool-reservation core-hours reproduce WALLS.md's 57.04",
          abs(ch["U5"]["pool_reservation_core_hours"] - 57.04) < 0.005,
          "%.4f = 25665.83147907257 s x 8 / 3600" % ch["U5"]["pool_reservation_core_hours"])
    check("the two units did NOT reserve at the same width (10 vs 8 workers)",
          u3["magnitudes"]["workers"] != u5["magnitudes"]["workers"],
          "U3 %d, U5 %d -- so 'core-hour' means WORKER-hour, not core-hour"
          % (u3["magnitudes"]["workers"], u5["magnitudes"]["workers"]))
    check("physical core count is NOT a field in either JSON",
          not any("core" in k.lower() for k in u3["resourcing"])
          and not any(isinstance(v, (int, float)) and "core" in k.lower()
                      for k, v in u5["resourcing"].items()),
          "reported as a MISSING ARTEFACT FIELD; NOT estimated (3d)")

    # ------------------------------------------------ (ii) the distinct count
    print("\n=== R0(ii)  THE DISTINCT COUNT, under the arbiter's own rule ===")
    dist = {}
    for tag, cur in (("U3", u3), ("U5", u5)):
        p = points(cur)
        cl = cluster_leader(p)
        rng = random.Random(20260813)
        idx = list(range(len(p)))
        orders = set()
        for _ in range(20000):
            rng.shuffle(idx)
            orders.add(len(cluster_leader(p, order=list(idx))))
        pairs = sorted(((max(abs(a["T"] - b["T"]), abs(a["S"] - b["S"])), a, b)
                        for a, b in itertools.combinations(p, 2)),
                       key=lambda x: x[0])
        merged = [x for x in pairs if x[0] <= TOL]
        unmerged = [x for x in pairs if x[0] > TOL]
        sizes = sorted((len(c) for c in cl), reverse=True)
        dist[tag] = {
            "n_convergences": len(p),
            "n_distinct_leader_greedy_implemented": len(cl),
            "n_distinct_single_linkage": cluster_single_linkage(p),
            "n_distinct_complete_linkage": cluster_complete_linkage(p),
            "counts_over_20000_random_orderings": sorted(orders),
            "cluster_sizes": sizes,
            "n_convergences_on_replicated_solutions":
                sum(n for n in sizes if n > 1),
            "n_replicated_solutions": sum(1 for n in sizes if n > 1),
            "n_singleton_solutions": sum(1 for n in sizes if n == 1),
            "clusters": [{"T": c[0]["T"], "abs_s": c[0]["S"], "n": len(c),
                          "attempts": [x["att"] for x in c],
                          "anchors": sorted({x["anchor"] for x in c})}
                         for c in cl],
            "widest_accepted_merge": {
                "chebyshev_distance": merged[-1][0],
                "as_multiple_of_tol": merged[-1][0] / TOL,
                "pair": [merged[-1][1]["att"], merged[-1][2]["att"]],
                "dT": abs(merged[-1][1]["T"] - merged[-1][2]["T"]),
                "d_abs_s": abs(merged[-1][1]["S"] - merged[-1][2]["S"]),
            } if merged else None,
            "narrowest_failed_merge": {
                "chebyshev_distance": unmerged[0][0],
                "as_multiple_of_tol": unmerged[0][0] / TOL,
                "pair": [unmerged[0][1]["att"], unmerged[0][2]["att"]],
                "T": [unmerged[0][1]["T"], unmerged[0][2]["T"]],
                "abs_s": [unmerged[0][1]["S"], unmerged[0][2]["S"]],
                "dT": abs(unmerged[0][1]["T"] - unmerged[0][2]["T"]),
                "d_abs_s": abs(unmerged[0][1]["S"] - unmerged[0][2]["S"]),
            } if unmerged else None,
            "tolerance_sweep": {("%.3f" % t): len(cluster_leader(p, tol=t))
                                for t in (0.01, 0.02, 0.03, 0.04, 0.05, 0.06,
                                          0.07, 0.08, 0.10, 0.15, 0.20, 0.30)},
        }
        d = dist[tag]
        print("  %s: %d convergences -> %d distinct (leader-greedy = single = complete: %s)"
              % (tag, d["n_convergences"], d["n_distinct_leader_greedy_implemented"],
                 d["n_distinct_leader_greedy_implemented"]
                 == d["n_distinct_single_linkage"]
                 == d["n_distinct_complete_linkage"]))
        print("      sizes %s ; widest accepted merge %.6f (%.3fx TOL) ; narrowest failed merge %.6f (%.3fx TOL)"
              % (d["cluster_sizes"],
                 d["widest_accepted_merge"]["chebyshev_distance"],
                 d["widest_accepted_merge"]["as_multiple_of_tol"],
                 d["narrowest_failed_merge"]["chebyshev_distance"],
                 d["narrowest_failed_merge"]["as_multiple_of_tol"]))
    res["distinct"] = dist

    check("U3's 14 convergences give 8 distinct under the arbiter's rule",
          dist["U3"]["n_distinct_leader_greedy_implemented"] == 8,
          "AGREES with WALLS.md's 8")
    check("U5's 9 convergences give 5 distinct under the same rule",
          dist["U5"]["n_distinct_leader_greedy_implemented"] == 5,
          "AGREES with WALLS.md's 5")
    check("the count is not an artefact of the greedy rule's ordering",
          dist["U3"]["counts_over_20000_random_orderings"] == [8]
          and dist["U5"]["counts_over_20000_random_orderings"] == [5],
          "20,000 random orderings each, one value each")
    check("greedy = single-linkage = complete-linkage on both runs",
          (dist["U3"]["n_distinct_leader_greedy_implemented"]
           == dist["U3"]["n_distinct_single_linkage"]
           == dist["U3"]["n_distinct_complete_linkage"] == 8)
          and (dist["U5"]["n_distinct_leader_greedy_implemented"]
               == dist["U5"]["n_distinct_single_linkage"]
               == dist["U5"]["n_distinct_complete_linkage"] == 5),
          "the partition is an equivalence class here, not a greedy accident")
    check("U3's 8 sits between a 0.9594x-TOL merge and a 1.2883x-TOL non-merge",
          abs(dist["U3"]["widest_accepted_merge"]["as_multiple_of_tol"] - 0.9594) < 5e-4
          and abs(dist["U3"]["narrowest_failed_merge"]["as_multiple_of_tol"] - 1.2883) < 5e-4,
          "attempts %s merge at dT=%.6f; attempts %s do not at dT=%.6f"
          % (dist["U3"]["widest_accepted_merge"]["pair"],
             dist["U3"]["widest_accepted_merge"]["dT"],
             dist["U3"]["narrowest_failed_merge"]["pair"],
             dist["U3"]["narrowest_failed_merge"]["dT"]))

    # WALLS.md's ORIGINAL prose argument, checked against the artefact.
    prose = {
        "walls_md_claim": "10 of U3's 14 convergences landed on three solutions",
        "measured_convergences_on_replicated_solutions":
            dist["U3"]["n_convergences_on_replicated_solutions"],
        "measured_replicated_solutions": dist["U3"]["n_replicated_solutions"],
        "measured_singletons": dist["U3"]["n_singleton_solutions"],
        "why_the_prose_argument_failed":
            "WALLS.md argued 10 convergences over 3 replicated solutions leaves "
            "4, which cannot yield 5 more, so 8 was unreconcilable. The premise "
            "is off by one: the measured figure is 9 over 3 (cluster sizes "
            "4+3+2), leaving 5 singletons, and 3+5 = 8 exactly. The count was "
            "never in doubt; the prose's own input number was wrong.",
    }
    res["walls_md_prose_argument"] = prose
    print("\n  WALLS.md prose: '10 of 14 on three solutions'. MEASURED: %d of 14 on %d, %d singletons -> %d + %d = %d."
          % (prose["measured_convergences_on_replicated_solutions"],
             prose["measured_replicated_solutions"], prose["measured_singletons"],
             prose["measured_replicated_solutions"], prose["measured_singletons"],
             prose["measured_replicated_solutions"] + prose["measured_singletons"]))
    check("WALLS.md's '10 of 14 on three solutions' is off by one; measured 9",
          dist["U3"]["n_convergences_on_replicated_solutions"] == 9
          and dist["U3"]["n_replicated_solutions"] == 3
          and dist["U3"]["n_singleton_solutions"] == 5,
          "4+3+2 = 9 replicated, 5 singletons, 3+5 = 8 -- the arithmetic closes")

    # ------------------------------------------------ (iii) the seed overlap
    print("\n=== R0(iii)  SEED OVERLAP -- never previously measured ===")
    k3 = {seed_key(a): a for a in u3["attempts"]}
    shared = [a for a in u5["attempts"] if seed_key(a) in k3]
    shared_conv = []
    for a in shared:
        b = k3[seed_key(a)]
        if a["success"]:
            shared_conv.append({
                "u5_attempt": a["attempt"], "u3_attempt": b["attempt"],
                "u3_also_converged": bool(b["success"]),
                "bit_identical_output": bool(
                    a["T_converged"] == b["T_converged"]
                    and a["s_converged"] == b["s_converged"]
                    and a["final_residual"] == b["final_residual"]
                    and a["n_iters"] == b["n_iters"]),
                "T_converged": a["T_converged"],
            })
    # which of U5's clusters survive if the shared seeds are removed
    p5_new = [x for x in points(u5)
              if seed_key(next(a for a in u5["attempts"]
                               if a["attempt"] == x["att"])) not in k3]
    n5_new_seed_clusters = len(cluster_leader(p5_new))
    overlap = {
        "u5_seeds_already_spent_by_u3": len(shared),
        "u5_attempts": len(u5["attempts"]),
        "u5_convergences_on_a_shared_seed": len(shared_conv),
        "u5_convergences": 9,
        "bit_identical_re_executions":
            sum(1 for x in shared_conv if x["bit_identical_output"]),
        "detail": shared_conv,
        "u5_distinct_from_seeds_u3_had_not_spent": n5_new_seed_clusters,
        "matching_key": "(T_seed, s_seed, R_seed) at full float precision",
    }
    res["seed_overlap"] = overlap
    print("  %d of %d U5 seeds were already spent by U3; %d of U5's 9 convergences are on them, %d bit-identical."
          % (overlap["u5_seeds_already_spent_by_u3"], 100,
             overlap["u5_convergences_on_a_shared_seed"],
             overlap["bit_identical_re_executions"]))
    check("57 of U5's 100 seeds had already been spent by U3",
          overlap["u5_seeds_already_spent_by_u3"] == 57)
    check("5 of U5's 9 convergences are bit-identical re-executions of U3 attempts",
          overlap["u5_convergences_on_a_shared_seed"] == 5
          and overlap["bit_identical_re_executions"] == 5,
          "same seed, same deterministic solver, same output to the last digit")
    check("on U5-only seeds the distinct count is 4, not 5",
          n5_new_seed_clusters == 4,
          "one of U5's five solutions was reached ONLY by re-running U3's seeds")

    # --------------------------------------------- the metric, all variants
    print("\n=== R0  THE METRIC: distinct orbits per core-hour ===")
    n3 = dist["U3"]["n_distinct_leader_greedy_implemented"]
    n5 = dist["U5"]["n_distinct_leader_greedy_implemented"]
    # 4 of U5's 5 are re-finds of U3's set (measured by the arbiter script and
    # re-measured here): only the cluster with no U3 counterpart is new.
    p3 = points(u3)
    c3 = cluster_leader(p3)
    c5 = cluster_leader(points(u5))
    novel5 = [c for c in c5
              if not any(abs(d[0]["T"] - c[0]["T"]) <= TOL
                         and abs(d[0]["S"] - c[0]["S"]) <= TOL for d in c3)]
    variants = {}
    for name, key in (("pool_reservation", "pool_reservation_core_hours"),
                      ("attempt_cpu", "attempt_cpu_core_hours"),
                      ("elapsed_wall_hours", "stage_elapsed_hours")):
        variants[name] = {
            "U3": n3 / ch["U3"][key], "U5": n5 / ch["U5"][key],
            "U5_over_U3": (n5 / ch["U5"][key]) / (n3 / ch["U3"][key]),
            "denominator_field": ch["U3"]["fields"].get(
                {"pool_reservation": "pool_reservation",
                 "attempt_cpu": "attempt_cpu",
                 "elapsed_wall_hours": "elapsed"}[name]),
        }
        print("  %-20s U3 %.4f  U5 %.4f  ratio %.3f"
              % (name, variants[name]["U3"], variants[name]["U5"],
                 variants[name]["U5_over_U3"]))
    headline = {
        "convention": "pool_reservation (WALLS.md's own, and U5's own)",
        "U3": {"numerator": n3,
               "numerator_field":
                   "clusters of attempts[].{T_converged, s_converged} at TOL=0.05",
               "denominator": ch["U3"]["pool_reservation_core_hours"],
               "denominator_field":
                   "magnitudes.wall_seconds (52087.95185184479) * "
                   "magnitudes.workers (10) / 3600",
               "distinct_orbits_per_core_hour": n3 / ch["U3"]["pool_reservation_core_hours"]},
        "U5": {"numerator": n5,
               "numerator_field":
                   "clusters of attempts[].{T_converged, s_converged} at TOL=0.05",
               "denominator": ch["U5"]["pool_reservation_core_hours"],
               "denominator_field":
                   "magnitudes.wall_seconds (25665.83147907257) * "
                   "magnitudes.workers (8) / 3600",
               "distinct_orbits_per_core_hour": n5 / ch["U5"]["pool_reservation_core_hours"]},
    }
    cumulative = {
        "what_it_counts": "orbits NEW TO THE PROGRAMME, not new to the run",
        "U3": {"n": n3, "per_core_hour": n3 / ch["U3"]["pool_reservation_core_hours"]},
        "U5": {"n": len(novel5),
               "per_core_hour": len(novel5) / ch["U5"]["pool_reservation_core_hours"],
               "the_one_new_solution": {"T": novel5[0][0]["T"],
                                        "abs_s": novel5[0][0]["S"],
                                        "attempt": novel5[0][0]["att"],
                                        "anchor": novel5[0][0]["anchor"]}},
        "U5_over_U3": (len(novel5) / ch["U5"]["pool_reservation_core_hours"])
                      / (n3 / ch["U3"]["pool_reservation_core_hours"]),
    }
    res["metric"] = {"headline": headline, "variants": variants,
                     "cumulative_reading": cumulative}
    print("  cumulative (new to the PROGRAMME): U3 %.4f  U5 %.4f  ratio %.3f"
          % (cumulative["U3"]["per_core_hour"], cumulative["U5"]["per_core_hour"],
             cumulative["U5_over_U3"]))

    check("headline U3 = 8 / 144.6888 = 0.0553 distinct orbits per core-hour",
          abs(headline["U3"]["distinct_orbits_per_core_hour"] - 0.0553) < 5e-5,
          "%.6f -- AGREES with WALLS.md" % headline["U3"]["distinct_orbits_per_core_hour"])
    check("headline U5 = 5 / 57.0352 = 0.0877 distinct orbits per core-hour",
          abs(headline["U5"]["distinct_orbits_per_core_hour"] - 0.0877) < 5e-5,
          "%.6f -- AGREES with WALLS.md" % headline["U5"]["distinct_orbits_per_core_hour"])
    check("U5 exceeds U3 under every derivable core-hour convention",
          all(v["U5_over_U3"] > 1.0 for v in variants.values()),
          "ratios %s" % {k: round(v["U5_over_U3"], 3) for k, v in variants.items()})
    check("under the CUMULATIVE reading U5 is 3.15x WORSE than U3, not better",
          cumulative["U5_over_U3"] < 1.0,
          "1 new orbit / 57.04 core-hours = %.4f against U3's %.4f"
          % (cumulative["U5"]["per_core_hour"], cumulative["U3"]["per_core_hour"]))

    # -------------------------------------------- the npz, and what it cannot do
    print("\n=== R0  WHAT THE BANKED STATES CAN AND CANNOT SETTLE ===")
    npz_note = {
        "u5_states_banked": True,
        "u3_states_banked": False,
        "consequence":
            "U3's distinct count of 8 is the headline numerator, and U3's "
            "converged STATES are not banked anywhere in this repository -- "
            "only U5's are (u5_m3_converged_orbits.npz, 9 fields). So the "
            "count can be tested only in the (T, |s|) invariant pair, never "
            "in state space. The narrowest failed merge sits at 1.288x the "
            "tolerance, in T alone, and nothing banked can adjudicate it.",
        "second_limit":
            "Even for U5, the npz banks ONE snapshot per converged attempt at "
            "an unspecified phase along the orbit, so two snapshots of the "
            "SAME orbit need not be close in state space. Measured: attempts "
            "64 and 76 (one cluster) agree to 0.0014 in shift-invariant "
            "spectrum, while attempts 40 and 52 (also one cluster) differ by "
            "0.199 -- more than attempts 52 and 45, which the rule separates. "
            "The snapshots therefore CANNOT validate the equivalence rule, "
            "and are reported as an instrument limit rather than as support.",
        "what_would_have_to_be_banked":
            "U3's 14 converged states, plus a phase-aligned distance (minimise "
            "over the continuous x-shift and over time-translation along the "
            "orbit). That needs the stepper, i.e. new compute, and is NOT "
            "estimated here.",
    }
    res["state_space_limit"] = npz_note
    try:
        import numpy as np
        z = np.load(NPZ)
        names = sorted(z.files)
        spec = {n: np.abs(np.fft.fft2(z[n])) for n in names}

        def rel(a, b):
            return float(np.linalg.norm(spec[a] - spec[b]) / np.linalg.norm(spec[a]))
        n64 = [n for n in names if n.startswith("attempt064")][0]
        n76 = [n for n in names if n.startswith("attempt076")][0]
        n40 = [n for n in names if n.startswith("attempt040")][0]
        n52 = [n for n in names if n.startswith("attempt052")][0]
        n45 = [n for n in names if n.startswith("attempt045")][0]
        npz_note["measured_spectral_distances"] = {
            "att64_att76_same_cluster": rel(n64, n76),
            "att40_att52_same_cluster": rel(n40, n52),
            "att52_att45_different_clusters": rel(n52, n45),
        }
        check("banked snapshots cannot validate the rule: same-cluster 0.199 > cross-cluster 0.089",
              rel(n40, n52) > rel(n52, n45),
              "att40-att52 %.4f (one cluster) vs att52-att45 %.4f (two clusters)"
              % (rel(n40, n52), rel(n52, n45)))
        check("U3's converged states are not banked anywhere",
              len(names) == 9 and all(n.startswith("attempt") for n in names),
              "the npz holds U5's 9 fields and nothing of U3's")
    except ImportError:            # pragma: no cover
        print("  (numpy unavailable -- spectral cross-check skipped)")

    # ------------------------------------------------------- the verdict
    res["verdict"] = {
        "core_hours":
            "AGREE with WALLS.md's 144.69 for U3 and 57.04 for U5, and "
            "DISAGREE with WALLS.md's account of why 134.45 arose. 134.45 is "
            "not prose: it is sum(attempts[].wall_seconds)/3600 = 134.4475, "
            "from the same JSON, and it is the figure U3's own INDEX row "
            "reports. The two numbers are the pool reservation and the "
            "attempt CPU time; U3's pool utilisation was 0.9292 and U5's "
            "0.9820, which is the whole of the difference.",
        "distinct_count":
            "AGREE with WALLS.md's 8 for U3 and 5 for U5, re-derived "
            "independently under the arbiter's own rule, and robust to "
            "linkage convention, to 20,000 orderings, and to the tolerance "
            "over 0.05-0.10. DISAGREE with the prose input WALLS.md's "
            "original argument used: '10 of 14 on three solutions' is "
            "measured as 9.",
        "the_finding":
            "The metric is confirmed and its INFERENCE is not. Per-run "
            "distinct-orbits-per-core-hour still counts a CROSS-RUN re-find "
            "as a success -- the same defect it was introduced to remove, one "
            "level up. 57 of U5's 100 seeds had already been spent by U3, 5 "
            "of U5's 9 convergences are bit-identical re-executions of U3 "
            "attempts, and one of U5's five distinct solutions was reached "
            "ONLY by re-running U3's seeds. Under the cumulative reading -- "
            "orbits new to the programme -- U5 is 0.0175 against U3's 0.0553.",
        "retraction":
            "'Lane R's first measured win' is RETRACTED AS AN INFERENCE. The "
            "arithmetic stands: U5 is above U3 under all three derivable "
            "core-hour conventions, by 1.27x to 1.59x. What does not stand is "
            "reading that as Lane R's machinery having improved. The metric "
            "is per-run, the two runs are not independent samples, and on the "
            "only reading that tracks what the programme actually gained U5 "
            "is 3.15x worse. Lane R may claim a cheaper run; it may not claim "
            "a better orbit finder on this evidence.",
        "ceiling":
            "TIER 2. No L1->L4 link moved. A best-in-field orbit finder does "
            "not move a Clay link -- it makes the questions affordable, which "
            "is a DIFFERENT AND LESSER THING. Clay stays ~0.05%.",
    }
    for k, v in res["verdict"].items():
        print("\n  [%s] %s" % (k.upper(), v))
    return res


def main():
    res = analyse()
    bad = [n for n, ok, _ in CHECKS if not ok]
    print("\n%d/%d R0 checks passed" % (len(CHECKS) - len(bad), len(CHECKS)))
    if bad:
        print("FAILED: " + ", ".join(bad))
    if "--write" in sys.argv:
        doc = {}
        if os.path.exists(OUT):
            with open(OUT) as fh:
                doc = json.load(fh)
        doc.setdefault("unit", "R0+R1")
        doc.setdefault("programme", "PROG-R4")
        doc.setdefault("lane", "R")
        doc.setdefault("wall", "W7")
        doc.setdefault("kind", "MEASUREMENT (metric reconciliation + flatness abort)")
        doc.setdefault("clay_movement", "none -- no L1-L4 link moved by this unit")
        doc["r0"] = res
        with open(OUT, "w") as fh:
            json.dump(doc, fh, indent=1, sort_keys=True)
        print("wrote %s" % OUT)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
