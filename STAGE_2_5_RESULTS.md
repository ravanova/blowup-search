# Stage 2.5 Results — Fitness-Axis Redesign

**Verdict: NO VIABLE AXIS. Candidate A (ν_crit at fixed a ∈ {0.4, 0.7,
1.0}) fails the six-property gate at every a; candidate B
(bandwidth-constrained ν_crit at a=0) fails it too, pinning its optimum to
the cap boundary exactly as PLAN.md's stated risk predicted. Per PLAN.md
Stage 2.5, the Stage 2 acceptance rerun is NOT executed — the GA must not
run on an unverified axis — and the project stops here for review.**

The one-line finding: **on gCLM at a fixed horizon, viscosity-resistance
(ν_crit) is in every tested variant dominated by low-wavenumber energy
concentration — a spectral property the init prior samples directly — not
by evolved blow-up structure.** The νk² dissipation scaling is the whole
landscape: unconstrained it selects pure k=1 (Stage 2); under moderate
advection it selects low-k mixtures the prior still reaches (a=0.4);
under a hard low-k cap it pins to the cap boundary (candidate B); and by
a=1.0 blow-up itself vanishes within the horizon. No fitness axis in this
family gives selection anything to do that prior sampling does not.

Date: 2026-07-22. Sweep code: `stage2_5_sweep.py` (candidate A commit
`f3dc522`, candidate B commit `a005ef8`), analysis: `analyze_stage2_5.py`.
Data: `experiments/stage2_5_sweep.jsonl` (A, 240 bisections),
`experiments/stage2_5_sweep_b.jsonl` (B). Oracle, stop criteria, and
bisection tolerance identical to Stage 2's frozen config (v2 predicate:
amplification-first, held-out R² ≥ 0.9, T* ≤ 1.5·t_max; t_max=12,
amplification 100×, early-decay 0.1/2.0, tol 1e-3), with a range ladder
[0, 0.1] → [0, 0.4] → [0, 1.0] extending only on censored-high.

## What was measured

Per PLAN.md Stage 2.5: ν_crit(t_max=12, N) over 40 shapes — the 20
Stage 1.5 hand-picked ICs **plus 20 draws from ga/evolve.py's actual init
prior** (N=32 coefficients ~ N(0,1), envelope p ~ U[0,3.5],
energy-normalized) — at both N=256 and N=512, gated on the six-property
checklist (Stage 1.5's five + the non-trivial-optimum property Stage 2
proved necessary). Selection rule: the largest a passing all six.

## Candidate A — ν_crit at a ∈ {0.4, 0.7, 1.0}: FAIL at every a

### Six-property table (N=256/512, 40 shapes per a)

| property | a=0.4 | a=0.7 | a=1.0 |
|---|---|---|---|
| 1. nonzero | PASS (37/37 uncensored > 2·tol) | PASS (36/36) | **FAIL (0)** |
| 2. finite | PASS | PASS | PASS |
| 3. monotone | PASS (0 violations) | **FAIL (1: prior seed=11, both N)** | PASS (trivially) |
| 4. resolution-stable | PASS (max Δ = 0.8·tol) | PASS (max Δ = 0.8·tol) | PASS (trivially) |
| 5. wide band | PASS (0.008–0.159, 151·tol) | PASS (0.004–0.157, 153·tol) | **FAIL (spread 0)** |
| 6. non-trivial optimum | **FAIL (gap 7·tol; ρ(k1)=0.79)** | PASS (gap 21·tol) | **FAIL (no structured shape alive)** |

### a=1.0 (De Gregorio) is a dead axis — the PLAN.md risk realized

35/40 shapes censored low: no blow-up within the horizon even at ν=0.
The 5 survivors are all rough, low-k1 init-prior draws (k1 fraction
0.00–0.16) with ν_crit ≈ tol/2, i.e. barely above zero; two flip
censored/uncensored between resolutions at that scale. The expected
physics held — at a=1 sin(x) is an equilibrium, every k1-dominant shape
dies (the k=1 refuge stops paying **completely**), and the only blow-up
that remains lives in rough shapes at viscosities too small to search.
Smooth-data blow-up within a fixed horizon effectively vanishes at
De Gregorio, consistent with the literature's regularity expectations for
smooth data.

### a=0.7 fails monotonicity — and the failure is systemic, not a fluke

prior(seed=11): bisected ν_crit = 0.0105, but the ν = crit+0.015 probe
(0.0255) classifies as blow-up at BOTH resolutions. Mapping ν ∈
[0.018, 0.045] finely: there is an island ν ∈ [~0.026, ~0.031] classified
blow-up via the fit rule with high R² (up to 0.997) and T* = 17.2–17.6 —
just inside the 18.0 cap — bounded below by a bursty regime where fit
quality collapses (R² 0.78 → −0.63) and above by T* drifting past the cap.
T*(ν) itself is monotone; what is non-monotone is **fit quality** across
the marginal band, so the frozen predicate's classification flickers.

The audit that generalizes this: at a=0 (Stage 1.5 data), 19/19 uncensored
boundary decisions at both resolutions were **amplification-decided** —
the run demonstrably grew 100× and stopped. At a=0.4 and a=0.7, **every
uncensored boundary (37/37 and 36–37 per resolution) is fit-decided**,
overwhelmingly on slow non-generic
growth (α ≤ 0.4 for ~90%), with T* within 2 of the horizon cap for
22–28 of ~37 shapes. So "ν_crit at a>0" under the frozen oracle is mostly
*"the ν at which a marginal power-law extrapolation crosses the horizon
cap"*, not a sharp blow-up/no-blow-up transition. That is a qualitatively
softer measurement than the a=0 axis, and the monotone violation is its
visible symptom. Resolution-exactness survives (max Δ = 0.8·tol) because
the fits are deterministic — but a GA fitness whose boundary semantics sit
on a fit-quality knife edge inherits flicker sensitivity everywhere.

### a=0.4 fails the non-trivial optimum — Stage 2's disease, softened

Gap between best init-prior draw (0.1520) and best structured shape
(0.1590) is 7·tol — prior sampling reaches within 5% of the top of the
landscape (the gate requires ≥ 10·tol). Spearman rank correlation between
ν_crit and k=1 energy fraction is 0.79, and 15 of the top 16 shapes have
k1 fraction ≥ 0.8. The k=1 refuge is no longer the *pure* optimum (pure
sin(x) sits mid-pack at 0.1434 vs top 0.1590 — advection does punish pure
k=1), but low-k dominance still organizes the landscape top, and the prior
reaches it by sampling.

Interesting physics, either way: ν_crit at a=0.4/0.7 is *larger* than at
a=0 (0.159 and 0.157 vs 0.053 for the best shapes) — moderate advection
*helps* blow-up survive viscosity at this horizon under this oracle
(consistent with the fit-decided caveat above: part of that "help" is
slow-growth extrapolation, not demonstrated amplification).

## Candidate B — bandwidth-constrained ν_crit at a=0 (k≤2 ≤ 50%): FAIL

Implementation (commit `a005ef8`): the energy fraction in modes k ≤ 2 is
capped at 0.5 at normalization — the low block is scaled onto the cap
boundary, then total energy is renormalized; enforced inside
`normalize()`/`effective_coeffs()` so every operator, the init prior, and
the literature baseline all respect it (unit-tested: cap + budget hold
after every operator; projection is idempotent and lands exactly on the
boundary; pure-k≤2 genomes are infeasible and raise). Four structured
shapes (sin(x), sin(2x), sin(x)±0.5sin(2x)) are infeasible by construction
and excluded; 36 shapes remain (16 structured + 20 prior draws).

Sweep: 72 bisections (36 shapes × N ∈ {256, 512}) at a=0, range [0, 0.1],
tol 1e-3. Data: `experiments/stage2_5_sweep_b.jsonl`.

| property | result |
|---|---|
| 1. nonzero | PASS (34/35 uncensored > 2·tol; only the beyond-horizon control bump(κ=5) censored low) |
| 2. finite | PASS (nothing censored high) |
| 3. monotone | PASS (0 violations in 35 probed bisections — the a=0 axis keeps its crisp amplification-decided boundaries) |
| 4. resolution-stable | PASS (median Δ = 0, max Δ = 1.6·tol on a 36·tol spread) |
| 5. wide band | PASS (0.002–0.0379, 36·tol) |
| 6. non-trivial optimum | **FAIL — decisively** |

Property 6 detail: the top of the landscape is a seven-way tie at
ν_crit = 0.0379 — six init-prior draws and one structured shape — and
every one of them sits at **exactly** the cap boundary (k≤2 fraction
= 0.500, k1 fraction ≈ 0.5). The best prior draw does not sit "clearly
below" the best structured value; it *equals* it (gap = 0.0·tol).
Spearman rank correlation between ν_crit and k1 fraction is **0.91** —
under the cap, fitness is again a near-monotone function of low-k
concentration, now saturating at the constraint instead of at k1 = 1.
This is PLAN.md's stated candidate-B risk ("the optimum pins to the
arbitrary cap boundary and the landscape inherits its value") realized in
full: the cap does not remove the trivial optimum, it just moves it to a
boundary any high-p prior draw projects onto automatically.

## Conclusion and what it means

Stage 2's negative result is now shown to be a property of the **fitness
axis family**, not of one configuration. Under the frozen v2 oracle at
t_max=12:

- ν_crit at a=0: trivial optimum at k=1 (Stage 2, replicated 3 seeds).
- ν_crit at a=0.4: trivial-adjacent optimum (low-k mixtures), prior
  reaches within 7·tol; ρ(k1) = 0.79.
- ν_crit at a=0.7: the only variant whose top shows genuine structure
  (gap 21·tol) — but its boundary semantics are soft (37/37 fit-decided,
  T* near cap) and it fails monotonicity via fit-quality flicker.
- ν_crit at a=1.0: dead axis (35/40 censored low).
- ν_crit at a=0 under a k≤2 cap: optimum pins to the cap boundary,
  gap 0.0·tol, ρ(k1) = 0.91.

A GA cannot beat budget-matched random sampling on any of these, and per
the Stage 2 methodology lesson that is now measurable for ~40 bisections
per candidate *before* any GA compute is spent — the six-property gate did
its job.

**Paths forward (all redesign-level, deliberately not taken unilaterally;
for review):**

1. **Harden the oracle (v3) and revisit a=0.7** — the only landscape with
   a structured top. E.g. require amplification-decided boundaries
   (extending t_max so slow growers can amplify), or add hysteresis /
   N-agreement to the fit rule to kill classification flicker. Changes the
   measured quantity; needs its own Stage-1.5-style validation sweep.
2. **Change the fitness quantity, not the constraint**: e.g. blow-up *rate*
   or T* margin at a fixed small ν (PLAN.md Stage 1.5's original fallback),
   or a normalized resistance (ν_crit relative to the shape's own νk²
   prediction — fitness = ν_crit · k_centroid², measuring resistance
   *beyond* the dissipation scaling that dominates every landscape above).
3. **Accept the finding**: on this model family at this horizon,
   viscosity-resistance is spectrally trivial; the scientifically honest
   deliverable is the map + this negative result, and the search premise
   moves to Stage 4's richer dynamics (where dissipation-vs-structure
   trade-offs are not one scaling law).

## Methodology notes

- The range ladder mattered: nearly half the a=0.4/0.7 bisections extended
  to [0, 0.4] (Stage 2's [0, 0.1] would have censored them high).
- Property 6's gap threshold is 10·tol ("clearly below"); Stage 2's failure
  signature was 0–0.2·tol, a=0.4's 7·tol is marginal-but-failing, a=0.7's
  21·tol passes. The threshold choice does not change any verdict here:
  a=0.7 fails on monotonicity independently.
- All monotonicity probes, censoring rules, and predicate decisions are
  identical to the frozen Stage 2 oracle; no predicate changes were made in
  Stage 2.5 (the fit-quality flicker finding argues for a future oracle v3 —
  e.g. requiring amplification-decided boundaries or an R² hysteresis band —
  but that is redesign work, deliberately not done unilaterally here).
