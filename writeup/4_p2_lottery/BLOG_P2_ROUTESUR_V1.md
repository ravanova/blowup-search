# The bug that only appears if you pick a round number

*Route-SUR v1 — leg 129. Technical companion: [TECHNICAL_P2_ROUTESUR_V1.md](TECHNICAL_P2_ROUTESUR_V1.md).
Figure: `writeup/figures/fig61_route_sur_v1_repair.png`.*

Every spectral fluid code in the world has a line that throws away the top third of its Fourier
modes. It is there because multiplying two fields together creates frequencies too high for the
grid to represent, and those frequencies do not politely vanish — they fold back down and
masquerade as low frequencies. Throw away the top third first, and the folded-back garbage
lands in the part you already threw away. That is Orszag's 2/3 rule, it is about fifty years
old, and it is four lines of code.

Ours had one character wrong.

```python
return wavenumbers(n) <= n / 3.0      # keep every mode up to n/3
```

The correct condition keeps every mode *strictly below* `n/3`. Here is the thing that makes
this a nice bug rather than an embarrassing one: for almost every grid size, those two
statements are identical. If `n` is 64, then `n/3` is 21.33, the largest whole-numbered mode
below it is 21, and `<=` and `<` pick the same one. The two versions only ever disagree when 3
divides `n` exactly — when `n` is 96, or 48, or 81 — because only then is `n/3` a whole number
that a mode can actually sit on.

And no grid size this repository has ever run is divisible by three. They are all powers of
two: 64, 256, 512, 1024, and so on up to 8192. No power of two is divisible by three. So the
bug had been sitting in the shared numerical core that every single simulation imports,
affecting **nothing**, waiting for the first person to type a round number.

## What it would have done

Leg 120 found this and measured what it costs, using an experiment the literature hands you.
Put all the energy on the highest mode you kept. Square the field. Look at that same mode
again. The whole point of dealiasing is that the answer must be exactly zero.

On the grids we use, it was zero to sixteen decimal places. On grids divisible by three, it was
**0.25**. Not a rounding error — a quarter of the signal, spurious, at every single such grid.

That propagates into something we log on every run. There is a function in the module whose
docstring calls it the *"Exact rate dE/dt"*, and the solver uses it as a self-check: compute the
rate of energy change two ways, and if they disagree, the run is under-resolved and its results
are suspect. On a grid divisible by three, that supposedly exact quantity was wrong by **17
percent**. The guard that exists to catch bad runs would itself have been the bad number.

## The part that took the actual work

Fixing it is one character. Being *allowed* to fix it is the leg.

This module is imported by everything. Every banked result in this repository — every
simulation whose numbers we have written into papers and JSON files and quoted in prose — came
out of it. A repair to a shared core is only acceptable if you can show it changes nothing that
already exists. Not "should change nothing". Show it.

So the leg's real deliverable is a measurement: pull the *old* version of the whole solver
directory out of git, run it in a separate Python interpreter, and compare it against the
repaired version quantity by quantity — not "are these numbers close", but are these the same
bytes. Same dtype, same shape, right down to whether a zero is positive or negative.

Across the masks themselves, every public helper function, and — the part that matters — four
complete end-to-end simulations run to convergence and compared on their final fields and every
diagnostic they report:

**0 of 156 quantities moved.**

## Why one row of that table is deliberately red

There is a failure mode in this kind of work that the repository has a standing lesson about:
*a control that cannot come out differently is not a control, and the tell is that its numbers
are identical.* If your before-and-after comparison says "identical" everywhere, you have not
necessarily proved a no-op. You may have proved that your comparison is broken.

So the table carries one row that **must** come out different: the mask at grid sizes divisible
by three, where the repair is supposed to change things. If that row also reported "identical",
the whole measurement is worthless.

The first time I ran it, that is exactly what happened. All zeros, including the control.

It was not a no-op. It was a dead harness — importing the runner quietly put the *repaired*
code ahead of the old code on the import path, so both sides of my careful A/B were the same
module comparing itself to itself. A perfect, meaningless result.

The control caught it. It is now a hard assertion in the runner: if fewer than all 33 control
quantities move, the run aborts with the message *"Every no-op claim in this run is void."*
With the harness fixed, the control moves 33 out of 33 — at `n = 96` the top retained mode drops
from 32 to 31, exactly one mode, exactly as intended — and the 156 banked quantities still do
not move at all. That combination is the licence, and neither number means anything without the
other.

## The rest of the sweep

Leg 120 had found five more defects in the same module, all of the same species: **input that
should have been refused or passed along was silently absorbed instead.** A corrupted
coefficient (a `NaN`, the numerical signal for "something has gone wrong upstream") was being
quietly overwritten with a clean zero, so the caller got a perfectly finite, perfectly wrong
answer with no indication anything had happened. Twelve out of twelve poisoned inputs came back
looking pristine.

The fix there is almost funny in how small it is. The published algorithm says *multiply* that
coefficient by zero. Our code *assigned* zero. On ordinary numbers those are the same thing. On
a `NaN` they are not: `0 × NaN` is `NaN`, so the published version passes the corruption on,
and ours erased it. One is an instruction; the other is an assertion that you know better.

All five are closed, and every one keeps the same property as the main repair: on well-formed
input, the output is bit-for-bit what it always was.

## What this is and isn't

This is housekeeping. No mathematics moved, no result changed, no claim about the actual
research got better or worse. The odds on the hard problem are exactly what they were.

What changed is that a trap has been taken out of the floor. The next person to run this solver
at `n = 96` — because 96 is a perfectly reasonable number to type, which is precisely the
danger — will now get the right answer instead of a plausible wrong one, and the guard that was
supposed to warn them will actually work.

Seven regression checks that used to *pin the bug in place*, so it could not drift unnoticed
before anyone was allowed to fix it, have been turned around. They now fail if it ever comes
back.
