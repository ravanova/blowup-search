# VERIFY 265 — independent review of Route-P2C (`leg/265-p2c-v1`), Phase-1 costing

**Verdict: CONFIRMED, no gap found.** Leg 265's four deliverables, its central number, its
correction to leg 251, and its absence-of-obstruction claim all survive independent scrutiny.
Every load-bearing magnitude below was **re-derived from the primary sources by this verifier**,
not re-run from leg 265's script. `main` is safe to receive this report; the construction
decision itself remains the user's, unchanged.

Verifier branch `verify/265-p2c-review`, from `origin/main`. Territory: this file only.

---

## 0. Provenance — four independent downloads now agree

I downloaded all three e-prints myself, from `arxiv.org/e-print`, in a verifier-private
directory:

| paper | md5 | lines | agrees with |
|---|---|---|---|
| BCG `arXiv:2208.09445` | `45ea63c45a1a199ecfb4dc4a15431600` | 6898 | leg 251, leg 266, `verify_251`, leg 265 — a **fourth** independent match |
| CGSS `arXiv:2310.05325` | `04676de9e3262b0740f4938dd8241b79` | 3916 | leg 265 |
| Larson–Penston `arXiv:2509.12435` | `a0a136ed5e961276e135e86fa43fb01a` | 7675 | leg 265 |

---

## A. THE NUMBER — re-derived from scratch, and an ambiguity resolved along the way

I located BCG's `(eq:R1)` (l.526), `(eq:def_R2)` (l.547), `(eq:k_asquotientDZ1)` (l.599–601) at
exactly the line numbers leg 265 cites, transcribed them by hand, and evaluated `k` in 50-digit
decimal arithmetic with no reference to leg 265's runner.

**`(eq:def_R2)` is typographically ambiguous, and the ambiguity is load-bearing.** BCG write
`\frac{1}{\gamma-1}\bigg( … \bigg)^{\frac12}`, which admits two readings:

* **(A) prefactor**: `R₂ = (1/(γ−1))·(bracket)^{1/2}`
* **(B) inside**: `R₂ = ((bracket)/(γ−1))^{1/2}`

Both satisfy the anchors `R₂(1) = 0` and `k(1) = 1`, so those two anchors **do not discriminate**.
The `r*` anchor does, decisively:

| reading | denominator of `k` at `r* = (7−√5)/4` | `k(7/6)` |
|---|---|---|
| **(A)** | `−1.64e−25` — **vanishes**, so `k → ∞` exactly as Lemma `k` requires | **16.3479210516613…** |
| (B) | `−1.0490` — does not vanish; `k` stays finite at `r*`, contradicting Lemma `k` | 3.5407 |

**Leg 265 used reading (A), and (A) is the correct one.** Had it used (B) the entire branch
placement would have been wrong by a factor of ~4.6 and every downstream consequence with it.
This is exactly the kind of silent transcription hazard that justifies re-derivation.

**My independent value: `k(7/6) = 16.34792105166133848739901684613…`**
Leg 265's journal reports `16.3479210517` (correct rounding to 12 s.f.); its banked JSON holds
`16.3479210516613`. **Agreement to 15 significant figures.**

**Anchors, each confirmed against BCG's own text, not assumed:**

* `R₁(1) = 0.8 = 2(γ−1)` — exact; BCG state this in the Lemma `k` proof at l.603.
* `R₂(1) = 0` — exact (bracket evaluates to `0.000`); BCG deduce it at l.603.
* `k(1) = 1` — exact; BCG claim it at l.603.
* `k → ∞` at `r*` — denominator vanishes to `1.6e−25`. And `r* = (7−√5)/4 = 1.19098300562…` is
  **derivable, not assumed**: BCG's `(eq:rstar)` l.363–366 gives `2/(√2·√(1/(γ−1))+1)²+1` for
  `1 < γ < 5/3`, which at `γ = 7/5` is `2/(√5+1)²+1 = (7−√5)/4`. Confirmed by hand.
* `α = (γ−1)/2` confirmed at BCG l.180, so `1/α = 5` at `γ = 7/5`.

**`δ_dis` re-derived independently.** BCG `(eq:delta:dis)` l.489–491 sets
`−δ_dis = 2 − r + (1−r)/α`, so at `γ = 7/5`, `δ_dis = r − 2 + 5(r−1) = 6r − 7` **exactly** — and
therefore `δ_dis = 0` precisely at `r = 7/6`, matching BCG's own `(eq:r:restriction)`
`r > 2γ/(γ+1) = 7/6`. (Leg 265 correctly credits the `6r − 7` line to leg 240 rather than
banking it as new.)

**Branch placement, re-derived by bisecting my own `k`:**

| | my value | leg 265 |
|---|---|---|
| `r_3` | 1.0703743786… | 1.070374378675 ✓ |
| `r_4` | 1.0949749631… | 1.094974963188 ✓ |
| `r_15` | 1.1643257393… | (`δ_dis` −0.014046) ✓ |
| `r_16` | 1.1660995206… | 1.166099520630 ✓ |
| `r_17` | 1.1676680194… | 1.167668019488 ✓ |
| `7/6 − r_16` | 5.6715e−04 | 5.67e−04 ✓ |
| `r_17 − 7/6` | 1.0013e−03 | 1.00e−03 ✓ |
| `δ_dis` on `(r_3, r_4)` | (−0.577754, −0.430150) | (−0.5778, −0.4302) ✓ |

**The consequence is correct.** BCG's NS theorem (Thm 1.3) needs `δ_dis > 0`, i.e. `r > 7/6`.
Since `r^(n) ∈ (r_n, r_{n+1})` and `r_16 < 7/6 < r_17`, every odd `n ≤ 15` has its **entire**
interval below `7/6`; `n = 16` is even. So **`n ≥ 17` is a genuine necessary condition** — and
leg 265 states it as necessary ("cannot use any odd branch below n = 17"), not as sufficient,
which is the correct logical form since "large enough" remains unquantified.

**"Exactly 7 odd branches" — checked for an off-by-one, and it holds.** `n = 1` would also be
odd with `r^(1) ∈ (1, r_2)` inside the window, which would make it 8. But BCG restrict to
**"odd `n ≥ 3`"** in their own words at l.372 ("for a subset of `γ > 1` and odd `n ≥ 3`"), and
`r_1 = 1` is the degenerate endpoint. So `{3,5,7,9,11,13,15}` — **seven** — is right.

**The autonomous-point trap confirmed.** `k(7/6) = 16.3479` is not an integer; `7/6` falls in
`(r_16, r_17)`, an even index; BCG's footnote at l.373 reads verbatim *"The requirement that `n`
is odd is used to ensure \ref{pt:1}"*. Confirmed at source.

**Novelty of the number confirmed in-repo**: `grep` for `k(7/6)`, `k_at_borderline`, `16.3479`
across all `.md`/`.py` on `origin/main` returns **0 hits**.

---

## B. THE CORRECTION TO LEG 251 — the most consequential check. CONFIRMED.

I traced this through leg 251's own corrected text (`origin/leg/251-p0t-v1` @ `873a15f`) and
BCG's equations independently of leg 265's framing.

**Leg 251's ansatz, verbatim (`leg_251.md` §3):**
> *"at a similarity exponent `r^(n) ∈ (r_n(γ), r_{n+1}(γ))`, **`n` odd and large** — the profile
> of Buckmaster–Cao-Labora–Gómez-Serrano, `arXiv:2208.09445`, **Theorem 1.2**, whose blow-up
> conclusion for Navier–Stokes is their **Theorem 1.3**."*

**Leg 251's obligation 4, verbatim, and explicitly *unchanged* by leg 266's correction:**
> *"**Explicit `r`-coverage.** The certificate must state the interval of similarity exponents
> it covers and show it is **not** contained in BCG's dominance regime."*

with the leg's own gloss under obligation 1: *"the certificate's `r`-coverage must lie outside
it, i.e. at `r ≤ 7/6`"*.

**The conflict is real, and it is a theorem, not a reading.** Lemma `k` makes `k` a monotone
bijection `[1, r*) → [1, ∞)`. Therefore `n → ∞` ⟹ `r_n → r*`, and `r^(n) ∈ (r_n, r_{n+1}) → r*`.
Since `7/6 < r*`, any `n` large enough to satisfy `r_n > 7/6` (i.e. `n ≥ 17`, by **my own**
evaluation of `k(7/6)`) puts `r^(n)` **strictly inside** the dominance window `(7/6, r*)` —
which is precisely the region obligation 4 forbids. **The ansatz and obligation 4 pull in
opposite directions.** Independently confirmed.

Two precision notes, neither of which weakens the finding:

1. Thm 1.2's "large enough" is unquantified, so "large" has no numerical threshold of its own.
   The conflict is nonetheless operative in two ways: (i) as a limit statement, `n` large forces
   `r → r*`, deep inside dominance; (ii) leg 251 cites **Thm 1.3** for its NS conclusion, and
   Thm 1.3 *requires* `δ_dis > 0`, hence `n ≥ 17`, hence inside the window. Either route lands
   on the same contradiction.
2. This is the **second** internal-consistency defect found in leg 251, and it is of the same
   species as the first: `verify_251` §C / leg 266 found obligation 1's *wording* naming a
   non-existent object while the leg's architecture prose was already correct. Here the
   *ansatz* names large `n` while obligation 4 was already pointing at the correct locus. In
   both cases the leg's own correct statement is the one that survives. That pattern is worth
   the user's attention when the packet is read: leg 251's obligations are sound; its
   *headline naming* has now twice drifted from them.

**The repair is coherent.** BCG **Theorem 1.1** (l.214) reads verbatim *"Let `γ ∈ (1, +∞)`.
There exists `r^(3)(γ) ∈ (r_3(γ), r_4(γ))` …"* — **no "large enough", no γ-restriction, and 7/5
is inside `(1, ∞)`.** So `n = 3`'s existence at `γ = 7/5` is genuinely unconditional, and
`δ_dis ∈ (−0.5778, −0.4302)` places it firmly outside the dominance window. Confirmed.

**The `n = 15` caveat is genuinely open, not assumed away.** BCG **Theorem 1.2** reads *"Let
`γ = 7/5` and `n ∈ ℕ` be an odd number **large enough**"* — and the paper never quantifies it;
the only quantitative statement in its vicinity is the footnote at l.373 saying they are *"not
aware of any counterexamples for `γ > 1` and `n ≥ 3` odd"*, which is explicitly not a proof.
Leg 265 reports this **open**, and that is the honest disposition.

---

## C. THE `δ_dis ≤ 0` TERM-BY-TERM BREAKDOWN. CONFIRMED at every locator.

* **l.2994 smallness chain** — transcribed verbatim and counted:
  `1/s₀ ≪ δ₀^{3/2} ≪ δ₁ ≪ δ_g δ₀ ≪ δ₀ ≪ 1/Ē ≪ 1/K ≪ 1/m ≪ η_w ≪ δ_g ≪ δ_dis = O(1)`.
  **Eleven elements, `δ_dis` at the top.** Leg 265's transcription is exact, and its structural
  reading — that the obligation removes the element the other ten are calibrated against — is
  the correct reading of BCG's own l.2996 (*"we recall … `δ_dis` is defined in `(eq:delta:dis)`"*).
* **Smallness knob flips.** Confirmed at l.3995–4001: BCG close the energy estimate with
  `J ≤ (2r^{1+1/α}/α^{1/α}) e^{−δ_dis s₀/2}` `(eq:massachusetts)`, small *because* `s₀` is large
  and `δ_dis > 0`. At `δ_dis ≤ 0` this same expression is `e^{+|δ_dis|s₀/2}` and **grows** with
  the proof's only free parameter. Leg 265's "the monotonicity in the free parameter flips
  sign" is exactly right.
* **Duhamel diverges.** Confirmed at `(eq:tambor1)` l.4061–4064
  (`‖F_dis‖_X ≤ δ₁e^{−δ_dis s/2} ≤ δ₁^{3/2}e^{−(9/10)δ_g(s−s₀)}`) and the Duhamel chain
  l.4072–4082, whose convergence rests on `9/10 δ_g > 1/2 δ_g`. At `δ_dis ≤ 0` the first
  inequality fails outright and `‖F_dis‖_X` grows. **"The estimate is false, not merely
  unproved" is accurate.**
* **Sign extraction survives.** Confirmed at l.3898 (`J` carries `e^{−δ_dis s}`) and
  `(eq:maine)` l.3946ff, `|(α^{1/α}/r^{1+1/α})e^{δ_dis s}J + G²| ≲ G` with `G² ≥ 0`. Since
  `e^{−δ_dis s} > 0` for **every real** `δ_dis`, the top-order part of `J` is `−G²` at every `r`,
  independent of `δ_dis`'s sign. **Confirmed, and the scoping is correct**: leg 265 writes
  `J ≈ −(…)e^{−δ_dis s}G² ≤ 0` and labels it *"the top-order SIGN extraction"*. That hedge is
  necessary and present — the raw inequality only gives `cJ ≤ −G² + O(G)`, which is not a
  pointwise `J ≤ 0` when `G` is small. Leg 265 does not overclaim it, and separately concedes
  that the closure `(eq:massachusetts)` does **not** survive. The distinction between the
  dissipation's *sign* (survives) and its *budget* (lost) is drawn correctly.
* BCG l.3804 quoted verbatim and correctly: *"which one cannot expect to bound (since it has
  more derivatives than our energy). Thus, the strategy is to extract the correct sign."* ✓

---

## D. THE LEG-257 ANALOGUE. CONFIRMED — I ran the census myself.

I ran my own 15-term nonlocal probe over both full TeX sources, plus a **live control**
(10 terms of my own choosing, not leg 265's):

| | BCG | CGSS |
|---|---|---|
| `leray`, `biot-savart`, `singular integral`, `calder`, `riesz transform`, `fourier multiplier`, `nonlocal`, `non-local`, `divergence free`, `divergence-free`, `solenoidal`, `incompressib`, `hilbert transform`, `pseudodifferential` — **14 terms** | **0 each** | **0 each** |
| `vorticity` | 5 occurrences | 5 occurrences |
| my own live control (10 terms) | **1112** occurrences | **589** occurrences |

**The probe is live and the absence is real.** My control totals differ from leg 265's 167/185
only because I chose different control terms; the conclusion — a probe that fires abundantly on
the papers' actual subject matter and returns exactly zero on every nonlocal-operator term — is
independently reproduced and, if anything, stronger.

**The 16th term adjudicated line by line, by me, not inherited:**

* **BCG's five**: l.160 and l.162 are literature review of *other authors'* shock work
  (Alinhac, Yin, Christodoulou; Buckmaster–Shkoller–Vicol); l.6424, l.6697, l.6703 are
  **bibliography entries** (`"Shock formation and vorticity creation for 3d Euler"`, etc.).
* **CGSS's five**: **four** on l.194 (literature review — Luk–Speck's *"shock formation
  involving non-zero vorticity"*, plus `\cite` keys) and **one** on l.251, inside a `\cite` key
  (`Zlatos:exponential-growth-vorticity-gradient-euler-torus`) in the wave-turbulence outlook
  paragraph.

**Zero occur in either paper's own mathematics.** Leg 265's adjudication is exactly correct,
including its line attributions. `leg 257`'s specific mechanism (nonlocal operator manufacturing
an algebraic tail against a super-algebraic weight) has **no compressible analogue here**.

**The named replacement obstruction is real and correctly sourced.**

* **(A) derivative excess** — BCG's `X` is `‖(U,S)‖²_{H^{2m}} = ∫_{B(0,2)}(|Δ^m U|² + …)`,
  confirmed verbatim at **l.2240**, unweighted on the ball of radius 2, with BCG's own reason at
  **l.500** (*"In place of weighted spaces, we modify the equation outside a neighborhood of the
  backwards acoustic cone"*). `ΔU/S^{1/α}` costs two derivatives, so it is genuinely unbounded
  `X → X`. Both author-group quotes verified verbatim: BCG l.3804 (above) and **CGSS l.494**
  — *"weighted energy estimates at a higher derivative level than the linear stability
  (regularity higher than `m`), together with lower bounds for `S` to rule out possible
  vacuum"*. Both halves of leg 265's obstruction (A) **and** (B) come from that single sentence,
  read in full.
* **(B) vacuum degeneracy** — `S^{−1/α}` with `1/α = 5` at `γ = 7/5`: a fifth-order pole,
  diverging as `γ → 1`. Arithmetic confirmed from `α = (γ−1)/2` (l.180).
* **Repaired by sign, `δ_dis`-independently** — this follows from §C above and is correct.

**The space claim checks out and matters**: `H^{2m}(B(0,2))` + `φ^{2K}` is neither Breden–Chu's
Gaussian `H²(µ)` nor an `ℓ¹` Fourier space, so the pending stage-V `H²(µ)` decision genuinely
does not gate this target, and the re-posed stage-V ban genuinely does not bite (a BCG-shaped
certificate uses barriers + maximal dissipativity + semigroup + weighted energy + bootstrap +
Brouwer, and **zero** radii polynomials). Confirmed.

---

## E. BUILD COST AND CAP SCOPE. CONFIRMED.

* **`capabilities.py`**: I imported it myself. **48 rows** ✓. Of leg 265's 18 apparatus terms,
  **15 return zero rows**; the 3 non-zero are exactly `taylor` (1), `spectral gap` (1),
  `shooting` (2). I read those four rows: `taylor` and `spectral gap` both live in
  `solver/origin_h2_certificate.py` on the **`a = 0` CLM** object (legs 163/176) — leg 265's
  "does not transfer" adjudication is right; `shooting` ×2 are `bc_weighted_sobolev.py` and
  `viscous_novelty.py`, the latter self-describing as *"an independent RK4"* — **float
  seed-finders, not rigorous interval barrier/shooting for a 2D system**, exactly as adjudicated.
  My own 8-term live control returns 6/14/2/2/14/13/48/10 — **0 of 8 absent**, so the probe is live.
* **BCG's computer-assisted scope**: **Arb** confirmed at l.5693. The `detailssth` appendix
  contains **14 blocks covering 16 distinct labelled statements** (`lemma:k`,
  `prop:left_global`, `prop:left_local_3`, `prop:right_f`, `lemma:biglebowski`,
  `lemma:aux_otromas`, `lemma:aux_Peyeout`, `lemma:paella`, `lemma:aux_34bounds`,
  `lemma:aux_WioverZi_7o5`, `lemma:tenthousand_7o5`, `lemma:aux_F1`, `lemma:aux_a2nr`,
  `lemma:aux_signsZ3Z4`, `lemma:enclosure_r3`, `lemma:enclosure_r4`) — leg 265's "**sixteen**"
  is exactly this enumeration. **Every one is in the ODE / barrier / Taylor-coefficient family;
  `prop:bootstrap`, `prop:topological` and `prop:maxdiss` — §7 and §8, the stability step —
  appear nowhere in the appendix. Zero of 16 touch the stability step.** Confirmed.
* **CGSS computer-assisted content = 0**: `interval arithmetic` / `computer-assisted` /
  `computer assisted` all return **0 occurrences** in CGSS's full source. Confirmed.
* **Runtimes** from Table `tablecompi`: `23:33:55` ✓ (`prop:left_global`), `14:22:36` ✓,
  `13:36:38` ✓. One bookkeeping nicety: the `13:36:38` row covers **`Lemmas aux_WioverZi_7o5,
  tenthousand_7o5` jointly**; leg 265's journal attributes it to `lemma:tenthousand_7o5` alone,
  while its **novelty file states it correctly** as both. Immaterial, and noted only for
  completeness. Leg 174's *"≈14 h single CPU / 10 000 coefficients"* is independently confirmed
  at source: BCG's own l.372 says *"This part of the calculation takes about 14 hours on a
  single CPU"* and l.5982 gives `Z_{10000} ~ 10^{46770}` at 2000 bits.
* **Larson–Penston prior art, verified at source**: IA inside the mode-stability step (l.378,
  l.2194) ✓; maximal dissipativity on backward light cones ✓; the compact box `Re λ ∈ [0,1]`,
  `|Im λ| ≤ 8` with `b₀ = 1/5`, `b₁ = 8` (l.498) ✓; **cites BCG as `BuCaGo2025`** (l.506, 4
  occurrences) ✓; public code at `github.com/mrischrecker/Larson-Penston-Stability`, VNODE-LP,
  **"run on a MacBook Air 2013"** (l.5818) ✓. And the crucial *limitation* is confirmed the hard
  way: **`viscos` appears 0 times in the entire 7675-line source.** It is genuinely inviscid, so
  there is genuinely no `F_dis` to enclose, and leg 265's insistence that obligation 1 stays
  unclaimed is correct. Treating this as both the largest downward cost revision **and** a
  novelty ceiling is the honest reading.

---

## F. DISCIPLINE, TERRITORY, ODDS

* **Territory**: `git diff --name-only <merge-base> origin/leg/265-p2c-v1` = **exactly the 4
  declared files** (`experiments/journal/leg_265.md`, `experiments/p2_route_p2c_v1_costing.py`,
  `writeup/data/p2_route_p2c_v1_costing.json`, `writeup/novelty/leg_265.md`). No shared ledger
  touched.
* **`plan_of_record.py`**: `git diff origin/main:plan_of_record.py leg/265:plan_of_record.py`
  is **empty — byte-identical**. No ban lifted; no stage claimed; stage **P0** is still NEXT.
* **Clay odds**: `~0.05%`, stated four times in the journal, unchanged. **No `L1→L4` link
  moved** — `L1` is still dead in three named realizations.
* **Gap to Clay stated in the same breath**, with the Leray irony (the absence that makes leg
  257 inapplicable is the absence that makes this not Clay's object) explicit rather than
  buried. Wall 2 correctly stated as **not crossed**.
* **Runner**: 32/32 self-tests pass on my execution, gate `YES`, and every printed headline
  matches my independent re-derivation. Both gate branches were reachable, and leg 265 records
  a genuine early `NO` from a real failing test rather than hiding it.
* **Provenance defect kept, not buried**: the shared-scratchpad collision that would have
  reported leg 257's `nov.json` as leg 265's is disclosed in both the journal and the novelty
  file. That disclosure is a credit, and it is a real hazard other concurrent legs should note.

---

## G. What I re-derived vs. what I cross-checked

**Re-derived independently from primary sources (no reliance on leg 265's code or numbers):**
`k(7/6)` to 15 s.f. from hand-transcribed `(eq:R1)`/`(eq:def_R2)`/`(eq:k_asquotientDZ1)`;
resolution of the `(eq:def_R2)` typographic ambiguity against the `r*` anchor; `r* = (7−√5)/4`
from `(eq:rstar)`; `δ_dis = 6r − 7` from `(eq:delta:dis)` and `α = (γ−1)/2`; all of
`r_3, r_4, r_15, r_16, r_17` by bisection on my own `k`; the `n ≥ 17` necessity and the
seven-odd-branch count (including the `n = 1` off-by-one check against BCG's own "odd `n ≥ 3`");
the ansatz-vs-obligation-4 contradiction traced through leg 251's corrected text and Lemma `k`;
the full 15-term nonlocal census plus my own live control on both papers; the line-by-line
`vorticity` adjudication in both papers; the `capabilities.py` census with my own control terms;
the `detailssth` statement enumeration; the LP `viscos = 0` check.

**Cross-checked at source (read the cited line, confirmed the quote):** BCG l.180, 214, 219,
372, 373, 489–491, 500, 2130, 2138–2139, 2142, 2240, 2994, 3595, 3804, 3898, 3946ff,
3995–4001, 4061–4064, 4072–4082, 5693, 5982, Table `tablecompi`; CGSS l.319–320, 382, 494;
LP l.378, 473, 498, 506, 2194, 5818.

---

## H. Standing

**Clean confirmation. No gap found, nothing softened.** The three items I looked hardest at —
the number, the correction to leg 251, and the absence-of-obstruction claim — each survived a
from-scratch re-derivation, and in the first case my re-derivation additionally *disambiguated*
a source formula that could have gone the wrong way. The two precision notes in §B and §C
(the unquantified-"large" logical form; the top-order scoping of the sign extraction) are
already handled correctly in leg 265's own wording; neither is a defect. The one bookkeeping
nicety in §E is immaterial.

Leg 265 is fit to serve as Phase 1's construction decision packet. It remains **escalated**:
construction needs the user's signature, not this verifier's and not the DM's.
