# Route-D v14 — the two-scale profile equation has a first integral

*Phase-2 P2, Route-D leg 14. Figure: `writeup/figures/fig32_route_d_v14_first_integral.png`.
Data: `writeup/data/p2_route_d_v14_first_integral.json` (rebuild the figure with
`writeup/4_p2_lottery/p2_route_d_v14_evidence.py`; regenerate the data with
`experiments/p2_route_d_v14_first_integral.py`, ~6 min, deterministic).
Code: `solver/first_integral.py` + `test_first_integral.py` (11/11; suite 21 files green).*

**Rigor level: 1 (a novel numerical map) plus one exact algebraic identity.
Nothing here is interval-enclosed, nothing is a certificate, and nothing is a Clay
result.** See the honesty section at the end.

---

## 0. The one-line summary

Thirteen legs treated

    R = Ω H(Ω) − c Ω_X − a U Ω_X = 0 ,      U(X) = ∫₀^X H(Ω) dX'      (P)

as a nonlinear integro-differential equation on the whole line, to be discretized and
inverted. It is not one. Writing `E = c + a U` for the effective transport coefficient
v12 introduced, `E_X = a H(Ω)` **exactly**, so wherever `Ω ≠ 0`

    R = 0  ⟺  Ω E_X / a = E Ω_X  ⟺  (log|Ω|)_X = (1/a)(log E)_X

and therefore `|Ω| = C E^{1/a}`. The amplitude gauge `Ω(0) = −1` fixes `C = c^{−1/a}`
(at `X = 0`, `U = 0` and `E = c`), giving

> **Ω(X) = − ( E(X) / c )^{1/a} ,   E = c + a U ,   U_X = H(Ω).**   (FI)

That is an exact first integral of (P). Three legs' worth of structure falls out of it
in one line each, and — the point of the leg — it makes the **kill switch** the
continuation prompt has been asking for cheap enough to just run.

**The kill switch passes.** Posed on `[0, X_c]` via (FI), the approximate inverse that
v12 measured diverging as `J^+2.86` is **flat**: `K^−0.0009 … K^+0.0011` over
`K = 48…192`, at every `a` tested, and unchanged under the decay grading the whole-line
measurement used.

---

## 1. Why it is a first integral, and what gates it

Nothing above assumes anything about `Ω` beyond `Ω ≠ 0` and `E ≠ 0` on the interval.
Three independent gates:

**(a) The `a → 0` limit IS the exact anchor.** `(1 + aU/c)^{1/a} → exp(U/c)`, so (FI)
degenerates to `Ω = −exp(U/c)`. On the anchor `U = −½ log(1+X²)`, `c = ½`, hence
`exp(U/c) = 1/(1+X²)` and `Ω = −1/(1+X²)` — **exactly** the known solution the whole
project is anchored on. Measured max error over `X ∈ [0,200]`: **1.11e−16**. The
finite-`a` form approaches it at the predicted `O(a)` (fitted `a^1.011`).

**(b) On a discretization that knows nothing about it.** `|Ω|/E^{1/a}` should be
constant. On the whole-line θ-collocation profiles of `solver/collocation_newton` the
relative spread over the core is

| J | 200 | 400 | 800 | 1600 |
|---|---|---|---|---|
| a=0.2 defect | 5.85e−8 | 2.56e−9 | 2.33e−10 | **1.00e−11** |
| a=0.2 profile residual | 1.81e−6 | 1.12e−7 | 1.44e−8 | 8.73e−10 |
| a=0.3 defect | 2.28e−6 | 5.34e−7 | 1.15e−7 | **5.14e−9** |
| a=0.3 profile residual | 6.23e−5 | 2.30e−5 | 7.08e−6 | 4.46e−7 |

The defect is an order of magnitude *below* the profile's own residual at every `J` and
falls **faster** (×251 vs ×126 at `a=0.2`; ×20 vs ×9 at `a=0.3`). That is the signature
of an exact identity evaluated on an approximate object: what is being measured is the
profile, not the identity. This is the test-suite gate, deliberately written as a *rate*
rather than a threshold, because a threshold would only have measured the profile.

**(c) The reconstruction solves the original equation.** Take the reduced solution,
rebuild `Ω`, and evaluate `R` itself with an independent quadrature at points that are
not collocation nodes: `max|R|` = 6.8e−7 → 4.3e−8 → 2.7e−9 → **1.9e−10** as the `U`
quadrature refines, fitted `n^−1.98` — converging at the trapezoid's own second order,
i.e. to zero.

---

## 2. What (FI) says without any computation

**The profile ends, and it is forced rather than discovered.** `E` is decreasing
wherever `H(Ω) < 0`, so it reaches zero at a finite `X_c`; beyond it `E < 0` and
`E^{1/a}` is not real, so `Ω ≡ 0`. With `Ω ≡ 0` outside, `H(Ω)` out there is still
negative (the mass inside is negative), so `E` stays negative and the situation is
self-consistent. v12 found the support edge by noticing a sign change in a measured
quantity; here it is a consequence.

*Caveat, stated rather than hidden:* the step needs `H(Ω) < 0` for `X > 0`, which holds
on every solution found here and is what the solve returns, but proving it a priori for
all admissible `Ω` is a separate lemma this leg did not attempt.

**The zero has order `1/a`, with the amplitude explicit.** `E` vanishes *linearly* at
`X_c` (`E_X(X_c) = a H(Ω)(X_c) ≠ 0`), so `Ω ~ −A (X_c − X)^{1/a}` with
`A = (2 s(1)/X_c)^{1/a}` computable from the solution — v12 got the exponent from a
leading balance and called the amplitude free; (FI) gives both. Measured edge exponents
against `1/a`:

| a | 0.25 | 0.30 | 0.40 | 0.50 | 0.80 |
|---|---|---|---|---|---|
| fitted | 4.000019 | 3.333350 | 2.500014 | 2.000013 | 1.250017 |
| `1/a` | 4 | 3.333333 | 2.5 | 2 | 1.25 |

(relative error ≤ 1.4e−5; v13's independent whole-line instrument got 0.02–0.6%.)

**The profile is only finitely smooth.** `Ω ∈ C^{1/a}` at the edge and no better. It is
a `C¹` (hence classical) solution exactly while `a < 1`; at `a = 1` — De Gregorio — the
edge is a **corner**, and for `a > 1` it is a cusp with `Ω_X → ∞` there (the equation
still holds in the limit, since `E Ω_X ~ s^{1/a} → 0`, but the solution is classical
only away from `±X_c`). Flagged as an observation, not a claim: whether the loss of `C¹`
exactly at De Gregorio is meaningful needs the literature check, not another leg.

---

## 3. The reduced system, and why it converges where the direct build did not

Scale by the radius, `v = X/X_c`, `e(v) = E(X_c v)/c`. The finite Hilbert transform is
scale invariant, so `X_c` drops out of `H` and the whole problem is scalar:

    c e'(v) + a X_c · Hpv[ e^{1/a} ](v) = 0 ,   e(0) = 1 ,   e(1) = 0 ,
    Hpv[w](v) = (1/π) p.v. ∫_{−1}^{1} w(|u|)/(v−u) du .                     (RS)

`c` enters only as a scale (dilation sends `X_c → μX_c`, `c → μc` and leaves `e`
alone), so the module fixes `c = 1` and every radius reported is the invariant `X_c/c`.

Two structural facts are why this works, and both are worth carrying forward:

1. **`e(1) = 0` goes in the ansatz, not in an extra row.** `e = (1−v²) s(v)` with `s` an
   even Chebyshev series. The support edge is exact by construction, and the order-`1/a`
   zero of `Ω = −e^{1/a}` is an **output** — not something a grid has to resolve and not
   something put in by hand. (The WIP direct build `solver/finite_support.py` put
   `(1−v²)^{1/a}` in the ansatz by hand, which is the same thing only if you already
   know `1/a`.)
2. **The edge row is non-degenerate.** The raw residual `R` is identically zero at `X_c`
   — every term carries `Ω` or `Ω_X`, both of which vanish — so a collocation row there
   carries no information, and a direct build must append an ad-hoc free-boundary
   condition. (RS) has `c e'(1) = −a X_c Hpv[w](1)` with both sides nonzero: **the free
   boundary is priced by the equation itself.**

`solver/finite_support.py` is the direct build. It never converged (residual 1.4 after
59 iterations at `a=0.3`). (RS) converges from a **cold start** — `s ≡ 1`, `X_c⁰ = 10`
regardless of `a` — in **5–10 Newton iterations to residual ~1e−14**, at every `a` from
0.2 to 1.2. That difference is the whole content of items 1–2.

Numerics: the p.v. is taken by one subtraction against the exact
`p.v. ∫_{−1}^{1} du/(v−u) = log((1+v)/(1−v))`, and the resulting integrand — analytic in
`(−1,1)` with an algebraic branch point of order `1/a` at each end — is integrated by
composite Gauss–Legendre on geometrically graded panels. Gated against the exact airfoil
family `(1/π) p.v. ∫ √(1−u²) U_{n−1}(u)/(v−u) du = T_n(v)`: **5.3e−14** at the default
rule. That gate is deliberately harsher than anything the module meets (`√` is endpoint
order ½; the profiles are `1/a ≥ 2`, where the same rule is at machine precision by
8 grading levels).

**Cross-build check.** `X_c/c` against the whole-line collocation profile's own zero
crossing of `E`: **3.9e−6 / 4.3e−6 / 7.3e−5** at `a = 0.3 / 0.4 / 0.5`. v12's two
independent discretizations agreed on this invariant to 0.06–0.11%; these agree to four
to five significant figures. And in its own `K` the reduced radius is converged to
**3.7e−13** over `K = 64…192`.

---

## 4. THE KILL SWITCH

The question the continuation prompt posed: v13 attributed the whole-line divergence to
a mode growing like `(log(X/X_c))^{1/a}` **outside** `X_c`, against a domain space that
is a decay class — a codimension-1 range obstruction that no refinement and no bordering
with a symmetry touches. The repair it named was to take the far field out of the
*domain*. (RS) does exactly that: its unknowns are `(s, X_c)` and its perturbations live
on `[0, X_c]` only, so the growing mode has nowhere to live.

`‖A‖ = ‖M⁻¹‖`, sup-to-sup, with the domain pushed through to function values on a fixed
fine grid (a coefficient vector is not a function space) and the `X_c` slot measured
relative to `X_c`:

| a | K=16 | 24 | 32 | 48 | 64 | 96 | 128 | 192 | slope (K≥48) |
|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 6.274 | 7.426 | 7.528 | 7.320 | 7.301 | 7.299 | 7.304 | 7.306 | **K^−0.0009** |
| 0.3 | 4.528 | 4.505 | 4.508 | 4.513 | 4.518 | 4.518 | 4.519 | 4.520 | **K^+0.0009** |
| 0.4 | 3.063 | 3.060 | 3.062 | 3.068 | 3.070 | 3.072 | 3.071 | 3.073 | **K^+0.0010** |
| 0.5 | 2.207 | 2.206 | 2.208 | 2.213 | 2.214 | 2.215 | 2.215 | 2.216 | **K^+0.0011** |

The control, **measured with the same code and the same decay grading that produced
v12's number** (`solver/turning_point.graded_norm_by_radius`, α=1.4):

| whole line | J=100 | 200 | 400 | 800 | slope |
|---|---|---|---|---|---|
| a = 0.0 (anchor) | 3.566 | 3.551 | 3.542 | 3.537 | **J^−0.004** |
| a = 0.2 | 46.06 | 292.1 | 2125 | 15350 | **J^+2.800** |
| a = 0.3 | 1520 | 1.10e4 | 7.57e4 | 4.98e5 | **J^+2.785** |

which reproduces v12 (`J^−0.003` at the anchor, `J^+2.86` at `a=0.2`) closely enough to
confirm it is the same object.

**Two honesty items that the leg would be worth less without.**

*The `a=0.2` full-ladder slope is `K^+0.0308`, not `−0.0009`.* Both are reported. The
difference is entirely the `K=16` point (6.27), which is under-resolved: at `a=0.2` the
support radius is `X_c/c = 34.3` while the core half-width stays `O(1)`, so the reduced
variable `v` carries a boundary layer of width `~1/X_c` and needs `K ≳ X_c` to see it.
From `K=48` the row is flat to four digits. The two-scale structure of the problem shows
up in the reduced formulation as a resolution requirement, and it is why small `a` costs
more modes.

*The flatness is not an artifact of choosing an unweighted norm.* Repeating the ladder
with the decay grading `w_dom = (1+X²)^{α/2}`, `w_cod = (1+X²)^{(α+1)/2}` at the
operating `α = 1.4` gives `K^−0.0030 / +0.0008 / +0.0011 / +0.0013` — the same verdict.
It has to: on a **compact** interval every such weight is bounded above and below, so it
can change the value but not the rate. On the whole line they are not equivalent, which
is exactly why v12's ladder had to be graded. Saying this out loud matters because the
*unweighted* whole-line norm grows like `J^+0.99` **even at the anchor**, purely because
the grid's outer radius `~4J/π` grows with `J` — so an unweighted whole-line ladder would
have "diverged" for a reason that has nothing to do with the operator.

---

## 5. Two things that changed elsewhere

**The radius law, with the constants measured (recommended brick (3), delivered).**
`E(X_c) = 0` with the far-field form `U ≈ (m/π) log X + U₀`, `m = ∫Ω`, gives

    log(X_c/c) = −π( c/a + U₀ ) / m .

v12 quoted `X_c ~ e^{c/a}`, which is this law with the **anchor's** `m = −π`. The
profiles' own `m` is not `−π` — it runs `−4.55 → −2.43` over `a = 0.2 … 1.0` — so the
coefficient of `1/a` is `−πc/m ≈ 0.69` at `a=0.2`, not `1`. Measuring `m` and `U₀`
outside the support (where `Ω ≡ 0` and there is no principal value) and substituting:

| a | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 | 0.80 | 1.00 |
|---|---|---|---|---|---|---|---|
| measured `X_c/c` | 34.330 | 12.256 | 6.985 | 4.846 | 3.725 | 2.584 | 2.006 |
| law, own `(m,U₀)` | 34.222 | 12.088 | 6.781 | 4.623 | 3.493 | 2.350 | 1.778 |
| ratio | **0.997** | 0.986 | 0.971 | 0.954 | 0.938 | 0.909 | 0.887 |

Agreement improves monotonically as `a → 0`, which is the right behaviour and attributes
the residual error: the law uses a far-field expansion evaluated *at* `X_c`, and `X_c`
grows as `a` falls, so the expansion gets better exactly where it is being used.

**v11's fourth confirmation of `a*` does not survive (the other three do).** v11 read a
grid-refinement spread on the whole-line Newton solve (`3.7e−3` at `a=0.8`, `1.3e−2` at
`a=1.0` vs `3e−5` at `a=0.5`) as "the solutions are continuum objects only up to
`a ~ 0.5`", and the continuation prompt banked it as a fourth independent confirmation
of the survival boundary. On (RS) the same object is grid converged in `K` to

| a | 0.5 | 0.6 | 0.8 | 1.0 | 1.2 |
|---|---|---|---|---|---|
| spread of `X_c/c`, K≥64 | 6.3e−13 | 4.9e−12 | 2.2e−10 | 2.3e−9 | 7.6e−9 |

i.e. eight to twelve significant figures, with Newton converging from cold start at every
one. The whole-line spread was the global basis failing to represent a compactly
supported profile whose edge regularity is `C^{1/a}` and therefore gets **worse as `a`
grows** — the same instrument-artifact family as v12's Gibbs ringing (banked lesson 31).

What that retires is v11's *argument*, not `a*`. The other three confirmations
(GA-, genome- and basis-convergence in §9-cont2) are about the two-scale GA problem —
whether the two-scale structure survives — which is a different question, and this leg
says nothing about them. **So `a*` is confirmed three times, not four, and separately:
the compactly supported traveling wave itself exists, as a grid-converged continuum
object, well past it.**

---

## 6. Gate-check against the Clay chain (answer it, don't re-paste it)

**(a) Which link does this move?** L1, and for the first time in three legs it moves it
*forward* rather than reclassifying it. v12/v13 established that L1 as posed was
mis-specified; v14 supplies the repair they named and shows it works: the approximate
inverse exists in the continuum limit at the profile the certificate is actually about.
L2, L3, L4 unmoved. Nothing here is a step whose success resolves Clay.

**(b) Is another L1 leg still the best use of the next chunk?** For exactly one more,
yes — and the reason is new. Until now the honest answer was "the L1 machinery is priced
at the wrong point"; that objection is now discharged, and the *remaining* work is
smaller than what it replaces, because eleven legs of far-field apparatus (v3's
resonance, v6's tail bound, v7–v9's estimates, v10's bracket) are simply not needed on a
compact interval. The next brick is `Y₀, Z₀, Z₁, Z₂` in the reduced space, i.e. brick (4)
of the "what would actually be worthwhile" list — **finish one certificate end-to-end** —
which the list ranks above another estimate leg and which is now cheap. If that does not
close in float with margin, the stopping rule applies and the alternative lanes go
primary.

**(c) Is there a cheaper experiment that kills the whole route?** The one this leg ran
was it. The next equivalent is: assemble the four radii-polynomial constants in the
reduced space at one `a` and see whether the budget closes in float. That is a day, not
a leg, and it is decisive in the same way.

---

## 7. What is NOT claimed

- **Not a certificate.** `Y₀`, `Z₀`, `Z₁`, `Z₂` have not been computed in the reduced
  space. `‖A‖` converging says the approximate inverse *exists in the limit*; it says
  nothing about whether the radii polynomial closes.
- **`4.52` is not "better than `47`".** The v7–v9 upper bounds are for a **different
  operator in a different space** (whole line, decay-graded Hölder). The comparable
  quantity between the two is the **slope in the discretization parameter**, not the
  value. Quoting the value as an improvement would be the same error v10 named
  (lesson 28) in a new costume.
- **`‖A‖` here is a measured induced norm, not an upper bound** in the v6/v7 sense: it is
  computed exactly for the discrete matrix at each `K`, which is a statement about the
  discretization, not a continuum theorem. It is on the honest side of lesson 15 only in
  that it is not a family-restricted maximum — it is the exact induced norm of the object
  it names.
- **The reduced ↔ original equivalence is for even, negative, unimodal profiles.** The
  monotonicity that forces `E` to decrease is observed on every solution, not proved.
- **Plain float64.** Nothing is interval-enclosed. `solver/interval.py` still has never
  been pointed at any of this, correctly, because nothing has closed in float.
- **Novelty is unchecked.** A first integral of a scalar traveling-wave equation is
  exactly the sort of thing that is folklore to people who work on gCLM/De Gregorio. The
  literature search is item (5) on the standing list and it blocks any novelty claim here
  as much as anywhere else. What is *not* in doubt is that this project has spent thirteen
  legs discretizing an equation that has a closed-form reduction, which is a lesson
  regardless of who knew it first.

**Honest ceiling.** Route-D v3–v14 remain validated tooling, a no-go theorem, partial
bounds at the wrong point, a diagnosis, and now a repair that passes its own kill switch.
They do not climb the rigor ladder. Even the eventual success this scouts is a
computer-assisted **toy-model** certification (Chen–Hou / Gómez-Serrano genre), not a
Clay solve. 1D gCLM is a toy model of the boundary behaviour of Hou–Luo /
3D-axisymmetric Euler. Overall Clay odds ~0.05%, unchanged by this leg.
