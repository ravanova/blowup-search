# TECHNICAL — Route-DECR v1 (leg 318): "DOMINATED → ENCLOSED", and the criterion that decides it

**Runner** `experiments/p2_route_decr_v1_scoping.py` (3.9 s) ·
**data** `writeup/data/p2_route_decr_v1.json` ·
**§0a pass** `writeup/novelty/leg_318.md` + `writeup/data/p2_route_decr_v1_lit.json` ·
**figure** `writeup/figures/fig84_route_decr_v1_knife_edge.png` ·
**blog sibling** `BLOG_P2_ROUTEDECR_V1.md` · **journal** `experiments/journal/leg_318.md`.

**Scoping leg. Nothing built.** No solver module written or edited; `solver/viscous_novelty.py`
is leg 197's and was **imported read-only**. `requirements.txt` untouched. `plan_of_record.py`
untouched and byte-identical to `origin/main`. No ban lifted, re-posed or weakened.

---

## 0. The gate, in its pre-committed and immutable wording

> **Gate.** Does the leg state a general structural criterion for viscous-term enclosure
> that is falsifiable on at least one banked model of this repository?
> — `yes` → Bank the criterion together with the named falsification test. **This still
> does not become a lane.**
> — `no` → Report VACUOUS and stop. The route dies; it is never redrafted and never
> becomes a lane.

**Answer: `yes`.** The criterion is stated in §2, its five named falsification tests in §4,
and **it does not become a lane** — §6 says why that is not a formality but the criterion's
own consequence. The gate was not edited and this leg does not think it is wrong.

---

## 1. What is being asked, and what "prior art" it inherits

Leg 240 measured a distinction and named its two sides. The viscous term of a self-similar
blow-up certificate is either

* **DOMINATED** — the certified object is the `ν = 0` system and viscosity is admitted as a
  decaying error under a scalar inequality on the scaling exponent. This is what
  `arXiv:2208.09445`, `arXiv:2310.05325` and (independently, with the computer removed)
  `arXiv:2501.15701` all do; or
* **ENCLOSED** — `ν` sits *inside* the certified problem, so the certified object itself
  depends on `ν`. This is what Dähne–Figueras do for complex Ginzburg–Landau
  (`arXiv:2410.05480`) and what `arXiv:2404.04054` does for viscous Burgers and the
  nonlinear heat equation.

Leg 240 asked whether a particular author group had closed that gap and answered **NO**, at
full text, twice over. It did not ask *why* — whether the gap is a contingency of effort or a
structural fact. That is this leg's question, and the gate demands the answer take the form of
a **falsifiable criterion**, not an explanation.

**Inherited prior art, stated up front and not claimed** (full pass in
`writeup/novelty/leg_318.md`): the sub/critical/supercritical classification of a dissipative
term against a scaling is **decades-old folklore** — Kiselev's survey `arXiv:1009.0540`,
`arXiv:1408.5499`, `arXiv:1809.04373`, `arXiv:2503.11095` and a dozen others populate that
cell. The criterion below **rests on** that classification and claims none of it. What the
§0a pass found unoccupied — nine ANDed queries, every zero audited component-wise against a
verified-working AND operator — is the cell where the classification is turned into a
**decision rule for a certificate designer** with a test that can kill it.

---

## 2. The criterion: **ENCLOSURE IS CRITICALITY**

> **You cannot enclose an object that does not exist.** A `ν`-dependent self-similar profile
> exists only when the dissipative term is scaling-**critical** for the blow-up ansatz.
> DOMINATED is therefore not a weakness of anyone's method; it is the **signature of a
> subcritical dissipative term**.

**Setting.** An evolution equation `∂_t u = N(u) + ν D u`, with `N` the inviscid part and `D`
dissipative and homogeneous of order `m` under `x ↦ λx`. Fix a self-similar ansatz
`u(x,t) = (T−t)^{−a} U(x/(T−t)^b)`, `s = −log(T−t)`, chosen so that `N` is **autonomous** in
`s`; let `A` be the exponent set admissible for the inviscid profile problem. In the rescaled
equation the dissipative term carries a prefactor `e^{−δ_dis s}`; call `δ_dis` the
**dissipation-criticality defect**. For a scalar operator of order `m` with the ansatz's own
`b`, `δ_dis = 1 − m·b`. For a system whose dissipation coefficient carries a field weight —
BCG's `ν/ρ ∼ S^{−1/α}` — `δ_dis` is the paper's own.

### C1 — criticality (necessary)

* **`δ_dis > 0` on all of `A`** ⟹ the rescaled system is genuinely **non-autonomous** in `s`,
  so every steady state of it solves the `ν = 0` system. **There is no `ν`-dependent profile
  object to enclose.** DOMINATED is the strongest treatment available, and it is maximal, not
  provisional.
  *Proof, one line:* a fixed point of the rescaled flow requires the explicit `s`-dependence
  to vanish; `e^{−δ_dis s}` with `δ_dis > 0` vanishes only in the limit, so the `ν`-term is
  absent from every fixed point.
* **`δ_dis = 0` at some `b ∈ A`** ⟹ the rescaled system is **autonomous with `ν` as a genuine
  parameter**; the enclosed object exists and enclosure is structurally possible.
* **`δ_dis < 0`** ⟹ dissipation outscales the nonlinearity, the ansatz fails, and the expected
  outcome is no blow-up at all.

### C2 — order compatibility (necessary for *continuation* from `ν = 0`)

Even where C1 holds, an **existing** `ν = 0` certificate can be **continued** into `ν > 0`
only if `D` does not raise the differential order of the profile problem. If
`ord D > ord N`, the `ν > 0` problem is a **singular perturbation**: its solution set is not a
deformation of the `ν = 0` one, and the enclosure must be built **ab initio** at fixed `ν > 0`.

### C3 — bridge type (necessary at PDE level) — **cited to leg 315, not claimed here**

The validated ODE→PDE bridge available in the literature is Zgliczyński's self-consistent
a-priori bounds (`math/0005247`), whose hypotheses are **dissipative**; BCG's rescaled system
is **quasilinear hyperbolic**. Leg 315 established this; this leg re-located `math/0005247`
independently through `all:"rigorous numerics" AND all:"dissipative PDE"` (2 hits, both
dissipative objects) and does no more than cite it.

### The criterion is NECESSARY, NOT SUFFICIENT

This is load-bearing and it is tested (FT5). Incompressible Navier–Stokes satisfies C1
exactly and C3 too, and is still closed — by the **NRS/Tsai non-existence theorems**, which
`plan_of_record.py`'s stage `P0` gate already carries as its screen. A criterion that opened a
route there would be refuted on the spot by a published theorem. **This one screens routes
out; it never opens one.**

---

## 3. The sharp corollary, and the realization named (lesson 91)

### **THE KNIFE-EDGE: the enclosure exponent is the domination window's own excluded endpoint.**

For BCG-type compressible implosion, leg 240 banked the viscous inequality in three papers'
notations, agreeing to `1.78e-15`: `δ_dis = (r−1)/α + r − 2`, with `α = (γ−1)/2`. Setting it
to zero,

```
2(r−1) + (r−2)(γ−1) = 0   ⟹   r(1+γ) = 2γ   ⟹   r = 2γ/(γ+1),
```

which is **exactly BCG's own threshold `r > 2γ/(γ+1)`** — i.e. exactly the **lower endpoint of
the banked domination window**, at every `γ`. Numerically, against leg 240's bank read from
its JSON rather than re-typed:

| γ | banked window | `r_crit = 2γ/(γ+1)` | deviation |
|---|---|---|---|
| 7/5 | `(1.1666666666666667, 1.1909830056250525)`, width `0.024316338958385808` | `7/6` | **`0.0`** |
| 5/3 | `(1.25, 1.2679491924311228)`, width `0.017949192431122807` | `5/4` | **`0.0`** |

So the two treatments are **complementary in the scaling exponent and share exactly one
point, which neither occupies**:

* **DOMINATED owns the open interval** `(2γ/(γ+1), r_*(γ))`. On the γ = 7/5 window the entire
  domination margin is `δ_dis ≤ 0.1458980337503153` — reproduced here to `< 1e-6` of leg 240's
  own banked maximum, as a control.
* **ENCLOSED could only live at `r = 2γ/(γ+1)`**, the endpoint the window **excludes** —
  because that is precisely where the domination decay rate hits zero (`δ_dis` at the window's
  lower endpoint, computed here: `8.88e-16`, i.e. zero to a rounding).
* And at that one point enclosure is blocked twice over: by **C2**, because the Euler profile
  problem is first order in the similarity variable and admitting `ν Δ` makes it second order
  — a singular perturbation, not a continuation; and by **C3**, the hyperbolic-vs-dissipative
  bridge mismatch.

**This is the structural answer to leg 240's measurement.** The enclosure-eligible set has
**measure zero in `r`**, and at its single point the cheap route in (continuation from the
inviscid certificate) is closed by an order jump. Nobody failed to enclose the viscous term
for want of effort.

---

## 4. The five named falsification tests

Every one is asserted in the runner, every one could have come out against the criterion, and
one of them **did**, until its instrument was fixed (§5).

| id | test | on which banked model | what would refute it | verdict |
|---|---|---|---|---|
| **FT1** | the knife-edge identity: `zero(δ_dis) = {r = 2γ/(γ+1)}` **and** that value is the banked window's *lower* endpoint at every γ | leg 240's bank, `writeup/data/p2_route_cns2_v1_lit.json` | any γ where they differ beyond leg 240's own `1.78e-15` transcription tolerance; **or** a bank whose lower endpoint turns out to be a profile-existence bound | **NOT REFUTED** (residual **identically 0** in exact rationals over 45 γ; endpoint deviation `0.0` at both banked γ; the lower endpoint is confirmed *not* a profile-existence bound, which supplies `r_*` and is strictly larger) |
| **FT2** | C1 against every banked row that carries a certificate: ENCLOSED ⟺ `δ_dis = 0`, DOMINATED ⟺ `δ_dis > 0` | `solver/viscous_novelty.py:PRECEDENTS` (leg 197) + leg 240 | one banked row enclosing a dissipative term at `δ_dis ≠ 0`, or DOMINATED at `δ_dis = 0` | **NOT REFUTED** — 4 rows tested, 3 abstained |
| **FT3** | C2: a certificate **continued** from `ν = 0` has no order jump | DF-CGL (`arXiv:2410.05480`), the only banked continued row | a validated continuation from `ν = 0` across an order jump — e.g. a viscous-Burgers branch certified down to `ν = 0` | **NOT REFUTED** |
| **FT4** | **out-of-sample**: C1 extended to `μ(ρ) = ρ^θ`, predicting two published theorems located in this leg's *own* §0a pass | BCG-NS extended; targets `arXiv:2512.18545`, `arXiv:2603.10141` (**both new to this repository's bank**) | an implosion theorem at `θ = 1`; or `arXiv:2603.10141`'s threshold ≠ `θ_*` | **NOT REFUTED on the sign test; the threshold-value half is NAMED AND NOT YET RUN** |
| **FT5** | necessary-not-sufficient, on the repository's own target | incompressible NS Leray self-similar, `plan_of_record.py` `P0`'s NRS/Tsai screen | reading C1 as sufficient — i.e. as saying an enclosure is achievable there | **NOT REFUTED** |

### FT2's table, in full — including every abstention

| model | `δ_dis` | C1 says | the bank says | C2 order jump | consistent |
|---|---|---|---|---|---|
| BCG-NS (compressible implosion) | `0.07294901687515853` (window midpoint, γ=7/5) | DOMINATION_ONLY | DOMINATED | yes | ✔ |
| DF-CGL `2410.05480` | `0.0` | ENCLOSURE_POSSIBLE | ENCLOSED | **no** | ✔ |
| BC viscous Burgers `2404.04054` | `0.0` | ENCLOSURE_POSSIBLE | ENCLOSED | yes | ✔ |
| BC nonlinear heat `2404.04054` | `0.0` | ENCLOSURE_POSSIBLE | ENCLOSED | no | ✔ |
| Chen–Hou Euler/Boussinesq | — | **ABSTAIN** | no certificate of a viscous term | — | abstained |
| dissipative gCLM `2207.07548`, `1908.09385` | — | **ABSTAIN** | no certificate at all | — | abstained |
| incompressible NS (Leray) | `0.0` | ENCLOSURE_POSSIBLE | **NONEXISTENT** (NRS/Tsai) | yes | abstained — this is FT5 |

**The abstentions are the point.** A criterion that "explains" rows it cannot see is
unfalsifiable; the runner counts them and a control fails the process if fewer than two rows
abstain.

Note the C2 column separating DF-CGL from viscous Burgers: **both** are ENCLOSED, but only
DF-CGL has no order jump — its `ε` multiplies the *same* Laplacian as the dispersive term.
That is exactly why DF can follow branches from `ε = 0` (their Thm 4.1) while nothing in the
bank continues a viscous-Burgers branch down to `ν = 0`; `2404.04054` certifies at fixed `ν`,
ab initio, as C2 says it must. **C2 was written before that column was computed.**

### FT4 in detail — the test most able to kill the criterion

C1 is extended to density-dependent viscosity `μ(ρ) = ρ^θ`. BCG's viscous term enters as
`(μ/ρ)Δu`; for constant `μ` the `ρ^{−1}` contributes the `(1/α)(1−r)` piece of
`−δ_dis = 2 − r + (1/α)(1−r)`. Replacing `ρ^{−1}` by `ρ^{θ−1} = (ρ^{−1})^{1−θ}` scales that
piece by `(1−θ)`:

```
δ_dis^(θ) = (1−θ)(r−1)/α + r − 2 ,      θ_*(γ,r) = 1 − α(2−r)/(r−1).
```

**This is DERIVED here from BCG's own exponent bookkeeping, not transcribed from either target
paper**, and it is flagged as such everywhere it is used. `θ = 0` recovers the published
formula to **`0.0`** (exact), which is the control on the derivation.

* **Prediction 1.** `θ = 1` — viscosity *linear* in density, the shallow-water degeneracy —
  gives `δ_dis^(1) = r − 2 < 0` for every `r < 2`, hence **supercritical**: the implosion
  mechanism cannot survive. Verified negative across the whole banked γ=7/5 window.
  **`arXiv:2512.18545` proves exactly that** — globally regular spherically symmetric
  solutions that cannot cavitate or implode, all `γ ∈ (1,∞)` in 2D and `γ ∈ (1,3)` in 3D.
* **Prediction 2.** Below `θ_*(γ,r)` the dissipation is subcritical and implosion survives, as
  DOMINATED — i.e. there is a **threshold in the viscosity power depending on the adiabatic
  exponent**. `arXiv:2603.10141`'s abstract, verbatim: *"We identify a threshold value,
  depending on the adiabatic exponent, such that, for any power below this threshold, there
  exists a class of smooth initial data … which implode … the degenerate viscous terms are not
  sufficiently strong to suppress the convective mechanism."* Predicted values at the window
  midpoints: `θ_*(7/5) = 0.08158712005267243`, `θ_*(5/3) = 0.046205799573696305`.

**What is honestly not done.** Only the *abstract* of `arXiv:2603.10141` was read. The
threshold **value** is therefore an open, named, one-leg falsification test — read that paper
at full text and compare its threshold with `θ_*(γ,r)`. If they disagree, C1's extension to
degenerate viscosity is refuted. The runner records this as *"NOT REFUTED (sign test passes;
threshold-value test NAMED AND NOT YET RUN)"* and the leg does not claim the match.

---

## 5. The instrument that had to be fixed, not the tolerance

**FT1 first came out `REFUTED`, and it was wrong.** In float64,
`max |δ_dis(γ, r_crit(γ))|` over 45 γ is **`5.329070518200751e-15`**, and the natural `1e-15`
tolerance therefore reported the knife-edge identity as **FALSE** — the leg's central claim,
killed by its own test.

~~Diagnosis before belief (leg 302's lesson, and this is the same failure mode verbatim — *an
IEEE-double cancellation masquerading as a transcription error*): `(r−1)/α` and `(r−2)` are two
quantities of size `≈ 0.9756` at the worst γ that cancel **exactly**, so the residual is
**`5.462e-15` relative**, about 25 ulp of the cancelled operands. That is what catastrophic
cancellation costs; it is not evidence about the identity.~~

**[LEG 337 CORRECTION — mechanism re-measured, FT1's verdict unchanged.]** The paragraph above
is struck: it named the wrong mechanism. Directly re-measuring which operand carries the
rounding error (`experiments/journal/leg_337.md` has the full script and grid): at the worst
γ = 1.075, `α_of(γ)` is computed with **zero** rounding error in float64 — `γ − 1.0` is exact by
Sterbenz's lemma and the following halving is always exact, so α carries no ulp at all. All of
the error lives in `r_crit(γ) = 2γ/(γ+1)`, whose float64 value differs from the true rational
`2γ/(γ+1)` by **`−0.88 ulp(r)`** (≈ 1 ulp), from the addition-then-division inside `r_crit`.
That single sub-ulp error in `r` is then **amplified** by δ_dis's own sensitivity to `r` at the
root, `d(δ_dis)/dr = 1/α + 1 = 27.667` at this γ (dominated by the `1/α = 26.667` term):
substituting the *exact* rational `r` and `α` into δ_dis gives exactly `0`; substituting the
*actual* float64 `r` (with its `−0.88 ulp` error) and the *actual* float64 `α` (0 error) into
δ_dis, evaluated in exact rational arithmetic, reproduces `−5.424e-15` — matching the observed
float64 residual `−5.329e-15` to within the small extra rounding of δ_dis's own float ops. So
it is **not** cancellation between two `≈1`-sized operands that costs precision; it is **1 ulp
of pre-existing rounding error in one operand (r), amplified by the other operand's reciprocal
(1/α)**. Confirmed across the full 45-γ grid: `α_of` never carries nonzero ulp error at any
grid point; `r_crit` always does, and the residual scales with `1/α_of(γ)` accordingly. "Leg
302's failure mode" as a category label is retracted with it — this is ill-conditioning under
amplification near a root, not a subtraction-of-near-equal-terms precision loss. **FT1's
verdict is byte-unchanged**: decided in exact rational arithmetic, residual identically `0`,
either way.

**The fix is the right instrument, not a looser threshold.** FT1's verdict is now decided in
**exact rational arithmetic** (`fractions.Fraction`), where the residual over the same 45 γ is
**identically `0`**. The float number is kept in the JSON as the *diagnosis*, never as the
*measurement*. Had the tolerance simply been relaxed to `1e-14`, the test would have passed
for the wrong reason and would have had no power to detect a genuine transcription error of
size `1e-14`.

---

## 6. Consequences — including the ones against this leg's own interest

**It does not become a lane, and that is the criterion's own verdict, not an administrative
restriction.** The criterion's only positive statement about BCG's object is that enclosure is
structurally possible on a set of **measure zero in `r`**, at a point where C2 forbids
continuation and C3 forbids the bridge. There is nothing to build. The gate's yes-branch
already said this; the mathematics agrees with it.

**No link of L1→L4 moved.** A statement about what *could* be enclosed is not a link moving.
Clay odds stay ~0.05%, behind Walls 1 and 2.

**It strengthens leg 240 rather than extending it.** Leg 240's negative was about one author
group's publication record; this leg says the negative would have held for any group, because
the object they would have had to enclose does not exist at the exponents their theorem lives
at. The two independent confirmations leg 240 already had — CGSS and the computer-free
Shao–Wei–Wang–Zhang route — are exactly what C1 predicts: the domination is a property of the
*scaling*, so removing the computer from the argument cannot change it.

**What it says about this repository's own target is not encouraging, and is said anyway.**
For incompressible NS the viscous term *is* scaling-critical, C1 is satisfied, and the
enclosure question was never the obstruction — NRS/Tsai non-existence is. Moving from the
compressible object to the incompressible one trades a *measure-zero* enclosure window for a
*non-existence theorem*. That is a worse position, not a better one, and the criterion is what
makes the comparison sayable at all.

**Adjacency declared, not entered.** Leg 305 (Route-DWM) is live on whether the
dominance-window **deficit** is sharp or slack via a per-constant ledger. This leg uses only
the window's **endpoint identity**, touches none of 305's files, and re-derives none of its
per-constant decomposition. Where the two meet: 305's certified width `0.0243163` against
available `0.1666667` — shortfall exactly `(7+3√5)/2 = 6.8541019662496845446`, leg 300's
corrected closed form, **not** the `6.855` this run corrected across seven surfaces — is
cross-checked here to `< 1e-9` purely as an internal consistency control on the banked width,
and is **not** re-derived as a result of this leg.

---

## 7. Controls (lesson 90), asserted in code

All eight pass; the runner exits non-zero if any fails.

| control | why it exists |
|---|---|
| `not_a_tautology__test_set_discriminates` | the test set must contain **both** a banked ENCLOSED row and a banked DOMINATED row plus rows the criterion abstains on |
| `not_a_tautology__C1_can_output_all_three_classes` | the classifier must be able to emit all three verdicts, not only the one the bank happens to contain |
| `abstention_is_recorded_not_hidden` | ≥2 rows must be abstained on and counted |
| `adverse__delta_dis_is_strictly_positive_on_the_OPEN_window_only` | the knife-edge claim **requires** `δ_dis` to vanish at the lower endpoint and be positive inside; positive *at* the endpoint would make "complementary, sharing one point" false |
| `adverse__banked_delta_dis_max_reproduced` | this leg's `δ_dis` must reproduce leg 240's banked maximum `0.1458980337503153` — otherwise it is testing a different formula from the bank it claims to test against |
| `adverse__criterion_makes_a_prediction_it_could_lose` | FT4's `θ = 1` sign test was run **before** `2512.18545`'s theorem was consulted for its direction; a positive sign would have been refuted by a published theorem the leg did not choose |
| `leg_305_territory_not_entered` | recorded, not assumed |
| `exact_closed_form_quoted_not_truncated` | `(7+3√5)/2` exactly, cross-checked against the banked width |

---

## 8. What this leg did **not** do

* Did not touch `plan_of_record.py`, `requirements.txt`, `writeup/build_figures.py`,
  `solver/capabilities.py`, or any other leg's territory. `solver/viscous_novelty.py` was
  **imported, never edited**.
* Did not build a solver module, a certificate, or any apparatus. This was a scoping leg.
* Did not read `arXiv:2603.10141` or `arXiv:2512.18545` at full text — abstracts only — and
  says so wherever their content is used.
* Did not register `fig84` in `writeup/INDEX.md` or `writeup/build_figures.py`; those are
  shared and integration allocates centrally. The figure file is written directly, as leg 315
  did with `fig79`.
* Did not widen into leg 305's per-constant ledger.
* Did not claim novelty for the criticality trichotomy, which is folklore.
