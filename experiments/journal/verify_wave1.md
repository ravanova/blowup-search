# V1 — WAVE 1 VERIFIER (CONDUCTOR mode, ORCHESTRATION.md §3f)

Unit: `V1`. Dispatched in wave 2 to verify wave 1 (`T1`, `T2`, `R0+R1`).
Branch: `verify/wave1`. Base: `main` @ `c1a8d5e`.
Date: 2026-08-13/14.

**Verification is a fresh session or it is not verification.** This session did not plan,
build, or read the construction of any wave-1 unit. Everything below is re-derived from
banked JSON under `writeup/data/` and from landed ledgers/evidence scripts under
`experiments/` alone.

## §0 — READ DISCIPLINE, DECLARED

NOT READ this session (forbidden by the dispatch, and confirmed by this session's own
tool log): `DIRECTION.md`, `WALLS.md`, `STATE.md`, `OPTIONS.md`, `reports/ORCH_STATE.md`,
the wave-1 dispatch briefs, and the REASONING of the wave-1 journals
(`experiments/journal/leg_391.md`, `experiments/journal/leg_392.md`,
`experiments/journal/prog_r4_r0r1.md`).

Pointer lookups performed, and only pointer lookups: `git log --stat` over the wave-1
commits, to learn **which file** each unit landed. That is a path lookup, not an argument.

Consequence, stated up front and honestly: every WALLS.md figure named in my gate is
therefore checked against the wave-1 unit's own **banked re-derivation** of it and against
the **primary ledgers**, never against WALLS.md itself, which I may not open. Where the
gate quotes a WALLS.md number I treat that quoted number as the target and re-derive the
value independently from primary data.

## §1 — THE GATE, VERBATIM AND PRE-COMMITTED

> Re-deriving from banked JSON and landed evidence scripts alone, do all five of the
> following reproduce **exactly**?
> **(1)** `R0`'s metric — U3 = 8 / 144.69 = **0.0553** and U5 = 5 / 57.04 = **0.0877**
> orbits-new-to-the-programme per worker-hour — **and** the **134.45 vs 144.69**
> reconciliation: attempt CPU as `Σ attempts[].wall_seconds / 3600` against pool
> reservation as `wall_seconds × workers`, giving **92.92%** utilisation.
> **(2)** `R0`'s retraction — **57/100** seed overlap, **5 of 9** bit-identical, **4 of 5**
> re-finds, **ONE** new orbit, and the corrected metric **0.0175** against the originally
> claimed **0.0553**.
> **(3)** `R1`'s **+0.45 pp** headroom, and the hold-out kill of **one of U3's 14**.
> **(4)** `T2`'s **32/32 MEASURED**, served opensearch namespace **`1.1`**, **5-of-6
> THROTTLED**, and a negative control returning **0 in both instruments**.
> **(5)** `T1`'s packet ruling **none** of the three questions it posed.
> **PLUS the question the Conductor deliberately declined to answer:** does
> **`M3 = DELIVERED`** survive U5's **57%** seed overlap, judged **on M3's own
> pre-committed wording** — which you must locate in the banked record and quote verbatim
> before you judge it?

## §2 — PRE-REGISTERED DERIVATION PATHS

Fixed **before** any value was computed. The only prior inspection was a survey of
**field names** (a `keys()` dump), required to name a path at all; no re-derivation was
run and no comparison was made before this section was written and committed. Every path
below is anchored in the **primary** artifact (the unit's own ledger / measurement JSON),
not in `R0`'s summary of it, so that `R0` is genuinely under test rather than quoted back
to itself.

### Item 1 — R0's metric and the 134.45 vs 144.69 reconciliation

Primary sources: `writeup/data/p2_prog_r4_g1_v1.json` (U3),
`writeup/data/p2_prog_r4_m3_v1.json` (U5).

* `pool_reservation_core_hours := magnitudes.wall_seconds * magnitudes.workers / 3600`
  — U3 expected `144.69`, U5 expected `57.04` (2 dp).
* `attempt_cpu_core_hours := sum(a["wall_seconds"] for a in attempts) / 3600`
  — U3 expected `134.45` (2 dp).
* `pool_utilisation := attempt_cpu / pool_reservation` — U3 expected `0.9292` → **92.92%**.
* `metric := n_distinct / pool_reservation_core_hours`, with `n_distinct` re-derived, NOT
  read: cluster `attempts[].{T_converged, |s_converged|}` over the converged attempts at
  the arbiter's own tolerance, taken from `r0.cluster_rule_verbatim` in
  `writeup/data/p2_prog_r4_r0r1_v1.json` (which quotes
  `experiments/p2_prog_r4_m3_evidence.py` §5 verbatim). Expected `8` (U3) and `5` (U5).
  Robustness: single-linkage and complete-linkage must both give the same count.
* Expected metrics: U3 `0.0553`, U5 `0.0877` (4 dp).

Note on the U5 sign convention: U3's ledger banks `s_converged`, U5's banks
`abs_s_converged`. The cluster key is `|s|` for both, per the quoted rule.

### Item 2 — the retraction

Primary sources: the two ledgers' `attempts[]` arrays, joined on the seed key.

* Seed key `(T_seed, s_seed, R_seed)` at full float precision, with `|s_seed|` used on
  both sides for the sign convention above.
* `57/100` := `#{U5 attempts whose seed key appears in U3's 100 seed keys}`.
* `5 of 9` := of U5's `9` converged attempts, how many carry a seed key U3 also spent.
* `4 of 5 re-finds` and `ONE new orbit` := cluster U5's `5` distinct orbits against U3's
  `8` distinct orbits at the same tolerance; count U5 clusters with no U3 counterpart.
  Expected `1` new, hence `4` re-finds of `5`.
* `corrected metric := 1 / 57.04` → expected `0.0175` (4 dp).
* The comparand `0.0553`: the gate's wording is ambiguous between (A) U3's metric `0.0553`
  and (B) U5's own originally claimed metric, which item (1) of the same gate gives as
  `0.0877`. **I do not re-word the gate.** I test both readings and report which holds.

### Item 3 — R1

Primary source: `writeup/data/p2_prog_r4_r0r1_v1.json` `r1` block, cross-checked by
re-executing the landed `experiments/programme_r4/r1_flatness.py` criterion **in my own
code** against the ledgers' `residual_history` arrays.

* `headroom_percentage_points := (best_admissible_u3_recovery - incumbent_u3_recovery)*100`
  → expected `+0.45` pp (2 dp).
* Independent re-implementation of the abort rule
  `abort at epoch k iff k >= K and ||R||_k > theta*||R||_{k-W}`, applied to U3's
  `residual_history` at both `r1.headroom.best_admissible_rule` and the incumbent rule,
  must reproduce both recovered fractions.
* `hold-out kill of one of U3's 14`: fit direction `fit_on_u5_scored_on_u3`, field
  `heldout_false_kills` expected `1`; re-derived by applying that rule to U3's **14**
  converged attempts and counting how many abort before their converged epoch.

### Item 4 — T2

Primary source: `writeup/data/p2_route_trig_v1.json`, recounted from the raw per-query
records, never from the `coverage` summary block.

* `32/32 MEASURED` := over `queries.*` (all six families) plus `controls`, count records
  with `status == "MEASURED"`; total record count must be `32` and MEASURED count `32`.
  (Whether controls are inside or outside the 32 is itself part of the check.)
* namespace := `set(r["opensearch_namespace_served"])` over all arXiv records; expected the
  single value `http://a9.com/-/spec/opensearch/1.1/`, i.e. namespace **1.1**.
* `5-of-6 THROTTLED` := over `s2.substantive`, count `THROTTLED`; expected `5` of `6`.
  A THROTTLED record must carry `total is None` and **never** `0` — checked, per the
  leg-387 fabricated-zero lesson.
* negative control `0 in both instruments` := the same nonsense query string must appear in
  `controls` (arXiv) with `status == MEASURED, total == 0` **and** in `s2.controls` with
  `status == MEASURED, total == 0`.
* Positive datum proving the service was reached: an HTTP 200 with a parsed non-zero
  `totalResults` on each instrument, banked in the same record set.

### Item 5 — T1

Pointer lookup says T1 (leg 391) landed **no `writeup/data/*.json`** and **no evidence
script**: its only artifacts are `experiments/journal/leg_391.md` (whose reasoning I may
not read) and `writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`.

Pre-registered path: search `writeup/data/` for any T1/leg-391 JSON. If none exists, the
claim "the packet rules none of the three questions it posed" is checked **structurally
only** against the packet: enumerate the three questions the packet poses, and confirm each
carries an explicit non-ruling. If the packet does not itself carry a machine-checkable
per-question verdict field, the item is **`UNVERIFIABLE`** under this gate's own standard
("banked JSON and landed evidence scripts alone"), reported as a banking-discipline defect
naming the absent file — **not** as evidence the claim is false (reading (c)).

### The M3 question

Pre-registered search for M3's pre-committed wording, in this order, stopping at the first
hit:
1. `writeup/data/p2_prog_r4_m3_v1.json` → `milestone.question`, `milestone.clauses`,
   `milestone.preregistered`.
2. The pre-registration the JSON's `preregistered` field points at.
3. `grep -rn "M3" writeup/data/ experiments/programme_r4/`.

Judgement rule, fixed now: M3 is judged **only** against the clauses its own pre-committed
wording states. For each clause I record `SATISFIED` / `NOT SATISFIED` / `SILENT` on the
evidence, and the verdict is: `M3 = DELIVERED` survives iff **no clause its own wording
states is falsified by the 57% overlap**. If M3's wording is silent on seed novelty, the
finding is that it is SILENT — not that it implicitly required it. I do not import a
novelty requirement M3 did not pre-commit to, and I do not excuse one it did.

## §3 — LESSON 68

The result of this unit is `experiments/p2_verify_wave1_v1_rederive.py`, which exits
non-zero on any mismatch. Gating is by **exit code**. Nothing below is gated by a printed
line.

## §4 — CEILING

TIER 2. Confirming arithmetic is not a link of the `L1→L4` chain. Nothing this unit
returns is movement toward Clay, whatever it returns. Clay stays ~0.05%.

---

## §5 — RESULTS

`experiments/p2_verify_wave1_v1_rederive.py` — **38 checks, 38 passed, EXIT 0.**
Machine record: `writeup/data/p2_verify_wave1_v1.json`.

**ANSWER TO THE GATE: all five reproduce, and `M3 = DELIVERED` survives.**

Per reading (a), agreement is expected and worth little, so the reproductions are
tabulated and not argued. The effort below is spent on the four places where something
could have been wrong.

| # | claim | re-derived | verdict |
|---|---|---|---|
| 1 | U3 = 8/144.69 = 0.0553 | 144.688755, 0.05529110 | reproduces |
| 1 | U5 = 5/57.04 = 0.0877 | 57.035181, 0.08766519 | reproduces |
| 1 | 134.45 vs 144.69 → 92.92% | 134.447483 / 144.688755 = 0.929219 | reproduces |
| 2 | 57/100 seed overlap | 57/100 | reproduces |
| 2 | 5 of 9 bit-identical | 5 shared-seed, 5 bit-identical of 9 | reproduces |
| 2 | 4 of 5 re-finds, ONE new | 4 re-finds, 1 new (T=20.417511, \|s\|=0.586670, UPO37, attempt 7) | reproduces |
| 2 | corrected 0.0175 | 1/57.035181 = 0.01753304 | reproduces |
| 3 | +0.45 pp headroom | 0.45366170 pp | reproduces |
| 3 | hold-out kill of one of U3's 14 | 1 false kill of 14 | reproduces |
| 4 | 32/32 MEASURED | 32 substantive, 32 MEASURED (+5 controls, 5/5) | reproduces |
| 4 | namespace `1.1` | `http://a9.com/-/spec/opensearch/1.1/`, sole value | reproduces |
| 4 | 5-of-6 THROTTLED | 5/6, every one `total = None` | reproduces |
| 4 | negative control 0 in both | arXiv 0 / S2 0, same query string | reproduces |
| 5 | packet rules none of three | (a),(b),(c) × 2 readings, none ruled | reproduces (prose only) |

### The four things worth reporting

**(i) A BANKING-DISCIPLINE DEFECT, not a `no`. T1 banked no machine record.**
Under this gate's own evidence standard — "banked JSON and landed evidence scripts
alone" — item (5) is the one item that **cannot** be met, because T1 (leg 391) landed
**no `writeup/data/*.json` and no evidence script**. Its artefacts are
`experiments/journal/leg_391.md` (reasoning, forbidden to me) and the prose packet
`writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md`.

The search I ran, so the absence is auditable: every `writeup/data/*.json` was opened and
its own `leg` / `route` / `unit` provenance fields scanned for `391`, `ban_wording`, or a
`T1 … WAVE 1` unit string. **Zero hits.** (A filename-substring search is not sufficient
here: it returns `p2_route_p2t1_v1.json`, which is leg **302**, route **P2T1**, and
unrelated.)

So the claim itself checks out against the landed packet — the packet states
*"This packet rules nothing"* and *"It ruled none of (a), (b), (c). No reading is endorsed,
preferred, ranked, or recommended"*, and structurally carries exactly two READING sections
for each of (a), (b) and (c), with (d) explicitly labelled *"Not a ban-wording question"*.
But it checks out **against prose, not against a machine record**. Per reading (c) this is
reported as a defect in the banking discipline, naming the absent file. It is **not**
evidence the claim is false. A future unit of this shape should bank the packet's
per-question verdict as JSON so the next verifier is not reduced to grepping headings.

**(ii) AN AMBIGUITY INSIDE THE GATE'S OWN WORDING. Banked, not reconciled.**
Item (2) asks for *"the corrected metric 0.0175 against the originally claimed 0.0553."*
Two readings of `0.0553` are available and exactly one holds:

- **Reading A — `0.0553` is U3's metric.** HOLDS. `8/144.688755 = 0.05529110 → 0.0553`
  (`writeup/data/p2_prog_r4_g1_v1.json`, `magnitudes.wall_seconds` × `magnitudes.workers`).
  The corrected U5 figure `0.0175` falls **below** it — which is exactly the retraction.
- **Reading B — `0.0553` is U5's own originally claimed metric.** DOES NOT HOLD. U5's own
  original claim is `5/57.035181 = 0.08766519 → 0.0877`, as **the same gate's item (1)**
  states (`writeup/data/p2_prog_r4_m3_v1.json`).

I do not re-word the gate and I do not decide which was meant. Both numbers, both
derivations, and both source files are stated; **the Conductor reconciles, not me.** Note
this is an ambiguity in the *gate text*, not a disagreement with any banked figure — every
banked figure reproduced bit-identically.

**(iii) The metric re-derivation is genuinely independent, and survives its robustness
check.** The distinct-orbit counts were not read from `R0`; they were re-clustered from
`attempts[].{T_converged, |s_converged|}` under the rule R0 itself names as arbiter
(`experiments/p2_prog_r4_m3_evidence.py` §§35–53, 70–81), **re-implemented here rather than
imported**, so a bug in the arbiter would surface as a disagreement instead of being
inherited. U3 = 8 and U5 = 5 under **leader/greedy, single-linkage and complete-linkage
alike** — the counts are not an artefact of the greedy ordering. Likewise R1: the abort
criterion was re-implemented from its stated family and reproduces `4629 → 2083` epochs and
`0.5500108014689997` **to the last bit**, and the hold-out kill of one of U3's 14 lands on
the same attempt.

**(iv) Instrument honesty.** Run 1 (`0633494`, exit 1) failed three checks. All three were
defects in **my own script**, not in wave 1; each is named in
`notes.instrument_repairs_after_run_1` in the banked JSON, the failing run is committed
before its repair, and no wave-1 artefact was adjusted. Recorded because a verifier that
silently repairs itself between runs is indistinguishable from one that moved its target.

### THE M3 QUESTION

**Located** — M3's pre-committed wording is in the banked record twice, in agreement:
`writeup/data/p2_prog_r4_m3_v1.json` → `milestone.question` + `milestone.clauses`, whose
`preregistered` field points to `experiments/journal/prog_r4_u2u3_prereg_addendum.md`
§3g.3 (AMENDMENT 5), *"committed before either stage ran"*. **Quoted verbatim from §3g.3:**

> **M3: THE SEED BUDGET IS STRATIFIED BY SHIFT — the anchored reservoir is exhausted, the
> published `|s|` band is filled to a pre-committed quota, and the per-stratum yield is
> measured against U3's banked baseline.**
>
> **DELIVERED** iff all five hold:
>
> 1. the mining pass takes **every** anchored strict local minimum not provably excluded by
>    the Newton window (§3g.4), and reports the realised counts;
> 2. the 100-attempt budget is allocated by the §3g.4 quota, with **at least 50** attempts
>    seeded in the published band `|s| ∈ [0.295, 0.707]` against U3's 31;
> 3. the run completes at U3's caps, `tol`, admission test, `m = 0` requirement, anchor rule
>    and matching predicate, with **none of them changed** and no iterations bought;
> 4. the per-stratum convergence yield is reported against U3's banked baseline, with the
>    in-band rate stated as a magnitude either way;
> 5. the planted controls fire as planted.

**ANSWER: `M3 = DELIVERED` SURVIVES the 57% seed overlap.**

Judged on that wording and on nothing else, per reading (d):

- **No clause conditions DELIVERED on seed novelty**, orbit novelty, or non-overlap with
  U3. The five clauses are about *exhaustiveness of the mining*, *in-band quota*, *unchanged
  settings*, *yield reporting*, and *controls*. Seed novelty is absent from all five.
- **Clause 1 does more than stay silent — it predicts the overlap.** It requires taking
  **every** anchored strict local minimum of the same anchored reservoir U3 drew from. A
  large overlap with U3's spend is what compliance with clause 1 *looks like*; a low overlap
  would be the thing needing explanation. The overlap is a consequence of the clause, not a
  breach of it.
- The clauses the overlap could conceivably touch were re-derived, not read: **clause 2** —
  60 in-band seeds against U3's 31, ≥ 50 (re-counted from `attempts[].s_seed` under the
  same `wrap_abs` convention); **clause 3** — `tol`, `max_newton`, `max_gmres`, `gmres_rtol`,
  `N`, `Re`, `T_dns`, `n_attempts` all equal to U3's; **clause 5** — controls fired as
  planted, zero failures.

**What this answer is not.** It is not a finding that M3 was *well*-worded. The overlap
does falsify a different claim — the per-run distinct-orbits-per-core-hour inference — and
`R0` has already retracted that one. M3 simply never made it. If the programme wants a
milestone whose DELIVERED implies novel supply, that requirement has to be *written into*
the milestone before the run; it was not written into M3, and I decline to read it in after
the fact.

### §3d RESOURCING

No item returned `UNDER-RESOURCED`. Every item was answerable at the scale posed, from
banked artefacts, at negligible cost (the whole re-derivation runs in seconds). No stop
fires from this unit.

### CEILING

**TIER 2. Not a proof, and not movement toward Clay.** Confirming arithmetic is not a link
of the `L1 → L4` chain, and no such link moved. Clay stays ~0.05%. Five reproductions buy
the programme almost nothing (reading (a)); what this unit actually delivers is (i) the
named banking defect at T1 and (ii) the gate-text ambiguity at item (2), both handed to the
Conductor un-reconciled.
