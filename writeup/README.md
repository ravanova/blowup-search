# Writeup — Evolutionary Search for Navier–Stokes-type Blow-up

This folder is the **self-contained, banked writeup** of the project. Two arcs:

- **The completed 1D gCLM pipeline** — a validated 1D pseudo-spectral solver, a
  quality-diversity evolutionary search, and an automated resolution study that
  promotes candidates to numerically-confirmed (Tier-2) blow-up — plus the
  honest negative result that closed the cheap route to a *novel* singularity.
- **Route A Phase 1 (in progress)** — the move to 2D Boussinesq in the Hou–Luo
  geometry (a *proven*-singularity model): a validated 2D solver and two
  de-risking spikes (resolution wall + fitness-axis choice) that recalibrated the
  reachable deliverable before any GA compute. No 2D candidate yet; see the
  Phase-1 rows below and [SUMMARY.md](SUMMARY.md).

It is designed so the work can be written up again in future **without digging
through raw logs or re-running any sweep or GA campaign**: every number quoted
and every figure is built from the small committed files in [`data/`](data/).

## Read in this order

1. **[SUMMARY.md](SUMMARY.md)** — one-page executive summary: what was built,
   what was proven, what it does and does not mean.
2. **[TECHNICAL_WRITEUP.md](TECHNICAL_WRITEUP.md)** — the full account: model,
   methods, the anti-self-deception protocol, results with evidence, and the
   honest scope.
3. **[BLOG.md](BLOG.md)** — a narrative technical blog post (the 1D arc) for a
   broader (still technical) audience.
4. **[BLOG_PHASE1.md](BLOG_PHASE1.md)** — a shorter companion post on the two
   de-risking experiments that opened Route A Phase 1 (2D Boussinesq).
5. **[BLOG_PHASE1_GATE4.md](BLOG_PHASE1_GATE4.md)** — the Gate-4 sequel: the
   ν_crit fitness passed the pre-committed gate but failed on substance (a false
   pass), and the inviscid growth-rate currency that escapes the wall.
6. **[BLOG_PHASE1_GSUSTAINED.md](BLOG_PHASE1_GSUSTAINED.md)** — the follow-on: the
   inviscid growth-rate *magnitude* hits the same uniform-grid wall, a second
   near-cheat (`accel_ratio`) is caught, and only a *rank-based* `g_frac` survives.
7. **[BLOG_PHASE1_GATE4_REFORM.md](BLOG_PHASE1_GATE4_REFORM.md)** — the conclusion:
   the rank check passes but the reformulated, cheat-audited Gate 4 **fails 4/6** —
   on free split `g_frac` rails to the ω₀→0 corner just as ν_crit did. Two
   currencies, one uniform-grid wall; the fitness search is concluded, pointing to
   an AMR / self-similar numerics upgrade.
8. **[NEGATIVE_RESULT_TWO_CURRENCIES.md](NEGATIVE_RESULT_TWO_CURRENCIES.md)** — the
   **standalone** methods / negative-result note: the anti-self-deception gate
   protocol and the "two currencies, one wall" finding, self-contained and
   data-attached (readable without the chronological series above). The
   citable packaging of the concluded fitness search.
9. **[TECHNICAL_PHASE2_RESCALING.md](TECHNICAL_PHASE2_RESCALING.md)** — Phase 2:
   the numerics-upgrade decision (dynamic rescaling over AMR), the rescaled-equation
   derivation confirmed against the literature, the Spike-0 reconnaissance (three
   false starts, each a finding), and the build recipe from the published scheme.
   Fully cited. (The decision + derivation record; the solver was built next.)
10. **[BLOG_PHASE2_RESCALING.md](BLOG_PHASE2_RESCALING.md)** — the narrative
    companion: "The wall has a far side, and it's made of other people's numerics."
11. **[TECHNICAL_SPIKE0_RESCALING.md](TECHNICAL_SPIKE0_RESCALING.md)** — Spike 0
    **built + validated**: the dynamic-rescaling solver, run on CLM against its
    closed-form answer, recovers the exact self-similar profile `-4X/(1+4X²)` and
    rate `c_ω→-1` from perturbed data, resolution-stable — including the crux
    (a line Hilbert transform on a non-uniform grid, derived stable, not
    transcribed) and the finding that one-scale rescaling is stable for CLM. Figure
    [`fig8`](figures/fig8_spike0_rescaling.png). Honest scope: reproduces a *proven*
    toy result; validates machinery, not novelty, not a proof.
12. **[BLOG_SPIKE0_RESCALING.md](BLOG_SPIKE0_RESCALING.md)** — the narrative
    companion: "We built the far side of the wall, and it held."
13. **[../CLAY_ROADMAP.md](../CLAY_ROADMAP.md)** — the forward plan for continuing
   to pursue the Clay problem. (Note: the AMR / self-similar-rescaling *numerics*
   upgrade is a solver upgrade to **Route A**, distinct from roadmap **Route D**,
   which is the later Tier-3 computer-assisted-proof leg.)

## Figures ([`figures/`](figures/))

| file | what it shows |
|---|---|
| `fig1_ga_vs_random.png` | Stage 2 acceptance — GA beats budget-matched random on 3/3 seeds |
| `fig2_resolution_convergence.png` | Stage 3 — T\* converges with resolution for all 9 elites |
| `fig3_nongenericity.png` | Stage 3.5 — the GA edge and the novel α≠1 target are disjoint |
| `fig4_blowup_curve.png` | a confirmed blow-up: max\|ω\| → ∞ and the BKM 1/M→0 diagnostic |
| `fig5_rough_rails.png` | Stage 3.6 — genuine `C^{0,h}` rough data still rails the exponent near a=1 (control validates the measurement) |
| `fig6_phase1_spike.png` | Phase 1 — the resolution wall: growth rate `g` converges (search-viable) while the blow-up exponent rails (true singularity out of uniform-grid reach) |
| `fig7_phase1_axis_screen.png` | Phase 1 — the fitness-axis screen: only ν_crit orders blow-up propensity (sharp>mild>control) and is N-stable |
| `fig8_spike0_rescaling.png` | Spike 0 — CLM dynamic rescaling: perturbed data relaxes onto the exact profile `-4X/(1+4X²)`, rate `c_ω→-1`, residual decays (known-answer validation) |
| `fig9_spike1_stepA_velocity.png` | Spike 1 Step A — 2D Boussinesq velocity operator `u=∇^⊥(-Δ)⁻¹ω` on the stretched grid recovers a manufactured `(ω,u,v)` to ~1e-5, 2nd-order convergence, `u_x(0)` origin read (known-answer validation) |
| `fig10_spike1_stepB_rescaled.png` | Spike 1 Step B — rescaled solver `(ω,η,ξ)`: formulation chosen by data (η-slope read ~2× better), operator convergence (transport ~3rd, gradient ~2nd), and the `c_l` ratio-cancellation (~3e-16) |
| `fig11_spike1_stepC_gate.png` | Spike 1 Step C — relax to the Chen–Hou profile (the gate, **PARTIAL**): `c_ω` matches to <0.5% and anisotropy to (2.24), far-field-exponent check fails; pre-committed predicate 3/4 |

## Evidence map ([`data/`](data/))

Every claim in the writeup traces to one of these committed files:

| file | contents | backs |
|---|---|---|
| `summary_metrics.json` | all headline numbers | SUMMARY / everything |
| `ga_vs_random.json` | best-so-far curves (GA vs random), 3 seeds | Stage 2 acceptance |
| `stage3_resolution.json` | T\*, α, R², drift by resolution — 18 studies | Stage 3 Tier-2 |
| `promoted_candidates.jsonl` | the 18 Tier-2 genomes **with coefficients** | Stage 3 Tier-2 |
| `nongenericity.json` | per-(shape, a) α + the six-property verdicts | Stage 3.5 |
| `stage3_6_rough.json` | per-(h, a, N) rough-data blow-up exponent + convergence kinds | Stage 3.6 / fig5 |
| `blowup_curve.json` | a representative max\|ω\|(t) trajectory | fig4 |
| `phase1_spike.json` | per-(IC, N) g / amp / exponent / T\* for the 2D resolution spike | Phase 1 / fig6 |
| `phase1_axis_screen.json` | per-(axis, IC, N) values + the pre-committed screen verdict | Phase 1 / fig7 |
| `phase1_gate4.json` | Gate-4 six-property gate on ν_crit (the false pass + ω₀ diagnostic), the fixed-split & currency probes | Phase 1 / BLOG_PHASE1_GATE4 |
| `phase1_gsustained.json` | staged inviscid growth-rate probe: magnitude on the resolution wall (LEG 1), rank-stability + `g_frac`-vs-`accel_ratio` cheat audit (LEG 2), free-split partials (LEG 3) | Phase 1 / BLOG_PHASE1_GSUSTAINED |
| `phase1_gate4_reform.json` | reformulated Gate 4 on `g_frac`: the 4/6 FAIL scorecard, the free-split rail to ω₀→0 (top-6 shapes), the property-6 sub-conditions, and the 7 grower→non-grower classification flips | Phase 1 / BLOG_PHASE1_GATE4_REFORM |
| `spike0_rescaling.json` | Spike 0 — line-H known-answer convergence, the perturbed-IC run (profile + `c_ω(τ)` + residual histories), and the two-resolution stability check | Spike 0 / fig8 |
| `spike1_stepA_velocity.json` | Spike 1 Step A — velocity-operator known-answer convergence, velocity errors, `u_x(0)` origin read, radial cut, error field | Spike 1 A / fig9 |
| `spike1_stepB_rescaled.json` | Spike 1 Step B — formulation decision (η-slope vs primitive-θ read error), transport/gradient convergence, `c_l` ratio-cancellation | Spike 1 B / fig10 |
| `spike1_stepC_gate.json` | Spike 1 Step C — the logged gate resolution study (`c_l,c_ω,α,`far-field,anisotropy per config) + the pre-committed predicate checks/verdict | Spike 1 C / fig11 |

The raw, full logs these were distilled from live under `experiments/`
(`run_logs/`, `*_sweep.jsonl`) in the repo root; they are gitignored (large,
regeneratable) — see [../LOGGING.md](../LOGGING.md). Nothing in this folder
depends on them.

## Rebuilding

```bash
# figures from the committed data (no solver runs needed):
.venv/bin/python writeup/build_figures.py

# Spike-0 figure from its committed data (add --generate to re-run the solver, ~1 min):
.venv/bin/python writeup/spike0_rescaling_evidence.py

# re-curate data from raw logs (only if you still have experiments/*, or after
# re-running the sweeps/GA per the stage docs):
.venv/bin/python writeup/curate_evidence.py
```

## Provenance / reproducing the underlying runs

The pipeline code and per-stage records live in the repo root:

- Solver: [`../solver/`](../solver) · win-condition diagnostics:
  [`../win_condition.py`](../win_condition.py)
- GA + resolution study: [`../ga/`](../ga)
- Sweeps: `../stage1_5_sweep.py`, `../stage2_6_sweep.py`,
  `../nongenericity_sweep.py`, `../stage3_6_sweep.py` (+ their `analyze_*.py`;
  `../stage3_6_progress.py` is a live viewer)
- Per-stage results & rationale: `../STAGE_1_5_RESULTS.md`,
  `../STAGE_2_6_RESULTS.md`, `../STAGE_3_RESULTS.md`,
  `../NONGENERICITY_RESULTS.md`, `../STAGE_3_6_RESULTS.md`; design contracts:
  `../PROJECT.md`, `../WIN_CONDITION.md`, `../PLAN.md`, `../LOGGING.md`.
- Route A Phase 1 (2D Boussinesq): solver `../solver/boussinesq.py`; spikes
  `../phase1_resolution_spike.py`, `../phase1_axis_screen.py` (+ their
  `analyze_*.py` and `../phase1_axis_progress.py` live viewer); results
  `../PHASE1_PLAN.md`, `../PHASE1_SPIKE_RESULTS.md`,
  `../PHASE1_AXIS_SCREEN_RESULTS.md`.
- Every logged run is pinned to a git commit and (for GA runs) a frozen
  `config.json`; tests: `../test_*.py`.
