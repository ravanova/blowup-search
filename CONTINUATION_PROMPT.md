# Continuation prompt (copy into a fresh session)

> ## ⛔ RUN THIS FIRST: `.venv/bin/python plan_of_record.py`
> It prints the committed sequence, the current stage, its pre-committed gate and the live
> bans. **`test_plan_of_record.py` fails if this file and the plan disagree.** Stages `M` and
> `PORT` are **DONE**; **`ROUTE-V` is NEXT**, by user direction on 2026-08-04.

---

# WHY THE PLAN CHANGED — THE CHAIN CANNOT BE CLIMBED

The user asked how to move a link of the L1→L4 chain toward Clay. Checked against the chain's
own definition (`PHASE2_P2_NOTES.md` §24), the answer is that **it cannot be climbed as
written**:

* **`L1`** — a certified 1D toy profile. Movable, and leg 45 found an *uncertified* target for
  it. **This is the only movable link.**
* **`L2`** — 2D Boussinesq. **Chen–Hou proved it**, 145 pages.
* **`L3`** — axisymmetric 3D Euler with boundary. **Chen–Hou proved that too.**
* **`L4`** — 3D Navier–Stokes. Clay, and out of reach of interval arithmetic by Wall 2.

The rungs above `L1` are occupied or unreachable. It reads like a ladder but climbing rung 1
does not bring rung 4 nearer. **Stop using "toward Clay" as though the ladder carried you
there** — and note that `L1` itself was re-priced by leg 47 (below).

---

# DIRECTIVE 1 — ROUTE-V (IN FLOAT): DOES THE CERTIFICATE'S MARGIN SURVIVE DISSIPATION?

**This is the one route identified that is both Clay-ADJACENT and matched to what this
project already owns.** The Euler→NS gap **is** viscosity: 3D Euler blow-up with boundary is
proved, NS is not, and the entire difference is the dissipative term.

**What this project has, and probably nobody holds together:** the certification machinery
(leg 46 — bordered Newton to 5.7e−15, `Y₀`/`Z₁`/`Z₂` assembling, the polynomial closing in
float); the dissipative machinery (Routes F/H/I — `s_c = α/2`, `μ` as an autonomous
coordinate, `α₁` as the marginal invariant); and the criticality result — **NS sits exactly
at the exponent where every scaling argument returns zero information**, and criticality is a
tar pit where `μ` decays algebraically, nine times per decade.

**THE QUESTION IS NOT THE SCALING ONE.** "Does the scaling say the blow-up survives" was
Route-F and **Xu pre-empted it** (`arXiv:2607.19762` §6.1, eleven days before us). The new
question is: **switch dissipation on and ask whether the RADII POLYNOMIAL STILL CLOSES**,
walking `μ` up toward criticality and watching the margin.

## ⚠️ RUN IT IN FLOAT, AND KNOW WHY

An earlier draft of this directive said *"on an object where the inviscid certificate is in
hand."* **We do not have one** — leg 47 established that the inviscid certificate needs a
tail lemma nobody here has written. That premise was wrong when written and is removed.

**The float form needs no prerequisite.** Leg 46's machinery already produces `Y₀`, `Z₁`,
`Z₂` in float64. Deliver: the certificate constants as a function of `μ`; the margin's
trajectory as `μ → μ_crit`; and whether it degrades smoothly or falls off a cliff, and at
which `μ`.

**It is decisive either way, which is the point of doing it first.** If the margin collapses
the moment `μ > 0`, the Euler→NS question is answered in this toy **for one leg of work** —
and it saves building interval arithmetic and a tail lemma for a target that was never going
to survive them. If it degrades smoothly, that is the signal that stage `L1` is worth the
investment.

**`V`-RIGOROUS IS DOWNSTREAM OF `L1`, NOT A COMPETITOR TO IT.** "Does the *certificate*
survive" needs a certificate to perturb. `L1` is the first step of `V`-rigorous **and** a
novel result in its own right, so the two are not in tension. **A float study cannot be
upgraded into a certificate after the fact** — that is a standing ban.

## ⛔ THE NOVELTY CHECK COMES FIRST, AND IT IS A BAN

*Has anyone already done certification-under-dissipation for a self-similar profile?* Use
Route-M's ledger machinery (`solver/target_selection.py`, `solver/literature_gates.py`) and
the Tier 2/3 PDFs already fetched. **YES → report it, fall back to `C-PILOT`, do not spend the
leg. NO → proceed.** Leg 42 deleted seven of twelve novelty claims; **this route is a
speculation about novelty of exactly that kind and was flagged as such when proposed.**

**SAY THE CEILING IN EVERY WRITEUP.** Even complete success here is **not Clay and not a
chain link** — it is a statement about a toy model's certificate under dissipation. What
makes it Clay-*adjacent* is that it probes the one structural difference between the proved
case and the open one. A certificate that **dies** at small `μ` is as informative as one that
survives, and is the more likely outcome.

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


