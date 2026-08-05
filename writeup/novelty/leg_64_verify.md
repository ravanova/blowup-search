# Leg 64 — VER-I post-landing review (trigger (b))

**Verifier** VER-I. **Branch** `verify/64-a12-review`. **Date** 2026-08-05.
**Subject** leg 64 (Route-A12 v1), landed on `main` as `bb0ac22` + `cec85ee`.
**Method** independent primary-source retrieval — every paper fetched by this verifier from
arXiv directly (`curl`, then `pdftotext -layout`), not read from leg 64's notes.

**Verdict: the gate answer STANDS on both halves.** The `sigma = 3` YES is confirmed
verbatim, to the line number, in Xu arXiv:2607.19762. The `alpha_1` NO is confirmed against
the whole located corpus. **Three defects found, all inside §4's "two traps" and its
decoration; none of them moves the verdict, and the largest one — `G1` — makes leg 64's own
conclusion *stronger* once corrected.** Recommend a small correction leg, not a rework.

---

## 1. What was independently confirmed

Egress to `arxiv.org` was open from this container (contrary to `Papers/fetch.sh`'s cached
diagnosis), so all five sources were re-fetched from scratch.

### Xu arXiv:2607.19762 — every claimed location is exact

The paper exists: **Jie Xu, "The spectral picture of self-similar collapse in the
Constantin-Lax-Majda equation"**. Its *abstract*, independently of anything in the body,
already carries the relation: it says the paper will "record the formal scaling-relevance
exponent `s*(a) = 1/c_l(a)`, below which fractional dissipation is asymptotically
subdominant in self-similar variables for fixed sufficiently regular data."

| leg 64's claim | this verifier's independent check |
|---|---|
| §6 at L1751 | L1751 = "6 The scaling-critical dissipation exponent s∗ (a)" ✔ |
| §6.1 at L1760 | L1760 = "6.1 The scaling-critical exponent" ✔ |
| eq (6.3) at L1769 | L1769 = "s∗ (a) = , (6.3)" ✔ |
| the `s*(1/2)=3` sentence at L1794–1797 | found at L1795–1796 ✔ |
| Table 1 at L230–247, row `a = 0.5` | L230 = the Table 1 caption; L240 = the `a=0.3` row ✔ |
| Fig 3 caption L1818–1829 | L1818 = "s*"; the annotation at L1821 ✔ |
| Appendix A at L1984 | L1984 = "Appendix A The exact linear semigroup at a = 0" ✔ |

All eleven cited extracted-text line numbers land on the claimed content under
`pdftotext -layout`. **The pass is reproducible to the line**, which is the standard the
leg set for itself.

**The verbatim quote (L1795–1796), as this verifier extracted it:**

> "The branch value is tested at a = 1/2, where s∗ = 3 exactly (cl ( 1/2 ) = 1/3 by the
> exact solution of [20]; also [4, Thm. 2]) and J. Chen [20] proved blow-up at s = 2 < 3
> (subcritical), consistent with persistence."

Word for word identical to leg 64's rendering.

**Table 1, row `a = 0.5`, as extracted:**

> `0.5   0.3333   0.833   3.000   J. Chen [20]: blow-up at s = 2 < 3 (subcritical)`

Exact. The caption also reads verbatim "the exponent `s*(a) = 1/c_l(a)`, and the anchor
cross-checks; `c_l(1/2) = 1/3` is exact ([20]; also [4, Thm. 2])" — so leg 64's rendering of
the caption is right too.

**Figure 3.** The in-plot annotation leg 64 quoted is in the PDF text layer at **L1821**,
verbatim: `s * (1/2) = 3 (exact)`. The caption independently states the same:
"rising from `s*(0) = 1` (Schochet's supercritical full-Laplacian blow-up) through
`s*(1/2) = 3` (J. Chen's subcritical `s = 2` blow-up) to about 54 near the branch endpoint".

**Xu's references, as claimed:** `[4] Lushnikov P M, Silantyev D A and Siegel M 2021
J. Nonlinear Sci. 31 art. 82` (L2281) and `[20] Chen J 2020 Nonlinearity 33 2502–2532
(Preprint 1908.09385)` (L2330). Both exactly as leg 64 stated.

**Xu's own caveats, both verbatim:** "…is not the sharp critical dissipation curve
separating blow-up from global regularity, which for this family remains unknown" and
"The case `s = s∗` is marginal (`γ = 0`) and `s > s∗` is relevant (the open supercritical
regime)". Also confirmed: "…Appendix A all live at `a = 0`, where the two lines coincide and
Theorem 1 is exact". Leg 64's §3 reproduces all three faithfully.

### The exponent dictionary — correctly applied, and this verifier closed an ambiguity the leg left open

This is the translation the review was asked to scrutinise hardest, because it is the step
at which a verdict could invert while still looking consistent.

`LITERATURE_CHECK.md` L117–120 says, verbatim: "ALS/XU write `ω ~ τ^{-β} f(x/τ^{c_l})`, so
**their `c_l` is our `β`** and **our `α = 1/c_l`**; their `Λ^σ` is our `(-Δ)^s` with
**`σ = 2s`**. Hence `s_c(ours) = α/2 = s*(XU)/2`." Leg 64 quotes this correctly.

Applied at `a = 1/2`: `c_l = 1/3` → our `α = 3` → our `s_c = 3/2` → our `σ_c = 2 s_c = 3`,
against Xu's `s* = 3`. **The translation is correct**, and this verifier pinned Xu's gauge
two independent ways rather than taking it on trust:

1. **Xu's own words fix his `s` as the `Λ`-power, not the `(-Δ)`-power.** In §6 he writes
   "for the ordinary Laplacian `s = 2` the sub/supercritical boundary sits at `a ≈ 0.39`".
   `s = 2` *is* the ordinary Laplacian for him, so `Λ^s` is his gauge — the same gauge as
   ALS's `σ` (ALS/SLSA define `-Λ^σ` with `Λ^σ-hat = |k|^σ`, confirmed in the SLSA abstract).
   Hence `s*(XU) ≡ σ(ours)` and the identity `s* = 3 ⇔ σ_c = 3` is a like-for-like match,
   not a conversion.
2. **The `a = 0` anchor corroborates it.** Xu's Table 1 gives `c_l(0) = 1.0000`,
   `s*(0) = 1.000`, and he notes raw CLM blows up at the full Laplacian `s = 2 > s* = 1`,
   supercritical — consistent with Schochet, whose solution ALS index at `σ = 2` (§5.1).
   Our gauge at `a = 0` gives `α = 1`, `s_c = 1/2`, `σ_c = 1`. **Matches `s*(0) = 1`.**

**One thing leg 64 should have surfaced and did not.** `LITERATURE_CHECK.md` L287–288 records
a *competing* branch of the same dictionary, hedged: "**If `c_l = 2β` in the source's
convention**, then `s*(a) = 1/c_l = 1/(2β) = α/2 = s_c`". Under *that* branch `s*(1/2)` would
be `1.5`, not `3`, and **the YES half of the gate would collapse**. Leg 64 asserts the
`c_l = β` branch by citation without noting that the repository's own file left the question
hedged. The assertion is **correct** — the two checks above settle it, and
`LITERATURE_CHECK.md` L128 independently reports the `F6` map against Xu Table 1 as "exact at
`a = 0` and `a = 1/2`" — but the leg closed the ambiguity silently instead of visibly.
Recording it here so the resolution is on the record rather than assumed.

### The `alpha_1` NO half — corpus exhaustiveness re-run and confirmed

**Corpus enumeration re-run independently** (`export.arxiv.org/api/query?search_query=
all:"Constantin-Lax-Majda"&max_results=100`): `totalResults = 25`, all 25 returned. The
enumeration is genuinely complete for arXiv. Every ID leg 64 listed is present, and the
dissipative-gCLM subset is the claimed four — `1908.09385` (Chen), `2207.07548` (ALS),
`2411.01891` (SLSA), `2607.19762` (Xu).

Leg 64's "everything else" list is abbreviated with an ellipsis; this verifier checked the
five items it omitted. Four are plainly inviscid/geometric (`1010.4844`, `1805.04401`,
`2010.12700`, `2107.04777`). The fifth, **`1907.08748` (Du, "On some model equations of Euler
and Navier-Stokes equations")**, was worth opening because its title suggests dissipation —
it is a **2D generalization of CLM**, not dissipative gCLM at `σ = 3`. **The four-paper claim
survives the omission.**

**Per-source confirmations:**

* **ALS `2207.07548`.** §5 headings extracted exactly: §5.1 `a=0, σ=2` (L1044), §5.2
  `a=1/2, σ=1` (L1178), §5.3 `a=0, σ=1` (L1298), §5.4 `a=0, σ=0` (L1561). **No `σ = 3`
  anywhere in the paper.** Leg 64's real-line corpus `{(0,0),(0,1),(0,2),(1/2,1)}` is exact.
  ALS L1816 also flags "one pair of double poles for `a = 1/2`, `σ = 0, 1`, as periodic
  analogues … Details are left for future work" — which is precisely the gap SLSA then filled,
  and it matches leg 64's periodic corpus.
* **SLSA `2411.01891`.** Abstract verbatim: "We derive new periodic solutions for `a=0` and
  `1/2` and `σ=0` and `1`". Exactly as leg 64 quoted. `σ = 3` absent.
* **LSS `2010.01201`.** Grepped `viscos|dissipat` over the full extracted text: **exactly one
  hit, at line 2236, and it is a bibliography entry** — precisely as leg 64 reported, line
  number included. The paper is inviscid and cannot contain `alpha_1`. (See `G3` for a
  trivial mislabel of *which* paper that entry cites.)
* **Chen `1908.09385`.** Confirmed to carry no `dα/dν`-type object. See `G1` for what it
  *does* say.

**Nothing in any located source computes, estimates, or names a quantity of the type
`dα/dμ` for this model, at `a = 1/2` or anywhere else.** The NO half stands.

**One scope caveat on the word "exhaustive."** The enumeration is arXiv-scoped. Pre-arXiv and
non-arXiv journal literature (Sakajo 2003 ×2, Schochet 1986, De Gregorio 1990) is not covered
by it — leg 64 handles Sakajo via Q7 and Schochet via ALS §5.1, which is the right treatment,
but "the entire dissipative gCLM corpus" is doing slightly more work in the prose than the
method supports. Not a defect; a phrasing note.

### Reproducibility of the numeric claim — clean

* `python3 experiments/p2_route_a12_v1_alpha_lit.py` **reproduces the committed
  `writeup/data/p2_route_a12_v1_alpha_lit.json` byte-identically** (`diff` empty). It is a
  self-contained re-emitter of the query log, as its docstring says; it computes nothing, so
  the standing gCLM measurement ban is genuinely respected.
* **The ladder traces to its source.** `writeup/data/p2_route_h_v1_critical.json` holds
  `0.13277004191934333` (K=96), `0.13347014931942064` (144), `0.1336284588391547` (192),
  `0.13368266982772414` (240). Rounded to 6 dp these are exactly the
  `0.132770 / 0.133470 / 0.133628 / 0.133683` quoted in both the JSON and the prose. The same
  ladder appears independently at `experiments/p2_route_i_v1_driven.py:66`.
* **Arithmetic checks.** Full-ladder spread `0.133683 − 0.132770 = 9.13e-4` ✔ ("9.1e-4" in
  prose). Last two rungs `5.5e-5` ✔. Distance from zero in last-rung spreads
  `0.133683 / 5.5e-5 = 2430.6` ✔ ("about 2400×"). Sign stable across every rung ✔.
* **DOCS quartet complete**: `experiments/p2_route_a12_v1_alpha_lit.py` (502 lines),
  `writeup/data/p2_route_a12_v1_alpha_lit.json` (335), `writeup/novelty/leg_64.md` (203),
  `experiments/journal/leg_64.md` (148). Every number in the prose is traceable to the JSON,
  and through it to Route-H v1.

---

## 2. The gaps

### G1 — Trap 1 misattributes Chen's criticality at `a = 1/2`. *(the real finding)*

Leg 64, `writeup/novelty/leg_64.md` §4:

> "J. Chen (`1908.09385` §1.2, L84–96) defines criticality by **norm scaling**:
> `‖ω(t,·)‖_{L^{|a|^{-1}}}` is the conserved-in-scaling norm, so `Λ^γ` with `γ = |a|^{-1}` is
> *his* critical dissipation. At `a = 1/2` that is **`γ = 2`**."

and `writeup/data/p2_route_a12_v1_alpha_lit.json`, trap `T1`:
`"chen_norm_criticality_gamma": 2.0`.

**Chen's §1.2 as this verifier extracted it, verbatim:**

> "For (1.1) with `a > −1`, there is no coercive conserved quantity or a-priori estimate for
> general initial data. … We will show that for several classes of initial data, `‖ω‖_{L^1}`
> is conserved. In these cases, a simple scaling analysis shows that **`L = Λ` corresponds to
> the critical dissipation**.
>  For (1.1) with `a ≤ −1`, we will show that the equation possesses a-priori `L^{|a|}`
> estimate, i.e. `‖ω(t,·)‖_{L^{|a|}} ≤ ‖ω_0‖_{L^{|a|}}`, which makes `Λ^γ` with
> `γ = |a|^{-1}` the critical dissipation with respect to the natural scaling of the
> equation."

Two errors follow:

**(a) The norm index is inverted.** Chen's a-priori estimate is in **`L^{|a|}`**, not
`L^{|a|^{-1}}`. The scaling `ω_λ = λ^γ ω(λx, λ^γ t)` gives `‖ω_λ‖_{L^p} = λ^{γ−1/p}‖ω‖_{L^p}`,
so scale-invariance needs `γ = 1/p`; with `p = |a|` that is `γ = |a|^{-1}`. **The norm index
and the dissipation index are reciprocals of each other**, and leg 64's prose wrote the norm
carrying the dissipation's index. Self-inconsistent as written.

**(b) The formula is applied outside the range Chen states it for, and Chen's actual answer at
`a = 1/2` is different.** `γ = |a|^{-1}` is asserted by Chen **only for `a ≤ −1`** (where
`|a|^{-1} ∈ (0,1]`, and where `L^{|a|}` is a genuine norm). At `a = 1/2` we are in Chen's
`a > −1` regime, where **his own stated critical dissipation is `L = Λ`, i.e. `γ = 1`, from
`L^1` conservation** — not `γ = 2`. Note also that the formula pushed to `a = 1/2` would want
the `L^{0.5}` "norm", `p < 1`, which is not a norm; the range restriction is not incidental.

**Where the `2` actually comes from.** Chen's **Theorem 1.1**, verbatim: "Consider (1.1) with
`Lω = −∂_xx ω`. There exists `δ > 0` such that for `a ∈ (1/2 − δ, 1/2 + δ)`, `0 ≤ ν ≤ 1`,
(2.1) develops a self-similar singularity in finite time for some `C_c^∞` initial data." The
`2` is **the full Laplacian Chen chose as his instrument** ("We focus on the full Laplacian
for simplicity", Remark 1.2), not a criticality in his scheme. That is exactly what Xu's
"blow-up at `s = 2 < 3` (subcritical)" refers to, and **Xu's sentence is verbatim correct** —
the misreading is leg 64's gloss on Chen, not Xu's citation of him.

**A related imprecision in the same leg.** Leg 64's §1 grep table says of Chen: "His `a = 1/2`
self-similar ansatz is at L195–222 and is **inviscid** (`ν = 0`, stated in the line)." True of
the *ansatz derivation* in §2, but Chen's **theorem** at `a ≈ 1/2` is **viscous**, `0 ≤ ν ≤ 1`
with `Λ^2`. The JSON's `CHEN` role field ("blow-up at gamma=2 for a near 1/2") gets the
viscous part right; the novelty prose's row reads as if Chen's `a = 1/2` result were inviscid.

**Effect on the gate: none, and the corrected reading is stronger.** Trap 1 exists to say
"Chen's 'critical dissipation' is not our `σ_c = 3`, so his theorems do not close the gate."
That conclusion is **untouched and better supported** once fixed: Chen's own norm criticality
at `a = 1/2` is `Λ^1` (two units below `σ_c = 3`), and the dissipation his theorem actually
carries is `Λ^2` (one unit below). Either way he is nowhere near `σ = 3`, and neither number
is a `dα/dμ`. **The verdict does not move; the reason given for it is wrong and needs
replacing.**

### G2 — Trap 2's Oldroyd-B attribution is not in ALS

Leg 64 §4: ALS's `σ = 0` "marginal dissipation" — "(it arises in a **1D Oldroyd-B stress
model**)". The JSON's `T2` repeats it: `"(1D Oldroyd-B stress model)"`.

**`2207.07548` contains no occurrence of "Oldroyd", "viscoelastic", "stress", or "polymer"**
anywhere in the extracted full text. The gloss is attributed to a specific paper that does not
make it.

The **load-bearing half of Trap 2 is confirmed verbatim**: ALS L214 reads "for `a = 0` with
'marginal' dissipation `σ = 0`", and it is the only "marginal" occurrence in the paper — so
the trap itself (ALS's "marginal" is the *bottom* of the `σ` range, not `σ = σ_c`) is real and
correctly identified. Only the parenthetical provenance is unsourced. Low severity; it should
be dropped or re-sourced rather than left attributed to ALS.

### G3 — two trivial mislabels

**(a)** Leg 64 describes LSS's single dissipation hit as "**the citation to ALS's
*Nonlinearity* 33 (2020) paper**". The entry at L2236 is *Nonlinearity* **33(5), 2502 (2020)**
— that is **J. Chen's** paper (Xu's `[20]`, "Chen J 2020 Nonlinearity 33 2502–2532"), not
ALS's. The substantive claim (LSS is inviscid; its one hit is a bibliography line at L2236) is
exactly right.

**(b)** The novelty prose calls Q8 a "**100-result** arXiv enumeration". `max_results=100` was
the request; `totalResults` is **25**, and 25 came back. The enumeration is *complete*, which
is the stronger and more accurate thing to say.

---

## 3. Editorial note on what landed downstream

`capabilities.py` line 80 now reads (via `260fec2`, applied by the orchestrator, not by
leg 64):

> "criticality sigma=3 at a=1/2 IS published (Xu arXiv:2607.19762 sec 6.1 + Table 1 row
> a=0.5, Fig 3, 's*(1/2)=3 exactly') …"

Accurate as a citation. But Xu labels `s*` **"a formal scaling diagnostic, not a proved
persistence threshold"** (Figure 3 caption, verbatim) and says it is consistent with Schochet
at `a = 0` "only as a formal scaling-relevance exponent … not as a proved persistence
threshold". Leg 64's §3 quotes this faithfully; the one-line annotation does not carry it.
**Recommend the qualifier ride along wherever the citation is quoted in compressed form**, so
"published" is never read as "proved threshold". Flagged for the DM — outside this verifier's
territory to edit.

---

## 4. Recommendation

**The leg's banked result stands.** The `sigma = 3` YES is as solid as a citation gets —
verbatim in three independent places in a Tier-1 paper, at line numbers that reproduce, with
the exponent dictionary correctly applied and independently double-pinned. The `alpha_1` NO is
supported by a genuinely complete arXiv enumeration and five full-text reads.

**`G1` warrants a correction leg**, not a rework and not a user question: it is a misread of a
primary source sitting inside the section whose whole purpose is exponent care, and it is
recorded in both the prose and the JSON. It rewrites no banked number — the fix strengthens
the argument it appears in. `G2` and `G3` can ride along in the same correction.
