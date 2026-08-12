# The auditor finds the bug it was hunting, in its own instrument

*Route-BVRRV v1 — leg 233. Figure: fig101. Data:
`writeup/data/p2_route_bvrrv_v1_postrepair.json`. Technical companion:
`TECHNICAL_P2_ROUTEBVRRV_V1.md`.*

## Three legs, and nobody outside the room

A while back, leg 205 found that one small routine in this repository —
`odd_field_x_slope` in `solver/boussinesq_rescaled.py`, which extrapolates a slope at the
origin by fitting `r`, `r³` and `r⁵` to whatever radial nodes fall inside a little window —
could return a confident number that was simply wrong. Two mechanisms. In one of them, the
fit window was empty, `lstsq` was handed nothing, and the routine returned **exactly `0.0`**
with no exception and no warning. In the other, the window was so wide relative to the field's
own scale that the fit had nothing to do with the origin at all: asked for a slope whose true
value is `2.0`, it answered `0.26930226316474387`. That is a relative error of **0.865**, and
nothing in the output says so.

Leg 205 found both and patched neither. Leg 221 patched both — and then did the other half of
the job too: it checked that no number already banked in the repository had been computed
through the broken routine and would now change. It found none.

That is a good outcome and it has one problem: **leg 221 graded its own repair.** Two later
legs then leaned on that grade. Leg 307 described leg 221's call census as a "cited input, not
re-run". Leg 335 said in its own journal that it *trusts rather than re-runs* leg 221's
zero-contamination result. So a number nobody outside the room had ever checked was quietly
becoming load-bearing.

Leg 233 is the party from outside the room. It re-runs both halves — the repair *and* the
re-confirmation that graded it — with its own instruments, and the gate answers **yes on
both**. The interesting part is not the yes. It is what the leg had to do to earn it, and the
bug it found in itself along the way.

## A zero you cannot believe yet

Suppose you want to show that a repaired routine changes nothing about the numbers already
banked. The clean way is a differential: run every banked computation again, but with a shim
in place that calls **both** the old routine and the new one on identical inputs, compares the
two results bit for bit, and hands back the old one — so the trajectory the computation
follows is exactly the trajectory that produced the banked file. If every call agrees bitwise,
nothing can have moved because of the repair.

Leg 233 did that over **340 233 calls**. All 340 233 agreed bit for bit. Zero moved.

And on its own, that zero is worth much less than it looks. It is equally consistent with two
completely different stories:

* the repair is correct on everything the repository actually computes; or
* the new guards were never *reached* on anything the repository actually computes, so nothing
  was tested and the zero is free.

A zero that is merely observed is not evidence. A zero that is *explained* is. So each call
was also instrumented for whether the guards could have fired: does the window cap actually
bind? How many nodes are in the window? And the answer is the load-bearing number of the whole
leg — sharper than the zero it explains:

> **`cap_binds = 0` across all 340 233 calls, and the smallest window occupancy anywhere in
> the banked corpus is 4 nodes, against the guard's floor of 3.**

No banked call comes anywhere near either guard. The cap is non-binding on every one, which by
the routine's shrink-only rule makes the effective window the identical float and the fit
bit-identical. *That* is why nothing moved. And the probe can report the opposite — it binds at
a shrink factor of 0.0622 on leg 205's own pathological field — so this is a statement about
the corpus, not about a probe that is incapable of complaining.

Panels C and D of fig101 are those two facts side by side: what was compared, and why the
answer had to come out as it did.

## Everything live, nothing from cache

One detail matters more than it sounds. Leg 221's original sweep was resumable and
cache-backed, and its re-confirmation completed in **66.1 seconds** against an original run of
roughly **34 hours**. A cache replay is not an independent re-run; it is a very fast way of
reading what you already believe.

Leg 233 refused that route. There is no cache-read path anywhere in its runner, every unit
carries `ran_live: true` and `from_cache: false`, and the bill came to about **1.9 hours of
wall time, four-way parallel** — six banked artifacts and the module's own three test suites,
all restored clean afterwards, no non-zero return codes.

It also turned out to be a **strict superset** of leg 221's scope rather than a match. Every
per-unit call count reproduces leg 221 exactly — 2, 62, 52 516, 42 488, 140 016 from the
artifacts and 4 999 / 0 / 142 from the suites — which is much stronger than a matching total,
because a total can agree while the composition underneath has shifted. The one divergence is
`spike1_stepC_gate`: leg 335 had established that its banked artifact records `steps: 2500`
while the script's command-line default is `400`, so running it correctly costs
**100 008 calls instead of 16 008**. That is **+84 000**, it is reported as an excess, and it
is why this leg's total legitimately exceeds leg 221's 256 233 instead of matching it.

## The repair, re-graded from outside

The other clause is the repair itself. Leg 205's 81-case battery was read verbatim out of git
— it is the object under test, so re-implementing it would test a different battery — and run
**twice in one process**: once against the pre-repair routine loaded straight out of the old
commit, once against today's. Panel A of fig101 is the result.

**SILENT_WRONG: 18 → 0.**

Before believing that differential, the leg checked it was not comparing a module against
itself: the two routines are asserted to be distinct objects with the signatures the repair
requires, and they are shown *disagreeing by a measured amount* — `0.26930226316474387` versus
`2.0007759522991355` on the wide-window case, and exactly `0.0` versus a raised `ValueError`
on the empty-window one.

Then the control on the control. The pre-repair column has to be leg 205's finding and not an
artifact of this leg's harness, so it was compared **case by case on the case name**, not
tally against tally — because a tally can match perfectly while individual verdicts swap
places. **0 of 81 mismatched.**

And then the measurement a count cannot make. "18 → 0" cannot see a repair that buys its zero
by breaking something else, so the leg built the full transition matrix. The 18 split **13 →
OK** (the value is now right) and **5 → RAISED** (the routine now refuses rather than
fabricating). Everything else stayed on the diagonal — except three cases that went **OK →
RAISED**, which leg 221 never reported.

## Two of leg 205's passes were luck

A new refusal is not automatically a regression and not automatically correct, so all three
were adjudicated against the routine's own documented precondition, by rebuilding each case's
grid and measuring the window occupancy and the **rank** of the fit's design matrix. Panel B
of fig101 shows what came out.

Two of them are the striking ones. At `r_win = 3e-4` and `5e-4` the window holds **21 and 32
nodes** — plenty, so the occupancy guard is provably blind to them — but the `(r, r³, r⁵)`
design matrix is numerically singular, with singular-value ratios of **4.125e-16** and
**3.867e-15**. `lstsq` quietly returned its minimum-norm solution, which is not the quantity
anyone asked for, and that solution landed at a relative error of **4.9972e-04** against a
tolerance of **5e-4**.

Leg 205's classifier scored both **OK**, with a margin of `2.792e-07` — **0.056% of the
tolerance**. They were accidental passes on rank-deficient fits: right by luck, in exactly the
fabrication class leg 205 had named. The repaired routine refuses them. The third case is the
same story with 2 nodes against 3 parameters.

Verdict on all three: **3 JUSTIFIED_REFUSAL, 0 UNJUSTIFIED_REGRESSION**. It strengthens leg
221's repair, and a verifier that had only re-counted would have missed it in either
direction.

## The part worth writing down: the auditor's own fabricated zero

While all this was running, the leg noticed something about its own instrument.

Its shim tracked a quantity called `max_rel_residual_seen`. It was initialised to `0.0` in the
state dictionary — and **never written to by any code path**. So it reported exactly `0.0` for
every artifact: a plausible-looking number that measured nothing at all.

That is the *same failure class* as leg 205's DEFECT A — an unguarded `lstsq` silently
returning exactly `0.0` — occurring in the auditor instead of the audited. It was caught by
noticing that a least-squares relative residual is never exactly zero on real data across
95 068 calls.

The probe was repaired to actually solve the fit and return ‖Ax − y‖/‖y‖, and re-measured
live. It is now demonstrably alive: **1.296e-05** over 2 calls on one artifact, **1.469e-01**
over 62 on another. None of the 64 exceeds the routine's `0.5` backstop, and the `0.1469` is
the informative one — it sits within a factor of **3.404** of the backstop, so the backstop is
set at a scale the data approaches, rather than being unreachable by construction.

But four heavy sweeps were already in flight when this was found, and retrofitting them would
have cost roughly 30 CPU-hours. So the leg did the honest thing rather than the tidy one: the
merge step **strips** the fake `0.0` from every record that lacks a measurement count and
marks it `residual_instrumented: false` with an explicit NOT MEASURED note. The key is absent,
not zero.

Which leaves a stated limit, not a smoothed one: **the residual is instrumented on 2 of 6
artifacts, 64 of 340 233 calls.** The rest is covered by the observation that the residual
backstop can only manifest as a *refusal*, and `raise_post = 0` across all 340 233 calls — a
backstop that never refused never fired. That is a covering argument, and it is itself a
measurement, but it is not a direct measurement of the residual on those calls. It stays open.

## What else moved, and what is still not understood

Seven hundred leaves in the regenerated artifacts differ from their committed values — 700 of
2 253 compared. Leg 221 saw the same thing (839, over its own smaller scope). **None of the
700 is attributable to the repair**, and not by a separate control run: by construction, since
the shim hands back the pre-repair value, so the executed trajectory *is* the pre-repair
trajectory, and every call agreed bitwise anyway.

What the movement actually *is* — pre-existing irreproducibility somewhere in this
repository's numerics — is measured here and **not diagnosed**. That is left open on purpose,
and a future leg that wants the cause should not borrow this one's conclusion as cover.

One thing did fall out for free. Leg 221's sharpest mover was `spike1_stepC_gate`, where
`alpha` shifted by **13.2%** and `cut_omega[10]` by a relative **4.47**. Leg 335 had
adjudicated that as an artifact of running the wrong step count. Re-run here at the corrected
2 500 steps, the worst leaf in that artifact moves by **9.028e-12** — about **eleven orders of
magnitude** below leg 221's 13.2%. Leg 335's call is confirmed, by live measurement, from a
harness that shares none of its code.

## What this is, and what it is not

Leg 205's finding is closed on independently-confirmed footing: the two mechanisms were real,
they are repaired, the repaired routine rejects correctly, and it contaminated nothing that
was banked.

It is worth being exact about how small that is. This is a verification of a solver utility's
**input-validation guards**. It establishes no new mathematics and no new numerics. It does
not certify that leg 205's battery is a good battery — this leg found two of its 32 passes to
be accidental. It does not certify that the moving artifact leaves *ought* to move; only that
none of the movement comes from the repair. It does not repair the caller-census drift it
found (15 real importers today against a registry of 6 banked artifacts, with all three
newcomers post-dating the repair and therefore unable to carry contamination) — verifiers
report; they do not repair.

**No `L1 → L4` link moved. Clay stays ~0.05%.**

What the leg is really an argument for is a habit: when a measurement comes out as zero, ask
whether the instrument could have said anything else. Leg 233 asked that of leg 221's zero and
got a real answer — `cap_binds = 0` with 4 nodes against a floor of 3. Then it asked the same
question of its own instrument, and the answer was no. Both are in the record, at the same
level of detail, because the second one is the more instructive.
