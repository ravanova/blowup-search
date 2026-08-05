# Leg 74 — Route-EXT: the target watch, dated

Literature only. Nothing was computed, no solver module was imported, no measurement was made —
the standing gCLM and Route-D bans are untouched by construction. `solver/target_selection.py`
was **read** for its rank-1 ledger fields and never opened for writing; that file is leg 63's
(M2). Runner: `experiments/p2_route_ext_v1_target_watch.py`, emitting
`writeup/data/p2_route_ext_v1_target_watch.json`. Full prose, with every query string, endpoint
URL and limitation, is in `writeup/novelty/leg_74.md`.

## The gate, answered

> **Has a certificate (computer-assisted or analytic) for arXiv:2604.01868's
> `HL_S2_nonsymmetric` profile been published, by Chen-Huang-Li or anyone else, since April
> 2026?**

**NO, as of 2026-08-06.** Six channels checked, **0** returned a candidate. The no-branch lands:
the ledger's `certified: "NO"` is **confirmed current, not stale**, and no ledger change is
needed or made.

## Why the answer is safe — the four load-bearing channels

**A. The source paper never moved.** `arXiv:2604.01868` is still at **v1**, sole submission
**2 Apr 2026**, comment `51 pages`, **no journal-ref**. That is **0 replacements in 126 days**,
and its abstract still says "a numerical investigation" with no proof claim for Scenario 2. The
likeliest route to a certificate — the same authors upgrading their own preprint — did not
happen.

**B. All three authors are silent.** De Huang, Bojin Chen and Xiangyuan Li each have
**0 submissions** after 2026-04-02; for all three, 2604.01868 is the *most recent item in the
feed*. Huang's maintained research page still lists it under "Preprints", with **0** companion
or follow-up entries.

**C. The whole "Hou-Luo" arXiv corpus since April 2026 is one paper, and it is a different
object.** `all:"Hou-Luo"`, date-descending, returns exactly **1** submission after the source:
arXiv:2605.16322 (Yaoming Shi, 5 May 2026), a Riccati-argument blow-up proof for a **closed
boundary-jet model** `(Q0)`. Its own abstract disqualifies it: *"the theorem is therefore a
blow-up result for the closed boundary-jet model, not for the unrestricted Boussinesq or Euler
systems."* It concerns no self-similar profile and does not cite 2604.01868.

**D. The CAP corpus since April 2026 has no Hou-Luo entry.** `abs:"computer-assisted" AND
abs:"self-similar"`, date-descending: **2** submissions after 1 Apr 2026, **0** on the 1D
Hou-Luo model — arXiv:2607.27072 (harmonic map heat flow) and arXiv:2607.15256 (Chen-Hou,
16 Jul 2026). The Chen-Hou one is the nearest miss and is a **methods review** of low-rank
corrections for singularly weighted 3D Euler estimates; by its own abstract it certifies **no
profile**, and mentions neither the 1D Hou-Luo model nor 2604.01868.

## The false positive, cleared

**Jiajie Chen** — co-author of the 2021 Hou-Luo CAP (arXiv:2106.05422) and the likeliest
certifier alive — has **5 submissions** after 1 Apr 2026 (one per ~25 days) and **0 of 5** target
the non-symmetric 1D profile: two are 3D Euler `C^{1,1/3-}` self-similar blowup (I/II), two are
Euler implosions/explosions, one is the methods review above. The neighbourhood is busy; it is
aimed elsewhere.

## What is weak, said out loud

The Semantic Scholar citation channel returned **zero citing works**, but a **126-day-old**
preprint sits inside S2's indexing lag and the paper-record endpoint **429'd** on retry, so the
zero is not independently corroborated. It is logged as **corroborating, not load-bearing**.
Likewise, the arXiv API searches *metadata*, not full text, so C/D would miss a certificate whose
title and abstract avoid both key strings — a hole covered from the source, author and citation
directions, which is why six channels were run rather than one.

## Consequences

- **Ledger, rank 1:** `HL_S2_nonsymmetric` `certified: "NO"` — **confirmed current 2026-08-06**.
  No edit; the file belongs to leg 63.
- **Ledger, rank 3:** `Boussinesq_S2_nonsymmetric` draws on §6.2 of the *same* paper, and the
  channels sweep the paper and the corpus rather than one profile — so it is re-dated by the same
  search, equally uncertified.
- **Route-PORT (legs 44-47) is not externally mooted.** The stall at **1.55e+08 ball radii**
  outside the truncated object, with reach worsening it at **+0.47 decades per unit ρ**, stands
  as this repository's own wall; nobody has closed the object from the other side. **126 days
  open, 0 published attempts by anyone**, from a field posting every ~25 days next door — that is
  a magnitude on how expensive the three-modulation-constant bordered shape (`c_l`, `c_ω`, `c_r`)
  is, and it is recorded as corroboration of the wall, **not** as evidence the object cannot be
  certified.
- **Re-run recipe:** execute the URLs in `ENDPOINTS`, diff against the banked counts
  **v1 / 0 / 0 / 1 / 2 / 0 / 5**. Best tripwire: a **v2 of 2604.01868**, or any new De Huang
  submission.
