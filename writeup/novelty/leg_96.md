# Leg 96 novelty pass — Route-LHA: adversarial audit of `solver/line_hilbert.py`

Run BEFORE construction, per the leg contract. Pass date: 2026-08-06.

## Question being claimed

> "Under an adversarial battery of near-degenerate non-uniform grids (near-duplicate points,
> extreme local stretching ratios), does `solver/line_hilbert.py`'s dense operator or its cached
> `slope_matrix` ever silently return a finite, plausible-looking wrong result instead of
> propagating or flagging the ill-conditioning?"

## In-repo prior art

| source | what it covers | overlap with leg 96 |
|---|---|---|
| `test_line_hilbert.py` (7 tests) | `d/dx sin` slopes on a sinh grid; `A`/`B` special values and a direct-quadrature cross-check; the CLM known-answer pair (rel 1.6e-4); a resolution ladder; matrix reuse; `slope_matrix` vs the Thomas sweeps (2.7e-13) | none. Every grid in the file is a smooth `sinh`-stretched or uniform mesh, i.e. bounded, monotone, gently graded. Grep over the file for `nan`, `inf`, `duplicate`, `adversarial`, `cond`: **zero hits**. No malformed, repeated, or violently graded grid is ever constructed. |
| leg 75 (Route-M, `slope_matrix`) | built and benchmarked the cached dense slope operator; 10x on the Scenario-2 step | **speed only.** Its exactness claim is an association-change claim on the *same well-behaved sinh grids*, not a conditioning claim. |
| `solver/hl_rescaled.py`, `solver/gclm_rescaled.py`, `solver/gclm_family.py`, `solver/bordered_hl.py`, `solver/interval_certificate.py`, `solver/weight_search.py` | six downstream consumers, all of which build their grid with the same monotone `sinh` stretch | consumers, not audits. None validates the grid it hands in; none checks `line_hilbert_matrix` for conditioning. |
| legs 69 / 79 / 80 / 83 / 85 / 88 / 89 / 91 / 92 | adversarial audits of other modules (`interval.py`, `bordered_hl.py`, `gclm_family.py`, …) | same *pattern*, different module. Leg 69's found a real gap; leg 88's answered NO over 37 cases. Precedent for the method and for the robustness-vs-measurement ban ruling below. |
| `test_bordered_hl_adversarial.py`, `test_gclm_family_adversarial.py`, `test_target_norm_adversarial.py` | the adversarial batteries already on main | different objects. **No file in the repository ever hands `line_hilbert_matrix` or `natural_spline_slopes` a non-monotone, repeated, or extremely graded grid.** |

The question is unasked in this repository. The gap is sharper than a generic "untested path"
because `capabilities.py:57-62` registers the module's `holds` as "spline-analytic H on a
**NON-uniform** grid" — non-uniformity is an advertised capability, and the advertised capability
is the one with untested degenerate cases.

## Capabilities grep (ban 10, discharged)

`grep -n -i "hilbert" capabilities.py` → `capabilities.py:57` registers
`solver/line_hilbert.py`, object "Hilbert transform on the whole line", `holds` as quoted above,
`validated` "the CLM known-answer pair to rel 1.6e-4; the cached slope operator matches the Thomas
sweeps to 2.7e-13", `test: test_line_hilbert.py`. Also present: `solver/hilbert_holder.py`
(weighted-Hölder *bound*, not a discrete operator) and `solver/hilbert_pointwise.py` (pointwise
`|H(h)|` bound, "no known-answer gate; sampled"). Neither is a discrete non-uniform-grid Hilbert
transform and neither registers a grid-validation or conditioning capability. **Nothing to reuse;
nothing to rebuild.** This leg builds no solver — it builds a battery around an existing one.

## Ban check (`plan_of_record.py`, printed 2026-08-06)

All ten live bans read against this leg:

- *another gCLM measurement leg* — not engaged. This leg produces no profile, no `a`-sweep, no
  self-similar exponent, and makes no claim about the gCLM model. It measures a **numerical
  linear-algebra property of a transform routine** on synthetic grids. Same
  robustness-vs-measurement distinction that cleared legs 83, 85, 88; verified here independently
  rather than inherited. The one physics object that appears — the CLM pair
  `f = -4X/(1+4X²) → H(f) = 2/(1+4X²)` — appears only as a **known answer to score the code
  against**, exactly as `test_line_hilbert.py` already uses it.
- *Route-D bound-sharpening*, *DSS re-ask*, *2D beta*, *scaling gauge*, *GA on unvalidated
  fitness*, *the four leg-51/53 reading bans*, *Chen-Hou as target* — none touches a discrete
  Hilbert operator's grid conditioning.
- *building a solver without grepping `capabilities.py`* — discharged above.

## External literature

The claim is about **this repository's discretization**, not about mathematics. The underlying
analytic content — the C¹₀ Hermite basis with closed-form bounded Hilbert transforms — is
Appendix C.1 of Huang–Tong–Wang arXiv:2603.25104, already cited in the module docstring and
already resolved by the repository. This leg does not extend, contest, or re-derive it: A(s), B(s)
and the diagonal limits are taken as given and are the *reference*, not the claim. What is being
measured is whether **this implementation's** finite-precision behaviour degrades loudly or
quietly when the grid violates the implicit well-gradedness assumption that the published method
carries but never states as a hypothesis in the form the code needs it. No arXiv precedence
question arises, for the same reason recorded at leg 88.

One reading note that shapes the design and is worth recording, since it is the difference between
an honest audit and a rigged one: a near-degenerate grid makes the *interpolant itself* a poor
representation of `f`, so a large error there is not automatically a code fault. The battery must
therefore separate (i) error the mathematics forces on any correct implementation from (ii) error
this implementation introduces or hides. That separation is made by scoring **only at nodes far
from the perturbation**, by carrying an unperturbed control grid of the same size, and by asking
whether the returned numbers are *finite and plausible* rather than merely *inaccurate*.

## Verdict

Novel within the repository. Proceed to construction.

---

# Leg 96 findings (written after the run)

## Gate answer: NO

> "Under an adversarial battery of near-degenerate non-uniform grids (near-duplicate points,
> extreme local stretching ratios), does `solver/line_hilbert.py`'s dense operator or its cached
> `slope_matrix` ever silently return a finite, plausible-looking wrong result instead of
> propagating or flagging the ill-conditioning?"

**No — 0 silent corruptions in 25 in-scope cases.** Confirmed robust; the battery is banked as
`test_line_hilbert_adversarial.py` (8 tests, all passing). `solver/line_hilbert.py` was not
edited, under this or any outcome.

Worst module-vs-independent-reference disagreement over the whole in-scope battery:
**3.07e-13** on the dense operator and **7.04e-16** on the slope operator, against a
pre-committed threshold of 1e-08 — i.e. the module clears its own gate by **4.5 orders of
magnitude** on the transform and by **7 orders** on the slopes.

## The methodological point, first, because the leg turns on it

**Scoring against the analytic answer alone would have produced a FALSE YES.** Three in-scope
cases miss the exact `H(f) = 2/(1+4X²)` by **1.3e-02**, **2.9e-01** and **1.3e+02** relative
while returning finite, unflagged output — and in all three the code is doing its job perfectly.
A near-degenerate grid makes the cubic spline interpolant a poor representation of the field, so
that error is what *any* correct implementation of Huang–Tong–Wang App. C.1 must produce. It is a
property of the grid, not a fault of the module.

Separating the two required an **independent implementation of the same discretization**, built
in `experiments/p2_route_lha_v1_adversarial.py` and sharing no formula with the module:

| | module | independent reference |
|---|---|---|
| slopes | two hand-rolled **unpivoted Thomas sweeps** | dense assembly + `np.linalg.solve` (**LU with partial pivoting**) |
| transform | closed forms `A(s)`, `B(s)` with a hand-removed cancellation (the L-series) | **exact per-cell Cauchy integration by polynomial deflation**, `∫p(z)/(w−z) = p(w)ln|w/(w−H)| − ∫q`, with a geometric-series far-field branch for `|w| > 2H` |

The reference is itself gated before use: on healthy grids it reproduces the module's **full
N×N matrix to 7.9e-15 relative** (`reference_selfcheck` in the JSON; `test_reference_selfcheck`
in the regression file). That gate earned its keep — it caught the reference's own first bug, a
dropped log-cancellation between adjoining cells, which presented as a clean O(h) bias and would
otherwise have been read as a module defect at the 2e-02 level.

## Magnitudes

| family | cases | worst matrix disagreement vs reference | behaviour |
|---|---|---|---|
| near-duplicate nodes, forward, separations `1e-1·h` → **1 ulp** (2.2e-16 absolute) | 8 | **4.1e-15** | graceful; error vs analytic grows 4.6e-04 → 4.1e-02 |
| near-duplicate nodes, **crossed** (the inversion roundoff produces) | 3 | **8.1e-15** | indistinguishable from the forward case |
| near-duplicates at the left edge, right edge, far tail | 3 | **2.6e-14** | no edge-case asymmetry |
| **19 simultaneous** collapsed spacings | 1 | **7.9e-15** | no accumulation |
| one cell compressed, ratios to **5.2e+15** | 6 | **3.2e-15** | error vs analytic unmoved at 5.7e-04 |
| one node displaced to +1e6 (ratio 1.9e+07) | 1 | **7.7e-16** | 9.9e-02 vs analytic — **representational, and the reference proves it** |
| geometric grading, spacing ratios to **1.0e+148** | 3 | **3.1e-13** | see below |
| **exact** duplicate | 1 | — | **100% non-finite, 16 warnings** |

Grid pathology actually reached: minimum spacing **7.4e-146**, maximum spacing ratio
**1.0e+148**, `‖S‖∞` up to **4.0e+145**.

### The exact duplicate is the boundary, and it is loud
A repeated node makes the interpolation problem genuinely undefined, and the module does the
right thing: the dense operator goes **100% non-finite** and **16 RuntimeWarnings** are raised.
It propagates. The independent reference goes 100% non-finite too. That is the "propagating or
flagging" branch of the gate, exercised.

### The slope operator never needed a pivot, for a structural reason
The unpivoted Thomas sweeps match pivoted dense LU to **7.0e-16** on every degenerate grid
tested. This is not luck and should not be re-measured by a later leg: the interior system has
diagonal `2(h_{i−1}+h_i)` against off-diagonals summing to `h_{i−1}+h_i`, so it is **strictly
diagonally dominant by a factor of exactly 2 for every grid**, however degenerate. No pivot is
ever required, so omitting pivoting cannot cost anything. Recorded here so the property is
available as a reason rather than as an observation.

## Two things measured that the gate did not ask for

### C1 — `capabilities.py`'s "matches the Thomas sweeps to 2.7e-13" is a healthy-grid figure
Route-M (leg 75) replaced `natural_spline_slopes(X, f)` with `slope_matrix(X) @ f` and gated the
change at 1e-12 on sinh grids. On a grid with a one-ulp cell the same quantity —
`|S@f − sweeps|∞ / |slopes|∞` — reaches **2.5e-01**. That is **eleven orders** worse than the
recorded figure.

**The operator is not losing accuracy.** `‖S‖∞` grows from **4.1e+01** to **9.0e+15** across that
range, and normalized by `‖S‖∞‖f‖∞` — the quantity a backward-stable gemv actually bounds — the
disagreement **never leaves 1e-16** (worst **2.4e-16** over the whole battery, while `‖S‖∞`
spans 144 orders of magnitude). The naive ratio degrades because the operator norm explodes, not
because the association change went wrong. Route-M's exactness claim survives intact; what does
not survive is reading its *number* as grid-independent. Pinned as
`test_characterize_association_claim_is_grid_dependent`. **Not repaired under this leg** — no
edit to `solver/line_hilbert.py` or `capabilities.py` was authorised, and none was made.

### C2 — grid MONOTONICITY is an unstated precondition, and violating it is silent
**Out of the gate's scope** (which names near-duplicates and stretching, not ordering), so it is
reported here and **not counted toward the verdict**. On a strictly *descending* grid the module
returns **exactly `−H(f)`**: the sign-flipped result agrees with the negation of the ascending
answer to **8.9e-16**, is entirely finite, peaks at **1.999** — the correct magnitude — and
raises **zero** warnings. A locally non-monotone grid (one swapped adjacent pair) puts the module
and the reference **1.12 relative** apart.

Three qualifications, all of which matter and none of which cancel the finding:

1. **It is a property of the method, not a bug unique to this module.** The independent
   reference sign-flips too. The orientation convention is inherited from the analytic formulas.
2. **It is latent, not live.** Every consumer in the repository — `hl_rescaled`,
   `gclm_rescaled`, `gclm_family`, `bordered_hl`, `weight_search`, `interval_certificate` —
   builds its grid as `sinh` of an ascending `linspace`, so all are strictly increasing today.
   Checked directly, not assumed.
3. **The module states no monotonicity precondition anywhere**, and a caller cannot tell from
   the output that one was violated: finite, right magnitude, wrong sign.

Pinned as `test_characterize_monotonicity_is_an_unstated_precondition`. This is the one place a
future leg with edit authority over `solver/line_hilbert.py` could cheaply add value — a two-line
`np.diff(x) > 0` assertion in `line_hilbert_matrix` — and it is **deliberately left undone here**
because leg 96's contract forbids editing the module under any outcome.

## The honest limit of the NO

The module carries **no grid-quality diagnostic at all**. On the one-ulp grid it returns an
operator that is right to **6.5e-15** entrywise and an *answer* that is wrong by **1.3e-02**; at
grading `r=10` the answer is wrong by **29%**. Both are finite, plausible and unflagged, and the
module is *correct* in both — it faithfully transforms the spline it was handed. Only the caller
can tell that the mesh was unusable. The single consolation, also pinned: push the grading to
`r=100` and the failure stops being plausible, the peak reaching **141x** the true peak, which is
visible to anyone looking.

One further number, recorded rather than left for a critic to ask for: on the one-ulp grid the
two implementations' transformed **vectors** differ by **4.7e-02** even though their **matrices**
agree to 6.5e-15. That gap is the ill-conditioning (`‖S‖∞ ~ 9e+15`) amplifying a rounding-level
difference between two equally entitled implementations — neither is "the wrong one". The gate
asks whether the module *hides* ill-conditioning, and it does not: `‖S‖∞` is sitting in plain
sight in the operator it returns. The audit criterion is therefore taken on the matrix, and the
amplified figure is emitted as `vec_rel_vs_ref` in the JSON so the choice is auditable.

## Lesson

**An adversarial audit of a discretization needs a second implementation, not a known answer.**
A known answer conflates "the grid was bad" with "the code was wrong", and on degenerate inputs
the first term dominates by orders of magnitude — this leg would have reported a spurious YES at
`1.3e+02` relative error had it scored the analytic yardstick alone. The cost of the second
implementation was about eighty lines and one bug of its own; the bug was caught by gating the
reference against the module on healthy grids **before** trusting it on hostile ones, which is
the step that makes the whole construction safe rather than merely impressive.
