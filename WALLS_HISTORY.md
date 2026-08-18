# WALLS_HISTORY — retracted and superseded text from `WALLS.md`, kept struck rather than deleted

Split out of `WALLS.md` on 2026-08-18 under §3j (headroom), struck text intact. Referenced from
`WALLS.md` as `## History`. **Nothing here is live.** A claim in this file has been retracted or
superseded by a measurement; the measurement that did it is named in place.


**§3j's remedy for this file's cap.** Nothing below is live; it is retained because a wall's history
is the point: a reader who finds only the corrected claim cannot tell whether it was ever wrong.
Full elaboration is in the journals and in git.

## W2's crack and Lane T's item 3 — the same claim, struck

> ~~Leg 348 located `arXiv:1902.00384` — **a certified periodic orbit of 3D Navier–Stokes with the
> viscous term inside the certified equation, on the three-torus.** Natively 3D, natively
> time-dependent, genuinely viscous, genuinely fluid. Not a blow-up, so it does not fill leg 174's
> Grade-A/fluid **blow-up** cell — but the *technology* clears W2's bar already, and only the
> *target* is missing.~~

**RETRACTED by `T4` / leg 393 (`2c87244`)**, from the authors' own data package, not from prose:
`N_x3 = 0`, arrays of extent 1 in `x₃`, `max|u⁽³⁾| = max|ω⁽¹⁾| = max|ω⁽²⁾| = 0.0` exactly against
`max|ω⁽³⁾| = 1.6351 / 1.5274` (so the zeros are structure, not an empty array), `setup = '2D'`; the
authors give the reason — a 3D solve's memory cost is *"for now, prohibitive."* **Certified by
exactly the banned apparatus besides**, and **VERIFIED by `V-W2`** from a re-fetched artefact whose
SHA-256 matched the banked digest. Leg 348 read it at abstract level and flagged that limit itself.
Detail: `experiments/journal/leg_393.md`.

## The `2409.09234` census correction, and the Conductor-wording defect inside it

**The ground is the FIRST clause, not the second** — this file and the dispatch quoting it had them
the wrong way round. **(i) PRIMARY**, `T6` verbatim: *"THIS PAPER CLOSES NO TAIL-DOMINATION ESTIMATE
AND IS NOT AN INSTANCE OF THAT TECHNOLOGY AT ALL"* — a theorem about a **1-D map fitted to DNS
data**; `V-W2` re-measured all five term counts at **0**. **(ii) SECONDARY**, *struck:* ~~"no-slip
walls, not periodicity"~~ — the paper never says *"no-slip"* and states moving-wall Dirichlet with
*"periodicity … enforced to the rest of boundaries"* (§2 p.4). **Count unchanged: 6 − 1 = 5.**
**Second Conductor-wording defect a verifier caught** (`V1` caught the first, on `R0`'s comparand);
**neither found by the Conductor.** Detail: `experiments/journal/verify_wave2.md`.


## §R0/R1 — Lane R's TAKEN and CLOSED units, retired from `WALLS.md` 2026-08-18

*Moved verbatim under ORCHESTRATION.md §3j's retirement amendment (2026-08-18): struck text is
evidence and is never dropped to make room; when the cap binds, history moves out and the live
walls stay. Nothing below is reworded. `WALLS.md` keeps the standing metric and a pointer here.*

### R0 — the metric, pre-committed BEFORE optimisation. **TAKEN, wave 1. Its inference RETRACTED.**

**The standing cross-unit metric is `ORBITS NEW TO THE PROGRAMME PER WORKER-HOUR`**; within-unit,
distinct orbits per worker-hour, per-attempt rate a secondary diagnostic beside it. **The denominator
is WORKER-hours, not machine-core-hours** — physical core count is in **no numeric field** of either
JSON; a future unit must bank `magnitudes.physical_cores` and per-attempt `time.process_time`.
**`V-W3` (2026-08-18) shows what that ambiguity costs: a claimed `8×` cost overrun for `E` was
`core ÷ wall` and equals the worker count. See `STATE.md`.**

| | distinct | worker-hours | distinct / worker-hour | NEW to programme / worker-hour |
|---|---|---|---|---|
| U3 | 8 | 144.69 | 0.0553 | 0.0553 |
| U5 | 5 | 57.04 | 0.0877 | **0.0175 — 3.15× WORSE** |

**THE INFERENCE FROM THIS TABLE IS RETRACTED** — ~~*"U5 is above U3 on every variant, Lane R's first
measured improvement"*~~ **WITHDRAWN.** The per-run arithmetic (1.27×–1.59×) is confirmed; the
inference is not — the metric counts **cross-run** re-finds as successes, the exact defect it was
introduced to remove, one level up. **57 of U5's 100 seeds were already spent by U3; U5's
contribution new to the programme is ONE orbit.** Report **both** rows. Core-hour convention:
**pool reservation (`wall × workers`)**. **`M3 = DELIVERED` SURVIVES** — adjudicated by `V1`, not by
the Conductor that planned it. **Instrument limit:** U3's converged states are **banked nowhere**, so
the numerator 8 is testable only in the `(T, |s|)` pair, deciding pair at **1.288 × TOL**
(`OPTIONS.md` §B).

### R1 — early abort on flatness. **CLOSED 2026-08-13 — the win was already taken.**

~~*"Cheapest competitive win in the repository."*~~ **Withdrawn.** R1's numbers are **CONFIRMED
exactly**, but **U5 had already collected the win** (`resourcing.stall_exit` **is** this criterion,
deployed). Headroom over 12,597 deterministic rules: **+0.48 worker-hours**, and **hold-out shows a
rule selected on U5's 9 convergences KILLS one of U3's 14.** Deployed rule: **zero false kills over
23 banked convergences, 6.90× margin — spend no more here.** The underlying measurement stands and
is reusable: U3's convergence is **bimodal** — all 14 convergences finished in **≤29 epochs**
(median 16) while the 86 non-convergences ran to the 52-epoch cap, **the majority of the run.**

