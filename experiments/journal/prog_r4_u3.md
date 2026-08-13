# PROG-R4, unit U3 — GATE G1

**Programme:** PROG-R4 (`ORCHESTRATION.md` §3c PROGRAMME lane, slot A, leg 380).
**Unit kind:** CLAIM. This unit answers a gate.
**Mode:** §3f SOLO. No paired verifier, no DM, no orchestrator.
**The answer below is UNVERIFIED** in the repo's sense: it was produced and checked in one
session. Verification is a fresh session or it is not verification.

---

## 1. The gate, in its pre-committed wording

> **G1: DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO tol=1e-8?**

Fixed in `experiments/journal/prog_r4_prereg.md` before any of this programme's units ran, and
not restated, softened or re-scoped here.

## 2. THE ANSWER

**G1 = `UNDER-RESOURCED`.**

- **0** of 100 attempts recovered a named Table IV orbit.
- **14** of 100 attempts converged to `tol = 1e-8`.
- Planted controls **FIRED AS PLANTED**: P recovered (`‖R‖ = 7.75e-9`), N did **not** recover
  (`‖R‖ = 1.75`), R recovered (`‖R‖ = 3.26e-9`). The instrument is therefore shown able to say
  `YES`, which is the precondition for any negative-side answer being admissible at all.

**`no` was not an available branch, and that was fixed before the run**, in AMENDMENT 3 of the
addendum, on measured cost. `ORCHESTRATION.md` §3d's stop **does not fire**. **Route 4 is not
stopped on measurement.** A reader who finds `UNDER-RESOURCED` in `p2_prog_r4_g1_v1.json` and
reads it as a verdict on the orbits is reading it backwards.

## 3. Resourcing, as run

| | |
|---|---|
| DNS length | `T = 1e5` (unit U2, MILESTONE M2) |
| grid | `N = 24`, `Re = 60`, forcing `n = 4` |
| globalisation | genuine Newton–GMRES–hookstep trust region (unit U1, MILESTONE M1) |
| attempts | 100, all anchored to a named row (Ban 2 PASS) |
| caps | `max_newton = 52`, `max_gmres = 140`, `gmres_rtol = 1e-3` |
| tolerance | `1e-8` |
| wall | **14.47 h**, 134.45 core-hours over 10 workers |
| seed funnel | 2014 candidates → 579 in window → 234 with `m=0` → 133 anchored → 100 run |
| shift sign | measured per seed, not assumed: 98 minus, 2 plus |

Leg 353's comparison baseline: 5 attempts at `T = 2000` with a line search, none converged.

## 4. What actually happened, which neither pre-committed branch anticipated

**The solver worked.** 14 convergences in 100 attempts is a **14% per-attempt rate**, above both
sourced rates — Chandler & Kerswell's 4.3% for the nonzero-shift RPO class at `Re = 60` and Lucas
& Kerswell's ~10%. Best final residual `8.67e-12`, four orders below tolerance.

**And it converged reproducibly.** Independent seeds — different snapshots, different anchors —
landed on the same solutions:

| solution | times found | seeds from | agreement |
|---|---|---|---|
| `T = 16.524–16.536`, `\|s\| ≈ 0.100` | 4 | UPO9, UPO17 | `T` to 0.012, `\|s\|` to 0.002 |
| `T = 16.810–16.922`, `\|s\| ≈ 0.073` | 4 | UPO9, UPO17 | `\|s\|` to 0.001 |
| `T = 19.2848 / 19.2929`, `\|s\| ≈ 0.117` | 2 | UPO32 | `T` to 0.008 |

Eight distinct converged solutions in all. These are genuine relative periodic orbits of the
discrete map, confirmed by internal replication rather than asserted.

**None of them is a named Table IV row.** That is the gate's predicate and it is unmet:
`n_recovered = 0`. A convergence that does not match a named row on **both** `T` and `s` to within
0.05 is not a recovery, and the curated record and fig97 both enforce that separation so that
"the solver works" cannot be quietly upgraded into "we found them."

## 5. Why the misses are systematic

Every converged solve has `|s|` between 0.073 and 0.317, twelve of fourteen below 0.14. The eight
published rows have `|s|` between 0.295 and 0.707. That is a separation in the shift coordinate,
not a scatter around the targets.

The cause is in the **seed supply**, and it is measurable. Over the 1153 `m = 0` candidates in the
library, the rank correlation between `|s|` and the recurrence score `R` is **0.50**, and
admission by the Newton window `R < 0.25` falls monotonically with shift:

| `\|s\|` band | n | median `R` | admitted |
|---|---|---|---|
| 0.000 – 0.150 | 322 | 0.3205 | **44%** |
| 0.150 – 0.295 | 213 | 0.5067 | 20% |
| 0.295 – 0.750 *(published band)* | 395 | 0.8317 | **11%** |
| 0.750 – 3.200 | 223 | 1.1278 | 3% |

Median `|s|` of the admitted pool: 0.112. Of all candidates regardless of window: 0.824. **The
large-shift recurrences exist in the DNS in quantity; the window removes them.** Newton then does
what Newton does — it converges near its seed — so a pool of small-shift seeds yields small-shift
orbits.

This is structurally identical to the period-band starvation AMENDMENT 4 fixed in unit U2: a
scalar score used as an admission filter, systematically monotone in a property the targets are
selected on. It is the same bug one dimension over, it was not anticipated, and the seed budget
was never stratified by shift.

## 6. Errata against my own pre-registration

Recorded in full in addendum §3e. Summarised:

1. **The envelope arithmetic ignored `Pool.map` chunking** — 34 chunks of 3 over 10 workers means
   the tail worker takes 12 attempts, not 10. Errs safe (more compute than planned).
2. **Per-epoch cost was underestimated ~1.7×** — 95 s/epoch measured against the probe's 54.7,
   probably ten-way memory-bandwidth contention. Successors should cost at 95.
3. **The cost model behind `max_newton_required = 238` does not describe the observed behaviour.**
   Convergence is bimodal: all 14 convergences finished in ≤29 epochs (median 16), while the 86
   non-convergences ran to the cap and were flat there — 53% reduced `‖R‖` by <1% over their final
   10 epochs, 83% by <10%, only 3% still halving, median final `‖R‖ = 2.11`. Max Krylov dimension
   over the whole run was 25 against `max_gmres = 140`.

**So neither cap bound any attempt that converged.** `UNDER-RESOURCED` is still the correct
pre-committed branch — the run *did* run below the budget the cap rule named, and `no` was
correctly unavailable — but the named compliant cost (36.2 h, 15.1 core-days) is the wrong thing
for a successor to buy. Buying 238 epochs extends 86 already-flat sequences.

## 7. Lesson 91: what this negative names

A negative names its realization. This one is:

- **first-order in time.** The stepper is Lie–Trotter (RK4 on the nonstiff part, then the exact
  viscous factor), globally **first** order, not fourth — measured, local ratio 4.00, global ratio
  2.00. Its periodic orbits are `O(dt)` perturbations of the true flow's.
- **blind to the `m ≠ 0` class.** The extended residual carries a continuous `x`-shift only, so
  345 in-window candidates could not be *expressed* as seeds. All eight named rows have
  `m_published = 0`, so nothing named is lost — but the sentence "no named orbit recovered" must
  carry "with a residual that cannot represent one of the two shift classes."
- **seeded from a shift-biased pool**, per §5.

So the honest form of this unit's negative is: *no named Table IV row was recovered by a
first-order-in-time realization, from a seed pool whose admission filter is monotone in the very
coordinate that separates the targets, inside an iteration budget below the one the cap rule
named.* Not "the orbits are not there." Not "Newton cannot find them" — it found eight others.

## 8. Successor items, in order

1. **Stratify the seed budget by shift, as AMENDMENT 4 did for period.** The published band
   (`|s| ∈ [0.295, 0.707]`) has 395 `m = 0` candidates in the library already, 11% of them already
   inside the Newton window. This is the cheapest untried thing and it targets the measured cause.
2. Relax or replace the `R < 0.25` admission test for large-shift candidates, since the score is
   confounded with the coordinate being filtered on.
3. Extend the residual to carry an `m` unknown, recovering the 345 dropped candidates. A change to
   the realization, not a tuning; would invalidate M1's reproduction and needs its own milestone.
4. Only then consider buying iterations. The bimodality says this is the *last* thing to spend on,
   not the first.

**None of these is started here.** Choosing one would be choosing my own next task.

## 9. Obligations and ceiling

`CLAY_OBLIGATIONS` §6's two no-method obligations remain **OPEN**. §4 remains **OPEN and NOT
discharged** until leg 386 lands with a pre-registered δ mode. **Ceiling TIER 2.** No `L1 → L4`
link is moved by this unit. **Clay stays ~0.05%.**

Gate G2 (unit U4, the basin radius, brick B5 clause c-iii) is **UNANSWERED** and was not opened.
It requires a recovered *named* orbit to perturb, which this unit did not produce.

## 10. Artefacts

- `experiments/programme_r4/u3_g1_attempts.py` — the runner
- `writeup/data/p2_prog_r4_g1_v1.json` — the curated record (gate, controls, resourcing, seed
  funnel, magnitudes, all 100 attempt rows)
- `experiments/programme_r4/u3_g1_ledger.json` — the full per-iteration ledger (4.9 MB)
- `writeup/figures/fig97_prog_r4_g1_attempts.py` + `.png` — 22/22 checks pass
- `experiments/journal/prog_r4_u2u3_prereg_addendum.md` §3e (errata), §3f (the second bias)
- no `u3_g1_recovered_orbits.npz` — nothing matched a named row, so nothing was saved under that
  name, which is the correct behaviour and not a missing file
