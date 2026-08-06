# TECHNICAL — Route-WVR v1 (leg 160): a different fitness DEFINITION, and P3 still does not move

Runner `experiments/p2_route_wvr_v1_fitness.py`; evidence
`experiments/p2_route_wvr_v1_fitness_evidence.py`; data
`writeup/data/p2_route_wvr_v1_fitness.json`; figure
`writeup/figures/fig64_route_wvr_v1_fitness.png` (`fig64`); novelty pass
`writeup/novelty/leg_160.md`; journal `experiments/journal/leg_160.md`.
Every number below is in the JSON and is re-derived from it by the evidence script.

**No GA compute ran, on either branch of this leg's gate.** `plan_of_record.py` bans it on an
unvalidated fitness; the runner imports nothing from `ga/` and the evidence script asserts that
by reading the runner's own source. The gate answered **NO**, so the ban's lift condition is not
met and nothing about the ban changes.

## 1. The object, and what a "definition" means here

`solver/weight_search.py` scores a weight `θ = (p, log10 L, q, log10 l, log10(w_l/X_max))` on
`BorderedCLM` — the `a = 0` CLM steady system bordered with `(c_l, c_ω)` as implicit unknowns,
exact profile `Ω_0(X) = −4X/(1+4X^2)` — by

    f_0(θ) = log10( Y_0(θ) / budget(θ) ),   budget = (1−Z_1)^2/(2 Z_2),
    Y_0(θ) = max_i w_i |(A F(z))_i|,        A = DF(z)^{-1} in float64,

in the weighted sup norm on `z = (Ω, c_l, c_ω)`, same weight on domain and codomain.

Legs 46/49/50/59 all score `f_0` and differ only in the **box** the search runs in. This leg
changes `f_0` itself. Both candidates were written into the runner's module docstring, with
their predicted failure modes, **before any number was computed** (leg 111's pre-naming
discipline; the runner's first commit is the record).

## 2. What was frozen, and the mechanism that guarantees it

FROZEN, untouched, and identical to leg 59's list: all six thresholds (`P1_SPREAD_MIN 1.0`,
`P2_FINITE_FRAC 0.90`, `P3_MONO_VIOLATIONS 0` and slope-error `0.05`, `P4_RANK_RHO_MIN 0.90` /
`P4_TOP3_OVERLAP 2`, `P5_BAND_MIN 2.0`, `P6_INTERIOR_FRAC 0.05`), the roster construction
(2 controls + 6 degenerates + 32 random, seed 0), the resolutions (`n = 201` / `401`), the
search settings (`per_gene=9`, `refine=4`), the defect grid `DEFECT_EPS_DEFAULT`, the window
constant `DEFECT_WINDOW_C = 0.1`, `DEFECT_MIN_WINDOW = 3`, the probe direction, and the 2-D wall
model.

`solver/weight_search.py` is **read-only** under this leg (`DIRECTION.md` leg 160 territory) and
is not edited. The gate is **not reimplemented**: `six_property_gate` is executed unmodified,
and a context manager substitutes the class the name `weight_search.FitnessEngine` resolves to
for the duration of the call. Consequence worth stating plainly — **not one frozen threshold is
copied into this leg as a literal**, so a constant cannot drift here without drifting in the
module, and the evidence script re-reads the thresholds out of the module to confirm.

CHANGED: only the score. Four modes, two of them controls.

## 3. The three definitions, as run

| mode | score | kind |
|---|---|---|
| `identity` | `log10(Y_0/budget)` verbatim | control (reproduction) |
| **WVR-1 coercivity-only** | `log10( 2 Z_2 / (1−Z_1)^2 ) = −log10(budget)`; `Y_0` **dropped** | CANDIDATE (definitional) |
| **WVR-2 floor-quotiented** | `log10( [ max_i w_i max(\|(A F)_i\| − τ_i, 0) + max_i w_i τ_i ] / budget )`, `τ = 8·\|A\| @ \|F_float64 − F_longdouble\|` | CANDIDATE (definitional) |
| `hiprec` | `log10(Y_0/budget)` with `Y_0`'s residual in longdouble | control (**realization**, not definitional) |

`τ` is computed by each engine at **its own** state, so WVR-2 needs no reference state and is
usable by a searcher. `hiprec` is labelled a realization control throughout (standing discipline
70) and is **not** offered as an answer to the gate.

## 4. The identity control, run before anything was believed

The substitution must reproduce leg 59 bit-for-bit. It does, on all six banked quantities:

| quantity | leg 59 | here | exact |
|---|---|---|---|
| P2 finite fraction | 0.975 | 0.975 | ✓ |
| P3 worst \|slope−1\| | 0.3421493449940881 | 0.3421493449940881 | ✓ |
| P3 violations | 8 | 8 | ✓ |
| P3 weights resolved | 21 | 21 | ✓ |
| P1 spread (decades) | 14.330842101913802 | 14.330842101913802 | ✓ |
| properties passed | 5 | 5 | ✓ |

## 5. THE GATE, at the frozen configuration `n = 201 / 401`

| fitness | verdict | P2 | P3 worst \|slope−1\| | Δ P3 vs `f_0` |
|---|---|---|---|---|
| `identity` | FAIL 5/6 | 0.9750 | 0.3421493449940881 | — |
| **WVR-1 coercivity-only** | FAIL 4/6 | 0.9750 | 1.0000325577018077 | **+0.6579** |
| **WVR-2 floor-quotiented** | FAIL 5/6 | 0.9750 | 1.0339015518487575 | **+0.6918** |
| `hiprec` (control) | FAIL 5/6 | 0.9750 | 0.3319205339135344 | **−0.0102288110805537** |

**The gate answers NO.** P3 is the only property that fails in three of the four modes, and it
has now survived three different kinds of repair:

    the BOX          leg 50 (1-D wall), leg 59 (2-D wall)   P3 moved by  0.0000000000
    the DEFINITION   this leg, WVR-1 and WVR-2             P3 moved by +0.6579, +0.6918
    the REALIZATION  this leg, hiprec control              P3 moved by −0.0102288110805537

`−0.0102` is the **first movement toward the threshold since leg 49**, and it closes `3.5%` of
the `0.2921` gap to the frozen `0.05` ceiling. It comes from the control, not from a candidate.

## 6. Why WVR-1 fails, and it is a statement about P3

Pre-registered before the run and confirmed: dropping `Y_0` makes the score nearly independent
of the injected defect, so the ladder's fitted slope is ≈ 0 and `|slope−1| ≈ 1`. That is not
under-tuning. **P3, as frozen, hard-codes that the fitness must be a defect-magnitude proxy** —
it admits only scores of the form `log10(c·‖z − z*‖ + …)`. Any definition that scores the
*norm's* quality rather than the *state's* residual is rejected by construction, including the
one leg 49's own gauge ablation argues for (its whole 5604× lives in `Y_0`'s border rows, i.e.
in preconditioning, not in the choice of space).

So the space of definitions P3 can accept is far narrower than "a fitness for a searched
certificate norm", and within it the only free choices are the norm and a prefactor — neither of
which touches the floor. This is the structural reason the definitional route was always thin,
and it is measured here rather than argued.

## 7. Why WVR-2 fails, measured

WVR-2 subtracts the state's own arithmetic floor componentwise and adds it back once as an
anchor. The failure is in the **estimator**, not the idea. The floor a single-state definition
can compute is

    τ = 8 · |A| @ |F_float64(z) − F_longdouble(z)|      (absolute values: NO cancellation)

while the floor actually present in the ladder is

    ρ = A F(z*)                                          (signed: it cancels)

Measured at `n = 201` (`over_subtraction` in the JSON):

    ||tau||_inf                         1.2999035590373247e-09
    ||rho||_inf                         4.790972900601766e-11
    ratio                               27.132350485097742
    median componentwise tau/|rho|      27.138837074030103
    fraction of components over-subtracted   0.9950738916256158

So the estimator over-subtracts by `27×` on `99.5%` of components. `‖τ‖_∞ = 1.30e-09` sits
inside the probe window — the window's top is `C/‖A‖_w ≈ 2.8e-08` — so roughly two of its ~3.4
decades are annihilated before any floor is removed, and the score goes defect-blind
(`P3 = 1.0339015518487575`). At `n = 101`, where there is signal to spare, the same definition
leaves some (`P3 = 0.2744581497130689`) — still `3.8×` worse than doing nothing, and the ratio
there is `44.6×`.

The idea of subtracting is not what fails. The **estimator** does, and it fails for a reason that
is structural rather than tunable: any floor estimate a single-state fitness can build has to
bound a *signed* quantity by an absolute-value expression, and the cancellation it throws away is
exactly the factor that makes it useless as a subtrahend.

## 8. What P3 actually measures — reconstructed, not correlated

**Credit first.** Leg 59 banked this mechanism for this exact object and deliberately left it
out of the frozen gate: its `D_probe_window` block carries per-weight
`eps_min_noise_floor = Y_0 / max_i w_i|d_i|`, reports
`Spearman(window width, |slope−1|) = −0.8779220779220779` over 21 weights, and its `reading`
field already says "this is a defect in the FITNESS's definition, not in the box the wall model
draws". The general principle is older and belongs to Moré–Wild (ECnoise) and the
Berahas–Byrd–Nocedal / Shi–Xie–Xuan–Nocedal derivative-free-optimization interval literature: a
finite-difference probe has a two-sided window, capped above by truncation and floored below by
the function's own noise. `defect_ladder` has the upper cut (leg 50's
`DEFECT_WINDOW_C = 0.1/‖A‖_w`) and **no lower cut** — the grid runs to `eps = 1e-11`. This leg
claims neither.

**What is this leg's.** Writing `A F(z* + eps d) = eps d + ρ + O(eps^2)` with `ρ = A F(z*)`, the
ladder can be rebuilt from `ρ` alone, **with no PDE evaluation at any perturbed state**, and each
weight's fitted slope predicted in the same frozen window. Over the 21 resolved weights:

    max |predicted − measured| slope   0.058
    median                             0.021
    predicted worst |slope−1|          0.3057   vs measured 0.3421  (under by 0.0365, 11%)

The 11% is the first-order model's own missing `O(eps^2)` term and is reported as its error, not
absorbed. A correlation of `−0.878` is consistent with several mechanisms; a reconstruction is
consistent with one.

Supporting magnitudes:

    ||F(z*)||_inf                6.661338147750939e-15      the converged residual
    float64 evaluation noise     2.432759939677287e-15      |F_float64 − F_longdouble|
    residual_floor(z*)           1.9462079517418296e-14     the module's own estimate
    ||rho||_inf   (n = 201)      4.790972900601766e-11      4.8x ABOVE the grid bottom
    ||rho||_inf   (n = 101)      4.640571829290985e-13      21x BELOW it
    frozen grid bottom           1e-11                      does not move with n

**16 of the 21 resolved weights are probed below their own floor** at `n = 201` (worst knee
`7.89e-11`, i.e. 7.9× the grid's bottom rung). And the arithmetic that produces the knee is
checked against the predecessor rather than asserted: this leg's `knee_eps` and leg 59's
`eps_min_noise_floor` are the same quantity, and they agree on all 21 shared weights to a worst
relative difference of **exactly `0.00e+00`** (evidence check 8).

## 9. The resolution ablation — labelled, and NOT a second chance at the gate

Coarsening the grid lowers `‖A‖_w`, lowers `ρ` by `103×`, and leaves the frozen `eps` grid where
it is. If the floor is what P3 measures, every defect-tracking mode must improve and the one
defect-blind mode must not.

| mode | P3 at `n=201` (THE GATE) | P3 at `n=101` (ablation) | factor | `n_pass` 201 → 101 |
|---|---|---|---|---|
| `identity` | 0.3421493449940881 | 0.02007528568401651 | **17.0×** | 5/6 → **6/6** |
| WVR-1 coercivity-only | 1.0000325577018077 | 1.0000562750220603 | **0.99998×** | 4/6 → 4/6 |
| WVR-2 floor-quotiented | 1.0339015518487575 | 0.2744581497130689 | **3.8×** | 5/6 → 5/6 |
| `hiprec` | 0.3319205339135344 | 0.009516196830762214 | **34.9×** | 5/6 → **6/6** |

**WVR-1 is the control that could have come out differently and did not.** It dropped `Y_0`, so
it is defect-blind by construction; a knob that moves every defect-tracking score by `3.8×` to
`34.9×` and moves the defect-blind score by `0.99998×` is acting on the defect's floor and on
nothing else.

### 9a. The finding in this table that is not the gate answer

**The unmodified, unrepaired leg-49 fitness passes the frozen six-property gate 6/6 at
`n = 101/151`.** Nothing was repaired to achieve it. `plan_of_record.py`'s ban lifts on "a re-run
of the six-property gate that PASSES on a repaired fitness", and that wording pins neither the
resolution nor what "repaired" means — so as measured, the lift condition is reachable by
coarsening the grid. That is a false pass in exactly Gate 4's sense.

This leg **reports it and does not use it**. The frozen configuration is `n = 201/401`; the gate
answer is read off that alone and it is NO; no GA compute ran. Whether the ban's wording should
pin the resolution is the user's call, not this leg's and not the DM's.

## 10. C3 — the tension between P1/P5 and P3

P1 and P5 require ≥ 1 and ≥ 2 decades of spread **at the converged state**; P3 requires exact
linearity in an injected defect **down to `eps = 1e-11`**. A fitness positively homogeneous of
degree 1 in the defect vanishes at the converged state, so it has no spread there and fails
P1/P5. Hence every fitness satisfying P1/P5 carries a nonzero floor at `z*`, and every floor
saturates the ladder's small-`eps` end and costs P3. The two are jointly satisfiable only when
the floor sits below the window's bottom decade — a statement about arithmetic and grid, not
about the fitness's definition. WVR-2 is precisely the attempt to have both (subtract for P3,
anchor for P1/P5); the anchor is what caps it. Nothing in the record states this; it is
elementary once §8 is stated, and it is presented as an observation with a measured consequence,
not as a named theorem.

## 11. A correction this leg owes on its own prediction

The runner's first docstring predicted that leg 59's ladder slopes would repeat **identically to
16 digits** across weights, cited `0.8378100167662509` as appearing twice, and invoked lesson 90.
**The data refutes it.** Leg 59's 21 finite slopes have **zero** exact duplicates; the two
entries are `0.83781001` and `0.83781002`, differing in the 8th digit. Lesson 90's
identical-numbers tell does not apply here.

The weaker, measured statement does hold and is what is claimed: the 21 slopes fall into **10
clusters at relative tolerance `1e-3`** (12 at `1e-5`, 17 at `1e-7`). Weights whose weighted max
selects the same component share a slope to about three significant figures; the residual spread
is the `O(eps^2)` term plus the budget's own `eps`-dependence. The correction is in the
docstring, in the JSON's `slope_degeneracy` note, and is asserted as evidence check (10) so it
cannot quietly revert.

## 12. The ceiling

No link of the L1→L4 chain moved. This is a property check on a **float** fitness over the
`a = 0` CLM linearisation, whose profile has been closed form since CLM 1985 — a rehearsal of a
certificate, not a certificate. It says nothing about `HL_S2_nonsymmetric`. It does **not**
reopen stage B, which leg 126 closed on the search space independently of the fitness. The GA
ban stands, its lift condition is unmet, and lifting it was never this leg's to do.
