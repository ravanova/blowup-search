# Continuation prompt (copy into a fresh session)

> ## 📉 THIS FILE WAS 2196 LINES AND IS NOW UNDER 400, BY DESIGN (leg 45).
> It had become append-only: a session-close block per leg back to ~38, each duplicating a
> `PHASE2_P2_NOTES.md` section verbatim. **The history did not move — it was always in the
> notes.** `test_plan_of_record.py::test_8` now fails if this file exceeds 400 lines or
> carries more than **two** session-close blocks. A briefing nobody can read is a briefing
> nobody reads, and the cost lands where context is scarcest: the first ten minutes.

**FIRST THREE COMMANDS OF EVERY SESSION.**

```
.venv/bin/python plan_of_record.py        # which stage is NEXT, its gate, the live bans
.venv/bin/python test_plan_of_record.py   # FAILS if the plan and the docs have drifted
.venv/bin/python capabilities.py <object> # WHAT IS ALREADY BUILT -- grep before you build
```

The third one is new and it is not optional. Leg 45 came within about ten minutes of
rebuilding a solver that had been sitting in `solver/hl_rescaled.py`, gated to 4.4e-16,
since 2026-07-26. **Before building anything, search `capabilities.py` for the object.**

---

# DIRECTIVE 1 — ROUTE-PORT: THE BORDERED SYSTEM, RE-AIMED AT THE 1D NON-SYMMETRIC PROFILE

**WHAT CHANGED, AND IT IS THE WHOLE POINT.** Leg 45 (Route-M) asked "certify WHAT, that
isn't already done?" and the answer for the port's target was: **Chen–Hou certified it
themselves in 2022** (arXiv:2210.07191 + Part II). Twenty legs of certification machinery
were aimed at a solved problem. **The target has changed. The machinery has not.**

**THE NAMED TARGET.** `HL_S2_nonsymmetric` — the **non-symmetric positive regular
self-similar profile of the 1D Hou–Luo model**, Chen–Huang–Li arXiv:2604.01868 §2.5 and §4.
Reported April 2026 as "a previously unreported blowup phenomenon". Numerical only. No
proof, computer-assisted or otherwise, and it is **not** covered by Chen–Hou–Huang (odd,
non-degenerate) or by Huang–Qin–Wang–Wei's analytic construction — both use the symmetry.

**WHY IT IS THE RIGHT ONE, IN ONE SENTENCE A SPECIALIST WOULD ACCEPT.** In every existing
proof of this kind, in Chen–Huang–Li's own words, *"the origin always acts as the source of
stability"*. This profile has **no symmetry point**, so the translation degree of freedom
has to be carried by the certificate itself — their formulation (2.9)/(4.1) adds a third
modulation constant `c_r` for exactly that. **A first certificate for a profile with no
symmetry to anchor it is a methodological result, not another profile.**

**WHAT THE LEG MUST DELIVER.**
1. **The bordered residual for CHL (4.1) with all THREE constants `(c_l, c_ω, c_r)` as
   unknowns.** Bordered from the start. **Do NOT project after the fact** — leg 44 (L-7)
   tried that on the 2D object and Newton accepted no step at all, `λ` down to 1/1024.
2. **A converged profile**, checked against the *normalization-independent* constant:
   `c_l/c_ω` vs CHL's **−2.5114**. The absolute triple `(1.0636, −0.4235, 0.0765)` depends
   on their initial normalization and ours will not match it — that is not an error, and
   §8 of the notes already documented it.
3. **Then `Y₀`, `Z₁`, `Z₂`** — now *measurable* against a budget, because
   `solver/target_selection.py::y0_budget` computes `(1−Z₁)²/(2Z₂)`, the largest residual a
   certificate can tolerate, and it is gated against Cadiot–Lessard–Nave's completed
   Kawahara certificate (their published `r₀` reproduced exactly).

**WHAT YOU ALREADY HAVE — DO NOT REBUILD IT.**
* `solver/hl_rescaled.py::RescaledHLScenario2` — CHL's (4.1)/(4.2), three-constant
  origin-pinned gauge, hand-rolled 3×3 solve. Gauge nulls `∂_τ{Ω(0), Ω_X(0), V(0)}` to
  **4.4e-16**. `test_hl_rescaled.py` 9/9.
* `line_hilbert.slope_matrix` — leg 45 made the Scenario-2 step **10× faster** (43 ms →
  4.2 ms at n=801) by caching the spline slope operator. Gated at 2.7e-13.
* `solver/interval.py`, `solver/nk_bounds.py`, `solver/op_lower.py` — the certificate side.
* `solver/target_selection.py` — the ledger, the budget algebra, the certification record.

**GATE, PRE-COMMITTED.** *Does the radii polynomial close in float, with margin?*
**Yes** → report it; stage C-PILOT can use it as a validated fitness.
**No** → **STOP AND REPORT — do not harden.** A negative here is worth more than a positive
anywhere else, because it is about the object certification results actually count on.

---

# DIRECTIVE 2 — C-PILOT: EVOLVE THE LYAPUNOV WEIGHT, ON A KNOWN-ANSWER OBJECT

*(queued behind PORT; see `CLAY_ROADMAP.md` §7 and `plan_of_record.py`)*

For 44 legs the search machinery was pointed at finding the **object**; the bottleneck since
Route-D has been closing a **certificate** around an object we already have. Route-D
hand-tuned a function space for **eleven legs** and it turned out `a = 0`-only; Routes K and
L hand-picked preconditioners. Those are search problems with a fitness that **cannot lie**.

The weight is the narrowest member of the family: fitness = the **worst-case coercivity
constant** of the linearized operator under that weight. One number, checkable pointwise.
**Run it on a KNOWN-ANSWER object.** Chen–Hou's 2D profile is still exactly right for this
— that role never needed the certificate to close, only the answer to be known, which is
why the 2D work is not wasted.

**GATE.** *Does the new fitness pass the six-property viability gate?* **Yes** → Directive 3.
**No** → **STOP. Do not run the GA.** Stage 3.5 is the precedent and it is non-negotiable.

---

# DIRECTIVE 3 — B: EVOLVE THE CERTIFICATE

*(queued behind C-PILOT)*

Search space: the choices a computer-assisted proof currently makes by human taste — the
weight exponents and norm of the function space, the split of the linearized operator into
"leading order + finite rank", the truncation dimension, the domain decomposition, the
preconditioner's free constants. **Fitness: the radii polynomial's margin** — a theorem, not
a plot, and an under-resolved run cannot fake it.

**GATE.** *Does the searched certificate beat the hand-tuned one?* **Yes** → report the
margin, and say plainly that the search found it, not us. **No** → report that too; a
negative bounds how much of the difficulty was tuning versus structure.

**WHAT NEITHER OF THESE DOES.** Create novelty, or touch Clay. They make certification
attempts cheaper, which widens the set of objects worth attempting. **Wall 2 is a
dimensional wall, not a tuning wall.** `CLAY_ROADMAP.md` §7.3.

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

*Updated 2026-08-04 (session close, third update). **THAT SESSION SHIPPED THREE LEGS: ROUTE-J
v1 (the primary-source pass), ROUTE-K v1 (the certification port's first step), and ROUTE-L
v1 (the preconditioner).** Condensed at leg 45; full detail in `PHASE2_P2_NOTES` §31–§33.*

**(L-0a) STEP (iii) OF THE CERTIFICATION CHAIN IS UNBLOCKED — FIRST TIME IN 44 LEGS.**
`line_sweep_solve` in `solver/port_certification.py` is an **exact `O(N)` inverse** of the
full 2D transport operator — one outward Thomas sweep, licensed by radial upwinding being
outward everywhere (`s_ρ ∈ [0.390, 5.732]`). Stall **0.6623 (flat) → 3.3e−6 at `m`=320**.
Gated to 9.5e−16. **Scaffolding, not chain.**

**(L-0b/c) BOTH OF §32's NAMED SUSPECTS WERE CLEARED BY A SIX-WAY ABLATION BATTERY; IT IS
THE ANGULAR TRANSPORT.** Freezing the nonlocal Biot–Savart velocity makes the stall *worse*
(0.6623 → 0.7582); the wall is not it either, measured by angular band. The boring term
carries the entire obstruction. **ADI does not work (0.9960, worse than nothing)** — the
operator does not split, which is what forced the coupled sweep. Keep that negative (76).

**(L-0e) NEWTON STILL FAILED ON THE 2D OBJECT, AND THE OBVIOUS EXPLANATION WAS REFUTED.**
A **near-null direction**, not a spectrum; the scaling gauge was tested and makes it
strictly worse. **Left UNIDENTIFIED.** Leg 45 raises the odds it was the translation mode —
Chen–Huang–Li needed a third constant for exactly this family — but **the 2D object is no
longer the target and chasing this is banned.**

**(K-0b/d) THE 2D RELAXATION HAS NO FIXED POINT, TWO INDEPENDENT WAYS.** In time it
**limit-cycles** (`‖F‖_∞` 0.9757 → 0.0257 → 0.2290 at 500/3000/5000 steps); under
refinement it **diverges** — `1.671e−2 → 7.708e−2 → 2.667e−1` at `n_r = 300/450/600`, **2×
finer, 16× worse.** `c_ω` holds to **0.77%** across that same ladder because the modulation
is a *local* read at the origin while the residual grows *at the wall*: **"resolution-stable"
is not "converged" (71).**

**(J-0b/c/d) SEVEN OF TWELVE STANDING CLAIMS WERE PRE-EMPTED**, `s_c = α/2` by Xu
arXiv:2607.19762 §6.1 eleven days before our leg. **Xu's Prop 2 (the realization dichotomy)
is the live correction:** our discretization has **no origin condition**, so §26's
"continuous spectrum" and §30's "141 of 144 unstable directions" are statements about the
**maximal `L²` realization** and must say so (70). One result arrived *from* the
literature: **above `s_c` the balance is dissipation-vs-stretching, `β = σ c_l`, with `ω_t`
SUBDOMINANT**, carried by a double pole with residue `∝ ν` — **absent inviscidly.**
