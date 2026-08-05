# Route-L1 v1 — the certificate stops being a rehearsal: the constants become bounds

*Phase 2, leg 50. Stage `L1` step one: wire `solver/interval.py` — an arithmetic layer
built in Route-D and never connected to anything — through the bordered residual, so
`Y₀`, `Z₁`, `Z₂` are **rigorous upper bounds** rather than float readings. Code:
`solver/interval_certificate.py`, `solver/interval.dot2_matvec`,
`test_interval_certificate.py` (7/7), `experiments/p2_route_l1_v1_interval.py` →
`writeup/data/p2_route_l1_v1_interval.json` → **fig45**. Deterministic, 11 s.*

**THE RADII POLYNOMIAL CLOSES IN INTERVAL ARITHMETIC ON `HL_S2_nonsymmetric`, at all three
rungs.** And the thing that decided it was not the mathematics: it was how the residual is
evaluated.

---

## 0. What is being claimed, exactly

Stated once, before the numbers, and not widened afterwards:

> Let `H`, `D`, `Uop` be the **stored float matrices** and let `F` be the bordered residual
> of `solver/bordered_hl.py` built from those matrices as exact data. Then `F` is a
> polynomial map `R^N → R^N` with exactly-representable coefficients, and there is a **true
> zero of that polynomial system** within `r` of the stored iterate, in the weighted sup
> norm, for every `r` in the reported interval.

What is **not** claimed: anything about the continuum profile. Two terms stand between the
two and neither is bounded here — the consistency of `(H, D)` with the operators they
discretise, and the far field beyond `X_max`. Leg 46 measured the truncation gap at
**1.55e+08 ball radii** and leg 47 measured that reach makes it *worse*; both stand. This
is **step one of `L1`, not `L1`** (standing discipline 75: two defects in the same problem
are not the same defect).

---

## 1. The result

`n = 201, 401, 801`, weight `p* = 0.39`, `w_l = 0.01 X_max`, `A = DF⁻¹` in float (a
**choice**, not a computed quantity that has to be right — a bad `A` merely makes `Z₁`
large).

| `n` | `Y₀` | `Z₁` | `Z₂` | budget | `Y₀/budget` | `r` interval | |
|---|---|---|---|---|---|---|---|
| 201 | 5.17e−12 | 8.59e−09 | 2.21e+08 | 2.27e−09 | **2.28e−03** | [5.18e−12, 4.53e−09] | ✓ |
| 401 | 1.30e−11 | 5.71e−08 | 8.46e+08 | 5.91e−10 | **2.20e−02** | [1.30e−11, 1.18e−09] | ✓ |
| 801 | 7.35e−12 | 1.54e−07 | 1.41e+09 | 3.55e−10 | **2.07e−02** | [7.39e−12, 7.11e−10] | ✓ |

`Z₁ < 1` rigorously at every rung, which is the precondition for anything else in the
certificate to mean anything.

**The price of rigour, per constant.** `Y₀` widens by 11.7×, 4.4×, 21.2× against its float
reading; `Z₁` by 63×, 79×, 31×. Neither is where the difficulty is. `Z₂` is essentially
unchanged, because it was already assembled from operator-norm bounds rather than measured.

---

## 2. The finding: the binding constraint was the arithmetic, not the object

The first version of this leg did **not** close. It missed by **1.48×** at `n = 201`, and
by 38.6× and 175× at the finer rungs. The term that ran out of margin was `Y₀`, and the
reason had nothing to do with the profile:

At a Newton-converged iterate the residual is `‖F‖_∞ = 5.7e−15`, assembled from terms of
size `~3e−02` — a cancellation of thirteen decades. The naive interval matvec bounds an
`m`-term accumulation by `γ_m Σ_j |M_ij v_j|`, which is sharp when terms do not cancel and
useless when they do. Measured, at `n = 201`:

| operator | naive enclosure width | compensated | tightening |
|---|---|---|---|
| `H` | 2.46e−13 | 8.88e−16 | 278× |
| `Uop` | 7.28e−12 | 1.14e−13 | 64× |
| `D` | 2.37e−12 | 2.22e−16 | **10664×** |
| `D` (on `V`) | 1.88e−12 | 2.22e−16 | 8474× |

The slope operator `D` is the worst offender — its rows cancel to about 1/270 of their
absolute mass — and it is the one that multiplies `S ~ 7` in the residual. **`Y₀` was being
set by the width of its own evaluation, 2.3e−12, against a residual of 5.7e−15: a factor of
400 of pure arithmetic.**

The fix is standard and it is not an approximation: `dot2` (Ogita–Rump–Oishi 2005), where
the product and the sum each return their own rounding error *exactly* through error-free
transformations, so the accumulated error carries the bound

    |dot2(x,y) − x·y| ≤ u|x·y| + γ_m² Σ_j |x_j y_j|

— the cancellation-sensitive term squared away at `γ_m² ~ 5e−28`, and what remains
*relative to the answer*. It costs one loop over the `m` columns with a handful of length-`n`
numpy operations each; at `n = 801` the whole certificate takes 4.5 s.

**Both paths are reported at every rung** (fig45 panel B), because the difference *is* the
finding: the same certificate, the same object, the same weight — one path says the zero
exists, the other says nothing can be concluded. **A rigorous bound that is dominated by
its own evaluation error is a statement about the code, not the mathematics.**

---

## 3. The enclosures are checked against exact rational arithmetic

A bound checked against another float is not checked. Selected rows of every operator
product were recomputed with `fractions.Fraction` — no floating point anywhere in the
reference — and **both** enclosures contain the exact value, at every row tested, for `H`,
`Uop` and `D`. That is the gate that separates "my interval code agrees with my float code"
from "my interval code is correct".

The two rigorous enclosures also stand in the right relation to each other: they overlap
everywhere, and the compensated one is never wider except on rows whose exact answer is `0`,
where both are denormal-scale (`±1e−323`) and both contain it.

---

## 4. It rejects a wrong point

A certificate that closes around anything certifies nothing. Perturbing the iterate:

| perturbation | `Y₀/budget` | |
|---|---|---|
| 1e−10 | 2.77e−01 | closes — **correctly**: 1e−10 is inside the certified ball, so a true zero really is nearby |
| 1e−08 | 4.50e+01 | rejected |
| 1e−06 | 5.65e+03 | rejected |

The certified ball at `n = 201` has `r_max = 4.53e−09`, so the transition sits exactly where
it should.

---

## 5. The known-answer object, through the same pipe

The `a = 0` CLM system of leg 49 — exact solution in closed form since 1985 — runs through
the identical code path. It **closes at `n = 201`** (`Y₀/budget = 5.33e−02`, certified ball
`r_max = 2.06e−08`, with the iterate sitting 4.13e−05 from the exact continuum profile) and
**fails at `n = 401`** (1.53e+02).

That failure is not a surprise and it is the cross-check: leg 49 measured the *float*
certificate on this object failing at exactly the same rung, for `Z₁ = κ(DF)·ε_mach`
reasons. The rigorous pipeline reproduces the float pipeline's resolution dependence on an
object where both can be run. **The two legs agree about where the wall is.**

### 5b. Leg 49's searched weight transfers to the rigorous constants

Not a validated method — leg 49's viability gate said `FAIL` and the GA never ran — but a
cheap measurement, and one whose answer does not follow from anything:

| `n` | leg 46's hand weight | leg 49's searched weight | gain |
|---|---|---|---|
| 201 | 5.33e−02 | 6.18e−03 | **8.63×** |
| 401 | 1.53e+02 | 2.11e+01 | 7.27× |

Leg 49 measured **8.61×** for the same pair in float. The weight was optimised against a
float objective; it buys the same factor on a rigorous bound, to within 0.2%. **The number
the search optimises is the number that matters** — which is an argument for repairing that
fitness rather than abandoning it, and not an argument for lifting its gate.

---

## 6. What this costs and what it does not buy

**Costs.** About four times the float constants: the point-matrix × interval-matrix product
splits monotonically into four BLAS matmuls, and no `O(N³)` interval operation is ever
performed in Python. `n = 801` (`N = 1605`) runs in 4.5 s.

**Does not buy.** A proof about the Hou–Luo profile. The object named at leg 45 still has
no proof of any kind, and this leg has not produced one — it has produced a rigorous
statement about a finite-dimensional truncation of it. The remaining work is exactly what
leg 47 priced: **an analytic far-field enclosure**, which is mathematics and not compute,
plus a consistency bound relating the stored `(H, D)` to the operators they discretise.
That is `L1` step two, and it is the gate the plan of record actually asks about.
