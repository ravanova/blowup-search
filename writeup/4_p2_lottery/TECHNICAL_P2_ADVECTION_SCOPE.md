# The advection scope of the Route-D bound programme: the velocity is logarithmically divergent

*Phase-2 P2, Route-D scoping note. Code: `solver/advection_scope.py` +
`test_advection_scope.py` (6/6). **No figure and no committed JSON** — every number
here is reproduced by running the gates, and a plot of two log-slopes would add
nothing a table does not.*

**Rigor level: 0–1 — a scoping measurement, in plain float64.** Nothing is
interval-enclosed, nothing is rigorous, and this is a statement about *which space
the later rigorous work has to be done in*, not a statement about blow-up.

---

## 0. The question nobody had asked

Eleven Route-D legs built a function space, priced it, and bounded constants in it.
Every one of them worked at the exact `a = 0` anchor — because that is where the
known-answer gate lives.

And `a = 0` is precisely the value at which the advection term `−a U Ω_X` is
**absent**.

So the space was chosen, tuned and optimised on the one member of the family where
the term it would have to carry does not exist. Whether it can carry that term at
all was never checked. It cannot.

## 1. The velocity is logarithmically divergent

The rescaled velocity is `U(X) = ∫₀ˣ H(Ω) dX'`. Route-D v3 (§S6) already
established the far-field law `H(Ω)(X) → (∫Ω)/(πX)`, so integrating it,

    U(X) → (M/π) log X ,      M := ∫ Ω dX .                              (U)

There is no cancellation available: `M ≠ 0` for every profile in this family — the
`a = 0` anchor itself has `∫ −1/(1+X²) = −π`, giving `M/π → −1`.

Measured against an independently integrated mass:

| `a` | fitted `dU/d log X` | `M_window/π` |
|---|---|---|
| 0.0 | −0.9970 | −0.9969 |
| 0.3 | −0.7544 | −0.7540 |
| 0.5 | −0.6862 | −0.6870 |

**A subtlety that had to be got right.** `dU/dX = H(Ω)` exactly, so
`dU/d log X = X·H(Ω)(X)` is an *identity*; the content of (U) is that it tends to
`M/π`. The right predictor is therefore the mass over the **fit window**, not over
the whole truncated domain — on the sinh grid the outermost decade is coarse (the
same far-field under-resolution v11 found), and at `a = 0.5` that moves the
full-domain mass by 15% while the windowed mass and the fitted slope agree to 0.3%.
Both are returned by `velocity_log_rate` so the discrepancy stays visible.

## 2. What that does to the operator

The linearization carries the advection term as two pieces,

    dR₂/dΩ · h  ⊃  −a [ (V H h)·Ω_X  +  U·h_X ] ,

and in the decay-graded codomain `‖g‖_Y = sup (1+X²)^{(α+1)/2}|g|` that v3–v11 use,
they behave completely differently:

- `(V H h)·Ω_X` ~ `(log X)·X⁻³` → weighted, `X^{α−2} log X`, which **decays** for
  `α < 2` (the whole working range). Harmless.
- `U·h_X` ~ `(log X)·X^{−α−1}` → weighted, `(a|M|α/π)·log X`, which **diverges**.
  For every `a ≠ 0`.

Measured at `α = 1.4` (the operating point of v8–v10), the transport piece's log
rate is **+0.317 against a predicted +0.318** at `a = 0.3`, and +0.480 at `a = 0.5`.
At `a = 0` both pieces are identically zero.

**So `DF` does not map the domain class into the codomain class for any `a ≠ 0`,
and neither does the residual — `Y₀` is infinite in that norm too. The eleven-leg
bound programme is `a = 0`-only.** That had never been stated.

## 3. Which half of this measurement is real

The stretch piece carries `Ω_X`, and for `a ≠ 0` the profile has collapsed to the
far-field discretization noise floor by `X ~ 10`. A log-rate fit out there measures
amplified noise, not the operator.

The discriminator is **reproducibility, not magnitude**:

| `a` | transport, grid-spread | stretch, grid-spread |
|---|---|---|
| 0.3 | **0.4%** | 5% |
| 0.5 | **2.6%** | **99%** |

The transport piece is built from `U` (fixed by the profile's *core* mass) and an
analytic test function, so it repeats under refinement. The stretch piece does not.
**Only the reproducible half is quoted as a result** — the gates enforce that, and
a first version of this note that quoted both would have been reporting noise at
`a = 0.5`.

## 4. The fix is a grading, and the project already has it

The two-scale (traveling-wave) residual balances `Ω H(Ω)` against `c Ω_X`, whose
far field is `X^{−α−1}`; that is why its codomain carries `α+1`. The **one-scale**
(self-similar) residual balances against `c_l X Ω_X` ~ `X^{−α}` instead, so its
natural codomain grading is `α` — one power *weaker*. One power is exactly what the
log needs: `X^α · (log X) X^{−α−1} = (log X)/X → 0`.

Measured on the same profile, same `h`, same grid:

| `a` | two-scale rate | one-scale rate | at `X = 10⁴`: two-scale → one-scale |
|---|---|---|---|
| 0.3 | **+0.317** | **−0.010** | 3.11 → 3.1×10⁻⁴ |
| 0.5 | **+0.480** | **−0.016** | 4.79 → 4.8×10⁻⁴ |

So the constructive reading is not *"`a ≠ 0` is out of reach"* but **"`a ≠ 0` needs
the one-scale formulation"** — which this project already has a validated solver for.

## 5. A crossing found on the way, and what it turned out to be

Because `U` is log-divergent and negative, the effective speed `c_eff = c + aU(X)`
changes sign at a finite, grid-independent radius: `X* = 7.16` at `a = 0.3` and
`3.10` at `a = 0.5`, each stable to ~1% across three grids, with no crossing at
`a = 0`.

This note originally read that as a *stagnation point* — the far field of an
`a ≠ 0` "traveling wave" moving opposite to its core. **A parallel line of work
(`solver/finite_support.py`, Route-D v12/v13) reads the same crossing as something
sharper and better: it is the EDGE OF SUPPORT `X_c`, beyond which the profile is
identically zero with an algebraic zero of order `1/a`.** That reading is the one to
carry forward, and it retro-explains §3's noise floor: the Newton profile collapses
to ~10⁻⁹ by `X ~ 10` while `X* = 7.16`. There is no tail out there. There is
numerical dust past the end of the profile.

The gates here depend only on the reproducible half, so they stand under either
reading.

## 6. Where this sits relative to Clay

**It moves no link of the L1→L4 chain.** It narrows the scope of an L1 sub-programme:
the bound machinery eleven legs built is now known to be `a = 0`-only, and the
repair is named. If anything it is a *cost* finding — work that looked general was
specific — and its value is that it was found before more estimate legs were built
on the assumption.

## 7. Reproduce

```
.venv/bin/python test_advection_scope.py     # 6/6, ~4 min
```

Gates: the log law against an independently integrated windowed mass; the
transport/stretch split with an `a = 0` control where both vanish identically; the
one-scale fix; the reproducibility discriminator; the grid-independence of `X*`;
and an input-sanity gate that the `d/dX` matrix is not double-counted — *which it
was, once, costing exactly one power of `X` and hiding the entire effect.*
