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

**D3 — `R5` / `arXiv:2305.05660v3`. MISQUOTE.** Banked as introduced verbatim: *"**linear** partial
differential equations that govern the motion of **the** ideal INVISCID fluid flow"*. Paper, p.1:
*"one of the most fundamental **non-linear** partial differential equations that govern the motion of
ideal inviscid fluid flow."* The `non-` was clipped (a `pdftotext` hyphenation artefact carried into
the artefact) and a `the` inserted. **Materiality: NIL** — eq. (1.1)
`omega_t + u.grad omega = omega.grad u` anchors and carries no dissipative term. `NOT_GRADE_A` stands.

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
Four verbatim-quote defects (D1-D4) are located and sized above; **none of them changes any verdict**,
and **none of them is repaired here**. `V3`'s eight `NO`s are, as it says itself, a statement about
**this named list only**; they do not re-establish that nobody else filled the cell.
