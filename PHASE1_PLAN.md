# Phase 1 build plan — 2D Boussinesq (Hou–Luo geometry)

*Route A, Phase 1 of CLAY_ROADMAP.md. Approved 2026-07-23 (scope + geometry
decisions both confirmed with the user). This is the reviewable contract for the
multi-week build; each gate STOPS for review before the next begins. Discipline
carried from Phase 0: never debug two unknowns at once; validate against a known
answer before trusting any new machinery; keep viscosity and the artifact guards
first-class from the first line.*

## Model

2D Boussinesq (the "poor man's 3D Euler"), vorticity–streamfunction form on a
`2π`-periodic-in-`x` domain:

    ω_t + u·∇ω = θ_x + ν Δω          (vorticity; buoyancy forcing θ_x)
    θ_t + u·∇θ = κ Δθ                (temperature/density transport)
    u = ∇^⊥ψ = (−ψ_y, ψ_x),  Δψ = ω  (Biot–Savart)

`ν` (viscosity) and `κ` (thermal diffusivity) are first-class from the start;
the inviscid Euler-analog is `ν = κ = 0`. Buoyancy force is `f = (0, θ)`; its
curl is `θ_x`, which is the whole singular mechanism.

This is the model with (i) a computer-assisted proof of finite-time singularity
in the boundary geometry (Chen–Hou 2022), giving the best Route-D / Tier-3
handoff, and (ii) a gold-standard numerical benchmark (Luo–Hou 2014) to validate
against. Both were the reasons for the geometry decision.

## Conserved quantities & artifact guards (analogs of the gCLM guards)

- `∫ω dx` (total vorticity): exactly conserved (the (0,0) Fourier mode is
  untouched by advection in divergence form, by `θ_x` (zero mean), and by `νΔ`).
  Drift normalized by an `L1` scale → the `mean_drift` analog.
- `∫θ dx`: exactly conserved likewise.
- Kinetic-energy balance: `d/dt (½∫|u|²) = ∫ v·θ dx − ν·(enstrophy dissipation)`.
  Accumulated trapezoid mismatch → the `energy_balance_residual` analog (the
  viscous-safe under-resolution signal).
- `conservation_drift = max(|∫ω drift|/scale, |∫θ drift|/scale, energy_residual)`
  — the single logged guard value, same design as `solver/gclm.py`.

## Gates (each STOPS for review)

**Gate 1a — doubly-periodic solver core.** `solver/boussinesq.py`, pure Fourier
(no wall yet), same `SolverResult`-style contract. Validated by an exact
analytic ladder in `test_solver_boussinesq.py`, each check isolating one piece:
  1. Biot–Savart: single-mode `ω → u` analytic; `∇·u` at machine zero.
  2. RHS terms: full spectral RHS (advection assembly + buoyancy `θ_x`) vs
     hand-computed analytic RHS on low modes — isolates the buoyancy coupling.
  3. Scalar transport: frozen divergence-free `u` translates `θ` exactly.
  4. Viscous decay: single mode `ω` under pure diffusion → `exp(−ν k² t)`.
  5. Taylor–Green: `ω = e^{−2νt} sin x sin y`, an exact solution of the full
     (advection + viscous, buoyancy off) system — advection self-cancels, so
     this checks Biot–Savart + transport dynamically together.
  6. Conservation: general nonlinear run with buoyancy on → `∫ω`, `∫θ` drift at
     machine scale, energy-balance residual small.

**Gate 1b — Hou–Luo geometry + benchmark.** Add the no-flow wall via a
parity/symmetry-restricted spectral basis (odd/even reflection so the wall is a
symmetry line where the normal velocity vanishes). Validate: symmetry is
preserved to machine precision under evolution, the wall BC holds, and the
solver reproduces the *qualitative* Luo–Hou vorticity-growth signature
(faster-than-exponential growth with the reciprocal-vorticity diagnostic
pointing to a finite `T*`) at feasible uniform resolution. We will not match the
`~10⁷` amplitude (that needs AMR); we validate the mechanism and early curve.

**Gate 2 — port the Phase-0 method.** A 2D rough-data representation (2D analog
of `holder_profile`, unit-tested for its regularity) and the fine-N exponent /
self-similar-quality measurement, each validated on a known-answer control
FIRST (the analog of the a=0.7 control in Stage 3.6).

**Gate 3 — 2D genome.** A 2D genome data structure applying the rough-data
principle; reuse MAP-Elites, budget-matched acceptance, win-condition tiers,
resolution study, single-writer logging conceptually.

**Gate 4 — NON-NEGOTIABLE viability gate.** Re-run the six-property viability
gate on the new Boussinesq fitness BEFORE any GA compute. Commit to a full GA
campaign only if all six pass. If it rails like gCLM's non-genericity axis did,
STOP — that is a finding, not a push-harder signal. (Stages 2.5 / 3.5 / 3.6 are
why this gate is non-negotiable.)

**Gate 5 — Route D.** On a Tier-2 novel candidate in this provable model, open
validated-numerics / a domain-expert collaboration — the actual proof leg, out
of scope for the search machinery.

## Honest framing (unchanged)

2D Boussinesq is still a toy model, not 3D Navier–Stokes; Tier 2 is not a proof.
The reachable win is a novel Tier-2 (and, with an expert collaborator, Tier-3)
candidate in a provable model. Overall Clay odds stay ~0.05%, capped by the two
structural walls.
