# Clay Roadmap — continuing the pursuit after the 1D pipeline is banked

**Purpose:** a durable strategic plan for continuing to attempt the
Navier–Stokes Millennium problem via evolutionary search, written at the point
where Stages 1–3 are complete and the *cheap* route to a novel result has been
closed. This is the "where next / don't lose track" document; the concrete
build-out stages live in [PLAN.md](PLAN.md), the banked results in
[writeup/](writeup/).

Read [writeup/1_gclm_1d/SUMMARY.md](writeup/1_gclm_1d/SUMMARY.md) first for what is already done.

---

## 1. Where we are (2026-07-23)

**Banked:** a validated 1D gCLM solver, a QD evolutionary search that beats
budget-matched random on a verified viscous-blow-up fitness (3/3 seeds), 18/18
resolution-**confirmed** (Tier-2) candidates, and a reproducible
shape→viscosity-resistance map. Full evidence: [writeup/](writeup/).

**Just learned (the pivot-shaping negative):** the confirmed blow-ups are all
*generic* (α=1.000, CLM-type); the search's edge (`a=0.7`) and the novel
*non-generic* (α≠1) target are **disjoint** on gCLM — non-genericity only
appears near `a=1` and only as a resolution artifact
([NONGENERICITY_RESULTS.md](NONGENERICITY_RESULTS.md)). So **continuing to run
the GA on the gCLM non-genericity axis is not worthwhile.**

## 2. The two structural walls (why the ceiling is ~0.05%, and what they forbid)

Any honest plan must respect these — they are about the problem, not our effort:

- **Wall 1 — a search can only argue *for* blow-up, never for regularity.** If
  3D NS is globally smooth (a real possibility many experts lean toward),
  direction (b) is empty and our approach has probability ~0 by construction.
  Nothing in this roadmap changes that; it caps the whole program.
- **Wall 2 — provable ≠ where Clay lives.** The only rigorous-proof technology
  today (validated/interval numerics: Chen–Hou, Buckmaster–Gómez-Serrano) works
  on 1D/2D models simple enough for interval arithmetic. 3D NS is far out of its
  reach. So a Tier-3 result is attainable *only* on toy models — which are not
  Clay.

**Consequence:** the realistic near-term prize is a **novel Tier-3 result on a
model where blow-up is provable**, as a genuine contribution and a stepping
stone — not Clay itself. Everything below is ranked by expected value toward
*that*, with Clay as the distal, low-probability horizon.

## 3. Routes forward (ranked by expected value)

### Route A — Toward provable non-generic blow-up: 2D Boussinesq / C^{1,α} De Gregorio  ★ recommended novel-result route
**Thesis:** go to where provable *non-generic* blow-ups actually live. 2D
Boussinesq (the "poor man's 3D Euler," Hou–Luo geometry) and De Gregorio with
limited-regularity data are exactly the models Elgindi–Jeong, Chen–Hou, and
Buckmaster–Gómez-Serrano prove blow-up for.

Run in **two phases**, because two unknowns (a new solver *and* a new
non-generic-exponent measurement) must not be debugged simultaneously — build
and validate the measurement on the cheap substrate first, then port a *trusted*
method to the expensive one.

**Route A, Phase 0 — 1D rough-data spike (formerly Route C; the cheap
prerequisite).** ~2 days on the existing, validated gCLM solver.
- **Goal:** build a genuine C^{1,α} (limited-regularity) rough-data genome mode
  and a fine-N non-generic-exponent measurement, validated where we already know
  the answers (CLM analytic T\*, published De Gregorio results).
- **Deliverables:** (i) a rough-data genome representation — the current `k^{-p}`
  envelope is the seed but a true Hölder-profile construction is needed;
  (ii) a resolution-methodology that measures α (or a self-similar-quality score)
  and can tell a converged exponent from a grid-scale rail, exercised at
  **N ∈ {1024, 2048, 4096}** near `a=1`.
- **Gate (pre-committed):** does the non-generic exponent **converge** at
  N=2048/4096, or still **rail** (as at N=256/512 in Stage 3.5)?
  - *Converges* → surprise: gCLM is not exhausted, a novel 1D candidate may be
    directly reachable — **re-plan before building any 2D solver.**
  - *Rails* (expected) → gCLM is confirmed exhausted; **stop 1D work** and carry
    the *methodology and the representation principle* (not the 1D code) into
    Phase 1. A Phase-0 negative is **informative, not a kill-signal for Phase 1**
    — Boussinesq blow-up is a different mechanism.
  - **Guardrail:** hard 2-day time-box; no third "try a few more shapes" branch.
    Phase 0's value is the transferable method + the honest exhaustion check, not
    open-ended gCLM tinkering.

**Route A, Phase 1 — the model switch (the real lift).** Only after Phase 0.
- **What transfers (most of the value of the work so far):** the whole harness —
  MAP-Elites, budget-matched acceptance, the six-property viability gate, the
  win-condition tiers, the resolution study, single-writer logging — plus
  Phase 0's validated exponent-measurement method and rough-data representation
  principle. New: the *solver* and the 2D *genome data structure*.
- **What's needed:** (i) a 2D Boussinesq spectral solver (or a
  rough-data-capable De Gregorio solver), materially heavier than 1D gCLM but
  far short of 3D, validated against known Boussinesq results; (ii) a 2D genome
  applying Phase 0's rough-data principle; (iii) **re-run the viability gate on
  the new fitness before any GA compute** (non-negotiable — Stage 3.5 is why).
- **Novel output if it works:** a QD map of blow-up-prone shapes in a
  provable-blow-up model, plus one or more Tier-2 candidates *specifically chosen
  to be Tier-3-tractable* — the input a validated-numerics proof needs.
- **Honest odds:** best available shot at a *novel* result — low-to-moderate
  single-digit-percent to a defensible Tier-2 novel candidate; a Tier-3 proof
  from it is a further, expert-level step (Route D). Clay contribution stays
  ~Wall-1/2 limited.
- **Cost:** the largest lift here, but *right-sized* (weeks of solver + gate
  work, not a 3D-Euler-scale program).
- **Decision gate:** commit to a full GA campaign only after the Phase-1
  viability-gate spike shows the new fitness passes the six properties. If it
  fails like gCLM's non-genericity axis did, stop — do not run the GA.

### Route B — The literal ladder: Stage 4, axisymmetric 3D Euler (Hou–Luo)
**Thesis:** the canonical stepping stone toward NS, and the scenario where
numerical blow-up was first found.

- **What transfers:** genome→search→resolution-study conceptually; almost none
  of the solver.
- **What's needed:** a cylindrical-domain finite-difference/spectral solver with
  adaptive mesh refinement near the singularity, likely compiled/GPU — a large
  program ([PLAN.md](PLAN.md) Stage 4, unscheduled).
- **Why it's *not* first:** it lands on the *already-proven* inviscid cousin
  (Chen–Hou settled 3D Euler blow-up with boundary), so a numerical
  rediscovery is low incremental value; and Euler ≠ viscous NS, so it doesn't
  transfer to Clay cleanly. High cost, modest novelty.
- **Honest odds:** reproduces known results at best; genuine value only as
  infrastructure toward the (still unproven) viscous case.
- **When to pick it:** if the goal is explicitly "get as close to the real 3D
  target as compute allows," accepting it won't itself be novel or decisive.

### Route C — *folded into Route A as Phase 0* (2026-07-23 decision)
The cheap "rough data + fine N on gCLM near a=1" probe is no longer a standalone
route: it is the prerequisite first phase of Route A (see **Route A, Phase 0**
above). Rationale: its main value is not a gCLM result (Stage 3.5 makes a
converged non-generic exponent unlikely) but the **transferable method** — a
rough-data genome and a validated fine-N exponent measurement — that Route A
needs regardless, plus an honest "is gCLM exhausted?" check. Building it on the
substrate with known answers, then porting the method, avoids debugging a new
solver and a new measurement at once. It is therefore sequenced as A/Phase 0,
not run in parallel.

### Route D — Tier-3 validated-numerics spike (the actual proof leg)
**Thesis:** the only tier that answers anything requires this, and we have no
pipeline. This is genuine mathematics (interval arithmetic / computer-assisted
proof), likely needing a **domain-expert collaborator**; the GA is a
candidate-*generator*, not a proof engine.

- **When:** only once Route A hands over a concrete, self-similar, Tier-2
  candidate in a provable model. Not before — the tooling depends on the
  specific profile.
- **Honest framing:** this is where a *novel* result actually gets certified;
  it is out of scope for the search machinery and should be planned as a
  collaboration, not an automation.

## 4. Recommended sequencing

1. **Now:** bank the 1D pipeline (this writeup) — done.
2. **Next → START HERE — Route A, Phase 0** (the former Route C, ~2 days):
   build the C^{1,α} rough-data genome mode + a fine-N exponent measurement on
   the existing gCLM solver (reusing `nongenericity_sweep`/`win_condition`),
   probe N ∈ {1024, 2048, 4096} near `a=1`. Pre-committed gate: exponent
   converges (→ re-plan, gCLM not exhausted) or rails (→ carry the method into
   Phase 1). See [PLAN.md](PLAN.md) Stage 3.6 for the concrete spec.
3. **Then — Route A, Phase 1 (the real move):** stand up a 2D Boussinesq (or
   rough De Gregorio) solver, port Phase 0's method, and **run the six-property
   viability gate on its fitness before any GA**. Commit to a full GA campaign
   only if the gate passes.
4. **On a Tier-2 novel candidate:** open Route D (validated-numerics /
   collaboration).
5. **Parallel/optional, only if resourced:** Route B (3D Euler) as long-horizon
   infrastructure toward the viscous target.

## 5. Go / no-go criteria (so we don't drift or self-deceive)

- **Never run a GA on an axis that hasn't passed the six-property gate** at the
  target resolutions. (Stages 2, 2.5, 3.5 are the record of why.)
- **A Tier-1 candidate is never reported as more than a candidate** until the
  resolution study confirms it (Tier 2), and Tier 2 is never called a proof.
- **"No blow-up found" is not evidence of regularity** — it means widen the
  search or change model, per [WIN_CONDITION.md](WIN_CONDITION.md).
- **Stop a route** if its viability gate fails as gCLM's non-genericity axis
  did — a disjoint or artifact-only landscape is a stop, not a
  push-harder signal.
- **Re-evaluate the whole program** against Wall 1: if the accumulating evidence
  (ours and the literature's) leans further toward regularity for the target
  model, the honest move is to say so, not to keep searching an empty set.

## 6. Bottom line

The cheap, on-model route to novelty is closed, but the *machine* — solver
discipline, viability gating, QD search, resolution confirmation, and the
anti-self-deception contract — is built and transfers. The highest-value
continuation is **Route A on a provable-blow-up model**, gated by the cheap
Route C probe, with a Tier-3 collaboration (Route D) as the eventual proof leg.
Clay itself stays a ~0.05% horizon behind Walls 1 and 2; the tractable next win
is a *novel* Tier-2 (and, with a collaborator, Tier-3) candidate in a model
where that means something.


---

## 7. Addendum (2026-08-04) — what the search machinery should actually be searching

**Status: ADOPTED 2026-08-04 by user decision. This is the plan of record and it supersedes
§4's sequencing.** The machine-readable form is [`../plan_of_record.py`](plan_of_record.py)
and it is enforced by `test_plan_of_record.py`, which fails if this file, the continuation
prompt and the committed sequence stop agreeing with each other. Run
`.venv/bin/python plan_of_record.py` for the current stage, its gate and the live bans.

**Adopted:** the re-framing in §7.1 and the sequence in §7.4 — target selection, then the
port, then the Lyapunov-weight pilot, then the certificate search.
**NOT adopted and not claimed:** any route to Clay. §7.3 stands unchanged; Walls 1 and 2 are
untouched by all of this.

### 7.1 The re-framing

For 44 legs the GA has been pointed at **finding the object** — MAP-Elites over initial
conditions, fitness = a blow-up predicate (`ga/evolve.py`, `ga/fitness.py`,
`win_condition.py`). That was the right target for Stages 1–3.

**It has not been the bottleneck since Route-D.** Every leg from Route-D v1 onward has been
blocked not by *"we cannot find a blow-up candidate"* but by *"we cannot close a certificate
around the candidate we already have."* Route-D spent **eleven legs hand-tuning a decay-graded
function space** and then discovered (the advection-scope finding, §A) that it was
`a = 0`-only — tuned on the one member of the family where the hard term vanishes. Route-K
hand-picked a preconditioner; Route-L hand-picked a better one by reading the operator's
structure off the page.

**Those are search problems being done by hand, and unlike blow-up hunting they have a
rigorous scalar fitness.** "Does the radii polynomial close, and with what margin?" is a
theorem, not a plot. It cannot be faked by an under-resolved run, which is the failure mode
`WIN_CONDITION.md` exists to guard against.

### 7.2 The options, ranked

**Option B — evolve the CERTIFICATE, not the solution.  ★ best expected value**
Search space: the choices a computer-assisted proof currently makes by human taste — the
weight exponents and norm of the function space; the split of the linearized operator into
"leading order + finite rank" (Chen–Hou's own phrase); the truncation dimension; the domain
decomposition; the preconditioner's free constants. Fitness: the radii polynomial's margin,
or `Z_1` itself.
*Why it fits a GA:* low-dimensional, no gradient, wildly non-convex, expensive-but-bounded
evaluation, and a **rigorous, unambiguous objective**.
*Why now:* Route-L made the inner linear solve `O(N)` and exact, which is what makes an
evaluation cheap enough to run thousands of times. Before leg 44 this was not affordable.
*What it does NOT do:* create novelty. It makes certification attempts cheaper, which widens
the set of objects worth attempting — it does not tell you which object to attempt (that is
Route-M).
*Honest odds:* good chance of materially outperforming hand-tuning on a target we choose;
**zero** direct contribution to Clay.

**Option C — evolve the Lyapunov weight / coercivity functional.**
Much of Elgindi's and Chen–Hou's work is finding a weight under which the linearized operator
is dissipative — a pointwise inequality. Search over weights, fitness = the worst-case
coercivity constant. Same family as B, narrower, and a natural first bite because the fitness
is one number and the constraint is checkable. Rank: second, and possibly the right *pilot*
for B.

**Option E — genetic programming for conserved / monotone quantities.**
Expression trees over the state, fitness = "is `d/dt` of this sign-definite along
trajectories?" The project has already found one first integral by hand (Route-D v14), so the
machinery is not fanciful. *Honest assessment:* low probability — many strong people have
looked for coercive conserved quantities for NS — but cheap, and a negative is publishable-ish
as an exhaustion result. Rank: third, opportunistic.

**Option A — evolve initial conditions for blow-up (the current use).**
Dead for Clay by Walls 1 and 2, and leg 42 showed the toy-model phenomenology is largely
already in print. Keep it only as a *candidate generator feeding B*, never as the headline.

**Option D — evolve the coordinate transformation / compactification** so the fixed-point
problem is better conditioned. A special case of B; fold in rather than run separately.

**Option F — evolve counterexample-shaped objects in reduced models chosen to be
uncertified.** This is Route A + Route-M. Sequenced, not parallel.

### 7.3 The honest ceiling, restated

**None of these defeats Wall 2.** A GA that makes certification cheaper does not make 3D
Navier–Stokes reachable by interval arithmetic — that is a dimensional and complexity wall,
not a tuning wall. Nor does anything here touch Wall 1: if NS is globally smooth, the entire
programme is empty by construction.

So the honest statement of what Option B buys is: **it attacks the bottleneck this project
actually has, using machinery it already owns, with a fitness that cannot lie.** That is a
real improvement in expected value toward the *stated* prize — a novel Tier-3 result on a
model where blow-up is provable — and it is not a route to Clay. Clay stays where §6 left it.

### 7.4 The committed sequence

Four stages. Each carries a pre-committed gate naming **both** outcomes; the machine-readable
form is `plan_of_record.py` and the drift detector is `test_plan_of_record.py`.

1. **`M` — target selection. ✅ DONE, leg 45. GATE: YES.** *Certify what, that isn't already
   done?* Six candidates, three questions each, in `solver/target_selection.py`.
   **Named target: the NON-SYMMETRIC positive regular self-similar profile of the 1D
   Hou–Luo model** (Chen–Huang–Li arXiv:2604.01868 §4) — uncertified, reported April 2026
   as "a previously unreported blowup phenomenon", at **1.11e−3 of the certified object's
   unknown count**, and requiring **three** modulation constants because it has no symmetry
   point to pin the translation. Three further uncertified objects rank behind it. Seven
   objects moved onto the exclusion list — including the port's old target and, in
   arXiv:2305.05895, the **entire smooth gCLM branch, proved analytically for all `a ≤ 1`**.
2. **`PORT` — finish the certification port, RE-AIMED at the object `M` named.** Build it as
   a **bordered** system from the start — all three modulation constants as unknowns — not
   as a projection, which is what failed in leg 44. *The 2D work is not wasted:* Chen–Hou's
   object remains the **known-answer substrate** the later GA fitness must be validated on
   before it is trusted anywhere else — the same "build it where you know the answer, then
   port the method" discipline as Route A/Phase 0. That role never required the certificate
   to close, only the answer to be known.
3. **`C-PILOT` — evolve the Lyapunov weight**, on that known-answer object. The narrowest
   member of the re-framing and the right first bite: the fitness is **one number** and the
   constraint is checkable pointwise. **Gate: re-run the six-property viability gate on the
   new fitness before any GA compute.** Stage 3.5 is why that is non-negotiable.
4. **`B` — evolve the certificate.** The function space, the operator split, the constants.
   Fitness = the radii polynomial's margin, which is a theorem and cannot be faked by an
   under-resolved run.

## 7.5 Addendum (2026-08-06) — the exit criterion is answered: pursue a full Clay solve

**Status: ADOPTED 2026-08-06 by user ruling, resolving escalation #1** (stage `B` above
closed its own gate NO at leg 126 — 1,686/1,686 of its declared search space covered, zero
uncovered, a perfect search still 6.04x short — and had no successor for many cycles). **This
supersedes §7's own "NOT adopted, and not claimed: any route to Clay" line and §7.3's "Clay
stays where §6 left it."** The user explicitly accepts that this means building seriously
heavy code. **What does NOT change, restated because it matters more now, not less: Walls 1
and 2 still cap everything, Clay odds stay ~0.05% (recorded here, in the same paragraph, not
quietly dropped now that the prize is bigger), and no output is ever described as movement
toward Clay unless a link of the L1→L4 chain actually moves** — that rule is easier to erode
under a Clay-directed programme, not harder.

**Wall 2, corrected.** §2's naive form (spatial dimension is the barrier) is false — van den
Berg–Williams certified genuinely 3D Ohta–Kawasaki stationary states in 2019. The real
barrier is *time-dependent singularity formation*, not dimension. Every work stating a 3D
singularity theorem *with* a certificate supplies the 3D-ness via a 2D reduction (Chen–Hou)
or a spherically-symmetric ODE profile (BCG → CGSS) — never via the certificate itself. Any
plan from here must say explicitly which side of that line it lives on.

**Direction (a) (global regularity) stays closed** to anything search-/certificate-shaped:
Tao's averaged-NS supercriticality barrier means energy methods plus the preserved algebraic
structure are provably insufficient. Only direction (b) (blow-up) is in scope.

**The ansatz is constrained.** Nečas–Růžička–Šverák and Tsai exclude nontrivial
exactly-backward-self-similar 3D NS blow-up under the relevant decay — the target must be
discretely self-similar, unstable-self-similar with a finite unstable spectrum, or
non-self-similar. `arXiv:2604.09949` is the recorded negative-control citation for what
happens when this is missed.

**The missing rung is viscous certification, strictly on the Clay path.** Leg 174's own
occupancy matrix has the Grade-A/fluid cell empty "for want of a target, not a method"; leg
242 confirms nobody has filled it since (via the one precedent flagged closest, Dahne &
Figueras). No certified viscous blow-up exists in any model, in any dimension, today. If it
cannot be done in 1D, 3D NS is not a question of compute.

**Programme, sequenced (do not build the 3D solver first — this repository's own Route-A
discipline against debugging two unknowns at once applies with more force here):**

1. **Phase 0 (`P0` in `plan_of_record.py`) — target selection under the Clay goal.** A
   Route-M-shaped leg redone against Clay, not novelty: which object, which ansatz (screened
   by NRS/Tsai above), and what certification would even mean for it.
2. **Phase 1 — the viscous rung.** Can a viscous blow-up be certified in *any* model? A
   well-defined, unclaimed target, genuinely on the Clay path, and does not need the 3D
   solver.
3. **Phase 2 — the heavy lift.** The 3D near-singular viscous solver (`PLAN.md` Stage 4,
   unscheduled; AMR or dynamic rescaling, likely compiled/GPU). User-authorized but
   deliberately sequenced after Phase 1 reports — a 3D candidate with no certification story
   reproduces Hou–Luo 2013 and answers nothing.

The machine-readable form of this addendum is `plan_of_record.py`'s `P0` stage; the ban
review that accompanied this ruling (the DSS ban kept as-is, Stage V's ban re-posed since its
own "needs L1 first" lift condition had become unliftable) is recorded there directly.
