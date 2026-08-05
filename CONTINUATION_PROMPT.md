# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`,
> `PORT`, `V`, `C-PILOT` and **`L1`** are **DONE**; **`T` is NEXT.** Stage `B` is still
> **blocked** — C-PILOT's gate answered **NO**, so the GA ban did not lift.

---

# DIRECTIVE 1 — ROUTE-T: THE TAIL LEMMA. MEASURE THE REPAIR BEFORE BUILDING ANYTHING ON IT.

`L1` closed at leg 51 with its gate answered **NO** and the term named: **the weight class
of the tail.** That is the branch `L1`'s own gate said to write up as the finding, and it is
written up (`TECHNICAL/BLOG_P2_ROUTEL1_V2.md`, `PHASE2_P2_NOTES` **§40**, fig46). `T` is
what leg 51 made possible, not a retry of it.

## What leg 51 settled, and do not re-derive it

The representation change **worked exactly as the plan predicted**. In Route-E's
compactified basis (`X = tan(θ/2)`, odd sines, now `solver/spectral_certificate.py`):

* **the operator gap is gone** — `H`, the dilation and the velocity are exact on the whole
  line, checked in exact rational arithmetic (defect 3.5e−15) and cross-checked against
  `solver/line_hilbert.py` with a `n^−1.00` refinement ladder;
* **`Y₀` is EXACTLY ZERO** — `Fraction(0)`, all 18 modes of the anchor's residual. Not
  small. Absent;
* **`Z₁` on the finite block is rigorous and tiny** (1.44e−10 at `K = 256`, `s = 1`) and
  **`Z₂` is finite from the basis algebra** (79.5). Three terms of four.

**And the fourth has no bound.** The tail operator's **diagonal is exactly zero** — the
unbounded part of the linearisation is the dilation **shift**, not a multiplier — and it is
**not injective**: its kernel is `h_m ~ m^{−2.007}`, i.e. the **`|X|^{−1}` far field**.
`‖T_tail⁻¹‖_w` diverges in every class tried: flat `M^{+1.28}`, algebraic best `M^{+0.64}`
at `s = 1`, geometric **×`ν` per neglected mode**. The window is **empty by 0.606 in
exponent units** (object needs `s < α = 0.394`, operator wants `s ≈ 1`) and no point of the
curve touches zero.

**The positive control is what makes that a measurement:** the same code path with `Λ¹`
dissipation saturates to exponent `+0.000` in every class. The machinery works the moment
the operator has a diagonal.

## T-0 FIRST: the novelty pass, before any construction

Leg 51 produced one methodological claim — *`ℓ¹`-Fourier radii-polynomial certification
needs the unbounded part of the operator to be a **multiplier**; inviscid self-similar
transport makes it a **shift** with zero diagonal* — and one **checkable prediction about
the shape of the field**: the certified self-similar blow-ups using this machinery
(Dahne–Figueras, CGL, `arXiv:2410.05480`) are **dissipative**, while the certified
**inviscid** ones (Chen–Hou) used weighted energy estimates over 145 pages instead.
**Check it.** If it is known, say so and drop the claim to a re-derivation. The novelty gate
has closed one stage (48) and narrowed two others (49, 51); do not skip it.

## T-1 THEN: border the tail with its own kernel, and measure

An operator that fails to be invertible by a **finite-dimensional kernel** is the classic
case for **bordering** — the same move that made the finite block work in Route-PORT (three
gauge freedoms → three border rows). Add the far-field mode(s) as explicit unknowns and the
transport's solvability functionals as border rows, **one per parity chain**, and measure
`‖T_tail⁻¹‖_w` on the **bordered** tail as a ladder in `M`, in the same three weight classes,
through the same code path. `solver/spectral_certificate.py` already carries the tail block
(`tail_block`), the homogeneous mode (`homogeneous_tail_mode`) and the dissipative control
(`dissipative_control`) — **if T-1 needs a new solver, the plan was wrong.**

**Gate:** does the bordered tail inverse stay bounded in `M`, in a class where the target
also has finite norm (`s < 0.394`)? **Yes** → `L1`'s no was about the standard construction
and not about the object; rebuild end to end on `HL_S2_nonsymmetric`, and re-run the ceiling
because the borders are new unknowns with their own `Y₀`. **No** → report which side failed
(bordered inverse still diverging = the kernel was not the whole obstruction; window still
empty = it was, but the class is), then **stop building `ℓ¹`-Fourier certificates for this
operator and say so in the plan.**

---

# DIRECTIVE 2 — THE TWO THINGS FROM EARLIER LEGS THAT ARE STILL LIVE

**STAGE `B` IS NOT NEXT, AND WHY.** It rested on one weight constant worth 5186×, therefore
*"closure is a property of the SPACE."* Leg 49 reproduced the effect (5604×) and **refuted
the explanation**: pin `c_l` with a border row instead of letting it come out implicitly and
the same weight change is worth **0.56×**. The weight was preconditioning the **border
rows**. The fitness also **failed its own viability gate 4/6**, and **no GA compute has
touched it** — `plan_of_record.py`'s GA ban is worded so it does not lift merely because the
stage closed. Two named repairs, both engineering: carry the *measured* lower wall in the
box, and state the fitness's defect tracking as a resolution (0.2% typical, 9% worst).
`solver/weight_search.py` + `test_weight_search.py` **8/8** hold all of it.

**THE CLAY CHAIN CANNOT BE CLIMBED AS WRITTEN** (`PHASE2_P2_NOTES.md` §24): `L1` a certified
1D toy profile — the only movable link, and leg 51 measured what stands in its way; `L2` 2D
Boussinesq — **Chen–Hou proved it**; `L3` axisymmetric 3D Euler with boundary — **Chen–Hou
proved that too**; `L4` 3D Navier–Stokes — Clay, out of reach by Wall 2. **The one
Clay-adjacent route was tried and is closed:** stage `V` was closed by its own novelty gate
at leg 48 (Dahne–Figueras verify CGL branches in interval arithmetic; leg 48 re-derived
their zeros to 1.8e−07, their branch to 3.0e−06, their fold to 3.8e−07).

---

# STANDING DISCIPLINE (applies to every leg)

Gate the **operator**, not the agreement. Report a **magnitude**, never a boolean. **"Small"
in which norm?** **Name the realization** (70). **Gate the quantity the measurement divides
by** (67). **Report the SHAPE of a ladder, not its endpoint** (72). **When a quantity has no
referent, say so instead of bounding it** (73). **Test all the suspects at once** (74).
**Two defects in the same problem are not the same defect** (75). **Keep the negative
construction in the artifact** (76). **A check that is not executable decays at the rate of
memory** (68). **A known-answer probe has a WINDOW, and the window is part of the probe**
(84). **Re-measure your own headline before building a stage on it, and ablate the
MECHANISM and not just the effect** (85). **A rigorous bound dominated by its own EVALUATION
error is a statement about the code** (86). **A certification method has a SHAPE, and the
shape is a property of the OPERATOR: multiplier or shift?** (87).

**PROCESS RULES THAT KEEP EARNING THEIR PLACE.** Before pushing: regenerate the data,
rebuild the figure, **check every number in the prose against the JSON**. When you commit a
convergence ladder, **read the residual column's direction**. **Run the ablation battery
before naming a suspect**, not after. **A negative result needs a positive control that can
report the other answer** — leg 51's dissipative dial is the template. And **grep
`capabilities.py` before building anything**.

**BANS ARE MACHINE-READABLE.** `plan_of_record.py` carries every ban with what lifts it;
`.venv/bin/python plan_of_record.py` prints the ones in force. Two are new: **do not sweep
another weight family before bordering the tail** (leg 51 swept nine algebraic exponents,
two geometric and flat — the curve has no zero), and **do not read leg 51's exactly-zero
`Y₀` as progress toward the target** (it is zero because the a=0 CLM profile *is* one basis
mode; the Hou–Luo profile is not).

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2. In 51 legs, **no link of the L1→L4
chain has moved.**

---

*Updated 2026-08-05 (session close). **THIS SESSION SHIPPED ROUTE-L1 v2 — the certificate
rebuilt where the operators are exact, and the wall that was left.***

**(L1v2-A) THE REPRESENTATION CHANGE DELIVERED WHAT IT PROMISED.** Two open-ended gaps
became one well-understood term: the operator gap vanished outright and `Y₀` went from
5.17e−12 to **exactly zero in rational arithmetic**. That is the first residual in this
project that is not a discretisation of anything.

**(L1v2-B) AND THE SURVIVING TERM IS UNBOUNDED IN EVERY STANDARD SPACE.** Tail diagonal
exactly `0.0`; kernel `= |X|^{−1}` far field at `m^{−2.007}` against a predicted `m^{−2}`;
geometric weights lose a factor `ν` **per neglected mode**. Leg 46's truncation gap and leg
47's wrong-sign reach trend were **this one mode seen through a grid** — two facts, one
object.

**(L1v2-C) THE CONTROL IS WHAT LICENSES THE NEGATIVE.** `Λ¹` dissipation saturates the same
code path in every class, and the geometric class needs **5× more of it** than the others.
The method is adapted to operators with a diagonal; inviscid transport has none.

**NOVELTY: nothing claimed, one prediction filed.** T-0 carries it. **No link of the chain
moved.**
