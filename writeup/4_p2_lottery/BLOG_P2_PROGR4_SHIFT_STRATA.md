# We fixed the sampling bias. The orbits still didn't turn up. (PROG-R4, milestone M3)

The [previous run](BLOG_P2_PROGR4_G1.md) ended with a diagnosis rather than a result. We had gone
looking for eight specific published orbits in a turbulent flow, found eight *different* ones, and
worked out why: the pipeline that supplies starting guesses was quietly filtering on the very
property that makes the targets unusual.

Each orbit has a **shift** — how far the flow pattern slides sideways over one period. The eight
published orbits all sit between 0.295 and 0.707. Our candidate pool was overwhelmingly below 0.15,
because the score used to admit candidates turns out to be correlated with shift. We were handing
Newton's method a pool of small-shift guesses and then noting, with some puzzlement, that it kept
returning small-shift orbits.

So this unit did the obvious thing: **stop ranking candidates globally, and spend the budget in
shift bands with quotas fixed in advance.** Fill the band the targets live in, deliberately, and
see what happens.

It worked, in the sense that the budget really is stratified now. And the answer is still zero.

That combination is the whole point of the exercise, so it's worth being precise about both halves.

## The repair, and that it was a real repair

You cannot stratify at the stage where candidates are first scored, because the score is built from
amplitude spectra and is **shift-invariant by construction** — shift doesn't exist yet at that
stage. That is the same property that makes the pre-filter safe, and it's why the previous fix (in
*period*, where the coordinate does exist) doesn't transfer.

So instead of stratifying the mine, we **exhausted** it: take every anchored near-repeat the Newton
window cannot provably exclude, rank nothing, truncate nothing. That took the candidate pool from
2,014 to **75,873** — 37.7× deeper — and then stratified downstream, at the one stage where the
shift is known.

The results, against the previous run:

| | before | after |
|---|---|---|
| candidates in the published shift band | 35 | **72** |
| attempts seeded in that band | 31 | **60** |
| Newton iterations spent | 4,629 | **2,104** |

Note the last row. We did not buy the result with extra compute — the run spent **less than half**
the iterations of the one it is being compared to, because a stall-exit rule ends attempts that
have visibly stopped descending. That rule was validated first by replaying it against the previous
run's stored iteration histories: it would have cut **none** of its 14 convergences, with a factor
of 6.9 to spare. Everything else — tolerances, caps, the admission window, the matching rule — was
held at the previous run's values by assertion at startup, not by hand-copying.

## The result: the "we just weren't looking there" explanation is dead

Two explanations were written down in advance, before any of this ran, along with what would kill
each.

**"There aren't enough candidates in the band"** — plausible, and now **refuted**. Its premise was
repaired: the supply doubled, the spend doubled. Its prediction was that more in-band seeds would
produce a recovery. Sixty in-band attempts produced none.

**"In-band seeds are genuinely harder"** — favoured, but honestly, not settled. Comparing seeds of
*matched quality* across both runs pooled, in-band seeds converged 6 times out of 91 and
out-of-band seeds 17 out of 109. That's a real-looking gap, and it fails significance
(p = 0.073). It is a lean, and it is reported as a lean.

## What we found instead: Newton walks out of the band

Here is the sharpest thing in the run, and it is not a null.

Of the nine attempts that converged, five were seeded inside the published band. **Four of those
five ended up outside it.**

| seeded at shift | converged at shift |
|---|---|
| 0.619 | 0.587 |
| 0.397 | → 0.117 |
| 0.425 | → 0.100 |
| 0.311 | → 0.133 |
| 0.346 | → 0.101 |

Eight of the nine convergences finished below 0.15. Put a starting guess squarely in the band where
the published orbits live, and the solver *leaves*, reliably, and lands on the same handful of
low-shift solutions it always lands on.

That changes the diagnosis. The previous run's finding was about the **seed supply** — a filter
that removed large-shift candidates. This run removed that filter and got the same destination
anyway. So the bias is not only in what we feed the solver. It is in the **basin structure**: in
this flow, at this resolution, the low-shift solutions have the large basins, and Newton falls into
them from wherever you put it.

The honest caveat is that "the basins are bigger" and "our particular globalisation strategy drifts
that way" are not distinguished by this data. Both are about the solver's *destination* rather than
its menu, which is the part that matters.

This was not a story we constructed after seeing the numbers. The same pattern was recorded from
the previous run's data before this one started — 13 of its 14 convergences also finished below
0.15 — and a separate note committed to the repository *while this run was still going*, before any
of its numbers were visible, fixed in advance that this is what would decide the unit. This run is
the replication, on an independent 60-attempt arm.

## The one thing it did find

Nine convergences, but not nine orbits: they collapse to **five distinct solutions**. Four of those
five were already found by the previous run. One was not:

**Period 20.418, shift 0.587.** New. And it is the only solution either run has produced **inside
the published band** — the one in-band convergence that didn't run away.

So the stratification bought exactly one orbit that a globally-ranked budget had not reached, for
about 57 core-hours. That is a narrow, real, unglamorous result, and it should be read narrowly: it
is not one of the eight named orbits, the count against those is still zero, and the gate about
them remains **under-resourced** rather than answered. Nothing here reopens it.

It also says something uncomfortable about the method. Four of five re-finds, *across* runs, not
just within one — Newton spends most of a fresh hundred-attempt budget rediscovering what the last
hundred already found. The obvious next move is deflation: subtract the known solutions from the
problem so the search cannot land on them again.

## Two smaller things worth writing down

**A number that looks like a bug and isn't.** The deeper mine's best candidate scores *worse* than
the shallow one's — 0.0685 against 0.0165. That reads like a regression until you look: all 81 of
the old pool's better-scoring candidates have periods between 1.75 and 2.5, i.e. they are trivial
short-time near-repeats that no published orbit is anywhere near. The new rule requires candidates
to be anchored to a real target period, so it never had them. Every one of the old pool's *anchored*
admissible candidates is inside the new one.

**An option got priced, and the price was informative.** One tempting next step is to let the
solver handle candidates with a discrete vertical shift instead of discarding them — and it would
unlock a lot, 334 of the 575 in-window candidates, 58% of the pool. But of those 334, exactly
**one** sits in the published shift band. So it is not a fix for the band problem, whatever else it
is. That is the kind of thing worth measuring before spending ten hours on it.

## What this doesn't say

It doesn't say the eight published orbits aren't there. A hundred attempts is not the scale that
question is posed at, and a silence at the wrong scale means nothing.

It doesn't say the solver is broken. Three planted controls fired exactly as designed — a positive
that had to converge and did, a negative that had to fail and did, a conditional positive that had
to converge and did. A null from an instrument with a dead control would be uninterpretable; this
one isn't.

And it moves nothing toward the Millennium problem this repository is aimed at. Those odds stay
where they were, around 0.05%. What changed is smaller and duller: an instrument that was pointed
wrong has been pointed correctly, and now reports that the thing we were blaming was not the only
thing wrong.

---

*Produced and checked in a single session with no independent reviewer, and therefore labelled
UNVERIFIED under this project's own rules. Verification is a fresh pair of eyes or it is not
verification.*
