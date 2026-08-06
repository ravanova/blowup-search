# Leg 0 (BENCH) — novelty pass: the two RED tests on `main`

**Branch.** `bench/fix-red-tests-g6-newton`. **Merge base.** `4975ea0`.
**Date.** 2026-08-06. **Claim-bearing** (both items touch a gate answer and numbers in prose).

Repo-wide bench work, so no leg number. The novelty pass still comes first and is
committed in its own commit, ahead of any probe script and ahead of any edit to
`solver/` or to either test — so that whatever the probes return cannot be read back
as having been fitted to a conclusion chosen in advance.

There is no external literature to pre-empt here (this is a self-audit of two of the
repo's own gates), so the job of this file is the same one `writeup/novelty/leg_71.md`
gave itself: **pin the claim, the alternatives, and the discriminating measurement in
writing before the instrument is pointed at them.**

---

## 0. What is claimed, by whom, and what I have already reproduced

`reports/ORCH_STATE.md` resume-checklist item 0 (from leg 71, landed `e742f6d`) says
two tests are RED on `main`, and marks fixing them TOP PRIORITY:

| test | leg 71's measurement | my measurement at `4975ea0` |
|---|---|---|
| `test_fractional_boussinesq.py` G6 | `[FAIL] p > 0 at s=0.10` — **p = -0.211** | `[FAIL]` — **p = -0.211** (bit-identical) |
| `test_profile_newton.py` item (6) | `AssertionError`: a=0.9 `converged=True`, residual_rms **3.881e-07**, relres **2.889e-06**, 40 iters | **PASSES**: a=0.9 `converged=False`, relres **1.6e-04** |

So item (a) reproduces exactly and item (b) does not reproduce at all. Both facts are
recorded here before the explanation is looked for.

`capabilities.py` was grepped first, per the standing ban ("no solver work without
grepping `capabilities.py` for the object"). Row 12 (line 132) cites
`solver/fractional_boussinesq.py` → "the critical-dissipation exponent for the 2D
object", validated "consistency with the 1D critical exponent; ... stored
s_c=0.1711999849 remains internally-consistent-only". Row 29 (line 277) cites
`solver/profile_newton.py` → "Newton on the two-scale profile equation", validated
"converges to the known a=0 two-scale profile; residual falls to the Newton floor".
Neither `validated` field mentions the two quantities that are actually in dispute
(the *sign* of p at s=0.10; *non*-convergence at a=0.9).

## 1. First structural fact, established before any probe: nothing changed

`git log --full-history` on all four files, over the full (un-shallowed, 405-commit)
history:

- `test_profile_newton.py` — **one** commit ever: `6a17ce6` (Route-D v11).
- `solver/profile_newton.py` — **one** commit ever: `6a17ce6`.
- `solver/gclm_family.py` (profile_newton's only repo dependency) — last touched at
  `44a507c`, far upstream of `6a17ce6`.
- `test_fractional_boussinesq.py` — one commit, `053ecbe`.
- `solver/fractional_boussinesq.py` — last touched at `59a9222` (Route-G v1).

`git log e742f6d..HEAD` (leg 71's audit commit to my merge base) over those paths plus
`solver/boussinesq.py` returns exactly two commits, and **neither touches any file
either test imports** except `cd91c5d` (boussinesq.py silent-corruption repair, 19 of
82 gate-deciding cases → 0) — which is a shared dependency of `fractional_boussinesq.py`
and must therefore be checked, but which cannot explain `profile_newton` (not in its
import graph) and which is *already excluded* for G6 by the fact that p = -0.211 is
bit-identical before and after it landed.

**Consequence, stated now:** *neither red can be a code regression.* No hypothesis of
the form "solver X broke" survives the history. That closes off one third of the
chartered question before a single number is measured, and it means the answer for
each test is either (i) a stale/mis-specified test expectation, (ii) a genuine
numerical boundary effect the threshold does not account for, or (iii) an environmental
non-determinism. Those are the three live branches below.

## 2. Item (a) — G6, `p > 0 at s=0.10`

### The instrument

`gate6_relevance_sign()` runs `FractionalBoussinesq(n=192, nu=1e-3, s)` at s ∈ {0.10,
1.00}, takes `fit_relevance(r, estimate_T(r))["p"]`, and asserts three things:

1. `p > 0 at s=0.10` — **RED**, p = -0.211
2. `p < 0 at s=1.00` — green, p = -3.486
3. `p decreases with s` — green, -0.211 → -3.486

The prediction the module derives is the line `p(s) = 1 - 2 β s` with β the collapse
exponent (`relevance_exponent`, and independently `relevance_exponent_buoyancy`).

### Arithmetic done in advance, so the probe cannot be aimed

Inverting the measured p's for the effective β the instrument is *implying*:

- s = 1.00, p = -3.486  ⟹  β_eff = (1 − p)/(2s) = **2.243**
- s = 0.10, p = -0.211  ⟹  β_eff = (1 − p)/(2s) = **6.055**

The same run family's *geometric* β, measured by G5 on `Lgrad` over three sub-windows,
is **[1.79, 2.079, 0.823]**. So the s = 1.00 endpoint sits inside the geometric range
and the s = 0.10 endpoint is **2.7× above its top**. The gate's threshold `p > 0` at
s = 0.10 requires β < 5; the object's own measured β is ≈ 2.

### Pre-registered hypotheses, ranked, with the discriminator for each

- **H1 (leading) — the gate asserts the one quantity the module says is not robust.**
  `fit_relevance`'s own docstring: *"THE WINDOW IS THE DOMINANT SYSTEMATIC AND IS SWEPT,
  NOT CHOSEN (Route-F F7). ... The SLOPE of p against s is much more robust than any
  single p ... which is why the claims are about the slope and the zero crossing, with
  the window sweep quoted as the error bar."* G6 calls `fit_relevance` at its **default
  single window (0.40, 0.94)** and then asserts an **absolute sign of a single p**. If
  H1 holds, sweeping `(lo, hi)` will move `p(s=0.10)` across zero while leaving the two
  green claims (sign at s=1.00, and the slope/ordering) invariant.
  *Discriminator:* window sweep. **Predicted signature: sign flip at s=0.10, no sign
  flip at s=1.00, slope stable.** Recorded before running.
- **H2 — the s = 0.10 run is pre-asymptotic in a way the s = 1.00 run is not.**
  `p = 1 − 2βs` is asymptotic. At s = 0.10 the symbol is |k|^0.2, which over this grid's
  wavenumber range varies by only ~2.3×, i.e. the dissipation is nearly *scale-blind* and
  the term it damps has not yet separated from the transient. *Discriminator:* the fit
  residual `fit_rms` and the drift of p across successive sub-windows at s=0.10 vs
  s=1.00.
- **H3 — the two runs are not the same length, so the two p's are not comparable.**
  G6 passes `wall_max=240.0`: the run can terminate on **wall-clock**. A machine-speed
  dependent termination would make the fit window machine dependent. *Discriminator:*
  record `outcome`, `steps`, sample count and `wall_seconds` for both runs; and re-run
  with `wall_max` raised.
- **H4 — G5's refusal already covers G6.** G5 asserts, and passes, that
  `collapse_window_report` **REFUSES** on this object (0.78 decades of (T−t), need 1.5;
  β moves 80% across sub-windows, allow 25%). If the object is not entitled to quote β,
  it is not entitled to quote `1 − 2βs` either — and G6 asserts a *sign* of exactly that.
  *Discriminator:* run `collapse_window_report` on the two G6 runs specifically (G5 runs
  a different configuration) and check it refuses there too.
- **H5 (must be excluded, not assumed) — a real defect in the D/N instrument**, e.g.
  the peak-index advection term not vanishing at n=192, or the ratio's denominator
  passing near zero. *Discriminator:* |adv|/|buo| at the peak for the G6 runs at both s
  (G4 checks this only for its own configuration), and the minimum of |drv| along the
  fit window.

**Pre-committed edit discipline for G6.** If H1/H2/H4 hold, the repair is to make the
gate assert what the module says is measurable (the slope / the sign change *between*
the two s, and/or the sign at s=0.10 under an explicit window sweep with the systematic
quoted), **not** to relax `p > 0` to `p > -0.3` and not to flip the assertion. If H5
holds, the repair is in `solver/fractional_boussinesq.py` and every other G-gate plus
every banked consumer must be re-run bit-for-bit.
**A repair that changes any number in `writeup/data/p2_route_g_v1_collapse.json` or
`p2_route_fd_v1_lit.json` is out of scope and escalates.**

## 3. Item (b) — `test_profile_newton.py` item (6)

### The disagreement is real and is in leg 71's own captured evidence

`writeup/data/p2_route_cap_v1_audit.json` stores leg 71's full stdout/stderr. It is not
a transcription error: the traceback carries
`{'a': 0.9, 'converged': True, 'residual_rms': 3.880940112012514e-07,
'relres': 2.8888943409112577e-06, 'c': 0.7483299284679625, 'iterations': 40}`.
That run's filesystem path is `/home/andy/projects/Unsolved/.claude/worktrees/
agent-a336c9a759d91444f/` — **a different host from mine** (`/home/user/blowup-search/`).

And **every** number in the other five items differs between leg 71's run and mine, at
the roundoff level:

| item | leg 71 | me | ratio |
|---|---|---|---|
| (1) Newton rms | 1.8e-15 | 2.0e-15 | 1.1× |
| (2) one-gauge direct stall | **8.8e-05** | **1.8e-06** | **49×** |
| (3) last history entries | 1e-15, 1e-15 | 9e-16, 9e-16 | ~1.1× |
| (4) Jacobian vs FD | 6.7e-11 | 6.6e-11 | 1.0× |
| (5) continuation best relres | 5.9e-15 | 7.2e-15 | 1.2× |
| (6) a=0.9 relres | **2.9e-06** | **1.6e-04** | **55×** |

The two entries that differ by ~50× are precisely the two that are **iteration-capped
stalls of a rank-deficient system** (item 2: the deliberately singular one-gauge solve,
40 iterations; item 6: a=0.9, 40 iterations). The four that agree to ~10% are the ones
that reach a genuine quadratic-convergence floor. That pattern is the hypothesis.

### The banked measurement contradicts the gate's premise

`writeup/data/p2_route_d_v11_anchor.json`, `v2_sweep`, n = **801**, a-ladder
0.0/0.05/…/0.55/0.6/0.7/0.8/0.9/1.0, records at **a = 0.9**:

> `{"a": 0.9, "converged": true, "residual_rms": 1.4886e-15, "relres": 1.1051e-14,
> "c": 0.760744125772949, "iterations": 7, "weighted_defect": 1.502e-07}`

i.e. **machine precision in 7 iterations**. The banked science therefore says Newton
*does* converge at a = 0.9 on the two-scale system — the opposite of what the test's
docstring asserts ("(6) FAILURE IS REPORTED. Past the survival boundary Newton does not
converge"). `test_profile_newton.py` item (6) differs from the banked sweep in exactly
two respects: **n = 601 not 801**, and a **4-point continuation ladder**
`[0.0, 0.3, 0.6, 0.9]` instead of a 17-point one.

### Pre-registered hypotheses, ranked, with the discriminator for each

- **H6 (leading) — item (6) is a coin-flip on an absolute threshold.** `solve()` returns
  `converged = (hist[-1] < 1e-6 * max(1.0, hist[0])) or (hist[-1] < 1e-9)`. Because
  `hist[0] ≤ 1` here, `max(1.0, hist[0]) = 1.0` and the first clause degenerates to the
  **absolute** test `residual_rms < 1e-6`. Leg 71 landed at 3.88e-07 — a factor **2.58
  below** the line. I land above it. If H6 holds, the gate's truth value is decided by
  where a 40-iteration stall of an ill-conditioned least-squares lands relative to a
  fixed absolute constant, i.e. by the LAPACK/BLAS backend's roundoff.
  *Discriminator:* re-run item (6) across thread counts (`OMP_NUM_THREADS`,
  `OPENBLAS_NUM_THREADS`) and across small, physically irrelevant perturbations
  (n = 599/601/603, ladder spacing), and measure the **spread of `residual_rms` at
  a = 0.9 in decades**. **Predicted signature: the spread straddles 1e-6.** Recorded
  before running.
- **H7 — item (6) is testing the continuation *path*, not the equation.** The banked
  n=801 dense ladder converges at a=0.9; the test's coarse n=601 ladder does not. If H7
  holds, refining the ladder alone (same n, same code) flips item (6) to `converged=True`
  deterministically. *Discriminator:* a-ladder refinement at fixed n.
- **H8 — n=601 vs n=801 is the whole story** (a genuine discretization boundary).
  *Discriminator:* n sweep at fixed ladder.
- **H9 — the retry branch in `continuation` is the source of the bistability.**
  `continuation` re-solves from the anchor whenever `relres > 1e-10` and keeps the
  *smaller* relres, so the reported a=0.9 row is a **min of two stalls**. A min of two
  noisy quantities is exactly what H6 needs to become bimodal.
  *Discriminator:* record both branches separately.
- **H10 (must be excluded) — a real defect** in `TwoScaleNewton.solve`'s convergence
  predicate (e.g. `hist[0]` normalisation being wrong, or the line search terminating on
  a false decrease). *Discriminator:* the same absolute-vs-relative analysis, checked
  against the other five items and against `experiments/p2_route_d_v11_anchor.py`,
  `p2_route_d_v12_defect.py`, `test_advection_scope.py`, `test_collocation_newton.py`
  — the four other consumers of this module.

**Pre-committed edit discipline for Newton.** No assertion is flipped. If H6/H7/H9 hold,
item (6) is not measuring what its docstring says and the repair is to make it assert a
**deterministic, magnitude-bearing** statement (the *stall level*, or the a-ladder
dependence, or non-convergence at a genuinely unreachable a), with the non-determinism
itself recorded as the finding. If H10 holds the repair is in `solver/profile_newton.py`
and all five banked consumers are re-run and diffed.
**No number in `writeup/data/p2_route_d_v11_anchor.json` is to change. If a repair would
change one, that is escalation #4 and this branch parks.**

## 4. What would make this pass wrong

Written down so it can fail:

- If a window sweep leaves `p(s=0.10)` negative at **every** window, H1 is dead and G6 is
  measuring something real about the object — the repair then has to be in the physics or
  in `solver/fractional_boussinesq.py`, not in the gate.
- If item (6) returns `converged=False` at a = 0.9 on **every** thread count, every n in
  a neighbourhood, and every ladder refinement, then H6/H7/H8/H9 are all dead, leg 71's
  single observation stands as an unexplained outlier, and the honest report is
  "irreproducible on this host, cause not found" — not "green".
- If the repaired G6 changes any other gate's number in `test_fractional_boussinesq.py`,
  the repair is wrong regardless of what G6 then says.

## 5. Scope

Territory: `solver/fractional_boussinesq.py`, `solver/profile_newton.py`,
`test_fractional_boussinesq.py`, `test_profile_newton.py`, `experiments/` probe +
`writeup/data/*.json` + `writeup/` quartet + `experiments/journal/` for this bench leg.
Explicitly **not** touched: `experiments/JOURNAL.md`, `LITERATURE_CHECK.md`,
`plan_of_record.py`, `CONTINUATION_PROMPT.md`, `PHASE2_P2_NOTES.md`.

---

# FINDINGS (appended after the probes ran)

*(appended in a later commit — see `experiments/journal/leg_0_bench_redtests.md`)*
