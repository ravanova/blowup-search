# The corner we said we'd already checked

*Leg 162, Route-CAPG. Figure: `fig64_route_capg_v1.png`. Data:
[`p2_route_capg_v1_corner.json`](../data/p2_route_capg_v1_corner.json).*

Six legs ago this project banked a completeness audit. Stage `B` — "evolve the certificate:
the function space, the operator split, the constants" — had failed on all three of its
degrees of freedom, and leg 126 went through the whole declared search space configuration by
configuration to check that nothing was left. It enumerated 1,686 of them and found **zero
uncovered**. That is a strong claim, and it was made carefully.

This leg was sent to poke at one specific corner that a review thought had never been tried:
a certificate written not on the compactified whole line, where every previous attempt lived,
but in a **global Chebyshev basis on the finite interval a compactly supported profile
actually occupies**. Two things came out of it, and the first one is embarrassing in a useful
way.

## The corner had been tried. By us.

Before writing any code, the novelty pass grepped the repository. `solver/first_integral.py`
already reduces the profile to its own support and expands it in an even Chebyshev series
with the finite Hilbert transform. `solver/reduced_certificate.py` already assembles three of
the four certificate constants in exactly that basis. `solver/finite_support.py` was the
first attempt at it, and is marked superseded.

So the premise the leg was launched on was wrong. But one line in
`reduced_certificate.py` explained why the corner had still never been *settled*:

> **(4) `Z_1` IS NOT COMPUTED.** It is the infinite-dimensional tail — the part of the
> operator outside the `K`-mode subspace — and it is the whole content of a real
> computer-assisted proof.

Three constants had been measured. The one that decides had not. That became the leg.

## One operator, two coordinate systems, opposite answers

Here is the thing that makes this corner interesting, and it is not what anyone expected.

"A global Chebyshev basis on the support interval" sounds like one choice. It is two. The
quantity a certificate lives or dies by, `Z_1`, is a *norm* — and it is a norm on a chosen
pair of coordinates. The compact-support problem admits two natural pairings, and **the same
operator classifies oppositely in them**:

- In this repository's own ansatz — perturbations shaped like `(1−v²)·Chebyshev` — the
  unbounded part of the operator is a **shift with an exactly zero diagonal** and
  off-diagonal entries growing like `n/2`. That is precisely the shape, and precisely the
  `n/2`, that killed every whole-line attempt. Same disease, new basis.
- In the *airfoil* pairing that Olver and Townsend use for singular integral equations —
  perturbations shaped like `√(1−v²)·Chebyshev-U` — the unbounded part is an **exact
  diagonal**, `diag(−n)`. That is the shape in which the standard tail estimate simply works.

We have a lesson banked in this project that says a certification method has a shape, and the
shape is a property of the *operator*. This leg is a friendly amendment: the shape is a
property of the operator **and the pairing you write it in**. One operator, one classifier,
two labels.

Why the difference? The first integral. On the whole line the unbounded part is a
*degenerate transport* term, and its degeneracy is why a direct build never converged. The
first integral integrates the transport away and leaves a plain derivative — and the first
integral is available only because the profile has compact support in the first place.

## And the number

Measured in exactly the convention leg 54's battery used — `Z_1 = colmax(I − AL)`, with an
approximate inverse built from the tail's own diagonal and never from inverting the truncated
tail — the airfoil realization gives **`Z_1` under 1**. `0.274` for the plain block-diagonal
approximate inverse; `0.087` for the block-upper-triangular one. It is stable to `0.19%`
under an eightfold refinement of the truncation.

Both of those have `A21 = 0`, which is the class leg 58 closed *as a theorem*: `Z_1 ≥ 1`,
always. There is no contradiction, and the file that proves the theorem is the file that says
why. The proposition needs the tail block to have a kernel — its proof sets `x = (0; h)` with
`Th = 0`. The airfoil tail is `diag(−n)`. It has no kernel. The hypothesis fails, exactly the
way it fails when you turn on dissipation in leg 58's own control. The theorem is untouched.
It just does not reach here.

## What we did to try to kill it

This is the branch of the gate that reverses a banked claim, so the list matters more than
the number.

An early draft asserted a closed form for one of the two Hilbert blocks. Checking it against
direct quadrature gave an error of **0.617** — the claim was false, and the reason is itself
the finding: the airfoil class is closed under the finite Hilbert transform and this
repository's own ansatz is not. A numerical projector replaced it, gated against the one
family whose answer is exactly known.

The assembled matrix was then gated against a direct pointwise evaluation of the operator.
It agreed to `3.4e-04` — but only after a second mistake was caught. The first version of
that gate reported a stubborn `1.1%` error that **did not move** across an eightfold
refinement of its quadrature. That invariance was the tell: the gate was measuring its own
pointwise series reconstruction, not the matrix.

The free boundary went in. The support radius here is not data — it is solved for, and a
`Z_1` measured without it is the failure mode this project has already paid for once, where
four terms were bounded one at a time and a fifth, which only exists after assembly, was the
one that decided.

And the caveat that travels with the number: **`Z_1 < 1` holds at two of four border gauges,
not all four.** A certificate designer does get to pick a gauge, so that is a restriction
rather than a refutation — but the number is never quoted without it.

## What this is not

`Z_1` is one of four constants, and **this is not a certificate**. `Z_2` was already measured
*infinite* on this very object in the sup realization, and its finiteness needs `a ≤ 1/2` —
which is why the sub-1 values inside that range (`0.737` at `a = 0.5`) matter more than the
prettier ones outside it. Everything here is float64 with no interval arithmetic.

And the object is the gCLM profile on `0 < a < 1` — **not** the target this project is
actually aimed at. That matters for how the completeness claim should be read, and it is the
honest complication in this leg. Leg 126's audit was written on the `a = 0` CLM linearisation,
whose profile decays like `1/X` forever. We measured that: decay exponent `−1.0000`, mass
outside any radius never reaching zero. There is no finite interval to put this basis on.
`first_integral.py` will not even construct at `a = 0`; it raises, and the message says *"the
degenerate limit … has no support."*

So there are two defensible readings of the same measurements. Either leg 126 declared a
space complete that had a fourth value on one of its axes — or leg 126's audit was always
scoped to an object on which this corner is empty. Both are honest. Choosing between them is
not a thing a leg gets to do to its own result, so this one is parked for a human.

No link of the L1→L4 chain moved. None has moved in 161 legs.
