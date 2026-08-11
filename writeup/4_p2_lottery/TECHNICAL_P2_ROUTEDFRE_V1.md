# Route-DFRE v1 (fig71, provisional) — DF-CGL, reproduced exactly from its own released proof data

*Phase 2 / P2, leg 316. First entry of the standing CAP-reproduction lane (steer item 6).
Code: `experiments/p2_route_dfre_v1.py` → `writeup/data/p2_route_dfre_v1.json` →
`experiments/p2_route_dfre_v1_evidence.py` → fig71. Novelty pre-commitment:
`writeup/novelty/leg_316.md`. Deterministic, ~27 s once the target repository is
cloned (~1 min including the one-time clone).*

**Every row of the released proof-witness data for Dähne–Figueras's (arXiv:2410.05480)
Case I, `j = 1` branch — 49,465 rows across three segments, plus both connection points —
satisfies the paper's own Section 6 box-chaining condition, checked in EXACT dyadic
rational arithmetic against the paper's own released `CGL.jl` output, independent of Arb,
Julia or CAPD. Gate answered YES.**

---

## 1. What this leg is, in one paragraph, and what it is not

Legs 61 and 256 established a lane: take a published computer-assisted proof (CAP), and
find out — mechanically, not by trusting the abstract — whether this repository can drive
enough of its own machinery to land inside the authors' published result. Both times, real
issues turned up (leg 61's sign convention; leg 256's stale notebook multiplier). The steer
(item 6) makes this a standing lane: one CAP reproduced per cycle. This is entry 1:
Dähne–Figueras's complex Ginzburg–Landau (CGL) singular-solution branches, `arXiv:2410.05480`.

**This is not a re-run of leg 48.** Leg 48 (Route-V v0) used this same paper to close stage
V's novelty gate, by re-deriving the branch/fold from the paper's *equations* in an
independent float64 shooting method. This leg reads the paper's *released proof-witness
output* — the actual interval-arithmetic balls their rigorous procedure emitted — and checks
them against the paper's own stated corollary, in exact rational arithmetic. Neither leg
substitutes for the other; §2 of `writeup/novelty/leg_316.md` states the ban check this
leg's brief required explicitly, and it is restated in §7 below.

## 2. The source, pinned

* **arXiv:2410.05480v2**, Dähne & Figueras, *Self-Similar Singular Solutions to the
  Nonlinear Schrödinger and the Complex Ginzburg–Landau Equations*. PDF
  `sha256 = d95df28d2d741b42315b11b0afe3e3cebe5fab6f7561559913e55fd2d749d4ac`.
* Their verification package, bibliography item **[15]**:
  `github.com/Joel-Dahne/CGL.jl`, **pinned at commit `be034923c0b63e3103a9b2cb030a02699d05625e`**
  — the exact commit the paper's own reference list names (`Papers/2410.05480.txt` line
  4943). Cloned read-only; this environment has no Julia, no Arb, no CAPD (checked), so
  nothing of theirs is executed — only their **released data files** are read:
  `proof/data/branch_d=1_j=1/{top,turn,bottom,connection_points}.csv.gz`.

## 3. What is actually in those files, and how it is decoded

Their code dumps each proved interval as an Arb `arb_dump_str` ball: `"mid_mantissa_hex
mid_exponent_hex rad_mantissa_hex rad_exponent_hex"`, each an **exact dyadic number**
`mantissa · 2^exponent` (read from Arb's own C source, `arb/{arf,mag,arb}/dump_str.c`, not
guessed from the format). Decoding into Python's `fractions.Fraction` reproduces every
value **exactly** — this is not a float64 approximation of their output; it is the same
number, in the same base, with no rounding introduced anywhere in the check.

Each row of `top`/`bottom` gives, for an `ε`-subinterval, two boxes in `(μ, γ_re, γ_im, κ)`:
a **uniqueness** box (`*_uniq_dump`) and a strictly smaller **existence** box (`*_exists_dump`)
— `μ_i^{(e)}×γ_i^{(e)}×κ_i^{(e)} ⊊ μ_i^{(u)}×γ_i^{(u)}×κ_i^{(u)}`. `turn` (the branch's
turning point, swept in `κ` instead of `ε`) has the same shape with `ε` playing the role
`κ` plays elsewhere. `connection_points` records the two boxes where `top` hands off to
`turn` and `turn` hands off to `bottom`.

## 4. The corollary being checked, quoted from the paper itself (Section 6)

> *"the procedure produces, for each `ϵᵢ`, two boxes,
> `μᵢ^(e)×γᵢ^(e)×κᵢ^(e) ⊊ μᵢ^(u)×γᵢ^(u)×κᵢ^(u)`, where for all `ϵ ∈ ϵᵢ` the function `G`
> is proved to have a zero in the inner box, and this zero is unique in the outer box. …
> it is enough to verify that `μᵢ^(e)×γᵢ^(e)×κᵢ^(e) ⊆ μᵢ₋₁^(u)×γᵢ₋₁^(u)×κᵢ₋₁^(u)` holds for
> all `i = 2, …, N`, i.e., the enclosure of existence for the ith interval is included in
> the enclosure of uniqueness for the preceding interval."*

That second condition is exactly what turns `N` separately-proved local existence results
into one continuous curve of solutions via the implicit function theorem — it is the
mechanism, not an incidental detail, and it is a purely set-theoretic (interval-inclusion)
statement, checkable without touching the PDE, the ODE, or any of the analysis that
produced the boxes. This leg checks that statement, and only that statement, on the
paper's own released output.

## 5. The result

| segment | rows | strict existence ⊊ uniqueness (own row) | chaining: existence ⊆ previous uniqueness | tiling gap |
|---|---|---|---|---|
| `top` | 6,588 | **6,588 / 6,588** | **6,587 / 6,587** | 0 |
| `turn` | 33,281 | **33,281 / 33,281** | **33,280 / 33,280** | 0 |
| `bottom` | 9,596 | **9,596 / 9,596** | **9,595 / 9,595** | 0 |
| `connection_points` | 2 | **2 / 2** (own exists ⊊ own uniq) | — | — |

**Total: 49,465 rows decoded and checked in exact arithmetic; every one of the 49,462
chaining comparisons and 49,467 strict-inclusion comparisons holds.** Runtime **26.8 s**
once `CGL.jl` is cloned (a one-time ~30 s network cost, cached and never committed —
`Papers/` is entirely gitignored).

**Decoder sanity, checked before the inclusion results were trusted (pre-committed in
`writeup/novelty/leg_316.md` §5):** the first `top` row's decoded `μ_exists` midpoint is
`1.2320381643118439` against the paper's own printed Section 6 value
`μ₁ = 1.23203752321003` — difference **6.41e-07**, and the decoded `κ_exists` midpoint is
`0.8531036243056758` against the paper's printed `κ₁ = 0.8531088807225934` — difference
**5.26e-06**. Both are inside the existence ball's own radius at that row
(`1.27e-06` for `μ`, `8.69e-06` for `κ`) — i.e. the paper's own printed starting point lies
inside the box our decoder reconstructed from their raw dump, which is exactly the relation
that should hold and is the check that the byte-level decode (mantissa/exponent parsing,
hex sign handling, the arb-vs-arf column distinction) is not silently wrong.

## 6. GATE, in its pre-committed wording

**"Does DF-CGL's published verification package reproduce the paper's own corollary from
its published constants, in this environment?"**

**YES.** Every row of the released proof-witness data for the Case I, `j=1` branch
satisfies the paper's own Section 6 chaining condition, verified independently in exact
rational arithmetic, with the decoder itself cross-checked against the paper's own printed
numbers. Per the gate's yes-branch: **the validation is banked at full strength**, in the
framing §0b of the leg's brief specified — this is independent validation of the field's
only Grade-A dissipative certificate (leg 174's occupancy-matrix finding: the cell is empty
"for want of a target, not a method"), which measurably nobody else has done. The lane's
second entry becomes dispatchable, selected by the DM at landing.

## 7. The ban check, restated after the numbers are in (per the leg brief's instruction)

Stage V's ban (re-posed 2026-08-04, `plan_of_record.py`) forbids re-opening the question
*this repository's own* certificate margin under dissipation, unless re-posed for a fluid
transport model with `L1` first. **This leg never measures this repository's own
`HL_S2_nonsymmetric` certificate, never touches `ℓ¹_w`/collocation/origin-H², and poses no
fluid model.** It checks whether a *third party's own, already-published, already-refereed*
result is internally consistent with its own released numbers — the same category of
question leg 256 asked of Breden–Chu. Having run the construction, that distinction held
throughout: nothing in the decode, the inclusion checks, or the sanity cross-check required
or produced any statement about a fluid transport model, a viscosity dial on this
repository's own operator, or a radii-polynomial construction of ours. The distinction did
not become unclean at any point; no escalation on this ground is triggered.

## 8. Attribution rule (leg 256's), applied — there is nothing to escalate

Leg 256's rule: a challenge to a theorem requires the **published constants**, at face
value, to fail the **paper's own corollary**. Here the released proof-witness data — the
most literal reading of "published constants" available, since it is the actual output of
their rigorous procedure, not a printed rounding of it — satisfies their own corollary on
every one of 49,465 rows, with no exceptions and no near-misses (every strict inclusion had
strictly positive margin in each of the four checked components; no row landed on a
boundary). **There is no finding of drift and no potential challenge to report.** This
result is a **positive** entry for the lane: unlike leg 256 (which found a stale notebook
multiplier) and leg 61 (which found a sign-convention slip), this reproduction turned up no
defect in the released package at the level this leg checked. That is itself worth
recording plainly, since three of the lane's four precedent legs (61, 256, and — by leg
174's own account — every prior audit of this cell) found *something*; a clean result is
not the norm and should not be over-read as "nothing to find here" beyond the specific
corollary checked (§9).

## 9. What this licenses, and what it explicitly does not

**Licensed:** DF-CGL's released verification package's raw output, for the Case I `j=1`
branch, is internally consistent with the paper's own stated box-chaining mechanism, to the
letter, independent of the tools (Arb/Julia/CAPD) used to produce it. This is a genuine,
independent check of a real computer-assisted proof, using nothing but the paper's own
data and Python's standard-library exact arithmetic.

**Not licensed:** (a) This is **not** a re-verification of the rigorous bounds themselves
— the boxes' correctness as enclosures of the true `G`-zero set rests on Arb/CAPD's interval
arithmetic and the analytic estimates of paper Sections 5–7, none of which this leg
recomputes; this leg checks only the *combinatorial/set-theoretic* chaining condition on
their *own reported* boxes, which is necessary but not sufficient for the full theorem. (b)
Only the `j=1` branch of Case I was checked (the window pre-committed in the novelty log);
the other seven Case I branches and the four (partial) Case II branches are unchecked. (c)
**Nothing here is evidence about Navier–Stokes.** CGL is semilinear and radial, as leg 48's
own closing note already said; reproducing an external CGL certificate does not move any
link of the L1→L4 chain, and no sentence in this write-up should be read as claiming
otherwise. Clay odds remain ~0.05%, unmoved.

## 10. Standing disciplines exercised

* **75** — the arithmetic model (exact dyadic rationals, not float64) is stated in §3
  before any number is quoted.
* **84** — the window (Case I, `j=1`, both readings via the sanity check and the full
  inclusion sweep) was pre-committed in `writeup/novelty/leg_316.md` before construction and
  not moved.
* **86** — the decoder is checked against an independent reference (the paper's own printed
  `μ₁, κ₁`) before its output is trusted for the main claim, rather than trusted from the
  algebra alone.
* **91** — the negative-result-naming discipline does not apply here (the gate is YES), but
  the realization is still named precisely: Case I, `j=1`, three named segments, exact
  arithmetic, one pinned commit — not "the package," unqualified.
