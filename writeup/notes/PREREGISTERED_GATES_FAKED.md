# Five pre-registered gates, five fakes

**What happened when we pointed a blind adversary at our own evidence — and found the
holes were in the pre-registration, not in the runs.**

Andy · 2026-09-10 · [ravanova/blowup-search](https://github.com/ravanova/blowup-search)
Full record: [`experiments/journal/leg_439.md`](../../experiments/journal/leg_439.md) ·
[`writeup/CORRECTIONS.md` §79](../CORRECTIONS.md) · data
[`writeup/data/arc7/k3/`](../data/arc7/k3/) · CC BY 4.0

---

## The one-paragraph version

We were checking a numerical construction with AI agents. To stop the agents from grading
their own homework, we pre-registered five falsifiable numerical gates — each a **two-route
agreement on a quantity the adversary cannot choose** — pushed them to a public branch before
any run, and dispatched five agents in isolation: four to run the gates, one *blind adversary*
whose only job was to make each gate say `YES` from a run it knew to be wrong. **The adversary
faked all five.** Every one, with a recipe and numbers. Separately, we found that one gate had
never had two routes at all: both its "independent" routes were the same closed form evaluated
twice. Net evidence produced by a wave designed entirely around producing evidence: **zero.**
The three defects that made this possible were all in **the pre-registration**, written by the
same agent that designed the wave.

## What this is not

Read this before quoting it.

- **This is not a finding that the mathematics is wrong.** Nothing here shows any of the five
  claims is false. A `FAKEABLE` verdict says the gate *as pre-registered* admits a run known to
  be wrong, so a `YES` from it is not evidence **on its own**. That is a statement about the
  instrument, not the object.
- **This is not a peer-reviewed result.** One operator, one session, Tier 2 by our own ladder.
  Every claim below is `UNVERIFIED` in the sense this repository uses: produced once, not
  independently reproduced.
- **The adversary is itself an AI agent**, and its verdicts are *recorded, not adjudicated*. The
  load-bearing exception: two of its recipes were independently reproduced by hand before being
  written down (marked ✔ below). Those two are the ones to trust.
- **The construction being checked is not ours.** We were auditing someone else's manuscript.
  We take no position on its correctness or on the priority dispute around it.

## The setup

**The rule**, fixed in advance and applied without exception: *evidence is a two-route agreement
on a quantity the adversary cannot choose.* Route A is what the paper predicts. Route B must
measure the same quantity by different machinery. **A gate that cannot be put in two-route form
is DROPPED, not weakened** — no partial credit, no substitute offered.

**The isolation.** Five agents, five separate worktree branches, one artefact each in a fixed
JSON schema. The adversary never saw the workers' files or methods; the workers never saw the
adversary's; no agent saw the previous wave's results. Each artefact had to carry a `claimed`
block — **the route-A prediction written down before the run** — plus its gates with numbers,
its planted controls, and an explicit list of what it could not determine.

**The gates.** `Q1` a realised stress, closed form vs direct quadrature. `Q2` a hierarchy
exponent `2h`. `Q3` a per-stage gain `h/10`. `Q4` a leading-order force, physical space vs
profile space. `Q5` a bracket `ℬ`'s exact zero with a heat factor against `−(2+2h)` without.
(A sixth was dropped by amendment before any run.)

## The result

| gate | what the worker got | adversary | integrated |
|---|---|---|---|
| `Q1` realised stress | `YES` — sup-err `1.71e-14` / `1.54e-14` at `M=256` against a `1e-8` gate, log–log slopes `−10.54` / `−10.58` | `FAKEABLE` | **NOT EVIDENCE** |
| `Q2` hierarchy `2h` | `UNDER-RESOURCED` — cost stated, not faked | `FAKEABLE` | **NOT ESTABLISHED** (not a `NO`) |
| `Q3` per-stage gain | `NOT-INSTANTIATED` — twin gains `~1e-14`, `h`-scaling `false` | `FAKEABLE` | **DROPPED by the rule** |
| `Q4` leading-order force | 4 cells `NO`, 3 `YES` of 8 | `FAKEABLE` | 4 `NO`; the `YES` cells **NOT EVIDENCE** |
| `Q5` `ℬ`'s exact zero | `YES` — `abs_error` **exactly `0.0`** in all four cells | `FAKEABLE` | **NOT EVIDENCE** |

`live_gates` **5** · `EVIDENCE` **0** · `gates_the_blind_adversary_faked` **5**.

Note `Q1`: a worker passed a `1e-8` gate by six orders of magnitude, with a convergence slope
three times steeper than required. It looks like the strongest result in the wave. It is not
evidence.

## How each one was faked

- **`Q1`, two ways.** Feed *both* routes the same wrong amplitude field: the identity being
  tested is algebraic in the amplitudes, so it holds for any assignment — relative error
  `3.5e-16`. ✔ **And** contaminate route B at Fourier harmonic 256: because `256/M` is an
  integer for every oversampling `M ∈ {16, 64, 256}`, `sin(256θ)` evaluates to `1.7e-13` **at
  every quadrature node**. A contaminant contributing `0.18` — **31% of a typical entry of
  `0.577`** — is invisible to a check whose whole purpose was catching aliasing. *(Reproduced
  by hand: exact.)*
- **`Q2`.** ✔ Assert `R(q) = 4.2·q^{2h}` and fit the slope. Nothing is solved, no profile is
  read, `h` enters as an input exponent — and the fit recovers `2h` to relative `1.3e-15`.
  *(Reproduced by hand: exact.)*
- **`Q3`.** Perform a real, honest tridiagonal solve — **of the wrong problem** — carrying `h`
  in an operator weight. The gate reads the exponent gain and never asks which problem was
  solved. Both planted controls fire correctly.
- **`Q4`.** A Gaussian stand-in stress. The exponent `−(3/2 + h)` is prefactor bookkeeping that
  *any* profile reproduces, and the pointwise leg compares two differentiations of the **same**
  field, so a wrong field passes.
- **`Q5`.** The pinned builder with the density `170×` wrong and the wrong cutoff. `ℬ` beyond
  the cut is the construction's own constant `(2+2h)(s_h − 1)` — it cannot see the density, the
  cutoff shape, or the normalisation.

**The adversary's own summary is the general statement, and it is the part worth keeping:**

> Every one of the five gates tests an algebraic **relation** that a **family** of objects
> satisfies, and pins the **object** only through route A's prediction — which is exactly what
> the adversary is free to choose.

## The three defects, all in the pre-registration

The uncomfortable half. These were written by the same agent that designed the wave, pushed
before any run, and found only by running it.

**(a) `Q5` had no second route.** Route B was specified as "numerical, from the pinned fields".
As implemented it read a function that computes

```python
sh = 1.0 if heat else 0.0
calB_beyond = (2 + 2 * h) * (sh - 1.0)
```

— algebra in a float and a boolean, reading no field, no profile, no quadrature. Route A was
the same algebra. The two "independent" routes were one closed form evaluated twice. Confirmed
directly: bit-identical at three values of `h`, and **invariant under every profile variation
tried** (four different perturbations, one value `−2.002` across all of them). The blind
adversary reached the same conclusion independently.

**(b) The second scale violated the construction's own hypotheses.** The paper's scale makes the
signal unresolvable, so the pre-registration fixed a computable second scale `h = 10⁻³` — and
never checked it was *admissible*. The construction requires `h < min{1/100, λ, e^{−T_d}}` with
`e^{−T_d} = 3.0·10⁻⁶`. The builder raises an `AssertionError` at `h = 10⁻³`. The scale check
asked whether the scale was **resolvable**; it never asked whether it was **allowed**. Two
workers noticed unaided and said so in their artefacts. They were honest; the instruction was
wrong.

**(c) `Q2` cited a table that does not contain the quantity.** The worker read the cited
proposition's own table and found every entry `≤ 1` — **no `q^{2h}` term at all**. It reported
this as a defect of the citation and did *not* quietly re-scope its own gate. The gate's number
and tolerance, fixed before the run, were unchanged; only the citation was wrong.

## Three diagnostics worth stealing

Transferable to anyone building automated checks, in or out of mathematics.

1. **An error of exactly `0.0`, rather than `~1e-16`, is the fingerprint of one closed form
   evaluated twice.** Two genuinely independent numerical routes to the same quantity disagree
   at roundoff. Perfect agreement is not the best possible outcome — it is a symptom. We now
   treat exact zero as a failure to be explained, not a pass.
2. **A quantity that does not move when the input is replaced measures nothing about the
   input.** Perturb the object your check is supposed to be reading. If the number is invariant,
   the check is not reading it. This is cheap, and it caught (a) directly.
3. **A pre-run scale check must ask three things per gate, not one:** is the quantity
   *resolvable*; is the scale *admissible to the construction's own hypotheses*; and does route
   B *read anything the object determines*? Our check asked only the first, which is why (a) and
   (b) both survived to the run.

## What we would do differently

- **Have the adversary attack the pre-registration, before the workers are dispatched** — not
  the runs, after. Four of the five fakes are visible in the gate definitions alone; the runs
  were never the weak point.
- **Require every route B to name a quantity of the object it reads**, and demonstrate the
  number moves when that quantity is perturbed. Had this been a schema field, (a) could not have
  been written.
- **Keep the "DROPPED, not weakened" rule.** It cost us gates and produced an embarrassing
  zero, and it is the only reason the zero is trustworthy. A rule that never costs anything is
  not being applied.
- **Two mechanically different routes, not two evaluations at different resolutions.** One gate
  passed while sharing a frozen fine solution between both routes and differing only in
  quadrature — recorded as a limitation at the time, and precisely the seam the adversary
  exploited.

## Two operational notes

**A planted control did not fire as planted**, and the worker reported it with a full diagnosis
instead of hiding it: a substitution intended to shift an exponent by `−0.1` moved one route by
`−0.2`, because holding one parameter pinned broke the paper's own `A + D = 1` identity. **A
defect of the plant, not of the run.** This is the behaviour the artefact schema was designed to
make easier than concealment.

**Three of five agents were killed mid-run by an API rate limit.** Two had written nothing and
were re-run from scratch; one had a complete artefact that was never committed, rescued from its
worktree and committed **unedited** with its provenance in the commit message. The method changed
in response: workers now commit the pre-run `claimed` block and the artefact **as soon as each is
valid**, so the two re-run agents carry independently timestamped pre-run commits that the
earlier agents do not. If you run agents at fan-out, assume they will die holding results.

## Reproducing this

Everything is banked. The five artefacts and their merge are under
[`writeup/data/arc7/k3/`](../data/arc7/k3/); the pre-registration and its amendment are
[`leg_439_prereg.md`](../../experiments/journal/leg_439_prereg.md) and
[`leg_439_prereg_amend.md`](../../experiments/journal/leg_439_prereg_amend.md), both pushed
before any run and unedited since; the integration is
[`leg_439.md`](../../experiments/journal/leg_439.md); the defects are `CORRECTIONS.md` §79,
recorded *beside* the data — **no banked artefact was edited**.

**If you reproduce any of this and disagree with it, that is the most useful thing you could
do with it.** Open an issue.
