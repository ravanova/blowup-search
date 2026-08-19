#!/usr/bin/env python3
"""Leg 413 / unit `L5-cmod` -- EVIDENCE for `writeup/data/p2_route_l5cmod_v1.json`.

`CORRECTIONS.md` SS45/SS49: every check below prints its CLASS.

  * `recompute-from-primary` -- re-runs the physics, or re-derives from a PRIMARY record this unit
    did not produce (`L5`'s artefact, `L5`'s code).  Can catch an error shared between this unit's
    artefact and this unit's own checker.
  * `re-read-own-artefact`   -- reads only what this unit wrote.  CANNOT, by construction, catch an
    error shared between the artefact and this script.  `ORCHESTRATION.md` SS6 clause 3 mandates
    exactly this blind spot; SS45 measured it at 32 of 49 scripts.

The two classes are TALLIED SEPARATELY and `N/N passed` is explicitly NOT treated as evidence.
`E6` MUTATES this script's own decision logic and REQUIRES it to fail, because a checker that has
never been shown to fail has not been shown to check.

Run:  OMP_NUM_THREADS=1 .venv/bin/python experiments/p2_route_l5cmod_v1_evidence.py
      (add `--fast` to skip E5, the ~9-minute discretisation-invariance re-run)
"""

import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "writeup" / "data" / "p2_route_l5cmod_v1.json"
L5_JSON = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"
ROW = "alpha=1|kappa=a_physical_frozen|DSS"

_spec = importlib.util.spec_from_file_location("l5cmod", ROOT / "experiments" / "p2_route_l5cmod_v1.py")
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

RESULTS = []


def check(name, cls, ok, detail):
    RESULTS.append({"name": name, "class": cls, "passed": bool(ok), "detail": detail})
    print("[%-24s] %-24s %s" % (cls, name, "PASS" if ok else "FAIL"))
    print("    %s" % detail)
    return ok


def main():
    doc = json.loads(ART.read_text())
    g, adj = doc["gate"], doc["gate_adjudication"]
    incs = g["increments_per_decade_curl_L32"]

    # -- E1 ------------------------------------------------------------------------------------
    core = {k: v for k, v in doc.items() if not k.startswith("_") and k != "self_hash"}
    core["self_hash"] = doc["self_hash"]
    recomputed = M.sha({k: v for k, v in doc.items() if not k.startswith("_") and k != "self_hash"})
    fields_ok = all(k in doc for k in ("gate", "gate_adjudication", "controls", "ceiling",
                                       "chain", "cost_own_footprint"))
    disclosures = [
        "DISCLOSURE" in doc["controls"]["X6_overlap"],
        "DISCLOSURE" in adj["measured_noise_floor"]["estimator_A_two_code_paths"],
        "DISCLOSURE_why_the_literal_rule_degenerated" in adj,
        adj["answer_by_literal_precommitted_rule_SS0_2"] == "UNDER-RESOURCED",
        doc["chain"]["links_moved"] == [],
    ]
    check("E1_artefact_shape", "re-read-own-artefact", fields_ok and all(disclosures),
          ("required blocks present=%s; the five disclosure invariants (X6 subsumption, noise "
           "estimator A understatement, SS0.2 degeneration, the raw UNDER-RESOURCED verdict "
           "preserved, links_moved empty) = %s. self_hash recomputes to %s (stored %s) -- note "
           "this proves only internal consistency and is NOT evidence about the physics."
           % (fields_ok, disclosures, recomputed[:8], doc["self_hash"][:8])))

    # -- E2 ------------------------------------------------------------------------------------
    K = M.load_l5_driver_constants()
    L5 = M.load_l5("evidence")
    spot = [1000.0, 1e5, 1e8]
    worst, tbl = 0.0, []
    for rho0 in spot:
        v = M.row(L5, rho0, K["ALPHA"], K["KAPPA"], K["N_S"], K["RES"])
        banked = [r for r in g["rows"] if r["rho0"] == rho0][0]
        rel = abs(v["curl_L32"] - banked["curl_L32"]) / banked["curl_L32"]
        tbl.append((rho0, v["curl_L32"], banked["curl_L32"], rel))
        worst = max(worst, rel)
    check("E2_ladder_reruns_bitwise", "recompute-from-primary", worst == 0.0,
          ("three rows of the gate ladder RE-RUN from L5's code in a fresh process: %s; max rel "
           "difference %.3e (bit-identical required, since the computation is deterministic)"
           % (["rho0=%g mine=%.10f banked=%.10f" % (a, b, c) for a, b, c, _ in tbl], worst)))

    # -- E3 ------------------------------------------------------------------------------------
    l5rows = json.loads(L5_JSON.read_text())["sweep"][ROW]["rows"]
    l5inc = [( (b["curl_L32"] - a["curl_L32"]) / math.log10(b["rho"] / a["rho"]) )
             for a, b in zip(l5rows[:-1], l5rows[1:])]
    s53 = [-263.078, -1.721, 0.404, 0.052]
    agree = all(abs(x - y) < 5e-4 * max(1.0, abs(y)) for x, y in zip(l5inc, s53))
    mine4 = [i["per_decade"] for i in incs[:4]]
    same = all(abs(x - y) < 1e-9 for x, y in zip(mine4, l5inc))
    check("E3_SS53_arithmetic_from_L5s_own_artefact", "recompute-from-primary", agree and same,
          ("re-derived from writeup/data/p2_route_l5_finite_energy_v1.json (a PRIMARY record this "
           "unit did not write): %s vs CORRECTIONS.md SS53's quoted %s -> agree=%s; and this unit's "
           "own first four bands reproduce them exactly -> %s. SS53's central arithmetic on THIS row "
           "is confirmed, including that the last two banked increments are POSITIVE."
           % (["%.6g" % v for v in l5inc], s53, agree, same)))

    # -- E4 ------------------------------------------------------------------------------------
    rows = g["rows"]
    re_inc = [((b["curl_L32"] - a["curl_L32"]) / math.log10(b["rho"] / a["rho"]))
              for a, b in zip(rows[:-1], rows[1:])]
    inc_ok = all(abs(x - i["per_decade"]) < 1e-18 for x, i in zip(re_inc, incs))
    floor = adj["measured_noise_floor"]["per_decade"]
    above = [i["per_decade"] for i in incs if abs(i["per_decade"]) > floor]
    ratios = [abs(above[k] / above[k + 1]) for k in range(3, len(above) - 1)]
    check("E4_increment_arithmetic_and_the_x100_law", "re-read-own-artefact",
          inc_ok and all(8.5 < r < 11.5 for r in ratios),
          ("per-decade increments re-derived from the banked rows: identical. Band-to-band ratios "
           "over the resolved bands beyond L5's reach = %s (each band is ~0.5 decade, so ~10 per "
           "band == ~100 per decade == rho^-2). THIS CHECK IS BLIND to any error shared between the "
           "artefact and this script -- it recomputes no physics."
           % ["%.3f" % r for r in ratios]))

    # -- E5 ------------------------------------------------------------------------------------
    if "--fast" in sys.argv:
        print("[skipped                ] E5_discretisation_invariance_of_the_increments (--fast)")
    else:
        base_lo = [r for r in rows if r["rho0"] == 1e4][0]["curl_L32"]
        base_hi = [r for r in rows if r["rho0"] == 1e6][0]["curl_L32"]
        base_pd = (base_hi - base_lo) / 2.0
        variants, worst_rel = {}, 0.0
        for tag, ns, res in (("n_s=12", 2 * K["N_S"], K["RES"]), ("RES_HI", K["N_S"], K["RES_HI"])):
            lo = M.row(L5, 1e4, K["ALPHA"], K["KAPPA"], ns, res)["curl_L32"]
            hi = M.row(L5, 1e6, K["ALPHA"], K["KAPPA"], ns, res)["curl_L32"]
            pd = (hi - lo) / 2.0
            variants[tag] = {"lo": lo, "hi": hi, "per_decade": pd,
                             "rel_vs_baseline": abs(pd / base_pd - 1.0)}
            worst_rel = max(worst_rel, variants[tag]["rel_vs_baseline"])
        check("E5_discretisation_invariance_of_the_increments", "recompute-from-primary",
              worst_rel < 0.05,
              ("POST-HOC control, added after X5 showed the ABSOLUTE value of c_mod carries a 0.391 "
               "s-quadrature error between n_s=6 and n_s=12 (4.5e-4 relative). The gate reads "
               "INCREMENTS, not the absolute value, so the question is whether the increment over "
               "the band rho0 1e4 -> 1e6 survives refinement. Baseline %.6e per decade; %s. Worst "
               "relative change %.3e. The 0.391 offset is a rho-INDEPENDENT systematic and cancels "
               "in the differences the gate reads -- measured, not asserted."
               % (base_pd, {k: "%.6e (rel %.2e)" % (v["per_decade"], v["rel_vs_baseline"])
                            for k, v in variants.items()}, worst_rel)))

    # -- E6: MUTATION.  The checker must FAIL on a planted logarithm. --------------------------
    planted = []
    c0, beta = 869.29, 0.05
    for k, r in enumerate([v["rho"] for v in rows]):
        planted.append({"rho": r, "curl_L32": c0 * (1.0 + beta * math.log(r))})
    pinc = [((b["curl_L32"] - a["curl_L32"]) / math.log10(b["rho"] / a["rho"]))
            for a, b in zip(planted[:-1], planted[1:])]
    pratios = [abs(pinc[k] / pinc[k + 1]) for k in range(3, len(pinc) - 1)]
    e4_would_pass = all(8.5 < r < 11.5 for r in pratios)
    x = np.log10([math.sqrt(a["rho"] * b["rho"]) for a, b in zip(planted[3:-1], planted[4:])])
    y = np.log10([abs(v) for v in pinc[3:]])
    A = np.vstack([x, np.ones_like(x)]).T
    slope_planted = float(np.linalg.lstsq(A, y, rcond=None)[0][0])
    real_slope = adj["decay_exponent_of_the_increments"]["slope"]
    check("E6_mutation_the_checker_must_fail", "recompute-from-primary",
          (not e4_would_pass) and abs(slope_planted) < 0.05 and abs(real_slope + 2.0) < 0.05,
          ("the SAME statistics applied to a SYNTHETIC c_mod = %.2f*(1 + %.2f ln rho) on the SAME "
           "rho ladder: E4's x100-per-decade test would return %s (must be False), and the decay "
           "exponent comes out %.4f (must be ~0), against %.4f (must be ~-2) on the real data. "
           "The instrument distinguishes the two hypotheses on identical sampling."
           % (c0, beta, e4_would_pass, slope_planted, real_slope)))

    # -- E7 ------------------------------------------------------------------------------------
    before = doc["L5_files_read_never_modified"]["before"]
    now = {}
    for nm, p in (("p2_route_l5_v1.py", M.L5_SRC), ("p2_route_l5_v1_driver.py", M.L5_DRV),
                  ("p2_route_l5_v1_evidence.py", M.L5_EVD),
                  ("p2_route_l5_finite_energy_v1.json", M.L5_JSON)):
        now[nm] = hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
    check("E7_L5_untouched_on_disk_now", "recompute-from-primary", now == before,
          ("L5's four files re-hashed from disk at evidence time against the hashes recorded before "
           "the run: %s. The instrument also replaces L5.checkpoint with a raising interlock, so "
           "L5's artefact cannot be written even by a coding error." % ("identical" if now == before
                                                                        else "CHANGED: %s" % now)))

    # -- E8 ------------------------------------------------------------------------------------
    c = doc["controls"]
    fired = {"X1": c["X1_reproduce_L5_banked_rows"]["passed"],
             "X2_planted_log_returns_YES": c["X2_planted_log_divergence_must_say_YES"]["fired_as_planted"],
             "X3_alpha=0.999": c["X3_planted_power_law_sign"]["cases"]["alpha=0.999"]["fired_as_planted"],
             "X3_alpha=1.001": c["X3_planted_power_law_sign"]["cases"]["alpha=1.001"]["fired_as_planted"],
             "X4_as_a_noise_floor": c["X4_exact_scale_invariance_noise_floor"]["passed"]}
    check("E8_controls_fired_as_planted_including_the_one_that_did_not",
          "re-read-own-artefact", fired["X1"] and fired["X2_planted_log_returns_YES"]
          and fired["X3_alpha=0.999"] and fired["X3_alpha=1.001"] and not fired["X4_as_a_noise_floor"],
          ("%s. X4 DID NOT FIRE AS PLANTED and that is REPORTED, not re-planted: the pure-power "
           "profile is NOT rho-independent, because T4 and T5 carry an intrinsic rho^-2 relative to "
           "T1..T3, so X4 measured no noise floor. What X4 DID establish -- that the pure power "
           "reproduces the entire ladder to 1e-7 -- identifies the MECHANISM of the rho^-2 decay, "
           "and the noise floor was measured elsewhere (adjudication, two estimators)." % fired))

    # -- tally ---------------------------------------------------------------------------------
    prim = [r for r in RESULTS if r["class"] == "recompute-from-primary"]
    own = [r for r in RESULTS if r["class"] == "re-read-own-artefact"]
    print("\n" + "=" * 96)
    print("TALLY BY CLASS (CORRECTIONS.md SS45) -- the two are NOT added together")
    print("  recompute-from-primary : %d/%d passed   %s"
          % (sum(r["passed"] for r in prim), len(prim), [r["name"] for r in prim]))
    print("  re-read-own-artefact   : %d/%d passed   %s"
          % (sum(r["passed"] for r in own), len(own), [r["name"] for r in own]))
    print("  N/N PASSED IS NOT EVIDENCE. The load-bearing checks are E2, E3, E5, E6, E7 "
          "(recompute-from-primary); E1, E4, E8 cannot see an error this unit's artefact and this "
          "script share.")
    print("  E6 is the only check that REQUIRES a failure, and it is the only one that shows the "
          "instrument can distinguish the two hypotheses at all.")
    print("=" * 96)
    print("GATE (literal SS0.2 machine verdict, preserved): %s"
          % adj["answer_by_literal_precommitted_rule_SS0_2"])
    print("GATE (adjudicated, disclosed)                  : %s" % adj["answer"])
    ok = all(r["passed"] for r in RESULTS)
    print("ALL CHECKS: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
