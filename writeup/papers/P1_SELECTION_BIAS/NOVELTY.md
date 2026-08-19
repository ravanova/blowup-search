# `P1_SELECTION_BIAS` — NOVELTY CHECK (leg 411, unit `PB1`, wave 8)

**VERDICT: BOTH EFFECTS ARE ALREADY IN PRINT. `YES` / `YES`. `P1` IS KILLED.**

The brief pre-committed that a `YES` is a good result and the cheapest possible way to
learn it. It is recorded as such and not as a loss. What follows is the evidence, then
the ceilings on it, then the reach of the instrument — in that order only because the
ceilings were WRITTEN FIRST, in `experiments/journal/leg_411.md` §0.1, before any answer
existed. That file is the pre-registration and it is unedited above its POST-RUN divider.

---

## 1. THE GATE, VERBATIM AS ISSUED

> Are **either** of `P1`'s two effects already in print:
> **(a)** that a **scalar recurrence score used as an admission filter biases the recovered
> orbit set along any coordinate the score is monotone in**; and
> **(b)** that **re-mining a fixed trajectory silently re-finds what the first run already
> found**?
> Search the Chandler–Kerswell / Lucas–Kerswell / Cvitanović line and the wider
> recurrence-mining literature. Answer, PER EFFECT: **is it in print — YES or NO — and if
> YES, in which paper, at which page, stated how strongly?**

Strength grades were fixed in §0.5 BEFORE the corpus was read:

| grade | meaning |
|---|---|
| `S3` | the effect is the paper's own stated result or premise |
| `S2` | stated explicitly as a limitation of the method, in the authors' own voice |
| `S1` | visible in the paper's numbers, and the authors comment on it |
| `S0 ADJACENT` | a neighbouring statement that a motivated reader could stretch; NOT a `YES` |

Two adjudication rules were also fixed in advance and both bind against me here:
**per-guess convergence probability is NOT effect (a)** — a low conversion rate is not by
itself a statement about WHICH orbits survive; and the **`silently` qualifier in effect (b)
is adjudicated separately from the duplication claim itself.**

---

## 2. EFFECT (a) — SCORE-MONOTONE ADMISSION BIAS — **YES**, at `S3`

**DEPTH: FULL TEXT** for every quote below (§3k vocabulary). Pages are PDF pages of the
arXiv version named, hashed in `Papers/MANIFEST.md`. `Papers/` is gitignored, so the quote
text is banked in `writeup/data/p1_novelty_fulltext_v1.json` and survives the PDFs.

### 2.1 The strongest statement: Page, Holey, Brenner & Kerswell (2024)

*JFM* **991** (2024) A10, doi `10.1017/jfm.2024.552`, arXiv:2309.12754v1.

p.2:

> asured with an 𝐿 2 norm– identifying a guess for both the velocity field and period of the
> solution (Viswanath 2007; Cvitanovic & Gibson 2010; Chandler & Kerswell 2013). This
> inherently restricts the approach to lower 𝑅𝑒, as the shadowing becomes increasingly
> unlikely as the Reynolds number is increased due to the increased instability of the UPOs.
> Furthermore, measuring near recurrence with an Euclidean norm is unlikely to be

p.16, §4 — the two shortcomings, stated as the reason a new method is needed:

> & Kerswell 2013; Lucas & Kerswell 2014, 2015). This is similar to the the issues discussed
> around the error metric (2.4) used for the neural networks in §2.2. There are two
> shortcomings with the approach outlined above: (i) it requires a near recurrence to occur,
> which is unlikely at higher 𝑅𝑒 due to the increased instability of the UPOs, and (ii) the
> measure in equation (4.1) is unlikely to be the best measure of similarity

p.18 — and this is the sentence that IS effect (a), in full:

> ulent p.d.f. Similar to the majority of structures found previously via recurrent flow
> analysis (e.g. in particular see Chandler & Kerswell 2013; Lucas & Kerswell 2014), all the
> UPOs found are relatively low dissipation. So, while latent recurrent flow analysis does
> provide access to large numbers of new solutions that a standard recurrent flow analysis has
> not been able to return, it is still constrained by the fact that the

> e numbers of new solutions that a standard recurrent flow analysis has not been able to
> return, it is still constrained by the fact that the more unstable structures are not
> flagged in this approach at all. We now discuss a new method to use latent Fourier analysis
> to isolate smaller-scale solutions which play a substantial role in the high-dissipation
> dynamics, and which is effective at both 𝑅𝑒 = 40 and 𝑅𝑒 = 100.

That last passage states, in the authors' own voice and as the standing limitation of the
whole family of methods: the recovered orbit set is **skewed low in dissipation**, the
skew is **attributed to the recurrence criterion**, and the **more unstable structures are
not flagged at all**. Dissipation and instability are precisely coordinates the recurrence
residual is monotone in. **Grade `S3`** — it is not an aside, it is the paper's premise for
existing.

### 2.2 Lucas & Kerswell (2015), the R–T shadowing argument

*Phys. Fluids* **27** 045106 (2015), arXiv:1406.1820**v1** (see the extraction note in
`Papers/MANIFEST.md`: v2 has a doubled text layer and is unquotable; v1 is quoted).

p.5:

> vered with a small residual are also likely to be visited ‘less closely’, i.e. with a larger
> residual, at about the same time. The variation with period T is marked by a large skew
> toward low periods, i.e. T < 5.0, which reflect close visits to unstable steady and
> travelling wave states. For larger periods (T > 20), there is little variation in the
> numbers of guesses found. This is somewhat counterintuitive since it should bec

p.5 — the authors' own reading of that skew:

> which reflect close visits to unstable steady and travelling wave states. For larger periods
> (T > 20), there is little variation in the numbers of guesses found. This is somewhat
> counterintuitive since it should become less probable that the trajectory shadows a
> recurrent flow the longer its period if the leading Lyapunov exponent is largely period-
> independent. From these guesses we converged 81 unique recurrent flows: see Tab

**Grade `S1`→`S2`**: the skew is in their numbers AND they interpret it as a property of
the recurrence criterion rather than of the flow.

### 2.3 Chandler & Kerswell (2013), the shift-coordinate case

*JFM* **722**:554–595 (2013), arXiv:1207.4682v1.

p.13:

> 35 at Re = 80 and 0.4 for Re = 100: see Table 1. Unfortunately, it was noticed after these
> (Series A) runs had been completed and the guesses tested for convergence that only s = m =
> 0 shifts had been searched over. So the runs were repeated (Series B runs o, p, q and r)
> searching specifically for recurrences which selected either s 6= 0 and/or m 6= 0 to
> minimise R. This was done to indicate

This is effect (a) in its cleanest possible form and it is TWELVE YEARS OLD: the search was
monotone in a coordinate (the shifts `s`, `m`), so the recovered set was confined along that
coordinate, and a second series of runs (Series B) had to be commissioned specifically to
undo it. **Grade `S2`.**

See also p.7, on the choice of threshold itself:

> eriodic orbit (P 1 in Table 2) with period 5.3807 and the next 4 dots with t ∈ [130, 160] to
> a TW (T 1 in Table 2) with phase speed c = 0.0198). The threshold Rthres was chosen
> judiciously to give enough good quality guesses. 3.3. UPO extraction method: Newton-GMRES-
> Hookstep Once a near-recurrence has been found by the above stated criterion, we then
> attempted to find if an exact recurrent flow was lurking nearby in phase spac

### 2.4 Redfern, Lazer & Lucas (2024 preprint) — the effect as an entire research premise

arXiv:2408.05079v1. **PUBLICATION STATUS NOT VERIFIED BY THIS LEG**: the served arXiv
metadata carries NO `journal_ref`. Cited as a preprint and graded as one.

p.2:

> recurrence in direct numerical simulations. Nearly recurrent episodes are identified from
> simulations and then converged using a standard Newton- GMRES-hookstep method, however with
> much greater diversity than previous studies which per- formed this ‘recurrent flow
> analysis’. Unstable periodic and relative periodic orbits are able to be identified which
> span larger values of dissipation rate, i.e. corresponding to extreme bur

p.2:

> greater diversity than previous studies which per- formed this ‘recurrent flow analysis’.
> Unstable periodic and relative periodic orbits are able to be identified which span larger
> values of dissipation rate, i.e. corresponding to extreme bursting events. The triad
> variables are found to provide a more natural way to weight the greater variety of spatial
> modes active in such orbits than a standard Euclidian norm of complex Fo

p.3 — the mechanism named as the norm's fault:

> es because of their choice of norm, this result may be a “false-negative”. Therefore we wish
> to explore the possibility that the recurrence functions used previously are ill-suited for
> high dissipation events. Where a broad range of spatial Fourier modes are active, a simple
> L2 norm of the difference between modes may not capture recurrence in small amplitude, but
> dynamically relevant modes. In order to tackle some of these is

**Grade `S3`, discounted one notch for preprint status.** The paper's whole reason to exist
is that the standard recurrence function's choice of norm decides which orbits are
recoverable. That is `P1`'s effect (a) as a research programme, not as a remark.

### 2.5 What did NOT count, by my own rule

Page & Kerswell, *JFM* **886** (2020) A28 (arXiv:1906.01310v1), p.2:

> Kerswell 2013). The resulting set of candidate orbits, each augmented with a guessed period
> from the time between two similar states, is then input into a Newton solver. The main
> downside of the approach is that it requires the turbulence to shadow a periodic orbit for
> at least one full cycle, and hence it can be increasingly ineffective as the Reynolds number
> is increased (Chandler & Kerswell 2013). In addition, the sensitivi

Graded **`S0 ADJACENT` and NOT counted as a `YES`**. It is a statement about the
*requirement* of shadowing, not about *which* orbits the requirement selects. §0.5's rule
was written before the corpus was read specifically so that this kind of near-miss could not
be quietly promoted, and it is recorded here as not promoted.

---

## 3. EFFECT (b) — RE-MINING RE-FINDS — **YES** on the duplication claim, **NO** on `silently`

### 3.1 Chandler & Kerswell (2013), p.14, §4.2

> a very efficient DNS code was important for this work. Table 1 also indicates the conversion
> rate of near-recurrences guesses to exactly recur- rent solutions. There is considerable
> duplication of such solutions so that a much smaller set of distinct recurrent structures is
> obtained.

> cates the conversion rate of near-recurrences guesses to exactly recur- rent solutions.
> There is considerable duplication of such solutions so that a much smaller set of distinct
> recurrent structures is obtained.

And the effect is QUANTIFIED in their Table 1, which this leg re-read at primary rather than
taking from our own record. At `Re = 60`, Series A runs `e`, `f`, `g`: **102 / 104 / 78
near-recurrence guesses yielding 64 / 67 / 58 convergences**, from which a much smaller set
of DISTINCT structures survives. Series B run `p`, `Re = 60`: **163 guesses, 7 convergences**
(the `4.3%` that our own record has been quoting since leg 358). **Grade `S3`.**

### 3.2 Lucas & Kerswell (2015), p.5 — the load-bearing sentence

> v exponent is largely period-independent. From these guesses we converged 81 unique
> recurrent flows: see Table IV in appendix B and figure 2. At low periods, there was a large
> repetition of the converged solutions already found in [6] (E1, T 1, T 3, T 4, R7, R8 and
> symmetry group permutations thereof) and so only about a third of the guesses with T < 5.0
> were processed. Likewise for T > 60.0, no recurrences with R < 0.25 conve

Reference `[6]` there is Chandler & Kerswell, *JFM* **722**, 554 (2013) — verified in the
bibliography at v1 p.21, not inferred:

> ). [4] G. Kawahara, M. Uhlmann, and L. van Veen, Annual Review of Fluid Mechanics 44, 203
> (2012). [5] P. Cvitanović, Journal of Fluid Mechanics 726, 1 (2013). [6] G. J. Chandler and
> R. R. Kerswell, Journal of Fluid Mechanics 722, 554 (2013). [7] E. Hopf, Commun. Appl. Maths
> 1, 303 (1948). [8] R. Artuso, E. Aurell, and P. Cvitanović, Nonlinearity 3, 325 (1990). [9]
> R. Artuso, E. Aurell, and P. Cvitanović, Nonlinearity 3, 361

This single sentence contains BOTH gate effects at once: re-mining re-found what run one
already had (**effect b**), and the response was to filter on `R` and `T` — which is
**effect (a)** being deliberately applied as a resource-allocation tool. **Grade `S3`.**

### 3.3 The head-to-head number

Redfern, Lazer & Lucas, arXiv:2408.05079v1 p.13, comparing their yield against the standard
`L2` recurrence function at identical parameters:

> us many which converge to known equilibrium and travelling wave solutions). For context [4],
> at the same parameters, from a DNS of 105 time units, were able to obtain 58 unique
> recurrent flows. Moreover the success of obtaining a greater diversity of solution is
> continued with 14 solutions having high mean dissipation. A. High dissipation orbits In
> order to compare and contrast the higher dissipation orbits to the more regular

`unique` is the operative word and it is the field's own: the count that matters to these
authors is DISTINCT recurrent flows, because they take for granted that a raw mining run
returns the same objects repeatedly.

### 3.4 THE `silently` QUALIFIER FAILS — and this is the finding that hurts

`P1`'s framing is that re-mining **silently** re-finds. That word is **contradicted by the
primary sources.** The duplication is:

* reported openly (`considerable duplication`, CK p.14);
* quantified in a published table (CK Table 1);
* acted upon as a documented methodological decision (LK p.5, skipping ~two-thirds of the
  short-period guesses BECAUSE they were known repeats).

Nothing about it is silent. It is stated, counted, and budgeted for. A `P1` that claimed
otherwise would have been asserting a novelty that its own cited sources refute on the page.
**This is why the check is worth more than the draft would have been.**

---

## 4. CONTROL LEDGER — EVERY CONTROL, AND ONE OF THEM FAILED

### 4.1 Instrument 2 (full text) — the one that adjudicates. 5 planted, 5 fired.

| control | rule | measured | fired as planted |
|---|---|---|---|
| `FT1_positive` — `hookstep` | `docs>=2` | `10` docs | **YES** |
| `FT2_topical_positive` — `recurrent flow` | `docs>=2` | `8` docs | **YES** |
| `FT3_nonsense_negative` — `Grznarov admission funnel` | `docs==0` | `0` docs | **YES** |
| `FT4_and_pair` — `Newton AND Kolmogorov (same document)` | `docs>=1` | `11` docs | **YES** |
| `FT5_substring_trap` — `'bias' as a bare substring vs the given name 'Tobias'` | `at least one doc must hit 'bias' ONLY via 'Tobias'` | `bias` in `3` docs, of which `3` are the name `Tobias` | **YES** |

`FT5` is not decoration. A naive substring count of `bias` over this corpus is dominated by
the GIVEN NAME `Tobias` in the reference lists (Tobias Kreilos, Tobias M. Schneider). Any
unit reporting "`bias` appears N times in the recurrence literature" would have been
reporting bibliography. The trap was planted so that a reader can see it was avoided rather
than having to trust that it was.

### 4.2 Instrument 1 (arXiv metadata) — 7 planted, **6 fired, 1 DID NOT**

| control | planted | measured | fired |
|---|---|---|---|
| `pos_generic` | generic positive: must return thousands, else the endpoint is not answering | `MEASURED` total=`10780` | **YES** |
| `pos_topical` | TOPICAL positive control -- IN THIS LITERATURE, not a generic one.  If the endpoint cannot see this field's own name, its zeros about this field mean nothing | `MEASURED` total=`33` | **NO — DISCLOSED** |
| `pos_topical_2` | second topical positive, on the exact object P1 is about | `MEASURED` total=`26` | **YES** |
| `neg_nonsense` | invented phrase; MUST be exactly 0.  If nonzero the endpoint is fuzzy-matching and every zero below is uninterpretable | `MEASURED` total=`0` | **YES** |
| `and_pair_generic` | THE AND TEST: two phrases certain to intersect.  If 0, every ANDed zero below is an instrument artifact, not a measurement | `MEASURED` total=`96` | **YES** |
| `and_pair_topical` | second AND control, in this leg's own topical vocabulary -- proves the operator works on the words actually being ANDed below | `MEASURED` total=`12` | **YES** |
| `and_pair_effect_vocab` | third AND control, on the phrase the effect batteries lean on hardest | `MEASURED` total=`10` | **YES** |

**`pos_topical` DID NOT FIRE AS PLANTED.** The query `all:"exact coherent structures"` was
planted at `>= 50` and MEASURED `33`. Per §0.2 rule 5 this is DISCLOSED and **the verdicts
that control governs are VOID.** It has NOT been re-planted at a threshold it would pass,
and `pos_topical_2` — which did fire — is **NOT** used to rescue it.

What that voids, precisely: it voids instrument 1. Nothing in §2 or §3 above rests on
instrument 1, which by construction (§0.1 ceiling 2) is **candidate enumeration only** —
the arXiv API searches TITLE/ABSTRACT/AUTHOR/COMMENTS metadata and both gate effects are
METHOD-SECTION statements that no abstract would carry. Instrument 1 pointed at papers;
instrument 2 read them. The verdict is instrument 2's.

---

## 5. THROTTLE LEDGER — NO THROTTLE IS RENDERED AS A ZERO ANYWHERE

Leg 387's exact failure was rendering a non-measurement as a zero. Every query here carries
`MEASURED` / `THROTTLED` / `FAILED`, and `total` is `None` BY CONSTRUCTION unless `MEASURED`.

| arm | queries | MEASURED | THROTTLED | FAILED | measured zeros |
|---|---|---|---|---|---|
| arxiv | 43 | 43 | 0 | 0 | 15 |
| semanticscholar | 8 | 2 | 6 | 0 | 0 |

The 15 arXiv **measured zeros** are measurements — the endpoint answered `200` and served a
total of `0`. They are still nearly worthless as evidence of absence, for the metadata-only
reason above, and §0.1 said so before they were collected.

The 6 Semantic Scholar **throttles are not zeros and are not counted anywhere as zeros.**
Worse, and this is the honest statement: **ALL THREE Semantic Scholar controls throttled**
(`HTTP 429`). The S2 arm therefore has **NO VALIDATED CONTROLS AT ALL**, so its two
`MEASURED` totals (`s2_a1 = 97`, `s2_b1 = 68`) are **UNINTERPRETABLE** and are used for
nothing. They are recorded because suppressing them would be its own distortion.

## 6. SERVED NAMESPACE, VERBATIM FROM THE RAW FEED

```
http://a9.com/-/spec/opensearch/1.1/
```

Read off the response body with `xmlns:opensearch="([^"]+)"`, **not assumed from the
request**, and the total-parsing regex is namespace-AGNOSTIC (`opensearch:totalResults[^>]*>`)
so that a served-namespace change cannot turn into a silent zero. That is the leg-387 fix,
implemented rather than promised. Note also that `http://export.arxiv.org` returns **HTTP
301**; the runner uses `https://` so that no redirect sits between the query and the count.

---

## 7. WHAT THIS INSTRUMENT CANNOT REACH — THE CEILING CLAUSE (leg 348) APPLIES

**A controlled zero is not evidence that nothing is in print, and nothing here is offered as
one.** Both verdicts are `YES`, so no zero is load-bearing in either direction — but the
reach statement is owed regardless, and these were named in §0.1 BEFORE the search:

* **Pre-arXiv literature (before ~1991), entirely.** The cycle-expansion and close-return
  line — Auerbach, Cvitanović, Eckmann, Grebogi–Ott–Yorke, Lathrop–Kostelich — is largely
  1987–1991 journal-only. If effect (a) or (b) was first stated there, THIS UNIT CANNOT SEE
  IT. Both verdicts being `YES` means this ceiling cannot flip an answer; it CAN mean the
  priority I assign is too late.
* **Paywalled journal versions.** Only arXiv preprints were fetched. Page/section numbering
  cited here is PREPRINT pagination, NOT journal pagination, and is labelled as such
  everywhere. No paywall was circumvented and none may be.
* **Books, theses, review chapters not deposited on arXiv.** Cvitanović et al.,
  *Chaos: Classical and Quantum* is a live example: read here only as arXiv chapters.
* **Non-English literature**, and the Japanese UPO line (Kawahara, Kida, van Veen) except
  where it is on arXiv.
* **Anything published after this container's arXiv snapshot** — queries ran 2026-08-19.
* **Semantic Scholar's citation graph**, in practice: throttled out (§5).
* **Full text of anything not in the 13-file corpus.** Instrument 2 is deep and NARROW.
  It reads 12 works completely; it does not read the field.

**NO EXTERNAL CONTACT OF ANY KIND WAS MADE OR ATTEMPTED.** Reading published material is
authorised; contacting an author, group, maintainer or list is not, and remains held. No
email, no issue, no list post, no correspondence of any kind.

---

## 8. CONSEQUENCE FOR `P1`

**`P1_SELECTION_BIAS` HAS NO NOVEL CENTRAL CLAIM AND SHOULD NOT BE DRAFTED PAST ITS TITLE.**

Both effects are in print, at `S3`, in the exact line of work `P1` was going to position
itself against — and one of them (CK 2013, shift coordinates) has been in print since 2013.
The `silently` framing is worse than not-novel: it is **contradicted** by the sources.

What survives, and it is NOT a paper: the programme's own quantitative instance of a
known effect. A known effect measured on a new system is a RESULT for the record, not a
contribution to the literature, and this unit is not authorised to decide it is one. That
call belongs to the Conductor.

**This unit did not draft `P1`, did not soften any of the above, and did not describe the
kill as progress.** It is a `YES`. The brief said a `YES` is a good result. It is recorded
as exactly that and nothing more.

---

*Leg 411, unit `PB1`, wave 8. TIER 2. No `L1→L4` link moved; Clay remains ~0.05%. Scale is
not evidence. Pre-registration and ceilings: `experiments/journal/leg_411.md` §0.*
