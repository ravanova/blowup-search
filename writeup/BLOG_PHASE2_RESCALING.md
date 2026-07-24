# The wall has a far side, and it's made of other people's numerics

*What happened when we stopped searching and started building. Sequel to
[BLOG_PHASE1_GATE4_REFORM.md](BLOG_PHASE1_GATE4_REFORM.md) ("The gate we built to
fail"). The technical record is [TECHNICAL_PHASE2_RESCALING.md](TECHNICAL_PHASE2_RESCALING.md);
the planning docs are [../PHASE2_NUMERICS_PLAN.md](../PHASE2_NUMERICS_PLAN.md) and
[../PHASE2_SPIKE0_NOTES.md](../PHASE2_SPIKE0_NOTES.md).*

The last post ended a search. Two independent fitness functions, two pre-committed
cheat-audited gates, one identical failure: on a uniform grid the "most singular"
optimum is never blow-up structure, it's the vanishing-vorticity corner. We proved,
carefully, that we'd hit a wall — and that the wall was the *grid*, not the currency.
On a uniform mesh the real singularity forms below grid scale, so nothing you read off
the trusted window is the thing you're hunting.

A wall is a finding, not a motivation. So we didn't reach for a third currency. We
asked the honest next question: what does the far side of this wall actually look
like, and what would it cost to get there?

## The far side is a change of variables

The field figured this out a while ago, and it isn't AMR. For a blow-up that's
(approximately) self-similar — which the Hou–Luo / Boussinesq / CLM singularities are —
the tool is **dynamic rescaling**: instead of watching a spike sharpen until your grid
gives up, you continuously zoom and renormalize into the singularity's own frame, where
the blow-up sits still as a *steady profile* you can resolve on a fixed grid forever.
It's the method McLaughlin and collaborators built for the nonlinear Schrödinger
equation in the 1980s, and it's how Chen and Hou constructed the self-similar profile
that their 2022 computer-assisted proof of Boussinesq blow-up actually rests on.

There's a subtlety worth stating plainly, because it reframes this whole project. The
*current* frontier isn't even dynamic rescaling — it's solving for the self-similar
profile **directly**, with Newton iterations or physics-informed neural networks,
chasing *unstable* profiles nobody had seen (Wang–Lai–Gómez-Serrano–Buckmaster, and
the 2025 machine-precision work). That world doesn't evolve initial conditions and
doesn't run a genetic algorithm at all. Which means the honest framing of our "evolve
the initial condition" premise is: dynamic rescaling is the shared substrate, and it's
an *on-ramp* to profile construction, not a destination. We build it, then we decide —
with a working solver in hand — whether searching over ICs still earns its keep.

That decision we deferred. The solver we started.

## Validate on a known answer, in 1D, first

The project has one iron build rule: never debug a new method and a new problem at the
same time. So before touching 2D Boussinesq, dynamic rescaling gets validated in 1D on
the CLM model, where the self-similar blow-up is *explicit*. Feed in `ω₀ = −sin x`, and
CLM blows up at the origin at exactly `T*=2`, with the closed-form profile
`Φ(η) = −4η/(1+4η²)`. If our rescaling machinery can't recover that, it isn't ready for
a problem where we don't know the answer.

I derived the rescaled equation by hand, got a clean target — amplitude rate `→1`,
length rate `→−1` — and started coding. Then I got to watch the method teach me why
it's hard.

## Three ways to be wrong, each worth knowing

**First:** I normalized the rescaling by pinning a third derivative at the origin. The
`(ik)³` in a spectral third derivative is a noise amplifier; the quantity I was pinning
read *a thousand* when its true value was one. Lesson: normalize with integrals, never
high pointwise derivatives.

**Second, and more instructive:** I ran the whole thing on a periodic grid, and it was
*stable*. It settled down. It converged to a profile. The profile was **wrong** — the
fitted shape parameter came out around −1 when CLM says 4. This is the kind of bug that
would sail straight past a casual eye: a stable-looking run that produces a confident,
plausible, incorrect number. The cause is subtle: the true CLM profile lives on the
whole real line and decays only like `1/X`, and the periodic Hilbert transform simply
isn't the line Hilbert transform for a tail that slow. My earlier optimistic note that
"periodicity is fine here" was itself an artifact of computing the wrong transform.

**Third:** so I moved to a big whole-line grid, got the line Hilbert transform right
(finally), and the thing NaN'd instantly — even when I *started it exactly on the answer*.
Not a subtle bug this time: a CFL violation. The self-similar zoom is an advection term
whose speed is the coordinate `X` itself, up to the edge of the domain. On a uniform
grid that demands a timestep 20× smaller than I was using, and no amount of filtering
buys it back.

Three failures, three findings. And a pattern I should have trusted sooner: every time
I tried to reinvent a piece of this method, the method won.

## So I read the paper

The uniform-grid CFL death isn't a nuisance to filter away — it's the reason the
literature uses a *stretched* grid. Put your points down as `X ~ sinh ρ` with `ρ`
uniform, and the spacing grows with `X` in exactly the way that makes the zoom's CFL
condition independent of how far out your domain reaches. That single trick is why these
solvers can push their outer boundary to `10¹⁰` and still take sane timesteps. But a
stretched grid is non-uniform, and a non-uniform grid can't use an FFT for the Hilbert
transform — which is why Huang, Tong and Wang (whose 2026 gCLM paper turns out to
contain the exact scheme we need, hand-derivation and all) spend an appendix computing
the line Hilbert transform analytically, element by element, on a cubic-spline basis
built specifically so each element's transform is a known closed form.

It's real numerical analysis, and it's a multi-day build: a spline-analytic line
Hilbert transform, a stretched cosh/sinh mesh, a WENO5 + high-order SSP Runge–Kutta
time integrator. We now have every formula. We've built none of the solver yet — and
saying so plainly is the point.

## Where this actually stands

No solver. No 2D result. No blow-up, no proof, nothing about the Millennium problem —
and, honestly, even the *best* case here is reproducing a singularity Chen and Hou
already proved, in a toy model two full steps removed from Navier–Stokes. What we have
is a decision made with open eyes (build the rescaling substrate; re-decide the search
question later), a formulation validated against a known answer on paper, and a
reconnaissance that mapped three dead ends and one correct road before spending a week
walking down it.

That last part is the whole method of this project, applied to ourselves. You can burn a
month building the wrong solver. Or you can spend a day finding out, in 1D, against an
answer you already know, which three things don't work and which paper already solved
the fourth. The far side of the wall is reachable. It's just made of other people's
numerics, carefully — and the least self-deceiving thing we can do is credit them and
build it right.
