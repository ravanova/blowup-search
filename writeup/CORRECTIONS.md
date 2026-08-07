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
