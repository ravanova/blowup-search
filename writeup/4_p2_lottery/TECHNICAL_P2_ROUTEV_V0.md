# Route-V v0 — the novelty gate: certification under dissipation was done in 2024, and here it is re-derived

*Phase 2 / P2, leg 48. Code: `solver/viscous_novelty.py` + `test_viscous_novelty.py` (8/8),
`experiments/p2_route_v_v0_novelty.py` → `writeup/data/p2_route_v_v0_novelty.json` → fig43.
Working notes: `PHASE2_P2_NOTES.md` §37. Deterministic, 84 s.*

**Stage V — "switch dissipation on and ask whether the radii polynomial still closes" — is
pre-empted. Dahne–Figueras (arXiv:2410.05480) verify whole branches of self-similar
singular solutions of the complex Ginzburg–Landau equation, continued in the dissipation
parameter from the conservative NLS limit, in interval arithmetic. This leg re-derives
their published zeros to `1.8e−07`, reproduces their branch to `3.0e−06` in the dissipation
parameter across its whole length, and locates their fold at `ε* = 0.0606365` against their
own figure's `0.0606361`. The plan's pre-committed fallback applies: stage V is closed,
stage C-PILOT is next. No chain link moved; Clay unchanged at ~0.05%.**

---

## 1. Why the gate exists, and why it is a ban rather than a habit

`plan_of_record.py` carries stage V behind a gate with both branches written down in
advance:

> FIRST: has anyone already done certification-under-dissipation for a self-similar blow-up
> profile? **yes** → report it, fall back to stage C-PILOT, and do NOT spend the leg.
> **no** → proceed to the deliverable.

and a standing ban — *building stage V's measurement before its novelty check has reported*.
The reason is leg 42, which read the primary sources for the first time and deleted **seven
of twelve** standing novelty claims. Stage V was proposed as a speculation of exactly that
kind, and was flagged as one when it was written.

The gate is asked here the way Route-J (§31) asks literature questions: not with a
paragraph asserting that a check happened, but with code that re-derives the published
result from the published equations. A literature claim that cannot be re-run decays at
the rate of memory (banked lesson 68).

## 2. The answer: YES, and the paper is Dahne–Figueras

**arXiv:2410.05480**, Dahne & Figueras, *Self-Similar Singular Solutions to the Nonlinear
Schrödinger and the Complex Ginzburg–Landau Equations* (Oct 2024). Their equation is

```
i u_t + (1 − iε) Δu + (1 + iδ) |u|^{2σ} u = 0
```

and **ε is a dissipation dial**: `ε = δ = 0` is the focusing NLS, conservative; `ε > 0` is
Ginzburg–Landau, in which the Laplacian acquires a dissipative real part. The Zakharov
ansatz reduces blow-up to a singular ODE for the profile `Q(ξ)`, and their Theorem 4.1
proves the existence of **eight continuous branches** of self-similar singular solutions in
Case I (`d = 1, σ = 2.3`), each born at an NLS solution and followed as `ε` grows, verified
along the whole branch by a rigorous shooting method in interval arithmetic. Theorem 4.4
does the same in Case II (`d = 3, σ = 1`) and verifies only **parts** of the branches.

That is stage V's question — *does the certificate still close as dissipation turns on, and
where does it stop closing* — asked and answered two years ago, with rigour this project
does not have. A second, weaker precedent (**arXiv:2404.04054**) certifies self-similar
profiles of parabolic PDEs including a viscous Burgers equation by Newton–Kantorovich in a
weighted Sobolev space, without following a dial.

**The one hole, stated precisely because it is tempting.** Twelve arXiv queries are logged
in `SEARCH_LOG`; the four asking for the *fluid* version — a viscous Boussinesq/Euler/CLM
blow-up certified under a viscosity dial — return nothing. That hole is real. It is **not**
what stage V asked for. Narrowing "has anyone done certification under dissipation" to "has
anyone done it for our model" after seeing the answer is the move leg 42 deleted seven
claims for.

## 3. The re-derivation (V0-2), which is what makes the gate a check

Their profile ODE is integrated from the origin by an independent RK4 with a
phase-resolving step, and matched at `ξ₁` to a **three-term far-field expansion derived in
this module**, not transcribed: with `p = −1/σ − iω/κ` and `Q = γ ξ^p (1 + a₁ξ^{−2} +
a₂ξ^{−4})`,

```
a₁ = [(1 − iε) p(p+d−2) + |γ|^{2σ}] / (2iκ)
a₂ = {(1 − iε) a₁ [p(p+d−2) − 2(2p+d−1) + 6] + |γ|^{2σ}[(σ+1)a₁ + σ ā₁]} / (4iκ)
```

The value equation defines `γ` by a fixed point, leaving the derivative equation as two
real equations in the two real unknowns `(μ, κ)`. Newton on that:

| row | published `μ`, `κ` | our `Δμ` | our `Δκ` | Newton steps | defect |
|---|---|---|---|---|---|
| Case I, j=1 | 1.23203754902, 0.85310897700 | −2.3e−08 | −1.8e−07 | 4 | 3.7e−13 |
| Case I, j=2 | 0.78307776500, 0.49322332400 | −1.5e−06 | −8.0e−07 | 5 | 1.8e−15 |
| Case I, j=3 | 1.12384441100, 0.34675442900 | −1.7e−06 | −9.5e−07 | 5 | 1.2e−15 |
| Case I, j=4 | 0.88388273000, 0.26676158000 | −1.1e−05 | −3.1e−06 | 5 | 1.0e−14 |
| Case II, j=1 | 1.885656965028834, 0.9173561185914533 | +2.3e−08 | +2.5e−08 | 6 | 6.5e−14 |

The gate was pre-committed at `1e−06` on the `j = 1` rows: **1.8e−07, VERIFIED**. The `j=4`
row is the worst at `1.1e−05` and the reason is stated rather than hidden — they match at
`ξ₁ = 25`, we clip to 20, and §4's ladder shows that is exactly what far-field truncation
costs.

**`γ` is deliberately NOT gated.** They parameterise the solution manifold at infinity in
their §7; our `γ` is the coefficient in *our* expansion. Two quantities with the same name
and different definitions is how a transcription error hides, so they are kept apart
(Route-J's rule: verified and transcribed are different words).

## 4. The guards, before the claim (V0-3)

* **Step halving.** Case II, 200 → 400 → 800 steps per oscillation: defect
  `4.994e−10 / 4.920e−10 / 4.915e−10`. Halving moves it by `7.9e−12`, two orders below the
  defect itself — so the residual floor is the far-field truncation, not the integrator.
* **Far-field truncation.** `ξ₁ = 10 / 15 / 20 / 30` moves the returned `κ` by `1.2e−06`
  in total, and by `3.6e−08` across the last three. The ladder's *shape* is reported, not
  its tightest rung (discipline 72).
* **The defect discriminates.** At the published zero the defect is `8.2e−07` (relative to
  `|Q'(ξ₁)| = 1.1e−02`, i.e. `7.5e−05` — the scale is named, not left implicit); perturbing
  `κ` by `1e−04` raises it `351×`. A diagnostic that is small everywhere gates nothing
  (lesson 55).

## 5. The dissipation dial, and their fold (V0-4)

Continuing directly in `ε` cannot pass a turning point: below `ε*` there are two solutions,
above it none. `κ` is monotone along the branch, so the continuation is run **in `κ`, solving
for `(μ, ε)`** — which makes the fold an ordinary interior point instead of a Newton
failure.

129 converged records, `dκ = 0.005`, `κ` from 0.8531 down to 0.21:

```
fold          eps* = 0.06063648    kappa* = 0.554682
published     eps* = 0.06063610    kappa* = 0.554644
difference          +3.8e-07             +3.8e-05
```

**The published curve is read as data, not eyeballed.** Their Figs. 1 and 2 are pgf vector
graphics, so the branch polylines and the axis tick marks are literally in the PDF content
stream; `read_df_figure` calibrates on the ticks and returns `(ε, κ)` pairs. The
calibration checks itself: the eight extracted curves' `ε = 0` endpoints land on the eight
`κ` of their Table 1 — transcribed from a different page — to **1.0e−05**, the width of a
plotted line. Against that curve, our branch agrees to **max 3.0e−06, rms 1.9e−06** over 13
samples spanning both sides of the fold.

## 6. The shape of their answer, which is the part stage V wanted (V0-5)

`‖J⁻¹‖∞` for the shooting Jacobian is the float analogue of `‖A‖` in a radii polynomial —
every certificate constant degrades with it — and it is called an analogue, not a
certificate constant, because that is what it is.

```
eps = 0 (the NLS end)      ||J^-1|| = 7.15e-01     cond(J) = 8.4e+00
mid-branch (eps = 0.0486)  ||J^-1|| = 2.71e-02     cond(J) = 2.1e+01
nearest sample to the fold ||J^-1|| = 1.53e+00     cond(J) = 2.4e+03
```

**Switching dissipation on does not degrade the margin — it improves it, by 26×.** The
degradation is entirely a fold phenomenon, and the fold's exponent is measured rather than
announced: `‖J⁻¹‖ ∼ |κ − κ*|^s` with

```
s = -1.061      (an ordinary quadratic fold predicts -1)
```

fitted on ten points at offsets `0.08 … 0.005` either side. Measuring an exponent instead
of declaring a threshold is Route-F's rule; the exponent is checkable and a threshold near
a critical point is biased in the direction you expect.

`|Q'(ξ₁)|`, the scale the proxy is implicitly divided by, moves only `1.09e−02 → 8.7e−03`
over the top of the branch, so the 26× is not a units artefact (discipline 67: gate the
quantity the measurement divides by).

## 7. What this is, and what it is not (V0-6)

**Is:** a novelty gate, answered YES, with the pre-empting result reproduced from its own
equations well enough to be sure the pre-emption is real — and, as a by-product, an
independent check on a published computer-assisted proof.

**Is not:** a certificate (nothing here is interval-enclosed; theirs is the rigorous
result). Not about a fluid model — CGL is semilinear and radial; the Hou–Luo target is a
transport model on the line. Not novel: reproducing somebody else's certified branch is not
a result of ours. Not a chain link, and not evidence about Navier–Stokes. Clay stays at
~0.05%.

## 8. What it changes in the plan

Stage `V` closes as **DONE (pre-empted)**, and the fallback the plan named before the check
was run — stage **C-PILOT** — is next. The leg also hands C-PILOT something it did not have:
`branch_in_kappa` is a **known-answer object with a dissipation dial**, whose answer is
published and whose fold is now reproduced to `4e−07`. C-PILOT's requirement is exactly an
object with a known answer.

**The banked lesson (82).** A gate whose YES branch costs one leg and whose NO branch costs
five is worth asking even when you are confident of the answer — and this one was asked
*because it was written down in advance*, not because it felt necessary on the day. The
result cost 84 seconds of compute and saved building interval arithmetic and a tail lemma
for a question that was already answered.
