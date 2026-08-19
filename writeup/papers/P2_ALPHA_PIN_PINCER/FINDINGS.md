# P2 — FINDINGS FROM DRAFTING

**`writeup/papers/P2_ALPHA_PIN_PINCER/FINDINGS.md`. Unit `P2-DRAFT`, leg 415, wave 9.**

**This file is the second output of drafting and it is not the paper.** It records every
contradiction, unsupported number, and claim that dissolves when it is written out for a referee.
**Nothing here is smoothed over in `DRAFT.md`, and nothing here was discovered by re-running
anything** — this unit ran no experiment and produced no new measurement. Every item is a statement
about the *record*, located in the field or file that carries it.

**`FINDINGS.md` APPLIES NOTHING.** It does not edit `CORRECTIONS.md`, `WALLS.md`, `STATE.md`,
`OPTIONS.md`, `writeup/waves/**`, or any artefact. It is a list for whoever holds the authority to
act on it.

**Severity vocabulary used below:**

- **ESCALATE NOW** — do not wait for end-of-wave.
- **BLOCKS SUBMISSION** — the paper cannot go to a referee until this is discharged.
- **DISCLOSED** — real, in the draft, not blocking.
- **OPEN** — a live unit or an unpriced measurement owns it; explicitly *not* a null result.

---

## SUMMARY TABLE

| id | severity | one line | reopens a wall? |
|---|---|---|---|
| **F1** | **ESCALATE NOW** | The term-by-term decomposition exists **only in the norm the gate calls SECONDARY**. The paper's whole sentence is at the wrong norm. | **No** — but it changes what P2 may claim |
| **F2** | **DISCLOSED** | `gate.the_obstruction_named` quotes two secondary-norm ratios inside a sentence about the load-bearing norm, unqualified | No |
| **F3** | **DISCLOSED** | The headline `ρ`-exponent **changes sign with the fit window**, and the gate's answer text attaches the tail-3 value to the full range | No |
| **F4** | **DISCLOSED** | `C3′`'s `meaning` says `c_mod` "vanishes" at zero modulation amplitude. The measured value is `0.5505448978148512` | No |
| **F5** | **DISCLOSED** | `C7`'s baseline column is **not** the gate sweep's `L3` at the same `ρ₀` (`62.96` vs `46.77`) and the artefact never states either domain | No |
| **F6** | **DISCLOSED** | Chae–Wolf Thm 1.1's decisive hypothesis is checked **at `α = 1`**, the value the theorem is being used to establish | No |
| **F7** | **OPEN** | `c_mod = 869.288` is under §53's divergence flag; the discharging unit had not returned | No — the **sign** protects the answer |
| **F8** | **OPEN** | `L6-e` is **NEVER DISPATCHED**. `L6`'s ladder is unusable as refinement evidence in either direction | No |
| **F9** | **DISCLOSED** | §54: `self_hash` covers `wall_seconds`, so **every "unchanged" citation in the record is void**; and one evidence suite's pass count measures nothing | No |
| **F10** | **BLOCKS SUBMISSION** | Novelty is **unassessed**. `P1`'s equivalent check killed `P1` | No |
| **F11** | **ESCALATE — USER/CONDUCTOR DECISION** | Should this paper be written at all, or is the honest object a note about the **exponent** plus a methodological piece? | No |
| **F12** | **DISCLOSED, PERMANENT** | The `α ≤ 1` jaw **cannot** be read at primary from this environment. This is a ceiling, not a debt | No |
| **F13** | **DISCLOSED** | `V-W5`'s three discrepancies remain **unrepaired**, and `V-W5` states it "did NOT verify the SCIENCE" | No |
| **F14** | **DISCLOSED** | The gate's own answer text says `c_mod` **"saturates"**. Under §53 that verb may be false | No |
| **F15** | **DISCLOSED, MINOR** | `C3′` does not record the cut-off radius it was run at. It is recoverable only by matching a float against the sweep | No |

**No finding below reopens a wall.** The reason, stated once and true of every item: **W4 clause (b)
is shut on `curl_L32`'s directly measured behaviour and on two published theorems, neither of which
depends on any decomposition, fit window, or constant flagged here.** Several findings destroy
numbers. None reverses an answer. **Both halves of that sentence matter and neither is allowed to
soften the other.**

---

## F1 — **ESCALATE NOW.** THE DECOMPOSITION IS IN THE SECONDARY NORM. THE PAPER'S SENTENCE IS AT THE WRONG NORM.

**Where.** `writeup/data/p2_route_l5_finite_energy_v1.json`,
`sweep["alpha=1|kappa=a_physical_frozen|DSS"]`.

**What.** The gate names two norms:

    gate.norm           = "||curl F||_{L1_t L3/2_x} ... (pressure-free)"      <- LOAD-BEARING
    gate.secondary_norm = "||F||_{L1_t L3_x}"                                 <- SECONDARY

**Every per-term field in the artefact is a secondary-norm field.** The complete list of per-term
keys is `T1_L3`, `T2_L3`, `T3_L3`, `T4_L3`, `T5_L3`, `T12_L3`, `T123_L3` and their
`_rho_exponent`, `_rho_exponent_tail3`, `_at_largest_rho` variants. **There is no per-term field in
the load-bearing norm anywhere in the file.** The load-bearing norm appears as one total per row:
`curl_L32`.

Consequently:

- `T12_over_T1_at_largest_rho = 2.5780635399678998e-08` is `T12_L3 / T1_L3`
  (`4.632834719327343e-06 / 179.70211546395896`) — **secondary norm.**
- `total_over_T3_at_largest_rho = 0.9999978617027289` is `L3 / T3_L3`
  (`46.76963450313766 / 46.769734510733336`) — **secondary norm.**

**Why it is more than a labelling slip.** The load-bearing norm is load-bearing *because* `curl`
annihilates `∇P`, so the pressure term `T₆` drops out of it. In the secondary norm **`T₆` does not
drop out — and `T₆` is not in the decomposition at all.** So the secondary-norm "total" is not the
sum of the seven terms; a term-wise conclusion drawn in that norm is not closed, and it is drawn in
the one norm where the pressure is unaccounted for.

**What it does to this paper.** The contribution ceiling is *"the identification of `T₃` as the sole
survivor and its `ṁ`-proportionality, in float64, on a synthetic profile."* **As the record stands,
the honest sentence is narrower: `…in float64, on a synthetic profile, in the secondary norm.`**
`DRAFT.md` now says exactly that, in the abstract, in a box before §4's first number, and in the
conclusion. Writing *narrower* than the ceiling is permitted; writing at the ceiling here would not
have been supported.

**What it does NOT do.** It does not touch `W4` clause (b). The `NO` is read off `curl_L32`
directly — `995.488, 869.968, 869.068, 869.261, 869.288` across the sweep — which is a
load-bearing-norm measurement requiring no decomposition. **The wall does not move.**

**Why this is `ESCALATE NOW` rather than end-of-wave.** It is the cheapest correction in this
paper's ledger and the one with the largest effect on what the paper may say. The apparatus already
computes `curl R_loc`; recording `‖curl Tᵢ‖_{L^{3/2}}` per term is a change in what is written to
the artefact, not a new calculation, and it would either (i) promote the paper's central sentence
to the load-bearing norm, or (ii) show that the load-bearing decomposition looks different — in
which case the paper as drafted is wrong and should not be written further. **Both outcomes are
results, and the second one is the reason not to wait.**

**A caution against the obvious shortcut.** Do **not** infer the curl-norm term sizes from the
`L³` ones. `curl` is a derivative; the terms live on different length scales — `T₄`, `T₅` are
supported in the transition shell of width `∝ ρ`, `T₃` is not — so the exponents need not shift by
a common power. **That inference is exactly the kind of step this programme has repeatedly had to
retract, and it must be measured, not argued.**

---

## F2 — THE GATE'S OWN OBSTRUCTION SENTENCE MIXES THE TWO NORMS WITHOUT SAYING SO

**Where.** Same file, `gate.the_obstruction_named`.

The field reads, in a passage whose subject is the load-bearing norm:

> "…at `kappa = a` the cutoff-drift `T1` and the modulation-transport `T2` CANCEL IDENTICALLY
> (measured `|T1+T2|/|T1| = 2.578e-08`) … and what is left is EXACTLY `T3` (measured
> `|R_loc|/|T3| = 0.999998`)."

Both quoted ratios are `L³` ratios (F1). **The field does not say so.** A reader of the artefact —
including a downstream unit, including this one on first pass — will take them for load-bearing
numbers, because the surrounding sentence is about the load-bearing norm.

**Not repaired here.** `W3` ruling Q3: a banked datum gets a correction record beside it, never an
edit. This is the record. `DRAFT.md` §4 states the norm before quoting either number and does not
reproduce the artefact's phrasing.

---

## F3 — THE HEADLINE `ρ`-EXPONENT CHANGES SIGN WITH THE FIT WINDOW, AND THE GATE TEXT MISSTATES ITS RANGE

**Where.** Same file, same row, and `gate.answer_in_precommitted_wording`.

| quantity | full-sweep fit | tail-3 fit |
|---|---|---|
| load-bearing `curl_L32` | `curl_L32_rho_exponent = -2.340048393964631e-02` | `curl_L32_rho_exponent_tail3 = +1.0850007559945518e-04` |
| secondary `L3` | `L3_rho_exponent = -4.913347365381298e-03` | `L3_rho_exponent_tail3 = +8.350419121029962e-05` |

`gate.rho_exponent` publishes the **tail-3** value. Both norms flip sign between the two windows.

**And the gate's pre-committed answer text attaches the tail-3 number to the wrong range**, verbatim:

> "with measured `rho-exponent 0.000109` over `rho0` in `[10, 1000]`"

The sweep's five `ρ₀` are `10, 30, 100, 300, 1000`; **the tail-3 fit uses `100, 300, 1000`.** Over
`[10, 1000]` the measured exponent is `-0.0234`, not `+0.000109`.

**Severity: DISCLOSED, not escalated.** The choice of the tail is *defensible on its face* — the
first two radii are still inside the transition region where `T₄`, `T₅` are large (`T4_L3` falls
from `15.34` at `ρ = 12.6` to `1.7e-3` at `ρ = 1261.7`), so a fit including them measures the decay
of terms the ansatz was never claiming to control. **But that argument is not written down
anywhere in the record**, and the window was not pre-registered in the artefact.

**And the `NO` does not depend on it.** What the `NO` actually rests on is the raw sequence
`869.968 → 869.068 → 869.261 → 869.288`, whose last two per-decade increments are `+0.403874` and
`+0.051881` — a sign that is read off the numbers, not off a fit.

---

## F4 — `C3′` SAYS `c_mod` "VANISHES" AT ZERO MODULATION AMPLITUDE. IT MEASURES `0.5505448978148512`.

**Where.** Same file, `controls.C3p_modulation_amplitude_linearity`.

The `meaning` field, verbatim:

> "amp = 0 is EXACTLY the self-similar case; **c_mod vanishes there** and is linear in the
> modulation amplitude, so c_mod = 0 iff the profile is SS"

The `rows` at `amp = 0.0` give `curl_L32 = 0.5505448978148512` and `L3 = 0.016567754303355667`.
The same control banks `value_at_amp_zero = 0.5505448978148512` — **so the artefact contains its own
refutation of its own prose, in an adjacent field.**

**Is it a contradiction or a wording defect?** A wording defect. `0.5505` is `6.33e-04` of the
`amp = 1` value `869.2606943625965`, and the non-modulation leftovers `T₄ + T₅` at the radius this
control was run at are `4.6e-04` of the total in the secondary norm and fall like `ρ^{-2}`. The
residual at `amp = 0` is the `T₄`, `T₅` floor, exactly as the term table predicts. **The number is
consistent with the physics; the sentence is not consistent with the number.**

**Why it is worth a finding anyway.** `"c_mod = 0 iff the profile is SS"` is the sentence that
licenses the whole `ṁ = 0` branch of the pincer — the branch §7 of the draft then hands to Tsai's
Theorem 2. **The strongest sentence in the artefact is the one its own adjacent field contradicts.**
The correct statement is: *`T₃` is algebraically exactly zero iff `ṁ ≡ 0`; the measured residual at
`ṁ = 0` is the `ρ^{-2}` floor of the other terms and is not zero at finite `ρ`.* `DRAFT.md` §4.3
says that and does not use the word "vanishes".

---

## F5 — `C7`'s BASELINE IS NOT THE GATE SWEEP'S `L3`, AND NEITHER DOMAIN IS STATED

**Where.** Same file, `controls.C7_modulation_absorption_falsifier.rows` against
`sweep[...].rows`.

| `ρ₀` | `C7.L3_before` | sweep `L3` |
|---|---|---|
| 10 | `50.7425735600177` | `48.16327253969874` |
| 30 | `61.50495315517625` | `46.69549900647345` |
| 100 | `62.833576033793676` | `46.76052659972439` |
| 300 | `62.95107567150693` | `46.76868146611154` |
| 1000 | `62.9644481181405` | `46.76963450313766` |

They agree to `5%` at the smallest radius and differ by `35%` at the largest, and the fitted
exponents differ in sign as well as size (`C7.rho_exponent_before = +3.920796934533938e-02` against
`L3_rho_exponent = -4.913347365381298e-03`).

`C7`'s `meaning` states only that **its** projection is *"taken over ALL of `ℝ³`, core included"*.
**The artefact nowhere states the domain over which the sweep's `L3` is taken.** So the two columns
are presumably different quantities — plausibly one integrated over `ℝ³` and one over the annulus
— but **that is an inference, and the record does not contain the sentence that would settle it.**

**What it costs.** `C7` is the paper's planted falsifier: the check that a modulated ansatz cannot
spend `(a, κ)` absorbing the residual. Its verdict is `fraction_remaining = 1.0009067172080548`,
i.e. absorption makes things marginally worse. **That verdict is internally consistent** — it is a
ratio of `L3_after` to `L3_before` **within `C7`'s own column**, so an undocumented domain does not
corrupt it. **What is not supported is any statement that `C7` falsified absorption of the residual
the gate reports.** `DRAFT.md` §4.4 states the discrepancy and explicitly declines to compare the
two columns.

---

## F6 — THE `α ≥ 1` JAW'S HYPOTHESIS IS CHECKED AT `α = 1`

**Where.** `writeup/data/p2_route_l2_decay_v1.json`, technique `T2a`, field `why_for_this_object`.

Chae–Wolf Theorem 1.1 requires `u ∈ C((−∞,0); L^p(ℝ³))` for some `3 ≤ p < ∞` and concludes
`|u| ≤ C/(√(−t)+|x|)`, i.e. `α ≥ 1`. The record's hypothesis check reads:

> "**At alpha = 1** the profile is in `L^p(R^3)` for every `p > 3`…"

**The hypothesis is verified at the value the theorem is invoked to establish.** As written this is
circular.

**It is repairable and I state the repair rather than merely the complaint:** for any `α > 0`, the
far-field integral `∫^∞ r^{-αp} r² dr` converges whenever `p > 3/α`, so an admissible finite
`p ≥ 3` exists for every `α > 0`, and the theorem applies without presupposing its own conclusion.

**But that sentence is not in the record**, and this file does not put it there — `FINDINGS.md`
applies nothing, and a repair to a banked artefact is not this unit's to make. `DRAFT.md` §3.1
discloses the gap and states the repair as a repair, not as a citation.

---

## F7 — **OPEN.** `c_mod = 869.288` SITS UNDER §53's DIVERGENCE FLAG AND THE DISCHARGING UNIT HAD NOT RETURNED

`CORRECTIONS.md` §53 flagged `c_mod` `NOT ADJUDICATED`: a power-law fit cannot distinguish
saturation from `log ρ` growth, because a logarithmic divergence **is** the exponent-zero case, and
`L5`'s sweep stops at `ρ ≈ 1.26e3` with its last two per-decade increments **positive**.

**Independently re-derived here from the banked rows**, so that the draft does not cite §53 for its
own arithmetic — the per-decade increments of `curl_L32` along the load-bearing row:

| band | Δ per decade |
|---|---|
| `12.617 → 37.852` | `−263.078289` |
| `37.852 → 126.172` | `−1.721357` |
| `126.172 → 378.515` | `+0.403874` |
| `378.515 → 1261.717` | `+0.051881` |

All four reproduce §53's quoted values exactly once the alternating `×3` and `×10/3` sweep steps
are used for the decade widths (`0.477121` and `0.522879`). **§53's arithmetic is confirmed at
primary by this unit.**

**Status at the time of writing: the unit that extends this sweep to `ρ = 1e8` had NOT returned.**
`DRAFT.md` §5.3 records it as **OPEN** and pre-writes both outcomes:

- **divergent** ⟹ `869.288` is a value of `L5`'s cut-off, not of the functional; *"saturates at
  `c_mod = 869.288`"* becomes **false as stated** and must read *"grows without bound"*; **the
  conclusion strengthens.**
- **saturating** ⟹ the constant stands, at its reach.

**`UNDER-RESOURCED` / `NOT ADJUDICATED` IS NOT A NULL RESULT AND IS NOT WRITTEN AS ONE.**

---

## F8 — **OPEN.** `L6-e` WAS NEVER DISPATCHED, SO `L6`'s LADDER IS UNUSABLE AS REFINEMENT EVIDENCE

`CORRECTIONS.md` §51: `L6`'s four-rung ladder moved the objective `−4.994561%` **with every rung
stopped at 800 iterations**; a single `×25` budget step at fixed `n_dof` moved it `−6.751678%`.
**One budget step moved it `×1.3518` of the entire ladder.** The ordering can invert on a margin of
`0.4636` percentage points.

`OPTIONS.md` now records `L6-e` as **`⛔ NEVER DISPATCHED`** — held for cores when the run stopped —
priced at `~20–35 core-h`, re-open condition *cores free*, with gate v2 (report at both the native
`nq_r = 60` and at `J4`'s reach `nq_r = 72`, `r ∈ [5.5e-4, 7.27e3]`; a straddle means *undecidable
at this reach*, which is itself a result) pre-committed and unchanged.

**Consequence for the paper, and it is a prohibition, not a caveat:** `DRAFT.md` may not use `L6`'s
ladder as evidence about refinement **in either direction** — not as evidence that refinement helps,
and not as evidence that it does not. §6.3 says so.

---

## F9 — §54: `self_hash` IS NOT A CONTENT HASH, AND ONE EVIDENCE SUITE'S PASS COUNT MEASURES NOTHING

Landed today, after `STATUS.md` was written and while `DRAFT.md` was being written; folded in.

**(a) `self_hash` covers `wall_seconds`.** Two executions with bit-identical mathematics produced
`4bb618d7c8b039ea` and `5b949a5c6b28fc72`. **A `self_hash` in this repository certifies nothing
about content and cannot detect drift, tampering or a silent change to a banked number.**

**This has a consequence for this paper specifically.** `DRAFT.md` §11 lists `self_hash` values for
nine artefacts. Every one of them is now an **identifier of a file version**, not an integrity
certificate, and §11 carries a box saying so. **Anywhere in the wider record a `self_hash` is cited
as evidence that an artefact is unchanged, that citation is void** — including, for completeness,
`p2_verify_wave5_v1.json` `item_4_self_hashes`, whose `"REPRODUCES"` verdict is true as arithmetic
and empty as assurance.

**(b) An evidence script that writes the artefact it checks cannot fail.** The suite reporting
`14 checks, 0 failures` recomputes everything and compares each number to its own fresh output.
**`DRAFT.md` cites that pass count nowhere.**

**(c) The good half, which must not be lost.** The same re-run happened on a machine `2.51×` more
loaded and reproduced **15 of 17 top-level fields byte-identically** — the exceptions being the
timing block and the hash that covers it. **Every field §52 and §53 cite is unchanged**, so the
divergence diagnosis is independently reproduced. And the thing the draft actually leans on is
untouched by the defect: a **second, independently written operator** — different basis,
derivatives and quadrature — reproducing the first to `1e-14` on the first's own nodes while
disagreeing by `43%` on its own. **That comparison is between two programs, not between a program
and itself.**

---

## F10 — **BLOCKS SUBMISSION.** NOVELTY IS UNASSESSED, AND THE PRECEDENT IS A KILL

Nobody has checked whether the assembly — cut off a DSS profile, expand the localisation error term
by term, observe that the sole survivor is the modulation commutator `∝ ṁ` — is already in print.
The **ingredients** are all published and cited. **The assembly has never been searched for.**

**The precedent is not neutral.** The sibling paper `P1`'s equivalent check was run and **killed
`P1`**. A `YES` here is the cheapest possible result and it ends the paper.

**Until it is run, `DRAFT.md` §8's related-work section is an assertion of ignorance, not of
novelty**, and it says so in a boxed heading rather than a footnote. **A paper may not be submitted
on an unexamined novelty claim.**

---

## F11 — **ESCALATE: A DECISION THIS UNIT MAY NOT TAKE.** SHOULD THIS PAPER EXIST IN THIS FORM?

Assembled from F1, F3, F7, F8 and `CORRECTIONS.md` §52/§53, the position is:

- The paper's **central identification** is in the **secondary** norm (F1).
- Its **headline constant** `c_mod` is (i) basis-dependent by `1.476038407975093`,
  (ii) a value at a reach of `ρ ≤ 1261.717`, and (iii) under an open divergence flag (F7).
- Route 4's own residuals are **values of a 72-node truncation of a divergent integral**, and their
  refinement ladder is budget-confounded with the settling measurement never dispatched (F8).
- What is **truncation-free, basis-robust and window-robust in sign at the scale that matters** is
  the **`ρ`-exponent being non-negative**, i.e. the endpoint, together with the two published
  theorems that close the two exits.

> **THE QUESTION, PUT TO THE CONDUCTOR AND THROUGH IT TO THE USER, AND NOT ANSWERED HERE:**
>
> Is the honest object a paper built around two constants that are values of truncations — or a
> **shorter note about the exponent**, which is the part that survives every defect in this file,
> plus a separate methodological piece on **what §52, §53 and §54 found**: a divergent objective
> that looked convergent because it was only ever evaluated at its minimisers; a refinement ladder
> differenced at an iteration cap that dominated it; an evidence script that could not fail; and a
> content hash that hashed the clock?
>
> **I have drafted the paper I was dispatched to draft.** I flag, without acting on it, that the
> methodological findings may be the more transferable result, and that they are not this paper's
> to carry — a sibling unit owns the methodology paper this wave and this unit does not write into
> its territory.

---

## F12 — **PERMANENT.** THE `α ≤ 1` JAW CANNOT BE READ AT PRIMARY FROM HERE

Not a debt to be worked off; a ceiling on the environment. Recorded so that no future unit spends a
leg rediscovering it.

- The step is Chae–Wolf **Remark 1.2** — **one unproved sentence, no hypotheses stated** — citing
  Escauriaza–Seregin–Šverák.
- **ESŠ 2003 is `UNREACHABLE` at primary**, banked as `UNREACHABLE` and **never as a zero**.
- **Nečas–Růžička–Šverák 1996 is `UNREACHABLE`** after four independent attempts (legs 253, 359,
  364, 410), held `SECOND HAND` through a verbatim quotation inside Tsai 1998.
- Reachable at primary **only** in the local suitable-weak form, Seregin `arXiv:math/0510396` §1, by
  an author of the unreachable primary. **This is not a technicality:** the object's global energy
  is *measured* infinite (`∫_{|y|<10^k}|U|²` linear in the cut-off radius: `1153.09`, `125445.0`,
  `1.2566e7`, `1.25664e9`), so it is **not** a Leray–Hopf solution and the *global* form of ESŠ does
  not apply to it. The local form is the only one that does.
- **Pineau–Vicol are independent AUTHORS, not an independent PROOF**: their statement is for
  *rotated globally self-similar* solutions and also terminates at ESŠ. Extending it to DSS is
  immediate — **and that step is this programme's, not in their bytes.**

**No external contact was attempted or is permitted.** Contacting an author, group, maintainer or
list remains held; obtaining these sources by asking is **not** an available remedy. `DRAFT.md` §3.2
states the jaw at exactly this strength and explicitly declines to present the two jaws as equally
sourced.

---

## F13 — `V-W5`'s THREE DISCREPANCIES ARE UNREPAIRED, AND `V-W5` DID NOT VERIFY THE SCIENCE

`writeup/data/p2_verify_wave5_v1.json`: `checks_run = 120`, `checks_failed = 0`,
`defects_repaired = 0`, `quadrature_rerun_in_this_run = true`.

Unrepaired: **`D-VW5-1`** — `C6`'s second pass-criterion `fired_on_tail3_fit` was added at the
landing commit `4be46ef`, **after** the failure on the pre-committed criterion
(`exponent_disagreement_curl = 0.020345978295982933` against `precommitted_tolerance = 0.01`) was
known. **In mitigation, and it is checkable: the tolerance was never moved** — three diff lines
across all refs, all additions, literal `1e-2` in each — the failing number was not deleted, and the
tail-3 window pre-existed the run. **`D-VW5-2`** — `c_mod` is quoted unqualified in the gate block
despite the `1.476` basis spread. **`D-VW5-3`** — a cost ratio scraped from prose rather than banked
(NIL effect; the banked-rows route gives the same conclusion).

**And the unit's own limit, in its own words:** `what_this_unit_did_NOT_do` includes
*"did NOT verify the SCIENCE -- only the arithmetic and the provenance"* and *"did NOT upgrade
`L5`'s `NO` on the strength of reproducing it"*.

**Reading this correctly matters.** `120/120` is a strong statement about *arithmetic reproduction*
— including a genuine re-run of the float64 quadrature from `L5`'s own code returning identical
doubles — and **not a statement about the science at all**. **A verifier that reproduces a number
exactly has said nothing about whether the number means what its field name says**, which is
precisely how F1, F2 and F4 survived a `120/120` verification.

---

## F14 — THE GATE'S ANSWER TEXT SAYS `c_mod` "SATURATES". UNDER §53 THAT VERB MAY BE FALSE.

`gate.answer_in_precommitted_wording`, verbatim: *"the error PER UNIT SIMILARITY TIME **saturates**
at `c_mod = 869.288`"*.

If F7's open flag resolves to *divergent*, `c_mod` does not saturate — it grows like `log ρ`, and
`869.288` is a property of where the sweep stopped. **The verb is load-bearing in the sentence and
is not adjudicated.**

**The answer survives either way, and only because of the sign**: the gate is `NO` because the error
is too **large**; growth makes it larger; `gate.threshold_free = true` and
`gate.Sigma_infinity = "infinity"` are unaffected. **A defect with a known sign can leave every
conclusion standing while destroying every number, and this file exists so that both facts are on
the record.** `DRAFT.md` §5.3 avoids the verb and states both branches.

---

## F15 — **MINOR.** `C3′` DOES NOT RECORD THE CUT-OFF RADIUS IT WAS RUN AT

`controls.C3p_modulation_amplitude_linearity` banks five `(amp, L3, curl_L32)` rows and no `ρ₀`.
The radius is recoverable **only** by matching the `amp = 1.0` row's `L3 = 46.76868146611154`
against the sweep, where it identifies `ρ₀ = 300` (`ρ = 378.5152032378359`) — a float-equality
match against another table.

**Why a finding at all.** F4's defence of `C3′` — that the residual at `amp = 0` is the `T₄`, `T₅`
floor — **is a statement about a specific radius**, and it is only checkable because the float
happens to match. **A control whose operating point must be recovered by float-matching is not
self-describing**, and the next reader may not get the match.

---

## WHAT THIS UNIT DID NOT DO

- Ran **no experiment**, produced **no new measurement**, touched **no experiment code or
  artefact**.
- **Repaired nothing.** Every defect above is recorded beside the datum, per `W3` ruling Q3.
- Wrote **nothing** into `STATE.md`, `WALLS.md`, `OPTIONS.md`, `reports/`,
  `writeup/CORRECTIONS.md`, `writeup/waves/**`, or the sibling unit's paper directory.
- **Made no external contact of any kind.** Reading published material is authorised here;
  contacting an author, group, maintainer or list is under a standing hold and no such contact
  occurred. No paywall was circumvented.
- **Moved no `L1 → L4` link.** Drafting a paper is not progress on the problem. **Clay stays
  ~0.05%.**
