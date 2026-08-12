# The control that caught a `no` before we published it (PROG-R4, units U2/U3)

There is a gate in this programme whose *negative* answer is the expensive one.

It is called G1, and its wording was fixed before any of the work below was done:

> **DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO tol=1e-8?**

`yes` and the programme continues. `no` and — under `ORCHESTRATION.md` §3d — a stop fires and
route 4 stops. Not "we retry with a better solver". Stops.

So the interesting question is not *how do we get a yes*. It is: **if the machinery hands us a
`no`, how do we know the `no` came from the fluid rather than from our own code?**

This post is about the answer arriving, unprompted, in exactly the way it was supposed to.

## The setup, quickly

We are trying to recover published relative periodic orbits (RPOs) of 2-D Kolmogorov flow at
Re=60 on a 24×24 grid — the eight named rows of Table IV of Lucas & Kerswell 2015
(arXiv:1406.1820v2). These are orbits somebody else already found and published. Recovering
them is a *known-answer test*: if our Newton solver cannot find an orbit that is definitely
there, the fault is ours.

Alongside the real attempts we planted three controls, pre-registered before anything ran:

* **P**, an unconditional positive. Something that *must* be recovered.
* **N**, a negative. A phase-scrambled field that must **not** be reported as a recovered orbit.
* **R**, a conditional positive that exercises the period and shift directions.

And a rule, also pre-registered, in blunt language: if the controls do not fire as planted,
**G1 is not answered `no`.** It is answered `UNANSWERED`. A `no` may only be recorded on an
instrument that has been shown capable of saying `yes`.

## Control P: an answer you cannot fake

P needed to be a solution the solver must find, that we know exactly, and that involves no
search of our own that could itself fail. It is the flow's relative equilibrium — but written
as the exact fixed point of the *discrete* map the code actually iterates, in closed form:

```
w*_hat = dt * forcing_hat * decay / (1 - decay)
```

Not the fixed point of the PDE. The fixed point of the timestepper. Measured:
`||Φ_dt(w*) − w*|| = 7.6e-14`. Perturb it by 0.1% and Newton must walk back.

**P failed the first time it ran.** At the pre-registered period T=19.33 the trust region
collapsed at epoch 1, the residual moved 236 → 223, and the state did not move.

We did not retune it until it passed. We measured *why*. The equilibrium's leading Lyapunov
exponent is λ≈2.88, so over T=19.33 a perturbation is amplified by ~1e24 — against the ~1e16
that double precision spans. The Jacobian over that window is numerically empty; there is no
information left in it to descend. The chaotic attractor the *real* seeds live on has λ≈0.35
and an amplification of 873 over the same window — eight orders of magnitude gentler. P at full
period was not a hard test, it was an impossible one, and it was impossible for a reason that
does not apply to the thing it is controlling.

So P was re-scaled, by a rule derived from the **target's** amplification rather than from P's
outcome: pick the period at which the equilibrium's *measured* amplification equals the
attractor's `8.73e2`. Log-interpolating the measured table gives T=2.65, where the plant is
still exact (`||Φ_T(w*) − w*|| = 8.03e-14`) and amplifies by `8.35e2` — as hard as the real
problem, neither easier nor harder. That distinction is the whole of the honesty here, and the
original failure stays in the record.

## The thing that actually got caught

With P re-scaled, we swept it over GMRES caps to find the smallest budget at which it works.
Three runs. And two of them returned a pair of numbers that cannot both be true:

```
reason = "converged"          converged_to_tol = False       final residual = 1.63e-8
```

against a tolerance of `1e-8`. The solver said it converged. The solver said it did not reach
tolerance. One of those is a lie.

It was the second one, and here is the mechanism. The outer routine drives the inner Newton
**one iteration at a time**, because the residual is measured against a moving reference that
has to be rebuilt each step. With a budget of one inner iteration, the inner solver can report
`"converged"` from two different places:

* **at entry** — the incoming point is already below tolerance. Nothing moved; the residual the
  outer routine reads is the right one.
* **on the step it just took** — the inner solver takes its step, appends the new residual,
  finds it below tolerance, and upgrades its exit reason on the way out.

In the second case the converged answer is the *output* point, and the residual the outer
routine was reading — the first entry of the history — is the value from **before** the step.
The outer routine treated the second case as the first. It read the pre-step residual, and it
broke out of the loop *before* the block that adopts the new point.

So it threw the solution away. It found the orbit, discarded it, and reported failure.

Read that against G1's wording one more time. **This would have recorded a non-recovery on an
attempt that recovered** — on the one gate whose `no` stops a research route. Not a crash, not
a `nan`, nothing that shows up as a bug. A clean, plausible, well-formatted false negative.

The fix is four lines. Under it, P recovers: `1.95e2 → 7.75e-9` in 33 epochs, state error
`1e-3 → 2.89e-6`.

## Why this is the argument for controls, not for code review

Nobody was going to find that by reading the code. It is a two-line interaction between two
functions that are each individually correct, in a branch that only executes when the solver
*succeeds* — which, on this problem, had never happened before. Every test in the suite passed
before the fix and passes after it. The one existing validation run, milestone M1, never reaches
that branch at all: we re-ran it against the fix and it reproduces **bit-identically**, every
stored field except wall times.

It was caught because we had planted something that was *required to succeed*, and it didn't.

That is the second time in this one unit that a number taken at face value would have set the
budget too low. The first: an early cost probe reported that GMRES was consuming about 20 Krylov
directions, so a cap of 40 looked generous. But that probe had only watched three iterations,
all far from the solution, where the linear solve is easy. The hard late iterations need far
more — P itself collapses at a cap of 50, needs 140. Had we set the caps from that probe,
**a `no` at G1 would have been a fact about our budget, not about the fluid.**

Both catches came from controls. Neither came from review.

## What this does not say

It does not say G1 is `yes`. At the time of writing G1 is **UNANSWERED** and the T=1e5 DNS that
feeds it is still running. No orbit has been recovered. No basin radius has been measured.

It does not say the solver is correct. It says one specific false-negative path is closed, and
that we found it the way we said we would.

And it moves nothing toward the Clay problem. No link of the chain moved; the ceiling on this
programme is Tier 2 and the odds stay ~0.05%. `CLAY_OBLIGATIONS` §6's two no-method obligations
remain **OPEN**, and §4 remains **OPEN and not discharged**.

One more caveat, and it is not a small one: this was all done in a single-worker mode where
there is no second pair of eyes. The diagnosis, the fix and the bit-identity check were made by
the same session that wrote the change. Every one of them is carried into G1's own answer
labelled **UNVERIFIED**, and stays that way until a fresh session checks it. A control that
catches your bug is worth a great deal. It is not worth as much as somebody else checking.

---

*Technical detail, the exact code paths and the cap arithmetic:*
[TECHNICAL_P2_PROGR4_CONTROL_CATCH](TECHNICAL_P2_PROGR4_CONTROL_CATCH.md).
*Pre-registration:* `experiments/journal/prog_r4_u2u3_prereg_addendum.md`.
