# We re-checked the empty square. Someone has claimed it.

**Route-GAF v1, leg 303, 2026-08-11.**
Data: [`writeup/data/p2_route_gaf_v1_sweep.json`](../data/p2_route_gaf_v1_sweep.json).
Figure: [`fig71_route_gaf_v1_cell.png`](../figures/fig71_route_gaf_v1_cell.png).
Runner: `experiments/p2_route_gaf_v1_sweep.py`. Novelty log: `writeup/novelty/leg_303.md`.

## The square

This project keeps a two-by-two table of everything anyone has ever *certified* about
singularity formation — certified in the strong sense, where a computer checks a chain of
rigorous bounds and the theorem does not stand without it.

One axis asks **where the viscosity is**. In the strong case, "Grade A", the dissipative term
sits *inside the equation the computer encloses*: the certificate is about a viscous problem.
In the weak case, "Grade B", the computer encloses the *inviscid* problem, and viscosity is
handled afterwards by an argument that it is too small to matter.

The other axis asks **what kind of equation it is** — a fluid transport model, or something
else.

Three of the four squares have occupants. Dahne and Figueras certified self-similar blow-up
for complex Ginzburg–Landau with the dissipation parameter genuinely inside the enclosed
equation: Grade A, but not a fluid. Buckmaster, Cao-Labora and Gómez-Serrano proved
finite-time singularity for compressible Navier–Stokes, but the object their interval
arithmetic encloses is the inviscid Euler profile, with viscosity dominated afterwards:
fluid, but Grade B. Chen and Hou's celebrated 3D Euler result is inviscid throughout.

**The Grade-A/fluid square is empty.** A computer-checked certificate for a blow-up profile of
a fluid transport model, with the viscosity still in the equation being checked. Leg 174, which
built the table, wrote that the square is empty *"for want of a target, not a method"* — the
machinery exists and has been aimed at dissipative equations; nobody had aimed it at a viscous
fluid.

That empty square is not a curiosity. It **is** Phase 1's premise: *no certified viscous
blow-up exists in any model, in any dimension, today.* Everything downstream leans on it. And
nobody had re-checked it in five days and roughly 130 legs of work.

## What we did

Thirty-five arXiv queries in five channels, every string written down before the first one
ran, every returned link recorded rather than counted. Twelve of the thirty-five are leg 174's
own queries, re-run verbatim, so that "nothing changed" would be a measurement and not a
memory. Twenty-three are new — including the whole compressible/implosion axis that leg 174
never asked, which is exactly how a 2022 paper sat outside the table until leg 197 noticed it.

Sixty-eight distinct papers came back. Six queries first came back as HTTP 429 and timeouts;
we re-ran those six slowly rather than let a rate-limit masquerade as a zero. All thirty-five
eventually landed.

The rule for what counts as a hit was fixed in advance, four clauses, all required: a
computer-assisted certificate, of a blow-up profile, with the dissipation inside the certified
object, for a fluid transport model.

## What came back

Leg 174's own twelve queries return **exactly the counts leg 174 banked — 0 of 12 grew.** By
that measure, nothing has changed and the square is still empty.

But one paper cleared all four clauses, and it is not in our table.

**[arXiv:2604.09949](https://arxiv.org/abs/2604.09949)** — *Stable Finite-Time Singularity
Formation for 3D Navier–Stokes via 5D-Lifted Axisymmetric Reductions*, Rishad Shahmurov,
posted 2026-04-10. From the abstract: a stationary rescaled profile solving a nonlinear
elliptic fixed-point equation in a weighted Hilbert space, "together with a computer-assisted
Newton–Kantorovich validation based on interval arithmetic", for the 3D incompressible
Navier–Stokes equations on the torus.

If that is what it says it is, it does not merely fill the square. It resolves the Clay
problem, in the negative.

## Why we are not celebrating, and not dismissing

**This leg's job was to look, not to judge.** The adversarial full-text read is a separate leg
(309) precisely so that whoever does it is not the person who found it. So the square is
recorded as **claimed, not filled**: zero *established* occupants, one *claimant*. Phase 1's
premise is not recorded as broken.

What we can say from the abstract and the metadata, and do record: the abstract describes the
manuscript as "organized **in the style of** a computer-assisted proof paper" — a statement
about presentation, not about a completed verification. Single author, v1 only, no page count,
no journal reference, no visible uptake in the four months since posting. And the claim, if
sound, would be one of the most consequential results in the history of the subject, arriving
without a ripple. Those are the priors. They are not a verdict.

## The uncomfortable part

The paper was returned by **leg 174's own query #12**, whose count has not changed since. So
leg 174's net saw it. Did leg 174 read it and reject it, or never open it?

**We cannot tell** — because leg 174 banked *counts*, not links. Seven of its twelve queries
returned something; ten links in total; none of them written down. That is this project's own
"links, not counts" lesson coming back four months later to charge interest. This sweep records
all thirty-five queries with their full link sets, so the next leg to stand here will not have
the same hole.

There is a second, sharper reason the paper may have been invisible: it writes its own subject
as `Navier--Stokes`, with the LaTeX double hyphen, throughout title and abstract. A search
string or a regex spelling it `Navier-Stokes` **does not match it**. Our own mechanical screen
scored it a near-miss for exactly that reason, and a human override is the only thing that
promoted it. A silent false-negative channel, aimed squarely at the one model this project
cares about most.

## The other half: the NRS/Tsai screen

The second question was whether anything has moved the boundary that stops us aiming a
self-similar viscous ansatz at 3D Navier–Stokes directly. Answer: **not at the exclusion
boundary.** Five boundary-adjacent works turned up; the only one that moves the line at all
([arXiv:1610.09464](https://arxiv.org/abs/1610.09464)) moves it *outward*, excluding more. The
rest are non-uniqueness and Type-I results, which the screen was never about.

## Where the near-misses cluster

Of the papers we adjudicated by hand, five fail on "no certificate" and four on "inviscid
object." That split is the state of the field in one line: **the analysts prove blow-up for
dissipative models without a computer, and the computer-assisted community certifies inviscid
objects.** The most recent method paper in the whole sweep
([arXiv:2607.15256](https://arxiv.org/abs/2607.15256), 26 days old) sharpens exactly the
machinery the empty square needs — and aims it at 3D Euler. Leg 174's phrasing survives its
own re-test: for want of a target, not a method.

Clay odds unchanged at ~0.05%. A freshness re-check of somebody else's literature moves no
link of our chain — and if leg 309 comes back saying the claimant holds, the thing that
changes is not our odds but our premise.

---
*Technical companion: [`TECHNICAL_P2_ROUTEGAF_V1.md`](TECHNICAL_P2_ROUTEGAF_V1.md).*
