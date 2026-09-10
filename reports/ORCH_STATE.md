# ORCH_STATE — orchestrator handoff

**Owner: CONDUCTOR** (`ORCHESTRATION.md` §3g; the separate "orchestrator" role no longer exists).
Written at **every** wave boundary — with the plan (§3g step 1) and with the integration (step 4) —
and at every handoff. A fresh session reads Step 0b before dispatching anything.

**The 2026-08-14 CONDUCTOR fork is CLOSED at `5d9c065`** — `E`, `V-W2`, `T1`'s record and the C1
ruling are **DONE**; any row claiming *"`E` DID NOT RETURN"* is **stale**. Full text retired
verbatim 2026-08-18 under §3j → `## Superseded — the 2026-08-14 fork`.

---

## ⛔ OPEN ESCALATIONS — ONLY THE USER CAN RESOLVE THESE. NONE IS RULED BY THE CONDUCTOR.

Collected here 2026-08-19 at the wind-down, verified against the record rather than copied from a
list. **§3h binds: a ban is superseded by a MEASUREMENT, never a decision — and a defective ban
WORDING is a user escalation.** Each row is phrased so it can be answered **Y or N**.

| # | file | what is at stake | ANSWER Y / N |
|---|---|---|---|
| 1 | `writeup/escalations/ESCALATION_D_BUNDLING_2026-08-18.md` | **The most direction-relevant open item on the board, and it has never been ruled.** Statement **(D)** is deferred *with Lane T*, and Lane T was demoted for a reason that has nothing to do with (D). **`W4`'s only surviving clause is (c), and clause (c) IS statement (D).** So `W4` currently has **no live clause any ranked lane may attack.** | **Is "clause (c) is `W4`'s sole survivor" a re-open condition for Lane T — Y or N?** |
| 2 | `writeup/escalations/ESCALATION_W2_SCOPE_2026-08-18.md` | `W2`'s statement names **SINGULARITY** theorems; `arXiv:2509.25116` certifies **NONUNIQUENESS**. Three defensible readings; **reading three would make Lane T's re-open condition (i) LIVE.** | **Does a nonuniqueness certificate meet `W2` — Y or N?** |
| 3 | `writeup/escalations/ESCALATION_PUB0C_PUBLISHED_2026-08-18.md` | Whether an unrefereed preprint with no journal-ref is a "published work" for `PUB_0C` §1. Raised by `V-W4`. | **Is an unrefereed preprint with no journal-ref "published" for `PUB_0C` §1 — Y or N?** |
| 4 | `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md` (`T1`'s packet) | The 2026-08-13 ruling settled the apparatus question as a **SCOPE** ruling and **explicitly left the lift clause untouched and defective**. The required edit is **recorded, not applied**. | **Apply the recorded lift-clause edit as written — Y or N?** |
| 5 | `writeup/escalations/ESCALATION_LEG257_LIFT_CLAUSE_2026-08-06.md` | The stage-V lift clause was **MET ON PAPER** by leg 257 — `H²(µ)`, all three named death mechanisms evaded — and the route **closed anyway** on a FOURTH obstruction not on the ban's list (the Leray projection leaves `L²(µ)`, measured). Recorded, **not ruled**, and still **EXEMPLAR-FREE**. Distinct from row 4. | **Is the leg-257 lift clause defective as recorded — Y or N?** |
| 6 | `writeup/escalations/ESCALATION_PHASE1_TARGET_2026-08-06.md` | Leg 251 named a Phase-1 target — BCG's compressible imploding profile — and escalated rather than landed, because its gate's YES **is** §8 escalation 1. **Legs 266 and 275 exist only on that branch.** Not Clay's system; feasibility not attempted. | **Does the leg-251 candidate get the go as the Phase-1 construction target — Y or N?** |
| 7 | `writeup/escalations/ESCALATION_PHASE1_COSTING_2026-08-07.md` | Leg 265 costed it: `k(7/6) = 16.3479210517`, never evaluated before, which **corrects leg 251's ansatz** from "n odd and large" to **n = 3**. A certificate would upgrade DOMINATED → ENCLOSED and decides **no open yes/no question**. Row 7 needs row 6 to be Y first. | **Authorize Phase-1 construction against the `n = 3` BCG target — Y or N?** |

**Rows 5, 6 and 7 were carried by GitHub PRs #19, #20 and #21 from 2026-08-06/07 until 2026-09-10, when the repository was made public and the PRs were CLOSED UNMERGED.** Each PR body said in bold that it must not be merged without the user's ruling, and none was. The closure retired the *carrier* only: the questions above are **still open and still unruled**, the three branches are preserved unmerged on `origin` with their head SHAs recorded in the files above, and `PROGRESS.md` — which `ORCHESTRATION.md` §8 names as the `⚠ NEEDS YOU` home for parked branches — **does not exist**, which is why these rows are the record.

### Two DECISIONS owed that are not escalations

| # | where | the question |
|---|---|---|
| A | `writeup/CORRECTIONS.md` **§49**, and now **§54** | Does `ORCHESTRATION.md` §6 clause 3 get a `recompute-from-primary` check beside it? **§54 REVERSES the evidence I originally recorded here:** `L-JVER`'s suite is 12/12 `recompute-from-primary` **because it re-runs everything and overwrites its own artefact**, which means it did not attempt clause 3 at all. `PB2`'s suite is the mirror image (0/31, clause-3 compliant). **No suite in the record satisfies both rules, and no instrument checks which one a suite is.** |
| B | `PB1`'s finding **F2** | `experiments/JOURNAL.md:5305` and `ORCHESTRATION.md` §3k:576 give **contradictory accounts of leg 387's arXiv harness**. Leg 411 re-measured 10,780 against a recorded 10,756, favouring the journal — which puts **leg 382's queue on the wrong reading.** |

---

## LIVE — §3g CONDUCTOR, wave sizing 5. **ARC 7 — INDEPENDENT CONFIRMATION, OPEN 2026-09-10, legs 436–440.** **ALL FIVE UNITS LANDED — `K0`, `K1`, `K2`, `K3`, `K4`. THE ARC IS CLOSED; the verdict is published at `writeup/7_confirmation/`.**

**⚠ WHERE THE CONDUCTOR IS (13:10Z): the operator's LAPTOP session, by user designation at 13:00Z.** The container
Conductor (`session_01LX5qCimBmdRGUMvwBDT3DZ`) landed K1 on `main` at 1829d68 (12:55Z) after that designation and
earlier committed four K2 worker files straight to `main` (08:38–09:21Z, see below). **If that session is still
running: STOP dispatching, push branches only, never `main`.** Every laptop push is preceded by `git ls-remote`
and a rebase; a collision is recorded here, never resolved by force.

**Goal (user ruling 2026-09-10):** independently CONFIRM the OpenAI Navier–Stokes result by running the Lean
kernel to completion on its two exported theorems. Rulings 1–6 recorded: `CORRECTIONS.md` §72, `STATE.md`
arc-7 block, `ORCHESTRATION.md` §3g. Legs 436–440.

**`K1` (leg 437) — LANDED GREEN in THREE environments, `UNVERIFIED`.** Journal `experiments/journal/leg_437.md`.
Phase A (remote container 1, resume): GREEN. Phase B (remote fresh container 2): GREEN, `total_s` 5605
(`writeup/data/arc7/k1/phaseB/`). Phase B on the operator's laptop (12 cores): GREEN, `total_s` 4272
(`writeup/data/arc7/k1/phaseB_local/`, merged d526329). Same pin, mathlib `85e3a25e`, Comparator `19e111e2`, both
theorems `[propext, Classical.choice, Quot.sound]`, `sorryAx` NO, everywhere. Three limits banked, none softened:
mathlib oleans REPLAYED from cache, not rebuilt; statements are Fefferman (C)/(D), not Theorem 1.1; a second
machine is not a second agent — **`VERIFIED` only when K2 slot 5, blind, reproduces it from the banked artefacts.**


**`K1` follow-on (landed 1b9f9ea) — olean INTEGRITY established, SEMANTIC MATCH not.** The first of the three
limits above is two claims. Integrity (the whole closure kernel-valid, no axiom outside the three) is now
ESTABLISHED on the container tree by `lake exe comparator`: both kernels — Lean and nanoda 0.4.17, an
independent Rust implementation — accept, statements identical, nothing recompiled
(`writeup/data/arc7/k1/phaseB_integrity/`). Semantic match needs a full 8371-module recompile and is NOT
established. Same Conductor lineage, so it verifies nothing: `K2` slot 3 is re-scoped and re-run BLIND on the
laptop tree (`leg_438_prereg_amend.md`), not retired, and `K1` stays `UNVERIFIED` until slot 5. §76.

**Retired VERBATIM at this boundary (§3j), nothing edited → `## Superseded — the K2 operational block` below:** the `K2` leg-438 wave-boundary record, the pre-pre-registration board state, the built-tree cursor for K2 slots 3/5, the previous headroom note, and the stale live-worker line.

**Wave boundary — `K3` leg 439 INTEGRATED and landed.** Five workers on their own branches, ten files
cherry-picked UNEDITED into `writeup/data/arc7/k3/`; merged by `experiments/arc7_k3_merge.py` →
`writeup/data/arc7/k3/merged.json`. **VERDICT: zero of the five live gates survive as EVIDENCE.** The
blind adversary (slot 5) made ALL FIVE say `YES` from runs it knew to be wrong, each with a recipe and
numbers; two of its recipes were reproduced exactly by the Conductor. `Q1` `YES` → NOT EVIDENCE; `Q2`
UNDER-RESOURCED (not instantiated, NOT a `NO`); `Q3` NOT-INSTANTIATED → DROPPED by the rule; `Q4` 4 cells
`NO` and 3 `YES` cells NOT EVIDENCE; `Q5` `YES` → NOT EVIDENCE; `Q6` dropped before any run (§75). Four
disagreements recorded, none adjudicated, including slot 3's control that did not fire as planted — which
slot 3 reported itself, with a diagnosis. **The rule the wave was written to enforce disqualified the
gates written to satisfy it. This is a finding about the GATES, not about the manuscript; nothing here
shows any gate's claim is false.** Three pre-registration defects, ALL the Conductor's, recorded beside
and nothing edited (§79): `Q5` had no second route (its route B is a closed form in `h` and a boolean
reading no field — `abs_error` exactly `0.0`, the fingerprint); the second scale `h = 10⁻³` VIOLATES
Lemma 4.8 / (A.6) at `λ = 0.1` (`e^{−T_d} = 3.0·10⁻⁶`, confirmed by the builder's own assertion), which
also explains slot 3's control; and `Q2` cited a Prop 9.1 table that contains no `q^{2h}` term. Journal
`experiments/journal/leg_439.md`. Slot 5's completed artefact was rescued from a rate-limit-killed
worktree and committed unedited on its behalf (`a574d89`, provenance in the commit message).

**Wave boundary — `K4` leg 440 INTEGRATED: THE ARC IS CLOSED AND THE VERDICT IS PUBLISHED.**
`writeup/7_confirmation/` — `TECHNICAL_CONFIRMATION.md` (the full `K0`–`K4` record, every number cited by
JSON field), `BLOG_CONFIRMATION.md`, `CONFIRMATION_FOR_OUTSIDERS.md`, and `confirmation_evidence.py`,
which re-derives every quoted number from the banked `writeup/data/arc7/` artefacts and draws **fig115**
(registered in `build_figures.py`): **all checks PASS**, no lake, no lean, no network. The verdict is the
prereg's §2 wording verbatim and leads every document: the kernel check is **GREEN and `VERIFIED`** — one
pin, three environments, two independent kernels — and that is the WHOLE of what arc 7 confirms; the
statements are Fefferman (C)/(D), **strictly weaker** than Thm 1.1; it is NOT a confirmation that the
166-page proof is correct; and `K3` produced ZERO surviving evidence in either direction. One prereg §4
FAIL was hit and resolved the pre-committed way — **the document was corrected to the artefact** (the
`11251 jobs` completion line is cited from `gate.a_build_completes`, per §77, not from the per-target
counter). Every document carries the explicit no-position-on-priority sentence, since silence is not
compliance. `INDEX.md` has its arc-7 row; the README verdict sits **BESIDE** the arc-6 banner, which is
left standing and unrewritten.

**Headroom at this boundary (§3j, bytes):** `STATE.md` 24,156 (cap 24,576); `WALLS.md` 32,157 of 32,768; `OPTIONS.md` 20,961; this LIVE block is the tight one — the superseded blocks below still exceed three and truncation is owed at a quieter boundary.

**Open, surfaced to the user, NOT ruled by the Conductor:** the targeted 399-module semantic-match check
for `K1` (costed at ~25 CPU-min / ~8–10 min wall on the phase-B container; declaration-level via
`lean4export`, weaker than a full rebuild, and its prereg needs PASS/FAIL/INCOMPLETE pre-committed per
§3g step 1). Rulings 5–6 still await a one-word confirm; nothing in arc 7 depends on them.

**What the next Conductor must do first:** read `git ls-remote origin main`. **ARC 7 IS CLOSED —
there is no next unit in it.** Do not open a new arc without a user ruling: the arc-7 goal was set
by one (`CORRECTIONS.md` §72) and has now been met and published. Two things are OWED and neither
is the Conductor's to rule: the **targeted 399-module semantic-match check** for `K1` (above), and
**rulings 5–6**, which still await a one-word confirm. If the user schedules the semantic-match
run it is a NEW leg, with its own pre-registration pushed BEFORE it (§3g step 1) and
PASS/FAIL/INCOMPLETE pre-committed.


**Landed this arc:** `K0` (436), `K1` (437), `K2` (438), `K3` (439), `K4` (440) — **arc 7 COMPLETE**. **Audited but not landed:** none. **Live workers:** none — all five `leg/439-k3-agent{1..5}` branches pushed, verified and cherry-picked unedited; `leg/439-k3-land` carries the integration. **Open escalations:** the five rows above, unchanged and unruled.


## Superseded — the K2 operational block, retired VERBATIM from the LIVE block 2026-09-10 (leg 439, arc 7 `K3`) under §3j. Nothing edited.

**Wave boundary — `K2` leg 438 run 2 INTEGRATED and landed.** Five blind workers, one file per owner,
cherry-picked unedited into `writeup/data/arc7/k2/r2/`; the support rebuild banked at
`writeup/data/arc7/k2/tree_rebuild/` (`runner_rc=0`, 11251 jobs, 2486 oleans, `total_s` 4287). Gate
answers: (1) five `PARTIAL` statements characterised, none weakening the exported statements via the
import path — `NO`, unanimous across both runs; (2) exactly four `sorry`, all challenge placeholders,
none in either solution closure, `CONSISTENT` with `K1`'s axiom output; (3) run for real under a
**real `landrun`** built from source — the follow-on's `fake-landrun.sh` deviation is closed — check 8
`PASS`, check 9 `PASS` (all four exported theorems exactly `[propext, Classical.choice, Quot.sound]`,
no `sorryAx`, RED not triggered), checks 0 and 1 `NOT-ESTABLISHED`; (4) DeepMind byte-identity `YES`
modulo 21 enumerated wrapper hunks, one sha256 at both cited pins and at upstream `main` today;
(5) adversarial verifier `VERIFIED-SUPPORTED`, blind, re-derived `K1` from the primary logs and re-ran
it in the built tree. **`K1` moved `GREEN, UNVERIFIED` → `GREEN, VERIFIED`** on prereg §4(5)'s
condition and nothing else — two agents, three machines, one pinned commit, two Fefferman (C)/(D)
theorems on the standard three axioms; the second agent added no new machine, and no wall moves.
Slot 3 and the container follow-on agree on every quantity both measured and neither chose, so no
ESCALATION; what neither lineage has is a single run both real-sandboxed and nanoda-checked, and that
remains owed. Defects recorded beside, nothing edited: §77 (two banked job counts off by one, plus one
overstated verifier flag), §78 (three prereg wording defects — `FAIL` vs `NOT-ESTABLISHED` on check 0,
slot 1's undefined label boundaries, `forbidden_paths_opened` path-shaped against a section-shaped
constraint). The naming hazard — challenge placeholders share the exported theorems' fully-qualified
names — is recorded at `leg_438.md` §3(e): not a RED, measured, but `K1`'s answer is made correct by
the import line, not by the name. Next: `K3` leg 439, prereg and wave row pushed BEFORE dispatch.

**`K2` (leg 438) — state of the board before its pre-registration.** Four worker files ALREADY on `main`
(`writeup/data/arc7/k2/agent_{1,2,4,5}_*.json`, commits 5f77a7e b397f68 601d7da 40cbfdb) were produced by the
container Conductor's agents 08:38–09:21Z **with no pre-registration pushed, no wave row committed, and no own
branch** — the §3g step-1 defect arc 6's wave 1 recorded, repeated; slot 3 never ran (needs a built tree); slot 5's
S-d is `PENDING`; slot 2 cross-checked against leg 435, not K1. They are banked worker files, not findings
(`READING_THIS_REPO.md`); K2's prereg (`leg_438_prereg.md`) says how they are treated.

**Built-tree cursor for K2 slots 3 and 5.** Phase A's tree is in remote container 1 (not reachable from here);
the laptop's B-local tree was deleted with its session scratchpad. **Relaunched 12:53Z on the laptop:**
`scripts/arc7_k1_kernel_check.sh B <scratchpad>/nse <scratchpad>/k2_rebuild_logs` (wrapper `k2_rebuild_wrapper.sh`,
mathlib cache in `/dev/shm/k2_mlcache`, deleted after). Expected ~70 min. Artefacts to be banked under
`writeup/data/arc7/k2/tree_rebuild/` as a support run. If this session dies: check for a live `lake`, read the newest
`[n/N]` line, RESUME in the same tree; never restart clean.

**Landed this arc:** `K0` (436), `K1` (437). **Audited but not landed:** none. **Live workers (K2 run 2):** slots 1, 2, 4
spawned 13:2xZ on `leg/438-k2-agent{1,2,4}` (source-only); slots 3, 5 spawned when the rebuilt tree's `t_end=` exists, on
`leg/438-k2-agent{3,5}`. Outputs `writeup/data/arc7/k2/r2/`. A successor gates and cherry-picks whatever those branches hold. **Open escalations:** the five rows above, unchanged and unruled; rulings 5–6 awaiting a one-word confirm
(nothing in arc 7 depends on them; the Conductor does not rule them). **Composition floor:** `K3` (leg 439), a `W4`
attack — its prereg `leg_439_prereg.md` is on `main` (b091c21, 08:30Z, before any K3 run); `K1`/`K2` are audit.

**Headroom at this boundary (§3j, bytes):** `STATE.md` 23,772 (cap 24,576); **`WALLS.md` 32,157 of a 32,768 cap —
611 B spare, `test_headroom.py` PASS. The previous note ("over its 32 KB cap by 157 B") read 32 KB as 32,000; NO
retirement is owed.** `OPTIONS.md` 20,961; this live block under 8 KB; superseded blocks below exceed three
(truncation owed at a quieter boundary). Integration cycles this session: 1. Context summarised: no.
