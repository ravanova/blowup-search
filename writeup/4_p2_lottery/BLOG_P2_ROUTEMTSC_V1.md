# The last survivor of a 14-space screen, tested on the real object instead of on paper

Leg 301 screened fourteen candidate function spaces against three separately-measured ways this
project's certification machinery has died before, and found exactly one that survives all
three on paper: a rational Hardy basis (Malmquist–Takenaka), where the Hilbert transform is
exactly diagonal instead of exactly zero on the diagonal, which is where the incumbent broke.
But 301's argument only used the *bare differentiation matrix* — a clean, closed-form object
with nothing else attached. This leg's job was to stop reasoning on paper and check the real
thing: solve the actual target, build its actual coupled linear operator, and see what it looks
like once it's moved into the new coordinates.

**First attempt gave the wrong answer, and the check that caught it is worth repeating.** The
first run showed the operator's conditioning collapsing toward zero as the truncation grew —
which would have read as a clean kill. A control (build the *same* transform with no operator
in it at all — it should be the identity) showed the *identical* collapse. That meant the
numerical grid, not the target, was the problem: it was too coarse to represent the basis
functions being tested against it. A denser, verified grid removed the collapse entirely.

**On the corrected, verified grid**, across an eightfold range of truncations, the real
operator's diagonal stays flat and nonzero, its growth rate tracks the theory's requirement, and
its conditioning does not degrade with truncation — the sharpest test this repository's own
history has for this failure mode, and it did not fire. The exact-diagonal Hilbert-transform
claim held up on the code's own machinery, not just on paper. And the piece nobody had measured
— what the nonlinear (quadratic) term does to this basis — was measured directly on the real
target's exact quadratic remainder, and it stayed bounded across two orders of magnitude of
input frequency, with the one caveat (the highest-frequency test hit the edge of the projection
window used) reported honestly rather than smoothed into a clean pass.

**None of this builds a certificate, and it does not lift the ban that has stood since three
earlier attempts at this same certification died.** It answers the specific question that
ban's own lift condition asked for: a scoping leg, on the fourth candidate, checking it against
each of the three ways this has died before. All three checks read "does not recur," with the
nonlinearity's evidence measured, not assumed, and the cost of actually building a validated
transform for this basis — which exists nowhere in the literature — priced at roughly six to
nine more legs of work.

**What happens next is not this leg's call.** The result is packaged and handed to the user, who
alone can rule on whether the ban's lift condition has actually been met. Nothing is built past
this point, and the odds on the underlying Clay problem have not moved: they stay at
roughly 0.05%, exactly where they were before this leg started.
