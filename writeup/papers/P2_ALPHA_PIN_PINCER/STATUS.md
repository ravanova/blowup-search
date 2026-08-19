# P2 — The α-pin × ṁ pincer. STATUS.

**Updated 2026-08-19 by `P2-DRAFT` (leg 415, wave 9).** The previous version is superseded, not
deleted: everything it said is either carried forward below or explicitly marked as discharged.
Per `writeup/papers/README.md`, **this file is written before `DRAFT.md`** so the draft cannot
route around its blockers.

**A PAPER IS A VIEW OF THE RECORD, NEVER A SOURCE. No unit may cite `DRAFT.md`.**

---

## The claim, as the record actually supports it

For a nontrivial backward `λ`-DSS blow-up profile of 3D Navier–Stokes the far-field decay exponent
is pinned to exactly `α = 1`. After cut-off of a **synthetic exactly-DSS realization**, of the five
localisation error terms generated, `T₁ + T₂` cancel, `T₄` and `T₅` decay like `ρ^{-2}`, and the
survivor is the **modulation commutator `T₃ ∝ ṁ`**, whose scale-invariant size is `ρ^{1-α}`. It
vanishes only at `α > 1` — which the pin forbids — or at `ṁ = 0` — which **Tsai 1998 Theorem 2**
forbids.

## THE CONTRIBUTION CEILING — user directive, verbatim, may not be exceeded anywhere in the draft

> **"the identification of `T₃` as the sole survivor and its `ṁ`-proportionality, in float64, on a
> synthetic profile."**

Nothing in the abstract, introduction or conclusion may be written as larger than that sentence.

## What is banked for it

| evidence | artefact / field | note |
|---|---|---|
| **The pin, `α ≥ 1`** | `SOURCES.md` row 1 — Chae–Wolf `arXiv:1610.09464` Thm 1.1, **FULL TEXT**, sha256 `1f537bc2…` | primary, hashed, re-confirmed by `PB2` |
| **The pin, `α ≤ 1`** | `p2_route_l2_decay_v2.json` correction `D6` | **weaker than the v1 wording said.** Runs through Chae–Wolf Rmk 1.2, *one unproved sentence with no hypotheses stated*, terminating at **ESŠ, `UNREACHABLE` at primary**. Reachable at primary **only** in Seregin's local suitable-weak form, `arXiv:math/0510396` §1 (`SOURCES.md` row 4, FULL TEXT). Pineau–Vicol are **independent authors, not an independent proof** |
| **The survivor** | `p2_route_l5_finite_energy_v1.json` `sweep["alpha=1\|kappa=a_physical_frozen\|DSS"]` | `T12_over_T1_at_largest_rho = 2.5780635399678998e-08`; `total_over_T3_at_largest_rho = 0.9999978617027289`; `T4_L3_rho_exponent_tail3 = -2.000005376382061`, `T5 = -2.0000138353404697` |
| **`T₃ ∝ ṁ`** | same file, `controls.C3p_modulation_amplitude_linearity` | `curl_over_amp_ratios` constant to `linear_in_amplitude_rel_spread = 1.424108612445009e-04`; `value_at_amp_zero = 0.5505448978148512` |
| **The endpoint** | same file, `gate.rho_exponent = 1.0850007559945518e-04` out to `gate.largest_cutoff_radius_in_y_tested = 1261.7173441261198` | summability needs strictly negative; `α = 1` delivers exactly `0` |
| **Falsifier did not fire** | same file, `controls.C7_modulation_absorption_falsifier` | optimal `(δa, δκ)` over all `ℝ³` left `fraction_remaining = 1.0009067172080548` — slightly **worse** |
| **Second jaw at primary** | `p2_route_pb2_v1.json`, `SOURCES.md` rows 33–35 | Tsai Thm 2's hypothesis `(1.4)` met by measurement; NRŠ's `L³` hypothesis **not** met |
| **Verification** | `p2_verify_wave5_v1.json` (`V-W5`, leg 403) | five items reproduce bit-for-bit; three discrepancies recorded, none repaired |

---

## BLOCKERS

### 1. ~~BOTH JAWS ARE JOURNAL-ONLY AND HAVE NEVER BEEN READ AT PRIMARY~~ — **DISCHARGED, and the answer changed the claim**

`PB2` (leg 410, gate **YES**, `p2_route_pb2_v1.json`) discharged §3k rule 2 — **and in doing so
moved which theorem carries the `ṁ ≡ 0` exit.**

- **W4 clause (b) is carried by Tsai 1998 (*ARMA* 143, 29–51) Theorem 2**, whose hypotheses are the
  Navier–Stokes equations in the sense of distributions plus the local energy estimates `(1.4)` in
  one cylinder `Q₁(0,T)`, for a `u` of the form `(1.2)₁`. **No `L^q`. No Leray–Hopf. No boundary
  condition.** `(1.4)` is met by measurement (`M5`).
- **Nečas–Růžička–Šverák (*Acta Math.* 176 (1996) 283–294) does NOT apply.** Its hypothesis is
  `U ∈ L³(ℝ³)` exactly, and at the pinned `α = 1` the object's `∫|U|³` is **log-divergent**
  (`M3`: `U_in_L3_R3 = false`, coefficient `60.49165798396497` measured against
  `60.49165798397186` closed-form, rel `1.1393743809599626e-13`).
- **The repository cited the wrong journal, volume and pages in FIVE places** including the
  generator (`CORRECTIONS.md` §47 / §47b). This goes in the paper.
- NRŠ remains `UNREACHABLE` at primary after four independent attempts (legs 253, 359, 364, 410).
  **The one source that cannot be obtained is the one that does not carry the case.**

### 2. THE NUMERICS ARE ON A SYNTHETIC PROFILE — **STANDS, unchanged**

Leg 381's synthetic exactly-DSS, exactly-divergence-free poloidal field, **not** route 4's own
object (`CORRECTIONS.md` §34). Route 4 has **no banked continuous profile**
(`p2_route_l5_finite_energy_v1.json` `realization_lesson_91.route_4_has_no_banked_profile = true`,
evidence `leg_382.md:174`, `leg_397.md §1`). The exponent is a property of the ansatz class; the
constant `c_mod` is a property of that realization and **is not route 4's number**
(`under_resourced_with_a_cost.what_is_missing`).

### 3. `C6` DID NOT FIRE AS PLANTED, AND THE CRITERION THAT PASSED WAS ADDED POST-HOC — **STANDS**

`p2_route_l5_finite_energy_v1.json` `controls.C6_basis.fired_as_planted = false`
(`exponent_disagreement_curl = 0.020345978295982933` against `precommitted_tolerance = 0.01`).
`fired_on_tail3_fit = true` — and `V-W5` located that this **second** pass-criterion was added at
the landing commit `4be46ef`, i.e. after the failure on the pre-committed criterion was known
(`p2_verify_wave5_v1.json` `DISCREPANCY_D_V_W5_1`). The tolerance itself was **never moved** —
three diff lines, all additions, literal `1e-2` in every one. The same control measures a
`constant_ratio_curl_C4_over_C2quintic = 1.476038407975093` basis spread in `c_mod`.
**This is disclosed in the paper, not only here.**

### 4. NOVELTY IS UNASSESSED — **STANDS, AND IT IS NOW THE LARGEST OPEN BLOCKER**

`P1`'s owed novelty check was run (`PB1`, leg 411) and **killed `P1`**. `P2`'s equivalent has
**never been run**. Nobody has checked whether the assembly — cut-off of a DSS profile, term-by-term
identification of the localisation error, and the observation that the survivor is `∝ ṁ` — is in
print. **Until it is run, the paper's related-work section is an assertion.**
The `P1` precedent is the reason this is ranked first among the survivors: **a `YES` kills the paper
and is the cheapest possible result.**

### 5. **NEW** — `c_mod = 869.288` IS UNDER AN OPEN §53 FLAG

`CORRECTIONS.md` §53: `L5`'s cutoff sweep stops at `ρ ≈ 1.26e3` and its last two per-decade
increments are **POSITIVE** (`+0.403874`, `+0.051881` — re-derived here from
`sweep["alpha=1|kappa=a_physical_frozen|DSS"].rows`). A power-law fit cannot distinguish saturation
from `log ρ` growth; both give exponent ≈ 0. `L5-cmod` (leg 413, this wave, pre-registered at
`91b8f17`) extends the sweep to `ρ = 1e8` and is the unit that discharges it.
**`L5-cmod` had NOT returned when this draft was written.** Both outcomes are stated in the draft.
**Direction saves the answer either way:** if `c_mod` diverges it *grows*, and `L5`'s `NO` was
because the error is too *large*.

### 6. **NEW** — EVERY ROUTE-4 `ρ` IS A VALUE OF A TRUNCATION OF A DIVERGENT INTEGRAL

`CORRECTIONS.md` §52 / `p2_route_ljver_v1.json` `divergence_diagnosis`. `L6`'s reach is banked at
`r_min = 5.502168747104923e-4`, `r_max = 7269.860638324989`, `nq_r = 72`. **A `ρ` printed without
its reach is a false statement in this paper.** Neither program is miscoded: `X9_operator_vs_rule`
reproduces `J_L6` at `1.1007215739872338e-14` … `1.8636918650427355e-14` on `L6`'s own nodes and
weights, *including at `P3` where the gate fails by 43%*.

### 7. **NEW** — `L6`'s REFINEMENT LADDER HAS NEVER BEEN MEASURED AT AN ADEQUATE BUDGET

`CORRECTIONS.md` §51. `L6`'s four-rung ladder moved `ρ` by `−4.994561%` with **every rung stopped
at 800 iterations**; `L6-b`'s single `×25` budget step at fixed `n_dof` moved it `−6.751678%`.
**One budget step moved the objective `×1.3518` of the entire refinement ladder.** The ladder can
also invert on a margin of `0.4636` percentage points. `L6-e` v2 is the measurement; it is **HELD
FOR CORES** and has not run. **The paper may not write `L6`'s ladder as evidence about refinement.**

---

## What it owes

1. **The novelty check** (blocker 4) — its own unit, on the `P1` model, before submission is
   contemplated.
2. **`L5-cmod`'s answer** (blocker 5) folded into §5 of the draft.
3. **`L6-e` v2's answer** (blocker 7) folded into §6 of the draft.
4. A decision — **not this unit's** — on whether a paper whose two central numbers are values of
   truncations should be written at all, or whether the honest object is a shorter note about the
   *exponent*, which is truncation-free, plus a `CORRECTIONS`-style methodological piece.
   `FINDINGS.md` **F9** puts this to the Conductor.

## What it must NOT claim, written here so the draft cannot drift

- Not that a blow-up profile exists or does not exist.
- Not that any `L1 → L4` link moved. **Clay stays ~0.05%.**
- Not that `L6`'s residual is an infimum, a bound, a certificate, or a statement about any
  `n_dof` other than `6720`.
- Not that NRŠ excludes the object. **It does not.**
- Not that the `α ≤ 1` direction was read at primary. **It was not, and it cannot be from here.**
