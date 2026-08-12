# The tolerance we could build, and the tolerance the proof could afford

*Route-DTOL (leg 386). Companion: `TECHNICAL_P2_ROUTEDTOL_V1.md`. Figure: `fig99`.
Ceiling: **Tier 2**. Clay progress: **~0.05%**, unmoved.*

---

## The problem we walked in with

A previous leg built an instrument that answers a narrow question exactly: given a function
sampled on a window of radii, **is there any pure power law that fits it exactly?** The
instrument does not guess. It eliminates the unknown amplitude algebraically and returns either
an interval of exponents that are still possible, or `EMPTY` — and `EMPTY` is a *proof* that no
power law fits, not a failure to find one.

That instrument had one embarrassing property: on every input anybody would actually feed it,
it answered `EMPTY`. Real profiles are not exact power laws. They have logarithmic corrections,
cutoffs, subleading terms. The instrument was correct and useless in the same breath.

The obvious repair is to allow a tolerance: ask not "is `f` exactly a power law" but "is `f`
within a factor `1+δ` of one". The previous leg noted this repair, measured some numbers for
it, and — to its credit — labelled those numbers **post-hoc and not gate-deciding**, because
they were measured after the fact on cases chosen after the fact.

This leg's job was to do it honestly: **write down what the tolerance mode would have to do
before running it**, then run it, then report what actually happened including where the
prediction was wrong.

## What we wrote down before running

Two things, both derived rather than fitted.

**A width law.** If you allow a factor `1+δ` of slack, how much wider does the answer get? We
derived, in closed form, `width = 4·log(1+δ)/log(R₁/R₀)`. The interesting part is the
denominator: **the cost of tolerance depends on how long your window is.** The previous leg's
number, `0.8686`, is exactly `4/log 100` — an artefact of measuring on `[10, 1000]`. Shorten
the window to `[10, 100]` and it should *double*. That is a falsifiable prediction about a
number someone had already quoted as if it were a constant.

**A critical tolerance.** Below some `δ*` the answer must still be `EMPTY` — otherwise the
tolerance is just a knob you turn until you get the answer you wanted. We derived `δ*` from
Chebyshev best-affine approximation theory and predicted, in advance, that the *measured* `δ*`
would come in slightly **below** the formula, because the arithmetic we use encloses cells
rather than points.

Both predictions, the pass bands, and the exact test cases went into the journal in a commit
that landed **before** any measurement.

## What happened

**The width law held**, to `+0.51 %` across nine decades of `δ`, with the same offset
everywhere — a discretisation cost, not a fit. And the window-doubling prediction landed at
`1.9999989` against a predicted exactly `2`.

**The critical tolerance held**, in the predicted direction: `−0.98 %`, `−2.94 %`, `−9.46 %`
below the closed form for the three test profiles, all inside the pre-registered `±20 %`.
It also reproduced the previous leg's post-hoc numbers to eight or nine digits — so those
numbers were right; they simply had not been *earned* yet. Now they are.

**And the control held.** At `0.9·δ*` and at `0.5·δ*`, every mismatched profile is still
proved impossible. Six out of six. The tolerance is not a knob.

So the first gate clause answers **yes**. The instrument gained a real mode, whose looseness is
a declared magnitude with a formula attached.

## And then the second question

The leg carried a second, co-equal question, and it is the one that matters: **can the proof
that would use this instrument actually afford any tolerance at all?**

The chain is this. A certified decay exponent feeds a cutoff-radius bound. That bound needs the
exponent to exceed `1` (for one conclusion) or `3/2` (for a stronger one). A certification
carrying a tolerance hands that tolerance straight down the chain — the exponent is no longer a
number but an interval, and only its *lower* edge counts. An earlier leg composed the two laws
on paper and derived a condition; nobody had measured whether that condition can ever be
satisfied, because it demands `δ` be simultaneously large enough to admit the profile's own
imperfection and small enough not to wreck the bound.

We measured it directly rather than composing two laws, on thirty configurations.

**The answer is that the tolerance buys exactly nothing.** Not "little" — nothing. In all
thirty rows, without a single exception, a window of admissible tolerances exists **if and only
if the certified centre already exceeds the threshold on its own**. We probed the crossover at
a relative offset of one part in a million and it sits exactly at the centre. Widening `δ` moves
the *left* edge of what you can certify; it never moves the centre. There is no configuration
in which slack rescues a profile that was going to miss.

The object this analysis is aimed at carries an exponent of exactly `1`. The threshold is `1`.
**The window is empty**, and it is empty at every exponent `≤ 1`, for every profile shape we
tried.

So the second clause answers **EMPTY**. We are reporting it as EMPTY. We did not widen a band
afterwards to rescue it, and there was a moment where we could have: one test profile, read by
its nominal label, would have counted as a success. Read by the exponent it *actually realises*
— its cutoff sits inside the measurement window, so it decays much faster than its label
suggests — it does not. The journal had pre-registered which of those two readings decides, and
it decides the strict way. The verdict flipped from ADMISSIBLE to EMPTY when we honoured our own
pre-registration.

## Two verdicts pointing opposite ways, left that way

**Clause 1: YES. Clause 2: EMPTY.** We are not netting those into one word. The honest sentence
is: *the tolerance mode is a genuine instrument that the specific composition this route needs
cannot use on the object it has.*

There is a consolation prize, and it is a real one. The earlier leg's paper composition turns
out to be **conservative by a factor of 1.33 to 4.06** — it understates the admissible tolerance
on every row where a window exists, and never once claims a window that isn't there. Its
implied demand, that the exponent clear roughly `2.46` before any tolerance is allowed, is
**refuted**: the true requirement is just that the exponent clear `1`. That corrects a bound
that was quietly making the route look harder than it is. Corrected text has been routed to the
document that carries it.

## A late addition, from someone else's control

While this was building, a neighbouring unit landed a result worth stealing. It had built the
adapter that turns point samples into the certified cells our instrument eats — a conversion
that requires the caller to *declare* a regularity hypothesis, because nothing in a finite set
of samples can establish one. To test itself, it planted a **secret** violation of that
hypothesis and fed it in. The adapter accepted it, correctly: a declared hypothesis cannot be
verified, only recorded.

The certificate that came out had width `7.438494264988549e-15`. The certificate of a genuine,
truthful test case had width `7.438494264988549e-15`. **Bit-identical, and one of them was
false about its profile.**

There is no way to tell them apart from inside the certificate. The only thing that separates
them is the record of what was assumed. So the rule adopted — and implemented here — is that
**every output row carries the hypothesis in force, and a certificate without a hypothesis is
no certificate.** Our rows now say which hypothesis was in play, whether it was *discharged*
(the instrument established it itself, by evaluating over whole cells) or merely *declared*
(someone upstream promised it), or whether it was never stated at all — in which case the row
says, in words, that it is not a certificate about any profile. The weaker of the instrument's
two modes now declares its own weakness inside the row rather than in a docstring nobody reads.

We re-ran everything afterwards. Not one number moved. That is the point: this changes what a
row *says*, not what the instrument *computes*, and it is the difference between a result and a
result you can trust six months later.

## What this does not mean

It does not mean the route is closed. It means the load-bearing question moved: it was
"how accurately can we certify the profile", and it is now "**does the certified exponent clear
1 at all**" — a question about the object, not about the instrument, and one to which nothing
here contributes an answer. No profile of the actual object exists in this repository. Every
input in this leg is a planted analytic function with a known answer.

The two standing no-method obligations remain **open**. No link in the chain from the hard
problem to the solved one moved. **Clay stays at ~0.05%.**

---

*Runner `experiments/p2_route_dtol_v1.py`; data `writeup/data/p2_route_dtol_v1.json`;
journal `experiments/journal/leg_386.md` (pre-registration in PART I, landed before
measurement; results in PART II; the hypothesis-field amendment in PART III); tests
`test_dssp_decay_enclosure.py`, 18/18, with the previous leg's 12 assertions unweakened.*
