# The hardest part of going to 2D turned out to be one line of algebra

*Sequel to [BLOG_SPIKE0_RESCALING.md](BLOG_SPIKE0_RESCALING.md) ("We built the far side of
the wall, and it held"). Technical record:
[TECHNICAL_SPIKE1_VELOCITY.md](TECHNICAL_SPIKE1_VELOCITY.md). Figure and committed data
rebuild with `python writeup/3_spikes/spike1_stepA_evidence.py`.*

Last time, in 1D, we watched a change-of-variables solver zoom into a forming singularity
and hold it still as a steady profile — and, crucially, reproduce a shape we already knew
in closed form. That was Spike 0. It validated the *technique*. But 1D is a rehearsal. The
model we actually care about is 2D Boussinesq: the "poor man's 3D Euler," the toy where a
buoyancy force does the same job that vortex stretching does in the real Navier–Stokes
problem, and the one Chen and Hou proved blows up in 2022.

So the plan is to port the 1D machinery up a dimension and reproduce *their* profile. This
is a multi-week build, and when you're staring down a multi-week build the smart move is to
find the single scariest piece and do it first, alone, against an answer you can check. If
it works, the rest is assembly. If it breaks, you find out now instead of in week three.

## The scariest piece

In 1D, the nonlocal heart of the equation was the Hilbert transform, and the hard part was
that our stretched grid killed the FFT that normally computes it — so we had to build a
non-FFT Hilbert transform by hand. In 2D, the nonlocal heart is the **velocity**: to move
the vorticity around, you have to solve for the flow it induces, which means solving a
Poisson equation `−Δφ = ω` and reading off `u` from `φ`. Same problem as before, one
dimension up: on a uniform grid it's a one-line FFT, and on the stretched grid we *need* —
because the real profile spreads out over a huge range of scales with a slowly-decaying
tail — the FFT is off the table.

A 2D Poisson solve on a stretched, non-uniform grid, with boundary conditions on a wall,
no sparse-matrix library available. That's the scary piece. That's Step A.

## The geometry, honestly transcribed

Here the project's iron rule kicked in: *don't reinvent the numerics — ground them in the
paper.* Every time this project tried to be clever about a known method it got burned; the
1D win came from carefully reading what Chen and Hou actually do. So before writing a line
of solver, I pulled their papers and transcribed the setup exactly.

The singularity sits in a corner where a wall meets a symmetry axis — the "Hou–Luo
geometry." By symmetry the whole problem lives in a single quadrant, and the stream
function `φ` is pinned to zero on both edges. The velocity is `u = −φ_y`, `v = φ_x`. The
scaling has the profile decaying like `r^{−1/3}` out to infinity, which is the thing that
forces the stretched grid. All of this is their Part I, equations (2.3)–(2.5) and (7.1);
none of it is mine.

One thing worth flagging, because it quietly makes the whole job easier: the version of the
method for *smooth* data uses a **single** zoom factor, not two. Somewhere in our old notes
was a worry that we'd need a fancier two-scale rescaling to keep things stable. That worry
came from a *different* Chen–Hou paper, about rougher data. For the profile we're chasing,
one scale is what they use — and one scale is exactly what Spike 0 already showed can be
stable. Good omen.

## The one line of algebra

Now the discretization. I wanted the Poisson solve to be something I could actually build
and *verify*, not a black box. So: use polar coordinates, put the radius on a logarithmic
grid (equal steps in `log r`, so the grid naturally spans many scales — the same trick that
cured our 1D timestep problem), and expand the angle in sines that automatically vanish on
both walls.

Then something nice happens. Write the Poisson equation out in these coordinates and the
messy `1/r` and `1/r²` terms — the parts that make polar Laplacians annoying — *cancel*.
What's left, for each angular mode `n`, is about as simple as a differential equation gets:

> `φ_n''(ρ) − (2n)² φ_n = −r² ω_n`

A constant-coefficient, second-order ODE. One tridiagonal solve per angular mode, no sparse
library needed, and the two natural solutions `r^{+2n}` and `r^{−2n}` are exactly the
regular-at-the-origin and decaying-at-infinity behaviors I need to bolt onto the two ends.
The scariest piece of the 2D port reduced, on the right grid, to one line of algebra and a
textbook tridiagonal solve. That is the good kind of surprise.

## Did it work? Check it against an answer you already know.

The rule that has kept this project honest: *never trust a solver you haven't run against a
known answer.* A confidently-wrong result nearly derailed Spike 0. So I didn't test on the
real profile (which I don't know exactly). I **manufactured** a problem: pick a stream
function `φ*` out of thin air, differentiate it to get the exact vorticity `ω*` and the
exact velocity, feed the solver `ω*`, and demand it reproduce the velocity I already know.

It does — to about one part in a hundred thousand. And the part I care about most: as I
refine the grid, the error falls like the *square* of the spacing, a clean straight line on
a log-log plot (middle panel of the figure). That second-order line is the difference
between "it happened to be close on this grid" and "it is converging to the right answer."
The solver is converging to the right answer.

There's one more number on that figure worth explaining. The whole rescaling scheme steers
itself using a single reading taken *at the corner* — essentially the local shear of the
flow at the singular point. Get that reading wrong and the zoom drifts. In 1D-recon this
kind of pointwise reading was a notorious noise amplifier. Here, because of the angular-mode
structure, it falls out cleanly from a single coefficient, and it lands on its known value
(`−2`) to within `0.0008`. The steering signal is trustworthy.

## What this is, and what it very much is not

Step A is one validated component. It is not a blow-up, not a profile, not a proof, and not
2D anything yet — it's the velocity solve, checked in isolation against a problem I made up
so I'd know the answer. Next comes wiring it into the full rescaled equation with its
self-steering zoom (Step B), and then the real test: letting it relax to Chen and Hou's
published profile (Step C). And even when *that* works, it will be reproducing a result
they already proved, in a toy model that is one hard wall away from the actual Millennium
problem. Reproduction earns you trustworthy machinery. It does not earn you novelty, and it
certainly doesn't earn you a proof.

But the machinery is the point right now. The far side of the wall needed a 2D velocity
solver on a stretched grid, and today that solver exists and is verified. The scary piece
turned out to be a small miracle of coordinate choice. On to the assembly.
