# Clay Roadmap — continuing the pursuit after the 1D pipeline is banked

**Purpose:** a durable strategic plan for continuing to attempt the
Navier–Stokes Millennium problem via evolutionary search, written at the point
where Stages 1–3 are complete and the *cheap* route to a novel result has been
closed. This is the "where next / don't lose track" document; the concrete
build-out stages live in [PLAN.md](PLAN.md), the banked results in
[writeup/](writeup/).

Read [writeup/SUMMARY.md](writeup/SUMMARY.md) first for what is already done.

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

### Route A — Switch model: 2D Boussinesq / De Gregorio with C^{1,α} data  ★ recommended novel-result route
**Thesis:** go to where provable *non-generic* blow-ups actually live. 2D
Boussinesq (the "poor man's 3D Euler," Hou–Luo geometry) and De Gregorio with
limited-regularity data are exactly the models Elgindi–Jeong, Chen–Hou, and
Buckmaster–Gómez-Serrano prove blow-up for.

- **What transfers (most of the value of the last month):** the whole harness —
  MAP-Elites, budget-matched acceptance, the six-property viability gate, the
  win-condition tiers, the resolution study, single-writer logging. Only the
  *solver* and the *genome's regularity handling* are new.
- **What's new / needed:** (i) a 2D Boussinesq spectral solver (or a
  rough-data-capable De Gregorio solver), materially heavier than the 1D gCLM
  but far short of 3D; (ii) a genome that natively represents C^{1,α}
  (limited-regularity) data — the current `k^{-p}` envelope is the seed of this
  but needs a real rough-data mode; (iii) re-running the viability gate on the
  new model's fitness before any GA compute (non-negotiable — Stage 3.5 is why).
- **Novel output if it works:** a QD map of blow-up-prone shapes in a
  provable-blow-up model, plus one or more Tier-2 candidates *specifically
  chosen to be Tier-3-tractable* — the input a validated-numerics proof needs.
- **Honest odds:** best available shot at a *novel* result — low-to-moderate
  single-digit-percent to reach a defensible Tier-2 novel candidate; a Tier-3
  proof from it is a further, expert-level step (see Route D). Clay contribution
  remains ~Wall-1/2 limited.
- **Cost:** the largest lift here, but the *right-sized* one (weeks of solver +
  gate work, not a 3D-Euler-scale program).
- **Decision gate:** commit only after a **1-week solver + viability-gate
  spike** shows the new fitness passes the six properties. If it fails the gate
  like gCLM's non-genericity axis did, stop — do not run the GA.

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

### Route C — Cheap probe: rough data + fine N on gCLM near a=1
**Thesis:** the one inexpensive thing left on the current model — push genuine
C^{1,α} data near `a=1` at N ≥ 2048 (adaptive) to see if a non-generic exponent
ever *converges* instead of railing.

- **Value:** cheap, and would either (a) surface a stable non-generic exponent
  (surprising, would reopen the gCLM route) or (b) reconfirm the artifact at
  higher fidelity (tightening the negative result).
- **Honest odds:** low — Stage 3.5 showed the apparent non-genericity forms at
  grid scale, so it will likely stay artifactual. But it's a 1–2 day check, not
  a program.
- **When to pick it:** as a quick sanity gate *before* committing to Route A's
  rough-data genome work — same regularity machinery, tiny cost.

### Route D — Tier-3 validated-numerics spike (the actual proof leg)
**Thesis:** the only tier that answers anything requires this, and we have no
pipeline. This is genuine mathematics (interval arithmetic / computer-assisted
proof), likely needing a **domain-expert collaborator**; the GA is a
candidate-*generator*, not a proof engine.

- **When:** only once Route A (or C) hands over a concrete, self-similar,
  Tier-2 candidate in a provable model. Not before — the tooling depends on the
  specific profile.
- **Honest framing:** this is where a *novel* result actually gets certified;
  it is out of scope for the search machinery and should be planned as a
  collaboration, not an automation.

## 4. Recommended sequencing

1. **Now:** bank the 1D pipeline (this writeup) — done.
2. **Next (cheap gate):** Route C — a 1–2 day rough-data + fine-N probe near
   `a=1`, reusing the existing solver + `nongenericity_sweep` harness. It also
   builds the rough-data genome mode Route A needs.
3. **Then (the real move):** Route A spike — stand up a 2D Boussinesq (or
   rough De Gregorio) solver and **run the six-property viability gate on its
   fitness before any GA**. Commit to a full GA campaign only if the gate passes.
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
