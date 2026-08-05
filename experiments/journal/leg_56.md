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

## The reading that decided the leg — **and the one I got wrong**

`line_hilbert_matrix` is **not a quadrature rule.** It applies the *exact* Hilbert transform
of a `C¹` spline. Because `H` is unbounded on `L^∞`, its defect cannot be bounded from
`‖e‖_sup`; it must be evaluated against an exact reference — which is why the leg needed
closed-form *truncated* Hilbert transforms and rigorous `log`/`arctan` rather than a one-line
estimate. All of that stands.

**What I got wrong, caught by VER-C, corrected in place:** I claimed `slope_matrix`
differentiates the *same* interpolant, so both defects were "one interpolation error through
two operators". False. `line_hilbert_matrix` assembles source columns for **interior nodes
only** (`Hp_full[:, 1:-1] = HP`), dropping the two endpoint basis functions, so it transforms
an **endpoint-zeroed** interpolant `Π⁰`. `D` really does use the full natural-spline slope
operator. They are different discretisations.

I re-derived this independently before rewriting rather than taking the review on trust.
At n = 201, node 1: `H_disc` = −1.8584719686e−03 matches `H(Π⁰f)` by PV quadrature to
**2.61e−15**, while `H(Πf)` = −1.4880639571e−03 differs by 3.70e−04. I also built a
full-interpolant Hilbert matrix (endpoint hats restored as one-sided half-hats) that
reproduces the quadrature to **4.34e−19**, which made the decomposition ladder cheap.

**The split** (`H_attribution`), all three rungs:

| n | total (gated) | endpoint zeroing | true interpolation | interp. order |
|---|---|---|---|---|
| 201 | 4.7287e−03 | 4.7351e−03 | 6.3159e−06 | — |
| 401 | 4.7131e−03 | 4.7148e−03 | 1.7022e−06 | 1.89 |
| 801 | 4.7041e−03 | 4.7046e−03 | 4.4181e−07 | **1.95** |

The artifact is **the whole defect** (share 1.00009 at n = 801), which is why the total does
not converge. **The gate answer is unaffected and strengthened:** the genuine interpolation
error, converging at order 1.95, would need **n ≈ 4.43e+06** to reach τ — an order of
magnitude worse than the derivative side's 5.22e+04.

**The lesson for me.** My own §8 ablation already refuted §3 and I shipped both: a dial that
leaves interior smoothness untouched cannot move a pure interpolation error 1503× while
moving the derivative's by 1.11×. The contradiction was inside the same document. *A
mechanism section and a results section that disagree is a finding, not a formatting
problem — reconcile them before shipping.*

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
3. **The shared-interpolant claim** (above) — not caught by me, caught by VER-C. The worst of
   the three, because it was a *mechanism* claim contradicted by my own measurements.

## Gate

> Can the `(H, D)` consistency defect be enclosed by a rigorous bound that is smaller than
> leg 46's `Y₀` budget at n = 801, with a convergence rate measured across n = 201/401/801?
>
> **NO.**

No-branch honoured: magnitude and rate reported; the collocation realization cannot carry
`L1`; the coefficient basis is the only lane left for it — which makes `L1`'s fate identical
to `MM`'s; **no grid-basis repairs proposed**, including the boundary-basis change the
mechanism obviously invites. That last clause follows from the gate's wording and is not a
prediction about leg 54, which is live and unanswered as this is written.

The negative is robust to that artifact: with the `H` defect deleted outright, `D` alone
still needs n ≈ 52,163 (`N = 104,329`, dense) at its measured order 4.

## Ceiling

No statement about `HL_S2_nonsymmetric` being certified, about the far-field gap, or about
the coefficient basis. **No link of the L1→L4 chain moved.** Clay ~0.05%.

## Left undone on purpose — one item for integration

VER-C also flagged that `capabilities.py`'s `holds` fields for `solver/interval.py` and
`solver/interval_certificate.py` do not mention the new capabilities (rigorous `ilog` /
`iatan_small`; `SplineConsistency` and the `(H, D)` consistency defect). **`capabilities.py`
is not in this leg's declared territory**, and a diff outside it fails the merge gate, so it
is deliberately untouched. `test_capabilities.py` passes as-is. Suggested text for whoever
folds this in:

* `solver/interval.py` — add: *rigorous `log` and `arctan` (`ilog`, `iatan_small`) built from
  series with proved remainders, plus enclosures of `log 2` and `pi`.*
* `solver/interval_certificate.py` — add: *`SplineConsistency`: the `(H, D)` consistency
  defect at fixed reach, on a rational test class with closed-form truncated Hilbert
  transforms; measured NO against the certificate's own budget at leg 56.*

## Note for the Decision Maker

Dispatched under the narrow reading of the standing ban on "further ℓ¹-Fourier
radii-polynomial machinery before MM's gate answers" (open direction question #1). This leg
built **no ℓ¹-Fourier machinery**: it works in the sup-norm collocation basis, on the
discretisation defect of stored operators.

`main` advanced during the leg (`94eeb79`, the DM's queue for 54–60) and has been merged in.
The leg 56 entry there — thesis, gate, both branches, territory — **matches the dispatch
prompt this leg worked from**, and the work was checked against it after the merge. The only
wording the prompt had condensed is the no-branch's closing clause, "which makes `L1`'s fate
identical to `MM`'s", now restored in the gate answer above and in the technical writeup.
