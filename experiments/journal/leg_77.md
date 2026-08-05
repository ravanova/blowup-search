# Leg 77 — Route-EXT2: has anyone certified the rank-2 target object since March 2026?

**Branch** `leg/ext2-v1`. **Light, claim-bearing, pure literature watch — no computation, no
solver, no figure.** **Territory:** `experiments/p2_route_ext2_v1_target_watch2.py`,
`writeup/data/p2_route_ext2_v1_target_watch2.json`, `writeup/novelty/leg_77.md`,
`experiments/journal/leg_77.md`. `solver/target_selection.py` was **read, never written** — it
is leg 63's (M2) exclusive territory. The five shared ledgers were not touched.

## The gate, verbatim

> Has a certificate (computer-assisted or analytic) for arXiv:2603.25104's
> `gCLM_degenerate_one_scale` branch been published since March 2026?

**Answer: NO.** Searched **2026-08-06**, **133 days** after the object was posted. The no-branch
applies: the dated literature-watch entry is banked and `solver/target_selection.py`'s
`"certified": "NO"` for this candidate is re-confirmed current, not stale. **0 of 6** theorem-
level statements in the paper's own v2 cover the `a > 0` degenerate branch; **0** indexed
citations; **3** entries from 2026 in the `Constantin-Lax-Majda` ∩ `self-similar` arXiv
enumeration, **0** of which address the branch.

## Order of work

1. `plan_of_record.py` — read (from `/home/andy/projects/Unsolved/.venv/bin/python`; the
   worktree has no `.venv` of its own). `NG` is `NEXT`. Every live ban is a research ban; the
   one that could bind is **"another gCLM measurement leg"**, and this leg **computes nothing,
   measures nothing, and derives no gCLM number** — it searches literature *about* an object,
   so the ban is respected rather than skirted.
2. `capabilities.py` grepped before writing anything (`solver/target_selection.py`, line 340).
   Not edited — outside territory.
3. `DIRECTION.md` leg-77 entry read for the gate and the independence clause.
4. Novelty pass run and **committed first** (`writeup/novelty/leg_77.md`, links not counts),
   before any other file in the quartet, per the leg's own protocol.
5. Script + curated JSON written and run; journal written last.

## What was actually searched

**5** web queries and **4** API enumerations, all logged verbatim with links (not counts) in
`writeup/novelty/leg_77.md` §1. The enumerations are the load-bearing part — they are corpus
sweeps, so the negative does not depend on keyword luck:

- `all:"Constantin-Lax-Majda"` and `abs:"Constantin-Lax-Majda" AND abs:"self-similar"`, newest
  first — the second returns **10** entries total, **3** from 2026.
- an author sweep over De Huang / Jiajun Tong / Xiuyuan Wang — the only 2026 math.AP entry among
  the three is **2603.25104v2 itself**. The discoverers filed no follow-up.
- the Semantic Scholar citations endpoint for the object — **empty `data` array**.

## The decisive read, and why the negative is strong

The paper has a **v2, dated 2026-06-16** — **82 days** after v1 and **51 days** before this
pass. In that revision the authors upgraded the `a ≤ 0` side to theorems (2.4 `a = 0` outer
profile → explicit singular function; 2.6 `a < 0` exact singular family; 2.7 `a < 1` inner
traveling wave by fixed point) and left the `a > 0` degenerate branch exactly where v1 had it:
**§4, titled "Numerical results with degenerate initial data for `a > 0`"**, with the abstract
still reading *"For `a > 0`, we observe one-scale self-similar blowups with regular profiles
that have not been found in previous studies."* The paper's only mention of computer-assisted
proof is in its **related-work** discussion of the De Gregorio model and axisymmetric Euler.

So this is not merely "nobody else got there": the people with the object, the numerics and a
live revision cycle proved the other half and left this half numerical.

## The trap this leg nearly walked into

**Xu, arXiv:2607.19762v1 (2026-07-22)** — the newest gCLM paper in the corpus, **118 days**
after the object — says *"For `a>0` we prove..."*. An abstract-only pass answers **yes** here
and reports a false stale-ledger claim. It is not the certificate on three independent counts:
the branch is *"each admissible smooth focusing profile"*, i.e. the **LSS non-degenerate**
family the ledger's own `q1` note already excludes; the statement is a **conditional two-line
spectral inclusion for a profile assumed to exist**, which certifies no profile even on its own
family; and a keyword check of the page returns **0 hits** for each of `degenerate`,
`degeneracy`, `vanishing order`, `Huang-Tong-Wang`. Recorded as false friend **F1** of **4** in
the JSON, so the next watch does not re-trip it.

One upside fell out of the trap: the ledger's `q1` exclusion ("Huang-Qin-Wang-Wei's analytic
branch is the NON-degenerate one") now covers **two** papers rather than one, since Xu works the
same non-degenerate family.

## Reported, not applied

**3** items for leg 63 (M2) or a future ledger leg, in
`writeup/data/p2_route_ext2_v1_target_watch2.json` under `reported_to_leg_63_not_applied`:
`"certified": "NO"` re-confirmed current (no correction owed); a **precision suggestion** to pin
the paper's version in the `"source"` field, since theorem content grew v1 → v2 while §4 did
not; and the strengthened `q1` exclusion above. **No edit to `solver/target_selection.py` was
made or attempted.**

## Independence from leg 74 (EXT)

Different object (rank 2 vs rank 1), different paper, different authors, different corpus. No
query here targets `HL_S2_nonsymmetric`; Hou-Luo sources appear only as listed off-target
returns. The two findings stand or fall separately.

## For the next re-ask

Cheapest trigger check: re-run the Semantic Scholar citations endpoint and the self-similar
arXiv enumeration. A non-empty citation list, or a **4th** 2026 entry in that enumeration, is
the only signal worth a full pass. Watch metadata is in the JSON under `watch_metadata`.
