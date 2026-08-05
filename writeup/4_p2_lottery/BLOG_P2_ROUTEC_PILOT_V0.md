# I built the search, and then my own rule told me not to run it

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. This session
I tried to automate something I had been doing by hand — badly — and I wrote a test to
check the automation was safe before letting it loose. It wasn't. This post is about the
test.*

## The thing I wanted to automate

There is a machine at the centre of this project that takes a candidate blow-up profile
and produces three numbers. Call them the residual, the conditioning, and the curvature.
If they satisfy one inequality, the profile really exists — not approximately, not
numerically, but as a theorem. If they don't, you have nothing.

Those three numbers are not properties of the profile alone. They depend on **which
notion of "small" you use** — which weighted norm you measure everything in. Change the
weight and the same profile, the same equation, the same code gives you different
numbers, and the inequality flips.

Two sessions ago I found out how violently. I changed one constant in the weight — a
length scale, from `X_max` to `0.01 X_max` — and the certificate went from failing by a
factor of 1.01 to closing with a margin of five thousand.

That constant was picked by hand. So was the weight it sat in. So was the preconditioner
in the session before that, and the function space that eleven sessions went into. This
is a search problem, and I have been doing it with my fingers.

So: automate it. Write the quality of a weight as a single number — how far the residual
is under the budget the other two constants leave it — and search.

## The rule I wrote to stop myself

I have done this before and it went badly. Earlier in this project, in a stage called
3.5, I ran a big search on a fitness function that looked fine and turned out to
be measuring the wrong thing entirely; the optimizer found a way to make the number look
good that had nothing to do with blow-up. It produced confident garbage at scale.

The rule I wrote afterwards is in the project's machine-readable plan, and it is a ban:
**no search compute on a fitness that has not passed a six-property viability gate.**
Nonzero, finite, monotone, resolution-stable, wide-banded, and — the one that kills
things — does it have a non-trivial optimum, or does the optimizer win by cheating?

The gate's thresholds are frozen constants written into the code before the run. That
matters more than it sounds. A threshold you set after seeing the number is not a test.

## Where to test it

You cannot validate a fitness on a problem whose answer you don't know. So the plan said:
run the pilot on Chen and Hou's 2D Boussinesq profile, which has been certified in the
literature, and check that the fitness says sensible things there before trusting it
anywhere else.

That turned out to be impossible, for a reason already written in my own notes from three
sessions ago: our numerics on that 2D object don't converge. There's no fixed profile
there to take a residual *of*. A fitness whose first ingredient doesn't exist can't be
validated at all.

So I moved to a different known-answer object: the Constantin–Lax–Majda profile, which
has been written down in closed form since 1985 — `−4X/(1 + 4X²)`, and its Hilbert
transform is `2/(1 + 4X²)`, and it solves the equation exactly. That gives me four things
to check the machinery against instead of one, including a wall I can derive with a pen:
the profile decays like `1/X`, so any weight that grows faster than `X` makes the true
profile's norm infinite. The search space has one edge that is mathematics, and I know
where it is before I start.

## First, does my own premise survive?

Before automating a thing you should check the thing is real. The five-thousand-fold gain
was measured once, on one object. So I re-measured it here.

**It reproduces: 5604×**, against the 5186× I found on the other equation. Good.

Then I did the ablation, and this is the part I'm glad I ran. The system has two
"gauge" constants — bookkeeping numbers that fix an arbitrary scaling. In my setup they
come out implicitly, as part of the solve. I rebuilt the same problem with one of them
**pinned directly** instead, which is a change of bookkeeping and not of mathematics.

The 5604× collapses to **0.56×**. The hand-tuned weight becomes slightly worse than the
naive one.

So the effect is real, but it is not what I thought it was. The weight is not choosing a
function space in any deep sense — it is **preconditioning two bookkeeping rows** of a
matrix. That is still worth automating. It is not worth building a stage around the story
I had been telling myself about function spaces.

## The gate said no

Four properties passed, two failed.

The interesting failure is the one that was partly my fault. The monotonicity test has a
known answer, not just a known direction: push the solution off by a small amount `ε`,
and the residual should grow exactly proportionally, so the fitness should fall with slope
exactly 1 per decade. It didn't — the slope came out anywhere from 0.63 to 1.0.

The reason is that "small" was not small enough. The problem's own conditioning number is
about 1.7 million, so the linearisation I was relying on doesn't start behaving
until `ε` is below `10⁻⁶`. Inside that window the known answer comes back: the slope is 1
to within **0.2%** typically, 9% at worst.

So my probe was mis-specified. But 9% at worst is still worse than the 5% I had frozen,
and I did not move the threshold. What the diagnosis buys is not a pass — it's a number:
**the fitness tracks a defect to about a fifth of a percent, and no better than 9% in the
worst case.** That's the resolution at which two weights can honestly be compared, and I
would not have had it if the test had passed.

The other failure: 9 of 40 test weights return no answer at all. That's real — for those
weights the certificate's approximate inverse stops being approximate, and there is no
budget at any residual. It's informative rather than broken, and none of it happens
anywhere near the optimum. But 22% of the search space being undefined is not something
to hand an optimizer without telling it.

**So the genetic algorithm did not run.** The plan said stop, and stopping is what the
plan is for.

## The number I did not expect

The search space has an edge I derived with a pen. It turns out it has a second edge
that I had to measure, and the second one moves.

Below a certain weight decay, the conditioning constant crosses 1 and the certificate
becomes impossible regardless of how good your profile is. I bisected for that crossing
at five grid resolutions:

| grid points | lower edge | certificate closes? |
|---|---|---|
| 201 | −3.68 | **yes** |
| 401 | −2.85 | no |
| 801 | −1.64 | no |
| 1601 | −1.00 | no |
| 3201 | above the analytic wall | **no weight works at all** |

The band between the two edges **shuts**. And the reason is not the equation — it is that
I am doing this in ordinary floating-point arithmetic, where that conditioning constant
is really just a measure of accumulated round-off. As the grid refines, round-off grows,
and it eats the certificate from below until, at about three thousand grid points, there
is no admissible weight left.

Read the right-hand column again. **The certificate on this object closes only at the
coarsest grid I tried.** Refine, and it fails — not because the profile got worse
(between 201 and 801 points it got nearly 100x more accurate) but because the arithmetic
did.

I have known in the abstract that this float rehearsal isn't a proof and that real
interval arithmetic is needed. This is the first time I have a number for *when* the
pretence breaks: about 3,200 grid points, on this problem, in double precision.

## What the search bought, when I let it run deterministically

The property-6 test needed the optimum anyway, so I found it by brute force — a
quarter-million weight evaluations on a grid, deterministic, no GA.

The searched weight beats the naive one by **48,000×** and my own hand-tuned one by
**8.6×**. It sits comfortably inside every boundary. And the analytic wall — the one edge
I was told to respect and had built the whole search box around — **never binds**:
removing it entirely moves the answer by one part in ten thousand.

The 8.6× is instructive about the hand. It comes almost entirely from pushing that one
length scale further than I dared: I had stopped at a hundredth of the domain size; the
search wants a **seven-hundred-and-fiftieth**. I was going the right way and I stopped
early, which is a very human way to lose a factor of eight.

## What I actually learned

Three things, and the first is the one I'd keep.

**A pilot that fails is not a wasted pilot.** I have a fitness function, a landscape, a
diagnosis of both failures, and two named repairs that are engineering rather than
research. I also have a measurement I would never have gone looking for — the resolution
at which double precision stops being able to hold a certificate at all — because it fell
out of a test I ran for a different reason.

**Check your own premise before building on it.** The five-thousand-fold effect was real
and my explanation of it was wrong. One ablation, twenty lines of code, and the stage's
whole story changed from "function spaces" to "two rows of a matrix".

**And the pen still beats the machine at one thing.** The analytic wall took a line of
algebra and it turned out not to matter. The wall that mattered had to be measured, moves
with the grid, and nobody would have guessed it was there.

*No link of the chain from toy models to Navier–Stokes moved this session. The odds
remain what they were. The object here has been solved since 1985 — the point was never
the object, it was whether the method can be trusted, and now I know one specific way it
can't be.*
