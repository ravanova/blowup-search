# Leg 420 — unit `U4` PRE-REGISTRATION (`INSTANTIATE`)

**COMMITTED BEFORE THE RUNNER EXISTS AND BEFORE ANY NUMBER IS PRODUCED.** The arc-6 charter is
explicit: *"Pre-commit the exponent and the tolerance BEFORE running. Widening a tolerance after
seeing the number is the failure mode this repository has caught in itself before — record the
temptation if you feel it, as leg 408 did."*

Everything below is fixed. If any of it changes after a number exists, the change is a
`CORRECTIONS.md` entry naming what was changed and why, not a quiet edit.

---

## 1. WHAT IS INSTANTIATED

A concrete axisymmetric velocity–pressure pair carrying **the manuscript's scalings** —
`u_θ ≍ q^{-A}`, `u_z ≍ q^{-A}`, `u_r = O(q^{-1/2})`, `ℓ_r = q^{1/2}`, `ℓ_z = q^{D}`,
`A = 1/2 + h`, `D = 1/2 − h`, `h = 1/100` — built so that **incompressibility is exact by
construction**, not enforced afterwards:

```
u = curl( (S/r) e_θ ) + B e_θ        ⟹  u_r = −(1/r)∂_z S,  u_z = (1/r)∂_r S,  u_θ = B
```

`S` is a Stokes streamfunction and `B` the azimuthal coefficient, both given in closed form
through the similarity variables `q(z,τ)`, `X = r²/2q`, `η = z/q^D`, with `q` the unique positive
root of `q − z²q^{2h} = τ` (Newton, to machine precision). The pressure is set by the leading
radial balance `∂_r p = u_θ²/r`, i.e. `p = q^{-2A}Π(X,η)` with `Π = −∫_X^∞ E²/(2x) dx`.

**THIS IS NOT THE MANUSCRIPT'S PROFILE AND IS NOT CLAIMED TO BE.** The manuscript's `(E, U, Π)`
are the output of Sections 4, A, B and C — a joined inner/exterior solution satisfying five radial
moment identities and an admissible-stress-cone condition. **None of that is reproduced here.**
What is instantiated is an object with **the manuscript's scaling structure and its exact
incompressibility**, which is what a *scaling* measurement needs and all it needs.

## 2. WHAT IS MEASURED

The **tangential momentum residual** of the instantiated pair, in cylindrical axisymmetric form at
viscosity one:

```
R_θ = ∂_t u_θ + u_r ∂_r u_θ + u_z ∂_z u_θ + u_r u_θ / r − [Δu_θ − u_θ/r²]
R_z = ∂_t u_z + u_r ∂_r u_z + u_z ∂_z u_z + ∂_z p − Δu_z
```

**The reported quantity is** `M(τ) = max over a FIXED similarity grid of |R_θ|`, the grid being
`X ∈ [0.05, 1.0]` × `η ∈ [−0.5, 0.5]`, 25 × 11 points, **the same similarity points at every
`τ`** — so `M(τ)` is exactly `q^{e}·max|C(X,η)|` up to the subleading corrections, and its slope
is the exponent.

**τ ladder:** `τ_k = 10^{−4−k}`, `k = 0 … 4`, five points spanning four decades.

**Fit:** ordinary least squares of `log₁₀ M` against `log₁₀ τ`. The slope is the measured exponent.

## 3. THE PRE-COMMITTED EXPONENT

The ledger of `solver/arc6_residual_ledger.py` (leg 419, landed) gives the leading tangential
residual as `q^{-3/2-h}`, and the same value arises three ways, which is the balance the
construction runs on:

| term | scale |
|---|---|
| `∂_t u_θ` | `q^{-A}·q^{-1} = q^{-3/2-h}` |
| `u_r ∂_r u_θ` | `q^{-1/2}·q^{-A}/q^{1/2} = q^{-3/2-h}` |
| `u_z ∂_z u_θ` | `q^{-A}·q^{-A}/q^{D} = q^{-2A-D} = q^{-3/2-h}` |
| `Δu_θ` (radial) | `q^{-A}/q = q^{-3/2-h}` |

## **PREDICTED EXPONENT: `−3/2 − h = −1.51` at `h = 1/100`.**

## 4. THE PRE-COMMITTED TOLERANCE

## **TOLERANCE: `|measured − (−1.51)| ≤ 0.05` on the fitted exponent.**

**Derived, not chosen for comfort.** At a fixed similarity point the residual is exactly
`C(X,η)q^{-3/2-h}` plus a relative correction of order `q^{2h}` (the axial-diffusion term, the
construction's own expansion parameter). Across the ladder `q^{2h} = τ^{0.02}` runs from
`(10^{-8})^{0.02} = 0.6918` to `(10^{-4})^{0.02} = 0.8318`. A correction factor varying by that
ratio over four decades perturbs the fitted slope by

```
log10(0.8318 / 0.6918) / 4  =  0.0201
```

so the **systematic floor is ≈ 0.020**. The tolerance is set at `0.05`, a factor 2.5 over the
floor, and it is still far tighter than the separation to every control below (`≥ 0.21`).

**A tolerance that cannot separate the controls would be worthless; a tolerance below the derived
systematic floor would be a trap. `0.05` is the smallest round number above `2 × 0.020`.**

## 5. THE PRE-COMMITTED RESOLUTION LADDER (`≥ 3 levels`)

Derivatives are 4th-order central finite differences with step `δ = ρ · ℓ`, `ℓ` the local length
scale in each variable (`ℓ_r = q^{1/2}` in `r`, `q^{D}` in `z`, `τ` in `t`), at

## **`ρ ∈ {1e-2, 1e-3, 1e-4}` — three levels.**

The **reported** exponent is the one at `ρ = 1e-3`. **The spread across the three levels is the
numerical uncertainty and MUST be `< 0.025` (half the tolerance), or the measurement is reported
`UNDER-RESOURCED` and the gate is not answered from it** (§3d: an under-resourced null returns a
cost, not a verdict).

## 6. CONSERVATION DRIFT, REPORTED WHATEVER IT IS

- `max |∇·u|` over the core grid, **normalised** by `max|u|/ℓ_r`, at every `τ` and every `ρ`.
  Incompressibility is exact by construction, so this measures the **differentiation scheme**, not
  the field. **Reported whatever it is; no threshold is attached to it and it gates nothing.**
- The two exterior moment identities the manuscript requires, `∫₀^∞ r²R_θ dr = 0` and
  `∫₀^∞ rR_z dr = 0`. **These are EXPECTED TO FAIL here** — they are conditions on the
  manuscript's joined profile, which is not reproduced. **They are reported as failing, with their
  values, because reporting a condition one does not meet is the point of measuring it.**

## 7. PLANTED CONTROLS — pre-computed predictions, firing in BOTH directions

The leading exponent is `−max(A + 1, 2A + D)`. Every prediction below follows from that formula
and is computed **before** any run.

| id | change | predicted exponent | separation from `−1.51` | must |
|---|---|---|---|---|
| **P0** | none — the instantiation itself | **−1.51** | — | **land inside `±0.05`** |
| **C1** | `A = 0.80`, `D = 0.49` | `−max(1.80, 2.09) = −2.09` | 0.58 | **move, and land inside `±0.05` of −2.09** |
| **C2** | `A = 0.51`, `D = 0.70` | `−max(1.51, 1.72) = −1.72` | 0.21 | **move, and land inside `±0.05` of −1.72** |
| **C3** | amplitudes rescaled: `B ×= 3.7`, `S ×= 0.4` | **−1.51, unchanged** | 0 | **NOT move — an amplitude is not an exponent** |
| **C4** | the residual operator applied to rigid rotation `u_θ = Ωr`, `p = Ω²r²/2` | residual `≡ 0` | — | **be zero to discretisation error** |
| **C5** | the residual operator applied to `u_z = e^{−a²t}J₀(ar)`, `p = 0` | residual `≡ 0` | — | **be zero to discretisation error** |
| **C6** | C5 with `a` perturbed by 1% in the time factor only | residual **≠ 0** | — | **be nonzero — C4/C5 must not be vacuous** |

**C4, C5 validate the instrument. C6 proves C4/C5 are not vacuous. C1, C2 prove the measurement
can say a different number. C3 proves it does not say a different number for the wrong reason.**

## 8. THE GATE, IN ITS FINAL WORDING

> **Does the measured residual scale as the construction requires?**

Answered **`YES`** iff **P0 lands inside `±0.05` of `−1.51`** *and* **the three-level spread is
`< 0.025`** *and* **every control in §7 does what its row says**. Answered **`NO`** if P0 lands
outside tolerance with the spread inside it. Answered **`UNDER-RESOURCED`** if the spread exceeds
`0.025`, in which case the cost is reported and no verdict is drawn (§3d).

## 9. CEILING, WRITTEN NOW

This is **float64 finite differences on a synthetic field with the manuscript's scalings**. It is
**Tier 2 at best and is not a proof of anything**. It confirms or refutes a **dimensional** claim
about a residual, on an object that is **not the manuscript's profile**. **No `L1 → L4` link can
move here. Clay stays ~0.05%. `W4` is not touched by this unit.**

## 10. THE TEMPTATION, RECORDED IN ADVANCE

The named risk is that P0 lands at, say, `−1.56` and the derived floor of `0.020` gets rewritten as
`0.05 + something`. **If that happens the gate answer is `NO` and the `NO` is banked.** The
tolerance above is fixed at `0.05` and the floor derivation in §4 is the whole of its
justification; there is no second argument held in reserve.
