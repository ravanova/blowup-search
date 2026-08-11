# The index that stops us rebuilding what we already built — audited a second time

*Leg 292, Route-CAPA. Companion: `TECHNICAL_P2_ROUTECAPA_V2.md`.
Figure: `writeup/figures/fig67_route_capa_v2_audit.png`.*

---

## Why this file exists at all

Some months ago this project came within about ten minutes of rebuilding, from scratch,
a numerical integrator that was already sitting in the repository — working, and
validated to four parts in ten thousand trillion. It was eventually found, but not by
looking it up: it was found by grepping for the number of the paper it implemented.

Which is a slightly humiliating way to find your own code.

The fix was a file called `capabilities.py`: a machine-readable index with one row per
solver module, each row saying what mathematical object it handles, what it computes,
**the strongest known-answer test it passes and by what margin**, and which test file
re-checks all of that. There is a standing rule with no expiry date — *do not build a
solver without grepping this file first* — and there is an automated check that fails
the build if the file drifts out of step with the code.

Here is the problem with that automated check, and it is the whole reason this leg
exists. It verifies three things: that each row names a test, that the named test file
**exists on disk**, and that the "validated" text is longer than twenty characters.

That's it. It never runs the test. It never asks whether the test has anything to do
with the module pointing at it.

Someone noticed this ~220 legs ago and audited the file by hand. This leg is the second
such audit.

## Five questions, five counts

Rather than ask "is the file fine?" — a question that can only be answered yes by
someone who wants the answer to be yes — the audit asks five separate, countable
questions.

**1. Is every module in the index?** Both directions: modules on disk with no row, and
rows naming modules that no longer exist.

**Answer: 48 rows, 48 distinct modules, 48 files on disk. Zero missing. Zero ghosts.**

This one was predicted, in writing, before it was measured — and the prediction is the
interesting part. The project's working convention is that a leg adding a module appends
its own index row *on the same commit*. If that convention holds, completeness isn't
something that decays over 220 legs; it's self-maintaining, because there's no moment at
which a module exists without its row. The audit confirms it: the index grew from 42
rows to 48 with no completeness defect at all.

**2. Do the named test files exist?** Yes — 46 distinct test files, all present. This is
the one thing the automated check genuinely enforces, so a failure here would have meant
a bug in the checker rather than rot in the index.

**3. Do those tests actually pass, today?** This is the check the automated detector
cannot do, and the reason it can't is cost: all 46 test files were executed, and the
cumulative bill runs to hours. See below.

**4. Does each row actually state a magnitude?** The file's own contract says the
"validated" field should give the strongest known-answer test *with the number*, or say
"no known-answer gate" plainly. **33 of 48 rows give a number; 3 say plainly that they
have no gate; 12 claim validation in words without a number.**

The honest way to report that is a rate — **75% of rows meet the contract in the
letter** — and to name the 12, not to quietly rewrite them. Read one at a time most of
the 12 are candid in words rather than digits ("explicitly NOT a proof — float64
throughout"; "no independent published known answer"). Inventing magnitudes for someone
else's module, from an audit chair, would be manufacturing precisely the kind of claim
this field exists to restrain. There's also a pattern worth noticing: nearly all 12 are
the oldest and most auxiliary modules. Everything registered in the last ~180 legs
carries numbers, usually several, plus an explicit statement of what it does *not*
establish. The convention tightened; the 12 are sediment.

**5. Does each cited test actually load the module citing it?**

This is the new one, and it's where the audit earned its keep.

## The pointer that couldn't fail

The first-generation audit did check this, and I initially wrote that it hadn't. Its own
saved data proves otherwise: it recorded, row by row, whether the cited test actually
loads the module, and it flagged **the same single row this leg flags**. So the story is
not "nobody looked". It is stranger and more useful than that.

The first audit couldn't fix what it found. At that time, no test anywhere in the
repository loaded that module — there was nothing to repoint the row at. So the finding
was written down, correctly, and left open.

**One row out of 48 fails,** still. The index's single *superseded* module — kept around only
so its name resolves to a warning rather than to nothing — pointed at a test file
containing zero occurrences of its name. Not a weak test. Not a partial test. A test
that literally cannot fail if that module breaks, sitting behind a row that reads as
though it were covered.

And here's the part that makes it a genuine finding rather than a typo: the *right* test
now exists, and has for a long time. A 22-kilobyte adversarial test file, written 53 legs
after the first audit, which opens by importing exactly that module — and which the index
cited nowhere at all. Run on its own, it passes; and one of its checks verifies the
precise sentence the index row claims, that the module has zero importers and its
DO-NOT-USE banner is intact.

So the gap that mattered wasn't the broken pointer. It was the roughly 220 legs during
which the fix sat on disk, unnoticed, because the check that would have noticed had been
run once instead of left running.

So the fix isn't "point it at some test that mentions the module". It's "point it at the
test that re-checks the claim the row is making". One field corrected, with a comment
recording why. The claim text itself is left untouched — this leg corrects pointers, it
doesn't reword other people's results.

Why did it rot *there*, of all places? Because that's the mechanism, not a coincidence.
Every instance of this defect the two audits have found — the one repaired last time, the
one repaired now — sits on a module nobody imports any more. A row whose module nobody
uses is a row nobody re-reads, so its pointer is the one most free to go quietly wrong.

## The fix broke the test, which is the best thing that happened here

Re-running the sweep after making the correction, that same adversarial test came back
**red** — the very test the correction was justified by. Re-run alone, under no load: red
again, so not a flake.

The cause turned out to be the comment I had just written next to the row. That test
proves nobody imports the superseded module by scanning every Python file in the tree for
a line mentioning both the module's name and the word "import". My comment *explaining
that a test imports the module* is, to a substring scan, indistinguishable from a file
importing it. Three lines of documentation registered as three new importers.

Reworded, it's green again — 33 seconds. The point isn't the embarrassment. It's that an
error introduced *by the audit itself* was caught by the audit's own sweep, in the same
run, instead of being shipped as a green-looking claim. That's the entire argument for
making these checks executable rather than written down, demonstrated at my own expense.

## Controls, because a check that can't fail isn't a check

Three of the rows make an arithmetic claim you can actually falsify: they say a test
file contains a specific number of checks — 17, 14, 10. The audit counts them.
**All three agree exactly.** That control had a real way to fail — anyone adding a check
without updating the row — and it didn't fire. That's worth as much as the defect that
did.

The relevance scanner got a control too. One row cites a test named after a *completely
different* module, which a naive filename-matcher would flag as broken. Hand-checked: it
genuinely does import the module in question, deep inside the file. The scanner clears
it. Which means it's reading code, not matching names — and had it been matching names,
it would have got both this row and the broken one exactly backwards.

## What this doesn't do

It doesn't move the mathematics an inch. No constant banked, no bound computed, no part
of the main problem closer than it was this morning. The odds on the big prize are
unmoved at about 0.05%, and it would be dishonest to imply otherwise.

What it does is keep a standing prohibition honest. "Don't rebuild anything without
checking the index first" is only as good as the index — and the index is now measured
at 48-of-48 on completeness, 47-of-48 on whether its tests are even pointed at the right
code, with the numbers, the runner and the failing case all written down.

The most durable output isn't the one defect. It's that the relevance check now ships as
code in the runner instead of as a sentence in a report. There's a banked lesson here
that keeps proving itself: *a check that isn't executable decays at the rate of memory.*
The first audit wrote that gap down. This one closed it, and left something behind that
can find the next instance without anyone remembering to look.
