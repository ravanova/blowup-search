# Leg 89 (Route-BOA) — novelty pass: has anyone already asked whether `solver/boussinesq.py` fails LOUDLY?

**Pass date: 2026-08-06. Written and committed BEFORE any construction and before any number
was seen, per the leg contract.** `plan_of_record.py` was run first; every ban it prints was
read (see §4). `capabilities.py` was grepped before anything was built (see §1).

## 0. What this leg claims, and what it does not

**Claimed:** a *software* fact about one module — that `solver/boussinesq.py`, driven by
deliberately malformed inputs, either does or does not return a normal-looking
`BoussinesqResult` whose validity fields read healthy while the computation behind them is
invalid.

**Not claimed:** any mathematical novelty. Nothing here is discovered about the Boussinesq
system, the Hou–Luo geometry, or blow-up. No link of the L1→L4 chain moves. Like every leg in
the adversarial-audit family (69/IA, 79/PC, 80/BHN, 83, 85, 88/GCA), this leg can only
*withdraw* confidence or bank a regression test; it can never add a result. The
external-literature dimension of a novelty pass is therefore **vacuous** — "does numpy's
builtin `max` drop a NaN in this repo's guard expression" is not a question the published
record answers — and no arXiv search is reported, so that no absence is later mistaken for a
searched-and-empty result.

## 1. Prior art INSIDE this repository — the dimension that actually bites

Grepped before construction: `capabilities.py` (the `solver/boussinesq.py` entry at line 392,
full current text), all eight `test_*boussinesq*.py` files, and every adversarial battery
already banked.

`capabilities.py` line 392–396 currently advertises:

> `solver/boussinesq.py`, object "2D Boussinesq, physical space",
> validated: "dedicated: `test_boussinesq_dedicated.py` (17 checks) + `test_solver_boussinesq.py`;
> odd-n derivative path checked correct"

| what exists | where | what it covers | why leg 89 is not a repeat |
|---|---|---|---|
| `check_solve_rejects_bad_arguments` | `test_boussinesq_dedicated.py:340` | exactly **four** cases: unknown `symmetry`, all-zero `omega0`, non-square `theta0`, rank-1 `theta0` | every one is a **well-formed** wrong-shape/wrong-label input on a path that already has an explicit `raise`. None is NaN- or Inf-poisoned, none is a degenerate *value* rather than a degenerate *shape*, and none touches a scalar coefficient at all. It audits the three `ValueError` branches that exist; it cannot see the branches that were never written. |
| the other 16 checks in `test_boussinesq_dedicated.py` (leg 66/QF) | same file | Biot–Savart hand values, parity projectors, pure diffusion exactness, frozen-u translation, mean invariants, both under-resolution guards | all on **well-behaved** inputs. Leg 66's own framing was "does a direct test find a discrepancy against what the indirect tests assumed" — a correctness question. Robustness under hostile input is a different question in kind, which is exactly the distinction DIRECTION.md's leg-89 entry draws. |
| `check_under_resolved_guards` | `test_boussinesq_dedicated.py:524` | `tail_guard`/`drift_guard` fire and don't fire, using thresholds of −1.0 and 2.0 | proves the guards are **not constants**. It says nothing about whether a guard can be made *blind* — i.e. fail to fire on a run that is genuinely invalid — which is the failure mode this leg is built to find. |
| `test_solver_boussinesq.py`, `test_boussinesq_wall.py`, `test_boussinesq_transport.py` | repo root | indirect/physics-level acceptance | all supply valid fields by construction. |
| `test_bordered_hl_adversarial.py` + `experiments/p2_route_bhn_v1_adversarial.py` (leg 80) | repo root | the damped Newton in `solver/bordered_hl.py` | different module, different flag (`converged`), different failure mode. Sibling, not duplicate. |
| leg 79's 39-case battery (recorded in `capabilities.py:113`) | port certification | `radii_polynomial_status` fabrication labels | different module entirely. |
| DIRECTION.md leg 88 (Route-GCA) | queue/landed | `solver/gclm_family.py` residual under poisoned `c_l`/`c_omega` | different module. The family pattern is deliberate; the target is not shared. |

**Conclusion of the in-repo pass: NOT a repeat.** No file in this repository has ever passed a
non-finite value, a degenerate grid size, or an out-of-domain physical coefficient into
`solve_boussinesq`. The zero-`omega0` check is the closest existing thing and it is a shape/exact-zero
guard, four decades of intent away from "does the reported guard value stay small while the state
is NaN".

## 2. Mapping the gate's third clause onto a module that has no grid stretching

The gate names three input families: NaN-seeded vorticity, degenerate/zero stream function, and
**extreme grid-stretching**. Read before construction: `solver/boussinesq.py` is a *uniform*
`2π`-periodic pseudo-spectral code (`grid2d` is `2π·arange(n)/n`); it has **no grid-stretching
parameter whatsoever**. The clause is therefore mapped, and the mapping is fixed here before any
run, to the nearest thing in kind — **extreme discretization and coefficient parameters**: the
grid size `n` itself at degenerate values, `dt_max`/`c1`/`c2` at zero, negative and non-finite,
and the physical coefficients `nu`/`kappa` out of their admissible domain. A leg that quietly
dropped the third clause because the literal words don't apply would be answering an easier
question than the one it was dispatched with.

Similarly, "degenerate/zero stream function" is mapped to what produces one in this module:
`Δψ = ω` with `inv_Ksq` zeroed at the mean mode, so a **constant** `ω` (all energy in the (0,0)
mode) and any `ω` annihilated by the 2/3 dealias mask both give `ψ ≡ 0`, `u ≡ 0`.

## 3. Pre-committed decision rule (fixed BEFORE the run)

The gate is decided on this definition and no other:

> **SILENT CORRUPTION** := the call returns **normally** (no exception raised), **AND** every
> field a caller reads to judge the run's validity — `outcome`, `conservation_drift`,
> `mean_drift`, `energy_balance_residual`, the `max_omega` trajectory — is **finite and in a
> plausible range**, **AND** the run is nevertheless invalid, because either (a) the returned
> state `omega_final`/`theta_final` is not all-finite, or (b) an invalid parameter was silently
> **dropped** and the integration that ran is not the one that was requested, while `params`
> records the value that was ignored.

Two readings are deliberately **excluded** from deciding the gate, and both are measured anyway
and reported separately:

- **Loud failure is a PASS, whatever its form.** A raised `ValueError`, an `outcome` of
  `"diverged"`/`"under_resolved"`/`"max_steps_hit"`, or a NaN that reaches a field the caller
  reads — all of these propagate or flag, which is what the gate asks for. This leg does not
  grade the *quality* of the flag.
- **A physically dull-but-correct answer is a PASS.** Constant `ω` really does have `u ≡ 0` and
  really does sit still; reporting `no_blowup` there is right, not corrupt.

The sharp case the definition is built to catch, identified statically before the run and to be
either confirmed or refuted by measurement: `conservation_drift` is documented at
`solver/boussinesq.py:141` as "max of the two above; the logged guard value", and it is computed
with Python's builtin `max`, which is **order-dependent on NaN** — `max(0.3, nan)` returns `0.3`.
If any input can put a NaN into one guard limb while the other stays small, the top-line logged
guard reads healthy on a poisoned run and `drift_guard` never trips. Whether such an input exists
is a measurement, not an assertion, and it is what the battery is for.

**Discipline: magnitudes, never booleans.** Each family reports its case count, how many returned
normally, and the *size* of the thing that could have gone wrong — the guard value actually
reported on a poisoned run, the NaN fraction of the returned state, the ratio between the
requested and the executed coefficient.

## 4. Bans (`plan_of_record.py`, read in full)

None are tripped. This is not a gCLM measurement leg (it measures no model — it measures a
module's error handling), not a Route-D bound-sharpening leg, not a DSS re-ask, not a `beta`
re-measurement on the 2D object, not a re-test of the scaling gauge, and it spends no GA compute.
It re-opens no closed stage and reads nothing about leg 51/53's ceilings. The standing ban
**"building a solver without grepping `capabilities.py` for the object first"** was honoured
before a single file was written — §1 quotes the entry. Nothing is built that a capability entry
already provides: `capabilities.py`'s `solver/boussinesq.py` entry advertises dedicated coverage,
and §1 establishes that the coverage is entirely on well-behaved inputs.

## 5. Territory

Writes only: `test_boussinesq_adversarial.py`, `experiments/p2_route_boa_v1_adversarial.py`,
`writeup/data/p2_route_boa_v1_adversarial.json`, `writeup/novelty/leg_89.md`,
`experiments/journal/leg_89.md`. `solver/boussinesq.py` is **read-only under every gate
outcome**, including the yes-branch: a silent-corruption finding is escalated, never patched
under this leg's authority.

---

## 6. FINDINGS (appended after construction, 2026-08-06)

The pass above was committed before any number was seen (`95d516e`). What the battery then
measured, over **90 cases in 84 s**:

**Gate answer: YES — 19 silent-corruption cases of 82 gate-deciding, plus 4 of 8 secondary.**
Escalated, not patched; `solver/boussinesq.py` is unchanged.

| family | cases | silent | magnitude |
|---|---|---|---|
| A — degenerate/zero stream function | 8 | **6** | false `blowup_candidate` off a represented `m0` of **1.797e-16**; amplification **5.566e+13**, and **1.0e+298** at amplitude 1e-300 |
| B — NaN/Inf-seeded vorticity | 30 | **0** | all 30 reach `diverged` in 1 step |
| C — NaN/Inf-seeded temperature | 15 | 0 | 12 propagated, 3 flagged; `theta_final` 100% NaN while `conservation_drift` = **8.077e-18** |
| D — out-of-domain `nu`/`kappa` | 13 | **8** | 5/5 `kappa` values bit-identical to the `kappa=0` run, energy-residual ratio **1.000** |
| E — degenerate grid / discretization | 16 | **5** | `n=1,2` retain **1** mode, report `drift = 0.0`; `c1=c2=nan` relaxes `dt_min` **168.8×** |
| F — detection thresholds (secondary) | 8 | **4** | `amplification_factor=nan` runs past **4.013×** amplification reporting `no_blowup` |

`conservation_drift` masks a NaN limb in **13 of 90** cases.

Full narrative, the four defects in severity order, and the scope caveats:
`experiments/journal/leg_89.md`.

### The three things this pass predicted, and what the run did with them

1. **§3 predicted the `max`-with-NaN mask, and the run confirmed it exactly.** The pass named
   `conservation_drift` (`solver/boussinesq.py:141`, "max of the two above; the logged guard
   value") as the sharp case *before* any measurement, on the ground that Python's builtin `max`
   is order-dependent on NaN. Measured: 13 of 90 cases, with `drift_guard=1e-9` failing to fire on
   a run whose `theta_final` is 100% NaN. The same defect turned up on the **`min`** side of the
   timestep, which the pass did *not* anticipate: a non-finite `c1`/`c2` removes its CFL limb
   rather than failing, worth a **168.8×** step relaxation.

2. **§2's mapping of clause 3 earned its keep, and clause 1 came back clean.** Had "extreme
   grid-stretching" been dropped as inapplicable to a uniform grid, families D and E — **13 of the
   19** gate-deciding silent cases — would never have been run, and the leg would have reported
   the gate's *easier* half. The named clause the module handles well is clause 1: NaN-seeded
   vorticity is the one genuinely robust path, 30/30 flagged. **The gate's own headline example is
   the case that passes**; the failures are next door to it.

3. **The witness discipline is what makes the `kappa` finding statable.** §3 pre-committed to
   bit-for-bit array equality against the neutral control rather than "both are small". Without
   it, `kappa=-0.5` returning `energy_balance_residual = 2.2188e-07` is indistinguishable from a
   healthy viscous run — that number *is* the `kappa=0` value, to the last bit, and only the
   bit-identity witness says so. The `nu` contrast (residual ratio **1.9745e+06**) then shows the
   energy guard catches the `nu` half by accident of the identity's shape and cannot, even in
   principle, see the `kappa` half.

### The one case the battery was corrected on, mid-run

`t_max = 0.0` was initially graded a failure and was **reclassified as a control** before the
final run: asking for zero integration time is a legitimate degenerate request, and returning at
once is the right answer. Only the malformed values (`nan`, negative) are graded. Recorded here
because the correction moved the secondary count from 5 to 4, and a count that moved should say
why it moved.

### Instrument that was measured and then refused

`n_runtime_warnings` is recorded per case but **decides nothing**. numpy raises its invalid-value
`RuntimeWarning`s from C with a once-per-code-location registry that `simplefilter("always")` does
not reliably reset — measured to report 0 on a case that does warn on a fresh interpreter. It is a
lower bound, kept for the record only. The "silently" half of the gate is decided structurally
instead, on whether every validity field is finite and plausible; no warning instrumentation is
needed, because the silent cases perform no non-finite arithmetic at all.
