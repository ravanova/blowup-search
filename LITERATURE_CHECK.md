# Literature check — SIXTH PASS (2026-08-04): the papers are read

> ## 🧭 EIGHTH PASS (leg 48, Route-V v0): the check turned to the DISSIPATION DIAL — and
> ## the question stage V was built around is a 2024 theorem
>
> The seventh pass asked *"has anyone already proved the object?"*. Stage V asked a
> different question — *"can a blow-up certificate be followed as dissipation is switched
> on, and what does its margin do?"* — and it too was already answered. The ledger lives in
> `solver/viscous_novelty.py::PRECEDENTS`, gated by `test_viscous_novelty.py` (8/8), and
> unlike a table of citations it **re-derives** what it cites.
>
> | source | what it does | verdict for stage V |
> |---|---|---|
> | **arXiv:2410.05480** (Dahne–Figueras, Oct 2024) | 8 branches of self-similar singular CGL profiles, continued in the dissipation parameter `ε` from the NLS limit, **verified in interval arithmetic** (whole-branch, Case I) | **PRE-EMPTS** |
> | arXiv:2404.04054 | computer-assisted (Newton–Kantorovich, weighted Sobolev) self-similar profiles of parabolic PDEs incl. **viscous** Burgers; no dial followed | ADJACENT |
> | arXiv:2207.07548 (ALS) | dissipative gCLM, analysis + numerics, no certificate | EXCLUSION |
> | arXiv:1908.09385 (J. Chen) | dissipative gCLM, analytic (checked leg 45: no computer assistance) | EXCLUSION |
> | arXiv:2210.07191 + 2305.05660 (Chen–Hou) | certified blow-up, **inviscid** — no dissipation dial | EXCLUSION |
> | arXiv:2509.14185 | unstable singularities at CAP-ready precision, inviscid, no certificate claimed | EXCLUSION |
>
> **Re-derived, not asserted:** their published `(μ, κ)` reproduce to **1.8e−07** (j=1 rows,
> two cases, four rows in all), their Fig. 1a branch to **max 3.0e−06 / rms 1.9e−06**, and
> their fold to **3.8e−07** in `ε*`. Their figure is a *vector* graphic, so the curve was
> read out of the PDF as coordinates and calibrated on the axis ticks; the calibration
> self-checks against Table 1 (a different page) to **1.0e−05**.
>
> **What their answer says, which is what stage V wanted to find out:** the margin does
> **not** die when dissipation is switched on — the conditioning *improves* 26× — and then
> diverges at a **fold** in the dissipation parameter, with exponent **−1.061** against −1
> for an ordinary quadratic fold. Rigorous branch verification must stop at or before the
> fold, which is why their Case II verifies only parts of its branches.
>
> **The hole, recorded as a hole:** twelve arXiv queries are logged in `SEARCH_LOG`; the
> four asking for the FLUID version — an inviscid Euler/Boussinesq/CLM blow-up certified
> under a viscosity dial — return nothing. That is a smaller question than the one stage V
> posed, and re-labelling one as the other after seeing the answer is the move that cost
> leg 42 seven claims.


> ## 🧭 SEVENTH PASS (leg 45, Route-M): the check turned OUTWARD — what is already PROVED
>
> The sixth pass below asks *"has anyone pre-empted our answers?"* Route-M asks the
> complementary question — *"has anyone already proved the thing we are trying to
> certify?"* — and the answer for the port's target was **yes, by its own authors, in
> 2022.** That ledger lives in `solver/target_selection.py::CERTIFICATION_RECORD` and
> `TARGET_LEDGER`, gated by `test_target_selection.py` (9/9). Summary:
>
> | object | proved? | how |
> |---|---|---|
> | 2D Boussinesq / 3D Euler w/ boundary (Chen–Hou) — **the port's old target** | **YES** | CAP, arXiv:2210.07191 + Part II |
> | 1D Hou–Luo, odd non-degenerate profile | **YES, TWICE** | CAP (CHH, Ann. PDE 2022) **and analytically** (arXiv:2308.01528) |
> | De Gregorio (gCLM `a=1`) | **YES** | CAP, CHH, CPAM 2021 |
> | **gCLM smooth self-similar profiles, ALL `a ≤ 1`** | **YES** | **analytic**, arXiv:2305.05895 — closes the whole smooth branch Routes D/E/F measured |
> | dissipative gCLM near `a = 1/2` | **YES** | analytic, arXiv:1908.09385 Thm 1.1 — no computer assistance |
> | 3D axisym. Euler, `C^{1,α}` | **YES** | analytic, Elgindi, Ann. of Math. 2021 |
> | 1D Hou–Luo singular steady state — *existence* | **YES** (weak sense) | arXiv:2604.01868 Thm 2.3; **its STABILITY is Conj 2.4, open** |
> | **1D Hou–Luo NON-SYMMETRIC regular profile** | **NO** | arXiv:2604.01868 §4, numerical, Apr 2026 — **Route-M's named target** |
> | **gCLM one-scale from degenerate data, `a>0`** | **NO** | arXiv:2603.25104 §4, numerical, Mar 2026 |
> | **2D Boussinesq non-symmetric profile** | **NO** | arXiv:2604.01868 §6.2, numerical |
> | 3D Navier–Stokes, backward self-similar profile | **claimed, unusable** | arXiv:2604.09949 — see below |
>
> **Tier 2 is now read for what it gates.** `2302.12877` (Cadiot–Lessard–Nave) is the
> completed unbounded-domain certificate this project's algebra is now checked against
> (their Kawahara `r₀` reproduced exactly); they work in **Hilbert/Fourier `H^l` spaces**,
> not weighted `ℓ¹`, so Route-D's weighted-`ℓ¹` no-go and discrete-ball trap are **still
> unsearched at primary source** — narrowed, not closed.
>
> **On arXiv:2604.09949 (3D Navier–Stokes).** Its scalar Newton–Kantorovich closure was
> recomputed both as printed (`2δMK = 8.9e−5`) and in the form the theorem requires
> (`2M²Kδ = 4.3e−2`); **both close**, and its `K` reproduces from its own stated factors
> to 2.2e−4. The arithmetic is not where it fails. It is recorded as unusable because no
> verification package is released — its appendix F says the reproducibility package "is
> intended to contain" its contents — and because the exactly-self-similar backward ansatz
> its Thm 12.1 reconstructs is the one excluded by Nečas–Růžička–Šverák and Tsai under the
> decay its own analytic weight implies. Its reference list cites Jia–Šverák on **forward**
> self-similar solutions and neither non-existence result.

> ## ✅ UNBLOCKED, AND DONE. THE FIVE PASSES BELOW ARE SUPERSEDED WHERE THEY CONFLICT.
>
> Egress to `arxiv.org`, `export.arxiv.org` and `api.semanticscholar.org` **works as of
> 2026-08-04**. `bash Papers/fetch.sh` pulled **all fourteen** manifest entries on the
> first attempt, no failures. Tier 1 is **read**. Everything below the sixth-pass section
> was written without opening a paper; where it disagrees with this section, **this
> section wins**.
>
> **The check is now CODE, not prose:** `solver/literature_gates.py` +
> `test_literature_gates.py` (9/9) re-derive each published number from the published
> equations and compare it to ours. See `writeup/4_p2_lottery/TECHNICAL_P2_ROUTEJ_V1.md`
> and `writeup/data/p2_route_j_v1_literature.json` (fig39).

## The verdict, in one table

Twelve standing claims. **Seven pre-empted, one partial, two still unsearched, one
confirmed-and-always-cited, and one result arriving FROM the literature.**

| claim | leg | source | verdict |
|---|---|---|---|
| `s_c = α/2` | Route-F v1 | **XU §6.1 eq (6.3)** | **PRE-EMPTED** |
| isolated eigenvalues are only symmetry modes | Route-E v1 | XU Thm 2 | confirmed & pre-empted |
| the non-symmetry spectrum is a continuum | Route-E v1, inherited by Route-I | **XU Prop 2** | **pre-empted AND re-classified** |
| `α(1/2) = 3` and the odd-integer resonances | Route-E v1 | ALS §5.2 + §1 | confirmed & pre-empted |
| the `α(a)` branch and `a_c ≈ 0.694` | Route-E v1 | XU Table 1; LSS `a_c = 0.6890665` | **PRE-EMPTED** |
| the closed form (E) | Route-H v1 | **ALS §5.3 eqs (57)-(58)** | **PRE-EMPTED** |
| `α₁ = 0` at `a = 0` (a line of viscous blow-ups) | Route-H v1 | ALS §5.3 eq (61) | confirmed & pre-empted |
| `α₁ = +0.133683` at `a = 1/2` | Route-H v1 | not in Tier 1 | unsearched |
| finite support, `X_c` = zero of `c + aU`, order `1/a` | Route-D v12/v13 | HTW Prop 2.3 | **PARTIAL** (they do `a = 1` only) |
| `β = 2.92` (2D Boussinesq anchor) | Route-G v1 | CH | confirmed; always cited |
| discrete-ball trap, weighted-`ℓ¹` no-go, elasticity | Route-D v3/v6 | 2302.12877 — **fetched, NOT read** | unsearched |
| **what happens ABOVE `s_c`** | none | ALS §5.1 | **inbound: they answer US** |

## The four sources

**ALS = arXiv:2207.07548** — Ambrose, Lushnikov, Siegel, Silantyev, Nonlinearity (2022).
**XU = arXiv:2607.19762** — Xu, 22 Jul 2026. **CH = arXiv:2210.07191** — Chen & Hou.
**HTW = arXiv:2209.08232** — Huang, Tong, Wei.

**The exponent dictionary, which every comparison depends on.** ALS/XU write
`ω ~ τ^{-β} f(x/τ^{c_l})`, so **their `c_l` is our `β`** and **our `α = 1/c_l`**; their
`Λ^σ` is our `(-Δ)^s` with **`σ = 2s`**. Hence `s_c(ours) = α/2 = s*(XU)/2`. Get this
wrong and every verdict here inverts while still looking consistent.

## What the sixth pass established, with the numbers

**1. `s_c = α/2` IS in the literature, and NOT where the fifth pass guessed.** The fifth
pass named `arXiv:2207.07548` as "the paper most likely to pre-empt Route-F" and said to
read it first. **That was wrong.** ALS §8 explicitly leaves the critical-σ question OPEN
("whether σ = 1 is the optimal lower bound ... left for future work"). The relation is
**XU §6.1 eq (6.3): `s*(a) = 1/c_l(a)`**, derived from exactly our rescaling argument
(dissipation enters with coefficient `e^{-γτ}`, `γ = 1 - s c_l`), **posted 22 Jul 2026 —
eleven days before Route-F v1**. Our `F6` map against XU Table 1: worst row **3.1e-3**,
mean **1.2e-3**, exact at `a = 0` and `a = 1/2`. XU state the same caveat we did — `s*` is
a formal relevance threshold, **not** the sharp blow-up/regularity curve, "which for this
family remains unknown".

**2. Route-H's (E) is ALS (57)-(58), verified pointwise.** Parameter map
`ω₋₁(0) = -(1+μ₀)κ`, `v_c(0) = κT` with `κ = ν/μ₀`. Three parameter sets × four times:
worst relative difference **6.5e-15**. ALS's blow-up-time formula (59) returns our `T`
with absolute error **0.0**. Their evolution law `dv_c/dt = ω₋₁(0)+ν` reduces to `-κ`,
which is (E)'s own. Route-H declined to claim it; that was right.

**3. `α(1/2) = 3` is EXACT and known — and this CLOSES Route-E's open question.**
Integrating ALS (49)-(50) cold (no shared grid, basis or code with our Newton solve):
`c_l = 0.3333076` vs `1/3`, **rel 7.7e-5**, with `Ω ~ v_c^{-2.000144}` vs the exact `-2`.
Route-E asked why `α = 3` is a round rational while `α = 5` is not. **ALS §1 answers it:
exact pole-dynamics solutions exist at `a = 0` and `a = 1/2` and, per Lushnikov et al.,
NOWHERE ELSE.** The `α = 5` "resonance" at `a = 0.5821792673` is a property of our
instrument (`Λ⁵` is a finite matrix there), not of the problem.

**4. THE RE-CLASSIFICATION WITH THE LARGEST FORWARD CONSEQUENCE — XU Proposition 2, the
realization dichotomy.** The essential-spectrum continuum Route-E measured is the faithful
spectrum of the **maximal `L²` realization**; on the **origin-`H²`** realization the open
strip is empty apart from `{0,1}`. XU say in as many words that the smear which grids
**without an origin condition** place inside the strip is that maximal realization's
spectrum. **Our discretization has no origin condition.** So "the non-symmetry spectrum is
continuous" is a statement about which operator we discretized, not about the operator.
The DSS conclusion survives (nothing to bifurcate in either realization) — but
**Route-I's "141 of 144 unstable directions at `μ = 0`" is counted in the loose
realization and must say so.** Top-ranked correction item.

**5. The one result arriving FROM the literature: what lies ABOVE `s_c`.** Routes F/H/I
all stop at criticality. ALS §5.1 (Schochet, corrected) supplies the other side:
supercritically the balance is **dissipation against stretching**, `β = σ c_l`, with
**`ω_t` subdominant**, and the mechanism is a **double pole with residue `B = -12iν`** —
proportional to `ν`, absent inviscidly. Measured here, not quoted: rescaling on a
τ-ladder, spread `0.0202` at `β = 2` vs `0.990` at `β = 1` (**49×**), and the `β = 2`
residual **falls** `0.0202 → 0.0060 → 0.00187` on deeper sub-ladders, which is ALS's stated
`O(τ^{-1})` correction behaving as stated.

**6. A 38-year-old typo, settled from our side.** ALS §5.1 correct Schochet (CPAM 1986)'s
constant to `K± = 24(3±√6)` from the printed `12(6±√6)`. Substituting both into the
complex Burgers equation with analytic derivatives: corrected **5.24e-16 / 2.85e-16**,
printed **2.40e-2 / 8.36e-2**. **13.66 decades.** ALS are right. Schochet CPAM 1986 is
still not obtainable (publisher PDF), but its content is now pinned through ALS — and the
constant one would have copied from it is the wrong one.

**7. Finite support is PARTIAL, not pre-empted.** HTW Prop 2.3 proves compact support for
the **De Gregorio model, `a = 1`**, where non-degeneracy forces `c_l = c_ω`. Same
mechanism as ours (the profile is locally `∝ u + c_ω x`; support ends where that
vanishes). **Not** in HTW: the `a`-dependence across `a ∈ (0, 1/2)` and the algebraic order
`1/a` of the zero — nor the certification-space consequence we actually used it for.

**8. On `a_c` we are the worst of three sources.** Published (LSS) **0.6890665**; XU's
recompute **0.6888** (0.04% off); ours **0.693493** (**0.64%** off). Quote theirs. There is
a gate asserting this, which will fail if we ever become the better source.

## What is still NOT checked, and it is the part that matters

**Tier 2 is fetched and text-extracted but NOT read closely** — `2302.12877`
(radii-polynomial methodology), `2312.01702` (log-lattice singularity tracking),
`1908.09385` (J. Chen, dissipative gCLM). Those gate the **Route-D methodological claims
(the discrete-ball trap, the weighted-`ℓ¹` conservation no-go, the elasticity discipline)
— still the only claims in this project with a real chance of being new.** After this
pass, "unchecked" means unchecked; it does not mean "probably fine". Reading Tier 2 is now
cheap and is the obvious next literature action.

Also still unobtainable and still only context: **Schochet CPAM 1986** (publisher PDF),
**Nečas–Růžička–Šverák**, **Jia–Šverák**.

---
---

# Literature check — first pass (2026-08-02)

> **⛔ NETWORK DIAGNOSIS CORRECTED 2026-08-03 — AND IT IS FIXABLE.** Earlier passes recorded
> the blocker as "a tool-level `WebFetch` block, not an allowlist question". **That was
> wrong.** Measured: the agent proxy returns **403 to the CONNECT** for non-allowlisted
> hosts. `github.com` is allowlisted and returns a real HTTP response; `arxiv.org`,
> `en.wikipedia.org` and `api.semanticscholar.org` are refused. `WebFetch` 403s for the
> same reason — it is not a separate bug. **This is the environment's egress policy and
> the user can change it.** Run `bash Papers/fetch.sh`; if it reports BLOCKED, ask the user
> to allowlist the hosts it names. See DIRECTIVE 1 in `CONTINUATION_PROMPT.md` and
> `Papers/MANIFEST.md` for what to read first and what each paper gates.
>
> **Everything below this line is still search-level. Zero papers have been read.**

**Status: PARTIALLY UNBLOCKED.** This had been open four legs and blocked on
"arxiv + publishers 403 at the proxy". The precise diagnosis is now known and is
narrower than that:

- **`WebFetch` is blocked for EVERY host, not just academic ones.** It returns
  403 on `arxiv.org/abs`, `arxiv.org/html`, `alphaxiv.org`, a plain
  `kurims.kyoto-u.ac.jp` PDF — **and on `en.wikipedia.org`**. That last one is the
  tell: this is not a publisher/paywall problem and not an arXiv problem, so
  "allowlist arxiv.org" would NOT have fixed it. Do not spend time re-diagnosing
  it as one.
- Direct `curl` egress is a separate, narrower allowlist: `export.arxiv.org`
  returns *"Host not in allowlist ... Add this host to your network egress
  settings"*, and `api.semanticscholar.org` fails CONNECT with 403.
- **`WebSearch` works**, and its backend *can* read those pages. It is currently
  **the only literature channel available**. So a first-pass check is possible
  today; full-text verification is not, by any route tried.

**Therefore every finding below is SEARCH-LEVEL and unverified against a primary
source.** Search summarisers paraphrase, blend sources, and occasionally echo the
query back. Nothing here should be quoted as established until someone reads the
actual paper. What it is good for is telling us *where to look* and *which of our
claims are now at risk* — which is exactly what a novelty check is for.

**To finish the job, TWO things are needed and they are different:** (i) restore
`WebFetch` (it is 403 on all hosts including Wikipedia — an environment/tool-level
block, not a domain question); and (ii) for direct `curl`, add `arxiv.org`,
`export.arxiv.org`, `api.semanticscholar.org`, `link.springer.com`,
`aimsciences.org` to the egress allowlist. Either one alone would unblock
full-text verification, which gates every novelty claim this project might make.

---

## Findings that put our claims AT RISK

### 1. Finite support of the a > 0 profiles (v12/v13) — likely KNOWN

Search reports, for the De Gregorio model, that *"self-similar profiles of the De
Gregorio model must be compactly supported"* and that the model *"admits
infinitely many compactly supported, self-similar solutions"*
([arXiv:2209.08232](https://arxiv.org/pdf/2209.08232), *On self-similar
finite-time blowups of the De Gregorio model on the real line*).

**Risk: HIGH.** v12/v13 treated the finite support (the profile ending at `X_c`)
as a discovery. If the above is what it appears to be, the *phenomenon* is known
for the a = 1 endpoint at least. What may still be ours: the explicit
`X_c = ` the zero of `c + aU`, the algebraic order `1/a` of the zero, and the
consequences for the certification space. Those are narrower claims than "the
profile ends".

### 2. The spectral picture / eigenvalues {0, 1} (Route-E v1) — likely PRE-EMPTED

[arXiv:2607.19762](https://arxiv.org/abs/2607.19762), *The spectral picture of
self-similar collapse in the Constantin–Lax–Majda equation* (submitted
**22 July 2026**, 41 pp) is reported to linearise about the exact CLM profile
`Ω(y) = −y/(y² + 1/4)` — **our `clm_one_scale` normalisation** — and to find the
**full point spectrum is exactly {0, 1}, the scaling and time-shift symmetry
modes, with no embedded eigenvalues**, leaving a spectral gap of 1/2.

**Risk: HIGH, and note the direction — this is good news for correctness.**
Route-E v1's Hopf-bifurcation negative found *"the only grid-converged isolated
eigenvalues are 0 and −1, the two exact symmetry modes"*. That agrees (sign
convention aside) with a rigorous, contemporaneous result. Our leg is therefore
**confirmed but not novel**, and the paper is 41 pages of rigour where we had a
dense eigenvalue solve.

### 3. Route-F v1's `s_c = α/2` — POSSIBLY KNOWN, and this one matters most

The first search returned: *"For a > 0, there is a formal scaling-relevance
exponent `s*(a) = 1/c_l(a)`, below which fractional dissipation is asymptotically
subdominant in self-similar variables for fixed sufficiently regular data."*

Route-F v1 derived `β = 1/α` and `s_c(a) = α(a)/2`. If `c_l = 2β` in the source's
convention, then `s*(a) = 1/c_l = 1/(2β) = α/2 = s_c` — **the same statement**.

**Risk: HIGH but UNCONFIRMED.** I could not attribute this sentence to a specific
paper: the second search's summary of 2607.19762 did not mention fractional
dissipation at all, so the first summary may have blended sources. **This is the
single most important thing to verify with a primary source**, because it is the
headline of the newest leg.

### 4. Travelling waves "for any a > 0" — challenges our a\* ≈ 0.5–0.55

Search reports that *"Okamoto et al provided numerical evidences for the
existence of non-trivial steady and travelling-wave solutions for any a > 0"*
([Okamoto–Sakajo–Wunsch](https://www.kurims.kyoto-u.ac.jp/~okamoto/paper/non273004p15.pdf);
[Steady-states and traveling-wave solutions of the gCLM equation](https://www.aimsciences.org//article/doi/10.3934/dcds.2014.34.3155)).

**Risk: MEDIUM, and needs care rather than alarm.** Our `a* ≈ 0.5–0.55` is about
a *specific* object — HQW25's **two-scale** (inner, moving-frame) traveling wave —
not about steady/travelling waves of gCLM generally. These may simply be different
objects. But we have confirmed that boundary four times and called it a property of
the model; if OSW find travelling waves throughout `a > 0`, then at minimum the
claim needs restating to say precisely *which* object stops existing.

## Context worth having (not a risk, just orientation)

- `a_c = 0.6890665337007457…`, a critical value for self-similar collapse, is
  Lushnikov–Silantyev–Siegel ([arXiv:2010.01201](https://arxiv.org/pdf/2010.01201)).
  **Different quantity from our `a*`** — do not conflate them.
- Blow-up proved for `a < −1`; global existence for `−1 ≤ a < 1`; the
  advection/stretching transition at `a = 1` (De Gregorio).
- gCLM with dissipation, singularity formation and global well-posedness:
  [arXiv:1908.09385](https://arxiv.org/abs/1908.09385).
- Smooth self-similar profiles for `a ≤ 1`:
  [arXiv:2305.05895](https://arxiv.org/pdf/2305.05895).
- Our own anchor paper HQW25 = [arXiv:2401.14615](https://arxiv.org/pdf/2401.14615).

## Third pass — the dissipation results, and one contamination check (2026-08-02)

### A contamination hypothesis, tested and RULED OUT

The quoted sentence *"`s*(a) = 1/c_l(a)`"* uses `c_l` — **this project's own
notation** — which raised the possibility that the search backend had indexed
**our repo** and was feeding our own claims back as "literature". Tested by
searching for distinctive repo strings (`blowup-search`, `ravanova`, `Route-D`
+ `radii polynomial`): **no hits, the repo is not indexed.** The coincidence is
innocent — `c_l` is the field's own notation for the focusing exponent
(Lushnikov–Silantyev–Siegel), which this project adopted. Hypothesis closed, but
worth re-running if we ever make the repo public.

### The paper that most likely pre-empts Route-F — read this one FIRST

[arXiv:2207.07548](https://arxiv.org/abs/2207.07548) / [Nonlinearity
(IOP)](https://iopscience.iop.org/article/10.1088/1361-6544/ad140c), *Global
existence and singularity formation for the generalized Constantin–Lax–Majda
equation with dissipation: the real line vs. periodic domains*.

Search reports it studies gCLM with dissipation `−Λ^σ` and:

- proves **global existence for `σ ≥ 1`, all real `a`, small data** (periodic);
- **derives new analytical solutions on the REAL LINE at `a = 1/2`** for various
  `σ`, exhibiting self-similar finite-time singularity formation, **with the
  similarity exponents and the conditions for singularity formation FULLY
  CHARACTERIZED**;
- reinterprets Schochet's `a = 0, σ = 2` solution as self-similar collapse.

**This raises the risk on TWO of our claims at once:**

1. **Route-F v1's `s_c(a) = α/2`** — a paper that "fully characterizes the
   conditions for singularity formation" in terms of `σ` for this exact model is
   the natural home for a dissipation-relevance threshold. **Risk: HIGH.**
2. **`α(1/2) = 3`** — flagged in the continuation prompt as a novelty claim.
   `a = 1/2` on the real line is *precisely* where this paper reports exact
   analytical solutions with fully characterized exponents. **Risk: HIGH**, and
   this one may be checkable by direct comparison of exponents once readable.

Also relevant and unread: [arXiv:1908.09385](https://arxiv.org/abs/1908.09385),
*Singularity formation and global well-posedness for the gCLM equation with
dissipation*.

### Revised reading order once full text is available

1. arXiv:2207.07548 — gates Route-F v1 **and** `α(1/2)=3`. Highest value.
2. arXiv:2607.19762 — gates Route-E v1 (already looks pre-empted).
3. arXiv:2209.08232 — gates the finite-support finding of v12/v13.
4. arXiv:2302.12877 — gates the methodological candidates (v3 no-go, v6 trap).
5. Okamoto–Sakajo–Wunsch — restates rather than refutes `a*`.

## Second pass — the methodological candidates (searched 2026-08-02)

Searched; **no direct hit for any of the three**. That is weak evidence of
novelty, not strong: a search that fails to find something is mostly evidence
about the search terms. But the *shape* of what came back is informative.

**What the standard literature does.** The radii-polynomial method
(van den Berg–Lessard and successors) is well established, and the recurring
setting is a **weighted ℓ¹ Banach space of Fourier coefficients with GEOMETRIC
decay** — weight `ν > 1`, which forces **analytic** regularity, typically on a
periodic or bounded domain. Representative:
[Rigorous numerics for ill-posed PDEs: periodic orbits in the Boussinesq
equation](https://arxiv.org/abs/1509.08648);
[Automatic differentiation for Fourier series and the radii polynomial
approach](https://www.sciencedirect.com/science/article/abs/pii/S0167278916000294).

**Why our obstruction may genuinely be off their path.** Our problem has
**algebraic decay on an UNBOUNDED domain**, so the natural weights are
polynomial, not geometric — and geometric weights sidestep the far-field
degeneracy that v2/v3 ran into entirely. If the v3 conservation law is new, this
is the likely reason: the standard setting assumes away the regime where it bites.
That is a defensible claim to make in a writeup, and a cheap one to check.

**The single nearest paper to read** — nobody has yet:
[Rigorous computation of solutions of semi-linear PDEs on unbounded domains via
spectral methods](https://arxiv.org/pdf/2302.12877). Same setting as ours
(unbounded domain, spectral, validated). If the v3 no-go or anything like the
discrete-ball trap is known, it is most likely to be here or in its references.

**Status of each candidate after this pass:**

| candidate | search result | read next |
|---|---|---|
| discrete-ball trap (v6) | no hit | arXiv:2302.12877; then radii-polynomial papers that discretise a *non-analytic* norm |
| weighted-ℓ¹ conservation law / no-go (v3) | no hit; standard work uses `ν>1` geometric weights, which avoids the regime | arXiv:2302.12877 |
| elasticity discipline (v9/v10) | no hit | likely folklore rather than published; low priority |

## The methodological candidates — original notes

These were the strongest novelty candidates and none has been searched:

1. **The discrete-ball trap** (v6) — duality over a discretised Hölder ball is
   unsound; extremizer inflated ~J².
2. **The weighted-ℓ¹ conservation law / no-go** (v3) — the two NK requirements are
   separated by exactly one grading power, and the separation is conserved.
3. **The elasticity discipline** (v9/v10) — sharpen a constant only in proportion
   to its elasticity in the final budget.

My prior is that these are **more likely to be genuinely new than the toy-model
results**, because they are about the *method* of computer-assisted proof rather
than about gCLM — but equally they may be folklore among people who do validated
numerics professionally, in which case they are written down somewhere I have not
looked. Search terms to try: "radii polynomial" + "discrete norm"; "validated
numerics" + "Hölder seminorm" + "duality"; "finite section" + "weighted ell^1" +
"unbounded domain".

## Third pass — Route-G v1's claims (searched 2026-08-02, still `WebSearch`-only)

`WebFetch` is **still 403 on arxiv.org/abs** (re-tested at the start of this leg), so
this pass is the same search-level quality as the ones above: it tells us where to
look, not what is true.

**Searched: the invariant law `s_c = 1/(2β)`.** No hit, in several phrasings. That is
weak evidence at best — the statement is three lines of scaling and is exactly the sort
of thing that lives in a remark rather than a title. My prior is that it is **folklore**:
anyone who has written down a dynamic rescaling has the ingredients. What is worth
claiming is not the formula but the *use* — putting the proven 2D object, the 1D family
and NS on one axis and reading off which side of `β = 1/2` each lands on.

**Nearby literature that did surface, and it matters:** the search returned
*"in hypo-diffusive systems the critical dissipation degree is predicted to be
γ = 1/3"* and a log-lattice paper ([Tracking complex singularities of fluids on
log-lattices](https://arxiv.org/pdf/2312.01702)). The log-lattice programme
(Campolina–Mailybaev and successors) studies exactly this question — where fractional
dissipation kills an Euler-type singularity — on a reduced model. **If the discipline of
"measure the exponent, not the threshold" is written down anywhere, it is most likely
there.** Nobody here has read it.

**TWO PAPERS TO READ FIRST when access is restored — both could move Route-G's number:**

1. [arXiv:2308.01528](https://arxiv.org/pdf/2308.01528), *Exact self-similar finite-time
   blowup of the Hou–Luo model with smooth profiles*. If a related model has an **exact**
   self-similar profile, it has an **exact `β`** — which would turn `s_c = 1/(2β)` from a
   measured number into a closed-form one for that model, and give this leg a
   known-answer gate it currently does not have in 2D.
2. [arXiv:2604.01868](https://arxiv.org/pdf/2604.01868), *Novel Self-similar Finite-time
   Blowups with Singular Profiles of the 1D Hou–Luo Model and the 2D Boussinesq
   Equations* (2026). **NEW self-similar solutions with different profiles means
   different `c_l`, `c_ω`, hence different `β`.** Route-G quotes `β = 2.92` as if the 2D
   scenario has one collapse rate. If this paper exhibits others, the honest statement
   becomes "the Chen–Hou branch sits at `β = 2.92`" and the map needs more than one point
   on it.

Also relevant to the *scope* sentence rather than the number: the Chen–Hou result is
reported to control the density in `C^γ` with **γ ≈ 1/3** up to the singular time. That is
a regularity exponent, not a dissipation exponent — **do not conflate it with `s_c`**, and
note that `0.171` and `1/3` are close enough to invite exactly that error.

## Fourth pass — Route-H v1's claims (NOT searched; recorded as unchecked, 2026-08-03)

**Nothing here has been searched.** `WebFetch` remains 403 on every host and this pass
was written from what the leg's own construction implies about its risk, not from a
query. It is a to-do list, not a finding, and it is filed so the next session does not
have to reconstruct it.

**AT HIGH RISK — presume known.**

1. **The closed-form viscous CLM blow-up (E).** Explicit solutions of the *viscous* CLM
   equation by complexification (`z = H(ω) + iω`, `Λz = i z_x`, reducing to a complex
   Burgers equation with constant complex characteristics) go back to **Schochet, CPAM
   1986**. The leg does not claim it and uses it only as a known-answer gate — which is
   the right use for something at this risk level, and the writeups say so.
2. **`λ_μ = 2s − α₀`.** This is Route-F's `s_c = α/2` in spectral clothing: the same
   number, re-derived as a stability exponent instead of fitted from a trajectory.
   Route-F's claim is already the one at "serious risk" in the summary below —
   arXiv:2207.07548 is flagged as the paper most likely to pre-empt it — so **Route-H
   inherits that risk in full**. Reading 2207.07548 settles both at once, which raises
   its priority rather than adding a new item.

**METHODOLOGICAL CANDIDATES — unchecked, and the only place novelty plausibly sits.**
These join the three from the second pass (discrete-ball trap, weighted-ℓ¹ no-go,
elasticity discipline) with the same status: no hit is not evidence, because nobody has
searched.

| candidate | why it might be new | why it might not | where to look |
|---|---|---|---|
| **`μ` as an autonomous coordinate of the rescaled flow**, so a scaling threshold becomes a stability eigenvalue | it converts a dimensional-analysis statement into a spectral one, and makes the *marginal* case a normal-form question rather than an empty one | anyone who writes a dynamic rescaling with a dissipative term has `μ_τ = (2s − α)μ` two lines away; this is exactly the kind of thing that is standard and unwritten | the log-lattice programme (Campolina–Mailybaev, arXiv:2312.01702 and successors) — the same "measure the exponent, not the threshold" discipline; and the modulation-equation literature around Merle–Raphaël |
| **`α₁ = dα/dμ` as the marginal invariant**, with its sign the whole verdict | it is a specific, cheap, checkable number attached to a case usually reported as "no information" | it is the leading coefficient of an obvious expansion once the previous row is granted | same |
| **Critical dissipation discretizes the inviscid continuum onto the negative integers without producing anything that could cross** | it is a concrete spectral statement about what a dissipative perturbation does to a continuous spectrum in this class, with a positive control behind it | continuum-to-discrete under a dissipative perturbation is a classical phenomenon; the *content* is the "and nothing crosses", which is a null result about one model | Route-E's own leads on the gCLM spectral picture (already flagged as likely pre-empted), plus standard fractional-dissipation spectral theory |

**The honest ranking:** item 3 is the one worth a specialist's five minutes. Items 1 and
2 should be presumed known until someone checks. **No claim of novelty should be made for
any of them on the strength of this file.**

**Reading order impact:** unchanged at the top — arXiv:2207.07548 is still the first
paper to read, and it now gates three claims (Route-F's `s_c`, Route-H's `λ_μ`, and by
extension the eigenvalue framing) instead of one.


## Fifth pass — Route-I v1's claims (NOT searched; recorded as unchecked, 2026-08-03)

**Nothing here has been searched.** `WebFetch` is still 403 on every host. Same status as
the fourth pass: a to-do list, not a finding.

**INHERITED RISK, unchanged.** Route-I re-measures Route-H's `λ_μ = 2s − α₀` and `α₁`
along a trajectory instead of off a static branch. Different computation, *same claim* —
so it inherits Route-F/H's risk in full, and **arXiv:2207.07548 still gates it.** Reading
that one paper now settles four claims across three legs.

**THE ONE CLAIM THAT IS NEW IN KIND — and the one most likely to be standard.**
"Dissipation regularizes the linearization of a self-similar rescaling": the inviscid
rescaled fixed point has `~K` unstable directions and any `μ > 0` has none, with the
crossover `μ*(K) ~ g/K^p`. My honest prior is that this is **well known in the
parabolic-blowup literature** — the whole modulation-analysis programme (Merle–Raphaël and
successors) works with viscous rescaled operators whose spectrum is discrete, and the
inviscid/essential-spectrum contrast is the reason that programme exists. What may be less
standard is the *specific* observation below.

| candidate | why it might be new | why it might not | where to look |
|---|---|---|---|
| **The unstable inviscid directions ARE the log-periodic band** — `Re` rises with `|Im|`, `max|Im|` grows with `K`, leading eigenvalue `+4.55 + 430i` — **so `μ` deletes exactly the DSS-shaped modes** | it makes "the DSS lane is shut" a statement with a mechanism *and* an obstruction that is the same object in both the inviscid and viscous problems, rather than two separate null results | continuum spectrum of a rescaled hyperbolic operator being log-periodic is Route-E's own (already-at-risk) observation; that dissipation damps high-frequency modes hardest is elementary. The *combination* is the only candidate part | the log-lattice programme (arXiv:2312.01702 and successors); DSS literature for Euler/NS; Route-E's existing leads |
| `μ*(K) ~ g/K^p` **as a non-commuting-limits diagnostic** | it is a cheap, general test for "is my stabilization an artifact of truncation" | almost certainly folklore in spectral-methods practice, just rarely written down | numerical-analysis texts on spectral discretization of stiff operators |

**Do not claim novelty for any of it on the strength of this file.** The methodological
items from passes two and four remain the only plausible candidates, and all remain
unchecked.


## The honest summary

Of four project claims checkable today, **two look pre-empted (finite support,
the spectral picture), one is unconfirmed but at serious risk (`s_c = α/2`), and
one needs restating rather than retracting (`a*`)**. That is a normal outcome for
a first literature pass on a well-studied model, and it is much cheaper to learn
now than after writing anything up. It also sharpens where the remaining value
plausibly sits: **the methodological findings, and the certification machinery** —
not the gCLM phenomenology.


## 🧭 NINTH PASS (LIT, 2026-08-05): the resurfacing flag re-checked, and BDL's
## zero-diagonal question resolved (network + PDF extraction both worked this time)

This pass answers the two open items CONTINUATION_PROMPT.md flagged for a later leg:
Directive 2's search-index flag, and stage T-0's unresolved "does BDL cover a
zero-diagonal Fredholm operator" question. Both are answered plainly below. Network
egress to `arxiv.org` and the `WebSearch`/`WebFetch` tools both worked in this session
(no retries needed); `pdftotext` on `arXiv:1503.06315` also worked this time, unlike
leg 52's attempt.

### Item 1 — does `arXiv:2604.01868` resurface in the search index now?

**No. It still does not resurface under a topical query.** Re-ran leg 52's own logged
query verbatim:

```
"Chen Huang Li 2026 Hou-Luo model non-symmetric self-similar profile blowup proof"
```

(`SEARCH_LOG` entry 5 in `experiments/p2_route_t_v1_border.py:116`, weight 5). Result:
five links returned, all 2021–2023 Hou–Luo/Chen–Hou/Chen–Hou–Huang work
(`arXiv:2308.01528`, `arXiv:2106.05422` ×2, the Caltech mirror of the Annals of PDE
paper, and the Springer landing page). `arXiv:2604.01868` did **not** appear in the
returned links — reproducing leg 52's finding exactly.

A second query naming the exact title and authors (*"arXiv:2604.01868 Chen Huang Li
Novel Self-similar Finite-time Blowups Hou-Luo Boussinesq"*) also did not return
`arXiv:2604.01868` among its **links** — the eight returned links are all other
papers (`2605.15130`, `2403.11471`, `2401.14615`, a ResearchGate De Gregorio page,
`2305.05660`, the CLM Springer page, and one arXiv listing page). The prose summary
that followed *did* correctly name the paper's title and authors — but that is the
underlying model answering from its own knowledge, not from a link the search actually
surfaced, and the same distinction matters for `2604.01868` itself: **direct retrieval
by ID works fine** (`WebFetch` on `arxiv.org/abs/2604.01868` returned the correct
title/abstract instantly, and `scripts/fetch_papers.sh 2604.01868` pulled the 28 MB PDF
without a hitch). The gap is specifically in the **search index's** *topical* recall,
not in the paper's availability or in this project's ability to fetch it once named.

**Plain answer: the flag stands. Re-querying today, by topic, still does not
resurface `arXiv:2604.01868`; fetching it by ID still works perfectly.** This is a
second independent confirmation of leg 52's search-index observation, not a new
finding about the paper.

### Item 2 — does Breden–Desvillettes–Lessard (`arXiv:1503.06315`) cover the
### zero-diagonal Fredholm case?

**No — their construction requires a diagonal bounded away from zero, and a
zero-diagonal operator is outside its stated hypotheses.** The PDF extracted cleanly
this time (`pdftotext`, 3679 lines); the relevant passages:

BDL's tridiagonal operator (their eq. (3)) is `L_k(x) = λ_k x_{k−1} + μ_k x_k + β_k
x_{k+1}`, and their **assumption (4)** (p.3) requires

> "there exist real numbers `s_L > 0`, `0 < C1 ≤ C2` and an integer `k0` such that
> `C1 ≤ μ_k / ω_k^{s_L} ≤ C2` for all `k ≥ k0`"

— i.e. the diagonal `μ_k` must be **bounded below** by `C1 ω_k^{s_L} > 0`; it can
never vanish past `k0`. Their **assumption (5)** then requires the off-diagonal-to-
diagonal ratios `λ_k/μ_k, β_k/μ_k ≤ δ < 1/2` — a ratio that is undefined at `μ_k = 0`.
Both hypotheses presuppose a **nonzero, dominant** diagonal; "tridiagonal dominant" in
their title is not decoration, it is the operating assumption their whole pseudo-
inverse construction (an LU-decomposition, their eq. (6)–(8), citing Ciarlet Thm
4.3-2) is built on — the algorithm literally divides by `μ_k` (`b_1 = μ_m, b_2 =
μ_{m+1}, ...` feeding the LU recursion).

Two further checks that this isn't just an unstated gap: (i) their own §5
"Conclusion and Perspectives" (p.25) lists three explicit future directions —
relaxing assumption (5)'s *symmetric ratio* restriction, adapting to `ℓ¹_ν`, and
generalizing to block-tridiagonal structures — and **none of the three is "extend to
a zero or vanishing diagonal."** A zero diagonal is not on their own list of
acknowledged limitations to lift. (ii) The words "Fredholm" and "kernel" do not occur
anywhere in the paper (`grep -i "fredholm\|kernel" ` on the extracted text returns
nothing) — the possibility of a non-injective / non-surjective linear part with a
genuine kernel/cokernel is not part of their framework at all, consistent with a
construction that assumes the diagonal already dominates and never needs a null-space
correction.

**Plain answer: BDL's method does not extend to, and does not cover, a zero-diagonal
Fredholm operator.** It is a different regime from what they built: their pseudo-
inverse is a perturbation of a dominant diagonal, and leg 51/T-0's problem has no
diagonal to perturb. This narrows T-0's `PROCEED_NARROW` verdict further, in the
direction it already pointed — leg 51/T-0's zero-diagonal Fredholm case is not
resolved by BDL and, on this reading of their construction, cannot be reached by it
without new work (their own listed future directions don't include it). It does not
by itself establish that the zero-diagonal case is *novel* in the wider literature —
only that this one adjacent paper, read in full, doesn't cover it.

**Sources used this pass:** `scripts/fetch_papers.sh` (arxiv.org egress, worked
first try), direct `curl` of `arxiv.org/pdf/1503.06315` (HTTP 200), `pdftotext` on
both PDFs, `WebSearch` (two queries, logged above), `WebFetch` on
`arxiv.org/abs/2604.01868`.

---

## Route-TC pass (leg 53, 2026-08-05) — run BEFORE the construction, verdict `PROCEED_NARROW`

> **CORRECTED AFTER REVIEW.** This section originally reported leg 52's search-index flag as
> **CLEARED**. **That clearance is WITHDRAWN.** VERIFIER adjudicated the conflict with LIT's
> ninth pass (above) in LIT's favour and the flag **stands** — see "the flag, withdrawn"
> below. Nothing else in this section changed.

**Query log (WebSearch/WebFetch, in session, six queries).** Committed verbatim in
`experiments/p2_route_tc_v1_assemble.py::SEARCH_LOG` and in `T0_novelty` of
`writeup/data/p2_route_tc_v1_assemble.json`, so the search is auditable rather than
remembered (leg 42's failure mode was an *unrecorded* search). **The log records query
strings and result COUNTS only, not the returned links** — which is the reason the
adjudication below went against this pass, and a later pass should enumerate links the way
LIT's ninth pass does.

1. `radii polynomial validated numerics coupling between finite block and tail unbounded off-diagonal operator approximate inverse block splitting` — 10 results
2. `computer-assisted proof self-similar profile far-field amplitude as unknown matching condition asymptotic expansion spectral series bordered system` — 9
3. `validated numerics sequence space tail estimate first-order transport operator no diagonal decay coupling term grows with truncation mode certificate fails` — 7
4. `arXiv 2604.01868 Chen Huang Li non-symmetric self-similar blowup Hou-Luo model 2026` — 9
5. `Breden Desvillettes Lessard tridiagonal dominant linear part approximate inverse construction requires diagonal dominance zero diagonal Fredholm kernel` — 10
6. WebFetch `aimsciences.org/article/doi/10.3934/dcds.2015.35.4765` — the hypothesis on the linear part

**Ledger.**

| ref | verdict |
|---|---|
| **arXiv:1503.06315** (Breden-Desvillettes-Lessard, DCDS-A 35(10) 4765-4789) | NARROWS, DOES NOT PRE-EMPT - **and SUPERSEDED by LIT's ninth pass, which read the full text** |
| **arXiv:2604.01868** (Bojin Chen, De Huang, Xiangyuan Li, April 2026) | ~~FLAG CLEARED~~ -> **CLEARANCE WITHDRAWN; the flag STANDS** |
| arXiv:2406.16597 / CPA (2026), self-similar blowup for cubic NLS | CONFIRMS BORDERING IS STANDARD |
| SIADS doi:10.1137/23M1607507, semilinear PDEs on unbounded domains, spectral | ADJACENT (SEMILINEAR ONLY) |

**THE FLAG, WITHDRAWN.** This pass reported the flag cleared because query 4 returned a
summary naming the paper's title and author list correctly. **That is not a test of the flag
as posed, and it is not probative.**

* The flag was raised against leg 52's *logged* query, which names authors and topic and
  **contains no arXiv identifier**. Query 4 above prepends the literal string
  `arXiv 2604.01868`. A query carrying the ID tests retrieval by ID, which was never in
  dispute - LIT confirms `WebFetch` on `arxiv.org/abs/2604.01868` and
  `scripts/fetch_papers.sh 2604.01868` both work first try. **This pass never ran leg 52's
  query.** LIT did, verbatim, and reproduced the null result.
* The evidence relied on - the prose summary naming the title and authors - is exactly the
  signal LIT demonstrated is **not** probative: LIT ran an essentially identical ID-bearing
  query, enumerated the eight returned **links** (all other papers), and identified the
  correct prose as the model answering from its own knowledge rather than from a surfaced
  link.
* This pass logged counts, not links, so its clearance could not be checked against the
  record it left. LIT's could.

**Plain statement, replacing the clearance:** *a query naming the arXiv identifier returns a
summary that correctly names the paper; the flag was about topical recall **without** the
identifier; LIT re-ran that query verbatim and it still does not resurface; and fetching by
ID has always worked.* **The flag stands as LIT reported it.**

**BDL: this pass is superseded, in the direction it pointed.** It read the *publisher's
abstract page* only and recorded that the stated hypothesis is a tridiagonal **dominant**
linear part, that our zero diagonal does not satisfy it, and that this was **evidence, not
proof**, with the flag left up. LIT's ninth pass then extracted the full PDF and settled it:
assumption (4) requires `C1 <= mu_k/omega_k^{s_L} <= C2` with `C1 > 0`, assumption (5)'s
ratios are undefined at `mu_k = 0`, the LU construction divides by `mu_k`, and their own
future-work list does not include a vanishing diagonal. **Read LIT's item 2, not this entry.**

**Novelty claimed by leg 53: none, beyond the negative measurement itself.** Bordering a
certificate to kill a symmetry-induced kernel is standard practice (the NLS entry above does
exactly that) and **no novelty is claimed for the move.** What leg 53 measured is what happens
when the kernel is the far field of an unbounded *off-diagonal* operator, so that the border
acquires a block-coupling term: with the block-diagonal approximate inverse the method
requires, `Z_1[Gamma<-tail] >= 43.15` at the best split in the whole sweep. Whether *that*
observation is in the literature was **not** settled by these six queries - no result addressed
an unbounded off-diagonal part - and it is recorded as **unchecked**, not as new.

## Legs 54-57 novelty passes (2026-08-05)

Links, not counts -- see `writeup/novelty/leg_54.md` through `leg_57.md` for the full logs.

**Leg 57 (Route-XS) closes the BDL question this file's previous entry left open.**
BDL's construction does NOT cover MM's zero-diagonal case (confirmed independently by a
second pass, tracing assumptions (4)-(5) to the source PDF). But leg 57 recommends NOT
lifting the "re-claiming leg 51's finding at full strength" ban anyway: Cadiot
arXiv:2505.03091 sec 2/3 independently states the same dominance-hypothesis observation,
so a different and stronger reason to keep the ban replaces the BDL-shaped one that just
closed. Leg 57 also classified BDL's approximate inverse as the published precedent for
MM's non-block-diagonal move (an LU of the tridiagonal tail), needing a diagonal bounded
below -- precedent, not proof that MM's construction would work.

Leg 54 (MM) ran its own novelty pass first (PROCEED_NARROW); leg 55 (NB) and leg 56 (TN)
likewise (PROCEED / PROCEED_NARROW). Nothing else banked as novel this cycle.
