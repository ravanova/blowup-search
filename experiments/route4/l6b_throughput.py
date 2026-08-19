#!/usr/bin/env python3
"""Leg 406, unit `L6-b` -- ARTEFACT ADDENDUM: throughput, reported two ways.

The Conductor caught a real reporting defect mid-run and it is recorded here rather than
quietly fixed.  This unit reported "rate has eased to 0.848 it/s under the heavier sibling
load".  That figure was the CUMULATIVE average -- total iterations divided by total seconds
-- presented as if it were the CURRENT rate.  Two things were wrong with it:

  1. it attributes a whole-run average to the present moment; and
  2. worse, it HIDES the very contention it was being used to describe, because the fast
     pre-contention hours never leave the numerator.  A cumulative figure will keep
     understating a mid-run slowdown for the rest of the run, by construction.

The correction is a reporting fix only.  No gate wording, no pre-committed reading, and no
cost figure moves: core-hours are wall x cores MEASURED, and are unaffected by which rate is
quoted.  What moves is the projected finish time and any sentence containing the word "now".

This script therefore banks BOTH, each labelled, for every start:
  * `cumulative_it_per_s`   -- total k / total s, correct as a whole-run average and as the
                               denominator of the core-hour price;
  * `windowed_it_per_s`     -- a LADDER of trailing windows (500/1000/2000/4000 iterations),
                               correct for "what is it doing now" and for the ETA.

The ladder, not a single window, is deliberate, and it is this unit's one point of
refinement on the Conductor's framing (SS`dissent` below): at the reading that prompted the
correction the trailing-2000 figure (0.722) sat BELOW the trailing-500 and trailing-1000
figures (0.757, 0.759), i.e. throughput had partially RECOVERED inside the window.  A single
trailing window can mislead in the slow direction just as a cumulative average misleads in
the fast one.  Reporting the ladder lets a reader see the recovery instead of taking either
end of it on trust.

Idempotent: rerunning reproduces the same block and the same `self_hash`.

    .venv/bin/python experiments/route4/l6b_throughput.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "writeup" / "data" / "p2_route_l6b_v1.json"

WINDOWS = (500, 1000, 2000, 4000)


def rates(traj):
    """(cumulative it/s, {window: (actual_iters, seconds, it/s)}) from a k/sec trajectory."""
    k = [r[0] for r in traj]
    s = [r[1] for r in traj]
    K, S = k[-1], s[-1]
    cum = K / S if S > 0 else float("nan")
    win = {}
    for w in WINDOWS:
        cand = [(kk, ss) for kk, ss in zip(k, s) if kk >= K - w]
        if not cand:
            continue
        k0, s0 = cand[0]
        dk, ds = K - k0, S - s0
        if dk > 0 and ds > 0:
            win[str(w)] = dict(actual_iterations=int(dk), seconds=float(ds),
                               it_per_s=float(dk / ds))
    return float(cum), win


def main():
    d = json.loads(ART.read_text())

    per = {}
    for name, st in d["starts"].items():
        traj = st["trajectory_k_sec_J_ginf_gscaled"]
        cum, win = rates(traj)
        per[name] = dict(
            iterations=int(traj[-1][0]), seconds=float(traj[-1][1]),
            cumulative_it_per_s=cum,
            windowed_it_per_s_by_trailing_iterations=win,
            terminal_windowed_it_per_s_1000=win.get("1000", {}).get("it_per_s"),
            ratio_cumulative_over_windowed_1000=(
                cum / win["1000"]["it_per_s"] if "1000" in win else None),
        )

    d["throughput"] = dict(
        why=("A cumulative it/s average quoted as a current rate hides a mid-run slowdown by "
             "construction, because the fast pre-contention hours stay in the numerator.  "
             "Both figures are banked here, each labelled, so no reader has to guess which "
             "one a sentence meant."),
        definitions=dict(
            cumulative_it_per_s="total iterations / total seconds, over the whole run",
            windowed_it_per_s="trailing-window iterations / trailing-window seconds, at the "
                              "stated window length, from this run's own k/sec trajectory",
        ),
        per_start=per,
        contention=dict(
            this_units_footprint_cores=6,
            box_cores=12,
            footprint_note="3 worker processes x 2 threads each; unchanged for the whole run",
            ambient_load_average_range_observed=[11.2, 18.2],
            ambient_note=("load average is AMBIENT and includes three concurrent sibling "
                          "units; it is NOT this unit's consumption and is not divided out"),
            measured_step_at_a_sibling_launch=dict(
                before_it_per_s=1.178, after_it_per_s=0.712,
                loss_fraction=0.396,
                source="Conductor's measurement at 02:21 -> 02:26 BST",
                note="partial recovery to ~0.76 it/s observed afterwards"),
        ),
        correction_on_the_record=dict(
            what_this_unit_said="rate has eased to 0.848 it/s under the heavier sibling load",
            why_it_was_wrong=("0.848 was cumulative (6800/8017), not current; quoting it as a "
                              "present rate both mislabelled it and understated the very "
                              "contention it was invoked to describe, by ~10-15% at that "
                              "reading"),
            corrected_current_rate_at_that_reading_it_per_s=0.759,
            eta_before_correction="~07:25 BST", eta_after_correction="~07:57-08:00 BST",
            raised_by="Conductor, mid-run", scope="reporting only",
            what_did_NOT_move=["the gate wording", "the pre-committed reading in either "
                               "direction", "the 1.45 material-drop threshold",
                               "the measured wall clock", "the measured core-hours"],
        ),
        dissent=dict(
            agree=("the arithmetic is correct and independently reproduced from this run's "
                   "own trajectory field: cumulative 0.846, trailing-500 0.757, "
                   "trailing-1000 0.759, trailing-2000 0.722 it/s at k=6900"),
            refinement=("this unit reports a LADDER of trailing windows rather than one.  At "
                        "the same reading the trailing-2000 figure (0.722) is BELOW the "
                        "trailing-500 and -1000 figures (0.757/0.759) and the trailing-4000 "
                        "figure (0.837) is above all of them -- throughput fell at the "
                        "sibling launch and has partially recovered since.  A single trailing "
                        "window would report the fall and conceal the recovery, which is the "
                        "same class of error in the opposite direction."),
            unchanged=("for the COST price neither figure is used: core-hours are wall-clock "
                       "x cores held, measured directly.  The rate framing changes the ETA "
                       "and any sentence containing 'now', and nothing else."),
        ),
    )

    d.pop("self_hash", None)
    d["self_hash"] = hashlib.sha256(
        json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]
    ART.write_text(json.dumps(d, indent=1, sort_keys=True))
    print(f"throughput written; self_hash={d['self_hash']}")
    for n, v in per.items():
        w = v["windowed_it_per_s_by_trailing_iterations"]
        print(f"  {n:24s} k={v['iterations']:6d}  cumulative {v['cumulative_it_per_s']:.3f}  "
              + "  ".join(f"w{k}={w[k]['it_per_s']:.3f}" for k in sorted(w, key=int)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
