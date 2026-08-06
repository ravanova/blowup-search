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

---
---

# TECHNICAL NOTE — Route-BHN v1: what the bordered Newton's `converged` flag certifies

*This is the leg's required findings section. It is carried here rather than in a separate
`writeup/4_p2_lottery/TECHNICAL_*.md` because the leg's declared file territory does not include
that path; the quartet permits either location, and leg 69 set the precedent.*

## Gate, verbatim, and the answer

> "Under an adversarial battery (near-singular Jacobian at the starting iterate, NaN/Inf-poisoned
> initial guess, a residual sequence oscillating just above and below tolerance), does
> `solver/bordered_hl.py`'s damped Newton solve ever incorrectly report convergence?"

**NO — 0 false reports in 336 cases on the module's own system.** The `no` branch applies:
confirmed robust under the battery, banked as a permanent regression test
(`test_bordered_hl_adversarial.py`), lands normally on `main`. **`solver/bordered_hl.py` was read
and not modified**, under this or any other outcome.

The predicate was fixed **before** the run and is never read off the ladder the solver returns:

> FALSE REPORT := `converged is True` AND ( `‖F(z_returned)‖_∞ ≥ tol`, **recomputed
> independently from the returned iterate**, OR `z_returned` is not all finite ).

That is the only claim the flag makes — the code sets
`converged = bool(res[-1] < tol and np.isfinite(res[-1]))` — so it is the reading the flag can be
*wrong* about. A weaker reading ("converged at a point that is not a locally unique root") was
**measured but not used to decide the gate**, because the flag never promised it. That is where
the exposure turned out to live, and it is reported in full below.

## Results, by family

| family | cases | false reports | the magnitude that matters |
|---|---|---|---|
| well-posed baseline (n = 101, 201) | 2 | 0 | converges to 7.42e-15 / 5.33e-15 in 16 steps; σ_min(DF) = 4.50e-04 / 4.28e-04 |
| near-singular Jacobian at `z0` | 11 | 0 | cond(DF(z0)) swept 4.02e+03 → **4.97e+15** → exactly infinite |
| NaN/Inf-poisoned initial guess | 231 | 0 | **222 of 231 returned a NON-FINITE iterate**; all 231 reported `converged=False` |
| residual oscillating across tol | 8 | 0 | dips of rise ratio 1.02x–1.70x, `tol` placed strictly inside each |
| degenerate root (zero profile) | 4 | 0 | `converged=True` at residual **exactly 0.0** with DF **nullity 3** |
| λ-collapse (random starts) | 80 | 0 | collapse in **78/80**; worst accepted uphill ratio **2.798e+05** |

### Finding 1 — the flag is not fooled, and the poison result is the sharp one

The strongest single number is that **222 of 231 poisoned runs returned an iterate containing
NaN or ±Inf, and not one of the 231 reported convergence.** The flag's only defence is
`np.isfinite` applied to the *residual*, and nothing anywhere checks the returned `z` — yet the
defence holds, because every slot of the packed unknown is read by `F` through a matrix product
and a non-finite entry cannot fail to propagate into `‖F‖_∞`. The gap between "the returned data
is garbage" and "the flag says so" is therefore real but currently harmless: a caller that trusts
`hist["converged"]` is safe, a caller that trusts `z` without checking the flag is not.

### Finding 2 — LAPACK does not raise where the novelty pass said it would not

`except np.linalg.LinAlgError: break` fired at **exactly one** point of the whole sweep: the
exactly-zero profile. At `eps = 1e-13`, with cond(DF) = **4.97e+15** and measured nullity 3,
`np.linalg.solve` returned a finite step and raised nothing, and the line search then accepted a
step that multiplied the residual by **1.067e+08**. This is the behaviour Q3 of the novelty pass
located in the scipy/numpy record *before* construction, confirmed at the predicted place. The
`except` branch is not the near-singularity guard it looks like; it is an exact-zero-pivot guard.

### Finding 3 — the oscillation family stops honestly, and the mechanism is a floor, not luck

Eight ladders were found that dip and then rise; `tol` was placed strictly between the dip and the
rise (geometric mean) so the solve had to stop at the bottom of an oscillation it was about to
climb out of. All eight reported `converged=True`, and all eight were **genuine**: the
independently recomputed residual was below the placed tolerance every time, and σ_min at every
stopping point was **4.50e-04**, nowhere near singular.

The reason this family cannot threaten the module is a measured separation, not luck. The
object's round-off floor is the band **[1.44e-15, 7.42e-15]**, where the ladder sits for 45
consecutive rungs; the module's own working tolerance is 1e-13, **1.13 decades above the top of
that band**. Every oscillation the solver can exhibit therefore lives strictly below any
tolerance in use, and the "just above and below tolerance" regime the gate names is not reachable
on this object without deliberately setting `tol` into the round-off band.

### Finding 4 — `converged=True` at an exactly singular Jacobian (the real exposure)

`Ω = V = 0` nulls both interior equations for **any** `(c_l, c_ω, c_r)`. With the three border
targets pinned at zero the residual is **exactly 0.0**, so the solve returns `converged=True` in
**zero iterations** with the three gauge constants **exactly as they were passed in** — verified
with `(1.06, −0.42, 0.077)`, `(1e6, 1e6, 1e6)` and `(−3.7, 91.2, −0.5)`, all returned unchanged,
all with DF nullity 3 (σ_min = 0.0 exactly; nullity **102 of 205** in the all-zero case).

This is **not** a false report — the residual really is below tol — and it is not escalated. It is
the precise sense in which the flag does not mean what the module's own docstring promises:
*"the constants are unknowns of the SAME Newton system from the first iterate"*. At this point
they are unknowns of a singular system and are not determined at all, and nothing in the returned
history says so. Any downstream certificate consumer needs an invertible `DF` (the radii
polynomial's `Z_1` is built around an approximate inverse `A`); `converged` does not supply it.

### Finding 5 — λ-collapse: the backtracking budget runs out and the step is taken anyway

```
while lam > 1.0 / 1024:
    if float(np.abs(self.F(z + lam * dz)).max()) < r0:
        break
    lam *= 0.5
z = z + lam * dz          # <- unconditional
```

The loop exits **at** `lam = 1/1024` whether or not any factor reduced the residual, and the step
is then taken regardless of direction. Measured over 80 random starts: collapse in **78**, and
the largest residual *increase* accepted by the line search was **2.798e+05x**. The only trace
left in the returned history is `lambda == 1/1024`. In Deuflhard's NLEQ-ERR the same event is
itself a termination criterion (novelty pass Q4), and COMSOL's stationary solver documents a hard
lower limit on the damping factor for exactly this reason. Note that this module's own docstring
already records the event from leg 44 — *"Newton accepted no step at all, lambda down to
1/1024"* — as a diagnosis; the loop still steps through it.

### Finding 6 — the advertised conditioning diagnostic is never written

`cond_hist = []` is allocated in `newton()` and nothing is ever appended to it; `hist["cond"]` is
a length-0 array in **every** run of this leg, at every tolerance. A caller guarding with
`np.all(hist["cond"] < X)` gets `True` vacuously (verified); one calling `.max()` gets an
exception. The diagnostic that would have caught Findings 2 and 4 is present in the return
signature and empty.

### Finding 7 — what "Newton to 5.66e-15" is worth in iterate units

`capabilities.py` validates this module with a residual. A residual is not an error:
`‖δz‖ ≤ ‖F‖ / σ_min(DF)`. Measured at the converged root, n = 101: σ_min = **4.504e-04**, cond =
**6.188e+04**. Independently of any linearization, perturbing the root along the smallest right
singular direction gives a residual response of **1.191e-04 per unit iterate error**. So a
converged `tol = 1e-13` pins the iterate only to about **8.40e-10** in the sup norm — roughly
**3.9 decades weaker** than the residual figure quoted. At n = 201 the same construction gives
σ_min = 4.28e-04 and **4.59e-10**. This is not a defect; it is the honest conversion, and it is
banked as a gate so the two numbers cannot drift apart silently.

### Finding 8 — scope: the criterion, driven on a system with no root

Driving the **unmodified production loop** (`BorderedHL.newton`, unbound) on a duck-typed object
with `F(x) = e^{-x}` — smooth, `|F| → 0`, and **no root at any finite x** — returns
`converged=True` after 28 full undamped steps at `x = 28.0`, residual 6.91e-13 < tol 1e-12. This
is fault injection into the *algorithm* and says nothing about the bordered system's own `F`,
which is a degree-2 polynomial; it is banked only to fix the scope of the flag exactly:
`res[-1] < tol` cannot distinguish *found a root* from *walked out along a decaying tail*. This
is the documented limitation of residual-only termination located at Q1/Q2 before construction,
and it is **not** claimed as a discovery and **not** escalated.

### Environment note, not a solver property

On this 12-core host an **unpinned** `np.linalg.solve` on the module's N = 205 matrix costs
**1.006 s** against **0.00082 s** with BLAS threads pinned to 1 — a **~1230x** penalty, which
makes one 16-step Newton solve take 20–33 s instead of 0.03 s. Both new files pin the thread
count before importing numpy. This is worth passing to whoever owns the bench-repair lane:
`test_bordered_hl.py` and every other consumer of this module pay the same tax today, and it is
an environment effect, not anything about the solver.

## What is and is not claimed

* **Claimed, and measured:** under the gate's three named adversarial families, on the module's
  own system, `BorderedHL.newton` produced **0 false convergence reports in 336 cases**, with
  every `converged=True` independently re-verified against a freshly recomputed residual and a
  finiteness check. That is a materially stronger validation footprint than the well-posed
  single-ladder evidence `capabilities.py` currently rests on.
* **Claimed, and measured:** four reporting weaknesses, with exact magnitudes — `converged=True`
  at DF nullity 3 (Finding 4), an accepted uphill step of up to 2.798e+05x at λ-collapse
  (Finding 5), an always-empty `cond` history (Finding 6), and a 3.9-decade gap between the
  residual quoted and the iterate error it pins (Finding 7). **None of them is a false report**,
  and none was patched under this leg's authority.
* **NOT claimed:** any novelty. Every mechanism above is in print — see Q1–Q4.
* **NOT claimed:** that any number produced by legs 46/47 is wrong. Nothing here shows that; the
  well-posed path reproduces its validated behaviour exactly. Finding 7 re-states what that path
  certifies, it does not contradict it.
* **Prediction scored.** The novelty pass predicted, before measurement, that the boolean flag
  would be hard to fool while the reporting around it would be where the exposure lives. Both
  halves held. The pass did **not** predict Finding 4 (the exactly-singular degenerate root),
  which the construction found on its own.

## Recommended disposition (for the orchestrator, not executed here)

1. `capabilities.py`'s validated line for `solver/bordered_hl.py` could gain the iterate-units
   conversion from Finding 7 — the residual 5.66e-15 corresponds to an iterate error near 1e-09
   at these σ_min values. That edit is outside this leg's territory and was not made.
2. The repairs implied by Findings 4–6 are small, standard, and each belongs to a leg with
   authority over `solver/bordered_hl.py`: populate `cond_hist`; treat λ-collapse as termination
   (Deuflhard); and refuse `converged=True` when DF at the returned iterate is numerically
   singular. Landing any of them will **fail** the four `test_characterize_*` gates in
   `test_bordered_hl_adversarial.py`. That is the intended signal — those gates must be converted
   into soundness assertions, never weakened.
3. The BLAS-threading tax belongs to the bench-repair lane, not here.
