# Experiment Journal

Hand-written context per experiment (see LOGGING.md — the structured logs
answer "what happened"; this records *why* and what a human noticed).

## Phase-2 P2 — ROUTE-TC v1: the seam, not the tail (non-logged) — 2026-08-05

**NOT a logged gate run** (deterministic; 318 s). Runner
`experiments/p2_route_tc_v1_assemble.py` → `writeup/data/p2_route_tc_v1_assemble.json` →
**fig48** via `writeup/4_p2_lottery/p2_route_tc_v1_evidence.py` (registered in
`writeup/build_figures.py`). Writeups TECHNICAL/BLOG_P2_ROUTETC_V1.md; PHASE2_P2_NOTES §42.
Stage `TC` of `plan_of_record.py`, 8 pre-committed clauses. No new solver module — the tail
side is leg 52's `solver/spectral_certificate.py`, imported and extended, not rebuilt.

**Why it exists.** Leg 52 bounded one term of four in isolation and the plan named the ban
in the same breath: a bounded bordered tail is not a certificate, because the border it adds
is an unknown with no column, no `Y₀` and no matching condition. This leg writes those three
down and puts all four terms in the same polynomial.

**REVISED after VERIFIER's line review.** The gate answer and every number were independently
confirmed; three attributions were not, and are corrected in the write-ups and in the runner:
the *scope* of the failure, the *mechanism* behind the sizes, and a control that could not fail.
A normalisation ablation (TC-8) was added. The resurfacing clearance is withdrawn (see (5)).

**What a human should notice.** Six things.

(1) **The binding term is one that did not exist before the assembly.** Three of the four
terms are fine — `Y₀` exactly 0, the finite-block `Z₁` at `10⁻¹⁵`, `Z₂` finite from the basis
algebra — and leg 52's tail constant behaves (2.19–10.32 at the splits used here). What kills
it is the *coupling* between the finite block and the tail, which is only a quantity once
both are in the same object: **43.15** at the best split in the entire sweep, against the 1 it
has to be under. This is the second time in three legs that the answer was in a place the
previous leg's framing could not see, and it is banked as lesson 89.

(2) **The first positive control was wrong, and it was wrong in an instructive way.** Adding
`μk` to the diagonal and keeping everything else identical made the answer *worse* (`Z₁` in
the thousands). The reason is not the mathematics: with `μ > 0` the tail has no kernel, so
bordering it with its near-null pair — and carrying a far-field amplitude it does not have —
manufactures a singularity. The control had to drop the border and the amplitude to be the
dissipative problem's *own* certificate. It then does exactly what the mechanism predicts,
`1/μ`, and reaches `Z₁ = 0.9156` at `μ = 2`. **A control that contradicts the mechanism is a
statement about the control's realization first (70), and I nearly wrote up a void negative.**

(3) **The gauge row has an entry that does not exist, and nobody could have seen it before.**
`Σ_k k b_k` is the obvious way to pin the dilation symmetry and it is what leg 51 used. Once
the far-field amplitude has a column, that column has an entry in the gauge row equal to
`Σ_m m h_m` — a harmonic sum, +1865 per e-fold. The dilation gauge is not a bounded functional
on any space where the target profile lives. The repair (pin `e₂`, which is *exactly* the zero
mode) is worth 1.5×–8.7× and changes no verdict, which is why it is written up as a defect of
the assembly and not as the cause of the failure.

(4) **The negative control I was proudest of was a bug, and the tell was that it was too
clean.** I reported `Z₁[Γ←tail] = 546.57` for all four border directions — analytic, SVD, wrong
singular pair, random — and called four identical numbers "the sharpest available form of 'this
is not about the border'." They were identical because the quantity was computed from two
objects neither of which references the border argument. It could not have come out otherwise.
Wired through properly (the border now sets the amplitude column's direction), the control
discriminates hard: analytic ties the SVD optimum at 1.0004, random is 13× worse, and the second
singular pair is 3.8e+13× worse because it makes the augmented block singular. **Four identical
numbers should read as a bug, not as a finding** — lesson 90.

(5) **I explained my own matrix using someone else's matrix.** I wrote that `‖Γ⁻¹‖` grows like
`K`, citing leg 51's `165 → 359 → 769 → 1633`. That is leg 51's *unaugmented* block; mine is
23× bigger at `K = 64` and grows like `K²` — exactly `2(K²−1)`, against exactly `4(K−1)` with
the amplitude column switched off. The `K²` is something *my augmentation* created, through a
weight pairing that leaves the matching equation carrying coefficient `≈ 2/K`. I also blamed a
factor `K/2` on the coupling entry when the measured factor is `2`. The conclusion survived a
six-way normalisation ablation (best case 20.47, still one to two orders too big) — but on a leg
whose entire methodological point is naming mechanisms, getting the mechanism wrong is the
expensive error, not the cheap one. **A suspiciously tidy closed form is a signal to check what
produced it.**

(6) **And I overstated what the result proves, in prose, while getting it right in the plan.**
`Z₁[Γ←tail]` contains `Γ⁻¹`, so the failure is scoped to the block-diagonal approximate inverse
the method requires. The sub-block that would have made it structural, `Z₁[tail←Γ]`, bottoms out
at **0.9961 — just under 1**. `plan_of_record.py` said "with the block-diagonal approximate
inverse the method requires" and stage `MM` asks exactly the right follow-up; the TECHNICAL
write-up and the curated JSON asserted the stronger claim. **The machine-readable artifact was
more honest than the prose, which is the wrong way round.**

*(Also withdrawn on review: this leg's clearance of leg 52's search-index flag. The query used
prepended the literal arXiv ID, which tests retrieval by ID rather than the topical recall the
flag was about; LIT re-ran leg 52's query verbatim and reproduced the null result. The leg
logged result counts, not links, so the claim could not be audited against its own record — a
novelty pass has to log the links.)*

## Phase-2 P2 — ROUTE-L1 v2: the representation change worked, and the tail did not (non-logged) — 2026-08-05

**NOT a logged gate run** (deterministic; 53 s). Code `solver/spectral_certificate.py` +
`test_spectral_certificate.py` (14/14); `experiments/p2_route_l1_v2_spectral.py` →
`writeup/data/p2_route_l1_v2_spectral.json` → fig46. Writeups
TECHNICAL/BLOG_P2_ROUTEL1_V2.md; PHASE2_P2_NOTES §40.

**Why it exists.** Leg 50's certificate closed in interval arithmetic around a truncated
grid object with two unbounded gaps. The plan of record said those are one gap and it is
the representation, and named the replacement: Route-E's compactified basis. This leg
builds the certificate there.

**What a human should notice.** Three things.

(1) **The prediction in the plan was right about the mechanism and wrong about which
response would be needed.** It expected the algebraic decay of the *profile* to bite and
proposed factoring the tail out. The profile used here is a single mode — as analytic as
anything can be — and the tail still fails, because the obstruction is in the *operator*:
the dilation transport is a shift with zero diagonal. Singularity subtraction would not have
touched it.

(2) **The positive control is doing the whole job of licensing the negative.** Adding `−μk`
to the diagonal — one line, no other change — makes every weight class saturate to exponent
`+0.000`. Without that dial the result would read as "my code diverges", which is not a
finding. With it, "inviscid transport has no diagonal and dissipation gives it one" is.

(3) **The exactly-zero `Y₀` is the least important number here and the most tempting one.**
It is zero because the anchor *is* one basis mode. It is banked in `plan_of_record.py` as a
ban rather than a headline, because the object that matters is not one mode and does not
even live in the space where the operator behaves best.

## Phase-2 P2 — ROUTE-L v1: the boring term did it (non-logged) — 2026-08-04

**NOT a logged gate run** (deterministic; ~13 min). Code `solver/port_certification.py`
(Route-L additions) + `test_port_certification.py` (10/10);
`experiments/p2_route_l_v1_precond.py` → `writeup/data/p2_route_l_v1_precond.json` → fig41.
Writeups TECHNICAL/BLOG_P2_ROUTEL_V1.md; PHASE2_P2_NOTES §33.

**Why it exists.** Route-K found the 2D linearized operator had no computable inverse and
named two suspects. This leg tests them.

**What a human should notice.** Three things.

(1) **Both suspects were innocent, and I had named them because they are the *interesting*
parts of the equation** — nonlocality and the boundary. Freezing the nonlocal velocity makes
the stall *worse*; the wall carries its proportional share of the stalled residual and no
more. The culprit was the angular transport: the term that just moves material sideways.
Building a six-way ablation battery cost about what writing the two guesses cost. Lesson (74).

(2) **I had conflated two different defects.** Route-K measured the *relaxation's* leftover
residual at the wall — correctly — and inferred the *linear solve's* would be there too. It
is not. Two failures in the same problem are not the same failure. Lesson (75).

(3) **The wrong construction is in the artifact on purpose.** ADI — composing an exact radial
solve with an exact angular one — gives 0.996, worse than doing nothing. That negative is
what ruled out the whole splitting family and forced me to notice the operator is triangular
in the radial index. A writeup that reports only what worked cannot stop the next session
re-trying what did not. Lesson (76).

**What it bought, and what it did not.** Step (iii) of the certification chain is unblocked —
first time in 44 legs. Newton still does not converge, but the failure changed kind: the
linear solves now succeed and a near-null direction caps the line search. I tested the
obvious explanation (the scaling gauge) and it is **refuted** — projecting onto it accepts no
step at all. Recorded as unidentified rather than replaced with a second guess.

## Phase-2 P2 — ROUTE-K v1: the certification port, and the ladder nobody read (non-logged) — 2026-08-04

**NOT a logged gate run** (deterministic; ~9 min). Code `solver/port_certification.py` +
`test_port_certification.py` (6/6); `experiments/p2_route_k_v1_port.py` →
`writeup/data/p2_route_k_v1_port.json` → fig40. Writeups
TECHNICAL/BLOG_P2_ROUTEK_V1.md; PHASE2_P2_NOTES §32; correction banner on Route-G.

**Why it exists.** Ranked item (3) — the L1→L2 certification port — had been deferred six
times. This is the leg that stops deferring it. It gets two rungs down the radii-polynomial
chain and the kill-switch fires.

**What a human should notice.** Three things.

(1) **The decisive evidence was already committed, two legs old, and nobody read the
column.** Route-G's resolution ladder has the steady residual going 1.7e−2 → 7.7e−2 →
2.7e−1 as `n_r` goes 300 → 450 → 600. Refining makes it sixteen times worse. I ran that
ladder, quoted a number from it, and never asked which direction the residual column went.
The new measurements in this leg confirm it and give the mechanism, but the finding was
sitting in `writeup/data/` the whole time. Lesson (71).

(2) **A local read stayed stable on a diverging object.** `c_ω` holds to 0.77% across that
same ladder, because the modulation is evaluated at the origin while the growing residual
lives at the wall. That is why "resolution-stable" felt like "converged" for two legs. The
concrete cost: Route-G's `β = 2.98 ± 0.02` sits 2.1% from the published 2.9206 — two and a
half times its own bar — and that gap was noted at the time and left alone.

(3) **The Krylov stall would have been a much weaker finding as a single number.** "GMRES
got to 0.66" is compatible with "hard but tractable". The ladder — 0.6946 at m=10, 0.6623 at
m=160 — is not, and the planted `cond ≈ 10⁸` control (which reaches 0.086) is what makes
"flat" mean something. Reporting the endpoint was the natural way to write it. Lesson (72).

**What it cost, and what it bought.** No link moved. But the blockage now has a location
(the wall), an identified removable component (the dilation continuum, worth 1.84× when
preconditioned away), and a named order of operations for the next two legs.

## Phase-2 P2 — ROUTE-J v1: the primary-source pass (non-logged) — 2026-08-04

**NOT a logged gate run** (deterministic; ~5 s). Code `solver/literature_gates.py` +
`test_literature_gates.py` (9/9); `experiments/p2_route_j_v1_literature.py` →
`writeup/data/p2_route_j_v1_literature.json` → fig39. Writeups
TECHNICAL/BLOG_P2_ROUTEJ_V1.md; PHASE2_P2_NOTES §31; LITERATURE_CHECK.md sixth pass.

**Why it exists.** Egress to arXiv opened after six legs. `bash Papers/fetch.sh` pulled
14/14 on the first attempt (the PDFs stay gitignored — re-run it, it takes ~30 s). Five
prose literature passes had produced zero durable facts, so the deliverable here is
deliberately code: nine gates that each re-derive a published number from the published
equations and compare it to ours.

**What a human should notice.** Three things.

(1) **The leg's job was to check one claim and the valuable thing came from elsewhere.**
I read arXiv:2207.07548 to see whether it pre-empts `s_c = α/2`. It does not — its §8
leaves the question open, and the actual pre-emption is arXiv:2607.19762 §6.1, which the
manifest had filed as a *spectral* paper. But §5.1 of the first paper turned out to
contain the thing no leg of this project had: what the self-similar exponents are ABOVE
criticality. Banked as lesson (69).

(2) **The first refusal predicate in J3 was wrong and passed.** I gated `τ` and the
deepest "resolved" rung read `c_l = 0.222` against an exact `1/3`, while the middle of the
ladder read `0.33333`. The local exponent is a difference quotient, so the thing that must
stay resolvable is `dτ`; `τ` at the bad rungs was `1e-11`, nowhere near underflow, so no
threshold on `τ` could have caught it. Panel C now draws the refused branch instead of
truncating the axis. Lesson (67).

(3) **Four numbers in the drafted prose did not match the regenerated JSON** and were
caught by re-reading the artifact rather than the draft — two residuals, the refused-rung
count, and `dlogΩ/dlogv_c` (`-2.00012` from a test run vs `-2.000144` in the committed
artifact). The process rule keeps paying.

**What it cost.** Seven of twelve standing claims. Nothing was found to be *wrong* —
what changed is who found it first.

## Phase-2 P2 — ROUTE-I v1: the marginal flow driven, and the NaN in the figure (non-logged) — 2026-08-03

**NOT a logged gate run** (deterministic; ~5 min). Code `solver/marginal_flow.py` +
`test_marginal_flow.py` (11/11); `experiments/p2_route_i_v1_driven.py` →
`writeup/data/p2_route_i_v1_driven.json` → fig38. Writeups
TECHNICAL/BLOG_P2_ROUTEI_V1.md; PHASE2_P2_NOTES §30.

What a human would want to know:

- **The leg was written before it was checked, and checking it is most of this entry.**
  The code, driver, data, figure script and both writeups already existed when I picked
  it up. The gate suite passed 10/10, which is why the headline survives intact. What did
  not survive was a sub-measurement and several writeup numbers — and finding those was
  worth more than the leg's arithmetic.

- **The headline, which is real.** The INVISCID rescaled fixed point at a = 1/2 has
  141 of 144 unstable directions (max Re +4.56) — §26's essential spectrum as a count, so
  nothing generic reaches it. Any μ > 0 has NONE. And the unstable directions are the
  log-periodic ones (leading eigenvalue +4.55 + 430i, Re rising with |Im|, max|Im| growing
  with K) — i.e. exactly the DSS-shaped modes, which μ deletes rather than damps. Third
  independent reason the cheap DSS entrances do not work.

- **THE FIGURE SAID `α₁ = nan`, THREE TIMES, AND I HAD ALREADY LOOKED AT IT.** Every
  off-branch run overflowed. The integrator's Newton has a stagnation stop that returns
  the unconverged iterate; nothing checked; the driver stored it; the legend rendered it.
  I read past it once. The lesson I want to keep is not "add a check" — it is that a
  rendered artifact is not a verification, and I treated looking at the picture as if it
  were.

- **Finiteness was not the right predicate either, which cost a second attempt.** After a
  partial fix the same run stayed finite and ended at μ = −1.6e24. The discriminator that
  actually separates healthy from broken is the implicit solve's own residual over its
  floor: ~6e2 versus 1e13. Four orders of clean separation, and it was already being
  recorded — just never read.

- **The cause was "small in the wrong norm", and it is the most transferable thing here.**
  The perturbation was normalized to max|v_k| = 1. But the gauge divides by
  (Λ^p Ω)_X(0), which weights mode k by ~k⁴, so that "1e−3" was 3.6e8 too large in the
  functional that binds: α came back 11713 instead of 3.037 at τ = 0, before a step. Same
  k^p amplification Route-H found killing Λ⁵. One mechanism, two legs, two symptoms.

- **And the fix made the result weaker, which is the honest part.** Normalized correctly,
  the largest "5%" perturbation is a 5e−11 change in the profile. So the off-branch test
  probes the gauge-sensitive direction and is a WEAK test of profile robustness — not the
  basin measurement it reads like. I wrote that into the technical note, the blog and the
  figure legend rather than letting "off-branch starts join the same law" stand.

- **Three writeup claims did not match the regenerated data.** §2 quoted the p = 5 rung
  (+2.007) as a measurement when the driver REFUSES it on operator truncation 1.77 — and
  it is the closest-agreeing rung in the table, which is precisely why the gate is on the
  operator and not the answer. §2 also quoted all three a = 0.3 rungs as a passing
  off-resonance control; every one is refused on an unresolved profile, so the leg has NO
  off-resonance control. §5 reported μ = 1e−3 as "≈ −1.0, <1%" when it is −1.81 against a
  gap of −1.00, 81% out. That number was never in the data — it was written from what the
  eigenvalue said it should be. All three are corrected.

- **What I trimmed from the claim.** The crossover μ*(K) falls ×10 from K = 48→96 (against
  a predicted ×8) but ×1.0 from 96→144, where the prediction is only ×3 — below the
  decade-spaced ladder's resolution. The first step carries the claim; the second is
  consistent and NOT independent evidence. The writeup said "μ* falls like K^-p" flatly.


## Phase-2 P2 — ROUTE-H v1: the marginal case, where scaling says nothing (non-logged) — 2026-08-03

**NOT a logged gate run** (deterministic; no GA, no seeds; ~10 min). Code
`solver/critical_dissipation.py` + `test_critical_dissipation.py` (10/10);
`experiments/p2_route_h_v1_critical.py` → `writeup/data/p2_route_h_v1_critical.json` →
fig37. Writeups TECHNICAL/BLOG_P2_ROUTEH_V1.md; PHASE2_P2_NOTES §29 (and §28, the
Route-G section that had been missing from the notes, added at the same time).

What a human would want to know:

- **Why bother with the case where the argument gives nothing.** Routes F and G both
  ended on "at s = s_c the two terms balance identically, so this returns zero
  information", and both filed it as a caveat. It isn't a caveat — β = 1/2 for NS makes
  s_c = 1 exactly, so the marginal point IS Navier–Stokes. The whole leg is the
  observation that a caveat repeated twice was the subject.

- **The one idea: μ is a coordinate, not a nuisance parameter.** Keeping the dissipative
  term through the dynamic rescaling gives μ_τ = (2s − α)μ. That single extra equation
  turns Route-F's fitted threshold into an eigenvalue, and makes the marginal case a
  normal-form question with one coefficient, α₁ = dα/dμ. Only the SIGN matters.

- **The a = 0 gate is unusually strong and I want to say why.** Complexification gives an
  exact viscous blow-up in elementary functions. The numerics do not know it: they solve
  the rescaled system with a re-derived gauge at μ = 4, where the dissipative term is four
  times everything else, and land on the closed form to 1e−15 with α = 1.00000000000000
  at every μ. "Build the same object twice" with a genuinely independent second build.

- **Two refusals, and they are the load-bearing part of the leg.**
  (a) THE CHORD IS NOT THE DERIVATIVE. Fitting α against μ over any finite window
  returns the chord — 0.1264 against the true 0.1337, 5.5% wrong in the one number the
  verdict is quoted from. Fixed by extrapolating the secants.
  (b) THE THIRD POINT WOULD HAVE SHIPPED A SIGN FLIP. At K = 288 it converges to a
  respectable 1e−4 and returns α₁ = −0.0017 — the opposite verdict to a = 1/2, and a
  headline. It is not a measurement: the whole excursion of α across the μ-window is
  2.0e−5, a factor of 19 BELOW the residual. Refusing on the residual alone would not have
  caught it. The predicate is now "is there signal above the solve error", it is unit
  tested against those exact numbers, and this is the thing I would most want a reader
  of this leg to take away.

- **I overstated the "lucky alignment" in my own module docstring and H4 caught it.**
  Landing on an odd-integer α makes Λ^{2s} a FINITE matrix; I wrote that as if it made the
  composite ACCURATE. Λ^p weights mode k by k^p, so it amplifies precisely the coefficients
  the single final truncation throws away — worst truncation ratio 1.7e4 at K = 192, 1.5e3 at
  K = 288. It does fall (~K^−4) but starts so high that trustworthy Λ^5 needs K ~ 3000.
  Corrected in place rather than quietly dropped.

- **The most interesting result is a negative that got BETTER.** Route-E shut the DSS lane
  with a mechanism: the spectrum is a continuum, and a continuum has no eigenvalue to move.
  Dissipation removes that mechanism — converged eigenvalues go 2 → 8 and condense onto the
  negative integers. And the lane stays shut anyway, because everything that condenses lands
  on the negative real axis (max Re = 3e−13) and nothing goes complex. That is a strictly
  better position than before: the negative now rests on a measurement with a working
  positive control (6 → 9 converged, one at Re = +1.58) rather than on there being nothing
  to measure.

- **A boolean lied to me and I changed the instrument.** "Any complex converged
  eigenvalues?" returned True — for a degenerate real pair at Re = −3 split by |Im| =
  1.8e−5. The driver now reports the largest |Im| instead. General form: for anything you
  are claiming the ABSENCE of, report a magnitude, never a boolean.

- **What it costs to be right at criticality.** α₁ > 0 means μ decays, so the critical
  viscous solution does relax onto the inviscid profile — but algebraically, 1/(α₁τ).
  μ: 0.2 → 0.02 costs τ = 337; one more decade costs τ = 3703; and τ is itself logarithmic
  in (T−t). Criticality is not a wall, it is a tar pit. That texture is the part I would
  actually carry over to thinking about NS, and it is not a theorem about anything.


## Phase-2 P2 — ADVECTION SCOPE: the space was tuned where the hard term vanishes (non-logged) — 2026-08-03

**NOT a logged gate run** (deterministic; no GA, no seeds). Code
`solver/advection_scope.py` + `test_advection_scope.py` (6/6). Writeups
TECHNICAL/BLOG_P2_ADVECTION_SCOPE.md; PHASE2_P2_NOTES §A. No figure and no JSON —
the numbers are reproduced by running the gates, and a plot of two log-slopes would
add nothing to a table.

What a human would want to know:

- **The shape of the mistake, because it is the transferable part.** Eleven legs
  gated everything against the a=0 known answer, which is correct practice and a
  banked lesson. But a=0 is exactly where the advection term is ABSENT. So the space
  was chosen, tuned, priced and optimised on the one member of the family where the
  term it would have to carry does not exist. The general form: a known answer is a
  SPECIAL case, and what makes it tractable is often what makes it unrepresentative.

- **The finding.** U = ∫H(Ω) inherits v3's far-field law and grows like (M/π)log X,
  with no cancellation available since M ≠ 0 for everything in the family. So the
  transport piece of DF comes back multiplied by a logarithm and leaves the
  decay-graded codomain for every a ≠ 0. Measured +0.317 against a predicted +0.318.
  Eleven legs of bounds are a=0-only, and nobody had said so.

- **Half my own measurement was noise.** I nearly reported both advection pieces.
  The stretch piece carries Ω_X, whose far field for a≠0 sits at the discretization
  noise floor — a log-rate fit there measures amplified dust. Magnitude cannot
  separate them; REPRODUCIBILITY can. Grid-spread 0.4%/2.6% for transport against
  5%/99% for stretch. The gate now tests that discriminator rather than trusting me.

- **The fix was already in the building.** The one-scale (self-similar) residual
  balances against c_l X Ω_X instead of c Ω_X, so its codomain grading is one power
  weaker — exactly what absorbs a log. Same profile, same h, same grid: +0.317 →
  −0.010. So the leg's output is a redirect, not a dead end.

- **I was wrong about the crossing, in a way worth recording.** c+aU changes sign at
  a grid-stable radius and I wrote it up as a stagnation point. A parallel line had
  already read it better: it is the EDGE OF SUPPORT. Their reading explains what mine
  did not — the profile is ~1e-9 by X~10 while the crossing is at 7.16, so there is
  no tail out there to have a sign. My gates survived only because they were written
  to depend on the reproducible half; that was habit paying off rather than foresight.

- **Honest ceiling.** Plain float64. Moves no link of the Clay chain; it is a cost
  finding that narrows an L1 sub-programme and names the repair. Its value is timing:
  three more bound-sharpening legs were queued on the assumption the space works.

## Phase-2 P2 — ROUTE-F v1: the number that says why NS is hard (non-logged) — 2026-08-02

**NOT a logged gate run** (deterministic). Data `writeup/data/p2_route_f_v1_viscosity.json`
(regen `python -u experiments/p2_route_f_v1_viscosity.py`, ~6 min); figure fig35; writeups
TECHNICAL/BLOG_P2_ROUTEF_V1; PHASE2_P2_NOTES.md §27. Code `solver/fractional_gclm.py` +
`test_fractional_gclm.py` (6/6; suite 24 files green).

What a human would want to know:

- **Everyone writes "any real proof has to beat viscosity at small scales" and nobody makes it
  quantitative.** This leg does, in a model where the arithmetic is checkable. Three lines of
  scaling give `s_c = α/2`: the critical dissipation exponent is HALF the profile's far-field
  decay exponent. The rate at which the profile decays in *space* decides whether the blow-up
  beats dissipation in *time*.

- **And it reuses the previous leg's by-product.** `α` was measured in Route-E v1 while asking
  a completely different question. I did not build it for this.

- **The NS reading is the point.** NS's natural scaling is `β = 1/2`, i.e. `α = 2`, i.e.
  `s_c = 1` — exactly the ordinary Laplacian. NS sits precisely on the line where neither term
  wins, which is what "critical" means and why every scaling argument about NS returns zero
  information. In gCLM `α` is a dial, so the family *walks through* the point where NS is stuck.
  That is the toy's value here — not that it blows up, but that it is off-critical in a
  controlled way.

- **I refused to run the obvious experiment.** Sweeping `s` and looking for where blow-up stops
  is biased, resolution-dependent, and biased in the direction I expect: three ways to fool
  myself in one measurement. Fitting `D/N ~ (T−t)^p` against `p = 1 − 2s/α` predicts a whole
  LINE instead, whose slope, intercept and zero are separately checkable.

- **The cross-check is the part I'd keep if I could keep one thing.** `α` comes from a steady
  compactified spectral solve on the LINE; `dp/ds` comes from time-dependent pseudo-spectral
  simulation on a PERIODIC domain with dissipation. No shared grid, basis, formulation or fitted
  constant. Ratio to the prediction: 1.042 / 1.014 / 1.016 / 1.017 at a = 0/0.2/0.3/0.4 —
  **1.022 ± 0.014 while α itself doubles.** A uniform 2% bias, not an a-dependent failure.
  Refining one computation can't test the other; agreement across two tests both.

- **The error bar is the fit window, and I swept it rather than picking one.** `p` is asymptotic,
  so early windows haven't got there and late ones are noise. Slope −2.02 ± 0.09 (predicted −2),
  `s_c` 0.51 ± 0.05 (predicted 0.5). Single exponents move ±0.07 and approach the prediction
  monotonically from above — which is what entering an asymptotic regime looks like, and is why
  the claims are about the slope and the zero rather than any one number.

- **One control passes only weakly and I said so.** The prediction has no `ν` in it, but the
  slope moves −1.866 / −2.051 / −2.110 over three decades of `ν`. −2 is inside the range and the
  middle decade is within 2.6%, but that is not a tight control; the two ends stress the
  asymptotic argument from opposite sides. It is the thing to tighten if this is ever revisited.

- **Three attempts at the resolution guard, and the first two were silently degenerate.** Energy
  above ⅔ of `k_max` reads exactly 0.0 at some grid sizes because the dealiasing already zeroed
  that band — a guard that is zero by construction reads as "perfectly resolved". Energy above
  `n/6` reads ~0.37 for every run because a near-singular spectrum genuinely is fat. What works
  is the amplitude AT the cutoff relative to the peak. The run now refuses rather than returning
  a number off an unresolved state.

- **The sentence I was careful with.** `s_c` crosses 1 at `a ≈ 0.383`, so above that the scaling
  says the blow-up beats ordinary viscosity. That is arithmetic about gCLM's own scaling. It is
  NOT a statement about NS, and it does NOT say a viscous gCLM blow-up exists there — the scaling
  says which term dominates *given* the self-similar form, and showing a solution reaches it is
  the entire difficulty. What the map is good for is orientation.

## Phase-2 P2 — ROUTE-E v1: looking for the door that isn't there (non-logged) — 2026-08-02

**NOT a logged gate run** (deterministic). Data `writeup/data/p2_route_e_v1_spectrum.json`
(regen `python -u experiments/p2_route_e_v1_spectrum.py`, ~35 min); figure fig34; writeups
TECHNICAL/BLOG_P2_ROUTEE_V1; PHASE2_P2_NOTES.md §26. Code `solver/rescaled_spectrum.py` +
`test_rescaled_spectrum.py` (8/8; suite 23 files green).

What a human would want to know:

- **First leg of a new lane, and a negative.** §24 said L1 is occupied and moved the swing to
  DSS. A DSS blow-up is a periodic orbit of the rescaled flow, so the cheapest way one could
  exist near what we already have is a Hopf bifurcation off the self-similar fixed point. There
  is no eigenvalue that could do it.

- **I wrote down two of the eigenvalues before computing anything, and that paid twice.** They
  follow in five lines from the flow's symmetries (dilation → 0, amplitude → −1, at every `a`).
  Once because the filter's "exactly two" then read immediately as "nothing but symmetry"
  instead of looking like a result. And once for a reason I did not anticipate: `λ = 0` is
  *exactly* right, so its computed value is a **free error bar on the whole spectrum** — 0.35 at
  `a = 0.2`, 8.9e−5 at `a = 1/2`. That number is what decided which rows of the sweep were
  allowed to carry a conclusion, and without it I would have reported the dilation mode
  "moving" with `a` when it was pure discretization error.

- **The compactification is startlingly good for this object.** `X = tan(θ/2)`, odd sines: `H`,
  `d/dX` and — the one that matters — the dilation term `X d/dX = sin θ ∂_θ` are all exact, and
  the velocity is exact too through a recursion whose `1 + cos t` denominator cancels
  identically. The CLM self-similar profile is then literally `Ω = −sin θ`, residual 1.1e−16.
  Sixteen Route-D legs used this variable for the *traveling-wave* object; nobody had put the
  *dilation* anchor in it.

- **A gauge the project had been carrying is wrong for `a ≠ 0`.** `c_ω = 1 − HΩ(0)` is right at
  `a = 0` and was used at every `a`. Differentiate the residual at the origin: for `a ≠ 0` it is
  nonzero, so that flow has *no fixed point at all*. Repair forced, not chosen.

- **The mechanism is nicer than the verdict.** At `a = 0` the linearization is exactly solvable
  and its continuum is `(w−1)^{1−λ}(w+1)^{1+λ}` on `−1 < Re λ < 1`. The purely imaginary members
  are `X^{1−iy} e^{iyτ}` — a wave travelling outward in log X, exactly τ-periodic. **The
  log-periodic structure a DSS solution is made of IS in this operator.** It is continuous
  spectrum, not a bound state, and a continuum has no eigenvalue to move. That is *why* there is
  no Hopf.

- **I got two things wrong in this leg and caught both. They are the useful part.**
  (i) The filter kept a third eigenvalue at `a = 1/2` near −2, and a K-ladder made it look
  *better* (−2.0073 → −2.0017 → −2.0005 → −1.999999). Six digits of grid-convergence. It is the
  **left edge of the essential spectrum**, `c_ω + 1` — and the control that settles it was free:
  at `a = 0` that identical edge sits at 0 and carries 99% of the discretized spectrum. Nobody
  would call that an eigenvalue. Tightening the filter would have made the artefact *more*
  convincing.
  (ii) I hypothesised "α odd integer ⇒ analytic" from the only two special points I had, went
  and found the third (α = 5 at a = 0.5821792673), read the first two rungs of its ladder as
  algebraic, **wrote the rule off as false and committed that**. Four more rungs: the implied
  order climbs 3.6 → 6.5 → 11.5 → 15.4 → 19.7, which is exponential convergence that had not
  settled. The rule holds. I had literally just written a lesson about not fitting a rule to two
  points, and then fitted a rate to two rungs.

- **Two by-products.** `α(a)` is an output that runs away (branch lost at `a = 0.65`, `1/α → 0`
  at `a ≈ 0.694`). And `α = 3` lands at exactly `a = 1/2` — twelve digits — while `α = 5` lands
  at 0.5821792673, which is not a special number. So the odd-α rule explains why those `a` are
  analytic but not why one of them is a round rational. Novelty unchecked; PDF access still
  blocked, three legs running.

- **The third a = 1/2 sighting, and I am not building on it.** v16 found `sup|N''|` finite
  exactly for `a ≤ 1/2`; the GA's survival boundary is `a* ≈ 0.5–0.55`; now `α(1/2) = 3`. All
  different objects. v12 had a similar coincidence, ran the `a = 1/3` control, and the control
  killed it. No control run here, so it stays a written-down coincidence.

- **Said alongside the verdict, not buried:** the flow is *not* spectrally stable. Its essential
  spectrum reaches `+1` at `a = 0` and `+5` at `a = 1/2`, complex members included. Those are
  the directions with a corner at the origin. It is norm-dependent, it is the familiar
  low-regularity essential instability of self-similar linearizations, and it is still not
  something that can Hopf-bifurcate.

## Phase-2 P2 — ROUTE-D v16: the wall I removed was not the only wall (non-logged) — 2026-08-01

**NOT a logged gate run** (deterministic). Data `writeup/data/p2_route_d_v16_rehearsal.json`
(regen `python -u experiments/p2_route_d_v16_rehearsal.py`, ~5 min); figure fig33; writeups
TECHNICAL/BLOG_P2_ROUTED_V16; PHASE2_P2_NOTES.md §25. Code `solver/reduced_certificate.py` +
`test_reduced_certificate.py` (16/16; suite 22 files green).

What a human would want to know:

- **Framing first: this is a capability build, not a result.** v15's literature check said the
  lane is occupied, so the certificate got demoted to "do the float rehearsal, find out whether
  the pipeline closes, stop". It doesn't close, and the reason is worth more than a yes.

- **Y₀ is finally the number a certificate needs.** 1.5e−12 at K=96, against a GA floor of 1e−2
  that this project carried for five legs and an anchor-priced 2.4e−4 that was wrong anyway.
  The nodal residual sits in the table as the control — flat at 1e−14 by construction — because
  without it the top row could be measuring the grid.

- **I nearly got the main result right for the wrong reason.** The quick probe (one high
  Chebyshev mode through the Hilbert transform) showed a divergence. The adversary (step partial
  sums) showed a divergence. Two independent-looking confirmations. Refine the quadrature
  fourfold and the quick probe collapses to 0.999 flat while the adversary doesn't move at all.
  One was the operator, one was my integrator, and they pointed the same way. Both rows are in
  the figure.

- **The thing I had quietly assumed was wrong.** Leg 14 removed the far field and I carried an
  unexamined belief that this dealt with the smoothness requirement too. It didn't and couldn't:
  the Hilbert transform's unboundedness on sup is about a *jump*, not about infinity. What the
  far-field removal killed was the decay grading. So legs 5–9's Hölder apparatus isn't wasted —
  its bounded-interval version is the next brick, and it's the cheap half.

- **There is a coincidence at a = 1/2 and I am leaving it as a coincidence.** The quadratic
  constant is finite exactly for a ≤ 1/2, which is exactly where the profile loses C², and the
  project's independently measured survival boundary is a* ≈ 0.5–0.55. Leg 14 solves the
  profile cleanly to a = 1.2, so this is my *norm* failing, not the equation — and a weight
  fixes it. Leg 12 had a similar coincidence at the same boundary, wrote it down, ran a control,
  and the control killed it. I haven't run a control, so it stays written down.

- **Z₁ I didn't compute at all**, and the code returns it as `None` rather than zero and refuses
  to assemble a budget. That's the whole content of a real computer-assisted proof and it isn't
  a chunk of work.

## Phase-2 P2 — ROUTE-D v15: I finally looked it up (no experiment) — 2026-08-01

**Not an experiment at all.** No code, no figure, no measurement. Data
`writeup/data/p2_literature_scope.json` (leads with explicit confidence levels and
must-verify lists); writeups TECHNICAL/BLOG_P2_LITERATURE_SCOPE; PHASE2_P2_NOTES.md §24.

What a human would want to know:

- **I could not read a single paper.** The container's network policy blocks arxiv.org and
  every publisher domain I tried — 403 at the proxy's CONNECT, before the request is even
  made. Web *search* works. So the whole leg is titles, abstracts and search-engine
  paraphrase, and everything in it is a lead rather than a fact. I wrote it down anyway,
  with the confidence levels attached, because the alternative was to keep building.

- **The object I have been building a certificate for appears to already have an existence
  proof.** A March 2026 preprint (Huang, Tong, Wang) says in its abstract that the two-scale
  blowup's inner traveling wave — my object — has its existence established rigorously via a
  fixed-point method. And a 2023 paper by the same group proves existence of compactly
  supported profiles in this family via a fixed point of an explicit nonlinear map. So leg
  12's "the profile ends" was a rediscovery, and leg 14's first integral is very likely the
  reduction their fixed point is built on.

- **The part that actually changes the plan is duller and bigger:** computer-assisted proofs
  with interval arithmetic and Newton–Kantorovich are *routine* in this exact family. My L1
  milestone — certify a 1D toy-model profile — is what these groups do as a matter of course.
  Finishing it is a capability demonstration and a reproduction. My own priority list said
  that in a bullet I had been ignoring for five legs.

- **One sentence in that March abstract worries me more than the novelty question.** It seems
  to place the two-scale scenario at *non-positive* advection parameter, with positive
  parameters giving one-scale profiles. I have worked the two-scale object at positive
  parameter throughout. If that reading is right, the question isn't whether my object is
  new — it's whether it's the right object. That is the single highest-value thing to verify
  and it is also the least verified thing in the file.

- **So the binding constraint on this project's next decision is access, not compute.** The
  cheapest decisive act available is "open one PDF", and I can't. Worth stating plainly
  rather than routing around.

- **I logged an extraordinary claim deliberately, marked do-not-use.** An April 2026
  single-author preprint claims stable finite-time singularity for 3D Navier–Stokes with a
  computer-assisted validation. It is in the data file flagged "do not repeat as a result",
  purely so a future session doesn't find it independently and lose a day. I am in no
  position to check it and a solo preprint claiming a Clay problem is almost certainly wrong.

- **Being second is not being wrong.** Every measurement from v3–v14 stands. What changed is
  what the next leg is worth, and it changed for reasons outside the work.

## Phase-2 P2 — ROUTE-D v14: the equation integrates once (non-logged) — 2026-08-01

**NOT a logged gate run** (deterministic). Data `writeup/data/p2_route_d_v14_first_integral.json`
(regen `python -u experiments/p2_route_d_v14_first_integral.py`, ~6 min); figure fig32
(`writeup/4_p2_lottery/p2_route_d_v14_evidence.py`); writeups TECHNICAL/BLOG_P2_ROUTED_V14;
PHASE2_P2_NOTES.md §23. Code: `solver/first_integral.py` + `test_first_integral.py` (11/11;
suite now 21 files green).

What a human would want to know:

- **The leg was supposed to be a build, and the build turned out to be two lines of algebra.**
  The instruction from v13 was "pose the problem on the profile's own support and measure the
  operator norm". Setting that up meant writing down the equation carefully, and written
  carefully it integrates: `E = c + aU` has `E' = aH(Ω)` *by definition*, which is the
  equation's own nonlinearity, so the whole thing is `(log|Ω|)' = (1/a)(log E)'`. Thirteen
  legs of space design, adversary construction and constant-pricing were spent on an equation
  with a closed-form first integral. The ingredient had been sitting in the notes since v12.

- **The check that made me believe it took one minute.** Let `a → 0` and the formula
  degenerates to `Ω = −exp(U/c)`, which on the anchor is `−1/(1+X²)` — the exact solution the
  project has been anchored on since the start. Agreement `1.1e−16`. If a claimed identity
  contains your known-answer gate as a limit, you are probably not wrong.

- **The kill switch passes, and I nearly measured the control wrong.** First pass I compared
  the reduced system's flat norm against an *unweighted* whole-line ladder — which diverges
  like `J^+0.99` even at the anchor, purely because the grid's outer radius grows with `J`.
  That would have been a manufactured contrast. Re-ran the control through v13's own
  `graded_norm_by_radius` at the same grading: `J^−0.004` at the anchor, `J^+2.800` at
  `a=0.2`, reproducing v12. Then re-ran the *reduced* ladder under that same grading too, in
  case "flat" was an artifact of a convenient norm. It isn't, and it can't be — on a bounded
  interval those weights are equivalent, which is the whole reason the old measurement had to
  be weighted.

- **The repair cost a banked result.** v11's grid-refinement argument that the solutions stop
  being continuum objects past `a ≈ 0.5` was banked as a fourth confirmation of the survival
  boundary. On its own support the same object is converged to 8–12 digits at `a` up to 1.2.
  The spread v11 saw was the global basis failing on a compactly supported profile whose edge
  regularity *degrades* as `a` grows. That retires the argument, not the boundary — the other
  three confirmations are about a different question — but the count is three now, not four.

- **Still not a certificate, and I want that said plainly.** None of `Y₀, Z₀, Z₁, Z₂` exist in
  the new space. `‖A‖` converging means the approximate inverse exists in the limit; it says
  nothing about the budget closing. And `4.52` is not "better than" v7–v9's `47` — different
  operator, different space; the comparable thing is the slope.

- **Novelty unchecked, and it should bother the reader as much as it bothers me.** A first
  integral of a scalar traveling-wave equation is exactly the kind of thing that is folklore
  to people who do gCLM/De Gregorio professionally. The literature search is the standing
  cheap item and it blocks this claim like it blocks the others.

## Phase-2 P2 — ROUTE-D v13: I had the sign wrong (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic). Data `writeup/data/p2_route_d_v13_turning.json`
(regen `python -u experiments/p2_route_d_v13_turning.py`, ~6 min); figure fig31
(`writeup/4_p2_lottery/p2_route_d_v13_evidence.py`); writeups TECHNICAL/BLOG_P2_ROUTED_V13;
PHASE2_P2_NOTES.md §22. Code: `solver/turning_point.py` + `test_turning_point.py` (6/6;
suite now 20 files green).

What a human would want to know:

- **This leg exists because the previous one explained its own result wrongly.** v12's
  measurements were gated six ways. The sentence explaining them — "linearizing about a
  zero of order p gives a mode blowing up like s^{−p}" — was not gated at all, and it is
  wrong: I dropped a sign converting d/dX into d/ds. The mode at the critical radius
  *vanishes*. Fitting the exponent it predicts takes ten minutes and is now a test.

- **The real obstruction is worse than the one I claimed.** Outside the critical radius the
  same equation gives a mode growing like (log X)^{1/a}, against a domain space that is a
  decay class. A local singularity would have been a resolution problem; this is a range
  obstruction, and no grid touches it.

- **The prediction is unusually clean.** 4.9988 / 3.9980 / 3.3307 / 2.8536 / 2.4855 against
  1/a = 5 / 4 / 3.3333 / 2.8571 / 2.5, from an instrument that never touches the matrix
  whose norm was diverging. That is the third role 1/a plays in this problem.

- **The outlier.** a = 0.5 came back at 0.054 instead of 2 — exactly the kind of point one
  is tempted to drop with a footnote. Refining: 0.054 → 1.84 → 1.70, while a = 0.4 sits at
  2.4855 → 2.5035 → 2.5014. v12 had already reported the profile stops converging there.
  The outlier is the instrument, and it is in the figure with that label on it.

- **Attribution beat argument again.** "The divergence is the far field" was a story until
  the domain sup was restricted to a fixed radius, at which point the slope fell from
  J^+2.86 to J^+0.31 while the a = 0 control stayed flat at every cutoff. The same ladder
  produced the part the story does *not* explain — a residual J^+0.3 at fixed radius — which
  is in the writeup as unattributed rather than rounded to zero.

- **The repair I recommended last time is dead, and cheaply.** Bordering with the speed
  cannot supply a range direction because the speed is tied to a symmetry — a fact already
  recorded twice in these notes. The square bordered system at the anchor has condition
  number 4e18. Three minutes to check.

- **Next.** Not a bordering trick: take the far field out of the domain. [0, X_c] with X_c
  an unknown. Kill switch unchanged — build it at one a, refine, watch the norm.

## Phase-2 P2 — ROUTE-D v12: the profile ends (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic Newton + deterministic sweeps; no GA, no seeds,
no predicate lock). Data `writeup/data/p2_route_d_v12_defect.json` (regen
`python -u experiments/p2_route_d_v12_defect.py`, ~13 min); figure fig30
(`writeup/4_p2_lottery/p2_route_d_v12_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V12; PHASE2_P2_NOTES.md §21. Code:
`solver/collocation_newton.py` + `test_collocation_newton.py` (6/6; suite now 19 files green).

What a human would want to know:

- **The leg I meant to run.** v11 measured the profile's defect on the sinh-ρ grid; every
  Route-D bound lives in the compactified θ-collocation basis. Carry it across, measure Y₀
  there. That is a two-hour job and it was done by lunchtime.

- **The measurement misbehaved in two ways at once**, which is what actually produced the
  leg. The weighted defect was NOT monotone in a (4.4e-4, then 8.4e-6, then 4.4e-5), and its
  arg-max was the outermost point of the domain — at every single value of a. Either one
  alone is a shrug. Together they say you are not looking at what you think you are.

- **What it was.** The transport coefficient in this equation is not c, it is E = c + aU,
  and U is an integral of a Hilbert transform, so it carries a logarithm and decreases
  without bound. E hits zero at a finite radius. Past that radius the profile does not decay,
  it ENDS: Ω ~ (X_c − X)^{1/a} approaching it, and Ω ≡ 0 solves the equation beyond it. The
  a = 0 anchor — where all eleven legs of far-field analysis were done — is the one case
  where this cannot happen, because there E ≡ c is constant.

- **The half hour where it looked like the best news in months.** At a = 0.2, J = 1600, the
  defect came in 7.7× UNDER budget — the first time this side of the inequality has been
  under target at a ≠ 0. Then: the budget's constants were all computed at the anchor. I
  measured ‖A‖ at the actual profiles and it is 2.1e3 rather than 20.94 — and the J-ladder
  says it DIVERGES (J^+2.86) while the anchor's is flat (J^−0.003). Correcting the budget
  turns 7.7× under into three orders over. Both sides of the inequality move the wrong way,
  by one mechanism.

- **What stopped the over-claim, twice.** (i) The a = 0 control: the exact anchor's defect in
  the same norm is 3.7e-11, nine orders below anything reported, so the numbers are the
  object and not the instrument. (ii) The J-ladder on ‖A‖: a single grid size cannot tell a
  large operator from a bad grid, and this project has now been burnt by that twice (v6's
  discrete-ball trap, v10's sign-pattern baseline). One extra loop, three minutes.

- **The one I wanted to be true and wasn't.** The zero's order is 1/a, which hits the integer
  2 exactly at a = 1/2 — the four-times-confirmed survival boundary — and the Hilbert
  transform of (X_c−X)^p_+ grows a log at integer p. That is a sharp mechanism landing exactly
  on the observed boundary. It also predicts trouble at a = 1/3, and there is none: that
  point is smooth in every column. So it is a coincidence, and v12 does not predict a*.

- **Next.** Beyond X_c the profile is exactly zero, so the certificate can move to the finite
  interval [0, X_c] with X_c as an unknown, and the whole far field disappears. The
  singularity at X_c should be absorbed by the free boundary (the singular mode is ∂/∂X_c of
  the solution family). Untested; the kill switch is ‖A‖ vs J in that formulation.

## Phase-2 P2 — ROUTE-D v11: Newton on the profile, and the number we carried for five legs (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic Newton; no GA, no seeds, no predicate lock).
Data `writeup/data/p2_route_d_v11_anchor.json` (regen
`python experiments/p2_route_d_v11_anchor.py`); figure fig29
(`writeup/4_p2_lottery/p2_route_d_v11_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V11; PHASE2_P2_NOTES.md §20. Code:
`solver/profile_newton.py` + `test_profile_newton.py` (6/6; suite now 18 files green).

What a human would want to know:

- **Why this leg instead of another constant.** v10 measured the ceiling on sharpening:
  a perfect ‖A‖ buys 7.7×, C_Q's slack is ~4×, and the two together only just reach the
  1e-2 residual floor with nothing spare for the three open Z₁ items. That is the point
  at which you stop polishing the left-hand side and look at the right. Y₀ enters the
  radii polynomial LINEARLY and had never been attacked in eleven legs.

- **The number we had been carrying as physics.** Every a≠0 profile in this project came
  from a GA over a small parametric genome or from fixed-grid dynamic relaxation, and both
  floor at ~1e-2. We had a banked discipline lesson saying exactly that — and §9 read it
  as a fact about the PROBLEM. Newton has no genome and no relaxation dynamics: it reaches
  **relres ~1e-14 at every a up to 0.5**. Twelve orders. The floor was the search.

- **The hour where it looked like a bigger result than it is.** Newton also converged at
  a = 0.8 and a = 1.0, which briefly read as "the survival boundary was a genome artifact
  all along" — a much louder claim, and wrong. Machine precision on a DISCRETE system
  proves nothing by itself; the test is whether the SOLUTION stops moving when you refine.
  Spread in c over n = 401/801/1601 is 8e-4 / 3e-4 / 3e-5 at a = 0 / 0.2 / 0.5 but
  3.7e-3 / 1.3e-2 at a = 0.8 / 1.0, with grids reaching machine precision 3/3/2/1/1. So
  the solutions are continuum objects up to a ≈ 0.5 and not beyond. **The GA's a*≈0.5–0.55
  is confirmed a fourth time, now by a method with no genome, no search budget and no
  stochasticity** — and sharpened, because below a* an exact discrete traveling wave
  demonstrably exists. One table stopped a correction from becoming an over-claim.

- **The known-answer gate has to be read the right way round.** At a = 0 Newton finds a
  zero of the DISCRETE system (1.1e-15) while the exact continuum anchor scores 7.7e-9 on
  those same equations — its own discretization error. A solver that reproduced the
  continuum profile exactly would be reporting something impossible.

- **What it actually does to Y₀: it changes the binding constraint, it does not solve it.**
  The certificate does not see the RMS; it sees the weighted sup defect
  sup(1+X²)^{(α+1)/2}|R₂|, and the codomain weight amplifies exactly the far field where
  the truncation error lives. That number is 6+ orders larger and NOT uniformly under
  budget: 2.3e-14 at a=0.1, but **1.5e-2 at a=0.45, against a 2.45e-4 budget**. So Y₀ is
  no longer SEARCH-limited, it is DISCRETIZATION-limited — which is already a ledger item
  (Z₁ core discretization, measured J^−2.1..−2.6 in v4 and never bounded). "Find a better
  profile" was the wrong problem; "control the far-field discretization of a profile we can
  now compute exactly" is the right one, and it is a question about a KNOWN object rather
  than about a search.

- **The lesson worth keeping.** A number that shows up in every measurement is the hardest
  instrument artifact to see. We had two independent tools agreeing on 1e-2 for five legs —
  and they agreed because they shared a weakness, not because they were right. Two tools
  are only a check if they fail differently.

- **Honest ceiling.** Plain float64; nothing interval-enclosed, nothing rigorous. This does
  not climb the rigor ladder — it moves one constraint from a place we could not attack to
  a place we already have a ledger item for. Clay odds unchanged (~0.05%).

## Phase-2 P2 — ROUTE-D v10: a lower bound worth reading, and the first measured ceiling (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic). Data `writeup/data/p2_route_d_v10_lower.json`
(regen `python experiments/p2_route_d_v10_lower.py`, ~20 min); figure fig28; writeups
TECHNICAL/BLOG_P2_ROUTED_V10; PHASE2_P2_NOTES.md §19. Code: `solver/op_lower.py` +
`test_op_lower.py` (6/6; suite now 17 files green).

What a human would want to know:

- **We had been quoting half a bracket for six legs.** Every lower bound on ‖A‖ in
  this project came from sign-pattern directions — exactly right if the space only
  measured size, and terrible here, because a sign pattern's Hölder seminorm is
  enormous and dividing by it discards what the numerator gained. The tell nobody
  had looked at: the baseline gets *worse* as the grid refines (0.973 → 0.921). It
  was never converging to anything about the operator.

- **What the ball actually contains.** Finite codomain norm forces a decay rate and
  forbids oscillation, so the family is that decay times a slowly varying shape.
  Validity is free — any g gives a lower bound — so the whole problem is
  construction, which is banked lesson 9 (build the adversary) pointed at the
  operator instead of the quadratic.

- **The winner is a wide bump in the far field** (X ≈ 90, half the domain wide),
  and nothing oscillatory is close. That is where v2's far-field degeneracy, v3's
  resonance and v6's matching radius all point, which is a small independent check
  that the number is about the problem rather than about the discretization.

- **The bracket that matters was never 50×.** At the reference point it falls
  50× → 16×. At the operating point — where the budget is actually evaluated, and
  has been for three legs — it is **2.74 ≤ ‖A‖ ≤ 20.94, a factor of 7.7**. Quoting
  the reference point's bracket was a second, quieter version of the same mistake.

- **The first measured ceiling on sharpening.** A perfect upper bound would move
  the budget 2.45e-4 → 1.88e-3 and no further: about 5× short of the residual floor
  rather than 40×. Better than it looked, and not enough alone — closing the gap
  also needs the quadratic constant's ~4×, and the two together only just reach the
  floor with nothing spare for the three open Z₁ items.

- **The rule this earns.** A bracket is two numbers and both have to be earned
  before any decision comes out of it. The cost of not doing that was a leg spent
  sharpening the wrong input and a phantom "19× available gain" that survived until
  someone checked the lower number.

## Phase-2 P2 — ROUTE-D v9: the sharpness leg, and the elasticity table that should have come first (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic; no GA, no seeds, no predicate lock). Data
`writeup/data/p2_route_d_v9_sharpen.json` (regen `python experiments/p2_route_d_v9_sharpen.py`,
~35 min); figure fig27 (`writeup/4_p2_lottery/p2_route_d_v9_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V9; PHASE2_P2_NOTES.md §18. Code: `solver/hilbert_pointwise.py` +
`test_nk_hilbert_pointwise.py` (6/6; suite now 16 files green).

What a human would want to know:

- **The leg did what it set out to do and it did not matter.** The bound on |H(h)|
  is the input the operator-norm closure feeds back through, and it was two legs
  old and built from textbook majorants. Rebuilding it on the exact folded kernel
  made it sharper at every point sampled — a factor of eleven near the origin, a
  third through the middle — and dropped ‖A‖ from 69.2 to 47.1, the largest single
  improvement since the closure was built. The certification budget went from
  2.39e-4 to 2.40e-4.

- **Why, in one line.** The closure raises the |H| input to the power γ, and the
  operating point sits at γ = 0.15. Gain by point: 32% at (1.5,0.5), 11% at
  (1.4,0.35), 3% at (1.4,0.25), 0% at (1.4,0.15). The rightmost is where the map's
  optimum has been for three legs. And it is there *because* small γ is where ‖A‖
  is cheap — which is the same thing as where ‖A‖ stops depending on this input.
  The optimiser had already walked to the corner where my improvement cannot
  matter.

- **The table that costs a minute.** Scale each input, fit the slope:
  d log‖A‖/d log C_sup = +1.00 at the operating point, d log‖A‖/d log|H| = +0.11.
  The last two legs both worked on inputs with elasticity ≤ 0.5 and both moved the
  budget by ≤ 7%. That is not luck. Nobody computed the table first, twice.

- **Something worth keeping anyway.** At each point of the integral the increment
  can be charged to smoothness or to decay, and any fixed rule gives a valid bound.
  The natural rule — take the smaller — is wrong here, and the general form is:
  tune the rule to the ratio of the two quantities *in the answer*, not to 1. In
  this closure the seminorm ends up ten times the sup part, so the neutral rule
  charges the expensive account; it comes out worse than the crude bound it was
  meant to replace. With the knob there is an interior optimum, and the two
  consumers of the bound want different values of it.

- **Banked lesson 15, missed again, in the place it warns about.** Asking how much
  is available from C_sup by substituting a measured value gave a 19× "available
  gain" that was an artifact — the measured value was a lower bound computed by
  dividing one part of a quantity by the full norm of a sign pattern. Having the
  lesson written down is not the same as applying it. What survives is smaller:
  ~2× is plausibly available from C_sup, and the wider bracket cannot be
  attributed at all until someone builds a decent lower bound.

- **What the next leg should be, decided by numbers.** C_sup is the only input
  left with elasticity ≈ 1 and has not been touched since v6 bounded it. But
  before that: a real lower bound on ‖A‖ (an LP over the polyhedral ball, or an
  actual adversary rather than sign patterns), because without one we cannot tell
  a lossy bound from a large truth, and every bracket in this project is currently
  uninterpretable in the same way.

## Phase-2 P2 — ROUTE-D v8: the codomain seminorm part of C_Q, and the first complete Z₂ (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic; no GA, no seeds, no predicate lock). Data
`writeup/data/p2_route_d_v8_quadratic.json` (regen `python experiments/p2_route_d_v8_quadratic.py`,
~12 min); figure fig26 (`writeup/4_p2_lottery/p2_route_d_v8_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V8; PHASE2_P2_NOTES.md §17. Code: `solver/hilbert_holder.py` +
`test_nk_hilbert_holder.py` (6/6; suite now 15 files green).

What a human would want to know:

- **The weight was the first thing to get right, and it is not the obvious one.** The
  natural guess is that H(h) should be measured with the same decay weight as h. It
  cannot be: H does not inherit decay. However fast h falls off, H(h) falls off like
  1/X, because the far field only sees h's total mass. So the seminorm weight for
  H(h) is 1−γ regardless of α, and asking for α−γ would have produced an infinite
  constant with nothing to point at. Third time in this series that a weight exponent
  was the entire difficulty, and the third time the right one was forced rather than
  chosen.

- **A bug worth publishing.** The scaling argument that shows the estimate is finite
  needs the two points close together relative to their distance from the far-field
  endpoint. The estimate itself needs no such thing — only that the near region fits
  on the circle once. The first version imposed the argument's condition on the code,
  which forced a much cruder fallback for the pairs just outside it, and the reported
  constant came out twelve times too large. Every one of those pairs was the fallback,
  not the estimate. General form: do not let the regime of an argument become the
  regime of the code.

- **The gate that earned its keep, again.** This estimate is a majorant of a
  three-piece decomposition, and a majorant of a *wrong* decomposition is still a
  valid inequality — about something else. No "is the bound bigger than the measured
  value" test can see that. So the decomposition was built a second time with the true
  integrand and checked against the answer known in closed form (cos kθ → sin kθ):
  agreement to 6 decimals, after it caught two sign errors, one of which was also
  wrong in the module's own docstring where it had been sitting looking correct.

- **v7's prediction was backwards, and the reason is mundane.** v7 called its optimum
  provisional because the omitted term "is worst exactly where γ is smallest". It is
  worst at the *other* end: 0.1% at γ = 0.05, 28% at γ = 0.9. v6's already-bounded sup
  part carried the same 1/γ near-region divergence, so nothing new blows up down
  there. The optimum does not move — (1.4, 0.15) in both maps.

- **The number that matters is the trend.** Budget history across four legs: 7.6e-2 →
  1.18e-2 → 2.58e-4 → 2.39e-4. Three order-of-magnitude losses, then one of 7%. After
  v7 the honest reading was that every remaining honesty step would cost an order and
  the approach would die of a thousand cuts. That reading rested on three data points
  with a common cause. This one had the same cause and cost almost nothing. That is
  not evidence the remaining three items are cheap — it is evidence that "each step
  costs an order" was a pattern, not a law, which is worth about one more leg.

- **What is now the bigger lever.** Z₂ is complete, so the open items are all Z₁-side
  or representational. But ‖A‖'s bracket is ~75× wide and C_Q's is ~4×, and the budget
  scales inversely with their product. Sharpening what we already have may now be
  worth more than bounding one more thing — which is a different kind of leg than the
  last three.

## Phase-2 P2 — ROUTE-D v7: the domain seminorm part of ‖A‖, closed by a derivative gain (non-logged) — 2026-07-31

**NOT a logged gate run** (deterministic; no GA, no seeds, no predicate lock). Data
`writeup/data/p2_route_d_v7_seminorm.json` (regen `python experiments/p2_route_d_v7_seminorm.py`,
~15 min); figure fig25 (`writeup/4_p2_lottery/p2_route_d_v7_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V7; PHASE2_P2_NOTES.md §16. Code: `solver/nk_seminorm.py` +
`test_nk_seminorm.py` (6/6; suite now 14 files green).

What a human would want to know:

- **The leg did not do what the previous leg told it to.** v6 named two routes to this
  bound and said "do (a) first" — restrict to a band-limited subspace where the discrete
  norm is faithful. A ten-minute diagnostic killed that plan: the J^γ growth sits
  *entirely* on pairs the grid barely separates, and a faithfulness defect of the ball is
  a statement about which directions are admissible — it cannot know or care whether the
  two domain indices being compared are adjacent. The J^γ does. So (a) was aimed at the
  wrong mechanism, and it was aimed there because v6 reasoned by analogy to v6's own
  headline finding. Worth remembering: the freshest lesson is the most tempting analogy,
  and an analogy is not a diagnosis.

- **What actually removes it.** The dual was pricing each row of the inverse separately
  and then dividing by |Δθ|^γ. That discards the near-cancellation of neighbouring rows,
  which is a property of the *equation*, not of the rows — so no refinement of a dual
  functional can recover it. Using the equation instead: solve `DF h = g` for `h_X`
  (an exact rearrangement), then split every pair of points at a fixed multiple of the
  local X-scale. The weights cancel identically at every scale, and what comes out has no
  J and no grid in it.

- **The closure never fails, and that is structural.** The bound feeds back on itself
  through `|H(h)|` linearly, while the interpolation gain is sublinear (`T^γ`). Concave,
  increasing, positive at zero ⇒ exactly one fixed point, no smallness condition, nothing
  to lose. Only γ = 1 turns it into a real contraction condition — which is a third
  independent reason the Lipschitz endpoint is excluded, after v5's measured blow-up and
  the classical unboundedness of H there. Three unrelated arguments landing on the same
  exclusion is the kind of agreement worth noticing.

- **The number, and the honest bracket.** ‖A‖ ≤ 69.1, essentially flat in J (the residual
  J^+0.006 is inherited entirely from v6's sup-part dual; the closure contributes none).
  First uniform upper bound on the whole operator in seven legs. But the best lower bound
  is 0.85, so the bracket is a factor ~75 wide, and that width is not cosmetic — see the
  next point.

- **The negative that matters more than the bound.** Substituting the honest ‖A‖ for the
  far-field proxy v6 used drops the conditional budget from 2.8e-3 to 2.0e-4. That is the
  *second consecutive leg* in which replacing a lower bound by an upper bound cost an
  order of magnitude. The losses multiply inside Z₁ and Z₂, so the approach does not just
  need the constants bounded — it needs them roughly sharp. Three of the four bounded so
  far are lossy by an order or more. If that pattern repeats twice more, the budget is
  gone, and it would be honest to say so early rather than after building the tooling.

- **A defect older than this leg, found by checking the chain.** A nodal vector on the
  midpoint grid is a trigonometric polynomial in θ; a trigonometric polynomial does not
  vanish at θ = π; the decay weight `sec^α(θ/2)` diverges there. So the interpolant's
  decay-graded norm is infinite at every J, and every discrete norm from v1 to v7 is
  finite only because the midpoint grid stops half a step short of π. It is soft
  (`h(π) ~ J^-3.01`, so the discretization is converging to something that does live in
  the space) and the derivative-gain closure is immune because it is a continuum
  statement — but it is a change of ansatz, not a small correction: write
  `h = (1+X²)^{-α/2} p(θ)` with `p` a trig polynomial and the weighted sup norm becomes a
  plain sup norm.

## Phase-2 P2 — ROUTE-D v6: first genuine UPPER bounds + the discrete-ball trap (non-logged) — 2026-07-30

**NOT a logged gate run** (deterministic; no GA, no seeds, no predicate lock). Data
`writeup/data/p2_route_d_v6_bounds.json` (regen `python experiments/p2_route_d_v6_bounds.py`,
~10 min); figure fig24 (`writeup/4_p2_lottery/p2_route_d_v6_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V6; PHASE2_P2_NOTES.md §15. Code: `solver/nk_bounds.py` +
`test_nk_bounds.py` (6/6; suite now 13 files green).

What a human would want to know:

- **The thing five legs got structurally wrong.** Every constant reported through v5
  was a maximum over a test family — a LOWER bound — and Z₁ was never bounded at
  all. The certificate needs UPPER bounds on all of them. So the budget we had been
  quoting was an upper bound assembled out of lower bounds, which is not a number
  that means anything. Worth saying plainly rather than quietly fixing.

- **The trap, which is the real result.** The obvious fix is duality: instead of
  maximising over functions you thought of, maximise over the whole unit ball,
  which for these norms is a closed-form computation. It ran fine and said the
  operator was unbounded, ‖A‖ ~ J^0.5, under three independent bounding routes and
  every gauge-row choice. All fiction. A discrete Hölder seminorm only looks at
  pairs of GRID NODES, so duality's extremizer is a grid-scale sign pattern whose
  interpolant thrashes in the gaps. Evaluated on a 6× finer grid over the same
  θ-range, its true norm is 3e3× bigger at J=125 and 5e4× at J=500 — growing like
  J² — while a smooth element of the same class stays faithful to 3%. The worst
  direction was not within four orders of magnitude of the unit ball.

- **Why that lesson is worth more than the bound.** We already had banked lesson (9)
  — BUILD THE ADVERSARY — from v4, where random sampling MISSED the adversary and
  reported a boundedness that was false. This is the mirror: a ball that is too BIG
  invents an adversary and reports an unboundedness that is false. Sampling
  under-reports, a sloppy ball over-reports, and neither is telling you about the
  operator. The general form: before trusting a number about an operator, check
  that the set you optimised over is the set you meant.

- **What survived.** Use only inequalities the CONTINUUM norm implies (a pointwise
  bound and a two-point increment bound) and the resulting estimate is honest
  whatever the grid does. On the domain sup part it SATURATES — 5.536 → 5.631 over
  a 13× range in J — the project's first uniform upper bound on any part of ‖A‖,
  and it brackets v5's family lower bound by about 2×. The seminorm part is still
  lossy (J^γ), and §B1 says exactly why: it is still paying for the fake direction.
  The equation says that part must be finite (the inverse gains a whole derivative),
  so this is now the sharpest open question in Route D.

- **The Z₁ half went cleanly, and one detail earned its keep.** The difference
  between the real operator and v3's far-field model is a two-term identity,
  h/(X(1+X²)) − H(h)/(1+X²), exact to 1.5e-16 against the collocation operator.
  Bounding |H(h)| for an arbitrary unit-ball h is exactly what the Hölder grading
  was introduced to pay for, and it works. The detail: doing the principal-value
  split with the textbook one-sided kernel gives a bound that diverges
  logarithmically as X→0, where the true value is exactly 0 by parity. Rewriting
  the kernel in its EVEN form — every function here is even — fixes that AND
  recovers the sharp far-field constant (1.681 vs 1.669). Symmetry you already know
  about is free accuracy; it is just easy to leave on the table.

- **And it moved the answer.** Z₁ had never entered the optimization, because nobody
  could compute it. At v5's joint optimum α=1.8 it comes out 2.3–4.3 against a
  requirement of <1 — dead at every X₀ tested, and dead structurally (the modelling
  error decays like X₀^{α−2}, so α=1.8 would need the far field 10⁵× further out,
  while ‖A‖=2/(2−α) runs toward the α=2 resonance). The optimum moves to α≈1.2 with
  a conditional budget 1.18e-2. The a≈0.5 GA floor is also ~1e-2, and I want that
  comparison read carefully: the budget prices ONE piece of Z₁, uses a far-field
  ‖A‖ validated only on α∈[1.4,1.7] (not where the optimum now sits), and omits
  three constants — every omission flatters it. The honest claim is only that the
  target is no longer out of reach by orders of magnitude.

- **Honest ceiling.** Plain float64 throughout; nothing interval-enclosed, nothing
  rigorous. Three of eight constants moved from measured to bounded; three remain,
  now named precisely enough to attack one at a time. Clay odds unchanged (~0.05%).

## Phase-2 P2 — ROUTE-D v5: THE TWO-GRADING SPACE (non-logged) — 2026-07-30

**NOT a logged gate run** (deterministic — no GA, no seeds, no predicate lock). Data
`writeup/data/p2_route_d_v5_holder.json` (regen `python experiments/p2_route_d_v5_holder.py`,
~10 min); figure fig23 (`writeup/4_p2_lottery/p2_route_d_v5_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V5; PHASE2_P2_NOTES.md §14. Code: `solver/holder_norms.py` +
`test_holder_norms.py` (6/6; suite now 12 files green).

What a human would want to know:

- **The question was well posed for once.** v3 and v4 between them stated the requirement
  completely: the space needs a decay grading (far-field transport) AND a smoothness scale
  (Hilbert transform). This leg just had to build it and check the two halves don't
  fight. They don't.

- **The algebra slip, caught by a check I nearly didn't write.** The conformal translation
  of the far-field Hölder seminorm through X = tan(th/2) eats a factor of gamma — the
  weight is alpha MINUS gamma, not alpha. With the wrong weight the model profile f_alpha
  has INFINITE seminorm, i.e. the space would not have contained the object the whole
  certificate is about. The numerical check failed by a whole exponent, not a rounding
  error. Second time in three legs. The habit pays.

- **The payoff from getting it right.** After the identity, the elaborate weighted
  conformal seminorm collapses to a PLAIN theta-Hölder seminorm with a diagonal weight.
  The compactification does the far-field bookkeeping for free — no local windows, no
  scale-dependent pair selection, one O(J^2) broadcast. That is the only reason the leg
  was cheap enough to run at all.

- **The adversary is genuinely defused.** Same square wave that killed v4: sup ratio grows
  x2.26 at EVERY gamma (it does not care about the decay weight — exactly v4's diagnosis),
  Hölder ratio x0.83 at gamma=0.5 and falling. The mechanism is not subtle: in a Hölder
  norm the adversary pays for its own oscillation.

- **The thing I did not expect: smoothness has an interior optimum too.** C_H(gamma) bowls
  — 1.60 at 0.15, 1.12 at 0.35, 1.29 at 0.85 — rising at both ends for DIFFERENT reasons
  (gamma->0 is the sup norm where H is unbounded; gamma->1 is Lipschitz where it fails
  again). v4 found the same shape in alpha from far-field-vs-core. Two knobs, two interior
  optima, four unrelated mechanisms. That the space has a finite non-degenerate best
  configuration in both parameters is the most encouraging structural fact five legs have
  turned up, and I would not have predicted it.

- **Chasing a disagreement paid, again.** The coarse (alpha,gamma) sweep said the inverse
  norm grows like J^0.14; a focused ladder said it settles. Both were right about their own
  test directions. Isolating it: at the codomain's CRITICAL decay rate the ratio creeps
  (a log), and at ANY delta>0 it is flat to four significant figures across a 16x range in
  J. That is v3's resonance one level down, and the same fix works. The difference is the
  price: v3's detuning cost 2/eps, this one is FREE and the constants improve with delta —
  because it tightens the CODOMAIN instead of loosening the DOMAIN off its own kernel.
  Worth remembering as a rule: detuning a requirement on the residual is cheap; detuning
  the class of solutions is expensive.

- **The number, with its four asterisks.** Z2 = 3.29 vs v4's 13.4; ceiling 7.6e-2 vs
  1.9e-2. But: ||A|| and C_Q are FAMILY-RESTRICTED lower bounds (the exact induced norm
  between polyhedral norms is an LP and we have no scipy), so the ceiling is an upper bound
  on an upper bound; Z1 has never been bounded in five legs and is now the biggest gap;
  and the argmax sits at alpha=1.8, the EDGE of the swept grid, in a row with an
  unconverged-J artifact. The optimum's existence is solid; its location is not.

- **What I would tell the next session.** The scoping phase of Route D is essentially done
  — we know the space. The remaining work is estimates, not exploration: bound Z1, and turn
  the family-restricted norms into real upper bounds (analytically, not by LP — the far
  field has a closed-form inverse and the core is finite-dimensional). solver/interval.py
  has existed since v1 and has still never been used, which is correct, because nothing has
  closed in float.

- Everything is plain float64. Nothing interval-enclosed, no rung climbed. Clay odds
  unchanged (~0.05%).

## Phase-2 P2 — ROUTE-D v4: THE FULL OPERATOR IN THE DECAY-GRADED PAIR (non-logged) — 2026-07-30

**NOT a logged gate run** (deterministic — no GA, no seeds, no predicate lock). Data
`writeup/data/p2_route_d_v4_graded.json` (regen `python experiments/p2_route_d_v4_graded.py`,
~10 min); figure fig22 (`writeup/4_p2_lottery/p2_route_d_v4_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_V4; PHASE2_P2_NOTES.md §13. Code:
`solver/decay_collocation.py` + `test_decay_collocation.py` (6/6; suite now 11 files green).

What a human would want to know:

- **The question: was v3's price real, or an artifact of the model?** Every number v3
  produced came from a one-line far-field ODE with the Hilbert coupling, the compact
  core and the gauge all thrown away. It is exactly the sort of estimate that looks
  authoritative and turns out to be missing the dominant term. So: rebuild without the
  simplifications and check.

- **It was real, and by a wider margin than I expected.** On alpha in [1.4,1.7] the model
  law 2/|a-2| predicts the FULL gauged inverse norm to 6% (2% on [1.5,1.7]). Z2 lands at
  13.4 vs the predicted 13.3. Everything we threw away was worth almost nothing. That is
  the good kind of surprise, and it is also a licence: the cheap far-field analysis is a
  trustworthy instrument for the next leg too.

- **The bonus nobody asked for.** The full ||A|| has its own interior minimum at a~1.40.
  v3 found an interior optimum in the BUDGET from two constants pulling opposite ways;
  this is a different quantity driven by a different pair of mechanisms (far-field cost
  rising toward the a=2 resonance, core cost rising toward a=1) and it lands in the same
  place. Two independent arguments agreeing on 1.4-1.5 is worth more than either.

- **The bad news, which is structural.** The decay-graded SUP pair does not control the
  quadratic term, and cannot: H is unbounded on L^infinity. No decay weighting escapes
  it, because the log blow-up happens at an ordinary interior point (the jump of a
  bounded function) where the weights are O(1).

- **The mistake I made, and would make again without a rule against it.** The first
  version of the quadratic test sampled RANDOM trig perturbations of increasing degree.
  Those constants go DOWN (1.40 -> 0.84 over m=4..512) and cheerfully reported the
  quadratic as bounded and converging. It agreed with what I wanted to be true. The real
  answer needed the textbook adversary — partial sums of a square wave, bounded with a
  logarithmically divergent conjugate — which gives +0.41 per e-fold, unbounded. The bad
  direction is a measure-zero cusp in the ball; you do not stumble onto it. **Sampling
  can refute a proposed bound and can give a lower bound. It can never establish
  boundedness, and it cannot reveal unboundedness. Build the adversary.**

- **The unified statement is the real output of the last two legs.** v3: a diagonal
  weight measures smoothness, we needed decay. v4: a sup norm measures decay, we also
  need smoothness. Each single-parameter family is missing exactly what the other has.
  The far-field transport forces a decay grading; the Hilbert transform forces a
  smoothness scale; the space has to carry both. Four legs in, this is the first time
  the requirement has been stated COMPLETELY.

- **Operational finding worth remembering:** the gauge must replace a CORE collocation
  equation. Dropping the outermost (far-field) row instead sends ||A|| from ~4 to 1.06e5.
  Obvious in hindsight; not obvious at 2am.

- **Honest read.** Budget ceiling 1.9e-2, and it IS a ceiling (Z1=0 assumed, smoothness
  component unpriced) against an a!=0 floor of ~1e-2. Thin, and thinner than v3's number
  because v3's was also a ceiling. Everything is plain float64; nothing interval-enclosed;
  no rung climbed. Clay odds unchanged (~0.05%).

## Phase-2 P2 — ROUTE-D v3: the SPACE-PAIR NO-GO (non-logged) — 2026-07-30

**NOT a logged gate run** (deterministic scoping — no GA, no seeds, no predicate lock).
Data `writeup/data/p2_route_d_v3_spaces.json` (regen
`python experiments/p2_route_d_v3_spaces.py`, ~1 min); figure fig21
(`writeup/4_p2_lottery/p2_route_d_v3_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_SPACES; PHASE2_P2_NOTES.md §12. Code:
`solver/decay_grading.py` + `test_decay_grading.py` (7/7; suite now 10 files green).

What a human would want to know:

- **This leg exists because §11 attached a condition to its own repair, and the
  condition was the whole ballgame.** v2 measured that grading the codomain by one
  mode power makes ‖A‖ flat at 3.000 and called that the pair to use. It also said:
  check that the quadratic lands in that codomain first, on paper, because if no
  consistent pair exists the leg stops cheaply. It doesn't exist. The check cost an
  afternoon of algebra and a minute of compute, and it saved building a two-region
  solver in a space pair that could never have been consistent.

- **The identity that does all the work.** Q(h) = hH(h) is a PURE CONVOLUTION —
  q_m = ½Σ_{j+k=m}h_jh_k, no difference frequencies. (h+iH(h) is a Hardy boundary
  value; 2hH(h) is Im of its square; squaring a holomorphic function can only add
  frequencies.) From it the sharp weighted constant is S = sup v_{j+k}/(u_ju_k),
  two-sided (S/4 ≤ M ≤ S/2), and the no-go is one line: k=0 gives v_m/u_m ≤ S·u_0
  bounded, while a bounded inverse needs v_m/u_m ≳ 2m. The constant mode multiplies
  everything at full strength — e_0·H(h) = H(h) — so no codomain strictly stronger
  than the domain can receive the quadratic.

- **The conservation law is the result I'd lead with.** Sweeping the whole family
  u_k=(1+k)^s, v_m=(1+m)^t, both requirements collapse onto the gap g = t−s, and the
  two growth exponents are exact complements: ‖A_N‖ ~ N^(1−g), S_K ~ K^g. A
  certificate needs both zero; the SUM is ≥1 everywhere and exactly 1 on 0≤g≤1.
  Measured minimum over the entire family: **0.98**. That is a stronger and cleaner
  statement than "the proposed repair fails" — it is "every repair in this category
  fails, and here is the invariant."

- **The control is what makes it an attribution.** (1+cosθ)→1, nothing else changed:
  the inverse boundary moves from t ≥ s+1 to t ≥ s−1. TWO powers — and that is
  exactly right, because a healthy first-order transport gains one power on
  inversion, this one loses one, and 1+cosθ vanishes to order 2 at θ=±π. Min
  exponent sum drops 0.98 → 0.00, overlap 0/9 → 9/9. I did not predict the 2 in
  advance; noticing it after the fact is what convinced me the picture is right.
  (First version of the figure claimed the control drops the boundary to t=s — wrong,
  caught by widening the t-grid to negative values.)

- **The reframe: it was a category error.** A diagonal weight measures SMOOTHNESS,
  not DECAY. cos(kθ) = (−1)^k at θ=π — a single mode does not decay at X=∞ at all,
  for any k, so no weight can see decay. Decay lives in the alternating structure of
  the coefficient sequence. Asking a weighted-ℓ¹ pair to express "loses one power of
  decay" was asking a ruler to weigh something.

- **The positive half, which I did not expect to get.** In DECAY-graded spaces
  (|h| ≲ X^−α, |g| ≲ X^−α−1) both requirements hold at once: the far-field inverse
  because of the ODE, and the quadratic because H(h) ~ (∫h)/(πX) means hH(h) decays
  ONE POWER FASTER than h. Products don't gain smoothness but they do gain decay —
  which is exactly why the coefficient picture couldn't see it.

- **A resonance nobody had named, and a design parameter nobody knew was there.**
  ‖L^{-1}‖ = 2/|α−2| exactly (measured to 0.008% against a 2nd-order discretization,
  and independently from the operator side: lim X^{α+1}DF[f_α] = cα−1, to 0.3%). The
  pole sits at α=2 — which is BOTH the homogeneous far-field solution at c=1/2 AND
  the decay of the anchor. The natural choice is the forbidden one. Detuning costs
  2/ε, but pushing α→1 blows up the quadratic constant (∫f_α)/π instead, so there is
  an INTERIOR OPTIMUM at α* ≈ 1.44 (3/2 is within 1%). Recommendation for any v3
  build: certify profiles decaying like X^−3/2 with residuals in X^−5/2, explicitly
  NOT the anchor's own X^−2.

- **Honest read of the number.** The optimum gives Z₂ ≈ 13, so a budget ~1e-2 BEFORE
  paying for anything this leg didn't estimate (compact core, Z₁, interval overhead).
  The a≠0 residual floor is also ~1e-2. The margin, if any, is thin. Better to know
  that now than after the build.

- Everything is plain float64. Nothing interval-enclosed, nothing rigorous, no rung
  climbed on the ladder. Clay odds unchanged (~0.05%).

## Phase-2 P2 — ROUTE-D v2: the FLOAT DRESS REHEARSAL — NEGATIVE (non-logged) — 2026-07-28

**NOT a logged gate run** (deterministic tooling + a scoping ladder — no GA, no seeds,
no predicate lock). Data `writeup/data/p2_route_d_dress.json` (regen
`python experiments/p2_route_d_dress.py`, seconds); figure fig20
(`writeup/4_p2_lottery/p2_route_d_dress_evidence.py`); writeups
TECHNICAL/BLOG_P2_ROUTED_DRESS; PHASE2_P2_NOTES.md §11. Code: `solver/nk_fourier.py`
+ `test_nk_fourier.py` (6/6; suite now 9 files green).

What a human would want to know:

- **The question was gating, and the answer was no.** §10 ended with one thing that
  decided whether to spend weeks on interval hardening: does the radii polynomial
  close at the a=0 anchor? Computed in plain float across N=4..256: **0/13**. Not
  marginal — the certification budget Y₀^max = (1−Z₀−Z₁)²/(4Z₂) is *identically
  zero* at every N. Running the cheap rehearsal first is exactly what it was for.

- **The pessimism in §10 was aimed at the wrong thing.** We had worried that a≠0
  would fail because its residual floor ~1e-2 makes Y₀ too big. But the anchor has
  defect *exactly* zero (it's an exact traveling wave and a degree-1 trig
  polynomial, so even the convolution tail vanishes) and it still doesn't close.
  The failure is not about accuracy. It is about the space.

- **The ablation is the part I'd defend hardest.** Growth in ‖A_N‖ alone would only
  be a suspicion. Rebuilding the identical ladder with the transport factor
  (1+cosθ) replaced by 1 — one feature removed, nothing else touched — makes
  ‖A_N‖ go *flat at exactly 4.0* where the true operator reaches 198.7 (N^0.97 →
  N^0.00). That converts "we think it's the far field" into "it is the far field."
  Meanwhile all three gauge normalizations sit on top of each other, so the crux we
  had flagged (sub-task G) is cleared and the footnote (sub-task R) is the blocker.
  The open-risk list from §10 is now reordered by evidence rather than by hunch.

- **Two things closed the argument off from "try harder".** (i) Z₁ ≥ N+1 exactly,
  from the truncation coupling alone — the finite section couples *more* strongly to
  what it discards as N grows, so bigger is strictly worse, not asymptotically
  better. (ii) The far-field column weight tends to 1 from *below* under one tail
  model and from *above* under the other, both at O(1/k) — so the marginality is not
  a modelling artifact — and no positive weight can fix it (the required recursion
  has characteristic roots on the unit circle, so any positive solution oscillates
  into negativity). That is a proof, not a scan.

- **The constructive half is what makes this worth writing up.** The far-field ODE
  −c h_X − h/X = g integrates in closed form and predicts the inverse loses exactly
  one power of X-decay; since mode m resolves X ~ m, it predicts ‖A e_m‖ ∝ m.
  Measured 1.97·m. Then grading the codomain by that one power gives ‖A‖ = 3.000,
  flat from N=8 to N=384. Prediction, confirmation, and a specification for the next
  brick — the asymmetric decay-graded space pair — rather than just a dead end.

- **Built the operator twice, found a bug.** `solver/nk_fourier.py` is exact closed
  form (no grid, no quadrature: the anchor nulls to 0.0, versus the grid's 1e-9),
  gated against three oracles — the anchor, finite differences, and the banked grid
  residual. Comparing it with §10's independently-written band exposed an unfolded
  sin(−θ) in the k=0 column there (−1/4 instead of −1/2); v1's cross-check only ran
  k≥1, so it never touched the folding case. Fixed, cross-check extended to k=0, and
  the two closed forms now agree to 0.0. No conclusion of §10 changes, but it is a
  standing argument for building the same object twice.

- **Honest ceiling.** All float64. Nothing here is interval-enclosed and nothing is
  rigorous. This does not climb the rigor ladder — it closes one route with a reason
  and gives its replacement an address. Clay odds unchanged (~0.05%).

## Phase-2 P2 — ROUTE-D v1: interval core + a=0 NK framing — TOOLING/SCOPING (non-logged) — 2026-07-26

**NOT a logged gate run** (deterministic tooling + a scoping probe — no GA, no
seeds, no predicate lock; every number is a property of the fixed anchor +
operators). Recorded here because it produces committed data + a figure. Data
`writeup/data/p2_route_d_probe.json` (regen `python experiments/p2_route_d_probe.py`);
figure fig19 (`writeup/4_p2_lottery/p2_route_d_evidence.py`); writeups TECHNICAL/BLOG_P2_ROUTED;
PHASE2_P2_NOTES.md §10. Code: `solver/interval.py` + `test_interval.py` (5/5, suite
now 8 files green). This is the FIRST brick on the rigor ladder (Level-1→Level-2);
it is validated tooling + a framing result, **NOT a certificate**.

What a human would want to know:

- **The question the user chose.** Not "certify the GA two-scale profile" but the
  honest prerequisite: *can a Newton–Kantorovich certification even be SET UP* for
  `residual_two_scale`, gated against the a=0 exact anchor? Answer the arithmetic +
  structural prerequisites first, frame the attempt, don't skip to the claim.

- **Evidence-first path (the user's steer: "interval-arith core first, then decide";
  "degeneracy — whichever is best based on testing").** Built the interval core,
  then measured. Q1: the rigorous enclosure width (8.5e-11) is ~10% of the anchor
  defect (8.9e-10) → the defect bound Y₀ is carryable. Q2: singular values COUNT the
  a=0 scaling valley — 2 kernel dims (gauge-slaved) → 1 (fixed speed) → **two** gauge
  conditions isolate a nondegenerate zero; the naive un-gauged inverse is ∞ (so the
  "gauge-fix vs document non-closure" fork was decided by the numbers: gauge-fix, and
  the non-closure is already demonstrated by the rank-deficient Jacobians).

- **The lucky structural break (Q3/Q4).** Spotted from the anchor's Fourier form and
  CHECKED: under X=tan(θ/2) the line Hilbert transform IS the circular conjugate
  (cos kθ↦sin kθ, verified ~1e-7, k=1..6). So the anchor is 2-term, and DF is
  **tridiagonal + rank-1** (cos→sin) — the reason Z₀+Z₁<1 is plausible, not hoped.
  The closed-form band matches the grid operator to 3.9e-2; that residual is the
  θ=±π (Cayley) endpoint correction, flagged as open sub-task R (not buried).

- **Honest ceiling + next.** Framing = radii-polynomial NK; F quadratic ⇒ Z₂
  constant. Open: G (exact gauge/Fredholm-index square system — the crux), R
  (endpoint correction), T (rigorous tail-inverse bound), a≠0 (no exact anchor off
  a=0 → Y₀ jumps ~1e-9→1e-2, boundary certificate likely won't close). NEXT = the
  FLOAT dress rehearsal (compute Y₀/Z₀/Z₁/Z₂ + radii polynomial in plain float to
  see if the ball closes at the anchor) BEFORE any interval hardening. Even full
  success = toy-model computer-assisted certification, NOT a Clay solve. Odds ~0.05%.

## Phase-2 P2 — TWO-SCALE a_p(K) CONVERGENCE map — LOGGED (7/7) — 2026-07-26

**LOGGED gate run** (predicate T1–T7 LOCKED in git before the run, commit 44a507c).
Data: committed `writeup/data/p2_two_scale_kladder.json`; harness
`experiments/p2_two_scale_kladder.py --logged`; writeups TECHNICAL/BLOG_P2_KLADDER
+ fig18 (rebuilds from JSON via `writeup/4_p2_lottery/p2_two_scale_kladder_evidence.py`);
PHASE2_P2_NOTES.md §9-cont2. Verdict **7/7 clauses hold** — a NOVEL toy-model
characterization (Tier-1/2), NOT a proof, NOT a Clay solve. This SHARPENS the prior
leg's T4 FAIL (the honest one): it turns the "genome-relative soft boundary" caveat
into a converged, resolvable answer.

What a human would want to know:

- **The question (from the prior leg's T4 fail).** The two-scale a-sweep found the
  exact a=0 traveling wave persists (relres<1e-2) only to a_p≈0.40 for a FIXED even
  K=2 genome — but T4 FAILED: a richer K=3 genome cut the a=0.5 floor 4×, below the
  1e-2 line. The GA gives only an UPPER BOUND, so a_p(K) can only rise with K. Open
  question the user chose to sharpen: does a_p(K) **saturate** (→ a genuine survival
  boundary a\*) or **keep marching out** with K (→ INCONCLUSIVE, genome-limited)?

- **The confounder the scout caught (this is the whole ballgame).** At the base
  budget the higher-K floors are **search-limited, not converged**: a GA-convergence
  probe showed the a=0.6 K=4 floor drop **45%** when the budget was doubled. A naive
  a_p(K) map at the old budget would have reflected GA effort, not genome richness.
  A scratch plateau probe (a=0.55/0.60, K=4/6, budgets 1×→8×) settled it: the floor
  **PLATEAUS** — a=0.55→~1.0e-2 and a=0.60→~1.8e-2, stable under ~8× budget AND not
  improved at K=6. That fixed the logged budget at pop150/gen250/8-seeds (converged)
  and put an IN-JSON budget spot-check (~1.7×) + a K=6 genome spot-check in the run
  so the plateau is reproducible from committed data, not just scratch.

- **Result (7/7).** a_p(K) = **0.40 → 0.50 → 0.50** — it rises off the K=2 value
  then **SATURATES**. Boundary a\* ≈ 0.55 (smallest a where the converged K=4 floor
  first exceeds 1e-2: K4(0.55)=1.08e-2). At the boundary the floor is **GA-converged**
  (K4 1.7×-budget 1.03e-2 vs 1.08e-2, <5%) and **genome-converged** (K6 1.23e-2 does
  NOT beat K4 1.08e-2), and **basis-independent** (a different even basis, Lorentzian
  + squared-pole `even_lorentz_sq`, gives 8.3e-3, within 3× of even K3). Resolution
  fine (min verdict width 35 grid pts ≫ 8). Far-end (De Gregorio) robust: K4 floor
  rises to 1.28e-1 at a=1.0 — survives richer genome + budget (this was the prior
  leg's ONE robust T4 sub-claim, now confirmed across the whole K-ladder).

- **The honest nuance I did NOT bury.** a\* is not a razor edge. Right at a=0.55 the
  converged floors straddle the 1e-2 line: even K3/K4 sit just above (≈1.1e-2) while
  the mixed basis dips just under (8.3e-3). That is exactly what a threshold crossing
  looks like — the boundary is a\* ≈ 0.5–0.55 with a soft ~1e-2 floor, not a sharp
  wall. Reported as such; the SCIENCE claim is "saturates near 0.5–0.55, genuine, not
  genome-limited," not "dies exactly at 0.55."

- **Bug/discipline notes.** New solver basis `even_lorentz_sq` (X^-4 poles) added +
  unit-tested as the basis-independence cross-check: gated to be genuinely DIFFERENT
  (a single squared pole is NOT an a=0 traveling-wave null, relres=0.11) yet to still
  CONTAIN the exact anchor (Lorentzian+zero-squared mix → 1.3e-8), so T1 holds on it.
  test_gclm_family 12/12; full suite 7 files green. Observed the plateau in scratch
  BEFORE locking the predicate (grounded the budget + thresholds). Did NOT re-run to
  move any clause.

- **Where this sits + next.** This is a Level-1 result (a novel *numerical* map), now
  clean and convergence-guarded — it does NOT move up the rigor ladder, it makes the
  Route-D **guess** sharper and better-justified (a\*≈0.5–0.55 boundary + the a=0
  exact + near-boundary profiles). **User confirmed Route D is the next brick**: an
  interval-Newton / Newton–Kantorovich certification on those profiles — the first
  rung that is genuinely "novel maths" (Level-2). Clay odds unchanged (~0.05%).

## Phase-2 P2 — TWO-SCALE-under-advection a-sweep — LOGGED (5/6, PARTIAL) — 2026-07-26

**LOGGED gate run** (predicate T1–T6 LOCKED in git before the run, commit 6fc1ff0).
Data: committed `writeup/data/p2_two_scale_sweep.json`; harness
`experiments/p2_two_scale_sweep.py --logged`; writeups TECHNICAL/BLOG_P2_TWO_SCALE
+ fig17 (rebuilds from JSON via `writeup/4_p2_lottery/p2_two_scale_sweep_evidence.py`);
PHASE2_P2_NOTES.md §9. Verdict **5/6 clauses, PARTIAL by construction** — a NOVEL
toy-model result (Tier-1/2), NOT a proof, NOT a Clay solve.

What a human would want to know:

- **The question.** HQW25 (arXiv:2401.14615) proves CLM (a=0) has an EXACT two-scale
  self-similar blowup whose profile is a TRAVELING WAVE Ω₂=−1/(1+X²). Does that
  mechanism survive gCLM advection as `a` grows (a=0 CLM → a=1 De Gregorio)? Nobody
  had mapped it. This is the novelty swing the user chose.

- **What we built + derived.** The two-scale residual R₂=ΩHΩ − c_tw Ω_X − a U Ω_X:
  carried HQW25's moving-frame ansatz to its leading (T−t)^{−3} order → a PURE
  TRAVELING WAVE (the dilation −c_l XΩ_X and amplitude c_ω Ω terms are subleading and
  DROP). Structurally a TRANSLATION, not a dilation. a=0 known-answer gate: Ω₂ nulls
  R₂ to 1.5e-9, gauge speed c_tw=0.5000000; EVERY even_lorentz A/(1+BX²) is an exact
  a=0 TW with c_tw=−A/(2√B) → the a=0 set is a 2-parameter scaling valley.

- **The GA-cheats bug we caught pre-lock.** Plain RMS ‖R₂‖ is NOT scale-invariant —
  a GA drives amplitude→0 (c_tw→0), a trivial null. Switched to the scale-invariant
  relres=‖R₂‖/‖ΩHΩ‖ (fraction of stretching unaccounted). The scratch literally
  showed the pathology first; fixing it is why the result is trustworthy.

- **Pre-lock robustness scout (grounds the thresholds).** The floor curve is INVARIANT
  across n=601/801/1201 and rho_max=8/10 (physical, not a tail artifact) and
  GA-converged (2.5× budget barely moves it). Config locked n=801, 6 seeds.

- **Result (5/6).** T1 known-answer PASS (5.8e-8). T2 persistence PASS: relres<1e-2
  out to a_p=0.40 (deformed-but-present traveling profile). T3 monotone-degradation
  PASS: floor rises to 1.8e-1 at a=1. T5 symmetry PASS: odd-fraction<0.013 throughout
  (mixed genome free to skew, STAYS EVEN). T6 resolution-guard PASS (min 49 pts).
  **T4 FAIL (the honest headline):** at a=0.5 a richer even K=3 ansatz cuts the floor
  4× (2.45e-2→5.6e-3), so the mid-range floor is partly GENOME-LIMITED — the K=2 map
  is a genome-relative UPPER BOUND, the survival boundary is NOT sharply pinned. This
  is exactly the pre-committed INCONCLUSIVE branch, reported not hidden. BUT at a=1
  K=3 does NOT rescue (1.83e-1→1.43e-1) → the De Gregorio-end degradation is robust.

- **Honest picture.** No sharp collapse: the two-scale traveling wave DEFORMS SMOOTHLY,
  persists well for small a, degrades toward De Gregorio, stays even, and advection
  SELECTS a scale (lifts the a=0 valley). Endpoints robust; middle genome-relative.

- **Discipline held.** Did NOT re-run to chase T4 into a pass. The T4 fail is the
  machine catching its own limitation — the right outcome. Next: richer/spectral
  genome to sharpen a_p (or a Route-D interval-Newton on these guesses); separately,
  the coupled-system HL two-stage leg. Clay odds unchanged (~0.05%).

## Phase-2 P2 — GA GLOBAL-SEARCH FRAMEWORK (BUILD/scout, NOT a logged gate run) — 2026-07-26

**Infrastructure build + a=0 known-answer validation. No logged experimental run; no science claim.**
Banked record: PHASE2_P2_NOTES.md §9 + writeup/4_p2_lottery/TECHNICAL_P2_GA_FRAMEWORK.md + BLOG_P2_GA_FRAMEWORK.md
+ fig16 (rebuilds from committed writeup/data/p2_ga_framework.json). Code: solver/gclm_family.py,
solver/ga_search.py; tests test_gclm_family.py (6/6; full suite 7/7).

What a human would want to know:

- **What the user asked for.** Pursue the gCLM two-scale↔two-stage transition (the novelty swing),
  and do it VIA a genetic algorithm (their idea), built to also serve Route D. Then: gCLM axis first,
  bridge to HL later.

- **What we built.** A GLOBAL search for self-similar profiles: the gCLM `a`-family rescaled residual
  R = (c_ω+HΩ)Ω − c_l XΩ_X − a U Ω_X (solver/gclm_family.py, velocity U=∫₀ˣHΩ cached) + a generic,
  problem-agnostic real-coded GA (solver/ga_search.py). Deliberately separate from the relaxation
  solvers so the SAME residual object is reusable by a future Route-D interval-Newton certification.

- **Why a GA (honest, said to the user).** Relaxation is LOCAL — it finds the attractor you seed near.
  A family can have MULTIPLE fixed points (different blowup mechanisms); a GLOBAL search maps the set +
  bifurcations = the open two-scale↔two-stage question. A GA proves nothing (Tier-1/2); its roles are
  the global mapper + the "guess" stage for Route D.

- **Fetched the missing anchor.** [HQW25] = arXiv:2401.14615 (Huang–Qin–Wang) downloaded to Papers/.
  Gives the EXACT a=0 two-scale profile Ω₂ (an even Lorentzian bump, c_ω=−3/2). Also corrected the
  framing: HQW25 two-scale = CLM (a=0, scalar gCLM); CHL two-stage = HL coupled system (different
  axis). Well-posed gCLM question: does the a=0 two-scale survive advection as `a` grows?

- **a=0 gate PASSES.** Exact Ω₀ nulls the residual to 2.2e-7; the GA recovers the exact steady set — as
  a 1-parameter DILATION family (gauge is dilation-invariant), so only the invariant A²/B=4.000 is a
  "match". The banked "report gauge-invariants only" lesson literally showed up as a valley (not a
  basin) in the GA landscape (Fig16A). Nice confirmation the discipline is right.

- **Diagnostic LOCKED (pre-run):** D1 scale-separation L_wid/L_loc→0 (slope c_l/c_s=2) ⟺ two-scale;
  D2 invariant c_l/c_ω=−2/3 vs −1; resolution guard → INCONCLUSIVE below ~8 grid pts, never "merged".

- **Honest stop.** The residual is ONE-scale; HQW25's two-scale ansatz (moving frame + c_s) is NOT yet
  built, so Ω₂ isn't a residual-null here yet. That two-scale residual + its Ω₂ gate is the next brick,
  THEN a locked predicate + the logged a-sweep. Validated tooling, not the ticket. Clay odds ~0.05%.

## Phase-2 P2 — B1 LOGGED: CHL Scenario 2 reproduced via the modified rescaling (4.1)/(4.2) — 2026-07-26

**LOGGED gate run** (predicate LOCKED in git before the run, commit b5294ff). Data:
committed `writeup/data/p2_scenario2_relax.json`; harness `experiments/p2_scenario2_relax.py --logged`;
full write-up `PHASE2_P2_NOTES.md` §8. Verdict **5/5 PARTIAL by construction** — Tier-2, NOT novel,
NOT a proof.

What a human would want to know:

- **What we built.** `RescaledHLScenario2` (solver/hl_rescaled.py) = CHL's modified formulation
  (4.1) (spatial-shift DOF `c_r`, evolve `V:=Θ_X`) with the origin-pinned 3-constant normalization
  (4.2): a hand-rolled 3×3 solve each step (`_solve_3x3`, no scipy) for `(c_l,c_ω,c_r)` that pins
  `∂_τΩ(0)=∂_τΩ_X(0)=∂_τV(0)=0`. Origin-clustered grid with X=0 a node. Tests 9/9 — the new gauge
  nulls those three origin time-derivatives to 4.4e-16 (known-answer).

- **Why B1 was the right brick (the user's steer: only if it helps the real direction).** The §6/§7
  degenerate gauge pins stagnation at X=1 and (measured, §7) can't HOLD a profile peaked away from
  X=1. CHL's origin-pinned (4.2) gauge can — and it's exactly the machinery a future gCLM
  two-scale↔two-stage sweep needs to hold regular profiles. B1 = "the gCLM-ready gauge, VALIDATED",
  not a trophy. Said out loud in §8 + to the user.

- **Result.** Two distinct non-symmetric positive ICs both relax to the amplitude-INVARIANT
  contraction exponent `c_l/c_ω = −2.533 / −2.535` (CHL Fig 4.2: −2.5114, ~0.9%) — a genuine
  IC-independent attractor to a regular strictly-positive profile (min Ω>0, smoothness 0.73 vs ≈1061
  for the singular anchor). Residual falls 15→2.2e-2 (≈680×).

- **The honest ceiling (S5, a PASS because it's the predicted boundary).** The residual FLOORS at
  ~2e-2 (does NOT reach CHL's 1e-6 — fixed grid vs their adaptive mesh) and the ABSOLUTE triple
  drifts to (1.59,−0.63,0.21), off CHL's raw (1.0636,−0.4235,0.0765) — the absolute constants are
  IC-normalization-dependent; only the ratio + shape are gauge-invariant. Adaptive dt (recompute CFL
  as the initial c_l=13 transient decays) was needed to reach τ≈42 in 14k steps.

- **Where this leaves us.** BOTH CHL scenarios now reproduced (§2 singular Stage-2 anchor + §8
  regular Scenario-2 exponent). Tier-2 consolidation. The lottery ticket still lives elsewhere: the
  gCLM two-scale↔two-stage transition (now has the validated origin-pinned gauge to build on) or a
  rigor step on Conjecture 2.4.

## Phase-2 P2 — SCOUT (non-logged): the "generic" state is CHL's regular Stage-1 profile; B1/B2 scoped — 2026-07-25

**NOT a logged gate run** — an exploratory characterization + literature scout, no pre-committed
predicate, no new solver code (used `RescaledHLDynamic` as-is). Recorded here because it upgrades the
prior entry's main caveat and decided the fork direction. Evidence:
`writeup/4_p2_lottery/p2_regular_profile_evidence.py` → `fig14` from committed `writeup/data/p2_regular_profile.json`
(+ `..._traj.json`). Full write-up: `PHASE2_P2_NOTES.md` §7, `TECHNICAL_P2_CONJ24.md` §7.

What a human would want to know:

- **The reframe.** CHL's rescaled HL system has TWO fixed points: the singular Stage-2 anchor
  `(2,-1)` AND a regular, strictly-positive Stage-1 profile (their Scenario 2, §4). The prior logged
  run's "generic degenerate IC → a DIFFERENT state (0.680,-0.487), honest predicted NEGATIVE" is
  **not** a POC artifact — characterizing that final field shows it is smooth (`max|Ω_X|/peak≈0.3`
  vs `≈1061` for the singular anchor), single-signed, peaked at `X≈0.35` away from `X=1`. That is
  qualitatively CHL's Stage-1 regular profile. Our machinery reaches BOTH CHL attractors.

- **Why it matters / the honest guards.** This is a QUALITATIVE match (regular, +ve, peak off `X=1`),
  reached with the STANDARD `(2.4)`+degenerate gauge — NOT CHL's modified Scenario-2 formulation
  `(2.9)/(4.1)`. So NOT a proven identity; constants differ under the different normalization (ours
  `c_l≈0.5, c_ω≈−0.45`; theirs `(c_l,c_ω,c_r)=(1.0636,−0.4235,0.0765)`). Not novel, not a proof.

- **The B1/B2 scout (8000-step trajectory).** Under our gauge the generic trajectory TRANSITS the
  CHL-S2 neighborhood (`c_l≈1.06` near step 1200 — nearly the published value) but CANNOT hold it,
  then wanders in the low-`c_l` regular regime and NEVER approaches `c_l=2`. Diagnosis: our gauge
  pins `c_l=−U(1)` (stagnation at `X=1`), a mismatch for a profile peaked at `X≈0.35`; CHL's `(4.2)`
  pins at the ORIGIN. Decision: **B1 (implement `(4.1)/(4.2)`) is the recommended next brick** —
  cheap (`+c_r` in transport, a 3×3 gauge solve), with a clean KNOWN-ANSWER `(1.0636,−0.4235,0.0765)`
  we already fly within `~0.005` of. **B2 (the Stage-1→Stage-2 transition) is NOT reachable on a
  fixed grid** and mostly re-confirms CHL — wrong brick now. Lottery ticket still lives elsewhere
  (gCLM-family two-scale↔two-stage transition; or a rigor step).

## Phase-2 P2 — dynamic relaxation: Conjecture 2.4 (CHL) at POC, LOCAL attractor confirmed — 2026-07-25

Full record: writeup/4_p2_lottery/TECHNICAL_P2_CONJ24.md + BLOG_P2_CONJ24.md; evidence fig13 from committed
writeup/data/p2_conj24_relax.json (`python writeup/4_p2_lottery/p2_conj24_evidence.py`). Logged harness
experiments/p2_conj24_relax.py --logged (predicate LOGGED to git before the run). Machinery
solver/hl_rescaled.py::RescaledHLDynamic + test_hl_rescaled.py (7/7). This IS a logged gate run.

**Verdict: PARTIAL (by construction) — 9/9 pre-committed clauses hold.** The first genuine swing
of the lottery-ticket leg. It reproduces the LOCAL content of a numerical-only conjecture — Tier-2
independent confirmation, NOT novel, NOT a proof.

The chosen path this session (with the user): *scout HH23 first, then build+validate the stepper,
then reassess.* The HH23 scout (JOURNAL not needed — it's a read, banked in PHASE2_P2_NOTES.md §5)
returned NO-GO on the literal 3D link (mechanism + geometry mismatch; would overclaim) but surfaced
the real 1D-tractable question (two-scale vs two-stage). Then this run.

What a human would want to know:

- **The novel piece is the degenerate GAUGE, and it works.** CHH22 pins the origin slope
  Omega_x(0), which is exactly 0 for degenerate data. CHL (their (3.2)) instead read the NONLOCAL
  U_X(0)=H(Omega)(0) (nonzero even when the slope vanishes) + pin c_l=-U(1). Implemented and
  validated as a KNOWN-ANSWER test on the proven Thm-2.3 anchor: (c_l,c_omega)=(1.949,-0.969)≈(2,-1).
  A clean identity makes it a real test: at the anchor Theta_X-(U+c_l X)Omega_X = Omega_bar and
  H(Omega_bar)(0)=-1 exactly (the delta at X=1 cancels analytically).

- **Hit a real numerical wall and diagnosed it (didn't hand-wave).** The naive SSPRK3+upwind+spline
  scheme is UNSTABLE at the singular profile: starting AT the regularized anchor the residual grows
  25→3e3→1e9 and blows up by tau~1.4. Cause: non-dissipative spline slopes ring at the X=1
  discontinuity; the stiff Theta_X delta-source amplifies it. Same class of difficulty that drove
  CHL to adaptive mesh + WENO. Fix = subgrid dissipation nu*d²/ds² — a POC crutch (O(nu) bias), NOT
  their industrial solution, but enough to ask the question.

- **Locked the predicate BEFORE the logged run; 9/9 held; did NOT tune to pass.** Gauge-invariant
  only, declared PARTIAL by construction. Result (n=801, nu=0.02, 2500 steps):
  - anchor HOLD → (1.939,-0.927), residual 180→3.4 plateau (a stable hold, explicitly NOT →0),
    shape rel-L2 4.9%.
  - two perturbations → the SAME fixed point (within 0.06 in both constants), residual drop >5×:
    the LOCAL asymptotic stability CHL only asserted.
  - nu=0.04 → (1.936,-0.925), unchanged: the fixed point is robust to the stabilizer, not a
    nu-artifact; the residual floor scales with nu (controllable, not a wall).
  - generic far degenerate IC → (0.680,-0.487): it relaxes to a DIFFERENT self-similar state (low
    residual, wrong constants, 29% shape). The honest predicted NEGATIVE — the GLOBAL basin is
    beyond a fixed-grid POC. (Note the nuance: generic data doesn't blow up, it converges ELSEWHERE.)

- **NOT achieved (on purpose, stated out loud):** residual→0 (POC dissipation floor) and the global
  basin. Both need WENO/adaptive mesh + vanishing-viscosity + a semi-analytic X^{-1/2} outer patch
  (the same tail fix flagged for Spike-1 Step C). The genuinely-new leg (two-scale vs two-stage,
  §5) needs exactly those global-basin numerics — hence the reassessment point.

## Phase-2 P2 — the 1D Hou–Luo singular-profile machine, validated against an exact solution — 2026-07-25

Full record: writeup/4_p2_lottery/TECHNICAL_P2_HL_ANCHOR.md + BLOG_P2_HL_ANCHOR.md; evidence fig12 from
committed writeup/data/p2_hl_anchor.json (`python writeup/4_p2_lottery/p2_hl_anchor_evidence.py`). Working
doc PHASE2_P2_NOTES.md. Code solver/hl_rescaled.py + test_hl_rescaled.py (5/5). This is solver
dev + unit validation, NOT a logged gate run.

**What this is: VALIDATION of a proven result — machinery, not novelty, not a proof.** After
Spike 1 we scoped P2 = the actual novelty frontier, and decided (with the user, from evidence)
to attack the **1D Hou–Luo model** singular-profile scenario of Chen–Huang–Li (arXiv:2604.01868),
NOT 2D Boussinesq.

What a human would want to know:

- **Scouted before committing.** Read CHL page-by-page: the novel thing is *degenerate* data
  → *singular* self-similar profiles (two-stage L^∞→L^p), and only *weak existence* of one
  explicit profile is proven — the asymptotic *stability* is numerical-only. That gap is the
  frontier. Chose 1D over 2D because the novelty lives there first, it reuses line_hilbert +
  gCLM rescaling, and 2D would compound the Step-C tail problem.

- **A feasibility probe made the decision on evidence, not vibes.** Fed the singular profile
  Ω̄=(X−1)^{−1/2} to our line-Hilbert operator and compared to the exact H I derived. The
  operator SURVIVES: the singular core is representable to a few % and improving; the only real
  error is the slow X^{−1/2} tail, and it is TRUNCATION-limited (falls with domain reach M,
  immune to node clustering — measured, not asserted). Not a wall; the known outer-patch gap.

- **Derived a closed-form velocity for their profile.** From the classical Hilbert pair
  H(x₊^{−1/2})=−(−x)₊^{−1/2}: H(Ω̄)=−(1−X)^{−1/2}1_{X<1}, U̅=2√(1−X)−2 (X<1), −2 (X≥1). Three
  independent checks line up (U̅(0)=0; U̅(1⁻)=−2 = strong steady form; c̄_l+2c̄_ω=0 exactly). A
  small self-contained by-product the paper didn't spell out — and the known answer that makes
  the validation a real known-answer test (the Spike-0 discipline).

- **Five known-answer checks pass** (test_hl_rescaled.py): velocity operator vs arctan(2X)
  1.1e−5; full pipeline 1.8e−3; velocity on the singular anchor → U̅ converging at the ½-order
  the √-singularity predicts; steady residual of the exact profile 6.2e−3 converging; Θ
  consistency exactly 0.

- **Performance (the user asked).** Bottleneck was the shared line_hilbert.py build, not P2 code:
  batched Thomas slope solve (_slope_matrix 6.15s→0.29s, 21×), Horner+shared+shortened L(s)
  series (n=4001 build 65s→19.7s, 3.3×), lazy Hilbert matrix. HL suite >120s→3.9s. Accuracy
  IDENTICAL — line_hilbert 6/6, gclm 5/5, hl 5/5 all green (verified the operator change didn't
  move a single error digit).

- **NOT done (on purpose):** the dynamic relaxation + degenerate normalization — the actual
  novelty swing (does generic degenerate data converge to the singular profile?). That is a
  logged run with a pre-locked predicate; paused here at the user's request to bank the anchor.

## Spike 1 Step C — relax to the Chen–Hou profile (the gate): PARTIAL, honestly reported — 2026-07-25

Full record: writeup/3_spikes/TECHNICAL_SPIKE1_STEPC.md + BLOG_SPIKE1_STEPC.md; evidence fig11 from
committed writeup/data/spike1_stepC_gate.json (`python writeup/3_spikes/spike1_stepC_evidence.py`).
Harness experiments/spike1_stepC_gate.py (predicate LOGGED to git before the run, commit
eabb418). This IS the logged gate run.

**Verdict: PARTIAL — 3 of 4 pre-committed checks pass, the far-field exponent check FAILS. Does
NOT pass the gate. Goalposts NOT moved.**

What a human would want to know:

- **The pre-committed predicate did its job.** We locked the pass/fail bar (alpha within 5%,
  far-field exponent within 10%, anisotropy <0.23, resolution-stable) in git *before* the run.
  It came back PARTIAL and we report PARTIAL — the whole point of WIN_CONDITION.

- **Found a bug, diagnosed it properly, fixed it.** First runs drifted: gauge-invariant alpha
  settled right (~-0.35) but c_l,c_om drifted individually and the run destabilized (~step 8000).
  Rather than hand-wave, we MEASURED the drift rate vs grid (experiments/diagnose_stepC_drift.py):
  it ~halves under n_r refinement and worsens as r_min shrinks -> a NEAR-ORIGIN TRUNCATION
  artifact, not a broken method. Fix: renorm=True re-pins omega_x(0),eta_x(0) each step (discrete
  enforcement of the paper's (2.12)); drift arrested, run stable. Standard dynamic-rescaling move,
  rediscovered by watching what breaks without it. test_renorm_pins_gauge added.

- **The good half (checks 1,3,4 PASS).** c_omega matches Chen–Hou to <0.5% across all configs
  (-1.026..-1.031 vs -1.0294) — and c_omega is the REAL result (it evolves via u_x(0) to the
  profile value while c_l is pinned to the gauge). alpha ~ -0.335 (2%), resolution-stable.
  Anisotropy ~0.026 << 0.23 — the profile's strong x/y anisotropy (2.24) reproduced.

- **The failing half (check 2 FAIL), stated straight.** The directly-fitted far-field exponent
  is ~-0.31 (7-13% off -0.342) and moves the WRONG way with n_r. Honest causes: (i) a PROTOCOL
  confound — fixed 2500 steps means higher-n_r runs reach smaller tau (under-relaxed; the slow
  r^{-1/3} tail forms last); (ii) POC limits — domain 1e5-1e6 vs the paper's 1e15, outer BC
  steepens the tail, no semi-analytic r^alpha split, 2nd-3rd order vs 6th-8th B-splines. A clean
  tail match needs the paper's apparatus. Did NOT re-run longer to chase a pass (that would be
  goalpost-moving); flagged fixed-tau protocol as future work.

- **Honest framing.** Even a clean pass reproduces a PROVEN result (Chen–Hou 2022) on a toy model
  across Wall C — validates machinery, NOT novel, NOT a proof. Clay ~0.05%. This is Tier-1/2: the
  machine captures the profile's core (invariants + anisotropy) with its POC limits located.

- **Next (the actual lottery ticket, P2).** Spike 1 has validated the stretched-grid dynamic-
  rescaling machinery end-to-end. The interesting move is to point it at a profile NOT already in
  a theorem (stable-vs-singular target: Chen–Huang–Li arXiv:2604.01868 in Papers/; or 3D-axisym).
  Deferred post-Spike-1 forks now actionable with the working machine.

## Spike 1 Step B — rescaled 2D Boussinesq RHS + modulation + SSPRK3, ASSEMBLED & VALIDATED — 2026-07-24

Full record: PHASE2_SPIKE1_NOTES.md §3 ("STEP B COMPLETE"). Code: `solver/boussinesq_rescaled.py`.
Suites: `test_boussinesq_transport.py` (5/5) + `test_boussinesq_rescaled.py` (7/7). NOT a logged
gate run — solver development validated piece-by-piece against manufactured known answers. The
scientific gate (does the steady state = the Chen–Hou profile?) is Step C, still to run.

What a human would want to know:

- **Grounded, then a fork the user made me EARN with data.** Transcribed the exact rescaled
  system (2.10)/(2.28), normalization (2.11)/(2.12), and — the payoff of re-reading Part I —
  the *precise* gate constants (2.23): c̄_l≈3.006499, c̄_ω≈−1.029425, ū_x(0)≈−2.532674, ratio
  ≈−2.92056, α≈−0.3424 (sharper than the round −2.92/−1/3 I'd been carrying). Also learned the
  paper evolves the *derivatives* (ω, η=θ_x, ξ=θ_y), not primitive (ω,θ).

- **The formulation decision, settled empirically (user asked "are there tests?").**
  `experiments/spike1_stepB_decide_formulation.py`: reading θ_xx(0) off primitive θ is an r²-curvature of two
  even modes, and the cos2β mode carries only (θ_xx−θ_yy) — contaminated by θ_yy. Measured **~2×
  worse and ~2× more noise-sensitive** than reading θ_xx(0)=η_x(0) as a clean *linear r-slope* of
  η's single odd cosβ mode. Ruled out primitive-θ. User chose the **full 3-field (ω,η,ξ)** (keep
  the v_x·ξ coupling) so the fixed point is *exactly* the Chen–Hou profile — a faithful gate.

- **The angular bases finally pinned down.** The sine basis was ONLY for φ (zero on both walls).
  The transported fields: ω,η odd-in-x → {cosβ,cos3β,…} (zero at axis, free at wall); θ,ξ
  even-in-x → {1,cos2β,…}. Transport uses β finite differences (basis-agnostic), so it didn't
  care; the origin reads and parities do.

- **The elegant confirmation.** c_l = 2η_x(0)/ω_x(0) is a RATIO of two same-basis slope reads, so
  the projection's quadrature bias **cancels**: c_l recovered to ~3e-16 in the test even though
  each slope alone carries ~2e-5. The thing the whole scheme's stability hinges on is the
  best-conditioned quantity in it.

- **Built de-risked, crux-first (Step-A discipline).** Piece 1 transport kernel (2D upwind on the
  curved log grid, the Spike-0 3rd-order Shu stencil generalized): manufactured rel err ~9.5e-6,
  order ~2.98, rigid-rotation→0 exact, far-field CFL cure carries to 2D. Pieces 2–4: grad_xy
  (order ~1.97), origin reads, modulation, then the coupled SSPRK3 integrator — RHS wiring locked
  by a term-by-term re-assembly test, and the whole machine steps stably (finite c_l,c_ω).

- **Honest status.** This is the MACHINE, validated to run. It is NOT yet shown to reproduce the
  profile — the smoke-test c_l≈1.06 is an arbitrary-blob transient, not a relaxation. And per the
  standing steer, even a flawless Step C reproduces a PROVEN result across Wall C: validates
  machinery, not novel, not a proof. Clay odds ~0.05%; the lottery ticket is post-Spike-1.

- **Next: Step C (the gate, a LOGGED run).** Needs (i) an initial guess in the profile's basin
  and (ii) a pre-committed pass/fail predicate (c_l,c_ω,ratio,α + shape, resolution-stable) fixed
  BEFORE the run. Both are genuine decisions — check in with the user first. Watch the r_min
  inflow inner-BC for domain/resolution sensitivity (flagged, not yet stressed).

## Spike 1 Step A — 2D Boussinesq velocity operator on a stretched grid, VALIDATED — 2026-07-24

Full record: PHASE2_SPIKE1_NOTES.md; technical writeup/3_spikes/TECHNICAL_SPIKE1_VELOCITY.md; blog
writeup/3_spikes/BLOG_SPIKE1_STEPA.md. Code: `solver/boussinesq_velocity.py`,
`test_boussinesq_velocity.py` (5/5 pass). NOT a logged gate run — solver development
validated against a manufactured known answer. Evidence figure fig9 + committed data
rebuild: `python writeup/3_spikes/spike1_stepA_evidence.py`.

User chose Spike 1 (2D Boussinesq port), **de-risked variant**: build + validate the
highest-risk new piece (the 2D velocity operator `u = ∇^⊥(−Δ)⁻¹ω`) standalone before
wiring the full rescaled solver. Step A is that piece — the 2D analogue of Spike-0's
non-FFT line Hilbert (on the uniform grid it's a trivial FFT; the real profile's slow
`r^{−1/3}` tail forces a stretched grid where FFT can't go).

What a human would want to know:

- **Grounded first, not reinvented.** Pulled Chen–Hou Part I (arXiv:2210.07191) + the MMS
  rigorous-numerics paper (2305.05660) into `Papers/` (gitignored) and transcribed the
  formulation exactly: physical (2.3)–(2.5), one-scale dynamic rescaling (2.10), modulation
  (2.11), half-plane Poisson velocity with `φ=0` on the wall, far-field `ω~r^α`,
  `α=c_ω/c_l≈−1/3`, gate target `c_l/c_ω≈−2.92`. WebFetch couldn't ingest the papers (size
  limit) — the user downloaded the PDFs; `Read` handles them page-by-page.

- **Correction banked:** the "two-scale rescaling" worry in the planning notes was from
  Chen–Hou's *earlier C^{1,α}-boundary* paper, NOT this smooth-data profile, which is
  **one-scale**. So Spike-0's one-scale-is-attracting headline is the relevant precedent.

- **The elegant win.** On a **log-radial** grid (`r=e^ρ`) with the Dirichlet **angular
  sine** basis `sin(2nβ)`, the polar Laplacian's `1/r`, `1/r²` terms cancel and `−Δφ=ω`
  decouples per mode into a constant-coefficient tridiagonal ODE
  `φ_n''(ρ) − (2n)²φ_n = −r²ω_n` — one Thomas solve per mode, no scipy sparse. The
  `r^{±2n}` homogeneous tails carry origin-regularity + far-field decay (the `r^{−1/3}`
  lever at POC level).

- **Validation (manufactured known answer, the house rule).** `φ*=r²e^{−r}sin2β +
  r⁴e^{−r}sin4β` → recover `u,v` to rel L∞ **~6e-5**, radial convergence order **2.00**
  (clean log-log line, not a lucky grid), and the modulation origin read **`u_x(0)=−2.0008`**
  vs −2 (that steering signal was a noise-amplifier in 1D recon; the angular-mode structure
  makes it clean here).

- **Honest POC scope (stated explicitly, flagged to user).** Chen–Hou's full apparatus
  (6th–8th-order B-spline FEM Poisson, adaptive mesh to `10¹⁵`, semi-analytic far-field
  split, `10⁻⁷` residual, INTLAB interval bounds) is months-scale and mostly built for the
  *proof*. The plan pre-committed Spike 1 to qualitative fidelity, so Step A uses a
  tractable **validated** Poisson solve (legitimate: an elliptic solve is textbook, unlike
  the exotic 1D line Hilbert) with the same mathematics. Reproduces a proven result across
  Wall C — validates machinery, NOT novel, NOT a proof.

- **Next:** Step B (rescaled RHS `(c_l x+u)·∇` + buoyancy `θ_x` + modulation, SSPRK in τ,
  with the `ζ=θ/x` substitution), then Step C (relax to the Chen–Hou profile — the gate).
  The stable-vs-singular target fork the user raised stays deferred to the post-Spike-1
  gate, when the working machine can probe both.

## Spike 0 COMPLETE — dynamic rescaling POC recovers the CLM profile + rate against the known answer — 2026-07-24

Full record: PHASE2_SPIKE0_NOTES.md ("SPIKE 0 COMPLETE" section). Code:
`solver/gclm_rescaled.py`, `test_gclm_rescaled.py` (5/5 pass, ~48s). NOT a logged gate
run — solver development validated against a closed-form known answer.

The dynamic self-similar rescaling technique is validated end-to-end in 1D. On a
sinh-stretched whole-line grid, CLM (a=0) dynamic rescaling recovers the exact profile
Ω̄₀=−4X/(1+4X²) to shape error ~2e-6 with the exact self-similar rate c_ω→−1, and it is
resolution-stable. This de-risks the whole method before the 2D port (Spike 1).

What a human would want to know:

- **The headline finding overturns recon finding-3.** The recon feared one-scale
  rescaling was unstable (the profile overshot and blew up in the rescaled frame → the
  Chen–Hou two-scale motivation). That instability was an **artifact of the wrong
  (periodic) Hilbert transform + integral modulation**, NOT fundamental. With the correct
  LINE Hilbert transform and value-based normalization (c_ω=1−HΩ(0), c_l≡1), Ω̄₀ is a
  clean **attractor**: two different perturbed odd ICs (Gaussian, narrower Lorentzian)
  both relax to it. One-scale suffices for CLM. (Whether Boussinesq/De Gregorio re-needs
  two-scale is a Spike-1 question — different mechanism.)

- **The scheme, reduced for CLM:** evolve f=Ω/X in the computational coordinate ρ
  (X=c·sinh ρ); the dilation becomes tanh(ρ)·f_ρ (speed ≤1 → CFL ~ Δρ independent of the
  reach M — the uniform-grid CFL death is cured). 3rd-order upwind (smooth profile → the
  paper's nonlinear WENO limiter is overkill at POC; outflow at both ends means upwind
  stencils reach inward, no ghosts) + SSPRK3. The origin slope f(0)=−4 is frozen to
  machine precision by the scheme itself (advection speed and source both vanish at ρ=0).

- **Honest scope, stated plainly:** this reproduces a *proven closed-form* toy result
  across Wall C — it validates machinery, it is NOT novel and NOT a proof. I deliberately
  did NOT claim the physical T*=2 from the whole-line run: T* belongs to the global
  periodic solve (already covered by test_solver_clm.py); a whole-line rescaling's initial
  amplitude is a free gauge, so its correct analogue is the *rate* c_ω→−1 (⟺ ω~(T−t)⁻¹),
  which it nails. The log-kernel velocity U was correctly deferred (CLM doesn't use it).

- **Gate reached (each spike STOPS for review, per PHASE2_NUMERICS_PLAN.md).** Technique
  de-risked in 1D. Forward decision = Spike 1 (2D Boussinesq port, the real multi-week
  lift) vs. first exercising a≠0 / De-Gregorio singular-profile targets in 1D (which need
  the deferred velocity U + AMR). Raised to the user as a scope decision.

## Spike 0 — the crux is BUILT: line Hilbert transform on a stretched grid PASSES against the known answer — 2026-07-24

Full record: PHASE2_SPIKE0_NOTES.md ("BUILT" section). Code: `solver/line_hilbert.py`,
`test_line_hilbert.py` (run `python test_line_hilbert.py`; 6/6 pass). NOT a logged gate
run — solver development against a closed-form known answer.

The hardest, most-de-risking component of Spike 0 now works. The whole-line Hilbert
transform on a non-uniform sinh-stretched grid maps `−4X/(1+4X²) → 2/(1+4X²)` (the exact
CLM self-similar pair) to **relative error 1.6e-4**, POC target was 1%, with clean
monotone convergence (2.35e-3 → 5.22e-4 → 1.16e-4) under whole-line refinement.

What a human would want to know:

- **This was THE crux** (per the recon notes and the standing steer): the stretched grid
  forces a NON-FFT Hilbert transform, and that spline-analytic transform was the one piece
  the periodic solver couldn't provide. It's now validated in isolation with a hard
  pass/fail against an answer we know exactly. The rest of Spike 0 (the time-stepper) is
  comparatively standard.

- **I derived the A,B basis-Hilbert formulas instead of transcribing the paper's minimax.**
  The recipe warned pdftotext mangles Appendix C's 23-term coefficient lists. Rather than
  hand-copy them, I substituted the Taylor split `ln|1−s| = L(s) − s − s²/2 − s³/3`
  (`L = −Σ_{n≥4}sⁿ/n`) into the exact closed forms; the cancellation cancels *analytically*.
  This reproduced the paper's minimax structure (exactly for B; the OCR's orphaned leading
  `−` confirmed the A sign) and is verified by branch-continuity at |s|=0.5 and against the
  raw closed form. **The minimax transcription the recipe flagged as risky is unneeded.**

- **Honest scope:** this validates machinery against a *proven* toy result, not novelty.
  The dominant error is ~1/M tail truncation (the profile's 1/X decay), expected and fine
  at POC level. No scipy in the venv, so the natural cubic spline slopes are hand-rolled
  (Thomas). `line_hilbert_matrix(x)` gives a reusable dense operator for the time-stepper.

- **Next increment:** `solver/gclm_rescaled.py` — the stretched-grid time-stepper (evolve
  f=Ω/X, k=1; c_ω=1−HΩ(0), c_l=1) + `test_gclm_rescaled.py` (steady residual at Ω̄₀, then
  convergence from perturbed odd data → c_ω→−1, T*→2, resolution-stable). The log-kernel
  velocity U (C.1 C,D elements) is a≠0-only, so deferrable for the CLM POC.

## Spike 0 reconnaissance (dynamic rescaling on 1D gCLM) — 2026-07-24 — scheme grounded on exact known answer; uniform-grid CFL dead-end; Appendix C recipe in hand; solver NOT yet built

Full record: PHASE2_SPIKE0_NOTES.md. Scratch code: phase2_spike0_probe.py (periodic,
kept as a negative example). Commits d39a504, 3242158, 9ed940f. This is NOT a logged
gate run — it is solver-development reconnaissance (cheap probes before the real build),
in the project's "learn before you build" spirit.

Goal: implement dynamic (self-similar) rescaling on the 1D gCLM solver and validate it
recovers a *known* self-similar blow-up before porting to 2D Boussinesq (Spike 1).

What a human would want to know:

- **The known-answer target is CLM (a=0):** data w0=−sin x → blow-up at x=0, T*=2,
  exact self-similar profile Ω̄₀(X)=−4X/(1+4X²), H(Ω̄₀)=2/(1+4X²), c_ω→−1. I first
  derived the rescaled equation + this profile by hand; later confirmed *identical* to
  Huang–Tong–Wang arXiv:2603.25104 (the exact gCLM dynamic-rescaling paper).

- **Three false starts, each a finding** (probes v1→v4, phase2_spike0_probe.py):
  (1) pointwise high-derivative normalization (pin Ω_yyy(0)) is a NOISE amplifier —
  the (ik)³ multiplier makes Ω_yyy(0) read ~1000 vs the analytic 1; use integral
  modulation. (2) A periodic pseudo-spectral run is *stable but converges to the WRONG
  profile* (fitted B≈−1, not the CLM value 4) — because the true profile is a whole-line
  ~1/X function needing the LINE Hilbert transform, and periodic H ≠ line H for slow
  tails. My earlier "periodicity is fine" read was an artifact of the wrong (periodic) H.
  (3) On a large *uniform* whole-line grid the line-H works (~1/M truncation err) but the
  −c_l X Ω_X dilation NaNs — diagnosed as a **CFL limit** (advection speed is X up to M,
  so dt < dX/M ≈ 1e-4; a spectral filter did not help). Uniform grid = wrong tool.

- **Grounding closed all gaps (the session's repeated lesson: read the paper, don't
  trial-and-error).** arXiv:2603.25104 gives: rescaled eqn Ω_τ=(c_ω+HΩ)Ω−c_l X Ω_X;
  a=0 normalization c_l=1, c_ω=1−HΩ(0) (value-based, robust). Appendix C gives the
  discretization: **C.1** line Hilbert transform via C¹₀ cubic-spline basis with analytic
  H(P_i),H(Q_i) (closed-form A,B,C,D + minimax series) — works on a NON-uniform grid where
  FFT cannot; **stretched cosh/sinh grid** X(ρ) with dX~X·Δρ so the dilation CFL ~ Δρ is
  independent of M (this cures the uniform-grid death); **C.2** WENO5 advection +
  SSPRK(10,4), evolve f=Ω/Xᵏ, converge ‖f_τ‖<1e-8. Full recipe banked in the notes.

- **Honest status:** Spike 0 is de-risked and fully specified but the solver is NOT built.
  Next increment: solver/line_hilbert.py + test vs the −4X/(1+4X²)↔2/(1+4X²) pair
  (the crux, self-contained, hard pass/fail). Confirmed a genuine multi-day build.

## Phase 2 route decision — 2026-07-24 — Phase 1 fitness search concluded; numerics upgrade (dynamic rescaling) chosen over AMR; NOT roadmap "Route D"

Full record: PHASE2_NUMERICS_PLAN.md. Commit e7e0e3b. Decision made WITH the user via a
reviewed options menu (per the standing "raise genuine scope decisions" steer).

Context: the uniform-grid fitness search concluded with a decisive negative (two
currencies — ν_crit, g_frac — both fail the honest gate via the same free-split ω₀→0
wall; root cause: on a uniform grid the singular structure forms below grid scale).
Standalone packaging of that negative: writeup/2_phase1_2d/NEGATIVE_RESULT_TWO_CURRENCIES.md
(commit 9cd2b21) — the Option-C deliverable this session.

What a human would want to know:

- **The forward move is a numerics upgrade, not another fitness.** Researched the field
  (Chen–Hou; Wang–Lai–Gómez-Serrano–Buckmaster; the 2025–26 unstable-profile frontier).
  Three paradigms: (P1) dynamic self-similar rescaling — time-integrate in a rescaled frame
  so the blow-up is a steady profile on a fixed grid; (P2) direct profile construction
  (Newton/PINN) — the current novelty frontier; (P3) AMR. **Chose P1**, reject P3: P1
  reuses the validated solver, dissolves the below-grid-scale wall (fitness on RESOLVED
  structure), and its late-time state IS a self-similar profile (the on-ramp to P2).

- **Terminology guard banked:** the AMR / self-similar-rescaling upgrade is a Route-A
  *numerics* upgrade, NOT roadmap "Route D" (the later Tier-3 computer-assisted-proof leg).
  Fixed this mislabel in writeup SUMMARY.md + README.md.

- **Honest catch surfaced (matters for the lottery ticket):** the literature's real novelty
  frontier is P2 profile construction of UNSTABLE profiles, not evolve-ICs search. P1 mainly
  finds the *stable* CLM/Boussinesq blow-up (which Chen–Hou already proved). So P1 is framed
  as the shared substrate + on-ramp; A-vs-B (evolve-ICs vs profile-hunting) is a gate to
  re-decide AFTER Spike 1, with a working rescaling solver in hand. User approved: do Option-C
  writeup first (done), then build Spike 0.

## Reformulated Gate 4 (g_frac) — 2026-07-24 — FAIL 4/6: free-split rails to ω₀→0, split-dominated + t_res proxy

Full results: PHASE1_GATE4_REFORM_RESULTS.md. Frozen predicate:
PHASE1_GATE4_REFORMULATED_PREDICATE.md. Scripts: phase1_gate4_reform.py +
analyze_phase1_gate4_reform.py (commit 13d888f, pre-run). Data:
experiments/phase1_gate4_reform.jsonl → writeup/data/phase1_gate4_reform.json.
The user reviewed + signed off the frozen predicate (3 improvements folded in:
rank-stability across 128→256→512, split-dominance promoted to gate condition 6g,
t_res-proxy check 6h; plus winner-not-at-split-rail 6b′ from designing the
adversarial roster). 138 solves (40 shapes × {128,256,512} + 18-shape split-sweep).

What a human would want to know:

- **The gate did its job and returned a decisive negative.** g_frac passes 1,2,3,5
  (discriminating, direction-correct, well-posed/window-robust +0.989, wide band)
  and its RANK is resolution-stable (+0.889, +0.926 — the de-risk result holds).
  But property 6 fails hard on FREE split.

- **The ω₀ cheat returns exactly as it killed ν_crit.** The de-risk fixed split=0.5
  (pinning ω₀). Free split lets the optimum drive ω→0 for max buoyancy forcing: the
  TOP-5 shapes at N=512 are all split 0.93–0.99, winner rand_18 split=0.99
  centroid=1.56. ρ(g,log|ω₀|)=−0.66. The controlled split-sweep STILL showed
  interior optima (property 6f passed) — but the free-roster WINNER rails anyway,
  because at free structure a high-split shape beats the interior-optimum structured
  ones. The sweep couldn't see it; the winner interrogation did. (Banked lesson
  reasserted: a controlled sub-test passing ≠ the winner being honest.)

- **6g confirmed the split-dominance finding as a gate condition:** partial
  ρ(g,centroid|split)=+0.11 < 0.15 — once split is controlled, g_frac barely ranks
  ω-geometry. And 6h: partial ρ(g,centroid|t_res)=−0.39 — g_frac is largely a
  formation-time proxy. Binning on split alone would NOT rescue it (it's also a
  t_res proxy).

- **Property 4's second axis (new here) also failed:** grower/non-grower
  CLASSIFICATION is not resolution-stable — 7/37 shapes are coarse-grid
  false-growers (t_res climbs to 4.0 as N grows; e.g. advlo_s20 2.91→3.56→4.00),
  textbook under-resolution false-positives. Rank-stable ≠ classification-stable.

- **Strategic read (the user's Clay-lottery focus):** TWO currencies now hit the
  same uniform-grid wall (ω₀→0 degeneracy); g_frac adds a t_res-proxy problem. A
  THIRD uniform-grid scalar currency is the weeds. Genuine structure lives below
  grid scale → the honest path to a structure-tracking fitness AND to Tier-2 is
  Route D (AMR / self-similar rescaling). Teed up as the next-session decision.

## g_sustained 256→512 rank check — 2026-07-24 — the rank SURVIVES the wall (Spearman +0.905), cheat audit clean at N=512

Full results: PHASE1_GSUSTAINED_RESULTS.md (Consequence section — the de-risk this
resolves). Script: phase1_gsustained_rankcheck.py (commit 19d51c0). Data:
experiments/phase1_gsustained_rankcheck.jsonl. This is the ONE expensive leg the
staged probe paused on: does g_frac's *ranking* hold at higher N, or is even the
rank on the uniform-grid wall? The user green-lit running it (over accepting the
negative now / pivoting to Route D).

What a human would want to know:

- **The rank holds across a doubling.** Spearman(rank@256, rank@512) = **+0.905**
  (precommitted bar > 0.85; 20/20 shapes finite). Essentially identical to the
  +0.90 at 128↔256 — the ordering did NOT degrade with resolution. The rank is not
  on the wall even though the magnitude is (g_frac@512 > g_frac@256 for every
  grower, e.g. struct_diag 0.33→0.74; the wall is real, only the order is stable).

- **Cheat audit re-run AT N=512 is clean** (not carried over from 256 — the banked
  lesson is that a rank can be stable AND cheat-organized): winner rand_01 is a
  genuine grower (t_res 2.95), top-5 all growers (5/5), ρ(g,log|ω₀|)=+0.21 (no ω₀
  cheat), ρ(g,centroid)=+0.31 (structure), ρ(g,t_res)=−0.70. Consistent with the
  256 audit.

- **The known-cheat control did its job.** accel_ratio was also rank-stable
  (+0.853) but winner rand_08 is a non-grower and ρ(accel_ratio,early_rate)=−0.58 —
  the small-denominator cheat, correctly separated from g_frac. The audit
  discriminates honest-vs-cheat even when both are rank-stable.

- **Ops note (a mistake, banked as a lesson, not a science problem):** the run
  finished cleanly but my monitoring hid it for ~10 min. A `while pgrep -f
  'script.py'` waiter matched *itself* (its own argv contains the string) so it
  never exited/notified; track.py's `py or raw` fallback then counted the leftover
  bash wrappers as a live producer and kept printing RUNNING. Fixed both
  (track.py commits aa402da, 81d592f): never wait on a pgrep pattern that matches
  the waiter, and never fall back to non-python matches when checking a python
  producer's liveness. The science/data were unaffected — all 40 solves present.

- **Verdict → forward.** Outcome (1): the g_frac rank-based currency survives the
  de-risk. Next is the reformulated 40-shape Gate 4 (property-4 ⇒ RANK-stable,
  property-6 ⇒ evaluated controlling for split). Paused at a checkpoint to review
  the reformulated predicate wording before spending the gate — reformulating an
  anti-self-deception predicate is exactly the step not to do unilaterally.

## g_sustained staged probe — 2026-07-24 — fixed-window magnitude fails (same wall); rank-based g_frac survives

Full results: PHASE1_GSUSTAINED_RESULTS.md. Data:
experiments/phase1_gsustained_probe.jsonl → writeup/data/phase1_gsustained.json.
This is the STAGED, cheap-first probe of the two Gate-4 forward refinements
(fixed-absolute window; free-split property-6), run before any 40-shape gate. The
user picked "continue staged (cheap caveat first)" at each fork, and the probing
kept paying off — it caught a second cheat and reframed the whole deliverable.

What a human would want to know:

- **The fixed-window refinement fails, and the reason is structural.** I measured
  the labeled ICs at N=128/256/512 and *looked at the trajectory* (window_diag
  scratchpad probes) before trusting any window. smooth_sharp re-accelerates right
  at the edge of its trusted window, and tail_guard pushes that edge out with N
  (t_res 2.46→2.74→2.98), so g_frac climbs 0.663→0.793→0.968 and never converges.
  Any window stable enough to avoid the drift sits in the earlier region where the
  spike already showed mild>sharp. You get stable OR blow-up-predictive, not both.
  This is spike finding #3 (near-singularity rate never resolution-converges on a
  uniform grid) reasserting — the SAME wall as ν_crit, on the growth-rate axis.
  Two currencies, one wall.

- **The rank order is what survives.** For a QD map only the ranking must be
  N-stable (bins are on resolution-stable descriptors). Spearman(rank@128,
  rank@256) = +0.90 for g_frac — the magnitude is on the wall but the order holds.

- **A second cheat, caught by the same reflex.** accel_ratio (late/early rate) was
  MORE rank-stable (+0.95) but is a small-denominator cheat: its winner rand_08
  never under-resolves (a non-grower), it mis-ranks the labeled ground truth
  (rand_08 +3.6 > sharp +1.4), and ρ(accel_ratio, early_rate) = −0.66. Its
  stability was real and worthless — it was stably ranking by the cheat. The
  banked lesson repeated: a rank-stable winner is a floor, not a ceiling; always
  interrogate against the dumbest cheat. g_frac passes the same audit clean
  (winner a grower, top-5 all under-resolve, ρ(g,log|ω₀|)=+0.17, ρ(g,centroid)=+0.31).

- **Caveat 2 (free split) is favorable.** No trivial max-split rail: a controlled
  split-sweep at fixed structure has an INTERIOR optimum (~0.3–0.5). The free-roster
  ρ(g,split)=+0.73 looked worrying but split↔ω₀ are mechanically entangled
  (ρ=−0.92); partial ρ(g,log|ω₀| | split)=+0.04 proves the ω₀ cheat is ABSENT and
  partial ρ(g,split | log|ω₀|)=+0.41 shows the split preference is genuine buoyancy
  physics. Honest caveat: split (logged, not binned) dominates ω-geometry.

- **Discipline notes.** Ran the 11-suite set (11/11) and committed the probe
  script (c1cf817) before the logged run; the run reproduced every scratchpad
  number exactly. STOPPED for review at the one remaining, expensive de-risk:
  256→512 RANK stability. If the rank holds → full reformulated (rank-based) Gate 4
  with property 6 evaluated controlling for split; if not → accept the negative.

## Gate 4 — 2026-07-24 — ν_crit FAILS property 6; inviscid growth-rate currency promising

Full results: PHASE1_GATE4_RESULTS.md. The headline: the pre-committed six-property
predicate printed 6/6 PASS, but that was a **false pass** — and catching it is the
whole point of the substantive re-analysis.

The frozen predicate (committed `5957155` before the run) anticipated the *1D*
property-6 failure mode (optimum → low-mode concentration) and tested spectral
centroid, which came back innocent (ρ=−0.15). But the real 2D degeneracy is
different: the smooth genome's free ω/θ split lets the "optimum" drive max|ω₀|→0,
trivially inflating amp=max|ω|/max|ω₀| (with κ=0 the undamped θ re-forces ω past
any viscosity). Diagnostic that caught it: **ρ(ν_crit, log|ω₀|) = −0.90**, slope
−2.11, R²=0.755 — ν_crit is 75% just the initial amplitude. Smoking gun: two
shapes reaching the SAME absolute vorticity get a 197× ν_crit gap from ω₀ alone,
and rand_24 grows MORE absolutely than rand_18 yet ranks 31× lower (the metric is
inverted vs propensity). A human asked exactly the right question — "be sure it's
actually a failure" — which forced the confirming analysis rather than trusting
the predicate's letter.

Then the disciplined ladder (each cheap, each decided on data): (1) fix the split
→ doesn't rescue (ρ(ν,log|ω₀|) −0.90→−0.44 persists; winner still trivial;
ρ(ν,centroid)=−0.21, the νk² dissipation wall reasserting). (2) normalized
resistance ν_crit·centroid² → only TAUTOLOGICALLY relocates the trivial optimum
(the centroid² multiplier dominates; struct_high has higher raw ν_crit but ranks
below struct_33 on centroid² alone) — exactly STAGE_2_5's "moves the trivial
optimum, doesn't remove it." So the ν_crit failure is the gCLM dissipation wall
reconfirmed, fundamental not fixable.

(3) One more currency (user decision): inviscid **sustained growth rate**
g_sustained escapes both cheats — inviscid (no νk² wall) + a rate not a ratio (no
ω₀ denominator). Probe clears the exact bars ν_crit failed: direction sharp
+0.79>mild +0.42>control 0.0; ρ(g,log|ω₀|)=+0.24 (cheat gone); ρ(g,centroid)=+0.38
(FLIPPED from ν_crit's −0.21 — structure rewarded). Necessary-not-sufficient
caveats: resolution-stability only modest (sharp 0.66→0.79, fractional window
drifts with t_res — fix with a fixed-absolute window); free-split untested (g
likely tracks split — real physics but a possible max-split triviality). A human
chose to DOCUMENT + pause before any further compute — banking the whole arc
before deciding the g_sustained Gate-4 path.

Compute note: the N=512 warm-start + 8 workers worked, but N=512 solves were
memory-bandwidth-bound (~12 min each under 8 concurrent FFT workers, ~3× a lone
solve). Stopped at 36/40 N=512 — property 6 is decided by N=256, and property 4
(the only thing the last 4 add) already passed on 36 shapes (all |Δν|≤½·tol).

## Gate 3 — 2026-07-24 — smooth 2D genome + ν_crit-analog fitness (built, no logged run yet)

Built the Gate-3 machinery: a smooth Hou–Luo-subspace genome
(`ga/genome2d_smooth.py`), the ν_crit-analog fitness wired through
`solve_boussinesq` (`ga/fitness2d.py`), and `test_genome_2d.py` (12/12; full
11-suite gate green). No logged experiment — Gate 3 is infrastructure; the first
logged 2D-genome run is Gate 4.

Genome design: ω = Σ a_jk sin(jx)sin(ky) (odd-x/odd-y, K=4), θ = Σ b_jk
cos(jx)sin(ky) (even-x/odd-y, j=0..K incl. the x-constant Luo–Hou modes). One
JOINT energy normalization pins total field energy at 2·ENERGY_BUDGET_2D, so the
overall-amplitude cheat (scale both fields up → needs more ν to kill; the 2D
analog of the 1D w→λw cheat) is removed, while the ω/θ energy RATIO (buoyancy
strength) stays free and is read off as the `split` descriptor. Confirmed
physically: because ν_crit is the fitness, a free overall amplitude WOULD be a
cheat (bigger fields need more viscosity) — fixing the budget is necessary, not
cosmetic.

MAP-Elites descriptor decision (raised with the user, then de-risked with a cheap
check before deciding). Candidates: anisotropy, spectral centroid, ω–θ alignment,
ω/θ split. A pure-genome probe (4000 random parity genomes, NO solver, seconds)
found: all four are mutually orthogonal (max |Pearson r| = 0.012 — none redundant,
unlike the 1D centroid/energy_top_k pair) and every pairing fills a 12×8 archive
at ≥0.83 coverage. So the cheaply-checkable failure modes are ABSENT for all
candidates — no empirical winner. The real differentiator (fitness-correlation →
archive collapse) is NOT cheaply measurable but comes free from Gate 4, so the
insurance move is: **bin on anisotropy × centroid, LOG all four raw** → binning
becomes a post-hoc, zero-re-run choice Gate 4's ν_crit data can overrule.
Rationale for the pair: both pure-geometry (unlikely to BE the fitness, keeping
cells populated), and the property-6 low-mode-collapse trap lands legibly on the
centroid axis. User approved.

Discipline notes: (1) the fitness reuses `ga.fitness.bisect_critical` with the v3
amplification-only predicate (amp≥2×, monotone in ν; an in-window slope is not —
the axis-screen smoke proved it), and its monotone-probes are exactly the Gate-4
property-6 instrument. (2) tail_guard makes the fitness read only the resolved
window. (3) The test suite's anti-self-deception anchor: a non-buoyant (2D Euler)
control conserves max|ω| → amp≈1 < 2× → ν_crit censored low (=0), confirming the
axis responds to the buoyancy mechanism, not merely to carrying a vortex.

## phase1_axis_screen (9033e6f) — 2026-07-23 — route fitness on ν_crit-analog

Why run BEFORE picking a fitness axis: the spike proved a resolution-stable
growth signal exists but flagged the confound — the windowed rate g is stable yet
NOT blow-up-predictive (smooth_mild has higher g yet saturates; smooth_sharp
lower g yet blows up). Rather than pick the axis on priors, a human asked the
right question: use the spike's two LABELED ground-truth ICs as a cheap
discriminator. Sharp BLOWS UP, mild SATURATES — so the routing question is simply
which candidate axis orders sharp>mild>control (propensity) AND is
resolution-stable. Necessary-not-sufficient screen (~an hour), not the gate.

Three axes at N=256,512 on {smooth_sharp, smooth_mild, euler_control}: (1)
ν_crit-analog = viscosity at which net resolved amplification crosses 2× (κ=0,
confirmed with the user; amplification is the blow-up currency, same predicate as
ga.fitness v3); (2) persistence = growth acceleration over the resolved window
(free from the ν=0 run); (3) g_baseline as the known-wrong-direction sanity axis.

The smoke (N=128) earned its keep BEFORE the committed run: the first ν_crit used
a windowed-slope zero-crossing, and smoke exposed it as contaminated — a
net-DECAYING mild run (amp=0.5) still showed a positive in-window slope, censoring
it in the wrong direction. Switched to the amplification boundary (monotone in ν,
cannot be fooled). A human-style discipline point: the screen caught its own
design bug because the labeled truth made the wrong answer visible.

Verdict (pre-committed gate): ν_crit is the SOLE survivor. Direction sharp
0.6519 ≫ mild 0.0483 > control 0.0000, and — the headline — ν_crit is IDENTICAL
to four decimals at N=128/256/512 (the amp-crossing ν is set by the dynamics, not
the grid). persistence FAILS on direction (the hard-saturating mild, persist
−2.69, sits BELOW the flat control ≈0 — it cannot rank a strong decelerator
against a non-grower; NOT a stability failure, correcting an earlier eyeball).
g_baseline reproduces the spike's mild>sharp (the built-in sanity check that the
discriminator is trustworthy). N=512 growers were ~32 min each (a single N=512
solve to t_max=4 is ~4 min × ~12 bisection runs); euler_control censored low in 1
run.

Honest scope: this settles ROUTING only. It clears the direction +
resolution-stability legs on 3 ICs; it does NOT clear the full six-property Gate
4. The big remaining risk is property 6 (non-trivial optimum) — the exact
property that killed gCLM's ν_crit (trivial k=1 collapse, STAGE_2_5). The Hou–Luo
singularity being robust smooth-data (not non-generic) is the REASON to expect
property 6 to fare better, but that's a hypothesis Gate 4 tests, not a result.
Next: Gate 3 genome wiring ν_crit(amp≥2×, κ=0, tail_guard window), then the
non-negotiable Gate 4. Full write-up: PHASE1_AXIS_SCREEN_RESULTS.md.

## phase1_resolution_spike (4741cda) — 2026-07-23 — de-risk: STABLE

Why run BEFORE the Gate 3 genome (a reorder, confirmed with the user): the
dominant risk to a Tier-2 result in 2D Boussinesq is not physics but RESOLUTION.
Unlike 1D gCLM (fully resolved at N≤4096), the Hou–Luo singularity is a corner
collapse Luo–Hou needed AMR (~1e12 effective) to track; on a uniform grid the
vorticity sharpens below grid scale before T*. So a cheap probe (hours) answers
"is there a resolution-stable fitness signal at feasible N?" before weeks of
genome/GA — exactly the Stages 2.5/3.5/3.6 de-risk-before-compute discipline.

Instrument added first (`solver` tail_guard): stop "under_resolved" when
enstrophy piles near the 2/3 dealias cut. A human noticed the key trap in
calibration: conservation drift stays ~1e-6 even when small scales are garbage
(∫w and energy-balance are robust to under-resolution), so drift is the WRONG
trust signal; the spectral tail is the right one. The solver now refuses to
report dynamics past that point.

Verdict STABLE (pre-committed gate in analyze_phase1_spike.py; full write-up
PHASE1_SPIKE_RESULTS.md). The fixed-window log-growth-rate g CONVERGES across
N=128→1024: smooth_sharp g→0.609 (finest-two 0.01%), smooth_mild g→1.239
(0.000%). Four findings: (1) resolution-stable growth fitness exists → search
viable; (2) the resolved window EXTENDS with N (amp_res 29→101×), so amp_res is
NOT a stable fitness but g is; (3) the blow-up EXPONENT/T* rails (a 2.45→1.20)
— uniform-grid Tier-2 confirmation of the true singularity is out of reach, the
resolution wall quantified; (4) rough C^{0,h} data is under-resolved from t≈0
(t_res 0.03–0.07 at all N) — the rough-data axis is resolution-starved on
uniform grids.

A gate-logic bug worth recording (fixed transparently, not post-hoc softening):
the first cut used STRICT per-step monotonicity for "converging", which gave a
false RAILS on g-sequences agreeing to <0.01% because of rounding-level (1e-4)
wobble. Replaced with "every successive relative change ≤ the pre-committed 10%
tolerance" — the honest reading of "settles across resolution", stronger than a
finest-two check and immune to rounding noise. The 10% threshold itself was
never moved (it passes by ~1000×).

Consequence (recalibrated, honest): PROCEED to Gate 3/4 on SMOOTH data with a
resolution-stable growth-based fitness (a ν_crit-analog is the prime candidate,
NOT amp_res); the near-term deliverable is a shape→growth QD map with Tier-1
candidates, NOT Tier-2-confirmed singularities (those need AMR / Route D). Gate 4
must still resolve which resolution-stable axis actually tracks blow-up
PROPENSITY — note smooth_mild has higher early g yet saturates, smooth_sharp
lower g yet blows up. Drop (or explicitly scope out) the rough-data axis.

## DECISION RECORD + boussinesq Gate 1a — 2026-07-23 — Route A Phase 1 begins

Post-Stage-3.6 review settled the scope: **commit to Route A Phase 1** (the
multi-week 2D-solver build), and — within Boussinesq — build around the
**Hou–Luo symmetry-wall geometry** (both decisions confirmed with the user). Why
Hou–Luo over the Elgindi-type C^{1,α} no-boundary variant: it is the setting of
the *computer-assisted proof* (Chen–Hou 2022) → best Tier-3/Route-D handoff; it
has a gold-standard numerical benchmark (Luo–Hou 2014) to validate against; and
its smooth-data singularity is robust, so the fitness is far less likely to rail
the viability gate than gCLM's non-generic axis did. The rough-data genome still
enters later as a C^{1,α} boundary-data variant. Full plan: PHASE1_PLAN.md.

**Gate 1a (doubly-periodic solver core) — PASS.** `solver/boussinesq.py`: full
fft2 pseudo-spectral 2D Boussinesq (w_t + u·∇w = th_x + νΔw; th transported;
Biot–Savart Δψ=w), RK4 + exact integrating-factor viscosity, 2/3 dealiasing,
advective CFL — the gCLM method lifted to 2D verbatim, same `SolverResult`
contract plus theta_final. Viscosity/thermal-diffusivity and the artifact guards
(∫w, ∫th conservation; kinetic-energy balance d/dt½∫|u|² = ∫vθ − ν∫w²) are
first-class from line one.

Validated by an exact analytic ladder (`test_solver_boussinesq.py`, 6/6), each
isolating one unknown: biot_savart 3.9e-16, rhs_terms (advection assembly +
buoyancy th_x vs hand-computed analytic RHS) 9.3e-15, scalar_transport (frozen-u
exact translate) 5.4e-11, viscous_decay 3.0e-15, taylor_green (w=e^{−2νt}sinx
siny exact solution — advection self-cancels) 5.3e-15, conservation 1.2e-16.
Everything at or near machine precision; the RK4-time-integration checks
(transport 5e-11, Taylor–Green 5e-15) confirm the coupled dynamics too. What a
human noticed: the Taylor–Green check is the strong one — it forces the
advection term and the Biot–Savart velocity to cancel exactly at machine scale,
which a sign error or a mis-indexed kx/ky mesh would not survive.

**Gate 1b (Hou–Luo symmetry-wall) — correctness PASS.** The no-flow wall is
imposed by parity (w odd-x/odd-y, th even-x/odd-y) rather than a Chebyshev
boundary: Biot–Savart then gives v even-x/odd-y (vanishes on y=0,π) and u
odd-x/even-y (vanishes on x=0,π), an effective [0,π]² box with the singular
corner at the origin. `test_boussinesq_wall.py`, 4/4: wall_bc 8.2e-17 (v,u zero
on the walls/axes at machine scale); **parity_preserved 9.0e-15 — the crucial
one: with NO projection, symmetric data stays in the subspace to roundoff, so
the wall is a genuine invariant of the discretised dynamics, not enforced by
fiat**; parity_enforced 3.7e-16; buoyancy_amplifies — a Luo–Hou-type IC (seed
vorticity + sharp buoyancy gradient) amplifies max|ω| 30.6× while holding parity
at machine scale and drift at 2.6e-6. The `symmetry="houluo"` solver option
projects each step so long runs stay exactly on the wall; the guard proves the
projection is only cleaning float-level leakage, not doing real work.

What is deliberately NOT claimed yet: the quantitative Luo–Hou growth curve /
finite-T\* singularity. Uniform-grid spectral resolution cannot reach the ~10⁷
amplitude Luo–Hou got with adaptive meshing, so matching their curve is a
separate resolution-limited study, and "how faithfully to chase it" is a
judgment call flagged for review rather than decided here. The two Boussinesq
suites (test_solver_boussinesq, test_boussinesq_wall) join the required pre-run
set for Phase 1.

**Gate 2 (port the Phase-0 method) — PASS.** Two pieces, each validated before
trust. (a) The 2D rough-data representation (`ga/genome2d.py`): the separable
Holder product w_h = P_h(x)P_h(y) with P_h = sign(sin)|sin|^h — automatically
odd-x/odd-y (the vorticity parity), plus the even-x/odd-y density partner
th_h = |sin x|^h P_h(y). Its slice at y=π/2 is exactly the 1D P_h, so the
Phase-0 regularity certificate transfers verbatim: `test_genome_rough_2d.py` 7/7
— corner Holder exponent recovers h, h=1 is exactly sin x sin y, the cusp x-slope
diverges at the N^{1-h} rate (C^{0,h}-not-C^1), tail energy monotone in h, and
the realized fields sit in the right parity subspace, energy-normalized. (b) The
fine-N exponent measurement is the SAME model-agnostic estimate_blowup_time; only
its wiring to the 2D solver is new, so it is validated on known-answer controls
(`test_phase1_measurement.py` 3/3): a synthetic (T*-t)^-a series is inverted back
to (a, T*) exactly (a=1.0/1.5/2.5, R²=1.0), and — the important one — 2D Euler
(buoyancy off, globally regular, ||w||_inf conserved) is fed through the whole
pipeline and must NOT reach Tier-2. It doesn't: ||w||_inf growth is 1.4%→0.4% as
N goes 128→192 (shrinking, as the theorem says), and the per-resolution T*/alpha
rail to OPPOSITE grid edges (T*=58,a=0.30 vs T*=12103,a=3.00, the finer with
negative held-out R²), so the convergence gate rejects it decisively. A single
coarse run's held-out R²=0.984 would have flagged a spurious candidate — exactly
why resolution-convergence, not single-run candidacy, is the real gate. What a
human noticed: the negative control is the sharp one — it proves the pipeline
cannot manufacture a Tier-2 blow-up from a flow we KNOW is regular, which is the
whole anti-self-deception contract, now demonstrated in 2D.

The four Phase-1 suites are solver-heavy (~30–60s each); the full 10-suite gate
needs a longer timeout than the 1D-only set. Next (STOP for review first): Gate
3 — the 2D genome data structure + MAP-Elites reuse, then the NON-NEGOTIABLE
Gate 4 viability gate before any GA compute.

## DECISION RECORD (not an experiment) — 2026-07-23 — Route A, Phase 0 is next

Post-Stage-3.5 review with the user settled the forward path. Decision: pursue
Clay via [CLAY_ROADMAP.md](../CLAY_ROADMAP.md) **Route A** (switch to a model
where non-generic blow-up is provable — 2D Boussinesq / C^{1,α} De Gregorio),
and fold the former "Route C" (cheap rough-data + fine-N gCLM probe) into it as
**Phase 0** rather than running it as a parallel detour.

Why Phase 0 first, not a leap to the 2D solver: two unknowns (a new solver AND a
new non-generic-exponent measurement) must not be debugged simultaneously — on a
weird rough-data blow-up you couldn't tell solver bug from measurement bug.
Build/validate the *measurement* on the 1D substrate where the answers are known
(CLM analytic T*, De Gregorio literature), then port a trusted method to 2D.
Phase 0's real value is the transferable method + rough-data genome + an honest
"is gCLM exhausted?" check — NOT a gCLM science result (Stage 3.5 makes a
converged non-generic exponent unlikely). What transfers to Phase 1 is the
method and the representation *principle*, not the 1D genome code; a Phase-0
negative is informative, not a kill-signal (Boussinesq is a different
mechanism). Hard 2-day time-box + pre-committed converge/rail gate so it can't
become open-ended 1D tinkering. Concrete spec: PLAN.md Stage 3.6.

## stage3_6_sweep (95ef09f) — 2026-07-23 — Route A Phase 0: RAILS (expected)

Why configured this way: the execution of the decision record above. Two
deliverables + one gated verdict, on the validated 1D solver. (1) A genuine
C^{1,α} rough-data genome mode — `holder_profile(h) = sign(sin x)|sin x|^h`,
an odd C^{0,h} vorticity with a *localized* Hölder cusp, unlike the delocalized
random-phase field the k^{-p} envelope reaches. Chose the real-space local
Hölder exponent as the regularity certificate (test_genome_rough.py) because
the spectral-decay rate is contaminated by the second cusp at x=π and
finite-k roundoff, whereas |f(x)|∼x^h near 0 is exact and definitional; also
pinned the C^{0,h}-not-C^1 signature (max|f′|∼N^{1-h} diverges). (2) A fine-N
exponent probe at N∈{1024,2048,4096} over h∈{0.2..1.0} × a∈{0.7,0.9,0.95,1.0}.
Added a=0.7 as a **methodological control** (not in the original spec's a-list
but demanded by "validate the measurement where the answer is known"): Stage
3.5 says a=0.7 must read generic α≈1 stably, so if the fine-N fit doesn't
recover that, the probe is inconclusive rather than a verdict. Frozen at the
Stage 3.5 config (t_max=24, amp=1e3, tail 0.15) except resolutions; max_steps
200k so De Gregorio non-blow-up runs bail (~700s each at N=4096) instead of
hanging. Pre-committed gate in analyze_stage3_6.py, not softened after seeing
data.

What a human noticed skimming the results (experiments/stage3_6_sweep.jsonl,
72 rows; full write-up STAGE_3_6_RESULTS.md):

- The control worked *perfectly*: a=0.7 is α∈{1.00–1.10} across a 4× grid
  range for every h, 18/18 usable. That's what lets the near-a=1 negative be
  believed. Mild honest wrinkle: the roughest shapes (h=0.20/0.35) tick from
  1.00 to 1.05–1.10 only at N=4096 — a small finite-N wobble, but still
  generic, never railing.
- Rough data DID revive blow-up *occurrence* — a=0.9 went 18/18 usable fits
  (vs Stage 3.5's 20/40 usable + 15 flips at N∈{256,512}). For a moment that
  looked like progress. But the exponent still scatters non-monotonically
  across resolution (median cross-N span 0.65, max 1.95; e.g. h=0.50:
  2.60→0.65→1.20). Occurrence improved; convergence did not.
- a=0.95 rails outright — h=0.20 goes 0.30→0.85→3.00, spanning the whole fit
  grid across resolution, and 4/18 flip well-definedness. a=1.0 (De Gregorio
  proper) is stone dead: 0/18 blow up even for C^{0,0.2} data (slow runs hit
  the 200k step cap). Not evidence of regularity (WIN_CONDITION.md) — just no
  searchable signal.
- Key reassurance the rail is real, not slop: max conservation_drift over all
  72 runs is 1.9e-4, well under the 1e-3 guard, and every counted fit clears
  R²≥0.9. The runs are well-resolved and individually clean; the exponent
  simply has no resolution-stable limit. Going N=256/512 → 1024/2048/4096 did
  not shrink the scatter (max span 2.70 vs Stage 3.5's 2.7). Refinement
  doesn't help — the strongest cheap evidence that gCLM's non-generic exponent
  is a grid-scale feature, not physics.
- Net: the cheap 1D route to a novel non-generic result is closed for smooth
  AND rough data. But the two deliverables (rough-data representation +
  validated fine-N method) transfer to Phase 1 exactly as scoped. STOP for
  review per the gate before any 2D solver work.

## nongenericity_sweep (7b… post-Stage-3) — 2026-07-23 — NO VIABLE AXIS

Why configured this way: review question after Stage 3 — the GA edge is at
a=0.7 but every confirmed blow-up there is generic (α=1.000), whereas the novel
Tier-3-provable target is non-generic (α≠1) near a=1 with rough data. Sweep
measured |α−1| inviscid across a∈{0.7,0.9,1.0} to see if the edge regime and
the novel regime overlap, before spending any GA compute. Amp raised 100→1e3
so α is fittable (100× gave R²=−1.7 garbage in the marginal regime in the
pre-build probe); max_steps capped at 300k so no-blow-up/near-critical runs
bail instead of burning t_max. p-regime question folded into the analysis via
the 20 init-prior draws' native envelope_p (they already span [0.02, 3.30]).

What a human noticed skimming the results:

- The answer is a clean "disjoint," and sharper than expected. At a=0.7 α is
  pinned at 1.00 for ALL 37 blow-ups including the p=0.02 (nearly white) draw —
  Spearman(|α−1|, p) = −0.07, i.e. roughness does nothing to the exponent
  there. Whatever the GA evolves at a=0.7, it's generic CLM. Independently
  re-confirms Stage 3's α=1.000 across the whole roster, not just the elites.
- a=0.9 is the tell: non-genericity DOES appear (α up to 3.0) but it's pure
  grid artifact — 15/40 well-def flips, and the biggest |α−1| shapes rail to
  α=3.0 at N=256 then collapse to 0.30–0.60 at N=512 (max Δα=2.7). This is
  literally the Stage 1.5 a_crit "near-critical advection collapse scale"
  instability, now on the exponent. Wrote it up as such.
- a=1.0: 0/40 blow up (34–35 clean no_blowup, rest stiff step-cap). Dead axis,
  as Stage 2.6 already found for smooth data — restated with the WIN_CONDITION
  non-goal caveat (absence of signal ≠ regularity).
- Net: the gate earned its keep — 240 runs / ~2 min killed a GA campaign that
  would have been optimizing resolution noise. The three forward options
  (rough+fine-N; switch to 2D Boussinesq; bank the 1D pipeline) go to review;
  NONGENERICITY_RESULTS.md records them.

## stage3-resolution-20260723T082807 (57b4a88) — 2026-07-23 — TIER 2: 18/18 CONFIRMED

Why configured this way: studied the top-3 elites per acceptance seed (9
genomes, spread across 9 MAP-Elites cells, all 3 seeds) rather than only the
single best, so a promotion means the evolved *shape family* confirms, not one
lineage. Two operating points per elite because fitness is a ν_crit bisection
but a resolution study is one trajectory: ν=0 (cleanest, gates promotion — the
sharpest test of the C^∞-may-not-blow-up regularity caveat) and ν=0.5·ν_crit
(inside the band; confirms the viscosity-resistant blow-up itself refines). Ran
each elite's *own* frozen config.json, not a shared default — the study must
mirror the exact fitness config each elite was produced under. Amplification
raised 100×→10⁴×: at a fixed 100× stop every resolution halts at the same
physical state, making T\* agreement almost tautological; 4 decades of growth
actually stresses the extrapolation.

What a human noticed skimming the results:

- The convergence is almost too clean. Inviscid 512→1024 relative T\* diff
  maxes at 3.5e-6 against a 2e-2 gate (~5000× margin); the top elite gives
  *bit-identical* T\*=2.17320 at N=1024 and N=2048. That is the signature of a
  singularity already fully resolved at N=256, i.e. NOT forming at
  ever-smaller scales — the direct refutation of the resolution-artifact worry
  for these shapes.
- Every single confirmed blow-up fits α=1.000 exactly. This is the *generic
  CLM* exponent, not a De Gregorio non-generic one — so honestly these are the
  CLM singularity surviving a=0.7 advection, consistent with (not beyond) the
  literature. Wrote this into STAGE_3_RESULTS.md so the pipeline-validation win
  isn't mis-sold as a new singularity. The novelty stays the QD map.
- Conservation drift *shrinks* monotonically with N (6.7e-5 → 1.0e-6 as
  256→2048), the opposite of an under-resolved run. The artifact guard (1e-3)
  never engaged; it is there for the axes we haven't confirmed yet.
- Cost was trivial (~4s/run at N=1024, 18 studies × 3 N in well under a
  minute at 10 workers) — the expensive part of this project was always the
  bisection-heavy GA, not the confirmation.
- Literal PLAN wording says "De Gregorio genome"; our axis is a=0.7, and a=1 is
  a dead axis for smooth odd data. Flagged the gap explicitly rather than
  quietly reinterpreting the criterion.

## stage2_6-seed1/2/3 (a10d6b2) — 2026-07-22/23 — FINAL: ACCEPTANCE PASS 3/3

**Final verdict (analyze_stage2.py): STAGE 2 ACCEPTANCE MET.** GA vs
random at matched budget: 0.1624/0.1591 (+3.3 tol), 0.1631/0.1585
(+4.6 tol), 0.1629/0.1597 (+3.2 tol); domination over the final half of
the budget on all seeds; GA above the literature best (0.1585) on all
seeds, random on none. QD replay (secondary): random still covers more
cells (74–79% vs 50–56%); GA wins QD-score on seed 3 only — peak search
and map-building remain different objectives (tuning lever: exploration
pressure). Cross-seed archives: Jaccard 0.62–0.72, |Δfitness| 0.005–0.011
on shared cells. Health: censoring 5/3/8, non-monotone 0/5/2 (excluded
from archives by rule), lit control reproduced the sweep within 1 tol on
every seed. Full write-up: STAGE_2_6_RESULTS.md. Next: Stage 3 resolution
study on the elites (pending review).

The interim seed-1 analysis below is preserved as written mid-protocol:

Why configured this way: the Stage 2 acceptance protocol rerun on the
axis Stage 2.6's gate verified — nu_crit under the v3 amplification-only
oracle at a=0.7, t_max=24, bisection [0, 0.3] tol 1e-3 (config-only
changes at commit a10d6b2). 3 seeds, pop 24 × 25 gens, budget-matched
interleaved baseline_random, literature control re-sampled at run start.

**Seed 1 interim analysis (written mid-protocol so a crash cannot lose
it; final 3-seed verdict pends in STAGE_2_6_RESULTS.md):**

- Shakedown clean: literature control best 0.15849 vs sweep's structured
  best 0.15820 (within 1 tol). ~170s/generation at 10 workers.
- **First-ever GA-vs-random separation in this project.** Random init
  ceiling (gen 0, 24 draws): 0.14736. Final GA best: 0.16236 at gen 21.
  Interleaved random baseline plateaued at 0.15908 (~600 draws). GA
  finished ~+3.3 tol above random and above the best literature profile
  (0.15849) — margin modest but structurally meaningful: the GA climbed
  where random stalled.
- **Operator attribution (the "do we need better breeding?" question,
  answered from the event stream):** after gen 0, ALL eleven best-so-far
  improvements came from variation — 6 mutation, 5 crossover, 0 from
  later random draws — a monotone climb 0.147 → 0.150 → 0.153 → 0.155 →
  0.158 → 0.160 (gens 1–9) then 0.161 → 0.162 (gens 12–21). Archive
  insertions: 96 mutation / 86 crossover / 21 init. Both operators
  productive for both peak fitness and map-building. Verdict: breeding is
  effective; no operator changes warranted, and none permitted mid-protocol
  (frozen acceptance config; changes would restart all 3 seeds).
- **Post-verdict tuning leads, if wanted (from this seed's data, to be
  re-checked against all 3):** (1) improvements still arriving at gen 21
  while mutation scale has decayed 0.3 → ~0.05 — a scale floor or longer
  run plausibly buys more; 25 gens may truncate the climb. (2) Archive
  coverage plateaus at 0.500 from gen ~17 (QD still creeping) —
  exploration pressure (novelty bonus / empty-cell-directed emission) is
  the standard lever if the map deliverable needs more coverage.
  (3) No evidence the genotype (sine coeffs + envelope p) is the
  bottleneck — the winning shapes are low-k mixtures it represents
  directly.

## stage2_5_sweep A + B (A: f3dc522, B: a005ef8) — 2026-07-22

Why configured this way: PLAN.md Stage 2.5's answer to the Stage 2
verdict — before any GA rerun, gate a redesigned fitness axis on the
six-property checklist, with the non-trivial-optimum property measured
against the GA's ACTUAL init prior (20 draws with the Stage 2 config's
N=32, p ∈ [0, 3.5]) alongside the 20 Stage 1.5 shapes. Candidate A:
ν_crit at a ∈ {0.4, 0.7, 1.0} (largest passing a wins). Candidate B
(fallback): ν_crit at a=0 under a k≤2 ≤ 50% energy cap enforced at
normalization. Same frozen v2 oracle and tol 1e-3 as Stage 2; a range
ladder [0,0.1]→[0,0.4]→[0,1.0] because moderate advection turned out to
RAISE ν_crit ~3× (unexpected and interesting on its own).

**Verdict: no viable axis — every candidate fails, each differently, and
the pattern is the finding** (full numbers: STAGE_2_5_RESULTS.md):

- a=1.0 (De Gregorio): dead axis. 35/40 censored low at ν=0. The k=1
  refuge dies at the equilibrium, but so does essentially all smooth-data
  blow-up within the horizon — only rough low-k1 prior draws survive, at
  ν_crit ≈ tol/2. The literature's smooth-data regularity expectation,
  watched in real data.
- a=0.7: the only landscape with a genuinely structured top (prior-vs-
  structured gap 21·tol) — but it fails monotonicity, and the audit shows
  why: 100% of its boundary decisions are fit-decided (slow α≈0.3 growth,
  T* extrapolated just inside the 1.5·t_max cap), vs 19/19
  amplification-decided at a=0. One shape's classification flickers
  non-monotonically as fit quality dips and recovers across a marginal
  band (island at ν ∈ [0.026, 0.031], R² up to 0.997). The critical value
  at a>0 measures "where a marginal extrapolation crosses the horizon
  cap" — resolution-exact but semantically soft.
- a=0.4: Stage 2's disease softened but present — gap 7·tol,
  ρ(ν_crit, k1frac) = 0.79; prior sampling reaches the top region.
- Candidate B: PLAN.md's own stated risk realized verbatim. Seven-way tie
  at the top, every one at EXACTLY the 0.5 cap boundary; best prior draw
  EQUALS best structured (gap 0.0); ρ(k1) = 0.91. The cap relocates the
  trivial optimum; it does not remove it.

What a human should take away: ν_crit on gCLM at fixed horizon is, in
every variant tried, a thin wrapper around the νk² dissipation scaling —
a spectral-concentration quantity the init prior samples directly. No GA
can beat random on it, and the six-property gate now proves that for ~40
bisections (~10 min) instead of ~3 GA-seed-days. Stage 2 acceptance rerun
deliberately NOT executed. Paths forward (oracle v3 + a=0.7; rate-based
fitness; ν_crit normalized by the shape's own k²; or accept the negative
result and re-scope) are redesign-level and go to review.

## stage2-seed1 / seed2 / seed3 (d47b579) — 2026-07-22

Why configured this way: the Stage 2 acceptance runs — 3 independent seeds,
pop 24 × 25 generations = 600 GA evals each, budget-matched interleaved
baseline_random (612 with the literature control), frozen fitness config
(nu_crit at a=0, N=256, t_max=12, bisection [0, 0.1] tol 1e-3, v2 oracle).
~12,200 solver runs / ~64 min per seed at 10 workers.

**Verdict: acceptance NOT MET, decisively and in triplicate — and the
reason is a finding, not a bug.** The nu_crit landscape at a=0 has a
trivially-located global optimum: pile energy into k=1. Numbers:

- Best-so-far: GA 0.0543 / 0.0543 / 0.0545 vs random 0.0543 / 0.0543 /
  0.0543. Margin 0, 0, and 0.2× tolerance. Both sides hit the ceiling
  within ~12 evaluations (order-statistics of the init prior, not search).
- All three seeds' best genomes are >= 99.5% k=1 energy with a few % of
  one low harmonic (k=2..4). Two of three were raw init draws; seed 3's
  crossover polish bought +0.0002 (~0.2 tol). This is the nu*k^2 scaling
  argument, rediscovered empirically: lowest mode survives viscosity best.
  PLAN.md's "frequency-space cheating" guardrail worry turns out to be the
  honest global optimum of this axis, not a cheat.
- Sharper: random *dominates the GA on map-building too* — replaying both
  event streams through identical archive-insertion rules, random reaches
  74–79% coverage / QD 2.6–2.7 vs the GA's 46–58% / 2.0–2.2 at the same
  budget. Fitness-driven tournament selection concentrates parents on a
  flat plateau; exploration is all cost, no signal. On a saturated
  landscape MAP-Elites' selection pressure is strictly worse than prior
  sampling for the map deliverable.
- The pipeline itself behaved to spec: 0/1800 GA+random evals censored
  (bump(κ=5) control aside), 6 non-monotone flags in 3,672 evals, ~6%
  bracket-expansion rate, warm starts saving ~2 runs/eval, zero cache
  hits (expected: MAP-Elites never re-evaluates elites).
- The map interior is real but partially confounded: median nu_crit falls
  smoothly with oscillation count (0.054 at 2 sign changes → 0.028 at 20)
  and with tail roughness — but per-bin maxima sit at ~0.054 nearly
  everywhere because the two archive descriptors don't pin k=1 dominance
  (a 99%-k=1 genome can carry any tail slope in its negligible tail).
  Cross-seed final archives: Jaccard 0.61–0.69, mean |Δfitness| on shared
  cells ≈ 0.0064 (~6 tol) — moderate convergence, consistent with sparse
  per-cell sampling.

Lesson recorded for any future fitness axis: Stage 1.5's viability
properties (nonzero, finite, monotone, resolution-stable, wide band) are
necessary but NOT sufficient — they never asked *where the optimum lives*.
Add a sixth check: the optimum must not be reachable by trivial sampling
of the init prior (e.g. require the best of ~20 random draws to sit well
below the best hand-constructed shape).

Redesign options for a non-degenerate axis (review decision, in rough
order of preference): (1) bandwidth-constrained nu_crit — cap the k=1 (or
top-k) energy fraction, or pin the spectral centroid, so resistance must
come from structure; (2) move to a > 0 (De Gregorio side) where advection
fights growth and low-k concentration stops being free — requires the
resolution-convergent oracle Stage 1.5 says the a-axis needs; (3) score
QD/map metrics directly rather than scalar best-so-far.

## stage2-shakedown (d47b579) — 2026-07-22

Why configured this way: first end-to-end run of the Stage 2 GA harness —
deliberately tiny (pop 6, 3 generations, seed 999) to shake out the
pipeline before the real 3-seed acceptance runs, per PLAN.md. Full frozen
fitness config (N=256, t_max=12, bisection [0, 0.1] tol 1e-3, v2 oracle).

What a human noticed skimming the results:

- The literature positive control lands where Stage 1.5 put it: sin(x)
  0.0535 (vs 0.0527 at the coarser Stage 1.5 tolerance), sin(2x) 0.0137
  exactly, and bump(κ=5) censored "low" — the beyond-horizon control
  behaves inside the GA harness too.
- Warm-started child evaluations took a median 9 solver runs vs 11 cold,
  with 0 bracket expansions in 12 — the ±0.01 margin is, if anything,
  generous; leaving it.
- Median 15.3s per evaluation, ~2× the Stage 1.5 per-bisection cost:
  the [0, 0.1] range concentrates bisection samples near the critical
  value, where no-blow-up runs burn the whole t_max. Real-run sizing
  (~25 min/seed at 10 workers) accounts for it.
- A random init genome (0.0543) edged out sin(x) immediately — the
  landscape above 0.053 is reachable, but the random baseline found it
  too. Whether the GA can *separate* from the baseline is exactly what
  the 3-seed acceptance runs measure.

## stage1_5_sweep (v1: 5c6dfc2, v2: b05b9bf) — 2026-07-22

Why configured this way: t_max=12 chosen after computing analytic CLM T*
for all 20 normalized ICs (live shapes span 1.0–6.5; bump(κ=5) at 15.9 kept
deliberately as a beyond-horizon censoring control). ν bisected at a=0 to
isolate viscosity in the proven-blow-up regime; a bisected at ν=0. One
energy scale (E of sin(x)) across all shapes so critical values compare
shape, not amplitude.

What a human noticed skimming the results:

- The ν axis is astonishingly clean: all 80 v1-vs-v2 and 256-vs-512
  ν-bisections take *identical* decision paths. The sin(2x) value landing at
  ν_crit(sin)/4 (νk² scaling) was not designed in — good sign the number is
  physical.
- The v1 a-axis anomalies (censored-high at N=512 only, for two shapes) all
  traced to one predicate flaw: accepting held-out-R²≈0.9 fits whose
  extrapolated T* was 6–11× beyond the horizon. Capping T* at 1.5·t_max
  (v2) fixed every one; tail(p=1)'s 2× resolution drift survived the fix
  and is the real, physical reason a_crit was rejected.
- 14% of amplification-stopped runs had tail fits below the R² floor
  (bursty near-critical growth) — the amplification-first predicate rule
  mattered in practice, not just in principle.
- Energy-balance residuals up to 0.5 on ν-axis blow-up runs looked alarming
  but are endgame dt-integration error: halving dt halves them and moves
  ν_crit by exactly zero (3-shape spot-check at N=512).

## Legs 54-57 (2026-08-05) — MM answers NO, NB answers YES, TN answers NO, XS answers NO

Four parallel legs closed this cycle (see `experiments/journal/leg_54.md` through
`leg_57.md` for full detail; pointers only here):

- **Leg 54 (Route-MM):** the last free choice (shape of the approximate inverse) does not
  close the certificate. Best admissible Z_1 = 8.9591 vs block-diagonal baseline 10.4584
  (1.167x, needed <1). Fires plan_of_record.py's pre-committed no-branch for stage MM.
- **Leg 55 (Route-NB):** HL_S2_nonsymmetric's compactified-basis coefficients decay as
  k^-1.396 -- finite ell^1_w norm at s=0/0.3, divergent at s=1. Narrows (not deletes) a
  ban-list clause; "the target was never in the space" is not an available explanation
  for legs 52-53's failures.
- **Leg 56 (Route-TN):** the (H,D) consistency defect exceeds L1 step one's admissible tau
  by 1.85e7x (derivative) / 2.04e11x (Hilbert, corrected mechanism after verifier review).
- **Leg 57 (Route-XS):** no published radii-polynomial certificate has an off-diagonal
  unbounded part with a non-decaying tail inverse -- banked as an executable ledger
  (`solver/certificate_shapes.py`, 15/15 gates, 4 papers).

No link of the L1->L4 chain moved. Clay unchanged at ~0.05%.

## Legs 60-70 (2026-08-06) — the eight gates that answered after MM/NB/TN/XS

Freshness audit (leg 72, Route-JR). Eight legs have answered their gate since the
`Legs 54-57` entry above and none had a pointer here. Pointers only; every headline
below is copied from that leg's own `experiments/journal/leg_N.md`, not re-derived.
Full detail and the audit's own counts: `writeup/novelty/leg_72.md`,
`experiments/journal/leg_72.md`.

- **Leg 60 (Route-PQ) — NO, parked and escalated (§8 escalation #4):** Route-PORT v1/v2's
  reproduction ledger re-derives 111 of 114 quoted numbers from stored curated data; 3 do
  not. The two numbers the standing bans actually rest on re-derive exactly. Branch
  `leg/pq-v1` pushed, **not merged** — so its journal and novelty files exist on that
  branch and not on `main`.
- **Leg 64 (Route-A12) — SPLIT:** YES on the `sigma = 3` half (Xu Tier 1, `s*(1/2) = 3`
  exact), NO on `alpha_1 = +0.133683`, which is searched-and-not-found across the arXiv
  CLM corpus. Three corrections reported, none applied.
- **Leg 65 (Route-L1G) — NO:** the weighted-`ell^1` no-go and the discrete-ball trap are
  not published; the last two unread Tier-2 papers are now read in full text and the
  nearest cousin is located and quoted.
- **Leg 66 (Route-QF) — YES:** dedicated unit tests for `spectral_utils`, `gclm`,
  `boussinesq` (41 checks) found a real odd-`n` `derivative_hat` defect, visible only
  because the module was tested directly. Zero current blast radius (every live call site
  uses even `n`); pinned, and repaired outside the leg system.
- **Leg 67 (Route-FD) — NO** for the quantity this repository holds: the published 2D
  Boussinesq criticality is `alpha + beta = 1`, a different object from `s_c`; no
  blow-up-arrest exponent is published. `s_c` stays internally-consistent-only.
- **Leg 68 (Route-IX) — YES:** 25 of 25 quartet pieces present for legs 53-57, so
  `writeup/INDEX.md` was caught up — five Arc 4 rows added (TC/MM/NB/TN/XS), stale
  in-progress text deleted.
- **Leg 69 (Route-IA) — NO, stop-the-line:** `solver/interval.py` is sound over the normal
  range (0 of 12356 failures) and unsound in the subnormal band (62 of 1680), with silent
  NaN above `2^997`. Live operators (0.5-128) sit ~140-298 decades clear of the failure
  band; repair dispatched outside the leg system.
- **Leg 70 (Route-RC) — NO:** `solver/rescaled_spectrum.py` imposes no origin condition;
  the 141/144 count is `K-3`, i.e. the maximal `L^2` realization's continuum, not a Morse
  index.

No link of the L1->L4 chain moved in any of the eight. Clay unchanged at ~0.05%.

Legs 58, 59, 61, 62 and 71 have since answered their gates and landed (see their pointer
lines below, added at leg 137/JR3's flag — this sentence originally said all six had "no
answered gate"; only leg 63 (Route-M2) still fits that description, parked as `leg/m2-v1`,
escalation #1, unmerged).

## Legs 59-97 (2026-08-06) — the twenty gates that answered after leg 72's pass

Second freshness audit (leg 102, Route-JR2), same audit as leg 72's, new window. Twenty
legs have answered their gate and landed on `main` since leg 72's block above, and none
had a pointer here (measured: 0 of 20). Pointers only; every headline below is copied
from that leg's own landed headline (`experiments/journal/leg_N.md` / its PR body), not
re-derived. Full detail and the audit's own counts: `writeup/novelty/leg_102.md`,
`experiments/journal/leg_102.md`.

Legs 59 and 61 appear here, not in leg 72's block, because leg 72 deferred them as "branch
progress but no answered gate" and their gates answered afterwards.

- **Leg 59 (Route-WV) — FAIL 5/6:** the conditioning wall modelled in both weight factors;
  the frozen six-property gate re-run answers FAIL 5 of 6 (P2 0.975 passes, P3 0.342
  unmoved). The GA-compute ban therefore did not lift.
- **Leg 61 (Route-KA) — YES on the literal gate, NO on the stricter pre-committed
  window:** the interval pipeline reproduces CLN's published Kawahara radius end to end;
  the gap between the two readings is measured, not argued.
- **Leg 73 (Route-BV) — YES:** the first *external* known-answer check for the 2D velocity
  solve — it reproduces Lamb's corner-image closed form to 1.76e-4 at order 2.00; the
  `r^{-2n}` closure costs 2.3e-5 at 5x truncation.
- **Leg 74 (Route-EXT) — NO:** `HL_S2_nonsymmetric` still uncertified 126 days on, 0 of 6
  channels.
- **Leg 77 (Route-EXT2) — NO:** the rank-2 target object is still uncertified, 133 days on.
- **Leg 78 (Route-HLB) — NO:** precision audit of CHL's Scenario-2 contraction anchor — no
  sixth digit exists on five channels; the `~1%` was ours, not theirs.
- **Leg 79 (Route-PC) — NO, stop-the-line:** `radii_polynomial_status` performs no domain
  validation; 11 of 25 hypothesis-violating inputs return `closes=True` (39-case battery).
  The BLOCKED_AT_STEP_ONE half holds (0 of 3 carry a bound). Latent only — both in-repo
  callers pass `(None, None)`. Not patched, per the gate; repaired outside the leg system.
- **Leg 80 (Route-BHN) — NO:** the bordered Newton's `converged` flag survives 336 hostile
  cases with 0 false reports; four reporting weaknesses measured, module untouched.
- **Leg 81 (Route-BRS) — NO:** 0 of 12 recorded rungs fire the status predicate, 4.2
  decades of margin at the loosest tolerance and 7.2 at the ladder's own.
- **Leg 82 (Route-EXT3) — NO:** rank-3 `Boussinesq_S2_nonsymmetric` uncertified, 0 of 7
  channels, 126 days open.
- **Leg 84 (Route-TNA) — YES/SILENT:** 8 of 8 domain hazards return a number, 0 of 6
  exponent-bearing surfaces carry a domain field, and 14 of 16384 samples move `p` by
  0.4166. Repaired outside the leg system; leg 55's banked margins confirmed uncontaminated.
- **Leg 86 (Route-LSP) — YES:** post-repair check of the line sweep — bit-identical across
  the repair, 20 of 20, timing +1.12% against a 0.29% null.
- **Leg 87 (Route-IVB) — YES:** independent post-repair regression check of
  `solver/interval.py` (leg 69's two soundness defects), gate answers YES.
- **Leg 88 (Route-GCA) — NO:** `gclm_family.py`'s residual propagates every poisoned
  coefficient, 0 silent corruptions in 37 cases.
- **Leg 89 (Route-BOA) — YES, escalated:** `solver/boussinesq.py` silently corrupts on 19
  of 82 gate-deciding cases; module untouched by the leg. Repaired outside the leg system
  (19/82 -> 0, bit-identical elsewhere, no banked Phase-1 result contaminated).
- **Leg 90 (Route-EXT4) — STILL OPEN:** Chen-Huang-Li Conjecture 2.4 (stability of the HL
  singular steady state) unresolved at 2026-08-06, 126 days after v1 — 10 channels, 0
  resolutions in either direction, 4 false friends excluded on quoted grounds.
- **Leg 91 (Route-FGA) — YES:** `fractional_gclm.py` silently accepts `s<0` and `nu<0`,
  returning a finite `p` that moves the measured `s_c` by up to +13.3%. Repaired outside
  the leg system (now rejected at construction; `s_c` untouched).
- **Leg 93 (Route-EXT5) — NO:** no independent verdict on arXiv:2604.09949 in 118 days;
  the author's own corpus asserts the negation.
- **Leg 94 (Route-TNB) — NO:** leg 84's domain guard is PRECISE — 0 false positives over
  163 in-window probes.
- **Leg 97 (Route-WSA) — NO:** `FitnessEngine`'s shared inverse answers NO to the
  silent-corruption gate, 0 of 100+ cases; banked as 14 regression gates.

Addendum: leg 67's gate was already narrated in the block above; what landed in this
window is its post-landing `VERIFY` review (primary source re-fetched, the negative holds,
two precision caveats). Five bench-repairs also landed in this window, all dispatched
outside the leg system: leg 64's Trap 1 prose, leg 69's `interval.py` soundness pair, leg
84's `target_norm.py` domain guard, leg 89's `boussinesq.py` four defects, and leg 91's
`fractional_gclm.py` parameter guard.

No link of the L1->L4 chain moved in any of the twenty. Clay unchanged at ~0.05%.

Per-leg file coverage inside this window is complete: 0 of 20 legs are missing
`experiments/journal/leg_N.md`, and 0 of 20 are missing `writeup/novelty/leg_N.md`. The
one standing gap is leg 72's own carry-over — `experiments/journal/leg_60.md` and
`writeup/novelty/leg_60.md` are still absent from `main` (1 leg, 2 files), because branch
`leg/pq-v1` was pushed and never merged per leg 60's own gate. This leg did not create
them on leg 60's behalf.

Legs 92, 96, 98, 99, 100 and 101 have branch progress but have NOT landed on `main` (0
`main` commits each at this pass), so they are deliberately absent from this block and
belong to a future window.

## Landings, 2026-08-06 integration cycle (resumed after the RemoteTrigger self-chain)

- **Leg 96 (Route-LHA) — NO:** `line_hilbert.py`'s dense operator (six importers) is robust —
  0 silent corruptions in 25 in-scope adversarial cases; worst disagreement 3.07e-13 vs a
  1e-08 threshold. Module untouched; battery banked as a permanent regression test.
- **Leg 92 (Route-GLA) — YES, repaired:** `gclm.py` had 4 silent-corruption mechanisms under
  adversarial inputs. Fixed via `bench/fix-gclm-silent-corruption`; all existing gates
  unchanged.
- **Leg 99 (Route-BVA) — YES, repaired:** `boussinesq_velocity.py` returned 7/22
  `SILENT_WRONG` results under degenerate polar-grid inputs (r=0 singularity,
  self-intersecting boundary). Fixed via `bench/fix-boussinesq-velocity-origin-fit`; leg 73's
  Lamb-benchmark reproduction confirmed unaffected.
- **Leg 89 — repaired:** `boussinesq.py`'s silent-corruption battery (4 defects). Fixed via
  `bench/fix-boussinesq-silent-corruption`.
- **Leg 83 (Route-MFG) — NO, partially repaired:** gate 11 missed 8 of 9 adversarial
  divergent trajectories (worst: 4.99e130x state growth, Newton residual 1.6e-10 of
  threshold). A scale-free state-growth threshold (via `bench/fix-marginal-flow-gate11-coverage`,
  superseding the unmerged `leg/mfg-v1`) closes 4 of the 9 missed cases including the worst,
  0 false positives, all 11 existing gates unchanged. 5 cases remain open — not re-raised as
  a fresh escalation since the repair is a genuine partial fix, not a quiet one.
- **Leg 106 (Route-HPA) — YES, not repaired (measurement leg, no fix in scope):**
  `hilbert_pointwise.py`'s pointwise |H(h)| bound fails to dominate the true value on 2 of
  the tested degenerate/NaN-poisoned configurations. Landed as a measurement; repair not yet
  scheduled.
- **Leg 60 (Route-PQ) — escalation #4, resolved by the user, landed 2026-08-06:** reproduced
  every quoted number in Route-PORT v1/v2 (legs 46/47) from their curated JSON; 111/114
  re-derived, 3 did not (a mislabelled ρ=8→10 baseline reading 28× instead of 63×, a
  transcription slip pasting the n=201 resolution-table value into the reach table's ρ=8
  row, and a truncated last digit). Both ban-bearing numbers (leg 46's clause P6b, leg 47's
  wrong-sign trend) were exact throughout. User approved the correction; applied directly to
  the prose and to both evidence scripts' quoted literals — both now report CLEAN 114/114.
- **Leg 112 (Route-AS2) — YES on both flagged readings:** verified §24's two unresolved
  readings of arXiv:2603.25104 from the full PDF. The a-sign dichotomy holds but is
  conditional on degenerate initial data, so §24's "possibly the wrong object" inference does
  not follow (their Thm 2.7/7.10 prove existence for all a in (-inf,1)). The fixed-point
  identification with the banked first integral is confirmed in its strongest form (their p.38
  definition matches (FI) including the anchor constant, re-checked to 1.15e-13 relative).
  Priority dated: the traveling-wave form is 2603.25104's; the underlying method is HQWW24
  (2024). No ban lifted, L1 stays measured-dead.
- **Leg 113 (Route-MS) — NO:** 0 of 8 published certified INVISCID self-similar blow-ups run
  a diagonal-tail (ell1-multiplier/radii-polynomial) framework, over a 15-row located ledger;
  holds 0/2 peer-review-confirmed, 0/6 with every judgement call reversed. Clause ablation:
  only dropping "inviscid" flips the gate (Takayasu-Lessard-Jaquette-Okamoto, Numer. Math.
  151:693-750 2022, on nonlinear heat). Lesson 87 confirmed; no published repair for the
  realization legs 52-54 measured dead. No escalation.
- **Leg 116 (Route-NKA) — YES, not repaired (audit leg, escalated per its own gate):**
  `nk_bounds.py`'s `budget()` validates only Z2>0, so a forbidden Z0=-1 turns an honest
  refusal at a planted non-solution into a certified ball containing no true zero (missing
  by 1.16 ball radii); 21/52 hypothesis-violating inputs false-close, plus a second family
  where `farfield_modelling_error_bound` under-reports by up to ~1e8x via a truncated-window
  max standing in for a supremum. All latent — every in-repo caller stays inside the range
  where the bounds dominate (worst ratio 0.99997); no banked Route-D number affected.
  `solver/nk_bounds.py` not patched, per the gate. Third module found with the same
  Y0/Z0/Z1 nonnegativity gap (after port_certification.py and interval_certificate.py, both
  already repaired) — flagged for the DM as a candidate shared-guard repair rather than a
  third one-off fix.
- **Leg 120 (Route-SUA) — YES, not repaired (audit leg, escalated per its own gate):**
  `spectral_utils.py`'s `dealias_mask` retains one Fourier mode too many whenever 3|n
  (Bowman 2013 requires k < n/3 strictly, module uses <=), making the "exact rate"
  `energy_production` wrong by 1.66e-01 relative at n=81 vs 2.47e-14 elsewhere. Latent:
  every grid size on that path is a power of two, so 0 of 107 banked
  `energy_balance_residual` records are exposed. Five further silent-absorption defects
  found (Nyquist/mean-mode poison erased, int truncation, malformed-k acceptance). The
  one-character fix is verified bit-identical at every resolution the repo runs, but is
  blocked by a test that encodes the defect (`test_spectral_utils_dedicated.py:121-122`)
  and by an identical `<= n/3` cut in `boussinesq.py`'s 2D sibling — flagged for the DM as
  a single repair pass covering both.
- **Leg 111 (Route-WE) — NO, 0 of 7:** the Chen-Hou weighted-energy realization is the
  THIRD to die on the a=0 CLM linearization. Every admissible weight's coercivity gap
  converges to -(3-gamma)/2 as the grid refines, and damping at the origin needs gamma>3
  while the weighted space exists only for gamma<3 — the same threshold, so the window has
  zero width, not merely a bad margin. No escalation.
- **Leg 103 (Route-GLB) — YES, repair confirmed solid:** leg 92's gclm.py fix holds under
  its own 54 gate-scoped adversarial cases (19 silent corruptions -> 0), with zero
  regression measured bitwise against the pre-repair module (0 of 20 banked T* values, 0
  of 17 production runs moved). Leg 92's battery now a permanent 8-check regression suite.
- **Leg 62 (Route-CP) — NO, 6 of 6 located clauses fail:** Cadiot arXiv:2505.03091 does not
  cover NG's zero-diagonal case at full-text depth. Lemma 3.2's required shift saturates at
  0.28723 on his own Whitham operator but grows linearly (63->1023 over M=128..2048) on
  ours, so no finite shift survives the limit for us. NG (leg 58, live and concurrent) may
  claim novelty against this paper and no further.
- **Leg 104 (Route-BVB) — YES on both clauses, repair confirmed solid:** leg 99's
  boussinesq_velocity.py fix holds under leg 99's FULL 22-case battery (0 SILENT_WRONG, 0
  returning -0.0, vs 7/5 before), and leg 73's Lamb corner-image benchmark reproduces to
  ~1e-12 relative. Banked as a permanent regression suite alongside legs 73 and 99.
- **Leg 115 (Route-DCA) — YES, not repaired (audit leg, latent):** `decay_collocation.py`'s
  `graded_inverse_norm` at grid size J=1 returns a value bit-identical regardless of
  NaN/Inf poisoning in c or the nodal field (the gauge row consumes the system's only
  row, so J>=2 correctly propagates poison but J=1 cannot). Two further gaps:
  `sup_op_norm` silently swaps domain/codomain axes on 1-D input (30/30 mismatch), and a
  complex-valued alpha silently downcasts via ComplexWarning. All latent — no in-repo
  caller uses J<8, non-2D sup_op_norm input, or complex alpha. Not patched.
- **Leg 117 (Route-HRA) — YES, not repaired (audit leg, latent):** `hl_rescaled.py` has 4
  silent-corruption mechanisms: `velocity()` never validates X is ascending (20/20
  permutations silently wrong) or X_ref in-domain (4/4 out-of-domain silently clamp);
  `sinh_grid_at(M<0)` silently mirrors; `degenerate_ic`'s closing `np.where(X>0.0,...)`
  launders a NaN abscissa into the same 0.0 a legitimate X<=0 point produces. All latent
  (0 of 35 in-repo call sites exposed). Not patched.
- **Leg 114 (Route-CNA) — YES, not repaired (audit leg, latent):**
  `collocation_newton.py`'s `newton_gauged`'s `converged` flag is blind to the dropped row
  (structurally always True on the reduced subsystem), and the one-gauge system has a
  second, quiet root: Omega = -1 satisfies every residual row and the gauge row to 1e-13,
  is returned with converged=True, and sits outside the decay class by 5.84e+03 at J=60,
  growing to 4.15e+04 at J=160 — the inflation grows WITH resolution, not shrinks.
  `critical_radius` also has no magnitude test (a -1e-16 dip in an otherwise-0.5 field
  returns a finite X_c where the truth is infinite). All three measured latent, not live:
  production always starts from the true anchor, 140 perturbation draws never hit the
  spurious constant, 200 noise draws never flipped X_c. Banked as a 12-check regression
  suite (7 KNOWN GAP assertions for a future repair to invert). Does not reopen leg 110's
  L1R death certificate audit. Not patched.
- **Leg 121 (Route-CDA) — YES, not repaired (audit leg, latent):**
  `critical_dissipation.py`'s precondition "p a positive integer (2s=p)" is enforced only
  by a bare `int(p)` cast: `CriticalDissipativeFlow(..., p=1.9, ...)` requests s=0.95 but
  silently builds p=1 (s=0.5) instead, converging to machine precision with alpha/alpha_1
  bit-identical to an honest p=1 run, no exception, no warning. A realistic float-
  arithmetic route to the same defect was demonstrated (2.0*(2.5-1e-12) lands int(p)=4,
  one unit below the intended 5). Supporting findings: negative mu (anti-dissipation)
  converges with no domain check, mu_decay_time can return a negative time,
  marginal_verdict(NaN) returns a definite wrong classification. All 24 call sites outside
  the module pass p as a literal integer — latent, 0 banked exponents at risk. Not patched.
- **Leg 119 (Route-HHA) — YES, not repaired (audit leg, latent):** `hilbert_holder.py`'s
  per-point routing rule transplants leg 106's unsound shape from the sibling
  hilbert_pointwise.py: two NaN-free configurations (gamma=0.0, gamma=-0.5) exceed the
  reported bound by up to 1.23x at extreme adversarial feature widths, both eps-
  truncations of a log-divergent integral. The public assembly API crashes cleanly at
  gamma=0.0 exactly but returns a silent finite pair at gamma=-0.3. Shipped
  (alpha=1.5,gamma=0.5) and production (alpha~1.4,gamma~0.15) configurations confirmed
  safe. Not patched.

No link of the L1->L4 chain moved. Clay unchanged at ~0.05%.

## Pointer catch-up (leg 137/JR3's flag) — 15 legs with landed gates and no prior pointer

Pointers only, per JR2/JR3 convention; full detail in each `experiments/journal/leg_N.md`.

- **Leg 58 (Route-NG) — YES:** the no-go is a THEOREM on the class `A21 = 0`: `Z_1 >= 1`
  at every `K`, every `s < 1`, three-line proof off the `(I - AL)x` block structure. The
  general `A21 != 0` class stays measured only (battery floor 8.9591). Merged as-is by DM
  ruling; stage `NG` -> DONE, stage `B` -> NEXT.
- **Leg 71 (Route-CAP) — capabilities.py self-audit, landed.**
- **Leg 85 (Route-GRA) — YES:** `gclm_rescaled.py`'s relaxation loop false-converges after
  1 step on certain gauge-scale trajectories. Bench-repaired.
- **Leg 98 (Route-ICA) — YES:** `interval_certificate.py` has the same Y0/Z0/Z1
  fabrication-acceptance gap as leg 79's `port_certification.py`. Bench-repaired.
- **Leg 100 (Route-HNA) — YES:** `holder_norms.py` silently accepts NaN/Inf/degenerate
  input across 6 mechanisms. Bench-repaired, independently re-confirmed by leg 131.
- **Leg 101 (Route-OLA) — YES:** `op_lower.py`'s lower bound is violated in 47 of 209
  adversarial cases. Bench-repaired, independently re-confirmed by leg 132.
- **Leg 105 (Route-ICB) — YES:** post-repair regression check on `interval_certificate.py`,
  leg 98's battery independently re-derived, 0/36 false accepts, bitwise same-process match.
- **Leg 107 (Route-FIA) — YES, escalated not patched:** `first_integral.py` fabricates
  out-of-support values and NaN-absorbs; bench-repaired (compact-support guard).
  Independently re-confirmed by leg 135.
- **Leg 108 (Route-IX2) — second freshness audit of `writeup/INDEX.md` since leg 68.**
- **Leg 123 (Route-EXT6) — NO:** literature watch, 0/17 channels find a new certified
  inviscid self-similar profile or completed dissipative gCLM certificate.
- **Leg 126 (Route-BX) — NO:** stage `B`'s full declared search space (1,686
  configurations) is fully covered by the banked record, zero uncovered; even a perfect
  search over the unexplored headroom lands at `Z_1 >= 6.0424`, 6.04x short. The committed
  sequence is now exhausted (escalation #1, parked for the user).
- **Leg 131 (Route-HNB) — YES:** independent re-confirmation of leg 100's `holder_norms.py`
  repair, 14/31 -> 0/31 silent cases, 19/19 clean values bit-identical.
- **Leg 134 (Route-FGB) — YES:** independent re-confirmation of leg 91's
  `fractional_gclm.py` repair, 7/7 cases closed at construction, `s_c` bit-identical.
- **Leg 136 (Route-MF2) — NO:** gate 11's 5 remaining divergent-trajectory misses
  decompose into 3 mechanisms; 0 of 5 pre-named criteria admit a separating threshold.
- **Leg 141 (Route-WEL) — YES:** leg 111's zero-width weighted-energy window is published
  in content (Elgindi-Ghoul-Masmoudi Prop 2.1 et al.), though not as a literal sentence;
  caps the reading of leg 111's numbers, does not rewrite them. Verified line-by-line by a
  post-landing review: all 10 quoted fragments confirmed genuine in freshly-downloaded
  PDFs, the numeric coincidence re-derived as a structural identity. Two process gaps
  flagged by the verifier, not the math: the novelty cap was never written back into
  `capabilities.py` (fixed in this same integration commit) and the DOCS quartet lacks
  BLOG/TECHNICAL files (precedent-conformant with leg 65/L1G, flagged for a DOCS pass).

No link of the L1->L4 chain moved in any of the fifteen. Clay unchanged at ~0.05%.

## Pointer catch-up #2 (leg 155/JR4's flag) — 17 legs, window e4199c2..e832ead

- **Leg 122 (Route-ASA) — YES:** `advection_scope.py`'s far-field probe fabricates 4 of 8
  values per call on the default grid (2.29061 vs honest 3.09296 at X=1e4, -25.94%).
- **Leg 124 (Route-FSA) — YES:** `finite_support.py`'s `converged` flag self-reports true at
  residual 3.331e-15 while violating the profile equation by 1.217 off-grid (3.66e14x); 0
  importers repo-wide.
- **Leg 127 (Route-NGX) — YES(i), UNVERIFIED pending dedicated review:** claims Z_1>=1 for
  EVERY bounded approximate inverse (A21 free), superseding leg 58's A21=0-only theorem;
  cites Xu arXiv:2607.19762 for the same operator's invertibility on origin-H^2.
- **Leg 128 (Route-NKR) — landed, shared guard repair for nk_bounds.py + siblings.**
- **Leg 133 (Route-BOB) — YES:** independent regression confirmation of leg 89's
  boussinesq.py repair, 0/0/0 silent cases remaining.
- **Leg 135 (Route-FIB) — YES:** independent regression confirmation of leg 107's
  first_integral.py repair.
- **Leg 138 (Route-IX3) — NO:** INDEX.md corrected, 14 rows.
- **Leg 139 (Route-DGA) — YES:** decay_grading.py, five silent-corruption sites, headline a
  half-enforced step condition (26630.848 vs exact 3.999996).
- **Leg 140 (Route-NFA) — YES:** nk_fourier.py, a forbidden weight flips an honest refusal
  into a certified ball missing the true solution by 1.990 ball radii.
- **Leg 142 (Route-NSA) — YES:** nk_seminorm.py, a negative anchor speed understates a norm
  12.4904x.
- **Leg 144 (Route-ECA) — YES:** energy_coercivity.py, admissibility() collapses a 1.678e7
  power-divergence signal to exactly 1.000000 "converged".
- **Leg 146 (Route-CSA) — YES:** certificate_shapes.py, seven silent-corruption sites; also
  independently corroborates leg 126's 1,686-configuration completeness count (7/7 agree).
- **Leg 147 (Route-NKB) — NO (incomplete fix, not a regression):** leg 128's shared guard
  closes 17/21 of leg 116's false-closing cases; the 4 survivors are not alike, one carries
  no flag at all (Z_2 understated 714,285.7x).
- **Leg 149 (Route-PGF) — NO:** PROGRESS.md/DIRECTION.md ledger drift found and reported.
- **Leg 157 (Route-CDX) — NO:** Cadiot arXiv:2505.03091 offers no untried A21!=0
  construction; every preconditioning shape induces A21=0.
- **Leg 158 (Route-BDX) — YES with a ceiling:** BDL's own future-work item (2x2 cyclic
  reduction) compensates the zero diagonal partially but stays ~2x short of BDL's own
  threshold.
- **Leg 161 (Route-LSS) — YES:** LSS arXiv:2010.01201 explicitly contains alpha(1/2)=3;
  corrects the "three independent sources" framing to one shared ancestor.

No link of the L1->L4 chain moved in any of the seventeen. Clay unchanged at ~0.05%.

- **Leg 195 (Route-PQVER) — V1 YES / V2 NO:** independently confirms leg 60's landed
  Route-PORT correction on all five numbers (62.9877x, -2.5410243874, 1.1685027%,
  1.548471e+08, +0.4703336113, all under 1 half-ulp); finds the corrected value had not
  fully propagated (the old -2.541222 literal survived, unconsumed, in
  PHASE2_P2_NOTES.md and experiments/p2_route_hrb_v1_postrepair.py) — fixed in this
  integration cycle, 0 banked results affected.
- **Leg 170 (Route-CDB) — YES on both clauses:** post-repair regression check of
  solver/critical_dissipation.py (leg 154's non-integer-exponent truncation repair),
  re-verified from scratch after the interrupted session: 96/96 case x entry-point
  cells refused, 276,077/276,077 leaves bit-identical, 0 moved. Leg 121's battery
  banked as a permanent regression suite. Secondary (non-claim-bearing): leg 121's
  own banked JSON is a drifted environmental reference (0/9 rows bitwise, worst
  2.95e-09 relative on alpha_1) -- does not affect either clause.
- **Leg 196 (Route-USC2) — STILL_SHORT:** the authors' later work (arXiv:2511.22819,
  read at full text, 27 pp) carries no certificate for arXiv:2509.14185's unstable
  singularities -- 0 hits for interval arithmetic/enclosure/certif/eigen; all 4
  "computer-assisted" mentions are definition/prerequisite/aspiration, 0 achieved.
  0 of leg 175's 4 open items closed; 3 new obstructions named (binding one: a
  6.0-decade gap between the 1e-13 residual and the +-1e-7 enclosure of lambda at
  IPM's 4th unstable mode).
- **Leg 190 (Route-EGML) — YES, with a correction:** "EGM" located at primary source
  (arXiv:1906.05811 / Anal. PDE 14 (2021) 891, Prop. 2.1), appended to
  literature_gates.py. Re-verified from the actual LaTeX e-print: the bracket is
  -(1/2 - C|a|) (degrading), not the (-1/2 - C|a|) form legs 141/165 and this leg's
  own novelty pass had carried -- identical at a=0 so 0 banked numbers move; 6 sites
  flagged for the record, none patched under this leg's authority.
- **Leg 187 (Route-M2CI) — NO:** the first attempted computer-assisted certificate of
  Chen's inviscid gamma=2 profile (Object A) fails on ISOLATION, not budget -- the
  profile sits on an exact dilation orbit (zero polynomial in exact Fraction
  arithmetic, 5/5 test values), so its tangent is an exact kernel and Z_0+Z_1 >= 1 for
  every admissible A; Y_0 is exactly 0, the best the framework admits, and it still
  cannot close. Second, independent failure: Z_2 ~ n^2.36 over a 6x ladder. Fully
  characterized negative, quartet complete (fig65).
- **Leg 197 (Route-VNL) — YES:** arXiv:2208.09445 (Buckmaster-Cao-Labora-Gomez-Serrano)
  appended to solver/viscous_novelty.py::PRECEDENTS (6->7 rows, append-only, 11/11
  claims traceable to leg 174's own JSON). Stage V's verdict unchanged (YES on
  arXiv:2410.05480 alone).
- **Leg 198 (Route-BHA) — YES, ESCALATED (parked, not merged):** bordered_hl.py
  silently accepts a negative border weight with no check -- induced_sup_norm can
  return a NEGATIVE "operator norm" (-1.0 to -4.0e9 on hand-checked cases whose true
  weighted norm is 101.0). Same-magnitude sign-flip corrupts Z_1 by up to 1.198e9x,
  Z_2 by up to 1.189e17x, and can flip a certificate's own closure verdict (no root ->
  root at 2.217e-11). Three more silent-corruption sites found (permuted-grid
  velocity_matrix, arity-truncating pin, NaN-dropping tail_exponent mask). Blast
  radius LATENT: 0 banked numbers currently impeached (no live caller passes a
  negative border weight). Module unpatched, branch leg/198-bha-v1 pushed.
- **Leg 201 (Route-ICA2) — YES, ESCALATED (parked, not merged):**
  interval_certificate.py's matmul_point_interval silently returns a
  non-containing enclosure in the subnormal band -- containment escape 200 eta =
  24.63% of the returned magnitude at the shipped BorderedHL N=405, driving Y_0
  19.66% below the quantity it claims to upper-bound while still flagged
  rigorous=True. An independent unrepaired clone of leg 69's defect 1 (a repaired
  sibling routine encloses at 0 eta on identical input). Severity LATENT: live
  minimum row mass sits 292.9 decades above the failing band, 0 banked numbers
  wrong. Module unpatched, branch leg/201-ica2-v1 pushed.
- **Leg 204 (Route-TNA2) — YES, ESCALATED (parked, not merged):** target_norm.py's
  domain guard windows on max|X| rather than the true data interval, so an
  asymmetric grid silently extrapolates 535 of 16384 theta-samples while reporting
  n_outside_grid=0 and domain_valid=True -- yields p=-0.0889 against exact 1.4
  (386x systematic error, wrong sign), defeating three legs' (55/84/94) worth of
  prior guard work while reporting clean. Three more silent-wrong mechanisms found
  (frac_outside_grid threading, a negative analytic_tail bound with finite=True,
  fit_exponent overstating n_points 3.0x when dropping NaN bins). 0 of 7 mechanisms
  reachable from the banked call path -- leg 55's +0.394/+0.094 margins
  uncontaminated. Module unpatched, branch leg/204-tna2-v1 pushed.
- **Leg 214 (Route-EGMB) — YES:** the 5 leg-141/leg-165 prose sites flagged by leg
  190 corrected to EGM Prop. 2.1's true bracket -(1/2 - C|a|), independently
  re-verified against arXiv:1906.05811's own LaTeX e-print (not just trusting leg
  190). Diff is exactly 5 lines / 5 changed characters across 3 files; 0 banked
  numbers moved (both readings give -0.500000 at a=0). Mechanical, quartet-thin
  per the leg-180/179/186/108 prose-correction precedent.
- **Leg 200 (Route-PCA) — YES, ESCALATED (parked, not merged):** port_certification.py
  has four independent silent-corruption mechanisms: line_sweep_solve inverts a
  DIFFERENT operator when s_rho<0 (18820x relative error, no exception);
  radii_polynomial_status closes on a ball of radius exactly 0 at Y_0=0 (leg 51's
  own a=0 CLM value); leading_order_solve truncates integer rhs (rel err 1.000);
  stall_verdict's NaN<2.0 comparison gives poisoned ladders a confident "bending"
  verdict. Two of the four are catchable by guards that already exist in-repo and
  are never called here. Measured: 0 banked numbers move -- the live PORT run's
  min(s_rho)=0.3896>0 sits inside the corner where all four are dormant. Module
  unpatched, branch leg/200-pca-v1 pushed.
- **Leg 215 (Route-CGR) — NO, ESCALATED (parked, not merged):** the one-line isinf
  repair at nk_bounds.py:430 closes leg 199's M1 mechanism cleanly (alpha=-inf now
  raises instead of returning NaN; 8/8 live call sites bit-identical at 0 ULP), but
  only 1 of leg 199's 16 originally-found gaps is M1 -- the other 15 (non-finiteness
  defects across M2/M3/M4/M5/M7) live in read-only certificate_guards.py, out of
  this leg's territory. Repair itself sound; gate's premise (that all 16 were the
  missing-isinf family) is what fails. Parked pending a leg that owns
  certificate_guards.py.
- **Leg 205 (Route-BVR) — YES, ESCALATED (parked, not merged):** boussinesq_rescaled.py
  silently fabricates origin slopes via TWO independent, separately-confirmed
  mechanisms in odd_field_x_slope. Defect A (second occurrence of leg 99's class, at
  the exact line leg 99 flagged and declined to test): empty fit window -> lstsq
  returns exactly 0.0 vs truth 2.0 (2000x tolerance). Defect B (NEW, needs no
  degenerate grid): hard-coded absolute r_win=0.4 with a discarded lstsq residual
  drives modulation()'s c_l to +0.188 vs truth 1.4 (86.5%, 1731x tolerance) on a
  FULLY RESOLVED grid -- rank and condition number constant throughout, so leg 99's
  own fix is provably blind to B. Measured: no banked result re-run, but the safe
  exp(-r^2)-class envelopes used elsewhere give reason (not proof) to expect no
  movement. Module unpatched, branch leg/205-bvr-v1 pushed.
- **Leg 193 (Route-M2CV) — YES:** independently reproduces leg 187's NO on both
  failure points, upgrading the dilation-orbit kernel argument from a 5-value float
  check to an EXACT symbolic identity in Q[X,b] (zero polynomial for every g>0, not
  just 5 pinned values); DF[phi]=0 confirmed exactly. 20/20 floats reproduce at
  relative difference 0.0. One precision caveat, not verdict-changing: Z_2's
  n^2.36 is a ladder-dependent least-squares average -- local slopes climb
  2.13->2.50, a second ladder fits 2.2466 -- but every local slope stays >=1.88 and
  rising, so the divergence verdict itself is unaffected.
- **Leg 206 (Route-GSA) — YES, landed directly (not claim-adjacent):** ga_search.py
  silently returns a wrong value on 12 of 41 adversarial cases across six mechanisms
  (a -inf optimum demoted to worst rank; a NaN gene surviving in a "converged"
  individual at finite fitness; inverted bounds collapsing offspring onto a single
  point; elite_frac>=1 freezing the breeding loop at 864347x worse while reporting
  40 generations; a bounds-length mismatch returning a rank-1 genome). All six are
  orthogonal to the standing GA ban (defects in optimiser input-handling, not
  fitness validity) and measured, not assumed, clean: all 9 live ga_minimize call
  sites audited safe (static ast parse) and the sole production fitness is
  structurally unable to emit -inf. Module read-only, landed straight to main.
- **Leg 208 (Route-TSA) — YES, ESCALATED (parked, not merged):** target_selection.py
  is a SIXTH, never-enumerated member of leg 128's radii-polynomial guard class
  (certificate_guards.py's own docstring claims to cover every such function; this
  one was never on the list). 9/9 forbidden (Y0,Z1,Z2) triples return
  feasible=True, 5 with a negative certified radius (worst -1413.71);
  y0_budget(2.0,1.0) == y0_budget(0.0,1.0) == 0.5 bit-for-bit against a true budget
  of 0; unknowns() understates the dim-2 count by 598.5x. LATENT: 85/85 banked Z1
  records lie in [0,1), no negative input is constructible from any live caller.
  Confirms leg 63's "exactly one candidate passes" and the whole gamma=2 line are
  NOT at risk -- that predicate lives on a disjoint, parked, unmerged branch and
  never touches Y0/Z1/Z2/budget. Process note for the DM: six legs have now each
  found "the last" uncensused guard-class member one at a time; a systematic census
  test may be worth more than another one-off audit.
- **Leg 203 (Route-RSA) — YES, ESCALATED (parked, not merged), CLAIM-ADJACENT:**
  rescaled_spectrum.py has 8 silent-corruption mechanisms. Headline (R1):
  converged_spectrum(K_fine==K_coarse) certifies the entire continuum -- n_kept
  goes from the correct 2 to ALL K (24/24 at K=48, 24x inflation), including a
  spurious +-40.4623i pair, the exact Hopf-crossing signature the module exists to
  rule out. R2 is the one NOT latent: 5/7 banked Route-E and 7/7 banked Route-G
  rows sit on points above the module's own 1e-8 convergence threshold -- but
  BOTH routes already banked their residuals and both are already flagged
  converged=False by the module's own conservative check, so no banked number is
  confirmed WRONG, only discoverably imprecise. Confirmed NOT downstream of the
  origin-H^2 certificate work (176/186/192): that module imports only numpy and
  math.comb. R3-R8 latent (sign-mismatched da degrading to a cold solve, a dropped
  36.9-decade far-field term, non-integer K truncation, etc). Tenth audit-family
  item and the first genuinely claim-adjacent one this cycle.
- **Leg 212 (Route-USC2V) — YES on all three clauses:** independently confirms leg
  196's STILL_SHORT verdict on arXiv:2511.22819 from a freshly re-fetched primary
  source (PDF extraction byte-identical to leg 196's own). 29/29 comparison rows
  agree, 0 disagreements: 0 certificate-apparatus terms, 0 of 4 computer-assisted
  mentions ACHIEVED, 0 of leg 175's 4 open items closed, all 3 named obstructions
  verbatim present (Fig.7(f) digit-exact, 6.0-decade gap and 1.570 decades/mode fit
  both independently re-derived). 3 locator-only citation slips found, none moving
  the gate.
- **Leg 207 (Route-DPA) — YES, landed directly (not claim-adjacent):**
  dissipative_profile.py has 4 latent silent-corruption sites. Most severe: Y_0/Z_2
  are measured at the constructor's stored `a`, not the solved one -- inflation up
  to 1.144e+12x when they drift; a zero profile silently echoes Chen's exact
  Delta=-1/3 at residual_rms exactly 0.0 with no health indicator distinguishing it
  from real convergence. Measured, not assumed: a static call-site audit of legs
  125/185/187 finds 0 exposed sites -- every landed call passes an explicit gauge
  and the correct norm string. Eleventh audit-family item.
- **Leg 211 (Route-XU11) — YES, ESCALATED (parked, not merged):** Xu arXiv:2607.19762
  characterizes NO anti-diffusive/sign-changing branch (0 of 12 verbatim-verified
  passages admit nu<=0; his own dissipative equations at s6.1 and Appendix A both
  STIPULATE nu>0). But his s=2 sub/supercritical boundary a~=0.39/0.386 (S6.1)
  matches leg 185's independently-computed a*=0.38649640 to 4.48e-04 (0.116%),
  within 1.23x of Xu's own stated error bar -- and his gamma := 1-s*c_l at s=2
  equals this repo's own Delta parameter EXACTLY (0.0e+00 over all 8 Table 1 rows,
  an algebraic identity not an approximation). Genuine external cross-validation
  of leg 185's boundary location, though NOT of its sign-flip claim, which Xu's
  paper does not address either way.
- **Leg 202 (Route-PNA) — YES, ESCALATED (parked, not merged), MATERIALLY EXPOSED
  (not just latent):** profile_newton.py has 3 mechanisms, 22 silent-wrong cases.
  M1 is the serious one: `continuation` returns off-branch grid-scale roots as
  converged=True at machine-zero relres (both gauges satisfied to 0.0e+00) --
  c(a=1.50) = 0.20427/0.23717/0.97282 at n=101/201/301, all three "converged" at
  machine precision, 376% apart. Route-D v11's own banked a_max_machine/GA_boundary
  claims trust exactly this flag and show the branch-jump signature already in
  their own JSON (weighted_defect 0.50/4788/73372 at a=0.5/0.8/1.0) -- the
  rejecting information existed in the caller's own diagnostics and never reached
  the module's verdict. Route-ASA (leg 122) confirmed NOT affected (substrate
  a=0.0/0.3, inside the on-branch zone). M2: a small-amplitude start escapes the
  scaling family at default parameters (Omega(0)=-0.75 not -1, c off by 6.15e+05x,
  sign flipped). M3: c0 never range-checked. THE MOST CONSEQUENTIAL FINDING THIS
  CYCLE given explicit banked-claim exposure, not just latency.
- **Leg 213 (Route-LGC2) — NO, ESCALATED (parked, not merged), minor/cosmetic:**
  legs 190's and 197's appended literature_gates.py/viscous_novelty.py rows are
  clean on format, duplicates, and transcription (all measured, not asserted). But
  EGM_PRIMARY_READ's own sign_correction_leg_190 field describes 5 prose sites as
  still carrying the wrong bracket -- true when the row was written, false now
  that leg 214 fixed all 5 (2c901c4). The ledger's own claim about this repo's
  current files is backwards. 0 banked numbers move; a one-tense-word mechanical
  fix, not urgent.
- **Leg 209 (Route-SCA2) — YES, ESCALATED (parked, not merged), PROOF CONFIRMED
  SAFE:** spectral_certificate.py (the module Theorem NGX is proved against) has 4
  latent mechanisms, headline being an unordered NaN comparison (`nan > 0` is
  False) sending sigma_min from 0.0349 to +inf and inverting
  counterexample_norm_floor from 14.3206 to a plausible-looking 0.0 -- exactly the
  theorem's own conclusion, reversed. But measured, not assumed: 0 shipped
  (class,param) pairs produce NaN/Inf or a negative weight, nearest shipped s is
  0.263852 clear of the failing band, and clean-input float64 matches exact
  rational Gauss-Jordan to 7.24e-16. Explicitly distinguished and confirmed:
  Theorem NGX rests on an exact folklore inequality and an analytic tail estimate,
  neither of which touches this code path -- the proof itself is untouched, only
  the numerical module has an adversarial-input gap. Careful, well-scoped finding.
- **Leg 223 (Route-PUB3) — YES:** the audit-family synthesis, corrected to the
  ACTUAL count this cycle -- THIRTEEN escalations (188, 198, 199, 200, 201, 202,
  203, 204, 205, 208, 209, 213, 215), not the seven its own dispatch spec named.
  Graded 1 MATERIALLY EXPOSED (202) / 1 claim-adjacent (203) / 1 uncertain (205) /
  9 zero-so-far / 1 pending-ruling, and states plainly that not one of the seven
  repair legs dispatched so far had actually landed at the time of writing, so
  every "zero" is the finding leg's own unconfirmed measurement. Recovered a
  second exposed consumer of leg 202's finding (Route-D v12, plausibly exposed,
  in no shared ledger) and printed three unresolved banked-record disagreements
  rather than silently picking a side. Self-referential finding: reports/STATUS.md
  (orchestrator-owned, committed) was stale by ten escalations at time of writing
  -- the same silent-wrong-bookkeeping shape the whole cycle was hunting in code.
- **Leg 220 (Route-TNR) — YES on both clauses:** target_norm.py's domain guard now
  windows on the true data interval [X.min(), X.max()] rather than |X|.max(),
  closing leg 204's finding. 5/5 asymmetry rungs go silent->flagged with EXACT
  counts matching independent truth (535/16384 at the worst rung, was 0). 295,203
  A/B leaves bit-identical, leg 55's banked margins reproduce to 0 difference.
  6 of leg 204's 7 mechanisms still open (territory was windowing only) --
  re-measured post-repair so "open" is a number, not a guess.

**EXTERNAL USER REVIEW APPLIED THIS CYCLE.** A composition-floor quota (>=3 of 10
live slots must be math/literature/construction-typed, not audit/repair/verify)
was written into ORCHESTRATION.md and DIRECTION.md so it survives a session
restart. Leg 202's Route-D v11 exposure was split into three actions: leg 226
(repair, now explicitly treating leg 202's prescribed fix as a hypothesis per the
150/151/152/154 precedent), leg 236 (independent dependency trace -- which banked
numbers actually move, separate from the repair), leg 237 (a class-level census:
which other modules share leg 202's scale-invariant-residual blind spot). Leg 238
folds leg 176 into PUB2 and applies leg 183's Xu-§8 citation to PUB1, both
additive. A new gate-contract clause (lesson 91) requires every negative-result
gate to name its realization/trial-space/basis. Three low-value slots (219
duplicate, 222 FBA, 224 GCC) were preempted for 236/237/238; none of the three
preempted agents had reached a landing.
- **Leg 238 (Route-PUB4) — YES on both conjuncts, LANDED:** PUB2 gains leg 176's
  construction outcome as its fourth data point (both halves inseparable: sigma_min
  = 0.0908 truncation-independent to 0.139% over 16-fold, vs the NO's Z_1 best cell
  140.72 where <1 is needed); PUB1 §3 now cites Xu §8 verbatim per leg 183. ONE
  DISPATCH PREMISE CORRECTED: leg 192 has NOT actually verified leg 176 yet --
  its only commit anywhere is a novelty pass (483b0d7), no runner, no verdict --
  so PUB2 states leg 176's numbers as one leg's own float64 measurements, not as
  independently confirmed. (Orchestrator note: leg 192's construction/measurement
  work exists uncommitted in its own worktree, mid-background-compute -- not lost,
  just not yet landed; leg 238's correction is accurate as of when it checked.)
  ONE RESIDUE FLAGGED: PUB2's three sigma_min>=0.71465 call-sites (leg 163's own
  witness) are optimistic by 7.9x against leg 176's true 0.0908 -- outside this
  leg's territory, banked as a stated conflict, direction doesn't change any
  conclusion. PUB1/PUB2 remain unapproved drafts.
- **Leg 217 (Route-PCR) — repaired all 4 named mechanisms, gate NO overall,
  ESCALATED (parked, not merged):** all four of leg 200's port_certification.py
  mechanisms repair cleanly (5/5 mixed-sign sweeps that silently returned a
  different operator's inverse now raise, vs 18820x error pre-repair; 5/5
  radius-0 certificates rejected; 3/3 integer-rhs cases exact; 6/6 poisoned
  ladders refused), with leg 195's 114/114 clean PORT reproduction bit-identical.
  A lesson-90 control leg 200's own battery structurally could not contain
  (all-negative s_rho, not just mixed-sign) confirms the repair: 1186.6 silent
  error pre-repair -> 2.11e-16 post. BUT: two landed artifacts OUTSIDE this leg's
  territory (test_port_certification_regression.py, a banked JSON row) still
  assert the pre-repair accept on the exact degenerate input leg 200 flagged, and
  3 more silent paths survive outside the 4 named mechanisms. Module not
  fully closed; a post-repair verification leg is owed once these are addressed.
- **Leg 239 (Route-USC3) — MIXED (per-obstruction, not averaged):** arXiv:2511.22819's
  three new obstructions characterized. N1 TECHNIQUE-specific (precision: 6.0
  decades residual-to-lambda at IPM's 4th unstable, 1.570 vs stated 2.0
  decades/mode, recurring in 3 model classes incl. non-fluid Gross-Pitaevskii
  vortices). N2 MODEL-specific (the paper itself names 2D incompressible porous
  media at l.278-280 as the alternative class, existence conditional, frontier 0
  modes on CCF vs +1 on IPM). N3 TECHNIQUE-specific (infrastructure: double-float
  floor named in 5 settings across 4 classes, extended-precision/quadruple/
  float64 all return 0 hits in 27pp). Escalation correctly did NOT fire: the
  named class (2D IPM) matches only 1 solver file (a bibliography line, not a
  model), against positive controls of 12 (Boussinesq) and 33 (gCLM) hits for
  the same test -- a control that demonstrably could have fired and didn't.
- **Leg 216 (Route-CGF) — mostly repaired, gate NO overall, ESCALATED (parked, not
  merged):** 13 of leg 199's remaining 15 silent-accept gaps in
  certificate_guards.py now correctly reject (M3 3/3, M2 4/5, M4 1/1, M5 4/5, M7
  1/1), 43/43 live call-site values bit-identical at 0 ULP, 17/17 controls pass.
  2 survivors correctly left unforced: D1b's accept lives outside this leg's
  territory (nk_bounds.py:225); B_nonreal_Fraction can't be closed without
  breaking leg 199's own M4 discrimination control (Fraction IS numbers.Real).
  ONE MORE BANKED NUMBER MOVES outside this leg's territory: a root regression
  test's raised_loudly count goes 5->7 (0 false_closes either side) -- needs a
  leg that owns that file. **PROCESS GAP FOUND: scripts/merge_gate.sh does not
  actually test certificate_guards.py** -- it maps solver/<name>.py to
  test_<name>.py, and test_certificate_guards.py does not exist, so the file
  three certified pipelines delegate their accept/reject decision to has never
  been in the merge gate's own always-run set.
- **Leg 230 (Route-TNRV) — YES on both clauses:** independently confirms leg 220's
  target_norm.py repair with a DECISIVE new test case leg 220 never ran
  (wide_asymmetric, X in [-41000, 745.2]): the pre-repair window falsely reports
  0 outside where 7 samples truly escape, worst pre-repair undercount 9463
  (677x). Also re-solved leg 55's margins from scratch (n=801, two bordered
  Newton solves): all FOUR classes bit-identical to leg 220's quoted two, and
  the other two (s=0.39, s=1) confirmed for the first time. Own harness caught
  itself: a first draft's control predicate was wrong (a symmetric grid need
  NOT report 0 outside), corrected before it could produce a spurious NO.
- **Leg 240 (Route-CNS2) — NO, thorough negative, no escalation:** arXiv:2208.09445's
  author group has 2 later works on the object, both read at full text, neither
  encloses the viscous term. The published follow-up (2310.05325, Cambridge J.
  Math.) imports its profile as the nu=0 system and admits viscosity by the SAME
  scalar inequality the parent used 14 months earlier (agreement 1.78e-15 over a
  39x19 grid). Strong control: a DIFFERENT author group (Shao-Wei-Wang-Zhang
  2501.15701) reaches the identical theorem with 0 interval-arithmetic
  occurrences -- domination is how this literature transfers an Euler profile to
  NS, not an artifact of the computer-assisted method. Leg 174's Grade-A/fluid
  cell stays EMPTY.
- **Leg 241 (Route-PCRC) — (a) INCOMPLETE, (b) CHARACTERISED, ESCALATED (parked,
  not merged):** correction for the stale port_certification.py artifacts is
  authored and verified against leg 217's parked blob but deliberately NOT
  applied -- applying it now would fail the merge gate against main (leg 217
  hasn't landed), and the bank turns out stale in FIVE rows, not the one leg 217
  named. All 3 residual silent paths characterized: leading_order_solve is
  sign-blind in c_l (26.02 on leg 200's fixture, 7.42e+18 at the live 200-node
  resolution, control <=1.6e-14); stall_verdict's positional read FLIPS
  Route-L's own headline verdict at 94.56x (9.72 bending -> 0.10 flat); pack/
  unpack layout-dependence at 1.32/1.42. None claim-adjacent, but two of the
  three have margin exactly 0.0 -- correct only by a hardcoded literal and a
  caller convention, nothing enforcing either. Ready-to-apply correction banked
  for leg 217's own eventual landing commit.
- **Leg 218 (Route-BHR) — YES on both clauses, LANDED:** repairs this cycle's
  single highest-blast-radius latent defect (leg 198's negative-border-weight
  acceptance in bordered_hl.py). Corrected the dispatch's own caller-set premise
  (legs 54/58/127 don't import this module; real live callers are port_v1/v2,
  l1_v1, l1rh_v1) and leg 198's own predicate ("zero weights are rejected" is
  false at the mechanism site -- it's a silent +inf, not a ZeroDivisionError).
  Adopted predicate np.all(isfinite(w) & (w>0)). Found a NEW in-kind extension:
  +inf weights silently understate a norm by 33.7x. ONE CORRECTION TO LEG 198's
  DIAGNOSTIC, NOT ITS VERDICT: the two Z_1 ratios don't reproduce exactly
  (2.287e8 vs 1.198e9, 5.24x; 1.505e12 vs 2.651e12, 1.76x) because Z_1 sits at
  the round-off floor (lesson 86) -- the verdict is robust, the ratio is
  environment-dependent. 0 banked numbers at risk.
- **Leg 227 (Route-EGMT) — YES, LANDED:** the tense-fix for leg 213's cosmetic
  finding. EGM_PRIMARY_READ's sign_correction_leg_190 field now records leg
  214's repair instead of asserting an outstanding defect. Diff is 5
  deletions/11 insertions inside one string literal, every sibling field
  byte-for-byte unchanged, 0 banked numbers/verdicts move.
- **Leg 242 (Route-DFL2) — NO on both clauses, thorough negative:** Dahne &
  Figueras have 0 joint works since arXiv:2410.05480 itself (still v2,
  unpublished, "Submitted" 668 days on). 7 subsequent works on the author line,
  2 genuine interval-arithmetic CAPs but on Almost Mathieu spectral gaps and
  polygon Dirichlet eigenvalues -- 0/7 fluid-adjacent, 0/7 blow-up. One
  candidate (Figueras-Gimeno-Parker, a fluid dynamicist coauthor) disqualifies
  itself in its own text ("this paper does not include a computer-assisted
  proof"). Live-probe control fires correctly (0 fluid/blow-up terms vs 15
  interval-arithmetic hits over the same 6656 lines). Leg 174's
  (fluid-adjacent, Grade A) occupancy cell stays EMPTY.
- **Leg 243 (Route-PCRS) — YES, CLOSES THE CONCERN:** independently confirms
  Route-L's published headline verdict is genuinely UNAFFECTED by leg 241's
  stall_verdict positional-read finding -- not a second leg-202/226 exposure.
  Found two additional holes in leg 241's own claim-adjacency evidence worth a
  follow-up: line 49 doesn't cover the deep rung's own dims=(240,320) literal,
  and L1_attribution's six further ladders reach stall_verdict through
  attribution_summary and were never audited.
- **Leg 237 (Route-SIRC) — YES, latent, not claim-adjacent:**
  collocation_newton.py's ACollocation.newton/continuation are a SECOND
  instance of leg 202's scale-invariant-residual defect class -- rel flat to
  8.725e-14 while c spans 1.000e+06x, verdict True on a member with gauge
  defect 999.0 and c wrong by 1000x. But GRADED LATENT: 0 escapes in 41 cases
  across 6 trial routes (vs 2/2 escapes reproducing leg 202's own banked M2 to
  the digit, confirming this is a measured contrast, not a null), and 0 of 14
  call sites sit in claim-bearing runners (Route-D's real consumer calls the
  sibling newton_gauged, which leg 150 already repaired). Census of 47 solver
  files / 20 verdict sites found no other instances. Own discipline caught a
  would-be false positive before it shipped (a criterion discovered mid-pass,
  and an initial probe that would have read as a hit without the reachability
  battery).
- **Leg 235 (Route-CDAP) — YES, ESCALATED (parked, not merged), DIRECTLY BEARS
  ON ROUTE-D v11 AGAIN:** a SECOND instance of the ignored-caller-diagnostic
  shape, in the SAME runner leg 202 escalated but a DIFFERENT mechanism (min/max
  selection, not a bad convergence flag) -- leg 226's dispatched repair does not
  touch it. Route-D v11's v5_budget headline margin (1.0468e+10) is built from
  newton_weighted_defect_min while newton_weighted_defect_max = 1.5196e-02 sits
  one line away in the same dict, never compared -- violates that block's own
  Y0 budget by 62.02x at a=0.45. 0 instances found in the other 195 banked
  JSONs (4,320 verdicts screened, 190 hits all adjudicated by hand). CORRECTS
  LEG 202: 2 of its 3 quoted weighted_defect magnitudes (4788, 73372) attach to
  rows already marked grid_converged=false -- the correctly-scoped form is 17
  rows all converged=true spanning 13.42 decades, shape confirmed, two
  magnitudes on the wrong rows.
- **Leg 244 (Route-PCRO) — YES, LANDED:** stall_verdict now keys its two rows
  on m (the ladder's own parameter) rather than array position, closing leg
  243's flagged fragility. 1682 permutations across 15 banked ladders (11
  Route-L + 4 Route-K) now return ONE verdict each (worst ratio exactly 1.0,
  vs up to 3795.25x pre-repair spread); all 10 published quantities including
  Route-L's own headline gain (9.724454) reproduce bit-identical at difference
  exactly 0.0. Deep rung's dims=(240,320) literal (line 180, never covered by
  leg 241's line-49 literal) now closed too. Methodological finding worth
  keeping: a MIS-KEYED repair (keying on k instead of m) PASSES the permutation
  battery -- order-immunity alone is necessary but not sufficient, only the
  preservation check catches it.
- **Leg 245 (Route-BCL2) — NO, but relevant to the user's new Clay-directed
  goal:** arXiv:2404.04054's authors (pinned for the first time in this repo:
  Maxime Breden, Hugo Chu -- the ledger's own who field was a description, not
  an attribution) published 7 papers in 28 months, 0 on a fluid model. THE
  SHARPER FIND: the parent's own Remark 40 states the Navier-Stokes
  nonlinearity (u.grad)u is reachable "in principle" by their Grade-A
  machinery in d in {2,3} -- while the group's newest paper still calls a
  higher-dimensional RECTANGLE "future work". Two near-misses on record:
  Breden's 2019 3D NS CAP (periodic orbit, not blow-up) and Cadiot-Haziot's
  vorticity-bearing water waves (inviscid, no viscous term). Directly relevant
  to Phase 1 (the viscous rung) under the user's new exit-criterion ruling --
  this group's own stated reachability claim is worth a full-text follow-up
  before any Phase-1 leg builds machinery from scratch.
- **Leg 246 (Route-ALSL2) — NO:** arXiv:2207.07548's authors (Ambrose,
  Lushnikov, Siegel, Silantyev) have no certificate at any dissipation
  exponent -- 19 subsequent works over 1483 days, 2 on the object, both read
  at md5-pinned full text (4336 lines), 0 with a certification-apparatus
  term. Their own published follow-up (Stud. Appl. Math. 155, e70115, 2025)
  is exact pole dynamics at sigma in {0,1} only, and states a verbatim defeat
  at gamma=2: "despite significant effort, we have been unable to generalize
  this solution to the periodic domain." Cross-check found au:"Ambrose_D"
  misses arXiv:2504.14346 -- the closest candidate to this repo's own gamma=2
  object -- recurring under-return failure mode (legs 240/242) on a third
  author-net query form.
- **MAJOR PLAN CHANGE, 2026-08-06.** Per the user's direct ruling (forwarded
  verbatim by the orchestrator to the DM, processed in full): PUB1 and PUB2
  are APPROVED as the project's deliverable (two submission-blocking legs
  drafted: 249 independently verifies leg 176's certificate, 250 fixes the
  leg 163/176 sigma_min citation conflict). THE EXIT CRITERION IS CHANGED TO
  A FULL CLAY SOLVE, superseding "a novel Tier-3 result, NOT Clay" -- this
  resolves escalation #1 (stage B's exhaustion). plan_of_record.py: B marked
  DONE, new stage P0 (target selection under Clay, screened by NRS/Tsai's
  exclusion of exactly-backward-self-similar 3D NS blow-up) is NEXT. Wall 2
  corrected per leg 172: the barrier is TIME-DEPENDENT singularity formation,
  not spatial dimension. Stage V's ban re-posed (its "needs L1 first" lift
  condition had become unliftable, L1 dead in 3 realizations); DSS ban kept
  unchanged. Programme sequenced Phase 0 (leg 251, target selection) -> Phase
  1 (viscous rung, no certified viscous blow-up exists in ANY model, any
  dimension) -> Phase 2 (3D solver, user-authorized, unscheduled until Phase
  1 reports). Clay odds UNCHANGED at ~0.05%, recorded in the same breath as
  the goal change -- the evidentiary bar does not lower.
- **Leg 247 (Route-VBR) — repair correct, gate NO, ESCALATED (parked, not
  merged):** leg 235's diagnosed fix for Route-D v11's v5_budget lands
  correctly -- the corrected margin moves from a fabricated 1.0468e+10 to the
  true worst-case 1.6123e-02, which IS a violation: the block misses its own
  Y0 budget by 62.0237x at a=0.45 (1 of 11 rows; the other 10 hold, worst
  10.656x). Re-solved from scratch, reproduces to 0.82%. 0 of 196 other banked
  JSONs affected (grown corpus, still isolated). REASSURING: Route-D v11's
  own PROSE already stated the non-uniformity honestly (TECHNICAL/blog both
  print 1.5e-2 and say "not uniformly under the budget") -- no written
  conclusion moves. Residue: the banked anchor JSON itself still carries the
  wrong 1.0468e+10 margin, outside this leg's territory -- needs a follow-up
  leg to regenerate it.
