# Leg 82 — Route-EXT3 v1: the rank-3 target-object literature watch

**Date: 2026-08-06. Kind: literature watch — light. No computation, no solver call, no figure.**

## Gate, verbatim

> Has a certificate (computer-assisted or analytic) for arXiv:2604.01868 section 6.2's
> `Boussinesq_S2_nonsymmetric` profile been published since the paper's own date?

## Answer

**NO.** Seven channels, 0 of 7 returning a candidate, 5 of them sufficient on their own. The
object has stood open **126 days** past its announcement (v1: 2026-04-02).

The consequence for `solver/target_selection.py`'s rank-3 entry — reported, **not applied**, that
file is leg 63 (M2)'s exclusive territory and was never opened for writing — is that its
`"certified": "NO"` is **current, not stale**.

## What was done, in order

1. `plan_of_record.py` run first. Every ban read. This leg trips none of them: it is not a gCLM
   measurement (it measures nothing at all), not a Route-D bound-sharpening leg, not a DSS
   re-ask, and it aims at nothing — it only *watches*.
2. `capabilities.py` grepped before anything else, per the permanent ban on building without it.
   `Boussinesq_S2_nonsymmetric` appears **nowhere** in it; the registered 2D Boussinesq object at
   line 88 is annotated "the CERTIFIED object", i.e. Chen-Hou's **symmetric** profile — a
   different object, and one the plan of record bans as a target. Nothing was built.
3. Novelty pass run and **committed before the writeup**, as required (`writeup/novelty/leg_82.md`
   §0, commit `Leg 82: LEG — novelty pass: …`).
4. Seven channels run. Three false friends opened in full and excluded on named, quoted grounds.
5. The ledger entry verified **field by field** against the repository's local copy
   `Papers/2604.01868v1.pdf` — the ledger's word was not taken for what the object is.

## The channels

| # | channel | enumerated | candidates |
|---|---|---|---|
| C1 | arXiv submission history of 2604.01868 | the full history block | 0 — **v1 only**, no revision in 126 days |
| C2 | all three authors' arXiv feeds | 28 entries | 0 filed after the source paper, in any field |
| C3 | `all:"Hou-Luo"` | 7 entries, 3 from 2026 | 0 |
| C4 | `abs:"Boussinesq" AND abs:"computer-assisted"` | 7 entries, 1 from 2026 | 0 |
| C5 | Semantic Scholar citations | empty `data` array | 0 — **corroborating only** |
| C6 | `abs:"2D Boussinesq" AND abs:"self-similar"` | 2 entries from 2026 | 0 |
| F1 | open web search | — | 0 |

C5 is deliberately **not** counted as decisive: that index lags arXiv by weeks, so an empty array
is as consistent with lag as with absence.

## The false friends

- **FF1 — Chen-Hou arXiv:2607.15256 (2026-07-16)**, the only 2026 entry on the CAP channel, with
  "computer-assisted proof" in its title and "2D Boussinesq" in its abstract. Excluded on four
  counts: it is a **review** of the [ChenHou2023a,b] low-rank correction method, not a new
  theorem; the object it reviews is Chen-Hou's own **smooth symmetric** profile (already
  certified, and banned as a target); "non-symmetric" and "singular profile" each return **0
  hits**; and 2604.01868 is **not cited**.
- **FF2 — Shi arXiv:2605.16322 (2026-05-05)**, which postdates the source paper and carries a
  genuine **proved** blow-up theorem. Excluded on four counts: the theorem is for a closed
  **(1+1)D boundary-jet reduction** (its own abstract disclaims the scope — "not for the
  unrestricted Boussinesq or Euler systems"); it is a **Riccati** blow-up result that certifies
  no self-similar **profile** at all; no interval arithmetic or CAP; 2604.01868 not cited.
- **FF3 — Rampf-Kolluru arXiv:2601.02464**, excluded before content matters: **1D**, and it
  **predates** the source paper by three months.

## Primary-source verification (`Papers/2604.01868v1.pdf`, `pdftotext -layout`)

Every field of the rank-3 ledger entry checked and **exact**:

| ledger field | line | finding |
|---|---|---|
| `source: "… section 6.2"` | 2309 | heading is *"6.2. Scenario 2: novel self-similar finite-time blowups with positive regular profiles"* |
| `object: "… NON-SYMMETRIC regular profile"` | 2556 | *"Ω converge to a non-symmetric regular profile that remains strictly positive throughout the computational domain"* |
| `ratio_cl_over_comega: -2.4489` | 2560 | *"The computed limiting value of c_l/c_ω is −2.4489, which is remarkably close to the 1D case"* — matches to all four digits; the 1D value is −2.5114 (line 1477), the rank-1 object's number |
| `n_modulation: 3` | 2320–2340 | free constants (c_l, c_ω, c_r); c_θ = c_l + 2c_ω is **determined**. Three, against the 1D object's two |
| `q1: "Numerical only"` | 2069 | the authors themselves name *"stability of (6.2) … using a powerful computer-assisted approach"* as the thing one would want to do |

## The honest weakness

Every channel here is an **absence** argument. Leg 77's rank-2 watch had something stronger — a
**positive act**: the authors revised their paper at 82 days and pointedly left the watched branch
as numerics. This leg has no such act, only 126 days of silence, a title ending in "A Numerical
Investigation", and line 2069's statement of intent. That is weaker evidence, it is recorded as
weaker, and the recommendation is to **re-ask this watch on a shorter interval than rank 2's**.

## For leg 63 (M2), or a future leg

No ledger edit is required. One **precision suggestion** only, of the same kind leg 77 raised for
rank 2: the entry's `"source"` field cites the paper **without a version**, and only v1 exists —
pinning it to `2604.01868v1` makes a future revision detectable by diff rather than by re-reading.
A bookkeeping nicety, not a correction.

## Territory

`experiments/p2_route_ext3_v1_target_watch3.py`,
`writeup/data/p2_route_ext3_v1_target_watch3.json`, `writeup/novelty/leg_82.md`,
`experiments/journal/leg_82.md`. `solver/target_selection.py` **read only, never written.**
