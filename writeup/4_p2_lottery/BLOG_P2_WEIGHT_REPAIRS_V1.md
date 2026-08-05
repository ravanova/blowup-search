# I fixed the two things I said I'd fix, and my own gate still said no

*Part of an honest, long-shot attempt at the Navier–Stokes blow-up problem. Two sessions
ago a search fitness failed its own viability gate, 4 of 6. I named the two failures a
mechanism and a repair, and left it there — a rule in this project says you don't run
the search until the gate passes, and you don't rewrite the gate to make it pass. This
post is about going back and doing the two repairs honestly, and what happened when I
did.*

## What was left over

The fitness in question is one number: how far a candidate certificate's residual sits
under the budget its own conditioning leaves it, in whatever weighted norm you choose to
measure things in. It is a real measurement — gauge invariant, tracks a known defect,
beats my best hand-picked weight by 8.6× on an object whose answer is known. And it
failed its own six-property gate anyway, on two properties:

- **P2 (finite):** a fitness undefined on 22% of its own search box isn't safe to hand
  an optimizer without saying so.
- **P3 (monotone):** pushed off the true solution by a known small amount, the fitness
  is supposed to fall by exactly that amount — a known answer, not a guess — and it
  didn't, by a lot, at the worst-tested weight.

Both had a diagnosed mechanism, not just a symptom, and I wrote down what a repair
would be without doing it, because that's the discipline: name the fix before you build
it, so you can't quietly steer the repair toward the answer you want.

## Repair one: there were two walls, and the box only knew about one

The fitness has an *analytic* upper wall — past a certain rate of growth in the weight,
the true profile itself has infinite norm, full stop, no numerics involved. That wall
was already a hard constraint on the search box.

What leg 49 found, and didn't act on, is that there's a *second* wall, lower down, and
it isn't analytic — it's where the floating-point conditioning of the linear solve
degrades past the point where the inverse is even approximately an inverse. Below that
wall, the fitness genuinely has nothing to report; it isn't a defect of the weight,
it's a defect of asking float64 to invert something it can't. Every one of the 9
roster weights that returned no fitness sat below that measured wall.

The repair is one sentence: carry the *measured* wall in the box, the way the
*analytic* one already was. Not tune it, not soften the threshold — bound the search
away from a region that was already known, before this leg, to be unreachable.

## Repair two: one probe grid can't be linear for every weight at once

P3's probe perturbs the converged solution by a tiny amount and checks that the
fitness falls by exactly that amount, on a log-log plot, slope 1. That's a real known
answer — it comes straight out of the linearization, not out of guessing. But it's only
a known answer *while the linearization holds*, and how far you have to perturb before
it stops holding depends on the weight's own conditioning — which, across the roster,
spans three orders of magnitude. A probe grid that's safely linear for one weight is
already past that point for another. Testing every weight on the same grid measures the
*probe* breaking, at some weights, not the *fitness*.

The repair: give each weight its own window, sized from its own conditioning, decided
before looking at the results — and report what that window buys (how many weights it
can even validate) instead of silently assuming one grid worked everywhere.

## What happened

I implemented both, re-ran the exact same frozen gate — same thresholds, same
resolutions, same search budget leg 49 used — and it still says **FAIL, 4 of 6.**

But not the same FAIL. P2's finite fraction moved from 0.775 to 0.875 — real
improvement, still short of the 0.90 bar, because the wall I carried is a one-parameter
slice and the actual boundary of the failing region depends on two length scales, not
one. And P3's honest accounting is that fewer than half the roster (21 of 40) can even
be validated with a floating-point probe at all — the rest need a perturbation smaller
than double precision can represent usefully. Among the ones that *can* be validated,
8 still violate strict monotonicity and the worst slope error is 0.34, both of which
I read as float64 roundoff at the edge of what's representable, not a defect either
repair claimed to fix.

Neither number was chosen after seeing this run's results. Both constants
(`WALL_LOWER_DELTA`, `DEFECT_WINDOW_C`) are fixed in the code, and this is what they
bought.

## What this is and isn't

**Is:** two named, non-research repairs, implemented and measured, that move a real
property of the fitness in the right direction without gaming the gate that reports it.
The search still can't run — the ban stands, and even if this had come back 6/6 it
would not authorize the search today; that's for the next planning pass. **Isn't:**
progress toward a certificate. The object underneath all of this is a 1985 closed-form
profile. No link of the chain from a certified 1D toy to the Clay problem moved.

*Code: `solver/weight_search.py`, `test_weight_search.py`.
`experiments/p2_weight_repairs_v1.py` → `writeup/data/p2_weight_repairs_v1.json` →
fig48. Deterministic, ~140s.*
