# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M`,
> `PORT`, `V`, `C-PILOT`, `L1` and **`T`** are **DONE**; **`TC` is NEXT.** Stage `B` is still
> **blocked** — C-PILOT's gate answered **NO**, so the GA ban did not lift.

---

# DIRECTIVE 1 — ROUTE-TC: ASSEMBLE IT. THE TAIL IS BOUNDED; THE CERTIFICATE IS NOT WRITTEN.

Leg 52 answered `T`'s gate **YES**. That is the first gate in a while to open rather than
close, and the single most likely way to waste the next session is to read it as more than
it is. **It is one term of four, measured in isolation.**

## What leg 52 settled, and do not re-derive it

`L1` closed at leg 51 with the tail term unbounded in every weight class — window **empty by
0.606 in exponent units**. Leg 52 bordered the tail with the far field it cannot invert:

| class | admissible? | unbordered | **bordered (analytic)** | |
|---|---|---|---|---|
| flat `s = 0` | **yes** | 4.06 → 48.76 (`M^{+1.085}`) | **7.46 → 9.44** (`M^{+0.100}`) | **saturates** |
| algebraic `s = 0.3` | **yes** | 3.03 → 20.67 (`M^{+0.837}`) | **8.09 → 11.37** (`M^{+0.147}`) | **saturates** |
| algebraic `s = 1.0` | no | 1.64 → 3.94 (`M^{+0.379}`) | 9.89 → 20.51 | still growing |
| algebraic `s = 1.5` | no | 2.41 → 11.54 (`M^{+0.681}`) | 11.44 → 31.81 | still growing |

**The window is no longer empty** — the operator is bounded inside the band where the target
profile has finite norm (`s < α = 0.394`). Leg 51's NO was about the **standard
construction**, not about the object.

**Three things make that a measurement rather than a fit, and they are the reason to trust
it:**

* **the failing side was predicted before the ladders ran**, from the Fredholm structure
  alone — kernel `h_m ~ m^{−2.0024}` is in the space iff `s < 1`, cokernel `u_m ~ m^{+1.0012}`
  is a bounded functional iff `s ≥ 1`, so bordering *must* help below 1 and *must not* at or
  above it. Measured: saturates at `s = 0, 0.3`, grows at `s = 1, 1.5`;
* **the analytic border achieves the optimum** — `analytic / SVD` = 1.000 and 1.007 in the
  admissible classes, alignment `|cos| → 1.00000`. A proof cannot border with a singular
  vector it computed; it turns out it does not have to;
* **two negative controls diverge** — the second singular pair lands on **48.76, exactly the
  unbordered value**, so a wrong direction is asymptotically worth nothing.

**T-0 novelty: `PROCEED_NARROW`, and it narrowed.** Breden–Desvillettes–Lessard
(`arXiv:1503.06315`) state leg 51's problem in nearly leg 51's words for **tridiagonal
dominant** operators. **The general observation is not new.** Only the zero-diagonal Fredholm
case is possibly open, and whether their construction reaches it **was not resolved** (the
PDF did not extract). It is recorded as an open question, not as a gap in the literature.
Do not re-inflate the claim.

## TC — what is actually missing, and it is not compute

Leg 52 measured `‖B⁻¹‖_w` for the **tail block plus one border row and one border column.**
In a certificate that border is **a new unknown — the far-field amplitude —** and an unknown
appearing in the tail must also appear everywhere else:

* **TC-1 THE COUPLING.** One extra column in the finite block (how the amplitude feeds back
  into modes `1…K`), one extra row (the **matching condition** between the spectral series
  and the asymptotic expansion), tail bordered as leg 52 measured it.
  `solver/spectral_certificate.py` carries the tail side already —
  `bordered_tail_inverse_norm`, `tail_right_null`, `tail_left_null`,
  `tail_singular_pair`, `fredholm_sides`. **What is missing is the coupling.** If TC-1 needs
  a new basis, stop: leg 51 chose the basis and leg 52 measured the tail in it.
* **TC-2 THE FOUR TERMS IN THE SAME POLYNOMIAL, WHICH IS THE POINT.** Leg 51 gave `Y₀ = 0`
  exactly, `Z₁ = 1.44e−10`, `Z₂ = 79.5` — **on the finite block alone.** Leg 52 gives a tail
  constant of **9.44 / 11.37**. These have never been in the same polynomial and **the tail
  constant is not small next to `Z₂`.** Assemble and report whether
  `Z₂r² − (1−Z₁)r + Y₀ ≤ 0` has a root.
* **TC-3 THE BORDER'S OWN DEFECT.** The matching condition has a residual; it enters `Y₀`
  and has never been computed. Report it as a magnitude and say which term it dominates.

**Gate:** with the amplitude carried as a real unknown through all four terms, does the
polynomial close on the `a = 0` CLM object at `s < 0.394`? **Yes** → then re-run it on
`HL_S2_nonsymmetric`, whose profile is *not* one basis mode and whose coefficients decay
**algebraically**; claim nothing about the target before that run. **No** → report which term
ran out, and **do not repair it by tuning `s`** (lesson 88).

---

# DIRECTIVE 2 — THE THINGS FROM EARLIER LEGS THAT ARE STILL LIVE

**STAGE `B` IS NOT NEXT, AND WHY.** It rested on one weight constant worth 5186×, therefore
*"closure is a property of the SPACE."* Leg 49 reproduced the effect (5604×) and **refuted
the explanation**: pin `c_l` with a border row and the same weight change is worth **0.56×**
— the weight was preconditioning the **border rows**. The fitness also **failed its own
viability gate 4/6**, and **no GA compute has touched it**. Two named repairs, both
engineering. `solver/weight_search.py` + `test_weight_search.py` **8/8** hold all of it.

**THE CLAY CHAIN CANNOT BE CLIMBED AS WRITTEN** (`PHASE2_P2_NOTES.md` §24): `L1` a certified
1D toy profile — **the only movable link**, and legs 51–52 are the live work on it; `L2` 2D
Boussinesq — **Chen–Hou proved it**; `L3` axisymmetric 3D Euler with boundary — **Chen–Hou
proved that too**; `L4` 3D Navier–Stokes — Clay, out of reach by **Wall 2**. **The one
Clay-adjacent route was tried and is closed:** stage `V` was closed by its own novelty gate
at leg 48 (Dahne–Figueras verify CGL branches in interval arithmetic; leg 48 re-derived their
zeros to 1.8e−07, their branch to 3.0e−06, their fold to 3.8e−07).

**ONE FLAG A LATER LEG SHOULD CLEAR.** Leg 52's search log records that the query naming
`arXiv:2604.01868` (Chen–Huang–Li, April 2026 — the source of this project's target) **did
not resurface it**; only 2021–2023 Hou–Luo work returned. That is a statement about the
search index, not about the paper, and the repo's seventh-pass record stands. Re-check it.

---

# STANDING DISCIPLINE (applies to every leg)

Gate the **operator**, not the agreement. Report a **magnitude**, never a boolean. **"Small"
in which norm?** **Name the realization** (70). **Gate the quantity the measurement divides
by** (67). **Report the SHAPE of a ladder, not its endpoint** (72). **When a quantity has no
referent, say so instead of bounding it** (73). **Test all the suspects at once** (74).
**Two defects in the same problem are not the same defect** (75). **Keep the negative
construction in the artifact** (76). **A check that is not executable decays at the rate of
memory** (68). **A known-answer probe has a WINDOW** (84). **Re-measure your own headline
before building a stage on it, and ablate the MECHANISM and not just the effect** (85). **A
rigorous bound dominated by its own EVALUATION error is a statement about the code** (86).
**A certification method has a SHAPE, and the shape is a property of the OPERATOR: multiplier
or shift?** (87).

**NEW — LESSON 88. THE MINIMUM OF A FAILURE CURVE IS NOT WHERE TO REPAIR IT.** Leg 51 swept a
weight exponent, found a U-curve, and read its minimum (`s = 1`) as "closest to working". It
was the opposite: `s = 1` is where the kernel leaves the space at the same moment the
cokernel functional enters the dual, so it is the one exponent at which the failure is
*irreparable by bordering*. The repair works at `s = 0` and `0.3`, where the curve looked
worst. **Decompose a failure by MECHANISM before optimising along its parameter** — when two
mechanisms trade off, the optimum of their sum is the worst place to stand.

**PROCESS RULES THAT KEEP EARNING THEIR PLACE.** Before pushing: regenerate the data, rebuild
the figure, **check every number in the prose against the JSON**. **Run the novelty pass
BEFORE the construction, and commit the query log** — it has now closed one stage (48) and
narrowed three (49, 51, 52). **A negative result needs a positive control that can report the
other answer**, and a positive result needs **negative controls that can fail** — leg 52's
second-singular-pair and random borders are the template. **Run the ablation battery before
naming a suspect.** And **grep `capabilities.py` before building anything**.

**BANS ARE MACHINE-READABLE.** `plan_of_record.py` carries every ban with what lifts it;
`.venv/bin/python plan_of_record.py` prints the ones in force. Three are new: **do not read
leg 52's bounded tail as a certificate or as a statement about the target** (lifts at `TC`),
**do not tune `s` toward leg 51's curve minimum** (lesson 88), and **do not re-claim leg 51's
methodological finding at full strength** (T-0 narrowed it to a re-derivation).

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2. In 52 legs, **no link of the L1→L4
chain has moved.**

---

*Updated 2026-08-05 (session close). **THIS SESSION SHIPPED ROUTE-T v1 — the tail bordered
with the far field, and the window that was empty is not.***

**(T-A) THE REPAIR WORKS, AND IT WORKS WHERE THE CURVE LOOKED WORST.** Bordered tail bounded
at `s = 0` (**9.44**, against `M^{+1.085}` unbordered) and `s = 0.3` (**11.37**) — inside the
band where the target has finite norm. `L1`'s NO was about the construction, not the object.

**(T-B) THE MECHANISM WAS PREDICTED BEFORE IT WAS MEASURED.** Kernel `m^{−2.0024}` in the
space iff `s < 1`; cokernel `m^{+1.0012}` bounded iff `s ≥ 1`; the two swap at `s = 1`, so
bordering must fail there — and it does. **The alignment to the analytic far field is
1.00000 where the repair works and flatlines at 0.902 where it does not.**

**(T-C) THE CEILING WAS WRITTEN BEFORE THE NUMBERS.** A bounded bordered tail **is not a
certificate**: the border is an unknown with no column, no `Y₀` and no matching condition.
The object is still the `a = 0` CLM linearisation — one mode, analytic — so this bounds the
target's difficulty **from below**, exactly as leg 51's failure did.

**NOVELTY: the claim was narrowed, not banked. No link of the chain moved.**
