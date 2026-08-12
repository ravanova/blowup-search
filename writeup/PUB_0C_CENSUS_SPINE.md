# §0c — the census-spine section (PUB track)

**Status.** Publication-track spine section, assembled from banked records. **Not
floor-eligible** — no new mathematics is performed here; every claim below is a citation of an
already-landed leg's own measurement, diffed against that leg's journal or data file, not
paraphrased from memory. **No link of the `L1 → L4` (Clay) chain moves.** Clay odds stay
**~0.05%**, unmoved, behind Walls 1 and 2.

**Assembled by** leg 345 (Route-PUB0C), 2026-08-12, from `origin/main` at commit `5c83f7e`.
**Precondition:** leg 328 (Route-ORC5) landed at `fa1ab94`, closing the closure-#5 register debt
at `writeup/CORRECTIONS.md` §21. That precondition is verified directly (§4 below), not assumed.

---

## 1. The claim, stated at its measured width

**The Grade-A/fluid cell is empty.** Definitions, exactly as this repository's own literature
apparatus (leg 174, `writeup/data/p2_route_vbs_v1_scoping.json::occupancy_matrix`; leg 303,
`writeup/data/p2_route_gaf_v1_sweep.json`) states them:

* **Grade A** — the interval-arithmetic certificate encloses a solution of an equation that
  itself carries the dissipative term (clause (c) below).
* **fluid** — the equation is a genuine fluid-dynamics equation (transport nonlinearity,
  incompressibility or a fluid-adjacent structure), not an off-axis scalar/complex-field model.

**The cell — Grade A *and* fluid, simultaneously — has never been filled by any published
work.** Leg 174's occupancy matrix (`experiments/journal/leg_174.md:51-58`) shows the other
three cells occupied — Grade B/fluid (`arXiv:2208.09445`, Buckmaster–Cao-Labora–Gómez-Serrano,
Forum Math. Pi 13 (2025) e6, a certified inviscid profile with an analytic viscous-transfer
argument) and Grade A/not-fluid (`arXiv:2410.05480`, Dähne–Figueras CGL) — and the Grade-A/fluid
cell alone empty. **This is narrower than "no certified viscous blow-up exists in any model, in
any dimension"** — that wider sentence was FALSE and is the claim closure #5 corrected (§4).

---

## 2. Ground: the target-absence finding (leg 174)

Cited from `experiments/journal/leg_174.md:222-240` verbatim in substance: **"the cell is empty
for want of a TARGET, not for want of a method"** (line 230). The method already exists and is
already Grade-A on a non-fluid dissipative equation — `arXiv:2404.04054` runs
Newton–Kantorovich in a weighted Sobolev space on self-similar profiles of parabolic PDEs
**including viscous Burgers**, banked in this repository's own ledger as `ADJACENT`. What has
never been found in the literature is a **dissipative fluid self-similar profile worth
enclosing**: every certified fluid blow-up profile in the literature is inviscid at the
certified object (`2208.09445`), and every proved viscous fluid blow-up either has no
self-similar profile (Prandtl/Kukavica–Vicol–Wang, Tao's averaged NS) or reaches viscosity from
an inviscid certified profile by an analytic transfer argument (`2208.09445`, MRRS).

This ground is a **literature-only** finding (leg 174's own header: *"no solve, no certificate,
no solver module, no dynamics run"*) and claims no stage in `plan_of_record.py`.

---

## 3. Defense: the claimant refuted (leg 309)

A claimant to the Grade-A/fluid cell was surfaced by leg 303's freshness sweep
(`arXiv:2604.09949`, Shahmurov 2026, banked as *claimed, not filled*) and adjudicated by leg 309
under the pre-committed gate *"does the full text sustain the claim as stated … or does it
break — with the breaking hypothesis quoted?"*

**Gate: NO — it breaks** (`experiments/journal/leg_309.md:11`). The manuscript's own Theorem
12.1, equation (18) — `u(x,t) = (1/√(T*−t))·ū(x/√(T*−t))` — is, verbatim, the definition of an
**exact backward self-similar solution** of 3D Navier–Stokes on `ℝ³`, with the profile space
forcing `ū ∈ L³(ℝ³)` and stronger. **That is exactly the object Nečas–Růžička–Šverák (Acta
Math. 176, 1996) prove must be trivial**, extended by Tsai (ARMA 143, 1998) — a 30-year-old
exclusion theorem the manuscript never cites, engages, or attempts to evade (leg 309 §"The
finding", H11). The break is theorem-level, not an arithmetic slip: every independently
recomputable constant checked out (`K ≈ 1.0998×10⁴`, `C_rec^map` maximizer at `k=2500`
reproducing `2.5652×10⁷` exactly, the NK closure `2δMK ≈ 8.9×10⁻⁵ < 1`, cross-confirmed against
this repository's own **prior, independent** recomputation in
`solver/target_selection.py::ns_preprint_closure_audit()`).

**Consequence, stated in leg 309's own words** (`experiments/journal/leg_309.md:79-85`): *"the
Grade-A/fluid viscous-certification cell stays EMPTY. Leg 303's 'claimed 1' is downgraded to
refuted by this leg's adversarial read; it does not become 'established 0' in the positive
sense — it is simply not a fill."*

---

## 4. Closures carried into this section

### 4a. Closure #5 — the width of the claim, corrected (`writeup/CORRECTIONS.md` §21)

**What was wrong.** `plan_of_record.py` (before correction) stated: *"No certified viscous
blow-up exists in any model, in any dimension, today."* Per the user's external-review packet
of 2026-08-11, this was **FALSE**, refuted by this repository's own banked data: leg 174's
occupancy matrix has `fluid=False, grade=A` **OCCUPIED** by DF-CGL (`arXiv:2410.05480`),
independently reproduced row-for-row by leg 316 (49,465/49,465 rows, zero failures, zero
tiling gaps — `experiments/journal/leg_316.md:42-62`), and Breden–Chu's viscous Burgers is a
second Grade-A dissipative object.

**What the correction narrowed the claim to.** *"What is actually empty, at measured width, is
narrower: the Grade-A/fluid cell — no published work applies interval arithmetic to a
dissipative fluid equation's own self-similar object."* (`writeup/CORRECTIONS.md` §21.1,
quoted verbatim.) **The Phase-1 rationale is unchanged** and never depended on the wider claim:
if it cannot be done for a dissipative fluid equation in 1D, 3D NS is not a question of compute.

**Verification, not assumption, that this closure landed.** `plan_of_record.py:47-55` (this
worktree, read not edited, md5 `a4ece173c3eb890043332127a7d4d900` per leg 328's own §21.4
verification) already carries the corrected wording. Six sites total were named by closure #5;
five are confirmed fixed (two `DIRECTION.md` sites by the DM cycle 6, `plan_of_record.py` and
`CONTINUATION_PROMPT.md` by the orchestrator at `ce74d6b`, `CLAY_ROADMAP.md:343` by leg 328
itself) and the sixth (a `DIRECTION.md` `6.5457e+11` gate-text label) is carried as an immutable
pointer per the DM's own ruling, not edited by any leg (`writeup/CORRECTIONS.md` §21.2–§21.3).

### 4b. Closure #6 — the grounds corrected, the width unchanged (`writeup/CORRECTIONS.md` §17)

**What was wrong.** Three sites (`experiments/JOURNAL.md:4929`, `DIRECTION.md:9683`,
`DIRECTION.md:14892`) carried the phrase *"closed three ways"* describing why the Grade-A/fluid
cell (in the narrower, post-closure-#5 sense) or an adjacent vorticity-route obstruction is
closed, with **no enumeration attached at the point of introduction**. Legs 331 and 332
measured the two candidate triples the record actually supports and found the count did not
survive as stated: **A1 (screen (iv_a)/Remark 40) MISATTRIBUTES its mechanism, A3 (Gallay–Wayne
prior art) OVERSTATES its reach, and only A2 (the NRS/Tsai composition) STANDS AT MEASURED
WIDTH** (`writeup/CORRECTIONS.md` §17.2, Enumeration A); the alternate cell-level reading
(Enumeration B) fares no better (B2 = A1's misattribution, B3 overstates).

**What is corrected, and what is not.** *"WIDTH STANDS, untouched. The Grade-A/fluid cell is
still empty… GROUNDS are corrected. One way misattributes its mechanism, one overstates its
reach, and the triple is not banked at any site that invokes it."* (`writeup/CORRECTIONS.md`
§17.3, quoted verbatim.) **This section therefore states the cell's emptiness without invoking
a "three ways" count** — consistent with lesson 91's catch (a count standing in for a named
realization), which is the defect both closure #5 and closure #6 correct, in different
currencies (over-generalized width vs. an unenumerated triple).

---

## 5. The variant-robust census (leg 323) — the current state of the search, at its own numbers

Leg 323 re-ran the literature instrument (`export.arxiv.org/api/query`) under the corrected,
variant-robust form (dash-shape normalization confirmed on the `abs:` field; a group-name
`au:` false-negative class independently caught and corrected) and applied leg 303's own
four-clause screen — **certificate (a)**, **finite-time blow-up (b)**, **dissipative object
itself, not an inviscid reduction later dominated (c)**, **fluid (d)** — to every hit.

**Gate: NO — the variant re-run surfaces no work the original instrument missed** (beyond
`2604.09949` itself, already adjudicated in §3 above), held in the realization: *the `abs:`
phrase-query layer, over the 12+35 compound query set, single-hyphen vs.
all-terms-double-hyphenated, `max_results=60`, on 2026-08-11*
(`experiments/journal/leg_323.md:12-16`).

**The screen, clause-by-clause, at leg 323's own numbers** (`experiments/journal/leg_323.md`
Part 6, "screening the census hits against the pre-committed candidate criterion"):

| quantity | value | source |
|---|---|---|
| distinct arXiv ids surfaced by the census (Step B + author-conjunction Step C2) | **58** | `leg_323.md:260` |
| of those, absent from both `solver/viscous_novelty.py::PRECEDENTS` and leg 303's result sets | **51** | `leg_323.md:260-261` |
| of those 51, clearing **all four** named clauses (a)+(b)+(c)+(d) at title level | **0 / 51** | `leg_323.md:271` |
| candidates clearing **three of four** clauses | **2** | `leg_323.md:271-286` |

**The two three-of-four candidates, named and adjudicated, not smoothed into the zero:**

* **`arXiv:2310.05325`** (non-radial implosion for compressible Euler/Navier–Stokes, T³ and
  R³) — clears blow-up, dissipative, fluid; already cited in 35 repo files. **Known ground**,
  not a new candidate.
* **`arXiv:1504.02775`** (splash singularities for the free-boundary Navier–Stokes equations,
  Castro–Córdoba–Fefferman–Gancedo–Gómez-Serrano) — clears blow-up, dissipative, fluid, and is
  cited in **0** repo files before this leg. Read at abstract depth, as the pre-committed
  criterion requires: **clause (a), certificate, FAILS** — the abstract states a purely
  analytical existence proof, no computer-assisted proof, no interval arithmetic, no validated
  numerics. Clause (b) is only partial: the breakdown is a **splash** (the free boundary
  self-intersecting in finite time), not a norm blow-up of the velocity field. **Verdict:
  mechanical near-miss** — banked with its link and its adjudication, not counted as a fill,
  exactly as leg 323's own pre-committed criterion requires
  (`experiments/journal/leg_323.md:284-286`).

**Controls, both directions, all five passed** (`experiments/journal/leg_323.md` Part 4,
`controls_pass: true`): the environment-alive control, an ANDed-quoted-phrase positive (a third
independent refutation of the struck MF3 clause, alongside legs 314 and 326), a nonsense-phrase
negative, a known-co-authored `au:` positive, and an unrelated-author `au:` negative. This
section's zero (0/51 clearing all four clauses) is therefore stated as a **measured absence
under an instrument whose controls demonstrably could have come out the other way**, not an
assumed one.

---

## 6. Prior-art map (leg 317) — cite, don't claim

Leg 317's own gate: *"Does any of the two families of measured defect (79/98/116/128/140/142
'Family A'; 202/237 'Family B') survive as literature-novel, under §0a's calibration (expect
folklore, weight toward OLD prior art)?"* **Gate: NO** — the write-up
(`writeup/CAP_SILENT_FAILURES.md`) is **not drafted**, and that is the finding at full strength
(`experiments/journal/leg_317.md:3-4`).

This section follows the same discipline **by citation, not restatement**: it does not draft or
imply a `CAP_SILENT_FAILURES.md`-shaped taxonomy claim anywhere in this document, and the
leg-202/237 mechanism is presented below (§7) exactly as leg 317 characterized it — **known
methodology applied**, not a novel result of this repository.

Leg 317's own prior-art map, banked in `writeup/data/p2_route_sftx_v1.json`, is cited here by
pointer rather than reproduced: **Family A** (hypothesis-violation/fabrication-acceptance in
Y0/Z0/Z1/Z2 constants) is folklore already settled by leg 79's own novelty pass (van den
Berg–Lessard, *AMS Notices* 2015; IEEE 1788-2015 decorations). **Family B** (a scale-invariant
convergence test cannot detect an escape from the scaling family — legs 202/237's mechanism) is
**"the named justification for an entire existing methodology"**
(`experiments/journal/leg_317.md:44`): Beyn–Thümmler's 2004 freezing method for Lie-group
actions including scaling, the pseudo-arclength phase-condition literature post-Keller, and the
dynamic-rescaling/modulation literature for self-similar PDE blow-up (Merle–Raphaël–Martel–Zaag
lineage, 1990s–2000s), plus domain-general numerical-solver folklore (MOOSE, OpenMDAO,
ADMM/Wohlberg) stating the same warning independently of self-similar PDEs at all.

---

## 7. The leg-202/237 mechanism, presented as known methodology applied

**What was measured (leg 202, `experiments/JOURNAL.md:3304-3315`; leg 237,
`experiments/journal/leg_237.md`).** `profile_newton.py::continuation` returned off-branch
grid-scale roots as `converged=True` at machine-zero relative residual — `c(a=1.50) =
0.20427/0.23717/0.97282` at `n = 101/201/301`, all three "converged," 376% apart — because the
convergence test consulted a scale-invariant ratio alone and never the two gauge rows that pin
which family member is returned. Leg 237's class census found exactly **one** other `solver/`
module sharing the same three-criterion defect shape (a scale-invariant sole verdict + no
absolute-scale companion + a genuine scaling degeneracy to escape into) —
`collocation_newton.py::ACollocation.newton` — graded **LATENT and NOT claim-adjacent**: 0/41
adversarial escape attempts across six named routes actually reached the escape, versus 2/2 on
`profile_newton` under the same route at the same resolution (leg 237's calibration control,
`experiments/journal/leg_237.md:138-149`).

**Why this section states it as known methodology, not a repository-original finding.** Per
leg 317's Family B verdict (§6 above): the underlying hazard — a residual criterion measuring
only "did the residual shrink relative to where it started," not "is this the branch I
intended," in the presence of a continuous symmetry (here, a scaling degeneracy) — is the
**named justification for an entire existing methodology already in the literature** (freezing
methods, pseudo-arclength phase conditions, dynamic-rescaling normalization conditions). **What
legs 202/237 contribute is the local application**: locating the specific unguarded verdict
sites in this repository's own `solver/` modules, measuring the specific magnitudes of the
escape (376%, 1000×, up to 999 in absolute gauge defect), and censusing which of the 47
`solver/*.py` files share the pattern (1 of 20 classified verdict sites; 27 modules carry no
convergence/closure verdict at all). **No claim is made here that the mechanism itself is
novel** — leg 317's own adversarial literature pass already closed that question NO.

---

## 8. Constraint checklist, verified clause-by-clause

Every named constraint in this section's thesis, checked against its banked source rather than
asserted:

| # | constraint | verified against | result |
|---|---|---|---|
| 1 | Grade-A/fluid cell is empty, at the corrected (narrow) width | `writeup/CORRECTIONS.md` §21.1 (closure #5); `plan_of_record.py:47-55` read, md5-confirmed unedited | **holds** |
| 2 | The cell's emptiness is attributed to target absence, not method absence | `experiments/journal/leg_174.md:230` (verbatim quote) | **holds** |
| 3 | A claimant to the cell was surfaced and adjudicated, not ignored | `experiments/journal/leg_309.md:11` (gate NO, break quoted) | **holds** |
| 4 | The refutation is theorem-level (NRS/Tsai exclusion), not an arithmetic slip | `experiments/journal/leg_309.md:33-62` (H11; all recomputable constants checked out) | **holds** |
| 5 | The variant-robust census surfaces no missed occupant beyond the already-adjudicated claimant | `experiments/journal/leg_323.md:8-16` (gate NO, realization named) | **holds** |
| 6 | 0 of 51 novel census candidates clear all four named clauses (a/b/c/d) | `experiments/journal/leg_323.md:271` | **holds** |
| 7 | The one 3-of-4 near-miss is named with its failing clause, not folded into the zero | `experiments/journal/leg_323.md:277-286` (`1504.02775`, clause (a) fails) | **holds** |
| 8 | Closure #5's six sites are individually verified fixed or pointer-carried, not assumed | `writeup/CORRECTIONS.md` §21.2–§21.4 | **holds** |
| 9 | Closure #6's "three ways" count is not re-invoked anywhere in this section | this document, §4b (no "closed N ways" phrase used) | **holds by construction** |
| 10 | Leg 317's prior-art map is cited, not restated as an original taxonomy | this document, §6 (pointer to `p2_route_sftx_v1.json`, no `CAP_SILENT_FAILURES.md`-shaped claim drafted) | **holds** |
| 11 | The leg-202/237 mechanism is presented as known methodology applied, not re-derived | this document, §7, against leg 317's Family B verdict | **holds** |
| 12 | No count stands in for a named realization anywhere in this section (lesson 91) | every numeric claim above carries its realization/trial-space in the same sentence (e.g. §5's "under this instrument, on this date, at this `max_results`") | **holds** |

**No claim in this document required stating at reduced strength or flagged as unverifiable.**
Every clause of the pre-committed gate is answered YES.

---

## 9. What this section does not claim

* **Not new mathematics.** Every number above is a citation, not a re-derivation; this leg ran
  no computation, reproduced no experiment, and introduced no numerical claim of its own.
* **Not a positive fill of the Grade-A/fluid cell.** Leg 309's refutation returns the cell to
  "not filled," not to "established impossible" — the cell's status is an absence in the
  literature this repository has searched, not a proved non-existence.
* **Not movement on `L1 → L4`.** Clay odds stay **~0.05%**, exactly as every leg cited above
  states independently.

---

## Reproduce

Every figure in this section is a direct quote or arithmetic-free transcription from:
`experiments/journal/leg_174.md`, `experiments/journal/leg_309.md`,
`experiments/journal/leg_323.md`, `experiments/journal/leg_317.md`,
`experiments/journal/leg_237.md`, `experiments/journal/leg_316.md`, `writeup/CORRECTIONS.md`
§17 and §21, and `plan_of_record.py:47-55`. No new JSON, no new runner, no figure — per this
leg's declared territory.
