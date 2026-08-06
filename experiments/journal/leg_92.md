# Leg 92 — Route-GLA: adversarial audit of `solver/gclm.py` (physical-space gCLM)

Branch `leg/gla-v1`. Claim-bearing. Difficulty: standard.
Gate answered **YES** — escalated, not patched, not merged to main under this leg's authority.

## Order of work (contract compliance)

1. `plan_of_record.py` run first; all ten live bans read and checked.
2. Novelty pass run and **committed before any construction** (commit `ee492c5`), as required.
   `writeup/novelty/leg_92.md` records it; the findings section was appended afterwards, below
   a marker, so the pre-registration is legible as pre-registration.
3. `capabilities.py` grepped before building: `capabilities.py:402-406` registers
   `solver/gclm.py` as "gCLM, physical space", test `test_gclm_dedicated.py`. No validation
   capability existed to reuse; nothing was rebuilt.
4. Battery built, run, criteria corrected (twice — see below), re-run, results curated.
5. `solver/gclm.py` **read only, never edited**, under this and every outcome.

## Ban ruling

The live ban "another gCLM measurement leg" does **not** bite. This leg produces no physics
quantity about the gCLM model — no `a`-sweep verdict, no exponent, no profile, no genome, no
blow-up claim. It measures the response of Python code to invalid input. Where the solver is
stepped, the runs are deliberately degenerate and their physics is discarded; only outcome labels
and finiteness are read. Same robustness-vs-measurement distinction that cleared legs 83, 85 and
88, verified independently here rather than inherited. The other nine bans were checked
one-by-one and none touches an input-validation audit.

## Result, in one line

**19 silent corruptions in 54 gate-scoped cases, four independent mechanisms**; the worst is a
finite, positive, ordinary-looking blow-up time that is **1.5× too early** (relative violation of
an exact scaling invariant = **1/3**, saturated) for initial vorticity of amplitude ≤ 1e-12,
caused by an **absolute** zero-tolerance `np.abs(w0) < 1e-12` at `solver/gclm.py:289` that never
measures the scale of its own input.

The four mechanisms, with the line each lives on:

| # | line | mechanism | headline magnitude |
|---|---|---|---|
| G1 | `gclm.py:289` | absolute zero-tolerance in `clm_analytic_blowup_time` | rel. violation 3.38e-03 at amplitude 1e-8, saturating at 1/3 below 1e-12 |
| G2 | `gclm.py:164` | `if nu > 0.0` drops negative/NaN viscosity | `nu=-1.0` bitwise identical to inviscid; real `nu=0.01` moves it 7.364e-03 |
| G3 | `gclm.py:226` | `max(mean_drift, energy_residual)` swallows NaN | logged guard reads 4.926e-17 on a run reaching `max|w| = 9.673e+144` |
| G4 | stop-criteria block | every NaN comparison is False | `amplification_factor=nan` flips `blowup_candidate` → `diverged`; `t_max=nan` → 0 steps, verdict `no_blowup` |

Robust and banked: NaN/Inf-seeded vorticity is flagged `diverged` on step 1 in all 12 cases;
extreme finite `a` (1e4…1e16) is honestly huge and unclamped (max|w| 7.69e+24 → 9.67e+204,
monotone); non-finite `a` is flagged; structural adversaries raise `ValueError`.

## Two criterion corrections, recorded rather than hidden

Both are written into the battery's own docstrings and into the JSON, not just here.

1. **Amplitude family.** First draft used a fixed `1e-9` tolerance and flagged 16/17 cases,
   including `eps=1e-2` — miscalibrated by me. The zero-finder's own noise floor is now
   *measured* on decades where the defect provably cannot reach (2.353e-06) and the threshold set
   three decades above it (2.353e-03). Count 16 → 11; onset moves 1e-2 → 1e-8. The surviving
   evidence is stronger: a monotone six-decade ramp terminating at an analytically predicted
   constant (1/3), which the mechanism check derives independently from the two H-maxima
   (0.75 global vs 0.5 over the zero set).
2. **Viscosity family.** First draft counted `nu = -0.0` as a silent corruption. False positive:
   `-0.0 == 0.0`, so skipping dissipation is correct. Restricted to NaN and strictly-negative.
   Count 2 → 1.

Also held to the pre-stated rule rather than bent to it: `nu = nan` and `nu = -inf` produce a
bitwise-inviscid trajectory (dissipation silently dropped) but *do* emit a non-finite
`energy_balance_residual`, so under the pre-registered definition they are FLAGGED, not silent.
Reported at full strength, excluded from the count.

## Blast radius (measured, deliberately not overclaimed)

**No banked result on main is corrupted.** The sole production consumer of
`clm_analytic_blowup_time` (`stage1_5_sweep.py:369`) energy-normalizes every IC to
`ENERGY_TARGET = π/2` at `stage1_5_sweep.py:174-181`, i.e. O(1) amplitude — about eight decades
above G1's onset. Every `solve_gclm` caller passes `nu = 0.0` or a non-negative bisected `nu`, so
G2/G4 are unreachable from them; G3 needs an `a` far past anything any sweep uses. These are
**latent** gaps — real and reachable by any future caller, invisible to the existing suite, but
not an active contamination.

## Deliverables

- `experiments/p2_route_gla_v1_adversarial.py` — the battery (9 families, ~46 s)
- `writeup/data/p2_route_gla_v1_adversarial.json` — curated data
- `test_gclm_adversarial.py` — permanent regression test, 8 checks, all passing
- `writeup/novelty/leg_92.md` — pre-registered novelty pass + findings
- `experiments/journal/leg_92.md` — this file

No figure required by the contract; none produced.

`test_gclm_adversarial.py` is a **characterization** test, not a "confirmed robust" bank — the
gate answered yes, so 4 checks pin the robustness that holds and 4 pin the gaps as measured. It
passes today. A `PINNED` check failing means the module was repaired, which the test's own output
says is good news, forcing the repairing leg to update it deliberately.

## Escalation

Per the contract's yes-branch: `solver/gclm.py` **not patched**, branch pushed, **not merged to
main** until the orchestrator has seen it. Suggested one-line-class repairs for whoever holds the
authority are listed at the end of `writeup/novelty/leg_92.md`; none was applied here.
