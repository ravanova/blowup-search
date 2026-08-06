# Leg 89 — Route-BOA: adversarial audit of the physical-space 2D Boussinesq solver

**Agent:** LEG-I. **Branch:** `leg/boa-v1`. **Date:** 2026-08-06. **Claim-bearing.**
**Module under test:** `solver/boussinesq.py` — **read, never edited, under every gate outcome.**

## Gate and answer

> "Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
> degenerate/zero stream function, extreme grid-stretching), does `solver/boussinesq.py` ever
> silently return a finite, plausible-looking result instead of propagating or flagging the
> invalid input?"

**YES — 19 silent-corruption cases out of 82 gate-deciding, plus 4 of 8 secondary.**
`yes` branch: **a silent-corruption gap. ESCALATED, not patched.** The module is untouched.
The branch is pushed and held for the orchestrator; it is **not** merged to `main` by this leg.

## Order of work

1. `plan_of_record.py` read in full; no ban touches this leg (it measures no model — it audits
   one module's error handling — so it is not a gCLM measurement, not Route-D bound-sharpening,
   not a DSS re-ask, not a beta re-measurement, no GA compute). The standing "grep
   `capabilities.py` before building" ban was honoured first: the `solver/boussinesq.py` entry at
   line 392 is quoted in the novelty pass.
2. **Novelty pass run and committed BEFORE construction** (`writeup/novelty/leg_89.md`, commit
   `95d516e`). It established that no file in the repository had ever passed a non-finite value,
   a degenerate grid size, or an out-of-domain coefficient into `solve_boussinesq`; that leg 66's
   `check_solve_rejects_bad_arguments` covers exactly four *well-formed* wrong-shape/wrong-label
   inputs; and it **pre-committed the definition of SILENT CORRUPTION and the mapping of the
   gate's third clause** before any number was seen.
3. Battery built and run: `experiments/p2_route_boa_v1_adversarial.py` → curated data
   `writeup/data/p2_route_boa_v1_adversarial.json`, **90 cases, 84 s**.
4. Banked: `test_boussinesq_adversarial.py`, 12 gates (2 soundness, 7 characterization,
   3 control), all passing.

## The predicate, fixed before the run

Returns **normally** (no exception) AND every field a caller reads to judge validity — `outcome`,
`conservation_drift`, `mean_drift`, `energy_balance_residual`, the `max_omega` trajectory — is
**finite and plausible** AND the run is nevertheless invalid, because either the returned state is
non-finite, or an invalid parameter was silently **dropped** while `params` records the ignored
value. **Loud failure is a pass in any form** (raise, `diverged`/`under_resolved`/`max_steps_hit`,
or a NaN reaching a field the caller reads). **A dull-but-correct answer is a pass.** Every
`silent` verdict carries an independent **witness** — bit-for-bit array equality against the
neutral-parameter control for a dropped parameter, the represented initial state recomputed
through the module's own dealias mask for a wrong label. "Both are small" was never accepted.

Gate clause 3 ("extreme grid-stretching") was **mapped before the run**: `solver/boussinesq.py` is
a *uniform* 2π-periodic pseudo-spectral code with no grid-stretching parameter at all, so the
clause was mapped to the nearest thing in kind — degenerate `n`, and `dt_max`/`c1`/`c2`/`nu`/`kappa`
out of domain. Dropping the clause because the literal words do not apply would have answered an
easier question than the one dispatched.

## Magnitudes

| family | cases | silent | the magnitude |
|---|---|---|---|
| A — degenerate/zero stream function | 8 | **6** | false `blowup_candidate` off a represented `m0` of **1.797e-16**; amplification **5.566e+13** (and **1.0e+298** at amplitude 1e-300) |
| B — NaN/Inf-seeded vorticity | 30 | **0** | all 30 reach `diverged` in 1 step — the module's one genuinely robust path |
| C — NaN/Inf-seeded temperature | 15 | 0 (12 propagated, 3 flagged) | `theta_final` **100% NaN** while `conservation_drift` reports **8.077e-18** and `drift_guard=1e-9` never fires |
| D — out-of-domain `nu`/`kappa` | 13 | **8** | 5/5 `kappa` values **bit-identical** to the `kappa=0` run, energy residual ratio **1.000** |
| E — degenerate grid / discretization | 16 | **5** | `n=1,2` retain **1 mode** and report `drift = 0.0`; `c1=c2=nan` relaxes `dt_min` **168.8×** |
| F — detection thresholds (secondary) | 8 | **4** | `amplification_factor=nan` runs past a **4.013×** amplification reporting `no_blowup` |

`conservation_drift` masks a NaN limb in **13 of 90** cases.

## The four defects, in order of severity

1. **False `blowup_candidate` from a vorticity that is zero in the represented subspace.**
   `omega0 = sin(15x)sin(15y)` at `n=32` lies entirely above the 2/3 dealias cut (`n/3 = 10.67`).
   The represented field is zero to roundoff — `max|w| = 1.797e-16`, **not** `0.0` — so the
   documented `omega0 is identically zero` guard, which tests `== 0.0` exactly and **does** fire
   on a bit-zero field (control confirms), misses it by 1.8e-16. The trigger is then
   `amplification_factor * m0 = 1.797e-13`, and the ordinary O(1) buoyancy forcing `th_x` clears
   it in **one step**. Returned: `outcome="blowup_candidate"`, `mean_drift=5.28e-18`,
   `energy_balance_residual=1.30e-10`. This is the most consequential label this repository's
   solver can emit, produced by a textbook-healthy-looking run on a benign spin-up. Same defect at
   `amplitude 1e-300` (amplification **1.0e+298**) and `1e-18`.

2. **`kappa` out of domain is dropped without a trace.** `if kappa > 0.0` means `kappa ∈
   {-0.5, -1e6, -1e-14, nan, -inf}` is neither applied nor rejected: all five return `omega_final`
   and `theta_final` **bit-identical** to the `kappa=0` control, with `energy_balance_residual =
   2.2188e-07`, *exactly* the control's value (ratio **1.000**), while `params["kappa"]` records
   the ignored value. There is no tell, because the module's energy identity
   `dE/dt = ∫vθ − ν∫ω²` does not contain `kappa` and **structurally cannot see it**.
   **Measured contrast:** `nu` is dropped the same way, but the same identity *does* contain `nu`,
   so `nu=-0.5` moves the residual to **4.3812e-01**, a factor **1.9745e+06**, and `nu=nan` makes
   it NaN outright (hence *propagated*, not silent). The guard catches the `nu` half by accident
   of the identity's shape and misses the `kappa` half entirely.

3. **`conservation_drift` masks a NaN limb.** Documented at `solver/boussinesq.py:141` as "max of
   the two above; the logged guard value", built with Python's builtin `max`, which is
   order-dependent on NaN. With a NaN-poisoned `theta0` and `buoyancy=False`: `theta_final` 100%
   NaN, `energy_balance_residual` NaN, `conservation_drift` **8.077e-18** — and the identical
   `max()` inside the loop means `drift_guard=1e-9` **never fires**. Same builtin-`min` defect on
   the timestep: a non-finite `c1`/`c2` **removes** its CFL limb instead of failing, relaxing
   `dt_min` from 1.7774e-03 to 9.9324e-03 (**5.588×**, 30 steps → 10) and, with both NaN, to a
   single step of 0.3 (**168.8×**, energy residual **801.7×** the control but still only 1.9e-03
   in absolute terms — small enough to read as healthy).

4. **Degenerate grids run happily, and non-finite detection thresholds are inert.** `n=1` and
   `n=2` leave the mask retaining exactly **one** mode (the (0,0) mean), so the method has no
   spatial resolution whatsoever, yet both return `no_blowup` over 30 steps with `mean_drift=0.0`
   and `energy_balance_residual=0.0` — the most reassuring numbers in the battery, from a
   discretization that cannot represent any dynamics. Secondary: `amplification_factor=nan/inf`
   disables blow-up detection outright (control at 2.0 fires `blowup_candidate` at `t=3.140`; the
   same trajectory with `nan` runs to `t=6.0` reporting `no_blowup` at a peak amplification of
   **4.013**), and `t_max=nan`/negative returns `no_blowup` from a **zero-step** run.

## What was measured and deliberately NOT used

`n_runtime_warnings` is recorded per case but **decides nothing** and is a lower bound: numpy's
C-level once-per-location warning registry is not reliably reset by `simplefilter("always")` —
verified to report 0 on a case that does warn on a fresh interpreter. The "silently" half of the
gate is decided **structurally**, on whether every validity field is finite and plausible, which
needs no warning instrumentation and is unambiguous here: the silent cases perform no non-finite
arithmetic at all, their returned states being 100% finite.

## Scope, and what this does NOT say

- **No mathematical claim.** Nothing is discovered about the Boussinesq system or blow-up; no link
  of the L1→L4 chain moves. This can only withdraw confidence.
- **No Phase-1 result is retracted by this leg.** Every defect requires a malformed input. The
  question of whether any *landed* Phase-1 Boussinesq run supplied one is **not** answered here —
  it is outside this leg's territory and is the first thing the orchestrator should route.
  Defect 1 is the one that could in principle have produced a spurious `blowup_candidate` in a
  real sweep; defect 2 is the one that could silently have run an inviscid-in-θ integration under
  a viscous label.
- **The module was not edited.** Not one character of `solver/boussinesq.py` changed. The repair
  is deliberately left to a leg with the authority to make it; each characterization test names,
  in its docstring, the assertion that should replace it once the fix lands.

## Files

- `experiments/p2_route_boa_v1_adversarial.py` — the 90-case battery
- `writeup/data/p2_route_boa_v1_adversarial.json` — curated data, every case's validity fields
- `test_boussinesq_adversarial.py` — 12 permanent gates (2 soundness, 7 characterization, 3 control)
- `writeup/novelty/leg_89.md` — novelty pass (committed pre-construction) + findings

---

## STATUS UPDATE, 2026-08-06 (appended by the bench repair; leg 89's report above is unchanged)

**All four defects are repaired.** `solver/boussinesq.py` was patched on
`bench/fix-boussinesq-silent-corruption` ("Leg 0: ORCH", a repo-wide bug fix, not a leg).
Leg 89's report above is left exactly as written, as the record of the pre-fix measurement.

Re-running **this leg's unchanged 90-case battery** against the repaired module:

| | pre-fix (leg 89) | post-fix |
|---|---|---|
| gate answer | **YES** | **NO** |
| silent, gate-deciding | 19 of 82 | **0** |
| silent, secondary | 4 of 8 | **0** |
| `conservation_drift` masks a NaN limb | 13 of 90 | **0** |

`writeup/data/p2_route_boa_v1_adversarial.json` is deliberately **not** regenerated — it is
this leg's banked evidence of the pre-fix module. The post-fix run, the zero-regression A/B
against the pre-fix module loaded from git (19 of 19 well-formed cases bit-identical), and
the Phase-1 contamination audit are in
`writeup/data/bench_boussinesq_silent_corruption_check.json`.

**The question this leg flagged as "the first thing the orchestrator should route" is
answered: NO banked Phase-1 result is contaminated, and no rework leg is needed.**

- **Defect 2 (`kappa` dropped):** all **5** `solve_boussinesq` call sites in the repository
  pass `kappa = 0.0` — literal at `phase1_axis_screen.py:121`, `phase1_currency_probe.py:95`,
  `phase1_gsustained_probe.py:96`, defaulted at `phase1_resolution_spike.py:94`, and
  `FITNESS2D_DEFAULTS["kappa"] = 0.0` at `ga/fitness2d.py:71`. That is *in* domain. No banked
  run ever executed an integration different from the one its `params` record.
- **Defect 1 (false `blowup_candidate`):** the defect needs a represented `m0` at roundoff
  relative to the state scale (this leg's witness: **1.797e-16**). Measured directly for every
  Phase-1 initial condition at every banked resolution (smooth_sharp, smooth_mild, rough h=0.5,
  rough h=0.3 at N = 128/256/512/1024): the **worst** ratio is **1.0e-01**, a factor **1e+12**
  above the new tolerance. No Phase-1 IC is within twelve orders of magnitude of the defect's
  precondition.
- **No banked artifact records a `solve_boussinesq` `blowup_candidate`** at all. The only
  `blowup_candidate` strings in `writeup/data/` are `stage3_6_rough.json` (1D gCLM, via
  `solver/gclm.py` — a different module) and this leg's own artifact. Banked Phase-1 outcomes
  are `under_resolved` and `no_blowup` only.
- **End-to-end reproduction:** `phase1_spike.json`'s N=128 column re-run against the repaired
  module reproduces **4 of 4** ICs exactly — worst absolute difference **0.0** in both
  `t_resolved` and `amp_resolved`, outcomes identical.

`test_boussinesq_adversarial.py`'s seven `test_characterize_*` gates are converted to
`test_repaired_*` and **inverted, not weakened**: every magnitude this leg measured is still
computed at the same threshold, and each docstring keeps the pre-fix numbers. 12/12 pass.

**`leg/boa-v1` must NOT be merged separately** — its two commits are bundled into
`bench/fix-boussinesq-silent-corruption`, the same pattern
`bench/fix-port-certification-validation` used for leg 79.
