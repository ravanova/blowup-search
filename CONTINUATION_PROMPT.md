# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`,
> `PORT` and `V` are **DONE**; **`ROUTE-C-PILOT` is NEXT.**

---

# WHERE THE CLAY QUESTION LANDED — READ THIS BEFORE PROPOSING A NEW DIRECTION

The user asked how to move a link of the L1→L4 chain toward Clay. Checked against the chain's
own definition (`PHASE2_P2_NOTES.md` §24): **it cannot be climbed as written.**

* **`L1`** — a certified 1D toy profile. Movable, and leg 45 found an *uncertified* target.
  **The only movable link.**
* **`L2`** — 2D Boussinesq. **Chen–Hou proved it**, 145 pages.
* **`L3`** — axisymmetric 3D Euler with boundary. **Chen–Hou proved that too.**
* **`L4`** — 3D Navier–Stokes. Clay, and out of reach of interval arithmetic by Wall 2.

The rungs above `L1` are occupied or unreachable. **Stop using "toward Clay" as though the
ladder carried you there.**

**AND THE ONE CLAY-ADJACENT ROUTE WAS TRIED AND IS CLOSED.** Stage `V` — *does a certified
inviscid blow-up survive dissipation, as a certificate?* — was proposed as the only route both
Clay-adjacent and matched to this project's holdings, and adopted by user direction. **Its
novelty gate closed it at leg 48.** Dahne–Figueras (`arXiv:2410.05480`) verify whole branches
of self-similar singular solutions of complex Ginzburg–Landau in **interval arithmetic**,
continued in the dissipation parameter from the conservative limit. Leg 48 re-derived their
published zeros to **1.8e−07**, reproduced their branch to **3.0e−06** across its length, and
located their fold at `ε* = 0.0606364` against their figure's `0.0606361`.

**That gate is the single most valuable thing in the plan machinery.** It cost one leg and it
prevented building a measurement on a question already answered rigorously by other people —
the exact failure leg 42 found seven times over. **Do not weaken it, and do not skip the
novelty check on whatever comes next.**

---

# DIRECTIVE 1 — ROUTE-C-PILOT: EVOLVE THE LYAPUNOV WEIGHT, ON A KNOWN-ANSWER OBJECT

**THE EVIDENCE FOR THIS STAGE ARRIVED BY ACCIDENT, WHICH IS WHY IT IS WORTH TRUSTING.** Leg
46 built the certificate on the uncertified 1D profile and found that **closure is a property
of the SPACE, not of the object**. The tuned and naive weights differ in **one constant** —
the length scale `w_l`, `0.01·X_max` against `X_max` — and it decides whether the radii
polynomial closes at all:

| `n` | tuned `Y₀/budget` | naive | gain |
|---|---|---|---|
| 201 | **1.95e−04** ✓ | 1.0125 ✗ | 5186.6 |
| 401 | **6.36e−04** ✓ | 3.3193 ✗ | 5221.5 |
| 801 | **2.40e−04** ✓ | 1.2578 ✗ | 5235.6 |

That fell out of a table built for another purpose. **Route-D hand-tuned a function space for
eleven legs and it turned out `a = 0`-only; Routes K and L hand-picked preconditioners.** Those
are search problems being done by hand, and unlike blow-up hunting they have a fitness that
**cannot be faked by an under-resolved run** — "does the polynomial close, and by how much" is
a theorem, not a plot.

**THE SEARCH SPACE HAS ONE WALL ALREADY BUILT BY THE EQUATION.** `p* = 0.39` is not tuned: the
profile's tail is `Ω ~ |X|^−0.394`, so any weight `(1+X²)^(p/2)` with `p > 0.394` gives the
**true** profile infinite norm. Search inside that box; do not rediscover its wall.

**WHAT THE LEG MUST DELIVER.**
1. A **searched weight** beating the hand-picked one **on an object where the answer is
   known** — Chen–Hou's 2D profile is that substrate, and it is the reason the 2D work of legs
   43/44 is not wasted. Validate the fitness where the result is checkable before trusting it
   anywhere else.
2. The fitness is **one number** and it cannot be faked. Say so, and gate it anyway.
3. **The six-property viability gate, re-run ON THE NEW FITNESS, before any GA compute.**

**GATE (pre-committed in `plan_of_record.py`):** does the new fitness pass the six-property
viability gate? **YES** → proceed to stage `B`. **NO** → **STOP. Do not run the GA.** Stage
3.5 is the precedent and it is non-negotiable: a fitness that fails the gate produces
confident garbage at scale.

**AND THE NOVELTY CHECK IS NOT OPTIONAL HERE EITHER.** Leg 48 is what that habit is worth —
one leg spent, an entire stage correctly closed. Before building, ask whether searching
certificate function spaces has been done; use Route-M's ledger machinery.

**BEFORE WRITING A SOLVER, GREP `capabilities.py` FOR THE OBJECT.** Leg 45 nearly rebuilt
`RescaledHLScenario2` from scratch. That ban is permanent.

---

# DIRECTIVE 2 — L1: THE ONLY MOVABLE LINK, AND `V`-RIGOROUS'S PREREQUISITE

Leg 46 closed the polynomial in float on `HL_S2_nonsymmetric` — an object with **no proof of
any kind**. Two things stand between that and a real result, and leg 47 priced both:

1. **INTERVAL ARITHMETIC.** `solver/interval.py` exists as an arithmetic layer and **has
   never been wired to a certificate**. Until it is, `Z₁` measures float *conditioning*
   rather than bounding an operator norm.
2. **A TAIL LEMMA — forced, not optional.** A rigorous bound for `|X| > X_max` from the
   asymptotic expansion, folded into the budget. **Leg 47 measured that reach makes the gap
   WORSE (+0.47 decades per unit `ρ`)**, so there is no domain size at which brute force
   closes it.

**Gate:** does the polynomial close in *interval* arithmetic, tail included? **Yes** → a novel
Tier-3 result on an uncertified object; report it as that and only that. **No** → stop and
report *which* term ran out of margin, the interval widening or the tail. Either answer
prices the road.

---

# WHAT LEG 47 SETTLED, AND IT RE-PRICES `L1`

Leg 46 left one number unmeasured. Leg 47 measured it, on a pre-committed predicate with both
branches actionable. Holding `dρ` fixed and varying reach only:

```
d log10(distance) / dρ  =  −0.0196      the gap does NOT shrink
d log10(r_max)    / dρ  =  −0.4899      the ball shrinks fast
d log10(ratio)    / dρ  =  +0.4703      so reach makes it WORSE
```

**Extending the domain cannot close the truncation gap at any size — the trend has the wrong
sign.** `ρ = 10` is **28× worse** than `ρ = 6`. Both of the earlier guesses were wrong, in
opposite directions: the distance is flat (an algebraic far field keeps exposing more
un-resolved tail), and the ball shrinks because the tuned weight `w_l = 0.01·X_max` grows *by
construction*.

**So `L1` now costs: interval arithmetic** (engineering — `solver/interval.py` is an
arithmetic layer that has never been wired to a certificate) **plus an analytic far-field
enclosure** (mathematics, forced, and nobody here has written one). **"Just refine" is banned
in `plan_of_record.py` and this is why.**

---

# STANDING DISCIPLINE (applies to every leg)

Gate the **operator**, not the agreement. Report a **magnitude**, never a boolean. **"Small"
in which norm?** **Name the realization** (70). **Gate the quantity the measurement divides
by** (67). **Report the SHAPE of a ladder, not its endpoint** (72). **When a quantity has no
referent, say so instead of bounding it** (73). **Test all the suspects at once** (74).
**Two defects in the same problem are not the same defect** (75). **Keep the negative
construction in the artifact** (76). **A check that is not executable decays at the rate of
memory** (68) — which is why the plan, the literature check and now the inventory are all
code.

**PROCESS RULES THAT KEEP EARNING THEIR PLACE.** Before pushing: regenerate the data,
rebuild the figure, **check every number in the prose against the JSON**. When you commit a
convergence ladder, **read the residual column's direction**. **Run the ablation battery
before naming a suspect**, not after. And **grep `capabilities.py` before building
anything** — leg 45's own second finding.

**BANS ARE MACHINE-READABLE.** `plan_of_record.py` carries every ban with what lifts it;
`.venv/bin/python plan_of_record.py` prints the ones in force. Do not re-derive them here.

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2. In 45 legs, **no link of the L1→L4
chain has moved.** Leg 44 opened a rung of the *scaffolding*; leg 45 re-aimed it at an
object worth certifying. Neither is a link.

---

*Updated 2026-08-04 (session close, fourth update). **THIS SESSION SHIPPED ROUTE-M v1 — the
target-selection leg. It cost this project its target, and gave it a better one.***

**(M-0a) THE PORT WAS AIMED AT A CERTIFIED OBJECT FOR TWENTY LEGS.** Chen–Hou proved the 2D
Boussinesq profile in arXiv:2210.07191 + Part II. Closing a radii polynomial there would
have demonstrated capability and produced no result. `solver/target_selection.py` +
`test_target_selection.py` **9/9**; `experiments/p2_route_m_v1_targets.py` →
`writeup/data/p2_route_m_v1_targets.json` → **fig42**; `TECHNICAL/BLOG_P2_ROUTEM_V1.md`;
`PHASE2_P2_NOTES` **§34**.

**(M-0b) GATE: YES. FOUR UNCERTIFIED OBJECTS, RANKED BY CONTRIBUTION.** Named target
`HL_S2_nonsymmetric` (see Directive 1), at **1.11e−3** of the certified object's unknown
count. Behind it: gCLM one-scale from degenerate data `a>0` (arXiv:2603.25104 §4 — the
cheapest object on the list at 602 unknowns, ranked *second* on purpose, and
`test_target_selection.py` fails if the ledger is ever re-sorted by cost); the same
non-symmetric phenomenon in 2D (arXiv:2604.01868 §6.2); and the stability of the singular
steady state (their Conjecture 2.4 — blocked on a function space, since the profile is
unbounded and only in `L^p` for `p<2`).

**(M-0c) THE EXCLUSION LIST IS THE LOAD-BEARING HALF, AND IT GREW.** Seven objects proved,
**four of them analytically** — including **arXiv:2305.05895, which closes the entire smooth
gCLM branch for all `a ≤ 1` by hand**, i.e. the branch Routes D/E/F spent a dozen legs
measuring; and **arXiv:1908.09385, checked and found to contain no computer assistance at
all**, so it is an exclusion and not a CAP precedent. `LITERATURE_CHECK.md` **seventh pass**
is the table.

**(M-0d) "WITHIN REACH" IS NOW A NUMBER: the `Y₀` BUDGET `(1−Z₁)²/(2Z₂)`.** The largest
residual a certificate can tolerate. Gated against Cadiot–Lessard–Nave (arXiv:2302.12877)
Thm 6.6: our algebra returns their published Kawahara `r₀` from their `Y₀` with relative
error **0.0**. Their spaces are **Hilbert/Fourier `H^l`, not weighted `ℓ¹`**, so Route-D's
weighted-`ℓ¹` no-go is **narrowed, not closed**.

**(M-0e) THE 3D NAVIER–STOKES CLAIM (arXiv:2604.09949), AUDITED RATHER THAN ASSUMED.** Its
scalar closure recomputed as printed (`2δMK = 8.9e−5`) and in the form Kantorovich requires
(`2M²Kδ = 4.3e−2`): **both close**, with 23× margin, and its `K` reproduces from its own
factors to 2.2e−4. **The arithmetic is not where it fails** — recorded that way on purpose
(76). It is unusable because no verification package is released (its appendix F: the
package "is intended to contain" its contents) and because its Thm 12.1 reconstructs the
**backward** self-similar ansatz excluded by Nečas–Růžička–Šverák / Tsai under the decay its
own analytic weight implies; its reference list cites Jia–Šverák on **forward** self-similar
solutions and neither non-existence result.

**(M-0f) THE SECOND FINDING IS ABOUT US, AND IT IS THE SAME SHAPE AS THE FIRST.**
`RescaledHLScenario2` — the solver for the newly named target — was built **2026-07-26**,
validated, described in the notes as "the validated brick", and then left unused for nine
legs while the port aimed at a certified object. It was found this leg by grepping for an
arXiv number. **The missing thing was an index of what exists**, so this leg shipped
`capabilities.py` (35 modules: object, what it holds, the strongest known-answer gate *with
the magnitude*, its test) + `test_capabilities.py` **5/5**, which fails if a module has no
entry, an entry has no file, or a `validated` field is too thin to say what was checked —
that last gate rejected **fourteen** of our own entries on first run.

**NOVELTY: nothing claimed.** Naming an object as uncertified is a statement about the
literature in `Papers/MANIFEST.md`. No `Y₀`, `Z₁` or `Z₂` was computed for any candidate.

---



