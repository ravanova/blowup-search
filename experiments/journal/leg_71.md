# Leg 71 — Route-CAP: the `capabilities.py` self-audit

**Branch** `leg/cap-v1`. **Merge base** `e203b52` (leg 66). **Date** 2026-08-05/06.
**Quartet** `experiments/p2_route_cap_v1_audit.py`,
`writeup/data/p2_route_cap_v1_audit.json`, `writeup/novelty/leg_71.md`, this journal.
No figure (pure audit, per the "no measurement, no figure" convention).

## Gate

> "Does every module row in capabilities.py have a test file that exists, is collected by
> pytest, and passes at current HEAD?"

**ANSWER: NO.**

42 rows, 40 distinct cited test files, **33 rows clean**. 6.3 hours of cumulative test
runtime (22,839 s of parallel sweep plus 2,364 s + 112 s of serial re-timing).

| category | count | modules |
|---|---|---|
| S1 cited test file missing | **0** | — |
| S1 module file missing | **0** | — |
| S2 uncollected / unrunnable | **0** | — |
| S2 runtime no-op | **0** | — |
| **S3 RED at HEAD** | **2** | `solver/fractional_boussinesq.py`, `solver/profile_newton.py` |
| S3 timeout unresolved | **0** | — |
| S4 cited test does not exercise the module | **2** | `solver/ga_search.py`, `solver/finite_support.py` |
| S4 unreachable from the merge gate's name map | **7** | `hilbert_holder`, `hilbert_pointwise`, `ga_search`, `boussinesq`, `gclm`, `spectral_utils`, `finite_support` |

The `test` field is in better shape than the charter feared in one specific respect —
**every cited file exists and every one of them runs**; there is no deleted test and no
renamed module hiding under a confident row. The drift is entirely in the two categories
the existing detector cannot see: *greenness* and *relevance*.

## PRIORITY BUG REPORT — 2 red tests at HEAD

Both reproduce deterministically (each run twice, standalone). **Neither is fixed here** —
a red test found by an audit is a bug report, not a silent repair, and repairing either
would mean touching a `validated` claim this leg is pre-committed not to touch.

### 1. `test_fractional_boussinesq.py` — 36 passed, **1 failed**

```
G6  the D/N instrument responds to s with the right sign
  [FAIL] p > 0 at s=0.10 (dissipation losing)     p=-0.211
  [PASS] p < 0 at s=1.00 (dissipation winning)    p=-3.486
  [PASS] p decreases with s                       -0.211 -> -3.486
```

The gate asserts that at weak dissipation (s = 0.10) dissipation should be *losing*
(p > 0); the measured p is **−0.211**, the wrong side of zero. The monotonicity and the
strong-dissipation end both hold, so the instrument's *ordering* is intact and only the
**sign at small s** is wrong — i.e. the zero-crossing of p(s) sits below s = 0.10 rather
than above it. Either the solver drifted, or the threshold was fitted on a coarser run.

**This one is urgent for a live leg.** `capabilities.py`'s row for this module claims
"consistency with the 1D critical exponent; no independent known answer", and **leg 67
(FD) is right now searching the literature for an independent critical fractional-
dissipation exponent for 2D Boussinesq**. Leg 67 is reading a module whose own
sign-convention gate is red. Whatever leg 67 finds should be compared against a repaired
instrument, not this one.

### 2. `test_profile_newton.py` — fails on an **inverted** assertion

```
assert not rows[-1]["converged"], rows[-1]
AssertionError: {'a': 0.9, 'converged': True, 'residual_rms': 3.88e-07,
                 'relres': 2.89e-06, 'c': 0.7483299284679625, 'iterations': 40}
```

The test demands that Newton **fail** to converge at a = 0.9 (the neighbouring assertion
prints "converged=False with relres %.1e (vs %.1e at a = 0.3)"), and it now **does**
converge, at relres 2.89e-06 in 40 iterations. Checks (1)–(4) of the same file all pass,
including quadratic convergence at a = 0.2 and the analytic Jacobian to 6.7e-11.

This is the more interesting of the two: it is a test encoding a **negative expectation**
about where the two-scale profile solve breaks down, falsified by the solver reaching
further than it used to. It is not obviously a regression — it may be an improvement that
invalidated a stale boundary — but it is red either way, and the row's `validated` prose
("converges to the known a=0 two-scale profile; residual falls to the Newton floor") does
not record the a = 0.9 non-convergence claim at all. Resolving it needs a leg that may
edit `validated`.

## Two timeouts that were MY artifact, not red tests

The parallel sweep runs 6 tests at once and these are multi-minute numerics.
`test_advection_scope.py` and `test_marginal_flow.py` both hit the 3600 s cap under
contention. Re-timed **alone**, both pass:

| test | 6-way parallel | alone | verdict |
|---|---|---|---|
| `test_advection_scope.py` | TIMEOUT > 3600 s | **PASS, 2363.7 s** | green, genuinely slow |
| `test_marginal_flow.py` | TIMEOUT > 3600 s | **PASS, 112.0 s** | green; **32x** contention blowup |

`test_marginal_flow.py`'s 112 s → >3600 s blowup is far past linear and looks like BLAS
thread oversubscription rather than CPU sharing. Worth knowing before anyone parallelises
this suite in CI. Reporting these as "red" would have been a false alarm of exactly the
kind this leg exists to prevent, so the script now re-times every timeout serially before
classifying it, and the JSON records both readings.

## A false positive in my own instrument, recorded rather than deleted

The first version of the audit demanded an `if __name__ == "__main__":` block or a
top-level `test_*` function, and flagged **`test_spectral_certificate.py` and
`test_target_norm.py` as "uncollected"**. That was wrong. Both are straight-line
module-level gate scripts that do their work at import and end in
`sys.exit(1 if n_fail else 0)`, and both run for real (28 and 25 lines of gate output;
875 s and 0.9 s). This repo has **three** test styles, not two.

Static collectability is now just "does it parse"; the genuine no-op case is caught at
runtime instead (exit 0 with no output at all), which found **0** rows. The dead heuristic
is documented in the script's own docstring rather than quietly removed — a self-audit
that silently repairs its own false positives is not auditable.

## The `test` field: 1 correction made

**`solver/ga_search.py`: `test_ga.py` → `test_gclm_family.py`.**

`test_ga.py` imports only the `ga/` package (`from ga.evolve …`, `from ga.fitness …`,
`from ga.genome …`); the string `ga_search` appears nowhere in it, nor anywhere under
`ga/`. So the row cited a green, 440 s test that **never loads the module it certifies**.
The module *is* exercised, by `test_gclm_family.py` (`from solver.ga_search import
ga_minimize, GAConfig`, green in 59.3 s), which drives `ga_minimize` on three seeds and
asserts exactly the determinism-per-seed property the row's `holds` field claims
(`"GA not deterministic for a fixed seed"`). Factual field only; `validated` untouched.

`test_capabilities.py` still passes after the edit.

## Reported, NOT corrected — and why

### `solver/finite_support.py` (S4, no coverage)
Cited test `test_first_integral.py` never mentions `finite_support`. The row is the
SUPERSEDED tombstone kept "only so the name resolves to a warning", so there is no test
that *should* cover it and no better citation exists. Left alone deliberately.

### Rows 39–41: `gclm.py`, `boussinesq.py`, `spectral_utils.py` — **needs a leg that may edit `validated`**
All three rows say, in `validated`: *"no dedicated test file — exercised through
test_solver_clm.py"* (resp. `test_solver_boussinesq.py`). **That sentence is now false.**
Leg 66 landed `test_gclm_dedicated.py`, `test_boussinesq_dedicated.py` and
`test_spectral_utils_dedicated.py`, all present at this leg's merge base.

I did **not** repoint the `test` fields. Doing so would leave each row internally
self-contradictory — a `test` field citing the dedicated file directly above a `validated`
field insisting no dedicated file exists — and the contradiction lives in the prose this
leg is pre-committed not to touch. The cited tests are not stale by the audit's own
definition (they exist, run, pass, and do reference their modules), so the honest outcome
is a flag, not a half-edit. **Recommend a follow-up leg chartered to update `validated`
and `test` together for these three rows.**

### Modules under a live leg
No stale or red row landed on a module claimed by a live leg, so the
"flagged, not corrected due to concurrent leg" rule did not have to fire.
`test_spectral_certificate.py` (875 s), `test_certificate_shapes.py` (271 s),
`test_literature_gates.py` (56 s), `test_target_selection.py` (0.5 s),
`test_weight_search.py` (195 s), `test_interval_certificate.py`, `test_interval.py` (1.2 s)
and `test_holder_norms.py` (5.2 s) are all green at HEAD.

## The structural finding: 7 modules the merge gate cannot reach

`scripts/merge_gate.sh` maps a changed `solver/<name>.py` to `test_<name>.py` **and runs
nothing if that exact filename is absent**. For these 7 modules the file is absent, so
editing any of them runs **no targeted test at all** — they are green today and ungated
tomorrow:

| module | cited test (green) | name the merge gate looks for |
|---|---|---|
| `solver/hilbert_holder.py` | `test_nk_hilbert_holder.py` | `test_hilbert_holder.py` ✗ |
| `solver/hilbert_pointwise.py` | `test_nk_hilbert_pointwise.py` | `test_hilbert_pointwise.py` ✗ |
| `solver/ga_search.py` | `test_gclm_family.py` | `test_ga_search.py` ✗ |
| `solver/boussinesq.py` | `test_solver_boussinesq.py` | `test_boussinesq.py` ✗ |
| `solver/gclm.py` | `test_solver_clm.py` | `test_gclm.py` ✗ |
| `solver/spectral_utils.py` | `test_solver_clm.py` | `test_spectral_utils.py` ✗ |
| `solver/finite_support.py` | `test_first_integral.py` | `test_finite_support.py` ✗ |

This is a hole in the *merge gate*, not in `capabilities.py` — every one of these rows
cites a real, green test, and the index is telling the truth. `capabilities.py` in fact
already knows the mapping the merge gate is missing. The cheap repair is for
`merge_gate.sh` to resolve a changed module through `capabilities.py`'s `test` field
instead of guessing the filename, which would close all 7 at once and keep closing them
as the index is maintained. **Out of this leg's territory** (`scripts/merge_gate.sh` is
not mine to edit); recorded for whoever picks it up.

## Standing bans

`plan_of_record.py` was run first; no ban touches an audit leg. The audit is
observational — it ran the existing suite and edited one factual field. It re-derives no
banned measurement and makes no claim about the L1→L4 chain. Note the standing ban
"building a solver without grepping capabilities.py for the object first" is precisely
what makes this file's accuracy load-bearing.

## Reproduce

```
.venv/bin/python experiments/p2_route_cap_v1_audit.py
```

Resumable: each test's result is appended to a JSONL cache outside the repo and flushed
as it completes, so an interrupted sweep resumes instead of restarting (this matters — the
first full attempt was killed at ~50 minutes and lost everything). Timeouts are re-timed
alone before being classified. Delete the cache to force a clean re-run.
