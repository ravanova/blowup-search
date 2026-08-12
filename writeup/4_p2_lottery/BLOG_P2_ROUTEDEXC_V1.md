# The number that always answers, and the number that knows when to refuse

*Route-DEXC v1 — leg 382. Figure: fig100. Data: `writeup/data/p2_route_dexc_v1.json`.*

## A confident number for a profile that has no number

Give this repository's screen a profile shaped like `r^(-2) + 0.01·r^(-1)`, and ask it for the
far-field decay exponent. It answers **1.500000**.

That profile does not have a decay exponent. On the window it is asked about, `[10, 1000]`, it
starts out looking like `r^(-2)` and ends up looking like `r^(-1)`; the crossover sits right in
the middle, at `r = 100`. There is no exponent `p` for which the profile is `C·r^(-p)`. The
answer 1.500000 is the least-squares compromise between two different behaviours, and nothing
in the output says so.

That is not a bug in `solver/dssp_screen.py`. Its routine is called
`fitted_far_field_decay_exponent` and it does exactly what the name says: `np.polyfit` of
`log|V|` against `log r` over twelve points. A fit always returns a number. That is what fits
are for.

The trouble is what the number is *for*. `CLAY_OBLIGATIONS.md` §4 spells it out: to cut a
self-similar profile off and get finite-energy data — which the Clay statement requires, and
which this object does not currently have — you need to choose a cutoff radius and bound the
perturbation the cutoff introduces, and **both of those are functions of the decay exponent**.
A compromise slope with no error bar cannot carry that weight. §4 says so in one sentence:
*fitted is not sufficient here.* §6 then lists it as one of two obligations in this programme
with **no known method in this repository**.

Leg 382 built the method. This is what it can and cannot do.

## The idea, which is not clever

Write `t = log r` and `g = log f`. Then "the profile is a power law with exponent `p`" is just
"`g` is the straight line `c − p·t`", where `c = log C` is the amplitude nobody cares about.

Now instead of a best-fit line, enclose the profile. Chop `[10, 1000]` into a thousand cells
and, using the interval arithmetic this repository already has, compute for each cell a
rigorous box that the profile *provably* lies inside across that whole cell — not at sample
points, across the entire cell, so there is no gap for the profile to wiggle through between
samples.

Then ask a different question. Not *which line fits best?* — but ***which lines fit at all?***
Every cell says the line has to pass through its box. Each of those is a linear inequality in
the two unknowns `(c, p)`. Eliminate the amplitude `c` — in two variables that elimination
(Fourier–Motzkin) is exact, no approximation — and what is left is precisely the set of
exponents that are still possible.

Three things can come out:

- **an interval** — no exponent outside these bounds is possible;
- **EMPTY** — *no* exponent is possible, at all. The profile is provably not a power law here;
- **INCAPACITY** — the machinery could not say, and says so.

None of this is new mathematics, and leg 382's novelty pass says so in as many words. What is
new is that this repository can now do it: the pass swept the tree and found that **every
log-log exponent anywhere in it is a least-squares fit**, without exception.

## What it does on things whose answer is known

Four planted profiles with exact exponents — `1`, `2`, `2.5`, `3` (the `2.5` deliberately not
an integer, to catch an instrument that quietly snaps to round numbers). All four exponents
land inside the certified interval, and the intervals are narrow: widths of
`7.4e-15`, `1.6e-14`, `2.0e-14`, `1.6e-14`. That is the floating-point rounding floor. The
certified answer and the fitted answer agree to twelve decimal places, which is exactly what
should happen when the profile really *is* a power law.

Then the mismatches. The two-power blend above: **EMPTY**. A profile with a far cutoff,
`r^(-2)/(1 + (r/300)^4)`: **EMPTY**. A logarithmic correction `r^(-2)·log r`, whose effective
slope only wanders between about 1.57 and 1.86 — subtle enough that a fit would never blink:
**EMPTY**.

The fitted column, on those same three profiles, returns `1.500000`, `2.808892` and `1.768252` —
three confident numbers for three profiles that have no exponent. Panel A of fig100 is just
those two columns side by side.

This mattered enough to be locked down in advance. This repository has been burned before by
an instrument that could not fail (leg 340) and by the temptation to widen a window until
something passes (leg 361), so the window, the planted knowns, the controls and even the
predicted numbers were all written down and committed **before the module existed**. The
commit order is in the git log and can be checked.

## The part that went wrong, which is the interesting part

The pre-registration made a prediction about how the certified interval would widen with
coarser cells. It was **wrong** — the interval turned out to sit at the rounding floor
regardless. Fine; the instrument is better than expected.

The second prediction was wrong in a way that actually matters.

Take an exact `r^(-2)` profile and perturb it by one part in a **trillion**. Ask the
instrument for the exponent. It answers **EMPTY**.

And it is *right*. A profile perturbed at the 1e-12 level is not exactly `C·r^(-p)` for any
`p`, so the set of exponents that fit it exactly really is empty. The pre-registration had
called "the truth stays inside" a soundness requirement whose violation would be a defect. It
was not a defect. It was a mis-statement of what had been defined.

But follow it through: **no numerical profile is ever exactly a power law.** So the instrument
as first specified would answer EMPTY for every real input it would ever be handed. It would
be rigorous and completely useless.

## What it costs to be useful

The fix is the obvious one, and its honesty depends entirely on where the extra number comes
from. Ask for exponents consistent with the profile **to within a stated relative accuracy
`δ`** — where `δ` is not a dial to turn until something passes, but a bound the caller already
owes about their own profile.

With that, the instrument reports (panel B):

> **certified exponent half-width ≈ 0.434 × δ**

Know your profile to a part in a million, get the exponent to about four parts in ten million.
Clean, linear, and it tells a future consumer exactly what accuracy to aim for before running
anything.

And the price is measurable too (panel C). Each mismatch has a **critical tolerance `δ*`** —
the sloppiness at which it stops being caught:

| mismatch | still excluded provided your profile is known to better than |
|---|---|
| far cutoff `r^(-2)/(1+(r/300)^4)` | 335 % — caught essentially always |
| two-power blend `r^(-2) + 0.01 r^(-1)` | **31.6 %** |
| log correction `r^(-2) log r` | **7.0 %** |

An exact power law, by contrast, is never excluded at any tolerance — so the instrument is not
merely fail-happy. It discriminates, and the table says by how much.

## What this does not mean

It would be easy to over-read this, so, plainly:

**There is no profile.** Route 4 has not produced one. This instrument has been validated on
planted analytic knowns and on nothing else. Its first real consumer is a future unit that does
not exist, and this leg claims nothing whatsoever about one.

**§4 is not discharged.** §4 wants three things: the certified exponent, the admissible cutoff
radius, and the size of the perturbation the cutoff introduces. This is the first. The other
two are untouched. **Both of `CLAY_OBLIGATIONS.md` §6's no-method items stay open** — item 1
because only half of it was attempted, item 2 because it was not attempted at all and, per leg
314, is not the kind of thing a computation can supply.

**The fitted column is still there.** Nothing was replaced. `solver/dssp_screen.py` was read
and edited nowhere. The certified column is recorded *alongside* the fitted one, in the same
row of the same JSON, which is the only arrangement in which the comparison in panel A can be
made at all.

And the ceiling has not moved: **Tier 2**, no link of the `L1 → L4` chain touched, Clay odds
unchanged at ~0.05%.

What did change is small and real. An obligation that read "no known method" now has a named
instrument, a test suite, and a measured price list. That is one line of a specification
turning into something you can run.

---

*Technical companion: `TECHNICAL_P2_ROUTEDEXC_V1.md`. Module: `solver/dssp_decay_enclosure.py`.
Tests: `test_dssp_decay_enclosure.py` (12/12). Runner: `experiments/p2_route_dexc_v1.py`.
Novelty pass: `writeup/novelty/leg_382.md`. Pre-registration and results:
`experiments/journal/leg_382.md`.*
