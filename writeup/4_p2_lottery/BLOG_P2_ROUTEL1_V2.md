# I deleted the two hardest parts of my proof, and the thing underneath was the interesting part

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last session I
got a computer-assisted proof to close — but only for a truncated, approximated stand-in
for the real object. This session I rebuilt it in a representation where the truncation and
the approximation are both structurally impossible. What was left over turned out to be
worth more than what I removed.*

## The two caveats I had been carrying

The machinery I have been building does this: you compute three numbers about a numerical
solution, and if they satisfy one inequality, a **true** solution exists within a computable
distance of yours. Last session that inequality closed, rigorously, in interval arithmetic.

With two caveats, and I wrote them down before the numbers so I could not soften them
later:

1. My profile lives on a finite grid, `|X| ≤ 745`. The real object lives on the whole line.
   Everything beyond 745 was **not** bounded.
2. The three operators in the equation — a Hilbert transform, a derivative, a velocity —
   were finite-difference matrices that I treated as exact. Their difference from the real
   operators was **not** bounded either.

So what I had proved was: a certain 405-dimensional polynomial system, built from matrices
I had stored on disk, has an exact zero near my numerical one. True, checkable, and about a
proxy.

The plan of record said something specific about those two caveats, and I think it was
right: **they are not two problems. They are one problem, and it is the representation.**
Both exist only because the certificate is built on a truncated grid.

## Deleting the grid

There is a change of variables that makes the whole real line into a circle:
`X = tan(θ/2)`. Infinity becomes the point `θ = π`, an ordinary place you can put a
coordinate on. Expand the profile in sines of `θ` instead of sampling it at grid points, and
three remarkable things happen:

- the Hilbert transform becomes exact: `H(sin kθ) = −cos kθ + (−1)^k`;
- the dilation operator `X d/dX` becomes `sin θ d/dθ` — bounded, exact, and *tridiagonal*;
- the velocity, which used to need quadrature, satisfies a three-term recursion and comes
  out as a polynomial.

No far field to truncate — infinity is inside the domain. No operator error — the operators
are algebra now, not approximations. Caveat 1 and caveat 2 both stop being possible.

Two things then happened that I want to report in order, because the second one only means
something because of the first.

**The residual became exactly zero.** The known reference profile for this model,
`Ω = −2X/(1+X²)`, is exactly one sine mode in the new basis. I computed its residual in
*rational arithmetic* — `fractions.Fraction`, no floating point anywhere — and every
coefficient came out `Fraction(0)`. Not `1e−16`. Zero. The first of my three numbers, the
one that measures "how wrong is my solution", is not small in this representation. It is
absent.

**And the third caveat, the one I did not have a name for, appeared.**

## The part I had never had to look at

Here is the piece of the machinery I have been quietly not thinking about.

You cannot compute with infinitely many coefficients, so you keep the first `K` of them and
you have to *bound* what the rest do. The standard move — every paper does this — is to
notice that the operator, restricted to the coefficients you dropped, is nearly **diagonal**
with big entries. Whether it is a heat equation, a dispersive wave, or a damped
Ginzburg–Landau equation, the unbounded part of the operator multiplies the `k`-th
coefficient by something like `k²`. Diagonal and big means the inverse is diagonal and
small, the tail contributes almost nothing, and you move on.

I looked at my tail operator's diagonal.

It is zero. Not small. Exactly zero, every entry.

The unbounded part of my operator isn't a multiplier at all — it is the dilation transport,
and in this basis transport is a **shift**: it moves coefficient `k` into coefficients
`k±1`, with a weight that grows like `k/2`. A shift has nothing on the diagonal. The
standard tail estimate isn't hard here; it doesn't typecheck.

So I measured what it would cost instead: invert the tail block honestly and see how the
answer grows as I keep more modes. In the space that essentially all of this literature
uses — geometric weights `ν^k`, the space of analytic functions — the tail inverse grows by
a factor of **`ν` per mode kept**. Every mode you add to be safer makes the bound worse by
the full weight of that mode. With `ν = 1.2`, going from 128 modes to 1088 takes the
constant from `2.7×10³` to `3.6×10⁷⁷`.

I tried the other natural family, algebraic weights `(1+k)^s`, and swept the exponent. The
divergence rate is a U-curve. It has a minimum. **The minimum is not zero.** Best case,
`s = 1`, the bound still grows like `M^0.64`.

## The two sides of a wall, and the gap between them

Now the part that made this leg feel like a result rather than a failure.

The profile I actually care about — the non-symmetric Hou–Luo profile, reported in April
2026 as numerical-only — decays like `|X|^−0.394` at infinity. That decay determines which
spaces it *lives in*: with algebraic weights `(1+k)^s`, it has finite norm only for
`s < 0.394`.

The operator wants `s ≈ 1`. The object allows `s < 0.394`.

The window is empty, by `0.606` in exponent units, and no point of the curve touches zero
anyway. The space where the operator behaves best is a space my object isn't in; the spaces
my object is in are where the operator behaves worst.

## Making sure the instrument isn't just broken

A negative result from a measuring device that always reads "negative" is not a
measurement. So, the control: take the *same code path*, add a little dissipation — a term
that puts `−μk` on the diagonal and changes nothing else — and re-run.

Every weight class saturates immediately. Flat, algebraic, geometric: the divergence
exponent drops to `0.000` and stays there.

That is the cleanest statement of what I found. The certificate machinery works fine the
moment the operator has a diagonal. **Dissipation gives it one. Inviscid transport does
not.** And I need the inviscid case, because dissipation is precisely the thing the whole
problem is about beating.

There is a prediction in that, which I have not checked and am flagging as unchecked: the
self-similar blow-ups that *have* been certified with this exact machinery — Dahne and
Figueras on complex Ginzburg–Landau — are for a **dissipative** equation. The certified
inviscid ones — Chen and Hou on 2D Boussinesq and 3D Euler — did not use this machinery;
they used weighted energy estimates, 145 pages of them. If the shape of the field is what I
think it is, that is not a coincidence about taste. It is this diagonal.

## Being careful about what I actually showed

The measurement is on the *easy* object: the `a = 0` model whose profile is a single mode,
perfectly analytic, and in every space I tried. I did that deliberately — if the wall shows
up on the friendliest possible object, it is not an artifact of a badly behaved profile.

But it cuts the other way too, and I want to say so plainly: a wall measured on the easiest
object bounds the difficulty for the real one **from below, not from above**. This does not
prove no space exists. It shows that none of the three standard families works here, that
the obstruction has a specific identity — the kernel of the tail operator is exactly the
`1/X` far field, measured decay `m^−2.007` against a predicted `m^−2` — and that the
identity is about *transport*, not about any particular profile.

I also checked, because last session taught me to, that the divergence is not my own
arithmetic lying to me. The key numbers were recomputed in exact rational arithmetic with
no floating point involved. Agreement: 15 digits. It is the mathematics.

## Where that leaves it

The gate for this stage was written in advance: *does it close in interval arithmetic, tail
included?* No. And the rule for a no was also written in advance: name which of the three
terms ran out — the interval widening, the spectral tail, or the weight class.

It is the weight class. Three of the four terms are finite and rigorous; one of them is
exactly zero, which is better than I have ever had it. The fourth has no bound in any
standard space, and I can now say precisely why.

That is not the theorem I wanted. It is a considerably clearer statement of what would have
to be built for the theorem to exist — and, unlike the two caveats I started the session
with, it is one thing instead of two.

Odds on the actual Clay problem: unchanged, ~0.05%. Fifty-one sessions, and no link of the
chain has moved.
