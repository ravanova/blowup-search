# Leg 90 (Route-EXT4) — novelty pass and literature watch: has Chen-Huang-Li's **Conjecture 2.4** (asymptotic stability of the HL singular steady state) been resolved since April 2026?

**Pass date 2026-08-06.**  Source paper `arXiv:2604.01868v1`, submitted **2026-04-02**.
Elapsed at pass date: **126 days**.

**Gate, verbatim:** *"Has Chen-Huang-Li's Conjecture 2.4 (stability of the HL singular steady
state) been proved or disproved, by anyone, since arXiv:2604.01868?"*

**Answer: NO.**  Ten channels, **0 of 10** produced a resolution in either direction.  The
conjecture is **still open** as of 2026-08-06.

This is a pure literature leg.  Nothing here computes a gCLM quantity, or any quantity at all —
the standing ban on further gCLM measurement legs is respected trivially.  Nothing under
`solver/` is edited; in particular `solver/target_selection.py` is **not touched** (it is parked
pending the user's ruling on leg 63's escalation).

---

## 0. The novelty pass: what this leg claims, and what it does not

**Claims.**  That as of **2026-08-06**, no proof and no disproof of `arXiv:2604.01868`'s
Conjecture 2.4 exists in the enumerated corpora below, and that the four papers which come
closest — the ones an abstract-only or keyword-only pass would return as a YES — each fail on
named, quoted grounds recorded in §3.

**Does not claim.**  That no such result exists anywhere.  A private manuscript, a journal-only
submission, or a preprint filed in the last days before the pass date and not yet indexed would
not be visible to any of these channels.  The channels are enumerations of specific corpora at a
specific date, and the answer is scoped to exactly that.

**Distinctness from legs 74 / 77 / 82.**  Those three watched whether a *certificate* had
appeared for the rank-1, rank-2 and rank-3 target objects — three uncertified-but-not-conjectural
profiles.  This leg watches a different kind of object: a **named open conjecture** with a
stated claim (asymptotic stability), which can be resolved in **either** direction.  Different
object (the rank-4 `HL_singular_steady_stability` entry, the *singular* steady state
`1_{X>1}(X-1)^{-1/2}`, not any regular profile), different question (resolution of a conjecture,
not existence of a certificate), and an independent answer.

---

## 1. The query log — links, not counts

Every arXiv channel is an **enumeration** (`export.arxiv.org/api/query`, sorted by submission
date, descending), not a keyword-luck web search.  All run 2026-08-06.

### Channel 1 — version history of the source paper itself

    https://export.arxiv.org/api/query?id_list=2604.01868&max_results=1

Returned `http://arxiv.org/abs/2604.01868v1`, `<published>2026-04-02T10:25:28Z`,
`<updated>2026-04-02T10:25:28Z`.  **Still v1.  It has never been revised.**

This is the single most informative channel, for the reason leg 77 established: when these
authors change their mind about a conjecture's status, the revision is where it shows.  Here
there is no revision at 126 days.

### Channel 2 — arXiv author enumeration, all three authors, separately

    https://export.arxiv.org/api/query?search_query=au:%22De_Huang%22        -> 24 entries
    https://export.arxiv.org/api/query?search_query=au:%22Bojin_Chen%22      ->  2 entries
    https://export.arxiv.org/api/query?search_query=au:%22Xiangyuan_Li%22    ->  4 entries

**Not one entry, by any of the three, is filed after 2026-04-02, in any field.**  For De Huang
the 24 entries run back to 2011 (two are name collisions — an ALMA receiver paper and a bilayer
manganites paper); `2604.01868` is the newest.  The newest *related* item is
`https://arxiv.org/abs/2603.25104` (v1 2026-03-26, **v2 2026-06-16**) — see FF3, §3.

### Channel 3 — arXiv corpus, the model's own name

    ...search_query=all:%22Hou-Luo%22                     -> 7 entries, 3 from 2026
    ...search_query=ti:%22Hou-Luo%22+OR+ti:%22Hou--Luo%22 -> 6 entries, 3 from 2026

The seven:
`https://arxiv.org/abs/2605.16322` (Shi, 2026-05-05) — the **only** entry filed after the source
paper; `https://arxiv.org/abs/2604.01868` (the source);
`https://arxiv.org/abs/2601.02464` (Rampf-Kolluru, 2026-01-05, predates);
`https://arxiv.org/abs/2308.01528`; `https://arxiv.org/abs/2106.05422`;
`https://arxiv.org/abs/2010.00648`; `https://arxiv.org/abs/1604.07118`.

### Channel 4 — arXiv corpus, the conjecture's own subject matter

    ...search_query=abs:%22singular+steady+state%22+AND+abs:%22stability%22   -> 4 entries

`https://arxiv.org/abs/2606.22291` (Bradshaw-Palmer, 2026-06-21 — the only 2026 entry, and FF2
below); `https://arxiv.org/abs/2309.15633`; `https://arxiv.org/abs/2110.12934`;
`https://arxiv.org/abs/0904.3759`.

### Channel 5 — arXiv corpus, the profile's own adjective

    ...search_query=abs:%22self-similar%22+AND+abs:%22singular+profile%22     -> 4 entries

`https://arxiv.org/abs/2604.01868` (the source, the only 2026 entry);
`https://arxiv.org/abs/2410.21765`; `https://arxiv.org/abs/1306.0859`;
`https://arxiv.org/abs/physics/0410119`.

### Channel 6 — arXiv corpus, the adjacent 1D family

    ...search_query=abs:%22Constantin-Lax-Majda%22                            -> 25 entries

Five from 2026: `https://arxiv.org/abs/2607.19762` (Xu, 2026-07-22 — FF1);
`https://arxiv.org/abs/2604.01244` (Shi, v4 2026-04-22);
`https://arxiv.org/abs/2603.25104` (Huang-Tong-Wang, v2 2026-06-16 — FF3);
`https://arxiv.org/abs/2603.26715` (Shi, v5 2026-07-12);
`https://arxiv.org/abs/2603.06182` (Fujita-Fukuizumi-Sakajo, 2026-03-06, predates).

### Channel 7 — arXiv corpus, stability-of-blowup generally

    ...search_query=abs:%22asymptotic+stability%22+AND+abs:%22blowup%22       -> 20 entries
    ...search_query=abs:%22degenerate%22+AND+abs:%22self-similar+blowup%22    ->  1 entry

Newest in the first: `https://arxiv.org/abs/2603.01924` (wave maps, 2026-03-02, predates).  The
whole list is wave maps / Yang-Mills / NLS / heat-flow blowup stability; no 1D transport model,
no Hou-Luo, no singular steady state.  The second returns only
`https://arxiv.org/abs/2510.25326` (supercritical wave maps with noise, 2025).

### Channel 8 — Semantic Scholar citations of the source paper

    https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.01868/citations

Returned `{"offset": 0, "data": []}` — an **empty array**, 126 days after v1.  The paper record
itself (`.../paper/arXiv:2604.01868?fields=title,citationCount,year`) reports
`"citationCount": 0`.  **CORROBORATING ONLY:** this index lags arXiv by weeks, so an empty array
is as consistent with lag as with absence.

### Channel 9 — OpenAlex cited-by, an *independent* citation graph

    https://api.openalex.org/works/doi:10.48550/arXiv.2604.01868   -> W7148668037, cited_by_count 0
    https://api.openalex.org/works?filter=cites:W7148668037        -> {"count": 0}, results []

A second, independently-built citation index agrees with the first at zero.  Two indexes with
different ingest pipelines both empty is stronger than either alone, and this is the channel
legs 74/77/82 did not run.

### Channel 10 — the authors' own homepage, and open web

    https://sites.google.com/view/de-huang/research

Lists `2603.25104` and `2604.01868` as the only "recent preprints"; nothing newer, and nothing
on stability of a singular steady state.  Two open-web searches
(`Chen Huang Li Conjecture 2.4 stability singular steady state Hou-Luo model 2026 proof`, and
`arXiv 2026 "asymptotic stability" singular steady state 1D Hou-Luo model weak solution proof`)
returned the source paper, `2601.02464`, `2106.05422`, `2308.01528` and unrelated
chemotaxis/Keller-Segel stability work — no resolution, in either direction.
