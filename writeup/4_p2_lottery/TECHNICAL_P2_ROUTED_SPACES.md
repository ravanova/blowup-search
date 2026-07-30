# Phase-2 P2 — Route D v3: which space pair can carry the certificate

**Status: Level-1 *tooling* + a **no-go theorem** for an entire category of
function spaces, with its numerical face, its control, and the replacement it
points to — NOT a certificate.** Clay odds unchanged (~0.05%).

[Route-D v2](TECHNICAL_P2_ROUTED_DRESS.md) ran the float dress rehearsal of the
Newton–Kantorovich bounds at the exact `a = 0` anchor and got an honest structural
negative: the ball closes at no truncation, because the transport term
`c(1 + cos θ)∂_θ` degenerates at `θ = ±π` (i.e. at `X = ∞`). It ended with a
*constructive* half — the linearized inverse loses exactly one power of decay, so
grade the codomain by one mode power and `‖A‖ = 3.000` goes flat in `N` — and
called that "the asymmetric space pair a working certificate must use."

That proposal came with a condition attached, and this leg discharges it:

> the quadratic term `D²F[h,h] = 2 h H(h)` must **also** land in the graded
> codomain; do this on paper first, and if no consistent pair exists, that is
> itself the answer and the leg stops cheaply.

**No consistent pair exists.** Not for the grading v2 proposed, and not for *any*
pair of diagonally weighted `ℓ¹` spaces: the two Newton–Kantorovich requirements
are separated by exactly one grading power, and the separation is *conserved* —
you can move it between the two bounds but you cannot remove it. That is the
no-go. The same measurements then identify what does work, and it is not a
weighted-`ℓ¹` pair at all: **decay-graded** spaces, in which both requirements
hold simultaneously, at a quantified price with an interior optimum.

Rebuild the figure from committed data (no re-derivation):
`python writeup/4_p2_lottery/p2_route_d_v3_evidence.py` →
`writeup/figures/fig21_p2_route_d_v3_spaces.png` (reads
`writeup/data/p2_route_d_v3_spaces.json`; regenerate the data — deterministic,
about a minute — with `python experiments/p2_route_d_v3_spaces.py`).

Code: `solver/decay_grading.py` + `test_decay_grading.py` (7/7). Full suite now
**10 files green**.

---

## 0. Why this was worth doing before writing any more solver

The v2 note ranked the v3 rebuild as a "real, multi-brick build": rederive the
bounds in the graded pair, handle the far field with the exact ODE inverse rather
than a diagonal model, and only then bring in interval arithmetic. All of that is
downstream of one question that costs an afternoon of algebra:

> is there a pair of spaces in which **every** Newton–Kantorovich bound is finite?

The radii polynomial needs four quantities, and they pull on the space pair in
opposite directions:

| bound | what it needs |
|---|---|
| `Y₀ ≥ ‖A F(x̄)‖_X` | `A : Y → X` bounded |
| `Z₀ ≥ ‖I − AA†‖_{X→X}` | `A` a genuine approximate inverse on `X` |
| `Z₁ ≥ ‖A(DF − A†)‖_{X→X}` | the discarded tail maps `X → Y` |
| `Z₂ ≥ ‖A·D²F‖` | the **quadratic** maps `X × X → Y` |

`A` bounded pulls `Y` to be *stronger* than `X` (the inverse of a degenerate
transport loses decay, so its input must supply the deficit). The quadratic pulls
`Y` to be *no stronger* than `X` (products do not gain decay). v2 measured the
first pull and proposed a `Y` one power stronger. Nobody had measured the second.

This is the discipline lesson from v2 §11 applied one level up: *do the cheap
rehearsal before hardening.* v2's rehearsal saved interval-enclosing bounds that
could never close. This leg's rehearsal saves **building a whole two-region solver
in a space pair that could never have been consistent.**

---

## 1. The quadratic term is a pure convolution

The starting point is an identity worth banking on its own.

With `H(cos kθ) = sin kθ` for every `k ≥ 0` and `H(1) = 0` (unconditional; the
Hardy/Cayley argument of v2 §1), write `h = Σ_{k≥0} h_k cos kθ`. Then

```
Q(h) := h H(h) = Σ_{j≥0, k≥1} h_j h_k cos(jθ) sin(kθ)
              = ½ Σ_{j≥0, k≥1} h_j h_k [ sin((j+k)θ) + sin((k−j)θ) ].
```

The difference part is antisymmetric in `(j,k)` *once the missing `k = 0` row is
restored*, and the same `k = 0` row is exactly what the sum part is missing. The
two corrections cancel identically, leaving

> **(Q)**  `Q(h) = ½ Σ_{m≥0} ( Σ_{j+k=m} h_j h_k ) sin(mθ)` — a **pure
> convolution**. No difference frequencies at all.

Structurally this is Hardy space: `h + iH(h)` is a boundary value of a function
holomorphic in the upper half plane, `2 h H(h)` is the imaginary part of its
square, and squaring a holomorphic function cannot produce difference frequencies.

`solver/decay_grading.quadratic_coeffs` implements (Q) as a single `np.convolve`.
It is a deliberately *independent* second build of the quadratic part of
`solver/nk_fourier.residual` (a double loop over sum **and** difference
frequencies) — the "build the same object twice" rule that caught the `k = 0` fold
bug in Route-D v1. They agree to `3.2e-17` on random inputs, and exactly (`0.0`)
at the anchor. (Gate 4.)

**Two immediate consequences.**

1. *A sharp constant.* For `X = ℓ¹_u` (cosine side) and `Y = ℓ¹_v` (sine side),
   (Q) gives termwise `‖Q(h)‖_Y ≤ ½ S ‖h‖²_X` with

   ```
   S := sup_{j,k ≥ 0}  v_{j+k} / (u_j u_k) .
   ```

   And it is *necessary*: take `h = ξ e_j + η e_k`, whose image contains
   `q_{j+k} = ξη`, and optimize `ξ, η > 0` at fixed `‖h‖_X = ξu_j + ηu_k`; the
   minimum of `(ξu_j + ηu_k)²/(ξη)` is `4u_j u_k`, so any valid constant `M`
   obeys `v_{j+k} ≤ 4M u_j u_k`. Hence

   > `‖Q(h)‖_Y ≤ M‖h‖²_X` for all `h`  ⟺  `S < ∞`,  with `S/4 ≤ M ≤ S/2`.

   Gate 5 checks this two-sidedly on four weight pairs by direct maximization over
   the two-mode optimizer plus random probes.

2. *A free 2× improvement on v2.* In the unweighted case `S = 1`, so `M = ½` — half
   the Wiener-algebra constant `‖hH(h)‖ ≤ ‖h‖‖H(h)‖ ≤ ‖h‖²` that v2 used. It
   changes no v2 conclusion (its certification budget was identically zero), but it
   is the sharp constant and it is what the v3 accounting uses.

---

## 2. The no-go, on paper

Take positive weights `u = (u_k)_{k≥0}` on the domain, `v = (v_m)_{m≥1}` on the
codomain.

**Requirement II (quadratic).** By §1, `S = sup_{j,k} v_{j+k}/(u_j u_k) < ∞`.
Setting `k = 0` already gives

```
v_m ≤ S u_0 u_m        for every m,   i.e.   v_m / u_m ≤ S u_0   UNIFORMLY.
```

If the constant mode is gauged out of the domain (as the `a0` normalization of
v2 D3 does, so that only `j,k ≥ 1` are available), take `k = 1` instead: `v_m ≤ S
u_1 u_{m−1}`, and for any weight that is non-decreasing (higher modes controlled at
least as strongly — the natural choice, and the one every implementation makes)
this again gives `v_m/u_m ≤ S u_1`, bounded.

**Requirement I (bounded inverse).** v2 D6 measured `‖A e_m‖_{ℓ¹} ≈ 1.97 m` and
derived it from the far-field ODE. In weighted norms the smallest admissible
codomain weight is `v_m^min(u) = ‖A e_m‖_{ℓ¹_u}`, so requirement I is
`v_m ≳ ‖A e_m‖_{ℓ¹_u}`. §3 measures this for weighted `u` as well, and the answer
is the same: `v_m ≳ κ · m · u_m` with `κ ≈ 1.3–3.2` over `s ∈ [0,2]`.

**They are incompatible.** `v_m/u_m` cannot be both `≤ S u_0` (bounded) and
`≥ κ m` (linearly growing). The failure margin grows linearly in the mode number,
so no clever tuning at finite `m` helps. ∎

The proof is almost embarrassingly cheap once (Q) is in hand, and it is the whole
point of doing the algebra before the code. The mechanism is worth stating in
words: **the constant mode (or any fixed low mode) multiplies everything at full
strength.** `e_0 · H(h) = H(h)` — no decay gained. A codomain strictly stronger
than the domain therefore cannot receive the quadratic, however the weights are
chosen.

---

## 3. The no-go, measured

`experiments/p2_route_d_v3_spaces.py` runs the theorem as an experiment, over the
two-parameter family

```
u_k = (1+k)^s   (domain),        v_m = (1+m)^t   (codomain),
```

with `s ∈ [0,2]`, `t ∈ [−1.5,3]` on a 0.25 grid, the gauge row carrying weight 1 in
every pairing (as in v2 D6).

**S2 — what the inverse costs.** The ratio `v_m^min/(m u_m)`, which the theorem
needs to be bounded below:

| `s` | `m=2` | `m=4` | `m=8` | `m=16` | `m=32` |
|---|---|---|---|---|---|
| 0.0 | 2.00 | 2.00 | 2.00 | 1.99 | 1.97 |
| 0.5 | 1.61 | 1.68 | 1.72 | 1.73 | 1.69 |
| 1.0 | 1.33 | 1.59 | 1.74 | 1.79 | 1.72 |
| 2.0 | 1.00 | 2.43 | 3.18 | 3.15 | 2.61 |

All `O(1)`: the price really is **exactly one mode power**, for weighted domains
as well as flat ones. (The `s = 0` column reproduces v2's `1.97 m`.)

**S3 — the map.** Both requirements turn out to depend only on the **gap**
`g = t − s`, and their growth exponents are exact complements:

| `g` | −1.75 | −1.0 | −0.5 | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|---|---|---|
| `‖A_N‖_{Y→X}` exponent in `N` | 2.70 | 1.96 | 1.47 | 0.98 | 0.50 | 0.04 | 0.00 |
| sharp quadratic `S_K` exponent in `K` | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 1.50 |
| **their sum** | 2.70 | 1.96 | 1.47 | **0.98** | **1.00** | **1.04** | 1.50 |

So `‖A_N‖ ~ N^{1−g}` and `S_K ~ K^{g}`:

> **The conservation law.** A certificate needs *both* exponents to be zero. Their
> sum is `≥ 1` at every `g`, and exactly `1` on `0 ≤ g ≤ 1`. The measured minimum
> over the entire family is **0.98**. The one power the far field loses has to be
> paid by one bound or the other; the choice of weights only decides **which**.

In `(s,t)` coordinates: a bounded inverse needs `t ≥ s+1`, a bounded quadratic
needs `t ≤ s`, and the unit strip between them is empty. Both boundaries are pinned
grid-independently by evaluating the exponents *on* the candidate lines (`t = s−1`:
1.96; `t = s`: 0.98; `t = s+1`: 0.00–0.06; algebra at `t = s`: 0.00, at `t = s+0.25`:
0.25 — all essentially constant in `s`).

**S4 — the control.** The v2 D4 ablation, re-run on the space-pair question:
replace the transport factor `(1 + cos θ) → 1`, change nothing else. The inverse
boundary moves from `t ≥ s+1` to `t ≥ s−1` — **down by exactly two powers.** That
is the right number: a non-degenerate first-order transport *gains* one power when
inverted, the true one *loses* one, and `1 + cos θ` vanishes to order **two** at
`θ = ±π`. The regions then overlap on a full unit strip (`s−1 ≤ t ≤ s`), the
minimum exponent sum drops from 0.98 to **0.00**, and the overlap is non-empty at
9/9 values of `s`.

> The obstruction is the far-field degeneracy of this specific operator, not the
> Newton–Kantorovich method and not the `ℓ¹` framing. Remove the degeneracy and
> the same machinery has an admissible space pair immediately.

This is the ablation discipline of v2 D4 doing its job again: a divergence is a
suspicion, a divergence that disappears when exactly one feature is removed is an
attribution.

---

## 4. Why weights were never going to work: a category error

The no-go is sharp, but it should not be read as "the far field is
un-invertible". It says something narrower and more useful.

A diagonal weight on Fourier coefficients measures **smoothness**, not **decay**.
The single mode `cos kθ` equals `(−1)^k` at `θ = π` — it does not decay at `X = ∞`
*at all*, for any `k`, and no weight `u_k` can see that. Decay in `X` is a
statement about the *oscillatory-in-k* structure of the coefficient sequence
(alternating coefficients concentrate mass at `θ = π`), i.e. about finitely many
linear moment conditions, not about a diagonal weight. Asking a weighted-`ℓ¹` pair
to express "loses one power of decay" was a category error, and the conservation
law of §3 is what the category error looks like when you measure it.

`solver/decay_grading.cos_power_coeffs` makes this concrete. The canonical element
of the class "decays like `X^{-α}`" is

```
f_α(X) = (1 + X²)^{-α/2} = |cos(θ/2)|^α ,
```

whose exact cosine coefficients follow from the generalized binomial series via a
stable two-term recursion (`a_{k+1} = a_k (α/2 − k)/(α/2 + k + 1)`; no Γ of a
negative argument is ever formed). Gate 1 pins it against `α = 0, 2, 4`, where the
answer is a finite trig polynomial — in particular `f_2 = (1 + cos θ)/2` is the
anchor's own shape. For non-even `α` the ratio tends to `−1`: the coefficients
**alternate** and decay like `k^{-α-1}`. Alternation *is* the decay. Combined with
`H(cos kθ) = sin kθ`, this makes `H f_α` computable to machine precision with no
quadrature at all, which is what lets the far field be measured rather than
assumed. (Gate 2 checks it against the closed-form pairs
`(1+X²)^{-1} ↦ X/(1+X²)` and `(1+X²)^{-2} ↦ X(3+X²)/2(1+X²)²`, to `1e-16`.)

---

## 5. The far field is resonant at the anchor's own decay rate

v2 D6 derived the far-field model operator and its "one lost power" from

```
L h = −c h_X − h/X ,      (X^{1/c} h)' = −(1/c) X^{1/c} g .
```

Between **decay-graded** sup norms `‖h‖ = sup X^α|h|` and `‖g‖ = sup X^{α+1}|g|`
that solution operator has norm

> **`‖L^{-1}‖ = 2 / |α − 2|`.**

`solver/decay_grading.farfield_inverse_norm` measures this independently: a
second-order (trapezoidal, in `τ = log X`) discretization on `[1, 10¹²]`, with the
integration direction chosen by which solution the space admits, and the induced
norm obtained in one pass because the discretization is an M-matrix. Agreement with
the exact finite-domain value is **≤ 0.008 %** across 15 values of `α` on both
sides of the pole. (Gate 7. Comparing instead against the infinite-domain `2/|α−2|`
shows a 6 % gap at `α = 1.9` — that is the honest finite-domain effect
`(X₀/X_max)^{|2−α|}`, not a discretization error.)

The pole at `α = 2` is not an artifact:

- `X^{-1/c} = X^{-2}` at `c = ½` is the **homogeneous** far-field solution, and
- `X^{-2}` is the decay of the **anchor** `Ω₂ = −1/(1+X²)`.

The space boundary sits exactly on the kernel. And the same resonance is visible
from the operator side without any ODE model at all: applying the full linearization
to `f_α` and using `Ω₂ ~ −X^{-2}`, `H(Ω₂) = −X/(1+X²) ~ −1/X`,

```
DF f_α = f_α H(Ω₂) + Ω₂ H(f_α) − c (f_α)_X  ~  ( c α − 1 ) X^{-α-1} + O(X^{-3}),
```

so `lim X^{α+1} DF[f_α] = cα − 1 = (α−2)/2`, which **vanishes at `α = 2`**. Measured
from the exact Fourier coefficients (no quadrature) at `X = 3·10³, 10⁴`, to ≤ 0.3 %.
Two independent routes, same resonance.

> **v2's "the inverse loses exactly one power" is this resonance seen at integer
> grading.** Generic `α` loses nothing; `α = 2` — the anchor's own rate — loses a
> logarithm, and integer-graded weights round that up to a full power.

Note also that the expansion above requires `α < 2`: for `α > 2` the coupling term
`Ω₂ H(f_α) ~ X^{-3}` *dominates* `X^{-α-1}`, so perturbations decaying faster than
the anchor leave the natural codomain class. The admissible window is
`1 < α < 2` — `α > 1` for integrability (which the far-field law
`H(f)(X) ~ (∫f)/(πX)` needs), `α < 2` from the coupling.

---

## 6. The pair that works, and what it costs

In the decay-graded pair

```
X = { h : |h| ≲ X^{-α} },        Y = { g : |g| ≲ X^{-α-1} },        1 < α < 2,
```

**every** term lands where it should:

| term | behaviour | in `Y`? |
|---|---|---|
| transport `c h_X` | `~ X^{-α-1}` | ✓ (exactly) |
| `h H(Ω₂)` | `~ −X^{-α-1}` | ✓ (exactly) |
| `Ω₂ H(h)` | `~ −(∫h/π) X^{-3}` | ✓ (`α<2` ⇒ faster) |
| **quadratic `h H(h)`** | `~ (∫h/π) X^{-α-1}` | ✓ (exactly) |

The quadratic line is the one the whole leg turns on. `H(h)(X) → (∫h)/(πX)` for
any integrable `h`, so `h·H(h)` decays **one power faster than `h`** — precisely
the gain the far-field inverse needs and precisely the gain no diagonal weight can
express. Measured directly on `f_α`:

> `X^{α+1} f_α H(f_α) → (∫f_α)/π`, with `∫f_α = √π Γ((α−1)/2)/Γ(α/2)`,

verified against that closed form at `α = 1.2, 1.5, 1.8` (gate 6; the approach to
the limit is `O(X^{1−α})` — the known second term of the multipole expansion —
which is fitted before comparing, and the extrapolated limit matches to < 0.1 %).

**The price.** Detuning off the resonance to `α = 2 − ε` buys a bounded far-field
inverse at cost `2/ε`, while the quadratic constant `C_Q(α) = (∫f_α)/π` blows up
like `2/(π(α−1))` as `α → 1`. Combining them in the same `Z₂ = 2‖A‖M` convention v2
used:

| `α` | 1.1 | 1.3 | **1.4** | **1.5** | 1.7 | 1.9 |
|---|---|---|---|---|---|---|
| `‖A_far‖ = 2/(2−α)` | 2.22 | 2.86 | 3.33 | 4.00 | 6.67 | 18.74 |
| `C_Q = (∫f_α)/π` | 6.80 | 2.53 | 2.00 | 1.67 | 1.29 | 1.08 |
| `Z₂` (scoping) | 30.2 | 14.5 | **13.3** | **13.4** | 17.2 | 40.3 |
| budget `~1/(4Z₂)` | 0.008 | 0.017 | **0.019** | **0.019** | 0.015 | 0.006 |

> **There is an interior optimum at `α* ≈ 1.44`** (`(2−α)/∫f_α` maximized; `α = 3/2`
> is within 1 % of it and is the natural round choice). The optimum is broad — the
> budget is within 1 % over `α ∈ [1.35, 1.55]`.

So a Route-D v3 build has a **design parameter it did not know it had**: certify
profiles decaying like `X^{-3/2}`, with residuals measured in `X^{-5/2}`. Not
`X^{-2}`, which is the anchor's own rate and the one every naive choice would pick
— and which is exactly the rate at which the far-field inverse is unbounded.

**This is a scoping estimate and nothing more.** It uses leading-order far-field
constants only; it contains no compact-core contribution to `Z₁` or `Z₂`; it is
plain float64; nothing in it is interval-enclosed. It sizes the next brick. It
certifies nothing.

---

## 7. What this changes for Route D

**Retired.** v2 D6's literal recipe — "grade the codomain by one mode power, `‖A‖ =
3.000 flat, that is the pair to use" — is retired. The measurement was right, the
inference was not: in that pair `Z₂` diverges exactly as fast as `‖A‖` converges.

**Established.** The whole diagonal-weight category is closed, with a proof, a
2-parameter numerical sweep, a grid-independent boundary check, and a control that
attributes the obstruction causally.

**Specified.** The replacement is a decay-graded (two-region) pair with an
identified optimum `α ≈ 3/2` and an estimated `Z₂ ≈ 13`. That is a much sharper
starting point than v2 handed over — but the honest reading of the number is
sobering: a `Z₂` of order 10 with a `Z₁` yet to be paid for leaves a certification
budget of order `10^{-2}` at best, and the `a ≠ 0` residual floor is `~10^{-2}`.
The margin, if it exists at all, is thin.

**Still open (unchanged by this leg).** The compact-core block; a rigorous
enclosure of the far-field inverse rather than an asymptotic one; the matching
between core and far field; and, downstream of all of it, the `a ≠ 0` case where
no exact anchor exists.

## 8. Honest ceiling

Everything here is plain float64. Nothing is interval-enclosed and nothing is
rigorous. This leg does not climb the rigor ladder: it closes one more route with a
reason, retires an inference that looked constructive, and gives the replacement an
address and a design parameter. Even the eventual success it scouts would be a
computer-assisted **toy-model** certification in the Chen–Hou / Gómez-Serrano
genre, of a profile that at `a = 0` is already known in closed form. 1D HL is a toy
model of the boundary behaviour of Hou–Luo / 3D axisymmetric Euler. Overall Clay
odds remain ~0.05%.

---

### Reproduce

```
python test_decay_grading.py                                  # 7/7 gates
python experiments/p2_route_d_v3_spaces.py                    # ~1 min, deterministic
python writeup/4_p2_lottery/p2_route_d_v3_evidence.py         # fig21 from committed data
```
