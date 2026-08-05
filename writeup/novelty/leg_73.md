# Leg 73 — Route-BV novelty pass (run BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-G, leg 73. **Branch:** `leg/bv-v1`.
**Verdict: `PROCEED_AS_KNOWN_ANSWER_CHECK`.** This leg builds no new mathematics and claims no
novel mechanism. It runs the existing `solver/boussinesq_velocity.py` against a closed form that
someone else published, and reports the magnitude of the disagreement. The pass below exists to
establish, *before* construction, **what is already in print**, so that whatever this leg
measures is reported as *"our code against a published answer"* and never as a discovery.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim, and every link returned that I judged on-topic is listed. Where a
search returned nothing on-topic I say so rather than reporting a number.

---

## What is being searched for

The module solves, on a log-radial × angular-sine polar grid over the first quadrant,

    -Lap phi = omega  on {r>0, beta in (0, pi/2)},   phi = 0 on beta = 0 and beta = pi/2,
    u = -phi_y,  v = phi_x,

with Robin radial closures `phi_n ~ r^{+2n}` at `r_min` and `phi_n ~ r^{-2n}` at `r_max`
(`poisson_solve(..., radial_bc="robin")`). `capabilities.py` records its validated line as
*"manufactured stream-function solutions; the Route-L line sweep is gated to 9.5e-16 against the
operator it inverts"* — i.e. **pick phi, differentiate to get omega, check phi comes back**, plus
one self-consistency gate. Both are internal.

The pass therefore asks four questions:

* **(N1)** Is there a **published closed-form solution** of the Biot–Savart / stream-function
  problem in which the **vorticity is prescribed** (not back-derived from a chosen `phi`)?
* **(N2)** Is there a published closed form for the **quarter-plane with Dirichlet data on both
  rays** — i.e. a benchmark whose *content is the boundary condition*, which a manufactured
  solution with hand-imposed Dirichlet data cannot test?
* **(N3)** Does **Chen–Hou / Chen–Hou–Huang** (the natural first place to look, since
  `solver/boussinesq_rescaled.py` already reproduces their `beta`) publish a **velocity-solve
  accuracy table** that could be hit directly?
* **(N4)** Is the *method* — validating a polar/log-radial Poisson solver against an externally
  published closed form — standard practice, or would this leg be inventing a protocol?

---

## Queries, verbatim, with the links returned

### Q1
`Lamb-Oseen vortex exact azimuthal velocity benchmark Biot-Savart Poisson solver validation`

- https://en.wikipedia.org/wiki/Lamb%E2%80%93Oseen_vortex — the Lamb–Oseen vortex, with the
  azimuthal velocity `v_theta(r) = (Gamma/2 pi r)(1 - exp(-r^2/(4 nu t)))` and the Gaussian
  vorticity that generates it. **Answers N1 affirmatively:** vorticity is prescribed, velocity
  is the published consequence.
- https://www.sciencedirect.com/science/article/pii/S0898122115001832 — *Numerical simulation of
  2D-vorticity dynamics using particle methods*. Uses the Lamb–Oseen exact solution to evaluate
  relative errors in **both vorticity and velocity** for a Biot–Savart evaluation. **Answers N4:**
  this is the standard first benchmark, not a protocol this leg invents.
- https://arxiv.org/pdf/1010.2475 — *A multi-moment vortex method for 2D viscous fluids*; states
  Lamb–Oseen as "the only known nontrivial, analytic solution to the vorticity equations" and
  uses it as the first spatial-accuracy benchmark.
- https://arxiv.org/pdf/1810.04646 — *The Lamb-Oseen Vortex and Paint Marbling*; independent
  restatement of the closed form.
- https://www.diva-portal.org/smash/get/diva2:205082/fulltext01.pdf — *Analytical Vortex Solutions
  to the Navier-Stokes Equation*; catalogue of the closed forms, Lamb–Oseen among them.
- https://www.researchgate.net/figure/Lamb-Oseen-vortex-test-Gaussian-blobs-s-0025-h-s-07-and-N-2177-t-001-M-4_fig1_228720059
  — a published "Lamb-Oseen vortex test" with Gaussian blobs of core `sigma` used exactly as a
  solver-verification case.

### Q2
`vortex in a right-angled corner image system Lamb Hydrodynamics hyperbola trajectory closed form`

- http://brennen.caltech.edu/fluidbook/basicfluiddynamics/potentialflow/singularities/images.pdf
  — Brennen, *An Internet Book on Fluid Dynamics*, "Images and Walls": the image vortex must be
  of **opposite sign** to make the wall a streamline. The half-plane half of the construction.
- https://www.math.unm.edu/~nitsche/pubs/2006EMP.pdf — Nitsche, *Vortex Dynamics* (Encyclopedia of
  Mathematical Physics, 2006); the standard survey statement of the method of images for point
  vortices near boundaries.
- https://archive.org/details/hydrodynamics00horarich — Lamb, *Hydrodynamics* (1895/1932), the
  primary source for the corner-vortex image system (Art. 155, "vortex in a corner"); scan
  available but not machine-readable through this pass, so it is cited, not quoted.
- https://estebanhufstedler.com/2020/06/30/conformal-mapping-point-vortex-near-a-corner/ —
  *Conformal Mapping: Point Vortex Near a Corner*. **Fetched and read in full.** It gives the
  conformal-map route (`z = c^{pi/(2 alpha)}`, so `z = c^2` for a right angle) and the pathline
  `r_v^k = x_0^k / cos(k theta_v)`. It does **not** state the three-image system nor cite Lamb or
  Greenhill, so it corroborates the *geometry* only; it is not the citation this leg leans on.

### Q3
`"point vortex" quarter plane "three images" self-induced velocity "1/x^2" "1/y^2" invariant classical result`

- https://arxiv.org/pdf/1301.6245 — Crosby, Johnson & Morrison, *Deformation of vortex patches by
  boundaries*, Phys. Fluids 25 (2013). **Fetched and read (ar5iv HTML; the raw PDF is
  FlateDecode-compressed and unreadable through WebFetch).** Section IV is exactly the
  quarter-plane case: *"the method of images ... requires two reflections, one in y = 0 and one in
  x = 0, creating three image patches, two of which have opposite vorticity to the original."*
  Eq. (14) gives the corner Hamiltonian with its `ln(2 x_c y_c / sqrt(x_c^2 + y_c^2))` term — the
  same function whose gradient is the corner-image velocity this leg checks. **Answers N2:** the
  quarter-plane three-image construction is published, peer-reviewed, and independent of this
  repository.
- https://arxiv.org/pdf/1308.1010 — *Integrable two layer point vortex motion on the half plane*;
  the half-plane image reduction, one reflection.
- https://arxiv.org/pdf/2504.20089 (`Learning the Position of Image Vortices from Data`) —
  on-topic only as further evidence the image construction is textbook.
- https://www.whoi.edu/cms/files/Vener_21367.pdf — *Two-dimensional Vortex Shedding From a
  Corner*; corner geometry, but the shedding problem, not the closed-form image velocity.

### Q4
`Greenhill 1878 vortex in a right angle corner three images trajectory x^-2 + y^-2 constant Lamb Hydrodynamics article 155`

- https://numdam.org/item/AFST_1887_1_1_4_57_0/ — *Questions d'hydrodynamique* (Ann. Fac. Sci.
  Toulouse, 1887), in the same classical lineage.
- Greenhill's own 1878 *Messenger of Mathematics* VIII note on fluid motion in a quadrantal
  cylinder was identified by name but **no digitised full text was returned**. Recorded as a
  located-but-unread primary source; the leg does not quote it.

### Q5
`Chen Hou Huang 2D Boussinesq self-similar blowup numerical validation table stream function Poisson solve accuracy benchmark arXiv 2210.07191`

- https://arxiv.org/abs/2210.07191v3 — Chen & Hou, *Stable nearly self-similar blowup of the 2D
  Boussinesq and 3D Euler equations with smooth data I: Analysis*.
- https://arxiv.org/pdf/2305.05660 — Part II, *Rigorous Numerics*.
- https://authors.library.caltech.edu/records/n8p3w-pkt03 — Part II, published record.
- https://jiajiechen94.github.io/research — Chen's research page, for the surrounding series.
- **N3 answers NEGATIVE.** What Part II publishes is rigorous error control on *their* space-time
  solution in *their* B-spline FEM discretisation, keyed to their own profile and their own
  weighted norms. There is no free-standing "given this omega, phi and u are these numbers" table
  that a different discretisation can be scored against, and the one number this repository
  already matches (`beta`, to 2.1%) is **banned by the plan of record** (`re-measuring beta on the
  2D object`, lifted by: never). So Chen–Hou is *not* the source of this leg's benchmark. It is
  ruled out here, on the record, rather than left as an unexamined "first place to look".

### Q6
`polar coordinates log-radial grid Poisson solver benchmark exact solution quarter plane Dirichlet manufactured versus published known answer`

- https://arxiv.org/pdf/1806.06623 — *An FFT-based Solution Method for the Poisson Equation on 3D
  Spherical Polar Grids*; **log-radial grid**, open boundary conditions, verified against the
  analytic point-source solution along coordinate lines. Closest published sibling of this
  module's grid, but spherical and open-boundary — not the quarter-plane Dirichlet case.
- https://arxiv.org/pdf/2507.06784 — *A Fast, Second-order Accurate Poisson Solver in Spherical
  Polar Coordinates*; same verification pattern.
- https://www.damtp.cam.ac.uk/user/reh10/lectures/nst-mmii-chapter2.pdf — standard Poisson /
  Green's-function reference for the image construction.
- **Nothing on-topic** was returned for a *published, canonical, named* benchmark case for the
  planar quarter-plane log-polar Dirichlet Poisson solve specifically. That gap is stated plainly
  below rather than papered over.

### Q7
`"method of images" Lamb-Oseen Gaussian vortex near wall exact stream function exponential integral E1 validation of Poisson solver`

- https://guilindner.github.io/VortexFitting/methodology.html — Lamb–Oseen as the fitted reference
  profile in a production tool.
- https://arxiv.org/pdf/1610.00599 — *Vortex generated fluid flows in multiply connected domains*;
  the images-in-a-domain machinery.
- https://fenix.tecnico.ulisboa.pt/downloadFile/3779572191888/vortex.pdf — *A Stochastic
  Lamb-Oseen Vortex Solution of the 2D Navier–Stokes*; restates the closed form.
- **Nothing on-topic** returned for the specific composite (Oseen core + corner images, stream
  function in terms of `E_1`) as a *named published test case*. Recorded as negative.

---

## What the pass concludes, stated at the strength the evidence supports

**The gate's "does a published, independent benchmark exist" answers YES, and the honest
description of it is an assembly of two published closed forms, not a single named benchmark
case.** Specifically:

1. **Lamb–Oseen** (Q1) supplies a **prescribed vorticity** with a published velocity — the exact
   inverse of a manufactured solution, where `phi` is picked first. This is the standard first
   verification case for Biot–Savart/Poisson solvers (Q1, five independent uses).
2. **The corner image system** (Q3, Q4) supplies the **boundary-condition content**: for a vortex
   at `(a,b)` in the quarter plane, `phi = 0` on both rays is enforced by three images at
   `(-a,b), (a,-b), (-a,-b)` with signs `-,-,+`, and the induced velocity at the vortex is a
   published closed form. Crosby–Johnson–Morrison Eq. (14) states this construction in a
   peer-reviewed venue; Lamb Art. 155 is the primary source.
3. What is **not** published, and is stated as such: nobody has named "Oseen blob in a
   right-angled corner on a log-polar grid" as a canonical benchmark (Q6, Q7 both negative). This
   leg assembles it from (1) and (2).

**Why this is a genuinely external check and not another manufactured solution** — three reasons,
each falsifiable:
* The **vorticity is prescribed**, and `phi` is a consequence. Nothing is reverse-engineered from
  a chosen `phi`.
* The **target number is not ours**. The corner-image velocity at the vortex centre is a classical
  published closed form. It is a *difference* of image contributions — a quantity that exists only
  because of the two Dirichlet rays, and that no manufactured solution with hand-imposed Dirichlet
  data can test.
* The **far-field Robin closure is under test, not assumed**. The four-vortex system has zero net
  circulation, so its leading far field is a quadrupole `~ sin(2 beta)/r^2`, and each higher
  angular mode `n` decays as `r^{-2n}`. That is *exactly* what `radial_bc="robin"` imposes, so if
  the closure is modelled wrongly the benchmark sees it. The `"dirichlet"` radial mode — the one
  the existing manufactured tests use, which is *handed* the answer at both radial ends — is
  deliberately **not** used for the headline number.

**Novelty claim of this leg: none.** The mathematics is Lamb's. The contribution is a measurement:
the magnitude of the gap between `solver/boussinesq_velocity.py` and that published closed form.

---

## Pre-committed tolerances (fixed HERE, before any code is written or run)

The refinement ladder is `(n_r, n_beta) = (601, 49), (1201, 99), (2401, 199)` on
`r in [1e-3, 1e3]`, blob at `r0 = 1`, `beta0 = 0.7 * (pi/2)`, Gaussian core `d = 0.25`,
circulation `Gamma = 1`, `radial_bc="robin"`. The blob centre sits **exactly on a grid node** at
every level, so no interpolation enters the headline read.

* **P1 (headline).** Relative error of the computed velocity vector at the blob centre against the
  corner-image closed form, `||u_num - u_exact|| / ||u_exact||`, is **<= 1e-2 at the finest
  level**.
* **P2 (convergence).** That error **decreases monotonically** along the ladder with an observed
  order **>= 1.5** (the scheme is nominally second order: central differences in `rho`, spectral
  in `beta`).
* **P3 (field).** Relative `L2` error of `phi` itself against the exact four-blob stream function,
  over `r in [0.1, 10]`, is **<= 1e-3 at the finest level**.

**Reading rule, fixed in advance so the outcome cannot be re-argued afterwards.** P1 and P3 are
*accuracy* statements and P2 is the *correctness* statement. A miss on P1/P3 while P2 holds at
order `>= 1.5` is a **resolution** finding, reported with its magnitude and its Richardson
extrapolate, and is **not** the gate's "disagrees" branch. A failure of **P2** — no convergence,
or convergence to the wrong limit — **is** the "disagrees" branch, and under it this leg escalates
and does not patch `solver/boussinesq_velocity.py` under its own authority.
