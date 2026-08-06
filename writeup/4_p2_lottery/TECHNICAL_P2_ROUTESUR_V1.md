# Route-SUR v1 — the dealias-boundary repair, and the measured no-op that licensed it

**Leg 129. Branch `leg/129-sur-v1`. Claim-bearing (it moves numbers in a shared numerical
core). Gate: YES on all three clauses — PARKED under escalation #4, branch pushed, `main`
untouched.**

> ⚠ **Why this is parked.** The corrected cut moves the 2D solver's minimum admissible grid
> from `n >= 3` to `n >= 4`: under a *strict* 2/3 rule an `n = 3` grid retains `|k| < 1`, the
> mean mode alone, and leg 89's condition-based guard rejects it unmodified. That moves exactly
> **one of leg 133's 90 banked battery verdicts** — family `E_degenerate_discretization`, from
> `raised 13 / benign 3` to `raised 14 / benign 2`. Making the census check pass would require
> rewriting `writeup/data/p2_route_bob_v1_postrepair.json`, and rewriting a banked result in
> `writeup/` is **escalation #4**, never merged without the user. The move is strictly in the
> safer direction — `n_quieter = 0` unchanged, `n_louder` 40 → 41, `n_silent_to_raised` 23
> unchanged, all 90 cases still zero-silent, and leg 133's bitwise `n = 32` regression hashes
> still pass. See §6.

Runner `experiments/p2_route_sur_v1_repair.py` · data
`writeup/data/p2_route_sur_v1_repair.json` · figure `writeup/figures/fig61_route_sur_v1_repair.png`
(rebuilt by `experiments/p2_route_sur_v1_repair_evidence.py`) · novelty
`writeup/novelty/leg_129.md` · journal `experiments/journal/leg_129.md`.

---

## 1. What was wrong

Leg 120 (Route-SUA) audited `solver/spectral_utils.py`, the module every gCLM run imports, and
found seven defects. It was read-only on `solver/` and its pre-committed yes-branch was
*"report the exact failing case … escalate, do not patch"*, so it pinned all seven as failing-
in-waiting regression checks and escalated. Leg 129 is the repair.

The headline defect is one character. The 2/3 dealiasing rule was implemented as

```python
def dealias_mask(n):
    return wavenumbers(n) <= n / 3.0          # keep |k| <= n/3
```

and the alias-free condition is `|k| < n/3`, **strictly**. The two agree for every `n` not
divisible by three, because `floor(n/3) < n/3` there. When `3 | n` they differ by exactly one
mode — and that mode is the worst possible one to keep, because it beats with itself straight
back into the retained band.

`solver/boussinesq.py`'s `dealias_mask2d` carried the identical cut in both directions.

### 1.1 Why strict, three ways

**Published, 2013.** Bowman (*How Important is Dealiasing for Turbulence Simulations?*,
U. Alberta, p.29): *"one needs to pad to `N >= 3m - 2` to prevent mode `m - 1` from beating
with itself to contaminate the most negative (first) mode."* With `K = m - 1` the largest
retained wavenumber, that is `N >= 3K + 1`, i.e. `K < N/3`.

**Published again, independently, 2026.** Leg 129's novelty pass found arXiv:2603.08892
(*Aliasing and phase shifting in pseudo-spectral simulations of the incompressible
Navier–Stokes equations*), whose cubic truncation *"zeroes all modes for which any single
wavenumber component satisfies `|k_i| >= (2/3) k_N`"*. With `k_N = n/2` that zeroes exactly
`|k| = n/3`. Two sources, thirteen years apart, agree — and the leg deliberately does not rest
on either alone, because a third source (FourierFlows.jl) states the rule loosely enough to
read the other way. That ambiguity is recorded in the novelty log and chased to a dead end
rather than dropped.

**Elementary, no authority needed.** On an `n`-point grid with largest retained wavenumber `K`,
a quadratic nonlinearity produces modes up to `2K`, which alias to `2K - n`. That lands back
inside the retained band iff `|2K - n| <= K`, i.e. iff `n <= 3K`. Alias-freedom is exactly
`n > 3K`.

### 1.2 The measured consequence

Leg 120 ran Bowman's own experiment — put the field on the top retained mode `K`, square it,
read mode `K` back, where the true coefficient is exactly zero:

| grids | spurious coefficient at `k = K` |
|---|---|
| `3 ∤ n` (12 sizes) | ≤ **4.83e-16** |
| `3 \| n` (11 sizes) | **2.500e-01**, identical at every one |

and the consequence in a shipped diagnostic: `energy_production`, whose docstring calls it the
*"Exact rate `d/dt E`"* and which `solver/gclm.py` accumulates into the per-run
**energy-balance residual** — the artifact guard of `LOGGING.md` — was wrong by **1.6621e-01
relative at `n = 81`**, against **2.47e-14** worst case at every `n` not divisible by three.
It evaluates a *cubic* product, so the over-wide band admits the triad `K + K + K = n`.

**No banked number was ever affected.** Every grid size declared on the dealias path in this
repository is a power of two (`{64, 256, 512, 1024, 2048, 4096, 8192}`, plus the 2D `n = 32`),
and no power of two is divisible by three. The defect was **latent** — exactly the severity
shape of legs 66, 69 and 79. It would have activated the first time anyone picked `n = 96`.

### 1.3 The five silent-absorption defects

| | function | before | after |
|---|---|---|---|
| **D3** | `derivative_hat` | assigned `d[-1] = 0.0`, so a non-finite Nyquist coefficient was **erased**: 12/12 poisons returned a fully finite spectrum with `max|w_x| = 1.0000`, indistinguishable from clean input | multiplies by zero (Johnson Alg. 1 step 2), 12/12 propagate |
| **D4** | `velocity_hat` | `np.zeros_like` left the mean mode at a fresh zero whatever came in: 3/3 poisons erased | multiplies by zero, 3/3 propagate |
| **D5** | `velocity_hat` | inherited the input dtype, so integer input was unsafe-cast on assignment: worst relative error **1.0000** over 600 draws | allocates `complex128`, worst relative error **0.0** |
| **D6** | `hilbert_hat`, `derivative_hat` | a scalar or length-1 `k` **broadcast** into a full-length wrong answer: 8/15 accepted, worst relative sup error **2.0000** (`k = -1.0` returns the sign-flipped transform) | 15/15 refused, all `ValueError` |
| **D7** | `grid`, `wavenumbers`, `dealias_mask` | three behaviours for one invalid `n`: silent empty array, `ZeroDivisionError`, or silent empty array | 15/15 refused, all `ValueError` |

D6 and D7 are as much about **consistency** as about absorption: `velocity_hat` already
refused malformed `k`, but only by accident of indexing it, and it raised `TypeError` or
`IndexError` depending on which malformation. One caller error, three behaviours.

---

## 2. The repair

```python
def dealias_mask(n):
    cut = (n - 1) // 3          # the largest integer STRICTLY below n/3
    return wavenumbers(n) <= cut
```

and the same `cut` in `dealias_mask2d`. `derivative_hat` and `velocity_hat` now write
`x * 0.0 + 0.0j` where they previously assigned `0.0`; the `+ 0.0j` normalizes the signed zero
a multiplication can produce, so **finite input still yields exactly `+0.0 + 0.0j`** while
`nan`/`inf` propagate. `_require_k` and `_require_grid_size` give one refusal shape for the two
caller errors.

**The repair form `(n - 1) // 3` is not published.** The novelty pass looked and found no
source that writes the retained set as an integer expression, so the runner **proves** it
instead of citing it: `(n-1)//3 < n/3 <= (n-1)//3 + 1` holds with **0 counterexamples over
`n = 1..5000`**, it equals `floor(n/3)` at **3334/5000** values of `n`, and the **1666** where
it differs are *exactly* the multiples of three.

---

## 3. The licence: a bitwise no-op on everything already banked

The leg's brief was explicit: *"if ANY power-of-two-grid quantity changes at all, stop and
escalate — the entire license for this repair is the measured no-op guarantee."* So the no-op
is measured, not argued.

**Method.** The pre-repair `solver/` tree is extracted from git at the merge base
(`acce159`), run in a **separate interpreter** with the repaired tree off `sys.path`, and
compared against the repaired tree quantity by quantity: `sha256` of raw array bytes (sensitive
to dtype, shape and signed zero) and `float.hex()` for scalars. `wall_clock_seconds` is
excluded as nondeterministic; nothing else is.

| bucket | quantities | moved |
|---|---|---|
| 1D mask, declared power-of-two grids | 21 | **0** |
| 2D mask, banked `n = 32` | 2 | **0** |
| every public helper + `energy_production`, declared grids | 84 | **0** |
| **END-TO-END solver runs** (gCLM `n = 64` × 3, Boussinesq `n = 32`) | 49 | **0** |
| 1D mask at `3 \| n` — **the control** | 33 | **33** |

**0 of 156.** The end-to-end row is the one that matters most: three full gCLM integrations
(CLM `a = 0`, De Gregorio `a = 1`, viscous `nu = 5e-3`) and one Boussinesq integration, compared
on `omega_final`, `theta_final`, the `max_omega` and `times` traces, and every scalar the result
object carries — including `energy_balance_residual` and `conservation_drift` themselves.

### 3.1 The control, and why it is in the figure

**Lesson 90: a control that cannot come out differently is not a control, and the tell is that
its numbers are identical.** This measurement earned that lesson the hard way. The *first* run
of the harness reported **0 differing in every bucket, including the `3 | n` control** — and
that was not a no-op, it was a dead harness. Importing the runner executes its module-level
`sys.path.insert(0, REPO)`, which put the *repaired* tree ahead of the extracted pre-repair one,
so the "pre" side was silently the post side and the comparison was a tautology of the code.

The `3 | n` bucket caught it, which is the entire reason it is carried. It is now an
**executable assertion** in the runner: if fewer than 33 of 33 control quantities move, the run
aborts with `HARNESS DEAD: … Every no-op claim in this run is void.` The repaired harness
reports `33/33` moving, with the top retained mode dropping by exactly one at every one of the
eleven grids (`n = 96`: `32 → 31`; `n = 81`: `27 → 26`; and so on).

### 3.2 The banked-record census, re-run

Leg 120 counted **107** banked `energy_balance_residual` records, in two files, **0** exposed.
Legs 103 and 133 have since banked their own post-repair data, so leg 129 re-ran the census
rather than quoting it: **129 records in four files** (`p2_route_boa_v1_adversarial.json` 89,
`p2_route_bob_v1_postrepair.json` 17, `p2_route_gla_v1_adversarial.json` 18,
`p2_route_glb_v1_postrepair.json` 5). Of the eight declared grid sizes on the dealias path,
**0** are divisible by three. **0 of 129 banked records were ever wrong.**

---

## 4. Gate clause (b): the defect is gone, not relocated

| `n` | rel. err before | rel. err after | improvement |
|---|---|---|---|
| 12 | 5.1939e-04 | 7.4107e-16 | 7.0e+11× |
| 24 | 1.7694e-02 | 1.1483e-15 | 1.5e+13× |
| 27 | 8.7971e-02 | 3.9374e-16 | 2.2e+14× |
| 48 | 6.6552e-02 | 5.3569e-16 | 1.2e+14× |
| **81** | **1.6621e-01** | **0.0000e+00** | — |
| 96 | 3.1790e-04 | 6.0904e-16 | 5.2e+11× |
| 192 | 7.0290e-02 | 4.2926e-16 | 1.6e+14× |
| 384 | 1.6106e-02 | 1.4543e-15 | 1.1e+13× |
| 768 | 1.5883e-02 | 7.3915e-16 | 2.2e+13× |

Worst **1.6621e-01 → 1.4543e-15**: **14.1 decades**, and the post-repair worst case is *below*
the 2.47e-14 round-off class the gate named as the target. The `n = 81` entry reproduces leg
120's banked headline exactly, which is the cross-check that the two legs measured the same
thing.

Bowman's experiment post-repair: worst spurious coefficient **1.142e-15** at `3 | n` (was
2.500e-01) and **4.828e-16** at `3 ∤ n` (was 4.83e-16 — *unchanged*). That second column is the
one that shows the repair did not merely move the defect somewhere else. `K < n/3` now holds at
**23/23** grid sizes.

The repair is also checked for **over-truncation**, which would be a silent resolution loss
dressed as a fix: the regression suite asserts `K + 1 >= n/3` as well as `K < n/3`, i.e. the
mask keeps the *largest* admissible mode.

---

## 5. What is banked, and the two territory notes

`test_spectral_utils_adversarial.py`'s **seven pins are inverted in the same commit as the
repair**, as leg 120 designed them to be: each check now asserts the correct behaviour, fails
if the defect returns, and keeps the pre-repair magnitude in its docstring as the BEFORE column
so that a future failure can report a magnitude rather than a boolean. 11/11 checks pass. Leg
69's odd-`n` `derivative_hat` control still passes (relative error 5.8e-15 / 1.5e-14 / 4.4e-14
at `n = 17, 65, 129`) — that fix is intact and is not re-found here.

Two files were edited that the declared territory did not name, both recorded rather than
quietly absorbed:

1. **`test_boussinesq_dedicated.py::check_dealias_mask2d`** asserted `kx = n/3 must be
   retained` — the same defect-encoding assertion the territory *did* authorize inverting in
   the 1D twin. Leg 120 audited only the 1D module and never opened this file, so the DM did
   not know the 2D twin carried it. Leaving it would have landed a suite asserting a defect
   the same commit removed. The edit is the same inversion on the same two lines and nothing
   else in the file.
2. **The quartet files** (`BLOG_`/`TECHNICAL_`/`*_evidence.py`/`build_figures.py`), which the
   standing documentation contract in `ORCHESTRATION.md` §6 requires of every leg but which
   the territory list omitted.

Both are minimal and in-kind. Neither touches a shared ledger.

---

## 6. The escalation: the 2D resolution floor moves 3 → 4

`solver/boussinesq.py` carries leg 89's guard, which raises when *"the 2/3 dealias mask retains
only the mean mode"*. It tests the **condition**, not a hard-coded `n` — which is why it needed
no edit, and why its behaviour changed the moment the mask became correct.

| `n` | retained modes, old cut | retained modes, new cut | accepted? |
|---|---|---|---|
| 1, 2 | 1 | 1 | rejected, before and after |
| **3** | **2** | **1** | **was accepted, now rejected** |
| 4, 5, 6 | ≥ 2 | ≥ 2 | accepted, before and after |

At `n = 3` the strict band is `|k| < 1`. A 3-point grid cannot carry a non-constant field under
a correct 2/3 rule, so rejecting it is right — but "right" is not the same as "this leg's to
land", and the number it moves was banked by leg 133 six commits ago.

**Scope, measured rather than asserted.** No power of two, no banked grid, no
`energy_balance_residual` record (0 of 129), and none of the 156 quantities in the §3 A/B are
affected. `n = 3` and `n = 4` appear in no run anywhere in the repository outside two
adversarial batteries. The leg's own pre-committed no-branch — *"if ANY power-of-two-grid
quantity changes at all, stop and escalate"* — did **not** fire; this is a narrower and
different thing, and the two must not be confused.

**The decision the user/DM owns:** re-bank leg 133's `E` family census as `14/2` (the repair is
correct and the move is strictly louder), or reject the 2D half of this repair. The 1D half is
independent of the question and unaffected by it.

Three dependent edits are already made and are *not* themselves the escalation — ordinary
in-kind updates whose intent is preserved exactly:
`test_boussinesq_adversarial.py::check_repaired_degenerate_grid_is_rejected` moves `n = 3` from
its "must run" list to its "must be rejected" list;
`test_boussinesq_postrepair.py::check_CONTROL_valid_input_is_still_accepted` takes `n = 4` as
"the smallest grid that can carry a non-constant field"; and the guard's message now reads
`n >= 4 required`. Both files pass afterwards **except** the census check, which is the only
failure in the entire affected-test set (23 tests selected by import closure, plus the two
always-on gate tests).

## 6a. The price, measured

A repair that adds per-call validation to a module in the solver's inner loop costs something,
and "negligible" is not a measurement. Min-of-3 per variant, the two variants interleaved and
repeated so a loaded machine cannot flatter either side (§C3 of the runner):

| quantity | ratio post/pre |
|---|---|
| `hilbert_hat` (50k calls, n = 256) | **1.12×** |
| `derivative_hat` | **0.88×** |
| `velocity_hat` | **2.06×** |
| **`solve_gclm`, full 200-step n = 64 integration** | **1.06×** |

The headline is the last row: **+6.4% on a real solve**. `velocity_hat` doubles because D4 and
D5 make it do strictly more work — a `complex128` allocation plus a masked multiply-by-zero on
the mean mode — but it is not the dominant cost in a step, so the solve-level figure is what
matters.

The first version of the validation was worse (**+14.5%** on `solve_gclm`) because it called
`np.asarray`/`np.shape` on every call; reading `.shape` directly gives identical refusals for
roughly a seventh of the cost. That was found by measuring rather than by inspection.

**A cheaper `velocity_hat` was available and was deliberately not taken.** Dividing the whole
array by `|k|` with the zero entry replaced by `inf`, then adding `0.0j` once, removes the
masked assignment entirely — but the trailing `+ 0.0j` would then also normalize signed zeros
in the *non-zero* modes, so any entry whose quotient is `-0.0` would change bitwise. That
trades the no-op guarantee this repair's whole licence rests on for 6%, which is not a trade
this leg is entitled to make. Recorded so the option is not silently rediscovered as an
improvement.

Wall-clock seconds are machine- and load-dependent (another leg's tests were running
concurrently); the **ratio** is the reportable quantity, and it is what the JSON carries.

## 7. Honest limits

- **Every number here is a statement about code behaviour.** None is a physics measurement,
  none contests any banked result, and nothing here touches a link of the L1→L4 chain.
- **The no-op is measured at the configurations the repository actually uses**, which is the
  strongest form available but is not the same as "for all `n`". At `3 | n` the module
  deliberately returns something different — that is the repair.
- **The "3 ∤ n unchanged" column is a control, not a proof of correctness**: it shows the
  repair is confined to the boundary, not that everything else in the module is right.
- **D4 remains the weakest of the seven**, as leg 120 reported it: the erased value was the
  intended zero-mean convention, so only the loss of the corruption signal was ever a defect.
  It is fixed at that strength and claimed at no higher.
- The alias-free reference in section 4 is a 6× grid refinement, not an analytic value. Its own
  convergence is evidenced by the `3 ∤ n` column agreeing with `energy_production` to 2.5e-14.
- `test_advection_scope.py` exceeds a 1200 s timeout on this machine both before and after the
  repair. Its import closure is 6 repository modules and contains **neither** changed file, so
  it is provably independent of this diff; it is reported, not swept.
