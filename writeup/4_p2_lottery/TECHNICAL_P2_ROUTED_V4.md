# Phase-2 P2 — Route D v4: the full operator in the decay-graded pair

**Status: Level-1 *tooling* + scoping — one confirmation and one new structural
gap. NOT a certificate.** Clay odds unchanged (~0.05%).

[Route-D v3](TECHNICAL_P2_ROUTED_SPACES.md) closed the entire weighted-`ℓ¹`
category with a conservation law and identified the replacement — **decay-graded**
spaces

```
‖h‖_X = sup_X (1+X²)^{α/2} |h| ,      ‖g‖_Y = sup_X (1+X²)^{(α+1)/2} |g| ,
```

— then priced them: far-field inverse norm `2/|α−2|`, quadratic constant
`(∫f_α)/π`, interior optimum `α* ≈ 1.44`, `Z₂ ≈ 13.3`. Every one of those numbers
came from the far-field **model** operator `L h = −c h_X − h/X`: no Hilbert
coupling, no compact core, no gauge. The obvious way for the recommendation to be
wrong is that the core contributes something the model cannot see.

This leg carries the same measurements to the **full gauged operator**, in a third
independent discretization (nodal spectral collocation with weighted sup norms;
v1, v2 and v3 were all coefficient-space). Two results:

1. **v3's far-field estimate stands.** It predicts the full inverse norm to within
   6% across the useful window, the optimum survives, and `Z₂` lands at 13.4
   against v3's predicted 13.3. The compact core costs almost nothing.
2. **The decay-graded sup pair does not control the quadratic term** — because the
   Hilbert transform is unbounded on `L^∞`. A decay grading alone is not a
   certificate space. It needs a *smoothness* component too.

Rebuild the figure from committed data:
`python writeup/4_p2_lottery/p2_route_d_v4_evidence.py` →
`writeup/figures/fig22_p2_route_d_v4_graded.png` (reads
`writeup/data/p2_route_d_v4_graded.json`; regenerate — deterministic, ~10 min —
with `python experiments/p2_route_d_v4_graded.py`).

Code: `solver/decay_collocation.py` + `test_decay_collocation.py` (6/6). Full suite
now **11 files green**.

---

## 1. Why a third discretization

The v1/v2/v3 layer (`solver/nk_fourier.py`) works in cosine coefficients, where the
operator is exact and banded. v3 established why that layer *cannot* carry the
decay grading: a function decaying exactly like `X^{-α}` with non-integer `α` is
only `C^α` at `θ = π`, its coefficients decay like `k^{-α-1}`, and a diagonal weight
sees smoothness rather than decay. A weighted **sup** norm sees decay directly. So
the graded pair wants a nodal discretization, and that is what
`solver/decay_collocation.py` is.

It is a spectral method, not a finite-difference one. On the midpoint grid
`θ_j = π(j+½)/J`, `X_j = tan(θ_j/2)` (reaching `|X| ~ 4J/π`), even functions are
represented exactly by their DCT-II coefficients, and on that space

```
H(cos kθ) = sin kθ  (exact) ,   d/dθ  (exact) ,   f_X = (1+cos θ) f_θ  (exact)
```

so `DF` is assembled as a dense `J × J` matrix with no quadrature and no finite
differences.

**Gates** (`test_decay_collocation.py`, all against independent oracles):
transforms exact to `1e-13`; the collocated residual, Jacobian and speed column
agree with the independently-written coefficient build `solver/nk_fourier` to
`2.6e-13` — the third construction of this operator in the project, and the second
time cross-building has been used as the primary correctness check; the anchor is
an exact zero (`6.5e-13`) and both closed-form kernel directions are annihilated;
the gauged square system inverts; and the collocated far field converges to the
exact operator like `J^{-2.1}…J^{-2.6}`.

---

## 2. The reproduction: v2's negative and v3's repair, a third time

`‖A‖_{Y→X}` for the gauged inverse, on a grid ladder:

| `J` | far field reaches | `‖A‖` ungraded (`α=0`) | `‖A‖` graded (`α=3/2`) |
|---|---|---|---|
| 125 | `X ≈ 159` | 11.91 | 3.794 |
| 250 | 318 | 13.26 | 3.892 |
| 500 | 637 | 14.62 | 3.973 |
| 1000 | 1273 | 16.00 | 4.029 |
| 2000 | 2547 | 17.39 | 4.069 |

Ungraded: `~J^{0.13}`, a steady **+1.37 per doubling** with no sign of stopping —
logarithmic divergence. Graded: `~J^{0.017}`, increments halving, settling at
`≈ 4.07`.

Worth noting the difference from v2: in unweighted `ℓ¹` on coefficients the
divergence was **linear** (`N^{0.97}`); in unweighted sup norms it is only
**logarithmic**. Different norm, much milder divergence, same verdict — unbounded
is unbounded, and no truncation certifies. The sup framing was already the better
half of the fix; the decay grading is the rest of it.

---

## 3. The compact core costs almost nothing

`‖A‖` against the decay class, with v3's far-field model law for comparison:

| `α` | 1.05 | 1.20 | **1.40** | 1.50 | 1.60 | 1.70 | 1.80 | 1.90 |
|---|---|---|---|---|---|---|---|---|
| full operator `‖A‖` | 4.07 | 3.81 | **3.54** | 4.07 | 5.06 | 6.58 | 9.29 | 14.39 |
| v3 far-field `2/|α−2|` | 2.11 | 2.50 | 3.33 | 4.00 | 5.00 | 6.67 | 10.00 | 20.00 |
| core excess | +1.97 | +1.31 | +0.20 | +0.07 | +0.06 | −0.08 | −0.71 | −5.61 |

Read the middle of the table. On `α ∈ [1.4, 1.7]` — exactly the window v3's optimum
picked out — the far-field model predicts the **full** gauged inverse norm to
within 6%, and to within 2% on `[1.5, 1.7]`. The model dropped the Hilbert
coupling, the core and the gauge, and lost almost nothing.

Two caveats, both honest. At `α ≥ 1.8` the negative "core excess" is not a core
effect at all: it is incomplete convergence in `J` (the `J`-exponent climbs from
`−0.001` at `α ≤ 1.4` to `0.108` at `α = 1.9`, and the finite-domain correction
near the resonance is `(X₀/X_max)^{2−α}`, which is 43% at `α = 1.9`,
`X_max ≈ 2500`). At `α ≤ 1.2` the excess is genuine: the core really does cost more
as the space gets weaker.

Which produces a result v3 could not have predicted: **the full `‖A‖` has its own
interior minimum, at `α ≈ 1.40`.** The far-field price rises toward the resonance
at `α = 2`; the core price rises toward `α = 1`. v3 found an interior optimum in
the *budget* from two constants pulling opposite ways; the same shape now appears
in `‖A‖` alone, from a completely different pair of mechanisms, and lands in the
same place.

---

## 4. The half of the space that is still missing

`Q(h) = h H(h)`, so

```
‖Q(h)‖_Y ≤ ‖h‖_X · sup (1+X²)^{1/2} |H(h)| ,
```

and the quadratic bound reduces to a **linear** question: is `H` bounded from `X_α`
to `X_1`? It is not. The Hilbert transform is unbounded on `L^∞` — the conjugate of
a bounded function with a jump has a logarithmic singularity — and no purely-sup
norm can escape that.

Measured with the explicit construction. Let `p_m` be the degree-`m` Fourier partial
sum of the even square wave `sign(cos θ)`: bounded by ≈1.18 (Gibbs), with
`‖H p_m‖_∞ ≥ (2/π) log m`, attained at the jump `θ = π/2`, i.e. at `X = 1`, where
*both* weights are `O(1)`. Then `h = f_α · p_m` gives

| degree `m` | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 |
|---|---|---|---|---|---|---|---|---|
| `C_Q` at `α = 1.5` | 0.74 | 1.00 | 1.26 | 1.53 | 1.81 | 2.10 | 2.40 | 2.73 |

**+0.41 per e-fold of degree** — logarithmic growth, unbounded, exactly as the
classical fact requires (the theoretical slope `2/π ≈ 0.64` is an upper estimate on
the pure conjugate; the measured slope is the weighted version).

**The methodological point, which cost a wasted measurement to learn.** The first
version of this test sampled *random* trigonometric perturbations of the same
degree. Those constants **fall** with `m` (1.40 → 0.84 over `m = 4…512`). Random
sampling does not find the unbounded direction — it is a measure-zero cusp in the
ball — so the first run reported the quadratic as comfortably bounded. Sampling can
demonstrate a *lower* bound and can refute a *proposed* bound; it cannot
demonstrate boundedness, and it certainly cannot demonstrate unboundedness. Only
the construction can. This is the ablation discipline of v2 D4 in a new costume:
you have to *build* the adversary, not hope to stumble on it.

### The unified statement across v3 and v4

This is the part worth carrying forward.

> **v3:** a diagonal weight on Fourier coefficients measures *smoothness*; we
> needed *decay*.
> **v4:** a weighted sup norm measures *decay*; we also need *smoothness*.

Two legs, two single-parameter families, each missing exactly what the other has.
The certificate's space must carry **both gradings at once** — decay, forced by the
far-field transport; smoothness, forced by the Hilbert transform — and no
one-parameter family of either kind has both. The natural candidates are weighted
Hölder `C^{0,γ}` spaces with a decay weight (Hölder is where `H` *is* bounded), or
a decay-adapted basis carrying a smoothness-graded `ℓ¹` on top. That is the v5
question, and — following the rule that has now paid off twice — it should be
settled on paper before any solver is written.

---

## 5. The price, confirmed, and what it leaves

Taking `C_Q` on the natural **smooth** family — the value a norm with a smoothness
component would deliver up to a constant, and the only honest input available until
that component is fixed:

| `α` | 1.20 | 1.30 | **1.40** | **1.50** | 1.60 | 1.80 |
|---|---|---|---|---|---|---|
| `‖A‖` | 3.81 | 3.66 | 3.54 | 4.07 | 5.06 | 9.29 |
| `C_Q` (smooth) | 2.91 | 2.33 | 1.93 | 1.65 | 1.44 | 1.17 |
| `Z₂ = 2‖A‖C_Q` | 22.2 | 17.0 | **13.6** | **13.4** | 14.6 | 21.7 |
| v3 far-field-only `Z₂` | 18.0 | 14.5 | 13.3 | 13.4 | 14.5 | 23.4 |
| budget ceiling `1/(4Z₂)` | 1.1e-2 | 1.5e-2 | 1.8e-2 | **1.9e-2** | 1.7e-2 | 1.2e-2 |

`Z₂^min = 13.4` at `α ≈ 1.5`, against v3's far-field-only prediction of 13.3 at
`α = 1.44`. The optimum is broad and it is where v3 said it would be.

The `C_Q` column also matches v3's closed form `(∫f_α)/π` to under 2% for
`α ≥ 1.3` — i.e. the far-field constant *is* the constant, on smooth data.

**But `1.9e-2` is a ceiling, not a result.** It assumes `Z₁ = 0`, and it prices no
smoothness component. The true budget is strictly smaller than this on both counts,
and the residual floor of an `a ≠ 0` profile is `~1e-2`. The margin is thin — thinner
than v3 already said, since v3's number was itself a ceiling.

---

## 6. Two operational findings

**The gauge must replace a *core* collocation equation.** The square system is
`[one normalization ; J−1 collocation rows]`, so one row is dropped. Which one
matters enormously:

| dropped row at | `X ≈ 0.001` | `X ≈ 0.4` | `X ≈ 1.0` | `X ≈ 1273` |
|---|---|---|---|---|
| `‖A‖` (origin gauge) | 4.03 | 4.41 | 5.70 | **1.06e5** |

Dropping a far-field row leaves the far field unconstrained and the inverse norm
explodes by four orders of magnitude. Among core rows the spread is 1.4×, and the
two gauges (`origin` vs `a0`) differ by 1.7× — a real but modest sensitivity, in
line with v2 D3's finding that the gauge is not where the difficulty lives.

**`Z₁` is quantified but not bounded.** Elements of the decay class are not
band-limited, so the collocation truncates them. Measured as the graded-codomain
error of the collocated `DF` against the exact operator:

| `α` | `J=250` | 500 | 1000 | 2000 | rate |
|---|---|---|---|---|---|
| 1.2 | 6.6e-3 | 1.8e-3 | 3.7e-4 | 9.3e-5 | `J^{-2.08}` |
| 1.5 | 3.3e-3 | 7.5e-4 | 1.2e-4 | 2.6e-5 | `J^{-2.36}` |
| 1.8 | 9.7e-4 | 1.9e-4 | 2.5e-5 | 4.3e-6 | `J^{-2.64}` |

It shrinks at a clean algebraic rate. It is **not bounded** here, and nothing in
this leg closes without it.

---

## 7. Honest ceiling

Everything is plain float64. Nothing is interval-enclosed, nothing is rigorous, no
rung of the ladder is climbed. What this leg did: confirmed that v3's far-field
pricing survives contact with the full operator (which was not obvious and could
easily have gone the other way), found that the core adds its own interior optimum
in the same place, and identified a second structural requirement on the
certificate's function space that neither v3 nor this leg has satisfied. Even the
eventual success it scouts would be a computer-assisted **toy-model** certification
in the Chen–Hou / Gómez-Serrano genre, at `a = 0`, where the profile is already
known in closed form. Clay odds ~0.05%.

---

### Reproduce

```
python test_decay_collocation.py                              # 6/6 gates
python experiments/p2_route_d_v4_graded.py                    # ~10 min, deterministic
python writeup/4_p2_lottery/p2_route_d_v4_evidence.py         # fig22 from committed data
```
