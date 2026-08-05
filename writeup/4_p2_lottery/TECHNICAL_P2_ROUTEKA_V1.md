# Route-KA v1 — the interval pipeline against a PUBLISHED certified radius

**Leg 61. Audit route (not critical path). Gate answered YES, with a measured caveat that
is part of the answer and not a footnote.**
Runner `experiments/p2_route_ka_v1_kawahara.py` · data
`writeup/data/p2_route_ka_v1_kawahara.json` · executable gate
`test_interval_certificate.py` tests (13)–(17) · novelty log `writeup/novelty/leg_61.md` ·
journal `experiments/journal/leg_61.md`. No figure: this is a known-answer audit and the
established convention is that such legs register none.

Every number quoted below is in the curated JSON.

---

## 1. What was missing, stated precisely

Read the `validated` column of `capabilities.py` for the certificate stack. Enclosures contain
exact rationals. Rigorous bounds dominate float readings. A poisoned iterate is rejected at
5.6e+03. Every one of those is **the pipeline agreeing with itself**.

`solver/target_selection.py` looks like the exception — its entry says it "reproduces CLN's
published Kawahara radius exactly". It does not run the certificate. It takes **CLN's** `Y_0`
and **CLN's** implied `Z_1`, puts them into our radii polynomial, and recovers their `r_0`.
That checks four lines of algebra and nothing else. The number is transcribed, not computed.

So before this leg, no output of `solver/interval_certificate.py` had ever been compared with a
certified radius that somebody else published and a referee checked.

## 2. The problem, and where its truncation came from

Cadiot–Lessard–Nave, [arXiv:2302.12877](https://arxiv.org/abs/2302.12877) (SIADS
[10.1137/23M1607507](https://doi.org/10.1137/23M1607507)) §6: the Kawahara soliton. With Bond
number `T` and speed `c`, the travelling-wave reduction integrated once is their (75), which in
the sign convention of their released code is

```
F(u) = L u + λ₃ u²,   L = I + λ₁ ∂ₓₓ + λ₂ ∂ₓₓₓₓ,
λ₁ = (1−3T)/(6(1−c)),  λ₂ = (19−30T−45T²)/(360(1−c)),  λ₃ = 3/(4(1−c)).
```

**The paper prints `T = 0.35`, `c = 0.9` and the constants — but not the truncation.** It gives
`‖DF_e(u₀)⁻¹‖_{2,l} ≤ 4.4`, `Y₀ ≤ 2.26e−14`, and Theorem 6.6's `r₀ = 2.27e−14` with uniqueness
in `B_{0.015}`. The discretisation is only in the code:
[`ProofKawahara.jl`](https://github.com/matthieucadiot/ProofKawahara.jl) lines 357–360 give
**`N = 250` cosine modes and half-domain `d = 50`**.

That matters beyond convenience. Lesson 84 requires a known-answer probe to pre-commit its
window, and the window is only meaningful *at their truncation*. It could be pre-committed here
because CLN released their package — the exact contrast with arXiv:2604.09949, which
`LITERATURE_CHECK.md` records as unusable partly because no package was released.

## 3. The sign convention was confirmed, not assumed

Drop `λ₂` and the KdV reduction `u + λ₁u'' + λ₃u² = 0` has the closed-form soliton
`u = α sech²(βx)` with `β² = −1/(4λ₁)`, `α = 6λ₁β²/λ₃`. At `T = 0.35, c = 0.9` that is
`α = −0.2`, `β = √3`. Newton from that seed converges to a profile with **minimum −0.181650 at
the origin**, decayed to `4.3e−18` at `x = d`. CLN's Figure 1 shows a minimum a little above
−0.18. The profile lands on their picture before any certificate constant is quoted, which is
how a sign slip in `λ₁, λ₂, λ₃` was ruled out rather than hoped away. Gate (13).

## 4. What is certified, and what is not — before the number

The object is the finite **Galerkin system** `F_n(a) = l_n a_n + λ₃ (a∗a)_n`, `n = 0..N`, in
even exponential coefficients, `l_n = 1 − λ₁k_n² + λ₂k_n⁴`, `k_n = nπ/d`. CLN certify strictly
more: the Fourier tail `n > N`, and the passage from the periodic problem on `Ω₀` to the one on
`ℝ`. Their Theorem 6.6 states both conclusions, and the periodic one — a solution in
`B_{r₀/√|Ω₀|}(U₀) ⊂ X^l_e` — is the one comparable to ours.

**Because we bound fewer terms, our radius is expected below theirs.** That was written down in
`writeup/novelty/leg_61.md` before construction, together with its consequence: a radius below
`r₀` is evidence of over-optimism, not of a sharper proof.

## 5. The norms differ, and the conversion is part of the result

This pipeline works in the weighted sup norm `‖a‖_w = max_n w_n|a_n|`; CLN work in `ℓ²_l`. For a
vector supported on `|n| ≤ N`,

```
‖a‖_{ℓ²_l} ≤ √(2N+1) · supₙ(lₙ/wₙ) · ‖a‖_w ,   then ×√|Ω₀| for CLN's H^l(ℝ).
```

Measured: `sup lₙ/wₙ = 1.000000000000007`, `√(2N+1) = 22.383`, total factor to `H^l` **223.83**.
Every step rounds up, so **every converted radius here is too large, never too small**. Gate (16)
checks the inequality against random vectors rather than trusting the algebra.

`√(2N+1)` is the worst case — the residual spread evenly across all modes. It is not tight, and
§8 shows it is the dominant term in the comparison.

## 6. The run

| quantity | value |
|---|---|
| float residual, sup norm | `1.301e−18` |
| `Y₀` (rigorous, `ℓ^∞_w`) | `3.0243e−17` |
| `Z₁` | `3.059e−13` |
| `Z₂` | `8.5455e+03` |
| `‖A‖_w` | `2.9834` |
| `Y₀ / budget` | `5.169e−13` |
| certified interval, `H^l` | `[6.7698e−15, 2.6193e−02]` |
| **CLN published interval** | **`[2.27e−14, 1.5e−02]`** |

## 7. The gate, both readings, magnitudes not booleans

> "Does `solver/interval_certificate.py`, run end to end on the Kawahara problem, produce a
> certified radius inside CLN's published interval at their truncation?"

**READING A — the gate's literal words, on the certified SET. YES.** A radii polynomial
certifies existence at *every* `r ∈ [r_min, r_max]`. Our certified interval
`[6.77e−15, 2.62e−02]` **contains CLN's published interval entirely**: their `r₀ = 2.27e−14` is a
certified radius of our polynomial, sitting **0.53 decades above our `r_min` and 12.06 decades
below our `r_max`**. Our `r_max` also reaches past their uniqueness ball by 1.75×, so the
certificate is not closing on something it cannot identify with their soliton.

**READING B — the stricter pre-committed window, on `r_min` itself. NO, by 3.35× (0.53
decades).** The window was `r* ∈ [2.27e−14, 1.5e−02]`, a span of 11.8 decades; `r_min`
converted is `6.77e−15`, below the lower end. The upper constraint is satisfied with 12.3
decades of headroom.

**Neither reading is the answer on its own and neither is suppressed.** Reading A is what the
gate asked. Reading B is what was written down in advance, and it came out low.

## 8. Why Reading B came out low — two explanations nominated in advance, both FALSIFIED

The pre-committed reading of a low `r_min` is over-optimism. Two concrete mechanisms would make
that reading correct, and both were tested rather than argued (disciplines 85/90).

**Ablation 1 — CLN's trace projection.** They do not certify the Newton iterate. They project it
onto `ker T^N_{4,e}` so its representation lies in `H⁴₀(Ω₀)` and extends by zero to `ℝ` —
a step that can only raise the residual. Replicated here (`kawahara_trace_projection`, the
`ℓ²_l`-nearest point of the kernel): `Y₀` moves from `6.769e−15` to `6.940e−15`, a factor
**1.025**. It needed to supply 3.34× and supplied 2.5%. **Not it.**

**Ablation 2 — the discarded mode-`(N, 2N]` tail of `u²`.** CLN's `Y₀` carries
`‖U² − π^N U²‖₂`; a finite Galerkin certificate has no such term. Measured:
`1.665e−17` in their normalisation, against a gap of `1.59e−14` to explain — **2.98 decades
short**. **Not it either.**

**What is left is the norm conversion, and the resolution sweep measures it.** Across
`N = 60, 100, 150, 200, 250, 300`, `Y₀` in our own norm is **flat at ≈3.0e−17** — it is set by
the float64 Newton residual, not by resolution (the coefficients are already at `1.6e−22` by
mode 250). The converted `r_min` nevertheless climbs `3.31e−15 → 7.20e−15`, tracking
`√(2N+1)` exactly. **The position of our radius relative to CLN's is set by the conversion
factor, not by the arithmetic.**

So the honest statement is not "we are 3.35× over-optimistic". It is: **our upper bound is
3.35× below their upper bound after a deliberately pessimistic conversion**, and two upper
bounds on different quantities in that relation contradict nothing. The disagreement branch of
the gate requires the pipeline to *fail* where they prove existence, or to close only above
their uniqueness ball. It does neither.

## 9. The resolution of this gate, stated so it is not over-read

Because the comparison passes through `√(2N+1)`, **this gate localises the pipeline to a factor
of a few — about half a decade. It is not a digit-level check.** Said plainly:

* it is **ample** for what it was built for. Leg 56 reports consistency defects of `1.85e7×` and
  `2.04e11×` from this same pipeline. Those are **7 and 11 decades** from where this gate's
  resolution sits, so they clear it with ~6.5 and ~10.5 decades to spare;
* it would be **useless** for validating a 2× claim, and must never be cited as if it were.

## 10. The poisoning control

A displaced iterate must be noticed, and the response must scale rather than saturate — a
saturating `Y₀` would be measuring the arithmetic instead of the iterate. Kicking the 20 lowest
modes: `Y₀/budget` = `4.968e−08` at `1e−12`, `4.968e−04` at `1e−08`, `4.966e+00` at `1e−04`.
Exactly linear in the displacement across 8 decades, and the certificate **fails to close** at
`1e−04`. Gates (15) and (17).

## 11. What this leg does NOT claim

Nothing about the Kawahara equation, solitons, or certification methodology. The soliton is
proved, published and refereed; the novelty pass returned `PROCEED_AS_INTERNAL_AUDIT` and no
claim is available. The only claimable object is a statement about **this repository's own
pipeline**, and it is the one in §7–§9.
