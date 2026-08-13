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

