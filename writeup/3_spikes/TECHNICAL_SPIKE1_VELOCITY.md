# Spike 1 (technical) — The 2D Boussinesq velocity operator on a stretched grid

### Step A of the 2D dynamic-rescaling port: grounding, the discretization, and its known-answer validation

*Technical companion to [TECHNICAL_SPIKE0_RESCALING.md](TECHNICAL_SPIKE0_RESCALING.md)
(the 1D result this ports from) and the planning/derivation record
[../PHASE2_SPIKE1_NOTES.md](../../PHASE2_SPIKE1_NOTES.md). Status: **Step A built and
validated; Steps B–C (the rescaled solver + the profile gate) are still ahead.** Figure
`figures/fig9_spike1_stepA_velocity.png` + committed data rebuild with
`python writeup/3_spikes/spike1_stepA_evidence.py`. Source papers in `Papers/` (gitignored).*

---

## 1. Where this sits

Spike 0 validated dynamic self-similar rescaling in 1D (CLM), against a closed-form
answer. Spike 1 ports the machinery to **2D Boussinesq** in the Hou–Luo geometry and aims
to reproduce the *published Chen–Hou self-similar profile* as the validation gate. The
user chose the **de-risked** build order: build and validate the highest-risk new piece —
the 2D velocity operator — as a standalone unit against a known answer *before* wiring the
full rescaled solver. This document is that step (Step A).

The velocity operator is the 2D analogue of Spike-0's non-FFT line Hilbert transform: on
the uniform periodic grid it is a trivial FFT multiplier, but the self-similar profile
lives on the whole quarter-plane with a slow `r^{-1/3}` far-field tail, so it must be
solved on a **stretched** grid where the FFT cannot go.

---

## 2. The grounded formulation (Chen–Hou, transcribed with equation refs)

From Chen–Hou Part I [CH22a-I, arXiv:2210.07191] §2, §7 and the MMS rigorous-numerics
paper [CH25-MMS] §2 (PDFs in `Papers/`).

**Physical 2D Boussinesq**, upper half-plane `ℝ²₊ = {y ≥ 0}`, singularity at the origin
on the wall (2.3)–(2.5):

```
ω_t + u·∇ω = θ_x,   θ_t + u·∇θ = 0
−Δφ = ω,   u = −φ_y,  v = φ_x,   φ(x,0) = 0     (Biot–Savart via the stream function)
```

with **ω odd in x, θ even in x**. Then `φ` is odd in x too, so `φ = 0` on the axis `x=0`
as well as the wall `y=0`: the effective domain is the **first quadrant `[0,∞)²` with the
singular corner at the origin** (the Hou–Luo geometry), and `φ` carries **Dirichlet data
on both** `β=0` and `β=π/2`.

**Dynamic rescaling** (one-scale; MMS (2.9)–(2.11)):

```
ω_τ + (c_l x + u)·∇ω = θ_x + c_ω ω
θ_τ + (c_l x + u)·∇θ = c_θ θ,          c_θ = c_l + 2 c_ω
u = ∇^⊥(−Δ)⁻¹ ω,   modulation:  c_l = 2 θ_xx(0)/ω_x(0),  c_ω = ½ c_l + u_x(0)
```

A self-similar profile is a **steady state**. Note this smooth-data scheme is **one-scale**
(a single isotropic `c_l`); the "two-scale" variant cited in earlier planning was from
Chen–Hou's *C^{1,α}-boundary* work, a different construction. So Spike-0's headline —
one-scale rescaling can be stable/attracting — is the relevant precedent.

**Far-field** (Part I (7.1)): `ω ~ g₁(β) r^α`, `θ ~ g₂(β) r^{1+2α}`, `α = c_ω/c_l ≈ −1/3`.
The Spike-1 gate values: `c̄_l/c̄_ω ≈ −2.92 ⟺ α ≈ −0.34`, `c̄_ω < 0`. The slow `r^{-1/3}`
decay is the 2D analogue of Spike-0's `1/X` whole-line tail — exactly why a stretched grid
is mandatory.

**Honest POC scope.** Chen–Hou's *full* method (6th–8th-order B-spline FEM Poisson,
adaptive mesh to `10¹⁵`, a semi-analytic far-field split, `10⁻⁷` residual, INTLAB interval
bounds) is a months-scale expert program, most of it built for the *proof*. The plan
pre-committed Spike 1 to **qualitative** fidelity. Step A therefore uses a **tractable,
validated** Poisson discretization in place of B-spline FEM — legitimate because the
elliptic solve is textbook (contrast the exotic singular-integral line Hilbert, which had
to be transcribed). The *mathematics* above is kept exactly.

---

## 3. The discretization (the elegant part)

Coordinates: polar `(r, β)`, `β ∈ [0, π/2]`, with a **log-radial** grid `r = e^ρ`
(uniform `ρ`) and the **Dirichlet angular sine basis** `sin(2nβ)`, `n = 1..M−1` — a DST-I
with kernel `sin(πjn/M)` (`β_j = (π/2)j/M`), so the angular transform and its inverse are a
pair of dense matrix multiplies (`S² = (M/2)I`).

The payoff is a clean cancellation. The polar Laplacian is
`Δφ = φ_rr + r⁻¹φ_r + r⁻²φ_ββ`. Expand `φ = Σ_n φ_n(r) sin(2nβ)`, `ω = Σ_n ω_n(r) sin(2nβ)`.
On the **log grid** (`r_ρ = r_ρρ = r`), the radial operator collapses:

```
φ_rr + r⁻¹φ_r = r⁻²(φ_ρρ − φ_ρ) + r⁻²φ_ρ = r⁻² φ_ρρ,
```

so `−Δφ = ω` decouples, per mode, into a **constant-coefficient tridiagonal ODE**:

```
φ_n''(ρ) − (2n)² φ_n = −r² ω_n(r).
```

No sparse linear algebra (there is no scipy in the venv): each mode is a Thomas solve. The
homogeneous solutions `r^{±2n} = e^{±2nρ}` carry the physics of the two boundaries:

- **near-origin regularity:** `φ_n ~ r^{+2n}` (Robin `φ_ρ = 2n φ` at `ρ_min`);
- **far-field decay:** `φ_n ~ r^{−2n}` (Robin `φ_ρ = −2n φ` at `ρ_max`) — the analytic
  `r^{-1/3}`-tail lever at POC level (the paper's semi-analytic split is the high-fidelity
  version of this same idea).

Velocity is recovered by the polar chain rule
`φ_x = cos β·φ_r − (sin β/r)·φ_β`, `φ_y = sin β·φ_r + (cos β/r)·φ_β`, with `φ_r = φ_ρ/r`
(central in `ρ`) and `φ_β` from the sine-basis angular derivative
`φ_β = Σ_n φ_n·(2n)cos(2nβ)`.

**The origin read `u_x(0)`.** The modulation (2.11) needs `u_x(0) = −φ_xy(0)`. Near the
origin the `n=1` mode dominates: `φ ≈ c₁ r² sin(2β) = 2c₁ xy`, so `u = −φ_y ≈ −2c₁ x` and
`u_x(0) = −2c₁` with `c₁ = lim_{r→0} φ₁(r)/r²`. We read it by **linearly extrapolating**
`φ₁(r)/r²` to `r=0` over a small-`r` window (skipping the innermost first-order-BC nodes).
This is a clean, mode-localized read — the antidote to the Spike-0 recon lesson that raw
high-order pointwise origin derivatives are noise amplifiers.

Code: `solver/boussinesq_velocity.py` (`PolarGrid`, `poisson_solve`,
`velocity_from_vorticity`, `u_x_at_origin`).

---

## 4. Validation against a manufactured known answer

Pre-committed predicate ([../PHASE2_SPIKE1_NOTES.md](../../PHASE2_SPIKE1_NOTES.md) §3):
recover a manufactured `(ω, u, v)` to a stated tol; error must **decrease under
refinement**; `u_x(0)` must match analytics. Manufactured field:

```
φ* = r² e^{−r} sin(2β) + r⁴ e^{−r} sin(4β)
ω* = (5r − r²) e^{−r} sin(2β) + (9r³ − r⁴) e^{−r} sin(4β)     (= −Δφ*, verified by hand)
u* = −φ*_y,  v* = φ*_x   (closed form);   u_x(0) = −2
```

Results (`test_boussinesq_velocity.py`, 5/5; figure
`figures/fig9_spike1_stepA_velocity.png`):

| Check | Result |
|---|---|
| `φ`, `u`, `v` vs analytic (rel L∞, robin far-field) | `2.4e-5`, `5.8e-5`, `6.2e-5` |
| Radial convergence order (`n_r` = 100→1600) | **2.00** (monotone) |
| `u_x(0)` origin read | **−2.0008** (target −2, tol 1e-3) |
| Angular DST-I transform | exact round-trip + mode isolation |

The convergence panel is the key honesty check: the error is not a lucky single-grid hit,
it is a clean second-order line, so the operator is *converging to the right answer*.

---

## 5. Honest scope

This validates the crux 2D operator; it is **not** a blow-up, a profile, or a proof. Step
A reproduces a manufactured answer — machinery validation, by construction. Steps B (the
rescaled RHS + modulation ODEs) and C (relaxing to the Chen–Hou profile — the actual gate)
are still ahead, and even a flawless Step C reproduces a *proven, published* 2D-Boussinesq
result across Wall C (2D Boussinesq ≠ 3D NS). Reproduction validates our machinery; it is
not novel and not a proof. See [../PHASE2_SPIKE1_NOTES.md](../../PHASE2_SPIKE1_NOTES.md) §4.

---

## 6. References

- [CH22a-I] J. Chen, T. Y. Hou, *Stable nearly self-similar blowup of the 2D Boussinesq and
  3D Euler equations with smooth data I: Analysis*, arXiv:2210.07191. (`Papers/`)
- [CH25-MMS] J. Chen, T. Y. Hou, *… II: Rigorous Numerics*, Multiscale Model. Simul. 23(1)
  (2025) / arXiv:2305.05660. (`Papers/`)
- [CH22a] J. Chen, T. Y. Hou, *Finite time blowup of 2D Boussinesq and 3D Euler equations
  with C^{1,α} velocity and boundary*, arXiv:1910.00173.
