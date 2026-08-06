# ORCH_STATE — orchestrator handoff

**Owner: the orchestrator.** Written at every handoff (`ORCHESTRATION.md` §9d) and at every
stop. A fresh orchestrator session reads this at Step 0b.5 **before dispatching anything**.

**Why it records branches and not agent handles:** subagent handles do not survive the session
that spawned them. The next orchestrator cannot message this session's agents. It can only
gate and merge what their branches contain, and re-spawn fresh agents for the next cycle's
queue.

---

## Status

**Proactive handoff — not a stop file.** This session ran one extremely long, extremely
productive integration cycle (still logically "cycle 1" from the prior resume, spanning the
2026-08-05→06 date boundary and dozens of leg landings) and is handing off now, well past the
volume that would normally trigger a 12-cycle handoff, to avoid running the session past a safe
context budget. Nothing is broken; the run is healthy and should resume immediately.

## Resume checklist for the next orchestrator

1. Read `plan_of_record.py` — stage `NG` is still `NEXT`.
2. Read `DIRECTION.md` in full — it is long (100+ candidate legs drafted across this session)
   but its Status section and live-assignments table are current as of this handoff (see
   below). The DM (agent name/id not portable across sessions — recreate fresh, its durable
   state is entirely in `DIRECTION.md`) has been very productive; trust the file over any
   assumption.
3. **Read `PROGRESS.md`'s `⚠ NEEDS YOU`** — it is git-ignored and NOT committed, so also check
   this file's "Open escalations" section below, which is the durable copy.
4. **This is the single highest-priority item**: leg 63 (Route-M2, escalation #1) found the
   first candidate in the whole project where the method's own multiplier/shift screen says
   "this could work" — gCLM with full Laplacian dissipation (γ=2), proved blow-up, no existing
   certificate. It is dissipative, which runs into stage V's ban (needs L1 first, and L1 is
   measured dead in both realizations) — escalation #2. These two escalations are now a pair
   and the single most consequential open decision in the project. Branch `leg/m2-v1` pushed,
   not merged.
5. Also leg 58 (NG, critical path) may be building toward something stronger than its original
   mandate — an unconditional `Z₁ ≥ 1` kernel result for every bounded approximate inverse, not
   just block-diagonal. Was still in progress at handoff, not yet pushed. Its agent handle does
   not survive — if no fresh push has appeared on `leg/ng-v1` by the time you read this,
   **re-spawn LEG-A fresh on the same brief** (`CONTINUATION_PROMPT.md` DIRECTIVE 1 plus the
   interim finding described in `PROGRESS.md`) rather than assuming it's still working.

## Run

| Field | Value |
|---|---|
| Cycles completed (loose count) | 1 very long cycle, effectively many integration passes |
| `main` SHA at handoff | `63dc163` (verify with `git log -1 origin/main` — may have advanced) |
| Highest leg number used | 108 (queue extends to 109 in reserve) |
| Reason for handoff | Proactive, to stay well inside a safe context budget given this cycle's exceptional length (100+ legs dispatched/landed, dozens of merges) |

## Live assignments at handoff (from `DIRECTION.md`, may have moved on)

| Slot | Leg | Route | Branch | Status at handoff |
|---|---|---|---|---|
| LEG-A | 58 | NG (critical path) | `leg/ng-v1` | Mid-build, interim finding may be stronger than mandate (see above). No push yet. |
| LEG-B | 62 | CP | `leg/cp-v1` | Gate answered NO, full writeup still assembling. No push yet. |
| LEG-C | 107 | FIA | `leg/fia-v1` | Dispatched, no completion yet. |
| LEG-D | — | open | — | Held for leg 76 (MI), pending its verifier's confirmation of leg 70's finding. Verifier (for leg 70) was still deepening its review at handoff — found the core finding solid, expanding scope (leg 70 never recomputed its own K-counts; a wording defect; a sharper continuum signature). Leg 76 not yet drafted as a dispatchable leg — do that once the verifier lands. |
| LEG-E | 100 | HNA | `leg/hna-v1` | **Landed with a finding, just before handoff.** Gate answered YES — `solver/holder_norms.py` has 6 silent-corruption mechanisms under NaN/Inf poisoning (all one IEEE-754 hazard: NaN compares unordered, so ordered-comparison filters silently drop poisoned items), including its own `conformal_check` self-validation routine returning a bit-identical "clean" result on a poisoned grid, and one case understating a bound by 2.1053x. Blast radius: no live certificate feeds NaN into this module, so no banked number is affected — but `conformal_check` can no longer be trusted as a self-validation gate until repaired. Branch pushed, held off main, PR #16 open. **Needs a bench-repair** (same pattern as legs 66/79/83/85/89/91/92/98/99 before it — dispatch one and bundle leg 100's unmerged commits, following `bench/fix-fractional-gclm-negative-params` as the template) before its slot can close out cleanly. |
| LEG-F | 71 | CAP | `leg/cap-v1` | Dispatched very early in the session, no completion notification ever received — likely still running, or check for a pushed branch. |
| LEG-G | 106 | HPA | `leg/hpa-v1` | Dispatched, no completion yet. |
| LEG-H | — | open | — | Leg 108 (IX2) just landed on main (`63dc163`), gate NO, mechanical, clean. Needs a fresh dispatch — reserve 103/104/105 are candidates (see below). |
| LEG-I | 101 | OLA | `leg/ola-v1` | Dispatched, no completion yet. |
| LEG-J | 102 | JR2 | `leg/jr2-v1` | Landed on main, gate NO, mechanical, clean. Table not yet refilled — needs a fresh dispatch too. |

**All agent handles above are unreachable from a fresh session.** For any slot showing "no
completion yet," check `git ls-remote origin 'refs/heads/leg/<slug>-v1'` — if a branch exists,
gate and merge/review it per its outcome; if not, the agent's work is lost and the slot should
be re-spawned fresh from `DIRECTION.md`'s entry for that leg number (the specs are fully
written, no need to re-derive them).

## Support agents live at handoff

| Agent | Task | Branch | Status |
|---|---|---|---|
| VER (leg 70) | Deepening post-landing review of leg 70's Morse-index finding | `verify/70-rc-review` | In progress at handoff — check for a push before re-spawning. |
| BENCH | gclm_rescaled.py gauge-relative tolerance fix (leg 85) | `bench/fix-gclm-rescaled-gauge-tolerance` | Was nudged twice for background-wait stalls; likely close to done — check for a push before re-spawning. If a push exists, it bundles leg 85's own commits (`leg/gra-v1` must NOT be merged separately). |
| BENCH | interval_certificate.py verdict-validation fix (leg 98) | `bench/fix-interval-certificate-validation` | In progress at handoff — specifically re-checking leg 61's Kawahara gate for impact. Check for a push before re-spawning. If a push exists, it bundles leg 98's own commits (`leg/ica-v1` must NOT be merged separately). |

## Reserve queue (from `DIRECTION.md`, ranked)

- **103, 104** — post-repair regression closures for the gclm.py (leg 92) and
  boussinesq_velocity.py (leg 99) fixes. **Both fixes have now landed on main**, so these two
  are unblocked and immediately dispatchable — good candidates for LEG-H/LEG-J's refill.
- **105** — post-repair regression closure for interval_certificate.py (leg 98)'s fix. **Still
  blocked** until the bench-repair above lands.
- **109** — adversarial audit of `reduced_certificate.py`'s self-consistency claim. Unblocked,
  dispatchable.

## Open escalations (durable copy — `PROGRESS.md` is git-ignored)

1. **`NG` entering the committed sequence — escalation #1, already applied**, under the user's
   pre-delegation. Reversible.
2. **Stage `V`'s ban-lift condition may be permanently unmeetable** — `L1` measured dead in
   both realizations.
3. **What is the exit criterion for this project?**
4. **Escalation #4 (leg 60, Route-PQ)** — a banked negative result partially fails reproduction
   from its own stored data (both ban-bearing numbers reproduce exactly; two other quoted
   numbers do not — a mislabelled ratio, a probable transcription slip). Branch `leg/pq-v1`
   pushed, not merged.
5. **NEW, highest priority — escalation #1+#2 paired (leg 63, Route-M2)**: the first target
   candidate in 63+ legs where the method's own screen says "this could work" (gCLM with full
   Laplacian dissipation, γ=2) — but it's dissipative, which runs straight into escalation #2
   above. See "Resume checklist" item 4. Branch `leg/m2-v1` pushed, not merged.
6. Leg 58 (NG) may land a materially stronger no-go than its original mandate. Not yet pushed
   at handoff.

## What this session accomplished (summary — full detail in `reports/REPORT_2026-08-05.md`'s
addendum and the individual leg quartets)

Roughly 40 legs landed (numbers 58-108, with some still in flight or parked). Nine real,
independently-confirmed infrastructure bugs found by the adversarial-audit pattern and fixed
with rigorous zero-regression proofs: `interval.py` (subnormal/NaN), `spectral_utils.py`
(odd-n derivative), `port_certification.py` (fabrication acceptance), `target_norm.py` (silent
domain extrapolation), `gclm_rescaled.py` (gauge-relative tolerance, in flight),
`boussinesq.py` (false blowup flag + 3 more), `gclm.py` (4 silent-corruption mechanisms),
`fractional_gclm.py` (negative-parameter acceptance), `boussinesq_velocity.py` (empty-window
origin fit). In every case, the fix was independently checked against every banked/production
measurement that could plausibly be affected, and confirmed clean (bit-identical, zero
regression) — most notably leg 55's target_norm margins, leg 73's Lamb benchmark, leg 61's
Kawahara gate (check in flight), and `stage1_5_sweep.py`'s banked gCLM runs.

Two new external known-answer gates banked (leg 61's Kawahara reproduction, leg 73's Lamb
corner-image reproduction). Two journal/index freshness audits closed real staleness gaps
(legs 72, 68's original passes plus this session's 102, 108 second passes). Multiple
literature watches confirmed no external development has mooted this repository's own work
(legs 74, 77, 82, 90, 93).

**Clay unchanged at ~0.05%. No link of the L1→L4 chain has moved.** The escalation #1+#2 pair
above (leg 63) is the first genuinely new strategic option to appear in many legs, and it is
squarely the user's call, not the DM's or orchestrator's.

## To resume

Paste the full text of `ORCHESTRATOR_PROMPT.md` into a fresh Claude Code session set to
Sonnet 5, in this repository.
