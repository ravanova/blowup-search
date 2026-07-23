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

**Gate 1b — Hou–Luo geometry + benchmark. [correctness DONE]** The no-flow wall
is imposed by parity (`w` odd-x/odd-y, `th` even-x/odd-y): Biot–Savart gives `v`
vanishing on `y=0,π` and `u` on `x=0,π`, an effective `[0,π]²` box with the
singular corner at the origin. Validated (`test_boussinesq_wall.py`, 4/4):
symmetry preserved to 9e-15 WITHOUT projection (the wall is a genuine invariant
of the discretised dynamics), wall BC at 8e-17, and a Luo–Hou-type IC amplifies
`max|ω|` 30.6× with parity + conservation intact. The `symmetry="houluo"` solver
option holds the wall exactly on long runs. **Deferred (judgment call, flagged
for review):** the *quantitative* Luo–Hou growth curve / finite-`T*` claim —
uniform-grid resolution cannot reach the `~10⁷` amplitude (needs AMR), so how
faithfully to chase it is a separate decision, not part of this correctness gate.

**Gate 2 — port the Phase-0 method. [DONE]** (a) 2D rough-data representation
`ga/genome2d.py`: the separable Holder product `w_h = P_h(x)P_h(y)` (odd-x/odd-y)
+ density partner `th_h = |sin x|^h P_h(y)` (even-x/odd-y); regularity certified
by `test_genome_rough_2d.py` (7/7) — its y=π/2 slice is exactly the 1D `P_h`, so
the Phase-0 certificate transfers verbatim. (b) Fine-N measurement = the same
`estimate_blowup_time`; validated on controls (`test_phase1_measurement.py`,
3/3): synthetic `(T*-t)^-a` inverted to `(a,T*)` exactly, and 2D Euler
(provably-regular, `||w||_inf` conserved) correctly refused Tier-2 — the
per-resolution exponents rail to opposite grid edges, so the convergence gate
rejects it (the anti-self-deception property, in 2D).

**Gate 3 — 2D genome.** A 2D genome data structure applying the rough-data
principle; reuse MAP-Elites, budget-matched acceptance, win-condition tiers,
resolution study, single-writer logging conceptually.

**Resolution de-risk spike [DONE, inserted before Gate 3].** Before building the
genome, a cheap fine-N probe tested the dominant risk — that the Hou–Luo
singularity is unresolvable on a uniform grid. Verdict **STABLE**
(`PHASE1_SPIKE_RESULTS.md`): a fixed-window growth-rate fitness converges across
N=128→1024 for smooth growers (search is viable), but (i) the blow-up exponent/T\*
rails → uniform-grid Tier-2 confirmation of the true singularity is out of reach
(needs AMR / Route D), and (ii) rough C^{0,α} data is under-resolved from t≈0 →
the rough-data axis is resolution-starved on uniform grids. Recalibrated plan:
proceed on **smooth data** with a **resolution-stable growth-based fitness**;
near-term deliverable is a shape→growth QD map with **Tier-1** candidates, not
Tier-2-confirmed singularities.

**Gate 3 — 2D genome.** A 2D genome over smooth Hou–Luo-subspace fields (parities
enforced), reusing MAP-Elites, budget-matched acceptance, single-writer logging.
The rough-data mode exists (`ga/genome2d.py`) but is deprioritised per the spike.

**Gate 4 — NON-NEGOTIABLE viability gate.** Re-run the six-property viability
gate on the new Boussinesq fitness BEFORE any GA compute. The spike already
cleared the dominant (resolution-stability) property for the growth-rate proxy;
Gate 4 must still confirm the other five — especially that the chosen axis tracks
blow-up PROPENSITY (a ν_crit-analog is the prime candidate; the early-window
growth rate alone is resolution-stable but not automatically blow-up-predictive —
smooth_mild has higher early g yet saturates). Commit to a full GA campaign only
if all six pass. If it rails, STOP — a finding, not a push-harder signal.

**Gate 5 — Route D.** On a Tier-2 novel candidate in this provable model, open
validated-numerics / a domain-expert collaboration — the actual proof leg, out
of scope for the search machinery.

## Honest framing (unchanged)

2D Boussinesq is still a toy model, not 3D Navier–Stokes; Tier 2 is not a proof.
The reachable win is a novel Tier-2 (and, with an expert collaborator, Tier-3)
candidate in a provable model. Overall Clay odds stay ~0.05%, capped by the two
structural walls.
