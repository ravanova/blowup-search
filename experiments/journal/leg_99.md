# Leg 99 — Route-BVA: adversarial audit of `boussinesq_velocity.py`'s degenerate-grid handling

**Agent:** LEG-I. **Branch:** `leg/bva-v1`. **Date:** 2026-08-06. **Claim-bearing.**
**Module under test:** `solver/boussinesq_velocity.py` — **read, never edited.**

## Gate and answer

> "Under an adversarial battery of degenerate polar-grid inputs (r=0 singularity,
> malformed/self-intersecting boundary), does `solver/boussinesq_velocity.py` ever silently
> return a finite, plausible-looking result instead of propagating or flagging the degeneracy?"

**YES — 7 `SILENT_WRONG` cases out of 22** (plus 2 `SILENT_EMPTY`, 4 `RAISED`, 5 `NONFINITE`,
3 `FINITE`, 1 `BASELINE`). `yes` branch: a silent-corruption gap.
**Reported and escalated, NOT patched** under this leg's authority. `git diff` touches nothing
under `solver/`.

## Order of work

1. `plan_of_record.py` read. No ban touches this leg: it is an audit of existing infrastructure,
   not a gCLM / Route-D / DSS / 2D measurement, and it builds no solver. The "grep
   `capabilities.py` before building" ban was honoured first — `capabilities.py:93-96` is where
   the claim under audit lives (leg 73's Lamb corner-image gate, 1.76e-4 relative at order 2.00).
2. **Novelty pass run and committed BEFORE construction** (`writeup/novelty/leg_99.md`, commit
   `c7f76ab`). Four channels, all internal (this is a code audit, not a literature question):
   existing adversarial batteries, leg 73's own test file, the shared ledgers, and the module's
   in-file guards. The decisive measurement: `grep -n "raise\|assert\|isfinite"` over the whole
   189-line module returns **exactly one guard**, the `ValueError` at line 112.
3. Battery built and run: `experiments/p2_route_bva_v1_adversarial.py` → curated data
   `writeup/data/p2_route_bva_v1_adversarial.json` (0.8 s).
4. Banked: `test_boussinesq_velocity_adversarial.py`, 9 tests, all passing against the
   **unpatched** module.

## The predicate, fixed before the run

A degeneracy is HANDLED if it is made visible by *either* route — `RAISED` (an exception
propagates) or `NONFINITE` (NaN/Inf reaches the returned array, where every downstream norm and
assertion sees it). Visible is visible; it need not be an exception. Only the strict reading
decides the gate:

    SILENT_WRONG := returns normally AND all values finite AND no warning emitted
                    AND wrong by more than the module's OWN existing acceptance tolerance
                        (leg 73: 5e-3 on fields, 1e-3 on the origin read)

A fourth, weaker verdict `SILENT_EMPTY` (accepted without complaint, output degenerate in
*shape*) is measured and reported but **not** used to answer the gate.

## What was found

### Headline — `u_x_at_origin` fabricates `-0.0`, 100% error, no warning

`u_x_at_origin` (lines 175-189) extrapolates `c1(r) = phi_1(r)/r^2` to `r=0` by a two-parameter
least-squares fit over the mask `(grid.r > grid.r[2]) & (grid.r < r_window)`, `r_window=0.1`.
**The mask's occupancy is never checked.** For any grid with `r_min >= r_window` the mask is
empty, `np.linalg.lstsq` on the resulting `(0, 2)` design matrix returns `[0., 0.]` at rank 0
without raising or warning, and the function returns `-2.0 * 0.0 = -0.0`.

Truth for leg 73's own manufactured field is `u_x(0) = -2` exactly.

| `r_min` | nodes in window | returned `u_x(0)` | abs error | vs leg 73's 1e-3 tol |
| --- | --- | --- | --- | --- |
| 1e-3 | 84 | -2.008611 | 8.61e-3 | 8.6x |
| 0.05 | 18 | -2.004006 | 4.01e-3 | 4.0x |
| **0.09** | **1** | **-1.783803** | **2.16e-1** | **216x** |
| **0.099** | **0** | **-0.000000** | **2.000** | **2000x** |
| 0.15 … 10.0 | 0 | -0.000000 | 2.000 | 2000x |

**Magnitudes.** Absolute error **2.000**, relative error **100.0%** — the entire signal is gone.
Against the well-posed read the degenerate read is worse by **232x**. The transition is a cliff:
`r_min` 0.09 → 0.099, a **10% change in one grid parameter**, takes the window 1 → 0 nodes and
the error up **9.25x**, with **0 warnings and 0 exceptions on either side**.

`-0.0` is not an obviously-broken sentinel. `u_x(0)` is the origin strain the modulation read of
PHASE2_SPIKE1_NOTES (2.11) depends on; a returned `0.0` reads as the physically meaningful
statement "the origin strain vanishes" and would be consumed as such. And the trigger is the
natural misuse — a grid that does not resolve the origin neighbourhood, precisely the input class
the `r=0` handling exists to reject.

The one-node case is silently under-determined too: rank-1 design matrix for a two-parameter fit,
`lstsq` returns the minimum-norm solution, error **2.16e-1** = **25x** the 84-node read, no rank
check anywhere.

### Second — a reversed radial interval hides its damage under a green global norm

`PolarGrid(r_min=40.0, r_max=1e-3)` builds without complaint. `drho = -0.02656`; the Thomas solve
sees only `drho^2` so the interior survives, but the two radial Dirichlet ends **swap**: index 0
is now the far field yet receives the near-origin regularity condition `dphi/drho = 2n phi`, and
index -1 is the singular corner yet receives the far-field decay condition `dphi/drho = -2n phi`
where the truth is `+2n phi`. The wrong analytic tail is imposed at the origin.

| grid | `drho` | rel L∞ global | rel L∞ at `r < 0.05` |
| --- | --- | --- | --- |
| ascending `[1e-3, 40]` | +0.02656 | 7.14e-5 | 2.15e-4 |
| reversed `[40, 1e-3]` | -0.02656 | **1.43e-4** | **3.30e-2** |

**Magnitudes.** Global relative error **1.43e-4** — only **2.00x** the ascending grid and
comfortably **inside** leg 73's own 5e-3 acceptance, hence invisible to every existing test.
Localized where the wrong BC bites, the error is **3.30e-2**: **154x** the ascending grid and
**6.6x outside** leg 73's tolerance. The global norm under-reports the local damage by **77x**.
This is the classic silent-corruption signature — a green global diagnostic over a destroyed
local quantity.

### Third, weak — `n_beta <= 0` silently builds an empty grid

`PolarGrid(n_beta=0)` and `PolarGrid(n_beta=-3)` both construct, yield 0 angular modes, and
`velocity_from_vorticity` returns all-finite arrays of shape `(n_r, 0)`. A missing `ValueError`,
but the degenerate output shape means a consumer cannot mistake it for a real field — classified
`SILENT_EMPTY`, not used to answer the gate.

### What IS robust — the r=0 axis proper

Every case that touches the origin singularity *numerically* makes the degeneracy visible:
`r_min = 0` (1024/1024 non-finite, 3 warnings), `r_min < 0` (1024/1024, 1 warning),
`r_min == r_max` (1024/1024, 33 warnings), `n_r = 1` (`IndexError`), one NaN in `omega`
(1024/1024 — poison propagates globally rather than being swallowed), one Inf in `omega`
(1024/1024), wrong-shaped `omega` (`ValueError` ×2), a mis-cased `radial_bc="Robin"`
(`UnboundLocalError`), and `dirichlet` without `phi_exact` (`ValueError`).

So the module's **field-level arithmetic is honest**. The failure is confined to the one place a
*reduction* happens — the least-squares origin extrapolation, where an empty or rank-deficient
input is absorbed into a zero coefficient instead of being refused.

## Relationship to leg 73

Leg 73's Lamb result **stands unweakened**. It asked whether the answer is right on a well-posed
problem and answered yes to 1.76e-4. It never asked whether a wrong answer is flagged. Both
defects found here sit outside every tolerance leg 73 set *at the point where they bite*, and
inside them *globally* — which is exactly why five passing correctness tests did not see them.

## What was banked, and a warning about it

`test_boussinesq_velocity_adversarial.py` passes against the **current, unpatched** module. Three
of its nine tests are marked CHARACTERIZATION: they pin the *defect*, not the desired behaviour.
**When the module is patched they will fail, and that failure is the fix working** — they must be
updated in the same commit as the patch. This is stated in the test file's own header so the next
reader is not misled into thinking the battery blesses the bug.

## UPDATE — bench repair (`Leg 0: ORCH`), landed bundled with this leg

The escalation below was actioned. This leg's two commits are **bundled with the fix on
`bench/fix-boussinesq-velocity-origin-fit`, so `leg/bva-v1` must NOT be merged separately.**

* **`u_x_at_origin`** now counts the origin fit window and checks the least-squares rank, and
  raises `ValueError` when the window holds fewer than `min_points` nodes (default 2, the
  well-posedness floor for the two-parameter fit) or the fit is rank-deficient — before
  `np.linalg.lstsq` can absorb a `(0, 2)` design matrix into `[0., 0.]`. The `-0.0` return
  against a truth of `-2.0` is unreachable. A new `min_points` argument lets a caller demand an
  accuracy margin above the well-posedness floor, since the default is not an accuracy
  guarantee: the 18-node read measured above is still 4.01e-3 off truth.
* **`PolarGrid.__init__`** now requires `r_min < r_max`, so the reversed interval is refused
  before any solve. This subsumes the collapsed `r_min == r_max` case, which this leg had
  measured as `NONFINITE`; raising is a strictly stronger flag than a non-finite field, so that
  one sub-case moved from `NONFINITE` to `RAISED`.
* **`n_beta <= 0` was deliberately NOT patched.** This leg classified it `SILENT_EMPTY` and
  explicitly did not use it to answer the gate; the repair was scoped to the two defects the
  gate turned on. The weak finding stays pinned as the gap it is.

**Leg 73's headline is NOT affected — verified by re-running, not by argument.** Leg 73's grids
are `r_min = 1e-3, r_max = 1e3` on the main ladder and `r_min = 1/r_max` on the truncation
study: all strictly ascending, so defect 2 never applied. Its main-ladder grids put **398 nodes**
in the origin fit window, three orders above the new floor. Its truncation study does reach
`r_min = 0.2` with **0 nodes** in the window — inside defect 1's affected range — but the
benchmark **never calls `u_x_at_origin`** (it scores P1/P3 field norms against the Lamb
corner-image closed form), so that row was never exposed. Re-running
`experiments/p2_route_bv_v1_velocity_benchmark.py` under the patched module reproduced
`writeup/data/p2_route_bv_v1_velocity_benchmark.json` **byte-for-byte**: P1 finest
**1.7584e-04**, P3 finest 1.2163e-05, observed orders **2.00, 2.00**, gate still
`YES_AND_IT_REPRODUCES`.

**Zero regression, verified.** `test_boussinesq_velocity.py` (leg 73's own five gates, including
`u_x(0) = -2.0008`), `test_boussinesq_rescaled.py` (whose `modulation` path calls
`u_x_at_origin`), `test_boussinesq_rescaled_status.py`, and `test_boussinesq_transport.py` all
pass with identical numbers. Every `PolarGrid` construction in the repository was enumerated: all
are strictly ascending, and every one that reaches `u_x_at_origin` puts 54–398 nodes in the
window. The single repo grid with a thin window — the 16×8 grid at
`test_boussinesq_rescaled_status.py:42`, 1 node — never calls the origin read, exactly as its own
comment ("the loop never solves on it") says.

**The battery is frozen, the tests carry the assertion.**
`experiments/p2_route_bva_v1_adversarial.py` and its curated JSON are deliberately left as this
leg ran them and are NOT regenerated — they are the evidence for the finding, and re-running
would erase the magnitudes that justified the repair. Against the patched module the script no
longer completes, because the cases it was built to measure now raise; a header note records
this. `test_boussinesq_velocity_adversarial.py` grew 9 → 10 tests: the three CHARACTERIZATION
tests are **inverted, not weakened** — every magnitude this leg measured is preserved in their
docstrings and only the demand flipped from "returns the wrong number" to "raises" — and one new
test pins the `min_points` lever.

## Escalation notes for the orchestrator

1. **The fix is small and belongs to the module's owner, not to this leg.** Count the mask in
   `u_x_at_origin` and raise (or return NaN) below 2 nodes; optionally check the `rank` that
   `lstsq` already returns and refuse rank < 2. Separately, validate `r_min < r_max` and
   `n_beta >= 1` in `PolarGrid.__init__`.
2. **The same mechanism is in a sibling.** `solver/boussinesq_rescaled.py:161` runs the identical
   `coef, *_ = np.linalg.lstsq(A, d1[m], rcond=None)` over a masked window. It was **not** tested
   here (out of territory) and is **not** claimed broken — but it is the same pattern in the same
   family, and after leg 89's find in `solver/boussinesq.py` this is now the **third** Boussinesq
   module implicated. A follow-up leg scoped to `boussinesq_rescaled.py` is the obvious next
   audit.
3. **Nothing downstream is retracted by this leg.** No result in the repository is known to have
   been produced through the failing path; the audit found the exposure, not a corrupted claim.

## Files

- `experiments/p2_route_bva_v1_adversarial.py` — the battery, 22 cases in three families
- `writeup/data/p2_route_bva_v1_adversarial.json` — curated data
- `test_boussinesq_velocity_adversarial.py` — 9 permanent regression tests
- `writeup/novelty/leg_99.md` — novelty pass and full findings

No figure required by the leg contract, and none produced.
