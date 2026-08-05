# Leg 84 — Route-TNA novelty pass (run BEFORE construction)

**Date:** 2026-08-06. **Agent:** LEG-E. **Branch:** `leg/tna-v1`.
**Verdict: `PROCEED_AS_AUDIT`.** This leg builds no new mathematics, measures no new
physics, and claims no novel mechanism. It adversarially audits one *software* property of
`solver/target_norm.py`: whether the module signals, at its own API boundary, that a caller
has pushed sample points outside the window in which `capabilities.py` says its exponent is
trustworthy. The physics of that window was measured by leg 55 (Route-NB) and is already
banked; nothing here re-measures it, and nothing here extends any domain.

## 1. What is already known, and by whom

* **Leg 55 (Route-NB), landed.** Measured the target's coefficient decay
  `p = k^-1.3937 (X_max = 4.1e+04) / k^-1.3963 (3.0e+05)` and recorded, in the
  `capabilities.py` validated line for `solver/target_norm.py`, the limitation this leg
  starts from: *"DOMAIN-limited, not resolution-limited: at the shipped X_max = 745 the
  far-field closure moves the exponent by 0.190 and the measurement is not trustworthy
  there; the headline is taken where no sample point leaves the grid."* That sentence is
  the **prior art for the physics**. This leg's claim is disjoint from it: the question is
  whether the *code* says any of that to a caller who does not read `capabilities.py`.
* **`test_target_norm.py` already has two relevant gates** (items 17 and 18): that the
  far-field closure *fires* at `X_max = 745` and not at `4e+04`, and that firing moves `p`
  by more than 0.02 across the `power/clamp/zero` ablation. Both are assertions *about the
  physics of the closure*, made by a test that supplies the threshold itself. Neither
  asserts that the module **reports** a domain violation to its caller, and neither
  exercises the exponent-returning surface (`fit_exponent`, `analytic_tail`,
  `norm_verdict`) at all. So the guard question is untested.

## 2. Repo-internal prior-art sweep (magnitudes, not booleans)

| probe | count |
|---|---|
| solver modules under `solver/` | 43 |
| of those calling `warnings.warn` | **0** |
| `raise` sites in `solver/target_norm.py` | 4 (all shape/argument validation: mismatched shapes, missing `tail_exponent`, unknown `far_field`, non-finite `h`) |
| `raise`/`warn` sites keyed on a **domain threshold** | **0** |
| occurrences of the literal `745` inside `solver/target_norm.py` | 2, **both in prose** (module docstring lines 75 and 211); 0 in executable code |
| module-level constants encoding a validated `X_max` | **0** |
| API surfaces returning any domain diagnostic | 2 (`compactify`'s third return value, `spectrum`'s `n_outside_grid` key) — a raw **count**, compared against no threshold |
| of 56 `test_*.py` files, those touching `compactify`/`n_outside_grid` | **1** (`test_target_norm.py`) |
| prior legs whose novelty log or journal mentions `target_norm` | **1** (`experiments/journal/leg_55.md`, the physics leg) |
| prior leg auditing target_norm's *guard* behaviour | **0** |

`warnings.warn` being absent from all 43 solver modules matters for how the finding must be
phrased: "no warning is emitted" is not a deviation from a repo idiom, because the repo has
no warning idiom. The repo's two idioms are (a) `raise` on an argument the function cannot
honour, and (b) a diagnostic field in the returned dict. Only (b) is present here, and only
on `compactify`/`spectrum`, never on the functions that return the exponent.

## 3. External prior art

The hazard class — *a numerical routine that silently extrapolates outside its validated
window* — is a named, textbook hazard (silent extrapolation / out-of-domain evaluation;
the same class as the unflagged `interp1d` extrapolation that scipy later made opt-in via
`bounds_error`). It is **not novel** and this leg does not present it as such. The leg's
deliverable is therefore a *measured* statement about one specific module in this
repository, with magnitudes, not a contribution to the literature.

## 4. What this leg may and may not claim

* MAY claim: how many adversarial inputs cross the documented window; how much the exponent
  moves when they do; and exactly which fields, if any, of the returned objects carry that
  information.
* MAY NOT claim: that the exponent shift itself is new (leg 55 measured it), that the window
  should be widened (a live ban forbids closing gaps by extending the domain, and this leg
  extends nothing), or that any patch is warranted under this leg's own authority.

## 5. Bans checked against this leg

`plan_of_record.py` was run first. Relevant bans: *"building a solver without grepping
`capabilities.py` for the object first"* — done, the `solver/target_norm.py` entry is quoted
above and in the runner; *"closing the truncation gap by extending the domain"* — this leg
varies `X_max` only as an adversarial probe of the guard and closes nothing; *"another gCLM
measurement leg"*, *"re-measuring beta on the 2D object"* — not this object. No ban fires.
