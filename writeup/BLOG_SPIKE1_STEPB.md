# Letting the data pick your unknowns

*Spike 1, Step B — building the rescaled 2D Boussinesq solver*

In the last post we built one gadget: an operator that, given the swirl (vorticity) of a 2D
fluid, recovers its velocity — on a *stretched* grid that can see across many decades of scale,
which is what you need if you're hunting a singularity that lives at a single point. This post
is about wiring that gadget into the full machine: a solver whose *steady state* is a
self-similar blow-up profile. If it relaxes to the profile the mathematicians Chen and Hou
proved exists, our machinery works.

Building it turned up a decision I didn't expect to have to *measure* my way through.

## A fork in the road: which quantities do you actually solve for?

The physics is written in terms of two fields: the vorticity `ω` and the buoyancy `θ`. The
obvious move is to track those two. But the paper we're reproducing tracks something slightly
different — not `θ` itself, but its slopes `θ_x` and `θ_y`. Three fields instead of two. More
work. Why would you do that?

Here's the thing the whole scheme balances on. To keep the blow-up "centered" as it sharpens,
the solver constantly reads a few numbers *right at the singular point* — the slope of `ω`
there, the curvature of `θ` there. Get those reads slightly wrong and the whole run drifts. And
an earlier lesson (from the 1D warm-up) was blunt: **reading high derivatives at a point is a
noise amplifier.**

So: does tracking `θ` directly, and reading its *curvature*, cost you accuracy versus tracking
the slope `θ_x` and reading *its* slope? I could argue it either way on a whiteboard. Instead I
built a tiny experiment with a hand-made test case where I knew the exact answer, and measured
both. The verdict wasn't close: reading the curvature off `θ` is **about twice as noisy and
twice as inaccurate**, at every resolution. (The reason, once you see it: the natural way `θ`'s
curvature shows up in the math also mixes in an unrelated quantity — the `y`-curvature — that
you then have to subtract back out, and subtractions of nearly-equal numbers are where accuracy
goes to die.)

So we track the slopes. Not because the paper does, but because the measurement said so — and
now we know *how much* it buys us. (My collaborator made the final call to keep all three fields
rather than cut a corner, so that the target we relax to is *exactly* the proven one.)

## The nicest surprise: the number you care most about is the easiest to get

There's a small piece of poetry in the result. The single most important control number in the
solver — call it `c_l`, the rate at which space rescales — is computed as a **ratio** of two of
those delicate origin reads. Ratios are forgiving: whatever small, consistent bias the
measurement has, it's the *same* bias top and bottom, so it cancels. In the test, each
individual read was good to about 1 part in 50,000; the ratio was good to 1 part in
10,000,000,000,000,000. The quantity the machine leans on hardest turned out to be the
best-behaved thing in it.

Every piece — the transport that carries the fields around the stretched grid, the gradient
operator, the origin reads — was checked the same way: against a problem with a known answer,
and under grid refinement (so it's genuine convergence, not one lucky grid). All green.

## Where this leaves us — and the part I won't dress up

The machine is **built and it runs**. That is exactly as far as this post goes. Whether it
actually relaxes to Chen and Hou's profile is the *next* step, and it's running as I write this.
The early signs are genuinely mixed and I'd rather say so than spin it: the one number that's
supposed to be universal — the far-field decay exponent — is settling right where it should
(around `−0.34`, matching the paper). But the run isn't cleanly converging: some of the
gauge-dependent numbers are slowly drifting, which means there's a bug or a boundary leak to
hunt down before I'd call anything a success.

And the honest frame, unchanged: even a *flawless* result here reproduces something that was
already **proven** in 2022, on a toy model that isn't the real 3D problem. It validates our
tools. It is not new mathematics and it is not a proof. We're building the ladder; the interesting
climb is above it.

*Next: Step C — does it reproduce the profile, and if not, why not?*
