# Route-NKR v1 — one guard for three pipelines: the Y₀/Z₀/Z₁ fabrication-acceptance gap, closed as a class

**Leg 128. Exploration/repair route (not critical path). Gate answers YES on (b) and (c),
NO on (a) — 17 of leg 116's 21 false-closing certificates now reject, and the 4 that
remain are a named class rather than a leftover.**
Runner `experiments/p2_route_nkr_v1_repair.py` · data
`writeup/data/p2_route_nkr_v1_repair.json` · executable gates
`test_nk_bounds_adversarial.py` (18, of which 7 are leg 116's GAP-PINs inverted) ·
novelty log `writeup/novelty/leg_128.md` · journal `experiments/journal/leg_128.md`.
No figure: this is a repair leg with no curve to plot, and the established convention is
that such legs register none.

Every number quoted below is in the curated JSON.

---

## 1. What was wrong, and why it was a class and not three bugs

Three legs, three modules, one defect. The radii polynomial theorem this repository imports
(van den Berg & Lessard, *Rigorous Numerics in Dynamics*, Notices AMS 62(9):1057, 2015;
Hungria–Lessard–Mireles James, Math. Comp.) defines its constants as upper bounds on norms,

    ‖T(x) − x‖ ≤ Y₀ ,     sup ‖A(DF(x+rv) − A†)u‖ ≤ Z₀ + Z₁ + Z₂ r ,

hence **finite and nonnegative by hypothesis**, and concludes existence and uniqueness of a
zero *inside* the ball of radius `r_min`. A negative constant is therefore not a pessimistic
input — it is an input the theorem says nothing about.

| module | leg | measured | state before leg 128 |
|---|---|---|---|
| `solver/port_certification.py` | 79 | 11/25 hypothesis-violating inputs returned `closes=True` | repaired in place, private `_hypothesis_violations` |
| `solver/interval_certificate.py` | 98 | 12/36, 8 load-bearing | repaired in place, **by copying leg 79's function** |
| `solver/nk_bounds.py` | 116 | 21/52, 19 load-bearing | **not repaired**, by leg 116's own gate |

The second row is the reason this is a leg and not a bench one-off. Leg 98's copy carries a
comment stating its own intent:

> *"Mirrors `solver.port_certification._hypothesis_violations` (leg 79's repair) so the two
> pipelines cannot drift apart on what 'outside the theorem' means."*

An intention not to drift is not a mechanism. `nk_bounds.py` was the third call site, and
three is where the Rule of Three says a copy stops being cheaper than an abstraction (novelty
log §Q1). So the predicate now lives once, in `solver/certificate_guards.py`, and the two
copies are deleted.

## 2. The sharpest case, restated so the repair can be judged against it

Leg 116's substrate is fully explicit: `F(x) = x² − 2` on ℝ, zeros exactly ±√2, approximate
inverse `A = 1/(2·1.4)`. The planted point `x̃ = 1.0` is not a zero — `|F(1.0)| = 1`, and the
nearest zero is `0.4142…` away. Honest constants there **refuse**, and that refusal is the
control.

One forbidden `Z₀ = −1` turned that refusal into `closes=True` with
`r_min = 0.19169540264054277`, i.e. the certified ball `[0.8083, 1.1917]`, which contains no
zero of `F` at all and misses √2 by **1.1607902780527646 ball radii**.

Post-repair the same input returns `closes=False`, `violations` naming `Z_0`'s nonnegativity,
`r_min = NaN`, and no ball — asserted in
`test_repaired_planted_non_solution_no_longer_survives_a_certified_ball`, which keeps the
ball arithmetic and asserts it *unreachable* rather than weakening it.

## 3. Gate (a): 21 → 4, and what the 4 are

Leg 116's battery is run **unmodified**, against both the pre-repair and the post-repair
module, in the same process, by substituting `sys.modules['solver.nk_bounds']` for the
duration of a fresh load (leg 105's technique; leg 116's territory file is never touched).

| | pre-repair | post-repair |
|---|---|---|
| false accepts / hypothesis-violating | **21/52** | **4/52** |
| load-bearing | 19 | 4 |
| degenerate or empty "balls" | 14 | 3 |
| planted-point survivors | 6 | 2 |
| outcomes that moved | — | 31, **0 of them on clean cases** |

The pre-repair column reproducing 21/19/14 exactly is what makes this an instrument rather
than a tautology (lesson 90): the same code path reports both answers.

**The 4 survivors, characterised rather than counted.** Every one supplies constants that are
nonnegative and finite in every slot:

| case | poison | why no guard can catch it |
|---|---|---|
| `P02_Y0_fabricated_zero` | `Y₀ = 0.0` | 0 is a legitimate norm bound; with `Y₀ = 0` the theorem's conclusion — the centre *is* a zero — is **true given the input** |
| `A05_Y0_zero_fabricated` | `Y₀ = 0.0` | same |
| `P09_Y0_tiny_fabricated` | `Y₀ = 1e-300` | positive and finite; a real certificate of radius ~1.4e-300 |
| `P06_Z2_shrunk_1e-6` | `Z₂ = 1e-6` | positive and finite; a magnitude under-reported by six decades |

The fabrication is in the **value**, not the type. `solver/interval_certificate.py`'s own
docstring already states the general fact — *"Validity checking cannot catch this and no
amount of it ever will."* Closing this class would require the **caller** to certify that
`Y₀` came from a residual evaluation rather than a literal, which is a different repair in a
different place. Three of the four are now flagged `degenerate_ball=True` with the mechanism
named, so a caller can at least see that the "ball" is a point.

So gate (a)'s literal wording — *"do **all** 21 … now reject"* — answers **NO**. It is
reported that way rather than by redefining the battery.

## 4. Gate (b): 4626/4626 bit-identical, worst 0 ULP

The instrument is not free, and leg 105 already established which one is wrong here:
comparing against a banked JSON fails, because re-running leg 61's literal original source
today gives `Y₀ = 2.9616e-17` against the committed `3.0243e-17` (~2.1%) — a BLAS/environment
sensitivity of a quantity converged to its own noise floor, predating every repair. So the
instrument is leg 105's: a **same-process bitwise differential** against the sources read out
of git at this branch's merge base, compared with `==` and an ULP distance, not a tolerance.

| function | identical | worst |
|---|---|---|
| `nk_bounds.budget` | 36/36 | 0 ULP |
| `nk_bounds.farfield_modelling_error_bound` | 4032/4032 | 0 ULP |
| `nk_bounds.hilbert_farfield_bound` | 288/288 | 0 ULP |
| `nk_bounds._I_out` | 32/32 | 0 ULP |
| `nk_bounds.quadratic_constant_upper` | 36/36 | 0 ULP |
| `nk_bounds.holder_local_X_constant` | 96/96 | 0 ULP |
| `nk_bounds.two_point_dual` / `sup_part_upper` | 7/7 | 0 ULP |
| `port_certification.radii_polynomial_status` | 50/50 | 0 ULP |
| `interval_certificate.radii_verdict` | 49/49 | 0 ULP |
| **total** | **4626/4626** | **0 ULP** |

All seven sibling suites pass **unedited**, legs 86's and 105's among them:
`test_port_certification_regression.py`, `test_port_certification_postrepair.py`,
`test_port_certification.py`, `test_interval_certificate_postrepair.py`,
`test_interval_certificate_adversarial.py`, `test_nk_bounds.py`, `test_op_lower.py`.

### 4a. The draft that DID move a clean input, and what happened to it

This is recorded because it is the leg's most useful negative result. An earlier draft
refused `r_min == 0.0` whenever `Y₀ > 0`, reasoning that the theorem's `r_min` is strictly
positive there, so a computed `0.0` must be cancellation. It is cancellation — and refusing it
is still wrong. At `(Y₀, Z₀, Z₁, Z₂) = (1e-30, 0.5, 0.4, 2.0)` the honest radius is ≈ 1e-29:
a genuine certificate whose radius is simply below float resolution against `one_minus = 0.1`.
The differential caught it as **36/36 → 35/36**, and the draft was reverted rather than
iterated, per the gate's own no-branch.

What survives is narrower and true: `r_min == 0.0` is **flagged**, with the reason naming
which of the two mechanisms produced it, and the genuine degeneracy underneath — leg 116's
`A21`, where `Z₂ = 1e-320` overflows the budget `Y0_max = one_minus²/(4Z₂)` to `+inf` — is
refused on the **budget** instead of on the radius. That is the distinction the first draft
missed.

## 5. Gate (c): routing, checked three ways

"They share a guard" is unfalsifiable unless it is measured, so it is measured three ways:

* **identity** — `pc._shared_hypothesis_violations is cg.hypothesis_violations`, likewise for
  `interval_certificate` and `nk_bounds`. True for all three post-repair; **False for all
  three pre-repair**, which is what makes it a control.
* **source** — inline copies of the predicate: `port_certification.py` 2 → 0,
  `interval_certificate.py` 2 → 0, `nk_bounds.py` 0 → 0.
* **behaviour** — a 7-case drift battery fed to all three verdict functions; identical
  offending constants, identical violation kinds, identical counts.

**The differences survive as parameters, not flattened.** This was pre-committed in the
novelty pass, because the WET counter-argument ("duplication is far cheaper than the wrong
abstraction") is the real risk of this repair:

| difference | why it is real | how it is carried |
|---|---|---|
| `port_certification` accepts `None` | `None` = NOT MEASURED, its `BLOCKED_AT_STEP_ONE` kill-switch | `allow_none=True` |
| `interval_certificate` raises on `None` | no not-measured branch exists | `allow_none=False` |
| three different NaN parentheticals | the three guard contraction in different senses (`Z₁ ≥ 1` rejects, `Z₁ < 1` accepts, `Z₀ + Z₁ < 1` accepts) | `nan_hint`, the two existing strings reproduced **byte-for-byte** |
| `nk_bounds` has a fourth slot `Z₀` | its contraction condition is `Z₀ + Z₁ < 1` | `(name, value)` pairs, not a fixed signature |

## 6. The other clauses of leg 116's repair list

* **`alpha < 2` in `farfield_modelling_error_bound`** — it returned a `max` over 40 samples
  of the truncated window `[X₀, 10⁴X₀]` and called it a supremum over `{X ≥ X₀}`, valid only
  under the hypothesis its own docstring states. Outside it the claimed bound sat >50× below
  the truth at `α = 2.25`, >5e3× at `2.5`, >5e7× at `3.0`. Now raises. **And** the
  self-diagnostic it was already computing and discarding — `argmax_X` pinned to the window's
  last sample — is returned as `argmax_at_window_end`, gated both ways (False at `α = 1.9`,
  True on a deliberately degenerate window).
* **`gamma ∈ (0, 1]`** — the near-field half carries a `1/γ`, so `γ = −0.5` flipped its sign
  and *reduced* the claimed upper bound. Now raises, including `γ > 1`. The admissible
  endpoints `1e-6, 0.5, 1.0` are asserted still to evaluate, so the guard rejects the range
  and not the function.
* **non-positive `q_cod` / `v_cod` in `two_point_dual`** — the mask `1/q if q > 0 else 0` is
  correct on the suppressed diagonal and a silent fabrication off it, pricing an honestly
  infinite contribution at zero: measured 2.19× (zeroed `q` column) and 3.57× (negative
  `v_cod` entry) *below* the honest bound. Both now raise. The guard is a vectorised numpy
  screen with the message builder behind it, because `seminorm_part_upper` calls
  `two_point_dual` once per chunk on a J×J kernel with J up to 1600 — a per-entry Python loop
  on the clean path would have cost more than the bound it guards. Leg 116's reachability
  result is re-asserted unchanged: `HolderNorm` has minimum off-diagonal kernel 3.58e-01 and
  minimum weight 1.0, so no in-repo path reaches it.

### 6a. The one clause that is FLAGGED, not recomputed — and the magnitude that decides it

`_I_out` grades its bulk panel `[0, X/2]` logarithmically from `eps = 1e-12·max(X,1)`. The
integrand's mass sits at `y = O(1)`, so once `eps` reaches that scale the single panel
`[0, eps]` replaces the resolved mass region and the claimed **upper** bound falls **below**
the truth — 2.12% at `α = 1.9, X = 1e12`, onset at `X = 1e11`.

DIRECTION.md offered "lower the bulk floor **or** bound the `[0, eps]` panel". Neither is
available under this leg's own gate, and the reason is measured rather than argued: lowering
`eps` from `1e-12` to `1e-18` rebuilds the geomspace grid and moves **15 of 15** clean
live-range values, worst **1.08e-04 relative**. Any clean-input result moving is this leg's
stop condition, so the value is untouched and the out-of-validated-range regime **warns**
above `X = 1e10`.

The margin is the honest part of the answer: every in-repo caller stays below `X = 3.2e7`,
**3.49 decades** below the measured first crossover. The pin survives as
`test_still_a_gap_Iout_log_grid_floor_undercuts_the_truth_past_X_1e11_but_now_WARNS`, which
keeps leg 116's 2.12% assertion *and* asserts that the warning fires at `X = 1e12` and stays
silent across the live range.

## 7. What this does not mean

`nk_bounds.py` is Route-D infrastructure; `port_certification.py` and
`interval_certificate.py` are the port's. **What a validation layer restores is the
guarantee, not the margin.** No banked number moved — that is gate (b), measured at 0 ULP
over 4626 comparisons. Every defect leg 116 found was already LATENT (every in-repo caller
passes `Y₀ = 0.0` literally and stays inside `α < 2`, `X ≤ 3.2e7`, worst reference/module
0.99997), and legs 79's and 98's repairs moved no banked number either.

**No link of the L1→L4 chain moved.** Route-D's own ceiling — the discrete-ball trap, the
unbounded core↔far-field coupling, and the three items `nk_bounds.py`'s docstring lists as
NOT bounded — is exactly where it was before this leg, and an audit of input validation
cannot touch it.

## 8. What the next leg on this gets

* The fabricated-**magnitude** class (4 cases) is the only remaining false-accept route
  through `budget`, and it is not closable inside `budget`. It needs the caller to carry
  provenance for `Y₀`.
* `_I_out`'s floor is closed only as a warning. Closing it in value means accepting that
  clean `_I_out` values move by up to 1.08e-04 relative, which is a decision for whoever owns
  the banked Route-D numbers, not for a repair leg forbidden to move them.
* `solver/certificate_guards.py` has no `test_certificate_guards.py`. It is exercised
  through all three modules' suites and through
  `test_repaired_all_three_modules_share_one_guard`, but a dedicated file was outside this
  leg's declared territory and is the obvious next brick.
