# VER-C review of leg 56 (Route-TN v1), branch `leg/tn-v1` @ `68d1713`

**Verdict: one substantive gap, prose-only. Every number, the gate answer, and the ceiling
discipline are independently reproduced and sound. The leg's central STRUCTURAL claim about
`line_hilbert_matrix` is false as written, and I falsified it by direct computation.**

The gate answer does not change. It gets stronger.

---

## 1. What I confirmed independently (not by re-reading)

**Territory and the index.** Diff against `main` is exactly the 13 declared files.
`writeup/build_figures.py` is a clean 3-line append inside `P2_EVIDENCE`; it does not touch
leg 53's entry. `DIRECTION.md` has a net-zero diff against `main` (commit `68d1713` restored
quoted text into the journal and TECHNICAL, not into `DIRECTION.md`).

**`capabilities.py`: no new entry was required, and this is the correct outcome.**
`test_capabilities.py` indexes at *module* granularity (`test_every_solver_module_is_indexed`
walks `solver/*.py`). Both `solver/interval.py` and `solver/interval_certificate.py` are
pre-existing indexed modules; leg 56 added classes and functions to them, not a new top-level
module. **Leg 56 did not repeat the miss that sent legs 54, 55 and 57 back.** (Soft note in §4.)

**Tests.** `test_interval.py` passes; `test_interval_certificate.py` passes all 12 gates.
Gates (8)–(12) test what the prose says they test, not a weaker proxy — (11) in particular
asserts `H` is flat to within 5% over the 4× refinement, which is falsifiable in the direction
that matters: a future fix that makes `H` converge *fails* this gate and forces a re-read.
That is the right way round.

**Every number in BLOG and TECHNICAL traces to the curated JSON** at the stated precision. I
checked all of them, including τ = 2.306e−14, the two defects (4.274e−07 / 4.704e−03), the
ratios (1.85e+07 / 2.04e+11 / 1.14e+12), orders 4.03/4.01 and 0.00, the 1.0052× total over the
4× refinement, the ablation column (1421×/1516×/1503× and 1.12×/1.11×/1.11×), M/a = 1490.5,
n ≈ 52,163 and N = 104,329, the width/value pair (6.34e−08, 1.15e−13), the scale curve, and the
validation widths (ilog 3.55e−14, iatan 1.48e−14, quadrature 4.44e−15 over 12 cases). No
orphan numbers.

**The figure rebuilds bit-identically from the JSON** (md5 match after re-running the evidence
script). Panel E shows **both** `Y₀ leg 46, stored` (7.35e−12) and `Y₀ re-derived here`
(9.97e−12) as separate, separately-labelled bars. The self-reported mislabelling is genuinely
fixed, and no other number reported anywhere as "leg 46's `Y₀`" changed — the pre-committed
`Y₀/budget = 2.068e−02` is carried in `leg46_reference_as_stored` and quoted unaltered.

**Lesson 86 does not bite, and I checked it at the level of the remainder terms rather than
accepting the width ratio.** `_atanh_series`' geometric majorant
`|z|^(2N+1)/((2N+1)(1−z²))` is the correct tail for `|z| ≤ 1/3`, and `zp` after the loop is
indeed `z^(2N+1)`. `iatan_small`'s alternating-series first-omitted-term bound is valid for
`|t| ≤ 1`. The `gamma(3*nterms)` accumulation factor is conservative against the true
per-term op count. `ILOG2`/`IPI` widen the nearest double outward in **both** directions, so
containment does not depend on the comment's claim about which side the double falls on.
Empirically: **0 containment failures in 30,009 `ilog` samples spanning `5e−324` to `1e300`
and 30,005 `iatan_small` samples**, against an 80-digit `decimal` reference computed
independently of the leg's own. The bounds are bounds.

**I re-derived the closed form from scratch.** Partial fractions of
`−u/((u²+a²)(X−u))` give `α = γ = −X/(X²+a²)`, `β = a²/(X²+a²)` — matching the module's
`A = C`, `B` exactly — and integrating reproduces the stated
`π H_M f = (A/2)ln(...) + (B/a)(atan(u₂/a) − atan(u₁/a)) − C ln|(x−M)/(x+M)|`, including the
sign of the last term. The cancellation-free rewrite
`π − (atan(u₂/a) − atan(u₁/a)) = atan(a/u₂) + atan(a/(−u₁))` is correct and is what keeps the
arctan arguments inside `iatan_small`'s proved domain.

**I closed a coverage hole in the leg's own validation.** Gate (8) checks the closed form
against quadrature at nodes `j = 60, 100, 140` only. The sup of the H defect is **not** there —
I located it at **node index 1**, the first interior node, immediately adjacent to the excluded
endpoint. So the headline 4.7287e−03 is produced exactly where the reference was never
cross-checked, and where the `−C ln|(x−M)/(x+M)|` term is nearly singular. I ran my own
60-point composite Gauss–Legendre PV quadrature (no shared code with the leg) at `j = 1, 2, 5,
199` for both families: **agreement to 1.2e−15 relative or better at every one**, including
the argmax node. The reference is right where it matters. Hole closed, no finding against the
leg's numbers — but the gate should have covered an edge node.

I also confirmed the even family's truncated transform is genuinely **zero** at `X = 0` (my
quadrature: 4.6e−16; closed form: 7.1e−17), which independently vindicates the leg's
self-reported fix from a pure-relative to a mixed abs/rel criterion. It divided by a true zero.

**The ablation is real and not cherry-picked.** Mismatch between the H collapse and `M/a`:
**4.69% at n=201, 1.74% at n=401, 0.83% at n=801** — converging toward the prediction as the
grid refines, which is a stronger result than the leg claims. "Within 1%" is true at n=801,
the rung quoted, and the TECHNICAL table prints all three rungs.

---

## 2. THE GAP: the structural claim the leg turns on is false as written

BLOG §"Then: the two operators turn out to be the same operator", TECHNICAL §3, the journal's
"The reading that decided the leg", and novelty Q2's "Read" all assert:

> `H_disc f = H(Π_n f)` and `D_disc f = (Π_n f)'` — the **same** interpolant — so
> "both consistency defects are **one interpolation error** `e = Π_n f − f`, seen through two
> different operators."

**They are not the same interpolant, and the two defects are not one error.**

`D` is bit-identical to `_slope_matrix(X)`, the full natural-spline slope matrix, endpoint
columns nonzero (max 0.0223). So `D_disc f = (Π_n f)'` is correct.

`line_hilbert_matrix` zeroes the endpoint columns of **both** `Hp_full` and `Hq_full`
(`[:, 1:-1]`), so the object it transforms is `Π⁰_n f` — the interpolant with the endpoint
**values and slopes dropped** — not `Π_n f`. I measured the difference directly at n=201,
node `j = 1` (the argmax), against my own quadrature of the actual spline:

| quantity | value |
|---|---|
| `H_disc f` (as built) | −1.858472e−03 |
| `H(Π_n f)` — the true interpolant | −1.488064e−03 |
| `H(Π⁰_n f)` — endpoint values zeroed | −1.852643e−03 |
| `H_M f` — the exact reference | −1.488558e−03 |

`H_disc` tracks `Π⁰`, not `Π`. The genuine interpolation error through `H` at that node is
**4.9e−07**, not 4.7e−03 — a factor of 750.

**And the honest interpolation error converges.** Weighted defect of `H(Π_n f) − H_M f` over
the edge nodes:

| n | true-interpolant H defect | as-built H defect |
|---|---|---|
| 201 | 6.3159e−06 | 4.7287e−03 |
| 401 | 1.7022e−06 | 4.7131e−03 |
| 801 | 4.4181e−07 | 4.7041e−03 |

Order ≈ **1.9**, converging. So the leg's flagship finding — "`H` does not converge at all;
refinement is not a lever; no `n` closes this" — is **entirely** an artifact of two dropped
matrix columns, and is **not** a property of the spline-Hilbert discretization. The
spline-Hilbert method converges; this repository's matrix drops the endpoint basis.

**This does not change the gate answer, and it strengthens it.** Honestly attributed, the H
defect at n=801 is 4.42e−07 ≈ **1.9e+07 τ** converging at order 1.9, which would need
**n ~ 5e6** to reach τ — worse than `D`'s 52,163. Every headline survives untouched: gate =
NO, τ = 2.306e−14, `D` at order 4.01, the D-only fallback at n ≈ 52,163, the ceiling, the
novelty verdict. The leg protected itself correctly with the D-only extrapolation.

**What is wrong is the mechanism narrative, and it is wrong in the way lesson 85 and the leg-53
post-mortem name: "the conclusion survives; the mechanism did not."** The leg's own §8 /
§"Why" section *empirically contradicts* its §3 — it discovers the endpoint drop and localises
it correctly — but the writeup never says §3 was falsified by §8, and leaves the false
identity standing as "the structural fact the leg turns on." A later leg grepping
`line_hilbert.py` will read TECHNICAL §3 and believe `H_disc f = H(Π_n f)`.

Note this is a **prose-only** correction. No number changes, no recompute, no figure rebuild.

---

## 3. Minor

* **BLOG line 43**: "`H_disc` is an 805 × 805 matrix" — wrong under any reading. `H` is
  `n × n` (801×801 at n=801); 805 is `N = 2n+3` at n=401.
* **`mechanism_ablation.value_at_cut_ratio_odd_over_even`** is computed as
  `float(abs(o["f_norm_w"]) and (X_max / 0.5))` — a tautological expression with a dead guard
  that hardcodes `a = 0.5` and never evaluates `f` at `±M`. The value is analytically exact
  (`|odd(M)|/|even(M)| = M/a`) and identical across rungs for a legitimate reason, so this is
  not a lesson-90 violation — but it is a control **asserted by the code rather than measured**,
  and it would silently go wrong if `SCALES` changed. Worth wiring through.
* **TECHNICAL §7**: "`H` is flat at 4.704e−03 across the whole range" — at `a = 32` it is
  4.6954e−03. Total spread 0.185%. Trivial.
* **`ilog` argument reduction**: `m − 1` is exact by Sterbenz, but `m + 1` is not, so
  `z = (m−1)/(m+1)` carries up to ~1 ulp of rounding that is **not** in the docstring's
  "proved remainder". It is absorbed with ~15× margin by the conservative `gamma(3N)` slack
  (and I verified containment on 30k samples), so this is a documentation gap, not a
  correctness failure. The proof text should mention it.
* **`capabilities.py` staleness**: no new entry was needed, but the `holds` fields of the two
  touched entries were not updated to mention `ilog`/`iatan_small` or `SplineConsistency`. The
  index is the thing that stopped Route-M rebuilding a solver from scratch; a leg grepping for
  "rigorous log" or "spline consistency defect" now finds nothing.

## 4. Interpretive caveats — declared by the leg, not gaps

* The defect is measured on a rational test class, never on the actual stored profile. This is
  inherent (the profile has no closed-form `H`, which is *why* the class exists) and TN-1
  declares it. The scale curve covers robustness reasonably: even the smoothest class member
  floors `D` at 7.13e−08 = 3.09e+06 τ.
* τ = budget/‖A‖_w compares an operator defect applied to a normalized test function against an
  admissible *residual* perturbation. TN-5 states the direction of the inequality and claims
  only that direction. Sound.

## 5. Open, and explicitly not mine to resolve

Open direction question #1. The live ban reads "building any further **ℓ¹-Fourier**
radii-polynomial machinery for this operator before `MM`'s gate answers". Leg 56 is sup-norm
collocation — different basis, different modules, no file overlap — so the narrow reading
exempts it. The leg flagged this itself and did not attempt to resolve it. **Recording, not
resolving.** If the orchestrator or user reads the ban broadly, this PR should be pulled
regardless of anything above.

---

## 6. Sign-off

**Conditional.** The mathematics, the numbers, the enclosures, the gate answer and the ceiling
are sound and independently reproduced — I would merge on all of that. I would **not** merge
the structural claim in §2 as written, because it is false, it is load-bearing for how the next
leg reads `line_hilbert.py`, and fixing it costs one paragraph in four files and zero compute.

Recommendation: send back for a prose-only correction of the `Π_n` vs `Π⁰_n` identity (BLOG
§"the two operators turn out to be the same operator", TECHNICAL §3, journal "The reading that
decided the leg", novelty Q2), stating that §8 falsifies §3 and that the honest interpolation
error converges at order ~1.9 while the as-built defect does not. The gate answer and every
number stay exactly as they are.

*— VER-C, paired verifier to leg 56.*
