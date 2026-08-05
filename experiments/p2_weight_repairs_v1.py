"""Weight-repairs v1 (leg 50, prep/weight-repairs): the two named repairs from
TECHNICAL_P2_ROUTEC_PILOT_V0.md S4, re-run on the six-property viability gate.

Leg 49 (C-PILOT v0) named the fitness `log10(Y0/budget)` a genuine measurement -- gauge
invariant, tracking a known defect, a genuinely five-dimensional landscape, 8.6x over
the best hand-tuned weight -- and then FAILED its own frozen six-property gate 4/6.
Two of the six failures were diagnosed with a mechanism and a specific, non-research
repair (S4a, S4b):

  P2 (finite, 0.775 against >= 0.90): 9/40 roster weights returned no fitness, and
     EVERY one of them sat below a SECOND wall -- `lower_wall()`, already measured by
     leg 49 but never carried into the box. Repair: carry it, the way the analytic
     upper wall already is.

  P3 (monotone, worst |slope-1| = 0.366 against <= 0.05): the probe pushed every
     weight through ONE global eps grid and asked for the known answer (slope 1)
     everywhere on it -- but ||A||_w spans 1.69e8 (naive) to 3.37e5 (searched) across
     the roster, so a grid that is linear for one weight is already nonlinear for
     another. Repair: give every weight its OWN eps window, sized from its OWN
     ||A||_w, fixed BEFORE this run -- and report what the window buys (how many
     weights resolve, how well the resolved ones track slope 1) as a RESOLUTION,
     rather than assuming one grid was valid for all forty weights.

Both repairs are implemented in `solver/weight_search.py` (`in_box`, `FitnessEngine`,
`roster`, `defect_ladder`, `six_property_gate`) and gated in `test_weight_search.py`.
This script re-runs the FROZEN predicate -- same thresholds, same roster construction,
same resolutions (n=201/401) and search settings (per_gene=9, refine=4) as leg 49 --
so the before/after comparison is apples to apples. `plan_of_record.py` bans GA
compute until this gate PASSES, and even a pass today does not authorize running it:
that is recorded for the next planning pass, not acted on same-day (ORCHESTRATION.md
lane 6).

Writes writeup/data/p2_weight_repairs_v1.json.

Run: .venv/bin/python -u experiments/p2_weight_repairs_v1.py
"""

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from solver.weight_search import (                                    # noqa: E402
    BorderedCLM, DEFECT_EPS_DEFAULT, DEFECT_MIN_WINDOW, DEFECT_WINDOW_C,
    WALL_LOWER_DELTA, six_property_gate,
)

OUT = ROOT / "writeup" / "data" / "p2_weight_repairs_v1.json"
BEFORE_JSON = ROOT / "writeup" / "data" / "p2_route_c_pilot_v0.json"
N_COARSE, N_FINE = 201, 401


def main():
    t0 = time.time()
    res = {"route": "weight-repairs", "version": "v1",
           "question": "Do the two named repairs (TECHNICAL_P2_ROUTEC_PILOT_V0 S4a/b) "
                       "move the six-property viability gate, on the SAME frozen "
                       "predicate and the same known-answer object leg 49 used?"}

    before = json.loads(BEFORE_JSON.read_text()) if BEFORE_JSON.exists() else None
    if before is not None:
        res["before"] = {"source": str(BEFORE_JSON.relative_to(ROOT)),
                         "verdict": before["verdict"],
                         "properties": before["C0_4_gate"]["properties"]}
        print(f"[before] leg 49 verdict {before['verdict']}: " +
              ", ".join(f"{k}={'PASS' if v['pass'] else 'FAIL'}"
                        for k, v in before["C0_4_gate"]["properties"].items()))

    res["repair_constants"] = {
        "P2_wall_lower_delta": WALL_LOWER_DELTA,
        "P3_defect_window_c": DEFECT_WINDOW_C,
        "P3_defect_min_window": DEFECT_MIN_WINDOW,
        "P3_defect_eps_grid": list(DEFECT_EPS_DEFAULT),
        "note": "fixed in solver/weight_search.py BEFORE this run -- not tuned "
                "against this run's own numbers (the plan-of-record discipline leg 49 "
                "S4a named explicitly).",
    }

    gate = six_property_gate(BorderedCLM(n=N_COARSE), BorderedCLM(n=N_FINE),
                             n_random=32, seed=0, per_gene=9, refine=4)
    res["after"] = {"verdict": gate["verdict"], "gate": gate}
    print(f"\n[after]  repaired verdict {gate['verdict']}:")
    for k, v in gate["properties"].items():
        print(f"        {'PASS' if v['pass'] else 'FAIL'}  {k}: "
              + ", ".join(f"{a}={b}" for a, b in v.items() if a != "pass"))

    if before is not None:
        bp = before["C0_4_gate"]["properties"]
        ap = gate["properties"]
        res["delta"] = {
            "P2_finite_fraction": {"before": bp["P2_finite"]["finite_fraction"],
                                   "after": ap["P2_finite"]["finite_fraction"]},
            "P3_max_slope_error": {"before": bp["P3_monotone"]["max_slope_error"],
                                   "after": ap["P3_monotone"]["max_slope_error"]},
            "P3_violations": {"before": bp["P3_monotone"]["violations"],
                              "after": ap["P3_monotone"]["violations"]},
            "n_pass_before": int(sum(1 for v in bp.values() if v["pass"])),
            "n_pass_after": int(sum(1 for v in ap.values() if v["pass"])),
        }
        print(f"\n[delta]  P2 finite fraction {bp['P2_finite']['finite_fraction']:.3f} "
              f"-> {ap['P2_finite']['finite_fraction']:.3f}; "
              f"gate {res['delta']['n_pass_before']}/6 -> {res['delta']['n_pass_after']}/6")

    res["ga_run"] = False
    res["ga_reason"] = ("plan_of_record bans GA compute until this gate PASSES; even "
                        "a same-day PASS is recorded for the NEXT planning pass, not "
                        "acted on today (ORCHESTRATION.md lane 6, ban list in "
                        "plan_of_record.py).")
    res["ceiling"] = ("No link of the L1->L4 chain moved. This leg is engineering on "
                      "a fitness measured on CLM (closed form since 1985); it reports "
                      "a gate result, not a certificate.")
    res["elapsed_s"] = time.time() - t0
    OUT.write_text(json.dumps(res, indent=1))
    print(f"\nwrote {OUT}  ({res['elapsed_s']:.0f}s)")


if __name__ == "__main__":
    main()
