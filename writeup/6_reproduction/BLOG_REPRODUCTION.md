# We read all 166 pages twice, rebuilt the thing, and measured the Lean. Here is what held and what didn't.

*Arc 6, second pass, of a search programme for finite-time blowup in 3D Navier–Stokes. Legs 423–434,
2026-09-09/10, run as a conductor with five agents at a time. Companion to
[`TECHNICAL_REPRODUCTION.md`](TECHNICAL_REPRODUCTION.md), which carries every number and where it came from.*

---

## Where we were

The first pass of this arc (legs 417–422) had read the beginning and the end of OpenAI's 166-page
manuscript claiming forced Navier–Stokes blowup, counted the Lean project's `sorry`s at source, and
asked our own wall the only question that is ours. The banner it left on the README said, honestly for
the time: *Sections 4–9 were not read and the Lean was not compiled.*

The user's charter for the second pass was blunt: read all of it, re-derive the spine, instantiate the
construction in our own machinery, and measure the Lean rather than assume it. Five agents at a time,
one file per agent, and one of every five an adversary who never sees how the others reached their
answer — because a finding only earns the word `VERIFIED` when someone who never saw the construction
reproduces it.

## Reading, twice

One session read all 166 pages and wrote a ledger: 79 numbered statements, each with its hypotheses,
its conclusion, its constants and its citations; 13 pages flagged as hard, the hardest being the
bookkeeping of the correction cycle and the parameter schedule of Appendix A.

Then five fresh agents read the same pages without seeing that ledger. They agreed with it on
content everywhere; where they differed it was always about *how many* cross-references to list,
never about *what a statement says*. They also produced the most useful list of the wave: 29 things
they could not determine, 15 of which turned out to be the PDF's text layer losing fraction bars — one
of them settled by measuring the fraction bar's coordinates on the page — and exactly one of which
was about the paper itself (a proposition asserts its exponents exist without displaying them).

## The graph, and the two propositions nobody cites

Before drawing the citation graph we wrote down what we expected of it. It refuted half our
expectations, which is what pre-registration is for. The graph is acyclic on three independent
passes. It is not complete, and the most interesting dangling nodes are **Propositions 9.5 and 9.6**
— stage zero and the inductive step of the correction cycle — which no downstream statement cites,
by name or by equation. The summation that follows them says "the finite corrections above". A graph
cannot say whether that is a gap or a writing habit. The re-derivation can, and did.

## Fifty-eight statements, four agents, one blind verifier

Four agents re-derived the 58-statement spine — 480 steps, 301 constants recomputed. They found no
`GAP`. A fifth agent was handed ten of the 58, drawn by a seed, and never shown the four files. It
agreed on ten of ten. Those ten nodes are the only things in this arc marked `VERIFIED`. The smallest
closing margin in the correction cycle's exponent ledger is 0.07; the pre-registered guess that we
would find at least three gaps was wrong.

This is a consistency check on a manuscript's spine. It is not a proof, and the journal says so on
every page.

## Building it

Then we built the thing. Lemma 4.8's outer profile — the self-similar vortex the whole construction
starts from — was instantiated from the paper's own Appendix A schedule, in the paper's own parameter
order, with nine gates and six planted controls written down before the runner existed.

The constants reproduce. The bracket numbers on page 133 reproduce to four digits. The exponents on
the reserved patches are exact. The pressure datum reproduces with margin. The pulse-end moment
cancellation reproduces to `10⁻¹²` at the paper's normalisation.

The closure does not. At every parameter value a grid can reach, the equation that is supposed to fix
the pulse amplitude has no root in the paper's bracket, and the reason is the paper's own arithmetic:
the remainder the bracket has to absorb is `(λ^{−120λ} − 1)/2`, which is `10¹²` at `λ = 0.1`. We swept
downward until a root appeared: **`λ ≤ 3·10⁻⁴`**. The cone condition on the intermediate interval
fails for a second reason with the same flavour: it needs `√λ P_*` small, and the paper's order of
choices makes `P_*` about `7·10⁵` before `λ` is chosen. None of this contradicts the paper, which asks
for `λ` "sufficiently small". It measures what "sufficiently" means, and it is far beyond any grid.

Two of the six planted controls could not fire. We say so, with the arithmetic of why, rather than
replacing them with controls that would have.

## The stress at the edge, and a collar `10⁻⁶⁹` wide

The residual stress the profile leaves on its outer tail was computed two ways — from the definition
in §4 with Lemma A.8's backward moments, and from the paper's explicit formula in Appendix A at three
physical scales — and the two agree to `10⁻⁹`. Its sign, its `e^{−4/δ²}` outer weight, its exact
vanishing beyond the edge, its shear bracket, its scale invariance: all reproduce.

Writing the formulas out by hand before running them exposed something the pre-registration had
missed, and we amended it before any number existed. The term that carries the paper's quoted
outer-edge powers is smaller than the dominant term by a factor of `X`, and `X` at the edge is about
`10²⁰⁷`. The paper's `δ⁻³`, `δ³`, `δ⁶` are correct as limits, on a collar of width about `10⁻⁶⁹`. At every
resolvable distance from the edge the paper's own Lemma A.9 predicts `δ⁰`, `δ³`, `δ³`, and that is what
we measure. The paper's conclusions — positivity, direction, a strict cone margin — hold either way.

Along the way we caught our own pre-registration in a slip: a cutoff constant it claimed satisfied
the paper's bound `h/4` in fact gives `0.4h`. The gate that matters still holds. The slip is recorded.

## The Lean, measured

Five agents, one file each. The build was measured, not assumed: this time the cache host answered,
mathlib compiled without error, and the theorem's module was not reached inside the agents' window.
The Conductor let the build run on afterwards, and it got there: the whole NavierStokes library compiled
with zero errors, and the kernel reports that both exported theorems rest on nothing but Lean's three
standard axioms. That is one run in one container, unreplayed by any independent checker — but it is
the kernel, and it said yes. The top-level theorem, read quantifier by
quantifier, is Fefferman's (C) and (D), which is strictly weaker than the paper's Theorem 1.1: five of
its twelve clauses are absent from what the Lean would prove. The `sorry` count is four, all four the
challenge placeholders the comparator setup requires. Source coverage of the 79 statements is 74
formalized, 5 partial, none absent — a reading, not a kernel check, and every agent said so.

> **Superseded in part 2026-09-10 (arc 7, leg 437) — added beside, nothing above rewritten.** "One run in one
> container" was arc 6's position and is no longer the record. Arc 7's unit `K1` ran the same check on the same
> pin in **three environments** (two remote containers and the operator's laptop): all GREEN, 11251 jobs, 0
> errors, both theorems on the same three axioms, `sorryAx` not reachable anywhere. And leg 435's build — the
> one this section describes — is now recorded as never having **completed** (`CORRECTIONS.md` §72). What does
> **not** change: the statements are still Fefferman's (C)/(D), strictly weaker than Theorem 1.1; mathlib was
> replayed from the official cache, not rebuilt; and the result is still **`UNVERIFIED`**, because a second
> machine is not a second agent. Record: `experiments/journal/leg_437.md`.

## What the adversary said

Wave 4 sent four agents at the rest of the construction — the annulus pulses, the correction
iteration, the two headline norms, the compact support of the force — and a fifth agent whose only job
was to fake their signals from deliberately wrong runs, seeing nothing but the gate definitions. The rule,
fixed before anyone started: a signal the adversary can fake is not evidence, whatever the worker found.

The adversary faked eleven of twelve. Not because the workers were careless — their own numbers are
the most interesting in the wave — but because the gates the Conductor wrote were, as defined, things
any transcription of the paper's algebra would pass: a joint norm that cannot see the small stress
component, a "convergence exponent" that belongs to the averaging window, a `±0.02` window on a
per-stage gain the paper states as `10⁻⁸`, refinement stability that is automatic for a prescribed
field, support clauses that are tautologies of the cutoff. The one signal that survived is a measured
gap: the force the leading order alone would need grows like `q^{−3/2}` toward the singular time, and
the paper's corrections must close every power of it.

What the workers actually found is better than their gates. The pulses' exact identity holds to
`10⁻¹⁶`, and the paper's own admissibility condition places the pulses at `log₁₀ q` below about `−7·10⁸`.
The correction ledger's 29 inequalities hold, with a smallest margin of 0.02, and the gain per stage is
`10⁻⁸` in `q` — invisible to any float. The energy headline is carried by the cutoff, not by the profile's
decay: the un-cut-off leading field has infinite energy at every time. The residual vanishes exactly
outside the edge, and the flatness the theorem needs at the singular time is a gap of every power
between the leading order and the corrections. Each of these is a place the paper assigns to a part of
the construction nobody here instantiated.

## What this is not

It is not a proof, and it does not verify one. It is Tier 2 throughout. No wall of ours moved. What it
is: a repository that can now say, unit by unit and with numbers, what in a 166-page claim it could
reproduce, what it could not, and exactly where the difference lives.
