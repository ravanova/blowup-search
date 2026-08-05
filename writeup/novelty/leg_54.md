# Leg 54 — Route-MM novelty pass (MM-3)

**Date:** 2026-08-05. **Run BEFORE any construction** (this file is committed ahead of
`p2_route_mm_v1_shape.py`). **Verdict: `PROCEED_NARROW`.**

**Links, not counts.** Leg 53's pass logged result counts, could not be audited, and its
resurfacing clearance was withdrawn. Every query below is recorded verbatim with the exact
URLs returned, so a later pass can re-run it and compare.

## The question this pass had to answer

MM-2 proposes the one move left: an approximate inverse `A` for the radii-polynomial /
Newton–Kantorovich framework whose **off-diagonal blocks across the finite/tail split are not
zero** (block Gauss–Seidel step, or the Schur complement of the coupling). Two things needed
checking:

1. **Is the block-diagonal `A = A^N ⊕ π^∞` actually the standing convention**, or have I
   mis-stated the method's requirement? (If non-block-diagonal `A` is routine in this
   literature, MM-2 is a re-derivation, not a move.)
2. **Has anyone applied a radii-polynomial certificate to an operator whose unbounded part is
   off-diagonal (a shift) rather than a multiplier**, which is the structural fact leg 51
   named and legs 52–53 confirmed?

## Queries, verbatim, with links returned

### Q1 — `non-block-diagonal approximate inverse radii polynomial computer-assisted proof Newton-Kantorovich`

- https://arxiv.org/pdf/2604.08715 — localized patterns/periodic solutions, 1D Thomas model
- https://arxiv.org/pdf/2403.18566 — CAPs of existence of invariant tori
- https://arxiv.org/pdf/2404.08529 — 2D Gray–Scott, localized stationary patterns
- https://arxiv.org/pdf/2509.17099 — localized patterns and saddle-node bifurcations, 1D activator–inhibitor
- https://arxiv.org/abs/2605.07500 — Shimizu–Morioka heteroclinic orbit case study
- https://link.springer.com/article/10.1007/s00332-016-9298-5 — (un)stable manifolds with validated error bounds
- https://arxiv.org/pdf/1711.06932 — restricted four-body chaotic motions
- https://arxiv.org/pdf/2502.20644 — rigorous integration of parabolic PDEs, Fourier–Chebyshev
- https://arxiv.org/html/2605.07500 — (HTML of the Shimizu–Morioka paper)
- https://arxiv.org/pdf/2403.10450 — planar Swift–Hohenberg non-radial localized patterns

**Reading.** Every hit uses the radii-polynomial machinery, and the "choice of approximate
inverse" is named as one of the four things the polynomial's coefficients encode — but none of
these returned a construction where the finite/tail off-diagonal blocks of `A` are populated.
The choice being *free* is stated in the literature; the choice being *spent on the coupling*
is not in this result set.

### Q2 — `approximate inverse with nonzero off-diagonal tail block validated numerics ell^1 Fourier`

- https://arxiv.org/pdf/2203.02404 — a posteriori validation of generalized polynomial chaos expansions
- https://arxiv.org/pdf/2203.10340 — triblock copolymers, inverse norm bounds, 4th-order elliptic
- https://arxiv.org/pdf/1408.1578 — directional preconditioner, high-frequency obstacle scattering
- https://arxiv.org/pdf/1906.06767 — quasi-periodic solutions, nonlinear wave equations on T^d
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8591708/ — approximating inverse FEM matrices with H-matrices
- https://arxiv.org/pdf/2411.18361 — validated matrix multiplication transform for orthogonal polynomials, CAPs for PDEs
- https://reference.wolfram.com/language/ref/Inverse — (noise)
- https://arxiv.org/pdf/1503.05671 — K-FAC (noise)
- two US patent PDFs — (noise)

**Reading, and this is the load-bearing one.** arXiv:2411.18361 states the convention
explicitly: for `DF` a compact perturbation of the identity one seeks `A` as a **finite-rank
perturbation of the identity**, `A = A^N + π^∞` — numerically invert the Galerkin projection,
and **let the tail act as the identity**. That is exactly block-diagonal, and it confirms
point (1): the block-diagonal `A` is the convention, not my mis-statement. It also localises
why: the convention is justified by `DF` being a **compact perturbation of the identity**, a
hypothesis our operator does not satisfy (leg 51: the unbounded part is a shift, not a
multiplier). **So the convention's own hypothesis is what fails here** — which is a sharper
statement of the mismatch than "the method requires block diagonal".

### Q3 — `block Gauss-Seidel Schur complement preconditioner computer-assisted proof bordered operator kernel`

- https://arxiv.org/pdf/2410.14918 — interior-point Gauss–Newton, PDE-constrained optimization
- https://link.springer.com/article/10.1007/BF01385611 — Elman/Golub-lineage: block diagonal *vs* Schur complement preconditioning
- https://arxiv.org/pdf/2101.12164 — two-level Nyström–Schur preconditioner
- https://arxiv.org/pdf/1708.09245 — Schur complement preconditioners, multiple saddle-point block tridiagonal
- https://arxiv.org/pdf/1709.10339 — preconditioners for saddle-point problems on truncated domains
- https://arxiv.org/pdf/2011.07410 — multilevel-ILU preconditioning, Newton–GMRES for INS
- https://arxiv.org/pdf/1910.09297 — block preconditioners, Ohta–Kawasaki
- https://www.emergentmind.com/topics/schur-based-methods — survey page
- https://www.researchgate.net/publication/348861334_... — Nyström–Schur (duplicate)

**Reading.** The block-Gauss–Seidel-vs-Schur-complement comparison is completely standard in
**iterative linear algebra / preconditioning** (BF01385611 is the classical statement), and
completely absent from the **validated-numerics** side of the result set. So MM-2 is not a new
idea about matrices — it is the transfer of a textbook preconditioning move into the
approximate-inverse slot of a radii polynomial. **Novelty claim is therefore narrow and I will
state it that way in the writeup: not "a new approximate inverse", but "the standard
preconditioning alternative, measured in the `Z₁` slot, on an operator whose unbounded part is
off-diagonal."** No banked novelty.

### Q4 — `radii polynomial approximate inverse unbounded off-diagonal operator shift transport self-similar blowup`

- https://arxiv.org/pdf/2310.19780 — from instability to singularity formation in incompressible fluids
- https://arxiv.org/abs/1906.05811 — stable self-similar blowup, family of nonlocal transport equations
- https://arxiv.org/pdf/2605.19716 — self-similar blow-up, incompressible Euler in R^d, low-regularity velocity
- https://arxiv.org/pdf/0911.0692 — corotational wave maps / Yang–Mills
- https://arxiv.org/pdf/1010.1768 — 4D energy-critical wave equation
- https://arxiv.org/pdf/1503.02712 — slightly L²-supercritical gKdV
- https://arxiv.org/pdf/2401.00394 — corotational energy-critical wave map, quantized rates
- https://arxiv.org/pdf/0901.4307, https://arxiv.org/pdf/0902.1090 — 4th-order reaction-diffusion blow-up
- https://www.researchgate.net/publication/351671065_... — (duplicate of 1906.05811)

**Reading.** The self-similar-transport blow-up literature that came back is **analytic**
(modulation, fixed-point on a characteristic curve), not computer-assisted-in-`ℓ¹`-Fourier.
No hit combines the two. That is consistent with — but does not prove — the lane being
untravelled rather than travelled-and-abandoned. **Recorded as unchecked, not as a gap**
(the leg 53 correction).

### Q5 — `Lessard Breden "approximate inverse" choice tail block coupling radii polynomial infinite dimensional operator not diagonal`

- https://arxiv.org/pdf/2203.10340 — triblock copolymers, inverse norm bounds
- https://link.springer.com/article/10.1007/s10208-015-9259-7 — smooth manifolds via rigorous multi-parameter continuation
- https://link.springer.com/article/10.1007/s10208-016-9325-9 — Fourier–Taylor unstable manifolds for compact maps
- https://www.math.mcgill.ca/jplessard/Continuation.html — Lessard's continuation page
- https://arxiv.org/pdf/1901.03738 — torus knot choreographies, n-body
- https://arxiv.org/pdf/1906.06767 — quasi-periodic solutions on T^d
- https://doi.org/10.1137/S0036142996304498 — Nakao-lineage numerical verification via Banach fixed point
- https://arxiv.org/pdf/2101.00684 — validated forward integration, parabolic PDEs via Chebyshev
- https://www.researchgate.net/publication/337191286_... — *Computer-Assisted Proofs for Dynamical Systems* (survey)

**Reading.** The phrase that came back is "approximate **right** inverses of **block diagonal**
operators" — i.e. the block-diagonal structure in this literature is a property attributed to
the *operator*, and the approximate inverse inherits it. Nothing in this set constructs an `A`
that couples the finite block to the tail. Confirms Q2's reading from the other direction.

### Q6 — `computer-assisted proof zero diagonal Fredholm operator approximate inverse construction failure Z1 bound`

- https://arxiv.org/pdf/2411.18361 — validated matrix multiplication transform (again; the `A = A^N + π^∞` statement)
- https://arxiv.org/abs/2605.07500 + https://arxiv.org/html/2605.07500 — Shimizu–Morioka case study (the four-step (i)–(iv) procedure)
- https://arxiv.org/pdf/2101.01491 — shear-induced chaos in stochastically perturbed Hopf systems
- https://math.colorado.edu/~alde9049/Talks/Fredholm%20Operators.pdf — lecture notes (background)
- https://gauss.math.yale.edu/~mr2245/func2018Data/fredholm.pdf — lecture notes (background)
- https://people.math.osu.edu/penneys.2/7211/2017/Fredholm.pdf — lecture notes (background)
- https://terrytao.wordpress.com/2011/04/10/a-proof-of-the-fredholm-alternative/ — background
- https://www.cs.cas.cz/~vera/publications/journals/AMC12.pdf — accuracy of approximations to Fredholm equations

**Reading.** The zero-diagonal case still returns only general Fredholm theory, no validated
construction. Consistent with LIT's ninth pass on Breden–Desvillettes–Lessard
(arXiv:1503.06315), whose assumptions (4)–(5) require a diagonal bounded away from zero.
**No change to that flag's status from this pass.**

## Standing flags — status after this pass

- **Leg 52's search-index flag (`arXiv:2604.01868` not resurfacing): STANDS.** This pass did
  not test it (it is LIT's, and leg 53 was withdrawn for testing it the wrong way — by ID
  rather than topically). Not touched, not cleared.
- **BDL (`arXiv:1503.06315`): CLOSED by LIT's ninth pass**, from the full PDF. Nothing here
  reopens it.
- **Whether the literature treats an *off-diagonal* unbounded part: still UNCHECKED**, not a
  gap. Q4 and Q6 both failed to surface anything either way, and absence in two web-search
  result sets is not a literature review.

## Verdict

**`PROCEED_NARROW`.** MM-2 is worth running and is not a re-derivation, but the novelty on
offer is small and precisely bounded: *the block-diagonal approximate inverse is the
convention (arXiv:2411.18361 states it), its stated justification is compactness-relative-to-
the-identity, our operator violates that hypothesis, and the standard preconditioning
alternatives (block Gauss–Seidel, Schur complement) have not been measured in this slot.*
**Nothing is banked as novel by this leg.** Whatever the gate answers, the claim in the
writeup is a measurement on a known object, not a new method.
