# TECHNICAL — Route-BVRRV v1: an independent re-run of a repair *and* of the re-confirmation that graded it

**Leg 233, verification class, not floor-eligible.** Closes leg 205's silent-fabrication
finding in `solver/boussinesq_rescaled.py::odd_field_x_slope` on independently-confirmed
footing.

| | |
|---|---|
| Runner | `experiments/p2_route_bvrrv_v1_postrepair.py` (~1.9 h wall, four-way parallel) |
| Curated data | `writeup/data/p2_route_bvrrv_v1_postrepair.json`, at commit `8e753a0` |
| Evidence / figure | `experiments/p2_route_bvrrv_v1_postrepair_evidence.py` → **fig101**, registered in `writeup/build_figures.py`; **45/45** checks, rebuilt from the curated JSON with nothing re-run |
| Standing gate | `test_boussinesq_rescaled_postrepair.py`, **14/14**; the module's own three suites, **3/3** |
| Journal | `experiments/journal/leg_233.md` |
| Reads, edits nowhere | `solver/boussinesq_rescaled.py` |
| Ceiling | No `L1 → L4` link moved. **Clay stays ~0.05%.** This is a verification of a solver utility's input-validation guards. |

*Quartet note: this document, its BLOG sibling, the evidence script and fig101 were produced by
a DOCS rework unit from the already-banked JSON (ORCHESTRATION.md §6). No number here is new;
no sweep was re-run.*

---

## 1. The gate, and its answer

> **Q.** Does an independent re-run confirm (a) both named mechanisms now reject correctly, and
> (b) the zero-contamination re-confirmation itself reproduces (no banked
> `boussinesq_rescaled.py`-dependent value actually moved)?

> **A. YES on both**, over the live scope stated in §6.

The chain being closed has three links and each was previously graded by the link below it:
leg 205 (`526bce4`) **found** two silent-fabrication mechanisms and patched neither; leg 221
(`d2d9769`, `7e58419`) **repaired** both **and** performed the zero-contamination
re-confirmation leg 205 had skipped — that is, leg 221 graded its own repair. Leg 233 is the
first party to grade it from outside.

## 2. Is the module under verification the module leg 221 verified?

A magnitude, not a boolean. `solver/boussinesq_rescaled.py` was last touched by **leg 352
(`aa9c5cd`), after the repair**, so leg 221's own "byte-identical to baseline" re-check no
longer holds.

| version | bytes | lines | docstring-stripped AST |
|---|---|---|---|
| pre-repair `1a3e63c` | 14 392 | 280 | `a30297121a75b194…` |
| repair commit `d2d9769` | 21 057 | 377 | `a162017d6d2b382f…` |
| leg 221 final `7e58419` | 21 821 | 386 | `a162017d6d2b382f…` |
| **`main` today** | **21 944** | **388** | **`a162017d6d2b382f…`** |

Main differs from leg 221's final state by **+123 bytes / +2 lines** raw, and by **nothing** at
docstring-stripped AST level. It differs from the pre-repair copy at that level. Leg 352's diff
is confined to the module docstring. **Every post-repair change to this module is docstring
text; the executable semantics under verification are exactly the repaired ones.** That
statement is pinned by `test_module_semantics_are_still_the_repaired_ones`, so a future leg
that edits executable code here gets a test failure telling it to re-run, not a silent
inheritance of this leg's answer.

## 3. Lesson 90 — before any zero is believed

A differential between a module and itself reports zero for free. The two module objects are
therefore asserted distinct, and shown **disagreeing by a measured amount** on the two inputs
leg 205 published (leg 205's own grids: `n_r=400, n_beta=16, r_min=1e-4, r_max=1e4`):

| | pre-repair | post-repair | truth | module tolerance |
|---|---|---|---|---|
| **DEFECT B** (`lam=400`, field scale 0.05) | `0.26930226316474387` (rel err **8.653e-01**) | `2.0007759522991355` (rel err **3.880e-04**) | 2.0 | 5e-4 |
| **DEFECT A** (empty window, `r_min = 0.5 > r_win`) | exactly **`0.0`**, no raise, no warning | **`ValueError`** | 2.0 | — |

The signature comparison is recorded as a magnitude rather than a check: the repair *adds*
`min_points` and `max_rel_residual`, so identical signatures would have been the surprise.
`(g, grid, r_win=0.4, i_lo=3)` becomes
`(g, grid, r_win=0.4, i_lo=3, min_points=3, max_rel_residual=0.5)`. All six control checks
pass.

*(The journal's §4.1 table quotes the DEFECT-B recovery to a slightly different rounding,
`2.0007346` / rel err `3.673e-4`. The curated JSON's `lesson_90_control.magnitudes` banks
`2.0007759522991355` / `3.8797614956775917e-04`; this document quotes the JSON, which the
evidence script checks. Both readings sit inside the module's 5e-4 acceptance tolerance and
neither changes any verdict.)*

## 4. Clause (a) — do both named mechanisms now reject correctly? **YES**

Leg 205's 81-case battery is read **verbatim** out of git at `origin/leg/205-bvr-v1` — it is
the object under test, so re-implementing it would test a different battery — and executed
**twice in one process**: once against the pre-repair module loaded out of `1a3e63c`, once
against main's module on disk. The classifier, flattener and comparison rule are written in
this leg's runner and imported from nothing, so a bug in leg 221's machinery cannot survive
into this answer by inheritance.

### 4.1 Three columns (fig101, panel A)

| | OK | SILENT_WRONG | RAISED | NONFINITE | NO_REFERENT | RETURNED |
|---|---|---|---|---|---|---|
| leg 205, committed | 32 | **18** | 11 | 9 | 2 | 9 |
| re-measured pre-repair, live | 32 | **18** | 11 | 9 | 2 | 9 |
| post-repair, main today, live | 42 | **0** | 19 | 9 | 2 | 9 |

**The control on the control:** the pre-repair column reproduces leg 205 **case-by-case on the
`case` string**, `n_verdict_mismatch_vs_committed = 0` of 81 — not merely tally-for-tally,
because a tally can match while individual verdicts swap. So the "before" column is genuinely
leg 205's finding, and **SILENT_WRONG 18 → 0** is a real differential rather than an artifact
of the harness.

### 4.2 The transition matrix — the measurement a count cannot make

A count of zero cannot see a repair that buys its zero by breaking something else. The full
matrix can, and it conserves the battery (the eight entries sum to 81):

```
OK -> OK                    29        SILENT_WRONG -> OK          13
RAISED -> RAISED            11        SILENT_WRONG -> RAISED       5
NONFINITE -> NONFINITE       9        OK -> RAISED                 3
RETURNED -> RETURNED         9        NO_REFERENT -> NO_REFERENT   2
```

The 18 SILENT_WRONGs split **13 → OK** (the value is now right) and **5 → RAISED** (the module
now refuses rather than fabricating). Both are the repair working, and the per-case fate list
agrees with the matrix, 13 and 5. Among the 13, the worst pre-repair reading recovered is the
`lam=400` DEFECT-B case, `0.26930226316474387` → `2.0007759522991355`; the gentlest is
`lam=4`, `1.9978467261707167` → `2.000768398060092` (rel err `1.077e-03` → `3.842e-04`). Among
the 5, four returned **exactly `0.0`** pre-repair on empty windows and one returned
`1.9061283431326006` on a single node.

### 4.3 Three OK → RAISED transitions leg 221 never reported (fig101, panel B)

A refusal is neither automatically a regression nor automatically correct, so each is
**adjudicated against the module's own documented precondition**: the case's grid is rebuilt
from the battery's recorded parameters, and the window occupancy and the lstsq **rank** of the
`(r, r³, r⁵)` design matrix are measured. A refusal counts as justified only if the stated
precondition genuinely fails.

| case | window nodes | rank | σ_min/σ_max | pre-repair returned | pre rel err | margin inside 5e-4 | verdict |
|---|---|---|---|---|---|---|---|
| `F1 r_min sweep: 2 nodes` | **2** (< 3 params) | 2 of 3 | 2.402e-02 | `1.9995773690878733` | 2.113e-04 | 2.887e-04 (57.7% of tol) | JUSTIFIED_REFUSAL |
| `F1 r_win sweep: r_win=0.0003` | 21 | **2 of 3** | **4.125e-16** | `2.0009994415183723` | 4.9972e-04 | **2.792e-07 (0.056% of tol)** | JUSTIFIED_REFUSAL |
| `F1 r_win sweep: r_win=0.0005` | 32 | **2 of 3** | **3.867e-15** | `2.000999441518362` | 4.9972e-04 | **2.792e-07 (0.056% of tol)** | JUSTIFIED_REFUSAL |

**3 JUSTIFIED_REFUSAL, 0 UNJUSTIFIED_REGRESSION**, and `precondition_genuinely_fails` is true
on all three.

The middle two are a finding about *leg 205's own battery*, not only about leg 221's repair. At
`r_win = 3e-4` and `5e-4` the window holds 21 and 32 nodes, so the occupancy guard is provably
blind to them — but the design matrix is numerically singular (singular values
`[9.009e-04, 1.943e-11, 3.716e-19]` and `[1.575e-03, 1.039e-10, 6.091e-18]`), and lstsq's
minimum-norm solution landed at rel err `4.9972e-04` against a `5e-4` tolerance. Leg 205's
classifier scored them OK with a margin of `2.792e-07`, **0.056% of the tolerance**. They were
accidental passes on rank-deficient fits, and the repaired module correctly refuses them. The
third is the same story at 2 nodes against 3 parameters — the exact fabrication class leg 205
named, right by luck.

An independent verifier that only re-counted would have missed this in either direction.

## 5. Clause (b) — does the zero-contamination re-confirmation itself reproduce? **YES**

### 5.1 Method, and why this zero means more than leg 221's zero

A differential shim replaces `odd_field_x_slope` with a wrapper that calls the **pre-repair**
and **post-repair** implementations on identical arguments, compares bitwise (NaN equal to
NaN), and **returns the pre-repair value**, so the trajectory each artifact script follows is
exactly the banked one. If every call agrees bitwise, the repaired module reproduces the run by
determinism, and no banked value can have moved *because of the repair*.

Three things make this a verification rather than a repetition:

1. **The shim is this leg's own** and imports nothing from
   `experiments/p2_route_bvrr_v1_repair.py`. A bug in leg 221's comparison — a `==` that
   swallows NaN, or a shim that never installs — could not have been detected by re-running leg
   221's code.
2. **No cache.** Leg 221's sweep was resumable and cache-backed; its re-confirmation replayed
   in **66.1 s** against a **~34 h** original. A cache replay is not an independent re-run.
   There is no cache-read path anywhere in this leg's runner, and every unit carries
   `ran_live: true`, `from_cache: false`.
3. **Guard reachability, not just agreement.** A bitwise-agreement count of zero is equally
   consistent with "the repair is correct on this trajectory" and with "the guard was never
   reached, so nothing was tested". Each call is therefore additionally instrumented for
   whether the DEFECT-B window cap **binds** (`r_win_eff < r_win`), the window's node count,
   and the fitted residual. That converts the zero from an observation into an *explanation*.

### 5.2 The sweep — 6 of 6 artifacts live, 0 from cache (fig101, panels C and D)

| unit | argv | wall | calls compared | bit-identical | **moved** | `raise_post` | cap binds | min window nodes |
|---|---|---|---|---|---|---|---|---|
| `spike1_stepB_rescaled` | `--generate` | 2.5 s | 2 | 2 | **0** | 0 | 0 | 481 |
| `p2_route_brs_v1_status_audit` | — | 0.3 s | 62 | 62 | **0** | 0 | 0 | **4** |
| `p2_route_k_v1_port` | — | 744.6 s | 52 516 | 52 516 | **0** | 0 | 0 | 62 |
| `p2_route_l_v1_precond` | — | 1 025.1 s | 42 488 | 42 488 | **0** | 0 | 0 | 62 |
| `p2_route_g_v1_g2` | `--only g2` | 2 836.0 s | 140 016 | 140 016 | **0** | 0 | 0 | 95 |
| `spike1_stepC_gate` | `--logged --steps 2500` | 2 360.3 s | 100 008 | 100 008 | **0** | 0 | 0 | 95 |
| `test_boussinesq_rescaled.py` | — | 32.5 s | 4 999 | 4 999 | **0** | 0 | 0 | 71 |
| `test_boussinesq_transport.py` | — | 0.2 s | 0 | 0 | **0** | 0 | 0 | — |
| `test_boussinesq_rescaled_status.py` | — | 0.3 s | 142 | 142 | **0** | 0 | 0 | **4** |
| **TOTAL** | | **~1.9 h, 4-way parallel** | **340 233** | **340 233** | **0** | **0** | **0** | |

`artifacts_run_live = 6/6`, `not_run_live = []`, `all_artifacts_restored_clean = true`,
`any_nonzero_returncode = false`, `test_suites_all_passed = true`. The 340 233 is
`335 092` artifact calls `+ 5 141` shimmed-suite calls, and both parts are the sum of the
per-unit rows rather than a separately reported figure.

**Guard reachability — the sharper reading, and the single most load-bearing number here.**
`cap_binds = 0` across all **340 233** calls, and the minimum window occupancy anywhere in the
banked corpus is **4 nodes** against the guard's floor of **3**. So the zero is *explained*: no
banked call comes near either guard, and the DEFECT-B cap is non-binding on every one of them,
which by the module's shrink-only rule makes `r_win_eff` the identical float and the fit
bit-identical. The probe can report the opposite — it binds at a shrink factor of 0.0622 on leg
205's own DEFECT-B field — so this is a statement about the corpus, not about the probe.

### 5.3 A strict superset of leg 221's scope, not a match

Per-unit call counts reproduce leg 221 **exactly** — 2 / 62 / 52 516 / 42 488 / 140 016, and
4 999 / 0 / 142 from the three shimmed suites — which is a stronger agreement than a matching
total, because a total can match while the composition shifts. Leg 221's **256 233** headline
decomposes in its own committed JSON as **251 092** banked-artifact calls **+ 5 141** suite
calls, and this leg reproduces that decomposition.

The single divergence is `spike1_stepC_gate`. Leg 221 swept it at **16 008** calls; this leg
sweeps it at **100 008**, because leg 335 established that the banked artifact records
`steps: 2500` while the script's CLI default is `400`. The excess is **exactly +84 000 calls**,
so this leg's scope is a strict superset of leg 221's. It is reported as an excess, not
smoothed into a matching number.

## 6. The negative construction: a fabricated zero in this leg's **own** instrument

`max_rel_residual_seen` was initialised to `0.0` in the shim's state dict and **never written
to by any code path**, so it reported exactly `0.0` for every artifact — a plausible number
that measured nothing. This is the **same failure class** as leg 205's DEFECT A (an unguarded
`lstsq` silently returning exactly `0.0`), occurring in the auditor rather than in the audited
module. It was caught by noticing that a least-squares relative residual is never exactly zero
on real data across 95 068 calls.

The probe now actually solves the `(r, r³, r⁵)` fit on the capped window and returns
‖Ax − y‖/‖y‖. Re-measured live it is demonstrably alive:

| unit | calls with residual measured | max rel residual | over the 0.5 backstop |
|---|---|---|---|
| `spike1_stepB_rescaled` | 2 | **1.296e-05** | 0 |
| `p2_route_brs_v1_status_audit` | 62 | **1.469e-01** | 0 |

**0 of 64 exceed the module's 0.5 backstop**, and the `1.469e-01` is the informative one: it
sits within a factor of **3.404** of the backstop, so the backstop is set at a scale the data
approaches rather than being unreachable by construction.

**The scope limit, stated rather than smoothed.** The four heavy sweeps were already in flight
when the defect was found and cannot be retrofitted without ~30 CPU-hours of re-running, so the
merge step **strips** the fake `0.0` from any record lacking `n_residual_measured` and marks it
`residual_instrumented: false` with an explicit NOT MEASURED note — the key is absent, not
zero. The residual is instrumented on **2 of 6 artifacts / 64 of 340 233 calls**.

**The gap is covered, and the covering argument is itself a measurement:** the residual
backstop can only manifest as a **refusal**, and `raise_post = 0` across all **340 233** calls.
A backstop that never refused never fired. So the residual magnitude was a sharpening this leg
wanted, not a load-bearing input to the gate. This is an **open** item, not a closed one, and
§8 carries it as such.

## 7. Artifact leaves that DO move — measured, non-attributable, cause undiagnosed

| artifact | leaves compared | identical | **moved** | worst leaf rel. diff |
|---|---|---|---|---|
| `spike1_stepB_rescaled` | 28 | 28 | 0 | — |
| `p2_route_brs_v1_status_audit` | 451 | 450 | 0 | — |
| `p2_route_k_v1_port` | 273 | 167 | **105** | 2.818e-02 (`K3…jv_step_study[5].rel_change_vs_previous_h`) |
| `p2_route_l_v1_precond` | 353 | 211 | **141** | 2.409e-02 (`L4_newton.iterations[2].gmres_rel`) |
| `p2_route_g_v1_g2` | 120 | 52 | **68** | **2.424e-12** (`g2_our_beta.steps_ladder[2].residual`) |
| `spike1_stepC_gate` | 1 028 | 642 | **386** | **9.028e-12** (`runs[1].cut_omega[7]`) |
| **TOTAL** | 2 253 | 1 550 | **700** | |

This reproduces leg 221's qualitative finding (it reported **839** moving leaves over its own,
smaller stepC scope) and **0 of the 700 is attributable to the repair** — not by a separate
control run but *by construction*: the shim returns the pre-repair value, so the executed
trajectory is the pre-repair trajectory, and all 340 233 calls agreed bitwise anyway. The
movement is pre-existing irreproducibility in this repo; it is measured here and, per §7b of
`ORCHESTRATION.md`, **reported, not repaired**. **Its cause is undiagnosed and is left open.**

**An independent confirmation of leg 335, which was not this leg's job.** Leg 221 flagged
`spike1_stepC_gate` as its sharpest mover — `alpha` −0.3350763095 → −0.3793563731, **13.2%**,
with `cut_omega[10]` at relative **4.47** and two of the artifact's own gate predicates
flipping true → false. Leg 335 adjudicated that gap `REPRODUCIBLE_AS_BANKED`, attributing it to
the harness running the CLI default `--steps 400` against an artifact banked at `steps: 2500`.
Run here at the corrected 2 500 steps, **the worst leaf in that artifact moves by 9.028e-12** —
about **eleven orders of magnitude** below leg 221's 13.2%. Leg 335's adjudication is confirmed
by live measurement from an independent harness.

## 8. Open, and reported-not-repaired

1. **The residual instrumentation is partial**: 2 of 6 artifacts, 64 of 340 233 calls. The
   remaining coverage is by `raise_post = 0`, which is an argument that the backstop never
   fired, **not** a direct measurement of the residual on those calls (§6).
2. **The 700 moving artifact leaves are non-attributable to the repair, but their cause is
   undiagnosed** (§7). A leg that wants that cause is a separate leg and must not borrow this
   leg's conclusion as cover.
3. **Caller-census drift is reported, not repaired.** The census was re-grepped live: **15**
   real importers today against the registry's **6** banked artifacts, with **3** newcomers —
   `experiments/p2_route_tscx_v1.py` (leg 307, `401a5f7`),
   `experiments/p2_route_s1gr_v1.py` (leg 335, `cc725d1`) and
   `test_boussinesq_rescaled_postrepair.py` (`b209ca0`) — **all three post-dating the repair
   commit `d2d9769`**. Contamination is a claim about values banked in the *pre-repair* world,
   so none of them can carry it. The precise statement is that the registry is **complete over
   its own scope** (pre-repair-banked artifacts) and **stale as a census of today's callers**.
   Two further files name the module in a string without importing it
   (`solver/target_selection.py:490`, `experiments/p2_route_sirc_v1_census.py:495`) and are
   correctly absent from both.

## 9. What this leg does not claim

* **No `L1 → L4` link moved. Clay stays ~0.05%.** This verifies a solver utility's
  input-validation guards; it closes an audit thread and establishes no new mathematics and no
  new numerics.
* **It does not certify leg 205's battery.** §4.3 found two of its 32 OKs to be accidental
  passes on rank-deficient fits. The battery is used as a *differential* instrument, which is
  valid precisely because both columns run through it.
* **It does not certify that the moving artifact leaves ought to move.** It establishes only
  that **0** of the movement is attributable to the repair — strictly weaker, and the statement
  the gate asks for.
* **It does not re-open leg 307's two-scale verdict or leg 335's `spike1_stepC_gate`
  adjudication.** Both are *pinned* by tests at the values those legs left them, so a future
  change surfaces as a test failure rather than a silent drift.
* **It does not repair the census drift, nor leg 221's registry.**

## 10. The independence ledger

Independence is the point of this leg, so reuse is enumerated rather than implied. Three things
are reused, each with a stated cost:

| reused | why it could not be avoided | what the reuse costs |
|---|---|---|
| **Leg 205's 81-case battery**, read verbatim out of `origin/leg/205-bvr-v1` | it *is* the object under verification | nothing for the differential — the same battery runs against both modules, so a battery bug cancels — but this leg does **not** certify that the battery is a good battery |
| **Leg 221's banked registry** (6 artifacts), as amended by leg 335 | the registry defines what "banked pre-repair" means | the one real dependency: if leg 221's grep missed a pre-repair caller, this leg inherits the miss. §8 item 3 bounds the exposure without eliminating it |
| **`spike1_stepC_gate`'s `--steps 2500`** (leg 335's correction) | the banked artifact records `steps: 2500` | none for correctness; it makes this leg's total legitimately **exceed** leg 221's 256 233, reported as +84 000 rather than smoothed |

Everything else — shim, probe, classifier, flattener, comparison rule, artifact restore,
census, staleness fingerprints, transition matrix and its adjudication — is written in this leg
and imports nothing from leg 221.

Two controls deliberately **not** run, stated so a successor is not misled: leg 221's separate
`baseline_rerun` attribution control (unnecessary here — the shim executes the pre-repair
trajectory, so leaf drift is non-attributable *a priori*), and any check of whether the moving
leaves *should* move (a live question about this repo's reproducibility, not this leg's gate).

## 11. Reproducing the claims

```
.venv/bin/python experiments/p2_route_bvrrv_v1_postrepair_evidence.py   # 45/45, rebuilds fig101
.venv/bin/python writeup/build_figures.py                               # fig101 among the rest
```

Neither re-runs the sweeps. The runner that produced the JSON,
`experiments/p2_route_bvrrv_v1_postrepair.py`, costs ~1.9 h wall four-way parallel and is the
only thing that touches the modules.
