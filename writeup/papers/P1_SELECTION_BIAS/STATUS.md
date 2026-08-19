# P1 — Selection bias in recurrence mining. STATUS.

> **STOP — LEG 411 (`PB1`, wave 8) ANSWERED THE NOVELTY GATE AND `P1` IS KILLED. BOTH EFFECTS ARE ALREADY IN PRINT AT `S3`. DO NOT DRAFT THIS PAPER PAST ITS TITLE.**
> See `NOVELTY.md` (verdict) and `FINDINGS.md` (nine findings about the record).
> Everything below this line is the PRE-GATE status and is left UNEDITED on purpose.

**Working claim.** A scalar recurrence score used as an *admission filter* biases the recovered
orbit set along any coordinate the score is monotone in — and a second run over the same trajectory
silently re-finds what the first already found.

## What is banked for it

| evidence | field | note |
|---|---|---|
| Bias in **period** | AMENDMENT 4, `prog_r4_u2u3_prereg_addendum.md` §3d | Found first, in a different coordinate. Two coordinates makes it a mechanism, not an anecdote. |
| Bias in **shift** | `p2_prog_r4_m3_v1.json` | Rank correlation `|s|`↔`R` = 0.50; admission by `R<0.25` falls 44% / 20% / 11% / 3% across bands; median `R` 0.32 at `|s|<0.15` vs 0.83 in the published band. |
| The **repair did not repair recovery** | `p2_prog_r4_m3_v1.json` | In-band supply 35→72, spend 31→60, and still 0 of 100 named rows. The bias is real *and* fixing it did not fix the outcome — which is the honest and more interesting version. |
| **Cross-run re-finding** | `R0`, `p2_prog_r4_r0r1_v1.json` | 57 of U5's 100 seeds identical to U3's; 5 of 9 convergences bit-identical re-executions; 4 of 5 distinct solutions re-finds. A second 100-attempt budget bought **one** orbit new to the programme. |
| **Metric consequence** | `R0` | Per-attempt convergence rate is inflatable by easier seeds and counts a re-find as a success. Distinct orbits per core-hour is the metric that is not. |

**Verified?** `R0` VERIFIED by `V1`. `U5`/`M3` VERIFIED as *surviving its own wording* by `V1`;
U2/U3/U5 themselves remain **UNVERIFIED**. Say so in the draft.

## BLOCKERS — enumerated before any drafting

1. **THE NOVELTY CHECK HAS NEVER BEEN RUN.** Owed since wave 1. Recurrence mining is mature —
   Chandler–Kerswell, Lucas–Kerswell, Cvitanović. **This may be known folklore, unstated in print.**
   It is the one blocker that can kill the paper outright, and it is cheap. **RUN IT FIRST.**
2. **One flow, one `Re`, one trajectory.** 2-D Kolmogorov, `N=24`, `Re=60`, forcing `n=4`, a single
   `T=1e5` run. A referee will ask whether the effect is a property of scores or of this flow.
3. **The realization is first-order in time** (Lie–Trotter, measured global ratio 2.00). Disclose it;
   it bounds what the recovered set means, and `R4` may change it.
4. **`SOURCES.md` depth.** The three comparison papers must be `FULL TEXT`, not `CITATION`, before
   the related-work section can be written honestly. §3k rule 2.

## What it owes

- The novelty verdict, **whichever way it comes out**, banked before drafting proceeds past §1.
- A statement of what the effect is *not*: it does not explain the 0-of-216 non-recovery — `E`
  refuted the supply hypothesis at seed quality no filter can beat.

---

# LEG 411 ADDENDUM — THE NOVELTY GATE IS DISCHARGED, AND IT KILLED THE PAPER

**ADDITIVE ONLY. Nothing above was edited** — including blocker 1's "THE NOVELTY CHECK HAS
NEVER BEEN RUN", which is now false but is a banked statement and is not this unit's to
rewrite. The correction is placed beside it, not over it. **Disclosing that choice rather
than making it silently is the point.**

**BLOCKER 1 — DISCHARGED. Outcome: `YES` / `YES`. `P1` HAS NO NOVEL CENTRAL CLAIM.**

* **Effect (a)** — a scalar recurrence score used as an admission filter biases the recovered
  orbit set along coordinates the score is monotone in: **IN PRINT, `S3`.** Page, Holey,
  Brenner & Kerswell, *JFM* **991** (2024) A10 (`10.1017/jfm.2024.552`, arXiv:2309.12754v1),
  pp.2/16/18 — the more unstable structures are `not flagged in this approach at all`. Also
  Chandler & Kerswell 2013 p.13 in shift coordinates, **twelve years old.**
* **Effect (b)** — a second run over the same trajectory re-finds what the first found:
  **IN PRINT, `S3`.** Chandler & Kerswell 2013 p.14 (`considerable duplication`, quantified in
  Table 1); Lucas & Kerswell 2015 v1 p.5 (two thirds of short-period guesses skipped BECAUSE
  they were known repeats).
* **THE WORD `silently` IN THIS PAPER'S OWN WORKING CLAIM IS CONTRADICTED BY ITS OWN INTENDED
  SOURCES.** The field reports the duplication, counts it in a published table, and budgets
  around it. A draft asserting it goes unnoticed would have been refuted by its own
  bibliography.

**Blocker 4 (SOURCES depth) is overtaken:** all three comparison papers, and nine more, are
now at `FULL TEXT` depth with hashes — `writeup/SOURCES.md` rows 36–48, `Papers/MANIFEST.md`.

**What survives, and it is NOT a paper.** The programme holds a quantitative instance of a
known effect on its own system. A known effect measured on a new system is a result for the
record, not a contribution to the literature, **and this unit is not authorised to decide it
is one.** That call is the Conductor's.

*A `YES` was pre-committed as a good result and the cheapest possible way to learn it. It is
recorded as exactly that. The kill is not written up as progress.*
