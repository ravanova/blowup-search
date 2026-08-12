# The search was looking in the wrong place, and the search was right to (PROG-R4, unit U2)

There is a class of bug that never throws, never fails a test, and never produces a wrong number.
It produces a *correct* number about the wrong population. This is one of those, and it is worth
writing down because it is not specific to fluid dynamics — any pipeline that ranks candidates
globally and then filters them by a property the ranking doesn't know about will hit it.

## The setup

The programme is trying to recover published relative periodic orbits of 2-D Kolmogorov flow at
`Re = 60`. Lucas & Kerswell 2015 list eight of them by name, with periods between `T = 14.776`
and `T = 19.334`. The standard method, which is theirs and Chandler & Kerswell's before them, has
three steps:

1. run a long turbulent simulation;
2. find moments where the flow nearly repeats itself — *near-recurrences* — and record the time
   `t` and the interval `T` at which it nearly repeated;
3. hand each of those `(t, T)` guesses to Newton's method and see whether it converges onto an
   exact orbit.

Step 2 produces far more candidates than step 3 can afford, so you rank them by how close the
near-repeat was and take the best few hundred. That is the obvious thing to do and it is what
everyone does.

## What came out

The simulation ran to `T = 1e5` — 400,000 snapshots, 3.44 hours. The recurrence scan looked at
**95,542,640** pairs of times and found **913,301** genuine local minima of the recurrence
measure. Plenty. The best one scored `R = 0.016543`, an order of magnitude better than the best
this repo had ever found before (`0.177`, from a run 50× shorter). Everything looked healthy.

Then the top 400 were passed forward, and by the time they reached Newton's method there was
**one** usable seed left.

Here is the funnel:

| stage | count |
|---|---|
| candidates passed forward | 400 |
| of those, close enough for Newton | 260 |
| of those, in the shift class the solver can represent | 102 |
| of those, near a *named published period* | **1** |

The plan called for ~100 attempts. There was one.

## Why

Nothing was broken. The ranking did exactly what it was asked to do.

Near-recurrences at short intervals are easy. If you compare the flow to itself `1.5` time units
later, it has barely had time to go anywhere, so the difference is small and the candidate scores
well. If you compare it `19` time units later — long enough for the chaos to do real work — the
difference is much larger, and the candidate scores badly *even when it is a genuine near-miss of
a real orbit*.

There are also vastly more short intervals available than long ones.

So a global top-400 fills itself with `T = 1.25` to `T = 2.5` candidates. They are real
near-recurrences. They score well *because* they are short. And every orbit anyone has ever
published for this flow lives at `T ≈ 15` to `19`, which is exactly where the ranking is least
willing to look.

The ranking was not wrong. It was answering "which pairs of times are most similar?" — and the
honest answer to that question is dominated by pairs of times that are close together. The
question that was actually needed was "which pairs of times are most similar *given how far apart
they are*?" Those are different questions, and the pipeline was quietly asking the first one.

## The fix, and the part that needs saying out loud

Spend the candidate budget *per named period* instead of globally. Keep the whole global list —
remove nothing — and additionally take the best few hundred local minima within `±1.0` of each
published period. Everything added faces exactly the same tests as everything else.

| | global only | stratified (80/band) | stratified (500/band) |
|---|---|---|---|
| candidates | 400 | 634 | 2014 |
| close enough for Newton | 260 | 333 | 579 |
| representable shift class | 102 | 131 | 234 |
| near a named period | **1** | **30** | **133** |

One to 133.

Now the part that needs saying out loud: **this change was made after seeing that the first
attempt produced one seed.** That is a researcher degree of freedom, and pretending otherwise
would be the actual dishonesty here. It went into the pre-registration as a labelled amendment
that says so in its first sentence.

Two things make it defensible rather than merely disclosed.

**It cannot manufacture the answer we want.** The gate this feeds asks whether at least one
*named published* orbit converges to a residual of `1e-8`, with the converged period and shift
then matched back against the published values to within `0.05`. Offering more starting guesses
does not relax any of that. A bad guess simply fails to converge and is recorded as a failed
attempt. The change alters which seeds are *offered*; it cannot alter what counts as a recovery.

**The knob was closed, not left open.** The rule written down says the per-band budget is raised
once, in a single step, and if the pool still came up short the run would proceed on whatever it
had and report the shortfall as a number. Otherwise "raise it until we get 100" becomes "raise it
until we get the result", and those look identical from the outside once the run is over.

## The other filter, which is not a bug at all

One row of that funnel deserves its own note: 345 perfectly good candidates were dropped because
they involve a *discrete* shift in the cross-stream direction, and this programme's Newton solver
carries only a continuous streamwise shift. Such a candidate cannot be **expressed** as a starting
guess for it.

That is not a defect to be fixed in passing. It is a limit of the specific implementation, and the
repo has a rule for exactly this (lesson 91: a negative result must name the implementation it was
obtained in). It happens to cost nothing here — all eight published orbits have zero cross-stream
shift, so nothing named is lost — but if this search comes up empty, "we did not find them" would
have to be stated as "we did not find them *with a solver that cannot represent one of the two
shift classes*". Those are very different sentences, and only one of them is true.

## What this does not say

It does not say any orbit was found. That is a separate gate, running as this is written, and its
answer is not in yet. It does not say the method works — only that it is now pointed at the right
part of the search space. The best candidate residual of `0.016543` is a *starting guess*, not a
converged solution, and the gap between those two numbers is the entire content of the question
that comes next.

And it moves nothing toward the Millennium problem this repo is nominally aimed at. The odds stay
where they were, at about 0.05%. This was a plumbing fix on an instrument, written up because the
failure mode is general and silent: **a global ranking will starve any band your filters care
about, if the ranking doesn't know your filters exist.**

---

*Built and checked in a single session with no independent reviewer, and therefore labelled
UNVERIFIED under this repo's own rules. Verification is a fresh pair of eyes or it is not
verification.*
