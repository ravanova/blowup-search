# Leg 73 — Route-BV v1: the first EXTERNAL known-answer check for the 2D velocity solve

**Branch** `leg/bv-v1`. **Exploration leg, CLAIM-BEARING** (external validation of shared
infrastructure). **Gate: YES, AND IT REPRODUCES.** Lands normally on `main`.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is NEXT. Two live bans bear on this leg:
   *re-measuring `beta` on the 2D object* (lifted by: never), and *building a solver without
   grepping `capabilities.py` for the object first*. Both were honoured: this leg measures no
   `beta`, and it builds **no** solver — it runs the one that already exists. `capabilities.py`
   grepped first; the entry under test is at line 89.
2. `DIRECTION.md` — leg 73 entry present, read in full. Gate quoted verbatim into the runner
   and the JSON.
3. **Novelty pass FIRST**, committed before any construction (`writeup/novelty/leg_73.md`,
   commit `13d98c1`), seven queries, **links not counts**, tolerances pre-committed in the same
   commit.
4. Then: runner, curated data, this note.

## What the novelty pass changed about the leg

Two things, both load-bearing.

**It ruled out the source the brief named first.** The dispatch said Chen–Hou–Huang's own
validation tables were "the first place to look". Q5 read them and answered **negative**: Part II
publishes rigorous error control on *their* space-time solution in *their* B-spline FEM, keyed to
their profile and their weighted norms. There is no free-standing "given this `omega`, `phi` and
`u` are these numbers" table a different discretisation can be scored against — and the one
number this repository already matches, `beta` to 2.1%, is **banned**. Recording that on the
record, rather than leaving it as an unexamined suggestion, is what freed the leg to go find a
benchmark that actually exists.

**It supplied the pre-commitment's reading rule.** Because the pass established that the scheme
is nominally second order, the tolerances could be split into *accuracy* statements (P1, P3) and
a *correctness* statement (P2, the observed order). Without that split, a tolerance miss from
under-resolution would have been indistinguishable from the gate's "disagrees" branch — and this
leg was instructed to escalate at maximum urgency on "disagrees". The reading rule was fixed
before any number existed, so the outcome could not be re-argued afterwards.

## The benchmark, and why it is external

Nobody has published "Oseen blob in a right-angled corner on a log-polar grid" as a named
benchmark case (Q6, Q7 both returned nothing on-topic; stated as negative). What is published,
and what this leg assembles, is two closed forms:

* **Lamb–Oseen** — prescribed Gaussian vorticity, published velocity
  `v_theta = (Gamma/2 pi R)(1 - exp(-R^2/d^2))`. The standard first verification case for
  Biot–Savart/Poisson solvers (five independent uses located in Q1).
* **The classical corner image system** — Lamb, *Hydrodynamics* Art. 155; Greenhill 1878;
  restated peer-reviewed in Crosby–Johnson–Morrison, *Phys. Fluids* 25 (2013) sec. IV eq. (14),
  which states the quarter-plane three-image construction verbatim.

Three reasons this is not another manufactured solution, each falsifiable:

* **The vorticity is prescribed and `phi` is the consequence.** A manufactured solution runs the
  other way — pick `phi`, differentiate to get `omega`. That is exactly what `capabilities.py`
  already claims, and exactly what this does not do.
* **The target number is not ours, and it is a pure boundary-condition quantity.** The velocity
  at the vortex centre is a *difference of image contributions*: the blob's own field vanishes
  there by radial symmetry, so everything that remains exists only because of the two Dirichlet
  rays. A manufactured solution handed its own Dirichlet data cannot test this.
* **It was verified to be Lamb's closed form, not a lookalike.** The point-vortex image velocity
  was checked against Lamb's corner-orbit invariant `d/dt(a^-2 + b^-2) = 0`; residual
  **−1.67e-16**, i.e. round-off.

The instrument was validated before use: the hand-rolled `E_1` (this repository ships no scipy)
agrees with published tabulated values to **6.86e-14** relative, cross-checked against an
independent Gauss–Laguerre/Gauss–Legendre quadrature that shares no code path with it. Two digits
of the reference table were mistyped on first writing and were caught by that cross-check — the
reason the check is dual and not a single typed table.

## What was measured

Ladder `(n_r, n_beta) = (601,49), (1201,99), (2401,199)`, `r in [1e-3, 1e3]`, blob at `r = 1`,
`beta = 0.7·(pi/2)`, core `d = 0.25`, `Gamma = 1`, `radial_bc="robin"`. The blob centre lands on
a grid node **exactly** at every level (`node_offset` `0.0` in both `rho` and `beta`), so no
interpolation enters the headline read.

**P1 — velocity at the vortex centre vs the published corner-image closed form.**
`2.815e-3 -> 7.034e-4 -> 1.758e-4`. Finest **1.758e-4** against a pre-committed **1e-2**: inside
by a factor of **57**. Componentwise at the finest level, numeric `(-0.0183853, 0.1391466)`
against the closed form `(-0.0184078, 0.1391567)`.

**P2 — observed order `2.0007` then `2.0002` on P1, `2.0011` then `2.0003` on P3.** Monotone in
both. This is the correctness statement, and it is the sharpest single result here: the solver
converges *at its design order* to *someone else's answer*.

**P3 — relative L2 of `phi` over `r in [0.1, 10]`.** `1.948e-4 -> 4.866e-5 -> 1.216e-5`. Finest
**1.216e-5** against a pre-committed **1e-3**: inside by a factor of **82**.

**The finite-core correction is 2.332e-6 relative** — the gap between the finite-`d` Oseen ground
truth and the textbook point-vortex formula. It sits *below* the resolved error, so the honest
statement is that the module reproduces the **textbook point-vortex corner formula to 1.76e-4
relative**, and the finite-core refinement is not yet resolved at this ladder.

## The far-field closure: the number worth carrying forward

The `"dirichlet"` control — handed the exact answer at both radial ends — reproduced the
`"robin"` ladder to every printed digit. That is a measurement, not a coincidence, and it was
converted into a magnitude rather than reported as "identical": at `r_max = 1e3` the two closures
separate by **2.1e-15 to 1.5e-13** in P1, i.e. at machine level. The domain is simply too large
for the closure to bind.

So block A does **not** stress the `r^{-2n}` Robin modelling. Block D shrinks the domain until it
does, at fixed `(1201, 99)`:

| domain | robin P3 | exact-Dirichlet P3 |
|---|---|---|
| `r in [0.2, 5]` | **2.596e-5** | **2.652e-6** |
| `r in [0.05, 20]` | 9.225e-6 | 9.151e-6 |
| `r in [0.01, 100]` | 2.163e-5 | 2.163e-5 |
| `r in [0.001, 1000]` | 4.867e-5 | 4.867e-5 |

At a truncation radius only **5×** the blob radius the Robin closure carries its own error of
about **2.3e-5** in relative L2 on `phi` — a factor **9.8** above what exact far-field data
achieves on the same grid. By `r_max = 20` the closure error has dropped below the discretisation
error and the two are indistinguishable. (The apparent *growth* down the column is `Delta rho`
growing at fixed `n_r` over a wider log range — pure discretisation, not closure.) Note also that
the closure error does **not** reach the vortex: P1 at `r in [0.2, 5]` is `3.965e-5` robin vs
`3.818e-5` exact-Dirichlet.

**The usable rule for every route importing this module: keep `r_max` at least ~20× the support
radius of `omega` and the `r^{-2n}` closure costs nothing measurable; at ~5× it costs ~2e-5.**

## What was deliberately NOT done

* `solver/boussinesq_velocity.py` was **not** modified. Read-only, as instructed, under every
  gate outcome.
* `capabilities.py`'s `validated` line was **not** edited — outside territory. It should now
  read that the module additionally reproduces the classical Lamb corner-image velocity to
  1.76e-4 relative at second order; that is a follow-up for whoever owns that file.
* No `beta` was measured, and no 2D-object convergence claim is made or implied.
* No figure. The result is a convergence ladder of three numbers and one closure table; a plot
  would dilute rather than clarify.

## Lesson offered

Leg 69's lesson was *a validation claim without a stated range of validity is not auditable*.
This leg adds the companion: **a validation claim without a stated *direction* is not auditable
either.** `capabilities.py` said "manufactured stream-function solutions", which sounds like
evidence and reads like coverage — but manufactured solutions run `phi -> omega`, and every
consumer of this module runs `omega -> u`. The module had never once been asked the question its
callers actually ask. It answers it correctly, at second order, against Lamb — but that was not
known until today, and nothing in the `validated` line would have revealed the gap.
