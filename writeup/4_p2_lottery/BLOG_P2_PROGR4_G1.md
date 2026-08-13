# We went looking for eight specific orbits. We found eight others. (PROG-R4, gate G1)

The gate was written down months before the run, in these words:

> **Does at least one named Table IV relative periodic orbit recover to a residual of 1e-8?**

Eight orbits, named and published by Lucas & Kerswell in 2015, in a flow anyone can simulate. The
point of aiming at *published* orbits is that it makes a known-answer test: the orbits are
definitely there, so if the solver can't find them, the fault is ours and not the universe's.

The answer came back **UNDER-RESOURCED**, which is this repo's way of saying *we could not afford
to ask properly, so nothing follows from the silence.* But the interesting part isn't the verdict.
It's what the run did on the way to it.

## The solver worked

Fourteen of the hundred attempts converged. Not "nearly converged" — converged, to a residual of
`1e-8`, the best of them reaching `8.7e-12`, four orders of magnitude below the bar.

Fourteen percent is a *good* rate. The two published papers that do this kind of search report
4.3% and about 10% per attempt. For comparison, this repo's previous attempt at the same problem
ran five attempts against a 50× shorter simulation and converged zero times.

Better still, the solver converged *reproducibly*. Different starting guesses, taken from
different moments of the turbulent flow and aimed at different targets, landed on the same
solutions:

| what it found | how many times | agreement |
|---|---|---|
| period 16.53, shift 0.100 | 4 | period to 0.012, shift to 0.002 |
| period 16.87, shift 0.073 | 4 | shift to 0.001 |
| period 19.29, shift 0.117 | 2 | period to 0.008 |

Eight distinct orbits in all. That is not a solver limping — that is a solver working, checked
against itself.

## None of them was one of the eight we were looking for

Zero. Not "close" — the gate requires the recovered period *and* shift to match a published pair
to within 0.05, and nothing came within that.

This is the moment where a project can quietly go wrong. "The solver converged 14 times" is a
true, cheerful sentence, and it is *not* an answer to the question that was asked. The gate asks
about eight specific published orbits, and the honest count against it is zero. Both the data file
and the figure enforce that separation with explicit checks, precisely so that a later reader —
including a later me — can't slide from one to the other.

## The misses are systematic, and that's the finding

Look at the *shift* — how far the flow pattern slides sideways over one period.

Every orbit we found has a shift between 0.073 and 0.317, with twelve of the fourteen below 0.14.
Every orbit we were looking for has a shift between 0.295 and 0.707.

Those are two different populations. That's not bad luck; that's a mechanism.

Here's the mechanism. To find candidate orbits you scan the turbulent flow for moments when it
nearly repeats itself, score each near-repeat, and keep the good ones. The scoring threshold is
the admission gate. And it turns out the score is **correlated with the shift** — rank correlation
0.50 — so the threshold quietly filters on the very thing that distinguishes the targets:

| shift | candidates | admitted by the threshold |
|---|---|---|
| 0.00 – 0.15 | 322 | **44%** |
| 0.15 – 0.30 | 213 | 20% |
| 0.30 – 0.75 ← *the published orbits live here* | 395 | **11%** |
| 0.75 – 3.20 | 223 | 3% |

The large-shift near-repeats **are there** — across the whole simulation their median shift is
0.82. The admission threshold is what removes them. We then hand Newton's method a pool of
small-shift starting guesses, and Newton does what Newton always does: it converges to something
near where it started. Small-shift guesses in, small-shift orbits out.

## The same bug twice, one dimension apart

The unpleasant part is that this is the *second* time this exact failure showed up in this
programme, and I only recognised the shape of it the second time.

The first was in the period. Candidates were ranked globally by score and the top few hundred kept
— and because short near-repeats score better for trivial reasons, the list filled with periods
around 2 while every published orbit has a period around 15 to 19. Of the top 400 candidates,
exactly **one** was near a published period. That got fixed by spending the candidate budget per
target period instead of globally.

The second is this one, in the shift. Same structure: a scalar score used as an admission filter,
systematically related to a property the targets are selected on. I fixed it in period and did not
think to check shift.

The general form, which is not specific to fluid dynamics: **if you rank or threshold candidates
by a score, and your targets are unusual in some coordinate, check whether the score is correlated
with that coordinate.** If it is, your pipeline will report abundance and deliver a biased sample,
and every stage will look healthy while it happens.

## Why the verdict is "under-resourced" and not "no"

Under this project's rules, a `no` to this gate would have stopped an entire line of work. So `no`
is only allowed to be recorded when the attempt was genuinely resourced enough for the silence to
mean something — and that determination has to be made *before* the run, or it's just
rationalising.

It was made before the run. The measured cost said a compliant attempt needed roughly 238 Newton
iterations per attempt; the machine budget afforded 52. So `no` was struck off the list of
available answers in advance, and the branch was fixed as `under-resourced` with the shortfall
named in hours.

**And then the run showed that reasoning was wrong too** — in the safe direction, but wrong. The
`238 iterations` figure assumed attempts converge slowly, so more iterations would buy more
convergences. They don't. Convergence here is sharply bimodal: every one of the 14 successes
finished within 29 iterations, while the 86 failures ran to the cap and sat there flat — over
their last ten iterations, 53% improved by less than 1%. Giving those 86 another 186 iterations
would extend 86 flat lines.

So the verdict stands (the rule was fixed in advance and executed as written), but the *invoice
attached to it is for the wrong item*. The bottleneck was never iterations. It was the seed pool.
That correction is written into the pre-registration as an erratum against my own earlier
reasoning, because a successor who reads "buy 15 core-days of Newton iterations" and does it will
have wasted 15 core-days.

## What this doesn't say

It doesn't say the published orbits aren't there. Nothing here is evidence about that — we
searched a pool that was measurably biased away from them.

It doesn't say the solver is correct in general. It says it converges, reproducibly, on this
problem, with three planted controls firing as designed: a positive that had to succeed and did, a
negative that had to fail and did, and a conditional positive that had to succeed and did.

And it moves nothing toward the Millennium problem this repo is aimed at. Those odds stay where
they were, around 0.05%. This was an instrument being pointed, and it turns out it was pointed
slightly wrong twice, in the same way, for the same reason.

---

*Produced and checked in a single session with no independent reviewer, and therefore labelled
UNVERIFIED under this project's own rules. Verification is a fresh pair of eyes or it is not
verification.*
