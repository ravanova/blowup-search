# Leg 92 novelty pass — Route-GLA: adversarial audit of `solver/gclm.py`

Run BEFORE construction, per the leg contract. Nothing below was written after seeing a result.

## Question being claimed (the gate, verbatim)

> "Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
> degenerate transform input, extreme `a`), does `solver/gclm.py` ever silently return a finite,
> plausible-looking result instead of propagating or flagging the invalid input?"

## In-repo prior art

| source | what it covers | overlap with leg 92 |
|---|---|---|
| `test_gclm_dedicated.py` (14 checks, leg 66 / Route-QF) | RHS on a single CLM mode, De Gregorio stationary mode, frozen-u transport, dealiasing, `energy_from_gradient` (even and odd N), the closed-form CLM blow-up time and its no-blow-up branch, zero-data rejection, the `SolverResult` contract, the early-decay exit, pure-diffusion exactness, mean invariance | **none on the gate's question.** `grep -ci 'nan\|inf\|adversarial\|malformed'` over the file returns **0**. Every one of the 14 checks feeds a finite, band-limited, well-formed `omega0` and a finite in-range `a`. It is a correctness check, not a robustness check. |
| `test_solver_clm.py` | the older CLM-path consumer test | 1 grep hit, and it is the word "infinity" inside a comment about the analytic solution — no non-finite input is ever constructed |
| leg 66 (`writeup/novelty/leg_66.md`) | the test-coverage census that *created* `test_gclm_dedicated.py` | it is the thing this leg complements; the census explicitly scoped itself to "does the module compute what it claims on data it was designed for" |
| leg 89 (Route-BOA) | adversarial audit of `solver/boussinesq.py`, the sibling physical-space module, also covered by leg 66 | same pattern, different module. Establishes precisely the correctness-vs-robustness distinction this leg re-applies. Not landed on this leg's merge base; no file collision either way |
| leg 88 (Route-GCA), `test_gclm_family_adversarial.py`, `experiments/p2_route_gca_v1_adversarial.py` | adversarial audit of `solver/gclm_family.py` — the **rescaled steady residual**, a different module | different object: leg 88 audits an algebraic residual evaluator with poisoned *gauge coefficients*; this leg audits a *time-stepping initial-value solver* with poisoned *physical-space fields*. No overlapping code path (leg 88 never calls `solve_gclm`, `_nonlinear_rhs_hat`, or `clm_analytic_blowup_time`) |
| leg 91 (Route-FGA) | adversarial audit of `solver/fractional_gclm.py` | sibling in the same audit family; different module, different territory |
| legs 69, 79, 80, 83, 85 | adversarial audits of `solver/interval.py`, the port certification, `solver/bordered_hl.py`, and two others | same *pattern*, different modules |
| `test_bordered_hl_adversarial.py`, `test_target_norm_adversarial.py`, `test_gclm_family_adversarial.py` | the adversarial batteries on main at this merge base | none names `solver/gclm.py`; `test_gclm_adversarial.py` does not exist |

Consumer sweep: `grep -rl 'solve_gclm\|clm_analytic_blowup_time'` finds 15 files
(`ga/fitness.py`, `ga/resolution_study.py`, `nongenericity_sweep.py`, the five stage sweeps,
`writeup/curate_evidence.py`, `solver/boussinesq.py`, and the two tests above). Every one of
them is a *producer of well-formed data* — sweeps generate genomes from a smooth Fourier basis.
Not one constructs a non-finite field, a rank-degenerate Hilbert input, or an out-of-range `a`.

**The question is unasked in this repository.**

## Ban check (`plan_of_record.py`, run at leg start)

The live ban list has ten entries. The one that could bite:

> "another gCLM measurement leg (lifted by: never — the model is exhausted (Stage 3.5, leg 42))"

This leg is **not** a gCLM measurement leg, and I verify that independently rather than inheriting
legs 83/85/88's ruling. It produces no new physics quantity about the gCLM model: no `a`-sweep
verdict, no self-similar exponent, no blow-up threshold, no genome, no profile. What it measures is
**the response of a piece of Python to invalid input** — the failure-flagging behaviour of
`solve_gclm` and `clm_analytic_blowup_time`. Where it does step the solver, the runs are
deliberately degenerate (poisoned or constant fields) and their *physics* is discarded; only the
outcome label and the finiteness of the returned arrays are read. It reads `solver/gclm.py` and
edits it under **no** gate outcome, as the contract requires.

The other nine bans are checked one by one and none touches an input-validation audit: Route-D
bound sharpening (no bounds here), DSS re-ask (no DSS), 2D beta (1D module), the scaling gauge as
near-null direction (no linearization), GA compute on unvalidated fitness (no GA is run — `ga/`
is read for consumer census only, never invoked), the four leg-51/53 reading bans (no claim about
`Y_0`, `Z_1`, the weight exponent `s`, or leg 51's methodological finding), and Chen-Hou's 2D
profile as a target (not a target here).

The tenth ban — "building a solver without grepping `capabilities.py` for the object first" — is
discharged before construction: `capabilities.py:402-406` registers

    {"module": "solver/gclm.py", "object": "gCLM, physical space",
     "validated": "dedicated: test_gclm_dedicated.py (14 checks) + test_solver_clm.py; ...",
     "test": "test_gclm_dedicated.py"}

No adversarial or input-validation capability is registered against it, and no other module in
`capabilities.py` exposes a reusable validation layer for physical-space fields. Nothing is being
rebuilt: the battery calls the registered entry points and adds no solver of its own.

## External literature

The claim is an engineering property of one file in this repository — whether a specific Python
function propagates a NaN or swallows it. It makes no mathematical statement about the gCLM
equation, so there is no external precedence question to resolve and no arXiv claim to scope
against. (Contrast leg 57 / VER-D, where the claim *was* mathematical and Cadiot
arXiv:2505.03091's scope had to be settled first.)

## Verdict

**Novel within the repository. Proceed to construction.**

---

# Leg 92 findings (written after the run)

## Gate answer: **YES** — a silent-corruption gap. Escalated, not patched.

> "Under an adversarial battery of malformed physical-space inputs (NaN-seeded vorticity,
> degenerate transform input, extreme `a`), does `solver/gclm.py` ever silently return a finite,
> plausible-looking result instead of propagating or flagging the invalid input?"

**Yes. 19 silent corruptions in 54 gate-scoped cases, across 4 independent mechanisms.**

Per family: `amplitude_invariant` 11/18, `viscosity_guard` 1/5, `guard_swallows_nan` 2/3,
`config_poisons` 5/6, `nan_seeded_vorticity` 0/12, `extreme_a` 0/10.

`solver/gclm.py` was **not edited**, under this or any outcome, exactly as the contract requires.

---

## G1 — the headline. An **absolute** zero-tolerance on data whose scale is never measured.

`solver/gclm.py:289`, inside `clm_analytic_blowup_time`:

```python
exact = np.abs(w0) < 1e-12
```

This decides which grid points count as zeros of `w0`. The CLM blow-up time is
`T* = 2 / max{ H(w0)(x) : w0(x) = 0 }` — a maximum over the **zero set**. When the amplitude of
`w0` falls below `1e-12`, *every* grid point passes that test, so the maximum is taken over the
**whole grid** instead, and the function returns `2 / max_x H(w0)(x)`.

The ruler is exact and stated before the measurement: the CLM closed form
`w = 4 w0 / ((2 - t H(w0))^2 + t^2 w0^2)` is exactly homogeneous of degree −1 in amplitude, so
`eps * T*(eps * w0)` must be **independent of `eps`**. Measured on
`w0 = sin x + 0.5 sin 2x` (chosen because its zero-set max of `H` is 0.5 while its global max is
0.75 — for `sin x` alone the two coincide and the defect is invisible), `n_scan = 4096`:

| amplitude `eps` | `eps * T*(eps w0)` | rel. violation of the exact invariant |
|---|---|---|
| 1e-1 | 4.000000000000 | 3.32e-13 |
| 1e-2 … 1e-4 | 3.999990587647 | 2.35e-06 ← root-finder noise floor |
| 1e-5 | 3.999915291346 | 2.12e-05 |
| 1e-6 | 3.999397750761 | 1.51e-04 |
| 1e-7 | 3.997282745892 | 6.79e-04 |
| **1e-8** | 3.986481281344 | **3.38e-03** ← first case past threshold |
| 1e-9 | 3.938261714174 | 1.54e-02 |
| 1e-10 | 3.733612200476 | 6.66e-02 |
| 1e-11 | 3.099789842164 | 2.25e-01 |
| 3e-12 | 2.694668336966 | 3.26e-01 |
| **≤ 1e-12** | **2.666667364087** | **3.3333e-01 — saturated** |

The exact answer is `4.0`. At and below amplitude `1e-12` the function returns a **finite,
positive, entirely ordinary-looking** blow-up time that is **1.5× too early**, with no exception,
no warning, no `None`, and no field in the return value that admits anything happened.

**The mechanism is confirmed independently, not inferred from the symptom.** Computed directly
from the profile: global max `H` = 0.7499998, max `H` over the true zero set `{0, π}` = 0.5, so
the ratio of the wrong answer to the right one is `(2/0.75)/(2/0.5) = 2/3` — i.e. a relative
violation of exactly **1/3**, which is what the saturated rows measure (0.3333332). Root-finder
noise does not saturate at an analytically predicted constant.

### Criterion correction, recorded rather than hidden

This family was first written with a fixed silent-corruption tolerance of `1e-9`, and on the first
run it flagged **16 of 17** cases — including `eps = 1e-2`, which is not a degenerate amplitude by
any standard. That criterion was miscalibrated by me, not violated by the module: the zero-finder
does 60 bisection steps on a dense trigonometric interpolant and has its own noise floor. The
floor is now **measured**, on the moderate decades `eps ∈ [1e-1, 1e-4]` where an absolute `1e-12`
tolerance provably cannot reach the grid (near a simple zero the profile has slope ~1.5·eps, so
`|w0| < 1e-12` demands `|x − x0| < 6.7e-11` while the grid spacing is `1.5e-3`). Measured floor:
**2.353e-06**. Threshold set three decades above it: **2.353e-03**. That drops the count from 16
to 11 and moves the onset from `1e-2` to `1e-8`. The surviving evidence is stronger than the
discarded evidence: a monotone ramp over six decades ending at an analytically predicted constant.

---

## G2 — `if nu > 0.0` silently drops an ill-posed viscosity

`solver/gclm.py:164` gates the integrating-factor dissipation step behind `if nu > 0.0`. A
**negative** `nu` fails that comparison, so an anti-diffusive (ill-posed) request silently runs
**inviscid** and returns `outcome="no_blowup"` with an entirely finite payload.

Measured: `nu = -1.0` returns `omega_final` **bitwise identical** to the `nu = 0.0` run
(`max|Δ| = 0.0` exactly), while a genuine `nu = 0.01` separates from inviscid by `7.364e-03`. The
only trace anywhere in the result is the energy-balance residual sitting at **4.163e+05×** its
baseline — because `energy_production` *does* use `nu` even though the evolution did not.

Reported at full strength but **not counted**: `nu = nan` and `nu = -inf` also produce a
bitwise-inviscid trajectory (dissipation silently dropped), but their `energy_balance_residual`
field comes out `nan`/`inf` respectively, so the poison does reach the caller through one field.
The trajectory is silently wrong; one guard field is honest. Under the pre-stated rule that is
FLAGGED, and I kept the rule rather than moving it.

Also corrected, and recorded: the first draft of this criterion counted `nu = -0.0` as a silent
corruption. That was a false positive — `-0.0 == 0.0`, so skipping dissipation is *correct*. Only
`nan` and strictly-negative `nu` are invalid inputs. Count dropped 2 → 1.

---

## G3 — the artifact guard reports clean while its own input is NaN

`solver/gclm.py:226`:

```python
conservation_drift=max(mean_drift, energy_residual)
```

Python's builtin `max(a, b)` returns `b` only if `b > a`, and NaN loses every comparison — so
`max(finite, nan) == finite`. Measured at `a = 1e12` and `a = 1e16`: `energy_balance_residual` is
`nan`, yet the **logged** guard value `conservation_drift` reads `4.926e-17` and `1.187e-16` —
i.e. "clean" — on runs that reached `max|w| = 9.673e+144` and `9.673e+204`. The one number
LOGGING.md's `solver_run` event records as the artifact guard is precisely the one that swallows
the NaN. (At `a = 1e8` the residual is still finite, `1.181e+90`, and the guard reports it
honestly — so the failure switches on exactly when the residual overflows.)

---

## G4 — every stop criterion is a bare comparison, so NaN disables it

`t_max = nan` → `while t < nan` is `False` → **zero timesteps**, and the function returns
`outcome="no_blowup"`, `t_final=0.0`, `conservation_drift=0.0`, every field finite: a clean
"no blow-up" verdict from a run that never happened. Same for `t_max = -1.0`. `c1=nan`, `c2=nan`
and `amplification_factor=nan` are each silently ignored.

The sharp form: **a NaN detector threshold suppresses a real detection.** With `a = 1e4`, the
clean run returns `blowup_candidate` (reaching `7.690e+24` in one step); poisoning only
`amplification_factor` flips the verdict to `diverged`. The blow-up detector — the thing this
whole repository exists to trust — is disabled by a NaN in its own threshold, silently.

Only `dt_max = nan` propagates honestly (`diverged`).

---

## What is genuinely robust (banked, not a gap)

- **NaN/Inf-seeded vorticity is flagged.** All 12 cases (nan/+inf/−inf × one node / three nodes /
  everywhere) reach `outcome="diverged"` on the **first step**, with a non-finite payload. The
  physical-space poison the leg thesis expected to find swallowed is in fact propagated.
- **Extreme finite `a` is not clamped.** `a = 1e4…1e16` gives `max|w|` = 7.690e+24, 9.672e+84,
  9.673e+144, 9.673e+204 — monotone, unsaturated, honestly enormous, all `blowup_candidate`.
  A big honest number is not corruption.
- **Non-finite `a`** (`nan`, `±inf`, `1e300`) all reach `diverged`.
- **Structural adversaries raise**: identically-zero `omega0` → `ValueError`; a length-mismatched
  profile function → `ValueError`.

## Out of gate, reported separately and not used to decide the gate

An all-NaN profile makes `np.sign(nan)` non-zero at every node, so `np.diff(np.sign(...)) != 0`
holds **everywhere** and the root list degenerates from O(1) to O(n_scan), each root costing 60
bisections of a dense trigonometric evaluation. Wall-clock ratio against the clean profile:
12.9× at `n_scan=64`, 28.7× at 128, 52.9× at 256, 111.6× at 512 — growing linearly in `n_scan`.
At the module's default `n_scan=4096` this is minutes, not milliseconds. A cost blow-up, not a
correctness claim; recorded under `out_of_gate` in the JSON.

## Blast radius — measured, and deliberately *not* overclaimed

**No banked repository result is corrupted by any of these four gaps.**

- The only production consumer of `clm_analytic_blowup_time` is `stage1_5_sweep.py:369`, and
  `stage1_5_sweep.py:174-181` **energy-normalizes every initial condition** to
  `ENERGY_TARGET = π/2` (the L2 energy of `sin x`) before it is ever used. Amplitudes are O(1),
  roughly **eight decades above** G1's onset at 1e-8.
- Every `solve_gclm` caller (`ga/fitness.py`, `ga/resolution_study.py`, `nongenericity_sweep.py`,
  `stage1_5/2_5/2_6/3_6_sweep.py`) passes `nu = 0.0` or a non-negative bisected `nu`, never NaN
  and never negative — G2 and G4 are unreachable from them.
- G3 requires `a` large enough to overflow the energy residual; no sweep goes past `a ≈ 1`.

These are **latent** gaps: real, reachable by any future caller, and invisible to the existing
test suite — not an active contamination of results already on main. Saying otherwise would be
the overclaim this repository's own lessons ban.

## Disposition

Gate answered **yes**, so per the leg contract: **not patched under this leg's authority**,
branch pushed, escalated to the orchestrator with maximum urgency, **not merged to main**.

`test_gclm_adversarial.py` is banked as a **characterization** test rather than a
"confirmed robust" bank: 4 checks pin the robustness that does hold, and 4 pin the gaps as
measured. A failure of a `KNOWN GAP` check means `solver/gclm.py` was repaired and is good news —
the test says so in its own output, so a repairing leg is forced to update it deliberately rather
than let the repair go unrecorded.

**Suggested repair, for whoever holds the authority (NOT applied here).** G1: replace the absolute
tolerance with a scale-relative one, `np.abs(w0) < 1e-12 * max(np.abs(w0).max(), tiny)`. G2:
`if nu > 0.0` → validate `nu` and raise on `nan`/negative. G3: use `np.maximum` (which propagates
NaN) instead of builtin `max`, or check finiteness explicitly. G4: validate the stop-criteria
block on entry. All four are one-line-class changes; none is this leg's to make.
