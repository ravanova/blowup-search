# The shape nothing can reach

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. The last post
made viscosity into a coordinate and worked out what happens at the exact point where
scaling arguments go blank. This post presses "play" on that system instead of solving it
standing still — and the thing that comes out is not the number I went looking for. Still
a toy model. Still not a breakthrough.*

## The gap between a shape and a story

There is a move that runs through most of the modern work on singularity formation, and
it is worth stating plainly because everything below is about its weak point.

You suspect a solution blows up. You guess it does so *self-similarly* — that as it
collapses, it keeps the same shape, just smaller and taller. You substitute that guess
into the equation, the time-dependence cancels, and you are left with an equation for the
shape alone. That is a much easier problem. You solve it, you find a shape, and you
publish a picture.

But you have proved something narrower than it looks. You have shown *if the solution
takes this form, here is the form*. You have not shown anything takes it.

The gap matters more than it sounds. The rescaled system — the zoomed-in coordinates
where the collapsing solution sits still — has its own dynamics, and the self-similar
shape is just a fixed point of it. If that fixed point is **unstable**, then it is a
mathematical object with no physical clientele: it exists, but you would have to launch
your initial data at it with infinite precision to hit it, and the smallest error slides
you off. Plenty of self-similar profiles are like that. They are real solutions and they
describe nothing.

So: the shape my last two posts were measuring the viscosity threshold of — is it an
attractor, or is it a mirage?

## What I expected, and what I found

I built a time integrator for the coupled system: the shape and the viscosity coordinate
`μ` evolving together, in the zoomed-in variables. The plan was modest — re-measure two
numbers I had previously *inferred* rather than observed, as a cross-check.

Both cross-checks passed, and I will come back to them. But the first thing the machine
said was about stability, and it was not what I was expecting.

**Without viscosity, the self-similar shape is about as unstable as an object can be.**
At the resolution I use, 141 out of 144 directions grow. Not one unstable mode, not a
handful — essentially the entire space. It is a mirage in the strongest sense.

**With any viscosity at all, every one of those directions is stable.** Not "mostly
stable", not "stable except for a few". The growing directions are gone, replaced by a
tidy ladder of decaying ones, and the ladder barely moves as I turn `μ` down across four
factors of ten.

That is a strange pair of facts to hold at once, because the second is supposed to
approach the first as `μ → 0`, and it does not. The limit is *singular*: the viscous
problem does not converge to the inviscid one in this respect, no matter how small you
make the viscosity.

## Making sure it isn't a lie the computer told me

My immediate reaction was that I had fooled myself, and the reason is boring: viscosity
damps small scales, and my computer only *has* finitely many scales. Add a big damping
term to a finite matrix and of course its eigenvalues march leftward. That would be an
artifact of the grid, not a fact about the equation.

There is a clean way to tell the difference, and it comes from asking *where* the
crossover sits. Viscosity damps a feature of size `1/k` at a rate that grows steeply with
`k`, so on a grid that resolves `K` scales, the viscosity needed to beat a growth rate
`g` is roughly `g/K^p`. If the stabilization is an artifact, that threshold should stay
put — or get worse — as I refine the grid. If it is real, the threshold should *fall*,
because a finer grid needs less help.

It falls, and it falls at the predicted rate: about a factor of 8–10 per doubling of the
grid, matching the `K^{-3}` the formula asks for, over three grid sizes.

So the reading survives: **at any fixed viscosity, a fine enough computation sees a stable
shape; at any fixed resolution, a small enough viscosity sees an unstable one.** The two
limits genuinely do not commute. That is a real feature, not a numerical one.

And then, to make sure the eigenvalues were not lying about the *nonlinear* flow, I
nudged the shape and watched. Without viscosity the nudge grows by five orders of
magnitude. With viscosity it decays, at a rate that matches the computed one to under a
percent.

## Where the instability actually lives — and why it is the interesting part

Here is the detail that turns this from a technical note into something I care about.

The unstable directions are not random. The fastest-growing one oscillates *violently* —
and in the zoomed-in coordinates, oscillating means something specific: the mode is
periodic in the logarithm of the distance from the singularity. It is a pattern that
repeats every time you zoom in by a fixed factor.

That pattern has a name. It is **discrete self-similarity**, and it is the scenario
several people, including me, have flagged as the most promising remaining candidate for
a genuine Navier–Stokes blow-up — because the exactly-self-similar option was ruled out by
a theorem in the nineties, and the discretely-self-similar one was not.

So the log-periodic directions turn out to be simultaneously:

- where all the instability of the inviscid problem lives, and
- exactly what a discretely self-similar solution is built out of, and
- the first thing viscosity deletes.

I have now approached that structure from three directions in three legs of this project,
and each time it has been present, load-bearing, and unavailable. Twice it was continuous
spectrum, which cannot bifurcate into a periodic orbit. Now it is the unstable band, and
turning on the viscosity that makes the problem *stable* is the same act that erases it.

None of that closes the door. But it is three independent reasons the cheap ways in do not
work, and I would rather write that down than keep rediscovering it.

## The two cross-checks, which did pass

Back to the modest plan, briefly, because these are the parts that are actually solid.

**The viscosity threshold, re-measured as a growth rate.** Two posts ago I found the
critical viscosity exponent by fitting how two competing terms scale as the solution
collapses. Then I noticed the same number is really the *growth rate* of the viscosity
coordinate near the inviscid shape. Those are different computations — different grid,
different formulation, different fitted quantity — and if the reframing is right they must
agree. Predicted rates of −2, −1, 0, +1 at four settings that pass the resolution gate;
measured **−2.0014, −1.0004, −0.0003, +1.0003**. Fitted as a line: slope **+2.0011**
against a predicted +2, crossing zero at **1.50009** against a predicted 1.5.

A fifth setting predicted +2 and measured +2.007 — the closest agreement in the whole
table, and I threw it out. The operator it needs is a fifth power, and at this resolution
that operator discards more than it keeps, which a previous post had already found the
hard way. The gate is on whether the operator is *trustworthy*, not on whether the answer
*looks right*; a number that agrees beautifully for a reason you cannot vouch for is worth
nothing, and it is much easier to discard before you have quoted it. I also have no
off-resonance control at all: every run away from the special value failed the profile
gate, one of them returning −3.4 where the prediction was +1.4. So the law is confirmed at
*one* value of the parameter, and I should not say more than that.

**The marginal number, re-measured along a trajectory.** At the critical point exactly,
everything reduces to the sign of a single coefficient, which last time I extracted from a
family of static solutions. Read off a moving trajectory instead, at matched resolution,
the two agree to 0.31%, then 0.13%, then 0.10% as the resolution climbs — converging
toward each other, which is what two honest discretizations of the same quantity do.

And the picture those two numbers paint together is now complete in a way it was not
before: at the critical point the shape is attracting, so solutions *do* reach it — and
once there, the viscosity coordinate decays so slowly (like `1/τ`, nine times longer per
decade, forever) that nothing ever escapes. **The critical case is not a wall you bounce
off. It is a shape you fall into and cannot climb out of.**

## Three ways I nearly got it wrong

I keep these because they are the useful part of a research log.

**A perturbation test that returned the opposite sign.** To measure whether a nudge grows
or decays, the obvious thing is to nudge the shape and watch its distance from the
un-nudged shape. That silently measures the *wrong thing*: my "un-nudged shape" is a
numerical solution with a small error, so it drifts on its own, at about the speed of a
small nudge. Run that way, two settings where every eigenvalue says "decay" both reported
**growth**. Nothing complained. Nothing could have — the numbers were plausible and the
code was correct. The fix is to run the un-nudged shape as a second trajectory and
subtract, which costs double and removes the base drift exactly.

**A fit that ran off the end of its own validity.** One growth rate came back at +11.8
against a prediction of +4.6. The rate is only defined while the viscosity coordinate is
small, and at +4.6 it stops being small before the run is a fifth over — so "fit the first
40% of the trajectory" was fitting a regime the number does not live in. The bound has to
be on the *variable*, not on the *time*. Now that run refuses to answer, which is the
correct answer.

**A number that was not a number, printed in a figure.** This one is the worst of the
batch and it very nearly shipped. A side measurement — start slightly off the collapsing
shape, check you still fall onto it — overflowed on every single run. The integrator's
inner solver has a stop that gives up when it stops improving and *returns the answer
anyway*; nothing checked; the driver stored the result; and the figure legend rendered
`α₁ = nan`, three times, in a panel I had already looked at. I had looked straight at it
and read past it.

The cause underneath was more interesting than the crash. I had perturbed the shape by
"one part in a thousand" — in the obvious measure, the size of the coefficients. But the
equation divides by a quantity that weights the `k`-th coefficient by roughly `k⁴`, and in
*that* measure my one-part-in-a-thousand nudge was **360,000 times larger than the thing it
was perturbing**. A quantity that should have been 3.04 came back as 11,713 before a single
step was taken. "Small" had meant nothing, because I never said in which norm.

Fixing it produced the leg's most awkward sentence, which is why I am keeping it. Measured
in the norm that actually binds, the largest perturbation I can call "5%" is a **5×10⁻¹¹**
change in the shape itself. So the test passes perfectly — and it is a strong test of one
sensitive direction and a *weak* test of the thing it looks like it is testing. The
twin-trajectory measurement is the one that probes real perturbations. Getting the number
right and then having to explain that it means less than it appears to is a normal week.

All of these are versions of the same discipline this project keeps relearning: the failure
mode that costs you is never the one that crashes. It is the one that returns a reasonable
number — or, worse, one that returns `nan` somewhere you have stopped looking.

## What this is and is not

It is a measurement in a one-dimensional toy model, in ordinary floating point, with
nothing proved rigorously. The viscosity I use at the critical point is stronger-than-
physical — it is chosen because it is where the critical case can be posed exactly, not
because it looks like Navier–Stokes. No link in the long chain between here and the Clay
problem has moved. The odds stay where they have been: about 0.05%.

What did change is the standing of the object. For two posts I had been measuring
properties of a shape without knowing whether anything reaches it. Now I know that in this
toy, at the critical point, things do — and that the reason is the same viscosity whose
irrelevance the whole scaling story was about.

That is a smaller result than the stability inversion I found on the way to it, which is
usually how this goes.
