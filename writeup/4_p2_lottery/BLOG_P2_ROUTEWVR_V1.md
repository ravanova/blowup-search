# The fitness was never the problem — and we found that out by changing it twice

*Route-WVR v1, leg 160. Technical companion: `TECHNICAL_P2_ROUTEWVR_V1.md`. Data:
`writeup/data/p2_route_wvr_v1_fitness.json`. Figure: `fig64`.*

## The setup

There is a genetic algorithm this project has been forbidden to run for about a hundred legs.

The reason is a good one. Before you let an optimizer loose on a score, you check that the score
is worth optimizing — otherwise it will find the score's bugs instead of your answer. This
repository has a frozen six-property battery for that, and the score in question — how good is
this weighted norm for closing a Newton–Kantorovich certificate? — has failed it three times.

The ban's own escape clause names exactly what would lift it: *a re-run of the six-property gate
that PASSES on a repaired fitness.* Never met. Leg 49 got 4/6. Leg 50 repaired the search box
and got 4/6. Leg 59 repaired the box better and got 5/6.

One property has failed every single time. Property 3: push the state off the known solution by
`ε` and the score has to fall with slope exactly 1 per decade, because the answer is known. It
must be within `0.05` of 1. It has been `0.37`, then `0.34`, then `0.34`.

That second `0.34` is the interesting one. Leg 59's repair changed which weights the search is
allowed to use, and property 3's error **did not move by a single digit**. Leg 59 wrote its own
conclusion into its data: *any future proposal must change the fitness's definition, not its
wall model.*

This leg took that instruction literally.

## Two new definitions, named before they were run

Both were written into the runner's docstring, with predicted failure modes, before a number was
computed. The file's first commit is the receipt.

**Definition one — score the norm, not the residual.** The incumbent score is a ratio: how big
is the current numerical state's leftover error, divided by how much error the certificate could
absorb. But a searcher is choosing a *norm*, and the numerator is mostly a property of how good
your numerics happen to be that day. So: drop the numerator. Score the weight purely on how much
error the certificate could absorb.

**Definition two — measure the defect above the noise.** Every residual computed in floating
point has a floor: below some size you are measuring your own arithmetic, not your equation. So
subtract that floor off, component by component, and add it back once as an anchor so the score
doesn't collapse to zero at the solution.

Plus two controls. One does nothing at all — it must reproduce leg 59 exactly, or the machinery
is lying. One changes no definition but computes the residual in higher precision — because if
the problem is arithmetic rather than definition, that one should move and the definitions
shouldn't.

## The answer: no, and both definitions made it worse

At the frozen settings:

| the score | property 3 error | vs incumbent |
|---|---|---|
| incumbent (control, reproduces leg 59 exactly) | **0.342** | — |
| **new definition one** | **1.000** | **+0.658 — worse** |
| **new definition two** | **1.034** | **+0.692 — worse** |
| higher precision (control, *not* a new definition) | **0.332** | **−0.010 — better** |

The threshold is `0.05`. Nobody is close.

But look at which column moved. Three kinds of repair have now been tried on this property:

- **the search box** — legs 50 and 59 — moved it by `0.0000000000`;
- **the definition** — this leg, twice — moved it *away*, by `+0.658` and `+0.692`;
- **the arithmetic** — this leg's control — moved it *toward*, by `−0.010`.

That `−0.010` is the first movement in the right direction since leg 49. It closes 3.5% of the
gap. And it came from the one change that wasn't a change of definition at all.

## What property 3 is actually measuring

Here is the punchline, and this leg is the third party to arrive at it.

The known-answer probe pushes the state by `ε` and reads the slope. It correctly refuses to use
`ε` that are too *large* — a repair leg 50 installed, because the linearisation breaks down up
there. It never checks whether `ε` is too *small*. The grid runs down to `10⁻¹¹`.

The state's own floating-point error is `4.8 × 10⁻¹¹`.

So the bottom of the probe's grid sits **underneath the floor of the thing it is probing**. Down
there the ladder is measuring roundoff, and the fitted slope is a report on the arithmetic.

None of that is new. It is standard numerical-optimization knowledge — Moré and Wild's ECnoise
paper says a computed function's noise level is a lower bound on what you can difference through,
and the whole derivative-free-optimization interval literature is about balancing the two ends.
And this repository's own leg 59 measured it *for this exact object*, correlated it (Spearman
`−0.878`), and deliberately left it out of the frozen gate because its territory was the wall
model. Its data file says, in as many words, "this is a defect in the fitness's definition, not
in the box."

What this leg adds is that you can now **rebuild the whole ladder from the floor alone**. Take
`ρ = A F(z*)` — the state's residual mapped into state units — and reconstruct every weight's
slope without evaluating the PDE at a single perturbed state. It reproduces the measured slopes
to `0.058` worst, `0.021` median, and reproduces the headline `0.34` as `0.31`. The 11% shortfall
is the second-order term the model deliberately drops.

A correlation is consistent with several stories. A reconstruction is consistent with one.

## The uncomfortable part

Coarsen the grid from 201 points to 101. The conditioning improves, the floor drops by 103×, and
the probe's bottom rung — which is a fixed number — is suddenly *above* the floor instead of
below it.

**The unmodified, unrepaired, three-times-failed leg-49 fitness then passes the frozen gate 6/6.**

Nothing was fixed. The grid got coarser.

The ban lifts on "a gate that PASSES on a repaired fitness." That sentence pins neither the
resolution nor what "repaired" means. As measured, its condition is reachable by coarsening.

So this leg reports that and refuses to use it. The frozen configuration is 201/401, the answer
read off it is **no**, and no GA compute ran on either branch of this gate — not when the
candidates failed, and not when the control passed at a resolution nobody froze. Whether the
ban's wording should pin the grid is a decision for the user.

The control that makes this a mechanism rather than a coincidence is definition one. It threw
away the residual, so it is blind to the defect by construction. Coarsening the grid moved every
other score by between `3.8×` and `34.9×`. It moved definition one by `0.99998×`. A knob that
moves everything that watches the defect, and nothing that doesn't, is a knob on the defect's
floor.

## One thing this leg got wrong

The first version of the runner's docstring predicted that the ladder's fitted slopes would come
out **identical to sixteen digits** across different weights, and cited two entries in leg 59's
data as proof, and invoked the standing lesson that identical numbers are a tell.

They are not identical. They are `0.83781001` and `0.83781002`. Twenty-one slopes, zero exact
duplicates.

The weaker claim survives and is what gets made: the slopes fall into **10 clusters** at a
tolerance of one part in a thousand. That is still the mechanism — weights that select the same
component share a slope — just not the dramatic version. The correction is in the docstring, in
the data file, and pinned by a test, so it cannot quietly revert.

## The ceiling

No link of the chain moved. This is a property check on a float-precision score defined over a
1D toy linearisation whose exact profile has been known since 1985. It is not a certificate, it
says nothing about the Hou–Luo profile, and it does not reopen stage B — which was closed on the
search space, independently of any fitness.

What it does is retire a route. The fitness's *definition* was the last of the three named repair
directions, and it is now measured dead in the two forms the plan named: one of them can't
satisfy property 3 by construction, and the other fails on the accuracy of the floor estimate it
needs.

The property that keeps failing was never asking about the fitness.
