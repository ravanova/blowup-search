# STATE — the compact working surface

**This file is the read surface for ALL modes.** Read it first and read it instead of
`DIRECTION.md`. Everything else is archive, consulted only when a pointer here names it.

**Why it exists.** `DIRECTION.md` is 23,699 lines / 1.5 MB (~380k tokens). With the other
mandatory reads the per-agent load is ~480k tokens — paid by *every* agent in orchestrated
mode, and on *every task* in solo mode. That cost is pure overhead: a task needs its own
entry, the live bans, and what landed recently, not the accumulated cycle history.

**Regenerate at every landing.** Stale state is worse than no state — this file is only
trustworthy if it is rewritten as part of finishing a task, the way `JOURNAL.md` pointers are.

**REGENERATED 2026-08-14** with the wave-3 plan, after the user's ruling on
`ESCALATION_C1_EXEMPLAR_2026-08-14.md`. Waves 1 and 2 are compressed to their landed rows; their
full gate texts and pre-committed readings are in the git history at `a384d92` and `c1a8d5e`, and
abbreviated in `reports/ORCH_STATE.md`.

---

## Mode

**CONDUCTOR** — one long-lived entity owning both direction and integration, dispatching waves
of 2–4 self-terminating workers. See `ORCHESTRATION.md` **§3g** for the contract and **§3h** for
what a wall-breaking mandate does and does not license.

*(§3f SOLO and the four-slot contract of §§2–5 both remain available and are unchanged.)*

## Goal, posture, odds

- **Goal:** a full Clay solve (user ruling 2026-08-06). Prize direction is Fefferman
  statement **(C)** — breakdown on `ℝ³`. **Statement (D), the torus, is deferred with Lane T
  (user ruling 2026-08-14)** and returns to being an open option rather than an active attack.
- **Posture (user ruling 2026-08-13, unchanged):** *the walls are the work.* Seven blockers are
  enumerated in **`WALLS.md`**, each with its evidence separated from its assumption and each with
  a pre-committed statement of what breaking it consists of. **Every lane is authorised to build
  whatever it needs, at any size, without a further ruling.**
- **Ceiling right now: Tier 2.** Route 4 produces a candidate; no certification route is
  built. `CLAY_OBLIGATIONS.md` §6 names the two obligations with **no known method**.
- **Clay odds ~0.05%**, unmoved. No `L1 → L4` link has ever moved. This line stays in the same
  section as the ambition, under a ruling that raises it — not in spite of that ruling.

## THE LANES — RE-RANKED 2026-08-14 BY USER RULING. Read `WALLS.md` before working in any of them.

**The ruling is authoritative at `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`; the
escalation it discharges is `ESCALATION_C1_EXEMPLAR_2026-08-14.md`.** Deferred options keep their
cost and their re-open conditions in **`OPTIONS.md`** — read that file alongside this one when
planning a wave. **Nothing is dropped because a lane was not chosen.**

| lane | attacks | status 2026-08-14 | one line |
|---|---|---|---|
| **V — VISCOUS RUNG** | W3 | **PRIORITY, ACTIVE** | **It decides whether any path exists.** W3 is the rung that settles whether **Tier 3 is reachable in principle**: if a viscous blow-up cannot be certified for a dissipative fluid equation in **one** dimension, 3D Navier–Stokes is not a question of compute and the honest ceiling of the whole programme is Tier 2. Leg 174's cell is empty **"for want of a target, not a method"**, so supplying the named target is the lane's first job. Both branches valuable — that is what makes it cheap. |
| **L — THE LAST OBLIGATIONS** | W4, **W5**, `CLAY_OBLIGATIONS` **§6(i)** and **§6(ii)** | **PRIORITY, ACTIVE** | **It is on every path.** Leg 390 measured that the torus does **not** retire §6(i)/(ii), so the two no-method obligations are the last blockers on **every** branch — and **no unit in 395 legs has ever attacked either.** Leg 381 banked the bill on §6(i): critical `L³` tail **326.875 per decade**, required `α > 1.5` against available `α = 1.0`. **A deficit of 0.5 in a decay exponent is a number, not an impossibility.** |
| **T — TORUS** | W2, W4, W6 | **DEFERRED** | Demoted from priority 1 on **the lane's own measurement**: `arXiv:1902.00384`, recorded as the crack in W2, is certified by **exactly the banned apparatus** and **both certified rows are 2D lifts** (leg 393 from the data package; leg 394 independently from the prose). **Not killed, and nothing measured is superseded** — the domain-shape obstruction is still not refuted, Theorem NGX and leg 341 stand, and **W2 stands strengthened.** Kept alive only through **`T2″`**; **`T3` is deferred WITH the lane, not killed.** Cost of deferring and both re-open conditions: `OPTIONS.md` §E. |
| **R — REFORMULATION + SOLVER COMPETITIVENESS** | W7 | **continuous, unchanged** | Runs inside **every** unit's pre-registration (*what makes this answerable an order of magnitude cheaper?*) and takes its own units when a wave has room. Every factor removed is permanent. |

**LANE T's TWO RE-OPEN CONDITIONS, either sufficient:** **(i)** a **demonstrated, genuinely-3D
closure** appearing in the literature — a certificate meeting **W2's own pre-committed test**, its
three-dimensionality supplied **by the certified object itself**; or **(ii)** **`T2″`** returning a
rigidity picture favourable to a **natively-periodic non-DSS** ansatz.

**C1 STANDS, EXEMPLAR-FREE, AND THIS BINDS EVERY UNIT IN EVERY LANE.** It is an **apparatus
scoping**: a Zgliczyński-style Galerkin-plus-tail **dynamical closure** is a different apparatus
from a Newton–Kantorovich radii-polynomial contraction, and that proposition is true independent of
any instance in the literature. **The scope no longer carries any implied *"and this has been
demonstrated"* — NO UNIT MAY CITE C1 AS EVIDENCE THE TECHNOLOGY CLOSES FOR ANY OBJECT CLASS.**
**The naming requirement is unchanged and is not waivable by the Conductor:** any unit claiming the
scope must, **in its own pre-registration**, both **(1) name its apparatus** with a citation and
**(2) show it does not construct a single bounded approximate inverse uniform in `M`**. **Absent
both, the ban applies in full**, and a unit reaching for a `Y₀/Z₀/Z₁/Z₂` contraction **in any
space** is inside the ban whatever it calls itself.

**Still in force from 2026-08-13, untouched by the 2026-08-14 ruling:** **A2** (the Cadiot ban
stands, lift clause CLOSED), **B1** (*"which needs L1 first"* struck from stage V's lift clause),
and the **narrowed outreach hold** — **reading any published document is authorised; contacting an
author, group, maintainer or list remains HELD.**

## In flight

| What | State |
|---|---|
| **WAVE 3** (`V2`, `L2`, `L3′`, `V-W2`) | **PLANNED AND COMMITTED 2026-08-14, BEFORE DISPATCH** (`42011ff`), per §3g step 1; all four dispatched after the plan was pushed. **`V-W2` HAS RETURNED, BEEN AUDITED AND LANDED; `V2`, `L2` and `L3′` ARE LIVE.** Gates in final wording and pre-committed readings are below. **Composition floor met TWICE OVER** — `V2` attacks W3 and `L2` attacks W4/§6(i), both on the Clay chain directly. **§3f rule 3 satisfied:** `V2` is construction and was dispatched first. **WAVE 3's OWN UNITS LAND `UNVERIFIED` AND WAVE 4 MUST CARRY THEIR VERIFIER.** |
| **`V-W2`** (verification) | **LANDED 2026-08-14**, audited against the gate committed at `42011ff` **before it existed**. **ALL FOUR ITEMS REPRODUCE**, and items (1)–(2) are **measurements, not transcription checks**: `Papers/` is untracked and was empty, so the unit **re-fetched all three primary artefacts and every SHA-256 matched the banked digest exactly**, then re-derived from them. `T4`'s 2D lift reproduces **bit-for-bit** on every field; `T4`'s first conjunct reproduces from the paper's own (4.33)/(4.34) with the smallest non-zero deviation at **`5.618065e-15`** and `δ = 5.2748360312e-06`; term counts **7/4/5/2** recounted, all six closure terms **0**, Zgliczyński once as **[48]**; `T6` **7/7, 2 UNDERCUT / 4 / 1, 0 `UNREACHABLE`, 0 `THROTTLED`** recounted with `Counter` rather than read off the banked totals; `T5` **1428 files / 417,476 lines**, `DIRECTION.md` absent **and the exclusion asserted executably**, **7 refusals APPARATUS 5 / REALIZATION 2**, **exactly 2** re-openable, leg 257 not. Evidence **100/100, exit 0** (2 skipped, each reporting the banked SHA-256 rather than passing silently). **THE ONE NUANCE, BANKED UNRECONCILED AND RULED BY THE CONDUCTOR AT LANDING — AGAINST THE CONDUCTOR'S OWN WORDING:** the gate said `arXiv:2409.09234` *"carries no-slip walls, not periodicity, **so** the census over-counts by one."* **The record's own ground is different and primary:** *"THIS PAPER CLOSES NO TAIL-DOMINATION ESTIMATE AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL"*; the wall point is `T6`'s **`u_code` U1, secondary**. Both reproduce; **the `so` was the Conductor's.** Verified independently by the Conductor against `p2_route_t6_v1.json` at landing. **The count is unchanged — 6 − 1 = 5** — and `WALLS.md` is corrected to lead with the primary ground. Also measured: the paper **never uses the phrase "no-slip"** (0 occurrences); it states a **moving-wall Dirichlet condition** with *"periodicity … to the rest of boundaries"*. **`T1`'s OWED MACHINE RECORD IS DISCHARGED** — 31/31, exit 0, mutation-tested three ways by the unit and **once more independently by the Conductor** (`questions_ruled` 0 → 3 ⇒ exit 1, restored ⇒ exit 0, file bit-identical). **Two of its own errors self-reported and recorded**, including a wrong pre-registered radii formula that would have banked a **70% false discrepancy** had it not been fixed against the paper. Forbidden-read list **honoured**. |
| **`E` / PROG-R4 unit E** (Lane R, wave 1) | **DID NOT RETURN. GATE UNANSWERED.** Branch `prog-r4/e-hhard` on `origin`, tip **`6a706f7`**, **not merged to `main`** and deliberately so. **Diagnostics (1) and (2) RETURNED, with planted controls firing BOTH ways** — (1) `PULL_TO_LOW_S` (median drift −0.03202, 21 of 23 convergences below `|s| = 0.15`, sign test `p = 0.0347`, secondary all-200 reading `NO_PULL` reported as the honest counterweight); (2) `MIXED` (2,131 constrained / 64 unconstrained accepted epochs, permutation `p = 0.9317`, so the rates are **statistically indistinguishable** and the unit does **not** get to say the minimisation is dragging the solve). **DIAGNOSTIC (3) NEVER RAN TO COMPLETION** — the host killed it twice, 8 of 16 attempts were written to per-attempt checkpoints, and **the checkpoints and U2's gitignored DNS archive are both gone with the container.** **NO BRANCH OF THE PRE-COMMITTED READING FIRED**: `E-i`…`E-iv` are all about diagnostic (3)'s outcome, so **none is claimed**, and the H-hard question is exactly where wave 1 found it. Its evidence script and `fig109` were written for the complete unit and **fail on the partial JSON** (`KeyError: 'diagnostic_3'`) — which is why nothing is landed on `main`. **Cost to finish, from the record's own banked rates:** regenerate U2's `T = 1e5` DNS ≈**3.4 h**, then 16 attempts at up to the 52-epoch cap ≈**1.4 h each serial**, ≈**2.7 h wall at 8 workers** — call it **≈6–7 h wall**, and it buys the single sharpest test of H-hard available. **Not re-dispatched this wave** (the wave is full and its composition is ruled), and it does **not** change wave 3's composition. |
| **`T4` / leg 393** (Lane T) | **LANDED 2026-08-14** (`2c87244`), **GATE = `STOP`, pre-committed branch (c)**. `arXiv:1902.00384` is certified by **exactly the banned apparatus** (Newton–Kantorovich radii-polynomial in weighted `ℓ¹_η`, on **one bounded approximate inverse** `A : X_{−2,−1} → X`) — stated in the **abstract** leg 348 read. **Both certified rows are 2D LIFTS**: `N_x3 = 0` in Table 1 and `Nrec`, decoded arrays of extent 1 in `x₃`, `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` exactly while `max|ω⁽³⁾| = 1.6351 / 1.5274`, `setup = '2D'`; the authors' reason is that a 3D solution's memory cost is *"for now, prohibitive."* The gate's **first** conjunct was met on both rows (criterion (4.32); `r_min`/`r_max` deviations to `5.6e-15`; both `r_sol^Ω` exact; norm check `δ = 5.3e-06` vs `1e-3`) by arithmetic on published constants — **no operator, no `Y₀/Z₀/Z₁/Z₂`**. `C−` could have fired and did not: all six closure terms **0**, Zgliczyński only as bibliography [48]. **W2 STANDS, STRENGTHENED. W6 UNTOUCHED.** Evidence 68/68, exit 0. **VERIFIED 2026-08-14 by `V-W2`** — items (1) and (2), re-derived from a re-fetched artefact whose SHA-256 matches the banked digest. |
| **`T6` / leg 394** (Lane T) | **LANDED 2026-08-14** (`e7db624`), **GATE ANSWERED: 7/7 full texts — 2 UNDERCUT / 4 strengthen / 1 confirm, 0 `UNREACHABLE`, 0 `THROTTLED`, 0 zeros banked.** **UNDERCUT 1 = the independent replication of `T4`**, reached by reading the authors' **prose** where `T4` reproduced from their **data package**, and never told what `T4` found: *"the solutions we present in Theorem 1.1 below are two-dimensional (in space) time-periodic solutions"* … *"they are independent of `x₃` and the third component of the velocity vanishes"* (§1, p.3) — **verified by the Conductor against the PDF in BOTH workers' separately fetched copies.** **UNDERCUT 2:** `arXiv:2409.09234` does not belong in leg 348's `domain_census` — 1-D map fitted to DNS data, **no-slip walls, not periodicity** — so **the census OVER-COUNTS BY ONE and leg 390's "6 compact/periodic" inherits it.** **The obstruction leg 348 named is NOT refuted**; its evidence base is **thinner than the record said, not wrong.** Evidence 77/77, exit 0. **VERIFIED 2026-08-14 by `V-W2`** on every count; the one nuance is in the *ground* the Conductor's wording gave for UNDERCUT 2, not in `T6`. |
| **`T5` / leg 395** (Lane T) | **LANDED 2026-08-14** (`a6f0c38`), **GATE = PASS.** An **obligation** discharged. Corpus 1428 tracked `*.md`+`*.py`, 417,476 lines, `DIRECTION.md` excluded by name **with the exclusion asserted executably**. **7 refusals: APPARATUS 5 / REALIZATION 2.** **Re-openable under C1 — 2, UNRANKED:** leg 348's Galerkin-plus-tail build, and **leg 315's `O1`** sonic-point-desingularized **Taylor-model flow-map** enclosure, which *"needs **no function space**"* — **the genuinely new item, and it points at LANE V.** **Leg 257 is NOT re-openable**: its apparatus **is** the Corollary-21 radii polynomial in a **fourth space**, and a fourth SPACE is not a fourth APPARATUS. Mutation-tested by the Conductor (corrupt the anchor → exit 1). Evidence exit 0, four controls PASS. **VERIFIED 2026-08-14 by `V-W2`**, corpus re-enumerated independently with `git ls-tree`. |
| **`V1`** (verification, wave 1) | **LANDED 2026-08-14** (`2fb399f`). **All five wave-1 claims reproduce** from banked JSON and landed evidence scripts alone. **`M3 = DELIVERED` SURVIVES** U5's 57% seed overlap on M3's own pre-committed wording. **Two defects banked, not reconciled:** `T1` banked **NO machine record** (now owed, folded into `V-W2`), and the gate's own comparand was the Conductor's ambiguous wording. Evidence 38/38, exit 0. |
| **`T1` / leg 391, `T2` / leg 392, `R0`+`R1`** (wave 1) | **LANDED 2026-08-13 and VERIFIED by `V1`.** `T1` gate `yes` — the escalation packet, ruling none of its three questions; **its ruling landed 2026-08-13** (`RULING_BAN_WORDING_2026-08-13.md`). `T2` returned **`UNDER-RESOURCED`, not `no`** — no periodic analogue of NRS/Tsai located, **and that is NOT a clearance**; it named **`T2″`**, the Type-I rigidity question on `T³`, which now keeps Lane T alive. `R0` landed the metric and **retracted "Lane R's first measured win"**; `R1` **closed against itself** (+0.45 pp headroom; spend no more compute on that family). |
| **`PROG-R4`** (route-4 DSS programme, leg 380) | **U0–U3, U5 LANDED. U4 BLOCKED** — it needs a recovered **named** orbit and there is not one. `G1` stays **`UNDER-RESOURCED`**; §3d's stop did **not** fire and **route 4 is NOT stopped.** U5's pre-committed reading fired on branch **(b)**: the bias is in **BASIN STRUCTURE**, not only seed supply. **U2, U3, U5 remain `UNVERIFIED`** — `V1` checked `R0`'s *reading* of them, not the runs. |

---

# WAVE 3 — PLANNED AND COMMITTED 2026-08-14, BEFORE DISPATCH

**Ranked after the user's ruling of 2026-08-14 and against `OPTIONS.md`, which §3g requires be read
alongside this file when planning every wave.** The ruling is the reason the ranking changed:
**Lane T is deferred, and the priority lanes are V and L.**

**Composition floor (§3g, per-wave): MET TWICE OVER.** `V2` attacks **W3** and `L2` attacks
**W4 / `CLAY_OBLIGATIONS` §6(i)**, both walls on the Clay chain, both directly. `L3′` is a
literature unit in the same lane; `V-W2` is verification and counts toward no floor.

**§3f rule 3 is satisfied and was checked before dispatch:** wave 2's last unit was construction
(`T4`) and this wave opens with construction (`V2`), which is dispatched first and is the wave's
centre of gravity. No two instrument/audit/repair units are queued back to back.

**`V-W2` IS OBLIGATORY.** §3g forbids a Conductor verifying a wave a Conductor planned, *with more
force rather than less because it has more context to be biased by.* `T4`, `T6` and `T5` are
`UNVERIFIED` and this Conductor planned all three.

> ### ⚠ WRITTEN INTO THE PLAN SO IT CANNOT BE FORGOTTEN
> **WAVE 3's OWN UNITS — `V2`, `L2` and `L3′` — LAND `UNVERIFIED`, AND WAVE 4 MUST CARRY THEIR
> VERIFIER.** This Conductor planned them and may not check them. A wave-4 plan without that unit
> is out of contract.

**C1's naming requirement binds `V2` and is not waivable by the Conductor.** And **C1 may not be
cited by any unit as evidence that any apparatus closes for any object class** — the scope ruling
says the ban does not *reach* a dynamical closure, never that one has *worked*.

**Every gate below is in FINAL WORDING and every unit carries a PRE-COMMITTED READING**, fixed here
before any worker is dispatched and before any number exists.

---

### 1. `V2` — NAME LANE V's TARGET, AND OPEN THE APPARATUS FEASIBILITY. *Lane V, CONSTRUCTION. leg 396. The wave's centre of gravity.*

Leg 174's Grade-A × fluid cell is empty **"for want of a target, not a method"**, and **supplying
the named target is the lane's first job.** Two record items point here and neither was found by
looking for it: **`T5`'s `O1`** — leg 315's sonic-point-desingularized **Taylor-model flow-map
enclosure**, which *"needs **no function space**"* and is the genuinely new thing C1 bought — and
the **Galerkin-plus-tail dynamical closure** itself. **Both are now outside the bans**, subject in
full to C1's naming requirement.

> **GATE (final wording).** Does the unit deliver **both**:
> **(A) a NAMED TARGET** — a specific **dissipative fluid** model in the lowest dimension admitting
> genuine fluid structure (1D unless the unit states why 1D cannot carry it), with **the dissipative
> term inside the equation that would be certified**, together with the named blow-up ansatz /
> object class and what a certificate for it would assert; **and**
> **(B) a FEASIBILITY VERDICT** on attacking that target with a **C1-compliant apparatus** — the
> Galerkin-plus-tail dynamical closure and/or leg 315's `O1` Taylor-model flow-map enclosure — where
> the apparatus is **named with a citation** and **shown, in the unit's own pre-registration, not to
> construct a single bounded approximate inverse uniform in `M`**?
> **yes →** name the target and the ansatz; name the apparatus and give the C1 compliance argument
> in full; give the feasibility verdict with the **named obstruction or the named next step**, and
> state explicitly what the verdict does **and does not** establish.
> **no →** return a **measured statement of which candidate targets were considered and why each
> fails** — per candidate, the named property that disqualifies it (not fluid; dissipative term
> outside the certified equation; already certified by someone; no expressible blow-up ansatz).
> **A named list of failures with the reason per candidate is a landable answer and is reported as
> the result, not as a failure of the unit.**
> **`UNDER-RESOURCED` →** §3d governs: an attempt that runs out of budget returns
> **`UNDER-RESOURCED` and a cost for the compliant attempt**, never a bare `no`.

**PRE-COMMITTED READING.** **(a) A NAMED TARGET IS NOT A CERTIFICATE.** Naming the object leg 174
says the cell is empty for want of does not fill the cell, does not enclose anything, and is not
evidence anything can be enclosed. **(b) A FEASIBILITY IS NOT A RESULT ON THE CLAY CHAIN.** No link
of `L1 → L4` moves in this unit under any branch; the ceiling stays **Tier 2** and **Clay stays
~0.05%**, and the write-up says so in its own words (§3h rules 2 and 3 — scale is not evidence, and
a large build is not a result). **(c) `W3` IS BROKEN ONLY BY LEG 174's OWN GRADE-A CRITERION,
APPLIED UNCHANGED** — an interval-arithmetic enclosure of a **genuine finite-time singularity** of a
**dissipative fluid** equation with the **dissipative term inside the certified equation**. Nothing
in this unit approaches that bar, and no sentence may suggest it does. **(d) IF THE APPARATUS, WHEN
ACTUALLY SPECIFIED FOR THIS TARGET, TURNS OUT TO REQUIRE A BOUNDED APPROXIMATE INVERSE UNIFORM IN
`M`, THE UNIT STOPS AND SAYS SO.** That is `T4`'s branch (c), and it fired once already this
programme; it is a **more valuable** finding than a feasibility verdict, because it is a fact about
the ban that nobody has measured. Report it as a **stop**, not as a failure. **(e) THE NEGATIVE
BRANCH IS AS VALUABLE AS THE POSITIVE ONE** — that is the whole reason this lane is cheap. A
measured "no admissible target exists in 1D, and here is the property each candidate fails" is the
strongest available evidence that the ceiling is Tier 2, and it is **not softened, not padded, and
not rewritten as a partial success.** **(f) NOVELTY.** The named target owes a novelty pass **before
any construction**: if a Grade-A certificate for it already exists in the literature, **W3 is broken
by someone else and that is the finding** — report it as such rather than proposing to rebuild it.
**(g) CONTROLS, PLANTED AND FIRING BOTH WAYS.** The unit's Grade-A/fluid classifier must be shown to
say **both** words: a **positive control** it must classify as Grade-A-but-not-fluid
(Dahne–Figueras CGL `arXiv:2410.05480`, reproduced here by leg 316), and a **negative control** it
must reject (an object whose dissipative term is outside the certified equation). A classifier that
cannot fire both ways has not classified anything. **(h) Lesson 91:** any negative names its
realization, trial space and basis.

**Territory (§5b).** `experiments/journal/leg_396.md`, `experiments/p2_route_v2_*.py`,
`writeup/data/p2_route_v2_v1.json`, `writeup/novelty/leg_396.md`, **figure `fig111`** (allocated
here, at dispatch, to this unit and to no other). **Branch:** `leg/396-v2-target`.
**Resourcing (§3d):** resourced as a **full unit** — build whatever the target selection and the
feasibility argument need. An under-resourced attempt returns `UNDER-RESOURCED` **and a cost**.

### 2. `L2` — ATTACK `CLAY_OBLIGATIONS.md` §6(i). *Lane L. leg 397. The first unit ever dispatched at a final blocker.*

**Is certified far-field decay plus an admissible cutoff genuinely without METHOD, or only without
an ATTEMPT?** The claim "no known method" has been carried as an assumption through 395 legs
without being checked to the standard this repository applies to everything else, and it sits on the
most load-bearing statement in the whole roadmap. **Leg 381's banked bill is the object:** critical
`L³` tail **326.875 per decade** (the increment of the *cube*; the norm itself runs 8.679 → 14.841),
required decay exponent **`α > 1.5`** against an a-priori **`α = 1.0`** — **a deficit of 0.5. That
is a number, not an impossibility, and the unit's question is what would supply it.**

> **GATE (final wording).** Reading the **published** localisation / far-field-decay techniques
> against **this object** — route 4's discretely-self-similar profile carrying leg 381's banked bill
> — does the unit state, **per technique**, the **named hypothesis** that fails for this object, or
> the one that does **not**?
> **yes →** report the table: technique, citation, the hypothesis it requires **quoted verbatim and
> located by section or page**, and whether this object satisfies it. State plainly whether the
> answer is *"still no method, and here is precisely which hypothesis fails"* or *"here is a
> candidate whose hypotheses this object may meet"* — **and for any candidate, state whether leg
> 381's bill is actually paid (`α > 1.5` supplied for THIS object) or not.**
> **no →** name which techniques could not be located or read at the level required, and **what it
> would take** — a cost, not a verdict (§3d). **`UNDER-RESOURCED`, never a bare `no`.**

**PRE-COMMITTED READING.** **(a) A MEASURED "STILL NO METHOD, AND HERE IS PRECISELY WHICH HYPOTHESIS
FAILS" IS A REAL, LANDABLE RESULT AND IS NOT SOFTENED.** It is **the answer to whether the Tier-2
ceiling is permanent**, which is the single most useful thing this lane can return short of a
method. It is not a failure, it is not padded with hedges, and it is not rewritten as "promising
directions". **(b) A CANDIDATE METHOD IS A LEAD, NOT A BROKEN WALL, UNTIL LEG 381's BILL IS ACTUALLY
PAID.** The word is **candidate**. `W4` is broken only by its own pre-committed test — a
localisation argument that carries blow-up from the infinite-energy profile to a finite-energy
solution **with the decay actually available**, or a natively finite-energy ansatz. A technique
whose hypotheses hold for a *different* object has not paid this object's bill. **(c) THE DEFICIT IS
THE MEASUREMENT, AND IT IS NOT TO BE RE-DERIVED SLOPPILY OR QUOTED FROM PROSE** — take 326.875 per
decade and `α > 1.5` vs `α = 1.0` from the banked artefact, and if the banked artefact disagrees
with any prose in the repository, **the artefact wins and the disagreement is banked**. **(d) READ,
DO NOT CONTACT.** Any published document may be fetched and read; **contacting an author, group,
maintainer or list remains HELD by the user** and needs its own ruling. Do not route around it — 
raise it. **(e) INSTRUMENT EVERY ZERO.** A technique not found is `UNREACHABLE` or `THROTTLED` with
the reason banked, **never a zero and never a confirmation**; leg 387's namespace bug fabricated a
controlled zero once already, and leg 392 was throttled on 5 of 6 substantive Semantic Scholar
queries. **No S2 key exists** — pace against the unauthenticated limits and back off. **(f) LESSON
91.** Any negative here names the object it is a negative about: the profile, the norm, the decay
available, the cutoff class. **(g) CEILING.** Reading the literature moves no `L1 → L4` link.
**Tier 2; Clay ~0.05%.**

**Territory (§5b).** `experiments/journal/leg_397.md`, `experiments/p2_route_l2_*.py`,
`writeup/data/p2_route_l2_v1.json`, `writeup/novelty/leg_397.md`. **No figure.**
**Branch:** `leg/397-l2-decay`. **Resourcing (§3d):** a literature-and-analysis unit against a
banked bill, ≈2–4 h. If the compliant reading costs more, return `UNDER-RESOURCED` **and the cost**.

### 3. `L3′` — THE CHEN–HOU READING UNIT. *Lane L, literature, FULL TEXT. leg 398.*

**`T6` found this as a near-miss and recorded it rather than dropping it**, which is the only reason
it is on the board. `arXiv:2308.01528` §1 describes the Chen–Hou line as **computer-assisted blow-up
on an UNBOUNDED domain, in >1D, with ALGEBRAIC decay** — precisely the combination leg 348's
obstruction says the Galerkin-plus-tail bridge cannot reach. **It is the record's best lead on the
compact-domain obstruction, and it points at route 4's actual `ℝ³` geometry — prize statement (C).**

> **GATE (final wording).** Reading `arXiv:2308.01528` and the Chen–Hou stability line **at full
> text**, does the unit answer **both** named questions, **each with the deciding sentence quoted
> verbatim and located by section or page**:
> **(a)** does its **unbounded-domain, algebraic-decay, computer-assisted** mechanism **bear on the
> compact-domain obstruction leg 348 named — and ON WHICH SIDE**: does it **UNDERCUT** the
> obstruction (a certified object living where the obstruction says the bridge cannot reach),
> **STRENGTHEN** it (the mechanism is available only because of a feature the obstruction already
> names), or **NOT REACH** it (the objects or apparatus differ)?
> **(b)** does its **nonlinear-stability-with-finite-unstable-spectrum** technique contain anything
> that reaches **`CLAY_OBLIGATIONS.md` §6(ii)** — persistence of the blow-up under localisation —
> **for this programme's object**, and if so, **which hypothesis would this object have to satisfy**?
> **yes →** both answered, with quotes located. Name explicitly anything that moves leg 348's
> obstruction in either direction.
> **no →** name which document could not be obtained at full text and **what it would take** (§3d).
> A document not obtained is banked as **`UNREACHABLE`** with its reason — **never as a
> confirmation and never as a zero.**

**PRE-COMMITTED READING.** **(a) ALL THREE BRANCHES OF QUESTION (a) ARE NAMED IN ADVANCE AND NO
FOURTH IS CONSTRUCTED** — UNDERCUT / STRENGTHEN / DOES NOT REACH. **The prior is DOES NOT REACH, and
it is `T6`'s, recorded before this unit existed:** the target is **stationary self-similar** rather
than time-periodic, and the apparatus is **energy estimates** rather than Galerkin-plus-tail, so
`T6` judged it **not** a counter-instance to the obstruction as posed. **This unit must say whether
full text AGREES or DISAGREES with that prior, in those words**, and an undercut is the valuable
branch and is **reported first**, not buried. **(b) A TECHNIQUE THAT REACHES §6(ii) IN SHAPE IS NOT
A METHOD.** Naming the hypothesis this object would have to satisfy **is** the deliverable; claiming
the obligation is discharged is not available on any branch of this gate. **W5 is unbroken and stays
unbroken by anything read here.** **(c) A CONFIRMATION IS NOT A STRENGTHENING** — `T6`'s standard,
applied unchanged: "the full text is consistent with the abstract" adds nothing; only a full-text
clause that could not have been seen at abstract level counts, and it must be quoted. **(d) THIS
UNIT READS. IT DOES NOT CONTACT.** Papers, proceedings, theses, publisher pages, full texts:
authorised. **Contacting an author, group, maintainer or mailing list: HELD by the user, and needs
its own ruling.** **(e) BANK `UNREACHABLE`/`THROTTLED` AS SUCH, NEVER AS ZEROS, AND INSTRUMENT EVERY
ZERO** — a positive datum proving the source was reached, on every query. **No Semantic Scholar key
exists**; pace against the unauthenticated rate limits and back off rather than assuming one.
**(f) CEILING.** No `L1 → L4` link moves. **Tier 2; Clay ~0.05%.**

**Territory (§5b).** `experiments/journal/leg_398.md`, `writeup/data/p2_route_l3p_v1.json`,
`writeup/novelty/leg_398.md`. **No figure.** **Branch:** `leg/398-l3p-chenhou`.
**Resourcing (§3d):** full text of one paper plus the stability line around it, ≈1.5–3 h.

### 4. `V-W2` — THE WAVE-2 VERIFIER. *Verification. OBLIGATORY under §3g.*

**`T4`, `T6` and `T5` are `UNVERIFIED` and this Conductor planned all three.** §3g is explicit that
this is the one thing a Conductor may not do for itself. **`V-W2` is a fresh worker with no memory
of the construction, re-deriving from banked JSON and landed evidence scripts alone**, briefed on
the **claims** and never on the reasoning that produced them.

> **GATE (final wording).** Re-deriving **from the banked JSON and the landed evidence scripts
> alone**, does each of the following reproduce **exactly**?
> **(1) `T4`'s 2D-lift finding:** `N_x3 = 0` in Table 1 and in `Nrec`; decoded coefficient arrays of
> **extent 1** in `x₃`; `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` **exactly** while
> `max|ω⁽³⁾| = 1.6351 / 1.5274`; `setup = '2D'`.
> **(2) `T4`'s first conjunct and its negative control:** criterion (4.32) verified on both rows,
> `r_min`/`r_max` relative deviations to **`5.6e-15`**, both `r_sol^Ω` exact, independent norm check
> **`δ = 5.3e-06`** against **`1e-3`**; and the apparatus finding with its control — term counts
> *approximate inverse* **×7**, *Newton-Kantorovich* **×4**, *interval arithmetic* **×5**, INTLAB
> **×2**, against **all six** closure terms (*self-consistent*, *a priori bounds*, *isolating*,
> *trapping region*, *logarithmic norm*, *dynamical closure*) at **zero**, Zgliczyński appearing
> only as bibliography item **[48]**.
> **(3) `T6`'s table:** **7/7** full texts read, **2 UNDERCUT / 4 strengthen / 1 confirm**, **0**
> `UNREACHABLE`, **0** `THROTTLED`; and **UNDERCUT 2** — `arXiv:2409.09234` carries **no-slip walls,
> not periodicity**, so leg 348's `domain_census` **over-counts by one**.
> **(4) `T5`'s sweep:** corpus **1428** tracked `*.md`+`*.py` / **417,476** lines with `DIRECTION.md`
> excluded by name **and the exclusion asserted executably**; **7 refusals, APPARATUS 5 /
> REALIZATION 2**; **exactly 2** re-openable under C1 (leg 348's Galerkin-plus-tail build and leg
> 315's `O1`); and **leg 257 NOT re-openable** — its apparatus is the Corollary-21 radii polynomial
> in a fourth **space**.
> **yes →** each reproduces; say so per item, **with the number you got**.
> **no →** name the item, the number you got, the number claimed, and the **file and line** the
> discrepancy is in. **A DISCREPANCY IS THE DELIVERABLE, NOT A FAILURE OF THE UNIT.**
>
> **AND ONE OBLIGATION FOLDED IN, FOUND BY `V1` AND OWED SINCE 2026-08-13** (`OPTIONS.md` §F; well
> under an hour): **`T1` / leg 391 banked NO machine record** — no JSON, no evidence script — so its
> gate answer checks out against **prose only**. **Bank the packet's three questions and the fact
> that it ruled NONE of them, with an evidence script that EXITS NON-ZERO on disagreement with
> `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`.**

**PRE-COMMITTED READING.** **(a) AGREEMENT IS THE EXPECTED OUTCOME AND IS WORTH LITTLE ON ITS OWN.**
The Conductor already re-derived parts of (1)–(3) at landing; the value is concentrated wherever a
number has been transcribed rather than measured. **(b) A DISAGREEMENT IS BANKED AS A DISAGREEMENT
AND IS NOT RECONCILED BY THE VERIFIER.** Report both numbers and stop — deciding which is right is
the Conductor's job, and doing it inside the verifier destroys the independence the unit exists for.
**(c) A CLAIM THE JSON CANNOT SUPPORT IS `UNVERIFIABLE`, NOT `no`** — and that is a finding about
banking discipline, which lesson 68 says decays at the rate of memory. It is exactly how `T1`'s
missing record was found. **(d) `V-W2` MUST NOT READ** `STATE.md`, `WALLS.md`, `OPTIONS.md`,
`DIRECTION.md`, `reports/ORCH_STATE.md`, the wave-2 briefs, or the wave-2 journals' **reasoning**
sections. It reads the **claims listed in this gate**, the **banked JSON**, and the **landed
evidence scripts**. **That narrowness IS the unit.** **(e) THE FILENAME TRAP, NAMED IN ADVANCE
BECAUSE THE RECORD ALREADY WARNS ABOUT IT:** `writeup/data/p2_route_p2t1_v1.json` is **leg 302,
route P2T1, unrelated to `T1`.** **Do not match on filename substrings** — scan the `leg`/`route`/
`unit` **fields** of every banked JSON. **(f) BANKING `T1`'s RECORD DOES NOT RE-OPEN `T1`'s GATE
ANSWER** and is not evidence for or against it; `V1` already ruled that. The record states what the
packet **asked** and that it **ruled none**. **(g) CEILING.** Verification moves no `L1 → L4` link.
**Tier 2; Clay ~0.05%.**

**Territory (§5b).** `experiments/journal/verify_wave2.md`, `writeup/data/p2_verify_wave2_v1.json`,
and for the folded-in obligation `writeup/data/p2_route_t1_packet_v1.json` +
`experiments/p2_route_t1_packet_evidence.py`. **Writes no source, no figure, and none of the
Conductor-owned files.** **Branch:** `verify/wave2`. **Resourcing (§3d):** ≈2–3 h.

---

### What `OPTIONS.md` offered and was NOT taken this wave, and why

§3g requires `OPTIONS.md` be read alongside this file when planning every wave, and a deferred
option that is never *said* to be deferred is an option that was silently dropped.

| option | why not this wave |
|---|---|
| **`L1`** — price §4 on `ℝ³` (`OPTIONS.md` §D) | **Deferred by ONE WAVE, deliberately, and it is ranked for wave 4.** It is the same *shape* of unit as `L2` — read the published attempts, name the hypothesis that fails per attempt — and running both in one wave would put two literature units on the same reading discipline before either has been verified. `L2` is ranked first because leg 381 banked it a **number** to attack, which `L1` does not have. |
| **`T2″`** — Type-I rigidity on `T³` (`OPTIONS.md` §E) | **Deferred with Lane T, and it is now RE-OPEN CONDITION (ii) FOR THE WHOLE LANE.** That raises its value rather than lowering it: it is the one unit that can bring Lane T back. Not taken because the wave is full and both priority lanes come first. |
| **`T3`** — the non-DSS `T³` ansatz | **DEFERRED WITH THE LANE, NOT KILLED** (user ruling 2026-08-14). Still the lane's real mathematical content; it runs when a re-open condition is met. |
| **`T2′`** — the compliant rigidity search | **Deferred with Lane T.** Priced at ≈1.2–1.7 h now that the ruling has landed and full text is readable. |
| **`E`** — the H-hard diagnostic (wave 1) | **NOT RE-DISPATCHED.** Its gate is unanswered and its branch holds two of three diagnostics; finishing it needs U2's DNS regenerated (≈6–7 h wall in total) because the container took the checkpoints. The user ruled this wave's composition, and `E`'s result **re-opens Lane R rankings in `OPTIONS.md` §A/§B — it does not change this wave.** Ranked for wave 4 alongside the verifier. |
| **`R2`** — deflation (`OPTIONS.md` §B) | **Deferred by contract and by ranking.** It is the strongest surviving Lane R item, but a wave with two priority-lane units, a literature unit and an obligatory verifier has no room, and Lane R never sets a wave's direction. |
| **`R3`/`R4`/`R5`, `PROG-R4` A/B/C/D, `U4`/`G2`** | **Deferred.** A/B/D buy supply and are demoted by U5's pre-committed reading (branch (b): the bias is in **basin structure**); `U4`/`G2` is **blocked**, not deferred — it needs a recovered **named** orbit and there is not one. |
| **(D)'s data conditions (8),(9)**; **leg 390 §5 item 1's `check_A` re-run** | **Deferred WITH Lane T.** Unblocked and cheap, but (D) is the torus branch and the torus is deferred; parked with the lane rather than run for a branch nothing is currently attacking. |
| **`T1`'s owed machine record** (`OPTIONS.md` §F) | **TAKEN — folded into `V-W2`.** It is well under an hour and it belongs with a verifier, not on its own. |
| **U3's two owed novelty questions; legs 387/388/389** (`OPTIONS.md` §F) | **Deferred.** Small, real, and they lose to two priority-lane units and an obligatory verifier. |

---

## Open — needs the user, not a task

1. **`PROG-R4` after U5 — five costed options, ONE RULED.** The user ruled **option E** on
   2026-08-13 and it is the unit that did not return (see "In flight"). **A, B and D stay
   unqueued** — all three buy supply, and the pre-committed reading points away from it. **C** stays
   unqueued with its own milestone, aimed at `|s| > 0.9` rather than at the named rows. Full text
   and costs: `experiments/journal/prog_r4_u5.md` §9, preserved verbatim. **`PROG-R4` is not
   stopped**; `G1` stays `UNDER-RESOURCED`.
2. **The two ban-wording defects that are RECORDED AND NOT RULED**, because nothing currently
   depends on them: the ℓ¹-Fourier ban's lift clause still names a *"FOURTH space/basis"*, which is
   the wrong kind of object for a candidate that is an **apparatus** (moot while Lane T is deferred,
   and `T5` measured that it is exactly what blocks leg 257); and stage V's lift clause is now clean
   after B1. **Neither is escalated** — an entity that both raises and rules an escalation has
   defeated the mechanism, and there is nothing to rule until a unit is blocked by one.
3. **Statement (D)'s data conditions (8) and (9) are UNREAD**, and readable since the outreach
   narrowing. **Parked with Lane T** (item above). Until they are read, `CLAY_OBLIGATIONS.md`'s
   "(D) carries no decay condition" stays narrowed to (D)'s **solution** conditions, and leg 390 §5
   item 1's `check_A` re-run stays owed.
4. **The DSS escalation packet** (legs 313/320, branches unmerged). Complete: both candidate
   theorems read at full text and neither reaches the screened object.

**DISCHARGED 2026-08-14 and no longer on the desk:** the C1-exemplar escalation
(`writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`) and, from 2026-08-13, all four
ban-wording items (`writeup/escalations/RULING_BAN_WORDING_2026-08-13.md`).

## Live bans — 19, one line each

Full text and lift conditions: `.venv/bin/python plan_of_record.py`. **Run it when a task
could touch one**; do not paraphrase from here. **§3h rule 1: a ban is superseded by a
measurement, never by a decision** — and a defective ban *wording* is a user escalation.
**Ban counts are UNCHANGED by the 2026-08-14 ruling: 26 recorded, 19 in force.**

gCLM measurement · DSS cheap entrance (bifurcation off a fixed point) · DSS expensive entrance
(**SCOPED 2026-08-11: a *seeded* search is outside it; name the seed or the ban applies**) ·
2D β re-measurement · scaling-gauge near-null · GA compute on unvalidated fitness ·
"closure is a property of the space" · stage V as posed · ℓ¹-Fourier/radii-polynomial on any
model (**SCOPED 2026-08-13 by C1 to an APPARATUS; C1 stands EXEMPLAR-FREE after 2026-08-14 and
is NOT evidence any apparatus closes; the naming requirement binds every unit**) ·
V-rigorous's L1 prerequisite (superseded) · closing the truncation gap by extending the
domain · three readings of legs 51/53 · `Z₁` block-coupling by tuning · weight exponent toward
leg 51's minimum · leg 51's finding at full strength · leg 51's zero `Y₀` as progress ·
Chen–Hou 2D as a target · leg 44's 2D near-null · building a solver without grepping
`capabilities.py`.

## Standing discipline — non-negotiable in every mode

Three-tier win condition (Tier 2 is never a proof) · pre-committed gates on every claim ·
novelty pass before construction (**once per programme**, not per unit, under §3c) ·
**lesson 91**: a negative names its realization/trial-space/basis · **§3d**: a stop fires only
on a null from an attempt resourced at the scale the question is posed at — an under-resourced
null returns a cost and answers `UNDER-RESOURCED` · planted controls that can fire both ways ·
**lesson 68**: checks are executable or they decay · `scripts/merge_gate.sh origin/main` must
PASS on everything that lands · **reading published material is authorised; CONTACTING an author,
group, maintainer or list is HELD** (narrowed 2026-08-13) · no output described as movement toward
Clay unless a link actually moved · **§3h rule 2: scale is not evidence** — a large build is not a
result, and the gate is the deliverable.

**WAVE COMPOSITION FLOOR (`ORCHESTRATION.md` §3g).** **Every wave carries at least one unit that
attacks a wall on the Clay chain directly** — a Lane T, V or L unit. Lane R work is real and it is
often the most productive thing here, which is exactly why this floor exists: efficiency work is
satisfying, it always has a next increment, and a programme can spend a year getting very good at
finding orbits it was never going to certify. **A wave of pure Lane R units is out of contract**,
and so is a wave whose only non-Lane-R unit is an audit.

**VERIFICATION IS A FRESH SESSION OR IT IS NOT VERIFICATION**, and **a Conductor may not verify a
wave a Conductor planned.** Every wave budgets one verifier, dispatched in the *following* wave.
**Wave 4 carries wave 3's.**

## Where the detail lives — consult by pointer, never wholesale

| Need | Read | Size |
|---|---|---|
| **The blockers and the lanes** | **`WALLS.md`** | **7 walls, 4 lanes — read whole** |
| **The 2026-08-14 lane ruling** | `writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md` | one page |
| The 2026-08-13 ban rulings | `writeup/escalations/RULING_BAN_WORDING_2026-08-13.md` | one page |
| The strategic ruling | `CLAY_ROADMAP.md` §7.5 + **§7.6** | two addenda |
| A task's own spec | `DIRECTION.md`, that entry only | 23,699 lines — never read whole |
| Bans, stage, gate, lanes | `.venv/bin/python plan_of_record.py` | executable, ~40 lines out |
| Does a module exist | `.venv/bin/python capabilities.py <term>` | executable, grep don't read |
| The contract | `ORCHESTRATION.md` §3c–§3h | 3g = CONDUCTOR, 3h = walls |
| What a Tier-2 candidate owes | `CLAY_OBLIGATIONS.md` | 8 sections, §4 verified |
| Per-leg record | `experiments/journal/leg_N.md`, `writeup/novelty/leg_N.md` | one leg each |
| **Deferred options, with costs and re-open conditions** | **`OPTIONS.md`** | read when planning a wave |
| Wave 1 and 2 gates, verbatim | git `a384d92` and `c1a8d5e`; `reports/ORCH_STATE.md` | history |
| `E`'s four pre-committed branches, verbatim | `experiments/journal/prog_r4_e.md` §3 on `prog-r4/e-hhard` | branch, unmerged |
| Banked numbers | `writeup/data/*.json` | **re-derive from these, never from prose** |
