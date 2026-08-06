# Route-BX v1 — stage `B`, answered from the banked record: the closure audit

**Stage `B`, leg 126. Gate answer: NO.** Data: `writeup/data/p2_route_bx_v1_stageb.json`.
Runner: `experiments/p2_route_bx_v1_stageb.py`. Ledger renderer (no recomputation):
`experiments/p2_route_bx_v1_stageb_evidence.py`. Novelty pass: `writeup/novelty/leg_126.md`,
run and committed **before** any construction.

> **Gate, in its pre-committed wording.** *Auditing stage `B`'s full declared search space
> (space × split × constants/shape, plus the fitness route) against the banked record (legs
> 49, 52, 53, 54, 56, 58, 59, 111): does any admissible, ban-respecting configuration remain
> that no banked measurement or theorem covers — i.e. a corner in which a searched
> certificate could still close on this operator?* — **NO.**
>
> The no-branch fires as written: *`B`'s own gate ("does the searched certificate beat the
> hand-tuned one?") answers its pre-committed NO in the only sense that matters: nothing in
> the searchable space closes — the floor is proved ≥ 1 on `A21 = 0`, measured `8.9591` at
> best anywhere, and the fitness that would steer a search is dead as parameterized. Write
> the honest report `B`'s deliverable names, quantifying how much of the difficulty was
> tuning versus structure (the structure share is now theorem-grade).*

> **NO FIGURE, BY DESIGN.** The yes-branch would have measured a corner and registered
> `fig62`. The no-branch measures none, and the repository's Route-D convention ("no
> measurement, no figure") applies. The deliverable is a ledger.

> **NO GA COMPUTE RAN, ON EITHER BRANCH.** The ban lifts only on a frozen six-property gate
> that PASSES; it has failed twice (§4). The runner imports no `ga/` module and calls neither
> `solver.ga_search` nor `solver.weight_search.grid_search`.

---

## 0. Why stage `B` could be answered but not run

`B` is the last `QUEUED` stage in the committed sequence. Its `why_here` is sound — hand-tuning
a function space (Route-D, eleven legs) and hand-picking preconditioners (Routes K, L) are
search problems with a fitness that cannot lie. What changed is that the eight legs which ran
while `B` waited each closed one of its doors, none of them aiming to:

| `B`'s degree of freedom | closed by | how |
|---|---|---|
| the function **space** | legs 52, 55 | repair works at `s = 0`/`0.3`, fails at `s = 1`/`1.5`; target's `ℓ¹_w` norm finite only below `s ≈ 0.394` |
| the operator **split** | leg 53 | coupling entry `K/2` for every choice; `K = 4…64` bottoms at the smallest `K`, `43.15` |
| the **constants / shape of `A`** | legs 54, 58 | battery over seven shapes bottoms at `8.9591` (`1.167×`, `>8×` needed); then **proved** impossible on `A21 = 0` |
| the **fitness** that steers a search | legs 49, 59 | frozen six-property gate `4/6`, then `5/6` with P3 unmoved to sixteen digits |
| the **realization** | legs 56, 111 | collocation defect `1.8537e7×`/`2.0403e11×` over budget; weighted-`L²` admissible window of **zero** width |

The remaining question is not whether `B` can be *run*. It is whether anything is *left* in it.
That is a completeness audit, and it can answer either way.

---

## 1. `BX1` — the declared space, enumerated before any covering check

The three axes are quoted verbatim from `plan_of_record.py`'s stage-`B` entry (`name`: *"the
function space, the operator split, the constants"*). Two further axes are declared by the same
entry's prose rather than its title, and are audited on the same footing: the **search
mechanism** (`why_here`: *"those are search problems with a fitness that CANNOT LIE"*) and the
**realization** (`why_here` names Routes D, K and L — three different ones).

| axis | values |
|---|---|
| `realization` | `l1_fourier`, `collocation`, `weighted_L2` |
| `s` (weight exponent) | `0.0, 0.3, 0.7, 1.0, 1.5` |
| `K` (split) | `2, 3, 4, 6, 8, 16, 32, 64` |
| `split_location` | `standard`, `far_field_in_tail` |
| `A21` | `zero`, `nonzero` |
| `shape` | leg 54's seven |
| `search` | `hand`, `grid`, `GA` |

**`μ` is not an axis.** `B` evolves the certificate around the object stage `M` named, not the
object. `μ` is held at `0` for every enumerated configuration and appears only as `BX3`'s
control.

Two consistency reductions are applied at enumeration rather than left to be silently covered:
`A21` is a function of `shape` (asserted from each shape's construction in leg 54's `build_A`,
checked numerically in leg 58's `NG2b`), so inconsistent pairs are dropped; and the non-`ℓ¹`
realizations carry no `K`, split placement or shape of `A`, so they are audited once each
rather than once per irrelevant axis value. **1,686 configurations** survive.

---

## 2. `BX2` — the clauses, and what kind of coverage each provides

Coverage is typed, because "proved impossible" and "we tried it" are not the same claim:

- **THEOREM** — a proof; the configuration cannot close, as mathematics.
- **STRUCTURAL** — an admissibility or well-posedness failure; not a legal certificate at all.
- **MEASURED** — tried over a named battery, did not close. Coverage, but not proof.
- **BAN** — a live `plan_of_record.py` entry with an unmet lift condition.

| id | leg | type | headline magnitude |
|---|---|---|---|
| `SPACE-TARGET` | 55 | STRUCTURAL | `target_alpha = 0.394` (margins `+0.394` at `s=0`, `+0.094` at `s=0.3`) |
| `SPACE-CROSSING` | 51 | STRUCTURAL | kernel exponent `−2.0024`, cokernel `+1.0012`, crossing `1.0` |
| `SPLIT-ODD` | 54 | STRUCTURAL | smallest sv `2.031e-16` at odd `K` vs `8.090e-3` at even |
| `SPLIT-ALT` | 58 | MEASURED | alternative-split tail inverse norm `292.57` |
| `SHAPE-THM` | 58 | **THEOREM** | proved floor `Z₁ ≥ 1`; in-class min column `6.0424` |
| `SHAPE-BATTERY` | 54 | MEASURED | best admissible `8.9591` vs baseline `10.4584` (`1.1674×`) |
| `SHAPE-GENERAL-A` | 54 | MEASURED | general-`A` floor `5.0444`; counter-construction total `Z₁ = 5.658e5` |
| `SHAPE-CREDIT` | 58 | MEASURED | `A21 ≠ 0` credit `0.9451…0.9990`, deficit ≤ `0.0549` |
| `SEARCH-BAN` | 49 | BAN | P2 `0.775 → 0.975` vs floor `0.90`; P3 `0.3656` vs ceiling `0.05`; `4/6 → 5/6` |
| `SEARCH-DEAD` | 59 | MEASURED | P3 `0.3656` (leg 49) `→ 0.3421493449940881` (leg 50) `→ 0.3421493449940881` (leg 59), ceiling `0.05` |
| `REAL-COLLOC` | 56 | MEASURED | defect/`τ` = `1.8537e7` (derivative), `2.0403e11` (Hilbert) at `n = 801`, `τ = 2.3056e-14` |
| `REAL-ENERGY` | 111 | MEASURED | largest admissible gap `−0.4999`, window width `0` |

**Every clause is scoped to `μ = 0`**, because every one of them was measured or proved on the
inviscid operator and none says anything about `μ > 0`. That scoping is not cosmetic; §3 is how
it was found.

**One reading note on the fitness clauses**, because the "unmoved" claim is easy to mis-attribute.
P3's worst `|slope − 1|` went `0.3656` (leg 49) → `0.3421493449940881` (leg 50's 1-D wall) →
`0.3421493449940881` (leg 59's 2-D wall). The *unmoved to sixteen digits* comparison is leg 50 →
leg 59: leg 59's repair moved P2 (`0.875 → 0.975`, clearing the `0.90` floor and taking the gate
from `4/6` to `5/6`) and left P3 bit-identical. Against leg 49 the total movement in P3 is
`0.0235`, against a ceiling that needs it at `0.05` — i.e. the quantity a search would steer on
responds to the probe **window's** width, not to the genes a search would vary (leg 59's
Spearman of window width against slope error: `−0.8779`).

### Result

**1,686 enumerated / 1,686 covered / 0 uncovered.** By strongest coverage: **144 THEOREM,
1,032 STRUCTURAL, 510 MEASURED**.

---

## 3. `BX3` — the controls, including the one that caught a tautology

### 3a. Instrument check

Leg 54's two headline numbers, recomputed read-only through its own landed
`assemble`/`build_A`/`measure` at `(algebraic, s=0.3, gauge=null, K=2, M−K=1024)`:

| quantity | recomputed | banked | rel gap |
|---|---|---|---|
| `block_diag` `Z₁` | `10.458427` | `10.458427` | `0.00e+00` |
| `ff_lift` `Z₁` | `8.959091` | `8.959091` | `0.00e+00` |

Bit-identical. Every leg-54 magnitude quoted here is therefore quoted against a reproducing
instrument.

### 3b. The positive control — and the bug it found

A covering predicate that cannot return NOT COVERED is a tautology of the code presented as a
finding (**lesson 90**). The control is the `μ > 0` operator, where a certificate demonstrably
closes: the predicate is **required** to return NOT COVERED there.

**It did not.** The first draft returned *covered* on every dissipative configuration, because
**not one of the twelve clauses referenced `μ`** — each silently claimed authority over an
operator its evidence had never seen. Scoping all twelve to `μ = 0` is simply writing down what
they measured, and it is what makes the audit falsifiable.

**A second realization bug, caught by the same control.** The first dissipative measurement
returned `Z₁ = 5904.13` against leg 58's banked `0.1740` — a factor of **33,927**. The
repository's standing rule is to suspect the control's *realization* before the banked number,
and it was right: the draft bordered the `μ > 0` object with the analytic far-field direction,
as the inviscid object is bordered. A dissipative tail is **already invertible** and has no
far-field kernel to border — the wrong operator, not the wrong answer. Rebuilt as leg 58's
`NG3` built it (`K = 16`, `border = None`, `far_field = False` for `μ > 0`), the control
reproduces leg 58's **entire twelve-entry dial elementwise to `1.25e-15`**.

| `μ` | class | shape | `Z₁` | closes | covered by |
|---|---|---|---|---|---|
| 0.0 | flat | `block_diag` | `1021.599028` | no | `SHAPE-THM`, `SHAPE-BATTERY`, `SHAPE-GENERAL-A` |
| 0.0 | flat | `gs_upper` | `318.778416` | no | idem |
| 0.0 | algebraic | `block_diag` | `549.450556` | no | idem |
| 0.0 | algebraic | `gs_upper` | `146.235992` | no | idem |
| 2.0 | flat | `block_diag` | `1.137176` | no | **NOT COVERED** |
| 2.0 | flat | `gs_upper` | `0.514935` | **yes** | **NOT COVERED** |
| 2.0 | algebraic | `block_diag` | `0.666349` | **yes** | **NOT COVERED** |
| 2.0 | algebraic | `gs_upper` | `0.402579` | **yes** | **NOT COVERED** |
| 4.0 | flat | `block_diag` | `1.035111` | no | **NOT COVERED** |
| 4.0 | flat | `gs_upper` | `0.229979` | **yes** | **NOT COVERED** |
| 4.0 | algebraic | `block_diag` | `0.519460` | **yes** | **NOT COVERED** |
| 4.0 | algebraic | `gs_upper` | `0.174027` | **yes** | **NOT COVERED** |

All four inviscid rows covered; all eight dissipative rows uncovered; six of them close. **The
predicate discriminates.**

**Honest reading, recorded with the control.** `μ > 0` is a *different operator*, not a corner
of stage `B`'s declared space. Reaching it means re-opening stage `V`, whose ban lifts only if
the question is re-posed for a fluid transport model — which needs `L1` first, and `L1` is dead
in both realizations. The control's job is to prove the predicate can say no. It is not a lane.

---

## 4. `BX4` — the space axis is a partition, with no gap

The space axis is the one place a coverage gap could hide, because it is a continuum and the
banked measurements sit at five points. It does not hide there, because the covering clauses
are **regions, not points**:

| region | status | covered by |
|---|---|---|
| `0 ≤ s < 0.394` | ADMISSIBLE | `SHAPE-THM` (theorem, `A21 = 0`) + `SHAPE-BATTERY` / `SHAPE-GENERAL-A` / `SHAPE-CREDIT` (measured, `A21 ≠ 0`) |
| `0.394 ≤ s < 1.0` | INADMISSIBLE | `SPACE-TARGET` — the target leaves its own space |
| `s ≥ 1.0` | INADMISSIBLE | `SPACE-TARGET` **and** `SPACE-CROSSING` — target out of the space, and the tail kernel leaves it exactly as the cokernel functional enters the dual |

Disjoint, and they exhaust `[0, ∞)`. **Gap: none.** The two boundaries are independently
banked: `0.394` is leg 55's measured admissibility exponent (leg 54 carries it as
`target_alpha`), and `1.0` is leg 51's Fredholm crossing, re-measured by leg 58's `NG2a` as
`−2.0024`/`+1.0012` with increment ratios `0.9988` (log-divergent) at `s = 1` and `1.9974`
(power-divergent) at `s = 1.5`.

---

## 5. `BX5` — a coverage gap and a proof-strength gap are different objects

One gap is real and it is named. Leg 58's theorem covers `A21 = 0`. The three **admissible**
shapes with `A21 ≠ 0` — `ff_lift`, `gs_lower`, `schur` — are covered by measurement and by no
theorem. (`oracle_pinv` and `exact_inv` also have `A21 ≠ 0` and are excluded: leg 54's own
`ADMISSIBLE` map marks them inadmissible because they invert the *truncated* operator, making
their `Z₁` a statement about `numpy.linalg.inv` — leg 54's `MM3` minimum over the admissibility
audit is `1.03e4`.)

This is a **proof-strength gap**, not a **coverage gap**, and the gate asked specifically for a
corner in which a searched certificate *could still close*. This one is measured not to:

| magnitude | value |
|---|---|
| best admissible `Z₁` anywhere in the class | `8.9591` |
| general-`A` floor on the kernel direction (`MM4`) | `5.0444` |
| ceiling on what `A21 ≠ 0` can buy back | `1.0` unit |
| max credit actually measured (`NG2d`) | `0.99903` |
| cost of cancelling the column (`MM4c`) | total `Z₁ = 5.658e5` |
| required | `< 1` |

What is missing is proof strength over an infinite class, not an untried configuration — and
that question is already routed: `DIRECTION.md` leg 127 (Route-NGX) is exactly it, queued as
**exploration, explicitly not the critical path**. Stage `B` does not need it to answer.

An earlier draft derived this class from "strongest coverage == MEASURED" and got it wrong: that
also picks up the `A21 = 0` shapes under the `far_field_in_tail` split placement, whose covering
clause `SPLIT-ALT` happens to be a measurement. The gap is a property of the `A21` **axis**, and
is now read off that axis.

---

## 6. `BX6` — tuning versus structure, which is what `B`'s no-branch actually owes

> *"A negative bounds how much of the difficulty was tuning versus structure, which is worth
> knowing either way."* — `plan_of_record.py`, stage `B`, `gate.if_no`

The requirement is multiplicative (`Z₁ < 1`), so the scale is decades of `log₁₀ Z₁`, on which
improvement factors subtract. Anchors: baseline `10.458427` (block-diagonal), best over the
whole battery `8.959091`, measured in-class floor `6.042396`, required `1`.

| quantity | decades | share of the requirement |
|---|---|---|
| **required** (baseline → `Z₁ = 1`) | `1.019466` | 100% |
| delivered by **tuning** | `0.067202` | **6.5919%** |
| searchable headroom left **unrealized** | `0.171055` | **16.7789%** |
| owned by **structure** | `0.781209` | **76.6292%** |

The three shares sum to `1.000000000000` by construction and are asserted to do so.

Two readings follow, and both are worth stating:

1. **There was real unexplored search space.** Tuning reached only **28.21%** of its own
   ceiling. Stage `B` was not proposing to search an empty box.
2. **It would not have mattered.** A *perfect* search — saturating every available decade —
   lands at `Z₁ ≥ 6.0424`, still **6.04× short**.

**MEASURED-grade caveat.** The `6.0424` floor is the minimum `ĥ`-column over leg 58's in-class
battery: a measurement, not a proof. It is the sharpest floor the repository can defend by
evidence, so the accounting above is MEASURED-grade throughout.

**PROVED-grade accounting, on `A21 = 0`.** Sharper, and covers less. The proved floor is
`Z₁ ≥ 1` while the certificate requires `Z₁ < 1`. The searchable headroom is exactly **zero
decades** and **structure owns 100%** of the difficulty — as a theorem rather than as a battery.
This is the sense in which "the structure share is now theorem-grade".

---

## 7. What is *not* claimed, and why the wording is narrow

The novelty pass is load-bearing on this point. Automated certificate synthesis is published as
**sound but not complete** (arXiv:2309.06090 / *Annual Reviews in Control* 2025): a found
certificate proves the property, but a search that fails to find one licenses **no conclusion**
about the model. Where completeness exists it comes from a **converse theorem** for the
certificate class, and those results are explicitly non-constructive — and no converse theorem
exists for the radii-polynomial class here.

Therefore this leg does **not** claim "no certificate exists". The claim is exactly:

> **The declared search space of stage `B`, as this repository declared it, is covered clause by
> clause by the banked record: 1,686 of 1,686 configurations, none uncovered.**

That is exhaustion of a **named enumeration**. It is not a statement about the mathematics
outside that enumeration. Separately, **leg 52's search-index flag STANDS** — untested and
uncleared by this pass.

---

## 8. Gate conditions

| condition | value |
|---|---|
| `instrument_reproduces_leg54` | `True` (rel gap `0.00e+00`, both) |
| `positive_control_discriminates` | `True` |
| `positive_control_reaches_below_one` | `True` (`Z₁ = 0.174027`) |
| `space_axis_is_a_partition_with_no_gap` | `True` |
| `every_enumerated_configuration_is_covered` | `True` (1,686 / 1,686) |
| `no_GA_compute_ran` | `True` |
| `shares_sum_to_one` | `True` |

**Conditions failed: none. Gate answer: NO.**

---

## 9. Ceiling, pre-committed

Bookkeeping on a measured negative. The object is the `a = 0` CLM linearisation, whose `Y₀` is
**exactly zero** because the anchor *is* one basis mode (clause `S7`), so every magnitude here
bounds `HL_S2_nonsymmetric`'s difficulty **from below, not above**. Closing `B` is not movement
on `L1 → L4`: **no link of the chain moved under either branch, and none has moved in 125
legs.** Clay odds unchanged at **~0.05%**.

Per the gate's no-branch, the orchestrator applies `B`'s pre-committed no-branch and the
committed sequence is **EXHAUSTED**. What enters next is escalation #1, for the user, framed by
Open question #3 — leading candidate the `γ = 2` dissipative certificate route, contingent on
leg 125's gate. That is the user's decision, not this leg's, and nothing here presumes it.
