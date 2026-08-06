# Leg 85 — Route-GRA novelty pass (run BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-C. **Branch:** `leg/gra-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics, measures no new gCLM
physics, and claims no novel mechanism. It adversarially audits one *status-reporting* property
of `solver/gclm_rescaled.py` — whether its relaxation loop's `converged` report can be True on a
trajectory that has not reached the CLM self-similar fixed point.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Query strings
below are verbatim; every returned link judged on-topic is listed.

---

## 0. The ban check, stated explicitly

The plan of record bans **"another gCLM measurement leg"** (lifted by: never — the model is
exhausted, Stage 3.5, leg 42). This leg does **not** touch that ban, and the reason is
structural, not rhetorical:

* The banned object is a **physics measurement** — a new statement about the gCLM model (a rate,
  an exponent, a stability boundary, a parameter sweep). Leg 42 exhausted that.
* This leg's object is a **Python predicate**: the expression `res < tol` on line 157 of
  `solver/gclm_rescaled.py` and the loop's `break` on line 145–146. Its output is a statement
  about *the code's self-reporting*, not about CLM. Every trajectory it runs is deliberately
  chosen to be one the model's physics is already known to do; none is run to learn physics from
  it, and no `a` is varied — the module is `a = 0` only, single point, no sweep.
* This is the same distinction that clears **leg 83** (Route-MFG, `marginal_flow.py` gate 11)
  and **leg 84** (Route-TNA, `target_norm.py` domain guard), both of which audit reporting rather
  than measure. It is also the same distinction as **leg 79** (Route-PC) and **leg 69**
  (Route-IA), which audit certificate-adjacent *logic* against poisoned or adversarial input.

Nothing in this leg is admissible as a gCLM result, and §4 pre-commits that cap.

## 1. `capabilities.py` grepped FIRST

Standing permanent ban: *"building a solver without grepping capabilities.py for the object
first"* (leg 45 nearly rebuilt `RescaledHLScenario2` from scratch). Grep result:

* line 69–72 — `solver/gclm_rescaled.py`, object *"1D CLM (a=0), dynamic rescaling"*, holds
  *"rescaled flow, fixed point, upwind transport in the stretched coordinate"*, **validated:**
  *"relaxes to the exact CLM self-similar fixed point -4X/(1+4X^2)"*, test
  `test_gclm_rescaled.py`. **This validated line is exactly the claim under audit.**
* Neighbours that are *not* this object and are not rebuilt here: `solver/gclm_family.py` (65),
  `solver/rescaled_spectrum.py` (73), `solver/fractional_gclm.py` (78),
  `solver/critical_dissipation.py` (82), `solver/gclm.py` (397), `solver/hl_rescaled.py` (45).
* Registered precedent for *this exact failure class* inside the repository:
  `solver/boussinesq_rescaled.py` (97–102) already carries the annotation that its relaxation
  **"LIMIT-CYCLES and its residual GROWS under refinement, so 'resolution-stable' here is not
  'converged' (71)"**, and `solver/critical_dissipation.py` (89) carries *"reports `converged`
  and gate 11 enforces it (the NaN of leg 41)"*. So the repository has already met (a) a
  relaxation loop that limit-cycles and (b) a `converged` flag that needed a NaN guard bolted on
  — in **sibling** modules. Nobody has asked the question of `gclm_rescaled.py`.

**Nothing is built from scratch. No solver is written. `solver/gclm_rescaled.py` is READ ONLY**
and is not edited under either gate outcome.

## 2. What is being checked for prior art

* **(N1)** Is *"an unnormalized absolute residual used as a stopping test gives false convergence
  when the solution amplitude is itself a free scale"* a recognised, named hazard — or would
  reporting it be a claim of discovery?
* **(N2)** Is *"a stopping test sampled once per step can fire at the turning point of a
  sustained oscillation"* a named hazard?
* **(N3)** Is the *method* — an adversarial non-convergent-trajectory battery banked as a
  permanent regression test against a relaxation loop's own status flag — standard practice
  rather than novel?

## 3. Queries, verbatim, with the links returned

### Q1
`unnormalized absolute residual stopping criterion false convergence steady state solver scale invariance`

- https://www.afs.enea.it/project/neptunius/docs/fluent/html/ug/node812.htm — ANSYS FLUENT 12.0
  User's Guide §26.13.1, *Monitoring Residuals*. Documents that residuals are **scaled and
  normalized by default**, and that unnormalized/unscaled residuals are an explicitly
  *opt-out* setting. i.e. normalization is the documented default expectation.
- https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/flu_ug/flu_ug_sec_solve_monitor.html
  — ANSYS §36.15, *Monitoring Solution Convergence*. States the absolute-criterion failure mode
  directly: when the scaling reference is itself small, the absolute criterion misfires.
- https://cfd.university/blog/how-to-determine-the-best-stopping-criterion-for-cfd-simulations/ —
  *How to determine the best stopping criterion for CFD simulations.* States the governing point
  in one line: **a small residual does not imply an equally small error, because a universal
  normalization scale is not known.**
- https://doc.comsol.com/5.5/doc/com.comsol.help.comsol/comsol_ref_solver.27.096.html — COMSOL,
  *About the Stationary Solver*; relative vs absolute tolerance in a stationary solve.

**Answer to (N1): this is a standard, documented, named hazard of CFD practice — it is not a
discovery.** Anything this leg finds is reported as *"a documented hazard that this module
exhibits"*, never as a new phenomenon.

### Q2
`dynamic rescaling self-similar blow-up solver convergence criterion residual tolerance pitfall`

- https://arxiv.org/pdf/2603.25104 — Huang–Tong–Wang, *Self-similar finite-time blowups with
  singular profiles of the generalized CLM model*. **This is the paper whose value-based
  normalization `solver/gclm_rescaled.py` implements** (cited in its module docstring). Relevant
  for the *scaling gauge*: it fixes the normalization precisely because the rescaled problem
  admits a free scale.
- https://arxiv.org/pdf/2604.01868 — Chen–Huang–Li, 1D Hou-Luo / 2D Boussinesq numerical
  investigation; the ledger's rank-1/rank-3 source.
- https://arxiv.org/pdf/1905.06387 — *On the Finite Time Blowup of the De Gregorio Model.*
- https://arxiv.org/pdf/2405.10916 — *Nearly self-similar blowup of generalized axisymmetric
  Navier-Stokes equations.*
- https://arxiv.org/pdf/2311.11511 — *Nearly self-similar blowup of the slightly perturbed
  homogeneous Landau equation.*
- https://arxiv.org/pdf/1908.09385 — *Singularity formation and global well-posedness for the
  gCLM equation with dissipation.*
- https://ww3.math.ucla.edu/camreport/cam10-66.pdf — *Self-similar blowup solutions*, UCLA CAM.

**None of these audits a stopping test.** They all *use* dynamic rescaling and report converged
profiles; the stopping criterion is treated as an implementation detail, which is exactly the gap
this leg probes locally. **Answer to (N2)/(N3): the method is ordinary software-verification
practice (adversarial regression battery), and the leg claims no novelty for it.**

## 4. Pre-committed cap on the claim (binding, written before construction)

Whatever the battery returns, this leg claims **at most** a statement of the form:

> On `solver/gclm_rescaled.py` as of commit `925913a`, over the battery enumerated in
> `experiments/p2_route_gra_v1_adversarial.py`, the reported `converged` flag was
> {true/false}-positive on N of M trajectories, with the following measured magnitudes.

It does **not** claim: anything about CLM as a model; anything about whether the *validated*
relaxation results already on main are wrong (the validated runs use well-behaved data, and
re-checking them is `test_gclm_rescaled.py`'s job, not this leg's); anything about other
modules' loops; and — per the yes-branch of the gate — **no repair is attempted under this
leg's own authority** even if the answer is yes.

## 5. Battery design, fixed BEFORE any run

Designed from reading the module, not from results. Four adversarial families, all driving the
**real** `RescaledCLM` through its **real** `run()`; the solver is never subclassed, monkeypatched
or edited:

* **G — amplitude gauge.** `f_init = eps * f_CLM` for eps down to 1e-10. The module's own
  docstring states *"the rescaled initial amplitude is a free gauge"*, while `res` is an
  **absolute** `||f_tau||_inf`. Prediction: the stopping test becomes eps-dependent.
* **S — scaling-family drift near the neutral direction.** `Omega_lambda(X) = Omega_0(lambda X)`
  is a steady state for every lambda (the dilation term is scale-invariant), so the fixed point
  is a **line**, not a point, and motion along it is neutral. Data off the line should crawl.
* **O — oscillation.** `dt_frac` pushed toward and past the upwind/SSPRK3 stability limit, and
  two-scale data, to produce sustained non-decaying oscillation rather than relaxation.
* **N — non-finite and trivial.** `f_init = 0` (a genuine but *wrong* fixed point), and data that
  overflows, to check that `res < tol` is not reachable through NaN/inf.

Reported per trajectory: `converged`, `residual`, `steps`, the **true** distance to the exact
profile `||Omega - Omega_0||_inf` and its relative form, `c_omega` vs the exact `-1`, and the
residual's own later history. **Magnitudes, never booleans alone.**
