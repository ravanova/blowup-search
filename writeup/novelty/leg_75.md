# Leg 75 — Route-LM novelty pass (run BEFORE benchmarking)

**Date:** 2026-08-05. **Agent:** LEG-I. **Branch:** `leg/lm-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg claims **no novelty of any kind** — not a theorem, not
a mechanism, not an algorithm. It re-measures a **performance number this repository asserted
about its own code** (`capabilities.py`'s `line_hilbert.py` entry: *"the cached slope operator
`slope_matrix` (Route-M: 10x on the Scenario-2 step)"*). A wall-clock multiplier on our own
integrator is not a literature object, so the outward pass below is deliberately narrow: it asks
only whether the **method** — asserting a speedup factor inside a regression test — is a
recognised practice with known failure modes we should design around, so that whatever this leg
banks is calibrated rather than invented.

The substantive pass for this leg is therefore **inward**: an internal-provenance audit of where
the 10x came from, recorded first, because the gate ("does it still hold **on the same step it
was originally measured on**") is unanswerable without knowing what "the same step" was.

Per `writeup/novelty/README.md`: **links, not counts.** Query strings are verbatim.

---

## Part 1 — INTERNAL PROVENANCE OF THE 10x (the load-bearing part of this pass)

The claim propagates through four files. Only one of them is a measurement; the other three are
restatements, and none of the three carries the measurement's conditions.

| Where | Text | Kind |
|---|---|---|
| `PHASE2_P2_NOTES.md` §34 (M-8) | "81% of a Scenario-2 step (3.4 s of 4.2 s over forty steps at n=801) was inside `natural_spline_slopes` … **43 ms → 4.2 ms per step at n=801**, gated to 2.7e-13" | **the measurement** |
| `capabilities.py:53-55` | "the cached slope operator `slope_matrix` (Route-M: 10x on the Scenario-2 step)" | restatement, conditions dropped |
| `plan_of_record.py:145` | "Route-M made the Scenario-2 step 10x faster (line_hilbert.slope_matrix, gated at 2.7e-13)" | restatement, conditions dropped |
| `solver/line_hilbert.py:125` docstring | repeats the 81% / 3.4 s of 4.2 s profile, but states **no multiplier** | restatement, honest |

**Findings of the provenance audit, before any timing is run.**

* **(P1) The originally measured conditions are fully recoverable.** `n = 801`, forty steps of
  `RescaledHLScenario2.step`, 43 ms/step uncached vs 4.2 ms/step cached — a ratio of
  **10.2x**, which is where the round "10x" comes from. The benchmark this leg builds must
  reproduce *those* conditions, not conditions of its own choosing; anything else answers a
  different question.
* **(P2) The claim is a whole-step ratio, not a kernel ratio.** 43 ms → 4.2 ms is the *entire*
  SSPRK3 step, which also contains three dense Hilbert gemvs. So the claimed 10x is
  **Amdahl-bounded**: with 81% of the step in the sweeps, removing that cost *entirely* caps the
  whole-step speedup at 1/(1−0.81) = **5.3x** — yet 10.2x was reported. The two numbers are
  reconcilable only if the Hilbert-transform part of the step also got cheaper between the
  profile and the timing, or if the 81% figure and the 43 ms figure were taken on different
  code. **This internal inconsistency is recorded here, before measuring, so that it cannot be
  retrofitted to whatever the benchmark returns.** It is the single most likely way the gate
  answers "no" for a reason that is *not* a regression.
* **(P3) A second, distinct 21x is in the record and must not be confused with this one.**
  `PHASE2_P2_NOTES.md:293` and `TECHNICAL_P2_HL_ANCHOR.md:109` report `_slope_matrix`
  **6.15 s → 0.29 s (21x)** — that is the *batched-RHS assembly* of the operator (Thomas sweeps
  vectorised across columns of the identity), i.e. the cost of **building** the cache once per
  grid. It is not the per-step apply. The gate is about the apply.
* **(P4) There is a live correctness gate but no live performance gate.**
  `test_line_hilbert.py::test_slope_matrix_matches_sweeps` checks `S @ f` against the sweeps to
  2.7e-13 *and* checks cache identity (`slope_matrix(X) is S`), so a refactor that deleted the
  cache would be caught. Nothing checks the **magnitude**. That is exactly the hole this leg is
  asked to fill.
* **(P5) The uncached path has itself changed since the claim.** `natural_spline_slopes` was
  rewritten to carry a stacked `(n, k)` right-hand side (for P3's batched assembly). For the
  single-RHS call the integrator makes, the Thomas loops now do NumPy operations on
  shape-`(1,)` arrays instead of scalars. **The uncached baseline may therefore be slower today
  than it was when the 10x was measured** — which would inflate, not deflate, the ratio. The
  benchmark must report the absolute per-step milliseconds on both paths, not only the ratio, or
  this drift is invisible.

---

## Part 2 — OUTWARD PASS: is "assert a speedup factor in a test" a sound method?

### Q1
`performance regression test benchmark speedup assertion flaky CI wall clock methodology`
*(2026-08-05)*

- https://pythonspeed.com/articles/speed-unit-tests/ — Itamar Turner-Trauring, *Unit testing
  your code's performance, part 2: catching speed changes*. Directly on point: argues wall-clock
  assertions in unit tests are flaky because machine load and CPU frequency scaling move the
  number, and recommends measuring something more stable, or comparing two paths **in the same
  process, in the same run**, rather than against an absolute stored time.
- https://bencher.dev/docs/explanation/continuous-benchmarking/ — states the same tension
  explicitly: harnesses use the wall clock because that is what developers care about, and
  general-purpose CI is noisy and inconsistent when measuring it.
- https://medium.com/androiddevelopers/fighting-regressions-with-benchmarks-in-ci-6ea9a14b5c71 —
  Chris Craik (Android): "benchmarks are like flaky tests"; single runs do not give confidence;
  compare with and without the change rather than against a fixed threshold.
- https://arxiv.org/pdf/2408.08148 — *Early Detection of Performance Regressions by Bridging
  Local and Cloud Testing*; same framing, research setting.
- https://arxiv.org/pdf/2204.04321 — MALI ice-sheet paper, noted because it reports the concrete
  failure mode: HPC nodes vary enough that fixed wall-clock performance tests fail with no code
  change at all.

**On-topic finding.** The practice is recognised and its failure mode is well documented. The
mitigation the sources converge on is exactly the shape available here: **a same-process,
same-run A/B ratio** (cached vs uncached on identical inputs) rather than an absolute stored
time, plus **repetition with a robust statistic** rather than a single timing. Both go into the
design below. A ratio also cancels the machine: it is the *only* form of this claim that can be
compared against Route-M's 2026-08-04 number at all, since that was measured on unknown hardware.

### Q2
`tridiagonal Thomas algorithm versus dense matrix multiply BLAS gemv crossover repeated right-hand sides`
*(2026-08-05)*

- https://handwiki.org/wiki/Tridiagonal_matrix_algorithm — the O(n) Thomas algorithm; the
  standard statement of what the cached operator throws away asymptotically.
- https://arxiv.org/pdf/1207.5217 — *Hierarchical Performance Modeling for Ranking Dense Linear
  Algebra Algorithms*; the general framing that BLAS-2 (gemv) is memory-bound.
- https://link.springer.com/chapter/10.1007/978-3-540-72584-8_19 — Thomas-algorithm
  restructuring beating BLAS/LAPACK by 35–54% on a vector machine, i.e. the trade can go the
  **other** way on other hardware.
- https://arxiv.org/pdf/0901.2859, https://arxiv.org/pdf/2502.06296, https://arxiv.org/pdf/1612.01855
  — parallel/dichotomy tridiagonal solvers and multi-RHS triangular solves; adjacent, not
  on-point for a single-threaded NumPy setting.

**On-topic finding.** No source gives a crossover point for "O(n) algorithm in the Python
interpreter vs O(n²) gemv in BLAS", which is the actual comparison here — the win is not
algorithmic (it is asymptotically a *loss*, O(n) → O(n²)) but an interpreter-overhead win, and
it must therefore **shrink as n grows**. That is a falsifiable prediction available to this leg
at no extra cost: the benchmark will sweep n and report the ratio at each, so the audit can say
*whether the 10x is a property of the code or a property of n = 801*. Nothing in the literature
pre-empts this; nothing in the literature is claimed by it.

---

## What this pass licenses

1. Benchmark at **n = 801, forty steps** first, because that is the originally measured
   condition (P1) and the gate names it.
2. Report **absolute ms/step on both paths** as well as the ratio (P5).
3. Add **n = 401 and n = 1601** as context, to separate "the cache works" from "801 is a lucky
   size" (Q2).
4. Bank a regression test as a **same-process A/B ratio with repeats and a median**, never an
   absolute time (Q1).
5. Report the **Amdahl inconsistency (P2)** as a finding regardless of which way the gate falls.

**Novelty claimed: none.** No link of the L1→L4 chain moves. Clay stays ~0.05%.
