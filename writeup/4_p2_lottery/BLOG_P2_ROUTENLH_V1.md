# The machinery does hold a nonlocal operator. It just can't see where it breaks.

*Leg 331, Route-NLH. float64, not interval arithmetic — everything below is a magnitude,
not an enclosure.*

## The question we had been answering by reading

Breden and Chu built a computer-assisted proof machine for semilinear PDEs on a weighted
Sobolev space `H^2(mu)` with `mu = e^{|x|^2/4}`. Their Remark 40 says, in effect, what the
method is for. Twenty-one times in this project — 18 fluid rows in leg 261, 3 non-fluid
rows in leg 311 — we killed a candidate object because it was nonlocal, and every one of
those kills cited Remark 40's two nonlocality reasons.

Not one of them cited a measurement. Nobody had ever pointed the machine at a nonlocal
operator and looked at the numbers. And every fluid object is nonlocal: Biot–Savart *is*
the nonlocality. So the whole question of whether a fluid certification path exists was
resting on a reading of a remark.

This leg does the experiment.

## Changing exactly one letter

Their equation (54) is a self-similar Burgers profile. We changed one letter:

    L u - u/4 + u^2 W_t u = 0,    W_t = (1-t) d_x + t (-Delta)^alpha

The parameter `t` slides from their operator to a nonlocal one. At `alpha = 1/2` the
nonlocal operator is the Hilbert transform composed with a derivative — the same object
that sits at the heart of every 1D fluid model in this repository.

The point of the slider is that `t = 0` has a known answer. If our code doesn't reproduce
Breden–Chu's own published bounds exactly at `t = 0`, we have learned nothing about `t > 0`.
It does: all eight bounds — `Y`, `Z1`, `Z2`, `Z3` and the four `Zbar` components — agree
with their solver to relative difference **0.0**, exactly, at every resolution and every
`alpha` we ran. That control could have come out differently, and checking it is most of
the work.

It also caught us being wrong. The first version of the nonlocal operator used a Fourier
identity that looks right and is false — their basis functions carry `e^{-y^2}`, not the
`e^{-y^2/2}` of true Hermite functions, so their Fourier transform is a *monomial*, not
another Hermite polynomial. The `alpha = 0` sanity check flagged it immediately: mode 0
exact to fifteen digits, every other mode wrong by 100%, and the error didn't move when we
tripled the resolution. Resolution-independent error is structural error. We fixed the
derivation, and the same check then read 4e-15.

## What we found

**The nonlocal operator throws its input out of the space.** The fractional Laplacian's
symbol is non-smooth at the origin, and that forces the output to decay *algebraically*
in `x`, where the local derivative decays like a Gaussian. We predicted the exponent
`1 + 2alpha` in advance and measured 1.5077, 2.0122, 2.5179 against predictions 1.5, 2.0,
2.5. Now put an algebraically-decaying function inside a norm that multiplies by
`e^{x^2/4}`. Measured, as we widen the window:

| window `|x| < R` | 4 | 8 | 12 | 16 |
|---|---|---|---|---|
| nonlocal | 0.97 | 1.2e3 | 5.9e10 | **1.9e22** |
| the local control | 0.954 | 0.99999948 | 1.0000000000 | 1.0000000000 |

The control settles down to 1 and stays there. The nonlocal one has no limit at all.

**And yet the machine returns finite numbers.** That is the interesting part. It returns
them because its quadrature rule has a largest node, and it simply never looks past it.
At the resolution Breden and Chu actually published — `n = 1500` — that horizon sits at
`x = 119.7`, and the quantity the machine is implicitly claiming is finite is about
**10^1546**. It overflows double precision by a factor of 10^1238. Refining the
computation makes this *worse*, because a finer grid pushes the horizon further out into
the divergence.

So the honest answer to "does it produce finite bounds?" is: yes, and the finiteness is
an artefact of where it stops looking.

**The failure has a signature inside their own bounds.** Breden and Chu need a contraction
constant `Z1 < 1`; above 1 their radii polynomial has no root at all and nothing is proved.
We slid the nonlocality up and bisected the crossing to six decimal places. The machine
tolerates somewhere between 30% and 52% of one nonlocal operator, depending on `alpha` and
resolution, and then leaves the admissible region.

And when it fails, it fails through exactly the two component bounds we had flagged, before
running anything, as the ones whose derivations quietly assume locality. The two we had
graded "derivation-free" never misbehave.

## What did *not* break, which matters just as much

We expected the sup-norm route to blow up. It doesn't — the relevant series converges to
1.24 against 0.86 for the local control. We also predicted a specific failure mode in the
tail estimator going negative. It never did. Both are recorded as our own predictions,
refuted. Anyone attacking this next should not spend a week re-deriving the bound that
turned out to be fine.

## The finding that actually changes the map

The obstruction is real and it is now measured rather than inferred. But it is **not** the
obstruction Remark 40 names.

What kills this is not nonlocality as an abstract property. It is the collision between an
algebraic tail and a Gaussian weight. `e^{|x|^2/4}` is a very aggressive weight; it is what
makes the local theory so clean, and it is precisely what a nonlocal operator cannot
survive. That is a statement about the *weight*, not about the operator class — and it
reframes the question for the twenty-one rows we killed. The right question is not "is this
object nonlocal?" It is "which weight tolerates an algebraic tail?" A Gaussian one
demonstrably does not.

We are not adjudicating what that means for the (iv_a) screen or for the certification path
— that is the decision-maker's call, and this leg routes it there rather than deciding it.
What we can say is that the twenty-one kills now stand on a measurement, and that the
measurement points somewhere slightly different from the reasoning that produced them.

---

*Figure `fig85`; data `writeup/data/p2_route_nlh_v1.json`; runner
`experiments/p2_route_nlh_v1.py`; full detail in `TECHNICAL_P2_ROUTENLH_V1.md`. No ban was
lifted, no result rewritten, and nothing here is a claim about the Clay problem.*
