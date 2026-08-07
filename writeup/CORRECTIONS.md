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
