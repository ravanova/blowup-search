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

<!-- findings appended after the run -->
