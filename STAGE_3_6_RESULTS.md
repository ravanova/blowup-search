# Stage 3.6 — Route A, Phase 0: rough-data spike results

**Verdict: RAILS (the expected branch of the pre-committed gate). Genuine
limited-regularity (C^{0,α} Hölder) vorticity does NOT give a resolution-stable
non-generic blow-up exponent near a=1 on gCLM, even at N up to 4096. The
fine-N measurement is validated at the a=0.7 control (generic α≈1, stable), so
this is a trustworthy negative, not a measurement failure. Per the gate: gCLM
is confirmed exhausted for smooth AND rough data at reachable resolutions.
Carry the rough-data representation principle + the validated fine-N
exponent-measurement method into Phase 1 (2D Boussinesq); a Phase-0 negative is
informative, NOT a kill-signal for Phase 1 (Boussinesq blow-up is a different
mechanism).**

This closes CLAY_ROADMAP.md **Route A, Phase 0**. Its value is exactly the two
transferable things it was scoped to produce — a genuine rough-data genome mode
and a validated fine-N exponent measurement — plus an honest exhaustion check,
NOT a gCLM result.

Date: 2026-07-23. Deliverables: rough-data genome mode in
[ga/genome.py](ga/genome.py) (`holder_profile` / `rough_genome` /
`realize_holder`), unit-tested in [test_genome_rough.py](test_genome_rough.py)
(7/7); sweep [stage3_6_sweep.py](stage3_6_sweep.py); pre-committed gate
[analyze_stage3_6.py](analyze_stage3_6.py); live viewer
[stage3_6_progress.py](stage3_6_progress.py). Data:
`experiments/stage3_6_sweep.jsonl` (72 rows).

---

## Deliverable 1 — the C^{1,α} rough-data genome mode

The old `k^{-p}` envelope reaches spectrally-*decaying* shapes, but with random
phases it produces a delocalized random Fourier field, not a profile with a
genuine, localized limited-regularity singularity — the kind the De Gregorio /
2D-Boussinesq blow-up literature (Elgindi–Jeong, Chen–Hou,
Buckmaster–Gómez-Serrano) actually uses (Hölder velocity u ∈ C^{1,α}, i.e.
vorticity ω ∈ C^{0,α}). The new mode constructs exactly that:

    f_h(x) = sign(sin x) · |sin x|^h,      h ∈ (0, 1]

an odd, 2π-periodic vorticity with a localized Hölder-h cusp at x=0 and x=π
(near 0 it is sign(x)|x|^h). h=1 is exactly sin(x) — the smooth endpoint —
so the mode connects continuously to the existing smooth genome.

[test_genome_rough.py](test_genome_rough.py) certifies the *intended
regularity* directly (7/7 passing):
- the real-space local Hölder exponent at the cusp equals the requested h
  (fitted slope of log|f| vs log x within 1e-3 of h) — the definitional
  regularity certificate;
- h=1 is exactly sin(x) (bitwise);
- the profile is genuinely **not C^1** for h<1: max|f′| ∼ N^{1-h} diverges
  under grid refinement (bounded only for h=1) — the C^{0,h}-not-C^1 signature;
- roughness is monotone in h (high-k energy fraction rises as h falls; the
  logged `spectral_tail_slope` descriptor tracks it);
- the GA-genome wrapper stays odd and energy-normalized.

This profile is model-agnostic — it is the "rough-data representation
principle" the roadmap carries into Phase 1; only the solver changes there.

## Deliverable 2 — the fine-N exponent measurement

[stage3_6_sweep.py](stage3_6_sweep.py) runs one inviscid (ν=0) blow-up per
(h, a, N) and fits the **blow-up-rate exponent** α (M ∼ (T*−t)^{−α}) via
`win_condition.estimate_blowup_time(fit_exponent=True)` — held-out
(out-of-sample) validated, so the reported R² is honest. Roster: the 6
Hölder profiles h ∈ {0.20, 0.35, 0.50, 0.65, 0.80, 1.00}, realized
analytically at each grid N so refining N resolves more of the Hölder tail
(not a truncated fixed genome). a ∈ {0.7, 0.9, 0.95, 1.0}; N ∈ {1024, 2048,
4096}. Frozen: t_max=24, amplification 1e3 (3 decades), tail_fraction 0.15,
max_steps 200k, early-decay exit — matching the Stage 3.5 substrate except for
the resolutions. `conservation_drift` guard on every run.

> **Two "α"s, kept separate:** `h` is the *data* regularity (Hölder exponent
> of the initial vorticity); `α` is the fitted *blow-up-rate* exponent (the
> gated quantity). They are unrelated.

## The a=0.7 control (validate the measurement where the answer is known)

Per the roadmap ("build and validate the measurement on the substrate with
known answers"), a=0.7 is a methodological control, not a target. Stage 3.5
established that at a=0.7 blow-up is generic (α≡1) and resolution-exact for
every regularity class. The fine-N measurement **recovers exactly that**:

| h | α@1024 | α@2048 | α@4096 |
|---|---|---|---|
| 0.20 | 1.00 | 1.00 | 1.10 |
| 0.35 | 1.00 | 1.00 | 1.05 |
| 0.50 | 1.00 | 1.00 | 1.05 |
| 0.65 | 1.00 | 1.00 | 1.00 |
| 0.80 | 1.00 | 1.00 | 1.00 |
| 1.00 | 1.00 | 1.00 | 1.00 |

18/18 blow up with usable fits; α is generic (≈1) and stable across a 4×
resolution range. (The roughest shapes tick up to 1.05–1.10 only at N=4096 —
itself a mild finite-resolution wobble, but it stays generic and never rails.)
**Gate control: PASS** — the measurement is trustworthy near a=1.

## Results near a=1 (the target)

| a | blow-up | usable fits | median cross-N α span | max span | verdict |
|---|---|---|---|---|---|
| **0.9** | 18/18 | 18/18 | **0.65** | 1.95 | unconverged (scatters) |
| **0.95** | 14/18 | 12/18 | **0.65** | 2.70 | rails / flips |
| **1.0** | **0/18** | 0/18 | — | — | dead axis |

**a=0.9 — every shape blows up, but the exponent never converges.** The fitted
α scatters non-monotonically across resolution (e.g. h=0.50: 2.60 → 0.65 →
1.20; h=0.65: 0.45 → 0.80 → 2.00; h=0.20: 1.85 → 1.65 → 1.10). Median
cross-resolution span 0.65 (13× the 0.05 grid step), max 1.95. Only the smooth
control h=1.00 lands near a stable α≈1. Rough data changed blow-up
*occurrence* (18/18 usable here, vs 20/40 usable and 15 flips at a=0.9 in
Stage 3.5's N∈{256,512}) but not exponent *convergence*.

**a=0.95 — railing and well-definedness flips.** h=0.20 spans the entire fit
grid across resolution (0.30 → 0.85 → 3.00, i.e. rails to the 3.00 edge at
N=4096); 4/18 runs do not blow up (or lose fit reliability) at some N, flipping
well-definedness with resolution. Max cross-N span 2.70.

**a=1.0 (De Gregorio proper) — dead axis.** 0/18 blow up within
(t_max=24, amp=1e3, 200k steps), even for the roughest h=0.20 C^{0,0.2} data;
the slow near-critical runs hit the step cap. **Per WIN_CONDITION.md this is
NOT evidence of regularity** — only the absence of a searchable blow-up signal
at these settings.

**The railing is not a crude under-resolution artifact.** Max
`conservation_drift` over all 72 runs is 1.9×10⁻⁴, comfortably under the 1×10⁻³
guard, and the individual held-out fits clear R²≥0.9. The runs are
well-resolved by the conserved-quantity guard and each fit is individually
clean — yet the exponent has no resolution-stable limit. That is the essential
finding: the non-generic exponent near a=1 is a grid-scale feature of gCLM, not
a converged physical quantity. Going from Stage 3.5's N∈{256,512} to
N∈{1024,2048,4096} did **not** shrink the exponent scatter (max span 2.70 here
vs Stage 3.5's max Δα=2.7) — refinement does not help.

## Gate outcome (pre-committed, not softened)

```
control a=0.7: 6 well-defined at fine N, 3 converged & generic (α~1) -> PASS
target  a=0.9:  converged_generic=1, unconverged=5
target  a=0.95: flip=3, railing=1, unconverged=2
target  a=1.0:  dead=6
-> RAILS (EXPECTED)
```

With the measurement validated at the control, **no (h, a) near a=1 yields a
converged, non-generic blow-up exponent.** This is the gate's *expected* branch.

## What this means, and the forward move (a scope decision — for review)

- The rough-data bet — that genuine C^{0,α} data would unlock a resolution-
  stable non-generic exponent where smooth/random data could not — **does not
  pay off on gCLM.** Rough data revives blow-up *occurrence* near a=0.9–0.95,
  but the exponent still rails, and De Gregorio proper (a=1.0) stays a dead
  axis for smooth *and* rough odd data at these resolutions.
- This **confirms and hardens** the Stage 3.5 conclusion (NONGENERICITY_RESULTS.md)
  with the strongest cheap probe available: not just finer N, but genuine
  limited-regularity data at finer N. The cheap 1D route to a *novel*
  (non-generic, Tier-3-provable) result is closed.
- **The deliverables transfer.** Per the pre-committed gate and CLAY_ROADMAP.md
  Route A, the two things Phase 0 was scoped to produce — (i) the validated
  rough-data representation principle (`holder_profile`), and (ii) a fine-N
  exponent-measurement method proven to distinguish a converged exponent from a
  grid-scale rail (validated on the a=0.7 known answer) — are exactly what
  Phase 1 (2D Boussinesq / rough De Gregorio) needs. A Phase-0 negative on
  gCLM is **informative, not a kill-signal for Phase 1**: Boussinesq blow-up is
  a different mechanism, and it is where the literature's *provable* non-generic
  blow-ups actually live.
- **Recommendation (for review):** proceed to Route A, Phase 1 — stand up a 2D
  Boussinesq (or rough-data-capable De Gregorio) solver, port this fine-N
  exponent method and the rough-data representation, and **re-run the
  six-property viability gate on its fitness before any GA compute** (Stage 3.5
  is why). Do not spend further compute on the gCLM non-genericity axis.

The honest ceiling is unchanged: these are 1D toy models, Tier 2 is not a
proof, and overall odds of a Clay result stay ~0.05% behind the two structural
walls (a search can only argue *for* blow-up; provable blow-up lives only in
simple models, not 3D NS). The reachable win remains a *novel* Tier-2 (and,
with an expert collaborator, Tier-3) candidate in a model where provable
non-generic blow-up exists — which is what Phase 1 targets.
