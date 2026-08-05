# Leg 60 — Route-PQ novelty pass (run BEFORE construction)

**Date:** 2026-08-05. **Agent:** LEG-F. **Branch:** `leg/pq-v1`.
**Verdict: `PROCEED_AS_BOOKKEEPING`.** This leg claims **no new science**. It writes the two
missing `*_evidence.py` scripts and the two missing figures for Route-PORT v1 (leg 46) and
Route-PORT v2 (leg 47), re-deriving already-banked numbers from already-stored curated JSON.
Nothing here is offered as a finding, so there is nothing here for the literature to pre-empt.

Per `writeup/novelty/README.md`: **links, not counts.** Every query string below is verbatim
and every link returned that I judged on-topic is listed. Where a search returned nothing
on-topic I say so rather than reporting a number.

---

## Why a pass at all, when nothing new is claimed

Two standing bans cite these two legs as settled:

* *"closing the truncation gap by extending the domain"* — cites leg 47's measured trend,
  **+0.47 decades per unit `ρ`**, the wrong sign.
* the ceiling clause behind Route-PORT v1 — the certificate closes around the **truncated**
  object, the true one **1.55e+08** ball radii outside it.

A ban is only as good as the finding under it. So the pass asks the one question that could
*lift* either ban: has anyone published, since legs 46–47 ran, either (a) a certification of
the non-symmetric Hou–Luo self-similar profile, or (b) a construction in which the truncation
gap **does** close under domain extension (which would make the negative trend an artifact of
this repository's weight family rather than of the algebraic far field)?

---

## Queries, verbatim, with the links returned

### Q1
`computer-assisted proof self-similar profile Hou-Luo model non-symmetric certified interval arithmetic 2026`

- https://arxiv.org/abs/2604.01868 — Chen–Huang–Li, the source of the target profile; explicitly
  **numerical-only**, which is the premise legs 45–46 aimed at and it still holds
- https://arxiv.org/abs/2308.01528 — exact self-similar blow-up of Hou–Luo with **smooth**
  profiles, existence by an analytic fixed point, not a CAP of *this* profile
- https://arxiv.org/abs/2106.05422 — Chen–Hou–Huang, asymptotically self-similar blow-up of
  Hou–Luo, computer-assisted — the **symmetric** setting, already logged as prior art
- https://www.researchgate.net/publication/372888928 — mirror of 2308.01528

**On-topic for (a):** none. The non-symmetric profile of arXiv:2604.01868 §2.5/§4 remains
uncertified in print. Nothing lifts the Route-PORT v1 ceiling clause from outside.

### Q2
`truncation error domain truncation far-field enclosure radii polynomial does not improve with larger domain`

- returns only the near-field antenna-measurement literature (Gerchberg–Papoulis truncation-error
  reduction, e.g. https://onlinelibrary.wiley.com/doi/10.1155/2012/438727) — a different field
  and a different meaning of "truncation"

**On-topic for (b):** **none.** No result speaks to a validated-numerics truncation distance
that *grows* relative to the contraction ball as the computational domain is extended. This is
the same null the leg-47 pass recorded, and it is why the ban stands on this repository's own
measurement rather than on a citation.

---

## What this pass actually settles

Nothing lifts either ban, and nothing in print pre-empts the two negatives, so the leg proceeds
as pure bookkeeping: **re-derivation only, no new measurement, no new claim.** The only thing
that can come out of this leg that is not already banked is a **discrepancy** between the prose
and the stored data — and a discrepancy is a defect report, not a novelty claim.
