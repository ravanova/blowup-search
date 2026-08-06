# Leg 99 (Route-BVA) — novelty pass and adversarial audit: does `solver/boussinesq_velocity.py` silently return a plausible wrong answer on degenerate polar-grid input?

**Pass date 2026-08-06.**  Target module `solver/boussinesq_velocity.py` (189 lines).
Prior gate on this module: **leg 73 (BV)** — the Lamb corner-image known-answer test, 1.76e-4
relative at observed order 2.00.

**Gate, verbatim:** *"Under an adversarial battery of degenerate polar-grid inputs (r=0
singularity, malformed/self-intersecting boundary), does `solver/boussinesq_velocity.py` ever
silently return a finite, plausible-looking result instead of propagating or flagging the
degeneracy?"*

**Answer: YES.**  One reachable silent-corruption case, plus one silent BC misapplication and
one silent under-determination.  Magnitudes in §2.  This leg does **not** patch the module —
per the gate's yes-branch it reports and escalates only.  `solver/boussinesq_velocity.py` is
byte-identical to its state at the merge base.

---

## 0. Novelty pass — is this question already answered anywhere in the repository?

Run **before** any construction, per the leg contract.  Four channels:

1. **Existing adversarial batteries.**  `test_bordered_hl_adversarial.py`,
   `test_gclm_family_adversarial.py`, `test_target_norm_adversarial.py` — three exist, none
   names `boussinesq_velocity`.  `grep -rl u_x_at_origin --include=*.py` returns four files
   (`solver/boussinesq_velocity.py`, `test_boussinesq_velocity.py`,
   `writeup/3_spikes/spike1_stepA_evidence.py`, `solver/boussinesq_rescaled.py`) and **none of
   them is a robustness test**.
2. **Leg 73's own gate.**  `test_boussinesq_velocity.py` has 5 tests, all on well-posed input
   with `r_min` between 1e-3 and 1e-4 and a fully occupied fit window.  Every one of them is a
   *correctness* assertion.  No test constructs a degenerate grid; no test asserts that a
   degenerate grid is rejected.  A correctness check on well-behaved input is not a robustness
   check.
3. **The shared ledgers.**  `experiments/JOURNAL.md` mentions the module once (line 1831),
   recording leg 73's development and its 5/5 pass — explicitly *"NOT a logged gate run — solver
   development"*.  `LITERATURE_CHECK.md` does not mention it.
4. **In-module guards.**  `grep -n "raise\|assert\|isfinite" solver/boussinesq_velocity.py`
   returns exactly **one** guard in the whole file: the `ValueError` at line 112 for
   `radial_bc="dirichlet"` with `phi_exact=None`.  There is no validation of `r_min`, `r_max`,
   `n_r`, `n_beta`, of the ordering of the radial interval, or of the fit-window occupancy in
   `u_x_at_origin`.

**Novelty: confirmed.**  Nothing in the repository asks this question of this module.

**Distinctness from leg 73.**  Leg 73 asked *is the answer right on a well-posed problem*
(yes, 1.76e-4).  This leg asks *is a wrong answer flagged as wrong*.  Independent questions with
independent answers, the same relation leg 89 (BOA) has to leg 66 (QF).

**Live-risk precedent.**  Leg 89 found a real silent-corruption bug in the sibling module
`solver/boussinesq.py` with this exact pattern.  That precedent is now extended: the mechanism
found here (§2.1) is *also* present verbatim in a second sibling,
`solver/boussinesq_rescaled.py:161`, which runs the same masked-`lstsq` origin extrapolation.
That module is outside this leg's territory and was not tested; it is flagged in §4.

---

## 1. The battery

`experiments/p2_route_bva_v1_adversarial.py`, **22 cases in three families** (origin
singularity, malformed boundary, origin read).  Totals: **7 `SILENT_WRONG`**, 2 `SILENT_EMPTY`,
4 `RAISED`, 5 `NONFINITE`, 3 `FINITE`, 1 `BASELINE`.  Each case is classified by what the module
*does*, not by whether it "works":

| verdict | meaning |
| --- | --- |
| `RAISED` | an exception propagates — the degeneracy is flagged.  **Robust.** |
| `NONFINITE` | NaN/Inf propagates into the output — the degeneracy is visible downstream.  **Robust.** |
| `SILENT_WRONG` | finite, plausible-looking, no warning, and wrong.  **Corruption.** |
| `SILENT_EMPTY` | accepted without complaint, output degenerate in shape.  **Weak.** |

Reference truth throughout is the single-mode manufactured field of leg 73's own test,
`phi* = r^2 e^{-r} sin(2b)`, `omega* = (5r - r^2) e^{-r} sin(2b)`, for which `u_x(0) = -2`
exactly.

---

## 2. Findings, in magnitude order

### 2.1 HEADLINE — `u_x_at_origin` fabricates `-0.0` on a grid that does not reach the origin

`u_x_at_origin(phi, grid, r_window=0.1)` extrapolates `c1(r) = phi_1(r)/r^2` to `r=0` by a
two-parameter least-squares fit over the mask `(grid.r > grid.r[2]) & (grid.r < r_window)`.
**The mask's occupancy is never checked.**  When `r_min >= r_window` the mask is empty, the
design matrix has shape `(0, 2)`, and `np.linalg.lstsq` on an empty system returns
`[0., 0.]` at `rank 0` — no exception, no warning.  The function then returns `-2.0 * 0.0`
= **`-0.0`**.

Occupancy sweep, `n_r=200`, `n_beta=16`, `r_max=40`, truth `u_x(0) = -2`:

| `r_min` | nodes in fit window | returned `u_x(0)` | absolute error |
| --- | --- | --- | --- |
| 1e-3 | 84 | -2.008611 | 8.61e-3 |
| 1e-2 | 53 | -2.008189 | 8.19e-3 |
| 0.05 | 18 | -2.004006 | 4.01e-3 |
| **0.09** | **1** | **-1.783803** | **2.16e-1** |
| **0.099** | **0** | **-0.000000** | **2.000e+00** |
| 0.15 | 0 | -0.000000 | 2.000e+00 |
| 1.0 | 0 | -0.000000 | 2.000e+00 |
| 10.0 | 0 | -0.000000 | 2.000e+00 |

**Magnitudes.**  The fabricated value carries **absolute error 2.000**, i.e. **100.0% relative**
— the returned number has lost the entire signal.  Against the well-posed read at `r_min=1e-3`
(error 8.61e-3) the degenerate read is worse by a factor of **232**.  The transition is a cliff,
not a taper: it happens between `r_min=0.09` and `r_min=0.099`, a **10% change in one grid
parameter**, across which the error jumps by **9.25x** (2.16e-1 -> 2.00e0) with no diagnostic of
any kind emitted at either side.

**Why this is corruption and not merely a limitation.**  `-0.0` is not an obviously-broken
sentinel.  `u_x(0)` is a signed quantity whose sign and vanishing are exactly what the
modulation read of PHASE2_SPIKE1_NOTES (2.11) tests; a returned `0.0` is a *physically
meaningful-looking* answer ("the origin strain vanishes") and would be consumed as such.  And
the trigger is the *natural* misuse: a caller who builds a grid that does not resolve the origin
neighbourhood — precisely the input class the `r=0` singularity handling exists to reject — gets
a confident number back instead of a complaint.

**Under-determination is silent too** (`r_min=0.09`, one node in the window): a rank-1 design
matrix for a two-parameter fit, so `lstsq` returns the minimum-norm solution.  Error **2.16e-1**,
**25x** the 84-node read, again with no warning and no rank check.

### 2.2 Inverted radial interval is accepted, and hides its damage at the origin

`PolarGrid(r_min=40.0, r_max=1e-3)` — a malformed (reversed) radial interval — is built without
complaint.  `rho` descends, `drho = -0.02656`, and because the Thomas solve sees only `drho^2`
the interior discretization is unharmed.  The **boundary conditions are not**: index 0 is now
the *far* end but receives the near-origin regularity condition `dphi/drho = 2n phi`, and index
-1 is the *origin* end but receives the far-field decay condition `dphi/drho = -2n phi`, whose
true behaviour there is `+2n phi`.  The wrong tail is imposed at the singular corner.

| grid | `drho` | rel L-inf, global | rel L-inf, `r < 0.05` | `u_x(0)` |
| --- | --- | --- | --- | --- |
| normal `[1e-3, 40]` | +0.02656 | 7.14e-5 | 2.15e-4 | -2.002852 |
| inverted `[40, 1e-3]` | -0.02656 | 1.43e-4 | **3.30e-2** | **-0.000000** |

**Magnitudes.**  The global relative L-inf error is **1.43e-4** — only **2.0x** the correct
grid's 7.14e-5, comfortably inside leg 73's own 5e-3 acceptance and therefore *invisible to
every existing test*.  Localized at the origin end where the wrong BC actually bites, the error
is **3.30e-2**, **154x** the correct grid's 2.15e-4 and **6.6x** outside leg 73's 5e-3 tolerance.
The global norm under-reports the local damage by a factor of **231**.  This is the classic
silent-corruption signature: a global diagnostic that stays green while the quantity of interest
is destroyed.  (The accompanying `u_x(0) = -0.0` here is the §2.1 mechanism firing again, since
`grid.r[2] ~ 39.8 > r_window`; the 3.30e-2 local error is an independent second defect.)

### 2.3 Empty angular basis accepted silently

`PolarGrid(n_beta=0)` and `PolarGrid(n_beta=-3)` both construct without error, yielding
`n_modes.size = 0` and fields of shape `(n_r, 0)`.  `velocity_from_vorticity` then returns
all-finite empty arrays.  A negative count silently becoming an empty grid is a missing
`ValueError`, though the degenerate output *shape* makes it far less dangerous than §2.1 —
classified `SILENT_EMPTY`, not `SILENT_WRONG`.

### 2.4 What IS robust — the r=0 singularity axis proper

Every case that touches the origin singularity numerically behaves correctly, i.e. makes the
degeneracy visible:

| case | verdict |
| --- | --- |
| `r_min = 0.0` (log(0) = -inf) | `NONFINITE` — 1024/1024 NaN in `phi` and `u`, 3 RuntimeWarnings |
| `r_min = -1.0` (log of a negative) | `NONFINITE` — 1024/1024 NaN, warned |
| `r_min == r_max` (`drho = 0`) | `NONFINITE` — 1024/1024 NaN, 33 RuntimeWarnings |
| `n_r = 1` | `RAISED IndexError` |
| `omega` containing one NaN | `NONFINITE` — one NaN contaminates 1024/1024 of `phi` |
| `omega` containing one Inf | `NONFINITE` — 1024/1024 non-finite in `phi` (960 NaN + 64 Inf), 4 warnings |
| `omega` shape `(n_beta, n_beta)` | `RAISED ValueError` |
| `omega` shape `(1, n_beta)` | `RAISED ValueError` |
| `radial_bc="Robin"` (case typo) | `RAISED UnboundLocalError` |

So the module's **field-level** arithmetic is honest: NaN propagates globally rather than being
swallowed, and shape/parameter errors raise.  The failure is confined to the one place where a
*reduction* happens — the least-squares origin extrapolation, where an empty or rank-deficient
input is silently absorbed into a zero coefficient.

---

## 3. Answer

**YES** — the gate's yes-branch.  The exact failing case, stated precisely:

> `solver/boussinesq_velocity.py`, `u_x_at_origin`, lines 185-189.  For any `PolarGrid` with
> `r_min >= r_window` (default `r_window = 0.1`), the mask
> `(grid.r > grid.r[2]) & (grid.r < r_window)` is empty; `np.linalg.lstsq` on the resulting
> `(0, 2)` design matrix returns `[0., 0.]` at rank 0 without raising or warning; the function
> returns `-0.0`.  Minimal reproducer: `PolarGrid(n_r=200, n_beta=16, r_min=0.15, r_max=40.0)`
> with leg 73's manufactured field, true answer `-2.0`, returned answer `-0.0`, absolute error
> **2.000**, relative error **100.0%**.  The same absence of a rank check returns a minimum-norm
> two-parameter fit from a single node at `r_min = 0.09` (error 2.16e-1, 25x the well-posed
> read).

**Not patched under this leg's authority**, per the gate.  `git diff` touches no file under
`solver/`.

---

## 4. Escalation notes for the orchestrator

1. **The fix is two lines and belongs to whoever owns the module**, not to this leg: count the
   mask, and raise (or return NaN) below 2 nodes; optionally check the returned `rank` from
   `lstsq` and refuse rank < 2.
2. **The same mechanism is in a sibling.**  `solver/boussinesq_rescaled.py:161` runs the
   identical `coef, *_ = np.linalg.lstsq(A, d1[m], rcond=None)` over a masked window.  It was
   **not** tested here (out of territory) and is **not** claimed broken — but it is the same
   pattern in the same family, and after leg 89's find in `solver/boussinesq.py` this is now the
   **third** module in the Boussinesq family implicated by pattern.  A follow-up leg scoped to
   `boussinesq_rescaled.py` is the obvious next audit.
3. **Leg 73's gate is not weakened.**  Its 1.76e-4 Lamb result stands; it simply never asked
   this question.  The battery banked as `test_boussinesq_velocity_adversarial.py` is written to
   pass **against the current, unpatched module** — it pins the *observed* behaviour, including
   the two defects, as a characterization test.  When the module is patched, the two
   `SILENT_WRONG` expectations flip to `RAISED` and the test must be updated in the same commit
   as the fix; this is stated in the test's own docstring so the next reader is not misled into
   thinking the battery blesses the bug.
