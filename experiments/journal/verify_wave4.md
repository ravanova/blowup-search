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

---

## §4 — ITEM (1): `V3`'s YES on `arXiv:2509.25116`. **VERDICT: REPRODUCES.**

**Source re-fetched today (2026-08-18), not read from any journal.**
`https://arxiv.org/pdf/2509.25116v2` -> 2,148,337 B PDF,
`sha256 2d369eade29bd0d5e8dfc6d7def7ed19b8282ab4450860978f3691176d9f8318`,
`pdftotext -layout` -> 315,767 B. Stamp on p.1: `arXiv:2509.25116v2 [math.AP] 19 Mar 2026`, dated
"March 20, 2026". `V3` recorded "v2, 19 Mar 2026" — **matches**. The abstract page carries **no
`journal-ref`**: this is an unrefereed preprint (see §4.4).

### §4.1 — The criterion, read at its own committed bytes (not at `V3`'s restatement)

`writeup/PUB_0C_CENSUS_SPINE.md` §1, read from disk:

> * **Grade A** — the interval-arithmetic certificate encloses a solution of an equation that
>   itself carries the dissipative term (clause (c) below).
> * **fluid** — the equation is a genuine fluid-dynamics equation (transport nonlinearity,
>   incompressibility or a fluid-adjacent structure), not an off-axis scalar/complex-field model.

`V3`'s `criterion.grade_A` and `criterion.fluid` are **character-identical** to these two strings
modulo the dropped parenthetical "(clause (c) below)". **Exactly two clauses. Neither mentions
blow-up or a finite-time singularity.** `V3` did **NOT** silently import one: its `criterion_note`
records `concludes_pde_singularity` as a *separate observable* and explicitly refuses to fold it in.
**No tightening. CLEAN.**

### §4.2 — Clause 1 (dissipative term inside the certified equation): **HOLDS, on my own reading**

The certified system is (1.12) (p.4 of the fetched text), which I read myself:

- eq. 1 of (1.12): `- 1/2 U~ - 1/2 xi.grad U~ + Pi(U~.grad U~) - Delta U~ = 0`
- eq. 2 of (1.12): `- 1/2 v~ - 1/2 xi.grad v~ + Pi(U~.grad v~ + v~.grad U~) - Delta v~ = lambda~ v~, lambda~ < 0`
- `div U~ = 0`, `div v~ = 0`

`V3`'s `equation_certified` transcription of both displays is **correct term-for-term**.

Proposition 1 (Exact self-similar profile), eq. (1.15), p.5, fetched verbatim:
`-1/2 Ubar - 1/2 xi.grad Ubar - Delta Ubar + Pi(...) = -Pi E_U, div Ubar = 0` (the overbars are lost
by `pdftotext`; the three Pi-terms are exactly the expansion
`Pi(U.grad Ubar + Ubar.grad U + Ubar.grad Ubar)` that `V3` records), "so that `U~ = U + Ubar`" solves
the first and third equations of (1.12), with `||Ubar||_{L2} <~ eps_U`.
**The Laplacian is a term of the very equation the enclosure solves.** Clause 1 **HOLDS**.

**Interval arithmetic is the enclosure mechanism** — anchored at 4 independent places in the
re-fetched text: "rigorously verify our numerical computations using interval arithmetic in Section
7" (Sec. 1.5 outline); "will need to be verified rigorously by interval arithmetic" (Sec. 1.6);
Sec. 7.3 "All pointwise evaluations fi,j are computed with interval arithmetic to enclose
round-off"; Sec. 7.4 "with interval arithmetic capturing floating-point uncertainty". The Sec. 7
opening at p.53 anchors verbatim as `V3` quotes it. The enclosure itself closes by a **Schauder
fixed-point** argument on a coercive + compact + finite-rank decomposition — **not** a
radii-polynomial contraction. **C1 is not engaged by this row, and C1 is not cited here as evidence
that anything closes.**

### §4.3 — Clause 2 (genuine fluid equation): **HOLDS**

eq. (1.1), p.1: `d_t u + u.grad u - Delta u + grad p = 0, div u = 0, u(t=0,x) = u_in(x)`, introduced
as "the three-dimensional incompressible Navier-Stokes equation on the whole space without forcing"
(**ANCHORED**, strict). Transport nonlinearity **and** incompressibility, both carried into the
certified profile system (1.12) through the Leray projection Pi. Clause 2 **HOLDS**.

### §4.4 — Is the object NOT a finite-time singularity? **CORRECT, as `V3` reports**

The decisive sentence anchors **strict** in the re-fetched bytes, Sec. 1.2, p.2, immediately after
(1.5): "The readers should not confuse this self-similar setting, which starts from singular initial
data, with the backward self-similar setting related to finite-time singularities from smooth
initial data." Theorem 1's conclusion is **nonuniqueness** of Leray-Hopf solutions, and the solutions
are "smooth for positive times" (**ANCHORED**). The singularity is in the *initial data* (scale
invariant, of size `O(|x|^-1)`, then localised), **not** a finite-time blow-up. `V3`'s
`the_qualification_that_must_travel_with_the_yes` is **accurate and not softened**.

**One observation `V3` does not carry, recorded here and NOT ruled.** `PUB_0C_CENSUS_SPINE.md` §1
says the cell "has never been filled by any **published** work". `arXiv:2509.25116v2` carries **no
`journal-ref`** on its abstract page as of today — it is an unrefereed preprint. Whether "published"
in that sentence means "peer-reviewed" or "publicly posted" is a **wording question for the user**,
exactly like the W3 defect `V3` already escalated. **I report it; I do not rule it.** Note the
record already treats preprints as fills elsewhere, so ruling "preprints do not count" would also
unfill other cells of leg 174's matrix.

### §4.5 — ITEM (1) VERDICT

**REPRODUCES.** Both clauses hold on my own reading of the re-fetched primary; the object is not a
finite-time singularity; `V3` did not import a third clause. `V3`'s own honest ceiling is accurate:
neither `V3` nor this verifier audited the certificate itself. **An adversarial full-text audit of
the Hou-Wang-Yang proof to leg-309 depth has still not been done by anyone in this record.**

---

## §5 — ITEM (2): the 8 `NO` rows. **VERDICT: REPRODUCES on every verdict; FOUR VERBATIM-QUOTE DEFECTS.**

All 8 papers re-fetched today. sha256 (first 16) / extracted text size:
`2605.19716v2` 796c5b3389e116e3 / 437,510 B; `2605.15149v1` 7e23d6a38744148d / 443,366 B;
`2604.09949v1` 59c5b623cd19d3ac / 45,883 B; `2305.05660v3` 7fe5f26365166f74 / 712,020 B;
`2208.09445` 0f3970d20aa2f5a5 / 688,725 B; `2404.04054` 8805857c5201196e / 148,131 B;
`2410.05480` d95df28d2d741b42 / 338,417 B; `2509.14185` ade2c449cbbc9314 / 89,681 B.
**Zero `UNREACHABLE`.**

### §5.1 — DEFECTS FIRST (pre-committed reading (b))

**D1 — `R7` / `arXiv:2509.14185`. MISQUOTE in a field labelled `failing_clause_quoted`.**
Banked: *"This level of precision meets **the requirements** for rigorous mathematical validation via
computer-assisted proofs."*
Re-fetched abstract, verbatim: *"This level of precision meets the **stringent** requirements for
rigorous mathematical validation via computer-assisted proofs."*
**The word `stringent` is dropped.** The field is presented as a verbatim quote and is not verbatim.
**Materiality: NIL to the verdict** — the sentence still says the numerics are CAP-*ready*, not that
a CAP was performed, which is the whole of `R7`'s failing clause. `NOT_GRADE_A` stands.

**D2 — `R6` / `arXiv:2208.09445`. ATTRIBUTION DEFECT on `failing_clause_second`.**
The quoted sentence ("Within this range of gamma, there exist self-similar solutions to the Euler
equations for which the dissipation terms for the corresponding self-similar Navier-Stokes problem
can be treated as exponentially decaying forcing...") **is in the paper, verbatim, at the location
given (Sec. 1.1.2, p.4)** — but Sec. 1.1.2 sits under **Sec. 1.1 "Background"**, and the sentence
describes the **prior work [69]** ("Applying stability analysis borrowed from [67], the authors then
use the solutions of [69]..."), **not this paper's own construction**. `V3` uses it as evidence about
what *this* paper certifies. **Materiality: NIL to the verdict**, because `V3`'s *first* failing
clause — Sec. 7 opening, p.54, "...while in the Navier-Stokes case we need to restrict the parameter
r to a regime where the self-similar profile dominates the dissipation" — **is the paper's own voice
and anchors strict**, and I independently confirmed at Theorem 1.3 (p.5) that the NS blow-up is
*asymptotically* self-similar with limiting profiles `(U^E, S^E)` **of Theorem 1.2, which solve the
Euler ODE (1.5)**. The certified object is the inviscid profile. `NOT_GRADE_A` (Grade B) stands.

**D3 (CORRECTED BY ME AT THE SECOND PASS, see SS5.4) - `R5` / `arXiv:2305.05660v3`. ONE CLIPPED
PREFIX, AND ONE CLAIM OF MINE THAT WAS ITSELF WRONG.** Banked by `V3` as introduced verbatim:
*"**linear** partial differential equations that govern the motion of the ideal INVISCID fluid
flow"*. Re-fetched `2305.05660`, Introduction, p.1, character for character:
*"The three dimensional incompressible Euler equations are one of the most fundamental **non-
linear** partial differential equations that govern the motion of **the** ideal inviscid fluid
flow."* So: the `non-` **is** clipped in `V3`'s field (a `pdftotext` line-break hyphenation,
`"non- linear"`, carried into the artefact) - that part of D3 **stands**. But my first-pass claim
that `V3` had **inserted a `the`** before "ideal" is **FALSE**: the paper has that `the`. I withdraw
it, unsoftened. **Materiality: NIL either way** - eq. (1.1) `omega_t + u.grad omega = omega.grad u`
anchors strict and carries no dissipative term. `NOT_GRADE_A` stands.

**D4 — `R3` / `arXiv:2605.15149v1`. MISQUOTE + LOCATION SLIP, in supporting evidence (not the
failing clause).** Banked: *"For **the** rigorous computer-assisted proof, we use interval arithmetic
[41,43] ... in INTLAB"*, located "Appendix B.3 'Interval Arithmetic', p.~68". Paper: *"For rigorous
computer-assisted proof, we use interval arithmetic [41, 43], and use the MATLAB toolbox INTLAB
(version 11 [44]) for the interval computations."* — a `the` inserted, "in INTLAB" is not the paper's
phrasing, and the paragraph headed "Interval Arithmetic." sits at **p.71** (Appendix B opens at p.68;
Sec. B.3 is titled "Rigorous piecewise bounds"). **Materiality: NIL** — this is `R3`'s *supporting*
evidence; its failing clause is eq. (1.1) itself.

**Minor sub-defect:** `R1`'s Sec. 7.3 quote writes `f_{i,j}` (LaTeX) where the paper renders `fi,j`;
`R1`'s Theorem-1 quote writes `R3 x [0,1]` for `R^3 x [0,1]`. Pure transcription. **NIL.**

### §5.2 — the 8 failing clauses, measured

| row | arXiv | failing clause as quoted | anchored today? | verdict holds? |
|---|---|---|---|---|
| R2 | 2605.19716v2 | "In contrast to [11,12], our construction of self-similar profiles is purely analytic and does not rely on any computer-assisted verification." (Remark 1.2, item (4), p.6) | **ANCHORED**, at the stated location, immediately before Theorem 1.3 | **YES** — and it fails twice: eq. (1.1) is Euler, no dissipative term |
| R3 | 2605.15149v1 | eq. (1.1) `d_t omega + 2 psi_alpha d_x omega = -(1-alpha) d_x psi_alpha omega`, a 1D model | **ANCHORED**; and I tested `V3`'s strong side-claim **mechanically**: `viscos*` occurs **0** times, `laplac*` **0** times, `navier` exactly **2** times — one body occurrence (literature survey, "...incompressible Navier-Stokes without forcing [34]") and one bibliography entry, which **is** `arXiv:2509.25116`. `V3`'s claim is **exactly right** | **YES** |
| R4 | 2604.09949v1 | Thm 12.1 (Singular solution recovery), eq. (18) `u(x,t) = (T*-t)^{-1/2} ubar(x/(T*-t)^{1/2})`, Sec. 12 "Blow-up Reconstruction" | **ANCHORED** (the display renders as a stacked fraction; structure identical) | **YES** — it is verbatim the backward-self-similar form excluded by Necas-Ruzicka-Sverak / Tsai. The break is theorem-level, as leg 309 found |
| R5 | 2305.05660v3 | eq. (1.1) `omega_t + u.grad omega = omega.grad u`, "ideal inviscid fluid flow" | **ANCHORED** (see D3 for the prose slip) | **YES** |
| R6 | 2208.09445 | Sec. 7 opening, p.54 (paper's own voice) + Sec. 1.1.2, p.4 (see D2) | **BOTH ANCHORED**; D2 is an attribution defect, not a fabrication | **YES** — Thm 1.3's limit profiles are the Euler ones of Thm 1.2 |
| R7 | 2509.14185 | abstract; CAP-ready, not CAP-done | **ANCHORED** *modulo D1* | **YES** |
| R8 | 2404.04054 | Remark 40, Sec. 6, p.28 | **ANCHORED**; I also confirmed eq. (53)/(54) render as banked (`Lu - u/4 + u^2 d_x u = 0, x >= 0` from `d_t v + v^2 d_x v = d_xx v`) | **YES** — the certified object is a scalar 1D Burgers profile; `(u.grad)u` is "in principle", i.e. NOT done |
| R9 | 2410.05480 | CGL, a complex-field semilinear equation | `V3` did **not** re-read it and says so. **I did**: title and abstract of the re-fetched v2 confirm NLS/CGL — no transport nonlinearity, no incompressibility | **YES** |

### §5.3 — ITEM (2) VERDICT

**REPRODUCES.** All eight `NO` verdicts are correct on their quoted hypotheses; **not one is wrong**.
Four quote defects (D1-D4) are located and sized above - D3 **reduced to one clipped `non-`** by my
own second pass, see SS5.4; **none of them changes any verdict**, and **none of them is repaired
here**. `V3`'s eight `NO`s are, as it says itself, a statement about
**this named list only**; they do not re-establish that nobody else filled the cell.

### §5.4 — SECOND PASS: THE MECHANICAL ITEM-(2) CHECK, AND ONE CORRECTION TO MY OWN D3

`experiments/verify_wave4_rederive.py --only 2` now anchors item (2) **mechanically** rather than by
hand. Three facts about `V3`'s artefact had to be built into it before the automated pass could be
honest, and each is a property of `V3`'s style, **not** a defect:

1. `V3` **transcribes displayed equations into ASCII on purpose** - `"partial_t omega + 2 psi_alpha
   partial_x omega = ..."`, `"i u_t + (1 - i eps) Laplacian(u) + ..."`, `"(u . grad)u"`, `"H^2(mu)"`.
   These can never anchor against `pdftotext` output and it is **not a misquote** that they do not.
   They are reported as **`TRANSCRIPTION`** (17 fields), never as discrepancies.
2. `equation_certified` is a **description field in `V3`'s own voice** (`"NOTHING IS CERTIFIED BY
   INTERVAL ARITHMETIC. The object constructed is..."`). Anchoring `V3`'s framing against the paper
   would **manufacture** defects. Reported as **`DESCRIPTION`** (12 fields).
3. `V3`'s `*_evidence` and `*_location` fields are `V3`'s framing **with the paper's words set inside
   single quotes**. Only the **embedded spans** are quotations, and only those are checked.

Within each quotation the script anchors the **longest run of plain prose** (>= 8 ordinary words, no
ASCII-ised Greek), which is where a dropped or altered word actually shows.

**Result of the mechanical pass: exactly two rows carry a verbatim defect, and both are already
written up above** - `R7 failing_clause_quoted` (**D1**, dropped `stringent`) and `R3
interval_arithmetic_evidence` (**D4**, inserted `the`). **Zero `UNREACHABLE`.** `D2` is an
attribution defect (the sentence *is* verbatim) and no mechanical check can catch it; it stands.

**AND ONE FINDING AGAINST MYSELF.** The mechanical pass anchored `R5`'s `failing_clause_location`
span **strict** - which my first-pass hand reading had called a misquote. Re-read of the re-fetched
bytes (`2305.05660`, Introduction, p.1) shows the paper **does** write *"govern the motion of **the**
ideal inviscid fluid flow"*. **My D3 claim that `V3` inserted a `the` was WRONG and is withdrawn.**
D3 now reduces to the clipped `non-` prefix alone, itself a `pdftotext` line-break artefact
(`"non- linear"`). Reading (b) - *any discrepancy is reported first and is not softened* - **applies
to my own errors as well as to `V3`'s**, so it is recorded here rather than quietly deleted.

---

## §6 — ITEM (3): `L2'`'s PIN AT alpha = 1

The gate: *"re-fetch `1610.09464` and `2607.09619`, verify the decisive quotes by anchor
and hash, and answer the question the Conductor flagged as this result's LOAD-BEARING
CEILING — THE 'AT MOST 1' DIRECTION RESTS ON ESCAURIAZA-SEREGIN-SVERAK, WHICH WAS NOT
READ AT PRIMARY AND REACHES THE RECORD ONLY THROUGH TWO SECONDARIES. DOES THE DIRECTION
ACTUALLY FOLLOW?"*

### §6.1 — hashes, re-fetched today

| file | banked md5 | recomputed md5 | |
|---|---|---|---|
| `1610.09464.pdf` | `f1d14db17f643323cfa1a16ba661eb9d` | `f1d14db17f643323cfa1a16ba661eb9d` | **MATCH** |
| `1610.09464.txt` | `73279aa90ce78c1190d0027000fd1cf2` | `73279aa90ce78c1190d0027000fd1cf2` | **MATCH** |
| `2607.09619.pdf` | `53680cb802803dda9b0a27975c7d1270` | `53680cb802803dda9b0a27975c7d1270` | **MATCH** |
| `2607.09619.txt` | `01bdf4c836b3a8b6ddfa071618335ef2` | `01bdf4c836b3a8b6ddfa071618335ef2` | **MATCH** |

sha256 of the two PDFs as fetched today:
`1f537bc2b6b2e7752db275a1eb1c903782068510c4d7bcd68dbdd45d14c0efdc` (Chae-Wolf) and
`379591aa3c1036c9140702ebe71aaab309fe207439a57db5ceff893f15d0ae8e` (Pineau-Vicol).

All three decisive quotes anchor **strict** (no token-level fallback needed), including
Chae-Wolf's own typo *"For **evrey** C∗ > 0"* preserved unaltered in the artefact —
evidence that the transcription is mechanical, not retyped.

### §6.2 — the strongest single reproduction in this unit

`L2'` carries its own generator, `experiments/p2_route_l2_v1_evidence.py`, which extracts
every quote mechanically by a (start-anchor, end-anchor) pair. I re-ran that generator
**against the twelve source texts I fetched and converted myself today**, with `PAPERS`
and `OUT` redirected out of the repository so nothing of `L2'`'s was written:

```
banked self_hash fd5c410859eb764b   re-run self_hash fd5c410859eb764b
payload bit-identical: True
```

`writeup/data/p2_route_l2_decay_v1.json` **regenerates bit-for-bit from primaries
re-fetched today.** All 18 rows: `chars` MATCH, `sha256_12` MATCH, quote **ANCHORED
(strict)**, zero `UNREACHABLE`, zero `NOT-ANCHORED`. `verdict_counts` recompute to
`{FAILS: 9, FAILS-BY-CONSTRUCTION: 8, SATISFIED: 1}`.

### §6.3 — ESS at primary: **UNREACHABLE**

Both relevant Escauriaza-Seregin-Šverák papers are journal-only:

* ESS, *Backward uniqueness for parabolic equations*, **Arch. Ration. Mech. Anal. 169
  (2003) 147-157**;
* ESS, *L_{3,∞}-solutions of the Navier-Stokes equations and backward uniqueness*,
  **Russian Math. Surveys 58 (2003) no. 2, 211-250**.

`au:"Escauriaza"` on the arXiv API returns **25** entries; **neither paper is among
them** (instrumented, `http 200`, not a throttle). No S2 key exists here and
**READ, DO NOT CONTACT** binds. **ESS banks as `UNREACHABLE`, never as a zero.**

### §6.4 — DISCREPANCY D5: the two secondaries cite **two different ESS papers**, and
Chae-Wolf's is the one that contains **no Navier-Stokes regularity theorem**

Read at its own committed bytes, Chae-Wolf Remark 1.2 says

> If u ∈ C((−∞, 0); L3(R3)), and discretely self-similar, then u ∈ L∞(−∞, 0; L3(R3)).
> Thus, in case p = 3, **by using the result in [5]**, we get the full regularity u in Q.

and Chae-Wolf's bibliography entry **[5]** is, verbatim:

> [5] L. Escauriaza, G. Sergin, and V. Šverák. **Backward uniqueness for parabolic
> equations**, Arch. Ration. Mech. Anal., 169, pp. 147–157, 2003.

That is the **backward-uniqueness lemma for parabolic operators**. It states no
Navier-Stokes regularity criterion at all. The paper that does is the *Russian Math.
Surveys* one, which **Pineau-Vicol cite as [23]** — verbatim from `2607.09619`:

> [23] L. Escauriaza, G. Seregin, V. Šverák. **L3,∞-solutions of the Navier-Stokes
> equations and backward uniqueness**. Russian Math. Surveys 58 (2):211–250, 2003.

**On its face, the citation carrying `L2'`'s load-bearing row `T2c` points at a paper
that cannot deliver the conclusion drawn from it.** The load therefore transfers to the
row `L2'` describes as the *second, independent* statement. Recorded; **not repaired**.
(The `T2c` row's own `name` field says "via Escauriaza-Seregin-Sverak **backward
uniqueness**", which matches Chae-Wolf's [5] exactly; the artefact names no ESS paper in
`citation`, so the artefact itself neither states nor mis-states which one. The gate's
own gloss — *"it is the L^{3,infty} / L^3 regularity criterion result"* — names the
**other** paper.)

### §6.5 — DISCREPANCY D6: `the_pin`'s word "independently" overstates what Pineau-Vicol say

`honest_ceiling.the_pin` reads *"AT MOST 1 by Chae-Wolf Remark 1.2 +
Escauriaza-Seregin-Sverak, **restated independently** by Pineau-Vicol (2026) Sec. 1.2."*
Pineau-Vicol §1.2 at primary, in full:

> Why is Conjecture 1.1 open for α ̸= 0? Assumption (1.9) only implies that the profile U
> belongs to the weak-L3 class L3,∞(R3). Had we assumed that the profile decays a little
> bit faster, to ensure that U ∈ L3(R3), then we would have u ∈ L∞([−1, 0); L3(R3)), and
> by the theory of Escauriaza, Seregin, and Šverák [23] this would imply regularity (and
> hence the triviality of U). **This argument applies to rotated self-similar solutions**
> since (1.7) implies that ∥u(·, t)∥L3 = ∥U∥L3 for all t < 0 and α ∈ R.

Two things follow, and neither is in the record:

1. **The class is different.** Pineau-Vicol state it for **rotated globally self-similar
   (RSS)** solutions, *not* for discretely self-similar ones. Route 4's object is DSS at
   a fixed λ ≫ 1. For the **actual object** the implication is stated at primary by
   **Chae-Wolf Remark 1.2 alone**. The extension of PV's sentence to DSS is immediate —
   `‖u(·,t)‖_{L³} = ‖U(·,s)‖_{L³}` is periodic in `s` hence bounded — but that step is
   **mine, not PV's**, and it is not in PV's bytes.
2. **The two are not independent.** Both terminate at ESS. They are independent
   *authors*, not an independent *proof*. Only one of them names the ESS paper that
   contains a Navier-Stokes regularity theorem (D5).

Recorded; **not repaired**.

### §6.6 — the substantive question, measured

Neither Chae-Wolf's one-sentence Remark 1.2 nor Pineau-Vicol's one-sentence §1.2 states
the hypotheses of the ESS theorem being invoked. The classical global ESS statement is
for **Leray-Hopf** solutions — finite energy. Route 4's object is not one:
`experiments/verify_wave4_rederive.py` computes, at the banked α = 1,

```
int_{|y|<1e2} |U|^2 = 1153.09      int_{|y|<1e6} |U|^2 = 1.2566e+07
int_{|y|<1e4} |U|^2 = 125445       int_{|y|<1e8} |U|^2 = 1.25664e+09
```

i.e. `∫_{R³}|u(·,t)|² dx = ∞`, growing linearly in the cutoff radius. **The object is not
a Leray-Hopf solution and the global form of ESS does not apply to it.** That is the real
load-bearing objection, and it is not addressed anywhere in the record.

It does **not** sink the direction. Seregin — an ESS author — states the same result in a
**purely local, suitable-weak-solution** form in a source that **is** reachable at
primary (arXiv:`math/0510396`, *"Navier-Stokes equations: almost L3,∞-case"*, fetched
today, `pdftotext` 688 lines). Its §1 defines `v, p` on `Q_T = Ω×]0,T[` for **any**
`Ω ⊂ R³` by the three conditions

> v ∈ L2,∞(QT) ∩ W21,0(QT), p ∈ L3/2(QT);  … the Navier-Stokes equations … in the sense of
> distributions;  … the local energy inequality …

and calls that pair *"a suitable weak solution to the Navier-Stokes equations in QT"*.
Its §1 then records, of the condition `v ∈ L3,∞(QT)` (Russian convention:
`L_{s,l}(Q_T) = L_l(0,T;L_s(Ω))`, i.e. **`L^∞_t L^3_x`** — confirmed by its own ref [6],
Neustupa, *"in the class L∞(0,T;L3(Ω)³)"*):

> Later, in [12], [2], it was proved that (1.5) implies regularity of v in QT and thus
> NT = 0.

with **[2] = ESS, Russian Math. Surveys 58 (2003) 211-250** — i.e. exactly Pineau-Vicol's
[23]. **No finite-energy and no Leray-Hopf hypothesis anywhere.** Seregin's own Theorem
1.1 is weaker still, needing only `m_T = liminf_{t↑T} (1/(T−t)) ∫_t^T ∫_Ω |v|³ < ∞`, and
its proof reduces by scaling to the unit cylinder `B×]−1,0[`.

The object supplies those local hypotheses. Re-derived numerically on `B_1 × (−1,0)` from
the Type-I bound `|u| ≤ C/(√(−t)+|x|)`:

```
sup_t int_{B_1} |u|^2 dx            ~ 1.42887   < inf   (L_{2,inf})
int_{-1}^{0} int_{B_1} |grad u|^2   ~ 6.28e+05  < inf   (W^{1,0}_2)
```

and `u` is `C^∞(Q)` by hypothesis, so the local energy inequality holds with **equality**.
And the criterion separates the two cases exactly where the pin sits:

```
alpha = 1.0 : m_T = +infinity   (int_{B_1}|u|^3 = 57.99, 115.7, 231.5, 463.0
                                 at |s| = 1e-4, 1e-8, 1e-16, 1e-32 — log-divergent)
alpha > 1   : m_T = ||U||^3_{L^3} < infinity, s-independent
```

so at α > 1 the criterion **applies**, `(0,0)` is a regular point, and DSS scaling
`u(λ^{−k}y, λ^{−2k}s) = λ^k u(y,s)` with `|u| ≤ M` near the origin forces `λ^k|u(y,s)| ≤ M`
for every `k`, hence `u ≡ 0`. At α = 1 exactly it **does not apply** — by a logarithm.
That is precisely why the case is open, and it is the sharpest available statement of
*why*.

### §6.7 — ITEM (3) VERDICT

**REPRODUCES**, with **TWO DISCREPANCIES (D5, D6)** and **ONE UNREACHABLE (ESS itself)**.
The pin at α = 1 stands: α ≥ 1 from Chae-Wolf Thm 1.1 (`T2a`, `SATISFIED`, quote anchored)
and α ≤ 1 for any nontrivial profile. The direction **DOES follow** — but through the
**local suitable-weak-solution** form of the ESS result, not the global Leray-Hopf form
that the phrase "by Escauriaza-Seregin-Šverák" invites, and the record nowhere says so.
The record did **not** overstate a secondary's paraphrase: both secondaries say what the
record says they say, character for character. What the record understates is **how much
is being taken on trust** in two unproved one-sentence remarks whose stated hypotheses the
object provably fails in the global reading.

---

## §7 — ITEM (4): the 18 adjudications, all 8 `FAILS-BY-CONSTRUCTION` and the 1 `SATISFIED`

Every row's `decisive_hypothesis_quote` re-anchors **strict** in the source re-fetched
today, with `chars` and `sha256_12` MATCH (§6.2). What follows is whether the **verdict**
is right **on the quoted hypothesis**.

| row | technique | decisive hypothesis as quoted | object | verdict right? |
|---|---|---|---|---|
| `T2a` | Chae-Wolf Thm 1.1 | `u ∈ C((−∞,0);L^p)`, `3 ≤ p < ∞` | met: at α = 1, `U ∈ L^p` for every `p > 3`, and `∫r^{−p}r²dr` converges iff `p > 3` | **YES**, `SATISFIED` |
| `T1b` | Tsai 1998 | backward **globally** self-similar | object is DSS at one fixed λ | **YES**, by construction |
| `T3a` | Bradshaw-Phelps | **forward** self-similarity | object is backward | **YES**, by construction |
| `T3b` | Jia-Šverák Thm 1.1 | `(−1)`-homogeneous data, **forward** Cauchy problem | object is backward, no data | **YES**, by construction |
| `T4a` | Elgindi | **Euler**, `C^{1,α}` | object is Navier-Stokes, `C^∞` (Clay cond. (6)) | **YES**, by construction |
| `T4c` | Chen-Hou §8.6 | Boussinesq/Euler **with boundary**, `C^{1,α}`, smallness from α | object is NS on `R³`, fixed viscosity, no such parameter | **YES**, by construction |
| `T5` | MRRS | **finite speed of propagation** | NS is parabolic with nonlocal pressure — and MRRS's own quoted sentence says *"This procedure cannot be applied in the Navier-Stokes case"* | **YES**, by construction |
| `T6` | Giga-Kohn | a scalar obeying a **maximum principle** | NS velocity has none; the Bernoulli head-pressure Π obeys an **elliptic** inequality only in the exactly-SS class, and the object's profile is `s`-periodic with period `2 log λ = 1.0612565021243408` | **YES**, by construction |
| `T10` | Luong-Ramsey-Bertozzi-Baty | **1D compressible Euler**, closed-form profile | object is 3D incompressible NS | **YES**, by construction |

**Not one verdict is wrong on its quoted hypothesis.** Three observations, none of which
changes a verdict, none repaired here:

* **O1 (`T1b`).** The field is `decisive_hypothesis_quote` and the decisive hypothesis is
  *"backward **globally** self-similar"*, but the 144-character quote is about `L^p`
  profiles and local energy estimates — the SS clause is supplied by the surrounding
  Pineau-Vicol section title ("Backwards self-similar solutions"), not by the quoted
  bytes. The quote does not, on its own, carry the hypothesis the row turns on.
* **O2 (`T6`).** The row is labelled *Giga-Kohn* but quotes **no Giga-Kohn text at all** —
  it quotes Pineau-Vicol on the Navier-Stokes analogue. The artefact declares this
  honestly in `location` ("for the Navier-Stokes analogue of the structural hypothesis
  and where it breaks"); it is still a row whose named source is never quoted.
* **O3 (`T1a` / `T6`).** `T1a`'s 99-character quote is a **strict prefix** of `T6`'s
  492-character quote — the same Pineau-Vicol sentence. Two rows, one piece of text.
  They are not two pieces of evidence.

**ITEM (4) VERDICT: REPRODUCES.** All 8 `FAILS-BY-CONSTRUCTION` and the 1 `SATISFIED` are
correct on the quoted hypothesis.

---

## §8 — ITEM (5): `L2'`'s bill against `p2_route_cloc_v1.json`

`cloc`'s `self_hash` recomputes from its own payload by its own stated recipe
(`sha256(json.dumps(payload, indent=2, sort_keys=False))[:16]`):
**`58c57b62c0cbc80d` stored, `58c57b62c0cbc80d` recomputed — MATCH.** `L2'`'s
`source_self_hash` equals it. Re-running `experiments/p2_route_cloc_v1.py` with `OUT`
redirected out of the repository regenerates the whole leg-381 artefact **bit-identically**
(`SELF-TESTS: ALL PASS`, payload identical `True`).

`L2'`'s own `self_hash` recomputes by its generator's recipe
(`sha256(json.dumps(art, sort_keys=True, ensure_ascii=False))[:16]`):
**`fd5c410859eb764b` stored, `fd5c410859eb764b` recomputed — MATCH.**

Field by field, `L2'`'s bill against `cloc`'s own numbers — every one **MATCH**:

```
L2_threshold_alpha                             1.5                     MATCH
L3_threshold_alpha                             1.0                     MATCH
banked_type_I_alpha                            1.0                     MATCH
deficit_to_L2_in_exponent                      0.5                     MATCH
required_over_available_exponent_ratio         1.5                     MATCH
critical_L3_tail_cubed_increment_per_decade    326.87521405120924      MATCH (= increment_per_decade[0])
critical_L3_tail_cubed_increment_spread        7.393926228758692e-10   MATCH (= RELATIVE spread, re-derived)
tail_L3_norm_2_decades                         8.678998071314405       MATCH
tail_L3_norm_10_decades                        14.840907203374448      MATCH
bogovskii_corrector_L2_rho_exponent_at_alpha_1 0.5004159707002005      MATCH
tail_L3_norm_rho_exponent_at_alpha_1           1.2768224253058113e-05  MATCH
```

Independently re-derived, not copied: `L^p` needs `p·α − 2 > 1`, so the `L²` threshold is
`α > 3/2` and the `L³` threshold is `α > 1` — both MATCH; deficit `1.5 − 1.0 = 0.5`;
overshoot `1.5 − 1.0 = 0.5`, so **any α paying the `L²` bill lands strictly inside `L³`** —
which is exactly what §6 measures to be fatal. The banked "spread" is a **relative**
spread, `(max − min)/mean = 7.393926e-10`; re-derived, MATCH.

**NOTE N1 (not a discrepancy).** `critical_L3_tail_cubed_increment_per_decade = 326.875`
is **not scale-free**: it carries leg 381's field amplitude. A unit-amplitude model
`|U| ≤ (1+|y|)^{−1}` gives `4π ln 10 = 28.935` per decade — a factor `11.30`. What is
load-bearing — a **constant** increment per decade, i.e. **logarithmic divergence** of the
critical `L³` tail at α = 1 — reproduces independently. The absolute number does not
travel outside leg 381's model and should not be quoted as if it did.

**ITEM (5) VERDICT: REPRODUCES.**

---

## §9 — the executable re-derivation

`experiments/verify_wave4_rederive.py` (lesson 68, reading (f)). Run:

```
.venv/bin/python experiments/verify_wave4_rederive.py --cache <dir> [--offline] [--only 1,2,3,5]
```

It writes nothing belonging to `V3` or `L2'`: both generators are copied to a temporary
directory with `OUT` redirected before being run. Missing sources bank as `UNREACHABLE`,
never as zeros. It exits non-zero if any check disagrees with the banked record.
Items (3), (4), (5) exit **0** with `DISCREPANCIES: none` — the discrepancies this unit
reports (D1-D6, O1-O3, N1) are **editorial and attributional**, located by reading, and
are recorded here rather than encoded as machine assertions, because none of them changes
a number or a verdict.

## §10 — CEILING

**TIER 2.** **NO LINK OF THE `L1`→`L4` CHAIN MOVED.** A verification builds nothing,
certifies nothing and realises no profile; even a clean PASS is not movement toward Clay.
Clay stays **~0.05%**. Scale is not evidence and Tier 2 is never a proof. C1 (the
l¹-Fourier / radii-polynomial apparatus ban) binds throughout, was not lifted, narrowed,
re-read or argued against, and is **not** cited anywhere in this unit as evidence that any
apparatus closes. Nothing here was contacted; ESS banks `UNREACHABLE`.
