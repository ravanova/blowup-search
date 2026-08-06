# We pointed bad input at twelve of our own modules. All twelve lied.

**Route PUB3, leg 223, v1. DRAFT — for the user's review. This leg's landing does not approve it.**

*Companion to [`TECHNICAL_P2_PUB3_V1.md`](TECHNICAL_P2_PUB3_V1.md), which carries every number
and its source. Third of three publication-scoping bundles, after leg 179 and leg 186 — and
unlike either of those, this one contains no mathematics.*

---

## The uncomfortable version first

This project is trying to build computer-assisted proofs. That means every claim it banks rests
on a piece of code being right. The literature has already said the quiet part out loud: *any
computer-assisted proof implicitly carries, as a hypothesis, the statement that the software
encountered no bugs.* It also carries the cautionary tales — a researcher who retracted five
papers from top journals after finding his career-defining results rested on a software bug; a
sign error that reversed an influential economics result used in public policy.

So over one cycle we dispatched twelve legs, each pointing adversarial and degenerate input at
one load-bearing module underneath our own banked results. Each asked the same question:

> *Under bad input, does this module ever silently return a wrong value — rather than reject
> it, or at least fail loudly?*

**Twelve out of twelve said yes.** Several had four to eight separate mechanisms. These were not
modules chosen for looking suspect; they were chosen for being load-bearing.

Before that number gets away from anyone: **it is not a discovery.** That adversarial input
finds silent defects in numerical code is thoroughly established — there are incidence studies
of silent bugs, a 269-bug dataset drawn from NumPy, SciPy and LAPACK, and an entire subfield
(metamorphic testing) built around *why* this code is so hard to test: for most numerical
routines there is no independent ground truth to check against. We rediscovered a known fact
about our own codebase. The technical note says so in its first section.

What we think is worth writing down is the *second* question we asked.

## The question that actually mattered

For every defect, we required the finding leg to answer a separate, pre-committed question:

> *Does this move a number we have already published?*

Not "how bad is this bug." **Does any banked result change.** That is a different question, it
is answered by measurement rather than judgment, and it repeatedly inverted the ranking.

The most spectacular magnitude of the cycle belongs to leg 198: a sign-flip that corrupts one
certificate constant by a factor of **1.19 × 10¹⁷**, big enough to flip a proof's own verdict
from "fails" to "closes." Contamination: **zero**. It needs a negative weight, and no caller in
the repository passes one.

The finding that actually reached a published claim looks like nothing at all. Leg 202 found
that our profile solver, when its first attempt stalls, quietly retries from a different
starting point and accepts the result if the residual is *better*. Spurious grid-scale
solutions satisfy that test better than the real ones do. So the solver reports
`converged = True` at machine-zero residual — the most reassuring diagnostic a numerical
routine can emit — while sitting on a lattice artifact. At one parameter value, three grid
resolutions return three different answers, **376% apart**, all three flagged converged at
machine precision.

And it re-seeds the rest of the sweep from the wrong branch.

That one materially exposes a banked headline (Route-D v11). The technical note states it as
**MATERIALLY EXPOSED** everywhere it appears and never groups it with the latent ones.

**The pattern behind the inversion:** every harmless defect needed an input nobody produces — a
negative weight, an infinite exponent, a subnormal number, a lopsided grid. The dangerous one
needed nothing. It fires on the default path, on a normal warm start, at a parameter we
genuinely sweep. **Reachability, not magnitude, predicts contamination.** It is cheap to
measure, and we measured it in eleven of twelve cases.

The twelfth is the one we are least sure about, and it stays marked uncertain.

## The scoreboard, both halves

Thirteen escalations. Graded:

- **1** materially exposes a banked claim (202)
- **1** claim-adjacent, no number confirmed wrong (203)
- **1** contamination never measured — status *uncertain*, not zero (205)
- **9** zero banked numbers affected, per the finding leg's own measurement
- **1** not a contamination question at all — a pending decision (188)

Reporting either half alone would be dishonest. "Twelve of twelve modules have silent-wrong
paths" without the grading is alarmism. "Only one of thirteen touched a published number"
without the defect rate is complacency. The grading is the whole point, and it only means
anything because it was pre-committed — each leg wrote down what would count as contamination
before it looked.

One caveat we are keeping in front, not in a footnote: **not one repair has landed yet.** Every
"zero" above is the finding leg's own measurement, re-confirmed independently by nobody. That
is weaker than "confirmed zero," and we do not use that phrase.

## The best thing the discipline did

It kept us from three overreactions and one convenient story.

Leg 209 found a bug in the module our own no-go theorem is proved against — an unordered NaN
comparison that flips the theorem's conclusion to its opposite. Alarming, and it would have
been easy to write it up that way. Instead the leg established that the theorem rests on an
exact inequality and an analytic estimate that **never touch that code path**. The proof is
fine. The module has a gap. Two different statements, kept apart.

Leg 208 found a guard accepting nine of nine forbidden inputs, five with a *negative* certified
radius. The obvious fear was that it invalidated a screening result we lean on — so the leg
checked, rather than assumed, and found that screening runs on a disjoint branch the defect
never reaches.

Leg 199 found a genuine silent accept whose actual magnitude is **one unit in the last place**.
It reported it at that size and said plainly it is unreachable from ordinary floating point.
Nobody inflated it.

And leg 202 — the one leg with a genuinely dramatic result, the one that could have padded it —
recorded a correction against its *own* earlier notes in the artifact instead of quietly
dropping it, and threw out the list of affected consumers it had been handed, because `grep`
showed none of them even imports the module. It then found the real ones itself, and one of
those (Route-D v12) appears in **no** shared ledger, only in that leg's own journal.

## The bit that stings

We commissioned this note believing there were **seven** escalations. There are **thirteen**.

The reason is not that anyone was sloppy. Every escalation was recorded correctly, each in at
least two places, by legs and an orchestrator working exactly to spec. The problem is that
there is no single committed place where they are recorded *together*.

Our documentation points readers, twenty-six separate times, at a file called `PROGRESS.md` for
the list of things needing human attention. **That file is not in the repository** — it is
excluded by `.gitignore` on purpose, rewritten each cycle, with a committed snapshot elsewhere.
That snapshot was last refreshed when the count was **three**. It still says three. The true
figure is thirteen, and the ten it is missing include the one item that materially exposes a
published headline.

To reconstruct the real list you must read a narrative log and a journal in commit order and
take the union. That is what this leg did. That is why the number moved by six.

There is a joke here and it is on us. We spent a cycle asking twelve modules what they do when
handed input nobody expected, and found that all twelve return a confident wrong answer. Then
we asked the same question of our own bookkeeping, and it confidently returned **3** when the
answer was **13**.

Same failure mode. No exception raised. The number just looked plausible.

## What has not moved

Nothing. Not a single link of the chain this project is actually trying to climb — not in this
cycle, not in 223 legs. The odds on the hard problem stay where they were, around **0.05%**.
Repairing a module restores a guarantee; it never improves a margin.

And the one genuinely open question is not a bookkeeping one. **Does Route-D v11's headline
survive once the solver stops trusting a convergence flag that its own caller's data already
contradicted?** The information needed to reject those profiles was sitting in that experiment's
own output the whole time — a diagnostic that blew up from 0.50 to 4,788 to 73,372 exactly
where the branch jump happens. It just never reached the module's verdict, because it lived in
the experiment and not in the solver.

Nobody knows the answer yet. The leg that would find out is ranked first in the entire backlog,
and it has not been dispatched.
