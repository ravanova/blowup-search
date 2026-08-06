# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-07, cycle 1 — first landings audited, first refill dispatched. Full detail
in `PROGRESS.md` (git-ignored, more current) and `reports/ORCH_STATE.md` (prior handoff).*

## ⚠ NEEDS YOU

1. **Leg 254 (Route-DSSX) — escalation, parked at PR #18 (`leg/254-dssx-v1`).** The user's
   2026-08-07 steer prioritized this leg to determine whether the DSS ban's "expensive
   entrance" (a global, unseeded periodic-orbit search of the rescaled gCLM flow) was excluded
   for a substantive reason or only by cost. **Finding: cost-shaped, not substantive** — all
   three of the ban's recorded reasons are local-linear spectral statements at a fixed point of
   the flow (0 of 3 concern a global search); the phrase "expensive entrance" entered
   `plan_of_record.py` in the same commit that authored the ban, never examined afterward; a
   repo-wide grep finds 0 periodic-orbit searches of the rescaled flow ever built, run, or
   costed. Leg 254 proposes re-posed wording splitting the ban into a cheap-entrance clause
   (stays banned as-is) and an expensive-entrance clause (opens under the Clay goal, gated on a
   3-clause lift condition: function space, object, price) — full text in
   `experiments/journal/leg_254.md` §8 and the PR body. **This is a ban weakening and cannot
   land under a leg's own signature — needs a ruling before leg 251 (Phase 0 target selection)
   redispatches with DSS treated as open.**
2. **Leg 178 (WES)** — parked, self-conflicted gate, three explicit questions for the user,
   unresolved for many cycles, not actioned this session.
3. **Leg 129/188** — escalation #4 (Bowman dealiasing rule), sharpened in scope, still parked.

## Now

- Cycle: 1
- `main` SHA: `f039d68`
- Agents live: 11 (10 leg slots + 1 verifier), plus 1 Decision Maker (Fable 5)

## Legs (10 slots)

| Slot | Leg | Route | Notes |
|---|---|---|---|
| A | 253 | NRSX | fresh; NRS/Tsai hypothesis boundary |
| B | 249 | H2CV2 | resuming from salvage; TOP PRIORITY, submission-blocking |
| C | 254 | DSSX | **done — escalated**, awaiting DM's next assignment for this slot |
| D | 221 | BVRR | resuming; zero-contamination re-confirmation |
| E | 255 | P1A | Phase 1 target census |
| F | 236 | RDDEP | resuming; Route-D v11 dependency trace |
| G | 256 | P1B | Breden-Chu end-to-end reproduction |
| H | 257 | P1C | Remark 40 reach + stage-V ban-lift scoping |
| I | 252 | VBRG | regenerates Route-D v11's stale anchor JSON |
| J | 226 | PNR | highest-priority repair, threatens a banked headline |

Session start recovered from a clean, graceful handoff — several of the prior session's "live"
slots were not actually recoverable (subagent handles don't survive session boundaries); WIP
was salvaged where real, leg 251 (Phase 0) was a total loss and redrafted. User steer applied:
DSS-ban scoping prioritized (254), Phase 1 authorized in parallel with Phase 0 (legs 255-257).
Landed this cycle: leg 250 (PUB2's σ_min citation fix — an inverted inequality sign, not a
measurement error), leg 258 (composition floor locked into `test_plan_of_record.py`).
