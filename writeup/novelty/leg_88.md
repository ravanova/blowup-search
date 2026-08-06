# Leg 88 novelty pass — Route-GCA: adversarial audit of `solver/gclm_family.py`

Run BEFORE construction, per the leg contract.

## Question being claimed

Under an adversarial battery (NaN/Inf-poisoned `c_l`/`c_omega`, `a` far outside `[0,1]`), does
`solver/gclm_family.py`'s residual computation ever silently return a finite, plausible-looking
value instead of propagating the invalid input or flagging it?

## In-repo prior art

| source | what it covers | overlap with leg 88 |
|---|---|---|
| `test_gclm_family.py` (12 tests) | a=0 one-scale known-answer gate (RMS 2.2e-7), velocity operator, parity, GA recovery, two-scale gate, relnorm scale-invariance, mixed genome, sq-Lorentzian basis | none — every test uses well-formed finite profiles and finite in-range coefficients. Grep for `nan`/`inf`/`adversarial` over the file: zero hits. |
| `test_nk_fourier.py` | imports `gclm_family` for a Newton-Kantorovich cross-check | correctness on well-behaved data; no malformed input |
| leg 66 (`writeup/novelty/leg_66.md`) | test-coverage census; lists `gclm_family` only as a *consumer* test of `solver/gclm.py` | census, not an audit |
| leg 69 | adversarial audit of `solver/interval.py` | same *pattern*, different module. Found a real gap (repaired later, closed by leg 87) |
| leg 79, leg 80 | adversarial audits of other modules | same pattern, different modules |
| leg 83, leg 85 | adversarial audits; both cleared the leg-42 gCLM-measurement ban on the same robustness-vs-measurement distinction | precedent for the ban ruling below; neither touched `gclm_family.py` |
| `test_bordered_hl_adversarial.py`, `experiments/p2_route_bhn_v1_adversarial.py` | the only adversarial battery files currently on main | bordered HL object, not the gCLM a-family residual |

No file in the repository passes a non-finite coefficient or an out-of-range `a` into
`GCLMResidual`. The question is unasked here.

## Ban check (plan_of_record.py)

The live ban reads "another gCLM measurement leg (lifted by: never -- the model is exhausted
(Stage 3.5, leg 42))". This leg measures **the residual code's response to malformed input**, not
the gCLM model's physics: it produces no new profile, no new `a`-sweep, no new self-similar
exponent, and no claim about blow-up in the a-family. It reads `solver/gclm_family.py` and edits
it under no outcome. That is the same robustness-vs-measurement distinction that cleared legs 83
and 85, and I confirm it independently here rather than inheriting it. Verified directly against
the printed ban list: none of the other nine live bans (Route-D sharpening, DSS, 2D beta, scaling
gauge, GA-on-unvalidated-fitness, the four leg-51/53 reading bans, Chen-Hou-as-target) touches an
input-validation audit.

The tenth ban — "building a solver without grepping `capabilities.py` for the object first" — is
discharged: `capabilities.py:64-68` registers `solver/gclm_family.py` as "gCLM a-family, rescaled
steady residual" with `test: test_gclm_family.py`. No adversarial/validation capability is
registered for it, and no other module offers one to reuse.

## External literature

Input-validation robustness of a research residual evaluator is an engineering property of this
specific file. There is no external claim to resolve: the finding is about this repository's code,
not about the gCLM equation, so no arXiv precedence question arises. (Contrast leg 57/VER-D, where
the claim was mathematical and Cadiot arXiv:2505.03091 had to be resolved.)

## Verdict

Novel within the repository. Proceed to construction.

---

# Leg 88 findings (written after the run)

## Gate answer: NO

> "Under an adversarial battery (NaN/Inf-poisoned `c_l`/`c_omega`, `a` far outside `[0,1]`), does
> `solver/gclm_family.py`'s residual computation ever silently return a finite, plausible-looking
> value instead of propagating the invalid input or flagging it?"

**No — 0 silent corruptions in 37 gate-scoped cases.** Confirmed robust; the battery is banked as
`test_gclm_family_adversarial.py` (13 tests, all passing). `solver/gclm_family.py` was not edited.

## What "silent" was defined to mean, before the run

The module has no validity flag, no `try/except`, no `nan_to_num`, no `clip`. Its whole contract is
the arithmetic it documents, so silence can only take two forms: swallowing a non-finite input, or
evaluating something other than the documented formula. Both were counted.

## Magnitudes

| family | cases | result |
|---|---|---|
| `c_l`/`c_omega` poisoned with NaN/±Inf, singly | 6 | each reached **100.0%** of 401 residual nodes; scalar norm non-finite in all 6 |
| `c_l`+`c_omega` poisoned jointly, all 9 pairs | 9 | all 100% non-finite; **+Inf/−Inf did not cancel** to a finite norm |
| `c_tw` poisoned (two-scale residual) | 3 | 100% non-finite |
| `a` ∈ {NaN, ±Inf} | 3 | advection branch correctly *taken* (`NaN != 0.0` is True); 100% non-finite on both residuals |
| `a` finite, nine decades outside [0,1] (\|a\|=1e1…1e9, both signs) | 12 | matches an **independent recomputation** of the documented formula to **1.96e-16** relative |
| `a` = 1e300 | 1 | overflows to `inf` — the honest answer, not a plausible finite number |
| extreme finite `c_l`/`c_omega` (±1e300, 1e-300, ±1e16) | 10 | all dwarf the 7.35e-07 baseline or overflow; none clamped |
| malformed shapes (wrong-length profile / coefficient array, (n,1) column, `a=None`) | 4 | all **raise** (`ValueError`×3, `TypeError`) — flagged, not silent |
| per-node `c_l` array with exactly one NaN | 1 | poisons **exactly 1** of 401 nodes — neither spreads nor vanishes |

Baseline for scale: one-scale anchor RMS **7.347e-07**, two-scale anchor RMS **1.229e-07** with
exact traveling-wave speed `c_tw = 0.500000`, at n=401.

## The anti-saturation evidence

A clamp is the failure mode that would matter most for `a`, and it cannot be ruled out by "the
number came back big". The signature used instead: `||R||/|a|` approaches the pure-advection
constant `k = ||U Ω_X||_rms = 0.2768551` with a deviation that **decays as 1/|a|** —

| \|a\| | 1e1 | 1e2 | 1e3 | 1e5 | 1e7 | 1e9 |
|---|---|---|---|---|---|---|
| dev × \|a\| | 8.0697e-07 | 8.0697e-07 | 8.0697e-07 | 8.0695e-07 | 8.0824e-07 | 8.8818e-07 |

constant to 6 decades (the drift at 1e9 is float64 resolution). A clamp or saturation would make
that product **grow**. `k` was computed independently, not fitted to the cases it judges.

## A criterion I got wrong, recorded rather than hidden

The magnitude branch was first written as "deviates from a *pure* linear law `||R|| = |a|·k` by
more than 1e-9 relative", and on the first run it flagged **2 of 8** cases — i.e. the battery
initially printed `GATE: yes`. That was my criterion being miscalibrated, not the module failing:
the true law carries an additive O(1) piece (the stretching and dilation terms, which do not scale
with `a`), so `||R||/|a|` approaches `k` from above with a 1/|a| tail, exactly as measured above.
The replacement criterion — agreement with an independent reassembly of the documented formula — is
strictly **stronger**, not weaker: it checks all 401 nodes against the formula rather than one
scalar against an asymptote, and it applies to every family in the battery. Both the original
criterion and the reason for replacing it are recorded in the runner's docstring.

## Two caveats found, neither one the gated question

**1. `gauge_c_tw` returns a finite `0.0` on a NaN-poisoned profile.** The three
`if denom > 0 else 0.0` guards (`gclm_family.py:190/204/233`) compare `False` on a NaN denominator,
so a profile with one NaN node yields a clean-looking gauge speed of exactly 0.0. This did not
decide the gate: profile poisoning is not the gated input class (the gate asks about
*coefficients*), and the residual accompanying that gauge is still **100%** non-finite, so no
consumer of the residual receives a plausible-looking value. Pinned in the regression test.

**2. `residual_two_scale_relnorm` loses its advertised scale-invariance below |Ω| ~ 1e-15.**
Out of the gate's scope (amplitude domain, not coefficient domain), reported separately. The
docstring claims the normalization by `||Ω H Ω||` "makes the fitness invariant under the family's
scaling symmetry" specifically so a GA cannot "CHEAT by shrinking the amplitude to zero (trivial
null)". The `max(scale, 1e-30)` floor on line 236 breaks that: once the RMS of `Ω·H(Ω)` falls below
1e-30 the denominator stops tracking ε² while the numerator keeps falling, so `relnorm ~ ε² → 0`.
Measured: invariance is exact to ε=1e-14; at **ε=1e-15** the ratio to the reference is
**1.179e-01**; by **ε=1e-78** it returns **exactly 0.0** — a perfect "exact traveling wave" score
from a garbage amplitude, which is precisely the cheat the normalization was introduced to prevent.

**Severity: latent, not active.** The GA's realized genome amplitudes are O(1), many decades above
the break. No GA run was performed to check drift — that would be a gCLM measurement, which this
leg is banned from. Flagged for the orchestrator as a bounded observation, not patched (this leg
edits nothing).

## Test is not vacuous

Mutation-checked by injecting the two canonical corruptions into `GCLMResidual.residual` in memory:
a `nan_to_num` swallow on the way out is caught by 2 of the tests; clipping `a` into [0,1] is caught
by 3. Plus a live anchor check, so the suite cannot pass by the anchors having gone dead.

