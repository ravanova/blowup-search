# The repair from last time doesn't work either. But now we know why — and the reason is a good one.

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The
[previous post](BLOG_P2_ROUTED_DRESS.md) ran a certification test that failed, found
the exact structural reason it failed, and ended with a proposed fix. This post
tests the fix. The fix doesn't work — and the way it fails turns out to be a
cleaner, more general statement than the thing it was supposed to fix. Still a toy
model. Still not a breakthrough.*

## Where we were

Quick recap. We have an exact solution to a simplified model — a travelling wave
profile, `Ω(X) = −1/(1+X²)` — and we want a computer-assisted **proof** that
solutions like it exist. The standard machinery (Newton–Kantorovich) needs four
numbers, and the whole thing dies unless all four are finite and small.

Last time, all four were computed in ordinary floating point and one of them was
catastrophically infinite. The culprit was found by ablation: the equation's
transport term carries a factor that **vanishes at spatial infinity**, and that
vanishing makes the linearized operator un-invertible in the space we were using.

That post ended constructively. The failure had a precise shape — the inverse
"loses exactly one power of decay" — and if you simply *measure the error in a
stronger norm*, one power stronger, the offending number becomes bounded and flat.
`‖A‖ = 3.000`, dead level across every truncation from 8 modes to 384. That looked
like the answer. The note said: rebuild in that pair of spaces.

It also said something more careful, which is the reason this post exists:

> the quadratic term has to land in the graded codomain too — do this on paper
> **before** coding, and if no consistent pair of spaces exists, that's itself the
> answer and the leg stops cheaply.

## The thing nobody had checked

Newton–Kantorovich juggles two spaces. Call them `X` (where your solution lives)
and `Y` (where the error you're trying to kill lives). Four requirements, but two
of them pull in opposite directions:

- **The inverse** wants `Y` to be *stronger* than `X`. Inverting a degenerate
  transport term loses decay, so the input has to supply the deficit up front.
- **The nonlinearity** wants `Y` to be *no stronger* than `X`. The equation has a
  quadratic term, and multiplying two functions doesn't make the product decay
  faster. Products are products.

Last time's proposal satisfied the first requirement. Nobody had checked it against
the second.

## The algebra takes an afternoon

First, a small identity that turns out to do all the work. The quadratic term in
our equation is `h·H(h)`, where `H` is the Hilbert transform. Written in Fourier
coefficients, you'd expect a mess of sum *and* difference frequencies. You get only
sums:

```
h H(h) = ½ Σ_m ( Σ_{j+k=m} h_j h_k ) sin(mθ)
```

A pure convolution. The reason is elegant: `h + iH(h)` is the boundary value of a
function that's holomorphic in a half-plane, and `2h·H(h)` is the imaginary part of
its *square*. Squaring a holomorphic function can only make frequencies add. The
difference terms cancel exactly.

(Small bonus: this gives a constant twice as sharp as the standard textbook bound
we'd been using. It changes nothing about last time's conclusion, but it's free.)

Now feed it a mode and a constant. Weighted spaces work by assigning a weight `u_k`
to mode `k` in `X`, and `v_m` to mode `m` in `Y`. Take `h` = (some mode `m`) + (the
constant mode). Their product contains mode `m` at full strength — the constant
mode multiplies everything without any decay whatsoever, `1·H(h) = H(h)`. So the
nonlinearity being bounded forces

```
v_m / u_m ≤ constant,    for every m.
```

The codomain can never be more than a bounded factor stronger than the domain.

And the inverse — measured, not assumed — needs

```
v_m / u_m ≥ (about 2) × m.
```

One is bounded. The other grows linearly. **There is no such pair of spaces.** Not
the one proposed last time; not any of them.

## Then you measure it, because a proof you haven't measured is a proof you might have got wrong

The algebra is cheap enough to be suspicious of. So: sweep the whole
two-parameter family of weights — domain weight `(1+k)^s`, codomain weight
`(1+m)^t` — and measure both requirements numerically across a ladder of
truncations.

Everything collapses onto a single variable, the **gap** `g = t − s`: how many
powers stronger the codomain is. And the two failure modes turn out to be exact
complements:

| gap `g` | −1.0 | −0.5 | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|---|---|
| how fast the inverse blows up | 1.96 | 1.47 | 0.98 | 0.50 | 0.04 | 0.00 |
| how fast the nonlinearity blows up | 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 1.50 |
| **sum** | 1.96 | 1.47 | **0.98** | **1.00** | **1.04** | 1.50 |

Read the bottom row. A certificate needs *both* numbers to be zero. Their sum is
never below **1**, anywhere in the family.

> **The one lost power is conserved.** You can move it from the inverse to the
> nonlinearity by re-grading. You cannot get rid of it. Choosing weights only
> chooses which of the two bounds pays.

That's a nicer statement than the thing it replaced. It isn't "the proposed repair
fails" — it's "an entire category of repairs fails, for one reason, and here is the
invariant that says so."

## The control

Same discipline as last time: a divergence is a suspicion, a divergence that
vanishes when you remove exactly one feature is an attribution.

So: take the offending factor `1 + cos θ` — the one that vanishes at spatial
infinity — replace it with `1`, change nothing else, re-run the entire sweep.

The inverse's requirement drops from `t ≥ s+1` to `t ≥ s−1`. That's **two powers**,
which is exactly right and is a satisfying check on the whole picture: a healthy
first-order transport term *gains* a power when you invert it, this one *loses*
one, and the difference of two is precisely the order to which `1 + cos θ` vanishes.
With the degeneracy gone, the two admissible regions overlap on a full unit strip
and the conserved quantity drops from 0.98 to **0.00**.

So the obstruction is this operator's far field. Not the method, not the `ℓ¹`
setting, not the arithmetic.

## Why weights were never going to work

Here's the part that reframes the last two posts. It was a **category error**.

A weight on Fourier coefficients measures *smoothness*. It does not measure
*decay*. The mode `cos(kθ)` equals `±1` at the point corresponding to spatial
infinity — it doesn't decay there at all, for any `k`, and no weight `u_k` can see
that. Decay lives in the *alternating* structure of the coefficient sequence, not
in any diagonal weight.

So asking a weighted-`ℓ¹` pair to express "loses one power of decay" was asking a
ruler to weigh something. The conservation law above is what that mistake looks
like when you measure it carefully.

## What actually works — and a design parameter nobody knew was there

Ask for decay directly. Let `X` be "functions decaying like `X^{-α}`" and `Y` be
"functions decaying like `X^{-α-1}`". Now check both requirements again.

The inverse: fine, by the far-field ODE, with norm `2/|α−2|`.

The nonlinearity: also fine — and this is the part the coefficient picture hides.
For any integrable `h`, the Hilbert transform decays like `(∫h)/(πX)` far away. So
`h·H(h)` decays **one power faster than `h`**. Exactly the gain the inverse needs.
Products don't gain smoothness, but they do gain decay.

Both requirements, satisfied simultaneously, in a pair of spaces that is not a
weighted-`ℓ¹` pair at all.

There's a price, and it has an interesting shape. The far-field inverse has a
**pole at `α = 2`** — and `X^{-2}` is exactly the decay rate of our anchor profile,
and exactly the homogeneous solution of the far-field equation. The natural choice
is precisely the forbidden one. You have to detune off it, and detuning costs
`2/ε`.

But you can't detune too far either: push `α` toward 1 and the nonlinearity's
constant blows up instead (the mass `∫h` diverges). Two constants pulling in
opposite directions gives an **interior optimum**:

| `α` | 1.1 | 1.3 | **1.4** | **1.5** | 1.7 | 1.9 |
|---|---|---|---|---|---|---|
| far-field inverse `2/(2−α)` | 2.2 | 2.9 | 3.3 | 4.0 | 6.7 | 18.7 |
| nonlinearity constant | 6.8 | 2.5 | 2.0 | 1.7 | 1.3 | 1.1 |
| product (the number that matters) | 30 | 14.5 | **13.3** | **13.4** | 17.2 | 40.3 |

`α* ≈ 1.44`, and `3/2` is within one percent of it.

So the answer to "which space?" is a concrete recommendation the previous post
couldn't have made: **certify profiles decaying like `X^{-3/2}`, with residuals
measured in `X^{-5/2}`** — deliberately *not* the anchor's own rate of `X^{-2}`,
which is the one every naive choice picks and the one where the machinery is
singular.

## Being honest about the number

The optimum gives a curvature constant of about 13. Run that through the
certification arithmetic and the largest tolerable error is of order `10^{-2}` —
and that's *before* paying for the parts of the calculation this leg didn't
estimate. The interesting case (a genuinely unknown profile, away from the exactly
solvable point) has an error floor of about `10^{-2}` too.

Which is to say: the margin, if there is one at all, is thin. That's the honest
read, and it's better to have it now, from an afternoon of algebra and a minute of
compute, than after building a two-region solver.

## The scoreboard

Everything here is ordinary floating point. Nothing is rigorous. Nothing is
certified. This is a **scoping** result: it retires an inference that looked
constructive, closes an entire category of function spaces with a proof and a
control, and hands the next attempt an address and a design parameter it didn't
know it needed.

The wider ceiling hasn't moved either. This is a one-dimensional toy model of the
boundary behaviour of a three-dimensional problem; even total success here would be
a computer-assisted certification of a toy, in a well-established genre. The
odds on the actual Millennium problem remain about 0.05%.

But that's what negative results are supposed to buy you: not progress toward the
summit, just an accurate map of which routes are cliffs. Two posts ago we learned
the naive route is a cliff. This post learns the obvious detour is also a cliff, and
— unusually — learns *why both are cliffs for the same reason*, which is the first
thing here that has felt like understanding rather than measurement.

---

*Figure: `writeup/figures/fig21_p2_route_d_v3_spaces.png`. Data:
`writeup/data/p2_route_d_v3_spaces.json`. Technical version with the proofs and
gates: [TECHNICAL_P2_ROUTED_SPACES.md](TECHNICAL_P2_ROUTED_SPACES.md).*
