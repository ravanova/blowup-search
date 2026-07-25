# The other profile: reproducing a regular self-similar blowup, and being honest about which number is real

*Phase-2 P2, the B1 leg. Companion to `TECHNICAL_P2_SCENARIO2.md`. Honest tier: a Tier-2
reproduction of a published numerical result — not novel, not a proof.*

The 1D Hou–Luo model has, in Chen–Huang–Li's (CHL) picture, two self-similar blowup profiles. One is
**singular** — a `(X−1)^{−1/2}` spike — and we reproduced it earlier, along with its local stability.
The other is **regular**: a smooth, strictly-positive, lopsided bump. This post is about reproducing
the second one, and about a discipline point that matters more than the reproduction: knowing which
number in your output is physics and which is an artifact of how you set up the problem.

## A gauge that can't hold the profile it's chasing

Dynamic rescaling zooms your coordinates into a forming singularity as it forms. To do that you need
a *normalization* — a rule that fixes the zoom rate. The natural rule for the singular spike pins the
zoom at the spike's location, `X=1`. But the regular profile peaks somewhere *else* (around `X≈0.8`).
Point a `X=1`-anchored gauge at an `X≈0.8`-peaked profile and it slides off — which is exactly what we
saw in an earlier run: the trajectory drifted past the regular profile and wandered away.

CHL's fix (their equations (4.1)/(4.2)) is elegant: give the rescaling an extra degree of freedom — a
*movable* origin — and pin the normalization at that origin instead of at a fixed point. The origin
becomes a "source of stability" that the system slides to wherever the profile actually wants it.
Concretely it's one more constant and a 3×3 linear solve at each step. We implemented it, and added a
unit test that checks the defining property directly: the gauge, by construction, must freeze three
quantities at the origin — and numerically it does, to one part in `10¹⁵`.

## It works — and then the honest part

Starting from two different generic bumps, the solver spirals onto the same answer (see the figure):
the **contraction exponent** `c_l/c_ω → −2.53`, versus CHL's published `−2.5114`. Same value from
different starting points — a genuine attractor, ~1% from the paper. The profile it lands on is
smooth, strictly positive, and lopsided: unmistakably the regular object, about a thousand times
smoother than the singular spike.

Now the part that's easy to skip and shouldn't be. The exponent `c_l/c_ω` is the real, physical
prediction — it doesn't care how you normalized your initial bump. But the *individual* constants
`(c_l, c_ω, c_r)`? Those land at `(1.59, −0.63, 0.21)`, while CHL report `(1.06, −0.42, 0.08)`. That
isn't an error. The normalization holds the origin values fixed at *whatever they were in your initial
data* — so the raw constants inherit your setup, and only their *ratio* is invariant. Report the raw
triple as a "match" and you'd be fooling yourself. The ratio and the profile shape are what we claim;
the triple we report as normalization-dependent and leave off.

There's a second honest line. The residual — how close we are to an exact steady profile — falls a few
decades and then **floors** at about `2×10⁻²`. CHL drive it to `10⁻⁶`, but they use an adaptive mesh
that follows the profile; we're on a fixed grid. So we wrote that ceiling *into the success criterion
ahead of time* rather than pretending we hit machine zero. The run passed all five clauses — including
the one that says "and here is the boundary we don't cross."

## Why bother reproducing someone else's result

Because it's not really about the result. Both of CHL's profiles are now reproduced by our machinery,
which is a nice consolidation — but the thing we actually needed was the *movable-origin gauge*. The
next question we want to attack is genuinely open: in a one-parameter family of these models, there's a
transition between two *different kinds* of blowup (a "two-scale" one that's been proven for one member,
and a "two-stage" one CHL found for another). Nobody has mapped where that transition happens. Sweeping
it means holding regular profiles like this one across the whole family — which needs exactly the gauge
we just built and validated.

So this leg is a de-risking brick, said plainly: not the swing at something new, but the tool the swing
needs. The odds on the big prize haven't moved. The toolbox got one piece more trustworthy.

*Data and code: `writeup/data/p2_scenario2_relax.json` (committed), `experiments/p2_scenario2_relax.py`,
figure via `writeup/p2_scenario2_evidence.py`. All reproducible without re-running the solver.*
