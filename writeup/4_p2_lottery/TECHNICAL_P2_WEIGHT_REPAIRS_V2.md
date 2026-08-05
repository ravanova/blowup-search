# TECHNICAL — Route-WV v2 (leg 59): the conditioning wall in both weight factors

Runner `experiments/p2_weight_repairs_v2.py`; evidence
`experiments/p2_weight_repairs_v2_evidence.py`; data
`writeup/data/p2_weight_repairs_v2.json`; figure
`writeup/figures/fig58_weight_repairs_v2.png` (`fig58`); gates (10)-(12) in
`test_weight_search.py`. Every number below is in the JSON and is re-derived from it
by the evidence script (18 checks, all passing).

## 1. The object

`solver/weight_search.py` scores a weight by `fitness(θ) = log10(Y_0/budget)` with
`budget = (1-Z_1)^2/(2 Z_2)`, on `BorderedCLM` — the a=0 CLM steady system bordered
with `(c_l, c_ω)` as implicit unknowns, whose exact profile `Ω_0(X) = -4X/(1+4X^2)` is
closed form. The genome is

    θ = (p, log10 L, q, log10 l, log10(w_l/X_max)),
    ν(X) = (1+(X/L)^2)^(p/2) (1+(X/l)^2)^(q/2),  w_ω = 1 (gauge-fixed),

and the norm is the weighted sup norm on `z = (Ω, c_l, c_ω)`, same weight on domain and
codomain.

## 2. What was frozen and what changed

FROZEN, untouched: all six thresholds (`P1_SPREAD_MIN` 1.0, `P2_FINITE_FRAC` 0.90,
`P3_MONO_VIOLATIONS` 0 and slope-error 0.05, `P4_RANK_RHO_MIN` 0.90 /
`P4_TOP3_OVERLAP` 2, `P5_BAND_MIN` 2.0, `P6_INTERIOR_FRAC` 0.05), the roster
construction (2 controls + 6 degenerates + 32 random, seed 0), the resolutions
(n = 201 coarse / 401 fine), the search settings (`per_gene=9`, `refine=4`), the
defect grid `DEFECT_EPS_DEFAULT`, `DEFECT_WINDOW_C = 0.1`, `DEFECT_MIN_WINDOW = 3`.

CHANGED: only the MODEL of the conditioning wall the box carries.
`six_property_gate(..., wall_model=...)` defaults to `"1d"` and reproduces leg 50
exactly; `"2d"` swaps the half-plane in `p+q` for the level set of the weight's
log-range. `in_box`, `FitnessEngine` and `roster` take an opt-in `wall2d` argument
whose default `None` is the previous behaviour (gate (12) asserts the opt-in).

## 3. The mechanism, and why the boundary cannot be 1-D

`A = DF^-1` in float, so `M = I - A DF` is roundoff and

    Z_1 = max_i w_i Σ_j |M_ij|/w_j  ≲  ‖M‖_max · (max_i w_i / min_j w_j),

i.e. the conditioning wall is a statement about the weight vector's **dynamic range**

    R(θ) = log10( max_i w_i / min_i w_i ),   w = (ν(X_1..X_n), w_l, w_ω).

`R` is gauge invariant, like the fitness. For the two-factor family, `log10 ν` is
stationary in `X^2` where `p/(X^2+L^2) + q/(X^2+l^2) = 0`, i.e. at

    X_ext^2 = -(p l^2 + q L^2)/(p+q),

so `R` is the spread of four candidates: `log10 ν(0) = 0`, `log10 ν(X_max)`,
`log10 ν(X_ext)` when that root is real and inside the domain, and the border entries
`log10 w_l`, `log10 w_ω = 0`. This is `log_range_analytic`; it agrees with the range
the grid actually carries (`weight_log_range`) to **0.057 decades** over 300 in-box
weights, the residual being grid discreteness at the interior stationary point (gate
(10) asserts < 0.15).

Two weights with the same `p+q` therefore have different `R` whenever `L ≠ l` — the
interior extremum exists precisely when `p` and `q` have opposite signs — so the
`Z_1 = 1` boundary is a level set of `R`, a curve in the `(p,q)` plane, and `p+q` is
one of its coordinates and not the boundary.

## 4. The wall's calibration is inherited

`two_factor_wall(engine)` runs `lower_wall(engine)` — the SAME bisection, unchanged —
and reads the log-range at its crossing:

    p_- = -3.7370  ->  r_crit = 11.6060 decades   (n = 201)
    fine grid:              r_crit =  9.2954 decades   (n = 401)

No constant is fitted to the 2-D data (`WALL_RANGE_DELTA = 0`; the standoff already
lives in the 1-D wall's own `WALL_LOWER_DELTA = 0.05`). On the measuring slice the two
models agree by construction, which gate (12) checks explicitly. The fine grid's
smaller `r_crit` is the same shrinking-band effect gate (7) already banks: refinement
raises `p_-` and tightens the admissible range.

## 5. Measurement A — the growth law re-derived in the 2-D geometry (known answer)

With `Ω_0 ~ -1/X`, `g(X) = ν(X)|Ω_0(X)|` has

    d log g / d log X = p r_L/(1+r_L) + q r_l/(1+r_l) + (1-4X^2)/(1+4X^2),
    r_L = (X/L)^2, r_l = (X/l)^2,

and `sup g` is attained at a root of that explicit equation or at `X = X_max`
(`weighted_sup_analytic`, a bisected root find on a closed form, not a max of sampled
data). The 1-D reading — "the norm grows like `X_max^(p+q-1)`" — is the edge branch
alone.

Growth of `sup ν|Ω_0|` over a reach of **54.598x** (`X_max` 13.65 -> 745.24), five
cases all at `p+q = 1.5`:

| case | (p, log10 L, q, log10 l) | measured | 2-D law | rel err | 1-D law | 1-D off by |
|---|---|---|---|---|---|---|
| slice_1d | (1.5, 0, 0, 0) | x7.3887 | x7.3887 | 6.7e-16 | x7.3891 | 1.00x |
| two_factor_same_sign | (0.75, 0.301, 0.75, -0.301) | x7.3881 | x7.3881 | 1.1e-15 | x7.3891 | 1.00x |
| two_factor_split | (2.0, 0, -0.5, 1.0) | x7.4066 | x7.4066 | 1.8e-15 | x7.3891 | 1.00x |
| interior_dominated_a | (-1.0, -1.0, 2.5, 0.477) | x1.5307 | x1.5307 | 4.0e-11 | x7.3891 | **4.83x** |
| interior_dominated_b | (3.0, 0.699, -1.5, -0.699) | x1.0000 | x1.0000 | 1.9e-10 | x7.3891 | **7.39x** |

The pre-committed window is the banked 1-D answer (x7.39 predicted, x7.39 measured,
`capabilities.py`); row 1 meets it to 6.7e-16. Worst 2-D error over the battery
1.9e-10. The last two rows are the point: at identical far-field power the sup sits at
an interior peak, the edge branch is the wrong branch, and the 1-D law is off by up to
7.39x. Gate (11) asserts both halves.

## 6. Measurement B — what each model explains of the `Z_1 >= 1` failure set

400 weights drawn inside the box (analytic upper wall only), seed 11, n = 201.
**123** have `Z_1 >= 1`.

| model | admitted | admitted-but-failing | excluded-but-fine | misclassified | failure rate among admitted |
|---|---|---|---|---|---|
| 1-D, `p+q >= p_- + 0.05` | 311 | 51 | 17 | **68** | **16.40%** |
| 2-D, `R <= r_crit` | 278 | 2 | 1 | **3** | **0.719%** |

Ratio of misclassification **22.67x**, with no new free constant. Gate (12) asserts
the 2-D model both misclassifies strictly less and at least halves the failure rate
among admitted weights.

## 7. Measurement C — the frozen gate, re-run

| property | leg 49 | leg 50 (1-D wall) | leg 59 (2-D wall) | threshold | verdict now |
|---|---|---|---|---|---|
| P1 spread (decades) | — | 12.694 | 14.331 | ≥ 1.0 | PASS |
| **P2 finite fraction** | 0.775 | 0.875 | **0.975** | ≥ 0.90 | **PASS** |
| **P3 worst \|slope-1\|** | 0.366 | 0.342 | **0.342** | ≤ 0.05 | **FAIL** |
| P3 monotonicity violations | 0 | 8 | 8 | 0 | FAIL |
| P4 Spearman / top-3 overlap | — | 0.9963 / 2 | 0.9966 / 2 | ≥ 0.90 / ≥ 2 | PASS |
| P5 band (decades) | — | 12.694 | 14.331 | ≥ 2.0 | PASS |
| P6 interior margin / wall cost | — | 0.161 / 1.6e-4 | 0.161 / 1.6e-4 | ≥ 0.05 / ≤ 0.05 | PASS |

**Verdict FAIL, 5/6** (leg 49: 4/6, leg 50: 4/6). P2's residual is a single roster
weight, `rand_10`, still without a finite score — one of the 0.72% the 2-D wall
admits and should not have.

P3's `max_slope_error` is `0.3421493449940881` here and
`0.3421493449940881` at leg 50: **identical to sixteen digits across two rosters that
share only the eight non-random weights**. That is the tell that P3 is not measuring
any property of the weights the wall model selects.

## 8. Measurement D — what carries P3 (diagnosis, NOT folded into the gate)

`defect_ladder` bounds `ε` above (`ε <= C/‖A‖_w`, leg 50's P3 repair) and never below.
But `Y_0(ε) = max_i w_i |A F(z*+ε d)|_i` stops tracking `ε` once the perturbation
falls under the roundoff already in `A F(z*)`, at

    ε_min(w) = Y_0(z*, w) / max_i w_i |d_i|,

so each weight's probe has a **window** `[ε_min, ε_max]` and the decade grid puts
points below its floor. Over the 21 resolved weights:

- Spearman(window width in decades, `|slope-1|`) = **-0.878**.
- Worst `|slope-1|` = **0.3421** at a **2.10**-decade window.
- Windows ≈ 5.2 decades fit slope **0.999**; ≈ 3.1-3.5 decades fit **0.825-0.841**;
  ≈ 1.8-2.2 decades fit **0.658** — the same 0.658 to five digits for five distinct
  weights.
- The pass/fail populations overlap only between **3.53** decades (narrowest window
  meeting P3) and **3.88** decades (widest failing it).

An independent ladder on `rand_12` shows the same thing directly: local slope stays
within `0.976-1.025` from `ε = 1e-6` down to `1e-9`, then collapses below `3e-10`,
while that weight's admitted window is `ε <= 2.86e-9` — two of its three grid points
sit under the floor.

This is stated as a diagnosis and is deliberately NOT applied to the gate. Applying it
would be moving a goalpost mid-leg; the gate is frozen and its answer stands.

## 9. Gate answer

> "With a 2-D wall model, does the FROZEN six-property viability gate pass 6/6 — in
> particular P2 >= 0.90 and P3 max |slope-1| <= 0.05?"

**NO — 5/6.** P2 passes at 0.975 (floor 0.90). P3 fails at 0.342 (ceiling 0.05) with 8
monotonicity violations, unmoved by the wall model. Per the pre-committed no-branch:
Stage B's fitness is dead as parameterized, and any future B proposal must change the
fitness's DEFINITION — sec 8 says exactly where, the probe's missing noise floor — and
not its wall model. **No GA compute was run**, which the ban requires on either branch.

## 10. Ceiling

No link of the L1->L4 chain moved. The substrate is the a=0 CLM linearisation, closed
form since CLM 1985, and every constant here is float: `Z_1` measures conditioning, not
a truncation tail, so this is a rehearsal of a certificate and not a certificate.
Nothing here is a statement about HL_S2_nonsymmetric.

Carried from the leg's brief, and load-bearing for how the result is read: leg 54
measured the shape of `A` dead on top of leg 53's split and leg 52's space, so even a
6/6 here would have unblocked a stage whose three degrees of freedom are all
separately measured worthless for this operator. Passing the gate would have been
worth knowing; it would not have been a route.

## 11. Novelty

`writeup/novelty/leg_59.md`, run and committed before construction. Chen–Hou
arXiv:2210.07191 sec 5.3.3 uses this same two-factor weight family and picks it by
hand, publishing no admissible set; arXiv:2203.02404 carries a single decay parameter;
arXiv:1702.07421 states the "which weight is least conservative" problem for
contraction metrics of DAEs, not for a Newton–Kantorovich norm. No source states the
admissible weight-parameter set of a radii-polynomial argument as a measured region in
any dimension. The claim here is correspondingly narrow: it is a MEASUREMENT of one
search space's geometry on one known-answer object in float, not a theorem.
