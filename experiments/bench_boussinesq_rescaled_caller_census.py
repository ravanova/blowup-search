"""Live caller census for `solver/boussinesq_rescaled.py`, with the two scopes kept apart.

WHY THIS FILE EXISTS
--------------------
Three legs have now answered "who calls this module?" and they did not all answer the same
question:

* **Leg 205** (`526bce4`, branch-only) *assumed* which callers exist.  That was the original
  sin: an assumed caller set cannot drift, because it was never measured.
* **Leg 221** (repair `d2d9769`, final `7e58419`) grepped once and banked a registry, in
  service of a specific and *historical* question -- **which artifacts were banked in the
  pre-repair world, and could therefore carry contamination from
  `odd_field_x_slope`'s two silent-fabrication mechanisms?**
* **Leg 233** (`43dce32`) grepped again, ~130 legs later, and found the registry had drifted
  by exactly two entries relative to *today's importer set*
  (`experiments/p2_route_tscx_v1.py`, `experiments/p2_route_s1gr_v1.py`; three counting leg
  233's own new test file).  It **reported and did not repair** -- correctly, per
  `ORCHESTRATION.md` §7b, and correctly on the substance too.

**THE DISTINCTION THIS MODULE ENFORCES, AND IT IS THE WHOLE POINT.**  Leg 221's registry is
**not wrong**.  It is complete over its own scope -- pre-repair-banked artifacts -- and stale
only as a census of today's callers.  Every drifted entry was first committed *after* the
repair commit `d2d9769`, and contamination is a claim about values banked in the *pre-repair*
world, so **no post-repair importer can carry contamination**.  Adding the drifted entries to
leg 221's registry would not fix anything; it would convert a correct frozen answer into an
incoherent half-census.

So there are two questions, and the repo had one word ("registry") for both:

  FROZEN  -- "which artifacts were banked pre-repair?"    Historical.  Answered.  Never changes.
  LIVE    -- "which files import this module today?"      Drifts every time a leg lands.

`FROZEN_PREREPAIR_BANKED` below is the first, quoted from leg 221 and cited to its commits;
it is **read-only evidence and must not be edited**.  `live_importers()` is the second, and it
is **computed, never transcribed** -- nobody re-types a list that a grep can produce.
`CLASSIFICATION` maps every live importer into a labelled scope, and
`test_boussinesq_rescaled_caller_census.py` fails loudly when a live importer appears that no
scope claims.  That test is the mechanism; the lists here are only its bookkeeping.

SCOPE OF THE GREP
-----------------
Deliberately identical to leg 233's `census()`
(`experiments/p2_route_bvrrv_v1_postrepair.py`), so the two numbers are comparable rather
than merely similar: the same import regex, the same directory exclusions, the module itself
excluded, paths relative to the repo root, sorted.  Do not "improve" the pattern without
saying so in a journal -- a silently widened scope makes every historical comparison below a
lie.

The scope excludes files that NAME the module in a string without importing it.  That
exclusion is not incidental, it is a correctness property: `solver/target_selection.py`,
`experiments/p2_route_sirc_v1_census.py` and `test_boussinesq_rescaled_status.py` all mention
the module path in text (the last one reads it as a *file*, to check its docstring) and none
of them calls it.  They are correctly absent from leg 221's registry and from leg 233's live
list, and the test pins that they stay absent -- see `NAMED_BUT_NOT_IMPORTING`.

NOT A LEG.  Bench repair work under `ORCHESTRATION.md` §3 priority 2.  No scientific claim, no
measurement, no figure, no `L1 -> L4` link moved, Clay stays ~0.05%.

Run it:  `.venv/bin/python experiments/bench_boussinesq_rescaled_caller_census.py`
         (prints a JSON report; writes nothing, banks nothing)
"""

from __future__ import annotations

import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODULE_PATH = "solver/boussinesq_rescaled.py"

# Leg 221's repair.  The line that separates the two scopes: an importer first committed after
# this commit did not exist when any pre-repair artifact was banked, so it cannot carry
# contamination, whatever else it does.
REPAIR_REF = "d2d9769"
LEG_221_FINAL_REF = "7e58419"
LEG_233_REF = "43dce32"

# Verbatim from leg 233's `census()`.  Anchored (`^\s*`) so a module name appearing inside a
# string, a comment, or prose does not count as an import.
IMPORT_PATTERN = re.compile(
    r"^\s*(from\s+solver\.boussinesq_rescaled\s+import|import\s+solver\.boussinesq_rescaled)",
    re.M,
)
SKIP_DIRS = {".git", ".venv", "__pycache__", "Papers", ".claude"}


# ---------------------------------------------------------------------------
# SCOPE 1 -- FROZEN.  Leg 221's registry.  Historical, complete over its own question, and
# NOT to be extended.  Quoted from `experiments/p2_route_bvrr_v1_repair.py::BANKED` at
# `d2d9769` / `7e58419`, and re-published by leg 233 at `43dce32` as
# `writeup/data/p2_route_bvrrv_v1_postrepair.json::census.leg_221_registry_scripts`.
# The test asserts this list against that banked JSON, so the frozen scope is pinned to
# landed evidence rather than to this file's good intentions.
# ---------------------------------------------------------------------------
FROZEN_PREREPAIR_BANKED = (
    "experiments/p2_route_brs_v1_status_audit.py",
    "experiments/p2_route_g_v1_collapse.py",
    "experiments/p2_route_k_v1_port.py",
    "experiments/p2_route_l_v1_precond.py",
    "experiments/spike1_stepC_gate.py",
    "writeup/3_spikes/spike1_stepB_evidence.py",
)

FROZEN_SCOPE_NOTE = (
    "Six scripts whose `writeup/data/*.json` artifacts were banked BEFORE leg 221's repair "
    "commit d2d9769. This is the contamination scope and nothing else: leg 221 compared "
    "256,233 calls across these six artifacts and found 0 moved. The set is closed by "
    "history and MUST NOT be extended -- a later importer is by construction outside the "
    "question this set answers."
)


# ---------------------------------------------------------------------------
# SCOPE 2 -- LIVE.  Every file that imports the module today, each assigned a label.
# `live_importers()` computes the set; this table only says what each member IS.
# A live importer absent from every bucket below is DRIFT and the test goes red.
# ---------------------------------------------------------------------------
CLASSIFICATION = {
    # --- pre-repair, banks nothing (print-only diagnostics; leg 221's UNBANKED_CALLERS) ---
    "experiments/spike1_stepC_relax.py": dict(
        scope="PRE_REPAIR_UNBANKED", first_commit="08aff55", leg=None,
        note="print-only; writes nothing to writeup/data/, so nothing to contaminate"),
    "experiments/diagnose_stepC_drift.py": dict(
        scope="PRE_REPAIR_UNBANKED", first_commit="1a3e63c", leg=None,
        note="print-only diagnostic; writes nothing to writeup/data/"),

    # --- pre-repair tests (leg 221's TEST_CALLERS that really do import) ---
    "test_boussinesq_rescaled.py": dict(
        scope="PRE_REPAIR_TEST", first_commit="2511653", leg=None,
        note="module's own dedicated test, predates the repair"),
    "test_boussinesq_transport.py": dict(
        scope="PRE_REPAIR_TEST", first_commit="2511653", leg=None,
        note="transport-side test, predates the repair"),

    # --- the repair itself ---
    "experiments/p2_route_bvrr_v1_repair.py": dict(
        scope="REPAIR_APPARATUS", first_commit="d2d9769", leg=221,
        note="leg 221's own repair + zero-contamination runner; landed AS the repair commit"),

    # --- post-repair.  Cannot carry contamination: first committed after d2d9769. ---
    "experiments/p2_route_tscx_v1.py": dict(
        scope="POST_REPAIR", first_commit="401a5f7", leg=307,
        note="Route-TSCX, the two-scale counterexample adjudication; DRIFT ENTRY #1 found by "
             "leg 233 -- post-dates d2d9769, so outside the contamination question"),
    "experiments/p2_route_s1gr_v1.py": dict(
        scope="POST_REPAIR", first_commit="cc725d1", leg=335,
        note="Route-S1GR, the spike1_stepC_gate regeneration adjudication; DRIFT ENTRY #2 "
             "found by leg 233 -- post-dates d2d9769, so outside the contamination question"),
    "experiments/p2_route_bvrrv_v1_postrepair.py": dict(
        scope="POST_REPAIR", first_commit="d551e63", leg=233,
        note="leg 233's independent post-repair verification runner; carries census() itself"),
    "test_boussinesq_rescaled_postrepair.py": dict(
        scope="POST_REPAIR", first_commit="d551e63", leg=233,
        note="leg 233's pin on the repaired semantics; the third newcomer in leg 233's banked "
             "census, and the reason its JSON says 3 where its journal §3 says 2"),
}

SCOPE_LABELS = {
    "PRE_REPAIR_BANKED": FROZEN_SCOPE_NOTE,
    "PRE_REPAIR_UNBANKED": "Imports the module, predates the repair, banks no artifact.",
    "PRE_REPAIR_TEST": "Test file predating the repair. Tests are re-run, never banked.",
    "REPAIR_APPARATUS": "Leg 221's repair/verification machinery.",
    "POST_REPAIR": ("First committed AFTER d2d9769. Cannot carry contamination -- "
                    "contamination is a claim about values banked in the PRE-repair world."),
}

# Files that name `solver/boussinesq_rescaled` in text without importing it.  Correctly absent
# from both scopes; listed so the exclusion is a tested property rather than a coincidence.
NAMED_BUT_NOT_IMPORTING = (
    "solver/target_selection.py",              # names the module path in prose
    "experiments/p2_route_sirc_v1_census.py",  # names it in a string, line 495
    "test_boussinesq_rescaled_status.py",      # READS it as a file to check its docstring
    # The census apparatus itself, which is the sharpest case available: this file spells the
    # import out inside a regex, and its test spells a real import out inside a string
    # literal.  If either ever counted itself the census would be self-inflating.
    "experiments/bench_boussinesq_rescaled_caller_census.py",
    "test_boussinesq_rescaled_caller_census.py",
)

# Leg 233's live grep, banked at `43dce32`.  Quoted for comparison only; recomputed, never
# trusted as the answer.
LEG_233_LIVE_CENSUS = (
    "experiments/diagnose_stepC_drift.py",
    "experiments/p2_route_brs_v1_status_audit.py",
    "experiments/p2_route_bvrr_v1_repair.py",
    "experiments/p2_route_bvrrv_v1_postrepair.py",
    "experiments/p2_route_g_v1_collapse.py",
    "experiments/p2_route_k_v1_port.py",
    "experiments/p2_route_l_v1_precond.py",
    "experiments/p2_route_s1gr_v1.py",
    "experiments/p2_route_tscx_v1.py",
    "experiments/spike1_stepC_gate.py",
    "experiments/spike1_stepC_relax.py",
    "test_boussinesq_rescaled.py",
    "test_boussinesq_rescaled_postrepair.py",
    "test_boussinesq_transport.py",
    "writeup/3_spikes/spike1_stepB_evidence.py",
)


# ---------------------------------------------------------------------------
def live_importers(root: str = ROOT) -> list:
    """Every `.py` file under `root` that imports `solver.boussinesq_rescaled`, sorted.

    COMPUTED, NEVER TRANSCRIBED.  Scope identical to leg 233's `census()` so the counts are
    comparable: same regex, same excluded directories, module itself excluded, paths relative
    to `root`.
    """
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root)
            if rel == MODULE_PATH:
                continue
            try:
                with open(path, errors="replace") as fh:
                    src = fh.read()
            except OSError:
                continue
            if IMPORT_PATTERN.search(src):
                found.append(rel)
    return sorted(found)


def classified_importers() -> list:
    """Every path this module claims to know about, in either scope."""
    return sorted(set(FROZEN_PREREPAIR_BANKED) | set(CLASSIFICATION))


def drift(root: str = ROOT) -> dict:
    """The two-sided difference between what is live and what is classified.

    `unclassified` is the alarm the regression test fires on: a file that imports the module
    today and that no scope claims.  `vanished` is its mirror -- a classified path that no
    longer imports (a rename, a deletion, or a scope statement that has gone stale).  Both are
    reported as lists of names, not as booleans, so the failure message can say WHICH file.
    """
    live = live_importers(root)
    known = set(classified_importers())
    unclassified = [f for f in live if f not in known]
    vanished = [f for f in sorted(known) if f not in set(live)]
    return dict(
        n_live=len(live),
        live=live,
        n_classified=len(known),
        unclassified=unclassified,
        vanished=vanished,
        n_unclassified=len(unclassified),
        n_vanished=len(vanished),
    )


def first_commit(path: str, root: str = ROOT) -> str:
    """Short hash of the commit that first introduced `path`, or "" if git cannot say."""
    try:
        out = subprocess.run(
            ["git", "log", "--reverse", "--format=%h", "--", path],
            cwd=root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return ""
    lines = out.strip().splitlines()
    return lines[0] if lines else ""


def postdates_repair(path: str, root: str = ROOT) -> bool:
    """True iff `path`'s first commit is NOT an ancestor-or-self of the repair commit.

    Measured against git, not read off the table above -- the table is the claim, this is the
    check on it.
    """
    fc = first_commit(path, root)
    if not fc:
        return False
    try:
        rc = subprocess.run(["git", "merge-base", "--is-ancestor", fc, REPAIR_REF],
                            cwd=root, capture_output=True, text=True)
    except OSError:
        return False
    return rc.returncode != 0


def report(root: str = ROOT) -> dict:
    d = drift(root)
    live = d["live"]
    by_scope = {}
    for f in live:
        if f in FROZEN_PREREPAIR_BANKED:
            scope = "PRE_REPAIR_BANKED"
        else:
            scope = CLASSIFICATION.get(f, {}).get("scope", "UNCLASSIFIED")
        by_scope.setdefault(scope, []).append(f)
    leg_233 = set(LEG_233_LIVE_CENSUS)
    return dict(
        module=MODULE_PATH,
        repair_commit=REPAIR_REF,
        scope_labels=SCOPE_LABELS,
        frozen_pre_repair_banked=dict(
            n=len(FROZEN_PREREPAIR_BANKED),
            scripts=list(FROZEN_PREREPAIR_BANKED),
            cited_to=dict(registry=LEG_221_FINAL_REF, repair=REPAIR_REF,
                          republished_by_leg_233=LEG_233_REF),
            note=FROZEN_SCOPE_NOTE),
        live_importers=dict(n=d["n_live"], files=live,
                            by_scope={k: sorted(v) for k, v in sorted(by_scope.items())},
                            counts_by_scope={k: len(v) for k, v in sorted(by_scope.items())}),
        drift=dict(unclassified=d["unclassified"], vanished=d["vanished"]),
        vs_leg_233_live_census=dict(
            leg_233_n=len(LEG_233_LIVE_CENSUS),
            added_since_leg_233=sorted(set(live) - leg_233),
            removed_since_leg_233=sorted(leg_233 - set(live))),
        named_but_not_importing=list(NAMED_BUT_NOT_IMPORTING),
    )


if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
