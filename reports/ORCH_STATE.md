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
| 5 | the **leg-257 lift-clause defect** | Recorded, **not ruled**, and still **EXEMPLAR-FREE**. Distinct from row 4. | **Is the leg-257 lift clause defective as recorded — Y or N?** |

### Two DECISIONS owed that are not escalations

| # | where | the question |
|---|---|---|
| A | `writeup/CORRECTIONS.md` **§49**, and now **§54** | Does `ORCHESTRATION.md` §6 clause 3 get a `recompute-from-primary` check beside it? **§54 REVERSES the evidence I originally recorded here:** `L-JVER`'s suite is 12/12 `recompute-from-primary` **because it re-runs everything and overwrites its own artefact**, which means it did not attempt clause 3 at all. `PB2`'s suite is the mirror image (0/31, clause-3 compliant). **No suite in the record satisfies both rules, and no instrument checks which one a suite is.** |
| B | `PB1`'s finding **F2** | `experiments/JOURNAL.md:5305` and `ORCHESTRATION.md` §3k:576 give **contradictory accounts of leg 387's arXiv harness**. Leg 411 re-measured 10,780 against a recorded 10,756, favouring the journal — which puts **leg 382's queue on the wrong reading.** |

---

## LIVE — §3g CONDUCTOR, wave sizing 5. **ARC 7 — INDEPENDENT CONFIRMATION, OPEN 2026-09-10, legs 436–440.** `K0` LANDED (leg 436); **`K1` IN FLIGHT (leg 437, the kernel check, no time cap).**

**Goal (user ruling 2026-09-10):** independently CONFIRM the OpenAI Navier–Stokes result by running the Lean
kernel to completion on its two exported theorems. Rulings 1–6 recorded: `CORRECTIONS.md` §72, `STATE.md`
arc-7 block, `ORCHESTRATION.md` §3g. **Legs renumbered 436–440** (leg 435 was already spent; §72).

**The wave plan, gates pre-committed in `STATE.md`'s arc-7 table (leg 436, committed before dispatch):**
`K1` leg 437 SERIAL → `K2` leg 438 FAN-OUT ×5 (Lean gaps; slot 5 blind adversary) → `K3` leg 439 FAN-OUT ×5
(wave-4 redux on the two-route rule; slot 5 blind adversary; **composition floor met here**, `W4` attack) →
`K4` leg 440 SERIAL (`writeup/7_confirmation/`, verdict-first, one outsider document).

**`K1` cursor — the next Conductor reads THIS before anything else.** Runner `scripts/arc7_k1_kernel_check.sh`,
prereg `experiments/journal/leg_437_prereg.md` (pushed before the run). Two phases, same commit `8937a8f4`,
same container (4 × Xeon 2.80 GHz, 15 GB, disk holds ONE tree):
- **Phase A DONE 09:05Z, GREEN** (`writeup/data/arc7/k1/phaseA/phaseA.json`, commit 5f4efcb): all 11251 jobs, rc 0, both theorems on the standard three. **Phase B RELOCATED to a fresh container by user ruling (`leg_437_prereg_amend.md`, §73): A's tree is KEPT for K2 slots 3/5; a new remote session (`session_01VEipCs6B23bjiQ8aku2Pvn`, created 11:10Z from branch `claude/arc6-navier-stokes-verify-n76kpt`) runs `scripts/arc7_k1_kernel_check.sh B` from nothing and pushes `writeup/data/arc7/k1/phaseB/` on `leg/437-k1-phaseB` — never to `main`. The Conductor integrates after reading its log; RED stops everything.**
- Phase A's tree/log paths retired VERBATIM 2026-09-10 (leg 437 amend) under §3j → this file, `## Superseded — K1 phase A paths`.
- **Phase B** (now in the fresh container, not here — A's tree is not deleted) fresh-clones at the pin, `lake exe cache get`, `lake build` from
  nothing, timed end to end, then `#print axioms`. Logs `k1/k1_B_*`.
- If the session dies mid-flight: the successor checks for a live `lake` process, reads the newest
  `k1_*_build.log` `[n/N]` line, and RESUMES with `lake build` in the same tree — never restarts from a clean
  tree to "be safe", and never kills a running build on a wall-clock guess.
- Readings are pre-committed (prereg §2): GREEN → stop and report; RED (`sorryAx` or any non-standard axiom)
  → STOP, ESCALATE, NO PUBLICATION, blind reproduction first; INCOMPLETE → `NOT-ESTABLISHED` with the blocker.

**Landed this arc:** `K0` (leg 436). **Audited but not landed:** none. **Live workers:** none (K1 is
Conductor-run, serial). **Open escalations:** the five rows above, unchanged and unruled; rulings 5–6 awaiting a
one-word confirm. **Composition floor:** `K3` (leg 439), a `W4` attack; `K1`/`K2` are audit and are not
counted toward it.

**Headroom at this boundary (§3j, bytes):** `STATE.md` 23,710 (cap 24,576); `WALLS.md` 32,157
(**over its 32 KB cap by 157 B — retirement owed, not compaction**); `OPTIONS.md` 20,961; this file's live block
under 8 KB; superseded blocks below are more than three (truncation owed at a quieter boundary, accumulating
sections carried verbatim). Integration cycles this session: 1. Context summarised: no.

**What the next Conductor must do first:** read `K1`'s cursor above, find the newest `k1_*_summary.txt`, and
either bank a finished phase (`writeup/data/arc7/k1/`) or resume the build.

---

## Superseded LIVE block — arc 6 second pass, demoted 2026-09-10 (leg 436, arc 7 `K0`) under §3j. **Verbatim. Nothing edited.**

## ~~LIVE~~ — §3g CONDUCTOR. **ARC 6 SECOND PASS CLOSED AND LANDED (legs 423–435, 2026-09-10). `R7` LANDED: `writeup/6_reproduction/`. NO SUCCESSOR SCHEDULED.**

**Mode paragraph** retired VERBATIM 2026-09-10 (leg 435) under §3j → this file, `## Superseded — mode paragraph`.

**Gates answered so far** — retired VERBATIM 2026-09-10 (leg 433) under §3j → this file, `## Superseded — gates-answered paragraph`; the live table is `STATE.md`'s arc-6 block.

**WAVE 1 dispatch table** (five `R2` shards, all landed, leg 428) retired VERBATIM 2026-09-10 (leg 431) under §3j → this file, `## Superseded — wave 1 dispatch table`.

Every shard was **forbidden to open the solo ledger, `dag.json`, `leg_425.md`, `leg_426*.md` or
`CORRECTIONS.md`**, told that *"I could not determine X, because Y"* is acceptable and inventing X is
not, and required to name its hard pages. **All five also ledger the four preamble statements**, so
the five-way agreement on Theorem 1.1 / Theorem 3.1 / Definitions 3.2–3.3 is a direct measurement
of reader variance for gate (d).

**Wave 1 integrated (leg 428, `leg_428.md`).** All five shards returned complete (no `stopped_at_page`),
76 entries + 4 preamble each; merged → `ledger/merged.json` under a named primary rule; reconciled
against the solo ledger: mean citation Jaccard 0.744 (statements) / 0.791 (labels); **every
disagreement is citation breadth or a page boundary — none is about what a statement asserts, none
is a paper finding.** 29 could-not-determine records: 15 extraction artefacts (fraction layout lost
in R1's text; (4.13) and p. 137 adjudicated at the PDF's geometry), 12 out-of-shard, 1 read gap, 1
remark on the paper (Proposition 7.2's exponents only asserted to exist → `R4`). Solo `ledger.json`
**not edited**. Audit load measured: not the bottleneck this wave. Worktrees removed after cherry-pick.

**Composition floor (§3g):** the wave's five slots are audit; the floor is met by the Conductor's
serial units in the same wave — `R3` (landed) and **`R5`(i)–(ii)**, the leading-order vortex and its
residual stress, which is the `W4` attack and is SERIAL by charter. **Two defects of this wave,
recorded:** the dispatch preceded the `STATE.md` wave row (§3g step 1 says commit the plan first);
and the audit load of five shard merges lands on one context — if it becomes the bottleneck, that
is measured here, not hidden.

**WAVE 2 — dispatched 2026-09-09 after wave 1 landed on `main` (`1b54840`), five agents, each in its
own worktree, each writing ONE file under `writeup/data/arc6/spine/` and committing on its branch:**

| slot | nodes | writes | status |
|---|---|---|---|
| 1 | §10, §3, summation, §5: Thm 1.1, Lemmas 10.2–10.5, Prop 10.1, Thm 3.1, Prop 9.9, Lemmas 9.7, 9.8, 5.4, Props 5.5, 5.3, Lemmas 5.1, 5.2 (15) | `agent_1.json` | **landed** |
| 2 | §9, §8: Def 9.4, Props 9.6, 9.5, 9.3, 9.1, Lemma 9.2, Lemmas 8.2, 8.6, 8.7, 8.8, Prop 8.4, Cor 8.5 (12) | `agent_2.json` | **landed** |
| 3 | §7, §6: Props 7.2, 7.5, 7.6, Lemmas 7.1, 7.4, 7.7, Cor 7.8, Lemma 6.2, Def 6.4, Lemma 6.3 (10) | `agent_3.json` | **landed** |
| 4 | §4, A, B, C: Thm 4.6, Props 4.2, 4.10, Lemmas 4.4, 4.5, 4.8, Def 3.2, Props C.3, C.2, Lemma C.1, Props A.4, A.7, A.10, Lemma A.8, Props B.2, B.3, B.5, B.8, Lemmas B.4, B.7, Cor B.10 (21) | `agent_4.json` | **landed** |
| 5 | **ADVERSARIAL VERIFIER**, blind, seed 428: Lemma 4.4, Prop 4.10, Lemma 6.3, Lemma 8.8, Prop 9.1, Lemma 9.8, Prop 9.9, Lemma B.7, Prop B.8, Prop C.3 (10; 2/2/1/5 across slots 1–4) | `agent_5_verifier.json` | **landed** |

Every agent: verdict `CHECKED` / `GAP` (step quoted) / `NOT-CHECKED` per node, constants recomputed
not read, garbled displays checked at the PDF's geometry, forbidden from the journals,
`CORRECTIONS.md`, `dag.json` and each other's files; **escalation candidates go in the file, never
as a refutation**. Gate pre-committed in `leg_426.md` §5: ≥ 35 of 58 `CHECKED`, ≥ 3 `GAP`, verifier
agreement ≥ 0.8; `VERIFIED` only where the verifier reproduced a node blind. Composition floor:
the Conductor's serial **`R5`(i)** runs in this wave (pre-registration `leg_430_prereg.md` first).

**Wave 2 integrated (leg 429, `leg_429.md`).** 58/58 `CHECKED`, 0 `GAP`, 0 `NOT-CHECKED`; verifier
10/10 blind, agreement 1.0; **10 `VERIFIED`**, 48 `UNVERIFIED`; 301 recomputations, 480 steps, 53
extraction artefacts; no escalation candidates. The pre-committed "≥ 3 GAPs" was **refuted** (the
(B.40)/p. 40 chains agree; Prop 9.6's smallest margin is 0.07; the uncited existence step is implicit
dependence, found blind twice). Eight `CHECKED` verdicts carry a stated limit (listed in the journal,
not re-labelled). Defect: agent 4's worktree lacked the data files and read the main checkout.
**Not a proof of the theorem.** Worktrees removed after cherry-pick.

**`R5`(i) IN FLIGHT (serial, leg 430, prereg `e01a64d`).** First numbers, before the full run: G1, G2, G4
(paper's normalisation), G6, G8 pass at `λ = 0.1`; **G3 and G7 fail there, and the failure is the
finding**: the paper's closure bracket needs `120 λ log(1/λ) ≪ 1` (`λ ≲ 10⁻⁴`) and its intermediate
cone needs `√λ P_* ≪ 1` with `P_* > e^{T_d} ≈ 3·10⁵` (`λ ≲ 10⁻¹²`); a λ-sweep and a `P_*` exploration
are running, labelled post hoc. G5's pre-registered measure is a 10⁸-fold cancellation; the identity
holds in Lemma A.8's form to 10⁻¹⁵.

**`R5`(i) LANDED (leg 430, §69): `NO-AND-HERE-IS-WHERE`** — G1/G2/G8/G4(paper's scale)/G6 slopes `YES`;
G3 and G7 `NO` at every pre-registered `λ`; the post-hoc sweep finds the paper's bracket root only at
`λ ≤ 3·10⁻⁴` and the intermediate cone governed by `√λ P_*`; C5/C6 did not fire, C2 not run. Tier 2.

**WAVE 3 — CLOSED AND INTEGRATED (leg 431).** Five Lean agents, one file each, cherry-picked unedited
(`writeup/data/arc6/lean/agent_*.json` → `merged.json`): (a) build `NOT-ESTABLISHED` (theorem never reached);
(b) top-level statement strictly `WEAKER` than Theorem 1.1; (c) 4 `sorry` all challenge placeholders, 0 `axiom`;
(d) comparator 7 PASS / 4 `NOT-ESTABLISHED`, never run; (e) 74/5/0 of 79. **No kernel check anywhere.**
The Conductor is continuing the build in the background (`scratchpad/lean_chain_leg431.log`, at ~9000/9400
jobs when this was written); if it reaches the theorem, `#print axioms` is a dated addendum to `leg_431.md`,
Conductor-run, `UNVERIFIED` — it changes (a) only. Stale README banner struck and recorded (user item 4).

**`R5`(ii) LANDED (leg 432, §70): `YES` H0–H7** — two routes to the tail stress agree to 10⁻⁹; (A.48)–(A.50)'s
`δ`-powers are the limit on a collar `δ ≲ 10⁻⁶⁹` (`NOT TESTABLE`), measured `δ⁰, δ³, δ³` as Lemma A.9 predicts;
six controls fired; the prereg was amended on a derivation before any number. Tier 2.

**WAVE 4 — CLOSED (leg 433, §71): 11 of 12 signals `NOT EVIDENCE` by the pre-committed adversary rule; V2 `EVIDENCE`.**
**`R7` LANDED (leg 434):** quartet in `writeup/6_reproduction/` (TECHNICAL, BLOG, `reproduction_evidence.py`, fig113/114),
INDEX and README rows, STATE block retired verbatim under §3j, verdict paragraph in all three. **The Lean build the Conductor
continued reached the theorem after `R7` landed (leg 435): both exported theorems accepted by the kernel with
`[propext, Classical.choice, Quot.sound]` — `R6`(a) `ESTABLISHED-HERE`, (b)–(e) unchanged; addendum `leg_431.md` §7.** No successor scheduled; the five open
escalations above are unchanged and unruled. **No wall moved. No `L1→L4` link moved. Clay ~0.05%.**

**Open escalations:** the five rows above, unchanged; row 1 still carries `U1`'s measured fact and
is still not ruled. **Lean source build** from leg 418 (`lean_build.log`): not re-checked this wave;
`R6` owns it. **No wall moved. No `L1→L4` link moved. Clay ~0.05%.**

## Superseded LIVE block — §3f SOLO, arc 6 first pass; demoted 2026-09-09 at wave 1 of the conductor pass (§3j). **Verbatim. Nothing edited.**

_Was:_ LIVE — §3f SOLO. **ARC 6 RAN AND LANDED 2026-09-09, legs 417–422. NO SUCCESSOR SCHEDULED.**

**Mode:** `ORCHESTRATION.md` **§3f SOLO** — one instance, one task at a time. **No subagents were
spawned; the Task/Agent tool was not used.** The four-slot contract, the DM, the orchestrator and
the paired verifiers stayed suspended. §3f's three replacement rules were the whole defence:

1. **VERIFICATION IS A FRESH SESSION.** **Every one of the six gates is `UNVERIFIED` and says so in
   its own gate answer.** Nothing arc 6 produced is recorded as verified.
2. **PRE-COMMIT THE NEXT UNIT.** Each journal closes with §"PRE-COMMITMENT OF THE NEXT UNIT". The
   arc-6 order was never re-ranked, so no re-ranking commit was owed and none was made.
3. **NO MORE THAN TWO CONSECUTIVE AUDIT UNITS.** `U1`/`U2` were the two; **`U3`, `U4`, `U5` are
   construction units** and each shipped a module or a runner, a test battery with planted controls
   firing both ways, and an artefact.

**Six gates, answered in their pre-committed wording. `UNVERIFIED`, all of them.**

| unit | leg | gate answer | §CORRECTIONS |
|---|---|---|---|
| `U1` ACQUIRE | 417 | **`DIFFERS-AS-FOLLOWS`** — 8 agreements, 7 differences; **`(D)` is CLAIMED** | §61 |
| `U2` LEAN | 418 | (a) **`NOT-ESTABLISHED`** on a denied host · (b) **it IS (C)+(D), byte-identical to DeepMind's** and **strictly weaker than Thm 1.1** · (c) **source YES / kernel NOT ESTABLISHED** · (d) **theorem fully, argument not measurably** | §62 |
| `U3` SKELETON | 419 | **`PARTLY`** — the forcing buys the escape; compact support costs **78.9%** | §63 |
| `U4` INSTANTIATE | 420 | **`YES` on the measurement, conjunction UNMET** — my own prereg's formula was wrong | §64 |
| `U5` **DOES W4 MOVE?** | 421 | **`NO`. `W4` STANDS.** (a3) fails twice; the second is a **logarithm** | §65 |
| `U6` LAND | 422 | this block, the quartet, the retirements | — |

**THE ARC'S OWN DEFECTS, BANKED RATHER THAN SMOOTHED.** `U4`'s pre-registration omitted the
axial-diffusion term and **its own planted control caught it**; the conjunction is reported UNMET
and **not re-scored** against the corrected formula. `U5`'s control `K1` **failed** its
pre-committed tolerance (`0.060` vs `0.05`) and is reported as failed, with the diagnosis beside it
rather than instead of it. `U2`'s first `sorry` count was **4** and its own evidence script returned
**5**; the larger number is banked with the split. `U5`'s `M6` stencil is **`UNDER-RESOURCED`**
(spread `0.857` vs `0.025`) and **the conclusion is not drawn from it**.

**WHAT ARC 6 DID NOT DO, said plainly.** It did **not** read manuscript §§4–9 or Appendices A–C.
It did **not** compile the Lean — the mathlib olean cache host is **egress-denied (502 to CONNECT)**,
reported and not routed around; the source build was started and left running. It did **not** rule
any escalation, and **it raised none** — the charter reserves one for a `W4` `YES` and the answer
was `NO`. It did **not** touch statement (D) as a target: that is Lane T's, deferred by a user
ruling.

**⚠ ESCALATION ROW 1 HAS A NEW MEASURED FACT AND IS STILL NOT RULED.** `U1` found the manuscript
**claims (D)** (Corollary 10.6, every `ν > 0`). `TECHNICAL_OUTPACED.md` §5's A6-D premise —
*"(D) is the nearest **unclaimed** Fefferman statement"* — is **false on the manuscript's own
text**. **That is a measurement added to the packet, not a ruling on it.** §3h rule 1 stands: a ban
or criterion is superseded by a measurement, never by a decision — and an entity that both raises
and rules an escalation has defeated the mechanism.

**HEADROOM at this landing (§3j).** `STATE.md` 23,548 / 24,576 · `WALLS.md` 32,157 / 32,768 ·
`OPTIONS.md` 20,961 / 24,576 · this LIVE block / 8,192. **Four blocks were RETIRED VERBATIM** to
make room, not compacted: `STATE.md`'s `⚠2026-08-18` `W4` block, `WAVE 9`, `WAVE 7`, `WAVE 6`
(→ `WALLS_HISTORY.md` §STATE-W4-2026-08-18, §STATE-WAVE9, §STATE-WAVE7-EFE, §STATE-WAVE6-V5), and
two `WALLS.md` `W4` paragraphs (→ §W4-L6-LADDER, §W4-JDIV). **Context has not been summarised.**

**THE DOCUMENTATION CONTRACT (§6), and the one item that is N/A.** ① runners:
`experiments/arc6_instantiate_v1.py`, `experiments/arc6_w4_port_v1.py`, and the module
`solver/arc6_residual_ledger.py` (`capabilities.py` row 58, `test_arc6_residual_ledger.py`).
② five curated JSONs in `writeup/data/`. ③ `writeup/6_adjudicated/` — `BLOG_ADJUDICATED.md`,
`TECHNICAL_ADJUDICATED.md`, and `adjudicated_evidence.py`, which **runs all five per-unit evidence
scripts** and cross-checks every prose number. ④ **`fig112`, registered in `build_figures.py` and
carrying executable assertions** — arc 5 recorded a deliberate figure gap; **arc 6 does not have
one.** ⑤ `U1`'s artefact has no runner, and that is **stated rather than skipped**: it fetches and
hashes, it computes nothing.

**NEXT.** Nothing is scheduled and nothing is in flight. The board's live items are the **five open
escalations above**, unchanged in number, with row 1 now carrying a measured fact. **The Lean
source build was left running and its final state is not known here** — a future session should
re-check it and, if it contradicts `arc6_lean_v1.json`'s gate (a), record that as a
`CORRECTIONS.md` entry rather than editing the gate.

## Superseded LIVE block — CONDUCTOR mode, run stopped 2026-08-19; demoted 2026-09-09 at arc 6's landing (§3j). **Verbatim. Nothing edited.**

**This run is over.** The wind-down directive (`writeup/prompts/WINDDOWN_2026-08-19.md`) arrived
mid-wave and forbade dispatching anything new, forbade `TaskStop`, and suspended §9e's successor
trigger. **No successor was scheduled and none is running.** Wave 9 had already been dispatched
~20 minutes before the directive reached me, so it is recorded as **DISPATCHED**, not as
`PLANNED, NOT DISPATCHED` — recording it the other way would be false. Everything in flight was
allowed to finish.

**To restart: paste `CONTINUATION_PROMPT.md`.** It is the CONDUCTOR restart document (14,836 B).
The four-slot contract it replaced is at `writeup/prompts/CONTINUATION_PROMPT_FOURSLOT_2026-08-12.md`.

### Wave 9 — all four units accounted for

| unit | leg | state | where it stopped |
|---|---|---|---|
| `L5-cmod` | 413 | **RETURNED, INTEGRATED** `§58`, **RE-INTEGRATED `§59`** | Sealed raw verdict `95f0bc6`, adjudicated `5077a0b`. Branch `main` (agent worktree).  **Journal §7–§12 landed AFTER the close-out, at `41b0ace`: its own check `E5` FAILED (`n_s` `6→12` ⇒ increment `×1.855293`) and `X4` did not fire as planted; §58's `CONTROLLED` and its 7-digit `relative_change` are WITHDRAWN in `§59`. Fix `~0.2 core-h`, gated, parked `OPTIONS.md` §G `P0-NS12`, NOT dispatched.** |
| `P4-DRAFT` | 414 | **RETURNED, INTEGRATED** `§57` | Landed `7ce5bd0` + `33866c9`. Branch `main`. |
| `P2-DRAFT` | 415 | **RETURNED, INTEGRATED** `§55` | Landed leg-415 commits. Branch `main`. |
| `V-W8` | 416 | **RETURNED, INTEGRATED** `§56` | Landed `6f0a52a`. Branch `main`. |

### Nothing is in flight. The last unit LANDED AFTER the stop.

**`E-FE` (leg 408, the 160-attempt field ensemble) — LANDED `1f27071`, `UNVERIFIED`.** It was still
running when this block was first written; it was never stopped (the directive forbade `TaskStop`
and I did not issue one), it finished on its own, and it was gated and integrated exactly as if the
run were continuing. **`ANY_ROW_RECOVERS_IN_ANY_DRAW = NO`** — 160/160 attempts, 7 converged, **0**
recovered any named row; pooled Clopper–Pearson two-sided 95% upper `0.02279174945547`.
- **The gate was NOT moved.** `MATCH_S_TOL` stayed `0.05`, asserted against `U3`'s value at import;
  widening it to `0.10` is in the PRE-REGISTRATION as a temptation recorded and refused.
- **Verified by me at primary:** counts re-summed from the 16 cells, both Clopper–Pearson bounds
  re-derived two independent ways to 14 digits, `self_hash` `dd42c307aa63ae3b` recomputed as a fixed
  point, and pre-registration `fbada1b` shown to contain no results and to precede attempt 1 by 11 s.
- **Three Conductor findings the unit's own summary does not support** — an UNBANKED `19/19, 14/14,
  17/17`; `fired_as_planted` present on only 17 of 20 controls; a metric-dependent `closest_approach`.
  `CORRECTIONS.md` §60, items 3–5.
- **It closes only the field-draw half of `E-iv`.** The realization gap, `N = 24`, and `R-bank`'s C2
  and C4 all SURVIVE. 99.99 core-h against 91 briefed. Tier 2. No `L1→L4` link moved.
- **UNVERIFIED.** It verified nothing of its own beyond the `self_hash` fixed point; a verifier was
  budgeted separately and the run is stopped. Cite it as UNVERIFIED or not at all.

### What landed this session, and the honest summary of it

Eight `CORRECTIONS.md` sections, `§53`–`§60`. **`§59` and `§60` landed AFTER the close-out** — `§59` withdraws part of `§58` on `L5-cmod`'s own failed check, `§60` integrates `E-FE`'s `NO`. **Four of the six are corrections to the Conductor's own
record**, and the two that are not are corrections to drafts. Specifically:

- `§54` — `L-JVER`'s "evidence script" re-runs and OVERWRITES the artefact it checks. Reverses `§49`.
- `§55` — `P2-DRAFT`'s `F1`/`F3`, verified at primary. The per-term decomposition is at the **wrong
  norm** (`L³`, not the gate's `‖curl F‖_{L¹ₜL^{3/2}}`), and `rho_exponent` is banked against the
  **wrong fit window** in three fields. **The naive repair of `F3` would have BROKEN `W4` clause (b)
  off a transient.**
- `§56` — `V-W8` lands four defects on me. **`§53`'s `×130` is WITHDRAWN as arithmetic** (per-decade
  rate divided by per-rung total); repaired figure `×18`, bracket `×5.4`–`×155`. Its conclusion
  survives. `§50` item 6's remedy had landed in one file of two; fixed in `WALLS.md`.
- `§57` — `P4-DRAFT`. **`§45`'s headline `32 of 49` is UNBANKED** — no artefact, no classifier
  anywhere in `writeup/data/`. An **`UNDER-RESOURCED` measurement was banked as a passed control**,
  with its refutation **four lines away in the same JSON object**, unread for eleven legs.
- `§58` — `L5-cmod`. **The literal pre-committed rule returned `UNDER-RESOURCED` and the board
  carries that.** `§53`'s flag is discharged **only** in the part directly measured (5 more decades
  move `c_mod` by `3.19e-06` relative). The saturation claim rests on a **post-hoc discriminant**
  with a pre-planted control, and is recorded at that status, not as a `NO`.

**No `L1 → L4` link moved. No wall moved in either direction. No `NO` was reopened. `W4` clause (c)
— the torus, statement (D) — remains UNTESTED, NOT CLOSED, and is the only surviving clause of W4.**

### Wave 10 — PLANNED, NOT DISPATCHED

Not written. The directive asked for a wave-9 plan; wave 9 was already dispatched, so the honest
equivalent is the successor's first wave, and **the six parked follow-ons in `OPTIONS.md §G` are it**
— each with a price and a re-open condition, **none in a brief**. `P4-F3` (an instrument that reads
a verdict field against its own object's sibling fields, ~2–3 h, **none exists**) is the
highest-value item and should open any new wave, alongside a construction unit — §3f rule 3 still
binds, and §57 recorded that three consecutive units were audits before `L5-cmod` broke the run.

### The state of the board in one line

**Lane V rank 1 by default, not by strength; Lane L DEMOTED 2026-08-19; Lane T rank 3, DEFERRED and
blocked on a USER RULING, not on work; Lane R continuous and never sets direction.** The cheapest
unit that could move an `L1 → L4` link: **NO SUCH UNIT IS KNOWN.** Clay **~0.05%**, unmoved.

### Headroom at the stop (§3j, bytes)

`STATE.md` 22,949 / 24,576 · `WALLS.md` 32,162 / 32,768 · `OPTIONS.md` 24,527 / 24,576 ·
this LIVE block / 8,192 · `STATE.md` longest row 502 / 600 chars. `test_headroom.py`: **PASS**.
⚠ `test_headroom.py:46` has a **known false-negative path** (unanchored `## LIVE` match, `§56` item
7); today's reading is **TRUE** and independently re-measured. Remedy parked as `V8-HR`, and it is
**NOT** `V-W8`'s proposed `count == 1`, which §3j's own preference for verbatim retirement would
break.

## Superseded LIVE block — wave 8 IN FLIGHT, demoted 2026-08-19 at wave 9's dispatch (§3j)

**Verbatim. Nothing edited.** Superseded by the wave-9 LIVE block above; wave 8 is
CLOSED AND INTEGRATED (`233a2c3`, `024a9b2`, `c63769b`).

## LIVE — CONDUCTOR mode, **WAVE 7 CLOSED (`L6-b` LANDED); WAVE 8 IN FLIGHT (4 units)**, 2026-08-19

**Wave 5 and wave 6: COMPLETE, VERIFIED, and RETIRED VERBATIM BELOW.** Neither `V-W5` nor `V5`
moved an `L1→L4` link; wave 6's §3i re-rank is DISCHARGED (`L6-b` landed `4df0ca0`). Full text →
`## Superseded — wave 5's close, the trigger, and wave 6's §3i` and `## Superseded — wave 6's close`.

### ⚠ 2026-08-19 USER RULING — **TEMPORARY PIVOT TO PAPERS**, entering at the NEXT wave boundary

**Wave 7 is NOT interrupted** — the ruling says so. Scaffold `7851899` (`writeup/papers/`: three
`STATUS.md`, no drafts), merged to `main` at `7608027`. **Wave 8 planned and committed BEFORE
dispatch: `writeup/waves/WAVE8_PLAN.md`** — `L8` (Clay-chain floor, opens) ‖ `PB2` (both jaws of
`P2`'s pincer at PRIMARY — **W4(b) is recorded SHUT AND VERIFIED on two theorems never opened
here**; a jaw that does not close as cited goes to the user IMMEDIATELY) ‖ `PB1` (`P1`'s owed
novelty check; a YES kills `P1` and is a GOOD result) ‖ `V-W7` (last). **A PAPER IS A VIEW OF THE
RECORD, NEVER A SOURCE; no unit may cite a draft; the composition floor STANDS.** `P4`'s draft
slips to wave 9 on the 2–4 cap — **flagged to the user, not silently dropped** (`WAVE8_PLAN.md` §5).

### WAVE 7 — `R-bank`, `R-prof`, `V-W6`, **`L6-b` LANDED**; `E-FE` alone in flight (legs 404–408)
**`L6-b` LANDED 2026-08-19 08:06 (`4df0ca0`, leg 406). GATE `NO`: `ρ = 1.5048519` at 20,000
iterations, −6.75%, threshold `<1.45` NOT met; 43.3 core-h; evidence 57/57.** Terminal
`‖x‖‖∇J‖₂/|J|` = 44.6/12.0/5.2 — **not stationary**, so §41 bites and the plan's `NO` sentence is
**SUPERSEDED**. Licenses ONLY: *budget alone does not reach 1.45; `L7`/`L4` prices stay OPEN; the
ansatz is neither exonerated nor convicted.* Withdraws `WALLS.md`'s seed-spread magnitude as a
cap artefact (§46). **No `L1→L4` link moved. §3i seven answered in `WAVE7_CLOSE.md`; RE-RANK:
NONE** — `L-JVER` → `L6-e` → `L8` stands, because `L-JVER` is the cheapest unit that can kill the
lane and every route-4 residual is downstream of the one function it re-implements.


Plan committed `2a5ea0d` **before** dispatch, gates verbatim in the briefs. Dispatch block
retired verbatim → `## Superseded — wave 7's dispatch block`; **its `E-FE` HOLD is DISCHARGED.**

**RETURNED — `R-prof`** (leg 405, `1f89ceb`): gate (iii) **NO, 4.34×** the named reference; breaks
no wall. Detail retired verbatim → `## Superseded — R-prof's return detail`.

**RETURNED — `V-W6`** (leg 407, `c7f242c`): `V5`/`V-W5` **VERIFIED**, `L6`
**VERIFIED-WITH-QUALIFICATION**, 11 defects open, 0 repaired; my own landing audit came back
three numbers overstated and **two understated** (§38). Detail → `## Superseded — V-W6's return`.

**⚠ THE §3i q5 RE-RANK MADE IN THAT COMMIT IS NOW DISCHARGED** — `L-JVER` was dispatched and is
in flight (leg 409). `L8`'s branch rule stays **DEFERRED VERBATIM to wave 9**, still keyed to
`L6-b`. Full text → `## Superseded — wave 7's §3i q5 re-rank`.

**RETURNED — `R-bank`** (leg 404, `8019c35`): **`YES` ×3**, 160/160 bit-identical, seedbank now
TRACKED. My independent re-hash and 4-field regeneration agreed bitwise. Detail retired verbatim
→ `## Superseded — R-bank's return detail`; the archive-size correction is `CORRECTIONS.md` §39.

**DISPATCHED — `E-FE`** (leg 408). **6 shards not 8**, on a measurement: **~15.2 h wall not ~11.4;
~91 core-h unchanged.** Inherits C2/C4; draw order a **declared choice** (lesson 91).

### WAVE 8 — IN FLIGHT (legs 409–412); **`PB2` LANDED `a7ffa1e`**, plan `5802a49`/`6ca49a6`

**RETURNED — `PB2`** (leg 410, `a7ffa1e`): gate **`YES`**. `W4` clause (b) is carried by **TSAI
1998 THM 2** (no `L^q` in the hypothesis), verified by me at FULL TEXT; **NRŠ does not apply** and
the one `UNREACHABLE` source is **not load-bearing** for it. Clause (b) STANDS. Three Conductor
findings at landing: **`WALLS.md` was 2,151 B OVER §3j and the gate did not check** (§48, remedied
by `test_headroom.py`, now always-on); the evidence suite is **0/31 recompute-from-primary and §6
clause 3 REQUIRES that** (§49); the citation defect is in **five** places, the fifth being the
generator (§47b). §3i seven + full audit: `writeup/waves/WAVE8_CLOSE.md`. **RE-RANK: NONE.**

`L-JVER` (409, Lane L construction, opens the wave, meets the composition floor: independently
re-implements `W[V]` and `J(c)` in a different basis; gate is `|ΔJ|/J_L6 < 1e-3` at three points,
`YES`/`NO`) ‖ `PB2` (410, Lane L literature, re-scoped by AMENDMENT 4 to the NRŠ/`q = 3` seam) ‖
`PB1` (411, paper blocker, `P1`'s owed novelty check under full leg-392 instrument discipline — a
`YES` KILLS `P1` and is a GOOD RESULT) ‖ `V-W7` (412, verifier, dispatched LAST). **Four units, at
the §3g cap; one verifier per wave, dispatched in the FOLLOWING wave, as budgeted.**

**`V-W7` is briefed against my own seventeen wave-7 integration commits**, itemised — the §41
three-way-licence row I fired on `L6-b`, the §46 withdrawal that overturns something `V-W6` UPHELD,
the §46b self-correction, and the §3j figures below, which it is told to measure itself. I planned
wave 7; I may not verify it.

**`E-FE` (408) is a LATE RETURN.** Ruling `99421dd` stands: Lane R, did not set this wave's
direction, **may not influence wave 8's ranking.** It holds 6 of 12 cores until ≈03:20 on 20-Aug.

### Headroom at the wave boundary — §3j, IN BYTES (`wc -c`)

| file | bytes | cap | free |
|---|---|---|---|
| `STATE.md` | 23,434 | 24,576 | 1,142 |
| `WALLS.md` | 32,446 | 32,768 | 322 |
| `OPTIONS.md` | 23,971 | 24,576 | 605 |
| `ORCH_STATE.md` LIVE | 7,811 | 8,192 | 381 |

**⚠ NO LONGER MEASURED BY HAND** — `test_headroom.py`, always-on in `merge_gate.sh` (§48). A LIVE
block it cannot locate is a **FAIL**, not a skip. **It caught this edit going over as it was written.**

**Defect of mine, §37 `writeup/CORRECTIONS.md`: retire by slicing between ASSERTED LINE INDICES,
never by title, and measure the live block by line index too, or the cap check silently passes.**

**Retired verbatim 2026-08-19** (headings are the index; git carries the rest): ORCH's wave-5
close / trigger / wave-6 §3i; `WALLS_HISTORY.md` §OPTIONS-A2, §OPTIONS-E, §STATE-WAVE5, **§LANE-T**
— the last **before** `WALLS.md`'s next edit rather than after it bounced off the cap.

**`R-prof`'s §3k rule 3 DISCHARGED before dispatch (2026-08-19)**: reference **named, fetched and
STEPPED at `N = 24`** — JAX-CFD `ForcedNavierStokes2D` (PNAS 2021) + FFTW3 via `pyfftw` for the
transform floor. `SOURCES.md` 23–25; caveats and drift fallback in `WAVE7_PLAN.md` §C.

### Open escalations — THREE OPEN, NONE RULED BY ME

1. **NEW 2026-08-18** — `ESCALATION_W2_SCOPE_2026-08-18.md`. `V5` measured the Grade-A × fluid
   occupant **genuinely 3D on W2's own test**, but W2's statement names **3D SINGULARITY**
   theorems and `arXiv:2509.25116` is a **NONUNIQUENESS** theorem. Three defensible readings; the
   third would make Lane T's **re-open condition (i)** live. **A wall's WORDING is the user's, and
   a deferral set by ruling is not undone by a Conductor's reading.** Nothing stops.
2. `ESCALATION_PUB0C_PUBLISHED_2026-08-18.md` — `PUB_0C` §1 grades *"any PUBLISHED work"*; the
   paper carries **no journal-ref** (`V5` confirmed at v2, and correctly did **not** grade it).
3. Still on the desk: `T1`'s ban-wording packet (machine record **DISCHARGED**) and the leg-257
   lift-clause defect — **recorded, NOT ruled**. C1 is **DISCHARGED**, **EXEMPLAR-FREE**.

**The W3 wording escalation is RULED** and transcribed. **`V5` did not run W3's prose test, so W3
does not move** — the audit says nothing about whether the wall stands.

## Superseded — the §3k directive and the Lane-R ruling, demoted 2026-08-19 (verbatim; DISCHARGED)

### 2026-08-18 — THE §3k DIRECTIVE AND THE LANE-R RULING, both discharged mid-wave

**`9b9571a` — §3k(a), `writeup/SOURCES.md` BUILT**, 22 rows, shipped incomplete and saying so.
1,671 arXiv ids are mentioned across the record; **6** appear in the load-bearing files. **DEPTH is
the column that matters.** Rule-2 sweep: **no live load-bearing claim rests on an `ABSTRACT`.**
**The register CORRECTS the directive that ordered it** — Chae–Wolf `1610.09464` (leg 359, hashed),
Seregin `math/0510396` (`V-W4`) and **Tsai 1998** (leg 359, re-downloaded from the author's page,
re-hashed, diffed) are **already at primary**. Only **NRŠ 1996** is unread, and it is `SECOND HAND`
(Tsai p.30 quoting `[NRS]` (1.3) verbatim + a second restatement), **not `ABSTRACT`**. So §3k(b)'s
unit is **much smaller than priced** and is scoped to NRŠ alone (`WAVE7_PLAN.md` §2).

**`f94cde4` — E's field ensemble PRICED, NOT QUEUED. 90.9 core-hours**, re-derived from `E`'s own
outturn (2,044.90 core-s/attempt × 160), **plus a ~3.4 h serial DNS prologue** that does not
parallelise. **W7 datum: size is NOT the binding risk.** `U3` **finished** — 14.47 h wall, 144.69
core-h reserved, 92.9% utilised. Every recorded loss was a **suspended session** or a **gitignored**
checkpoint. Conditional survivability, four cheap conditions, in
`writeup/prices/FIELD_ENSEMBLE_2026-08-18.md`.

**`9811c1e` — LANE-R RANKING RULED: `R4` > `R2` > `R3`** (`WAVE7_PLAN.md` §0). Broken on **kind**:
`R4` is a **validity** fix (Lie–Trotter, first order, **measured** ratio 2.00), `R2`/`R3` are
throughput fixes, and deflating a first-order solver produces objects whose status is in doubt,
faster. **I overturned `OPTIONS.md`'s standing "`R2` is strongest"** and said so. **Self-unwinding:**
if §1's displacement lands below the acceptance band, `R4` drops below `R2` in that commit.
**Options A/B/D RETIRED, not deferred** — all three buy supply, a standing prohibition.

**WAVE 7 IS PLANNED, NOT DISPATCHED.** `L6` is still in flight; §3i is answered when a unit
**returns**. Gates are in final wording already.

## Superseded — the FIRST headroom table of the wave-6 boundary, demoted 2026-08-18 (verbatim)

**Why:** it names a `WALLS.md` `## History` exemption **that does not exist** — the file has no
such section, so the whole file counts. Kept verbatim because the `wc -c` lesson inside it is the
reason two files were committed over cap.

### Headroom at the wave boundary (§3j) — IN **BYTES**, AND THE FIRST COUNT WAS WRONG

Detail retired verbatim 2026-08-18 → `## Superseded — wave 5's headroom detail` below.
**Live consequence: measure the caps with `wc -c`, NOT Python `len()`** — these files are
dense with multi-byte UTF-8 and a character count under-reports by ~2% (~500 B at
`WALLS.md`'s size); on that error I read two files as inside their caps and committed
them **over**. `ORCHESTRATION.md` §3j now carries the rule. Rows stay in **characters**.

| file | bytes | cap | free |
|---|---|---|---|
| `STATE.md` | 23,639 | 24,576 | 937 |
| `WALLS.md` *(excl. exempt `## History`)* | 32,233 | 32,768 | 535 |
| `OPTIONS.md` | 23,971 | 24,576 | 605 |
| `ORCH_STATE.md` LIVE | 7,247 | 8,192 | 945 |

**Next retirement NAMED:** `WALLS.md` — W3's cell-occupancy narrative behind a pointer;
`OPTIONS.md` — §F's discharged items. Cycles: wave 5 = 2; context HAS summarised.

---

---

## Superseded — wave 5's close, the trigger, and wave 6's §3i, demoted 2026-08-19 (verbatim)

### Wave 5 — CLOSED, INTEGRATED and now VERIFIED; rows retired

3 planned, 3 dispatched, 3 landed (`L5`, `V-W4`, `D-REPAIR`); `V-W5` verified it 2026-08-18.
`L5` and `V-W4` rows have **left `STATE.md` under §3j** → `writeup/INDEX.md`. Narrative, the
mechanical audits and wave 5's §3i: **retired verbatim below the boundary**. Live consequences
kept: **no re-ranking** (W4 running out of clauses in Lane L does **not** re-open Lane T); `L5`'s
ceiling is **both jaws of its pincer unread at primary**, `UNDER-RESOURCED` with a cost; **q7 fired
twice**, which is why wave 6 opened with construction.

### ⚠ THE TRIGGER FIRED — `V-W5` CLEARED `L5` 2026-08-18, AND THE MESSAGE WAS SENT

Standalone, not folded into a wave summary, carrying **all three caveats**: `L5` verified as
**arithmetic only**; `c_mod = 869.288` is the **SYNTHETIC** profile's number *and* basis-dependent
by `1.476×`; **(c) is UNTESTED, NOT CLOSED.** Do not re-send it and do not restate the structural
claim without those three.

**STILL QUEUED FOR WAVE 7 (owed on the run's own output, not screening):** a `writeup/novelty/`
pass on `L5` — no novelty entry exists (dir stops at `leg_394.md`). Claim to check: Chae–Wolf's
`α`-pin **and** NRŠ/Tsai's exclusion of exactly-SS profiles **jointly** shut clause (b).

### §3i — THE DIRECTION CHECK, per unit, `V-W5` (leg 403) and `V5` (leg 402)

**`V-W5`.** (1) No link moved — a verifier cannot move one. (2) Made FALSE: that `L5` is
unverified, and that `c_mod` is portable (**`1.476×` basis-dependent**). (3) Lane L keeps priority.
(4) **Ceiling unchanged and now the sharpest thing in the file:** both jaws of `L5`'s pincer (ESŠ;
NRŠ 1996, Tsai 1998) are **journal-only, never read at primary** — verifying arithmetic does
nothing for that. (5) Cheapest killer: read them at primary; **cannot be bought here** —
`UNDER-RESOURCED` with a cost. (6) If Lane L died: `T2″`, not cheaper. (7) 2 of the last 3 units
were audit — which is what `L6` exists to break. Detail: `CORRECTIONS.md` §35.

**`V5`.** (1) **No link moved**, and the unit says so itself. (2) Made FALSE: that the Grade-A ×
fluid occupant might be **another 2D lift** — it is **genuinely 3D on W2's own test**, swirl 57% of
`max|u_r|`; and that wave 4's `D1`–`D6`/`N1` were undischarged. (3) **Lane V's rank is re-earned,
not merely retained**: the lane's premise was that the cell is occupied by something worth
auditing, and the audit found a closing certificate **with four broken constants**. (4) **YES, and
it is now named in the wall itself:** the certificate's **Class A — 22 interval-arithmetic inputs —
was NOT verified** and is banked as a **LIMIT OF THE AUDIT, never a pass**; the closure claim rests
on it. (5) Cheapest killer of Lane V: re-running the **Julia certification** end-to-end, which this
audit did not do. Not next because `L6`'s construction debt outranks it and q7 has fired twice.
(6) If Lane V died: Lane L already is the priority; nothing changes. (7) See above.

**RE-RANKING: NONE.** `V5`'s clause 2 raises a **scope** question about W2 — its statement names
**3D SINGULARITY theorems** and this is a **nonuniqueness** theorem — and one reading of that
scope would make Lane T's **re-open condition (i)** live. **THE CONDUCTOR IS NOT RULING IT:** a
wall's WORDING is the user's, a deferral set by ruling is not undone by a Conductor's reading, and
a ban or wall is superseded by a **MEASUREMENT**, never a decision. Recorded, not ruled →
`writeup/escalations/ESCALATION_W2_SCOPE_2026-08-18.md`.

**WAVE 6 STATUS: 2 of 3 returned and integrated** (`V-W5` `95cf861`, `V5` `dacc01c`). **`L6` is
still in flight** — the wave does not close until it returns or is declared under-resourced.

---

## Superseded — wave 6's dispatch record, demoted 2026-08-18 under §3j (verbatim)

### WAVE 6 — **DISPATCHED**, 2026-08-18, in the order the plan fixes (§3f rule 3)

Plan `e202653`, `STATE.md` pointer `5c49486`, both **before any worker started**. Three
self-contained briefs, each carrying **its gate verbatim from the plan**, its readings,
its territory, *pre-register in its own commit before any result-producing code*, and
**COMMIT DURING THE RUN, NOT ONLY AT THE GATE**.

| unit | lane | branch | order |
|---|---|---|---|
| `L6` — bank a discrete route-4 profile | L | `leg/401-l6-route4-profile` | **first (construction)** |
| `V5` — adversarial audit of `arXiv:2509.25116` + the `_v2` repair | V | `leg/402-v5-audit-25116` | second |
| `V-W5` — verify wave 5 | — | `leg/403-vw5-verify-wave5` | **last (verifier)** |

**POST-COMPACTION RE-READ 2026-08-18** caught a real defect: `WALLS.md` has **no `## History`
section any more**, so the exemption I had been subtracting does not exist and the file was **31 B
OVER**. Fixed by retirement (§PRIORITIES-Q6). **§34 applied to every wave-6 gate — all artefacts
named in a brief exist.** Handoff at **wave 6's END**.

**I planned this wave, so I may not verify it** — `V-W5` verifies **wave 5**. No brief
sends a worker on a repo tour; each names the files it may read. `V5` carries reading (e):
the journal-ref finding is an **open user escalation** — record it, **do not grade the
criterion, do not stop for it**. `V5` and `V-W5` may not edit any `_v1` artefact (Q3).

### WAVE 6 — PLANNED, COMMITTED BEFORE DISPATCH: `writeup/waves/WAVE6_PLAN.md` @ `e202653`

**`L6`** (Lane L, **CONSTRUCTION, FIRST**, ~10² agent-h) — **bank a discrete route-4 profile.** Route
4 has never had one; leg 381's bill and `L5`'s clause-(b) bill were both measured on a **synthetic**
stand-in, which is why `L5`'s exponent is a class fact and its constant is not route 4's.
**`V5`** (Lane V, **obligatory under ruling Q4**) — adversarial full-text audit of
`arXiv:2509.25116` at leg-309 depth, **two clauses answered separately**, the 3D clause arbitrated by
**W2's own pre-committed test**, **not** folded into the close/does-not-close verdict; it carries the
wave-4 repair as `_v2` files, `v1` untouched (Q3). **`V-W5`** (**last**) — verifies wave 5, which it
did not plan, including **whether `C6`'s tolerance was ever moved**.

**A GATE DEFECT OF MINE, FOUND WHILE PLANNING.** `L5`'s wave-5 gate named *"route 4's **banked**
discrete profile"*, which **does not exist** — the gate was **unsatisfiable as worded**, and my
integration commit `e42e7ab` called the substitution a *limitation* when it is a **gate deviation**.
`writeup/CORRECTIONS.md` §34, row 16. **No wave-6 gate names an artefact I have not checked exists.**

## Superseded — wave 5's close narrative and audit pointer, demoted 2026-08-18 under §3j (verbatim)

### Wave 5 CLOSED — 3 planned, 3 dispatched, 3 landed

`D-REPAIR` `036e56d`, **`L5` `4be46ef`**, **`V-W4` `b46ee4d`**. Gates immutable at
`writeup/waves/WAVE5_PLAN.md` @ `1e49a00`, committed before any dispatch and **unchanged after it** —
including when a ruling landed mid-wave asking for an addition to `L5`'s reading: **I refused to
amend a dispatched gate** and required it at integration instead (demoted block below).

### What I audited, mechanically, and NOT on either unit's report

**Demoted verbatim 2026-08-18 when wave 6's plan was written**, per the remedy in the headroom
report below → `## Superseded — wave 5's mechanical audits`. Nothing was shortened.

### §3i — wave 5's direction check: retired 2026-08-18 → `## Superseded — wave 5's §3i`

**Live consequences kept:** no re-ranking (W4 running out of clauses in Lane L does **not** re-open
Lane T — a decision may not supersede a measurement); `L5`'s ceiling is **both jaws of its pincer
unread at primary**, `UNDER-RESOURCED` with a cost; **q7 fired twice**, which is why wave 6 opened
with construction.

## Superseded — wave 5's §3i direction check, demoted 2026-08-18 under §3j (verbatim)

### §3i — THE DIRECTION CHECK, per unit, against the RECORD

**`L5`.** **(1)** No link moved; Tier 2, float64, **synthetic** profile. **(2)** It made **FALSE** the
record's own description of clause (b) as *"the strongest surviving item in the lane"* which
*"never asks the profile for decay at all, so the pin at `α = 1` does not bind it"* (`OPTIONS.md` §D,
now corrected): the ansatz **does** ask, through the modulation commutator's `ρ^{1-α}` scaling, and
the escape was illusory. **(3)** Lane L keeps its rank, but **not on W4** — its rank rests on leg
390's measurement that §6(i)/(ii) block every branch, and those are untouched. Its W4 content is now
**exhausted**; the one clause left is Lane T's. **(4) YES, and this is the sharpest thing in the
wave.** `L5`'s `NO` is a pincer whose **two jaws are both literature this repository has never read
at primary**: the `α = 1` pin (ESŠ, `UNREACHABLE`, journal-only, and `V-W4` found the carrying
citation names the **wrong ESŠ paper** — `D5`) and the exact-self-similar exclusion (NRŠ 1996, Tsai
1998, both pre-arXiv, both banked `UNREACHABLE`). **The clause-(b) result is exactly as strong as
four secondary readings.** **(5)** Cheapest killer: *read those four at primary*, ~1 unit — **not next
because it cannot be bought here** (all journal-only, no S2 key, author contact prohibited). That is
`UNDER-RESOURCED` **with a cost**, not a ranking. **(6)** If Lane L died tomorrow: Lane V's
obligatory audit and Lane T's `T2″`, both cheaper — but **neither touches §6(i)/(ii)**, which is why
Lane L is not dead. **(7) YES, still in the loop, flag stands.** Last six landed: reading, grading,
verification, infrastructure, **construction**, verification. Wave 6's debt 1 is **binding** now.

**`V-W4`.** **(1)** No link moved — a verification builds nothing. **(2)** It made **FALSE** four
fields presented as verbatim, the `T2c` citation, the word *"independently"*, and `326.875` as a
portable constant — and the implicit claim that the `≤ 1` direction runs through the **global** ESŠ
theorem: this object has infinite global energy, is **not** Leray–Hopf, and runs through the
**local** suitable-weak form or not at all. **(3)** Lane V's rank is the user's (un-held by ruling);
`V-W4` adds a **user escalation**, not a ranking input. **(4)** As `L5` (4) — the same undischarged
ceiling, now named precisely instead of gestured at. **(5)–(7)** as above.

**RE-RANKING: none this wave, and the reason is recorded so it is not drift.** W4 running out of
clauses in Lane L does **not** re-open Lane T — that would be a decision superseding a measurement,
backwards. Lane T's two re-open conditions are unchanged and neither fired. What changed is the
**value** of `T2″`, now the cheapest thing that could put a live W4 clause back in front of Lane L.
**Cost before ranking.**

## Superseded — wave 5's headroom detail, demoted 2026-08-18 under §3j (verbatim)

### Headroom at the wave boundary (§3j) — IN **BYTES**, AND THE FIRST COUNT WAS WRONG

**A correction the next Conductor needs:** I first measured with Python `len()` — **characters**.
These files are dense with multi-byte UTF-8, so that under-reports by ~2%, and on bytes **`WALLS.md`
and `OPTIONS.md` were both OVER cap** when I read them as inside it. `HEAD` was compliant: the defect
is **mine**. **Measure with `wc -c`.** `ORCHESTRATION.md` §3j now says so.

| file | bytes | cap | free |
|---|---|---|---|
| `STATE.md` | 23,639 | 24,576 | 937 |
| `WALLS.md` *(excl. exempt `## History`)* | 32,233 | 32,768 | 535 |
| `OPTIONS.md` | 23,971 | 24,576 | 605 |
| `ORCH_STATE.md` LIVE | 7,247 | 8,192 | 945 |

Cycles: **wave 5 = 2**. **Context HAS been summarised** — §9d's triggers are 12 cycles
*or* first summarisation, and **the second has fired**: wave 6 is planned knowing a handoff is due.

**Retired this integration**, verbatim: `E`'s H-hard narrative and the superseded lane-priority
paragraphs → `WALLS_HISTORY.md` §E, §PRIORITIES; `V3` and `L2′` rows → `writeup/INDEX.md`; wave 5's
unit table → its own committed plan file; the wave-5 in-flight narrative, the fork paragraph and this
wave's audit detail → the blocks below; **and, on finding the overrun** — `V-W4`'s `≤ 1` provenance
paragraph → §W4-PROV (1,087 B) and the refuted `~8×` cost-model block → §OPTIONS-A (753 B, struck
kept struck), both leaving live pointers. **Retirement, not compaction.**

**THE NEXT RETIREMENT IS NAMED, because 535 bytes is not headroom.** `WALLS.md`: W3's
cell-occupancy narrative retires **the moment wave 6's audit lands** (that unit supersedes it), and
Lane T's *price* bullets restate `OPTIONS.md` §E — **but Lane T got MORE load-bearing this wave, so
those move only behind a pointer that keeps every number.** `OPTIONS.md`: §F's discharged items.
`ORCH_STATE.md`: **done** — wave 5's audit detail demoted verbatim when this plan was written.
**If a wave needs more than that, the cap itself is the escalation, not the content.**

## Superseded — wave 5's mechanical audits, demoted 2026-08-18 under §3j

### What I audited, mechanically, and NOT on either unit's report

**`L5`.** Five new files, **no banked JSON touched**, journal insert-only 654/0. Pre-registration
`e2f13c1` carries the gate, the readings and the discriminator, holds **no result number**, and
precedes the first code commit by 15 min. **I re-fitted all 18 sweep cells** and reproduced every
exponent; its evidence script runs clean from a fresh worktree. **The controls are
why I believe the `NO` is about the object and not the apparatus:** the same machinery returns
`−0.2498` at `α = 1.25` and `−0.5996` at `α = 1.6`, tracking `1 − α`, and the unmodulated `SS`
control at `κ = a` returns `−2.000005` — with `ṁ = 0` the localisation error **is** summable. `C6`
did **not** fire as planted on its 5-point form (`2.03e-02` vs `1e-02`); it **says so**, **the
tolerance was not moved**, and the constant it perturbs is not what the `NO` rests on.

**`V-W4`.** Three new files, **nothing of `V3`'s or `L2′`'s edited**, no Conductor file touched.
`self_hash` `e0171ac1e855f90e` recomputed independently. **I re-ran its re-derivation from an empty
cache against primaries I fetched myself**: exit **1** with **exactly the two item-(2) discrepancies
it reports**, none manufactured, (1)(3)(4)(5) clean, `p2_route_l2_decay_v1.json` regenerating
**bit-identically**. It also **withdrew one of its own first-pass claims** mid-run.

## Superseded — the 2026-08-14 fork, retired from the live preamble 2026-08-18 under §3j

**The 2026-08-14 fork is CLOSED at `5d9c065`.** Two concurrent CONDUCTOR sessions diverged at
`2928966` and were merged: the branch supplied the C1-exemplar ruling, wave 3 and `V-W2`; `main`
supplied unit **`E` LANDED COMPLETE at `d0d72b1`**. **Any row anywhere claiming "`E` DID NOT RETURN"
is stale** — it was true when written on the branch and is false now. Do not re-dispatch a wave-2
verifier, do not re-raise the C1 escalation, do not redo `T1`'s machine record: all three are DONE.

## Superseded LIVE block — wave 5 IN FLIGHT, demoted verbatim 2026-08-18 at wave 5's close (§3j)

### Wave 5 — planned and committed before dispatch: retired from LIVE under §3j

*The plan, the gates-by-pointer mechanism and the dispatch record are verbatim in the Superseded
LIVE block below. `writeup/waves/WAVE5_PLAN.md` @ `1e49a00`; dispatch at `54183bb`.*

### Wave 5 — `D-REPAIR` RETURNED AND LANDED (`036e56d`), the other two in flight

**Audited mechanically, not on report.** Territory clean (STATE/WALLS/OPTIONS/ORCHESTRATION/reports/
and every banked JSON untouched; `p2_route_vbs_v1_scoping.json` not touched, per reading (b)). Both
`prog_r4` journals are **insert-only, 0 deletions** — corrections placed beside standing text. The
coverage check re-run by me reproduces its numbers exactly, exit 1. I **independently re-derived D5**
off `p2_prog_r4_e_v1.json`: exactly **8** attempts exceed the 2,047.44 s window, their walls sum to
**20,117.0 s = 5.5880 core-h**, all 16 sum to **32,718.3 core-s = 9.0884 core-h**, and
32,718.3/343 = **95.389 s/epoch**. The subset the record called unrecoverable is recoverable.

**SCOPE, STATED PLAINLY: this unit exceeded its literal listing once.** Registering T6's evidence
script required widening `P2_EVIDENCE`'s entry schema to `(path, args, required_inputs)` with a
counted `SKIP` for absent gitignored PDFs. **Accepted** — a naive registration would have broken the
rebuild on every clean checkout, and the alternative was `UNDER-RESOURCED` — but it is a behaviour
change to a shared runner, and reading (a) said repair only what is listed. Recorded, not hidden.

**NEW DEBT, NOT REPAIRED AND NOT MINE TO SLIP IN:** `fig81_route_egmf_v1_evidence.py` is tracked and
unregistered — **the same defect as D6 at a different figure**, one line from fixed. It is a unit,
not a favour. The 52 cited figures with a `.png` and no rebuild path (`fig8`–`fig47` is a contiguous
block of 40, and looks like a pre-convention era rather than 40 lapses) are the larger item; there is
**no room in `OPTIONS.md` to open them as options** — 15 bytes free. That is the cap question biting
a second time, in a place where it now costs the record something.

### A USER RULING LANDED MID-WAVE, from a concurrent session (`c41280e`)

**Caught by `git ls-remote` before the push, not after.** `origin/main` had moved from `54183bb` to
`c41280e` while wave 5 was in flight: the W3 wording escalation is **RULED, all three questions plus
two consequential items**, and **§3j gains RETIREMENT**. Merged at `e45ef0e`; `STATE.md`, `WALLS.md`
and `OPTIONS.md` re-read from disk after the merge, as the standing rule requires.

**The ruling is transcription work and it is now transcribed.** (Q1) prose test governs, **W3
STANDS**, Lane V's premise **survives**. (Q2) W3 **retitled**, old title struck not deleted, the
required paragraph placed beside it verbatim. (Q3) the banked field is **NOT edited** — correction
record at `writeup/CORRECTIONS.md` register row 13 and §32, and the refusal to rewrite a banked datum
is now the **standing rule**. (Q4) the `2509.25116` audit is **OBLIGATORY IN WAVE 6**, scope fixed,
with the separate **W2** clause. (Q5) confirms `L5`, already in flight and planned before the ruling
existed. **Lane V is UN-HELD** in all three capped files — the hold went in on one line and comes out
on one, which was the point of recording it that way.

**RETIREMENT APPLIED THE DAY IT ARRIVED, and it is the difference between a cap and a treadmill.**
`T4`/`T5`/`T6`/`T1`/`T2`/`R0`/`R1` left `STATE.md` for a new *Retired from `STATE.md`* table in
`writeup/INDEX.md` (unit, gate answer in the gate's own words, SHA, verifier); waves 3 and 4 became a
paragraph pointing at the Superseded LIVE blocks here; `WALLS.md` §R0/R1 moved **verbatim** to
`WALLS_HISTORY.md`; `OPTIONS.md`'s `E` and `R0`/`R1` entries retired to one line plus a pointer.
**`STATE.md` went 24,531 → 23,474 with MORE content in it than before** — the ruling, the wave-6
debt list and `D-REPAIR`'s row all landed inside a file that got smaller.

**AND ONE CORRECTION CARRIED WHILE THE FILE WAS OPEN.** `OPTIONS.md` §A still printed `V-W3`'s
*"21.44 vs 21.95 epochs/attempt"* — the cross-convention comparison `D-REPAIR` refuted. It now
carries the like-for-like numbers (**+1.9% / +1.7%, `E` used MORE**) with the convention spelled out.

### The retirement BACKLOG cleared, and one path discrepancy recorded not fixed

**Re-read from disk after the ruling — `RULING_W3_WORDING_2026-08-18.md`, `ORCHESTRATION.md` §3j,
`STATE.md`, `WALLS.md` — and the transcription checked MECHANICALLY, not by eye.** The ruling's
required paragraph is present in `WALLS.md` **byte-identical after whitespace normalisation**
(9 blockquote lines, 0 missing); the retitle is on disk; the old title is struck and not deleted;
`HELD` appears nowhere in the three capped files.

**Backlog cleared, and it was real:** `V-W2` **is** verified — `V-W3`'s item 3 is literally *verify
the verifier*, verdict **CONFIRMED**, with an independent re-fetch-and-hash of all three sources —
and `E`'s **gate answer** is verified by `V-W3`'s item 1 (16 rows recounted off
`diagnostic_3.attempts`). Both retired to `writeup/INDEX.md` with their verifier named. **`E`'s row
carries the distinction that makes it honest: the gate answer verified, the RECORD'S COST CLAIM about
it refuted.** `V1` stays — nothing has audited it; `V-W3` audits `V-W2`, not `V1`.
**`STATE.md`: 22,457 / 24,576 — 2,119 free, from 162 free two integrations ago.**

**PATH DISCREPANCY, RECORDED NOT FIXED.** The amendment names `writeup/WALLS_HISTORY.md`; the file
created at `6320790` and used by every existing pointer is `WALLS_HISTORY.md` at the repo root. I did
not rename it — a rename breaks the live `## History` pointers to buy nothing — but a later reader
should know the two names refer to one file.

### Ruling Q5's added requirement, and what I did NOT do about it

The ruling requires `L5` to state **what distinguishes a genuine natively-finite-energy ansatz from
the same trap wearing a different hat.** `L5` was dispatched before the ruling existed, and its
pre-committed reading (c) already says: *"THE MOST LIKELY OUTCOME IS THAT THE ANSATZ IS EXACTLY (D)SS
IN DISGUISE … SAY SO, STOP, AND CALL IT A `NO`."* **I did not message the worker to amend a gate
after dispatch** — that is the one thing the pre-registration discipline exists to prevent, and the
requirement is already covered in substance. **If `L5`'s return does not draw the distinction
explicitly, I require it at integration and say so there.** Recorded now, before the return, so it
cannot be a judgement made after seeing the answer.

## Superseded LIVE block — wave 5 as PLANNED AND DISPATCHED, 2026-08-18

*Demoted from LIVE 2026-08-18 under §3j. Nothing deleted, nothing reworded.*

### Wave 5 — PLANNED AND COMMITTED BEFORE DISPATCH

**`writeup/waves/WAVE5_PLAN.md` @ `1e49a00`.** Three units: **`L5`** (Lane L, CONSTRUCTION, first)
attacking **W4 clause (b)**, the natively finite-energy ansatz; **`D-REPAIR`** for `V-W3`'s D2–D6
plus the four held Conductor debts; **`V-W4`** (LAST) verifying wave 4. §3f rule 3, §3h composition
floor and §3i q7 all discharged by named units.

**A SECOND §3j MECHANISM, FLAGGED NOT SILENT.** The gates are in a committed plan file and
`STATE.md` carries the wave-5 block **by pointer to that SHA** — plan committed first, pointer
second, **both before any worker starts**. This is §3j rule 5 (*quote a gate by pointer once
committed*) applied at plan time rather than after dispatch, and it was forced by the cap: wave 4's
equivalent block was 5,598 bytes and `STATE.md` had 142. **The gates are not weaker for it — they
are in final wording and unchangeable after dispatch.** If the user prefers gates inline, that is a
cap ruling, and it is asked for above.

**DISPATCHED 2026-08-18, plan and pointer both landed first (`1e49a00`, `d842898`; `origin/main` and
local agreed at `d842898`, no concurrent push).** `L5` → `leg/400-l5-finite-energy`, `D-REPAIR` →
`repair/wave3-defects` — **construction opened the wave** — then `V-W4` → `verify/wave4` **last**.
Each brief carries its gate in the final committed wording, COMMIT DURING THE RUN, the never-relax
rules and the prohibitions; **no brief was given `DIRECTION.md` or a repo tour**. Nothing was
committed to the gates after the first worker started.

---

## Superseded LIVE block — CONDUCTOR mode, **WAVE 4 CLOSED: ALL THREE RETURNED**, 2026-08-18

*Demoted from LIVE 2026-08-18 under §3j — the live block keeps the three most recent
records. Nothing deleted, nothing reworded.*

**Plan committed BEFORE dispatch at `8f4cb53`; dispatch record `d0c2c5d`. Gates and pre-committed
readings live there in final wording and are quoted BY POINTER per §3j rule 5, not restated.**

| unit | lane | branch | outcome |
|---|---|---|---|
| `V3` / leg 399 | **V** | `leg/399-v3-gradeA` @ `16ba44e` | **RETURNED. GATE `YES` on 1 row of 9.** Merged. `UNVERIFIED`. |
| `V-W3` | verification | `verify/wave3` @ `2b8755e` | **RETURNED. 3 of 4 CONFIRMED, 1 REFUTED.** Merged. `UNVERIFIED`. |
| `L2′` / leg 397 | **L** | `leg/397-l2-decay` @ `1493e5e` | **RETURNED. GATE `YES`, all 18 techniques.** Merged. §§0–3 byte-identical to the pre-registration. `UNVERIFIED`. |

**THE THREE RESULTS, IN ONE LINE EACH.**
- **`V3`:** leg 174's Grade-A × fluid cell is **OCCUPIED** — `arXiv:2509.25116` passes both of leg
  174's clauses and had never been graded here — **but the certified object is not a finite-time
  singularity**, and W3's prose test and its own named grading predicate **disagree on whether that
  matters**. **Defective wall WORDING → USER escalation, `ESCALATION_W3_WORDING_2026-08-18.md`,
  OPEN, NOT RULED.** Ranking consequence: **Lane V → HELD, Lane L sole priority** — a ranking, not a
  ruling. `V3`'s pre-committed reading (a) fired and was honoured rather than re-interpreted.
- **`V-W3`:** `E`'s claimed **`8×` cost overrun is REFUTED** — `0.0713` is wall-hours at 8 workers,
  `0.57` is core-hours; like for like `E` came in **0.4% UNDER**. **The Conductor's own record broke,
  and the Conductor had written it into a live gate.** Third such defect a verifier has caught.
  Corrected in `STATE.md` and `OPTIONS.md` this commit; **D2–D6 left unrepaired for wave 5.**

- **`L2′`:** Lane L's **first landed unit in 399 legs**, and it **narrowed the lane**: 18 techniques
  read against this object, failing hypothesis named/quoted/located in every one, and **ZERO could
  supply `α > 1.5` even in principle** — `α` is **pinned to exactly 1** (Chae–Wolf Thm 1.1 from
  below; Chae–Wolf Rmk 1.2 + ESŠ from above, restated by Pineau–Vicol `2607.09619` §1.2), and any
  `α > 1` gives **full regularity**. **W4 clause (a) is measured SHUT. §6(i) is NOT retired** —
  nothing was certified. **A closed attack is not a broken wall and is not progress toward Clay.**
  What survives in Lane L: W4 clause (b) — a natively finite-energy ansatz — and `L3`/§6(ii).

**§3i WAS RUN PER UNIT, NOT PER WAVE** — seven questions answered twice in the integration commit.
The re-rank came out of q3/q5/q6 and is recorded in `WALLS.md` and `STATE.md`, not only here.

**HEADROOM AT THIS BOUNDARY (§3j).**

| file | cap | now | headroom |
|---|---|---|---|
| `STATE.md` | 23,639 | 24,576 | 937 |
| `WALLS.md` | 32,526 | 32,768 | 242 |
| `OPTIONS.md` | 23,971 | 24,576 | 605 |
| this LIVE block | 8,192 | see commit | — |

**⚠ THE CAPS ARE NOW THE BINDING CONSTRAINT, AND THIS IS A FINDING, NOT A COMPLAINT.** Three of the
four capped files sit inside **0.7%** of their limits **on live content**, and every named §3j
remedy has been applied: `WALLS.md`'s History is out to `WALLS_HISTORY.md`; `OPTIONS.md`'s `TAKEN`
entries are one line plus a pointer; `STATE.md`'s detail is in the units' journals. Integrating
`L2′` alone required compacting **all three**. **The next wave cannot land a result of this size
without either a structural split or a cap ruling** — flagged for the user, **not decided here**.
What was compacted this commit, so nothing looks silent: `STATE.md` wave-3 block and `V-W3` detail
→ pointers; `WALLS.md` `R2`–`R5` → `OPTIONS.md` §B pointer (their ledger already lives there);
`OPTIONS.md` Lane T `TAKEN` rows → one row. **No measurement was dropped and nothing was unstruck.**

**§3j REMEDY EXTENDED ONE STEP, FLAGGED NOT SILENT.** `WALLS.md`'s named remedy — *retracted text
stays struck but moves to a `## History` section at the foot* — had stopped buying headroom once that
section reached ~2.9 KB. **History moved to `WALLS_HISTORY.md`, struck text byte-for-byte intact,
nothing deleted, nothing unstruck**, every `## History` pointer resolving there. `OPTIONS.md` was compacted again here under its own named remedy.

**Cycles: context was summarised twice this Conductor session**; all four files were re-read from
disk after each. `git ls-remote` checked before **both** integrations: **no concurrent push**; `origin/main` and
local `main` agreed at `950115f`, then at `6320790`.

---

## Superseded LIVE block — CONDUCTOR mode, **WAVE 3 CLOSED AND INTEGRATED**, 2026-08-18

**WAVE 3'S OUTCOME: ONE UNIT OF FOUR RETURNED.** Established from `origin`, not from prose.

| unit | lane | branch on `origin` | outcome |
|---|---|---|---|
| `V-W2` | verification | `claude/wave-3-conductor-dispatch-7rdhlg` @ `594ff89` | **RETURNED, AUDITED, LANDED.** Verified wave 2 (`T4`, `T6`, `T5`) and discharged `T1`'s machine record. Itself `UNVERIFIED`. |
| `V2` / leg 396 | V | **none** | **DEAD. Zero bytes.** No branch, no commit. Gate unanswered. |
| `L2` / leg 397 | L | `leg/397-l2-decay` @ `a9a4370` | **DEAD, but its pre-registration SURVIVED** because it was committed: `experiments/journal/leg_397.md` §§0–3 (object, leg 381's banked bill, search plan, controls, criteria), 256 lines, **fully resumable**. Gate unanswered. |
| `L3′` / leg 398 | L | **none** | **DEAD. Zero bytes.** No branch, no commit. Gate unanswered. |

**"COMMIT DURING THE RUN" PAID FOR ITSELF A SECOND TIME.** Three units died; the only one that left
anything behind is the one that had committed. This clause, and mandatory checkpointing above ~1 h
wall, go in **every** brief. Wave 4's briefs carry both.

### §3i THE DIRECTION CHECK — answered against the RECORD, 2026-08-18

1. **Did a unit move an L1→L4 link?** **No.** `V-W2` is verification; the other three produced no
   measurement. The chain has not moved in 398 legs.
2. **What did it make FALSE?** `V-W2` made false the live possibility that `T4`/`T6`/`T5`'s headline
   numbers were transcription artefacts: items (1) and (2) were re-measured from **re-fetched primary
   artefacts whose SHA-256 matched the banked digests exactly**. It also falsified a **Conductor
   wording defect**, ruled at landing against the Conductor's own wording (`WALLS.md` History).
   `V2`, `L2`, `L3′` made nothing false.
3. **Do the lanes still deserve their rank ON WHAT IS MEASURED NOW?** **Lane L: yes, and re-earned —
   zero units in 398 legs, and leg 390 measured §6(i)/(ii) OPEN in *both* branches, so it is on every
   path. Lane V: rank UNCHANGED but now CONDITIONAL on `V3`** — see q4. Lane T stays DEFERRED; nothing
   re-opened it. Lane R never sets a wave's direction.
4. **Is a live claim resting on a source whose recorded ceiling is undischarged?** **YES, and this is
   the wave's finding.** `WALLS.md` W3 carried *"leg 242 confirms nobody filled it since."* Leg 242's
   gate is an **author-line** question about Dahne–Figueras, answered `NO` over twelve author nets —
   it closes the CGL line, **not the cell** — and **its own control net surfaced six fluid blow-up
   computer-assisted proofs (`2509.25116`, `2605.19716`, `2605.15149`, `2604.09949` among them) and
   graded none against leg 174's Grade-A criterion.** Leg 174's matrix rests on an 11-row hand-built
   ledger recording a **Tier** ceiling and **no coverage ceiling**. **Struck in `WALLS.md` W3 and
   `OPTIONS.md` §C as a flag on the SUPPORT, not a retraction of the wall:** nothing measures that
   anyone DID fill the cell, and W3 stands until something does.
5. **Cheapest unit that could KILL the priority lane, and why is it not next?** **`V3` — grade the
   `fluid × Grade-A` cell against leg 174's own unchanged Grade-A criterion, starting from leg 242's
   six ungraded CAPs. It IS next.** If one grades Grade-A, W3 is broken by someone else and Lane V's
   premise dies for ~2–3 h of reading.
6. **If Lane V died tomorrow, what instead, and is it cheaper?** **Lane L, and yes** — `L2′` resumes a
   committed pre-registration at ≈2–4 h against a full `V2` build. Lane L is on every path regardless
   of how `V3` lands, which is why wave 4 runs both.
7. **Are we in an audit/instrument loop?** **YES — the last three landed units are `V1`
   (verification), `E` (instrument), `V-W2` (verification). Three of three.** Remedy applied in the
   wave-4 plan: **the wave opens with construction and the verifier is dispatched last.**

**RE-RANK MADE (q3/q5):** priority order **V, L** is unchanged, but **Lane V's rank is now
conditional on `V3`.** If `V3` finds a Grade-A fluid row, Lane V's premise is dead and Lane L becomes
sole priority in the same commit. Recorded in `WALLS.md` §LANE PRIORITIES.

### §3j HEADROOM REPORT — wave boundary 2026-08-18

| file | cap | now | headroom |
|---|---|---|---|
| `STATE.md` | 23,639 | 24,576 | 937 |
| `WALLS.md` | 32,526 | 32,768 | 242 |
| `OPTIONS.md` | 23,971 | 24,576 | 605 |
| this LIVE block | 8,192 | see foot | — |

**Context WAS summarised — twice — during this Conductor session.** All four files were re-read from
disk after the fork closed and after each summarisation, per §3j. Remedies used: `STATE.md` detail
moved to journals leaving pointers; `WALLS.md` retracted text moved to a `## History` foot section;
`OPTIONS.md` `TAKEN`/`KILLED` entries compressed to one line plus a pointer; this file truncated to
the three most recent superseded blocks with the accumulating sections carried verbatim.

### Standing obligations wave 4 MUST carry (not preferences — contract)

- **A VERIFIER for `E` AND for wave 3's own units.** `V-W2` covered wave 2 only; `E` (`d0d72b1`) and
  `V-W2` (`594ff89`) are both `UNVERIFIED`. **YOU MAY NOT VERIFY A WAVE YOU PLANNED** — the verifier
  is dispatched in the wave *after* the units it checks.
- **Whatever `L2` needs to finish.** Lane L's first unit in 398 legs, pre-registration committed.
- **The composition floor: at least one unit attacking a wall on the Clay chain directly.** Three
  consecutive waves met it from Lane T. Wave 4 meets it from **V and L**, per q6.

### Open escalations

| id | what | state |
|---|---|---|
| ban-wording packet (`T1`) | on the user's desk | machine record **DISCHARGED** by `V-W2` (`writeup/data/p2_route_t1_packet_v1.json`, 31/31, exit 0) |
| lift-clause defect (leg 257 / fourth space) | recorded in `OPTIONS.md` §F, **NOT ruled** | a ban-wording question is a **user** escalation, never a Conductor's call |
| C1 exemplar | **DISCHARGED** 2026-08-14 | C1 stands **EXEMPLAR-FREE**; no unit may cite it as evidence the technology closes for any object class |

### What the next Conductor must do first

Read `STATE.md`, `WALLS.md` whole, `OPTIONS.md`, `ORCHESTRATION.md` §§3g–3j, run
`.venv/bin/python plan_of_record.py`, then this file. **Never `DIRECTION.md`.** Check
`git ls-remote --heads origin` before any handoff — concurrent sessions commit to `main` mid-run and
also diverge onto their own branches.

---

## Superseded LIVE block — CONDUCTOR mode, WAVE 3 PLANNED AND COMMITTED BEFORE DISPATCH, 2026-08-14

**`main` = this commit.** The user's ruling on `ESCALATION_C1_EXEMPLAR_2026-08-14.md` is transcribed
(one commit per item, `test_plan_of_record.py` ALL GATES PASS after each), and the wave-3 plan is
committed **before any worker is dispatched**, per §3g step 1. **`STATE.md` is authoritative on
every gate's wording**; this block is the successor's fallback.

### The ruling, transcribed 2026-08-14 — four commits, no ban touched

| # | item | commit |
|---|---|---|
| 1 | `RULING_C1_EXEMPLAR_2026-08-14.md`; escalation **DISCHARGED** | `e60e8f4` |
| 2 | `OPTIONS.md` — Lane T **DEFERRED** with cost + two re-open conditions; Lanes **V** and **L** **ACTIVE, PRIORITY** | `41c9f1e` |
| 3 | `WALLS.md` lane priorities + `plan_of_record.py` `LANES`/`POSTURE_LIMITS` (**`BANNED` table byte-identical, verified mechanically: 17128 bytes before and after**) | `ff73307` |
| 4 | `STATE.md` regenerated + this block + the wave-3 plan | this commit |

**The rulings in one line each.** **(1) C1 needs NO replacement exemplar and STANDS
EXEMPLAR-FREE** — it is an apparatus scoping, true independent of any instance; **the scope no
longer carries any implied *"and this has been demonstrated"* and NO UNIT MAY CITE C1 AS EVIDENCE
THE TECHNOLOGY CLOSES FOR ANY OBJECT CLASS**; the **naming requirement is unchanged and binds every
unit**, and the Conductor may not waive it. **(2) Lane T's priority-1 ranking does NOT survive —
DEMOTED TO DEFERRED**, kept alive only through **`T2″`**; **`T3` deferred WITH the lane, not
killed**; two re-open conditions recorded in `OPTIONS.md` §E. **Nothing measured is superseded.**
**(3) The packet's defect was material to the RANKING, not to the SCOPING** — C1's transcription in
`plan_of_record.py` stands byte-unchanged; A2, B1 and the narrowed outreach hold untouched.
**DIRECTION: the priority lanes are now V and L.** **Ban counts unchanged: 26 recorded, 19 in force.**

### Wave 3 — units, branches, gates (abbreviated), pre-committed readings

**Composition floor (§3g): met TWICE OVER** — `V2` attacks **W3**, `L2` attacks **W4 / §6(i)**.
**§3f rule 3 satisfied:** the wave opens with construction (`V2`), dispatched first.

| unit | lane | branch | gate (final wording, abbreviated) | pre-committed reading | state |
|---|---|---|---|---|---|
| `V2` / leg 396 | **V**, CONSTRUCTION | `leg/396-v2-target` | Does the unit deliver **both** (A) a **named dissipative fluid target** in the lowest dimension admitting fluid structure, dissipative term **inside** the certified equation, with its ansatz; **and** (B) a **feasibility verdict** for a **C1-compliant** apparatus (Galerkin-plus-tail closure and/or leg 315's `O1` Taylor-model flow map), apparatus **named with a citation** and **shown to build no single bounded approximate inverse uniform in `M`**? `no` → a **measured list of candidate targets with the named property each fails**, which is landable. `UNDER-RESOURCED` + a cost, never a bare `no`. | (a) a named target is **not a certificate**; (b) a feasibility is **not a result on the Clay chain**; (c) **W3 breaks only on leg 174's own Grade-A criterion, unchanged**; (d) if the apparatus turns out to need a bounded approximate inverse uniform in `M`, **STOP and say so** — `T4`'s branch (c), more valuable than the verdict; (e) the negative branch is as valuable as the positive and is not softened; (f) novelty pass owed — if the target is already certified, **W3 is broken by someone else and that is the finding**; (g) controls that fire **both** ways (Dahne–Figueras CGL as the Grade-A-but-not-fluid positive); (h) lesson 91 | **DISPATCHED** |
| `L2` / leg 397 | **L** | `leg/397-l2-decay` | Reading the published localisation/far-field-decay techniques against **this object** (route 4's DSS profile carrying leg 381's bill: `L³` tail **326.875/decade**, `α > 1.5` required vs `α = 1.0` available), does the unit state **per technique** the **named hypothesis** that fails — or the one that does not? Quote it and locate it. `no` → what it would take (§3d), `UNDER-RESOURCED`. | (a) a measured **"still no method, and here is precisely which hypothesis fails"** is a **real, landable result** — the answer to whether the Tier-2 ceiling is permanent — **and is not softened**; (b) a candidate is a **lead, not a broken wall**, until leg 381's bill is actually paid; (c) the deficit comes from the **artefact**, never prose; (d) **READ, do not CONTACT**; (e) instrument every zero, `THROTTLED`/`UNREACHABLE` never zeros, **no S2 key exists**; (f) lesson 91; (g) ceiling | **DISPATCHED** |
| `L3′` / leg 398 | **L**, literature | `leg/398-l3p-chenhou` | At **full text**, `arXiv:2308.01528` + the Chen–Hou stability line: **(a)** does its unbounded-domain / algebraic-decay / computer-assisted mechanism bear on **leg 348's compact-domain obstruction — and on which side** (UNDERCUT / STRENGTHEN / DOES NOT REACH)? **(b)** does its nonlinear-stability-with-finite-unstable-spectrum technique reach **§6(ii)** for this object, and **which hypothesis** would this object have to satisfy? Deciding sentence **quoted and located**. | (a) three branches named in advance, **no fourth**; the prior is **DOES NOT REACH** (`T6`: stationary self-similar target, energy-estimate apparatus) and the unit must say whether full text **agrees or disagrees**; an undercut is the valuable branch and is **reported first**; (b) reaching §6(ii) **in shape is not a method** — **W5 stays unbroken**; (c) a confirmation is **not** a strengthening; (d) **READ, do not CONTACT** — contact is **HELD**; (e) `UNREACHABLE`/`THROTTLED` banked as such, **never zeros**; (f) ceiling | **DISPATCHED** |
| `V-W2` | verification, **OBLIGATORY** | `verify/wave2` | From **banked JSON and landed evidence scripts alone**, do these reproduce exactly: **(1)** `T4`'s 2D-lift finding (`N_x3=0`, extent 1 in `x₃`, `max|u⁽³⁾|=max|ω⁽¹⁾|=max|ω⁽²⁾|=0.0` exactly vs `max|ω⁽³⁾|=1.6351/1.5274`, `setup='2D'`); **(2)** `T4`'s first conjunct ((4.32), `5.6e-15`, `δ=5.3e-06` vs `1e-3`) **and** the apparatus term counts (7/4/5/2) against **all six** closure terms at **zero**, Zgliczyński only as [48]; **(3)** `T6`'s **7/7, 2 UNDERCUT/4/1, 0 UNREACHABLE, 0 THROTTLED** and the `2409.09234` no-slip-walls undercut; **(4)** `T5`'s **1428 files / 417,476 lines**, **7 refusals APPARATUS 5 / REALIZATION 2**, **exactly 2** re-openable, **leg 257 not**. **PLUS the folded-in obligation: bank `T1`'s missing machine record** — the packet's three questions and the fact it **ruled none** — with an evidence script that **exits non-zero** on disagreement with the escalation document. | (a) agreement is expected and worth little; (b) **a disagreement is BANKED, not reconciled** by the verifier; (c) a claim the JSON cannot support is **`UNVERIFIABLE`, not `no`**; (d) **must not read** `STATE.md`, `WALLS.md`, `OPTIONS.md`, `DIRECTION.md`, this file, the briefs, or the wave-2 reasoning — **that narrowness IS the unit**; (e) **filename trap: `p2_route_p2t1_v1.json` is leg 302, unrelated** — scan `leg`/`route`/`unit` **fields**, not filenames; (f) banking `T1`'s record does **not** re-open its gate answer; (g) ceiling | **RETURNED, AUDITED, LANDED** |

**Figure allocation at dispatch: `fig111` → `V2`, and to no one else.** `L2`, `L3′` and `V-W2` were
allocated **no figure** (the figure-collision incident is why this is stated at dispatch).
**Every brief instructs: push the branch only, never merge and never push to `main`** — the
Conductor gates and merges. **No brief was given `DIRECTION.md`** (§3e). Territories are disjoint.

> ### ⚠ WAVE 4 MUST CARRY WAVE 3's VERIFIER
> `V2`, `L2` and `L3′` land **`UNVERIFIED`** and this Conductor planned them. A wave-4 plan without
> that verifier is **out of contract**. Written here as well as in `STATE.md` so it survives the
> loss of either file.


### `V-W2` — RETURNED, AUDITED AND LANDED, 2026-08-14

**Gate answer: ALL FOUR ITEMS REPRODUCE**, audited by the Conductor against the gate committed at
`42011ff` **before the unit existed**. Items (1) and (2) are **measurements, not transcription
checks**: `Papers/` is untracked and was empty in the worker's worktree, so it **re-fetched all
three primary artefacts read-only and every SHA-256 matched the banked digest exactly**, then
re-derived from them. It did **not** accept a unit's own script agreeing with itself.

- **(1)** `T4`'s 2D lift: bit-for-bit on every field (`N_x3 = 0`, `x₃` extent 1, the three exact
  zeros, `max|ω⁽³⁾| = 1.6351/1.5274`, `setup = '2D'`).
- **(2)** `T4`'s first conjunct: recomputed from the paper's own (4.33)/(4.34); smallest non-zero
  deviation **`5.618065e-15`**, `δ = 5.2748360312e-06` vs `1e-3`. Term counts **7/4/5/2** recounted,
  all six closure terms **0**, Zgliczyński once as **[48]**. *Refinement, not a contradiction:* the
  bracket `[48]` is cited once in the body as prior work on Kuramoto–Sivashinsky.
- **(3)** `T6`: **7/7, 2 UNDERCUT / 4 / 1, 0 `UNREACHABLE`, 0 `THROTTLED`** — recounted with
  `Counter`, not read off the banked totals. Both leg-348 lock hashes still hold.
- **(4)** `T5`: corpus re-enumerated with `git ls-tree` — **1428 files / 417,476 lines**,
  `DIRECTION.md` absent **and the exclusion asserted executably**; **7 refusals, APPARATUS 5 /
  REALIZATION 2**; **exactly 2** re-openable; leg 257 not. All 7 quotes still at their `file:line`.

**THE ONE NUANCE, BANKED UNRECONCILED — AND IT IS A FINDING AGAINST THE CONDUCTOR'S WORDING, NOT
AGAINST `T6`. RULED AT LANDING:** the gate said `2409.09234` *"carries no-slip walls, not
periodicity, **so** the census over-counts by one."* `T6`'s **own** stated ground is *"THIS PAPER
CLOSES NO TAIL-DOMINATION ESTIMATE AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL"*, with the wall
point filed as `u_code` **U1, secondary**. **Verified independently by the Conductor against
`writeup/data/p2_route_t6_v1.json` at landing.** Both facts reproduce; **the `so` was mine.** The
count is unchanged (**6 − 1 = 5**) and `WALLS.md` now leads with the primary ground. Also measured:
the paper **never uses the phrase "no-slip"** (0 occurrences) — it states a **moving-wall Dirichlet
condition** with *"periodicity … to the rest of boundaries"*. **This is the SECOND Conductor-wording
defect a verifier has caught** (`V1` caught the first, on `R0`'s comparand). Neither was found by
the Conductor.

**`T1`'s OWED MACHINE RECORD: DISCHARGED.** `writeup/data/p2_route_t1_packet_v1.json` +
`experiments/p2_route_t1_packet_evidence.py`, **31/31, exit 0**, `questions_ruled = 0`, carrying
`does_not_reopen_t1_gate_answer: true`. **Mutation-tested three ways by the unit and once more
independently by the Conductor at landing** (`questions_ruled` 0 → 3 ⇒ **exit 1**; restored ⇒
**exit 0**, file bit-identical). The filename trap was instrumented rather than merely avoided: a
**field-scoped census of 306/306 banked JSONs** found **no record carrying leg 391 or unit `T1`**,
and confirmed `p2_route_p2t1_v1.json` is leg 302 / route P2T1 / unit null.

**Two errors the unit found in ITSELF and recorded**, which is why its agreement is worth
something: a wrong pre-registered radii formula (textbook quadratic instead of the paper's validity
bound) that **would have banked a 70% false discrepancy**, and a strict-whitespace quote locator
that reported 0/7 before repair. **Forbidden-read list honoured** and stated. Evidence **100/100,
exit 0**, with 2 checks reporting **`skip` plus the banked SHA-256** rather than passing silently.

**One banking-discipline observation the Conductor makes and does NOT edit:** the unit's
`unreconciled_disagreements` array is **empty** while its own summary calls the nuance *"the one
unreconciled disagreement"*. The nuance **is** banked, in `item_3`, so nothing is lost — but the
machine-readable field and the prose disagree, and lesson 68 says the machine-readable one is what
survives. Recorded here; **the unit's file is not edited by the Conductor.**

**Environment side effect, recorded rather than glossed:** the unit installed **`scipy`** into the
shared gitignored `.venv` to read the authors' `.mat` files. **No tracked file changed.**

### `E` (wave 1) — **DID NOT RETURN. GATE UNANSWERED. NOT LANDED, AND THAT IS A DECISION, NOT AN OVERSIGHT.**

Branch `prog-r4/e-hhard` on `origin`, tip **`6a706f7`** (pre-registration `70f3962`, diagnostics
`952b2cf`, evidence+`fig109` `6a706f7`). **Diagnostics (1) and (2) RETURNED with planted controls
firing BOTH ways** — (1) `PULL_TO_LOW_S`, (2) `MIXED` at permutation `p = 0.9317`, so the unit does
**not** get to say the minimisation drags the solve. **Diagnostic (3) never completed:** the host
killed it twice; 8 of 16 attempts reached per-attempt checkpoints, and **the checkpoints and U2's
gitignored `T = 1e5` DNS archive are both gone with the container** (verified: no `*.npz` DNS
archive and no `e_hhard_partial/` in this checkout).

**NO BRANCH OF ITS PRE-COMMITTED READING FIRED.** `E-i`…`E-iv` are **all** about diagnostic (3)'s
outcome, so **none is claimed**, and H-hard is exactly where wave 1 left it.

**Why it is NOT merged, departing from the previous block's *"land (1) and (2) either way"*:** its
evidence script and `fig109` were written for the **complete** unit and **fail on the partial JSON**
(`KeyError: 'diagnostic_3'`, reproduced by the Conductor), and merging also **registers `fig109` in
`writeup/build_figures.py`**, so the merge would put a **failing figure build and a failing evidence
script on `main`**. The alternative — editing another unit's evidence script to make it green — is
the exact move this repository refuses (`V1` committed run 1 **as it ran**, exit 1, rather than
adjust an artefact to pass). **The branch is on `origin` and is durable; it is the record.**

**Cost to finish, from the record's own banked rates:** regenerate U2's `T = 1e5` DNS ≈**3.4 h**,
then 16 attempts at up to the 52-epoch cap (≈1.4 h each serial) ≈**2.7 h wall at 8 workers** —
**≈6–7 h wall in total**, and it buys **the sharpest single test of H-hard available**, never yet
run at this realization. **Ranked for wave 4.** Its result re-opens the Lane R rankings in
`OPTIONS.md` §A/§B; **it does not change wave 3's composition**, which the user ruled.

### Open escalations

| escalation | state |
|---|---|
| `ESCALATION_C1_EXEMPLAR_2026-08-14.md` | **RULED AND DISCHARGED 2026-08-14.** Ruling at `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`; transcribed in four commits, **no ban lifted, narrowed or reworded**. |
| `ESCALATION_BAN_WORDING_2026-08-13.md` | **RULED AND DISCHARGED 2026-08-13** (`RULING_BAN_WORDING_2026-08-13.md`). A2, B1, C1 and the outreach narrowing all transcribed. |
| Author contact | **STILL HELD BY THE USER.** Reading any published document is authorised; contacting an author, group, maintainer or list is not, and needs its own ruling. **Both `L2` and `L3′` carry this verbatim.** |
| The *"FOURTH space/basis"* lift-clause defect | **RECORDED, NOT RULED, and deliberately not escalated** — nothing currently depends on it while Lane T is deferred, and an entity that both raises and rules an escalation has defeated the mechanism. `T5` measured that it is exactly what blocks leg 257. |

### What the next Conductor must do first

**Audit each wave-3 branch against the gate committed in `STATE.md` BEFORE it was dispatched, land
what passes, regenerate `STATE.md`, refresh this block in the same commit (§3g step 4), and push.**
Only then re-plan. **Wave 4 must carry wave 3's verifier**, and `E` and `L1` are the two units
ranked for it.

---

## Superseded LIVE block — CONDUCTOR mode, wave 2 COMPLETE AND INTEGRATED, 2026-08-14

> **SUPERSEDED 2026-08-14 by the wave-3 block above**, which carries the user's ruling on
> `ESCALATION_C1_EXEMPLAR_2026-08-14.md` and the wave-3 plan. **Retained verbatim, not
> deleted** — its wave-2 audit trail, gate texts and `E` instructions are history a successor
> needs. Two of its statements are overtaken and are corrected in the block above rather than
> edited here: *"plan wave 3 with `T3`, `T2″` and Lane L ranked first"* (Lane T is now
> **DEFERRED**; the priority lanes are **V and L**), and *"land (1) and (2) either way"* for
> `E` (not landed — its evidence script and `fig109` fail on the partial JSON, and the merge
> would put a failing figure build on `main`).


**ALL NINE UNITS OF BOTH WAVES HAVE RETURNED, BEEN AUDITED AND LANDED, AND EVERYTHING IS PUSHED.**
Wound up on the user's instruction: *"complete what is outstanding from wave 2, complete E, and then
wind up, push all to main."* **This is a wind-up, not a stop** — no lane is held and no ban changed.

| unit | wave | gate answer | landed |
|---|---|---|---|
| `T4` | 2 | **`STOP`, pre-committed branch (c)** — `1902.00384` is certified by the BANNED apparatus and both rows are **2D lifts** | `2c87244` |
| `T6` | 2 | **7/7 read. 2 UNDERCUT / 4 strengthen / 1 confirm.** 0 UNREACHABLE, 0 THROTTLED, 0 zeros | `e7db624` |
| `V1` | 2 | **all five wave-1 claims reproduce; `M3 = DELIVERED` SURVIVES**; two defects banked | `2fb399f` |
| `T5` | 2 | **7 refusals, APPARATUS 5 / REALIZATION 2, 2 re-openable and unranked** | `a6f0c38` |
| `E` | 1 | **PASS** — all three diagnostics RETURN with two-sided controls; branch **`E-iii`**; **0 of 16 recovered any named row** | `d0d72b1` |

**THE TWO RESULTS.** (i) **Lane T's central premise is measured FALSE** — twice, by two units, by
two different methods — and the record has been **corrected rather than defended**. (ii) **The named
Table IV rows are not reachable even from their own published coordinates**, with a positive control
proving the predicate can return a recovery. **Neither is a Clay advance. Ceiling TIER 2; no
`L1→L4` link moved; Clay stays ~0.05%.**

**OPEN ESCALATION, AWAITING THE USER:** `writeup/escalations/ESCALATION_C1_EXEMPLAR_2026-08-14.md`.
C1's *general proposition* stands; its *exemplar* has fallen. Three questions are put; none is the
Conductor's to answer.

**What the next Conductor must do first: READ THE WIND-UP BLOCK BELOW** (§ *"WOUND UP BY USER
INSTRUCTION, 2026-08-14"*). In short: plan wave 3 and commit the plan **before** dispatching, and it
**must carry the verifier for `T4`, `T6`, `T5` AND `E`** — this Conductor planned all four and may
not check any of them — **alongside** a real Lane T/V/L unit, since a verifier is an audit and both
the composition floor and §3f rule 3 bite.

### ⚠ READ THIS BEFORE ACTING ON ANYTHING ABOVE — A CONCURRENT CONDUCTOR SESSION EXISTS

**Found on `origin` at wind-up, 2026-08-14, after this session's work was pushed.** A **second,
concurrent CONDUCTOR session** has been running against this repository on branch
**`claude/wave-3-conductor-dispatch-7rdhlg`** (tip `594ff89`, 2026-08-14 02:00 UTC). It branched from
**`2928966`** — this session's wave-2 integration commit — and it is **NOT** downstream of `E`. **The
two histories have diverged and neither contains the other.**

**Established by inspection of the remote, not assumed:**

| on that branch | consequence for the record above |
|---|---|
| `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md` (130 lines), transcribed in 4 commits, escalation marked **DISCHARGED** | **The C1 escalation is described as OPEN throughout `main`. On that branch it is RULED.** |
| `WAVE 3 PLANNED AND COMMITTED BEFORE DISPATCH: V2, L2, L3′, V-W2` (`42011ff`) | **Wave 3 is already planned and dispatched there.** The ranked candidates below are this session's, made without knowledge of it. |
| `V-W2` landed (`594ff89`): *"wave 2 is VERIFIED"*, with `p2_verify_wave2_v1.json` and `p2_verify_wave2_evidence.py` | **The wave-2 verification debt asserted below may already be discharged.** |
| `p2_route_t1_packet_v1.json` + `p2_route_t1_packet_evidence.py` | **`T1`'s missing machine record — banked as an obligation in `OPTIONS.md` §F — appears to be REPAIRED there.** |
| `leg/397-l2-decay` (`a9a4370`), pre-registration only | A **Lane L** unit is in flight there. Lane L is described below as having zero units in 395 legs. |

**WHAT THIS CONDUCTOR DID AND DID NOT DO, deliberately.** It **did not merge that branch.** Three
reasons, each sufficient: (i) `V-W2` verifies **the wave this Conductor planned**, and blessing one's
own verifier is exactly what §3f rule 1 exists to prevent; (ii) the ruling **was never delivered to
this session** — transcribing a user ruling received second-hand off a branch is not transcription,
it is inference, and ban-wording questions are prohibited to the Conductor in any case; (iii) that
branch is **live work with a unit still in flight**, and merging it is its own session's integration
step, not this one's. **Nothing on that branch has been read into any claim on `main`.**

**THE RECONCILIATION IS THE NEXT SESSION'S FIRST TASK, BEFORE IT DISPATCHES ANYTHING.** `main` holds
`E` and this wind-up; that branch holds the ruling, wave 3 and `V-W2`. **Neither is wrong; both are
partial.** Do not re-dispatch a wave-3 verifier, do not re-raise the C1 escalation, and do not
re-do `T1`'s record until that branch has been read. **Expect a real conflict in `STATE.md`** — that
branch rewrites it heavily (+1072/−768) from a base that predates `E`, so `E`'s row and this
wind-up block exist on **one side only.**

---

## Wave 2 as dispatched and everything older — DROPPED 2026-08-18 under §3j

The live block is truncated to **the three most recent** status blocks. Wave 2's dispatch
block, the 2026-08-14 wind-up, and every block from the four-slot-contract era (2026-08-07 to
2026-08-12) are in git history and their results are in `STATE.md`, `WALLS.md` and `OPTIONS.md`.
The accumulating sections below are carried forward **verbatim**, as §3j requires.

---

# Accumulating sections — carried forward verbatim across every handoff

Everything below this line is the run's institutional memory ([ORCHESTRATION.md](../ORCHESTRATION.md)
§9d): things a session learned by losing time to them. A handoff rewrites the live state
*above*; it carries these sections forward, adds to them, and deletes an entry only when it is
provably obsolete. (Added 2026-08-11, ported from the Project Building Engine.)

## Environment notes (carry forward every session)

0. **`Papers/` IS UNTRACKED AND A FRESH CONTAINER HAS IT EMPTY**, and the same is true of every
   gitignored working directory — `.venv/`, `experiments/programme_r4/*.npz`, per-unit checkpoint
   directories. **Anything a unit needs across containers must be in git or re-fetchable.**
   `V-W2` (2026-08-14) turned this into an advantage rather than a blocker: it **re-fetched all
   three primary artefacts read-only and checked every SHA-256 against the banked digest**, which
   made its items (1)–(2) measurements rather than transcription checks. **Copy that move** —
   re-fetch and hash-check, and if a source cannot be reached, bank `UNREACHABLE` with the banked
   digest, never a silent pass. Note also: **`.venv/` is gitignored, so a fresh git worktree has
   none.** `ln -s /home/user/blowup-search/.venv .venv` inside the worktree resolves it.
   **`scipy` was installed into that shared `.venv` on 2026-08-14** (to read the authors' `.mat`
   files); no tracked file changed.

1. **The orchestrator session itself can be suspended for going quiet**, taking every
   dispatched background agent and all `TaskOutput`/`SendMessage` handles with it, while the
   git worktrees survive on disk. Keep a `send_later` heartbeat armed whenever agents run
   unattended (ORCHESTRATION.md §9f); it fires from outside the container and can wake a
   suspended session, which a completion notification cannot.
2. **Account-wide usage limits kill all agents simultaneously** with a "session limit" error
   naming a reset time. This is not an agent failure: do not re-dispatch until the named reset
   time has passed, and salvage worktrees first (finished work can be gated and landed on the
   agent's behalf; partial work is pushed as raw WIP branches, never merged) — see the
   2026-08-07 incident below.
3. **`send_later` does not exist in this environment; the §9f heartbeat has no true
   out-of-session waker.** `ToolSearch` for it returns nothing. The closest available tools
   are `CronCreate` (cron-style, **session-only, in-memory, dies with the session**) and
   `ScheduleWakeup` (only valid inside `/loop` dynamic mode). This session armed a recurring
   `CronCreate` every 7 minutes, which does re-invoke an *idle-but-alive* session — but it
   **cannot wake a suspended or reclaimed one**, which is the exact failure mode of the
   2026-08-06 incident. Treat the heartbeat as partial cover: it catches an orchestrator that
   has gone quiet, not a container that has been reclaimed. Nothing better is currently
   available; do not spend a cycle re-searching for `send_later`.
4. **The Headroom MCP compression proxy rewrites large tool outputs.** Long `Bash` output and
   long subagent replies come back **lossily summarised** — sentences with words dropped, and
   a trailing `[N items compressed to M ...]` marker. Consequences: never trust a long piped
   `bash` result for exact values; read files with the `Read` tool (which is not compressed)
   when precision matters; and ask subagents for **short** replies, putting the detail in a
   committed file you read yourself. A DM reply of ~120 lines came back with three roster
   rows mangled this session and had to be re-read from `DIRECTION.md`.
5. **This file's live state can lag the true latest handoff.** At least one handoff
   (2026-08-11, commit `c14b9c5`) recorded its actual state in the commit message while this
   file still showed an older pause. Cross-check `git log -- reports/ORCH_STATE.md` against
   `git log` on `main` before trusting the header above.

**2026-08-19 — THE TOOL-OUTPUT CHANNEL DROPS WORDS, INCLUDING INSIDE `repr()`.** Hit independently by `P4-DRAFT` (leg 414) and by the Conductor twice this session, reading `WALLS.md` and `test_headroom.py`; characters are silently removed from the middle of lines. **Any ruling made by eye off a piped tool read is unsafe.** Byte-level checks and exact file reads are the only trustworthy read. This is an ACTIVE hazard, not historical.


- **LEAKED WATCHER PROCESSES OUTLIVE THE UNITS THEY WATCH — measured 2026-08-19, and it is worse
  than the unit that reported it knew.** `E-FE` (leg 408) disclosed on teardown that four of its own
  watchers survived the solver and kept firing heartbeats reading `160/160` for over a day: the
  heartbeat loop's `break` on zero driver processes is evaluated only AFTER its `sleep 3600`, and the
  sibling `tail -f | grep` log watcher had **no exit condition at all**. **Conductor finding: the leak
  is at least two units deep.** A `ps` sweep at integration time found
  `tail -f experiments/route4/l6b_run.log` **still alive at 65,611 s = 18.2 hours**, belonging to
  `L6-b` — a WAVE 8 unit that closed before `E-FE` even landed — plus two `sleep 3600` loops of ages
  1,430 s and 244 s.
- **I did NOT kill them, deliberately.** A concurrent CONDUCTOR session exists (recorded on `main`,
  `772399f`), process ownership is not determinable from inside this session, and killing another
  session's watcher is not a wind-down integrator's call. A blocked `tail -f` costs a PID and an fd,
  not CPU. **The finding is recorded; the cleanup is left to whoever owns the processes.**
- **Cheap fix for every future unit, from `E-FE`'s own teardown:** give every watcher a hard deadline
  (`timeout`), and test the break condition BEFORE the sleep, not after.
## Known flakes

Tests confirmed to fail under load (many worktrees gating at once) and pass in isolation —
re-run alone under low load before treating one as a regression (ORCHESTRATION.md §9g).

| Test | Trigger | Times re-confirmed clean |
|---|---|---|
| — | | |

## Incidents and root causes

**2026-08-18 — a units error survived four documents, a wave plan and a live gate.** `E`'s cost was
recorded as an `~8×` overrun against its commissioning estimate. `V-W3` refuted it: `0.0713` is
**wall**-hours per attempt at **8 workers** and `0.57` is **core**-hours per attempt, so the `8×` is
`core ÷ wall` and is numerically the worker count (`7.967`). Like for like, `E` came in **0.4%
under**. **Root cause: the repository has no convention forcing a time figure to name its unit at the
point of use.** `WALLS.md`'s R0 block already warned that the R0 denominator is worker-hours and that
physical core count is banked in **no numeric field of either JSON** — the warning existed and did
not stop the error, because it lived in one file and the numbers lived in four others. **Fix owed
(not done here, it is a unit): every banked duration field carries its unit in its key, and
`plan_of_record.py` or a test enforces it.** Contributing factor: the Conductor wrote the bad
comparison into `V-W3`'s own gate, so the verifier was asked to confirm an artefact of the record —
which is exactly why the gate said *"real, or an artefact of what was counted?"* and why that
phrasing was worth having.


One short paragraph each: what happened, how it was diagnosed, what changed as a result.

- **2026-08-06 — 13 agents lost simultaneously.** All stopped mid-novelty-pass ~10 minutes
  after dispatch, with the orchestrator's tracking of all 13 breaking at the same moment;
  diagnosed as the orchestrating session (and its container) being judged idle and suspended,
  not 13 independent failures. Worktrees survived; commits were recovered by hand. Result:
  the §9f heartbeat contract.
- **2026-08-07 — account-wide usage limit hit mid-run.** Five agents died with the identical
  "session limit" error. One leg (261) was actually finished and was gated and landed on its
  behalf; three were salvaged as raw WIP branches; one had nothing to salvage. Result:
  environment note 2 above.
- **2026-08-11 — unpushed local work found across ~21 branches.** A post-handoff check found
  17 leg/verify branches plus 4 worktree-agent branches holding commits that existed nowhere
  on origin, including live-leg WIP the 2026-08-11 handoff had described as committed locally.
  All were pushed (diverged same-name branches under `-local-snapshot` suffixes). Result: the
  §7b leg liveness rules and the §9g liveness sweep were adopted the same day.
- **2026-08-11 (second occurrence, same day) — 17 more unpushed local branches, including a
  finished result.** The next orchestrator session ran the same sweep at Step 0 and found 17
  branches with commits absent from `origin`, hours after the first sweep was supposed to have
  closed this. The serious one was `leg/266-p0tc-v1`: a **completed GATE YES** — the correction
  to leg 251's certificate obligation #1, the item blocking the user-facing Phase-1 packet —
  finished on 2026-08-07 in a session that died before its finish protocol ran, and invisible
  to every session since because it existed only on local disk. Diagnosis: the §7b rules bind
  the *leg agent*, and a leg agent that dies cannot obey them; nothing bound the orchestrator
  to sweep for orphans. Result: **the unpushed-branch sweep is now a Step 0 action for every
  session, not a post-handoff check** — run it before dispatching, not after, because a
  finished-but-unpushed result changes what the next roster should contain. Leg 266 is now
  pushed, and slot A's leg 300 was cut to verify it before it lands.

- **2026-08-11, cycle 4c — a cherry-pick from the Decision Maker's stale base nearly
  un-landed a correction that had just landed.** The DM agent commits into a local checkout
  sitting on a leg branch and cannot push; the orchestrator cherry-picks each DM commit onto
  `origin/main`. The DM's cycle-4c commit `6ac84b3` was written against a base that predated
  leg 319's landing, and three of its hunks overlapped text leg 319 had just corrected.
  Applying the diff verbatim would have **silently reverted four of leg 319's corrected
  `6.854` surfaces back to the known-wrong `6.855`** — including **leg 305's own title and
  thesis**, while leg 305 was live in slot G working from that spec. Nothing would have
  flagged it: the merge gate does not know which digit is right, and the commit message
  describes only the intended rulings.
  Caught because the resolution was inspected rather than accepted — `git checkout --theirs`
  was the fast path and would have been wrong. All four surfaces were restored by hand and
  verified against `origin/main` before pushing; the two **immutable gate-text sites** were
  confirmed still reading `6.855x` and untouched, per the standing rule.
  **Rule adopted: any DM commit touching `DIRECTION.md` must be diffed against `origin/main`
  for unintended deletions BEFORE it is pushed, never after** — `git diff origin/main --
  DIRECTION.md | grep '^-'` and read every deletion. A stale base plus an overlapping hunk is
  exactly how a landed correction gets un-landed with no one noticing. Related: an earlier
  incident this session where an orchestrator integration commit stacked onto a leg branch,
  same root cause — **the DM and the orchestrator sharing a checkout with the legs.** The
  orchestrator now works in a dedicated detached worktree; the DM still does not.

- **2026-08-11, cycle 4 — two legs stalled by ending their turns to wait.** Legs 292 and 323
  both committed real WIP and then ended their turns *waiting* on long background jobs (a 712s
  test, an arXiv sweep), expecting to be woken. Nothing wakes them. By §7b's iteration-boundary
  rule a leg whose turn has ended is stalled regardless of how much work is committed, and
  from the orchestrator's side it is indistinguishable from a dead agent. **323 was the
  expensive one — all §0c publication drafting is gated on it, and it had silently stopped.**
  Both were resumed with the instruction to **poll from inside the turn** (a bounded
  check-and-sleep loop) and never end a turn to wait. Worth stating in dispatch briefs for any
  leg expected to run something long.

- **2026-08-11, cycles 2–4 — eight independent figure-number collisions in three cycles.** Legs
  choose figure numbers in parallel from a shared list they have no way to lock, so collisions
  are the expected behaviour of the system rather than the fault of any leg. **One of the eight
  was the orchestrator's own error** (leg 316 was told mid-run to take `fig71`, which the
  orchestrator had itself just assigned to leg 303). Resolution rule now applied consistently:
  **first to land keeps the number; a landed artifact beats a reservation held by a parked
  branch** (so leg 302 kept `fig69` over parked leg 301, whose reservation moved to `fig75`).
  Every renumber re-runs the leg's evidence script afterwards so the figure and its checks
  agree. The durable fix is to allocate figure numbers **at dispatch**, from the orchestrator,
  and to state the number in the brief — which is now done, but only from cycle 4 onward.

- **2026-08-11, resume-session cycle 1 — orchestrator force-removed a worktree without
  checking `git status` first, in direct violation of the standing safety rule, and lost
  uncommitted work.** While salvaging leg 221 (BVRR)'s WIP after a second monthly spend-limit
  kill, five stale worktrees were found across three branches of that leg's lineage. The
  orchestrator correctly salvaged and pushed real uncommitted WIP from the first
  `leg/221-bvrr-v1-resume` worktree it inspected (`agent-af848d3928da9762c`, committed at
  `281647e`), then ran `git worktree remove --force` on a **second** worktree on the same
  branch (`agent-a1932a3521e22b4a6`) without checking its status first. That worktree also
  held real uncommitted changes (`experiments/journal/leg_221.md`,
  `writeup/novelty/leg_221.md`, and a new `writeup/data/p2_route_g_v1_g2.json.bvrr_attr_backup`
  file) — content that was never staged, so it was never written to the git object database,
  so it is **not recoverable**: confirmed via `git reflog show leg/221-bvrr-v1-resume` (shows
  only real commits) and `git fsck --no-reflog --unreachable --dangling` (no matching dangling
  blob), and the worktree directory itself no longer exists on disk. Practical impact is likely
  bounded — the sibling worktree's salvaged WIP had overlapping file-level footprint with this
  one and was already pushed — but the loss itself is real and disclosed here rather than
  assumed harmless. **Fix, applied for the rest of this session**: before removing either of
  the two remaining leg-221 worktrees, `git status` was checked first; both turned out to hold
  real uncommitted content and were salvaged via defensive WIP-preservation commits before
  removal (`ea77e0f` on `leg/221-bvrr-v1`, `5cf4dcf` on `leg/221-bvrr-v1-wip2`). **Rule
  restated, this time as a hard precondition, not a preference: `git worktree remove --force`
  is never issued without a `git status --short` on that exact worktree path immediately
  before it, in the same tool call sequence, no exceptions** — "I already checked a sibling
  worktree on the same branch" is not a substitute, since sibling worktrees on the same branch
  can hold independent uncommitted diffs.

- **2026-08-13 (measured by leg 392, incurred by leg 387) — an XML namespace typo made a search
  instrument report a controlled ZERO it had not measured.** arXiv's Atom responses carry the
  opensearch namespace `http://a9.com/-/spec/opensearch/1.1/`. Leg 387's harness listed `1.0`, so
  every response failed its own well-formedness check, every query was discarded, and the leg
  **reported a zero** — an absence of results that was an absence of *parsing*. Nothing caught it:
  a zero is exactly what a clean novelty pass looks like, the harness exited 0, and the negative
  control (which also returned nothing) agreed. Diagnosed only because leg 392 re-queried the same
  endpoint with a parser that **names no version anywhere** and banked the served namespace as a
  field on every record: 32/32 queries MEASURED, `1.1` on all of them. **Result, and it generalises
  past arXiv:** an instrument whose negative branch is a *zero* must bank a positive datum proving
  it reached the service — the served namespace, a version string, a hit count on a control query —
  and a query that fails to reach the service is banked as `THROTTLED`/`FAILED`, **never as a zero**.
  Do not pin a version you do not control; parse namespace-agnostically and record what was served.
  This is the second time a controlled zero has been fabricated by an instrument bug, and the first
  time the fabrication was caught by another leg rather than by the leg that made it.

- **2026-08-14 — the whole of wave 2 was lost to a process exit, and the pre-registration discipline
  is the only reason it cost nothing.** All four wave-2 workers (`T4`, `T6`, `V1`, `T5`) and the
  wave-1 unit `E` stopped without completion records when the host process exited. **Not one had
  reached its gate.** What survived is exactly what had been committed: every one of the five had
  **landed its pre-registration on its own branch before computing** — `9e36e3c` (`T4`), `0ee0b4c`
  and `c113c6a` (`T6`), `fc84241` (`V1`), `7af3f64` (`T5`), `70f3962` and `952b2cf` (`E`). What was
  at risk is exactly what had not: every worktree held uncommitted work — harnesses, sweep scripts,
  re-derivation scripts, and in two cases **partial result JSON**. **Root cause:** briefs required
  committing the pre-registration before the first computation but said nothing about committing
  *during* the run, so each worker held its output in the worktree until it had a complete answer to
  report. A worker optimising for one clean commit at the gate is a worker betting the whole unit on
  surviving to the gate. **Result, and it is a dispatch-brief rule now:** a brief instructs
  **COMMIT EARLY AND OFTEN on the unit's branch** — a partial table with the remainder marked
  not-yet-attempted is a real return; an uncommitted complete one is nothing. Second rule, same
  incident: **poll long jobs from INSIDE the turn** with a bounded check-and-sleep loop; a worker
  that ends its turn waiting to be woken is never woken. **Recovery:** all five were resumed by
  message from their saved transcripts, with context and worktrees intact — gates, territories,
  pre-committed readings and `V1`'s forbidden-read list all restated **unchanged**, since an
  interruption is not a licence to re-scope, and for `V1` specifically not a licence to go looking
  for orientation in a file it was forbidden to read. Re-spawning cold would have been the expensive
  path and would have put fresh, un-pre-registered workers on gates that were already committed.

- **2026-08-14 — the rule adopted from leg 387 caught leg 387's bug in a different leg, in flight.**
  `T6`'s run 1 queried arXiv with `search_query=id:` and got `totalResults=0` for an old-style arXiv
  id. **That is leg 387's exact failure shape**: a clean, controlled, entirely fabricated zero,
  forming again. This time it did not land. It was caught by **endpoint disagreement** — the rule
  that an instrument whose negative branch is a zero must bank a positive datum proving it reached
  the service — fixed to `id_list=`, and a hard `ARTEFACT` rule was added so such a zero can never be
  banked as an absence. The parser names no namespace version. `T6` recorded the repair as `R1`
  rather than hiding it, and committed the failing run. **Result: the leg-387 rule is not
  bookkeeping. It has now paid for itself once, against a different endpoint parameter than the one
  that produced it.** Keep it in every dispatch brief whose negative branch can be a zero.

- **2026-08-14 — a 45-leg-old classification was load-bearing and had never been checked, and its
  disqualifying sentence was in the abstract the whole time.** Leg 348 classified seven papers **at
  abstract level** and declared, in its own words, that a full-text pass could strengthen *or
  undercut* it. That flag sat undischarged while `WALLS.md`'s W2 crack, `CLAY_ROADMAP.md` §7.6, the
  Lane T priority-1 ranking and an escalation packet were all built on top of it. `T4` and `T6`
  independently found the classification wrong. **The apparatus half was not even a full-text
  finding** — `arXiv:1902.00384`'s abstract says *"a Newton-Kantorovich theorem is applied"* on *"a
  Banach space of geometrically decaying Fourier coefficients"*, which is the banned apparatus,
  named in the text leg 348 read. **Result:** when a leg declares its own ceiling, the ceiling is an
  **obligation with a deadline**, not a footnote — and a classification may not become load-bearing
  in `WALLS.md` or a lane ranking until it is discharged. The user's instruction to run `T6` **early,
  precisely because it could undercut the lane**, is the only reason this cost one wave instead of
  another forty-five legs.

- **2026-08-14 — a unit's own checkpoints did not survive the container, and a partial unit's
  artefacts were written for the complete unit.** `E` (the H-hard diagnostic) was killed by the host
  **twice**. After the first kill it added per-attempt checkpoints so a relaunch would skip finished
  attempts — the right fix — and after the second kill **8 of 16 attempts were checkpointed and the
  checkpoints were gone anyway**, because they live in a gitignored working directory and the
  container was replaced. So did U2's gitignored `T = 1e5` DNS archive that diagnostic (3) seeds
  from, which is why finishing the unit now costs ≈3.4 h of DNS before a single attempt runs.
  **Second, separable finding:** `E`'s evidence script and `fig109` were both written to require
  `diagnostic_3`, so on the partial JSON they **fail** (`KeyError`) — a correct unit whose artefacts
  cannot be landed. **Result, two rules worth carrying:** a checkpoint that lives only in a
  gitignored directory is a **within-run** optimisation and not a **cross-container** one, so a unit
  expected to run for hours should bank its partial results the way it banks its final ones; and an
  evidence script should degrade to *"this diagnostic did not return"* rather than raising, so a
  partial unit's landed record can still be executable. Neither rule was applied retroactively by
  the Conductor — **editing another unit's evidence script to make it pass is the move this
  repository refuses**, and the branch was left as the record instead.


## Superseded — wave 7's premise checks, demoted 2026-08-19 under §3j (verbatim)

**Two premise checks I ran before committing the gates, both against the repo.** (1) **`R-bank`'s
premise HOLDS exactly as stated** — the `.gitignore` calls the 1.2 GB `u2_dns_ckpt.npy` *"never
committed"*, and `e_hhard_diagnostic.py` builds each seed as a bit-for-bit re-integration through it,
so no shard can build a seed without it. Sharpened: one field is **4,608 B**, so 160 are **737 KB**,
not ~5 MB — committable by two orders. (2) **`R-prof`'s gate REWORDED BEFORE dispatch, because the
solver is ALREADY FFT-based** — so it is implementation-vs-implementation. Smoke (load 21.5 on 12
cores; absolutes inflated ~2×, ratios not): `fft2` **197 µs at `N = 24` vs 189 µs at `N = 32` — FLAT
across 1.9× the work**, paid **20× per RK4 step**, ~69% of a 4,306 µs step. **OVERHEAD-bound, not
FLOP-bound — a hypothesis with a measurement behind it, not the unit's answer.**

## Superseded — the 2026-08-19 "PRICE, DO NOT QUEUE WITHDRAWN" block, retired verbatim 2026-08-19 under §3j

(All three of its units have now moved: `R-bank` LANDED `8019c35`, `R-prof` LANDED `1f89ceb`, `E-FE` DISPATCHED leg 408. Nothing reworded.)

### 2026-08-19 — USER DIRECTIVE: "PRICE, DO NOT QUEUE" WITHDRAWN. THREE UNITS QUEUED.

**Order fixed: `R-bank` → `E-FE` ‖ `R-prof`** (`WAVE7_PLAN.md` §§A–C, final wording). **§0's
`R4` > `R2` > `R3` ranking STANDS** — additions, not a re-rank; these run first because they are
**cheaper and upstream**, not because they outrank `R4-a`.

**The two premise checks I ran before committing those gates — `R-bank`'s 1.2 GB blocker, and `R-prof`'s gate reworded because the solver is ALREADY FFT-based and overhead-bound — retired verbatim → `## Superseded — wave 7's premise checks`. Live wording: `WAVE7_PLAN.md` §A, §C.**

**Consequence I have to own: my own 90.9 core-hour price is an OUTTURN, not a FLOOR.** It inherits
`95.389 s/epoch`, unprofiled in 403 legs. If `R-prof` finds a factor, that number and every cost
figure in `OPTIONS.md` move together.


## Superseded — wave 7's dispatch block, retired verbatim 2026-08-19 under §3j

(Retired at `R-bank`'s landing: its `E-FE` HOLD is discharged and three of its four units have returned. Nothing reworded.)

### WAVE 7 — DISPATCHED 2026-08-19: `R-bank` ‖ `R-prof` ‖ `L6-b` ‖ **`V-W6`** (legs 404–407)

Plan committed `2a5ea0d` **before** dispatch; gates carried verbatim into self-contained briefs.
**`V-W6` verifies WAVE 6** — I planned wave 6, so I may not, and it is briefed to scrutinise my own
landing audit too. **`E-FE` IS HELD** until `R-bank` returns **160/160** bit-identical: that is
`R-bank`'s own pre-committed reading, not a new decision. Territories disjoint; every brief carries
explicit-paths-only commits (four workers, one tree), COMMIT DURING THE RUN, and its §3d price.


## Superseded — wave 6's close and its §3i re-rank, demoted 2026-08-19 on `L6-b`'s landing (verbatim)

*Discharged: the re-rank it made — Lane L's next unit is `L6-b`, not `L7` — was executed and
`L6-b` landed at `4df0ca0` with gate `NO`. Nothing reworded.*

### WAVE 6 — **COMPLETE 2026-08-19. Three planned, three dispatched, three landed.**

Plan `e202653` before any worker started; `V-W5` `95cf861`, `V5` `dacc01c`, `L6` `e62c449`; **all
three now VERIFIED by `V-W6`.** Detail retired verbatim → `WALLS_HISTORY.md` §ORCH-W6-DISPATCH.

**`L6`'s landing audit and its §3i — retired verbatim 2026-08-19 → `WALLS_HISTORY.md`
§ORCH-W6-L6AUDIT. THREE OF ITS NUMBERS ARE CORRECTED BY `V-W6` at `writeup/CORRECTIONS.md` §38**;
the one-start finding is UPHELD. Full text with the audit: `writeup/waves/WAVE6_CLOSE.md`.

**Wave 6's seven §3i answers retired verbatim 2026-08-19 → `WALLS_HISTORY.md` §ORCH-W6-3i; full
text with its landing audit: `writeup/waves/WAVE6_CLOSE.md`. What binds: no `L1→L4` link moved;
`OPTIONS.md`'s `L7` and `L4` prices made FALSE; Lane L keeps its rank; the loop risk is REAL —
wave 7's Lane-L slot is a measurement on the object, not another audit.**

**RE-RANK MADE HERE (§3i q5): Lane L's next unit is `L6-b`, not `L7`.** `R4` > `R2` > `R3` stands.

---

## Superseded — the "PRICE, DO NOT QUEUE" discharge block

Retired from LIVE 2026-08-19 under §3j when wave 8 was dispatched. VERBATIM.

### 2026-08-19 — "PRICE, DO NOT QUEUE" WITHDRAWN: all three queued units have now moved.

**`R-bank` LANDED `8019c35`, `R-prof` LANDED `1f89ceb`, `E-FE` DISPATCHED leg 408.** The block
that set their order and priced them retired verbatim → `## Superseded — the 2026-08-19 "PRICE,
DO NOT QUEUE WITHDRAWN" block`. **§0's `R4` > `R2` > `R3` ranking STANDS** — those were
additions, not a re-rank. **My 90.9 core-h price was an OUTTURN, not a FLOOR, and `R-prof` has
now measured the factor: 4.34× a named reference, gate (iii) `NO`, and it breaks no wall.**

---

## Superseded — R-bank's return detail

Retired from LIVE 2026-08-19 under §3j when wave 8 was dispatched. VERBATIM.

**RETURNED — `R-bank`** (leg 404, `8019c35`): **`YES` ×3** — 160/160 bit-identical, 16/16 at
`ulp_gap 0`, attempt 15 **12/12 byte-equal with both DNS field artefacts ABSENT**. Seedbank
**TRACKED, 737,408 B**. I recomputed `self_hash`, re-hashed all 160 slices, re-ran `regenerate`
on 4 fields — bitwise. **My own `~1.2 GB` is 268.9 MB**, `U2`'s *rejected* archive size (§39).

---

## Superseded — R-prof's return detail

Retired from LIVE 2026-08-19 under §3j when wave 8 was dispatched. VERBATIM.

**RETURNED — `R-prof`** (leg 405, `1f89ceb`): gate (iii) **NO, 4.34×** the named reference; 79.1%
transforms; remedy priced not landed. Integration audit + §3i seven: `writeup/waves/WAVE7_CLOSE.md`.
Conductor finding: the unit's "every round exceeds 3×" is **cpu-clock-only** (worst wall 1.9975).

---

## Superseded — V-W6's return

Retired from LIVE 2026-08-19 under §3j when wave 8 was dispatched. VERBATIM.

**RETURNED — `V-W6`** (leg 407, `c7f242c`): `V5` and `V-W5` **VERIFIED**, `L6`
**VERIFIED-WITH-QUALIFICATION**, no arithmetic defect anywhere in wave 6, 11 defects open, 0
repaired. My landing audit: one-start finding UPHELD, three numbers overstated, one wrong
conservatively, **two understated** — `CORRECTIONS.md` §38. `D-VW6-7` (undeclared scipy) repaired.

---

## Superseded — wave 7's §3i q5 re-rank

Retired from LIVE 2026-08-19 under §3j at `PB2`'s landing, DISCHARGED. VERBATIM.

**⚠ RE-RANK MADE IN THAT INTEGRATION COMMIT (§3i q5).** Wave 8 opens with **`L-JVER`** — an
independent re-implementation of `W[V]`/`J(c)` in a different basis — because every route-4 residual
number is downstream of one function whose only evidence is a selftest comparing two of `L6`'s own
implementations. **`L8`'s branch rule is deferred VERBATIM to wave 9**, still keyed to `L6-b`.
`WAVE8_PLAN.md` AMENDMENT 1, written **before** dispatch.

## Superseded LIVE block — wave 9 DISPATCHED, demoted 2026-08-19 at the RUN STOP under §3j (verbatim)

**Verbatim. Nothing edited.** Superseded by the RUN STOPPED live block above.

## LIVE — CONDUCTOR mode, **WAVE 8 CLOSED AND INTEGRATED; WAVE 9 DISPATCHED (4 units)**, 2026-08-19

Waves 5, 6 and 7: COMPLETE, VERIFIED, RETIRED VERBATIM BELOW. Wave 8's LIVE block retired verbatim
→ `## Superseded LIVE block — wave 8 IN FLIGHT`. **The 2026-08-19 USER PIVOT TO PAPERS is IN FORCE**
(paper units are ADDITIONAL; §3g's composition floor STANDS; a wave of pure paper units is out of
contract). **A PAPER IS A VIEW OF THE RECORD, NEVER A SOURCE. No unit may cite a draft.**

### WAVE 8 — CLOSED. All four returned; integrated `233a2c3`, `024a9b2`, `c63769b`; audit in `writeup/waves/WAVE8_CLOSE.md`

- **`L-JVER`** (409, `a55ca9b`): gate **`NO`** — and the **largest structural finding in the record**.
  Its independent operator, put on `L6`'s own nodes and weights, reproduces `J_L6` to `1e-14` at all
  four points **including P3 where the gate misses by 43%**. Neither program is miscoded:
  **`J(c) = ∫₀^{T_s}‖W(·,s)‖_{L^{3/2}} ds` IS A LOGARITHMICALLY DIVERGENT INTEGRAL**, at `r→∞`
  (`w_s ~ ∂_s A/r²` survives DSS annihilation) and at `r→0` (`l = 1`). `CORRECTIONS.md` §52.
- **`PB2`** (410, `a7ffa1e`): gate **`YES`**. `W4` clause (b) carried by **Tsai 1998 Thm 2** at FULL
  TEXT (no `L^q`, no Leray–Hopf, no boundary condition); **NRŠ does NOT apply** (`U ∈ L³` exactly,
  and `∫|U|³` is log-divergent at `α = 1`). Clause (b) **STANDS**. Debt: no BLOG/TECHNICAL, no figure.
- **`PB1`** (411, `1b2c0f0`): gate **`YES` — `P1` IS KILLED, and that is a GOOD RESULT.** Both effects
  are in print, one of them twelve years old, and `P1`'s framing word was *silently contradicted by
  its own bibliography*. **This is the pivot's first return and it paid for itself.**
- **`V-W7`** (412, `f3d4e0e`): seven defects against the Conductor's own integration. I re-checked all
  seven at primary: **6 UPHELD, 1 UPHELD IN PART** (`V-W7`'s `2.89873` came from its own re-run and is
  **not in the banked artefact**) → `CORRECTIONS.md` §50.

### THE TWO CORRECTIONS THAT MATTER MORE THAN ANY WAVE-8 GATE

- **§51 — THE UNDER-CLAIM.** `L6`'s four-rung refinement ladder moved `ρ` **−4.994561%**; `L6-b`'s
  single ×25 budget step at FIXED `n_dof` moved it **−6.751678%** — **×1.3518 of the whole ladder**.
  Both numbers correct, both banked, in two units, **and nobody divided one by the other for eleven
  legs.** `J3` needs `7.2153%` to invert and `6.7517%` is measured one rung up: **margin 0.4636 pp.**
  Rule: *when a refinement study and a budget study measure the same objective, DIVIDE ONE BY THE
  OTHER BEFORE REPORTING EITHER.* §45's neighbouring blind spot — **an error shared between two
  artefacts that no single checker reads together** — and there is no count for it.
- **§53 — THE SIGN.** The divergence **reaches the minimiser** (`+6.226e-5`, `+6.246e-5`, `+6.212e-5`
  per decade of `r_max` over `1e6→1e14`; three bands inside 1%). **THE SIGN IS POSITIVE**, which is
  the ONLY reason `L6`'s, `L6-b`'s and `L5`'s `NO`s survive — **their gate answers stand, their
  numbers do not.** §52 does **NOT** subsume §51 (×130 apart). `L5`'s `c_mod = 869.288` **FLAGGED,
  not adjudicated** — its sweep stops ~3 decades short and a log divergence is exactly the
  exponent-zero case a power-law fit calls "saturation". `W4`(b) **NOT affected** (searched `PB2`'s
  artefact for `c_mod`/`869.288`/`J(`/`curl F`/`L1_t`: none present).

### WAVE 9 — DISPATCHED 2026-08-19. Plan committed BEFORE dispatch at `11abd04` (`writeup/waves/WAVE9_PLAN.md`), gates verbatim in the briefs

1. **`L5-cmod`** (413, **Lane L, CONSTRUCTION, opens the wave — §3f rule 3, meets the composition
   floor**). Extends `L5`'s cutoff sweep on its load-bearing row from `ρ≈1.26e3` to `ρ = 1e8`.
   Gate: *is the per-decade increment in `c_mod` approaching a NONZERO CONSTANT — YES or NO?*
   **YES ⟹ `c_mod` is a value of the cutoff, not of the functional, and `L5`'s `NO` is STRENGTHENED.**
   NO ⟹ genuine saturation, `L5` was right, **and that is NOT written as a null result.**
2. **`P4-DRAFT`** (414, PAPER, ADDITIONAL). §51 is its centre of gravity, not an appendix. Honest
   tally **2 prospective against 9 retrospective** goes in the paper in those words.
3. **`P2-DRAFT`** (415, PAPER, ADDITIONAL). **Unblocked because `PB2` cleared `YES`.** Contribution
   capped verbatim by the user at *"the identification of T₃ as the sole survivor and its
   ṁ-proportionality, in float64, on a synthetic profile."* Every `J` printed with its truncation.
4. **`V-W8`** (416, VERIFIER, **dispatched LAST**). **I PLANNED WAVE 8; I MAY NOT VERIFY IT.** Aimed
   at my own work: §53's arithmetic, **§53's SIGN claim** (*a single negative increment at any reach
   reopens `L6`, `L6-b` and `L5` simultaneously — escalate immediately, not at wave end*), §53's ×130,
   §50 item 6, the W7 byte-identity after my misplacement, all nine verbatim retirements, and a
   **mutation test on `test_headroom.py`** because I wrote it.

**`L6-e` v2 — HELD FOR CORES, not descoped.** Gate pre-committed at `CORRECTIONS.md` §53 (matched
truncation: report `ρ(J3@20k)` at `nq_r = 60` **and** at `72`; straddling the threshold means the
ladder is **undecidable at this reach and that is the result**). Held on a MEASUREMENT: load 27 on
12 cores with `E-FE` live. Dispatch on `E-FE`'s return. **This is a scheduling decision, not a
scoping one.**

**`E-FE`** (408) is a **LATE RETURN** and **may not influence wave 8's ranking** (ruling `99421dd`).

### USER DECISIONS OWED — recorded, NOT ruled by me
1. **§49** — does `ORCHESTRATION.md` §6 clause 3 get a recompute-from-primary check beside it?
   `L-JVER`'s suite is the first in the record claimed 12/12 of that class; `V-W8` is checking it.
2. **`PB1`'s F2** — `JOURNAL.md:5305` and `ORCHESTRATION.md` §3k:576 give **contradictory accounts of
   leg 387's arXiv harness**; leg 411 re-measured 10,780 against a recorded 10,756, favouring the
   journal, which puts leg 382's queue on the wrong reading.

### Open escalations — THREE OPEN, NONE RULED BY ME
`ESCALATION_W2_SCOPE_2026-08-18.md` (W2 names 3D SINGULARITY, `arXiv:2509.25116` proves
NONUNIQUENESS; the third reading would make Lane T's re-open condition (i) live);
`ESCALATION_PUB0C_PUBLISHED_2026-08-18.md`; **`T1`'s ban-wording packet**. **A ban is superseded by a
MEASUREMENT, never a decision — a defective ban WORDING is a user escalation, and I may not rule it.**
The **leg-257 lift-clause defect** stays open and EXEMPLAR-FREE.

### Debt carried into wave 9
`PB2`'s BLOG/TECHNICAL pair (~1 h) and registered figure (~15 min); **`R-bank`'s `--verify` CANNOT
FAIL** (0 `raise`/`assert`/`sys.exit` in `verify()`) — remedy owed, an instrument that cannot fail is
not an instrument; the §37 **"assert the NEIGHBOURHOOD, not only the match COUNT"** rule owed to
`CORRECTIONS.md` (my own defect: `§51`/`§52` landed under `## W7` because a search walked past W5 and
W6, neither of which carries a `⚠` block); Lane R queue `L5-nov`, `R4-a` (remedy **NOT** specified as
"Strang" — needs naming before dispatch), `R2`, `R3`.

### Headroom, IN BYTES (`wc -c`), §3j — **no longer measured by hand**
`test_headroom.py` is always-on in `merge_gate.sh` (§48) and **FAILS rather than skips** when it
cannot locate the LIVE block. Caps: `STATE.md` 24,576 **and NO ROW OVER 600 CHARS**; `WALLS.md`
32,768; `OPTIONS.md` 24,576; this LIVE block 8,192. Retirement (verbatim move) is preferred over
compaction; nine blocks were retired verbatim at wave 8's close.

## Superseded — wave 1 dispatch table, retired VERBATIM from the LIVE block 2026-09-10 (leg 431) under §3j

**WAVE 1 — dispatched 2026-09-09, five agents, each in its own git worktree, each writing ONE file
and committing it on its worktree branch (not pushed):**

| slot | unit | brief | writes | status |
|---|---|---|---|---|
| 1 | `R2` shard A | §§1–3 preamble + §4 pp 24–44, 11 + 4 preamble statements | `writeup/data/arc6/ledger/shard_A.json` | **landed** |
| 2 | `R2` shard B | preamble + §5–§6 pp 45–72, 11 + 4 | `…/shard_B.json` | **landed** |
| 3 | `R2` shard C | preamble + §7–§8, App C pp 73–99, 157–164, 19 + 4 | `…/shard_C.json` | **landed** |
| 4 | `R2` shard D | preamble + §9–§10 pp 100–125, 15 + 4 | `…/shard_D.json` | **landed** |
| 5 | `R2` shard E | preamble + App A–B pp 126–156, 19 + 4 | `…/shard_E.json` | **landed** |

## Superseded — gates-answered paragraph, retired VERBATIM from the LIVE block 2026-09-10 (leg 433) under §3j

**Gates answered so far, all `UNVERIFIED`:** `R0` §66/§67 · `R1` `NO-AND-HERE-IS-THE-DIFF` strictly,
`MATCH` after six named rules · `R2` (solo) (a) `YES` 79/79, (b) `YES`, (c) 13 hard-page notes ·
`R3` acyclic `YES`, complete `NO-AND-HERE-ARE-THE-DANGLING-NODES` (Remark B.9; 134 labels in
unnumbered prose; **Propositions 9.5/9.6 never cited by anything downstream**), spine through
§4/§7/§9 **refuted by citation, confirmed by equation**, prereg 4 of 8 (§68).

## Superseded — mode paragraph, retired VERBATIM from the LIVE block 2026-09-10 (leg 435) under §3j

**Mode:** `ORCHESTRATION.md` **§3g CONDUCTOR**, wave sizing **5** by user ruling (recorded in §3g
beside its original reason; `CORRECTIONS.md` §67). The charter arrived while `R3` was mid-flight
under the solo charter; `R0`–`R2` (legs 423–425) were already on `main`. The conductor charter is
applied **forward** (§67): landed units are not redone; `R2` is **re-read by five fresh shards** and
reconciled; `R3` stayed the Conductor's serial unit and has landed (this commit).

## Superseded — K1 phase A paths, retired VERBATIM from the LIVE block 2026-09-10 (leg 437 amendment) under §3j

- **Phase A** resumed the arc-6 tree at `/tmp/claude-0/-home-user-blowup-search/f04cf05e-…/scratchpad/nse`
  (NavierStokes built in leg 435; Euler stopped `[10526/11251]`). Logs: this session's scratchpad
  `k1/k1_A_{build,axioms}.log`, `k1_A_summary.txt`.
