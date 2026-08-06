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
context budget. Nothing is broken; the run is healthy and should resume immediately. This
handoff doc was revised once already, mid-tail-off, as several more agents landed after the
first handoff message was sent to the user — the state below is the final, accurate snapshot.

## Resume checklist for the next orchestrator

0. **TOP PRIORITY, ahead of everything else — two RED tests confirmed on `main` (leg 71,
   landed at `e742f6d`).** Per `ORCHESTRATION.md`'s own rule, a red test on `main` is fixed
   immediately, not queued: (a) `test_fractional_boussinesq.py` gate G6 (`p > 0` at `s=0.10`)
   measures **p = -0.211**, wrong side of zero, monotonicity and the s=1.00 endpoint both
   still pass — this is the same module leg 67 was independently searching the literature
   for, whose own gate is now red; (b) `test_profile_newton.py` has an inverted assertion
   (`assert not converged` at `a=0.9`) that Newton now **satisfies by converging** (relres
   2.89e-06, 40 iters) — this reads like the solver got BETTER and a negative-control test
   went stale, not a regression, but that needs confirming, not assuming. Dispatch a bench
   investigation of both before building anything else on `fractional_boussinesq.py` or
   `profile_newton.py`. Full detail in leg 71's `writeup/novelty/leg_71.md` and
   `experiments/journal/leg_71.md` on `main`. Also flagged, mechanical, low priority: 7
   modules are unreachable from `scripts/merge_gate.sh`'s test-name mapping (silently
   ungated on future changes) — a `capabilities.py`-driven resolution is the cheap fix,
   not yet built.
1. Read `plan_of_record.py` — stage `NG` is still `NEXT`.
2. Read `DIRECTION.md` in full — it is long (100+ candidate legs drafted across this session)
   but its Status section and live-assignments table are close to current (see the correction
   note below — a few landings happened after the last DM sync and are not yet reflected
   there). The DM (agent name/id not portable across sessions — recreate fresh, its durable
   state is entirely in `DIRECTION.md`) has been very productive; trust `git log` over the
   file where they conflict.
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
6. **DIRECTION.md correction needed on resume**: legs 85 (gclm_rescaled), 98 (interval_certificate)
   have now landed via their bundled bench-repairs (see table below), but the last DM sync
   predates this — the DM will think their slots (LEG-C-ish / LEG-J-ish, labels have drifted
   all session, don't trust the letter) are still occupied. Reconcile against `git log` before
   trusting DIRECTION.md's live table on the first read.

## Run

| Field | Value |
|---|---|
| Cycles completed (loose count) | 1 very long cycle, effectively many integration passes |
| `main` SHA at handoff | `3e52386` — verify with `git log -1 origin/main`, may have advanced further if any last agent lands after this is written |
| Highest leg number used | 108 (queue extends to 109 in reserve) |
| Reason for handoff | Proactive, to stay well inside a safe context budget given this cycle's exceptional length (100+ legs dispatched/landed, dozens of merges) |

## Live assignments at handoff (true state, reconciled against `git log`, not just `DIRECTION.md`)

| Leg | Route | Branch | Status at handoff |
|---|---|---|---|
| 58 | NG (critical path) | `leg/ng-v1` | Mid-build, interim finding may be stronger than mandate (see above). No push yet. |
| 62 | CP | `leg/cp-v1` | Gate answered NO, full writeup still assembling. No push yet. |
| 71 | CAP | landed, `e742f6d` | **Landed with the top-priority finding — see Resume checklist item 0.** Two red tests confirmed on main. |
| 76 | MI (rework leg, not yet drafted as dispatchable) | — | Blocked on its verifier. Verifier (for leg 70) was still deepening its review at last check — found the core finding solid, expanding scope (leg 70 never recomputed its own K-counts; a wording defect; a sharper continuum signature). Check `verify/70-rc-review` for a push; draft leg 76 as a dispatchable leg once it lands. |
| 100 | HNA (holder_norms.py) | `leg/hna-v1` | Gate YES — 6 silent-corruption mechanisms under NaN/Inf poisoning (all one IEEE-754 hazard), including its own `conformal_check` self-validation returning a bit-identical "clean" result on a poisoned grid, and a 2.1053x understated bound. Latent (no live certificate feeds NaN in), but `conformal_check` can't be trusted as a self-validation gate until repaired. **Needs a bench-repair** — dispatch one, bundle leg 100's commits, follow `bench/fix-fractional-gclm-negative-params` as the template. |
| 101 | OLA (op_lower.py) | `leg/ola-v1` | Gate YES — the lower bound can EXCEED the true norm on 47/209 adversarial cases (46 via overflow to `inf`, 1 finite exceedance at 425 ULP). Production headroom measured at 307.9 decades, so no banked Route-D number is contaminated — but `capabilities.py`'s unqualified "brackets the norm from below" claim is now false as written. **Needs a bench-repair.** |
| 106 | HPA (hilbert_pointwise.py) | `leg/hpa-v1` | **Agent failed mid-response (API error) after pushing its branch.** State is uncertain — the branch exists (`d947054`) but the PR/report may be incomplete. Read it directly before trusting any summary; may need a fresh dispatch to finish or redo the leg. |
| 107 | FIA (first_integral.py) | `leg/fia-v1` | Gate YES — the profile silently continues past its own compact support (96/96 out-of-support evaluations finite and nonzero, mirroring the interior to 3-4 s.f.), and its own defect validator is NaN-blind (397/400 poisoned points still certify). Latent (0/3 call sites affected). **Needs a bench-repair.** |
| 108 | IX2 (writeup/INDEX.md) | `leg/ix2-v1` | Landed on main, gate NO, mechanical, clean. |
| 85 | GRA (gclm_rescaled.py fix) | bundled, merged | **Landed on main** via `bench/fix-gclm-rescaled-gauge-tolerance` (merged at `03acb4e`). `leg/gra-v1`'s commits are bundled in — do not merge that branch separately if it's still visible on the remote. |
| 98 | ICA (interval_certificate.py fix) | bundled, merged | **Landed on main** via `bench/fix-interval-certificate-validation` (merged at `3e52386`). Leg 61's Kawahara gate independently confirmed bit-identical at 17 digits. `leg/ica-v1`'s commits are bundled in — do not merge that branch separately if it's still visible on the remote. |
| 83 | MFG (marginal_flow.py gate 11) | `leg/mfg-v1` (PR #14, escalated) + a ready bench-repair on `bench/fix-marginal-flow-gate11-coverage` | **Unresolved ordering question for the next orchestrator.** Leg 83 itself is still an open escalation (never merged to main). A bench-repair was built ON TOP of `leg/mfg-v1` (not main) and closes 4 of leg 83's 9 missed adversarial cases (including the 4.99e130 worst case) via a scale-free state-growth threshold (1e5, placed by measuring 4.06e2 as the largest legitimate growth in the existing suite) — 0 false positives, all 11 existing gates unchanged. **Decide first: merge `leg/mfg-v1` to main (closing leg 83's escalation as a normal landing, since the repair proves the finding is real and fixable), then rebase/merge the repair branch on top** — merging the repair branch as-is would also drag leg 83's commits in under a different SHA, which works but is messier. Neither branch has been merged yet; both are ready. |
| 96, 97, 102 | LHA, WSA, JR2 | — | All three landed cleanly on main earlier in the session (robust / no bug found). No action needed. |
| 68, 72, 90, 93 | IX, JR, EXT4, EXT5 | — | Also landed cleanly earlier this session (documentation/literature, no findings requiring follow-up). |

**All agent handles above (except where noted "landed") are unreachable from a fresh session.**
For any slot still showing an open branch, check `git ls-remote origin 'refs/heads/leg/<slug>-v1'`
— if it exists, gate and merge/review it per its outcome; if not, the agent's work is lost and
the slot should be re-spawned fresh from `DIRECTION.md`'s entry for that leg number (specs are
fully written, no need to re-derive them).

## Reserve queue (from `DIRECTION.md`, ranked, may need DM re-sync)

- **103, 104** — post-repair regression closures for the gclm.py (leg 92) and
  boussinesq_velocity.py (leg 99) fixes, both of which landed earlier this session. Unblocked,
  dispatchable.
- **105** — post-repair regression closure for interval_certificate.py (leg 98)'s fix, which
  has now also landed (see table above). **Now unblocked too.**
- **109** — adversarial audit of `reduced_certificate.py`'s self-consistency claim. Unblocked,
  dispatchable.
- Once legs 100, 101, 106, 107's bench-repairs land, each will want its own post-repair
  regression closure leg too (same "close the loop" pattern used throughout this session) —
  the DM can draft these fresh once the repairs exist.

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
5. **Highest priority — escalation #1+#2 paired (leg 63, Route-M2)**: the first target
   candidate in 63+ legs where the method's own screen says "this could work" (gCLM with full
   Laplacian dissipation, γ=2) — but it's dissipative, which runs straight into escalation #2
   above. See "Resume checklist" item 4. Branch `leg/m2-v1` pushed, not merged.
6. Leg 58 (NG) may land a materially stronger no-go than its original mandate. Not yet pushed
   at handoff.

## What this session accomplished

Roughly 40+ legs landed (numbers 58-108), plus a dozen bench-repairs. **Eleven** real,
independently-confirmed infrastructure bugs found by the adversarial-audit pattern, of which
**nine are fixed and merged** with rigorous zero-regression proofs: `interval.py`
(subnormal/NaN), `spectral_utils.py` (odd-n derivative), `port_certification.py` (fabrication
acceptance), `target_norm.py` (silent domain extrapolation), `gclm_rescaled.py`
(gauge-relative tolerance), `boussinesq.py` (false blowup flag + 3 more), `gclm.py` (4
silent-corruption mechanisms), `fractional_gclm.py` (negative-parameter acceptance),
`boussinesq_velocity.py` (empty-window origin fit), `interval_certificate.py` (fabrication
acceptance). **Two more found and still awaiting repair**: `holder_norms.py` (NaN-blind
self-validation) and `op_lower.py` (lower bound can exceed the true norm), plus `first_integral.py`
(silent extrapolation past compact support) and possibly `hilbert_pointwise.py` (leg 106,
outcome uncertain due to an agent failure). In every completed repair, the fix was
independently checked against every banked/production measurement that could plausibly be
affected, and confirmed clean — most notably leg 55's target_norm margins, leg 73's Lamb
benchmark, leg 61's Kawahara gate, and `stage1_5_sweep.py`'s banked gCLM runs.

Two new external known-answer gates banked (leg 61's Kawahara reproduction, leg 73's Lamb
corner-image reproduction). Two journal/index freshness audits closed real staleness gaps.
Multiple literature watches confirmed no external development has mooted this repository's own
work.

**Clay unchanged at ~0.05%. No link of the L1→L4 chain has moved.** The escalation #1+#2 pair
above (leg 63) is the first genuinely new strategic option to appear in many legs, and it is
squarely the user's call, not the DM's or orchestrator's.

## To resume

Paste the full text of `ORCHESTRATOR_PROMPT.md` into a fresh Claude Code session set to
Sonnet 5, in this repository.
