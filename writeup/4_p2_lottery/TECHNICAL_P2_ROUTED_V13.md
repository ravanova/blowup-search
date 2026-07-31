# Route-D v13 — the turning point: correcting v12, and locating the wall

**Status: Level-1 tooling + a correction to the previous leg + an attributed
negative. NOT a certificate, NOT rigorous, NOT a Clay result.** Plain float64.

**Figure:** `fig31` · **Data:** `writeup/data/p2_route_d_v13_turning.json`
**Code:** `solver/turning_point.py` (+ `test_turning_point.py`, 6/6),
`experiments/p2_route_d_v13_turning.py`, `p2_route_d_v13_evidence.py`

---

## 0. What this leg is for

v12 found that the `a > 0` two-scale profile ends at a finite radius `X_c` where
the effective transport coefficient `E = c + aU` crosses zero, with an algebraic
zero of order `1/a`; and it measured that the gauged inverse's graded norm
**diverges** with `J` at that profile (`J^+2.86` at `a = 0.2`) while it is flat at
the `a = 0` anchor (`J^−0.003`). Both stand.

It then attributed the divergence to a homogeneous mode `h ~ (X_c − X)^{−1/a}`.
**That attribution is wrong.** This leg corrects it, finds where the obstruction
actually is, attributes the measured divergence to it by measurement rather than
by argument, and disqualifies the cheap repair v12 recommended.

## 1. The correction

Beyond and around `X_c` the profile vanishes, so the linearization is

```
L h = H(Ω) h − E h_X ,    E(X) ≈ a h_c (X − X_c) ,   h_c = H(Ω)(X_c)
```

with `H(Ω)` and `E` fixed functions of the profile. Put `s = X_c − X`, so
`h_X = −h_s` and `E = −a h_c s`. The homogeneous equation is

```
   h_c h − a h_c s h_s = 0   ⇒   h_s/h = 1/(a s)   ⇒   h ~ s^{+1/a}
```

— a mode that **vanishes** at `X_c`. v12 wrote `s^{−1/a}`, from a sign dropped in
converting `d/dX` to `d/ds`. Nor is the inhomogeneous problem singular there: with
the integrating factor `s^{−1/a}`,
`h = s^{1/a}[C − (1/(a h_c))∫ g σ^{−1/a−1} dσ] → g(X_c)/h_c` as `s → 0`.
**Nothing blows up at the turning point.**

Measured (fit of the inner mode, integrated inward from `0.8 X_c` on the profile's
own `H(Ω)` and `E`, `J = 400`):

| a | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|
| fitted `p` | **+5.28** | +4.21 | +3.51 | +3.01 | +2.65 | +2.14 |
| corrected prediction `+1/a` | +5.00 | +4.00 | +3.33 | +2.86 | +2.50 | +2.00 |
| v12's claim `−1/a` | −5.00 | −4.00 | −3.33 | −2.86 | −2.50 | −2.00 |

Positive at every `a`, within 5–7% of `+1/a` (the same systematic overshoot a
leading-order fit over a finite window gives everywhere in this series).

## 2. Where the obstruction actually is

Outside `X_c` the same equation has the same exponent, and now it is a **growing**
mode. For `X ≫ X_c`, with `m = ∫Ω dX < 0`:

```
H(Ω) ~ m/(πX) ,   E = c + aU ~ (a m/π) log(X/X_c)          [E(X_c) = 0]
⇒  h_X/h ~ 1/(a X log(X/X_c))
⇒  h ~ ( log(X/X_c) )^{1/a}
```

The domain space of the entire Route-D programme is the decay class
`|h| ≲ X^{−α}`. A growing mode is not in it, and the constant multiplying it is
fixed by matching to the inner solve rather than free — so the image of the
inverse generically **leaves the space**. That is a codimension-1 range
obstruction of the continuum operator, and no amount of grid refinement touches
it. It is a strictly worse situation than the local singularity v12 named, which
would at least have been a resolution problem.

Measured with an instrument independent of the matrix inverse — integrate
`h_X = (H(Ω)/E) h` outward from `1.5 X_c` on the profile's exact `H(Ω)` and `E`,
out to `X = 1e8`:

| a | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 |
|---|---|---|---|---|---|
| `q` in `h ~ (log(X/X_c))^q` | **4.9988** | 3.9980 | 3.3307 | 2.8536 | 2.4855 |
| prediction `1/a` | 5.0000 | 4.0000 | 3.3333 | 2.8571 | 2.5000 |
| `h` at `X = 1e8` | 8.2e7 | 2.4e6 | 2.2e5 | 3.9e4 | 1.0e4 |

Agreement is 0.02–0.6%, with no fitted constant anywhere. The quadrature is
converged (the exponent moves 1.6e-4 over a 16× refinement of the integration
grid).

**The row that did not fit, refined rather than dropped.** At `a = 0.5` the
measurement returns `q = 0.054` against a prediction of 2. v12's own rate table
(T4) already said the collocation profile stops converging around there, so the
question is whether the prediction fails or the profile is unresolved:

| a = 0.5 | J = 400 | J = 800 | J = 1600 |
|---|---|---|---|
| `q` | 0.054 | 1.838 | 1.696 |
| `a = 0.4` control | 2.4855 | 2.5035 | 2.5014 |

`a = 0.4` is converged to four digits; `a = 0.5` moves by a factor of 34 on the
first refinement and is still drifting. The outlier is the instrument.

## 3. So `1/a` appears three times, in three roles

One exponent, in one problem:

* the order of the **profile's zero** at `X_c` (v12 T3),
* the exponent of the **vanishing inner mode** of the linearization (§1),
* the power of the logarithm by which the **outer mode grows** (§2).

All three are forced by the same leading balance `Ω H(Ω) = E Ω_X` with `E`
vanishing linearly, and none of them has a fitted constant.

## 4. Attributing v12's divergence

An argument that says where a divergence comes from is not a measurement. The
measurement: recompute `‖A‖` with the **domain** sup restricted to a fixed outer
radius, so that the grid's own outer radius (`~4J/π`, which grows with `J`) stops
being the thing that moves.

| `‖A‖` J-slope | rows `X ≤ 20` | `X ≤ 50` | `X ≤ 200` | all |
|---|---|---|---|---|
| a = 0 (control) | `J^−0.00` | `J^−0.00` | `J^−0.00` | `J^−0.00` |
| a = 0.2 | `J^+0.31` | `J^+0.54` | `J^+1.06` | **`J^+2.86`** |
| a = 0.3 | `J^+0.53` | `J^+1.15` | `J^+1.42` | **`J^+2.75`** |

The divergence is monotone in the outer radius and nearly gone when the far field
is excluded — and the `a = 0` control is flat at every cutoff, so the ladder is
measuring the profile and not the discretization. The residual `J^+0.3…0.5` at
`X ≤ 20` is real and **not attributed by this leg**; it is small compared to what
the far field contributes, but it is not zero and should not be described as such.

Where the extremal row is *sourced* is the complementary measurement: the
fraction of its mass coming from codomain slots within 10% of `X_c` is
**69→86→92% (a=0.2)**, **87→93→97% (a=0.4)** over `J = 200/400/800`. So the
picture is coherent: the perturbation is *sourced* at the turning point and *does
damage* in the far field, which is exactly what a growing homogeneous mode
excited at `X_c` does.

## 5. The cheap repair, disqualified

v12 recommended bordering the system with an extra unknown to supply the missing
range direction, and the obvious candidate is the speed `c`, which the
certificate's gauge freezes. **It cannot work, and the reason is already in the
project's own notes:** dilation `Ω(X) → Ω(X/μ)`, `c → μc` is a symmetry of the
zero set at every `a`, so restoring `c` supplies a **kernel** direction, not a
range direction. A symmetry cannot discharge a solvability condition.

Measured anyway, because a prediction that is not measured is an opinion:

* the **square** bordered system `[gauge ; DF | dF/dc]` at `a = 0` has
  `cond = 4.4e18`, `σ_min = 4.4e-17` — singular to machine precision, which is
  Route-D v1 Q2's and v11 V0's finding read forward;
* the overdetermined version's norm **grows with `J` even at the anchor**
  (`J^+1.40` at `a = 0`, where the plain system is flat), and at `a = 0.2/0.3` it
  grows `J^+1.57/J^+1.86` — better than `J^+2.86` but still divergent.

## 6. Ledger, gate-check, honest reading

**CORRECTED:** v12's stated mechanism for the `‖A‖` divergence.
**UNCHANGED:** the profile ends at `X_c` with a zero of order `1/a`; `‖A‖`
diverges with `J` at the `a > 0` profile and is flat at `a = 0`; `Y₀` in the
graded codomain norm is not under budget once the operator is priced at the right
point.
**NEW:** the obstruction is a codimension-1 **range** condition from a growing
far-field mode, not a local singularity; and the cheap repair is disqualified.

**GATE-CHECK (a) which link does this move?** L1, and only in the sense of
knowing what is wrong. It corrects a published claim and replaces an argument with
an attributed measurement. Nothing here is rigorous and nothing climbs the ladder.

**(b) is another L1 leg the best use of the next chunk?** The repair is now
sharper than it was in v12, because the diagnosis changed what it has to do. It is
not "border the operator". It is **remove the far field from the domain**: pose
the problem on `[0, X_c]` with `X_c` an unknown and perturbations supported there,
so that the growing mode has nowhere to live. That is consistent — the residual
`Ω H(Ω) − E Ω_X` vanishes identically outside the support because every term
carries a factor of `Ω` or `Ω_X`, even though `H(Ω)` does not vanish there.

**(c) a cheaper experiment that kills the route?** Unchanged and still the right
first move: build the finite-interval system at one `a` and measure `‖A‖` against
`J`. Flat ⇒ the framing is repaired and eleven legs of far-field machinery are
simply not needed. Still divergent ⇒ the framing needs replacing, and the
alternative lanes (the coupled-system HL question; writing the P2 arc up) become
primary.

**HONEST CEILING (unchanged).** Plain float64; nothing interval-enclosed; nothing
rigorous; a toy model. What v13 adds is that the previous leg's headline number
was right and its explanation was not — which is the sort of thing that is only
cheap to find if you go looking.
