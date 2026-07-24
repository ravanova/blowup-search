# Phase 1 — reformulated Gate 4 (`g_frac`) results

*Route A Phase 1, the NON-NEGOTIABLE viability gate re-run on the inviscid
rank-based growth-rate currency `g_frac`, after the ν_crit gate failed
(PHASE1_GATE4_RESULTS.md) and the staged probe + 256→512 rank de-risk found the
`g_frac` **rank** stable (PHASE1_GSUSTAINED_RESULTS.md). Frozen predicate + runner
committed BEFORE the run (commit `13d888f`;
PHASE1_GATE4_REFORMULATED_PREDICATE.md). Data:
`experiments/phase1_gate4_reform.jsonl` → `writeup/data/phase1_gate4_reform.json`.
This records the outcome. A finding, not a push-harder signal.*

## Verdict (one line)

**FAIL — 4/6.** `g_frac`'s rank is resolution-stable (property 4 Spearman part
+0.889 / +0.926 ✓) and it is direction-correct, discriminating, well-posed, and
wide-band — but on a **free-split** roster with the anti-cheat audits as gate
conditions, **property 6 fails decisively: the landscape rails to the split→1
(ω₀→0) corner**, `g_frac` carries almost no ω-geometry signal beyond split
(partial ρ(g,centroid|split) = +0.11 < 0.15), and it is largely a **formation-time
proxy** (partial ρ(g,centroid|t_res) = −0.39). Property 4 also fails a *second*
axis the rank-check never tested: the grower/non-grower **classification** is not
resolution-stable — 7/37 shapes are coarse-grid false-growers, corrected at finer N.

## The scorecard

| # | property | result | detail |
|---|----------|--------|--------|
| 1 | nonzero/discriminating | **PASS** | 28/28 growers > 0.1; spread 1.308 |
| 2 | direction + control | **PASS** | sharp>mild>control at N=128/256/512; euler censored <0.1 |
| 3 | well-posed measurement | **PASS** | growers finite; window-robust Spearman(g₀.₅,g₀.₆)=+0.989 |
| 4 | RANK-resolution-stable | **FAIL** | rank ✓ (+0.889, +0.926, not degrading) **but 7 grower→non-grower flips** |
| 5 | wide band | **PASS** | grower g_frac spread 1.308 |
| 6 | non-trivial optimum (split-controlled) | **FAIL** | 5 of the sub-conditions fail — see below |

## Why property 6 fails — the ω₀ cheat returns on free split

The de-risk fixed split=0.5, which pinned ω₀'s scale. Freeing split (the actual
search setting) lets the optimum drive ω→0 to maximize buoyancy forcing — **exactly
the degeneracy that killed ν_crit**, now on the growth-rate axis. The **top 5**
shapes at N=512 are all high-split:

| rank | shape | g_frac | centroid | split | t_res |
|------|-------|--------|----------|-------|-------|
| 1 | rand_18 | +1.635 | 1.56 | **0.99** | 2.01 |
| 2 | rand_06 | +1.631 | 2.84 | **0.99** | 2.26 |
| 3 | rand_01 | +1.561 | 1.59 | **0.95** | 2.53 |
| 4 | rand_17 | +1.521 | 2.19 | **0.93** | 2.26 |
| 5 | rand_07 | +1.291 | 1.62 | **0.99** | 2.15 |
| 6 | struct_high | +1.269 | 3.07 | 0.69 | 3.17 |

The failing sub-conditions (winner `rand_18`, split 0.99, centroid 1.56):
- **b_winner_structured = False** — winner centroid 1.56 < 1.3·√2 (low-mode ω).
- **b′_winner_not_split_rail = False** — winner split 0.99 > 0.85 (**at the rail**).
- **d_no_ω₀_cheat = False** — ρ(g, log|ω₀|) = **−0.66** (bar 0.40). The partial
  controlling for split is small (−0.10), i.e. the ω₀ dependence is *mediated by
  split* — but the cheat is present in the ranking regardless.
- **g_gradient_beyond_split = False** — partial ρ(g, centroid | split) = **+0.11**
  < 0.15. **Split-dominance confirmed as a gate condition:** once split is
  controlled, `g_frac` barely discriminates ω-geometry.
- **h_more_than_t_res_proxy = False** — partial ρ(g, centroid | t_res) = **−0.39**.
  Controlling for *when tail_guard trips*, the structure signal not only vanishes
  but reverses: `g_frac` is largely a re-encoding of the formation time t_res.

What *passed* inside property 6: **e** (structure not dissipation-penalized,
ρ(g,centroid)=−0.51 > −0.70) and **f** (the controlled split-sweep still has
interior optima — b_diag@0.7, b_high@0.5, b_low@0.3 — and partial
ρ(g,split|ω₀)=+0.33 > 0). The sweep-vs-winner disagreement is the subtle point: at
**fixed** structure the split optimum is interior, but on the **free** roster a
high-split shape with the right geometry still beats the interior-optimum
structured shapes. The de-risk's controlled sweep could not see this; the
free-roster **winner interrogation** did. (Banked lesson, again: a controlled
sub-test passing is necessary, not sufficient — interrogate the actual winner.)

## Why property 4 fails — classification is not resolution-stable

The rank-check established that the *rank* of `g_frac` survives 256→512 (+0.905),
and that holds here (+0.889 128→256, +0.926 256→512). But the gate additionally
tested whether the **grower/non-grower classification** is resolution-stable, and
it is not — 7/37 shapes trip tail_guard at coarse N (look like they are forming
small scales) but **saturate** at fine N once resolved:

| shape | t_res @128 | @256 | @512 |
|-------|-----------|------|------|
| advlo_s20 | 2.91 | 3.56 | **4.00** |
| advlo_s10 | 3.13 | 3.92 | **4.00** |
| rand_09 | 3.11 | 3.93 | **4.00** |
| rand_12 | 3.00 | 3.91 | **4.00** |
| (…rand_00, rand_08, rand_16 similar) | | | |

These are textbook **under-resolution false-positives** (WIN_CONDITION.md Tier-2:
"under-resolved simulations routinely look like they're blowing up"). The low-split
adversarial shapes (weak buoyancy, mostly ω) are the clearest cases. So even the
*binary* "is this a grower" is a coarse-grid artifact for ~19% of the roster.

## The unifying finding — two currencies, the same wall, plus a new one

Both viability currencies now fail the honest gate via the **same root
degeneracy**: on a free genome the "most singular" optimum drives ω₀→0 (via the
buoyancy split), so the fitness rewards the trivial ω₀→0 corner, not blow-up
structure. `ν_crit` did it through `amp = max|ω|/max|ω₀|`; `g_frac` does it because
more θ → more forcing → faster *rate*. `g_frac` additionally turns out to be
largely a **formation-time (t_res) proxy** carrying little independent ω-geometry
information.

The deeper, resolution-level reading: **on a uniform grid the genuine
singular structure lives below grid scale, so no scalar fitness read off the
trusted (pre-tail_guard) window can cleanly isolate it** — the trusted-window
signal is dominated by resolvable-but-trivial degrees of freedom (amplitude/ω₀,
buoyancy split, formation time). This is the same uniform-grid wall the spike and
axis screen found, now demonstrated to defeat *fitness design itself*, not just
Tier-2 confirmation.

## Consequence (a finding; the honest strategic read)

A third uniform-grid scalar currency is **not** indicated — that would be "pushing
harder" against a wall two independent currencies have now hit. The result points
to the structural conclusion the spike already flagged: the path to a fitness that
tracks **genuine structure** (and to Tier-2 of the true singularity) is **Route D**
— AMR / self-similar rescaling, which resolves the singular region so the fitness
is measured on real structure rather than grid artifacts.

**Scientific value (a real negative result):** blow-up-search fitness design in 2D
Boussinesq on a uniform grid is systematically confounded by trivial degeneracies;
a pre-committed, cheat-audited viability gate is necessary to detect this (both
currencies produced a *superficially passing* signal — ν_crit a false 6/6, g_frac
a rank-stable de-risk — that only the substantive winner/cheat interrogation
exposed). Worth writing up as guidance for anyone attempting evolutionary
singularity search.

## Honest framing (unchanged)

2D Boussinesq is a toy model, not 3D Navier–Stokes; this is a result about *fitness
machinery*, not about blow-up. It neither finds nor rules out a singularity. Route
A's uniform-grid fitness search has reached its wall; the Clay lottery ticket (a
novel, genuinely-resolved singular structure) requires Route D. Overall Clay odds
unchanged, ~0.05%.
