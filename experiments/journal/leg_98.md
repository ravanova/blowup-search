# Leg 98 — Route-ICA v1: adversarial fabrication-rejection audit of `interval_certificate.py`

**Branch** `leg/ica-v1`. **Exploration leg (standard), CLAIM-BEARING** (soundness of the
L1-step-one certificate pipeline).
**Gate: YES — a fabrication-rejection gap, the same shape as leg 79's finding in the sibling
pipeline.** Escalated with maximum urgency. **Nothing was patched**: `solver/interval_certificate.py`
is read-only for this leg under every gate outcome, and the repair belongs to a bench-repair
agent under the orchestrator's authority, exactly as legs 69, 66 and 79 were handled.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is NEXT. Every live ban noted; **none binds this leg** — it
   builds no gCLM measurement, no Route-D bound sharpening, no DSS re-ask, no GA compute, no new
   ℓ¹-Fourier machinery, and it adds no mathematics at all. The ban that *did* apply is *"build
   nothing without grepping `capabilities.py` first"* — done; the module's entry is at line 157
   and the claim under audit is its own summary line, *"`interval_constants` and a conservative
   `radii_verdict`"*.
2. `DIRECTION.md` — leg 98 entry present at line 1584, read in full; thesis, gate and territory
   match the dispatch prompt verbatim.
3. `writeup/novelty/leg_79.md` — read in full before starting, as instructed, since this leg is
   that leg's question aimed at the other pipeline.
4. **Novelty pass FIRST**, committed before any construction (commit `ac57551`,
   `writeup/novelty/leg_98.md`), four verbatim queries, **links not counts**.
5. Then: battery runner, curated data, permanent regression test, findings.

## What the novelty pass changed about the leg

It supplied the **standards**, and there are two of them, one more than leg 79 had.

* **(H1) the theorem's.** `Y_0`, `Z_1`, `Z_2` are upper bounds on norms in the published radii
  polynomial theorem (Hungria–Lessard–Mireles James; van den Berg–Lessard), hence finite and
  nonnegative *by hypothesis*. So "negative `Y_0`" is not a matter of taste, it is **outside the
  hypotheses of the imported result** — a decidable predicate.
* **(H2) the arithmetic's.** IEEE Std 1788-2015 carries a dedicated **`ill`** decoration for
  ill-formed intervals, precisely so a `lo > hi` or NaN-endpoint input cannot be silently
  consumed. That converts "reversed interval" from an opinion into a *published conformance
  requirement*, and it also means detecting one is **bookkeeping, not a discovery**.
* It also pre-emptively removed the methodological novelty claim: adversarial fault injection
  with a soundness/completeness partition is standard (Arguzz, arXiv:2509.10819).

## What was actually measured

**39 cases in two families**, against the `BorderedCLM` (a=0 CLM, bordered) substrate at
`n = 101`, `N = 103`, weight `θ = (0, 0, 0, 0, −2)` (ν ≡ 1, `w_l = 10⁻² X_max`, `w_ω = 1`).
Deterministic, ~4 s, no solver sweep.

Positive controls first, so no gate below is satisfiable by a pipeline that refuses everything:
at the converged Newton iterate the honest certificate **closes** with `Y_0 = 1.396e-11`,
`Z_1 = 2.754e-09`, `Z_2 = 7.993e+05`; displaced by `1e-3` it **does not**, at
`Y_0 = 5.907e-03` — a separation of **4.23e+08×**.

| magnitude | value |
|---|---|
| cases | 39 |
| hypothesis-violating (H1/H2/H3) | 36 |
| **accepted as `closes=True` anyway** | **12 (33.3% of the 36)** |
| of those, **load-bearing** (the same-magnitude hypothesis-*satisfying* input does NOT close) | **8** |
| correctly rejected | 20 |
| raised an exception (a refusal, but a loud one) | 4 |

"Load-bearing" is the severity measurement and it is a number, not a label: for every finite
poisoned triple the battery also evaluates `radii_verdict(|Y₀|, |Z₁|, |Z₂|)` and records whether
*that* closes. If it does not, the hypothesis violation is exactly what bought the certificate.

## The failing cases, precisely

**Downstream — `radii_verdict` accepts constants outside the theorem (this is leg 79's finding,
in the other pipeline, unrepaired).**

| case | input | verdict | why it is wrong |
|---|---|---|---|
| `B04` | `Y₀ = −1.0, Z₁ = 0.3, Z₂ = 1.0` | **closes**, `r_min = −0.8780` | `Y₀ = +1.0` does **not** close (budget `0.2450`). A negative `Y_0` enlarges the discriminant, and the reported radius interval starts at a **negative** radius. |
| `B06` | `Y₀ = −1e6` | **closes** | same mechanism, six decades further out |
| `B07` | `Z₁ = −5.0` | **closes** | `Z₁ < 0` passes the `Z1 < 1.0` guard |
| `B08` | `Y₀ = 1e3, Z₁ = −1e6` | **closes**, budget `5.000e+11` | a negative `Z₁` inflates `(1−Z₁)²/(2Z₂)` without bound and **rescues an arbitrarily large `Y_0`**; `Z₁ = +1e6` rejects it |
| `B17` | `Y₀ = −inf` | **closes**, `r_min = −1.341e+154` | and `Y₀ = +inf` **is** refused — the asymmetry is the tell that the guard is arithmetic, not a hypothesis check |
| `B25` | `Y₀ = −1e-30, Z₁ = 1−1e-16` | **closes** | the `+1e-30` counterpart (`B24`) does not |
| `B05`, `B22` | small negative `Y₀`/`Z₁` | closes | accepted, but the magnitude counterpart closes too — **not** load-bearing |

**Upstream — `interval_constants` never checks the enclosure it is handed.**

| case | input | verdict | why it is wrong |
|---|---|---|---|
| `A1` | an enclosure object reporting `F(z) ≡ [0, 0]` at `z_bad` | **closes**, `Y₀ = 7.9e-323` | the true residual there is `5.907e-03`; the fabricated constant is **~320 decades** below it and nothing notices |
| `A6` | the honest enclosure **scaled by 1e-8** | **closes**, `Y₀ = 5.907e-11` vs honest `5.907e-03` | **the sharpest case in the battery.** This interval is *perfectly well formed* — `lo ≤ hi`, all endpoints finite, positive width — so every validity check that exists, including leg 69's, passes it. It simply does not contain the residual. Only a **containment** check catches this; no amount of interval-validity checking can. |

**Norm data — the weight vector is taken on trust too (H3).**

`A11`: `w → −w` is accepted as a norm and produces `Y₀ = −2.463e-28`, which `radii_verdict` then
closes. This is the one **end-to-end** path in the battery from structurally valid enclosures to
a hypothesis-violating constant. `A12` (a single negative component) is accepted as well, though
inertly.

**The mild one.** `B20`/`B21`: `Z₂ = 0` and `Z₂ = −0.0` raise a bare `ZeroDivisionError` from
inside the verdict function. A crash is a refusal, so this is not unsound — but `Z₂ = 0` is what
an exactly linear system gives, and a caller with a broad `except` converts it into a silent skip.

## What HELD, and it matters

Three checks are real and are now pinned so they cannot regress:

* **NaN is handled correctly, 4/4.** `radii_verdict`'s guard is written `if not (Z1 < 1.0)`,
  which is NaN-safe by construction, and the downstream `bool(r_min < r_max)` is `False` for NaN.
  This is exactly the hazard that defeated the sibling pipeline before leg 79's repair, and this
  pipeline does *not* have it.
* **`Interval.__init__` refuses `lo > hi`** — leg 69's validity repair, still holding, and now
  demonstrated to cover this pipeline's residual path as well. It is the reason the two
  negative-width poisoned-residual cases (`A2`, `A3`) raise instead of lying.
* **A Jacobian enclosure poisoned to the identity, or with swapped endpoints, or with a NaN
  entry, is rejected** (`A7`–`A10`) — the `Z_1` path is much harder to fool than the `Y_0` path.

## Blast radius — why this is a latent gap, not a wrong banked number

**No banked result in this repository is shown to be affected**, and the reason is structural,
not statistical. Every in-repo caller of `radii_verdict` (`experiments/p2_route_l1_v1_interval.py`,
`p2_route_ka_v1_kawahara.py`, `p2_route_tn_v1_consistency.py`, `kawahara_certificate`, and
`test_interval_certificate.py`) feeds it constants that came from `interval_constants`, and there
`Y₀ = max(w · mag(·))` and `Z₁`, `Z₂` are weighted row-sum bounds over magnitudes — nonnegative
whenever `w > 0`. The shipped weight is built as `exp(clip(·))`, so it is strictly positive by
construction. The unsound inputs are therefore **reachable only by a caller that constructs
constants some other way, or hands in a fabricated enclosure object** — which is precisely the
trust boundary an audit is for, and precisely the state `port_certification.py` was in before
leg 79.

The scoping is the same shape as leg 69's: a real defect, correctly located, with no live number
behind it today. What it removes is the *guarantee*. `radii_verdict` is a public function whose
`closes` field is read as the verdict of the whole L1 step-one certificate; today that field is
`True` for 12 out of 36 inputs the imported theorem says nothing about.

## Deliverables

* `experiments/p2_route_ica_v1_adversarial.py` — the battery runner (39 cases, two families plus
  the weight supplement), with the pre-committed failure predicate in its docstring.
* `writeup/data/p2_route_ica_v1_adversarial.json` — every case with the constants produced and
  the r-interval reported, so the verdict arithmetic is re-checkable without rerunning anything.
* `test_interval_certificate_adversarial.py` — 14 permanent gates: **1 CONTROL**, **5 HOLDS**
  (never regress these), **7 GAP-PINs** (the defect, pinned; **invert them when the guard lands,
  do not weaken them** — each names its own inversion), and the banked-total reproduction gate.
* `writeup/novelty/leg_98.md` — the pre-construction novelty log.

## Recommended repair (NOT performed under this leg's authority)

Mirror the sibling's repair, which is already written and tested in
`solver/port_certification._hypothesis_violations`:

1. `radii_verdict` rejects non-finite or negative `Y₀`/`Z₁`/`Z₂` **before** evaluating any
   discriminant, with a distinct reason string (the sibling uses `INVALID_INPUT`).
2. `Z₂ = 0` returns a structured non-closing verdict naming the degeneracy instead of raising.
3. `interval_constants` validates `w`: strictly positive, finite.
4. **The one that is not in the sibling**: `interval_constants` re-evaluates `F` in float at `z`
   and refuses an enclosure that does not contain it. Case `A6` shows this is the only check that
   catches a well-formed non-containing enclosure — validity checking, however thorough, cannot.

Gates 7–13 of `test_interval_certificate_adversarial.py` are written so the repair flips them,
and each docstring states the assertion the repaired code should carry.

---

## STATUS UPDATE (2026-08-06, leg 0 bench repair — this leg's report is left as written)

**The repair has landed on `bench/fix-interval-certificate-validation`, and it followed all
four recommendations above.** Leg 98's report is deliberately unedited: it is the record of the
pre-fix measurement, and the numbers in it are the numbers that motivated the repair.

* **12/36 false accepts → 0/36**, 8 load-bearing → 0. Same 39 cases, same judgement predicate;
  the battery is the instrument that measured the defect and now measures its absence. The
  pre-fix totals are carried in `experiments/p2_route_ica_v1_adversarial.PRE_FIX_MEASUREMENT`
  and written into the JSON under `history.pre_fix`, so regenerating the artifact cannot erase
  the finding. Post-fix split: 29 rejected, 7 refused with an exception.
* `radii_verdict` gained `_hypothesis_violations`, the same check leg 79's repair put in the
  sibling, and **returns** `closes=False` / `reason: INVALID_INPUT` rather than raising —
  recommendation 1, in the sibling's own shape. Raising would have converted the NaN and
  infinity paths, which this leg measured as *already correct 4/4*, from a sound refusal into
  an exception; those are HOLDS gates and they are untouched.
* `Z_2 = 0` returns a structured non-closing verdict naming the affine degeneracy —
  recommendation 2. No mathematics was added: the affine case is refused, not certified.
* `interval_constants` refuses a `w` with negative components — recommendation 3, narrowed on
  purpose to the *negative* case. Zero and NaN components are left to drive `Z_1` non-finite as
  they do today, because that path is already sound, is pinned as a HOLDS gate, and a weight
  can underflow to zero legitimately mid-sweep.
* `interval_constants` re-evaluates `F` in float at `z` (new `F_float` on all three enclosure
  classes) and refuses an enclosure that does not contain it — **recommendation 4, the one that
  is not in the sibling**, and the only thing that catches case A6.
* **The one thing this leg could not have known**: exact componentwise containment of the float
  residual FAILS on honest data (40/103 components at BorderedCLM n=101), because the float
  evaluation of `F` is itself noisy — this repository's own lesson 86, `residual_floor`. The
  check is therefore made in the `Y_0` currency with a measured slack of `1e4`: honest data
  never exceeds ratio 1.0 (0.038–1.000 across BorderedCLM n=101/201/401 and Kawahara N=250),
  and this leg's sharpest lie sits at 1.0e+08. It is a screen against order-of-magnitude
  fabrication and is documented as one, not as a proof of containment.
* **Blast radius as this leg scoped it, re-verified independently and confirmed: LATENT.** Leg
  61's Kawahara known-answer gate certifies **bit-identically** before and after
  (`Y_0 = 3.02425170856154917e-17`, `r_min_Hl = 6.76981691313455990e-15`,
  `r_max_Hl = 2.61929080131872404e-02`, 17 significant digits on every constant), and all 18
  gates of `test_interval_certificate.py` print byte-identical output. No banked number moves.
