# Leg 91 — Route-FGA v1: adversarial audit of `solver/fractional_gclm.py`'s critical-exponent path

**Branch** `leg/fga-v1`. **Exploration leg, standard, CLAIM-BEARING** (adversarial audit).
**Gate: YES — a silent-corruption gap.** `s < 0` (and `nu < 0`) are accepted silently, run to
completion, and return a finite, plausible-looking exponent that moves the measured `s_c`.
**Escalated, not patched:** leg 91 was forbidden to edit `solver/fractional_gclm.py` under any
outcome, and did not.

**This leg does not reopen, contest or re-measure `s_c = alpha/2`.** That result is validated
against XU eq (6.3) row by row and marked PRE-EMPTED under Route-J. It is settled physics and was
treated throughout as fixed background. Every number below is a statement about **code behaviour
under invalid input**; not one is a statement about the value of `s_c`.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read in full. `NG` is NEXT. The ban that could bite is *"another gCLM
   measurement leg — lifted by: never, the model is exhausted (Stage 3.5, leg 42)"*. It does not
   bite, and the distinction was confirmed before any work: this leg **measures no gCLM physics**.
   It runs the solver only as the *subject* of an input-validation audit, and no run's output is
   quoted as a physics result. Also honoured: *build nothing without grepping `capabilities.py`
   first* — done, entry at line 78, which is where the "PRE-EMPTED, Route-J" marking is recorded.
2. `DIRECTION.md` leg-91 entry read; thesis, gate and territory agree verbatim with the dispatch.
3. `solver/fractional_gclm.py` read in full (337 lines) — **read only, never edited.**
   `test_fractional_gclm.py`'s six gates read: all six exercise physically admissible `s` only,
   which is the gap.
4. **Novelty pass FIRST**, committed before any construction (`22d01ea`,
   `writeup/novelty/leg_91.md`), four queries, links not counts.
5. Then: runner, curated data, permanent regression gates, this note.

## What the novelty pass changed about the leg

Two things, and both reshaped the battery before a line of it was written.

**(1) It set the invalid-input boundary from the literature instead of from taste.** The
dissipative-gCLM corpus writes the dissipation as `Lambda^sigma`-hat `= |k|^sigma` with
**`sigma = 2s`**, and works at **`sigma >= 0`** throughout — global existence on the circle is
proved *"for `sigma >= 1` for all real values of the advection parameter `a`"* for small data, and
the lowest exponent anyone treats is the *"marginal"* `sigma = 0`, which carries a physical
reading (Oldroyd-B stress). So `s < 0` is outside every published range, and — important for
honesty — **`s = 0` is ADMISSIBLE**. The first run of the battery had counted `s = 0` among the
"invalid inputs that returned a finite `p`"; that was wrong, and it was corrected before the
result was banked. `s = 0` is now carried as a **second positive control**. The literature gives
**no upper bound**, so the upper wall could not be asserted as physics and is instead *measured*
as a float64 property of the code.

**(2) It named the exact line to instrument.** Riesz-potential theory: for a negative exponent
the multiplier `|xi|^sigma` *"has a singularity at `xi = 0` … the operator is not well defined on
Schwartz space when the parameter is negative"*. The obstruction is **precisely the `k = 0`
mode**. And `solver/fractional_gclm.py` lines 160–161 are:

```
self.visc = np.abs(self.k).astype(float) ** (2.0 * self.s)
self.visc[0] = 0.0                       # the mean is not dissipated
```

For `s > 0` the second line is harmless. For `s < 0` it **overwrites the `inf` that is the
mathematical signal the operator is ill-defined**. The audit went straight there.

## The five batteries (`experiments/p2_route_fga_v1_adversarial.py`, n = 512, 141 s)

**A1 — the closed forms.** `critical_s(alpha) = alpha/2` and `relevance_exponent(s, alpha) =
1 - 2s/alpha` have no domain checks at all. **6 of 10 malformed arguments returned a finite value
with no exception and no warning**: `critical_s(-1.0) = -0.5` (a negative critical dissipation
exponent), `critical_s(+inf) = +inf`, `critical_s('0.8') = 0.4` (a **string**, coerced by
`np.asarray(x, float)`), `relevance_exponent(-0.5, 1) = +2.0`, `relevance_exponent(-2.0, 1) =
+5.0`, `relevance_exponent(1e6, 1) = -1999999.0`. Correct behaviour where it exists is recorded
too: both propagate NaN cleanly, and `alpha = 0` gives `-inf` rather than a number.

**A2 — operator construction, and the mask.** At `s = -0.5` the raw `k = 0` entry of `|k|^{2s}`
is **`inf`**, and the next line replaces it with `0.0`, leaving `visc` **entirely finite**. What
survives is worse than an `inf`: `visc` is **strictly decreasing in `|k|`**, with
`visc[k_max]/visc[1] = 1/k_max` **exactly** (3.906e-3 at n = 512; 7.8125e-3 at n = 256). That is
an operator that damps the *largest* scales hardest — a smoothing multiplier wearing the
dissipation's name. **The sign inversion emits nothing.** The single warning raised is
`'divide by zero encountered in power'`, which is about the `k = 0` entry the next line
overwrites; no field of any returned object records the inversion. Measured upper wall:
`visc` goes non-finite for `s > 64.0000` at n = 512 (`s > 73.1429` at n = 256), i.e.
`s_ovf = log(DBL_MAX)/(2 log k_max)`.

**A3 — the full pipeline** (`FractionalGCLM.run` → `estimate_T` → `fit_relevance`), one row per
input. Of **5 invalid-`s` inputs, 2 returned a finite `p` with no exception** (`s = -0.5` →
`p = +2.1864`; `s = -2.0` → `p = +3.2481`) and **3 refused with `p = nan`** (`s = 60`, `s = 200`,
`s = NaN`). Controls: `s = 0.35` → `p = +0.4948`, `s = 0` → finite, both correct. The two silent
rows are indistinguishable in *form* from the control — same dict, same keys, same outcome string
`'under_resolved'`, no exception.

**A4 — THE HEADLINE, the contamination of the measured `s_c`.** Route-F locates the measured
`s_c` as the **zero crossing of a straight-line fit of `p(s)`**. A clean 7-point line gives slope
`-1.9744`, crossing `s = 0.602492`. Injecting **one** invalid point:

| injected | `p` returned | crossing moves | shift | slope |
|---|---|---|---|---|
| `s = -0.5` | `+2.1864` finite | `0.602492 → 0.602075` | **−0.000417 (−0.07 %)** | −1.9744 → −1.9819 |
| `s = -2.0` | `+3.2481` finite | `0.602492 → 0.682800` | **+0.080308 (+13.33 %)** | −1.9744 → −1.2419 |

Both crossings are audit artefacts at n = 512 and **neither is a physics number** — only the
*difference* is claimed, and clean and contaminated share every setting so resolution bias
cancels. The `s = -0.5` row is the more disquieting of the two: a **0.07 % shift is invisible**,
so the corruption is not merely silent at the module boundary but undetectable downstream. The
reason is A1's gate 5 — `p = 1 - 2s/alpha` is a *line*, so an invalid `s` gets a value that sits
**on** the valid points' line (`+2.1864` measured against the formula's own extrapolation
`+2.0000`, within 9 %). **A plausibility check on the value cannot catch this.**

**A5 — the dissipation strength `nu`.** The gate's NaN-poisoning case is handled **correctly**:
`nu = NaN` and `nu = +inf` both give outcome `'diverged'` at step 1 with `p = nan`. But
`nu = -1e-3` — anti-dissipation, an energy *source* — returns a finite `p = +0.5264` against the
control's `+0.4948`, **+6.38 %**, with no exception and no warning. The sign of the dissipation is
never checked anywhere in the module.

## The gate, answered

> *Under an adversarial battery (negative `s`, `s` above the model's admissible threshold,
> NaN-poisoned dissipation strength), does `solver/fractional_gclm.py`'s critical-exponent
> computation ever silently return a finite, plausible-looking `s_c` instead of propagating or
> flagging the invalid input?*

**YES.** And the answer is precisely one-sided, which is the useful part:

* **The two cases the gate expected to be dangerous are SAFE.** `s` above the model's threshold
  refuses (`p = nan`, whether just under the float64 wall at `s = 60` or over it at `s = 200`),
  and NaN-poisoned `nu` refuses (`'diverged'`, `p = nan`). Both are banked as ordinary
  regressions so a future "fix" cannot quietly turn them silent.
* **The gap is entirely on the LOW side**, which the gate did not anticipate and the novelty pass
  found first: `s < 0` and `nu < 0`. It exists because `visc[0] = 0.0` — a line written for a
  correct physical reason ("the mean is not dissipated") — happens to overwrite the exact `inf`
  that Riesz theory says is the signal of an ill-defined operator, and nothing else in the module
  ever looks at the *sign* or the *monotonicity* of what it built.

**The exact failing case, in one line:** `FractionalGCLM(n=512, a=0.0, nu=1e-3, s=-0.5)` builds
a monotonically **decreasing** `visc` with `visc[0]` masked from `inf` to `0.0`, runs to
completion, and returns `p = +2.1864` — which, injected into the `p(s)` fit whose zero crossing is
the measured `s_c`, moves that crossing by −0.07 % (invisible) at `s = -0.5` and by +13.33 % at
`s = -2.0`, with no exception, no flag, and no field recording it.

## Disposition, and what is explicitly NOT claimed

* **No patch.** `solver/fractional_gclm.py` is byte-identical to `origin/main`; leg 91's territory
  forbids editing it under any gate outcome, and the yes-branch says escalate. **Escalated.**
  The obvious repair (validate `s >= 0` and `nu >= 0` in `__init__`, and check the monotonicity of
  `visc` before masking `k = 0`) is one the orchestrator commissions, not this leg.
* **The 13 gates in `test_fractional_gclm_adversarial.py` PIN the current silence deliberately.**
  Gates 2, 3, 5, 6, 7, 8, 9 and 13 **will fail the day a guard lands. INVERT them, do not weaken
  them** — keep every magnitude at the same threshold and flip only the sign of the signal claim
  (the pattern leg 84 set and leg 87 followed). Gates 1 and 4 are positive controls; 10–12 are
  regressions on behaviour the module already gets right. Runtime 17 s.
* **No novelty is claimed.** The novelty pass pre-empted it: a defect in this repository's own
  code, measured against a boundary already in print, is not a discovery. The method
  (adversarial battery, propagate-or-flag) is established practice.
* **Nothing here is a statement about the value of `s_c`.** `s_c = alpha/2` remains validated
  against XU eq (6.3) and PRE-EMPTED under Route-J, exactly as it was before this leg ran.
  The relevance-line crossings quoted above are n = 512 audit artefacts used only as a
  clean-vs-contaminated *difference*, and are not comparable to Route-F's measurements.
