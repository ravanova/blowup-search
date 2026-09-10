# Leg 439 — unit `K3`, arc 7: WAVE 4 REDUX — PRE-REGISTRATION, pushed BEFORE any run

**Date:** 2026-09-10. **The Conductor's.** **FAN-OUT ×5**: four workers + the adversary (slot 5). **Charter
(user, 2026-09-10, item K3; `CORRECTIONS.md` §72):** rebuild wave 4's four numerical gates on ONE rule and
only that rule — ***evidence is a two-route agreement on a quantity the adversary cannot choose*** — the rule
wave 4's own adversary named (`leg_433.md` §3, `agent_7_adversary.json` X2) and leg 432 satisfied. **A gate
that cannot be put in two-route form is DROPPED, not weakened.** Composition floor: this is the `W4` unit.
**Every unit is Tier 2: nothing here is a proof and nothing here verifies the theorem.**

## 0. The scale check, done BEFORE the gates were fixed (§71's lesson)
Wave 4 mis-scaled three of twelve gates against the paper's asymptotics. Each tolerance below was set
against the signal it must resolve, and the two derivations that changed a gate are recorded here:
- **The flat weight's local slope is `8 − 3δ`, not `8`.** With `k(δ) := δ³ ∂_δ log T_{0,θ}` and leg 432's
  H2 factorisation `T̂_θ δ³ → b_θ(0,η)` (`T̂ = e^{4/δ²}T_0`): `log T_{0,θ} = −4/δ² − 3 log δ + log b + O(δ)`, so
  `k = 8 − 3δ + O(δ³)`. A gate on `k → 8` alone cannot see the adversary's fake cutoff `e^{−4/δ²+0.2/δ}`
  (which shifts the linear coefficient from `−3` to `−3.2`); a gate on the linear coefficient can. Q6 below.
- **The `h`-signals.** `2h = 2·10⁻⁷` (Q2) and the stage gain `h/10 = 10⁻⁸` (Q3) are unresolvable as
  `q`-exponents at the paper's `h = 10⁻⁷` against any honest tolerance, so every `h`-gate is run at
  **two `h`** — the paper's `10⁻⁷` and a computable `10⁻³` (Q2, Q4, Q5) or `{10⁻¹, 3·10⁻², 10⁻²}` (Q3) — and the
  gate is on the **`h`-dependence**, which a constant or drifting fake cannot reproduce at both. Tolerances
  are stated **relative to the signal**, never absolute.
- **`−(3/2 + h)` vs `−3/2`** (Q4): the `h` is `10⁻⁷` at the paper's `h`; only `−3/2` is resolvable there;
  `−1.501` is resolvable at `h = 10⁻³`. The gate says which.

## 1. The pinned interface (unchanged from `leg_433_prereg.md` §0; on `main`)
The outer profile `writeup/data/arc6_profile_v1.json` (`λ = 0.1`, `h = 10⁻⁷`, `A = ½ + h`); the tail stress
`writeup/data/arc6_residual_v1.json` (`leg_432.md`: `T_{0,θ} = E_pow √(X/2)[𝒜/L + ℬ/X]`, `T_{0,z}` as there,
both exactly zero for `X ≥ X_b = e³X_tail` with the heat factor; flat weight `e^{−4/δ²}`, `δ = 3 − y`;
`T = q^{−A−½}T_0`). **Everything is computed in the scaled form `T̂ = e^{4/δ²}T_0` so nothing underflows.**
Runners to import, never edit: `experiments/arc6_profile_v1.py`, `experiments/arc6_residual_v1.py`, and
wave 4's `experiments/arc6_w4_{pulses,iteration,headline,support}.py` (their `tail_data`, `pinned_stress`,
`stress`, `profile_fields`, `force_profiles` are the pinned quantities' builders). `.venv/bin/python`.
Manuscript text `writeup/data/arc6/manuscript_pages.txt`; ledger `writeup/data/arc6/ledger.json`.

## 2. Ownership — ONE runner, ONE artefact, own worktree branch, nothing else
| slot | unit | runner | artefact | branch |
|---|---|---|---|---|
| 1 | Q1–Q2 pulses + hierarchy | `experiments/arc7_k3_pulses.py` | `writeup/data/arc7/k3/agent_1_pulses.json` | `leg/439-k3-agent1` |
| 2 | Q3 iteration | `experiments/arc7_k3_iteration.py` | `writeup/data/arc7/k3/agent_2_iteration.json` | `leg/439-k3-agent2` |
| 3 | Q4 leading-order force | `experiments/arc7_k3_force.py` | `writeup/data/arc7/k3/agent_3_force.json` | `leg/439-k3-agent3` |
| 4 | Q5–Q6 support + flat weight | `experiments/arc7_k3_support.py` | `writeup/data/arc7/k3/agent_4_support.json` | `leg/439-k3-agent4` |
| 5 | ADVERSARY, blind | `experiments/arc7_k3_adversary.py` | `writeup/data/arc7/k3/agent_5_adversary.json` | `leg/439-k3-agent5` |
Slot 5 never sees slots 1–4's files or methods; slots 1–4 never see slot 5's; no slot sees wave 4's
`agent_*.json` or `leg_433.md`. Every artefact: `schema: arc7_k3_v1`, `agent`, `leg: 439`, pages read, a
`claimed` block (page, equation, **the route-A prediction written before the run**), `routes` (A and B
each with its method), `gates` (`YES`/`NO` with numbers), `controls` (fired / did not fire), `dropped`
(gates the worker could not put in two-route form, with why), `instantiated_vs_scaled`,
`could_not_determine`, and the sentence **"This is Tier 2, not a proof."**

## 3. The gates — every one a two-route agreement; the quantity named; what the adversary cannot choose
### Q1 (slot 1) — the realised stress: closed form vs direct quadrature
**Quantity:** the pinned `T_0` (both entries) on `y ∈ [½, 2.9]`, every `η` node — fixed by leg 432, not by this unit.
**Route A:** Proposition 7.5 / identity (7.26): the paper's closed-form averaged product for pulses whose
amplitudes Definition 6.4 assigns from `T`. **Route B:** the same pulses, built explicitly, their quadratic
product averaged over one fast period by direct quadrature at oversampling `M ∈ {16, 64, 256}` points per
period, **independent of `N`** (aliasing is what faked P1). **Gate:** per entry (`θθ` and `z` SEPARATELY, each
normalised by its own sup — the joint norm hid `T_z`), relative error `< 10⁻⁸` at `M = 256`, decreasing with `M`
at the quadrature's order (log–log slope `≤ −3.5` for Simpson). **Controls:** one pulse phase-shifted `π/2` →
error `O(1)` at every `M` (must fail); amplitude halved → error `0.75 ± 0.01` (must fail); twin passes.
### Q2 (slot 1) — the viscous hierarchy exponent
**Quantity:** the `q`-exponent of the ratio (subleading over leading) in the paper's `q^{2h}` hierarchy on the
pinned annulus (Proposition 9.1's table, quote the page). **Route A:** the paper's exponent, `2h` exactly.
**Route B:** the ratio's log–log slope over `q ∈ {10⁻², 10⁻³, 10⁻⁴}`, at **`h = 10⁻⁷` AND `h = 10⁻³`**. **Gate:**
`|slope − 2h| / 2h < 0.05` at **both** `h`. (Wave 4's `±0.05` absolute admitted a constant ratio and a
`q^{0.04}` drift; here both fail at both `h`.) **Controls:** constant ratio → fails; ratio `× q^{0.04}` → fails
at both `h`; twin passes.
### Q3 (slot 2) — the per-stage gain as a function of `h`
**Quantity:** the exponent gain of ONE correction stage (§8–§9's linear mean-correction solve on the annulus,
sourced by the pinned residual), as a function of `h`. **Route A:** Propositions 9.5/9.6's gain, `h/10` in the
`q`-exponent, evaluated at `h ∈ {10⁻¹, 3·10⁻², 10⁻²}` → `{10⁻², 3·10⁻³, 10⁻³}`, written before the run.
**Route B:** the solve, with `h` entering ONLY through the profile and the operator's weights — **never as an
input gain** — residual exponent before and after over `q ∈ {10⁻², 10⁻⁴, 10⁻⁶}`. **Gate:** measured gain within
10% of route A at each `h`, and `gain/h ∈ [0.09, 0.11]` at all three. **Controls:** zero correction → gain
`≈ 0` (must fail); source negated → residual grows (must fail); twin passes. **If the stage's linear problem
cannot be instantiated in the budget (it was not in wave 4): the gate is `NOT-INSTANTIATED` and DROPPED,
with the cost of instantiating it stated (§3d). No exponent-ledger arithmetic is offered in its place.**
### Q4 (slot 3) — the leading-order force, physical space vs profile space
**Quantity:** `f⁽⁰⁾ := NS(u⁽⁰⁾)` for the pinned leading-order field (`(4.7)–(4.8)`, the paper's `q(t)`).
**Route A:** physical variables, the Navier–Stokes operator by finite differences in `(r, z)` at three
stencil spacings (halving), divergence-free residual reported. **Route B:** Proposition 4.2 in profile
variables, `R⁽⁰⁾ = −div(q^{−A−½}T_0)` plus the viscous and time terms as the paper writes them (page quoted),
from the pinned stress. **Gate:** pointwise relative agreement `< 10⁻⁶` on the annulus at `q ∈ {10⁻², 10⁻³,
10⁻⁴}`, on the finest stencil, with the stencil error extrapolating below `10⁻⁶`; and `sup|f⁽⁰⁾|`'s `q`-exponent
on BOTH routes `= −3/2` within `10⁻⁴` at `h = 10⁻⁷` and `= −(3/2 + 10⁻³)` within `10⁻⁴` at `h = 10⁻³`. **DROPPED,
by the rule:** V1 and V3 — the norm scalings and refinement stability of a prescribed field — because any
second route is the same Jacobian identity; the un-cut-off field's infinite `L²(ℝ³)` is recorded as a known
fact, not re-gated. **Controls:** `A → A + 0.1` moves the exponent by `−0.1` on both routes (must move); drop
the `T_z` entry in route B → `z`-component mismatch `> 10⁻²` (must fail); twin passes.
### Q5 (slot 4) — `ℬ`'s exact zero with the heat factor against `−(2 + 2h)` without
**Quantity:** the bracket `ℬ` of `T_{0,θ}` beyond `X_b`. **Route A:** Lemma A.8: `ℬ ≡ 0` with the heat exterior,
`ℬ = −(2 + 2h)` exactly without it (leg 432's K6). **Route B:** numerical, from the pinned fields, at
`h ∈ {10⁻⁷, 10⁻³}`. **Gate:** with heat `|ℬ| < 10⁻¹⁴` (scaled); without heat `|ℬ + 2 + 2h| < 10⁻⁸` at both `h` —
a fake returning `−2` fails at `10⁻³` by `2·10⁻³` and at `10⁻⁷` by `2·10⁻⁷ > 10⁻⁸`. **Controls — the adversary's
own two fakes, planted:** truncate to the `√X` term; cut off the stress instead of the profile: each gives
`0` in BOTH legs and so must fail the no-heat leg; twin passes.
### Q6 (slot 4) — the flat weight's linear coefficient
**Quantity:** `k(δ) = δ³ ∂_δ log T_{0,θ}` at `δ ∈ {0.05, 0.02, 0.01}`. **Route A:** `k = 8 − 3δ + O(δ³)` (§0
above; the `−3` is leg 432's H2 factorisation, (A.48)). **Route B:** numerical `k(δ)` by centred differences on
the pinned stress, spacing halved twice to show convergence. **Gate:** `c₁ := (k(δ) − 8)/δ` at `δ = 0.02` and
`0.01` within `±0.05` of `−3`, and `|k − 8 + 3δ| ≤ C δ³` with `C` derived in `claimed`. The fake cutoff
`e^{−4/δ²+0.2/δ}` gives `c₁ = −3.2` and fails. **DROPPED, by the rule:** S2's support clauses (tautologies of
the cutoffs; the flatness clause is the corrections' and is the gap Q4 reports). **Controls:** the fake cutoff
(must fail); polynomial cutoff `(δ/2)⁴` → `k → 0` (must fail); twin passes.
### Slot 5 — the ADVERSARY, blind
Given **only §3's gate definitions**: for each of Q1–Q6, try to produce `YES` from a deliberately wrong or
under-resolved run — aliasing, a built-in gain, a wrong profile, a cutoff on the wrong object, a
single-`h` run. **X1:** per gate `FAKEABLE` / `NOT FAKEABLE` / `NOT ATTEMPTED`, with the faking run's numbers.
**X2:** the verdict sentence. It states honestly when it could not fake a signal. **Standing rule, applied at
integration whatever a worker's gate said: a signal the adversary can fake is NOT EVIDENCE.**

## 4. Resourcing (§3d) and what the wave does not establish
Each worker: one session, `.venv/bin/python`, 4 cores shared, no run longer than the session; a gate not
reached at that resourcing answers `UNDER-RESOURCED` with a cost, never `NO`. **Every gate is a check that
the paper's algebra is realised numerically on a pinned object at computable parameters; none is evidence
that the construction closes at the paper's `λ`, `h`, none moves `W4`, none is a proof.** Instantiated at
computable `λ = 0.1`; scaled toward the paper's regime in `h` and `q`.

## 5. What the Conductor does at integration (pre-committed)
Cherry-pick the ten files unedited; `experiments/arc7_k3_merge.py` → `k3/merged.json`; the gate table Q1–Q6
with each number; X1 row by row; `DROPPED` gates listed with the reason; every worker/adversary disagreement
recorded, not adjudicated; a faked signal marked `NOT EVIDENCE` in `STATE.md`. Then `K4`.
