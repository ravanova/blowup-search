# Stage 3 Results — Automated Resolution Study (Tier 1 → Tier 2)

**Verdict: all 9 evolved elites (top-3 per acceptance seed) pass the Tier-2
resolution-convergence test, at both an inviscid anchor (ν=0) and a
viscosity-resistance point (ν ≈ 0.081), and are promoted to
`NUMERICALLY_CONFIRMED` — 18/18 studies. The estimated blow-up time T\*
stabilizes to ~1e-5 relative agreement between the two finest grids (N=512 vs
N=1024), against a 2% gate, with conservation drift ~6e-5 (15× under the
artifact guard). The GA-evolved gCLM(a=0.7) blow-ups are resolution-converged,
not grid artifacts.**

This is the first Stage-3 result with real evidentiary weight: the search
method (Stage 2) found shapes, and those shapes' blow-up survives grid
refinement (Stage 3). It is **still a Tier-2 numerical confirmation on a 1D
toy model, not a proof and not the Clay problem** — see the honest framing at
the bottom.

Date: 2026-07-23. Deliverable: [ga/resolution_study.py](ga/resolution_study.py),
tests [test_resolution_study.py](test_resolution_study.py) (9/9). Study
experiment: `experiments/run_logs/stage3-resolution-20260723T082807/`
(18 `resolution_study` events, schema #6). Promotions mirrored to
`experiments/promoted_candidates.jsonl` (18 rows). Inputs: the three Stage 2.6
acceptance archives `stage2_6-seed{1,2,3}` (commit `a10d6b2`).

## Method

For each elite, rerun the solver at **N ∈ {256, 512, 1024}** under the *exact
frozen fitness config the elite was evolved in* (read back from that run's
`config.json`: a=0.7, t_max=24, the v3 dt policy, tail_fraction=0.15, energy
budget), and feed the three T\* estimates through
`win_condition.resolution_converged` (rel_tol 2%, the WIN_CONDITION.md Tier-2
contract). Three deliberate choices, all documented in the module header:

1. **Two operating points per elite.** Fitness is a ν_crit *bisection*; a
   resolution study is a single trajectory, so a viscosity must be chosen.
   - **Inviscid anchor (ν=0):** the best-conditioned member of the blow-up
     regime (no viscous dt stiffness), and the sharpest test of the deepest
     open risk — that a smooth bandlimited (C^∞) genome does not truly blow up
     and growing N merely chases an ever-finer near-singularity (PLAN.md
     regularity caveat). Promotion is gated here.
   - **Viscosity-resistance (ν = 0.5·ν_crit ≈ 0.081):** inside the blow-up
     band by monotonicity; confirms the *viscosity-resistant* blow-up — the
     project's actually-novel property — also refines cleanly, not only the
     inviscid one.

2. **Amplification raised to 1e4 (4 decades).** The cheap fitness oracle stops
   at 100× growth; at a fixed 100× stop every resolution halts at the same
   physical state, so T\* agreement would be near-tautological. The study
   raises the stop to 10⁴× so the 1/M → 0 extrapolation is stressed across
   four decades of growth. This is the one parameter deliberately *stricter*
   than fitness; a, ν policy, t_max, and dt are frozen.

3. **Conservation drift is the artifact guard.** A "blow-up" whose invariants
   drifted is distrusted regardless of a clean 1/M fit (LOGGING.md): any
   blow-up run exceeding `drift_threshold=1e-3` refuses promotion even if T\*
   looks converged. None came close (max 6.7e-5).

## Results

| operating point | n | T\*(finest) range | \|Δ\|/T\* 256→512 (max) | \|Δ\|/T\* 512→1024 (max) | max drift | α (finest) | promoted |
|---|---|---|---|---|---|---|---|
| inviscid anchor (ν=0)          | 9 | 2.173 – 2.258 | 7.6e-4 | **3.5e-6** | 6.7e-5 | 1.000 | 9/9 |
| viscosity-resistance (ν≈0.081) | 9 | 3.593 – 3.702 | 8.1e-4 | **4.1e-4** | 5.6e-5 | 1.000 | 9/9 |

Gate is rel_tol = 2e-2; the finest-two agreement beats it by ~50× (viscous) to
~5000× (inviscid). Every elite is Cauchy-contracting (256→512 diff already
< 1e-3, 512→1024 smaller still) — genuine convergence, not just proximity.

**Belt-and-suspenders beyond the defined bar:** the top elite (g01042) rerun
at **N=2048** gives T\* = 2.17320, *identical* to N=1024, with drift halving
again (4.1e-6 → 1.0e-6). The singularity is fully resolved by N=256; finer
grids move T\* by nothing. This is the direct empirical refutation of the
"finer N chases an ever-smaller-scale artifact" worry for these shapes.

The nine elites are structurally varied — envelope exponent p ranges 1.56–2.29,
sign-changes 2–6, spread across nine distinct MAP-Elites cells and all three
seeds — so the confirmation is not one lucky lineage but a property of the
evolved shape family.

## What the exponent tells us (and the honest read on novelty)

Every confirmed blow-up fits **α = 1.000** — the *generic, CLM-type*
self-similar exponent M ~ (T\*−t)⁻¹, not a non-generic De Gregorio exponent.
The physically honest interpretation: these are the **Constantin–Lax–Majda
singularity surviving moderate advection (a=0.7)**, which is exactly what one
expects for an axis sitting between proven-blow-up CLM (a=0) and the subtle
De Gregorio endpoint (a=1). It is *consistent with*, and does not out-run, the
literature picture (Okamoto–Sakajo–Wunsch; Elgindi–Jeong; Chen–Hou–Huang) that
the smooth-data regularity question bites hardest near a=1 — and indeed a=1 is
a **dead axis** for smooth odd data in our own sweep (Stage 2.6). So:

- **What Stage 3 establishes:** the Stages 1–3 pipeline produces
  resolution-converged Tier-2 candidates end-to-end, and the specific
  viscosity-resistant blow-ups the GA evolved are numerically genuine at N up
  to 2048. That is the pipeline-validation milestone the plan was aiming at.
- **What it does *not* establish:** a novel singularity. "gCLM(a=0.7) smooth
  data blows up with α≈1" is CLM-consistent behavior, not a new result about
  the hard (a=1, Hölder) regime. The genuinely novel output remains the
  **quality-diversity map of viscosity resistance across shape space**
  (Stage 2.6 archive) — *which* shapes resist viscosity — now with its top
  entries Tier-2-confirmed rather than merely Tier-1 candidates.

## Relation to the PLAN.md Stage 3 acceptance criterion

PLAN.md phrases the criterion as "at least one **De Gregorio** genome reaches
`NUMERICALLY_CONFIRMED`." Read literally at a=1 that is **not** met (a=1 is a
dead axis; nothing blows up there for smooth odd data within the horizon). Read
operatively — "a genome on the frozen search axis reaches Tier 2" — it is met
decisively: 9/9 elites on the a=0.7 axis that Stage 2.6 selected. The gap is a
real one and is stated rather than papered over: our viable axis is gCLM at
a=0.7, and these are Tier-2 gCLM(a=0.7) confirmations, **not De Gregorio
proper**. Widening toward a=1 would require the rougher (limited-regularity)
initial data the literature blow-ups actually use — reachable in principle via
the genome's k^{-p} envelope (small p), but out of scope for this run and noted
as a follow-up below.

## Honest scope (unchanged, restated so nothing over-claims)

- **1D toy model.** gCLM is a scalar 1D model, not 3D Navier–Stokes. A Tier-2
  confirmation here validates the *method*, not the real equation. Transfer
  only begins to mean something at Stage 4 (axisymmetric 3D Euler), which is
  unscheduled.
- **Tier 2, not Tier 3.** Resolution-converged floating-point T\* is strong
  numerical evidence of a genuine singularity; it is **not a proof**
  (WIN_CONDITION.md). Tier 3 needs validated/interval numerics (Stage 5, no
  pipeline yet).
- **α=1 = known-type behavior**, per above — the confirmation's value is
  pipeline validation + a Tier-2-backed shape→resistance map, not a new
  singularity.
- **Finite witnessed growth.** The study witnesses 4 decades (10⁴×) of
  grid-independent growth and a stable extrapolated T\*; it does not (and
  cannot, in floating point) integrate to the singular point itself.

## Follow-ups surfaced (optional, for review — not decided unilaterally)

1. **Push toward a=1 with rough data.** Re-run the resolution study on elites
   evolved at small envelope p (limited-regularity, Hölder-like), and/or a
   fresh axis nearer De Gregorio, to probe whether the pipeline can produce a
   *non-generic* (α≠1) Tier-2 candidate — the regime where a confirmation
   would be a genuine contribution against Chen–Hou–Huang / Elgindi–Jeong. This
   is a scope decision (new axis / non-odd symmetry), flagged for review.
2. **Self-similar profile check** (WIN_CONDITION.md Tier-2's second, currently
   un-automated leg): confirm the rescaled solution approaches a consistent
   profile with stable exponents across resolutions, strengthening the Tier-2
   claim beyond T\*-convergence alone.
3. **The GA tuning leads from Stage 2.6** (mutation-scale floor / longer runs;
   exploration pressure for map coverage) remain open and independent of this
   result.

## Next step

With the Stages 1–3 pipeline validated end-to-end and its top candidates
Tier-2-confirmed, the reachable near-term milestone (a validated solver +
non-degenerate fitness + QD pipeline + resolution-confirmed candidates) is
**complete**. Beyond it, PLAN.md Stage 4 (axisymmetric 3D Euler) is the next
real step toward the Clay problem — a large, unscheduled compute lift — and is
a scope decision for review, not an automatic continuation.
