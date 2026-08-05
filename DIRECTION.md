# DIRECTION — the leg queue

**Owner: the Decision Maker (Opus 5). No other agent edits this file.**

This is the Decision Maker's durable state. It exists so a DM whose context has bloated can be
discarded and recreated from the file instead of re-derived from the whole repository.

It is **not** `plan_of_record.py`. The plan carries the committed sequence and exactly one
stage marked `NEXT`; this file carries the *exploration* routes running alongside it. Promoting
a route from here into the plan's committed sequence is escalation #1 in `ORCHESTRATION.md` §8
and needs the user.

---

## Status

**SEED — no queue yet.** The first orchestrator session spawns the DM (Step 1 of
`ORCHESTRATOR_PROMPT.md`), which replaces everything below this line.

Last leg number used: **53** (Route-TC v1, gate answered NO). Next leg: **54**.

---

## Live assignments

| Slot | Leg | Route | Critical path? | Difficulty (pre-registered) | Branch | Gate |
|---|---|---|---|---|---|---|
| LEG-A | — | — | — | — | — | — |
| LEG-B | — | — | — | — | — | — |
| LEG-C | — | — | — | — | — | — |
| LEG-D | — | — | — | — | — | — |

Exactly one of the four is the stage `plan_of_record.py` marks `NEXT` (currently `MM`). The
other three are independent exploration routes.

## Queue

Ranked. Each entry needs all six fields or it is not dispatchable.

```
### <leg number> — <route name>
**Thesis.** <one paragraph: what this leg believes and what it will build to find out>
**Gate.** <question ending in "?">
  yes -> <what happens, concretely>
  no  -> <what stops, concretely — a gate with no failure branch is not a gate>
**Territory.** experiments/leg<N>_*.py, solver/<module>.py, test_<module>.py,
               writeup/<subdir>/, writeup/data/<name>.json
**Difficulty.** light | standard | heavy   (pre-registered, before any agent starts)
**Independence.** <why this does not depend on, or collide with, the other live legs>
```

*(empty — the DM fills this)*

## Ranking rationale

Refreshed whenever a gate answers. Rank by, in order:

1. could this leg actually move a link of the L1→L4 chain;
2. can its gate answer either way within one leg's work;
3. is it independent of the other three live legs.

**Ordering the queue by proximity to the Clay chain is a choice of what to try. It is never a
claim that anything moved.** In 53 legs, no link has moved; Clay stays at ~0.05% behind Walls 1
and 2.

*(empty — the DM fills this)*

## Open direction questions for the user

These also appear under `⚠ NEEDS YOU` in `PROGRESS.md`. The run continues around them.

*(none)*
