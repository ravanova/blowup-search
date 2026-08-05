# Route-M2 v1 (leg 63) — target reselection, screened by the measured predicate

**Branch** `leg/m2-v1`. **Exploration leg, not critical path. Claim-bearing.**
**Gate answered: YES — which is escalation #1. Nothing is promoted; the branch is parked.**
**Data** `writeup/data/p2_route_m2_v1_targets.json`. **Figure** `fig57_route_m2_v1_targets.png`.
**Module** `solver/target_selection.py` (M2 section). **Gates** `test_target_selection.py`.
**Runner** `experiments/p2_route_m2_v1_targets.py` (940 s on a contended box, deterministic —
re-run end to end and every number reproduced identically).

---

## 0. What this leg is, and the two things it may not claim

Stage M picked `HL_S2_nonsymmetric` on defensible grounds, and leg 55 confirmed the object
was never the problem — it sits in an admissible class with coefficients decaying
`k^{-1.396}`. What legs 51–57 refuted is the **method's reach**, and they refuted it with a
predicate sharp enough to screen candidates:

> does the linearization's unbounded part act as a **multiplier** (diagonal in the spectral
> basis — cut the tail at `K` and its inverse **decays**), or as a **shift** (off-diagonal,
> bordered tail inverse a **constant that grows** in `K`)?

This leg re-runs stage M's ledger machinery with that predicate as a **column**.

**It may not claim the screen.** Leg 57 settled that the dichotomy is folklore in print
(Cadiot arXiv:2505.03091 §2 and §3). Using it as a selection column is bookkeeping.

**It may not promote anything.** A YES answer is escalation #1 under ORCHESTRATION §8. The
ledger is scoping. The user decides whether any row enters the sequence, and §6 below states
the constraint that decision runs into.

---

## 1. The dial: the ORDER of the dissipation, not its strength

Leg 57's dial was `mu`, the strength of a `Λ¹` dissipation. That dial cannot screen targets,
because what separates candidate **models** is the *order* of their dissipation. So the tail
block gets a two-parameter diagonal:

```
T[j, j] = -ν k^γ        T[j+1, j] = 1 - k/2        T[j-1, j] = k/2
```

**Containment is gated, not asserted.** At `γ = 1` this is
`spectral_certificate.tail_block(K, M, mu=ν)` **entry for entry** — measured
**max entrywise difference `0.0e+00`** across four `(K, M, ν)` settings. A dial that does not
contain the old one is a new operator, not a generalization, and leg 53 already paid for
quoting numbers from an operator that had quietly changed.

The tail block is tridiagonal, so its inverse is computed by Thomas elimination in `O(n²)`
rather than `O(n³)` — a dense `np.linalg.inv` at `n = 768` costs ~10 s on this box, which
prices the bisection out of existence. The fast path is unpivoted and therefore **falls back
to the dense inverse on any zero pivot**, and it is gated against the dense path across the
dial: **worst relative disagreement `3.0e-15`** over twelve `(ν, γ)` settings.

---

## 2. The predicate curve, and the hypothesis it killed

At `ν = 0.1`, over `γ ∈ [0, 2.4]` in steps of `0.1`, with `K ∈ {4,…,128}` and `M = 1024`:

| `γ` | K-exponent | M-exponent | bordered? | verdict |
|---|---|---|---|---|
| 0.0 | **+0.4372** | +0.997 | yes | SHIFT side |
| 0.1 | +0.4372 | +0.943 | yes | SHIFT side |
| 0.2 | +0.4372 | +0.813 | yes | SHIFT side |
| 0.3 | +0.4372 | +0.547 | yes | SHIFT side |
| 0.4 | **−0.5130** | +0.078 | no | MULTIPLIER side |
| 0.5 | −0.4449 | −0.305 | no | MULTIPLIER side |
| 2.0 | **−2.0270** | ~0 | no | MULTIPLIER side |

**21 of 25 grid points come out multiplier-side, the first at `γ = 0.4`.**

**The hypothesis this leg posed, and lost.** The obvious guess is `γ* = 1`: the transport
off-diagonal grows like `k/2`, so the diagonal `ν k^γ` "should" have to out-grow it. **False,
and by a wide margin.** The bracketed bisection gives

| `ν` | `γ*` |
|---|---|
| 0.01 | **0.824** |
| 0.1 | **0.402** |
| 1.0 | **0.0117** |

A diagonal that is *pointwise far smaller* than the off-diagonal still breaks the recursion
that makes the tail inverse grow. This is leg 57's `δ < 1/2` lesson repeating on a different
dial: **the threshold a size comparison predicts is not the threshold the operator has.**

**And the honest correction to this leg's own framing.** `γ*` moves across nearly two decades
of `γ` as `ν` moves across two decades. "The order decides and the strength only shifts it" is
right in direction and **wrong in magnitude** at this truncation. That is why every
dissipative row is re-screened across `ν` in §4 rather than being quoted at one strength.

**Resolution control (M2-6).** Every headline exponent recomputed at `K ∈ {8,…,64}`, `M = 512`:
differences **0.014, 0.019, 0.035, 0.083** at `(ν, γ) = (0, 0), (0.1, 0.5), (0.1, 1), (0.1, 2)`,
and the predicate **agrees at 4 of 4**. The exponents are resolution-stable to the second
decimal; the verdicts are stable outright.

---

## 3. The ledger, with the predicate column

Stage M's `TARGET_LEDGER` is **not edited** — it records an answered gate, and a test fails if
a later pass writes the new column back into it. M2 adds a parallel layer: stage M's four
uncertified rows (which enter at `γ = 0`, because that is what their models are) plus two
dissipative candidates the predicate makes newly relevant.

| M2 rank | id | `γ` | predicate | K-exponent | blow-up on the model |
|---|---|---|---|---|---|
| 1 | `gCLM_Lambda2_viscous_profiles` | 2.0 | **MULTIPLIER** | **−2.0270** | PROVED (analytic) |
| 2 | `CCF_fractional_subcritical` | 0.5 | MULTIPLIER | −0.4449 | PROVED (analytic) |
| 3 | `gCLM_degenerate_one_scale` | 0.0 | SHIFT | +0.4372 | proved (inviscid) |
| 4 | `HL_singular_steady_stability` | 0.0 | SHIFT | +0.4372 | proved (inviscid) |
| 5 | `HL_S2_nonsymmetric` | 0.0 | SHIFT | +0.4372 | proved (inviscid) |
| 6 | `Boussinesq_S2_nonsymmetric` | 0.0 | SHIFT | +0.4372 | proved (inviscid) |

**The four inviscid rows return the identical exponent `+0.4372`, and that is not a bug.** The
shape is a property of the **operator**, not of the target (lesson 87) — which is exactly what
makes the column computable at all, and exactly what limits it: a row's verdict is a statement
about its dissipation **order**, not about its profile. Every target stage M ever ranked,
including the one the port is aimed at, is on the wrong side of the screen, and they are all
on the wrong side *for the same reason and by the same amount*.

**The ranking rule is pre-committed and predicate-first**, then blow-up provability, then cost.
Cost does not drive it: all four 1D rows share a cost ratio of `5.6e-04`–`1.1e-03` against the
certified object, so the ordering here is entirely the screen's.

---

## 4. The gate

> **"Is there at least one uncertified target, on a model where blow-up is provable, whose
> linearization's unbounded part is a MULTIPLIER under the leg-57 predicate?"**

**YES.** `gCLM_Lambda2_viscous_profiles`, K-exponent **−2.0270**, **2 of 6** rows multiplier-side.

The evidence for the top candidate, in the order it matters:

1. **The model's blow-up is proved.** Chen, arXiv:1908.09385, abstract, quoted verbatim:
   *"We use the method in [chen2019finite] to prove finite time self-similar blowup for `a`
   close to `1/2` and `γ = 2`."* `γ = 2` is the full Laplacian. Analytic, not computer-assisted.
2. **Its unbounded part is multiplier-shaped by a whole power of `k`** — diagonal `ν k²`
   against a `k/2` transport off-diagonal — and the measured K-exponent `−2.0270` is the
   largest-magnitude decay anywhere in either ledger.
3. **It is uncertified.** No computer-assisted certificate of *any* dissipative self-similar
   profile was located (novelty pass Q4): every certificate in this family — Chen–Hou–Huang
   for inviscid De Gregorio/gCLM, Chen–Hou for 2D Boussinesq — is inviscid.
4. **Its tail block needs no bordering.** The whole apparatus legs 52–54 had to build — the
   border row, the border column, the matching condition, the block coupling that then failed
   at `K/2` — is not required here.

**Three limits on that YES, each measured or located rather than hedged.**

* **`ν`-robustness (§4b below).** The rank-2 CCF row sits at `γ = 0.5`, which is above `γ*`
  at `ν = 0.1` and *below* it at `ν = 0.01`. Its verdict is strength-dependent. The rank-1
  row's is not: `γ = 2` clears the largest measured `γ* = 0.824` by a wide margin.
* **Transcription depth.** The blow-up claim is read from an **abstract**, not full text. The
  `a`-neighbourhood is unquantified and the `ν`-dependence unstated in what was read. This
  repository has been burned twice by literature read at the wrong depth; a promotion leg must
  discharge this first, and the JSON says so on the row.
* **What a multiplier-shaped tail does not buy.** A decaying tail inverse removes the
  obstruction that killed legs 51–54. It says nothing about `Y_0` being under budget, which is
  a statement about a *profile* and needs constants this leg deliberately did not transcribe.

### 4b. Robustness across strength

Each dissipative row re-screened across two decades of `ν`:

| id | `γ` | `ν = 0.01` | `ν = 0.1` | `ν = 1.0` | robust? |
|---|---|---|---|---|---|
| `gCLM_Lambda2_viscous_profiles` | 2.0 | −1.8033 | −2.0270 | −1.9589 | **3/3 — yes** |
| `CCF_fractional_subcritical` | 0.5 | **+0.4372** | −0.4449 | −0.4345 | 2/3 — **no** |

The CCF row **flips to shift-side at `ν = 0.01`**, exactly as `γ* = 0.824 > 0.5` predicts, and
its exponent there is `+0.4372` — the same number the four inviscid rows return, because at
that strength the diagonal has stopped buying anything at all. The rank-1 row does not flip at
any strength tried. **The gate's YES does not depend on a fragile row**
(`answer_depends_on_a_fragile_row: false` in the JSON), and that is recorded as a field rather
than as a sentence so it cannot quietly stop being true.

---

## 5. Where the two thresholds leave a window — arithmetic only

Two conditions must hold at once for a dissipative target to be worth anything here:

* the **method** needs `γ > γ*`, or its tail estimate has nothing to decay with;
* the **blow-up** needs the dissipation asymptotically negligible, which
  `solver/fractional_gclm.py` derives (validated against XU eq (6.3)) as `s < s_c = α/2` for a
  `(-Δ)^s` dissipation — i.e. `γ < α` in the `Λ^γ` convention, with `α` the profile's
  far-field decay exponent.

So the window is `γ* < γ < α`. Using `α = -c_ω` from constants **already transcribed in stage
M's ledger** (arXiv:2603.25104 Table 4.1, degenerate `k = 3` branch) — **no gCLM solver was
run; the standing ban on another gCLM measurement leg is live and this is arithmetic**:

| `a` | `α = -c_ω` | open at `γ* = 0.0117`? | open at `γ* = 0.824`? | contains `γ = 2`? |
|---|---|---|---|---|
| 0.1 | 3.8668 | yes | **yes** | **yes** |
| 0.2 | 0.8357 | yes | **yes** (barely) | no |
| 0.232931 | 0.6055 | yes | no | no |
| 0.232932 | 0.6055 | yes | no | no |
| 0.3 | 0.3479 | yes | no | no |
| 0.4 | 0.1718 | yes | no | no |
| 0.5 | 0.0872 | yes | no | no |

**Reading, and its caveat.** The window is real but **narrow and branch-dependent**. Taking
`γ*` at its most generous measured value (`0.0117`) it is nonempty at **7 of 7** values of `a`;
taking it at its worst (`0.824`) it is nonempty at only **2 of 7**, and it contains the proved
exponent `γ = 2` at exactly **one** `a` (`a = 0.1`, where `α = 3.8668`). And the branch these constants come
from is the **degenerate `k = 3`** branch, which is *not* the branch Chen's `γ = 2` theorem is
about — so this is an illustration of how the two thresholds combine, **not** a claim about the
proved object. It is included because it is the cheapest available check that the two
conditions are not trivially incompatible, and it says they are not.

---

## 6. The constraint this leg surfaces and does not decide

**Every multiplier-side row in this ledger is dissipative.** `plan_of_record.py` bans
re-opening stage V as posed, and the ban's lift condition reads:

> *unless the question is re-posed for a FLUID transport model, which needs L1 first*

**L1 is measured dead in both realizations** (legs 51–54). So the only rows the method's own
predicate says it can handle sit behind a ban whose lift condition currently cannot be met.
Three readings are available and this leg picks none of them:

1. the lift condition is about *stage V's question* (viscous survival of an existing
   certificate's margin), and a **new target on a dissipative model is a different question**
   that the ban does not reach;
2. the lift condition binds, `L1` cannot be met, and the dissipative rows are unreachable —
   in which case the ledger's honest reading is that **every reachable row is shift-shaped**
   and the method is exhausted for this repository's target class;
3. the lift condition should be **re-posed** in light of this measurement.

**That is a user call.** It is escalation #1 whichever way it goes: reading (1) promotes a
route into the sequence, and reading (3) rewrites a ban other than via its recorded lift
condition. The constraint is stored in the module as `M2_LIFT_CONSTRAINT` and copied into the
JSON's `lift_constraint`, so it travels with the verdict and cannot be dropped by a summary.

---

## 7. Scope — what this is not

* **Not rigorous.** Float64, no intervals. Every number is a measurement of a matrix.
* **Not a claim that a certificate closes.** That needs `Y_0` under budget.
* **Not a full-text literature result.** Every `blowup` field is transcribed from abstracts and
  surveys, with links in `writeup/novelty/leg_63.md`.
* **Not a per-target linearization.** The predicate is measured on the shared spectral tail
  operator with a dissipation dial; the column is a statement about dissipation order.
* **Not movement on the L1→L4 chain, and not movement on Clay.** The odds stay ~0.05%.
* **Not a promotion.** Nothing entered the sequence. `main` was not touched.
