#!/usr/bin/env python3
"""Leg 406, unit `L6-b` -- ARTEFACT ADDENDUM: the terminal stationarity block.

`V-W6`'s recommendation, made binding by the Conductor mid-run and recorded in
`experiments/journal/leg_406.md` SS7.7 BEFORE the gate number existed: report the TERMINAL
`max_abs_grad` AND `scale_invariant_grad` at each of the three starts, not only rho and not
only J.  A residual reported at a point with a large scale-invariant gradient is a point on
a descent path, not a critical point, and the artefact must say so on its face.

This is a separate script rather than a change to `p2_route_l6b_v1.py` for one reason,
stated so it is not mistaken for convenience: THE PRODUCTION RUN WAS ALREADY LIVE when the
requirement arrived.  Editing the running module would not have affected the running
interpreter, and restarting the run to pick the edit up would have thrown away hours of the
gate's own budget.  Every number this script writes is COPIED from fields the run itself
banked (`starts.<name>.max_abs_grad`, `.scale_invariant_grad`, `.final_residual`,
`.coeff_norm`, `.iterations`, `.hit_maxiter`) -- it computes no new science, and the
comparison row for `L6` is read out of `L6`'s untouched artefact.

Idempotent: rerunning it reproduces the same block and the same `self_hash`.

    .venv/bin/python experiments/route4/l6b_terminal_stationarity.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "writeup" / "data" / "p2_route_l6b_v1.json"
L6_ART = ROOT / "writeup" / "data" / "p2_route_l6_profile_v1.json"

# a scale-invariant stationarity measure this large is not a critical point by any reading;
# fixed here rather than chosen against the numbers
NOT_CRITICAL = 1.0


def main():
    d = json.loads(ART.read_text())
    d6 = json.loads(L6_ART.read_text())

    l6_top = d6["ladder_results"]["B"][-1]
    l6_rows = {s["start"]: s for s in l6_top["starts"]}

    per = {}
    for name, st in d["starts"].items():
        per[name] = dict(
            J_terminal=st["final_residual"],
            smallest_J_over_the_run=st["smallest_residual_at_20000"],
            max_abs_grad=st["max_abs_grad"],
            scale_invariant_grad=st["scale_invariant_grad"],
            coeff_norm=st["coeff_norm"],
            iterations=st["iterations"],
            hit_maxiter=st["hit_maxiter"],
            is_a_critical_point=bool(st["scale_invariant_grad"] < NOT_CRITICAL),
        )

    still_descending = {
        n: bool(v["hit_maxiter"] and not v["is_a_critical_point"]) for n, v in per.items()
    }
    banked = per.get("banked_J4_minimiser", {})
    verdict = bool(banked.get("hit_maxiter") and not banked.get("is_a_critical_point", True))

    d["terminal_stationarity"] = dict(
        why=("V-W6's binding recommendation: a residual is not a result on its own.  The "
             "terminal gradient says whether the number is a critical point of the "
             "residual functional or a point on a descent path at which the budget ran "
             "out.  Reported for all three starts, whichever way the gate answers."),
        measure="scale_invariant_grad = ||x||_2 ||grad J||_2 / |J|, invariant under x -> t x "
                "(the objective is scale-invariant: leg_401.md SS7.3)",
        not_a_critical_point_above=NOT_CRITICAL,
        per_start=per,
        starts_still_descending_at_the_cap=still_descending,
        L6_same_quantities_at_its_own_J4_rung={
            n: dict(J=r["fun"], max_abs_grad=r["max_abs_grad"],
                    scale_invariant_grad=r["scale_invariant_grad"],
                    coeff_norm=r["coeff_norm"], nit=r["nit"],
                    hit_maxiter=r["hit_maxiter"])
            for n, r in l6_rows.items()},
        L6s_reported_minimum_was_never_a_critical_point=bool(
            l6_rows["continuation"]["scale_invariant_grad"] >= NOT_CRITICAL),
        L6s_reported_minimum_scale_invariant_grad=l6_rows["continuation"]["scale_invariant_grad"],
        L6s_reported_minimum_had_the_LARGEST_such_gradient_of_its_six_starts=bool(
            l6_rows["continuation"]["scale_invariant_grad"]
            == max(r["scale_invariant_grad"] for r in l6_rows.values())),
        finding=(
            "L6's reported branch-B minimum rho = 1.613811231995397 carries "
            f"||x|| ||grad J|| / |J| = {l6_rows['continuation']['scale_invariant_grad']:.1f}, "
            "the LARGEST of all six starts at its own J4 rung (the five seeds read "
            "4.65-16.58).  It is therefore NOT a critical point of the residual "
            "functional: it is the point at which an 800-iteration budget ran out on a "
            "descent path.  This is legible in L6's OWN BANKED ARTEFACT and was not "
            "stated by L6 or by the landing audit."
            + ("  THE SAME IS TRUE OF THIS UNIT AT 20,000: the banked_J4_minimiser start "
               "is still at the cap and still not a critical point, so this unit's own "
               "number is likewise a stopping point and NOT an infimum."
               if verdict else
               "  At 20,000 this unit's banked_J4_minimiser start did NOT end at the cap "
               "in a non-critical state, so the qualification above does not extend to "
               "this unit's own number in the same form; see per_start.")),
    )

    d.pop("self_hash", None)
    d["self_hash"] = hashlib.sha256(
        json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]
    ART.write_text(json.dumps(d, indent=1, sort_keys=True))
    print(f"terminal_stationarity written; self_hash={d['self_hash']}")
    for n, v in per.items():
        print(f"  {n:24s} J={v['J_terminal']!r:22s} |g|inf={v['max_abs_grad']:.4g}  "
              f"gscaled={v['scale_invariant_grad']:.4g}  "
              f"critical_point={v['is_a_critical_point']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
