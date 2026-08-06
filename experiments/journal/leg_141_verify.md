# Leg 141 (Route-WEL) — post-landing verifier report

**Branch:** `verify/141-wel-review`. **Date:** 2026-08-06. **Reviewed:** `main` @ `208c91c`
(leg 141 landed at `7bd6c08`, novelty log at `c4b6640`).
**Verdict: CONFIRMED ON SUBSTANCE — 2 process gaps, 5 wording notes. No misquote, no
mismatched operator class, no unsupported numeric coincidence.**

Method: I did **not** trust leg 141's quotes. I downloaded all four PDFs myself
(`curl https://arxiv.org/pdf/<id>`), ran `pdftotext -layout`, and grepped each fragment
in the raw text. I re-derived the numeric coincidence from EGM's own proof rather than
accepting the leg's assertion of it.

---

## 1. Sources — 10/10 fragments independently re-located, verbatim

All four PDFs fetched fresh and converted. Every fragment appears **in the section leg 141
claims**, character for character.

| # | Paper | Locator claimed | Independently found at | OK |
|---|---|---|---|---|
| 1 | EGM 1906.05811 | Prop. 2.1 (§2 Coercivity) | line 316, `§2 Coercivity` | ✓ |
| 2 | EGM | §1 Main Theorem, `L²_φ` def | lines 125–134, `φ = (1+y²)²/y⁴` | ✓ |
| 3 | EGM | §1, a=0 is CLM; `F₀=y/(1+y²)` | lines 94, 146–149 | ✓ |
| 4 | EGM | §3 opening sentence | line 394, `§3 Modulation equation…` | ✓ |
| 5 | CHH 1905.06387 | §2.1 damping derivation | lines 313–317 | ✓ |
| 6 | CHH | §2.1, the far-field squeeze | lines 323–326 | ✓ |
| 7 | CHH | (3.6) + Prop. 3.1 | lines 432–443 | ✓ |
| 8 | Xu 2607.19762 | §8 Discussion | lines 1865, 1909–1919 | ✓ |
| 9 | Xu | Appendix A | lines 2150–2156, 2199–2203 | ✓ |
| 10 | Chen–Hou 2210.07191 | §2 | lines 785–789 | ✓ |

Notes on the hard cases:

* **EGM Prop. 2.1** reads, verbatim: *"There exists a universal constant C > 0 so that if a
  is small enough and if f is odd, f′(0) = Hf(0) = 0 and ∫_R |f|²φ(y)dy < +∞,
  ∫_R f M_a f φ(y)dy ≤ (−1/2 − C|a|) ∫_R f(y)²φ(y)dy."* Exact match to the leg's quote,
  including the three hypotheses and the constant.
* **Xu arXiv:2607.19762 is a real paper** — `v1 [physics.flu-dyn] 22 Jul 2026`, Jie Xu,
  UIC. I checked this because a 2607 identifier plus unusually convenient phrasing is
  exactly what a fabricated citation looks like. It is genuine, §8 exists at line 1865, and
  the §8 parenthesis naming `[15, Prop. 2.1]` (= EGM, confirmed in Xu's bibliography) is
  verbatim as quoted, including *"in which a gap is certified"*.
* **Xu's abstract independently confirms leg 111's object**: *"Linearizing about the exact
  profile Ω(y) = −y/(y² + 1/4)"* and *"leaves a spectral gap of 1/2 on X"* — so
  `KNOWN_ANSWER_CEILING = 0.5` in `solver/energy_coercivity.py` is correctly sourced.
* **Fragment 10 initially failed my grep** — a false alarm from the PDF encoding `≠` as
  `6=`. On a second pass the sentence is present verbatim at line 785. Not a leg 141 defect.

---

## 2. The numeric coincidence is REAL, and stronger than leg 141 claimed

This was the main thing I was asked to break, and I could not. It is **not** a
unit/convention artifact.

EGM's proof (lines 355–390) does two things the leg asserted but never exhibited:

**(a) The nonlocal term vanishes identically** under the stated hypotheses:
`∫ Hf · f · F₀ · φ = 0`, proved by reduction to `H(f Hf)(0) + ½H(∂yy(f Hf))(0) = 0`. This is
why a purely *local* multiplier can carry the whole constant — the mechanism leg 111's
`D_φ` isolates.

**(b) The surviving multiplier is leg 111's `D_φ`, and its origin value is `(3−γ)/2`.**
EGM's line is `−2HF₀ − 1 + ½ ∂_y(yφ)/φ = 2/(1+y²) − 1 + (y²−3)/(2(y²+1)) = −1/2`.
I re-derived this for a **general** origin exponent γ (i.e. `φ ~ y^{−γ}`):

* `−2HF₀(0) − 1 = 2 − 1 = +1`
* `½ ∂_y(yφ)/φ = ½ + (y/2)(log φ)′ → ½ − γ/2` at the origin
* total `= 1 + ½ − γ/2 = (3 − γ)/2`

which is **identically** leg 111's `D_φ(0) = 3/2 + ½ sin θ (log φ)′(θ)|₀ = (3−γ)/2`
(`solver/energy_coercivity.py:257`). At γ = 4 both give −1/2. Same γ, same meaning
(weight exponent at the origin), same operator, same integration-by-parts identity.

**Normalization check (the unit-mismatch worry, run explicitly).** EGM use `F₀ = y/(1+y²)`
(b = 1); CHH, Xu and leg 111 use `Ω = −x/(x²+¼)` (b = ½), which is `−2F₀(2x)` — an
amplitude factor, and amplitude is *not* a symmetry of the profile equation (1.7), so this
genuinely needed checking. Redoing the origin multiplier in the b = ½ normalization from
CHH (3.5) (`c̄_l = 1`, `c̄_ω = −1`, `ū_x = b/(b²+x²)`):

* `(c̄_ω + ū_x)(0) = −1 + 1/b = −1 + 2 = +1` — the same `+1`
* transport `−c̄_l x ω_x` contributes `½(1 − γ)`
* total `= 1 + (1−γ)/2 = (3 − γ)/2` — **the same function of γ**

So the constant is invariant across the b = 1 and b = ½ normalizations. The coincidence
survives the exact test it was most likely to fail. Leg 141 asserted the match; it is in
fact a structural identity, and the leg under-claimed.

**Operator class.** Same class, confirmed on three independent grounds: EGM say
*"when a = 0 we get CLM model"*; CHH's (3.5) profile is obtained *"by using the exact
formula of the solution of (1.3) with a = 0"* with b = ½; Xu linearizes about
`Ω(y) = −y/(y²+¼)` explicitly. All three are leg 111's `a = 0` CLM linearization, not a
different operator dressed up.

---

## 3. Reproduction from leg 111's own banked data

Re-ran `experiments/p2_route_wel_v1_lit.py`. Confirmed:

* `p = 1` column **bit-identical** to leg 111's banked admissibility in
  `writeup/data/p2_route_we_v1_coercivity.json`: abs diff `0.000e+00` at both `A3` (γ=3)
  and `A4_chen_hou` (γ=4); divergence ratio `1.677722e+07`. The instrument control is a
  real control and it passes.
* `p = 2, 3` at γ = 4 converge (ratio `1.000000e+00`) — the pre-registered check could have
  reported NO and did not.
* `D_φ(0) = −0.500000` at γ = 4; max abs discrepancy across the three sources `0.000e+00`.
* Re-running changed **zero numeric lines** of the JSON (I diffed: the only 11 changed
  lines are `fragment_source` provenance strings; I reverted them).

---

## 4. Territory and banked prose

Clean. `7bd6c08` is **purely additive**: `experiments/journal/leg_141.md` (+234),
`experiments/p2_route_wel_v1_lit.py` (+570), `writeup/data/p2_route_wel_v1_lit.json` (+340).
`c4b6640` adds only `writeup/novelty/leg_141.md` (+312). **1456 insertions, 0 deletions, 0
modifications.** No banked prose anywhere was altered, no other leg's territory touched.

---

## GAP 1 (process, real) — the cap was announced but never applied

Leg 141's own JSON records the gate's branch instruction verbatim:

> `gate_answer_branch_verbatim`: "Record the located statement with hypotheses verbatim;
> **cap the finding's novelty accordingly wherever it is cited.**"

And leg 141's novelty log §1 quotes, as "the claim under test", this line from
`capabilities.py` (the `solver/energy_coercivity.py` row):

> "…because damping at the origin needs gamma > 3 while the basis is in L^2_phi only for
> gamma < 3 -- the SAME threshold, so the window has ZERO width."

**That line is still there, unqualified** (`capabilities.py:243–246`, verified on `main`
HEAD). It still presents zero-width as a structural fact of the operator, with no pointer
to leg 141, no mention of EGM Prop. 2.1, and no statement that the zero width holds only
on the unconstrained odd-sine (p = 1) trial space. Leg 141 quoted the exact line it was
instructed to cap and did not cap it.

The leg's commit message says *"nothing in `writeup/` is rewritten"* — true, but
`capabilities.py` is not in `writeup/`, and it is the primary citation site.

**Precedent says this write-back is expected.** Leg 65 (L1G), the closest prior literature
leg, *did* write its verdict into `capabilities.py` — the `solver/holder_norms.py` row
carries "…were SEARCHED at primary source (leg 65, 4 papers full-text + 39 forward
citations) and NOT found — nearest cousin arXiv:2607.15256 §1.2, same genre, resolved not
obstructed." Leg 141 owes the symmetric sentence and did not write it.

Repair (for a rework leg, not for me): annotate the `energy_coercivity.py` row with leg
141's cap. I have not touched the file.

## GAP 2 (contract, needs an orchestrator ruling) — the DOCS quartet is incomplete

Leg 141 shipped runner + JSON + journal + novelty log. It shipped **no `BLOG_*.md`, no
`TECHNICAL_*.md`, no `*_evidence.py`, and no figure**. `ORCHESTRATION.md` §6 is explicit
that all four are required and that "the merge gate rejects one without the other".

Leg 141's "no measurement, no figure" claim **is** consistent with precedent — but so is
much more than the leg claimed. Leg 65/L1G shipped the *identical* three-file set
(`09728ec`: journal + `p2_route_l1g_v1_lit.py` + `p2_route_l1g_v1_lit.json`; `cda8edc`:
novelty log) with no BLOG/TECHNICAL/evidence/figure, and it was verified and merged
(`20622b4`). So leg 141 is precedent-conformant and contract-nonconformant simultaneously.

This is not a leg 141 defect so much as an unwritten carve-out. **Recommend the
orchestrator either write the literature-leg carve-out into §6 explicitly, or open a rework
leg to give both 65 and 141 their BLOG/TECHNICAL pair.** Silently accepting a third
instance turns §6 into dead text.

---

## Wording notes (not gaps — the verdict does not depend on any of them)

1. **CHH's `k = 4` is stated for `a = 1`, not `a = 0`.** The sentence reads "(we choose
   k = 4 for **a = 1** and small |a|)". Leg 141 quotes it accurately, but its §3 narration
   ("the same chosen exponent 4") sits next to a claim about leg 111's `a = 0` object. The
   a=0-side γ=4 evidence is real, but it comes from CHH (3.6)/Prop. 3.1 (b = ½), not from
   this sentence. Worth foregrounding the right sentence.
2. **CHH's threshold is not numerically leg 111's.** Their `D = −C(k−1)/2 + (c̄_ω + ū_x)`
   has an unspecified `C` (they assume `c̄_l x + aū = Cx` only "to illustrate the idea"), so
   "choose k so that D is negative" is a threshold in `k` that is not `γ > 3`. Leg 141 §3
   says this "**is** leg 111's 'damping at the origin needs γ > 3', published" — that is a
   shape-match written as an identity. The genuine identity is EGM's (§2 above), so the
   verdict is unharmed, but the CHH sentence is doing less work than the prose implies.
3. **"exactly leg 111's `A4_chen_hou` member"** (JSON, `EGM-WEIGHT`) overstates. EGM's
   `φ = (1+y²)²/y⁴` and leg 111's `(2 sin(θ/2))^{−4}` share the origin exponent γ = 4 but
   differ away from the origin (→ 1 vs → 1/16). Only the origin exponent is load-bearing,
   so this is harmless; "same origin exponent as" would be accurate.
4. **The §7 Chen–Hou 2D ellipsis drops the causal step.** The elided text ("If 1 − β is not
   small, I is a large growing factor in the energy estimate") is the actual reason for
   `α ≥ 14`. The ellipsis is marked, so this is not a misquote, but the mechanism as leg 141
   states it (non-vanishing at the singular point caps the exponent) is one link short of
   what the paper argues.
5. **The runner self-confirms on a clean checkout.** `Papers/` is gitignored and the runner
   does not fetch; with PDFs absent it reads `fragment_located` back from its own committed
   JSON. The JSON provenance is honest (`"read back from committed JSON (PDF absent)"`,
   and `located_source` degrades too), and the docstring discloses it — but the console
   table prints `LOCATED` identically in both modes, so a reader watching stdout sees
   "10/10 located" having read zero PDFs. Suggest echoing the provenance in the table.
   (Moot for this review: I fetched all four PDFs myself, and network access works fine, so
   the runner could simply call `Papers/fetch.sh` itself.)

---

## Verdict

**The gate answer YES is CONFIRMED.** Every quoted fragment is genuine, in the claimed
section, and means what leg 141 says it means. The operator class is the same across all
three sources and leg 111. The numeric coincidence `D_φ(0) = (3−γ)/2 = −1/2 at γ = 4` is
not numerology and not a convention mismatch — it is the same multiplier, and I verified
it is invariant across the b = 1 and b = ½ profile normalizations. The window-width
argument reproduces bit-identically off leg 111's own quadrature. The landing is clean and
purely additive.

**Two gaps, both process, neither touching the mathematics:** the cap was never written
back to `capabilities.py` (GAP 1, leg 141 owes this and precedent confirms it), and the
DOCS quartet is missing its BLOG/TECHNICAL pair (GAP 2, precedent-conformant but
§6-nonconformant — needs an orchestrator ruling, not a leg 141 fix).
