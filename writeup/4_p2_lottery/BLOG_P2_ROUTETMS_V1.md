# The tool we never bought

*Leg 315, Route-TMS. Companion to `TECHNICAL_P2_ROUTETMS_V1.md`. Figure: `fig79`.*

There is a line in this project's `requirements.txt` that has been quietly steering the work
for a long time:

> `# scipy is intentionally NOT required (no adaptive ODE integrators are used).`

Read it again. It is not a discovery. Nobody measured anything and concluded that adaptive ODE
integrators are useless here. It is a **decision** — a sensible one, made early, that kept the
dependency list to two packages and the code auditable. But a decision that has never been
revisited starts to look like a fact, and the whole point of this leg was to ask whether that
particular decision has been costing us something.

The honest answer turned out to be: **yes, but not for the reason the question implied.**

## The tempting argument, and why it is wrong

The tempting argument goes: every certificate in this repository is a radii-polynomial or
Newton–Kantorovich argument. Those certify *things that sit still* — a profile, an equilibrium,
a zero of some operator. Anything that *moves in time* is out of reach, and Taylor-model
arithmetic — the standard enclosure toolkit of the validated-numerics world — is how you reach
moving things.

That argument is wrong, and finding out that it is wrong was the most useful hour of the leg.
The prior-art pass turned up **van den Berg, Breden and Sheombarsing, *Validated integration of
semilinear parabolic PDEs*** (`arXiv:2305.08221`, 2023), which does rigorous *time* integration
of PDEs using — of all things — a **Newton–Kantorovich** argument. Breden is one of the author
groups this project already keeps a file on. Newton–Kantorovich does time perfectly well.

So the leg could not stand on "NK cannot do time". It had to find something sharper. It did.

## The sharper thing: a sonic point

The target here is the compressible-fluid implosion of Buckmaster, Cao-Labora and
Gómez-Serrano at the adiabatic constant γ = 7/5 — the value for air. An earlier verifier on
this project established something important and slightly awkward: the gap in that programme is
**not a profile enclosure**. There is no viscous profile to enclose. The profile equation is the
*Euler* one; viscosity enters later, as a forcing term that decays exponentially in rescaled
time. The real gap is the **stability step** — the argument that the profile dominates that
forcing — and it only works on a narrow band of one parameter.

How narrow? The argument certifies a band of width `0.0243163` where the target makes
`0.1666667` available. That is a shortfall of `(7 + 3√5)/2 ≈ 6.854`. Panel A of `fig79` is just
that: a small blue rectangle inside a much larger grey one.

The thing you would want to do is push the certified band past its upper endpoint,
`r = 1.1909830`. And here is where the toolchain actually bites. The profile is governed by an
**ordinary differential equation** — a genuinely finite-dimensional, autonomous one — whose
trajectory has to pass through a **sonic point**, a place where the equation degenerates. A
Newton–Kantorovich certificate needs a fixed function space and an invertible linearisation in
that space, and a global basis handles a degeneracy like that badly. This project has already
measured its own version of that failure in three separate settings, and its own rules forbid
trying a fourth without a dedicated leg.

A Taylor-model integrator does not need a function space at all. It encloses the **flow** — it
steps along the trajectory carrying a polynomial plus a rigorously bounded remainder — and you
cross the degeneracy with a change of coordinates. That is the whole reach, and it is a
difference in *shape*: one apparatus certifies a zero, the other certifies a map.

## What it would cost, honestly

This is the part worth being careful about, because "cheap" and "expensive" are easy to say and
usually mean nothing.

There are three real cost classes. **A**: an existing library, with a licence and a version
number you can pin. **B**: a hand-roll — the kind of thing leg 256 was forced into when it had
to compute Gauss–Laguerre quadrature nodes by Sturm bisection because, with no scipy, there was
simply nothing to call. **C**: an actual research problem.

The arithmetic substrate is **class A**: `python-flint` 0.9.0, MIT-and-LGPL, released July 2026,
needs nothing but Python 3.10, and — pleasingly — is not scipy, so it does not even bump into
the policy line. That alone would close leg 256's recorded ceiling, where the journal says
plainly that it reproduced Breden–Chu's *constants* but not their *proof*.

The integrator is **class B**: there is no maintained Python Taylor-model ODE integrator to
install. The good ones are C++ (CAPD, Flow\*, VNODE-LP), restricted-licence (COSY Infinity), or
Julia. So it is a hand-roll, and a bigger one than leg 256's, because the hard part is the
"wrapping" control that stops the enclosure ballooning as you step.

And the destination is **class C**, a real research problem — which is the finding I would most
want carried forward. Enclosing the profile ODE is only the first rung. The obligation the
verifier actually wrote down is about the stability step over *infinite* rescaled time, with the
forcing retained. Getting from a validated ODE integrator to a validated PDE statement has a
standard bridge — Zgliczyński's self-consistent a-priori bounds, from 2000 — and that bridge
assumes the equation is **dissipative**. This one is **hyperbolic**. The bridge does not reach.

Naming that mismatch is, I think, the most valuable thing this leg produced. It is not a
tooling gap you can purchase your way out of.

## Two rows that come out the other way

One last note on method. A comparison table where every row favours the thing you set out to
advocate is not evidence, it is a mood. So the matrix in panel B of `fig79` carries two
deliberate controls: the project's own certificate machinery, which Taylor models cannot touch,
and that Breden time-integration result, which Newton–Kantorovich wins outright. The runner
*asserts* those rows in code and fails if they ever stop coming out that way. And one row —
the full infinite-time stability argument — is marked as reached by **neither**, because it is.

## The usual disclaimer, which is not a formality

Nothing was built here. Nothing was certified. Naming an object you could reach is not reaching
it, and no link of this project's chain to the Clay problem moved. The odds stay where they
have been all along: **about 0.05%**.

What changed is smaller and more honest: a policy line is now a policy line *with a measured
consequence attached*, and the thing that is actually blocking the compressible route turns out
to be a theorem nobody has proved, not a package nobody installed.
