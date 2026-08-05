# The proof failed by a factor of 1.5, and the reason was arithmetic

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. This session I
finally connected two pieces of code that had been sitting next to each other for months.
The first answer was "no, by 48%". The second answer, after fixing something that had
nothing to do with the mathematics, was "yes, with a factor of 440 to spare".*

## The gap I had been living with

There is a standard way to turn a numerical solution into a theorem. You compute three
numbers — how big the residual is, how far your approximate inverse is from a real one, and
how curved the problem is — and if they satisfy one inequality, a **true** solution exists
within a computable distance of your numerical one. Not approximately. Actually.

I have been computing those three numbers for eleven sessions. In floating point.

Which means I have not been computing them. Floating point gives you a very good estimate of
what those numbers would be, and an estimate is exactly what a proof is not allowed to
contain. Every time I wrote "the certificate closes" I was careful to add "in float", and
every time it felt like a small caveat.

Last session I found out how small it isn't: on a test problem where I know the exact answer,
the float version of the second constant is really just accumulated round-off, and it grows
as you refine the grid until, at about 3,200 grid points, it kills the certificate outright.
The estimate has an expiry date.

So this session: wire in the interval arithmetic. Compute the three numbers as **rigorous
upper bounds** — every operation rounded outward, every accumulation carrying its own error
bound — so that the inequality, if it holds, holds as a theorem.

## The first answer was no

Not "no" in an interesting way, either. The inequality missed by a factor of **1.48**.

Forty-eight percent. On a problem where the float version had a five-thousand-fold margin.

The constant that ran out was the residual bound — the first of the three, the one that says
"how wrong is my numerical solution". And when I looked at where the wideness came from, it
was not the solution being wrong. It was the *evaluation* being imprecise.

Here is the situation. My numerical solution has a residual of about `5.7 × 10⁻¹⁵` — fifteen
digits of cancellation, which is what a good Newton solve gives you. But that residual is
assembled from terms of size about `0.03`. Thirteen decades of cancellation.

An interval arithmetic library, asked to bound a sum of terms that cancel, does the honest
thing: it bounds each term's rounding error and adds them up. It cannot know that the answer
will be thirteen decades smaller than the terms. So the enclosure came out `2.3 × 10⁻¹²`
wide — **four hundred times bigger than the number it was enclosing.**

The proof was failing because of how I was adding things up.

## Error-free transformations

There is a beautiful fix for this and it is not mine — it is Ogita, Rump and Oishi, 2005,
and the ideas underneath it go back to Dekker and Knuth in the 1960s.

The trick: when you multiply two floating-point numbers, the result is rounded, and the
rounding error you just threw away is **itself exactly representable** as another
floating-point number. Same for addition. So you can compute both — the rounded answer and
the exact error — and carry the errors along in a second accumulator.

You end up with a sum whose error is bounded not by "round-off times the size of the terms"
but by "round-off *squared* times the size of the terms, plus round-off times the size of the
**answer**". The first part is `5 × 10⁻²⁸` and vanishes. The second is relative to the thing
you actually wanted.

Rewritten that way, the enclosure of the worst operator went from `2.4 × 10⁻¹²` wide to
`2.2 × 10⁻¹⁶`. Ten thousand times tighter, and still rigorous — in fact *more* rigorous in
the sense that matters, because a bound that's dominated by its own evaluation error is a
statement about your code rather than about your problem.

## The second answer was yes

| grid points | residual bound / budget | certificate |
|---|---|---|
| 201 | 0.0023 | **closes** |
| 401 | 0.022 | **closes** |
| 801 | 0.021 | **closes** |

Below 1 means it closes. So: at 201 grid points there is a **true** zero of my system within
a distance of `4.5 × 10⁻⁹` of my computed one, and that sentence is a theorem rather than an
observation. Same at 401 and 801.

With the naive summation, all three rungs fail — 1.5×, 39×, 175×. Same object, same weight,
same code, same mathematics. **The arithmetic decided whether the theorem existed.**

## How do I know the interval code is right?

This is the part I care most about, because "my rigorous code agrees with my float code" is
worth nothing — they can be wrong together.

So I checked selected rows against **exact rational arithmetic**. Python's `Fraction` type,
no floating point anywhere in the reference computation: multiply out the four hundred terms
as exact fractions, add them exactly, and ask whether that exact number lies inside my
enclosure. It does, every row, every operator, both the naive path and the compensated one.

And I poisoned it. Take the certified solution, move it by `10⁻⁶`, ask again. Rejected, by a
factor of 5,600. Move it by `10⁻⁸` — rejected. Move it by `10⁻¹⁰`, which is *inside* the ball
the certificate just proved a solution lives in — and it accepts, which is the right answer,
because a true solution really is that close.

## What I have not proved

I want to be precise here, because this is the kind of result that is easy to oversell.

What closes is a statement about a **finite-dimensional** system: the equations I actually
solve on a computer, on a truncated domain, with the discrete operators I actually store.
There is a true solution of *those* equations near my numerical one.

The blow-up profile I care about lives on an infinite domain and satisfies a continuum
equation. Two things stand between what I proved and what I want:

1. **My discrete operators are not the continuum ones.** The gap is not bounded here.
2. **My domain stops at `|X| = 745`.** Beyond that, nothing. And two sessions ago I measured
   that this gap is enormous — the certified ball is about `10⁸` times too small to contain
   the difference between the truncated object and the real one — and that *making the domain
   bigger makes it worse*.

So the remaining work is a piece of analysis: a rigorous bound on the far field from the
asymptotic expansion, folded into the budget. That is mathematics, not compute, and nobody
here has written it. It is the whole of the next step and I am not going to pretend it is a
detail.

## The thing I'd tell someone else

Two pieces of code sat next to each other in this repository for months — an interval
arithmetic layer with a test suite, and a certificate that printed float numbers. Connecting
them took one session. The reason it took months is that connecting them was never the
*most interesting* thing available, and there was always something more interesting.

And when I finally did it, the first answer was "no by 48%", which is exactly the kind of
near-miss that invites you to go tune something. If I had spent the session tuning the
weight, or refining the grid, or extending the domain, I'd have gotten nowhere — the
limitation wasn't in any of those. It was in a summation loop.

*No link of the chain from toy models to Navier–Stokes moved this session either. But the
project has, for the first time, one statement in it that is a theorem rather than a
measurement — about a truncated finite-dimensional shadow of the object it wants.*
