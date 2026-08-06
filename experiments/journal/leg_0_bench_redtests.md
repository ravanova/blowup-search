# Leg 0 (BENCH) — findings: the two RED tests

Branch `bench/fix-red-tests-g6-newton`. Novelty pass committed first at `bfd6292`
(hypotheses H1–H10, each with its discriminator and its predicted signature, recorded
before any probe existed). This file is the FINDINGS half; it is written against those
pre-registered predictions and says which survived.

Probes: `experiments/leg_0_bench_g6_probe.py`, `experiments/leg_0_bench_newton_probe.py`,
`experiments/leg_0_bench_newton_eps.py`, `experiments/leg_0_bench_newton_threads.sh`.

---

## 0. Both reds reproduce as the novelty pass said, including the asymmetry

| test | leg 71 (host `/home/andy/projects/Unsolved/…`) | here (`/home/user/blowup-search/…`) |
|---|---|---|
| G6 `p > 0 at s=0.10` | `p = -0.211` | `p = -0.211` — **bit-identical** |
| Newton item (6) | `converged=True`, rms **3.881e-07**, 40 iters | `converged=False`, rms **2.120e-05**, 40 iters |

The G6 solver is bit-reproducible across hosts; the Newton solve is not. That single
contrast is the whole result: **the two reds have opposite causes.**

`git log --full-history` confirms the novelty pass's structural pin: `profile_newton.py`
and `test_profile_newton.py` have **exactly one commit each** (`6a17ce6`), `gclm_family.py`
last moved at `44a507c` (upstream of it), and `fractional_boussinesq.py` last at `59a9222`.
Nothing in either import graph changed between leg 71's audit and now. **Neither red is a
code regression** — that branch of the chartered question is closed by history, not by
argument.

---

## 1. G6 — a mis-specified gate on a deterministic solver

### The verdict

`p > 0 at s=0.10` asserts the **sign of a single-window fit whose window systematic is
~8x the quantity being signed.** The solver is fine. The gate was measuring the window.

### H1 (leading) — CONFIRMED, and the predicted signature matched exactly

Pre-registered prediction, quoted from the novelty pass: *"sign flip at s=0.10, no sign
flip at s=1.00, slope stable."* Measured by the probe over **15** windows:

| quantity | measured | pre-registered? |
|---|---|---|
| `p(s=0.10)` range | **[-1.574, +2.041]** — straddles 0, **5/15 windows positive** | yes, flip predicted |
| `p(s=1.00)` range | **[-4.090, -0.379]** — negative at **15/15** | yes, no flip predicted |
| ordering `p(1.00) < p(0.10)` | holds at **15/15** | yes, stable predicted |

The repaired gate ships a **10**-window subset (the widest windows dropped, since the two
most extreme p values come from the 5-point tail fits). On that subset, measured in the
gate itself: `p(s=0.10)` spans **[-0.457, +1.284]**, still straddling zero with **2/10**
windows positive; `p(s=1.00)` spans **[-3.971, -1.699]**, negative at 10/10, worst margin
**-1.699**; and the gap `p(0.10) − p(1.00)` stays in **[1.450, 4.999]**, positive at 10/10.
The conclusion is the same on either sweep, which is the point.

The gate's own default window `(0.40, 0.94)` gives -0.211; `(0.40, 0.80)` gives **+0.207**
and `(0.55, 0.85)` gives **+1.284**. The sign at s=0.10 is a property of the window, not
of the object.

### H2 — SUPPORTED. The fit residual exceeds the fitted quantity

`fit_rms` at the default window is **0.421** at s=0.10 against `|p| = 0.211` — the scatter
is **2.0x the number whose sign was asserted.** At s=1.00 `fit_rms` is 0.325 against
`|p| = 3.486`, a ratio of 0.09. Across thirds of the same run p(s=0.10) drifts
**-1.110 → +0.237** (the middle third has too few points to fit).

### The arithmetic that names the mechanism

| | s = 0.10 | s = 1.00 |
|---|---|---|
| fitted `p` (default window) | -0.211 | -3.486 |
| implied `beta_eff = (1-p)/2s` | **6.054** | 2.243 |
| geometric `beta` from `Lgrad`, same run | **1.740** | 1.903 |
| `p` predicted from that geometric beta | **+0.652** | -2.806 |
| \|predicted p\| vs window systematic (±1.8) | **0.36x — unresolvable** | **1.6x — resolvable** |

The run's own geometry predicts `p(s=0.10) = +0.652`, i.e. the sign the gate wanted — but
that prediction is **three times smaller than the window systematic**, so no single-window
fit can recover its sign. At s=1.00 the predicted `p = -2.806` is larger than the
systematic, which is exactly why that assertion is green and robust.

### H4 — CONFIRMED. The runs were never entitled to quote this at all

`collapse_window_report` **REFUSES on both G6 runs**, the same refusal G5 already gates on
for its own configuration:

- s=0.10: **0.67 decades** of (T−t) (need 1.5); beta moves **73%** across sub-windows (allow 25%)
- s=1.00: **0.63 decades**; beta moves **57%**

A run not entitled to quote `beta` is not entitled to quote the sign of `1 − 2·beta·s`.

### H3, H5 — EXCLUDED, as the discipline required

- **H3 dead.** Neither run terminates on wall clock: both stop on `under_resolved` (the
  spectral guard) at **34.2 s** and **28.5 s** against `wall_max=240`. Steps 420/440,
  samples 21/22. No machine-speed dependence, which is also why p is bit-reproducible.
- **H5 dead.** No instrument defect: the ratio is **strictly positive everywhere** (min
  **2.00e-04** at s=0.10, **1.70e-03** at s=1.00), no denominator approaches zero, no sign
  pathology. G4 separately measures `|adv|/|buo| = 8.77e-18` at the peak.

### The repair, and why it is not a threshold relaxation

Pre-committed discipline: *"the repair is to make the gate assert what the module says is
measurable … not to relax `p > 0` to `p > -0.3` and not to flip the assertion."*
H1, H2 and H4 all hold, so G6 now asserts, over an explicit 10-window sweep:

1. `p < 0 at s=1.00` at **every** window (worst margin quoted) — strengthened from one window to ten.
2. `p` decreases with s at **every** window — the instrument-response claim G6 is named for.
3. The s=0.10 sign is **window-indeterminate** while the s=1.00 sign is not — the withdrawn
   claim, recorded as the measurement that withdrew it.
4. `collapse_window_report` refuses on both runs, with the decades and spreads quoted.

`p > 0 at s=0.10` is **withdrawn, not inverted**: the run cannot support a claim of that
shape in *either* direction, and the gate now says so with numbers.

### Zero-regression proof

**`solver/fractional_boussinesq.py` is byte-identical — the repair is entirely in the
test.** Therefore every banked Route-G number (`p2_route_g_v1_collapse.json`,
`p2_route_g_v1_g2.json`, `p2_route_fd_v1_lit.json`) is unchanged **by construction**, not
by re-measurement. The other 36 gate lines in the file (G0–G5) are unchanged and still
pass; G6 goes from 2-of-3 to 4-of-4.

---

## 2. Newton item (6) — FLAKY, not red and not reliably green

### The verdict

The gate's truth value is decided by where a **40-iteration stall of a rank-deficient
least-squares** lands relative to a **fixed absolute constant `1e-6`**. It is green here,
red on leg 71's host, and neither outcome is a statement about the equation.

### H6 (leading) — CONFIRMED. The threshold is absolute, and the stall straddles it

`solve()` returns

    converged = (hist[-1] < 1e-6 * max(1.0, hist[0])) or (hist[-1] < 1e-9)

Measured `hist[0] = 0.0465` at a=0.9, so `max(1.0, hist[0]) = 1.0` **exactly** and clause 1
degenerates from a relative test to the **absolute** test `residual_rms < 1e-6`. Both
observations are 40-iteration stalls sitting on opposite sides of it:

| | residual_rms | decades vs 1e-6 | iterations | c | converged |
|---|---|---|---|---|---|
| leg 71 | **3.881e-07** | **−0.41** | 40 | 0.74833 | **True** |
| here, warm start | **2.120e-05** | **+1.33** | 40 | 0.76146 | **False** |
| here, cold start | **7.879e-05** | **+1.90** | 40 | 0.76953 | **False** |

Spread across the three: **2.31 decades**, and it straddles the threshold. `iterations = 40`
in every case — the iteration cap, never the `tol = 1e-13` break.

### The same signature in the other five items — the pattern that predicts it

The novelty pass pre-registered this table. It holds:

| item | leg 71 | here | ratio | nature |
|---|---|---|---|---|
| (1) Newton rms | 1.8e-15 | 2.0e-15 | 1.1x | true quadratic floor |
| (2) one-gauge **stall** | **8.8e-05** | **1.8e-06** | **49x** | 40-iter stall, rank-deficient |
| (3) history tail | 1e-15 | 9e-16 | 1.1x | true floor |
| (4) Jacobian vs FD | 6.7e-11 | 6.6e-11 | 1.0x | true floor |
| (5) continuation best | 5.9e-15 | 7.2e-15 | 1.2x | true floor |
| (6) a=0.9 **stall** | **2.9e-06** | **1.6e-04** | **55x** | 40-iter stall, rank-deficient |

**Every quantity that reaches a genuine convergence floor agrees to ~10% across hosts.
Both quantities that are iteration-capped stalls differ by ~50x, in opposite directions.**
This is not a solver defect; it is what a stalled ill-conditioned least-squares does under a
different LAPACK/BLAS backend.

### The sharpest form: a 1e-13 perturbation moves the stall, the floor does not move at all

`experiments/leg_0_bench_newton_eps.py` perturbs the last ladder point by `eps` and
re-runs the gate's exact continuation. Two rows are enough:

| eps | a=0.9 `residual_rms` | a=0.9 `c` | a=0.3 `relres` |
|---|---|---|---|
| 0 | **2.1197880415806517e-05** | 0.761460 | **2.576127359571511e-13** |
| **1e-13** | **8.051646124505419e-06** | 0.760991 | **2.576127359571511e-13** |

A relative perturbation of **1e-13** in `a` — seven orders below the ladder spacing and
right at the double-precision floor — changes the a=0.9 stall by a factor of **2.63**,
an amplification of order **1e12**. The a=0.3 value, which is a *genuine* convergence, is
**bit-identical to all 16 digits** across the same perturbation.

That is the finding in one table: **the converged points of this solver are exactly
reproducible and the stalled point is chaotic.** `eps = 0` also reproduced
2.1197880415806517e-05 bit-for-bit against the independent H9 run, so the stall is
deterministic *within* a fixed environment and unstable *across* environments — precisely
the profile of a quantity no gate should take the sign or the threshold-crossing of.

Both thresholds the repaired gate asserts (`a=0.3 < 1e-9`, `a=0.9 > 1e-8`) held on every
row measured.

### H9 — CONFIRMED as a contributing amplifier

`continuation` re-solves from the cold anchor whenever `relres > 1e-10` and keeps the
**smaller** relres, so the reported a=0.9 row is a **min of two independent stalls**
(2.120e-05 and 7.879e-05 here — a 3.7x spread between the two branches of a single run).
A min over noisy stalls is exactly the construction that makes the reported value bimodal
across environments.

### The banked measurement contradicts the gate's premise

`writeup/data/p2_route_d_v11_anchor.json` records a=0.9 at n=801 on a 17-point ladder as
`converged: true, relres 1.105e-14, iterations 7` — **machine precision in 7 iterations.**
So the banked science says Newton *does* converge at a=0.9, while item (6)'s docstring says
"past the survival boundary Newton does not converge." The gate's n=601 / 4-point ladder is
a **weaker continuation path**, not a boundary of the equation.

### The repair

Pre-committed: *"item (6) is not measuring what its docstring says and the repair is to make
it assert a deterministic, magnitude-bearing statement … with the non-determinism itself
recorded as the finding."* No assertion is flipped and `solver/profile_newton.py` is **not**
touched, so no banked number moves.

### Reported to the orchestrator, not fixed here

`TwoScaleNewton.solve`'s convergence predicate has a real latent weakness — `max(1.0, hist[0])`
silently converts the intended *relative* criterion into an *absolute* one whenever the
initial residual is below 1, and the predicate never checks whether the iteration cap was
hit, so an iteration-capped stall can be reported as `converged=True`. Repairing it would
change `converged` flags in five banked consumers, which the novelty pass pre-committed as
**escalation, not in-scope work.** Flagged, measured, left alone.
