# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-07, cycle 1 — two major escalations surfaced (legs 253, 257), one user
ruling applied (leg 254), one more forwarded to the DM (leg 178). Full detail in
`PROGRESS.md` (git-ignored, more current).*

## ⚠ NEEDS YOU

1. **Leg 257 (Route-P1C) — escalation, parked at PR #19 (`leg/257-p1c-v1`).** Stage-V ban's
   lift clause is now satisfied on paper: Breden-Chu's H²(µ) weighted-Sobolev space is
   confirmed a genuine "namable fourth space" — all three prior death mechanisms evade at the
   mechanism level, each independently checked with its own locator (measured Z₁ = 0.065136 in
   the new space vs 8.9591/140.72 in the dead ones). This is a ban weakening and needs a ruling
   to actually lift, same as leg 254 was. Separately, and regardless of the ban question: leg
   257 also independently found the Leray projection provably leaves L²(µ) in this space, which
   structurally closes the fluid route through this machinery even if the ban lifts — this
   confirms and strengthens leg 255's earlier finding that the one fluid-adjacent Phase-1
   candidate (Li-Zhou) dies on the same clause. Both findings forwarded to leg 251 (Phase 0,
   still in flight).
2. **Leg 178 (WES)** — parked, self-conflicted gate, three explicit questions for the user.
   The user has now ruled on all three (unpark under the YES branch; leg 111's headline gets a
   scoped correction, not a global search-and-replace; the depth ladder becomes a contamination
   cap) plus bounded what it licenses. Forwarded to the DM; dispatch pending its response.
3. **Leg 129/188** — escalation #4 (Bowman dealiasing rule), sharpened in scope, still parked.

(Leg 254's DSS-ban escalation is RESOLVED — the user ruled "let's get leg 254 merged" and it's
applied to `main` at `47f76eb`, PR #18 closed with an explanation.)

## Now

- Cycle: 1
- `main` SHA: `f9952fb`
- Agents live: 9 of 10 leg slots (A and H vacant, pending DM assignment), plus 1 Decision Maker

## Legs (10 slots)

| Slot | Leg | Route | Notes |
|---|---|---|---|
| A | (vacant) | — | leg 253 (NRSX) finished, escalated |
| B | 249 | H2CV2 | resuming from salvage; TOP PRIORITY, submission-blocking |
| C | 251 | P0T | Phase 0 target selection, most consequential leg in flight |
| D | 221 | BVRR | resuming; zero-contamination re-confirmation |
| E | 248 | CNR2 | resuming; repairing collocation_newton.py |
| F | 236 | RDDEP | resuming; Route-D v11 dependency trace |
| G | 256 | P1B | Breden-Chu end-to-end reproduction |
| H | (vacant) | — | leg 257 (P1C) finished, escalated |
| I | 252 | VBRG | regenerating Route-D v11's stale anchor JSON |
| J | 226 | PNR | highest-priority repair, threatens a banked headline |

Landed this cycle: leg 250 (PUB2's σ_min citation fix, verified), leg 258 (composition floor
locked into code), leg 255 (Phase 1 census — 2 non-fluid survivors, fluid candidate killed,
verified). User ruling applied on leg 254 (DSS ban split). Two new escalations surfaced (253,
257), both forwarded to leg 251 and the DM. Session start recovered from a clean handoff;
several "live" slots from the prior session were not actually recoverable and were
salvaged/redrafted as needed.
