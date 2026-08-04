# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree**, so the plan is
> the source of truth and this file is its briefing. Stages `M` and `PORT` are **DONE**;
> **`C-PILOT` is NEXT.**

---

# DIRECTIVE 1 — ROUTE-C-PILOT: EVOLVE THE LYAPUNOV WEIGHT, ON A KNOWN-ANSWER OBJECT

**WHY THIS IS NOW THE LEG, AND THE EVIDENCE ARRIVED BY ACCIDENT.** Leg 46 built the
certificate on the uncertified 1D Hou–Luo profile and found that **closure is a property of
the SPACE, not of the object**. The tuned and naive weights differ in **one constant** — the
weight's length scale `w_l`, `0.01·X_max` against `X_max` — and that constant decides whether
the radii polynomial closes at all:

| `n` | tuned `Y₀/budget` | naive | gain |
|---|---|---|---|
| 201 | **1.95e−04** ✓ | 1.0125 ✗ | 5186.6 |
| 401 | **6.36e−04** ✓ | 3.3193 ✗ | 5221.5 |
| 801 | **2.40e−04** ✓ | 1.2578 ✗ | 5235.6 |

That was not gone looking for — it fell out of a table built for another purpose — and it is
the empirical case for this stage.

**THE SEARCH SPACE HAS ONE WALL ALREADY BUILT BY THE EQUATION.** `p* = 0.39` is not tuned:
the profile's own tail is `Ω ~ |X|^(c_ω/c_l) ~ |X|^−0.394`, so a weight `(1+X²)^(p/2)` with
`p > 0.394` makes the **true** profile's norm infinite. Search inside that box; do not
rediscover its wall.

**WHAT THE LEG MUST DELIVER.**
1. A **searched weight** beating the hand-picked one, on an object where the answer is
   **known** — Chen–Hou's 2D profile is the substrate for exactly this and it is the reason
   the 2D work is not wasted. Validate the fitness where the result is checkable before
   trusting it anywhere else.
2. The fitness is **one number** (the worst-case coercivity constant, or `Y₀/budget`) and it
   **cannot be faked by an under-resolved run** — that is the whole reason this target beats
   blow-up hunting. Say so, and gate it anyway.
3. **The six-property viability gate, re-run ON THE NEW FITNESS, before any GA compute.**

**GATE (pre-committed, in `plan_of_record.py`):** does the new fitness pass the six-property
viability gate? **YES** → proceed to stage `B`. **NO** → **STOP. Do not run the GA.** Stage
3.5 is the precedent and it is non-negotiable: a fitness that fails the gate produces
confident garbage at scale.

**BEFORE WRITING A SOLVER, GREP `capabilities.py` FOR THE OBJECT.** Leg 45 nearly rebuilt
`RescaledHLScenario2` from scratch. That ban is permanent.

---

# DIRECTIVE 2 — ROUTE-B: EVOLVE THE CERTIFICATE  *(after C-PILOT's gate says yes)*

The function space, the operator split, the constants — with fitness the radii polynomial's
margin, which is a theorem rather than a plot. **Gate: does the searched certificate beat the
hand-tuned one?** Either answer is reportable; a negative bounds how much of the difficulty
was tuning versus structure.

---

# THE TWO THINGS BETWEEN HERE AND A REAL RESULT — NAMED AND QUANTIFIED BY LEG 46

Do not let these slide out of the writeups. They are the ceiling and they are now numbers.

1. **INTERVAL ARITHMETIC.** Everything so far is float64 with `A = DF⁻¹`, so `Z₁` measures
   the *conditioning* of the discretized problem rather than bounding an operator norm on a
   function space. **It is a rehearsal, not a proof** — the boundary Route-D v16 drew.
2. **THE TRUNCATION BUDGET, AND IT IS 1.55e+08× OUT.** Leg 46's pre-committed clause P6b:
   `‖z(X_max=745) − z(X_max=2026)‖ = 1.831e−01` against a ball of `r_max = 1.18e−09`. **The
   certificate closes around the TRUNCATED object; the true one is eight orders of magnitude
   outside the ball.** "The polynomial closes" and "the ball does not contain the thing we
   care about" are both true at once. **Never report the first without the second.**

**CLAY.** Odds remain **~0.05%** behind Walls 1 and 2, and **no link of the L1→L4 chain has
moved in 46 legs.** Leg 44 opened a rung of the scaffolding and leg 46 ran the machine end to
end; neither is a chain link, and the writeups say so. Read `CLAY_ROADMAP.md` §7 (ADOPTED)
before proposing any new direction.

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

