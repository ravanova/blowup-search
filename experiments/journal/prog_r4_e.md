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
