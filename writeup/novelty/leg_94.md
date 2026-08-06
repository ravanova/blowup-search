# Leg 94 — Route-TNB novelty pass (run and committed BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-I. **Branch:** `leg/tnb-v1`.
**Verdict: `PROCEED_AS_REGRESSION_CHECK`.**

This leg builds no new mathematics, measures no new physics, and claims no novel
mechanism. It audits one *software* property of the domain guard that a bench repair added
to `solver/target_norm.py` after leg 84 (Route-TNA): whether that guard, which was verified
against the FALSE-NEGATIVE direction (silently accepting out-of-window input), ever fires in
the opposite direction — flagging a legitimately IN-WINDOW input as a violation. The physics
of the window is leg 55's (Route-NB) and is banked; nothing here re-measures it, and nothing
here extends any domain. `solver/target_norm.py` is READ-ONLY under this leg, under either
branch of the gate.

## 1. What is already known, and by whom

* **Leg 55 (Route-NB), landed.** Measured the target's coefficient decay
  `p = k^-1.3937 (X_max = 4.1e+04) / k^-1.3963 (3.0e+05)`, margins `+0.394` at `s = 0` and
  `+0.094` at `s = 0.3`, and recorded the limitation this whole route starts from: *"at the
  shipped X_max = 745 the far-field closure moves the exponent by 0.190 and the measurement
  is not trustworthy there; the headline is taken where no sample point leaves the grid."*
  That sentence is the trust criterion the guard implements. Prior art for the physics.
* **Leg 84 (Route-TNA), landed.** Answered its gate **YES (SILENT)**: 8 of 8 adversarial
  domain hazards returned a finite number with no exception and no warning, `0 of 6`
  result-bearing surfaces carried any domain field, and the exponent spread across the
  `power/clamp/zero` closures at the shipped domain was `0.4166` (worst error `0.2512`
  against an exact `1.4`), invisible at the API. Escalated; did not patch.
* **The bench repair (`Leg 0: ORCH`), landed.** Added `TargetNormDomainWarning`,
  `domain_fields()`, `_warn_if_outside()`, and an `n_outside_grid=` argument threaded into
  `fit_exponent`, `weighted_partial_sums`, `analytic_tail`, `norm_verdict`. Threshold is
  `n_outside_grid > 0` against the **caller's own** `max|X|` — dynamic, not the literal 745.
* **`test_target_norm_adversarial.py`, landed.** Leg 84's ten silence-pinning gates,
  INVERTED after the repair, plus two remaining gap-pins.

## 2. Repo-internal prior-art sweep (magnitudes, not booleans)

| probe | count |
|---|---|
| `test_*.py` files in the repo | 63 |
| of those touching `target_norm` at all | **2** (`test_target_norm.py`, `test_target_norm_adversarial.py`) |
| of those touching `domain_valid` | **1** (`test_target_norm_adversarial.py`; leg 55's own test predates the guard and mentions it 0 times) |
| files in the repo mentioning `domain_valid` | 4 (`solver/target_norm.py` 12x, `test_target_norm_adversarial.py` 28x, `experiments/bench_target_norm_domain_guard_check.py` 6x, `capabilities.py` 1x) |
| cases in the bench repair's A/B battery (`A_zero_regression`) | 4 — of which **IN-WINDOW: 1** (`rho_max = 12`, `power`, `alpha = 0.4`, `M = 16384`, `n = 801`) |
| rungs in the adversarial ladder (gate 3) | 7 — of which **clean (`n_outside = 0`): 1**, the same `rho_max = 12` configuration |
| distinct in-window CONFIGURATIONS exercised anywhere in the repo | **1** (one grid, one `M`, one closure, one profile), asserted from 3 places |
| existing assertions of the form `domain_valid is True` | **3** (gates 3 and 9 of the adversarial file; all on that one configuration) |
| prior legs whose gate is the guard's FALSE-POSITIVE direction | **0** |
| in-window probes at the boundary `max\|X_of_theta\| == X_max` (the `<=` in `compactify`) | **0** |
| in-window probes on `clm_anchor` / `inverse_X` / `sawtooth` / any `alpha != 0.4` | **0** |

The gap is therefore precise and worth one light leg: the repair's correctness in the
false-positive direction rests on a **single** in-window configuration, repeated three
times, at the one grid (`rho_max = 12`) that leg 55 already declared the trustworthy
headline. Nothing exercises the guard at the boundary of its own `<=` comparison, at other
resolutions `M`, at other profiles, or anywhere across the validated range up to
`X_max = 745`, which is exactly the span the gate names.

## 3. External prior art

The hazard class — *an over-aggressive input validator that rejects legitimate input* — is
a named, textbook failure mode (false-positive validation / over-restrictive precondition;
the mirror of the silent-extrapolation hazard leg 84 cited, and the reason `scipy` made
`bounds_error` opt-in rather than mandatory). It is **not novel** and this leg does not
present it as such. The deliverable is a *measured* statement about one module in this
repository, with magnitudes.

## 4. What this leg may and may not claim

* MAY claim: how many legitimate in-window calls, over how wide a span of `(X_max, M,
  profile, closure)`, the guard passes without flagging; the exact behaviour at the
  `<=` boundary; whether any in-window number moves when the guard's argument is threaded;
  and, if a false positive exists, the exact input that produces it.
* MAY NOT claim: anything about the exponent's physics (leg 55 owns it), that the window
  should be widened (a live ban forbids closing gaps by extending the domain, and this leg
  extends nothing), that the guard's `None`/unknown case is a defect (it is documented,
  deliberate, and was left open on purpose as adversarial gate 13's remaining gap-pin), or
  that any patch is warranted under this leg's own authority.

## 5. Bans checked against this leg

`plan_of_record.py` was run first, in full. Relevant bans: *"building a solver without
grepping `capabilities.py` for the object first"* — done, the `solver/target_norm.py` entry
was read in full, including the leg-84 domain-guard sentences appended to its `validated`
line, and is quoted in the runner; *"closing the truncation gap by extending the domain"* —
this leg varies `X_max` and `M` only as guard probes and closes nothing; *"another gCLM
measurement leg"*, *"re-measuring beta on the 2D object"*, *"another Route-D
bound-sharpening leg"*, *"re-testing the scaling gauge"* — none is this object. No ban
fires.

---

# Findings (written after construction; the pass above was committed first)

**Gate answer: NO.** The runner's own verdict field reads `NO_FALSE_POSITIVE`; the JSON
headline reads `gate_answer: "NO"`. Across **163 legitimate in-window probes** and
**1088 domain-field reads** at `spectrum` plus all four downstream surfaces, the guard
raised **0 warnings**, reported `domain_valid = True` **1088 of 1088 times**, raised
**0 exceptions**, and changed **0 numbers**. The repair did not over-correct.

## The battery, in magnitudes

* **B1 — the in-window ladder.** 136 calls: every `(X_max, M)` pair with
  `X_reach(M) <= X_max`, `X_max` spanning **13.6 .. 745.2** (the whole validated range the
  gate names) and `M = 16 .. 1024`, crossed with all four far-field settings
  (`power/clamp/zero/none`). Headroom ratio `X_max / X_reach(M)` spans **1.143x .. 73.4x**.
  22 further pairs were excluded as genuinely out-of-window and handed to B6. Result:
  **1088 of 1088** surface reads `True`, **0** warnings, **0** false positives.
* **B2 — the `<=` boundary, and a methodological correction worth banking.** `compactify`
  tests `|X_j| <= max|X|`. A grid built so `max|X|` equals the largest sample **bit for
  bit** is accepted: `n_outside_grid = 0`, 0 warnings, 7/7 surfaces `True`. So the `<=` is
  the right comparison and a `<` would have been caught here. The threshold is sharp:
  clean at relative headroom **exactly 0.0**, firing at **-9.77e-15** with **1** sample
  outside. **The correction:** the first pass of this runner scored 2 false positives and
  they were an artifact of the *runner*, not the guard. `tan` is catastrophically
  ill-conditioned at `theta/2 -> pi/2`, so the closed form `cot(pi/(2M)) =
  325.94830079770134` and the grid's actual largest sample `325.94830079770776` differ at
  `M = 512` by **113 ulp (relative 1.97e-14)**. Rows inside that band really did put a
  sample outside the data; the guard was right and the closed-form criterion was wrong.
  Both runner and test now compute `X_reach(M)` from the module's own grid constructors,
  and the 113 ulp is pinned as a gate so nobody "simplifies" it back.
* **B3 — profile- and argument-blindness.** All 8 library profiles (CLM anchor, both
  negative controls, calibration sweep `alpha = 0.1 .. 1.5`) pass in-window: **0 of 8**
  flagged. So does each of the two argument combinations an over-eager guard would most
  plausibly reject — `far_field='none'` (whose NaN branch must not run in-window: it did
  not, 0 NaN) and `far_field='power'` with `tail_exponent` omitted (whose `ValueError` must
  not fire when there is no far field to close: it did not, `exception = None`).
* **B4 — `domain_fields` itself.** All **4** integer flavours of a clean zero
  (`int`, `np.int64`, `np.int32`, `float 0.0`) return `domain_valid = True`; `1` returns
  `False`; `None` returns `None`. All four downstream surfaces called directly with
  `n_outside_grid=0` return `True` with **0** warnings and **0** exceptions.
* **B5 — numeric invariance.** Over 3 in-window configurations, every value returned with
  `n_outside_grid=0` threaded versus the argument omitted: **0 differences** across
  `fit_exponent`, `analytic_tail`, `norm_verdict`, every `weighted_partial_sums`
  checkpoint, and the `k`/`hk`/`hk_real_basis` arrays. The guard adds fields and computes
  nothing — independently reconfirmed here on in-window input at three `(X_max, M)` pairs
  the bench A/B never visited.
* **B6 — negative controls, so none of the above is vacuous (lesson 90).** **3 of 3**
  genuinely out-of-window calls fire, warning and reporting `domain_valid = False` on
  **8 of 8** surfaces. The sharpest is one relative `1e-9` below the boundary: **2** of 512
  samples leave and it fires. The last reproduces leg 84's headline count **exactly** —
  **14 of 16384** at the shipped `X_max = 745.2`.

## The one thing worth flagging that is NOT a false positive

Staying in-window at the shipped domain caps the transform size: `X_reach(1024) = 651.9`
but `X_reach(2048) = 1303.8 > 745.2`, so **`M <= 1024`** there. On the calibration family
at `alpha = 0.4` (exact `p = 1.4`) the in-window exponent runs
`M = 256 -> 2.5948`, `512 -> 2.1427`, `1024 -> 1.5207` (errors `1.195`, `0.743`, `0.121`).
That is **leg 55's own tension restated as a magnitude** — the trustworthy domain and the
resolved exponent pull apart — and it is banked as `context_resolution_cost_of_staying_in_window`,
explicitly labelled context. It is **not** a defect of the guard, which computes nothing;
**not** a claim about the target, whose exponent is leg 55's; and **not** an argument for
widening the domain, which a live ban forbids and this leg does not do.

`domain_valid = None` for a caller who does not thread the count is likewise **not** counted
as a false positive: it is documented, deliberate, falsy-on-purpose, and already owned by
adversarial gate 13's standing gap-pin. It is a statement that provenance is unknown, not a
claim that a violation occurred, and this leg measured that it is silent (**0** warnings).

## Disposition

Per the gate's no-branch: **confirmed the guard is precise — it catches violations without
rejecting valid input.** Banked as `test_target_norm_postrepair.py`, 9 permanent gates,
9/9 passing in 2.3 s, sitting alongside `test_target_norm_adversarial.py`: that file pins
the guard's SENSITIVITY, this one pins its PRECISION. `solver/target_norm.py` was **not
modified** — the diff confirms it.
