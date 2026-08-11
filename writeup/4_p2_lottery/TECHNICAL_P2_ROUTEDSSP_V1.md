# TECHNICAL — Route-DSSP v1 (leg 334): the seeded-DSS/RPO programme plan, brick 0 of route 4

*Leg 334, cycle 8d, slot A (critical path). Curated data: `writeup/data/p2_route_dssp_v1.json`.
Novelty pass: `writeup/novelty/leg_334.md` (committed first). Journal:
`experiments/journal/leg_334.md`. Reads `leg/313-sdss-v1` (parked), `leg/315-tms-v1` (parked),
`leg/260-dssb-v1` (parked), legs 331/332/326/262 (landed on `main`); **edits none of them**.*

---

## 0. THE CEILING, STATED BEFORE ANYTHING ELSE — AND IT IS NOW A MEASUREMENT, NOT A POLICY

> **CEILING: TIER 2.** The best outcome this entire programme can produce is a **numerical
> discretely-self-similar blow-up candidate for 3D Navier–Stokes that survives a resolution-
> convergence study**. `WIN_CONDITION.md` is unambiguous: *"Passing Tier 2 is strong numerical
> evidence of a genuine singularity. It is still **not a proof** — floating-point simulation cannot
> certify behavior at an actual singular point."* **Only Tier 3 answers the Clay problem**, and Tier
> 3 requires certification machinery that **does not exist for this object**. Every brick below
> restates this ceiling inside its own drafted gate. Any prose in this file, or in any brick drafted
> from it, that could be read as claiming or implying Tier-1-in-the-Clay-sense or Tier-3 progress
> **fails this leg's own gate**, and the reader is invited to hold it to that.

**The ceiling is not merely a stated caution here; it tracks the state of the certification
question.** §2.5 records that the only weight class in which this object appears to have a finite
norm is an **algebraic** one, and §2.8 that the only weight class in which any available
certification machinery is known to close is a **Gaussian** one — which leg 331 has now measured does
not tolerate algebraic tails. **On the record as it stands there is no known route from the Tier-2
candidate this programme aims at to a Tier-3 certificate.**

**That question now has an owner and this plan is not it.** Per the DM's cycle-9 ruling the weight
question belongs to **leg 341 (ROUTE-ALGW)**, and any Tier-2→Tier-3 build is a **DM-drafted §3 build
gated on leg 341's report and on a USER ruling** — explicitly *"drafted ONLY after 341 reports"*,
with the standing instruction that *"until it lands, every route-4 gate keeps the Tier-2 ceiling
unchanged"*. **So the ceiling on this plan is TIER 2 in both branches of leg 341's answer (§2.9), and
no brick below may be read as moving it.**

**No ban is lifted, narrowed, re-read or argued against here. `plan_of_record.py` was not touched
and this leg has no authority over it. No link of the L1→L4 chain moved. Clay odds ~0.05%.**

---

## 1. The gate, in its pre-committed wording, and its answer

> **Does the plan name (a) the function space, carrying 313's (a) answer and §26/4.1's
> limited-regularity difficulty; (b) the solver architecture and RPO extraction design, with build
> costs in legs; (c) a concrete, non-empty seeding strategy — or the measured statement that none
> exists yet and what would create one; and (d) the brick sequence sized through FOUR slots over
> cycles — with the Tier-2 ceiling stated in the plan and in every brick's drafted gate?**

> **YES — all four clauses are answered on paper, and clause (c) is answered on its second branch,
> which the gate explicitly provides for: the seeding problem is STILL MEASURED EMPTY, re-measured
> independently at leg 334, and what would create a non-empty seed set is named in three concrete
> items (§4.7).** Clause (a) **names the space it targets (§2.3), states its NRS/Tsai position
> outright (§2.7), carries §26/§4.1's limited-regularity difficulty with leg 313's measured cost
> (§2.6) — and, per the DM's cycle-9 narrowing, CONSUMES rather than answers the weight question,
> which is now OWNED BY LEG 341. Leg 341 had not landed, so the question is recorded as
> OWNED-BY-341-PENDING and BOTH BRANCHES of its answer are named with what this programme does in
> each (§2.9). The programme's brick sequence and its Tier-2 ceiling are robust to either branch.**
> Clause (b) names five modules, an architecture, and a **bracketed** cost that is honest about being
> uncertain by a factor of ~11 (§3.5). Clause (d) lays nine bricks across four slots over six cycles
> (§5), every one carrying the Tier-2 ceiling in its own drafted gate.

**The gate answers YES in the narrowed frame, and the narrowing does not cost it a clause.** Clause
(a) asks the plan to *name the function space carrying leg 313's answer and §26/4.1's difficulty* —
which §2.3/§2.6/§2.7 do. The weight-tolerance sub-question added at cycle 8d was re-owned at cycle 9,
and a plan that **consumes** an owned question with both branches costed is answering it in the form
the current ruling asks for. **If a reader judges otherwise — that deferring the weight question
makes clause (a) unanswered — then the correct reading is the gate's no-branch on (a) alone, with the
named blocker being "leg 341 has not reported", which routes to leg 341 and NOT to the user, since
the DM has already assigned it.** Either reading leaves clauses (b), (c), (d) answered and the brick
sequence dispatchable from B1 onward, and B1 carries 341 as its precondition in both.

**Four things are routed, not decided, and the plan is explicit that they gate specific bricks:**

1. **The weight question** — **OWNED BY LEG 341 (ROUTE-ALGW)**, undispatched at this leg's finish.
   Brick B1 carries it as a **precondition**. §2.0, §2.9.
2. **The ban-wording question** leg 313 §5 handed to the user (does either DSS ban entry reach a
   *seeded* search?) is **undecided**. Brick B6 — the first brick that runs a periodic-orbit search
   at all — **must not be dispatched before the user rules**. §6.
3. **Leg 330 (PVLX)** owns the adjudication of Pineau–Vicol `arXiv:2607.09619`'s reach, and **had not
   landed when this leg started**. A positive reach moves the admissibility screen this plan designs.
   §2.7.
4. **Clause (c)'s seeding question has a second owner**: **leg 342 (ROUTE-SEED)**, created in the same
   cycle-9 ruling to scope route 4's seeding problem in depth. Per its own coordination clause,
   **this plan answers clause (c) on paper as drafted and leg 342's deeper scoping consumes and
   extends that answer** — §4 is written to be extended, not to close the question.
5. **The critical-collapse transfer** located in this leg's novelty pass (§4.6) is engineering
   precedent, not mathematics this leg claims. Its disanalogy is stated at full strength.

---

## 2. CLAUSE (a) — THE FUNCTION SPACE

### 2.0 OWNERSHIP, STATED FIRST: LEG 341 OWNS THE WEIGHT QUESTION; THIS PLAN CONSUMES ITS ANSWER

**This clause was narrowed in flight, and the narrowing is honoured rather than worked around.** The
DM's cycle-9 ruling (`a17554c`, relayed to this leg mid-drafting) creates **leg 341 (ROUTE-ALGW)** to
scope leg 260's algebraically weighted space as a candidate **fourth space/basis**, and rules:

> *"the weight question (cycle 8d's binding, where it collides with 332's open lane) is OWNED by 341.
> 334's clause (a) NARROWS TO CONSUMING it — the plan names the space and cites 341's answer if
> landed, or records the question as owned-by-341-pending if not; it does not answer the weight
> question ad hoc."*

**Leg 341 had not landed when this leg finished** — it sits at the head of the reserve queue,
undispatched. **Therefore this clause records the weight question as OWNED-BY-341-PENDING and names
both branches (§2.9), and the analysis in §2.2–§2.5 is offered as CONTEXT FOR LEG 341's screens, not
as an adjudication of them.** Where §2.2–§2.5 reach a conclusion, the conclusion is **conditional and
non-authoritative**, and any brick that depends on it carries leg 341 as a precondition (§5).

**What is NOT deferred, because it is not the weight question.** Two parts of clause (a) are this
leg's own and are answered outright: the **NRS/Tsai position** of the target class (§2.7 — the DM's
cycle-8b binding, unchanged by the narrowing) and the **§26/§4.1 limited-regularity difficulty**
(§2.6 — the ban's own lift clause, a *basis-resolution* question, not a weight question). Neither
depends on which weight leg 341 reports.

**One caution this plan puts on the record about its own §2.2.** Leg 341's dispatch thesis states
that leg 260 already computed the space holding an algebraic tail **sharp**: *"L^p, p > 3, or
L²((1+|y|)^{-s}), s > 1, L³, L², Gaussian H²(μ) excluded"*. §2.2's criterion reproduces that
`s > 1` independently, from the exponent alone. **That agreement is offered to leg 341 as a
cross-check between three separate derivations (260's, 313's measurement, this leg's arithmetic) —
and precisely because it agrees, it is the kind of thing that can be believed too easily. Leg 341
should test it, not inherit it.**

### 2.1 The collision, stated exactly as the DM stated it

The cycle-8d ruling requires this clause to confront a head-on collision between the two legs that
landed as this leg's preconditions:

* **Leg 332 (`bd438de`)** opened the **vorticity-formulation lane**: the Leray-type obstruction that
  legs 257/261 derived in the velocity formulation **fails at step S4** in the vorticity formulation,
  because *"the entire non-vanishing tail sits inside the pressure gradient, and `curl ∘ grad ≡ 0`"*.
  The space it measured this in is Breden–Chu's / Gallay's **Gaussian-weight** space,
  `μ(x) = Γ(d/2)(2√π)^{-d} e^{|x|²/4}`, and the reconstruction it depends on is **Biot–Savart**,
  which is **nonlocal**.
* **Leg 331 (`e9f4956`)** measured, for the first time, that Breden–Chu's machinery does **not** hold
  a nonlocal operator, and — this is the leg's own reframing, endorsed by the DM — the mechanism is
  **not nonlocality**: *"What breaks is the interaction between an algebraic tail and a Gaussian
  weight — the `e^{|x|^2/4}` weight, not nonlocality as an abstract property. […] it reframes the
  (iv_a) re-screen question as 'which weight tolerates an algebraic tail', and a Gaussian one
  demonstrably does not."*

Leg 331's measured numbers, quoted rather than paraphrased. The forced tail exponent of
`Λ^{2α}ψ_m` is `1+2α+2m`, **pre-registered before measurement**:

| α | predicted exponent | fitted exponent |
|---|---|---|
| 0.25 | 1.5 | **1.507674** |
| 0.50 | 2.0 | **2.012245** |
| 0.75 | 2.5 | **2.517908** |

and against `μ = e^{x²/4}`, `‖Op ψ_0‖²_{L²(μ), |x|<R}` at `α = 0.5`:

| R | `Λ^{2α}ψ_0` | control `∂_x ψ_0` |
|---|---|---|
| 4 | 0.9655 | 0.953988 |
| 8 | 1.196e3 | 0.999999477 |
| 12 | 5.872e10 | 0.9999999999999978 |
| 16 | **1.869e22** | **1.0000000000000000** (0.9999999999999993) |

*"The control saturates at 1; the nonlocal norm has no limit."*

**The collision, in one sentence: the standard vorticity space IS the Gaussian weight leg 331
measured intolerant of algebraic tails, and Biot–Savart IS nonlocal.**

### 2.2 An arithmetic observation offered to leg 341 — NOT this leg's adjudication

*Per §2.0 this subsection is context, not a ruling. It was drafted under the cycle-8d framing that
asked this leg to resolve the collision; the cycle-9 ruling moved that resolution to leg 341, and it
is retained — on the DM's instruction not to discard it — as **material describing what leg 341
should check**, with its conclusions marked conditional throughout.*

**The observation is that the DSS target may not be in the Gaussian space at all**, in which case the
two findings never meet in one space and the collision is dissolved rather than resolved. It is
arithmetic, checkable in three lines, and **leg 341 should verify or refute it rather than take it
from here.**

For a profile with an **algebraic** far field `|f| ~ |y|^{-p}` in `R^d`:

| weight `w` | `∫_{|y|>R} |f|² w dy` finite? | tolerated decay |
|---|---|---|
| Gaussian, `w = e^{|y|²/4}` | **never**, for any algebraic `p` | only `|f|` decaying **faster than** `e^{-|y|²/8}` |
| algebraic, `w = (1+|y|)^{-s}` | **iff `2p + s > d`** | any `p > (d-s)/2` |

The screened object is leg 251's `NS3D-DSS-NONAXI-LAMBDA-LARGE`, carrying leg 253/260/313's
**Type-I-scale bound** `|V(y)| ≤ C/(1+|y|)` (Chae–Wolf `arXiv:1610.09464` Thm 1.1). So `p = 1`,
`d = 3`, and the criterion gives the crossing at **`s = 3 − 2 = 1`**.

**Leg 313 MEASURED that crossing, and measured it at exactly `s = 1`.** Its banked shell-ratio
table (`writeup/data/p2_route_sdss_v1.json`, quoted from its TECHNICAL §1.1):

| space | shell ratio | verdict |
|---|---|---|
| unweighted `L²(dy)` | **2.000277** | DIVERGES |
| weighted `L²(ρ)`, `s = 0.9` | 1.071997 | diverges |
| weighted `L²(ρ)`, `s = 1.0` | **1.000216** | **the crossing** |
| weighted `L²(ρ)`, `s = 1.1` | 0.933242 | FINITE |
| weighted `L²(ρ)`, `s = 1.5` | 0.707 | finite |
| compactified `X = \|y\|/(1+\|y\|)` | — | FINITE, `‖U‖_{L²(dX)} = √(1/3) = 0.577350` |

**This is a control that could have come out differently.** The criterion `2p+s>d` was written down
from the exponent alone; leg 313's crossing was measured on shell integrals started at `R = 1e4` with
a faithful envelope `(1+r)^{-1}`, by a different leg, in a different year of this project's record,
for a different purpose. It lands on `s = 1` to `2.16e-4` in the shell ratio. Had the criterion given
`s = 0` or `s = 2` the whole of §2.3 would be wrong and this section would say so.

**Therefore, conditionally and subject to leg 341:** the Gaussian weight `e^{|y|²/4}` appears not to
contain the target — not because of any nonlocal operator, not because of leg 331, but because
`e^{|y|²/4} · |y|^{-2}` is not integrable and never was. **If leg 341 confirms this, then leg 332's
open lane and leg 331's obstruction are both statements about the Gaussian space, the search this
programme runs does not take place there, and they are statements about the certification step
instead** — which is what §2.8 prices. **If leg 341 refutes it, §2.3's space choice and §2.8's
conclusion both change, and §2.9 says how.** This leg does not decide between those branches.

### 2.3 The space this plan TARGETS, named — conditional on leg 341

**Target: the VORTICITY, `Ω = ∇ × V`, in unweighted `L²(R³) ∩ H^k`, realised in leg 313's
compactified radial variable `X = |y|/(1+|y|)` with a spherical-harmonic angular basis.**

**"Targets", not "chooses".** Per §2.0 the authoritative weight ruling is leg 341's. This is the
space the plan is *built against* so that clause (a) says something concrete rather than deferring
into vacuity; **brick B1 (§5.1) is the brick that pins it, and B1 carries leg 341 as a precondition.**

The vorticity choice is not inherited from leg 332 as a preference — **it buys a full unit of weight,
and the same arithmetic says so.** For a Type-I profile `|V| ~ |y|^{-1}`, the vorticity decays one
order faster, `|Ω| ~ |y|^{-2}`, so `p = 2` and the criterion `2p+s>d` reads `4 + s > 3`:

| field | `p` | criterion at `d=3` | weight needed |
|---|---|---|---|
| velocity `V` | 1 | `2 + s > 3` | **`s > 1`** — a weight is mandatory |
| vorticity `Ω = ∇×V` | 2 | `4 + s > 3` | **`s ≥ 0`** — **none**; `Ω ∈ L²(R³)` unweighted |

**So in the vorticity formulation the state variable of the screened object sits in a plain
unweighted `L²(R³)` with margin 1, and no weight has to be chosen at all for it.** That is an
independent, arithmetic reason to use the vorticity formulation, and it agrees with leg 332's
independent, Leray-obstruction reason. Two different arguments, same conclusion — recorded as such,
not merged into one.

### 2.4 The weight-tolerance question — ROUTED TO LEG 341, with 331's exponents made executable for it

The cycle-8d binding asked: *"whether its weight tolerates the algebraic tails its nonlocal operators
produce, citing 331's measured exponents — or name that as the blocker its no-branch routes to the
user."* **Under the cycle-9 narrowing this question has an OWNER — leg 341 — so it is neither
answered here nor routed to the user as a blocker; it is routed to LEG 341**, which exists precisely
to answer it and whose own gate names it. What this section supplies is the two parts of the question
that this leg can usefully hand over.

*Both parts are, per §2.0, offered to leg 341 rather than asserted over it. Part 1 is the piece leg
341 owns outright. Part 2 is a design rule about how an operator is USED, which is this leg's to
state, and which survives either branch of leg 341's answer.*

**Part 1 — the weight tolerates them, and leg 331's own measured exponents are the test case
(SUBJECT TO LEG 341).**
Leg 331 works in `d = 1`. Its measured tails are `p = 1.507674 / 2.012245 / 2.517908`. Applying
`2p + s > d` with `d = 1` and the **unweighted** case `s = 0`:

| α | measured `p` | `2p + 0 > 1`? |
|---|---|---|
| 0.25 | 1.507674 | **3.015 > 1 — YES** |
| 0.50 | 2.012245 | **4.024 > 1 — YES** |
| 0.75 | 2.517908 | **5.036 > 1 — YES** |

**Every tail leg 331 measured is square-integrable against Lebesgue measure.** The divergence
`0.9655 → 1.869e22` is produced **entirely by the weight** — which is precisely leg 331's own
reframing, now stated as an inequality with margins rather than as a description. **The re-screen
question leg 331 posed — *"which weight tolerates an algebraic tail"* — is exactly leg 341's gate,
and the candidate answer this arithmetic suggests, for leg 341 to test rather than inherit, is: any
weight of polynomial growth `≤ |y|^{2p−d}`; no weight of Gaussian growth.** Note what this leg's
arithmetic does *not* address, and what leg 341's gate does: whether such a space **escapes the
three-realization death** (ℓ¹_w / collocation / origin-`H²`) and whether the CAP apparatus has a
coherent formulation in it. **Integrability of the target is necessary and nowhere near sufficient,
and nothing here should be read as evidence toward the Stage-V ban's lift condition — that evidence
is leg 341's to produce and the ruling on it is the USER's.**

**Part 2 — the chosen space does not have to tolerate the nonlocal output in the first place, and
this is the design rule the plan extracts from reading 331 and 332 together.**

> ### THE NONLOCAL-OUTPUT RULE (this leg's named mechanism)
>
> **An algebraic tail is fatal when the nonlocal operator's output stands ALONE as a summand inside
> the weighted norm, and harmless when it enters only as a bounded MULTIPLIER against a factor that
> already decays.** Leg 331's fatal quantity is `‖Λ^{2α}ψ_m‖_{L²(μ)}` — the nonlocal output, alone,
> in the norm. Leg 332's finite quantity is
>
> `‖(u·∇)ω − (ω·∇)u‖_{L²(μ)} ≤ ‖∇u‖_∞ ‖ω‖_{L²(μ)} + ‖u‖_∞ ‖∇ω‖_{L²(μ)}`
>
> in which the nonlocal output `u = BS(ω)` appears **only through `‖u‖_∞` and `‖∇u‖_∞`**, and every
> term carries a factor of `ω` or `∇ω`. Leg 332 measured both ratios strictly inside `(0,1)` —
> `0.10094` (witness A) and `0.13863` (witness B), bound `3.691487980` vs actual `0.372629937`, and
> `0.731194238` vs `0.101364697` — i.e. **the bound holds and is not vacuous**, and its own words for
> why: *"Every term in the vorticity nonlinearity carries a factor of `ω` or `∇ω`, which is Gaussian;
> `u` and `∇u` need only be **bounded**, and are. In the velocity formulation the projector's output
> stands alone with nothing to multiply it down."*
>
> **This is lesson 87 in its own terms** — *a certification method has a SHAPE, and the shape is a
> property of the OPERATOR: multiplier or shift?* Leg 331 met the shift; leg 332 met the multiplier.
> **Every brick below is required to keep Biot–Savart on the multiplier side**, and B3's gate is
> written to fail if it does not.

Transposed to the chosen unweighted space, the same inequality reads
`‖(V·∇)Ω − (Ω·∇)V‖_{L²} ≤ ‖V‖_∞‖∇Ω‖_{L²} + ‖∇V‖_∞‖Ω‖_{L²}`, and for a Type-I profile the two
`L^∞` factors are exactly what the Type-I bound supplies: `|V| ≤ C/(1+|y|)` is **bounded**. **Whether
`‖∇V‖_∞ < ∞` for the actual numerical profile is a hypothesis, not a theorem, and it is B3's gate.**

### 2.5 The price of the algebraic weight — the dichotomy, stated because it is the real content

The Gaussian weight is not chosen anywhere in this literature for taste. It is chosen because
Gallay's rescaled operator `L = −Δ − (x/2)·∇` has **discrete** spectrum on it, which is what makes
Fredholm arguments, radii-polynomial certificates and normal-form/spectral analyses close. On an
**algebraically** weighted or unweighted space, the same operator has **continuous** spectrum.

**This repository has already measured that trade in its own model, and it is the reason the cheap
entrance is banned.** `plan_of_record.BANNED`, Entry A, reason (1), machine-read: *"Route-E `cd43893`
/ `PHASE2_P2_NOTES` §26 — the log-periodic directions are **CONTINUOUS spectrum**, the only
grid-converged isolated eigenvalues are the two exact symmetry modes 0 and −1, planted positive
control +1.083 (V=6) / +4.578 (V=12); a continuum has no eigenvalue to move."*

> **THE WEIGHT DICHOTOMY.**
> **Algebraic weight ⇒ the target is in the space, and the linearisation has continuous spectrum.**
> **Gaussian weight ⇒ the linearisation has discrete spectrum, and the target is not in the space.**
> There is no third column **on the measured record as this leg found it**, and **whether a third
> column exists is precisely leg 341's gate** — a fourth space that holds an algebraic tail *and*
> escapes the three-realization death would be one. **This plan takes the first column and therefore
> inherits the continuous spectrum**, which is exactly why the entrance must be a *seeded orbit
> search* and can never be a bifurcation off a fixed point — *"a continuum has no eigenvalue to
> move"*. **The ban and the function-space choice are the same fact seen twice, and this stays true
> in both branches of §2.9**: even if leg 341 finds a third column, the continuous spectrum is what
> made the cheap entrance impossible, and no report from leg 341 revives it. **Entry A's lift
> condition is `never` and nothing here touches it.**

### 2.6 §26/§4.1's limited-regularity difficulty, carried (not re-derived)

The ban's own lift clause requires carrying it: the orbit's building blocks are *"of LIMITED
REGULARITY at the origin (`X^{1-iy}`, fractional power at `X=0`)"*. Leg 313 carried it by
transposition and measured the cost, and this plan carries **both** verbatim:

* **The transposition** (leg 313 §0): under `X = |y|/(1+|y|)`, `r^{-1+iκ} ↦ (1-X)^{1-iκ}` — *"the
  **identical functional form** to clause (a)'s recorded gCLM difficulty `X^{1-iy}` […] now sitting
  at `X = 1` instead of `X = 0`. The difficulty is conserved under the map. It is not about the seed,
  which is why seeding does not touch it."*
* **The measured cost** (leg 313 §1.2, Chebyshev on `[0,1]`, `N = 2^20`, converged; its own `N=2^14`
  numbers and its `1e-8` column are **withdrawn** and are not quoted here):

| `κ` | fitted decay rate `p` | modes for `1e-6` relative truncation |
|---|---|---|
| smooth control (entire, asymmetric) | geometric | **10** |
| 0 (control) | terminates exactly | 2 |
| 1 | 3.000 | **823** |
| 2 | 3.000 | 1482 |
| 5 | 2.999 | 3564 |
| 10 | 2.994 | 7086 |
| 20 | 2.977 | **14149** |

  Cost law `n(κ) ≈ 791 · κ^0.954`, max relative residual **3.9%**; separation from the smooth control
  at the cheapest `κ ≠ 0` row is **82.3×**.
* **The extrapolation leg 313 explicitly forbade importing is not imported here.** Its 257,466-mode
  row at gCLM's `|Im| = 430.35` is *"reported only to price an import that is not licensed"*; the ban
  text itself says *"Nothing about NS. gCLM's scaling structure is not NS's."* **The NS log-periodic
  frequency `κ` is unknown and is an OUTPUT of the search being planned.** No number in §3's costing
  uses a gCLM `κ`.
* **The viscous half does not transfer either**, and the ban's own clause (b) says so: the gCLM
  statement *"in the VISCOUS gCLM problem that band is absent entirely (max Re = -1e-13 at
  mu=0.05)"* is gCLM's, and leg 260 §1.1's crossover mechanism (gCLM's band sits where dissipation
  wins, NS's where the rescaling drift wins by `r²`) is **transcribed, not re-derived**.

**Design consequence, which is what carrying it is for:** the basis for the radial direction must
resolve a **fractional power at a boundary point**, and a plain polynomial basis costs `O(10³–10⁴)`
modes per unit of `κ` to do it. **This is brick B2's whole subject**, and B2's gate is written as a
comparison against the 823–14149 baseline, so that "we improved it" cannot be asserted without a
number.

### 2.7 NRS/Tsai POSITION — stated here, not discovered later

The DM's binding (cycle 8b, restated at 8d): *"334's function-space answer must state how its target
class stands relative to NRS/Tsai, not discover this later."*

**The target class.** Backward **discretely** self-similar, **non-axisymmetric**, `λ` **significantly
larger than 1**, profile **outside `L^∞_t L³`**; as a search object, a **periodic orbit of the
dynamically rescaled flow with period `S₀ = 2 log λ`**, `λ` an **output**. (Leg 313 §2 re-located that
equivalence from an independent published source: Chae `arXiv:1306.0305` defines the asymptotically-
DSS object as a solenoidal `V̄(y,s)` with `V̄(y,s) = V̄(y,s+S₀)`, `S₀ ≠ 0` — **DSS is
time-periodicity of the rescaled field, published, not this repository's coinage**.)

**The rigidity ledger, every entry with its status:**

| theorem | hypothesis it needs | does it reach the target? | status |
|---|---|---|---|
| Nečas–Růžička–Šverák / Tsai | **exactly backward self-similar**, with `u ∈ L³` or Type-I local-Leray admissibility | **No — fails on the ansatz.** The target is *discretely*, not exactly, self-similar | standing, per `CONTINUATION_PROMPT.md`'s framing |
| Chae–Tsai `arXiv:1304.7414v1` (DSS with time-periodic `V`) | *"a time periodic solution (1.6)"*, and **(1.6) is the rescaled EULER system** | **No — fails on the equation.** Leg 326 read it at full text and measured: the authors' own reach statement generalises over *two real constants* `a, b` in `V_s + aV + b(y·∇)V + (V·∇)V = −∇P`, and **`−ΔV` is not a member of that family for any `a, b`**. Independently, its decay hypothesis (2.2) demands `Ω ∈ L^q` for **every** `q ∈ (0,r)`, far stronger than the Type-I-scale bound | **MEASURED SILENT**, leg 326 `c541cdb` |
| Pineau–Vicol `arXiv:2607.09619` (Liouville for backward SS and DSS under a Type I bound) | its **RDSS clause requires `λ` sufficiently close to 1** | **Unknown — the target has `λ` significantly larger than 1, i.e. the complementary regime** | **NOT ADJUDICATED. Leg 330 (PVLX) owns it and had not landed when this leg started.** This plan does not adjudicate it and does not predict its answer |

**The position, stated plainly: the target class sits in the COMPLEMENT of every rigidity hypothesis
reachable on this repository's record — exactly-SS (fails by ansatz), DSS-on-Euler (fails by
equation, measured), DSS-with-λ-near-1 (fails by parameter regime, unadjudicated).** Two consequences,
and the second is uncomfortable and is stated anyway:

1. **`λ` significantly larger than 1, and decay strictly slower than `L³`-admissible, are not design
   preferences — they are the only region in which a found candidate would not already be excluded by
   a published theorem.** They therefore become a **live screen** on every candidate (brick B7), not
   a note in a README.
2. **A search deliberately confined to the complement of every rigidity theorem is a search for an
   object that no theorem forbids and no theorem predicts.** That is a Tier-2 object at best, by
   construction. It is honest to say this in the plan rather than at the end of the programme.

**Leg 332's `L³` finding is the operational warning, and it is why B7 exists.** Leg 332 measured that
a Gaussian-decaying vorticity reconstructs to a velocity with *"fitted decay exponent of `|u_B|` on a
generic off-axis ray: **−3.0000000000000027**"* and *"`‖u_B‖_{L³(R³)}` = **0.7307683991070311**,
converged at `R = 60`"*, and recorded: *"`u ∈ L³(R³)` is exactly the Nečas–Růžička–Šverák / Tsai
hypothesis, which forces `u ≡ 0` for backward-self-similar 3D Navier-Stokes. The vorticity
formulation buys admissibility into the space and hands the target straight to the ansatz constraint."*
**A profile that decays too fast lands in `L³` and, as `λ → 1`, walks into the regime the published
theorems occupy.** So the screen is not optional and it is not post-hoc: `‖V‖_{L³}`, the fitted decay
exponent, `λ`, and an axisymmetry diagnostic are computed on **every** candidate, at every Newton
step, and a candidate that lands in `L³` with `λ` near 1 is **reported as excluded, not as a result**.

**Leg 332's §10 rider, inherited and answered.** Its rider records that Breden–Chu's `L = −Δ −
(x/2)·∇` is the **forward** generator, that a **backward** self-similar profile carries `+(y/2)·∇`,
that both remain maps `H²(μ) → L²(μ)` (`5.716528960333894` vs `6.041350443296389`; Rayleigh quotients
`7.2727` vs `6.4545`), and that *"a later leg reaching for this space with a backward ansatz will meet
it."* **This plan meets it and answers: the sign flip is inherited (the rescaled equation in §3.1
carries `+(y/2)·∇`), and the mapping question it raises is moot for the search, because §2.3's space
is not `H²(μ)`.** The rider is carried into the certification lane (§2.8), where it does bind.

### 2.8 What the collision COSTS: the certification step has no known route ON THE RECORD AS IT STANDS

This is the part the DM's ruling makes unavoidable, and it must not be buried. **"On the record as it
stands" is load-bearing: leg 341 exists to test whether a fourth space changes it, and §2.9 states
what happens in each of its branches. Nothing below is a claim that no such apparatus could exist —
only that none is known here, now.**

* Certification of a self-similar fluid profile, on this repository's and the literature's measured
  record, closes in **weighted-Sobolev Gaussian** spaces (Breden–Chu `arXiv:2404.04054v2`;
  Dähne–Figueras CGL `arXiv:2410.05480`, reproduced row-for-row by leg 316).
* **Leg 331 measured that this machinery does not hold even ONE nonlocal operator on its own space**:
  the apparent finiteness is a **quadrature-horizon artefact** (true `log10` norm² `95.151` at
  `n=100`, `197.728` at `n=200`, **`1546.389` at Breden–Chu's own published `n=1500`, where it
  overflows float64** — *"refining `n` makes it monotonically worse"*), the `K`-product
  Gauss–Laguerre rule **loses exactness** (0.3393 relative error at 20% nonlocality vs a local
  control exact to `1.6e-12`), and the contraction constant `Z₁` **crosses 1 at 30–52% of one
  nonlocal operator** (`t* = 0.3000/0.4000/0.4559` at `n=100`; `0.4705/0.5156` at `n=200`; bisected
  to width `6.1e-06`).
* **And §2.2 argues — conditionally, pending leg 341 — that the target is not in that space anyway.**

**Therefore, on the current record: the Tier-2 → Tier-3 step for this object has no known apparatus.
Not a hard one — an absent one.** The plan's response is *not* to invent one, and — since cycle 9 —
*not* to scope one either, because that scoping now has an owner (leg 341) and the build it might
license is DM-drafted and user-ruled:

* **The validated-integration / Taylor-model item (leg 315) folds in HERE, and is NOT scheduled.**
  Leg 315's reaching mechanism is a Taylor-model **flow** enclosure of a finite-dimensional
  **autonomous ODE**, which *"requires no function space at all"*. **The DSS object is a PDE orbit in
  infinite dimensions, not an ODE trajectory**, so 315's `O1` mechanism does not reach it as it
  stands; the standard bridge (Zgliczyński–Mischaikow self-consistent a-priori bounds, `math/0005247`)
  has **dissipative/parabolic** hypotheses, which the *rescaled NS* system does satisfy — unlike
  BCG's quasilinear hyperbolic system, which is what made 315 class it cost-class C. **That is a
  genuinely different situation from 315's and it is recorded as an open, unscoped possibility, not
  as a plan.** Brick B9 exists to scope it, and B9 is **drafted but not scheduled**.
* **Leg 315's re-entry guard is carried verbatim and binds every brick here**, exactly as the DM
  confirmed it: *"GUARD, binding on any future O1 work: the moment a build introduces a
  sequence-space certificate step, it re-enters the ban's scope and stops."* **Restated for this
  route: if any brick in §5 introduces a sequence-space (ℓ¹-Fourier / radii-polynomial) certificate
  step, that brick RE-ENTERS the re-posed Stage-V ban's scope and STOPS.** No brick below contains
  one, and B9's drafted gate makes the guard its own first check.

> **Consequence, stated so it cannot be read apart from the programme: this programme is designed to
> reach TIER 2 and to stop there.** It does not have, and does not claim, a route to Tier 3. If it
> succeeds completely, the output is a numerical DSS blow-up candidate that has survived a
> resolution-convergence study, and **`WIN_CONDITION.md` says in as many words that this is not a
> proof and not an answer to the Clay problem.**

### 2.9 THE TWO BRANCHES OF LEG 341's ANSWER, AND WHAT THIS PROGRAMME DOES IN EACH

Per §2.0, leg 341 had not landed. Both branches are named here at a high level so that the plan is
actionable the moment it reports, and so that neither branch can be presented afterwards as the one
the plan expected.

**BRANCH A — leg 341 reports that the algebraically weighted space ESCAPES the three-realization
death.** Then §2.5's dichotomy is broken on the algebraic side: the target is in the space *and* an
apparatus has a coherent formulation there. Consequences: **(i)** §2.3's target space stands and B1
pins it as written; **(ii)** §2.8's "no known route to Tier 3" is **weakened but NOT removed** — the
DM has already reserved that clause: the packet's `§3 build` is *"drafted ONLY after 341 reports"*,
carries the Tier-2→Tier-3 clause **in its own gate**, and *"until it lands, every route-4 gate keeps
the Tier-2 ceiling unchanged"*; **(iii)** brick **B9** (§5.1) is **superseded** by that DM-owned §3
build and should be struck rather than dispatched, to avoid two bricks owning one question.
**The Tier-2 ceiling on THIS plan does not move in branch A.** Only a landed §3 build, under a
user ruling, could move it, and that is neither this leg's nor this plan's to assert.

**BRANCH B — leg 341 reports that the algebraically weighted space DIES**, naming the realization and
mechanism that kill it. Then the Stage-V lift condition **stays unmet**, the §3 build is **never
drafted**, and the fourth space joins the measured dead ends. Consequences: **(i)** §2.3's target
space still stands **for the SEARCH** — a search does not need a certificate apparatus, only a
discretisation, and §2.2's integrability is what the search needs; **(ii)** §2.8's conclusion
**hardens from "no known route" to "the fourth candidate route is measured dead too"**, and the
Tier-2 ceiling becomes correspondingly firmer; **(iii)** B9 is struck as pointless. **The programme
in §5 is UNCHANGED in branch B except that B9 disappears** — which is the honest reading of a plan
whose ceiling was Tier 2 in the first place.

> **The programme's brick sequence is therefore robust to leg 341's answer, and its CEILING is robust
> to leg 341's answer.** What leg 341 changes is whether anyone may later draft a Tier-2→Tier-3
> build — a question this plan does not own, does not schedule, and does not predict.

---

## 3. CLAUSE (b) — SOLVER ARCHITECTURE AND RPO EXTRACTION, WITH BUILD COSTS IN LEGS

### 3.1 The equations, written down

Backward self-similar variables about a putative singular point `(0, T)`:

```
u(x,t) = (T−t)^{−1/2} V(y,s),    y = x/(T−t)^{1/2},    s = −log(T−t)
```

`V` solves the dynamically rescaled Navier–Stokes system

```
∂_s V + ½V + ½(y·∇)V + (V·∇)V + ∇P = ΔV,        div V = 0
```

and, taking the curl (which removes `P` **before any projection is needed** — leg 332's S2 is
*vacuous*, not repaired), the **rescaled vorticity equation the solver actually integrates**:

```
∂_s Ω + Ω + ½(y·∇)Ω + (V·∇)Ω − (Ω·∇)V = ΔΩ,     Ω = ∇×V,   V = BS(Ω)
```

(the coefficient of the undifferentiated `Ω` is `1`: `½` from `curl(½V)` and `½` from
`curl(½(y·∇)V) = ½(y·∇)Ω + ½Ω`). **The drift is `+½(y·∇)`, the backward sign — leg 332's §10 rider,
inherited explicitly.**

**The object sought:** `Ω(·, s + S₀) = Ω(·, s)` with `S₀ = 2 log λ`, `λ > 1` **an output**; i.e. a
**periodic orbit of the rescaled flow**. Allowing the period map to close only up to a **rotation**
makes it a **relative** periodic orbit (RPO) — and an RPO of this flow is precisely a **rotating**
DSS solution, i.e. Pineau–Vicol `arXiv:2607.09619`'s "rotated backwards self-similar" class, whose
window leg 262 read at full LaTeX source (1869 lines, md5 `62c6bdae8e08cfd3ef4cdf17263ffcca`) and
measured **open**. That alignment is recorded as an observation, **not as an argument that the object
exists**, and it does not pre-empt leg 330.

### 3.2 The five modules — leg 260's list, unchanged in count, re-read live

Leg 260 §3.1's five must-build modules, carried:

| # | module | status in `capabilities.py`, **read live at leg 334** |
|---|---|---|
| M1 | 3D NS in similarity variables | **absent** — 0 of 49 indexed modules |
| M2 | 3D Leray / Biot–Savart | **absent** — the only Biot–Savart in the index is `solver/boussinesq_velocity.py`, **2D** |
| M3 | unbounded-domain discretisation carrying an algebraic far field with log-periodic oscillation | **absent** |
| M4 | a periodic-orbit search | **absent** — 0 occurrences of "periodic orbit" or "Newton-Krylov" in the index |
| M5 | a phase / gauge condition | **absent** |

**The standing grep-first ban is honoured and re-run at leg 334, not cited from leg 313**: 0 modules
hold a periodic-orbit search, 0 hold a Newton–Krylov solver, 0 hold a 3D velocity field, 0 hold a
Leray projection. The **one** partial precedent found is `solver/port_certification.py`, which holds
*"ProfileResidual, GMRES, Krylov ladders"* — a Krylov ladder for a **different operator** in a
**different formulation**. It is reusable as an implementation reference for M4's linear solve and
**nothing more**; it is not a periodic-orbit search.

### 3.3 The architecture, module by module

* **M3 (discretisation) — first, because everything sits on it.** Radial: leg 313's compactified
  `X = |y|/(1+|y|)` on `[0,1]`, in which the Type-I envelope is the **exact linear zero `(1−X)`**
  with `‖U‖_{L²(dX)} = √(1/3) = 0.577350`. Angular: real spherical harmonics up to `ℓ_max`;
  **non-axisymmetric by construction**, since the screened object is non-axisymmetric and leg 261
  is on record for having caught itself measuring on an axis where its witness vanished identically.
  **The open design question is the boundary singularity of §2.6**: whether to pay 823–14149 plain
  modes per unit `κ`, or to **enrich** the basis with explicit `(1−X)^{1−iκ}` blocks. B2's gate is
  exactly this comparison, against leg 313's table as the baseline.
* **M2 (Biot–Savart) — the nonlocal step, built to the NONLOCAL-OUTPUT RULE.** In the compactified
  variable, `V = BS(Ω)` is a radial ODE solve per `(ℓ, m)` mode (leg 332's witness-B construction is
  the exact 1-D template: `a'' + 4a'/r = 2e^{−r²}`, solved in closed form there). **Its output is
  required to be used only through `‖V‖_∞` and `‖∇V‖_∞`.** B3's gate fails if any assembled quantity
  needs `V` in the state norm as a standalone summand.
* **M1 (time stepping).** Integrating factor on the stiff linear part `(Δ − 1 − ½(y·∇))`, explicit
  on the nonlinearity. The `½(y·∇)` drift is a pure dilation in `X`, diagonal in a suitable variable.
* **M4 (RPO extraction) — the mature part.** Newton–Krylov (Newton–GMRES) with a **matrix-free**
  Jacobian formed by directional derivatives of the time-`S₀` map, wrapped in **multiple shooting**
  and continuation, with **`S₀` itself an unknown** in the Newton system. Precedents, all located in
  this leg's novelty pass with identifiers rather than counts: `1705.03720v2` (*Relative periodic
  orbits form the backbone of turbulent pipe flow* — RPO extraction in **3D NS** at research
  resolution), `1705.03838v2` (*The Openpipeflow Navier–Stokes Solver* — a published Newton–Krylov-
  with-hookstep code whose purpose includes finding periodic orbits of 3D NS), `1411.3303v4`
  (symmetry reduction, the "relative" in RPO), and the 22-year-old machinery leg 313 already banked
  (Sánchez–Net–García-Archilla–Simó, *J. Comput. Phys.* **201** (2004) 13–33, at NS discretisation
  dimension `O(10⁴)`, *"whose own guidance is that good initial conditions matter most"*).
  Leg 260's `arXiv:1406.1820` (Lucas & Kerswell 2014) is carried at **abstract level only**, exactly
  as leg 260 recorded it; **this leg did not upgrade that provenance and does not lean on it.**
* **M5 (phase/gauge).** Two constraints are needed, not one: a **temporal** phase condition pinning
  the origin of `s` on the orbit, and a **rotational** phase condition fixing the RPO's shift. Both
  are standard in the M4 precedents. **This is the module that is smallest to write and easiest to
  get wrong**, and B6's gate names a defective-phase-condition control that must be able to fail.

### 3.4 What is deliberately NOT in the architecture

* **No bifurcation off a fixed point of the rescaled flow, in any brick, in any form.** That is
  `plan_of_record.BANNED` Entry A, lift condition *"never"*, and §2.5 explains why the ban and the
  function space are the same fact.
* **No global, unseeded periodic-orbit trawl.** That is Entry B's named object, and its lift
  condition is the (a)/(b)/(c) triple; the wording question about whether it reaches a *seeded*
  search is the user's, undecided (§6).
* **No ℓ¹-Fourier / radii-polynomial certificate step anywhere** — leg 315's re-entry guard (§2.8).
* **No Gaussian-weight space** — §2.2.

### 3.5 Cost in legs — reported as a BRACKET, because a point estimate here would be dishonest

Leg 260 instructed that its construction floor *"should be re-read, not cited"*, and predicted it
would **fall**. It has now been re-read three times and has risen twice:

| read at | modules in `capabilities.py` | legs | legs/module (cumulative) | five-module floor |
|---|---|---|---|---|
| leg 260 | 48 | 260 | 5.4167 | **27** |
| leg 313 | 48 | 313 | 6.5208 | **≈ 33** (32.60) |
| **leg 334** | **49** | **334** | **6.8163** | **≈ 34** (34.08) |

**And the marginal rate is far worse than the cumulative one.** Between leg 260 and leg 334 the index
grew by exactly **one** module (`solver/interval_mp.py`, indexed by leg 312 at `d89bedd`) over
**74 legs** — a marginal rate of **74 legs per module**, i.e. a five-module floor of **≈ 370 legs**.

**Neither number is the cost of a module, and the plan says so rather than picking the flattering
one.** The cumulative rate averages over a period in which the repository was building modules; the
marginal rate is measured over a period in which it deliberately was not (legs 260–334 are dominated
by literature, adjudication and scoping legs). **The marginal rate measures the policy, not the
difficulty.** What is defensible is the bracket:

> **Five new modules cost somewhere between ~34 and ~370 legs on this repository's own measured
> rates. The uncertainty is a factor of ~11 and this leg cannot close it.** The operational
> consequence is stated in clause (d): **the programme cannot be scheduled to completion, and §5
> schedules only its first bricks**, with a re-read of this table required at each brick's landing.

### 3.6 Per-brick estimates, given with reasons rather than a rate

| brick | legs | why that number |
|---|---|---|
| B1 space/spectrum | 1 | quadrature + one eigenvalue solve on an existing-style 1-D operator; comparable to leg 331's own scope |
| B2 basis | 2 | a new `solver/` module plus a resolution study against leg 313's 823–14149 baseline |
| B3 Biot–Savart | 2 | new module; leg 332's witness-B closed form is the known-answer probe |
| B4 stepping | 2 | new module; needs its own known-answer probe with a window (lesson 84) |
| B5 NK basin (2-D known answer) | 2 | a 2-D periodic-box solver plus Newton–GMRES; the cheapest place the basin question is askable |
| B6 RPO layer | 3 | the largest single build; multiple shooting + two phase conditions + continuation |
| B7 screen | 1 | diagnostics only, on top of B2/B3 |
| B8 Tier-2 convergence study | 2 | ≥3 resolutions per `WIN_CONDITION.md`, and it only fires if B6 returns something |
| **sum of scheduled bricks** | **15** | against a calibrated five-module floor of **34–370** |

**The gap between 15 and 34–370 is real and is not explained away.** Three honest readings, all
recorded: (i) the per-brick estimates are optimistic in the way per-brick estimates always are;
(ii) the bricks do not build all five modules to the completeness leg 260's floor assumes — B1, B5
and B7 build no new `solver/` module at all; (iii) the calibrated floor is the better instrument for
*programme* cost and the per-brick table is the better instrument for *sequencing*, which is what
clause (d) needs. **The plan uses the per-brick table for sequencing only and quotes the bracket
whenever total cost is discussed.**

---

## 4. CLAUSE (c) — SEEDING: THE HONEST ACCOUNTING

### 4.1 The measured state of the seed set: STILL EMPTY

Leg 313's banked finding, quoted verbatim:

> **"THE SEED SET FOR THE SCREENED OBJECT IS EMPTY.** No published numerical DSS candidate for 3D NS
> survives the NRS/Tsai + axisymmetric screen, so a search 'seeded from a known numerical DSS
> candidate' has, today, nothing to be seeded from."

and the three-way failure of the one demonstrated seeded method's object, Hou `arXiv:2405.10916`:
**(1) axisymmetric** — killed by leg 253's composition of Chae–Wolf Thm 1.1 with the axisymmetric
Type-I exclusion; **(2) generalized, not NS** — solution-dependent viscosity, effective dimension
**≈ 3.188**; **(3) stationary, not time-periodic** — *"a fixed point of the rescaled flow, not a DSS
orbit."*

**This leg RE-MEASURED that emptiness rather than citing it** (`writeup/novelty/leg_334.md` §2). On a
battery leg 313 did not run, with controls in both directions:

* `"discretely self-similar" AND "Navier-Stokes" AND numerical` → **1 result**, and it is
  `2011.02800v1`, *On bifurcation of self-similar solutions of the **stationary** Navier-Stokes
  equations* — **not a backward blow-up candidate**.
* The 23-record backward-DSS-NS neighbourhood (`2607.09619v2`, `2409.13586v1`, `2202.08352v1`,
  `1610.09464v2`, `1610.05680v1`, `1510.07504v1`, …, all banked as identifiers in the novelty file)
  contains **existence, decay, rigidity and rough-data results for FORWARD DSS solutions — and no
  numerical computation of a backward DSS blow-up profile.**
* Controls pass in both directions: positive `all:electron` → 184814; negative nonsense phrase → 0;
  ANDed quoted phrases demonstrably non-empty (23). **So the zero is a MEASUREMENT and is banked as
  an absence**, per the standing rule that a controlled zero is not discarded.

> **CLAUSE (c) IS ANSWERED ON THE GATE'S SECOND BRANCH. There is no concrete, non-empty seeding
> strategy today. The seed set is empty, and this leg measured it empty independently.** What follows
> is the second half of that branch: what would create one.

### 4.2 S1 — continuation from Hou's object. **REJECTED: its last step is the banned entrance.**

Hou's own `ν₀`-continuation plan (drive `c_l(ν₀) → 1/2`, `n(ν₀) → 3`) would have to move **three**
parameters: viscosity model → true NS, axisymmetric → non-axisymmetric, **stationary → time-periodic**.
Route-A discipline forbids moving two at once, so it is a sequence of three one-parameter
continuations — and **the third one is the prohibited object**: continuing a *fixed point* of the
rescaled flow into a *periodic orbit* is exactly *"any attempt to obtain a DSS orbit by BIFURCATION
OFF A FIXED POINT of a rescaled flow (Hopf or otherwise), inviscid or viscous"*, `plan_of_record`
Entry A, lift condition **never**.

**S1 is therefore not available to this programme and no brick uses it.** This is recorded as
ban-compliance, not as a complaint: the plan did not need to reinterpret a ban, it needed to drop a
strategy, and it dropped it.

### 4.3 S2 — manufacture a seed by recurrent-flow extraction. **Contingent, and it re-opens leg 260's objection.**

Extract a near-recurrence from a long trajectory of the rescaled flow (Lucas–Kerswell shape) and hand
it to Newton. Leg 313 recorded that seeding *dissolves* leg 260's ergodicity objection — but if
recurrence extraction is what **makes** the seed, **leg 260's objection comes straight back**: the
method's substrate is *"an ergodically visited chaotic trajectory"*, and whether the rescaled 3D NS
flow supplies one is unmeasured. **It is measurable** (integrate from generic large data, look for
near-recurrences at any `Δs`) — but the measurement **presupposes the solver S2 is supposed to seed**,
so it cannot be an early brick. It is folded into B6 as an alternative seeding path, not a separate
brick, and it is contingent on the user's ban-wording ruling (§6).

### 4.4 S3 — a fixed-point argument around an approximate profile (Chen `arXiv:2605.15149`'s shape). **Not a seeding strategy.**

It requires the numerically constructed approximate profile as **input**. It is a *certification*
strategy, and §2.8 already says the certification step has no route here. Recorded so the plan is not
read as having three strategies where it has fewer.

### 4.5 S4 — an ansatz-driven cold start. **Available, and honestly labelled.**

Build `Ω₀` in the compactified variable from the structure that is known: the Type-I envelope (the
exact linear zero `(1−X)`), times a log-periodic factor with a **guessed** `κ`, times a
non-axisymmetric angular mode, with a **guessed** `λ`, and let Newton–Krylov converge or not.

**This is a cold start dressed as a seed**, and the plan says so. Newton's basin of attraction for an
`O(10⁸)`-DOF nonlinear system around a two-parameter guess is **unmeasured**, and there is no reason
on this record to believe it is non-empty. **But it is measurable, cheaply, somewhere else** — which
is the whole reason brick B5 exists and is scheduled early.

### 4.6 S5 — the critical-collapse entrance. **The novelty pass's find; a changed SHAPE, not a solved problem.**

This leg's novelty pass, weighted toward **old** prior art per the standing calibration, located
something not previously in this repository's record (checkable by grep: no repo file cites this
literature): **computing a discretely self-similar solution numerically, with the echoing period an
OUTPUT, is decades-old routine engineering in numerical relativity** — 40 records on `"discretely
self-similar" AND "numerical"`, overwhelmingly gravitational critical collapse, **including
explicitly non-spherical cases** (`1807.10342v2` *Aspherical deformations of the Choptuik spacetime*;
`2303.05530v1` *Critical phenomena in the collapse of quadrupolar and hexadecapolar gravitational
waves*; `2511.04649v2` *Twist and higher modes in complex scalar field threshold collapse*).

**And the entrance used there is neither of the two entrances this repository has banned.** The DSS
solution is found as the **intermediate attractor on a threshold**, located by **bisection on a
one-parameter family of initial data** — not by Hopf bifurcation off a fixed point (Entry A), and not
by a global periodic-orbit trawl (Entry B's named object).

**The disanalogy, at full strength, because it is decisive and softening it would fail this leg's own
gate:** the bisection works there because the DSS solution is **codimension-one on a threshold
between two known outcomes** (black hole / dispersal). **For 3D NS, the existence of such a threshold
presupposes blow-up — which is the very thing in question.** There is no known one-parameter family
of NS initial data with a known bifurcation of outcomes to bisect on.

> **So S5 changes the SHAPE of the seeding problem — from "find a seed" to "find a one-parameter
> family with a threshold" — and it does not make the seed set non-empty.** It is listed because the
> gate asks *what would create one*, and this is the most substantive answer available. **It is
> engineering precedent, not mathematics this leg claims**, and whether either DSS ban entry reaches
> a threshold-bisection entrance is a **wording question for the user** and is not decided here (§6).

### 4.7 What would create a non-empty seed set — three concrete items, in order of cost

1. **(c-i) A non-axisymmetric, true-NS, time-periodic-in-`s` numerical profile, from any source.**
   Currently **zero exist** (§4.1, measured twice). Cost: not this repository's to pay unless it
   builds it, which is the programme itself. *This item is the seeding problem restated, and it is
   listed first so nobody mistakes items 2 and 3 for solving it.*
2. **(c-iii) A measured Newton-basin radius for the RPO operator on a KNOWN-ANSWER substrate.**
   Buildable **now**, at 2-D cost: extract an RPO of 2-D Kolmogorov flow (Lucas–Kerswell's own
   object, where the answer is published) with the same Newton–Krylov + phase-condition layer, and
   measure how far the initial guess can be perturbed before Newton fails. **This converts S4 from a
   hope into a number**, and it is the cheapest thing on this list that could move clause (c). It is
   **brick B5**, and it is scheduled early and in a parallel slot for exactly this reason.
3. **(c-ii) A measurement that the rescaled 3D NS flow RECURS** (S2's precondition). Buildable only
   after B4, since it needs the solver. Folded into B6.

**None of these three is a claim that a seed will be found.** Item 1 is empty, item 2 measures a
method not an object, item 3 needs the solver first.

### 4.8 Clause (c) is drafted TO BE EXTENDED — leg 342 (ROUTE-SEED) is its second owner

The cycle-9 ruling also created **leg 342 (ROUTE-SEED)** to scope route 4's seeding problem in depth
— *"enumerate candidate seed sources — Hou–Luo-style 3D Euler near-singular data, PINN-discovered
profiles, whatever a controlled literature pass adds — screen them against leg 313's screen AND the
CHEAP-ENTRANCE BAN (in force: no bifurcation-off-a-fixed-point entrance may be smuggled in as a
seed), and cost creating a seed where none exists."* Its coordination clause states that **this leg
answers clause (c) on paper as drafted, with its gate text unedited, and leg 342's deeper scoping
consumes and extends that answer.**

**Three things §4 hands leg 342, and one warning.** Handed over: (i) the **independent
re-measurement** that the seed set is empty (§4.1) with its controls, so 342 need not re-establish
the baseline; (ii) the **S1 rejection** (§4.2) — the Hou-continuation route is dead *on the ban*, not
on feasibility, which is exactly the screen 342's own gate names, already applied to the leading
candidate; (iii) the **three creation items** (§4.7), of which (c-iii) is a scheduled brick. The
warning: **§4.6's critical-collapse entrance is the one item in §4 that has NOT been screened against
either ban**, because whether threshold-bisection is a third entrance or a re-description of a banned
one is a **wording question for the user** (§6). **Leg 342 should screen it and must not resolve the
wording question itself**, exactly as this leg did not.

---

## 5. CLAUSE (d) — THE BRICK SEQUENCE, SIZED THROUGH FOUR SLOTS OVER CYCLES

Nine bricks drafted; **eight dispatchable, one (B9) struck by the cycle-9 ruling and retained only as
a record.** **Every drafted gate below states the TIER 2 ceiling in its own text**, per the leg
spec's requirement; the wording is deliberately repetitive rather than cross-referenced, because a
brick is dispatched with its own gate and not with this file. **Two bricks carry hard preconditions
that are NOT this plan's to satisfy: B1 waits on leg 341, B6 waits on the user's ban-wording
ruling.**

### 5.1 The bricks, with drafted gates

**B1 — DSSP-SPACE (1 leg, no new `solver/` module). PRECONDITION: LEG 341 (ROUTE-ALGW) HAS REPORTED.
Do not dispatch before — leg 341 owns the weight question and B1 must consume its answer, not
re-litigate it (§2.0). B1's first action is to read 341's verdict and record which branch of §2.9 the
programme is in.**
*Gate (drafted).* **Does the targeted space hold the object and the operator? Specifically: (i) does
the weight-tolerance criterion `2p+s>d` reproduce leg 313's measured crossing at `s=1` and leg 331's
measured exponents (1.507674 / 2.012245 / 2.517908) when made executable; and (ii) is the spectrum of
the backward rescaled operator `−Δ + ½(y·∇) + 1` on the compactified basis CONTINUOUS, as Route-E §26
measured for gCLM, with a planted-eigenvalue positive control that could have come out otherwise?*
**yes →** the space is pinned and B2 proceeds. **no →** the space is wrong and clause (a) of the
programme plan is refuted; report which of (i)/(ii) failed and stop route 4.
**CEILING: TIER 2 — nothing in this brick is a proof, a certificate, or a Clay claim.**

**B2 — DSSP-BASIS (2 legs, new `solver/` module).**
*Gate (drafted).* **Does an enriched compactified basis resolve the `(1−X)^{1−iκ}` boundary block at
a lower mode count than leg 313's measured plain-Chebyshev baseline (823 at `κ=1`, 14149 at `κ=20`,
`n(κ) ≈ 791·κ^0.954`), at the same `1e-6` truncation, with the smooth-control separation (82.3× at
the cheapest `κ≠0` row) reproduced first?*
**yes →** report the factor and B3 proceeds on the enriched basis. **no →** report the factor
(possibly 1.0) and B3 proceeds on the plain basis at the baseline cost, which is then the programme's
resolution price.
**CEILING: TIER 2 — a basis is not a certificate; nothing here is a proof or a Clay claim.**

**B3 — DSSP-BS (2 legs, new `solver/` module).**
*Gate (drafted).* **Does Biot–Savart in the compactified variable stay on the MULTIPLIER side of the
nonlocal-output rule? Specifically: are `‖V‖_∞` and `‖∇V‖_∞` finite and measured on a
Type-I-enveloped `Ω`, and is leg 332's mapping bound `‖(V·∇)Ω−(Ω·∇)V‖ ≤ ‖V‖_∞‖∇Ω‖ + ‖∇V‖_∞‖Ω‖`
non-vacuous in the CHOSEN unweighted space (ratio strictly inside `(0,1)`, as leg 332 measured
0.10094 and 0.13863 in its own)?*
**yes →** the nonlocal step is safe and B4 proceeds. **no →** the nonlocal output has re-entered the
norm as a standalone summand, which is leg 331's measured failure mode transposed; report the
magnitude and route the blocker — do not tune the weight to hide it.
**CEILING: TIER 2 — a finite mapping bound is not a certificate; nothing here is a proof or a Clay
claim.**

**B4 — DSSP-STEP (2 legs, new `solver/` module).**
*Gate (drafted).* **Does the rescaled-vorticity time-stepper reproduce a KNOWN answer inside a stated
window? (Lesson 84: a known-answer probe has a window — state it before running.) The probe is a
decaying Leray solution, which in these variables must relax to the trivial state at a measured rate;
a planted non-trivial control must fail.*
**yes →** B5/B6 proceed. **no →** report the defect's magnitude and repair the stepper, not the
tolerance (leg 318's lesson).
**CEILING: TIER 2 — a converged time-stepper is not evidence of blow-up; nothing here is a proof or
a Clay claim.**

**B5 — DSSP-NKBASIN (2 legs, parallel slot; 2-D, shares no module with B2–B4).**
*Gate (drafted).* **Does the Newton–Krylov + phase-condition layer recover a PUBLISHED relative
periodic orbit of 2-D Kolmogorov flow, and what is the measured radius of its basin — i.e. how far
can the published initial guess be perturbed before Newton fails?*
**yes →** clause (c)'s item (c-iii) becomes a number and S4 becomes assessable. **no →** the
extraction layer does not work on an object where the answer is KNOWN, which refutes the "mature
engineering" premise of clause (b) on this repository's realization and stops route 4 before any
3-D cost is committed.
**CEILING: TIER 2 — recovering a known 2-D orbit says nothing about 3-D blow-up and is not a proof
or a Clay claim.**

**B6 — DSSP-RPO (3 legs). PRECONDITION: the user's ban-wording ruling (§6). Do not dispatch before.**
*Gate (drafted).* **Does the seeded Newton–Krylov / multiple-shooting layer, with `S₀ = 2 log λ` an
UNKNOWN and both phase conditions imposed, converge to a non-trivial relative periodic orbit of the
rescaled 3-D flow — and if it does not, what is the measured residual, condition number and
continuation arclength before failure?** (Leg 313 §3.3: a seeded continuation's failure **is** a
magnitude, which is what makes a negative here reportable in this repository's required form.)
A defective-phase-condition control must be able to fail, and the trivial solution `Ω ≡ 0` — which
closes every residual — must be excluded by an explicit non-triviality guard (**lesson 90**, and leg
331's own handling of `u ≡ 0`).
**yes →** a candidate exists and goes to B7's screen, **as a TIER 1 candidate at most**. **no →**
report the magnitudes; a costed negative is the deliverable.
**CEILING: TIER 2 — a converged orbit is a numerical candidate, NOT a proof, NOT a Clay answer.**

**B7 — DSSP-SCREEN (1 leg, parallel with B6).**
*Gate (drafted).* **Does every candidate carry its admissibility screen, computed at every Newton
step: `‖V‖_{L³(R³)}`, the fitted far-field decay exponent, `λ`, and an axisymmetry diagnostic — and
does the rigidity ledger (NRS/Tsai; Chae–Tsai, MEASURED SILENT by leg 326; Pineau–Vicol, PENDING leg
330) get machine-read rather than transcribed?**
**yes →** candidates are reportable with their exclusion status attached. **no →** no candidate may
be reported at all, because leg 332 measured `‖u_B‖_{L³} = 0.7307683991070311` for a well-behaved
witness — landing in `L³` is the default, not the exception.
**CEILING: TIER 2 — surviving the screen means "not already excluded by a published theorem", which
is not evidence for existence and is not a proof or a Clay claim.**

**B8 — DSSP-T2 (2 legs; fires only if B6 returns a candidate).**
*Gate (drafted).* **Does the candidate pass `WIN_CONDITION.md`'s Tier-2 bar — at least three
resolution levels, successive differences shrinking, the finest two `T*` estimates agreeing within
2%, and a self-similar profile check with stable exponents across resolutions?**
**yes →** **the output is a TIER 2 numerical candidate and NOTHING MORE.** `WIN_CONDITION.md`:
*"Passing Tier 2 is strong numerical evidence of a genuine singularity. It is still not a proof."*
**Escalation #3 applies**: if this reads like movement on the L1→L4 chain, it is parked for the user
and is not written into prose. **no →** the candidate was a resolution artefact and is reported as
one.
**CEILING: TIER 2 — this brick DEFINES the ceiling; passing it is not a Clay answer.**

**B9 — DSSP-CERT-SCOPE (drafted, NOT SCHEDULED — and SUPERSEDED by cycle 9; see the note below).**

> **STATUS NOTE, cycle 9.** B9 was drafted before the ruling that created leg 341. **Its subject
> matter is now leg 341's, and the build it might have licensed is the DM's own §3 build, drafted
> only after 341 reports and dispatched only under a USER ruling.** B9 is therefore **struck in both
> branches of §2.9** and is retained below **only as a record of what this leg thought the
> certification question was**, so that leg 341's report can be compared against it. **It must not be
> dispatched.** Two bricks owning one question is the failure mode this note exists to prevent.

*Gate (drafted).* **Does any apparatus reach the certification of a DSS orbit of the rescaled 3-D NS
system — given that (i) §2.2 measured the target outside the Gaussian-weight space where all
available machinery closes, (ii) leg 331 measured that machinery unable to hold one nonlocal operator
on its own space, and (iii) leg 315's `O1` mechanism encloses the flow of a finite-dimensional
autonomous ODE, which this object is not? FIRST CHECK, before anything else: does the proposal
introduce a sequence-space certificate step? If yes, it RE-ENTERS the re-posed Stage-V ban's scope
and STOPS (leg 315's re-entry guard, carried verbatim).*
**yes →** name the apparatus and its cost class; escalate, do not build. **no →** the Tier-2 ceiling
is confirmed as a measured fact and route 4's output is final at Tier 2.
**Not scheduled, and now struck**: on the measured record there was nothing for it to find,
scheduling it would have implied a Tier-3 route this plan does not have, and as of cycle 9 the
question is leg 341's. It is retained so the plan is honest about where Tier 3 would have to come
from, and so that leg 341's report has something to be checked against.
**CEILING: TIER 2 — this brick exists to CONFIRM the ceiling, not to raise it.**

### 5.2 The four-slot schedule

Route 4 occupies **one slot per cycle at steady state** (slot A, the critical path) with a **second,
parallel slot** used twice, for the two bricks that share no module with the main chain (B5, B7).
Slots B/C/D remain available to other routes throughout — the plan does **not** ask for the roster.

| cycle | slot A (route 4 critical path) | parallel slot (route 4, when used) | other slots |
|---|---|---|---|
| 9 | *(route 4 idle in slot A — **leg 341** must land first)* | **B5** DSSP-NKBASIN (2, starts) | free |
| 10 | **B1** DSSP-SPACE (1) — **only after 341 reports** | B5 continues | free |
| 11 | **B2** DSSP-BASIS (2, starts) | — | free |
| 12 | B2 completes | — | free |
| 13 | **B3** DSSP-BS (2) | — | free |
| 14 | **B4** DSSP-STEP (2) | — | free |
| 15 | **B6** DSSP-RPO (3) — **only if the user has ruled** (§6) | **B7** DSSP-SCREEN (1) | free |
| 16+ | B6 completes → **B8** DSSP-T2 (2), only if B6 returns a candidate | — | free |

**15 leg-units of route-4 work across ~8 cycles, never more than 2 of 4 slots at once.** Note the
consequence of the cycle-9 narrowing: **route 4's critical-path slot is IDLE in cycle 9**, because its
first brick now waits on leg 341. **B5 is unaffected — it is 2-D, shares no module with the main
chain, and does not depend on the weight question at all — so the parallel slot starts on schedule
and clause (c)'s item (c-iii) is not delayed by the narrowing.** That B5 is insensitive to leg 341 is
a property of the sequence, not a repair applied after the fact: B5 was placed early and in a
parallel slot before the narrowing existed, for the independent reason given in §4.7.

The schedule stops at B8 deliberately: **§3.5's cost bracket (34–370 legs for five modules, a factor
of ~11) means this programme cannot be scheduled to completion, and pretending otherwise would be the
kind of claim this leg exists to avoid.** The table is re-derived, not extended, at each brick's
landing, with `capabilities.py` re-read live each time (leg 260's instruction).

### 5.3 The two decision points that can stop route 4 early, by design

* **B5's no-branch** stops the route before any 3-D cost is committed, on the measurement that the
  extraction layer fails on a **known answer**.
* **B1's no-branch** stops the route on the measurement that clause (a)'s space is wrong.

Both are placed early on purpose. A programme with a Tier-2 ceiling and a factor-of-11 cost
uncertainty should be cheap to abandon, and this one is.

---

## 6. THE BANS, HONOURED ONE BY ONE

| ban (`plan_of_record.BANNED`) | how this plan stands |
|---|---|
| **DSS CHEAP ENTRANCE** — any attempt to obtain a DSS orbit by **bifurcation off a fixed point** of a rescaled flow, Hopf or otherwise, inviscid or viscous. Lift: **never** | **No brick does this.** S1 (§4.2) was the one strategy that required it and is **REJECTED for that reason**. §2.5 records that the ban and the function-space choice are the same fact: an algebraic weight gives continuous spectrum, and *"a continuum has no eigenvalue to move"* |
| **DSS EXPENSIVE ENTRANCE** — a **global** periodic-orbit search of a rescaled flow with **no fixed point nearby to seed it**. Lift: a scoping leg answering (a) space, (b) object, (c) price | Leg 313 answered the triple; leg 313 §5 also observed that **neither entry names a SEEDED search**, and correctly refused to decide the wording question, escalating it. **It is still undecided.** **This plan does not decide it either**, and makes it a hard precondition on **B6** — the first brick that runs a search at all. Bricks B1–B5 and B7 build and measure; none of them searches |
| **re-posed Stage V** — no ℓ¹-Fourier / radii-polynomial machinery on any model. Lift: a namable fourth space/basis with its own scoping leg | **No brick contains a certificate step.** Leg 315's re-entry guard is carried verbatim (§2.8). **The lift condition's "namable fourth space/basis with its own scoping leg" is EXACTLY leg 341's shape, and leg 341 — not this plan — is that scoping leg.** Nothing in §2 is offered as lift-condition evidence: §2.4 states explicitly that target-integrability is necessary and nowhere near sufficient, that the three-realization-death and CAP-formulation screens are 341's, and that **the ruling is the USER's** |
| **another gCLM measurement leg.** Lift: never | No brick measures gCLM. §2.6 **transcribes** gCLM statements from Route-E/H/I and leg 260 and re-derives none, and §2.6 explicitly declines to import gCLM's `κ = 430.35` into an NS cost |
| **building a solver without grepping `capabilities.py` first.** Lift: never | §3.2 re-ran the grep **live at leg 334** (49 modules; 0 periodic-orbit searches, 0 Newton–Krylov, 0 3-D velocity fields, 0 Leray projections; one partial precedent named) |
| every other entry printed by `plan_of_record.py` | reviewed; none is touched by a planning leg that builds nothing |

**`plan_of_record.py` was not edited, and this leg has no authority over it. No ban is lifted,
narrowed, re-interpreted or argued against anywhere above. Where a strategy required weakening a ban
(S1), the STRATEGY was dropped.**

---

## 7. HONEST CEILING AND LIMITS

* **TIER 2, in BOTH branches of leg 341's answer (§2.9).** §2.8: on the record as it stands the
  certification step has no known apparatus for this object, because the only weight class holding
  the target is algebraic and the only weight class where machinery closes is Gaussian, which leg 331
  measured intolerant of algebraic tails. **A completely successful programme ends with a numerical
  candidate that `WIN_CONDITION.md` says is not a proof.** Only a DM-drafted, 341-gated, user-ruled
  §3 build could ever change that, and it is not this plan's and is not scheduled here.
* **The weight question is NOT answered by this leg.** Per the cycle-9 narrowing it belongs to leg
  341, which had not landed. **§2.2–§2.5 are context offered to leg 341, marked conditional, and
  anyone citing them as a settled function-space result is citing them against their own stated
  status.** In particular §2.2's agreement with leg 260's banked sharp answer and leg 313's measured
  `s = 1` crossing is a **cross-check between three derivations, not a fourth independent
  confirmation** — the three are not obviously independent of each other, and §2.0 flags exactly this.
* **This leg cannot say whether the narrowing changed its own conclusions**, because it had already
  reached them under the broader framing when the narrowing arrived. The work was retained on the
  DM's instruction and re-labelled; **it was not re-derived under the narrower brief, and a reader
  should treat §2.2–§2.5 as having been written to answer a question this leg no longer owns.**
* **Nothing here is a measurement of Navier–Stokes.** This leg ran **no solver, built no module, and
  produced no numerical result about NS**. Its arithmetic is the exponent criterion `2p+s>d`, the
  cost table, and the novelty pass's queries. Every physical number quoted is **carried** from legs
  313, 331, 332, 326, 262 or 260, with its locator.
* **The `2p+s>d` criterion is a far-field statement, not a theorem about the object.** It says where
  an assumed algebraic tail is integrable. **That the NS DSS profile actually has a Type-I algebraic
  far field with a log-periodic block is a HYPOTHESIS** — leg 313 labelled it as such (*"that the NS
  far field genuinely carries a log-periodic block with a particular `κ` is hypothesis, and `κ`
  itself is unknown"*), and every consequence in §2.3 and §3 inherits that conditionality.
* **The `‖∇V‖_∞ < ∞` step of §2.4 is a hypothesis, not a measurement**, and is B3's gate rather than
  a claim.
* **Five routed items are NOT decided here** (§1): the weight question (leg 341's, undispatched at
  this leg's finish), the seeding question's deeper scoping (leg 342's), the ban-wording question
  (user's), leg 330's
  Pineau–Vicol adjudication (leg 330's), and the critical-collapse transfer's mathematical content
  (nobody's yet — §4.6 claims only engineering precedent).
* **The cost is uncertain by a factor of ~11** and §3.5 declines to pick a number.
* **The seed set is EMPTY and this leg did not fix it.** Clause (c) is answered on the gate's second
  branch. Anyone reading §4 as "seeding is solved" has read it backwards.
* **No external PDF was read at full text this leg.** The full-text readings this plan leans on are
  other legs' (262 on `2607.09619v1`; 326 on `1304.7414v1`), carried with locators.
* **`arXiv:2405.10916` (Hou) is still not read at full text by anyone in this repository**, and leg
  313's three-way screen of it is carried with that caveat intact.
* **No figure is registered by this leg.** It produced no measurement to plot, and
  `writeup/build_figures.py` is outside its declared territory and shared with nine live legs.
* **No BLOG sibling is shipped**, because the declared territory names *"a new TECHNICAL file of its
  own naming"* and adding a BLOG file would be a diff outside territory. The merge gate's docs
  contract binds BLOG → TECHNICAL, not the reverse.
* **No link of the L1→L4 chain moved. Walls 1 and 2 both stand — §2.7 notes the screened object is
  non-axisymmetric 3-D with no symmetry reduction available, squarely on the far side of Wall 2.
  Clay odds remain ~0.05%.**
