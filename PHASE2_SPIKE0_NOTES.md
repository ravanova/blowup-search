# Phase 2 — Spike 0 reconnaissance notes (dynamic rescaling on 1D gCLM)

**Status:** in progress. Cheap probes run (scratch), formulation derived, three
findings banked. NOT yet a validated solver. This doc records what the probes
established so the stable formulation can be built without re-deriving.

**Goal of Spike 0:** implement one-scale dynamic (self-similar) rescaling on the
existing 1D gCLM solver and validate it recovers a *known* self-similar blow-up,
before porting the machinery to 2D Boussinesq (Spike 1).

## Known-answer target (CLM, a=0)

Initial data `w0 = -sin(x)` → CLM closed-form blow-up at `x=0`, `T* = 2`. Local
self-similar structure `w(x,t) ≈ (T-t)^{-1} Φ(x/(T-t))` with explicit profile

```
Φ(η) = -4η / (1 + 4η²).
```

In rescaled time `τ = -log(T-t)`: amplitude `c_ω = e^{βτ}`, length `c_l = e^{δτ}`,
with **true exponents β = 1, δ = -1** (so `w ~ 1/(T-t)`, length `~ (T-t)`).

## Rescaled formulation (derived)

Write `w(x,t) = c_ω(τ) W(y,τ)`, `y = x/c_l(τ)`, `dτ/dt = c_ω`. The Hilbert
transform is scale-invariant (`H` commutes with dilation), so the rescaled gCLM
equation is

```
W_τ = -β W + δ y W_y - a Ũ W_y + W·HW,     Ũ_y = HW,   β = d log c_ω/dτ,  δ = d log c_l/dτ.
```

For CLM (`a=0`) the advection term drops: `W_τ = -β W + δ y W_y + W·HW`.
A self-similar profile is a steady state `W_τ = 0`.

**Modulation (choosing β, δ each step).** Two normalization conditions pin the
amplitude/length gauge. Robust integral form — conserve `I2 = ∫W²` and
`J2 = ∫W_y²` (integration by parts, periodic):

```
2β + δ = R1 = 2·∫W²·HW / ∫W²
2β − δ = R2 = −2·∫W_yy·W·HW / ∫W_y²
  ⟹  β = (R1+R2)/4,   δ = (R1−R2)/2.
```

## Findings from the probes (scratch/probe_rescale_clm.py, v1→v3)

1. **Periodicity is NOT the wall for the CLM profile.** Earlier worry was that the
   `~1/y` tail would break periodicity as the frame zooms. In practice the rescaled
   profile stays localized: edge value `|W(±π)| ≈ 0.01–0.02` while stable. So the
   existing periodic pseudo-spectral machinery (`solver/spectral_utils.py`) is a
   viable substrate for the CLM POC — **no whole-line solver needed for Spike 0.**
   (This corrects the initial pessimism; the cheap probe earned its keep.)

2. **Pointwise high-derivative normalization is unusable.** Pinning `W_yyy(0)` (a
   third pointwise derivative) is a noise amplifier: the `(ik)³` multiplier makes
   `W_yyy(0)` read ~1000 when the analytic value is 1. Integral-based modulation
   (finding-3 system) is the correct family — no pointwise high derivatives.

3. **One-scale rescaling is unstable here — the known scaling instability.** With
   integral modulation, β climbs correctly *through* the target (β passes ≈1 near
   τ≈2.5) — the physics is right — but then the rescaled solution **overshoots and
   blows up in the rescaled frame** (maxW: 3→52→NaN by τ≈3), and the length rate δ
   fails to develop (stays ≈0 instead of →−1), so the frame never zooms. This is
   the one-scale scaling instability Chen–Hou report and which motivated their
   **two-scale dynamic rescaling** formulation ([arXiv:2305.05660], and the Hou MMS
   2025 numerics paper). It is a formulation issue, not a coding bug.

## What Spike 0 still needs (the real work)

The remaining substance is a **stable, convergent** formulation. Candidate fixes,
to ground in the published scheme rather than re-derive by trial and error:
- **Explicit renormalization each step** (rescale amplitude *and* the y-grid to pin
  the normalization exactly, accumulating `c_ω`, `c_l`) instead of relying on the
  `−βW + δyW_y` modulation terms alone — discretely far more stable, and forces the
  length zoom the δ-term failed to produce.
- **Two-scale dynamic rescaling** (Chen–Hou) if the one-scale instability persists —
  a second scaling degree of freedom eliminates it.
- Correct **success predicate** (pre-committed): rescaled solution reaches a steady
  profile; recovered `β → 1`, `δ → -1` within tolerance; profile matches
  `Φ = -4y/(1+4y²)` (shape error < tol); reconstructed `T*` matches
  `clm_analytic_blowup_time` (2.0).

**Recommended next step:** pull the exact one-scale/two-scale formulation +
normalization from the Hou MMS-2025 numerics paper before more coding, then
implement `solver/gclm_rescaled.py` + `test_gclm_rescaled.py` against the predicate
above. Probe code: `phase2_spike0_probe.py` (repo root).

## Sources
- Chen & Hou, *Stable nearly self-similar blowup … II: Rigorous Numerics*, arXiv:2305.05660.
- Hou, *Stable Nearly Self-Similar Blowup of the 2D Boussinesq …* (MMS numerics, 2025),
  users.cms.caltech.edu/~hou/papers/MMS-Numerics-2025.pdf.
