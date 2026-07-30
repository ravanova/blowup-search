# Phase-2 P2 — Route D v5: the two-grading space

**Status: Level-1 *tooling* + scoping. The obstruction v4 found is removed, and
one marginal direction is left, with a known fix. NOT a certificate.** Clay odds
unchanged (~0.05%).

The last two legs each found half of one requirement, and neither could satisfy it:

- [**v3**](TECHNICAL_P2_ROUTED_SPACES.md): a diagonal weight on Fourier
  coefficients measures **smoothness**; the far-field transport needs **decay**.
  No weighted-`ℓ¹` pair works, and the obstruction is a conservation law.
- [**v4**](TECHNICAL_P2_ROUTED_V4.md): a weighted **sup** norm measures decay and
  fixes the inverse — but the Hilbert transform is unbounded on `L^∞`, so the
  **quadratic** term is uncontrolled. Smoothness is needed as well.

So the certificate's space must carry both gradings at once. This leg builds it and
asks whether the two halves are compatible.

**They are.** The construction that broke v4 is defused; the smoothness exponent
turns out to have its own interior optimum, structurally identical to the decay
one; and the quadratic constant drops below 1 and stops growing. What is left is a
single **marginal direction** — at the codomain's critical decay rate the inverse
creeps logarithmically — which is the same marginality v3 already named at `α = 2`,
one level down, and which the same detuning fixes.

Rebuild the figure from committed data:
`python writeup/4_p2_lottery/p2_route_d_v5_evidence.py` →
`writeup/figures/fig23_p2_route_d_v5_holder.png` (reads
`writeup/data/p2_route_d_v5_holder.json`; regenerate — deterministic, ~10 min —
with `python experiments/p2_route_d_v5_holder.py`).

Code: `solver/holder_norms.py` + `test_holder_norms.py` (6/6). Full suite now
**12 files green**.


> **Update (Route-D v6, 2026-07-30).** Two claims below are superseded; see
> [TECHNICAL_P2_ROUTED_V6.md](TECHNICAL_P2_ROUTED_V6.md) / fig24. (i) The **joint
> optimum `(α,γ) = (1.8, 0.35)` is dead**: once the far-field part of `Z₁` is
> bounded it comes out 2.3–4.3 there, against a requirement of `< 1`, at every
> far-field cut tested; the optimum moves to `α ≈ 1.2`. (ii) Every operator norm
> below is a **family-restricted lower bound**, as this note says — v6 supplies
> the first genuine upper bounds for three of the eight constants, and shows that
> the obvious way to compute the rest (duality over a *discrete* Hölder ball) is
> unsound. Everything else here stands.

---

## 1. The space, and the exponent that is not a free choice

```
‖h‖_{α,γ} = sup_j w^{(α)}_j |h_j|
          + sup_{j≠k} min(w^{(α−γ)}_j, w^{(α−γ)}_k) · |h_j − h_k| / |θ_j − θ_k|^γ ,
w^{(β)} = (1 + X²)^{β/2} .
```

Two things about this deserve emphasis.

**The seminorm's weight is `α − γ`, not `α`, and that is forced.** The natural
far-field Hölder seminorm on the line is the conformal one, measured at the local
scale `|X − Y| ≲ 1 + |X|`:

```
[h] = sup (1+X²)^{(α+γ)/2} |h(X) − h(Y)| / |X − Y|^γ .
```

Under `X = tan(θ/2)` the Jacobian is *exactly* `dX/dθ = (1+X²)/2`, so for nearby
points

```
(1+X²)^{(α+γ)/2} |dh| / |dX|^γ  =  2^γ (1+X²)^{(α−γ)/2} |dh| / |dθ|^γ .
```

The `γ` in the numerator's exponent is eaten by the Jacobian. **The first draft of
this module used weight `α`** — and with that weight the model profile `f_α`
itself has an infinite seminorm, i.e. the space would not contain the objects the
certificate is about. The numerical conformal check is what caught it (gate 3),
which is the second time in three legs that a cheap consistency check has caught an
algebra error before it propagated into a conclusion.

**The compactified variable does the far-field bookkeeping for free.** After the
identity above, the whole weighted-conformal seminorm is a *plain* `θ`-Hölder
seminorm with a diagonal weight — no local windows, no scale-dependent pair
selection, one `O(J²)` broadcast. That is a real simplification and it is the
reason this leg was cheap enough to run at all.

The identity is checked pointwise and is `α`-independent (the ratio is the Jacobian
identity raised to `γ`, with `α` cancelling): agreement to **0.04%** out to
`X ≈ 121`, with the Jacobian itself to 0.06%. Beyond that the grid stops resolving
`X`-scales — consecutive far-field nodes differ in `X` by an `O(1)` factor — which
is the same limitation every far-field measurement in this project carries.

---

## 2. The v4 adversary is defused

v4's obstruction was concrete: `p_m`, the degree-`m` Fourier partial sum of the
square wave `sign(cos θ)`, stays bounded (≈1.18, Gibbs) while its conjugate grows
like `(2/π) log m`. In the sup norm the ratio `‖H p_m‖/‖p_m‖` grows without bound.
Measured in both norms:

| `m` | 8 | 32 | 128 | 512 | growth |
|---|---|---|---|---|---|
| **sup norm** (v4) | 1.80 | 2.56 | 3.31 | 4.07 | **×2.26** |
| Hölder, `γ = 0.15` | 1.13 | 1.16 | 1.19 | 1.60 | ×1.41 |
| Hölder, `γ = 0.35` | 1.04 | 1.02 | 1.01 | 1.00 | **×0.96** |
| Hölder, `γ = 0.50` | 1.02 | 0.98 | 0.92 | 0.85 | **×0.83** |
| Hölder, `γ = 0.85` | 0.97 | 0.90 | 0.81 | 0.74 | **×0.76** |

The sup ratio grows identically at every `γ` — it does not care about the decay
weight, which is exactly v4's point. The Hölder ratio is flat or falling as soon as
`γ ≳ 0.35`. The mechanism is not subtle: in a Hölder norm the adversary pays for
its own oscillation, since `[p_m]_γ ~ m^γ` sits in the denominator.

The failure at small `γ` is the expected degeneration — `γ → 0` *is* the sup norm,
so the obstruction has to come back, and it does.

---

## 3. Smoothness has its own interior optimum

The Hölder constant of `H`, measured over the adversarial family plus 300 random
trigonometric polynomials:

| `γ` | 0.15 | 0.25 | **0.35** | 0.50 | 0.65 | 0.75 | 0.85 |
|---|---|---|---|---|---|---|---|
| `C_H` | 1.60 | 1.21 | **1.12** | 1.13 | 1.18 | 1.20 | 1.29 |

A bowl, with the minimum at `γ ≈ 0.35–0.5` and the two ends rising for different
reasons: `γ → 0` is the sup norm where `H` is unbounded, `γ → 1` is Lipschitz where
`H` fails again. This is the *same shape* the decay exponent has (v4: `‖A‖` bowls
in `α` with a minimum at `α ≈ 1.4`, because the far-field price rises toward the
`α = 2` resonance and the core price rises toward `α = 1`).

> Two gradings, two interior optima, arrived at by four unrelated mechanisms. That
> the certificate's space has a *finite, interior* best choice in both parameters
> is the most encouraging structural fact these five legs have produced.

(Honest caveat: `C_H` is a measured max over a finite family, i.e. a lower bound.
The rise as `γ → 1` is real but under-resolved — the sampled family is not the
Lipschitz extremizer.)

---

## 4. The quadratic term, in the new norm

Same measurement v4 made, now in the two-graded pair, at `α = 1.5`:

| `γ` | 0.15 | 0.25 | **0.35** | 0.50 | 0.65 | 0.85 |
|---|---|---|---|---|---|---|
| adversary growth (m: 8→512) | ×1.63 | ×1.13 | **×0.77** | ×0.42 | ×0.24 | ×0.11 |
| `C_Q` (smooth family dominates) | 0.86 | 0.90 | 0.94 | 0.99 | 1.06 | 1.14 |

v4's number at `α = 1.5` was `C_Q = 2.73` at `m = 512` **and still climbing**. Here
it is below 1 and the adversary's contribution *falls* with degree. The
transition is at `γ ≈ 0.3`, consistent with §2.

---

## 5. The one marginal direction

The coarse `(α, γ)` sweep and a focused ladder disagreed about whether the inverse
norm settles in `J`, which is exactly the kind of disagreement worth chasing. The
cause is which test direction dominates. Feeding the inverse residuals
`g = f_{α+1+δ}` — `δ = 0` is *exactly* the codomain's critical decay rate, `δ > 0`
is strictly inside it — at `α = 1.5`, `γ = 0.5`:

| `δ` | `J=125` | 250 | 500 | 1000 | 2000 | exponent |
|---|---|---|---|---|---|---|
| **0.00 (critical)** | 1.956 | 2.223 | 2.471 | 2.691 | 2.879 | **+0.139** |
| 0.10 | 1.778 | 1.778 | 1.777 | 1.777 | 1.777 | −0.000 |
| 0.25 | 1.764 | 1.764 | 1.763 | 1.763 | 1.763 | −0.000 |
| 0.50 | 1.711 | 1.711 | 1.711 | 1.711 | 1.711 | −0.000 |
| 1.00 | 1.596 | 1.597 | 1.597 | 1.597 | 1.597 | +0.000 |

Every `δ > 0` is flat to **four significant figures across a 16× range in `J`**.
`δ = 0` creeps, with shrinking increments — a logarithm, not a power.

This is not a new phenomenon. It is v3's resonance, one level down. v3 found that
the far-field inverse produces a *logarithm* exactly at the critical exponent
(`α = 2`, the anchor's own decay rate) and a clean power otherwise, and its fix was
to detune. The same thing is happening at the boundary of the codomain class, and
the same fix applies:

> **Keep the residual class open.** Require the residual to decay strictly faster
> than `X^{−(α+1)}`, by any margin `δ > 0`. The cost is small and *decreasing* in
> `δ` (1.78 at `δ = 0.1`, 1.60 at `δ = 1`) — unlike v3's detuning, which cost
> `2/ε`, this one is nearly free.

The reason it is nearly free is worth noting: the detuning is on the **codomain**,
where a stronger requirement makes the operator norm *smaller*, whereas v3's
detuning moved the **domain** off its own kernel and paid for the near-degeneracy.

---

## 6. Where the joint optimum sits, and what it is worth

`Z₂ = 2‖A‖C_Q`, over the plane, restricted to the defused region `γ ≥ 0.35`:

| quantity | value |
|---|---|
| best `(α, γ)` | `(1.8, 0.35)` |
| `‖A‖` (family-restricted) | 2.45 |
| `C_Q` | 0.67 |
| `Z₂` | 3.29 |
| budget ceiling `1/(4Z₂)` | **7.6e-2** |

For comparison: v4's sup-pair numbers were `Z₂ = 13.4`, ceiling `1.9e-2`. The
two-graded pair is about **4× better** on this measure.

**Four reasons not to celebrate that number.**

1. `‖A‖` here is **family-restricted** — a lower bound. The exact induced norm
   between two polyhedral norms is a linear program, and this project has no LP
   (no scipy). So `Z₂` is a lower bound and the ceiling is an upper bound on an
   upper bound.
2. `C_Q` is likewise a max over a finite family.
3. `Z₁` is still **not bounded** anywhere in Route D.
4. The argmax sits at `α = 1.8`, the edge of the swept grid, and that row showed
   non-monotone behaviour in the coarse sweep (a negative growth exponent at small
   `γ`, which is an unconverged-`J` artifact near the `α = 2` resonance). The
   optimum's *location* is not firm; its *existence* is.

What can be said cleanly: in the two-graded pair the constants are single digits
rather than tens, both gradings have interior optima, and the obstruction that
killed v4 is gone.

---

## 7. What this changes for Route D

**Resolved.** v4's quadratic obstruction. The space that carries both gradings
exists, is cheap to compute in (thanks to the conformal identity), and its
constants are smaller than the sup pair's.

**Newly identified and fixed.** The critical-rate marginality, with a detuning that
costs almost nothing.

**Still open, and now the whole list.**

- `Z₁` — the truncation/tail term. Quantified in v4 (`J^{-2.1..-2.6}`), never
  bounded. This is the largest remaining gap and it is not a scoping question any
  more; it needs a genuine estimate.
- **Exact operator norms.** Everything here is family-restricted. Turning these
  into upper bounds needs either an LP or an analytic estimate of the
  Hölder-to-Hölder norms. The analytic route is more likely: the far-field block
  has a closed-form inverse and the core is finite-dimensional.
- **Interval arithmetic.** `solver/interval.py` has existed since v1 and has still
  never been pointed at any of this — correctly, since nothing has closed in float.
- **`a ≠ 0`.** No exact anchor, residual floor `~1e-2`, and the budget ceiling here
  is `7.6e-2` *before* the four caveats above are paid.

---

## 8. Honest ceiling

Everything is plain float64. Nothing is interval-enclosed, nothing is rigorous, no
rung of the ladder is climbed. Five legs of Route D have produced: a validated
interval core (unused), an exact Fourier operator, a structural negative with a
mechanism, a no-go theorem for an entire category of spaces, a confirmed far-field
price, and now a space in which every requirement identified so far is
simultaneously satisfiable. That is real progress on *scoping*, and it is not a
certificate of anything. Even complete success would be a computer-assisted
toy-model certification in the Chen–Hou / Gómez-Serrano genre, at `a = 0`, of a
profile already known in closed form. Clay odds ~0.05%.

---

### Reproduce

```
python test_holder_norms.py                                   # 6/6 gates
python experiments/p2_route_d_v5_holder.py                    # ~10 min, deterministic
python writeup/4_p2_lottery/p2_route_d_v5_evidence.py         # fig23 from committed data
```
