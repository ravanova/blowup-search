# PROG-R4, unit E — THE H-HARD DIAGNOSTIC

**Programme:** PROG-R4 (leg 380). **Lane R**, wave-1 item 4. **Unit kind: INSTRUMENT.**
**Mode:** CONDUCTOR (`ORCHESTRATION.md` §3g), dispatched worker, self-terminating.
**Ruled by the user 2026-08-13:** `PROG-R4` takes U5 §9 option **E**. This unit runs it.
**The answer below is UNVERIFIED** in the repository's sense: produced in one session, no
paired verifier. Wave 2 carries the verifier (§3g).

**§3f rule 3.** This is an instrument task, permitted here because U5 was construction, and
**it cannot be followed by another one** — wave 2 may not queue a second instrument/audit/repair
unit before a mathematics or construction unit.

---

## 0. PRE-REGISTRATION — committed BEFORE the first attempt ran

**Sections 0 through 4 of this journal, and the whole of
`experiments/programme_r4/e_hhard_diagnostic.py`, were committed to
`prog-r4/e-hhard` before any attempt was run.** The commit order is the evidence, and it is
the only thing that makes the reading below a reading rather than a story assembled after the
numbers. Sections 5 onward were written after the run and record what happened.

## 1. THE PRIOR, STATED UP FRONT AND NOT REDISCOVERED

**Leg 353 already attempted five of these rows and all five failed.** UPO37 (×2), UPO35, UPO9
and UPO22, seeded from the best recurrence-search candidates at relative seed residual 0.18–0.26,
every one exiting `reason=line_search_failed` with final `‖R‖` in **[22.5, 29.5]** — no attempt
within two orders of magnitude of `tol=1e-8`, and the basin radius never measured
(`writeup/data/p2_route_dsspb5_v1.json`, `experiments/journal/leg_353.md`, and the capability
index's own entry for `solver/kolmogorov2d_nkbasin.py`).

**That is the prior this unit's result must agree or disagree with. It is not a reason to skip
the unit, because leg 353 was under-resourced and ran a different realization**, and the two
differences are named here, before the run, rather than discovered afterwards:

| | leg 353 | unit E |
|---|---|---|
| **DNS supplying the field** | `T_total = 2000` | **`T = 1e5`** (U2, MILESTONE M2) — 50× longer, so the near-recurrence supply at any published `(T, s)` is a different and far larger object |
| **globalisation** | `newton_krylov_rpo` — plain Newton, **step-halving line search** | **`newton_hookstep_rpo`** — the genuine Viswanath trust-region hookstep U1 built as MILESTONE M1, which **rotates** the step inside the Krylov subspace instead of merely rescaling it. `line_search_failed` is not a reachable exit reason here at all |

**If this run reproduces leg 353's failure at the same budget, this journal says so in those
words.** It does not get to call the same outcome a new result because the apparatus changed.

## 2. THE GATE, IN ITS FINAL WORDING — NOT RE-SCOPED

> On the 200 banked attempts, do all three named diagnostics return, each with a planted control
> demonstrated firing in **both** directions: **(1)** the converged-`|s|` distribution against
> seed `|s|`; **(2)** whether the low-`|s|` solutions are attractors of the **hookstep iteration**
> or of the **minimisation**; and **(3)** whether the named Table IV rows are reachable **at all**
> when seeded directly at their published `(T, s)`?
> **yes →** report all three.
> **no →** name which diagnostic the banked data cannot support, and what it would take — a cost,
> not a verdict (§3d).

**The gate is about the DIAGNOSTICS RETURNING, not about convergence. A clean non-convergence
with working controls is a PASS of this gate.** The run is not steered.

## 3. THE FOUR PRE-COMMITTED BRANCHES — fixed on `main` before dispatch, carried verbatim

Reproduced from `STATE.md` (WAVE 1, item 4) so that this file can be read alone. **No fifth
branch is constructed.**

- **E-i — direct seeding CONVERGES to the named row** (within the matching predicate's own 0.05
  tolerance). The named rows *are* solutions of this discrete map at achievable tolerance and the
  failure is one of basin size / seed reachability. Refutes the **strong** form of H-hard,
  promotes **R3** (multiple shooting) and **U4/G2** (basin radius). **`G1` STAYS
  `UNDER-RESOURCED` AND DOES NOT BECOME A RECOVERY** — a hand-placed seed at published
  coordinates is not a mined seed and does not answer the question G1 asks.
- **E-ii — it does NOT converge at any published row.** The rows are unreachable even from their
  own published coordinates, so the obstruction is in the **REALIZATION, NOT THE SEARCH**. Points
  at **R4** (U3's stepper is Lie–Trotter, globally first order, measured global ratio 2.00, so its
  periodic orbits are `O(dt)` perturbations of the true flow's) and would be the **first evidence
  in this programme that the realization rather than the budget is what G1 has been measuring**.
  **Still NOT a `no` under §3d**: reported as a measurement of *this realization at this budget*,
  with the compliant scale named and costed.
- **E-iii — it converges to something ELSE** (a different orbit, or drifts to `|s| < 0.15`). The
  basin-structure finding of U5 §9 reappearing **at the strongest possible seed quality**, the
  sharpest available form of U5's result; no amount of seed quality fixes this. Points at
  `R3`/`R2`. Reported with the distance from the published row quantified.
- **E-iv — the instrument limit.** A published row supplies `(T, s)` but **NOT A FIELD.** This
  unit must state exactly what it planted, in what basis, at what resolution, and what the
  published row did and did not determine, and **must not describe a field-plus-pinned-`(T,s)`
  seed as "seeding at the published orbit."** If the instrument limit dominates, that is branch
  E-iv and it is a legitimate outcome.

**On diagnostic (2):** if the low-`|s|` solutions are attractors of the **minimisation** rather
than of the hookstep, **the fix is in the SCORE, not the solver, and not in more seeds** — and
**leg 349's ban binds the repair to stay DETERMINISTIC.** Name it; do not build it.

## 4. WHAT WAS PLANTED — branch E-iv's discipline, applied in advance

**A published Table IV row determines `(T, s, m)` and nothing else. It does not determine a
field.** Every attempt in diagnostic (3) therefore plants a **field drawn from this repository's
own DNS together with `(T, s)` pinned at the published values**. That is a
**field-plus-pinned-`(T,s)` seed**, and no sentence anywhere in this unit calls it "seeding at
the published orbit."

| what | exactly what was planted |
|---|---|
| **basis** | real vorticity `w(x, y)` on a uniform **24 × 24** collocation grid — the state variable of `solver/kolmogorov2d_nkbasin.Kolmogorov2D` (2/3-rule dealiased pseudospectral, `Re = 60`, forcing `n = 4`, `dt = 0.01`, Lie–Trotter split, **globally first order in time**) |
| **field** | an exact bit-for-bit re-integration (`u2_m2_dns_recurrence.regenerate`) of one snapshot of U2's `T = 1e5` trajectory, selected by the rule below |
| **`T`** | the **published period, exactly** — not the candidate's measured period, which is quantised to the 0.25 snapshot spacing |
| **`s`** | **±** the published shift wrapped to `(-π, π]`. **The sign is MEASURED, not assumed**: both signs are evaluated in the extended residual and the smaller is taken, exactly as U3 and U5 do — this module already cost the repository one real sign bug (leg 353's FFT cross-correlation peak sits at `j = -s`) |
| **`m`** | 0. All eight named rows have `m_published = 0`, and the extended residual carries a continuous `x`-shift only, so the `m ≠ 0` class cannot be expressed at all |

**Seed-selection rule, fixed before the run.** For each named row, from the **full `m = 0`
candidate set** of U2's banked library (2,014 candidates, 1,153 with `m = 0`) restricted by U3's
own anchor rule `|T_c − T_pub| ≤ 1.0`:

- **arm S — "shift-matched field":** among candidates whose measured `|s|` agrees with the
  published `|s|` to within **the matching predicate's own 0.05**, take the **lowest recurrence
  score `R`**; if that subset is empty, minimise `| |s|_c − |s|_pub |`.
- **arm Q — "score-optimal field":** take the **lowest `R`** outright — U3's own ranking, i.e.
  the field U3 would have chosen for that row.

**No field is reused** across the 16 attempts. **The `R < 0.25` Newton admission window is
DELIBERATELY NOT APPLIED.** U3 §5 measured that window to be monotone in the very coordinate the
targets are separated on (rank correlation `|s|`↔`R` = 0.50; 44% admitted below `|s| = 0.15`
against 11% in the published band), so it is the biased filter, and **this is the unit entitled
to ignore it. Neither U3 nor U5 ever ran a seed from outside it.**

**Solver and budget, held at U5's values and imported rather than copied** so the algorithm is
identical to the one the 200 banked attempts ran under: `tol = 1e-8`, `max_newton = 52`,
`max_gmres = 140`, `gmres_rtol = 1e-3`, `fd_eps = 1e-6`, and U5's pre-registered stall exit
(`k ≥ 20`, window 10, threshold 0.5). The stall rule is **re-validated in this unit against both
banked ledgers** before being used again: it must kill **zero** attempt either unit's record shows
converged.

**The matching predicate is U3's, applied unchanged**: a convergence is a recovery only if it
matches a named row on **both** `T` and `s` (mod 2π) to within 0.05. A sign-agnostic `|s|` variant
is computed and reported **as SECONDARY only**, because the published shift's sign convention
relative to this realization's is not established by anything in the repository; **no verdict
rests on it.**

**Compliance statements, made before the run.**

- **Leg 349's ban (`GA compute on an unvalidated fitness`) is COMPLIANT and is not approached.**
  Every score this unit touches is **deterministic and pre-existing**: U2's recurrence score `R`,
  and the solver's extended residual `‖R‖`. **Nothing is fitted, learned, evolved or tuned to an
  outcome, and this unit proposes no learned or evolved seed-scoring fitness.** If diagnostic (2)
  returns a minimisation attractor, the repair is *named* as a score repair and left deterministic
  and unbuilt.
- **Ceiling TIER 2.** Nothing here is a proof, nothing is described as movement toward Clay, no
  `L1 → L4` link moves, **Clay stays ~0.05%**. A best-in-field orbit finder makes the questions
  affordable; that is a different and lesser thing, and Lane R's write-ups say so.
- **Lesson 91.** This unit's negative, if it has one, names: *this discretization (`N = 24`,
  `Re = 60`, `n = 4`), this resolution, this stepper (Lie–Trotter, globally first order), this
  hookstep solver, this budget (16 attempts, `max_newton = 52`, `tol = 1e-8`).*
- **§3d.** A non-convergence at this budget is **not** a `no` about the named rows in general. It
  is a measurement of **this realization at this budget**, and the scale at which the question is
  properly posed is named and costed in §8.
- **No new DNS, no new seed mining, no new solver construction.** The existing hookstep solver is
  used as built; `solver/kolmogorov2d_nkbasin.py` is untouched.
- **No external outreach** (standing user hold). **`DIRECTION.md` was not read** (§3e).

---
## 5. DIAGNOSTIC (1) — WHERE THE CONVERGED `|s|` SITS AGAINST THE SEED `|s|`

**RETURNED. Verdict: `PULL_TO_LOW_S`. Controls fired BOTH ways.**

Over the **200 banked attempts** (U3's 100 and U5's 100, read and never edited), **23 reached
`tol = 1e-8`** — 14 in U3, 9 in U5. The pre-registered classifier fires `PULL_TO_LOW_S` only if
**all three** of its clauses hold, and all three do:

| clause | measured |
|---|---|
| median drift `|s|_conv − |s|_seed` **< 0** | **−0.03202** (mean −0.06880) |
| at least half of convergences finish below `|s| = 0.15` | **21 of 23 = 91.3%** |
| exact two-sided sign test on the drift, `p < 0.05` | **17 down / 6 up, p = 0.0347** |

Seed `|s|` of those 23 spans `[0.0061, 0.6187]`; converged `|s|` spans `[0.0729, 0.5867]`.
Spearman(seed `|s|`, converged `|s|`) = **0.3205** — the seed shift explains rather little of
where the solve lands. **6 in-band seeds converged and 5 of them left the band**, which is U5 §9's
band-exit count reproduced here from the pooled record.

**The SECONDARY reading over all 200 attempts** — counting the terminal `|s|` of the 177 attempts
that never reached `tol` — returns **`NO_PULL`**, and it is reported because it is the honest
counterweight: the drift is still negative (median −0.0239, 120 down / 80 up, `p = 0.0057`) but
only **38.5%** of attempts finish below `|s| = 0.15` and Spearman rises to **0.793**. **A
non-converged attempt has not landed anywhere**, so its terminal `|s|` is mostly its seed `|s|`;
that is exactly what the higher Spearman says. **The pull is a property of the solutions this
realization actually reaches, not of the trajectory of every attempt.** Neither reading is
suppressed.

**Controls (planted, fired both ways).** Positive: converged `|s| := 0.10` for every attempt →
`PULL_TO_LOW_S` (100% below 0.15). Negative: converged `|s| := ` seed `|s| ± 0.001` → `NO_PULL`
(`p = 1.0`, Spearman 0.9985). `fired_both_ways = true`. **The classifier can say both words**, so
its saying `PULL_TO_LOW_S` here is a measurement and not a foregone conclusion.

## 6. DIAGNOSTIC (2) — ITERATION OR MINIMISATION?

**RETURNED. Verdict: `MIXED`. Controls fired BOTH ways.**

The pre-registered split: an accepted Newton epoch is **`constrained`** if its accepted hookstep
trial sits **on the trust-region boundary** (`on_boundary = True`, i.e. the *minimisation* chose
the step) and **`unconstrained`** if the full Newton step was taken (`on_boundary = False`, i.e.
the *iteration* chose it). Over **2,195 accepted epochs**:

| | constrained | unconstrained |
|---|---|---|
| **epochs** | **2,131 (97.1%)** | **64 (2.9%)** |
| **mean per-epoch `d|s|`** | −0.002695 | −0.001842 |
| **net `Σ d|s|`** | **−5.7431 (98.0% of the total descent)** | −0.1179 |

**The observed difference in per-epoch rate is −0.000853 with a within-attempt label permutation
`p = 0.9317`** (20,000 permutations, `PERM_SEED = 380`). **The rates are statistically
indistinguishable**, so the pre-registered rule returns **`MIXED`** and this unit does not get to
say "the minimisation is dragging the solve to low `|s|`."

**What the numbers do say, stated carefully.** 98.0% of the total `|s|` descent happens on
constrained epochs **because 97.1% of accepted steps are constrained at all**, not because a
constrained step descends in `|s|` faster than an unconstrained one. **In this realization the
full Newton step is almost never taken** — the trust region binds on 29 accepted steps out of
every 30. The per-epoch correlation between `Δ‖R‖` and `d|s|` is **+0.1954**: epochs that descend
in residual tend, weakly, to descend in `|s|` as well.

**THE BAN, CONFIRMED.** Because diagnostic (2) did **NOT** return `MINIMISATION_ATTRACTOR`, the
commissioned conditional — "if the score is the attractor, the fix is in the SCORE" — **does not
fire**, and nothing is proposed. Independently: **leg 349's ban is COMPLIANT and was never
approached.** Every score this unit touched is deterministic and pre-existing (U2's recurrence
score `R`; the solver's extended residual `‖R‖`). **Nothing was fitted, learned, evolved or tuned
to an outcome, and this unit proposes no learned or evolved seed-scoring fitness.**

**The score's own `|s|` bias, re-derived here independently** from U2's library (1,153 `m = 0`
candidates), because it is the standing context for both diagnostics: **Spearman(`|s|`, `R`) =
0.5012**, and the fraction admitted by the `R < 0.25` window falls monotonically across the four
`|s|` bands — **43.79% / 20.19% / 11.53% / 2.86%** for `|s| ∈ [0, 0.15) / [0.15, 0.295) /
[0.295, 0.707) / [0.707, π]`. That reproduces U3 §5's 0.50 and 44/20/11/3 from the library rather
than from U3's table. **The published band is the third of those four cells.**

**Coverage limit, declared in the pre-registration and not discovered afterwards.** The per-epoch
`|s|` path exists for **U5's 100 attempts only**: U3's banked ledger records no `T_before` /
`s_before`, because those fields were added to the solver's hookstep ledger after U3 ran. **Cost
to close: re-running U3's 100 attempts under the current ledger = 4,629 epochs × 95 s = 122.1
core-hours, 15.3 h wall at 8 workers.** Not bought here, not needed for this gate, and named
rather than hidden.

**Controls (planted, fired both ways).** A synthetic run with `d|s| = −0.02` on constrained
epochs only → **`MINIMISATION_ATTRACTOR`** (`p = 0.0005`); the same with the labels swapped →
**`ITERATION_ATTRACTOR`** (`p = 0.0005`). `fired_both_ways = true`. **The classifier can say
either word**, which is what makes `MIXED` a reading rather than a shrug.

## 7. DIAGNOSTIC (3) — SEEDING DIRECTLY AT THE EIGHT PUBLISHED ROWS

**RETURNED. 16 attempts, 2 converged, 0 recovered their own named row, 0 recovered ANY named row,
0 secondary sign-agnostic `|s|` matches. Controls P/N/R fired as planted, with no failures.**

**Read §4 first.** What was planted was a **field-plus-pinned-`(T,s)` seed**, sixteen of them, one
per (row, arm). **No sentence below means "we seeded at the published orbit," because nothing in
this repository can do that**: a Table IV row supplies `(T, s, m)` and no field.

| row | arm | `R` seed | seed `‖R‖` | final `‖R‖` | epochs | `T` final / pub | `|s|` final / pub | exit |
|---|---|---|---|---|---|---|---|---|
| UPO37 | S | 0.1371 | 20.06 | 6.041 | 20 | 20.448 / 19.334 | 0.3951 / 0.3750 | stalled |
| UPO37 | Q | 0.1108 | 33.02 | 4.355 | 20 | 19.425 / 19.334 | 0.2404 / 0.3750 | stalled |
| UPO35 | S | 0.4780 | 38.61 | **9.669** | 20 | **18.876 / 18.912** | **0.6218 / 0.7072** | stalled |
| UPO35 | Q | 0.0836 | 54.94 | **4.83e-09** | 22 | 22.036 / 18.912 | 0.1349 / 0.7072 | **converged** |
| UPO34 | S | 0.1710 | 36.20 | 10.32 | 20 | 18.348 / 18.878 | 0.3183 / 0.4180 | stalled |
| UPO34 | Q | 0.1120 | 47.80 | 1.814 | 26 | 17.440 / 18.878 | 0.1965 / 0.4180 | stalled |
| UPO32 | S | 0.2167 | 28.86 | 5.875 | 20 | 17.900 / 18.694 | 0.6054 / 0.4340 | stalled |
| UPO32 | Q | 0.1240 | 31.21 | 1.135 | 23 | 19.282 / 18.694 | 0.0541 / 0.4340 | stalled |
| UPO22 | S | 0.1833 | 25.74 | 0.804 | 24 | 16.847 / 17.160 | 0.3893 / 0.3610 | stalled |
| UPO22 | Q | 0.0866 | 47.04 | 3.272 | 25 | 16.858 / 17.160 | 0.0497 / 0.3610 | stalled |
| UPO20 | S | 0.1362 | 23.98 | 2.668 | 20 | 17.880 / 16.908 | 0.4665 / 0.5530 | stalled |
| UPO20 | Q | 0.1383 | 54.87 | 0.978 | 31 | 17.745 / 16.908 | 0.6150 / 0.5530 | stalled |
| UPO17 | S | 0.1852 | 29.29 | 2.280 | 20 | 17.549 / 16.753 | **0.0032** / 0.4820 | stalled |
| UPO17 | Q | 0.1387 | 38.08 | 1.758 | 20 | 17.617 / 16.753 | 0.3147 / 0.4820 | stalled |
| UPO9 | S | 0.1945 | 22.19 | 3.580 | 20 | 14.466 / 14.776 | 0.4289 / 0.2950 | stalled |
| UPO9 | Q | 0.1239 | 24.27 | **2.06e-10** | 12 | 16.537 / 14.776 | 0.0994 / 0.2950 | **converged** |

Sign tally over the 16 seeds: **`{plus: 5, minus: 11}`** — the sign was measured per seed, never
assumed. **One seed (UPO35 arm S, `R = 0.478`) sits OUTSIDE the `R < 0.25` Newton admission
window**; that seed is exactly the point of arm S and is the one U3 and U5 were structurally
incapable of running.

**The two convergences are not recoveries and are not close to being recoveries.**

- **UPO35 arm Q** → `‖R‖ = 4.827e-09` in 22 epochs at `T = 22.0358` (published 18.912, **ΔT =
  3.124**) and `|s| = 0.1349` (published 0.7072, **Δs = 0.572**).
- **UPO9 arm Q** → `‖R‖ = 2.055e-10` in 12 epochs at `T = 16.5369` (published 14.776, **ΔT =
  1.761**) and `|s| = 0.0994` (published 0.295, **Δs = 0.394**).

**Both landed at low `|s|`** — 0.13 and 0.099, both under diagnostic (1)'s 0.15 shelf, from seeds
pinned at 0.707 and 0.295. **That is diagnostic (1)'s pull reappearing at the strongest seed
quality this programme can construct**, and it is the single most informative line in this unit.

**Closest approach to a published row: UPO35 arm S, `ΔT = 0.0362`, `Δs = 0.0854`, final `‖R‖ =
9.669`.** It is inside the matching box on `T` and just under twice the tolerance out on `s` — and
it is a **STALLED attempt with a residual of ten, not a solution.** Being near a published row in
`(T, s)` and being a solution of this realization are, on this evidence, different things.

**Exit reasons: `{stalled: 14, converged: 2}`. Not one attempt hit the iteration cap.** All 14
stopped at U5's pre-registered stall exit, at 20–31 epochs out of 52 available. **"More Newton
iterations" is therefore not the obviously-missing resource** — the residual stopped falling
before the budget ran out.

**Arm S starts closer and finishes further, for 8 rows out of 8.** The shift-matched field has the
lower seed residual in every single row (that is what selecting on `|s|` buys), yet arm Q's mean
final residual is **1.66** against arm S's **5.15**, and **both convergences are arm Q**. In this
realization the recurrence score `R` — a quantity that knows nothing about the published rows —
predicts Newton progress better than agreement with the published shift does.

**Instrument fact for branch E-iv, stated plainly: the seed residuals are `[20.06, 54.94]`**,
against `≈14–19` for the mined seeds U3 and U5 actually ran. **Planting at the published `(T, s)`
produced a WORSE starting point than the repository's own mining does.** That is not a defect of
the rows; it is the direct measurement of the fact that **the row does not supply the field**, and
it is the cost of E-iv's honesty.

**Controls (planted, fired as planted).**

| control | role | result |
|---|---|---|
| **P** | positive, unconditional — MUST succeed. The exact relative-equilibrium fixed point in closed form (`‖Φ_dt(w*) − w*‖ = 7.6e-14`), perturbed 0.1% | **converged**, `‖R‖ = 7.75e-09`, 33 epochs |
| **N** | negative — MUST NOT succeed. Phase-scrambled field at the same `(T, s)` | **did not converge**, `‖R‖ = 51.46`, 51 epochs, `max_newton_hit` |
| **R** | positive, conditional — the harness must be able to say YES. A banked U5 convergence (`attempt007_P_UPO37`) perturbed and re-solved | **converged and MATCHED BACK**, `‖R‖ = 1.52e-10`, 5 epochs, `ΔT = 2.99e-07`, `Δs = 6.50e-08`, `harness_predicate_says_recovered = True` |

`fired_as_planted = True`, `failures = []`. **Control R is the one that matters for this unit's
negative**: it proves the matching predicate that returned 0 recoveries **is capable of returning
a recovery**, on this solver, at this tolerance, in this harness. **The zero is a measurement, not
a broken assertion.**

**The stall rule was re-validated before being trusted** (§4's precondition): replayed against
both banked ledgers it kills **zero** of U3's 14 and **zero** of U5's 9 convergences, worst
10-epoch ratio **0.0724** (U3) and **0.0606** (U5) against the 0.5 threshold — margin factors 6.9
and 8.2.

---
## 8. THE BRANCH THAT FIRED — E-iii

**E-iii fired: "converges to something else."**

Two attempts converged to genuine solutions of this realization at `‖R‖ ≈ 1e-9` and `1e-10`, and
**neither is the row it was planted at**: `ΔT = 3.124 / Δs = 0.572` for UPO35 arm Q and `ΔT = 1.761
/ Δs = 0.394` for UPO9 arm Q, against a matching box of `0.05 × 0.05`. **Both landed under
diagnostic (1)'s low-`|s|` shelf.** This is **U5 §9's basin-structure finding reappearing at the
strongest possible seed quality** — the distances are quantified above and drawn in fig109 panel
D, where the matching box is empty.

**E-ii's antecedent is also literally satisfied** — "does not converge at any published row", and
**0 of 16 recovered any named row**. **E-iii is reported because it is the more specific of the
two**: E-ii describes an absence, E-iii describes what happened instead, and what happened instead
is the finding. **The E-ii reading is recorded, not suppressed**, and its consequence stands with
it: *on this evidence, the obstruction sits in the REALIZATION rather than in the search.* **This
is the first evidence in this programme that what G1 has been measuring is the realization rather
than the budget** — and it is one unit's 16 attempts at one budget, which is exactly as much as it
is.

**No fifth branch is constructed.** E-i did not fire (no convergence at a published row). E-iv's
discipline was honoured throughout rather than fired as an outcome.

**`G1` STAYS `UNDER-RESOURCED`. Nothing here converts it to a recovery, a `no`, or a resolution,
and this unit does not touch the G1 record.**

---
## 9. LEG 353 — WHERE THIS UNIT AGREES AND WHERE IT DISAGREES

Leg 353 attempted UPO37 (×2), UPO35, UPO9 and UPO22 and **failed all five at `line_search_failed`
with final `‖R‖ ∈ [22.5, 29.5]`** (`writeup/data/p2_route_dsspb5_v1.json`, read machine-readably,
not re-transcribed).

**AGREEMENT — the headline is unchanged.** Under a bigger DNS, a better solver and twice the row
coverage, **this unit also recovered none of the named rows.** Leg 353's negative is not
overturned by the resourced version of itself.

**DISAGREEMENT — three, and they are what makes this a new measurement.**

1. **The exit reason is gone.** `line_search_failed` does not appear once in these 16 attempts,
   and it **cannot**: the hookstep's trust region always accepts a step, so plain Newton's failure
   mode is unreachable here. Every attempt exited at the stall rule or at `tol`. **Leg 353's five
   failures were the solver refusing to move; these fourteen are the solver moving and stopping.**
2. **The residuals are an order of magnitude better.** Final `‖R‖` here spans **[0.80, 10.32]**
   against leg 353's [22.5, 29.5], from seeds that were themselves **worse** (20.1–54.9). **The
   `T = 1e5` + hookstep realization gets strictly further into the problem and still recovers no
   named row.**
3. **It converged at all.** Leg 353 converged nothing; this unit converged twice — **to other
   solutions.**

**Neither run's negative is about the published rows.** Lucas & Kerswell's orbits live in *their*
discretization; **lesson 91 binds and §11 states the realization.**

---
## 10. §3d — WHAT THIS COST, AND THE SCALE AT WHICH THE QUESTION IS PROPERLY POSED

**This is a measurement of THIS realization at THIS budget. It is NOT a `no` about the named rows,
and nothing in this unit may be quoted as one.**

**What was actually spent.** Diagnostic (3): `wall 0.569 h on 10 workers = 5.687 core-hours`
banked, plus **0.806 h** of planted controls. The banked figure counts the relaunch only; the
**sum of per-attempt wall over all 16 attempts is 9.088 core-hours**, and a first unattended launch
was killed by the host after ~2 h with nothing banked (see §12). Diagnostics (1) and (2) were
re-derivations of banked records and cost minutes.

> **CORRECTION, 2026-08-18 — unit `D-REPAIR` (wave 5), discharging `V-W3`'s defect D5.**
> D5 recorded that `diagnostic_3.resourcing.core_hours = 5.687` and
> `sum(diagnostic_3.attempts[].wall_seconds) = 9.088` core-hours do not reconcile (**3.40
> core-hours, 37.4% of the larger**), and that **"which subset the 5.687 covers is not
> recoverable from the record"**. **The banked JSON is NOT edited** — reading (b), no banked
> artefact may be rewritten to match a later finding — but **the subset IS recoverable, and here
> it is.**
>
> **1. `5.687` is OCCUPANCY, not consumption.** `resourcing.core_hours` is exactly
> `wall_seconds × workers / 3600` = `2047.4409 × 10 / 3600` — a 10-worker pool held open for the
> relaunch window. It is not the sum of anything the attempts spent.
>
> **2. The relaunch's elapsed window identifies its members.** `resourcing.wall_seconds`
> (**2047.4409 s**) equals attempt **11**'s own `wall_seconds` (**2047.4169 s**) to **0.024 s**,
> `1.2e-5` relative: attempt 11 was the last of the relaunch to finish, so the window IS its
> duration. **No attempt can run longer than the window that contains it**, so the eight rows
> with `wall_seconds > 2047.4409` — attempts **0, 1, 2, 3, 4, 6, 7, 8** — **cannot** have been in
> the relaunch. That is **exactly eight**, and §12(e) records **exactly eight** completed attempts
> reused from checkpoint. The relaunch is therefore attempts **5, 9, 10, 11, 12, 13, 14, 15**.
>
> **3. The books then close, to the second.**
>
> | quantity | attempts | core-seconds | core-hours |
> |---|---|---|---|
> | relaunched, CPU actually spent | 5, 9, 10, 11, 12, 13, 14, 15 | 12,601.38 | **3.5004** |
> | inherited from the killed launch, CPU spent | 0, 1, 2, 3, 4, 6, 7, 8 | 20,116.96 | **5.5880** |
> | **all 16, `sum(attempts[].wall_seconds)`** | — | **32,718.33** | **9.0884** |
> | relaunch OCCUPANCY, `= wall_seconds × workers` (the banked `core_hours`) | 8 tasks on a 10-worker pool | 20,474.41 | **5.6873** |
> | of which BUSY / IDLE | — | 12,601.38 / 7,873.03 | 61.5% / **38.5%** |
>
> **The 3.40 core-hour gap is two effects, not one:** the banked figure **omits** the 5.588
> core-hours the eight inherited attempts really cost, and **adds** 2.187 core-hours of idle pool
> (two of ten workers were never given a task at all — 1.1375 core-hours of that on its own).
>
> **4. What this unit cost, stated once.** **9.0884 core-hours of attempt CPU** (`sum` over all
> 16 rows) **plus 0.8057 h of planted controls** (`resourcing.control_wall_seconds = 2900.554 s`),
> on top of the ~2 h first launch that banked nothing. **`5.687` is not that number and must not
> be quoted as it.**
>
> **A finding about the verifier, reported not ruled.** D5's ceiling — *"the reconciliation itself
> is beyond this artefact"* (`verify_wave3.md` §5 item 2) — **does not hold**: the provenance flag
> D5 correctly says is missing turned out not to be needed, because the elapsed window and the
> per-attempt walls determine the partition on their own. D5's **size** (3.40 core-hours, 37.4%)
> is exact and stands.

**The commissioned model was ~0.0713 h/attempt → ~1.14 core-hours for 16 attempts. The true figure
is ~0.57 h/attempt, an ~8× under-estimate**, and the reason is structural rather than accidental:
the model was calibrated on U5 attempts that stall early, while **an attempt planted at a published
`(T, s)` runs 20–31 epochs before the stall rule fires.** A seed that is *plausible* is expensive
exactly because it does not fail fast. **This is logged as a correction for the Conductor (§12d).**

> **CORRECTION, 2026-08-18 — unit `D-REPAIR` (wave 5), discharging `V-W3`'s defect D3.**
> Per `writeup/CORRECTIONS.md`'s convention the paragraph above stands as written; this block is
> beside it, and it is the measurement. **D3's finding holds and its arithmetic does not.** The
> structural explanation IS contradicted — but **not** because `E` used fewer epochs. `V-W3`
> compared `E`'s **343** (an `n_iters` count) against U5's **2195** (a ledger-row count), and
> those are two different conventions (see `prog_r4_u5.md` §"Cost basis", D4's correction block:
> a non-converged attempt banks one ledger row beyond its `n_iters`, and `2195 − 2104 = 91` is
> exactly U5's non-converged count, `357 − 343 = 14` exactly `E`'s). **Like for like, in EITHER
> convention, `E` used slightly MORE epochs per attempt, not 2.3% fewer — and it is still nowhere
> near a structural difference.**
>
> | quantity, like for like | `E` | U5 | ratio |
> |---|---|---|---|
> | epochs/attempt, `n_iters` convention | **21.4375** (343/16) | **21.04** (2104/100) | **1.0189** — `E` +1.9% |
> | epochs/attempt, ledger-row convention | **22.3125** (357/16) | **21.95** (2195/100) | **1.0165** — `E` +1.7% |
> | core-s/attempt | **2044.90** (32,718.334/16) | **2053.44** (0.0713 wall-h × 8 workers) | **0.9958** — `E` 0.4% **under** |
> | s/epoch, `n_iters` convention | **95.389** | **97.597** | **0.9774** — `E` 2.3% cheaper |
> | s/epoch, realised vs the **95 s** U5 banked as `seconds_per_epoch_costed_at` | **95.389** | 95 (model) | **1.0041** — 0.41% over |
>
> Sources, all re-derived: `writeup/data/p2_prog_r4_e_v1.json` (`diagnostic_3.attempts[].n_iters`,
> `.wall_seconds`), `experiments/programme_r4/e_hhard_ledger.json`,
> `writeup/data/p2_prog_r4_m3_v1.json` (`resourcing.epochs_spent`, `.seconds_per_epoch_costed_at`),
> `experiments/programme_r4/u5_m3_ledger.json`.
>
> **Both factors of the cost model land within ~2% in either convention**, so there is no
> structural over-run for the "runs 20–31 epochs before the stall rule fires" story to explain:
> that story predicts a *multiple*, and the measurement is a couple of per cent. The same wording
> at §12(d) carries its own correction block.
>
> **A finding about the verifier, reported not ruled.** `V-W3`'s D3 sentence "`E` used 2.3% fewer
> epochs per attempt, not more" is **wrong in size and in direction** — it is +1.9% (or +1.7%),
> not −2.3% — because it mixed the two epoch conventions. **D3's conclusion survives; its number
> does not.** The same mixed comparison reached `STATE.md` and `OPTIONS.md` in the Conductor's D1
> correction ("21.44 epochs/attempt vs U5's 21.95"); **those files are the Conductor's and are
> untouched by this unit.**
>
> **NOT repaired here, and deliberately.** The `~8×` in the sentence above is `V-W3`'s defect
> **D1**, which is **not in this unit's scope** — D1 was the Conductor's to rule and was
> corrected by the Conductor in `STATE.md` and `OPTIONS.md` on 2026-08-18 (`0.0713` is
> **wall**-h/attempt at 8 workers, `0.57` is **core**-h/attempt; like for like `E` came in 0.4%
> *under*, and the `8×` is `core ÷ wall` = the worker count). **The residue at these lines and at
> `writeup/4_p2_lottery/TECHNICAL_P2_PROGR4_HHARD.md:212` is FLAGGED, NOT FIXED**, and is
> reported to the Conductor as such. A repair is a unit; this one was not commissioned to make it.

**The scale at which the question "are these rows reachable in this realization?" is properly
posed**, priced from this unit's own measured 0.57 h/attempt:

| version | what it buys | cost |
|---|---|---|
| **what was run** | 8 rows × 2 arms, one field each | **9.1 core-hours** |
| **field ensemble** | 8 rows × 2 arms × **10 independent fields** — the honest fix for E-iv, since the row does not determine the field and one draw per arm measures one draw | **~91 core-hours** (~11 h wall at 8 workers) |
| **resolution lift** | the same 160 attempts at `N = 48`, where the published rows' own discretization is approached; DNS and Newton both scale ≳ 8× | **~730 core-hours**, plus a new `T = 1e5` DNS not budgeted here |
| **close diagnostic (2)'s gap** | re-run U3's 100 attempts under the current per-epoch ledger | **122.1 core-hours** (§6) |

**None of these were bought and none are proposed as work here.** Per the dispatch: **no new DNS,
no new seed mining, no new solver construction, no re-run of U5, and NO proposal of more seed
supply for PROG-R4.** The numbers exist so that the next person who wants this answer knows what
it costs instead of re-discovering it.

**§3d verdict on diagnostic (3): the diagnostic RETURNED and is not `UNDER-RESOURCED`.** The gate
asks whether the diagnostics returned, not whether anything converged. **The `0 of 16` is
`UNDER-RESOURCED` as a claim about the rows and a clean RESULT as a claim about this realization
at this budget**, and the two are not interchangeable.

---
## 11. LESSON 91 — WHAT THIS NEGATIVE NAMES

**Realization.** 2-D Kolmogorov flow, vorticity–streamfunction pseudospectral, **`N = 24`**,
**`Re = 60`**, forcing wavenumber **`n = 4`**, **`dt = 0.01`**, 2/3-rule dealiasing, RK4 with an
exact viscous integrating factor in a **Lie–Trotter split that is GLOBALLY FIRST ORDER in time**.
Fields from U2's single `T = 1e5` trajectory.

**Trial space.** 16 field-plus-pinned-`(T,s)` seeds: the 8 rows UPO37/35/34/32/22/20/17/9 of
Table IV, two arms each (shift-matched `S`, score-optimal `Q`), one field per (row, arm), drawn
from the 1,153 `m = 0` candidates anchored by `|T_c − T_pub| ≤ 1.0`, **with the `R < 0.25`
admission window deliberately NOT applied**.

**Basis.** Real vorticity on a uniform 24 × 24 collocation grid; extended residual with a
continuous `x`-shift `s` and period `T`, two phase rows; **`m` (discrete `y`-shift) is not carried
and the `m ≠ 0` class cannot be expressed** — all eight rows have `m_pub = 0`, so this bites the
generality of the instrument, not these attempts.

**Solver and budget.** Newton–GMRES–hookstep, `tol = 1e-8`, `max_newton = 52`, `max_gmres = 140`,
`gmres_rtol = 1e-3`, `fd_eps = 1e-6`, U5's stall exit (`k ≥ 20`, window 10, threshold 0.5),
9.1 core-hours.

**Determinism.** Fixed recorded seeds throughout: `PERM_SEED = 380`, `N_PERM = 20000`; every field
is a bit-for-bit re-integration of a recorded snapshot index; the sign of `s` is measured, not
drawn. Re-running the module reproduces the ledger.

**CEILING TIER 2. Nothing in this unit is a proof, nothing is described as movement toward Clay,
no `L1 → L4` link moves, Clay stays ~0.05%.** **Scale is not evidence** — the `T = 1e5` trajectory
buys candidates, not truth, and this unit's own headline is that the bigger realization got
*further* and still recovered nothing.

---
## 12. CORRECTIONS FOR THE CONDUCTOR

*Routed here verbatim and applied nowhere. `STATE.md`, `WALLS.md`, `DIRECTION.md` and
`plan_of_record.py` were not touched.*

**(a) `writeup/INDEX.md` has NO row for this unit's write-ups.** `INDEX.md` is outside the granted
territory (§5b), so no row was added. The BLOG/TECHNICAL pair and fig109 exist unindexed and need
a Conductor-side row.

**(b) fig107 is not registered in `writeup/build_figures.py`.** The dispatch named fig107 as U5's
and fig108 as another worker's in this wave; fig107's registration line is absent from the build
list. **fig109 was added as exactly one additive line and nothing else in that file was touched**
(the diff is `1 insertion(+), 0 deletions(-)`). Flagging fig107 rather than fixing it, because
that file's other lines are not mine.

**(c) The granted territory omitted this unit's own data artifacts.** A diagnostic that runs
Newton must bank a ledger and its converged fields. I created
`experiments/programme_r4/e_hhard_ledger.json` and `e_hhard_converged_orbits.npz` **by direct
precedent** — `u1_m1_ledger.json`, `u3_g1_ledger.json`, `u5_m3_ledger.json` and
`u5_m3_converged_orbits.npz` are all tracked in that directory under the same naming scheme.
**Nothing belonging to another unit was created, moved or edited.** Future briefs should list the
unit's own artifacts explicitly.

**(d) The commissioned cost model under-estimated this unit by ~8×.** `≈0.0713 h/attempt` was
calibrated on mined-seed attempts that stall early; **direct-seed attempts measured `≈0.57
h/attempt`** because a plausible seed runs 20–31 epochs before the stall rule fires. **A brief that
prices direct seeding off mined-seed telemetry will under-resource it every time.**

> **CORRECTION, 2026-08-18 — unit `D-REPAIR` (wave 5), `V-W3` defect D3.** The wording above
> stands; this is the measurement beside it. **The mined-seed-vs-direct-seed explanation does not
> survive either ledger.** Like for like, `E` ran **21.44** epochs/attempt against U5's **21.04**
> on the `n_iters` convention (**+1.9%**) and **22.31** against **21.95** on the ledger-row
> convention (**+1.7%**), at **95.389 s/epoch** against the **95 s** U5 banked as
> `seconds_per_epoch_costed_at` (**0.41% over**), for **2044.90** core-s/attempt against a
> modelled **2053.44** (**0.4% under**). A structural difference is a multiple; this is a couple
> of per cent. So the recommendation this item draws is unsupported by the numbers it draws it
> from: **the mined-seed telemetry priced this unit correctly in both of its factors.** Full table,
> sources, and the note on `V-W3`'s own mixed-convention arithmetic at §10. **The `~8×` here is
> D1, not D3: flagged, not fixed.**

**(e) The host killed the unattended run TWICE.** The first launch died after ~2 h with **zero**
banked results. Per-attempt pickle checkpointing plus `imap_unordered(chunksize=1)` was added to
the unit's own module in response; the second kill then cost nothing, because all 8 completed
attempts were reused from checkpoint. **Recommendation: any wave unit budgeted above ~1 h wall
should be required to checkpoint per unit-of-work before it launches.**

**(f) The `R < 0.25` Newton admission window is a live confound and no unit before this one could
see past it.** U3 §5 measured it monotone in `|s|` (Spearman 0.5012 here, admission
43.79/20.19/11.53/2.86% across the four bands); **neither U3 nor U5 ever ran a seed from outside
it**, so every banked PROG-R4 attempt is drawn from a distribution biased toward exactly the low
`|s|` that diagnostic (1) then observes the solves being pulled toward. This unit ran one
out-of-window seed (UPO35 arm S). **That is not enough to separate the two effects, and this unit
does not claim to have separated them.**
