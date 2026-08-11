# Fourteen rooms, one door: the fourth-space screen

*Leg 301, Route-FSB. Companion to `TECHNICAL_P2_ROUTEFSB_V1.md`. **Parked and escalated** —
nothing here is built, and no ban is lifted by it.*

---

A year ago this project banned itself from a technique. Not because the technique is bad — it is
the standard machinery of computer-assisted proof, and it works beautifully elsewhere — but
because we had tried it three times, in three different function spaces, and measured it dead
three times. The ban came with an unusually specific escape clause: it lifts *never*, unless
somebody names a **fourth** space we have not tried, and a scoping leg establishes that the
fourth space isn't subject to the same death.

Nobody had ever run that search. This leg ran it.

## Three deaths, not one

The first thing the screen refuses to do is treat "measured dead" as a single blur. The three
realizations died of three *different* mechanisms, and a fourth space has to survive all three.

**The first death was a zero.** In our weighted-`ℓ¹` Fourier basis, the unbounded part of the
operator has entries above and below the diagonal — and exactly nothing on it. Zero. That single
fact is the whole failure: the standard estimate works by making the tail's entries *small*, and
you cannot make a zero smaller. Bordering the matrix restores invertibility without touching
size, and the "constant" that argument needs turns out not to be a constant at all — it climbs
2.191, 3.234, 4.653, 6.530, 8.890, 11.528 as the truncation grows. The best shape we ever found
bought a factor of 1.167 where a factor of about 9 was needed.

**The second death was an inconsistency.** In the collocation realization, our discrete Hilbert
transform and our discrete derivative turned out to be discretisations of *different things* —
one of them quietly zeroes the endpoints. The mismatch is 2.04e+11 times the budget, and it does
not shrink when you refine the grid. Order 0.00.

**The third death was a profile.** The origin-`H²` space is genuinely good: it has a spectral
gap that survives truncation, and a tail inverse that converges where the `ℓ¹` one diverged. It
still fails, because everything usable in it descends from one identity satisfied by the exact
`a = 0` profile — an equation with no norm, no weight and no index in it. Our actual target is
not that profile and inherits none of it.

## The screen

Fourteen candidates went in: everything this repository has tried, plus everything the
certification literature offers that it hasn't. Each was checked against all three mechanisms by
a predicate over its structural facts, not by prose assertion.

Most died, and two of the deaths are worth reporting on their own.

A previous leg had already proposed a fourth space — a Gaussian-weighted Hermite basis — and its
argument about the *first* mechanism was correct and still stands. It dies on the *third*, to a
measurement a different leg had banked two legs earlier. The kill was already in the building.
It just had never been in the same table as the proposal. That is the entire value of an
enumeration.

And the sharpest result is a pair of rows that use the **same polynomials**. Chebyshev with the
obvious pairing gives a zero diagonal and dies. Chebyshev with the airfoil pairing gives an
exact `diag(−n)` and produced the only `Z₁ < 1` ever measured in this repository. Same family,
opposite fates. It is the pairing, not the basis, that decides — so any future proposal that
names a "basis" without naming its pairing has not actually named anything.

## The survivor

One candidate cleared all three: the **Malmquist–Takenaka** basis, also called the Christov
rational functions — a complete orthonormal basis of the line built out of rational functions
rather than waves.

Why it clears them is a single structural fact repeated three times. Half the basis spans the
Hardy space of the upper half plane and the other half its conjugate, so **the Hilbert transform
is exactly diagonal on it**: multiplication by `±i`. The differentiation matrix is tridiagonal
with diagonal `i(2n+1)` — non-zero everywhere, minimum modulus exactly 1, growing linearly. So
the first death cannot recur: there is no zero to be stuck with. Both operators are *exact* in
closed form on the basis, so the second cannot recur: the inconsistency is identically zero
rather than small and hopefully convergent. And none of this mentions a profile, so the third
cannot recur either. As a bonus, every basis function carries the same algebraic decay
`1/√(1+4x²)`, which means the basis expresses decay *in its own functions* rather than in a
weight — the exact repair for a category error an earlier route diagnosed and could not fix.

## The bill

Three things are against it, and they belong in the same breath as the result.

The dominance ratio is exactly 1. Not approximately — the computation gives
`(|n| + |n+1|)/|2n+1| = 1` at every single mode. The classical hypothesis wants it below 1/2. We
land on precisely the wall an earlier leg hit by hand. We do *not* score that as a death, and
the reason isn't optimism: this repository already **refuted** that ratio as the coordinate. We
measured an operator at ratio 2 — four times outside the hypothesis — that is still boundedly
invertible. The hinge is zero-versus-nonzero, and we have to use the coordinate we measured
rather than the one we disproved.

Second: nobody has ever done rigorous numerics in this basis. Anywhere. That's the novelty, and
it's also the invoice — there is no validated transform to inherit, so somebody has to build one.

Third, and most likely to kill it: this whole screen is about the *linear* operator's shape. The
nonlinear term is untouched. In a rational basis the quadratic term is not the clean convolution
a Fourier basis hands you, and whether the coefficient space is an algebra is simply unmeasured.
That is the third stage of the proposed scoping leg, and it is capable of ending the story.

## What happens now: nothing, deliberately

The gate answers yes, and a yes here is an escalation, not a licence. The ban's lift condition
asks for two things — a proposal, *and* a scoping leg that establishes the fourth space escapes
the three deaths. This leg supplies the first and writes the specification for the second. The
second has not been run.

So the ban stands exactly as it stood this morning. Nothing was built. No certificate was
assembled. No link of the chain moved, and the odds on the hard problem are the same 0.05% they
were before. What changed is only this: for the first time, the escape clause has a named
candidate standing in front of it, with its costs itemised and a control that reports the
opposite answer when pointed at the space we already know is dead.

That is a smaller thing than it sounds like. It is also the first time in a year the clause has
had anything in front of it at all.
