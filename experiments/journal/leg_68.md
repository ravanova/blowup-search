# Leg 68 — Route-IX: catching `writeup/INDEX.md` up to leg 57

**Branch** `leg/ix-v1`. **Light mechanical/documentation leg, not critical path.**
**Territory:** `writeup/INDEX.md`, `writeup/novelty/leg_68.md`, `experiments/journal/leg_68.md`.
No shared ledger touched; no solver, runner, data file or figure produced or modified.

## The gate, verbatim

> Do legs 53 (TC) / 54 (MM) / 55 (NB) / 56 (TN) / 57 (XS) each have a complete
> runner/data/BLOG+TECHNICAL/evidence/figure quartet on disk, matching the convention
> documented at the top of INDEX.md?

**Answer: YES.** 25 of 25 quartet pieces present (5 legs x 5 slots), 0 missing, 0 zero-byte.
Per-leg: TC 5/5, MM 5/5, NB 5/5, TN 5/5, XS 5/5. The full file-by-file inventory, with byte
counts for every data JSON and evidence script and the figure reference each doc actually
cites, is `writeup/novelty/leg_68.md` — committed before any edit to `INDEX.md`, as the leg's
novelty pass.

So the yes-branch applied: five rows added, stale text deleted. No `GAP` marker was warranted
on any of the 25 pieces.

## What was stale, in counts

At merge base `925913a`, `writeup/INDEX.md`:

- Arc 4's table ended at Route-T v1 — **5 route rows missing** (TC, MM, NB, TN, XS), covering
  5 merged legs.
- **2 stale assertions about Route-TC**, both claiming it has no writeup and is "in progress
  on `leg/tc-v1`": one paragraph under the `gen*` note, one trailing `## Route-TC (in
  progress...)` section. Both false — leg 53 landed with 5/5.
- `grep -cE "ROUTETC|ROUTEMM|ROUTENB|ROUTETN|ROUTEXS" writeup/INDEX.md` returned **0** before
  the edit, confirming the five routes were absent entirely rather than mislabelled somewhere.

## What changed

1. **5 rows appended** to Arc 4's table, after Route-T v1, in leg order 53 → 57. Each carries
   R/D/B-T/E/F columns and links to its TECHNICAL and BLOG. Headlines are one-line labels
   lifted from each route's own TECHNICAL title; **no numeric claim was written into the
   index**, per the file's own standing rule ("links and one-line labels only").
2. **Both stale Route-TC assertions removed.** The trailing section is replaced by a single
   sentence recording that TC landed as leg 53 and is indexed above.
3. **An index-currency note added**: Arc 4 is current through leg 57, with the 25/25 count and
   a pointer to the inventory.
4. **`Y†` legend introduced** and **2 gap-list items added** (7 and 8) for the two form
   deviations found — both non-gaps, recorded so they are documented rather than silently
   absent:
   - **4 evidence scripts placed in `experiments/`** (MM, NB, TN, XS) instead of beside their
     docs in `writeup/4_p2_lottery/`, where every prior Arc-4 route including leg 53 keeps
     them. All 4 exist and run; this is placement drift, not a missing piece, so `Y†` not
     `GAP`. Moving them would rewrite paths quoted inside their own TECHNICAL files, which is
     outside a links-and-labels remit.
   - **1 duplicated figure number**: `fig48` is claimed by both
     `fig48_route_tc_v1_assemble.png` (leg 53) and `fig48_weight_repairs_v1.png`. Leg 53's
     figure exists and is correctly cited, so its F slot is filled; the collision is a figure
     registry matter and out of territory here.

## Bans checked

`plan_of_record.py` prints 13 active bans. All 13 concern running or re-running measurements
(gCLM measurement legs, Route-D bound sharpening, DSS re-asks, 2D β re-measurement, the
scaling-gauge direction, GA compute on unvalidated fitness, weight-exponent tuning, Z₁
block-coupling repair, stage-V re-opening, truncation-gap-by-domain-extension, the Chen–Hou
target, the 2D near-null direction) or forbid a specific *claim* being restated. This leg ran
no solver, produced no number, and restated no claim — it added links and labels and deleted
two false statements about a leg's status. **0 of 13 bans engaged.**

Two bans are adjacent enough to name explicitly and confirm clear: the ban on reading leg 53's
result as a statement about `HL_S2_nonsymmetric`, and the ban on re-claiming leg 51's
methodological finding at full strength. Neither leg-53 nor leg-51 prose was written or
touched; the TC row's headline says only that the term that ran out is Z₁'s block coupling,
which is exactly the framing the ban itself uses.

## Verification

- `git diff --name-only` against merge base `925913a`: 3 paths, all inside declared territory.
- `scripts/merge_gate.sh origin/main`: PASS.
