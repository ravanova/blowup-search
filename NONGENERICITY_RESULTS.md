# Non-Genericity Axis — De-Risking Sweep Results

**Verdict: NO viable non-genericity axis. The GA's demonstrated edge (a=0.7)
and the scientifically novel target (non-generic, α≠1, De Gregorio-type
blow-up) are DISJOINT within reachable gCLM at N ∈ {256, 512}. At a=0.7 every
blow-up is generic CLM-type (α≡1) regardless of regularity; non-genericity
appears only at a=0.9, and there only as a resolution artifact (15/40
well-definedness flips, α railing 3.0↔0.3, max cross-resolution Δα = 2.7); at
a=1.0 nothing blows up at all. This is the same resolution instability that got
`a_crit` rejected in Stage 1.5, now reconfirmed on the exponent.**

This settles the review question — *does the pivot toward a provable
non-generic blow-up keep the GA edge we found at a=0.7?* — with a clean **no,
they don't overlap.** The answer cost 240 inviscid runs (~2 min at 10 workers),
exactly the cheap gate-before-compute the six-property checklist exists for.

Date: 2026-07-23. Sweep: [nongenericity_sweep.py](nongenericity_sweep.py),
gate: [analyze_nongenericity.py](analyze_nongenericity.py). Data:
`experiments/nongenericity_sweep.jsonl` (240 rows). Roster: the same 40 shapes
as Stage 2.6 (20 Stage 1.5 ICs + 20 init-prior draws spanning envelope
p ∈ [0.02, 3.30]).

## Method

For each shape × a ∈ {0.7, 0.9, 1.0} × N ∈ {256, 512}, one **inviscid**
(ν=0) run to blow-up, recording the held-out fitted exponent α (with R², T*,
drift). The candidate fitness is **|α − 1|** (distance from the generic CLM
exponent), gated on the six-property checklist with candidate-D's single-run
adaptations (monotonicity → well-definedness; noise floor from cross-resolution
|Δα|, floored at the 0.05 exponent-grid step). An α counts only if the run
blew up, a held-out fit exists, and its R² ≥ 0.9 (an unreliable fit does not
define the exponent). Frozen at Stage 2.6's solver config except amplification
1e3 (three decades, so α is fittable) and a 300k-step cap (near-critical / no
blow-up runs bail rather than burn the horizon). The "× p-regimes" question is
folded in by correlating α and blow-up with the init-prior draws' envelope p.

## Results per a

| a | blow-up | usable (both N) | well-def flips | non-generic (\|α−1\|>noise) | resolution-stable | verdict |
|---|---|---|---|---|---|---|
| **0.7** | 37/40 | 37 | **0** | **0** | yes (median Δα=0) | FAIL — dead-flat (α≡1) |
| **0.9** | 35/40 | 20 | **15** | 3 | **no** (max Δα=2.7) | FAIL — artifact |
| **1.0** | **0/40** | 0 | 0 | 0 | — | FAIL — dead axis |

**a=0.7 — generic everywhere, perfectly stable, and therefore useless as a
non-genericity axis.** 37/40 shapes blow up (the 3 exceptions are the known
beyond-horizon bumps and `sin(x)+0.5sin(2x)`); every single fitted exponent is
α ∈ {0.95, 1.00} — `|α−1|` maxes at one grid step (0.05). Zero
well-definedness flips, median cross-resolution Δα = 0. Crucially, this holds
across the **entire regularity range**: Spearman(|α−1|, p) = −0.07 — roughness
does **not** move the exponent. The rough (p=0.02) and smooth (p=3.30) draws
alike give α=1.000. So where the GA has its edge, blow-up is uniformly generic
CLM-type; there is nothing non-generic to select for. (This also independently
re-confirms the Stage 3 finding α=1.000 as a property of the whole roster, not
just the nine confirmed elites.)

**a=0.9 — non-genericity appears, but it is a grid artifact.** Now α scatters
(prior(seed=16): 3.00→0.30 across N; prior(seed=4): 3.00→0.60;
prior(seed=18): 0.90→2.20), median cross-resolution Δα = 0.30, max = 2.7 —
55× the noise floor. 15 of 40 shapes flip well-definedness between N=256 and
512 (blow-up onset or fit-reliability appearing/vanishing with resolution);
the apparent non-genericity is strongest for the roughest shapes
(Spearman(|α−1|, p) = −0.63) but those are exactly the ones whose α **rails to
the grid edge 3.0 at N=256 and collapses at N=512** — the fit is chasing a
grid-scale feature, not a converged exponent. This is the Stage 1.5 `a_crit`
resolution instability ("near-critical advection collapse scales") reappearing
on the exponent axis. It fails four of six properties (finite,
well-definedness, resolution-stability, wide-band).

**a=1.0 — dead axis.** 0/40 shapes blow up (34–35 clean `no_blowup`, 5–6 hit
the step cap while stiff and near-critical). Consistent with the Stage 2.6
"a=1.0 is a dead axis for smooth odd data" finding and the literature
expectation that the smooth-data regularity question bites hardest at De
Gregorio. Blow-up is not *demonstrated* here within (t_max=24, amp=1e3, 300k
steps) — which, per WIN_CONDITION.md's explicit non-goal, is **not** evidence
of regularity, only absence of a searchable signal.

## What this means for the pivot

The hoped-for overlap does not exist. Laid out plainly:

- The **generic, stable, searchable** regime is a=0.7 — but its optimum is
  known-type CLM blow-up, not a novel contribution.
- The **non-generic** regime (α≠1) only switches on as advection approaches De
  Gregorio (a≥0.9) — and there the measurement is resolution-unstable and
  ill-defined at N ∈ {256, 512}, so no fitness built on it can be trusted, let
  alone climbed. A GA would be optimizing grid noise.

So **evolving for non-genericity on gCLM is not viable at these resolutions.**
The gate caught this for ~2 minutes of compute, before any GA campaign.

## Options (a real scope decision — for review, not decided here)

1. **Rougher data + much finer N (≥2048, adaptive).** Push genuinely
   limited-regularity (C^{1,α}-like, very small p) data near a=1 at resolutions
   where the exponent might converge. **Caution:** the a=0.9 flips show the
   apparent non-genericity currently *forms at grid scale*, so this may stay
   artifactual — it is a real-but-uncertain bet, and expensive.
2. **Change model — 2D Boussinesq / De Gregorio with C^{1,α} data.** Go to
   where the literature's *provable* non-generic blow-ups actually live
   (Elgindi–Jeong, Chen–Hou, Buckmaster–Gómez-Serrano). This is the honest
   home of a Tier-3-provable novel result, but it is a new-solver build
   (the Stage-4-class lift, on a different equation).
3. **Bank the validated Stages 1–3 pipeline as the deliverable.** Accept that
   the reachable, defensible result is the validated solver + QD search +
   resolution-confirmed *generic* candidates + the shape→viscosity-resistance
   map, and treat Clay (and a novel non-generic blow-up) as out of reach via
   this 1D route.

My read: option 3 is the honest current standing; option 2 is the only route
with a genuine shot at a *novel* Tier-3 result but is a major escalation;
option 1 is cheap-ish to probe but the artifact warning makes it low-odds.
Recommend **not** spending GA compute on a gCLM non-genericity axis regardless.
This is a scope decision for review.
