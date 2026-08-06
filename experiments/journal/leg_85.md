# Leg 85 — Route-GRA: adversarial audit of `solver/gclm_rescaled.py`'s fixed-point reporting

**Agent:** LEG-C. **Branch:** `leg/gra-v1`. **Date:** 2026-08-06.
**Merge base:** `925913a`. **Module audited and NOT edited:** `solver/gclm_rescaled.py`.

## Gate, verbatim

> Under an adversarial battery of non-convergent upwind-transport trajectories (sustained
> oscillation, slow drift near a saddle rather than the fixed point), does
> `solver/gclm_rescaled.py`'s relaxation loop ever report having reached the fixed point when it
> has not?

## Answer: **YES** — 4 of 25 trajectories. Escalated, not patched.

The yes-branch forbids repair under this leg's own authority. `solver/gclm_rescaled.py` is
byte-identical to `origin/main`; `git diff origin/main -- solver/` is empty. The branch is
pushed for the orchestrator; it is **not** merged to `main` by this leg.

## Order of work (the protocol, in the order it was actually run)

1. `plan_of_record.py` run first. The relevant standing bans: *"another gCLM measurement leg"*
   and *"building a solver without grepping `capabilities.py` for the object first"*.
2. **Ban distinction confirmed before proceeding** (recorded in `writeup/novelty/leg_85.md` §0):
   the banned object is a gCLM *physics measurement*; this leg's object is the Python predicate
   `res < tol` at `gclm_rescaled.py:157` and the `break` at `:145-146`. `a = 0` throughout, one
   model point, no parameter sweep. Same clearance as legs 83/84.
3. `capabilities.py` grepped. Line 69–72 is the entry under audit; its `validated` field —
   *"relaxes to the exact CLM self-similar fixed point -4X/(1+4X^2)"* — is the claim tested.
   Nothing was rebuilt; no solver was written.
4. **Novelty pass written and committed BEFORE construction** (`e1b95d9`), including the battery
   design and a binding cap on the claim, both fixed before any trajectory was run.
5. Battery built, run, curated to JSON; regression test built; findings appended.

## The finding, in one paragraph

The rescaled CLM fixed point is a **one-parameter line**, not a point: `X ∂_X` is scale-invariant,
so `Ω_λ(X) = Ω₀(λX)` is an exact steady state for every `λ > 0` (measured residuals 2.11e-06 …
4.03e-04 for λ = 0.25 … 2, all with `c_omega` within 1e-2 of −1). The member is selected by the
origin slope `f(0) = −4λ`, **which the scheme freezes exactly**, and the module's docstring tells
callers the amplitude is a **free gauge**. The residual `‖f_τ‖_inf` is exactly degree-1 in λ
(measured `residual/λ` = 2.9373, 2.9423, 2.9423 at λ = 1e-3, 1e-6, 1e-9) while `tol` is a fixed
**absolute** number. So the stopping test is not scale-invariant along the one direction the
module declares free, and for **λ < tol/2.942 = 3.40e-09** the loop satisfies it on the initial
data and returns `converged=True` after **one step**, having relaxed nothing.

## The exact failing trajectory

```python
s = RescaledCLM(n=601, c=0.5, rho_max=7.0)
r = s.run(1e-10 * (-4.0 * np.exp(-s.X**2 / 2.0)), dt_frac=0.4, tol=1e-8, max_steps=20000)
# r["converged"] is True, after r["steps"] == 1
```

`converged=True`, `steps=1`, `residual=2.942e-10`, `c_omega=+1.00000` against the exact **−1**
(wrong **sign**), `‖Ω−Ω₀‖_inf = 1.000` = **100%** of `max|Ω₀|`, and — the decisive number —
**post-stop relative drift 1.0000**: the returned state moves by its **entire own amplitude**
over 4000 further steps of the same integrator, where a genuinely relaxed trajectory scores
**2.47e-09**. Identical verdict at n = 401/601/901, so it is the predicate, not the grid.

## Method note: the adjudicator this leg introduces

An absolute residual cannot adjudicate its own soundness, so the battery scores every trajectory
by **post-stop relative drift** — `‖f(after N more steps) − f_returned‖_inf / ‖f_returned‖_inf`.
It is dimensionless and invariant under the very gauge that breaks the stopping test, which is
why it forecloses the defence *"`res < tol` was literally true"*. Threshold for calling a false
positive was set at 1e-3, three decades above the ~2e-9 a relaxed trajectory shows. This may be
reusable for the sibling loops (`hl_rescaled.py:418,573`, `boussinesq_rescaled.py:278`, whose
capabilities line already admits it limit-cycles).

## What the battery found ROBUST (recorded so the audit is not one-sided)

* **No NaN bypass.** Overflow, a planted NaN, and `dt_frac` = 2.0/3.0 past the stability limit
  all give `residual = nan` and all correctly report `converged=False`. Unlike
  `critical_dissipation.py` (leg-41 NaN guard), this loop never needed one.
* **Oscillation — the gate's FIRST named case — does not break it.** `dt_frac` 0.8/1.0/1.2/1.5
  all still land on Ω₀ (shape err 1.07e-05, drift ≤ 2.47e-09); a mode-6 modulation lands on gauge
  member λ=1.3 at the exact rate. The gate's **second** named case (slow drift rather than the
  fixed point) is the one that broke it, in the specific form of the scaling gauge.
* **Nothing on `main` is impugned.** Every banked run and every trajectory in
  `test_gclm_rescaled.py` uses `f(0) = −4` (λ=1), where the report is trustworthy in **both**
  directions — a relaxing datum converges honestly (drift 2.47e-09) and a still-drifting
  far-field datum is correctly reported `converged=False` after 40000 steps. Battery field
  `false_positive_at_validated_gauge_f0_minus4` is **`false`**. This is a **latent** defect.

## Secondary, reported not escalated

1. `step()` returns the residual of the state passed **in**, so `result["residual"]` is one
   iterate stale — measured 3.187087 reported vs 3.090352 for the state returned, **3.13%**.
2. `f ≡ 0` reports `converged=True`, `residual` exactly 0.0, `c_omega=+1.0`. A genuine fixed
   point (drift 0.0), so not a kinematic false positive — but not the CLM one, and the wrong-sign
   rate is handed back unflagged.
3. `"converged"` is a raw `numpy.bool_`, not cast to `bool` as the sibling loops at
   `hl_rescaled.py:418,573` and `bordered_hl.py:253` all do. Cosmetic.

## Deliverables

| file | what |
|---|---|
| `experiments/p2_route_gra_v1_adversarial.py` | the battery: 25 trajectories, 4 families (G gauge, S gauge-line members, O oscillation, N trivial/non-finite) + the scaling law, the resolution check, and the off-by-one probe. ~56 s. |
| `writeup/data/p2_route_gra_v1_adversarial.json` | every magnitude, curated |
| `test_gclm_rescaled_adversarial.py` | 8 permanent regression tests, ~11 s, all passing |
| `writeup/novelty/leg_85.md` | novelty pass (pre-construction) + findings |

**On the regression test under a `yes` outcome.** The battery is banked as required, but since
the defect is unrepaired, `test_gauge_false_positive_is_locked_in` asserts the defect **as
measured** and is written to fail loudly in **either** direction. Its docstring instructs whoever
repairs the line to delete it and assert the repaired predicate rather than loosen it.

## The repair NOT made, for the orchestrator

Not applied, and offered only as information: make the stopping test relative to the gauge the
scheme has **already frozen** — `res < tol * max(|f(0)|/4, floor)` — or normalize the datum on
entry and reject `f(0) = 0`. Either makes the test scale-invariant along the declared-free
direction, and neither changes any banked λ=1 number (multiplier is exactly 1 there). One line,
in a file this leg is forbidden to touch. **The decision is the orchestrator's.**
