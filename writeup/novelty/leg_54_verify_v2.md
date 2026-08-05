# Leg 54 — VER-A2 independent review of `leg/mm-v1` (HEAD `b9fb069`)

**Reviewer:** VER-A2, branch `verify/mm-v1-review`. **Scope:** leg 54's own construction and
PR, reviewed from scratch. Distinct from VER-A (`verify/mm-headline`, unmerged), which
re-measured *leg 53's* headline before leg 54 built on it.

**Bottom line.** **The gate answer NO is correct and robust** — I re-derived it independently
and it survives every probe I ran, including one the leg did not run. **But the leg's headline
number is wrong**, and two of its load-bearing arguments are stated more strongly than the
algebra supports. **Recommend: fix, then merge.** Not merge as-is.

---

## 1. What I confirmed independently

**Bit-for-bit reproducibility.** Re-ran `experiments/p2_route_mm_v1_shape.py` from a clean
checkout. The regenerated JSON differs from the shipped one in **exactly one field**,
`elapsed_s`. Every substantive number reproduces byte-identically.

**MM-2's headline arithmetic, re-derived from hand-built block matrices** (not read from the
JSON, not via `build_A`): I assembled `L = [[G,B],[C,T]]` and the Schur `A` by hand and formed
`I − AL` myself.

| quantity | leg's JSON | my hand-build |
|---|---|---|
| `schur` `Z₁` (alg. `s=0.3`, null, `K=4`) | 32.74889495071105 | 32.7488949507 |
| `block_diag` `Z₁` (same cell) | 45.36284244157659 | 45.3628424416 |
| `Z₁[Γ←tail]` (leg 53 instrument check) | 43.15129110858924 | 43.1512911086 |
| `Z₁[tail←Γ]` (leg 53 instrument check) | 1.387314691515264 | 1.3873146915 |
| improvement factor | 1.385171698460368 | 1.3851716985 |

**MM-1 is an exact equality.** Re-derived the RHS from `wfun` and `A_t` directly:
`max |ratio − 1| = 1.887e-15`, matching `1.887379141862766e-15`. The `K=2` vacuity is real —
RHS is *exactly* `0.0` in both classes while the measured quantity is `4.9e-04` / `2.0e-03`.
Thresholds confirmed: RHS first clears 1 at **`K=6` flat**, **`K=4` algebraic`**. *Note:* flat
`K=4` gives `0.99611` — the `K≥6` threshold hangs on a 0.4% margin. Correctly read, but thin.

**MM-1b odd-split singularity — confirmed, and it is genuinely exact.** Built the augmented
finite block myself at `K = 2…9`, both classes, and took SVDs: `σ_min ≈ 1e-17…1e-18` at every
odd `K`, `σ_min ≈ 1e-2…1e-1` at every even `K`. Not ill-conditioning; singularity.

**MM-4's floor values.** Reproduced `5.044374` (alg. `K=2`), `7.0078125` (flat `K=2`),
`23.0703125` (flat `K=4`). The **identity itself is correct**: with `T ĥ = 0`,
`(I − AL)_{Γ,tail} ĥ = −A₁₁ B ĥ`, so `A₁₂` does drop out. Corroborating evidence the leg did
not cite: `oracle_pinv` at alg./null/`K=2` measures `5.139`, sitting just above the `5.044`
floor.

**MM-4b defect.** `‖Tĥ‖/‖ĥ‖ = 1.46e-02` at `M−K = 1024`, edge-only, halving per doubling —
all confirmed via the test gate's own ladder (`5.86e−02 → 2.93e−02 → 1.46e−02 → 7.32e−03`).

**Hygiene.** `test_spectral_certificate.py` **26/26 pass**, including both new leg-54 gates.
`test_plan_of_record.py` all gates pass. `fig49` rebuilds from the curated JSON alone.
Novelty pass is properly done — run before construction, verbatim queries, **links not
counts**, `PROCEED_NARROW`, nothing banked as novel.

**Territory: clean.** Ten files, all inside declared territory. **None of the five shared
ledgers touched.** `capabilities.py` untouched and correctly so — `solver/spectral_certificate.py`
is already indexed (line 136, with `test_spectral_certificate.py` as its test). *Note for the
orchestrator:* contrary to the review brief, this leg **does not modify
`solver/spectral_certificate.py` at all** — all new code is in `experiments/`. The one-line
`writeup/build_figures.py` edit is the standard figure registration.

---

## 2. GAP 1 — the headline number is wrong (material; must fix)

**MM-2's shape battery sweeps only `K ∈ {4,8,16,32,64}`.** `K = 2` and `K = 6` were added to
`K_SWEEP_SMALL` in response to VER-A's correction — but `K_SWEEP_SMALL` is used **only by MM-1
and MM-4**. The battery, which is where the gate answer is computed, still runs the old
`K_SWEEP`. So does MM-6's polynomial.

I ran the leg's own `assemble`/`measure` at the omitted splits, same conventions
(`border="analytic"`, `norm="shipped"`, both gauges, both classes):

```
  flat      s=0.0 null     K= 2: block_dia=12.42  gs_upper=11.41  schur=11.41  ff_lift=11.07
  algebraic s=0.3 null     K= 2: block_dia=10.46  gs_upper=9.566  schur=9.565  ff_lift=8.959
  algebraic s=0.3 null     K= 6: block_dia=96.47  gs_upper=55.11  schur=55.10  ff_lift=94.95
  flat      s=0.0 dilation K= 2: block_dia=514    gs_upper=20.02  schur=19.78
  algebraic s=0.3 dilation K= 2: block_dia=89.21  gs_upper=17.32  schur=17.11
```

**Best admissible `Z₁` at `K ∈ {2,6}` is `8.9591`** (algebraic `s=0.3`, null gauge, `K=2`,
`ff_lift`) — **not `32.7489`**. Consequences:

* `headline/smallest_Z1_over_every_admissible_shape_class_gauge_and_split = 32.7489` and
  `gate_smallest_Z1_admissible` are **false as worded**. The true value over every admissible
  split is `8.96`.
* The block-diagonal baseline is likewise mis-minimised: `10.46` at `K=2`, not `45.36`.
* `MM2_improvement_over_block_diagonal = 1.385` is computed on the restricted sweep. At `K=2`
  it is `10.46 → 8.96 = 1.17×`.
* The framing in both writeups — *"a factor of ~1.4 where ~45 was needed"*, the blog's
  *"45.4 → 32.7"* and *"roughly forty times too small"* — should read roughly
  *"10.5 → 9.0"* and *"roughly nine times too small"*.

`K=2` is not a corner the leg can decline: **the leg itself treats it as admissible**, sweeps
it in MM-1 and MM-4, calls it *"the most favourable split that exists"*, and MM-1b's own
conclusion (*"the split must be EVEN"*) admits it. `K=2` is also the **best-conditioned** split
(`σ_min = 0.269`).

**This is the same error class VER-A already caught once** — a sweep starting at `K=4` hiding
the small-`K` corner — reproduced in a different clause after being fixed in two others.

**It does not change the gate answer.** `8.96 ≫ 1`; no positive interval appears at `K=2`.

---

## 3. GAP 2 — MM-4's floor is not shape-independent (over-claim; must fix)

The identity is right. The **floor** is over-stated. `A₁₁` is part of the shape of `A`, and it
is not pinned by anything the leg checks.

The leg's hedge is that *"`A₁₁` is not completely free (the `(Γ,Γ)` block needs
`A₁₁G + A₁₂C = I`)"*, ablated over two realisations. **That constraint does not pin `A₁₁`.**
Solving it gives `A₁₁ = (I − A₁₂C)Γ⁻¹`, hence `A₁₁ B ĥ = (I − A₁₂C) v` with `v = Γ⁻¹B ĥ` the
floor vector — and since `A₁₂` is free, choosing rank-one `A₁₂ = v wᵀ/(w·Cv)` kills `v`
outright. I built it:

| | alg. `K=2` | alg. `K=4` | flat `K=2` | flat `K=4` |
|---|---|---|---|---|
| leg's floor | 5.0444 | 13.7426 | 7.0078 | 23.0703 |
| my `A₁₁`, same constraint | **7.8e−16** | **7.8e−16** | **2.2e−16** | **3.7e−15** |
| `(Γ,Γ)` block of `I−AL` | 1.2e−16 | 1.3e−15 | **0.0** | **0.0** |

The `(Γ,Γ)` constraint is satisfied *exactly* and the floor is beaten by fifteen orders of
magnitude. The leg's two-point ablation cannot see this because both its `A₁₁` choices are
≈`Γ⁻¹` (they agree to `3.3e−03`), so it varies nothing.

`TECHNICAL §8` **does** disclaim this correctly (*"not finite-block-independent — it contains
`A₁₁`"*). But `§4`'s own summary, the JSON key `headline/shape_independent_floor`, the
`verdict` string, and the blog's *"no shape of `A` can get below that floor. Not the seven I
tried; any of them"* all assert more than the algebra gives. Since the review brief describes
MM-4 as closing the gate *"decisively regardless of any future shape choice"* — **it does
not**, and that reading must not propagate into the plan.

**Mitigating, and why the conclusion survives:** my construction makes the *overall* `Z₁`
catastrophically worse — `5.7e+05` to `4.0e+06` — because `‖A₁₂‖` runs `1.1e+03…7.2e+03` and
wrecks every other tail column. So the floor's **conclusion** holds empirically even though
its **proof** does not. What MM-4 actually establishes is: *for `A₁₁` in the neighbourhood of
`Γ⁻¹`, the coupling along `ĥ` is `≥ 5.04` and no `A₁₂/A₂₁/A₂₂` can touch it.* That is still a
good result. It is not the universal one claimed.

---

## 4. GAP 3 — the defect argument is not quantitatively sound as written (must fix)

MM-4b argues the `O(1/M)` defect is negligible because *"1.46e−02 relative, against a floor of
5.04"*. **That compares a relative defect to an absolute floor.** The term that must actually
be bounded is `‖A₁₂(Tĥ)‖ ≈ ‖A₁₂‖ · ‖Tĥ‖`, and `‖A₁₂‖` is nowhere bounded. Measured:

| shape | `‖A₁₂‖` | `‖A₁₂(Tĥ)‖` | vs floor |
|---|---|---|---|
| `schur` | 8.03 | 0.0007 | 0.000× |
| `gs_upper` | 8.03 | 0.0007 | 0.000× |
| `oracle_pinv` | 1237 | 13.7426 | **1.000×** |
| `exact_inv` | 618.5 | 6.8713 | **0.500×** |

(algebraic `s=0.3`, `K=4`; flat `K=2` behaves identically.) **The leg's own battery contains
two shapes where the truncation defect exactly cancels the floor** — `oracle_pinv` to the last
digit. Indeed `exact_inv`'s coupling along `ĥ` measures `1.5e−14`, not `≥13.74`.

**Answering the brief's question directly: no, this does not flip the sign of the conclusion.**
For every *admissible* shape actually measured, `‖A₁₂‖ = O(10)` and the defect term is `7e−04`
against floors of `5`–`23` — utterly negligible. The two shapes where it bites are inadmissible
and are independently killed by MM-3's audit (`1.03e+04`). But the sentence as written is
unsound and should be restated with the `‖A₁₂‖` factor visible.

---

## 5. GAP 4 — MM-1b's stated mechanism is not what the matrix shows (should fix)

The **fact** is solid. The **reason** given is not. MM-1b says: *"at odd `K` the mode-`K`
residual row acquires no entry on any of `b_1…b_K` or `δc_ω` and is carried entirely by the
amplitude column."* Inspecting the matrix actually built:

* at `K=3`: **two** rows have zero mass off the amplitude column (0-based rows 2 and 4), and
  the left null vector is supported on **exactly those two** — they are proportional, hence
  singular. A single such row would not be enough.
* at `K=5`: only **one** row has zero mass off the amplitude column (row 6), yet the block is
  still singular, and the left null vector is supported on rows **2, 4 and 6** — a parity
  *chain*, not one row.
* rows with zero mass off the amplitude column exist at **even** `K` too, where the block is
  nonsingular. So the stated criterion does not discriminate.

The parity intuition is directionally right; the one-row statement is not what the matrix
does. This is the same failure mode the standing discipline flags from leg 53 (*"a growth rate
you cite must be measured on the matrix you actually built"*). Cheap to fix — the left null
vector's support is the mechanism, and it is one `svd` call away.

---

## 6. Judgment on the two self-flagged weaknesses

**Weakness #1 — the border control does not discriminate for `schur`. Honest orthogonal
weakness; it does not undermine the headline.** The control tests whether the instrument is
sensitive to a deliberately wrong far-field direction. For `schur` it is not, and the leg's
mechanism is correct and checkable: `S = G − B A_tail C` partly undoes what the border did to
`Γ`, so the shape is far less border-sensitive by construction. Three things make this
non-threatening: (i) the negative result does not **rest** on this control — it rests on the
direct measurement and on the `μ`-dial positive control, which *does* discriminate and reaches
`Z₁ < 1`; (ii) the smallest `Z₁` anywhere in the whole border table is `5.2188`, still five
times the bar, so even the "helpful" wrong border does not approach closure; (iii) chasing it
would be tuning the border direction, which is banned and was measured dead in leg 53. **This
is lesson 90 working as intended** — a control that *could* come out differently, did, and was
reported rather than dropped. I would keep it exactly as the leg wrote it.

**Weakness #2 — the `O(1/M)` defect. Negligible, but for the wrong reason.** See §4. The
conclusion is safe by a wide margin for every admissible shape; the *argument* needs the
`‖A₁₂‖` factor made explicit, because as written it is refuted by two rows of the leg's own
battery. **It cannot flip the sign of the conclusion.**

**Neither weakness threatens the gate answer.** The threat I did find is GAP 1, which the leg
did not flag because it did not look.

---

## 7. Is the gate answer NO robust?

**Yes — more robustly than the leg's own argument establishes, and at a different number.**

Over every admissible shape, class, gauge and **every even split including the two the leg
omitted**, the smallest assembled `Z₁` is **`8.9591`**, against the `1` it must be under. Every
route below 1 I could construct is either inadmissible (`exact_inv` `1e−9`, `oracle_pinv`), or
catastrophic elsewhere (my `A₁₁` construction: floor `8e−16`, total `Z₁` `5.7e+05`). MM-3's
admissibility audit independently kills the inadmissible ones at `1.03e+04`. `Y₀ = 0` for the
pre-committed degenerate reason, and no row has a positive interval.

**The orchestrator can safely apply `T`'s no-branch to `plan_of_record.py`.** The gate answer
does not change under any correction I found.

---

## 8. Sign-off

**I would not merge `leg/mm-v1` as-is.** The gate answer is right and the leg's discipline is
mostly exemplary — pre-committed clauses, novelty pass first with links, an instrument check
against leg 53, a correction made *against* its own interest (§3.1), a failed test chased
rather than coded around, and a control reported honestly when it misbehaved. But:

* **GAP 1 must be fixed** — it puts a wrong number in the headline of both writeups, the JSON
  and the gate field, and it is a repeat of the error class already caught once on this leg.
  The fix is mechanical: use `K_SWEEP_SMALL` in MM-2 and MM-6, re-run, restate the headline,
  the improvement factor and the "forty times" framing.
* **GAPs 2 and 3 must be fixed** — both are over-claims in the leg's most load-bearing and most
  novel argument, and GAP 2's wording is what would propagate into the plan as "MM-4 closes
  this regardless of future shape choice." It does not.
* **GAP 4 should be fixed** — one `svd` call; the fact stands either way.

None of these is a repair of the *result*. All are repairs of *what the result is said to be*.
After them, I sign off.

**Unresolved gaps requiring new work: none.** Everything above is correctable inside leg 54's
existing runner and prose.
