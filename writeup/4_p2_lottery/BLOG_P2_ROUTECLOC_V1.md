# The one-line arithmetic that decides how hard the last mile is

*Leg 381, Route-CLOC. Technical companion: `TECHNICAL_P2_ROUTECLOC_V1.md`. Data:
`writeup/data/p2_route_cloc_v1.json`.*

Last week an external reviewer wrote this repository a document called `CLAY_OBLIGATIONS.md` — a
list of what a numerically-confirmed blow-up candidate would still owe before anyone could call it a
proof. The document says of itself, in its own header, that the clauses resting on the reviewer's
reading are the ones most likely to be wrong. And then its closing note says: *if one clause here is
worth verifying first, it is §4.*

§4 rests on exactly two things. A one-line piece of arithmetic, and a paraphrase of the official
Clay problem statement. This leg checked both.

**The arithmetic survives. The paraphrase has an error in it.**

## The arithmetic

The candidate object is a *discretely* self-similar blow-up: it repeats itself, but only after a
fixed zoom factor `λ`, not continuously. In similarity variables that means the profile is periodic
in `s = −log(T*−t)` with period `2 log λ` — it breathes, log-periodically, all the way into the
singularity.

The reviewer's line was: the energy at time `t` scales like `(T*−t)^{1/2}` times the profile's own
`L²` mass. That is textbook for the *continuously* self-similar case. The question this leg was
given was whether it survives when the breathing is **handled rather than dropped** — and if not, by
what factor.

It survives. The exponent is `1/2` for both, and the ratio of the two exponents came out
**0.9999998844** — one, to seven digits. There is no factor. The reason is structural rather than
computational: the discrete zooms `λ^ℤ` are a *subgroup* of the same scaling group that fixes the
self-similar exponents, and restricting a group cannot move an exponent. All it can do is turn a
constant into a periodic function.

But "handled rather than dropped" turned out to be the operative phrase. The breathing on this
object is not a small correction — the profile's `L²` mass swings by a factor of about **three**
within a single period. Fit the energy naively, ignoring the modulation, and you get an exponent of
**0.4876** instead of `0.5`: wrong by 2.5%, and wrong in a way that looks exactly like a real
physical finding. Put the log-periodic factor into the fit and the exponent snaps back to `0.5` to
eight digits. The 2.5% is the price of dropping the modulation, and it is the mistake the gate was
written to catch.

One more thing came out of the re-derivation, which the reviewer could not have caught in one line:
in the case that actually matters — where the profile has infinite `L²` mass, which is the whole
point of §4 — **both sides of the reviewer's identity are infinite**, and an equation between
infinities cannot prove anything. The fix is to run the same argument on a finite ball, where every
quantity is finite and the conclusion is identical. Same answer; now with a derivation that holds
where it is needed.

## What the object's numbers actually are

Every discretely self-similar solution decays at least like `1/|y|` in the far field — that is a
theorem (Chae–Wolf), banked here at leg 260. Call that exponent `α = 1`. Then:

* finite total energy needs `α > 3/2`. The available bound gives `α = 1`. **Short by exactly one
  half — the certified exponent would have to be 1.5× the one the literature guarantees.**
* the energy inside any *fixed* ball, right up to the singular time, scales like `(T*−t)^{α−1}`. At
  `α = 1` that exponent is **zero, measured at −0.00026**. The energy near the singularity is
  bounded and essentially constant. **The infinity is entirely a far-field statement** — nothing is
  piling up at the origin.

That second point is the useful one, and it is why localisation is the right instinct: the problem is
out at infinity, so cut it off out at infinity.

## Why that instinct doesn't finish the job

Cutting off changes the solution. §4 says the obligation is therefore *transferred* to §5 —
persistence — rather than discharged. This leg's job was to price that transfer, not to attempt it,
and the prices are all clean powers of the cutoff radius `ρ`, each measured to better than 0.1%:

* the error the cutoff introduces into the equation does shrink: `ρ^{-3/2}`, both the nonlinear and
  the viscous part — and at exactly `α = 1` **those two scale identically**, so neither can be
  neglected;
* the pressure, which is global and feels the cutoff instantly everywhere, is perturbed at the
  singular point by only `ρ^{-2}` — relative to the profile's own pressure that ratio vanishes. **The
  pressure non-locality is not the obstruction**, which is worth knowing, because it looks like one;
* but the part you throw away is **not small in any critical norm**. Its `L³` size grows by a fixed
  amount for every decade you push the cutoff further out — constant to nine digits across five
  window widths. You cannot make the discarded tail negligible by cutting further out. You can only
  make the *equation error* small.

So the transfer to §5 is real, and now it is quantified: §5 inherits a problem where the forcing
error is `ρ^{-3/2}` small but the thing removed is never small.

## The paraphrase, and the error in it

The reviewer's summary of the Clay problem said the target is initial data that is smooth,
divergence-free, decaying faster than any polynomial, **with `f ≡ 0`**, such that no smooth solution
with bounded energy exists.

This repository had never actually cited the official problem statement. So this leg fetched it and
read it. Four clauses check out, one needed a labelling fix, and one is wrong:

* **bounded energy is confirmed** — it is numbered condition (7), verbatim, uniform in time. §4's
  premise stands.
* the decay condition is confirmed and is in fact *stronger* than stated: it binds every derivative,
  not just the field. That happens to be the easy one — a compactly supported cutoff satisfies it for
  free.
* **`f ≡ 0` is wrong.** Fefferman's breakdown statement on `ℝ³` permits *"a smooth `f(x,t)` …
  satisfying (4),(5)"*. The words "take `f(x,t)` to be identically zero" appear only in the two
  *existence* statements. A blow-up candidate is allowed a rapidly-decaying forcing.

Before anyone gets excited: that relaxation is not a shortcut, and the technical companion explains
precisely why the obvious exploit — define the forcing to *be* the cutoff error — fails on the
statement's own terms. But it is a real change to what the programme owes, and it is exactly the kind
of thing you only find by reading the primary source instead of the paraphrase.

## What this is not

It is not progress on the Clay problem. Verifying an obligation is not discharging one, and nothing
here moved any link of this repository's `L1 → L4` chain. **The odds stay at ~0.05%.** The numerics
here are float64 quadrature of a *synthetic* field built specifically so that any algebra error in
the derivation would show up as a disagreement — it is a falsifier, not a measurement of the real
object. The certified decay exponent that §4 actually needs is being built by a different leg, and
this one deliberately expressed every magnitude as a function of that exponent so it can be dropped
in when it exists.

What it is: the most valuable clause of the obligations document, checked, corrected in two places,
and priced.
