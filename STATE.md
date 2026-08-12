# STATE — the compact working surface

**This file is the read surface for BOTH modes.** Read it first and read it instead of
`DIRECTION.md`. Everything else is archive, consulted only when a pointer here names it.

**Why it exists.** `DIRECTION.md` is 23,699 lines / 1.5 MB (~380k tokens). With the other
mandatory reads the per-agent load is ~480k tokens — paid by *every* agent in orchestrated
mode, and on *every task* in solo mode. That cost is pure overhead: a task needs its own
entry, the live bans, and what landed recently, not the accumulated cycle history.

**Regenerate at every landing.** Stale state is worse than no state — this file is only
trustworthy if it is rewritten as part of finishing a task, the way `JOURNAL.md` pointers are.

---

## Mode

**SOLO** — one instance, one task at a time. See `ORCHESTRATION.md` §3e for the solo contract
(verification rule, consecutive-audit cap, pre-committed next task).

*(Set to `ORCHESTRATED` and fill the roster table when running the four-slot contract. The
rest of this file is identical in both modes.)*

## Goal, ceiling, odds

- **Goal:** a full Clay solve (user ruling 2026-08-06). Prize direction is Fefferman
  statement **(C)** — breakdown on `ℝ³`.
- **Ceiling right now: Tier 2.** Route 4 produces a candidate; no certification route is
  built. `CLAY_OBLIGATIONS.md` §6 names the two obligations with **no known method**.
- **Clay odds ~0.05%**, unmoved. No `L1 → L4` link has ever moved.

## In flight

| What | State |
|---|---|
| **`PROG-R4`** (route-4 DSS programme, leg 380) | **RUNNING** — GMRES early exit landed, U2/U3 runners, DNS in flight. Seed named per the scope ruling: Lucas–Kerswell arXiv:1406.1820v2 Table IV. Tier-2 ceiling in every gate. |

## Next tasks — pre-committed, in order

Re-ranking requires its own commit stating why (`ORCHESTRATION.md` §3f). Ordering respects
§3f's cap: no more than two consecutive audit/repair/instrument tasks before construction.

1. **`PROG-R4` U2/U3 — continue the programme.** *Construction, critical path.* M1 (the
   hookstep/trust-region globalisation layer) is landed and reproduced against leg 353's
   laminar control; U2/U3 runners are built and DNS is in flight. This is a **programme**
   under §3c — one novelty pass already committed at U0, milestones not gates for build
   units, and the worker is **not** terminated on landing. Tier-2 ceiling in every gate.
2. **Leg 389 (CT2C) — wire 382's certified enclosure into the screen's second T2 column**,
   alongside the fitted one, consuming 386's δ-mode. *Instrument.* Leg 383 closed the report
   path with the **fitted** exponent per its dispatch and deliberately did not wire in the
   enclosure; `CLAY_OBLIGATIONS.md` §8 ask 2 requires certified, not fitted. Note 386's
   clause 2 first: **the δ-window is EMPTY at every `α_centre ≤ 1`**, and the banked object
   carries `α = 1`, so this task wires the path and reports the empty window honestly — it
   does not manufacture headroom.
3. **Leg 387 (DXNV) — discharge 382's owed novelty obligation.** *Literature, owed work.*
   arXiv and Semantic Scholar both returned HTTP 429 on 382's external pass; the refusal is
   disclosed at its novelty §3 and is **owed work, not new screening**, so it does not
   violate the standing stop on screening as a unit of work.

**Held behind these:** leg 388 (CRVB, bound 382's curvature-detection threshold from below —
the ladder bottomed out at ≤1e-6 and is currently one-sided).

## Open — needs the user, not a task

1. **The POCP spend.** Periodic-orbit/flow-map certification is the *only* open route for
   `CLAY_OBLIGATIONS.md` §1. Leg 348: **(ii) OPEN-AND-REACHABLE**, cost class C. Inputs cut
   both ways — exactly one viable basis (leg 374 ADVERSE, Hermite sole survivor, decay concern
   cleared by leg 377) and **no discrete spectral anchors** (leg 376, both channels continuous).
2. **Fefferman statement (D), the torus variant.** Priced by leg 390, *no recommendation
   attached by design*. It drops condition (7) bounded energy — making §4 vacuous — but
   **0 of 4 rigidity clearances carry to `T³`**, and no non-constant exactly-DSS field exists
   on `T³` (342 modes survive one DSS step at `λ=1.7`, **0 survive two**).
3. **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate
   theorems read at full text and neither reaches the screened object.

## Live bans — 19, one line each

Full text and lift conditions: `.venv/bin/python plan_of_record.py`. **Run it when a task
could touch one**; do not paraphrase from here.

gCLM measurement · DSS cheap entrance (bifurcation off a fixed point) · DSS expensive entrance
(**SCOPED 2026-08-11: a *seeded* search is outside it; name the seed or the ban applies**) ·
2D β re-measurement · scaling-gauge near-null · GA compute on unvalidated fitness ·
"closure is a property of the space" · stage V as posed · ℓ¹-Fourier/radii-polynomial on any
model · V-rigorous's L1 prerequisite (superseded) · closing the truncation gap by extending the
domain · three readings of legs 51/53 · `Z₁` block-coupling by tuning · weight exponent toward
leg 51's minimum · leg 51's finding at full strength · leg 51's zero `Y₀` as progress ·
Chen–Hou 2D as a target · leg 44's 2D near-null · building a solver without grepping
`capabilities.py`.

## Standing discipline — non-negotiable in both modes

Three-tier win condition (Tier 2 is never a proof) · pre-committed gates on every claim ·
novelty pass before construction (**once per programme**, not per unit, under §3c) ·
**lesson 91**: a negative names its realization/trial-space/basis · **§3d**: a stop fires only
on a null from an attempt resourced at the scale the question is posed at — an under-resourced
null returns a cost and answers `UNDER-RESOURCED` · planted controls that can fire both ways ·
`scripts/merge_gate.sh origin/main` must PASS · **no external outreach** · no output described
as movement toward Clay unless a link actually moved.

## Where the detail lives — consult by pointer, never wholesale

| Need | Read | Size |
|---|---|---|
| A task's own spec | `DIRECTION.md`, that entry only | 23,699 lines — never read whole |
| Bans, stage, gate | `.venv/bin/python plan_of_record.py` | executable, ~40 lines out |
| Does a module exist | `.venv/bin/python capabilities.py <term>` | executable, grep don't read |
| The contract | `ORCHESTRATION.md` §3b–§3e | 788 lines |
| What a Tier-2 candidate owes | `CLAY_OBLIGATIONS.md` | 8 sections, §4 verified |
| Strategy, walls, routes | `CLAY_ROADMAP.md` §7.5 | — |
| Per-leg record | `experiments/journal/leg_N.md`, `writeup/novelty/leg_N.md` | one leg each |
| Banked numbers | `writeup/data/*.json` | **re-derive from these, never from prose** |
