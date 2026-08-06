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

---
---

# TECHNICAL NOTE — Route-MFG v1: gate 11 catches 1 of 9 non-NaN divergent trajectories

*This section is the leg's required findings note. It is carried here rather than in a
standalone `writeup/4_p2_lottery/TECHNICAL_*.md` because the leg's declared file territory does
not include that path; the quartet permits either location. **The orchestrator should promote it
if it wants a citable document.***

## Gate, verbatim, and the answer

> "Under an adversarial battery of non-NaN divergent trajectories (slow polynomial blowup,
> sustained non-decaying oscillation), does gate 11 correctly flag non-convergence, or does it
> only catch the NaN case it was built for?"

**NO — it misses 8 of the 9 scored divergent trajectories.** The one it catches is the
finite-time blowup, i.e. the NaN case it was built for. Zero of 3 genuinely convergent controls
is falsely flagged, so this is a pure coverage gap and not a mis-tuned threshold.

Per the gate's `no` branch: `solver/marginal_flow.py` was **not** modified under this leg's
authority, the battery is banked as a characterization test that currently passes, and this
branch is **not** pushed to `main`.

## What the predicate actually is

`capabilities.py:85` records *"`integrate` reports `converged` and gate 11 enforces it (the NaN
of leg 41)"*. The predicate, at the bottom of `solver/marginal_flow.py:integrate`, is

```
converged = finite(y)  AND  "diverged_at_tau" not in rec  AND  worst_res < 1e8
```

with `worst_res = max over steps of (Newton residual / its floor)`. Gate 11 is
`test_marginal_flow.py::test_11`, whose (b) half asserts that predicate on exactly two
trajectories: the leg-41 naive-perturbation trap, and one healthy on-branch run.

**Every clause is an observable of the inner nonlinear solve or of IEEE finiteness. None is an
observable of the state.** That is the whole finding; the battery measures its consequences.

## Method

`integrate` runs on its real code path. What is swapped is the flow object: a `SyntheticFlow`
duck-types `AugmentedFlow` and supplies a right-hand side with a **closed-form** solution, so
"divergent" is an analytic fact about the exact solution, never an impression about a big number.

Three disciplines make the verdicts mean something:

1. **Fidelity is enforced, not assumed.** A member counts only if the *computed* trajectory is
   verified to still exhibit its exact solution's divergence — by relative endpoint error for
   polynomial growth, by **fitted rate** for exponential growth (an endpoint error across 130
   decades is meaningless), by retained amplitude for oscillation. This is not bookkeeping: it
   excluded a real case, see Finding 3.
2. **Convergent controls are carried.** A predicate that flags everything would score perfectly
   on divergence. Three trajectories with genuine limits are in the battery and all three must
   be kept.
3. **Live controls reproduce gate 11's own two verdicts**, on the real `AugmentedFlow` at
   K = 96, before any new verdict is credited: the leg-41 trap → `converged = False`
   (residual/floor 1.28e13), the on-branch run → `converged = True` (residual/floor 6.28e2).
   Both reproduce. The harness is therefore not the explanation for the misses.

## Results

`writeup/data/p2_route_mfg_v1_adversarial.json`; reproduce with
`python experiments/p2_route_mfg_v1_adversarial.py` (~170 s, most of it the live controls).

| member | exact law | state growth | Newton residual/floor | verdict |
|---|---|---|---|---|
| `mu_linear` | `mu = mu0 + tau` | 2.01e2 | 5.91e-02 | **MISSED** |
| `mu_quartic` | `mu = (1+tau)^4` | 1.41e7 | 7.53e-01 | **MISSED** |
| `b_quadratic` | `b = (1+tau)^2` | 3.73e3 | 9.56e-01 | **MISSED** |
| `mu_exp_mild` | `mu = 0.3 e^{tau/2}` | 1.25e13 | 1.15e-02 | **MISSED** |
| `mu_exp_extreme` | `mu = 0.3 e^{5 tau}` | **4.99e130** | 1.60e-02 | **MISSED** |
| `mu_negative_runaway` | `mu = -0.3 e^{tau/2}` | 1.25e13 (sign flipped) | 1.15e-02 | **MISSED** |
| `osc_sustained` | pure rotation, amplitude 1 forever | 1.00 | 6.94e-04 | **MISSED** |
| `osc_growing` | rotation, `Re = +0.05` | 1.99 | 2.29e-03 | **MISSED** |
| `nan_finite_time_blowup` | `mu' = mu^2`, blows at `tau = 1` | — | **1.49e14** | CAUGHT |
| `osc_stiff_underresolved` | rotation, `omega dt = 4` | 1.00 | 9.99e-01 | EXCLUDED (Finding 3) |
| `decay_to_zero` | `mu = 0.3 e^{-tau}` | limit 0 | 9.95e-01 | kept (correct) |
| `exact_fixed_point` | `rhs == 0` | limit | 0.00 | kept (correct) |
| `damped_oscillation` | spiral in | limit 0 | 5.55e-04 | kept (correct) |

### Finding 1 — the miss is not marginal, it is by nine orders of magnitude

The threshold is `1e8`. **Every missed trajectory's worst Newton residual/floor is below 1.0**,
i.e. its inner Newton converged to its own floor at every step. The smallest headroom anywhere in
the missed set is **1.05e8×** and the largest is **1.44e11×**. The worst missed case,
`mu_exp_extreme`, ends at `mu = 1.50e130` — a state 130 decades from where it started — with a
residual/floor of **1.60e-02**, which is **1.6e-10 of the threshold**. No re-tuning of `1e8`
reaches these cases: the discriminator is not merely set too high, it is measuring something
else. Newton is *well-conditioned precisely because* the trajectory is smooth, so on this family
the discriminator is anti-correlated with the failure it is asked to detect.

### Finding 2 — the misses are not about size, and `osc_sustained` proves it

`osc_sustained` is a pure rotation: the exact amplitude is **1 for all time**, the computed one
0.931 after 20 periods. Nothing is large, nothing is small, and the trajectory has no limit at
all. It is missed. This separates *"the predicate misses big numbers"* from *"the predicate does
not look at the state"* and establishes the second. `test_8` in the regression file asserts the
mechanism directly and without reference to any adversarial case: the exact fixed point and a
state 1.2e13× larger receive the **same verdict on all three clauses**, which is impossible if
any state clause existed.

`mu_negative_runaway` is the same point in the repository's own vocabulary. `integrate`'s comment
records the historical failure as *"the off-branch trap ended at mu = −1.6e24 with every value
finite"*. Made smooth — same runaway, healthy Newton — it reaches `mu = −3.7e12`, a **negative
viscosity**, and is accepted. The clause added in response to that incident does not cover the
incident's own shape once the inner solve is healthy.

### Finding 3 — a second, distinct hazard, found by the audit's honesty clause

`osc_stiff_underresolved` (rotation at `omega dt = 4` rad/step) is **excluded** from the
statistic, and the reason is itself a finding. BDF2 is L-stable — deliberately so, per the
module's integrator note — and it damps that mode to **3.5e-14 of its exact amplitude**. The
trajectory the predicate saw genuinely converged, to zero. Counting it as a missed divergence
would blame the gate for the integrator.

But the underlying event is a real hazard with no detector anywhere in the module: **an
under-resolved sustained oscillation is silently converted into a spurious decay**, and the run
reports `converged = True` with every diagnostic healthy. That is the opposite failure direction
from the rest of this note — not "divergence accepted" but "a limit manufactured" — and nothing
downstream would say so. `frequency_profile`'s docstring already warns that *"any time integrator
caps the |Im| it can resolve at ~1/dt"*; this measures what that costs when it binds, and no
`dt`-vs-`max|Im|` guard exists to catch it.

## Severity: what this does and does not reach

`rec["converged"]` has exactly one consumer in the tree: `experiments/p2_route_i_v1_driven.py`
`i4_adiabaticity`, which quotes `mu_end` and `alpha_1` for each accepted off-branch start and
records a refusal otherwise. **No banked number is shown to be wrong.** Read from the committed
`writeup/data/p2_route_i_v1_driven.json`, all three accepted off-branch runs land at
`mu_end = 0.052066574…`, agreeing with the on-branch reference to **1.4e-10, 4.0e-10 and 4.3e-10
relative**, with `alpha_1 = 0.1323605483…` to ten significant figures.

The honest reading of that agreement: those trajectories are healthy, and it is an **independent
redundancy** — the driver's own comparison against the on-branch reference — that demonstrates
it. The gate did not. Had one of those runs diverged smoothly, this measurement says the gate
would have passed it and the driver would have quoted its `alpha_1`.

## What is and is not claimed

* **Claimed, and measured:** on 9 divergent trajectories with closed-form exact solutions and
  verified integrator fidelity, the predicate `capabilities.py` calls a convergence gate flags
  **1**, the NaN case it was built for. Every miss sits at least 1.05e8× below its own threshold.
  0 of 3 convergent controls is falsely flagged.
* **Claimed, and measured:** the mechanism is that all three clauses are inner-solve or IEEE
  observables and none is a state observable — asserted directly in `test_8`, not inferred.
* **Claimed, and measured:** a distinct second hazard, BDF2 damping an under-resolved sustained
  oscillation to 3.5e-14 of its amplitude while reporting `converged = True`.
* **NOT claimed:** any novelty. SUNDIALS treats "the nonlinear solve converged" and "the state is
  admissible" as two separate tests (novelty pass Q2), and every published blow-up detector is a
  predicate on the state or its time series (Q3). This is a known distinction that this
  repository's predicate does not make.
* **NOT claimed:** that any banked number is wrong. The severity section measures the opposite.
* **NOT claimed:** that `converged` is *misimplemented*. It does what its own in-code comment
  says — it separates a stagnated Newton from a healthy one. The defect is in the **name and the
  advertised scope**: `capabilities.py` calls it convergence enforcement, and it is not that.

## Recommended disposition (for the orchestrator, not executed here)

1. `capabilities.py`'s validated line should be **narrowed**, e.g. *"`integrate` reports
   `converged`, which separates a stagnated inner Newton from a healthy one; it is NOT a
   trajectory-convergence test and does not detect smooth divergence"*. That file is outside this
   leg's territory and was not touched.
2. The repair, when a leg is authorised, is a **state clause** alongside the existing ones and is
   small: a bound on `|mu|`/`|b|` growth relative to the run's start, a sign guard on `mu` (a
   negative viscosity is never admissible), and a tail-of-trajectory Cauchy or drift test for the
   no-limit case. All three quantities are already in `rec` — `mu`, `b_end`, `mu_end` — so the
   information is present and merely unused.
3. Separately, a `dt` vs `max|Im|` resolution guard for Finding 3, in the spirit of the existing
   `resolution_guard`, which covers the mu–K crossover and not this.
4. `test_marginal_flow_adversarial.py` pins all of the above as characterization tests that
   **currently pass**. When a repair lands they will start failing — that is the intended signal,
   and the correct response is to flip the assertions, never to weaken them so a repair looks
   unnecessary. The three convergent controls and the NaN control are soundness assertions and
   must keep passing throughout.
