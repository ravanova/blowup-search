# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`,
> `PORT`, `V`, `C-PILOT`, `L1`, `T` and **`TC`** are **DONE**; **`MM` is NEXT.** Stage `B` is
> still **blocked** — C-PILOT's gate answered **NO**, so the GA ban did not lift.

---

# DIRECTIVE 1 — ROUTE-MM: THE MISMATCH. SPEND THE LAST FREE CHOICE, OR CLOSE THE LANE.

`TC`'s gate answered **NO** at leg 53. The four terms are now in one polynomial and it does
not close. **The term that ran out had never been computed before, because it does not exist
until the pieces are assembled.**

## What leg 53 settled, and do not re-derive it

Leg 52 bordered the tail and bounded it. Leg 53 gave the far-field amplitude its own column,
its own matching row and its own place in the polynomial. With the block-diagonal approximate
inverse the method requires, `A = Γ⁻¹ ⊕ A_tail`, the four sub-blocks of `I − A L` are:

| sub-block | flat `s = 0`, best split | `s = 0.3`, best split | trend |
|---|---|---|---|
| `Z₁[ΓΓ]` (float inverse defect) | 3.5e−16 | 7.7e−16 | fine |
| `Z₁[tail tail]` | 1.2e−12 | 6.0e−13 | fine |
| **`Z₁[tail←Γ]`** | **0.996** | **1.387** | **×2 per doubling of `K`** |
| **`Z₁[Γ←tail]`** | **59.0** | **43.15** | **×4 per doubling of `K`** |

Best split is `K = 4`; the sweep runs `K = 4 … 64`, both admissible classes (`s < α = 0.394`),
both gauges. **Smallest `Z₁` lower bound anywhere in that sweep: 43.15** (and **20.47** over every
normalisation of the augmented block ablated in TC-8). **Assembled `Z₁` at its minimum:
44.54.** `Y₀ = 0` exactly, so the polynomial's only root is `r = 0` and there is **no
positive interval** (`r_max = 0` in all ten rows). The same polynomial with leg 51's
finite-block `Z₁` alone *does* close (`r_max` 2.14e−02 … 4.64e−04) — **the difference between
those two columns is the whole leg.**

**SCOPE — SAY THIS EXACTLY, IT WAS OVERSTATED ONCE ALREADY.** `Z₁[Γ←tail]` **contains
`Γ⁻¹`** (it equals `2‖Γ⁻¹‖` to four digits in every row under the shipped convention), so what
is established is that the **block-diagonal `A` the method requires** cannot close this — not
that no finite block can. The genuinely finite-block-independent sub-block is `Z₁[tail←Γ]`, and
its minimum over the whole sweep is **0.9961, BELOW 1.** That is exactly why `MM` is a real
question.

**THE MECHANISM, CORRECTED AFTER VERIFIER'S REVIEW.** `‖Γ⁻¹‖` for the augmented block is
**exactly `2(K²−1)`** — `K²`, not `K` — and dropping the amplitude column restores **exactly
`4(K−1)`**. **The `K²` is created by the augmentation's weight pairing** (amplitude column
`≈ ‖ĥ‖_w ≈ K/2` against a matching row of weight `w_{K+1}`, so the matching equation carries
coefficient `≈ 2/K`). The coupling itself contributes a factor **2, not `K/2`**, and its
dominant column is the **rank-one row-1 term**, not the `(K+1)/2` sub-diagonal. TC-8 ablates
five normalisations plus the un-augmented block; smallest `Z₁` lower bound over all of them is
**20.47**, so the NO survives the renormalisation the corrected mechanism invites.

**The structural fact underneath is unchanged.** The standard tail estimate works because the
unbounded part is a **multiplier**: the split cuts an entry of size `Λ_M` and the tail inverse
is `1/Λ_M`. Here it is **off-diagonal** while the bordered tail inverse is a **constant**
(2.19 … 10.32 here, 9.44 in leg 52's ladder), not `1/K` — which is exactly the `×2` per
doubling measured in `Z₁[tail←Γ]`, reaching 38.2 by `K = 64`. Tuning `s` cannot touch it.

**The controls license the negative.** Positive: `Λ¹` dissipation, unbordered tail, no
far-field unknown (a dissipative tail has no kernel) — the coupling falls like `1/μ` and the
assembled `Z₁` reaches **0.9156 at `μ = 2`**. The instrument can say yes. Negative: the border direction is
**wired through the amplitude column**, so a wrong direction changes `Γ` and the control can
fail — `analytic/SVD = 1.0004`, random `13×` worse, the second singular pair `3.8e+13×` worse
(it makes the augmented block essentially singular). *The first version computed the coupling
from `Γ⁻¹` and `L_{Γ,tail}`, neither of which sees the border, and reported the resulting
identical number as the sharpest form of the result — a **tautology of the code**. Fixed.*

**TC-3, and it is the finding that was invisible before assembly.** The matching row's residual
at the anchor is exactly `0.0` (same degeneracy that gives `Y₀ = 0` — the anchor *is* one basis
mode). The expansion's truncation defect is 6.15e−02 / 1.10e−01, falling like `M^{−1.00}` /
`M^{−0.78}`. But the **gauge row's entry on the far-field column is log-divergent**: `Σ_m m h_m`
runs 3347 → 7222 over `M−K = 256 … 2048`, **+1865 per e-fold**, because the dilation gauge
`Σ_k k b_k` has dual norm `max_k k/w_k`, infinite for every `s < 1`. **The far-field column has
an entry that does not exist.** The repair is not a tuning: pin the exact dilation zero mode,
which is **exactly `e₂`** (`‖L e₂‖_∞ = 0.0`, checked). Worth 1.5×–8.7×. Gate still **NO**.

**TC-0 novelty: `PROCEED_NARROW`, six queries — and this leg's resurfacing clearance was
WITHDRAWN.** Leg 53 first reported leg 52's search-index flag as cleared; VERIFIER adjudicated
against LIT's ninth pass and **LIT wins. The flag STANDS.** Leg 53's query prepended the
literal arXiv ID, which tests retrieval *by ID* (never in dispute) rather than the **topical
recall** the flag was raised against; LIT re-ran leg 52's query **verbatim** and reproduced the
null result. Leg 53 logged **counts, not links**, so its claim could not be audited — *a later
pass must enumerate links.* BDL: leg 53 read the abstract only; **LIT's ninth pass settled it
from the full PDF** — assumptions (4)–(5) require a diagonal bounded away from zero, so the
zero-diagonal Fredholm case is outside their construction. Whether the literature treats an
*off-diagonal* unbounded part is recorded as **unchecked**, not as a gap.

## MM — what is actually left, and it is one thing

Every other degree of freedom is now measured and banned: `s`, the weight family, the split
`K`, the border direction. **The one remaining free choice is the SHAPE of `A`** — the method's
block-diagonal approximate inverse is exactly what makes the coupling a term at all.

* **MM-1 THE MISMATCH AS AN INEQUALITY, NOT A MOOD.** `Z₁ ≥ |1 − K/2| · (w_{K+1}/w_K) ·
  ‖A_tail e_{K+1}‖_w / w_{K+1}` holds for **every** finite block, because that sub-block does
  not contain `Γ⁻¹`. With leg 53's measured second factor (0.94 … 1.33) that is a statement
  that no block-diagonal `A` can work for this operator. Write it as one.
* **MM-2 THE ONE MOVE THAT IS NOT A TUNING.** An approximate inverse whose off-diagonal blocks
  are **not zero** — one step of block Gauss–Seidel across the split, or the Schur complement
  of the coupling — measured on the **same assembled object**
  (`experiments/p2_route_tc_v1_assemble.py`), with the same controls.
* **MM-3 THE NOVELTY PASS FIRST**, and commit the log.

**Gate:** does a non-block-diagonal `A` bring the assembled `Z₁` below 1, on the `a = 0` CLM
object at `s < 0.394`? **Yes** → report the assembled terms and the positive interval, then
re-run on `HL_S2_nonsymmetric`; claim nothing about the target before that run. **No** → **STOP
building `ℓ¹`-Fourier radii-polynomial certificates for inviscid self-similar transport and say
so in the plan** (that is `T`'s own no-branch), and do not re-enter by tuning `s`, the weight
family, the split, or the border.

---

# DIRECTIVE 2 — THE THINGS FROM EARLIER LEGS THAT ARE STILL LIVE

**STAGE `B` IS NOT NEXT, AND WHY.** It rested on one weight constant worth 5186×, therefore
*"closure is a property of the SPACE."* Leg 49 reproduced the effect (5604×) and **refuted the
explanation**: pin `c_l` with a border row and the same weight change is worth **0.56×** — the
weight was preconditioning the **border rows**. The fitness also **failed its own viability gate
4/6**, and **no GA compute has touched it**. Two named repairs, both engineering.
`solver/weight_search.py` + `test_weight_search.py` **8/8** hold all of it. Leg 53 sharpens the
warning: B's three degrees of freedom are the space, the **operator split** and the constants —
and leg 53 measured the split to be worthless as a dial (`K/2` for every choice).

**THE CLAY CHAIN CANNOT BE CLIMBED AS WRITTEN** (`PHASE2_P2_NOTES.md` §24): `L1` a certified 1D
toy profile — **the only movable link**, and legs 51–53 are the live work on it; `L2` 2D
Boussinesq — **Chen–Hou proved it**; `L3` axisymmetric 3D Euler with boundary — **Chen–Hou
proved that too**; `L4` 3D Navier–Stokes — Clay, out of reach by **Wall 2**. **The one
Clay-adjacent route was tried and is closed:** stage `V` was closed by its own novelty gate at
leg 48 (Dåhne–Figueras verify CGL branches in interval arithmetic; leg 48 re-derived their zeros
to 1.8e−07, their branch to 3.0e−06, their fold to 3.8e−07).

**FLAG STATUS.** Leg 52's search-index flag (`arXiv:2604.01868` not resurfacing) **STANDS** —
leg 53's clearance was withdrawn, LIT reproduced the null result on leg 52's verbatim query,
and fetching by ID has always worked. The BDL flag is **CLOSED** by LIT's ninth pass: their
assumptions (4)–(5) require a diagonal bounded away from zero, their LU construction divides by
it, and a vanishing diagonal is not on their own future-work list — **BDL does not cover the
zero-diagonal Fredholm case.**

---

# STANDING DISCIPLINE (applies to every leg)

Gate the **operator**, not the agreement. Report a **magnitude**, never a boolean. **"Small" in
which norm?** **Name the realization** (70). **Gate the quantity the measurement divides by**
(67). **Report the SHAPE of a ladder, not its endpoint** (72). **When a quantity has no
referent, say so instead of bounding it** (73). **Test all the suspects at once** (74). **Two
defects in the same problem are not the same defect** (75). **Keep the negative construction in
the artifact** (76). **A check that is not executable decays at the rate of memory** (68). **A
known-answer probe has a WINDOW** (84). **Re-measure your own headline before building a stage
on it, and ablate the MECHANISM and not just the effect** (85). **A rigorous bound dominated by
its own EVALUATION error is a statement about the code** (86). **A certification method has a
SHAPE, and the shape is a property of the OPERATOR: multiplier or shift?** (87). **The minimum
of a failure curve is not where to repair it** (88).

**NEW — LESSON 90. A CONTROL THAT CANNOT COME OUT DIFFERENTLY IS NOT A CONTROL, AND THE
TELL IS THAT ITS NUMBERS ARE *IDENTICAL*.** Leg 53 reported "the coupling is 546.57 for all
four border directions" as the sharpest form of its result. It was computed from two objects
neither of which references the border: a tautology of the code, presented as evidence. Four
identical numbers should have read as a bug, not as a finding. **Before quoting a control,
ask what would have had to change in the code for it to report the other answer** — and if the
answer is "nothing", wire the varied quantity through until there is one.

**NEW — LESSON 89. A TERM THAT DOES NOT EXIST UNTIL YOU ASSEMBLE CANNOT BE BOUNDED BY FIXING
THE TERMS THAT DO.** Legs 51–52 measured four terms of a certificate one at a time: three were
exact or tiny and the fourth was repaired. Assembling them produced a *fifth* quantity — the
coupling between the two blocks of the approximate inverse — which is 43 where it needs to be
under 1, and which no amount of further work on the original four can touch. **Assemble early,
even with placeholder constants: the terms you have not written down yet are the ones that
decide.** The corollary is positive, and leg 53 is the case: the assembly took one leg, and it
corrected the reading of two.

**PROCESS RULES THAT KEEP EARNING THEIR PLACE.** Before pushing: regenerate the data, rebuild
the figure, **check every number in the prose against the JSON**. **Run the novelty pass BEFORE
the construction, and commit the query log** — it has now closed one stage (48), narrowed four
(49, 51, 52, 53) and cleared one standing flag (53). **A negative result needs a positive
control that can report the other answer** — leg 53's dissipative control reaching `Z₁ = 0.9156`
is the template — and a positive result needs **negative controls that can fail**. **When a
control contradicts the mechanism, suspect the control's REALIZATION first**: leg 53's first
positive control failed because it bordered an *already invertible* dissipative tail with its
near-null pair, which is the wrong operator, not the wrong answer. **Run the ablation battery
before naming a suspect.** And **grep `capabilities.py` before building anything**.

**AND ONE MORE, EARNED THE HARD WAY THIS SESSION.** **A GROWTH RATE YOU CITE MUST BE
MEASURED ON THE MATRIX YOU ACTUALLY BUILT.** Leg 53 explained its own `‖Γ⁻¹‖` by citing leg
51's numbers for a *different* (unaugmented) matrix — 23× smaller at `K = 64` — and got the
exponent wrong (`K` instead of `K²`) and the responsible factor wrong (`K/2` instead of `2`).
The conclusion survived; the mechanism did not. **When a quantity has a suspiciously tidy
closed form (`2(K²−1)`, `4(K−1)`), that is the signal to check what produced it.**

**BANS ARE MACHINE-READABLE.** `plan_of_record.py` carries every ban with what lifts it;
`.venv/bin/python plan_of_record.py` prints the ones in force. Three are new: **do not read leg
53's assembled result as a statement about the target or as a failure of the TAIL term**, **do
not repair the coupling by tuning `s`, the weight family, the split or the border** (all four
measured), and **do not build further `ℓ¹`-Fourier machinery for this operator before `MM`'s
gate answers.**

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2.
In 53 legs, **no link of the L1→L4 chain has moved.**

---

*Updated 2026-08-05 (session close). **THIS SESSION SHIPPED ROUTE-TC v1 — the four terms in one
polynomial, and the term that ran out is the seam between them.***

**(TC-A) THE GATE ANSWERED NO, AND THE TERM IS NAMED.** `Z₁`'s block-coupling sub-blocks:
**43.15** at the best split in the whole sweep, **20.47** over every normalisation ablated,
against the **1** it must be under. Not the tail constant (2.19–10.32, well-behaved), not `Y₀`
(exactly 0), not `Z₂`. **Scope: the block-diagonal `A` the method requires cannot close it —
NOT that no finite block can** (the finite-block-independent sub-block bottoms out at 0.9961).

**(TC-B) THE MECHANISM IS THE SAME ONE, ONE LEVEL DOWN.** Leg 51: the method needs a multiplier
and this operator is a shift. Leg 52: bordering repairs the shift's *invertibility*. Leg 53: it
does not repair its *size*, and the size is what the seam needs. **Constant × `K/2` diverges for
every `s`.**

**(TC-C) THE CEILING HELD.** `Y₀` is exactly zero *including the new matching row*, for the
degenerate reason banked as a ban since leg 51: the anchor **is** one basis mode. Nothing is
claimed about `HL_S2_nonsymmetric` — on the gate's own terms that run happens only if the
polynomial closes here.

**(TC-D) AND THE REVIEW CAUGHT THREE THINGS THE LEG GOT WRONG** — the scope of the failure,
the mechanism behind the numbers, and a control that could not fail. All three are corrected in
place, with the wrong versions left visible. **The gate answer was independently confirmed and
did not move.**

**NOVELTY: nothing banked; the resurfacing clearance WITHDRAWN; the BDL flag closed by LIT.
No link of the chain moved.**
