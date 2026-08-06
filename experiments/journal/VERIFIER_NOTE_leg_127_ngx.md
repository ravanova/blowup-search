# VERIFIER NOTE — leg 127 (Route-NGX), post-landing independent review

**Not a leg. Not a repair.** Independent post-landing verification of leg 127 (`f6c6e41`,
plus novelty `55e849b` and addendum `a8b907b`). Branch `verify/127-ngx-review`. No file
outside this note was edited; nothing pushed to `main`.

**VERDICT: CONFIRMED, with two prose/mechanism gaps in one flagged side-finding.**

The theorem, the `M^{-(1-s)}` law, the exponents, the battery cross-check, the Xu scope
line, and the territory discipline all hold under independent re-derivation and
recomputation. Two statements about *why* the bordering is irrelevant are wrong; they do
not touch Theorem NGX or any banked number.

---

## 1. The proof, re-derived independently — HOLDS

**(T1) is valid and correctly disclaimed.** `x = (I−AL)x + A(Lx)`, then the triangle
inequality and submultiplicativity give `‖x‖ ≤ ‖(I−AL)x‖ + ‖A‖‖Lx‖`. One line, genuinely
folklore, correctly forbidden as a claim by the novelty pass and correctly attributed in
all four artifacts.

**`A` is never decomposed, so `A₂₁` genuinely never enters.** I checked for a hidden block
assumption and there is none: the argument quantifies over a single bounded `A` and uses
only `‖A‖_w`. Leg 58's `A₂₁ = 0` class is the special case, so the supersession claim is
correct.

**The quantifier is stated honestly.** The conclusion is really `limsup_M Z₁(M) ≥ 1` — `A`
must be one fixed bounded operator with `‖A‖_w` uniform in `M`. The theorem says exactly
that ("the truncation of one fixed bounded operator"), and §5 concedes in plain words that
a *fixed-`M`* counterexample is not excluded and that leg 54's `exact_inv` already is one.
No overclaim.

**The singular sequence is well-defined and does what is claimed.** Verified from scratch:

- `h = tail_right_null(K,M)` solves `T h = 0` by a two-term recursion; `G z = −B h` is
  solvable (`G` is nonsingular at even `K`; leg 54 already records odd `K` as singular).
- **`h_m ∼ m^{-2}` re-derived analytically**: the recursion ratio is `(k−3)/(k+1) ≈ 1−4/k`
  over a step of 2 in `m`, so `d log h/dm = −2/m`. **Measured: −2.0007.**
- Hence `‖v‖_w ∼ Σ m^{s-2}` converges iff `s < 1`. **Measured: `‖v‖₁` = 77.198 → 77.696
  over `M = 128…2048`, fitted exponent +0.0023** (bounded, as required).
- **The "one row" claim is rigorous for the *infinite* operator, not merely the
  truncation.** I verified `T` has nonzero diagonal offsets `{−1, +1}` **only**, with an
  exactly zero diagonal at `μ = 0`. Since `T h = 0` exactly and `T` is tridiagonal with
  zero diagonal, `T` applied to the truncated `h` is supported within one row of the cut.
  So the `M^{s-1}` edge size is a two-line analytic computation, not a fit, and `v_M` is a
  genuine singular sequence for the infinite operator. **Measured edge-residual exponent
  −0.6962 vs predicted −0.700; finite-block residual ≤ 2.7e−14 (float zero).**

Both halves of the mechanism therefore check out separately, not just their ratio.

## 2. Numerics, recomputed independently — HOLDS, and is if anything understated

Recomputed in my own script, via a **second code path** (`np.linalg.solve` on the identity
rather than `np.linalg.inv`), using leg 54's **unmodified** `p2_route_mm_v1_shape.assemble`.

- `σ_min` reproduces the banked JSON **to every printed digit** at every `s` and `M`
  (e.g. `s=0.3`: 0.006432331354229795 → 0.0009277828119989831).
- Fitted exponents reproduce **exactly**: **0.9925 / 0.6985 / 0.3202 / 0.0788** at
  `s = 0 / 0.3 / 0.7 / 1.0`.
- **The test the leg did not run: local slopes between consecutive `M`, extended to
  `M = 4096`.** This is the real check that the law is not a pooled-fit artifact:

  | `s` | local slopes `128→…→4096` | `1−s` |
  |---|---|---|
  | 0.0 | 0.9834, 0.9916, 0.9958, 0.9979, **0.9989** | 1.00 |
  | 0.3 | 0.6956, 0.6984, 0.6996, 0.7000, **0.7001** | 0.70 |
  | 0.7 | 0.3279, 0.3220, 0.3174, 0.3139, **0.3111** | 0.30 |

  All three converge **monotonically** to `1−s`. The pooled-fit deviations are finite-`M`
  transient, not noise or a bug. At `s = 0.3` the asymptotic local slope is **0.7001** —
  the banked 0.6985 is conservative. At `s = 0.7` convergence is slower, which fully
  explains the largest reported deviation (0.0219).
- Explicit sequence's ratio equals `σ_min` to all printed digits (the banked
  `1.0000000000045×` is real).
- **Zero-pad audit reproduces 1.3543× exactly** (`s=0.3`, `M=512`) — bounded, not a return
  to `O(1)`. Not a truncation artifact.
- **`μ>0` control genuinely bidirectional**: exponent 0.69788 at `μ=0` → 0.00317 / 0.00000
  / 0.00000 at `μ=0.1/0.5/1.0`. `T`'s max diagonal is 0.0 at `μ=0` and 44.0 at `μ=1.0`, so
  the control changes the operator as intended.
- **196/196 battery rows re-verified** from the banked `A_norm`/`σ_min`: zero violations,
  min slack **7.734300317748637e−10**, bit-identical to banked, at `exact_inv`, `K=64` —
  and `exact_inv` is correctly recorded as *inadmissible*, which is the sharpness
  demonstration, not a loophole.

## 3. The Xu citation (arXiv:2607.19762) — CONFIRMED as claimed

Fetched abstract page and full HTML text.

- Paper is real: **Jie Xu, "The spectral picture of self-similar collapse in the
  Constantin–Lax–Majda equation", submitted 22 July 2026, 41pp**, physics.flu-dyn/math-ph.
- The abstract is quoted **verbatim and accurately** in `writeup/novelty/leg_127.md`.
- **Same operator, not a lookalike**: it linearizes about `Ω(y) = −y/(y²+1/4)` — the
  identical profile this repository anchors on.
- **Space is genuinely origin-`H²`**: `X = {φ odd, φ, φ'' ∈ L²(0,∞), φ(y)=a₁y+o(y)}`.
- **Spectral claim is as stated**: point spectrum exactly `{0,1}` on the odd realization,
  essential spectrum meeting `{Re λ ≥ −1/2}` only in `{Re λ = −1/2}`, explicit Hardy–Mellin
  resolvent bound for `Re z > −1/2`, gap **1/2** after standard modulation.
- **No conflict and no pre-emption**: Xu uses no weighted-`ℓ¹` Fourier space and is not
  computer-assisted, so the "two realizations of one operator" reading is correct and the
  ban-lift disclaimer is right.
- Independent coherence signal: Xu's `0` eigenvalue is the scaling mode; this repo's gauge
  row removes exactly the scaling mode (`e₂`). Consistent.
- **Nuance, handled correctly**: `L₀` itself is *not* invertible on `X` (`0` is an
  eigenvalue) — only the modulated operator is. Every artifact carries the "after
  modulation" qualifier (journal L36-37, novelty F2, TECHNICAL §7, module header, BLOG
  L132-133). The loosest sentence in isolation is BLOG L135 *"So the operator is fine. It
  has a bounded inverse."*, but the preceding sentence names both the space and the
  modulation, so it is scoped in context. Not a gap; noted for the publication pass.

## 4. Territory and non-tampering — CLEAN

- Commit touches exactly **9 files**, all declared territory: its own runner/evidence/JSON/
  figure/BLOG/TECHNICAL/journal, plus `solver/spectral_certificate.py` (declared sole owner
  post-leg-58-merge) and `test_spectral_certificate.py`.
- **5447 insertions, ZERO deletions across the entire commit.** `solver/` is a pure
  end-of-file append at line 804 (`@@ -804,3 +804,121 @@`). The test file adds 2 import
  lines and 95 appended gate lines, no deletions.
- **No leg 54 / leg 58 artifact altered.** `p2_route_mm_v1_shape.py`, its JSON, and all
  prior TECHNICAL/BLOG prose are untouched. Scope-line propagation is correctly left undone
  and declared orchestrator pointer-block work — confirmed not silently performed.
- Worth recording: the operator assembly used is **leg 54's, unmodified**, so the operator
  was not tuned to produce this leg's answer. My recomputation ran against that same module.

## 5. Documentation quartet — complete, one disclosed backlog item

Runner ✓, JSON ✓ (4055 lines), BLOG ✓ + TECHNICAL ✓, fig63 ✓.
**The figure rebuilds byte-identically from the curated JSON alone** (md5
`e0c919b27849736ed588119ab4489e71`, both committed and my scratch rebuild) — genuine
reproducibility, not just a committed PNG.

`fig63` is not registered in `writeup/build_figures.py` (which stops at fig60) and the
TECHNICAL is not in `writeup/README.md`'s 33-entry index. Leg 127 explicitly declared both
out-of-territory. `fig61`/`fig62` are also unregistered, so this is a pre-existing
orchestrator backlog, **not a leg-127 regression**.

---

## GAP-1 — a flagged "finding" states a mechanism that is false

**Locations** (all three carry the same sentence):
- `writeup/4_p2_lottery/TECHNICAL_P2_ROUTENGX_V1.md` §6, "A coincidence that had to be
  interrogated"
- `experiments/journal/leg_127.md`, "Two things worth flagging to the orchestrator", item 1
- `experiments/p2_route_ngx_v1_general.py` ~L343-345, the `"reading"` string baked into
  `NGX5_border_makes_no_difference_at_mu_0` in the curated JSON

**The claim:** *"the singular sequence has exactly zero far-field-amplitude component, so
bordering with that amplitude — leg 52's repair, the whole point of the assembled object —
does not move the obstruction at all."*

**This is false.** The far-field amplitude is finite-block index `K+1`. Measured at `K=4`,
`s=0.3`, `μ=0`:

| `M−K` | `z[K+1]` | as fraction of `‖v‖₁` |
|---|---|---|
| 128 | +4.996088 | **6.4718%** |
| 256 | +5.130518 | **6.6277%** |
| 512 | +5.214343 | **6.7239%** |
| 1024 | +5.266279 | **6.7831%** |

The numerically-optimal near-null vector agrees to 4+ digits (6.4718% at `M−K=128`). The
component is not zero, not machine-epsilon, and **grows** slowly with `M`.

**Magnitude:** claimed 0; actual ≈ **6.5% of the vector's mass** — an infinite relative
error on a quantity asserted as "exactly zero".

**The conclusion survives; the mechanism does not.** I independently confirmed bordered and
unbordered `σ_min` agree to **4.05e−16 / 1.24e−15 / 5.73e−15** at `M−K = 128/512/2048`, so
*"bordering does not move the obstruction / the wall is not where the far-field unknown is
put"* is **TRUE**. The real mechanism, which I measured: the far-field column of the
coupling block, `C[:,K+1]`, is supported on **exactly one row — the truncation edge** (row
127 of 128; row 511 of 512), because the far-field direction `ff["h"]` *is* the tail kernel,
so `T·ff["h"]` vanishes off the edge. The bordering unknown couples into the tail only at
the very row that already carries the entire residual. It is irrelevant because it **cannot
reach anywhere else**, not because the singular sequence avoids it.

**Why this is worth more than a typo.** This is precisely the item the journal elevates as
*"A `μ=0` coincidence was interrogated under lesson 90 and turned out to be a finding."*
Lesson 90 says identical numbers are a bug until the mechanism is proven. The runner
measures the `σ_min` equality and the `μ=0.1` discrimination, but **never computes the
far-field component that would test its own explanation** — even though
`explicit_far_field_direction` already returns the `z` containing it, one line away. So the
lesson-90 interrogation is incomplete, and the mechanism it concluded with is the wrong one.

## GAP-2 — "the sole finite-to-tail coupling entry" undercounts by one (same family)

**Locations:** `TECHNICAL_P2_ROUTENGX_V1.md` §3.1; `solver/spectral_certificate.py`,
`explicit_far_field_direction` docstring.

Both say `z_K = 0` "switches off the **sole** finite-to-tail coupling entry `(1 − K/2)`".
There are **two** finite-to-tail coupling columns in `C`, not one: `C[:,K−1]` (the `(1−K/2)`
entry) and `C[:,K+1]` (the far-field column). `z_K = 0` kills the first; the second is
killed by its own edge-supportedness, not by `z`.

The **"residual = 1 row" conclusion is correct** — I measured exactly 1 row, with
finite-block residual ≤ 2.7e−14 — but it has two ingredients and the writeup names one.
This is the same root cause as GAP-1: the far-field column's edge-supportedness is the
unnamed ingredient in both places.

## Minor observation (not a gap)

`TECHNICAL` §3 reports the `K`-spread of `σ_min` as "0.29% for `s < 1`" vs 2.14 at
`s = 1.5`. Correct as qualified. The `s = 1.0` value, **0.2645 (26%)**, is not mentioned in
that comparison; `s = 1` is outside the theorem's range and is discussed separately, so this
is a completeness note for the publication pass, not a misstatement.

---

## Bottom line

**Theorem NGX is CONFIRMED.** `Z₁ ≥ 1` for every bounded `A` with `A₂₁` free, in `ℓ¹_w` at
every `s < 1`, on the bordered `a=0` CLM linearization. The proof is elementary, correct,
carries no unstated assumption on `A`, and its one non-folklore ingredient — the explicit
singular sequence — is well-defined, analytically justified for the infinite operator, and
numerically reproduced independently. The `M^{-(1-s)}` law is real and converges to the
predicted exponent more cleanly than the banked pooled fits suggest. The Xu citation says
what it is claimed to say, about the same operator, and the "space not operator" reframing
is sound. Territory is clean and no prior leg's numbers moved.

The two gaps are confined to the *explanation* of one side-finding (why the bordering is
irrelevant). Both leave the finding's conclusion intact and neither touches the theorem, the
exponents, the battery, or the scope line. They are, however, in the curated JSON's
`reading` string and so will propagate if quoted.
