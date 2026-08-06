# ORCH_STATE — orchestrator handoff

**Owner: the orchestrator.** Written at every handoff (`ORCHESTRATION.md` §9d) and at every
stop. A fresh orchestrator session reads this at Step 0b.5 **before dispatching anything**.

**Why it records branches and not agent handles:** subagent handles do not survive the session
that spawned them. The next orchestrator cannot message this session's agents. It can only
gate and merge what their branches contain, and re-spawn fresh agents for the next cycle's
queue.

---

## Status

**Proactive handoff after one integration cycle, following the RemoteTrigger self-chain from
the prior session.** This session resumed from the prior handoff, cleared its priority-0 and
resume-checklist items (gated/merged 5 ready branches, resolved the leg-83 merge-order
question, confirmed leg 106's "uncertain" state was actually complete and merged it), got a
fresh queue from a freshly-spawned Decision Maker, and dispatched 13 fresh background agents
(2 re-spawned lost legs, 7 new exploration legs, 4 bench-repairs/investigations). It is handing
off now — before those 13 agents finish — to stay inside a safe context budget, since this
session already did substantial merge/audit work before dispatching. **This is earlier than
a typical handoff** (no full integration loop cycle completed on the newly-dispatched agents
yet) — the next orchestrator's first job is to collect their results, not to assume a cycle
already happened on them.

## Resume checklist for the next orchestrator

0. **Two RED tests on `main`, status changed since the last handoff — re-confirm, do not
   assume.** `test_fractional_boussinesq.py` gate G6 (`p > 0` at `s=0.10`) is CONFIRMED still
   red (`p = -0.211`) as of this session's direct test run. `test_profile_newton.py`,
   surprisingly, **passed cleanly** when run directly on `main` at this session's start —
   `converged=False` at `a=0.9`, relres 1.6e-04, consistent with the test's own assertion —
   which contradicts leg 71's finding of an inverted assertion (`assert not converged`
   satisfied by convergence, relres 2.89e-06). **A bench agent (branch
   `bench/fix-red-tests-g6-newton`, running now, not yet landed) was dispatched to
   investigate both and reconcile the discrepancy.** Check its branch first; do not re-run
   the tests and assume the earlier finding without reading its report.
1. Read `plan_of_record.py` — stage `NG` is still `NEXT`. Unchanged this session.
2. Read `DIRECTION.md` — the DM (fresh Fable 5 spawn, agent name not portable — recreate
   fresh, its durable state is entirely in the file) added 15 new candidate legs (110-124)
   and filled 7 open exploration slots (110 L1R, 111 WE, 112 AS2, 113 MS, 114 CNA, 116 NKA,
   120 SUA) in a 2026-08-06-dated block appended near the end of the file plus a refreshed
   live-assignments table around line ~471-530. Reserve queue after these seven: existing
   legs 103 (GLB) and 104 (BVB, now dispatchable since 92/99 landed), then 115, 117-119,
   121-124.
3. **13 agents are running in the background as of this handoff, none yet collected:**

   | Leg | Route | Branch | Kind |
   |---|---|---|---|
   | — | red-test investigation | `bench/fix-red-tests-g6-newton` | bench, branch-only (do not merge without review) |
   | 100 | HNA repair | `bench/fix-holder-norms-nan-blind-validation` | bench, branch-only |
   | 101 | OLA repair | `bench/fix-op-lower-bound-violation` | bench, branch-only |
   | 107 | FIA repair | `bench/fix-first-integral-support-extrapolation` | bench, branch-only |
   | 58 | NG (critical path) | `leg/ng-v1` | leg, pushes itself to `main` on landing |
   | 62 | CP | `leg/cp-v1` | leg, pushes itself to `main` on landing |
   | 110 | L1R | `leg/l1r-v1` | leg, pushes itself to `main` on landing |
   | 111 | WE (heavy) | `leg/we-v1` | leg, likely escalates rather than merges (see gate) |
   | 112 | AS2 | `leg/as2-v1` | leg, pushes itself to `main` on landing |
   | 113 | MS | `leg/ms-v1` | leg, pushes itself to `main` on landing |
   | 114 | CNA | `leg/cna-v1` | leg, pushes itself to `main` on landing |
   | 116 | NKA | `leg/nka-v1` | leg, pushes itself to `main` on landing |
   | 120 | SUA | `leg/sua-v1` | leg, pushes itself to `main` on landing |

   **None of these agent handles survive this session.** For any branch not yet visible on
   `git ls-remote origin` when you read this, the agent is still working — do not assume it
   died; check timestamps/activity if uncertain, and only re-spawn from `DIRECTION.md`'s entry
   if the branch genuinely never appears after a reasonable wait. The 4 "bench, branch-only"
   items are deliberately NOT set up to self-merge — they touch flagged-priority or
   already-contentious ground (the red tests; three separate silent-corruption repairs) and
   the orchestrator should read their findings before merging, not merge blind.
4. **Two open escalations, unchanged from the prior handoff, still parked for the user, NOT
   for the DM or orchestrator to resolve:**
   - **Leg 63 (Route-M2) + stage V's ban, paired.** The first target candidate in 63+ legs
     where the method's own multiplier/shift screen says "this could work" — gCLM with full
     Laplacian dissipation (γ=2), proved blow-up, no existing certificate — but it's
     dissipative, which needs stage V's ban lifted, and that ban's lift condition (re-posing
     for a fluid transport model, which needs L1 first) is now measured dead in both L1
     realizations. Branch `leg/m2-v1`, pushed, not merged, unchanged this session.
   - **Leg 60 (Route-PQ).** A banked negative result partially fails reproduction from its
     own stored data — two ban-bearing numbers reproduce exactly, two other quoted numbers do
     not (a mislabelled ratio, a probable transcription slip). Branch `leg/pq-v1`, pushed, not
     merged, unchanged this session. (Leg 110, dispatched this session, extends this exact
     audit pattern to legs 54/56's L1 death certificates — watch for interaction.)
5. **This session's exit criterion question is unchanged and still open:** what is the exit
   criterion for this project, given Clay is at ~0.05% and unmoved, and the prize target
   (Tier-3 result) has one open critical-path leg (58/NG) left before either a real negative
   theorem or a capped "measured, not proved" report? Not urgent — leg 58 is running now and
   its answer may clarify this on its own.

## This session's landings (2026-08-06, before the 13-agent dispatch)

Confirmed via direct `git diff` inspection (not just trusting commit messages) that each merge
was either a genuine net-new addition or a safe no-op on code — none introduced a regression:

- `bench/fix-boussinesq-silent-corruption` (leg 89), `bench/fix-boussinesq-velocity-origin-fit`
  (leg 99), `bench/fix-gclm-silent-corruption` (leg 92) — merged. Each verified: zero net
  diff on the affected `solver/*.py` file relative to pre-merge `main` (the code fix was
  already bundled in from an earlier session; these merges only added the missing
  quartet files — journal, novelty writeup, adversarial test, curated JSON — that had never
  landed). Merge gate PASS before and after each.
- `bench/fix-marginal-flow-gate11-coverage` (leg 83) — merged directly, superseding the
  unmerged `leg/mfg-v1` (confirmed via `git merge-base --is-ancestor` that the repair branch
  is NOT built on `leg/mfg-v1` but is a strict superset of its content plus the actual fix,
  resolving the merge-order question the prior handoff flagged as unresolved). Merge gate
  PASS.
- `leg/hpa-v1` (leg 106) — merged. The prior handoff flagged this as "agent failed mid-response,
  state uncertain" — on inspection the branch had its full quartet already pushed (2 clean
  commits) and the failure was only a post-push API error. No re-dispatch needed.
- `bench/fix-interval-certificate-validation` (leg 98) — **checked and deliberately NOT
  merged.** Confirmed via `git diff` that its `solver/interval_certificate.py` change is
  already byte-identical on `main` (bundled in earlier, per the prior handoff's note) and its
  other files (journal, adversarial test) already exist on `main` via a different path — this
  branch is a stale fork now missing 14 files' worth of newer `main` content in its own
  three-dot diff. Left un-merged and un-deleted; safe to ignore or prune later.
- Approximately 20 other remote branches (`verify/*`, `docs/2026-08-05`, `prep/*`,
  `repro/2026-08-05`, `lit/tc-v1`, and 4 more `bench/fix-*`) were checked with
  `git rev-list --count` and found 163-307 commits behind current `main` — i.e. stale forks
  from well before this session's rebases, already superseded. Not investigated further;
  flagged here in case that judgment call needs revisiting, but the volume and staleness
  pattern strongly suggests they are dead ends, not lost work.

## Run

| Field | Value |
|---|---|
| Cycles completed | 0 full integration-loop cycles on the newly-dispatched 13 agents (this handoff happens before the first collection pass) |
| `main` SHA at handoff | `4975ea0` |
| Highest leg number used | 124 (DM's reserve queue) — 13 agents currently in flight are legs 58, 62, 100, 101, 107, 110, 111, 112, 113, 114, 116, 120, plus the unnumbered red-test bench investigation |
| Reason for handoff | Proactive — substantial merge/audit/dispatch work already done (5 merges, 2 lost-leg respawns, 1 DM cycle, 7 new leg dispatches); handing off before burning further context on a full collection+re-dispatch loop |

## To resume

Paste the full text of `ORCHESTRATOR_PROMPT.md` into a fresh Claude Code session set to
Sonnet 5, in this repository — or, per §9e, the self-chain `RemoteTrigger` scheduled at the
end of this session should fire automatically.
