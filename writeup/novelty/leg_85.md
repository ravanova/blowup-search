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

---

# LEG 85 FINDINGS (written after the battery; the §4 cap above is honoured)

## GATE ANSWER: **YES** — a false-positive convergence report exists.

Gate, verbatim: *"Under an adversarial battery of non-convergent upwind-transport trajectories
(sustained oscillation, slow drift near a saddle rather than the fixed point), does
`solver/gclm_rescaled.py`'s relaxation loop ever report having reached the fixed point when it
has not?"* — **Yes**, on **4 of 25** trajectories, all in one family, by one mechanism.

Per the yes-branch: **nothing was patched.** `solver/gclm_rescaled.py` is byte-identical to
`origin/main`. This is escalated to the orchestrator, not repaired here.

## The exact failing trajectory

```
solver  = RescaledCLM(n=601, c=0.5, rho_max=7.0)
f_init  = 1e-10 * (-4.0 * np.exp(-solver.X**2 / 2.0))
result  = solver.run(f_init, dt_frac=0.4, tol=1e-8, max_steps=20000)
```

| quantity | reported / measured | what it should be |
|---|---|---|
| `result["converged"]` | **`True`** | `False` |
| `result["steps"]` | **1** (of a ~2000-step relaxation) | — |
| `result["residual"]` | 2.942e-10 | — |
| `result["c_omega"]` | **+1.00000** | **−1** (wrong **sign**; abs error **2.0**) |
| `‖Ω − Ω₀‖_inf` (core) | **1.000** = **100%** of `max|Ω₀|` | ~1e-5 |
| **post-stop relative drift** | **1.0000** (**100%**) | ~2.5e-9 |

*Post-stop relative drift* is the gauge-invariant adjudicator this leg introduces: take the
state the loop returned, integrate it 4000 further steps with the same integrator, and measure
‖Δf‖_inf / ‖f_returned‖_inf. A genuinely relaxed trajectory scores **2.5e-09**. This one scores
**1.0000** — the "converged" state subsequently moves by its own entire amplitude. That number
is what forecloses the defence "the flag only ever claimed `res < tol`, and `res` really was
< tol": by every scale-free measure the returned state is not at rest.

Onset is graded, not a cliff — the full ladder at `tol = 1e-8`:

| λ (= `-f(0)/4`) | converged | steps | c_omega | ‖Ω−Ω₀‖_inf | post-stop drift | verdict |
|---|---|---|---|---|---|---|
| 1e+00 | True | 1995 | −0.9977 | 1.07e-05 | 2.47e-09 | honest (the validated case) |
| 1e-01 | True | 1920 | −0.9764 | 8.18e-01 | 2.46e-08 | honest |
| 1e-02 | True | 1938 | −0.7585 | 9.80e-01 | 2.46e-07 | honest |
| 1e-04 | True | 1189 | +0.9319 | 1.00e+00 | 1.25e-05 | honest |
| **1e-06** | **True** | 924 | **+0.9993** | 1.00e+00 | **1.22e-03** | **FALSE POSITIVE** |
| **1e-08** | **True** | 670 | **+1.0000** | 1.00e+00 | **1.30e-01** | **FALSE POSITIVE** |
| **1e-09** | **True** | **1** | **+1.0000** | 1.00e+00 | **1.0000** | **FALSE POSITIVE** |
| **1e-10** | **True** | **1** | **+1.0000** | 1.00e+00 | **1.0000** | **FALSE POSITIVE** |

## The mechanism, measured not argued

**The rescaled CLM fixed point is a one-parameter LINE, not a point.** The dilation term
`X ∂_X` is scale-invariant and `H` is scale-invariant at the origin, so

> Ω_λ(X) = Ω₀(λX) = −4λX/(1+4λ²X²)

is an exact steady state for **every** λ > 0, all with `c_omega = −1`. Measured on the line
(n=601): residual 2.11e-06 (λ=0.25), 4.75e-06 (λ=0.5), 2.16e-05 (λ=1), 4.03e-04 (λ=2), with
`c_omega` = −0.9906, −0.9953, −0.9977, −0.9988 respectively. The member is selected by the
origin slope `f(0) = −4λ`, **which the scheme freezes exactly** (both `tanh(0)` and
`HΩ − HΩ(0)` vanish at ρ=0) — and the module's own docstring tells the caller that *"the
rescaled initial amplitude is a **free gauge**"*.

**The dynamics are equivariant along that gauge; the stopping test is not.** Measured
directly, `‖f_τ‖_inf` is exactly degree-1 in λ:

| λ | residual | residual/λ |
|---|---|---|
| 1e-03 | 2.9373e-03 | 2.9373 |
| 1e-06 | 2.9423e-06 | 2.9423 |
| 1e-09 | 2.9423e-09 | **2.9423** |

while `tol` at line 145/157 is a **fixed absolute number**. Hence the closed-form threshold:
the loop stops on the **initial data**, before performing any relaxation, whenever

> **λ < tol / 2.942 = 3.40e-09**  (at `tol = 1e-8`)

which is exactly where the 1-step stops appear in the ladder above.

**It is structural, not numerical.** The failing trajectory is bit-for-bit the same verdict at
three resolutions — n=401/601/901 all give `converged=True`, `steps=1`, `c_omega=+1.00000`. It
is a property of the predicate `res < tol`, not of the discretization.

This is the hazard §3/Q1 already established as **standard and documented** (an unnormalized
absolute residual is not a convergence test when the solution scale is free; *"a small residual
does not imply an equally small error, because a universal normalization scale is not known"*).
**No novelty is claimed for the phenomenon** — only for the located, measured instance.

## Scope of the damage — deliberately narrow, and stated against this leg's own interest

* **No result currently on `main` is impugned.** Every trajectory in `test_gclm_rescaled.py`
  and every banked run uses the validated gauge `f(0) = −4` (λ=1), where the report is
  **trustworthy in both directions** — measured: a relaxing datum converges with post-stop drift
  **2.47e-09**, and a genuinely still-drifting datum (far-field bump at the same gauge) is
  correctly reported **`converged=False`** after 40000 steps with residual 3.86e-07. The battery
  field `false_positive_at_validated_gauge_f0_minus4` is **`false`**.
* This is therefore a **latent** false positive: reachable only by handing the module an origin
  slope ~9 orders below the validated one — through a gauge the module itself calls free, with
  no check, no warning, and no normalization enforced anywhere in `run()`.

## What the battery found to be ROBUST (the audit's other half)

* **No NaN bypass.** Overflowing amplitude (−4e6 datum), a NaN planted in the initial data, and
  `dt_frac` = 2.0 and 3.0 past the stability limit all produce `residual = nan` and are all
  correctly reported **`converged=False`**. `nan < tol` is `False`, and unlike
  `solver/critical_dissipation.py` (which needed the leg-41 NaN guard) this loop never needed
  one. Locked in as a regression test.
* **Oscillation does not trip the stopping test** — the gate's first named adversarial case
  **fails to break it**. `dt_frac` at 0.8/1.0/1.2/1.5 all still land on Ω₀ (shape err 1.07e-05,
  post-stop drift ≤ 2.47e-09), and a mode-6 modulation in ρ lands on gauge member λ=1.3 with the
  exact rate (`c_omega` = −0.99820, drift 1.89e-09). The gate's *second* named case — slow drift
  rather than the fixed point — is the one that broke it, in the specific form of the scaling
  gauge.
* **Converging to a non-validated member of the gauge line is honest, not a false positive.**
  λ = 0.25/0.5/2/4 all return `converged=True` with post-stop drift 6.2e-10 … 1.1e-08 and
  `c_omega` within 1e-2 of −1, while sitting ‖Ω−Ω₀‖_inf = 0.333 (λ=2, 0.5) and 0.600 (λ=4, 0.25)
  from Ω₀. These **are** genuine self-similar CLM fixed points; only the capabilities line's
  word *"the exact ... fixed point −4X/(1+4X²)"* is narrower than what the loop actually
  delivers. Recorded, deliberately **not** counted as failures.

## Secondary observations (reported, not escalated)

1. **The reported residual is one step stale.** `step()` returns `res = ‖L0‖_inf` where `L0` is
   the RHS at the state passed **in**, so `result["residual"]` describes the **previous**
   iterate, not the `f` returned alongside it. Measured mismatch at `dt_frac=0.4`, n=401:
   reported 3.187087 vs 3.090352 for the returned state — **3.13%**. Harmless at these step
   sizes; locked in so a future change is noticed.
2. **`f ≡ 0` is reported as convergence** (`residual` exactly 0.0, `steps` 1, `c_omega` +1.0).
   It is a *genuine* fixed point (post-stop drift 0.0) and so is not a kinematic false positive
   — but it is not the CLM one, and the loop hands back a rate of the wrong sign with no flag.
3. **`"converged"` is a raw `numpy.bool_`, not a Python `bool`** (line 157) — unlike the sibling
   loops at `solver/hl_rescaled.py:418,573` and `solver/bordered_hl.py:253`, which all cast.
   It is not JSON-serializable without a cast. Cosmetic; noted for whoever repairs the line.

## The repair this leg did NOT make

For the orchestrator's benefit only, and explicitly **not** applied: the cheapest sound fix is
to make the stopping test **relative to the gauge the scheme has already frozen**, e.g.
`res < tol * max(|f(0)|/4, floor)`, or equivalently to normalize the datum on entry and reject
`f(0) = 0`. That change makes the test scale-invariant along exactly the direction the module
declares free. It is one line in a file this leg is forbidden to touch, and it will change the
banked λ=1 numbers by nothing (λ=1 ⇒ multiplier 1). **The decision is the orchestrator's.**
