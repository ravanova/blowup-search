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
(the Spike-1 gate values): `c̄_l/c̄_ω ≈ −2.92`  ⟺  `α = c̄_ω/c̄_l ≈ −0.34 ≈ −1/3`, with
`c̄_ω < 0`, `c̄_l > 0`. `α`, the angular profiles `g₁,g₂`, and the profile shape are what we
match. The slow `r^{−1/3}` decay is the analogue of Spike-0's `1/X` whole-line tail: it is
exactly why a uniform/periodic grid fails and a stretched grid + far-field handling is
mandatory.

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
