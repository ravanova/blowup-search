# Leg 66 novelty pass — Route-QF, dedicated tests for the three indirectly-covered modules

**Run BEFORE any test is written** (standing discipline). This is a **test-hygiene** leg, so
the pass is not a literature pass: writing unit tests against three of this repository's own
modules is, obviously, not a contribution to anyone's literature and **nothing here is banked
as novel**. What the pass has to establish instead is the leg's factual premise: *how much
coverage do these three modules actually have today, and which of their public entry points
has never been named by any test?* That is the question a "no dedicated test file" line in
`capabilities.py` is asserting an answer to, and it is the question that decides whether this
leg has anything to find.

**Verdict: `PROCEED`. Premise confirmed but overstated by `capabilities.py`; six public
entry points across the three modules are named by zero test files.**

---

## Q1 — what does `capabilities.py` actually say?

Verbatim, `capabilities.py:350-361`:

```
    {"module": "solver/boussinesq.py", ...
     "validated": "no dedicated test file -- exercised through test_solver_boussinesq.py",
     "test": "test_solver_boussinesq.py"},
    {"module": "solver/gclm.py", ...
     "validated": "no dedicated test file -- exercised through test_solver_clm.py",
     "test": "test_solver_clm.py"},
    {"module": "solver/spectral_utils.py", ...
     "validated": "no dedicated test file -- exercised through the solvers above",
     "test": "test_solver_clm.py"},
```

## Q2 — is the "exercised through <one file>" part true?

**No — it undercounts, in all three cases.** Test files that import each module:

| module | test files importing it | count |
|---|---|---|
| `solver/spectral_utils.py` | `test_fractional_gclm`, `test_ga`, `test_genome_rough`, `test_solver_clm` | 4 |
| `solver/gclm.py` | `test_gclm_family`, `test_gclm_rescaled`, `test_nk_fourier`, `test_solver_clm` | 4 |
| `solver/boussinesq.py` | `test_boussinesq_rescaled`, `test_boussinesq_transport`, `test_boussinesq_velocity`, `test_boussinesq_wall`, `test_fractional_boussinesq`, `test_genome_2d`, `test_genome_rough_2d`, `test_phase1_measurement`, `test_port_certification`, `test_solver_boussinesq` | 10 |

So the *breadth* claim in `capabilities.py` is wrong in the safe direction: there is more
indirect traffic than the line admits. That weakens the leg's expected yield but does not
kill it, because breadth of traffic is not the same as breadth of *interrogation* — see Q3.

## Q3 — which public entry points are named by **zero** test files?

Symbol-level sweep over all 52 `test_*.py` files (word-boundary match on the public name):

| module | symbol | test files naming it |
|---|---|---|
| `spectral_utils` | `dealias_mask` | **0** |
| `spectral_utils` | `velocity_hat` | **0** |
| `spectral_utils` | `derivative_hat` | **0** |
| `spectral_utils` | `l1_norm` | **0** |
| `spectral_utils` | `energy_production` | **0** |
| `gclm` | `energy_from_gradient` | **0** |
| `boussinesq` | `project_even_odd` | **0** |
| `spectral_utils` | `hilbert_hat` | 1 (`test_fractional_gclm`) |
| `spectral_utils` | `wavenumbers` | 3 |
| `spectral_utils` | `integral` | 3 |
| `gclm` | `solve_gclm` | 1 (`test_solver_clm`) |
| `gclm` | `clm_analytic_blowup_time` | 1 (`test_solver_clm`) |
| `boussinesq` | `dealias_mask2d` | 1 (`test_solver_boussinesq`) |
| `boussinesq` | `project_odd_odd` | 1 (`test_fractional_boussinesq`) |
| `boussinesq` | `velocity_from_vorticity` | 3 |
| `boussinesq` | `solve_boussinesq` | 3 |

Seven public symbols are named by no test at all. Five of them (`velocity_hat`,
`derivative_hat`, `dealias_mask`, `energy_production`, `energy_from_gradient`) are on the
**hot path of every gCLM run in the repository** — they are executed thousands of times per
solve, and are therefore covered in the weak sense that a catastrophic error would show up
as a failed end-to-end blowup-time comparison. They are covered in no stronger sense than
that. That gap is exactly the leg's thesis, and it is real.

## Q4 — what do the two "indirect" tests actually assert?

- `test_solver_clm.py` (182 lines): end-to-end. Blow-up time vs the CLM closed form, a
  frozen-`u` transport check, a pure-diffusion check, dealias/conservation guards. Every
  assertion is on `SolverResult` fields after a full integration. **No helper is ever called
  with hand-chosen input and checked against a hand-computed value.**
- `test_solver_boussinesq.py` (233 lines): same shape — Biot–Savart on a single mode,
  frozen-`u` translation, conservation drift, all through `solve_boussinesq`.

**Read:** the indirect tests are *system* tests. A helper-local error that the system test's
particular initial data happens not to excite — an off-by-one in a mask, a wrong branch for a
grid size the sweeps never use, a sign that cancels in the specific combination the RHS forms
— survives both files intact. That is the class of defect this leg goes looking for.

## Q5 — is any of this bankable as science?

**No.** Zero science content, by construction, and the leg is under the standing ban on new
gCLM measurement legs: it runs the existing code as-is at existing parameters and asserts
against its present behaviour and against closed-form values. No parameter is changed, no
new sweep is run, nothing enters the Clay estimate. Clay stays at ~0.05% behind Walls 1
and 2.
