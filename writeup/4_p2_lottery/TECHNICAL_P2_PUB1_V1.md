# A combined methodological note: four negative results from a computer-assisted-proof attempt that failed

**Route PUB1, leg 179, v1. DRAFT — for the user's review. This leg's landing does not approve it.**

**Status.** This is the publication-scoping draft that leg 58's gate escalated to the user and
that the strategic review recommended be bundled rather than shipped standalone. It is
assembled entirely from banked results; **nothing in it is new to the world**, and its only
contribution is arrangement. Every number is quoted from the JSON or journal of the leg that
produced it — the provenance audit is [`writeup/novelty/leg_179.md`](../novelty/leg_179.md),
which lists each number against the file it was read from.

**What this note is not.** It is not a certificate, not a theorem about the Navier–Stokes
equations, and not a claim that any link of this project's `L1 → L4` chain has moved. None
has, in 178 legs. The object throughout is the `a = 0` Constantin–Lax–Majda (CLM) steady
linearisation — an already-solved, already-published model — and every magnitude below bounds
the difficulty of the real target **from below, not above**.

---

## 0. The shape of the argument, and why four results rather than one

A radii-polynomial / Newton–Kantorovich certificate needs four constants — `Y₀`, `Z₀`, `Z₁`,
`Z₂` — and closure needs `Z₁ < 1`. Seven successive legs of this project tried to produce such
a certificate for a 1D fluid transport model in a weighted `ℓ¹` Fourier space, and did not. The
useful residue is not the failure; it is that the failure has **four separable causes**, each
of which was isolated, measured, and in two cases proved. Three of them are statements about
*method*, not about this particular operator, and that is why they are worth writing down:

| § | result | kind | where it bites |
|---|---|---|---|
| 1 | the exponent-sum conservation law | a measured no-go over a family of spaces | choosing the function space |
| 2 | the discrete-ball trap | a soundness failure mode | computing an induced norm |
| 3 | the `A₂₁` inequality | a **theorem** (two versions; the second supersedes the first) | choosing the approximate inverse |
| 4 | the closure audit | an exhaustion of a named enumeration | deciding when to stop |

They are ordered by where in a certificate construction a practitioner meets them.

---

## 1. The exponent-sum conservation law

**The claim.** In a weighted `ℓ¹` Fourier space, a certificate for this operator needs two
things of the weight, and they are separated by exactly one grading power — and the separation
is **conserved**, so no choice of weights can satisfy both. The weights only decide *which*
requirement pays.

**The measurement.** Write the domain weight exponent `s`, the codomain exponent `t`, and
`g = t − s`. The two exponents are exact complements:

| `g` | −1.75 | −1.0 | −0.5 | 0.0 | 0.5 | 1.0 | 1.5 |
|---|---|---|---|---|---|---|---|
| `‖A_N‖_{Y→X}` exponent in `N` | 2.70 | 1.96 | 1.47 | 0.98 | 0.50 | 0.04 | 0.00 |
| sharp quadratic `S_K` exponent in `K` | 0.00 | 0.00 | 0.00 | 0.00 | 0.50 | 1.00 | 1.50 |
| **sum** | 2.70 | 1.96 | 1.47 | **0.98** | **1.00** | **1.04** | 1.50 |

So `‖A_N‖ ~ N^{1−g}` and `S_K ~ K^{g}`. A certificate needs *both* exponents to be zero;
their sum is `≥ 1` at every `g` and exactly `1` on `0 ≤ g ≤ 1`. The **measured minimum over
the entire family is 0.98**. In `(s,t)` coordinates a bounded inverse needs `t ≥ s+1`, a
bounded quadratic needs `t ≤ s`, and the unit strip between them is empty. Both boundaries are
pinned grid-independently by evaluating the exponents *on* the candidate lines: `t = s−1` gives
**1.96**, `t = s` gives **0.98**, `t = s+1` gives **0.00–0.06**.

**The control, which is what makes it an attribution rather than a suspicion.** Replace the
transport factor `(1 + cos θ) → 1` and change nothing else. The inverse boundary moves from
`t ≥ s+1` to `t ≥ s−1` — **down by exactly two powers**, which is the right number, because a
non-degenerate first-order transport *gains* one power on inversion, this one *loses* one, and
`1 + cos θ` vanishes to order two at `θ = ±π`. The admissible regions then overlap on a full
unit strip, the minimum exponent sum drops **0.98 → 0.00**, and the overlap is non-empty at
**9 of 9** values of `s`.

> The obstruction is the far-field degeneracy of this specific operator — **not** the
> Newton–Kantorovich method and **not** the `ℓ¹` framing. Remove the degeneracy and the same
> machinery has an admissible space pair immediately.

**Why it is true, in one sentence.** A diagonal weight on Fourier coefficients measures
**smoothness**; the far-field transport needs **decay**; and these are not the same thing. The
single mode `cos kθ` equals `(−1)^k` at `θ = π` — it does not decay at `X = ∞` *at all*, for
any `k`, and no diagonal weight can see that. Decay is a statement about the *oscillatory-in-k*
structure of the coefficient sequence, i.e. about finitely many linear moment conditions.
Asking a weighted-`ℓ¹` pair to deliver both is a category error.

**Novelty status, and the citation this note owes.** Searched at primary source over four
papers at full text plus a 39-item forward-citation sweep, and **not found**. The nearest
published relative is Chen & Hou, *Analytic finite-rank corrections for singularly weighted
estimates* ([arXiv:2607.15256](https://arxiv.org/abs/2607.15256)) §1.2, eqs (1.17)–(1.18),
which publishes a weight tension of exactly this **genre**: one exponent squeezed from both
sides, finite energy forcing `β < 1` while the nonlocal term's constant diverges like
`(1−β)^{−1/2}`. Three things differ, and any write-up must say so rather than pretend nothing
like it is in print: it is in weighted `L²`/`L^∞` energy spaces, not a weighted `ℓ¹` sequence
space; the competing requirements are *damping vs. finite energy*, not *smoothness vs.
far-field decay*; and it is **resolved by a choice** (take `α` large) rather than stated as a
no-go over a class of weights. The untested direction, stated as an explanation and not as a
search result: the validated-numerics corpus that uses `ℓ¹`-Wiener norms with *geometric*
weights `ν > 1` avoids the algebraic-decay regime by construction, which is why nobody has had
to state this.

---

## 2. The discrete-ball trap

**The claim.** Computing an induced operator norm by duality over the **discrete** unit ball is
unsound. A discrete Hölder seminorm only inspects grid nodes, so the extremizer that duality
selects is a grid-scale sign pattern whose *interpolant* has an enormous continuum norm. The
resulting number is a true statement about a discrete object and a useless one about the
continuum operator the certificate actually needs.

**The magnitude, with a control that stays flat.**

| `J` (nodes) | dual extremizer, inflation | smooth control, inflation |
|---|---|---|
| 125 | **2 994.16** | 1.0275 |
| 250 | **12 233.31** | 1.0273 |
| 500 | **49 698.93** | 1.0272 |

Inflation grows like **`J^{2.03}`** (fitted 2.0265) — it is not a constant-factor nuisance, it
diverges with refinement, so the trap gets *worse* the harder you work. The smooth control,
computed through the same code path, is flat at ~1.027: the failure is a property of the
extremizer, not of the norm evaluation.

**What survives, and this is the constructive half.** A two-point dual bound uses only
inequalities the **continuum** norm implies, so it is valid. On the domain sup part it
**saturates** in `J` (growth exponent `+0.006`) — a genuinely uniform upper bound. On the
domain seminorm part it is valid but lossy, growing like `J^{+0.496}`; it is reported with its
growth so the slack is visible rather than hidden.

**The practitioner's rule.** Never let a rigorous step depend on node values alone. A
coefficient representation determines a function on the whole domain; a grid does not.

**Novelty status, and the background this note owes.** Searched at primary source and not
found. But the ambient mathematics is named and must be cited: the sampling-discretization
literature (Kosov–Temlyakov and co-authors,
[arXiv:1812.08100](https://arxiv.org/abs/1812.08100),
[arXiv:2203.07126](https://arxiv.org/abs/2203.07126)) asks exactly when a norm evaluated at
finitely many nodes is comparable to the continuum norm, and its headline is that this
**degrades as the smoothness of the class drops**. That is *why* the trap is true. None of
those papers is about a dual/extremizer computation inside a certificate, none is about a
Hölder seminorm on a graded grid, and none reports an inflation factor — so this is a concrete
instance of a known phenomenon, and should be written as one, not as the discovery of one.
Chen–Hou §1.4 states the same *hygiene* as working practice ("the numerical step only
determines coefficients … the corrections are performed analytically on the resulting globally
defined functions"), which again is the moral, not the claim.

---

## 3. The `A₂₁` inequality — and the supersession, stated first

> **READ THIS BEFORE QUOTING ANYTHING IN THIS SECTION.** This project banked **two** versions
> of this result. The first (leg 58) proves the inequality on the restricted class `A₂₁ = 0`.
> The second (leg 127) proves it for **every bounded `A`, with `A₂₁` completely free**, by a
> different argument. **The second supersedes the first.** Leg 58's narrower statement is
> preserved below for the record and because its hypothesis-necessity control is still the
> sharpest one available — but **the citable result is leg 127's**, and any external
> presentation that cites the `A₂₁ = 0` version is citing a weaker theorem than this project
> actually holds.

### 3.1 The current, correct form

**Setting.** `L` is the `a = 0` CLM steady linearisation in the compactified odd-sine
coefficient basis, bordered with the far-field amplitude as an extra unknown and its matching
condition as an extra equation, in weighted `ℓ¹` with `w_k = (1+k)^s`.

**Hypotheses.** `s < 1`; `μ = 0` (no dissipation, so the tail block's diagonal is exactly zero
and its far-field kernel lies in the space); and `A` a **bounded** operator on the space in the
sense that it is the truncation of one fixed bounded operator, so `‖A‖_w` is uniform in the
truncation `M`. **`A₂₁`, `A₁₁`, `A₁₂`, `A₂₂` are all arbitrary.**

**Conclusion.** `Z₁ = ‖I − AL‖_w ≥ 1`. Quantitatively, at truncation `M`,
`Z₁ ≥ 1 − ‖A‖_w · σ_min(L_M)` with `σ_min(L_M) = c_s M^{−(1−s)} → 0`.

**The two ingredients, and only one is this project's.**

1. *Folklore, explicitly not claimed.* `‖x‖ ≤ ‖(I−AL)x‖ + ‖A‖‖Lx‖` for every `x`, hence
   `Z₁ ≥ 1 − ‖A‖σ_min(L)`. This is the contrapositive-with-remainder of the
   `Z₁ < 1 ⟹ invertible` hypothesis every radii-polynomial paper states.
2. *This project's content.* That `σ_min(L) = 0` on this operator in this space at `s < 1`,
   witnessed by an **explicit** sequence rather than found numerically.

**The measurements.**

| quantity | measured |
|---|---|
| fitted `p` in `σ_min ∼ M^{−p}` at `s = 0 / 0.3 / 0.7` | **0.9925 / 0.6985 / 0.3202** (predicted `1 − s`) |
| max deviation from `1 − s` over `s < 1`, all `K` | **0.0219** |
| relative spread of `σ_min` over `K = 2, 4, 8` for `s < 1` | **0.29%** (vs **2.14** at `s = 1.5`) |
| explicit witness vs numerical optimum | ratio **1.0000000000045×**, cosine **0.9999999999999998** |
| rows of the finite block carrying the residual of `Lv` | **1** (the truncation edge), with `z_K = 0.0` exactly |
| the bound is attained: max slack at `A = L⁻¹` | **1.2366e−08** |
| holds across leg 54's shape battery | **196 / 196**, min slack **7.7343e−10** |
| `μ > 0` control (the instrument can say otherwise) | exponent `≤ 2.62e−03`, i.e. `σ_min` **saturates**, vs 0.6985 at `μ = 0` |

**A mechanism worth recording, because the obvious repair is measured not to work.** Bordering
the operator with the far-field amplitude — the entire point of the assembled object — changes
`σ_min` by **5.7e−15 relative** at `μ = 0`. The reason is *not* that the singular sequence has
no far-field-amplitude component: that component is **6.5–6.8% of `‖v‖₁` and growing with `M`**.
The reason is that its coupling column is supported on a **single row**, the truncation edge, so
the border has nowhere else to reach. (The same two code arms differ by **6.1e−02** at
`μ = 0.1`, so the comparison is live in both directions.)

**The scope line, and it is the whole discipline of this section.** Xu
([arXiv:2607.19762](https://arxiv.org/abs/2607.19762)) proves that the **same** operator, on
origin-`H²`, has point spectrum exactly `{0,1}` and essential spectrum meeting `{Re λ ≥ −1/2}`
in the single line `{Re λ = −1/2}` — hence is invertible after modulation, with spectral gap
`1/2`. **So this is a statement about the `ℓ¹_w` realization, never about the operator.** No
sentence anywhere in this project says the operator "has no bounded approximate inverse," and
none may.

### 3.2 The superseded form, kept for the record

**Proposition NG (leg 58).** On the class `A_upper = {[[A₁₁, A₁₂], [0, A₂₂]]}` — i.e. `A₂₁ = 0`,
strictly larger than block-diagonal and containing the separately-measured `gs_upper` shape —
`Z₁ ≥ 1 + ‖A₁₁ B h‖_w/‖h‖_w ≥ 1`, at every split `K` and every `s < 1`.

The proof is three lines: test `I − AL` on `x = (0; h)` where `h` is the tail block's kernel.
`Th = 0` kills the `A₁₂` and `A₂₂` terms, `A₂₁ = 0` kills the third, the column is
`(−A₁₁Bh; h)`, and dividing by `‖h‖_w` gives the bound. `A₁₂` and `A₂₂` never appear — which is
exactly why the class is larger than block-diagonal, and exactly why the argument **stops** at
`A₂₁ ≠ 0`.

**Leg 58's own scope line, verbatim, and it is the sentence leg 127 retired:** *"MEASURED, NOT
PROVED: every `A` with `A₂₁ ≠ 0`."*

**What survives supersession, and is still the sharpest thing in the section.** Leg 58's
hypothesis-necessity control. Hypothesis **(H2)** is that the tail block has a kernel **in the
space**: `Th = 0` with `0 < ‖h‖_w < ∞`. The kernel is explicit from a two-term recursion; its
measured decay exponent is **−2.0024** (cokernel **+1.0012**), so it lies in `ℓ¹_w` exactly when
`s < 1` — the crossing is measured at **1.0**, reached from the opposite side to the Fredholm
argument that first found it. And the control varies `μ`, which changes the tail operator
itself: at `μ = 0` the proposition forbids `Z₁ < 1` and the measurement agrees at every `K` and
in both weight classes; at `μ = 0.1` the kernel is gone; by `μ = 2.0` the **same two in-class
shapes** reach `Z₁ = 0.174027`. **The hypothesis is necessary, not decorative** — and, as §5.2
shows, (H2) is also precisely where a later result found a corner the theorem does not reach.

---

## 4. The closure audit — when to stop, and how much of the difficulty was tuning

**The question.** The project's remaining stage proposed to *search* for a certificate over the
function space, the operator split, and the constants. All three degrees of freedom were
separately measured dead. Rather than run the search, the audit asks: enumerate that declared
space, and does any admissible configuration remain that no banked measurement or theorem
covers?

**The answer: none.** **1,686 configurations enumerated, 1,686 covered, 0 uncovered** —
by strongest coverage, **144 THEOREM / 1,032 STRUCTURAL / 510 MEASURED**.

**The accounting that the audit actually owes, and it is the interesting number.** On decades
of `log₁₀ Z₁` from the block-diagonal baseline `Z₁ = 10.458427`:

| | decades | share of the requirement |
|---|---|---|
| required (to reach `Z₁ < 1`) | **1.019466** | 100% |
| delivered by tuning | **0.067202** | **6.5919%** |
| left unrealized (tuning headroom never searched) | **0.171055** | **16.7789%** |
| owned by structure | **0.781209** | **76.6292%** |

The three shares sum to **1.0000000000000002**, and the runner asserts it.

**There was unexplored search space, and it would not have mattered.** Tuning reached only
**28.21%** of its own ceiling — so the stage was not proposing to search an empty box. But a
*perfect* search lands at `Z₁ ≥ 6.0424`, still **6.04×** short of closure.

**And on the proved class the accounting collapses.** On `A₂₁ = 0` the floor *is* the
requirement: `Z₁ ≥ 1` against a need for `Z₁ < 1`. Searchable headroom is exactly **zero
decades** and structure owns **100%** — as a theorem rather than as a battery. That is the
sense in which "structure, not tuning" is theorem-grade here rather than merely measured.

**Instrument checks, because an audit of banked numbers is only as good as its ability to
reproduce them.** Leg 54's two headline numbers, recomputed read-only through that leg's own
landed code: `block_diag` **10.458427031841403** and `ff_lift` **8.959091169104095**, relative
gap **0.00e+00** — bit-identical. The positive control reproduces leg 58's entire twelve-entry
dial elementwise to **1.2482e−15**.

**Two things the audit's own controls caught, both of which are this project's standing
lessons repeating.** (1) The covering predicate was initially a **tautology**: run it on the
dissipative `μ > 0` operator, where a certificate demonstrably closes, and it answered
"covered" — because not one of the twelve clauses referenced `μ`. Scoping every clause to
`μ = 0` is what made the audit falsifiable. (2) The control's own realization was wrong first
— it bordered the dissipative object with a far-field direction it does not have — giving a
number off by **33,926×**.

**The limit on what this may be written as, and it is a hard limit.** Automated certificate
synthesis is published as **sound but not complete** ([arXiv:2309.06090](https://arxiv.org/abs/2309.06090)):
a search that fails to find a certificate licenses **no conclusion** about the model. So the
audit's claim is exhaustion of a **named enumeration** — this project's own declared search
space — and **never** "no certificate exists." One flag from an earlier leg (a search-index
concern) **stands**, untested by this work.

---

## 5. Two findings folded in as they landed, without softening or strengthening

### 5.1 Does the published record already account for the scaling exponent, and for `a_c`?

The two literature-anchored numbers this project carries had never been checked against the
paper they came from. Reading Lushnikov–Silantyev–Siegel
([arXiv:2010.01201](https://arxiv.org/abs/2010.01201)) at full text settles both, and **moves
them in opposite directions**.

**(a) `alpha(1/2) = 3`: YES, explicitly and exactly.** LSS Eq. (39), p. 11, *is*
`ξ = (x − x₀)/(t_c − t)^{1/3}`, so their exponent is `1/3` and this project's `alpha(1/2) = 3`
follows from its own dictionary. It is on the page three further ways: the far-field exponent
`1/α = 3` of Eq. (38), the closed form `α₀(1/2) = 1/3` of Eq. (45), and Table 1 p. 48 listing
`α_e = 0.333333333` at `a = 0.5`. It is an exact closed-form solution LSS write down and prove.

Re-derived independently here: the PDE residual of their Theorem 2 is **7.92e−16** at
`a = 1/2`, against a best of **6.05e−02** at `a = 0.45 / 0.55 / 0` — **13.9 decades** apart. As
the root of a scalar equation, `p` bisects to **0.333333333333333** and the exponent to
**3.000000000000000**; the same code path returns `1`, `3`, `6`, `10` at other parameter values,
so the `3` is a measurement of the object and not of the code.

**The correction this produces, and it is a correction to a source count, not to a number.**
The three citations this project had been treating as independent confirmations are **one
ancestor, not three**: three of the four authors of the secondary source are the three authors
of LSS, LSS came first, and the third source's own text says its branch was checked against
LSS's. Nothing claimed was wrong; the *count of independent sources* was inflated. The
genuinely independent second discoverer is a different paper, J. Chen
([arXiv:1908.09385](https://arxiv.org/abs/1908.09385)), whom LSS themselves credit on p. 11.

**(b) `a_c ≈ 0.6890665`: YES as primary source, NO from the exact solution.** The value
`0.6890665337007457…` is LSS's own (abstract; §1 Eq. (8); §12), and this project's constant is
that number truncated (relative offset **4.89e−08**). But it is **not** implied by the exact
`a = 1/2` solution: LSS define it by `α(a_c) = 0` and locate it **numerically**, while the
exact family's closed form `α₀(a) = 2(1−a)²/(2−a)` is strictly positive for every `a < 1` and
has **no root at all** (scanned over `a ∈ [−1, 0.999]`; the scan's minimum is `2e−06` at the
`a → 1` end, so a root would have been seen). The useful new fact is about *what kind of number
it is*: converged numerics from an iterative solve that does not converge past `a_c` at all,
with the paper's own stated accuracy in that range being **"at least 5 digits"** — not
seventeen certified digits, whatever the printed tail looks like. Anyone quoting it should
quote it as that.

### 5.2 A corner the closure audit does not cover — parked, and genuinely ambiguous

This is stated exactly as it landed. **It is an open escalation, not a settled result: the
branch that produced it was pushed and deliberately NOT merged, pending a human ruling.**

**What it is.** On a *compact support interval* — available because the profile at `0 < a < 1`
has compact support — a **global Chebyshev basis** is a fourth value of the audit's
realization axis, which has three values on disk. The shape vocabulary this project uses
enumerates no basis and no domain at all, so it can neither cover nor fail to cover it.

**And the corner is two corners, which is the structural finding.** One operator, two pairings
that both close under it, **opposite** classifications:

| | domain → codomain | unbounded part | classified as |
|---|---|---|---|
| **A** — this project's own ansatz | `(1−v²)T_n → T_m` | bidiagonal, **exactly zero diagonal**, off-diagonal `~n/2` | SHIFT |
| **B** — the Olver–Townsend airfoil pairing ([arXiv:1507.00596](https://arxiv.org/abs/1507.00596)) | `√(1−v²)U_{n−1} → T_m/√(1−v²)` | **exact `diag(−n)`** | MULTIPLIER |

**The numbers, with their realization and gauge named.** Realization B, `A₂₁ = 0`, bordered,
`N = 192`, `K = 16`, amplitude gauge: `block_diag` **0.2737** and `gs_upper` **0.0874** at
`a = 0.8`; **0.7370** and **0.2287** at `a = 0.5`, which is where the nonlinear constant `Z₂`
was previously measured finite. `Z₁` moves **0.19%** over an 8× refinement; the target is in
its own space (margin **−0.73**); the operator is gated against direct pointwise evaluation at
**3.4e−04**; and the same code path returns `148.7` at the worst corner, so a value below 1 is
a discrimination and not an instrument floor.

**The caveat that must travel with every one of those numbers.** `Z₁ < 1` holds at **2 of 4**
border gauges — the other two give **93.3** and **6.7e9**. Over the whole parameter grid,
**27 of 120** `A₂₁ = 0` configurations fall below 1, **all** in realization B and **none** in
realization A. A certificate designer does get to pick a gauge, so this is a **restriction, not
a refutation** — but the headline is never stated as a bare `Z₁`.

**Why this does not contradict §3.** Every sub-1 number above has `A₂₁ = 0`, so it looks like a
counterexample to Proposition NG. It is not. That proposition's hypothesis **(H2)** requires the
tail block to have a kernel in the space, and realization B's tail is `diag(−n)`, which has **no
kernel at any `n ≥ 1`**. (H2) fails outright — the same way it fails for `μ > 0` in leg 58's own
dissipative control. **The theorem is untouched; it simply does not reach this realization.**
That is exactly the sense in which the corner is new.

**And the ambiguity, which this note states and does not resolve.** The closure audit of §4 was
performed on the `a = 0` CLM linearisation, and **this corner does not exist on that object at
all**: its measured decay exponent is `−1.0000`, the mass outside any radius never reaches
zero, and `a = 0` sits outside the range `0 < a < 1` on which the compact-support theorem holds.
So *"the audit's completeness claim is reversed"* and *"the audit's completeness claim was
always scoped to an object where this corner is empty"* are **both defensible readings of the
same measurements**. Choosing between them is a human decision, and it has not been made.
Anything published from §4 must carry §5.2 with it.

**Its own ceiling.** `Z₁` is one of four constants and this is **not a certificate**: `Y₀`,
`Z₀`, `Z₂` were not measured here, and `Z₂` was previously measured *infinite* on this same
object in a different realization, with finiteness of the nonlinearity requiring `a ≤ 1/2` —
which is why the `a ≤ 0.5` values above are the ones that matter. Float64 throughout; no
interval arithmetic. And the object is the gCLM profile on `0 < a < 1`, **not** this project's
nominal target.

---

## 6. Currency addenda — four things that landed after the bundle was specified

The bundle was specified before these landed. They are included because a scoping note that is
out of date on its own record is the failure mode this note exists to prevent. Each is stated
as its own leg banked it.

**6.1 One of the three "dead realizations" must be de-rated twice over.** An earlier leg
recorded, for this note's attention, that of three dead realizations two (§1 and §2) are
confirmed novel while the third — a weighted-energy formulation whose admissible window was
measured to have **width zero** — is **pre-empted in the published literature** and must be
de-rated to a statement about a trial-space choice. A later leg then sharpened that from
"pre-empted" to **"realization-dependent, and here is the other realization"**: the zero-width
window is a property of the trial space (vanishing order `p = 1`), not of the operator. Hold
the weight parameter at its published value and move `p → 2` — the same degree of freedom,
already measured elsewhere in this project's own record — and the admissible window goes from
width **0.0** to **2.0**, while the membership norm ratio per refinement goes from
**1.6777e+07** (divergent) to **1.0000000000000002** (convergent). **So the weighted-energy
result is not publishable as a negative at all**, and this note does not include it as one.

Two things follow for the other results. First, the organising concept — that an obstruction
can belong to the *realization* rather than the operator — is **published and named on this
exact operator** (Xu, Prop. 2 §3.1) and is used here, not claimed. Second, when that same
classification is applied to the other banked negatives, the two that underpin §3 come back
**realization-invariant across every choice their own axes contain**, and are besides subsumed
by §3's own argument rather than being independent companions to it.

**6.2 The "validated numerics cannot reach 3D" barrier is the field's, and its usual wording is
wrong.** Across a survey spanning fluid mechanics, parabolic blow-up, dispersive PDE,
chemotaxis, pattern formation and the dynamical-systems computer-assisted-proof lineage, the
largest number of spatial variables in any machine-certified **singularity** object is **2**.
Zero records satisfy all four clauses of the test. But **one** record certifies a genuinely 3D
PDE object — van den Berg & Williams' Ohta–Kawasaki stationary states (SIAM J. Math. Anal.
51(1):131–158, 2019, giving the first existence proofs for the double gyroid and BCC-packed
sphere solutions). **The barrier is time-dependent singularity formation, not dimension**, and
the note states it that way. Every 3D singularity theorem carrying a computer-assisted
ingredient obtains its 3D-ness from a symmetry reduction or from an ODE profile plus analysis.
This matters for scoping because it means the 1D/2D restriction in §§1–4 **is the field's
scope**, not a self-imposed limitation of this project.

**6.3 The nearest competing modern technique's obstruction is technique-specific, not
model-specific.** A recent paper producing computer-assisted-proof-ready *unstable* self-similar
singularities attributes its own precision floor to its **training method**, in its own words
(*"we are unable to reach maximum equation residuals much below 10⁻⁸"*), and applied its
precision-improving technique to only **4 of 12** solutions. The solutions left at the floor
are the ones the technique was never applied to. So it exhibits an **unapplied technique**, not
a **model wall** — which means §§1–4 should not be read as evidence that a different model
class would have worked.

**6.4 A Hilbert-space realization is scoped but not built, and the honest form of that matters
here.** A separate line found that origin-`H²` admits a structurally viable certificate
*formulation* — a split, a shape, and no obstruction of §3's class — and it too was escalated
and parked without building anything. What must not be written, and is not written here, is
"the operator is invertible there, therefore a certificate is possible." Xu bounds his own
result in his own abstract: the closed-form decay is obtained *"on a weighted space of the
conjugated variable reached from `X` by a bounded transfer map; we keep the two separate, since
`L₀` is non-normal and a spectral gap does not by itself give a decay rate in the `X` norm."*
A construction leg on that realization was in flight and **had not landed** when this note was
drafted; nothing in this note is attributed to it.

---

## 7. Housekeeping: one stale framing note, corrected

A literature leg's novelty log describes a subsequent leg as *"Route-NGX, live"* and its subject
as *"the open `A₂₁ ≠ 0` question this leg is mining literature for."* That leg has since landed
and **closed** the question — it is §3.1 above. The row is stale as written, and this note
corrects it in place, in one sentence, explicitly as housekeeping. **The literature leg's
finding is untouched**: every preconditioning construction in the papers it read still induces
`A₂₁ = 0`, the one theorem that drops the nonzero-diagonal hypothesis still fails a *different*
hypothesis (compact resolvent) on this operator, and a diagonal change of basis still cannot
move a diagonal. Only the tense of the pointer changed.

---

## 8. What is claimable, and what is not

For anyone scoping this for external publication, the four results sit at three different
grades and must not be levelled:

| result | grade | what may be claimed |
|---|---|---|
| §3 the `A₂₁` inequality | **theorem** | `Z₁ ≥ 1` for every bounded `A`, on the `ℓ¹_w` realization at `s < 1`, on this operator. **Not** about the operator; **not** about the method in general. The inequality it rests on is folklore and is not claimed. |
| §1 exponent-sum conservation | **measured no-go over a family** | a conserved separation, minimum **0.98**, with an ablation that attributes it to the operator's far-field degeneracy. Cite Chen–Hou §1.2 as the nearest published cousin and say what differs. |
| §2 discrete-ball trap | **soundness failure mode** | a concrete, quantified instance (`~J^{2.03}`) of a phenomenon whose ambient theory is published. Cite the sampling-discretization literature as background. |
| §4 closure audit | **exhaustion of a named enumeration** | 1,686/1,686 covered, and the tuning/structure split. **Never** "no certificate exists" — synthesis is sound but not complete. And §5.2 must travel with it. |

**Three things this note must never be read as saying.** (1) That the operator has no bounded
approximate inverse — it is invertible on origin-`H²`, published. (2) That the
Newton–Kantorovich or radii-polynomial method is obstructed in general — §1's own ablation
removes the obstruction by changing the *operator*. (3) That any of this bears on the target
problem. The object is the `a = 0` CLM linearisation, whose `Y₀` is exactly zero for a
degenerate reason (the anchor *is* one basis mode), so every magnitude here bounds the real
target's difficulty **from below**.

---

## 9. Ceiling

The object throughout is the `a = 0` CLM steady linearisation, except in §5.2 where it is the
gCLM profile on `0 < a < 1`. No dynamics were run. Nothing is claimed about this project's
nominal target profile. Every number is float64 at a stated truncation; **nothing here is
interval-enclosed or rigorous** in the computer-assisted-proof sense, including the two results
called theorems, whose *proofs* are exact but whose *verifying measurements* are floating-point.
**No link of the `L1 → L4` chain moved.** None has moved in 178 legs. Clay odds remain ~0.05%.

**This draft is for the user's review. Its landing records that the bundle reproduces from its
sources; it does not approve the bundle for publication.**
