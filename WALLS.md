# WALLS — the blockers between here and a Clay answer, and what attacking each one means

**Adopted 2026-08-13 by user ruling: a full Clay solve is the driving objective, and the walls
are the work.** This file exists because "break through the walls" is not actionable until each
wall is stated as a proposition, its evidence is separated from its assumption, and a
*pre-committed* test says what breaking it would consist of. Ambition without that turns into
prose that claims movement no measurement supports — the one failure mode this repository has
spent 390 legs building defences against.

**Read this with `CLAY_OBLIGATIONS.md`.** That file says what a Tier-2 candidate owes. This file
says what stands between us and being able to pay.

---

## 0. The distinction that makes attacking walls safe

A wall is not a ban and a ban is not a wall.

- **A wall** is a gap in what anyone knows how to do. Walls are attacked. Every one of them is
  in scope, and no wall in this file is closed on the grounds that it is hard.
- **A ban** is a record of something *this repository measured dead*, with the measurement
  named. `plan_of_record.py` holds 19 of them.

**A ban is superseded by a new measurement, never by a decision.** This is not caution, it is
arithmetic: legs 51–56, 126, 260, 341 and 349 each cost real time and each ended in a number.
Re-walking a lane because the goal got more ambitious spends that time again and returns the same
number. **The revolutionary act is to attack the wall the ban is evidence about — in a lane the
measurement does not cover — not to repeal the measurement.**

Concretely, the pattern to copy is the **DSS expensive-entrance ban**: it was not lifted. It was
*scoped* (user ruling, 2026-08-11) by observing that its own text names an **unseeded** trawl,
and that a **seeded** search is a different object. The measurement stayed true, the lane opened,
and `PROG-R4` exists because of it. Do that again, four more times, and the board looks different.

**What is NOT permitted, under any reading of "be revolutionary":** describing output as movement
toward Clay when no link of the `L1 → L4` chain moved; softening the three-tier win condition;
calling Tier 2 a proof; retiring a planted control because it keeps firing.

---

## W1 — A search can only ever argue *for* blow-up

**Statement.** Any method of this class produces evidence for singularity formation and can never
establish global regularity. Direction (a) of the Clay problem is closed to us — and closed on a
theorem, not on effort: Tao's averaged-Navier–Stokes supercriticality barrier shows energy methods
plus the preserved algebraic structure are provably insufficient.

**Status: NOT A TARGET.** This is a scope statement, correctly handled, and it is recorded here
only so that no one re-discovers it as news. It costs us one of the two Clay directions and
nothing else.

**Attack:** none. Do not spend on it.

---

## W2 — No certificate has ever supplied its own three-dimensionality

**Statement.** Every published work stating a 3D singularity theorem *with* a certificate obtains
the 3D-ness from somewhere other than the certificate — a 2D reduction (Chen–Hou) or a
spherically-symmetric ODE profile (BCG → CGSS). No certificate has ever certified a genuinely
three-dimensional, genuinely time-dependent object by itself.

**What is measured, and what is assumed.** Measured: the census, and leg 172's correction of the
naive form of this wall (spatial dimension is *not* the barrier — van den Berg–Williams certified
genuinely 3D Ohta–Kawasaki stationary states in 2019). Assumed: nothing. This is a statement about
the literature as read, and absence of an instance is not a theorem of impossibility.

**The crack — RETRACTED 2026-08-14 BY MEASUREMENT (leg 393 / `T4`, landed `2c87244`).** The
superseded text is kept inline below, struck, because this wall's history is the point:

> ~~**The crack.** Leg 348 located `arXiv:1902.00384` — **a certified periodic orbit of 3D
> Navier–Stokes with the viscous term inside the certified equation, on the three-torus.** That is
> natively 3D, natively time-dependent, genuinely viscous, genuinely fluid. It is not a blow-up, so
> it does not fill leg 174's Grade-A/fluid **blow-up** cell — but it means the *technology* clears
> W2's bar already, and only the *target* is missing.~~

**THERE IS NO CRACK. `arXiv:1902.00384` FAILS THIS WALL'S OWN PRE-COMMITTED TEST**, which requires
showing *"the certified object is not a lift of a lower-dimensional one."* **Both certified rows are
2D lifts.** Measured from the authors' own published data package, not from prose: `N_x3 = 0` in
Table 1 and in the package's `Nrec`; the decoded coefficient arrays have **extent 1** in `x₃`;
`max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` **exactly** while `max|ω⁽³⁾| = 1.6351 / 1.5274`, so the
zeros are structure and not an empty array; the `setup` field reads `'2D'`. The authors say why:
the memory cost of a three-dimensional solution is *"for now, prohibitive."*

**The technology does NOT clear W2's bar, and the target was never the only thing missing.** Leg 348
read this paper **at abstract level only** and flagged that limit itself; the full text contradicts
its classification on this wall's most load-bearing clause.

**Second finding, separate and also adverse:** the paper is certified by **exactly the banned
apparatus** — a Newton–Kantorovich radii-polynomial contraction in a weighted `ℓ¹_η` Fourier space
built on **one bounded approximate inverse** `A : X_{−2,−1} → X`. This is visible **in the abstract**
(*"a Newton-Kantorovich theorem is applied"*, on *"a Banach space of geometrically decaying Fourier
coefficients"*), independently confirmed by the Conductor at the landing of `2c87244`. **Ruling C1's
general proposition is untouched — a Galerkin-plus-tail dynamical closure remains a different
apparatus — but its EXEMPLAR falls.** **RULED 2026-08-14 (`RULING_C1_EXEMPLAR_2026-08-14.md`, the
escalation DISCHARGED): C1 needs NO replacement exemplar and STANDS EXEMPLAR-FREE** — it is an
apparatus scoping and its proposition is true independent of any instance. **What the ruling
removes is the implied *"and this has been demonstrated"*: no unit may cite C1 as evidence the
technology closes for any object class.**

**W2 STANDS, AND IS STRENGTHENED**: the one instance the programme believed cleared it does not.

**BREAKING W2 CONSISTS OF:** a certificate whose three-dimensionality and whose time-dependence
both come from the certified object itself, for a dissipative fluid equation. Not a 2D reduction
carried up. Not an ODE profile. Pre-committed test: name the certified equation, show the viscous
term is inside it, and show the certified object is not a lift of a lower-dimensional one.

**Lane: T** (below) — **DEFERRED 2026-08-14.** A **demonstrated, genuinely-3D closure meeting this
wall's own pre-committed test** is re-open condition **(i)** for that lane (`OPTIONS.md` §E). The
credit stays unclaimed; deferring the lane neither collects it nor concedes it.

---

## W3 — The Grade-A × fluid cell is empty

**Statement.** No certified (interval-arithmetic-enclosed, equation-carrying-the-dissipative-term)
blow-up exists for any *fluid* equation, in any dimension. Leg 174's occupancy matrix; leg 242
confirms nobody filled it since.

**What is measured, and what is assumed.** Measured: the cell is empty, and it is empty **"for
want of a target, not a method"** — leg 174's own words. Grade-A dissipative certification exists
off the fluid axis (Dahne–Figueras CGL `arXiv:2410.05480`, reproduced row-for-row by leg 316;
Breden–Chu viscous Burgers). Assumed: nothing — and note the **corrected** width, over-read
closure #5, leg 328: the wider claim "no certified viscous blow-up in any model in any dimension"
was **FALSE** and is retired.

**Why this wall matters more than its size suggests.** It is the rung that decides whether Tier 3
is reachable *in principle*. If a viscous blow-up cannot be certified for a dissipative fluid
equation in **one** dimension, then 3D Navier–Stokes is not a question of compute and the honest
ceiling of the whole programme is Tier 2. The information is worth as much on the negative branch
as on the positive one, which is what makes it cheap.

**BREAKING W3 CONSISTS OF:** an interval-arithmetic enclosure of a blow-up solution of a
dissipative *fluid* equation — any dimension, any model, provided the dissipative term is inside
the certified equation and the object is a genuine finite-time singularity. Pre-committed test:
leg 174's own Grade-A criterion, applied unchanged.

**Lane: V** (below) — **PRIORITY LANE, ACTIVE 2026-08-14.**

---

## W4 — Finite energy: the localisation problem

**Statement.** A discretely-self-similar profile on `ℝ³` has infinite global energy. Clay
condition (7) demands bounded energy. Converting one into the other — cutting the profile off and
showing the cut solution still blows up — has **no known method**, here or anywhere.

**What is measured.** Leg 381's cutoff bill: the critical `L³` tail runs at **326.875 per decade**
(the increment of the *cube*; the norm itself runs 8.679 → 14.841), and the required decay exponent
is `α > 1.5` against an a-priori `α = 1.0`, a deficit of 0.5. Leg 390 priced the torus alternative:
`α > 2.996995` to wrap the uncut profile, deficit 1.996995 — **3.99399× worse** — but **0.0 if the
profile is cut first** (disjoint supports at `L > 2ρ`), in which case leg 381's bill is inherited
unchanged. Conclusion in leg 390's own words: **"(D) deletes the acceptance test, not the work."**

**BREAKING W4 CONSISTS OF:** either (a) a localisation argument that carries blow-up from the
infinite-energy profile to a finite-energy solution with the decay actually available, or (b) an
ansatz that is natively finite-energy, or (c) a target for which condition (7) is not imposed —
which is Fefferman statement **(D)**, the torus.

**Lanes: T and L** (below) — **L is a PRIORITY LANE, ACTIVE 2026-08-14; T is DEFERRED.** W4's
attack (c), the torus, is deferred with Lane T; attacks (a) and (b) live in Lane L and run now.

---

## W5 — Persistence and stability under localisation

**Statement.** Even granted W4's cutoff, the cut solution must still be shown to blow up. No known
method. `CLAY_OBLIGATIONS.md` §6(ii).

**Status: DOWNSTREAM — but its LITERATURE is not.** Nothing to *build* here until W4 has a shape,
and it is recorded so it is not forgotten when W4 moves and someone declares victory one obligation
early. **Amended 2026-08-14:** downstream in logic is not downstream in reading. The published
nonlinear-stability-with-finite-unstable-spectrum technique (the Chen–Hou line) has **never been
read against this object**, and `L3′` reads it in wave 3. **A reading is not an attack on the wall
and does not move it** — it establishes whether a method exists to attack it with.

---

## W6 — The certificate's function space (Theorem NGX)

**Statement.** `Z₁ ≥ 1` for every bounded approximate inverse `A`; `σ_min(L) ∼ M^−(1−s)`. The
obstruction is the certificate's **space**, not the operator. Three independent realizations of the
ℓ¹-Fourier / radii-polynomial machinery are dead here (ℓ¹_w coefficient basis, leg 54; collocation,
leg 56; origin-`H²`/Mellin, legs 163/176), and leg 341 killed the algebraically-weighted space in
three further lanes.

**The ban's own lift condition names the attack:** *"unless a namable **FOURTH** space/basis this
repository has not yet tried is proposed, with its own scoping leg establishing it is not subject
to the same three-realization death."* That clause is an invitation, not a closure.

**What is already known about the fourth space.** It is **not** the algebraic weight (leg 341, three
lanes, dead). Leg 374 left **Hermite as the sole surviving basis**, with its decay concern cleared
by leg 377; leg 376 found **no discrete spectral anchors**, both channels continuous. The live
candidate is not a fourth *weight* at all — it is a fourth **apparatus**: Zgliczyński-style
self-consistent bounds / Galerkin-plus-tail, which is a *dynamical closure* rather than a
Newton–Kantorovich contraction in a function space, and which leg 348 explicitly flagged as
possibly outside the ban's subject ("a **different** apparatus … I make no claim about whether that
apparatus distinction matters to the ban's scope; that reading is for the DM/user").

~~**THAT READING IS NOW REQUIRED WORK, and it is the first thing Lane T must settle.**~~ **RULED C1
BY THE USER 2026-08-13, and the ruling STANDS EXEMPLAR-FREE after 2026-08-14:** the ban names an
apparatus, and a Galerkin-plus-tail dynamical closure is outside its object. **But C1 is a statement
about the ban's SCOPE, not about any apparatus having WORKED** — no unit may cite it as evidence the
technology closes for any object class, and the exemplar the record once had for that claim
(`arXiv:1902.00384`) is certified by exactly the banned apparatus. **W6 is unbroken, and the fourth
apparatus is a candidate, not a result.**

**BREAKING W6 CONSISTS OF:** a named certificate framework, run to a `Y₀/Z₀/Z₁/Z₂`-equivalent
closure (or its analogue in the framework's own terms) on route 4's object class, with `Z₁ < 1`
achieved — or the framework's own contraction criterion met, if it does not use radii-polynomial
bounds at all.

**Lane: T — DEFERRED 2026-08-14.** W6 is unbroken and stays unbroken; the fourth *apparatus* is a
candidate, not a result, and C1 may not be cited as evidence it closes.

---

## W7 — Compute

**Statement.** `ORCHESTRATION.md` §3d says a stop fires only on a null from an attempt resourced at
the scale the question is posed at. `PROG-R4` U3 spent **134.45 core-hours of attempt CPU** (convention label added 2026-08-13 by R0; the same run reserved **144.69** worker-hours of pool, 92.92% utilised — both are real measurements of different quantities, see §R0); the source papers use
**~10.2 GPU-days** for the *2D* problem, and `PROG-R4`'s own pre-registration records that the
literature-scale escalation "is GPU-dependent in the source papers' own hands and this repository
does not currently have that compute."

**Why it is a wall and not a complaint.** Under §3d, an unresourced programme cannot return `NO`.
It returns `UNDER-RESOURCED` forever. A search side that never reaches compliant scale produces an
unbounded sequence of honest non-answers, which is indistinguishable from no programme at all.

**BREAKING W7 CONSISTS OF:** either compute at the sources' own scale, or — and this is the
cheaper attack, and it is mathematics not procurement — **a reformulation whose compliant scale is
smaller.** Every order of magnitude taken out of the required resourcing is worth more than an
order of magnitude of hardware, because it is permanent.

**Lane: R.**

---

# THE FOUR LANES

Each lane attacks named walls. Each is authorised to build whatever it needs. None may claim a
Clay link moved without the link moving.

## ⚠ LANE PRIORITIES — RE-RANKED 2026-08-14 BY USER RULING

**`writeup/escalations/RULING_C1_EXEMPLAR_2026-08-14.md`.** The 2026-08-13 ranking is superseded
**as a ranking**; every measurement it rested on stands.

| lane | 2026-08-13 | **2026-08-14** | why |
|---|---|---|---|
| **V** | priority 2 | **PRIORITY, ACTIVE** | **It decides whether any path exists.** W3 is the rung that determines whether **Tier 3 is reachable in principle**, and both branches are valuable. |
| **L** | priority 3 | **PRIORITY, ACTIVE** | **It is on every path.** Leg 390 measured that the torus does **not** retire `CLAY_OBLIGATIONS.md` §6(i)/(ii), so the two no-method obligations are the last blockers on **every** branch — and **no unit in 395 legs has attacked either.** |
| **T** | priority 1 | **DEFERRED** | The demonstrated-technology argument fell to the lane's **own** measurement (leg 393, replicated by leg 394). Kept alive only through **`T2″`**; **`T3` is deferred with the lane, not killed.** Cost and the two re-open conditions: `OPTIONS.md` §E. |
| **R** | continuous | **continuous, unchanged** | Runs inside **every** unit's pre-registration (*what makes this answerable an order of magnitude cheaper?*) and takes its own units when a wave has room. |

**Two byproducts of wave 2 point at V and L, and neither was found by looking for them:** `T5`'s
`O1` (leg 315's Taylor-model flow-map, *"needs **no function space**"*) points at **Lane V**, and
`T6`'s Chen–Hou near-miss (`arXiv:2308.01528` — computer-assisted blow-up, **unbounded** domain,
**>1D**, **algebraic decay**) points at **Lane L** and at route 4's actual `ℝ³` geometry, prize
statement **(C)**.

**Binding on every lane: C1 STANDS, EXEMPLAR-FREE.** The scope no longer carries any implied *"and
this has been demonstrated"* — **no unit may cite C1 as evidence the technology closes for any
object class.** Its **naming requirement is unchanged**: name the apparatus with a citation, and
show it constructs no single bounded approximate inverse uniform in `M`. **Absent both, the ban
applies in full**, and the Conductor may not waive it.

## LANE T — THE TORUS LANE. ~~*Priority 1. This is the breakthrough candidate.*~~ **DEFERRED 2026-08-14.**

> **DEFERRED BY USER RULING 2026-08-14**, on the lane's own measurement. **Not killed, and nothing it
> measured is superseded.** `T3` is deferred **with** the lane; `T2″` is what keeps the lane alive and
> is re-open condition 2. The full cost of deferring, and both re-open conditions, are recorded in
> **`OPTIONS.md` §E** — read that before re-opening anything here. The lane text below is retained as
> written, because the price paragraphs are still the live statement of what this lane would cost.

**Attacks W2, W4, W6 simultaneously.** It is first because it is the only lane where four
independently-measured repository results line up in the same direction, and **no leg has ever put
them side by side** — each one was explicitly out of scope for the leg that found it.

The four results:

1. **Leg 348 (POCP), gate (ii) OPEN-AND-REACHABLE, cost class C.** The *only* named obstruction to
   periodic-orbit certification reaching route 4's object is **domain shape**: the
   Galerkin-plus-tail bridge closes against a **compact domain with a discrete,
   geometrically/exponentially decaying spectral basis**, and route 4 wants an unbounded `ℝ³` in an
   algebraic weight, which excludes the Gaussian weight that would supply the discrete basis. Leg
   348 adjudicated (not transcribed) that leg 315's PDE-type blocker **does not transfer** — the
   rescaled Navier–Stokes system is genuinely parabolic.
2. **`T³` is exactly the domain the obstruction asks for.** Compact, discrete Fourier basis,
   exponential decay. Leg 390's census: **6 compact/periodic instances, 0 unbounded.**
   **⚠ THE CENSUS COUNT IS WRONG AS OF 2026-08-14 — leg 394 / `T6` (`e7db624`), and the GROUND is
   corrected here 2026-08-14 by `V-W2`, whose finding was against the Conductor's wording, not
   against `T6`.** At full text, **`arXiv:2409.09234` does not belong in leg 348's `domain_census`**,
   and **the record's own ground is the FIRST clause below, not the second** — this file and the
   dispatch that quoted it had the two the wrong way round:
   **(i) PRIMARY — it is not an instance of the technology at all.** `T6`, verbatim: *"THIS PAPER
   CLOSES NO TAIL-DOMINATION ESTIMATE AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL. The census
   over-counts by one."* Its rigorous content is a theorem about a **1-D map fitted to DNS data** —
   no interval arithmetic, no Galerkin projection, no tail-domination estimate, no
   Newton–Kantorovich argument anywhere in it (`V-W2` re-measured all five term counts at **0**).
   **(ii) SECONDARY, and it is `T6`'s own `u_code` U1** — the domain is **not a pure periodic cell**.
   *(Superseded wording, struck: ~~"its domain carries no-slip walls, not periodicity"~~. `V-W2`
   measured that the paper **never uses the phrase "no-slip"** — 0 occurrences. What it states is a
   **moving-wall Dirichlet condition**, *"the boundary conditions at the inner and outer cylinder
   walls `r = r_i` and `r = r_o` are `v = R_i θ̂` and `v = R_o θ̂`. Periodicity is enforced to the
   rest of boundaries of the parallelogram domain"* (§2, p.4). That **is** no-slip on a rotating
   cylinder, but the compression dropped "to the rest of boundaries", which is the substance.)*
   **The count is unchanged: 6 entries − 1 = 5**, and `V-W2` reproduced the arithmetic and both
   grounds independently from a re-fetched PDF whose SHA-256 matches the banked digest. The authors:
   *"our results, depending on numerical approximations, do not guarantee that the Navier-Stokes
   solutions exhibit chaotic behaviour in the sense of Devaney."* **Leg 348's census over-counts by
   one, and leg 390's figure inherits from it. Re-check before citing this count again.** The
   direction of the correction does not threaten item 2 — the removed instance was compact-domain
   only by miscount — but the number is wrong and is not to be repeated as read.
3. ~~**`arXiv:1902.00384` already certifies a periodic orbit of 3D Navier–Stokes on `T³` with the
   viscous term inside the certified equation.** The technology closes there, demonstrated, for
   exactly our equation.~~ **RETRACTED 2026-08-14 by leg 393 / `T4` (`2c87244`). Both certified rows
   are 2D LIFTS** (`N_x3 = 0`, decoded extent 1 in `x₃`, `max|u⁽³⁾| = 0.0` exactly, `setup = '2D'`);
   the authors call a 3D solution's memory cost *"for now, prohibitive."* The technology is **not**
   demonstrated to close for a genuinely 3D object. It is also certified by **exactly the banned
   apparatus** (Newton–Kantorovich radii-polynomial, one bounded approximate inverse), which the
   abstract itself states. **This item can no longer carry weight in this argument.** See W2.
4. **Leg 390: statement (D) vacates §4 as an acceptance test**, and leg 390's own §5 item 4 says
   in terms: ***"§1's POCP credit is unclaimed. Whether any non-DSS torus blow-up ansatz could
   collect that credit is outside this leg's scope entirely."***

**The price, stated first, because free lunches here get repurchased.**
- **0 of 4 rigidity clearances carry to `T³`** (leg 390, machine-applied domain-marker rule). The
  §2 screen must be rebuilt from scratch. **Searched 2026-08-13 by T2 / leg 392 — see below.**
- **THE CONVERSE, WHICH THIS FILE WAS MISSING AND WHICH IS LOAD-BEARING** (routed by T2, applied
  2026-08-13). "0 of 4 clearances carry to `T³`" says the `ℝ³` screen does not *help* on the torus.
  It does **not** say the `ℝ³` *exclusions* stop applying — **and they do not. An `ℝ³` exclusion
  still reaches a `T³` object built by periodic extension of an `ℝ³` self-similar core.** This is
  not hypothetical: `2604.09949` was read at **full text** by leg 309 and reached **GATE NO, broken
  at H11**, on exactly that ground — its `T³` object is a periodized `ℝ³` **backward self-similar**
  core, killed by the very NRS/Tsai row whose periodic analogue leg 392 went looking for. **The one
  previous attempt at Lane T's target, by anyone, died this way.** So the torus does not buy an
  escape from `ℝ³` rigidity *by construction*; it buys one only for an ansatz that is **natively
  periodic**, which compounds with the item below.
- **NO PERIODIC ANALOGUE OF NRS/TSAI WAS LOCATED — and that is NOT a clearance** (leg 392, gate
  returned `UNDER-RESOURCED` under §3d, not `no`). Coverage holes, stated: NRS 1996 (Acta Math.) and
  Tsai 1998 (ARMA) are **pre-arXiv** and were declared unreachable in advance; Semantic Scholar, the
  instrument for exactly that gap, was **throttled on 5 of 6** substantive queries; and one battery
  **failed its own domain control** (`1304.7414` Chae–Tsai not re-found), so that row's null is
  under-resourced by the leg's own rule. arXiv coverage was clean — **32/32 MEASURED**, served
  namespace banked as 1.1 on every query, no throttled query recorded as a zero. **What DOES exist**
  are torus/periodic *global-regularity* theorems under scaling-invariant smallness / LPS hypotheses
  (`1909.09125`, `math/9811161`, `0710.1604`); they bite in shape but thinly, since every clause is
  somewhere a blow-up ansatz would already be. **Compliant search costed at ≈1.2–1.7 h plus one user
  ruling** (an S2 key, the battery repair, a forward-citation pass on NRS/Tsai, depth beyond top-8).
- **DE NOVO ITEM LANE T MUST ESTABLISH, named by leg 392: a TYPE-I RIGIDITY THEOREM ON `T³`.** A
  *rate* condition needs no dilation symmetry, so it carries to the torus intact **as a question**,
  and nothing located proves it. Row 1's object is **vacuous** on `T³` (no dilation action). Row 4's
  Morrey `sup_{R>0}` partly degenerates on a compact torus (recorded as an observation, not a
  result).
- **The DSS ansatz does not survive periodization.** 342 modes survive one DSS step at `λ = 1.7`;
  **0 survive two.** So Lane T needs a **non-DSS** blow-up ansatz on `T³`, and identifying one is
  open work, not a lookup.
- (D)'s data conditions **(8)** and **(9)** are not in this repository. **READABLE AS OF 2026-08-13 — the outreach hold was NARROWED to author contact only, and reading any published document is now authorised.** Fefferman's official problem description may be fetched and (8),(9) read verbatim; **leg 390 §5 item 1 owes the re-run of `check_A` against them, and the §4 disposition MAY CHANGE** if either carries a data-side decay or regularity requirement. Until that runs, the narrowing below stands. *(Superseded wording: they "require outreach to read
  verbatim (leg 390 §4). Until they are read, `CLAY_OBLIGATIONS.md`'s "(D) carries no decay
  condition" is narrowed to (D)'s **solution** conditions.

**Lane T's first four units, in order.**

- **T1 — the ban-scope reading, and it is a user escalation, not a leg's call.** Does the
  ℓ¹-Fourier/radii-polynomial ban reach a Galerkin-plus-tail *dynamical* closure? Leg 348 raised
  it and correctly refused to answer it. Nothing in Lane T may be built until this is ruled.
  **Escalate with the two readings and the evidence for each; do not rule it inside the lane.**
- **T2 — the periodic-rigidity literature search.** Never done. It decides whether a `T³` blow-up
  target is excluded by a published theorem before anything is built. Cheap, and it can kill the
  lane. Run it early *for that reason*.
- **T3 — the non-DSS `T³` ansatz.** The open mathematics. What structure can concentrate on a torus
  without an exact dilation symmetry? Leg 390 §5 item 3 already names the nearest priced object:
  the one-step DSS margin decays with band width at exponent **−0.99057**, so an
  *almost-periodic-almost-DSS* object is the first thing to price. This is genuinely new work and
  the lane's real content.
- **T4 — reproduce `arXiv:1902.00384`'s certificate**, row for row, the way leg 316 reproduced
  Dahne–Figueras. Until it is reproduced in this repository it is a citation, not a capability.

## LANE V — THE VISCOUS RUNG. **PRIORITY LANE, ACTIVE (user ruling 2026-08-14).** *Highest information per unit of spend.*

> **PROMOTED 2026-08-14.** The user's reason, in its own terms: **Lane V decides whether any path
> exists.** `V2` runs in wave 3 and is that wave's centre of gravity — it supplies the **named
> target** leg 174 says the cell is empty for want of, and opens the feasibility of a **C1-compliant**
> apparatus against it. **C1's naming requirement binds and is not waivable.**

**Attacks W3.** Fill the Grade-A × fluid cell in the lowest dimension that admits a genuine fluid
structure. Leg 174 says the cell is empty **for want of a target**, so the lane's first job is to
supply the target, not the method.

**Both branches are valuable, which is what makes this cheap:** success gives the Clay path a
certification mechanism; failure is the strongest available evidence that the ceiling is Tier 2,
and it is evidence the programme can act on rather than assume.

**Note the dead lift condition.** The stage-V ban's wording is *"unless the question is re-posed for
a FLUID transport model, which needs L1 first"* — and L1 has three dead attempts and no fourth
candidate, which makes that precondition unliftable **as written**. That is a wording defect of the
same shape as the Cadiot escalation already pending. **Lane V's first unit escalates the wording to
the user**; it does not read around it.

## LANE L — THE LAST OBLIGATIONS. **PRIORITY LANE, ACTIVE (user ruling 2026-08-14).** *The only lane that touches the FINAL blockers.*

> **PROMOTED 2026-08-14.** The user's reason, in its own terms: **Lane L is on every path.** `L2`
> (§6(i)) and `L3′` (the Chen–Hou reading, §6(ii)) run in wave 3 — **the first units ever dispatched
> at a final blocker.** Leg 381's banked bill is the object: critical `L³` tail **326.875 per
> decade**, required `α > 1.5` against available `α = 1.0`. **A deficit of 0.5 in a decay exponent is
> a number, not an impossibility.**

**Widened 2026-08-13.** This lane was drafted to price W4 on `ℝ³`. That is L1 below, and it is
still the right first unit — but the lane's real subject is larger and nothing in this repository
has ever attacked it.

**The gap this lane exists to close.** `CLAY_OBLIGATIONS.md` §6 names **two obligations with no
known method**, and they are the literal last things standing between a Tier-2 candidate and a
Clay answer:

- **§6(i)** — certified far-field decay together with an admissible cutoff.
- **§6(ii)** — persistence / stability of the blow-up under that localisation.

**Leg 390 checked whether the torus disposes of them and recorded that it does not:** §6's two
obligations stay **OPEN in both branches**, and (D)'s gain on §4 is *"the acceptance test, not the
work"* (`α > 2.996995` to wrap the uncut profile against §4's `α > 1.5`; 0.0 only if the profile is
cut first, which inherits leg 381's entire bill unchanged). **So Lane T does not retire them, Lane
V does not retire them, and Lane R does not touch them.** If every other lane succeeded completely,
these two would still be the answer to "why isn't this a Clay solve yet."

**Nobody here has ever spent a unit on either.** They have been carried as an assumption — "no
known method" — through 390 legs without being checked to the standard this repository applies to
everything else. That is the same defect `WALLS.md` was written to fix, and it sits on the most
load-bearing claim in the whole roadmap.

**L1 — price §4 on `ℝ³`.** Read the published attempts to localise a self-similar profile to finite
energy; state, per attempt, the **named hypothesis** that fails for DSS. Converts an assumption
into a measurement. It may also find the method — the claim has never been tested.

**L2 — attack §6(i).** Is certified far-field decay plus an admissible cutoff genuinely without
method, or without an *attempt*? Leg 381 banked the bill (`L³` tail 326.875 per decade, required
`α > 1.5` against available `α = 1.0`). A deficit of 0.5 in a decay exponent is a *number*, not an
impossibility — and no unit has ever asked what would supply it.

**L3 — attack §6(ii).** Persistence under localisation. Downstream of L2 in logic but not in
literature: the published techniques for persistence of singular behaviour under perturbation
(nonlinear stability with a finite unstable spectrum, as in the Chen–Hou line) have never been
read against *this* object.

**BREAKING EITHER OF §6's OBLIGATIONS IS THE SINGLE MOST VALUABLE OUTCOME AVAILABLE TO THIS
PROGRAMME** — more valuable than a Tier-2 candidate, because a candidate without them is what we
already know how to produce. **A measured, honest "still no method, and here is precisely which
hypothesis fails" is also a real result**, and it is the one that would tell the user whether the
Tier-2 ceiling is permanent.

## LANE R — REFORMULATION FOR SCALE, AND SOLVER COMPETITIVENESS. *Runs continuously, unchanged 2026-08-14.*

> **UNCHANGED BY THE 2026-08-14 RE-RANKING.** Lane R runs **continuously inside every unit's
> pre-registration** — *what would make this question answerable an order of magnitude cheaper?* — and
> takes its own units when a wave has room. `R1` is closed against itself; `R0` landed; `R2`–`R5`
> stay deferred in `OPTIONS.md` §B.

**Attacks W7 by mathematics and engineering rather than hardware.** Every unit in every lane asks,
as a standing question in its pre-registration: *what would make this question answerable an order
of magnitude cheaper?* `PROG-R4` U5's shift stratification is exactly this move — it buys compliant
scale by fixing a selection bias rather than by buying compute, and it is the second time (after
AMENDMENT 4's period stratification) that the same reformulation paid.

**Promoted 2026-08-13 by user ruling: raise the recovery rate until this repository's orbit-finding
machinery is the best in the field, not merely adequate.** This is not vanity. W7 says an
under-resourced programme returns `UNDER-RESOURCED` forever; every factor taken out of the cost of
an answer is permanent, transfers to Lane T's torus search unchanged, and is the difference between
a programme that can pose the compliant question and one that cannot.

### R0 — the metric, pre-committed BEFORE any optimisation

**Per-attempt convergence rate is the wrong headline and must not be the reported one.** It is
trivially inflated by feeding the solver easier seeds — which is precisely what U5 deliberately
stops doing — and it counts a re-find of a known orbit as a success. **U3's own numbers show the
problem: 14 convergences, but NINE of them landed on just three solutions** (cluster sizes 4+3+2,
leaving 5 singletons; 3+5 = 8 and the arithmetic closes). **Corrected from "10" 2026-08-13 by R0**,
measured under `p2_prog_r4_m3_evidence.py` §5's own rule and re-derived independently by the
Conductor before landing. R2's conclusion is unaffected — 9 of 14 is still the majority.

**The reported metric is `DISTINCT ORBITS PER CORE-HOUR`,** with per-attempt rate retained as a
secondary diagnostic and always alongside it.

**The baseline to beat, and R0 must reconcile it before anything is measured against it.**
U5 (2026-08-13) already found **two defects in the baseline as first written here**, which is
exactly why R0 exists:

- **Core-hours — RESOLVED 2026-08-13 by R0, and this file's framing was the thing that was wrong.**
  Both numbers are correct measurements of **different quantities**, and *neither came from prose*:
  **144.69** = `magnitudes.wall_seconds` × `workers` / 3600 (pool reservation) and **134.45** =
  `Σ attempts[].wall_seconds / 3600` (attempt CPU) — the latter straight from the same JSON, and
  already the figure U3's own `writeup/INDEX.md` row reports. The gap is U3's **92.92%** pool
  utilisation against U5's **98.20%**. This file's original instruction, *"reconcile against the
  JSON, not against prose"*, **mislabelled a real second measurement as a defect**; what these
  figures needed was a **convention label**, not a replacement. Standing convention: **pool
  reservation (`wall × workers`)**, stated as such wherever quoted. §W7's "U3 spent 134.45
  core-hours" is correct under the attempt-CPU convention and is labelled there rather than changed.
- **The denominator is WORKER-hours, not machine-core-hours** (U3 reserved 10, U5 reserved 8). The
  physical core count is in **no numeric field** of either JSON — it exists only inside the prose
  string `resourcing.workers_note`, which §3e forbids using as a number, and **R0 did not estimate
  it**. A future unit must bank `magnitudes.physical_cores` and per-attempt `time.process_time` to
  make a true core-hour figure derivable. Until then the honest axis label is **worker-hours**.
- **The distinct count.** This file first argued U3's 8 was unreconcilable with its §4 table
  (10 convergences over 3 replicated solutions, then 4 remaining cannot yield 5 more). **U5
  measured it instead of arguing it:** clustering U3's 14 convergences at the matching predicate's
  own 0.05 tolerance, with `s` wrapped to `(-π, π]`, **reproduces 8**
  (`experiments/p2_prog_r4_m3_evidence.py` §5). The table almost certainly lists only replicated
  rows. **R0 reconciles against that script, not against this paragraph** — and the lesson is the
  one this repository already knows: a count derived from prose is not a measurement.

**LANDED 2026-08-13 by R0. The count did NOT resolve down — U3 = 8, U5 = 5, confirmed** under the
arbiter's exact rule (greedy leader clustering on `(T_converged, wrap_abs(s))`, `TOL = 0.05`),
re-derived independently by the Conductor. Robust: greedy = single = complete linkage, invariant
over 20,000 orderings, stable for `TOL` 0.05–0.10.

| | distinct | worker-hours | **distinct / worker-hour** |
|---|---|---|---|
| U3 | 8 | 144.69 | 0.0553 |
| **U5** | **5** | **57.04** | **0.0877** |

**THE INFERENCE FROM THIS TABLE IS RETRACTED. This file previously read "U5 is above U3 on every
variant — Lane R's first measured improvement." That claim is WITHDRAWN.** The per-run arithmetic
(1.27×–1.59×) is confirmed and is not in dispute; **the inference from it is not supportable**,
because the metric counts **cross-run** re-finds as successes — the exact defect it was introduced
to remove, one level up. Measured by R0:

- **57 of U5's 100 seeds were already spent by U3** (matched on `(T_seed, s_seed, R_seed)`).
- **5 of U5's 9 convergences are bit-identical re-executions** of U3 attempts.
- **4 of U5's 5 distinct solutions are re-finds of U3's. U5's contribution NEW TO THE PROGRAMME IS ONE ORBIT.**
- On U5-only seeds the distinct count is **4, not 5**.

**Cumulative reading: U5 = 1 / 57.04 = 0.0175 against U3's 0.0553 — 3.15× WORSE.** Report **both**
rows from here on. **The standing cross-unit metric is `ORBITS NEW TO THE PROGRAMME PER
WORKER-HOUR`**; the per-run figure is retained as a within-unit diagnostic only.

**This does not by itself retract `MILESTONE M3 = DELIVERED`** — M3's gate was about the seed budget
being stratified by shift, which it was. But **57% seed overlap means U5's 9/100 against U3's 14/100
is partly a re-run rather than an independent comparison, and that bears on how M3 is read.** The
Conductor planned this wave and therefore **may not adjudicate it (§3f rule 1); the wave-2 verifier
is instructed to.**

**Instrument limit, recorded rather than glossed:** U3's converged states are **banked nowhere** —
only U5's are. The headline numerator 8 can therefore only ever be tested in the `(T, |s|)` pair,
and the pair that decides it sits at **1.288 × TOL**. U5's own `.npz` banks one snapshot per attempt
at an **unspecified orbital phase**, so it cannot validate the rule either (measured: a same-cluster
distance of 0.1992 exceeds a cross-cluster 0.0888). Settling it needs U3's 14 states plus a
phase-aligned distance — i.e. new compute — and **is not proposed here**.

### R1 — early abort on flatness. **CLOSED 2026-08-13 — the win was already collected, and R1 closes against itself.**

**This heading previously read *"Cheapest competitive win in the repository, and it is measured."*
That is withdrawn.** R1's own numbers below are **CONFIRMED exactly** — but the win they describe
**U5 had already collected**: `resourcing.stall_exit` in `p2_prog_r4_m3_v1.json` **is** this
criterion, deployed. Measured remaining headroom, over 12,597 deterministic rules (9,760
admissible), for the best rule that does not degrade the deployed safety margin: **+0.45 percentage
points = +0.48 worker-hours.** The 65%-recovery rules sit at a 1.09× margin and are rejected, and
**hold-out shows a rule selected on U5's 9 convergences KILLS one of U3's 14.** Deployed rule: 55.00%
of U3's 4,629 epochs (→ 2,083) = 74.87 of its 134.45 attempt-CPU hours, **zero false kills over 23
banked convergences, 6.90× safety margin. Spend no further compute on this family.** (Criterion is
three fixed constants and a residual comparison — deterministic, never touches seed selection, so
leg 349's ban is respected.)

U3 measured convergence as **bimodal**: all 14 convergences finished in **≤29 epochs** (median 16),
while the 86 non-convergences ran to the 52-epoch cap and were **flat there** — 53% reduced `‖R‖`
by <1% over their final 10 epochs, 83% by <10%, only 3% still halving. **Those epochs are pure
waste and they are the majority of the run.** A flatness criterion that kills an attempt and
recycles its budget into a fresh seed converts wasted compute directly into extra attempts, with no
change to the per-attempt rate and no change to the realization. Estimate the recoverable fraction
from U3's banked ledger *before* building it, and plant a control that the criterion never kills an
attempt that U3's ledger shows would have converged.

### R2 — deflation. *Attacks the largest measured waste after R1.*

**NINE** of U3's 14 convergences landed on three solutions (corrected from "10" 2026-08-13 by R0; still the majority, so R2's conclusion is unaffected). **U5 made this worse and made it
cross-unit: 4 of U5's 5 distinct solutions were already in U3's set, so a second 100-attempt
budget at 57 core-hours bought exactly ONE solution the first run had not reached.** Newton keeps
finding what it has already found, across runs, from an entirely different seed pool.

**Deflated continuation (Farrell–Birkisson–Funke) removes located solutions from the residual so
the same Newton cannot reconverge to them**, which converts re-finds into new orbits and improves
the R0 metric directly rather than by making attempts cheaper. It is a well-established technique,
this repository does not have it, and after U5 it is matched to the largest measured waste in the
programme. **Deflate against the union of both runs' solutions**, not just the current one's.

### R3 — multiple shooting. *Standard in this field and absent here.*

Route-DSSP brick **B6's own spec already names it** — *"the seeded Newton–Krylov / multiple-shooting
layer"* — and U1 built the hookstep/trust-region globalisation without it. Splitting the period into
segments is the standard conditioning fix for long orbits in the Kerswell line, and long orbits are
where the published targets live. A build unit with its own milestone.

### R4 — a second-order-in-time stepper. *Realization change; needs its own milestone.*

Lesson 91 forced U3 to disclose that its stepper is **Lie–Trotter, globally first order** (measured:
local ratio 4.00, global ratio 2.00), so its periodic orbits are `O(dt)` perturbations of the true
flow's. The published rates being competed against come from higher-order codes. Strang splitting or
an IMEX-RK scheme moves the discrete orbits closer to the true ones — which raises the chance a
named orbit *is* a solution of the discrete map at achievable tolerance. **This invalidates M1's
reproduction and must re-run it**, which is why it is a milestone and not a tuning.

### R5 — carry the `m` unknown in the residual. *U3's option (c). Realization change.*

U3's extended residual carries a continuous `x`-shift only, so a large block of in-window
candidates cannot be expressed as seeds at all. Every negative this repository states about orbit
recovery currently has to carry the clause *"with a residual that cannot represent one of the two
shift classes"*, and removing that clause is worth more than the seeds.

**CORRECTED 2026-08-13 by U5's measurement — this file previously implied R5 helps the band, and
it does not.** U5 priced it: carrying `m` unlocks **334 anchored in-window candidates, 58.1% of the
window, but only 1 of the 334 lies in the published `|s|` band.** So **R5 is not a fix for the
named rows.** It is the fix for `|s| > 0.9`, where the `m = 0` rate collapses to 0.02%/0.01% while
the window rate recovers. Do it as the largest measured hole in the trial space — and do not let it
be sold as a route to the published targets, which is how the earlier wording read.

**Consequence for the basin-structure finding's pointer.** U5's pre-committed reading said branch
(b) "points at `R3`/`R5`". Given the count above, the live pointers are **`R3` (multiple shooting)**
and **`U4`/`G2` (the basin radius)** and the H-hard diagnostic; `R5` stays valuable for a different
reason than the one the pointer implied.

**THE H-HARD DIAGNOSTIC HAS NOW RUN — `E`, landed `d0d72b1`, 2026-08-14 — and this is the hardest
number Lane R has produced about the named rows.** Seeded directly at the published `(T, s)` of all
eight named Lucas–Kerswell Table IV rows, two arms each: **2 of 16 converged, 0 recovered their own
row, 0 recovered ANY named row.** The two convergences are genuine solutions of this realization
that are **not** their rows, and **both fell below the 0.15 `|s|` shelf** — the basin-structure
finding reproduced **at the strongest seed quality this programme can construct.** The null is a
measurement, not a broken instrument: a positive control recovered a perturbed banked orbit at
`‖R‖ 1.5e-10`, `ΔT 3e-07`, through **this unit's own predicate**, while the phase-scrambled negative
control failed as planted.

**What this does and does not do to the wall.** It does **not** convert `G1` to a `no` — §3d holds,
and a hand-placed seed at published coordinates is **not** a mined seed, so `G1` stays
`UNDER-RESOURCED` and was not written to. It does **not** refute H-hard's alternatives outright: the
`R < 0.25` admission window **remains a live confound `E` could not separate.** What it does is
**move the suspicion from the budget to the realization**, for the first time here — `E` got
strictly closer than leg 353 (final residuals **[0.80, 10.32]** against leg 353's **[22.5, 29.5]**)
from strictly **worse** seeds, using a better realization, and still recovered nothing. **`E`'s
pre-committed branch `E-ii` named `R4` — the first-order-in-time stepper — in advance as where
exactly this outcome would point, and `E-ii`'s antecedent is satisfied.** `E-iii` also fired and
points at `R3`/`R2`. **Both pointers are live and the re-ranking between them is not yet made.**

**A ban that binds this lane: leg 349's GA gate answered NO (0 of 6 properties cleared), so
`GA compute on an unvalidated fitness` is live.** A *learned* or *evolved* seed-scoring function is
banned territory. R1–R5 are all deterministic and none of them touch it — keep it that way.

---

## What the lanes do not change

The three-tier win condition — **Tier 2 is never called a proof**. Pre-committed gates naming both
outcomes. The novelty pass before construction. Lesson 91: a negative names its realization.
Planted controls that fire in both directions. §3d's `UNDER-RESOURCED`. `merge_gate.sh` PASS.
**Clay stays ~0.05% until a link of the `L1 → L4` chain actually moves**, and that number is
recorded in the same paragraph as the ambition, not quietly dropped because the ambition went up.
