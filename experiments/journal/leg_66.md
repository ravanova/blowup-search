# Leg 66 — Route-QF v1: dedicated tests for the three indirectly-covered solver modules

**Branch** `leg/qf-v1`. **Exploration leg** (light, hygiene). **Gate: YES — a real defect,
local to `solver/spectral_utils.py`, found only because the module was tested directly.**

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. Every live ban noted; the binding one is **"another gCLM
   measurement leg"**. This leg runs no measurement: it changes no parameter, runs no
   sweep, and every target value it asserts is a closed form or a structural invariant of
   code that already exists. Also noted and obeyed: **"building a solver without grepping
   `capabilities.py` for the object first"** — this leg's whole premise is a line in
   `capabilities.py`, grepped first (see 3).
2. `DIRECTION.md` — **has no leg 66 entry.** Grepped for `leg 66`, `leg_66`, `Route-QF` and
   `LEG-J` in both `DIRECTION.md` and `ORCHESTRATION.md`: zero hits. The thesis and the
   verbatim gate came from the dispatch prompt instead. **Flagged for the orchestrator**,
   same flag leg 57 raised: the queue entry the leg is supposed to read does not exist.
3. **Novelty pass FIRST**, committed before a line of test was written
   (`writeup/novelty/leg_66.md`, commit `125111e`). For a hygiene leg the pass is a
   coverage audit, not a literature sweep — the premise to confirm is factual, not novel.
4. Three test files, written and run in order: `spectral_utils`, `gclm`, `boussinesq`.

## What the novelty pass changed about the leg

Two things, both of which narrowed it.

**`capabilities.py` undercounts the indirect coverage.** It names one test file per module.
The truth: `spectral_utils` is imported by 4 test files, `gclm` by 4, `boussinesq` by 10.
So the leg could not be sold as "these modules are untested".

**But seven public symbols are named by ZERO of the repository's 52 test files** —
`dealias_mask`, `velocity_hat`, `derivative_hat`, `l1_norm`, `energy_production`
(spectral_utils), `energy_from_gradient` (gclm), `project_even_odd` (boussinesq). Five of
those seven run thousands of times per solve. They are covered in the sense that a
*catastrophic* error would break an end-to-end blow-up-time fit, and in no stronger sense.
That is the gap the leg aimed at, and it is where the defect turned out to be.

## The finding

**`solver/spectral_utils.derivative_hat` returns a wrong derivative on odd-length grids.**

```python
def derivative_hat(w_hat, k):
    d = 1j * k * w_hat
    if len(w_hat) > 1:
        d[-1] = 0.0          # <-- unconditional
    return d
```

Zeroing the last `rfft` coefficient is the standard, correct treatment of odd derivatives
of real fields **when n is even**, because that entry is then the Nyquist mode. When n is
**odd there is no Nyquist mode**: `rfftfreq` runs `0 .. (n-1)/2`, the last entry is an
ordinary fully-resolved wavenumber, and zeroing it destroys it outright.

Magnitudes, all measured, none inferred:

| datum | grid | relative sup error |
|---|---|---|
| `sin(((n-1)/2)·x)`, derivative | n = 17, 65, 129 | **1.000** (returns identically zero, max abs 1.8e-14) |
| `sin(x) + 0.1·sin(32x)`, derivative | n = 65 | **7.62e-01** |
| `exp(sin x)`, derivative | n = 65 | 7.31e-15 — unaffected |
| `energy_from_gradient(sin(32x))` | n = 65 | got **2.56e-26**, exact 1.6085e+03 → **1.000** |
| `energy_from_gradient(sin(64x))` | n = 129 | got 5.50e-25, exact 6.4340e+03 → **1.000** |
| `energy_production(sin(32x), a=0, nu=0.1)` | n = 65 | got 3.07e-15, exact −3.2170e+02 → **1.000** |
| same quantities | n = 64, 128 | 4.5e-16, 2.9e-15, 3.8e-16 — correct |

**Blast radius: latent, not active.** Every call site in this repository passes an even n
(surveyed: 8, 12, 32, 64, 128, 256, 512, 1024). **No recorded measurement is affected**, and
the leg claims no correction to any number in the ledgers.

**Why it is still worth reporting with urgency.** The error is invisible on smooth data
(7.3e-15) and total on grid-scale data (1.000). A blow-up study is precisely a study of
fields that develop grid-scale content. Any future leg that reaches for an odd resolution —
to break a symmetry, to test resolution independence off the powers of two, to place a
collocation point at a grid centre — inherits a silently wrong `w_x`, a silently wrong
dissipation integrand, and therefore a silently wrong `energy_balance_residual`, which is
one of the two artifact-guard numbers every run logs. The guard would be reporting on a
quantity it had itself corrupted.

**Not fixed here.** Under this leg's territory rules a bug in `solver/` is reported, not
silently patched. Both affected tests pin the CURRENT behaviour and record the corrected
reference beside it, so the day someone makes `d[-1] = 0.0` conditional on `n % 2 == 0`,
those two tests fail and hand them the replacement assertion.

**The 2D module is clean.** `solver/boussinesq.py` builds `i·KX` from a full `fft2` and has
no such special case: measured relative sup error 5.9e-15 at n = 17 and 7.3e-15 at n = 33,
against 1.000 for the 1D helper. Recorded as
`check_derivative_odd_n_is_correct_here`, so the contrast is on file and the defect is
correctly localized to one line of one module.

## What was checked and found sound

41 checks, all passing.

- `test_spectral_utils_dedicated.py` (10 checks) — grid non-duplication of the endpoint;
  integrality of `wavenumbers` at even and odd n; the 2/3 cut counted exactly, including
  that `k = n/3` is **retained** at n = 96; the Hilbert sign convention against
  `H(sin) = −cos` and `H(cos) = sin`; `H² = −Id` (4.1e-16) and skewness (4.0e-16);
  `velocity_hat` verified by `u_x == H(w)` (9.4e-16) with zero mean (6.9e-18);
  `energy_production` against an **independently built** analytic reference across five
  `(a, nu)` pairs (≤4.2e-16) plus the affine-in-`a` structure.
- `test_gclm_dedicated.py` (14 checks) — the RHS on hand-computed data; **`sin x` is an
  exact stationary point of De Gregorio (a = 1)**, RHS max abs 2.1e-15, and the solver
  holds it for t = 5 to 2.6e-15 (this is the sharpest available check on the relative sign
  and scaling of the two nonlinear terms, and no existing test asks it — the only a ≠ 0
  check in `test_solver_clm.py` freezes u, which switches that term off); dealiasing shown
  to remove a product that lands above the cut while an O(1) unmasked value confirms it was
  not merely small; `clm_analytic_blowup_time` against **hand-derived** T* on five data
  (≤2.8e-16) plus its never-exercised `None` branch; pure diffusion exact to 3.1e-15 and
  **independent of dt** to 5.3e-15 across a 100× step-count ratio (`test_solver_clm.py`
  allows 1% here); the `SolverResult` contract and the `max_steps_hit` / `blowup_candidate`
  / `decay_exit` branches, the last saving 10× the steps.
- `test_boussinesq_dedicated.py` (17 checks) — the `indexing='ij'` convention pinned;
  Biot–Savart on three hand-solved modes (≤5.6e-16) plus divergence-free (5.1e-16) and
  curl-inversion (4.2e-16); `_reflect` as a commuting involution; the parity projectors
  shown to be **genuine orthogonal projectors** (idempotent 2.2e-16, mutually annihilating
  5.6e-17, L² orthogonal 1.4e-14) and exact on their own basis functions; all four
  `ValueError` branches; both `under_resolved` guards fired **and** shown not to fire
  spuriously; `symmetry="houluo"` shown to project the *initial* data too, taking an input
  parity residual of 0.300 to an output residual of 3.3e-16.

## Gate

> "Do the new dedicated tests find any discrepancy — an assertion failure, a numeric
> mismatch, or a code path the indirect tests never exercised producing a wrong answer —
> versus what test_solver_boussinesq.py / test_solver_clm.py currently assume?"

**YES.** One numeric mismatch, in a code path the indirect tests never exercise: the
odd-`n` branch of `solver/spectral_utils.derivative_hat`, relative sup error 1.000, and its
two downstream consumers `energy_from_gradient` and `energy_production` at the same
magnitude. Localized to one line. Latent under current call sites.

## For the orchestrator

1. **`solver/spectral_utils.py:derivative_hat` needs `d[-1] = 0.0` guarded by `n % 2 == 0`**
   (equivalently, by whether the last entry is the Nyquist mode). Independent of NG. Not
   done here — territory rules. Two pinned tests will fail when it is done; that is the
   handshake, and the corrected reference values are already in them.
2. **`capabilities.py`'s three `"validated"` fields are now false** for
   `solver/boussinesq.py`, `solver/gclm.py` and `solver/spectral_utils.py`: each has a
   dedicated test file. Left unedited — the shared index is integration-owned, and the
   correct new text depends on how item 1 is resolved. Suggested replacements:
   `"dedicated: test_boussinesq_dedicated.py (17 checks) + test_solver_boussinesq.py"`,
   `"dedicated: test_gclm_dedicated.py (14 checks) + test_solver_clm.py"`,
   `"dedicated: test_spectral_utils_dedicated.py (10 checks); ODD-n derivative_hat defect
   pinned, leg 66"`.
3. **`DIRECTION.md` still has no entry for this leg.** Second leg in a row to report this.

## Science content

**None, by construction.** No parameter changed, no sweep run, nothing enters the Clay
estimate. Clay stays at ~0.05% behind Walls 1 and 2. The banked value is one localized
defect report and 41 assertions that did not exist yesterday.
