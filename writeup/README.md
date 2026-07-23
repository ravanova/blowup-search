# Writeup — Evolutionary Search for Navier–Stokes-type Blow-up (1D gCLM pipeline)

This folder is the **self-contained, banked writeup** of the project's first
completed arc: a validated 1D pseudo-spectral solver, a quality-diversity
evolutionary search, and an automated resolution study that promotes candidates
to numerically-confirmed (Tier-2) blow-up — plus the honest negative result
that closed the cheap route to a *novel* singularity.

It is designed so the work can be written up again in future **without digging
through raw logs or re-running any sweep or GA campaign**: every number quoted
and every figure is built from the small committed files in [`data/`](data/).

## Read in this order

1. **[SUMMARY.md](SUMMARY.md)** — one-page executive summary: what was built,
   what was proven, what it does and does not mean.
2. **[TECHNICAL_WRITEUP.md](TECHNICAL_WRITEUP.md)** — the full account: model,
   methods, the anti-self-deception protocol, results with evidence, and the
   honest scope.
3. **[BLOG.md](BLOG.md)** — a narrative technical blog post for a broader
   (still technical) audience.
4. **[../CLAY_ROADMAP.md](../CLAY_ROADMAP.md)** — the forward plan for continuing
   to pursue the Clay problem.

## Figures ([`figures/`](figures/))

| file | what it shows |
|---|---|
| `fig1_ga_vs_random.png` | Stage 2 acceptance — GA beats budget-matched random on 3/3 seeds |
| `fig2_resolution_convergence.png` | Stage 3 — T\* converges with resolution for all 9 elites |
| `fig3_nongenericity.png` | Stage 3.5 — the GA edge and the novel α≠1 target are disjoint |
| `fig4_blowup_curve.png` | a confirmed blow-up: max\|ω\| → ∞ and the BKM 1/M→0 diagnostic |

## Evidence map ([`data/`](data/))

Every claim in the writeup traces to one of these committed files:

| file | contents | backs |
|---|---|---|
| `summary_metrics.json` | all headline numbers | SUMMARY / everything |
| `ga_vs_random.json` | best-so-far curves (GA vs random), 3 seeds | Stage 2 acceptance |
| `stage3_resolution.json` | T\*, α, R², drift by resolution — 18 studies | Stage 3 Tier-2 |
| `promoted_candidates.jsonl` | the 18 Tier-2 genomes **with coefficients** | Stage 3 Tier-2 |
| `nongenericity.json` | per-(shape, a) α + the six-property verdicts | Stage 3.5 |
| `blowup_curve.json` | a representative max\|ω\|(t) trajectory | fig4 |

The raw, full logs these were distilled from live under `experiments/`
(`run_logs/`, `*_sweep.jsonl`) in the repo root; they are gitignored (large,
regeneratable) — see [../LOGGING.md](../LOGGING.md). Nothing in this folder
depends on them.

## Rebuilding

```bash
# figures from the committed data (no solver runs needed):
.venv/bin/python writeup/build_figures.py

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
  `../nongenericity_sweep.py` (+ their `analyze_*.py`)
- Per-stage results & rationale: `../STAGE_1_5_RESULTS.md`,
  `../STAGE_2_6_RESULTS.md`, `../STAGE_3_RESULTS.md`,
  `../NONGENERICITY_RESULTS.md`; design contracts:
  `../PROJECT.md`, `../WIN_CONDITION.md`, `../PLAN.md`, `../LOGGING.md`.
- Every logged run is pinned to a git commit and (for GA runs) a frozen
  `config.json`; tests: `../test_*.py`.
