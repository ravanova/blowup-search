# ORCH_STATE — orchestrator handoff

**Owner: the orchestrator.** Written at every handoff (`ORCHESTRATION.md` §9d) and at every
stop. A fresh orchestrator session reads this at Step 0b.5 **before dispatching anything**.

**Why it records branches and not agent handles:** subagent handles do not survive the session
that spawned them. The next orchestrator cannot message the previous one's agents. It can only
gate and merge what their branches contain, and re-spawn fresh agents for interrupted legs.

---

## Status

**SEED — no run has handed off yet.** The first orchestrator session overwrites this.

## Resume checklist for the next orchestrator

1. Gate and merge every branch listed under *Live branches* below, oldest first.
2. Re-spawn a fresh leg agent for every leg marked **interrupted**, with a brief describing how
   far it got.
3. Read `DIRECTION.md` for the queue; re-spawn the Decision Maker if it is not alive.
4. Resume the loop at `ORCHESTRATOR_PROMPT.md` Step 3, cycle count reset to 1.

## Run

| Field | Value |
|---|---|
| Cycles completed | — |
| `main` SHA at handoff | — |
| Highest leg number used | 53 |
| Reason for handoff | — |

## Live branches

| Branch | Leg | Role | State at handoff | Interrupted? |
|---|---|---|---|---|
| — | — | — | — | — |

## Queue at handoff

*(from `DIRECTION.md`)*

## Open escalations

*(the four in `ORCHESTRATION.md` §8, plus anything else parked under `⚠ NEEDS YOU`)*

## Sharding-experiment ledger

*(`ORCHESTRATION.md` §10 — per leg: wall-clock dispatch→merged, agent invocations + follow-up
messages, rework rounds, pre-registered difficulty)*

| Leg | Arm | Difficulty | Wall-clock | Invocations | Rework rounds |
|---|---|---|---|---|---|
| — | — | — | — | — | — |
