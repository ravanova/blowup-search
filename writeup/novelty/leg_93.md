# Leg 93 — Route-EXT5 novelty pass / literature-watch query log

**Pass date: 2026-08-06.** Watched object: `arXiv:2604.09949`, "Stable Finite-Time
Singularity Formation for 3D Navier–Stokes via 5D-Lifted Axisymmetric Reductions",
Rishad Shahmurov, single author, v1 submitted **2026-04-10**.

**Gate (verbatim).** "Since arXiv:2604.09949 was posted, has any independent group
published a confirmation, refutation, retraction, or correction of its 3D NS
self-similar singularity claim?"

**Answer: NO — no *independent* verdict exists, on four channels, after 118 days.**
**But the watch turned up something the gate did not ask for and that is larger than
what it did ask for: the author has since published six papers claiming the LOGICALLY
OPPOSITE result, using the SAME 5D-lifted machinery, without ever citing 2604.09949.**

This log records links and query strings, not counts, per this directory's README.

---

## Part 1 — the query log

### W1 — web search
Query: `arXiv 2604.09949 Shahmurov "Stable Finite-Time Singularity" 3D Navier-Stokes
refutation error`

Links returned:
- https://arxiv.org/abs/2604.09949
- https://arxiv.org/html/2604.09949v1
- https://arxiv.org/pdf/2604.09949
- https://arxiv.org/abs/2107.06509 (Hou, potentially singular behavior of 3D NS)
- https://arxiv.org/pdf/2112.14917
- https://arxiv.org/pdf/math/0504219
- https://arxiv.org/abs/1811.03304

Verdict: every return is the source paper itself or pre-existing, unrelated NS
near-singularity work. **No critique, no comment, no response paper.**

### W2 — web search
Query: `Shahmurov Navier-Stokes singularity claim 2026 contradictory global regularity
preprints discussion`

Links returned:
- https://arxiv.org/html/2604.21213
- https://arxiv.org/html/2605.01873
- https://arxiv.org/html/2605.01875
- https://arxiv.org/html/2605.09797v1
- https://arxiv.org/pdf/2605.04181
- https://arxiv.org/pdf/2605.04526
- https://arxiv.org/html/2604.09949

Verdict: **this is the query that broke the leg open.** Every hit is by the same
author. Nothing by anyone else. The "discussion" the query asked for does not exist;
what exists is the author's own contradictory corpus.

### W3 — web search
Query: `MathOverflow OR blog 2026 "Navier-Stokes" singularity preprint computer-assisted
Newton-Kantorovich claim flawed backward self-similar Necas Ruzicka Sverak excluded`

Links returned (three successive rounds):
- https://arxiv.org/html/2606.07501 (non-uniqueness, axisymmetric swirl-free NS)
- https://arxiv.org/pdf/2606.25341 (Runlong Yu, structural audit of NS obstruction calculus)
- https://arxiv.org/pdf/2606.12756 (invisible defect cascades for NS regularity)
- https://arxiv.org/pdf/2509.25116 (nonuniqueness of Leray–Hopf solutions)
- https://arxiv.org/pdf/2510.20757
- https://arxiv.org/pdf/2101.03727
- https://navier-stokes.dev/
- https://terrytao.wordpress.com/wp-content/uploads/2024/03/machine-assisted-proof-notices.pdf

Verdict: **no MathOverflow thread, no blog post, no commentary of any kind on
2604.09949.** The nearest candidate, arXiv:2606.25341, was opened and cleared — see E5.

---

## Part 2 — the structured channels (these re-run verbatim)

### E1 — the source paper has not moved, and has not been withdrawn
`https://export.arxiv.org/api/query?id_list=2604.09949`
`https://arxiv.org/abs/2604.09949`

- Versions: **`v1` only.** The abs page carries the single marker `[v1]` and **no**
  withdrawal notice.
- v1 submitted `2026-04-10T23:03:18Z`; **118 days** elapsed to the pass date.
- **0 replacements, 0 corrections, 0 errata, no journal-ref, no DOI beyond
  `10.48550/arXiv.2604.09949`.**
- Sole author: Rishad Shahmurov. Primary category `math.AP`.

**No retraction and no correction.** The paper is exactly as M-5 audited it.

### E2 — the citation graph is empty, on two independent indexes
`https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.09949/citations?fields=title,year,externalIds,abstract&limit=100`
→ `{"offset": 0, "data": []}`

`https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.09949?fields=title,year,citationCount,influentialCitationCount,externalIds,venue`
→ `citationCount: 0`, `influentialCitationCount: 0`, `venue: ""`,
  `CorpusId: 287425079` — i.e. the paper **is** indexed, so the zero is a measured
  zero and not an indexing miss.

`https://api.openalex.org/works?search=2604.09949&per_page=20`
→ `count: 0` over an explicit **full-text** search
  (`works where full text has (2604.09949)`), not a metadata search.

**Nobody has cited it — including the author.** The OpenAlex channel is the stronger
of the two because it is full text: a paper that discussed 2604.09949 in its body
without formally citing it would still be caught, and none is.

### E3 — the author feed: eight submissions since, six of them claiming the opposite
`https://export.arxiv.org/api/query?search_query=au:%22Shahmurov%22&start=0&max_results=60&sortBy=submittedDate&sortOrder=descending`

Submissions **after** 2604.09949 (2026-04-10):

| arXiv | date | ver | claim |
|---|---|---|---|
| https://arxiv.org/abs/2604.21213 | 2026-04-23 | v1 | axisymmetric+swirl **unconditional global existence** program, master manuscript |
| https://arxiv.org/abs/2605.01873 | 2026-05-03 | v2 | large-data **global regularity**, 3D NS **full system** |
| https://arxiv.org/abs/2605.01875 | 2026-05-03 | v3 | large-data **global regularity**, axisymmetric swirl class |
| https://arxiv.org/abs/2605.04181 | 2026-05-05 | v1 | Euler blow-up (different system — not contradictory) |
| https://arxiv.org/abs/2605.04526 | 2026-05-06 | v1 | Euler blow-up (different system — not contradictory) |
| https://arxiv.org/abs/2605.09797 | 2026-05-10 | v2 | **global smoothness** for NS, two-part first-threshold |
| https://arxiv.org/abs/2606.07869 | 2026-06-05 | v1 | **global smoothness**, axisymmetric NS with arbitrary swirl |
| https://arxiv.org/abs/2606.07875 | 2026-06-05 | v1 | any hypothetical 3D NS singularity **reduces to** axisymmetric-with-swirl |

And one **before** it, already in the same direction:

| https://arxiv.org/abs/2604.03519 | 2026-04-03 | v1 | "**Unconditional** Axis-Regularity in the 5D Corridor" — 3D axisymmetric NS via the **same** `dμ₅ = r³ dr dz` five-dimensional radial lift, **seven days before** the singularity paper |

### E4 — the later papers use the same machinery and never mention the singularity claim
`https://arxiv.org/html/2605.01873` (fetched)
- Theorem 2.1: "Let `u₀ ∈ C_c^∞(ℝ³)` be divergence-free … Then `T₊ = ∞`" — **the
  solution is global, for the full 3D system.**
- Bibliography: **23 entries, all classical. Zero self-citations. 2604.09949 does not
  appear.** No acknowledgement of any contradiction.

`https://arxiv.org/html/2606.07869` (fetched)
- Theorem 1.1: "Let `u₀ ∈ C_c^∞(ℝ³)` be divergence-free and axisymmetric … Then
  `T* = ∞`."
- §2.4 defines "the five-dimensional lifted measure `dμ₅ = r³ dr ∂z`" and the lifted
  radial Laplacian `Δ₅ = ∂_rr + 3r⁻¹∂_r + ∂_zz`; Lemma 3.1 is the "Lifted G-equation".
  **This is the same 5D lift named in 2604.09949's own title.**
- **No citation of 2604.09949, no retraction, no correction, no acknowledgement.**

### E5 — the nearest independent candidate, opened and cleared
`https://arxiv.org/abs/2606.25341` — Runlong Yu, "A Structural Audit of Navier–Stokes
Obstruction Calculus". Fetched and read: it is a structural analysis of CKN-badness
across scales, concluding "no unconditional single-scale domination by a signed
combined-work detector is available". It **does not mention 2604.09949, Shahmurov, or
any 2026 singularity claim.** Not a response paper. Cleared.

---

## Part 3 — findings, at full depth

### F1 — the gate's literal answer is NO, and it is a well-measured NO
No independent group has confirmed, refuted, retracted, or corrected 2604.09949 in the
**118 days** since it was posted. Four channels agree and none of them is the weak
"absence of search hits" inference that lesson 40's companion warning (M-5's own
recommendation (2)) tells this project never to over-read:

- **E1 is positive evidence, not absence:** the paper's own version history is `v1`
  with 0 replacements and no withdrawal marker. A retraction or correction by the
  author would be *visible here* and is not.
- **E2 is a measured zero, not an indexing gap:** the paper has a Semantic Scholar
  `CorpusId`, so it is in the index and its citation count is 0; and OpenAlex's channel
  is **full-text**, so it would catch discussion-without-citation.
- **E3/E4 are positive evidence about the one person most likely to correct it.**
- **E5 closes the single nearest false positive by reading it rather than by
  pattern-matching its title.**

So the no-branch lands as written: `LITERATURE_CHECK.md`'s `CLAIMED_UNUSABLE` and
`solver/target_selection.py`'s rank-6 "claimed by arXiv:2604.09949" are **confirmed
current as of 2026-08-06**, not stale. This leg edits neither file.

### F2 — the finding the gate did not ask for: a de facto self-refutation
The author of 2604.09949 has, in the 118 days since, published **six** papers whose
conclusions are logically incompatible with it, and the incompatibility is not a
distant one:

- 2604.09949 claims a **finite-time singularity** for 3D NS **via 5D-lifted
  axisymmetric reductions**.
- 2606.07869 claims **`T* = ∞`, global smoothness, for axisymmetric 3D NS with
  arbitrary swirl**, in the **same** `dμ₅ = r³ dr dz` 5D lift.
- 2606.07875 claims **any** hypothetical first singularity of a general 3D solution
  reduces to the axisymmetric-with-swirl class.

Compose the last two and you get global regularity for 3D Navier–Stokes, which
directly negates the first. 2605.01873 does not even need the composition: it asserts
`T₊ = ∞` for the **full system**. And 2604.03519, posted **seven days before** the
singularity paper, was already claiming *unconditional* axis regularity in the *same*
5D corridor — so the contradiction is not a later change of mind that the singularity
paper could have predated innocently; the two lines were running **simultaneously**.

Magnitudes worth stating rather than the boolean:
- **6** contradictory NS papers in **56 days** (2026-04-23 → 2026-06-05).
- The regularity line is **actively maintained** — 2605.01875 is at **v3**, 2605.01873
  and 2605.09797 at **v2** — while the singularity paper has sat at **v1 for 118
  days** with **0** revisions. The author has, in revealed preference, abandoned it.
- **0** of the six cite it; 2605.01873's bibliography has **0** self-citations of any
  kind.

### F3 — what this does and does not do to M-5
**It does not overturn M-5. It strengthens it, and it does so from a direction M-5
did not use.**

M-5's audit was careful in exactly the way that now pays off: it checked the
*arithmetic* and reported that the arithmetic **closes** — `2δMK = 8.9e−5` as printed,
Kantorovich's `2M²Kδ = 4.3e−2` with **23× margin**, `K` reproducing from its own factor
product to `2.2e−4` — and then rested `CLAIMED_UNUSABLE` on two reasons that "stand on
their own and are on the face of the document": **(i)** no verification package
released, **(ii)** its Thm 12.1 reconstructs the exactly-**backward** self-similar
solution excluded by Nečas–Růžička–Šverák and Tsai.

This leg adds a **third**, independent of both, and unavailable in April:
**(iii) the author's own subsequent corpus asserts the negation.** Reason (iii) is
cheaper to state and harder to argue with than either (i) or (ii) — it needs no reading
of the manuscript at all — but it is *weaker as mathematics*, because a
self-contradicting corpus tells you at most that one of the two lines is wrong and does
not say which. It is a **provenance** signal, not a **proof** signal. M-5's reason (ii)
remains the one that says *which*, and it stays the load-bearing reason.

The right way to characterize the state of the field, for `NG` and for any future
write-up, is therefore:

> The 3D-NS finite-time-singularity claim of arXiv:2604.09949 has attracted **no
> independent scrutiny whatsoever** — zero citations, zero commentary, zero response
> papers, 118 days on. It has also not been withdrawn. Its author has meanwhile
> published six papers claiming the opposite conclusion for the same equations using
> the same 5D-lifted formulation, none of which cite it. This repository's own audit
> (M-5) remains, as far as can be determined, **the only independent check of the
> document that exists**, and its verdict `CLAIMED_UNUSABLE` is unchanged and
> reinforced.

### F4 — the honest caveat, recorded rather than hidden
Two limits on the above, stated so a later session does not over-read this leg:

1. **"No independent verdict" is still partly an absence argument.** E2's zeros are
   measured and E1's `v1` is positive evidence, but a referee report, a private
   erratum, a seminar dismissal, or a comment on a version of record would be invisible
   to all four channels. A four-month-old single-author preprint is also within the
   window where indexes lag. What is defensible is the *public* record; that is what is
   claimed, and nothing more.
2. **The self-contradiction is inference, not the author's own statement.** No paper in
   the corpus says "2604.09949 is withdrawn" or "supersedes". The incompatibility is
   read off theorem statements — `T₊ = ∞` / `T* = ∞` versus finite-time singularity —
   which is a strong reading but a reading. It is recorded as **provenance evidence**,
   and it must not be reported as "the author retracted", because he did not.

### F5 — a lesson for the watch discipline
Leg 74 watched an object where the question was "did anyone finish it". This leg
watched an object where the question was "did anyone check it", and the answer — that
**nobody did, at all** — is itself the finding. A claim of this magnitude (a Clay
problem, resolved, with a computer-assisted certificate) drawing **zero** citations in
four months is not neutral silence: it is the field's verdict, expressed by
non-engagement. **Record the silence with its duration, or the next session will read
an unchallenged claim as a surviving one.**
