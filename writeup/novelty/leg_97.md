# Leg 97 — Route-WSA novelty pass (run and committed BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-G. **Branch:** `leg/wsa-v1`.
**Verdict: `PROCEED_AS_ROBUSTNESS_AUDIT`.**

This leg builds no new mathematics, measures no new physics, and claims no novel mechanism.
It audits one *software* property of `solver/weight_search.py`'s `FitnessEngine`: whether the
batched evaluation path — Jacobian formed once, inverted once, reused across every weight in
the batch — can return a **finite, plausible-looking** fitness number when the shared inverse
is garbage (near-singular state) or when the weight genome is poisoned (NaN/inf genes).
`solver/weight_search.py` is READ-ONLY under this leg, under either branch of the gate.

**Explicit non-claim, stated first because it is the thing most easily misread.** Stage B's
frozen gate verdict (leg 49, 4/6; leg 59 measured 5/6 in the 2-D wall model) is NOT reopened,
re-scored, contested or referenced as live. The plan-of-record ban *"any GA compute on an
unvalidated fitness"* is respected literally: **no GA is run, no search is run, no roster is
re-scored, and no six-property property is re-measured.** The battery calls
`FitnessEngine.constants_many` / `fitness_many` directly on hand-built adversarial inputs and
compares them against a higher-precision recomputation. The question is arithmetic hygiene of
one class, not the scientific viability of the fitness it computes.

## 1. What the object is, and where the shortcut lives

`FitnessEngine.__init__` (weight_search.py:623-638) computes, once:
`J = problem.jacobian(z)`, `A = np.linalg.inv(J)`, `absM = |I - A J|`, `aAF = |A F(z)|`,
`absA`, `absH`, `absXD`. `constants_many` (640-657) then produces `(Y0, Z1, Z2)` for `k`
weights with four `(k,N)x(N,N)` products. Nothing in the batch depends on the weight except
`W`/`NU`, so the inverse is genuinely shared. The two hazard axes the gate names are exactly
the two inputs that shortcut does not re-validate: the **state** `z` (which fixes `J`, hence
`A`'s conditioning, for every member at once) and the **genome** `theta` (which enters only
through `W`, but through it into every max/reciprocal in the batch).

## 2. Repo-internal prior-art sweep (magnitudes, not booleans)

| probe | count |
|---|---|
| `test_*.py` files in the repo | 64 |
| of those importing `solver.weight_search` at all | **2** (`test_weight_search.py`, `test_interval_certificate.py`) |
| tests in `test_weight_search.py` | 12, over 374 lines |
| of those constructing a `FitnessEngine` | **3** (lines 182, 228, 328; plus one inside `lower_wall` at 200) |
| assertions anywhere in the repo on `constants_many` | **0** (4 mentions in `solver/`, 2 in `experiments/p2_route_c_pilot_v0.py`, 0 in any test) |
| assertions anywhere in the repo on `fitness_many` | **0** (6 mentions, all inside `solver/weight_search.py`) |
| lines in `test_weight_search.py` mentioning `isnan/isinf/np.nan/np.inf` | **1**, and it is about an unresolved *slope* fit (line 255), not about the engine |
| `np.linalg.cond` calls anywhere in the repo | 2, neither in `weight_search.py` nor in any weight-search test |
| `np.linalg.inv` call sites in `solver/` | 17, of which 2 in `weight_search.py` (lines 394, 633) |
| prior legs whose gate is `FitnessEngine`'s arithmetic robustness | **0** |
| prior probes feeding a NaN or inf gene into `weight_vector` / `in_box` | **0** |
| prior probes evaluating a `FitnessEngine` at a state whose Jacobian is deliberately ill-conditioned | **0** |
| prior cross-checks of the BATCH path against the per-theta path (`certificate_constants`) | **0** |

What `test_weight_search.py` *does* verify is real and is not duplicated here: Newton's
residual ladder against a measured float64 floor, the exactly-quadratic remainder, fitness
gauge-invariance (4.4e-16), the analytic wall, the 1-D/2-D wall generalisation. Every one of
those is a **well-posed** input. The gap is therefore precise: the class has never been
evaluated on an input that is *wrong* rather than merely hard.

## 3. Sibling legs in this adversarial family (same pattern, different module)

`test_bordered_hl_adversarial.py`, `test_gclm_family_adversarial.py`,
`test_target_norm_adversarial.py`, `experiments/p2_route_bhn_v1_adversarial.py`,
`experiments/p2_route_gca_v1_adversarial.py`. Two of the family's findings set the prior:
leg 79 found `port_certification.py`'s status function accepted fabricated `Y_0`/`Z_1`
**11/25** times; leg 84 found `target_norm.py` returned a finite number on **8/8** domain
hazards with no exception and no warning. So the base rate for "a repo module silently
absorbs bad input" is not low, and this leg's yes-branch is a live possibility, not a
formality. Nothing in this leg re-measures either of those; they are cited as prior art for
the *method*.

## 4. External prior art

The hazard class is textbook and no originality is claimed for it: reuse of a factorization
across a batch, loss of the residual `I - A J` as a conditioning signal, silent
overflow/underflow inside a max-of-products, and NaN passing an interval/box test because
every comparison against NaN is false (IEEE-754 §5.11). LAPACK's own guidance (`gecon`, the
reason `numpy.linalg.inv` does not warn) is the reference point. What is novel here is only
the **measurement on this repository's class**, with magnitudes.

## 5. What this leg may and may not claim

* MAY claim: the measured conditioning at which the shared inverse degrades; whether `Z_1`
  tracks that degradation (the module's own comment at lines 486-495 asserts
  `Z_1 ~ eps*kappa*range` — this leg checks that assertion numerically rather than
  quoting it); the exact behaviour of every poisoned genome, per gene, with `box=True` and
  `box=False`; whether a poisoned batch member perturbs a clean member's bits; the
  batch-vs-per-theta agreement of `constants_many` against `certificate_constants`; and, if
  a silent finite value exists, the exact input that produces it.
* MAY NOT claim: anything about the fitness's scientific viability; anything about stage B's
  or leg 49's or leg 59's gate score (frozen, untouched, and out of scope); that any weight
  is good or bad; that a patch is warranted under this leg's own authority (the gate's
  yes-branch escalates, it does not repair); or that a garbage `A` makes a
  Newton-Kantorovich certificate *unsound* — in NK, `A` is an arbitrary operator and a bad
  one is supposed to show up as a large `Z_1`, which is precisely the property under test.

## 6. Bans checked against this leg

* *"any GA compute on an unvalidated fitness"* — respected. No GA, no `grid_search`, no
  `roster` scoring, no `six_property_gate` call. Direct calls on hand-built inputs only.
* *"building a solver without grepping capabilities.py for the object first"* — done;
  `capabilities.py:370-386` is the `weight_search` entry, which names the shortcut under
  audit verbatim ("FitnessEngine (batched, Jacobian inverted once)") and its test as
  `test_weight_search.py`. No new solver is built; the battery builds no object that
  `capabilities.py` already carries.
* *re-opening stage V, gCLM measurement, Route-D sharpening, DSS, 2-D beta, the scaling
  gauge, domain extension, `s`-tuning, weight-family tuning* — none touched; this leg
  changes no bound and reports no physics.

---

# FINDINGS (appended after the run; the sections above are as committed BEFORE construction)

**Gate answer: NO — confirmed robust.** Full narrative in `experiments/journal/leg_97.md`,
every case in `writeup/data/p2_route_wsa_v1_adversarial.json`.

| measurement | magnitude |
|---|---|
| adversarial cases run | 100+ across 10 gates |
| silent finite fitness values | **0** |
| finite answers whose higher-precision `Z_1` is ≥ 1 | **0** of 42 |
| worst flattering of a weight by the shortcut | **+2.1e-11** decades (threshold 0.5) |
| batch path vs documented per-theta path, max relative deviation | **5.6e-16** |
| float64 `Z_1` vs EXACT rational defect, at `cond = 1.8e14` | **1.6e-12** relative |
| a poisoned batch member's effect on a clean member | **exactly 0.0**, both orderings |
| batch-shape (`k=1` vs `k=6`) summation-order effect, no poison involved | 1.0 ulp |
| conditioning span over which `Z_1` is monotone | `cond(J)` 2.7e5 → 2.4e19 |
| `cond(J)` at which `Z_1` crosses 1 | **2.4e18** |
| poisoned genomes / states returning a number | **0 of 17** / **0 of 8** |
| extreme-range weights underflowing `Z_1` to zero | **0 of 5** (all overflow, all refused) |

**The thesis's own channel turned out not to exist**, and that is the sharpest result:
`jacobian(z)` and `inv(J)` take no `theta` argument, so a batch member *cannot* drive the
shared Jacobian anywhere. The conditioning hazard is real but enters through the **state**,
and there the module's defect term `‖I − A·DF‖` makes it visible — monotonically, over 13
decades, and faithfully to exact arithmetic. In Newton–Kantorovich `A` is an arbitrary
operator, so a garbage inverse is a large `Z_1`, not an unsound certificate.

**Two gaps, pinned not patched** (no patch authority under this leg): `in_box` admits a NaN
genome 7/7 (harmless — `fitness` still returns `+inf`), and `LOG_NU_CLIP` is a silent
weight substitution that no in-box genome can reach (`max|log ν| = 94.3` vs 500 over 122473
admitted genomes, 5.3x headroom). Neither warrants escalation; both are executable gates
(12, 13) so they cannot decay at the rate of memory.
