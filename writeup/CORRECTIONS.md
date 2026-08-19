# CORRECTIONS — the over-read register

**Created 2026-08-07 by leg 263 (Route-WESC), on the user's Ruling 2 of leg 178:**

> *"This is the fourth over-read closure found (165, 180, 185, and now 178 independently
> confirming 165), and the pattern now warrants being visible rather than inferable."*

This file exists because the alternative was a qualifier buried in a `capabilities.py`
`validated` string, which is where the leg-111 re-scope had been living since leg 141. A
correction that can only be found by grepping a 900-line index is not visible.

**What belongs here.** A *closure* — a banked negative result, a gate answered `NO`, a "measured
dead" — that a later leg found was **over-read**: the measurement stood, the sentence written
about it did not. Not every mistake; not typos; not sharpenings. The test is whether a reader
of the original artifact would come away believing something the repository now knows is false.

**What does NOT belong here.** Nothing in this file lifts a ban, promotes a route, or moves a
link of the `L1 → L4` chain. A correction that "not dead" replaces "dead" is not a route:
**"not dead" is not "open."** Every entry carries its own ceiling.

**Convention.** Corrections are **marked, never hidden**. The original wording stays standing in
its own artifact with a correction block beside it (the precedent is
`TECHNICAL_P2_ROUTETN_V1.md` §"The first version of this section was wrong…" and banked
lesson 35). This file is the index, not the substitute.

---

## The register

| # | closure, as banked | found over-read by | what was actually true |
|---|---|---|---|
| 1 | legs 111/141: the weighted-energy zero-width window is an **operator**-level obstruction, "a third dead realization" | **leg 165** (2026-08-06), then **leg 178** independently and by measurement (2026-08-07) | a property of **one trial space** (`span{sin kθ}`, `p = 1`). §4 below |
| 2 | the gCLM two-scale survival boundary `a* ≈ 0.5–0.55`, stated without its measured domain across **15 documents** | **leg 180** (2026-08-06) | the boundary is real; the scope line was missing, and is now carried in all 15 |
| 3 | leg 125: Object-B's Newton continuation stalls ⇒ the profile does not exist | **leg 185** (2026-08-06) | a **solver artifact**, named precisely enough to repair; reachability returns `a`-dependently |
| 4 | *(this file's occasion — the same closure as #1, closed by measurement rather than by literature)* | **leg 178**, landed by the user's Ruling 1 of 2026-08-07 | §4 below |
| 5 | leg 176's banked `C1_bordered_sigma_min_X.reading`, which **opens** "BOUNDED AWAY FROM ZERO and truncation-independent" before hedging in its own last sentence | **leg 249** (numerics) → **leg 268** (the tail-block twin, K3) → **verify_271** §6b (named the C1 field as the *upstream* regeneration source) | `σ_min` is **flat, not independent** — `0.139 %` over a 16-fold range — and the positive limit is float64 **evidence**, not a proof. §5 below |
| 6 | `σ_min = 0.0908` printed at **15 sites** of PUB2 as if it were an absolute magnitude of the operator | **leg 249** §10 (`W5`, measured the sweep) → **leg 270** (`E1`, found PUB2 discloses it nowhere: 0 hits for `convention`/`normaliz`/`0.0420`/`2π`) → **leg 276** (disclosed) | the **digits** are convention-relative by a factor of **12.5** (`0.01086 … 0.13580`, and `0.0420` in Xu's own `y`-space normalization); the **gate property** — bounded away from zero uniformly in the truncation — **is invariant**. §6 below |
| 7 | legs 198/218's **`Z_1` understatement ratio** (`1.198e9×` vs `2.2867e8×`, `5.24×` apart), banked side by side by leg 223 as an **unresolved disagreement**, "neither adopted" — left open across the record for 30 legs | **leg 228** (2026-08-07, Route-BHRV §4, a pre-committed falsification test) → **leg 279** (this entry; swept the record and carried the closure to every site) | **neither number is "the" ratio, because there is no such number.** The quantity is round-off-floor noise in a near-total-cancellation denominator: it spans **11.77×** under math-neutral perturbations *alone* — more than the disagreement it was supposed to explain — while the `‖A‖` control both legs agree on moves by **7.2e−12**. Quote **`‖A‖`** and **`Z_2`** instead. §8 below |

| 8 | leg 263's own census, whose clause (a) claimed **zero missed occurrences** over the "third realization" phrase family, and which argued the live stage-`V` ban's protection from the class-P list that census produced | **leg 272** (2026-08-07, re-ran both patterns over the same blobs) → **leg 282** (this entry; carried the pointer and both count corrections to their sites) | the census is short by **30 triple-asserting occurrences across 17 files**, from two named instrument causes (**case** and **hyphenation/wrap**): **class P is 28, not 18**, and the second sweep's file count is **32, not 34**. **0 of the 30 produced a wrong edit and exactly 1 lies in territory.** A **warrant** defect, not a text defect — `plan_of_record.py` is byte-identical and stays so. §9 below |

| 9 | leg 185's `a = 1/2` `ν` **magnitudes** (`−0.00817525` / `−0.00895316`), banked in a table beside a refined `a = 0.30` number and read downstream as measurements; and its `a* = 0.3865` **cross-check**, banked as *"two different calculations agreeing on the same number"* | **leg 210** (2026-08-07, Route-M2SV, parked branch `leg/210-m2sv-v1` @ `6e06880`, independently discretized re-derivation) → **leg 283** (this entry; swept the record and carried both halves to every site) | **SPLIT, and both halves matter.** UP: `ν = +0.01799364` at `a = 0.30` is **independently confirmed to 1.198e-06 relative (~5.9 digits)**, and the sign law is **strengthened to gauge-independence** (`ν → μ²ν` under dilation, `μ² > 0`, so no gauge can flip it). DOWN: the `a = 1/2` magnitudes are **sign-only** — leg 210's independent value is `−0.00082927`, a **10.33×** gap, and **neither scheme is grid-converged there** (leg 185's own ladder spans **62.2%** non-monotonically; leg 210's spans **119.2%** with amplitude collapsing toward the trivial null). The `a*` cross-check is **UNPINNED** by leg 185's own data — its two starts **straddle zero** at `a = 0.3865` (`+0.00000035` / `−0.00425080`). **Leg 125's own `a*` value is untouched.** §10 below |
| 10 | Whether `a*` itself (as opposed to leg 185's flawed corroboration of it) is a real, locatable feature of Object B — left an open, un-adjudicated three/four-way contradiction after §10/leg 283: leg 210's independent bracket `[0.36, 0.37]` **excludes** leg 125's `a* = 0.3864963972206034` | **leg 284** (2026-08-07, Route-NU12, pseudo-arclength continuation — a third, independent method) → **leg 296** (this entry; read all four reports method-by-method and reconciled) | **`a* ≈ 0.386` IS PINNED**, by two mutually independent methods agreeing to ~2e-3: leg 125's algebraic `Δ(a) = 0` crossing (`ν = 0`, residual `1.933e-15`) and leg 284's grid-converged pseudo-arclength turning point (`0.3857 ± 0.004`, monotone over 4 grids). Leg 210's exclusion bracket is **explained, not outvoted**: it used the same fixed-`a` Newton-restart method leg 284 showed (Findings 2 and 4) folds and develops a singular Jacobian (`σ_min/σ_max = 3.454e-19` at `n = 1601`) in exactly this neighborhood — and leg 210's own report already recorded the predicted symptom (non-convergence at `a = 0.3865`, residual `6.0e-03`; amplitude collapse toward the trivial null beyond it) independently of anything leg 284 later found. Leg 185's specific corroboration claim **stays refuted** — its two starts still straddle zero at `a = 0.3865`. §11 below |
| 11 | PUB3's `a_max_machine` exposure row (`writeup/4_p2_lottery/TECHNICAL_P2_PUB3_V1.md`, the Route-D v11 "Exposure" table) named the scalar as materially exposed but never carried a resolution once one existed; leg 294's own flag additionally mis-cited the site as line 134 quoting the literal `a_max_machine=1.0` — checked directly, no such literal string exists anywhere in the file (line 134 is unrelated prose; the actual site is the table row at line 148, which names the scalar without printing a value) | **leg 236** (row-exclusion) + **leg 226** (D2/D3 repair), reconciled by **leg 294** → **leg 295** (this entry; located the true site, found leg 294's line/citation imprecise, appended the resolution) | `a_max_machine`'s corrected value **0.55** (confirmed by two independent methods from the stale `1.0`) is now recorded at the site as a dated, additive footnote — **zero** existing sentence reworded. §12 below |
| 12 | PUB2's caveat family printed a single Xu-normalization digit, `0.0420`, at four sites (§0, §3.2, the §4.5 sign-correction paragraph, §7) as if it were the unambiguous conversion of `0.0908` into “Xu's own normalization” | **leg 277** (2026-08-07, Route-XUN, branch `leg/277-xun-v1`, never merged) → **leg 280** (this entry; applied the correction to the two sites that state it independently, §0 and §7 — the other two are backreferences to §0 and needed no separate edit) | Xu's Definition 4.1 names **two** norms: the *displayed* half-line definition (4.2), constant `π`, and the *equivalent* full-line norm, constant `2π`. `0.0420` is the **full-line** reading (`κ = 2π`); under the **displayed** definition the value is **`0.057643`** (`‖R‖_X = 17.348`, not `23.792`) — **`1.37×`** larger. §13 below |
| 13 | leg 174's banked `writeup/data/p2_route_vbs_v1_scoping.json::the_empty_cell.meaning`: *"no published work applies interval arithmetic to a **dissipative** fluid equation's own self-similar object"* — banked as the meaning of an empty occupancy cell and read downstream as the content of wall **W3** | **`V3` / leg 399** (2026-08-18, `16ba44e`), grading 9 fluid blow-up CAPs against leg 174's **own, unchanged** criterion → **the Conductor** (this entry), on **USER RULING (Q3) of 2026-08-18**, `writeup/escalations/RULING_W3_WORDING_2026-08-18.md` | **MEASURED FALSE, and no reading survives** — the word *self-similar* is in the sentence. `arXiv:2509.25116` (Hou–Wang–Yang) encloses, by interval arithmetic (§7.3, p.55), a solution of a system carrying `−ΔŨ` (Prop. 1, eq. (1.15), p.5) for the **unforced 3D incompressible Navier–Stokes equations** (eq. (1.1)), and its object **is** self-similar (forward, from singular data). **THE ARTEFACT IS NOT EDITED**: the ruling makes the Conductor's refusal — *"rewriting a banked datum to match a later finding is precisely how a record stops being a record"* — **the standing rule for banked artefacts**, not a one-off judgement. **W3 itself is unrefuted and STANDS**: its prose test requires a genuine **finite-time singularity**, and this object is not one (§1.2, p.2, *"smooth for positive times"*). The cell is occupied and the wall stands — **two different claims.** §32 below |
| 13 | (a) PUB2 §4.5 stated that “any claim that the digits `0.0908` and `0.71465` are convention-independent” does not survive; (b) the same paragraph's “optimistic by `7.9×`” factor was printed with no convention caveat anywhere in the document | **leg 281** (drafted 2026-08-07, Route-CVF, branch `leg/281-cvf-v1`, never dispatched) → **leg 280** (this entry; corrected (a), flagged (b), both in place, 2026-08-11) | (a) is **backwards for `0.71465`**: it is convention-**free** to `1.87e−16` (a ratio of `X`-norms with no border coordinate, so the weight cancels) — only `0.0908` is convention-relative. (b) the `7.9×` factor **is** convention-relative and unflagged: it ranges `5.265 … 656.95` (`124.8×`) over the same weight sweep §0 names. §14 below |
| 14 | leg 221's own repair-verification sweep found `writeup/data/spike1_stepC_gate.json` does not reproduce (`.runs[0].alpha` moves `13.2%`, two of four `predicate_checks` flip), identically with and without its own repair; declined to adjudicate, flagged forward as possible staleness or environment sensitivity | **leg 335** (2026-08-12, Route-S1GR) | **neither.** `experiments/p2_route_bvrr_v1_repair.py`'s `BANKED` registry entry for this artifact invokes the generator with `argv=["--logged"]` only, omitting the `--steps 2500` flag the banked artifact's own `runs[*].steps` field proves was used originally, silently falling back to the CLI default of `400` — a harness bug, not code drift or environment sensitivity (BLAS-thread control: `alpha` spread `1.55e-15` across `1/2/4` threads). All four resolution rungs reproduce the banked `alpha` to float64 precision when re-run at the correct `steps=2500`, and `0` of `4` `predicate_checks` actually differ. **REPRODUCIBLE_AS_BANKED.** §23 below |
| 15 | wave 4's two banked artefacts, `p2_route_v3_gradeA_v1.json` (4 quote/attribution sites) and `p2_route_l2_decay_v1.json` (the pin's provenance, and `326.875` per decade presented as a portable constant) | **`V-W4`** (2026-08-18, `b46ee4d`, `writeup/data/p2_verify_wave4_v1.json`), which **REPORTED and REPAIRED NOTHING** — the Conductor recorded it at integration | **six defects and one note, NONE of which changes a verdict or a number.** The `≤ 1` direction **still follows**, through the **local** suitable-weak-solution form (Seregin, `arXiv:math/0510396` §1), not the global Leray–Hopf form the phrasing suggested; ESŠ is `UNREACHABLE` at primary and banked as such, **never as a zero**. **ARTEFACTS NOT EDITED** (ruling Q3); the per-field repair is a wave-6 unit. §33 below |

**The process pattern, which is the reason for the register.** In #1 the repository *had the
reference in hand before it drew the conclusion* — leg 111's own novelty log §2 recorded the
EGM neighbourhood via a landing page, without the full text. In #1 and #3 the corrections came
from re-reading the repository's own banked data, not from new compute. This is what
**LESSON 91** (`CONTINUATION_PROMPT.md`) was written for: *"measured dead" without a named
realization is not an admissible gate answer.*

---

## §4 — The leg-111 headline re-scope, in full

### What over-read what

**Leg 111** (Route-WE, 2026-08-06) measured the Chen–Hou-shaped weighted-energy coercivity form
of the `a = 0` CLM linearisation over a seven-member weight family, on the trial space
`span{sin kθ}` — vanishing order `p = 1` at the origin. Its gate answered **`NO — 0 of 7`**, and
it took its own no-branch verbatim: *"the weighted-energy realization joins the dead list on the
friendliest object… **Bank it as a third dead realization**."*

**The over-read is the word "realization."** The weight exponent `γ` and the trial space are two
halves of the *same* degree of freedom: the trial space's vanishing order `p` is what sets the
membership threshold `γ < 2p + 1`, while damping at the origin needs `γ > 3`. Leg 111 swept one
half and held the other fixed, then reported the result as a property of the whole.

### The magnitudes, three trial spaces, one quadrature

| | leg 111, `p = 1` | leg 141, `p = 2` | leg 178, `p = 3` (`T2_egm`) |
|---|---|---|---|
| admissible window `(3, 2p+1)` | `(3, 3)` — **width 0.0** | `(3, 5)` — width **2.0** | `(3, 7)` — width **4.0** |
| contains the published `γ = 4`? | **no** | yes | yes |
| membership `‖·‖²` ratio per refinement at `γ = 4` | **`1.677722e+07`** (divergent) | `1.0000000000000002` | **`1.000000`** (convergent) |
| exponent margin at `γ = 4` | **`−1.0`** | — | **`+3.0`** |
| largest admissible gap | **`−0.4999241`** | — | **`+0.499999667`** |

Leg 141 reproduced leg 111's `p = 1` admissibility column at **`abs_diff 0.0`** — same
quadrature, same code, only the trial space moved. Leg 178's grid stability at `p = 3`:
relative change over the last two refinements **`5.890e−07`** and **`7.409e−08`**.

Three constants agree to **`0.000e+00`**: leg 111's own `D_φ(0) = (3−γ)/2` at `γ = 4` is
`−0.500000`; EGM's `−(1/2 − C|a|)` at `a = 0` is `−0.500000`; Xu's published modulated gap is
`0.500000`.

And one exact fact that lands on leg 111's own enumeration: EGM's published weight **is** leg
111's family `B` at `γ = 4` — `φ^E/φ^B4` constant **`32`**, relative spread `1.998e-15`,
`|ratio − 32| ≤ 3.553e-14` — the single member the seven-weight ladder excluded (`B` stopped at
`γ = 2`, `A` at `γ = 4`).

### The correction chain, dated

| leg | commit | what it did |
|---|---|---|
| 111 | — | banked the closure as a realization-level death |
| 141 | `7bd6c08` | found the content **published** (EGM [arXiv:1906.05811](https://arxiv.org/abs/1906.05811) Prop. 2.1, gap `1/2` at `γ = 4` on this object); capped the *reading* in `capabilities.py` — the buried qualifier |
| 165 | `84a5c7e` | classified the row **TIER 1, realization-dependent**, from banked data only; escalated. Left the coercivity half at `p ≥ 2` explicitly *"recomputed by nobody"* |
| 171 | — | recorded Xu's own *"Map of realizations"* (§3.1), incl. `S8` = EGM singular weight, **ALIVE** |
| 178 | `ba1a22c` | **recomputed it.** `+0.499999667` on a constrained `p = 3` space. Parked at run time under escalation #3; landed by the user's Ruling 1, 2026-08-07 |
| 263 | *this leg* | the re-scope, made visible; per-occurrence triple pinning |

### The ceiling — what this correction does NOT license

Verbatim, the user's bounding language at leg 178: **"Do NOT open a weighted-energy lane.
'Not dead' is not 'open.'"** Concretely:

- EGM buy the origin conditions with **two free modulation parameters**, so a gap on a
  constrained trial space is **not a certificate**.
- The `−1/2` is **EGM's**. Reproducing it numerically is not a new theorem — leg 178 says so in
  as many words.
- The object throughout is the **`a = 0` CLM linearisation**, this repository's friendliest
  substrate, whose `Y₀` is **exactly zero for the banned degenerate reason**. Nothing here is a
  statement about `HL_S2_nonsymmetric`.
- **No ban lifts. No route is promoted. No link of the `L1 → L4` chain moves. Clay `~0.05%`.**
  Clause S7 binds unchanged.

### The two triples — read this before editing any "three realizations" sentence

The phrase *"`L1` stays measured-dead in all three realizations"* names **two different sets**
in this repository, and confusing them would silently weaken a live ban:

| | members | where it is authoritative |
|---|---|---|
| **plan-triple** | `ℓ¹_w` coefficient basis (leg 54) · collocation basis (leg 56) · origin-`H²` capped at `a = 0` (legs 163/176/182) | `plan_of_record.py` — the `P0` deliverable **and** the re-posed stage-`V` ban. **Weighted-energy is NOT a member.** |
| **journal-triple** | `ℓ¹_w` coefficient basis (leg 54) · collocation basis (leg 56) · **weighted-energy form (legs 111/141)** | the journals of legs 141, 165, 183 (and the same boilerplate elsewhere) |

**The revival falsifies the journal-triple's third member and leaves the plan-triple entirely
untouched.** Per the user's Ruling 2: *"Do not globally search-and-replace the phrase, and do
not let a correction to journal prose silently weaken a live ban whose justification rests on a
different set."*

Dating fact that makes the pin checkable rather than asserted: the plan-triple's wording
entered `plan_of_record.py` at commit **`4ff544a`**, *after* legs 141 (`7bd6c08`), 165
(`84a5c7e`) and 183 (`e8eb831`) all landed. At their dates the only enumerated triple was the
journal one, and `capabilities.py` calls the weighted-energy form *"the THIRD realization
(Route-WE, leg 111)"*.

**`plan_of_record.py` was not edited by leg 263** — its ban text is byte-identical before and
after, which is clause (c) of leg 263's own gate.

### Occurrences pinned by leg 263

See `experiments/journal/leg_263.md` for the full per-occurrence table, including the
occurrences that were pinned to the **plan-triple** and deliberately left unedited.

---

## §5 — Leg 176's `reading` field, and the regeneration hazard it carries

### The entry's class, stated honestly

Entries 1–4 are over-read **negative** closures: a gate answered `NO`, read wider than it was
measured. This one is an over-read of a gate answered **`YES`** — leg 176's origin-`H²`
construction closed, and the *sentence banked about it* claimed more than the ladder shows. The
register's own admission test is unchanged and it passes: *a reader of the original artifact
would come away believing something the repository now knows is false.* Recorded here rather
than in a new file, because a second register would be exactly the "grep a 900-line index"
problem this file was created to end.

### What is over-read

`writeup/data/p2_route_h2c_v1_construction.json`, key `C1_bordered_sigma_min_X.reading`, opens:

> **"BOUNDED AWAY FROM ZERO and truncation-independent."**

and only its *last* sentence supplies the hedge — *"This is float64 EVIDENCE of a positive limit,
not a proof of one."* Both halves of the opening fail at the precision the numbers are quoted to:

| half of the opening claim | what the banked data actually say |
|---|---|
| "bounded away from zero" | float64 **evidence** of a positive limit; **no proved floor** exists in leg 176 or in PUB2 — the field's own last sentence concedes this, and `TECHNICAL_P2_PUB2_V1.md` §3.5 states the limitation in full |
| "truncation-independent" | **flat, not independent**: `relative_spread` = **`0.0013899483438452888`** over `reliable_window` `[32, 64, 128, 256, 512]` — **`0.139 %` across a 16-fold truncation range** |

Leg 268 already corrected the *tail block's* twin descriptor (its `K3`, on
`C2_tail_block_sigma_min.reading`). **`C1`'s was never covered.** That gap is what
`verify_271` §6b identified as the upstream source of a phrase legs **250, 268 and 271** each
had to chase out of PUB2's prose separately.

### The hazard, and the three mechanisms that do NOT close it

The banked JSON is a **measurement record** and is correctly immutable — mutating it would
destroy the audit trail that let legs 249/268/271 and `verify_271` find these defects at all.
So: not a silent edit. Nor a fourth prose sweep — the prose is already clean (`verify_271`
clause (a): **0 surviving sites**). Nor a ban, since nothing here is a route.

**What closes it** is the precedent this file was built on — *corrections are marked, never
hidden* — applied to a data field instead of prose:

| layer | artifact | covers |
|---|---|---|
| primary record, **byte-untouched** | `writeup/data/p2_route_h2c_v1_construction.json` | leg 176's measurements, as banked |
| companion 1 (leg 268) | [`…_correction_leg268.json`](data/p2_route_h2c_v1_construction_correction_leg268.json) | `K1` `sigma_min_at_512` · `K2` `tail_inverse_norm_K2_at_512` · `K3` the **`C2`** descriptor |
| companion 2 (leg 274) | [`…_annotation_leg274.json`](data/p2_route_h2c_v1_construction_annotation_leg274.json) | `A1` the **`C1`** `reading` descriptor · `A2` the §3.5 subject label |
| index (this file) | `writeup/CORRECTIONS.md` §5 | makes both findable without grepping |

Both companions are in force simultaneously; neither supersedes the other. **The instruction a
future quoter is bound by** (verbatim from `A1`): any quotation of `C1_bordered_sigma_min_X.reading`
must quote the corrected framing —

> *`σ_min` is **flat** across the reliable window — `0.0908`, varying by `0.139 %` over a 16-fold
> truncation range (`N = 32 … 512`) — which is float64 **evidence** of a positive limit and not a
> proof of one. No proved floor is claimed.*

— or quote the banked text **with the annotation cited beside it**. Quoting the opening phrase
alone regenerates the defect.

### The second residue: the §3.5 subject label (`A2`)

`TECHNICAL_P2_PUB2_V1.md` §3.5 printed the `‖T⁻¹‖_X` ladder
(`3.994032 → … → 4.028864`, rising) and then attributed to it *"decrements shrinking
geometrically (`1.126e−3 → 5.745e−4 → 3.027e−4 → 1.617e−4`, ratios `0.510 / 0.527 / 0.534`)"`.

The four numbers are **correct** — they are the decrements of the **reciprocal**, the tail
`σ_min = 1/‖T⁻¹‖_X` (`0.25037356 → 0.24924783 → 0.24867333 → 0.24837063 → 0.24820892`, leg 268's
own `tail_sigma_min` list). A rising quantity has **increments**, and `‖T⁻¹‖_X`'s own are
`1.804e−2 → 9.269e−3 → 4.901e−3 → 2.623e−3`, ratios `0.514 / 0.529 / 0.535`. The two sets differ
by **`16.02× / 16.13× / 16.19× / 16.22×`** — a referee recomputing from the ladder printed in the
same sentence lands ~16× away. Provenance: `experiments/journal/leg_249.md` L233–234 → PUB2 via
leg 268 (`3f6d5d0`); found by `verify_271` §5; both sets now stand in §3.5 under their own names.

**This is not a fifth truncation-independence site.** It asserts no independence and overstates
no strength — `0.510/0.527/0.534` and `0.514/0.529/0.535` support the *same* conclusion, that the
sequence converges. It is a subject-attachment slip, graded as such by its finder.

### The ceiling

Leg 176's **gate answer is unchanged**, and leg 249 re-derived every matrix, identity and
convergence claim from the definitions — all survived. The `ℓ¹_w` **converges-vs-diverges
contrast is unaffected**; `Z₁` still fails at `140.72`. The object is the `a = 0` case only.
**No ban lifts. No route is promoted. No link of the `L1 → L4` chain moves. Clay `~0.05%`.**

---

## 6. `σ_min = 0.0908` is convention-relative, and PUB2 printed it 15 times without saying so

**Found by leg 249 (`W5`), located as a disclosure gap by leg 270 (`E1`), disclosed by leg 276.**

### What a reader would have believed

That `0.0908` is a magnitude of the operator, comparable across papers the way a residual or a
decay exponent is. It is not. Leg 249 §10 measured the freedom directly: the `X ⊕ ℂ` Gram puts
weight `1` on the border amplitude while the `X` block carries the **bare Laguerre
normalization** — no `2π`, no half-line `½`. That is a **choice**, and it is not a small one:

| what is swept | over | `σ_min` moves across | factor |
|---|---|---|---|
| the border-amplitude weight | `10⁻² … 10²` | `0.01086 … 0.13580` | **12.5×** |
| the `X`-block normalization | bare Laguerre → Xu's own `y`-space (carrying the `2π`) | `0.0908` → **`0.0420`** | **2.2×** |

Leg 270 grepped both PUB2 files for `convention`, `normaliz`, `0.0420` and `2π`: **0 hits**, at
**15 sites** printing the digit. Leg 249's own sentence: *"the digits are not invariant, and PUB2
quotes the digits without the convention."*

### What is actually true, and why this is a disclosure and not a retraction

**The gate property is invariant.** The thing leg 176's gate turns on — `σ_min` bounded away
from zero uniformly in the truncation — cannot be moved by a positive weight, because a positive
weight cannot send a positive limit to zero. And the only thing PUB2 ever argues *from* is the
**contrast in ladder behaviour**: flat here (`0.139 %` over a 16-fold truncation range), decaying
like `M^{−(1−s)}` in `ℓ¹_w`. Both halves of that contrast survive any positive reweighting. Leg
249 certified this in the same paragraph in which it measured the sweep, and leg 270 named it as
the reason `E1` sat below the escalation line.

**So: 0 arguments move, 0 gate answers move, and one class of sentence had to be added.**

### The repair, as applied

A single **convention note** at §0 of `TECHNICAL_P2_PUB2_V1.md`, carrying the sweep, Xu's
`0.0420`, and the invariance of the gate property *in the same breath* — plus a pointer back to
it at each of the six clusters where the digit is printed (§3.2, §3.5 ladder, §3.5 correction,
§4.5, §5(3), §7) and a plain-language paragraph at the blog's first use. The mechanism was chosen
from leg 270's own trace, whose `E1` entry reads *"what is missing is one disclosing sentence at
first use"*: 15 per-site caveats would have been six times the prose for the same content, and
would have required editing lines that carry byte-exact banked figures.

### The rest of the same pass (leg 276), recorded here for findability but **not** register-grade

Four bounds printed tighter than the data allow, now loosened to what the source supports:
`≤ 2.62e−03 → ≤ 2.63e−03` (banked `2.6248e−03`), *"at most 0.0090" → 0.00905* (banked
`0.00904587`), *"`p`-blind to 0.009" → 0.00904* (banked `0.00903658`), `≤ 2.22e−14 → ≤ 2.221e−14`
(banked `2.22012e−14`). One provenance chain corrected: `0.71465` is the five-decimal rounding of
leg 163's banked `implied_sigma_min_lower_witness = 0.7146549471256172`, itself
`1/1.39927667753796` in full precision — **one step**, not the two-step "round the ratio to
`1.3993`, invert, then round up by `7.0e−06`" that PUB2 printed twice and that does not reproduce
(`1/1.3993 = 0.7146430`, which rounds to `0.71464`). One subject slip: `0.868155` was seed 0's
`M = 8192` value, not a figure "over four data"; the four-data max is `0.8681539`.

**None of these is an over-read in this register's sense** — no reader would have come away
believing a closure that was not there. They are precision and provenance, listed so a future
pass finds them in one place.

### The ceiling

Nothing here measures anything. Leg 176's gate answer, leg 127's theorem, leg 163's census and
leg 182's `NO` are all exactly as they were. The object is the `a = 0` case only. **No ban lifts.
No route is promoted. No link of the `L1 → L4` chain moves. Clay `~0.05%`.**

---

## 7. `seven` vs `seventy`: one transcription error fixed, one figure banked as unanchored

**Not a register row.** No reader came away believing a closure that was not there — this is a
number-transcription defect and a provenance gap. It is filed here because leg 278 is the
**declared final** correction pass on PUB2, and the standing rule from that leg's brief is
*consistency-or-banked-residue*: anything not fixed in that pass is written down here rather
than deferred to an eighth pass. An eighth pass requires the **user's own sign-off**.

### The defect, and how it survived six passes

PUB2 carried a `seven` / `seventy` split across four sites. Leg 270 found it (`C1`) and could
not resolve it. Leg 276 inherited it, searched **within the read-set that leg 270's framing
implied**, found no determining source, and honestly reported it as undetermined. `verify_276`
§9 then found the anchor **one grep outside that read-set, in the same directory**:

* `writeup/4_p2_lottery/BLOG_P2_ROUTECP_V1.md:12` — *"Seven legs of work (51–57) had produced a
  negative result about a certification method"*
* `writeup/4_p2_lottery/TECHNICAL_P2_ROUTENG_V1.md:22–24` — *"What seven legs held… Legs 51–57
  produced every part of a negative result and assembled none of them"*

Both name the same range. **The certificate-closure activity is legs 51–57 — seven.** That
splits the four sites **2/2**, not 4/0.

| site | text | status |
|---|---|---|
| `TECHNICAL_P2_PUB2_V1.md:35` | "**Seven** successive legs of this project failed to close such a certificate" | **correct**, anchored at legs 51–57. Not touched. |
| `BLOG_P2_PUB2_V1.md:14` | "We spent about **seventy** work-legs failing to build a computer-assisted proof…" | **plain transcription error** — near-verbatim copy of `BLOG_P2_PUB1_V1.md:9` ("We spent **seven** successive work-legs…") with the number mistyped. **FIXED by leg 278** to *"We spent seven successive work-legs…"*, matching PUB1 verbatim and PUB2's own technical companion. |
| `TECHNICAL_P2_PUB2_V1.md:627` | "the obstruction that consumed roughly **seventy** legs" | a **different, broader claim** — the span of the *obstruction*, not of the certificate attempts. **Unanchored.** Left standing; see below. |
| `BLOG_P2_PUB2_V1.md:52` | "the wall we had been hitting for **seventy** legs" | same broader claim as `:627`. **Unanchored.** Left standing. |

### The banked residue: `seventy` has no source, in either direction

Leg 278 swept `writeup/`, `experiments/journal/` and `reports/` for an anchor to the
seventy-leg obstruction span. **Result: zero.** The only occurrences of `seventy` outside the
two PUB2 sites are `BLOG_P2_ROUTED_V9.md:13` (an unrelated factor-of-seventy bracket) and the
meta-discussions in `writeup/novelty/leg_270.md`, `leg_276.md` and `verify_276.md` that are
*about* this very question. By contrast `seven` / legs 51–57 has **two** independent banked
sources. **That asymmetry is the finding, and it is recorded rather than repaired.**

The two sites were **not** rewritten, deliberately. Substituting a different figure would
replace one unanchored number with another; softening the sentence would edit a claim that
`verify_276` §9 judged *defensible as a distinct, broader claim*. Neither is a fix, and this
register's own rule is that a sentence with no source gets its lack of source written down.

**What a reader should take from the two surviving `seventy` sites:** they are a rhetorical
span for how long the `ℓ¹_w` obstruction was being walked into, **not a counted figure**, and
nothing in PUB2's argument rests on the count. The load-bearing claim at
`TECHNICAL_P2_PUB2_V1.md:627` is the clause *after* it — that the obstruction is a property of
the certificate's **space**, not of the operator — which is leg 127's theorem and is anchored.

### The process defect this closes, which is the more important half

`verify_276` §10 diagnosed why PUB2 needed six passes: **each pass scoped its read-set to the
prior pass's defect list.** Leg 278 was scoped by **artifact** instead — a claim-sharing sweep
over all 117 markdown files in `writeup/4_p2_lottery/`, keying on every figure and named claim
PUB2 prints. That sweep is what confirms the 2/2 split rather than inheriting it, and it is the
reason this pass could be declared the last one.

### The ceiling

One word changed in one blog sentence. **0 arguments, 0 conclusions, 0 gate answers, 0 numbers
moved** — leg 276's 122-row trace re-runs at **122/122 rows green, 185/185 numeric tokens
byte-identical**, before and after the edit. Leg 176's gate answer, leg 127's theorem, leg 163's
census and leg 182's `NO` are exactly as they were. The object is the `a = 0` case only. **No
ban lifts. No route is promoted. No link of the `L1 → L4` chain moves. Clay `~0.05%`.**

---

## 8. The legs-198/218 `Z_1` disagreement is closed as EXPLAINED — and neither banked number survives as "the" ratio

**Class, stated honestly before anything else.** This is **not** an over-read of a closure; it
is the opposite shape — an *open item* that stayed open because both candidate resolutions were
wrong in the same way. It is registered here because the register is the repository's index of
"what a reader of the original artifact would come away believing that is now known false," and
a reader of legs 198, 218 or 223 would come away believing that one of two competing `Z_1`
ratios is correct and the other is a defect. **Neither is.** Landed by leg 279 (Route-Z1X,
2026-08-07); measured by leg 228 (Route-BHRV, 2026-08-07).

### The locators

| what | where |
|---|---|
| the measurement that closes it | `experiments/journal/leg_228.md` §4 ("THE `Z_1` DISAGREEMENT IS RESOLVED") |
| leg 228's runner | `experiments/p2_route_bhrv_v1_postrepair.py` (the two disputed values are pinned as `LEG_198_Z1_RATIO`/`LEG_218_Z1_RATIO`, `:599-600`, as *inputs* to the variance test) |
| leg 228's banked data | `writeup/data/p2_route_bhrv_v1_postrepair.json:2530-2531` |
| leg 218's original report | `experiments/journal/leg_218.md:60`, `:182`, `:258`; `writeup/novelty/leg_218.md:163` |
| leg 223's banking of the open item | `experiments/journal/leg_223.md:69-70` |
| leg 198's own journal | **does not exist on `main`** — branch `leg/198-bha-v1` is unmerged (leg 228 §5 records the same). Its number reaches the record only through the sites above. |

### What was banked, and what is actually true

Leg 198 (Route-BHA) measured that `solver/bordered_hl.py` silently accepted an inadmissible
border weight and reported the `Z_1` understatement on the `w_r = ±1e−6` configuration as
**`1.198e9×`**. Leg 218 (Route-BHR), re-running both modules in one process, measured
**`2.2867e8×`** — `5.24×` apart — while the `‖A‖` (`6.6712e+09×`) and `Z_2`
(`+1.188608e+17 / −1.779456e+07`) columns agreed to 4–6 significant figures. Leg 223 (PUB3)
printed both and adopted neither, per its own provenance rule.

Leg 218 offered the explanation (lesson 86): `Z_1 = ‖I − A·DF‖` with `A = inv(DF)` is a
near-total cancellation, so the *flipped* `Z_1` sits at the round-off floor and the **ratio** is
environment-dependent while the **verdict** is not. That was an explanation, not a measurement,
and it stayed unmeasured through leg 223.

Leg 228 measured it, and did so without the lesson-90 tautology of running the same arithmetic a
third time. It fixed the falsification condition **before looking at any number** — perturb only
in ways that provably cannot change the mathematics (algebraically identical re-associations of
the same matrix products; BLAS thread counts), and measure the spread **of the disputed quantity
itself**. If the spread brackets `5.24×`, the explanation stands; if the quantity is stable to
within a few percent, the explanation is wrong and one of the two numbers is a real defect to
escalate.

| quantity | spread under math-neutral perturbations alone |
|---|---|
| **the disputed `Z_1` ratio** | **11.77×** — `2.6422e8` to `3.1108e9`, against a disagreement of only `5.239×` |
| its denominator (flipped `Z_1`, ~`1e−15…1e−16`, the cancellation) | `6.407×` |
| its numerator (honest `Z_1`) | `1.165×` |
| `Z_1` at an **admissible** weight (not a cancellation) | `1.022×` |
| **control — the `‖A‖` ratio, the column both legs agree on** | **`1.0000000000072×`** (`7.2e−12` relative) |

Two illustrations of how little it takes: the `einsum` re-association alone moves the ratio from
`1.8015e9` to `3.2766e8`, having changed nothing but reduction order; **thread count alone**
spans the whole disagreement and then some, `2.6422e8` at 1 thread to `3.1108e9` at 4 — same
code, same machine, same inputs. The control is the sharpest number in the closure: if these
perturbations were breaking the computation rather than exposing a cancellation, `‖A‖` would
have moved too. It did not.

Leg 198's `1.198e9×` falls **inside** the observed band; leg 218's `2.2867e8×` falls just
**outside** it, `1.16×` below the observed minimum — reported precisely rather than rounded into
agreement, because the perturbation set is finite and obviously not exhaustive of the two legs'
actual environments. Leg 228's own third measurement (`1.801e9×`) is a **third point in the same
band, not a tie-breaker**.

### The forward practice this installs

> **Adopt NEITHER `1.198e9×` nor `2.2867e8×` as *the* `Z_1` understatement ratio. There is no
> such number to adopt.** Quote the reproducible columns instead: **`‖A‖` understated
> `= 6.6712e+09×`** (`w_r = ±1e−6`) and **`6.0663e+10×`** (`w_om = ±1e−9`), and **`Z_2`
> `= +1.188608e+17 / −1.779456e+07`**.

The same reading applies to the second, less-cited pair on the `w_om = ±1e−9` case
(`2.651e12` vs `1.5048e12`, `1.76×` apart): same cancellation, same mechanism, same advice.
Leg 228 measured the `w_r` case directly; the `w_om` pair is not separately re-measured and is
recorded here as **inheriting the explanation, not as independently closed**.

### Where the closure was carried (leg 279's sweep), and where it was not

Scoped by **artifact / claim-sharing set**, not by an inherited defect list: a repository-wide
sweep for either number and its roundings (`1.198e9`, `1.198e+09`, `2.2867e8`, `2.287e8`,
`2.2867e+08`, `2.287e+08`) found **13 occurrences in 9 files**.

**Carried (append-only; every original wording left standing):**

| site | what was added |
|---|---|
| `writeup/4_p2_lottery/TECHNICAL_P2_PUB3_V1.md` §5(a) | a dated update block after the original paragraph. §5's framing ("printed rather than resolved") was correct as of leg 223 and is preserved; the block records that item (a) was resolved **elsewhere**, by leg 228, not by that document. |
| `experiments/journal/leg_218.md` (`:60`, `:182`, `:258`) | dated pointer appended at end of file |
| `experiments/journal/leg_223.md` (`:69-70`) | dated pointer appended at end of file |
| `writeup/novelty/leg_218.md` (`:163`) | dated pointer appended at end of file |

**Deliberately not edited, and why — these are flagged for integration, not repaired here:**

| site | reason |
|---|---|
| `experiments/JOURNAL.md:3173`, `:3465`, `:3924` | **integration-owned shared ledger** (ORCHESTRATION.md §5a). `:3924` is the standing open item itself, which the orchestrator can now close against this entry. |
| `DIRECTION.md:7137`, `:7361`, `:7536`, `:7612`, `:7947`, `:8958` | DM-owned, and all six are **dated dispatch-priority records** citing `1.198e9x/1.189e17x` as the corruption potential that justified a ranking at the time. They are history, not live claims; rewriting them would be rewriting the record rather than annotating it. |
| `experiments/journal/leg_228.md:158`, `:188`; `experiments/p2_route_bhrv_v1_postrepair.py:573-4`, `:599-600`; `writeup/data/p2_route_bhrv_v1_postrepair.json:2530-1` | leg 228's own landed artifacts — read, never edited. They already **state** the closure; the two constants are its measurement's inputs and must stay verbatim. |

### The separate finding that travels with this one: leg 218's caller enumeration was incomplete

Recorded here because anyone re-reading legs 218/223 on the strength of this entry will read the
caller list too, and it is wrong. Leg 218 aimed its clause (b) at a caller set "enumerated **by
import**" and named six. Leg 228 §3 re-enumerated from the callers themselves: **13** direct
importers in the worktree, of which **10** existed contemporaneously with leg 218 (membership
decided by `git cat-file -e d9a20fb:<path>`, not a hardcoded list). **Five of the ten were
missed**, and the split was fixed in advance — *material iff a missed importer touches the weight
surface*:

* `experiments/p2_route_tn_v1_consistency.py:219` calls `b.weights(p=P_STAR, w_l=0.01*|X|max)` →
  the verdict is **MATERIAL**;
* the other four missed importers (`test_bordered_hl_adversarial.py`,
  `experiments/p2_route_bhn_v1_adversarial.py`, `p2_route_hlb_v1_contraction_lit.py`,
  `p2_route_nb_v1_targetnorm.py`) do not touch the weight surface;
* leg 218's sixth name, `p2_route_port_v2_reach.py`, imports `p2_route_port_v1_bordered` and not
  `solver.bordered_hl` — correct as a *transitive* caller, but that is the gap four direct
  importers fell through.

**This does not impeach leg 218's repair, and leg 228's gate is YES anyway**: the differential is
caller-*agnostic*, and leg 228 re-ran it over the full ten-importer configuration space —
`tn_v1_consistency`'s live configuration (`n=201`, `p=0.39`, `w_l = 0.01 |X|max`) included — at
45 configurations, 77,040 float leaves, **0** bit mismatches. What is corrected is the
*enumeration*, and the hazard is that a verification leg trusting it would have inherited the
hole.

**A consequence site, flagged not repaired (out of leg 279's gate scope, which was the two
disputed numbers).** `TECHNICAL_P2_PUB3_V1.md` §5(b) reproduces leg 218's incomplete list
verbatim — *"The live caller set, enumerated by import, is `port_v1`/`port_v2`/`l1_v1`/`l1rh_v1`
plus two test files"* — and `experiments/journal/leg_223.md` §"three disagreements" item 2 rests
on the same enumeration. Neither quotes a disputed `Z_1` number, so neither fell inside this
leg's sweep. **Recommended follow-up:** a pass scoped to the caller-enumeration claim, carrying
leg 228 §3's ten-importer table to both sites.

### The ceiling

**0 arguments changed, 0 gate answers changed, 0 banked values moved, 0 solver modules touched.**
Legs 198's and 218's verdicts stand exactly as banked — a sign flip corrupts these constants
catastrophically, which was never the disputed part — and so does leg 218's repair, leg 228's
`YES` on both clauses, and the contamination status (zero). Nothing here lifts a ban, promotes a
route, or moves a link of the `L1 → L4` chain. What changes is one thing only: **the record no
longer carries an open disagreement it had the measurement to close, and no longer invites a
reader to pick a side.** Clay `~0.05%`.

---

## §9 — leg 263's census was incomplete, and the record-maintenance bundle that closed it out

**Entered 2026-08-07 by leg 282 (Route-RMX).** Four small, verified, non-urgent record fixes,
bundled because none of them is worth a leg alone and all four were already measured by legs
272, 228 and 279. **0 new measurements, 0 solver modules imported, 0 shared ledgers opened for
writing, 0 lines deleted anywhere.**

### (1) The one in-territory occurrence leg 263's sweep missed

`experiments/journal/leg_141.md:232` (leg 272 pinned it at `:203`, its pre-leg-263 line number;
leg 263's own inserted correction block shifted it by 29 lines). It is a **local enumeration**
naming weighted-energy as the third dead realization, it is **wrapped** across two lines
(`three dead` / `realizations`) and therefore invisible to leg 263's line-oriented `grep`, and it
sits **below** that leg's correction block. **A dated pointer is now beside it.**

**Its severity is low and measurably so, which is why this was a light leg and not an
escalation.** Leg 141's own sentence de-rates the third member *in the same breath that counts
it* — "must be de-rated to a statement about a trial-space choice." A reader of that sentence
does not come away believing something the repository now knows is false, which is this file's
own admission test.

### (2) + (3) Two count corrections in leg 263's journal

Pointer appended at end of `experiments/journal/leg_263.md`, correcting `:72`, `:77–78`, `:98`
and `:163`:

| published | actual | bears on |
|---|---|---|
| class **P** = **18** | **28** | the warrant for the ban argument, not any edit |
| second sweep = 58 occurrences across **34** files | **32** files | nothing — no pin depends on it |
| P1 `76/39`, P2 `58 further`, total `134` | **reproduce exactly** | — |

The **occurrence** counts are exact to the occurrence. The instrument asymmetry behind the miss
is now on the record too: P1 reproduces **only case-sensitively**, P2 **only
case-insensitively** — `grep` run without `-i` on one pattern and with it on the other, stated
nowhere in leg 263's journal.

### The `plan_of_record.py:868` finding — recorded here as warrant-noise, deliberately not repaired

One of the 30 missed occurrences is inside the re-posed stage-`V` ban's **lift condition**
(*"…establishing it is not subject to the same **three-realization death**"* — the hyphenated
compound form, which is exactly what leg 263's space-separated patterns could not match). Leg 272
flagged it because its mandate said a miss touching the ban text is flaggable.

**It is recorded and not acted on, and the direction of the miss is why.** The occurrence is
**byte-identical** across leg 263 (`git diff 1fbbd0f^ 7724e67 -- plan_of_record.py` is 0 bytes;
same blob sha `846701e…` on both sides). It pins unambiguously to the plan-triple by local
enumeration — the ban's three members are spelled out seven lines above at `:861–862`. **A census
that had caught it would have classified it class P and edited nothing.** So the ban's text, its
members and its lift condition are all correct as they stand; what was short was the list the
protection argument was made from. **The text stays byte-identical. `plan_of_record.py` is
integration-owned and this leg did not open it for writing.** Locators for whoever audits it
next: `plan_of_record.py:868` · `DIRECTION.md:9523, :9602, :10075, :10651` ·
`experiments/JOURNAL.md:3639` · `experiments/journal/leg_256.md:36` ·
`experiments/journal/leg_262.md:315` · `writeup/novelty/leg_255.md:26` ·
`writeup/novelty/leg_262.md:152`.

### (4) Leg 279's forward flag, discharged: the six-name caller list

Leg 279 §5 named two consequence sites reproducing leg 218's incomplete enumeration and
explicitly declined to edit them (out of its gate scope). **Both now carry leg 228 §3's verified
ten-importer table:** `TECHNICAL_P2_PUB3_V1.md` §5(b) (dated update block appended after the
original paragraph) and `experiments/journal/leg_223.md` disagreement 2 (dated pointer appended
at end of file). The table itself is in §8 above and is not restated here.

**Nothing in either site's argument moves, and each check was made rather than assumed:**

* PUB3 §5(b)'s actual claim — legs 54/58/127 do not import `bordered_hl.py`, 0 of 7
  runners/evidence files — is untouched: **0 of the five missed importers belongs to leg 54, 58
  or 127**;
* its `w_om = w_r = 1.0` observation survives with sharpened wording: **none of the five missed
  importers mentions `w_om` or `w_r` at all**, so all five take `BorderedHL.weights`' defaults,
  which are `w_om = 1.0, w_r = 1.0` (`solver/bordered_hl.py:312`) — "passes" should read "passes
  or inherits by default";
* leg 218's repair is unimpeached, leg 228 having re-earned the differential over the full
  ten-importer space at 45 configurations, 77,040 float leaves, **0** bit mismatches.

**One precision correction to leg 279's own forward flag**, made rather than silently absorbed:
it described `leg_223.md` as reproducing "the six-name list." It does not do so *literally* —
that journal names no importer — it reproduces the **claim derived from** the enumeration. The
pointer was carried anyway, on the ground that a reader auditing disagreement 2 goes to leg 218's
list next.

### The sweep for other sites, and its blind spots

Clause (c) asked for any **other** site quoting the six-name list or either wrong count. The
instrument is the standing hardened rule this bundle's own sources produced (leg 272's real
product, PUB2's correction history): **case-insensitive** (`re.IGNORECASE` throughout),
**wrap-immune** (each file read as one stream with all whitespace — plus wrapped-blockquote
`#`/`>`/`|` markers — collapsed to single spaces *before* matching, so a phrase split at the
100-column hard wrap still matches), and **hyphenation-tolerant** (every intra-phrase space
written `[-\s_]+`, so `six name` / `six-name` / `six_name` all match, and module names match
across `[-_.]` boundaries). **13 patterns over 1,236 files** (`*.md`, `*.py`, `*.json`, `*.txt`,
`*.sh`; `.git`, `.venv`, `Papers`, `__pycache__` excluded).

**Result: no third consequence site exists.** Outside the four sites fixed above, every hit falls
into one of four classes, all correctly left alone:

| class | sites | why not edited |
|---|---|---|
| the finding's own artifacts | `leg_228.md:112, :118`, `leg_279.md:125`, `p2_route_bhrv_v1_postrepair.py:23–24, :390`, `CORRECTIONS.md` §8, `novelty/leg_228.md:73` | they **state** the correction; editing them would corrupt it |
| leg 218's own record | `leg_218.md:130`, `novelty/leg_218.md:84`, `p2_route_bhr_v1_repair.py:50, :358, :466, :515`, `p2_route_bhr_v1_repair.json:574` | the original wording stays standing by this file's convention; leg 279 already appended pointers to the two journals, and the runner/JSON are banked evidence |
| integration- and DM-owned ledgers | `experiments/JOURNAL.md:2918, :3939`; `DIRECTION.md:12178, :12194, :12199` | ORCHESTRATION.md §5a — flagged here, never edited by a leg |
| leg 272's own verification artifacts | `p2_route_wescv_v1_verify.py:114`, `p2_route_wescv_v1_verify.json:433` (both record `class_P: 18`) | that **18** is leg 272's faithful record of what leg 263 *published* — it is the measurement's input, and must stay verbatim |

**The blind spots, stated because a sweep's blind spots are part of its result.** The scan reads
five text-ish extensions only (no PDFs under `Papers/`, no binary or notebook formats); it treats
`|`, `*` and backtick as separators, so a phrase deliberately written with an *internal* asterisk
inside a word would be split; and it is a phrase-family sweep, so a site that paraphrases the
six-name list without any of the 13 patterns' anchors would not surface. Two patterns
(`class-P-18`, `all-18`) are deliberately over-broad and returned 43 hits of which **0** concern
this phrase family — reported rather than tuned away, since a pattern narrowed until it looks
clean is the exact instrument failure this register was opened over.

### The ceiling

**0 arguments changed. 0 gate answers changed. 0 banked values moved. 0 solver modules touched.
0 lines deleted. `plan_of_record.py` byte-identical.** Leg 263's 8 edits, its refusal to `sed`,
and the stage-`V` ban's text all stand exactly as they were; legs 218's repair, 228's `YES` on
both clauses and 279's closure are untouched. Nothing here lifts a ban, promotes a route, or
moves a link of the `L1 → L4` chain. The object under all of it is still the `a = 0` CLM
linearisation, and **"not dead" is still not "open."** Clay `~0.05%`.

---

## §10 — leg 185's `a = 1/2` magnitudes go sign-only, its `a*` cross-check goes unpinned, and its `a = 0.30` number gets stronger

**Carried by leg 283 (Route-M2SR), 2026-08-07. Measured by leg 210 (Route-M2SV), parked branch
`leg/210-m2sv-v1` @ `6e06880`, `experiments/journal/leg_210.md`.** Leg 283 produced **no number
of its own**; every magnitude below is leg 210's, and the only original work in this entry is
the sweep, the classification, and the provenance finding in §10.4.

### 10.1 Why this is a register entry and not a footnote

Leg 185 refined the number it was proud of and banked the numbers it was cautious about without
refinement. It **stated** the caution correctly — *"only the sign is banked"* — and leg 210
explicitly endorses that sentence. But an unrefined number printed to 8 digits, in the same
table as a refined one, acquires credibility from its neighbour, and the record duly quoted the
magnitudes downstream. **A reader of the original table would come away believing the repository
had measured `ν ≈ −0.0082` at Chen's `a`. It had not.** That is exactly this file's test.

The general lesson, in leg 210's words: **a grid ladder is owed to every banked number in a
sweep, not just the headline.**

### 10.2 The upgrade — which travels with the downgrade, and is the larger half

Recording only the negative half would misrepresent leg 210's SPLIT verdict more badly than
silence:

| clause | verdict | magnitude |
|---|---|---|
| `ν = +0.01799364` at `a = 0.30` | **CONFIRMED, independently** | Richardson **0.0179936185** at observed order **4.12** vs banked **0.01799364** — **1.198e-06** relative, ~**5.9 significant digits** |
| the gauge the reparametrization rests on | **VERIFIED AS A NUMBER** | predicted offset **8.634e-07**, observed **8.634e-07**, ratio **1.0000** |
| the covariance used as a derivation, at gauges wrong by `κ ∈ {0.5, 0.8, 1.25, 2.0}` | **RECOVERS** | worst **3.184e-05** across a 4× gauge range |
| the sign law `ν > 0` below the crossing, `ν < 0` at and above | **CONFIRMED AND STRENGTHENED** | now **gauge-independent**: `Ω(X) → Ω(X/μ)` sends `ν → μ²ν`, `μ² > 0`, so **no dilation can change the sign** |

The independence is real and was pre-committed before any number was computed: 6th-order
differences against leg 185's 4th, the second derivative by chain rule against `D∘D`, a
degree-5 Lagrange panel quadrature against 4-point Adams–Moulton, and the system restricted to
the odd subspace and solved by **LU** rather than least squares — with all four operators
validated against closed forms (`1.283e-08`, `2.236e-09`, `5.319e-10`, `3.468e-10`) *first*.
One operator is shared (`solver/line_hilbert.py`) and leg 210 declares it rather than hiding it.

**The gauge-independence is the most durable thing in this leg family**, and it is what the
downstream statements actually rest on — leg 174's catalog input and leg 187's construction
context both survive **fully**.

### 10.3 The downgrade, measured

At Chen's `a = 1/2`, leg 210's independent scheme gives **`−0.00082927`** from both starts at
relative residual `4.4e-15` — a **10.33×** gap against the banked `−0.00817525`. The decisive
instrument is the grid ladder **leg 185 never ran at `a = 1/2`** (it refined only `a = 0.30`),
and it **exonerates neither scheme**:

| | span across n = 201/401/801 | amplitude min/max |
|---|---|---|
| leg 185's own scheme at `a = 1/2` | **62.2%**, non-monotone (`−0.00655 → −0.00818 → −0.00443`) | ~flat, near Chen's scale |
| leg 210's scheme at `a = 1/2` | **119.2%** | **0.483** — collapsing toward the trivial null |
| **`a = 0.30` control, both schemes** | **1.94e-03** / **2.11e-04** | **0.999** |

The control is what makes this a measurement rather than an impression: the positive side
refines cleanly in **the very same code**, 320× to 5600× better. Leg 210 reports its own number
against itself — *"not the better number; it is a differently bad one"* — and `a = 0.45` (leg
185's `−0.00606636` / `−0.00792936`) is the worst point of all, leg 210's amplitude there
collapsing by **160×**. A gauge-free structural diagnostic agrees: seeded with its own dilation
image, the covariance recovery at `a = 1/2` is off by **5.977e-01** against **3.184e-05** at
`a = 0.30` — a genuine isolated root returns to its own dilation image; this one does not.

**Conclusion: no `ν < 0` magnitude of leg 185's is quotable. Sign only.** The `a = 0.55` and
`a = 0.70` rows were not separately re-measured but share the single-unrefined-grid provenance
and are covered by the same downgrade.

**What is NOT claimed.** "Not reproduced" is not "refuted as false", and neither scheme's number
is promoted over the other. There is **no converged quantity there** for the two to disagree
about. This is not a non-existence proof at Chen's `a`, and it does not touch the sign.

### 10.4 The `a*` half — and the boundary this correction must not cross

Leg 185 wrote that its `ν(a)` zero crossing *"lands on leg 125's own independently measured
`a* = 0.3864963972206034`"* and called it *"a cross-check, not a restatement"*. **The
cross-check is withdrawn, on evidence internal to leg 185's own journal:** its `a`-sweep row at
`a = 0.3865` reports **`+0.00000035`** from one start and **`−0.00425080`** from the other —
**the two starts straddle zero at that exact `a`**. Its own data never pinned the crossing; the
reported 8-digit coincidence is *one of two disagreeing starts* matching leg 125. Independently,
leg 210's sign-change bracket between **converged** scan points is **[0.36, 0.37]**, and
`a = 0.3865` is a point its scheme **fails to converge at** (relative residual **6.0e-03**).

**The line this entry does not cross, stated because it is the entry's largest hazard.**
`a* = 0.3864963972206034` is **leg 125's / Route-M2P's own number**, from the `Δ(a)` sweep at
`ν = 0` with `c_l` as the output, at relative residual **1.933e-15**
(`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEM2P_V1.md` §3.5, row `ν = 0`). **Leg 210 neither
measured nor refuted it.** What is unpinned is **leg 185's corroboration**, not the value. Every
site citing it as leg 125's stands untouched; leg 283 changed **0** numeric values of `a*`
anywhere.

**A provenance defect found by leg 283's own sweep** (not by leg 210): **five landed sites**
credit the value to **leg 185** as its own measurement — `writeup/novelty/leg_207.md:124`,
`experiments/journal/leg_207.md:19` (a verbatim dispatch quote), `TECHNICAL_P2_PUB3_V1.md:68`,
and the `A_STAR` comments in `experiments/p2_route_dpa_v1_adversarial.py` and
`test_dissipative_profile_adversarial.py`. All five carry attribution pointers now. **None is
load-bearing**: in leg 207's battery `A_STAR` is a *bracketing input*, never a claim, and in
PUB3 the `a*` label sits inside an escalation-**counting** argument that does not depend on it.

### 10.5 Where it was carried, and where it deliberately was not

Instrument: the hardened standing scoping rule — **case-insensitive**; **wrap-immune** (markdown
leaders `>`/`#`/`|`/bullets stripped and all whitespace collapsed to single spaces before
matching, so a phrase broken at the hard wrap still matches); **hyphenation-tolerant** (numeric
patterns written as bare digit runs with an optional `[-\s_.]{0,3}` separator between *every*
character and **no** sign, decimal point or leading zero required, so `−0.00817525`,
`-.00817525`, `0.00817525` and hyphen-broken renderings all match one pattern). **21 patterns
over 1,239 files** (`.md`, `.py`, `.json`, `.jsonl`, `.txt`, `.sh`; `.git`, `.venv`, `Papers`,
`__pycache__`, `.claude` excluded).

| class | sites | action |
|---|---|---|
| the primary record | `experiments/journal/leg_185.md` — D5 table, the `a*` paragraph, the honest-limits paragraph, the D5 summary, the leg-174-facing blockquote | **5 append-only pointer blocks**, original text preserved verbatim |
| leg 174's catalog — the site leg 210 addressed | `experiments/journal/leg_174.md`, `writeup/data/p2_route_vbs_v1_scoping.json` | **0 hits on every pattern**: the catalog carries no `ν` magnitude and no `a*` at all; its `CHEN-GCLM-DISS` row is model-level. **Nothing to downgrade** — the null check is recorded in `leg_174.md` as a dated note rather than left unrecorded |
| attribution sites | `writeup/novelty/leg_207.md`, `experiments/journal/leg_207.md`, `TECHNICAL_P2_PUB3_V1.md`, and two `A_STAR` comments | **pointers added**; 0 values, 0 assertions, 0 thresholds, 0 gate quotes altered |
| run artifacts (legs 185's and 207's) | `writeup/data/p2_route_m2sd_v1_diagnostic.json`, `experiments/p2_route_m2sd_v1_diagnostic.py`'s conclusion strings, `writeup/data/p2_route_dpa_v1_adversarial.json` | **never edited.** Leg 210's replay tier reproduced leg 185's banked ladder **exactly, to all 8 digits on all 4 grids** — these are a faithful transcription of what that code computed, and editing them would destroy the record of what leg 185 concluded, which is what the correction is *about* |
| leg 125 / Route-M2P's own `a*` | `experiments/journal/leg_125.md:116`, `BLOG_P2_ROUTEM2P_V1.md:89,115`, `TECHNICAL_P2_ROUTEM2P_V1.md:241,369`, `writeup/data/p2_route_m2p_v1_promotion.json` | **untouched** — a different computation, which leg 210 did not measure. Editing these is hazard (a) of leg 283's novelty pass |
| leg 180's own flags | `experiments/journal/leg_180.md:106`, `writeup/novelty/leg_180.md:112` | **untouched** — they already flag M2P's `a*` as a *different* `a*`, which is correct |
| integration- and DM-owned ledgers | `experiments/JOURNAL.md` (`:3298`, `:4008`, `:4011`, `:4016`, `:4018`), `DIRECTION.md` (`:6711`, `:6714`, `:6793`, `:6794`, `:6825`, `:12238`, `:12244`, `:12258`), `CONTINUATION_PROMPT.md` | **flagged here, never edited by a leg** — ORCHESTRATION.md §5a. `DIRECTION.md:6793` and `JOURNAL.md:4011` both quote `−0.00818`/`−0.00895`; the DM/orchestrator owns those lines |

**False positives, reported rather than tuned away.** The hyphenation-tolerant separator class
plus the dropped decimal point makes the numeric patterns deliberately over-broad inside numeric
JSON: `rounded_00818` returned **34 hits in 14 files** and `rounded_00895` **56 in 23**, of
which all but the `leg_185.md` and ledger occurrences are unrelated floats (e.g. `895316`
matching inside `0.4986225895316804`); `astar_4dig_3865` returned **83 hits in 28 files**,
mostly unrelated. `phrase_zero_crossing` returned **52 hits in 29 files**, almost all about the
fractional-gCLM and Route-F zero crossings — a different object entirely. One pattern,
`richardson_0179936185`, returned **0** hits, correctly: leg 210's Richardson limit had never
been carried into `main` before this entry.

**Blind spots, because a sweep's blind spots are part of its result.** Six text extensions only
(no PDFs under `Papers/`, no binary or notebook formats); anchoring is on **numbers**, so a site
that paraphrases *"the negative values at Chen's `a`"* without any digits would not surface; and
the parked branch `leg/210-m2sv-v1` is **read, never merged**, so leg 210's own artifact and
runner are not on `main` and this entry is currently the only place on `main` carrying its
magnitudes.

### 10.6 The forward note

**Leg 284 is taking leg 210's ladder to actual grid-convergence at `a = 1/2`.** If it succeeds,
this downgrade is **superseded by citation, not by deletion** — the sign-only status and these
pointers stay standing as the record of what was true when it was true, per this file's
"marked, never hidden" convention.

### The ceiling

**0 arguments changed. 0 gate answers changed. 0 numeric values altered anywhere. 0 lines
deleted. 0 run artifacts edited. 0 solver modules touched. 0 test assertions or thresholds
changed. `plan_of_record.py` not opened.** Leg 185's original text stands in full, with pointer
blocks beside it. Nothing here lifts a ban, promotes a route, or moves a link of `L1 → L4`:
"sign-only" is a *narrowing* of a banked claim, and a confirmed float number on a discretised,
truncated domain is still not a certificate and still not an existence proof. Stage P0 is
unaffected. Clay stays **~0.05%**.

---

## §11 — `a*`'s pinning status, reconciled across legs 125/210/283/284

**Carried by leg 296 (Route-ASR), 2026-08-07.** Every number below is one of legs 125, 210, or
284's own — this entry produces no measurement of its own. §10 above left one question
un-adjudicated: whether `a*` (an Object-B existence threshold) is a real, locatable feature at
all, given that leg 210's independent bracket `[0.36, 0.37]` excludes leg 125's `a* =
0.3864963972206034`. This entry closes that question.

### 11.1 The four data points, read method-by-method

| leg | quantity | mechanism | precision |
|---|---|---|---|
| 125 | `a*` where `Δ(a) := 2c_l/\|c_ω\| − 1 = 0` at `ν = 0` | algebraic sweep of `Δ(a)`, every point converged to machine precision, crossing found two independent ways | residual `1.933e-15`, `a* = 0.3864963972206034` |
| 210 | zero-crossing of `ν(a)` along a branch reached by restarting Newton from Chen's profile at each fixed `a` | scan between converged points only (a bisection was tried first and discarded, lesson 67) | bracket `[0.36, 0.37]`; `a = 0.3865` **fails to converge** in this scheme (residual `6.0e-03`), single grid |
| 283 | none — carrier of leg 210's finding | record sweep, 21 patterns / 1,239 files | 0 numeric values changed |
| 284 | `a` at which the branch **folds** (turning point), by pseudo-arclength continuation in `(Ω_odd, ν, a)` from the independently-converged `a = 0.30` root | `a` treated as an unknown, not a scan parameter, so the fold is traversable | 4-grid monotone convergence `0.39259 → 0.38626 → 0.38592 → 0.38568`; fold spread `0.008719` (< pre-registered `0.02`); re-pin `0.3857 ± 0.004` |

### 11.2 The determination

**`a* ≈ 0.386` IS PINNED**, to roughly `2 × 10⁻³`, by two mutually independent methods: leg
125's algebraic `Δ(a) = 0` crossing and leg 284's grid-converged pseudo-arclength turning point.
Both are computations distinct from the flawed one (leg 185's `ν(a)` sign-crossing via
fixed-`a` Newton restarts, refuted by its own straddling starts and by leg 210's independent
non-reproduction).

**Leg 210's exclusion bracket is explained, not outvoted.** Leg 210 used the same family of
method leg 185 used — Newton restarted at each fixed `a` — which leg 284 subsequently showed
(its own Findings 2 and 4) **folds and terminates near `a ≈ 0.386`** on every tested grid, with
an augmented Jacobian that collapses toward singularity in the same neighborhood
(`σ_min/σ_max` down to `3.454e-19` at `n = 1601`, seven orders below the control's drift). A
fixed-`a` Newton scheme has no mechanism to track a branch through a point where its own
Jacobian is singular; pseudo-arclength continuation is the standard remedy, which is exactly
what distinguishes leg 284's instrument from leg 185's and leg 210's.

**This is not retrofitted to the desired answer.** Leg 210's own report, written before leg 284
existed, already recorded the predicted symptom without explaining it: `a = 0.3865` itself
**fails to converge** in leg 210's scheme (residual `6.0e-03`), and its solution amplitude
**collapses toward the trivial null** as `a` increases past its converged range (`a = 0.45`:
160× collapse; Chen's `a = 1/2`: further collapse). Leg 284 independently supplies the
mechanism — a fold with a singular Jacobian — for a symptom leg 210 had already measured and
flagged as unexplained instability.

### 11.3 What does not change

**Leg 185's specific corroboration claim stays refuted**, exactly as leg 210 and leg 283
recorded it: its own two starts straddled zero at `a = 0.3865` (`+0.00000035` / `−0.00425080`),
an internal inconsistency independent of anything below. What this entry resolves is the
separate question of whether `a*` is a real feature of Object B at all — it is, and it sits
near `0.386`, corroborated by two methods leg 185 never used.

**Leg 283's UNPINNED note is not deleted.** It was the correct reading of the evidence
available on 2026-08-07 before leg 284 landed. Both `experiments/journal/leg_174.md` and
`experiments/journal/leg_283.md` carry append-only pointers to this entry; nothing in either is
reworded or removed.

### 11.4 Where it was carried

`experiments/journal/leg_174.md` (append at end, after leg 283's block), `experiments/journal/
leg_283.md` (append at end), `writeup/novelty/leg_296.md`, `experiments/journal/leg_296.md`.
Leg 174's catalog itself carries no `ν` magnitude and no `a*` value (per leg 283's 0-hit sweep,
§10.5 above) — nothing there required a numeric edit.

### The ceiling

**0 numbers re-measured. 0 gate answers of legs 125/210/283/284 changed. 0 lines deleted
anywhere.** This entry does not lift a ban, promote a route, or move a link of `L1 → L4`. `a*`
is a float-computed feature (an algebraic crossing and a turning point) of a discretised,
truncated profile equation — not a certificate and not an existence proof. Stage P0 is
unaffected. Clay stays **~0.05%**.

---

## §12 — PUB3's `a_max_machine` exposure row, resolved (and leg 294's own site citation corrected)

### 12.1 The dispatch, and what checking it directly found

Leg 294's consolidated Route-D v11 impact-trace (`writeup/data/p2_route_v11x_v1_consolidated.json`,
`experiments/journal/leg_294.md:97`) named one live document defect: `writeup/4_p2_lottery/
TECHNICAL_P2_PUB3_V1.md:134` "quotes `a_max_machine=1.0` in a consumer table," stale against the
corrected value `0.55`.

Checked directly, not assumed: `origin/main`'s line 134 (unchanged since before leg 294 ran —
last touch was leg 283's `0aa9da9`, an ancestor of leg 294's own landing commit `07c1098`) reads
`` `c(a = 1.50)` returns **0.20427 / 0.23717 / 0.97282** at `n = 101 / 201 / 301`, all three ``,
unrelated to `a_max_machine`. A whole-file, case-insensitive, wrap-immune sweep (the file
whitespace-normalized to a single line first, so a Markdown line-wrap cannot hide a match) for
the pattern `a_max_machine[^a-zA-Z0-9]{0,20}=?\s*1\.0` returns **zero hits** anywhere in
`TECHNICAL_P2_PUB3_V1.md`. The literal string `a_max_machine=1.0` exists only in leg 294's own
`experiments/journal/leg_294.md` and `writeup/novelty/leg_294.md` — leg 294 paraphrased the
table row as if it printed the stale number; it does not.

The real site is line 148, the Route-D v11 row of the "Exposure" consumer table: it **names**
`a_max_machine` as a banked, exposed quantity and grades it **DIRECT AND MATERIAL**, but prints
no numeric value for it at all. There was no literal digit to swap.

### 12.2 What was done

Because the site already correctly flags exposure without asserting the stale value as settled,
the gate's intent ("does the site state 0.55 with a dated note citing legs 236/226/294") is met
additively: one dated blockquote note was appended immediately after the exposure table (before
the following section), stating the resolved value — `a_max_machine`: `1.0 → 0.55`, confirmed by
two independent methods (leg 236's dependency-trace row-exclusion; leg 226's adversarial D2/D3
repair), reconciled by leg 294's consolidated report. **Zero existing sentences were reworded**;
the table row's own text is untouched.

### 12.3 The sweep for sibling repeats

Case-insensitive, wrap-immune (whitespace-normalized), scan of every `writeup/**/*.md` and
`experiments/**/*.md` for `a_max_machine` co-occurring with the stale value `1.0`. Hits outside
leg 294/295's own notes: four lines in `experiments/JOURNAL.md` (append-only history), all of
which **already state the correction inline** — e.g. `` a_max_machine 1.0->0.55 `` and
`` `a_max_machine`: 1.0 -> 0.55, confirmed by two independent methods ``. None asserts `1.0` as a
current, uncorrected value. No sibling document needed a fix.

### The ceiling

**0 numbers re-measured. 0 existing sentences reworded. 0 lines deleted anywhere.** This entry
does not touch `writeup/data/p2_route_d_v11_anchor.json` on `main` (still stale by ~6.55e+11x on
`margin` — leg 252's own integration decision, unmade, reserved as leg 297) and does not touch
any argument's meaning beyond adding the resolved scalar. Clay stays **~0.05%**.


---

## §13 — Xu's `0.0420` was the wrong constant among two, and the right one is `0.057643`

### What over-read what

Leg 249 §10 (W5) computed exactly one converted `σ_min` digit, `0.0420303`, under "Xu's own
`y`-space normalization." Leg 270 (E1) found PUB2 disclosed nowhere that this digit was
convention-relative and named `0.0420` as the Xu reading. Leg 276 disclosed it, at four sites
of `TECHNICAL_P2_PUB2_V1.md`: §0 (the convention note), §3.2 (the space-axis contrast table),
the §4.5 sign-correction paragraph, and §7 (Ceiling). **None of the four asked which of Xu's
two named norms `0.0420` actually was.**

Leg 277 (Route-XUN, 2026-08-07) read Xu's Definition 4.1 at primary source and found it names
**two** norms in consecutive sentences: eq. (4.2), the *displayed* definition, `‖φ‖²_X = ‖φ‖²_{L²(0,∞)} + ‖φ″‖²_{L²(0,∞)}`
(half-line, constant `π`), and the next sentence, which calls the odd part of `H²(ℝ)` an
*"equivalent"* — i.e. different — norm (full-line, constant `2π`). `solver/origin_h2_certificate.py`'s
`x_norm_y`/`x_norm` compute the **second** one, which is what leg 249's `0.0420` is. Leg 277
measured the half-line Gram independently (a double-exponential quadrature at both endpoints)
and found the two norms are **not proportional as Hermitian forms**: `H = πG + iS`, with `S`
real, antisymmetric, exact-integer-valued, and contributing exactly zero only on the real
coefficient subspace the certificate actually lives on (checked to `2.20e−14`).

### What was actually true

Under Definition 4.1's own **displayed** half-line norm (constant `π`, not `2π`),
`σ_min = 0.057643` (`‖R‖_X = 17.348`), **not** `0.0420` (`‖R‖_X = 23.792`) — a factor **`1.3715`**.
Both are legitimate readings of "Xu's own normalization"; PUB2 named only one, without saying
which, and the leg that produced the digit (249) never distinguished them either.

### Where carried

Applied 2026-08-11 (leg 280) to `TECHNICAL_P2_PUB2_V1.md` §0 (the convention note, where
`0.0420` is first printed) and §7 (Ceiling, the other site that states the figure independently
rather than pointing back to §0). §3.2 and the §4.5 sign-correction paragraph both already read
"§0's `0.0420`" / reference the convention note rather than asserting the digit independently,
so they carry the correction by reference and needed no separate edit — consistent with §6's own
design ("every later printing... points back to this paragraph rather than repeating it").
**`writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md`** also prints `0.0420` (its own §-equivalent of the
convention note) — **outside this leg's declared territory** (the dispatch names "the four named
TECHNICAL sites" only); flagged here, not edited, for whoever holds that path.

### What does not change

Leg 176's gate answer is untouched — it turns on `σ_min` being bounded away from zero uniformly
in the truncation, a property invariant under every positive weight, `π` or `2π` alike. No
conclusion in §§3–5 depended on which Xu constant was named; only the printed digit did.

### Ceiling

**0 numbers re-measured** (leg 277's measurement is reused, not repeated). **0 arguments
changed.** `a = 0` only, float64. No link of the `L1 → L4` chain moved. Clay stays `~0.05%`.

---

## §14 — `0.71465`'s convention-dependence claim was backwards, and its `7.9×` companion was unflagged

### What over-read what

`TECHNICAL_P2_PUB2_V1.md` §4.5, in the paragraph correcting the sign of leg 163's witness bound,
stated: *"Nor — per §0's convention note — any claim that the digits `0.0908` and `0.71465` are
convention-independent [survives]."* The same paragraph's antecedent sentence quotes leg 176's
own characterization of leg 163's witness as **"optimistic by `7.9×`"**, printed with no
convention caveat anywhere in the document.

Leg 281 (Route-CVF, drafted 2026-08-07, never dispatched) enumerated all 32 quantities the
certificate forms or quotes and classified each as convention-free (no border coordinate, so
the weight cancels between domain and range Grams) or convention-relative (mixes an `X`-norm
with a border amplitude carrying a different weight), measured over an eleven-point weight sweep
spanning `κ ∈ [10⁻⁴, 10⁴]`. Two of its rows bear on §4.5's sentence directly: `E5` (`0.71465`
itself) and `E6` (the `7.9×`/`7.87×` factor).

### What was actually true

`0.71465` is `1/max(‖u‖_X/‖f‖_X)` over leg 163's finite data family — a ratio of `X`-norms with
**no border coordinate** — and is measured **convention-free to `1.87e−16`** across the full
sweep. §4.5's sentence is right about `0.0908` (convention-relative, factor `12.5` over the
named sweep, up to `17321×` for the ladder-flattening digit measured separately) and **wrong
about `0.71465`**, which needs no convention caveat at all.

The `7.9×`/`7.87×` "optimistic by" factor is the **opposite** case: it divides a convention-free
quantity by a convention-relative one and is therefore fully convention-relative, ranging
**`5.265 … 656.95`** (**`124.8×`**) over the same weight sweep §0 already names — and carried no
flag anywhere in the document before this entry.

### Where carried

Applied 2026-08-11 (leg 280) to `TECHNICAL_P2_PUB2_V1.md` §4.5: the sentence about `0.71465`'s
convention-independence is corrected to apply to `0.0908` only, with `0.71465`'s convention-free
status and its `1.87e−16` measurement named; the `7.9×` factor is flagged with its measured
range in place immediately after it. Both edits are additive — no existing wording asserting a
conclusion in §§3–5 was reworded.

### What does not change

The reconciliation `0.0908 ≤ 0.71465` (§4.5's actual purpose in printing both digits) is
unaffected — it mixes a convention-relative quantity with a convention-free one and, per leg
281's 61-point fine sweep over twelve decades, **holds at every point tested**, with headroom
`5.26×` at the global `σ_min` maximum. Leg 176's gate answer and leg 249's verification are
untouched.

### Ceiling

**0 numbers re-measured** (leg 281's measurements are reused, not repeated). **0 arguments
changed.** `a = 0` only, float64, nothing interval-enclosed. `writeup/data/p2_route_cvf_v1_classify.json`
(leg 281, never merged to `main`) is not banked by this entry — this leg reads it, does not
publish it as a `main`-resident artifact, and leg 281's branch remains undispatched. No link of
the `L1 → L4` chain moved. Clay stays `~0.05%`. No ban lifted. No route promoted. No GA compute.

---

## §15 — The width ratio `6.855` corrected to `6.854` on 5 of the 7 landed surfaces
(leg 300's own no-branch rework)

### 15.1 What leg 300 found

Leg 300 (`experiments/journal/leg_300.md`, landed `5e30bf3`) independently verified leg
266's GATE-YES correction. Its clause (c) found the width ratio quoted `6.855` re-derives
from BCG's own `(eq:rstar)` and `(eq:r:restriction)` at γ=7/5 as the closed form
`(7+3√5)/2 = 6.8541019662496845...`, i.e. `6.854` at the quoted precision — absolute error
`0.00090`, relative error `1.310e-04`. Re-dividing leg 266's own rounded endpoints
(`0.1666667 / 0.0243163`) independently reproduces `6.854`, so the defect is a single
transcribed digit, not an architectural or arithmetic error. Leg 300's own propagation
census (§7) measured 8 surfaces carrying `6.855`, 7 already on `main`, and drafted this
leg (Route-P0TCR) as the rework.

### 15.2 What was done

5 of the 7 enumerated surfaces were corrected in place to `6.854`, each citing leg 300's
re-derivation and the closed form `(7+3√5)/2`: `experiments/JOURNAL.md:3730`,
`DIRECTION.md:11154`, `DIRECTION.md:13288`, `DIRECTION.md:13474` (reserve leg 305's
title), `DIRECTION.md:13479` (reserve leg 305's thesis). Window endpoints `1.1666667` /
`1.1909830` and both widths `0.0243163` / `0.1666667` are byte-identical before/after on
every touched line; no other numeric content changed.

### 15.3 What resisted, and why

2 of the 7 — `DIRECTION.md:13328` and `DIRECTION.md:13336`, the text of **leg 300's own
pre-committed gate** (thesis and question) — were left untouched, verbatim. Leg 300's own
journal (§7) states this text must not be edited: "a pre-committed gate records what was
asked." Editing it after the fact would misrepresent the historical record of what leg 300
was actually asked to verify (it was asked to check whether `6.855x` re-derives; it found
that it does not). This is this leg's own gate's no-branch condition — "a surface resists
correction without touching an argument" — so the gate answers **NO**, reported here and
in `experiments/journal/leg_319.md` rather than silently forced to yes.

### 15.4 The sweep for an 8th surface

A whole-tree, case-sensitive, literal-decimal-point sweep for `6.855` found no 8th
surface. All hits outside the 7 enumerated surfaces and leg 266/300's own prior artifacts
are incidental digit overlap in unrelated floats (`writeup/data/spike1_stepA_velocity.json`
`6.855039399091452` / `-6.855288156608295`; `writeup/data/p2_weight_repairs_v2.json`,
`p2_route_wvr_v1_fitness.json`, `p2_route_ngx_v1_general.json` — `26.85575221999712`,
`86.85522233596849`), and `writeup/INDEX.md` / leg 300's own `BLOG_`/`TECHNICAL_` /
`experiments/p2_route_p0tcv_v1_verify*.py` quote `6.855` accurately as leg 266's original,
now-superseded claim under test, outside this leg's declared territory.

### The ceiling

**5 numbers corrected, each cited to leg 300. 2 left untouched by design (§15.3). 0 other
numeric content changed anywhere (window endpoints and widths byte-identical). 0 lines
deleted.** This entry does not touch `leg/266-p0tc-v1` / `leg/251-p0t-v1` branch files, does
not touch `experiments/journal/leg_266.md:70`, does not touch `writeup/INDEX.md`, and does
not re-derive the closed form independently. Clay stays **~0.05%**.

---

## §16 — Pointers to the two immutable gate-text sites still reading `6.855`, and the BLOG_P2_PUB2
`0.0420`/`0.71465` sites corrected

### 16.1 The two immutable gate-text sites

**[ANCHOR CORRECTED 2026-08-12, leg 338 — Route-LCB1.]** This entry originally pointed at
`DIRECTION.md:13330` and `DIRECTION.md:13338` by line number. Those line numbers were already
stale at this file's own merge base (leg 338 finds the same quoted text now sitting at
`DIRECTION.md:13614` and `:13622`, having moved under unrelated edits) and would go stale
again with every further edit to `DIRECTION.md`. Per the verifier's own prescription, the
pointer is replaced below with grep-stable **text anchors** — the quoted phrases themselves,
not their line numbers.

The DIRECTION.md site quoting `6.855x wider` and the DIRECTION.md site quoting `6.855x width
ratio` (`grep -n "6.855x wider\|6.855x width ratio" DIRECTION.md` locates both at any commit)
— leg 300's own pre-committed gate thesis and question — **must stay that way** by standing
rule: editing a dispatched gate after the fact would corrupt the audit trail that caught the
wrong digit in the first place (leg 319's §2/§15.3 reasoning, adopted here as the rule rather
than re-argued). This entry is the pointer *beside* the record: the width ratio quoted at
those two sites as `6.855` re-derives as the closed form `(7+3√5)/2 = 6.8541019662496845...`,
i.e. `6.854` at the quoted precision — a slipped final digit, relative error `1.310e-04` — see
`experiments/journal/leg_300.md` §3 (the re-derivation) and `experiments/journal/leg_319.md`
§2 (why these two surfaces resist correction). `DIRECTION.md` is not touched by this entry; no
digit at either site is changed.

### 16.2 `writeup/4_p2_lottery/BLOG_P2_PUB2_V1.md:102,108`

Flagged by leg 280 (§6 of `experiments/journal/leg_280.md`, and this file's own §13) as
outside its TECHNICAL-only territory: L102 printed the uncorrected `0.0420` and L108's
parenthetical wrongly implied `0.71465` shares `0.0908`'s convention-dependence. Both are now
corrected in place, citing already-landed values only:

| site | before | after | source |
|---|---|---|---|
| L102 | `0.0420` (unqualified) | `0.057643` (`‖R‖_X = 17.348`), Definition 4.1's own displayed half-line reading; `0.0420` (`‖R‖_X = 23.792`) named as Xu's separate full-line-equivalent reading, `1.37×` smaller | leg 280, per leg 277 — this file's §13 |
| L108 | "(The same goes for the `0.71465` further down.)" | "(By contrast, the `0.71465` further down is convention-*free*, measured to `1.87e−16`.)" | leg 280, per leg 281 finding E5 — this file's §14 |

No value was re-derived by this leg; both are quoted from §13/§14 above, which leg 280 had
already banked. `git diff --stat` on the blog file: 1 file, 9 insertions / 3 deletions, both
hunks inside the two flagged sentences; window/witness numbers elsewhere in the file
(`0.0908`, `140.72`, `4.03`, `7.9×`) are byte-identical before/after.

### The ceiling

**0 numbers re-derived** (leg 277's, leg 281's and leg 300's measurements are reused, not
repeated). **2 blog-prose digits corrected, quoting already-banked values. 2 gate-text sites
left untouched by design, with a pointer added beside them instead.** `DIRECTION.md` not
edited. No conclusion in any leg's gate answer changed. No link of the `L1 → L4` chain moved.
Clay stays **~0.05%**.

---

## §17 — over-read closure #6: "closed three ways" — the GROUNDS were over-read, the WIDTH stands

**Found by:** leg 339 (2026-08-11, Route-ORC6, branch `leg/339-orc6-v1`), adjudicating on two
measurements it did not make — **leg 331** (Route-NLH) and **leg 332** (Route-VLO), both landed
before this entry was written.

**Pre-committed, not retrofitted.** DM cycle 7b wrote, at `DIRECTION.md:15343-15348`: *"'Closed
three ways' appears at two sites in this file … **No over-read closure #6 is recorded now.**
Whether any of the three ways rests on the (iv_a) silence screen is exactly what legs 331 and 332
measure; the pre-committed handling is written into their gates — a correction is drafted on a
measured answer, never on this reading."* Both answers came back; this is the correction drafted
on them. Neither measuring leg drafted it (`writeup/novelty/leg_331.md:283-284`: *"**No over-read
closure is drafted.** The gate answered NO, so the `yes`-branch instruction … does not fire, and
it is not drafted speculatively."*).

### 17.1 The claim, and where it stood

| site | wording |
|---|---|
| `experiments/JOURNAL.md:4929` | "The Grade-A/fluid cell really is empty, **closed three ways**, and leg 309 defended it against a claimant last cycle." |
| `DIRECTION.md:9683` (was `:9656` at `e9f4956`) | "THE GRADE-A/FLUID CELL IS EMPTY … **closed three ways** and defended against a claimant by leg 309." |
| `DIRECTION.md:14892` (was `:14865` at `e9f4956`) | "What stands, at measured width: **the Grade-A/fluid cell is empty** — **closed three ways**, defended against a claimant by 309." |

The phrase occurs in **no other file** — not in `plan_of_record.py`, not in `CLAY_ROADMAP.md`,
not in `CONTINUATION_PROMPT.md`, not in any leg journal or `writeup/` artifact. `git log -S`
places its introduction at `ce74d6b`, `cf72799` and `980f4cc`, all 2026-08-11, and **at none of
them is an enumeration attached**.

### 17.2 What was actually true — six verdicts over five distinct grounds

The record supplies **two** candidate triples and the sites disambiguate neither. Both were
adjudicated so the correction is right under either reading.

**Enumeration A**, the only literal banked triple (`experiments/journal/leg_261.md:184-202`) —
what closes the Breden-Chu weighted-Sobolev *vorticity route*:

| way | verdict | deciding measurement |
|---|---|---|
| A1 — screen (iv_a) / Remark 40's stated reach | **MISATTRIBUTES** | leg 331 §6: *"the reason it fails is **not** the reason Remark 40 gives … what actually breaks is that `Lam^{2a}` leaves `L^2(mu)`, i.e. it is the **weight** `e^{|x|^2/4}` versus an algebraic tail, not nonlocality as such."* Kill survives with magnitudes — truncated weighted norm `1.869e22` at `R = 16` against a local control saturating at `1.000000000` on the same code path; log₁₀ coefficient norm `1546.389` at Breden-Chu's own `n = 1500`; algebraic tails fitted `1.507674 / 2.012245 / 2.517908` vs predicted `1.5 / 2.0 / 2.5`. The *mechanism* does not: leg 261 said "incompressibility", leg 311 moved it to "nonlocality", leg 331 moves it to "weight vs algebraic tail". |
| A2 — the NRS/Tsai composition | **STANDS AT MEASURED WIDTH** | leg 332 §8 re-derives it independently and numbers it: `‖u_B‖_{L³(ℝ³)} = 0.7307683991070311`, decay exponent `−3.0000000000000027` vs predicted `−3`. Claimed at exactly the width now measured. |
| A3 — Gallay-Wayne prior art as evidence about the target | **OVERSTATES** (narrowly) | leg 332 §9: the weight `e^{+|x|²/4}` is adapted to the **forward** self-similar generator; Clay's object is **backward**. `‖L_forward ω_A‖ = 5.716528960333894` vs `‖L_backward ω_A‖ = 6.041350443296389`; Rayleigh quotients `7.2727` vs `6.4545`. Two decades of non-sighting under one drift sign is weaker evidence about the other than a closure needs. |

**Enumeration B**, the cell-level reading (components banked individually, never as a triple):

| way | verdict | deciding measurement |
|---|---|---|
| B1 — target absence (`leg_174.md:230`, *"the cell is empty for want of a TARGET, not for want of a method"*) | **STANDS AT MEASURED WIDTH** | Neither 331 nor 332 measures the literature. Leg 332 opens a lane and declines to call it a road: *"the NRS/Tsai wall is a **different** obstruction … named here so that nobody reads 'escape route' as 'open road'."* |
| B2 = A1 — screen (iv_a) | **MISATTRIBUTES** | as above |
| B3 — the Leray obstruction (legs 257/261, class C1, tail exponent `−4.0000`) | **OVERSTATES** | leg 332: *"**The step that fails is S4.** It fails because the entire non-vanishing tail of leg 257's obstruction lives inside `grad v` … and `curl(grad v) ≡ 0`."* Velocity-formulation-specific, measured: leg 257's divergence reproduced to 12 digits, max rel. diff `4.088e−12` with no shared code (FT1); the killing identity exhibited to `1.652e−10` (FT2); a two-arm control whose arms separate by ~11 000 decades on one code path (FT5). |

**The non-enumeration is itself part of the finding.** A closure claimed "three ways" for which
the banked record supplies two different, non-equivalent triples is a claim carrying more
definiteness than its own record — which is the same defect, in a different currency, as the one
closure #5 corrected.

### 17.3 What is corrected, and what is emphatically not

* **WIDTH STANDS, untouched.** The Grade-A/fluid cell is still empty. It is not that width was
  re-checked and passed — it is that **neither measured answer is about width**. Both legs
  returned *route* findings (leg 331 §6 is titled *"routed, not adjudicated"*). An escape from
  one obstruction into a second, named wall does not put an occupant in the cell. This is the
  weaker and more honest statement, and it is the one the record supports.
* **GROUNDS are corrected.** One way misattributes its mechanism, one overstates its reach, and
  the triple is not banked at any site that invokes it.
* **Nothing here re-opens the cell**, promotes a route, lifts a ban, or moves a link of the
  `L1 → L4` chain. A misattributed mechanism does not manufacture an occupant.
* **This is not a correction to leg 261.** Leg 261's own text is careful — it headed its section
  *"What kills the vorticity route instead"* and wrote *"Three named obstructions remain, and
  **none is leg 257's tail**"*, already recording C4 as convergent. The over-read is manufactured
  downstream, at the consuming sites, by compressing per-formulation, per-realization results
  into an unqualified count. That is lesson 91's exact catch: **a count standing in for a named
  realization.**

### 17.4 Sites, executed and delegated

| site | owner | status |
|---|---|---|
| `experiments/JOURNAL.md:4929` | integration ledger; leg 339 held a **declared single-site exception** | **corrected in place**, inline `[CORRECTED …]` marker, original sentence quoted verbatim and not deleted |
| this file, §17 | leg 339 (append-only territory) | **this entry** |
| `DIRECTION.md:9683`, `:14892` | **the DM** | **NOT edited by leg 339.** Exact drop-in replacement wording is delivered in `experiments/journal/leg_339.md` §7a/§7b, with a note on the stale pattern-count sentence at `:14887` in §7c. |
| `DIRECTION.md:89`, `:15454`, `:15488`, `:15882`, `:16108` | the DM | flagged, not prescribed. The last four are pre-commitment and dispatch text describing this very leg and **must not be corrected** — editing dispatched gate text after the fact corrupts the audit trail, the standing rule adopted at §16.1. |

### 17.5 A fact about this file, recorded not fixed

`grep -c "closure #5" writeup/CORRECTIONS.md` returns **0**. **Over-read closure #5 has no entry
in this register.** It was ruled (DM cycle 6, `DIRECTION.md:14896-14902`) to be **leg 328's**
territory, and leg 328 remains undispatched. Leg 339 does not write leg 328's entry. Recorded
here so that closure #6 arriving before closure #5 reads as a dispatch order, not as a gap.

### The ceiling

**0 numbers re-derived** — every magnitude above is quoted from leg 331 or leg 332 with its
locator; if either is wrong, this entry inherits the error. **1 prose site corrected in place**
(`experiments/JOURNAL.md:4929`), **0 conclusions in any leg's gate answer changed**, **0 bans
touched**, `plan_of_record.py` byte-identical and staying so, `DIRECTION.md` not edited. No link
of the `L1 → L4` chain moved. Clay stays **~0.05%**. The net effect is that one fewer thing is
believed than yesterday, which is the only kind of progress this register records.

## §18 — leg 305's landed prose: two claim-bearing corrections, measured against its own ledger JSON

**Dispatch: leg 336 (Route-C305).** Territory: the named claim sites in
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDWM_V1.md` and `BLOG_P2_ROUTEDWM_V1.md`, this entry, and
an appended note in `experiments/journal/leg_305.md`. `writeup/data/p2_route_dwm_v1.json` was
read, never edited.

### 18.1 Claim A — "C1 has the largest elasticity" (false)

Both landed surfaces (`TECHNICAL_P2_ROUTEDWM_V1.md` §4, `BLOG_P2_ROUTEDWM_V1.md`, and leg 305's
own journal §13) asserted that `C1_c_lap`'s elasticity, `−13.708%` of the window per `1%` move,
was the **largest** of any constant in the ledger. Measured directly against the ledger's own
`M2_pct_of_window_per_1pct` field (`writeup/data/p2_route_dwm_v1.json`, `ledger[]`):

| constant | `M2_pct_of_window_per_1pct` | `|·|` |
|---|---|---|
| `C9_a1` | `−31.058%` | **largest** |
| `C1_c_lap` | `−13.708%` | second |
| `C4_alpha` | `−5.702%` | |
| `C7_R2scale` | `−4.588%` | |
| `C2_c_r` | `+7.983%` | |
| `C3_c_dens` | `+5.665%` | |
| `C6_c_lin` | `−1.172%` | |
| `C5,C8,C10` | `0%` (flat side, per how `M2` is defined) | |
| `C11_aR1` | `0%` (see §18.2 — degenerate, not a genuine flat) | |

`C9_a1` is `2.27×` `C1_c_lap`'s magnitude. **`C1_c_lap` remains "the costliest constant" only
under leg 305's separately pre-registered rule — smallest `|move_to_close|` — which is a
different metric than elasticity and was never claimed to be the same thing; the two rows'
prose conflated the two by calling `C1` both "costliest" and "the single most sensitive knob" /
"largest elasticity" in the same breath.** The `move_to_close` ranking is unaffected: `C1` at
`−42.705%` is still the smallest-magnitude reachable move, ahead of `C2` (`+83.383%`), `C4`
(`−87.539%`), `C3` (`+702.492%`), with `C5`–`C11` unreachable.

### 18.2 Claim B — "all seven capped rows" (holds for six)

The same three surfaces asserted the `p ≈ 2` stationary-maximum response exponent and the T6
linearity-tolerance failure (`relative deviation ≈ 0.899`) held for **all seven** capped rows
(`C5`–`C11`). Measured against `scaling_exponent_up`/`_dn` and `M1_linearity_rel_dev`:

* `C5_c4`, `C6_c_lin`, `C7_R2scale`, `C8_a2`, `C9_a1`, `C10_a0` — genuine: one-sided exponent
  `≈ 1.996`–`1.9996` ("`p ≈ 2`"), `M1_linearity_rel_dev` `0.8991`–`0.8999`.
* `C11_aR1` — **not** genuine: both `scaling_exponent_up` and `scaling_exponent_dn` are `"flat"`,
  and `M1_linearity_rel_dev = 0E-54` exactly (not `≈0.899`), because both one-sided derivatives
  (`M1_one_sided_up`, `M1_one_sided_dn`) are exactly `0`.

**Adjudication: `C11_aR1` is inert-by-construction, not missing or broken data.** `C11_aR1`'s
row is the term `R₁ × (9(γ−2)γ + ((2−3γ)γ+5)r + 5)` in BCG's `R₂` (`eq:def_R2` l.550). The JSON's
own `structural_findings.R1_radicand_at_r_star ≈ 3E-59` records that `R₁` itself vanishes at
`r = r*` — the same fact that makes `r*` the `P_s`/`P̄_s` saddle-node in the first place (§4/§14
of the technical companion and journal). Perturbing the polynomial factor multiplying `R₁` by
`(1 ± ε)` multiplies an exact zero, which stays exactly zero; there is no undetected response to
measure, no broken perturbation script, and no data the runner failed to collect. This is
distinct from the six genuine capped rows, whose one-sided derivatives are small (`1e-4`–`1e-6`
scale) but strictly nonzero — a real, measured cap, not an identity. Lesson 90 applies directly:
a row whose both perturbation directions report bit-identical zero is a control that cannot come
out differently, and the tell (an exact `0` rather than a decaying-but-present quantity)
distinguishes "the geometry forces this to vanish" from "the instrument never fired."

### 18.3 SHARP verdict: dependence stated explicitly, UNMOVED by both

The SHARP_FOR_BCG_ARGUMENT_AS_STATED verdict (leg 305, banked, fig82) rests on two facts alone:
(i) every one of the eleven ledger rows classifies `M4_class = EXACT_IDENTITY`, and (ii) the
smallest-`|move_to_close|` rule names `C1_c_lap` as costliest, with no row classified
`ESTIMATE`. **Neither correction above touches `M4_class` for any row, introduces an `ESTIMATE`,
or changes which constant has the smallest `|move_to_close|`.** Claim A corrects which constant
is *most elastic* — a quantity the sharp/slack rule never used. Claim B corrects a count from
seven to six and adjudicates the seventh — a diagnostic (T6) that was pre-registered as
non-gate-triggering in leg 305's own text and stayed non-gate-triggering. **The SHARP verdict is
UNMOVED.**

### 18.4 Downstream consumers flagged

`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDWM_V1.md` §7 (leg 315 cross-reference) and any future
leg quoting "the costliest constant" or "the largest elasticity" from leg 305 should read `C1`
as costliest **by `move_to_close` only**; the elasticity superlative belongs to `C9_a1`. A sweep
(`grep -rln "largest elasticity\|most sensitive knob\|all seven capped\|0.899.*all seven"`,
excluding worktrees) found the "largest elasticity" clause repeated at two further sites outside
this leg's declared territory: `experiments/JOURNAL.md:5018` and `writeup/INDEX.md:124` (both
integration ledgers, not this leg's to edit — same discipline as leg 339's flag-not-prescribe
treatment of `DIRECTION.md` sites in §17.4). **Flagged here, not corrected**: both repeat "largest
elasticity (`−13.708%` window per 1%)" for `C1_c_lap`, which this entry's §18.1 has now measured
false against the source ledger. Neither site repeats the "all seven capped" wording verbatim
(`INDEX.md`'s summary omits the T6 detail entirely). Whoever owns `experiments/JOURNAL.md` and
`writeup/INDEX.md` should apply the same correction: `C9_a1` at `−31.058%`, not `C1` at
`−13.708%`, is the largest-magnitude elasticity in the ledger.

### The ceiling

**0 numbers re-derived** — every value above is quoted from `writeup/data/p2_route_dwm_v1.json`,
which this leg read and did not edit. **5 prose sites corrected in place** (`TECHNICAL_P2_ROUTEDWM_V1.md`
§4 ×2, §6 ×1 addition; `BLOG_P2_ROUTEDWM_V1.md` ×2; `experiments/journal/leg_305.md` §22
appended), **0 gate answers changed**, **0 bans touched**, `plan_of_record.py` and `DIRECTION.md`
untouched, `writeup/data/p2_route_dwm_v1.json` untouched. No link of the `L1 → L4` chain moved.
Clay odds stay **~0.05%**. The SHARP verdict for leg 305's argument stands, now resting on the
same two facts it always rested on, described correctly.

## §19 — leg 318's FT1 mechanism re-measured (r carries the ulp, not cancellation), and one
tautological control made falsifiable

Two independent, narrow findings against leg 318's landed Route-DECR criterion
(`ENCLOSURE IS CRITICALITY`, `writeup/data/p2_route_decr_v1.json`, `experiments/
p2_route_decr_v1_scoping.py`). **FT1's own verdict — decided in exact rational arithmetic,
residual identically `0` — is unchanged by either finding**, byte-for-byte, throughout.

### 19.1 The float64 mechanism, re-measured

Leg 318 banked FT1's float64 diagnostic residual (`5.329070518200751e-15` at the worst
γ = 1.075) as "~25 ulp of catastrophic cancellation between two `≈1`-sized operands,
`(r−1)/α` and `(r−2)`" — leg 302's failure mode, verbatim. **Directly re-measured (script and
full 45-γ grid in `experiments/journal/leg_337.md`), that story is wrong about the mechanism:**

* `α_of(γ) = (γ−1)/2` is computed with **zero** rounding error at the worst γ (and at every
  γ on the grid): `γ − 1.0` is exact under Sterbenz's lemma, and halving in binary floating
  point is always exact. α never carries any ulp error at any grid point.
* `r_crit(γ) = 2γ/(γ+1)` carries essentially all of it: its float64 value differs from the
  exact rational `2γ/(γ+1)` by `−0.88 ulp(r)` (≈ 1 ulp) at γ = 1.075, from the addition and
  division inside the formula.
* That single sub-ulp error in `r` is then **amplified** by δ_dis's own sensitivity to `r` at
  the root, `d(δ_dis)/dr = 1/α + 1 = 27.667` at this γ (dominated by `1/α = 26.667`).
  Substituting the exact rational `r`, `α` into δ_dis gives exactly `0`. Substituting the
  actual float64 `r` (with its `−0.88 ulp` error) and the actual float64 `α` (0 error) into
  δ_dis, evaluated in exact rational arithmetic, reproduces `−5.424e-15` — matching the
  observed float64 residual `−5.329e-15` to within the small extra rounding of δ_dis's own
  float ops.

**Corrected mechanism: 1 ulp of pre-existing rounding error in one operand (`r`), amplified by
the other operand's reciprocal (`1/α`) — not cancellation between two `≈1`-sized operands.**
"Leg 302's failure mode" as a category label is retracted along with it: this is
ill-conditioning under amplification near a root, not a subtraction-of-near-equal-terms
precision loss. **FT1's verdict is byte-unchanged**: decided in exact rational arithmetic,
residual identically `0`, either way — the mechanism correction does not touch the gate.

Corrected with inline strikethrough/correction markers in
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEDECR_V1.md` §5 and
`writeup/4_p2_lottery/BLOG_P2_ROUTEDECR_V1.md` ("The test that nearly killed it"), plus
correction comments (code comments only — no dict/string content banked into the JSON was
touched) in `experiments/p2_route_decr_v1_scoping.py` around FT1's instrument note and the
headline string.

### 19.2 The tautological control, made falsifiable and re-run

`experiments/p2_route_decr_v1_scoping.py`'s control `"adverse__criterion_makes_a_prediction_it_
could_lose"` read

```python
not shallow_water_supercritical or True,  # recorded explicitly below
```

which is `True` for **every** possible value of `shallow_water_supercritical` — a control that
can never fail is not a control (standing discipline, lesson 90: negative controls must be able
to come out FALSE). **Corrected to assert the sign-test result itself:**

```python
shallow_water_supercritical,
```

which genuinely can be `False` (if FT4's θ = 1 sign test had come out non-supercritical on the
window, this control would FAIL). **Re-run after the fix: `shallow_water_supercritical` measures
`True` (unchanged from FT4's own report), so the corrected, now-genuinely-falsifiable control
PASSES.** Not a smoothed-over result — the corrected control's pass/fail was checked, and it
passes for a real reason now instead of by construction. Running the corrected script reproduces
`writeup/data/p2_route_decr_v1.json` byte-identical to the version already banked (the "why"
text and the boolean's truth value are both unchanged; only the expression that could no longer
fail can now fail), so the banked JSON was read for comparison and left untouched, per this
leg's territory.

### The ceiling

**0 numbers re-derived** beyond the ulp-accounting values quoted above, all newly measured
directly against the live functions in `experiments/p2_route_decr_v1_scoping.py` (script in
`experiments/journal/leg_337.md`). **1 control expression corrected and re-run** (still PASSES,
now for a real reason). **2 writeup prose sites corrected in place**
(`TECHNICAL_P2_ROUTEDECR_V1.md` §5, `BLOG_P2_ROUTEDECR_V1.md`), plus comment-only markers in the
scoping script. **0 gate answers changed** — FT1's verdict and the leg 318 gate answer (`yes`,
`ENCLOSURE IS CRITICALITY`, not a lane) are untouched. `writeup/data/p2_route_decr_v1.json`
read, never edited (regenerates byte-identical). `plan_of_record.py` and `DIRECTION.md`
untouched. No link of the `L1 → L4` chain moved. Clay odds stay **~0.05%**.

## §20 — leg 338, Route-LCB1: four light non-structural corrections, batched

**Dispatch: leg 338 (Route-LCB1), amended before dispatch to add item (iv).** Four unrelated
verifier findings, each already located and each corrected to an already-banked source value —
no number is re-derived by this leg. All four are diff-checked to touch nothing beyond the
named site.

| # | site | before | after | source |
|---|---|---|---|---|
| (i) | `writeup/data/p2_route_fus_v1.json`, `sources.USC.cite` | `"Wang, Lai, Leger, Buckmaster …"` | `"Wang, Lai, Gomez-Serrano, Buckmaster …"` | arXiv:2509.14185's own author list (fetched directly): Javier Gómez-Serrano is a co-author; there is no author named "Leger" on the paper. `sources.USC2.cite` (a sibling field, `"Wang, Leger, Lai, Buckmaster …"`, arXiv:2511.22819) carries the same misspelling and is **flagged here, not corrected** — outside this leg's territory, which names "the one cite field" only. |
| (ii) | `writeup/CORRECTIONS.md` §16.1, and `experiments/journal/leg_321.md`'s citation of it | pointer by line number: `DIRECTION.md:13330` / `:13338` | pointer by grep-stable text anchor: the sites quoting `6.855x wider` / `6.855x width ratio` | Directly re-grepped: those two line numbers were already stale at this file's own merge base — the quoted phrases now sit at `DIRECTION.md:13614`/`:13622`. `DIRECTION.md` itself is untouched by this correction, per the standing immutable-gate-text rule (§16.1, leg 319's §2/§15.3 reasoning). |
| (iii) | `writeup/4_p2_lottery/TECHNICAL_P2_APIA_V1.md` §5 (leg 312's landed timing prose) | `117s` / `48s` / combined `346s` (`25.9s + 309.0s`, which does not itself sum to `346`) | `100.553s` / `35.515s` / combined `345.478s` (`36.480s + 308.998s`) | `writeup/data/p2_route_apia_v1.json`'s own `N1024_seconds` (`100.55331301689148`), `N512_seconds` (`35.51472449302673`), and the two `total_seconds` fields (`36.47977542877197` for leg 178's re-measurement, `308.99795627593994` for leg 176's), all already banked, none re-derived here. Non-claim-bearing prose; no gate answer touches this leg's timing. |
| (iv) | `experiments/JOURNAL.md:5018` and `writeup/INDEX.md:124` | "largest elasticity (−13.708% of window per 1%)" for `C1_c_lap` | inline `[CORRECTED …]` marker: `C9_a1`'s elasticity, `−31.058%`, is `2.27×` larger in magnitude; `C1_c_lap`'s `−13.708%` stands unchanged as its own value and as the smallest `move_to_close` | `writeup/CORRECTIONS.md` §18.1 / leg 336, which measured this directly against `writeup/data/p2_route_dwm_v1.json`'s `ledger[]`, `M2_pct_of_window_per_1pct` field. These two sites are exactly the ones leg 336 flagged, at §18.4, as outside its own declared territory (integration ledgers, not leg 336's to edit) — this leg applies the same correction leg 336 already measured, with no new measurement of its own. |

**Amendment note.** Item (iv) was added to this leg's dispatch at DM cycle 10, before dispatch
(`DIRECTION.md`, the `[AMENDED 2026-08-12, cycle 10, before dispatch: …]` note following the
§338 spec) — it is part of the pre-committed gate, not a widening performed by the leg itself.

### The ceiling

**0 numbers re-derived** — every value in the table above is quoted from an already-banked
source (arXiv:2509.14185's own author list for (i); `DIRECTION.md`'s own live text for (ii);
`writeup/data/p2_route_apia_v1.json` for (iii); `writeup/CORRECTIONS.md` §18.1 / leg 336 for
(iv)). **4 sites corrected, 1 batched entry** (this one). **0 gate answers changed** anywhere —
leg 314's classification, leg 312's `YES`, and leg 305's `SHARP` verdict are all untouched;
this leg's own corrections are non-claim-bearing (a citation spelling, two stale pointers, a
timing-prose arithmetic slip, and an already-adjudicated elasticity superlative). **0 bans
touched**, `plan_of_record.py` and `DIRECTION.md` byte-identical, untouched by this leg. No
link of the `L1 → L4` chain moved. Clay odds stay **~0.05%**.

## §21 — over-read closure #5, the register entry (six sites, four already fixed elsewhere)

**Dispatch: leg 328 (Route-ORC5), amended cycle 6b** (`CONTINUATION_PROMPT.md` removed from
territory — see 21.5). `grep -c "closure #5" writeup/CORRECTIONS.md` returned **0** before
this entry (recorded by leg 339 at §17.5); this section is the entry closure #5 was owed.

### 21.1 The claim, and why it was wrong

Load-bearing in `plan_of_record.py` (the file that states the plan): *"No certified viscous
blow-up exists in any model, in any dimension, today."* Per the user's external-review packet
of 2026-08-11, this is FALSE, and refuted by this repository's own banked data in leg 174's
own words: the occupancy matrix has `fluid=False, grade=A` OCCUPIED by DF-CGL
(`arXiv:2410.05480`), reproduced row-for-row by leg 316 (49,465/49,465 rows), and Breden-Chu's
viscous Burgers is a second Grade-A dissipative object. What is actually empty, at measured
width, is narrower: **the Grade-A/fluid cell** — no published work applies interval
arithmetic to a dissipative *fluid* equation's own self-similar object. Phase 1's rationale is
unchanged and never depended on the wider claim: if it cannot be done for a dissipative fluid
equation in 1D, 3D NS is not a question of compute. This is lesson 91's catch (a count/claim
standing in for a named realization) applied to width rather than a count.

### 21.2 The six sites

| # | site | fixer | status | wording now |
|---|---|---|---|---|
| 1 | `DIRECTION.md`, directive sentence, DM's own Phase-1 prose block — **[LOCATOR CORRECTED 2026-08-12, leg 298: the line number `:9856` originally recorded here had already drifted to unrelated text; grep-stable anchor `grep -n "user steer item 1, over-read"` locates the marker at `:9857` as of this leg's check]** | the DM, cycle 6 | **fixed** | inline `[CORRECTED 2026-08-11, user steer item 1, over-read closure #5: …]` marker; original sentence left standing, corrected wording follows it in the same block |
| 2 | `DIRECTION.md`, leg 303's (`ROUTE-GAF`) dispatched thesis — **[LOCATOR CORRECTED 2026-08-12, leg 298: the line number `:13722` originally recorded here had already drifted by 7 lines; grep-stable anchor `grep -n "only HL_S2_nonsymmetric specifically"` locates the site at `:13729` as of this leg's check]** | the DM, cycle 6 | **fixed** | inline `[CORRECTED 2026-08-11, user steer item 1, over-read closure #5: …]` marker pointing to site 1 and this leg |
| 3 | `plan_of_record.py:47` | the orchestrator, commit `ce74d6b` | **fixed** | `"Grade-A/fluid cell is empty -- no published work applies interval arithmetic to a dissipative FLUID equation's own self-similar object -- but Grade-A dissipative certification DOES exist off the fluid axis: Dahne-Figueras CGL (arXiv:2410.05480) … and Breden-Chu's viscous Burgers"` — verified present, byte-diff confirmed zero against this leg's pre-edit checkout (§21.4) |
| 4 | `CONTINUATION_PROMPT.md:68-80` | the orchestrator, commit `ce74d6b` | **fixed** | same measured wording as site 3; **NOT this leg's territory** (amended cycle 6b — §6 of that file reserves it to integration; this leg cites `ce74d6b` rather than re-editing it, per the DM's own amendment) |
| 5 | `CLAY_ROADMAP.md:343` | **this leg** | **fixed in this commit** | inline `[CORRECTED 2026-08-12, over-read closure #5, leg 328: …]` marker, same measured wording (Grade-A/fluid cell empty; Grade-A dissipative certification off the fluid axis, DF-CGL + Breden-Chu Burgers), pointing to this section |
| 6 | `DIRECTION.md`, the leg-294-era consolidation gate, `6.5457e+11` label | none — **gate text, immutable** | **pointer only** | see 21.3; the DM's own ruling (cycle 6, Item 3) holds this site is dispatched gate text and out of reach of any correction leg, itself included |

### 21.3 Item 3 — the `6.5457e+11` label, gate-text pointer

The DM's cycle-6 ruling (`DIRECTION.md`, "Item 3"): the one in-file site is a dispatched,
immutable gate (the leg-294-era consolidation gate), so the fix is carried as a standing
pointer rather than an edit. Recorded here per that ruling, verbatim in substance: the label
"stale-vs-regenerated" misattributes the whole `6.5457e+11` factor to staleness. Measured
decomposition: total stale/regen `6.5457e+11` = selection-repair alone `6.4926e+11`
(99.99%+ of the factor, leg 247's repair) × provenance drift `1.008188` (0.82%). The
consolidated JSON's own note already warned against exactly this misattribution.
`experiments/journal/leg_294.md` and `leg_297.md` are their owners' territory, not this
leg's or the DM's — flagged for those journals' integration notes, not edited here.

### 21.4 Verification that sites 3 and 4 needed no edit

`plan_of_record.py` before and after this leg's work is byte-identical (md5
`a4ece173c3eb890043332127a7d4d900`, confirmed both at worktree checkout and at push time) —
this leg never opened the file for editing, only read it to confirm the fix already present
and quote it above. `CONTINUATION_PROMPT.md` was read, not edited, and its current wording
(lines 68-80) matches the measured claim; the ban on editing it (§6, integration-reserved,
`ce74d6b`) is honoured.

### 21.5 Why `CONTINUATION_PROMPT.md` is not in this entry's "this-leg" column

The original spec (`DIRECTION.md`, leg 328's dispatch, drafted DM cycle 6) named
`CONTINUATION_PROMPT.md:70` as a second this-leg site alongside `CLAY_ROADMAP.md:343`. Cycle
6b amended the spec before this leg ran: the orchestrator had already corrected that site at
`ce74d6b`, and `CONTINUATION_PROMPT.md` §6 reserves the file to integration, not to leg
territory — a conflict the orchestrator surfaced rather than resolved silently. This leg
honours the amendment: site 4 above is recorded as orchestrator-fixed, cited, not re-edited.

### The ceiling

**0 numbers re-derived** — the DF-CGL/Breden-Chu occupancy facts are leg 174's and leg 316's,
quoted; the `6.5457e+11` decomposition is the DM's own cycle-6 Item 3 arithmetic, quoted. **1
site edited by this leg** (`CLAY_ROADMAP.md:343`, one inline marker, diff-checked to touch
nothing else). **4 sites verified already fixed, 0 re-edited** (two DM, one orchestrator on
`plan_of_record.py`, one orchestrator on `CONTINUATION_PROMPT.md`). **1 site is an immutable
gate, carried as a pointer only, no edit attempted.** `plan_of_record.py` byte-identical
before and after (§21.4); the live bans are untouched. No gate answer anywhere changes; no
link of the `L1 → L4` chain moves. Clay odds stay **~0.05%**.

## §22 — leg 352, Route-LCB2: one corrected, one resister found and NOT forced

**Dispatch: leg 352 (Route-LCB2), the accumulator's first harvest, leg 338's exact shape.** Two
proposed corrections were dispatched; the leg's own verification step (mandatory before
applying either) found site (i)'s premise **false** and did not apply it. Site (ii) is
corrected. One diff-checked site edited, one resister reported verbatim, per the gate's NO
branch ("a site resists... report the resister verbatim, land the other site... do not widen
scope to compensate").

| # | site | dispatched claim | verification result | disposition |
|---|---|---|---|---|
| (i) | `writeup/data/p2_route_fus_v1.json`, `sources.USC2.cite` (`"Wang, Leger, Lai, Buckmaster …"`, arXiv:2511.22819) | dispatched as "the same fix leg 338 made to `sources.USC.cite`" — i.e. that "Leger" is a misspelling of "Gomez-Serrano" here too | **FALSE.** arXiv:2511.22819's own live byline (fetched directly this leg) is "Yongji Wang, Tristan Léger, Ching-Yao Lai, Tristan Buckmaster" — four authors, no Gómez-Serrano at all. `Leger` is the ASCII form of the real coauthor **Tristan Léger**, a different person from **Javier Gómez-Serrano** (the coauthor on the sibling paper, 2509.14185, that leg 338 correctly fixed). The two papers have different, non-overlapping-in-this-name author lists; leg 338's fix does not generalize to this field. | **RESISTER, not forced.** `sources.USC2.cite` is left exactly as it was — its "Leger" is correct as written. Reported here so no future leg re-attempts this specific "fix" on the mistaken premise that it mirrors leg 338's. |
| (ii) | `experiments/journal/leg_221.md` and `solver/boussinesq_rescaled.py`'s module docstring (the two identical "86x the module's own tolerance" / "86x tolerance" sites describing the two-scale counterexample) | leg 307's arithmetic finding: the passage's own `5e-4` basis implies `~865x`, not `86x` | **Confirmed by direct re-computation:** `(2.0-1.135121)/2.0 = 0.4324395`; `0.4324395/5e-4 = 864.879`, i.e. `~865x`. The passage's other three magnitudes (`2000x`, `93.9x`, `1731x`) were checked by leg 307 and found consistent with their own bases; untouched by this leg. | **Corrected**, both sites, inline `[CORRECTED 2026-08-12, leg 307's arithmetic finding, batched at leg 352: 0.4324/5e-4 = 864.9, i.e. ~865x, not 86x]`, original `86x` wording left standing alongside the marker. |
| 16 | `L5`'s pre-committed gate (wave 5, `WAVE5_PLAN.md` @ `1e49a00`) said measure *"on route 4's **banked** discrete profile"* — **route 4 has no banked profile**, so the gate as worded was **unsatisfiable** | **`L5` itself** (2026-08-18, `4be46ef`), which banked `route_4_has_no_banked_profile = True` with evidence at `experiments/journal/leg_382.md:174` and `leg_397.md` §1, and substituted leg 381's **banked SYNTHETIC** exactly-DSS profile; the Conductor records it here as a **gate deviation**, which its integration commit `e42e7ab` described only as a limitation | **The substitution is the right one and the deviation is the unit's, not a defect**: leg 381's synthetic profile is the object clause (a)'s bill was computed on, so clause (b)'s bill is **directly comparable** to it, and control `C1` reproduces leg 381's exponents to `1.996e-12`. What it costs: **the EXPONENT is a class fact, the CONSTANT `c_mod = 869.288` is not route 4's number.** This is the direct motivation for wave 6's `L6`. |
| 17 | `L5`'s `C6` basis control **did not fire as planted** (`2.03e-02` against a pre-committed `1e-02`), and a **second, passing** criterion on a narrower fit window (`fired_on_tail3_fit`) sits beside the failing one; `c_mod = 869.288` is quoted unqualified though it is basis-dependent; the `U5` half of the `0.9958` cost ratio is **not in any banked JSON** | **`V-W5`** (2026-08-18, leg 403, `writeup/data/p2_verify_wave5_v1.json`, `self_hash da8a0d7cb9fb4896`), **LOCATED THREE, REPAIRED ZERO** — Conductor recorded at integration | **three defects, NONE changes a verdict.** The tolerance was **NEVER moved** (`347676f`; no `−` line on any ref, checked by the Conductor independently). The added criterion is **post-hoc**: it went in at the **landing** commit `4be46ef`, after the failure was known. The gate `NO` rests on the **exponent** and is untouched; the **CONSTANT is basis-dependent by `1.476×`** (C⁴ smoothstep vs leg 381's quintic C²). §35 below |
| 18 | `arXiv:2509.25116` v2 prints **four constants that do not recompute** (`H28`, `H30`, `H32`, `H33`), the worst being `x_0^U = 1.44e-5` where 50-dps re-derivation from the paper's own Class-A inputs gives `1.45054706437e-5` — **non-conservative** — because `η₂ = 0.005` was substituted where the certified `M_2^U ≤ 0.0061` belongs; separately, wave 4's `D1`–`D6`/`N1` were still undischarged | **`V5`** (2026-08-18, leg 402, `writeup/data/p2_route_v5_audit_v1.json`, `self_hash ae2b95efcbe5209b`) | **the certificate CLOSES anyway.** Carrying the corrected values through the whole chain, both closure conditions survive (`M_4^v = 0.0210567838661 ≥ 0.021`; `|λ| = 0.00426280601272 ≤ 0.0045`) — but `x_1^U` clears by **0.08%**, recorded as **luck, not margin**. `D1`–`D6`/`N1` discharged as **`_v2` deltas, no `_v1` edited** (ruling Q3). §36 below |

### The ceiling

**0 numbers re-derived beyond direct reproduction** — the author-list fact for (i) is
arXiv:2511.22819's own live text, fetched directly by this leg, and refutes the dispatched
premise rather than confirming it; the arithmetic for (ii) reproduces leg 307's own quoted
figure. **2 sites edited by this leg** (the two identical "86x" sites only — `USC2.cite` is
byte-identical, untouched), **1 batched entry** (this one, recording both the fix and the
resister). **0 gate answers changed** anywhere — leg 221's two-scale-gap finding, leg 314's
classification, and leg 307's own verdict are all untouched; this leg's correction is
non-claim-bearing (a tolerance-multiplier arithmetic slip). **0 bans touched**,
`plan_of_record.py` and `DIRECTION.md` byte-identical, untouched by this leg. No link of the
`L1 → L4` chain moved. Clay odds stay **~0.05%**.

## §23 — the spike1_stepC_gate.json reproducibility gap: not staleness, not environment — a missing `--steps 2500` in the regeneration harness

**Dispatch: leg 335 (Route-S1GR).** Territory: `experiments/p2_route_s1gr_v1.py` (new
diagnostic), `writeup/data/p2_route_s1gr_v1.json`, this entry, `writeup/novelty/leg_335.md`,
`experiments/journal/leg_335.md`. `experiments/spike1_stepC_gate.py` and
`writeup/data/spike1_stepC_gate.json` were read, never edited.

### 23.1 The claim, as banked

Leg 221's repair-verification sweep (`experiments/journal/leg_221.md` §2b,
`writeup/data/p2_route_bvrr_v1_repair.json`) regenerated `writeup/data/spike1_stepC_gate.json` by
shelling out to `experiments/spike1_stepC_gate.py --logged` and found it did **not** reproduce:
`.runs[0].alpha` moved from `-0.3350763095` to `-0.3793563731` (**13.2%**), and two of the four
`predicate_checks` flipped, `1_alpha_within_5pct` and `4_resolution_stable_alpha`, both
`true → false`. This reproduced identically whether leg 221's own repair (two guards in
`odd_field_x_slope`) was present or absent, so leg 221 could not attribute the movement to
itself, and — correctly, per its own stated discipline of not clearing what it cannot measure —
declined to adjudicate, flagging it forward as either staleness (code drift since the artifact
was banked at `51b63b2`) or genuine environment sensitivity.

### 23.2 What was actually true

**Neither.** The banked artifact's own `runs[i].steps` field reads **2500** in all four
resolution rungs — meaning the original run was invoked with an explicit `--steps 2500` flag,
since `experiments/spike1_stepC_gate.py`'s own CLI default is `400`
(`ap.add_argument("--steps", type=int, default=400)`). `experiments/p2_route_bvrr_v1_repair.py`'s
own `BANKED` registry entry for this artifact reads:

```python
dict(key="spike1_stepC_gate", artifact="writeup/data/spike1_stepC_gate.json",
     script="experiments/spike1_stepC_gate.py", argv=["--logged"], slow=True,
     calls="RescaledBoussinesq.run(renorm=True), 4 resolution rungs"),
```

`argv` carries no `--steps`, so leg 221's regeneration silently fell back to the CLI default of
`400` steps — an entirely different, far-less-relaxed trajectory, not a differently *computed*
one. This is a harness bug in the regeneration `argv` list, named in the source line quoted
above, not code drift and not environment sensitivity.

**Proven two independent ways, both measured this leg:**

* Re-running config 0 (`n_r=300, n_beta=48, r_min=1e-3, r_max=1e5, renorm=True, tol=1e-9`) at
  `max_steps=400` — the harness's actual, un-overridden invocation — reproduces leg 221's exact
  "regenerated" alpha: `-0.37935637310385306` vs. leg 221's reported `-0.3793563731`, `rel_diff =
  1.0157e-11`. This confirms the **cause**, not just the symptom.
* Re-running all four resolution rungs at `max_steps=2500` — the banked artifact's own recorded
  step count — reproduces every banked value to float64 precision:

  | run | banked `alpha` | rerun `alpha` | `rel_diff` |
  |---|---|---|---|
  | 0 (`n_r=300, r_max=1e5`) | `-0.3350763095343765` | `-0.33507630953437806` | `4.64e-15` |
  | 1 (`n_r=450, r_max=1e5`) | `-0.33396053473198634` | `-0.33396053473198667` | `9.97e-16` |
  | 2 (`n_r=600, r_max=1e5`) | `-0.3367555909794855` | `-0.3367555909794855` | `0.0` |
  | 3 (`n_r=450, r_max=1e6`) | `-0.33619163643975625` | `-0.33619163643975647` | `6.60e-16` |

  All four are float64-identical (a few ULP of accumulated-order-of-operations noise at worst).

* A BLAS-thread control (`OMP_NUM_THREADS`/`OPENBLAS_NUM_THREADS`/`MKL_NUM_THREADS` in `{1, 2,
  4}`, three separate subprocess invocations, config 0 at `max_steps=2500`, following this repo's
  own precedent `experiments/leg_0_bench_newton_threads.sh`) shows `alpha` moves by **`1.55e-15`**
  across the sweep — no environment/thread sensitivity. This rules out the second alternative
  leg 221's thesis left open.
* Re-evaluating the four gate `predicate_checks` against the correctly re-run values (all four
  resolution rungs at `steps=2500`) reproduces the banked `predicate_checks` **exactly** — `0 of
  4` actually differ. `1_alpha_within_5pct` and `4_resolution_stable_alpha` are `true` in both
  the banked record and this leg's correct re-run; the two "flips" leg 221 reported were a
  property of its own regeneration harness's missing `--steps` flag, not of the banked artifact
  or the code that produced it.

`solver/boussinesq_rescaled.py` and `solver/boussinesq_velocity.py` (the only two solver files on
this gate's call path) are byte-identical on the relevant well-posed-grid code path since
`51b63b2` except for leg 221's own repair (measured `0` of `256,233` calls moved) and commit
`26e6bd3` (adds raise-guards in `u_x_at_origin`/`PolarGrid.__init__` for empty/rank-deficient
windows and reversed intervals, which never trigger on this gate's well-posed configs,
`r_min=1e-3 ≪ r_window=0.1`). So there is no code-drift candidate either.

### 23.3 Adjudication

**REPRODUCIBLE_AS_BANKED.** `writeup/data/spike1_stepC_gate.json` needs no correction to any of
its numbers — the re-run harness (`experiments/p2_route_bvrr_v1_repair.py`'s `BANKED` registry
entry for `spike1_stepC_gate`) was at fault, shown above with the deciding evidence quoted. The
banked artifact's own `predicate_checks` (`1_alpha_within_5pct: true`,
`2_alpha_far_within_10pct: false`, `3_anisotropy_below_0p23: true`,
`4_resolution_stable_alpha: true`, overall `predicate_pass: false` on clause 2 alone) stand
unmoved.

### 23.4 Downstream consumers flagged

`experiments/journal/leg_221.md` §2b's language ("does not reproduce today... two gate predicates
flip") should be read alongside this entry: the non-reproduction was leg 221's own regeneration
harness's artifact, not a property of `writeup/data/spike1_stepC_gate.json` or the solver code.
`writeup/data/p2_route_bvrr_v1_repair.json`'s `clause_b.banked_runs` entry for `spike1_stepC_gate`
(`moved_detail`, e.g. `.runs[0].alpha` moving `0.1321`) records a real measurement of what its own
`argv=["--logged"]` invocation produced, and is **not corrected** here (append-only discipline;
the number it reports is accurate for the harness it actually ran) — but any future leg reading
that `moved_detail` list as evidence of drift in the banked artifact itself should read this
entry first. `experiments/p2_route_bvrr_v1_repair.py`'s `BANKED` registry entry is not this leg's
territory to edit (reads only, per dispatch) and is flagged, not corrected, for whoever owns that
file to add `"--steps", "2500"` to `argv` if the intent is a faithful regeneration.

### The ceiling

**0 numbers changed** in `writeup/data/spike1_stepC_gate.json` — every value in it was
independently re-derived, not re-read, and matched to float64 precision. **1 mechanism named**
with source-line evidence quoted (`argv=["--logged"]` in `experiments/p2_route_bvrr_v1_repair.py`,
missing `--steps 2500`). **0 gate answers changed** (the gate's own `predicate_pass: false` — on
clause 2, `alpha_far` — is unmoved). **0 bans touched**, `plan_of_record.py` untouched,
`writeup/data/spike1_stepC_gate.json` and `experiments/spike1_stepC_gate.py` untouched (read-only
per territory). No link of the `L1 → L4` chain moved. Clay odds stay **~0.05%**. What changes is
that leg 221's honest, undischarged flag now has a name and a closed status: **harness bug, not
staleness, not environment** — and the two "flipped" predicates never actually flipped against a
correctly re-run gate.

---

## §24 — environment-portability census (leg 287): leg 252's finding generalizes to ONE other
family, not to the other eight numerically-live ones

Leg 252 (`writeup/data/p2_route_d_v11_anchor.json`) found that regenerating one banked artifact
family with zero code change, in a later environment, moved 202 of 359 leaves (46 by >10%, one
`converged: True -> False` flip) — and left open whether that was an outlier or the norm across
this repository's other banked artifact families. Leg 287 censused N=10 other families (chosen
in advance, in `writeup/novelty/leg_287.md`, before any number was regenerated; explicitly
excluding the v11 anchor family itself, owned by the separate 236/226/252 consolidation), banked
in full at `writeup/data/p2_route_epa_v1_census.json`. Answer: **outlier, not the norm.** Nine of
the ten families reproduce their own banked bytes EXACTLY (`max_rel_move = 0.0`) when regenerated
with the same code at their own banking commit, in this environment. The exception is
`p2_route_e_v1_spectrum` (`experiments/p2_route_e_v1_spectrum.py`): `max_rel_move = 1.880`, 62
leaves moved by >10%, with the worst movers showing an index-level sign/ordering swap in an `E5`
spectral sweep near a degeneracy, plus (a strictly worse finding than leg 252's) run-to-run
disagreement between two independent regenerations made in THE SAME environment
(`determinism_control.two_processes_agree_on_nonvolatile_leaves: false`).

**The generalization, stated no further than the data supports:** for
`writeup/data/p2_route_e_v1_spectrum.json` specifically, banked leaf values are environment-local
and (per its own determinism control) not fully process-stable even within one environment;
compare its findings via a fresh re-solve in the environment you are actually working in, not by
reading the banked bytes as ground truth, exactly as leg 252 already established for the v11
anchor family. This does NOT extend to the other eight numerically-live families the census
measured (`p2_route_mf2_v1_residual`, `p2_route_l1rh_v1_construction`, `p2_route_hhr_v1_repair`,
`p2_route_h2i_v1_scoping`, `p2_route_nka_v1_adversarial`, `p2_route_dpa_v1_adversarial`,
`p2_route_cvf_v1_classify`, `p2_route_cap_v1_audit`) — the census positively confirmed those
reproduce exactly at their own banking commit, so their banked bytes ARE a valid stand-in for a
fresh re-solve, and this entry does not manufacture doubt about them.

One further, distinct thing the census surfaced and which this pointer explicitly does NOT fold
into the environment-portability lesson above: `p2_route_nka_v1_adversarial` fails to run at all
at today's HEAD (`solver/nk_bounds.py` now raises inside `farfield_modelling_error_bound` because
a later, unrelated leg tightened a validity boundary that one of `nka`'s adversarial cases now
sits exactly on) — a source-code change, not an environment effect, and not a harness/argv bug
either (the census's own invocation is identical at both refs; see
`experiments/journal/leg_287.md` §4 for the full three-way distinction). Recorded as
`classification_at_head: IRREPRODUCIBLE-AT-HEAD` in the census JSON; no CORRECTIONS pointer is
warranted for it because it is not a claim about banked VALUES being untrustworthy, only about
one adversarial case no longer running against current solver code.

### The ceiling

**0 numbers re-measured. 0 banked files modified (SHA-256 manifest before/after the census is
identical over all 23 hashed files;** `writeup/data/p2_route_epa_v1_census.json`'s own
`read_only_guarantee.zero_banked_files_modified: true`**). 0 gate answers changed.** This entry
adds a re-solve-not-bytes pointer for exactly one family and explicitly withholds it from the
other eight measured; it does not touch `writeup/data/p2_route_d_v11_anchor.json` or any of its
own consolidation work. Clay stays **~0.05%**.

---

## §25 — leg 356 (ROUTE-ESPX), 2026-08-12: §24's exception REPAIRED, not just re-solved.
Mechanism named and measured; every consumer diff-checked and unmoved

287 (§24) left `p2_route_e_v1_spectrum` in a specific, uncomfortable state: NON-PORTABLE (`max_rel_move
= 1.880`, 62 leaves >10%) AND (its own `determinism_control`) apparently failing to reproduce
itself even in ONE environment. Leg 356 was dispatched to name the mechanism, enumerate every
consumer, and either repair to canonical determinism or quarantine with consumers flagged.

**(a) Mechanism, measured directly, twice.** `solver/rescaled_spectrum.py`'s `match_filter()`
sorts kept eigenvalues by `-Re(lambda)` descending. That is the right key for the two isolated
STRUCTURAL modes (exactly 0 and -1, present at every `a`) but a broken one for the discretized
ESSENTIAL/continuum spectrum, which sits on the imaginary axis in exact arithmetic (`Re
lambda = 0`) and therefore has a computed real part that is pure floating-point noise at the
1e-11 .. 1e-17 level with a build-dependent sign. A direct repro (calling `spectrum(0.0, 96)` /
`spectrum(0.0, 144)` and `match_filter(..., tol=0.1)` in this environment, bypassing the
41-minute full pipeline) reproduced the SAME multiset of eigenvalue magnitudes leg 287's `E5_sweep[0]`
banked at commit `c45e81890a` — `{0, ±0.271, ±0.840, ±7.156, ±8.135, ±14.828, ±23.008, ±45.174,
-1}` — bit-for-bit, just at different array positions with the paired sign swapped, because the
sort key that placed them is noise. This is the SAME mechanism the dispatch text guessed
("eigenpair ordering/sign instability... near a degeneracy"), now pinned to one line
(`match_filter`'s `np.argsort(-np.real(kept))`) with a measured, reproduced witness rather than
assumed. **A second, distinct finding: 287's `determinism_control.
two_processes_agree_on_nonvolatile_leaves: false` is itself a FALSE ALARM.** Its
`string_moves_sample` (visible on the main `comparison`, not overwritten by the determinism
block, but the two share the one and only non-volatile string leaf in this document) names the
single differing leaf as `generated` (a timestamp) — which 287's own `VOLATILE_TOKENS` list
contains as `"generated_at"` but not bare `"generated"`, a one-token near-miss that let a
harmless timestamp masquerade as a content disagreement. All 1235 numeric leaves and 0 flag
flips agree between two independent same-environment regenerations. So: the cross-ENVIRONMENT
failure (banked-2026-08-02 vs regenerated-today) is real and is the ordering bug above; the
within-one-environment "determinism failure" 287 read off its own control was an instrumentation
gap in the census script, not a defect in this family's generator. (No fix to 287's census script
is made here — out of this leg's territory — this is recorded as a finding, not a repair of that
file.)

**(b) Every consumer, enumerated by repo-wide grep for `p2_route_e_v1_spectrum` / `fig34`:**
1. `experiments/p2_route_f_v1_viscosity.py` (Route-F) reads `E2_branch` -> `{a: alpha}` only.
2. `experiments/p2_route_j_v1_literature.py` (Route-J) reads `E7_end.a_c_linear_extrapolation`
   and (indirectly, via Route-F's own banked JSON) `E2_branch`.
3. `test_literature_gates.py::test_7_branch_against_xu` reads
   `E7_end.a_c_linear_extrapolation` directly and gates on it (`ours_err < 0.02`,
   `ours_err > xu_err`).
4. `writeup/4_p2_lottery/p2_route_e_v1_evidence.py` builds `fig34_p2_route_e_v1_spectrum.png`
   from `E1_anchor`, `E2_branch`, `E3_resonance`, `E5_sweep[*].kept_ref` (NOT the unstable
   `kept["0.1"]`), `E8_third_mode`, `E9_essential_edges`.
5. `writeup/README.md`, `PHASE2_P2_NOTES.md` §26, `writeup/data/p2_route_dssx_v1_scoping.json`,
   `writeup/data/bench_boussinesq_silent_corruption_check.json`, `experiments/JOURNAL.md`,
   `DIRECTION.md` — name-only mentions / provenance-index entries; no numeric leaf is extracted.
6. `experiments/journal/leg_254.md`, `writeup/novelty/leg_254.md`, `experiments/journal/leg_287.md`,
   `writeup/novelty/leg_287.md` — historical narrative, not live consumers.
None of these read `E5_sweep[*].kept["<loose tol>"]` (the leaf family that actually reordered)
except `E6_control`'s internal `plain`/`planted` lists, which call the SAME `match_filter` inside
`solver/rescaled_spectrum.py` (out of this leg's territory to touch) at a tight `tol=1e-3` that in
practice admits only the well-separated structural/planted modes — the census recorded no `E6`
mover over 10%, and this leg's regeneration confirms `E6` unmoved beyond noise level. Flagged here
as a residual, out-of-territory risk for a future leg, not evidenced as broken.

**(c) REPAIRED**, inside `experiments/p2_route_e_v1_spectrum.py` only (the allowed generator
file; `solver/rescaled_spectrum.py`'s `match_filter` itself is untouched). A new `canonical_order()`
helper re-sorts `match_filter`'s output by `(round(Re(lambda), 6), -Im(lambda))` instead of trusting
its raw noise-level real part: 1e-6 is far above the observed 1e-11..1e-17 noise floor and far
below any genuine isolated real part this module has ever measured, so the entire noisy continuum
collapses onto one rounded bucket and is ordered purely by (signed) imaginary part — content, not
noise. Applied at both `match_filter` call sites in `e5_sweep()` (the per-tolerance `keeps` dict
and `kept_ref`). Verified deterministic THREE independent ways in this environment: two standalone
`e5_sweep()`-only runs (bypassing the 41-minute pipeline, ~150s and ~132s) plus the full
41-minute regeneration, all three giving the IDENTICAL `E5_sweep[0].kept["0.1"]` array
byte-for-byte. Cross-environment stability is not directly re-testable here (one environment
available) but is the fix's explicit design goal (rounding two orders of magnitude coarser than
the widest noise observed) rather than an untested hope.

**Every consumer's read leaf, diff-checked banked-vs-repaired:**
- `E2_branch` alpha at every `a` moved by <3e-13 relative (float noise from the environment's
  different numpy/OpenBLAS build vs the 2026-08-02 banking environment — same order of magnitude
  as the 287 census's own noise-level movers, nowhere near test_7's `5e-3`/`0.02` tolerances).
- `E7_end.a_c_linear_extrapolation`: `0.6934927291222032` (old) -> `0.6934927291222008` (new),
  2.4e-15 relative.
- `test_literature_gates.py` run end to end against the repaired banked JSON: **`ALL GATES PASS
  (4s)`**, all nine tests, including `test_7_branch_against_xu` and `test_9_artifact_matches_the_
  module`.
- `fig34`'s only touch on the formerly-unstable leaf family is `E5_sweep[0].kept_ref` (the
  `tol=1e-2` list), which both before and after contains exactly the two structural eigenvalues
  `{~0, -1}` in the same order (0 > -1 is never ambiguous) — unaffected by construction, confirmed
  by inspection of both banked files. Rebuilt anyway
  (`writeup/figures/fig34_p2_route_e_v1_spectrum.png`) since the JSON it is nominally built from
  changed, even though no rendered pixel depends on the repaired leaves.
No consumer's verdict, gate, or plotted content moved.

### The ceiling

**Repaired, not merely re-solved: `experiments/p2_route_e_v1_spectrum.py` changed (canonical
ordering, `solver/rescaled_spectrum.py` untouched); `writeup/data/p2_route_e_v1_spectrum.json`
and `writeup/figures/fig34_p2_route_e_v1_spectrum.png` regenerated and re-banked.** 0 other
banked files touched. 0 consumer gate answers changed (`test_literature_gates.py` re-run in full,
passes). This closes 287's exception with a named mechanism and a repair rather than leaving it
as a standing re-solve-not-bytes warning. Clay stays **~0.05%**.

> **Cross-reference annotation (leg 378, ROUTE-LCB6, 2026-08-12) — not a rewrite of this section.**
> §25(a)'s phrase above, "sits on the imaginary axis in exact arithmetic (`Re lambda = 0`)," is the
> theorem-level claim the 367/369/371 trilogy subsequently investigated and downgraded (367:
> UNVERIFIED for the full truncation; 369: not derivable from generic backward-error theory,
> foreclosed; 371, terminal: derivable, but only from LAPACK's specific real-Schur structure, not
> from any generic argument — matches leg 367's four measured points to within 0.93-1.68x via a
> second driver, `scipy`'s `dgees`). `canonical_order()`'s repair itself is UNAFFECTED — see this
> file's new entry below and the inline marker at `experiments/journal/leg_356.md` §2.

---

## §26 — leg 361 (ROUTE-LCB4), 2026-08-12: §25's `VOLATILE_TOKENS` diagnosis fixed at the
instrument; §24's "within-environment nondeterminism" clause corrected

§25 diagnosed, but did not fix (out of that leg's territory), a one-token gap in leg 287's own
census instrument, `experiments/p2_route_epa_v1_census.py`: its `VOLATILE_TOKENS` list contained
`"generated_at"` but not the bare substring `"generated"`, so the single leaf leg 287's
`determinism_control` found differing between two same-environment regenerations — a timestamp
field named `generated` — was misread as content nondeterminism rather than correctly bucketed as
volatile. Leg 361 closed that gap directly: `"generated"` added to `VOLATILE_TOKENS`, confirmed
live against `experiments/p2_route_e_v1_spectrum.json`'s own `generated` leaf (the exact field
§25 traced the false alarm to). While auditing the rest of the list for the same shape of gap
(a suffixed/underscore-bounded token present without its bare root, checked against every
CENSUS family's actual leaf names, not guessed), one genuine sibling surfaced: bare `"seconds"`
was likewise missing (only `"seconds_"`/`"_seconds"` were present), which left
`p2_route_cap_v1_audit`'s own `rows[*].run.seconds` wall-clock leaves — real per-test runtimes in
a NEGATIVE CONTROL family that is supposed to classify PORTABLE — outside volatile
classification; added for the same reason. A planted-control test
(`planted_nondeterminism_control()`, run via `--self-test`) constructs a synthetic pair of "runs"
that differ in BOTH a bare `generated` timestamp AND a genuinely content-bearing numeric leaf, and
confirms the comparator, post-fix, stays silent on the timestamp while still correctly flagging
the real numeric movement (`n_numeric_leaves_moved == 1`, the moved leaf named, not swallowed) —
so the fix closes the false-alarm gap without blinding the instrument to real content
nondeterminism, which was checked, not assumed.

This corrects two pieces of standing prose without deleting them: `experiments/journal/leg_287.md`
carries inline markers, at every site asserting "within-environment nondeterminism" or a "strictly
worse defect than leg 252's," pointing to §25 and to this entry — the original text is left
visible and unedited. §24 above (leg 287's landed CORRECTIONS entry) is qualified by this same
correction: its generalization was framed correctly as applying only to `p2_route_e_v1_spectrum`,
but the mechanism it pointed at for that family included a within-environment nondeterminism
claim that does not hold; §25 already named and repaired the family's REAL defect (eigenvalue
position/sign scrambling under a degenerate `match_filter` sort key, value multisets bit-identical
across regenerations), so no live claim in this repository still rests on the false alarm this
entry closes.

### The ceiling

**One file touched for the fix (`experiments/p2_route_epa_v1_census.py`: two `VOLATILE_TOKENS`
additions plus one new planted-control test, nothing else in the file changed). Zero banked JSONs
touched — no census run, no `writeup/data/*.json` diff.** Re-running the census's own comparator
logic against the banked `p2_route_e_v1_spectrum.json` confirms 0 false-alarm leaves post-fix,
while the planted control confirms the same fixed comparator still trips on genuine content
nondeterminism. `experiments/journal/leg_287.md` corrected in place (inline markers only, no
deletion); this entry is purely additive to `writeup/CORRECTIONS.md`. No solver file touched, no
gate answer changed, no proof or certificate claimed. Clay stays **~0.05%**.
## §27 — leg 355, Route-LCB3: two light corrections, both source-verified at entry, both landed

**Dispatch: leg 355 (Route-LCB3), the accumulator's items (3)-(4).** Both items were
source-verified before this leg was drafted; this leg re-verified both independently rather than
trusting the dispatch. Territory: `experiments/p2_route_bvrr_v1_repair.py` (the one argv list),
`experiments/p2_route_cadx_v1_scope.py` (the one guard path), this entry,
`writeup/novelty/leg_355.md`, `experiments/journal/leg_355.md`.

### 27.1 Item (i) — `experiments/p2_route_bvrr_v1_repair.py`'s `BANKED` registry entry for
`spike1_stepC_gate`: applied leg 335's own flagged fix

Leg 335 (`CORRECTIONS.md` §23) diagnosed but did not itself fix (outside its own territory) that
this registry entry's `argv=["--logged"]` omits `--steps 2500`, silently falling back to
`experiments/spike1_stepC_gate.py`'s CLI default of `400` and producing a spurious "does not
reproduce" reading. This leg applies the one-line fix it flagged:

```python
# before
dict(key="spike1_stepC_gate", artifact="writeup/data/spike1_stepC_gate.json",
     script="experiments/spike1_stepC_gate.py", argv=["--logged"], slow=True,
     calls="RescaledBoussinesq.run(renorm=True), 4 resolution rungs"),

# after
dict(key="spike1_stepC_gate", artifact="writeup/data/spike1_stepC_gate.json",
     script="experiments/spike1_stepC_gate.py", argv=["--logged", "--steps", "2500"],
     slow=True,
     calls="RescaledBoussinesq.run(renorm=True), 4 resolution rungs"),
```

**Verified two ways, both against the untouched banked `writeup/data/spike1_stepC_gate.json`:**

1. The real registry entry, with the fix applied, run through
   `experiments/p2_route_bvrr_v1_repair.py`'s own `rerun_one()` (the per-call differential
   apparatus, pre-repair vs. post-repair `odd_field_x_slope`, backs up and restores the artifact
   itself): completed with `returncode=0`; every compared leaf (`c_l`, `c_omega`, `alpha`,
   `residual`, `cut_omega[*]`, `anisotropy_p90`, …) differs at `rel_diff` in the `1e-13`-`1e-16`
   range, i.e. float64 noise, not divergence. The banked file's sha256
   (`dfe4433cdd54891e3e3bc45b915440b6cc7c573b715f1e1d9e7d1fce150718f4`) is identical before and
   after this run.
2. A direct, lighter re-run — `experiments/spike1_stepC_gate.py --logged --steps 2500` (exactly
   the fixed argv, single implementation, no differential doubling), artifact backed up first and
   restored after diffing — reproduces every one of the four `alpha` values leg 335 already
   reported, to the same digit:

   | run | config | banked `alpha` | this leg's re-run `alpha` | `rel_diff` |
   |---|---|---|---|---|
   | 0 | `n_r=300, r_max=1e5` | `-0.3350763095343765` | `-0.33507630953437806` | `4.64e-15` |
   | 1 | `n_r=450, r_max=1e5` | `-0.33396053473198634` | `-0.33396053473198667` | `9.97e-16` |
   | 2 | `n_r=600, r_max=1e5` | `-0.3367555909794855` | `-0.3367555909794855` | `0.0` (exact) |
   | 3 | `n_r=450, r_max=1e6` | `-0.33619163643975625` | `-0.33619163643975647` | `6.60e-16` |

   `predicate_checks` reproduce exactly: `1_alpha_within_5pct: true`,
   `2_alpha_far_within_10pct: false`, `3_anisotropy_below_0p23: true`,
   `4_resolution_stable_alpha: true`, overall `predicate_pass: false` (on clause 2 alone) — same
   as banked, same as leg 335's own re-derivation. `writeup/data/spike1_stepC_gate.json` was
   copied back from a pre-run reference immediately after diffing; sha256 confirmed identical
   before and after (`dfe4433c…`), `git status`/`git diff` on the file empty throughout.

**Disposition: CORRECTED.** The registry regeneration now reproduces the banked artifact to
float64 precision, both via the harness's own differential apparatus and via a direct re-run.

### 27.2 Item (ii) — `experiments/p2_route_cadx_v1_scope.py`: missing-PDF guard added

Leg 304's evidence script (`experiments/p2_route_cadx_v1_scope.py`) unconditionally computed and
wrote `writeup/data/p2_route_cadx_v1.json` even when `Papers/2505.03091.pdf` (gitignored) was
absent — in that case `verify_quotes()` correctly reported `NOT_AVAILABLE`, but `main()` still
wrote a diminished artifact (`quote_verification.status: NOT_AVAILABLE` vs. the banked
`VERIFIED`) over the real one. Two independent legs' smoke tests (322, 327) hit this and reverted
the accidental rewrite by hand before committing; this leg adds a guard so a third occurrence
fails loudly instead:

```python
def main():
    t0 = time.time()
    if not PDF.is_file():
        sys.exit(
            "[CADX] ABORTING, NOT WRITING %s: %s is absent.  Papers/ is gitignored on "
            "purpose; re-fetch with `bash Papers/fetch.sh 2505.03091` and re-run to "
            "regenerate the artifact for real.  Refusing to overwrite the banked, "
            "quote-verified JSON with a diminished (NOT_AVAILABLE quote-check) rerun."
            % (OUT.relative_to(ROOT), PDF)
        )
    res = { ... unchanged ... }
```

**Demonstrated both branches, per the gate's own requirement:**

* **(a) PDF absent** (this leg's default container state — `Papers/*.pdf` is gitignored and was
  not present at leg start): `PYTHONPATH=. .venv/bin/python experiments/p2_route_cadx_v1_scope.py`
  now exits `1` with the message above, printed to stderr via `sys.exit(str)`. The banked
  `writeup/data/p2_route_cadx_v1.json`'s sha256
  (`75fab364a3b79ecc58129563d12e734810fb10cb54409760cb5d7025e9758e1d`) is identical
  before and after the run; `git diff` on the file is empty. Before this leg's guard, the same
  invocation would have exited `0` and silently overwritten that file with
  `quote_verification.status: NOT_AVAILABLE` in place of the banked `VERIFIED`.
* **(b) PDF present** (normal path — fetched via `bash Papers/fetch.sh 2505.03091`, egress `HTTP
  200`, sha256 `0f1bc6181ce0d4375df3a012846d851c366cfc768b73fbfa3e2f7b6631f8081d`, matching
  `PDF_SHA256` in the script): the guarded script produces output **identical to before this
  leg's change** field-for-field, excluding only the `elapsed_s` wall-clock key (before
  `6.138346195220947`, after `1.1012506484985352` — both real, non-cached runs; not a result).
  `writeup/figures/fig67_route_cadx_v1_zero_diagonal.png` is **byte-identical** (`cmp` clean).
  Both banked files were then restored from the pre-run reference and confirmed byte-identical
  by sha256 and empty `git diff` before this leg's own commit.

**Disposition: CORRECTED.** No regression on the normal path; the hazard that bit legs 322 and
327 now fails loudly instead of silently rewriting the banked artifact.

### The ceiling

**0 numbers re-derived beyond direct reproduction of already-banked/already-flagged facts** — the
`alpha` values are leg 335's own quoted table, independently re-derived to the same digit, not
copied; the CADX guard's evidence is this leg's own fresh runs, diffed against a pre-run
reference. **2 sites edited by this leg** (the one `argv` list, the one `main()` guard), **1
batched entry** (this one). **0 gate answers changed anywhere** — leg 335's
`REPRODUCIBLE_AS_BANKED` verdict and leg 304's `CADIOT_DOES_NOT_COVER_A_ZERO_DIAGONAL` verdict
are both unmoved; neither banked JSON's contents changed, both confirmed byte-identical by sha256
before and after this leg's runs. **0 bans touched**, `plan_of_record.py` and `DIRECTION.md`
byte-identical, untouched by this leg. No link of the `L1 → L4` chain moved. Clay odds stay
**~0.05%**.

## §28 — leg 366, Route-LCB5: three light corrections, each source-verified at entry, all landed

**Dispatch: leg 366 (Route-LCB5).** Three independently source-verified items, applied as
markers/citation-text corrections (not new derivations). Territory:
`experiments/journal/leg_341.md` (marker only, append), `experiments/p2_route_pnrv_v1_postrepair.py`
(the one diagnostic `zip`, nothing else in that file), `solver/dssp_screen.py` (citation text
only, two named locations) plus a re-run of `test_dssp_screen.py`, this entry,
`writeup/novelty/leg_366.md`, `experiments/journal/leg_366.md`.

### 28.1 Item (i) — leg 341's S2 site: grounds correction, width unchanged

Leg 341's S2 discussion (`experiments/journal/leg_341.md`, "the NRS/Tsai composition DISSOLVES")
argued the `u ∈ L³` hypothesis fails at the target's own decay rate, citing that as one of "two
independent grounds" alongside an ansatz (SS-vs-DSS) finding. Leg 359's adjudication
(`experiments/journal/leg_359.md`, `writeup/data/p2_route_l3bd_v1.json`), reading Tsai 1998's
Theorem 2 (the local-energy-estimates route) at full primary text, found Theorem 2's finishing
step needs no `L^q` integrability at all (only `U → 0 at infinity`) and that Tsai's own headline
motivating example (eq. 1.5, p.31) is essentially this repo's target's exact decay rate — i.e.
Theorem 2 **reaches** exactly the decay class leg 341's decay-insufficiency argument relied on.
The decay-based ground is therefore incomplete as stated; per leg 359, the SOLE surviving ground
is the ansatz clause (both Theorem 1 and Theorem 2 are stated only for Leray's exact, continuous
backward self-similar form `(1.2)`, and the screened object is DISCRETELY self-similar).

**A grounds-vs-width correction: the conclusion (`NOT EXCLUDED` / DISSOLVES) does not change,
only which clause supports it.** A blockquote marker was inserted immediately after leg 341's
`**Verdict: DISSOLVES.**` paragraph, citing leg 359's finding verbatim-sourced and pointing to the
ansatz subsection immediately following as the sole surviving ground. Leg 341's original
decay-based paragraph is left **fully intact**, not edited out — the marker is additive only.

**Disposition: CORRECTED (grounds only).**

### 28.2 Item (ii) — `experiments/p2_route_pnrv_v1_postrepair.py`'s `per_row` diagnostic zip:
row-ordering bug fixed, cosmetic-only status demonstrated live

Leg 229 (`experiments/journal/leg_229.md` §5a) flagged but did not fix (out of its own territory)
that `m4_v4_grid_converged_a_max.comparison_to_leg226.per_row` was built by
`zip(v4_rows, t4["rows"])` — pairing this leg's rows (ordered `n` outer / `a` inner) against leg
226's banked table (ordered `a` outer / `n` inner) by **position**, not by key. The two orderings
coincide only at index 0. Fixed here by keying `t4["rows"]` on `(n, a)` explicitly:

```python
"per_row": [
    {"n": m["n"], "a": m["a"], ... }
    for m, t in (
        lambda t4_by_na: ((m, t4_by_na.get((m["n"], m["a"]), {})) for m in v4_rows)
    )({(row["n"], row["a"]): row for row in t4["rows"]})
] if not FAST else "skipped(FAST)",
```

**Demonstrated live, not merely argued**, using the already-banked `v4_rows` (from
`writeup/data/p2_route_pnrv_v1_postrepair.json`) and leg 226's own banked table (fetched via
`git show leg/226-pnr-v1-resume:writeup/data/p2_route_pnr_v1_repair.json`, exactly as the runner
does): the OLD positional zip produces **12 of 15** spurious mismatches (`c_rel_err > 1e-9`); the
NEW keyed-on-`(n,a)` version produces **0 of 15** — matching leg 229's own finding that all 15
`(n,a)` pairs are bit-identical once correctly keyed. The gate's actual verdict/output is
unchanged before and after: `m4_v4_grid_converged_a_max["v11_own_test"]` and `["repaired_verdict"]`
(what `data["gate"]`'s `answer: "YES"` is built from) are computed by `v4_verdicts()` directly off
`v4_rows`, keyed by `r["a"] == a`, and never read `per_row` at all — confirmed identical
regardless of which zip version ran. Only the diagnostic *display* was broken, exactly as leg 229
reported; the banked `writeup/data/p2_route_pnrv_v1_postrepair.json` is left untouched by this
leg (this leg's territory is the script only, not a re-run of the ~40-minute solve).

**Disposition: CORRECTED (the one zip); demonstrated cosmetic, not claim-bearing.**

### 28.3 Item (iii) — `solver/dssp_screen.py`'s T1 citation: re-attributed to NRS 1996

Leg 364 (`experiments/journal/leg_364.md`, `writeup/data/p2_route_nrsv_v1.json`) found that the
module's `deciding_clause` string in `_ledger_nrs_tsai_three_way()`'s `EXCLUDED-BY-T1` branch
(then lines 534–539) and the identical header-comment quote (then lines 364–367) cited Tsai 1998's
Theorem 1 (`q ∈ (3,∞]`, which is **open at 3** and explicitly excludes `q=3`) to justify the exact
`q=3` (`L³`) test the ledger actually runs — but the `q=3` case is NRS 1996's own, earlier,
disjoint result, attested secondhand (NRS 1996 itself remains paywalled/unobtainable after three
independent refusal-to-obtain attempts: legs 253, 359, 364) at two independent obtainable
sources: Tsai 1998, p.30 ("The main result of [NRS] is that the only weak solution of (1.3)
belonging to L³(R³) is U ≡ 0.") and the Bradshaw & Tsai survey, arXiv:1802.00038, p.3 ("...was
excluded in Nečas, Růžička, and Šverák in [35].").

**Both cited locations re-attributed to NRS 1996 with the provenance caveat, citation text
only** — `l3_norm_ladder()`'s operational logic (the exact-cube-norm computation) and every
verdict/reason string were left untouched. Re-ran the full battery after the change:
`python test_dssp_screen.py` → **ALL DSSP-SCREEN TESTS PASSED** (every one of the 19 checks,
including the `EXCLUDED-BY-T1`/`EXCLUDED-BY-T2`/`NOT-REACHED-BY-ANSATZ` three-way controls).
`git status`/`git diff --stat` confirm **no diff on any banked JSON**
(`writeup/data/p2_route_dsspb7_v1.json`, `writeup/data/p2_route_b7x_v1.json`, or any other file
under `writeup/data/`) — only `solver/dssp_screen.py` itself changed, and only at the two named
citation sites.

**Disposition: CORRECTED (citation text only); verdict battery reproduces unmoved.**

### The ceiling

**0 numbers re-derived** — items (i) and (iii) are citation/grounds corrections sourced verbatim
from legs 359/364's own quoted primary-text locators; item (ii)'s demonstration re-derives
`per_row` from already-banked `v4_rows` and leg 226's own already-banked table, live, both ways,
to show the mismatch count collapses from 12/15 to 0/15. **3 sites edited** (one blockquote
marker, one `zip` call, two citation strings in one file), **1 batched entry** (this one). **0
gate answers changed anywhere** — leg 341's `DISSOLVES`/`NOT EXCLUDED` verdict, leg 229's `YES`
gate, and every one of `test_dssp_screen.py`'s 19 checks are all unmoved; every banked JSON this
leg's territory touches is confirmed byte-unchanged (`git diff --stat` empty on all of them). **0
bans touched**, `plan_of_record.py` and `DIRECTION.md` untouched. No link of the `L1 → L4` chain
moved. Clay odds stay **~0.05%**.

## §29 — leg 372, Route-IDXB: the cycle-5 batched evidence follow-up — items 9, 10, 13 dispositioned

`writeup/INDEX.md`'s quartet-gap list carried three items reserved by leg 327's own comment in
`writeup/build_figures.py` for "a later batched follow-up leg": items 9 (Weight-repairs v1), 10
(Route-KA v1), and 13 (Route-M2P v1 + Route-NKR v1). All three are dispositioned here, in
322/327's shape — rebuilt from banked/curated data only, no fresh solves, no banked JSON
touched.

### 29.1 Item 9 (Weight-repairs v1) — ALREADY CLOSED, verified and cited, not re-touched

`experiments/journal/leg_138.md` and `writeup/INDEX.md`'s own item-9 text already record that
leg 138 found `writeup/4_p2_lottery/p2_weight_repairs_v1_evidence.py` landed in commit `9d9b7ea`
(the same commit that created the route, pre-dating leg 108's own pass) — the route has 5 of 5
quartet pieces, not 4. Leg 372 re-confirmed the file is present on disk and runs. Per this leg's
own gate, recreating an already-closed artifact is a duplicate and a FAIL — nothing was written
for item 9 beyond this citation.

**Disposition: CLOSED-WITH-CITATION-TO-EXISTING-CLOSER (leg 138, commit `9d9b7ea`).**

### 29.2 Item 10 (Route-KA v1, leg 61) — E closed with a new artifact; F was never a real gap; BLOG stays open

`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEKA_V1.md`'s own header states, verbatim: "No figure:
this is a known-answer audit and the established convention is that such legs register none."
The gap list's own item 6 already records the same by-design "no measurement, no figure"
convention for Route-D's advection/literature-scope legs, and item 13 below records it again for
Route-NKR v1 — this is the third confirmed instance, not an isolated inconsistency. Leg 372
therefore does not claim a new figure number for this route: this repository's own standing
practice ("legs must not pick their own numbers; integration allocates," `writeup/INDEX.md`'s
in-flight figure-allocation section) is respected, and this leg's dispatch carried no figure
reservation. The `F` cell's `**GAP: none**` mark is corrected to "not a gap — by design."

What IS built: `experiments/p2_route_ka_v1_kawahara_evidence.py` reads only
`writeup/data/p2_route_ka_v1_kawahara.json` (no solver import, no re-run) and asserts 8/8
checks, run live:

```
8/8 checks pass -- Route-KA v1's magnitudes reproduce from
writeup/data/p2_route_ka_v1_kawahara.json alone, no re-run.
```

covering Reading A (CLN's published `r0` is a certified radius of ours — YES), Reading B (the
pre-committed window's shortfall, `3.3531x` / `0.5254` decades, reported at its banked magnitude,
not smoothed), both nominated explanations for that shortfall FALSIFIED at their banked
magnitudes (trace projection explains `1.0252x` of the needed `3.3387x`; the discarded tail is
`2.978` decades short), the resolution sweep (`Y0` flat across `N=60..300`, `r_min_Hl` tracking
`sqrt(2N+1)` almost exactly), and the poisoning control (linear across 8 decades of displacement
scale, fails to close at the largest tested kick).

The BLOG piece remains genuinely owed and is NOT written here: prose is a claim-bearing
write-up, outside this leg's scripts/figures-only remit.

**Disposition: NARROWED (same shape as gap-list item 2/Route-PORT v2) — `E` closed with a new
artifact, `F` corrected from a false gap to "not a gap, by design," `B/T`'s BLOG clause left
honestly open.**

### 29.3 Item 13 (Route-M2P v1, leg 125 + Route-NKR v1, leg 128) — both halves CLOSED with new artifacts

**M2P.** `experiments/p2_route_m2p_v1_promotion_evidence.py` imports no solver module and reads
only `writeup/data/p2_route_m2p_v1_promotion.json`, rebuilding the already-registered `fig61`
byte-identical across two reruns (`sha256sum` match:
`0c44b3554dce1b7da98fc73c70435f3f67cc8c6359cbe842ba5082df5577e6dc` both times). The one
deliberate deviation from the original `build_figure()` (in
`experiments/p2_route_m2p_v1_promotion.py`, which re-solves a Newton iterate live for panel
(a)'s dashed line, because the raw coefficient array is not itself banked in the JSON — only
summary scalars are): leg 372's panel (a) plots ONLY Chen's closed form
`Omega(x) = -2 b x / (x^2+b^2)^2`, evaluating a fixed analytic formula at the banked constant
`b` — not a solve — and annotates it with the banked `n=1201` Newton-reconstruction numbers
(`c_l -> 0.333333435`, abs err `1.02e-07`) as text rather than a re-solved curve. Registered
additively in `writeup/build_figures.py`'s `P2_EVIDENCE` list.

**NKR.** `experiments/p2_route_nkr_v1_repair_evidence.py` reads only
`writeup/data/p2_route_nkr_v1_repair.json`, no solver import, and asserts 6/6 checks, run live:

```
6/6 checks pass -- Route-NKR v1's magnitudes reproduce from
writeup/data/p2_route_nkr_v1_repair.json alone, no solver import, no re-run. No figure
produced, matching the route's own declared 'no curve to plot' convention.
```

covering gate (a)'s false-accept count (`21/105` pre-repair to `4/105` post, `17` rejected by
the repair, `0` clean-input outcomes moved, the remaining `4` a named residual class rather
than a leftover), gate (b)'s zero regression (`4626/4626` comparisons bit-identical,
`worst_ulps=0`, sibling suites all pass), gate (c)'s shared-guard agreement across all three
certificate-assembly modules, and the overall pre-committed answer (`YES` on (b) and (c), `NO`
on (a)). No figure is produced, per the route's own by-design "no curve to plot" header — the
script is therefore NOT registered in `P2_EVIDENCE`, same reasoning as the Route-KA v1 script.

**Disposition: CLOSED-WITH-NEW-ARTIFACT (both halves).**

### The ceiling

**0 banked JSON files touched** anywhere (`git diff --stat` on `writeup/data/*.json` is empty).
3 new evidence scripts (`experiments/p2_route_ka_v1_kawahara_evidence.py`,
`experiments/p2_route_m2p_v1_promotion_evidence.py`,
`experiments/p2_route_nkr_v1_repair_evidence.py`), 1 figure regenerated
(`writeup/figures/fig61_route_m2p_v1_promotion.png`, byte-identical across reruns), 1 additive
line in `writeup/build_figures.py`'s `P2_EVIDENCE` list, `writeup/INDEX.md`'s three named rows
plus their gap-list annotations updated, this entry. **0 gate answers changed anywhere** — every
route's own YES/NO verdict is read verbatim from its existing banked JSON and reproduces
unmoved. **0 bans touched**, `plan_of_record.py` and `DIRECTION.md` untouched. No link of the
`L1 → L4` chain moved. Clay odds stay **~0.05%**.

---

## §30 — leg 378 (ROUTE-LCB6), 2026-08-12: accumulator item (10) applied — leg 356's
`Re(lambda)=0` claim corrected to its earned status, per the 367/369/371 trilogy

**Dispatch.** The DM's accumulator normally batches 2-3 finalized items before applying them
together; this cycle it was amended for the empty-queue case — when the accumulator holds at
least one finalized item and nothing else is dispatchable, the batch fires early rather than
waiting for company (a finalized correction sitting idle is staleness by policy, not discipline).
Item (10), finalized by leg 371 (`experiments/journal/leg_371.md` §7), is the only item in the
queue this cycle. Leg 378 applies it. **Text-only: nothing re-derived or re-measured here.**

**What was corrected, and where.** `experiments/journal/leg_356.md` §2 (and, identically in
substance, `writeup/CORRECTIONS.md` §25(a) — annotated above, not rewritten) stated the
discretized essential/continuum spectrum's pinning to `Re(lambda) = 0` as settled fact ("in exact
arithmetic"). An inline `[CORRECTED 2026-08-12 by leg 378 …]` marker was inserted directly after
the original sentence in `experiments/journal/leg_356.md` §2, quoting that original wording in
place (not deleted), recording the corrected status: **UNVERIFIED as a theorem for the full
truncated matrix (leg 367) — NOT derivable from generic backward-error theory, that route tried
and foreclosed (leg 369) — but IS derivable from LAPACK's specific real-Schur numerical structure
(`dlanv2.f`'s shared 2x2-block half-trace plus the Ahues-Tisseur local deflation criterion), NOT
from any generic argument, independently reproduced via a second driver (`scipy.linalg.schur` /
LAPACK `dgees`) matching leg 367's four measured points to within a factor of 0.93-1.68x (leg
371, terminal).** `canonical_order()`'s repair itself needs only the empirical floor below
`1e-6`, which the trilogy leaves untouched and re-confirmed — no gate answer, no repair, and no
consumer verdict for the E5 family moves as a result of this correction.

### The ceiling

**One marker inserted at one site (`experiments/journal/leg_356.md` §2, inline, non-deleting),
one non-destructive cross-reference annotation added to §25 above (its own content untouched),
this one batched entry appended to `writeup/CORRECTIONS.md`.** 0 other files touched. 0 banked
JSON files touched or read-write (all read-only throughout). `plan_of_record.py` and
`DIRECTION.md` untouched (off-limits to this leg). This closes the accumulator: item (10) is
applied: item (11) opens only whenever a future leg flags the next correction — not this leg's
concern. Clay stays **~0.05%**.

---

## §31 — leg 379 (ROUTE-LCB7), 2026-08-12: two light corrections to permanent regression
suites, each narrowed with a planted-failure control per the 361 lesson

**(i) `test_boussinesq_postrepair.py` — `check_banked_record_carries_no_out_of_domain_coefficient`
narrowed to acknowledge leg 185's self-flagged negative-`nu` diagnostic rows.** The check scans
every banked JSON for a key named `nu`/`kappa`/`nu_crit`/`nu0`/`nu_c` and asserted none was
outside `[0, inf)` in a `scientific_measurement`-bucketed file. Two banked files were tripping
it: `writeup/data/p2_route_m2sd_v1_diagnostic.json` (leg 185, Route-M2SD, 11 rows) and
`writeup/data/p2_route_nu12_v1_converge.json` (leg 284, Route-NU12, its grid-refinement
continuation, 284 rows) — 295 rows total, matching the check's failing `n_recorded_coefficients_
out_of_domain`. Both files' `nu` is the recovered diffusion coefficient of a Newton continuation
on `solver/dissipative_profile.py`'s STEADY profile equation, explicitly self-flagged in leg
185's journal (§D5: *"The negative rows DOWNGRADED TO SIGN-ONLY... only sign banked"*) —
**not** a `solve_boussinesq(nu=..., kappa=...)` coefficient at all; grepping both producing
runners (`experiments/p2_route_m2sd_v1_diagnostic.py`, `experiments/p2_route_nu12_v1_converge.py`)
for `solve_boussinesq` returns zero hits, so a negative value there cannot be defect 2's
call-site contamination reaching a Boussinesq run. The check now re-derives the full
out-of-domain list itself (the existing scanner in `experiments/p2_route_bob_v1_postrepair.py`
caps its reported examples at 10 per key, too few to name and exclude by file) and asserts the
excused set is **exactly** these two named files — no third file may silently start relying on
the exclusion — with everything else still required clean. **Planted-failure control added and
demonstrated to trip**: the shipped control
(`check_CONTROL_narrowed_scan_still_catches_a_planted_out_of_domain_coefficient`) plants a
synthetic `nu = -0.42` in a third, unexcused scratch file on every run and asserts the narrowed
scan still reports it as unexcused — confirmed passing (see `experiments/journal/leg_379.md`).

**(ii) `test_gclm_postrepair.py` — `check_banked_stage1_5_t_stars_are_unmoved` replaced its
bit-identity (`float.hex`) pin with a documented ULP tolerance.** Under this suite's current
environment (numpy 2.5.1), 2 of the 20 banked production T* values fail bit-identity with no
`solver/gclm.py` change and no thread-count sensitivity (reproduced identically with
OMP/OPENBLAS/MKL/NUMEXPR/VECLIB threads all pinned to 1): `bump(kappa=2)` moves 3 ULP and
`bump(kappa=5)` moves 12 ULP (`np.spacing`-defined), both through `clm_analytic_blowup_time`'s
`np.fft.rfft`/`irfft`. This is a library-version FFT-kernel drift, not a repair regression — the
same shape as two existing precedents in this repo: leg 147 (Route-NKB) measured 20 of 22 leaves
moving at <= 3 ULP from a numpy-version FFT/reduction-order change with banked totals otherwise
exact (`experiments/journal/leg_147.md`), and leg 131 measured 1-2 ULP BLAS reduction-order
drift on the same kind of re-run (`experiments/journal/leg_131.md:128`). The check now asserts
each computed T* is within `ULP_TOLERANCE = 25` ULP of its banked literal (>= 2x the 12 ULP
worst actually measured, and ~13 orders of magnitude tighter than G1's own real defect, which
saturated at a *relative* 1/3). **Planted-failure control added and demonstrated to trip**:
`check_CONTROL_ulp_tolerance_still_catches_a_planted_deviation` plants a synthetic banked value
displaced by `2 * ULP_TOLERANCE` ULP from a live-computed T* and asserts the same
`<= ULP_TOLERANCE` comparison used by the real check rejects it — confirmed passing.

Both planted controls were run and shown to trip (see `experiments/journal/leg_379.md` for the
verbatim failing output captured before the exclusions/tolerance were finalized). No planted
control was widened after failing to trip; neither did.

### The ceiling

**2 test files edited** (`test_boussinesq_postrepair.py`, `test_gclm_postrepair.py`), both
additively (new helper functions, new `check_CONTROL_*`/`test_CONTROL_*` entries, and one
narrowed assertion body each — no existing check deleted or weakened beyond the documented
narrowing/tolerance). **0 banked JSON files touched** (`git diff --stat` on `writeup/data/*.json`
is empty; `p2_route_m2sd_v1_diagnostic.json` and `p2_route_nu12_v1_converge.json` are read-only
citations, unedited). **0 solver files touched.** `test_boussinesq_postrepair.py`: 16/16 checks
pass. `test_gclm_postrepair.py`: 9/9 checks pass. `test_plan_of_record.py` and
`test_capabilities.py` (the merge gate's always-on pair) both pass unchanged. **0 gate answers
changed anywhere** — leg 133's and leg 103's own YES verdicts are untouched; this leg only
repairs the regression suites that bank them. `plan_of_record.py` and `DIRECTION.md` untouched.
No link of the `L1 → L4` chain moved. Clay odds stay **~0.05%**.

---

## §32 — the W3 wording ruling of 2026-08-18: leg 174's `the_empty_cell.meaning`, correction record

**Class, stated first.** This is an over-read closure of the register's kind: **the measurement
stood, the sentence written about it did not.** Leg 174's occupancy matrix returned `0` in the
`fluid=True, grade=A` cell and said so *"for want of a target, not a method"* — that count was of
what leg 174 had screened, and it was honest. The banked **meaning** field went further than the
count and asserted a fact about the published literature. That assertion is now false.

**The field, named exactly.** `writeup/data/p2_route_vbs_v1_scoping.json`, key
`the_empty_cell.meaning`. **It is NOT edited, and it will not be.**

**The measurement that falsified it.** `V3` (leg 399, `16ba44e`, `writeup/data/p2_route_v3_gradeA_v1.json`,
`experiments/journal/leg_399.md`) graded 9 candidate computer-assisted proofs against **leg 174's own
two clauses, applied unchanged**, having been told explicitly not to tighten them. One row passes
both: **`arXiv:2509.25116` (Hou–Wang–Yang)** — interval arithmetic at §7.3, p.55, enclosing a
solution of a system carrying `−ΔŨ` (Prop. 1, eq. (1.15), p.5), for the **unforced 3D incompressible
Navier–Stokes equations** (eq. (1.1)). The other 8 rows are `NO` with the failing clause quoted. It
**had never been graded here**. The YES is **UNVERIFIED and UNAUDITED** — one database,
title-screened, Semantic Scholar banked as a **gap, not a zero** (no key in this environment) — and
the ruling makes the adversarial full-text audit **obligatory in wave 6**.

**The unit that made it, and the behaviour that is being protected.** `V3` recorded the YES **first
and unsoftened**, with the disqualifying qualification beside it. The ruling's second reason for
letting the prose test govern is about exactly that: *"Letting the predicate redefine the wall would
convert that honesty into a wall-break it does not support; tightening the predicate after seeing the
row it admitted would be the mirror error."* Neither happens here. Leg 174's predicate stays exactly
as leg 174 wrote it and **stops being described as W3's test**.

**What this entry does NOT do**, per this file's own rule and per the ruling. It does not withdraw
`V3`'s YES. It does not restore ~~*"leg 242 confirms nobody filled it since"*~~, which stays struck.
It does not make the cell empty: **on leg 174's own definitions the cell is OCCUPIED, and W3 is true
anyway.** It does not lift a ban, promote a route, or open anything. **"Not what we said" is not
"open."**

### The ceiling

**0 banked JSON files touched** — that is the point of the entry, not an aside. `WALLS.md` (W3
retitled, old title struck not deleted, the ruling's required paragraph placed beside it),
`STATE.md`, `OPTIONS.md` and this file carry the correction; the artefact carries none of it.
**No link of the `L1 → L4` chain moved.** The ruling says so itself: it moved wording and a queue.
Ceiling **TIER 2**. Clay stays **~0.05%**.

## §35 — `V-W5`'s three defects: a post-hoc pass-criterion, a basis-dependent constant quoted as if portable, and a ratio half-scraped from prose

**Unit** `V-W5` (leg 403), verifier of wave 5, which it did not plan. **Repaired: none.** A verifier
that repairs destroys the evidence of the defect, so it was told to record and stop, and it did.

**D-VW5-1 — the pass-criterion is post-hoc.** `L5`'s control `C6` (cutoff basis: degree-9 C⁴
smoothstep against leg 381's quintic C²) **was planted to fire and did not**: `2.03e-02` against the
pre-committed tolerance `1e-02`. **The tolerance was NEVER moved** — `git log --all -p` over the
driver returns three C6-tolerance diff lines across every ref, **all three `+` lines, no `−` line
exists**, and the literal is `1e-2` in all three (introduced `347676f`, 2026-08-18 16:25). I checked
this myself rather than on the unit's report. **But** a second criterion, `fired_on_tail3_fit`, was
**added at the LANDING commit `4be46ef` (16:59) — after the failure was known** — and it passes, on
the narrower tail-3 window where the two bases agree to `5.408e-05`, `185×` inside tolerance. The
honest statement: **the pre-committed control failed and a post-hoc one passed.** Nothing about the
gate `NO` depends on it.

**D-VW5-2 — the constant is basis-dependent by `1.476×`.** `c_mod = 869.288` per unit similarity
time is quoted unqualified in `L5`'s gate block. It moves by a factor **`1.47604`** between the two
cutoff bases. **The EXPONENT is basis-independent and the `NO` rests on the exponent**
(`+1.085e-04`, threshold-free), so the verdict is untouched — but this narrows `c_mod`'s reach
**further than §34 already did**: it is not route 4's number *and* it is not basis-portable.

**D-VW5-3 — half of `0.9958` is scraped from prose.** The `E` side of the cost ratio is
banked-row-derived (`32718.334 s / 16` attempts). The `U5` side (`0.0713` wall-h × 8 workers) is
**in no banked JSON** — it is regex-scraped from `experiments/journal/prog_r4_u5.md:405`. **Changes
nothing**: the banked-rows-only route gives `95.389` s/epoch against the banked `95.0`, ratio
`1.0041`, same conclusion. It is a **provenance** defect, and the standing rule it violates is
*re-derive from `writeup/data/*.json`, never from prose*.

**Conductor's own re-run, recorded for the audit trail.** I integrated on the fast path
(`--no-quad`, EXIT 0) plus my own mutation test (exponent perturbed in the 13th digit inside the
worker's worktree, restored after: EXIT 1, naming both the bit-pattern and the `self_hash` check).
The **expensive path finished afterwards and agrees**: `quadrature re-run: ON` → *ALL FIVE ITEMS
REPRODUCE*, 8 notes, 0 repaired, **EXIT 0**. Nothing in the verdict changed; the difference between
the two runs is the single note saying the quadrature was skipped.

**What `V-W5` verified, and what it did not.** Verified: `L5`'s `NO` and `ρ`-exponent
`0.00010850007559945518` (bit-for-bit, including a **full float64 quadrature re-run**, not just a
re-fit of banked rows); the three positive controls (`−0.2498`, `−0.5996`, `−2.000005`, each
recovering what it planted); both `self_hash`es; `D-REPAIR`'s epoch correction and the `0.9958` cost
model. **Not verified — and it must not be read as verified:** the SCIENCE. A reproduction validates
**arithmetic**. `L5`'s object is still the **SYNTHETIC** stand-in (§34), the tier is still **Tier 2**,
and **no `L1→L4` link moved.**

## §36 — `V5`'s audit of `arXiv:2509.25116`: four broken constants that do not break the certificate, and one defect of the unit's own

**Unit** `V5` (leg 402), the adversarial audit made **obligatory** by user ruling Q4. Both gate
clauses were answered **separately**, as the ruling required.

**CLAUSE 1 — the certificate CLOSES (branch `B1-PARTIAL`).** The enumeration was **frozen before
adjudication** (commit `548b9af`, 20:22, against the clause-1 verdict at `8bcdee0`, 20:31): 22
Class-A interval-arithmetic inputs, 24 Class-B recomputable constants, 8 Class-C structural. All 24
Class-B were re-derived at 50 dps **from Class-A inputs alone**. The localisation step (Remark 2,
§1.3 with §2) was checked at full text across twelve links: **no gap**.

**The four that fail, both numbers each:**

| id | what | printed | recomputed at 50 dps | direction |
|---|---|---|---|---|
| `H28` | coefficient in the reduced `M_4^U`, which *is* `4ε^U` | `2.8e-6` | `2.6e-6` | conservative |
| `H30` | `x_0^U` | `1.44e-5` | `1.45054706437e-5` | **NON-CONSERVATIVE** |
| `H32` | `y_0^U` | `1.3e-7` | `1.30549235793e-7` | propagated |
| `H33` | `y_1^U` | `4.8e-7` | `4.82306898903e-7` | propagated |

`H30` is the substantive one. The failing clause, character-exact from `main.tex:2278-2280`:
`0.25 - 0.199 - 0.005 + \sqrt{0.002}` — `η₂ = 0.005` stands where the certified bound
`M_2^U ≤ 0.0061` belongs. **Carrying the corrections through the whole chain, closure survives**:
`M_4^v = 0.0210567838661 ≥ 0.021` and `|λ| = 0.00426280601272 ≤ 0.0045`. But `x_1^U` clears its
bound by **0.08%**, and `V5` recorded that as **luck, not margin** — the right call.

**WHAT THIS AUDIT DID NOT ESTABLISH, banked as limits and never as passes:** the 22 Class-A
interval-arithmetic outputs were **not verified** (unrecomputable by design here); the Julia
certification was **not re-run**; **W3's prose test was not run, so W3 does not move**; and **no
`L1→L4` link moved.**

**CLAUSE 2 — the profile IS genuinely 3D, answered standing alone.** Not folded into clause 1, per
the ruling. Detail and the scope question it raises: `WALLS.md` W2 and
`writeup/escalations/ESCALATION_W2_SCOPE_2026-08-18.md` (**recorded, NOT ruled**).

**THE SECOND DELIVERABLE — wave 4's repair, `_v1` UNTOUCHED (ruling Q3).** Re-issued as deltas:
`p2_route_v3_gradeA_v2.json` (`6322309acc4d8bf8`, discharges `D1`–`D4`) and
`p2_route_l2_decay_v2.json` (`9a58a36c81734066`, discharges `D5`/`D6`/`N1`). Both carry
`supersedes` and a `correction_record` pointer to §33; both self-hash correctly; the Conductor
confirmed **no `_v1` file was edited**. Re-anchoring the quotes against the authors' own LaTeX
e-prints showed **`D3`'s `non- linear` was a pdftotext artefact** and **`D4`'s "in INTLAB" was a
splice of two sentences eleven lines apart**. Two further defects §33 does not name (a double
space, an upper-cased `INVISCID`) were **flagged in a dedicated field rather than silently merged**
— the correct handling.

**⚠ D-V5-1 — A DEFECT OF THE UNIT'S OWN, FOUND BY INTEGRATION AND NOT BY THE UNIT.**
`experiments/p2_route_v5_v1_evidence.py` imports **`mpmath`**, which was **not in
`requirements.txt` and not in the repo venv**: on a clean checkout it exited **3**, not 0, until
the Conductor installed it. **Lesson 68 — a check nobody can execute decays into a claim.** Fixed
at integration by adding `mpmath>=1.3` to `requirements.txt`. The unit's own sanity report said the
script "exits 0", which was true **in its worktree** and false in the repository it shipped to.
**The rule this makes explicit: an evidence script must run in the environment `requirements.txt`
describes, and a unit that adds a dependency must add it to that file.**

**What the Conductor checked mechanically, not on the unit's report:** territory (5 files, all
additions); the pre-registration `eb756b1` predates the paper fetch and names W2's test, so the
test was **located before adjudication**; the evidence script **EXIT 0 on 75 checks** once the
dependency was installed; a **Conductor-run tampering test** (swirl set to zero) **EXIT 1**,
failing in three independent places — `self_hash`, the swirl-fraction re-derivation, and `L2`'s
consistency; and all three `self_hash`es recompute.

## §33 — `V-W4`'s six defects and `N1`: the correction RECORD for wave 4, artefacts untouched

**Recorded 2026-08-18 at wave 5's integration. Ruling Q3 governs: a correction RECORD, and the banked
artefacts are NOT edited.** `V-W4` (`b46ee4d`, `writeup/data/p2_verify_wave4_v1.json`, `self_hash`
`e0171ac1e855f90e`, recomputed independently by the Conductor) reproduced **all five** of its gate
items and located **six defects plus one note**, none of which changes a verdict or a number. The
authoritative list is that artefact's `discrepancies_first_and_unsoftened` and
`experiments/journal/verify_wave4.md`; this entry exists so the record names them where a reader of
the corrections file will find them, and so the **repair unit wave 6 owes** has a scope.

| id | site | what is wrong | what it does NOT change |
|---|---|---|---|
| **D1** | `p2_route_v3_gradeA_v1.json`, row `R7` (`2509.14185`), `failing_clause_quoted` | *"stringent"* dropped from a field presented as **verbatim** | the `NO` verdict — NIL |
| **D2** | row `R6` (`2208.09445`) | attribution: the second failing clause is verbatim but describes **prior work [69]**, not the paper's own construction | the verdict — the **first** clause is the paper's own voice |
| **D3** | row `R5` (`2305.05660v3`) | *"linear"* banked where the paper has *"non- linear"* (a `pdftotext` hyphenation) | NIL. **`V-W4`'s own first-pass extra claim here was WRONG and it withdrew it against itself** |
| **D4** | row `R3` (`2605.15149v1`), supporting evidence | inserted *"the"*; *"in INTLAB"* is not the paper's phrasing; the paragraph is at **p.71**, not *"~68"* | the verdict — NIL |
| **D5** | `p2_route_l2_decay_v1.json`, row `T2c` | the citation carrying the load-bearing row points at ESŠ *Backward uniqueness* (ARMA 169), which contains **no NS regularity criterion**; the paper that does is ESŠ *Russian Math. Surveys* **58** (2003) | **the pin at `α = 1` still holds** — through the **local** suitable-weak-solution form (Seregin, `arXiv:math/0510396` §1), see `WALLS.md` §W4 |
| **D6** | same artefact, `the_pin` | *"restated **independently** by Pineau–Vicol"* overstates: PV state it for **rotated globally self-similar** solutions, not DSS, and both routes terminate at ESŠ — independent **authors**, not an independent **proof** | the pin — see D5 |
| **N1** | same artefact, `326.875` per decade | **amplitude-dependent**: a unit-amplitude model gives `4π ln10 = 28.935`. The **log-divergence** reproduces independently; the **number does not travel** | the divergence, which is what the bill rests on |

**Also recorded, and NOT a defect:** ESŠ 2003 is **journal-only and `UNREACHABLE` at primary here**.
It is banked as `UNREACHABLE`, **never as a zero**, and `read-do-not-contact` binds.

### The ceiling

**0 banked JSON files touched.** `WALLS.md` §W4 carries the D5/D6 provenance correction in the live
wall text; the artefacts carry none of it, and the per-field repair is a **wave-6 unit**, not a
passing edit. **No link of the `L1 → L4` chain moved.** Tier 2. Clay stays **~0.05%**.


## §34 — `L5`'s gate deviation: a pre-committed gate that named an object which does not exist

**Recorded 2026-08-18, after the wave-5 integration commit `e42e7ab`, by the Conductor against its own
audit.** The gate was written by me. It required the measurement *on route 4's banked discrete profile*.
**Route 4 has no banked discrete profile**, and `L5` said so in its artefact rather than quietly using
something else: `route_4_has_no_banked_profile = True`, evidenced at `experiments/journal/leg_382.md`
line 174 and `leg_397.md` §1. It then measured on leg 381's **banked synthetic** exactly-DSS
divergence-free poloidal field, reproducing leg 381's own `ρ`-exponents to `1.996e-12` (control `C1`).

**The `NO` is unaffected**, because the `NO` is threshold-free and rests on an **exponent** —
`0.0001085`, i.e. zero — not on a constant. What is affected is the reach of the constant:
`c_mod = 869.288` per unit similarity time is **that synthetic profile's** number, not route 4's.

**What this changes about how I write gates:** a gate may not name an artefact without the Conductor
having checked that the artefact exists. Wave 6's `L6` exists to remove the deficiency itself.
**0 banked JSON files touched. No link of the `L1 → L4` chain moved.**

## §37 — the Conductor's own retirement splice: a section moved by SEARCHING FOR ITS TITLE, when the title also lives in every pointer to it

**Whose defect.** Mine, the Conductor's. Found and repaired 2026-08-19, one day after it was made.
No unit is implicated and no measurement was touched.

**What happened.** A §3j retirement in `reports/ORCH_STATE.md` located its insertion point with
`txt.index(marker)`, where `marker` was the retired section's own title. **The first match was not
the section — it was a POINTER SENTENCE in the live block that names the section it points at.** The
retired block was therefore spliced into the middle of a live paragraph. Three consequences, none of
which raised an error: the wave-6 paragraph was cut in half; a mangled heading appeared, welded to
the sentence it had landed inside; and — the one that actually mattered — **the current headroom
table and the whole open-escalations list ended up BELOW the superseded boundary**, where a reader
following the file's own convention would have read them as retired.

**Why it is worth a numbered entry rather than a note.** Nothing was deleted, so no diff review
would flag data loss, and the file still parsed as markdown. The damage was *positional*: live
material silently reclassified as superseded. **In a file whose entire function is to tell the next
session what is still live, mis-filing is indistinguishable from lying.** This is the retirement
mechanism's failure mode in general, and §3j prescribes retirement everywhere.

**The rule, stated so it can be followed mechanically.** **Retire by SLICING THE SECTION between
asserted line indices; never locate it by searching for its title.** A well-maintained file
guarantees the title appears more than once — once as the heading, and once in every pointer that
sends a reader to it. The better the cross-referencing, the more reliably a title search finds the
wrong occurrence. Assert the boundaries (`assert L[i].startswith(...)`, `assert L[j].startswith(...)`)
so a shifted file fails loudly instead of splicing quietly.

**Repair.** Restored by line-index slicing with asserted boundaries: the pointer's truncated opening
backtick was put back, the mis-placed block was moved below the superseded boundary, and the live
headroom table and escalations list were returned above it. Verified by re-reading the heading list.

**A second-order point the repair made obvious.** The same trap catches *size measurement*:
computing a live-block length as `len(t[:t.index('## Superseded')])` returns the offset of the first
POINTER to a superseded section, not the boundary — 540 bytes against a true 8,008 on the file as it
stood. **Measure the block by line index too, or the cap check silently passes.**

## §38 — The Conductor's `L6` landing audit: the finding is real, three supporting numbers overstate it, and two stronger facts were sitting unused in the same artefact

**Recorded 2026-08-19, on `V-W6`'s ruling (leg 407, `writeup/data/p2_verify_wave6_v1.json`), every
number below re-derived by me from `writeup/data/p2_route_l6_profile_v1.json` rather than taken from
the verifier's word.** `V-W6` was briefed to scrutinise my own landing audit; it did, and this is
the result. The audit is `writeup/waves/WAVE6_CLOSE.md`.

**What stands.** *"At every rung above the coarsest, the reported `ρ` is attained by exactly one
start — the continuation."* **UPHELD on both branches**, confirmed independently twice. On my own
recompute the minimum at `n_dof` = 576, 1800, 2400 and 6720 is the `continuation` start on branch A
and on branch B, at every one. `L6` does not report this anywhere. It is the audit's genuine find
and it is what forced the re-rank to `L6-b`.

**Overstated, three times, all in the same direction — the rhetoric ran ahead of the arithmetic.**

1. *"Five independent random seeds land 10–24× higher."* The band is right only for **branch B's
   top two rungs**. Recomputed branch B: 3.93–4.02× at `n_dof` = 576, 8.04–11.35× at 1800,
   10.08–11.29× at 2400, 18.32–23.67× at 6720. **On branch A the factor never reaches 10× at any
   rung** (1.01–1.04, 2.55–2.62, 2.58–2.62, 5.36–5.95) — at the first refined rung the seeds are
   within 4% of the continuation, i.e. essentially tied. The top of the range was quoted as the
   range, and one of the two branches does not support it at all.
2. *"And get monotonically worse as `n_dof` grows."* True of the per-rung **minimum over seeds**
   (6.680 → 13.470 → 16.355 → 29.567) and of three seeds individually; **false for `seed402` and
   `seed403`**, both of which fall at the third rung. True as written only under a reading the
   sentence does not state.
3. *"All 133 starts capped at 800 iterations."* **133 of 133 hit their cap** — that part is exact,
   and I re-counted it: every start carries `hit_maxiter = true` and `status = 1`. But only **58**
   were capped at 800 (the gate-bearing joint ladder); the other **75** were capped at **250**, the
   artefact's own `maxiter_on_the_secondary_axis_ladders`. Imprecise, not wrong.

A fourth, minor: the `J4` seed range is **29.567–38.197**, not "32–38" — a slip that *understates*
the spread.

**Wrong once, and conservatively.** I wrote that an interval/NK enclosure needs a residual small
enough for a contraction to close and that this one is *"1.6 against a unit-normalised field"*.
**1.6 is branch B, and branch B is not the unit-normalised branch.** Branch B pins the far-field
angular amplitude to 1; its Gaussian-weighted interior `L²` is 0.0021915332982833375, **0.22% of
branch A's**. The unit-normalised branch is **A**, `weighted_L2_total = 1.0000000000`, residual
**7.583387202236438** — which my own recompute confirms is branch A's banked minimum. **`L7` is
blocked harder than the audit said, not less.** The unit disclosed the asymmetry at its §10 reading
(c-3); the audit did not carry it.

**Understated twice, and this matters more than the overstatements.**

- **The audit conceded ground it did not have to concede.** It wrote that the cap sweep (50→800)
  *supports* `L6`'s claim against the iteration-budget hypothesis. **It does not.** `V-W6`
  re-derived the whole `by_cap` block: it is `residual_at_cap()` taking the minimum over recorded
  trajectory points with `k ≤ K` — a **post-hoc truncation of the same 800-iteration runs** — and
  each rung's continuation start was warm-started from the previous rung's **full-budget**
  minimiser, so the truncated columns still carry the full budget from below. `J1` at "cap 50" reads
  3.2798, a truncation of a run seeded from `J0`'s 800-iteration answer; `J0`'s own cap-50 value is
  14.0239. **`verdict_is_stable_in_the_cap = true` is not a control on the budget at all**, and no
  evidence check touches it. Refusing §8.2's sentence was right; the reason available was stronger
  than the one given.
- **The audit never mentioned that the banked minimiser is not a stationary point in any sense.** At
  the reported `ρ` the scale-invariant gradient is **153.22** against a **pre-registered `gtol` of
  `1e-12`** — about fourteen orders — and it **grows monotonically with `n_dof` on both branches**
  (B: 23.05, 24.06, 60.11, 153.22; A: 1.16, 1.75, 3.11, 16.12). I re-read these per start and they
  are exactly as `V-W6` states. A ladder whose iterates get *further* from stationarity as they
  refine is a stronger statement of the audit's own thesis than the seed spread is, and it was
  banked per start, in the same artefact, unremarked.

**What does not change.** The gate answer. `ρ = 1.613811231995397` and
`decreases_under_refinement = NO` are correct and re-derivable; `V-W6` re-synthesised `C18` to
`1.613811231995` exactly and reproduced both rates with an independent non-numpy OLS. **No
arithmetic defect exists anywhere in wave 6.** The consequence drawn — that `NO` cannot yet be read
as a statement about the ansatz — **stands, and is better supported by `V-W6`'s evidence than by my
own argument for it**: three independent facts force it, and any one of them alone would.

**The lesson, stated so it binds later units and me.** *When the supporting numbers are banked per
start, quote the recomputed range, not its top; and read the whole artefact for the fact that makes
your case, because it was already there.* Both understatements were fields in the same JSON the
audit was written against.

**Repair.** None to the record: no banked number changes and no verdict changes. This entry is the
repair. `D-VW6-7` — `requirements.txt` declaring scipy "intentionally NOT required" while
`experiments/p2_route_l6_v1.py` imports `scipy.optimize` and `scipy.special`, so `L6`'s evidence
script dies with an uncaught `ImportError` on a clean checkout — **is repaired in the same commit**.
The other ten `V-W6` defects are recorded, unrepaired, in its artefact.

### §37, ADDENDUM — 2026-08-19: the same defect fired again, on TABLE ROWS, and was caught before the commit

Refreshing the §3j headroom table in `reports/ORCH_STATE.md`, I set the row for each file by
`line.startswith('| `WALLS.md')` **without stopping at the first match**. `reports/ORCH_STATE.md`
carries **four historic headroom tables** below its `## Superseded` boundary, and every one of them
has a `WALLS.md` row. All four were silently overwritten with today's numbers — including one whose
cap column then read `32,476 | **32,600**`, an arithmetic impossibility that is the only reason I
looked. **Retired history had been rewritten to agree with the present.** Repaired before the commit
by restoring the whole superseded section from `HEAD` and diffing it line by line; the four rows are
back to 32,233/535, 32,233/535, 32,768/168 and 32,768/46.

**The rule generalises, and this is its second firing.** §37 says: locate by asserted line index,
never by searching for a title. The addendum: **when a mechanical edit must search, assert the match
COUNT before writing** — in a file that keeps its own history, every string you can search for
appears once per historic copy, and an edit that "fixes them all" is a falsification of the record,
not a tidy-up. A live-block edit must never touch a byte below the boundary.


---

## §39 — the `~1.2 GB` figure was never a measurement: a counterfactual copied onto the files it was contrasted with, and it propagated into two of my own documents

**Found by:** `R-bank` (leg 404, `8019c35`), as its `defects_found.D1`. **Sharpened by:** CONDUCTOR at landing. **Files corrected here:** `OPTIONS.md` (live). **Files given a correction beside, NOT edited:** `writeup/waves/WAVE7_PLAN.md` §A, `experiments/programme_r4/.gitignore`, `reports/ORCH_STATE.md`'s superseded block, `writeup/data/p2_r_bank_v1.json`, `experiments/programme_r4/seedbank/manifest.json`, `experiments/programme_r4/r_bank_build.py`, `experiments/programme_r4/u5_reduce_library.py`.

**The claim.** `experiments/programme_r4/.gitignore:1-2` reads *"Large binary artefacts of the T=1e5 DNS: regenerated by `u2_m2_dns_recurrence.py --stage dns`, never committed (~1.2 GB)."*

**The measurement.** `u2_dns_ckpt.npy` is **36,864,128 B**, `u2_dns_feat.f32` is **232,000,128 B**, total **268,864,256 B = 268.9 MB**. The header overstates by **4.5×**.

**Why this is worse than an arithmetic slip, and better than it looks.** `experiments/programme_r4/u2_m2_dns_recurrence.py:127-136` is explicit, in `U2`'s own comment: storing all 400,000 snapshots as float32 *"would need ~1.2 GB and this machine has 1.5 GB free"*, so the archive written instead is features-plus-checkpoints and *"benefit is ~280 MB instead of ~1.2 GB."*

So **`1.2 GB` is the size of the archive `U2` deliberately did not write.** The `.gitignore` header, written later, attached the counterfactual to the two files it actually lists — which are the ~280 MB archive. The failure mode is **transcription of a rejected alternative as the accepted one**, not a mis-multiplication. And `U2`'s own `~280 MB` estimate is right: it agrees with the measurement to **4%**. The repository has held the correct number since `U2` was written and quoted the wrong one for months.

**How far it travelled.** Into `WAVE7_PLAN.md` §A (mine, the dispatch brief for `R-bank` itself), into `OPTIONS.md`'s `R7` row (mine), and from there into `r_bank_build.py`, `seedbank/manifest.json`, `u5_reduce_library.py` and `reports/ORCH_STATE.md`. `R-bank` reproduced it in its own artefact *and then measured it and reported itself* — which is the behaviour the discipline is for.

**What is NOT affected.** The argument every one of those documents was making. 268.9 MB is still **365×** the 737,408 B seedbank, still gitignored, still **3.44 h** to regenerate (`u2_dns_meta.json`: 12,379.47 s). `R-bank`'s premise held exactly as stated; only its magnitude was wrong.

**The rule applied, and why it differs by file.** A **banked datum gets a correction beside it, never an edit** (W3 ruling Q3) — so the `.gitignore` line, the two JSON artefacts, the two scripts and the retired ORCH block stand verbatim with `R-bank`'s correction record appended in `.gitignore`. A **committed pre-dispatch record** is the same kind of object: `WAVE7_PLAN.md` §A gets an appended correction, not a rewrite, because the whole value of a pre-committed gate is that it cannot be revised after the answer. **`OPTIONS.md` is a live ranking document** whose rows are rewritten every time a lane's status moves, so its `R7` row is corrected in place in this commit.

**What I should have caught and did not.** I wrote `WAVE7_PLAN.md` §A. I checked that the `.gitignore` *said* the artefact was never committed — that premise check is in `reports/ORCH_STATE.md`'s superseded block and it was correct — and I quoted the size from the same line without measuring it, in a brief whose entire subject was *"the blocker is a `.gitignore` line."* `ls -l` on the two files it names would have cost one second. **The number I did check I got right (4,608 B per field, so 160 = 737 KB, and I sharpened it from a wrong ~5 MB at the time). The number I did not check I propagated.** The generalisation: **when a brief's argument is a size comparison, measure BOTH sides of it.** One side being measured is what makes the other side look measured.

---

## §40 — a concurrency brief that asked for the AMBIENT LOAD instead of the unit's OWN FOOTPRINT: a co-tenant lost 40% of its throughput and nothing in the instrument would have caught it

**Class:** defect in a CONDUCTOR-written brief. Not a defect in any unit, and not a result.
**Found:** 2026-08-19 02:35, by me, while both affected units were still running.
**Filed:** BESIDE the artefacts, per the W3 ruling Q3 — nothing in `E-FE`'s or `L6-b`'s output is edited.

**The wording.** My `E-FE` dispatch brief said: *"Report in the artefact: shards used, wall clock,
core-hours, and the load average at start and end."* That reads like a complete concurrency report and
is not one. **Load average is the weather. It tells you the box was busy; it does not tell you whose
work was destroyed, or how much of it.** A unit reporting `load 17` has discharged that clause perfectly
while remaining structurally blind to the fact that its six shards took 40% of the throughput of the
job running beside it — because the evidence for that lives in the OTHER unit's checkpoint file, which
the reporting unit has no reason to open and no standing to interpret.

**The measurement it missed.** `L6-b`'s own in-run trajectory, rolling 250-iteration windows:
**1.178 it/s at 02:21 → 0.712 it/s at 02:26**, a clean step at exactly the window in which `E-FE`'s
shards came up. Full table and provenance: `writeup/waves/WAVE7_CLOSE.md`, CONDUCTOR MEASUREMENT
2026-08-19. Schedule consequence: `L6-b`'s return moves ~07:15 → **~08:20**, conditional on `E-FE`
holding six shards.

**Compounding my own error, stated plainly.** I priced this box at ~11 of 12 cores busy. It ran at ~17.
I had already recorded one half of that (I assumed `L6-b` held ~5 cores; it holds 6). This is the other
half, and it is the half that costs wall-clock. **Both halves were available to measurement before
dispatch and I estimated instead.**

**THE RULE.** *A brief that puts a unit on a shared box must name the co-tenant and ask for the DELTA
imposed on it — measured from the co-tenant's own instrument, before and after — not the ambient load.
Where there is no co-tenant, the brief says so explicitly, so that the absence is a recorded fact rather
than an unasked question.* Ambient load may still be reported; it is not a substitute.

**What this does NOT do.** It does not change `E-FE`'s shard count — that was pre-committed against,
and a mid-run change destroys the per-attempt cost figure the ensemble owes the record. It does not
touch `L6-b`. It bears on **no gate**: this is a fact about one machine on one night, not about Route 4,
`W4`, or the field ensemble. And it is **not progress** — it is an instrument getting one notch less
blind, which §3i q7 counts against me, not for me.

## §41 — a gate of my own that is sound in one direction and under-specified in the other: `L6-b`'s `NO` branch cannot separate the two hypotheses it was built to separate

**Found:** 2026-08-19 03:20, by me, at iteration 7,000 of 20,000 — **before the gate number exists.**
**Filed:** as a pre-registration in `writeup/waves/WAVE7_CLOSE.md`, and here. `WAVE7_PLAN.md`'s
committed wording is **not edited**; the amendment is a document beside it, per the W3 ruling Q3.
**Whose defect:** mine. I wrote the wording, I dispatched on it, and no unit or verifier flagged it.

**The wording.** *"No material drop ⟹ the stall is the CONSTRUCTION, and `L6`'s `NO` hardens into a
real result about route 4's ansatz."*

**Why it does not follow.** That inference is only available at a stationary terminal iterate, and
the wording never required one. A `NO` at a point with `‖x‖‖∇J‖/|J| ≈ 10²` says the optimiser was
still descending when the cap arrived — which is *budget-limited*, the very hypothesis the `NO` was
supposed to eliminate. **A non-critical terminal point makes the two branches of the alternative
indistinguishable.** On present evidence (the banked start reads `116.9` at 7,000, oscillating in a
66–274 band rather than decaying) this is the outcome that will actually fire.

**The asymmetry, which is the useful part.** The `YES` branch is unaffected: a drop below `1.45`
proves `L6`'s ladder was budget-limited whether or not 20,000 converged. **Gates can be
half-defective.** A gate is not validated by having named both outcomes — it is validated by each
named outcome being *entailed* by the measurement that triggers it, and those are different checks.

**The exhaustive fact underneath it.** All **58** non-angular start-records in
`writeup/data/p2_route_l6_profile_v1.json` — both branches, every rung — have `nit == 800`. **100%
hit the cap. Not one terminated on a convergence criterion; 56 of 58 are non-critical at threshold
1.** `L6` conceded its headline "is not the infimum"; the artefact supports the stronger statement
that the ladder never located a stationary point anywhere, and so compared stopping points.

**A second omission, mine, closed in the same commit.** I have been quoting the banked minimiser's
`scale_invariant_grad = 153.22` as "the largest of its six starts" without its companion: that same
start has `max_abs_grad = 252.2`, **the smallest of the six**. The two columns rank the starts in
opposite orders. (**That "opposite orders" gloss is itself wrong; corrected at §43, which also
withdraws the seed comparison as confounded.**) The scale-invariant one governs — the objective is
invariant under `x → t·x`, and
raw `‖∇J‖_∞` can be shrunk by rescaling alone, which is exactly how `L6`'s L-BFGS-B was fooled into
a false convergence report once already (`leg_401.md` §7.3). **But "the correct column governs" is a
disclosure, not a licence to quote it alone.** Both columns, with the invariance argument, every time.

**THE RULE.** *A pre-committed gate must state, for EACH named outcome, the condition under which
that outcome ENTAILS its stated reading — not merely what the number will be. Where a reading
depends on the measurement having converged, convergence is part of the gate and is reported with
the number.* Naming both directions is necessary and is not sufficient.

**What this does NOT do.** `1.45` does not move and the run is untouched. It moves no `L1→L4` link.
It is **not progress** — it is a gate I wrote being caught under-specified, which §3i q7 counts
against the instrument.

## §42 — three throughput arithmetic errors in twenty-four hours, two of them mine, and the one thing they share

**Filed:** 2026-08-19 03:20. All three were caught before any of them entered a banked artefact.
**Why they are filed together:** individually each looks like a slip. Together they are a pattern —
**every one produced a rate that was wrong in the direction that flattered the reporter's schedule.**

| # | whose | the error | the direction it erred |
|---|---|---|---|
| 1 | mine | reported `0.690 it/s` from a **hand-picked tail window** before sweeping the trajectory | picked the window, then read it |
| 2 | `L6-b`'s | reported *"rate has eased to 0.848 it/s"* — a **cumulative average** presented as a current rate | hid the contention it was invoked to describe; the fast pre-contention hours never leave the numerator |
| 3 | mine | projected `E-FE` at **×2.09** of its briefed budget by dividing 6 shards × elapsed by **4 COMPLETED attempts while 6 were in flight** | billed work-in-progress to finished units; nearly doubled a real overrun |

**Error 3 in full, because it was 40 minutes old and I had already started writing it up.** The
correct arithmetic uses the unit's own per-attempt shard-hours (`0.39, 0.70, 0.77, 0.78` — one
converged, three stalled): mean `0.660 h/attempt` against a briefed `0.569`, i.e. **×1.16 on core-
hours (105.6 vs 91), or ×1.32 (120 core-h) if stalls dominate as the 1-in-4 recovery rate so far
suggests.** Wall `17.6–20.0 h` against a briefed `15.2`. **A real and reportable overrun of
16–32%, not the doubling I first computed.** `n = 4`; this is not yet a rate estimate worth an
interval and is not written as one.

**What they share.** All three take a ratio whose numerator and denominator are drawn from
**different windows of the run** — a tail numerator on a whole-run denominator, a whole-run
numerator on a current-moment claim, an in-flight numerator on a completed-work denominator. The
error is never in the division; it is in two time-spans silently differing.

**THE RULE.** *Any reported rate or per-unit cost names the window of BOTH its numerator and its
denominator, and they are the same window. Where a run has a regime change, report a LADDER of
trailing windows and the cumulative, each labelled — a single trailing window conceals recovery
exactly as a cumulative average conceals the fall.* The ladder clause is `L6-b`'s refinement, offered
as reasoned dissent when invited to disagree rather than complied with, and it is right: at its own
reading trailing-2,000 (`0.722`) sits BELOW trailing-500 (`0.757`) while trailing-4,000 (`0.837`)
sits above both, and only the ordered ladder shows the fall AND the partial recovery.

**Not progress.** Three arithmetic errors caught is an instrument working, not a result. Nothing
here bears on `W4`, route 4, or the field ensemble.

## §43 — the same figure corrected three times in one night, and the third correction removes it from the evidence: `153.22` is confounded by the very property that makes it the minimiser

**Filed:** 2026-08-19 03:30, still before `L6-b`'s gate number exists. **Corrects §41, filed ten
minutes earlier, and `L6-b`'s own amendment to it, filed five minutes after that.** Both were closer
than what preceded them and both were wrong.

**The three statements, in order, all about `L6`'s branch-B top rung.**

1. **Mine, standing for days:** *"the banked minimiser carries `scale_invariant_grad = 153.22`, the
   largest of its six starts, while the five seeds read 4.65–16.58."* True; a selected column.
2. **Mine, §41:** *"the two columns rank the six starts in opposite orders."* **FALSE.**
3. **`L6-b`'s:** *"a near reversal, not exact — `seed401` and `seed402` transpose."* **ALSO FALSE**,
   and it under-claimed in the wrong place: it conceded precision on the tidiness of the reversal
   while keeping the reversal.

**What the ranks actually are.**

| ascending by | order |
|---|---|
| `max_abs_grad` | `continuation`, `seed404`, `seed405`, `seed403`, `seed402`, `seed401` |
| `scale_invariant_grad` | `seed404`, `seed405`, `seed403`, `seed401`, `seed402`, `continuation` |
| an exact reversal of the first would be | `seed401`, `seed402`, `seed403`, `seed405`, `seed404`, `continuation` |

**Only 2 of 6 positions match a reversal.** Spearman `ρ = +0.086` (`p = 0.87`) across all six —
no relationship. **But excluding the continuation start, `ρ = +0.900` (`p = 0.037`): among the five
independent seeds the two columns AGREE.** The overall null is manufactured entirely by one point.
There is no reversal. There is **agreement everywhere except at a single start, which disagrees
maximally** — rank 1 by the raw column, rank 6 by the invariant one.

**And now the part that removes the figure from the evidence.** `sig = ‖x‖‖∇J‖₂/|J|`. Decomposing
the continuation start against the median seed:

| factor | continuation | median seed | ratio |
|---|---|---|---|
| `‖x‖` (`coeff_norm`) | 0.2641 | 0.0509 | **×5.19** |
| `‖∇J‖₂` (implied) | 936.2 | 5555.3 | **×0.17** — its gradient is SIX TIMES SMALLER |
| `|J|` | **1.6138** | 32.18 | **×0.05** — its residual is TWENTY TIMES SMALLER |
| `sig` | 153.22 | 9.67 | ×15.85 |

**The dominant factor is the denominator.** The continuation start's relative gradient is large
principally because its `J` is twenty times smaller — which is the same property that makes it the
banked minimiser in the first place. **The comparison to the seeds is confounded by the outcome
being compared.** "The largest of its six" is not evidence and is withdrawn from the finding.

**What survives, and it is the whole substantive claim.** `sig = 153.22 ≫ 1` is an **absolute**
statement: a relative perturbation of the coefficients of size `ε` moves `J` by up to `~153·ε·|J|`.
The point is not a critical point, and that rests on the threshold alone, needing no comparison to
any other start. **`L6-b`'s instrument was already built this way** — `NOT_CRITICAL = 1.0`, fixed a
priori — so its verdict logic is unaffected. Only the rhetoric around it was wrong, and only mine.

**Untouched by any of this:** all 58 non-angular start-records at `nit == 800`, 100% at the cap, none
converged, 56/58 non-critical. That fact needs no ranking and no comparison, and it remains the
largest thing in `L6`'s artefact.

**THE RULE.** *A ratio offered as evidence must be decomposed into its factors before it is
believed, and a comparison across units must not be confounded by the quantity that distinguishes
them. Where a relative measure is used, the ABSOLUTE threshold statement is the claim; a ranking
against other units is decoration and is usually contaminated.*

**A note on the sequence, because it is the honest finding about the discipline.** This figure was
corrected three times in ninety minutes — by me, then by the unit against me, then by me against
both — and every correction came from someone opening the primary artefact for a different reason.
**The second and third corrections were each produced by a party who had just been corrected.** That
is the mechanism working. It is not progress, it moves no `L1→L4` link, and §3i q7 counts three
audit-kind actions in a row against the instrument.

## §44 — a monotone trend manufactured from a non-monotone series, and the defect it exposes in MY OWN three-way licence: a single terminal sample cannot decide a threshold on a series with a 7-fold spread

**Filed:** 2026-08-19 03:35, still before the gate number exists. **Two defects, one measurement.**

### 1. The reported trend does not exist as reported

`L6-b` reported the banked start's `scale_invariant_grad` as *"205 → 162 → 117 → 99.7 → 74.7,
falling steadily."* Located in the run's own checkpoint trajectory, those five values occur at:

| reported order | 205.1 | 161.8 | 116.9 | 99.7 | 74.7 |
|---|---|---|---|---|---|
| **actual `k`** | **4,700** | **3,900** | 7,000 | 7,400 | 7,700 |

**`161.8` precedes `205.1` by 800 iterations. The reported chain puts them in the reverse of their
true order**, which is what makes the sequence read as monotone. And it omits the two largest values
in the same span: **`260.1` at `k = 5,500`** and **`423.9` at `k = 4,800`** — the latter being the
global maximum after `k = 4,000` and **5.7× the current reading**.

The series is not decaying steadily. Over the last 3,000 iterations, 61 samples:

| start | min | p25 | median | p75 | max | max/min |
|---|---|---|---|---|---|---|
| `banked_J4` | 62.9 | 96.5 | 124.9 | 166.2 | 423.9 | **6.7×** |
| `seed406` | 4.1 | 11.5 | 18.9 | 32.3 | 97.7 | **24.1×** |
| `seed407` | 3.2 | 9.0 | 20.1 | 31.2 | 106.9 | **33.7×** |

**Extrapolation from it is worthless and I checked before relying on it.** A log-linear fit over the
last 3,000 iterations predicts `sig(20,000) = 2.01`; the same fit over the last 5,000 predicts
`30.3`. **A forecast whose answer moves 15× with the choice of window is not a forecast.** I
therefore make none, and the plain statement is: the banked start's relative gradient drifts
downward inside a band that spans a factor of seven, and where it will sit at 20,000 is unknown.

**Almost certainly innocent in origin** — an earlier report said *"down from 205.1 at `k = 4,700` and
161.8 earlier"*, which is accurate, and the arrow chain is a later compression of it. **The
compression is where the trend was created.** This is `CORRECTIONS.md` §42's family again: a
statistic assembled from points drawn out of their own ordering.

### 2. THE DEFECT IN MY AMENDMENT, which is the more serious half

`CORRECTIONS.md` §41 gave `L6-b` a three-way licence keyed to **`scale_invariant_grad` at 20,000** —
a **single sample** of a series whose trailing-window spread is 6.7× on the banked start and 24–34×
on the seeds. **A single sample cannot decide a threshold crossing on a series like that.** Both
seeds visit `sig ≈ 3.2–4.1` transiently while sitting at a median near 20; a terminal sample landing
in a trough would license a reading the series does not support, and one landing on a spike would
deny a reading it does.

**I wrote that licence ten minutes after finding the gate it was fixing under-specified.** The fix
had the same shape as the defect: it named a quantity without naming how the quantity is read.

**THE AMENDMENT TO THE AMENDMENT.** The licence keys off a **trailing-window statistic, and in the
conservative direction**: to license the "critical, pre-committed reading stands in full" row, the
**MAXIMUM** of `scale_invariant_grad` over the last 2,000 iterations must be below 1 — not the
terminal sample. *To claim a point is critical you must show it STAYS critical, not that it touched
critical once.* The middle row is the default and requires nothing. `1.45` is untouched; the `YES`
branch is untouched; the run is untouched. Report min / p25 / median / p75 / max over the trailing
2,000 for all three starts alongside the terminal value.

**On present numbers this changes no outcome** — the trailing minima are 62.9 and 3.2–4.1, all above
1, so the middle row fires either way. **It is written down because it must be right for the right
reason, and because the terminal-sample version would have been the load-bearing sentence in a
different run.**

### 3. One thing worth reporting in its own right

**The two independent seeds' relative gradients are RISING, not falling** — log-linear fits over the
last 3,000 iterations give `r = +0.77` and `r = +0.83`, strongly positive — **while their `J` falls**
(≈18 → 10.7 and 11.2). `sig = ‖x‖‖∇J‖₂/|J|`, so a falling `J` raises `sig` unless the gradient falls
faster, and it is not. **They are descending in objective while becoming relatively LESS stationary.**
That is a fact about the landscape, not about the optimiser, and it belongs in the artefact.

**Not progress.** No `L1→L4` link moves. This is the fourth audit-kind action in a row and §3i q7
counts every one of them against the instrument.

## §45 — a repository-wide measurement provoked by `C37`: 32 of 49 evidence scripts cannot, by construction, detect an error shared between an artefact and its own checker

**Filed:** 2026-08-19 03:45. **Provoked by `L6-b`**, which found that its evidence check `C37`
**asserted** the `153.22` ranking that §43 withdrew — the check would have PASSED on the false claim
and certified it. `L6-b`'s generalisation, which is its own and is correct, is that *a self-check
that encodes the claim it tests verifies only internal consistency between an artefact and a script
written by the same unit in the same hour.* **This entry is the measurement of how far that reaches.
It reaches most of the repository.**

### The measurement

Every `experiments/*_evidence.py` was classified by whether it references any data file **outside
its own unit's artefact**:

| | count | share |
|---|---|---|
| evidence scripts | **49** | |
| **reference NO file outside their own unit's artefact** | **32** | **65%** |
| reference at least one independent source | 17 | 35% |
| of the 32, do not recompute at all (pure field read) | 3 | |

**Classifier validated by hand on three scripts before the number was believed** — `t4` (solo,
correct: its own docstring says *"every number this leg's journal quotes, re-derived from
`p2_route_t4_v1.json`"*), `l6b` (independent, correct: it opens `L6`'s untouched artefact and the raw
checkpoint iterates), `ng` (solo, correct). §44's lesson applied to §45's own number.

### What the number does and does not say

**It does NOT say those 32 checks are worthless.** A solo check catches transcription errors,
internal arithmetic inconsistency, and a journal quoting a figure the artefact does not contain —
all real defects, all caught here before.

**It says exactly one thing, and it is sufficient:** a check that reads only the artefact its own
unit wrote **cannot detect a claim that is wrong in the artefact AND in the script**, because the
same reasoning produced both. That is not a hypothetical failure mode. **It is what `C37` was**, and
`C37` sat inside a unit that was otherwise running better instrument discipline than most.

**The pointed instance.** `p2_route_t4_v1_evidence.py` is solo. `T4` is one of the two units that
measured **the lane's central premise FALSE** — the single largest adverse finding this programme
has produced, and the first row of `P4`'s evidence table. Its evidence check re-derives the journal's
numbers from `T4`'s own artefact and reads nothing else. **The result survives because `T6` reached
it independently by another method and the two were never told each other's result** — which is the
cross-unit design, not the evidence-check design, and the distinction has been invisible in the
record until now.

### THE RULE

*An evidence check is classified, not counted. A check that reads only its own unit's artefact
certifies INTERNAL CONSISTENCY and is labelled as such; a check that recomputes from an independent
artefact, from raw data, or from a source the unit did not write certifies the CLAIM.* **`N/N
passed` is not evidence of anything until every check carries its class.** Where a finding is
load-bearing, at least one check on it must be of the second kind or the finding is `UNVERIFIED`
however many checks passed.

### What this does NOT do, and a count I owe against myself

It moves **no** `L1→L4` link. It retracts **no** landed result — `V-W3`, `V-W4`, `V-W5` and the
cross-unit design are independent of the evidence-check layer and are untouched. It is **not
progress**; it is the verification layer being measured for the first time and coming back weaker
than its `N/N passed` headlines implied.

**§3i q7, answered honestly: this is the FIFTH audit-kind action in a row** (§41, §42, §43, §44,
§45). Two of the five corrected remedies I had written minutes earlier. **That is an audit loop and
I am naming it as one.** The five were cheap, they were forced by a live unit's returns rather than
sought, and every one landed before a gate number existed — but the count stands and the direction
check answers it the same way regardless. **Wave 8 opens on the Clay chain: `L-JVER` and `PB2` both
attack `W4` directly, and no further instrument work is dispatched ahead of them.**

## §46 — `L6`'s seed spread was quoted as a property of the ANSATZ and is substantially a property of the BUDGET; plus my own misreading of a failing check as a false alarm

**The withdrawn claim.** `WALLS.md`'s `L6` block records, as a ceiling measured by the Conductor on
landing and upheld by `V-W6`: *"Seed spread **3.93–23.67× on B**, never above 5.95× on A"*, offered
as evidence about the construction's basin structure — that `ρ ≈ 1.6` is a continuation artefact
which fresh seeds do not find. **The direction of that statement survives. The NUMBER does not, and
it was never a number about the ansatz.**

**Why, and this time the comparison is not confounded.** `L6-b` (leg 406) ran two fresh seeds to
20,000 iterations and banked their whole trajectories, so **the same seeds can be read at both
budgets** — same apparatus, same `n_dof = 6720`, same branch, same norm, only the cap differs:

| | `seed406` | `seed407` | seed/continuation ratio |
|---|---|---|---|
| at `k = 800` (`L6`'s cap) | `28.6934` | `35.5608` | **17.81× and 22.07×** |
| at `k = 20,000` | `6.4597` | `6.5024` | **4.29× and 4.32×** |
| improvement, same seed | **×4.44** | **×5.47** | **the ratio falls ~5×** |

⚠ **THE NEXT SENTENCE IS FALSE — see §50 item 1. Left standing, not edited.**
`L6-b`'s two seeds sit inside `L6`'s own five branch-B seeds at the same cap (`29.57`–`38.20`), so
they are drawn from the same population and the comparison is like-for-like. **`23.67×` is what the
seed/continuation ratio reads when every start is stopped at 800 iterations. It is not what the
landscape is; it is where L-BFGS-B happened to be at 800.**

**What still stands, stated separately so it is not lost.** At 20,000 iterations both independent
seeds are still at `6.46`/`6.50`, **outside** the pre-committed `[1.55, 1.70]` band. *At this budget
`ρ ≈ 1.6` remains reachable by continuation and not from cold starts.* That claim is intact and it
is the one the ceiling was for. What is withdrawn is the **magnitude** being read as a landscape
property, and any inference that the gap is large because the basin is narrow.

> **THE RULE.** *A quantity measured at a resource cap is a property of the cap until it is shown
> otherwise, and it may not be quoted as a property of the object. Where a spread, ratio or ranking
> is offered as evidence about a construction, the record must state the budget at which every term
> was measured — and if the terms were measured at DIFFERENT budgets, the comparison is void.*

⚠ **The second clause as written voids this section's own evidence — repaired at §50 item 3.**

This is §43's error in its second costume: there a ratio was confounded by `|J|`, here by the
iteration cap. Both were quoted by me, both were true of what was computed, and both were read as
establishing a property they cannot reach. **`V-W6` upheld the first version of this ceiling; a
verifier agreeing is not the same as the claim being measured.**

### §46b — and one of mine, from the same landing, in the same family

Auditing `L6-b` I ran its evidence suite and saw `C41` **FAIL**. The unit was mid-landing: it
rewrote the check at 08:08:58 and the artefact at 08:09:19, my run having started at 08:08:0x. I
recomputed the three correlation coefficients, found them identical to `0.00e+00`, and reported to
the user that the failure was **"void"** and **"a false defect against a unit that had done nothing
wrong."**

**Both words were wrong.** `C41` had genuinely failed on a true artefact, and the unit had already
diagnosed why: the check **asserted a direction** (the seeds' relative gradient rising, `r = +0.76`
/`+0.82` over `k = 4,700–7,700`) which **reverses** over the final 3,000 (`−0.23`/`−0.35`). That is
the exact mirror of `C37`, which would have *passed* on a false claim — one check encoding a claim
instead of verifying a number, in both directions. My recomputation compared **the rewritten check
against the rewritten artefact** and concluded the **original** failure was spurious.

> **THE RULE.** *When an artefact and its checker are both moving, a check result names WHICH
> VERSION OF EACH it was produced from, or it is not a result. And a recomputation that agrees with
> the current pair says nothing whatever about a failure observed against a previous pair.*

**The race was real; the conclusion drawn from it was not.** The failing check was the unit finding
its own defect, and I read it as the unit being wronged by my timing.

## §47 — the wall's most load-bearing citation names the wrong journal, wrong volume and wrong pages, and names two theorems jointly where only one of them applies; the MEASUREMENT is untouched, the SENTENCE written about it was not checked against the paper

Unit `PB2` (leg 410) was sent to a seam, not a defect: `WALLS.md`'s W4 clause (b) — **SHUT** and
**✅ VERIFIED** since leg 403 — shuts the `ṁ ≡ 0` exit with *"excluded by **Nečas–Růžička–Šverák**
(ARMA 136, 1996) **and** Tsai (ARMA 143, 1998)"*, two theorems named jointly with no statement of
which carries which case. Reading Tsai at primary to settle that produced two findings, and it
matters that they are kept apart.

**Finding 1, the small one, which is nevertheless in four load-bearing places.** Tsai 1998's own
bibliography, p.50, read at FULL TEXT from the copy this repository has held since leg 359:

> `[NRS]` J. Nečas, M. Růžička & V. Šverák, *On Leray's self-similar solutions of the Navier-Stokes
> equations*, **Acta Math. 176 (1996), 283–294.**

The repository cites it as **`ARMA` 136 (1996)** in `WALLS.md` (W4 clause (b)), `SOURCES.md` row 3,
`WAVE8_PLAN.md` (twice), and `p2_route_l5_finite_energy_v1.json`, the last adding pages **`55–98`**.
**Wrong journal, wrong volume, wrong pages.** `ARMA 136 (1996) 55–98` is not a null string — it
looks exactly like a real citation, which is why it survived a verifier. The likely origin is
adjacency to Tsai's own `ARMA 143`, and it propagated from one artefact into the wall and the plan
without anyone opening the paper. **Leg 364's journal already had it right** — `Acta Math. 176
(1996) 283–294`, DOI `10.1007/BF02551584` — so the repository has held the correct citation and the
incorrect one simultaneously for six legs, in different files, without either noticing the other.

**Finding 2, the one that actually needed the paper.** The joint citation is not merely
under-specified; **as applied to route 4's object it names one theorem that does not apply.** NRŠ's
hypothesis is `U ∈ L³(ℝ³)`. At the pinned `α = 1` the object's `∫|U|³` is **log-divergent** —
measured this leg, increments constant at `139.287` per decade, coefficient `60.4916579840` against
`60.4916579840` in closed form. **`U ∉ L³`, so NRŠ's hypothesis is not satisfied and NRŠ does not
exclude this object.** What excludes it is **Tsai 1998 Theorem 2**, whose hypotheses are (§2, p.34)
*"we do not require the weak solution `u` to be a Leray-Hopf weak solution. Our only requirements
(apart from self-similarity) are (i) and (ii)"* — the equations and the local energy estimates
`(1.4)`, with **no `L^q` in the hypothesis at all** — and (ii) is satisfied by measurement.
**Tsai Theorem 1 independently carries it too**, since `U ∈ L^q` for every `q ∈ (3,∞]`.

> **THE RULE.** *When a wall clause is shut by a NAMED theorem, the record must name WHICH theorem
> and state that the object meets ITS hypotheses. Two theorems joined by "and" assert that both
> apply; if one does not, the sentence is false even when the clause is true. And a citation that
> no unit has ever opened is an UNVERIFIED string however many artefacts repeat it — repetition is
> not corroboration, it is one source counted many times.*

**What is NOT wrong, stated plainly because the temptation runs the other way.** **Clause (b)
STANDS.** It stands on a **stronger** footing than its citation suggested: the theorem that carries
it is the one this repository has at **FULL TEXT**, and the theorem it cannot obtain — NRŠ, four
failed fetches across legs 253, 359, 364 and 410, `UNREACHABLE` at primary, `SECOND HAND` in the
register — turns out to be **not load-bearing for this clause at all.** The `SECOND HAND` debt is
still a debt; it is no longer a debt W4 clause (b) is resting on. **A defective citation is not a
defective theorem**, and reading it as one would be §43's error in a new costume. `V-W5`'s verdict
is upheld; what failed was not the verification of the mathematics but the transcription of the
attribution, which no verifier in this programme has ever been asked to check against a PDF.

**The correction is placed BESIDE the data, not over them.** `WALLS.md`'s banked W4(b) sentence and
`p2_route_l5_finite_energy_v1.json` are **unedited**; the wall gets an added paragraph naming the
carrier, `SOURCES.md` gets an append-only block, and the measurements live in
`writeup/data/p2_route_pb2_v1.json` with `experiments/p2_route_pb2_v1_evidence.py` (31 checks).

**A defect this leg found in ITSELF, banked here so the count is honest.** `PB2`'s first run
truncated the `L^q` integral at `r = e⁶⁰`, where the `q = 3.01` integrand still sits at `0.55` of
its far-field size; `‖U‖_{3.01}` read `17.478` against a true `18.085`, a **3.4% error that
doubling the resolution cannot detect**, because it is a DOMAIN error wearing a convergence
study's clothes. Fixed with a closed-form `α = 1` tail beyond `r = e³⁰` and a new
`seam_moved_rel_change` control banked next to `resolution_doubled_rel_change`. *A resolution
control certifies resolution. It says nothing whatever about where you stopped integrating.*

---

## §48 — a cap that nobody measures is not a cap: `WALLS.md` landed **2,151 bytes over §3j** through a `MERGE GATE: PASS`, and the check that would have caught it did not exist

**What happened.** `PB2` (leg 410) added 25 lines to `WALLS.md` and landed at `a7ffa1e`. The file
went from **32,526** to **34,919 bytes** against an `ORCHESTRATION.md` §3j cap of **32,768**. The
merge gate printed `MERGE GATE: PASS`. Nothing objected, because nothing was looking.

**Whose defect this is, stated plainly: MINE, and in two distinct ways.** First, `WAVE8_PLAN.md`
§6 STANDING CLAUSES — the block whose entire purpose is *"IN EVERY BRIEF"* — **does not mention
§3j at all**, so no unit in this wave was told the caps exist. Second, and worse, I had measured
those caps by hand at `0c7c52e` **ninety minutes earlier**, retiring five blocks to hold them, and
recorded the result in a table. **I treated a number I had just computed by hand as a standing
property of the repository.** That is `§45`'s substitution again, and this time the cheap quantity
was one I produced myself.

**THE RULE.** *A cap enforced by a person reading `wc -c` at a boundary is not enforced between
boundaries, and every concurrent unit works between boundaries. A limit that is not mechanically
checked at the same moment the artefact is written is a description of intent, not a constraint —
and it will be quoted as though it were a measurement, because the last time someone measured it,
it was true.*

**The remedy, and it is a construction rather than a note.** `test_headroom.py`, wired into
`scripts/merge_gate.sh` as an always-on check alongside `test_plan_of_record.py` and
`test_capabilities.py`. It measures all four §3j caps in **bytes**, measures `STATE.md`'s rows in
**characters** (they are not the same thing in a file full of `‖`, `∇` and em dashes), locates
`ORCH_STATE.md`'s LIVE block by heading, and **fails when it cannot locate that block** — an
UNCHECKED cap is a FAIL, never a silent PASS. Mutation-tested in a scratch copy on four separate
breaks: a file over cap, a row over 600 characters, a LIVE block over cap, and a missing LIVE
heading. All four were caught; the unmutated control passed.

**What it does NOT do, said here so nobody quotes it as more than it is.** It cannot tell a
retirement from a deletion, so §3j's *"retirement is preferred over compaction"* remains a
discipline held by a person. It checks size and says nothing about whether the text is true. And
it enforces caps that were themselves chosen by judgement, not measured — the caps are a policy,
and this test only makes the policy binding.

**The honest accounting for `P4`.** This is the **second** prospective catch on that page against
**eight** retrospective ones, and it is weaker than the first: `§42` caught its instance *before
the number was banked*, whereas this one was found **after** a bad state had already landed on
`main` and been pushed. The catch was a `wc -c` run during an integration audit for an unrelated
reason — **which is, for the fifth recorded time, how defects are actually found here.**

---

## §49 — the documentation contract MANDATES the blind spot that §45 measured: `ORCHESTRATION.md` §6 clause 3 REQUIRES evidence scripts to re-read their own artefact and re-run nothing

**The measurement.** `experiments/p2_route_pb2_v1_evidence.py` runs **31 checks, 0 failed**. It
imports `json`, `sys` and `pathlib`, and nothing else. **Zero of its 31 checks recompute anything
from a primary source.** All 31 read `writeup/data/p2_route_pb2_v1.json` — the file written by the
unit whose claims they check. On `§45`'s classification the script is 0/31
`recompute-from-primary` and 31/31 `re-read-own-artefact`, which is worse than the repository's
already-poor 35%.

**And the unit was not free to do otherwise.** `ORCHESTRATION.md` §6 clause 3, verbatim: an
*"`*_evidence.py` script rebuilds figures/claims from the curated JSON **without re-running
anything**"*. The unit followed the contract exactly. `§45` diagnosed this as a property of 32 of
49 scripts and treated it as drift; **it is not drift. It is compliance.** The contract that
exists to make claims checkable specifies a check that cannot fail on the error that matters.

**THE RULE.** *Where a standard prescribes the FORM of a check, read the form for what it makes
IMPOSSIBLE to detect before congratulating the check for passing. A rule that mandates a procedure
also mandates that procedure's blind spot, and the blind spot inherits the rule's authority — so
it is defended rather than noticed.*

**What is NOT concluded, and this matters.** §6 clause 3 has a real purpose: it stops an evidence
script silently re-running the experiment and "verifying" a fresh answer against fresh prose,
which is how a wrong number gets laundered into agreement. **The clause is not withdrawn and no
part of it is called defective here.** What is recorded is that it is not sufficient, that the
`N/N passed` line it produces means less than it reads as, and that the two purposes need two
checks rather than one. **Naming the amendment is not this correction's job** — it is a change to
the orchestration contract, and it goes to the user with the rest of this integration.

**Also not discharged, and it is mine again.** `PB2`'s brief required, in terms, *"classify every
check you write as recompute-from-primary vs re-read-own-artefact and state the class beside it"*.
The script carries **zero** such labels. Nothing checked that the brief's own instrument clause
was obeyed, and I did not notice until I grepped for the labels during the landing audit. **A
requirement stated in a brief and verified by nobody is a preference.**

---

## §47b — the citation defect is in FIVE places, not four, and the one `PB2` missed is the one that GENERATES the others

**The correction to a correction.** `§47` names four sites carrying NRŠ as *`ARMA` 136 (1996)*:
`WALLS.md`, `SOURCES.md` row 3, `WAVE8_PLAN.md`, and `p2_route_l5_finite_energy_v1.json`. There is
a fifth, and it is the source of the fourth: **`experiments/p2_route_l5_v1_driver.py:640`** emits
the string `"136 (1996) 55-98) and Tsai (ARMA 143 (1998) 29-51) exclude."` into the banked JSON.
The JSON is a **product**; the driver is the **plant**. There is also a sixth occurrence in
`experiments/journal/leg_400.md:505`, which is a journal and correctly gets a correction beside it
rather than an edit.

**The count was low for a reason worth naming.** `PB2` searched the prose record — the `.md` files
and the banked `.json` — and found every occurrence in it. It did not search the **code that wrote
the JSON**. A defect in a generated artefact is not fixed, and is not even fully counted, until
the generator is in the list.

**And I propagated it myself.** `WAVE8_PLAN.md` AMENDMENT 4, which I wrote **to scope the very
unit that found this**, cites *"Nečas–Růžička–Šverák ARMA 136 (1996)"* twice — in the jaw table
and in the quoted `WALLS.md` sentence. The second is a quotation and correctly reproduces the
error it quotes. **The first is my own assertion, made while auditing citations, and it is wrong.**

**THE RULE.** *When a wrong string is found in a banked artefact, the search is not finished until
it has been run against the code that produces the artefact. Prose and data are downstream of a
generator, and correcting the downstream copies leaves the plant running.*

**Unchanged by all of the above, and stated so no one reads this as a retreat:** the citation is
wrong and the theorem is right. **Tsai 1998 Theorem 2 carries `W4` clause (b)**, its hypotheses
are met by measurement, and clause (b) STANDS. A defective citation is not a defective theorem —
which is `WAVE8_PLAN.md` AMENDMENT 4's own pre-committed constraint, and it binds here.

## §50 — the correction §46 needed: one FALSE sentence, one over-broad withdrawal, and a rule that voided its own evidence; plus a §5b commit crossing of mine

**Provenance.** All four were found by `V-W7` (leg 412, `aefe590`) auditing **the Conductor's own
integration**, not the units. Every one is re-verified here from the banked primary, not accepted on
the verifier's word. `V-W7` ruled seven defects against me; the three that touch `§46` are below,
the commit crossing is item 4, and the two that were already remedied or that I rule differently are
recorded at items 5–6.

**Item 1 — §46's support sentence is FALSE.** §46 says `L6-b`'s two seeds *"sit inside `L6`'s own
five branch-B seeds at the same cap (`29.57`–`38.20`)"*. Read from
`experiments/route4/l6b_ckpt/seed406.json`, trajectory row `k = 800`:

| | at `k = 800` | inside `29.57–38.20`? |
|---|---|---|
| `seed406` | **`28.693380532819674`** | **NO — 2.96% BELOW the lower end** |
| `seed407` | `35.560845905666` | yes |

One of the two is outside. The sentence was written to establish that the fresh seeds and `L6`'s
seeds are drawn from one population, and it overstated its own evidence to do it. **What survives:
the like-for-like comparison, which never needed that sentence** — `L6-b` fixed `n_dof`, branch,
norm, apparatus and seeds and varied *only* the cap, so the budget effect is measured within the
same seeds and does not depend on where they fall among `L6`'s. The population claim is now: one
seed inside the observed range, one just below it.

**Item 2 — the withdrawal is too broad at the low end.** §46 withdraws the range *"3.93–23.67× on
B"* entire. But the same seeds read at 20,000 iterations give seed/continuation ratios
**`4.29257`** and **`4.32093`** — both *above* `3.93`. **The bottom of that range is not a cap
artefact; it survives a 25× budget.** What the budget destroys is the TOP of the range and the
inference drawn from its width. The withdrawal is hereby narrowed: `23.67×`, and the spread read as
basin structure, are withdrawn; **`≈ 4×` at full budget stands as measured.**

**Item 3 — §46's rule voided §46's own evidence.** The rule's second clause said *"if the terms were
measured at DIFFERENT budgets, the comparison is void."* §46's own decisive column — the
`×4.44`/`×5.47` improvement per seed — **is** a comparison of terms at two different budgets. Under
its own rule §46 deletes its own proof. The clause is replaced:

> **THE RULE, REPAIRED.** *A quantity measured at a resource cap is a property of the cap until it
> is shown otherwise, and it may not be quoted as a property of the object. Comparing terms measured
> at DIFFERENT budgets in order to claim something about the OBJECT is void. Comparing the SAME term
> at two budgets in order to claim something about the BUDGET is not merely valid, it is the only
> instrument that settles it — which is exactly what `L6-b` did. A rule about confounding must name
> what is confounded with what, or it forbids the experiment that would resolve it.*

**Item 4 — a §5b commit crossing, mine.** `04f9ff5` (*"PB2 pre-dispatch: rescue two load-bearing
primaries out of an ephemeral worktree"*) and `6ca49a6` (*"WAVE8 AMENDMENT 4: re-scope PB2"*) each
carry `experiments/route4/l6b_ckpt/seed406.json` and `seed407.json` — **`L6-b`'s live in-run
checkpoints, swept into commits whose subjects name neither the files nor the unit.** Confirmed from
`git show --stat`. Nothing was corrupted and the sweep is why the k=800 rows above are on `main` at
all, but a concurrent unit's live state entered the record under an unrelated subject, and the next
reader has no way to know it. **This is how a checkpoint gets attributed to the wrong leg.**

> **THE RULE.** *A commit subject is an index into the record. Sweeping another unit's live files
> under a subject that does not name them is not untidiness — it silently reassigns their
> provenance, and provenance is the only thing that makes a checkpoint evidence rather than a file.*

**Item 5 — the §3j table, ALREADY REMEDIED, recorded for the count.** `V-W7` found the headroom
table at `c6287a2` overstated 2 of 4 rows (STATE `24,016` not `23,639`; ORCH LIVE `7,401` not
`7,247`) and that both wrong rows were **byte-identical to the superseded wave-6 table** — carried
forward, not re-measured. Same disease as §48, one boundary earlier. Already fixed by re-measuring
every row, and `test_headroom.py` now makes the class impossible to repeat. `V-W7` separately
**UPHELD** the verbatim retirements (`§W4-L6CEIL` byte-identical, 11/11 lines).

**Item 6 — the `R-prof` sentence: UPHELD IN PART, and the part that differs matters.** `V-W7` rules
my repaired sentence — *"'every round exceeds 3×' holds on the cpu clock only"* — **still false**,
citing `raw_ratio_cpu_clock.min = 2.89873`. Checked: that number is from **`V-W7`'s own re-run**, and
it is **not in the banked artefact**. `writeup/data/p2_r_prof_v1.json` records exactly one
`raw_ratio_cpu_clock`, at `gate/iii_within_3x_of_reference`, with **`min = 3.3721551723168335`**. So
the sentence is TRUE of the record and FALSE on re-execution. That is not a misreading; it is a
**reproducibility** finding, and the better one: a ratio sitting `12%` above a threshold, on a
machine the artefact itself flags `MACHINE_WAS_NOT_QUIET`, is not a stable property of the code. The
sentence is qualified as run-specific rather than withdrawn.

> **THE RULE.** *A verifier's number that disagrees with the banked artefact has not necessarily
> found an error in the reading — check whether it re-ran. A claim that is true of the record and
> false on re-execution is a claim about one run, and the threshold it sits near is the finding.*

## §51 — the under-claim: `L6-b`'s 25× budget moved the residual `×1.3518` of `L6`'s ENTIRE refinement ladder, and `L6`'s ladder can INVERT on a margin of 0.46 percentage points

**This is not a correction of a wrong number. Every number below was already banked. It is the
correction of a landing — mine — that recorded the smaller finding and missed the larger one, and it
went un-noticed through the unit's own write-up, the Conductor's integration, and a verifier.**
Found by `V-W7` (leg 412) and re-derived here from `writeup/data/p2_route_l6_profile_v1.json` and
`experiments/route4/l6b_ckpt/*.json`.

**The comparison nobody made.** `L6` refined the discretisation four rungs and `L6-b` raised the
iteration cap 25× at the discretisation held FIXED. Both are reported in `ρ`, `L5`'s load-bearing
norm, on branch B. Put side by side:

| what was varied | `ρ` | change |
|---|---|---|
| `L6`, **four rungs of refinement**, `J1 → J4`, cap 800 | `1.6986514108481086 → 1.613811231995397` | **`−4.994561%`** |
| `L6-b`, **one budget step ×25**, `n_dof` FIXED at 6720 | `1.613811231995397 → 1.504851895102804` | **`−6.751678%`** |

**One budget step moved the objective `×1.3518` of what the entire four-rung refinement ladder
moved.** `L6`'s headline reading — *the residual does not decrease under refinement* — was measured
with every rung stopped at 800 iterations, i.e. **at a cap now demonstrated to dominate the very
quantity being differenced.** The ladder does not measure refinement. It measures where L-BFGS-B
had got to after 800 iterations at each `n_dof`, and the rungs are not converged enough to be
subtracted from one another.

**And the ladder can invert.** `L6`'s rung `J3` (`Nr = 16`, 2400 dof) reads `ρ = 1.6218749783288575`
at 800 iterations, above `J4`'s `1.6138`. For the ordering to reverse, `J3` at raised budget must
fall below `J4`-at-20,000 = `1.504851895102804` — a drop of **`7.2153%`**. One rung up, at *more*
degrees of freedom, the same budget increase delivered **`6.7517%`**.

> **THE MARGIN IS `0.4636` PERCENTAGE POINTS, AND IT IS THE WRONG WAY ROUND BY LESS THAN THE
> MEASUREMENT ALREADY IN HAND.**

`J3` has *fewer* degrees of freedom than `J4`, so it is cheaper to run and, on the usual expectation
that smaller problems converge further per iteration, it is the rung most likely to clear the bar.
**Nothing in the record establishes that it does not.** `L6`'s `NO` is not overturned by this — it
is left resting on an ordering that has never been measured at a budget where the ordering means
anything.

> **THE RULE.** *When a refinement study and a budget study measure the same objective, DIVIDE ONE
> BY THE OTHER BEFORE REPORTING EITHER. If the budget term is the same size as the refinement term,
> the refinement study has not measured refinement, and its monotonicity — in either direction — is
> an artefact of where the iteration stopped. The comparison costs one line of arithmetic and it was
> not done at the landing, not done in the unit, and not done by the first verifier.*

**What this obliges.** A new Lane L unit, `L6-e`: **one rung, `J3` (`Nr = 16`, 2400 dof), re-run to
20,000 iterations**, same apparatus, same seed policy, same norm — the single cheapest measurement
in this record that could overturn Lane L's own headline. Priced **~20–35 core-h** (below `L6-b`'s
43.3 because `J3` carries fewer dof), one shard, ~6 h wall. **Queued for wave 9.** Its gate is
pre-committed here: `ρ(J3 @ 20,000) < 1.504851895102804` ⟹ **the ladder inverts and `L6`'s
"not decreasing under refinement" is withdrawn as budget-confounded**; `≥` ⟹ the ordering survives
one honest test and `L6`'s `NO` is strengthened, having been at risk. **Both outcomes are results.**

**Why it was missed, which is the part `P4` needs.** The two numbers live in different units, in
different waves, in different JSON files, under different headings — and each was correct where it
sat. No check compares across units; §45 counted 32 of 49 evidence scripts unable to see an error
shared between artefact and checker, and this is the neighbouring blind spot: **an error shared
between two artefacts that no single checker reads together.** The discipline did not catch this. A
verifier reading both legs did, on the third pass, at leg 412 — **eleven legs after `L6` landed.**

---

## §52 — `J(c)` is a DIVERGENT integral, and every route-4 residual in the record is a value of a 72-node truncation of it; the operator is RIGHT, which is why nobody saw it

**Provoked by** `V-W6`'s `D-VW6-6`, executed by `L-JVER` (leg 409, wave 8), artefact
`writeup/data/p2_route_ljver_v1.json`, `self_hash 4bb618d7c8b039ea`, journal
`experiments/journal/leg_409.md` §§7–15.

**This is a correction record placed BESIDE the banked data. `writeup/data/p2_route_l6_profile_v1.json`,
`writeup/data/p2_route_l6b_v1.json` and `experiments/p2_route_l6_v1.py` are NOT edited and must not be.**

`V-W6` observed that `J(c)` — `‖curl F‖_{L¹_t L^{3/2}_x}` for the backward λ-DSS profile, λ = 1.7,
`a = 0.5` — had never been checked against anything outside its own author's code. Its only internal
evidence was a self-test comparing two of `L6`'s OWN implementations. `L-JVER` built a second
implementation from the written mathematics in a disjoint basis (Cartesian real solid harmonics, term
algebra on `y^α r^p G^{(k)}`), a disjoint radial-derivative mechanism (Taylor jets, cross-checked
against mpmath at 40 dps), and a disjoint quadrature (composite Gauss–Legendre in `ln r` over an
explicit `[r_min, r_max]`, equiangular cube-sphere in angle, offset-uniform in `s`). Twelve controls,
**all twelve `recompute-from-primary`, none `re-read-own-artefact`** (§45/§46b), fired first —
including both implementations against a field with closed-form `curl` and a hand-computable
`L^{3/2}` norm (mine `7.51e-12`, `L6`'s `2.80e-15`), and a planted-defect control that moves `J` by
80% and so proves the pipeline can fail.

**The pre-committed two-sided gate — `|J_new − J_L6|/J_L6 < 1e-3` at branch B, branch A, AND a
non-minimiser — answers `NO`:**

| point | `J_new` | `J_L6` | rel |
|---|---|---|---|
| banked branch B, `n_dof = 6720` (minimiser) | `1.613972916` | `1.613811232` | `1.0019e-04` |
| banked branch A, `n_dof = 6720` (minimiser) | `7.582440062` | `7.583387202` | `1.2490e-04` |
| **`J0` index box of B in the 6720 space — NOT a minimiser** | `21.09203973` | `14.76088926` | **`4.2891e-01`** |
| pseudo-random, seed 409 (extra) | `12855.55435` | `7222.503805` | `7.7993e-01` |

**And now the part that matters more than the `NO`.** The natural reading — "one of the two programs
computes `W` wrongly" — is **refuted by measurement.** Take `L-JVER`'s independent operator and
evaluate it at `L6`'s own quadrature nodes, contracted with `L6`'s own weights: `J` reproduces `J_L6`
at rel `1.101e-14`, `2.460e-15`, `5.897e-15`, `1.864e-14` at the four points respectively. Pointwise,
on 580 608 of `L6`'s grid points, `max rel 1.75e-10`.

> **`L6`'s OPERATOR `W[V]` IS RIGHT. THE ENTIRE 43% IS THE QUADRATURE RULE — AND A DISAGREEMENT THAT
> LIVES ONLY IN THE RULE, WHILE EACH RULE IS SEPARATELY CONVERGED, MEANS THERE IS NO FINITE NUMBER
> FOR THE TWO PROGRAMS TO AGREE ON.**

`J(c)` diverges logarithmically at both ends for generic `c` in this trial space. At `r → ∞`,
`F_lm → F_lm(∞,s)` finite, so `w ~ A(ŷ,s)/r²`; the DSS term `a(2w + y·∇w)` annihilates a degree `−2`
homogeneous `w` exactly and `Δw` and both nonlinear terms are `O(r^{-4})`, but `w_s ~ ∂_s A/r²`
survives, giving `|W|^{3/2} r² ~ 1/r`. Branch B's own normalisation forces `Σ F_lm(∞,s)²` to average
1 and its `k > 0` `s`-modes force `∂_s A ≠ 0`, so branch B cannot escape it. At `r → 0`, the radial
basis `u^l T_n(2u−1)` with `u = r/2 − r²/4 + …` carries a nonzero `r^{l+1}` coefficient and
`Δ²(r^{l+1}Y_lm) = −4l(l+1) r^{l−3}Y_lm`, which at `l = 1` is `r^{-2}`, again `|W|^{3/2}r² ~ 1/r`.
The integrand's **mass per decade of `r` is FLAT** — `0.199, 0.181, 0.202, 0.185` over `1e-6…1e-3`;
`0.139, 0.156, 0.173, 0.155, 0.170` over `1e3…1e7` — and a flat mass per decade IS a logarithmic
divergence. The cutoff study shows a near-constant increment per decade out to `r_max = 1e14` with no
sign of a limit.

**`L6`'s grid reach is `nq_r = 72`, `r ∈ [5.502e-4, 7.270e+3]`.** So: `L5`'s `c_mod = 869.288`,
`L6`'s `ρ = 1.613811231995397` and `L6-b`'s `ρ = 1.504851895102804` are all **correct values of a
72-node truncation**, and what was not previously known is *which* functional they are values of.

**Why eleven legs of scrutiny missed it.** Because the disagreement *shrinks toward the minimiser* —
`6.58e-01`, `4.25e-01`, `4.26e-01`, `3.43e-02`, `1.00e-04` across rungs `J0…J4`. The optimiser
suppresses the divergent tail; that is its job. **The functional is best behaved precisely where it
was always evaluated.** Every evaluation in the record sits at or near a minimiser, and at a
minimiser two truncations of a divergent integral agree to `1e-4` and look like a converged number.

> **THE RULE.** *A verification of an objective that is only ever evaluated AT ITS OWN MINIMISERS
> verifies almost nothing. Evaluate at a point the optimiser has never visited — a restriction, a
> random vector, anything not stationary — BEFORE believing an agreement. And when two independently
> converged quadratures disagree about the same integrand, do not go looking for the coding error
> first: check whether the integral CONVERGES. An objective must be shown to be finite on its own
> trial space before any minimum of it is quoted, and that check — a cutoff sweep, or the mass per
> decade — costs minutes.*

**What this obliges.**
1. `L6-b`'s `ρ = 1.504851895102804` is **HELD**: it is a minimum of a truncation whose value depends
   on the truncation.
2. `L5`'s W4-clause-(b) closure rests on `c_mod = 869.288`, downstream of the same functional.
   **Flagged, not adjudicated** — that is `L5`'s to answer.
3. **§51's queued `L6-e`** (re-run rung `J3` to 20 000 iterations to test whether `L6`'s refinement
   ladder inverts) is measuring this same functional. Its gate is still worth running — an inversion
   is a real finding about the truncation — but its result must be stated as a property of **the
   72-node truncation**, not of `J`.
4. Any future route-4 unit must state its `[r_min, r_max]` **as part of the reported number**, since
   the number is a function of them.
5. `L6` is **NOT** repaired. `L-JVER` was forbidden to and did not.

**What is NOT concluded.** This does **not** say either program is miscoded — the measurement says
the opposite, at `1e-14`. It does **not** say the truncated minima are wrong numbers. It does **not**
move any `L1→L4` link in either direction, and nothing here is progress toward anything. It does
**not** say a blow-up profile does or does not exist: a divergent objective is a statement about a
trial space and a norm as coded, not about Navier–Stokes. And it does **not** establish that a
regularised `J` has a minimiser anywhere near the banked one — `L-JVER` ran no optimiser and that
question is open.

**Ceilings `L-JVER` declared before its answer existed.** The `Y_lm` convention is INHERITED, not
independent (a comparison at a coefficient vector is meaningless otherwise), so a common-mode error
in the convention itself is invisible to this check. The `s` trial space is common in spirit, since
the coefficient vector is defined in it. `Byrd–Lu–Nocedal–Zhu 1995` was **UNREACHABLE** from this
container (two public PDF URLs: one SSL certificate-name failure, one HTML block page) and no depth
was faked. Chandrasekhar 1961 remains unread here, though the identity it carries is now
**RECOMPUTED** independently (`div V = 2.08e-16`).
