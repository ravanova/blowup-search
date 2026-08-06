# It was never the operator. It was the room we put it in.

*Route-NGX, leg 127. Companion to `TECHNICAL_P2_ROUTENGX_V1.md`. Data:
`writeup/data/p2_route_ngx_v1_general.json`. Figure: `fig63_route_ngx_v1_general.png`.
Novelty pass: `writeup/novelty/leg_127.md`, run and committed before any construction.*

---

Eight legs ago this project started walking into a wall, and it has been describing that wall
in slightly different words ever since.

The setting, once more. We want a computer-assisted certificate — the standard
radii-polynomial machinery — for a self-similar profile of an inviscid transport equation. The
machinery needs an **approximate inverse** `A` of the linearised operator `L`, good enough that
`‖I − A L‖_w < 1`. That number is called `Z₁`. Everything else in the certificate works.
`Z₁` does not. The best we ever measured, after spending every free choice in the
construction, was **8.9591**, against the 1 it has to beat.

Leg 58 turned part of that into a theorem. It showed that if `A` has a zero in one corner —
the block called `A₂₁`, the one coupling the tail rows back to the finite block — then
`Z₁ ≥ 1` always. Not "in our experiments". Always. The proof is three lines and it works by
testing `I − A L` on a single direction: the far-field mode `h` that the tail operator sends
to zero. Because `T h = 0`, two of the three terms vanish, and what is left is `‖h‖`.

And that is exactly where it stopped. With `A₂₁ ≠ 0` a new term appears, `h − A₂₁ B h`, and
`A₂₁` can be chosen to cancel it. Leg 54's battery said that in practice this buys you almost
nothing — one construction drove the offending term to `10⁻¹⁶` and paid for it with a total
`Z₁` of **5.66 × 10⁵** — but "almost nothing in seven attempts" is a table, not a result.

This leg's job was to decide the general case. It decided it. The answer is yes — `Z₁ ≥ 1`
for **every** bounded `A`, with `A₂₁` completely free — and the interesting part is that the
argument we expected to need turned out to be the wrong argument entirely, and that the
result, once you have it, is not about the operator at all.

## The argument we planned, and why it failed

The plan, written into `DIRECTION.md` before the leg started, was a **two-direction** argument.
The intuition: `A₂₁` can buy you the kernel direction, but `A₂₁` also has to appear somewhere
else — in the tail-row images of the finite-block directions — and what it wins on one
direction it should pay for, with interest, on the other.

We carried it out. It gives

```
Z₁  ≥  1 / (1 + η),        η = ‖G⁻¹ B h‖_w / ‖h‖_w
```

and on this operator `η` settles at about **13.7** instead of decaying. So the two-direction
argument proves `Z₁ ≥ 0.068`, which is worth exactly nothing. The pre-registered plan was a dead end, and it
is written down here because that is what this repository does with dead ends.

## The argument that worked never mentions `A₂₁` at all

Here is the whole thing. For any `x`,

```
‖x‖  ≤  ‖(I − A L)x‖  +  ‖A‖ ‖L x‖
```

which is the triangle inequality and nothing else. Divide by `‖x‖` and take the best `x`:

```
Z₁  ≥  1  −  ‖A‖_w · σ_min(L),        σ_min(L) = inf ‖Lx‖/‖x‖ = 1/‖L⁻¹‖_w.
```

There is no `A₂₁` in that line because there are no blocks in it. `A` is never decomposed, so
there is no corner for the argument to get stuck in. **This inequality is not ours** — it is
the contrapositive, with a remainder, of the `Z₁ < 1 ⟹ invertible` hypothesis that every paper
in this field states on page one. The novelty pass established that first and forbade the
claim. What is ours is only the next question:

**Is this operator bounded below, or isn't it?**

Because if `σ_min(L) = 0`, that line reads `Z₁ ≥ 1` for every bounded `A`, and we are done.

## It isn't. And the sequence that proves it is one row wide

`σ_min` falls off like `M^−(1−s)` as the truncation `M` grows, where `s` is the weight
exponent of the space. Measured slope at `s = 0.3`: **0.6985**, against a predicted 0.7000.
At `s = 0`: **0.9925** against 1.0000. It does not matter where you put the split — across
`K = 2, 4, 8` the numbers move by under **0.3%**.

The vector that does it is not something a linear-algebra routine found. It is written down:
take the far-field kernel `h`, truncate it at `M`, and correct the finite block by solving
`G z = −B h`. Then:

- the finite-block rows of `L v` are **zero to floating point** (at most `1.2 × 10⁻¹⁴`);
- `z_K` is **exactly 0**, by a parity property of the recursion, which switches off the only
  entry coupling the finite block back into the tail;
- and the entire residual of `L v` sits in **one row** — the truncation edge at `m = M`, of
  size `|1 − M/2| · |h_M| · w_M ∼ M^(s−1)`.

Meanwhile `‖v‖` stays bounded, because `Σ m^(s−2)` converges for `s < 1`. A defect shrinking
like `M^(s−1)` divided by a norm that does not shrink is a rate of `M^−(1−s)`. That is the
whole proof, and it agrees with the numerically-optimal direction to ten digits.

We then tried to break it. Zero-pad the vector built at `M` into a tail four times larger — if
the near-null behaviour were an artifact of stopping at `M`, the ratio would jump back to
order 1. It costs a factor of **1.354**. Turn on dissipation, which gives the tail a diagonal
and destroys the kernel: `σ_min` stops falling and flattens completely (fitted exponent under
`3 × 10⁻³`, against 0.6985 in the same code path). The instrument can report the other answer.

And the bound is not lossy. Feed it leg 54's entire banked battery — 196 rows — and it holds
on all of them, with a minimum slack of **7.7 × 10⁻¹⁰**, attained exactly where theory says it
must be: at the exact inverse, where `‖A‖` equals `1/σ_min` and both sides are zero.

## What this actually costs a would-be counterexample

Stated as a magnitude rather than a verdict: any `A` reaching `Z₁ ≤ 1 − δ` must have

```
‖A‖_w  ≥  δ / σ_min(L)  ∼  δ · M^(1−s).
```

Be honest about what that does and does not exclude. At any **fixed** truncation the floor is
small — reaching `Z₁ = 0.99` at `M − K = 1024` needs only `‖A‖_w ≥ 6.64` — so a finite-`M`
counterexample is not excluded, and in fact leg 54 already built one: the exact inverse, whose
norm is `1/σ_min` on the nose. That is why leg 54 ruled it inadmissible. What is excluded is a
**single bounded `A` that works for every `M`**, and that is the only thing the method ever
meant by an approximate inverse. The floor grows by **1.99×** per doubling of `M` in the flat
class and **1.62×** at `s = 0.3`, without bound.

## The part that changes the story

Here is the finding that made this leg worth running, and it came from the novelty pass rather
than from the mathematics.

A preprint appeared in July 2026 — [arXiv:2607.19762](https://arxiv.org/abs/2607.19762), Jie
Xu — on **exactly this operator**: the `a = 0` CLM linearisation about the same exact profile.
It proves that on the origin-`H²` space, the point spectrum is exactly `{0, 1}` — the two
symmetry modes — and the essential spectrum meets the right half-plane only in the vertical
line `Re λ = −1/2`. Remove the two symmetry modes by the standard modulation, which is exactly
what our gauge row does, and **the operator is invertible, with a spectral gap of 1/2.**

So the operator is fine. It has a bounded inverse. It simply does not have one *here*, in the
weighted `ℓ¹` space of Fourier coefficients that the radii-polynomial method needs in order to
control its tail.

That reframes eight legs of negative results. The wall was never a property of the CLM
linearisation. It is a property of the room we insisted on putting it in — and we insisted
because that room is where this particular certificate machinery knows how to work. The
project's standing discipline has a lesson numbered 70 that says *name the realization*. This
is that lesson arriving as a literature fact instead of a note to self, and it is the reason
no sentence in this leg says the operator "has no bounded approximate inverse". It says: no
bounded approximate inverse **in `ℓ¹_w` at `s < 1`**.

There is a matching detail inside our own data. At `s < 1` the kernel is in the space and
`σ_min → 0`. At `s ≥ 1` the kernel leaves, and the exponent drops to zero — the wall is gone.
But at `s = 1.5` `σ_min` starts diverging again at a completely different rate, because a
*different* obstruction has taken over: the dual functional, the cokernel, has entered the
space. Two mechanisms, swapping at `s = 1`, and `s = 1` is precisely the exponent where the
object we actually want to certify has infinite norm. The space is squeezed from both sides,
which is the sharpest form of the thing this project has been circling since leg 51.

## What it does not say

Nothing here is about `HL_S2_nonsymmetric`, the real target. Nothing here moves any link of
the chain that leads to the Clay problem; no link has moved in 127 legs and none moved today.
The object is the `a = 0` CLM linearisation, whose `Y₀` is exactly zero for a degenerate reason
that certifies nothing. No dynamics were run. A wall measured on this object bounds the real
target's difficulty **from below**, not from above.

What did change: leg 54's scope line — *"`A₂₁ ≠ 0` is measured, not proved"* — is retired for
this operator in this space. It is proved now. The general class is closed, and the honest
statement of what was closed is that the certificate's **space**, not the operator, is where
this method runs out.
