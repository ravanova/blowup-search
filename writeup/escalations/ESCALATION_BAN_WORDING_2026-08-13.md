# ESCALATION — BAN WORDING, 2026-08-13

**Raised by:** leg 391 (unit `T1`, Lane T, CONDUCTOR wave 1).
**Route:** `ORCHESTRATION.md` **§8**, escalation 2 (*lifting or weakening any ban other than via its
recorded lift condition*) and escalation 1 (*a change to `plan_of_record.py`*). Under **§3h rule 1**
a ban whose **wording** has become defective is a **user escalation, not an agent's reading**.

**This packet rules nothing.** It states, for each pending question, **both** supportable readings
with the evidence for each, drawn from the ban's own text and from the landed record. It expresses
no preference between them and recommends no option. `ORCHESTRATION.md` §3g notes that an entity
which both raises and rules an escalation has defeated the mechanism; the Conductor has refused to
rule these, leg 348 §5 refused before it, and this packet refuses too.

**Ban text below is quoted from the executable output of `.venv/bin/python plan_of_record.py`.**
`plan_of_record.py` was not read, edited, or touched by this leg; `git diff origin/main --
plan_of_record.py` is empty (recorded in `experiments/journal/leg_391.md` §7).

---

## 0. The four items, and what each one blocks

| # | question | pending since | what it blocks |
|---|---|---|---|
| **(a)** | **Cadiot.** The lift clause says *"unless a pass resolves whether…"*; a pass has resolved it, and the resolution **confirmed** the ban's justification. | 2026-08-11 (leg 304) | **Nothing operational.** Its subject is a *claim about the literature*, not a build. Bundled here because it is pending, not because a lane needs it. |
| **(b)** | **Stage V's "needs L1 first."** A lift condition that is unliftable as written — and a 2026-08-06 ban review whose own text says it retired that wording. | 2026-08-06 / re-raised 2026-08-13 | **Lane V's first unit (`V1`).** |
| **(c)** | **The apparatus question.** Does the ℓ¹-Fourier/radii-polynomial ban reach a Zgliczyński-style Galerkin-plus-tail **dynamical** closure? | 2026-08-13 (leg 348 §5 raised it 2026-08-12 and refused to answer) | **THE WHOLE OF LANE T** — `T3` and `T4` included. |
| **(d)** | **The outreach hold on Lane T's critical path.** Not a ban-wording question; raised here because it is the fourth thing the user must decide before Lane T can be read honestly. | 2026-08-13 (leg 390 §4) | Any Lane T claim about statement **(D)**'s acceptance conditions. |

---

## (a) CADIOT — the lift clause's literal reading and its evident purpose disagree

### The ban, verbatim

> **BANNED:** re-claiming leg 51's methodological finding at full strength — RESOLVED at leg 57:
> Breden-Desvillettes-Lessard arXiv:1503.06315's assumptions (4)-(5) require a diagonal bounded
> away from zero (read from the full PDF, not the abstract), so BDL does NOT cover the zero-diagonal
> Fredholm case — that BDL-shaped reason to keep this ban is discharged. A DIFFERENT, STRONGER
> reason replaces it: Cadiot arXiv:2505.03091 sec 2/3 independently states the same
> dominance-hypothesis observation, in full text, located and verified by a second independent pass
> (VER-D)
>
> **lifted by:** never — **unless a pass resolves whether Cadiot's construction covers a zero
> diagonal**, which is now the live open question, not BDL's.

The entry then carries an annotation landed 2026-08-11, which already states the conflict in terms
and refuses to resolve it: *"…the lift clause is worded as 'unless a pass resolves whether', and a
pass has now resolved it, so the clause's literal reading and its evident purpose now disagree. That
is a wording question, not a judgement call an agent may make: ESCALATED TO THE USER 2026-08-11 and
pending. Until the user rules, the ban stands in force, unchanged, and binds every leg."*

### What the pass measured

Leg 304 (Route-CADX), gate branch **(i)**, landed at `b319449`
(`experiments/journal/leg_304.md`). Cadiot arXiv:2505.03091, Assumption 1, p.6, verbatim from the
pinned PDF:

> *Let l be defined in (2). Assume that there exists ρ > 0 such that l is analytic on the strip
> I_ρ … Moreover, assume that there exists* **l_min > 0** *such that* **|l(ξ)| ≥ l_min for all
> ξ ∈ ℝᵐ** *and lim_{|ξ|₂→+∞} |l(ξ)| = +∞.*

`L` is a Fourier multiplier by the class definition (1)–(2), so `l` **is** the diagonal, and a
vanishing diagonal is exactly the excluded case `l_min = 0` — excluded **by hypothesis**, before
anything is constructed. **Load-bearing at 8 of 12 located clauses** (`A1_LMIN`, `SPACE_H`,
`SPACE_XQ`, `SIGMA_DELTA`, `LEMMA_4_1_USES_IT`, `LEMMA_3_1_USES_IT`,
`TAIL_DIAGONAL_IS_THE_SYMBOL`, `SYSTEMS_KAPPA`). All 11 machine-checkable quotes were re-extracted
from the pinned PDF and matched (`quote_verification: VERIFIED, 11/11, sha256 match true`). The
hypothesis is not vestigial: leg 304 measured `l_min` on the paper's own four examples (0.2 Whitham,
0.28, 0.32, and planar Swift–Hohenberg where `l_min = µ` exactly, `max |l_min − µ| = 0.0e+00`).

### READING A1 — the condition is stated as a *resolution*, and it has been met

1. **The clause's plain text.** It asks for *"a pass [that] resolves **whether** Cadiot's
   construction covers a zero diagonal"* — a question, not a direction. A pass ran; the question is
   resolved; the recorded condition is satisfied on its face. Lifting *via* a ban's recorded lift
   condition is the ordinary route, not §8 escalation 2.
2. **The clause names the question as the ban's own live issue** — *"which is now the live open
   question, not BDL's"* — i.e. the drafter identified one question as what the ban turned on, and
   that question no longer has an unknown answer.
3. **The structural parallel inside the same entry, which is A1's strongest support.** The
   predecessor reason was discharged by a pass with **the same finding shape**: leg 57 read BDL's
   assumptions (4)–(5) from the full PDF, found they *require a diagonal bounded away from zero*,
   i.e. **BDL does NOT cover the zero-diagonal case** — and the ban's own text records the
   consequence as *"that BDL-shaped reason to keep this ban is **discharged**."* Leg 304 returned
   the same finding about Cadiot ("does not cover the zero-diagonal case") and the annotation
   records the **opposite** consequence. A drafter working in the pattern the entry itself
   establishes would reasonably have expected "does not cover" to discharge. On this reading the
   defect is not in the *answer* but in a reason that was drafted so that the same measurement
   points both ways depending on which prior work it is about.

**If A1 is the ruling:** the ban lifts by its recorded lift condition. What becomes permitted is
*re-claiming leg 51's methodological finding at full strength* — a novelty/priority claim about the
literature. Note that leg 304's own evidence is what such a claim would then have to be stated
against, and that no lane in `WALLS.md` is waiting on it.

### READING A2 — the resolution confirmed the ban's justification, so lifting on it inverts §3h rule 1

1. **What the ban actually rests on.** Not "somebody covered the zero-diagonal case", but *"Cadiot
   … **independently states the same dominance-hypothesis observation**"* — i.e. Cadiot is prior art
   for leg 51's *observation*. Leg 304's finding is the **strongest possible form** of that: Cadiot
   does not merely fail to cover a zero diagonal, it **excludes it by explicit hypothesis on the
   paper's first page of setup**, and relies on that exclusion at 8 of 12 located clauses. The
   observation leg 51 made is exactly the hypothesis Cadiot writes down.
2. **This is why the two passes point opposite ways, and it is a real distinction, not an
   inconsistency.** BDL's reason was *coverage*; Cadiot's reason is *statement*. "Does not cover"
   discharges a coverage reason and confirms a statement reason.
3. **§3h rule 1.** *A ban is superseded by a measurement, never by a decision.* Here the measurement
   went the ban's way. Lifting on it would be lifting a ban **because its own justification was
   validated** — the annotation's own words, and the reason it escalated rather than lifted.

**If A2 is the ruling:** the ban stands and the *clause* is the defect. What the user would be
re-drafting is a lift condition that tracks the **direction** of a resolution rather than its
occurrence.

**Both readings are supportable. This packet does not choose between them.**

---

## (b) STAGE V'S "NEEDS L1 FIRST" — live defect, or retired one?

The dispatch authorises this leg to answer the **factual** question — *which text is operative* —
because it is settled by artefacts. It does **not** authorise ruling what the operative text means.
§1 below is the factual answer; §2 and §3 are the two readings, and they are not ruled.

### 1. THE FACTUAL ANSWER, from the artefacts

**Fact 1 — three entries exist today.** `plan_of_record.py`'s executable output prints, among the
19 bans in force:

> **(V-as-posed)** re-opening stage V as posed — the novelty gate answered YES on 2026-08-04
> (arXiv:2410.05480 verifies CGL branches in the dissipation parameter, in interval arithmetic), and
> leg 48 re-derived their zeros, branch and fold to confirm it
> — *lifted by:* **never — unless the question is re-posed for a FLUID transport model, which needs
> L1 first**

> **(re-posed ℓ¹-Fourier)** RE-POSED 2026-08-06 (ban review, user ruling 2): re-attempting the
> ell^1-Fourier/radii-polynomial machinery this repository has measured DEAD in three realizations
> (ell^1_w coefficient basis leg 54, collocation basis leg 56, origin-H^2 capped at a=0 with no
> transfer to the real target legs 163/176), on ANY model, fluid or otherwise — **this retires the
> prior 'needs L1 first' wording**, which the ban review found had become an impossible precondition
> (L1 has three independent dead attempts and no fourth candidate) rather than a live lift path
> — *lifted by:* never — unless a namable FOURTH space/basis this repository has not yet tried is
> proposed, with its own scoping leg establishing it is not subject to the same three-realization
> death

> **(superseded)** SUPERSEDED 2026-08-06 (ban review): reading V-rigorous's L1 prerequisite as
> optional — a float study cannot be upgraded into a certificate after the fact. Retained for the
> record; **the re-posed ban above is now the operative wording on this question.**
> — *lifted by:* never — superseded by the re-posed ban above, retained for history only

**Fact 2 — the V-as-posed entry has never been edited.** `git log -S "which needs L1 first" --
plan_of_record.py` returns **exactly one commit**: `561bb68` (2026-08-05, *"Route-V v0: the novelty
gate closes the stage"*), the commit that introduced it. The 2026-08-06 ban review (`4ff544a`) did
**not** touch that string.

**Fact 3 — what the ban review actually deleted was a different entry.** The diff hunk
`@@ -739,7 +824,20 @@ BANNED = [` in `4ff544a` shows the V-as-posed entry as **unchanged
context**. The single deleted line was:

```
-    ("reading V-rigorous's L1 prerequisite as optional -- a float study cannot be upgraded into a certificate after the fact", "L1"),
```

replaced by the two new entries quoted above.

**Fact 4 — the deleted entry did not contain the retired phrase.** Its lift field was the bare
string `"L1"`. The phrase *"needs L1 first"* appears nowhere in it. In the whole `BANNED` table, past
and present, the phrase occurs in **exactly one place: the V-as-posed entry's lift clause.**

**Fact 5 — four landed records say stage V's ban *was* re-posed.** `4ff544a`'s own commit message:
*"Stage V's ban re-posed since its 'needs L1 first' lift condition was unliftable (L1 dead in 3
realizations)."* Also `CONTINUATION_PROMPT.md:118`, `experiments/JOURNAL.md:3561`,
`CLAY_ROADMAP.md:367`.

**Fact 6 — a measured ambiguity, not an argued one: two landed legs use the name "the stage-V ban"
for two *different* entries.**

- **Leg 341** (Route-ALGW, *"THE FOURTH SPACE"*) means the **re-posed ℓ¹-Fourier** entry:
  *"Does the algebraically weighted space leg 260 computed for the NS3D-DSS target escape the
  **stage-V ban's three-realization death**…"* (`experiments/journal/leg_341.md:3-4`); *"The lift
  condition on the stage-V ban stays unmet"* (`:123`).
- **Leg 316** (Route-DFRE) means the **V-as-posed** entry, and quotes its "needs L1 first" clause
  in full as live: *"`plan_of_record.py`'s stage-V ban (re-posed 2026-08-04, **confirmed live in the
  printout run this leg**)"* (`writeup/novelty/leg_316.md:28-34`).

**Factual answer.** *As printed today, the V-as-posed entry is in force, unedited since 2026-08-05,
and still carries "which needs L1 first". The 2026-08-06 ban review did not amend it. The entry the
review replaced was a different one, and it did not contain the retired phrase.* Whether the review's
declared retirement nonetheless **reaches** the V-as-posed clause is a question about meaning, and
this packet does not answer it.

### 2. READING B1 — retired in substance, unapplied in text (the defect is editorial)

1. **Fact 4 is the core.** The re-posed entry says *"this retires the prior 'needs L1 first'
   wording"*. The only text in the table that has ever carried that wording is the V-as-posed lift
   clause. The entry the review actually deleted did not. **The referent of the retirement sentence
   can only be the V-as-posed clause**, and the sentence therefore describes an amendment that was
   declared in the new entry's prose but never made to the old entry's field.
2. **Fact 5.** The ban review's own commit message names *Stage V's ban* as the thing re-posed, and
   names *"needs L1 first"* as the reason. Three further landed files say the same.
3. **The stated justification fits only the V-as-posed clause.** *"L1 has three independent dead
   attempts and no fourth candidate"* is a diagnosis of a **lift path**. The deleted V-rigorous
   entry had no lift path to diagnose — its lift field was the bare token `"L1"`.
4. **Practice (Fact 6, leg 341 side).** A landed leg already treats the re-posed entry as stage V's
   ban's successor and works against *its* fourth-space/basis clause.

**If B1 is the ruling:** there is **no live wording defect**. The remedy is a bookkeeping edit to
`plan_of_record.py` — deleting or explicitly superseding the stale clause — which is still §8
escalation 1 and still the user's, but is a correction rather than a ruling on meaning.

### 3. READING B2 — live and unliftable as written (the defect is substantive)

1. **The plan of record is the record.** `plan_of_record.py` is the executable plan; `STATE.md`
   points every task at it and says *"do not paraphrase from here"*. The V-as-posed entry prints
   today, among the 19 in force, with that clause. A commit message is not a ban.
2. **The two entries have different subjects and different justifications.** V-as-posed forbids
   *re-opening stage V as posed*, justified by a **novelty gate** (arXiv:2410.05480 verifies CGL
   branches in the dissipation parameter; leg 48 re-derived their zeros, branch and fold). The
   re-posed entry forbids *re-attempting the ℓ¹-Fourier/radii-polynomial machinery on ANY model*,
   justified by a **three-realization death**. Reading a retirement across from one to the other,
   on a commit message, would be superseding a ban's text **by a decision** — which §3h rule 1
   forbids in terms.
3. **The table demonstrably knows how to mark supersession, and did not mark this one.** The third
   entry carries an explicit marker — *"the re-posed ban above is now the operative wording **on
   this question**"* — scoping the supersession to the V-rigorous L1-prerequisite question. The
   V-as-posed entry carries no marker at all.
4. **The most recent landed readings treat it as live.** `WALLS.md` (2026-08-13, seven days after
   the review): *"the stage-V ban's wording is 'unless the question is re-posed for a FLUID
   transport model, which needs L1 first' — and L1 has three dead attempts and no fourth candidate,
   which makes that precondition unliftable as written."* `ORCHESTRATION.md` §3h rule 1 lists it as
   one of the two already-pending escalations. And Fact 6's leg-316 side quotes it as *confirmed
   live in the printout run this leg*, **after** the review.

**If B2 is the ruling:** the clause is a live defect and Lane V's first unit is blocked on it. What
the user would be deciding is whether stage V's question may be re-posed for a fluid transport model
without L1, or under some other named precondition.

### 4. A THIRD TEXTUAL FACT THE USER SHOULD HAVE, WHICH CUTS ACROSS BOTH READINGS

`plan_of_record.py`'s own `SEQUENCE` prints:

```
[x] L1       Certify HL_S2_nonsymmetric FOR REAL: interval arithmetic + an analytic far-field enclosure
```

**Stage `L1` is marked complete.** The ban review's justification for calling the precondition
impossible is *"L1 has three independent dead attempts and no fourth candidate"* — a statement about
L1's three **realizations** (the same three the re-posed ban names: leg 54, leg 56, legs 163/176),
not about the stage's completion marker. So the same file simultaneously marks `L1` done and
describes it as dead in three realizations. This is recorded as an observation about operative text;
it is **not** offered as a third reading, and this packet does not build an argument on it.

### 5. Both readings agree on venue, and differ on character

Under **B1** the item goes to the user as an edit to `plan_of_record.py` (§8 escalation 1). Under
**B2** it goes to the user as a ban-wording ruling (§8 escalation 2, §3h rule 1). **No branch
resolves inside a lane**, which is why it is here.

---

## (c) THE APPARATUS QUESTION — this is what blocks Lane T

### The question, in leg 348's own words, and its refusal

Leg 348 §5 (`experiments/journal/leg_348.md:122-127`), verbatim:

> **Does not lift, narrow, or re-read any ban.** The stage-V ban and its two entries are outside
> this leg's authority and outside its subject — this leg is about a *different* apparatus
> (periodic-orbit dynamical closure) than the NK/CAP-in-a-function-space apparatus the ban names,
> **and I make no claim about whether that apparatus distinction matters to the ban's scope; that
> reading, if it is ever needed, is for the DM/user** exactly as leg 315 routed its own analogous
> question.

It is now needed. `WALLS.md` W6: *"THAT READING IS NOW REQUIRED WORK, and it is the first thing Lane
T must settle."* Lane T's `T3` (the non-DSS `T³` ansatz — the lane's actual mathematics) and `T4`
(reproducing `arXiv:1902.00384`) are both downstream of it.

### The ban whose scope is in question, verbatim

> **BANNED:** RE-POSED 2026-08-06 (ban review, user ruling 2): re-attempting the
> **ell^1-Fourier/radii-polynomial machinery** this repository has measured DEAD in **three
> realizations** (ell^1_w coefficient basis leg 54, collocation basis leg 56, origin-H^2 capped at
> a=0 with no transfer to the real target legs 163/176), **on ANY model, fluid or otherwise** …
>
> **lifted by:** never — unless a namable **FOURTH space/basis** this repository has not yet tried
> is proposed, with its own scoping leg establishing it is not subject to the same
> three-realization death

### The object whose status is in question

A **Zgliczyński-style Galerkin-plus-tail dynamical closure**: self-consistent a-priori bounds on a
finite Galerkin block plus a rigorously enclosed tail, propagated along a trajectory — the apparatus
`arXiv:1902.00384` uses to certify a periodic orbit of 3D Navier–Stokes on `T³` with the viscous term
inside the certified equation (leg 348 §3). It is a **dynamical closure**, not a
Newton–Kantorovich contraction in a function space.

### READING C1 — the ban's text names an APPARATUS

**From the ban's own text:**

1. **The subject noun is "machinery"**, qualified by *"ell^1-Fourier/radii-polynomial"*.
   "Radii-polynomial" is not a space; it is the specific `Y₀/Z₀/Z₁/Z₂` contraction apparatus.
2. **The ban individuates its object by "three realizations", and all three are NK/CAP-in-a-
   function-space realizations** — ℓ¹_w coefficient basis (leg 54), collocation (leg 56),
   origin-`H²`/Mellin (legs 163/176). A dynamical Galerkin-plus-tail closure is not among them and
   has never been attempted in this repository at all.
3. **The generality clause the ban review actually wrote is a MODEL clause** — *"on ANY model, fluid
   or otherwise"*. It widens across models and is silent about apparatus. The sentence that widened
   the ban is the place apparatus-generality would have been written.

**From the measurement the ban records:**

4. **Theorem NGX states its exclusion in apparatus terms.**
   `writeup/4_p2_lottery/TECHNICAL_P2_ROUTENGX_V1.md:156-157`: *"What Theorem NGX excludes is a
   **single bounded `A` working uniformly in `M`**, which is the only sense the radii-polynomial
   method has."* A Galerkin-plus-tail closure does not construct a single bounded approximate
   inverse uniform in `M`; on this reading NGX's quantity is not defined for it.
5. **The landed record already draws the distinction, in a leg that was not trying to open a lane.**
   Leg 348 §4 (`experiments/journal/leg_348.md:104-105`) lists leg 341's three-realization death as
   *"suggestive but not direct … different apparatus (NK fixed-point contraction vs. Galerkin-tail
   dynamical closure)"*.
6. **Practice, offered as weak evidence and labelled as such.** Legs 374, 376 and 377 were run
   explicitly *for* the Galerkin-plus-tail bridge (leg 374's own framing: *"route 4's
   Galerkin-plus-tail bridge (leg 348's own four named asks)"*, `experiments/journal/leg_377.md:8-9`)
   and none treated this ban as blocking them. They were reading legs, and reading legs do not touch
   bans, so this is practice, **not** authority.

**IF C1 IS THE RULING — what becomes available, stated and NOT exercised.** The **2026-08-11 scoping
precedent** (the DSS expensive-entrance ban) is available **in shape**: read the ban's own text,
identify an object it does not name, and open that lane while the measurement stays true. The
precedent's own recorded shape, quoted so the user can see what would be being invoked:

> *"the ban's object, in its own text above, is a search with NO FIXED POINT NEARBY TO SEED IT. A
> SEEDED search … is outside the ban … Any leg claiming this scope MUST NAME ITS SEED in its own
> pre-registration … ABSENT A NAMED SEED, THIS BAN APPLIES IN FULL … Two reasons this is a scope
> ruling and not a lift: lifting would also release the unseeded trawl leg 260 genuinely killed;
> and clause (a) below can no longer be met on leg 260's own answer."*

**AVAILABILITY IS NOT EXERCISE. This packet records that the precedent is available in shape and
DOES NOT EXERCISE IT.** No scope is claimed, no ban is narrowed, no lane is opened. Lane T stays
blocked until the user rules. Per the dispatch's pre-committed reading, that recording is the
entire content of this branch.

### READING C2 — the ban's text names a CONCLUSION (a certificate for this object class)

**From the ban's own text:**

1. **Half the ban's own name is a SPACE.** *"ell^1-Fourier"* is a space, not an apparatus. If the
   space is the binding half, any apparatus that truncates in a Fourier/coefficient space and
   controls a tail inherits the measurement.
2. **The lift clause is SPACE-indexed:** *"unless a namable **FOURTH space/basis** … is proposed,
   with its own scoping leg establishing it is not subject to the same three-realization death."* A
   lift condition that asks for a fourth space is congruent with a ban whose subject is the space.
   Under C1 the ban and its own lift clause would be indexed on **different axes** — which is a cost
   C1 has to carry.
3. **The ban review's drafting instinct on display was widening, not narrowing** — it replaced a
   model-specific precondition with *"on ANY model, fluid or otherwise."*

**From the measurement the ban records:**

4. **Theorem NGX's own summary is space-indexed.** `TECHNICAL_P2_ROUTENGX_V1.md:196-199`: *"The
   obstruction is a property of the **certificate's space**, not of the `a = 0` CLM linearisation.
   The radii-polynomial method needs weighted `ℓ¹` of Fourier coefficients in order to control its
   tail; in that space, at every `s < 1`, this operator is not bounded below, and no bounded
   approximate inverse exists at all."* `WALLS.md` W6 restates it: *"The obstruction is the
   certificate's **space**, not the operator."*
5. **The quantitative content is about a truncated block, which every Galerkin scheme must invert.**
   `σ_min(L_M) = c_s M^{−(1−s)} → 0` (Theorem NGX). A Galerkin-plus-tail closure also needs its
   finite block invertible and its tail summable in some space.
6. **The only leg that has ever worked this lift clause read it as space-indexed.** Leg 341
   (Route-ALGW, *"THE FOURTH SPACE"*): *"Does the algebraically weighted space … escape the stage-V
   ban's three-realization death, and does the CAP apparatus (radii-polynomial `Y`/`Z0`/`Z1`/`Z2`)
   have a coherent formulation in it?"* (`:3-6`) → *"**DIES** … the weight question does not escape,
   **no lift-condition packet exists to cite**"* (`:113`, `:216-218`).

**IF C2 IS THE RULING — reported plainly and not softened, per the pre-committed reading.**
**`T3` and `T4` are inside the ban whatever the apparatus, and Lane T is blocked on a LIFT, not a
SCOPE.** That is a **materially worse position** than a scope, and the record says why:

- A lift requires *a namable fourth space/basis … with its own scoping leg establishing it is not
  subject to the same three-realization death.* The one leg that attempted that answered **DIES**
  and closed leg 334's clause (a) **CLOSED-NO** (leg 341 `:216-218`).
- Leg 374's inventory against the bridge's four named asks reports: *"**No row publishes a result
  meeting all four of the bridge's asks simultaneously.** Every genuinely spectral candidate located
  is 1D/scalar in its published form — no `R³` or vector/Leray-projected extension was located for
  any of them"* (`experiments/journal/leg_374.md:74-76`). *(Note: `STATE.md` and `WALLS.md` compress
  this to "Hermite sole survivor". Leg 374 does not make that claim; this packet uses leg 374's own
  wording, and flags the compression rather than propagating it.)*
- Leg 376 measured both the `ℓ=1` and `ℓ=2` channels of the rescaled operator
  `-Δ + (1/2)(y·∇) + 1` as **continuous** (`experiments/journal/leg_376.md:10-14`) — no discrete
  spectral anchors on `ℝ³`.
- **`T4` would be inside the ban too**, on this reading — Lane T could not reproduce a published
  certificate without a lift. The record carries a directly relevant precedent the user should weigh:
  **leg 316 reproduced Dahne–Figueras (arXiv:2410.05480) row-for-row while this ban was in force**,
  and cleared it by individuating on the three realizations — *"it never touches
  `HL_S2_nonsymmetric`, `ℓ¹_w`, collocation, or origin-`H²`"* (`writeup/novelty/leg_316.md:50-51`).
  Whether that clearance extends to `T4` is a further question this packet does not answer.

### THE LIFT-CLAUSE MISMATCH — surfaced as part of the defect, and NOT resolved

Per the pre-committed reading, and stated here because it is a defect in its own right:

**The lift clause reads *"a namable FOURTH space/basis"*. What Lane T holds is a fourth APPARATUS.
A fourth apparatus is not literally a fourth space or basis.** `WALLS.md` W6 says so in terms:
*"The live candidate is not a fourth **weight** at all — it is a fourth **apparatus**: Zgliczyński-
style self-consistent bounds / Galerkin-plus-tail, which is a *dynamical closure* rather than a
Newton–Kantorovich contraction in a function space."*

- Under **C1** the mismatch is harmless: no lift is needed, because the ban does not reach the
  apparatus.
- Under **C2** the mismatch is **disabling, in the same shape as item (b)**: the lift condition
  names an object (a fourth space/basis) that is not the object the lane holds (a fourth apparatus).
  Lane T would then hold a candidate its own lift clause cannot receive — a lift condition that is
  unmeetable not because the work is hard but because it names the wrong kind of thing.

**An entailed sub-question the user may need to rule alongside (c), flagged and NOT answered here:**
under C2, is `T³`'s **discrete Fourier basis** — compact domain, exponential decay, none of the three
dead realizations — itself *"a namable FOURTH space/basis this repository has not yet tried"*? Under
C2 that is the only door Lane T has; under C1 it is moot. **This packet takes no position on it**, and
notes only that answering it would require its own scoping leg, exactly as the clause says.

### Why neither reading can be settled from the measurement

**Theorem NGX never varied the apparatus.** Its own contrast is *space versus operator* — *"a
property of the certificate's space, **not of the `a = 0` CLM linearisation**"* — and its object is
the assembled bordered `a = 0` CLM steady linearisation in the compactified odd-sine coefficient
basis. Apparatus is not a variable the measurement moved. **So neither C1 nor C2 can claim the
measurement settles it**, and that is precisely why this is a wording question and not a
measurement question. §3h rule 1 puts it with the user.

---

## (d) THE OUTREACH HOLD NOW SITS ON LANE T'S CRITICAL PATH

Not a ban-wording question. Raised here, as instructed, rather than routed around.

Leg 390 §4 (`experiments/journal/leg_390.md:113-117`), verbatim:

> (D)'s **data** conditions **(8)** and **(9)** are not in this repository (leg 381 banked
> (4),(5),(6),(7),(10),(11),(A),(C),(D) and not (8),(9)), and this leg has no outreach — so no claim
> about them is supportable here, and `CLAY_OBLIGATIONS.md`'s "(D) carries no decay condition" needs
> narrowing to (D)'s **solution** conditions until a leg with outreach reads (8),(9).

**No external outreach is authorised** — a standing user hold. Lane T's whole target is Fefferman
statement **(D)**, and two of (D)'s own conditions cannot be read verbatim under the hold. The
consequence is concrete and not hypothetical: every Lane T claim about what (D) accepts carries an
unread-condition caveat, and leg 390 §5 item 1 records that *"if (8) or (9) carries a data-side decay
or regularity requirement, the §4 disposition may change"* — i.e. `W4`'s pricing of the torus
alternative could move.

**What the user is being asked:** whether to lift the hold for this one read, to accept the narrowing
indefinitely and have Lane T carry the caveat in every artefact, or to name a non-outreach route to
(8) and (9). **This packet knows of no non-outreach route** and does not propose one. Lane T's `T2`
unit is separately instructed to report this rather than route around it; this is the same item, and
it is stated once here so the user sees all four decisions together.

---

## What this packet did not do

- **It ruled none of (a), (b), (c).** No reading is endorsed, preferred, ranked, or recommended.
- **It did not exercise the 2026-08-11 scoping precedent** on the ℓ¹-Fourier ban. Under reading C1
  the precedent is available *in shape*; availability is recorded, exercise is refused.
- **It did not touch `plan_of_record.py`.** `git diff origin/main -- plan_of_record.py` is empty.
- **It did not edit `STATE.md`, `WALLS.md`, or `DIRECTION.md`** — all Conductor-owned.
- **It did not read `DIRECTION.md`.** `DIRECTION.md` carries text bearing on item (b) at lines
  **755, 2262, 2275, 9798, 9997** (located by grep for the phrase, not read). They are named here as
  **unread artefacts**; a user or Conductor pass with authority to read that file should check them
  before ruling (b), and this packet's item (b) is stated without them.
- **It made no external outreach.**
- **It built nothing, ran nothing, and moved no link of the `L1 → L4` chain.** Preparing an
  escalation is choosing what to ask. **Tier 2 ceiling; Clay odds ~0.05%, unmoved.**

## Until the user rules

Every one of the 19 bans stands **in force, unchanged**, exactly as the Cadiot annotation already
records for its own entry. **`BUILD NOTHING IN LANE T` — that includes `T3` and `T4`.** Lane V's
`V1` is blocked on (b) for its wording half; its target-selection half needs no ruling.
