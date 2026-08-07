# ORCH_STATE — orchestrator handoff

**Owner: the orchestrator.** Written at every handoff and at every stop. A fresh orchestrator
session reads this at Step 0b before dispatching anything.

---

## Status: PAUSED — SESSION-WIDE USAGE LIMIT HIT (2026-08-07, ~00:03 UTC / ~01:03 BST)

**Five background agents failed simultaneously** (legs 236, 226, 248, verify-256, and leg 261's
sibling checks) with the identical error: `"You've hit your session limit · resets 1am
(Europe/London)"`. This is an account-wide usage limit, not an individual agent failure — it is
external to this run and cannot be worked around by retrying. **The orchestrator stopped
dispatching new agents the moment this was detected**, per the same discipline as an
externally-forced stop (this is not a graceful user-requested close, nor a context-exhaustion
handoff — those get different procedures; this is neither).

**What the orchestrator did before pausing, all completed and pushed to `main`:**

1. Checked every failed agent's worktree for salvageable work.
2. **Leg 261 (P1A2, relaxed fluid census) had actually finished** — a complete, well-documented
   GATE NO (0 survivors of 18 fluid rows under the relaxed evidence tier; screen (iv_a),
   Remark 40's stated reach, kills all 18 because incompressibility is a nonlocal constraint no
   fluid row can pass by construction) — its agent just died before running its own finish
   protocol. The orchestrator verified territory, rebased, ran the merge gate (PASS), and pushed
   it to `main` on the leg's behalf: commit `28545ce`.
3. **Legs 236, 226, and 248 had real but incomplete work** (repairs in progress, one runner
   partially written). Salvaged as WIP and pushed to new branches — **none merged, none gated,
   raw salvage only**:
   - `leg/236-rddep-v1-wip2` — 699-line runner in progress (D3/D4 exclusion-axis analysis)
   - `leg/226-pnr-v1-wip2` — repair to `solver/profile_newton.py` in progress (D2 gauge test +
     D3 decay-class test being wired into `converged`)
   - `leg/248-cnr2-v1-wip2` — repair to `solver/collocation_newton.py` in progress (leg 150's
     absolute-companion fix)
4. **verify-256 (leg 256's post-landing verifier) had nothing to salvage** — no commits, no
   uncommitted changes at time of failure. Leg 256 itself already landed clean on `main` at
   `68c74de` before its verifier died; the verifier's own review is simply unfinished and needs
   re-dispatching once the session limit resets.

## What the next orchestrator (or this same session, once the limit resets) must do first

1. **Do not immediately re-dispatch a fresh batch of ten agents.** Check whether the usage limit
   has actually reset (the error names ~1am Europe/London; confirm the current time is past
   that before assuming capacity is back) — a premature re-dispatch will likely fail identically
   and waste the attempt.
2. Resume/recreate the Decision Maker (Fable 5) — it was mid-cycle, DIRECTION.md is its own
   durable state and is fully current as of this pause (commit `6a795cd` and earlier, all synced
   to `main`).
3. **Re-check every "live" slot's actual state before trusting it** — five of them were
   interrupted mid-flight (see below); their agent processes are gone.
4. Re-spawn fresh agents for the interrupted slots, resuming from the WIP branches above where
   real work exists (236, 226, 248) or from a clean restart where nothing was salvageable
   (verify-256's re-dispatch).

## Live-slot roster at pause (branches, not live-process guarantees)

| Slot | Leg | Route | Branch | State at pause |
|---|---|---|---|---|
| A | 266 | P0TC (rework) | not yet dispatched | DM drafted this rework leg (re-poses leg 251's certificate obligation #1 per the verifier's finding) but the orchestrator had not dispatched it before the limit hit — **dispatch this first**, it's blocking the user-facing packet on leg 251. |
| B | 249 | H2CV2 | `leg/249-h2cv2-v2` | Was mid-flight (independently re-deriving leg 176's certificate, found leg 176's "truncation-independent" tail descriptor may not hold at quoted precision — potentially real gap in PUB2's 4.026 figure). Last nudge sent, no completion notification received before the limit hit — **status unknown, re-check the branch for a finished commit before assuming it needs a full restart.** |
| C | 260 | DSSB | `leg/260-dssb-v1` | Was mid-flight (Entry B scoping: function space/object/price for the DSS expensive entrance). Status unknown at pause — re-check branch. |
| D | 221 | BVRR | `leg/221-bvrr-v1` | Was mid-flight, firmly re-nudged twice, found live orphaned processes writing to its own comparison baseline. Status unknown at pause — re-check branch. |
| E | 248 | CNR2 | `leg/248-cnr2-v1-wip2` | **CONFIRMED interrupted, WIP salvaged** (see above). Real repair in progress, not finished. |
| F | 236 | RDDEP | `leg/236-rddep-v1-wip2` | **CONFIRMED interrupted, WIP salvaged** (see above). Runner in progress, not finished. |
| G | 267 | FDL | not yet dispatched | DM drafted this fresh literature leg (precedent census for BCG's stability-step argument shape) but the orchestrator had not dispatched it before the limit hit. |
| H | 261 | P1A2 | — | **LANDED** by the orchestrator on the leg's behalf, commit `28545ce`. Slot is genuinely vacant, needs a fresh assignment from the DM. |
| I | 252 | VBRG | `leg/252-vbrg-v1` | Was mid-flight, nudged to finish in foreground. Status unknown at pause — re-check branch. |
| J | 226 | PNR | `leg/226-pnr-v1-wip2` | **CONFIRMED interrupted, WIP salvaged** (see above). Repair in progress, not finished. |

**Support in flight at pause:** verify-256 (leg 256's post-landing verifier) — confirmed dead,
nothing salvageable, needs a fresh re-dispatch.

## What this session accomplished before pausing (full detail in `experiments/JOURNAL.md`'s
tail and the git log)

This was an extremely eventful single cycle. Landed on `main`: legs 250 (PUB2 σ_min citation
fix, verified), 258 (composition floor locked into code), 255 (Phase 1 census, verified), 178
(WES, landed under the user's ruling), 256 (Breden-Chu reproduction, gate YES), 261 (relaxed
fluid census, gate NO — landed by the orchestrator post-agent-death). The user's ruling on leg
254 (DSS ban split) was applied directly to `plan_of_record.py`. The user's ruling on leg 178
(WES) was forwarded, processed by the DM, and executed.

**The single most consequential event: leg 251 (Phase 0) named its Phase-1 candidate** — the 3D
compressible Navier-Stokes imploding self-similar profile (BCG/CGSS, γ=7/5), explicitly flagged
as compressible NS, not the incompressible system Clay's problem asks about. Parked as PR #20,
NOT merged (correctly, per its own gate). An independent verifier confirmed nearly everything at
primary source but found ONE load-bearing gap: certificate obligation #1 asks to enclose a
"profile system of the dissipative equation" that doesn't exist at BCG's scaling (dissipation
enters only as a decaying forcing term, never a stationary profile term) — the real gap is in
the stability step. The DM cut a rework leg (266, drafted, not yet dispatched) to re-pose just
that one obligation before anything goes to the user as final.

Two more major escalations, both still parked pending the user's ruling:
- **Leg 253 (NRSX)** — pinned the NRS/Tsai exclusion at full text, narrowed Phase 0's survivor
  classes, surfaced a fourth candidate class (Pineau-Vicol rotated self-similar, 28-day-old
  preprint) — later independently confirmed viable by leg 262's adversarial full-text read
  (landed on `main`), which also found the class necessarily has infinite kinetic energy, so
  even total success there resolves Perelman's conjecture, not Clay.
- **Leg 257 (P1C)** — confirmed the stage-V ban's lift clause is satisfied on paper (Breden-Chu's
  H²(µ) space evades all three prior death mechanisms) but independently found a NEW obstruction
  (the Leray projection provably leaves L²(µ)) that closes the fluid route through this space
  regardless of the ban question.

**⚠ NEEDS YOU, as of pause** (also in `PROGRESS.md`, more current):
1. Leg 257's stage-V ban-lift recommendation (the DM drafted a recommendation: lift it, since
   the space is validated for non-fluid targets even though the fluid route is independently
   closed) — awaiting the user's ruling.
2. Leg 251's named candidate — awaiting the verifier-confirmed correction (leg 266, drafted, not
   yet dispatched) before it should be treated as final, and awaiting the user's read once
   corrected.
3. Leg 129/188 (Bowman dealiasing rule, escalation #4) — still parked, unchanged this session.

## Run

| Field | Value |
|---|---|
| `main` SHA at pause | `28545ce04979bf0f337ad0f3ba93ca3c60436672` |
| Highest leg number drafted | 267 (leg 268 next) |
| Stop reason | External, hard usage limit (account-wide, not context or user-requested) — resets ~1am Europe/London |
| Self-chain scheduled? | No — this is a pause expecting the same session (or a manually-restarted one) to resume once capacity returns, not a context-exhaustion handoff |
