# We went looking for the theorem that would kill our own lane. We didn't find it — and that isn't good news.

*Leg 392 · unit T2 · Lane T · branch `leg/392-t2-periodic-rigidity`*

Two legs ago we learned something uncomfortable about the blow-up search. The Clay problem has two
versions: one on all of space, `ℝ³`, and one on the torus `T³` — space that wraps around, like a
video game where walking off the right edge brings you back on the left. Almost everything we knew
about *where a singularity cannot hide* came from the `ℝ³` literature. Leg 390 checked, row by row,
how much of that carries over to the torus.

**Zero of four.**

Not "mostly" — none. The reason is almost embarrassingly simple. The great rigidity theorems
(Nečas–Růžička–Šverák 1996, Tsai 1998, and their descendants) rule out singularities that are
*self-similar*: the flow near the blow-up looks like the same shape, repeated at ever-smaller
scales, forever. That idea needs zooming. On a torus, you cannot zoom forever — you run out of
torus. The symmetry those theorems live on doesn't exist there. Our own measurement made it
concrete: of 342 Fourier modes that survive one zoom step, **zero** survive two.

So the safety net has a torus-shaped hole in it. The obvious next question is whether somebody
already patched it: **is there a published theorem that excludes a finite-time singularity on the
torus, the way NRS and Tsai do on `ℝ³`?** If yes, our Lane T is probably dead, and we'd want to
know that today rather than after months of work. If no, we need to say precisely what nobody has
proved.

That was this leg's whole job. Search the literature, honestly.

## The reason this is harder than typing a query

A search that finds nothing looks identical to a search that is broken.

We know this because it happened here. Five legs ago, one of our own literature passes reported a
clean zero on an important question. It was fiction. The code was checking for an XML namespace
labelled `1.0`; arXiv serves `1.1`. Every single response was silently discarded. The instrument
was reporting "the field is empty" when what it meant was "I am blindfolded."

So this leg wasn't allowed to trust its own tooling. Before any verdict, five controls had to fire
and be logged:

- A query that **must** return a lot: `"Navier-Stokes"` → **10,759**. Alive.
- A narrower one that must still return plenty: `"Liouville theorem"` → **628**. On topic.
- **A phrase we invented so that it cannot exist** — *"quasiperiodic rigidity of the Zlatohorsky
  enclosure torus"* → **exactly 0**. The endpoint isn't fuzzy-matching and handing back
  near-misses; a zero here is a real zero.
- Two tests that the `AND` operator actually works, since our whole result rests on ANDed queries
  → **29** and **234**. It works.

Five for five. And the namespace that actually answered, recorded from the raw feed on all 32
queries: **`1.1`**. The exact trap from five legs ago, confirmed real, and stepped around.

We added one more control, and it's the one we're proudest of. A live endpoint isn't enough — the
*queries* have to be good enough to find things. So we demanded the query set re-find the three
`ℝ³` rigidity papers **we had already read in earlier legs**. If the searches can't rediscover
papers we know exist, they're in no position to tell us a paper doesn't.

It re-found two of three. The third — Chae–Tsai, which underpins one of the four rows — **it
missed entirely.**

That failure is in the record, in the data file, in the evidence script. It is not smoothed over.
It means one of our four answers is not an answer.

## What we found

32 queries on arXiv, all 32 measured, no throttling, 244 results, 119 distinct papers read at
abstract level.

The direct form of the question — *Liouville/rigidity* AND *Navier–Stokes* AND *torus* — returns
**zero**. In both spellings (the literature writes it both `Navier-Stokes` and `Navier--Stokes`,
and we checked both, because an em-dash convention should not be allowed to decide a research
programme). `"Type I blowup" AND "periodic"`: **zero**. `"three-torus" AND "Navier-Stokes" AND
"regularity"`: **zero**. `"Morrey" AND "torus" AND "Navier-Stokes"`: **zero**.

Five measured zeros, on an instrument whose nonsense control is dead and whose `AND` is
demonstrably alive.

**No torus analogue of the rigidity theorems was located.**

## Why that is not a green light

Here is the part that matters more than the finding, and it was written down *before* the search
ran, precisely so we couldn't reinterpret it afterwards:

> **A controlled zero is not evidence the lane is clear.** Report it as *"not excluded by anything
> located, with the coverage stated"* — never as *"clear"*, and never as progress.

There is a real difference between *"we proved nothing blocks this"* and *"we looked and didn't
see anything."* The first is a result. The second is a description of our eyesight. This leg
produced the second.

And our eyesight had specific limits, all of them stated:

- **The 1996 and 1998 originals predate arXiv.** An arXiv-first search structurally cannot see the
  journals where the `ℝ³` theorems were published — so it cannot see a torus analogue published
  the same way, either.
- **The one database that reaches those venues throttled us**, returning 3 of 8 queries with the
  rest refused by rate limit. Refused is not zero, and it's logged as refused.
- **One battery failed its own control** (the Chae–Tsai miss above).
- We read abstracts, not full texts. Nine queries were truncated at the top 8 hits.

So the honest verdict is not "no." Our orchestration rules have a name for a null from an
under-covered search, and a rule that it must never be dressed up as a finding:
**`UNDER-RESOURCED`, with the coverage stated and a price for the compliant version.** The price is
roughly an hour and a half of work plus one decision from the user — mostly an API key to stop the
throttling, and a forward-citation sweep of the 1996/1998 papers, which is the single most likely
place a torus analogue would be hiding.

That's cheap. It should be bought before Lane T builds anything.

## What we did find, and what it costs the lane

The torus isn't a total blank. There are published theorems guaranteeing that periodic solutions
stay smooth — just not of the shape that would kill us. They all say *"no singularity, **provided**
your initial state satisfies X"*, where X is a smallness or near-two-dimensionality condition.
For example, a 2020 *Nonlinearity* paper proves global smoothness whenever the data is
*"sufficiently close to being two dimensional"* — and notes that on the torus this yields
arbitrarily large smooth-forever data in a critical space. Another, from 1999, covers *thin*
periodic boxes.

We'd pre-committed to taking such theorems seriously if they appeared: a result covering a
*broader* class than self-similar objects would bite our lane directly, and we'd have to say what
class survives. So, saying it: **what survives is any candidate that is genuinely
three-dimensional at the start, not small, not on a squashed thin torus, and singular in the
ordinary sense.** Which is to say — every clause of the located constraint is somewhere a blow-up
candidate would already be standing. The bite is real in shape and thin in substance, and we'd
rather report the size of it than just its outline.

The most useful thing on the torus turned out not to be an exclusion at all. Tao, 2007, reformulates
the whole periodic problem as: does there exist a function `F` bounding the solution's size at
time `T` in terms of its size at time `0`? **A blow-up construction is exactly a refutation of that
`F`.** That is the cleanest available statement of what Lane T is actually trying to do, and it's
on the torus, in the source's own words.

## The finding we didn't expect

The search surfaced, twice, a preprint claiming to *build* a finite-time singularity on `T³`.
Before calling it anything, we grepped our own repository for its ID — a habit installed after an
earlier leg claimed seven papers were new and two of them weren't.

It wasn't new. We had already read it, at full text, at leg 309, and rejected it. And the reason is
the point: its torus object is an `ℝ³` **self-similar** core, wrapped around the torus by periodic
extension. It dies to the very `ℝ³` theorems this leg went looking for the torus version of.

Which flips the picture in a way our own wall notes don't yet say. We recorded that *0 of 4
clearances carry to the torus.* True. But the converse is also true and more useful: **the `ℝ³`
exclusions still reach a torus object built by wrapping an `ℝ³` self-similar core.** The old screen
isn't void on the torus. It's void as a source of *permission* while remaining live as a source of
*kills* — aimed precisely at the cheapest, most tempting way to build a torus target. The one
previous attempt anyone has made died exactly there.

## What nobody has proved

The deliverable of a "no" is a list of what would have to be established from scratch. Three of
the four rows have no torus counterpart in anything we located; the fourth we can't speak to
because its battery failed. But one row is sharper than the others.

A **Type I** condition — the solution blows up no faster than a specific rate — is a statement
about *speed*, not about self-similar shape. It needs no zooming symmetry. **It carries to the
torus intact, as a perfectly meaningful question, and no torus Type-I rigidity theorem exists in
anything we found.** That is the de novo item: the theorem someone would have to prove, and the
one a torus blow-up candidate would have to survive.

Meanwhile, row 1's object is not merely unproved on the torus — it's *vacuous*. There is nothing to
prove a torus NRS about, because the object it constrains cannot exist there.

## One thing we refused to do

The torus version of the Clay problem has two data conditions we have never read, because reading
them properly requires contacting people, and there's a standing instruction not to contact anyone.
We could have quietly worked around it. Instead: **they are unread, they sit on this lane's
critical path, and we're saying so rather than pretending otherwise.**

---

**Bottom line.** No theorem killing Lane T was located, and that is a statement about our search,
not about mathematics. The result is filed as `UNDER-RESOURCED` with a stated price, the lane is
*not* cleared, and the sharpest thing learned is a warning: the only torus blow-up attempt on
record died to the `ℝ³` theorems everyone assumed didn't apply there.

No new capability. No progress on Clay — a literature search doesn't move that in either
direction, and it stays at ~0.05%. No figure this time; there is nothing to plot.

*Everything above is rebuilt from a single banked data file by an evidence script that makes no
network calls and reruns nothing: 41 of 41 checks, including the control that failed.*
