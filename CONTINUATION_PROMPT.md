# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`,
> `PORT`, `V` and `C-PILOT` are **DONE**; **`L1` is NEXT.** Stage `B` is **blocked** —
> C-PILOT's gate answered **NO**, so the GA ban did not lift.

---

# DIRECTIVE 1 — ROUTE-L1: CHANGE THE REPRESENTATION. DO NOT PUSH THE CURRENT ONE.

`L1` = certify `HL_S2_nonsymmetric` **for real** — the non-symmetric self-similar Hou–Luo
profile, reported by Chen–Huang–Li in April 2026 as *numerical only, no proof of any kind*.
**It is the only movable link of the chain** and it is a genuine, citable result if it lands.

## What leg 50 already did — step one is DONE

`solver/interval_certificate.py` wires `solver/interval.py` through the bordered residual.
**The radii polynomial closes in INTERVAL arithmetic at all three rungs**: rigorous
`Z₁ = 8.59e−09 / 5.71e−08 / 1.54e−07` at `n = 201/401/801`, all below 1, with
`Y₀/budget = 2.282e−03` at `n = 201` where the naive evaluation path gives 1.479 and fails.
The float expiry date leg 49 measured is no longer the binding constraint.

**But read the claim as leg 50 states it, and do not widen it.** It is a theorem about the
**finite-dimensional polynomial system with `H`, `D`, `Uop` taken as EXACT STORED DATA** —
not about the continuum profile.

## The two remaining gaps are the SAME gap, and it is the representation

1. **the truncation tail**, `|X| > X_max` — and leg 47 measured that reach makes it **worse**
   (+0.47 decades per unit `ρ`), so no domain size closes it;
2. **the operators** — `H`, `D`, `Uop` are finite-difference approximations being treated as
   exact.

**Both exist only because the certificate is built on a truncated finite-difference grid.**

## The move: rebuild the certificate in Route-E's compactified basis

`solver/rescaled_spectrum.py`, `X = tan(θ/2)` with odd sines. Its own docstring:

> *three operators are then exact on the whole line with **no truncation and no
> quadrature*** — `H(sin kθ) = −cos kθ + (−1)^k`, the dilation `X d/dX = sin θ d/dθ`, and
> `d/dX = (1+cos θ) d/dθ` — **and the velocity is exact too**, via
> `N_{k+1} = −2N_k − N_{k−1} − 2cos kt`.

Rebuild there and **gap (2) vanishes outright**, while **gap (1) becomes a spectral tail
bound on neglected Fourier coefficients** — which is the standard radii-polynomial move, not
a bespoke asymptotic enclosure. Two open-ended obstacles collapse into one well-understood
one.

## Expect the algebraic tail to bite — and that is the interesting part

`Ω ~ |X|^{−0.394}` is **non-smooth at `θ = π`**, so the sine coefficients decay
*algebraically* (`~k^{−1.4}`), not geometrically. `ℓ¹` still converges; **geometric `ℓ¹`
weights do not.** Two responses, in order:

1. **Factor the tail out** — `Ω = (1+X²)^{−p/2} Ψ`, so `Ψ` is smooth and its coefficients
   decay geometrically. Standard singularity-subtraction; try this first.
2. If that is not enough, **algebraic weights** — and note what that is: *"standard
   radii-polynomial work uses GEOMETRIC weights on bounded domains while ours is ALGEBRAIC
   decay on an UNBOUNDED one"* is **the one methodological claim Route-J's literature pass
   found NO hit for.** If the weight class is what blocks, **that is the contribution**, and
   it should be written up as a result rather than filed as a failure.

**Gate:** does the polynomial close in interval arithmetic, tail included? **Yes** → a novel
Tier-3 result on an uncertified object; report it as that and only that. **No** → stop and
report *which* term ran out of margin — the interval widening, the spectral tail, or the
weight class. **If it is the weight class, write it up.**

---

# DIRECTIVE 2 — WHAT LEG 49 SETTLED ABOUT STAGE `B`, AND WHY IT IS NOT NEXT

Stage `B` ("evolve the certificate") rested on one table from leg 46: one weight constant
worth **5186×**, therefore *"closure is a property of the SPACE."* Leg 49 tested that
claim on the known-answer object rather than assuming it.

* **The effect reproduces: 5604×.** It is not a one-object accident.
* **The explanation does not.** Pin `c_l` with a border row instead of letting it come out
  implicitly — a change of bookkeeping, not of mathematics — and the same weight change is
  worth **0.56×**. `‖A‖_w` goes 1.69e+08 → 1.69e+06 with the tuned weight *only when `c_l`
  is implicit*; pin it and that row of `A` is a unit vector the norm never sees.
  **The weight is preconditioning the BORDER ROWS, not choosing a function space.**
* **The fitness FAILED its viability gate, 4/6, and the GA was not run.** P2 finite 0.775
  < 0.90 (nine of forty weights have `Z₁ ≥ 1`); P3 `max|slope−1|` 0.092 > 0.05 against the
  known answer that `Y₀` is linear in an injected defect.
* **The analytic wall never binds.** `p* = 1` from the `1/X` tail was the one constraint
  the plan told the stage to respect; removing it entirely moves the optimum by
  **1.5e−04 decades**. The wall that binds had to be measured (see Directive 1).
* **A deterministic grid still beat the hand: 48,270× over naive, 8.61× over leg 46's
  constant** — and the win is almost entirely `Y₀`, from `w_l ≈ 0.99`, a factor **750**
  below `X_max` where the hand stopped at 100. **The hand had the right direction and
  stopped early.**

**If `B` is ever revived**, two repairs are named and both are engineering: carry the
*measured* lower wall in the box as the analytic one already is, and state the fitness's
defect-tracking accuracy as a resolution (0.2% typical, 9% worst) rather than assuming it
exact. `solver/weight_search.py` + `test_weight_search.py` **8/8** hold all of it.

---

# WHERE THE CLAY QUESTION LANDED — READ THIS BEFORE PROPOSING A NEW DIRECTION

The chain **cannot be climbed as written** (`PHASE2_P2_NOTES.md` §24):

* **`L1`** — a certified 1D toy profile. **The only movable link.**
* **`L2`** — 2D Boussinesq. **Chen–Hou proved it**, 145 pages.
* **`L3`** — axisymmetric 3D Euler with boundary. **Chen–Hou proved that too.**
* **`L4`** — 3D Navier–Stokes. Clay, and out of reach of interval arithmetic by Wall 2.

**AND THE ONE CLAY-ADJACENT ROUTE WAS TRIED AND IS CLOSED.** Stage `V` — *does a certified
inviscid blow-up survive dissipation, as a certificate?* — was closed by its own novelty
gate at leg 48: Dahne–Figueras (`arXiv:2410.05480`) verify whole branches of self-similar
singular CGL solutions in **interval arithmetic**, continued in the dissipation parameter.
Leg 48 re-derived their zeros to **1.8e−07**, their branch to **3.0e−06**, and their fold
to **3.8e−07**. **Do not weaken the novelty check, and do not skip it on whatever comes
next** — it has now closed one stage (48) and narrowed another (49, where SOS/neural
Lyapunov synthesis turned out to be an `ADJACENT` field and Chen–Hou §5.3.3 turned out to
be the hand procedure we were automating).

---

# STANDING DISCIPLINE (applies to every leg)

Gate the **operator**, not the agreement. Report a **magnitude**, never a boolean. **"Small"
in which norm?** **Name the realization** (70). **Gate the quantity the measurement divides
by** (67). **Report the SHAPE of a ladder, not its endpoint** (72). **When a quantity has no
referent, say so instead of bounding it** (73). **Test all the suspects at once** (74).
**Two defects in the same problem are not the same defect** (75). **Keep the negative
construction in the artifact** (76). **A check that is not executable decays at the rate
of memory** (68). **A known-answer probe has a WINDOW, and the window is part of the probe**
(84). **Re-measure your own headline before building a stage on it, and ablate the
MECHANISM and not just the effect** (85).

**PROCESS RULES THAT KEEP EARNING THEIR PLACE.** Before pushing: regenerate the data,
rebuild the figure, **check every number in the prose against the JSON**. When you commit a
convergence ladder, **read the residual column's direction**. **Run the ablation battery
before naming a suspect**, not after. And **grep `capabilities.py` before building
anything**.

**BANS ARE MACHINE-READABLE.** `plan_of_record.py` carries every ban with what lifts it;
`.venv/bin/python plan_of_record.py` prints the ones in force. Do not re-derive them here.

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2. In 49 legs, **no link of the L1→L4
chain has moved.**

---

*Updated 2026-08-05 (session close). **THIS SESSION SHIPPED ROUTE-C-PILOT v0 — a pilot
that failed its own gate, and was worth more for failing it.***

**(C-0) THE GATE ANSWERED NO AND THE BAN HELD.** 4/6 on the frozen predicate; **no GA
compute has touched this fitness**, and `plan_of_record.py`'s GA ban is re-worded so it
does *not* lift merely because the stage closed. The deterministic grid that property 6
needed anyway supplied the search result, so the ban cost the leg nothing but the right to
call it a GA result. `solver/weight_search.py`, `test_weight_search.py` **8/8**,
`experiments/p2_route_c_pilot_v0.py` → `writeup/data/p2_route_c_pilot_v0.json` → **fig44**;
`TECHNICAL/BLOG_P2_ROUTEC_PILOT_V0.md`; `PHASE2_P2_NOTES` **§38**.

**(C-1) THE PLAN'S NAMED SUBSTRATE COULD NOT SUPPLY THE FITNESS.** Chen–Hou's certified 2D
profile has no defect to take (§32: the relaxation limit-cycles, the residual grows under
refinement, `radii_polynomial_status` is `BLOCKED_AT_STEP_ONE`). Substituted the **a = 0
CLM profile** and got four known answers instead of one: the exact pair `(Ω₀, HΩ₀)`; two
ladders on two knobs (**spacing** converges the profile 4.13e−05 → 4.24e−07, **reach**
converges `c_ω` to −1 as `1/X_max`); the analytic wall gated against its own predicted
growth rate (×7.39 vs ×7.39); and an exact gauge invariance of the fitness, to 4.4e−16.

**(C-2) THE PROBE HAD A WINDOW AND THE FIRST VERSION WAS OUTSIDE IT.** P3's known answer
(slope exactly 1) holds only for `ε ≲ 1/‖A‖ = 5.9e−07`; applied at `ε = 10⁻²` it reported
0.63 and looked like a property of the fitness. **The threshold was not moved and P3 is
reported FAIL** — what the diagnosis bought is a *resolution*, not a pass: the fitness
tracks a defect to 0.2% typically, 9% at worst.

**(C-3) THE FLOAT REHEARSAL HAS AN EXPIRY DATE: n ≈ 3.2e+03.** See Directive 1's table.
This is the strongest quantitative case this project has produced for interval arithmetic,
and it arrived out of a property-2 diagnosis rather than from anyone looking for it.

**NOVELTY: nothing claimed.** `novelty_verdict()` returns `PROCEED_NARROW` off fourteen
queries — nothing searches the norm of a radii-polynomial certificate, but automatic search
for a *certificate* is mature (SOS / neural Lyapunov, barrier synthesis), so the idea is
not new, only its object. **No link of the chain moved.**
