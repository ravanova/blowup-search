# Phase 2 (technical) — From a uniform-grid wall to a dynamic-rescaling solver

### The numerics upgrade for Route A: decision, derivation, and the Spike-0 reconnaissance

*Technical companion to [NEGATIVE_RESULT_TWO_CURRENCIES.md](../2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md)
(which concluded the uniform-grid fitness search) and the planning records
[../PHASE2_NUMERICS_PLAN.md](../../PHASE2_NUMERICS_PLAN.md),
[../PHASE2_SPIKE0_NOTES.md](../../PHASE2_SPIKE0_NOTES.md). Status: this records the
**decision, derivation, and reconnaissance**. The solver has since been **built and
validated** — see the results companion
[TECHNICAL_SPIKE0_RESCALING.md](TECHNICAL_SPIKE0_RESCALING.md). References in
[§6](#6-references).*

---

## 1. Why a numerics upgrade, and why *this* one

Phase 1 concluded that on a **uniform grid** no scalar fitness read off the trusted,
pre-artifact window can isolate genuine singular structure: the near-singularity forms
below grid scale, so the fitness re-expresses through whatever *is* resolved (amplitude,
buoyancy split, formation time). Two independent currencies failed a pre-committed,
cheat-audited gate through the same degeneracy. The honest exit is not a third currency
but a solver that **resolves the singular region**, so a fitness measures real structure.

The field offers three numerical paradigms for exactly our models (Hou–Luo 2D Boussinesq
/ 3D axisymmetric Euler / the 1D CLM–De Gregorio family):

- **(P1) Dynamic (self-similar) rescaling.** Integrate the PDE in rescaled variables so a
  finite-time self-similar blow-up becomes a **steady profile** held resolved on a fixed
  grid as physical time approaches `T`. Classical, originating in the NLS focusing-singularity
  work of McLaughlin–Papanicolaou–Sulem–Sulem [MPSS86]; it is how Chen–Hou constructed the
  approximate self-similar profile underpinning their computer-assisted proof [CH22b].
- **(P2) Direct profile construction.** Solve the self-similar profile equation itself
  (Newton, or a physics-informed neural network). No time-integration, no resolution wall.
  This is the 2023–2026 frontier: the first smooth 2D-Boussinesq / 3D-Euler profiles
  [WLGB23], now pushed to *unstable* and *singular* profiles at machine precision [2511.22819].
- **(P3) Adaptive mesh refinement.** The original Luo–Hou 2014 discovery tool [LH14].
  General but heavy; strictly more work than P1 when the blow-up is self-similar.

**Decision (with the user, via a reviewed options menu): build P1, reject P3.** P1 reuses
the validated pseudo-spectral solver, dissolves the below-grid-scale wall, and its late-time
state *is* a self-similar profile — the de-risked on-ramp to P2. Honest caveat, surfaced by
the research and recorded for the record: the genuine *novelty* frontier is P2 profile
construction of unstable profiles, not evolutionary search over initial conditions; P1
mainly finds the *stable* blow-up, which for 2D Boussinesq Chen–Hou already proved [CH22a].
So P1 is framed as the shared substrate, with the "evolve-ICs vs hunt-profiles" question
re-decided at a gate *after* the solver works.

> **Terminology.** This is a Route-A **numerics** upgrade. It is *not* roadmap "Route D"
> (the later Tier-3 computer-assisted-proof leg). AMR-or-rescaling ≠ proof.

---

## 2. Spike-first, on a known answer

Per the project's build discipline — validate a new method on a substrate with a *known*
answer before porting it — Spike 0 implements dynamic rescaling in **1D on the gCLM solver**
(`solver/gclm.py`), where the self-similar blow-up is explicit, before Spike 1 ports it to
2D Boussinesq.

**Model.** gCLM: `ω_t + a u ω_x = ω u_x`, `u_x = H(ω)`, `a=0` is CLM [CLM85], `a=1` De
Gregorio [DG90]. CLM has the closed-form solution
`ω(x,t) = 4ω₀/((2 − t H ω₀)² + t² ω₀²)`, blowing up at `T* = 2 / max{Hω₀ : ω₀=0}`.

**Known-answer target (CLM, `a=0`).** Data `ω₀ = −sin x` → blow-up at `x=0`, `T*=2`, and
near the singularity `ω(x,t) ≈ (T−t)^{−1} Φ(x/(T−t))` with the explicit profile

```
Φ(η) = −4η / (1 + 4η²).
```

---

## 3. The rescaled formulation (derived, then confirmed against the literature)

Write `ω(x,t) = c_ω(τ) W(y,τ)`, `y = x/c_l(τ)`, `dτ/dt = c_ω`. The Hilbert transform is
scale-invariant (`H` commutes with dilation), so the rescaled gCLM equation is

```
W_τ = −β W + δ y W_y − a Ũ W_y + W·HW,     Ũ_y = HW,
β = d log c_ω/dτ,   δ = d log c_l/dτ.
```

For CLM (`a=0`) the advection term drops: `W_τ = −β W + δ y W_y + W·HW`. A self-similar
profile is a steady state. In the physical scaling `c_ω ~ 1/(T−t)`, `c_l ~ (T−t)`, i.e.
`β=1`, `δ=−1`.

This hand derivation was subsequently confirmed **identical** to the published gCLM
dynamic-rescaling scheme of Huang–Tong–Wang [HTW26] (convention `ω = C_ω^{−1}Ω`, `X=C_l x`):

```
Ω_τ + (c_l X + a U) Ω_X = (c_ω + U_X) Ω,     U_X = H(Ω),
U(X,τ) = (1/π) ∫_ℝ ln|(X−Y)/Y| Ω(Y,τ) dY.
```

with the normalization conditions (non-degenerate, `a=0`)

```
Condition 1 (fix slope Ω_X(0)):  c_l = c_ω + (1−a) U_X(0,τ)
Condition 2 (a=0):               c_ω = 1 − U_X(0,τ) = 1 − HΩ(0,τ)
  ⟹ for a=0:  c_l ≡ 1,   c_ω = 1 − HΩ(0),   and at the profile HΩ̄₀(0)=2 ⇒ c_ω → −1.
```

Exact CLM target in this convention: `Ω̄₀(X) = −4X/(1+4X²)`, `HΩ̄₀(X) = 2/(1+4X²)`. The
pair `Ω̄₀ ↔ 2/(1+4X²)` is a ready-made **unit test for the line Hilbert transform**.

---

## 4. Reconnaissance: three false starts, each a finding

Cheap probes (`../../phase2_spike0_probe.py`, and a scratch whole-line build) established,
before committing to the real solver:

| # | attempt | outcome | lesson |
|---|---|---|---|
| 1 | modulation via pointwise `W_yyy(0)` | `W_yyy(0)` reads ~1000 vs analytic 1 | high pointwise derivatives are noise amplifiers (`(ik)³`); use **integral** modulation |
| 2 | periodic pseudo-spectral rescaling | **stable but wrong profile** (`B≈−1`, not 4) | the true profile is a whole-line `~1/X` function; **periodic H ≠ line H** for slow tails |
| 3 | uniform whole-line grid, spectral | line-`H` ok (`~1/M` err); dilation **NaNs** | the `−c_l X Ω_X` term is **CFL-limited** (`dt < dX/M ≈ 1e-4`); a spectral filter did not help |

The unifying reading: the true CLM self-similar profile lives on the **whole line** and
decays only like `1/X`, and the self-similar dilation `X Ω_X` has an **unbounded advection
coefficient**. A periodic or uniform spectral discretization cannot carry either. This is
exactly why the published scheme uses a *stretched, non-uniform grid* and a *non-FFT*
Hilbert transform.

---

## 5. The build recipe (from [HTW26] Appendix C), and the remaining work

**C.1 — line Hilbert transform on a non-uniform grid (the crux).** Approximate `f` on
`[−M,M]` with `C¹₀` cubic-spline / Hermite basis functions `P_i, Q_i` chosen so their
Hilbert transforms are *bounded and closed-form*: `H(P_i)=A(l)−A(r)`,
`H(Q_i)=(x_{i-1}−x_i)B(l)−(x_{i+1}−x_i)B(r)`, with `A(s),B(s)` rational-plus-`ln|1−s|` and
Mathematica minimax series near `s=0` to avoid cancellation; diagonal terms
`H(P_i)(x_i)=(1/π)ln|(x_{i-1}−x_i)/(x_{i+1}−x_i)|`, `H(Q_i)(x_i)=(x_{i-1}−x_{i+1})/(3π)`.
The velocity `U` is the analytic integral of the same elements. This computes the *line*
`H` on an arbitrary grid — where FFT cannot go.

**Grid — stretched cosh/sinh.** `X(ρ) = X_m(1−cosh ρ) + √(c+X_m²) sinh ρ`, uniform `ρ`,
`Δρ=0.01`, truncated at `M=10¹⁰`, `X_m=argmax|Ω|`, `c` set so `N_bulk=600` points fall in
the half-max peak. **Key property:** `X ~ sinh ρ ⇒ dX ~ X·Δρ`, so the dilation CFL is
`dt < dX/X ~ Δρ`, **independent of `M`** — this is the cure for the uniform-grid death.

**C.2 — time-stepping.** Evolve `f = Ω/Xᵏ` (`k≥3` odd for degenerate profiles; `k=1` for the
non-degenerate CLM whose profile vanishes to order 1) to protect the origin vanishing;
advection via 5th-order **WENO** [JS96]; time via **SSPRK(10,4)** [GKS11]; converge at
`‖f_τ‖_∞ < 10⁻⁸`.

**Remaining work (a genuine multi-day solver build).** In dependency order:
1. `solver/line_hilbert.py` + `test_line_hilbert.py` — the C.1 spline-analytic transform,
   validated against `−4X/(1+4X²) ↔ 2/(1+4X²)`. The crux; self-contained; hard pass/fail.
2. the stretched grid + WENO/SSPRK time integration of the rescaled equation.
3. `test_gclm_rescaled.py` — the pre-committed CLM success predicate: `Ω → Ω̄₀`,
   `c_ω → −1`, reconstructed `T* → 2`, all resolution-stable.

For a POC (Spike 0, ~1% not machine precision) the stretched mesh can be fixed (no AMR) and
`M ~ 10²–10³`; the C.1 transform is essential regardless.

---

## 6. Honest scope

Even a flawless Spike-1 solver reproducing the Chen–Hou 2D-Boussinesq profile reproduces a
*proven, published* result in a toy model across "Wall C" (2D Boussinesq ≠ 3D Navier–Stokes;
Chen–Hou already proved 2D-Boussinesq boundary blow-up [CH22a]). Reproduction validates our
machinery; it is not novel and not a proof. Any genuine novelty is downstream (a new /
unstable profile, or one an IC-search surfaces that direct construction had not) and would
still require Route D to certify. Nothing here is a blow-up, a proof, or a statement about
the Millennium problem. The value is a structure-resolving solver — the enabler that lives
on the far side of the uniform-grid wall — and, so far, an honestly-documented reconnaissance
of what building it takes.

---

## 7. References

- [CLM85] P. Constantin, P. D. Lax, A. Majda, *A simple one-dimensional model for the
  three-dimensional vorticity equation*, Comm. Pure Appl. Math. 38 (1985).
- [DG90] S. De Gregorio, *On a one-dimensional model for the three-dimensional vorticity
  equation*, J. Stat. Phys. 59 (1990).
- [MPSS86] D. McLaughlin, G. Papanicolaou, C. Sulem, P. Sulem, *Focusing singularity of the
  cubic Schrödinger equation*, Phys. Rev. A 34 (1986) — dynamic-rescaling origin.
- [LH14] G. Luo, T. Y. Hou, *Potentially singular solutions of the 3D axisymmetric Euler
  equations*, PNAS 111 (2014) — adaptive-moving-mesh discovery.
- [E21] T. Elgindi, *Finite-time singularity formation for C^{1,α} solutions to the
  incompressible Euler equations on ℝ³*, Ann. of Math. 194 (2021).
- [CH22a] J. Chen, T. Y. Hou, *Finite time blowup of 2D Boussinesq and 3D Euler equations
  with C^{1,α} velocity and boundary*, arXiv:1910.00173.
- [CH22b] J. Chen, T. Y. Hou, *Stable nearly self-similar blowup of the 2D Boussinesq and
  3D Euler equations with smooth data* — Part I arXiv:2210.07191; Part II (Rigorous
  Numerics) arXiv:2305.05660.
- [WLGB23] Y. Wang, C.-Y. Lai, J. Gómez-Serrano, T. Buckmaster, *Asymptotic self-similar
  blow-up profile for 3D axisymmetric Euler equations using neural networks*, Phys. Rev.
  Lett. 130, 244002 (2023); arXiv:2201.06780.
- [2511.22819] *Resolving Sharp Gradients of Unstable Singularities to Machine Precision via
  Neural Networks* (2025).
- [HTW26] D. Huang, J. Tong, X. Wang, *Self-similar finite-time blowups with singular
  profiles of the generalized Constantin–Lax–Majda model: theoretical and numerical
  investigations*, arXiv:2603.25104 — **the exact scheme + Appendix C discretization used
  here**.
- [2308.01528] *Exact self-similar finite-time blowup of the Hou–Luo model with smooth
  profiles* (2023).
- [JS96] G.-S. Jiang, C.-W. Shu, *Efficient implementation of weighted ENO schemes*, J.
  Comput. Phys. 126 (1996) — WENO5 (cited as [JW99] in [HTW26]).
- [GKS11] S. Gottlieb, D. Ketcheson, C.-W. Shu, *Strong Stability Preserving Runge–Kutta and
  Multistep Time Discretizations*, World Scientific (2011) — SSPRK(10,4).
