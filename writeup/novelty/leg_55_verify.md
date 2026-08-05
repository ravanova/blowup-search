# Leg 55 — VER-B independent review of `leg/nb-v1` (HEAD `94e6322`)

**Verifier:** VER-B, branch `verify/nb-v1-review`. **Scope:** line-by-line review of leg 55's
PR after it passed `scripts/merge_gate.sh`. I report gaps; I do not repair. Nothing in the
leg's territory was edited by this review — the only file added is this one.

**Bottom line: SIGN OFF, with three findings to fix in-place before or at merge, none of
which touches the gate answer.** The gate answer `YES` is independently reproduced and
survives every correction below. One finding (F1) is quantitative and does change a
published number and one row of the norms table.

---

## 1. What I independently confirmed

Everything here was re-run or re-derived by me, not read and nodded at.

**Gates.** `test_target_norm.py` → **23/23 pass** on my own run. I read the implementations of
the positive control, both negative controls, the closure ablation and the two regression
gates rather than trusting their names.

**Headline exponent.** Re-solved and re-measured from scratch at the headline domain
(`ρ_max = 12`, `M = 16384`, band `[32,256]`):

| `n` | Newton residual | `α` | `p` | pts outside grid |
|---|---|---|---|---|
| 401 | 6.86e-15 | 0.397345 | 1.393723 | 0 |
| 801 | 1.33e-14 | 0.397353 | 1.393745 | 0 |
| 1601 | 3.01e-14 | 0.397356 | 1.393757 | 0 |
| 3201 | 6.33e-14 | 0.397358 | 1.393764 | 0 |

This reproduces `p = 1.3937` and **independently confirms the one claim-bearing sentence in
the PR that has no JSON backing** — TECHNICAL §4.1's "confirmed at `ρ_max = 12`:
`p = 1.3937 → 1.3938` across `n = 401 → 3201`". Drift `4.1e-05`. It also produces §1's
`≤ 6.3e-14` (it is the `n = 3201` residual). Both are true; they are simply not serialized.
This matters because the JSON's resolution ladder is at `ρ_max = 8` only, so this sentence is
the *sole* evidence that the headline domain is resolution-converged. It is correct.

**Numbers vs. the curated JSON.** I sampled far more than the brief asked. Confirmed matching
to the digits quoted: `p = 1.3937 / 1.3963`; all four domain-ladder rows (`p`, `p−1`,
`(p−1)−α`, physical-space tail exponent, `α`); the three margins `+0.39374 / +0.09374 /
−0.60626`; `S_4096` and the tail bounds in §6; `C = 0.48560`; the window `gap = +0.60265,
empty = True`; §5.1 closure spread `0.190` and `finest cell reaches 1.043e+04`; §5.2's full
interpolation table including the `rel_diff_vs_order12` column; §5.3's `M` and band tables and
both spreads; §6.1's `V` row. **One column does not match — see F3.**

**Controls are real and can report the other answer (lesson 90).** The positive control runs
the *full* pipeline (`BorderedHL` grid → `compactify` → interpolation → FFT) and its window
(`1e-10` / `1e-08`) was pre-registered. The closure ablation is demonstrably not a tautology:
where it fires the three closures give genuinely different `p` (spread `0.190` shipped,
`0.4166` in gate 18). The strongest lesson-90 evidence in the PR is historical and it is
sound: negative control 1 *did* report the other answer twice (`p = −0.06`, `p = −0.25`) under
two earlier fitters, and gates 14/15 reconstruct exactly those two spectra shapes and would
fail loudly on a regression. The leg's self-report of catching its own vacuous "0.00000"
ablation is confirmed against `experiments/journal/leg_55.md` and against the code
(`n_theta_points_outside_grid` is reported beside the identical numbers, and
`P5_headline_needs_no_extrapolation` is in `evaluation`).

**Fitter methodology.** Sound and unusually well-reasoned. Log-spaced bins merged to ≥ 8
modes, **linear** mean within bin, least squares on the bin means; stated fit band with a
4-band sensitivity sweep. The linear mean is correctly argued to be the physically right
object for an `ℓ¹` question. The two documented failure modes are real and are genuinely
regression-gated.

**Figure.** `p2_route_nb_v1_targetnorm_evidence.py` regenerates `fig50` from the committed
JSON **byte-identically** (clean `git status` after the rebuild). The figure matches its data.

**Territory.** The diff against `main` is **exactly the 12 declared files**, 4566 insertions,
no deletions. `capabilities.py` is a clean `+29`-line append at the end of `CAPABILITIES`
with no reordering or edits above it; `writeup/build_figures.py` is a clean `+4`-line append
to `P2_EVIDENCE`. `solver/spectral_certificate.py` and `solver/bordered_hl.py` have no diff,
as the independence condition requires.

---

## 2. Findings

### F1 — the quoted instrument systematic is measured at a transform size 4× finer than the headline (**substantive**)

`experiments/p2_route_nb_v1_targetnorm.py` line 62 sets `M_PRIMARY = 16384`, and every target
measurement uses it. But line 127 builds `th = midpoint_theta_grid(65536)`, and the
calibration family — and both negative controls — reuse that `Xt`. **The calibration that
produces the quoted systematic `+0.0022` is run at `M = 65536`; the headline it is quoted
against is run at `M = 16384`.**

I swept the calibration systematic against `M` myself (band `[32,256]`):

| `M` | `α=0.1` | `α=0.2` | **`α=0.3935`** | `α=0.6` | `α=1.0` | `α=1.5` |
|---|---|---|---|---|---|---|
| 4096 | +0.03132 | +0.02484 | +0.01613 | +0.01073 | +0.00667 | +0.00680 |
| 8192 | +0.01492 | +0.01140 | +0.00722 | +0.00516 | +0.00457 | +0.00622 |
| **16384** | +0.00752 | +0.00571 | **+0.00389** | +0.00335 | +0.00405 | +0.00612 |
| 32768 | +0.00411 | +0.00325 | +0.00263 | +0.00275 | +0.00392 | +0.00611 |
| **65536** | +0.00253 | +0.00219 | **+0.00215** | +0.00256 | +0.00388 | +0.00610 |

The bottom row reproduces the committed calibration table exactly (JSON:
`0.0025275, 0.0021904, 0.0021524, 0.0025575, 0.0038844, 0.0061032`), which confirms the
diagnosis rather than merely suggesting it. **At the headline's own `M = 16384` the systematic
at the target's `α` is `+0.0039`, not `+0.0022` — 1.8× larger.** Worst over the sweep at
`M = 16384` is `+0.0075`, not `+0.0061`.

This is not carelessness: at `M = 65536` the finest `θ` cell reaches `|X| = 2M/π = 4.17e+04`,
which exceeds the headline's `X_max = 4.07e+04`, so the closure would start firing and the
`n_outside = 0` property the headline rests on would be lost. The leg was right to keep the
target at `M = 16384`. But that makes it *more* important, not less, to quote the systematic
at the `M` actually used.

The systematic is **positive** (the fitter over-estimates `p`), so the correction moves `p`
down: bias-corrected `p ≈ 1.3937 − 0.0039 = 1.3898`.

**Consequences.**
- `s = 0`: margin `+0.390` — survives by 100×. **Unaffected.**
- `s = 0.3`: margin `+0.090` — survives by 23×. **Unaffected.**
- **`s = 0.39`: margin `−0.0002`.** TECHNICAL §6 justifies not relying on this row by saying
  its margin `+0.0037` is "only `1.7×` the calibration systematic `0.0022`". At the headline's
  own `M` the true ratio is **`0.96×`** — i.e. below one. The *conclusion* ("reported but not
  relied on", "thin") is the right call and I endorse it, but the quantitative justification
  errs in the unsafe direction, and the row should be reported as **not resolved** rather than
  as finite-but-thin. Correspondingly `evaluation.admissible_classes_with_finite_norm`
  currently reads `[0.0, 0.3, 0.39]`; `0.39` should drop out or be marked unresolved.
- `s = 1`: margin `−0.610`. **Unaffected, still divergent.**
- **The gate answer `YES` is unaffected** — it needs one admissible `s < 0.394`, and it has two
  with margins two orders of magnitude clear of any version of the systematic.

BLOG line 49 ("finite for **every** `s < 0.394`") and line 107 ("worst-case error of
**0.006**. That is the instrument's error bar") both inherit this and should be narrowed;
the TECHNICAL is more careful than the BLOG here, and the two should agree.

### F2 — the calibration and both negative controls bypass the interpolation stage; I closed this gap myself (**scope issue, magnitude nil**)

The calibration family and negative controls 1 and 2 are evaluated analytically **directly on
the `θ` grid** (`Xt = X_of_theta(th)`), so they exercise only the FFT + fitter. They never
touch `compactify`, the `ρ`-grid Lagrange interpolation, or the far-field closure. Only the
positive control runs end-to-end, and it is a *single mode* — the easiest possible object for
an interpolator. So as shipped, the interpolation path is never calibrated on an object with a
nontrivial exponent, while §2.3 presents `+0.0022` as "**the instrument's** error bar" and §2
is titled "The instrument".

I ran the missing end-to-end calibration: sampled `calibration_family` on the solver's own
`BorderedHL` grid and pushed it through `spectrum()` (interpolation and all), at both
`ρ_max = 8` and `ρ_max = 12`, against the θ-direct path.

**The interpolation-attributable difference in `p` is `< 1e-5` at every `α` and both domains
— zero to five decimals.** The gap is real in scope but empty in magnitude. The leg's
systematic is not undermined by it, and its interpolation-order ablation (order 8 vs 12 moves
`h` by `1.5e-09` relative at `ρ_max = 12`) was already good indirect evidence. Recommend
folding one end-to-end row into the calibration table so the claim is calibrated rather than
argued; no number changes.

### F3 — "every number is a field of the JSON" is false for three items, and the JSON is the stale one (**housekeeping**)

TECHNICAL line 7 asserts "Every number in this document is a field of the JSON"; the leg
reports "0 unmatched" from its own machine check. Three items are not JSON fields:

1. §4.1's Newton-residual column (`7.4e-15 / 1.5e-14 / 2.3e-14`). The JSON's
   `newton_residual` entries for those rows are `4.80e-15 / 1.24e-14 / 2.09e-14`.
2. §1's "`≤ 6.3e-14`".
3. §4.1's `n = 401 → 3201` confirmation sentence.

Items 2 and 3 I verified by direct re-run — they are correct (see §1 above). Item 1 is the
interesting one: **my re-run at `ρ_max = 8` gives `7.4385e-15 / 1.4599e-14 / 2.2760e-14`,
which matches the DOCUMENT and not the JSON.** So the prose is reproducible and the committed
JSON's residual field is stale — that field was not regenerated by the final code. Nothing
claim-bearing depends on it (all values are ~1e-14 and convergence is not in question), but
the leg's own number-matching check evidently does not cover that column, which is worth
knowing since "0 unmatched" is doing reassurance work across the whole PR.

### F4 — minor attribution: `+0.603` is close to a number leg 51 already published

Leg 51's own `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md` §9 already states "**The window
is empty by 0.606 in exponent units**". Leg 55's `+0.60265` is a confirmation of that, not a
new quantity. TECHNICAL §7 point 1 states the actual delta correctly and modestly ("the object
side is now a measurement where it was previously a docstring derivation applied to an assumed
`α`"), and the BLOG says "one side was a measurement and the other was a docstring". That is
honest. But §7 point 3 states "the window is **empty by `+0.603`** in exponent units, with both
sides measured" without citing leg 51's prior `0.606`, and a reader could take `+0.603` for a
new finding. Recommend one clause citing leg 51's number. No claim changes.

---

## 3. The ban-clause self-correction — I judge leg 55's framing **correct**, and on stronger evidence than it cites

This is the item the brief flagged as most important, so I traced it to its origin rather than
stopping at the plan.

The ban text, verbatim from `plan_of_record.py` (line 702, printed output):

> *reading leg 51's exactly-zero `Y_0` as progress toward the target -- it is exactly zero
> because the a=0 CLM profile IS one basis mode; the non-symmetric Hou-Luo profile is not, and
> **does not have finite norm in the class where the operator is least bad*** — (lifted by:
> never -- the ceiling was pre-committed as clause S7)

Leg 55 argues "the class where the operator is least bad" means `s = 1`, and cites "leg 51's
divergence-curve minimum". That inference is correct, and it is **directly attested**, not
merely inferred. Two independent textual anchors:

1. The adjacent ban entry in the same list: *"tuning the weight exponent s toward the minimum
   of leg 51's divergence curve -- **that minimum (s = 1)**..."*
2. Decisively, the originating document — leg 51's own
   `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEL1_V2.md` §9, which is where the phrase comes from:
   > *"The operator side, measured: the tail's divergence exponent as a function of `s` is a
   > U-curve with its **minimum at `s = 1.00`** (exponent +0.64), rising to +1.28 at `s = 0`
   > and +1.27 at `s = 2`. ... **The class where the operator is least bad is the class where
   > the target has infinite norm**, and vice versa."*

That last sentence is the phrase itself, in its own document, explicitly attached to the
`s = 1` U-curve minimum. There is no ambiguity left.

I considered and reject the competing reading — that "least bad" might mean "the class where
the method works best", which would be `s = 0 / 0.3` (where leg 52 measured the repair
working) and under which the clause **would** be false. That reading is unavailable: the plan
describes `s = 1` as "the ONE exponent at which bordering cannot help", i.e. the *worst* class
for the method, so "least bad" cannot be method-relative. It is a property of the operator's
own divergence curve, and that curve's minimum is `s = 1`.

**Therefore: the ban clause, read literally, is CORRECT.** At `s = 1` the target's norm does
diverge, margin `−0.606` (`−0.610` bias-corrected). The gate's yes-branch text — "the ban-list
clause asserting it is not is **factually wrong**" — **overstates the finding, and leg 55 is
right to refuse to propagate it.** I endorse the leg's self-correction without reservation;
this is the leg pushing back correctly against its own dispatch, and it should not be talked
back out of it.

**The accurate framing for escalation** is leg 55's: *not* "the ban text is wrong", but "the
ban text is literally correct, and its practical window is now measured empty from both
sides — the object side having moved from derivation to measurement". The one thing I would
add for the Decision Maker: the clause is correct but **incomplete in a way that misleads in
practice**, because as written it invites the reading "the target is not in the space", full
stop — and that reading *is* false. The target is comfortably in the space at `s = 0` and
`s = 0.3`, the classes legs 52 and 53 actually used, with margins ~100× and ~23× the
instrument's systematic. That consequence — **"the target was never in the space" is not an
available explanation for legs 52–53's failures, and leg 53's block coupling stands as the
operative reason** — I independently confirm, and it is the part of this leg with real
downstream force.

---

## 4. Verdict

**Sign off on merging `leg/nb-v1`.** The gate answer `YES` is independently reproduced and is
robust to every correction I found. The controls are real, can fail, and one of them
demonstrably did fail twice and caught a live bug. The methodology is honest about its own
limits — including two self-caught lesson-90 traps that I verified are genuinely fixed and
genuinely gated. Territory is exactly as declared and the read-only imports are respected.

**Unresolved gaps: F1 is real and should be fixed** — the systematic quoted against the
headline should be `+0.0039` (worst `+0.0075`), the `s = 0.39` row should be reported as not
resolved rather than finite, `evaluation.admissible_classes_with_finite_norm` should drop
`0.39`, and BLOG lines 49 and 107 should be narrowed to match the TECHNICAL. **None of this
blocks the merge**: it changes one row of one table and a sentence of justification, and the
gate stands on `s = 0` and `s = 0.3` regardless. F2 I closed myself (magnitude nil); F3 and F4
are housekeeping.

**On the escalation: escalate as leg 55 frames it, not as the dispatch framed it.** The ban
clause is not factually wrong.
