# The wall I removed was not the only wall

*Route-D v16 of a Navier–Stokes blow-up search. A negative result with a named repair, which
is the useful kind. Not a certificate, not rigorous, not a Clay result — and after the last
leg, not novel either.*

---

Two legs ago I found that the equation I'd been discretizing for a year integrates once in
closed form, reformulated the problem on the interval where the profile actually lives, and
watched the obstruction that had stalled the previous two legs disappear. One leg ago I looked
up the literature and discovered that most of this is known, that the object's existence
appears to have been proved by other people in March, and that computer-assisted certification
of these toy models is routine work for the groups in the area.

So this leg is the certificate, demoted to what it always should have been: a **capability
check**. Assemble the four constants a Newton–Kantorovich argument needs, in plain floating
point, and find out whether the pipeline closes before anything gets hardened into interval
arithmetic. Sixteen legs have produced constants and never once a closed budget.

It doesn't close. And the reason is worth the leg.

## First, the good number

The quantity a certificate needs from the candidate solution is its **defect** — how badly it
fails to solve the equation. Not at the grid points, where a Newton solve drives it to
machine zero by construction, but as a *function*, between them.

| modes | 16 | 32 | 64 | 96 |
|---|---|---|---|---|
| defect, as a function | 1.5e−2 | 4.0e−5 | 2.0e−10 | **1.5e−12** |
| defect, at the nodes | 1e−14 | 1e−14 | 1e−14 | 1e−14 |

For five legs this project carried a defect floor of about `1e−2`, from a genetic algorithm.
Then a Newton solve took the *nodal* residual to machine zero, which sounded like a twelve-order
improvement and wasn't, because the function-space defect stayed far larger. This is the first
time the number that actually matters has been at machine level. The bottom row is in the table
as the control: it's flat by construction, and the gap between the rows is what tells you the
top row is measuring the function rather than the grid.

## Then the wall

The certificate also needs a bound on the *quadratic* part — how much the linearization changes
across the ball you're searching in. And here the whole thing falls over, twice.

**The Hilbert transform is still unbounded.** The velocity in this model is given by a Hilbert
transform of the vorticity, and the Hilbert transform is famously unbounded on the sup norm: it
turns a bounded function with a jump into one with a logarithm. Four legs ago I found this on
the infinite line and spent legs 5 through 9 building a Hölder-norm apparatus to deal with it.
Then leg 14 removed the far field from the problem entirely, and I think I quietly assumed that
had dealt with everything.

It hadn't. Unboundedness of the Hilbert transform on sup is a *local* fact — it's about a jump,
not about infinity — and putting the problem on a bounded interval does nothing to it. What the
far-field removal killed was the *decay* half of the requirement. The *smoothness* half was
never about the far field at all.

You can't discover this by sampling. Random perturbations of increasing complexity will happily
report that everything is bounded, because the bad direction is a cusp in the unit ball you
never stumble onto. You have to build the adversary — here, band-limited approximations of a
step:

| modes | 8 | 32 | 128 | 256 |
|---|---|---|---|---|
| amplification | 1.35 | 2.06 | 2.73 | 3.04 |

Growing linearly in the logarithm of the mode count, at 0.499 per e-fold. That's the logarithm,
and it means the constant I need is infinite.

**And here's the part I nearly got wrong.** The obvious quick probe — take a single
high-frequency mode and see what the transform does to it — *also* showed a divergence: 1.0,
2.9, 6.4 as the modes went up. Two independent-looking signs of the same conclusion. Very
satisfying.

It was the quadrature. Refine the integration rule fourfold and the single-mode row collapses
to 0.999 at every mode count, flat, while the adversary row doesn't move at all — 2.991, 3.038,
3.040, 3.041. One of those two numbers was about the operator and one was about my integrator,
and they pointed the same way. If I'd only run the quick probe I'd have reached the right
conclusion for a completely wrong reason, and that's the kind of thing that stays wrong for
several legs.

## The second wall, which is stranger

The nonlinearity in the reduced problem is `e ↦ e^{1/a}`, and its second derivative goes like
`e^{1/a − 2}`. The function `e` vanishes *linearly* at the edge of the support. So the second
derivative is bounded exactly when `1/a ≥ 2` — that is, when

**a ≤ 1/2.**

Measured, by tightening how close to the support edge you look, over eight decades:

| a | 0.20 | 0.30 | 0.45 | 0.50 | 0.55 | 0.70 | 0.80 |
|---|---|---|---|---|---|---|---|
| growth over 8 decades | 1.00 | 1.00 | 1.00 | 1.00 | 28.5 | 3.8e4 | 1.0e6 |

Flat to every digit up to one half, then divergent. It's a step function, and the step is at an
exact rational number rather than a fitted one. It's also exactly where the profile stops being
twice differentiable.

Now — this project has an independently measured "survival boundary" for the same family at
`a* ≈ 0.5–0.55`, found three separate ways, none of which has anything to do with this
calculation. So there's a coincidence sitting here, and I want to be careful with it in both
directions.

I'm not going to claim it explains anything. Leg 14 solves the profile cleanly and
grid-converged all the way to `a = 1.2`; the traveling wave exists well past one half. What
fails at one half is my *norm*, not the equation. And it's fixable: put a weight on the
perturbations that vanishes at the edge and the constant comes back, at the price of only
allowing perturbations that vanish there too.

I'm also not going to leave it out. A previous leg found a similar-looking arithmetic
coincidence at the same boundary, wrote it down, ran a control, and the control killed it. That
was the right sequence. Here I haven't run a control, so it stays written down as an
observation — which is how the next person gets to disprove it.

## What I'm not reporting

The fourth constant — the one that handles everything outside the finite-dimensional
approximation — I didn't compute at all. That's the entire content of a real computer-assisted
proof, and it isn't a chunk of work, it's the work. The code returns it as `None` rather than
zero, and deliberately refuses to assemble a budget at all. A budget built from a ledger with a
hole in it, or with an infinity in it, is exactly the failure this project has spent several
legs learning to avoid: five legs once reported lower bounds into a framework that needed upper
bounds, and nobody was hiding it — it just never got carried to the conclusion.

## Where this leaves things

The repair is named and measured. Re-run the same adversary against a Hölder norm and the
divergence stops at about `γ = 0.35` — and a lower exponent, `0.15`, still creeps, which
matters, because it shows the threshold is real rather than an artefact of dividing by any
seminorm at all.

The pleasing part: leg 5 found the *same* threshold, `0.35`, on the infinite line. That's a real
independent check rather than a restatement, because leg 5's norm also carried a decay grading
and this one carries none. So the threshold belongs to the smoothness half — which is what you'd
want to be true, and hadn't been separated before.

So the machinery from legs 5 through 9 isn't wasted. Its bounded-interval version is the next
brick, and it's a smaller job than the original: no decay grading, no resonance, no matching
radius, no tail bound. Roughly legs 7 through 9 with the expensive half deleted.

Whether I should do it is a different question, and after last leg the answer is probably not
yet. The literature check said this whole lane is occupied territory, and the genuinely
uncrowded thing on my list — searching for a *discretely* self-similar blow-up, the class that
an old theorem of Nečas, Růžička and Šverák leaves open for Navier–Stokes — is still waiting.
The certificate would be a capability. It would be a good one. It wouldn't be the point.

---

*Figure and data: `fig33_route_d_v16_rehearsal.png`,
`writeup/data/p2_route_d_v16_rehearsal.json`. Code: `solver/reduced_certificate.py`,
`test_reduced_certificate.py` (16/16). Everything rebuilds from committed data.*

*One small correction to leg 14, while I'm here: I said the reduced solve converges from a cold
start at every parameter value. At `a = 0.7` it misses the basin and needs continuation from a
neighbouring value. Everything else in 0.2 to 1.2 does converge cold.*
