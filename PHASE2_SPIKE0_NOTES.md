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

## Sources
- Zheng, Hou, et al., *Self-similar finite-time blowups with singular profiles of the
  generalized Constantin–Lax–Majda model*, arXiv:2603.25104 (exact scheme + CLM profile).
- Chen & Hou, *Stable nearly self-similar blowup … II: Rigorous Numerics*, arXiv:2305.05660.
- Hou, *Stable Nearly Self-Similar Blowup of the 2D Boussinesq …* (MMS numerics, 2025).
