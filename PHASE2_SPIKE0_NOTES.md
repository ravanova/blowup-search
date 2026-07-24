# Phase 2 — Spike 0 notes (dynamic rescaling on 1D gCLM)

**Status: SPIKE 0 COMPLETE (2026-07-24) — validated against the known answer.**
The dynamic self-similar rescaling POC works: on a sinh-stretched whole-line grid,
CLM (a=0) dynamic rescaling recovers the exact profile Ω̄₀=−4X/(1+4X²) to shape
error ~2e-6 with the exact rate c_ω→−1, resolution-stable. Code: `solver/line_hilbert.py`,
`solver/gclm_rescaled.py`; tests `test_line_hilbert.py` (6/6), `test_gclm_rescaled.py`
(5/5). See the "SPIKE 0 COMPLETE" section at the bottom. The reconnaissance record
below is preserved for the derivation trail.

**Reconnaissance status (historical):** cheap probes run (scratch), formulation
derived, three findings banked. This doc records what the probes established so the
stable formulation could be built without re-deriving.

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

## CORRECTION + the exact published scheme (from arXiv:2603.25104)

The grounding pass overturned finding-1 and finding-3's proposed fixes. The naive
periodic run was *stable but converging to the WRONG profile* (`B_fit ≈ -1`, not the
CLM value 4) — because **the true CLM self-similar profile is a whole-line,
`~1/X`-decaying function and requires the *line* Hilbert transform**, which differs
from the periodic one for such slow tails. So a whole-line discretization IS needed
after all; the periodic probe's apparent localization was an artifact of the wrong
(periodic) `H`.

The exact scheme for gCLM (Zheng–Hou et al., *Self-similar finite-time blowups …
of the gCLM model*, arXiv:2603.25104), convention `ω(x,t) = C_ω(τ)^{-1} Ω(X,τ)`,
`X = C_l x`, `dτ/dt = C_ω^{-1}`, `C_ω = exp∫c_ω`, `C_l = exp∫c_l`:

**Rescaled equation:**
```
Ω_τ + (c_l X + a U) Ω_X = (c_ω + U_X) Ω,     U_X = H(Ω)
U(X,τ) = (1/π) ∫_ℝ ln|(X-Y)/Y| Ω(Y,τ) dY      (line velocity, U(0)=0)
```
For a=0:  `Ω_τ = (c_ω + HΩ) Ω − c_l X Ω_X`.

**Normalization (non-degenerate, value/first-derivative based — robust):**
```
Condition 1 (fix slope Ω_X(0,τ)=Ω_X(0,0)):   c_l = c_ω + (1-a) U_X(0,τ)
Condition 2 (a=0):                            c_ω = 1 − U_X(0,τ) = 1 − HΩ(0,τ)
  ⟹ for a=0:  c_l ≡ 1  (constant),   c_ω = 1 − HΩ(0).
```

**Exact CLM (a=0) target (non-degenerate):**
```
Ω̄₀(X) = −4X/(1+4X²),   H(Ω̄₀)(X) = 2/(1+4X²),   c_ω → −1,  c_l = 1,  γ = 1.
```
(Sign/convention map to my derivation: their `c_ω=−1, c_l=1` ⇔ amplitude
`~1/(T-t)`, length `~(T-t)` — same physical blow-up.)

The `HΩ̄₀ = 2/(1+4X²)` pair is a ready-made **unit test for the line Hilbert
transform** (the hardest component): any discretization must map `−4X/(1+4X²)` to
`2/(1+4X²)`.

## What Spike 0 still needs (the real work, now de-risked)

1. **Whole-line discretization** — mapped/stretched grid or large-domain FFT — with
   a validated **line** Hilbert transform (unit-tested on the pair above) and the
   log-kernel velocity `U`. This is the crux; the paper's Appendix C has their
   method (mapped grid; not in the fetched excerpt).
2. Time-step the a=0 rescaled equation with `c_ω = 1 − HΩ(0)`, `c_l = 1`, from
   odd data; **success predicate (pre-commit):** `Ω → Ω̄₀ = −4X/(1+4X²)` (shape
   err < tol), `c_ω → −1`, and reconstructed `T*` matches `clm_analytic_blowup_time`
   (2.0), all resolution-stable.

**Next step:** build `solver/gclm_rescaled.py` + `test_gclm_rescaled.py` on a
whole-line grid, testing the line Hilbert transform first. Probe (periodic, WRONG-H —
kept as a negative example): `phase2_spike0_probe.py`.

### Build finding: uniform whole-line grid is a dead end; a MAPPED grid is required

Verified components on a large **uniform** line grid `[-Xmax,Xmax]` (FFT-based):
- **line Hilbert transform works** but converges slowly — `~1/Xmax` truncation error
  from the `~1/X` tail (`≈6e-3` at Xmax=200, `≈3e-3` at Xmax=400), N-independent.
- **the `−c_l X Ω_X` dilation term is CFL-strangled**: even initialized *exactly at*
  `Ω̄₀`, an explicit RK4 step NaNs. Diagnosis (confirmed by the numbers, not a fixable
  instability — a spectral filter did not help): the advection *speed* is `X` itself,
  up to `Xmax`, so explicit stability needs `dτ < dX/Xmax ≈ 0.024/200 ≈ 1×10⁻⁴`,
  whereas `2×10⁻³` was used (20× over). A CFL-safe `dτ` makes the uniform grid ~20×
  more expensive AND still carries the slow `~1/Xmax` tail error. Uniform grid = wrong
  tool.

This is exactly why the paper discretizes on a **mapped grid**. Under e.g.
`X = L·tan θ`, `θ∈(−π/2,π/2)`: `∂_X = (cos²θ/L)∂_θ`, so the dilation becomes the
**bounded** coefficient `X Ω_X = sin θ cos θ · Ω_θ` (|coeff| ≤ ½) — restoring a sane
CFL *and* resolving the tail (points cluster correctly on the line). The non-trivial piece
is the **line Hilbert transform in the mapped coordinate** (no longer a plain FFT
multiplier) — this is what Appendix C of arXiv:2603.25104 specifies and what should
be extracted rather than reinvented (the session's repeated lesson: ground the
scheme in the paper, don't trial-and-error).

**Concrete remaining build:** (1) get Appendix C's mapped-grid + mapped Hilbert
transform method; (2) implement `solver/gclm_rescaled.py` on that grid with
`c_ω=1−HΩ(0)`, `c_l=1`; (3) `test_gclm_rescaled.py`: line-H unit test on the
`Ω̄₀ ↔ 2/(1+4X²)` pair, steady-profile residual test at `Ω̄₀`, and convergence from
perturbed odd data with `c_ω→−1` — all resolution-stable. Scratch build (uniform,
dilation-unstable — negative example): session scratchpad `build_rescaled.py`.

### Appendix C method (arXiv:2603.25104, Huang–Tong–Wang) — the build recipe

**C.1 line Hilbert transform (NON-FFT, works on a non-uniform grid).** Approximate
`f` on `[−M,M]` with `C¹₀` cubic-spline / Hermite-type basis functions `P_i`, `Q_i`
(chosen so their Hilbert transforms are *bounded*); node slopes `f'_i` from the
standard cubic spline with `f''(x_0)=f''(x_N)=0`. Each basis element's Hilbert
transform is **known analytically**: `H(P_i)=A(l)−A(r)`, `H(Q_i)=(x_{i-1}−x_i)B(l)−
(x_{i+1}−x_i)B(r)` with `l=(x_{i-1}−x_i)/(x−x_i)`, `r=(x_{i+1}−x_i)/(x−x_i)` and
closed-form `A(s), B(s)` (rational + `ln|1−s|`; use the paper's Mathematica minimax
series for `|s|<0.5` to avoid `s→0` cancellation). Diagonal terms:
`H(P_i)(x_i)=(1/π)ln|(x_{i-1}−x_i)/(x_{i+1}−x_i)|`,
`H(Q_i)(x_i)=(x_{i-1}−x_{i+1})/(3π)`. The velocity integral `U` (i.e.
`−(−Δ)^{−1/2}`) is the analytic integral of the same elements → closed forms
`C(d,s), D(d,s)` (again with a minimax series). *Transcribe the exact `A,B,C,D`
series from the PDF at build time — pdftotext mangles the fractions.*

**Grid (stretched, whole-line).** `X(ρ)=X_m(1−cosh ρ)+√(c+X_m²) sinh ρ`, `ρ` uniform
on `[0,ρmax]`, `Δρ=0.01`, truncated at `M=10¹⁰`; `X_m`=argmax|Ω|, `c` set so
`N_bulk=600` points fall in the half-max peak `[X_1,X_2]`. **Why it matters:**
`X~sinh ρ ⇒ dX~X·Δρ`, so the dilation CFL is `dt<dX/X~Δρ≈const`, independent of `M`
— this is what cures the uniform-grid CFL death. (For `a<0` singular profiles they
add AMR regeneration; for a smooth POC a fixed stretched mesh suffices.)

**C.2 time-stepping.** Evolve `f=Ω/Xᵏ` (`k≥3` odd, or `k=1` for the non-degenerate
CLM whose profile vanishes to order 1) to protect the origin vanishing:
`f_τ+(c_l X+aU)f_X=(c_ω+U_X−k(c_l+aU/X))f`. Advection via **WENO5**; time via
**SSPRK(10,4)**. Converge at `‖f_τ‖_∞<1e-8` (exclude the `X≈1` singularity
neighborhood for `a<0`).

**POC simplification (Spike 0, ~1% not machine precision):** fixed stretched mesh
(no AMR), `M~10²–10³` (not 10¹⁰), the C.1 spline-H (essential — the crux), an
upwind/WENO advection + SSPRK or CFL-safe RK. Target: recover `Ω̄₀=−4X/(1+4X²)`,
`c_ω→−1`, reconstructed `T*→2`, resolution-stable.

**Scope:** confirmed a genuine multi-day solver build; all literature gaps now
closed. Paper text cached this session: scratchpad `gclm_paper.txt` (Appendix C at
line ~7169); PDF via `arxiv.org/pdf/2603.25104`.

### BUILT (2026-07-24): the crux — `solver/line_hilbert.py` + `test_line_hilbert.py` PASS

The hardest component is done and validated against the known answer. The line
Hilbert transform on a non-uniform (sinh-stretched) whole-line grid recovers the
CLM pair `H(−4X/(1+4X²)) = 2/(1+4X²)` to **relative error 1.6e-4** (POC target was
1%), with clean monotone convergence under whole-line refinement
(2.35e-3 → 5.22e-4 → 1.16e-4 as core resolution + reach M grow together).

Implementation notes worth keeping:
- **A,B derived, not transcribed.** pdftotext mangled the paper's 23-term minimax
  coefficient lists, so instead of copying them I substituted
  `ln|1−s| = L(s) − s − s²/2 − s³/3` with `L(s) = −Σ_{n≥4} sⁿ/n` into the exact
  `A(s), B(s)` closed forms; the leading polynomial terms cancel *analytically*,
  giving stable small-|s| forms `A = (s³−3s+2)L/(πs³) − (3s²+2s³)/6π`,
  `B = (s−1)²L/(πs³) + (s−2s²)/6π`. This matched the paper's minimax structure
  exactly for B and (with the OCR's detached leading `−`) for A. Verified two ways:
  branch continuity across |s|=0.5, and against the raw closed form at moderate |s|.
  So the minimax coefficient transcription warned about in the recipe is UNNEEDED.
- **Diagonal (x=xᵢ) limits and the s→1 neighbor singularity** both handled:
  `H(Pᵢ)(xᵢ)=(1/π)ln|(xᵢ₋₁−xᵢ)/(xᵢ₊₁−xᵢ)|`, `H(Qᵢ)(xᵢ)=(xᵢ₋₁−xᵢ₊₁)/3π`; the
  `s=1` case (evaluation at an immediate neighbor) is the finite limit
  `A(1)=−5/6π, B(1)=−1/6π` via the `(s−1)²ln|1−s|→0` guard.
- **Node slopes fᵢ′** from a hand-rolled natural cubic spline (Thomas algorithm,
  `f''=0` at both ends) — no scipy in the venv.
- **`line_hilbert_matrix(x)`** returns a dense N×N operator (folds in the linear
  slope map) so the transform is a single matmul reused every RHS eval on the
  fixed grid — ready for the time-stepper.
- **Dominant error is the ~1/M tail truncation, not core resolution** — expected
  for this `~1/X` profile; both knobs must grow to converge. Fine at POC level.

**Next increment:** the stretched-grid time-stepper `solver/gclm_rescaled.py`
(evolve `f=Ω/X`, k=1 for non-degenerate CLM; `c_ω=1−HΩ(0)`, `c_l=1`; WENO5 +
SSPRK(10,4) or a CFL-safe RK) + `test_gclm_rescaled.py` (steady-profile residual
at Ω̄₀, then convergence from perturbed odd data with c_ω→−1, T*→2, resolution-
stable). The velocity `U` (log-kernel) via the C.1 `C,D` integral elements is only
needed for a≠0 advection — **CLM (a=0) does not use U**, so it can be deferred.

## SPIKE 0 COMPLETE (2026-07-24) — the whole POC is validated

`solver/gclm_rescaled.py` + `test_gclm_rescaled.py` (5/5 pass) close Spike 0. The
scheme, reduced for CLM (a=0), and its validation:

**Reduced scheme.** Evolving `f=Ω/X` (k=1) in the computational coordinate ρ
(`X=c·sinh ρ`, uniform ρ), c_l≡1, the rescaled CLM equation is
```
f_τ = −tanh(ρ)·f_ρ + (HΩ − HΩ(0))·f ,     Ω = X·f ,   c_ω = 1 − HΩ(0).
```
The dilation `X Ω_X` becomes `tanh(ρ)·f_ρ` — advection speed ≤ 1, so the CFL is
`dτ ≲ Δρ` independent of the reach M (the uniform-grid CFL death, cured). Method:
3rd-order upwind-biased advection (the profile is smooth → the paper's nonlinear
WENO limiter is unnecessary at POC level; flow is outward at both ends so the
upwind stencil always reaches inward — no ghost points), SSPRK3 in time, line
Hilbert transform as the fixed-grid dense operator.

**Analytic facts used (all verified):** (i) Ω̄₀=−4X/(1+4X²) is an exact steady
state; (ii) the origin slope `f(0)=Ω_X(0)=−4` is frozen *exactly* by the scheme
(both tanh(0) and the source HΩ(0)−HΩ(0) vanish at ρ=0) — this realizes the slope
normalization; (iii) at the fixed point HΩ(0)=2 ⟹ c_ω=−1, self-consistently.

**Validation (pre-committed predicates, all met):**
- STEADY: initialized at Ω̄₀, `‖f_τ‖=4e-6`, c_ω=−0.999, HΩ(0)=1.999.
- FROZEN ORIGIN: f(0)=−4 held to machine precision (0 drift / 300 steps).
- DYNAMIC CONVERGENCE: two *different* perturbed odd ICs (a Gaussian and a narrower
  Lorentzian, both with slope −4) each relax to Ω̄₀ — shape err ~2e-6, c_ω→−0.999.
- RESOLUTION-STABLE: c_ω = −0.9986 (n=901) → −0.9995 (n=1801) trending to −1;
  shape err 4.0e-6 → 7.7e-7 under refinement.

**Headline finding (overturns finding-3's pessimism).** One-scale rescaling is
**dynamically stable and attracting** for CLM — the earlier "one-scale is unstable,
need two-scale" read was an artifact of the *wrong (periodic) Hilbert transform +
integral modulation*, NOT a fundamental scaling instability. With the correct LINE
Hilbert transform and value-based normalization (c_ω=1−HΩ(0), c_l=1), Ω̄₀ is a clean
attractor. (Chen–Hou's two-scale need was for Boussinesq/De Gregorio, a different
mechanism — Spike 1 will reveal whether it recurs there; it does NOT for CLM.)

**Honest scope (do not oversell).** This reproduces a *proven, closed-form* toy
result across Wall C — it validates the machinery, it is not novel and not a proof.
The physical `T*=2` is deliberately NOT claimed here: it is a property of the global
periodic solve (validated by `test_solver_clm.py`), not of a whole-line local
rescaling whose initial amplitude is a free gauge; the correct local analogue is the
rate c_ω→−1 (⟺ ω~(T−t)⁻¹), which is recovered. The velocity U (log-kernel, C.1
`C,D` elements) was correctly deferred — CLM does not use it; it is the first thing
Spike 1 / the a≠0 path will need.

**Spike 0 gate (per PHASE2_NUMERICS_PLAN.md — each spike STOPS for review):** the
technique is de-risked in 1D against a known answer. The forward decision (port to
2D Boussinesq for Spike 1, i.e. the real lift, vs. exercise a≠0/De-Gregorio targets
in 1D first) is a scope decision for the user.

## Sources
- Zheng, Hou, et al., *Self-similar finite-time blowups with singular profiles of the
  generalized Constantin–Lax–Majda model*, arXiv:2603.25104 (exact scheme + CLM profile).
- Chen & Hou, *Stable nearly self-similar blowup … II: Rigorous Numerics*, arXiv:2305.05660.
- Hou, *Stable Nearly Self-Similar Blowup of the 2D Boussinesq …* (MMS numerics, 2025).
