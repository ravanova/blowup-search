# We built a machine for singular blow-ups, and checked it against a shape we could solve by hand

*Phase 2, P2 — starting the swing at something genuinely new, honestly*

For the last stretch we've been building solvers for a hard question in fluid math: can a smooth
flow spontaneously form a singularity — a point where the equations blow up — in finite time?
Our earlier work reproduced a blow-up that other mathematicians had already *proven* exists. That
validated our tools, but it wasn't new. This post is about aiming the tools at the frontier, and
the first honest step: making sure they work on a case where a genuinely singular shape is
involved.

## The frontier: a "singular" blow-up nobody has proven yet

Most studied blow-ups have *regular* profiles: as the flow concentrates, its shape (suitably
rescaled) settles onto a nice bounded curve. In early 2026 a group (Chen, Huang, and Li) reported
something stranger, numerically: starting from carefully *degenerate* initial data — flat to
higher order at the center — the rescaled shape settles onto a profile that is itself **unbounded**
at a point. A singular limit shape. They see it in two stages, and they call it previously
unreported. Importantly, they've only *proven* a small piece of it (that one exact singular shape
exists in a weak sense); the interesting claim — that generic degenerate flows actually get pulled
onto that shape — is so far **only numerical**. That gap is exactly the kind of place where new
mathematics can live.

## The lucky break: an exact shape with a formula

Buried in their paper is a gift. For the simplest model (a 1-D equation that stands in for the
boundary behaviour of the 3-D problem), they write down an *explicit* singular steady shape:

> Ω̄(X) = 1/√(X−1) for X > 1, and 0 otherwise.

It's genuinely singular — it goes to infinity at X = 1 — but it's a formula. And with a classic
identity for the Hilbert transform, we could derive, **by hand**, the exact velocity that goes
with it: `U(X) = 2√(1−X) − 2` on one side, and a flat `−2` on the other. Three independent
sanity checks all line up (the value at the origin, the value at the singular point, and an exact
cancellation in one of the equations). So now we have a known answer to test against — the same
trick that made our earlier 1-D work trustworthy.

## Does our machine survive an *infinite* shape?

That's the real worry. Every tool we built assumes reasonably smooth, bounded shapes. Feed it
something that blows up at a point and it could quietly produce garbage. So before building
anything new, we ran a cheap probe: hand our existing Hilbert-transform operator the singular
shape and compare to the exact answer we derived.

It **survives.** Right up against the singularity, the operator gets the answer to a few percent
and keeps improving as we refine. The only real error lives far out in the shape's slowly-fading
*tail* — and that error shrinks steadily as we enlarge the computational domain. In other words,
the hard-looking singularity is *not* the problem; the slow tail is, and it's the same,
well-understood issue we already know how to patch. (Picture on the right of the figure: the bar
at the singular core shrinks with refinement; only the far-tail bar stays tall.)

## Standing the machine up, and checking every number

With that green light we built the actual 1-D solver — the transport, the buoyancy field, and the
new ingredient, a velocity that has to be *integrated* from the vorticity and pinned at the
center. Then we validated it against the exact anchor, five checks, all passing:

- the velocity operator matches a clean analytic formula to one part in 100,000;
- run through the full machinery it recovers the singular shape's velocity, converging as we
  refine (at exactly the fractional rate the square-root singularity predicts);
- the exact singular shape sits as a genuine steady state of our equations;
- and a consistency relation the paper's constants must satisfy comes out *exactly* zero.

The left panel of the figure says it best: our recovered velocity lies right on top of the exact
curve, straight through the point where the shape goes to infinity.

## A speed win along the way

The user asked us to look at performance, and it paid off. The slow part turned out to be a shared
piece of old code — a series computation buried in the Hilbert operator, plus a matrix built one
column at a time in a Python loop. Rewriting both (a batched solve, and a leaner series evaluated
the efficient way) cut a key build step by 21×, another by 3×, and took our test suite from over
two minutes to under four seconds — with the accuracy digits *unchanged*.

## What this is, and isn't

Plainly: **this reproduces something already proven. It validates our machinery; it is not new,
and it is not a proof.** Same honesty bar we've held all along. But it's the necessary first step,
and it's now a small, self-contained, data-backed result on its own — including an explicit
velocity formula for their singular profile that the paper didn't spell out.

The genuinely new swing comes next: let the machine *evolve* generic degenerate data and ask
whether it really gets pulled onto that singular shape — the stability claim that currently rests
only on the original authors' numerics. We'll write down the pass/fail bar before we run it, as
always. The overall odds of touching the million-dollar version of this problem remain tiny (call
it 0.05%). But the realistic prize — new, shareable, carefully-checked results about how these toy
singularities form — is squarely on the far side of this machine, and we've now confirmed the
machine can hold a singular shape without falling apart.
