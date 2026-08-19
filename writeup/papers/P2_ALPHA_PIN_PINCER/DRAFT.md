# The far-field pin and the modulation commutator: what survives when a discretely self-similar Navier–Stokes blow-up profile is cut off

**DRAFT — `writeup/papers/P2_ALPHA_PIN_PINCER/DRAFT.md`. Unit `P2-DRAFT`, leg 415, wave 9.**

> **A PAPER IS A VIEW OF THE RECORD, NEVER A SOURCE.** Every number below cites the banked JSON
> field it came from. **No unit may cite this draft.** It is downstream of everything and
> load-bearing for nothing.

---

## Abstract

A backward discretely self-similar (DSS) blow-up profile of the three-dimensional Navier–Stokes
equations has infinite global energy, while the Clay problem's condition (7) demands bounded
energy. One of the two standard ways to reconcile them is to build a **natively finite-energy**
modulated, localised ansatz: cut the profile off at radius `ρ`, let the modulation amplitudes
`m(s)` move, and ask whether the error this introduces can be made small.

We report a float64 computation, on a **synthetic exactly-DSS realization**, of every error term
that cut-off and modulation generate. **The term-by-term decomposition exists in the record only in
the `L¹_t L³_x` norm, which the gate designates *secondary*; the pressure-free load-bearing norm
`‖curl F‖_{L¹_t L^{3/2}_x}` is banked only as a total. Every ratio in this abstract is a
secondary-norm ratio and we say so wherever it appears.** Five terms are generated. The cut-off drift `T₁` and the
modulation transport `T₂` **cancel** when the cut-off radius is frozen to the similarity rate
(`κ = a`), measured `|T₁+T₂|/|T₁| = 2.5780635399678998e-08`. The viscous and nonlinear commutators
`T₄`, `T₅` **decay** like `ρ^{-2}` (measured exponents `-2.000005376382061` and
`-2.0000138353404697`). The pressure term is annihilated by the curl and the divergence corrector
is identically zero for this ansatz. **What is left is the modulation commutator `T₃`**, and it
carries `0.9999978617027289` of the total residual at the largest radius tested — in the secondary
norm, the ratio rising monotonically toward `1` across the sweep (`1.0286, 0.99828, 0.99979,
0.999976, 0.9999979`).

`T₃` is algebraically proportional to `ṁ` and its scale-invariant size is `ρ^{1-α}`. It therefore
vanishes only if `α > 1` or `ṁ = 0`. **Chae–Wolf's Remark 1.2, via Escauriaza–Seregin–Šverák,
forbids the first** — a DSS solution with an `L³` profile is fully regular, so there is no
singularity to localise. **Tsai's 1998 Theorem 2 forbids the second** — an exactly self-similar
weak solution satisfying the local energy estimates is identically zero. The route closes at an
**endpoint**, not by a margin: summability of the localisation error over the infinitely many DSS
periods a backward-DSS blow-up requires needs a strictly negative `ρ`-exponent, and the pinned
`α = 1` delivers exactly zero (measured `1.0850007559945518e-04`).

**We claim nothing beyond this**, and §1 states the boundary explicitly. In particular we prove no
theorem, we do not construct a blow-up profile, and the constant `c_mod` attached to the endpoint is
under an **open divergence flag** disclosed in §5.

---

## §1. THE CONTRIBUTION, AND ITS CEILING

This section exists so that a reader meets the boundary before any result.

> **THE CONTRIBUTION OF THIS PAPER IS:**
> **the identification of `T₃` as the sole survivor and its `ṁ`-proportionality, in float64, on a
> synthetic profile.**
>
> **Nothing in this paper is written as larger than that sentence.**

Everything else here is either (i) a restatement of published theorems, cited and not reproved, or
(ii) a caveat. Specifically, **this paper does not claim**:

- that a backward DSS blow-up profile of 3D Navier–Stokes exists, or does not exist;
- any certified bound. Every number is **float64**. There is no interval arithmetic anywhere in it;
- anything about route 4's own object beyond what §6 states, since **no continuous profile for it
  exists in the record** (`p2_route_l5_finite_energy_v1.json`
  `realization_lesson_91.route_4_has_no_banked_profile = true`);
- that the modulation-amplitude linearity we measure is a proof of `T₃ ∝ ṁ`. The proportionality is
  **algebraic**, read off the ansatz; the measurement is a **consistency check on the apparatus**
  and is reported as such in §4.3.

**Tier.** Tier 2 throughout, in this programme's internal vocabulary: a measured quantity in
floating point, not a bound and not a certificate.

---

## §2. THE OBJECT, AND WHAT IT IS NOT

### 2.1 The ansatz

Write the similarity variables `y = x/λ(t)`, `ds/dt = λ^{-2}`, so that a backward `λ`-DSS blow-up
profile is a field `U(y,s)` periodic in `s` with period `T_s`. The cut-off ansatz is

    V(y,s) = χ(r/ρ(s)) · U(y,s),      ρ(s) = R_phys(t) · e^{(κ−a)s},

with `χ` a smoothstep transition profile and `a > 0` the similarity rate. The profile system is

    V_s + a(V + y·∇V) − ΔV + V·∇V + ∇P = 0,   div V = 0

(`p2_route_l5_finite_energy_v1.json` `ansatz.profile_system`). The residual `R_loc` is the
commutator `R[V] − χ R[U]`, and the load-bearing norm is the **pressure-free**

    ‖curl F‖_{L¹_t L^{3/2}_x} = ∫ ‖curl_y R_loc(·,s)‖_{L^{3/2}_y} ds

(`gate.norm`), with `‖F‖_{L¹_t L³_x}` as a secondary (`gate.secondary_norm`).

### 2.2 The realization, stated at the top because it bounds everything

The field `U` used is **leg 381's synthetic exactly-DSS, exactly-divergence-free poloidal field**

    U = m₁(s) P[ψ_α](·; e_z) + m₂(s) P[ψ_α](·; e_x),   ψ_α(r) = (1+r²)^{(2−α)/2},
    P[f](y;e) = curl curl (f(|y|) e)

(`realization_lesson_91.profile_used`), at `λ = 1.7`, DSS period
`1.0612565021243408` in `s` (`bill_from_artefact.period_in_s`), DSS symmetry verified to
`dss_symmetry_max_rel_error = 1.1380795944685018e-15`.

> **THIS IS NOT ROUTE 4's OWN OBJECT AND IT IS NOT A SOLUTION.** It is an exactly-DSS field chosen
> so that the commutator `R[V] − χR[U]` is well defined and its scaling in `ρ` can be read off. The
> record's own statement of why this is nevertheless a measurement:
> *"the measured quantity is the COMMUTATOR `R[V] − χ R[U]`, a well defined field […]; it depends on
> the profile only through `(α`, angular structure, modulation amplitude`)`"*
> (`realization_lesson_91.why_this_is_still_a_measurement`).
> **Consequence, stated once and honoured everywhere below: the `ρ`-EXPONENTS are properties of the
> ansatz class; the CONSTANTS are properties of this realization.**

### 2.3 Resolution

`n_theta = 16`, `n_phi = 32`, `n_panel = 6`, `n_gl = 14`, six `s`-nodes per DSS period
(`realization_lesson_91.resolution`, `.n_s_per_period`); product Gauss–Legendre with
geometric/linear radial panels; degree-9 `C⁴` smoothstep basis.

---

## §3. THE PIN: `α = 1` EXACTLY, AND EXACTLY HOW WELL IT IS SOURCED

The far-field decay exponent `α` is defined by `|U(y)| ~ |y|^{-α}` as `|y| → ∞`.

### 3.1 `α ≥ 1`

**Chae–Wolf, `arXiv:1610.09464`, Theorem 1.1**, read at **FULL TEXT** here (`SOURCES.md` row 1,
sha256 `1f537bc2…`, pdf md5 `f1d14db17f643323cfa1a16ba661eb9d`), quoted verbatim in
`p2_route_l2_decay_v1.json` technique `T2a`:

> "For `3 ≤ p < +∞` let `u ∈ C((−∞,0); L^p(ℝ³)) ∩ C^∞(Q)` be a solution to the Navier-Stokes
> equations, and `λ`-DSS for some `λ ∈ (1,+∞)`. Then the solution `u` is regular on `Q \ {(0,0)}`,
> and satisfies the estimate `(1.3) |u(x,t)| ≤ C/(√(−t) + |x|)`."

`(1.3)` evaluated at `t → 0⁻` is decay at least `|y|^{-1}`, i.e. `α ≥ 1`. The census records the
decisive hypothesis and records the object satisfying it: `T2a.this_object_status = "SATISFIED"` —
**the only one of eighteen techniques whose decisive hypothesis this object meets.**

**A gap in this step that we disclose rather than paper over.** The hypothesis check in the record
is performed **at `α = 1`** (`T2a.why_for_this_object`: *"At alpha = 1 the profile is in `L^p(ℝ³)`
for every `p > 3`"*), i.e. at the value the theorem is being used to establish. The step is
repairable — for any `α > 0` the far-field integral `∫ r^{-αp} r² dr` converges at infinity for any
finite `p > 3/α`, so some admissible `p` exists — but **that sentence is not in the record**, and a
referee is entitled to ask for it. It is logged as `FINDINGS.md` **F5**.

### 3.2 `α ≤ 1` — and this direction is weaker than the record's earlier wording said

**Chae–Wolf Remark 1.2**, same document, verbatim (`T2c.decisive_hypothesis_quote`):

> "If `u ∈ C((−∞,0); L³(ℝ³))`, and discretely self-similar, then `u ∈ L^∞(−∞,0; L³(ℝ³))`. Thus, in
> case `p = 3`, by using the result in `[5]`, we get the full regularity `u` in `Q`."

`U ∈ L³(ℝ³)` is exactly `α > 1`. So `α > 1` ⟹ full regularity ⟹ **no singularity to localise**.

**The honest provenance, taken from the correction record `p2_route_l2_decay_v2.json` `D6`, which
withdrew the word "independently" from an earlier version of this sentence:**

- Remark 1.2 is **one unproved sentence with no hypotheses stated** (`D6.now`), and `[5]` is
  Escauriaza–Seregin–Šverák.
- The ESŠ Navier–Stokes criterion (*Russian Math. Surveys* **58** (2003) 211–250) is
  **`UNREACHABLE` at primary from this work** and is banked as `UNREACHABLE`, **never as a zero**
  (`SOURCES.md` row 5; `D5.primary_reachability_of_both_ESS_papers`).
- The `≤ 1` direction is reachable at primary **only** in the **local suitable-weak-solution** form,
  Seregin `arXiv:math/0510396` §1, read at FULL TEXT by an ESŠ author (`SOURCES.md` row 4). This
  matters and is not a technicality: **the object's global energy is measured infinite**
  (`∫_{|y|<10²}|U|² = 1153.09`, `10⁴ → 125445.0`, `10⁶ → 12566000.0`, `10⁸ → 1256640000.0`, linear
  in the cut-off radius — `D5.…why_this_matters_and_not_a_technicality`), **so the object is not a
  Leray–Hopf solution and the global form of ESŠ does not apply to it.**
- **Pineau–Vicol (`arXiv:2607.09619`) §1.2 are INDEPENDENT AUTHORS, NOT AN INDEPENDENT PROOF**: they
  state the implication for *rotated globally self-similar* solutions, not for DSS, and their route
  also terminates at ESŠ (`D6.what_was_removed_and_why`: *"Two secondaries citing the same
  unreachable primary are one line of evidence, not two."*).
- Extending Pineau–Vicol's sentence from rotated-globally-self-similar to DSS is immediate, but
  **that step is this programme's, not theirs, and is not in their bytes**
  (`D6.the_step_that_is_the_verifiers_not_Pineau_Vicols`).

> **We therefore state the `≤ 1` jaw at the strength the record actually holds: it rests on one
> unproved remark in a secondary, terminating at a primary this work could not obtain, plus one
> reachable restatement by an author of that primary in a local form the object does satisfy.**
> The `≥ 1` jaw is at primary and hashed. **The two jaws are not equally sourced and we do not
> present them as if they were.**

### 3.3 What the pin costs the localisation route

Leg 381's cut-off bill for clause (a) of the same wall demanded `α > 1.5`; the pin gives `α = 1`,
deficit `0.5` in the exponent. **Any `α` paying that bill satisfies Remark 1.2's hypothesis, whose
conclusion is full regularity** — `T2c.why_for_this_object`: *"Paying the bill destroys the object
the bill is for."* Eighteen localisation / far-field-decay techniques were read against this object
and **none could supply `α > 1.5` even in principle** (`p2_route_l2_decay_v1.json` `techniques`:
9 `FAILS`, 8 `FAILS-BY-CONSTRUCTION`, 1 `SATISFIED`).

---

## §4. THE MEASUREMENT: FIVE TERMS IN, ONE TERM OUT

> ### **BEFORE ANY NUMBER: WHICH NORM THE DECOMPOSITION IS IN, WHICH IS NOT THE LOAD-BEARING ONE**
>
> The gate names two norms (`gate.norm`, `gate.secondary_norm`):
> the **load-bearing** `‖curl F‖_{L¹_t L^{3/2}_x}`, which is pressure-free because `curl` annihilates
> `∇P`; and the **secondary** `‖F‖_{L¹_t L³_x}`.
>
> **Every per-term field banked in the record is a secondary-norm field.** The artefact's keys are
> `T1_L3…`, `T2_L3…`, …, `T5_L3…`, `T12_L3…`, `T123_L3…`. **There is no per-term field in the
> load-bearing norm anywhere in the artefact.** The load-bearing norm appears only as the *total*,
> `curl_L32`.
>
> **Consequences, stated plainly rather than absorbed:**
> 1. The two headline ratios below — `|T₁+T₂|/|T₁| = 2.578e-08` and `total/|T₃| = 0.999998` — are
>    **secondary-norm ratios**. The gate's own `the_obstruction_named` field quotes both inside a
>    sentence about the load-bearing norm **without saying so**. We do not repeat that.
> 2. The pressure term `T₆` is annihilated only by the `curl`. In the secondary norm it is **not**
>    annihilated, and **it is not in the decomposition at all** — so the secondary-norm "total" is
>    not the sum of the terms listed, and no term-wise conclusion in that norm is closed.
> 3. **Therefore this paper's identification of `T₃` as the sole survivor is an identification IN
>    THE SECONDARY NORM.** That is *narrower* than the contribution ceiling permits, and it is the
>    version we assert. The measurement that would widen it — the same sweep, recording `‖curl Tᵢ‖`
>    per term — **has not been run**, and its absence is not evidence either way.
>
> The `NO` itself does **not** depend on the decomposition: it is read off `curl_L32` directly,
> which is measured. **What depends on the decomposition is this paper's sentence, not the wall.**

All numbers in this section are from `writeup/data/p2_route_l5_finite_energy_v1.json`, `self_hash`
`0c5e0f827f526df6`, load-bearing row `sweep["alpha=1|kappa=a_physical_frozen|DSS"]`, and were
reproduced bit-for-bit by an independent verifier (`p2_verify_wave5_v1.json`, `V-W5`, leg 403,
which **re-ran the float64 quadrature from `L5`'s own code and returned identical doubles**).

### 4.1 The terms cut-off and modulation generate

| term | what it is | predicted scale-invariant size |
|---|---|---|
| `T₁` | cut-off drift, `∂_s χ` part | `\|κ − a\| ρ^{1−α}` |
| `T₂` | modulation transport, `a[(V + y·∇V) − χ(U + y·∇U)]` | (cancels `T₁` at `κ = a`) |
| `T₃` | **modulation commutator**, `Σ_k ṁ_k (P[χψ] − χP[ψ])` | `\|ṁ\| ρ^{1−α}` |
| `T₄` | viscous commutator | `ρ^{−α−1}` |
| `T₅` | nonlinear commutator | `ρ^{−2α}` |
| `T₆` | pressure | annihilated by `curl` |
| `T₇` | divergence corrector | **identically zero** for this ansatz (potential cut-off) |

(`ansatz.terms_generated`, `ansatz.predicted_scale_invariant_sizes`.)

### 4.2 What is measured, at `α = 1`, `κ = a`, DSS

Radii `ρ ∈ {12.6171734412612, 37.851520323783596, 126.171734412612, 378.5152032378359,
1261.7173441261198}`, the last being `gate.largest_cutoff_radius_in_y_tested`.

**All rows below are in the SECONDARY `L³` norm** (see the box above).

| quantity | field | value |
|---|---|---|
| `\|T₁+T₂\| / \|T₁\|` at largest `ρ` | `T12_over_T1_at_largest_rho` | **`2.5780635399678998e-08`** |
| total `/ \|T₃\|` at largest `ρ` | `total_over_T3_at_largest_rho` | **`0.9999978617027289`** |
| `T₄` `ρ`-exponent (tail-3) | `T4_L3_rho_exponent_tail3` | `-2.000005376382061` |
| `T₅` `ρ`-exponent (tail-3) | `T5_L3_rho_exponent_tail3` | `-2.0000138353404697` |
| `T₁+T₂` `ρ`-exponent (tail-3) | `T12_L3_rho_exponent_tail3` | `-1.9999930154541286` |
| `T₃` `ρ`-exponent (tail-3) | `T3_L3_rho_exponent_tail3` | `-4.962567269511898e-06` |
| predicted leading exponent | `predicted_rho_exponent_leading` | `0.0` |

The "sole survivor" ratio is not a single-point measurement: across the five radii it reads
`1.0285935244169777, 0.9982831750453196, 0.9997915495946416, 0.9999763023011322,
0.9999978617027289` — approaching `1` from above and then from below, each step about an order of
magnitude closer, consistent with the `ρ^{-2}` leftovers.

Read across the row: at `κ = a` the cut-off drift and the modulation transport annihilate one
another to eight digits; the two commutators that do not involve the modulation fall like `ρ^{-2}`,
matching their predicted `ρ^{-α-1}` and `ρ^{-2α}` at `α = 1`; and **the modulation commutator does
not fall at all**, its exponent being zero to five decimal places, matching the predicted `ρ^{1-α}`
at `α = 1`. At the largest radius the total residual **is** `T₃` to one part in `4.7e5`.

> **That last row is the result of this paper.**

### 4.3 `T₃ ∝ ṁ`: what is algebra and what is measured

The proportionality is **algebraic**: `T₃ = Σ_k ṁ_k (P[χψ] − χP[ψ])` is linear in `ṁ` by
inspection of the ansatz (`ansatz.terms_generated.T3_modulation_commutator`). It is **exactly zero
iff the profile is exactly self-similar.**

The measurement (`controls.C3p_modulation_amplitude_linearity`) is a **consistency check on the
apparatus**, and we report it as one. Scaling the modulation amplitude by `0, 0.25, 0.5, 1, 2` gives
`‖curl F‖` of `0.5505448978148512, 217.28884822129643, 434.6122960485687, 869.2606943625965,
1738.5583753659312`, i.e. slope ratios constant to
`linear_in_amplitude_rel_spread = 1.424108612445009e-04`.

**Disclosure, because the artefact's own summary overstates it.** That artefact's `meaning` field
reads *"`c_mod` vanishes there"* at amplitude zero. **The measured value at amplitude zero is
`0.5505448978148512`, not zero** — `6.33e-04` of the amplitude-one value. This is consistent with
the non-modulation leftovers `T₄`, `T₅` at that finite `ρ₀` (they are `4.6e-04` of the total in the
secondary norm there) and it decays like `ρ^{-2}`, so it is not a contradiction. **But "vanishes" is
the wrong word for `0.55`, and we do not repeat it.** Logged as `FINDINGS.md` **F4**.

### 4.4 The falsifier that was planted, and did not fire

A modulated ansatz is allowed to spend its free parameters `(a, κ)` absorbing the residual.
`controls.C7_modulation_absorption_falsifier` performs the optimal `(δa, δκ)` absorption **projected
over all of `ℝ³`, core included**, so that absorption helping in the annulus is charged for what it
injects in the core. At `ρ₀ = 1000` the optimal `(δa, δκ) = (0.7481789545378188,
−0.7417515250807672)` leaves `fraction_remaining = 1.0009067172080548` — **the residual is very
slightly *worse* after optimal absorption**, and `flips_gate_to_YES = false`.

**A disclosure a referee would demand and the record does not supply.** `C7`'s baseline column
`L3_before` reads `50.74…, 61.50…, 62.83…, 62.95…, 62.96…` across `ρ₀ = 10 … 1000`, whereas the
gate's own `L3` at the same `ρ₀` reads `48.16…, 46.70…, 46.76…, 46.77…, 46.77…`. These are **not the
same numbers**, and the artefact states only that `C7`'s projection is *"taken over ALL of `ℝ³`,
core included"*, without stating the domain over which the sweep's `L3` is taken. **The two are
therefore not directly comparable and we do not compare them.** Logged as `FINDINGS.md` **F6**.

---

## §5. THE ENDPOINT — AND THE CONSTANT THAT SITS UNDER AN OPEN FLAG

### 5.1 The exponent, which is the part that travels

A backward-DSS blow-up requires **infinitely many** DSS periods. The localisation error summed over
`S` units of similarity time is `Σ(S) = c_mod · S` when the per-unit error is `ρ`-independent. The
measured `ρ`-exponent of the load-bearing norm is

    gate.rho_exponent = 1.0850007559945518e-04       (TAIL-3 window: rho0 = 100, 300, 1000 only)

**and the same quantity fitted over the full sweep is `curl_L32_rho_exponent =
-2.340048393964631e-02`, i.e. NEGATIVE.** The sign of the headline exponent is a property of the
fit window, and we print both because a referee is entitled to both. The gate's pre-committed
answer wording attaches the tail-3 value to the full range — *"measured `rho-exponent 0.000109`
over `rho0` in `[10, 1000]`"* — **which is the wrong range for that number**; the full range gives
`-0.0234`. The secondary norm behaves identically (`L3_rho_exponent = -4.913347365381298e-03` full,
`+8.350419121029962e-05` tail-3). What is *not* window-dependent, and is what the `NO` rests on, is
the raw sequence of per-decade increments in §5.3.

Against a requirement of **strictly negative** for summability
(`gate.the_clause_b_bill.required_rho_exponent_for_summability`). The pinned `α = 1` delivers
**exactly `0`**: `deficit_in_exponent = 0.0`, `measured_exponent_deviation_from_zero =
1.0850007559945518e-04`.

> **This is an ENDPOINT failure, not a gap.** The deficit in the exponent is zero, and it is still
> a failure, because summability needs strict negativity. Contrast clause (a)'s bill, where the
> deficit is `0.5` (`gate.the_clause_b_bill.the_bill`).

**The answer is threshold-free.** `gate.threshold_free = true`: because `c_mod > 0` and
`ρ`-independent already makes `Σ(S)` divergent, the answer is `NO` **for every `ε_close > 0`** and
no closure constant is needed (`gate.why_threshold_free`). For scale:
`gate.N_periods_affordable_by_threshold` gives `1.0839669489698014e-03` similarity-time units
affordable at `ε = 1`, and `1.0839669489698015e-09` at `ε = 1e-6`.

**The exponent, unlike the constant, is basis-robust:** both smoothstep bases give a tail-3 exponent
within `1e-3` of zero (`p2_verify_wave5_v1.json`
`does_anything_the_NO_rests_on_depend_on_the_constant_C6_perturbs.the_NO`).

### 5.2 The constant `c_mod`, at its truncation, under its flag

    gate.c_mod_per_unit_s              = 869.2878218404479
    gate.c_mod_per_DSS_period          = 922.5373531456809
    gate.c_mod_per_unit_s_velocity_norm= 46.76963450313766

**Every one of those is a value at a stated reach and in a stated basis, and must never be printed
bare.** Its qualifications, in full:

1. **Reach.** Measured at cut-off radii up to `ρ = 1261.7173441261198` and no further.
2. **Basis.** Degree-9 `C⁴` smoothstep. The quintic `C²` basis gives `578.0234164438871` at the same
   largest `ρ₀` — a ratio `constant_ratio_curl_C4_over_C2quintic = 1.476038407975093`
   (`controls.C6_basis`). **`c_mod` is basis-dependent by a factor of ~1.48.**
3. **Realization.** It is a property of leg 381's synthetic profile and **is not route 4's number**
   (`under_resourced_with_a_cost.what_is_missing`).
4. **AND IT IS UNDER AN OPEN DIVERGENCE FLAG.** See §5.3.

### 5.3 The open flag — stated, not resolved, and not written as a null

`CORRECTIONS.md` §53 observed that a power-law fit **cannot distinguish saturation from `log ρ`
growth**: both give exponent ≈ 0, and a logarithmic divergence is exactly the exponent-zero case.
Re-derived here from `sweep["alpha=1|kappa=a_physical_frozen|DSS"].rows`, the per-decade increments
of `c_mod` along the load-bearing row are

| `ρ` band | Δ`c_mod` per decade |
|---|---|
| `12.617 → 37.852` | `−263.078289` |
| `37.852 → 126.172` | `−1.721357` |
| `126.172 → 378.515` | **`+0.403874`** |
| `378.515 → 1261.717` | **`+0.051881`** |

**The last two increments are positive: `c_mod` is creeping upward where the sweep stops.** Two
positive points are not a floor, and we do not claim they are one. But the sweep ends at
`ρ ≈ 1.26e3`, and an independent sweep of a closely related route-4 functional shows increments
still decaying steeply through `r ≈ 1e6` and flattening to a nonzero floor only beyond it
(`p2_route_ljver_v1.json` `cutoff_sensitivity`; §6.2). **`L5`'s sweep is roughly three decades too
short to distinguish saturation from logarithmic divergence, and it was read as saturation.**

> **STATUS AT THE TIME OF WRITING.** The unit that discharges this — extending the same sweep, same
> apparatus, same norm, to `ρ = 1e8`, with the gate *"is the per-decade increment approaching a
> nonzero constant, YES or NO"* pre-committed at `WAVE9_PLAN.md` UNIT 1 and pre-registered at commit
> `91b8f17` — **HAD NOT RETURNED WHEN THIS DRAFT WAS WRITTEN.** This is an **open** item, not a null
> result.
>
> **Both outcomes have been written down in advance and neither changes the paper's answer:**
> - **YES (divergent)** ⟹ `869.288` is a value of `L5`'s cut-off, not of the functional. The
>   sentence *"the error per unit similarity time saturates at `c_mod = 869.288`"* is then **wrong
>   as stated** and must be replaced by *"grows without bound"*. **The conclusion is strengthened**,
>   because a growing error is further above any threshold.
> - **NO (saturating)** ⟹ the original reading was right and the constant stands at its reach.
>
> **The reason the answer is insensitive is the SIGN**, and it is the only reason. `L5`'s gate was
> `NO` because the error is too **large**; a divergence makes it **larger**. **A defect with a known
> sign can leave every conclusion standing while destroying every number, and both facts must be
> reported.**

---

## §6. ROUTE 4's OWN OBJECT — AND WHY ITS NUMBERS CANNOT BE QUOTED BARE

Everything above is on the synthetic realization. A separate line of work built a **discrete**
route-4 profile and minimised the same class of residual. We report it because a referee will ask,
and because **its two central defects are the most instructive part of this record.**

### 6.1 The construction and its residual, at its reach

`p2_route_l6_profile_v1.json` (`self_hash 6a033004deef39d3`), branch B, poloidal–toroidal trial
space, L-BFGS-B minimisation. The refinement ladder, `gate.B.per_rung_residual`, **each rung at a
different radial reach**:

| rung | `n_dof` | `nq_r` | `ρ` |
|---|---|---|---|
| `J0` | 384 | 36 | `3.646708645559305` |
| `J1` | 576 | 48 | `1.6986514108481086` |
| `J2` | 1800 | 48 | `1.6756137293407118` |
| `J3` | 2400 | 60 | `1.6218749783288575` |
| `J4` | 6720 | **72** | `1.613811231995397` |

`J4`'s reach is `r ∈ [5.502168747104923e-04, 7269.860638324989]`
(`p2_route_ljver_v1.json` `divergence_diagnosis.L6_grid_reach`). The material threshold is
`1.45` (`p2_route_l6b_v1.json` `gate.material_threshold`) and is **not met**. Raising the iteration
cap `×25` at `n_dof` fixed gives `1.5048518951028045` (`p2_route_l6b_v1.json`), still above `1.45`,
at a terminal scale-invariant stationarity `‖x‖‖∇J‖/|J|` of `44.56974279510679` for the banked
minimiser — **nowhere near stationary.** All 133 starts hit the iteration cap
(`p2_route_l6_profile_v1.json` `cost_and_shortfall.starts_that_hit_the_iteration_cap = 133`,
`UNDER_RESOURCED = true`).

### 6.2 **THE OBJECTIVE IS A DIVERGENT INTEGRAL, AND NEITHER PROGRAM IS MISCODED**

An independent re-implementation of `J(c) = ∫₀^{T_s}‖W(·,s)‖_{L^{3/2}} ds` — disjoint basis
(Cartesian real solid harmonics), disjoint radial derivatives (Taylor jets cross-checked against
mpmath at 40 dps), disjoint quadrature (composite Gauss–Legendre in `ln r`) — was built and compared
at three pre-committed points (`p2_route_ljver_v1.json`, `self_hash 4bb618d7c8b039ea`). It agrees at
the two **minimisers** (`1.0018748007447623e-04`, `1.2489672672387814e-04`) and **disagrees by 43%**
at a point that is not a minimiser (`4.2891389318254153e-01`).

The natural reading — one of the two programs computes `W` wrongly — **is refuted by measurement.**
Evaluating the independent operator **on the original program's own nodes with its own weights**
reproduces its `J` at relative `1.1007215739872338e-14`, `2.4595535367364584e-15`,
`5.896764322492505e-15`, `1.8636918650427355e-14` — **including at the point where the comparison
fails by 43%** (`X9_operator_vs_rule`).

> **A disagreement that vanishes to machine precision the moment both codes use the same quadrature
> rule, while each rule is separately converged, cannot be a coding error in either program. It is a
> property of the integral: `J` diverges logarithmically, at `r → ∞` and at `r → 0`.**

At `r → ∞`, `F_lm → F_lm(∞,s)` finite, so `w ~ A(ŷ,s)/r²`; the DSS term `a(2w + y·∇w)` annihilates a
degree `−2` homogeneous `w` exactly and `Δw` and both nonlinear terms are `O(r^{-4})`, but
`w_s ~ ∂_s A/r²` survives, giving `|W|^{3/2}r² ~ 1/r`. At `r → 0` the radial basis carries a nonzero
`r^{l+1}` coefficient and `Δ²(r^{l+1}Y_lm) = −4l(l+1)r^{l−3}Y_lm`, which at `l = 1` is `r^{-2}`,
again `|W|^{3/2}r² ~ 1/r` (`divergence_diagnosis`). The integrand's **mass per decade of `r` is
flat**, which *is* a logarithmic divergence.

**This diagnosis has since been re-executed independently of the run that produced it**
(`CORRECTIONS.md` §54): the suite was re-run on a differently loaded machine — `wall_seconds`
`1259.17` against the banked `501.32`, a `2.51×` slowdown — and **15 of 17 top-level fields came
back byte-identical**, the two exceptions being the timing block and the hash that (defectively; see
§9 item 12) covers it. **`gate`, `X9_operator_vs_rule`, `cutoff_sensitivity`,
`divergence_diagnosis`, `five_rung_table` and `L6_grid_reach` — every field this section cites — are
unchanged.**

**And one thing about that re-run must be reported against interest.** The script that produced the
`14 checks, 0 failures` line **writes the artefact it checks** (`CORRECTIONS.md` §54 items 1–3):
it recomputes everything and then compares each number to its own fresh output. **Such a script
cannot fail**, and its pass count is therefore not evidence of anything. **We do not cite that pass
count anywhere in this paper.** What *is* evidence, and is untouched by the defect, is the thing
this section actually rests on: a **second, independently written operator** — different basis,
different derivatives, different quadrature, written from the mathematics and not from the original
code — reproducing the original to `1e-14` on the original's own nodes while disagreeing by 43% on
its own. That comparison is between two programs, not between a program and itself.

**And the divergence reaches the minimiser.** From `cutoff_sensitivity` at `P1`, the banked branch-B
minimiser:

| `r_max` band | Δ`J` per decade |
|---|---|
| `1e3 → 1e4` | `+9.573e-03` |
| `1e4 → 1e5` | `+3.316e-04` |
| `1e5 → 1e6` | `+6.537e-05` |
| `1e6 → 1e8` | **`+6.226e-05`** |
| `1e8 → 1e11` | **`+6.246e-05`** |
| `1e11 → 1e14` | **`+6.212e-05`** |

(re-derived here from the banked `J` values `1.613848401215308`, `1.6139729156760465`,
`1.6141602831540638`, `1.6143466387029002`). **Three consecutive decade-bands spanning eight decades
agree to better than 1%: that is a constant increment per decade.** The origin sweep gives
`+4.19e-06` per decade over `r_min = 1e-6 → 1e-8`. **So the `1e-04` agreement at the minimiser is
not evidence that `J` converges there** — it is evidence that two truncations of similar reach
agree.

**Why eleven legs of scrutiny missed it, which is the transferable part:** the disagreement
*shrinks toward the minimiser* — `6.58e-01, 4.25e-01, 4.26e-01, 3.43e-02, 1.00e-04` across rungs
`J0…J4` (`five_rung_table`). The optimiser suppresses the divergent tail; that is its job.
**The functional is best behaved precisely where it was always evaluated.**

> **THE RULE THIS BOUGHT, and it is cheap enough that we recommend it unconditionally:** *an
> objective must be shown FINITE on its own trial space before any minimum of it is quoted, and a
> verification performed only AT the minimisers of the objective verifies almost nothing. Evaluate
> at a point the optimiser has never visited. The finiteness check — a cut-off sweep, or the mass
> per decade — costs minutes.*

### 6.3 The refinement ladder was differenced at an iteration cap that dominates it

Independently of §6.2. The four-rung ladder moved `ρ` from `1.6986514108481086` to
`1.613811231995397`, **`−4.994561%`, with every rung stopped at 800 iterations.** A single `×25`
budget step at `n_dof` **fixed** moved it from `1.613811231995397` to `1.5048518951028045`,
**`−6.751678%`**.

> **One budget step moved the objective `×1.3518` of what the entire four-rung refinement ladder
> moved.** The ladder therefore does not measure refinement; it measures where L-BFGS-B had reached
> after 800 iterations at each `n_dof`.

It can also **invert**: rung `J3` at 800 iterations reads `1.6218749783288575`, above `J4`'s
`1.613811231995397`. For the ordering to reverse, `J3` at raised budget must fall below
`1.5048518951028045` — a drop of `7.2153%`, against the `6.7517%` the same budget increase delivered
one rung up at *more* degrees of freedom. **The margin is `0.4636` percentage points, and it is the
wrong way round by less than the measurement already in hand.**

**The measurement that settles it — `J3` re-run to 20,000 iterations, reported at matched truncation
`nq_r = 72` — has not been run.** It is priced (~20–35 core-h) and its gate is pre-committed
(`CORRECTIONS.md` §53, gate v2: report the re-run rung at **both** its native `nq_r = 60` **and**
at `J4`'s reach `nq_r = 72`, `r ∈ [5.5e-4, 7.27e3]`, and treat a straddle as *undecidable at this
reach*, which is itself a result). **It was never dispatched** — it was held for cores when the run
stopped, and is parked in `OPTIONS.md` with that price and the re-open condition *cores free*.
**`NEVER DISPATCHED` is not a null result and is not written as one here.** **Until then this paper does not use `L6`'s ladder
as evidence about refinement, in either direction**, and the reader should not either.

### 6.4 What §6 does and does not license

The two defects are **independent**: the truncation bias at the minimiser is `+6.22e-05` per decade
against the ladder's last step of `−8.064e-03`, a ratio of **×130**, so §6.2 is two orders of
magnitude too small to explain §6.3.

**The sign saves the answers.** Extending the domain makes `J` **larger**, and the thresholds these
numbers had to beat were **upper** thresholds. So the `NO` answers are robust in direction; **what
is destroyed is the meaning of the numbers as values of the functional, not the answers read off
them.** Both facts are reported, and neither is allowed to soften the other.

**Nothing in §6 moves §4 or §5**, which are computed on a different object with a different
apparatus, and whose load-bearing claim is an **exponent**, not a value.

---

## §7. THE SECOND JAW: WHICH THEOREM EXCLUDES `ṁ = 0`, AND WHICH DOES NOT

`T₃ = 0` requires `ṁ ≡ 0`, i.e. an **exactly self-similar** profile. The record carried, for
months and in five places, the sentence that this is *"excluded by Nečas–Růžička–Šverák and Tsai"*.
**That sentence is wrong on both counts** — wrong in its citation and wrong in naming NRŠ. We state
the correction in the paper because the correction is part of the result.

### 7.1 NRŠ does **not** apply to this object

Nečas–Růžička–Šverák's hypothesis is `U ∈ L³(ℝ³)` **exactly**. At the pinned `α = 1` the object's
`∫|U|³` is **logarithmically divergent** — measured (`p2_route_pb2_v1.json`
`measurements.M3_q_equals_3_NRS_hypothesis`):

- decade increments constant, `increment_ratio_last_over_previous = 1.0000000000144942`;
- measured log-coefficient `60.49165798396497` against the closed form
  `∫_{S²}|A|³ dΩ = 60.49165798397186`, relative error `1.1393743809599626e-13`;
- `U_in_L3_R3 = false`.

**So NRŠ's hypothesis is not satisfied and NRŠ does not exclude this object.**

**NRŠ is also the one source this work could not obtain.** It is `UNREACHABLE` at primary after
four independent attempts (legs 253, 359, 364, 410), held `SECOND HAND` through a verbatim
quotation inside Tsai 1998 (`SOURCES.md` rows 3, 35). **The one source that cannot be read is the
one that does not carry the case.**

### 7.2 The citation the record carried was wrong in journal, volume and pages

Tsai's own bibliography, p. 50, read at FULL TEXT (`Papers/TSAI1998.pdf`, sha256
`6d3182d53806ce82fa0a2d834b31b758f22399ff625b8c8d7025a65f83fb8182`, re-confirmed by this unit
against the leg-359 pin):

> `[NRS]` J. Nečas, M. Růžička & V. Šverák, *On Leray's self-similar solutions of the Navier-Stokes
> equations*, **Acta Math. 176 (1996), 283–294.**

The record cited it as ***ARMA* 136 (1996) 55–98** in **five** places — a wall clause, a source
register, a wave plan, a banked JSON artefact, **and the driver line that generates the artefact**
(`CORRECTIONS.md` §47, §47b). *`ARMA 136 (1996) 55–98` is not a null string — it looks exactly like
a real citation, which is why it survived a verifier.* We report it because **repetition is not
corroboration; it is one source counted many times.**

### 7.3 What actually carries it: **Tsai 1998 Theorem 2**

Verbatim from the primary (`Papers/TSAI1998.pdf`, p. 30):

> **Theorem 2.** *Suppose `u` is a weak solution of `(1.1)` satisfying the local energy estimates
> `(1.4)` in the cylinder `Q₁(0,T) = B₁(0) × (T−1,T)`. If `u` is of the form `(1.2)₁`, then `u` is
> identically zero.*

and, from §2 (p. 34), the sentence that bounds its hypotheses:

> *"We remark that, in Theorem 2, we do not require the weak solution `u` to be a Leray-Hopf weak
> solution. Our only requirements (apart from self-similarity) are (i) and (ii): the Navier-Stokes
> equations and the local energy estimates."*

**No `L^q`. No Leray–Hopf. No boundary condition.** The estimate `(1.4)` is

    ess sup_{t₃<t<T} ∫_B ½|u(x,t)|² dx + ∫_{t₃}^{T} ∫_B ν|∇u(x,t)|² dx dt < ∞

for **some** ball `B` and **some** `t₃ < T`, and it is met by measurement
(`p2_route_pb2_v1.json` `M5_local_energy_estimate_TSAI_THM2_hypothesis`):
`ess_sup_t_half_L2_over_B1 = 17.090273855454814` (converged),
`int_R3_absGradU_squared_converges_to = 44.0431096341644`, space-time Dirichlet integral
`88.0862192683288`, `estimate_1p4_finite = true`.

**Tsai's Theorem 1 carries it independently**, since `U ∈ L^q(ℝ³)` for **every** `q ∈ (3,∞]`
(`M4_q_gt_3_TSAI_THM1_hypothesis`: `U_in_Lq_for_every_q_in_open_3_inf = true`,
`U_in_L_infinity = true`, `sup|U| = 2.3323807579381204`). Theorem 1's range is **open at 3**, which
is precisely where this object sits.

### 7.4 A confirmation from Tsai's own introduction that the record had not written down

Tsai, p. 30–31, describing what `[NRS]` leaves open (verbatim, read by this unit):

> *"then we only get estimates of some weighted norms which do not imply that `U ∈ L³`. […]
> Therefore, `[NRS]` left open the existence of self-similar singularities which satisfy the local
> energy estimates. For example, a solution with the following decay was not excluded:
> `(1.5) U(y) = A(y/|y|)/|y| + o(1/|y|) as y → ∞`, where `A : S² → ℝ³` is smooth."*

**`(1.5)` is the `α = 1` object.** So the case reached here by *measuring* `∫|U|³` and finding NRŠ's
hypothesis unmet is **exactly the case Tsai says in words that NRŠ leaves open and Theorem 2
closes.** Two independent routes, one conclusion. The measurement also supplies the amplitude
condition Tsai's `(1.5)` states: `min_over_S2_abs_A = 1.16619037896906 > 0`,
`vanishes_anywhere_on_S2 = false` (`M2_far_field_amplitude`).

### 7.5 The ceiling on §7, which is severe and is not softened

**Both of Tsai's theorems require the object to BE a solution.** It is not one: the smallest residual
ever measured for route 4's own object is `1.5048518951028045` (§6, at its own truncation). **The
solution hypothesis is supplied by the `ṁ = 0` branch's own counterfactual, not by measurement**
(`p2_route_pb2_v1.json` `gate.hypothesis_supplied_by_the_branch_not_by_measurement`). What is
measured is that **if** such an object existed, it would satisfy Theorem 2's *other* hypotheses.
**That is a hypothesis check, not a theorem, and this paper claims nothing more from it.**

**The class argument leaves no third case at `α = 1`:** either the far-field amplitude `A ≢ 0`, and
then `U ∉ L³` but `U ∈ ⋂_{q>3}L^q`, which is Tsai's range; or `A ≡ 0`, and then `α > 1`, which is
the other exit, shut by §3.2.

---

## §8. RELATED WORK, AND WHAT THIS PAPER DOES NOT REINVENT

We name the published methods this work uses rather than re-deriving them, and we name the depth at
which each was read here (`writeup/SOURCES.md` carries the register; `ABSTRACT` may not carry a
load-bearing claim).

| what | published home | depth reached in this work |
|---|---|---|
| a-priori decay of backward DSS solutions | Chae–Wolf, `arXiv:1610.09464`, Thm 1.1 / Rmk 1.2 | **FULL TEXT**, hashed |
| triviality of self-similar solutions under local energy estimates | Tsai, *ARMA* **143** (1998) 29–51, Thm 1 / Thm 2 | **FULL TEXT**, hashed, re-confirmed here |
| `L³` rigidity for Leray backward SS solutions | Nečas–Růžička–Šverák, *Acta Math.* **176** (1996) 283–294 | **`UNREACHABLE`** at primary; `SECOND HAND` via Tsai's verbatim quotation. **Not load-bearing here** |
| `L^{3,∞}` regularity / backward uniqueness | Escauriaza–Seregin–Šverák, *Russ. Math. Surveys* **58** (2003) | **`UNREACHABLE`**, banked as such, **never as a zero** |
| the local suitable-weak form the `α ≤ 1` step actually runs through | Seregin, `arXiv:math/0510396` §1 | **FULL TEXT** |
| Liouville theorems for rotated backward SS solutions | Pineau–Vicol, `arXiv:2607.09619`, Thms 1.6/1.7, §1.2 | **FULL TEXT**. **Independent authors, not an independent proof** |
| spatial decay of DSS flows | Bradshaw–Tsai, `arXiv:2202.08352`, `arXiv:2409.13586` | **FULL TEXT** |
| forward (D)SS existence | Jia–Šverák `arXiv:1204.0529`; Bradshaw–Tsai `1210.2783`, `1703.03480` | **FULL TEXT** |
| the poloidal–toroidal representation making `div V ≡ 0` identically | Chandrasekhar, *Hydrodynamic and Hydromagnetic Stability* (Oxford, 1961), §II | **CITATION, UNREAD.** The *identity* is `RECOMPUTED` here by two disjoint implementations (`max|div V| = 2.08e-16`); **completeness of the representation is neither used nor claimed** |
| the bound-constrained limited-memory minimiser | Byrd–Lu–Nocedal–Zhu, *SIAM J. Sci. Comput.* **16**(5) (1995) 1190–1208, via `scipy` | **`ABSTRACT`** — library executed, **paper `UNREACHABLE`** from this environment (two public URLs: one TLS certificate-name failure, one HTML block page). **Carries no load-bearing claim**: every number is the value of a residual at a banked coefficient vector, recomputable without knowing which algorithm produced it |
| divergence right-inverse (not needed for this ansatz) | Bogovskiĭ 1979 | **`UNREACHABLE`**, declared in advance; secondary `arXiv:1103.3718` at **FULL TEXT** |

**Eighteen localisation and far-field-decay techniques** were read against this object with the
failing hypothesis named, quoted and located in each: 9 `FAILS`, 8 `FAILS-BY-CONSTRUCTION`, 1
`SATISFIED` (`p2_route_l2_decay_v1.json` `techniques`).

> ### **THE NOVELTY OF THE ASSEMBLY HAS NEVER BEEN CHECKED, AND WE SAY SO HERE RATHER THAN IN A
> ### FOOTNOTE**
>
> The **ingredients** above are published. Whether the **assembly** — cut off a DSS profile, expand
> the localisation error term by term, and observe that the sole survivor is the modulation
> commutator `∝ ṁ` — is already in print **has not been assessed by anyone**. A companion effort in
> this programme ran exactly such a check on a different claim and **the check killed that claim.**
> A referee should treat this section as **an assertion of ignorance, not of novelty**, until the
> corresponding search is run and reported.

---

## §9. THREATS TO VALIDITY — THE COMPLETE LIST, INCLUDING THE ONES THAT LOOK BAD

**This section is not a formality and it has not been trimmed.**

1. **A planted control did not fire as planted.** `controls.C6_basis.fired_as_planted = false`:
   the two smoothstep bases disagree in the `curl` exponent by `0.020345978295982933` against a
   **pre-committed** tolerance of `0.01`. A **second** criterion, `fired_on_tail3_fit = true`, uses
   the same tolerance on a different fit window and passes.
   **The second criterion was added at the landing commit, after the failure on the pre-committed
   criterion was known** (`p2_verify_wave5_v1.json` `DISCREPANCY_D_V_W5_1`, site
   `experiments/p2_route_l5_v1_driver.py` `control_C6()`, commit `4be46ef`).
   **What is true in mitigation, and it is checkable:** the tolerance itself was **never moved** —
   three diff lines across all refs, all additions, literal `1e-2` in every one — the failing number
   was **not deleted**, and the tail-3 window was already in the driver **before** the run and is
   the window the gate uses everywhere else. **The failure is banked; the passing criterion is
   post-hoc; both facts belong to the reader.**
2. **The object is synthetic.** §2.2. Route 4 has no banked continuous profile. The exponents
   travel; the constants do not.
3. **`c_mod` is basis-dependent by `1.476038407975093`** and is quoted unqualified in the artefact's
   own gate block (`p2_verify_wave5_v1.json` `DISCREPANCY_D_V_W5_2`, **not repaired**).
4. **`c_mod` is under an open divergence flag** (§5.3), whose discharging unit had not returned when
   this was written. **This is `OPEN`, not `NO`.**
5. **The `α ≤ 1` jaw is not at primary and cannot be from here** (§3.2). It rests on an unproved
   one-sentence remark in a secondary plus a restatement by an author of the unreachable primary.
6. **The `α ≥ 1` jaw's hypothesis check is recorded at `α = 1`**, the value being established
   (§3.1). Repairable; not repaired in the record.
7. **Route 4's own objective is a divergent integral** and every residual for it is a value of a
   72-node truncation (§6.2). The affected numbers' **direction** is known and unfavourable to
   closure; their **values** have no limit.
8. **`L6`'s refinement ladder is budget-confounded** (§6.3) and the measurement that would settle it
   has not been run. `UNDER-RESOURCED`, priced, **not a null**.
9. **The independent re-implementation inherited the `Y_lm` convention** of the code it checks — a
   comparison at a shared coefficient vector is meaningless otherwise — so **a common-mode error in
   the convention is invisible to it** (`CORRECTIONS.md` §52, ceilings). Closed-form controls guard
   it partially; they do not close it.
10. **Novelty unassessed** (§8).
11. **The independent re-implementation's own evidence script re-runs the experiment and
    overwrites the artefact it checks**, so its `14/14 passed` measures nothing
    (`CORRECTIONS.md` §54). The **operator comparison** it contains is unaffected, was re-executed
    on a different machine load, and reproduced byte-identically (§6.2) — but the pass count is
    void and is not cited here.
12. **`self_hash` in this repository certifies nothing about content.** The hash is taken over a
    record that already contains the run's `wall_seconds`, so two executions with bit-identical
    mathematics hash differently (`4bb618d7c8b039ea` vs `5b949a5c6b28fc72`) — `CORRECTIONS.md` §54
    item 5. **The `self_hash` values in §11 are identifiers of the banked file, not integrity
    certificates**, and no claim in this paper rests on one.
13. **The load-bearing norm has no term-by-term decomposition in the record** (§4 box). The
    identification of `T₃` as the sole survivor is asserted **only in the secondary norm**.
14. **The headline `ρ`-exponent changes sign with the fit window** (`+1.085e-04` tail-3 against
    `-2.340e-02` full-range), and the gate's answer text attaches the tail-3 value to the full
    range (§5.1).
15. **One primary and two monographs are `UNREACHABLE`** from this environment (NRŠ 1996, ESŠ 2003,
    Chandrasekhar 1961; plus Byrd–Lu–Nocedal–Zhu 1995). Each is banked as `UNREACHABLE`, **never as
    a zero**, and no paywall was circumvented at any point.

---

## §10. CONCLUSION

For a natively finite-energy modulated, localised ansatz built on a backward DSS profile, the
localisation error is, at large cut-off radius, **the modulation commutator and nothing else**:
`|T₁+T₂|/|T₁| = 2.5780635399678998e-08`, `T₄`, `T₅ ~ ρ^{-2}`, and the total is `T₃` to
`0.9999978617027289` — **all three in the secondary `L³` norm, the only norm in which the record
decomposes the residual at all** (§4). `T₃` is algebraically `∝ ṁ` with scale-invariant size `ρ^{1-α}`, so it
vanishes only at `α > 1` or `ṁ = 0`, and each exit is closed by a published theorem — the first by
Chae–Wolf's Remark 1.2 through Escauriaza–Seregin–Šverák, the second by **Tsai's Theorem 2**, whose
hypotheses this object is measured to satisfy.

The failure is at an **endpoint**: summability needs a strictly negative `ρ`-exponent and `α = 1`
delivers exactly zero (`1.0850007559945518e-04` measured).

> **THIS IS THE WHOLE CONTRIBUTION: the identification of `T₃` as the sole survivor and its
> `ṁ`-proportionality, in float64, on a synthetic profile** — and, narrower than that ceiling
> requires, **in the secondary norm.**

It is not a proof, it does not construct or exclude a blow-up, and **it does not move the
Navier–Stokes existence-and-smoothness problem.**

---

## §11. DATA AVAILABILITY AND REPRODUCTION

Every number above is a field of a banked artefact. In file order.

> **READ THE `self_hash` COLUMN AS AN IDENTIFIER, NOT AS A CERTIFICATE.** `CORRECTIONS.md` §54
> item 5 established that `self_hash` is computed over a record that includes the run's wall-clock
> time, so it changes when nothing mathematical has. **It cannot detect drift, tampering or a
> silent change to a banked number, and nothing in this paper rests on one.** It is printed only so
> a reader can name the exact file version consulted.

| artefact | `self_hash` | what it carries here |
|---|---|---|
| `writeup/data/p2_route_l5_finite_energy_v1.json` | `0c5e0f827f526df6` | §4, §5 — the five terms, the exponents, `c_mod`, `C3'`, `C6`, `C7` |
| `writeup/data/p2_route_l2_decay_v1.json` | — | §3 — the 18-technique census with verbatim decisive hypotheses |
| `writeup/data/p2_route_l2_decay_v2.json` | `9a58a36c81734066` | §3.2 — the provenance correction `D6`; the `N1` amplitude-dependence correction |
| `writeup/data/p2_route_pb2_v1.json` | — | §7 — `M1`–`M5`, the hypothesis checks |
| `writeup/data/p2_route_l6_profile_v1.json` | `6a033004deef39d3` | §6.1, §6.3 — the ladder and its reaches |
| `writeup/data/p2_route_l6b_v1.json` | — | §6.1, §6.3 — the `×25` budget step |
| `writeup/data/p2_route_ljver_v1.json` | `4bb618d7c8b039ea` | §6.2 — the independent operator, `X9`, `cutoff_sensitivity` |
| `writeup/data/p2_verify_wave5_v1.json` | — | §4, §9 — the independent verification and its three unrepaired discrepancies |
| `writeup/data/p2_route_cloc_v1.json` | `58c57b62c0cbc80d` | §2 — leg 381's banked `ρ`-exponents |

**Correction records:** `writeup/CORRECTIONS.md` §34 (synthetic realization), §47/§47b (the
citation), §51 (the budget confound), §52 (the divergent objective), §53 (the landing audit, the
sign, and the open `c_mod` flag).

**Source register with per-source depth:** `writeup/SOURCES.md`.

**A note on what "reproduction" means for the numbers in §6.** They are values of a truncation of a
divergent integral. Reproducing them requires reproducing the **truncation** — `r_min`, `r_max`,
`nq_r` — and those are stated everywhere they appear in this paper for exactly that reason.

---

### Standing statement

**No external contact of any kind was made in the preparation of this draft.** Reading published
material is authorised in this programme; contacting an author, group, maintainer or list is under
a standing hold, and no such contact occurred. No paywall was circumvented; sources that could not
be obtained are recorded as `UNREACHABLE` rather than as absent.

**A companion file, `FINDINGS.md`, records everything that would not state cleanly here.** It is the
second output of drafting and it is not summarised in this paper.
