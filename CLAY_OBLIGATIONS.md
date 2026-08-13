# Clay obligations — what a Tier-2 DSS candidate still owes

> **STATUS: VERIFIED CLAUSE BY CLAUSE, with six corrections landed. Written by the external
> reviewer, 2026-08-11, at the user's instruction; NOT banked as an established mathematical
> result — verified as a *specification*, which is a different and lesser thing.**
> The verification pass is leg 384 (`a029565`, gate YES): **23 clauses checked mechanically
> against their landed sources, 17 MATCH / 6 MISMATCH / 0 UNVERIFIED**, with **23 of 23 planted
> controls firing in both directions** (a corrupt-plant forced MATCH→MISMATCH and a repair-plant
> forced MISMATCH→MATCH on every row), so the counts are measurements and not a checker that
> could only say yes. All six mismatches are repaired in place below and each repair names its
> finding (I8, I10, I15, II1, III1/III3/III4). §4 additionally carries leg 381's own
> specification-level verification at its section header.
> **What this does NOT mean.** No clause here is a theorem, no obligation is discharged by being
> correctly stated, and §6's two no-method obligations remain **OPEN**. The ceiling stays
> **Tier 2**. Nothing here moves a link of the `L1 → L4` chain. Clay odds unchanged, ~0.05%.

## Why this document exists, and why it exists *now*

Route 4's ceiling is **Tier 2** — a numerically-confirmed candidate — and `WIN_CONDITION.md`
is unambiguous that Tier 2 is never called a proof. The programme is about to spend real
compute (leg 358: ~10.2 GPU-days at literature scale). **The purpose of this document is to
state, before that spend, what the numerics must produce so that the candidate is capable of
being certified at all** — rather than discovering afterwards that it is in an uncertifiable
form.

It has a second purpose, and it may be the more important one: **if the obligations cannot be
enumerated, there is no path, and that is worth knowing before the spend.** They can be
enumerated. Two of them currently have no known method, and those are named in §6.

## The target, as specified

`NS3D-DSS-NONAXI-LAMBDA-LARGE` (leg 251, screened by leg 313): a **discretely self-similar**,
**non-axisymmetric** blow-up profile for **3D incompressible** Navier–Stokes, realised as a
periodic orbit of period `2 log λ` in the similarity variable with `λ` an output, at `λ ≫ 1`
(leg 260's framing).

The Clay statement being answered is the breakdown direction — *exhibit* a breakdown. It asks
for initial data `u₀` on `ℝ³` that is **smooth, divergence-free, and decaying faster than any
polynomial**, such that no smooth solution exists for all time with **bounded energy**. Each
italicised word is an obligation below.

> **CHECKED AGAINST THE PRIMARY TEXT — leg 381 (`7aecf78`), integration-landed corrections.**
> The reviewer's reading was checked clause by clause against Fefferman's official problem
> statement: **4 clauses CONFIRMED, 1 CORRECTED, 1 REFUTED.**
> - **CONFIRMED, verbatim:** *bounded energy* is Fefferman's condition **(7)**, and it is the
>   condition §4 and §5 are about. Smoothness and divergence-free stand as stated.
>   **Decay is confirmed and strengthened** (leg 384, I15 — a leg-381 JSON verdict this document
>   had not carried): condition **(4)** bounds *every derivative*,
>   `|∂ₓ^α u°(x)| ≤ C_{αK}(1+|x|)^{−K}` for **any** `α` and `K`, so "faster-than-polynomial
>   decay" understates what the statement requires.
> - **CORRECTED (labelling):** the breakdown statement on `ℝ³` is **(C)**, not "(b)". All
>   references to "direction (b)" in this document mean statement **(C)**.
> - **REFUTED:** *"with `f ≡ 0`"* is **wrong**. `f ≡ 0` appears only in the *existence*
>   statements **(A)** and **(B)**. Statement **(C)** permits a smooth forcing `f` satisfying
>   its own decay conditions (4),(5). This is a genuine relaxation of the target — the
>   candidate need not be force-free — but leg 381 recorded explicitly why it is **not** a
>   shortcut: the forcing must itself satisfy (4),(5), so it buys no escape from the decay
>   and bounded-energy obligations that §4 and §5 price.
>
> A further clause is **named but not authorised**: statement **(D)** (breakdown on the torus).
> **Priced, and the price corrected, by leg 390 (DTOR, `e89cdbd`) — which makes no retarget
> recommendation, and neither does this document.** What is supportable is narrower than what
> was written here: machine-read against (D)'s own banked text, (D)'s **solution** conditions are
> (1),(2),(3),(10),(11) and contain no (7), so exactly one condition leaves — **(7) bounded
> energy** — and exactly one arrives, (10) periodicity. (D)'s **data** conditions are (8),(9),
> **whose verbatim text is not in this repository**, so no claim about what they do or do not
> require is supportable here and none is made. **(UPDATED 2026-08-13: the outreach hold was narrowed to author contact only — READING published material is now authorised, so this gap is closable by an ordinary literature unit and no longer needs a ruling.)** (A leg with outreach should close that gap:
> `writeup/data/p2_route_cloc_v1.json` banks (4),(5),(6),(7),(10),(11),(A),(C),(D) but not
> (8),(9).) **(D) deletes the acceptance test, not the work.** A non-constant exactly-λ-DSS field
> does not exist on `T³` (measured: at λ = 1.7 one DSS step leaves 342 modes in a 64-band and two
> steps leave 0; the λ = 1 control leaves 2,146,688 and never annihilates), so (D) is reachable
> only by periodizing the `ℝ³` object, at one of two prices: **wrap the uncut profile** and the
> lattice sum converges only above `α = 2.996995` against §4's `α > 1.5` — both against the same
> a-priori `α = 1.0`, a **3.993989× repurchase in deficit** (torus size is a prefactor only,
> measured L-exponent −1.0000000000000002); or **cut off first and then wrap**, whose wrapping
> bill is `0.0` at `L > 2ρ` but which inherits **leg 381's entire cutoff bill unchanged**,
> the log-divergent critical `L³` tail at 326.875 per decade included. And the cost §2 pays is
> total: **0 of 4 rigidity clearances carry to `T³`** (all four are `ℝ³`-only, two of them via the
> ansatz class rather than the ambient space). It is recorded so it is not rediscovered as new.

---

## §1 — The profile exists (rigorous enclosure)

**Obligation.** A true solution of the profile equation exists within a certified ball of the
numerical one.

**What the numerics must produce.** The approximate profile, the operator's linearisation at
it, and whatever enclosure data the chosen certification route consumes — in the form that
route requires, decided *before* the run rather than converted afterwards.

**Method status: OPEN, ONE ROUTE.** The function-space route is dead in four lanes (leg 341:
sup-norm/collocation, coefficient/`ℓ¹_w`, origin-`H²`/Mellin, and the algebraic-weight
generalisation of all three). The surviving route is periodic-orbit/flow-map certification
(leg 348, classified **(ii) OPEN-AND-REACHABLE**, cost class C), whose inputs "cut both ways":
exactly one viable spectral basis (leg 374 ADVERSE; Hermite the sole survivor, its decay
concern cleared by leg 377) and **no discrete spectral anchors** (leg 376: both `ℓ=1` and
`ℓ=2` channels continuous).

**This is the obligation the POCP spend decision buys.** Nothing downstream can be discharged
without it.

## §2 — The profile is admissible (not already excluded)

**Obligation.** The profile is non-trivial and survives every published rigidity theorem.

**Method status: LARGELY DISCHARGED, and this is the programme's strongest position *for the
`ℝ³` target*.** (Scope word added per leg 390: **0 of these 4 clearances carry to `T³`**, so on
the (D) variant §2 re-opens in full — the position is strong, and it is strong about `ℝ³`.) The
repository has an executable screen (`solver/dssp_screen.py`) encoding the exclusions, with
the object clearing each:

- **NRS 1996 / Tsai (T1/T2)** — bind *exactly-backward-self-similar* profiles only; DSS at
  `λ ≫ 1` is outside the hypothesis (leg 341's landed record; encoded operatively in
  `solver/dssp_screen.py` by legs 357/359/362 — leg 253 is cited from narrative only and has
  no landed JSON, per leg 384's II1).
- **Chae–Wolf / Pineau–Vicol** — the DSS rigidity route caps its `λ` window near 1
  (`λ̲ ≤ e^{1/2} ≈ 1.6487`, "sufficiently close to 1") against an object specified at
  `λ ≫ 1` (leg 330, full text).
- **Chae–Tsai** — Euler-only; all four theorems hypothesise the rescaled Euler system and the
  paper proves nothing about the NS equation it displays separately (leg 326, full text).
- **Morrey (Jiu–Wang–Wei arXiv:2006.15776)** — strictly *widens* the exact-SS exclusion beyond
  T1/T2 and still does not reach DSS (legs 368/370, `EXCLUDED-BY-MORREY` in the ledger).

**What remains.** The screen is only as complete as the literature searched. Any new rigidity
result for DSS at large `λ` would land here, so the screen must be re-run before publication,
not only before the build.

## §3 — The profile generates a genuine NS solution

**Obligation.** The DSS solution assembled from the enclosed profile actually solves 3D
incompressible Navier–Stokes, and loses smoothness at a finite `T*`.

**What the numerics must produce.** The consistency of the ansatz as a *certified* statement,
not a residual — the enclosure of §1 must be of a solution to the profile equation *whose
assembly back into `(x,t)` is exact*, with the Biot–Savart/pressure reconstruction included in
the enclosure rather than bolted on. Leg 351 established Biot–Savart stays on the multiplier
side in the compactified variable with the swirl potential in exact closed form — that is the
form this obligation wants.

**Method status: reachable if §1 is.** No separate obstruction identified.

## §4 — Finite energy, and the localisation problem

> **VERIFIED AS A SPECIFICATION — leg 381 (`7aecf78`), gate YES.** §4 alone carries this
> header at *problem-statement* depth; the rest of the document is verified at the shallower
> clause-against-landed-source depth of leg 384 (see the STATUS block). Three findings amend the text below
> and are integrated into it:
> 1. **The DSS case costs nothing extra.** The DSS energy exponent, with the log-periodic
>    modulation of period `2 log λ` *handled* rather than dropped, is **0.499999942** against
>    the exact self-similar **0.500000000** — **ratio 0.9999998844, no factor.** The reason is
>    structural: `λ^ℤ` is a subgroup of the same scaling group that fixes the SS exponents, so
>    discrete self-similarity can only turn the constant `∫|U|²dy` into a log-periodic `G(s)`.
>    Handling it is not optional bookkeeping: `G` swings **2.99×** (299%) within one period,
>    and a fit that drops the modulation returns **0.4876, biased 2.47%**. Measured residual
>    period **1.0574** against `2 log λ = 1.0613` (0.36%).
> 2. **One step of the arithmetic below is not valid as written.** When `U ∉ L²` — which is
>    precisely the case §4 is about — *both sides* of the scaling identity are `+∞`. Leg 381
>    repaired it with the truncated law `E_ρ(t) ≍ ρ^{3−2α}(T*−t)^{α−1}`, verified across four
>    exponents to a worst-case absolute error of `2.57e-2` (at `α = 1.4`); at `α = 1` — the
>    exponent §4 is about — the error is `2.65e-4`. (Leg 384, I8: this document previously quoted
>    `2.6e-5`, which is the single best row, α = 0.8, not the verification's worst case — a
>    factor of **988.05** between the two.) **Same conclusion, valid derivation.**
> 3. **The gap is measured, not asserted.** `L²` needs `α > 3/2`; the banked Type-I object
>    gives `α = 1` — **deficit 0.5, ratio 1.5×**. At `α = 1` the fixed-ball energy exponent is
>    **−0.00026** against a predicted 0: **the divergence is purely far-field. Nothing
>    concentrates.**

**Obligation.** The Clay statement requires **bounded energy**. This is where the object as
currently specified does not yet meet the statement, and it is the obligation most likely to
be underestimated.

**The measured problem.** Leg 260 recorded that the target has **infinite energy in the
similarity variable** — that is why it lies outside any unseeded trawl's state space. On the
reviewer's arithmetic, `∫|u|²dx` at time `t` scales as `(T*-t)^{1/2} ∫|U|²dy`, so bounded
energy requires `U ∈ L²(ℝ³)`, which the specification does not give.

**Consequence: localisation is not a tidying step, it is load-bearing.** The standard move is
to treat the self-similar solution as a *local* description near the singularity and cut it
off to obtain finite-energy, rapidly-decaying data. **Cutting off changes the equation's
solution**, so this obligation is not discharged by the cutoff — it is transferred to §5.

**What the numerics must produce.** The profile's far-field decay exponent, certified, not
fitted — because the admissible cutoff radius and the size of the perturbation the cutoff
introduces are both functions of it. `solver/dssp_screen.py` already records a fitted
far-field decay exponent per candidate; **fitted is not sufficient here.**

**The cutoff bill, priced (leg 381, all measured to ≤0.1% against closed forms).** What
shrinks: nonlinear residual `ρ^{−1.4993}`, viscous `ρ^{−1.4999}` (**identical scaling exactly
at `α = 1`**), divergence defect `ρ^{−0.4996}`, and the pressure perturbation at the origin
`ρ^{−1.9997}` — vanishing relative to `(T*−t)^{−1}`, so **pressure non-locality is not the
obstruction**. What does **not** shrink: the **cube** of the critical `L³` tail grows **326.875
per decade of window, constant to 7.4e-10** — the norm itself running `8.679 → 14.841` across
the banked 2→10 decades — log-divergent, and **never small however far out you cut.** (Leg 384,
I10: the increment was previously attached to the norm rather than to its cube; the conclusion
is unaffected, the quantity was misnamed.)
Leg 381 attempted no localisation; §4's transfer of the obligation to §5 is verified correct.

**§4 IS NOT DISCHARGED BY A δ = 0 CERTIFICATION (user ruling, 2026-08-11); THE δ QUESTION IS
NOW ANSWERED, AND THE ANSWER IS EMPTY AT THE α IN PLAY (leg 386, DTOL, `0ecaeee`).** The
admissible cutoff radius is a function of the *certified* exponent, so a certification carrying
a tolerance `δ` passes that tolerance into the cutoff bound. Leg 386 pre-registered the δ mode
before running and measured the composition directly rather than composing two legs' laws.
**Three corrections to what was written here.** (i) The width law is
`width = 4·log(1+δ)/log(R₁/R₀)`; leg 382's `0.8686` is `4/log 100`, **a property of the
window**, doubling to `1.7457` on `[10,100]` — any half-width quoted at `0.434` per unit δ is
quoted at a window. (ii) Leg 381's `δ < (α_centre − 1)/0.434` is **conservative by
`1.33×`–`4.06×`** on every measured row and never optimistic; its implied demand
`α_centre > 1 + 0.434·δ*` (≈ `2.456` at `δ* = 3.35`) is **REFUTED** — the certified half-width
vanishes at `δ*`, not at `δ = 0`, so the requirement is just `α_centre > 1`. (iii) **The
tolerance buys ZERO headroom on the threshold.** Over 30 measured configurations (3 mismatch
shapes × 5 exponents × thresholds `{1, 3/2}`) the admissible window
`D = { δ ≥ 0 : INTERVAL and p_lo > α_threshold }` is non-empty **if and only if** the realised
certified centre already exceeds the threshold — **0 exceptions**, crossover located at the
centre to `1e-6`. The dependence on `α_centre` is **a step, not a slope**; once open the
window is wide (`0.735` to `≥ 9.93` in δ). **The banked Type-I object carries `α = 1`, so its
composed δ window is EMPTY** — and would be at any `α_centre ≤ 1`. The load-bearing question
for §4 is therefore **not** the certification tolerance but whether a certified `α_centre`
exceeding `1` (or `3/2`) can be produced at all; **no profile of route 4's object exists in
this repository**, and leg 386 contributes nothing to that question. **§4's δ sub-question is
CLOSED (answer: EMPTY at α = 1). §4 itself remains OPEN**, on the admissible-cutoff half and
on the missing profile. **Method status: NO KNOWN METHOD IN THIS REPOSITORY.** Named in §6.

> **Integration note on the standing route-4 gate clause.** "Until DTOL lands, §4 stays OPEN in
> every route-4 gate" is satisfied on its own terms — DTOL has landed with a pre-registered δ
> mode — but **§4 does not thereby close**, and every route-4 gate must keep it open on the two
> grounds in the paragraph above (the admissible-cutoff half, and the absent profile), *not* on
> leg 386's account. §6 items 1 and 2 stay OPEN in every branch.

**Method status: NO KNOWN METHOD IN THIS REPOSITORY.** Named in §6.

## §5 — Stability / persistence under localisation

**Obligation.** The localised, finite-energy, Schwartz-class data still blows up. Equivalently:
the blow-up survives the perturbation §4 introduces, and survives whatever unstable directions
the profile has.

**Method status: NO KNOWN METHOD, AND THE HARDEST ITEM.** Leg 314 classified the neighbouring
question — the finite-unstable-spectrum condition — as **(iii) OPEN**, on two grounds that both
apply here: the condition **is not realization-invariant** and the source that assumes it names
no realization, so as written it has no truth value; and once a realization is fixed, the
residual obligation is a **high-frequency resolvent bound on `|Im μ| → ∞`** — *"a theorem, not
a computation, which no certified count on a bounded box can supply."* Leg 314's own summary of
the mechanism is the sentence to carry: **for this condition, numerics is a refuter, not a
verifier.**

Published work reaches 3D by *analysis on top of* a reduction, never by the certificate
(leg 172). This obligation is where that shows up for this object.

## §6 — The two obligations with no known method

Stated plainly so the programme is not planned as though they were scheduling problems:

1. **§4's certified far-field decay and the admissible cutoff.** Fitted decay exists; certified
   decay does not, and the cutoff analysis has not been attempted here.
2. **§5's persistence/stability under localisation**, including the unstable-manifold question
   leg 314 classified OPEN. This requires a theorem of a kind nobody in this repository has
   produced, and — per leg 314 — of a kind computation cannot supply.

**Neither is a reason not to build.** §1–§3 are reachable and are what the compute buys, and a
Tier-2 candidate that is *certifiable-in-principle* is strictly more valuable than one that is
not. But **the programme's honest ceiling remains Tier 2 until §4 and §5 have methods**, and no
document should describe it otherwise.

## §7 — Non-mathematical obligations

The Millennium Prize rules (CMI, 2018 revision) impose **four** conditions in their Section 4,
not three:

1. **Publication in a qualifying outlet** — Section 6(a)(i), *"a refereed mathematics
   **publication** of worldwide repute meeting the conditions in Section 6(e)"*; Section
   6(a)(ii) admits a second route, *"a publication meeting a relaxed set of conditions
   approved by the BOD following a recommendation from the SAB"*. Section 6(e)'s conditions
   include *"inclusion in the list of publications maintained by MathSciNet"*.
2. **At least two (2) years** elapsed since publication in a qualifying outlet.
3. **General acceptance in the global mathematics community, as determined in the sole
   discretion of CMI** — Section 4(c). It is a CMI determination, not a community fact;
   Section 7(a)(i)(4) enumerates what CMI may consider.
4. **The Proposed Solution has satisfactorily answered the questions raised by the Problem's
   official description, as determined in the sole discretion of CMI** — Section 4(d),
   sharpened by Section 5(d).

Two further facts of planning relevance: Section 5(e) — *"CMI will not accept Proposed
Solutions submitted directly to CMI"*; and Section 5(b) — for the Navier–Stokes Problem
*"a resolution in either direction will be evaluated by the standard evaluation procedure set
forth in Section 7"*, so the breakdown direction this repository pursues is explicitly in
scope. These are listed so that "the obligations are discharged" is never read as "the problem
is solved", and because the two-year clock is a planning fact.

> **CHECKED AGAINST THE PUBLISHED RULES — leg 384 (`a029565`), gate YES, HTTP 200**
> (`millennium_prize_rules_0.pdf`, sha256 `9b500374…`). §7's own "check before relying on it"
> is discharged. The reviewer's three-condition reading was wrong in three ways, all repaired
> above: "journal" for **publication** (III1, and it dropped route 6(a)(ii) entirely), the
> omission of *global* and of *sole discretion of CMI* (III3), and a missing fourth condition
> (III4).

## §8 — What this document asks of the build

1. Decide the certification route (§1) **before** the compute runs, because §3's assembly form
   and §4's decay-certification requirement both follow from it.
   > **SATISFIED, and recorded so it is not re-opened (user ruling, 2026-08-11).** POCP is the
   > only open route (leg 348); every alternative is closed. This ask is discharged *by that
   > fact*, **not** by waiting for a POCP report. The obligations track and the route-4 build
   > therefore run in parallel — a sequential reading of this document was wrong.
2. Produce far-field decay as a **certified enclosure**, not a fit.
3. Carry the §6 items in every route-4 gate as open, so the Tier-2 ceiling is never quietly
   relaxed by a leg that only discharged §1–§3.
4. Re-run the §2 screen before any publication, not only before the build.

---

*Reviewer's note. The most useful thing in this document is §4. The object's infinite energy in
the similarity variable is banked (leg 260) and the Clay statement's bounded-energy requirement
is explicit, but the two have not previously been written on the same page in this repository —
and the gap between them is the localisation problem, which is unattempted here and is where
comparable programmes have historically spent their hardest years. If one clause here is worth
verifying first, it is that one.*
