# Leg 81 — Route-BRS: novelty pass on the status-reporting audit of `solver/boussinesq_rescaled.py`

**Leg 81, Route-BRS v1. Date of pass: 2026-08-06, written and committed BEFORE any line of the
audit runner or the regression test.** This is a CODE audit, not a physics leg: it changes no
parameter, runs no sweep, fits no exponent, and asserts no new number about the object. The
novelty question is therefore not "has anyone in the literature asked this" — nobody outside
this repository has ever seen this module — but the two internal ones: **has this repository
already audited this code path, and is the premise (that the path is unaudited) actually true?**

Both were checked against the repository, and the second changed how the leg is framed.

---

## 0. Bans, checked first

`plan_of_record.py` was run before anything else. The live bans, and this leg against each:

| ban | this leg |
|---|---|
| **re-measuring beta on the 2D object** (leg 43, lifted by never) | **Not touched.** The banned quantity is a *physics number* — `beta` — obtained by relaxing the 2D object and reading `c_omega/c_l`. This leg reads no `beta`, computes no `c_omega`, and runs no parameter sweep. Its quantity is the value of a *boolean field in a returned dict* and the arithmetic that sets it. Distinct quantity, distinct question. The refinement ladder it audits against is **read out of `writeup/data/p2_route_g_v1_g2.json`**, already on record — it is not re-run. |
| another gCLM measurement leg | no gCLM module is imported |
| another Route-D bound-sharpening leg | no interval / NK code touched |
| any GA compute on an unvalidated fitness | no GA |
| **building a solver without grepping `capabilities.py` for the object first** | `capabilities.py` was grepped first (row `solver/boussinesq_rescaled.py`, **lines 93–98**) — it is this leg's entire premise, quoted in §1. Nothing is built: no solver, no object, no new physics function. |

The ban that could plausibly bite is the beta one, and the distinction is worth stating sharply
because it is the reason this leg is allowed to exist at all: leg 43's ban says *the object does
not converge, so stop measuring it*. This leg takes that as **given** and asks the strictly
downstream question — **given that it does not converge, does the code say so?**

---

## 1. The premise, verbatim from `capabilities.py`

```
{"module": "solver/boussinesq_rescaled.py", "object": "2D Boussinesq, rescaled RHS",
 "holds": "the rescaled (omega, eta, xi) system, modulation (c_l, c_omega), relaxation",
 "validated": ("reproduces Chen-Hou's beta to 2.1% -- and Route-K showed the "
               "relaxation LIMIT-CYCLES and its residual GROWS under refinement, so "
               "'resolution-stable' here is not 'converged' (71)"),
 "test": "test_boussinesq_rescaled.py"},
```

Every clause of that `validated` string is a statement about **the object's dynamics**. None of
it is a statement about **the reporting code**. The gap between the two is this leg.

## 2. Has this repository already asked it? — NO, and the near misses are named

Six channels, all internal.

**A. `DIRECTION.md`.** Leg 81's own entry (lines 995–1027) is the only place in the file where
`boussinesq_rescaled` and a status question meet. No earlier leg entry proposes it.

**B. Route-K itself (leg 71, `experiments/p2_route_k_v1_port.py`).** This is the closest prior
work and it is *the source of the ladder*, so it must be excluded carefully. Route-K's K1 asks
**"does the relaxation have a fixed point?"** and answers it about the *object*: its verdict
string is *"There is no fixed profile, so Y_0 is UNDEFINED — a stronger statement than
'large'."* Its consumer is the radii polynomial. It reads `res["residual"]` from `run()` and
never reads, tests, or mentions `res["converged"]`. Route-K measured the physics that makes the
label falsifiable; it never looked at the label.

**C. `solver/port_certification.py` lines 32–42.** Prose header: *"It does not converge — it
LIMIT-CYCLES."* Again a claim about the dynamics, written by the consumer, not a check of the
producer's own flag.

**D. `solver/weight_search.py` line 26** repeats the same caveat as a *citation of the record*.

**E. The 56 `test_*.py` files.** `converged` is asserted in the repository for **three other**
modules — `solver/gclm_rescaled.py` (`test_gclm_rescaled.py`, 5 sites, including
`assert r["converged"]`), `solver/hl_rescaled.py`, and `solver/rescaled_spectrum.py`
(`test_rescaled_spectrum.py` line 190 asserts the *negative*, `assert not out["converged"]`, and
its docstring line 28 states the intended contract: *"converged=False rather than handing back
its last iterate"*). For `solver/boussinesq_rescaled.py` the count is **zero**: the two test
files that import it — `test_boussinesq_rescaled.py` (6 tests) and `test_boussinesq_transport.py`
— contain **0 occurrences of the string `converged`**. The nearest test,
`test_integrator_runs_stably`, calls `run(..., max_steps=60)` and asserts only that the residual
and the fields are **finite**. It never reads the status.

**F. The `writeup/` tree.** The refinement-ladder numbers are banked and cited repeatedly; no
document evaluates the exit predicate against them.

**Conclusion: novel within this repository.** The one module in the family whose *known* answer
is "it does not converge" is the one module whose convergence flag no test has ever read.

## 3. What the pass changed about the leg — two narrowings

**(i) The ladder is stricter than the default, so the audit must not use the default alone.**
The refinement rungs on record were **not** produced at the module's default `tol=1e-6`.
`p2_route_g_v1_collapse.py` line 136 runs `tol=1e-9`; `p2_route_k_v1_port.py` line 63 runs
`tol=1e-12`; `p2_route_l_v1_precond.py` line 56 also `tol=1e-12`. The audit must evaluate the
predicate at **all four** tolerances actually used in this repository (1e-6, 1e-9, 1e-12, and
`spike1_stepC_gate.py`'s 1e-9), not just the signature default, or it would answer a question no
caller asks.

**(ii) A caller already depends on the flag, so a false positive would not be cosmetic.**
`p2_route_g_v1_collapse.py` lines 137–147 branch on `if res["converged"]:` and **breaks out of
the checkpoint ladder**, printing *"converged at N steps; higher rungs skipped"*. So the flag is
not decorative: a false `True` would silently truncate the very ladder Route-K then read as
evidence. That raises the stakes of the gate and is recorded here as the reason the regression
test is worth banking under the `no` branch rather than being a formality.

## 4. Independence from the neighbouring legs

- **Leg 43** (banned): 2D `beta`, a physics number, by sweeping. This leg: a dict field, by
  reading recorded data and replaying a scripted residual sequence through the loop. No overlap.
- **Leg 66** (Route-QF): the *methodological* precedent — a real defect (`derivative_hat` on
  odd-length grids) found only by testing a module directly rather than through its consumers.
  Different module, different symbol; cited as the reason to expect the class of bug, never as
  evidence for it.
- **Leg 73** (Route-BV): `solver/boussinesq_velocity.py` — a **different module** (Biot–Savart /
  stream function), and an external check rather than a code audit.
- **Leg 71** (Route-K): §2B above. Provider of the ladder, not asker of the question.

## 5. External novelty — stated and dismissed honestly

No literature search was run and none is owed: the object of the audit is a private 280-line
file in this repository. There is no external claim in this leg, so there is nothing for an
external source to have scooped. The only external-facing content would be the *class* of bug
(convergence flags that fire on a transient dip of a non-convergent iteration), which is
folklore in numerical software and is not claimed as novel here.

## 6. What the audit is therefore permitted to do

- **Read** `solver/boussinesq_rescaled.py`; edit it under no outcome.
- **Read** the recorded rungs from `writeup/data/p2_route_g_v1_g2.json` and
  `writeup/data/p2_route_k_v1_port.json`; re-run neither.
- **Exercise** the `run()` loop's control flow with a *scripted* residual sequence (a subclass
  overriding `rhs`/`step`), which touches no PDE, no grid physics and no modulation constant —
  this is how the loop is audited without running the object.
- Report **magnitudes** — decades of margin between the recorded residuals and each tolerance
  actually used — never a bare boolean.

---

# Part II — the findings (written after the audit ran)

**The gate, verbatim:**

> At the grid refinement levels where Route-K already measured the residual GROWING
> (limit-cycling), does `solver/boussinesq_rescaled.py`'s own relaxation loop ever report a
> converged/stable status?

**Answer: NO.** The predicate fires at **0 of 12** recorded rungs × **4** tolerances in use.
The closest any recorded residual has ever come to a tolerance is **4.2 decades** (the smallest
residual on record, `1.671e-02`, against the loosest tolerance, the `1e-6` signature default);
against the `1e-9` those runs actually passed it is **7.2 decades**, and against Route-K's
`1e-12` it is **10.2 decades**. `solver/boussinesq_rescaled.py` was **not edited**, and this
lands on the `no` branch: banked as a regression check tied to the ladder already on record.

## 7. The magnitudes

**The premise, restated from the record** (`writeup/data/p2_route_g_v1_g2.json`,
`p2_route_k_v1_port.json` — read, not re-run):

| ladder | rungs | residual | shape |
|---|---|---|---|
| Route-G grid refinement, `r_max=1e5`, 2500 steps | `n_r` = 300 / 450 / 600 | 1.671e-02 → 7.708e-02 → 2.667e-01 | **GROWS 16.0×** under refinement |
| Route-K steps, `n_r=200`, `tol=1e-12` | 500 / 1500 / 3000 / 5000 | 9.757e-01 → 2.060e-01 → 2.570e-02 → 2.290e-01 | falls **38×**, then **climbs 8.9× back** — the limit cycle |
| Route-G steps, `n_r=300`, `tol=1e-9` | 400 / 1200 / 2500 / 4000 | 1.136 → 5.167e-01 → 1.671e-02 → 1.782e-02 | flattens, does not descend |

**The predicate against them.** The module's exit test is the single expression `res < tol`,
used both for the loop `break` (line 272) and for the reported label (line 278) — one
expression, so the label cannot disagree with the stop. Margins, in decades, of the closest
rung:

| tolerance | call site | margin at the closest rung | rungs where the predicate fires |
|---|---|---|---|
| 1e-6 | signature default | **+4.2** | 0 / 12 |
| 1e-7 | `spike0_rescaling_evidence.py:66` | **+5.2** | 0 / 12 |
| 1e-9 | `p2_route_g_v1_collapse.py:136` (the ladder on record) | **+7.2** | 0 / 12 |
| 1e-12 | `p2_route_k_v1_port.py:63` | **+10.2** | 0 / 12 |

**The endpoints are not the whole claim.** `run()` breaks the instant `res < tol` and returns
*that same* `res`. So a recorded **final** residual of 1.671e-02 from a run with `tol=1e-9`
proves no *intermediate* step of that run was sub-tolerance either — otherwise the run would
have stopped there and reported the smaller number. That argument covers **19 000 distinct step
evaluations** (4 refinement rungs × 2500, plus the deepest checkpoint of each of the two
cumulative steps ladders), not 12 endpoints.

**And the loop agrees when actually driven.** The recorded residual sequences were replayed
through the *real* `run()` control flow with the PDE removed (`ScriptedRelaxation` overrides
only `rhs`/`step`): `converged=False` and `max_steps` exhausted on **12/12** case × tolerance
combinations. The positive control — a monotone one-decade-per-step decay — fires correctly at
all 4 tolerances, so the negative is the module's behaviour and not a dead instrument.

## 8. Three secondary observations, reported and NOT patched

The module was not edited under any outcome, as the territory requires. Each of these is
recorded for whoever owns the module next.

**(a) The reported residual lags the returned state by exactly one step.** `step()` computes
`res` from the state it is *given* (`R0`, the first SSPRK3 stage) and returns the state one
full update later; `run()` then stores that `res` beside the *later* state. Measured on a
one-decade-per-step sequence, the reported residual is **1.0 decade** away from the residual of
the iterate handed back with it. With `renorm=True` there is a second half-step of the same
kind: the fields are rescaled *after* `res` was measured. Consequence, stated precisely:
`converged=True` certifies the **predecessor** of the returned iterate. It never manufactures a
sub-tolerance number, and at every recorded rung it is **7.2+ decades** from being reachable.
Pinned by test (7) so a future repair is noticed rather than silently changing the contract.

**(b) A single-step dip below tolerance would be reported converged.** This is the shape that
*could* produce a false positive, so it was built deliberately: a scripted cycle
`[2.5e-1, 2.6e-2, dip, 2.3e-1, 1.9e-1]` with one sub-tolerance step. `run()` stops there and
reports `converged=True`, with the returned state's true residual **6.4 decades** (at `tol=1e-6`)
to **12.4 decades** (at `1e-12`) larger than the number reported beside it — (a) and (b)
compounding. **This does not flip the gate**, and the magnitude is why: the residual would have
to fall **5.2 decades** below anything ever recorded on this object at the loosest tolerance in
use, and **8.2 decades** below it at the `1e-9` the recorded runs used, for that path to be
reachable at all. It is a latent trap at a depth this object has never been within four orders
of magnitude of.

**(c) `run(max_steps=0)` raises `UnboundLocalError`.** `step` is the `for` variable and
`step + 1` is evaluated unconditionally in the result dict. No caller in this repository passes
0. A robustness wart, one line, not this leg's to fix.

## 9. Why the `no` is worth banking rather than shrugging at

A caller already branches on the flag: `experiments/p2_route_g_v1_collapse.py` lines 137–147
does `if res["converged"]: break` and **skips the remaining checkpoint rungs**, printing
*"converged at N steps; higher rungs skipped"*. A false `True` would therefore have silently
truncated the very ladder Route-K then read as evidence that the object has no fixed point.
That path is now covered by `test_boussinesq_rescaled_status.py` — 8 tests, seconds, no PDE
solve — where before this leg the string `converged` appeared **0 times** in the two test files
that import the module, against **5 sites** in `test_gclm_rescaled.py` for its sibling.

## 10. What this leg does NOT claim

- It does **not** say the relaxation converges. It says the opposite, and re-confirms from the
  record that the residual **grows 16.0×** under refinement.
- It does **not** re-measure `beta`, `c_l`, `c_omega`, `alpha` or any profile quantity. The
  audit never solves the velocity field: the only numbers it produces are decades of margin,
  step counts, and booleans read back out of a scripted loop.
- It does **not** validate `capabilities.py`'s physics caveat, which stands untouched and
  unchanged. It closes the *other* half: the caveat is true of the object **and** the code says
  so, at every refinement level the repository has on record.
