# Leg 64 — VER-I verification journal (post-landing review, trigger (b))

**Verifier** VER-I. **Branch** `verify/64-a12-review`. **Date** 2026-08-05.
**Subject** leg 64 (Route-A12 v1), already landed on `main` (`bb0ac22`, `cec85ee`).
**Role** report gaps; **repair nothing**. No leg-64 file, no ledger file, and no solver
module was edited by this verifier.

**Headline: gate answer CONFIRMED on both halves. Three defects found, all in §4's "two
traps" and its decoration. None moves the verdict; the largest one makes leg 64's own
conclusion stronger once corrected. Recommend a correction leg, not a rework.**

Full line-by-line report, with every verbatim extract and every line number checked:
`writeup/novelty/leg_64_verify.md`. This journal records how the check was run and what it
cost, so the next verifier does not re-derive the method.

---

## Order of work

1. Read `DIRECTION.md`'s leg-64 entry (L494–513), then the landed quartet.
2. Re-ran the reproduction script; diffed its output against the committed JSON.
3. **Re-fetched all five primary sources from arXiv directly**, rather than reading leg 64's
   extracted notes. This is the part that makes the review independent.
4. Grepped each source for the exact strings and line numbers leg 64 cited.
5. Re-ran the arXiv corpus enumeration from scratch and audited the papers leg 64's
   abbreviated list omitted.
6. Traced the numeric ladder back through `writeup/data/p2_route_h_v1_critical.json`.
7. Wrote both verification files. Committed. Pushed. Did not merge.

## Method note worth banking: egress was OPEN

`Papers/fetch.sh` carries a cached, emphatic diagnosis — "BLOCKED: arxiv.org is not reachable
from this container … verified, do not re-derive" — and instructs the reader to ask the user
to allowlist hosts. **That diagnosis is stale.** Plain `curl` to `arxiv.org` returned `200` on
every one of six requests in this session:

```
curl https://arxiv.org/html/2607.19762v1   -> 200   (1.23 MB)
curl https://arxiv.org/pdf/2607.19762      -> 200
curl https://arxiv.org/pdf/2207.07548      -> 200
curl https://arxiv.org/pdf/1908.09385      -> 200
curl https://arxiv.org/pdf/2010.01201      -> 200
curl https://arxiv.org/abs/2411.01891      -> 200
curl 'https://export.arxiv.org/api/query?...' -> 200
```

Note the asymmetry that probably produced the stale note: **`WebFetch` on an arXiv `/abs/`
page returns only the abstract landing page** (it did so here — the fetcher explicitly
reported it could not see Table 1 or §6.1), whereas **`curl` of `/html/` or `/pdf/` gets the
full text**. The lesson is not "egress is blocked" but "fetch the `/html/` or `/pdf/` URL with
`curl`, not the `/abs/` page with `WebFetch`." Recorded here rather than edited into
`Papers/fetch.sh`, which is outside this verifier's territory — **flagged for the
orchestrator: `Papers/fetch.sh`'s blocked-egress banner should be re-tested and probably
retired.**

Working pipeline, for reuse:

```
curl -sS --max-time 90 -o xu.pdf https://arxiv.org/pdf/2607.19762
pdftotext -layout xu.pdf xu64.txt
```

The `-layout` flag matters: leg 64's line numbers reproduce **exactly** under it, and Table 1's
column structure survives only with it.

## What was checked, and how it came out

**Reproduction.** `python3 experiments/p2_route_a12_v1_alpha_lit.py` regenerates the committed
`writeup/data/p2_route_a12_v1_alpha_lit.json` **byte-identically** (`diff` empty). The script
computes nothing — it re-emits the query log — so the standing gCLM measurement ban is
genuinely respected, as claimed.

**Ladder provenance.** `writeup/data/p2_route_h_v1_critical.json` holds
`0.13277004191934333`, `0.13347014931942064`, `0.1336284588391547`, `0.13368266982772414` at
`K = 96/144/192/240`. Rounded to 6 dp: `0.132770 / 0.133470 / 0.133628 / 0.133683`. Matches
both the JSON and the prose. Spreads recomputed: `9.13e-4` full ladder, `5.5e-5` last two
rungs, `0.133683/5.5e-5 = 2430.6` sigma-free "distance from zero". All three quoted figures
check out.

**Xu, line by line.** All **eleven** cited extracted-text line numbers land on the claimed
content. The `s*(1/2) = 3` sentence (L1795–1796), the Table 1 row `a=0.5`
(`0.5 / 0.3333 / 0.833 / 3.000 / J. Chen [20]: blow-up at s = 2 < 3 (subcritical)`), the
Figure 3 in-plot annotation (`s * (1/2) = 3 (exact)`, L1821), the Table 1 caption, Xu's two
"marginal case is open" sentences, and `Appendix A … at a = 0` (L1984) are **all verbatim
exact**. Xu's `[4]` = LSS and `[20]` = J. Chen, as claimed.

**Exponent dictionary — the step the review was told to scrutinise hardest.** Correct, and
double-pinned independently: (i) Xu writes "for the ordinary Laplacian `s = 2`", which fixes
his `s` as the `Λ`-power, the same gauge as ALS's `σ`, making `s* = 3 ⇔ σ_c = 3` a
like-for-like identity rather than a conversion; (ii) the `a = 0` anchor — Xu's `s*(0) = 1`
against our `σ_c(0) = 1` — agrees, and would **not** agree under the competing `c_l = 2β`
reading that `LITERATURE_CHECK.md` L287–288 itself leaves hedged. Leg 64 asserted the right
branch but did not note that its own source file hedged the question; the resolution is now on
the record.

**Corpus.** Enumeration re-run: `totalResults = 25`, all 25 returned — genuinely complete for
arXiv, and the dissipative subset is the claimed four. Audited the five IDs leg 64's ellipsis
omitted; the only one worth opening (`1907.08748`, Du) is a **2D** CLM generalization, not
dissipative gCLM. ALS §5's four headings, SLSA's abstract, and LSS's single bibliography-only
dissipation hit at L2236 all confirmed exactly as reported.

**Quartet.** All four files present and substantive (502 / 335 / 203 / 148 lines). Every number
in the prose traces to the JSON and through it to Route-H v1.

## The three gaps (detail in the novelty file)

**G1 — Trap 1 misattributes Chen's criticality at `a = 1/2`.** Leg 64 says Chen's norm
criticality gives `γ = |a|^{-1} = 2` there. Chen states that formula **only for `a ≤ −1`**;
for `a > −1` (which includes `a = 1/2`) his own text says `L = Λ`, i.e. `γ = 1`, is the
critical dissipation, from `L^1` conservation. Leg 64 also writes the norm as `L^{|a|^{-1}}`
where Chen writes `L^{|a|}` — the norm index and the dissipation index are reciprocals, and
the leg gave the norm the dissipation's index. The `2` that Xu quotes is not a criticality at
all: it is the full Laplacian Chen **chose** in Theorem 1.1 ("We focus on the full Laplacian
for simplicity"). **Xu's own sentence is correct; the misread is leg 64's gloss on Chen.**
Recorded in both the prose and the JSON (`"chen_norm_criticality_gamma": 2.0`). **Verdict
unaffected — and stronger corrected**, since Chen's own criticality at `a = 1/2` is `Λ^1`, two
units below `σ_c = 3`, rather than one.

**G2 — Trap 2's "1D Oldroyd-B stress model" gloss is not in ALS.** `2207.07548` contains no
"Oldroyd", "viscoelastic", "stress" or "polymer". The load-bearing half of Trap 2 — ALS's
"'marginal' dissipation `σ = 0`", L214 — is verbatim confirmed and the trap is real; only the
parenthetical provenance is unsourced.

**G3 — two trivial mislabels.** (a) LSS's dissipation hit at L2236 cites *Nonlinearity* 33(5)
2502 (2020), which is **Chen's** paper, not ALS's. (b) Q8 is called a "100-result enumeration";
it returned 25 of 25 — complete, which is the better claim.

## Cost and scope

Seven `curl` fetches, four `pdftotext` extractions, one script re-run, ~20 greps. No compute,
no solve, no gCLM measurement. Files written: `experiments/journal/leg_64_verify.md` and
`writeup/novelty/leg_64_verify.md` only. `experiments/JOURNAL.md`, `LITERATURE_CHECK.md`,
`plan_of_record.py`, `CONTINUATION_PROMPT.md`, `PHASE2_P2_NOTES.md`, `DIRECTION.md`,
`capabilities.py`, `solver/critical_dissipation.py` and all leg-64 files: **untouched.**

## Two items flagged for the orchestrator / DM

1. **`G1` warrants a correction leg** — a misread primary source inside the section whose
   purpose is exponent care, recorded in both prose and JSON. It rewrites no banked number.
   `G2` and `G3` should ride along in the same leg.
2. **`Papers/fetch.sh`'s "BLOCKED: arxiv.org is not reachable" banner is stale** and says "do
   not re-derive". It cost this review a moment's hesitation and could cost a future
   literature leg its full-text pass. Re-test and retire.
