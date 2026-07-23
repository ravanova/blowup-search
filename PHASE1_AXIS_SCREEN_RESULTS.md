# Phase 1 fitness-axis discrimination screen — results

*Route A Phase 1, the pre-Gate-4 routing check (2026-07-23). Pre-committed
question + pass criterion in `phase1_axis_screen.py` / `analyze_phase1_axis_screen.py`;
this records what came back. Screen = 3 ICs × N∈{256,512} = 6 bisections, 2160s.*

## Verdict: route the fitness on the **ν_crit-analog** (sole survivor)

Before spending a genome + a full 40-shape Gate 4 on an unverified fitness axis,
the spike's two **labeled ground-truth** ICs answer the one routing question
decisively: which candidate axis orders `smooth_sharp` (blows up, amp>100) above
`smooth_mild` (saturates, amp≈5) above `euler_control` (non-grower) — the blow-up
**propensity** direction — AND stays resolution-stable across N?

| axis | sharp@256 | sharp@512 | mild@256 | mild@512 | control | direction | stable | screen |
|------|-----------|-----------|----------|----------|---------|-----------|--------|--------|
| **ν_crit** | 0.6519 | 0.6519 | 0.0483 | 0.0483 | 0.0000 | sharp>mild>control ✓ | Δ=0.0000 ✓ | **PASS** |
| persistence | 0.2913 | 0.5509 | −2.6931 | −2.6912 | −0.0000 | mild<control ✗ | — | FAIL |
| g_baseline | 0.6088 | 0.6087 | 1.2389 | 1.2389 | 0.0000 | mild>sharp ✗ | — | FAIL |

## The three findings

1. **ν_crit-analog passes both legs cleanly.** Defined as the viscosity at which
   net resolved amplification `amp = max|ω|_end/max|ω|_0` crosses `A_CRIT = 2×`
   (κ=0; amplification is the project's blow-up currency, the same
   amplification-only predicate as `ga.fitness` v3). Direction: sharp 0.65 ≫
   mild 0.05 > control 0 (relative separation 0.93, ≫ the 0.10 floor).
   Resolution-stability: **identical to four decimals at N=128, 256, 512** — the
   amplification-crossing ν is set by the dynamics, not the grid, so it does not
   move with N. This is exactly the resolution-stable **propensity** axis Gate 4
   needs. → route the fitness here.

2. **Persistence fails on direction, not stability.** Growth acceleration
   (late-window minus early-window rate) orders sharp (+0.29/+0.55) above mild
   (−2.69) — the right *pair* separation — but the hard-saturating grower sits
   *below* the flat non-grower (mild −2.69 < control ≈0), so it breaks the
   sharp>mild>control ordering: persistence cannot place a strongly-decelerating
   flow correctly against a non-grower. (Its cross-N drift was within the lenient
   screen tolerance against the large sharp-mild spread, so stability was not the
   deciding failure.)

3. **The sanity control fired correctly.** `g_baseline` reproduces the spike's
   `mild > sharp` (1.24 vs 0.61) — the raw windowed growth rate rewards transient
   early rate, not propensity — confirming the screen's discriminator is
   trustworthy (it faithfully reproduces the known-wrong axis).

## What this does and does NOT establish

- **Does:** on the labeled ground-truth pair, ν_crit(amp≥2×, κ=0) is the fitness
  axis that both tracks blow-up propensity (right direction) and is
  resolution-stable — cheaply, before any genome/GA compute. Routing settled.
- **Does NOT:** clear the full **six-property Gate 4**. This screen tested only
  the direction + resolution-stability legs on 3 ICs. Gate 4 (40 shapes) must
  still confirm the other properties — **especially property 6 (non-trivial
  optimum)**, the very property that killed gCLM's ν_crit (its optimum collapsed
  to trivial k=1 energy concentration; STAGE_2_5_RESULTS.md), and property 5
  (wide discriminating band). Passing this screen is **necessary, not
  sufficient.** The Hou–Luo smooth-data singularity being robust (not
  non-generic) is the reason to expect property 6 to fare better here than in
  gCLM — but that is a hypothesis Gate 4 must test, not an established result.

## Consequence

Proceed to **Gate 3** (2D smooth genome over the Hou–Luo parity subspace) wiring
the **ν_crit-analog** (amp≥2×, κ=0, tail_guard-trusted window) as the fitness,
then the **non-negotiable Gate 4** six-property viability gate on it over 40
shapes before any GA campaign. If ν_crit rails property 6 as it did in gCLM,
**STOP — a finding, not a push-harder signal.**
