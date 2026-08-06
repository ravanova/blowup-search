# VERIFY 251 — independent review of Route-P0T (PR #20, `leg/251-p0t-v1`)

**Verdict: the gate answer, the named candidate, and the honesty framing all hold. ONE
load-bearing defect found, in the stated certificate obligation #1 — not in the gate, not in
the honesty framing, but in the sentence Phase 1 would be built from. Branch pushed, `main`
NOT pushed, per the dispatch's own instruction that even a small gap be flagged rather than
smoothed over.**

Reviewer discipline: every primary source below was downloaded by this review, from
`arxiv.org/e-print`, and read at full LaTeX source — not re-read from leg 251's transcriptions
and not obtained by re-running its runner (lesson 90).

| source | md5 (e-print tarball) | lines of TeX |
|---|---|---|
| BCG `arXiv:2208.09445` | `45ea63c45a1a199ecfb4dc4a15431600` | 6898 |
| CGSS `arXiv:2310.05325` | `04676de9e3262b0740f4938dd8241b79` | 3916 |
| Pineau–Vicol `arXiv:2607.09619` | `05dfc6a9d461d5b42f0e637ced866c66` | 1869 |

---

## A. The critical honesty point, checked first

**PRESERVED, accurately and prominently.** "The named candidate is **compressible**
Navier–Stokes, which is **not** the system the Clay problem asks about" is the first bullet of
`leg_251.md` §7 ("The honest ceiling"); the JSON carries it twice, at
`clay.statement` and at `what_a_certificate_would_NOT_show`; the word COMPRESSIBLE is
capitalised in the commit subject. Clay odds are stated as `~0.05%` in the journal header, in
§7, in `clay.odds`, and in the commit message. No phrase resembling "Clay-relevant target"
appears anywhere in the leg's four files.

**One presentation note for whoever restates this.** §8 — the pre-committed gate-answer block,
and therefore the block most likely to be quoted onward — names the object as "compressible"
but does **not** repeat the "not the system Clay asks about" clause, which lives one section
earlier. Any restatement should carry the clause explicitly rather than rely on the adjective.

---

## B. What I independently re-derived (not merely cross-checked)

### B1. BCG Thms 1.2/1.3 say what the leg says they say. CONFIRMED, verbatim.

`\newtheorem{theorem}{Theorem}[section]` (l.84) numbers by section, so within §1:
`th:mainlarge` = **Thm 1.1**, `th:mainr3` = **Thm 1.2** (l.217), `th:stability` = **Thm 1.3**
(l.220). Thm 1.2: *"Let `γ = 7/5` and `n ∈ N` be an odd number large enough. There exists
`r^{(n)}(γ) ∈ (r_n(γ), r_{n+1}(γ))` … This gives a smooth and radially symmetric self-similar
solution."* Thm 1.3: *"Let `(U^E, S^E)` be the profiles of Theorem [1.2]"*, concluding
finite-time singularity for `\eqref{eq:NS}` from smooth finite-energy data with `ρ₀` constant
at infinity. **Every element of the leg's citation — `γ = 7/5`, odd large `n`,
`r^{(n)} ∈ (r_n, r_{n+1})`, the profile pair `(U^E, S^E)`, the 1.2→1.3 dependency — is exact.**

### B2. The §7 sentence is genuinely there. CONFIRMED, word for word.

BCG l.2085, inside `\section{Linear Stability of the Profile}\label{sec:linear}` at l.2084 —
the **seventh** `\section` (intro / expansions / left / right / left7on5 / mainproof /
**linear** / nonlinear stability / appendices), so "§7" is right:

> *"The stability for the Euler equation will follow in general, while in the Navier-Stokes
> case we need to restrict the parameter `r` to a regime where the self-similar profile
> dominates the dissipation."*

Micro-imprecision, immaterial: the leg calls this "§7, **opening** sentence". It is the
**second** sentence of §7's opening paragraph.

### B3. The gap is genuinely unaddressed by the named follow-up. CONFIRMED at source, with a
scope caveat.

CGSS's section tree puts `\subsubsection{Dissipation term}` at l.2693, under §3.4 (l.2446)
of §3 *Nonlinear Stability* (l.1579) — i.e. **exactly `§3.4.2`, exactly titled "Dissipation
term"**, and it is an energy estimate, as the leg states. CGSS l.1803 confirms the
architecture in its own words: *"we need to develop additional decaying rate estimates on `S`
to control the dissipative term `ΔU/S^{1/α}`"* — domination, not enclosure. **The companion
does not close the gap.**

*Caveat, stated:* I verified non-closure **at source for the one named companion**. I did not
run an independent forward-citation sweep of everything citing `2208.09445`. The stronger claim
"nobody has enclosed it" rests on the leg's own §3 novelty net plus this one source-level check.

### B4. The Tsai/L^p logic. CONFIRMED — re-derived from scratch, and the agreement with leg 253
is real, not asserted.

Independent derivation: for an exactly-backward-self-similar profile the Type-I bound is
equivalent to `|U(y)| ≤ C_{U,0}/(1+|y|)` — this is Pineau–Vicol's `\eqref{eq:decay}`, read
verbatim inside Conjecture 1.1 (l.198–205). Then
`∫_{R³}(1+|y|)^{-p} dy < ∞ ⟺ p > 3`, so `U ∈ L^p(R³)` for every `p > 3` and `U ∉ L³`. Tsai 1998
Thm 1's hypothesis is `U ∈ L^q`, `q ∈ (3, ∞)`, a condition on the **profile's integrability
alone** — it contains no reference to the linearisation. Therefore the exclusion applies
**whatever the unstable spectrum of that profile is**. The leg's and leg 253's shared word for
this, "stability-blind", is exactly right.

Pineau–Vicol state the `L^p` step themselves, and the leg's quotation of them is verbatim
(l.223): *"the borderline decay rate, which guarantees `U ∈ L^p(R³)` for every `p > 3`, but not
membership in the scaling-critical space `L³`."*

**Agreement with leg 253 checked directly, not taken on assertion.** I read
`leg/253-nrsx-v1:experiments/journal/leg_253.md`. Its §4 table's second row reads **EXCLUDED**
with the identical mechanism and the identical primary locator (`rotated.txt` l.176–180 = the
sentence above). Two legs, same source, same inference, independently reached. **251's claim of
agreement is accurate**, and it correctly credits 253 with finding it first rather than
claiming priority.

### B5. The Leray-projector claim about the compressible system. CONFIRMED at source — the
leg is right, and for the right reason.

BCG `\eqref{eq:NS}` (l.143–147):

```
∂_t(ρu) + div(ρu⊗u) + ∇p(ρ) − µ₁Δu − (µ₁+µ₂)∇div u = 0 ,    ∂_tρ + div(ρu) = 0
```

with `p(ρ) = ρ^γ/γ` (l.140) and `µ₁ > 0`, `2µ₁ + µ₂ > 0` (l.149) — the Lamé conditions the leg
quotes, exactly. The pressure is **constitutive and pointwise in `ρ`**: there is no divergence
constraint, no elliptic pressure solve, and hence no Helmholtz/Leray projection anywhere in the
system. The `∇div u` viscosity term is itself the tell — it would vanish identically under
incompressibility. **"The compressible system has no Leray projector at all" is true as
stated.**

### B6. Both CONDITIONAL-tier blocks are real and correctly cited. CONFIRMED.

* **Entry B.** `plan_of_record.py` on `main` carries the DSS ban **split**, with Entry B
  *"SPLIT OUT AND RE-POSED 2026-08-07 (leg 254, user-approved)"* and a three-clause lift
  condition — (a) function space, (b) object, (c) price in leg-hours. The leg's wording
  ("blocked on Entry B's own scoping leg, not on a flat ban") matches the live plan. I re-ran
  the runner: it prints `entries 2 / split True / flat-never False / conditional-lift True`,
  read from `plan_of_record.BANNED` at run time.
* **Leg 257.** Read at `leg/257-p1c-v1`. Its measurement is
  `v ~ |x|⁻³` with **fitted exponent −3.000000**, multipole ratio **1.000000** at
  `r = 10/20/40/80`, `∇v ~ |x|⁻⁴`, and coefficient `T = tr S = ∫|U|² = 3.937402486` stable to
  12 digits — hence `P[(U·∇)U] ∉ L²(µ)` for any nonzero divergence-free `U ∈ H²(µ)`. **Every
  magnitude 251 transcribes is 257's, correctly.** Cosmetic imprecision: 251 compresses this
  into one clause — *"an algebraic `|x|⁻⁴` tail, fitted exponent −3.000000"* — without saying
  that the `−4` is `∇v` and the `−3` is `v`. The leg explicitly flags that it did **not**
  re-derive 257, which is the honest handling.

### B7. Wall 2's side. CONFIRMED — the leg's statement is correct and not finessed.

BCG's Thms 1.1/1.2 both conclude a *"smooth and **radially symmetric** self-similar solution"*,
obtained as a connecting orbit of the autonomous `(W, Z)` ODE system `\eqref{eq:DS}` — a
one-dimensional phase-plane object, and the computer-assisted parts (§6, App. B) act on that
ODE. CGSS l.235 states its own contribution as *"a linear stability analysis that allows for
**non-radially symmetric perturbations**"* around *"a radial solution"*, and l.244 decomposes
by vector spherical harmonics **about that radial profile**. **So the 3D-ness comes from a
spherically-symmetric ODE profile, and the non-radial companion is a perturbation off it —
never from the certificate. The leg's "same side as every existing work" is exactly right.**

### B8. The fourth survivor, deliberately not named. DEFENSIBLE — verified against the
preprint itself.

Leg 262 (Route-PVRW) **does not exist**: `git ls-remote --heads origin` returns no `262`
branch, so the requested cross-check was impossible. I read Pineau–Vicol directly instead. All
three of the leg's stated reasons hold:

1. *Expected answer is nonexistence* — **exact**. Conjecture 1.1 (l.198–205) is a triviality
   conjecture: under `|U(y)| ≤ C_{U,0}/(1+|y|)`, *"then `U ≡ 0`."* A computer-assisted
   **existence** certificate is indeed the wrong shape for it.
2. *No numerical anchor* — **supported**. A full-text grep of the preprint for
   `numeric | computer-assisted | interval arithmetic | figure` returns **0**. The paper is
   purely analytic; there is no approximate profile in it to put in a ball.
3. *Wrong side of Wall 2* — **sound**. PV's profile equation is a genuine 3D PDE on `R³`
   carrying the rotation terms `α(JU − (Jy·∇)U)`; there is no ODE reduction, so its 3D-ness
   would have to come from the certificate.

And "leaves open the case `α ≈ 1`" is verbatim at l.232. **This is a reported survivor with
reasons, not a dismissal** — the leg gives it its own §5 and opens it with *"it survives both
screens and it is not DSS-dependent, so I am not entitled to hide it."*

### B9. Territory, bans, plan of record. CONFIRMED from my own checkout.

Merge-base `06e45e1` (= `origin/main` tip). Diff is **exactly four files, 2269 insertions, 0
deletions**: `experiments/journal/leg_251.md`, `experiments/p2_route_p0t_v1_targetselection.py`,
`writeup/data/p2_route_p0t_v1_targetselection.json`, `writeup/novelty/leg_251.md`. No shared
ledger touched; `plan_of_record.py` not in the diff. The runner **imports** `plan_of_record` and
reads `BANNED` read-only, and writes exactly one path — its own JSON. **No ban lifted, no plan
change taken under this leg's authority.** Re-running the runner reproduces the banked JSON
**bit-identical** (`diff` empty).

---

## C. THE FINDING — certificate obligation #1 names an object that does not exist for this target

This is the one gap, and it is reported unsoftened because it sits in the exact sentence Phase 1
would be authorized from.

`leg_251.md` §3, obligation 1:

> *"**Existence, in interval arithmetic, of a solution of the self-similar profile system *of
> the dissipative equation*** — the enclosed object itself carries the viscous term."*

**At BCG's scaling there is no self-similar profile system of the dissipative equation.**
Measured at source:

* The self-similar reduction `\eqref{eq:DS}` — the autonomous `(W, Z)` ODE system that Thms
  1.1/1.2 solve — is the **Euler** system. That is why the profiles are written `(U^E, S^E)`.
* Dissipation does not enter a stationary profile equation at all. It enters the
  **dynamically rescaled** system as a forcing term, `F_dis`, defined at l.2130 and appearing
  on the right-hand sides at l.2138–2139; l.2142 names it in the paper's own words: *"`F_dis`
  … [is] the **dissipative forcing**"*.
* That forcing is **non-autonomous and exponentially decaying in self-similar time**: the
  bounds at l.3371–3384 all carry an explicit `e^{−δ_dis s₀}` prefactor.
* Consistently, BCG Thm 1.3's conclusion for Navier–Stokes is ***asymptotically*** self-similar
  blow-up (l.203 uses exactly that phrase for the analogous MRRS result; Thm 1.3 item 4 states
  the conclusion as a `t → T` limit onto `U^E`, not as an exact NS self-similar solution).

So the object obligation 1 asks to enclose — a stationary profile of the dissipative equation —
**is not a thing that exists for this target**. The gap the leg correctly quotes from §7 is in
the **stability step**: the `r`-restriction that lets the profile *dominate* `F_dis`. Enclosing
it means enclosing the linearised operator with `F_dis` retained, at an `r` outside the
dominance regime — not enclosing a viscous profile.

**Two mitigating facts, both real.** (i) The leg *describes the architecture correctly* two
paragraphs above the obligation list: *"the computer-assisted part encloses the **inviscid** ODE
profile … and the viscous term is then handled analytically, by a parameter restriction, **in
the stability step**."* So this is an **internal inconsistency in the obligation's wording**,
not a misreading of the papers. (ii) Obligation 4 ("explicit `r`-coverage … not contained in
BCG's dominance regime") is already pointing at the correct locus.

**What it does and does not change.**

* It does **not** change the gate answer. The target is still unclaimed, still un-excluded by
  NRS/Tsai (out of scope, correctly labelled as scope), and the §7 gap is real and open.
* It does **not** touch the honesty framing, the Wall-2 statement, the Leray finding, or the
  Clay-odds discipline — all of which check out.
* It **does** change what Phase 1 should be authorized to build. Taken literally, obligation 1
  would send Phase 1 after a stationary viscous profile that does not exist at this scaling.
  **Before Phase 1 is authorized, obligation 1 should be re-posed** as: a rigorous enclosure of
  the *linear/nonlinear stability step with the dissipative forcing retained*, at a similarity
  exponent outside BCG's dominance regime.

*I have repaired nothing. This is reported for the Decision Maker.*

---

## D. Everything else found, ranked below the finding

1. **Leg 262 does not exist** — the requested cross-check for the fourth survivor could not be
   run. Substituted a direct full-text read of `2607.09619`; 251's characterisation holds
   against it (§B8).
2. **Two cosmetic locator imprecisions**, neither affecting substance: the BCG §7 quote is the
   second, not the opening, sentence of §7; and the leg-257 clause pairs "`|x|⁻⁴` tail" with
   "fitted exponent −3.000000" without distinguishing `∇v` from `v`.
3. **Scope caveat on "nobody has enclosed it"** (§B3): verified at source for the named
   companion only, not by an independent forward sweep.
4. **§8 restatement risk** (§A): the gate-answer block names "compressible" without the "not the
   system Clay asks about" clause. Carry the clause.

## E. Summary of standing

| claim | how checked |
|---|---|
| BCG Thms 1.2/1.3 content | **independently re-derived** — full LaTeX source, md5-pinned, theorem numbering counted |
| BCG §7 "restrict `r` … dominates the dissipation" | **independently located**, verbatim, l.2085 |
| CGSS §3.4.2 is a domination-architecture energy estimate | **independently located**, l.2693 |
| `U ∈ L^p ∀p>3` ⇒ Tsai applies, stability-blind | **independently re-derived** from the decay bound; PV quote verified verbatim |
| agreement with leg 253 | **independently checked** against 253's own journal on its branch — genuine, same source, same inference |
| compressible NS has no Leray projector | **independently verified** at source from `\eqref{eq:NS}` |
| Wall-2 side | **independently verified** — BCG radial ODE + CGSS perturbation off the radial profile |
| fourth survivor's three reasons | **independently verified** against PV (Conjecture 1.1, l.232, zero-numerics grep) |
| Entry B block | **independently verified** against live `plan_of_record.BANNED` |
| leg 257's magnitudes | **cross-checked** against 257's journal (251 flags it did not re-derive them; nor did I) |
| territory / bans / plan untouched / JSON reproduces | **independently verified** from my own checkout |
| certificate obligation #1 | **FAILS** — §C |
