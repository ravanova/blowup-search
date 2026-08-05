# Leg 74 (Route-EXT) — novelty pass and literature watch: has anyone certified `HL_S2_nonsymmetric` since April 2026?

**Pass date: 2026-08-06.** This leg is a literature watch, so the novelty pass and the leg's
deliverable are the same search — but they answer two different questions and both are recorded
separately below:

1. **Novelty of the *method*** (§0) — is "check whether the target ledger's rank-1 entry has gone
   stale" a thing this repository already did? **No, and that is the whole point of the leg**; but
   this leg claims **zero mathematical novelty**. It discovers nothing about the Hou-Luo model.
   Its output is a *dated absence*, which is a fact about the literature, not about fluids.
2. **The gate** (§1–§4) — the search itself.

Query strings, endpoints and links (not counts, per this directory's README rule after leg 53)
are in `experiments/p2_route_ext_v1_target_watch.py` and re-emitted to
`writeup/data/p2_route_ext_v1_target_watch.json`. Every arXiv-API URL there re-runs verbatim.

---

## 0. What this leg claims, and what it does not

**Claimed:** that as of **2026-08-06**, on six independent channels, the published record
contains **zero** certificates — computer-assisted or analytic — for the non-symmetric
Scenario-2 self-similar profile of the 1D Hou-Luo model reported in Chen-Huang-Li
arXiv:2604.01868.

**Not claimed:** anything about whether such a certificate is *possible*, anything about the
profile itself, and — importantly — anything about work that exists but is unposted. The gate
asks about the *published* record and that is exactly the scope of the answer.

**Not touched:** `solver/target_selection.py`. It was read for the ledger entry's exact fields
and never opened for writing; leg 63 (M2) owns that file, and any ledger edit this watch implies
is that leg's to make. This watch implies **none** — see §4.

`capabilities.py` was grepped first, as the plan of record requires. `HL_S2_nonsymmetric` appears
at lines 130, 230 and 297 (the radii polynomial closing at n=201/401/801; the compactified-basis
coefficient decay; the bordered steady system of Route-PORT legs 46/47), and
`solver/target_selection.py` is registered at line 340. Nothing was built, so nothing was
rebuilt.

---

## 1. The gate, answered

> **Has a certificate (computer-assisted or analytic) for arXiv:2604.01868's
> `HL_S2_nonsymmetric` profile been published, by Chen-Huang-Li or anyone else, since April
> 2026?**

**NO.** Six channels, **0 of 6** returning a candidate. The object has now stood open for
**126 days** past its announcement.

| # | channel | what was enumerated | candidates found |
|---|---|---|---|
| C1 | the source paper itself | version history of arXiv:2604.01868 | **0** |
| C2 | the three authors | arXiv feeds for Chen / Huang / Li + Huang's own page | **0** |
| C3 | the whole "Hou-Luo" corpus | every arXiv entry matching `all:"Hou-Luo"`, date-descending | **0** (1 new paper, wrong object) |
| C4 | the CAP corpus | `abs:"computer-assisted" AND abs:"self-similar"`, date-descending | **0** (2 new papers, neither Hou-Luo) |
| C5 | the citation graph | Semantic Scholar citations of 2604.01868 | **0** (weak channel — see §3) |
| F1 | the likeliest certifier | Jiajie Chen's feed (author of the 2021 Hou-Luo CAP) | **0** (5 new papers, all aimed elsewhere) |

C1–C4 and F1 are each sufficient on their own. C5 is corroborating only and is explicitly *not*
load-bearing.

---

## 2. The channels, with their magnitudes

### C1 — the source paper has not moved

`arXiv:2604.01868` is still at **v1**, sole submission **2 Apr 2026**, comment field
`51 pages`, **no journal-ref**, no DOI beyond the arXiv DOI. That is **0 replacements in 126
days**. Its abstract still says *"numerically demonstrate"* and *"a numerical investigation"*;
there is no proof claim of any kind attached to Scenario 2.

This matters more than a null result usually does. The single most likely route to a certificate
for a numerically-reported profile is the *same authors* upgrading their own preprint — a v2
carrying a proof, or a companion paper. Neither exists.

### C2 — the authors have posted nothing since

| author | most recent arXiv submission | submissions after 2026-04-02 |
|---|---|---|
| De Huang | **2604.01868 itself** | **0** |
| Bojin Chen | **2604.01868 itself** | **0** |
| Xiangyuan Li | **2604.01868 itself** | **0** |

De Huang's next-most-recent is `2603.25104` (gCLM singular profiles, 26 Mar 2026) — i.e. the
Scenario-2 paper is the *terminal* item in his feed, not a step in an ongoing series that has
since continued. His maintained research page lists 2604.01868 under **"Preprints"**, unchanged,
with **0** follow-up or companion entries and **0** items carrying proof/verification language
for the Scenario-2 object.

### C3 — the entire "Hou-Luo" corpus since April 2026 is **one** paper, and it is a different object

A date-descending enumeration of every arXiv entry matching `all:"Hou-Luo"` returns exactly
**1** submission after the source paper:

> **arXiv:2605.16322** (Yaoming Shi, 5 May 2026) — *"A unified Boussinesq–Euler formulation and
> finite-time blow-up for a Hou–Luo type boundary-jet system"*

It proves finite-time blow-up for a **closed boundary-jet model** `(Q0)` on a periodic interval,
by a **Riccati argument** in the Choi–Hou–Kiselev–Luo–Šverák–Yao line. It is disqualified as a
certificate for the ledger's rank-1 object on three independent counts, and its own abstract
supplies the cleanest one verbatim:

> "The theorem is therefore a blow-up result for the closed boundary-jet model, not for the
> unrestricted Boussinesq or Euler systems."

The three counts: (i) different object — a first-order-Taylor-truncated boundary jet, not the
Hou-Luo self-similar profile; (ii) it is not about a *self-similar profile* at all, so it cannot
certify one; (iii) it does not cite 2604.01868 and does not mention a non-symmetric profile.

**Read this the right way.** "One new Hou-Luo paper in four months" is not evidence of a quiet
field — the Hou-Luo/Boussinesq singularity area is extremely active right now (see F1). It is
evidence that the activity has moved to 3D Euler and to methods, and that *nobody has picked up
the Scenario-2 object*.

### C4 — the CAP corpus since April 2026 contains no Hou-Luo entry

Enumerating `abs:"computer-assisted" AND abs:"self-similar"`, date-descending, gives **2**
submissions after 1 Apr 2026; **0 of 2** concern the 1D Hou-Luo model.

| arXiv | date | authors | topic | Hou-Luo? |
|---|---|---|---|---|
| 2607.27072 | 2026-07-29 | Angerer, Kistner, Schörkhuber | corotational harmonic map heat flow shrinker | no |
| 2607.15256 | 2026-07-16 | **Jiajie Chen, Thomas Y. Hou** | analytic finite-rank corrections for singularly weighted estimates in the 3D Euler CAP | no |

The Chen–Hou entry is the **nearest miss** and deserves to be named precisely, because a careless
reading of its title could be mistaken for the certificate this leg is looking for. It is a
**methods review** of the low-rank-correction technique from [ChenHou2023a, ChenHou2023b] — the
trick that enforces, analytically, the local vanishing conditions that singular weights require
and that neither the equations nor a numerical construction preserve. By its own abstract it
**certifies no profile**; it reviews machinery. It mentions neither the 1D Hou-Luo model nor
arXiv:2604.01868.

*(A note for a future leg, not a claim of this one: 2607.15256's subject — enforcing exact local
vanishing conditions that a numerically constructed profile does not automatically satisfy — is
in the same family of difficulty as this repository's own bordered-system troubles. It is
recorded here as a pointer, unevaluated.)*

### F1 — the false positive that had to be cleared

**Jiajie Chen** is the co-author of the existing Hou-Luo CAP (arXiv:2106.05422, with Hou and
Huang) and therefore the single most likely person on earth to certify this object. He has **5**
submissions after 1 Apr 2026 — a rate of one paper per ~25 days — and **0 of 5** target the 1D
non-symmetric profile:

| arXiv | date | subject |
|---|---|---|
| 2607.15256 | 2026-07-16 | CAP methods review (= C4 above) |
| 2606.18152 | 2026-06-16 | a new class of Euler explosions |
| 2605.15149 | 2026-05-14 | 3D Euler `C^{1,1/3-}` asymptotically self-similar blowup, I |
| 2605.15130 | 2026-05-14 | 3D Euler `C^{1,1/3-}` asymptotically self-similar blowup, II |
| 2605.00808 | 2026-05-01 | smooth and stable Euler implosions |

The correct summary is **not** "nobody was working nearby." The correct summary is that the
nearest expert is highly active and aiming entirely elsewhere — at 3D Euler and at compressible
implosion/explosion — while the 1D Scenario-2 profile sits untouched.

---

## 3. What the search cannot see — recorded, not hidden

Three limitations, stated so that a later leg re-running this watch knows exactly what it is
re-running:

1. **The arXiv API's `all:` and `abs:` fields search metadata, not full text.** C3 and C4 would
   miss a certificate whose title *and* abstract avoid both the string "Hou-Luo" and the string
   "computer-assisted". This is a real hole. It is covered from the other three directions — the
   source paper (C1), the authors (C2) and the citation graph (C5) — which is why no single
   channel is treated as sufficient here.
2. **C5's zero is weak evidence and is labeled as such.** Semantic Scholar's citations endpoint
   for arXiv:2604.01868 returns **zero** citing works, but a **126-day-old** preprint sits inside
   S2's indexing lag, and the paper-record endpoint (which would have confirmed the paper is
   indexed at all) returned **HTTP 429** on retry. A zero-citation count from a possibly
   unindexed record is a false negative waiting to happen. It corroborates C1–C4; it does not
   carry the answer.
3. **A certificate could exist unposted** — in review, in a seminar talk, on a personal page not
   enumerated. The gate asks about the *published* record as of the pass date, and that is the
   claim's scope.

None of the three moves the answer, because C1 (the source paper never upgraded) and C2 (all
three authors silent for 126 days) are metadata facts that no full-text gap can overturn.

---

## 4. Consequences

### For the target ledger — no action, and none taken

`solver/target_selection.py`'s `TARGET_LEDGER` rank-1 entry:

```
"id": "HL_S2_nonsymmetric",
"source": "arXiv:2604.01868 sections 2.5 and 4",
"certified": "NO",
```

is **confirmed current as of 2026-08-06**, not stale. The gate's **no-branch** lands: bank the
dated watch, change nothing. This leg makes no edit to that file, which is leg 63's (M2)
exclusively.

**The confirmation extends to rank 3 for free.** `Boussinesq_S2_nonsymmetric` (`certified: NO`)
draws on section 6.2 of the *same* paper. Channels C1–C4 sweep the paper and the corpus, not one
profile, so the 2D Scenario-2 object is equally uncertified as of the same date. Two ledger rows
are re-dated by one search.

### For Route-PORT — the four-leg spend is not externally mooted

Legs 44–47 stalled **1.55e+08 ball radii** outside the truncated object (leg 46), and leg 47
measured the reach trend at **+0.47 decades per unit ρ** — the *wrong sign*, i.e. extending the
domain makes the gap worse. That stall stands as this repository's own measured wall. Nothing has
since closed the object from the outside, so the four legs bought a wall, not a duplication.

The negative is worth stating with its magnitude rather than as a shrug: **126 days open, zero
published attempts by anyone, from a field posting a paper every 25 days in the immediate
neighbourhood.** That is a statement about how expensive the three-modulation-constant bordered
shape (`c_l`, `c_ω`, `c_r` — no symmetry point to pin the translation) is to certify, not about
how uninteresting it is. The repository's own experience and the field's silence agree on the
same object being hard, which is mild external corroboration for the Route-PORT wall — and is
recorded as *corroboration*, not as proof of anything.

### For a future re-run

This watch is cheap and should be repeated rather than trusted indefinitely. The re-run is:
execute the URLs in `ENDPOINTS` in `experiments/p2_route_ext_v1_target_watch.py`, compare against
the banked counts (**v1 / 0 / 0 / 1 / 2 / 0 / 5**), and any number that has moved is the thing to
read. The tripwire with the best signal-to-noise is **C1**: a v2 of 2604.01868, or any new
submission from De Huang, is the event that would most likely carry the certificate.

---

## 5. Novelty verdict

**Zero mathematical novelty claimed.** No result, bound, profile or method here is this
repository's. Every fact in §2 is a metadata reading of someone else's published record, dated
and linked so it can be audited or re-run.

The one thing that is genuinely this leg's own is the **dated absence** and its magnitudes — the
126-day window, the 0-of-6 channels, the 1-new-Hou-Luo-paper-and-it-is-a-different-object, the
5-papers-from-the-likeliest-certifier-all-aimed-elsewhere. That is a fact about the state of the
literature on 2026-08-06 and nothing more, and it should be cited as such: **not** as evidence
that the object cannot be certified.
