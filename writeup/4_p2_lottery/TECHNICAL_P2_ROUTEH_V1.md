# Route-H v1: the marginal case, where every scaling argument returns zero information

*Phase-2 P2, Route-H v1. Code: `solver/critical_dissipation.py` +
`test_critical_dissipation.py` (10/10); driver
`experiments/p2_route_h_v1_critical.py` → `writeup/data/p2_route_h_v1_critical.json`
→ **fig37**. Deterministic, not a logged Tier run.*

**Rigor level: 0–1 — plain float64 throughout.** Nothing is interval-enclosed, nothing
here is rigorous, and none of it is a statement about Navier–Stokes. It is a statement
about a one-dimensional toy whose only relevance is that it can be *put* at the point
where NS sits.

---

## 0. The wall both previous legs stopped at

Route-F v1 (§27) measured the critical dissipation exponent for gCLM and Route-G v1
(§28) ported it to 2D Boussinesq, arriving at the invariant law

    s_c = 1/(2β) ,      L ~ (T−t)^β .

Both then said the same thing about the point `s = s_c` itself: **at criticality the
dissipative and nonlinear terms balance identically, so the scaling comparison returns
zero information.**

That is not a footnote about a corner of the map. `β = 1/2` for Navier–Stokes by
dimensional analysis, so `s_c = 1` — the ordinary Laplacian, exactly. **NS is the
marginal member**, and "every scaling argument about NS comes back empty" is a
restatement of that fact rather than a separate difficulty.

So the marginal case is the case. This leg asks what actually happens there, in a model
where the marginal point is *reachable* because `α` is a dial.

## 1. Promote `μ` to a dynamical variable

Take gCLM with fractional dissipation on the line,

    ω_t + a u ω_x = ω u_x − ν Λ^{2s} ω ,      u_x = H(ω) ,

and Route-E's dynamic rescaling `ω = A(t) Ω(X, τ)`, `X = x/L`, `dτ = A dt`, `c_l = 1`.
The dissipative term neither vanishes nor survives with a fixed coefficient: it returns
multiplied by

    μ(τ) := ν / (A L^{2s}) ,

and the rescaling ODEs `A'/A² = −c_ω`, `L'/(LA) = −1` turn that into an ODE for `μ`.
With `α := −c_ω` (Route-E's output, and the profile's far-field decay exponent),

    Ω_τ = (c_ω + HΩ)Ω − X Ω_X − a U Ω_X − μ Λ^{2s} Ω ,          (F_μ)
    μ_τ = (2s − α[Ω, μ]) μ .                                     (M)

The pair `(Ω, μ)` is autonomous, and reading it is the whole leg.

### 1a. Route-F's `s_c` is an eigenvalue

Linearize (M) at the inviscid fixed point `(μ = 0, α = α₀)`. The `μ`-direction has
growth rate

    λ_μ = 2s − α₀ ,

negative exactly when `s < α₀/2 = s_c`. Route-F obtained `s_c` by fitting a power law to
`D/N` along a time-dependent trajectory; this is the same number, and it says what it
**is** — the stability exponent of the inviscid self-similar profile against the one
direction dissipation opens. A scaling statement has become a spectral one. *(fig37 A)*

### 1b. At criticality the eigenvalue is exactly zero, and one number decides

Set `2s = α₀`. The linear term in (M) is gone, so the outcome is set by the next one.
Expanding `α(μ) = α₀ + α₁μ + O(μ²)`,

    μ_τ = −α₁ μ² + O(μ³) ,

so **the entire marginal case reduces to the sign of `α₁ = dα/dμ`**:

| `α₁` | (M) at criticality | reading |
|---|---|---|
| `> 0` | `μ ~ 1/(α₁ τ)` — **algebraic** decay, not exponential | the critical viscous solution relaxes onto the inviscid self-similar profile and blows up anyway |
| `< 0` | `μ` runs away | dissipation wins; the self-similar form is not reached |
| `= 0` | `μ_τ = 0` | a genuine **line** of viscous self-similar blow-ups |

One number, and it is cheap. That is the payoff for writing (M) down.

### 1c. The gauge had to be re-derived

Route-E's `c_ω = 1 + (a−1)H(Ω)(0)` comes from freezing the origin slope,
`(Ω_τ)_X(0) = 0`. The dissipative term contributes to that derivative — for odd `Ω`,
`Λ^{2s}Ω` is odd and its `X`-derivative at `0` is not zero — so

    c_ω = 1 + (a−1)H(Ω)(0) + μ (Λ^{2s}Ω)_X(0) / Ω_X(0) .          (N′)

Banked lesson 48 says re-derive a gauge when you generalize it rather than extending it;
this is that lesson applied to the previous leg's own gauge. Gate (3) finite-differences
the resulting Jacobian, because (N′) contributes a quotient and a quotient rule is
exactly the kind of thing that is wrong by one term. It matches to **4.0e−11**.

## 2. Why the marginal problem is exactly representable here

Route-E's compactified basis (`X = tan(θ/2)`, odd sines) makes `H` exact, and therefore

    Λ = H d/dX  maps sines to sines exactly,

as does every **integer** power of it. So `Λ^{2s}` is an exact, quadrature-free matrix
precisely when `2s` is a positive integer — when `s` is a half-integer.

And criticality asks for `2s = α`. Route-E found `α(a)` passing through the odd integers
at isolated `a`: `α = 1` at `a = 0`, `α = 3` at `a = 1/2`, `α = 5` at
`a = 0.5821792673`. **The critical dissipative problem is exactly representable at
precisely the points where criticality can be posed at all.** That is a coincidence of
two conditions, not a design choice, and it is what makes this leg cheap. Away from
those `a` the equations are still correct; `Λ^{2s}` is simply no longer a finite matrix.

**§6 shows this alignment is weaker than it looks at the third point.**

## 3. H1 — the known answer: a closed-form viscous blow-up

At `a = 0`, `s = 1/2` the marginal problem is solvable in closed form. With
`z = H(ω) + iω` (analytic in the lower half plane for these profiles) one has
`Λz = i z_x`, so the dissipative CLM equation becomes a complex Burgers equation

    z_t + iν z_x = z²/2

whose characteristics are the constant complex shift `x → x − iνt`. Substituting the
CLM profile gives, for every `μ₀ > 0` and every `ν > 0` with `κ := ν/μ₀`,

    ω(x, t) = −2(1 + μ₀) κ x / ( κ²(T−t)² + x² )                  (E)

as an **exact self-similar finite-time blow-up of the dissipative equation**, with
`‖ω‖_∞ = (1 + μ₀)/(T − t)` and `L = κ(T−t)` — i.e. `β = 1`, `α = 1`, `s_c = 1/2`:
critical, for every `μ₀`.

Checked in closed form (no quadrature, no differencing) against
`ω_t − ω H(ω) + ν Λω = 0` over `ν ∈ {0.05, 0.5, 2}`, `μ₀ ∈ {0.1, 1, 3}`,
`t ∈ {0, 0.5, 0.9, 0.99}`: worst relative residual **6.3e−16**. The amplitude law is
measured, not asserted: `4.0/4.0`, `20.0/20.0`, `200.0/200.0`, `1998.5/2000.0`.

**Novelty: not claimed, and (E) is at high risk of being known.** Explicit solutions of
the viscous CLM equation by complexification go back to Schochet (CPAM 1986). See
§9 and `LITERATURE_CHECK.md`. What this leg is *for* is (M) and `α₁`, not (E).

## 4. H2 — `a = 0` carries a line of viscous self-similar blow-ups

In rescaled variables (E) is the one-parameter family `Ω_μ = −(1 + μ₀) sin θ` with
`α ≡ 1` identically. So `α₁ = 0` at `a = 0`: the marginal direction is neutral **to all
orders**, and the viscous self-similar blow-ups form a line rather than a point.

Newton rediscovers it from a cold start — the "build the same object twice" gate:

| `μ` | `α` | residual | `‖Ω_num − Ω_exact‖_∞` |
|---|---|---|---|
| 0.00 | 1.00000000000000 | 1.1e−16 | 1.1e−16 |
| 0.25 | 1.00000000000000 | 1.3e−15 | 6.7e−16 |
| 1.00 | 1.00000000000000 | 8.9e−15 | 8.4e−15 |
| 4.00 | 1.00000000000000 | 1.6e−14 | 1.1e−15 |

`α₁ = −3.9e−17`. Verdict: **`neutral_line`**. *(fig37 B)*

Note what makes this a real gate rather than a tautology: the numerics do not know (E).
They solve (F_μ) with the re-derived gauge (N′) at `μ = 4`, where the dissipative term
is four times the size of everything else, and land on the closed form to `1e−15`.

## 5. H3 — `a = 1/2`, `s = 3/2`: the degeneracy does not survive, and `α₁ > 0`

At the second resonance `Λ³` is exact and `α₀ = 3.0000000000`. `α(μ)` is now genuinely
curved, and **that curvature is a trap**: a straight fit of `α` against `μ` over a finite
window returns the **chord**, not the derivative at the origin. Over `μ ≤ 0.2` the chord
is `0.1264` while the extrapolated slope is `0.1337` — a 5.5% error in the one number
the verdict is quoted from. So the secants `(α(μ) − α₀)/μ` are fitted linearly in `μ`
and extrapolated to `μ = 0` (banked lesson 52's "add rungs until the exponent stops
moving", applied to a derivative instead of a rate):

| `K` | `α₁` (extrapolated) | `α₁` (chord) | max `Λ³` truncation |
|---|---|---|---|
| 96 | 0.132770 | 0.125510 | 0.0840 |
| 144 | 0.133470 | 0.126193 | 0.0326 |
| 192 | 0.133628 | 0.126345 | 0.0169 |
| 240 | **0.133683** | 0.126396 | 0.0102 |

`K`-spread **9.1e−4**, and the `Λ³` truncation falls by 8× across the ladder while `α₁`
stops moving at the fourth digit. **`α₁ > 0`**, so the verdict is
`relaxes_to_inviscid`. *(fig37 C)*

The truncation number is worth reading rather than hiding: it is **not small** in
coefficient terms (8% at `K = 96`). What has to be true is that it *falls* with `K` and
that `α₁` stops moving anyway. Gate (8) asserts both, not just the second.

## 6. H4 — the third point is NOT REACHED, and the refusal predicate is the finding

At `a = 0.5821792673`, `α = 5`, `s = 5/2` the leg does not converge. Reported as a
failure rather than dropped, on a two-rung ladder:

| `K` | seed residual | worst branch residual | `α` drift over the `μ`-window | signal/residual | worst `Λ⁵` truncation | `α₁` it *would* have quoted |
|---|---|---|---|---|---|---|
| 192 | 7.9e−4 | 6.7e−3 | 1.2e−4 | **0.018** | 1.7e+04 | −0.004557 |
| 288 | 5.2e−6 | 3.8e−4 | **2.0e−5** | **0.052** | 1.5e+03 | −0.001703 |

Both rungs refuse. Neither reaches a signal-to-residual ratio of 1, let alone the
factor of 10 the gate asks for.

### 6a. The rung that would have shipped a sign flip

The `K = 288` rung looks respectable. Its seed matches Route-E's own ladder for this
point (`α = 5` is steeper and reaches its asymptotic regime late), and a branch residual
of `4e−4` is not obviously disqualifying. Fed to `alpha_slope` it returns

    α₁ = −0.0017    →    verdict: dissipation_runs_away

which is **the opposite sign to `a = 1/2`**, and would have been a headline: "the
marginal verdict flips at the third resonance."

It is not a measurement. The entire excursion of `α` across the `μ`-window is `2.0e−5`,
**a factor of 19 below the residual of the solve it was extracted from**. The derivative
being fitted is an order of magnitude smaller than the error bar of the quantity it is
fitted from.

**Refusing on the residual alone would not have caught this** — `4e−4` is a perfectly
ordinary residual, and the guard `worst < 1e−5` would have been the only thing standing
between this leg and a wrong sign, on a threshold chosen before the number was seen. The
predicate is now the stricter and more honest one:

    drift  >  10 × worst residual                        (is there signal at all?)

which is a different question from "did it converge", and both numbers are recorded at
every rung so the refusal can be audited rather than trusted. Gate (10) tests the
predicate against these exact numbers, including that the sign it would have quoted is a
real sign — the trap is live, not hypothetical.

### 6b. §2's "lucky alignment" was overstated, and is corrected in place

The worst `Λ⁵` truncation is `1.7e4` at `K = 192` and `1.5e3` at `K = 288`: the
coefficients the fifth power throws off the end of the basis are three to four orders
**larger** than the ones it keeps, because `Λ^p` weights mode `k` by `k^p` and so
amplifies precisely the modes the single final truncation discards.

It does fall under refinement — roughly `K^{−4}` — and that is the honest statement
rather than "refining does not help". But it starts so far above 1 that the observed rate
puts the `K` needed to make `Λ⁵` trustworthy at around **3000**, which dense linear
algebra does not reach.

So the alignment claim in §2 is real but weaker than it was written. **Landing on an
odd-integer `α` makes `Λ^{2s}` a finite matrix; it does not make the composite
accurate.** The alignment buys `p = 1` and `p = 3` and does not buy `p = 5`. The module
docstring has been corrected in place.

### 6c. What this costs the leg

`α₁` at the third resonance is **unmeasured**. The two-point trend — `α₁ = 0` at
`a = 0`, `α₁ > 0` at `a = 1/2` — has no third point holding it up, and one leg has
already been paid for reading a trend off two points (banked lesson 52). Read the sign
at `a = 1/2` as a measurement at `a = 1/2`, not as the start of a pattern.

## 7. H5 — the DSS re-ask: dissipation *does* discretize the continuum

This is the leg's most interesting negative.

Route-E shut the DSS (discretely self-similar) lane's cheapest entrance with a
mechanism, not just a null result: the only grid-converged isolated eigenvalues of the
inviscid generator are `0` and `−1`, the two exact symmetry modes; **everything else is
continuous spectrum, and a continuum has no eigenvalue to move** into `Re > 0` as a
complex conjugate pair. Critical dissipation is exactly the perturbation that could
repair that — so the question is whether the continuum discretizes, and if it does,
whether anything then moves or goes complex.

**It discretizes.** Route-E's convergence filter (coarse `K = 96` against fine
`K = 144`, tolerance `1e−3`) applied to the dissipative generator at `a = 0`, `s = 1/2`:

| `μ` | converged | max `Re λ` | max abs `Im λ` | integer ladder |
|---|---|---|---|---|
| 0.00 | 2 / 96 | +1.9e−16 | 0 | `[−1, 0]` |
| 0.10 | 2 / 96 | +1.1e−14 | 0 | `[0]` |
| 0.25 | 5 / 96 | +2.5e−14 | 0 | `[−4, −3, −2, 0]` |
| 0.50 | 6 / 96 | +3.3e−14 | 0 | `[−5, −4, −3, −2, 0]` |
| 1.00 | 6 / 96 | +2.4e−13 | 0 | `[−5, −4, −3, −2, 0]` |
| 2.00 | 7 / 96 | +3.3e−13 | 1.8e−05 | `[−6, −5, −4, −2, 0]` |
| 4.00 | 8 / 96 | +2.8e−13 | 0 | `[−7, −6, −5, −4, −3, −2, 0]` |

*(`μ = 0.10` shows an empty-looking ladder because the `−1` mode has already moved off
the integer to `−1.183216`; it is the same two converged values as `μ = 0`.)*

Turning `μ` on takes the converged count from **2 to 8** and grows a ladder of
eigenvalues sitting on the **negative integers**. That is a real structural change:
the mechanism Route-E used to shut the lane is gone.

**And the lane stays shut anyway, for a better reason.** Everything that condenses out
of the continuum lands on the negative real axis. No converged eigenvalue reaches
`Re > 0` (worst `+3.3e−13`, i.e. zero), and none is complex: the two values flagged at
`μ = 2` are a pair at `Re = −3` split by `|Im| = 1.8e−05`, a near-degenerate real pair
resolved to noise, not a Hopf. *(The driver now reports the largest `|Im|` rather than
a boolean, because the boolean read "True" for that pair — the first version of this
table would have overstated it.)*

One mode does move, and it moves the wrong way for a bifurcation. The amplitude mode
sits at

    λ_amp(μ) = −√(1 + 4μ)                                          (measured)

to **2.1e−09** across the whole `μ`-ladder. At `μ = 0` this is Route-E's exact symmetry
eigenvalue `−1`; dissipation breaks the amplitude symmetry (rescaling `ω` changes the
effective size of `ν`), which frees that eigenvalue to move — and it moves **left**. The
amplitude mode becomes *more* stable. **This formula is an empirical fit to six digits
and is not derived**; it is in the module because it is gated, not because it is
understood.

The absence claim has a positive control (banked lesson 47): planting a localized
potential in the same dissipative generator takes the filter from **6 converged
eigenvalues to 9, one of them at `Re = +1.58`**. So "nothing crosses" is a measurement
and not a filter that cannot see. *(fig37 D)*

## 8. H7 — the cross-check, through unrelated machinery

At `s = 1/2` exactly the prediction from (M) is `λ_μ = 0`, i.e. the time-dependent
`D/N ~ (T−t)^p` fit should return `p = 0`. That fit lives in a completely different
instrument: periodic pseudo-spectral, RK4, integrating factor, fitted singular time.
Nothing about the compactified steady solve enters it.

At `n = 8192` (Route-F's resolution):

| `ν` | `T` (inviscid 3.33333) | `p` over three windows | mean `p` | reached |
|---|---|---|---|---|
| 1e−2 | 3.37331 | +0.024 / −0.001 / −0.015 | +0.003 | 0.99965 `T` |
| 1e−3 | 3.33716 | +0.037 / +0.005 / −0.011 | +0.010 | 0.99966 `T` |
| 1e−4 | 3.33380 | +0.035 / +0.001 / −0.017 | +0.006 | 0.99969 `T` |

Mean `p = +0.006`, spread across `ν` **0.007**, against a prediction of exactly `0` —
and the window spread within each `ν` (~0.04) is larger than the deviation from zero, so
**the honest error bar is the fit window, not the residual bias**.

**The caveat, stated rather than buried:** every one of these runs ends
`under_resolved`. The solver refuses to integrate past its spectral-tail criterion
rather than return a number off an unresolved state (banked lesson 45). What softens it
is the `reached` column, which is recorded for exactly this reason: each trajectory gets
to **99.97% of the fitted singular time** before refusing, so "stopped short" here means
stopped short by three parts in ten thousand, not stopped early. It is still a
cross-check with a stated limitation rather than a clean confirmation. *(fig37 E)*

## 9. Novelty and literature risk

**Not claimed for (E).** Explicit solutions of the viscous CLM equation by
complexification go back to Schochet, CPAM 1986; the relevance exponent for dissipative
gCLM is reported in arXiv:1908.09385 / arXiv:2207.07548. Route-F's `s_c` already sits at
high risk of being pre-empted by the latter (see `LITERATURE_CHECK.md` §3 and the third
pass), and Route-H's `λ_μ = 2s − α₀` is the same statement in spectral clothing — so it
inherits that risk in full.

**What is plausibly new here is methodological**, and remains **unchecked** because PDF
access is still blocked:

1. **`μ` as an autonomous variable of the rescaled flow**, turning a scaling threshold
   into a stability eigenvalue and the marginal case into a quadratic normal form with
   one coefficient. Whether this is standard in the dynamic-rescaling literature is
   exactly the kind of thing that would be obvious to someone in the field.
2. **`α₁ = dα/dμ` as the marginal invariant.** The sign is the whole verdict.
3. **The observation in §7** — that critical dissipation discretizes the inviscid
   continuum onto the negative integers without producing anything that could cross.

Item 3 is the one worth a specialist's five minutes; items 1 and 2 should be presumed
known until someone checks.

## 10. Where this sits relative to Clay

**It moves no link of the L1→L4 chain.** Three honest statements about what it does do:

- It converts Route-F/G's stopping point into an answerable question in a toy model, and
  answers it there: at criticality `μ` decays **algebraically**, `μ ~ 1/(α₁τ)`, so a
  critical viscous solution relaxes onto the inviscid profile — but impossibly slowly.
  With `α₁ = 0.1337`, taking `μ` from 0.2 to 0.02 costs `τ = 337` and to 0.002 costs
  `τ = 3703`, and `τ` is itself logarithmic in `(T−t)`. Each decade costs nine times the
  last, because the linear term is gone. *(fig37 F)*
- It removes Route-E's *mechanism* for shutting the DSS lane (`μ > 0` does discretize
  the continuum) while leaving the lane shut on the direct evidence. That is a strictly
  better epistemic position than before: the negative now rests on a measurement with a
  positive control rather than on "there is nothing there to measure".
- It is a **toy**. `s = 3/2` is hyperviscosity, used because it is where criticality can
  be posed exactly, not because it resembles NS. (E) decays like `1/x` and is therefore
  **not finite energy** — the honest analogy to Nečas–Růžička–Šverák, whose theorem
  excludes exactly self-similar NS blow-up in the finite-energy class, and whose escape
  route is precisely the slowly-decaying non-`L²` profiles Jia–Šverák constructed. (E)
  is the toy analogue of the escaping class, **not** a counterexample to NRS.

## 11. Reproduce

```
.venv/bin/python test_critical_dissipation.py                       # 10/10, ~4 min
.venv/bin/python -u experiments/p2_route_h_v1_critical.py           # ~8 min -> JSON
.venv/bin/python writeup/4_p2_lottery/p2_route_h_v1_evidence.py     # fig37 from JSON
```

Gates: `Λ` exact three ways (closed-form conjugate-Poisson identity to `1e−15`,
`Λ² = −d²/dX²` against a differently-built second derivative, and an independent
line-grid Hilbert transform); `μ = 0` reproduces Route-E **bit for bit**; the Jacobian
including (N′)'s quotient term; (E) against the PDE in closed form; Newton rediscovering
(E) from a cold start; the **sign** of the marginal verdict as a test in words, because
"more dissipation ⇒ more dissipation" is the reflex reading and it is backwards;
`α = −c_ω` still being the far-field exponent with dissipation on; the `a = 1/2`
`K`-ladder; and the positive control for the spectral filter.
