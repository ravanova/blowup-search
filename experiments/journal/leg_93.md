# Leg 93 — Route-EXT5: the community's verdict on arXiv:2604.09949

**Date:** 2026-08-06. **Kind:** light, pure literature watch. No computation, no code
edits, no solver module imported, no ledger touched.

## Gate, verbatim

> "Since arXiv:2604.09949 was posted, has any independent group published a
> confirmation, refutation, retraction, or correction of its 3D NS self-similar
> singularity claim?"

## Answer: NO — and one thing the gate did not ask for

**NO.** No independent group has said anything about arXiv:2604.09949 in the **118
days** since it was posted (v1, 2026-04-10). Four channels, zero independent verdicts.

**But:** the pass turned up that the **author** has published **six** papers since,
claiming the **logically opposite** result for 3D Navier–Stokes, using the **same**
5D-lifted axisymmetric machinery, **none** of which cite 2604.09949. That is a de
facto self-refutation. It is **not** a retraction and is not reported as one.

## The channels, with magnitudes

| # | channel | finding |
|---|---|---|
| E1 | source version history | still **v1**, **0** replacements, **0** corrections, **not withdrawn**, no journal-ref, 118 days |
| E2a | Semantic Scholar | `citationCount 0`, `influentialCitationCount 0`, live `CorpusId 287425079` — a **measured** zero, not an indexing miss |
| E2b | OpenAlex **full-text** | `count 0` for the string `2604.09949` — catches discussion-without-citation, still zero |
| E3 | author feed | **8** submissions since; **6** claim the opposite for NS, **2** are Euler (different system, not counted), **0** cite the source |
| E4 | document fetches | 2605.01873 Thm 2.1 `T₊ = ∞` full system, **23** refs, **0** self-citations; 2606.07869 Thm 1.1 `T* = ∞` in the **same** `dμ₅ = r³ dr dz` lift |
| E5 | nearest false positive | arXiv:2606.25341 (Yu, "Structural Audit of NS Obstruction Calculus") **fetched and read** — mentions neither the paper nor the author. Cleared. |

The sharpest single fact: **2604.03519, "Unconditional Axis-Regularity in the 5D
Corridor", was posted seven days BEFORE the singularity paper**, in the same 5D lift.
The two contradictory lines were running **simultaneously**; the singularity paper is
not an earlier position later superseded.

Second sharpest: the regularity line is **actively maintained** — 2605.01875 at **v3**,
2605.01873 and 2605.09797 at **v2** — while the singularity paper has sat at **v1** for
**118 days** with **0** revisions.

## What it does to M-5

**Confirmed current, not stale. Strengthened, not overturned.** M-5's audit found the
arithmetic **closes** (`2δMK = 8.9e−5`; Kantorovich `2M²Kδ = 4.3e−2` with **23×**
margin; `K` reproduced to `2.2e−4`) and rested `CLAIMED_UNUSABLE` on two document-face
reasons. This leg adds a third:

- **(i)** no verification package released;
- **(ii)** Thm 12.1 reconstructs the exactly-**backward** self-similar solution excluded
  by Nečas–Růžička–Šverák and Tsai — **still load-bearing**;
- **(iii) NEW:** the author's own subsequent corpus asserts the negation.

Reason (iii) is cheaper to state — it needs no reading of the manuscript — but is
**weaker as mathematics**: a self-contradicting corpus says one of the two lines is
wrong without saying which. Only (ii) says which. **(ii) stays the load-bearing reason.**

As far as four channels can determine, **M-5 is the only independent check of
arXiv:2604.09949 that exists anywhere.**

## Ledger action

**None.** `solver/target_selection.py`'s rank-6 entry "claimed by arXiv:2604.09949" and
`LITERATURE_CHECK.md`'s `CLAIMED_UNUSABLE` are confirmed current as of 2026-08-06. This
leg never opened either file for writing.

## Limitations, recorded not hidden

1. All four channels see only the **public** record — a referee report or private
   erratum is invisible to all of them.
2. The self-contradiction is **inference from theorem statements**, not a statement by
   the author. Must not be reported as "he retracted".
3. The 2 Euler blow-up papers are a different system and are deliberately **excluded**
   from the count of 6.

## Deliverables

- `experiments/p2_route_ext5_v1_target_watch5.py` — executable query/endpoint log
- `writeup/data/p2_route_ext5_v1_target_watch5.json` — curated data
- `writeup/novelty/leg_93.md` — full-depth findings (committed **before** writeup)
- no figure (pure literature watch)
