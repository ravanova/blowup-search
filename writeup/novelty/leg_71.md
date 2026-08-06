# Leg 71 — Route-CAP novelty pass: what `capabilities.py` claims, BEFORE it is checked

**Leg.** 71, Route-CAP, `leg/cap-v1`. **Merge base.** `e203b52` (leg 66).
**Date.** 2026-08-05.

For a self-audit leg the novelty pass is not a literature search — there is no external
claim to pre-empt. Its job is the same one it always has: **pin the claim in writing
before the instrument is pointed at it**, so the audit cannot be read back as having
found what it was aimed to find. This file is committed in its own commit, ahead of the
audit script, the results JSON, and any edit to `capabilities.py`.

## The claim under audit

`capabilities.py` states, in the header comment it is read under:

> `test` — the file that re-checks the above

and `test_capabilities.py` (the existing drift detector) enforces exactly three things
about that field:

1. the field is non-empty (`test_entries_are_complete_and_point_at_real_files`);
2. `(ROOT / c["test"]).exists()` — the named path is a file on disk;
3. `validated` is longer than 20 characters.

**Nothing in the repository currently checks that the cited test RUNS, that it PASSES,
or that it has anything to do with the module whose row cites it.** That gap is this
leg's whole subject. Existence is checked; greenness and relevance are not.

## Pre-registered scope of what "stale or broken" will mean

Decided here, before running anything, so the categories are not fitted to the results:

- **S1 missing file** — the cited path does not exist. (Already covered by the existing
  drift detector, so an S1 hit would also mean `test_capabilities.py` is itself red.)
- **S2 uncollected / unrunnable** — the file exists but does not execute as this repo's
  test convention expects (see "invocation" below): import error, no runnable entry
  point, a `__main__` block that asserts nothing.
- **S3 red at HEAD** — it runs and FAILS. This is the priority-bug category.
- **S4 name/coverage drift** — the file exists and is green, but the row's module is not
  the module the test actually exercises, or the test's name does not follow the
  convention `scripts/merge_gate.sh` relies on to map a changed `solver/<name>.py` to
  `test_<name>.py`. An S4 row is green but **untested by the merge gate**, which is a
  silent hole of exactly the kind this leg was chartered to find.

## Invocation: the gate's wording vs. this repo's reality

The chartered gate says "collected by pytest". **This repository has no pytest.** The
`.venv` contains numpy, matplotlib, pillow and their dependencies — no `pytest`, and no
`scipy` either. `scripts/merge_gate.sh` states the convention explicitly:

> Test convention in this repo: every `test_*.py` is a self-running script
> (`.venv/bin/python test_x.py`, no pytest). A `solver/<name>.py` change maps to
> `test_<name>.py` at the repo root when that file exists.

So "is collected" is audited in the only form that is meaningful here: the file is
importable, and its `__main__` block runs to completion with exit status 0 under
`.venv/bin/python`. This substitution is recorded here, in advance, rather than
presented afterwards as a result.

## The 42 rows as they stand at merge base `e203b52`

42 rows, citing 40 distinct test files (`test_first_integral.py` and
`test_solver_clm.py` are each cited by two rows).

| # | module | cited test |
|---|---|---|
| 1 | `solver/hl_rescaled.py` | `test_hl_rescaled.py` |
| 2 | `solver/line_hilbert.py` | `test_line_hilbert.py` |
| 3 | `solver/gclm_family.py` | `test_gclm_family.py` |
| 4 | `solver/gclm_rescaled.py` | `test_gclm_rescaled.py` |
| 5 | `solver/rescaled_spectrum.py` | `test_rescaled_spectrum.py` |
| 6 | `solver/fractional_gclm.py` | `test_fractional_gclm.py` |
| 7 | `solver/critical_dissipation.py` | `test_critical_dissipation.py` |
| 8 | `solver/marginal_flow.py` | `test_marginal_flow.py` |
| 9 | `solver/boussinesq_velocity.py` | `test_boussinesq_velocity.py` |
| 10 | `solver/boussinesq_rescaled.py` | `test_boussinesq_rescaled.py` |
| 11 | `solver/port_certification.py` | `test_port_certification.py` |
| 12 | `solver/fractional_boussinesq.py` | `test_fractional_boussinesq.py` |
| 13 | `solver/interval.py` | `test_interval.py` |
| 14 | `solver/interval_certificate.py` | `test_interval_certificate.py` |
| 15 | `solver/spectral_certificate.py` | `test_spectral_certificate.py` |
| 16 | `solver/nk_bounds.py` | `test_nk_bounds.py` |
| 17 | `solver/op_lower.py` | `test_op_lower.py` |
| 18 | `solver/holder_norms.py` | `test_holder_norms.py` |
| 19 | `solver/decay_grading.py` | `test_decay_grading.py` |
| 20 | `solver/decay_collocation.py` | `test_decay_collocation.py` |
| 21 | `solver/collocation_newton.py` | `test_collocation_newton.py` |
| 22 | `solver/reduced_certificate.py` | `test_reduced_certificate.py` |
| 23 | `solver/nk_fourier.py` | `test_nk_fourier.py` |
| 24 | `solver/nk_seminorm.py` | `test_nk_seminorm.py` |
| 25 | `solver/hilbert_holder.py` | `test_nk_hilbert_holder.py` |
| 26 | `solver/hilbert_pointwise.py` | `test_nk_hilbert_pointwise.py` |
| 27 | `solver/first_integral.py` | `test_first_integral.py` |
| 28 | `solver/turning_point.py` | `test_turning_point.py` |
| 29 | `solver/profile_newton.py` | `test_profile_newton.py` |
| 30 | `solver/advection_scope.py` | `test_advection_scope.py` |
| 31 | `solver/target_norm.py` | `test_target_norm.py` |
| 32 | `solver/literature_gates.py` | `test_literature_gates.py` |
| 33 | `solver/certificate_shapes.py` | `test_certificate_shapes.py` |
| 34 | `solver/bordered_hl.py` | `test_bordered_hl.py` |
| 35 | `solver/viscous_novelty.py` | `test_viscous_novelty.py` |
| 36 | `solver/weight_search.py` | `test_weight_search.py` |
| 37 | `solver/target_selection.py` | `test_target_selection.py` |
| 38 | `solver/ga_search.py` | `test_ga.py` |
| 39 | `solver/boussinesq.py` | `test_solver_boussinesq.py` |
| 40 | `solver/gclm.py` | `test_solver_clm.py` |
| 41 | `solver/spectral_utils.py` | `test_solver_clm.py` |
| 42 | `solver/finite_support.py` | `test_first_integral.py` |

**Three rows pre-flag themselves on the name convention alone**, before a single test is
run — rows 25, 26 and 38 cite a test whose name is not `test_<module basename>.py`, and
rows 40/41/42 share or borrow another module's test. Whether those are defensible
(a deliberately shared test) or holes (the merge gate never runs them) is what the audit
decides. Recording the suspicion here so that finding it is not mistaken for luck.

## Pre-committed edit discipline

Whatever the audit returns, this leg edits `capabilities.py` only in:
- the factual `test` field of a row proven stale, **or**
- a one-line self-audit stamp in the header comment.

No `validated` field — numeric or prose — is touched under either gate branch. Rows for
modules currently claimed by a live leg (`spectral_certificate.py`,
`certificate_shapes.py`, `literature_gates.py`, `target_selection.py`,
`weight_search.py`, `interval_certificate.py`, `interval.py`, `holder_norms.py`) are
reported but **not corrected** this cycle, to avoid colliding with a live leg's own
in-flight test changes.

---

# FINDINGS (appended after the audit ran)

**Gate answer: NO.** 42 rows, 40 distinct cited tests, **33 clean**. Measured twice — at
the original merge base `e203b52`, then re-run in full from a cleared cache at the rebased
HEAD `10fed85` after `origin/main` advanced by tens of legs. Both agree.

- **S1 missing: 0.** Every cited test file exists; every cited module exists. There is no
  deleted test and no renamed module hiding under a confident row.
- **S2 uncollected / no-op: 0.** Every cited test runs.
- **S3 RED at HEAD: 2** — `test_fractional_boussinesq.py` (36 passed, 1 failed: gate G6
  `p > 0 at s=0.10`, measured **p = -0.211**) and `test_profile_newton.py` (the inverted
  assertion `assert not rows[-1]["converged"]` -- Newton now **does** converge at a = 0.9,
  relres 2.89e-06 in 40 iterations). Both reproduce deterministically. Reported, not
  fixed.
- **S4 relevance: 2** rows cite a test that never loads the module — `solver/ga_search.py`
  (**corrected**: `test_ga.py` → `test_gclm_family.py`, leaving 1) and
  `solver/finite_support.py` (the SUPERSEDED tombstone; left alone deliberately).
- **7 modules are unreachable from `scripts/merge_gate.sh`'s name map** — green today,
  ungated tomorrow. A hole in the merge gate, not in the index.

**The three pre-flagged suspicions from the section above resolved unevenly**, which is
why pre-registering them was worth it: rows 25/26 (`hilbert_holder`,
`hilbert_pointwise`) are *accurate* — the cited tests exist, run and pass, and the odd
name is only a merge-gate reachability problem. Row 38 (`ga_search`) was a **genuine
mis-citation**. Rows 40/41/42's shared/borrowed tests are accurate as `test` fields but
sat under `validated` prose that leg 66 falsified, so they were flagged rather than
half-edited — and the rebase revealed main had already repointed all three, so that
recommendation is withdrawn as already-done.

**One false positive in this leg's own instrument**, recorded rather than deleted: the
first classifier demanded a `__main__` block or top-level `test_*` functions and wrongly
flagged `test_spectral_certificate.py` and `test_target_norm.py` as uncollected. Both are
straight-line module-level gate scripts — a third valid style in this repo. Fixed, and
documented in the script's docstring.

**Two timeouts were contention artifacts, not red tests**: `test_advection_scope.py` and
`test_marginal_flow.py` both exceeded 3600 s under a 6-way parallel sweep and both pass
when re-timed alone (2363.7 s and **112.0 s** — a 32x blowup for the latter).

Full evidence: `writeup/data/p2_route_cap_v1_audit.json`; discussion:
`experiments/journal/leg_71.md`.
