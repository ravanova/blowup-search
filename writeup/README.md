# Writeup — Evolutionary & rigorous search for Navier–Stokes-type blow-up

The **self-contained, banked writeup** of the project: an honest, long-shot attempt
at the Navier–Stokes blow-up problem via singular-profile / self-similar research.
Every number quoted and every figure is rebuilt from the small committed files in
[`data/`](data/) — **no raw logs, no re-run of any sweep, GA, or solver needed.**

Only a *rigorous proof* (Tier 3 / Level 3) would resolve the Clay problem; nothing
here does. The realistic prize is **novel toy-model singularity research** plus a
tiny Clay "lottery ticket." Each note states its own honest ceiling.

## How this folder is organized

Documents are grouped into four **numbered arc folders** (chronological). The
shared **build layer stays central**: [`data/`](data/) (committed inputs),
[`figures/`](figures/) (rebuilt outputs), and the two cross-arc builders
[`build_figures.py`](build_figures.py) / [`curate_evidence.py`](curate_evidence.py).
Each arc folder holds its own `TECHNICAL_*` / `BLOG_*` notes **and** the
`*_evidence.py` scripts that rebuild that arc's figures from `../data/`.

```
writeup/
  README.md                     <- you are here (the index)
  data/  figures/               <- shared, central (never moved)
  build_figures.py              <- figs 1–7 from data/
  curate_evidence.py            <- (re)curate data/ from raw logs (needs experiments/)
  1_gclm_1d/       the completed 1D gCLM pipeline (Level-0/1)        figs 1–5
  2_phase1_2d/     Route-A Phase-1 2D Boussinesq fitness search      figs 6–7
  3_spikes/        numerics upgrade + Spikes 0/1 (dynamic rescaling) figs 8–11
  4_p2_lottery/    P2 — the 1D Hou–Luo lottery-ticket legs           figs 12–20
```

## The rigor ladder (the project's framing)

- **Level 0** — reproduce a known result.
- **Level 1** — a *novel numerical map* (GA finds an approximate profile, measures a
  residual). **All of Arcs 1–4 through fig18 live here.** A GA proves nothing.
- **Level 2** — a *rigorous, computer-assisted statement* (interval / Newton–
  Kantorovich certification). **Arc 4's Route-D legs (figs 19–20) are the first
  bricks here** — validated tooling, a framing result, and then an honest structural
  *negative* (the naive certification does not close, and why). *Not a certificate.*
- **Level 3** — the Clay problem.

---

## Read in this order

### Arc 1 — the completed 1D gCLM pipeline ([`1_gclm_1d/`](1_gclm_1d/))
1. [SUMMARY.md](1_gclm_1d/SUMMARY.md) — one-page executive summary.
2. [TECHNICAL_WRITEUP.md](1_gclm_1d/TECHNICAL_WRITEUP.md) — full account: model,
   quality-diversity GA, resolution study, the anti-self-deception protocol.
3. [BLOG.md](1_gclm_1d/BLOG.md) — narrative companion (the 1D arc). *(figs 1–5)*

### Arc 2 — Route-A Phase 1: 2D Boussinesq fitness search ([`2_phase1_2d/`](2_phase1_2d/))
4. [BLOG_PHASE1.md](2_phase1_2d/BLOG_PHASE1.md) — the two de-risking experiments that
   opened Phase 1.
5. [BLOG_PHASE1_GATE4.md](2_phase1_2d/BLOG_PHASE1_GATE4.md) — the ν_crit false pass.
6. [BLOG_PHASE1_GSUSTAINED.md](2_phase1_2d/BLOG_PHASE1_GSUSTAINED.md) — the inviscid
   growth-rate currency hits the same wall; a second cheat caught.
7. [BLOG_PHASE1_GATE4_REFORM.md](2_phase1_2d/BLOG_PHASE1_GATE4_REFORM.md) — the
   reformulated Gate 4 fails 4/6; the fitness search is concluded. *(figs 6–7)*
8. [NEGATIVE_RESULT_TWO_CURRENCIES.md](2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md)
   — the **standalone** citable negative-result / methods note.

### Arc 3 — numerics upgrade + Spikes 0/1 ([`3_spikes/`](3_spikes/))
9. [TECHNICAL_PHASE2_RESCALING.md](3_spikes/TECHNICAL_PHASE2_RESCALING.md) ·
   [BLOG_PHASE2_RESCALING.md](3_spikes/BLOG_PHASE2_RESCALING.md) — the
   dynamic-rescaling decision + derivation.
10. [TECHNICAL_SPIKE0_RESCALING.md](3_spikes/TECHNICAL_SPIKE0_RESCALING.md) ·
    [BLOG_SPIKE0_RESCALING.md](3_spikes/BLOG_SPIKE0_RESCALING.md) — the CLM
    dynamic-rescaling solver, validated against its closed form. *(fig 8)*
11. [TECHNICAL_SPIKE1_VELOCITY.md](3_spikes/TECHNICAL_SPIKE1_VELOCITY.md) ·
    [BLOG_SPIKE1_STEPA.md](3_spikes/BLOG_SPIKE1_STEPA.md) — 2D velocity operator. *(fig 9)*
12. [TECHNICAL_SPIKE1_STEPB.md](3_spikes/TECHNICAL_SPIKE1_STEPB.md) ·
    [BLOG_SPIKE1_STEPB.md](3_spikes/BLOG_SPIKE1_STEPB.md) — rescaled 2D formulation. *(fig 10)*
13. [TECHNICAL_SPIKE1_STEPC.md](3_spikes/TECHNICAL_SPIKE1_STEPC.md) ·
    [BLOG_SPIKE1_STEPC.md](3_spikes/BLOG_SPIKE1_STEPC.md) — relax to the Chen–Hou
    profile (the gate, PARTIAL 3/4). *(fig 11)*

### Arc 4 — P2: the 1D Hou–Luo lottery-ticket legs ([`4_p2_lottery/`](4_p2_lottery/))
14. [TECHNICAL_P2_HL_ANCHOR.md](4_p2_lottery/TECHNICAL_P2_HL_ANCHOR.md) ·
    [BLOG_P2_HL_ANCHOR.md](4_p2_lottery/BLOG_P2_HL_ANCHOR.md) — the singular-profile
    machine vs the exact Chen–Huang–Li Thm 2.3 state. *(fig 12)*
15. [TECHNICAL_P2_CONJ24.md](4_p2_lottery/TECHNICAL_P2_CONJ24.md) ·
    [BLOG_P2_CONJ24.md](4_p2_lottery/BLOG_P2_CONJ24.md) — Conjecture 2.4: local
    attractor confirmed (9/9), global basin beyond a fixed-grid POC. *(fig 13)*
16. [TECHNICAL_P2_SCENARIO2.md](4_p2_lottery/TECHNICAL_P2_SCENARIO2.md) ·
    [BLOG_P2_SCENARIO2.md](4_p2_lottery/BLOG_P2_SCENARIO2.md) — the regular Stage-1
    profile / CHL's modified (4.1)/(4.2). *(figs 14–15)*
17. [TECHNICAL_P2_GA_FRAMEWORK.md](4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md) ·
    [BLOG_P2_GA_FRAMEWORK.md](4_p2_lottery/BLOG_P2_GA_FRAMEWORK.md) — the global GA
    fixed-point search infrastructure (validated tooling). *(fig 16)*
18. [TECHNICAL_P2_TWO_SCALE.md](4_p2_lottery/TECHNICAL_P2_TWO_SCALE.md) ·
    [BLOG_P2_TWO_SCALE.md](4_p2_lottery/BLOG_P2_TWO_SCALE.md) — the two-scale
    traveling-wave a-sweep (5/6 PARTIAL). *(fig 17)*
19. [TECHNICAL_P2_KLADDER.md](4_p2_lottery/TECHNICAL_P2_KLADDER.md) ·
    [BLOG_P2_KLADDER.md](4_p2_lottery/BLOG_P2_KLADDER.md) — the a_p(K) convergence
    map: the survival boundary is genuine, not genome-limited (7/7). *(fig 18)*
20. [TECHNICAL_P2_ROUTED.md](4_p2_lottery/TECHNICAL_P2_ROUTED.md) ·
    [BLOG_P2_ROUTED.md](4_p2_lottery/BLOG_P2_ROUTED.md) — **Route-D v1**: the rigorous
    interval-arithmetic core + the a=0 Newton–Kantorovich framing (the first Level-2
    brick; tooling + scoping, NOT a certificate). *(fig 19)*
21. [TECHNICAL_P2_ROUTED_DRESS.md](4_p2_lottery/TECHNICAL_P2_ROUTED_DRESS.md) ·
    [BLOG_P2_ROUTED_DRESS.md](4_p2_lottery/BLOG_P2_ROUTED_DRESS.md) — **Route-D v2**:
    the float dress rehearsal. The Newton–Kantorovich ball does **not** close at any
    truncation, gauge or weight; the cause is isolated by ablation (the transport term
    degenerates at `X = ∞`), and the repair — an asymmetric decay-graded space pair, in
    which `‖A‖ = 3.000` uniformly — is identified and measured. *(fig 20)*

Forward plan: [../CLAY_ROADMAP.md](../CLAY_ROADMAP.md). Working notes:
[../PHASE2_P2_NOTES.md](../PHASE2_P2_NOTES.md).

---

## Figures ([`figures/`](figures/))

| file | arc | what it shows |
|---|---|---|
| `fig1_ga_vs_random.png` | 1 | Stage 2 — GA beats budget-matched random on 3/3 seeds |
| `fig2_resolution_convergence.png` | 1 | Stage 3 — T\* converges with resolution for 9 elites |
| `fig3_nongenericity.png` | 1 | Stage 3.5 — GA edge and the novel α≠1 target are disjoint |
| `fig4_blowup_curve.png` | 1 | a confirmed blow-up: max\|ω\|→∞, BKM 1/M→0 |
| `fig5_rough_rails.png` | 1 | Stage 3.6 — rough `C^{0,h}` data still rails the exponent near a=1 |
| `fig6_phase1_spike.png` | 2 | Phase 1 — the resolution wall: `g` converges, exponent rails |
| `fig7_phase1_axis_screen.png` | 2 | Phase 1 — only ν_crit orders blow-up propensity + is N-stable |
| `fig8_spike0_rescaling.png` | 3 | Spike 0 — CLM rescaling relaxes onto `-4X/(1+4X²)`, `c_ω→-1` |
| `fig9_spike1_stepA_velocity.png` | 3 | Spike 1A — 2D velocity operator, 2nd-order, `u_x(0)` read |
| `fig10_spike1_stepB_rescaled.png` | 3 | Spike 1B — rescaled `(ω,η,ξ)` formulation chosen by data |
| `fig11_spike1_stepC_gate.png` | 3 | Spike 1C — relax to Chen–Hou (gate PARTIAL 3/4) |
| `fig12_p2_hl_anchor.png` | 4 | P2 — singular machine vs exact CHL Thm 2.3 `(X-1)^{-1/2}` |
| `fig13_p2_conj24_relax.png` | 4 | P2 — Conjecture 2.4: local attractor (9/9), global basin not |
| `fig14_p2_regular_profile.png` | 4 | P2 — the regular Stage-1 positive profile (CHL Scenario 2) |
| `fig15_p2_scenario2.png` | 4 | P2 — CHL modified (4.1)/(4.2): invariant `c_l/c_ω→-2.533` |
| `fig16_p2_ga_framework.png` | 4 | P2 — GA global fixed-point map; a=0 known-answer gate |
| `fig17_two_scale_sweep.png` | 4 | P2 — two-scale traveling wave deforms under advection to `a_p≈0.4` |
| `fig18_two_scale_kladder.png` | 4 | P2 — a_p(K) saturates: boundary `a*≈0.5–0.55` genuine |
| `fig19_p2_route_d.png` | 4 | P2 — Route-D v1: interval enclosure, the 2-D valley, the line→circle diagonalization, and the banded+rank-1 linearized operator |
| `fig20_p2_route_d_dress.png` | 4 | P2 — Route-D v2: the NK ball never closes (‖A_N‖ ~ N), the ablation that pins it on the far field, and the decay-graded repair (‖A‖ = 3.000 flat) |

## Evidence map ([`data/`](data/))

Every claim traces to one committed file. Key P2 / Route-D rows:

| file | backs |
|---|---|
| `summary_metrics.json` | SUMMARY / headline numbers |
| `ga_vs_random.json`, `stage3_resolution.json`, `promoted_candidates.jsonl`, `nongenericity.json`, `stage3_6_rough.json`, `blowup_curve.json` | Arc 1 (figs 1–5) |
| `phase1_spike.json`, `phase1_axis_screen.json`, `phase1_gate4.json`, `phase1_gsustained.json`, `phase1_gate4_reform.json` | Arc 2 (figs 6–7) |
| `spike0_rescaling.json`, `spike1_stepA_velocity.json`, `spike1_stepB_rescaled.json`, `spike1_stepC_gate.json` | Arc 3 (figs 8–11) |
| `p2_hl_anchor.json`, `p2_conj24_relax.json`, `p2_regular_profile*.json`, `p2_scenario2_relax.json`, `p2_ga_framework.json`, `p2_two_scale_sweep.json`, `p2_two_scale_kladder.json` | Arc 4 (figs 12–18) |
| `p2_route_d_probe.json` | Arc 4 / fig19 — Q1 enclosure precision, Q2 degeneracy singular values, Q3 line→circle covariance, Q4 the banded operator |
| `p2_route_d_dress.json` | Arc 4 / fig20 — D1 the N-ladder (`‖A_N‖ ~ N^0.97`), D2 the radii-polynomial bounds, D3 gauge insensitivity, D4 the `(1+cosθ)→1` ablation, D5 the far-field marginality + weight-repair impossibility, D6 the decay-graded pairings |

## Rebuilding

```bash
# Arc-1/2 figures from committed data (no solver runs):
.venv/bin/python writeup/build_figures.py

# any single leg's figure from its committed data (examples):
.venv/bin/python writeup/3_spikes/spike0_rescaling_evidence.py          # fig8
.venv/bin/python writeup/4_p2_lottery/p2_two_scale_kladder_evidence.py  # fig18
.venv/bin/python writeup/4_p2_lottery/p2_route_d_evidence.py            # fig19
.venv/bin/python writeup/4_p2_lottery/p2_route_d_dress_evidence.py      # fig20

# regenerate the Route-D data itself (deterministic; ~10 s and a few seconds):
.venv/bin/python experiments/p2_route_d_probe.py
.venv/bin/python experiments/p2_route_d_dress.py

# re-curate data/ from raw logs (only if you still have experiments/*):
.venv/bin/python writeup/curate_evidence.py
```

## Provenance

Solver: [`../solver/`](../solver) (incl. `interval.py`, `gclm_family.py`,
`line_hilbert.py`); GA + resolution study: [`../ga/`](../ga); per-stage records and
design contracts in the repo root (`../PROJECT.md`, `../WIN_CONDITION.md`,
`../CLAY_ROADMAP.md`, `../LOGGING.md`, `../PHASE2_P2_NOTES.md`); one
`../experiments/JOURNAL.md` entry per logged run; tests `../test_*.py` (8 suites
green). Every logged run is pinned to a git commit (and, for GA runs, a frozen
config). The raw logs under `../experiments/` are gitignored (large, regeneratable).
