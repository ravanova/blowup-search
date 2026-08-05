# Leg 59 — Route-WV: the weight fitness's wall is 2-D, not 1-D

Branch `leg/wv-v1`. Claim-bearing. Frozen gate re-run, NO GA compute on either branch.

## Order of work

1. `plan_of_record.py` read first; every ban carried, including the ban on any GA
   compute (it lifts only on a gate that PASSES, and lifting it is the user's call).
2. Novelty pass BEFORE construction — `writeup/novelty/leg_59.md`, committed on its
   own. Verdict: no source states the admissible weight-parameter set of a
   radii-polynomial argument as a measured region, in any dimension. Chen–Hou
   arXiv:2210.07191 sec 5.3.3 uses the same two-factor weight family and picks it by
   hand; nobody publishes its boundary.
3. `capabilities.py` grepped before building: `solver/weight_search.py` already holds
   `BorderedCLM`, the fitness, `FitnessEngine`, `lower_wall`, `grid_search` and the
   frozen gate. Nothing was rebuilt; the wall model was added alongside them.

## What was actually changed

`in_box`, `FitnessEngine`, `roster` and `six_property_gate` gain an OPT-IN `wall2d`
/ `wall_model` parameter. Default (`"1d"`, `None`) reproduces leg 50 bit for bit —
checked by the fact that the gate's P1/P4/P5/P6 numbers are unchanged. The new
objects are `weight_log_range`, `log_range_analytic`, `weighted_sup_analytic`,
`TwoFactorWall`, `two_factor_wall`, `wall_model_disagreement`.

The wall's ONE number is inherited: `r_crit` is the log-range at the SAME bisected
crossing `lower_wall()` already measured (p_- = -3.7370 -> r_crit = 11.6060 decades).
Nothing is fitted to this leg's own data, so the 1-D vs 2-D comparison is a comparison
of geometry and not of calibration.

## Mechanism, stated before the numbers

In this float rehearsal `M = I - A DF` is roundoff, so
`Z_1 = max_i w_i sum_j |M_ij|/w_j ~ eps * kappa * (max_i w_i / min_j w_j)` — the
weight's DYNAMIC RANGE. Two weights with the same far-field power `p+q` do not share
a range once the two algebraic factors carry different scales (the weight then dips or
peaks INSIDE the domain), and the border weight `w_l` enters the range as well. The
admissible set is therefore a level set of the range, i.e. a curve in the `(p,q)`
plane — and the 1-D model is that curve's intersection with one line.

## Results (magnitudes; full table in writeup/data/p2_weight_repairs_v2.json)

- **Known-answer window met.** The growth law re-derived in the 2-D geometry
  reproduces the banked 1-D answer exactly: measured x7.3887, 2-D law x7.3887, rel
  6.7e-16, against the pre-committed x7.39 over a 54.6x reach. Over the five-case
  battery its worst relative error is 1.9e-10. The 1-D law `X_max^(p+q-1)` is off by
  up to **7.39x** on weights with opposite-sign factor powers, where the sup sits at an
  interior peak and the edge branch is simply the wrong branch — at IDENTICAL p+q.
- **The failure set is separated by range, not by p+q.** On 400 in-box weights, 123
  with `Z_1 >= 1`: the 1-D wall admits 311 of which **51 fail (16.4%)**; the 2-D wall
  admits 278 of which **2 fail (0.72%)**. Misclassified 68 -> 3, a **22.7x** reduction.
- **The frozen gate: FAIL 5/6.** P2 finite fraction 0.875 -> **0.975** against the 0.90
  floor — passes, and exactly one roster weight (`rand_10`) is left infinite. P3 worst
  |slope-1| **0.342 -> 0.342**, unmoved to sixteen digits, with 8 monotonicity
  violations, against the 0.05 ceiling. P1/P4/P5/P6 unchanged and passing.
- **What carries P3 (diagnosis, NOT folded into the gate).** The fitted slope is a
  function of the probe WINDOW's width in decades, not of the weight: `defect_ladder`
  bounds eps above (leg 50's repair, `C/||A||_w`) and never below, while
  `Y_0(eps)` stops tracking eps under `eps_min(w) = Y_0(z*,w) / max_i w_i |d_i|`.
  Weights whose window is ~5 decades wide fit slope 0.999; ~3 decades give 0.83-0.84;
  ~2 decades give 0.658 — the same 0.658 for five different weights, and the same
  0.342 worst error across two DISJOINT rosters (leg 50's and this one). Spearman
  (window width, |slope-1|) = **-0.878** over the 21 resolved weights; the worst error
  sits at a 2.10-decade window, and the pass/fail populations overlap only between
  3.53 and 3.88 decades. That is the probe's own noise floor being measured, not the
  fitness's defect tracking.

## Gate answer

"With a 2-D wall model, does the FROZEN six-property viability gate pass 6/6 — in
particular P2 >= 0.90 and P3 max |slope-1| <= 0.05?" — **NO. 5/6.** P2 passes at 0.975;
P3 fails at 0.342 against 0.05, unmoved by the wall model. So Stage B's fitness is dead
as parameterized, and any future B proposal must change the fitness's DEFINITION (P3's
probe has no floor) and not its wall model. This branch lands normally on main; no
escalation, and NO GA compute was run.

## Ceiling

No link of the L1->L4 chain moved. This is a gate result on a fitness measured in
FLOAT on the a=0 CLM linearisation (closed form since CLM 1985) — not a certificate,
and not a statement about Hou–Luo. Carried per the leg's brief: leg 54 measured the
shape of A dead on top of leg 53's split and leg 52's space, so even a PASS here would
have unblocked a stage whose three degrees of freedom are all separately measured
worthless for this operator. The 2-D wall is worth having because it is a MEASURED
geometry of a search space; it is not a route.
