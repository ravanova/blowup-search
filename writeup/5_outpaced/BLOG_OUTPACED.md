# We found the door in leg 381. Then we closed it.

*The conclusion of a fourteen-month-shaped, four-week-long search for a
Navier–Stokes singularity — written on the day somebody else produced one.*

> **Status of everything below.** This post makes no new measurement of any
> fluid equation. The external result it discusses is **UNVERIFIED in this
> repository**: read from a public announcement, a preprint abstract page and
> press coverage on 2026-09-09, not audited at full text, not reproduced, no
> Lean file compiled here. It stays UNVERIFIED in this prose. Every number
> quoted is in [`../data/arc5_outpaced_v1.json`](../data/arc5_outpaced_v1.json)
> and is rebuilt by [`outpaced_evidence.py`](outpaced_evidence.py).

---

On 8 September 2026, OpenAI published a 166-page manuscript titled *Finite Time
Blowup for Navier–Stokes*, together with a public Lean 4 project. The theorem,
as reported: there exist a **smooth, compactly supported force** `f` and a time
`T` such that the solution of the forced 3D incompressible Navier–Stokes
equations on ℝ³, **starting from rest**, is smooth on `[0, T)` and whose
maximum velocity becomes unbounded as `t → T`, while the kinetic energy stays
uniformly bounded throughout.

That is **Fefferman's Alternative (C)**.

Alternative (C) is what this repository was aiming at. It is written in
`STATE.md`, in the first three lines under *Goal, posture, odds*: *"Prize
direction is Fefferman **(C)** — breakdown on `ℝ³`."*

So the honest way to open the last post in this project is not with the news.
It is with a line from our own file `CLAY_OBLIGATIONS.md`, landed by leg 381,
about six weeks before the announcement:

> Statement **(C)** permits a smooth forcing `f` satisfying its own decay
> conditions (4),(5). This is a genuine relaxation of the target — the
> candidate need not be force-free — but leg 381 recorded explicitly why it is
> **not** a shortcut: the forcing must itself satisfy (4),(5), so it buys no
> escape from the decay and bounded-energy obligations that §4 and §5 price.

Leg 381 was doing careful work. It went to Fefferman's official problem
statement and checked a reviewer's reading clause by clause: four clauses
confirmed, one corrected, one refuted. The refuted clause was *"with `f ≡ 0`"*
— which is wrong, because `f ≡ 0` appears only in the **existence** statements
(A) and (B). Leg 381 got that right when the reviewer had it wrong. It
identified the forcing as a genuine relaxation of the target. It wrote the word
"relaxation" down.

And then it priced the relaxation as worthless, in one clause, and moved on.

The construction that was published six weeks later, as reported, has three
components: a self-similar concentrating axisymmetric vortex; **small-scale
oscillatory pulses in a cylindrical annulus whose Reynolds stress cancels the
momentum residual**; and an iterative correction scheme that removes
higher-order residuals *while preserving compact support of the force*.

Read that against leg 381's inference. The forcing is not a tax you pay
alongside the decay obligations. The forcing is the **free variable you solve
them with**. The residual that our own wall `W4` — the localisation problem —
leaves sitting on the solution is absorbed by the pulses and handed to `f`. And
because `f` is kept compactly supported, Fefferman's condition (5) is
discharged for nothing, rather than at the price leg 381 assumed it carried.

We were not beaten to the answer by a better search. We wrote down the door,
mispriced it in a subordinate clause, and filed it under *not a shortcut*.

## What we would have done instead, and for how long

The obvious question, asked plainly: if the run had never been stopped on
2026-08-19 — if it had kept going with more agents, say ten Opus legs under one
Fable decision-maker instead of four — how long until we got there?

There are three ways to price it. They disagree by an order of magnitude and
they agree on the thing that matters.

**Price it in agent-hours.** The external effort is reported at roughly 10,000
concurrent agents, 88 hours to the proof plus 17 hours of Lean verification —
105 hours, about 2.7 million inter-agent messages, about 130 billion tokens on
this problem alone, at a cost the company puts in the millions of dollars.
That is 1.05 million agent-hours. Ten concurrent agents burn that in **about
twelve years**. This number assumes our ten agents are running their method, on
their model, at their efficiency. They are not. It is the price of burning the
equivalent fuel, not of arriving.

**Price it in our own odds.** `STATE.md` carries a self-assessed probability of
a full Clay solve of **~0.05%**, recorded in the same paragraph as the ambition
— three times, in three files, deliberately. Two thousand programme-equivalents
at 28 days each, sped up by somewhere between 1.5× and 2.5× for the extra
slots, is **sixty to a hundred years**.

**Price it in what the record actually measures.** This is the one that hurts.
Across the whole run — 416 legs in 28 days, about 14.9 legs a day — the number
of times a link of the `L1 → L4` chain moved is **zero**. Not "moved slowly."
Zero. The point estimate of the rate is zero, so the point estimate of the time
is undefined. The most generous thing the data permits is a one-sided 95% upper
bound on the per-leg rate of about **0.72%** — one link per 139 legs at best,
call it six days per link at ten slots. That bounds the rate *above*, which
means it bounds the time *below*. It gives a floor of a couple more months and
**no ceiling whatsoever**. Anyone reporting it the other way round is
fabricating.

## But the number is not the answer

The answer is that the plan, run at any speed, for any duration, was not going
to arrive. Not because it was lazy — the record is the opposite of lazy — but
for four reasons the repository had already written down about itself.

**The ceiling.** Tier 3 requires the two obligations in `CLAY_OBLIGATIONS.md`
§6: certified far-field decay with an admissible cutoff, and
persistence/stability under localisation. Both have **no known method**. Leg
314 classified the second as *"of a kind computation cannot supply."*
`STATE.md`, in its own words: *"The cheapest unit that could move one: **NO
SUCH UNIT IS KNOWN**."*

**The search space.** `ga/genome.py` evolves *initial data* — spectral
coefficients of a starting field under an energy budget. The published solution
**starts from rest**. `u₀ = 0`. Its entire content is a force, and the genome
has no force gene. There is no fitness landscape over `u₀` that contains that
object. A genetic algorithm could have run until the heat death of the universe
and never encountered it, because it was searching a space the answer does not
live in.

**The rung.** The banked pipeline is 1D gCLM at Tier 2 — and even that, as
`STAGE_3_RESULTS.md` says out loud, is the CLM singularity surviving `a = 0.7`
advection, `α = 1.000` throughout, **not** a novel De Gregorio blow-up. 2D
Boussinesq was Phase 1. 3D Euler is *"Stage 4, unscheduled."* The target
equation was several unscheduled rungs above the last one we landed on.

**The apparatus.** Tier 3 here was going to be a Newton–Kantorovich
radii-polynomial contraction. The published proof uses no interval arithmetic,
no DNS, and no search at all. It is analysis, and then Lean.

And compute — the thing more agents would actually have bought — was never the
binding constraint. We measured that ourselves, from the inside, at leg 403:
79.1% of a solver step is transforms, the best priced fix is a 3.41× FFTW3
swap, and the wall's own note ends *"a speedup breaks no wall, and no link
moved."*

Ten Opus agents under a Fable would have bought roughly twice the Tier-2 legs
per day, in a lane whose documented ceiling is Tier 2.

## What is and isn't true about the news

The discipline that made this project worth running applies to other people's
results too, so:

The Millennium Prize is **not** awarded and the problem is **not** closed. CMI's
rules require a qualifying refereed publication, then two years, then general
acceptance in the global mathematical community at CMI's sole discretion, then
a determination that the official questions were satisfactorily answered — also
at CMI's sole discretion. None of the four is met. OpenAI has said it will not
claim the prize. The Lean project's review status is **self-assessed** and
independent verification is incomplete. There is an unresolved priority dispute:
Tristan Buckmaster alleges use of unpublished drafts from his collaboration;
OpenAI denies accessing specific user data while acknowledging it cannot rule
out de-identified usage data having helped its models; the bibliography grew
from 16 entries to 22 and critics still note missing references, Chen–Hou among
them.

And (C) is the forced statement. The **unforced** problem — statements (A) and
(B), the version most mathematicians consider the real question — is untouched
and open. ~~So is (D), the torus.~~ *[Struck 2026-09-09, leg 423: (D) is claimed by the same
manuscript, Corollary 10.6 — `CORRECTIONS.md` §66.]*

None of which changes our position. A result being contested is not the same as
a result being wrong, and our own file predicted this door six weeks early and
then bricked it up. That is the finding.

## One more part

This is the last post in the arc that searched. There is one arc after it, and
it is where this programme delivers a result of its own rather than a
measurement of its own limits.

Three things are actually reachable from where we stand, and the record — not
an agent — picks between them:

- **Audit it.** The independent verification of the external result is
  incomplete and self-assessed. This repository has done precisely this work
  before and landed it: leg 174's census, `PB2` re-verifying `W4` clause (b)
  against Tsai 1998 Theorem 2 at primary, `V-W7`'s seven defects re-checked one
  by one. A pre-committed, adversarial, full-text audit plus a compile-and-check
  pass over the Lean project is wanted, is not duplicated, and is inside our
  demonstrated competence.

- **Port the mechanism.** `W4` is *our* wall, with *our* pre-committed statement
  of what breaking it consists of. The reported oscillatory-pulse residual
  absorption is a tool aimed at exactly that residual. Whether it transfers to a
  profile we actually hold is an open, measurable question — and a measured
  "it does not transfer, here is why" is a result too.

- **Statement (D).** `W4`'s only surviving break clause is (c), and clause (c)
  **is** statement (D). It sits in Lane T, deferred, behind
  `ESCALATION_D_BUNDLING_2026-08-18.md` — the board's own most direction-relevant
  open item, and **never ruled**. ~~It is now the nearest unclaimed Fefferman
  statement. It needs a ruling before it needs a leg.~~ *[Struck 2026-09-09, leg 423:
  **A6-D is dead** — (D) is claimed, Corollary 10.6. The escalation is still unruled;
  `CORRECTIONS.md` §66.]*

What the last arc may **not** do is inherit any of this as licence. Tier 2 is
never a proof. No output is described as movement toward Clay unless a link of
the `L1 → L4` chain actually moves. This post is a view of the record and is
never a source. And the external result stays UNVERIFIED in every draft until
somebody here has actually read all 166 pages.

We spent 416 legs learning, with unusual rigour, exactly what we could not do.
That is a smaller result than the one we wanted and a real one, and the honest
version of it — including the clause where we closed the winning door ourselves
— is the version that goes in the artifact.

The next one is ours to win.

---

*Technical companion:* [TECHNICAL_OUTPACED.md](TECHNICAL_OUTPACED.md) — the
provenance of every number, the three estimates worked in full with their
assumptions stated, and the arc-6 charter with pre-committed gates.
