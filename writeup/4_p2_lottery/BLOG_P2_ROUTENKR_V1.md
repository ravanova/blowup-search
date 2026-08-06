# The third copy is where you stop copying

**Leg 128 · Route-NKR · a repair, and the draft of it that had to be thrown away**

Technical companion: `TECHNICAL_P2_ROUTENKR_V1.md`. Every number here is in
`writeup/data/p2_route_nkr_v1_repair.json`.

---

## A certificate that certifies nothing

Here is the smallest version of the problem. Take `F(x) = x² − 2`. Its zeros are exactly
±√2. Now point a certificate at `x = 1.0`, which is emphatically **not** a zero — `F(1) = −1`,
and the nearest actual zero is 0.414 away.

Fed honest constants, the code refuses. Good.

Fed one forbidden number — `Z₀ = −1`, where `Z₀` is by definition an upper bound on a norm
and so cannot be negative — the code cheerfully reported a **certified ball**
`[0.8083, 1.1917]` around the non-solution. That ball contains no zero of `F` whatsoever. It
misses √2 by 1.16 of its own radii.

Leg 116 found that. It found 21 such cases in a 52-case battery, 19 of them load-bearing
(meaning: the honest version of the same input refuses, so the forbidden number is exactly
what bought the certificate). And then, by its own gate, leg 116 **did not fix it** — it
pinned every defect as a failing-on-purpose test and handed the repair on.

This leg is that repair.

## Why it was one repair and not three

The interesting part isn't the bug. It's that we'd already found it twice.

- Leg 79 found it in `port_certification.py`: 11 of 25 bad inputs certified. Fixed in place.
- Leg 98 found it in `interval_certificate.py`: 12 of 36. Fixed in place — **by copying leg
  79's function**.
- Leg 116 found it in `nk_bounds.py`: 21 of 52. Not fixed.

And leg 98's copy came with a comment explaining itself:

> *"Mirrors `port_certification._hypothesis_violations` so the two pipelines cannot drift
> apart on what 'outside the theorem' means."*

That comment is a promise with no mechanism behind it. Two functions that are supposed to
stay identical, kept identical by someone remembering. The third call site is where the
software-engineering folklore says to stop copying — it's literally called the Rule of Three —
so the predicate now lives exactly once, in a new `solver/certificate_guards.py`, and both
copies are gone. All three modules now call the *same function object*, and there's a test
that checks it by identity rather than by resemblance.

The nice property of that test: it comes out **False** on the pre-repair modules. A check
that can't fail isn't a check.

## The rule the repair had to obey

This is code that certifies mathematical claims. So the leg came with a hard constraint:
**it may turn things that used to be accepted into refusals, and it may never change a number
that a good input already produced.** Not "change it a little". Not "change it within
tolerance". Bit-for-bit.

That got measured properly: 4626 clean-input comparisons, pre-repair source pulled out of git
and run side by side with the new one in the same process, compared with `==` and a
distance-in-ULPs rather than a tolerance.

**4626 out of 4626 identical. Worst distance: 0 ULP.** All seven neighbouring test suites pass
untouched.

## The draft that broke the rule

This is the part worth writing down, because the first attempt failed and the failure was
instructive.

Three of the surviving bad cases produce a ball of radius exactly zero. That looks like an
obvious thing to reject — a "ball" of radius 0 doesn't contain anything, so how can you
certify a zero inside it?

So the draft rejected it whenever the residual `Y₀` was positive, reasoning: the theorem says
the radius is strictly positive when `Y₀ > 0`, so a computed `0.0` must be a floating-point
artifact.

It *is* a floating-point artifact. Rejecting it is still wrong.

The differential caught it immediately — 36/36 dropped to 35/36 — on the input
`(Y₀, Z₀, Z₁, Z₂) = (1e-30, 0.5, 0.4, 2.0)`. There, the honest radius is about `1e-29`. That's
a **real certificate**. Its radius just happens to be too small to represent against the other
numbers in the formula. Refusing it isn't caution; it's a false negative on a valid proof.

So the draft was reverted rather than tuned — the leg's own rules say a repair that moves a
clean result stops, it doesn't iterate. What survives is narrower and actually true: a
zero radius is now **flagged**, with the verdict stating which of the two mechanisms produced
it. And the one case that is a genuine degeneracy — where `Z₂ = 1e-320` makes the contraction
budget overflow to infinity — is refused on the *budget*, which is where the actual problem
was, not on the radius, which was just where it showed up.

The general shape of that mistake is worth keeping: **the symptom and the defect were in
different places, and the first fix went to the symptom.**

## What got fixed, and what honestly didn't

Of leg 116's 21 false-closing certificates, **17 now reject**. The headline case — the ball
around the non-solution — is gone: refused by hypothesis, no radius reported at all.

Four remain, and they're a class rather than a leftover. All four supply constants that are
nonnegative and finite. They satisfy every hypothesis of the theorem. They just **lie about
the magnitude** — a residual reported as `0.0` when it's really `1`, or a quadratic constant
under-reported by six decades.

No validation layer can see that. A guard checks that a number is the right *kind* of number;
it cannot check that the number is *true*. Our own `interval_certificate.py` said so years ago
in a docstring: *"Validity checking cannot catch this and no amount of it ever will."* Closing
that class means making the **caller** prove where `Y₀` came from, which is a different repair
in a different file.

One more thing didn't get fixed, and it's flagged rather than quietly dropped. Deep in the
far-field integral there's a grid whose lower cutoff scales with `X`, and past `X ≈ 1e11` that
cutoff swallows the part of the integrand that carries the mass — so the "upper bound" drops
2.12% below the truth. The obvious fix is to lower the cutoff. Measured: doing that moves
**15 of 15** clean values in the live range, worst 1.08e-04 relative. That's exactly the thing
this leg isn't allowed to do. So the number is untouched and the code now *warns* when you
evaluate it out there. The margin is the honest part: nothing in the repository ever evaluates
above `X = 3.2e7`, which is 3.49 decades clear.

## The part that isn't progress

None of this moves anything mathematically. `nk_bounds.py` is scaffolding for a bound
programme whose real ceiling is somewhere else entirely, and every defect leg 116 found was
already unreachable from any actual caller in the repository. Nothing that was ever published
from this code was wrong.

What changed is narrower and duller: before, if you handed the certificate an impossible
number, it would hand you back a proof. Now it tells you the number is impossible.

**A validation layer restores the guarantee, not the margin.** Those are different things, and
the difference is most of what makes this kind of work honest.
