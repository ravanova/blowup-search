# We checked our own scoreboard. Both numbers were right, and the conclusion was still wrong.

*(PROG-R4, units R0 and R1)*

A programme that hunts for periodic orbits in a turbulent flow needs a way to say whether it is
getting better at it. Ours settled on **distinct orbits per core-hour** — deliberately, and
deliberately in advance, because the obvious alternative is worse. "Fraction of attempts that
converge" can be inflated by feeding the solver easy starting guesses, and it happily counts finding
the same orbit twice as two successes.

Then two of the numbers behind that metric stopped agreeing with each other, and this unit was sent
to work out which was right.

The short version: **both were right.** The interesting part is what fell out of checking.

## The first number: how much compute did we spend?

One place said the previous run cost **134.45 core-hours**. Another said **144.69**. A note in the
project's wall file had already declared the second correct and the first a slip of the pen — "a
count derived from prose is not a measurement", which is a rule this repository takes seriously.

Except it wasn't a slip of the pen. Both numbers come out of the same data file:

- **144.69** is how long we *reserved* the machine: 14.47 hours of wall clock with 10 workers going.
- **134.45** is how much CPU the attempts *actually consumed*, added up one attempt at a time.

The 10.24-core-hour gap is idle time at the end of the run, when most workers had finished and a few
stragglers were still grinding. The pool was 92.9% busy. The next run, with a different scheduler,
was 98.2% busy — which is a scheduling difference, not a solver difference.

So the correction that had been written into the wall file was itself slightly wrong: it labelled a
second real measurement as an error. Both numbers stay; they need a label saying which is which.

There is also a caveat neither escapes. That denominator is really **worker-hours**. One run
reserved 10 workers and the other 8, and the machine's actual core count isn't recorded as a number
anywhere in the banked data — only inside an English sentence, which under our own rules doesn't
count. We're reporting that as a missing field rather than guessing at it.

## The second number: how many *distinct* orbits?

Fourteen attempts converged in the baseline run. How many different orbits is that?

The rule is fixed and was not ours to choose: two convergences are the same orbit if their period
and their sideways shift both agree to within 0.05 — the same tolerance we use to decide whether we
have recovered a published orbit, so "distinct" can never be finer than "recovered".

Under that rule: **eight.** Which is what the wall file currently says, so we agree.

We then tried fairly hard to break it, because the rule as implemented is a shortcut — it compares
each new point only against the *first* member of each group, which in general depends on what order
you feed it. On this data it doesn't: three different ways of grouping give eight, and so do twenty
thousand random orderings. Loosen the tolerance and you get eight all the way to 0.10; you need to
triple it, to 0.15, before you get seven.

The count does hang on one narrow call. Two convergences sit 0.064 apart in period — 1.29 times the
tolerance — and nothing else distinguishes them. Tighten the rule by a third and they merge.

And there was a genuine error, just not where anyone was looking. The wall file's reason for
doubting the eight was that "10 of the 14 convergences landed on just three solutions", which leaves
four, which can't produce five more. The real figure is **nine**, not ten — group sizes four, three
and two — leaving five singletons, and 3 + 5 = 8 exactly. The count was never in trouble. The
sentence explaining why it looked like trouble had an off-by-one in it.

## The part nobody asked for

Both headline numbers survived. The conclusion drawn from them did not.

The metric exists to stop us counting a re-find as a win. It does that *within* a run. It does not
do it *between* runs — and we had never checked whether that mattered. It does:

- **57 of the second run's 100 starting guesses were the exact same guesses the first run had
  already tried.** Identical to the last digit.
- **5 of its 9 convergences are bit-for-bit re-runs of attempts the first run had already made** —
  same starting point, same deterministic solver, same answer.
- Of the five distinct orbits the second run reports, **four had already been found by the first
  one.** It contributed **one** orbit that was new to the programme.

So the scoreboard reads two ways, and they point in opposite directions:

| | first run | second run | |
|---|---|---|---|
| distinct orbits per core-hour, per run | 0.0553 | **0.0877** | 1.59× **better** |
| orbits *new to the programme* per core-hour | 0.0553 | **0.0175** | 3.15× **worse** |

The first row is what was reported as "the lane's first measured improvement". It's arithmetically
correct. But the two runs aren't independent samples of anything — more than half the second one is
a replay of the first — and on the reading that tracks what the project actually *gained*, the
second run was the worse deal.

**So we're retracting the conclusion and keeping the arithmetic.** The second run was cheaper. That
is a real and useful thing. It is not evidence that the orbit finder got better, and we'd already
written down, before starting, that retracting this was an allowed outcome. It was the right one.

## And the "cheapest win in the repository"

The second half of this unit was supposed to build an early-stopping rule. Most attempts fail by
running the full 51 iterations while making no progress: 53% of them reduce their error by less than
1% over their final ten iterations. Every one of those iterations is waste, and they are most of the
run.

The rule is embarrassingly simple: if you're past iteration 20 and your error hasn't halved compared
to ten iterations ago, stop. Replayed against the banked record of every attempt, it **recovers 55%
of the run's compute — 74.87 of 134.45 core-hours — while killing none of the 14 attempts that
actually converged.** There's a comfortable safety factor: the threshold sits about 7× away from the
worst behaviour any real convergence ever showed.

There is one wrinkle, and it's the whole finding. **That rule was already built and deployed** by
the previous unit, before this one was commissioned. So the "cheapest competitive win in the
repository" had already been collected, and our job turned into a different question: *is there
anything left in it?*

We swept 12,597 variants of the rule. 9,760 of them kill no real convergence. Ranked by how much
compute they recover without giving up any safety margin, the best one beats the deployed rule by
**0.45 percentage points** — about half a core-hour on a 134-core-hour run.

You can do better if you're willing to be reckless. One variant recovers 65%, but it sits within 9%
of killing a real convergence, and picking the best of 12,597 rules against 23 examples is exactly
how you fool yourself. We also tried fitting the rule on one run and testing it on the other. Fit on
the bigger run, tested on the smaller: clean. Fit on the *smaller* run, tested on the bigger: it
kills an attempt that really did converge.

So the honest summary is that this line of work is finished. The win was real, it's already banked,
and what remains is half a percentage point and a demonstrated way to overfit.

If we do rerun the baseline with the rule in place, we'd expect the same eight orbits for 59.6
core-hours instead of 134.4 — **0.1343 distinct orbits per core-hour, PROJECTED**, against the
measured 0.0595. That is a projection from a replay, not a run, and it is labelled as one
everywhere it appears. We are deliberately *not* claiming the recovered compute would buy more
orbits: the finding above is that 57 core-hours of the last run bought exactly one.

## What this is worth

It's worth being blunt about the ceiling. This unit made the search cheaper to run and its
scoreboard honest. **A best-in-field orbit finder does not move a Clay Millennium problem — it makes
the questions affordable, which is a different and lesser thing.** Our estimate for the Clay
statement stays where it was, around 0.05%.

What we'd defend is the process. A previous session had already written both corrections into the
project's own notes, and the numbers there were right. But they were *transcribed* from the run that
found them, not independently measured — and the only reason we caught the seed overlap, which
reverses the conclusion those numbers supported, is that we went back to the raw records and derived
everything again from scratch.

A correction that comes from the same place as the original isn't a check. That's the actual lesson.

---

*Data: `writeup/data/p2_prog_r4_r0r1_v1.json`. Every number above is rebuilt from it by
`experiments/p2_prog_r4_r0r1_evidence.py` (66/66). Figure: fig108. Technical version:
[TECHNICAL_P2_PROGR4_R0R1.md](TECHNICAL_P2_PROGR4_R0R1.md).*
