# P4 — Running a computational-mathematics programme that catches its own errors. STATUS.

**Working claim, REVISED 2026-08-19 and now weaker than it was.** A set of mechanical disciplines
— pre-committed gates naming both outcomes, planted controls that must fire in both directions,
`UNDER-RESOURCED` as a verdict distinct from `NO`, verifiers forbidden from checking what they
planned, and bans superseded only by measurement — produces a programme that **finds and retracts
its own errors**, and the evidence is a record of those retractions rather than a claim that it
works.

**The revision, and it is the paper's spine rather than a caveat.** The disciplines that do the
catching are **not** the ones the programme most advertises. Measured 2026-08-19 (`CORRECTIONS.md`
§45): **32 of this repository's 49 `*_evidence.py` scripts reference no data file outside their own
unit's artefact**, and therefore cannot detect a claim that is wrong in the artefact and in the
checker together — the same reasoning wrote both. That failure mode is not hypothetical (`C37`,
§43). **The `N/N evidence checks passed` line that appears in nearly every artefact here is, 65% of
the time, a statement about internal consistency and not about the claim.**

**What actually caught things, on the record below:** units run in parallel and never told each
other's result (`T4`/`T6`); a verifier forbidden from auditing what it planned; a co-tenant's
instrument read from outside the unit; and, repeatedly, someone opening a primary artefact for an
unrelated reason. **Every one of those is a STRUCTURAL separation between the claimer and the
checker. None of them is a check the unit wrote about itself.** If this paper has a thesis, that is
it, and it is considerably less flattering than the one it started with.

**And a second thesis, which fell out of one night's record and may be the more portable of the
two.** Between 02:35 and 03:50 on 2026-08-19 this programme produced **six** defects of its own
(`CORRECTIONS.md` §40–§45, plus a monitor found dead-but-counted). They look unrelated — a
concurrency brief, a gate, three arithmetic slips, a verification layer, a process supervisor —
**and they are one error wearing six costumes: a COUNT or a RATIO quoted as evidence of a property
it does not establish.**

| the number quoted | the property it was taken to establish | why it could not |
|---|---|---|
| `load average 17` | this unit's cost to its neighbour | ambient load is the weather, not a footprint (§40) |
| `0.848 it/s` | the current contended rate | a cumulative average; the fast hours never leave the numerator (§42) |
| `153.22`, largest of six | this point is furthest from stationary | confounded by `|J|`, the very thing that makes it the minimiser (§43) |
| `205 → 162 → 117 → …` | a steady decay | two points reordered, two maxima dropped, from a series with 6.7× spread (§44) |
| `N/N evidence checks passed` | the claim is verified | 65% of the checks read only the artefact their own unit wrote (§45) |
| `4 processes running` | the monitor is monitoring | the wrapper was dead and its orphaned `sleep` held the count (`L6-b`, 03:50) |

**In every row the number was true.** Not one is a miscalculation. The failure is always the
*inference*, and it always runs the same way: **a quantity that is cheap to produce is substituted
for a property that is expensive to establish, and the substitution is invisible because the number
is correct.** A programme that mechanises its own scepticism will mechanise it into exactly these
substitutions, because the mechanism's own outputs are counts and ratios. **That is the finding a
referee should take away, and it is not specific to fluid dynamics.**

**What it costs this paper to say:** the six were caught in seventy-five minutes because two parties
were reading the same live run for different reasons — and **four of the six were caught by the
party who had just been corrected on the previous one.** That is not a discipline. It is two agents
with different vantage points and no incentive to agree, which is cheaper to describe than to
institutionalise, and the paper must not dress it up as a procedure.

## The evidence, and it is unusual because it is all adverse to the programme's own hopes

| what was caught | by | what it overturned |
|---|---|---|
| `R0` retracted its own headline | `R0`, wave 1 | *"Lane R's first measured win"* — the metric counted **cross-run** re-finds as successes, the defect it was introduced to remove, one level up. |
| The lane's central premise measured FALSE | `T4` + `T6`, wave 2 | `arXiv:1902.00384` is certified by the banned apparatus and both rows are 2D lifts. **Two units, two methods, never told each other's result.** |
| An `8×` cost overrun refuted | `V-W3` | Wall-hours against core-hours; the factor **was the worker count**. |
| A post-hoc control criterion located | `V-W5` | On a result the record calls *shut and verified*. |
| A unit's own remedy unexamined | the Conductor, pre-dispatch | `R4-a` was queued as *"Strang"* — a **family name, not a scheme**. Naming it properly (`WAVE8_PLAN.md` AMENDMENT 2, 2026-08-19) found that the gate needed **two** second-order steppers, not one: they differ only in whether the viscous term stays exact, and without the second, *"Crank–Nicolson moved the orbits"* would have been reported as *"`M1`'s reproduction is invalidated"*. The pre-condition attached to it was also withdrawn as defective — it demanded `FULL TEXT` of a 1968 paper to license a **measurement**. Caught **before** dispatch. |
| A load-bearing source read only at abstract | §3k sweep | Leg 348's declared ceiling had carried a lane, a roadmap section, an escalation and a user ruling for **45 legs**. |
| A gate **half-defective**, caught before it fired | the Conductor, mid-run, at iteration 7,000 of 20,000 | `L6-b`'s pre-committed `NO` branch — *"the stall is the CONSTRUCTION"* — **only follows at a stationary terminal iterate, and the wording never required one.** Its `YES` branch is sound. **Naming both outcomes is not the same check as each outcome being entailed by its trigger**, and this programme had been conflating them (`CORRECTIONS.md` §41, 2026-08-19). |

## BLOCKERS

1. **It needs an honest account of what the discipline FAILED to catch, and for how long.** The
   leg-348 ceiling ran 45 legs. The C1 exemplar was ruled on a packet that inherited it. A paper
   that reports only the catches is the failure mode it is describing.
   **A third item, and it is the most uncomfortable of the three because no instrument found it:**
   a dispatch brief asked a unit to report *"the load average at start and end"*. That is the
   weather, not a footprint — the unit could discharge the clause perfectly while its six shards took
   **40% of the throughput of the job beside it** (`CORRECTIONS.md` §40, measured 2026-08-19 at
   1.178 → 0.712 it/s). It was caught because the Conductor happened to look at the co-tenant's
   checkpoint file while both were still running. **Nothing in the discipline would have caught it,
   and nothing in it would have caught the omission either.** This belongs in the paper.
   **A fourth, and it ran longest.** For days the Conductor quoted `L6`'s banked minimiser as
   carrying `scale_invariant_grad = 153.22`, *"the largest of its six starts"*, as evidence it was
   never a critical point — into a landing audit, a wave plan, and a dispatch brief. The same start
   carries `max_abs_grad = 252.2`, **the smallest of the six.** The two columns rank the starts in
   opposite orders **— itself wrong, and corrected at §43, which withdraws the seed comparison
   entirely as confounded by the very property that makes that start the minimiser.** The
   scale-invariant column does govern, for a reason in the record rather than a
   preference — the objective is invariant under `x -> t x` and the raw norm is not — but **a
   selected column was quoted as though it were the whole reading, repeatedly, by the person whose
   job is to catch that.** Nothing flagged it; it surfaced only when the Conductor went to the
   banked JSON to check something else (`CORRECTIONS.md` §41).
   **The pattern across all four: every one was found by looking at a primary artefact for an
   unrelated reason. Not one was found by a discipline designed to look for it.** That sentence is
   the paper's most important finding about its own subject and it must not be softened.
   **A fifth, and it is the sharpest of all because the instrument was complicit.** When the
   `153.22` ranking was withdrawn as confounded (`CORRECTIONS.md` §43), the unit found that its own
   evidence check `C37` **asserted that ranking** — the check would have PASSED on the false claim
   and certified it. A self-check that encodes the defect it exists to catch is not a weak check;
   it is an **error-amplifier wearing the costume of verification**, and this programme's whole
   claim rests on checks of that kind. It was found only because a correction arrived from outside
   the unit and forced a re-examination. **The check did not catch the error; the check was part of
   the error.** `C37` was replaced by one that recomputes the decomposition and requires the
   withdrawal label, plus `C37b` on the rank statistics.
   **And a sixth, twenty minutes later, of the same kind and mine.** The remedy I wrote for a
   half-defective gate (§41) keyed its licence to a **single terminal sample** of a series whose
   trailing spread is 6.7× on one start and 24–34× on the others — **the fix had the same shape as
   the defect it fixed**, naming a quantity without naming how the quantity is read (`§44`).
   **Two consecutive remedies were themselves defective in the same way as what they remedied.**
   That is the paper's second-most-important finding and it is worse than the first.
2. **Framing, not results.** This is the one draft where the material exists and the work is
   deciding what the contribution *is*. Resist writing it as a tour of the repository.
3. **Anonymity and scope.** It describes an ongoing programme with a live prize target and a
   standing outreach hold. What may be said publicly is a **user decision**, not a drafting one.

## What it owes

- A named comparison to existing practice: pre-registration in the sciences, adversarial
  collaboration, and computer-assisted-proof reproducibility norms. §3k rule 3 applies — **this is
  the paper most at risk of reinventing a published idea under a new name.**
