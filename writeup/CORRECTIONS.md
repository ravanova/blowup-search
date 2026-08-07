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
