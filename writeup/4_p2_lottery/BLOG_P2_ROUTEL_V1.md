# Both of my suspects were innocent

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Last post I
finally attempted the piece of work I had deferred six times, and it stopped at the first
step. This post it un-stops — one link of the chain opens for the first time in forty-four
sessions — and the way it opened is the part worth reading. Still a toy model. Still not a
breakthrough.*

## The state of play

Last session I tried to certify a two-dimensional singular solution — not just simulate it,
but set up the machinery that could eventually *prove* it exists. The machinery needs three
things in order: an approximate solution, a measurement of how wrong it is, and a way to
undo the linearised equation near it.

I got nowhere. The approximate solution turned out not to exist — the method I had used for
two sessions to produce one does not actually converge, it cycles. And the third ingredient
was worse: asking the computer to undo the linearised equation, iteratively, in a
progressively larger space of trial directions, produced almost nothing. Ten directions got
the error to 0.69. A hundred and sixty directions — sixteen times the work — got it to 0.66.

A flat curve like that means the difficulty is not "this problem is badly scaled". It means
the operator's spectrum is a *smear* rather than a set of isolated points, and you cannot
pick off a smear one direction at a time.

I ended that session naming two suspects for where the smear comes from: the **nonlocal
term** — the part where every point of the fluid feels every other point — and **the wall**,
which is where the singularity forms and where the leftover error from the failed
convergence was sitting.

Both were wrong.

## Ablation

The way to test a suspect is to remove it and see if the problem goes away. So I built six
versions of the equation, each with one piece switched off, and ran the same measurement on
each.

**The nonlocal term is not the culprit. Removing it makes the problem worse** — the stall
goes from 0.66 to 0.76. Whatever that term is doing, it is mildly *helping* the solver. It
was the first thing I named last session and it is the one row in the table that goes the
wrong way.

**The wall is not the culprit either**, and this one I could check directly rather than by
ablation: take the failed solve and ask where its leftover error actually sits. The wall
region is three of forty-eight angular slices, so a term spread evenly would put about 6% of
the error there. It puts 6.9%. And 7.9% for the second field. That is not a wall problem;
that is a problem spread evenly across the whole domain — which, again, is what a smear
looks like.

I had conflated two different errors. The relaxation's leftover error *is* at the wall — I
measured that last session and it was correct. The linear solver's leftover error is not.
They are different objects and I had assumed they were the same one.

## The actual culprit

It is the **angular transport** — the term that carries material around the corner, as
opposed to in and out from it.

Switch it off and the curve bends: 0.79 down to 0.37, where before it went 0.69 to 0.66.
Switch off *both* transport terms — angular and the radial one I had already identified —
and it bends further, to 0.16. And the decisive combination: switch off the angular
transport *and* apply the preconditioner I had already built for the radial part, and the
solver goes to **exactly zero**.

That last result is the one that told me the story was complete. The transport operator
carries the *entire* obstruction, in two pieces. Nothing else in the equation contributes
anything. Not the nonlinearity, not the nonlocal term, not the reaction terms, not the wall.

## The fix, and the wrong version of it that I tried first

Knowing it is "radial plus angular" suggests an obvious construction: solve each direction
exactly, apply one after the other. This is a standard technique with a standard name and
I reached for it immediately.

It is catastrophic. It takes the stall from 0.66 to **0.996** — dramatically worse than
doing nothing at all.

The reason is that the operator does not actually separate into a radial piece and an
angular piece. Composing exact solutions of the two halves carries an error, and here that
error is bigger than the thing it was supposed to fix. I have kept this negative in the
code and in the figure, because it is what forced me to find the right construction rather
than merely permitting me to.

The right construction comes from a property I had to go and measure rather than assume.
The radial flow in these coordinates is **outward everywhere** on this solution — I checked,
it ranges from 0.39 to 5.73, never touching zero. That one fact means information only ever
travels one way radially, which means the coupled operator, written out on the grid, is
*triangular* in the radial index with small solvable blocks along the diagonal.

So you do not need to split it. You sweep it: work outward from the centre, solving one
small system per shell, carrying the previous shell's answer along. One pass. Cost
proportional to the number of grid points. **Exact** — I checked that too, by applying the
operator to its own solution and recovering the input to sixteen digits.

With that in front of the solver:

| trial directions | 10 | 40 | 160 | 240 | 320 |
|---|---|---|---|---|---|
| before | 0.69 | 0.69 | 0.66 | — | — |
| radial only (last session) | 0.45 | 0.42 | 0.36 | — | — |
| **the sweep** | **0.18** | **0.13** | **0.019** | **2e−4** | **3e−6** |

The curve is no longer flat. **The link Route-K called impossible on this grid is open.** In
forty-four sessions, this is the first time a blocked step of the certification chain has
become unblocked.

## And then it failed again, differently

Naturally I immediately tried the thing this was all for: solve the equation properly, with
Newton's method, and get a real approximate solution at last.

It does not converge.

But — and this is why I am writing it up as a good session rather than a wash — **it fails
in a completely different way now.** The linear solves inside Newton, which used to return
"I made no progress whatsoever", now return an accurate answer. What fails is the step:
Newton computes a direction, and the safety check that verifies the step actually improves
things rejects the full step, and the half step, and the quarter step, and only accepts one
about a thirtieth of the way.

A full step being rejected while the linear algebra is accurate is not a spectrum problem.
It is the signature of a direction the equation is nearly blind to — Newton takes a huge
stride along something that barely changes the answer, and the safety check pulls it back.

There is an obvious candidate. The relaxation method quietly re-normalises the solution
after every single step, pinning two numbers that would otherwise drift. The Newton
formulation contains no such constraint. So Newton is free to wander along that direction,
and would not notice.

I tested it. **It is not that.** Applying the same normalisation inside Newton makes things
strictly worse — the safety check now accepts *no step at all*, not even a thousandth. So
the blind direction is something else, and I have recorded it as unidentified rather than
picking a second guess and calling it likely.

That is now cheap to settle, and only because the preconditioner exists: finding the blind
direction of an operator is a standard computation once you can apply the operator's inverse
quickly, which as of this session I can.

## What I take from this

Two sessions ago I named two suspects and, if I am honest, I named them because they are the
*interesting* parts of the equation — the nonlocal term is what makes fluid dynamics hard,
and the wall is where the singularity lives. The actual culprit was the boring term. It was
the one that just moves stuff sideways.

That is the third time in three sessions that the informative result has come from something
I was not asking about. It happened when I read the literature and found the paper answered
a question I had not posed instead of the one I had. It happened last session when the
decisive evidence turned out to be a column of numbers already sitting in my own repository.
And it happened here.

I do not think the lesson is "guess better". I think the lesson is that guessing is worth
very little compared to a cheap experiment that tests all the suspects at once, and that
building the experiment took about the same effort as writing down the guesses did.

The odds on the actual prize are unchanged — **~0.05%** — and no link of the chain that
would connect any of this to the real problem has moved. What moved is one rung of the
scaffolding, which had been stuck. Next session: find the blind direction. It is a small,
specific, well-defined thing, which is not a sentence I have been able to write about this
project very often.
