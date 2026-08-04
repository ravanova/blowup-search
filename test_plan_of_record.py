"""The drift detector: gates that fail when the plan and the documents disagree.

This project's characteristic failure is drift, not error -- ranked item (3) lost to a
cheaper leg six consecutive times while a document at the top of the repository said it was
the most important thing to do.  Prose did not stop it.  These gates are the executable form
(banked lesson 68).

  (1) THE PLAN IS WELL-FORMED. Exactly one stage is NEXT, the order is DONE* NEXT QUEUED*,
      and every stage names a deliverable and a time-box.
  (2) EVERY GATE NAMES BOTH OUTCOMES. This project has shipped gates that specified only the
      pass branch; Route-H's refusal predicate is the counterexample that fixed it. A gate
      whose failure branch is unwritten is a gate that will be argued around at 2am.
  (3) EVERY BAN NAMES WHAT LIFTS IT. A ban with no lifting condition becomes a superstition.
  (4) THE CONTINUATION PROMPT AGREES WITH THE PLAN. Its leading directive must name the
      current stage, and must not have quietly re-ordered the sequence.
  (5) THE ROADMAP AGREES WITH THE PLAN. CLAY_ROADMAP.md section 7 must be marked ADOPTED,
      not left as an option analysis, now that it has been.
  (6) THE HONESTY INVARIANTS ARE STILL THERE. Both walls, the odds, and the statement that
      this plan does not move Clay. If a future session quietly deletes those, this fails.

Run: .venv/bin/python test_plan_of_record.py
"""

from pathlib import Path

from plan_of_record import (
    ADOPTED, BANNED, CLAY_ODDS, DISCIPLINE, PRIZE, STAGES, WALLS,
    banned_now, current, status_report,
)

ROOT = Path(__file__).resolve().parent


def test_1_plan_is_well_formed():
    s = current()                      # raises unless exactly one NEXT
    order = [st["status"] for st in STAGES]
    seen_next = False
    for i, st in enumerate(order):
        if st == "DONE":
            assert not seen_next and "QUEUED" not in order[:i], "DONE after NEXT/QUEUED"
        if st == "NEXT":
            seen_next = True
    assert order.count("NEXT") == 1
    ids = [st["id"] for st in STAGES]
    assert len(ids) == len(set(ids)), ids
    for st in STAGES:
        assert st["deliverable"].strip(), st["id"]
        assert st["time_box"].strip(), st["id"]
        assert st["name"].strip(), st["id"]
    print(f"  {len(STAGES)} stages, order valid, NEXT = {s['id']} ({s['name'][:50]}...)  OK")


def test_2_every_gate_names_both_outcomes():
    for st in STAGES:
        g = st["gate"]
        assert g["question"].strip().endswith("?"), st["id"]
        for branch in ("if_yes", "if_no"):
            assert len(g[branch].strip()) > 30, f"{st['id']} {branch} is too thin to bind"
        # the failure branch must actually say what to DO, not merely describe a feeling
        assert any(w in g["if_no"].upper()
                   for w in ("STOP", "DO NOT", "REPORT", "PROCEED")), st["id"]
    print(f"  all {len(STAGES)} gates name both outcomes, and every failure branch is "
          f"actionable  OK")


def test_3_every_ban_names_what_lifts_it():
    ids = {st["id"] for st in STAGES} | {"never"}
    for what, lifts in BANNED:
        assert what.strip() and lifts.strip(), what
        head = lifts.split(" --")[0].strip()
        assert head in ids, f"'{what}' is lifted by unknown stage '{head}'"
    now = banned_now()
    assert len(now) == len(BANNED), "nothing is DONE yet, so no ban should be lifted"
    print(f"  {len(BANNED)} bans, each naming its lifting stage; {len(now)} in force  OK")


def test_4_continuation_prompt_agrees():
    t = (ROOT / "CONTINUATION_PROMPT.md").read_text()
    s = current()
    head = t[:6000]
    assert f"ROUTE-{s['id']}" in head.upper() or f"DIRECTIVE 1 — ROUTE-{s['id']}" in head, (
        f"the continuation prompt's leading directive does not name stage {s['id']}")
    # the queued stages must still be present somewhere, so the sequence has not been dropped
    for st in STAGES:
        if st["status"] == "QUEUED":
            assert st["id"].lower() in t.lower() or st["name"].split(" --")[0].lower() in t.lower(), (
                f"stage {st['id']} has vanished from the continuation prompt")
    # the honest ceiling must survive at the top of the file
    assert "0.05%" in t and "chain has moved" in t.lower()
    print(f"  continuation prompt leads with {s['id']}, retains all queued stages, and "
          f"still carries the odds and the no-link-moved statement  OK")


def test_5_roadmap_is_marked_adopted():
    t = (ROOT / "CLAY_ROADMAP.md").read_text()
    assert "## 7." in t, "roadmap section 7 is missing"
    sec = t[t.index("## 7."):]
    assert "ADOPTED" in sec.upper(), "section 7 is not marked adopted"
    assert "NOT A COMMITTED PLAN" not in sec.upper(), (
        "section 7 still says it is not a committed plan, but it was adopted on " + ADOPTED)
    assert ADOPTED in sec
    print(f"  CLAY_ROADMAP.md section 7 is marked ADOPTED ({ADOPTED})  OK")


def test_6_honesty_invariants_survive():
    assert len(WALLS) == 2
    for name, text in WALLS:
        assert len(text) > 60, name
    assert abs(CLAY_ODDS - 0.0005) < 1e-9
    assert "NOT Clay" in PRIZE
    # the roadmap and the plan must agree that nothing here moves Clay
    t = (ROOT / "CLAY_ROADMAP.md").read_text()
    sec = t[t.index("## 7."):]
    assert "Wall 2" in sec and "does not" in sec
    # and the discipline list must not have been quietly trimmed
    nums = [n for n, _ in DISCIPLINE]
    assert nums == sorted(nums) and len(nums) >= 10, nums
    for n in (67, 68, 72, 73, 74):
        assert n in nums, f"lesson ({n}) has been dropped from the standing discipline"
    print(f"  two walls intact, Clay at {CLAY_ODDS:.2%}, prize says NOT Clay, "
          f"{len(DISCIPLINE)} discipline items retained  OK")


def test_7_status_report_renders():
    r = status_report()
    assert current()["id"] in r and "BANNED RIGHT NOW" in r and "Clay" in r
    assert len(r.splitlines()) > 15
    print("  status_report() renders the sequence, the next gate and the live bans  OK")


if __name__ == "__main__":
    import time
    t0 = time.time()
    for fn in (test_1_plan_is_well_formed,
               test_2_every_gate_names_both_outcomes,
               test_3_every_ban_names_what_lifts_it,
               test_4_continuation_prompt_agrees,
               test_5_roadmap_is_marked_adopted,
               test_6_honesty_invariants_survive,
               test_7_status_report_renders):
        print(f"\n{fn.__name__}")
        fn()
    print(f"\nALL GATES PASS ({time.time() - t0:.1f}s)")
    print("\n" + status_report())
