# Clay obligations — what a Tier-2 DSS candidate still owes

> **STATUS: DRAFT, UNVERIFIED. Written by the external reviewer, 2026-08-11, at the user's
> instruction, and NOT banked as an established result.** Every clause below needs this
> repository's own verification pass before anything is built against it. Where a clause
> rests on a landed leg it is cited; where it rests on the reviewer's reading of the Clay
> problem statement or the literature it says so, and those are the clauses most likely to
> be wrong. Nothing here moves a link of the `L1 → L4` chain. Clay odds unchanged, ~0.05%.

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
>   condition §4 and §5 are about. Smoothness, divergence-free, and faster-than-polynomial
>   decay all stand as stated.
> - **CORRECTED (labelling):** the breakdown statement on `ℝ³` is **(C)**, not "(b)". All
>   references to "direction (b)" in this document mean statement **(C)**.
> - **REFUTED:** *"with `f ≡ 0`"* is **wrong**. `f ≡ 0` appears only in the *existence*
>   statements **(A)** and **(B)**. Statement **(C)** permits a smooth forcing `f` satisfying
>   its own decay conditions (4),(5). This is a genuine relaxation of the target — the
>   candidate need not be force-free — but leg 381 recorded explicitly why it is **not** a
>   shortcut: the forcing must itself satisfy (4),(5), so it buys no escape from the decay
>   and bounded-energy obligations that §4 and §5 price.
>
> A further clause is **named but not authorised**: statement **(D)** (breakdown on the torus)
> carries *no* decay condition and *no* bounded-energy condition, which would make §4 vacuous
> by construction — at the cost of re-opening §2's rigidity screen. No leg is dispatched
> against it; it is recorded so it is not rediscovered as new.

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

**Method status: LARGELY DISCHARGED, and this is the programme's strongest position.** The
repository has an executable screen (`solver/dssp_screen.py`) encoding the exclusions, with
the object clearing each:

- **NRS 1996 / Tsai (T1/T2)** — bind *exactly-backward-self-similar* profiles only; DSS at
  `λ ≫ 1` is outside the hypothesis (legs 253, 341).
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
> header; §1/§2/§3/§5/§6/§7 remain **DRAFT, UNVERIFIED**. Three findings amend the text below
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
>    repaired it with the truncated law `E_ρ(t) ≍ ρ^{3−2α}(T*−t)^{α−1}`, verified to `2.6e-5`.
>    **Same conclusion, valid derivation.**
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
obstruction**. What does **not** shrink: the critical `L³` tail grows **326.875 per decade of
window, constant to 7.4e-10** — log-divergent, and **never small however far out you cut.**
Leg 381 attempted no localisation; §4's transfer of the obligation to §5 is verified correct.

**§4 IS NOT DISCHARGED BY A δ = 0 CERTIFICATION (user ruling, 2026-08-11).** The admissible
cutoff radius is a function of the *certified* exponent, so a certification carrying a
tolerance `δ` passes that tolerance into the cutoff bound. Leg 382's enclosure landed at width
`≈ 0.8686·δ`, which is **EMPTY at δ = 0** — and δ = 0 is the only gated mode it has, so it
answers EMPTY on every real sampled profile. Composing it with leg 381's thresholds requires
`δ < (α_centre − 1)/0.434` while `δ` must simultaneously exceed the profile's own departure
from an exact power law (leg 382 measured `δ*` up to **3.35**). **Whether both can hold is
settled by neither leg.** Leg 386 (DTOL) must answer it with a *pre-registered* δ mode.
**Until DTOL lands, §4 stays OPEN in every route-4 gate.**

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

The Millennium Prize rules require, on the reviewer's reading: publication in a **refereed
journal of worldwide repute**, a **two-year waiting period** following publication, and
**general acceptance in the mathematics community**. These are listed so that "the obligations
are discharged" is never read as "the problem is solved", and because the two-year clock is a
planning fact. *Check against the Clay Institute's own published rules before relying on it.*

> **STILL UNCHECKED.** Leg 381 read the *problem statement*, not the *prize rules*, and said
> so explicitly. §7's own "check before relying on it" stands undischarged.

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
