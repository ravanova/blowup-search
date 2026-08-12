# TECHNICAL — Route-DTOL v1 (leg 386): the pre-registered tolerance mode, and the tolerance the §4 composition can afford

*Companion: `BLOG_P2_ROUTEDTOL_V1.md`. Figure `fig99`
(`writeup/figures/fig99_route_dtol_v1_delta_window.png`, rebuilt from JSON alone by
`experiments/p2_route_dtol_v1_evidence.py`). Runner `experiments/p2_route_dtol_v1.py`;
data `writeup/data/p2_route_dtol_v1.json`; journal `experiments/journal/leg_386.md`
(PART I = pre-registration, committed `caf48e8` **before** any measurement; PART II = results);
novelty log `writeup/novelty/leg_386.md` (`36d01c7`).*

**CEILING: TIER 2 in every branch. `CLAY_OBLIGATIONS.md` §6 items 1 and 2 remain OPEN.
No `L1 → L4` link moved. Clay stays ~0.05%.**

---

## 0. The two gate clauses, answered in the gate's own wording

**Clause 1.** *At the freshly-measured `δ*`: do the three non-power planted cases certify with
contained truth and reported widths, does the exact power law still certify at `δ = 0` with
382's widths reproduced, AND does a sub-`δ*` control remain EMPTY (the mode must not turn the
instrument into a fit with extra steps)?*

> **YES.** 1a ✔ (width law), 1b ✔ (three cases certify at `δ*`, truth contained), 1c ✔ (`δ = 0`
> reproduces 382's widths to a factor `1.0002`), 1d ✔ (6/6 EMPTY below `δ*`).

**Clause 2.** *Does the admissible-cutoff analysis tolerate `δ > 0` AT ALL?*

> **EMPTY at the α value in play.** At `α_centre = 1`, the α the banked Type-I object carries,
> the composed window `D = { δ ≥ 0 : verdict = INTERVAL and p_lo > α_threshold }` is empty, and
> it is empty at every `α_centre ≤ threshold`. **0 of 30** measured rows are admissible with a
> realised `α_centre ≤ 1`.

**They are not netted.** The mode is a real instrument (clause 1) that the specific composition
§4 needs cannot use on the object §4 has (clause 2).

---

## 1. Definitions

Leg 382's instrument certifies
`P_cert(f, R₀, R₁) = { p ≥ 0 : ∃ C > 0, C·r^{−p} = f(r) ∀ r ∈ [R₀, R₁] }`
by exact Fourier–Motzkin elimination of `log C` from an outward-rounded interval enclosure of
the log–log tube. Verdicts `INTERVAL` / `EMPTY` (a proof of a negative) / `INCAPACITY`.

The mode this leg pre-registers and lands:

    P_cert^δ(f, R₀, R₁) = { p ≥ 0 : ∃ C > 0,  f(r)/(1+δ) ≤ C·r^{−p} ≤ f(r)·(1+δ)  ∀ r ∈ [R₀,R₁] }

`δ = 0` recovers `P_cert` exactly and remains the **default**. A nonempty interval is still not
proof of a power law — it is the statement that no exponent outside it is consistent within `δ`.

## 2. The width law (clause 1a) — derived, then measured

In the log–log plane with `t = log r`, `y = log f(r)`, a tolerance `δ` inflates the tube by
`h = log(1+δ)` on each side. Fourier–Motzkin over a window `[t₀, t₁]` gives half-width `2h`
per edge pair, hence

> **`width(δ) = 4·log(1+δ) / log(R₁/R₀)`**

pre-registered in PART I §2.1 with pass band `[0.95, 1.05]` on the ratio measured/predicted.

| quantity | measured | closed form | ratio |
|---|---|---|---|
| measured / predicted, all 10 rows (`δ = 1e-9 … 1e-1`, both windows) | — | — | **1.005051 – 1.005074** |
| small-`δ` coefficient on `[10, 1000]` | `0.87283702` | `4/log 100 = 0.86858896` | `1.004896` |
| small-`δ` coefficient on `[10, 100]` | `1.74566404` | `4/log 10 = 1.73717793` | `1.004887` |
| window ratio short/long | `1.9999989` | exactly `2` | `1.0000` |

**PASS.** The uniform `+0.51 %` is the cell-enclosure overhead, constant over nine decades of
`δ` — which is what makes this a law rather than a fit.

**Disagreement with leg 382's lead `0.8686`, reported as a disagreement:** measured
**`0.87284`, i.e. `+0.49 %` above the lead**. The substantive correction is not the digit. It is
that **`0.8686` is `4/log 100` — a property of the WINDOW — and it doubles to `1.7457` on
`[10, 100]`.** Any downstream threshold quoted at "`0.434` per unit `δ`" (half-width) is quoted
at a window, and leg 381's composition inherits that dependence silently. Panel (a) of `fig99`.

## 3. The critical tolerance (clause 1b + the fresh `δ*`)

Write `f(r) = C·r^{−p₀}·φ(r)`. In the log–log plane `P_cert^δ` becomes nonempty exactly when
the tube of half-width `h` admits an affine function through `log φ`, i.e. when
`h ≥ E∞(log φ)`, the Chebyshev best-affine approximation error. Hence

> **`δ* = exp(E∞(log φ)) − 1`**, with transition exponent `p_c = p₀ − b*` (`b*` the optimal
> affine slope).

PART I §2.2 predicted **in advance** that the measured `δ*` would land **below** this value,
because the cell enclosure is slightly wider than the exact tube, with band `±20 %`.

| id | profile | measured `δ*` | closed form | meas/pred | leg 382's lead | meas/lead − 1 |
|---|---|---|---|---|---|---|
| C1 | two-power `r^{−2} + 0.01 r^{−1}` | `0.31569700` | `0.318807` | `0.99024` | `0.315697` | `−5.4e-09` |
| C2 | rational cutoff `r^{−2}/(1+(r/300)^4)` | `3.35286818` | `3.454378` | `0.97061` | `3.352868` | `+5.5e-08` |
| C3 | log-corrected `r^{−2} log r` | `0.06973929` | `0.077025` | `0.90541` | `0.069739` | `+4.2e-06` |

**Two findings in opposite directions, both reported.** (i) **No disagreement with leg 382** —
the leads reproduce to `5e-9`/`5e-8`/`4e-6` relative; they were correct, they were simply not
yet earned, and they are now measured under a pre-registration. (ii) **A systematic `−0.98 %`,
`−2.94 %`, `−9.46 %` against this leg's own closed form**, in the predicted direction and
inside the band; the deficit grows as `δ*` shrinks, consistent with a fixed discretisation width
being a larger share of a smaller threshold. **The continuum formula is an upper bound on the
measured `δ*`, not an equality** — PART I did not say so and should have.

Certification at the freshly-measured `δ*` (N = 1000, mode `cells`, bracket `[0, 12]`):

| id | verdict | `[p_lo, p_hi]` | width | exact local-slope range | truth contained | `p_c` predicted |
|---|---|---|---|---|---|---|
| C1 | INTERVAL | `[1.49794908, 1.49794908]` | `2.220e-16` | `[1.090913, 1.909087]` | **yes** | `1.500000` |
| C2 | INTERVAL | `[3.03284150, 3.03284150]` | `1.332e-15` | `[2.000005, 5.967854]` | **yes** | `3.047509` |
| C3 | INTERVAL | `[1.76241212, 1.76241212]` | `2.220e-16` | `[1.565714, 1.855234]` | **yes** | `1.761439` |

Each interval lies inside the profile's own exact local-slope range — the instrument certifies
no exponent the profile never exhibits. **As pre-registered, none contains the nominal
`p₀ = 2`, and that is recorded rather than repaired**: a profile that is not a power law has no
true exponent, and the transition exponents match the closed forms to `0.0021` / `0.0147` /
`0.0010`.

## 4. `δ = 0` unchanged (1c) and the sub-`δ*` control (1d)

| known | `p₀` | width at `δ = 0` | 382's lead | ratio |
|---|---|---|---|---|
| K1 | 1 | `7.438494e-15` | `7.438e-15` | `1.00007` |
| K2 | 2 | `1.598721e-14` | `1.599e-14` | `0.99983` |
| K3 | 2.5 | `1.998401e-14` | `1.998e-14` | `1.00020` |
| K4 | 3 | `1.554312e-14` | `1.554e-14` | `1.00020` |

Truth contained in all four; a factor `10` was pre-registered as sufficient and a factor
`1.0002` was achieved. **The mode changed nothing at `δ = 0`.**

Sub-`δ*` control: at `0.9·δ*` and `0.5·δ*`, **6/6 EMPTY** (C1 `0.284127`/`0.157848`, C2
`3.017581`/`1.676434`, C3 `0.062765`/`0.034870`). Below its threshold every mismatch is still
*proved* impossible — the mode is not a knob, and leg 382's pinned "EMPTY at every `ε` down to
`1e-12`" regression test is untouched and still passing.

## 5. Clause 2 — the mechanism, measured rather than composed

§4's composition is: `α_lo = α_centre − 0.434·δ` must exceed `1` (fixed-ball energy, critical
`L³`) or `3/2` (global `L²`). Leg 381 read this as **H-381**: half-width `= 0.434·δ`, vanishing
at `δ = 0`, giving `δ < (α_centre − 1)/0.434`. PART I §4 registered the alternative **H-shift**:
half-width `= 0.434·(δ − δ*)`, vanishing at `δ*`. The discriminant, at `δ = 1.1·δ*`:

| id | `δ` | measured half-width | H-381 `0.434 δ` | meas/H-381 | H-shift | meas/H-shift |
|---|---|---|---|---|---|---|
| C1 | `0.347267` | `0.0203348` | `0.150816` | **`0.1348`** | `0.013711` | `1.483` |
| C2 | `3.688155` | `0.0743487` | `1.601745` | **`0.0464`** | `0.145613` | `0.511` |
| C3 | `0.076713` | `0.0056791` | `0.033316` | **`0.1705`** | `0.003029` | `1.875` |

**H-shift, by the pre-registered rule** (H-381 required `±10 %`; all three are below a seventh
of it). Stated precisely: **the intercept is confirmed — the half-width vanishes at `δ*`, not
at `0`** — while the near-transition slope coefficient is **not** `0.434` and is pinned only to
within a factor `0.51`–`1.88`.

**What this refutes.** H-381 implies a profile with `δ* = 3.35` needs
`α_centre > 1 + 0.434·3.35 = 2.456` before any tolerance is admissible. **Refuted.** Because
the half-width vanishes at `δ*`, the requirement is `α_centre > 1` and nothing more. Measured
`δ_max` against leg 381's law at threshold `1`:

| shape | `α_centre` | measured `δ_max` | 381's `(α_c−1)/0.434` | ratio |
|---|---|---|---|---|
| two-power | `1.497949` | `2.126079` | `1.146570` | `1.854` |
| two-power | `1.997949` | `8.772372` | `2.297862` | `3.818` |
| rational cutoff | `2.032842` | `9.658038` | `2.378205` | `4.061` |
| rational cutoff | `3.032842` | `10` (capped) | `4.680790` | `2.136` |
| log-corrected | `1.262412` | `0.804843` | `0.604226` | `1.332` |
| log-corrected | `1.762412` | `4.642082` | `1.755518` | `2.644` |

**Leg 381's law understates the admissible `δ_max` by `1.33×`–`4.06×` and never once claims a
window that is not there. It is conservative, not wrong-signed** — nothing built on it is
unsafe; it is simply tighter than the measurement requires.

## 6. Clause 2 — the answer, its window table, and its α-sensitivity

Measured directly by `cutoff_admissible_delta_window`, 3 shapes × `p₀ ∈ {1, 1.5, 2, 2.5, 3}` ×
thresholds `{1, 3/2}` = **30 rows**.

> **The window is non-empty if and only if the realised certified centre exceeds the threshold.
> 30 rows, 0 exceptions.** Six crossover probes at relative offset `1e-6` place the crossover
> exactly at the realised centre (admissible just below, EMPTY just above). **`δ` buys ZERO
> headroom on the threshold**: widening `δ` moves the LEFT edge of what can be certified and
> never moves the centre.

| shape / `p₀` | `α_centre` | window at `1` | width | window at `3/2` | width |
|---|---|---|---|---|---|
| two-power 1.0 | `0.497949` | **EMPTY** | — | **EMPTY** | — |
| two-power 1.5 | `0.997949` | **EMPTY** | — | **EMPTY** | — |
| two-power 2.0 | `1.497949` | `[0.315697, 2.126079]` | `1.810` | **EMPTY** | — |
| two-power 2.5 | `1.997949` | `[0.315697, 8.772372]` | `8.457` | `[0.315697, 2.126079]` | `1.810` |
| rational cutoff 1.0 | `2.032842` | `[3.352868, 9.658038]` | `6.305` | `[3.352868, 5.570913]` | `2.218` |
| log-corrected 1.0 | `0.762412` | **EMPTY** | — | **EMPTY** | — |
| log-corrected 1.5 | `1.262412` | `[0.069739, 0.804843]` | `0.735` | **EMPTY** | — |
| log-corrected 2.0 | `1.762412` | `[0.069739, 4.642082]` | `4.572` | `[0.069739, 0.804843]` | `0.735` |

(Representative rows; all 30 in the JSON. `δ_max = 10` rows are capped at the search ceiling and
flagged `capped`. Panel (b) of `fig99`.)

**α-sensitivity, stated as §4's consumers need it: the dependence is A STEP, NOT A SLOPE.** The
window is empty for every `α_centre ≤ threshold` and non-empty for every `α_centre > threshold`,
uniformly across all three mismatch shapes, and once open it is **wide** (`0.735` to `≥ 9.93`
in `δ`). **At `α_centre = 1` it is EMPTY; at `α_centre = 1.0001` it is non-empty.** So the
answer does not vary shape-to-shape at fixed realised α — it varies only across the threshold,
and the question §4 must ask is not "how accurate is the profile" but "**does the certified
centre clear `1` (or `3/2`) at all**".

**The nominal-vs-realised trap, disclosed in full.** One row — the rational cutoff at nominal
`p₀ = 1` — is admissible, and a **nominal** reading of the α ladder would have returned
**ADMISSIBLE** for clause 2 on the strength of it. It is not admissible at `α = 1`: the
measurement window `[10, 1000]` **contains** its cutoff at `r = 300`, so it realises
`α_centre = 2.0328`. PART I §4 fixed the decision at the **realised** α before any measurement
("the clause is decided at the α actually realised and not at a nominal one"), precisely so this
could not be counted. The JSON records both (`nominal_p0_reading`: 1 admissible shape;
`realised_alpha_reading_OPERATIVE`: 0). **The verdict flipped ADMISSIBLE → EMPTY when the
pre-registration was honoured.** That is a faithfulness fix in the stricter direction, not a
post-hoc rescue; no band was widened, and no rescue is reported as gate-deciding.

## 7. TEXT ROUTED TO INTEGRATION — two files this leg may not edit

Both are integration-owned. **Neither has been touched by this leg.** The exact proposed text
follows.

### 7.1 `CLAY_OBLIGATIONS.md` §4 — proposed replacement for the paragraph beginning "**§4 IS NOT DISCHARGED BY A δ = 0 CERTIFICATION (user ruling, 2026-08-11).**"

> **§4 IS NOT DISCHARGED BY A δ = 0 CERTIFICATION (user ruling, 2026-08-11); THE δ QUESTION IS
> NOW ANSWERED, AND THE ANSWER IS EMPTY AT THE α IN PLAY (leg 386, DTOL).** The admissible
> cutoff radius is a function of the *certified* exponent, so a certification carrying a
> tolerance `δ` passes that tolerance into the cutoff bound. Leg 386 pre-registered the δ mode
> before running and measured the composition directly rather than composing two legs' laws.
> **Three corrections to what was written here.** (i) The width law is
> `width = 4·log(1+δ)/log(R₁/R₀)`; leg 382's `0.8686` is `4/log 100`, **a property of the
> window**, doubling to `1.7457` on `[10,100]` — any half-width quoted at `0.434` per unit δ is
> quoted at a window. (ii) Leg 381's `δ < (α_centre − 1)/0.434` is **conservative by
> `1.33×`–`4.06×`** on every measured row and never optimistic; its implied demand
> `α_centre > 1 + 0.434·δ*` (≈ `2.456` at `δ* = 3.35`) is **REFUTED** — the certified half-width
> vanishes at `δ*`, not at `δ = 0`, so the requirement is just `α_centre > 1`. (iii) **The
> tolerance buys ZERO headroom on the threshold.** Over 30 measured configurations (3 mismatch
> shapes × 5 exponents × thresholds `{1, 3/2}`) the admissible window
> `D = { δ ≥ 0 : INTERVAL and p_lo > α_threshold }` is non-empty **if and only if** the realised
> certified centre already exceeds the threshold — **0 exceptions**, crossover located at the
> centre to `1e-6`. The dependence on `α_centre` is **a step, not a slope**; once open the
> window is wide (`0.735` to `≥ 9.93` in δ). **The banked Type-I object carries `α = 1`, so its
> composed δ window is EMPTY** — and would be at any `α_centre ≤ 1`. The load-bearing question
> for §4 is therefore **not** the certification tolerance but whether a certified `α_centre`
> exceeding `1` (or `3/2`) can be produced at all; **no profile of route 4's object exists in
> this repository**, and leg 386 contributes nothing to that question. **§4's δ sub-question is
> CLOSED (answer: EMPTY at α = 1). §4 itself remains OPEN**, on the admissible-cutoff half and
> on the missing profile. **Method status: NO KNOWN METHOD IN THIS REPOSITORY.** Named in §6.

*(Integration note: the standing "Until DTOL lands, §4 stays OPEN in every route-4 gate" clause
is satisfied on its own terms — DTOL has landed with a pre-registered δ mode — but §4 does not
thereby close, and PROG-R4 should keep it open on the two grounds named in the last sentence,
not on leg 386's account. §6 items 1 and 2 stay OPEN in every branch.)*

### 7.2 `capabilities.py` — APPLIED IN THIS LEG'S COMMIT, not routed

The coordinator's mid-leg amendment directed that a `validated`-text update belonging to this
leg's own module ship **in the same commit as the module change** — the standing rule adopted
after a mid-rebase `HEAD` published a solver module without its capability row and reddened
`test_every_solver_module_is_indexed` for every agent. The `solver/dssp_decay_enclosure.py`
entry's `holds` and `validated` texts were therefore edited here (test count `12/12 → 18/18`,
the fresh width-law and `δ*` numbers, the zero-headroom limit, the refuted α demand, and the
hypothesis-field contract). Its CEILING sentence stands unchanged and still applies.


## 7bis. THE HYPOTHESIS FIELD — the standing rule, implemented here

A mid-leg amendment adopted a standing rule on every consumer of the enclosure chain:
**every output row carries the hypothesis in force; a certificate-without-hypothesis is no
certificate.** It is earned rather than hygienic. Leg 385's control X3 planted a **secret**
monotonicity violation and was accepted — as it must be, the hypothesis being caller-declared
and unverifiable from samples — and the certificate it produced had width
**`7.438494264988549e-15`, bit-indistinguishable from the true certificate of the genuine
planted known K1**. Same width, false about its profile. Only the recorded hypothesis
separates them.

**What this leg shipped.** `hypothesis` / `hypothesis_detail` / `conditional_on` are now
present on **every return path of every function** in `solver/dssp_decay_enclosure.py`, bound
in the same breath as `δ` and **before any early return**, so no path can emit a row whose
tolerance *or* whose hypothesis is implicit. Specifically:

| path | hypothesis recorded | why |
|---|---|---|
| `certified_decay_interval(..., mode="cells")` | `EXACT-INTERVAL-EVALUATION` | **discharged, not declared** — outward-rounded evaluation over whole cells *establishes* the enclosure |
| `certified_decay_interval(..., mode="nodes")` | `NODES-ONLY` | the weaker mode now **declares its own weakness in the row**, not only in the docstring |
| `certified_decay_from_cell_enclosures(...)` with an upstream declaration | passed through unmodified (`MONOTONE` / `MODULUS` / `MONOTONE+MODULUS`) | byte-identical to leg 385's adapter strings, pinned by a test against drift |
| the same, with none supplied | `UNDECLARED` | **never absent, never silently forgiven**; `conditional_on` states plainly that the row is not a certificate about any profile |
| all three `INCAPACITY` paths, including the zero-crossing early return | recorded | that return was the one that had already been found dropping `rel_tolerance` |
| `cutoff_admissible_delta_window(...)` | inherits `EXACT-INTERVAL-EVALUATION` | a composed window is **exactly as conditional as the certifications it composes**, and must not launder that away by being one level further from the arithmetic |

The dependency deliberately points one way (adapter → enclosure, never back), so the three
shared strings are duplicated rather than imported and `test_hypothesis_strings_match_the_adapter`
fails loudly if leg 385's module renames one.

**No measurement changed.** The runner was re-run in full after the amendment; every number in
this document, in `fig99` and in the JSON is bit-for-bit what it was before (`δ*` to all 17
digits, ratios `1.005051–1.005074`, both coefficients, both gate answers). The field is an
addition to what each row *says*, not to what the instrument *computes*.

**A related result cited rather than rediscovered** (leg 385, banked): prediction P11 was
**REFUTED and recorded as refuted** — a shifted grid does *not* detect a node-aligned wiggle,
because a uniform shift multiplies every sample by one constant; detection is a
**commensurability** effect (`N = 1100`, `1500` refuse; `500`, `997`, `1001`, `1010`, `2000` do
not), so **a violating profile can hide from any fixed grid**. Also banked: a globally-stated
`absolute` modulus is unusable across three decades (341/1000 cells non-positive from
`r = 207.97`) and must be stated in log–log. Neither bears on how `δ*` was measured here — this
leg's inputs are interval-evaluated closed forms, never samples, which is exactly the case that
records `EXACT-INTERVAL-EVALUATION` — but both bear on any caller who arrives with samples, and
they are why the `UNDECLARED` row says what it says.

## 8. Anti-tautology checks (9/9) and reproduction

1. No planted known returns the full `[0, 12]` bracket at any δ ✔
2. No exact power law is ever certified EMPTY (4 exponents × 4 tolerances) ✔
3. Every mismatch is EMPTY at `δ = 0` ✔
4. δ recorded on every row ✔ — **4b, on the INCAPACITY paths specifically ✔**; this closed a
   real gap in leg 382's module, whose zero-crossing early return dropped `rel_tolerance`
5. Widths non-decreasing in δ; EMPTY downward-closed ✔
6. Hypothesis recorded in every row ✔ — **6b: the hypothesis separates what the width cannot**
   ✔ (a cells row and a nodes row of the *same* profile carry different hypotheses, and an
   undeclared caller comes back `UNDECLARED` rather than inheriting one it never declared);
   **6c: the composed window carries the hypothesis it was composed from** ✔

```
.venv/bin/python experiments/p2_route_dtol_v1.py            # ~61 s -> writeup/data/p2_route_dtol_v1.json
.venv/bin/python experiments/p2_route_dtol_v1_evidence.py   # JSON only -> fig99
.venv/bin/python test_dssp_decay_enclosure.py               # 18/18
```

## 9. Deviations, disclosed

1. **`p₀ = 1.25` dropped** from the pre-registered clause-2 ladder: the planted generators go
   through `ipow_half_integer`, which accepts only half-integers by leg 382's deliberate design.
   A limit of the planted profile, not of the enclosure (which searches the continuum). Nothing
   in either clause turns on it — the step is located to `1e-6` by the crossover probes.
2. **Two files beyond the literal territory list**, both under this route's own name:
   `experiments/p2_route_dtol_v1_evidence.py` (required convention for a registered figure) and
   this BLOG/TECHNICAL pair.
3. **`CLAY_OBLIGATIONS.md` NOT edited** (forbidden) — exact proposed text routed in §7.1 above.
   **`capabilities.py` WAS edited**, in the same commit as the module change, under the
   coordinator's mid-leg amendment; this is a departure from the dispatch brief's literal
   territory list and is disclosed as one (§7.2).
3b. **The hypothesis field was added after the pre-registration was written**, under the same
   amendment. It is an addition to the interface, not to either gate clause, and the full
   re-run confirmed it changed no measured value. Neither clause was re-decided.
4. **External novelty endpoints refused** (arXiv and Semantic Scholar, both HTTP 429, banked
   verbatim in `writeup/novelty/leg_386.md` §3). No external prior-art result was obtained; no
   methodological novelty is claimed, so nothing rests on it, but the hole is real and open.

## 10. Interface for leg 389 (CT2C), which consumes this mode

Argument **`rel_tolerance`** (name deliberately unchanged from leg 382 — it is
capability-indexed and has a consumer), **default `0.0`**, `float`, `ValueError` on `< 0`,
validated and bound **before any early return**. Arguments **`hypothesis`** and
**`hypothesis_detail`** on `certified_decay_from_cell_enclosures`, both defaulting to `None`
and both recorded (as `UNDECLARED`) rather than dropped. Recorded on every row:
`rel_tolerance`, `tolerance_mode ∈ {"exact", "relative"}`, `predicted_width_exact_power_law`,
`hypothesis`, `hypothesis_detail`, `conditional_on`. **Read `hypothesis` before `width`** —
§7bis is the reason. Helpers exported:
`predicted_width(delta, r0, r1)` (float reference, **never a certified bound**) and
`cutoff_admissible_delta_window(...) -> {admissible, delta_min, delta_max, width,
alpha_threshold, alpha_centre, p_lo_at_delta_min, delta_star_lo/hi, capped, reason, config}`.

**Still owed, and not by this leg:** the samples→cells conversion (a caller with pointwise
samples needs a certified modulus of continuity or a stated monotonicity hypothesis); a sharp
near-transition half-width law (the H-shift intercept is confirmed at `δ*`, its slope
coefficient is pinned only to a factor `0.51`–`1.88`); and an `α_centre` for the actual object.
