# Leg 83 — Route-MFG novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-J. **Branch:** `leg/mfg-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics, measures no new gCLM
physics, and claims no novel mechanism. It stress-tests one predicate — the `converged` flag
`solver/marginal_flow.py:integrate` returns, which `capabilities.py` line 85 records as
*"`integrate` reports `converged` and gate 11 enforces it (the NaN of leg 41)"* — against
divergent trajectories that never produce a NaN.

Per `writeup/novelty/README.md`: **links, not counts.** Every query string below is verbatim and
every returned link I judged on-topic is listed.

**Ban check, done first and recorded.** `plan_of_record.py` bans *"another gCLM measurement
leg"*, permanently. This leg runs no parameter sweep, computes no profile, and reads no new
number off the gCLM model: the objects under test are synthetic trajectories constructed to
have a known analytic form, pushed through the *existing* integrator's *existing* validity
predicate. The two live-solver runs it does perform are byte-for-byte the two already in
`test_marginal_flow.py::test_11` and are used only as harness controls, not as measurements.
`solver/marginal_flow.py` is **read-only** under this leg, under either gate outcome. Also
checked: *"building a solver without grepping capabilities.py for the object first"* — grepped,
line 82–86, quoted above, and that line is the exact claim being audited.

---

## What is being checked for prior art

* **(N1)** Is "an implicit ODE integrator's success flag does not certify that the trajectory
  stayed bounded" a known, documented distinction in production solver software — i.e. is the
  gap shape this leg is looking for a *documented hazard* rather than a discovery?
* **(N2)** Is a Newton-residual-based discriminator (the `worst_newton_residual_over_floor <
  1e8` clause) known to be *insufficient* as a divergence detector, and is the interaction
  between a stagnation stop and an accepted step documented?
* **(N3)** How does the blow-up literature actually detect unbounded growth, and does it use
  anything the integrator's own inner solve can see?
* **(N4)** Is "inject synthetic failure-mode inputs through the real code path to measure a
  validity gate's catch coverage" a standard testing method?

---

## Queries, verbatim, with the links returned

### Q1
`stiff ODE solver silent failure convergence criterion blow-up detection unbounded solution finite time`

- https://people.sc.fsu.edu/~jburkardt/classes/math1902_2020/stiff/stiff.pdf — Burkardt, backward
  Euler and implicit solvers for stiff ODEs.
- https://docs.sciml.ai/DiffEqDocs/stable/solvers/ode_solve/ — DifferentialEquations.jl solver
  documentation and return codes.
- https://reference.wolfram.com/language/tutorial/NDSolveStiffnessTest.html — `NDSolve` stiffness
  test; treats stiffness as a *transient, finite-interval* property.
- https://people.maths.ox.ac.uk/trefethen/publication/PDF/1993_56.pdf — Söderlind/Trefethen-school
  *Stiffness of ODEs*, BIT 33 (1993) 285–303.
- https://www.mathworks.com/help/matlab/math/solve-stiff-odes.html — MATLAB stiff-solver guide.
- https://arxiv.org/pdf/2204.08621, https://arxiv.org/pdf/2505.24210 — adjacent (implicit solvers
  for neural ODEs; stiffness in flow-matching samplers), retained for the record.

**On-topic finding for (N1), partial.** The literature is clear that stiffness and instability
are *transient* phenomena on finite intervals, which is precisely the regime in which an
integrator can complete every step successfully while the solution goes somewhere useless.
Nothing here states the sharper software claim; that came from Q2.

### Q2
`SUNDIALS CVODE return flags convergence failure "too much work" solver success flag does not guarantee solution bounded`

- https://sundials.readthedocs.io/en/latest/cvode/Usage/index.html — CVODE usage and return flags
  (`CV_SUCCESS`, `CV_CONV_FAILURE`, `CV_TOO_MUCH_WORK`).
- https://sundials.readthedocs.io/en/latest/cvodes/Mathematics_link.html — CVODES mathematical
  considerations, including the **inequality-constraint** mechanism.
- https://github.com/LLNL/sundials/blob/main/src/cvode/cvode.c — the implementation.
- https://computing.llnl.gov/projects/sundials/usage-notes — SUNDIALS usage notes.
- https://inria-parkas.github.io/sundialsml/Cvode.html — Sundials/ML binding, flags enumerated.
- https://github.com/bmcage/odes/issues/118 — a field report of non-convergence in practice.

**On-topic finding for (N2), and the sharpest in this pass.** SUNDIALS treats "the nonlinear
solve converged" and "the solution is admissible" as **two separate tests**: constraint
satisfaction is checked *after* a successful nonlinear solve, and only then is a convergence
failure declared. That is an explicit, in-production acknowledgement that a converged inner
Newton solve does **not** certify the state — the state needs its own, separate predicate. The
repository's `converged` flag has only the first test (finiteness, no NaN break, Newton residual
over floor) and no analogue of the second. This is the precise hole the construction will probe,
and it means any miss found here is a **known hazard present in our code**, never a discovery.

### Q3
`numerical detection of finite-time blow-up ODE rescaling algorithm distinguishing blow-up from slow growth`

- https://arxiv.org/pdf/1502.03250 — *Adaptivity and blow-up detection for nonlinear evolution
  problems*.
- https://link.springer.com/article/10.1007/s13160-015-0198-0 — *Numerical detection of blow-up:
  a new sufficient condition for blow-up*, JJIAM.
- https://link.springer.com/article/10.1007/s11075-024-01791-2 — convergence of the numerical
  blow-up time for a rescaling algorithm (Berger–Kohn lineage).
- https://arxiv.org/html/2603.12957 — *A priori adaptive numerical methods for estimating blow-up
  times of autonomous ODEs*.
- https://www.sciencedirect.com/science/article/abs/pii/S016727891630447X — numerical analysis of
  the rescaling method for parabolic blow-up.
- https://www.researchgate.net/publication/257797453_On_the_computation_of_the_numerical_blow-up_time,
  https://www.researchgate.net/publication/309306932_A_numerical_algorithm_for_blow-up_problems_revisited —
  the two standard "numerical blow-up time" papers.

**On-topic finding for (N3).** Every published blow-up detector is a predicate **on the state or
on the time series** — a rescaling of the solution's own amplitude, a sufficient condition
evaluated on the numerical solution, an adaptive tolerance keyed to the growing magnitude. Not
one of them is a property of the inner nonlinear solve. So the literature's answer to "how do you
detect unbounded growth" and the repository's `converged` predicate are looking at different
objects entirely. That is a *prediction*, made before construction, about which battery members
will slip through.

### Q4
`metamorphic testing scientific numerical software oracle problem validity check adversarial synthetic failure injection`

- https://en.wikipedia.org/wiki/Metamorphic_testing — the method, and the test-oracle problem it
  addresses.
- https://arxiv.org/pdf/2310.00338 — *Towards a Complete Metamorphic Testing Pipeline*.
- https://arxiv.org/pdf/2605.17437 — a semantic mutation metric for metamorphic-relation adequacy
  **in scientific computing programs**.
- https://arxiv.org/html/2606.17529 — *Domain-Validity-Gated Metamorphic Testing of Scientific ML
  Surrogates*; the closest framing to this leg's, in that the *validity gate itself* is the object
  under scrutiny.
- https://arxiv.org/pdf/2109.09798 — metamorphic-relation prioritization for regression testing.
- Content-moderation MT papers (https://arxiv.org/pdf/2509.24215,
  https://arxiv.org/pdf/2302.05706) and the NIST cybersecurity MT note
  (https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=920197) — returned, off-domain, listed
  for completeness.

**On-topic finding for (N4).** Injecting inputs with known ground-truth classification through
the real code path to measure a checker's catch rate is standard practice with published
precedent. Not novel and not presented as such here.

### In-repository prior art

Searched the tree for any existing adversarial exercise of this predicate:
`grep -rln "marginal_flow"` over `experiments/*.py` and `test_*.py` returns exactly two files —
`experiments/p2_route_i_v1_driven.py` (which *consumes* `rec["converged"]` at lines 248–272 and
records a refusal) and `test_marginal_flow.py` (whose `test_11` is the gate itself). `test_11`'s
only divergent input is the naive-perturbation trap of leg 41, which ends in a **NaN**. So the
non-NaN cases have never been run, exactly as the leg's thesis states.

---

## What this pass settles, before any code is written

1. **No novelty is available and none will be claimed.** If the gate misses a case, the finding
   is *"a distinction that production ODE software (SUNDIALS) makes explicitly and this
   repository's predicate does not"* — not a discovery.
2. **It sharpens the construction and makes a falsifiable prediction.** Q2 and Q3 together say
   the predicate is built entirely from *inner-solve* observables while every published
   divergence detector is built from *state* observables. Prediction, recorded before
   measurement: the battery members whose inner Newton stays well-conditioned — smooth
   polynomial growth, and a pure rotation — will be classified `converged = True` despite
   diverging, and the NaN control will be caught. The battery is built to make that prediction
   falsifiable by including members that are hard on the inner solve too.
3. **The severity question is separated from the catch question, in advance.** A miss matters
   only if it can reach a banked number, so the battery carries a live-solver control section
   measuring what the real `AugmentedFlow` trajectories actually do — so that a "miss" is
   reported with its blast radius attached rather than as a bare alarm.
