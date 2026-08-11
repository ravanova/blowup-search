# The number was never wobbling. It was an identity all along.

*Route-EGRB v1 — leg 340. Figure: `fig89_route_egrb_v1_ladder.png`. Data:
`writeup/data/p2_route_egrb_v1.json`.*

## The argument we were having with ourselves

Two hundred legs ago this project computed a "weighted-energy coercivity gap"
for the `a = 0` Constantin–Lax–Majda operator and got `+0.4999930`. There is a
published ceiling at exactly `1/2` (Xu, arXiv:2607.19762), and a clause in our
own pass predicate that says the gap has to come in at or below `1/2 + 10⁻⁹`.
`0.4999930` is below `0.5`, so the clause passes — except leg 178, which owned
that measurement, answered **NO**, and the reasons why have been argued over
ever since. It has been a parked escalation for a long time.

Leg 329 re-ran the whole thing at 200 decimal digits. It found something
tantalising: evaluate the quadratic form directly at the computed maximiser,
node by node, in arbitrary precision, and you land **`5.19 × 10⁻¹⁸` below
`1/2`**. That is a one-sided upper bound, and it is under the ceiling. But leg
329 refused to claim it, and the decision-maker agreed, for a reason that is
worth stating plainly: **the same leg had measured how much the answer moves
when you change the truncation, and it moves by `3.85 × 10⁻⁵`.** A margin
thirteen orders of magnitude smaller than your own instrument's wobble is not a
margin. It is noise wearing a margin's clothes.

So the ask for this leg was: **compute that bound again, with the truncation
controlled.**

## The move

We stopped truncating.

Substitute `X = tan(θ/2)`. Then `sin kθ` and `cos kθ` become ratios of integer
polynomials in `X`; the Hilbert transform does too; the three weights we care
about become *exactly* `u³/(64X⁴)`, `u³/(2X⁴)` and `u²/(16X⁴)` with `u = 1+X²`;
and every integral in the Rayleigh quotient collapses onto a single classical
moment,

    ∫₀^∞ Xᵃ (1+X²)^(−M) dX  =  ½ B((a+1)/2, M−(a+1)/2),

which is a **rational number** when `a` is odd and a **rational multiple of π**
when `a` is even. So the whole quotient is

    R = (r₁ + q₁π) / (r₂ + q₂π),      r, q all exact fractions.

No mesh. No quadrature rule. No `rcond` cutoff. No eigensolver. No floating
point anywhere in the exact path. There is nothing left to be sensitive to.

None of this is clever — the half-angle substitution is centuries old and so is
the Beta function. It is just the right elementary tool, and nobody had pointed
it at this particular operator.

## What came out

At every one of nineteen rungs — four truncation sizes, four conditioning
cutoffs, four quadrature depths — for both of the two weights that matter:

    R = −1/2.

Exactly. The rational parts of both the numerator and the denominator come out
identically zero, so π cancels and the answer is a plain fraction. `−1/2`. Every
single time.

And then the structural check, which computes the whole matrix instead of one
number, and is the thing that actually settles it:

    Sym(B) = −G/2,  entry by entry, exactly.

The matrix pencil isn't *close to* `−I/2`. It **is** `−I/2`. The mechanism is
that the nonlocal term — the one carrying the Hilbert transform, the only place
the operator's difficulty lives — vanishes identically on the constrained class,
while the damping factor is identically `−1/2`.

So the literal question we were asked answers **yes**: the bound holds at every
rung, and its dependence on the truncation parameter is not "small", it is
**zero**.

## And here is the part that has to be said in the same breath

If the answer is an identity, then the clause we were testing **cannot come out
any other way.**

Not for any admissible trial function. Not at any truncation. Not in any
arithmetic. A test that one side always wins is not a test. This project has a
lesson written down for exactly this — *a control that cannot come out
differently is not a control* — and this is that lesson in its purest form, met
not as a suspicion but as an exact matrix identity we can print.

So: flipping our old **NO** to a **YES** on this clause would be flipping it
**on an identity**, not on a measurement of anything. Both readings are the
result. We committed, before running any of this, to reporting the second one
alongside the first, and we are not going to bury it now that the first one
looks exciting.

There is a genuinely useful corollary, though. Leg 178's `+0.4999930` is now
*fully* explained rather than merely suspected: the true value is exactly `1/2`,
the Gram matrix has condition number `2.6 × 10¹¹`, and the deficit is arithmetic
all the way down. The earlier "it's a float64 artifact" story was right. This
leg supplies the exact identity it was reaching for.

## What this is not

It is **not** a coercivity gap in any sense a proof could use. The estimate is
*saturated* — there is no slack left. A blow-up argument needs room to absorb a
perturbation, and an identity gives you none. It says nothing about `a ≠ 0`,
which is where Elgindi–Ghoul–Masmoudi's `−C|a|` term lives and where this
estimate genuinely does work. It moves no link in the roadmap. And the
underlying inequality is not ours: EGM's Proposition 2.1 already states the
`−1/2` coefficient at `a = 0`. All we own here is the measurement that it is
tight, exactly, and therefore uninformative as a test.

The long-parked escalation is a decision for a human, and it stays parked until
one is made. Leg 178's gate text is untouched, byte for byte.
