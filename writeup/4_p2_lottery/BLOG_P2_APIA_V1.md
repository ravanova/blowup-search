# the calculator was the artifact

*Route-APIA v1, leg 312. Technical companion: `TECHNICAL_P2_APIA_V1.md`. Data:
`writeup/data/p2_route_apia_v1.json`. Runner: `experiments/p2_route_apia_v1.py`.
Figure: `fig73`.*

*Gate answer: **YES** — arbitrary precision changes both of the two pre-registered
banked headlines it was asked to re-check.*

## the assignment

Two banked numbers in this repository were computed in float64, at the exact spot
where float64 was least trustworthy. Leg 178 measured a coercivity gap that went
from `+0.5` to `−230.71` between one grading refinement and the next, at a quadrature
node where `theta ~ 3e-31`. Leg 176's own ladder of a singular value lost its
`N=1024` row to what its journal calls "a Gram float floor `~1e12`". Both readings
were banked with the honest caveat that they might be measuring float64's own
roundoff rather than the mathematics underneath it.

This leg builds arbitrary-precision interval arithmetic — `solver/interval_mp.py`,
`decimal.Decimal`-backed, directed rounding via `ROUND_FLOOR`/`ROUND_CEILING`,
Taylor-series transcendentals with proved remainders — and re-runs exactly those
two numbers at however much precision the problem actually needs. Nothing else.
Building a general arbitrary-precision library was explicitly not the assignment;
`writeup/novelty/leg_312.md` names seven existing libraries that already do that
(INTLAB, MPFI, mpmath's `iv`, Arb, kv, Boost.Interval, Julia's IntervalArithmetic.jl)
and states plainly why none of them is importable here (dependency ban, and the
question is two named numbers, not a library).

## leg 178: the −230.71 was the calculator failing, not the operator

Leg 178's own instrument finding (`writeup/novelty/leg_178.md`) already suspected
this: the trial-space basis functions at `n_grade=96` are formed as a pointwise sum
`F_m = sum_k V[k,m] sin(k*theta)` designed to cancel to order `theta^3` — and at
`theta ~ 3e-31`, that cancellation needs digits float64 simply does not have. The
`contamination` diagnostic leg 178 built (comparing a roundoff bound against the
signal) already read `3.066e+03` — a roundoff floor exceeding the signal by three
thousand times — and the leg's own ruling treated that as the instrument breaking,
not a finding about the operator.

This leg checks that suspicion directly: patch exactly the `F` computation at the
1,640 quadrature nodes (of 7,824) where the cancellation is severe enough to matter,
using `solver/interval_mp.py`'s rigorous `MPInterval` sin/cos (spot-checked against
an independent plain high-precision recurrence, agreeing to all 120 requested
digits), leave everything else — the quadrature nodes and weights themselves, the
final eigenvalue solve — exactly as leg 178 computed it.

**The gap at `n_grade=96` moves from `−230.7108028` to `+0.4999999875`** — the same
`+0.5` ceiling every other clean depth in leg 178's own ladder reads, to nine
significant figures. The `−230.71` reading was a float64 artifact, full stop; the
mathematics was never in the negative region.

## leg 176: float64 broke a monotone ladder; arbitrary precision restores it

`rect_sigma`'s own docstring states its `sigma_min` should be non-increasing in `N`
— more trial functions, a tighter upper bound. Leg 176's banked `N=1024` reading,
`0.0909363`, is HIGHER than the banked `N=512` reading, `0.0908047` — the ladder's
own monotonicity is violated by the very row leg 176 flagged as suspect.

The precision-losing step is `origin_h2_certificate._sym_sqrt`: a dense
`np.linalg.eigh`-based symmetric square root of a Gram matrix (`x_gram`) whose
condition number reaches `~1e13` at `N=1024`. `x_gram = I + J^4` is exact and
banded (bandwidth 4) — this leg replaces the dense eigendecomposition with banded
Cholesky + banded triangular inverse (both `O(N^2 * bw)`, not `O(N^3)`) at 60
working decimal digits, using the fact that any valid factorisation of the same
inner product (Cholesky, not necessarily the *symmetric* square root) gives the
same singular values.

**`sigma_min` at `N=1024` moves from `0.09093626` to `0.09079113`** — below the
`N=512` value, restoring the expected monotone-decreasing shape. The magnitude
change is smaller than leg 178's (0.16%, not a sign flip), but it is real: the
"lost row" is recoverable, and its corrected value continues the survival-boundary
trend rather than bending it upward.

## what this doesn't do

Nothing here moves a link of the L1→L4 chain. Better arithmetic changed what this
repository could accurately *measure* about two already-banked, already-flagged
exploratory readings — it did not touch the equations either leg's construction is
approximating. Clay odds stay ~0.05%. Both legs whose numbers changed were explicitly
exploratory ("not critical path" per leg 178's own header); this correction, if
anything, strengthens leg 178's own ruling (the instrument really was the thing
that broke) rather than reopening it.
