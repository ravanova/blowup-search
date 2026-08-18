# VERIFY WAVE 4 — unit `V-W4`, wave 5 verifier (ADVERSARIAL)

Branch `verify/wave4`. Data `writeup/data/p2_verify_wave4_v1.json`.
Re-derivation script: `experiments/verify_wave4_rederive.py`.

**Covers WAVE 4 ONLY** — `V3` (`16ba44e`) and `L2'` (`1493e5e`). This unit did not plan them.
**REPORT, DO NOT REPAIR.**

---

## §0 — THE GATE AS GIVEN, read from disk at `1e49a00`

Source of truth: `git show 1e49a00:writeup/waves/WAVE5_PLAN.md`, section
"## `V-W4` — verification, **OBLIGATORY, dispatched LAST.**". Reproduced here in its committed
wording; nothing added, nothing dropped.

**From re-fetched primary sources and banked artefacts alone — never from a journal's narrative — do
these reproduce exactly?**

**(1)** `V3`'s **YES** (`16ba44e`, `writeup/data/p2_route_v3_gradeA_v1.json`): does `arXiv:2509.25116`
pass **both** of leg 174's clauses, on **my own** reading of the paper — the interval certificate
encloses a solution of an equation **carrying the dissipative term**, and the equation is a **genuine
fluid** equation? And is the object **not** a finite-time singularity, as `V3` reports?

**(2)** the **8 `NO` rows** — does each failing clause hold as quoted?

**(3)** `L2'`'s **pin at `alpha = 1`** (`1493e5e`, `writeup/data/p2_route_l2_decay_v1.json`): re-fetch
`1610.09464` and `2607.09619`, verify the decisive quotes by anchor and hash, and answer the question
the Conductor flagged as this result's **load-bearing ceiling** — **the "at most 1" direction rests on
Escauriaza-Seregin-Sverak, which was NOT read at primary and reaches the record only through two
secondaries. Does the direction actually follow?**

**(4)** the **18 adjudications** — spot-check **all 8 `FAILS-BY-CONSTRUCTION`** and **the 1
`SATISFIED`**: is any verdict wrong on the quoted hypothesis?

**(5)** `L2'`'s bill re-derivation against `p2_route_cloc_v1.json` — do the numbers and the
`self_hash` match?

### Pre-committed readings — binding, copied from the plan

(a) Reproducing everything is **PASS, and a real result** — say so plainly.
(b) **Any discrepancy is reported FIRST and is not softened.**
(c) Re-measure from artefacts and re-fetched primaries, **never from prose**.
(d) **`UNVERIFIABLE` is a valid verdict** with its reason. A source I cannot reach banks as
`UNREACHABLE`, **never as a zero**; **no S2 key exists here**.
(e) **REPORT, DO NOT REPAIR.** A fix is a separate unit.
(f) **Lesson 68:** leave an executable re-derivation behind.
(g) **I may not verify a wave I planned.** This verifier covers **wave 4 only**.
(h) **READ, do not CONTACT.**

### Carried constraints (from the brief, binding)

- A ban is superseded by a **MEASUREMENT**, never a decision. A defective ban **wording** is a
  **USER escalation** — record it, do **not** rule it. **C1 binds, is not waivable, and may not be
  cited as evidence that any apparatus closes.**
- Scale is not evidence. Tier 2 is never a proof. **No output is movement toward Clay unless a link
  of the L1->L4 chain actually moved.** Clay ~ 0.05%.
- A retraction is not progress and must never be described as such.
- Instrument every zero: `THROTTLED` and `UNREACHABLE` bank as themselves.
- Lesson 91: a negative names its realization, trial space and basis.
- §3d: return `UNDER-RESOURCED` **with a cost**, never a bare `no`.

---

## §1 — METHOD, pre-committed BEFORE any check was run

Everything below §3 is **recomputed or re-fetched**. The disciplines, fixed in advance:

1. **Artefact over prose.** A claim passes only if it falls out of `writeup/data/*.json` bytes, out
   of a re-fetched primary source's bytes, or out of the git object store. A journal sentence
   agreeing with another journal sentence is **not** evidence and is recorded as `PROSE-ONLY`.
2. **Hashes are recomputed, never copied.** Every `md5` / `self_hash` in a wave-4 artefact is
   recomputed by the re-derivation script from the artefact's own quoted bytes. A hash that does not
   reproduce is a **discrepancy**, reported first, regardless of whether the underlying claim is true.
3. **Quotes are anchored in re-fetched bytes.** A verbatim quote passes only if the string is found
   (after whitespace normalisation only) inside the source text fetched **today**. Not found = the
   quote is `NOT-ANCHORED`; source not reachable = `UNREACHABLE`.
4. **Adversarial reading of clauses.** For item (1) I read `arXiv:2509.25116` myself and ask each
   clause independently, and I check specifically whether **blow-up / singularity** was silently
   imported into leg 174's criterion — neither clause mentions it. Leg 174's definition is read from
   `writeup/PUB_0C_CENSUS_SPINE.md` §1 at its committed bytes, not from `V3`'s restatement of it.
5. **Item (3) is graded on the logic, not on the citation count.** The question is not "did `L2'`
   cite ESS" but "does `alpha <= 1` FOLLOW from what the primaries actually state". I will (i) try
   ESS at primary, (ii) if unreachable say so and name exactly what the record then rests on, and
   (iii) grade the implication chain step by step, allowing myself to conclude the record
   **overstates** a secondary's paraphrase if that is what the bytes show.
6. **No repairs.** No file belonging to `V3` or `L2'` is edited. Territory is exactly
   `experiments/journal/verify_wave4.md`, `experiments/verify_wave4_rederive.py`,
   `writeup/data/p2_verify_wave4_v1.json`.

---

## §2 — PER-ITEM VERDICT VOCABULARY, fixed in advance

Per gate item exactly one of:

- `REPRODUCES` — the claim falls out of artefact / primary bytes exactly as recorded.
- `DISCREPANCY` — it does not, with the delta quantified and the location named. Reported FIRST.
- `UNVERIFIABLE` — the check cannot be decided from reachable evidence, with the reason.

Sub-verdicts on rows: `ANCHORED` / `NOT-ANCHORED` / `UNREACHABLE` / `PROSE-ONLY`.
Hash rows: `HASH-MATCH` / `HASH-MISMATCH`.

**Pre-committed:** a `DISCREPANCY` on any of (1)-(5) is a real finding and lands unsoftened; a clean
`REPRODUCES` on all five is a PASS and also a real result. **Neither moves a Clay link.**

---

## §3 — WHAT WOULD FALSIFY EACH ITEM (written before looking)

- **(1)** Falsified if `2509.25116` is inviscid, or if its certificate encloses a solution of an
  equation from which the dissipative term has been removed / approximated away, or if the object IS
  a finite-time singularity of the equation carrying dissipation, or if `V3` imported a blow-up
  clause leg 174 does not contain.
- **(2)** Falsified if any of the 8 `NO` rows' quoted failing clause is not in the paper, or the
  quote is real but does not entail the failure recorded.
- **(3)** Falsified if `alpha <= 1` does **not** follow from the primaries — e.g. if ESS's hypothesis
  is strictly stronger than what the DSS profile supplies, if the secondaries' restatement adds a
  hypothesis, or if the chain needs a step nobody in the record has.
- **(4)** Falsified if any `FAILS-BY-CONSTRUCTION` technique in fact could apply on its quoted
  hypothesis, or if the single `SATISFIED` row does not satisfy what it is said to.
- **(5)** Falsified if the bill numbers or `self_hash` do not recompute.

**Committed before any checking. Everything after this line is measurement.**
