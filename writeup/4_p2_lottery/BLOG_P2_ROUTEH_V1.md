# The case where scaling tells you nothing

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The two
previous posts measured where viscosity starts winning. Both ended at the same sentence:
"and at the critical point exactly, this argument returns no information." That point is
where Navier–Stokes lives. This post is about going there anyway. Still a toy model.
Still not a breakthrough.*

## Why the empty answer is the whole problem

The standard way to ask whether viscosity stops a blow-up is to compare two terms. The
nonlinear term wants to concentrate; the dissipative term wants to spread. Write down
how each scales as the solution collapses, compare the powers, and you get a threshold —
above it viscosity wins, below it the blow-up survives.

For Navier–Stokes the two powers are **equal**. Not close: equal, by dimensional
analysis, exactly. The comparison gives `0 = 0`.

This is what people mean when they say NS is *critical*, and it is a much more specific
statement than "the problem is hard". It says a particular, powerful, cheap tool returns
a blank. Everything else about the problem is downstream of that blank.

The previous two legs of this project measured that threshold in a toy model where you
can dial it around, confirmed it against an independent instrument, ported it to a 2D
system, and found — as expected — that the toy hits the same blank at its own critical
point. Which left the obvious question unasked: **what actually happens there?**

## The move: make the viscosity a variable

Here's the trick, and it's the only real idea in this post.

When you zoom in on a collapsing solution — rescaling as it shrinks so the shape stays
put — the viscous term doesn't vanish and doesn't stay fixed. It comes back multiplied
by a number that depends on how far you've zoomed. Call that number `μ`. Most treatments
regard it as a nuisance parameter.

Treat it as a **coordinate** instead. Then the zoomed-in system has one more equation:

    dμ/dτ = (2s − α) μ

where `s` is the viscosity's exponent and `α` describes how the collapsing profile falls
off far from the singularity. Now everything is a dynamical system in `(shape, μ)`, and
two things fall out immediately.

**First: the threshold was an eigenvalue all along.** The rate `2s − α₀` is the growth
rate of `μ` near the inviscid solution. Negative means `μ` decays and viscosity is
irrelevant; positive means it takes over. The threshold is where it changes sign. A
scaling exponent has turned into a stability exponent — same number, but now it belongs
to an operator instead of a dimensional-analysis argument.

**Second: at criticality the eigenvalue is zero, which is not the end but the beginning.**
When a linear term vanishes, you look at the quadratic one. Expand `α` in `μ`:

    dμ/dτ = −α₁ μ² + …

and the whole marginal case is now the **sign of one number**, `α₁`. Positive: `μ` still
decays, but as `1/τ` instead of `e^{−cτ}` — algebraically, because the fast term is gone.
Negative: viscosity runs away and there's no self-similar collapse. Zero: a whole family
of viscous blow-ups sitting side by side.

That's the reduction. One number instead of a blank.

## Measuring it

Two places in this family let you pose the critical problem exactly, and at both of them
the answer is checkable.

**At `a = 0` there's a closed form.** The equation reduces to a complex Burgers equation
whose characteristics are a constant shift into the imaginary direction, and out drops an
exact viscous blow-up in elementary functions — for *every* viscosity, and every member
of a one-parameter family. Which means `α₁ = 0` there: a line of viscous self-similar
blow-ups, neutral not just to leading order but exactly.

That's the gate. The numerical machinery, which does not know the closed form, solves the
rescaled equation from a cold start and lands on it to fifteen digits, at values of `μ`
where the viscous term is four times the size of everything else. The far-field exponent
comes back as `1.00000000000000` at every single `μ`.

**At the next point the degeneracy breaks**, and there's a trap worth naming. `α(μ)` is
curved, so if you fit a straight line to it over any finite window you get the *chord*,
not the slope at zero. That's a 5.5% error in the one number the whole verdict rests on.
Fitting the secants and extrapolating them to zero instead:

| grid size | `α₁` |
|---|---|
| 96 | 0.132770 |
| 144 | 0.133470 |
| 192 | 0.133628 |
| 240 | 0.133683 |

Stable in the fourth digit, and **positive**. So at criticality `μ` decays — and the
reflex reading ("more dissipation means more dissipation") is backwards. There's a unit
test that checks the *sentence*, in words, because I do not trust myself to keep the sign
straight.

But look at the *rate*. Algebraic decay means taking `μ` from 0.2 down to 0.02 costs
`τ = 337`, and going one more decade costs `τ = 3703`. Nine times as long per decade,
forever — and `τ` is itself a logarithm of the time remaining. So the critical viscous
solution does relax onto the inviscid one, and does so impossibly slowly. That's the
texture of criticality: not a barrier, a tar pit.

## The third point nearly shipped the opposite answer

There's a third place where the critical problem should be exactly posable, and this is
the part of the leg I'd most want someone to read.

At a finer grid it *looks like it works*. The solve converges to about `4e−4`, which is
an unremarkable residual, and the slope comes back **negative** — the opposite verdict.
That's a headline: "the answer flips at the third point."

It's not a measurement. The entire movement of the quantity being differentiated, across
the whole window, is `0.00002` — **twenty times smaller than the error bar of the solve
it came out of.** I was fitting a derivative to something well below my own noise, and
getting a confident sign out of it.

What makes this worth writing down is that the obvious guard doesn't catch it. "Did the
solve converge?" is the check you reach for, and `4e−4` passes any threshold you'd have
picked in advance without knowing the answer. The check that catches it is a different
question:

> Is the thing I'm measuring bigger than the error in what I measured it from?

That's now the gate, and it's unit-tested against these exact numbers — including a test
that the sign it *would* have quoted is a real sign, so the trap stays live rather than
becoming a story about a trap.

The underlying reason it fails is also a correction to something I'd written. The
operator needed there is a *fifth* power, built by composing five copies of something
that each time pushes a little energy off the end of the basis. At the fifth power the
discarded part is **three to four orders larger than the part you keep**. The "lucky
alignment" I put in the module's own documentation — that landing on these special
points makes everything exact — is true about the operator being *finite* and false
about it being *accurate*. It buys the first and third powers, not the fifth. Refining
does help, roughly as the fourth power of the grid size, but from so far up that you'd
need a grid around 3000 to get there. I corrected the docstring rather than quietly not
mentioning it.

So there is no third data point. The trend from two points is a trend from two points,
and an earlier leg in this project already paid for forgetting that.

## The interesting negative

An earlier leg tried a different attack — looking for solutions that repeat themselves at
geometrically shrinking scales — and shut it down with a mechanism rather than a shrug.
The relevant operator turned out to have almost no isolated eigenvalues at all. Its
spectrum is a *continuum*, and a continuum has nothing discrete in it that could move,
collide, and spiral off into the complex plane the way a bifurcation needs.

Critical viscosity is exactly the perturbation that could repair that. So: does it?

**Yes.** Turning `μ` on takes the count of grid-converged eigenvalues from 2 to 8, and
they arrange themselves on the negative integers — a clean ladder condensing out of what
was a continuum. The mechanism that shut the lane is genuinely gone.

**And the lane stays shut anyway**, which is a better place to be than before. Everything
that condenses out lands on the negative real axis. Nothing reaches the right half plane
(worst value: `3e−13`, i.e. zero). Nothing goes complex — the two values my code first
flagged as complex turned out to be a degenerate real pair split by `0.000018`, which is
noise wearing a costume. I changed the driver to report the size of the imaginary part
instead of a yes/no, because the yes/no said "yes" and it was wrong.

One mode does move: the amplitude mode slides from `−1` out to `−√(1+4μ)`, fitting to
nine digits. It moves **left**. More stable, not less.

The claim "nothing crosses" is an absence, so it needs a control: plant a bump in the
same operator and the same filter finds three extra eigenvalues, one of them at `+1.58`,
firmly in the right half plane. The filter can see. It's just that there's nothing there.

## What this is and isn't

It moves nothing toward the Clay problem, and I want to be exact about the gap. This is a
one-dimensional toy. The exponent used at the second point is *hyper*viscosity, chosen
because it's where the critical problem can be posed exactly, not because it resembles
anything physical. The closed-form solution decays like `1/x`, so it has infinite energy —
which is the honest analogy to the classical theorem ruling out exactly self-similar
Navier–Stokes blow-up in the finite-energy class. The escape route from that theorem is
precisely the slowly-decaying profiles, and they were constructed decades ago. This is a
toy version of the thing that escapes, not a counterexample to anything.

What it does do is convert "the argument returns no information" into a question with an
answer, in a setting where the answer is checkable against a closed form. And it leaves
the project in a slightly better epistemic position on one lane: the negative result now
rests on a measurement with a working control, rather than on there being nothing to
measure.

The novelty is unchecked, and probably thin. Explicit viscous solutions of this equation
by complexification date to 1986. The threshold formula is likely in a 2022 paper I still
cannot download. If anything here is new it's methodological — treating the viscosity
coefficient as a dynamical coordinate so that the marginal case becomes a normal form with
one coefficient — and that's exactly the sort of thing that turns out to be standard the
moment you ask someone in the field.
