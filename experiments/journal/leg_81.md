# Leg 81 — Route-BRS: does `boussinesq_rescaled.py` ever conflate "resolution-stable" with "converged"?

**Branch** `leg/brs-v1`. **Exploration leg** (standard, status-reporting audit), claim-bearing.
**Gate answered NO** — the module never claims convergence it has not earned, with **4.2
decades** of margin at the tightest point and **7.2 decades** at the tolerance the recorded runs
actually used. `solver/boussinesq_rescaled.py` **was not edited**; it was imported and read.

## The gate, verbatim

> At the grid refinement levels where Route-K already measured the residual GROWING
> (limit-cycling), does `solver/boussinesq_rescaled.py`'s own relaxation loop ever report a
> converged/stable status?

**NO.** 0 of 12 recorded rungs × 4 tolerances in use. Lands normally on main.

## Order of work

1. `plan_of_record.py` run first. The ban that could bite is **"re-measuring beta on the 2D
   object"** (leg 43, lifted by never). It does not: the banned quantity is a *physics number*
   read off a relaxation; this leg's quantity is a *boolean field in a returned dict* and the
   arithmetic that sets it. No sweep, no parameter change, no velocity solve anywhere in the
   leg. `capabilities.py` grepped first (lines 93–98) — it is the leg's premise.
2. **Novelty pass committed BEFORE construction** (`writeup/novelty/leg_81.md`, commit
   `1e4c26d`). It found the premise true and sharpened the leg twice — see below.
3. `experiments/p2_route_brs_v1_status_audit.py` → `writeup/data/p2_route_brs_v1_status_audit.json`
   (0.2 s, no PDE).
4. `test_boussinesq_rescaled_status.py`, 8 tests, seconds.

## What the novelty pass found, and what it changed

**The premise held, and more sharply than expected.** `converged` is asserted in this
repository for three sibling modules — `gclm_rescaled` (5 sites), `hl_rescaled`,
`rescaled_spectrum` — and for `boussinesq_rescaled` it appears **0 times** across the 56
`test_*.py` files. The one module whose known answer is *"it does not converge"* was the one
module whose convergence flag no test had ever read. Route-K (leg 71) is the closest prior work
and is the *source* of the ladder, but it reads `res["residual"]` and never `res["converged"]`:
it measured the physics that makes the label falsifiable and never looked at the label.

Two narrowings came out of the pass:

- **The recorded ladder is stricter than the default.** The rungs were produced at `tol=1e-9`
  (Route-G) and `tol=1e-12` (Route-K), not the `1e-6` signature default. The audit evaluates
  the predicate at **all four** tolerances any caller in the repository passes.
- **A caller already branches on the flag.** `p2_route_g_v1_collapse.py:137` does
  `if res["converged"]: break` and skips the remaining rungs. A false `True` would have
  silently truncated the ladder Route-K then read as evidence. That is why the `no` branch is
  worth banking as a permanent test rather than noting and moving on.

## Method — how a status path is audited without running the object

- **A1.** Rungs read out of `writeup/data/p2_route_g_v1_g2.json` and `p2_route_k_v1_port.json`;
  the predicate `res < tol` evaluated against each, margin in decades.
- **A2.** `ScriptedRelaxation` — a subclass whose `rhs`/`step` emit a scripted residual
  sequence. `run()`'s real control flow, with the PDE removed: no velocity solve, no modulation
  constant, no grid physics.
- **A3/A4.** The reporting lag, and the abnormal exits (NaN, the 1e8 cut, `max_steps=0`).

## The numbers

| datum | magnitude |
|---|---|
| refinement ladder, `n_r` 300 → 600 | residual **1.671e-02 → 2.667e-01**, GROWS **16.0×** |
| Route-K limit cycle, 500 → 5000 steps | falls **38×**, then climbs **8.9×** back |
| rungs where `res < tol` fires | **0** of 12, at each of 4 tolerances |
| closest approach, `tol=1e-6` (default) | **+4.2 decades** |
| closest approach, `tol=1e-9` (the ladder's own) | **+7.2 decades** |
| closest approach, `tol=1e-12` (Route-K's) | **+10.2 decades** |
| step evaluations covered | **19 000** distinct, not 12 endpoints — `run()` returns the residual it broke on, so a large final residual rules out every intermediate step of that run |
| replay through the real loop | `converged=False`, `max_steps` exhausted, **12/12** case × tolerance |
| positive control | monotone decade decay fires at **4/4** — the negative is the module's, not the instrument's |

## Three secondary observations — reported, not patched (the module is read-only here)

1. **One-step reporting lag.** `residual` is the residual of the **predecessor** of the returned
   iterate (`step()` measures `R0`, then returns the state one update later; `renorm=True`
   rescales after the measurement). Measured at **1.0 decade** on a one-decade-per-step
   sequence. Unreachable at every recorded rung; pinned by test (7).
2. **A single-step dip below tol would be reported converged** — the one shape that could
   produce a false positive. Built deliberately: the returned state's true residual is then
   **6.4–12.4 decades** larger than the number reported beside it. It does **not** flip the
   gate, because the residual would have to fall **5.2 decades** (at `1e-6`) to **8.2 decades**
   (at `1e-9`) below anything ever recorded on this object to be reachable.
3. **`run(max_steps=0)` raises `UnboundLocalError`** on `step + 1`. No caller passes 0.

## Consequences

- `capabilities.py`'s caveat for this module is a statement about the **physics** and stays
  exactly as it is. This leg closes the other half: the code says what the physics says.
- The 8 tests are tied to the ladder **in `writeup/data/`**, so if a future leg re-measures the
  object and the residual regime changes, test (1) and the 3-decade margin floor in test (2)
  force someone to re-run the audit rather than letting a stale negative ride.
- Whoever next owns `solver/boussinesq_rescaled.py` inherits three named, measured, unpatched
  items above. None is load-bearing today; item 2 is the one to fix first if the relaxation is
  ever made to descend.
