# Leg 80 — Route-BHN: adversarial audit of the bordered HL Newton solve

**Agent:** LEG-H. **Branch:** `leg/bhn-v1`. **Date:** 2026-08-05/06. **Claim-bearing.**
**Module under test:** `solver/bordered_hl.py::BorderedHL.newton` — **read, never edited.**

## Gate and answer

> "Under an adversarial battery (near-singular Jacobian at the starting iterate, NaN/Inf-poisoned
> initial guess, a residual sequence oscillating just above and below tolerance), does
> `solver/bordered_hl.py`'s damped Newton solve ever incorrectly report convergence?"

**NO — 0 false reports in 336 cases.** `no` branch: confirmed robust, banked as a permanent
regression test, lands normally on `main`. No escalation.

## Order of work

1. `plan_of_record.py` read; no ban touches this leg (it is an audit of existing infrastructure,
   not a gCLM/Route-D/DSS/2D measurement, and it builds no solver — the "grep `capabilities.py`
   before building" ban was honoured by reading the `bordered_hl.py` entry first, which is where
   the claim under audit lives).
2. **Novelty pass run and committed BEFORE construction** (`writeup/novelty/leg_80.md`, commit
   `ee59c27`). Four verbatim queries, links not counts. It located the failure modes in print and
   sharpened the battery: Deuflhard's NLEQ-ERR λ-collapse termination criterion (Q4) added a
   fourth family the gate did not name, and the scipy/numpy record (Q3) predicted that
   `np.linalg.solve` would *not* raise on the near-singular members. Both predictions were then
   confirmed by measurement.
3. Battery built and run: `experiments/p2_route_bhn_v1_adversarial.py` → curated data
   `writeup/data/p2_route_bhn_v1_adversarial.json` (46.8 s).
4. Banked: `test_bordered_hl_adversarial.py`, 8 gates, 24.4 s.

## The predicate, fixed before the run

`converged` is set as `bool(res[-1] < tol and np.isfinite(res[-1]))`, so the residual is the only
thing it claims. FALSE REPORT was therefore defined as `converged=True` AND
(`‖F(z_returned)‖_∞ ≥ tol` **recomputed independently from the returned iterate**, OR `z_returned`
non-finite). Never read off the returned ladder.

## Magnitudes

| family | cases | false reports | magnitude |
|---|---|---|---|
| well-posed baseline (n=101, 201) | 2 | 0 | 7.42e-15 / 5.33e-15 in 16 steps |
| near-singular Jacobian at `z0` | 11 | 0 | cond(DF) 4.02e+03 → 4.97e+15 → ∞ |
| NaN/Inf-poisoned initial guess | 231 | 0 | 222/231 returned a NON-FINITE iterate; all 231 said False |
| residual oscillating across tol | 8 | 0 | rise ratios 1.02x–1.70x, tol placed strictly inside |
| degenerate root (zero profile) | 4 | 0 | `converged=True`, residual **exactly 0.0**, DF nullity **3** |
| λ-collapse (random starts) | 80 | 0 | collapse **78/80**, worst accepted uphill **2.798e+05x** |

Four reporting weaknesses found, none of them a false report, none patched here:

* **F4** `converged=True` at an exactly singular DF (nullity 3; 102/205 in the all-zero case) with
  the three gauge constants returned exactly as passed in — `(1e6,1e6,1e6)` and `(−3.7,91.2,−0.5)`
  both accepted. The flag never inspects the Jacobian at the returned iterate.
* **F5** λ-collapse: `while lam > 1/1024` exits *at* 1/1024 and `z = z + lam*dz` runs
  unconditionally, so an uphill step of up to 2.798e+05x is accepted silently. NLEQ-ERR treats the
  same event as termination. The module's own docstring already records this event from leg 44.
* **F6** `cond_hist = []` is allocated in `newton()` and never appended to; `hist["cond"]` is
  length 0 in every run, and `np.all(empty < x)` is vacuously True.
* **F7** what the flag is worth in iterate units: σ_min(DF) = **4.504e-04**, cond 6.19e+04, and a
  measured residual response of 1.191e-04 per unit iterate error, so `tol = 1e-13` pins the
  iterate only to ≈ **8.40e-10** — about **3.9 decades** weaker than the 5.66e-15 residual
  `capabilities.py` quotes. Not a defect; the honest conversion, now gated.

Scope-limited (F8, not escalated, not the module's own F): the same production loop driven on a
rootless residual `F(x)=e^{-x}` reports `converged=True` at x = 28.0. That is the documented
limitation of residual-only termination (novelty Q1/Q2), banked only to fix the flag's scope.

## Environment finding, for the bench-repair lane

On this 12-core host an **unpinned** `np.linalg.solve` on the N=205 bordered matrix costs
**1.006 s** vs **0.00082 s** with BLAS threads pinned to 1 — **~1230x**, turning one 16-step
Newton solve from 0.03 s into 20–33 s. Both new files pin threads before importing numpy.
`test_bordered_hl.py` and every other consumer pays this tax today. Environment, not solver.

## Discipline notes

* Two test kinds in the banked file and they are labelled: `test_no_false_convergence_*` are
  soundness gates; `test_characterize_*` describe today's code and **will fail when F4/F5/F6 are
  repaired**. That failure is the intended signal (leg 69's `test_interval_stress.py` precedent).
  They must be converted into soundness assertions, never weakened.
* The gate was decided on the strict reading only. The weaker reading — "converged at a point that
  is not a locally unique root" — is where the exposure lives (F4) and is reported in full, but it
  was not used to flip the gate, because the flag never promised it.
* Prediction scored honestly: the novelty pass predicted the boolean would be hard to fool and the
  reporting around it would be the exposure. Both held. It did **not** predict F4.

## Deliverables

* `experiments/p2_route_bhn_v1_adversarial.py` — the battery runner
* `writeup/data/p2_route_bhn_v1_adversarial.json` — curated data, gate computed off the data
* `test_bordered_hl_adversarial.py` — 8 permanent gates
* `writeup/novelty/leg_80.md` — novelty pass (pre-construction) + technical note
* no figure required
