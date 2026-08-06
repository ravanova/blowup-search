# Phase-2 P2 — Route D v6: the first genuine upper bounds, and the discrete-ball trap

**Status: Level-1 *tooling* + the project's first **upper** bounds on Route-D's
Newton–Kantorovich constants — NOT a certificate.** Five legs built the space
(v3 the decay grading, v4 the price, v5 the smoothness scale) and measured in it.
Every one of those numbers was a *family-restricted* maximum — a **lower** bound —
and `Z₁` was never bounded at all. A budget assembled from lower bounds is not a
quantity a certificate can use, so this leg attacks the two gaps the v5 note
named: bound `Z₁` from the closed-form far field, and turn the family-restricted
operator norms into genuine upper bounds analytically.

The second half turned out to be **half right and half a trap**, and the trap is
the leg's most useful output. Clay odds unchanged (~0.05%).

Rebuild the figure from committed data (no re-derivation):
`python writeup/4_p2_lottery/p2_route_d_v6_evidence.py` →
`writeup/figures/fig24_p2_route_d_v6.png` (reads
`writeup/data/p2_route_d_v6_bounds.json`; regenerate — deterministic, ~10 min —
with `python experiments/p2_route_d_v6_bounds.py`).

Code: `solver/nk_bounds.py` + `test_nk_bounds.py` (6/6). Suite now **13 files
green**.

---

## 1. The discrete-ball trap (fig24-A)

The obvious way to turn a family-restricted lower bound into an upper bound is
duality. The domain norm is a max of linear functionals, so

    ||A|| = max over those functionals of ||functional ∘ A||_{Y*} ,

and `‖·‖_{Y*}` is a supremum over the codomain unit ball — which, on a grid, one
computes over the **discrete** unit ball. That is unsound, and not marginally.

A discrete Hölder seminorm only inspects pairs of **grid nodes**. A grid vector
that alternates in sign at the grid scale therefore reports a modest seminorm,
while the trigonometric interpolant it actually stands for oscillates violently
*between* nodes. Duality, asked for the worst direction, picks exactly such a
vector. Measured on the extremizer it selects, comparing both norms over the same
`θ`-range:

| `J` | inflation `‖·‖_continuum / ‖·‖_discrete` | smooth control |
|---|---|---|
| 125 | 3.0 × 10³ | 1.028 |
| 250 | 1.2 × 10⁴ | 1.027 |
| 500 | 5.0 × 10⁴ | 1.027 |

**`~J^2.03`.** A smooth element of the same decay class is faithful to 3%. The
"worst direction" is not in the true unit ball at all, and the unboundedness it
reports is the instrument's, not the operator's.

This is banked lesson (9) — *build the adversary* — meeting its mirror image. In
v4, random sampling **missed** the adversary and reported a boundedness that was
false. Here a discrete norm **invents** an adversary and reports an unboundedness
that is false. A test family that is too small errs one way; a ball that is too
big errs the other. Both are the instrument.

## 2. What survives: duality from continuum-valid inequalities (fig24-B)

The sound route is to use only inequalities the **continuum** norm implies. Both
of

    |g_m| ≤ ‖g‖_Y / v_m ,        |g_m − g_{m₀}| ≤ ‖g‖_Y / q_{m,m₀}

hold for the continuum norm, because it dominates the discrete one on nodal
values. Applying them to a functional row `c` and minimising over a reference
index gives

    ‖c‖_{Y*} ≤ min_{m₀} [ |Σ_m c_m| / v_{m₀} + Σ_m |c_m| / q_{m,m₀} ] ,

`two_point_dual`. Minimising over a *subset* of `m₀` keeps it valid (a min over
fewer terms is larger), so it stays cheap. On the two parts of the domain norm:

| `J` | domain **sup** part (upper) | domain **seminorm** part (upper) | v5 family (lower) |
|---|---|---|---|
| 125 | 5.536 | 17.2 | 2.25 |
| 250 | 5.531 | 24.2 | 1.35 |
| 500 | 5.528 | 34.2 | 2.52 |
| 1000 | 5.580 | 48.3 | 2.73 |
| 1600 | 5.631 | — | 2.85 |

The sup part **saturates**: `J^{+0.006}` over a 13× range in `J`. That is the
project's first uniform **upper** bound on any part of `‖A‖`, and it brackets the
v5 family-restricted lower bound (~2.2–2.9) by about a factor 2.

The seminorm part grows like `J^{+0.496} ≈ J^γ`. It is a *valid* bound, so this is
slack, not a verdict — and §1 identifies the slack precisely: the direction it
prices is the grid-scale sign pattern that is not in the continuum ball. The
continuum expectation is that this part is comfortably finite, because the inverse
gains a whole derivative (`h_X = −(g + H(h) + X h)/c`, so `g ∈ C^{0,γ}` puts `h`
in `C^{1,γ}`). Three routes were tried — the direct pair dual, the two-point dual,
and bounding the seminorm through `‖h_θ‖` — and all three grow. **Closing this is
now the sharpest open question in Route D.** (It is not the gauge: every
gauge-row choice tested gives the same `J^γ`, with the innermost row merely the
smallest constant, consistent with v4 W5.)

## 3. The far-field modelling error, in closed form (fig24-C)

v3's far-field model is `L h = −c h_X − h/X`, whose inverse norm between the
decay-graded sup norms is exactly `2/|α−2|`. The full linearization at the anchor
`Ω₂ = −1/(1+X²)`, `H(Ω₂) = −X/(1+X²)` is `DF h = h H(Ω₂) + Ω₂ H(h) − c h_X`, so
the modelling error is an exact two-term identity:

    (DF − L) h = h [H(Ω₂) + 1/X] + Ω₂ H(h)
               = h / (X (1 + X²))  −  H(h) / (1 + X²).                      (E)

Verified against the collocation operator to **1.5 × 10⁻¹⁶ relative**.

The first term is pointwise. The second needs `|H(h)|` in the far field for an
*arbitrary* `h` in the unit ball — exactly where v4's adversary lives, and exactly
what the Hölder grading was introduced to pay for. Splitting the principal value
at half-scale on the **even** kernel `K(X,y) = 2X/(X²−y²)`:

    |H(h)(X)| ≤ (1/π) [ I_near(X) + I_out(X) ] ,
    I_near ≤ (4/3) S 2^γ (X/2)^γ / γ + (8/15) (1+(X/2)²)^{−α/2} ,
    I_out  = ∫_{y≥0, |y−X|>X/2} (1+y²)^{−α/2} |K(X,y)| dy ,

with `S = 2^γ (1+(X/2)²)^{−(α+γ)/2}` the X-side Hölder envelope (v5 fixed the
seminorm weight at `α−γ` in `θ`; converting with `|dθ| ≤ 2|dX|/(1+X_min²)` makes
the X-side weight `α+γ`, not `α−γ`).

Using the **even** kernel is not cosmetic. A two-sided `1/(X−y)` split diverges
logarithmically as `X → 0` — where the true value is `0`, since `H` of an even
function is odd — and loses a factor 2 in the far field. The even form is finite
at the origin and recovers the sharp constant: `X · bound → 1.681` against
`M_α/π = 1.669`.

Feeding this into (E) and taking the supremum over `X ≥ X₀` gives the **first
bounded piece of `Z₁` in six legs**. Validated against the collocation operator
on nodes the grid resolves in `X` (`|X| dθ ≤ 1`, the project's standing
convention) over an adversarial test set:

| `X₀` | measured | bound | headroom |
|---|---|---|---|
| 20 | 1.85 × 10⁻¹ | 5.62 × 10⁻¹ | 3.0× |
| 50 | 1.81 × 10⁻¹ | 3.12 × 10⁻¹ | 1.7× |
| 100 | 1.81 × 10⁻¹ | 2.05 × 10⁻¹ | 1.1× |

and it decays at the predicted rate `X₀^{α−2}` across the whole grading range
(measured −0.874, −0.815, −0.740, −0.653, −0.556, −0.453, −0.347, −0.240 for
`α = 1.1 … 1.8`, against predicted −0.9 … −0.2).

The same `|H(h)|` bound gives the first upper bound on the quadratic constant:
`C_Q ≤ sup_X (1+X²)^{1/2} · bound(X)`, finite because the bound decays like
`M_α/(πX)`. At `α = 1.5, γ = 0.5` it is **3.13**, against v5's family-restricted
lower bound of 0.86–1.14.

## 4. Pricing `Z₁` moves the optimum (fig24-D)

`Z₁` has never before entered the optimization, and it changes the answer.

| `α` | `‖A‖_far` | `C_Q` (upper) | `Z₂` | `Z₁` @ `X₀`=200 | @800 | @3200 | budget @3200 |
|---|---|---|---|---|---|---|---|
| 1.1 | 2.22 | 6.16 | 27.4 | 0.100 | 0.030 | 0.009 | 8.97 × 10⁻³ |
| **1.2** | 2.50 | 4.11 | 20.6 | 0.141 | 0.046 | 0.015 | **1.18 × 10⁻²** |
| 1.4 | 3.33 | 3.36 | 22.4 | 0.329 | 0.134 | 0.056 | 9.94 × 10⁻³ |
| 1.5 | 4.00 | 3.13 | 25.1 | 0.548 | 0.255 | 0.123 | 7.68 × 10⁻³ |
| 1.7 | 6.67 | 2.79 | 37.2 | 1.92 | 1.20 | 0.775 | 3.41 × 10⁻⁴ |
| 1.8 | 9.96 | 2.66 | 53.0 | 4.32 | 3.13 | 2.34 | **0** |

Two things stand out.

**v5's joint optimum is dead.** At `α = 1.8`, `Z₁` is 2.3–4.3 — not near the 1 it
must beat — at every `X₀` tested. The reason is structural: the modelling error
decays like `X₀^{α−2}`, so at `α = 1.8` the far field must be pushed out `10⁵`×
further to buy what `α = 1.2` gets for free, while `‖A‖ = 2/(2−α)` is
simultaneously blowing up toward the `α = 2` resonance. Both of v5's knobs were
tuned against constants that did not include `Z₁`.

**The optimum moves to `α ≈ 1.2`**, and the conditional budget there is
`1.18 × 10⁻²`. That number invites a comparison that must be made carefully: the
GA residual floor at the `a ≈ 0.5` two-scale boundary (measured on `a > 0`) is also `~10⁻²`. The two
being the same order is **not** a statement that the boundary profile could be
certified. The budget above is *conditional* and *optimistic* — it prices only
the far-field part of `Z₁`, uses the far-field `‖A‖` (v4 confirmed that predicts
the full gauged `‖A‖` to 6% on `α ∈ [1.4, 1.7]`, which is not the range the
optimum now sits in), and omits three constants entirely. The honest reading is
that the target is no longer obviously out of reach by orders of magnitude, which
is a change from v5, and nothing more.

## 5. The ledger

| constant | status | note |
|---|---|---|
| `Y₀` (at the `a=0` anchor) | **exact** | the anchor is an exact zero |
| `Z₀` | **bounded** | finite-block rounding (~10⁻¹¹) |
| `Z₁` far-field modelling error | **bounded (new)** | closed form, `X₀^{α−2}`, 1.1–3.0× headroom |
| `Z₁` core ↔ far-field coupling | open | sharp split has a `1/(X−X₀)` seam; needs a smooth cutoff + a commutator estimate for `H` |
| `Z₁` core discretization | measured only | v4 W6: `J^{−2.1…−2.6}` |
| `‖A‖` domain **sup** part | **bounded (new)** | two-point dual, uniform in `J` (5.53) |
| `‖A‖` domain **seminorm** part | open | three routes, all valid but lossy (`J^γ`) |
| `C_Q` sup part | **bounded (new)** | same `|H(h)|` bound; the codomain seminorm of `hH(h)` is not bounded |

**Three of eight moved from *measured* to *bounded*. Three remain open**, and
they are now named precisely enough to be attacked one at a time rather than
scoped.

## 6. Honest ceiling

Everything here is plain `float64`: analytic bounds with numerically evaluated
constants, gated against measurements. Nothing is interval-enclosed and nothing
is rigorous — `solver/interval.py` has existed since v1 and still has not been
pointed at any of this, correctly, because nothing has closed in float. This leg
does not climb the rigor ladder; it converts three of the eight constants from
things we had measured into things we can bound, kills one candidate optimum,
and disqualifies one method. Even the success it is scouting would be a
computer-assisted *toy-model* certification (Chen–Hou / Gómez-Serrano genre), not
a Clay solve. 1D HL remains a toy model of the boundary behaviour of Hou–Luo /
3D axisymmetric Euler. Overall Clay odds ~0.05%.
