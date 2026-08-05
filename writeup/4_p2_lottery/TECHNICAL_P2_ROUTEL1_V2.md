# Route-L1 v2 — the certificate rebuilt where the operators are exact, and the one term that is left

*Phase 2, leg 51. Stage `L1` step two: move the certificate off the truncated
finite-difference grid and into Route-E's compactified basis, where `H`, the dilation and
the velocity are exact on the whole line. Code: `solver/spectral_certificate.py`,
`test_spectral_certificate.py` (14/14), `experiments/p2_route_l1_v2_spectral.py` →
`writeup/data/p2_route_l1_v2_spectral.json` → **fig46**. Deterministic, 53 s.*

**THE REPRESENTATION CHANGE DID EXACTLY WHAT THE PLAN SAID IT WOULD, AND THEN THE
SURVIVING TERM FAILED.** The operator gap vanishes, `Y₀` becomes **exactly zero in rational
arithmetic**, the truncation gap collapses into a single spectral-tail term — and that term
has no bound in any weight class tested. The class that standard radii-polynomial work uses
is the worst of them: the tail inverse grows by a factor **`ν` per neglected mode**.

---

## 0. What is being claimed, exactly

Stated before the numbers, and not widened afterwards:

> On the **a = 0 CLM fixed point** written in the odd-sine basis of `X = tan(θ/2)`, three
> of the four terms of the radii polynomial are finite and rigorous — `Y₀ = 0` exactly,
> `Z₁` on the finite block bounded in interval arithmetic, `Z₂` finite from the Banach
> algebra structure of the basis. The fourth, the **tail term**, is measured to diverge in
> every weight class tried: flat `ℓ¹`, algebraic `(1+k)^s` for `s ∈ [0, 2]`, and geometric
> `ν^k` for `ν ∈ {1.05, 1.2}`.

What is **not** claimed: that no space exists. What is measured is that no space *in these
three families* does, on the friendliest object available, and that the obstruction has a
name — the tail operator's diagonal is exactly zero and its kernel is the `|X|⁻¹` far
field. And the leg's ceiling (clause S7, pre-committed): the a = 0 CLM profile is **one
mode**, analytic, and in every class considered, so a wall measured there bounds the
difficulty for `HL_S2_nonsymmetric` **from below**.

---

## 1. Why the basis was changed

Leg 50 closed the radii polynomial in interval arithmetic, but around a
finite-dimensional system built from stored finite-difference operators on `|X| ≤ 745`.
The two gaps it left were named in the plan of record as the same gap: **the certificate
lives on a truncated grid**. Route E's compactification removes the grid:

| | grid certificate (leg 50) | compactified certificate (this leg) |
|---|---|---|
| far field | truncated at `X_max = 745`, gap **1.55e+08 ball radii** (leg 46) | exact; `θ = π` **is** `X = ∞` |
| `H` | dense finite-difference matrix, treated as exact data | `H(sin kθ) = −cos kθ + (−1)^k`, exact |
| `X d/dX` | finite differences on a sinh grid | `sin θ d/dθ`, bidiagonal, exact |
| velocity | quadrature operator `Uop` | `N_{k+1} = −2N_k − N_{k−1} − 2cos kt`, exact |
| `Y₀` at the anchor | 5.17e−12 (a float residual, enclosed) | **0**, in `fractions.Fraction` |
| terms left unbounded | 2 (operators, far field) | **1** (the spectral tail) |

## 2. The exactness audit is executable, not a docstring (S1)

`rescaled_spectrum.py` has claimed the three identities since Route E. This leg makes them
runnable:

* **Exact rational check.** `w = (1+iX)/(1−iX)`, and `w^k` computed as a **Gaussian
  rational** for rational `X`, agrees with `cos kθ + i sin kθ` to **3.5e−15** over
  `k = 1,2,3,5,9` — machine epsilon times the size of `k`. The identity for `H` then
  follows from where `w^k`'s only pole is: `(1 − iX)^k` vanishes at `X = −i`, in the
  **lower** half plane, so `w^k` is analytic in the upper one and the Hilbert transform on
  the line carries its real part to its imaginary part.
* **The velocity's closed form.** The recursion's constant terms are `c_k = (−1)^k k`
  **exactly** (defect `0.0`, `k = 1..16`) — and that is not a decoration, see §6.
* **Independent numeric cross-check.** `solver/line_hilbert.py`, an unrelated
  implementation, reproduces `H(sin kθ) = −cos kθ + (−1)^k` with a defect that falls like
  `n^−1.00` on refinement — a rate, not a single agreement number.

## 3. The anchor's residual is exactly zero (S2)

`Ω₀ = −sin θ`, `c_ω = −1`, `c_l = 1`. In coefficient space the residual of an 8-mode
profile has 18 modes and **every one is `Fraction(0)`**. Not 1e−16 — zero. The negative
control: perturb `b₄` by 2e−3 and 5 modes become nonzero.

This is a thing the grid certificate structurally could not do. `Y₀` is not a small number
in this basis; it is *absent*.

## 4. The four terms (S3)

Finite block, `K = 256`, rigorous (interval arithmetic on exactly-representable matrix
entries), norms `‖b‖_w = Σ w_k |b_k|`:

| class | `Y₀` | `Z₁` (finite) | `Z₂` | `r_max` |
|---|---|---|---|---|
| flat `w=1` | 0 | 1.18e−08 | 9.80e+03 | 1.02e−04 |
| **algebraic `s=1`** | **0** | **1.44e−10** | **79.5** | **1.26e−02** |
| geometric `ν=1.1` | 0 | 1.19e−05 | 1.50e+08 | 6.65e−09 |

And the tail term, `‖T_tail⁻¹‖_w` on modes `65 … M`:

| class | `M=128` | `M=1088` | divergence | per mode |
|---|---|---|---|---|
| flat `w=1` | 1.02 | 16.3 | `M^{+1.28}` | ×1.0029 |
| algebraic `s=0.394` | 0.876 | 7.66 | `M^{+1.00}` | ×1.0023 |
| algebraic `s=1` | 0.706 | 2.87 | `M^{+0.64}` | ×1.0015 |
| geometric `ν=1.05` | 2.51 | 5.75e+18 | — | **×1.045** |
| geometric `ν=1.20` | 2.74e+03 | 3.60e+77 | — | **×1.195** |

The geometric rows are quoted per mode because a power-law exponent would be meaningless
there: the growth factor **is `ν`**, to three digits, in both cases. Every neglected mode
costs the full weight of the mode.

## 5. The structural fact, and why it is not a tuning problem

**The tail operator's diagonal is exactly zero.** `max|diag(T_tail)| = 0.0`, not 1e−16.

Every radii-polynomial certificate in the literature splits the approximate inverse as
`A = A_K ⊕ A_tail` with `A_tail` **diagonal**, because the unbounded part of the operator
being certified is a **multiplier** — a Laplacian, a dispersion relation, a `Λ^s` — whose
tail `Λ_k → ∞` has a diagonal inverse `1/Λ_k` that is both explicit and small. Here the
unbounded part is the **dilation transport** `sin θ ∂_θ`, whose matrix is bidiagonal with
entries `±k/2` and nothing on the diagonal. There is no `A_tail` of the standard shape,
for any weight.

And the operator is not merely awkward to invert; it is **not injective** in the classes
where the object lives. The homogeneous recursion

    v_{m+1} = v_{m−1} + 2 g_m ,        h_m = v_m / m

gives a measured decay `h_m ~ m^{−2.007}` (predicted `m^{−2}`). A coefficient decay
`k^{−1−α}` is a far field `|X|^{−α}`, so **the kernel of the tail operator is the `|X|^{−1}`
profile** — in `ℓ¹_w` for every `s < 1`. Leg 46's truncation gap and leg 47's wrong-sign
reach trend were not two facts about a domain size. They were this one mode, seen through a
grid.

## 6. The velocity does not escape it either

`c_k = (−1)^k k` means each mode's velocity carries a term **linear in `θ`**. `θ` is not a
trigonometric polynomial: its odd Fourier series is the sawtooth, coefficients exactly
`1/m`. So for any model *with advection* — and `HL_S2_nonsymmetric` has it — the exact
velocity operator injects an algebraic `1/m` tail regardless of how analytic the profile
is. **The far field does not leave when the grid does.**

## 7. The positive control (S4)

A negative result needs an instrument that can say "bounded". Add `Λ¹` dissipation — the
same code path, `−μk` on the diagonal, turning the shift into a multiplier and nothing
else:

| | inviscid | `μ = 0.1` | `μ = 0.5` |
|---|---|---|---|
| flat `ℓ¹` | `M^{+1.28}` | `M^{+0.000}` | `M^{+0.000}` |
| algebraic `s=1` | `M^{+0.64}` | `M^{+0.000}` | `M^{+0.000}` |
| geometric `ν=1.2` | ×1.195/mode | ×1.081/mode | `M^{+0.000}` |

Two things worth keeping. The instrument reports **bounded** the moment the operator has a
diagonal, so the inviscid divergence is a measurement. And the geometric class needs
**five times more dissipation** than the other two before it saturates — it is the fragile
class on both sides of the experiment.

## 8. Float against exact (S5)

Banked lesson 86 says a bound dominated by its own evaluation error is a statement about
the code. The quantity that decides this leg — the weighted inverse norm — was recomputed
in **exact rational Gauss–Jordan** (`fractions.Fraction`, no floating point) at
`K = 16, 32, 64, 96, 128`, `ν = 1.1`. Maximum relative gap against float: **8.8e−15**. At
`K = 96` the exact answer is `62.0005`; at `K = 128` it is `609.17`. The divergence is
mathematics.

## 9. The window, from both sides (S6)

The object side: a far field `Ω ~ |X|^{−α}` gives coefficients `~ k^{−1−α}`, so
`‖Ω‖_w < ∞` for `w_k = (1+k)^s` **iff `s < α`**. For `HL_S2_nonsymmetric`, `α = 0.394`.

The operator side, measured: the tail's divergence exponent as a function of `s` is a
U-curve with its minimum at **`s = 1.00`** (exponent `+0.64`), rising to `+1.28` at `s = 0`
and `+1.27` at `s = 2`. At the object's own boundary `s = α = 0.394` the exponent is
`+1.00`.

**The window is empty by 0.606 in exponent units,** and no point of the curve touches zero.
The class where the operator is least bad is the class where the target has infinite norm,
and vice versa.

## 10. What this leg answers, and what it does not

`L1`'s pre-committed gate was: *does the polynomial close in interval arithmetic, tail
included?* The answer is **no**, and the term that ran out is named: **the weight class of
the tail**, not the interval widening (three terms are rigorous and small) and not the
spectral truncation as such (`Y₀` is exactly zero).

The plan of record says that if it is the weight class, that is the contribution and it
should be written up rather than filed as a failure. Route J's literature pass found **no
hit** for the one methodological claim this touches — geometric `ℓ¹` weights on bounded
domains versus algebraic decay on an unbounded one — and this leg sharpens what that claim
should be: the obstruction is not the profile's decay but **the unbounded part of the
operator being a shift instead of a multiplier**, which is a statement about self-similar
*transport* and not about any particular profile. It also predicts the literature's shape:
the certified self-similar blow-ups that used this machinery (Dahne–Figueras, CGL) are
**dissipative**, and the certified inviscid ones (Chen–Hou) use weighted energy estimates
instead. That prediction is checkable and it has not been checked here.

**No link of the L1→L4 chain moved.** The object still has no proof of any kind.
