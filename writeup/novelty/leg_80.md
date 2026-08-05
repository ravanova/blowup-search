# Leg 80 — Route-BHN novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-H. **Branch:** `leg/bhn-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics and claims no novel
mechanism. It stress-tests the damped-Newton solve in `solver/bordered_hl.py` — the module
`capabilities.py` validates with "Newton to 5.66e-15 at n=201" — against an adversarial battery.
The pass below exists to establish, *before* construction, which failure modes of a
residual-based damped Newton are **already documented in print**, so that anything this leg finds
is reported as *"a known globalisation hazard, present in our code"* and never as a discovery.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim, and every link returned that I judged on-topic is listed. Where a
search returned nothing on-topic I say so rather than reporting a number.

---

## What is being checked for prior art

The solver under test makes four design choices. The pass asks, for each, **whether the published
literature already names the failure mode**, because a named failure mode the code does not guard
is exactly where a false-convergence gap would live.

* **(N1)** The convergence flag is `‖F‖_∞ < tol` — a purely **residual-based** criterion. Is the
  unreliability of residual-only termination for a nonlinear system a documented result, and is
  there a named alternative?
* **(N2)** The backtracking loop halves `λ` from 1 down to `1/1024` and, **if no `λ` reduces the
  residual, still takes the step at `λ = 1/1024`**. Is "the damping factor collapsing" recognised
  in print as a *termination/failure* signal rather than something to step through?
* **(N3)** The step is `np.linalg.solve(J, -Fz)` inside `try/except LinAlgError`. Is it documented
  that LAPACK's `gesv` does **not** reliably raise on a singular or near-singular matrix, so that
  the `except` branch is not the guard it appears to be?
* **(N4)** Is a small residual at an ill-conditioned Jacobian known to be a **misleading** proxy
  for closeness to a root — i.e. is `‖F‖ < tol` known to be compatible with an arbitrarily large
  error in the iterate?
* **(N5)** Is adversarial / fault-injection testing of a nonlinear solver's *convergence
  reporting* (as opposed to its accuracy) an established method?

---

## Queries, verbatim, with the links returned

### Q1
`damped Newton method backtracking line search false convergence residual stopping criterion unreliable`

- https://www.sciencedirect.com/science/article/abs/pii/S0168927421003202 — *A hybrid-line-and-curve
  search globalization technique for inexact Newton methods*, J. Comput. Appl. Math. Names the
  **overshoot of the Newton search step**: the regime in which no acceptable damping factor is
  found within a finite number of backtracking steps.
- https://www.di.ens.fr/~aspremon/PDF/ENSAE/Newton.pdf — d'Aspremont, ENSAE lecture notes on
  Newton's method; the damped Newton phase and its guaranteed-decrease constant γ.
- https://www.stat.cmu.edu/~ryantibs/convexopt-S15/scribes/14-newton-scribed.pdf and
  https://web.stanford.edu/class/ee270/scribes/lecture15.pdf — standard treatments of the damped
  phase; both state the decrease guarantee as a *hypothesis-carrying* claim.
- https://arxiv.org/pdf/2006.00318 — *Basins of attraction and critical curves for Newton-type
  methods in a phase equilibrium problem*; retained because it is an empirical study of exactly
  the failure geometry (a damped Newton that terminates somewhere other than the intended root).
- https://arxiv.org/abs/2108.10249 — New Q-Newton's method meets Backtracking line search; adjacent.

**On-topic finding for (N1) and (N2).** The published statement is that **the residual is not
guaranteed to decrease even under an appropriate line-search condition**, and that line search can
*fail* — no acceptable damping factor exists within the backtracking budget. Both are named
phenomena. The code has no branch for either.

### Q2
`nonlinear solver stopping criterion small residual ill-conditioned Jacobian misleading convergence test Dennis Schnabel`

- https://par.nsf.gov/servlets/purl/10075349 — *Numerical methods for nonlinear equations* (Kelley,
  Acta Numerica survey). The sharpest item in this pass: it states that when one accepts low
  accuracy in the Jacobian or the linear solve, **it is unwise to terminate on small steps; one
  must terminate on small residuals and accept the effects of ill-conditioning** — i.e. the
  residual criterion is knowingly adopted *together with* an acknowledged ill-conditioning defect.
- https://www.sciencedirect.com/science/article/abs/pii/S0021999117306939 and
  https://www.researchgate.net/publication/320092171_A_stopping_criterion_for_the_iterative_solution_of_partial_differential_equations
  — a stopping criterion for iterative PDE solution; states plainly that **the residual can be a
  misleading indicator for ill-conditioned problems**, and that the classical repair (condition
  number × normalised residual) is both expensive and excessively conservative.
- https://arxiv.org/pdf/2106.16090 — a new stopping criterion for Krylov solvers in interior point
  methods; same theme one level down.
- https://mooseframework.inl.gov/application_usage/failed_solves.html and
  https://mooseframework.inl.gov/source/systems/NonlinearSystem.html — production-code
  documentation of nonlinear-solve failure modes; useful as evidence of what a *hardened*
  convergence report contains.
- https://www.osti.gov/servlets/purl/876345/ — robust large-scale parallel nonlinear solvers.

**On-topic finding for (N4).** In print, and not subtle: a small residual with an ill-conditioned
Jacobian does not bound the error in the iterate. Any measurement this leg makes there is a
*confirmation*, not a discovery.

### Q3
`numpy linalg.solve singular matrix does not raise LinAlgError NaN silently LAPACK gesv exact singularity`

- https://github.com/scipy/scipy/issues/22263 — *BUG: linalg.solve doesn't raise an error when A is
  a singular matrix* (Jan 2025). Directly on point: the singular-matrix exception is **not** a
  reliable guard.
- https://numpy.org/doc/stable/reference/generated/numpy.linalg.LinAlgError.html — the NumPy
  reference; documents `LinAlgError` as raised for singular input, which is the *expectation* the
  code encodes.
- https://mitra.stanford.edu/kundaje/marinovg/oak/programs/numpy/linalg/linalg.py — a mirrored
  `linalg.py` source, read for the actual `_raise_linalgerror_singular` call site (it fires on
  LAPACK's `info > 0`, i.e. an **exact** zero pivot only).
- https://bobbyhadz.com/blog/numpy-linalg-linalgerror-singular-matrix,
  https://www.statology.org/python-numpy-linalg-singular-matrix/,
  https://www.pythonpool.com/linalgerror-singular-matrix/,
  https://www.askpython.com/python-modules/numpy/numpy-linalgerror,
  https://www.zerve.ai/data-science-problems/numpy/linalgerror-singular-matrix-fix — practitioner
  write-ups, all consistent: the error fires on exact singularity, not near-singularity.

**On-topic finding for (N3).** The `except np.linalg.LinAlgError: break` branch catches only the
*exact* zero-pivot case. A near-singular Jacobian returns a finite but arbitrarily wrong `dz`
with no signal at all. This is the predicted entry point for the battery's near-singular family.

### Q4
`Kelley Newton method termination criteria damping failure report convergence flag scientific software fuzzing numerical solver`

- http://elib.zib.de/pub/elib/codelib/NewtonLib/ — Deuflhard's **NewtonLib** / NLEQ codes. The
  decisive precedent for (N2): the *error-oriented* global Newton (**NLEQ-ERR**) treats the damping
  factor becoming arbitrarily small as **itself a termination criterion**, because that is what a
  singular problem looks like from inside the line search.
- https://doc.comsol.com/5.6/doc/com.comsol.help.comsol/comsol_ref_solver.32.100.html — COMSOL's
  stationary solver reference; damping-factor prediction/correction, and an explicit hard lower
  limit on the damping factor plus an extra requirement to lower the risk of **premature
  termination**. Production practice matches Deuflhard, not our code.
- https://mooseframework.inl.gov/application_usage/failed_solves.html — again, for the taxonomy of
  reported failure states.
- https://arxiv.org/pdf/2605.13378 — *Robust Matrix-Free Newton-Krylov Solvers via Automatic
  Differentiation*; useful for (N5): its metrics **distinguish Krylov stagnation from poor Newton
  progress from complete nonlinear failure**, and classify runs as failed on non-finite values.
- https://arxiv.org/pdf/2103.13993 — *Rotating Boson Stars Using Finite Differences and Global
  Newton Methods*; a research code that reports the damped-Newton outcome as a graded state.
- https://arxiv.org/pdf/2006.00318 — as in Q1.

**On-topic finding for (N2) and (N5), and the sharpest of the pass.** Deuflhard's λ-collapse
criterion is the exact repair for the defect predicted by reading our loop: our `while lam >
1/1024` exits **with `lam = 1/1024` and then takes the step unconditionally**, whether or not the
residual decreased. In NLEQ that same event is a *stop-and-report-failure*. So the construction
must measure not just the boolean flag but **how far uphill the accepted step goes** and **whether
the ladder recorded in `res` can still end below `tol` after such a step**.

---

## What this pass settles, and how it sharpens the construction

1. **No novelty is available to this leg and none will be claimed.** Every mechanism that could
   fool a residual-based damped Newton — non-monotone residuals, line-search failure, λ-collapse,
   small residual at large condition number, a `gesv` that does not raise — is in print, in most
   cases as an explicit stated limitation of the design the module chose.
2. **It converts the gate's three named families into four measurable ones**, with a predicted
   defect for each:
   - **near-singular Jacobian at the starting iterate** — predicted entry via Q3: no exception, a
     finite wrong `dz`. Measure `cond(J)`, `‖dz‖`, and the *distance from the returned iterate to
     the true root* alongside the residual, because Q2 says the residual alone cannot bound it.
   - **NaN/Inf-poisoned initial guess** — measure whether the poison reaches `res[-1]`; the flag's
     `np.isfinite` guard is the only thing standing there, and it is applied to `res[-1]` only, not
     to the returned `z`. Poison every one of the `2n+3` slots, plus the three `pin` targets.
   - **residual oscillating just above/below tol** — construct exactly, by overriding `F` on a
     harness subclass, so the ladder is prescribed rather than hoped for.
   - **λ-collapse (added by this pass, from Q4)** — does the accepted uphill step at `λ = 1/1024`
     ever land the ladder below `tol`, and is that event visible anywhere in the returned history?
3. **A prediction recorded before measurement**, so it can be scored honestly afterwards: the
   boolean `converged` flag is expected to be *hard to fool into `True`* — it is a conjunction of
   `res[-1] < tol` with `np.isfinite`, and NaN propagates through `np.abs(...).max()` — while the
   *reporting around it* (the `cond` array, the λ-collapse event, and the meaning of a small
   residual at a large condition number) is expected to be where the exposure actually lives. If
   the measurement contradicts this, the measurement wins.
