# Phase 2 — Spike 1 notes (dynamic rescaling on 2D Boussinesq)

**Status: GROUNDED, build starting (2026-07-24).** The 2D Boussinesq dynamic-rescaling
formulation is now transcribed from the source papers (Chen–Hou Part I arXiv:2210.07191
§2, §7; Part II / MMS-Numerics-2025 §2). This doc locks the formulation, records the
honest scope decision (POC fidelity, *not* the full rigorous-numerics apparatus), and
pins the de-risked build order with a pre-committed validation predicate for the crux
piece (Step A, the velocity operator). Source PDFs live in `Papers/` (gitignored).

**Goal of Spike 1:** port the validated 1D dynamic-rescaling machinery (Spike 0) to 2D
Boussinesq in the Hou–Luo geometry and reproduce the *published Chen–Hou self-similar
profile* as the validation gate — qualitative profile shape + the scaling exponent in the
reported range. This reproduces a **proven** result (Chen–Hou 2022 proved 2D-Boussinesq
boundary blow-up): it validates our machinery across Wall C (2D Boussinesq ≠ 3D NS). It is
**not novel and not a proof.** (Novelty, if any, is the *post-Spike-1* gated decision.)

---

## 1. The grounded formulation (transcribed, with equation refs)

### Physical 2D Boussinesq — upper half-plane `ℝ²₊ = {y ≥ 0}`, singularity at the origin

Chen–Hou Part I (2.3)–(2.5) / MMS (2.3)–(2.5):

```
ω_t + u·∇ω = θ_x                          (vorticity; buoyancy forcing θ_x)
θ_t + u·∇θ = 0                            (density transport)
−Δφ = ω,   u = −φ_y,   v = φ_x,   φ(x,0) = 0   (Biot–Savart via stream function)
```

Symmetry class: **ω odd in x, θ even in x** (so θ_x is odd in x, matching ω's parity;
one checks the transport + buoyancy preserve these). With the wall `φ=0` at `y=0` and the
`x`-parity, the effective domain is the **first quadrant `[0,∞)²` with the singular corner
at the origin** — the Hou–Luo geometry. This is the analogue of Spike 0's odd-symmetry
whole-line reduction, now in 2D with a genuine boundary.

### Dynamic-rescaling formulation (one-scale) — MMS (2.10), (2.11)

`ω̃(x,τ) = C_ω(τ) ω(C_l(τ)x, t)`, `θ̃ = C_θ θ`, `ũ = C_ω C_l⁻¹ u`, with `dt/dτ = C_ω`.
Rescaled system (dropping tildes, `x = (x,y)`):

```
ω_τ + (c_l x + u)·∇ω = θ_x + c_ω ω
θ_τ + (c_l x + u)·∇θ = c_θ θ,        c_θ = c_l + 2 c_ω           (MMS 2.9)
u = ∇^⊥(−Δ)⁻¹ ω  =  (−φ_y, φ_x),   −Δφ = ω,   φ|_{y=0}=0
```

**Modulation / normalization (MMS 2.11)** — pins the origin slopes `ω_x(0)`, `θ_xx(0)`:

```
c_l = 2 θ_xx(0,τ) / ω_x(0,τ)
c_ω = ½ c_l + u_x(0,τ)                 (u_x(0) = ∂_x u at the origin)
c_θ = c_l + 2 c_ω
```

A self-similar profile is a **steady state** of this system. Note this smooth-data scheme
is **ONE-SCALE** (a single isotropic length factor `c_l`). The "two-scale" variant in the
planning notes was from Chen–Hou's *earlier* C^{1,α}-boundary work, not this profile — so
the Spike-0 headline (one-scale can be stable/attracting) is the relevant precedent, and
we start one-scale. (If a scaling instability appears, revisit — cf. Spike-0 discipline.)

### Far-field asymptotics — Part I (7.1) (the crux difficulty, and its lever)

```
ω(r,β) ~ g₁(β) r^α,   θ(r,β) ~ g₂(β) r^{1+2α},   α = c_ω / c_l < 0,  α ≈ −1/3
```

i.e. the profile decays only like `r^{−1/3}` on a huge domain. **Known-answer target**
(the Spike-1 gate values). Part I (2.23) reports these to high precision — use them, not the
round `−2.92`/`−1/3` shorthand:

```
c̄_l ≈ 3.00649898,   c̄_ω ≈ −1.02942516,   ū_x(0) ≈ −2.532674,   v̄_x(0) = 0
c̄_l/c̄_ω ≈ −2.9205600,   α = c̄_ω/c̄_l ≈ −0.342407
```

`α`, the angular profiles `g₁,g₂`, and the profile shape are what we match (POC tol ~1–5%,
resolution-stable). The slow `r^{−1/3}` decay is the analogue of Spike-0's `1/X` whole-line
tail: exactly why a uniform/periodic grid fails and a stretched grid + far-field handling is
mandatory. Advection is **outward & anisotropic** (2.23/2.24): near the origin
`c̄_l x + ū ≈ 0.47 x`, `c̄_l y + v̄ ≈ 5.54 y`, and `|ω_y| < 0.23|ω_x|`, `|θ_y| < 0.16|θ_x|`.

---

## 2. What the paper's apparatus is — and the honest POC scope

Chen–Hou's *full* method (Part I §7, Part II Appendix C) is a serious expert-numerics
program, most of which exists for the **computer-assisted proof**, not for merely obtaining
the profile:

- semi-analytic / numerical **split** `ω̄ = ω̄₁ + ω̄₂`: an analytic far-field part
  `χ(r) r^α g(β)` capturing the `r^{−1/3}` tail + a fast-decaying compactly-supported
  numerical remainder (to dodge round-off on a `10¹³`–`10¹⁵`-sized domain);
- **piecewise 6th–8th-order B-spline** representation, adaptive mesh (`h ≤ 1/256` near 0);
- **B-spline finite-element** Poisson solve for `−Δφ = ω` with a weight `ρ_p(y)` enforcing
  `φ(x,0)=0`; angular ODE `(−∂_β² −(2+α)²)f = g₁` for the far-field stream function;
- 2nd-order Runge–Kutta in `τ`; residual driven to `~10⁻⁷`; rigorous `C³` interval bounds
  (INTLAB) for the proof.

Reproducing all of that to `10⁻⁷` + interval rigor is a **months-scale expert build and is
not the Spike-1 goal.** The plan pre-committed Spike 1 to *qualitative* fidelity
(`PHASE2_NUMERICS_PLAN.md` §3: "qualitative shape + exponent in the reported range").

**POC-fidelity scope (this Spike):**
- moderate domain and precision (target ~1–5%, resolution-stable — *not* `10⁻⁷`, no
  interval arithmetic, no proof);
- a **tractable, validated** Poisson discretization in place of B-spline FEM (see Step A) —
  the elliptic solve is *textbook*, so validating it against a manufactured known answer is
  legitimate engineering (contrast the 1D line-Hilbert, an exotic singular integral that
  *had* to be transcribed/derived from the paper);
- the same *mathematical* formulation (§1) is kept exactly: eqs (2.10), modulation (2.11),
  half-plane BC, `r^α` far-field.
- success = reproduce the profile shape + `α ≈ −1/3` / `c_l/c_ω ≈ −2.92`, resolution-stable.

> Decision recorded (mine, POC-level, flagged for the user): use an **angular-spectral +
> radial** Poisson solve, not B-spline FEM. Rationale below (Step A). Reversible.

---

## 3. Build order (de-risked: crux piece first, validated standalone)

The user chose Spike 1, **de-risked** — build + validate the highest-risk new piece (the 2D
velocity operator) as a standalone unit against a known answer *before* wiring the full
rescaled solver. Order:

**Step A — the 2D velocity operator `u = ∇^⊥(−Δ)⁻¹ω` on the stretched grid (THE CRUX).**
The FFT did this on the uniform grid; it *cannot* on the stretched grid — this is the 2D
analogue of Spike-0's non-FFT line-Hilbert. Plan:
- coords: polar-ish `(ρ, β)`, `β ∈ [0, π/2]`, radial stretch `r = r(ρ)` (sinh/exp map, so
  `dr ~ r·Δρ` — the Spike-0 CFL cure, and it lands points across many decades of `r`);
- angular treatment: expand in the Dirichlet angular basis on `[0,π/2]` (`f(0)=f(π/2)=0`
  from `φ=0` on the wall + odd-x symmetry). `−Δ` becomes, per angular mode `m`, a **radial
  ODE** `(∂_rr + r⁻¹∂_r − λ_m r⁻²)φ_m = −ω_m` → a tridiagonal solve per mode (no scipy
  sparse needed; mirrors the paper's own angular ODE (7.6) for the far field);
- far field: match to the homogeneous `r^{+√λ_m}`/`r^{−√λ_m}` radial solutions so the slow
  `r^{−1/3}` tail is handled instead of chopped (POC-level: a truncation + analytic tail,
  not the full semi-analytic split).
- recover `u = −φ_y`, `v = φ_x` via the same basis derivatives.

**Step A PRE-COMMITTED VALIDATION PREDICATE (hard pass/fail, before trusting anything):**
Manufactured known solution — pick an analytic `φ*(x,y)` that (i) vanishes on `y=0`,
(ii) gives `ω* = −Δφ*` **odd in x** and decaying, (iii) has closed-form `u* = −φ*_y`,
`v* = φ*_x`. Feed `ω*` to the operator; require:
1. recovered `φ, u, v` match `φ*, u*, v*` in **relative L∞** to a stated tol
   (target `< 1e-3` at moderate resolution), AND
2. the error **decreases under grid refinement** at the expected order (convergence, not a
   lucky single-grid hit), AND
3. `u_x(0)` (the quantity the modulation (2.11) reads) matches its analytic value to
   `< 1e-3` — because the whole solver's stability hinges on that origin read (Spike-0
   lesson: pointwise origin reads are noise-sensitive; verify this one explicitly).
Written as `test_boussinesq_velocity.py`, added to the suite. Step A does **not** proceed
to Step B until this passes and is resolution-stable.

**Step B — the rescaled RHS + modulation.** Assemble (2.10): transport `(c_l x + u)·∇`
(upwind/WENO-lite, per Spike 0), buoyancy `θ_x`, reaction `c_ω ω`/`c_θ θ`; modulation
(2.11) from the origin slopes; SSPRK time stepping in `τ`. Validate pieces incrementally.

**Step B PIECE 1 DONE + VALIDATED (2026-07-24):** the 2D upwind transport operator
`(c_l x+u)·∇f` on the log-polar grid. Decomposes as `s_ρ f_ρ + s_β f_β` with
`s_ρ = c_l + (u cosβ + v sinβ)/r`, `s_β = (v cosβ − u sinβ)/r`, upwinded independently in ρ,β
by the Spike-0 3rd-order Shu stencil (generalized to 2D). `solver/boussinesq_rescaled.py`,
`test_boussinesq_transport.py` (5/5): manufactured advection rel err ~9.5e-6, convergence
order ~2.98, structural checks exact (rigid-rotation→0, dilation→f_ρ), far-field CFL cure
carries to 2D (`s_ρ→c_l`, `s_β→0`).

**Step B FORMULATION DECIDED (2026-07-24): evolve the 3-field system `(ω, η=θ_x, ξ=θ_y)`**
— the paper's own numerics variables (Part I (2.27)–(2.28)), NOT primitive `(ω,θ)`.
*Why (decision experiment `experiments/spike1_stepB_decide_formulation.py`, user-requested):* the crux is
the modulation origin reads. `θ_xx(0)` read off primitive `θ` is an `r²`-curvature of two
even modes, contaminated by `θ_yy` (the `cos2β` mode carries only `θ_xx−θ_yy`) — measured
**~2× worse and ~2× more noise-sensitive** than reading `θ_xx(0)=η_x(0)` as a clean *linear*
`r`-slope of `η`'s single odd `cosβ` mode (same read class as ω_x(0), Step-A `u_x(0)`). The
user chose the **full 3-field** variant (keep `ξ`, don't drop the `v_x ξ` coupling) so the
steady state is *exactly* the Chen–Hou profile — a faithful, honest gate.

*Angular structure (settles the bases — the sine basis was only for `φ`):* `ω, η` are **odd
in x** → live in `{cosβ, cos3β,…}` (zero at axis `β=π/2`, free at wall `β=0`); `θ, ξ=θ_y` are
**even in x** → `{1, cos2β, cos4β,…}` (Neumann at axis, free at wall). Transport uses β
finite differences (basis-agnostic — already built). Origin reads project onto the leading
mode and extrapolate in `r`.

*The derived rescaled RHS (one-scale, nonlinear; `u_x+v_y=0` used for the ξ reaction):*
```
ω_τ = −(c_l x+u)·∇ω + η + c_ω ω
η_τ = −(c_l x+u)·∇η + (2c_ω − u_x) η − v_x ξ
ξ_τ = −(c_l x+u)·∇ξ + (2c_ω + u_x) ξ − u_y η
c_l = 2 η_x(0)/ω_x(0),   c_ω = ½ c_l + u_x(0),   c_θ = c_l + 2 c_ω
```
Needs velocity-gradient FIELDS `u_x, v_x, u_y` (from differentiating the Step-A velocity) in
the reaction terms — build+validate those next (piece 2), then origin reads (piece 3), then
assemble RHS + SSPRK3 (piece 4). `v_x(0)=0` (2.23) is a free sanity check on the reads.

**STEP B COMPLETE + VALIDATED (2026-07-24).** `solver/boussinesq_rescaled.py`; suites
`test_boussinesq_transport.py` (5/5) + `test_boussinesq_rescaled.py` (7/7). All sub-operators
validated vs manufactured answers, all convergent:
- piece 2 `grad_xy` (velocity-gradient fields): rel err ~3.9e-4, order ~1.97.
- piece 3 `odd_field_x_slope` (origin slopes ω_x(0), η_x(0)): recovers −2.1 to ~2e-5; and
  `c_l = 2η_x(0)/ω_x(0)` recovered to ~3e-16 — the projection quadrature bias **cancels in the
  ratio** (the design win); `modulation` (2.11) assembles correctly with `u_x(0)`.
- piece 4 `RescaledBoussinesq.rhs/step/run`: SSPRK3 coupled integrator; RHS wiring locked by a
  term-by-term re-assembly test; end-to-end **runs stably** (60 steps, finite c_l,c_ω, res↓).

Angular parities (recorded, used in seeds/tests): `φ` odd-x ⇒ `u=−φ_y` **odd-x**, `v=φ_x`
**even-x**; hence `u_x` even, `u_y` odd, `v_x` odd — every RHS term is parity-consistent
(ω,η odd; ξ even). Honest status: the machine is BUILT and stable; whether its steady state IS
the Chen–Hou profile is **Step C** (unproven until run).

**Step C — reproduce the Chen–Hou profile (the gate).** Relax perturbed data to the steady
profile; check shape + `α ≈ −1/3` / `c_l/c_ω ≈ −2.92`, resolution-stable. Pre-committed
predicate written before the logged run.

**Then (post-Spike-1 gated decision):** stable-vs-singular target, and evolve-ICs vs
hunt-profiles (P2) — decided with the working machine, per the standing plan. The
stable-vs-singular fork the user raised is deferred to here (both share Steps A–B).

---

## 4. Honest framing to preserve

2D Boussinesq is a toy model, not 3D NS. A flawless Spike-1 solver reproduces a *proven,
published* profile across Wall C — validates machinery, not novel, not a proof. Overall
Clay odds ~0.05%. The lottery ticket lives on the far side of this solver and, per the
banked catch, probably in profile construction (P2) more than GA-over-ICs. The POC
simplifications above (moderate domain/precision, angular-spectral Poisson) are *scoped
down from* the paper deliberately and disclosed; they do not change the mathematics being
solved.
