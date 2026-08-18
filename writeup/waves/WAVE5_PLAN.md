# WAVE 5 — PLANNED AND COMMITTED BEFORE DISPATCH (§3g step 1)

**Committed 2026-08-18, BEFORE any worker was dispatched.** Gates and pre-committed readings are in
their FINAL WORDING here. `STATE.md` carries the wave-5 block by pointer to this file's SHA, per
§3j rule 5 and the cap finding recorded in `reports/ORCH_STATE.md` — **the plan is committed first,
the pointer second, both before dispatch.** Nothing here may be re-worded after dispatch.

**Why these three.** §3f rule 3: the wave **opens with construction** (`L5`), the verifier goes
**last** (`V-W4`). §3i q7 fired on wave 4 — `V3` a grading, `V-W3` a verification, `L2′` a reading,
**zero construction in three** — so wave 5's first unit **must build something**. §3h composition
floor: `L5` attacks **W4 clause (b)** directly, on the Clay chain, from a **non-T lane**. `V-W4`
discharges the standing obligation that wave 4's units are `UNVERIFIED` and **the Conductor may not
verify a wave it planned**. `D-REPAIR` discharges `V-W3`'s located defects, which the hand that
planned wave 4 must not fix itself.

---

## `L5` — Lane L. **CONSTRUCTION. Dispatched FIRST.** ~4–8 h.

**The object.** `L2′` (leg 397, `1493e5e`) measured **W4 clause (a) SHUT**: for any nontrivial
backward λ-DSS blow-up profile of 3D NS the far-field decay exponent is pinned to **exactly `α = 1`**,
and any `α > 1` puts `U ∈ L³(ℝ³)` and yields **full regularity**. Leg 381's bill (`α > 1.5`) therefore
cannot be paid by *more decay*. **The pin binds EXACTLY-(D)SS objects, through the scaling identity
that makes `‖u(·,t)‖_{L³} = ‖U‖_{L³}` constant.** W4 clause (b) — **a natively finite-energy ansatz** —
is the surviving constructive attack precisely because such an ansatz **never asks the profile for
decay at all**.

**GATE, final wording.** Construct the natively finite-energy ansatz explicitly — a **modulated,
localised** ansatz in which the spatial cutoff and the scaling modulation are part of the ansatz
rather than applied afterwards — derive its profile system including **every extra term the
modulation and the cutoff generate**, and then MEASURE, on route 4's **banked** discrete profile:
**is there a cutoff radius `ρ` and a named norm in which the total localisation-plus-modulation error
is SMALLER than the closure threshold it must beat — YES or NO, with the number?** This is the
**analogue for clause (b) of the bill leg 381 banked for clause (a)**, and the answer must be a
number, not a verdict.

**Pre-committed readings.**
(a) A **YES** is a **LEAD, NOT A BROKEN WALL.** It would be a statement about a *discrete, banked*
profile in a *named* norm — **not a certified bound and not a blow-up** — and it must be reported with
what certification would cost (§3d) before anything else is said about it.
(b) A **NO with a number** is a **real, landable result** and **must not be softened**: it prices
clause (b) the way leg 381 priced clause (a), and together with `L2′` it would say the localisation
problem is priced on **both** of its live clauses for the first time.
(c) **THE MOST LIKELY OUTCOME IS THAT THE ANSATZ IS EXACTLY (D)SS IN DISGUISE.** If the constructed
ansatz reduces to an exactly-(D)SS object under any change of variables, **SAY SO, STOP, AND CALL IT
A `NO`** — the pin then applies to it and clause (b) is shut too. **Do not paper over this**; it is
the single most valuable thing this unit can discover, and finding it early is a success, not a
failure.
(d) **Every number comes from the ARTEFACT, never from prose** — route 4's banked profile and
`writeup/data/p2_route_cloc_v1.json` (`self_hash 58c57b62c0cbc80d`). Re-derive; do not quote `STATE.md`.
(e) **C1 BINDS AND IS NOT WAIVABLE BY THE CONDUCTOR.** If this unit reaches for a `Y₀/Z₀/Z₁/Z₂`
radii-polynomial contraction **in any space** it is inside the ban unless it, **in its own
pre-registration**, (1) names its apparatus with a citation and (2) shows that apparatus does not
construct a single bounded approximate inverse uniform in `M`. **C1 may not be cited as evidence that
any apparatus closes for any object class.**
(f) **Lesson 91:** a negative names its **realization, trial space and basis**. A number without them
is not a measurement.
(g) §3d: **`UNDER-RESOURCED` with a cost, never a bare `no`.**
(h) **A ban is superseded by a MEASUREMENT, never by a decision.** If a ban's *wording* obstructs,
that is a **user escalation** — record it, do not rule it, and do not stop.
(i) **No learned or evolved fitness (leg 349). No proposals for more seed supply. READ, do not
CONTACT** — reading published material is authorised, contacting any author group is not.

---

## `D-REPAIR` — infrastructure. ~2–4 h.

**GATE, final wording.** Repair **exactly** the defects `V-W3` located and no others
(`experiments/journal/verify_wave3.md` §4, **D2–D6**), plus the four Conductor debts held open until
`V-W3` returned so as not to destroy a live measurement: **register `fig107` and
`p2_route_t6_v1_evidence.py` in `P2_EVIDENCE`** in `writeup/build_figures.py`; **add `writeup/INDEX.md`
rows for `E` and `V-W2`**; **reconcile `INDEX.md`'s stale in-flight figure allocation table**. Then
answer, **mechanically and with the check left behind as an executable script**: **does
`build_figures.py` self-check every figure the record cites — YES or NO, with the enumeration?**

**Pre-committed readings.**
(a) **Repair only what is listed.** Anything else found is **REPORTED, NOT REPAIRED** — a new defect
is a new unit.
(b) **NO BANKED ARTEFACT MAY BE REWRITTEN TO MATCH A LATER FINDING.**
`writeup/data/p2_route_vbs_v1_scoping.json::the_empty_cell.meaning` is measured FALSE and is
**EXPLICITLY OUT OF SCOPE** — it is question (Q3) of an OPEN user escalation.
(c) If a listed defect turns out **not to exist**, say so plainly — that is a finding about the
verifier and is worth more than a silent no-op.
(d) `scripts/merge_gate.sh origin/main` must print **MERGE GATE: PASS** before you finish.
(e) **Lesson 68:** a check that is not executable decays. Leave the check runnable, and run it.

---

## `V-W4` — verification, **OBLIGATORY, dispatched LAST.** ~3–5 h.

**Covers WAVE 4 ONLY** (`V3`, `L2′`). **You did not plan these units: REPORT, DO NOT REPAIR.**

**GATE, final wording.** From **re-fetched primary sources and banked artefacts alone** — never from a
journal's narrative — do these reproduce **exactly**?
**(1)** `V3`'s **YES** (`16ba44e`, `writeup/data/p2_route_v3_gradeA_v1.json`): does `arXiv:2509.25116`
pass **both** of leg 174's clauses, on **your own** reading of the paper — the interval certificate
encloses a solution of an equation **carrying the dissipative term**, and the equation is a **genuine
fluid** equation? And is the object **not** a finite-time singularity, as `V3` reports?
**(2)** the **8 `NO` rows** — does each failing clause hold as quoted?
**(3)** `L2′`'s **pin at `α = 1`** (`1493e5e`, `writeup/data/p2_route_l2_decay_v1.json`): re-fetch
`1610.09464` and `2607.09619`, verify the decisive quotes by anchor and hash, and answer the question
the Conductor flagged as this result's **load-bearing ceiling** — **the "at most 1" direction rests on
Escauriaza–Seregin–Šverák, which was NOT read at primary and reaches the record only through two
secondaries. Does the direction actually follow?**
**(4)** the **18 adjudications** — spot-check **all 8 `FAILS-BY-CONSTRUCTION`** and **the 1
`SATISFIED`**: is any verdict wrong on the quoted hypothesis?
**(5)** `L2′`'s bill re-derivation against `p2_route_cloc_v1.json` — do the numbers and the
`self_hash` match?

**Pre-committed readings.**
(a) Reproducing everything is **PASS, and a real result** — say so plainly.
(b) **Any discrepancy is reported FIRST and is not softened.**
(c) Re-measure from artefacts and re-fetched primaries, **never from prose**.
(d) **`UNVERIFIABLE` is a valid verdict** with its reason. A source you cannot reach banks as
`UNREACHABLE`, **never as a zero**; **no S2 key exists here**.
(e) **REPORT, DO NOT REPAIR.** A fix is a separate unit.
(f) **Lesson 68:** leave an executable re-derivation behind.
(g) **You may not verify a wave you planned.** This verifier covers **wave 4 only**.
(h) **READ, do not CONTACT.**

---

## Carried in EVERY wave-5 brief

**COMMIT DURING THE RUN, NOT ONLY AT THE GATE.** A host process exit on 2026-08-14 took five in-flight
workers and wave 3 lost three of four the same way; **the pre-registrations survived because they were
committed, three worktrees of partial result JSON did not.** Any unit above ~1 h wall **checkpoints to
disk at a granularity it can resume from, and says where.**

**Scale is not evidence. Tier 2 is never a proof. No output is movement toward Clay unless a link of
`L1 → L4` actually moved — Clay is ~0.05%.** A retraction is not progress. **Screening is not a unit
of work.** Report your own ceiling; `UNDER-RESOURCED` with a cost beats a confident `no`.
