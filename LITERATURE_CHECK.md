# Literature check — first pass (2026-08-02)

**Status: PARTIALLY UNBLOCKED.** This had been open four legs and blocked on
"arxiv + publishers 403 at the proxy". The precise diagnosis is now known and is
narrower than that:

- The environment's egress is an **allowlist**, not a broken proxy.
  `export.arxiv.org` returns *"Host not in allowlist ... Add this host to your
  network egress settings"*; `api.semanticscholar.org` fails CONNECT with 403.
- `WebFetch` on `arxiv.org/abs/...`, `arxiv.org/html/...` and `alphaxiv.org`
  all return **403**.
- **`WebSearch` works**, and its backend *can* read those pages. So a first-pass
  check is possible today; full-text verification is not.

**Therefore every finding below is SEARCH-LEVEL and unverified against a primary
source.** Search summarisers paraphrase, blend sources, and occasionally echo the
query back. Nothing here should be quoted as established until someone reads the
actual paper. What it is good for is telling us *where to look* and *which of our
claims are now at risk* — which is exactly what a novelty check is for.

**To finish the job, add to the environment's egress allowlist:** `arxiv.org`,
`export.arxiv.org`, `api.semanticscholar.org`, `link.springer.com`,
`aimsciences.org`. That is the cheapest unblocking act available and it gates
every novelty claim this project might make.

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

## The honest summary

Of four project claims checkable today, **two look pre-empted (finite support,
the spectral picture), one is unconfirmed but at serious risk (`s_c = α/2`), and
one needs restating rather than retracting (`a*`)**. That is a normal outcome for
a first literature pass on a well-studied model, and it is much cheaper to learn
now than after writing anything up. It also sharpens where the remaining value
plausibly sits: **the methodological findings, and the certification machinery** —
not the gCLM phenomenology.
