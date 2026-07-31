# Route-D v12 — the profile ends: Y₀ in the bounds' own basis

**Status: Level-1 tooling + a structural finding that re-specifies the target.
NOT a certificate, NOT rigorous, NOT a Clay result.** Plain float64.

> **CORRECTION (Route-D v13).** §6 below attributed the `‖A‖` divergence to a
> homogeneous mode `~ (X_c − X)^{−1/a}`. That is **wrong** — a sign dropped in
> converting `d/dX` to `d/ds`; the mode at `X_c` *vanishes* like
> `(X_c − X)^{+1/a}` and nothing is singular there. The measurements in this
> document stand; the mechanism is corrected in
> [TECHNICAL_P2_ROUTED_V13.md](TECHNICAL_P2_ROUTED_V13.md), where the obstruction
> turns out to be a **growing far-field mode** `~ (log(X/X_c))^{1/a}` against a
> domain space that is a decay class. The offending passages below are marked.

**Figure:** `fig30` · **Data:** `writeup/data/p2_route_d_v12_defect.json`
**Code:** `solver/collocation_newton.py` (+ `test_collocation_newton.py`, 6/6),
`experiments/p2_route_d_v12_defect.py`, `p2_route_d_v12_evidence.py`

---

## 0. Why this leg

v11 put Newton on the two-scale profile equation and killed the ~1e-2 residual
floor that five legs had carried as a fact about the problem. It ended with one
instruction: **that measurement is in the wrong discretization.** It was made on
the Route-A sinh-`ρ` grid; every Route-D bound — `‖A‖`, `C_Q`, `Z₁`'s far-field
piece — is written in the compactified midpoint `θ`-collocation basis of
`solver/decay_collocation.py`, where `X = tan(θ/2)`. `Y₀` is the defect measured
*there*, in the codomain norm of *that* space. Carry the profile across and
measure it.

This leg does that. The carry-over is a build; the measurement is the point; and
the measurement found something else.

## 1. The build — the `a`-term in the compactified basis

`decay_collocation` is exact at `a = 0`: on even trigonometric polynomials of
degree `< J`, `H(cos kθ) = sin kθ`, `d/dθ` and `d/dX = (1+cos θ) d/dθ` are all
exact, so `DF` is a dense `J×J` matrix with no quadrature. The `a`-family adds a
transport term built from the velocity `U(X) = ∫₀^X H(Ω) dX'`, the one object
that is not local in the coefficients. It has a closed form. With
`Ω = Σ A_k cos kθ` we have `H(Ω) = Σ A_k sin kθ` and `dX = dθ/(1+cos θ)`, so
`U = Σ A_k I_k(θ)` with

```
I_k(θ) = ∫₀^θ sin(kt)/(1+cos t) dt ,
I_0 = 0 ,   I_1 = log(2/(1+cos θ)) = log(1+X²) ,
I_{k+1} = 2(1 − cos kθ)/k − 2 I_k − I_{k−1}
```

(from `2 sin kt cos t = sin(k+1)t + sin(k−1)t` with `cos t = (1+cos t) − 1`). So
the velocity is a dense matrix on coefficients, assembled once — and, the part
that matters here, **evaluable at any `θ`, not only at grid nodes.**

The recursion's homogeneous solutions are `(A + Bk)(−1)^k` and `I_k` itself grows
like `2k log(1/(π−θ))` near the outer endpoint — the same rate, so the relative
error is controlled but the absolute error tracks `ε k²`. In float64 that is
**1.7e-11 by `k = 800`**, so the assembly runs in longdouble and casts down (gate
1 measures both). Gate 2 is the strong one: at `a = 0` the module reproduces
`decay_collocation` bit for bit, and the exact anchor — which solves the equation
identically — has residual **1.8e-12 on the nodes and 1.9e-12 between them**,
which is the only check the off-node evaluator gets, and a demanding one.

## 2. Newton in the certificate's own coordinates

`gauged_jacobian` builds `M = [gauge row ; DF rows except one]` with the speed `c`
**fixed**, and `A = M⁻¹` is the approximate inverse every Route-D bound has been
about. The Newton iteration for that same square system is `x ← x − A F(x)`:
**the certificate's `A` is the Newton matrix, and `Y₀ = ‖A F(x̄)‖` is the size of
the Newton step at the profile we hand over.** Fixing `c` is what makes the system
nonsingular — the zero set carries two symmetries at every `a`, scaling
`(Ω,c) → (λΩ, λc)` and dilation `Ω(X) → Ω(X/μ)` with `c → μc` (the `a`-term is
dilation invariant because `U` picks up the `μ` that `Ω_X` loses), and fixing `c`
kills the second while the gauge row kills the first.

That framing sets up the trap the leg is really about. **A Newton solve zeroes the
residual at the nodes.** The certificate does not ask about nodes: `F(x̄)` is the
residual of the *interpolant*, as a function on `(0,π)`. `Ω H(Ω)` is a product of
two degree-`<J` trigonometric polynomials, hence degree `< 2J`, and collocation
imposes `J` conditions on it. The rest is aliasing, invisible to the solve by
construction, and it is what `Y₀` is made of.

## 3. T1/T2 — the measurement

`J = 400`, `c = 0.5`, operating point `(α, γ) = (1.4, 0.15)`. The rows Newton
enforces go to **1.5e-13 – 2.4e-13 at every `a`**, exactly as advertised. The one
row the gauge displaced does not:

| a | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|
| rows enforced | 1.5e-13 | 1.6e-13 | 2.4e-13 | 1.9e-13 | 1.6e-13 | 1.5e-13 |
| row displaced | 7.1e-13 | 4.8e-7 | 4.5e-7 | 9.3e-5 | 3.3e-3 | 9.1e-3 |

At `a = 0` both are roundoff, because the anchor is an exact solution — that is
the control. At `a > 0` they differ by six to ten orders. **Zero at the nodes is
not zero as a function**, and the gap is not a subtlety at the margin.

In the codomain norm the picture is worse, because that norm weights the far
field by `(1+X²)^{(α+1)/2}`:

| a | 0 (control) | 0.05 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|---|
| `‖F‖_Y` | 3.7e-11 | 4.4e-4 | 8.4e-6 | 4.4e-5 | 1.5e-2 | 7.9e-1 | 1.7e0 |
| `Y₀ ≤ ‖A‖·‖F‖_Y` | 7.7e-10 | 9.3e-3 | 1.8e-4 | 9.2e-4 | 3.1e-1 | 1.7e1 | 3.5e1 |
| × budget 2.45e-4 | 0.000003 | 38 | 0.7 | 4 | 1256 | 67000 | 143000 |

(`‖A‖ ≤ 20.94`, v10 W2 at the same point. The exact-anchor control at 3.7e-11
says the measurement floor is nine orders below anything reported here.)

Two things stand out. The sequence is **not monotone** in `a` — 4.4e-4, then
8.4e-6, then 4.4e-5 — and the arg-max of the weighted defect is **the outermost
evaluation point, at every single `a`**. Both are symptoms of the same thing, and
it is not a numerical detail.

## 4. T3 — why: the profile ends at a finite radius

The far field of this equation is governed by one balance. With
`E(X) = c + a U(X)` the residual is `Ω H(Ω) − E Ω_X`, and for large `X`,
`H(Ω) → m/(πX)` with `m = ∫Ω dX < 0`.

* **At `a = 0`,** `E ≡ c` is constant, and `Ω·m/(πX) = c Ω_X` integrates to
  `Ω ~ X^{m/(πc)}`. For the anchor `m = −π`, `c = ½`, giving exactly `X⁻²` — the
  decay the whole graded-space programme was built around, and the source of the
  `α = 2` resonance v3 found in the far-field solution operator `2/|α−2|`.
* **At `a > 0`,** `U` inherits the Hilbert transform's logarithm:
  `U(X) = U₀ + (m/π) log X + o(1)`, which **decreases without bound**. So `E`
  crosses zero at a finite radius, `log X_c ≈ π(c + aU₀)/(a|m|)`, i.e.
  `X_c ≈ e^{c/a}` evaluated with the anchor's own `m = −π`, `U₀ = 0`.

Near that radius the balance changes character. Write `s = X_c − X`; then
`E(X) ≈ −a h_c s` with `h_c = H(Ω)(X_c)`, and `Ω = A s^p` gives

```
   A s^p h_c   =   (−a h_c s)(−p A s^{p−1})   =   a h_c p A s^p
   ⇒   a p = 1   ⇒   p = 1/a
```

— **an algebraic zero of order `1/a`, with no free constant**: `A` and `h_c`
cancel. Beyond `X_c`, `Ω ≡ 0` solves the equation exactly (`H(Ω)` is not zero
there, but every remaining term carries a factor of `Ω` or `Ω_X`). So the `a > 0`
two-scale profile **ends**, and the `a = 0` anchor with its `X⁻²` tail is the
degenerate `X_c = ∞` limit of that picture.

Measured, in two independent discretizations (`θ`-collocation with `c` fixed, and
the sinh-`ρ` build of v11 with `c` free and two gauges — different family members,
so they are compared through the dilation invariant `X_c/c`):

| a | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|
| `X_c/c` (θ, J=800) | 576.8 | 34.33 | 12.257 | 6.985 | 4.846 |
| `X_c/c` (ρ, n=801) | 560.1 | 34.31 | 12.243 | 6.985 | 4.846 |
| gap | 3.0% | 0.06% | 0.11% | 0.00% | 0.01% |
| fitted zero order `p` | — | 5.40 | 3.59 | 2.73 | 2.20 |
| predicted `1/a` | 10 | 5 | 3.33 | 2.50 | 2.00 |

The fitted exponent sits **7–9% above `1/a` uniformly**, which is what a
leading-order fit over a finite window should do (the next-order correction is
positive); the prediction itself has no fitted constant in it. The `a = 0.1`
column is where the compactified grid stops resolving `X_c ≈ 290` — the 3% gap is
the instrument, and the `p` fit there has two usable points and is reported as
`nan` rather than dressed up. Refinement `n = 801 → 1601` moves `X_c/c` by 3e-5
(a=0.3) and 0 (a=0.5).

**This is what the T2 anomalies were.** A compactly supported function
represented in a *global spectral basis* leaves Gibbs-type oscillation where it
should be identically zero, and the codomain weight `(1+X²)^{(α+1)/2}` amplifies
precisely that region — hence the arg-max at the outermost point, always. And the
non-monotonicity in `a` is the moment `X_c` crosses into the grid: at `a = 0.05`,
`X_c ≈ e^{10} ≈ 2e4` is far outside the domain (`X_max ≈ 4J/π ≈ 509`) and the
profile still looks like a tail that is being truncated; by `a = 0.1`,
`X_c ≈ 290` is inside, and the object being represented has changed.

## 5. T4 — the rate, and the one number that goes the right way

`‖F‖_Y` against `J`, and the budget line it must get under:

| a \ J | 100 | 200 | 400 | 800 | 1600 | fitted | predicted |
|---|---|---|---|---|---|---|---|
| 0.2 | 1.2e-3 | 1.7e-4 | 4.4e-5 | 1.1e-5 | **1.5e-6** | `J^−2.31` | `J^−6` |
| 0.3 | 3.7e-2 | 2.0e-2 | 1.5e-2 | 1.0e-2 | 1.5e-3 | `J^−1.02` | `J^−4.33` |
| 0.4 | 9.2e-1 | 7.3e-1 | 7.9e-1 | 8.1e-1 | 7.6e-1 | `J^−0.04` | `J^−3.50` |

The naive prediction — aliasing of a `C^{1/a}` function, `J^−(1/a+1)` — is wrong
everywhere, and wrong in the informative direction: convergence is far *slower*
than the profile's own regularity would give, because the error being measured is
not the aliasing of the zero, it is the far-field oscillation left over from
representing a compactly supported function globally. At `a = 0.4` it **does not
converge at all** over a 16× range in `J`.

The one number that goes the right way is `a = 0.2`:

> `Y₀ ≤ ‖A‖·‖F‖_Y = 2.37e-4` at `J = 800` and **3.17e-5 at `J = 1600`, against a
> budget of 2.45e-4** — 7.7× under. That is the first time in this project that
> the defect side of the inequality has been under budget at `a ≠ 0`.

Section 6 is why that sentence does not mean what it looks like.

## 6. T5 — the operator does not transfer

Every constant in the budget was computed by linearizing at the `a = 0` anchor.
The certificate linearizes at the profile it certifies. The graded sup-to-sup
induced norm of the gauged inverse (v4's W1/W2 measurement — an *exact* induced
norm between discrete sup norms, so v6's discrete-ball trap does not apply), at
`J = 400`, `α = 1.4`:

| a | 0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 |
|---|---|---|---|---|---|---|
| `‖A‖` | 3.54 | 3.88 | 2.1e3 | 7.6e4 | 5.0e5 | 1.6e7 |
| `cond(M)` | 1.4e6 | 1.7e6 | 1.7e6 | 2.1e6 | 2.4e6 | 1.8e7 |

`cond(M)` barely moves, so this is not the raw conditioning of the matrix; it is
the *weighted* norm. And a single `J` cannot tell a large operator from a grid
artifact, so the ladder is the measurement that decides:

| `‖A‖` at `α=1.4` | J=200 | J=400 | J=800 | fitted |
|---|---|---|---|---|
| a = 0 (anchor) | 3.551 | 3.542 | 3.537 | **`J^−0.003`** |
| a = 0.2 | 292 | 2.1e3 | 1.5e4 | **`J^+2.86`** |
| a = 0.3 | 1.1e4 | 7.6e4 | 5.0e5 | **`J^+2.75`** |

**At the anchor the norm is flat to three decimal places over a 4× refinement;
at the real profile it diverges like a power of `J`, measured with the same
code.** The approximate inverse the whole Route-D programme is built on does not
exist in the limit at `a > 0`.

It has a mechanism. ~~Linearizing about a solution with a
zero of order `p` at `X_c` gives a homogeneous solution `~ (X_c − X)^{−p}`:~~
**[CORRECTED by v13 — the sign is wrong; see the banner. The derivation below
drops a sign in `h_X = −h_s`, and the correct local mode is `s^{+1/a}`, which
vanishes. The real obstruction is the growing far-field mode.]**

```
   h_X / h  =  H(Ω)/E  ≈  h_c / (−a h_c s)  =  −1/(a s)     ⇒   h ~ s^{−1/a}
```

which is in no sup norm at all. **The linearized operator at the true `a > 0`
profile has a genuine singular mode at the critical radius**, and `‖A‖` is
measuring how much of it the grid can see — which is why it grows with `J` rather
than settling, and why the `a = 0.1` value (3.9) is small: there `X_c ≈ 290` is
barely resolved and the grid cannot see the mode at all. The measured exponent
(`J^+2.8`) is not `1/a`; the weights enter too, and this leg does not claim a
rate, only the divergence and its source.

So the `a = 0.2` result reads as follows. `Y₀ ≤ 3.2e-5` used `‖A‖ ≤ 20.94`. The
measured `‖A‖` at that profile is `2.1e3` — a hundred times larger — and the
budget scales like `1/‖A‖`, so the honest comparison is `Y₀ ≈ 3e-3` against a
budget of roughly `2e-6`. **Both sides move the wrong way, by the same
mechanism.** The near-miss at `a = 0.2` is an artifact of pricing a new object
with an old object's constants.

## 7. T6 — the survival boundary: a candidate mechanism, and the control that
## refuses to confirm it

`X_c(a)` from the sinh-`ρ` build (`n = 801`), against the profile's own core
half-width:

| a | 0.25 | 0.30 | 1/3 | 0.35 | 0.40 | 0.45 | 0.48 | 0.50 | 0.52 | 0.55 | 0.60 | 0.70 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `X_c` | 10.63 | 7.13 | 5.78 | 5.29 | 4.24 | 3.55 | 3.25 | 3.08 | 2.93 | 2.74 | 2.48 | 2.12 |
| `p` fitted | 4.24 | 3.55 | 3.23 | 3.07 | 2.69 | 2.41 | 2.26 | 2.18 | 2.12 | 2.00 | 1.84 | 1.56 |
| `X_c`/half-width | 10.7 | 7.16 | 5.80 | 5.31 | 4.25 | 3.57 | 3.27 | 3.09 | 2.95 | 2.75 | 2.49 | 2.13 |

Two readings were on the table. **Geometric:** the outer scale `X_c` descends
toward the core, and when the support radius reaches the profile's own width
there is no two-scale structure left. **Arithmetic:** the zero order is `1/a`,
which passes through the integer `2` exactly at `a = 1/2`, and the Hilbert
transform of `(X_c−X)^p_+` grows a logarithm at integer `p` — which would break
the ansatz at exactly the four-times-confirmed boundary `a* ≈ 0.5`.

They differ at `a = 1/3`, where `p = 3` is also an integer but `X_c ≈ 5.8` is
still well outside the core. **The control says the arithmetic reading is wrong:
`a = 1/3` sits smoothly between its neighbours in every column.** So the
tempting coincidence is a coincidence.

What survives is the geometric statement, and it is a trend rather than a
threshold: `X_c` falls monotonically and smoothly through `a*`, with nothing
special happening at 0.5. That is consistent with what §9-cont2 already
established by other means — the crossing is **soft** — and it explains where the
outer scale comes from and why it shrinks, but **it does not predict `a*`**. The
leg gets a mechanism for the two-scale structure and does not get the boundary.

## 8. Ledger, gate-check, and the honest reading

**LEDGER.** Nothing moved from OPEN to BOUNDED this leg. What changed is the
specification: `Y₀` is now measured in the right basis, and the space itself
joins the open list.

* EXACT: `Y₀` (as a *measurement*, in the certificate's basis — not a bound).
* BOUNDED (at the `a = 0` anchor, unchanged): `Z₀`; `Z₁` far-field modelling
  error; `‖A‖` sup part; `‖A‖` seminorm part; `C_Q` sup part; `C_Q` codomain
  seminorm part.
* OPEN: `Z₁` core↔far coupling; `Z₁` core discretization; discrete↔continuum
  transfer; **and, new: every bounded constant above is a constant for the
  ANCHOR's linearization, and T5 shows they do not transfer to the profile the
  certificate would be about.**

**GATE-CHECK (a) which link does this move?** L1, and sideways: it does not make
a certificate closer, it shows that the object being certified is not the object
the space was designed for. That is worth a leg on its own terms — a
misspecification found by measurement is cheaper than one found after a hardening
attempt — but it is not progress up the ladder, and nothing here is rigorous.

**(b) is another L1 leg the best use of the next chunk?** The answer is genuinely
different from what it was before this leg, because the repair is concrete and
it is *cheaper* than what it replaces:

> Beyond `X_c` the profile is exactly zero. A certificate could work on the
> **finite interval** `[0, X_c]` with `X_c` as an unknown, and the far field —
> eleven legs of decay grading, resonances, and tail bounds — is handled in
> closed form because there is nothing there. ~~The price is the interior
> singularity at `X_c`, and the standard reason to expect that price to be
> refundable is that the singular mode `s^{−1/a}` is precisely `∂/∂X_c` of the
> solution family.~~ **[CORRECTED by v13: there is no interior singularity, and
> bordering with the speed is disqualified because dilation is a symmetry. The
> reason the finite interval is the right repair is simpler — the obstruction is a
> growing mode in the far field, and on `[0, X_c]` the far field is not in the
> domain at all.]** Untested, and it is the obvious v13.

**(c) a cheaper experiment that kills the route?** Yes, and it is now specific:
solve the free-boundary formulation at one `a` and measure `‖A‖` against `J`. If
the singular direction is *not* absorbed by the free boundary, `‖A‖` keeps
growing with `J` and the whole Route-D framing needs replacing rather than
repairing.

**HONEST CEILING (unchanged).** Plain float64; nothing interval-enclosed; nothing
rigorous. Even the eventual success this scouts is a computer-assisted toy-model
certification, not a Clay result. What v12 adds to that is not comfort: it says
the certificate this project has been pricing for eleven legs was priced at the
wrong point.
