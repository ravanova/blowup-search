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
  4_p2_lottery/    P2 — the 1D Hou–Luo lottery-ticket legs           figs 12–24
```

## The rigor ladder (the project's framing)

- **Level 0** — reproduce a known result.
- **Level 1** — a *novel numerical map* (GA finds an approximate profile, measures a
  residual). **All of Arcs 1–4 through fig18 live here.** A GA proves nothing.
- **Level 2** — a *rigorous, computer-assisted statement* (interval / Newton–
  Kantorovich certification). **Arc 4's Route-D legs (figs 19–24) are the first
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
22. [TECHNICAL_P2_ROUTED_SPACES.md](4_p2_lottery/TECHNICAL_P2_ROUTED_SPACES.md) ·
    [BLOG_P2_ROUTED_SPACES.md](4_p2_lottery/BLOG_P2_ROUTED_SPACES.md) — **Route-D v3**:
    the space-pair question. A **no-go theorem** for the whole weighted-`ℓ¹` category
    (the two NK requirements are separated by exactly one grading power, and the
    separation is conserved: measured minimum exponent sum **0.98**, control **0.00**),
    which retires v2's literal repair; plus the decay-graded pair that does satisfy
    both, its resonance at the anchor's own decay rate, and its interior optimum
    `α* ≈ 1.44`. *(fig 21)*
23. [TECHNICAL_P2_ROUTED_V4.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V4.md) ·
    [BLOG_P2_ROUTED_V4.md](4_p2_lottery/BLOG_P2_ROUTED_V4.md) — **Route-D v4**: the full
    gauged operator in the decay-graded pair, in a third independent discretization.
    v3's far-field pricing **survives** (model law within 6% of the full `‖A‖`;
    `Z₂ = 13.4` vs 13.3 predicted; a second interior optimum at `α ≈ 1.40`), but the
    decay-graded sup pair does **not** control the quadratic — `H` is unbounded on
    `L^∞`. The certificate's space must carry a decay grading **and** a smoothness
    scale. *(fig 22)*
24. [TECHNICAL_P2_ROUTED_V5.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V5.md) ·
    [BLOG_P2_ROUTED_V5.md](4_p2_lottery/BLOG_P2_ROUTED_V5.md) — **Route-D v5**: the
    two-grading space (decay × smoothness). v4's obstruction is **defused**
    (`γ ≳ 0.35`), smoothness turns out to have its **own interior optimum** just as
    decay does, and `Z₂` falls from 13.4 to 3.29. One marginal direction survives —
    the codomain's critical decay rate — fixed by a detuning that costs nothing.
    *(fig 23)*
25. [TECHNICAL_P2_ROUTED_V6.md](4_p2_lottery/TECHNICAL_P2_ROUTED_V6.md) ·
    [BLOG_P2_ROUTED_V6.md](4_p2_lottery/BLOG_P2_ROUTED_V6.md) — **Route-D v6**: the
    first genuine **upper** bounds (every earlier constant was a family-restricted
    *lower* bound), and the **discrete-ball trap** — computing an induced norm by
    duality over a discrete Hölder ball is unsound, its extremizer being inflated
    `~J²` in the continuum norm. Three of eight constants move to *bounded*; v5's
    joint optimum dies once `Z₁` is priced. *(fig 24)*

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
| `fig24_p2_route_d_v6.png` | 4 | P2 — Route-D v6: the discrete-ball trap (extremizer inflated ~J²), the two-point dual that saturates, the closed-form far-field `Z₁` bound, and the optimum moving once `Z₁` is priced |
| `fig23_p2_route_d_v5_holder.png` | 4 | P2 — Route-D v5: the square-wave adversary defused in the Hölder norm, the two interior optima (one per grading), the surviving marginal direction at the critical decay rate, and the quadratic constant before/after |
| `fig22_p2_route_d_v4_graded.png` | 4 | P2 — Route-D v4: the third build reproduces the negative and the repair, the compact core costs ~nothing (far-field law within 6%), the conjugate-extremal family showing the quadratic is unbounded in sup norms (and random sampling missing it), and the confirmed price |
| `fig21_p2_route_d_v3_spaces.png` | 4 | P2 — Route-D v3: the conservation law (the two NK exponents sum to ≥1 over every diagonal weight pair), the empty strip in the (s,t) plane with its ablation control, the far-field resonance at α=2, and the decay-graded optimum α*≈1.44 |

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
| `p2_route_d_v6_bounds.json` | Arc 4 / fig24 — B1 the discrete-ball inflation, B2 the two-point dual ladder, B3 the exact modelling identity, B4 the far-field `Z₁` bound + validation, B5 the `α` tension and conditional budget, B6 the ledger |
| `p2_route_d_v5_holder.json` | Arc 4 / fig23 — U1 the defusal of the v4 adversary, U2 the Hölder constant of `H` vs `γ`, U3/U3b/U3c the inverse over `(α,γ)` and the critical-direction isolation, U4 the quadratic in the two-graded pair, U5 the joint optimum |
| `p2_route_d_v4_graded.json` | Arc 4 / fig22 — W1 the third-build reproduction, W2 the core's contribution vs the far-field law, W3 the conjugate-extremal quadratic divergence + the random control, W4 the confirmed `Z₂`/budget ceiling, W5 the gauge/drop-row operational finding, W6 the quantified (not bounded) `Z₁`-analogue |
| `p2_route_d_v3_spaces.json` | Arc 4 / fig21 — S1 the pure-convolution identity + sharp constant, S2 the inverse's price in weighted norms, S3 the (s,t) map + gap collapse + conservation law, S4 the ablation control, S5 the far-field resonance (both sides), S6 the decay-graded pair and its optimum |
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
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v3_evidence.py         # fig21
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v4_evidence.py         # fig22
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v6_evidence.py         # fig24
.venv/bin/python writeup/4_p2_lottery/p2_route_d_v5_evidence.py         # fig23

# regenerate the Route-D data itself (deterministic; ~10 s and a few seconds):
.venv/bin/python experiments/p2_route_d_probe.py
.venv/bin/python experiments/p2_route_d_dress.py
.venv/bin/python experiments/p2_route_d_v3_spaces.py
.venv/bin/python experiments/p2_route_d_v4_graded.py
.venv/bin/python experiments/p2_route_d_v5_holder.py
.venv/bin/python experiments/p2_route_d_v6_bounds.py

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
