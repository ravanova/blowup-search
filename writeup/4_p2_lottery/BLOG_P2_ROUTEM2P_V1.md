# The candidate passed the test — and stopped being the candidate

*Route-M2P, leg 125. Technical companion: `TECHNICAL_P2_ROUTEM2P_V1.md`.*

---

Sixty-three legs into looking for something certifiable, this project found exactly one target
that passed its own screen: the generalized Constantin–Lax–Majda equation with full Laplacian
dissipation. Blow-up on it isn't conjectured — it's **proved**, by Jiajie Chen, in
*Nonlinearity* (arXiv:1908.09385). And a literature search said nobody has ever built a
computer-assisted certificate for a *dissipative* self-similar blow-up profile. So: a proved
singularity, an empty field, one obvious next step.

The leg that found it read the abstract. It said so, and listed reading the actual paper as an
open debt. This leg paid that debt.

## What the paper actually says

The abstract is accurate. Theorem 1.1 proves finite-time self-similar blow-up for `a` close to
`1/2` with `γ = 2` — full Laplacian, viscosity up to 1. All true.

Then you get to section 2, and it opens: *"Firstly, we study the inviscid problem, i.e.
ν = 0."* And a page later, having written down a beautiful closed-form profile, Chen adds:

> "In this self-similar blowup, the spatial blowup scaling is `c_l = 1/3`, if we add the
> diffusion term, such term is asymptotically small compared to the nonlinear term... we will
> treat the diffusion term as a small perturbation."

The viscosity appears in exactly two places in his argument, and both of them **decay to zero**
as the singularity forms. The profile at γ=2 is the profile at γ=0. Blow-up survives the
dissipation not because the dissipation is part of the structure, but because it's too slow to
matter: the singularity concentrates at rate `t^{1/3}`, and diffusion would need `t^{1/2}` to
keep up.

So the paper does prove what the abstract says. It just doesn't contain the object we came for.
**"A dissipative self-similar profile" isn't a thing here — it's an inviscid profile with
dissipation that can't catch it.**

Two independent checks agree. A separate group (Lushnikov, Silantyev, Siegel) catalogued the
exact solutions for this equation; their list has `a=1/2` at `σ=1`, and `a=0` at `σ=2` and
`σ=1` and `σ=0` — and no `a=1/2, σ=2`. Their `a=1/2` solution is labelled, in their own words,
"an exact solution of the **inviscid** problem." Same shape, same exponents, same story.

And we checked the other direction too: we asked the solver to find the dissipative steady
profile — the one that would have to exist if the candidate were what we hoped. Started it from
Chen's own profile, the friendliest possible guess. Newton's method ran away: the scaling
exponent drifted from `1/3` to `−10.7`, the residual stuck at order 1, and refining the grid
didn't help. There's nothing there to find.

## We measured it anyway, and it passed

The pre-committed gate was: does the residual `Y₀` come in under the certificate's budget? We
built the profile from scratch — a new solver module, Newton's method on the steady equation,
three resolutions — and measured.

It passed, comfortably. `Y₀/budget` ranges from `1.3e-09` to `5.8e-05` depending on resolution
and function space: **under budget by four to nine orders of magnitude**, at every resolution
tried. Chen's closed form nulls our discrete residual at fourth-order convergence, and the
solver independently rediscovers his `c_l = 1/3` to six digits without being told it.

So the gate says yes. It just says yes about the inviscid profile.

## The part where the instrument nearly lied

Two things went wrong first, and both were caught by controls rather than by anyone being
clever — which is the only reason they're worth writing down.

The first version reported `Y₀ ≈ 0.18`, and reported it at *every* resolution — the same number
whether the residual was `1e-4` or `1e-8`. That's not a measurement, that's a broken inverse.
The equation has two hidden symmetries (you can rescale the profile, and you can stretch it),
which means the linearised operator is exactly singular, and inverting it produces confident
nonsense.

The obvious fix is to pin the symmetry with a normalisation. We picked the natural one —
Chen's own `u_x(0) = 8/3` — and it did nothing. Conditioning went from `1.225e+07` to
`1.233e+07`: the fix bought a factor of 0.99. It turns out that particular quantity is
*constant* along the exact symmetry we were trying to kill. We'd bordered the system with a
tautology.

This project has a banked lesson from leg 53 that says precisely this: **a control that returns
the same number no matter what you do to it is a bug in the code, not a fact about the world.**
It took a second reading of that lesson to spot it. The working normalisation is `Ω_X(0)`,
which does vary along the symmetry; conditioning dropped by four orders and Newton started
converging in three steps. Both the fault and the tautology are now regression tests.

We also re-read the one "positive control" this project had banked for dissipative problems —
`Z₁ = 0.9156 at μ = 2` — instead of assuming it transferred. It doesn't. Reading the source,
`μ` is the *coefficient* of a `Λ¹` dissipation, not an exponent of `Λ`. The control was γ=1 all
along, on a different operator, in a different basis, around a different anchor. Nothing to
borrow.

## Where this leaves it

The gate answered yes, so under the rules this leg was given, the candidate advances and the
decision about whether to spend a full certificate attempt goes up to the human. But it goes up
with the honest version attached, because the yes and the reason we cared have come apart:

- What clears the budget is an **inviscid** profile — and this project's own exclusion list
  already says inviscid gCLM profiles for `a ≤ 1` are analytically known, which is why targets
  like that were excluded to begin with.
- At `a = 1/2` exactly, the target is a **closed form**. Certifying it means certifying
  something you can already write on a napkin.
- The genuinely new remainder is smaller but real: at `a = 0.45` or `0.48`, no closed form
  exists, our solver converges to visibly different profiles (8% away), and `Y₀` is still four
  decades under budget. **Those numbers appear to be the first of their kind.** If a
  certificate attempt happens, that's what it should be aimed at — not at the dissipative
  framing, which didn't survive contact with the paper.

## The honest ceiling

This is **not** progress on Navier–Stokes. The Clay odds stay where they were, at roughly
0.05%, and nothing here touches the chain of results that would have to move for that to
change. Everything measured is a truncated system in ordinary floating point, with the
far-field tail unbounded — a *necessary* condition for a certificate, nowhere near a sufficient
one.

What the leg is actually worth is smaller and, we'd argue, still worth having: the repository's
best remaining candidate has been read at full depth instead of abstract depth, one inherited
formula has been corrected, one banked control has been shown not to transfer, two instrument
faults have been found and fenced, and a target that looked like it was about dissipation turns
out not to be.

The third time this project has been burned by reading an abstract, it caught it. That's the
result.
