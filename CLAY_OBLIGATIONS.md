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

The Clay statement being answered is direction (b) — *exhibit* a breakdown. On the reviewer's
reading of the official problem statement, it asks for initial data `u₀` on `ℝ³` that is
**smooth, divergence-free, and decaying faster than any polynomial**, with `f ≡ 0`, such that
no smooth solution exists for all time with **bounded energy**. Each italicised word is an
obligation below. *This paragraph is the reviewer's reading and should be checked against the
official statement directly — it is load-bearing for §4 and §5.*

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

## §8 — What this document asks of the build

1. Decide the certification route (§1) **before** the compute runs, because §3's assembly form
   and §4's decay-certification requirement both follow from it.
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
