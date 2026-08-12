"""The drift alarm for `solver/boussinesq_rescaled.py`'s caller census.

Bench repair (`ORCHESTRATION.md` §3 priority 2) of the finding in
`experiments/journal/leg_233.md` §3.  Leg 205 *assumed* the caller set; leg 221 grepped it
once and banked a registry; leg 233 grepped again ~130 legs later and found the live importer
set had moved.  **Nothing would have caught the next drift either** -- which is this file's
whole reason to exist.  The census itself lives in
`experiments/bench_boussinesq_rescaled_caller_census.py` and is computed on every run; these
tests are the thing that makes a *silent* drift impossible.

WHAT THIS FILE MUST NOT DO.  It must not "fix" leg 221's registry.  That registry is complete
over its own scope -- artifacts banked in the PRE-repair world, which is what contamination is
a claim about -- and stale only as a census of today's callers.  Both entries leg 233 flagged
post-date the repair commit `d2d9769` and therefore cannot carry contamination.  Test (2)
below asserts the frozen set against leg 233's landed JSON precisely so that a future editor
who "helpfully" appends the drifted entries turns the record red instead of quietly
rewriting what a landed artifact asserts.

THE ONE THAT MATTERS is test (4): a file that imports the module today and that no scope
claims fails the suite by name, and the failure message says which scope it needs classifying
into.  It was demonstrated red on a planted importer before this file was pushed -- a test
that cannot go red is not a test.

No scientific claim, no measurement, no figure; Clay stays ~0.05%.

Run:  python test_boussinesq_rescaled_caller_census.py
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))

from bench_boussinesq_rescaled_caller_census import (                 # noqa: E402
    CLASSIFICATION, FROZEN_PREREPAIR_BANKED, IMPORT_PATTERN, LEG_233_LIVE_CENSUS,
    LEG_233_REF, MODULE_PATH, NAMED_BUT_NOT_IMPORTING, REPAIR_REF, SCOPE_LABELS,
    classified_importers, drift, first_commit, live_importers, postdates_repair, report,
)

LEG_233_JSON = ROOT / "writeup" / "data" / "p2_route_bvrrv_v1_postrepair.json"


def _leg_233_census():
    """Leg 233's banked census, READ-ONLY.  Absent -> the tests that need it skip loudly
    rather than silently passing on nothing."""
    if not LEG_233_JSON.exists():
        return None
    with open(LEG_233_JSON) as fh:
        blob = json.load(fh)
    return blob.get("census")


# ---------------------------------------------------------------------------------------
# (1) the census is COMPUTED, and it agrees with itself
# ---------------------------------------------------------------------------------------

def test_census_is_computed_and_nonempty():
    live = live_importers()
    assert live, "the census returned nothing -- the grep is broken, not the repo empty"
    assert live == sorted(set(live)), "the census must be sorted and duplicate-free"
    assert MODULE_PATH not in live, "the module must not count itself as its own importer"
    assert len(live) >= 10, (
        f"only {len(live)} importers found; leg 233 measured 15 and the repo has only grown. "
        f"A collapse this large means the pattern or the walk broke, not that callers left.")
    print(f"[ok] (1) live census computed: {len(live)} importers of {MODULE_PATH}, "
          f"sorted, self excluded")


# ---------------------------------------------------------------------------------------
# (2) the FROZEN scope is pinned to landed evidence and is NOT to be extended
# ---------------------------------------------------------------------------------------

def test_frozen_registry_matches_leg_221_as_banked_by_leg_233():
    census = _leg_233_census()
    if census is None:
        print(f"[skip] (2) {LEG_233_JSON.name} absent; frozen scope not cross-checked")
        return
    banked = sorted(census["leg_221_registry_scripts"])
    frozen = sorted(FROZEN_PREREPAIR_BANKED)
    assert frozen == banked, (
        "the frozen PRE-repair-banked scope no longer matches leg 221's registry as banked by "
        f"leg 233 at {LEG_233_REF}.\n"
        f"  here:      {frozen}\n"
        f"  banked:    {banked}\n"
        "That registry is COMPLETE over its own scope (artifacts banked pre-repair) and stale "
        "only as a census of today's callers. Do NOT append post-repair importers to it: they "
        "post-date d2d9769 and cannot carry contamination, and appending them converts a "
        "correct frozen answer into an incoherent half-census. Classify them in "
        "experiments/bench_boussinesq_rescaled_caller_census.py::CLASSIFICATION instead.")
    assert census["n_banked_in_registry"] == len(frozen) == 6
    print(f"[ok] (2) frozen PRE_REPAIR_BANKED scope = {len(frozen)} scripts, identical to "
          f"leg 221's registry as republished at {LEG_233_REF}")


def test_frozen_scope_contains_no_post_repair_entry():
    offenders = [f for f in FROZEN_PREREPAIR_BANKED
                 if CLASSIFICATION.get(f, {}).get("scope") == "POST_REPAIR"]
    assert not offenders, (
        f"post-repair scripts have leaked into the frozen pre-repair scope: {offenders}")
    measured = {f: first_commit(f) for f in FROZEN_PREREPAIR_BANKED}
    late = [f for f, h in measured.items() if h and postdates_repair(f)]
    assert not late, (
        f"these frozen-scope scripts were first committed AFTER the repair {REPAIR_REF}, so "
        f"they cannot belong to the pre-repair-banked set: {late}")
    print(f"[ok] (2b) all {len(FROZEN_PREREPAIR_BANKED)} frozen-scope scripts measured as "
          f"first-committed at or before {REPAIR_REF}: "
          + ", ".join(f"{Path(f).name}@{h}" for f, h in sorted(measured.items())))


# ---------------------------------------------------------------------------------------
# (3) the two scopes are separate, labelled, and jointly cover nothing twice
# ---------------------------------------------------------------------------------------

def test_the_two_scopes_are_disjoint_and_both_labelled():
    overlap = set(FROZEN_PREREPAIR_BANKED) & set(CLASSIFICATION)
    assert not overlap, (
        f"a path is claimed by BOTH the frozen scope and the live classification: "
        f"{sorted(overlap)} -- one scope per file, or the census means nothing")
    for f, entry in CLASSIFICATION.items():
        assert entry["scope"] in SCOPE_LABELS, (
            f"{f} carries scope {entry['scope']!r}, which has no label in SCOPE_LABELS")
        assert entry.get("note"), f"{f} is classified but carries no note saying why"
    assert "PRE_REPAIR_BANKED" in SCOPE_LABELS
    scopes = sorted({e["scope"] for e in CLASSIFICATION.values()} | {"PRE_REPAIR_BANKED"})
    print(f"[ok] (3) {len(scopes)} labelled scopes, pairwise disjoint over "
          f"{len(classified_importers())} classified paths: {', '.join(scopes)}")


# ---------------------------------------------------------------------------------------
# (4) THE ALARM.  A live importer no scope claims fails, BY NAME.
# ---------------------------------------------------------------------------------------

def test_no_live_importer_is_unclassified():
    d = drift()
    if d["unclassified"]:
        lines = []
        for f in d["unclassified"]:
            h = first_commit(f)
            if not h:
                where = "uncommitted / not yet in history  ->  POST_REPAIR"
            elif postdates_repair(f):
                where = f"first commit {h}, after {REPAIR_REF}  ->  POST_REPAIR"
            else:
                where = (f"first commit {h}, at or before {REPAIR_REF}  ->  a PRE_REPAIR_* "
                         f"scope; decide which by whether it banks a writeup/data artifact")
            lines.append(f"    {f}   ({where})")
        raise AssertionError(
            "CALLER CENSUS DRIFT: %d file(s) import %s today and no scope claims them:\n%s\n\n"
            "FIX IT IN experiments/bench_boussinesq_rescaled_caller_census.py::CLASSIFICATION -- add one entry "
            "per file with its scope, first_commit and leg number.\n"
            "DO NOT add it to FROZEN_PREREPAIR_BANKED: that set answers the historical "
            "question 'which artifacts were banked BEFORE the repair %s?' and is closed. A "
            "file first committed after the repair cannot carry contamination, so it belongs "
            "in POST_REPAIR."
            % (len(d["unclassified"]), MODULE_PATH, "\n".join(lines), REPAIR_REF))
    print(f"[ok] (4) 0 unclassified importers out of {d['n_live']} live "
          f"({d['n_classified']} paths classified across both scopes)")


def test_no_classified_path_has_silently_vanished():
    d = drift()
    assert not d["vanished"], (
        "CALLER CENSUS DRIFT (reverse): %d classified path(s) no longer import %s -- renamed, "
        "deleted, or the import was dropped:\n    %s\n"
        "Remove or re-point the entry in experiments/bench_boussinesq_rescaled_caller_census.py, and leave the "
        "FROZEN set alone if the path is in it (a deleted file's banked artifact is still a "
        "banked artifact)."
        % (len(d["vanished"]), MODULE_PATH, "\n    ".join(d["vanished"])))
    print(f"[ok] (5) 0 vanished paths: all {d['n_classified']} classified entries still "
          f"import the module")


# ---------------------------------------------------------------------------------------
# (6) the string-mention exclusion is a PROPERTY, not a coincidence
# ---------------------------------------------------------------------------------------

def test_files_that_only_name_the_module_are_excluded():
    live = set(live_importers())
    for rel in NAMED_BUT_NOT_IMPORTING:
        p = ROOT / rel
        assert p.exists(), f"{rel} is listed as a string-mention case but does not exist"
        src = p.read_text(errors="replace")
        assert "boussinesq_rescaled" in src, (
            f"{rel} no longer names the module at all; it is no longer a test case for the "
            f"exclusion and should be dropped from NAMED_BUT_NOT_IMPORTING")
        assert not IMPORT_PATTERN.search(src), (
            f"{rel} now IMPORTS the module -- it has become a real caller. Move it out of "
            f"NAMED_BUT_NOT_IMPORTING and into CLASSIFICATION with its scope.")
        assert rel not in live, f"{rel} names the module but was counted as an importer"
    print(f"[ok] (6) {len(NAMED_BUT_NOT_IMPORTING)} files name the module without importing "
          f"it and are excluded: " + ", ".join(NAMED_BUT_NOT_IMPORTING))


def test_a_planted_string_mention_is_not_counted():
    """Negative control on the control: the pattern must reject a mention in a string even
    when the exact import text appears inside it."""
    fake = 'X = "from solver.boussinesq_rescaled import RescaledBoussinesq"\n'
    assert not IMPORT_PATTERN.search(fake), (
        "the import pattern matched a module name inside a string literal; the exclusion "
        "leg 233 relied on is broken")
    real = "from solver.boussinesq_rescaled import RescaledBoussinesq\n"
    assert IMPORT_PATTERN.search(real), "the import pattern no longer matches a real import"
    indented = "    import solver.boussinesq_rescaled\n"
    assert IMPORT_PATTERN.search(indented), "a function-local import must still count"
    print("[ok] (7) pattern control: rejects the import text inside a string literal, accepts "
          "the top-level and the indented real import")


# ---------------------------------------------------------------------------------------
# (8) every POST_REPAIR classification is MEASURED against git, not asserted
# ---------------------------------------------------------------------------------------

def test_post_repair_entries_really_post_date_the_repair():
    if not (ROOT / ".git").exists():
        try:
            subprocess.run(["git", "rev-parse", "--git-dir"], cwd=ROOT,
                           capture_output=True, check=True)
        except (OSError, subprocess.CalledProcessError):
            print("[skip] (8) no git history available; post-repair ordering not measured")
            return
    post = {f: e for f, e in CLASSIFICATION.items() if e["scope"] == "POST_REPAIR"}
    assert post, "no POST_REPAIR entries at all -- leg 233 found at least two"
    measured = []
    for f, e in sorted(post.items()):
        h = first_commit(f)
        assert h, f"git cannot date {f}; a POST_REPAIR claim must be checkable"
        assert h.startswith(e["first_commit"]) or e["first_commit"].startswith(h), (
            f"{f} claims first commit {e['first_commit']} but git says {h}")
        assert postdates_repair(f), (
            f"{f} is classified POST_REPAIR but its first commit {h} is an ancestor of the "
            f"repair {REPAIR_REF} -- it is NOT outside the contamination question")
        measured.append(f"{Path(f).name}@{h}(leg {e['leg']})")
    print(f"[ok] (8) all {len(post)} POST_REPAIR entries measured strictly after "
          f"{REPAIR_REF}: " + ", ".join(measured))


def test_leg_233_two_drifted_entries_are_classified_post_repair():
    for f, leg, commit in (("experiments/p2_route_tscx_v1.py", 307, "401a5f7"),
                           ("experiments/p2_route_s1gr_v1.py", 335, "cc725d1")):
        e = CLASSIFICATION.get(f)
        assert e is not None, f"leg 233's drifted entry {f} is not classified at all"
        assert e["scope"] == "POST_REPAIR", (
            f"{f} must be POST_REPAIR (leg 233 §3): it post-dates {REPAIR_REF}")
        assert e["leg"] == leg and e["first_commit"] == commit, (
            f"{f} provenance disagrees with leg 233 §3: expected leg {leg} / {commit}, "
            f"table says leg {e['leg']} / {e['first_commit']}")
    print("[ok] (9) leg 233's two drifted entries classified POST_REPAIR with provenance: "
          "p2_route_tscx_v1.py (leg 307, 401a5f7), p2_route_s1gr_v1.py (leg 335, cc725d1)")


# ---------------------------------------------------------------------------------------
# (10) comparability with leg 233's live grep, as a MAGNITUDE
# ---------------------------------------------------------------------------------------

def test_leg_233_live_census_is_still_fully_classified():
    """Leg 233's 15 entries are historical fact.  New importers are allowed to appear -- that
    is what test (4) is for -- but nothing leg 233 saw may fall out of the classification
    without someone saying so."""
    known = set(classified_importers())
    lost = sorted(set(LEG_233_LIVE_CENSUS) - known)
    assert not lost, (
        f"leg 233 recorded these importers at {LEG_233_REF} and no scope claims them now: "
        f"{lost}")
    census = _leg_233_census()
    if census is not None:
        banked = sorted(census["real_importers_today"])
        assert banked == sorted(LEG_233_LIVE_CENSUS), (
            "the quoted leg 233 live census disagrees with its own banked JSON:\n"
            f"  quoted: {sorted(LEG_233_LIVE_CENSUS)}\n  banked: {banked}")
    r = report()
    added = r["vs_leg_233_live_census"]["added_since_leg_233"]
    removed = r["vs_leg_233_live_census"]["removed_since_leg_233"]
    print(f"[ok] (10) vs leg 233's live grep ({len(LEG_233_LIVE_CENSUS)} entries at "
          f"{LEG_233_REF}): {len(added)} added, {len(removed)} removed; today's census is "
          f"{r['live_importers']['n']} importers, by scope "
          f"{r['live_importers']['counts_by_scope']}")


def test_report_is_json_serialisable():
    blob = json.dumps(report())
    assert len(blob) > 500, "the report collapsed to something trivially small"
    print(f"[ok] (11) report() serialises to JSON ({len(blob)} bytes) for on-demand use")


if __name__ == "__main__":
    test_census_is_computed_and_nonempty()
    test_frozen_registry_matches_leg_221_as_banked_by_leg_233()
    test_frozen_scope_contains_no_post_repair_entry()
    test_the_two_scopes_are_disjoint_and_both_labelled()
    test_no_live_importer_is_unclassified()
    test_no_classified_path_has_silently_vanished()
    test_files_that_only_name_the_module_are_excluded()
    test_a_planted_string_mention_is_not_counted()
    test_post_repair_entries_really_post_date_the_repair()
    test_leg_233_two_drifted_entries_are_classified_post_repair()
    test_leg_233_live_census_is_still_fully_classified()
    test_report_is_json_serialisable()
    print("\nALL BOUSSINESQ-RESCALED CALLER-CENSUS TESTS PASSED")
