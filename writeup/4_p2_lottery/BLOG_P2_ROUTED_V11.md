# The floor we had been treating as physics was our search

*Route-D v11 of a Navier–Stokes blow-up search. Level-1 tooling plus a structural
positive. Not a certificate, not rigorous, not a Clay result.*

---

For eleven legs this project has been improving the *constants* in a
certification argument, and the previous leg finally measured what that can buy:
not enough. Perfect bounds on both remaining constants only just reach the
threshold, with nothing spare for the three that are still unbounded.

There is another factor in the inequality, and nobody had touched it. The
argument needs the candidate profile's **defect** — how badly it fails to solve
the equation — to be below a budget. Every profile we had for the interesting
case came from a genetic algorithm over a handful of shape parameters, or from
relaxation on a fixed grid. Both floor around 1e-2. We had been reading that
number as a property of the problem.

It is a property of the search.

## Newton, with two gauges

The equation has a two-parameter family of exact solutions at the anchor point,
which means the linearisation is singular and one normalisation is not enough —
solved directly with one gauge, Newton crawls to 1.8e-6 in forty iterations. With
two gauges and a least-squares step it reaches 2e-15 in five, and the convergence
is visibly quadratic.

The first check is the one that matters most: at the anchor the true solution is
known in closed form, and Newton must *not* reproduce it. It finds a zero of the
**discrete** system, which sits a small distance away — while the exact continuum
profile scores 7.7e-9 on the same discrete equations, which is precisely its
discretization error. A solver that returned the continuum answer exactly would
be reporting something impossible.

Then the sweep: **twelve orders of magnitude** below the old floor, everywhere
the solution exists.

## Where it exists — and the check that stopped me over-claiming

Newton also converged at large (still positive) advection strength, past the survival
boundary the GA had mapped on positive `a`. For about an hour that looked like the headline: the boundary is a
genome artifact.

It is not. Machine precision on a discrete system proves nothing on its own — a
solver can null discrete equations with something that has no continuum limit.
The test is whether the *solution* stops moving as the grid refines. Below
`a ≈ 0.5` the wave speed is stable to one part in 10⁵ across a 4× refinement.
Above `a ≈ 0.8` it moves in the third digit and two of three grids fail outright.
The large-`a` successes are solver artifacts.

So the boundary the GA found survives — now confirmed by a fourth, completely
independent method, one with no genome, no search budget and no randomness. And
the character is sharper than before: below the boundary an exact discrete
traveling wave *exists*.

## What it actually does to the budget

Less than the headline number suggests, and this is the part worth being careful
about. The certificate does not look at the root-mean-square residual. It looks
at a *weighted* defect that amplifies the far field — and there the numbers are
six orders larger, typically 1e-8 to 1e-7, and at one value of the parameter
1.5e-2, which is *above* the budget.

So the honest statement is a change of binding constraint rather than a solved
problem:

> The profile's defect is no longer limited by our ability to find a profile. It
> is limited by how well our grid resolves the far field — which is a problem
> already on the list, and a much better problem to have.

"Find a better profile" is a search. "Control the far-field discretization of a
profile we can now compute to machine precision" is a statement about a known
object. The second one has a method.

## The lesson

We carried a number for five legs — 1e-2 — that was never a fact about the
equation. It was a fact about the two tools we happened to be using, and both
have the same weakness. Nobody re-derived it because it appeared in every
measurement, which is exactly what makes an instrument artifact hard to see.

And the thing that stopped the correction from turning into an over-claim was
one table: refine the grid, see whether the answer moves.

---

**Data + code:** rebuilds from `writeup/data/p2_route_d_v11_anchor.json` via
`p2_route_d_v11_evidence.py` (figure `fig29`); solver in
`solver/profile_newton.py`, six gates in `test_profile_newton.py`. Technical
companion: `TECHNICAL_P2_ROUTED_V11.md`.

**Honest ceiling:** nothing interval-enclosed, nothing rigorous, no certificate.
Overall odds on the Millennium problem from this line: ~0.05%.
