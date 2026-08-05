# Leg 67 — Route-FD novelty pass: is there a PUBLISHED critical fractional-dissipation exponent for 2D Boussinesq?

**Date:** 2026-08-05. **Agent:** LEG-H. **Branch:** `leg/fd-v1`. **Claim-bearing,
literature-only leg** — no computation beyond arithmetic on numbers already on file, and **no
new solve was run under either branch of the gate**.

Per `writeup/novelty/README.md` and the lesson from leg 53: **links, not counts.** Every query
string below is verbatim; every link a query returned that I judged worth recording is listed;
where a query returned nothing on-topic I say so instead of reporting a number.

**Bans checked before starting.** `plan_of_record.py` prints "re-measuring beta on the 2D object
(lifted by: never — leg 43 showed the object does not converge)" and "chasing the 2D near-null
direction of leg 44". This leg measures nothing: it checks the **critical fractional-dissipation
exponent** `s_c`, a stored constant derived from published Chen–Hou rescaling constants, against
the literature. It runs no solve, fits no growth rate, and touches neither ban. The
`capabilities.py` grep required before building anything was run; nothing was built.

---

## The claim under test, as this repository states it

`capabilities.py` line 107–110, verbatim:

> `{"module": "solver/fractional_boussinesq.py", "object": "2D Boussinesq, fractional dissipation",`
> ` "holds": "the critical-dissipation exponent for the 2D object",`
> ` "validated": "consistency with the 1D critical exponent; no independent known answer",`
> ` "test": "test_fractional_boussinesq.py"},`

and the number itself, from `solver/fractional_boussinesq.py`'s module docstring:

> "**beta(Chen-Hou 2D Boussinesq) = 2.9206  =>  s_c = 0.17120 .**"

built on the law (same docstring, (SC)) `s < s_c = 1 / (2 beta)` with `beta = -c_l/c_omega` from
the Chen–Hou Part I (arXiv:2210.07191, (2.23)) constants `c_l = 3.00649898`,
`c_omega = -1.02942516`.

**The question this pass answers is whether "no independent known answer" is still true.**

---

## Queries, verbatim, with the links returned

### Q1
`2D Boussinesq fractional dissipation critical exponent blow-up Hou-Luo boundary`

- https://www.sciencedirect.com/science/article/abs/pii/S0022039621004447 — Boundary layer models of the Hou-Luo scenario
- https://arxiv.org/html/2605.16322 and https://arxiv.org/pdf/2605.16322 — A unified Boussinesq–Euler formulation and finite-time blow-up for a Hou–Luo type boundary-jet system
- https://arxiv.org/pdf/2010.00648 — Boundary layer models of the Hou-Luo scenario
- https://www.tandfonline.com/doi/full/10.1080/00036811.2026.2685067 — Comprehensive analysis of the 2D generalized Boussinesq equations with critical anisotropic fractional dissipation
- https://link.springer.com/article/10.1007/s11854-018-0073-4 — A global regularity result for the 2D Boussinesq equations with critical dissipation
- https://link.springer.com/content/pdf/10.1007/s00220-021-04067-1.pdf — Chen–Hou, Finite Time Blowup of 2D Boussinesq and 3D Euler with C^{1,α} Velocity and Boundary

**On-topic for the stored quantity: none.** Every "critical" here is either a *well-posedness*
threshold (the Springer/Taylor&Francis hits) or an *inviscid* blowup theorem (Chen–Hou). The two
categories never meet in one paper.

### Q2
`finite time blowup 2D Boussinesq with fractional dissipation (-Delta)^s self-similar profile persists supercritical`

- https://arxiv.org/pdf/2604.01868 — Novel Self-similar Finite-time Blowups … 1D Hou-Luo Model and the 2D Boussinesq Equations
- https://arxiv.org/abs/2305.05660 — Chen–Hou, Stable nearly self-similar blowup … II: Rigorous Numerics
- https://arxiv.org/pdf/2210.07191 — Chen–Hou, … I: Analysis
- https://arxiv.org/pdf/1910.00173 — Chen–Hou, C^{1,α} velocity and boundary
- https://arxiv.org/pdf/2308.01528 — Exact self-similar finite-time blowup of the Hou-Luo model with smooth profiles
- https://epubs.siam.org/doi/10.1137/23M1580395 — MMS version of Part II

**On-topic: none.** All six are inviscid. Abstracts of 2604.01868 and 2210.07191 were fetched and
checked directly (below); **neither mentions dissipation at all**.

### Q3
`Chen Hou 2D Boussinesq blowup stability under fractional Laplacian dissipation critical alpha threshold`

- https://arxiv.org/abs/2606.03680 — Stefanov–Wu–Xu–Ye, Global regularity of the 2D fractional Boussinesq equations with subcritical dissipation
- https://arxiv.org/pdf/1506.00470 — Global well-posedness of the 2D Boussinesq equations with fractional Laplacian dissipation
- https://link.springer.com/article/10.1007/s00021-015-0245-2 — Global Regularity Results … Fractional Laplacian Dissipation
- https://arxiv.org/pdf/2408.15154 — Long-time stability of a stably stratified rest state
- https://jiajiechen94.github.io/research — Jiajie Chen's publication list
- https://arxiv.org/pdf/2207.06581 — Existence of blowup solutions to Boussinesq on R^3 with dissipative temperature

**On-topic: `2606.03680` only, and as a survey of the *other* quantity.** Read at full text below;
it is the most recent and most complete published account of what "critical" means for 2D
Boussinesq under fractional dissipation, which is exactly what is needed to settle the gate.

### Q4
`Hou-Luo model 1D fractional dissipation Lambda^s blowup threshold critical exponent scaling`

- https://arxiv.org/pdf/2601.02464 — Rampf–Kolluru, Complex-time singular structure of the 1D Hou-Luo model
- https://arxiv.org/html/2308.01528 — Exact self-similar finite-time blowup of the Hou–Luo model
- https://arxiv.org/pdf/2604.01868 — Novel Self-similar Finite-time Blowups …
- https://users.cms.caltech.edu/~hou/papers/HL-Annals-PDE-202.pdf — Asymptotically self-similar blowup of the Hou-Luo model
- https://arxiv.org/pdf/2312.01702 — Tracking complex singularities of fluids on log-lattices

**A retracted lead, recorded because it nearly became a false positive.** The search engine's
prose summary of this query asserted: *"the critical dissipation exponent is γ = 1/3, which
represents the value at which the dissipative term is no longer strong enough to prevent a
finite-time singularity."* **This is not in any of the returned papers.** I fetched
arXiv:2601.02464's abstract and arXiv:2604.01868's abstract in full: neither mentions fractional
dissipation, a critical dissipation exponent, or the value 1/3. A follow-up query
(`"critical dissipation exponent" Hou-Luo model 1/3 fractional Laplacian blowup arrested`)
returned nothing supporting it either, and its own summary silently re-attached "1/3" to a
*different* object — a `C^γ` Hölder norm of the density `θ` with `γ ≈ 1/3`. **The number was a
search-summary artefact and is discarded.** This is logged, not deleted, because a search-level
pass that had stopped one step earlier would have reported a published 1D critical exponent that
does not exist.

### Q5
`2D Boussinesq global regularity fractional dissipation alpha threshold (sqrt(1777)-23)/24 supercritical`

- https://arxiv.org/abs/2606.03680 and https://arxiv.org/pdf/2606.03680 — Stefanov–Wu–Xu–Ye
- https://arxiv.org/pdf/1411.1362 — A global regularity result for the 2D Boussinesq equations with critical dissipation
- https://arxiv.org/pdf/1510.03237 — Global smooth solution to the 2D Boussinesq equations with fractional dissipation
- https://www.researchgate.net/publication/309206998 — On the global regularity of the 2D critical Boussinesq system with α>2/3

**On-topic for the *other* quantity, and this is the query that located the exponent ladder** read
verbatim below. Note the ladder is `(√1777−23)/12 ≈ 0.7981`, not `/24` as my query guessed.

### Q6
`axisymmetric Euler Hou-Luo blowup with fractional viscosity Lambda^{2s} scaling argument dissipation negligible self-similar`

- https://users.cms.caltech.edu/~hou/papers/mms_luo_hou_2014.pdf — Luo–Hou 2014
- https://arxiv.org/abs/2106.05422 — Asymptotically self-similar blowup of the Hou-Luo model
- https://arxiv.org/pdf/2405.10916 — Nearly self-similar blowup of generalized axisymmetric Navier-Stokes equations
- https://arxiv.org/pdf/2212.11912 — Potential Singularity of the Axisymmetric Euler with C^α Initial Vorticity
- https://arxiv.org/pdf/2102.06663 — Potential singularity formation … with degenerate viscosity coefficients
- https://arxiv.org/pdf/1708.09648 and https://arxiv.org/pdf/1402.4560 — remarks on the Luo–Hou ansatz

**On-topic: none.** `2405.10916` and `2102.06663` are the closest — viscous, self-similar,
Hou-authored — but both use *degenerate/solution-dependent* viscosity, not a fractional exponent
dial, and `2405.10916`'s abstract (fetched) gives an *effective dimension* ≈ 3.188, not a
dissipation exponent.

### Q7
`blowup 2D Boussinesq supercritical hypodissipation proved singularity persists small fractional dissipation exponent`

- https://link.springer.com/article/10.1007/s00332-014-9220-y — Eventual Regularity of 2D Boussinesq with Supercritical Dissipation
- https://www.sciencedirect.com/science/article/abs/pii/S0022247X24003299 — Regularity criteria of the 2D fractional Boussinesq in the supercritical case
- https://arxiv.org/pdf/1608.01285 — Blowup with vorticity control for a 2D **model** of the Boussinesq equations
- https://arxiv.org/html/2510.10090 — On the Profile of Singularity Formation for the Incompressible **Hydrostatic** Boussinesq system
- https://arxiv.org/html/2209.08713 — Non-uniqueness of Leray solutions to the hypodissipative Navier-Stokes in 2D
- https://math.okstate.edu/people/jiahong/CMS_14_07_A10.pdf — Regularity criteria for the 2D Boussinesq

**On-topic: none.** The supercritical Boussinesq literature produces *regularity criteria* and
*eventual regularity*, i.e. conditional statements, never a threshold exponent at which a known
blowup is arrested. `1608.01285` is a 2D **model**, not the system.

### Q8
`"2D Boussinesq" blowup "how much dissipation" critical fractional exponent self-similar collapse rate (T-t)^beta viscosity defeats singularity`

Returned the same Chen–Hou inviscid set plus `2606.03680` and the Taylor & Francis anisotropic
paper. **Nothing new.** This is the query most directly phrased as the gate, and it produced no
object the gate could consume.

### Q9
`Chen Hou 2210.07191 Boussinesq self-similar profile c_l c_omega values 3.0065 1.0294 scaling parameters`

- https://link.springer.com/article/10.1007/s00205-026-02195-3 — Stationary Self-Similar Profiles for the 2D Inviscid Boussinesq
- https://arxiv.org/abs/2210.07191, https://arxiv.org/abs/2305.05660, https://users.cms.caltech.edu/~hou/papers/MMS-Numerics-2025.pdf

**No source outside this repository re-quotes the pair `(c_l, c_omega)` in a dissipation
context.** They are published *rescaling* constants; the conversion to a dissipation exponent is
this repository's, and remains this repository's.

### Q10 (targeted publication-list sweep, not a search engine)
Fetched https://jiajiechen94.github.io/research and extracted every title mentioning Boussinesq,
dissipation, viscosity or fractional Laplacian:

- arXiv:2305.05660 — Stable nearly self-similar blowup … II: Rigorous Numerics
- arXiv:2210.07191 — … I: Analysis
- arXiv:2206.01296 — On stability and instability of C^{1,α} singular solutions to the 3D Euler and 2D Boussinesq equations
- arXiv:1908.09385 — **Singularity formation and global well-posedness for the generalized Constantin–Lax–Majda equation with dissipation**

**The author who proved the 2D Boussinesq blowup has exactly one paper combining blowup with
dissipation, and it is the 1D gCLM.** That is the strongest single piece of evidence for the
gate's answer, and 1908.09385 was therefore read at full text.

---

## Papers read at full text

`bash Papers/fetch.sh 1908.09385 2606.03680` — arxiv.org HTTP 200, both fetched, both extracted
with `pdftotext -layout`. (`Papers/` is gitignored; re-run to reproduce the quotes.)

### 1. arXiv:2606.03680 — Stefanov, Wu, Xu, Ye, *Global regularity of the 2D fractional Boussinesq equations with subcritical dissipation*

**Read:** abstract, §1 introduction in full (the complete survey of published exponents), and the
reference list. This is the newest and most complete published account of "critical dissipation"
for exactly the system in question — dissipation `(-Δ)^{α/2} u` and `(-Δ)^{β/2} θ`.

**It poses the gate's question in the gate's own words, and answers a different one.** Verbatim,
§1:

> "In contrast, determining whether local classical solutions of the inviscid Boussinesq
> equations can develop finite-time singularities remains an extremely challenging problem.
> Recently, some significant progress on the inviscid Boussinseq equations finite-time blowup
> problem has been made (see, e.g., [5, 6, 7, 10, 13, 14]). **This naturally leads to the
> fundamental question: how much dissipation is required to ensure global regularity?**"

That is our question. What the literature supplies in answer is a ladder of **sufficient
conditions for global regularity**, never a critical value. Verbatim, §1, with the definition of
"critical":

> "Jiu, Miao, Wu, and Zhang [20] discovered that the global regularity problem for (1.1) depends
> crucially on the value of α + β. In the special case α + β = 1, the Boussinesq regularity
> problem boils down to the corresponding problem on the generalized surface quasi-geostrophic
> equation with critical dissipation. This insight led to the classification of α+β into three
> regimes: the subcritical regime (α+β > 1), the critical regime (α+β = 1) and the supercritical
> regime (α + β < 1). … In particular, **the global regularity problem for the supercritical
> regime remains largely out of reach**, while substantial progress has been made in the critical
> and subcritical cases."

and the ladder itself, verbatim (all are global-regularity *sufficient* conditions):

> "α + β = 1, α > (23 − √145)/12 ≈ 0.9132." (Jiu–Miao–Wu–Zhang [20])
> "α + β = 1, α > (√1777 − 23)/12 ≈ 0.7981." (Stefanov–Wu [24])
> "α + β = 1, α > 10/13 ≈ 0.7692." (Wu–Xu–Xue–Ye [26])
> "α + β = 1, α > 2/3" (the authors [25], under small `‖θ₀‖_∞`)
> "α + β > 1, 0.8876 ≈ (6 − √6)/4 < α < 1." (Miao–Xue [22])
> "α + β > 1, 0.7351 ≈ (10 − 2√10)/5 < α < 1." ([28])
> "β > 2/(2+α), 0 < α < 1." (Constantin–Vicol [9])

Earlier endpoints of the same ladder, also §1: Chae [4] and Hou–Li [19] at `α = 2, β = 0` or
`α = 0, β = 2`; **Hmidi–Keraani–Rousset [16,17] at `α = 1, β = 0` or `α = 0, β = 1`.**

**Verdict.** `2606.03680` publishes a critical *exponent relation* for 2D Boussinesq under
fractional dissipation — `α + β = 1` — and it is **not the quantity `solver/fractional_boussinesq.py`
holds.** Its criticality is a *well-posedness/scaling* threshold, inherited by reduction to
critical gSQG; ours is the exponent at which dissipation overtakes a *particular* collapse rate,
`s_c = 1/(2β_collapse)`, and it depends on the Chen–Hou profile's constants, which enter nowhere
in this ladder. Every published number is a one-sided *sufficient* condition for regularity —
an upper bound on any true arrest threshold — so none of them can be equated to `s_c` even in
principle.

### 2. arXiv:1908.09385 — J. Chen, *Singularity formation and global well-posedness for the generalized Constantin–Lax–Majda equation with dissipation*

**Read:** abstract, §1.1 (prior results with dissipation), **§1.2 "Scaling and the critical
dissipation" in full**, §1.3, §1.4 Theorems 1.1–1.5 and Remarks 1.2–1.7. (Leg 65 read this paper
for the weighted-`ℓ¹` claims; §1.2 was not the object then. Leg 45 read it for computer
assistance. This is the first pass to read it *for the dissipation exponent*.)

**This is the one paper found anywhere that publishes a critical dissipation exponent for a
Hou-Luo-family object — and it is 1D, and it is again the scaling quantity.** Verbatim, §1.2:

> "Suppose that L = Λ^γ in (1.1) for some γ ∈ [0, 2]. Then the solution of (1.1) enjoys the
> following scaling property: if ω(x, t) is a solution of (1.1), then for any λ > 0,
> `ω_λ(x, t) ≜ λ^γ ω(λx, λ^γ t)` is also a solution of (1.1). … We will show that for several
> classes of initial data, ‖ω‖_{L¹} is conserved. In these cases, **a simple scaling analysis
> shows that L = Λ corresponds to the critical dissipation.** For (1.1) with a ≤ −1, we will show
> that the equation possesses a-priori L^{|a|} estimate, i.e. ‖ω(t,·)‖_{L^{|a|}} ≤ ‖ω₀‖_{L^{|a|}},
> which makes **Λ^γ with γ = |a|^{−1} the critical dissipation** with respect to the natural
> scaling of the equation."

So the published 1D critical exponents are `γ_c = 1` (for `a > −1`, `L¹`-conserving classes) and
`γ_c = |a|^{−1}` (for `a ≤ −1`) — **derived from which Lebesgue norm the equation's scaling
preserves, not from any blowup profile's collapse rate.** Route-F's `s_c = α/2` (equivalently
`γ_c = α`, the profile's far-field decay exponent) is a *different function of a*: it varies with
the self-similar profile, whereas Chen's `γ_c` is fixed at 1 across the entire range `a > −1`.
The two agree only where `α = 1`.

**The blowup theorems point the same way.** Theorem 1.1, verbatim:

> "**(Finite time blow-up for a close to ½).** Consider (1.1) with Lω = −∂_xx ω. There exists
> δ > 0 such that for a ∈ (½ − δ, ½ + δ), 0 ≤ ν ≤ 1, (2.1) develops a self-similar singularity in
> finite time for some C_c^∞ initial data."

and Remark 1.2:

> "If the dissipative operator is replaced by fractional Laplacian Λ^γ with γ ∈ [0, 2], one can
> apply similar analysis to obtain finite time blowup. We focus on the full Laplacian for
> simplicity. … one can also prove finite time blowup of (1.1) with L = Λ^γ, γ ∈ [0, 1) when a is
> sufficiently close to 0"

**Note the magnitude, because it is the sharpest external datum this pass produced.** Chen proves
blowup **with the full Laplacian** (`γ = 2`, i.e. `s = 1` in our `(-Δ)^s` convention) for `a ≈ ½`
— *above* his own critical line `γ_c = 1`. He therefore does not treat `γ_c` as an arrest
threshold at all, which is precisely the distinction this pass is drawing: **a "critical
dissipation exponent" in the published sense is not a statement about whether a given blowup
survives.** Reading Chen's `γ_c` as comparable to our `s_c` would have produced a contradiction
out of two correct statements about different quantities.

**Verdict.** Not the quantity, not the dimension. It does, however, mean the 1D anchor our 2D
number was validated against is *itself* an internal construction, unmatched by Chen's published
1D critical exponent.

### 3. Abstracts fetched directly and checked for the quantity (no full text warranted)

- https://arxiv.org/abs/2210.07191 (Chen–Hou Part I): abstract reproduced in full; **no mention of
  dissipation, viscosity, or fractional Laplacian, and it does not state `c_l`, `c_omega`.**
- https://arxiv.org/abs/2604.01868 (Novel Self-similar Finite-time Blowups, 1D HL + 2D Boussinesq):
  abstract reproduced in full; **no fractional dissipation, no critical exponent, no scaling
  constants.** Purely inviscid, two-stage `L^∞`-then-`L^p` blowup.
- https://arxiv.org/abs/2601.02464 (Rampf–Kolluru): abstract reproduced in full; complex-time
  analytic structure, **no dissipation of any kind.**
- https://arxiv.org/abs/2405.10916 (generalized axisymmetric NS): abstract; solution-dependent
  viscosity, effective dimension ≈ 3.188, **no fractional dissipation exponent.**

---

## THE GATE

> "Does a primary source publish an independent critical fractional-dissipation exponent for 2D
> Boussinesq (or its vorticity-stream equivalent)?"

**ANSWER: NO** — for the quantity `solver/fractional_boussinesq.py` holds. Stated at full
precision, because a bare "no" would be wrong in the other direction:

1. **A published exponent named "critical fractional dissipation" for 2D Boussinesq exists** and
   is `α + β = 1`, with a ladder of sufficient conditions descending to `α > 2/3` on that line
   (`2606.03680` §1, Jiu–Miao–Wu–Zhang, Stefanov–Wu, Wu–Xu–Xue–Ye). Its vorticity-stream
   equivalent is stated too: at `α + β = 1` the problem "boils down to" critical gSQG.
2. **It is not comparable to our `s_c`.** It is the exponent at which the *equation's scaling*
   stops preserving the controlling norm; `s_c = 1/(2β_collapse)` is the exponent at which
   dissipation overtakes *one specific collapse*. Every published value is a one-sided
   *sufficient condition for global regularity*, i.e. an upper bound on an arrest threshold,
   never an equality. **No arithmetic comparison of the two is meaningful**, and the leg does not
   make one as a claim.
3. **No primary source anywhere publishes an arrest exponent for the Chen–Hou blowup.** The
   blowup corpus (2210.07191, 2305.05660, 1910.00173, 2308.01528, 2604.01868, 2601.02464) is
   inviscid without exception; the dissipation corpus never touches a blowup profile. The one
   author who has published in both, Jiajie Chen, does so in one paper only, in 1D
   (1908.09385), and there the "critical dissipation" is again the scaling quantity.

**Therefore the exponent remains internally-consistent-only. No claim upgrade. No computation
was attempted.**

---

## What the comparison WOULD have been, recorded as arithmetic so the gap has a size

Not a claim — a magnitude, so that "not comparable" is not doing silent work. Converting our
stored number into the literature's convention (`(-Δ)^{α/2}` on the vorticity, so `α = 2s`):

| quantity | value |
|---|---|
| `beta` (Chen–Hou collapse, `-c_l/c_omega`) | `2.9205610051341666` |
| stored `s_c = 1/(2 beta)` | `0.17119998490736224` |
| `alpha_equiv = 2 s_c` | `0.3423999698147245` |
| Chen–Hou far-field exponent `c_omega/c_l` | `-0.3423999698147245` |
| literature critical line `α + β = 1`, at `β = 0` | `α = 1` |
| our `alpha_equiv` as a fraction of that line | `0.3423999698147245` |
| factor by which it sits below the line | `2.9205610051341666` |
| gap in `α` | `0.6576000301852756` |

Two things this table says, and one it does not.

* **The ratio is arithmetically vacuous.** `alpha_equiv / 1 = 1/beta` identically, by the
  definition `s_c = 1/(2 beta)`. Comparing our number to the `α+β=1` line recovers `beta` and
  nothing else. **This is the precise sense in which the check "against a published value" is
  unavailable: the only published line is the one our formula reproduces trivially.**
* **`alpha_equiv` coincides with the Chen–Hou far-field exponent** `|c_omega/c_l| = 0.34240`, to
  all digits — as `collapse_exponent_from_rescaling`'s docstring predicts (`alpha = -1/beta`).
  Also internal, also not a check.
* **One weak external consistency statement is available, and it passes.** Hmidi–Keraani–Rousset
  (via `2606.03680` §1) prove global regularity at `α = 1, β = 0`. Our law predicts arrest for
  `α > 0.34240`, so it predicts regularity at `α = 1`: **consistent, with the published datum
  sitting a factor `2.9206` above our threshold.** The check is one-sided and weak — it would
  pass for any `s_c < 0.5` — but it is the only contact between our number and a published one,
  and it is not a contradiction. Recorded as a margin, not as a validation.

**Where a real check would have to come from:** a published statement of the form "the Chen–Hou /
Hou–Luo self-similar blowup persists for `(-Δ)^s` with `s < s*`", for the *same* profile. No such
statement exists at the date of this pass. The nearest existing objects — `2606.03680`'s
supercritical regime `α + β < 1`, which contains our `alpha_equiv = 0.3424` — is exactly the
regime the survey calls "largely out of reach", so the absence is structural, not an oversight.

---

## The `capabilities.py` correction (OUTSIDE this leg's territory — reported, not applied)

The gate requires the annotation be corrected either way. `capabilities.py` is not in this leg's
file territory, so the exact edit is handed to the orchestrator. Precedent: commit `ab07316`,
"Leg 0: ORCH — correct capabilities.py's holder_norms.py annotation from UNSEARCHED to
searched-and-not-found, per leg 65's full-text literature pass".

**File:** `capabilities.py`, the `solver/fractional_boussinesq.py` entry, `validated` field
(line 109).

**Replace:**

```python
     "validated": "consistency with the 1D critical exponent; no independent known answer",
```

**With:**

```python
     "validated": "consistency with the 1D critical exponent; leg 67 searched at primary source "
                  "and found no comparable published value -- the literature's critical exponent "
                  "for 2D Boussinesq under fractional dissipation is alpha+beta=1 (Jiu-Miao-Wu-Zhang; "
                  "gSQG reduction, arXiv:2606.03680 sec 1), a well-posedness scaling threshold and "
                  "NOT a blow-up-arrest exponent; s_c=0.17120 is alpha_equiv=0.34240, a factor 2.9206 "
                  "below that line, inside the supercritical regime the survey calls largely out of reach",
```

`test_capabilities.py` requires only `len(validated) > 20` and a non-empty field, so the
replacement is drop-in. **The change is from "no independent known answer" (an absence never
looked for) to "searched at primary source and found none, and here is why none exists" — a
strictly stronger statement of the same negative.** No claim is upgraded by it.

---

## Residual risk

Absence at this depth is not proof. Three directions were classified but not read at full text:
(i) the Taylor & Francis anisotropic-critical paper
(https://www.tandfonline.com/doi/full/10.1080/00036811.2026.2685067), paywalled, whose title
promises "blow-up criteria" — but *criteria* are conditional statements, the same category as
`S0022247X24003299`, not threshold exponents; (ii) arXiv:2605.16322, the 2026 Hou–Luo-type
boundary-jet system, which is a *different* system (a jet model), not 2D Boussinesq; (iii) the
Chinese-language and non-arXiv Boussinesq regularity literature, which `2606.03680`'s reference
list surveys and which contains no blowup-arrest statement by that survey's own account. None of
the three could supply a value for the Chen–Hou profile, which is what the gate needs.
