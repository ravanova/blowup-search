# STATE — the compact working surface

**Read this instead of `DIRECTION.md`, which is never read (§3e).** Everything else is archive,
consulted only when a pointer here names it. **Regenerated at every landing**, under `ORCHESTRATION.md`
**§3j**'s caps: this file **≤24 KB, no row over 600 characters**. A row's job is to let you decide
whether to open the journal — not to summarise it. **Numbers are cited by JSON field, not restated.**

**REGENERATED 2026-08-18** at wave 3's integration. Waves 1–3 are compressed to their landed rows.
Gate texts are immutable on `main` and are quoted **by pointer**: wave 1 `a384d92`, wave 2 `c1a8d5e`,
wave 3 `42011ff`.

## Mode

**CONDUCTOR** — one long-lived entity owning direction *and* integration, dispatching waves of 2–4
self-terminating workers. Contract `ORCHESTRATION.md` **§3g**; wall mandate **§3h**; **§3i** the
direction check (seven questions, in every integration commit, per unit); **§3j** headroom.
*(§3f solo and the §§2–5 four-slot contract remain available, unchanged.)*

## Goal, posture, odds

- **Goal:** a full Clay solve (user ruling 2026-08-06). **Arc 7 (ruling 2026-09-10): independently CONFIRM the OpenAI result by running the kernel — see the arc-7 block below.** Prize direction is Fefferman **(C)** —
  breakdown on `ℝ³`. **(D), the torus, is deferred with Lane T** (ruling 2026-08-14).
- **Posture (ruling 2026-08-13):** *the walls are the work.* Seven blockers in **`WALLS.md`**, each
  with evidence separated from assumption and a pre-committed statement of what breaking it consists
  of. **Every lane may build whatever it needs, at any size, without a further ruling.**
- **Ceiling: Tier 2.** Route 4 produces a candidate; no certification route is built.
  `CLAY_OBLIGATIONS.md` §6 names the two obligations with **no known method**.
- **Clay odds ~0.05%**, unmoved. **No `L1 → L4` link has EVER moved, in over 410 legs.** **The cheapest unit that could move one: NO SUCH UNIT IS KNOWN** — `CLAY_OBLIGATIONS.md` §6 names two obligations with **no known method**, every landed unit is Tier 2, and nothing in `OPTIONS.md` is priced to deliver a certified result.

## ⚠⚠ ARC 7 — INDEPENDENT CONFIRMATION, **OPEN 2026-09-10**, §3g CONDUCTOR ×5, legs 436–440. The arc-6 block retired VERBATIM → `WALLS_HISTORY.md` §STATE-ARC6-CLOSED (leg 436).

**Arc 7's goal, in one sentence (user ruling 2026-09-10, item 1):** *independently CONFIRM the OpenAI
Navier–Stokes result — not re-derive it — by running the Lean kernel to completion on its exported
theorems, because out-refereeing 166 pages is beyond this repository and running a kernel is not, and
nobody has published a kernel run.*

**Rulings 2026-09-10 (recorded leg 436, `CORRECTIONS.md` §72):** **(1)** the programme is NOT finished; the
goal is the sentence above. **(2)** finish the Lean kernel check — arc 7's headline, `K1`. **(3)** re-run
wave 4 under adversary-proof gates, `K3`. **(4)** publishing this repository and its writeups is NOT the
outreach hold; the hold stays on CONTACTING authors, groups and lists. **(5)** Lane T re-open:
recommended **N**, AWAITING one-word confirm. **(6)** an unrefereed preprint counts as "published" for
`PUB_0C` §1: recommended **Y**, AWAITING one-word confirm. Nothing in arc 7 depends on 5 or 6.

**Leg numbering:** the charter said *legs run from 435*; leg 435 was spent on the kernel-check addendum
(`leg_431.md` §7) before the charter arrived, so `K0`–`K4` are legs **436–440**. Arc 6's kernel check
(leg 435) reached `#print axioms` on a build that never COMPLETED (Euler 725 jobs short, mathlib from
cache) — one run, one container, `UNVERIFIED`; `K1` owes the completed build and a second run.

| unit | leg | shape | gate, in final wording | status |
|---|---|---|---|---|
| `K0` | 436 | DOCS, serial | rulings 1–4 recorded in ORCHESTRATION / STATE / CORRECTIONS; goal stated where a fresh session reads it; STATE rows retired under §3j before any were added | **LANDED** |
| `K1` | 437 | SERIAL, **no time cap** | (a) does `lake build` complete; (b) `#print axioms` verbatim for `navier_stokes_breakdown_R3` and `_periodic`; (c) `sorryAx` reachable from either — YES/NO; (d) wall time and machine. GREEN = the standard three only → STOP AND REPORT. RED = `sorryAx` or any other axiom → STOP, ESCALATE, NO PUBLICATION, blind reproduction first. Prereg `leg_437_prereg.md`; runner `scripts/arc7_k1_kernel_check.sh`; phase A resumes the arc-6 tree (**GREEN, banked**), phase B is a fresh clone timed end to end — **relocated to a fresh container by user ruling (§73), A's tree kept for `K2`** | **IN FLIGHT** |
| `K2` | 438 | FAN-OUT ×5 | (1) the 5 `PARTIAL` statements — what is missing, per statement; (2) the 4 `sorry` — each a challenge placeholder, none reachable from a main declaration, cross-checked against `K1`'s axiom output, which WINS on disagreement; (3) the Comparator's 4 `NOT-ESTABLISHED` checks — run them; (4) DeepMind byte-identity re-verified at upstream source, independently; (5) ADVERSARIAL VERIFIER, blind, a sample of 1–4. One file per agent, own branch, cherry-picked unedited | planned |
| `K3` | 439 | FAN-OUT ×5, CONSTRUCTION — the composition floor | wave 4 redux on ONE rule: *evidence is a two-route agreement on a quantity the adversary cannot choose* (what leg 432 did and wave 4's gates did not). A gate that cannot be put in two-route form is DROPPED, not weakened. Scales checked against the paper's own asymptotics BEFORE the prereg is pushed (§71). Slot 5 the adversary, blind: a signal it can fake is NOT EVIDENCE whatever the worker's gate said | planned; prereg pushed first |
| `K4` | 440 | SERIAL | `writeup/7_confirmation/`: full §6 quartet plus ONE document written for outsiders. LEAD WITH THE VERDICT, never with the fragments; every damning-sounding finding sits UNDER the verdict it qualifies. States what a green kernel does and does not establish; takes no position on priority | planned |

**Standing for the arc:** Tier 2 is never a proof · no `L1→L4` claim without the link moving · every gate
`UNVERIFIED` unless a blind agent reproduced it (§3f rule 1) · pre-registrations pushed BEFORE the runs
they govern · escalate, never rule (K1's RED branch, any ban lift, any `W4` movement) · hand off per §9d
with `K1`'s build cursor if it is mid-flight.

## THE LANES — **RE-RANKED 2026-08-19 AT THE STOP, on what is measured NOW** (order unchanged; Lane L DEMOTED); re-earned per unit under §3i

Ruling: `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`. Deferred options keep their cost and
re-open conditions in **`OPTIONS.md`** — read it alongside this file when planning. **Nothing is
dropped because a lane was not chosen.**

| lane | attacks | status | one line |
|---|---|---|---|
| **V — VISCOUS RUNG** | W3 | **RANK 1 — BY DEFAULT, NOT BY STRENGTH** | First because the lanes below it are shut or blocked, **not** because its method is measured to work. ACTIVE, un-held 2026-08-18 by USER RULING; `V3` (leg 399) measured leg 174's Grade-A × fluid cell OCCUPIED, its pre-committed reading (a) FIRED and stays honoured, and **RULED (Q1): the prose test governs — W3 STANDS, the premise SURVIVES.** **Still owes the OBLIGATORY unit (Q4), never dispatched.** |
| **L — THE LAST OBLIGATIONS** | W5, §6(i), §6(ii) | **RANK 2 — DEMOTED 2026-08-19 from PRIORITY** | **Both `W4` clauses it can reach are shut BY ITS OWN UNITS** — (a) by `L2′` (leg 397), (b) by `L5` (leg 400) and re-verified by `PB2` (leg 410) on Tsai 1998 Thm 2. What is left in its charter — **W5, §6(i), §6(ii) — is untouched and no-method**. Inside `W4` only clause (c), **which is Lane T's**. **DEMOTED, NOT KILLED.** |
| ↳ *why the demotion is not merely bookkeeping* | — | — | `CORRECTIONS.md` **§52/§53**: `J(c)`, the functional every route-4 residual is scored against, is a **logarithmically divergent integral**. Its gate answers survive **only on the SIGN** of the truncation error — **the numbers do not.** A lane cannot hold PRIORITY on an objective that does not exist as a number. **§54: `§52`/`§53` are now independently reproduced bit-identically, so the demotion rests on a re-run result, not on one run.** |
| **T — TORUS** | W2, **W4(c)**, W6 | **RANK 3 — DEFERRED, and BLOCKED ON A USER RULING, not on work** | Deferred on **the lane's own measurement** (`arXiv:1902.00384` certified by exactly the banned apparatus; both certified rows 2D lifts). **But `W4`'s ONLY surviving clause is (c), and clause (c) IS statement (D), which sits in this deferred lane** — `ESCALATION_D_BUNDLING_2026-08-18.md`, **never ruled**. Alive through `T2″`; `T3` deferred *with* the lane, not killed. `OPTIONS.md` §E. |
| **R — REFORMULATION + SOLVER** | W7 | **continuous — NEVER sets a wave's direction** | Runs inside every unit's pre-registration (*what makes this an order of magnitude cheaper?*) and takes its own units when a wave has room. Every factor removed is permanent. Internal ranking RULED 2026-08-18: **`R4` (validity) > `R2` > `R3`**. |

**LANE T's TWO RE-OPEN CONDITIONS, either sufficient:** **(i)** a **demonstrated, genuinely-3D
closure** in the literature, meeting W2's own pre-committed test with three-dimensionality supplied
**by the certified object itself**; or **(ii)** **`T2″`** returning a rigidity picture favourable to a
**natively-periodic non-DSS** ansatz.

**C1 STANDS, EXEMPLAR-FREE, AND BINDS EVERY UNIT IN EVERY LANE.** It is an **apparatus scoping**: a
Zgliczyński-style Galerkin-plus-tail **dynamical closure** is a different apparatus from a
Newton–Kantorovich radii-polynomial contraction, true independent of any instance. **NO UNIT MAY CITE
C1 AS EVIDENCE THE TECHNOLOGY CLOSES FOR ANY OBJECT CLASS.** **The naming requirement is not waivable
by the Conductor:** a unit claiming the scope must, **in its own pre-registration**, both **(1) name
its apparatus** with a citation and **(2) show it does not construct a single bounded approximate
inverse uniform in `M`**. **Absent both the ban applies in full**, and a unit reaching for a
`Y₀/Z₀/Z₁/Z₂` contraction **in any space** is inside it whatever it calls itself.

**Still in force, untouched by the 2026-08-14 ruling:** **A2** (Cadiot ban stands, lift clause
CLOSED), **B1** (*"which needs L1 first"* struck from stage V's lift clause), and the **narrowed
outreach hold** — **reading any published document is authorised; contacting an author, group,
maintainer or list remains HELD.**

---

## ⚠ W4 — TWO BREAK CLAUSES SHUT, (b) VERIFIED; CLAUSE (c) IS STATEMENT (D), LANE T's, DEFERRED

`L2′` shut (a); `L5` (leg 400) shut (b), re-verified by `PB2` (leg 410) on **Tsai 1998 Thm 2**. Both fail
against **the same pinned `α = 1`** — the first time two independent clauses failed against a property of
**the object**. **NOT a wall movement and NOT a Clay movement.** Full record: **`WALLS.md` §W4**; block
retired verbatim 2026-09-09 → `WALLS_HISTORY.md` §STATE-W4-2026-08-18.

**THE W3 WORDING ESCALATION IS RULED AND OFF THE DESK** — the prose test governs, `W3` STANDS, Lane V's
premise survives, the cell stays OCCUPIED by `arXiv:2509.25116`, and the two are different claims.

## Landed — what the record actually holds

| unit | gate answer | SHA | state |
|---|---|---|---|
| *retired under §3j, STILL UNVERIFIED* | **`D-REPAIR`** (gate `NO` twice, 110 fig ids, `V-W3`'s D3 wrong in sign) `036e56d`; **`V-W3`** (3 of 4 CONFIRMED, 1 REFUTED — `E`'s `8×` overrun was wall-h vs core-h, like for like `E` was 0.4% **UNDER**) `2b8755e`; **`V1`** (all five wave-1 claims reproduce) `2fb399f`. Rows verbatim: `WALLS_HISTORY.md` §STATE-LANDED-UNVERIFIED. | — | **UNVERIFIED** |
| **`PROG-R4`** (route-4 DSS, leg 380) | **U0–U3, U5 LANDED; U4 BLOCKED** — needs a recovered **named** orbit and there is not one. `G1 = UNDER-RESOURCED`, `M2`/`M3 = DELIVERED`. **`E` tightened `G1` without converting it to a `no`** and made **U4/G2 harder to open**. §3d's stop did **not** fire; **route 4 is NOT stopped.** | leg 380 | **UNVERIFIED** |
| *retired under §3j* | **`T4`, `T5`, `T6`, `T1`, `T2`, `R0`, `R1`, `V-W2`, `E`, `L2′`, `V3`, and now `L5` + `V-W4` (`L5` VERIFIED by `V-W5` 2026-08-18) — LANDED and VERIFIED, so they leave this file.** Gate answers in their own words, SHAs and verifiers: `writeup/INDEX.md`, *Retired from `STATE.md`*. | — | **VERIFIED** |
| **`plan_of_record.py` posture** | **Additive only**, 75 insertions / 0 deletions. **No ban lifted, narrowed, reworded or re-read**; `BANNED` byte-identical, `test_plan_of_record.py` **26 bans / 19 in force, ALL GATES PASS**. | `1ca9e91` | — |

## WAVES 3 AND 4 — CLOSED. Detail retired 2026-08-18/19 under §3j → `WALLS_HISTORY.md` §STATE-WAVE34.

The rule it produced is live in
**Standing discipline** below: COMMIT DURING THE RUN, NOT ONLY AT THE GATE.

## WAVE 5 — COMPLETE, LANDED, **VERIFIED** by `V-W5`. Retired 2026-08-19 → `WALLS_HISTORY.md` §STATE-WAVE5.

**Precedent, still binding:** a request to change a gate **mid-wave was REFUSED** — `WALLS_HISTORY.md` §STATE-WAVE5-PRECEDENT.

## ⚠ 2026-08-19 — TEMPORARY PIVOT TO PAPERS (user ruling). Block retired VERBATIM 2026-09-10 (leg 436) under §3j → `WALLS_HISTORY.md` §STATE-PIVOT-2026-08-19. Still binding: a paper is a VIEW of the record, never a source; no unit may cite a draft; §3g's composition floor stands; outreach stays held.

## WAVE 8 — **CLOSED AND INTEGRATED 2026-08-19** (legs 409–412). Detail retired verbatim → `WALLS_HISTORY.md` §STATE-WAVE8.

`L-JVER` **`NO`** (`J` is a DIVERGENT integral — `CORRECTIONS.md` §52) ‖ `PB2` **`YES`** (`W4`(b) carried by Tsai 1998 Thm 2; NRŠ does NOT apply) ‖ `PB1` **`YES` — `P1` IS KILLED, and that is a GOOD RESULT** ‖ `V-W7` (seven defects against my integration; I re-checked all seven at primary: **6 UPHELD, 1 UPHELD IN PART** → §50).

**The two items that outrank every wave-8 gate: `CORRECTIONS.md` §51 (the under-claim — a refinement ladder and a budget step measuring the same objective, never divided, for eleven legs) and §53 (THE SIGN IS POSITIVE, which is the only reason three `NO`s survive).** §54 reproduces §52/§53 bit-identically on a 2.51× slower box.

## WAVES 6, 7, 9 — CLOSED. Blocks retired VERBATIM 2026-09-09 → `WALLS_HISTORY.md` §STATE-WAVE9, §STATE-WAVE7-EFE, §STATE-WAVE6-V5.

Live residue, one line each: **`L5-cmod`'s literal rule returned `UNDER-RESOURCED`** and its own evidence
check `E5` **FAILED** (§58's *CONTROLLED* withdrawn; `c_mod` defensible to `869.288`) · **`E-FE` (leg 408)
LANDED `1f27071`, `ANY_ROW_RECOVERS_IN_ANY_DRAW = NO`, 0/160, pooled CP-95 upper `0.02279`, gate NOT moved**
· **`V5` (leg 402) both clauses `YES`, VERIFIED by `V-W6`** · `L6-e` v2 priced in `OPTIONS.md`, never dispatched.

## Open — needs the user, not a task

0. **⚠ NEW, RAISED BY `V-W4` AND NOT RULED HERE — is an UNREFEREED PREPRINT a "published work"
   for leg 174's census?** `arXiv:2509.25116`, the paper now occupying the Grade-A × fluid cell,
   **carries no journal-ref**; `PUB_0C_CENSUS_SPINE.md` §1 speaks of *"any **published** work."*
   **A defective criterion WORDING is a user escalation and the Conductor has not ruled it**
   (§3h rule 1: a ban or criterion is superseded by a **measurement**, never by a decision).
   **Nothing is stopped:** the ruling of 2026-08-18 (Q1) already makes **W3 stand on the prose test
   whatever the answer**, and wave 6's obligatory audit (Q4) proceeds either way — but if the answer
   is *no*, the **cell-occupancy fact** changes status, not the wall. Packet:
   `writeup/escalations/ESCALATION_PUB0C_PUBLISHED_2026-08-18.md`.

1. **`PROG-R4` — A, B and D are RETIRED, not deferred** (all buy supply, a standing prohibition):
   `WALLS_HISTORY.md` §OPTIONS-A2. **C** stays unqueued, own milestone, aimed at `|s| > 0.9`.
   **QUEUED 2026-08-19 by user directive, order fixed:** `R-bank` (bank the 160 seed fields, **737
   KB**, kills the 3.4 h-per-shard DNS) → **`E-FE` the field ensemble** (160 attempts, **90.9
   core-h, ~11.4 h wall**, closes `E-iv`) ‖ `R-prof` (**profile the inner loop — never once done in
   403 legs**). Gates in final wording: `writeup/waves/WAVE7_PLAN.md` §§A–C.
2. **Two ban-wording defects RECORDED AND NOT RULED**, because nothing currently depends on them: the
   ℓ¹-Fourier ban's lift clause still names a *"FOURTH space/basis"*, the wrong kind of object for a
   candidate that is an **apparatus** (`T5` measured that it is exactly what blocks leg 257); stage
   V's lift clause is clean after B1. **Neither is escalated** — an entity that both raises and rules
   an escalation has defeated the mechanism, and there is nothing to rule until a unit is blocked.
3. **Statement (D)'s data conditions (8) and (9) are UNREAD** and readable since the outreach
   narrowing. **Parked with Lane T.** Until read, `CLAY_OBLIGATIONS.md`'s *"(D) carries no decay
   condition"* stays narrowed to (D)'s **solution** conditions, and leg 390 §5 item 1's `check_A`
   re-run stays owed.
4. **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate theorems
   read at full text and neither reaches the screened object.

**Conductor-owned debts — ALL FOUR DISCHARGED by `D-REPAIR` (`036e56d`)**, after `V-W3` returned
and not before, because `fig107`'s registration gap *was* `V-W3`'s gate item (4) and fixing it early
would have destroyed the measurement. **A NEW ONE IS OPEN IN ITS PLACE, and it is a unit, not a
passing fix:** `fig81_route_egmf_v1_evidence.py` is tracked and unregistered — the same defect at a
different figure — and **52 cited figures have a `.png` a reader is shown and no rebuild path at
all** (`writeup/check_figure_coverage.py`, executable, currently exits 1).

**RULED 2026-08-18 AND OFF THE DESK — the W3 wording escalation, all three questions plus two
consequential items:** `writeup/escalations/RULING_W3_WORDING_2026-08-18.md`. **(Q1)** W3's **prose
test governs**; the wall **STANDS** and Lane V's premise **survives**; the cell-occupancy fact is
recorded **beside** the wall, not as a break of it. **(Q2)** W3 **retitled** to *No certified blow-up
exists for any fluid equation*, the old title struck not deleted, with the required paragraph beside
it. **(Q3)** leg 174's banked `the_empty_cell.meaning` is **NOT edited** — a correction record
instead, and the refusal to rewrite a banked datum is now the **standing rule**. **(Q4)** the
adversarial full-text audit of `2509.25116` is **OBLIGATORY IN WAVE 6**, ≈4–8 h, scope set by the
ruling, and it must answer as a **separate clause** whether the certified profile is genuinely 3D —
which bears on **W2**, whose own pre-committed test is the arbiter. **(Q5)** Lane L's next unit is
**W4 clause (b)** — already in flight as `L5`, planned at `1e49a00` before the ruling existed; the
ruling adds that `L5` must state **what distinguishes a genuine natively-finite-energy ansatz from
the same trap wearing a different hat.** **Nothing in the ruling moved an L1→L4 link** — it moved
wording and a queue, and it says so itself.

**DISCHARGED and off the desk:** the C1-exemplar escalation (`RULING_C1_EXEMPLAR_2026-08-14.md`) and
all four 2026-08-13 ban-wording items (`RULING_BAN_WORDING_2026-08-13.md`).

## Live bans — 19 in force of 26 recorded, one line each

Full text and lift conditions: `.venv/bin/python plan_of_record.py`. **Run it when a task could touch
one**; do not paraphrase from here. **§3h rule 1: a ban is superseded by a measurement, never by a
decision** — and a defective ban *wording* is a **user escalation**.

gCLM measurement · DSS cheap entrance (bifurcation off a fixed point) · DSS expensive entrance
(**SCOPED 2026-08-11: a *seeded* search is outside it; name the seed or the ban applies**) · 2D β
re-measurement · scaling-gauge near-null · GA compute on unvalidated fitness · "closure is a property
of the space" · stage V as posed · ℓ¹-Fourier/radii-polynomial on any model (**SCOPED 2026-08-13 by
C1 to an APPARATUS; C1 stands EXEMPLAR-FREE and is NOT evidence any apparatus closes; the naming
requirement binds every unit**) · V-rigorous's L1 prerequisite (superseded) · closing the truncation
gap by extending the domain · three readings of legs 51/53 · `Z₁` block-coupling by tuning · weight
exponent toward leg 51's minimum · leg 51's finding at full strength · leg 51's zero `Y₀` as progress
· Chen–Hou 2D as a target · leg 44's 2D near-null · building a solver without grepping
`capabilities.py`.

## Standing discipline — non-negotiable in every mode

Three-tier win condition (**Tier 2 is never a proof**) · pre-committed gates on every claim · novelty
pass before construction (once per programme, §3c) · **lesson 91**: a negative names its
realization/trial-space/basis · **§3d**: a stop fires only on a null from an attempt resourced at the
scale the question is posed at — an under-resourced null returns a **cost** and answers
`UNDER-RESOURCED` · planted controls that can fire **both** ways · **lesson 68**: checks are
executable or they decay · `scripts/merge_gate.sh origin/main` must PASS on everything that lands ·
**reading published material is authorised; CONTACTING an author, group, maintainer or list is HELD**
· no output described as movement toward Clay unless a link actually moved · **§3h rule 2: scale is
not evidence** · **a retraction is not progress and is never described as it.**

**WAVE COMPOSITION FLOOR (§3g).** Every wave carries at least one unit attacking a wall on the Clay
chain **directly** — Lane T, V or L. Lane R work is real and often the most productive thing here,
which is exactly why the floor exists: a programme can spend a year getting very good at finding
orbits it was never going to certify. **A wave of pure Lane R units is out of contract**, and so is a
wave whose only non-Lane-R unit is an audit.

**VERIFICATION IS A FRESH SESSION OR IT IS NOT VERIFICATION**, and **a Conductor may not verify a
wave a Conductor planned.** Every wave budgets one verifier, dispatched in the *following* wave.
**Wave 4 carries the verifier for `E` and for `V-W2`.**

## Where the detail lives — consult by pointer, never wholesale

| Need | Read |
|---|---|
| **The blockers and the lanes** | **`WALLS.md`** — 7 walls, 4 lanes, read whole |
| **Deferred options, costs, re-open conditions** | **`OPTIONS.md`** — read when planning a wave |
| The contract | `ORCHESTRATION.md` §3c–§3k (**3g** CONDUCTOR, **3h** walls, **3i** direction, **3j** headroom, **3k** literature) |
| Bans, stage, gate, lanes | `.venv/bin/python plan_of_record.py` — executable |
| Does a module exist | `.venv/bin/python capabilities.py <term>` — grep, don't read |
| The 2026-08-14 lane ruling | `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md` |
| The 2026-08-13 ban rulings | `writeup/escalations/RULING_BAN_WORDING_2026-08-13.md` |
| What a Tier-2 candidate owes | `CLAY_OBLIGATIONS.md` — §6 is the two no-method obligations |
| Wave gates, verbatim and immutable | git `a384d92` (w1), `c1a8d5e` (w2), `42011ff` (w3) |
| `E`'s four pre-committed branches | `experiments/journal/prog_r4_e.md` §3 |
| Per-leg record | `experiments/journal/leg_N.md`, `writeup/novelty/leg_N.md` |
| Live wave state, escalations, headroom | `reports/ORCH_STATE.md` — LIVE block |
| **Sources + the DEPTH each was read at** | **`writeup/SOURCES.md`** — §3k register; no load-bearing claim may rest on an `ABSTRACT` |
| **Banked numbers** | **`writeup/data/*.json` — re-derive from these, never from prose** |
| A task's own spec | `DIRECTION.md`, that entry only — **never read whole** |
