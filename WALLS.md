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

**The crack.** Leg 348 located `arXiv:1902.00384` — **a certified periodic orbit of 3D
Navier–Stokes with the viscous term inside the certified equation, on the three-torus.** That is
natively 3D, natively time-dependent, genuinely viscous, genuinely fluid. It is not a blow-up, so
it does not fill leg 174's Grade-A/fluid **blow-up** cell — but it means the *technology* clears
W2's bar already, and only the *target* is missing.

**BREAKING W2 CONSISTS OF:** a certificate whose three-dimensionality and whose time-dependence
both come from the certified object itself, for a dissipative fluid equation. Not a 2D reduction
carried up. Not an ODE profile. Pre-committed test: name the certified equation, show the viscous
term is inside it, and show the certified object is not a lift of a lower-dimensional one.

**Lane: T** (below) — this is where the credit is collected.

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

**Lane: V** (below).

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

**Lanes: T and L** (below).

---

## W5 — Persistence and stability under localisation

**Statement.** Even granted W4's cutoff, the cut solution must still be shown to blow up. No known
method. `CLAY_OBLIGATIONS.md` §6(ii).

**Status: DOWNSTREAM.** Nothing to attack until W4 has a shape. Recorded so it is not forgotten
when W4 moves and someone declares victory one obligation early.

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

**THAT READING IS NOW REQUIRED WORK, and it is the first thing Lane T must settle.**

**BREAKING W6 CONSISTS OF:** a named certificate framework, run to a `Y₀/Z₀/Z₁/Z₂`-equivalent
closure (or its analogue in the framework's own terms) on route 4's object class, with `Z₁ < 1`
achieved — or the framework's own contraction criterion met, if it does not use radii-polynomial
bounds at all.

**Lane: T.**

---

## W7 — Compute

**Statement.** `ORCHESTRATION.md` §3d says a stop fires only on a null from an attempt resourced at
the scale the question is posed at. `PROG-R4` U3 spent **134.45 core-hours**; the source papers use
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

## LANE T — THE TORUS LANE. *Priority 1. This is the breakthrough candidate.*

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
3. **`arXiv:1902.00384` already certifies a periodic orbit of 3D Navier–Stokes on `T³` with the
   viscous term inside the certified equation.** The technology closes there, demonstrated, for
   exactly our equation.
4. **Leg 390: statement (D) vacates §4 as an acceptance test**, and leg 390's own §5 item 4 says
   in terms: ***"§1's POCP credit is unclaimed. Whether any non-DSS torus blow-up ansatz could
   collect that credit is outside this leg's scope entirely."***

**The price, stated first, because free lunches here get repurchased.**
- **0 of 4 rigidity clearances carry to `T³`** (leg 390, machine-applied domain-marker rule). The
  §2 screen must be rebuilt from scratch, and **this repository has never searched the periodic
  rigidity literature** (leg 390 §5 item 2).
- **The DSS ansatz does not survive periodization.** 342 modes survive one DSS step at `λ = 1.7`;
  **0 survive two.** So Lane T needs a **non-DSS** blow-up ansatz on `T³`, and identifying one is
  open work, not a lookup.
- (D)'s data conditions **(8)** and **(9)** are not in this repository and require outreach to read
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

## LANE V — THE VISCOUS RUNG. *Priority 2. Highest information per unit of spend.*

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

## LANE L — LOCALISATION, PRICED. *Priority 3.*

**Attacks W4 on `ℝ³`, in parallel with Lane T's route around it.** §4 is currently the only
load-bearing claim in the roadmap carrying "no known method" **without having been checked to this
repository's own standard.** A scoping unit that reads the published attempts to localise a
self-similar profile to finite energy and states, per attempt, the named hypothesis that fails for
DSS converts an assumption into a measurement. It may also find the method — the claim has never
been tested.

## LANE R — REFORMULATION FOR SCALE. *Priority 4, and it runs continuously.*

**Attacks W7 by mathematics rather than hardware.** Every unit in every lane asks, as a standing
question in its pre-registration: *what would make this question answerable an order of magnitude
cheaper?* `PROG-R4` U5's shift stratification is exactly this move — it buys the compliant scale by
fixing a selection bias rather than by buying compute, and it is the second time (after AMENDMENT
4's period stratification) that the same reformulation paid.

---

## What the lanes do not change

The three-tier win condition — **Tier 2 is never called a proof**. Pre-committed gates naming both
outcomes. The novelty pass before construction. Lesson 91: a negative names its realization.
Planted controls that fire in both directions. §3d's `UNDER-RESOURCED`. `merge_gate.sh` PASS.
**Clay stays ~0.05% until a link of the `L1 → L4` chain actually moves**, and that number is
recorded in the same paragraph as the ambition, not quietly dropped because the ambition went up.
