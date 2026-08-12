"""Drift detector for capabilities.py -- the index of what is already built.

An index that is allowed to go stale is worse than no index, because it is believed.
These gates fail if a solver module appears without an entry, if an entry points at a
module or a test that does not exist, or if an entry's `validated` field is empty --
which is the field that stops a module being trusted further than it was tested.

Run: .venv/bin/python test_capabilities.py
"""

from pathlib import Path

from capabilities import CAPABILITIES, find, modules

ROOT = Path(__file__).resolve().parent


def test_every_solver_module_is_indexed():
    """No solver/*.py may exist without an entry. This is the gate with teeth."""
    on_disk = {f"solver/{p.name}" for p in (ROOT / "solver").glob("*.py")
               if p.name != "__init__.py"}
    indexed = modules()
    missing = sorted(on_disk - indexed)
    ghosts = sorted(indexed - on_disk)
    assert not missing, f"solver modules with no capability entry: {missing}"
    assert not ghosts, f"capability entries for modules that do not exist: {ghosts}"
    print(f"    {len(on_disk)} solver modules, all indexed, no ghosts")
    print("[ok] every solver module is in the capability index")


def test_entries_are_complete_and_point_at_real_files():
    """Four fields, all non-empty, and the test file exists."""
    for c in CAPABILITIES:
        for k in ("module", "object", "holds", "validated", "test"):
            assert c.get(k), f"{c.get('module')}: empty field {k}"
        assert (ROOT / c["test"]).exists(), f"{c['module']}: missing test {c['test']}"
        assert len(c["validated"]) > 20, \
            f"{c['module']}: `validated` is too short to say what was checked"
    print(f"    {len(CAPABILITIES)} entries, all four fields present, all tests exist")
    print("[ok] entries are complete and point at real files")


def test_objects_are_distinct_enough_to_search_on():
    """The `object` field is the search key -- duplicates make it useless."""
    objs = [c["object"] for c in CAPABILITIES]
    assert len(set(objs)) == len(objs), \
        f"duplicate object keys: {[o for o in objs if objs.count(o) > 1]}"
    print(f"    {len(set(objs))} distinct object keys")
    print("[ok] object keys are distinct")


def test_the_search_finds_the_thing_route_m_nearly_rebuilt():
    """The regression this file exists for: `capabilities.py hou-luo` must find it.

    Route-M came within about ten minutes of rebuilding RescaledHLScenario2 from
    scratch.  If this test ever fails, the index has stopped answering the one question
    it was created to answer.
    """
    hits = find("hou-luo")
    assert hits, "the Hou-Luo machinery is not findable by name"
    assert any("Scenario2" in c["holds"] for c in hits), \
        "the Scenario-2 integrator is not named in what the Hou-Luo entry holds"
    assert find("scenario 2") or find("Scenario2"), "Scenario-2 is not searchable"
    assert find("interval arithmetic"), "the interval arithmetic is not findable"
    assert find("radii"), "the radii-polynomial machinery is not findable"
    print(f"    'hou-luo' -> {len(hits)} entr(ies), Scenario-2 named in `holds`")
    print("[ok] the index finds the machinery Route-M nearly rebuilt")


def test_superseded_modules_say_so():
    """A superseded module must be labelled, not silently indexed as usable."""
    sup = [c for c in CAPABILITIES if "SUPERSEDED" in c["object"].upper()
           or "SUPERSEDED" in c["holds"].upper()]
    for c in sup:
        assert "supersed" in (c["object"] + c["holds"]).lower()
    src = (ROOT / "solver" / "finite_support.py").read_text()
    if "SUPERSEDED" in src:
        assert any("finite_support" in c["module"] for c in sup), \
            "solver/finite_support.py says SUPERSEDED but the index does not"
    print(f"    {len(sup)} superseded module(s), all labelled in the index")
    print("[ok] superseded modules are labelled")


def test_leg_362_dssp_screen_extension_is_findable():
    """Leg 362's three-way NRS/Tsai extension (EXCLUDED-BY-T1/
    EXCLUDED-BY-T2/NOT-REACHED-BY-ANSATZ) must be described in the SAME
    dssp_screen.py entry it extends, not a duplicate/ghost entry."""
    hits = find("NOT-REACHED-BY-ANSATZ")
    assert hits, "leg 362's extension is not findable via capabilities.find()"
    assert all(c["module"] == "solver/dssp_screen.py" for c in hits), \
        "leg 362's extension should live in the existing dssp_screen.py entry, not a new module"
    assert find("EXCLUDED-BY-T2"), "leg 362's Theorem-2 verdict is not findable"
    print(f"    'NOT-REACHED-BY-ANSATZ' -> {len(hits)} entr(ies), same module as leg 357's")
    print("[ok] leg 362's extension is registered additively, no duplicate module entry")


if __name__ == "__main__":
    test_every_solver_module_is_indexed()
    test_entries_are_complete_and_point_at_real_files()
    test_objects_are_distinct_enough_to_search_on()
    test_the_search_finds_the_thing_route_m_nearly_rebuilt()
    test_superseded_modules_say_so()
    test_leg_362_dssp_screen_extension_is_findable()
    print("\nALL CAPABILITY-INDEX TESTS PASSED")
