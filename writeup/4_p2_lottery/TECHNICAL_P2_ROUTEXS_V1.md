# Route-XS v1 (leg 57) — the shape dichotomy against published certificates

**Branch** `leg/xs-v1`. **Exploration leg, not critical path.** **Gate answered: NO.**
**Data** `writeup/data/p2_route_xs_v1_shapes.json`. **Figure** `fig52_route_xs_v1_shapes.png`.
**Module** `solver/certificate_shapes.py`, **gates** `test_certificate_shapes.py` **15/15**.
**Runner** `experiments/p2_route_xs_v1_shapes.py` (357 s on a contended box, deterministic -- the numbers reproduce exactly).

---

## 0. What this leg was for, and the one thing it may not claim

Legs 51–53 explained Route-TC's failure with lesson 87:

> A certification method has a SHAPE, and the shape is a property of the OPERATOR. The
> standard radii-polynomial tail estimate closes because the unbounded part is a
> **multiplier** — cut an entry of size `Λ_M` and the tail inverse is `1/Λ_M`. Here it is
> **off-diagonal** (a shift), and the bordered tail inverse is a **constant**
> (2.19 … 10.32), not `1/K`.

If `MM` answers NO, that sentence becomes the lane's epitaph. **An epitaph with no
external check is a mood, not a finding.** This leg supplies the check.

**And the novelty pass, run first and committed before any construction
(`writeup/novelty/leg_57.md`, verdict `PROCEED_AS_BOOKKEEPING`), settled the ownership
question against us.** The observation is folklore in print. Cadiot, arXiv:2505.03091,
states both halves in one paper:

* §2, on the periodic counterpart: *"the operator `L` becomes an infinite diagonal matrix
  `L_q` with entries `l(n/2q)` on the diagonal."*
* §3 opening, *Spectrum of `DF(U₀)` using Gershgorin disks*: *"By construction `D` is
  supposed to be diagonally dominant, which hints to the Gershgorin theorem."*

**This leg therefore classifies known practice; it does not discover it.** That is
consistent with — and sharpens — the standing ban from legs 51/53. What is not in print
is the classification as an *executable ledger*, and that is a bookkeeping artifact whose
only virtue is that it does not decay at the rate of memory (lesson 68). It is not a
result and is not written up as one.

---

## 1. The ledger: four published certificates, eleven located statements

`SHAPE_LEDGER` in `solver/certificate_shapes.py`. Vocabulary is closed (test 3), every row
carries a resolvable arXiv link (test 2), and **every classification is traced to a located
full-text statement — section, assumption or proposition number, plus the sentence
verbatim.** `unlocated_rows()` is the guard and test 1 asserts it empty. Leg 53 lost a
claim by reading BDL's *abstract*; that failure is now a test, not a habit.

| | radii-poly? | unbounded part | approx. inverse | tail inverse decays? |
|---|---|---|---|---|
| **CLN** [2302.12877](https://arxiv.org/abs/2302.12877) | yes | **multiplier** | block-diagonal | **yes** |
| **BDL** [1503.06315](https://arxiv.org/abs/1503.06315) | yes | tridiagonal-dominant | **NOT block-diagonal** | **yes** |
| **CH** [2210.07191](https://arxiv.org/abs/2210.07191) + 2305.05660 | **no** | **SHIFT** | none built | n/a |
| **DF** [2410.05480](https://arxiv.org/abs/2410.05480) | no | (none — finite-dim) | finite Jacobian | n/a |

### 1.1 CLN — the multiplier hypothesis, stated as a hypothesis

**Assumption 2.1:** *"Assume that the Fourier transform of the linear operator `L` is given
by `F(Lu)(ξ) = l(ξ)û(ξ)`, for all `u ∈ S`, where `l` is a polynomial in `ξ`. Moreover,
assume that `|l(ξ)| > 0`, for all `ξ ∈ R^m`."* That is the multiplier classification,
verbatim, as a standing assumption of the method.

**§1, literature review, the periodic case** — the clearest statement in the corpus, and it
gives the *reason*, which is what makes it more than a coincidence:

> *"One of the main ingredients … is to exploit the fact that the Fréchet derivatives are
> (asymptotically) diagonally dominant. … Therefore, the tail of `DF(U₀)` can be seen as a
> diagonally-dominant infinite dimensional matrix. From this, one can approximate the
> inverse of `DF(U₀)` as a finite matrix acting on a finite part of the sequence, and a
> tail operator (which is diagonal) which acts on the tail of the sequence."*

**The block-diagonal `A` is downstream of the multiplier. It is not an independent design
choice, and that is exactly why MM is spending the last free choice on it.**

**Remark 2.7** gives the abstract form: *"`DG(u₀)` is relatively compact with respect to
`L` … the essential spectrum of `DF(u₀) = L + DG(u₀)` is equal to the essential spectrum of
`L`."* A transport term of the same order as the unbounded part is not relatively compact
with respect to it — which is the dichotomy in one line, in someone else's notation.

`solver/target_selection.py` already reproduces this paper's Kawahara `r₀`; nothing here
re-derives it.

### 1.2 BDL — the row that matters for MM

BDL is **not** the diagonal case, and their own abstract says so: *"Since `Df(x̄)` does not
have an asymptotically diagonal dominant structure, the computation of `A` is not
straightforward."* **They publish a non-block-diagonal approximate inverse** — an LU
factorisation of the tridiagonal tail, with `A`'s finite block carrying a nonzero coupling
to the tail (their eq. (21)). §1: *"In [3,4,6,7,9,5] the nonlinear equations under study
have asymptotically diagonal or block-diagonal dominant linear part … In contrast, the
present work considers problems with tridiagonal dominant linear part. To the best of our
knowledge, this is the first attempt."*

**So MM's remaining move is not unprecedented. What matters is what it costs, and the
paper is explicit.** Two assumptions buy it:

* **assumption (4):** `C₁ ≤ |μ_k| / ω_k^{s_L}` for `k ≥ k₀` — **the diagonal is bounded
  below, at the same growth rate that makes the operator unbounded.** (This is LIT's ninth
  pass finding, now confirmed at full text rather than from the abstract.) **Transcription
  note, carried in the ledger row:** this display's fractions come through `pdftotext`
  stacked and out of order, so the ledger's rendering of (4) is a **reconstruction, not a
  verbatim copy**, and is labelled as such. The load-bearing clause — a *lower* bound on
  the diagonal — is unambiguous in the extraction. A reconstruction presented as a
  quotation would defeat the point of this leg.
* **assumption (5):** `|λ_k/μ_k|, |β_k/μ_k| ≤ δ < 1/2` — the off-diagonals are strictly
  subordinate. *"Tridiagonal dominant"* means the diagonal dominates **within** a
  tridiagonal operator. It is a near-multiplier, not a shift.

And **Proposition 2.3:** *"Assume that `m ≥ k₀` and `δ < 1/2`. Then `A` maps `Ω^s` into
`Ω^{s+s_L}`."* The pseudo-inverse **gains `s_L`** — the same decay the pure multiplier case
gives. The tridiagonal structure costs nothing in the decay rate; **the diagonal lower
bound is what buys it.**

Their §5 future-work list asks to relax the *symmetry* in (5) and to extend to
block-tridiagonal structures. **A vanishing diagonal is not on that list.**

### 1.3 Chen–Hou — the row most likely to be misread

Chen–Hou certify an operator whose unbounded part **is** a transport term. If the
classification stopped at "unbounded part = shift" they would read as a refutation. They
are the opposite, and the located statement says why.

**Part I §2.7,** *The local parts and functional spaces*:

> *"we will perform weighted energy estimate in some suitable space `X` and derive the
> damping terms in the weighted energy estimate from the local terms, especially the
> advection term `(c̄_l x + ū)·∇f` in (2.30)."*

**The one published computer-assisted proof whose unbounded part is a shift does not invert
it and does not estimate its tail. It extracts damping from the advection term itself.**
The shift is the *source* of the coercivity rather than the obstruction to it. Part I §2.6
supplies the sign condition — `c̄_l x + ū(x,y) ≥ c₁x`, `c₁ ≈ 0.47` — which is a **pointwise
inequality on the profile**, and therefore has no expression in an `ℓ¹`-Fourier tail
estimate at all.

**A negative located observation, reported as a checkable search rather than an
impression:** the strings *"radii polynomial"*, *"Newton–Kantorovich"*, *"approximate
inverse"* and *"contraction mapping"* **do not occur in either Part I or Part II**.

Chen–Hou is banned as a *target* (leg 45 M1: already certified) and is admitted here only
as a classification datum.

### 1.4 Dåhne–Figueras — in the ledger to record that it is silent

**§4, eq. (8):** *"we can treat `G` as a map from `R⁴` to `R⁴`. To prove the existence of a
root we make use of the so-called interval Newton method."* There is no infinite tail and
no approximate inverse of an unbounded operator; the infinite-dimensionality is discharged
by rigorous ODE integration *before* the Newton step. This paper is silent on the
dichotomy, and the row exists so that its silence is recorded rather than counted. Leg 48
re-derived its branch; nothing here repeats that.

---

## 2. The gate, as a predicate that can answer both ways

```
is_counterexample(row)  ==  row.is_radii_polynomial
                       and row.unbounded_part == SHIFT
                       and row.tail_inverse_decays is False
```

**Answer: NO. 0 of 4** (`XS2_gate`). Each clause does work, and the two near-misses fail
**different** clauses (test 7) — which is the substance of the classification:

* drop `is_radii_polynomial` and **Chen–Hou** become a spurious counterexample; they have
  the shift and form no tail estimate.
* drop `unbounded_part == SHIFT` and **BDL** become one; they have a non-block-diagonal `A`
  and a diagonal bounded below.

**Lesson 90 is honoured explicitly.** A fictitious `SYNTHETIC_CONTROL` row satisfies all
three clauses. Admitting it flips the same predicate to **yes** (test 5). Without it, the
"no" would be a property of the code rather than of the literature — which is precisely the
failure leg 53 shipped and VERIFIER caught.

---

## 3. The dichotomy, measured rather than asserted

The labels above are not decorations: `classify_operator` returns them **from a
measurement**. The object is `solver/spectral_certificate.tail_block` — the `a = 0` CLM
linearisation's far-field block, off-diagonal entries `~ k/2`, **diagonal exactly zero** —
and `mu` adds `mu·k` to the diagonal (`Λ¹` dissipation). **`mu` is a continuous path from
shift to multiplier.** Norm: `‖M‖_w = max_j (1/w_j) Σ_i w_i |M_ij|`, flat `ℓ¹`.

| `mu` | shape | `M`-exponent | `K`-exponent | decays? |
|---|---|---|---|---|
| **0.0** | **SHIFT** | **+1.021** | **+0.437** | **NO** |
| 0.25 | tridiag-dom | +0.000 | −0.849 | yes |
| 0.5 | tridiag-dom | −0.000 | −0.886 | yes |
| 1.0 | tridiag-dom | +0.000 | −0.915 | yes |
| 2.0 | multiplier | +0.000 | −0.933 | yes |
| 4.0 | multiplier | +0.000 | −0.946 | yes |

**Exactly one row fails, and it is the only row whose diagonal is exactly zero.**

### 3.1 Two different failures, and legs 52–53 are each one of them

**(XS2) Existence.** At `mu = 0` the *unbordered* tail inverse at `K = 8` runs
**17.14 → 35.43 → 72.0 → 145.14 → 291.43** over `M = 128 … 2048`: exponent **+1.021**,
linear. **It does not exist in the limit.** That is what forced leg 52 to border. Note it is
finite at every `M` — the divergence is visible only as a ladder (lesson 72).

**(XS3) Size.** Bordered, the same quantity **saturates**: `3.041 → 3.250`, exponent
**+0.023**. **Leg 52's repair works, and this is the check that it does.** But in the split
`K` the bordered inverse runs

> **2.191 → 3.234 → 4.653 → 6.530 → 8.890 → 11.528** over `K = 4 … 128`, exponent **+0.437**, ratio **5.26×**.

**This sharpens legs 52–53's own headline.** The bordered tail inverse is *not* "a constant
rather than `1/K`". **It is not a constant at all — it grows.** The 2.19 those legs quote is
**the smallest rung of a rising ladder**, not a bound. A tail estimate needs this quantity
to fall like `1/Λ_K`; it rises.

### 3.2 The hypothesis this leg posed, checked, and killed

BDL's admissibility is `δ = |off-diag|/|diag| < 1/2`. For this operator (off-diagonal
`~ k/2`, diagonal `mu·k`) that is `δ = 1/(2·mu)`, so **BDL-admissible means `mu > 1`.** The
obvious hypothesis — appealing, and wrong — was that the tail inverse stops behaving at
`mu = 1`.

**REFUTED.** `mu = 0.25` has `δ = 2`, four times **outside** BDL's admissible set, and is
boundedly invertible with `K`-exponent **−0.849** — indistinguishable in character from
`mu = 2`. **`δ < 1/2` is what BDL's LU construction needs; it is not where the operator
changes character. The hinge is zero-versus-nonzero diagonal, and `δ` is not the coordinate
for it.** Kept as test 14 so the dead hypothesis cannot quietly return.

### 3.3 The wrong construction, kept in the artifact (lesson 76)

Bordering a `mu > 0` tail with the `mu = 0` near-null pair gives, at `K = 4`:
**1.06e+03** (`mu = 0.25`), **2.06e+04** (`mu = 1`), **8.26e+04** (`mu = 2`) — apparently
catastrophic next to the `mu = 0` bordered 2.191. **That reading is wrong and leg 53 already
banked why:** at `mu > 0` the tail block has no kernel, so bordering it with a pair that is
not near-null *for that operator* adds a spurious almost-dependent row and column. It is the
wrong operator, not the wrong answer. The comparison across `mu` must use the unbordered
inverse wherever the block is invertible, which is what `classify_operator` does. The
numbers are recorded (`XS5`) **only so the next agent recognises them instead of publishing
them.**

---

## 4. The gate answer, in its pre-committed wording

> **Gate.** Is there a published radii-polynomial certificate whose unbounded part is
> OFF-DIAGONAL (a shift) and whose tail inverse does not decay — i.e. a counterexample to
> the dichotomy legs 51-53 rest on?
>
> **NO** → The dichotomy is a real classification, TC/MM's negative generalizes beyond this
> repository, and it is banked as an executable ledger entry with links. Stop restating the
> multiplier/shift explanation without this ledger as its citation.

---

## 5. Scope — what this establishes, and what it does not

**Establishes.** Across the four published computer-assisted certificates this repository
cites, no radii-polynomial certificate has an off-diagonal unbounded part whose tail
inverse fails to decay. The two near-misses fail for different and informative reasons: BDL
publish the non-block-diagonal `A` that MM is about to try, and still require a diagonal
bounded below; Chen–Hou certify a genuine transport operator and do so by **abandoning the
tail estimate entirely**. So the dichotomy is a real classification of the published record,
and TC/MM's negative is not an artifact of this repository.

**Does not establish.**

* **That no such certificate could exist.** Four papers is a corpus, not a theorem, and
  every ledger row is **transcribed** from a full text by a human-equivalent process. The
  `url` on each row is there so the next pass can check the quote rather than trust it.
* **That the dichotomy is this leg's finding.** It is folklore in print (§0).
* **That Chen–Hou's method ports.** It is the obvious next thing to look at and **nobody has
  run it.** This leg does not claim the port works, and saying "there is a template" is not
  the same as saying it applies.
* **Anything about `HL_S2_nonsymmetric`**, or about any link of the L1→L4 chain. Clay stays
  at ~0.05% behind Walls 1 and 2. **In 57 legs no link has moved.**

**Forward consequence for MM, stated as a statement about BDL and not as a prediction.**
MM's one remaining free choice is the shape of `A`. BDL is the published instance of that
move, and this ledger locates what it costs: Proposition 2.3 delivers the same decay gain
`s_L` as the pure multiplier case, **but only under assumption (4), a diagonal bounded below
at the growth rate.** The published precedent for MM's move does not carry over to a zero
diagonal. **MM measures its own object and this leg does not pre-empt its gate.**

---

## 6. Reproducing

```
.venv/bin/python test_certificate_shapes.py                       # 15/15
.venv/bin/python -u experiments/p2_route_xs_v1_shapes.py          # regenerate JSON (357 s)
.venv/bin/python experiments/p2_route_xs_v1_shapes_evidence.py    # rebuild fig52 from JSON
```

Source PDFs are re-pullable with `bash Papers/fetch.sh 1503.06315 2302.12877 2410.05480
2210.07191 2305.05660` (`Papers/` is gitignored on purpose). The Cadiot statements in §0 are
in arXiv:2505.03091, which is **not** currently in `Papers/MANIFEST.md`; the novelty log
carries the link.
