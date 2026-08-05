# Leg 56 — Route-TN v1: enclose `L1` step one's other named gap

**Branch `leg/tn-v1`. Exploration route, not critical path. Gate answered NO.**

Quartet: runner `experiments/p2_route_tn_v1_consistency.py`; data
`writeup/data/p2_route_tn_v1_consistency.json`; prose
`writeup/4_p2_lottery/BLOG_P2_ROUTETN_V1.md` + `TECHNICAL_P2_ROUTETN_V1.md`; figure
`fig51_route_tn_v1_consistency.png` rebuilt by
`experiments/p2_route_tn_v1_consistency_evidence.py`, registered in `writeup/build_figures.py`.
Novelty log `writeup/novelty/leg_56.md`.

---

## Order of work

1. **Novelty pass first**, committed before any construction (`b24b5eb`'s parent). Verdict
   `PROCEED_NARROW`, **nothing banked**, six queries logged **with links** — leg 53's
   counts-only log was withdrawn for exactly that failure, so every query carries its URLs.
2. Grepped `capabilities.py` before building (standing ban). Reused `BorderedHL`,
   `line_hilbert_matrix`, `slope_matrix`, `dot2_matvec`, `interval_constants`,
   `radii_verdict`. Nothing was rebuilt from scratch.
3. Read `solver/line_hilbert.py` closely — which changed the leg's shape (see below).
4. Built, measured, ablated, wrote.

## The reading that decided the leg

`line_hilbert_matrix` is **not a quadrature rule.** It applies the *exact* Hilbert transform
of the `C¹` spline interpolant, and `slope_matrix` differentiates the *same* interpolant.
So both consistency defects are one interpolation error seen through two operators — and
because `H` is unbounded on `L^∞`, its defect cannot be bounded from `‖e‖_sup`; it must be
evaluated against an exact reference. That is why the leg needed closed-form *truncated*
Hilbert transforms and rigorous `log`/`arctan`, rather than a one-line estimate.

## What was built

* `solver/interval.py`: `ilog`, `iatan_small`, `ILOG2`, `IPI` — series with **proved**
  remainders, not `np.log`/`np.arctan` (no ULP guarantee available). Domain guards raise.
* `solver/interval_certificate.py`: `SplineConsistency` — the rational test class in two
  families, their closed-form `H f`, `H_M f`, `f'`, and the enclosed defects with widths.
* 5 new gates in `test_interval_certificate.py`, 1 in `test_interval.py`. All 12 pass (414 s).

## Numbers (all in the curated JSON)

Fixed reach `X_max = 745.239` throughout; only `n` moves.

| n | `D` defect | `H` defect | truncation | τ = budget/‖A‖ |
|---|---|---|---|---|
| 201 | 1.1220e−04 | 4.7287e−03 | 1.9042e−02 | 2.3008e−13 |
| 401 | 6.8724e−06 | 4.7131e−03 | 2.2582e−02 | 3.1728e−14 |
| 801 | 4.2738e−07 | 4.7041e−03 | 2.6260e−02 | 2.3056e−14 |

At n = 801: `D` = **1.854e+07 τ** at **order 4.01**; `H` = **2.040e+11 τ** at **order 0.00**.

## Things that could have gone wrong and were checked

* **Lesson 86 (the pre-registered central risk).** Enclosure width/value at n = 801:
  `D` 6.34e−08, `H` 1.15e−13. The bounds are not their own evaluation error.
* **Lesson 85 (re-measure your own headline).** `budget` and `‖A‖_w` re-derive to all
  printed digits from leg 46/50's stored run. `Y₀` does **not** (9.97e−12 vs 7.35e−12
  stored) — a Newton iterate landing differently. It does not enter the comparison, and both
  values are on panel E rather than being quietly dropped.
* **Lesson 90 (a control that cannot come out differently).** The mechanism ablation dials
  *only* the value at the cut, by `M/a ≈ 1490`. `H` collapsed 1503×, matching `M/a` to 1%;
  `D` moved 1.11×. Both moving, or neither, would have refuted the mechanism.
* **Lesson 73.** There is no `‖H_disc − H‖`; the defect is reported as a curve in the test
  class's scale, never as a scalar impersonating an operator norm.
* **Lesson 75.** The far-field term is computed only to be subtracted off and reported
  separately. The banned "extend the domain" move is not made: reach is frozen.
* **The reference is independently verified.** Closed form vs direct PV quadrature sharing no
  code: worst absolute disagreement 4.44e−15 over 12 cases.

## Two bugs found in my own work, recorded because they were nearly shipped

1. **A relative-error test that divided by a true zero.** Gate (8) first used a pure relative
   criterion and failed. The failing cases were *only* the `even` family at `X = 0`, where
   `H_M g` vanishes identically by symmetry — the disagreement there is at the rounding
   floor, and it was the denominator that was wrong, not the integrand. Diagnosed by
   sweeping the quadrature's `N` and seeing the "error" fail to converge, which is the
   signature of a bad denominator. Fixed to a mixed absolute/relative criterion, with the
   reason written into the test. Worst absolute disagreement across all 12 cases is
   **4.44e−15** (`validation.quadrature_worst_abs_disagreement`).
2. **The figure's `Y₀` bar was labelled "leg 46" while plotting my own re-derived value.**
   Caught on visual inspection. Now both bars are shown, labelled separately, and the
   discrepancy is stated in the prose rather than hidden by the label.

## Gate

> Can the `(H, D)` consistency defect be enclosed by a rigorous bound that is smaller than
> leg 46's `Y₀` budget at n = 801, with a convergence rate measured across n = 201/401/801?
>
> **NO.**

No-branch honoured: magnitude and rate reported; the collocation realization cannot carry
`L1`; the coefficient basis is the only lane left for it; **no grid-basis repairs proposed**,
including the boundary-basis change the mechanism obviously invites.

The negative is robust to that artifact: with the `H` defect deleted outright, `D` alone
still needs n ≈ 52,163 (`N = 104,329`, dense) at its measured order 4.

## Ceiling

No statement about `HL_S2_nonsymmetric` being certified, about the far-field gap, or about
the coefficient basis. **No link of the L1→L4 chain moved.** Clay ~0.05%.

## Note for the Decision Maker

Dispatched under the narrow reading of the standing ban on "further ℓ¹-Fourier
radii-polynomial machinery before MM's gate answers" (open direction question #1). This leg
built **no ℓ¹-Fourier machinery**: it works in the sup-norm collocation basis, on the
discretisation defect of stored operators. `DIRECTION.md` on `main` is still at its seed
state and carries no leg 56 entry and no open-question list, so the thesis and gate used here
are the ones in the dispatch prompt, quoted verbatim in the runner docstring and above.
