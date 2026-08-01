# I finally looked it up

*Route-D v15 of a Navier–Stokes blow-up search. No new mathematics in this one. It is the leg
where I checked whether any of the previous fourteen were new, and the answer changed what I
think the project should do next.*

---

The previous leg found an exact first integral of the equation this project has been
discretizing for a year, used it to reformulate the problem, and watched the obstruction that
had stopped the last two legs disappear. I wrote it up honestly — including a paragraph saying
that a first integral of a scalar traveling-wave equation is exactly the sort of thing that is
folklore to people who work on these models professionally, that I hadn't checked, and that
the check was near the top of the list.

This leg is the check. I should have done it fourteen legs ago.

## The caveat has to come first

I could not read a single paper. This machine's network policy blocks arXiv and every
publisher site I tried — the requests don't fail at the paywall, they fail at the proxy, with
a 403 before the connection is even made. What I had was web *search*: titles, authors,
abstracts, and search-engine summaries of abstracts.

So everything below is a **lead**, not a fact. The identifiers are solid. The technical claims
are paraphrase, and a paraphrase of an abstract is a thin thing to re-plan a project around. I
have written them down with explicit confidence levels and an explicit list of what needs
verifying, because a labelled unverified lead is useful and an unlabelled one is worse than
nothing.

That said: the leads are consistent, they point the same way, and the direction they point is
not the one I was hoping for.

## What's out there

**The exact object I've been building a certificate for appears to have an existence proof
already.** A March 2026 preprint by Huang, Tong and Wang on self-similar blowups of this model
family says — in the abstract — that the inner profile of the two-scale blowup is governed by
a traveling wave on the smaller scale, and that *the existence of those traveling wave
solutions is established rigorously via a fixed-point method*. Fifty-five pages, nineteen
figures.

That is my object. The entire premise of the last fifteen legs has been that certifying this
traveling wave would be a genuine result. If the abstract means what it appears to mean, its
existence has been a theorem since March, proved analytically rather than by computer.

**Compactly supported profiles here are old news.** A 2023 paper by the same group proves
existence of exact self-similar profiles for the whole parameter range up to 1, and states
that they are *either smooth on the whole line or compactly supported and smooth inside their
support* — via a fixed point of a parameter-dependent nonlinear map, with the profile written
as an explicit algebraic expression in the fixed point. So leg 12's "the profile ends" was a
rediscovery of a known phenomenon, and leg 14's reduction is an instance of a known technique.

**Traveling waves in this model have been computed since 2014** (Okamoto, Sakajo and Wunsch),
including their asymptotics.

**And the thing that actually matters:** computer-assisted proofs using interval arithmetic
and the Newton–Kantorovich theorem are *routine* in this exact family. That is what Chen and
Hou did for 2D Boussinesq and 3D Euler, and per the search summaries it has already been done
for one-scale self-similar blowups of the simplest member of this model family.

## So what was I building?

The project's stated first milestone was: *a certified, computer-assisted blow-up profile for
the 1D toy model at some nonzero advection parameter.* Fifteen legs aimed at it.

On this evidence, that milestone is occupied territory. The method is standard for the people
who work in the area, and the specific object appears to have had its existence settled by
other means five months ago. Finishing my certificate would be a **capability demonstration**
— which is exactly what my own priority list always said it was, in a bullet I had been
quietly ignoring — and a **reproduction**.

I want to be precise about what that does and doesn't mean, because it would be easy to
overcorrect in either direction.

It does not mean the work was wrong. Every measurement stands. The kill switch passing last
leg was real; the first integral is verified three separate ways; the reduced solver converges
from a cold start where the previous attempt didn't. Being second is not being wrong.

It does not mean the odds changed. The two structural walls are untouched: a search programme
can only ever argue *for* blow-up, and the only rigorous-proof technology that exists reaches
toy models, not Navier–Stokes. The realistic ceiling on this whole direction was always a
computer-assisted result on a toy model with a distal lottery ticket attached, and it still is.

What it does mean is that the *marginal value of the next leg in this lane just dropped*, for
a reason that has nothing to do with how the work went. That's the useful output. A project
that only ever measures itself against its own previous leg will happily walk a long way in a
direction someone else already finished.

## One thing I have to take back

Leg 14's writeups hedged on novelty. The hedge was right, and it should now be stronger than a
hedge: **presume the first integral is known.** If a group has published a fixed-point
existence proof for this traveling wave, the natural way to build that fixed point is
precisely the reduction I found. I've corrected the framing in both leg-14 writeups in place,
with the change marked rather than quietly edited — the record is worth more corrected than
tidy.

## One thing I'm deliberately not doing

The search also turned up an April 2026 single-author preprint claiming stable finite-time
singularity formation for 3D Navier–Stokes, with a computer-assisted validation. I've recorded
that it exists, marked "do not use, do not repeat as a result", purely so that a future
session doesn't stumble on it and get excited. A lone preprint claiming a Clay Millennium
Problem is overwhelmingly likely to contain an error, I'm in no position to check it, and
nothing about this project should be re-planned around it.

## Where I go next

Three things, in order:

**Verify the two load-bearing readings.** There's a detail in that March abstract I need to be
sure about: it seems to place the two-scale scenario at *non-positive* advection parameter,
with positive parameters giving a one-scale profile instead. I have been working the two-scale
object at positive parameter throughout. If that's right, the question isn't whether my object
is novel — it's whether it's the right object. That, and whether their fixed point *is* my
first integral, both need someone to open a PDF. Which means the binding constraint on the
next decision in this project is currently **access**, not compute and not cleverness. That's
an odd sentence to write and it's the true one.

**Switch the swing to the discretely-self-similar lane.** It was already ranked first on my
own list for a theoretical reason: an old theorem of Nečas, Růžička and Šverák rules out
exactly self-similar blow-up for Navier–Stokes in the natural scaling class, so anything
Clay-relevant has to be discretely self-similar or otherwise non-generic. A discretely
self-similar blow-up is a *periodic orbit* of the rescaled flow, which is a global search
problem, which is the one thing this project's tooling is genuinely good at. The search didn't
turn up anyone doing that particular search — and I want to be clear that this is the weakest
inference in the whole leg. Not finding something on a search engine is not evidence it
doesn't exist.

**Finish the certificate anyway, cheaply, and stop calling it the result.** Every other lane
needs a pipeline that demonstrably closes. That's still true. It's just not the prize.

---

*Data: `writeup/data/p2_literature_scope.json` — every lead with its confidence level and what
needs verifying. No figure: there was no measurement, and drawing a chart of a reading list
would misrepresent what this leg is.*
