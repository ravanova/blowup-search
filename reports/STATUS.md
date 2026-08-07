# STATUS — committed snapshot (sections 1-3 of PROGRESS.md)

*Refreshed 2026-08-07, cycle 1 — an exceptionally eventful cycle: Phase 0 named its candidate,
two independent verifiers found real gaps now being corrected, a session-wide usage outage hit
and was recovered from. Full detail in `PROGRESS.md` (git-ignored, more current) and
`reports/ORCH_STATE.md` (outage incident record).*

## ⚠ NEEDS YOU

0. **Leg 251 (Phase 0) named the run's first Phase-1 candidate**: the 3D compressible
   Navier-Stokes imploding self-similar profile at γ=7/5 (Buckmaster-Cao-Gómez-Serrano +
   companion), explicitly flagged as compressible NS, not the incompressible system Clay's
   problem asks about. An independent verifier confirmed nearly everything at primary source but
   found one gap (a mis-stated certificate obligation) — a rework leg is in flight to fix it
   before this is presented as final. Separately, leg 261 confirmed the incompressible-fluid
   route through this run's other main tool (Breden-Chu's machinery) is now closed three
   independent ways — a re-posing decision for Phase 1 is being held for you in one packet.
1. **Leg 257 — stage-V ban's lift clause is satisfied on paper**, needs your ruling. The DM
   recommends lifting it (useful for non-fluid targets even though the fluid route is separately
   closed) — held for the same packet as leg 251's corrected finding.
2. **Leg 249 — PUB2 (an approved submission-track document) quotes a figure (4.026) that an
   independent exact-arithmetic re-derivation shows doesn't actually hold** — the true value
   converges to ≈4.0318. A rework leg is in flight to correct it.
3. Leg 254 (DSS ban) — RESOLVED, applied. Leg 178 (WES) — RESOLVED, applied.
4. Leg 129/188 — escalation #4, still parked, unchanged.

## Now

- Cycle: 1
- `main` SHA: `2a152b9`
- Agents live: 10/10 leg slots + 2 verifiers + 1 Decision Maker

## Incident, recovered

A session-wide usage-limit outage killed 5 background agents simultaneously partway through
this cycle. One (leg 261) had actually finished and was landed on its behalf; four others had
real partial work salvaged as WIP branches and have since been redispatched. Capacity is
confirmed restored — legs 249 and 260 both finished normally after the outage, and all
redispatches are proceeding.

## Legs (10 slots)

| Slot | Leg | Route | Notes |
|---|---|---|---|
| A | 266 | P0TC | corrects leg 251's certificate obligation |
| B | 268 | PUB2R | corrects PUB2's unsupported figure |
| C | (needs refill) | — | leg 260 landed (DSS ban basis upgraded to substantive) |
| D | 221 | BVRR | resumed after outage |
| E | 248 | CNR2 | resumed after outage |
| F | 236 | RDDEP | resumed after outage |
| G | 267 | FDL | precedent census |
| H | 264 | WETP | licensed transfer probe |
| I | 252 | VBRG | resumed after outage |
| J | 226 | PNR | resumed after outage; highest-priority repair |

Landed this cycle, in order: 250, 258, 255, (user ruling on 254 applied), 178, 256, 261, 262,
260. Parked escalations awaiting correction/ruling: 251, 253, 257, 249.
