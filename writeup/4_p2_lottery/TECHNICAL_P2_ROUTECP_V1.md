# Route-CP v1 — The Cadiot pre-emption, settled from the full text

**Leg 62. Branch `leg/cp-v1`. Claim-bearing (literature classification).**
Runner: `experiments/p2_route_cp_v1_cadiot.py` ·
Data: `writeup/data/p2_route_cp_v1_cadiot.json` ·
Figure: `writeup/figures/fig56_route_cp_v1_cadiot.png` ·
Ledger: `solver/certificate_shapes.py` (`CP_LEDGER`), `solver/literature_gates.py`
(the re-derivations) · Gates: `test_certificate_shapes.py` 22/22,
`test_literature_gates.py` 11/11 · Novelty pass: `writeup/novelty/leg_62.md`.

---

## 1. The question, and why leg 57's answer was not enough

Leg 57 flagged Cadiot arXiv:2505.03091 as independently pre-empting leg 51's
methodological claim and recommended not re-claiming that finding at full strength. That
recommendation was correct. It was also incomplete, for a specific reason: **leg 58's
(NG's) hypothesis is narrower than leg 51's.**

Leg 51's claim was about a general observation — the standard radii-polynomial tail
estimate presumes an asymptotically diagonal Fréchet derivative. Leg 57 settled that: it
is folklore in print, and Cadiot §2/§3 is where it is in print.

NG's proposition is a different sentence. It is about an unbounded part that is
**off-diagonal**, with a **non-decaying tail inverse**. Leg 57 read two sentences of
Cadiot off a search index and explicitly declined to say whether the construction reaches
that case. That undecided question is the largest single novelty risk to NG, and it is
what this leg settles.

The standing reason to settle it from the PDF and nowhere else is banked twice over. Leg
53 read BDL's dominance hypothesis off a publisher abstract page, claimed against it, and
lost the claim; only the full PDF fixed it. That correction is a ban in
`plan_of_record.py`, and this leg is bound by it.

**The gate, verbatim:**

> Does Cadiot arXiv:2505.03091's construction cover an operator whose unbounded part is
> off-diagonal with a non-decaying tail inverse — i.e. does it already contain leg 58's
> no-go, or a positive result that contradicts it?

**Answer: NO.** Over four papers fetched and read in full
(`Papers/fetch.sh 2505.03091 2504.05066 2404.08529 2302.12877`), 19 located statements,
none from an abstract.

---

## 2. The answer, and the three independent reasons for it

The NO is not a gap in the paper's coverage. It is the paper's **defining hypothesis**,
which is a stronger and more durable form of NO — a later revision could fill a gap, but
not without becoming a different paper.

**(i) Assumption 1 (§2.1), verbatim.**

> "Let `l` be defined in (2). Assume that there exists `ρ > 0` such that `l` is analytic
> on the strip `I_ρ = {z ∈ C^m, |Im(z)|_∞ ≤ ρ}` … Moreover, assume that there exists
> `l_min > 0` such that `|l(ξ) ≥ l_min` for all `ξ ∈ R^m` and
> `lim_{|ξ|_2 → +∞} |l(ξ)| = +∞`."

Read together with eq. (2), `F(Lu)(ξ) = l(ξ) F(u)(ξ)`, this says the unbounded part is a
**Fourier multiplier**: constant-coefficient, hence exactly diagonal in the Fourier
basis, and additionally bounded below. Our unbounded part is a variable-coefficient
transport term `a ũ ∂_x`. It is outside the class by definition — and it is precisely the
*variable coefficient* that makes it off-diagonal.

**(ii) The diagonality is load-bearing inside a proof.** Proof of Lemma 3.3, §3:

> "Now, since `L` is diagonal, we have that `L π_N = π_N L π_N` and therefore
> `(P^N)^{-1} DF(U_0) π_N = (P^N)^{-1} DG(U_0) π_N` and
> `π_N DF(U_0) P^N = π_N DG(U_0) P^N`."

This is the step that **removes the unbounded part from the off-diagonal blocks**, so
that the Gershgorin radii `r_n` involve only the bounded `DG(U_0)`. When the unbounded
part is off-diagonal this identity simply fails and `r_n` inherits the unbounded entries.
That is exactly NG's mechanism, and it is the one place in the paper where the mechanism
could have been met. It is not met; it is assumed away.

**(iii) Relative compactness.** Lemma 2.2 (§2.3): `DG(ũ)` is *"relatively compact with
respect to `L`"*. A transport term of the same order as the unbounded part is not
relatively compact with respect to anything in this setup.

And the tail bounds decay for exactly the reason our object lacks. Remark 4.1: `Z_{u,1},
Z_{u,2} ≤ C e^{−2πρd}`, *"where `ρ` is given in Assumption 1"*.

### The near miss, which is the most informative row

§5.2 is the capillary-gravity Whitham equation, `u_t + ½ ∂_x M_T u + u ∂_x u = 0` — the
**one** equation in the paper carrying a transport term. It never becomes an unbounded
off-diagonal operator, because the traveling-wave reduction divides out `∂_x`: the
equation collapses to `F(u) = M_T u − c u + u²`, and `DG(ũ) = 2ũ` is a **bounded
multiplication operator**. The gCLM/CLM linearisation admits no such reduction. This is
worth stating plainly because it is the shape of every apparent counterexample one might
chase: transport appears, and is disposed of before it reaches the linear part.

---

## 3. What Cadiot cites forward, and the one finding that caps NG

The gate required doing the same for what the paper cites forward into this case. Three
citations could plausibly have carried it, and one of them changes what NG may *say*.

### BRT — Breden, Payan, Reisch, Tang, arXiv:2504.05066 (Cadiot's [15])

Cadiot describes this as deriving a generalized Gershgorin theorem *"under very broad
assumptions … whenever a linear operator is expressed on an adequate Schauder basis"*. It
is the most general Gershgorin statement located anywhere in this project, and it is the
dangerous one. **It removes the hypothesis NG would most naturally have leaned on.** §2.1:

> "some of the assumptions of [FL91, Theorem 2.1] are needlessly restrictive (for
> instance, **all the diagonal elements of `L` have to be nonzero**), and others may not
> be straightforward to check in practice … We propose below a simpler and slightly more
> general statement."

Their Theorem 2.6 requires only a Schauder basis, a sup-attaining property (2.2), and a
**compact resolvent** — nothing whatever about the diagonal.

**Consequence, and NG must act on it: a no-go phrased as "the published machinery
requires a nonzero diagonal" is FALSE against a 2025 paper.**

This costs NG nothing in substance, because the generalised theorem *applies* to a zero
diagonal and says nothing. Definition 2.5: *"We note that its radius `r_i(L)` can be
infinite."* With a zero diagonal and divergent row sums every disk is `D(0, ∞) = C`. The
theorem is **vacuous, not violated**. All the content sits in whether the radii can be
made finite *and* smaller than the diagonal.

And BRT say exactly what that takes. They hit infinite radii themselves (§2.2: *"we get
no information … as some of the disks have infinite radius"*), repair them with a
diagonal weight (Definition 2.8), and the repair works under a **quantitative, published
inequality** — Lemma 2.10 with (H:B):

> `p ∈ (1 − q_2, q_1 + 2/n)` … `r_{2i+1}(M̃) ≤ C'|δ| i^{p−q_1} + |c|` …
> `M̃_{2i+1,2i+1} + r_{2i+1}(M̃) ≤ −κ i^{2/n} + C'|δ| i^{p−q_1} + d + |b|`. *"Since `θ, κ,
> C' > 0` and `p − q_1 < 2/n`, the right hand side … is negative for all `i` large
> enough."*

Off-diagonal row-sum growth **strictly below** diagonal growth. That is the predicate, in
print, in the form NG's proposition should take.

### CB — Cadiot & Blanco, arXiv:2404.08529 (Cadiot's [20])

The systems extension — the only mechanism by which the framework could acquire an
off-diagonal entry in the *linear* part at all. Assumption 1: `l` is a `k × k` **matrix
of polynomials** in `ξ` with `|det(l(ξ))| ≥ σ_0 > 0`. Still constant-coefficient, so
still a multiplier: block-diagonal by frequency, with finite blocks — precisely the case
MM-1 already proves. Remark 2.1 calls the hypothesis *"necessary for constructing a
contracting Newton-like fixed point operator"*.

The instance is the sharpest datum in the ledger. Cadiot §5.3 eq. (44), `λ₁ = 19,
λ₂ = 10`: the off-diagonal entry is `λ₁λ₂ − 1 = **189**, a constant, while the diagonal
grows like `|2πξ|²`. The one off-diagonal entry in the corpus is bounded and dominated.

### FL91 — Farid & Lancaster, *Linear Algebra Appl.* 143:7–17 (1991) (Cadiot's [24])

The theorem Cadiot's Lemma 3.2 actually invokes. **Paywalled, no arXiv copy, and this leg
did not read it.** Its row is flagged `SECOND_HAND`, carries `rho = None`, and
`cp_gate_answer` **refuses** it rather than counting it either way. That is leg 53's
correction applied as code rather than as a resolution.

It does not matter for the gate, because Cadiot's own discharge of it was read first-hand
(proof of Lemma 3.2): he establishes *shifted strict diagonal dominance with finite row
sums*, `|λ_n + s| > ½ Σ_k |R_{n,k}|`. Our operator has neither.

---

## 4. The axis: why `ρ`, and not the exponent difference

`SHAPE_LEDGER` (leg 57) classifies by label — MULTIPLIER / SHIFT. A label cannot express
what the sources actually require, which turned out to be an **ordering of growth rates**.
So `CP_LEDGER` carries two magnitudes per row,

- `γ_D` — growth exponent of the diagonal,
- `γ_R` — growth exponent of the (weighted) off-diagonal **row sum**,

and the gate reads the asymptotic Gershgorin dominance ratio

> `ρ = limsup_k (off-diagonal row sum at k) / |diagonal entry at k|`, which every located
> construction needs `< 1`.

**`ρ` is the right coordinate and `γ_D − γ_R` is not**, and BDL is the row that proves it:
BDL has *equal* exponents (`γ_D − γ_R = 0`) and is still admissible, because assumption
(5) buys `ρ ≤ 2δ < 1` on a constant factor. Any classification by exponent alone would put
BDL on the wrong side. Panel A of fig56 is this plane; BDL sits on the boundary and is
marked as such.

| source | `γ_R` | `γ_D` | `ρ` |
|---|---|---|---|
| Cadiot §5.1 Swift–Hohenberg | 0 | 4 | 0 |
| Cadiot §5.3 Gray–Scott = CB | 0 | 2 | 0 |
| Cadiot §5.2 Whitham | 0 | 0.5 | 0 |
| BRT Lemma 2.10 (`p=1.7, q₁=1, n=1`) | 0.7 | 2 | 0 |
| BDL (4)+(5), `s_L=1` | 1 | 1 | `≤ 2δ < 1` |
| **OURS** a=0 CLM bordered tail | **1** | **0** | **∞** |

Every number in that table is in the JSON.

---

## 5. The transcription is re-derived, not trusted

Transcription is where errors hide, so `solver/literature_gates.py` recomputes from
Cadiot's published formulas at his published parameters. If Assumption 1 failed at his own
numbers, this leg's whole reading would be wrong.

| check | measured | expected |
|---|---|---|
| Swift–Hohenberg `l_min` (§5.1, `µ=0.32`) | **0.3200** | `µ` = 0.32 |
| Swift–Hohenberg growth exponent | **4.0000** | 4 |
| Whitham `l_min` (§5.2, `T=0.5, c=0.8`) | **0.2000** | `1 − c` = 0.2 |
| Whitham growth exponent | **0.5017** | ½ |
| Gray–Scott `σ₀` (§5.3, `λ₁=19, λ₂=10`) | **10.000** | `λ₂` = 10 |
| Gray–Scott off-diagonal entry | **189** (constant) | `λ₁λ₂ − 1` |
| Gray–Scott dominance crossover | `ξ* = ` **2.1293** | — |
| Gray–Scott `ρ` decay exponent | **−1.9967** | −2 |

The Whitham row is the tightest hypothesis in the paper and worth naming: `T = 0.5` sits
*above* the critical Bond number `1/3`, so `m_T` increases from `m_T(0) = 1` and the
infimum of `|l|` is attained at `ξ = 0` at `1 − c = 0.2`. Assumption 1 holds by a margin
of 0.2, not by a wide one, and its growth exponent is only ½ — the weakest unbounded part
in the corpus. **Even there, `γ_D = 0.5 > γ_R = 0`.** The ordering never reverses.

---

## 6. Why the one published repair cannot reach us — and why legs 51–53 measured what they measured

BRT repair infinite Gershgorin radii by conjugating with a **diagonal weight**
`Q = diag(1/f(i))`, `f(i) = max(1, i^p)` — which is *the same one-parameter family legs
51–53 swept as the weight exponent `s`*. Conjugation maps entry `(i,j)` to
`(f(i)/f(j)) M_{i,j}`. So:

> For a **nearest-neighbour** coupling, `j = i + offset` with `offset` fixed,
> `f(i)/f(i+offset) = (i/(i+offset))^p → 1` as `i → ∞`, **for every `p`.**

A diagonal weight cannot damp a shift, because a shift's entries live a *bounded distance*
from the diagonal and any diagonal weight is asymptotically flat there. Measured
(`shift_damping_ladder`): at index 8192, over `p ∈ {0, 0.5, 1, 2, 4}`, the weight damps a
nearest-neighbour coupling by **at most 4.88 × 10⁻⁴**. That is not a repair.

The contrast is what makes this a finding rather than an isolated fact. BRT are not
damping a shift — their `B_{i,j}` is **bounded and spread across the whole row**
(hypothesis (H:B): `|B_{i,j}| ≤ C / (max(1,i^{q₁}) max(1,j^{q₂}))`), merely non-summable.
Against *their* operator the same weight works, and `spread_damping_ladder` reproduces
their own published exponent:

| `p`, `q₁` | measured growth exponent | BRT's `p − q₁` | error |
|---|---|---|---|
| 1.2, 1.0 | +0.2000 | +0.2000 | 2.4e−15 |
| 1.7, 1.0 | +0.7000 | +0.7000 | 8.9e−16 |
| 2.5, 1.0 | +1.5000 | +1.5000 | 0.0 |

**This is the mechanism behind legs 51–53's measured "the coupling entry is `K/2` for
EVERY `s`".** That was recorded as a measurement with no explanation; it now has one, and
the explanation is an identity rather than a sweep. Panel B of fig56 is both ladders.

---

## 7. What this caps, for leg 58 (NG)

**NG may claim novelty against arXiv:2505.03091, arXiv:2504.05066, arXiv:2404.08529 and
arXiv:2302.12877 — and no further.** Four papers read in full is a corpus, not a theorem.

**NG must not phrase its no-go as a structural prohibition on a zero diagonal.** That
wording is false against BRT §2.1. The recommended wording is the quantitative one, which
is true, defensible, and is BRT Lemma 2.10's own requirement:

> No located construction covers an operator whose off-diagonal **row-sum growth** exceeds
> its **diagonal growth**.

NG may additionally use the diagonal-weight identity of §6 as the reason no reweighting
closes the gap.

---

## 8. What this does NOT establish

- **Not that no such construction exists.** A NO here is *"no located source covers
  this"*, over four papers. It is a bounded statement about a corpus.
- **Not a mathematical finding of this leg.** The observation is folklore in print (leg
  57). What is new here is the *reading depth* and the *axis*, both of which are
  bookkeeping. The novelty pass (`writeup/novelty/leg_62.md`) records the verdict
  `PROCEED_AS_LEDGER_EXTENSION` and it binds this document.
- **Not a first-hand reading of FL91.** It is paywalled; its row is refused by the gate.
- **Not rigorous.** Float64 on grids, no intervals. The `l_min` values are minima over
  grids and the growth exponents are least-squares fits over three decades. They say the
  published hypotheses are consistent with the published parameters; they prove nothing.
- **Nothing here moves any link of the L1→L4 chain.** Clay stays at ~0.05% behind Walls 1
  and 2.
