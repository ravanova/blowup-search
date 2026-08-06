# Leg 87 — Route-IVB v1: the independent post-repair regression check of `solver/interval.py`

**Branch** `leg/ivb-v1`. **Exploration leg, CLAIM-BEARING** (soundness of shared infrastructure).
**Gate: YES.** The repair is solid and non-regressive. Leg 69's adversarial corpus plus this
leg's fresh battery banked as a permanent regression suite. Lands normally on `main`.

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is NEXT. Every live ban noted. Two bind and neither bites:
   *no further ℓ¹-Fourier or collocation machinery before NG's gate answers* (this leg builds
   none — it tests arithmetic that already exists) and *build nothing without grepping
   `capabilities.py` first* — done, the `solver/interval.py` entry read in full at line 125,
   post-bench-repair text.
2. `DIRECTION.md` — **has a leg 87 entry** (unlike leg 69, which had none). Thesis and gate read
   from it and cross-checked against the dispatch prompt; they agree verbatim.
3. Leg 69's original corpus read in full: `experiments/p2_route_ia_v1_interval_stress.py`,
   `writeup/data/p2_route_ia_v1_interval_stress.json`, `test_interval_stress.py`,
   `writeup/novelty/leg_69.md`, `experiments/journal/leg_69.md`. The repair commit
   (`be99b280`) read as a diff, not as a description.
4. **Novelty pass FIRST**, committed before any construction (`43f55f0`,
   `writeup/novelty/leg_87.md`), four queries, links not counts.
5. Then: runner, curated data, permanent regression gates, this note.

## What the novelty pass changed about the leg

Leg 69's pass located Rump BIT 2012 but recorded its theorem text as *"located but not
verbatim-verified"* — the PDF fetch returned an encoded stream. This pass got the text
(`pdftotext`) and read **Theorem 4.3** verbatim:

> `| s̃n − xᵀy | < (n + 2)u · ufp(S̃n) + n·eta/2`

That single line reorganised the whole battery. The published absolute underflow coefficient for
the plain recursive dot product is **0.5 η per accumulated term**. The repaired module carries
**2.0** on the plain path — 4× the published constant — and **8.0** on the compensated path,
which Rump's theorem **does not cover at all** (it is stated for the plain recursion; the
compensated path's constant rests on ORO 2005's `a·b = p + e + 5η·θ` remark plus the repair's own
margin argument). So the pass identified, before a line of code was written, **the one number in
the repair with no published bound behind it**, and the battery was aimed there instead of merely
re-running leg 69's scales wider.

It also produced two smaller corrections and one scope note, all recorded rather than patched
(this leg may not edit `solver/interval.py` under any gate outcome):

* Jeannerod–Muller–Zimmermann: Veltkamp's splitting *"works correctly even in the presence of
  underflows"*. Both leg 69 and the repair's comment describe the subnormal defect as "Dekker's
  TwoProduct is error-free only in the normal range" — the **split** is underflow-safe; what
  fails is the **product** `fl(a·b)` once `a·b` itself is subnormal. Same repair, slightly wrong
  reason in the comment.
* Boldo, quoted in the same paper: *"if Cx does not overflow, then no other operation will
  overflow"* — which is why guarding the first multiplication is the right and sufficient guard
  point. The published **remedy** there is *scaling*; the repair chose to **raise**. Sound, more
  conservative, and a legitimate scope choice — a possible future bench item, not a defect.
* IEEE 1788-2015's set-based flavor returns a valid result plus a **decoration** (`trv`/`ill`)
  rather than a NaN. The repair implements the first half and not the second: a widened-from-NaN
  interval is bit-identical to a genuinely computed entire interval and no caller can tell them
  apart. Sound but uninformative; measured and recorded.

## What was actually measured

**20,909 cases, 0 false negatives**, every one decided against **exact rational** ground truth
(`fractions.Fraction` on exact float64 inputs — containment decided exactly, not numerically).

### Part A — leg 69's original corpus, re-run verbatim

Not re-implemented: leg 69's own runner is imported as a module and its seven family builders are
called with its own seed (`20260805`) in its own order, so the corpus is literally the same
corpus. Case counts match the banked file exactly, family by family (6772 / 240 / 720 / 720 /
3904 / 840 / 840).

| family | false negatives pre → post | worst relative slack pre → post |
|---|---|---|
| `elementary_ops` | 0 → 0 | 5.0591067023618705e-20 → **identical**, Δ = 0.0 |
| `isum_cancellation` | 0 → 0 | 0.4930564171798272 → **identical**, Δ = 0.0 |
| `matvec_point_and_box` | 0 → 0 | 1.7403580402497008e-12 → **identical**, Δ = 0.0 |
| `dot2_normal_range` | 0 → 0 | 0.4991042453068184 → **identical**, Δ = 0.0 |
| `tail_block_conditioning` | 0 → 0 | 0.4763772490895882 → **identical**, Δ = 0.0 |
| `dot2_subnormal_range` | **43 → 0** | −0.8223 → **+0.4901** |
| `matvec_subnormal_range` | **19 → 0** | −0.9756 → **+0.4754** |

The five normal-range families reproduce their banked worst-case statistic to **all 17 printed
digits, Δ exactly 0.0** — that is gate clause (b)'s core answer, and it is a bit-level
reproduction rather than an "unchanged within tolerance". Worst absolute escape 6.579 η → **0**.
The Dekker probe that returned a silent `[nan, nan]` at 2^997 now **raises `OverflowError` at
exactly 2^997**, and no exponent below it returns a non-finite error term.

### Part B — the fresh battery (six families of this leg's own design)

* **F1b, the sharpest one — the η constants against the extremal case, in closed form.** Take
  `M_ij = η` exactly and `v_j = c_j + 1/2` with every `c_j` of the same parity: each exact product
  lands precisely halfway between two representable subnormals, round-half-to-even breaks every
  tie in the same direction, and sums of integer multiples of η are exact while subnormal. So the
  absolute accumulation error is **exactly m·η/2 — Rump's bound attained with equality**.
  Measured demand: **0.5000 η per term**, matching the theorem to machine precision. Implemented
  2.0 and 8.0 therefore carry **exactly 4× and 16× margin**, measured rather than asserted.
  Random subnormal data never gets near this; leg 69's corpus could not have distinguished 4×
  margin from 4000×.
* **F1, the band wider and finer than leg 69's** (scales 1e-130…1e-190 in steps of 3, m ∈
  {8, 32, 64, 258} rather than leg 69's single m = 64, because the constant scales with m):
  worst **radius utilisation 0.0673** — the true error consumes under 7% of the enclosure at its
  worst — minimum headroom 22 η.
* **F2, operands that are themselves subnormal** (integer multiples of η, not merely small):
  160 cases, 0 false negatives, minimum headroom 11 η. This is the regime where every relative
  term is identically zero and the η constant is the only thing holding the enclosure up.
* **F3, the Dekker wall swept in BOTH operands.** Leg 69 and the repair both probed `a = 2^e,
  b = 1`. The splitting is applied to both operands and the product can overflow independently of
  either. 324 (e_a, e_b, sign, sign) cells including product overflow: **284 raised, 40 enclosed
  the exact rational product, 0 silent NaN, 0 missed.** The wall is at **2^997 in operand a and
  2^997 in operand b** — symmetric, as it must be.
* **F4, the NaN path.** 0 stored NaN endpoints across 8 constructor and arithmetic cases
  (including `entire − entire` and `entire × 0`, which manufacture fresh NaNs); a NaN matrix row
  widens to `[−∞, +∞]` while its clean neighbour in the same matvec keeps width 3.55e-15.
* **F5, the live K-range, every row.** `bordered_linearization` at K = 16/32/64/128 — nonzero
  entries **0.5 to 128**, tail diagonal exactly zero — uncancelled and catastrophically
  cancelled, both reductions, 5,856 cases: **0 false negatives, worst relative slack +0.375, no
  case touching an endpoint.** (Not directly comparable to leg 69's banked 0.4764: this corpus is
  wider, including uncancelled rows and every row of every K.)
* **F6, the pre/post differential — the check no containment test can perform.** The pre-repair
  module is reconstructed in memory from `git show be99b280^:solver/interval.py` and **endpoint
  bit patterns** are diffed. A repair that made an enclosure *narrower* would pass every
  containment test whenever the narrower enclosure happened to keep the answer, and would have
  silently eaten the rigour. Result over 2,192 endpoints: **1,216 identical, 976 wider, 0
  narrower, max 2 ulp.**

## The one number that sharpens the repair's own claim

The repair reported *"100 pre/post enclosures on the live `bordered_linearization` (K = 16…128)
and a normal-range battery are IDENTICAL endpoint bit patterns."* Split by conditioning, that is
half the picture:

| live-operator endpoints, K = 16…128 | identical | wider | narrower |
|---|---|---|---|
| **uncancelled** | **976 / 976** | 0 | 0 |
| **catastrophically cancelled** | **0 / 976** | **976** (1–2 ulp) | **0** |

On uncancelled data the claim is exactly right. On rows cancelled to ~1e-32 relative — **the
leg 51–53 conditioning the certificate actually runs in** — every endpoint moved, by 1 to 2 ulp,
always outward.

The cause is **not** the η term. The repair made *two* edits to each error term, not one:

```
pre :  err = _up(g * mass)
post:  err = _up(_up(g * mass) + eta_term)
```

The η term is ~1e-321 at m ≤ 260, some 290 decades below these endpoints, so it cannot move a bit
there. Attribution was measured, not argued: re-loading the **post-repair source with both η
constants set to 0.0** (keeping the extra push, removing the η floor) reproduces the post-repair
bits on **976/976** cancelled live endpoints. The live-range movement is **entirely the second
outward push**. On a cancelled row the error term *is* the endpoint, which is why it shows there
and nowhere else.

Consequences, stated plainly: this is **not a regression** and does not touch the gate's `no`
branch. Zero endpoints are narrower, zero containment checks changed verdict, and the banked
worst-case slack statistics reproduce to 17 digits (a 1-ulp shift moves slack and width together,
leaving the ratio invariant at double precision). It is a **1–2 ulp conservative widening in the
cancelled live range**, and the accurate form of the repair's claim is *"bit-identical on
uncancelled live data, ≤ 2 ulp wider and never narrower on cancelled live data"*. Recorded here;
`capabilities.py` is integration-owned and was not edited by this leg.

## A second recorded nuance (measured, not patched)

`solver/interval.py`'s own comment says a NaN endpoint *"used to pass the `lo <= hi` guard
vacuously and then pass every downstream containment check with it."* Measured against the
pre-repair source: `Interval.contains(1e300)` on a `[nan, nan]` interval returned **False**, not
True — the safe direction. A caller writing `assert iv.contains(x)` would have *caught* the
defect. What was genuinely vacuous is the constructor's `np.any(lo > hi)` invariant guard, and any
check written in the negated form `not (x < lo or x > hi)`, which **is** True on NaN. The defect
was real and worth fixing; its blast radius depended on which form the caller used. The comment
overstates it slightly.

## What this leg does NOT claim

No novelty, of any kind. Both defects are documented limitations of Dekker's and ORO's algorithms
(leg 69 established that; this pass confirmed it with verbatim theorem text). The extremal
half-η construction is a *test-design* device for attaining a published bound, not a new bound.
No certification claim is made or moved. `solver/interval.py` was read and never edited, and the
`ilog`/`iatan_small` transcendentals and the `interval_certificate.py` pipeline above it were out
of scope.

## Files

* `experiments/p2_route_ivb_v1_postrepair.py` — the runner (Part A re-run + Part B battery).
* `writeup/data/p2_route_ivb_v1_postrepair.json` — curated data, including the family-by-family
  delta against leg 69's banked pre-repair numbers and the full pre/post bit differential.
* `test_interval_postrepair.py` — six permanent regression gates, 3.2 s.
* `writeup/novelty/leg_87.md` — the novelty pass, committed before construction.
