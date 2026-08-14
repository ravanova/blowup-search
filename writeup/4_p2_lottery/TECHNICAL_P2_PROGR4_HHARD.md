# PROG-R4 unit E — THE H-HARD DIAGNOSTIC: is the obstruction the seed supply, or the realization?

**Unit:** PROG-R4 unit E (leg 380, wave 1), `ORCHESTRATION.md` §3g CONDUCTOR mode, Lane R.
**INSTRUMENT unit — it answers a gate about whether three diagnostics RETURN, not about whether
anything converges.**
**Mode:** §3f SOLO. **UNVERIFIED** — produced and checked in one session, no paired verifier.
**Data of record:** `writeup/data/p2_prog_r4_e_v1.json`; ledger
`experiments/programme_r4/e_hhard_ledger.json`; converged fields
`experiments/programme_r4/e_hhard_converged_orbits.npz`. Read-only inputs:
`experiments/programme_r4/u3_g1_ledger.json`, `u5_m3_ledger.json`,
`u2_recurrence_library.json`, `writeup/data/p2_route_dsspb5_v1.json`.
**Evidence:** `experiments/p2_prog_r4_e_evidence.py`, **60/60** — re-derives every number below
from banked records, re-running no solve.
**Figure:** fig109, **17/17** checks.
**Pre-registration:** `experiments/journal/prog_r4_e.md` §§0–4, commit `70f3962`, **before the
first attempt ran.**
**Journal:** `experiments/journal/prog_r4_e.md`.

> **G1 IS NOT RE-ANSWERED HERE.** It stays `UNDER-RESOURCED` as banked in
> `writeup/data/p2_prog_r4_g1_v1.json`, which this unit does not write to. `0 of 16` is a
> **count**, pre-registered as such; it is not a `no` at G1, and no G1 re-open is raised.

---

## 1. The gate, and the answer

> **Do all three diagnostics return, each with a planted control that fires both ways?**

**YES.** All three returned; each carries a planted control demonstrated firing in **both**
directions. **The gate is about the diagnostics returning, not about convergence** — a clean
non-convergence with working controls passes it.

| # | diagnostic | verdict | controls |
|---|---|---|---|
| 1 | where converged `\|s\|` sits against seed `\|s\|`, over the 200 banked attempts | **`PULL_TO_LOW_S`** | fired both ways |
| 2 | is the solve an *iteration* or a *minimisation*? | **`MIXED`** | fired both ways |
| 3 | 16 attempts planted at the eight published rows | **RETURNED**: 2 converged, **0 recovered any named row** | P ✓, N ✗ (as planted), R ✓ |

**Branch fired: E-iii — "converges to something else."**

**Ceiling: TIER 2.** Nothing here is a proof. No `L1 → L4` link moved. Clay stays ~0.05%.

## 2. What was planted — the E-iv discipline, stated before the run

**A published Table IV row (arXiv:1406.1820v2) determines `(T, s, m)` and NOTHING ELSE. It does
not determine a field.** Every attempt therefore plants a **field-plus-pinned-`(T,s)` seed**, and
no sentence in this unit calls that "seeding at the published orbit."

| | exactly what was planted |
|---|---|
| basis | real vorticity `w(x,y)` on a uniform **24 × 24** grid, `Re = 60`, forcing `n = 4`, `dt = 0.01`, 2/3-rule dealiased pseudospectral, **Lie–Trotter split, globally FIRST order in time** |
| field | bit-for-bit re-integration of one snapshot of U2's `T = 1e5` trajectory |
| `T` | the **published period exactly** — not the candidate's period, which is quantised to the 0.25 snapshot spacing |
| `s` | **±** the published shift wrapped to `(-π, π]`; **the sign is MEASURED**, both evaluated and the smaller residual taken. Tally over 16 seeds: `{plus: 5, minus: 11}` |
| `m` | 0 — all eight rows have `m_pub = 0`, and the extended residual carries a continuous `x`-shift only |

Two arms per row, one field each, **no field reused**: **arm S** "shift-matched field" (lowest `R`
among candidates whose measured `|s|` is within 0.05 of published), **arm Q** "score-optimal
field" (lowest `R` outright — the field U3 would have chosen).

**The `R < 0.25` Newton admission window is DELIBERATELY NOT APPLIED.** U3 §5 measured it monotone
in the very coordinate the targets are separated on; **this is the unit entitled to ignore it, and
neither U3 nor U5 ever ran a seed from outside it.** One seed here (UPO35 arm S, `R = 0.478`) sits
outside it.

Solver held at U5's values and **imported rather than copied**: Newton–GMRES–**hookstep**,
`tol = 1e-8`, `max_newton = 52`, `max_gmres = 140`, `gmres_rtol = 1e-3`, `fd_eps = 1e-6`, U5's
stall exit (`k ≥ 20`, window 10, threshold 0.5). Matching predicate is U3's, unchanged: a
recovery requires **both** `|ΔT| < 0.05` **and** `|Δs|_{2π} < 0.05`.

## 3. The prior — leg 353, stated up front, not rediscovered

Leg 353 attempted UPO37 (×2), UPO35, UPO9 and UPO22 and **failed all five at
`line_search_failed`, final `‖R‖ ∈ [22.5, 29.5]`**. **This unit is a new measurement, not a
re-walk, for two named reasons:** leg 353 used a `T_total = 2000` DNS against U2's `T = 1e5`, and
**plain-Newton line search, not the hookstep.**

## 4. Diagnostic (1) — `PULL_TO_LOW_S`

Over the **200 banked attempts** (U3's 100 + U5's 100, read and never edited), **23 reached
`tol`**. All three pre-registered clauses hold:

| clause | measured |
|---|---|
| median drift `\|s\|_conv − \|s\|_seed < 0` | **−0.03202** (mean −0.06880) |
| ≥ half of convergences finish below `\|s\| = 0.15` | **21 of 23 = 91.3%** |
| exact two-sided sign test, `p < 0.05` | **17 down / 6 up, p = 0.0347** |

Spearman(seed, converged) = **0.3205** — the seed shift explains little of where a solve lands.
**6 in-band seeds converged and 5 left the band.**

**The SECONDARY all-200 reading returns `NO_PULL`** (median −0.0239, 120/80, `p = 0.0057`, but
only 38.5% below 0.15 and Spearman 0.793) and is **reported, not suppressed**: a non-converged
attempt has not landed anywhere, so its terminal `|s|` is mostly its seed `|s|`. **The pull is a
property of the solutions this realization reaches, not of every trajectory.**

Controls: converged `|s| := 0.10` → `PULL_TO_LOW_S`; converged `|s| :=` seed `± 0.001` →
`NO_PULL` (`p = 1.0`). **Both ways.**

## 5. Diagnostic (2) — `MIXED`, and the ban

An accepted epoch is **`constrained`** if the accepted hookstep trial sits on the trust-region
boundary (the *minimisation* chose the step) and **`unconstrained`** otherwise. Over **2,195
accepted epochs**:

| | constrained | unconstrained |
|---|---|---|
| epochs | **2,131 (97.1%)** | 64 (2.9%) |
| mean per-epoch `d\|s\|` | −0.002695 | −0.001842 |
| net `Σ d\|s\|` | **−5.7431 (98.0% of the descent)** | −0.1179 |

Observed rate difference **−0.000853**, within-attempt label permutation **`p = 0.9317`** (20,000
perms, `PERM_SEED = 380`). **The rates are indistinguishable**, so the rule returns **`MIXED`**
and this unit does not get to say the minimisation is dragging the solve. 98.0% of the descent is
on constrained epochs **because 97.1% of accepted steps are constrained at all** — in this
realization the full Newton step is almost never taken. `corr(Δ‖R‖, d|s|) = +0.1954`.

**THE BAN, CONFIRMED. Because (2) did NOT return `MINIMISATION_ATTRACTOR`, the commissioned
"the fix is in the SCORE" conditional does not fire and nothing is proposed. Independently, leg
349's ban is COMPLIANT and was never approached: every score touched is deterministic and
pre-existing (U2's recurrence score `R`, the solver's extended residual). Nothing was fitted,
learned, evolved or tuned to an outcome, and this unit proposes no learned or evolved seed-scoring
fitness.**

**The score's own bias, re-derived from U2's library** (1,153 `m=0` candidates):
Spearman(`|s|`, `R`) = **0.5012**; admission fractions **43.79 / 20.19 / 11.53 / 2.86%** across
`|s| ∈ [0,0.15) / [0.15,0.295) / [0.295,0.707) / [0.707,π]`. **The published band is the third
cell.** That reproduces U3 §5's 0.50 and 44/20/11/3 from the library rather than from U3's table.

**Coverage limit, declared in the pre-registration:** the per-epoch `|s|` path exists for U5's 100
attempts only — U3's ledger predates those fields. **Cost to close: 122.1 core-hours.** Not
bought, not needed for this gate, not hidden.

## 6. Diagnostic (3) — 16 attempts at the eight named rows

**2 of 16 reached `tol`. 0 recovered their own named row. 0 recovered ANY named row. 0 secondary
sign-agnostic `|s|` matches. Exits `{stalled: 14, converged: 2}`.**

**The two convergences are genuine solutions of this realization and neither is its row:**

| | final `‖R‖` | epochs | `T` / published | `\|s\|` / published | `ΔT` | `Δs` |
|---|---|---|---|---|---|---|
| **UPO35 arm Q** | 4.83e-09 | 22 | 22.0358 / 18.912 | 0.1349 / 0.7072 | **3.124** | **0.572** |
| **UPO9 arm Q** | 2.06e-10 | 12 | 16.5369 / 14.776 | 0.0994 / 0.2950 | **1.761** | **0.394** |

**Both landed below diagnostic (1)'s 0.15 shelf, from seeds pinned at 0.707 and 0.295. That is the
pull of diagnostic (1) reappearing at the strongest seed quality this programme can construct.**

**Closest approach: UPO35 arm S, `ΔT = 0.0362`, `Δs = 0.0854`, final `‖R‖ = 9.669`** — inside the
box on `T`, just under 2× the tolerance out on `s`, and **a STALLED attempt, not a solution.**

**No attempt hit the iteration cap.** All 14 non-convergences stopped at the pre-registered stall
exit at 20–31 of 52 available epochs, so **"more Newton iterations" is not the obviously-missing
resource.**

**Arm S starts closer and finishes further, 8 rows out of 8.** The shift-matched field has the
lower seed residual in every row, yet arm Q's mean final residual is **1.66** against arm S's
**5.15**, and **both convergences are arm Q**. The recurrence score, which knows nothing about the
published rows, predicts Newton progress better than agreement with the published shift does.

**Instrument fact (E-iv):** the seed residuals here span **[20.06, 54.94]** against ≈14–19 for the
mined seeds U3 and U5 ran. **Planting at the published `(T,s)` yields a WORSE starting point than
the repository's own mining** — the direct cost of the row not supplying a field.

**Controls.** **P** (exact relative equilibrium in closed form, perturbed 0.1%) → converged,
`‖R‖ = 7.75e-09`, 33 epochs. **N** (phase-scrambled field at the same `(T,s)`) → did not converge,
`‖R‖ = 51.46`, 51 epochs, `max_newton_hit`. **R** (banked U5 convergence `attempt007_P_UPO37`,
perturbed) → converged **and matched back**, `‖R‖ = 1.52e-10`, 5 epochs, `ΔT = 2.99e-07`,
`Δs = 6.50e-08`, `harness_predicate_says_recovered = True`. `fired_as_planted = True`,
`failures = []`.

**Control R is what makes the zero a measurement:** the same predicate that returned 0 recoveries
**can** return a recovery, on this solver, at this tolerance, in this harness.

**The stall rule was re-validated before use:** replayed against both banked ledgers it kills
**zero** of U3's 14 and **zero** of U5's 9 convergences (worst 10-epoch ratios 0.0724 and 0.0606
against 0.5).

## 7. The branch — E-iii, with E-ii's antecedent recorded

**E-iii fired: "converges to something else."** Two convergences at `1e-9` and `1e-10`, neither
its row, both at low `|s|`, distances quantified in §6 and drawn in fig109 panel D where the
matching box is **empty**.

**E-ii's antecedent is also literally satisfied** — 0 of 16 recovered any named row — and is
**recorded, not suppressed**: on this evidence the obstruction sits in the **realization rather
than the search**, which would be **the first evidence in this programme that what G1 has been
measuring is the realization rather than the budget.** **E-iii is reported because it is the more
specific of the two:** E-ii names an absence, E-iii names what happened instead. **E-i did not
fire. No fifth branch is constructed.**

## 8. Leg 353 — agreement and disagreement

**AGREEMENT:** under a bigger DNS, a better solver and twice the row coverage, **this unit also
recovered none of the named rows.**

**DISAGREEMENT, three:** (i) **`line_search_failed` does not occur once and cannot** — the
hookstep always accepts a step, so plain Newton's failure mode is unreachable; every attempt
exited at the stall rule or at `tol`. (ii) **Final `‖R‖` spans [0.80, 10.32] against [22.5, 29.5]**
— from *worse* seeds. **The bigger realization gets strictly further into the problem and still
recovers no named row.** (iii) **It converged at all** — twice, to other solutions.

## 9. §3d — cost, and the scale at which the question is properly posed

**This is a measurement of THIS realization at THIS budget. It is NOT a `no` about the named rows
and may not be quoted as one.**

Spent: **5.687 core-hours** banked (0.569 h wall on 10 workers) plus **0.806 h** of controls; the
**sum of per-attempt wall over all 16 attempts is 9.088 core-hours**, and one unattended launch
was killed by the host after ~2 h with nothing banked.

**The commissioned model was ~0.0713 h/attempt; the true figure is ~0.57 h/attempt — an ~8×
under-estimate**, structurally so: mined-seed attempts stall early, while an attempt planted at a
published `(T,s)` runs 20–31 epochs before the stall rule fires. **A plausible seed is expensive
precisely because it does not fail fast.**

| version | what it buys | cost |
|---|---|---|
| **what was run** | 8 rows × 2 arms, one field each | **9.1 core-hours** |
| **field ensemble** | 8 × 2 × **10 independent fields** — the honest fix for E-iv | **~91 core-hours** |
| **resolution lift** | the same 160 attempts at `N = 48` | **~730 core-hours** + a new `T = 1e5` DNS |
| **close (2)'s gap** | re-run U3's 100 attempts under the current ledger | **122.1 core-hours** |

**None were bought and none are proposed as work.** No new DNS, no new seed mining, no new solver
construction, no re-run of U5, and **no proposal of more seed supply for PROG-R4.** The numbers
exist so the next person knows the price instead of rediscovering it.

## 10. Lesson 91 — what this negative names

**Realization:** 2-D Kolmogorov flow, `N = 24`, `Re = 60`, `n = 4`, `dt = 0.01`, 2/3-rule
dealiasing, RK4 with an exact viscous integrating factor in a **Lie–Trotter split that is globally
FIRST order in time**; fields from U2's single `T = 1e5` trajectory.
**Trial space:** 16 field-plus-pinned-`(T,s)` seeds — 8 rows × 2 arms, one field each, from the
1,153 `m = 0` candidates anchored by `|T_c − T_pub| ≤ 1.0`, **with the `R < 0.25` window
deliberately not applied.**
**Basis:** real vorticity on a 24 × 24 grid; extended residual with continuous `x`-shift and
period, two phase rows; **`m` is not carried and the `m ≠ 0` class cannot be expressed** — which
bites the instrument's generality, not these eight `m_pub = 0` rows.
**Budget:** hookstep, `tol = 1e-8`, `max_newton = 52`, U5's stall exit, 9.1 core-hours.
**Determinism:** fixed recorded seeds (`PERM_SEED = 380`, `N_PERM = 20000`); every field a
bit-for-bit re-integration of a recorded snapshot index; the sign of `s` measured, not drawn.

**Scale is not evidence.** The `T = 1e5` trajectory buys candidates, not truth — and this unit's
own headline is that the bigger realization got *further* and still recovered nothing.

---

*Produced and checked in a single session with no independent reviewer, and therefore labelled
UNVERIFIED under this project's own rules. Verification is a fresh pair of eyes or it is not
verification.*
