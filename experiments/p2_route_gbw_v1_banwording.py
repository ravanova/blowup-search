"""Leg 184 / Route-GBW v1 -- the GA ban's lift condition, pinned so coarsening cannot satisfy it.

WHAT THIS RUNNER IS FOR.  Leg 184 changed one string in `plan_of_record.py`: the lift
condition of the ban on "any GA compute on an unvalidated fitness".  A prose statement that
the loophole is closed decays at the rate of memory (banked lesson 68), so the closure is
stated here as an EXECUTABLE PREDICATE and applied to two inputs:

  * the PRE-EDIT wording, quoted verbatim from merge base 2d89233 -- must FAIL the predicate,
  * the POST-EDIT wording, read live out of `plan_of_record.BANNED` -- must PASS it.

A predicate that only ever sees the string it was written for is not a check (banked lesson
90: a control that cannot come out differently is not a control).  The pre-edit string is the
negative control, and it is the reason this file can fail.

WHAT IT DOES NOT DO.  No GA compute.  No solver compute.  No import of anything under `ga/`
or `solver/`.  The ban this leg edits is still IN FORCE after the edit, and this runner
asserts that too -- closing a loophole in a ban's wording must not lift the ban.

Run:  .venv/bin/python experiments/p2_route_gbw_v1_banwording.py
Data: writeup/data/p2_route_gbw_v1_banwording.json
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from plan_of_record import BANNED, banned_now  # noqa: E402

OUT = ROOT / "writeup" / "data" / "p2_route_gbw_v1_banwording.json"

# The ban this leg edits, identified by its SUBJECT (element 0), which this leg did not touch.
BAN_SUBJECT_HEAD = "any GA compute on an unvalidated fitness"

# The lift condition as it stood from leg 49 (commit 9f33c42) until this leg, verbatim.
# This is the NEGATIVE CONTROL: the predicate below must reject it.
PRE_EDIT_LIFT = (
    "never -- only a re-run of the six-property gate that PASSES on a repaired fitness")

# Leg 160's measured coarsening, from experiments/journal/leg_160.md.  The frozen
# configuration is n = 201 coarse / 401 fine; the loophole is the n = 101 / 151 run.
FROZEN_COARSE, FROZEN_FINE = 201, 401
LOOPHOLE_COARSE, LOOPHOLE_FINE = 101, 151


def pins_resolution(lift_text):
    """Does this lift condition pin the resolution the six-property gate must pass at?

    Four independent requirements, each checkable, each able to fail:
      (R1) the frozen resolution is NAMED, both grids;
      (R2) it is named as a PIN, not as an example;
      (R3) coarser grids are EXCLUDED explicitly (this is the loophole leg 160 measured);
      (R4) the excluded coarsening is named by its numbers, so a reader cannot mistake
           which run is being ruled out.
    Returns (verdict, per-requirement dict).
    """
    t = lift_text
    checks = {
        "R1_frozen_resolution_named": (
            str(FROZEN_COARSE) in t and str(FROZEN_FINE) in t),
        "R2_named_as_a_pin": bool(re.search(r"\bPINNED\b", t)),
        "R3_coarser_excluded": bool(
            re.search(r"COARSER[^.]*does NOT lift", t)),
        "R4_loophole_named_by_number": (
            str(LOOPHOLE_COARSE) in t and str(LOOPHOLE_FINE) in t),
    }
    return all(checks.values()), checks


def leg_160_numbers_agree():
    """Cross-check every leg-160 number this leg quotes against leg 160's own journal.

    The numbers in the pinned clause are read off a landed artifact, not off memory.  If
    leg 160's journal does not contain them verbatim, this leg has misquoted its
    predecessor and says so here rather than in prose.
    """
    journal = (ROOT / "experiments" / "journal" / "leg_160.md").read_text()
    quoted = {
        "P3_at_loophole_grid": "0.02007528568401651",
        "P2_at_loophole_grid": "1.0000",
        "P3_at_frozen_grid": "0.3421493449940881",
        "rho_inf_at_n201": "4.790972900601766e-11",
        "rho_inf_at_n101": "4.640571829290985e-13",
    }
    return {k: (v, v in journal) for k, v in quoted.items()}


def main():
    ga_bans = [(w, l) for w, l in BANNED if w.startswith(BAN_SUBJECT_HEAD)]
    assert len(ga_bans) == 1, f"expected exactly one GA-compute ban, found {len(ga_bans)}"
    subject, lift = ga_bans[0]

    post_ok, post_checks = pins_resolution(lift)
    pre_ok, pre_checks = pins_resolution(PRE_EDIT_LIFT)

    in_force = {w for w, _ in banned_now()}
    lift_head = lift.split(" --")[0].strip()
    quoted = leg_160_numbers_agree()

    # --- the assertions.  Any one of these failing is a real failure of this leg. ---
    assert post_ok, f"POST-EDIT lift condition does not pin the resolution: {post_checks}"
    assert not pre_ok, (
        "NEGATIVE CONTROL FAILED: the PRE-EDIT wording also passes the pinning predicate, "
        "so the predicate is not measuring the edit")
    assert not pre_checks["R1_frozen_resolution_named"], pre_checks
    assert not pre_checks["R3_coarser_excluded"], pre_checks
    assert subject in in_force, "the GA ban is no longer in force -- this leg must not lift it"
    assert lift_head == "never", (
        f"the lift head changed from 'never' to '{lift_head}' -- this leg must not make the "
        "ban liftable by a stage")
    assert all(ok for _, ok in quoted.values()), (
        f"a number quoted in the pinned clause is not in leg 160's journal: {quoted}")
    assert len(BANNED) == 24 and len(in_force) == 17, (
        f"ban inventory changed: {len(BANNED)} total / {len(in_force)} in force "
        "(expected 24 / 17) -- this leg edits ONE clause and adds or removes no ban")

    payload = {
        "leg": 184,
        "route": "GBW",
        "what": ("the GA ban's lift condition in plan_of_record.py, pinned to the frozen "
                 "resolution so a coarser grid cannot satisfy it"),
        "ban_subject_unchanged": subject,
        "lift_condition_pre_edit": PRE_EDIT_LIFT,
        "lift_condition_post_edit": lift,
        "pinning_predicate": {
            "post_edit_pins_resolution": post_ok,
            "post_edit_checks": post_checks,
            "pre_edit_pins_resolution": pre_ok,
            "pre_edit_checks": pre_checks,
        },
        "frozen_configuration": {
            "n_coarse": FROZEN_COARSE, "n_fine": FROZEN_FINE,
            "wall_model": "2d", "seed": 0, "per_gene": 9, "refine": 4,
            "source": "experiments/journal/leg_160.md (leg 59's configuration, unchanged)",
        },
        "excluded_coarsening": {
            "n_coarse": LOOPHOLE_COARSE, "n_fine": LOOPHOLE_FINE,
            "unrepaired_leg49_fitness_score_there": "6/6",
            "unrepaired_leg49_fitness_score_at_frozen": "5/6",
            "P3_worst_abs_slope_minus_1_at_loophole_grid": 0.02007528568401651,
            "P3_worst_abs_slope_minus_1_at_frozen_grid": 0.3421493449940881,
            "rho_inf_at_n201": 4.790972900601766e-11,
            "rho_inf_at_n101": 4.640571829290985e-13,
            "frozen_eps_grid_bottom": 1e-11,
            "mechanism": ("coarsening drops ||A||_w and with it the residual floor ||rho||_inf "
                          "below the frozen eps grid's bottom, so P3's probe measures the "
                          "fitness's own arithmetic noise instead of the injected defect; the "
                          "property stops failing without anything being repaired"),
        },
        "leg_160_numbers_verified_against_its_journal": {
            k: {"value": v, "found_in_leg_160_journal": ok} for k, (v, ok) in quoted.items()},
        "ban_still_in_force": subject in in_force,
        "lift_head": lift_head,
        "ban_inventory": {"total": len(BANNED), "in_force": len(in_force)},
        "no_landed_gate_answer_altered": {
            "leg_49": {"scored_at": "n=201/401", "result": "4/6", "unchanged": True},
            "leg_59": {"scored_at": "n=201/401", "result": "5/6", "unchanged": True},
            "leg_160": {"scored_at": "n=201/401", "result": "NO", "unchanged": True},
            "note": ("all three ran at the now-pinned configuration, so pinning ratifies "
                     "what they already did; leg 160's own NO stays NO"),
        },
        "compute": {"ga": False, "solver": False,
                    "note": "text predicate only; imports nothing from ga/ or solver/"},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n")

    print("Leg 184 / Route-GBW v1 -- GA ban lift condition")
    print(f"  pre-edit  pins resolution: {pre_ok}   {pre_checks}")
    print(f"  post-edit pins resolution: {post_ok}  {post_checks}")
    print(f"  ban still in force: {subject in in_force};  lift head: '{lift_head}'")
    print(f"  ban inventory: {len(BANNED)} total / {len(in_force)} in force")
    print(f"  leg 160 numbers verified against its journal: "
          f"{sum(ok for _, ok in quoted.values())}/{len(quoted)}")
    print(f"  wrote {OUT.relative_to(ROOT)}")
    print("ALL ASSERTIONS PASS")


if __name__ == "__main__":
    main()
