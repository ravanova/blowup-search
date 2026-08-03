# Literature check — first pass (2026-08-02)

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


## The honest summary

Of four project claims checkable today, **two look pre-empted (finite support,
the spectral picture), one is unconfirmed but at serious risk (`s_c = α/2`), and
one needs restating rather than retracting (`a*`)**. That is a normal outcome for
a first literature pass on a well-studied model, and it is much cheaper to learn
now than after writing anything up. It also sharpens where the remaining value
plausibly sits: **the methodological findings, and the certification machinery** —
not the gCLM phenomenology.
