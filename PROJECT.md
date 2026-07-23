# Project Aim

Attempt the **Navier–Stokes Existence and Smoothness** Millennium Prize Problem
using evolutionary computation (genetic-algorithm-style search over candidate
initial conditions), chosen out of the six open Millennium Prize Problems as
the best fit for search-based methods. Rationale for the choice is in
[millennium_prize_problems.md](millennium_prize_problems.md).

## Target problem, precisely

The Clay Institute problem asks to either:
- **(a)** prove that smooth, globally-defined solutions to the 3D
  incompressible Navier–Stokes equations always exist given smooth,
  finite-energy initial data, **or**
- **(b)** disprove it, by exhibiting smooth initial data whose solution loses
  smoothness (blows up) in finite time.

**We are pursuing (b).** Direction (a) is a universal claim over an
infinite-dimensional space of initial data — there's no way to "search" your
way to a proof of something true for every possible input. Direction (b) is
existential — we only need to construct *one* counterexample — which is
exactly the kind of target a fitness-driven search can climb toward.

This mirrors real precedent: Hou, Luo, and collaborators have used numerical
optimization over initial data to hunt for near-singular solutions in the 3D
Euler equations (Navier–Stokes' inviscid cousin, and a common stepping stone),
and Buckmaster/Gómez-Serrano have converted similar numerical candidates into
rigorous computer-assisted proofs for related equations.

## Approach (planned, not yet built)

1. Represent candidate initial velocity fields as a genome (e.g. coefficients
   of a truncated spectral/Fourier expansion, or a parameterized vortex
   configuration).
2. Run each genome through a numerical Navier–Stokes/Euler solver.
3. Score fitness using the win-condition diagnostics below (rate of vorticity
   blow-up).
4. Select, crossbreed, and mutate genomes across generations, evolving toward
   the fastest / most convergent blow-up behavior.

The PDE solver and the GA itself are **future milestones** — not yet built.
This first pass establishes the aim and, more importantly, a rigorous
definition of *how we'll know if we've won*, so we don't fool ourselves later
with a numerical artifact.

## Documents in this project

- **[writeup/](writeup/) — the banked, self-contained writeup of the completed
  1D pipeline** (executive summary, full technical writeup, technical blog post,
  figures, and curated evidence data that rebuilds without any re-runs). Start
  at [writeup/SUMMARY.md](writeup/SUMMARY.md).
- [CLAY_ROADMAP.md](CLAY_ROADMAP.md) — forward strategic plan for continuing the
  Clay pursuit (the two structural walls, ranked routes A–D, go/no-go criteria).
- [millennium_prize_problems.md](millennium_prize_problems.md) — survey of
  all 6 open Millennium Prize Problems and why Navier–Stokes was chosen.
- [WIN_CONDITION.md](WIN_CONDITION.md) — the precise, tiered criteria for
  recognizing a real solution vs. a numerical false alarm.
- [win_condition.py](win_condition.py) — executable implementation of the
  Tier 1/2 diagnostics.
- [test_win_condition.py](test_win_condition.py) — sanity tests proving the
  diagnostics correctly detect a known analytic blow-up and correctly reject
  non-blow-up behavior.
- [PLAN.md](PLAN.md) — staged build-out plan for the real PDE solver and
  genetic algorithm (next milestone).
- [LOGGING.md](LOGGING.md) — design for run/generation/genome logging, so
  each GA run informs future runs instead of being a one-off black box.
- [STAGE_1_5_RESULTS.md](STAGE_1_5_RESULTS.md) — fitness-signal viability
  sweep results: `ν_crit` chosen as the Stage 2 fitness axis, `a_crit`
  rejected (resolution-unstable).
- [STAGE_2_RESULTS.md](STAGE_2_RESULTS.md) — GA acceptance runs: NOT MET
  because `ν_crit` at a=0 has a trivially-located optimum (k=1
  concentration); harness validated, fitness-axis redesign planned in
  PLAN.md Stage 2.5.
- [STAGE_2_5_RESULTS.md](STAGE_2_5_RESULTS.md) — fitness-axis redesign
  sweep: NO VIABLE AXIS (ν_crit at a ∈ {0.4, 0.7, 1.0} and
  bandwidth-constrained ν_crit at a=0 all fail the six-property gate);
  ν_crit on gCLM is dominated by the νk² dissipation scaling in every
  variant. Stopped for review before any GA rerun. **Review decision:
  proceed with PLAN.md Stage 2.6** (oracle v3 amplification-only
  boundaries + reformulated quantities C/D), with "accept the negative
  result" as the documented fallback.
- [STAGE_2_6_RESULTS.md](STAGE_2_6_RESULTS.md) — **Stage 2 milestone
  closed: ACCEPTANCE MET.** The v3 amplification-only oracle at a=0.7
  passes all six viability properties, and the GA beats budget-matched
  random search on 3/3 seeds (+3.3/+4.6/+3.2 tol, above the literature
  best on every seed), with evolved shapes more viscosity-resistant than
  any hand-built profile measured. Next: Stage 3 resolution study.
- [STAGE_3_RESULTS.md](STAGE_3_RESULTS.md) — **Stage 3 PASSED: Tier-2
  numerically-confirmed.** The automated resolution study
  ([ga/resolution_study.py](ga/resolution_study.py)) reran the top-3 elites
  per seed at N ∈ {256, 512, 1024}; all 9 (18/18 studies, inviscid + viscous)
  converge far inside the 2% T\* gate with shrinking conservation drift, and
  are promoted to `NUMERICALLY_CONFIRMED`. Honest read: α=1.000 throughout, so
  these are the CLM singularity surviving a=0.7 advection (pipeline
  validation + a Tier-2-backed shape→resistance map), **not** a novel
  De Gregorio blow-up. The near-term Stages 1–3 milestone is complete;
  Stage 4 (3D Euler) is unscheduled.
- [NONGENERICITY_RESULTS.md](NONGENERICITY_RESULTS.md) — **pivot de-risking:
  NO viable non-genericity axis.** A 240-run gate ([nongenericity_sweep.py](nongenericity_sweep.py))
  shows the GA edge (a=0.7, generic α≡1, resolution-exact) and the novel
  α≠1 target are DISJOINT: non-genericity appears only at a=0.9 and only as a
  grid artifact (15/40 resolution flips, α railing 3.0↔0.3), a=1.0 is a dead
  axis. Evolving for non-genericity on gCLM is not viable at N∈{256,512}.
  Forward options (rough+fine-N; switch to 2D Boussinesq; bank the 1D
  pipeline) are a scope decision for review.
