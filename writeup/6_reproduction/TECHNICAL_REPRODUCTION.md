# Arc 6, second pass — Reproduction: reading all of it, re-deriving the spine, instantiating it, measuring the Lean

**Technical note. The conductor pass of arc 6 (§3g), legs 423–434.**

| | |
|---|---|
| **Dates** | 2026-09-09 → 2026-09-10 |
| **Mode** | `ORCHESTRATION.md` **§3g CONDUCTOR**, wave sizing **5 by user ruling** (recorded beside §3g's own reason for 2–4; `CORRECTIONS.md` §67). Four waves, one adversarial verifier per fan-out wave, one file per agent, cherry-picked unedited |
| **Legs** | 423–434 (`R0` 423/427 · `R1` 424 · `R2` 425 + wave 1 (428) · `R3` 426 · `R4` wave 2 (429) · `R5`(i) 430 · `R6` wave 3 (431) · `R5`(ii) 432 · `R5`(iii)–(vii) wave 4 (433) · `R7` 434) |
| **Curated data** | `writeup/data/arc6/` — `extract_manifest.json`, `ledger.json`, `ledger/merged.json` (+ five shards), `dag.json`, `spine/merged.json` (+ five agents), `lean/merged.json` (+ five agents), `wave4/merged.json` (+ five agents); `writeup/data/arc6_profile_v1.json`, `arc6_residual_v1.json` |
| **Evidence** | [`reproduction_evidence.py`](reproduction_evidence.py) — rebuilds every number in this note from the banked artefacts, runs each leg's own evidence script, exits nonzero on drift; figures `fig113`, `fig114` from `build_figures.py` |
| **Narrative companion** | [`BLOG_REPRODUCTION.md`](BLOG_REPRODUCTION.md) |
| **Verification** | **Every Conductor-written answer is `UNVERIFIED`.** `VERIFIED` is used exactly where a blind agent that never saw the construction reproduced it: **ten spine nodes** (leg 429). Everything else — including every number the Conductor measured alone (`R5`(i), `R5`(ii)) — is one author's |
| **Clay movement** | **NONE.** No `L1 → L4` link moved. Clay stays ~0.05%. **Tier 2 is never a proof.** |

---

## 0. What the second pass was asked, and the one paragraph it answers with

The first pass (legs 417–422, `../6_adjudicated/`) read §§1–3 and §10 of the OpenAI manuscript
*Finite Time Blowup for Navier–Stokes* (166 pp., `sha256 0e779481…`), censused the Lean at source,
and asked our own wall `W4` whether the mechanism moves it (it does not, `CORRECTIONS.md` §65). The
second pass was chartered to **reproduce**: read all 166 pages, re-derive the spine, instantiate the
construction in this repository's own machinery, and measure the Lean rather than assume it.

**The verdict, in one paragraph (the charter's `R7`):** *Read twice — once solo and once by five
blind shards — all 79 numbered statements index, cite and close as the manuscript says, with one
citation-discipline finding (Propositions 9.5 and 9.6 are never cited downstream). Re-derived by
four agents and checked blind by a fifth, the 58-statement spine holds step by step — 480 steps,
301 recomputed constants, no `GAP`, ten nodes `VERIFIED`. Instantiated from the paper's own
Appendix A schedule, Lemma 4.8's outer profile reproduces its bracket constants, exponents, pressure
datum and pulse-end moment cancellation, and its terminal-tail stress reproduces Proposition A.10
by two independent routes to `10⁻⁹`; its closure and its cone do **not** reproduce at any `λ` a grid
can reach, because the paper's own asymptotics place them at `λ ≲ 3·10⁻⁴` with `√λ P_* ≪ 1`, and its
outer-edge powers are the limit on a collar `δ ≲ 10⁻⁶⁹`. Measured rather than assumed, the Lean
project is large and `sorry`-free outside its challenge placeholders, source-covers all 79
statements, and exports Fefferman's (C) and (D) — a statement strictly weaker than Theorem 1.1 — and
**no kernel check of it was reached** here. Nothing this pass measured contradicts the manuscript;
nothing this pass measured is a proof of it, and no wall of ours moved.*

The sections below carry the numbers, unit by unit, and stop there.

---

## 1. `R0` — the charter corrected before anything ran (legs 423, 427)

**`A6-D` is dead** (`CORRECTIONS.md` §66): arc 5's charter called statement (D) *"the nearest unclaimed
Fefferman statement"*; Theorem 1.1's last sentence claims it through Corollary 10.6. Struck in three
artefacts, nothing rewritten. The conductor charter arrived mid-flight and was applied **forward**
(§67): landed units were not redone, `R2` was re-read by five fresh shards instead, and the wave-sizing
ruling (4 → 5) was recorded beside §3g's own reason for the 2–4 cap before the first dispatch.

## 2. `R1` — the extraction, checked against the PDF's text layer (leg 424)

Gate answer **`NO-AND-HERE-IS-THE-DIFF`** strictly, **`MATCH`** after six named typographic rules
(ligatures, hyphenation, fraction layout, superscripts, the two-column preamble, page furniture).
**79 numbered statements** indexed with page and kind (`writeup/data/arc6/statement_index.json`);
two overrides named. The manuscript text is banked page by page (`manuscript_pages.txt`, 166
`<<<PAGE n>>>` blocks) and every later unit quotes from it, never from memory.

## 3. `R2` — all 166 pages, read twice (legs 425, 428)

**Solo (leg 425):** (a) `YES` — 79 of 79 statements carry hypotheses, conclusion, constants and
citations in `ledger.json`; (b) `YES` — the two Definitions (3.2, 3.3) carry no constants and say so;
(c) **13 hard-page notes**, hardest pp. 107–111 (the correction cycle's bookkeeping), 74–77 (the
oscillatory ansatz), 129–137 (Appendix A's schedule). 196 statement-to-statement edges, 304 equation
labels, 696 citations, 158 hypotheses, 270 constants.

**Five blind shards (wave 1, leg 428):** shards A–E re-read the same pages without the solo ledger;
merged by page-range ownership with three named overrides. (a) 79; (b) `YES`; (c) **33 hard-page
notes**; (d) mean Jaccard against the solo ledger **0.744** (hypotheses) / **0.791** (conclusions),
**every inconsistency is citation breadth, none is about content**. **29 could-not-determine items**:
15 extraction artefacts (fraction layouts lost in the text layer; (4.13) adjudicated at the PDF's
geometry — the fraction bar spans `x = 202–261`, the `−2L` at `x = 179` is outside it), 12
out-of-shard cross-references, 1 reading, **1 about the paper** (Proposition 7.2's exponents are
asserted to exist, not displayed).

## 4. `R3` — the citation graph and the spine (leg 426)

Pre-registered (`15fc747`) before the graph existed: five edge rules, a 38-node judgment spine, eight
numeric expectations. **Acyclic `YES`** on all three passes (ledger citations; proof-block text;
displayed-equation labels resolved to their owners). **Complete `NO-AND-HERE-ARE-THE-DANGLING-NODES`:**
`Remark B.9`/(B.40); 134 labels that live in unnumbered prose; and **Propositions 9.5 and 9.6 —
stage 0 and the inductive step of the correction cycle — are never cited by any statement downstream
of them**, by name or by an equation they display (named only in the outline, the notation table and
section introductions). Closures of Theorem 1.1: 56 / 51 / 70 statements by the three passes; longest
chains 22 / 14 / 27. **§7 is unreachable by statement citation and reached by equation label**
(through Definition 9.4 → Proposition 9.3). Pre-registered expectations met **4 / 2 / 5 of 8**
(`CORRECTIONS.md` §68). The `R4` spine is the union: **58 nodes**.

## 5. `R4` — the spine re-derived by four agents and checked blind by a fifth (wave 2, leg 429)

| | `CHECKED` | `GAP` | `NOT-CHECKED` |
|---|---|---|---|
| agents 1–4 (15 + 12 + 10 + 21 nodes) | **58** | **0** | **0** |
| verifier, ten nodes drawn with seed 428, never shown the four files | 10 | 0 | 0 |

**Agreement 10 of 10 → ten nodes `VERIFIED`** (`Lemma 4.4`, `Proposition 4.10`, `Lemma 6.3`,
`Lemma 8.8`, `Proposition 9.1`, `Lemma 9.8`, `Proposition 9.9`, `Lemma B.7`, `Proposition B.8`,
`Proposition C.3`); 48 `UNVERIFIED`. 480 reproduced steps, 301 recomputed constants, 53 extraction
artefacts resolved at the PDF (Lemma 10.5's cutoffs are the powers `φ_R⁸` etc.). **Proposition 9.6's
smallest closing margin is 0.07.** The pre-committed expectation "≥ 3 `GAP`s" was **refuted**. Eight
nodes are `CHECKED` with stated limits (listed in `leg_429.md`). **Not a proof of the theorem** — 58
reproduced arguments, ten of them twice, is a consistency check on the manuscript's spine.

## 6. `R5`(i) — Lemma 4.8's outer profile, built from the paper's schedule (leg 430)

Pre-registered (`e01a64d`): Appendix A.2's schedule in the paper's own parameter order (A.6) —
`M_d = 1`, `T_d = e + 10`, `P_* = 2e^{T_d} = 6.68·10⁵`, `λ ∈ {0.1, 0.05, 0.025}`, `h = 10⁻⁷`, `X_R = 10¹²` —
nine gates with the paper's numbers, six planted controls. Runner `experiments/arc6_profile_v1.py`,
fully log-scaled (the profile spans ~450 e-folds of `X`; `E` under- and overflows in plain floats).

| gate | pre-committed | measured (`λ = 0.1`) | answer |
|---|---|---|---|
| G1 `K_b` | `(.20, .25]` | **0.2450** | `YES` |
| G2 `P(.9), P(1.2), P′` | `< −.047, > .038, ≥ .36` | −0.0515, 0.1029, 0.441 | `YES` |
| G3 closure root in `[.9, 1.2]` | one root per `η` | **none**; (A.19) remainder `−1.08·10¹²` | **`NO`** |
| G4 `M, J` at pulse end | `< 10⁻¹⁰` | `1.1·10⁻¹²`, `1.5·10⁻¹²` at the paper's bump-centre scale (`NO` at the scale the prereg wrote) | `YES` / `NO` |
| G5 angular identity | measure `< 10⁻⁶` | `3.4·10⁻⁶` (a 10⁸-fold cancellation); the identity holds in Lemma A.8's form to `10⁻¹⁵` | `NO` |
| G6 exponents | `−½−λ`, `−A ± 10⁻⁹`; `d log e_b/d log λ ∈ [30, 36]` | exact; `2·10⁻¹³`; **24.0** (= the schedule's `λ^{30+60λ}` to 0.04) | `YES` / `NO` |
| G7 cone (A.24) | everywhere; pulse margins | intermediate interval **84 %**; `√λ|w| = 6128` | **`NO`** |
| G8 `Π_0/(P_*²f²) ≤ −5/2`, even, `ηΠ_0′ > 0` | | **−3.31**, `4·10⁻¹⁶`, `> 0` | `YES` |

**The finding (`NO-AND-HERE-IS-WHERE`):** the (A.19) remainder is `(λ^{−120λ} − 1)/2` — `10¹²` at
`λ = 0.1`, `81.6` at `0.01`, and within a factor 3 of that asymptote at every swept `λ` — so the paper's
bracket `[.9, 1.2]` holds a root only once `120 λ log(1/λ) ≪ 1`: **measured, at every `λ ≤ 3·10⁻⁴` and
at none above** (post hoc sweep to `5·10⁻⁵`, fig113). The intermediate cone is governed by `√λ P_*`:
at `λ = 0.01` the paper's `P_*` passes 93.5 % of the interval, `P_* = 100` passes all of it. Neither is a
defect of Proposition A.4, which asks for `λ` *sufficiently small* after `P_*`; it is the measured size
of "sufficiently". Controls C1, C3 fired; **C5 and C6 could not fire** (the hold relaxes `I/(XH)` to its
target before the (A.11) bumps act; the `e^{−2ξ}` weight makes the `R_0` cut worth `3·10⁻⁴`); C2 was not
run (§69). **Tier 2, not a proof.**

## 7. `R5`(ii) — the residual stress on the terminal tail (leg 432)

Pre-registered (`96657de`) and **amended on a derivation before any number** (`fcac005`): writing Lemma
A.8's tail representation by hand showed the heat factor must be kept to first order — (4.11)
multiplies `Q_s` by `X`, and with it `X Q_s → (2+2h)L` beyond `X_b` **exactly**, so the stress vanishes
there; without it the power law's own viscous residual `−(2+2h)F` survives — and that the inviscid term
is `X ≈ 10^{207}` times the boundary term whose `δ⁻³` weight (A.48) quotes.

| gate | `h = 10⁻⁷` and `10⁻³` | answer |
|---|---|---|
| H0 two routes — (4.11) on Lemma A.8's backward moments vs (A.54)/(A.46)/(A.53) at explicit `q` | `1.2·10⁻⁹` (inviscid bracket), `3.2·10⁻¹⁰` (sub-dominant bracket), `1.5·10⁻⁷` (`T_z`) | `YES` |
| H1 sign | `𝒜, ℬ > 0`; the three (A.54) terms `≥ 0` | `YES` |
| H2 (A.48) | boundary term ÷ `b_θ(0,η)` → 1.11 at `δ = .05` from above; `e^{4/δ²}T_{0,θ}` carries **`δ⁰`** (power 0.051); boundary fraction `10^{−203}`; **`δ_× = 1.1·10⁻⁶⁹`** | `YES` as amended; original **NOT TESTABLE** |
| H3 (A.49)–(A.50), (A.55) | `|T_z/T_θ|` carries **`δ³`** (power 3.02); `C = 0.49` | `YES` as amended; original `δ⁶` **NOT TESTABLE** |
| H4 (A.56) `2 + h < a ≤ 2 + 2h` | `a − 2 ∈ [1.20h, 2.00h]` | `YES` |
| H5 admissible cone | `T_{0,θ}/F > 0`; `log₁₀ sup (a−2)(T_z/T_θ)² = −278` | `YES` |
| H6 scaling in `q` | `q^{A+½}T` invariant to `1.6·10⁻¹⁵` at `q = 1, 10, 10³` | `YES` |
| H7 support, (A.51) | `𝒜 = ℬ = 0` beyond `X_b` exactly; `δ³∂_δ log T = 8.0001` | `YES` |

Six planted controls fired (K1 no flat factor, K2 `D = A`, K3 residual moment, K4 reversed cutoff, K5
`h → −h`, K6 no heat factor: `ℬ(y ≥ 3) = −2.002`). **Leg 430 corrected in passing:** with the (A.5)
step's derivative 8, `c_o = 0.1` gives `f_o′/f_o = 0.40h`, not the `< h/4` its pre-registration claimed;
the paper's `h/4` needs `c_o ≤ 1/16`; (A.56) needs only `2f_o′/f_o < h` and holds (§70). **Tier 2.**

## 8. `R6` — the Lean, measured not assumed (wave 3, leg 431)

Five agents, one file each, no agent saw another's:

| | answer |
|---|---|
| **(a) build** | **`NOT-ESTABLISHED`** — the cache host *was* reachable this time; `lake build` ran 13.6 min with 0 errors (oleans 3608 → 3982, mathlib 3580 of 8370), one project module written (the problem statement, not the proof); `#print axioms` on the main theorem failed because its module was never reached — unreached, not refuted |
| **(b) statement** | **strictly `WEAKER`** than Theorem 1.1: the two exported theorems are Fefferman's **(C)** (nine clauses `PRESENT`) and **(D)** (`PRESENT` clause for clause, periodic pressure `STRONGER`); of Theorem 1.1's twelve clauses **5 `ABSENT`** (∃ compact `K`, smooth `(u,p)` on `[0,1)`, support in `K`, `sup‖u‖_{L²} < ∞`, `limsup‖u‖_{L∞} = ∞`), 4 `DIFFERENT`, 1 `WEAKER`, 2 `PRESENT`; the clause-for-clause transcription `breakdownStatement` is a definition no theorem proves |
| **(c) census** | 2486 files, 616,276 lines: **4 `sorry` in code, all four the challenge placeholders in `ComparatorChallenges/`**, which no solution module imports; **0 `axiom`**, 0 `admit`/`opaque`/`unsafe`/`native_decide`/`set_option`; 2409 modules reachable from the two main files, 73 dead; kernel level **`NOT-ESTABLISHED`** |
| **(d) comparator** | 11 checks: **7 PASS / 4 `NOT-ESTABLISHED`** — challenge definitions byte-identical to the project-side copies, target statements byte-identical challenge vs solution, no solution closure imports a challenge module; the comparator itself **never run** (binary absent); the upstream Formal-Conjectures pin could not be checked (three inconsistent pins, no copy) |
| **(e) coverage** | **74 `FORMALIZED` / 5 `PARTIAL` / 0 `ABSENT`** of 79 at source level (Theorem 3.1, Definition 3.3, Lemma 4.4, Corollary 7.3, Lemma 9.7 partial); the Lean cites a differently numbered draft, so every match rests on content; *"not a kernel check"* |

**No agent ran a kernel check.** The build was continued by the Conductor after the agents reported
(the cache completed; the project's own modules were compiling when this note was written); if it
reaches the theorem, `#print axioms` is a dated, Conductor-run, `UNVERIFIED` addendum to `leg_431.md`
and changes (a) only. The stale first-pass README banner (*"Sections 4–9 not read, Lean not
compiled"*) was struck and recorded, not rewritten.

## 9. `R5`(iii)–(vii) — pulses, iteration, headline norms, compact support, and the adversary (wave 4, leg 433)

_[WAVE 4 IN FLIGHT WHEN THIS DRAFT WAS WRITTEN — this section is filled at integration from
`writeup/data/arc6/wave4/merged.json`, gate by gate, with the adversary's verdict beside each worker's
answer; a signal the adversary faked is `NOT EVIDENCE` whatever the worker found (`leg_433_prereg.md` §3).]_

## 10. What the second pass does NOT establish, said once

That the proof is correct. That the Lean proves anything (no kernel check was reached). That the
construction closes at any `λ` a grid can reach (it does not; the paper never said it would). That
`W4` moves (the first pass measured that it does not). **Every unit is Tier 2. No `L1 → L4` link moved.
Clay ~0.05%.**

## 11. Defects of this pass, recorded (`CORRECTIONS.md` §66–§70)
Wave 1 dispatched before its STATE row existed (§3g step-1 defect); `R4`'s agent 4 worked in a
worktree without the gitignored inputs and read from the main checkout; the Conductor mis-stated
agent 1's build cap (13.5 of 40 min); `R5`(i)'s pre-registration mis-set three yardsticks (G4's scale,
G5's measure, G6's exponent window) and planted two controls that could not fire; `R5`(ii)'s
pre-registration was amended before numbers and four runner defects were fixed after the quick run,
none a tolerance; one ORCH_STATE commit was pushed without the merge gate and over the LIVE cap,
fixed in the next commit. None of these changed a gate answer; each is named where it happened.
