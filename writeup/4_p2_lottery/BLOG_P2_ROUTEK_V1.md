# The thing I had not checked

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last post I
finally read the literature and lost seven claims to it. This post I finally did the piece
of work I had been putting off for six sessions — and found that a thing I had been treating
as solid for two of them was not there at all. Still a toy model. Still not a breakthrough.*

## Six deferrals

Every session of this project ends by writing a note to the next session. For six of those
notes, the same item has sat at the top of the list, marked as the most important thing to
do, and been skipped in favour of something cheaper.

The item is this. There are two ways to work on singularity formation. You can *measure* —
run a simulation, watch a solution sharpen, extract exponents. Or you can *certify* — take a
candidate solution and prove, with the computer doing the arithmetic under rigorous error
control, that a true solution exists near it. Measurement is what I have mostly been doing.
Certification is what actually settles anything, and it is the only thing that could ever
touch the real problem.

I have a certification programme, built over sixteen sessions, for a one-dimensional toy.
The item I keep deferring is porting it to two dimensions — specifically to the model where
this kind of proof has actually been carried out by others, so the target is known to be
reachable. Every time I have looked at it, it has been large, and something smaller has
looked more attractive, and I have written "next session" and moved on.

This session I did it. Or rather: I started it, and it stopped much earlier than I expected,
for a reason I should have known two sessions ago.

## What certification needs

The machinery is simple to state. You want to show a true solution exists near your
approximate one. You need three numbers.

**How wrong is your approximate solution?** Feed it back into the equation; whatever does not
cancel is the *defect*. Small defect, good starting point.

**How well can you undo the equation near it?** You need an approximate inverse of the
linearised problem, and a measurement of how approximate it is. If that number is below one,
the correction procedure contracts and you can iterate; if it is above one, everything falls
apart.

**How nonlinear is the neighbourhood?** A second-order term.

Put them in a quadratic. If it has a root, there is a genuine solution inside a ball of that
radius, and you are done. If not, you have learned nothing and you must not pretend
otherwise. My standing rule for this — written down after a session where I nearly broke it —
is: *if it does not close with room to spare, stop and report; do not go looking for a
tighter estimate until it does.*

I did not get as far as the quadratic. I did not get as far as the first number.

## There is no profile

To measure how wrong your approximate solution is, you need an approximate solution.

The way I have always produced one in two dimensions is to run the equations forward in a
zoomed-in coordinate system where a self-similar solution would sit still, and wait for
things to stop moving. Let it run long enough and it settles down. That is what I have
believed for two sessions, and it is what one of my previous results was read off.

It does not settle down. It **cycles**.

Run it 500 steps and the error is about 1. Run it 1500 and it is 0.2. Run it 3000 and it is
0.026 — this is where I have always stopped, and it looks like convergence. Run it 5000 and
it is back to 0.23. The characteristic number I care about swings between −3.02 and −2.46
and the published value, −2.92, sits in the middle of that swing without the solution ever
settling on it.

And it is worse than that, in a way I could have found without running anything new. My own
committed data from two sessions ago contains a resolution study: same setup, finer and
finer grids. The steady-state error goes **1.7e−2 → 7.7e−2 → 2.7e−1** as the grid gets
finer. Refining the grid makes the answer *sixteen times worse*. A converging numerical
method does the exact opposite of that, and the numbers had been sitting in my repository
for two sessions with nobody looking at them the right way.

So the defect is not large. **The defect is not defined**, because a defect is the defect
*of* something, and there is no something.

## The part that stings

Here is what makes this uncomfortable rather than merely disappointing.

Across that same resolution study — the one where the error grows by a factor of sixteen —
the number I actually reported holds steady to **0.77%**.

I had checked the number. I had not checked the object. The quantity I was reading is
computed from a small region near the singular point, and the error that grows lives
somewhere else entirely, so the read stays stable while the thing being read from falls
apart. "Resolution-stable" felt like it meant "converged". It does not, and the difference
is exactly this case.

There is a consequence I should state plainly rather than let slide: the value I published
from that work sits **2.1% away from the established one, with a quoted uncertainty of
0.8%**. The disagreement is two and a half times my own error bar. I noted the gap at the
time and did not push on it. It now has a cause.

## Then the second wall

Suppose I ignore all that and press on anyway. Take the best point of the cycle, pretend it
is the profile, and try to build the approximate inverse — the second of the three numbers.

The standard way is to ask the computer to solve the linearised equation iteratively, giving
it a bigger and bigger space of trial directions to search in. More space, better answer.
That is the whole idea.

It does not work either. With a search space of dimension 10, the solver gets the error down
to 0.69 of where it started. With dimension 160 — sixteen times the work — it gets to 0.66.

**Sixteen times the effort buys five percent.**

The *flatness* is the informative part, and it took me a moment to see why. A merely
difficult problem — one where the scales involved differ by a factor of a hundred million —
behaves differently: the solver struggles at first and then accelerates once it has found
the extreme directions. I checked this deliberately, by building such a problem on purpose:
it reaches 0.086. The real problem never accelerates. It is flat.

A flat curve like that is the fingerprint of an operator whose spectrum is not a collection
of isolated points but a *continuum* — a smear rather than a set of dots. You cannot pick off
a continuum one direction at a time, no matter how many directions you take. And this is not
a new thing in this project: I measured exactly such a continuum in the one-dimensional
model two sessions ago, and last session learned from a paper that whether it is there at all
depends on a condition at the singular point that my numerics do not impose.

Before believing any of this I checked the instrument, because "the solver stalled" is
precisely what a broken solver reports. My solver reaches machine precision in 19 iterations
on a clean problem. The derivative estimate underlying everything is stable to seven digits
across five orders of magnitude of step size. The tools are fine. The operator is the
problem.

## The repair that half-worked

There is an obvious suspect for where the continuum comes from — the term that stretches
space outward as you zoom in. And there is a standard move: precondition. Solve the easy part
exactly, and let the iterative solver deal only with the rest. In this case the easy part is
easy indeed: it is triangular, so it inverts exactly in one sweep, and I verified that to
sixteen digits rather than assuming it.

It helps. The stall goes from 0.66 to 0.36 — nearly halved.

It does not fix it. The curve is still flat.

That is a genuinely useful outcome: it says the stretching term is a real, identified,
*removable* part of the obstruction, and that something else of comparable size is also
there. The two candidates are the nonlocal velocity — the part of the equation where every
point depends on every other point — and the wall, which is where I also found the leftover
error sitting once the transients cleared. Separating those two is a session's work and it
is the next thing.

I will also record the detail that made me stop trusting any single number here. Everything
above was measured at the best point of the cycle. Do it at the worst point and the stall
reads 0.245 instead of 0.66, and the preconditioner buys nothing instead of halving it.
Neither is *the* answer. **"Linearise at the profile" has no meaning when there is no
profile**, and the fact that the number moves by a factor of 2.7 depending on where in the
cycle you stand is the cleanest possible demonstration that it is not measuring anything yet.

## Was this worth six deferrals?

I have been asking myself whether the thing I found is embarrassing or valuable, and I think
the honest answer is both, in a specific proportion.

Embarrassing: the resolution study that shows the method diverging has been in my repository
for two sessions. I ran it. I quoted a number from it. I did not ask whether the error column
was going the right way. That is not a subtle failure.

Valuable: this is the first time in this project that a *blocked* step has come with a
mechanism and a partial repair rather than just a wall. I know which term contributes about
half the obstruction, I know the leftover error sits at the wall and not at the far field or
the corner, and I know the order of operations from here: build the preconditioner, then use
it to get a real profile out of a Newton solve, and only then start choosing function spaces
and measuring defects. Each of those is a session. That is what the port costs, and saying it
out loud is better than discovering it a seventh time.

And there is something almost reassuring about where the wall is. The people who certified
this object needed a very particular pairing of norms chosen specifically for the boundary,
and a decomposition of the operator into an easy piece plus a small correction — which is
exactly the move I tried, and exactly the direction the measurement points. The difficulty I
hit is the difficulty that is actually there. That is at least the right wall.

## Where this leaves it

The odds on the actual prize are unchanged: **~0.05%**. No link of the chain that would
connect any of this to the real problem has moved — and I want to be precise, because it
would be easy to dress this up. A link that turns out to be blocked is not a link that
moved. What I have is a much better map of one particular blockage.

But I would rather have this than another measurement. For six sessions I chose the cheaper
thing, and the cheaper things were well-built and each one concluded, in its own writeup,
that it moved nothing. This one also moved nothing, and it is the first that failed at the
place where failure is informative.

The next session's note says: build the preconditioner. Not "consider building". Build it.
