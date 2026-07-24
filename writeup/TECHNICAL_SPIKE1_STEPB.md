# Spike 1 Step B — the rescaled 2D Boussinesq solver (technical)

**Status (2026-07-25): ASSEMBLED + VALIDATED at the piece level. NOT yet shown to reproduce
the profile — that is Step C (the gate), in progress.** This note documents the machine:
the full dynamic-rescaling right-hand side for 2D Boussinesq in the Hou–Luo geometry, the
data-driven choice of evolved variables, and the piece-by-piece known-answer validation.
Evidence figure + committed data: `python writeup/spike1_stepB_evidence.py`
(`writeup/figures/fig10_spike1_stepB_rescaled.png`, `writeup/data/spike1_stepB_rescaled.json`).

## 1. What Step B builds

Step A built the velocity operator `u = ∇^⊥(−Δ)⁻¹ω` on the stretched quarter-plane grid.
Step B wires it into the full **rescaled** system whose steady state is a self-similar blow-up
profile (Chen–Hou, *Stable nearly self-similar blowup of the 2D Boussinesq and 3D Euler
equations with smooth data*, arXiv:2210.07191, eqs (2.10)/(2.28)):

```
ω_τ = −(c_l x + u)·∇ω + η + c_ω ω
η_τ = −(c_l x + u)·∇η + (2c_ω − u_x) η − v_x ξ
ξ_τ = −(c_l x + u)·∇ξ + (2c_ω + u_x) ξ − u_y η          (v_y = −u_x used)
c_l = 2 η_x(0)/ω_x(0),   c_ω = ½ c_l + u_x(0),   c_θ = c_l + 2 c_ω
```

with `u = ∇^⊥(−Δ)⁻¹ω` from Step A. The gate target is Chen–Hou's reported profile constants
(2.23): `c̄_l ≈ 3.006499`, `c̄_ω ≈ −1.029425`, `ū_x(0) ≈ −2.532674`, and the far-field
exponent `α = c̄_ω/c̄_l ≈ −0.3424` (`ω ∼ r^α`, `θ ∼ r^{1+2α}`).

## 2. Which variables to evolve — decided by experiment, not taste

The physical system is `(ω, θ)`, but the paper's numerics evolve the *derivatives*
`(ω, η=θ_x, ξ=θ_y)`. Why it matters: the whole scheme's stability rides on the modulation
origin reads `ω_x(0)`, `θ_xx(0)`, `u_x(0)` — and *how well those reads condition* depends on
the variable choice. The Spike-0 discipline says pointwise high-derivative origin reads are
noise amplifiers, so we settled the choice with a measurement
(`experiments/spike1_stepB_decide_formulation.py`):

- The angular bases follow from parity. `ω, η` are **odd in x** → they live in `{cosβ, cos3β,…}`
  (zero at the axis `β=π/2`, free at the wall `β=0`). `θ, ξ` are **even in x** → `{1, cos2β,…}`.
- Reading `θ_xx(0)` off **primitive θ** means an `r²`-curvature of two even modes — and the
  `cos2β` mode carries only `θ_xx − θ_yy`, contaminated by `θ_yy`; recovering `θ_xx` needs a
  second (constant-mode) read plus a `θ(0,0)` subtraction.
- Reading `θ_xx(0) = η_x(0)` off **η** is a single clean *linear* `r`-slope of `η`'s one odd
  `cosβ` mode — the same read class as `ω_x(0)` and the Step-A `u_x(0)=−2.0008`.

Measured (fig10 panel A): the η-slope read is **~2× more accurate at every resolution and
~2× more noise-robust** (mean read error under 10⁻³ grid-scale noise: 3.1% vs 6.3%). Primitive-θ
was ruled out. The user chose the **full 3-field** variant (keep the `v_x ξ` coupling, don't drop
it) so the steady state is *exactly* the Chen–Hou profile — a faithful gate.

## 3. The pieces, each validated against a manufactured known answer

Built de-risked, crux-piece-first (the Step-A discipline). `solver/boussinesq_rescaled.py`;
suites `test_boussinesq_transport.py` (5/5) and `test_boussinesq_rescaled.py` (7/7).

**Piece 1 — the 2D upwind transport `(c_l x+u)·∇f`.** On the log-radial × angular grid a
general advection decomposes as `s_ρ f_ρ + s_β f_β` with

```
s_ρ = c_l + (u cosβ + v sinβ)/r,      s_β = (v cosβ − u sinβ)/r,
```

upwinded independently in ρ and β by the signs of `s_ρ, s_β` using Spike-0's 3rd-order Shu
stencil, generalized to 2D. Manufactured advection (dilation + rotation): rel L∞ **~9.5e-6**,
convergence **order ~2.98** (fig10 panel B), with exact structural checks (rigid rotation of a
radial field → 0; pure dilation → `f_ρ`). Crucially the **Spike-0 CFL cure carries to 2D**: as
`r→∞`, `s_ρ → c_l` (bounded outward dilation) and `s_β → 0`, so the timestep scales with `Δρ`
independent of the domain reach — the reason a stretched grid works where a uniform one dies.

**Piece 2 — the velocity-gradient fields `u_x, v_x, u_y`** (for the η/ξ reaction terms), via a
polar chain-rule gradient `grad_xy` with central finite differences (basis-agnostic, since
`u=−φ_y`, `v=φ_x` are not a pure sine/cosine series): rel L∞ **~3.9e-4**, order **~1.97**.

**Piece 3 — the origin slope read + modulation.** `g_x(0)` for an odd field is the linear
`r`-slope of its `cosβ` mode. The design payoff (fig10 panel C): `c_l = 2η_x(0)/ω_x(0)` is a
**ratio of two same-basis slope reads, so the projection quadrature bias cancels** — `c_l` is
recovered to **~3e-16** even though each slope alone carries ~2e-5. The quantity the scheme's
stability most depends on is the best-conditioned quantity in it.

**Piece 4 — the coupled SSPRK3 integrator** (`RescaledBoussinesq`). The RHS wiring (signs,
coefficients, which field enters each reaction term) is locked by a term-by-term re-assembly
test against the separately-validated sub-operators; the machine steps end-to-end with a
per-step advective-CFL `dt` and stays finite.

## 4. Honest scope

This is the **machine**, validated to run. It is *not* yet shown to reproduce the Chen–Hou
profile — that is **Step C** (the gate). Preliminary Step-C relaxation (exploratory) shows the
gauge-**invariant** far-field exponent settling near `α ≈ −0.34` (matching Chen–Hou) while the
individual gauge parameters `c_l, c_ω` drift and the residual plateaus around 3e-2 — i.e. the
*shape* looks right but the run does **not** cleanly converge to steady, a drift to be
diagnosed before any gate claim. And the standing caveat holds regardless of outcome: a flawless
Step C reproduces a **proven** result (Chen–Hou 2022) across Wall C — it validates our
machinery, it is **not novel and not a proof**. Overall Clay odds remain ~0.05%; the lottery
ticket lives past this solver, in profile construction.

## 5. Reproduce

```
python test_boussinesq_transport.py          # piece 1        (5/5)
python test_boussinesq_rescaled.py           # pieces 2–4     (7/7)
python experiments/spike1_stepB_decide_formulation.py   # the formulation decision experiment
python writeup/spike1_stepB_evidence.py --generate       # rebuild committed data + figure
```
