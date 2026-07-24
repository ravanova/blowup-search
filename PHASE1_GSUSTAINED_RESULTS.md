# Phase 1 — staged `g_sustained` probe results

*Route A Phase 1, the forward decision after Gate 4 (2026-07-24). The `ν_crit`
fitness FAILED Gate 4 property 6 (PHASE1_GATE4_RESULTS.md); the open decision was
whether an **inviscid growth-rate** currency could pass a full Gate 4 with two
refinements — (1) a fixed-absolute growth window re-verified for N-stability, and
(2) a free-split property-6 check. This records the STAGED, cheap-first probe of
those refinements (`phase1_gsustained_probe.py`, commit `c1cf817`; data
`experiments/phase1_gsustained_probe.jsonl`, curated to
`writeup/data/phase1_gsustained.json`), run BEFORE any 40-shape gate. STOPPED for
review at the last (expensive) de-risk.*

## Verdict (one line)

**The inviscid growth-rate *magnitude* is on the same uniform-grid resolution wall
that killed `ν_crit` — but the *rank order* is resolution-stable, and one currency
(`g_frac`) survives the full cheat audit.** So the honest reframing is: the
fixed-window refinement (1) does **not** work as a *magnitude* fix, yet a
**rank-based** `g_frac` fitness clears direction, the ω₀/dissipation cheats, and
the free-split property-6 check (2). The one un-run de-risk — 256→512 **rank**
stability — is paused for review.

## The forward decision this addresses

`ν_crit` was doomed because it is a measure *about viscosity*: it inherits the
νk² dissipation wall (trivial low-k optimum) and, on the free ω/θ genome, an
amp = max|ω|/max|ω₀| denominator cheat (ρ(ν_crit, log|ω₀|) = −0.90). The proposed
escape was to measure **inviscidly** (ν=0, no νk² term) and as a growth **rate**
over a mid-run window (a log-derivative, so it never divides by ω₀). A cheap probe
cleared the exact bars `ν_crit` failed, with two open caveats. This staged probe
closes — or fails to close — those caveats before spending a 40-shape gate.

## LEG 1 — the fixed-window refinement FAILS: magnitude is on the resolution wall

Refinement (1) hoped a **fixed-absolute** growth window (like the spike's stable
`g`) would remove the fractional window's N-drift. It does not, and the reason is
structural, not a tuning bug.

On the labeled ground truth (`smooth_sharp` blows up, `smooth_mild` saturates,
`euler_control` flat), the blow-up shape **re-accelerates right at the edge of its
trusted window**, and `tail_guard` keeps pushing that edge outward as N grows
(t_res 2.46 → 2.74 → 2.98). So every window that *captures* the near-singularity
signal has a magnitude that climbs monotonically with N:

| IC | g_frac @128 | g_frac @256 | g_frac @512 | t_res @128→512 |
|----|------------|------------|------------|-----------------|
| smooth_sharp | +0.663 | +0.793 | **+0.968** | 2.46 → 2.98 |
| smooth_mild  | +0.421 | +0.421 | +0.421 | 4.00 (saturates, stays resolved) |
| euler_control | 0.000 | 0.000 | 0.000 | 4.00 |

A window *stable* enough not to drift sits in the earlier region where the spike
already showed the mis-ranking `g(mild) 1.24 > g(sharp) 0.61`. **This is spike
finding #3 reasserting** (the near-singularity rate/exponent never
resolution-converges on a uniform grid) — the *same root wall* as `ν_crit`, now on
the growth-rate axis. Direction on the labeled ICs is nonetheless correct at every
tested N: `g_frac`(sharp 0.79 > mild 0.42 > control 0.00).

## LEG 2 — the rank order IS stable, and `g_frac` survives the cheat audit

The magnitude is on the wall, but for a MAP-Elites/QD map only the *ranking* needs
to be stable (binning is on resolution-stable descriptors; a rank-stable fitness
makes stable elite-selection decisions even with drifting absolute values). On the
fixed-split (0.5) 20-shape roster at N=128 vs 256:

| currency | Spearman(rank@128, rank@256) | winner | winner is a grower? | top-5 that under-resolve |
|----------|------------------------------|--------|---------------------|--------------------------|
| **`g_frac`** = rate over [0.5·t_res, t_res] | **+0.901** | rand_01 | **yes** | **5/5** |
| `accel_ratio` = late_rate / early_rate | +0.949 | rand_08 | **no (full T_MAX)** | 3/5 |

`accel_ratio` is *more* rank-stable but is a **small-denominator cheat** —
ρ(accel_ratio, early_rate) = **−0.66**, its winner is a non-blow-up shape that
never under-resolves, and it mis-ranks the labeled ground truth (rand_08 +3.6 ranks
*above* the known-blow-up sharp +1.4). It is the ω₀ cheat in a new disguise. Its
+0.95 rank-stability is real but organized *by the cheat* (early_rate is itself
resolution-stable). **Lesson, again: rank-stability is necessary, not sufficient —
interrogate the winner against the dumbest cheat.**

`g_frac` passes the audit `accel_ratio` fails:

| audit (N=256 growers) | `g_frac` | reading |
|-----------------------|----------|---------|
| ρ(·, log\|ω₀\|) | **+0.17** | ~0 — no ω₀ denominator cheat (it's a rate, not a ratio) |
| ρ(·, early_rate) | +0.27 | weak — not just the spike's early-growth mis-rank |
| ρ(·, centroid) | **+0.31** | rewards structure (flipped +ve vs `ν_crit`'s −0.21) |
| ρ(·, t_res) | **−0.70** | good: shapes that generate small scales *fastest* (shortest trusted window) rank highest; the three full-T_MAX non-growers sink to the bottom |

## LEG 3 — caveat 2 (free split) is FAVORABLE

Freeing the ω/θ split could let `g_frac` develop its *own* trivial optimum (dump
energy into θ → more buoyancy forcing → faster growth → rail to split=1, ω₀→0).
It does not.

- **Controlled split-sweep (structure fixed, split varied):** all three base
  shapes have an **interior** optimum (argmax split 0.3–0.5) and `g_frac`
  *decreases* toward split=0.97 — no rail. The physics wants a balance of ω and θ.
- **Free random roster:** ρ(g_frac, split) = +0.73 looks like a split preference,
  but split and ω₀ are mechanically entangled (ρ(split, log|ω₀|) = −0.92 at fixed
  energy). Partial correlations disentangle it:
  - **partial ρ(g_frac, log\|ω₀\| \| split) = +0.04** → once split is controlled,
    **no residual ω₀ effect**: the small-denominator cheat that killed `ν_crit` is
    **definitively absent**.
  - partial ρ(g_frac, split \| log\|ω₀\|) = **+0.41** → the split preference is
    genuine **buoyancy physics**, not the ω₀ artifact. (Buoyancy strength is the
    actual driver of Boussinesq vorticity growth.)

**Honest caveat this surfaces:** split (a *logged, not binned* descriptor)
dominates ω-geometry in `g_frac`'s ranking (partial ρ(g_frac, centroid | split) =
+0.09). A full Gate 4 must therefore evaluate property 6 *controlling for split*,
and the archive can re-bin on split from the logs.

## Consequence / open decision (paused for review)

`g_frac`, used as a **rank-based** fitness, is direction-correct, cheat-free
(no ω₀/small-denominator/dissipation triviality), rewards structure at fixed split,
and is caveat-2-favorable — and its rank is stable at N=128↔256 (+0.90). Its
*magnitude* is on the uniform-grid resolution wall, so a full Gate 4 must:
1. reformulate "resolution-stable" (property 4) as **RANK-stable**, and
2. evaluate property 6 (non-trivial optimum) **controlling for split**.

The remaining, un-run de-risk is the **256→512 rank-stability check** — does the
*ranking* hold at higher N, or is even the rank on the wall? It is the expensive
leg (~20–40 min of N=512 solves) and is **paused for review** before either
running it (→ full reformulated Gate 4 if it holds) or accepting the negative.

## Honest framing (unchanged)

2D Boussinesq is a toy model, not 3D Navier–Stokes; a viable fitness axis is
machinery for a search, not a blow-up. Even a full Gate-4 pass would yield only a
resolution-stable **shape→growth QD map with Tier-1 candidates** — uniform-grid
Tier-2 of the true Hou–Luo singularity remains out of reach (Route D). The unifying
finding of this probe is that **two independent currencies (viscosity-resistance
and inviscid growth-rate *magnitude*) hit the *same* uniform-grid resolution wall**;
the only clean escape found is to demote the fitness to a **rank**, whose viability
now hinges on the un-run 256→512 rank check. Overall Clay odds stay ~0.05%.
