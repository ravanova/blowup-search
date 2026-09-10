# Leg 440 — unit `K4`, arc 7: THE CONFIRMATION WRITEUP — PRE-REGISTRATION, pushed BEFORE any document is written

**Date:** 2026-09-10, the laptop Conductor. **Shape:** SERIAL (`STATE.md` arc-7 table). **Mode:** §3g step 1 —
this file and the `IN FLIGHT` wave row are committed and pushed BEFORE the work they govern. Arc 6's wave 1
got that ordering backwards and it is recorded as a §3g step-1 defect; it is not repeated here.

## 0. Why a pre-registration for a writeup

A writeup can be steered by its own findings after it has seen them: the temptation is to lead with whichever
unit came out strongest. The verdict below is therefore fixed NOW, before the prose exists, in the wording it
must be answered in. If the material will not support this verdict, the verdict is CORRECTED beside — never
quietly re-aimed.

## 1. The deliverables — `writeup/7_confirmation/`, and nothing outside it

| # | file | what it is |
|---|---|---|
| 1 | `TECHNICAL_CONFIRMATION.md` | the arc's full record, `K0`–`K4`, every number cited by JSON field |
| 2 | `BLOG_CONFIRMATION.md` | the same verdict for a reader who knows fluid dynamics but not this repo |
| 3 | `confirmation_evidence.py` | re-derives every number in (1) from the banked artefacts; exits nonzero on drift |
| 4 | `fig115_arc7_confirmation.png` + its generator, registered in `writeup/build_figures.py` | the quartet's figure (`fig114` is the highest registered) |
| 5 | `CONFIRMATION_FOR_OUTSIDERS.md` | the ONE document written for someone outside this project entirely |

Plus: `writeup/INDEX.md` gains an arc-7 row; `README.md` gains the arc-7 verdict BESIDE the existing banner,
struck-not-rewritten per the arc-6 precedent; `STATE.md`'s `K4` row and `reports/ORCH_STATE.md` are closed.

## 2. THE VERDICT, in its final pre-committed wording

> **The Lean kernel check is GREEN and VERIFIED: on one pinned commit, in three environments and by two
> independent kernels, both exported theorems are accepted depending on no axiom beyond `propext`,
> `Classical.choice` and `Quot.sound`, with `sorryAx` unreachable. That is the whole of what arc 7
> confirms. It confirms that the Lean project proves what its own statements say — and those statements
> are Fefferman's alternatives (C)/(D), which are strictly weaker than the manuscript's Theorem 1.1. It
> is not a confirmation that the 166-page proof is correct, and this repository's independent attempt to
> check the construction numerically produced ZERO surviving evidence in either direction.**

**LEAD WITH THIS.** Every damning-sounding finding — `K3`'s zero, the adversary's five fakes, the three
pre-registration defects, the open semantic-match limit — sits **UNDER** the verdict it qualifies, never
above it and never as the opening. A reader who stops after the first paragraph must not come away with a
false impression in EITHER direction.

## 3. Pre-committed boundaries (any breach is a defect of this leg, recorded in `CORRECTIONS.md`)

1. **The canonical claims list is a CEILING.** `READING_THIS_REPO.md` §"What this repository claims, and
   what it does not" governs. `K4` may RESTATE and may NARROW; it may not add a claim, widen one, or drop a
   "does not claim". If arc 7 has changed what is claimable, the list is EDITED FIRST, in its own commit,
   with the reason — not exceeded silently in prose.
2. **No position on the priority dispute, stated explicitly.** The list's last "does not claim" is *any
   position whatsoever*. Each of the five documents that touches the manuscript's authorship says so in
   words. Silence is not compliance; an explicit sentence is.
3. **Attribution per `NOTICE.md`:** credit **Andy**, link <https://github.com/ravanova/blowup-search>.
4. **Tier 2 is never a proof.** No document claims a wall moved or an `L1→L4` link moved. Neither did.
5. **`K3`'s zero is not a finding against the manuscript** and must never be written as one. It is a
   finding about the GATES, and the three defects behind it are the Conductor's own (`CORRECTIONS.md` §79).
6. **Worker files are not findings** (`READING_THIS_REPO.md`). Every quoted worker line carries its frame.
7. **`UNVERIFIED` vs `VERIFIED` labels are carried, per unit, not averaged over the arc.**

## 4. The evidence script's reading, pre-committed BEFORE it is written

- **PASS:** `confirmation_evidence.py` exits 0 — every number quoted in `TECHNICAL_CONFIRMATION.md` is
  re-derived from a banked artefact under `writeup/data/arc7/`, and every per-unit evidence path it calls
  exits 0.
- **FAIL:** any quoted number does not re-derive. Then the DOCUMENT is corrected to the artefact, never the
  artefact to the document, and the drift is recorded in `CORRECTIONS.md`.
- **INCOMPLETE:** a number in the prose has no banked artefact behind it. That number is REMOVED from the
  prose (it was never evidence), and its absence recorded.

## 5. What `K4` explicitly does NOT do

Re-open any gate; re-run any unit; adjudicate the worker/adversary disagreements `K3` recorded (they stay
recorded, not adjudicated); rule escalations or rulings 5–6; schedule the targeted 399-module semantic-match
check (surfaced to the user, the Conductor does not rule it); or contact anybody — the outreach hold is on
CONTACT, not on publication (ruling 4).
