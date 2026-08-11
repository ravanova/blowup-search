# TECHNICAL — Route-FUS v1 (leg 314): the finite-unstable-spectrum condition, classified

**Scoping leg. Builds nothing. `solver/` is read, never written, never run.**
Runner `experiments/p2_route_fus_v1_scoping.py`; curated data
`writeup/data/p2_route_fus_v1.json`; evidence + figure
`experiments/p2_route_fus_v1_scoping_evidence.py` → `writeup/figures/fig77_route_fus_v1.png`;
novelty pass `writeup/novelty/leg_314.md` (committed first, `8c1f35f`).
**Every number quoted below is in the JSON.**

---

## 1. The gate, in its pre-committed wording

> *"Does the scoping produce a definite classification — finiteness for these profiles is
> (i) provable, with the argument sketched and its load-bearing step named; (ii) checkable
> only numerically, with a named certified-count/lower-bound route this repository's spectral
> tools bear on; or (iii) open, with the obstruction named?"*

**Answer: `yes` — a definite classification was produced. The classification is (iii) OPEN.**

The gate text is immutable and was not edited. The classification is **computed by the runner
from five pre-committed discriminators**, not asserted; the classifier's self-tests show it
reaches all four of its outcomes (`DISCHARGED`, `i_PROVABLE`, `ii_NUMERICAL`, `iii_OPEN`),
so this is a verdict that could have come out differently (lesson 90).

---

## 2. The object

`arXiv:2509.14185` p.19:

> *"For a computer-assisted proof to be feasible, it is **desirable** that the spectrum in the
> right-half µ-plane consists of a **finite number** of eigenvalues."*

Leg 175 banked that this is *"called 'desirable' and assumed, which no residual reduction
discharges"*, and that neither `2509.14185` nor `2511.22819`'s precision fix touches it. This
pass **re-verified the second half on the instrument**: `2511.22819`'s abstract never mentions
unstable spectrum, eigenvalues or spectral finiteness — instability appears only *ordinally*
(*"1st unstable"*, *"4th unstable solution for IPM"*). Leg 175's reading stands.

Two further restrictions accompany the paper's own mode count, and both matter here: it is a
PINN eigensolve *"under the assumption that there exist eigenvalues with non-negative real part
that lie on the real axis"*, and *"restricted to Ψ that lie within the same symmetry class"*.

---

## 3. The finding: the condition is not realization-invariant

**The load-bearing observation is that the FUS condition, as stated, is not a property of the
profile. It is a property of the (profile, realization) pair — and `2509.14185` names no
realization.**

This is not this leg's inference. It is **Xu, `arXiv:2607.19762`** (22 Jul 2026, 41 pp), a paper
this repository already holds and has audited (legs 70 / 171 / 173 / 249). For the `a = 0` CLM
profile `Ω(y) = −y/(y²+¼)`:

* a **realization dichotomy** — the *"in-strip smear"* seen in generic discretizations is the
  spectrum of the **maximal `L²` realization**, which the **origin-`H²`** choice **eliminates**;
* in origin-`H²`, the essential spectrum in `{Re λ ≥ −½}` is the **single vertical line
  `{Re λ = −½}`**, produced by a **log-widening Weyl sequence**, with a **Hardy–Mellin resolvent
  bound** clearing the rest of the half-plane;
* the **point spectrum over all of `ℂ` is exactly `{0, 1}`** — scaling and time-shift symmetry
  modes — **with no embedded eigenvalues**; quotienting gives a spectral gap of `½`.

**Same PDE, same profile, two spectral pictures.** In one realization the unstable set is finite
(and purely symmetry-induced); in the other it is smeared. So *"the spectrum in the right-half
µ-plane consists of a finite number of eigenvalues"* has **no truth value until the space is
fixed** — in particular the condition imposed at the profile's singular point. This is lesson 91
(*name the realization*) applied to somebody else's assumption.

---

## 4. The smear, made quantitative on banked numbers

`solver/rescaled_spectrum.py`'s discretization is the **maximal-`L²`** side of Xu's dichotomy —
leg 70's Route-RC established that **from the code**, finding it imposes **no origin condition at
`X = 0`**. Route-I's banked ladder (`writeup/data/p2_route_i_v1_driven.json`, `i5_stability`)
therefore measures the smear directly.

**Realization, named in full (lesson 91):** `solver/rescaled_spectrum.py`'s compactified
odd-sine basis (`OddCompactBasis`), gCLM at `a = ½`, `p = 3`, `µ = 0` (inviscid), dilation mode
excised by identity, unstable tolerance `Re > 1e-6`.

| `K` | `n_unstable` | `max Re µ` | `max |Im µ|` | profile residual | `λ_truncation` |
|---|---|---|---|---|---|
| 48 | 45 | 4.523568 | 202.39 | 4.2737e-03 | 7.6532e-01 |
| 96 | 93 | 4.545506 | 430.35 | 3.3187e-08 | 3.6960e-02 |
| 144 | 141 | 4.557538 | 661.22 | 2.8691e-13 | 1.1134e-06 |

* **`n_unstable = K − 3` exactly.** Least-squares slope `dn/dK = 1.000000`, **max |residual| = 0**.
  Verdict `DIVERGENT` on the pre-committed criterion (strictly increasing **and** slope ≥ 0.5).
* **`max Re` is flat to `0.751%`** across the ladder while **`max |Im|` grows ×3.267** as `K`
  grows ×3.000. The unstable set is not a fixed finite collection being resolved better; it is a
  **curve on which `Re` rises with `|Im|`**, whose visible extent is set by the truncation.
  `solver/marginal_flow.py`'s own `frequency_profile` docstring states this independently.

### 4a. The tidy closed form is diagnosed, not banked

`n = K − 3` is exactly the kind of suspiciously tidy closed form the standing discipline says to
check rather than quote. The bookkeeping: the Jacobian is `K × K` (`OddCompactBasis` carries
`b_k`, `k = 1..K`), `unstable_count` excises **one** eigenvalue by identity (the dilation mode,
`L(X Ω_X) = 0` exactly; its measured real part falls `0.2710 → 8.899e-05 → 4.156e-08` along the
ladder), leaving `K − 1` judged. So

> **offset 3 = 1 excised dilation + 2 eigenvalues with `Re ≤ 1e-6`.**

`min Re` converges to `−2` (`−2.0814`, `−2.0073`, `−2.0017`). That the two non-positive
eigenvalues are isolated symmetry/edge modes is *consistent* with Route-E's banked finding that
the only grid-converged isolated eigenvalues of this flow are its two exact symmetry modes — but
**this leg did not measure them and does not assert it** (doing so needs a fresh gCLM
eigendecomposition, which is **banned**). **The load-bearing quantity is the slope, not the
offset:** the unstable count is *proportional to the number of degrees of freedom*.

### 4b. It is not an under-resolution artifact — the check runs the other way

The obvious objection is that a badly resolved profile manufactures spurious unstable
directions. If so, the count would **fall** as resolution improves. It **rises**: across the
ladder the profile residual improves by **10.17 decades** and `λ_truncation` by **5.84 decades**
while `n_unstable` goes `45 → 93 → 141`. **Better resolution buys more unstable directions.**
That is the continuum signature and the opposite of the artifact signature.

### 4c. The positive control (lesson 90)

A control that cannot come out differently is not a control. Ask what would have to change for
the counting code to report *finite*: **only `µ`**. On the identical ladder, the identical basis
and the identical profile family, the **viscous** rows report `n_unstable = 0` at **every** `K`
(verdict `K_STABLE`, `all_zero = True`). The `DIVERGENT` verdict is therefore a statement about
the inviscid operator, not about the instrument.

**Figure `fig77`** shows all three panels: (a) the divergent inviscid count against the flat
viscous control, (b) `Re` flat while `|Im|` grows, (c) resolution improving while the count rises.

---

## 5. Why this is (iii) OPEN and not (ii)

The tempting classification is (ii) — *checkable only numerically*. It is wrong, and the reason
is the whole content of this leg.

**Every certified numerical route counts inside a bounded box.** The finiteness claim is a
statement about **`|Im µ| → ∞`**: a discrete eigenvalue set in a half-plane may still accumulate
at infinite imaginary part, and forbidding that accumulation requires a **resolvent bound**, not
a count. No finite computation, however rigorously enclosed, sees the region where the condition
actually lives.

**The literature confirms this split, and the sharpest confirmation is a paper that does the
work.** Guo–Hadžić–Jang–Schrecker, `arXiv:2509.12435` (*Nonlinear stability of the Larson–Penston
collapse*, 15 Sep 2025, 149 pp) prove **maximal dissipativity of the linearised operator on
arbitrarily large backward light cones**, and then establish mode stability by

> *"a high-order energy method in low- and high-frequency regimes (relying on monotonicity) and
> **rigorous computer-assisted techniques in the intermediate regime**."*

**The computer does the bounded middle. The unbounded high-frequency end is done analytically.**
This repository already recorded the box at leg 265 / verify_265: `Re λ ∈ [0,1]`, `|Im λ| ≤ 8`,
with `b₀ = 1/5`, `b₁ = 8` (VNODE-LP; code at `github.com/mrischrecker/Larson-Penston-Stability`).

The same structural step, under its other name, is BCG `arXiv:2208.09445` (and non-radially CGSS
`arXiv:2310.05325`): `L = A₀ − δ_g + K` with `A₀` **maximally dissipative** and `K` compact on
`X = H₀^{2m}(B(0,2))`, giving `Λ = σ(L) ∩ {Re λ > −δ_g/2}` **finite**, of finite algebraic
multiplicity — a **theorem**, supported on an unbounded region, and the thing that makes the
unstable spectrum finite. Under its third name it is Xu's **Hardy–Mellin resolvent bound**.
The classical ancestor is Weyl's theorem plus a high-frequency estimate; the old fluid-adjacent
template is the 2007/2010 wave-map mode-stability trio (`math-ph/0702025`, `1006.2172`,
`1003.0707`).

**None of these is available for CCF, IPM, 2D Boussinesq or 3D Euler with boundary**, and no
certified count has been published for any of them.

### 5a. Four independent literatures corroborate the same split

The bounded-box / unbounded-tail split is not an artefact of the blow-up literature. It recurs,
with the same division of labour, in four places found this pass:

* **Barker–Zumbrun, `arXiv:1601.00837`** — the closest thing to a *certified unstable count*
  anywhere. Interval arithmetic plus rigorous ODE bounds plus an **Evans-function winding number**
  on `∂(B(0,R) ∩ {Re λ ≥ 0})`. The decisive detail is the radius: `R = (√γ + ½)²`, enclosing all
  possible unstable eigenvalues, is **derived analytically**. *The computer works inside the disc;
  the disc itself is a theorem.* Exactly this leg's classification, in a worked example.
* **Gallay–Wayne** — in the weighted spaces `L²(m)`, `σ_ess = {Re λ ≤ −(m−1)/2}`. Finiteness of
  the unstable set is **bought by raising the weight `m`**, i.e. by *changing the realization*.
  Independent confirmation of obstruction (1): the answer is a property of the space.
* **Weyl / Kato IV.5.35, and the Jörgens–Vidav–Voigt chain** (with Chicone–Latushkin's
  evolution-semigroup version) — the classical statement that the essential spectrum is invariant
  under relatively compact perturbation. This is the ancestor of "maximal dissipativity + compact
  `K`", and it is where the unbounded region is discharged by estimate.
* **Chen–Hou** — sidesteps the condition rather than discharging it: the computer-assisted 3D
  Euler-with-boundary proof is built on **energy estimates with a finite-codimension stability
  argument**, not on a certified enumeration of the unstable spectrum. That an existing
  computer-assisted blow-up proof *avoids* the FUS condition is evidence about its cost.
* **Bricmont–Kupiainen** — the old renormalisation-group template in which finiteness of the
  unstable directions is *imposed by the choice of space*, again not proved for a given profile.

### 5b. The one absence claim, and its audit (MF3)

The classifier's discriminator `d4` — *no certified unstable-mode count exists for CCF, IPM, 2D
Boussinesq or 3D Euler with boundary* — is this leg's **only** absence-based discriminator, and
absence claims are the ones a broken search instrument can fake. It was audited against the
orchestrator's defect report MF3 (*"the arXiv endpoint returns zero for any two ANDed quoted
phrases"*); the audit is at `writeup/novelty/leg_314.md` §4a. Result, in short:

* **MF3 did not reproduce** on the instrument used here — ANDed quoted pairs returned 6, 1, 2 and
  **251** results. **No zero from an ANDed quoted query is banked anywhere in this leg.**
* The only all-zero return came from a `curl`/`urllib` instrument independently diagnosed as
  broken (301 → 429) and **discarded before** MF3 arrived; none of its output is cited.
* `d4` rests on a **multi-instrument sweep** (WebSearch, WebFetch, direct PDF pulls of
  `2208.09445`, `2310.05325`, `2509.14185`), and its strongest support is **positive, not
  negative**: `2509.14185` p. 19 calls finiteness *"desirable"* — the authors state in their own
  words that they have not established it.

**So the (iii)-OPEN branch does not rest on any query zero.** Obstructions (1) and (2) below are
presence claims resting on quoted text, and would stand even if `d4` were withdrawn entirely.

---

## 6. The classification, stated

**(iii) OPEN.** The named obstruction, in two parts, both load-bearing:

1. **The condition is not realization-invariant, and no realization is named.** Until the space
   is fixed — in particular the condition at the profile's singular point — the FUS hypothesis
   has no truth value to prove, disprove **or check**. Xu's dichotomy shows one profile with two
   answers; §4 shows the smear side is not hypothetical but quantitative, `n = K − 3`.
2. **Once a realization is fixed, the residual obligation is a high-frequency resolvent bound on
   the unbounded region `|Im µ| → ∞`** — Hardy–Mellin, or maximal dissipativity plus relatively
   compact perturbation. **It is a theorem, not a computation**, and no certified count on a
   bounded box can supply it.

**The corollary worth stating on its own: for this condition, numerics is a refuter, not a
verifier.** A truncation ladder can *falsify* finiteness (as it does in §4) and can *count* what
sits inside a box. It can never *establish* finiteness.

---

## 7. What a construction leg would need — **named, not built**

The brief forbids building this, and it is not built. Recorded so the DM can draft or decline it.

**Prerequisite before either half: name the realization.**

| half | what | method | this repository's tools that bear |
|---|---|---|---|
| **A — bounded box** | certified count of eigenvalues in `Re µ ∈ [0,R]`, `|Im µ| ≤ C` | argument principle / winding number of a regularised determinant, in interval arithmetic | `solver/interval.py` (interval arithmetic, Dekker splitting); `solver/spectral_certificate.py` (bordered linearisation, exact rational inverse norms); **`solver/op_lower.py`** (certified **lower** bound — a lower bound on `‖(L−µ)u‖/‖u‖` over a sub-box **excludes** eigenvalues from it) |
| **B — unbounded tail** | exclusion of spectrum in `{Re µ ≥ 0, |Im µ| > C}` | an **analytic** resolvent bound: Hardy–Mellin, or maximal dissipativity + relative compactness | **none. This repository has no tool for it, and neither does any repository.** |

Half A is buildable here. **Half B is the load-bearing half and it is a theorem.** Building half
A alone would produce a certified count that *does not discharge the condition* — which is
precisely the trap this leg exists to mark. External precedent for exactly this shape:
GHJS `arXiv:2509.12435`.

---

## 8. Bans

Walked term by term in `writeup/novelty/leg_314.md` §3. The one that made contact is
**"another gCLM measurement leg"**, and it **bound and redesigned this leg**: following leg 70's
Route-RC precedent, the runner performs **arithmetic on counts already banked** and carries an
**AST self-guard** asserting zero banned calls (`newton`, `continuation`, `spectrum`,
`converged_spectrum`, `unstable_count`, `eigvals`, …) and **zero `solver`/`numpy`/`scipy`
imports** — both verified in the JSON and re-checked by the evidence script. One
`frequency_profile` call was made as a **runtime cost probe before the ban walk completed**; it
reproduced Route-I's banked `max_re` to `~3e-14` and **no quantity from it is banked, quoted, or
in the JSON**. It is reported rather than quietly dropped. **The ban is not lifted, and this leg
does not lift it.**

The near-miss on *"closure is a property of the SPACE"* is recorded explicitly in the novelty
file: the banned move was *explaining a certificate failure* by appeal to the space, refuted
because leg 49's gauge ablation put the 5604× in the border rows. Here the realization-dependence
is a **cited published theorem** (Xu, Prop. 2), audited from this repo's own code by leg 70 — not
an explanatory habit.

---

## 9. Ceiling

**Wall 1 and Wall 2 stand. No link of the L1→L4 chain moved. Clay odds remain ~0.05%,
unchanged.**

**Classifying a condition is not discharging it.** If anything this leg makes the FUS hypothesis
*harder to state* — it shows the hypothesis is under-specified as written — not easier to prove.

**Scope, stated as narrowly as it holds.** The divergent count is measured in **one realization
of one model** (gCLM, `a = ½`, `p = 3`, maximal-`L²` compactified odd-sine basis) and is **not a
claim about CCF, IPM, Boussinesq or 3D Euler with boundary**. It demonstrates that the missing
step **can** fail — not that it **does** fail for those four. What holds for those four is the
statement of §6: **open, obstruction named.**
