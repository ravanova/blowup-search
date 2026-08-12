# PROG-R4 (leg 380) — PROGRAMME PRE-REGISTRATION

**Committed at programme start, together with U0's novelty pass, BEFORE any construction.**
This document is immutable for the life of the programme except where it says a successor may
append. It exists so that no gate can be re-scoped after its numbers are seen.

- **Lane:** `ORCHESTRATION.md` §3c PROGRAMME, slot A, long-lived worker, state persists across
  units, not terminated on a unit landing. The slot does not vacate on landing (user ruling,
  2026-08-12); the four-slot roster is three-plus-one while this programme runs.
- **Spec:** `DIRECTION.md` cycle-11a §4 (immutable; this document restates, never re-scopes).
- **Object:** recover published relative periodic orbits of 2-D Kolmogorov flow at the scale
  the question is posed at, then measure the Newton basin radius — brick B5 clause (c-iii).
- **Novelty pass (U0):** `writeup/novelty/prog_r4.md`, one pass, programme-level, binds the
  whole programme. Verdict `PROCEED` with three named neighbours.
- **Base:** `origin/main` at `104f5b3`. Preconditions verified by reading main: `bb00a0d`'s
  Ban-2 scope annotation present in `plan_of_record.py`; `solver/kolmogorov2d_nkbasin.py`
  carries leg 353's sign-fixed `optimal_shift_residual`; `writeup/data/p2_route_rpol_v1.json`
  and `writeup/data/p2_route_dsspb5_v1.json` both present. All four TRUE.

## 1. The named seed

Carried verbatim in `writeup/novelty/prog_r4.md` §1 and re-screened there against **Ban 2**
(§1a: named, published, initialised-from, not a global unseeded trawl) and against **Ban 1**'s
literal wording (§1b: no step of any unit continues a fixed point into an orbit — re-applied
per unit, not once). **If any unit ever finds itself without a named seed, Ban 2 applies in
full: the programme STOPS and escalates.** The one wording discrepancy in the seed's own text
("the five published RPOs" = five *attempts* over four distinct rows, inside leg 353's
eight-row pre-registered `TABLE_IV_TARGETS`) is recorded at §1c and resolved *without*
re-scoping: the seed pool is the eight named Table-IV rows of arXiv:1406.1820v2 already
pre-registered by leg 353, which is the reading G1's own wording ("named Table-IV RPO")
requires. UPO37 (T=19.334, s=0.375, m=0) remains the primary named target.

## 2. Units, with the milestone/gate distinction fixed in advance

| unit | kind | milestone / gate |
|---|---|---|
| U0 | novelty | the ONE programme-level pass. Landed first. |
| U1 | build | **MILESTONE M1** — the globalisation layer. No claim, so no gate. |
| U2 | build | **MILESTONE M2** — DNS at compliant scale + recurrence library. No claim, so no gate. |
| U3 | claim | **GATE G1** |
| U4 | claim | **GATE G2** |

**M1.** A genuine hookstep/trust-region on top of the existing Newton–Krylov apparatus
(Viswanath 2007: plain and damped Newton steps are ineffective on this problem class).
Milestone met when: the layer exists; the laminar-fixed-point control reproduces leg 353's
clean convergence (99.3% residual reduction baseline) **through the new layer**; a
per-iteration ledger is persisted. **No claim is made, so no two-branch question is
manufactured for it** (§3c rule 2).

**M2.** DNS at `T=1e5`, `N=24`, with recurrence-candidate extraction, thresholds taken from
the sources as banked in `writeup/data/p2_route_rpol_v1.json`. Milestone met when: the
trajectory archive and the near-recurrence library are persisted with their thresholds
stated. No claim.

**§3d pre-registration of the compliant scale, stated NOW so the gate cannot fire on a
budget.** The compliant scale IS: `T=1e5` DNS / genuine hookstep / ~100 attempts / `N=24`
(leg 358's minimum-viable spec). At the sources' own success rates this sample is resourced:
`P(0 successes in 100) ≈ 1.2%` at Chandler–Kerswell's 4.3% (7/163, the nonzero-shift RPO
class UPO37 belongs to) and `≈ 3e-5` at Lucas–Kerswell's ~10%. **Escalation to literature
scale (`T=5e6`, ~10.2 GPU-days) is authorised in kind but is GPU-dependent in the source
papers' own hands and this repository does not currently have that compute: minimum-viable
runs FIRST and the escalation question is reported WITH G1's numbers, never assumed.**

### GATE G1 (U3) — pre-committed, both branches

> **G1: DOES AT LEAST ONE NAMED TABLE-IV RPO RECOVER TO tol=1e-8?**
>
> - **yes** → the extraction premise is re-established on this realization at compliant
>   scale; U4 proceeds. **CEILING: TIER 2.** `CLAY_OBLIGATIONS` §6's two no-method
>   obligations — (i) certified far-field decay + admissible cutoff, (ii) persistence /
>   stability under localisation — are **OPEN and unrelaxed by this branch**. **§4 is OPEN
>   and NOT discharged** (see §3 below).
> - **no** → a **RESOURCED null**: §3d's stop genuinely fires this time, on measurement, and
>   route 4 stops. The programme ends and reports per-attempt residuals, condition numbers,
>   and the comparison against the sources' own success curves **as magnitudes**. The same two
>   §6 obligations recorded **OPEN**; **§4 OPEN and NOT discharged** (§3 below).
>   **CEILING: TIER 2.** The stop packet goes to the user; **nothing is retried on DM
>   authority.**

### GATE G2 (U4) — pre-committed, both branches

> **G2: IS A RADIUS MEASURED WITH A COHERENT (MONOTONE) FAILURE BOUNDARY, CONTROL FIRING AS
> PLANTED?**
>
> - **yes** → clause (c-iii) becomes a number; S4's cold-start assessability reported as a
>   magnitude; the 2-D object is complete and the next route-4 decision returns to the DM and
>   the user. **CEILING: TIER 2**; §6's two obligations **OPEN**; **§4 OPEN and NOT
>   discharged** (§3 below).
> - **no** → the boundary is incoherent or below the perturbation floor: report the magnitudes
>   and the mechanism. **A non-boundary IS the deliverable, not a defect to tune away.**
>   **CEILING: TIER 2**; §6's two obligations **OPEN**; **§4 OPEN and NOT discharged** (§3).

U0 §3c records, before any measurement, that Parker & Schneider (arXiv:2108.12219) describe
*"the complex, fractal regions of convergence"* for this problem class. **G2's `no` branch is
therefore literature-anticipated, and the programme will not tune an incoherent boundary
away.**

## 3. THE AMENDMENT — CLAY_OBLIGATIONS §4 is OPEN and NOT discharged

**Binding on both branches of both gates above, by user ruling relayed 2026-08-12.** It stays
open in every route-4 gate **until leg 386 (ROUTE-DTOL) lands with a pre-registered δ mode.**

Stated in this programme's own words, so it is understood rather than asserted. Leg 382
(ROUTE-DEXC, landed `104f5b3`) produced a certified far-field decay enclosure with gate YES,
and the easy misreading is that this discharges §4. It does not:

1. **§4's admissible cutoff radius is a function of the CERTIFIED decay exponent.** If the
   certification carries a tolerance `δ`, the cutoff bound inherits that `δ`. So a certified
   exponent is an *input* to §4, not §4's discharge.
2. **Whether the cutoff analysis tolerates `δ > 0` at all is unanswered.** Leg 382's gated
   `δ=0` form answers EMPTY on every real input — it proved this itself and recorded it as a
   **refuted pre-registered prediction** rather than amending the prediction, because no
   numerical profile is exactly a power law. Its usable `δ`-mode is post-hoc and explicitly
   **not gate-deciding**.
3. **The measured critical tolerances span two orders of magnitude:** `δ* = 3.352868`,
   `0.315697`, `0.069739` on three planted non-power cases, and `0` for an exact power law.
   That range is the difference between a usable instrument and a relabelled one. Leg 386 is
   ranked top of the reserve to answer it.
4. **§6 item 1's cutoff half is entirely unattempted by anyone**, in this repository or, so
   far as U0's pass found, outside it.

**Operational consequence for this programme:** no branch of G1 or G2 may be written or
reported in a way that treats far-field decay as a settled obligation. Every gate report, every
BLOG/TECHNICAL pair, and every curated JSON this programme emits carries §4 as OPEN alongside
§6's two.

**Also recorded, as the reason this programme runs in parallel rather than behind the
obligations track:** `CLAY_OBLIGATIONS` §8 ask #1 — *decide the certification route before the
compute runs* — is **SATISFIED** by POCP being the only open route (leg 348). It is not
waiting on a report and it is not a gate on this build. Legs 381 (CLOC), 383 (ST2G, landed),
384 (COBV) and 385–388 run **beside** this programme, not ahead of it. Nothing in that track
blocks a unit here, and **nothing this programme does presumes the POCP spend, which remains
the user's decision.**

## 4. Scope limits, stated so the programme cannot drift

- **No 3-D unit exists in this spec.** B6 (the 3-D seeded search) requires a NAMED 3-D seed
  under §1, and the 3-D seed set is measured **EMPTY twice, with controls** (leg 313;
  re-measured leg 334 §4.1). Absent a named seed Ban 2 applies in full, so **nothing 3-D
  dispatches from this programme.**
- **Nothing here presumes the POCP spend, either way.** No unit prepares for it or against it.
- **Ceiling is TIER 2 throughout.** `WIN_CONDITION.md` is unambiguous that Tier 2 is never
  called a proof.
- **No output of this programme is described as movement toward Clay unless a link of the
  `L1 → L4` chain actually moved. Clay stays ~0.05%.**

## 5. Territory (exclusive to PROG-R4) and figure allocation

`solver/kolmogorov2d_nkbasin.py`, `solver/hookstep_newton.py` (NEW),
`test_kolmogorov2d_nkbasin.py`, `test_hookstep_newton.py` (NEW),
`experiments/programme_r4/**`, `writeup/data/p2_prog_r4_*.json`,
`writeup/novelty/prog_r4.md`, `experiments/journal/prog_r4_*.md`.
Plus the two shared files every leg is permitted to touch in the prescribed way:
`capabilities.py` (**append only**, at the end of this object's own section, never reorder —
§5a's stated exception) and `writeup/build_figures.py` / `writeup/figures/` for the two
allocated figure numbers.

**FIGURE ALLOCATION: `fig97` and `fig98`, reserved for this programme. No other number is
taken** (fig96 is the highest in use; eight figure-number collisions have already cost this
repository time).

## 6. Persistent state

`experiments/programme_r4/` holds `state.json` (the unit ledger: milestones reached, gate
answers, costs measured), the DNS trajectory archive, the recurrence-candidate library, and
the per-attempt convergence ledger. It survives across units by construction: the worker is
not terminated between them.
