# ORCH_STATE — orchestrator handoff

**Owner: the orchestrator.** Written at every handoff (`ORCHESTRATION.md` §9d) and at every
stop. A fresh orchestrator session reads this at Step 0b before dispatching anything.

---

## Status: GRACEFUL, USER-REQUESTED STOP (2026-08-06, ~23:50 BST)

The user explicitly asked this session to stop gracefully and make everything resumable,
and said **they will start the next orchestrator session themselves** — no self-chain
`RemoteTrigger` was scheduled. Paste `ORCHESTRATOR_PROMPT.md` fresh to resume, exactly as
for any other manual restart.

This was an extremely long, single continuous session (resumed from an external-shutdown
interruption at the very start — see the git history around commit `5c18c13` for that
earlier handoff). It ran roughly one full ten-leg cycle, closed a large audit-family sweep,
and ended by applying a **major, user-authorized change to the plan of record itself**: the
exit criterion changed from "a novel Tier-3 result, NOT Clay" to **pursuing a full Clay
solve**. That is now live in `plan_of_record.py`, `test_plan_of_record.py`,
`CLAY_ROADMAP.md`, and `CONTINUATION_PROMPT.md`, all consistent, merge gate green.

## What the next orchestrator must do first

1. Read this file in full, then `PROGRESS.md` (git-ignored, current as of this session's
   last write — should be very close to accurate) and `reports/STATUS.md` (committed
   snapshot, refresh it after reading this if it's gone stale relative to what's below).
2. **Run `.venv/bin/python plan_of_record.py` and read its full docstring output** — the
   plan changed goal this session. `P0` (target selection under the Clay goal) is `NEXT`.
   Stage `B` is `DONE` (gate NO). Do not be surprised that the prize line no longer says
   "NOT Clay" — that's deliberate, not drift; `test_plan_of_record.py`'s honesty-invariant
   test was updated in the same commit to check odds+walls are still recorded, not the
   literal string.
3. **Resume or recreate the Decision Maker (Fable 5)** — it was mid-cycle, its full state is
   in `DIRECTION.md` (its own durable state, last touched by this session, fully current).
   It has just processed two major user rulings (PUB1/PUB2 approved; Clay goal change) and
   drafted the first legs of the new programme.
4. **Re-check every live agent's actual status before trusting anything below as "still
   running"** — subagent handles do not survive a session boundary. Everything below is
   this session's *last observed* state, verified against git/worktrees at handoff time,
   not a live process check the next session can rely on.
5. Re-arm the ten-leg pool and a heartbeat per the standing contract (`ORCHESTRATION.md`
   §9f) once slots are re-populated.

## Composition floor (`ORCHESTRATION.md` §3b, added this session per external user review)

**At or above the required 3/10 as of handoff**, tracking: 236 (RDDEP, math), 251 (P0T,
Phase 0 construction/scoping). A third may have landed or vacated since — check
`DIRECTION.md`'s own canonical reserve line first. This is a NEW standing rule this session
added (both to `DIRECTION.md` and `ORCHESTRATION.md` §3b, to survive exactly this kind of
restart) — do not let it silently lapse.

## Live-slot roster at handoff (branches/worktrees, not live-process guarantees)

| Slot | Leg | Route | Branch | State at handoff |
|---|---|---|---|---|
| A | 192 | H2CV (orphaned) | (no branch — see below) | **Agent terminated, not replaced in this slot.** Real uncommitted work (871-line runner, 592-line JSON, full journal) sits at `/home/andy/projects/Unsolved/.claude/worktrees/agent-a64cddd522d1387c5`, worktree unlocked (agent gone). Leg 249 was dispatched to recover/verify this work, but landed in slot B, not slot A — **slot A itself needs a fresh dispatch**, this is a real gap, not intentional. |
| B | 249 | H2CV2 (verify) | `verify/249-h2cv2-v1` (not yet pushed to any remote-visible ref) | **SUBMISSION-BLOCKING for PUB2, top priority.** Independently verifying leg 176's origin-H² certificate (σ_min=0.0908, ‖T⁻¹‖_X=4.026), recovering leg 192's uncommitted work per instructions. Worktree: `/home/andy/projects/Unsolved/.claude/worktrees/agent-a546b7de93147d173`. Was locked (in use) at last check. |
| C | 248 | CNR2 (repair) | `leg/248-cnr2-v1` (not yet pushed) | Repairs leg 237's scale-invariant-residual finding in `collocation_newton.py`. Worktree: `/home/andy/projects/Unsolved/.claude/worktrees/agent-af9dd50d65ff02aca`. Was locked at last check. |
| D | 221 | BVRR (repair) | `leg/221-bvrr-v1` | Has a real repair commit (`6a0abb8`) — closes leg 205's two `boussinesq_rescaled.py` mechanisms with an explicit zero-contamination re-confirmation. Last known status: running its own long verification relaxations (Step-C gate, Route-G G2, Route-K, Route-L), not yet finished/pushed. |
| E | 251 | P0T (Phase 0) | `leg/251-p0t-v1` (not yet pushed) | **First leg of the new Clay-directed programme.** Target selection screened by Nečas–Růžička–Šverák/Tsai's exclusion and every already-banked dead end. High-stakes — its YES branch names the Phase 1 (viscous rung) candidate; its own gate says push-branch-only-and-escalate on YES (needs DM/user sign-off before anyone builds on it), normal landing on NO. Worktree: `/home/andy/projects/Unsolved/.claude/worktrees/agent-aeb76e39a1329e543`. Was locked at last check. |
| F | 236 | RDDEP (math) | `leg/236-rddep-v1` | Has a novelty-pass commit (`6e4e100`) resolving that leg 226 was undispatched at the time it checked (leg 202's own diagnostic data used directly per its gate's second clause). Independently traces which banked Route-D v11 numbers actually depend on `profile_newton.py` and whether any move. Not yet finished. |
| G | — | VACANT | — | Was open at last check, awaiting the DM's next candidate. Reserve has 250 (PUB2 citation fix) and 252 (VBRG, Route-D v11 anchor-JSON regeneration) both ready-drafted and immediately dispatchable — check `DIRECTION.md`'s tail for their full specs before drafting anything new. |
| H | 228 | BHRV (verify) | `verify/228-bhrv-v1` | Verifying leg 218's `bordered_hl.py` repair (this cycle's highest-blast-radius fix). Has a rich novelty-pass commit (`f8aa892`) that already found a real gap: leg 218's own caller-set enumeration missed several importers (found 10 direct, not 6). Not yet finished. |
| I | 210 | M2SV (verify) | `verify/210-m2sv-v1` | Independently verifying leg 185's reparametrized `nu` measurement. No commits of its own beyond the shared history at last check — likely still mid-computation (its own status update earlier in the session described long-running numerical stages). |
| J | 226 | PNR (repair) | `leg/226-pnr-v1` | **Top-priority repair** for leg 202's Route-D v11 exposure (the first materially-exposed, not-just-latent finding this cycle). Has a novelty-pass commit (`cef3282`) that already found the dispatch's own prescribed fix doesn't work as specified (the `weighted_defect` diagnostic is anti-correlated with the off-branch cases, not a rejector of them) — its gate explicitly authorizes finding a *different* mechanism, so this is not a failure, it's the leg doing its job. Not yet finished. |

## What this session accomplished (summary, full detail in `experiments/JOURNAL.md`'s tail
and the git log)

- **~20 legs landed clean, ~20 escalated** across a large audit-family sweep (adversarial
  input testing against claim-adjacent modules) — the highest density of real findings this
  audit family has produced. Two are still-open, real findings worth the next session's
  attention if not already resolved: leg 198/218 (`bordered_hl.py`, repaired, verification in
  flight as leg 228) and leg 202/226/235/236/247 (Route-D v11's `profile_newton.py` and
  `v5_budget`, TWO independent mechanisms found, one repaired-with-a-real-violation-confirmed
  (leg 247, escalated — the corrected budget genuinely misses by 62x at a=0.45, though the
  banked prose already said so honestly), one still being repaired (leg 226/236).
- **An external user review mid-session found the leg queue had drifted into an
  audit/repair-only composition** (leg 0 orchestrator commits at 57% of recent history). Applied:
  a new **composition floor** rule (`ORCHESTRATION.md` §3b, `DIRECTION.md`), requiring at
  least 3/10 live slots to be math/literature/construction-typed at all times. This oscillated
  a few times as floor-eligible legs landed faster than replacements could be drafted — the
  DM eventually pre-drafted spares to get ahead of it. **Watch this in the next session**;
  if it breaches again, the DM already flagged that the fix would be roster-shaped, not
  reserve-shaped.
- **THE MAJOR EVENT: two user rulings, both applied.** (1) PUB1 and PUB2 (this project's
  publication-scoping bundles) are now **APPROVED as the deliverable**, pending two
  submission-blocking legs (249 verification, 250 citation fix — 250 not yet dispatched,
  ready in reserve). (2) **The exit criterion changed to a full Clay solve**, resolving a
  long-parked escalation (stage B's exhaustion had no successor for ~120 legs). Applied to
  `plan_of_record.py` (new stage `P0`, Wall 2 corrected, one ban re-posed), verified against
  all 8 `test_plan_of_record.py` invariants, merge gate green. **Clay odds explicitly did
  NOT move — still ~0.05%, recorded in the same breath as the goal change per the user's own
  explicit instruction.** The full technical framing (Tao's supercriticality barrier, the
  corrected Wall 2, the NRS/Tsai ansatz constraint, the viscous-rung-first sequencing) is
  recorded in `CONTINUATION_PROMPT.md`'s Directive 1 and `CLAY_ROADMAP.md` §7.5 — read those
  before drafting any further Phase 0/1 legs, so the next session doesn't restart work this
  one already did.
- **Leg 251 (Phase 0) is the single most consequential leg in flight** — its YES branch
  names the actual object+ansatz the rest of the Clay-directed programme will build on.
  Treat its output (whenever it lands) as needing DM/user sign-off before anything is built
  on it, per its own gate wording.

## Open escalations / user-facing items (also in `PROGRESS.md`'s NEEDS YOU, check there for
the fullest, most current version)

1. Route-D v11 has two confirmed distinct exposures this cycle (legs 202/226 and 235/247) —
   repairs in flight for both, neither fully landed+verified yet.
2. Leg 178 (WES) — parked, self-conflicted gate, three explicit questions for the user,
   unresolved for many cycles now, never actioned by any ruling this session.
3. Leg 129/188 — escalation #4 (Bowman dealiasing rule), sharpened in scope, still parked.
4. The exit-criterion ruling itself is applied, but PUB1/PUB2's own approval is not yet
   "final" in the sense of the two submission blockers (249, 250) landing — check whether
   249 has reported back by the time you read this.

## Run

| Field | Value |
|---|---|
| `main` SHA at handoff | `7046ccf` |
| Highest leg number drafted | 252 |
| Stop reason | User-requested graceful stop, explicitly to hand off to a fresh orchestrator the user will start manually — not a context-limit or error-triggered handoff |
| Self-chain scheduled? | **No** — user explicit that they will start the next session themselves |
