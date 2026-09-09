# Leg 421 — unit `U5` PRE-REGISTRATION (`DOES IT MOVE W4?`)

**COMMITTED BEFORE THE RUNNER EXISTS AND BEFORE ANY NUMBER IS PRODUCED.**

Everything below is fixed. If any of it changes after a number exists, the change is a
`CORRECTIONS.md` entry naming what was changed and why — as `U4` did at `§64`, where a control
this unit's predecessor wrote for itself caught a defect in its own pre-registration.

---

## 1. `W4`'s OWN TEXT — quoted, not paraphrased

The charter is explicit: *"Read W4's own pre-committed statement of what breaking it consists of
and answer against THAT text, not a paraphrase."* From `WALLS.md`, verbatim:

> **Statement.** A DSS profile on `ℝ³` has infinite global energy; Clay condition (7) demands
> bounded energy. Converting one into the other — cutting the profile off and showing the cut
> solution still blows up — has **no known method**, anywhere.

> **BREAKING W4 CONSISTS OF:** (a) a localisation argument carrying blow-up from the
> infinite-energy profile to a finite-energy solution with the decay actually available, or (b) a
> natively finite-energy ansatz, or (c) a target for which condition (7) is not imposed —
> Fefferman statement **(D)**, the torus. **Lanes: T and L.** Attack (c) is deferred with Lane T.

**This unit tests clause (a) and only clause (a).** (b) is measured shut (`L5` leg 400, `PB2` leg
410 on Tsai 1998 Thm 2). (c) is statement (D), which is **Lane T's, deferred by a user ruling**,
and which `U1` found the manuscript *claims* — a fact recorded at `CORRECTIONS.md` §61 and **not
ruled on here**.

## 2. THE PORT, AND EVERY ADVANTAGE GRANTED TO IT

The object is **this repository's own banked route-4 witness**, unmodified:
`solver/dssp_biot_savart.py`'s closed-form `field_uB`, whose vector potential is
`𝒜(y) = a(|y|)(y₂, −y₁, 0)` and whose far-field decay is the **pinned `α = 1`**.

Self-similar ansatz, `T = 1`, `τ = 1 − t`:

```
u(x,t) = τ^{-1/2} U(x/√τ),   U = field_uB
       = curl_x [ 𝒜(x/√τ) ]                     (the τ prefactor cancels)
```

The manuscript's mechanism, applied **literally** (its §3.5): cut the **vector potential**, then
take the curl, so incompressibility survives exactly:

```
u_cut(x,t) = curl_x [ χ(|x|/R) · 𝒜(x/√τ) ],     f := ∂_t u_cut + (u_cut·∇)u_cut − Δu_cut
```

**THREE ADVANTAGES ARE GRANTED, EACH DELIBERATELY, SO THAT A `NO` CANNOT BE BLAMED ON THE SETUP:**

1. **`p ≡ 0`.** Fefferman (C) needs a *smooth* pressure, and zero is smooth. Because `f` is free,
   any pressure can be absorbed into it; taking `p ≡ 0` is the most favourable choice available
   and it removes a modelling decision entirely.
2. **`f` is whatever is left.** `(u_cut, 0)` then solves forced Navier–Stokes **exactly**, by
   construction, at every `τ > 0`. There is nothing to estimate and nothing to approximate.
3. **The cutoff is applied to the potential, not the velocity**, so `∇·u_cut = 0` exactly.

**Consequently the ONLY question left is whether `f` is admissible** — i.e. whether it is a smooth
force on `ℝ³ × [0,∞)` satisfying Fefferman **(5)**. That is the whole of clause (a) once the free
force is granted, and it is what this unit measures.

## 3. WHAT IS MEASURED, AND THE PRE-COMMITTED NUMBERS

Residual operator: full 3D Cartesian, `R_i = ∂_t u_i + u_j ∂_j u_i − Δu_i`, 4th-order central
differences at **three levels** `ρ ∈ {1e-2, 1e-3, 1e-4}` of the local scale; **the reported value
is `ρ = 1e-3`, the spread across levels must be `< 0.025` or the measurement is
`UNDER-RESOURCED`** (§3d). `τ` ladder `10^{-4} … 10^{-8}`, five rungs.

| # | measurement | where | **pre-committed prediction** | tolerance |
|---|---|---|---|---|
| **M1** | `max\|f\|` at **fixed similarity points** `y`, `\|y\| ∈ [0.5, 4]` | the core, `χ ≡ 1` | **exponent −3/2 = −1.500** | **0.05** |
| **M2** | `∫\|u_cut\|² dx` | all space | **exponent 0** (bounded energy) | **0.05** |
| **M3** | `\|U(sŷ)\|` on two rays | far field | **exponent −1.000** — the `α = 1` **pin**, `L2′` leg 397 | **0.05** |
| **M4** | the far-field **correction** exponent `δ` in `s\|U(sŷ)\| = c + d·s^{−δ}` | far field | **NO PREDICTION. MEASURED.** This repository has never measured it. | — |
| **M5** | `max\|f\|` at **fixed physical points** in the cutoff annulus `\|x\| ∈ [R, 2R]` | the annulus | **exponent 0** (finite limit) | **0.10** |
| **M6** | `max\|∂_t f\|` in the same annulus | the annulus | **exponent `δ/2 − 1`**, from `M4` measured in the same run — a **consistency test between two independent measurements**, which is stronger than a prediction | **0.15** |

**M1's prediction is exact, not asymptotic.** At a fixed similarity point every term of the
residual is exactly `τ^{-3/2}` times a function of `y`: `∂_t u = ½τ^{-3/2}[U + (y·∇)U]`,
`(u·∇)u = τ^{-3/2}(U·∇)U`, `Δu = τ^{-3/2}Δ_y U`. **There is no subleading contamination in M1**,
which is why its tolerance is the same `0.05` `U4` needed for a contaminated fit.

## 4. THE PRE-COMMITTED DECISION RULE FOR THE GATE

> **Does `W4` break under its own test?**

**`W4` clause (a) BREAKS iff ALL THREE hold:**

- **(a1)** the cut solution has **uniformly bounded energy** — `M2` exponent `≥ −0.05`;
- **(a2)** the cut solution **still blows up** — true by construction, since `χ ≡ 1` on a fixed
  ball around the origin and `u` there is the uncut self-similar field; **recorded as satisfied by
  construction, not measured, and said so**;
- **(a3)** `f` is **admissible as a Fefferman (C) force** — every measured residual exponent
  (`M1`, `M5`, `M6`) is `≥ −0.05`, i.e. **nothing diverges as `t → T`**.

**If any of the three fails, the answer is `NO` with the measured reason. A `NO` is banked with
the same care as a `YES`.**

## **PRE-COMMITTED EXPECTATION: (a1) YES, (a2) YES, (a3) NO — so the gate answers `NO`.**

**The reason predicted in advance:** route 4 **has no exact profile**. `L6` (leg 401) and `L6-b`
(leg 406) measured `ρ = 1.5048519` at 20,000 iterations against a threshold `< 1.45`. The banked
witness is a *Type-I-enveloped* field, not a solution of the profile equation, so its residual at
a fixed `y` is a **non-zero** function of `y` and `M1` must come back at `−3/2`, i.e. divergent.

**Writing the expected answer down in advance is the point.** If `M1` instead comes back `≥ 0`
this unit has found something enormous, and the charter's instruction is absolute: **stop, write
it up, escalate to the user. Do not extend, do not generalise, do not claim Clay.**

## 5. THE SECOND FINDING, MEASURED SEPARATELY — the one with reach

`M1` fails for a reason **specific to this repository**: route 4 has no exact profile. That says
nothing about whether the mechanism would work for a profile that *did* solve its equation.

**`M5` and `M6` are measured on the CUTOFF-GENERATED TERMS ALONE** — the difference
`f_cut − χ·f_uncut`, which is what survives when the core residual is granted to be zero. **This
is a counterfactual and it is labelled one.** It asks: *even granting an exact `α = 1` profile,
does the manuscript's mechanism produce an admissible force?*

**`M6` is where that is decided**, and its answer is `δ/2 − 1` where `δ` is `M4`. **`δ ≥ 2` is
required for admissibility. If `δ < 2`, `∂_t f` diverges at the singular time for EVERY `α = 1`
profile, exact or not, and that is a statement about the wall rather than about route 4.**

**A LOG IS FLAGGED IN ADVANCE.** If `δ = 2` exactly, the correction may carry a `log` and `∂_t f`
would then diverge **logarithmically** — invisible to a power fit. `CORRECTIONS.md` §52–§54 and
`PB2` record two log divergences this repository has already been caught by. **The runner
therefore also reports the per-decade increment of `max|∂_t f|`, which is constant for a log and
falls to zero for a convergent quantity, and no `δ = 2` result may be read as admissible without
that increment.**

## 6. PLANTED CONTROLS — pre-computed, firing in BOTH directions

| id | change | prediction | must |
|---|---|---|---|
| **K1** | Type-II ansatz `u = τ^{−0.7}U(x/√τ)` | core exponent `−max(1.7, 1.9) = −1.9` | **MOVE**, inside `±0.05` |
| **K2** | `U → 2.5·U` | core exponent **−1.5, unchanged** | **NOT MOVE** |
| **K3** | far-field fitter on planted `A/s + B/s^{1+δ₀}`, `δ₀ = 1.5` | recover `1.5` | inside `±0.10` |
| **K4** | same, `δ₀ = 3.0` | recover `3.0` | inside `±0.10` |
| **K5** | residual operator on the exact solution `u = (e^{−k²t}sin(kx₃), 0, 0)`, `p ≡ 0` | residual `≡ 0` | zero to discretisation error |
| **K6** | `K5` with `k` 1% wrong **in the time factor only** | residual `≠ 0` | **nonzero — K5 must not be vacuous** |
| **K7** | `∇·u_cut` on the cut field | zero by construction | **reported whatever it is; gates nothing** |

## 7. CEILING, WRITTEN NOW

Float64 finite differences on this repository's own banked closed-form witness. **Tier 2 at best
and a proof of nothing.** A `NO` here says the mechanism does not port **to this object, measured
this way**; it does not prove no localisation argument exists, and `W4`'s own statement is
*"no known method"*, which a measurement cannot upgrade to *"no method"*. **Clay stays ~0.05%
whatever the answer.**

## 8. THE TEMPTATION, RECORDED IN ADVANCE

The named risk is the opposite of `U4`'s. Here the **expected** answer is `NO`, and the temptation
is to find it comfortable and stop looking — to let `M1`'s divergence end the unit and never
measure `M4`–`M6`, which are the ones that could say something about the wall rather than about
route 4. **`M4`, `M5` and `M6` are run and reported whatever `M1` says.** That is written here so
that skipping them would be visible.
