# The wall has a name now — but only on part of the map

*Route-NG, leg 58. Companion to `TECHNICAL_P2_ROUTENG_V1.md`. Data:
`writeup/data/p2_route_ng_v1_nogo.json`. Figure: `fig55_route_ng_v1_nogo.png`.*

---

For seven legs this project has been walking into the same wall and describing it slightly
differently each time.

The setting: we are trying to build a computer-assisted certificate — the standard
radii-polynomial machinery — for a self-similar profile of an inviscid transport equation.
The machinery needs an **approximate inverse** `A` of the linearised operator, good enough
that `‖I − A L‖ < 1`. Everything else in the certificate had been made to work. That one
number would not go under 1. It kept coming out around 10, and the best we ever managed,
after spending every free choice in the construction, was **8.9591**.

Leg 54 spent the last of those free choices — the *shape* of `A` — across seven different
shapes, and reported the honest thing: a **1.167×** improvement where more than **8×** was
needed. That is a battery of measurements. It is not a theorem. And there is a real
difference between *"every `A` we tried failed"* and *"every `A` fails"*, which is exactly
the difference between a table and a result.

This leg's job was to find out which one we have.

## The answer was in the repository, in two halves

Leg 51 had established that the tail operator has a **kernel** — a direction it sends to
zero — and that this kernel, the far-field mode falling off like `1/|X|`, actually lives
inside the function space we work in. Leg 54 had noticed that on that one direction, one
block of the error `I − A L` collapses to something no choice of `A₁₂` can touch, and had
even written down the dual remark about the other block.

Nobody had put the two block-rows in the **same column** and taken the norm.

Do that and the proof is three lines. Feed the operator the vector that is zero on the
finite block and equal to the kernel `h` on the tail. Because `T h = 0`, two of the four
terms vanish *identically* — they involve `A₁₂` and `A₂₂`, and both get multiplied by `T h`.
A third vanishes if `A₂₁ = 0`. What is left is the kernel itself, coming straight back out:

```
(I − A L)(0; h)  =  (−A₁₁ B h ;  h)
```

and therefore, dividing by the norm of the input,

> **For every approximate inverse whose tail rows do not couple back to the finite block,
> `Z₁ ≥ 1`. At every split. In every weight class with `s < 1`. Whatever `A₁₂` and `A₂₂`
> are.**

`A₁₂` and `A₂₂` never enter the calculation. That is the whole trick, and it is also
precisely why the argument stops where it does.

## What this is worth, stated carefully

The class it covers — call it *block-upper-triangular* — is **strictly larger** than the
block-diagonal `A` the method conventionally uses. It contains the block-diagonal shape as a
single point, it contains a second shape leg 54 had measured separately, and it leaves two
of the three off-diagonal blocks completely free. It also has no restriction on the split
`K`, which the previous inequality did: that one carried a prefactor `|1 − K/2|` that
vanishes at `K = 2` and left a corner open. This closes it.

The class it does **not** cover is everything with `A₂₁ ≠ 0` — and that includes the shape
that gave leg 54 its best number.

So the honest summary is a two-line scope, and it is on the front of the technical writeup:

* **Proved:** no block-diagonal or block-upper-triangular approximate inverse can close this
  certificate.
* **Measured, not proved:** everything else. Leg 54's battery, bottoming at 8.9591, is the
  entire evidence.

## The part that is satisfying

You can measure exactly what breaking the hypothesis buys you. The one shape that couples
the tail back to the finite block — a rank-one lift of the far field — removes **one unit**
from that column and then stops. It buys back the kernel's own contribution, which is
precisely the term the theorem's hypothesis excludes. The rest of the column, the part
involving `A₁₁`, survives every admissible lift.

Measured across the sweep the credit is `0.9451 … 0.9990`, not a flat 1. That is worth
saying carefully, because the gap is the interesting part: on the infinite tail the credit
*is* exactly 1, and at a finite truncation it falls short by an amount that should be
proportional to the truncation error if the mechanism is what we think it is. It is. Across
all ten configurations the shortfall stays **below** the truncation defect `ρ_M` and tracks
it at a ratio between **0.856 and 0.997** — over a sweep in which `ρ_M` itself moves by a
factor of 66. The mechanism predicts the residue, on numbers nobody tuned.

## Two ways this could have been fooling us, and both were checked

**"You picked a bad split."** The obvious objection is that we chose to put the far-field
amplitude in the finite block, which is what leaves the tail block singular. Put it in the
tail instead and the tail block is invertible — objection dissolved?

No. That alternative is the *same operator with one index moved*, so we built it that way
and measured it. The tail block is indeed invertible at every truncation — and the norm of
its inverse **diverges** as the truncation grows, at exactly the rate `M^{1−s}`. Which is
the same exponent, with the opposite sign, at which the kernel defect vanishes in the
original split. Either the block has a kernel, or its inverse is unbounded. The obstruction
belongs to the operator, not to our bookkeeping.

**"Your hypothesis is unfalsifiable."** A no-go whose hypothesis always holds is not a
theorem, it is a description. So the hypothesis is put on a dial: add dissipation, and the
tail stops being a shift and becomes a multiplier with no kernel at all. Then the *same
class of approximate inverses* — the one the theorem says can never get below 1 — reaches
**0.6663** and then **0.4026**. The instrument can say yes. It says no here because the
answer is no.

## And a near-miss worth recording

The hypothesis needs the kernel to have finite norm in the working space. Checking that
across weight exponents, the partial sums at `s = 0.7` are still visibly climbing after
16384 modes — and a "has it converged yet?" test calls that a failure. It isn't one: the
increments are shrinking by a factor of `0.66` each rung, so the series converges, just
slowly. Meanwhile at `s = 1` the increments are *constant* — a logarithmic divergence
wearing the same costume.

Reading a boolean off those curves would have put a false negative on the one hypothesis the
whole result rests on. Reading the **increment ratio** instead separates them cleanly:
`0.25`, `0.38`, `0.66` converge; `0.9988` is log-divergent; `1.9974` is a power divergence.
*Report a magnitude, never a boolean* — this time applied to a convergence test.

## What it does not mean

It does not mean the underlying problem is settled, and it does not touch the Clay chain.
The object measured here is the `a = 0` CLM linearisation, a model whose certificate is
degenerate anyway — its residual is exactly zero for a trivial reason. A wall measured on
the easy object bounds the hard one's difficulty **from below**, and that is the only
direction the inference runs. Nothing here says anything about the non-symmetric Hou–Luo
profile, and **no link of the chain moved.** In 58 legs, none has.

What it does mean is that the repository now has one honest sentence where it used to have a
table — and a precisely drawn line showing where that sentence stops being true.
