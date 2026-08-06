# Route-CP v1 (leg 62) — Cadiot arXiv:2505.03091's scope, settled from the full text

**Gate (pre-committed, `DIRECTION.md`):** *Does Cadiot arXiv:2505.03091's construction
cover an operator whose unbounded part is off-diagonal with a non-decaying tail inverse —
i.e. does it already contain leg 58's no-go, or a positive result that contradicts it?*

**Answer: NO** — in the branch's own pre-committed wording: *"The gap leg 57's ledger
measured is confirmed at full-text depth for the one paper most likely to close it. Bank
the located hypotheses as an executable ledger entry; NG may claim novelty against this
paper and no further."*

Runner `experiments/p2_route_cp_v1_cadiot.py` → `writeup/data/p2_route_cp_v1_cadiot.json`.
Figure `writeup/figures/fig56_route_cp_v1_cadiot.png`, rebuilt from that JSON alone by
`experiments/p2_route_cp_v1_cadiot_evidence.py`. Ledger and measurement live in
`solver/certificate_shapes.py` (additive; leg 57's `SHAPE_LEDGER` is untouched), gated by
`test_certificate_shapes.py` gates 16–25. **Every number quoted below is in the JSON.**

---

## 0. Scope, before anything else

`writeup/novelty/leg_62.md`, verdict **`PROCEED_AS_BOOKKEEPING`**, committed *before* any
of this was built. **This leg claims no mathematical novelty of its own.** The
dominance-hypothesis observation is folklore in print — leg 57's finding, unchanged. What
this leg produces is a located, executable scope record plus magnitudes measured against
the paper's own examples.

Three things this document does **not** say:

* not that leg 58's no-go is **true**. A gap in one paper is not a theorem, and leg 58's
  gate is a separate question this leg does not touch. This leg **caps** NG's claim; it
  does not support it.
* not that the standing ban on re-claiming leg 51's finding at full strength is **lifted**.
  The ban's lift condition names this *question*; answering it does not by itself
  discharge the ban. The correct bookkeeping change is a **narrowing annotation**, and
  that is integration-owned.
* not that Cadiot's paper is deficient. Every clause below is a hypothesis that paper
  states plainly and discharges on its own examples — as the measurement confirms.

Nothing here moves any link of the L1→L4 chain. Clay stays at ~0.05% behind Walls 1 and 2.

---

## 1. Why this leg exists and why leg 57 did not close it

Leg 57 located two sentences in this paper (§2's "the operator `L` becomes an infinite
diagonal matrix `L_q`", §3's "By construction `D` is supposed to be diagonally dominant")
and correctly concluded that our observation is folklore. It did **not** establish whether
the paper's *construction* reaches the off-diagonal unbounded part with a non-decaying tail
inverse — which is NG's hypothesis, not leg 51's. The standing ban says so verbatim:

> *lifted by: never — unless a pass resolves whether Cadiot's construction covers a zero
> diagonal, which is now the live open question, not BDL's*

The paper was fetched, not searched: `bash Papers/fetch.sh 2505.03091` (egress probe HTTP
200, 1004 KB, 30 pp., extracted with `pypdf`).

---

## 2. CP1 — six located clauses, and our operator is outside every one

Each row of `CADIOT_SCOPE` carries a section/assumption/lemma number and the sentence
verbatim. `cp_unlocated_rows()` is asserted empty (gate 16); a row citing an abstract is
inadmissible, which is leg 53's failure mode made executable.

| Clause | Where | What it requires | Ours |
|---|---|---|---|
| `CLASS` | §1, eq. (1)–(2) | *"we assume that `L` is a Fourier multiplier operator, that is it is given by its symbol `l`… `F(Lu)(ξ) = l(ξ)F(u)(ξ)`"* | the dilation transport `X d/dX`, **variable-coefficient, no symbol at all** |
| `A1_LMIN` | Assumption 1, first half | *"assume that there exists `lmin > 0` such that `\|l(ξ)\| ≥ lmin` for all `ξ ∈ R^m`"* | `min_k \|diag(tail_block)\| = 0.0` **exactly** |
| `A1_GROWTH` | Assumption 1, second half | *"`lim_{\|ξ\|→+∞} \|l(ξ)\| = +∞`"* | the diagonal is identically zero; the growth is entirely in the **off**-diagonal, `~ k/2` |
| `LEMMA_3_1` | Lemma 3.1, proof | *"`(L + tI)^{-1} : ℓ² → ℓ²` is compact **thanks to Assumption 1**"* | leg 57: the unbordered tail inverse grows linearly in `M` — it does not exist in the limit |
| `LEMMA_3_2` | Lemma 3.2, proof | *"since `DG(U0)L^{-1}` is compact **and `\|l(ñ)\| → ∞`**, there exists `s0 ∈ C` … such that `\|l(ñ) + s0\| > ½ Σ_{k≠n} \|(DG(U0))_{n,k}\|` **for all `n ∈ Z^m`**"* | the required `\|s\|` **grows linearly in the truncation** (§4) |
| `SYSTEMS` | §5.3, eq. (44) | the one systems example: `l(ξ) = [[−λ₁\|2πξ\|²−1, 0], [λ₁λ₂−1, −\|2πξ\|²−λ₂]]` | off-diagonal is a **bounded constant** against an unbounded diagonal (§3) |

The `CLASS` clause is the strongest and it is reached *before* Assumption 1: a Fourier
multiplier is diagonal in the Fourier index by construction (§2.2 spells it out —
`L_q U = (l(n/2q) u_n)_n`), and Remark 2.2 says a polynomial `l` makes `L` "a linear
differential operator with **constant coefficients**". Our unbounded part is
`X d/dX = sin θ ∂_θ`, whose matrix in the sine basis is bidiagonal with **exactly zero
diagonal**. It is outside the class at the level of the class, not at the level of a
hypothesis.

**Forward closure.** Two genuine forward citations, both read at full text, neither
relaxing anything:

* **arXiv:2509.17099** (Blanco–Cadiot–Fassler, cites 2505.03091 as [19]) — Assumption 1,
  verbatim: *"assume there exists `σ₀ > 0` such that `|det(l(ξ))| ≥ σ₀` for all `ξ ∈ R`."*
  This is the **systems** form, and it is the one that matters: a system is the only route
  an off-diagonal entry has into this framework, and the systems hypothesis is a
  **non-vanishing determinant of the matrix symbol**, checked (their Lemma 2.1) not dropped.
* **arXiv:2509.16693** (van der Aalst–Cadiot, cites it as [4]) — establishes an explicit
  positive lower bound on its own symbol. Same hypothesis, discharged by computation.

**One independent candidate**, the strongest off-diagonal one the search produced:
**arXiv:2605.03920** (Castro–Gómez-Serrano–Pascual-Caballo, Burgers–Hilbert). Its
unbounded part *is* a transport term. It is not a counterexample, does not cite
2505.03091, and proceeds by Fuchsian ODE theory to a **finite-dimensional** interval-Newton
system — the Chen–Hou pattern again, the shift case certified by *abandoning* the tail
estimate rather than repairing it, on the torus instead of the line.

**Not obtained, recorded rather than glossed:** Farid–Lancaster, *LAA* 143:7–17 (1991),
Cadiot's [24] and the engine behind Lemma 3.2 — paywalled. It did not need to be obtained:
the load-bearing hypothesis is reproduced inside Cadiot's own proof (the row above).

---

## 3. CP2/CP3 — the hypothesis as a number, on the paper's own examples

A hypothesis you can only quote is a sentence. Cadiot states `l_min` **in words** for three
of his four examples; `cadiot_symbol_admissibility` computes it from the transcribed
symbols and reports the difference.

| Example | `l_min` measured | author states | diff | growth exponent |
|---|---|---|---|---|
| §5.1.1 Swift–Hohenberg (square) | `0.280000` | `0.28` | `+1.42e−07` | `+4.0000` |
| §5.1.2 Swift–Hohenberg (hexagon) | `0.320000` | `0.32` | `+1.42e−07` | `+4.0000` |
| §5.2 capillary-gravity Whitham | `0.200000` | `0.2` | `−5.55e−17` | `+0.5083` |
| §5.3 Gray–Scott (matrix symbol) | `0.999938` | not stated | — | `+2.0000` |

(The Whitham row reproduces his own sentence: *"notice that `l(ξ) ≥ l(0) = 1 − c = 0.2`
for all `ξ ∈ R`."* The Swift–Hohenberg residual `1.42e−07` is grid resolution at the
minimum, which sits at `|2πξ| = 1`.)

**`l_min` for our operator is `0.0` exactly**, and that is not a small number — it is the
absence of the quantity. Ratios against it have no referent, so none are reported
(discipline 73).

**CP3, the one systems example.** §5.3 is the only place an off-diagonal entry appears
anywhere in the paper, so if the framework reached an off-diagonal *unbounded* part it
would have to be here. It does not:

* off-diagonal entry `λ₁λ₂ − 1 = 1/9 = 0.111111`, a **constant**;
* diagonal growth exponent `+2.0000`;
* `|offdiag| / min_i |diag_i|` **exponent `−2.0000`**, value `2.53e−10` at `|ξ| = 1e4`.

For our operator the same ratio is **flat in `k`** (`1/(2μ)` at every mode) and infinite at
`μ = 0`. And Cadiot's off-diagonality is in the **component** index; ours is in the
**Fourier** index — a different axis of the same matrix.

---

## 4. CP4/CP5 — Lemma 3.2's shift: one finite number, or none at all

This is the load-bearing measurement, and it is a statement about his *proof* rather than
an opinion about his paper. Lemma 3.2 imports Farid–Lancaster's generalized Gershgorin
theorem, and to enter it the proof exhibits **one** `s ∈ C`, big enough in amplitude, with

    |λ_n + s| > r_n / 2      simultaneously at every n,      r_n = Σ_{k≠n} |R_{n,k}|.

For real centres the minimum-modulus such `s` is purely imaginary, giving the closed form
`|s| = sqrt( max_n (r_n²/4 − λ_n²)_+ )` — that is `cadiot_shift_requirement`, and it is
computed on whatever matrix it is handed.

| operator | `|s|` at successive truncations | exponent |
|---|---|---|
| **Cadiot §5.2 Whitham**, `N = 128, 256, 512, 1024` | `0.28723` at **every** `N` | `+6.1e−17` — **saturates** |
| **ours, `μ = 0`**, `M = 128…2048` | `63 → 127 → 255 → 511 → 1023` | `+1.0051` |
| ours, `μ = 0.25` | `54.4 → 885.8` | `+1.0060` |
| ours, `μ = 0.45` | `26.5 → 445.0` | `+1.0165` |
| ours, `μ ≥ 0.5` | `0.0` at every `M` | already dominant |

**Linear growth in the truncation means no finite `s` survives the limit**, so Lemma 3.2
cannot be entered at all on our operator — not "the constant is bad", but "the object the
proof needs does not exist".

The same contrast in the underlying quantity (`fig56` panel A): Cadiot's dominance ratio
`r_n/|λ_n|` **decays**, with the ladder `−0.816, −0.738, −0.659, −0.605` over
`N = 128, 256, 512, 1024` — drifting toward the analytic `−1/2` set by his symbol's `sqrt`
growth (it is pre-asymptotic because `l = m_T − c` subtracts a constant). Ours is **flat**:
exponent `+0.0039` at every `μ > 0`, identically to 13 digits, if anything very slightly
*increasing*; and **refused** at `μ = 0`, where all 502 interior rows have an exactly zero
diagonal and the ratio has no referent.

### CP5 — the control can report the other answer, and it does

The Whitham row above is a positive control run through the identical code path: **his**
symbol `l(ξ) = m_T(2πξ) − c` (`T = 0.5`, `c = 0.8`) exactly on the diagonal, plus a
finitely-supported convolution off it — which is what `DG(U0)` is for his
`F(u) = M_T u − c u + u²`.

**The convolution is a surrogate and is labelled one.** His `u₀` is not distributed with
the paper. The surrogate is built so it *cannot* carry the conclusion: its `ℓ¹` norm is a
dial, and its centre coefficient is set to zero on purpose (a convolution's centre lands on
the diagonal, where it only *helps* his dominance, so zeroing it is the choice that is
conservative **against** his framework).

Lesson 90 says four identical numbers should read as a bug. Here is why they do not:

* the level **moves** with the operator — `|s| = 0.0, 0.28723, 1.98997, 9.99800` as
  `‖V‖₁ = 0.05, 0.35, 2.0, 10.0`;
* the ratio's **exponent does not move at all** — spread `4.1e−15` across those four —
  because the numerator is exactly `2‖V‖₁` in the interior, so the exponent belongs to
  **Cadiot's symbol alone**;
* and the binding row is the one Assumption 1 is *about*:
  `|s| = sqrt((r/2)² − l_min²) = sqrt(0.35² − 0.2²) = 0.28723`, matching the measurement
  exactly. **The shift his proof needs is set by his own `l_min`.**

---

## 5. CP6 — three numbers on one dial, kept apart

Two published hypotheses land on the *same* `Λ¹`-dissipation dial at *different* places,
and neither is the operator's own hinge. Conflating them is how a hypothesis of a
construction gets read as a property of an operator.

* **Cadiot Lemma 3.2** admits this family for **`μ ≥ 0.5`** — measured: `μ = 0.45`
  diverges (exponent `+1.0165`), `μ = 0.50` needs `|s| = 0` exactly. The mechanism is an
  identity, checked not assumed: `r_k = k − 1` exactly for the interior rows of
  `tail_block` (max error `≤ 5.7e−14` over `μ = 0.25, 0.45, 1.0`), against a diagonal
  `μk`, so the condition is `μk > (k−1)/2`.
* **BDL assumption (5)** admits it only for **`μ > 1`** (`δ = 1/(2μ) < 1/2`).
* **The operator's own hinge** (leg 57, a different quantity — the tail inverse's
  finiteness in `M`) is **`μ = 0` exactly**.

The factor between the two published thresholds is exactly **2**: Gershgorin bounds the
whole row sum with a `½`, BDL bounds each ratio separately. **Both are vacuous at `μ = 0`,
which is the case of interest.** This does not contradict leg 57 — it measures a different
quantity and says so.

That `r_k = k − 1` identity is also why the ratio's exponent is `μ`-independent (`+0.0039`
at every `μ`, spread `< 1e−9`) while its level moves — `3.992, 1.996, 0.998, 0.499` at
`μ = 0.25, 0.5, 1, 2`. **A level alone cannot make a tail estimate close.**

---

## 6. CP7 — the gate, and it can answer both ways

`cadiot_covers()` answers off the located clauses: **`no`**, with `6` of `6` clauses
failing and `0` of `3` forward citations relaxing anything. Lesson 90 again — the predicate
flips to `yes` two independent ways, both exercised in `test_certificate_shapes.py` gate 18:

* `CP_SYNTHETIC_COVERING_SCOPE`, a fictitious clause set that our operator satisfies;
* setting `relaxes_the_hypothesis` on any `CP_FORWARD` row.

So `no` is a property of the located clauses, not of the code.

---

## 7. What this establishes, and its ceiling

**Establishes.** arXiv:2505.03091 does not cover an operator whose unbounded part is
off-diagonal with a non-decaying tail inverse, and it fails to on **six independent located
clauses** rather than one. The obstruction is quantitative: Lemma 3.2 needs one finite `s`
serving every mode, and on our operator the required `|s|` grows **linearly** in the
truncation (exponent `+1.005` over `M = 128…2048`) while on Cadiot's own Whitham operator
it is a single number, `0.28723`, unchanged across `N = 128…1024` and predicted exactly by
his own `l_min = 0.2`. Both forward citations restate the hypothesis; the systems form is
`|det(l)| ≥ σ₀ > 0`.

**Ceiling.** Four papers is a corpus, not a theorem. Every `quote` here is **transcribed**
from a full text by a human-equivalent process and is exactly as good as that — the `url`
is on every row so the next pass can check rather than trust. The measurement is float64,
no intervals: every number is a measurement of a matrix. The Whitham control's `DG(U0)` is
a surrogate (§5). And a gap in one paper is not a theorem: **NG may claim novelty against
this paper and no further.**
