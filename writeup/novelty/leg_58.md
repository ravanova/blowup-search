# Leg 58 — Route-NG novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-A. **Branch:** `leg/ng-v1`.
**Verdict: `PROCEED_NARROW`.** Nothing located states the proposition this leg writes; the one
paper that could pre-empt it (Cadiot, arXiv:2505.03091) **excludes this operator by hypothesis**
rather than covering it. The claim is narrowed in three named ways at the bottom.

Per `writeup/novelty/README.md` and the lesson banked at leg 53: **links, not counts.** Every
query string below is verbatim; every returned link I judged on-topic is listed. Where a search
returned nothing on-topic I say so rather than reporting a number.

---

## The claim under test (NG's proposition, not leg 51's)

> Let `L` be the bordered `a = 0` CLM linearization in the compactified odd-sine coefficient
> basis, split at `K` into a finite block `Γ` and a tail `T`, in a weighted `ℓ¹_w` space with
> `w_k = (1+k)^s`, `s < 1`. `T` has a kernel direction `ĥ` (the far field, `ĥ_m ~ m^-2`) that
> lies **in** the space. Then for every approximate inverse `A` whose tail solve `A₂₂` is within
> `δ` of the prescribed bordered tail inverse — **with `A₁₁`, `A₁₂`, `A₂₁` completely
> arbitrary and unbounded** — the contraction constant obeys
>
>   `Z₁ ≥ ( ‖ĥ + A₂₂ C y‖_w − δ‖C y‖_w ) / ( 1 + ‖y‖_w )`,  `y = G^{-1} B ĥ`,
>
> which is `> 1` for `δ` below an explicit, measured threshold. This is a **lower bound on the
> contraction constant over a class of approximate inverses**, i.e. a no-go for the standard
> radii-polynomial construction on an operator whose unbounded part is a **shift, not a
> multiplier**.

Three separable novelty questions, kept apart on purpose:

* **(N1)** Is the *structural observation* — the standard tail estimate presumes an
  asymptotically diagonal / multiplier unbounded part — in print? **Already settled: YES**
  (leg 57: Cadiot §2–3, and arXiv:2411.18361's `A = A^N ⊕ π^∞` convention). This leg does not
  re-claim it.
* **(N2)** Does any published framework *cover* an operator whose unbounded part is off-diagonal
  with a non-decaying tail inverse — i.e. does the no-go's hypothesis class already have a
  positive result inside it?
* **(N3)** Is a *lower bound on `‖I − AL‖` over a named class of `A`*, for this or any
  comparable operator, in print?

---

## Queries, verbatim, with the links returned

### Q1
`Cadiot arXiv:2505.03091 approximate inverse Fourier series computer-assisted proof`

- https://arxiv.org/abs/2505.03091 — Cadiot, *Stability analysis for localized solutions in PDEs
  and nonlocal equations on R^m* (the paper leg 57 flagged as the largest novelty risk)
- https://iopscience.iop.org/article/10.1088/1361-6544/adb5e8 — Whitham / capillary–gravity
  Whitham solitary waves, constructive existence and stability
- https://arxiv.org/pdf/2409.20457 — validated enclosure of renormalization fixed points via
  Chebyshev series and the DFT
- https://arxiv.org/html/2509.16693 — traveling waves on an infinite strip, suspension bridge
- https://arxiv.org/abs/2105.02995 — approximate inversion of discrete Fourier integral operators
  (off-topic on inspection: numerical linear algebra, not validated numerics)

**On-topic for N2:** Cadiot only. Resolved below.

### Q2 — Cadiot's hypotheses, read from the paper rather than the abstract
Fetched https://arxiv.org/html/2505.03091v1 (the HTML rendering; the PDF fetch returned binary
and was not readable — see the caveat under "How far this pass goes").

The located hypothesis is **Assumption 1**, which requires the dominant linear part to be given
by a **symbol**:

> "`𝕃` is given by its symbol `l : R^m → C` as `F(𝕃u)(ξ) = l(ξ) F(u)(ξ)`"

and §2.2 then carries that into coefficient space as an **infinite diagonal matrix**:

> "`L_e U = ( l(n/2q) u_n )_{n ∈ Z^m}`"

**This is the answer to N2, and it is negative in the useful direction.** Cadiot's construction
*assumes* the unbounded part is a Fourier multiplier — the exact hypothesis this operator fails
(leg 51: the unbounded part is the dilation transport `sin θ ∂_θ`, bidiagonal with **zero
diagonal**). The paper therefore does **not** contain a positive result inside NG's hypothesis
class, and does not pre-empt or refute NG's proposition. It does confirm, again, that the
multiplier hypothesis is the convention — which is N1, already banked and not re-claimed.

### Q3
`radii polynomial approach impossibility "no approximate inverse" lower bound Z1 tail estimate fails`

- https://www.researchgate.net/publication/274384127 — Lessard et al., "Rigorous numerics for
  analytic solutions of DEs: the radii polynomial approach" (states the method, `p(r) = Z₂r² +
  (Z₀ + Z₁ − 1)r + Y₀`; no lower bound on `Z₁`)
- https://arxiv.org/pdf/1605.01086 — framework for numerical computation and a posteriori
  verification of invariant objects
- https://arxiv.org/pdf/2101.00684 — validated forward integration for parabolic PDEs via
  Chebyshev series
- https://arxiv.org/pdf/1706.10107 — analytic continuation of (un)stable manifolds with rigorous
  error bounds

**On-topic for N3:** none. Every hit computes an *upper* bound on `Z₁` for a *chosen* `A`. None
bounds `Z₁` from below over a class of `A`.

### Q4
`"no preconditioner" OR "any approximate inverse" lower bound "I - AL" norm greater than one obstruction operator with nontrivial kernel Newton-Kantorovich validated`

- https://www.sciencedirect.com/science/article/pii/S0898122113006111 — optimal *diagonal*
  approximate inverse preconditioner, generalization
- https://link.springer.com/chapter/10.1007/978-3-031-25820-6_11 — sparse approximate inverse
  preconditioners (survey chapter)
- https://arxiv.org/html/2512.21744v1 — factorized sparse approximate inverse preconditioning for
  **singular** M-matrices
- https://arxiv.org/pdf/2203.10340 — equilibrium validation for triblock copolymers via inverse
  norm bounds for fourth-order elliptic operators

**On-topic for N3:** the singular-M-matrix paper is the nearest miss and it is a *construction*
for a structured singular class (M-matrices, non-negative inverse structure), not a lower bound,
and not in a weighted `ℓ¹` sequence space. The classical preconditioning literature defines
`‖I − AT‖ ≤ ε < 1` as the *goal* and optimizes `A` numerically; I found no statement that a named
class of `A` cannot reach it for a specific operator. **Nothing located states N3.**

### Q5
`Breden Lessard "diagonally dominant" assumption approximate inverse infinite dimensional Newton operator tail "acts as" identity limitation`

- https://arxiv.org/pdf/1503.06315 — Breden–Desvillettes–Lessard, *Rigorous numerics for
  nonlinear operators with tridiagonal dominant linear part* (the closest prior art in the whole
  corpus: the tail here **is** tridiagonal)
- https://www.aimsciences.org/article/doi/10.3934/dcds.2015.35.4765 — the journal version
- https://arxiv.org/abs/1902.00668 — approximating the inverse of a diagonally dominant matrix

**Status: already settled at leg 57 and NOT re-litigated here.** BDL is the one paper that builds
an `A` for a *non*-asymptotically-diagonal derivative, so it is the natural place for a positive
result inside NG's class — but leg 57 read assumptions (4)–(5) from the full PDF and they require
a diagonal bounded away from zero. This operator's diagonal is **exactly zero** for every
`k ≥ 2`. BDL is prior art for the *problem*, not for the *case*.

### Q6
`computer-assisted proof self-similar blow-up transport term approximate inverse tail zero diagonal weighted l1 Chen Hou De Masi`

- https://arxiv.org/pdf/2308.01528 — Chen–Hou, exact self-similar finite-time blowup of the
  Hou–Luo model with smooth profiles
- https://epubs.siam.org/doi/10.1137/23M1580395 — Chen–Hou, 2D Boussinesq / 3D Euler, Part II:
  rigorous numerics
- https://arxiv.org/html/2603.25104 — self-similar blowups with singular profiles of the gCLM
  model
- https://arxiv.org/pdf/2305.05895 — self-similar blowups with smooth profiles of gCLM

**On-topic, and it sharpens the scope line rather than threatening the claim.** These are the
successful computer-assisted proofs *on transport-dominated operators*, and none of them uses an
approximate inverse in a weighted `ℓ¹` coefficient space: they use **weighted energy estimates
with a coercivity/Lyapunov structure** plus interval-arithmetic verification of finitely many
inequalities. That is a *different method*, not a counterexample — and it is the honest reading
of what NG's no-go does and does not say: it is a no-go for the `ℓ¹`-Fourier
radii-polynomial/approximate-inverse lane, and the weighted-energy lane is untouched by it and
is where the published successes are. This sentence goes into the writeup verbatim.

### Q7
`"Constantin-Lax-Majda" OR "De Gregorio" computer-assisted proof Fourier coefficients validated numerics approximate inverse transport dilation term tail bound`

- https://arxiv.org/html/2607.19762v1 — *The spectral picture of self-similar collapse in the
  Constantin–Lax–Majda equation* (2026). **The single most relevant nearby statement found.**
  It reports that on the real line the self-similar generator "carries a dilation-generated
  continuous essential spectrum and admits **no Fourier-series reduction**", and that the
  Hilbert-transform term is "not relatively compact".
- https://arxiv.org/pdf/2506.02800 — stability/instability for the De Gregorio modification
- https://link.springer.com/article/10.1007/s00205-018-1298-1 — Jia–Stewart–Sverak, De Gregorio

**Assessment.** This is a statement about the **spectrum** of the dilation generator on the line,
not about the contraction constant of a radii-polynomial certificate, and it is about the `L²`
realization rather than a weighted `ℓ¹` coefficient space. It is nevertheless the closest
published articulation of "the dilation term is what obstructs the coefficient-space route", and
it must be **cited as adjacent prior art** wherever NG's mechanism paragraph appears. NG's
proposition adds what that paper does not have: a quantitative lower bound on `Z₁` over a named
class of `A`, on a bordered finite/tail split, with a positive control.

---

## What this pass settles, and the three narrowings it forces

1. **Cadiot does not pre-empt NG** — Assumption 1 requires a Fourier-multiplier dominant part, so
   the paper's hypotheses **exclude** this operator instead of covering it. Leg 62 is settling
   the same question from the full PDF with a different tool; **if leg 62's reading disagrees
   with this one, leg 62 wins** and NG's claim is capped by its answer. This pass is not a
   substitute for that one.
2. **N1 is not claimable and is not claimed.** The observation that the standard tail estimate
   presumes a multiplier is folklore stated in print (leg 57). NG restates it as *hypothesis*,
   with attribution, not as a finding.
3. **What is offered as new is N3 only:** a lower bound on the radii-polynomial contraction
   constant `Z₁`, valid over a named class of approximate inverses strictly larger than block
   diagonal, for a specific operator whose unbounded part is off-diagonal. Nothing located states
   this, for this operator or any other. The adjacent claim (Q7) is spectral, not certificate-
   theoretic.

## How far this pass goes (say the limits out loud)

* Cadiot's hypotheses were read from the **HTML rendering (`v1`)**; the PDF fetch returned
  unreadable binary. Leg 57 was burned by reading BDL at abstract depth, and HTML-of-v1 is deeper
  than an abstract but shallower than the full PDF of the current version. **This is why leg 62
  exists**, and NG's writeup carries the caveat rather than hiding it.
* Searches are English-language web search only; no MathSciNet/zbMATH review search was run.
* The `leg52_search_index_flag` (that this project's searches may share an index bias across
  legs) **STANDS** and is not cleared by this pass.
