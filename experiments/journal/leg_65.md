# Leg 65 — Route-L1G v1: the last two unread Tier-2 papers, read for the weighted-`ℓ¹` no-go and the discrete-ball trap

**Branch** `leg/l1g-v1`. **Exploration leg, claim-bearing, literature only** — no computation,
no new bound, no figure. **Gate: NO.**

---

## Order of work (the discipline, as executed)

1. `plan_of_record.py` — read. `NG` is `NEXT`; every live ban noted. The one that could have
   bound this leg is *no further Route-D bound-sharpening* — **this leg produces no constant and
   resumes no Route-D computation**, so it does not touch it. Also noted: *no gCLM measurement
   leg* (none here — `1908.09385` is a gCLM paper but it is being **read**, not measured
   against), and *grep `capabilities.py` before building anything* (done; line 179 is precisely
   the bookkeeping this leg audits, and nothing was built).
2. `DIRECTION.md` — **has no leg-65 entry.** Its status block still closes the 2026-08-05 cycle
   at leg 57, and its queue runs 58–63. The thesis and the verbatim gate came from the dispatch
   prompt instead. **Flagged for the orchestrator**, same flag leg 57 raised; not worked around.
3. **Novelty pass FIRST**, committed before the writeup (`writeup/novelty/leg_65.md`, commit
   `ccea86a`). Six query records, **links not counts**, verdict `PROCEED`.
4. Full text: four papers fetched, extracted, read; findings appended to the same file
   (commit `c59f6d2`) — it doubles as this leg's technical note, per the dispatch.
5. Quartet: `experiments/p2_route_l1g_v1_lit.py` → `writeup/data/p2_route_l1g_v1_lit.json`,
   then this journal.

## What was read, and at what depth

`bash Papers/fetch.sh 2312.01702 1908.09385 2607.15256 2005.14027` — egress worked on the first
attempt (arxiv.org HTTP 200); all four extracted with `pdftotext -layout`.

| paper | why | depth |
|---|---|---|
| `2312.01702` (Pikeroen et al., log-lattice singularity tracking) | Tier 2, fetched but never read | §2.1–2.5, §3.1–3.4, §4.1–4.5, §5.1–5.3, all 28 references |
| `1908.09385` (J. Chen, dissipative gCLM) | Tier 2, previously read **for computer assistance only** (leg 45) | §1 incl. Thms 1.1–1.5, §2.1–2.6 in full, Appendix A |
| `2607.15256` (Chen–Hou, analytic finite-rank corrections, Jul 2026) | **forward citation** of `1908.09385`; the only methodological CAP paper in the sweep | abstract, §1.1–1.4, §2.1, §4, §5 Step 2 |
| `2005.14027` (Campolina–Mailybaev, log-lattice framework) | **forward-cited** framework of `2312.01702`; the only place a weighted sequence-space law could live | function spaces (37)–(40), local existence (45)–(50), Appendix B Lemma 15 |

## The answer, and the two things that make it worth more than a "no hit"

**NO on both claims.** The details, locators and verbatim quotes are in
`writeup/novelty/leg_65.md`; the machine-readable form is the JSON. Two findings carry the
weight:

* **The near-miss is located, not hand-waved.** `2607.15256` §1.2, eqs (1.17)–(1.18), publishes a
  weight tension of exactly C1's *genre*: one weight exponent squeezed from both sides — finite
  energy forces `β < 1`, while the nonlocal term's constant diverges like `(1−β)^{−1/2}` as `β`
  approaches the ceiling. It is in weighted `L²`/`L^∞` energy spaces, the competing requirements
  are *damping vs. finite energy* rather than *smoothness vs. far-field decay*, and it is
  **resolved by a choice** (take `α` large) rather than stated as a no-go over a class of
  weights. A future write-up of C1 must cite this and say what is different; claiming nothing
  like it is in print would now be false.
* **C2's ambient mathematics is named.** The sampling-discretization literature
  (arXiv:1812.08100, arXiv:2203.07126) is exactly the theory of when a norm sampled at nodes
  controls the continuum norm, and its headline is that this degrades as class smoothness drops.
  That is *why* the discrete-ball trap is true. It is not a publication of the trap — no
  dual/extremizer step inside a certificate, no inflation factor — but C2 should be written as a
  concrete instance of a known phenomenon, not as a discovery of one.

**Magnitudes, since booleans are banned.** 4 papers at full text; 6 query records; 39 forward
citations swept (8 for `2312.01702`, 31 for `1908.09385`), of which **1** was on-topic enough to
fetch. Term counts over the extracted texts, which carry the argument: "weight" occurs **0**
times in `2312.01702`, **14** in `1908.09385`, **108** in `2607.15256`, **1** in `2005.14027`;
"computer-assist" **0 / 0 / 12 / 0**; "duality" **0** in all four. Chen's two weights differ by
exactly `x^{−4}` (`φ = ψ/x⁴`, eq. 2.12); Chen–Hou's singular weight is order `|x|^{−3}` with a
required-vs-preserved vanishing gap of `O(|x|³)` against `O(|x|²)`.

## What this changes, and what it does not

* **`solver/holder_norms.py`: no change, and none made.** Read only, as the territory requires.
  Its docstring states the v3 no-go as *derived here* and makes no novelty claim, so the gate's
  no-branch leaves it correct as written.
* **`capabilities.py` line 179 needs one word changed, and it is not mine to change.** It says
  the weighted-`ℓ¹` no-go "is derived here and is UNSEARCHED at primary source". After this leg
  the accurate wording is **searched at primary source and not found**, over five papers
  (`2302.12877`, `2312.01702`, `1908.09385`, `2607.15256`, `2005.14027`). Same for
  `LITERATURE_CHECK.md`'s row (`discrete-ball trap, weighted-ℓ¹ no-go, elasticity | Route-D v3/v6
  | 2302.12877 — fetched, NOT read | unsearched`) and `solver/literature_gates.py` line 599–600,
  which still says "(Tier 2, fetched, NOT read closely)". **All are integration-owned or outside
  territory — handed to the orchestrator, not edited here.**
* **The Route-D ban is untouched.** No bound was computed, sharpened or re-opened; `B` remains
  dead on all three DOF regardless of this leg's answer, exactly as the dispatch pre-committed.
* **Tier 2 is now fully read.** `PHASE2_P2_NOTES.md` §31 and `Papers/MANIFEST.md` both record
  Tier 2 as "fetched and text-extracted but NOT read". With leg 45 (`2302.12877`) and this leg
  (`2312.01702`, `1908.09385`), that sentence is spent. The orchestrator may want the manifest's
  status line updated.

## Honest residual

Absence over five papers is not proof. The two directions classified but **not** read at full
text, recorded so nobody claims they were: the sampling-discretization corpus (C2's ambient
mathematics), and the `ℓ¹`-Wiener CAP corpus that uses geometric weights `ν > 1` — a regime that
avoids C1's algebraic-decay setting by construction, which is an *explanation* for why nobody has
had to state C1, not a search result.
