# TECHNICAL — Route-VORT v1: the Leray obstruction is a velocity-formulation artifact

*Leg 332, cycle 7b, route 2. Blog sibling:
[BLOG_P2_ROUTEVORT_V1.md](BLOG_P2_ROUTEVORT_V1.md). Figure: `fig86`. Data:
`writeup/data/p2_route_vort_v1.json`. Runner: `experiments/p2_route_vort_v1.py`.
Full journal: `experiments/journal/leg_332.md`.*

**Result. The Leray-type obstruction that legs 257/261 derived in the velocity
formulation on Breden-Chu's Gaussian-weight space does NOT survive re-derivation
in the vorticity formulation on the same space, with the velocity reconstructed
by Biot-Savart. The step that fails is S4. It fails because the entire
non-vanishing tail sits inside the pressure gradient, and `curl ∘ grad ≡ 0`.**

No ban is touched. No certificate is built. No link of the L1→L4 chain moves.
Clay odds unchanged at ~0.05%.

---

## 1. Setting

Breden-Chu's space (arXiv:2404.04054v2, Definition 5): `H²(μ)` with

```
μ(x) = Γ(d/2) (2√π)^{-d} e^{|x|²/4},     Z := (2√π)^d / Γ(d/2) = 16π   (d = 3)
L := −Δ − (x/2)·∇
```

Leg 257's obstruction, in six steps:

* **S1** `U = curl(e^{−|x|²} e₃)` is divergence-free and Gaussian, so `U ∈ H²(μ)`.
* **S2** `P[F] = F − grad v` with `Δv = div F`, `F := (U·∇)U`.
* **S3** the multipole tail of `v` is set by the lowest non-vanishing moment of
  `div F`; monopole and dipole vanish, the quadrupole does not.
* **S4** hence `|grad v| ~ C r^{−4}` with `C ∝ T = ∫|U|² > 0`, so the coefficient
  **cannot** vanish.
* **S5** `∫_{|x|>R} r^{−8} e^{r²/4} r² dr = +∞`.
* **S6** therefore `P[(U·∇)U] ∉ L²(μ)`: the nonlinearity is not a map
  `H²(μ) → L²(μ)`, and `F(U) = U − L^{-1}P(…)` is not well-defined.

The gate asks whether this survives when the same argument is re-derived on the
space the *vorticity* lives in, with the velocity **reconstructed** rather than
assumed — because Biot-Savart lands outside the Gaussian-weight space.

## 2. Method — closed form throughout, no 3D convolution

Every field here is a Gaussian times a polynomial, which makes an exact and
**independent** route to leg 257's numbers. Leg 257 used a 216 000-node tensor
quadrature; leg 261 used the same machinery. This leg shares no code with either.

**Witness A** (leg 257's own field, as a velocity), all verified against
8th-order finite differences at generic off-axis points:

```
U      = 2E(−x₂, x₁, 0),                          E := e^{−r²}
ω_A    = curl U = (4x₁x₃E, 4x₂x₃E, 4E(1 − x₁² − x₂²))
F_A    = (U·∇)U = −4E²(x₁, x₂, 0)
div F_A = 8(2x₁² + 2x₂² − 1)E²                    [matches leg 261 exactly]
G_A    = curl F_A = 16x₃(−x₂, x₁, 0)E²            [purely Gaussian]
```

**The Leray potential, exactly.** Using `x₁²+x₂² = (2/3)r²(1 − P₂(cos θ))`, the
source splits into two spherical harmonics only:

```
S₀(r) = 8[(4/3)r² − 1] e^{−2r²},      S₂(r) = −(32/3) r² e^{−2r²}
v_l(r)  = −1/(2l+1) [ r^{−(l+1)} A_l(r) + r^l B_l(r) ]
v_l'(r) = −1/(2l+1) [ −(l+1) r^{−(l+2)} A_l(r) + l r^{l−1} B_l(r) ]
A_l(r) = ∫₀^r s^{l+2} S_l ds,        B_l(r) = ∫_r^∞ s^{1−l} S_l ds
```

(the two quadrature terms cancel exactly in the derivative). Verified against a
finite-difference Laplacian of the reconstruction: residual **8.909e−07**.

**Witness B** (the same field as a *vorticity*, velocity reconstructed):

```
ω_B := U,    u_B := BS(ω_B) = curl A,   A = a(r)(x₂, −x₁, 0)
a'' + 4a'/r = 2e^{−r²}   ⟹   a'(r) = 2G₄(r)/r⁴,  G₄(r) = ∫₀^r s⁴e^{−s²} ds
a(r) = −[ 2G₄(r)/(3r³) + (1/3)e^{−r²} ]           [by parts; NO quadrature]
u₁ = x₁x₃a'/r,  u₂ = x₂x₃a'/r,  u₃ = −2a − (a'/r)(x₁²+x₂²)
```

Checked: `div u_B` = 1.110e−16, `curl u_B − ω_B` = 3.331e−16, analytic Jacobian
vs FD = 6.356e−11, `l=1` ODE residual ≤ 1.409e−18, `a(0) = −1/3` exact,
`a(r) → −(√π/4)r^{−3}` to 0.000e+00 at r=20.

**Norms.** Gauss-Legendre in `r × cos θ × φ`. No axisymmetry assumed anywhere —
deliberately, since leg 261 caught itself measuring class C4 on the `e₃` axis
where the witness `ω` vanishes identically.

**Dependencies.** The repo venv carries numpy and matplotlib only — no scipy.
Every special function and quadrature is built in the runner and checked against
an independently known closed form before use (`G4` vs composite Gauss-Legendre,
relative ≤ 1.6e−15 across the series/asymptotic branch crossover at r = 0.6).

## 3. FT1 — leg 257 reproduced to 12 digits

| `r` | this leg | leg 257 | rel. diff |
|---|---|---|---|
| 10 | 3.1332853432887914e−04 | 3.1332853433e−04 | 3.577e−12 |
| 20 | 3.9166066791115055e−05 | 3.9166066791e−05 | 2.938e−12 |
| 40 | 4.895758348891509e−06 | 4.8957583489e−06 | 1.734e−12 |
| 80 | 6.11969793612502e−07 | 6.1196979361e−07 | 4.088e−12 |

Fitted exponent **−2.999999999998944**.

**The coefficient identity, closed form rather than fit.** With
`Q_kl := ∫ y_k y_l div F` and `div U = 0`, integration by parts gives
`∫ y_k F_l = −∫ U_k U_l`, hence `Q_kl = 2∫U_k U_l` (residual **3.342e−14**).
Since `U₃ ≡ 0`, `Q₃₃ = 0`, so `3Q₃₃ − tr Q = −2T` and the on-axis coefficient is
`T/4π` exactly:

* measured `v(80)·80³` = 0.313328534329601
* `T/4π` = 0.3133285343288751 → relative residual **2.317e−12**
* `T = ∫|U|² = π√(π/2)` = 3.9374024864306048; vs leg 257 1.168e−13, vs leg 261
  1.470e−13
* monopole of the source: **−1.134e−16** (vanishes identically — this is *why*
  the tail is `r^{−4}`, and it is checked, not assumed)

Leg 257's S1–S4 are therefore **correct**, and this leg independently confirms
them. The question is only whether they survive the change of formulation.

## 4. FT2 — the killing step

`P F = F − grad v`, so

```
curl P[F] = curl F − curl grad v = curl F
```

exactly, since `curl ∘ grad ≡ 0`. Leg 257's entire algebraic tail lies in
`ker(curl)`. The vorticity formulation constructs no Leray projector at all:
taking the curl of the momentum equation removes the pressure *before* any
projection is needed.

As a field identity at generic off-axis points, for divergence-free `u`:

```
curl[(u·∇)u] = (u·∇)ω − (ω·∇)u        residual 1.652e−10
```

**Defects this check caught** (recorded because they were caught by tests, not by
reading): the first version had this sign backwards — residual **2.895**, i.e.
*twice the term*, the signature of a sign flip. A second check caught a missing
Gaussian-derivative term in the stripped gradient at residual **3.089e−1**.

## 5. FT5 — two arms, one code path

`log₁₀` of the weighted radial density `e^{r²/4} r² ∫_{S²}|f|² dΩ / Z`. One
function, five fields; only the field varies.

| field | r=5 | r=10 | r=20 | r=40 | r=80 |
|---|---|---|---|---|---|
| C1 `P[(U·∇)U]` velocity | −2.61 | 3.72 | 34.49 | 162.97 | **+682.32** |
| B `u = BS(ω_B)` reconstructed velocity | −1.09 | 5.85 | 37.22 | 166.30 | **+686.25** |
| C0 `(U·∇)U` unprojected control | −37.49 | −158.43 | −645.81 | −2598.93 | **−10415.03** |
| C4 `curl[(U·∇)U]` vorticity | −35.59 | −155.93 | −642.70 | −2595.22 | **−10410.72** |
| B `(u·∇)ω − (ω·∇)u` vorticity, reconstructed | −19.38 | −76.38 | −304.38 | −1216.40 | **−4864.48** |

C1's `+682.32` reproduces leg 261's banked `+683.4` (leg 261 measured on a ray;
this leg integrates the sphere). C0 and C4 nearly coincide in the plot — that
overlap is real content, not a plotting artifact: the *unprojected* velocity
nonlinearity and the vorticity nonlinearity are both Gaussian, and it is the
projector alone that ruins the velocity arm.

**Instrument note.** At `r = 80` a Gaussian field is `e^{−12800}` (underflows to
exactly 0) while the weight is `e^{1600}` (overflows). The product is finite and
meaningful and neither factor is representable. A first version reported the
convergent arms as `−inf` — a floor, not a measurement. Each Gaussian-carrying
field is therefore also written as `unit(x)·exp(logpref(r))` with `unit`
polynomial, the density assembled in logs, and each pair checked against direct
evaluation where the direct one is valid (0.0, 0.0, 7.077e−17).

## 6. FT3 — converged norms over ℝ³

Refinement ladder `(R, n_r, n_c, n_φ) = (8,200,32,8) → (10,300,48,16) → (12,400,64,24)`:

| quantity | value | evidence |
|---|---|---|
| `‖G_A‖²_{L²(μ)}` | 0.13885306999296618 | closed form `(128/Z)(π/a)^{3/2}/a²`, `a = 15/4`; agrees to **2.359e−14** |
| `‖G_A‖_{L²(μ)}` | **0.3726299370594946** | |
| `‖G_B‖_{L²(μ)}` | **0.10136469652649564** | ladder change **1.722e−14** |
| `‖ω_A‖_{L²(μ)}` | 0.7180717835721682 | |
| `‖ω_B‖_{L²(μ)}` | 0.33071958297286563 | |

The exponent `a = 4 − 1/4 = 15/4` — field `e^{−4r²}` against weight `e^{+r²/4}`
— is the entire reason the vorticity arm converges.

## 7. The positive content — a finite mapping bound

```
‖(u·∇)ω − (ω·∇)u‖_{L²(μ)}  ≤  ‖∇u‖_∞ ‖ω‖_{L²(μ)}  +  ‖u‖_∞ ‖∇ω‖_{L²(μ)}
```

| | `‖u‖_∞` | `‖∇u‖_∞` | `‖ω‖_{L²(μ)}` | `‖∇ω‖_{L²(μ)}` | bound | actual | ratio |
|---|---|---|---|---|---|---|---|
| A | 0.857463504 | 2.828427091 | 0.718071784 | 1.936495591 | **3.691487980** | **0.372629937** | 0.10094 |
| B | 0.666666662 | 0.688598396 | 0.330719583 | 0.755191901 | **0.731194238** | **0.101364697** | 0.13863 |

Both ratios lie strictly in `(0,1)`: the bound holds and is not vacuous. Every
term of the vorticity nonlinearity carries a factor of `ω` or `∇ω`, which is
Gaussian; `u` and `∇u` need only be *bounded*, and they are. In the velocity
formulation the projector's output stands alone with nothing to multiply it down.
This is leg 261's discriminator, here as the derivation.

## 8. The audit

| step | carries over? | magnitude |
|---|---|---|
| S1 | **YES** | `div U` 3.886e−11; `‖ω_A‖_{L²(μ)}` = 0.718072 |
| S2 | **VACUOUS** | no Leray projector in the vorticity formulation |
| S3 | **YES, still true** | monopole −1.134e−16; quadrupole 3.342e−14; `Q₃₃ = 0` |
| **S4** | **NO — FAILS HERE** | exponent −2.999999999999, coefficient = `T/4π` to 2.317e−12 — and `curl` of that term is exactly 0 |
| S5 | YES velocity / **VACUOUS** vorticity | 3.72 → 682.32 vs −155.93 → −10410.72, same code path |
| S6 | **NO** | it *is* such a map: bound 0.731194, ratio 0.1386 |

**The coefficient is non-vanishing precisely because it equals the energy, and it
is carried precisely by the pressure gradient.** The feature that makes the
obstruction unavoidable in the velocity formulation is the feature that makes it
invisible in the vorticity formulation.

## 9. Where the route lands next — the replacement wall

`∫ω = 0` for any decaying divergence-free field
(`∫ω₃ = ∫ω·∇x₃ = −∫x₃ div ω = 0`), so Biot-Savart's `|x|^{−2}` term is killed and

* fitted decay exponent of `|u_B|` on a generic off-axis ray:
  **−3.0000000000000027** (matching leg 261's class C3 exponent −3.0000)
* `‖u_B‖_{L³(ℝ³)}` = **0.7307683991070311**, converged to `R = 60`

`u ∈ L³(ℝ³)` is exactly the Nečas–Růžička–Šverák / Tsai hypothesis, which forces
`u ≡ 0` for backward-self-similar 3D Navier-Stokes. The vorticity formulation
buys admissibility into the space and hands the target straight to the ansatz
constraint that already binds the velocity form. Leg 261 recorded this
composition; here it carries a number.

This does **not** un-answer the gate: leg 257 stated its obstruction ansatz-free
("d=2 and d=3, self-similar or not"), and *that* obstruction does not carry over.
NRS/Tsai is a different obstruction with a different hypothesis, named here so
nobody reads "escape route" as "open road".

## 10. Rider — the weight is adapted to the FORWARD drift

Breden-Chu's `L = −Δ − (x/2)·∇` and Gallay's rescaled vorticity operator are the
**forward** self-similar generators, for which the growing weight `e^{+|x|²/4}` is
natural. A **backward** self-similar profile carries `+(y/2)·∇`. Both remain maps
`H²(μ) → L²(μ)`:

* `‖L_forward ω_A‖_{L²(μ)}` = **5.716528960333894**
* `‖L_backward ω_A‖_{L²(μ)}` = **6.041350443296389**
* Rayleigh quotients **7.2727** vs **6.4545**

So the drift sign flip moves the spectrum, not the mapping property — it does not
touch this leg's gate, but a later leg reaching for this space with a backward
ansatz will meet it.

## 11. Limits

* Two witnesses, not a theorem. The §7 bound is *derived* in general but
  *evaluated* on two fields; a general statement needs the Biot-Savart `L^∞`
  bound proved on all of `H²(μ)`.
* Full `H²(μ)`-norm closure (not just `L²(μ)` of `ω` and `∇ω`) is not checked.
* No claim that the vorticity formulation is *usable* for a computer-assisted
  proof on this space — separate leg, separate gate, and stage V's
  `ℓ¹`-Fourier/radii-polynomial ban still stands over it.

## 12. Reproduce

```
.venv/bin/python experiments/p2_route_vort_v1.py --self-test   # 33/33 liveness
.venv/bin/python experiments/p2_route_vort_v1.py               # JSON + fig86
```

Runtime 18.9 s. The gate's YES and INDETERMINATE branches are exercised on
synthetic input in `self_test`, so the NO is a measurement and not the only
reachable code path.
