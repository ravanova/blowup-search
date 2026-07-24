# We built the far side of the wall, and it held

*What happened when the change-of-variables stopped being a plan and started being
code that runs. Sequel to [BLOG_PHASE2_RESCALING.md](BLOG_PHASE2_RESCALING.md)
("The wall has a far side, and it's made of other people's numerics"). Technical
record: [TECHNICAL_SPIKE0_RESCALING.md](TECHNICAL_SPIKE0_RESCALING.md). Figure and
committed data rebuild with one command; see the end.*

Last time ended on a promise and a caveat. The promise: the far side of our
uniform-grid wall is a **change of variables** — dynamic rescaling, where you
continuously zoom into a forming singularity so the blow-up sits still as a *steady
profile* you can resolve forever. The caveat: this is other people's machinery, it
mostly finds the blow-up that's already been *proven*, and the honest novelty lives
one more step out. Both are still true. This post is about the promise becoming real:
the solver is built, and it recovers an answer we already knew — exactly, which is the
entire point.

## The rule of the house: never debug against a mystery

The discipline this project keeps returning to is *build on the substrate where you
already know the answer.* So the first dynamic-rescaling solver isn't for the model we
care about. It's for the one model where the self-similar blow-up is written down in
closed form: the Constantin–Lax–Majda equation, `ω_t = ω·H(ω)`. Start from `ω_0 =
-sin x` and it blows up at the origin at `T*=2`, and — this is the part we get to check
against — the *shape* it blows up into is exactly

$$\bar\Omega_0(X) = \frac{-4X}{1+4X^2},$$

with a Hilbert transform of `2/(1+4X^2)` and a blow-up rate of `ω ~ (T-t)^{-1}`. If our
rescaling solver is honest, it has to reproduce that curve and that rate from scratch.
If it can't hit an answer that's on paper, it has no business being pointed at an answer
that isn't.

## Two things had to work, and one of them was the whole game

The rescaled equation, once you specialize it to CLM and do the bookkeeping, is almost
disappointingly clean:

$$f_\tau = -\tanh(\rho)\,f_\rho + \big(H\Omega - H\Omega(0)\big)\,f.$$

That `\tanh(ρ)` is the hero of the story. The naive version of this equation has an
advection term whose *speed is the coordinate itself* — it grows without bound as you go
out the tail, and on a uniform grid it strangles your timestep so badly the solver dies
even when you hand it the exact answer as a starting point. (We watched it do exactly
that, in the reconnaissance. It's in the notes as a dead end.) Putting the grid points on
a `sinh` stretch — dense near the origin, exponentially sparse in the tail — turns that
runaway speed into `\tanh(ρ)`, which never exceeds 1. The timestep problem just
evaporates. That's not a trick; it's *why* the professionals discretize on a mapped grid,
and now we understand it from the inside.

The second thing was the crux, and it ate most of the effort. On a stretched grid you
can't use the fast Fourier transform to compute the Hilbert transform — the FFT wants a
uniform periodic grid, and our profile is a whole-line function with a slow `1/X` tail
that a periodic transform gets *wrong* (another banked reconnaissance finding: a periodic
solver converges, confidently, to the wrong shape). You need a **line** Hilbert transform
that works on a non-uniform mesh. The reference paper gives one — represent your function
in a special spline basis whose Hilbert transform is known analytically — and it comes
with a warning we'd flagged in advance: the closed-form coefficients go numerically
unstable near a certain limit, and the paper patches it with a 23-term polynomial that a
PDF-to-text tool turns to confetti.

We didn't transcribe the confetti. The instability is a Taylor-series cancellation, and
if you do the cancellation *by hand* — substitute the log's expansion into the formula
and watch the dangerous terms annihilate each other on paper — you get a clean expression
that's stable everywhere, no coefficient table required. It matched the paper's structure
exactly (one orphaned minus sign in the mangled OCR even confirmed a sign we'd derived
independently). The test that mattered: feed it `-4X/(1+4X^2)`, and out comes
`2/(1+4X^2)` to a relative error of `1.6×10⁻⁴`, POC target one percent. The hardest
component, validated in isolation against a number we knew. That was the day the project
felt real again.

## Then the nice surprise

With the crux working, the actual experiment is almost anticlimactic. Take the exact
profile — the solver holds it steady, residual `4×10⁻⁶`, rate `c_ω = -0.999` against a
target of `-1`. Good. Now the real question: take some *other* odd bump with the right
slope at the origin — a Gaussian, say, visibly wider and taller than the true profile —
and let it run. Does it find its way home?

It does. The wrong shape flows smoothly onto the right one (panel A of the figure: the
gray dashed starting bump collapsing onto the black exact curve), the rate slides to
`-0.999` and parks there (panel B), and the whole thing settles to a steady state as the
residual decays five orders of magnitude (panel C). A second, differently-shaped
perturbation lands on the same profile. Refine the grid and the numbers tighten toward the
exact answer. The self-similar profile isn't just *a* solution — it's an **attractor**.

Here's why that's worth a paragraph. Going in, we'd half-expected trouble. The
reconnaissance had seen the one-scale rescaling *overshoot and blow up in the rescaled
frame* — which looked exactly like the famous scaling instability that forced Chen and Hou
to invent a more elaborate *two-scale* method. If that instability were real for us, this
spike would have been the start of a much longer detour. It wasn't real. It was an artifact
of the wrong (periodic) Hilbert transform and a fussy normalization choice. Swap in the
correct line transform and the correct value-based normalization, and one scale is plenty:
the profile is stable and attracting. A worry we'd written down got answered, and the
answer was the good one.

## What this is, said plainly

It is a solver that reproduces a **proven, closed-form** result in a **1D toy model.** It
validates machinery — the stretched grid, the line Hilbert transform, the normalization,
the attractor. It is **not novel, and it is not a proof.** We're being deliberate about
two temptations in particular:

- We do **not** claim we "recovered `T*=2`." We didn't, and we shouldn't. That blow-up
  time belongs to the global periodic problem; a whole-line rescaling run has a free
  amplitude gauge, so it simply doesn't determine `T*`. What it determines is the *rate*,
  `c_ω → -1`, which is the local shadow of that number and is the honest thing to report.
  Claiming the famous constant off a run that can't see it is exactly the self-deception
  the whole project is built to avoid.
- We do **not** claim this gets us closer to the Millennium Prize in any way that matters.
  It gets us a trustworthy tool. The prize stays behind the two walls it's always been
  behind.

## Where the road forks

The technique is de-risked in 1D against a known answer, which is precisely what a spike
is for. The next lift is the real one: port this machinery to two dimensions — the
Boussinesq / Hou–Luo geometry — and try to reproduce the Chen–Hou profile there. That's a
different mechanism, and it's where we'll find out whether the two-scale ghost we just
exorcised in 1D comes back. It also, honestly, reproduces another *proven* profile; the
step where anything *new* could happen is further out still, in constructing the unstable
profiles nobody has pinned down. We're keeping that horizon in view and not pretending
we're standing on it.

But the thing that was a diagram last month runs now, and it hit the number it was
supposed to hit. On a project whose entire ethic is *don't fool yourself*, there's a
specific pleasure in checking your work against an answer the universe already wrote down —
and matching it.

---

*Reproduce it:* `.venv/bin/python test_line_hilbert.py` and
`.venv/bin/python test_gclm_rescaled.py` run the validation (11 predicates). The figure
and its committed evidence rebuild with
`.venv/bin/python writeup/spike0_rescaling_evidence.py` (no solver re-run needed for the
figure; add `--generate` to regenerate the data, ~1 min). Full technical record:
[TECHNICAL_SPIKE0_RESCALING.md](TECHNICAL_SPIKE0_RESCALING.md).*
