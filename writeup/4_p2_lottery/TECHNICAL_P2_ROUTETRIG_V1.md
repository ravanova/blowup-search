# TECHNICAL — Route-TRIG (leg 392, unit T2): the periodic (`T³`) rigidity literature

**Lane T · WAVE 1 · CONDUCTOR §3g · branch `leg/392-t2-periodic-rigidity`**
Artifacts: runner `experiments/p2_route_trig_v1.py`, data `writeup/data/p2_route_trig_v1.json`,
evidence `experiments/p2_route_trig_v1_evidence.py` (41/41 checks, rebuilt from the JSON alone,
no re-run), novelty `writeup/novelty/leg_392.md`, journal `experiments/journal/leg_392.md`.
**No figure** — a pure-literature scoping leg declares one rather than inventing one (legs 334,
348); `writeup/build_figures.py` is untouched by this leg.

**CEILING: TIER 2.** No `L1 → L4` link moved — a literature search does not move one, in either
branch. **Clay stays ~0.05%.** `CLAY_OBLIGATIONS.md` §6's two no-method obligations stay **OPEN**;
leg 390 measured that the torus does not retire them and nothing here changes that.

---

## 1. The gate, and the answer

> **GATE (final wording, pre-registered, not re-scoped).** Does the search locate a **published
> theorem** excluding a finite-time singularity for 3D Navier–Stokes on `T³` of the shape Lane T
> would need — a periodic/torus analogue of the Nečas–Růžička–Šverák / Tsai rigidity results?

**ANSWER: no such theorem was located — and under `ORCHESTRATION.md` §3d that null is returned as
`UNDER-RESOURCED`, not as `no`.**

The arXiv arm executed **100 %** of its planned query set with every control firing, and its zeros
are genuine measured zeros. The Semantic Scholar arm — the only instrument in scope that reaches
the venue class the ℝ³ originals themselves live in — executed **3 of 8** queries and was
**throttled on 5**. One battery failed its own pre-registered domain control. Both facts are
stated in §4 and neither is smoothed over, so the honest verdict on the gate is a cost, not a
verdict. §3d is explicit that this is the case where `UNDER-RESOURCED` is the answer.

**This is reported per the pre-committed reading's branch (c) and is NOT a clearance.** Leg 348's
ceiling clause governs: *absence of a positive instance is not a proof of impossibility.* The
result is **"not excluded by anything located, with the search's coverage stated"** — never
*"clear"*, and it does **not** advance Lane T.

**Which pre-committed branch fired:** **(b)**, in its literal wording — see §5. **(a) did not
fire**: no `T³` theorem covering self-similar or asymptotically self-similar objects exists to
narrow with, because none was located at all. **(c)** governs the reporting of the null.
**(d)** is honoured and raised in §7.

---

## 2. The instrument, controlled before it was trusted

Leg 387 fabricated a controlled zero: its harness listed opensearch namespace `1.0` while arXiv
serves `1.1`, so it refused every response, and a `len(entries)` implementation would have
reported *"0 results, no prior art"* on the exact question it existed to answer. That is why this
leg's verdict is a committed runner rather than a paragraph.

| control | query | measured | required | passed |
|---|---|---|---|---|
| `pos_broad` | `all:"Navier-Stokes"` | **10759** | ≥ 1000 | ✓ |
| `pos_topic` | `all:"Liouville theorem"` | **628** | ≥ 100 | ✓ |
| `neg_nonsense` | `all:"quasiperiodic rigidity of the Zlatohorsky enclosure torus"` | **0** | = 0 | ✓ |
| `and_pair` | `all:"Liouville theorem" AND all:"Navier-Stokes"` | **29** | > 0 | ✓ |
| `and_pair_b` | `all:"Navier-Stokes" AND all:"torus"` | **234** | > 0 | ✓ |

**5 of 5 passed.** The AND verdict is therefore *"AND WORKS — an ANDed zero below is a MEASUREMENT
(absence)"*, which is the precondition for reading anything at all off a zero.

**The leg-387 defence returned a number.** The namespace **actually served**, recorded from the raw
feed on all 32 substantive queries, is `http://a9.com/-/spec/opensearch/1.1/`. The hazard leg 387
fell into is real, it is `1.1` against the `1.0` that harness listed, and this parser names no
version anywhere (regex on `opensearch:totalResults`).

**`MEASURED` vs `DID-NOT-MEASURE` is structural, not editorial.** `total` is `None` by construction
in every `THROTTLED` and `FAILED` record, so a non-measurement cannot be silently rendered as a
zero downstream — including by a reader of the JSON who never saw this document.

---

## 3. What was measured

**arXiv, 32 substantive queries in 8 batteries, ≥ 12 s spacing:**
**32 MEASURED (100 %), 0 THROTTLED, 0 FAILED, 244 total results, 119 distinct ids inspected at
abstract level, 5 MEASURED zeros.**

The five measured zeros, each with the AND operator demonstrated working and the nonsense control
at exactly 0:

| query | total |
|---|---|
| `all:"Navier-Stokes" AND all:"torus" AND all:"Liouville"` | **0** |
| `all:"Navier--Stokes" AND all:"torus" AND all:"Liouville"` (MF1, LaTeX double hyphen) | **0** |
| `all:"three-torus" AND all:"Navier-Stokes" AND all:"regularity"` | **0** |
| `all:"Type I blowup" AND all:"periodic"` | **0** |
| `all:"Morrey" AND all:"torus" AND all:"Navier-Stokes"` | **0** |

The direct form of this leg's question — *Liouville/rigidity × Navier–Stokes × torus* — returns
**zero in both spellings**, on an instrument whose AND operator is demonstrated live and whose
nonsense control is demonstrated dead.

**Semantic Scholar: 3 of 8 MEASURED, 5 THROTTLED (HTTP 429).** Its two controls passed
(`Navier-Stokes equations` → 149 086; the nonsense phrase → 0) and one substantive query returned
(`Morrey space Liouville theorem Navier-Stokes` → 1 117 hits, every inspected hit **steady-state**
and on `ℝ³`, none periodic). The remaining five substantive queries did not measure and are banked
as `THROTTLED` with `total = None`.

---

## 4. The coverage, stated as §3d requires

**What was covered.**

* 100 % of the planned arXiv query set, every query `MEASURED`, all five controls passing.
* The **domain positive control** — pre-registered at journal §0.3 as *the query set must re-find
  the ℝ³ rigidity papers this repository has already screened* — re-found **2 of 3**:
  `2607.09619` (Pineau–Vicol, row 2) ✓ and `2006.15776` (Jiu–Wang–Wei Morrey, row 4) ✓.

**What was not, and each of these is a real hole.**

1. **The domain control FAILED on one arm.** `1304.7414` (Chae–Tsai, row 3) was **not re-found by
   any of the 32 queries.** Under the leg's own pre-registered rule, battery `E`'s null is
   therefore `UNDER-RESOURCED` and is not reported as absence. *The control fired adversely and is
   reported, not retired.*
2. **Row 1's own sources are invisible to this instrument, and it was declared in advance.**
   Nečas–Růžička–Šverák (Acta Math. 176, 1996) and Tsai (ARMA 143, 1998) are **pre-arXiv**. An
   arXiv-first pass cannot see the venue class in which the ℝ³ originals were published — so it
   cannot see a periodic analogue published the same way either.
3. **Semantic Scholar, the instrument for exactly that gap, was 5/6 throttled on its substantive
   queries.** This is the single largest coverage deficit in the leg.
4. **No MathSciNet / zbMATH / Crossref query**, because the pre-committed reading names arXiv and
   Semantic Scholar and nothing else. Recorded as a scope limit, not as absence in the field.
5. **Top-8 truncation.** 9 of the 32 queries returned more than the 8 records fetched (largest:
   `"discretely self-similar" AND "periodic"` at 33), so those batteries were inspected only at
   arXiv's own top-8 relevance ordering.
6. **Abstract-level reading only.** No PDF or LaTeX source was fetched this leg.
7. **No outreach** (standing user hold), so (D)'s data conditions **(8)** and **(9)** remain
   unread — see §7.

**Cost of the compliant search** (§3d requires a cost, not a verdict):

| step | what it closes | cost |
|---|---|---|
| Re-run the 5 throttled Semantic Scholar queries with a key / 60 s spacing | the published-venue gap, incl. pre-arXiv journals | ≈ 0.2 h |
| Repair battery `E` (author/title queries for Chae–Tsai) until the domain control re-finds `1304.7414` | row 3's null | ≈ 0.2 h |
| Forward-citation pass on NRS 1996 / Tsai 1998 / Chae–Wolf, filtered for torus/periodic | the highest-yield instrument this leg did **not** have; a periodic analogue would almost certainly cite one of them | ≈ 0.5–1 h (needs the S2 citations endpoint, i.e. a key) |
| Depth beyond top-8 on the 9 truncated queries | the truncation limit | ≈ 0.3 h |
| A review database (MathSciNet / zbMATH) | the venue class neither API indexes well | **needs a user ruling**, outside the pre-committed reading |

Total ≈ **1.2–1.7 h** plus one user ruling. **That is what it would cost to convert this
`UNDER-RESOURCED` into a defensible `no`, and it is cheap.**

---

## 5. What *was* located — the branch-(b) class, quoted verbatim

Branch **(b)** of the pre-committed reading fires on its literal wording: *"a located theorem
covering a BROADER class — any bounded-energy periodic solution under a scaling-invariant
smallness or regularity hypothesis — bites Lane T directly, and the lane must state what class
survives before anything is built."* Such theorems exist, they are published, and they are on the
torus. **They are not analogues of NRS/Tsai** — they exclude a singularity *under a hypothesis*
rather than for a self-similar object class — which is why they do not make the gate a `yes`
under the pre-registered K1–K4 rule (K4: *the hypothesis class is one a Lane T ansatz would have
to sit in*, and none of them is).

**(b-1) `arXiv:1909.09125` — Nonlinearity **33** (2020) No. 10, DOI `10.1088/1361-6544/ab9246`.
PUBLISHED.** *Global regularity for solutions of the three dimensional Navier-Stokes equation with
almost two dimensional initial data.* Hypothesis and conclusion, verbatim from the abstract:

> "we will prove a new result that guarantees the global existence of solutions to the
> Navier--Stokes equation in three dimensions when the initial data is sufficiently close to being
> two dimensional … the closer the initial data is to being two dimensional, the larger the
> initial data can be in $\dot{H}^\frac{1}{2}$ while still guaranteeing the global existence of
> smooth solutions … **On the torus, however, this approach does give examples of arbitrarily
> large initial data in the endpoint Besov space $\dot{B}^{-1}_{\infty,\infty}$ that generate
> global smooth solutions to the Navier--Stokes equation.**"

**Which hypothesis a Lane T ansatz would have to violate:** *"sufficiently close to being two
dimensional"*, measured in the critical spaces `Ḣ^{1/2}` / `Ḃ^{-1}_{∞,∞}` — i.e. the ansatz's
genuinely-3D part must exceed this theorem's threshold at the initial time.

**(b-2) `math/9811161` — Electronic J. Differential Equations **1999** no. 11, 1–19. PUBLISHED.**
*Global regularity of the Navier-Stokes equation on thin three dimensional domains with periodic
boundary conditions.* Verbatim:

> "the solution of the Navier-Stokes equation on a thin 3 dimensional domain with periodic
> boundary conditions has global regularity, as long as there is some control on the size of the
> initial data and the forcing term, where the control is larger than that obtainable via ``small
> data'' estimates."

**Which hypothesis a Lane T ansatz would have to violate:** the **thin-domain** aspect ratio
together with the size control on data and forcing. On a fixed, non-degenerate `T³` the theorem
simply does not apply — but a Lane T construction that gains its concentration by squeezing one
period would run straight into it.

**(b-3) `arXiv:2009.07631` (preprint, no journal ref)** — *On Ladyzhenskaya-Serrin condition
sufficient for regular solutions to the Navier-Stokes equations. Periodic case*: "We consider the
Navier-Stokes equations in a bounded domain with periodic boundary conditions … The aim of this
paper is to prove the bound $\|V(t)\|_{H^1}\le c$ for any $t\in\mathbb{R}_+$", under a smallness
hypothesis relative to a large-bulk-viscosity Lamé system. **Recorded as a preprint, not as a
published theorem**, and the gate's word is *published*.

**(b-4) `arXiv:0710.1604` — Dynamics of PDE **4** (2007) 293–302. PUBLISHED.** Not an exclusion —
it is the sharpest available statement of *what an unconditional torus result would have to be*:

> "this qualitative question is equivalent to the more quantitative assertion that there exists a
> non-decreasing function $F: \R^+ \to \R^+$ for which one has a local-in-time *a priori* bound
> $\| u(T) \|_{H^1_x((\R/\Z)^3)} \leq F(\|u_0\|_{H^1_x((\R/\Z)^3)})$ for all $0 < T \leq 1$".

**A Lane T ansatz is exactly a refutation of that `F`.** This is the cleanest formulation of the
target and it is on the torus, in the source's own words.

**What survives, stated before anything is built, as branch (b) requires.** On `T³`, nothing
located excludes a blow-up ansatz that is, at its initial time, (i) not small and not almost-2D in
`Ḣ^{1/2}`/`Ḃ^{-1}_{∞,∞}`, (ii) not on a thin torus below (b-2)'s control, (iii) not in a
Ladyzhenskaya–Prodi–Serrin class up to the singular time — automatic for a genuine singularity but
it must be *stated*, not assumed — and (iv) a counterexample to (b-4)'s `F`. **That is the whole
of the located constraint, and it is a weak one: every clause of it is a region a blow-up ansatz
would be outside of anyway.** The bite branch (b) anticipated is real in shape and thin in
substance, and this leg reports the magnitude rather than the shape alone.

---

## 6. The four §2 rows: what has no periodic counterpart, i.e. what Lane T must establish de novo

This is the gate's no-branch deliverable. Row verdicts are per battery, each with its own control
status; **none of the four has a located periodic counterpart.**

| § 2 row | ℝ³ record | battery | domain control | verdict |
|---|---|---|---|---|
| **1. NRS 1996 / Tsai 1998** | `solver/dssp_screen.py` `ledger_nrs_tsai()` | `B` | row 1's sources are **pre-arXiv, unreachable, declared in advance** | **no counterpart located — UNDER-RESOURCED** |
| **2. Chae–Wolf / Pineau–Vicol** | `p2_route_pvlx_v1.json` | `D` | `2607.09619` **re-found** ✓ | **no counterpart located — measured null** |
| **3. Chae–Tsai** | `p2_route_ctrx_v1.json` | `E` | `1304.7414` **NOT re-found** ✗ | **UNDER-RESOURCED — the battery failed its own control** |
| **4. Morrey (Jiu–Wang–Wei)** | `p2_route_mryx_v1.json` | `F` | `2006.15776` **re-found** ✓ | **no counterpart located — measured null** |

**Two of the four rows are partly *vacuous* on `T³`, not merely unproved, and the distinction
matters for what Lane T must build.**

* **Row 1's object does not exist on `T³`.** The theorem constrains exactly backward self-similar
  profiles, and the dilation action defining them does not descend to `ℝ³/ℤ³` — leg 390's check_B
  measured the consequence (342 modes survive one DSS step at `λ = 1.7`, **zero** survive two). So
  a "periodic NRS/Tsai" is not a translation of a theorem; it is a **different theorem about a
  different object class**, and naming that class is Lane T's `T3` work, not a lookup.
* **Row 4's hypothesis partly degenerates.** The Morrey condition read from the landed record is
  `sup_{R>0} sup_x [R^{3(1/p−1/l)} ∫_{B_x(R)}]^{1/l}`; on a compact `T³` the large-`R` half of that
  supremum saturates, so the scale-invariant content of the hypothesis is not what it is on `ℝ³`.
  **This is an observation for the successor, not a measured result of this leg**, and it is
  flagged as such.
* **Row 2 is the sharp one, and it is the single most useful line in this leg.** A **Type I**
  condition is a *rate* condition — `|u| ≲ (T−t)^{−1/2}` — and it needs **no dilation symmetry** to
  state. It therefore carries to `T³` intact as a *question*, and **no torus Type-I rigidity
  theorem was located** (`all:"Type I blowup" AND all:"periodic"` = **0**, measured; the single
  `Type I × NS × torus` hit is a 2D data-assimilation paper). **A Type-I rigidity theorem on `T³`
  is meaningful, absent from the located literature, and is precisely what a Lane T ansatz would
  have to survive or evade.** That is the de novo item this leg names.
* Row 3's counterpart cannot be spoken to at all: its battery failed its control.

---

## 7. Located, adjudicated elsewhere, and load-bearing for Lane T: `arXiv:2604.09949`

The search surfaced, by **two independent queries** (`self-similar × Navier--Stokes × torus`, and
`finite time singularity × Navier-Stokes × torus`), the only located claim of a finite-time
singularity for 3D NS on `T³`:

> **`arXiv:2604.09949`** — *Stable Finite-Time Singularity Formation for 3D Navier–Stokes via
> 5D-Lifted Axisymmetric Reductions*: "a 5D-lifted analytic-profile program for finite-time
> singularity formation in the 3D incompressible Navier--Stokes equations on the periodic torus
> $\T^3$ … a computer-assisted Newton--Kantorovich validation based on interval arithmetic …
> reconstructed into a nearly self-similar singular evolution and then transferred to $\T^3$ by
> periodic extension and exact Leray projection."

It fails the gate's K3 (its conclusion is **existence**, not exclusion) and it is **not new to this
repository** — grepped before being called anything, per leg 348's own correction. It is already
at legs 303, 309, 323 and in `solver/target_selection.py`. **Leg 309 read it at full text and its
gate answered NO**: it breaks at `H11`, because its `T³` object is built from an exact backward
self-similar core on `ℝ³` — *"exactly the object Nečas–Růžička–Šverák prove must be trivial"* —
and transferred by periodic extension.

**The consequence for Lane T is the most useful thing this leg found, and it is stated as a
correction routed to the Conductor rather than applied here.** `WALLS.md` records that **0 of 4
rigidity clearances carry to `T³`**. That is true and it is about *clearances*. The converse is
**not** recorded and leg 309 already demonstrated it: **the ℝ³ exclusions still reach a `T³` object
whose core is an ℝ³ self-similar profile carried over by periodic extension.** The screen is not
void on the torus — it is void as a *source of clearances* while remaining live as a *source of
kills* against exactly the cheapest way to build a torus target. **The one previous attempt at
Lane T's target, by anyone, died that way.** Lane T's `T3` unit inherits this as a hard constraint:
a non-DSS ansatz must not be a periodization of an ℝ³ self-similar core, and leg 390's check_B
already says the DSS route cannot be one anyway.

---

## 8. Corrections routed to the Conductor, verbatim, applied nowhere by this leg

1. **`WALLS.md`, LANE T, "The price" bullet 1** currently reads *"this repository has never
   searched the periodic rigidity literature (leg 390 §5 item 2)"*. After this leg it has, at the
   coverage stated in §4. **Suggested replacement is a record of the result, not a clearance:**
   *"searched at leg 392 (arXiv 32/32 MEASURED, Semantic Scholar 3/8, one battery's domain control
   failed): no periodic analogue of any of the four rows was located, and the verdict is
   `UNDER-RESOURCED`, not `no`."*
2. **`WALLS.md`, LANE T, same bullet, needs the converse added:** *"0 of 4 clearances carry to
   `T³` — but the ℝ³ exclusions DO reach a `T³` object built by periodic extension of an ℝ³
   self-similar core (leg 309 killed `arXiv:2604.09949` on exactly that ground)."*
3. **(D)'s data conditions (8) and (9) are still UNREAD**, they need outreach, the standing hold
   forbids it, and **the hold therefore sits on Lane T's critical path.** This leg **raises this
   rather than routing around it**, exactly as its pre-committed reading (d) requires. Nothing in
   this leg assumes anything about their content.
4. **Row 4's Morrey hypothesis partly degenerates on a compact `T³`** (§6). Flagged as an
   observation for a successor with a measurement, not as a result of this leg.

---

## 9. What this leg does not claim

* It does **not** claim Lane T is clear. It claims *nothing located excludes it*, with the
  coverage above. Branch (c) of the pre-committed reading is explicit that these are different
  statements, and the difference is the whole discipline.
* It does **not** advance Lane T. A null here is not a permission.
* It does **not** retire `CLAY_OBLIGATIONS.md` §6's two no-method obligations. They stay **OPEN**,
  leg 390 measured that the torus does not retire them, and this leg does not write otherwise.
* It moves **no** link of the `L1 → L4` chain. **Clay stays ~0.05 %. Ceiling TIER 2.**
