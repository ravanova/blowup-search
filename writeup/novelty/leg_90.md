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

---

## 2. The gate, answered

**NO.**  Chen-Huang-Li's Conjecture 2.4 has been **neither proved nor disproved**, by anyone, in
the enumerated corpora, as of **2026-08-06** — **126 days** after `2604.01868v1`.

| magnitude | value |
|---|---|
| channels run | **10** |
| channels returning a candidate | **0** |
| channels sufficient alone (excl. the two citation indexes and the homepage) | **6** |
| versions of the source paper in existence | **1** |
| revisions of the source paper since v1 | **0**, at 126 days |
| author entries enumerated (3 authors) | **30** (24 + 2 + 4) |
| author entries filed after 2026-04-02 | **0** |
| author *revisions* after 2026-04-02 | **1** — `2603.25104` v1→v2, and it is FF3 |
| indexed citations, Semantic Scholar | **0** |
| indexed citations, OpenAlex | **0** |
| independent citation indexes agreeing at zero | **2** |
| false friends opened and excluded on named grounds | **4** |
| out-of-scope items recorded | **2** |

**This watch is two-sided.**  Legs 74/77/82 asked "has a certificate appeared?", a one-sided
existence question where absence means only "nobody has done it yet".  This leg asks whether a
**named conjecture** has been **resolved**, and a *disproof* answers it as loudly as a proof.
The search was run symmetrically: channel 4's corpus literally contains a paper titled
*"Stability vs. instability of singular steady states..."*, so an instability result for the HL
singular steady state would index there; channel 7 sweeps blowup-stability generally; and any
resolution in either direction would cite the source paper, hence channels 8 and 9.  All empty.

---

## 3. The object, verified against the primary source

The ledger's word was not taken for what the conjecture says.  `Papers/2604.01868.pdf` was
re-pulled (`bash Papers/fetch.sh 2604.01868`, 28 MB; `Papers/` is gitignored on purpose) and
`pdftotext -f 1 -l 30` extracted.  **Conjecture 2.4, verbatim:**

> *Conjecture 2.4. The singular steady state* (Ω̄, Θ̄, c̄_l, c̄_ω) *is asymptotically stable. More
> specifically, under suitable normalization conditions, for any degenerate smooth initial data*
> (ω_0, θ_0) *which is sufficiently close to* (ω̄, θ̄) *in **some norm** ‖·‖, the solution of the
> Cauchy problem (2.4) converges to* (Ω̄, Θ̄) *in* ‖·‖*.*

**Some norm.**  The conjecture does not name its own function space.  That is not this
repository's reading of the paper — it is the paper, and it is the single sharpest confirmation
of the rank-4 ledger entry's q2 note, *"the obstruction is not the unknown count, it is the
SPACE"*.  Theorem 2.3 checks out equally exactly: it opens *"In the weak sense"*, which is
precisely what the entry's q1 records.  Section 1's mechanism sentence — the solution *"is
locally unbounded at some point"* and develops *"a local L^p blowup at a later time T > T̃ for
some p > 0"* — is the source of the entry's `p < 2` note, though see §6 for a provenance nicety.

One further thing the primary source makes explicit and the ledger only implies: §2 records that
the **smooth**-profile line used *"a weighted H^1 norm ‖·‖"* and showed the solution stays in a
neighbourhood.  The weighted-H^1 route that worked for the smooth profile is exactly what the
singular profile denies.  That is why Conjecture 2.4 is blocked on a space and Theorem 2.3 was
not.

**Not re-derived here:** the entry's `c_l = 2.0`, `c_omega = -1.0`.  `capabilities.py` line 45
already records `solver/hl_rescaled.py` as validated with *"the exact Thm-2.3 singular anchor is
a steady state on its support"*; re-deriving them would be a computation this leg is not
chartered for.

---

## 4. The four false friends, and why each is a NO

### FF1 — Xu, `arXiv:2607.19762v1` (2026-07-22) — the one that most looks like a resolution

It **proves** stability-flavoured statements: a spectral gap of 1/2 after modulation, full point
spectrum exactly {0, 1} with no embedded eigenvalues, and an exact linear decay rate `e^{-τ/2}`
in closed form.  Excluded on four counts:

* **FF1a wrong PROFILE** — it linearizes about Ω(y) = −y/(y² + 1/4), the **smooth** exact a = 0
  CLM collapse profile, realized on an origin-H² space.  Conjecture 2.4's steady state is
  unbounded at X = 1 and lies in L^p only for p < 2; no origin-H² realization holds it.
* **FF1b wrong MODEL** — CLM/gCLM, a single field.  The HL model carries a second field Θ and a
  second modulation constant c_ω.
* **FF1c the words are ABSENT** — "Hou-Luo"/"Hou–Luo" and "singular steady" each return **0**
  hits in the extracted full text.
* **FF1d no CONTACT** — `2604.01868` is not cited.  It cites the sibling `2603.25104` at
  reference [7], which is the only reason it enters this leg's corpus at all.

**Already known here, and not re-opened:** `Papers/fetch.sh` lists `2607.19762` in TIER1 and
`Papers/MANIFEST.md` gates Route-E v1's spectral picture on it ("already assessed as *likely
pre-empted*").  This leg does not discover it.

> **Flag for the orchestrator, orthogonal to this gate, reported and not acted on.**
> `2607.19762` gives a realization-dependent spectral picture of the **a = 0 CLM linearization
> L_0** — including the non-normality caveat *"a spectral gap does not by itself give a decay
> rate in the X norm"*.  That is the same operator the **NG** stage's no-go is stated about, and
> the same a = 0 object Route-D's NK framing uses.  NG is not this leg's territory and nothing
> here touches it; this line exists so a future NG leg does not have to rediscover the overlap.

### FF2 — Bradshaw-Palmer, `arXiv:2606.22291v1` (2026-06-21)

The only 2026 entry on the "singular steady state" + "stability" channel, and its abstract
announces the gate's own words: *"The second objective of this paper is to establish asymptotic
stability for many of these solutions"*.  Excluded on three counts:

* **FF2a wrong EQUATION** — 3D **stationary** Navier-Stokes: Landau solutions, Squire's
  solution, Serrin's swirling vortex.  A viscous stationary problem.  The HL model is a 1D
  inviscid transport model and Conjecture 2.4 lives in dynamic-rescaling coordinates around a
  **blowup** profile.
* **FF2b wrong SINGULARITY** — an isolated point singularity at the origin of a stationary flow
  ("Type III" in that literature).  Conjecture 2.4's profile is singular at X = 1, the edge of a
  one-sided support.
* **FF2c no CONTACT** — `2604.01868` is not cited; the Hou-Luo model does not appear.

### FF3 — Huang-Tong-Wang, `arXiv:2603.25104`, **revised to v2 on 2026-06-16** — the sharpest one

By the source paper's own **lead author**; revised **75 days after** the source paper; and its
abstract says *"we rigorously prove the convergence of the outer profile to an explicit singular
function in self-similar coordinates"*.  A rigorous convergence-to-a-singular-profile theorem by
De Huang, filed after the conjecture, is exactly the shape a YES would have.  It is not one:

* **FF3a wrong MODEL** — the generalized Constantin-Lax-Majda model with parameter a.  Its own
  title says so.  Not the Hou-Luo model.
* **FF3b wrong STATEMENT** — at a = 0 it proves convergence of the **outer** profile for the
  constructed solution, plus existence of the inner traveling wave by a fixed-point method.
  Neither is an asymptotic-stability statement about a steady state under perturbation of
  initial data, which is what Conjecture 2.4 asserts.
* **FF3c its own stability language is NUMERICAL, and says so** — verbatim: *"This indicates
  that the self-similar blowup with a singular profile is robust with respect to the choice of
  degenerate initial data, hence **suggesting** stability of the observed blowup."*  Suggesting,
  from two initial-data cases agreeing to numerical error.  That is the same evidentiary status
  Conjecture 2.4 already has.
* **FF3d no CONTACT** — `2604.01868` is not cited (v1 predates it by 7 days, and the **v2
  revision did not add the citation**).  "Hou-Luo" appears **once** in the extracted full text,
  listing prior work; "Conjecture 2.4" appears **nowhere**.

**Read the other way, FF3 is this leg's strongest positive datum** — the thing leg 82's rank-3
watch explicitly said it lacked.  The lead author *did* touch a sibling paper 75 days after
announcing Conjecture 2.4, and did not use the occasion to announce a resolution, add a
citation, or upgrade the conjecture's status.  That is an **act**, not a silence.

### FF4 — Shi, `arXiv:2605.16322v1` (2026-05-05)

The **only** entry in the entire "Hou-Luo" corpus filed after the source paper, and it carries a
genuine proved theorem.  Excluded on four counts: **FF4a** wrong object — a closed (1+1)D
boundary-jet reduction (system Q0, the truncation φ_qq(x,1,t) = 0); **FF4b** wrong question —
finite-time blow-up by a Riccati argument, no stability claim about any steady state and no
profile exhibited at all; **FF4c** its own abstract disclaims its scope (*"The theorem is
therefore a blow-up result for the closed boundary-jet model, not for the unrestricted
Boussinesq or Euler systems."*); **FF4d** no contact — `2604.01868` is not cited.

Leg 82 excluded this same paper for the **rank-3** object on *different* grounds.  The grounds
differ because the watched object differs; it is a false friend for both, non-identically.

### Out of scope before content matters

`https://arxiv.org/abs/2601.02464` (Rampf-Kolluru, 2026-01-05) **predates** the source paper by
three months — a gate scoped to "since `arXiv:2604.01868`" cannot be answered by it, whatever it
contains.  `https://arxiv.org/abs/2604.16842` (2026-04-18) surfaced on the open-web channel and
postdates the source, but is a **PhD thesis** on NLH / CGL / 3D Keller-Segel with logistic
damping, PINNs and Kolmogorov-Arnold networks: no Hou-Luo model, no singular steady state.

---

## 5. What the answer rests on, and how strong each leg of it is

**Strongest, and sufficient alone.**  Channel 1: the source paper is still at **v1** at 126
days.  Channel 2: **0 of 30** author entries filed after 2026-04-02.  Channels 3–7: five corpus
enumerations, **0** post-source candidates that survive contact with their own abstracts.

**Corroborating only, and explicitly not decisive.**  Channels 8 and 9 — two citation indexes at
zero.  Each lags arXiv by weeks, so either alone is as consistent with lag as with absence.
Their value is that they are **independently built**: "indexing lag" has to be a coincidence
across two different ingest pipelines.  It is still not proof, because both index arXiv and a
common upstream delay is not fully excluded.  Channel 10 — the corresponding author's homepage —
matters for a reason the others cannot cover: authors list submitted-but-unposted work there.
It shows none.

**The known weakness, stated plainly.**  Every channel is an **absence** argument.  What this
leg has that leg 82's did not: (i) a second independently built citation index agreeing at zero,
and (ii) one genuine positive act, FF3's v2 revision.  What it still lacks is any statement *by
the authors* that the conjecture remains open; the evidence is that nobody has said otherwise.

**Why a resolution would matter more here than at ranks 1–3.**  Ranks 1–3 are *uncertified
objects*: an absence answer means only that nobody has done the work, and the ledger entry is
unchanged either way.  Rank 4 is a *named conjecture*.  A **proof** would move
`HL_singular_steady_stability` from "an open problem before the certificate is even posed" to "a
certifiable target with a known function space" — the exact obstruction the entry's q3 gives as
the reason it ranks fourth.  A **disproof** would delete the entry outright, because an unstable
steady state is not a blow-up mechanism.  Either direction is consequential.  Neither has
happened.

---

## 6. Consequence for the ledger — reported, never applied

`solver/target_selection.py` was **read and never written**.  It is parked pending the user's
ruling on leg 63's escalation, and no leg touches it.

**The finding, for leg 63's successor or a future leg to act on:** the rank-4
`HL_singular_steady_stability` entry — `"certified": "NO"`, and q1's *"Stability is an explicitly
stated conjecture with numerical support only"* — is **CURRENT as of 2026-08-06, not stale**.
No edit is required by this pass.

Two precision suggestions, both bookkeeping, neither a correction:

1. The entry's `"source"` field cites the paper **without a version**.  Only v1 exists as of this
   pass, so pinning it to `2604.01868v1` costs nothing and makes a future revision detectable by
   diff rather than by re-reading.  Leg 82 made the same suggestion for the rank-3 entry; it
   applies verbatim here.
2. The entry's q2 note says the profile *"is only in L^p for p < 2"*.  The paper's own phrasing
   in §1 is looser — *"a local L^p blowup ... for some p > 0"* — and the `p < 2` threshold is a
   **consequence of the explicit profile**, not a sentence in the paper.  Recording it as
   *derived* rather than *quoted* would keep the provenance clean.

---

## 7. Re-asking this watch

| field | value |
|---|---|
| object | `HL_singular_steady_stability` (rank 4) |
| source | `arXiv:2604.01868v1` Thm 2.3 (existence) + Conj 2.4 (open) |
| last pass | 2026-08-06 |
| last verdict | **NO — still open** |

Cheapest sufficient channels, in order of value:

1. `https://export.arxiv.org/api/query?id_list=2604.01868` — a v2 is the single strongest
   signal, exactly as it was for the rank-2 object at leg 77.
2. `https://export.arxiv.org/api/query?search_query=au:%22De_Huang%22&sortBy=submittedDate&sortOrder=descending`
3. `https://api.openalex.org/works?filter=cites:W7148668037` — the cheapest single call that
   would surface **any** citing work, in either direction.
4. `https://export.arxiv.org/api/query?search_query=abs:%22singular+steady+state%22+AND+abs:%22stability%22&sortBy=submittedDate&sortOrder=descending`

**Interval: shorter than the rank-3 watch's.**  A named conjecture is a target people aim at,
and the next pass has a cheap, sharp trigger that the certificate watches do not: **any nonzero
`cited_by_count` at all**, in either index.  Both are at zero now.

**What would make this watch unnecessary:** the user's ruling on leg 63's escalation.  If
`target_selection.py` is unparked and the rank-4 entry is retired or promoted on other grounds,
the watch's consumer disappears.
