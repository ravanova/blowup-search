# Leg 439 — AMENDMENT to `leg_439_prereg.md`, BEFORE ANY K3 RUN: **Q6 is DROPPED by the rule; Q1–Q5 unchanged**

**Date:** 2026-09-10, 13:40Z, the laptop Conductor. **Deviation class:** a pre-registration amended before the run
it governs, on a derivation checked against the banked record — the §70 precedent — not a widening. No K3 worker
has been spawned; no K3 number exists. `CORRECTIONS.md` §75.

## What is wrong with Q6 as pre-registered
§0 of the prereg derives the flat weight's slope `k(δ) := δ³ ∂_δ log T_{0,θ}` as `8 − 3δ + O(δ³)` from
`log T_{0,θ} = −4/δ² − 3 log δ + log b + O(δ)`, and Q6 gates the "linear coefficient" `c₁ = (k − 8)/δ` on `−3 ± 0.05`.
Two errors, either fatal:
1. **The algebra.** `δ³ ∂_δ(−3 log δ) = −3δ²`, not `−3δ`. On the prereg's own expansion `k = 8 − 3δ² + O(δ³)`; the
   quantity it gates, `(k − 8)/δ`, would be `−3δ → −0.06, −0.03` at `δ = 0.02, 0.01`, never `−3`.
2. **The expansion is not reached at any resolvable `δ`.** Leg 432 measured it: `writeup/data/arc6_residual_v1.json`
   `preregistered_runs/1e-07/H2/local_power_Ttheta_hat_at_0.05 = 0.051` (**`δ⁰`**, not `δ⁻³`), with
   `H2/not_testable` = *"T_hat δ³ → b_θ(0,η) needs δ < δ_cross"* and `H2/delta_cross = 1.1·10⁻⁶⁹`; and
   `H7/delta3_dlogT_ddelta_at_0.05 = 8.000135`, i.e. `(k − 8)/δ = 0.0027` where Q6 predicts `−3`. The `−3 log δ`
   term Q6 rests on is the `δ → 0` limit on a collar no grid reaches (`leg_432.md` §1, H2 "NOT TESTABLE").

## Why DROPPED rather than re-scaled
With the `−3` gone, route A's only surviving prediction at resolvable `δ` is `k → 8`, which is the exponent of the
cutoff `e^{−4/δ²}` itself — a quantity the adversary chooses (a bare cutoff with no profile at all returns `k = 8`
exactly). That is the tautology the prereg already dropped S2's support clauses for. The rule of the wave is
*evidence is a two-route agreement on a quantity the adversary cannot choose; a gate that cannot be put in that
form is DROPPED, not weakened.* A `δ³`-coefficient gate would be a re-scaling after the number (H7's `0.000135`),
which is exactly what §71 forbids. **Q6 is dropped. Slot 4 runs Q5 only.** The flat weight's exact zeros beyond
`X_b` remain covered by Q5's heat/no-heat contrast, which is profile-derived (`ℬ = −(2 + 2h)`, `K6_no_heat/H7/
B_beyond_Xb = −2.002` at `h = 10⁻³`).

## The other scales, checked against the record before this push (unchanged)
Q2 `2h`: measured real in wave 4 (`leg_433.md`: `2.0096·10⁻⁷`), gated here relative at two `h`. Q3 `h/10` as a
`q`-exponent: §71's diagnosis, run here at `h ∈ {10⁻¹, 3·10⁻², 10⁻²}` where it is resolvable, `NOT-INSTANTIATED →
DROPPED` allowed. Q4 `−(3/2 + h)`: wave 4 V2 measured `−1.5000001` at `h = 10⁻⁷`. Q5 `−(2 + 2h)`: leg 432 K6.
Q1 is an exact identity (7.26) at oversampling independent of `N`. **Nothing else in the prereg is amended.** Slot 5,
the adversary, is told Q6 is dropped and why, and nothing else.
