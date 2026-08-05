# Leg 82 (Route-EXT3) — novelty pass and literature watch: has anyone certified `Boussinesq_S2_nonsymmetric` since April 2026?

**Pass date: 2026-08-06.** This leg is a literature watch, so the novelty pass and the leg's
deliverable are the same search — but they answer two different questions, and both are recorded
separately below:

1. **Novelty of the *method*** (§0) — is "check whether the target ledger's **rank-3** entry has
   gone stale" a thing this repository already did? **No**, and this leg claims **zero
   mathematical novelty**. It discovers nothing about the 2D Boussinesq equations. Its output is
   a *dated absence*, which is a fact about the literature, not about fluids.
2. **The gate** (§1–§5) — the search itself.

Query strings, endpoints and links (not counts, per this directory's README rule after leg 53)
are in `experiments/p2_route_ext3_v1_target_watch3.py` and re-emitted to
`writeup/data/p2_route_ext3_v1_target_watch3.json`. Every arXiv-API URL there re-runs verbatim.

---

## 0. The novelty pass: what this leg claims, and what it does not

**Claimed:** that as of **2026-08-06**, on **seven independent channels**, the published record
contains **zero** certificates — computer-assisted or analytic — for the non-symmetric,
strictly-positive regular self-similar profile of the **2D Boussinesq** equations reported in
Chen-Huang-Li arXiv:2604.01868 **section 6.2** (their Scenario 2, 2D).

**Not claimed:** anything about whether such a certificate is *possible*; anything about the
profile itself; and — importantly — anything about work that exists but is unposted. The gate
asks about the *published* record, and that is exactly the scope of the answer.

**Prior art inside this repository, and why this leg is not a repeat.** Two dated watches of the
same shape have already run and are on main:

| leg | route | ledger rank | object | dimension | source | verdict |
|---|---|---|---|---|---|---|
| 74 | EXT  | 1 | `HL_S2_nonsymmetric`         | **1D** | arXiv:2604.01868 §2.5 / §4 | NO |
| 77 | EXT2 | 2 | `gCLM_degenerate_one_scale`  | **1D** | arXiv:2603.25104 §4        | NO |
| **82** | **EXT3** | **3** | **`Boussinesq_S2_nonsymmetric`** | **2D** | **arXiv:2604.01868 §6.2** | **this leg** |

Leg 82 shares a *paper* with leg 74 but not a *section*, not an *object*, not an *equation* and
not a *dimension*: leg 74 watched the 1D Hou-Luo model's non-symmetric profile (§2.5/§4); this
leg watches the 2D Boussinesq analogue (§6.2). The two live in different sections of the same
51-page numerical paper and would be certified by different machinery — §6.2 carries a 2D
Biot-Savart law with **no symmetry reduction available** and **three** modulation constants
against the 1D object's two. A certificate for one is not a certificate for the other, so the
watches are genuinely independent. Leg 77 shares neither paper nor object.

**Not touched:** `solver/target_selection.py`. It was **read** for the rank-3 entry's exact
fields and never opened for writing; leg 63 (M2) owns that file, and any ledger edit this watch
implies is that leg's to make. This watch implies **none** — see §5.

**`capabilities.py` was grepped first**, as the plan of record requires ("building a solver
without grepping capabilities.py for the object first" is a standing permanent ban). Result:
`Boussinesq_S2_nonsymmetric` appears **nowhere** in `capabilities.py` — the registered 2D
Boussinesq object at line 88 is explicitly annotated as "the CERTIFIED object", i.e. Chen-Hou's
symmetric profile, which is a *different* object and is the one the plan of record bans as a
target. `solver/target_selection.py` itself is registered at line 353. **Nothing was built, so
nothing was rebuilt.** This leg is pure literature: no computation, no solver call, no gCLM
measurement (the standing ban on further gCLM measurement legs is respected trivially — this leg
touches no model at all).

---

## 1. The gate, answered

> **Has a certificate (computer-assisted or analytic) for arXiv:2604.01868 section 6.2's
> `Boussinesq_S2_nonsymmetric` profile been published since the paper's own date?**

**NO.** Seven channels, **0 of 7** returning a candidate. The object has now stood open for
**126 days** past its announcement (v1: 2026-04-02; pass date: 2026-08-06).

| # | channel | what was enumerated | candidates |
|---|---|---|---|
| C1 | the source paper itself | arXiv submission history of 2604.01868 | **0** — still **v1 only**, no revision in 126 days |
| C2 | all three authors | arXiv API `au:"De_Huang"` (24 entries) and `au:"Xiangyuan_Li" OR au:"Bojin_Chen"` (4 entries) | **0** — no post-2604.01868 filing by any author |
| C3 | the "Hou-Luo" corpus | arXiv API `all:"Hou-Luo"`, date-descending (7 entries, 3 from 2026) | **0** — 2 other 2026 papers, both wrong object |
| C4 | the CAP corpus | arXiv API `abs:"Boussinesq" AND abs:"computer-assisted"` (7 entries, 1 from 2026) | **0** — the 2026 entry is a method review |
| C5 | the citation graph | Semantic Scholar citations endpoint for arXiv:2604.01868 | **0** — `{"offset": 0, "data": []}`, an **empty array**, 126 days after v1 |
| C6 | the 2D self-similar corpus | arXiv API `abs:"2D Boussinesq" AND abs:"self-similar"`, date-descending (2 entries from 2026) | **0** — one is the source paper itself |
| F1 | the open web | targeted search for a CAP on the non-symmetric 2D profile | **0** — returns only the pre-existing corpus |

C1–C4 and C6 are each sufficient on their own. **C5 is corroborating only and is explicitly not
treated as decisive** — the Semantic Scholar index lags arXiv by weeks and an empty citation
array is as consistent with indexing lag as with genuine absence. It is reported because it
*agrees*, not because it *proves*.

---

## 2. The object, verified against the primary source

This leg did not take the ledger's word for what the object is. The repository's local copy
`Papers/2604.01868v1.pdf` was extracted and read directly, and every field of
`solver/target_selection.py`'s rank-3 entry was checked against it:

- **The section is right.** Line 2309 of the extracted text is the heading
  *"6.2. Scenario 2: novel self-similar finite-time blowups with positive regular profiles."*
  Section 6 is the 2D Boussinesq half of the paper (§6.1 is Scenario 1, the singular-profile
  scenario); §2.5 and §4, which leg 74 watched, are the **1D Hou-Luo** analogues. The ledger's
  `"source": "arXiv:2604.01868 section 6.2"` is exact.
- **The object is right.** The paper's own sentence, verbatim: *"Ω converge to a non-symmetric
  regular profile that remains strictly positive throughout the computational domain."* That is
  the ledger's `"2D Boussinesq, the NON-SYMMETRIC regular profile (Chen-Huang-Li Scenario 2, 2D)"`,
  word for word in substance.
- **The published number is right.** The ledger records
  `ratio_cl_over_comega: -2.4489` with the note *"remarkably close to the 1D case"*. The paper,
  verbatim: *"The computed limiting value of c_l/c_ω is −2.4489, which is remarkably close to the
  1D case."* The 1D value it is close to is **−2.5114** (line 1477), which is the rank-1 object's
  number. Both match to all four recorded digits.
- **The modulation count is right.** The ledger records `n_modulation: 3`. §6.2's rescaling
  introduces a **time-dependent spatial shift** r(τ) on top of the usual pair, giving free
  constants **(c_l, c_ω, c_r)** with c_θ = c_l + 2c_ω *determined*, not free. Three. The 1D
  rank-1 object has two. This is the concrete sense in which the 2D object is strictly harder.

**Status in the paper: numerical only.** Section 6.2 reports residual decay (Figure 6.12) and
profile convergence (Figures 6.13–6.14) — evidence, not a theorem. The paper's own framing of
what remains to be done, at line 2069, is that one would want to establish *"stability of (6.2)
around some steady state using a powerful computer-assisted approach"*. That is the certificate
this watch is looking for, described by the discoverers themselves as **not yet done**. The
paper's title ends in *"A Numerical Investigation"*.

---

## 3. The two false friends, and why each is a NO

Both would produce a wrong **YES** from an abstract-only or keyword-only pass. Both were opened
and read.

### FF1 — Chen-Hou, arXiv:2607.15256 (2026-07-16), the newest hit on the CAP channel

*"Analytic finite-rank corrections for singularly weighted estimates in a computer-assisted proof
of 3D Euler singularity."* It is the **only** 2026 entry on channel C4 and the **only** other
2026 entry on channel C6, it is by the authors most likely to certify anything in this area, its
title contains "computer-assisted proof", and its abstract contains "2D Boussinesq". It is not
this certificate, on four independent counts:

- **FF1a — wrong kind of statement.** It is a **review**, not a new theorem. Its own sentence:
  *"In this paper, we review an analytic low-rank correction method first developed in
  [ChenHou2023a, ChenHou2023b]"*, and later *"For completeness, we briefly review the singularly
  weighted estimates…"*. It announces no new certified profile.
- **FF1b — wrong object.** The "2D Boussinesq / 3D Euler stability argument" it reviews is
  Chen-Hou's own **smooth, symmetric** profile — the object the plan of record already records as
  *certified* (arXiv:2210.07191 + Part II) and **bans as a target**. §6.2's object is
  **non-symmetric** and arises from the **singular**-profile scenario.
- **FF1c — the words are absent.** "non-symmetric"/"nonsymmetric" and "singular profile" each
  return **0 hits** on the paper.
- **FF1d — no contact with the discovery.** arXiv:2604.01868 is **not cited**, and none of Bojin
  Chen / De Huang / Xiangyuan Li appear in its references. It does not know this object exists.

### FF2 — Shi, arXiv:2605.16322 (2026-05-05), the only post-dated hit on the Hou-Luo channel

*"A unified Boussinesq–Euler formulation and finite-time blow-up for a Hou–Luo type boundary-jet
system."* It postdates the source paper, it is about the 2D Boussinesq equations, and it contains
a genuine **proved** blow-up theorem. It is not this certificate, on four counts:

- **FF2a — wrong object.** The theorem is for a **closed (1+1)D boundary-jet reduction** (system
  Q0), obtained by truncating the elliptic relation at first order, φ_qq(x,1,t) = 0. The paper
  disclaims the scope in its own abstract, verbatim: *"The theorem is therefore a blow-up result
  for the closed boundary-jet model, not for the unrestricted Boussinesq or Euler systems."*
- **FF2b — wrong kind of result.** It proves *finite-time blow-up* by a **Riccati argument**. It
  certifies no **self-similar profile** at all — there is no profile, no modulation constants, no
  enclosure. §6.2's open question is the existence and stability of a specific profile.
- **FF2c — no computer assistance.** No interval arithmetic, no CAP; a purely analytic Riccati
  estimate in the spirit of Choi-Hou-Kiselev-Luo-Šverák-Yao.
- **FF2d — no contact with the discovery.** It does not cite arXiv:2604.01868.

*(A third 2026 Hou-Luo entry, Rampf-Kolluru arXiv:2601.02464, "Complex-time singular structure of
the 1D Hou-Luo model", is excluded on two counts before its content matters: it is **1D**, not
the 2D object, and it **predates** the source paper by three months — 2026-01-05 against
2026-04-02 — so it cannot answer a gate scoped to "since the paper's own date".)*

---

## 4. What the answer rests on, and how strong each leg of it is

Reported as magnitudes, not booleans:

- **126 days** of arXiv silence on the object, with the source paper at **v1 only** — no revision.
  For calibration, leg 77's rank-2 object *did* get revised at **82 days** (v2, 2026-06-16), so a
  126-day silence in this corpus is a real signal, not merely a short window.
- **28 author-feed entries** enumerated across all three authors; **0** filed after 2604.01868.
  The discoverers have published nothing at all — in any field — since the announcement.
- **3 of 3** 2026 papers in the `all:"Hou-Luo"` corpus accounted for individually and excluded by
  named, quoted grounds; **2 of 2** in the 2D-Boussinesq/self-similar corpus.
- **0 indexed citations** (corroborating only).
- **4 independent exclusion counts** for each of the two false friends — no exclusion rests on a
  single criterion.

**The known weakness of this answer**, stated plainly: every channel is an *absence* argument.
Unlike leg 77 — whose decisive evidence was **positive** (the authors revised the paper and
pointedly left the watched branch as numerics) — this leg has no positive act by the authors to
point at, only 126 days of silence and the source paper's own "A Numerical Investigation". The
strongest positive element available is §6.2's own line 2069, in which the authors describe the
computer-assisted stability proof as the thing one would *want* to do. That is a statement of
intent, not of absence, and it is weaker evidence than leg 77 had. This watch should therefore be
re-asked sooner than the rank-2 one.

---

## 5. Consequence for the ledger — reported, never applied

`solver/target_selection.py` is **leg 63 (M2)'s exclusive territory** and was **not touched** by
this leg under any branch of the gate. For that leg, or a future one:

**Its `Boussinesq_S2_nonsymmetric` entry, field `"certified": "NO"`, is CURRENT as of 2026-08-06,
not stale.** No edit is required. Every other field of the entry (source section, object
description, `ratio_cl_over_comega`, `n_modulation`, the "numerical only" note in `q1`) was
independently verified against `Papers/2604.01868v1.pdf` in §2 and is **accurate**.

**One precision suggestion only**, of the same kind leg 77 raised for rank 2: the entry's
`"source"` field reads `"arXiv:2604.01868 section 6.2"` **without a version**. Only **v1** exists
as of this pass, so pinning it to `2604.01868v1` costs nothing now and makes a future revision
detectable by diff rather than by re-reading. This is a bookkeeping nicety, not a correction —
the field is not wrong.

**Watch metadata for the next re-ask.** Object: `Boussinesq_S2_nonsymmetric`, arXiv:2604.01868v1
§6.2. Last pass: 2026-08-06, verdict NO, 126 days open. Cheapest sufficient re-ask, in order of
value per query: (1) the arXiv abs page for 2604.01868 — a **v2** would be the single strongest
signal, exactly as it was for rank 2; (2) `au:"De_Huang"` date-descending; (3) `all:"Hou-Luo"`
date-descending. Given §4's noted weakness, re-ask on a **shorter** interval than rank 2's.
