# Leg 90 — Route-EXT4 v1: has the rank-4 target object's CONJECTURE been resolved since April 2026?

**Kind.** Literature watch, claim-bearing, light.  No computation, no code, no figure, no solver
touched.  The standing ban on further gCLM measurement legs is respected trivially — nothing
here measures anything.

**Gate, verbatim.** *"Has Chen-Huang-Li's Conjecture 2.4 (stability of the HL singular steady
state) been proved or disproved, by anyone, since arXiv:2604.01868?"*

**Answer: NO.**  Ten channels, **0 of 10**, pass date **2026-08-06**, **126 days** after
`2604.01868v1` (2026-04-02).  Conjecture 2.4 is **still open**.

## What was done

1. `plan_of_record.py` run; every ban read.  The gCLM ban, the "no building without grepping
   `capabilities.py`" ban and the "no re-aiming at certified objects" ban are the ones this leg
   could plausibly have tripped.  None was tripped: nothing was built and nothing was measured.
2. `capabilities.py` grepped first.  `solver/hl_rescaled.py` is registered at line 45 and its
   `validated` field already carries this leg's object — *"the exact Thm-2.3 singular anchor is
   a steady state on its support"*.  `solver/target_selection.py` is at line 387.  The anchor
   exists; nothing needed building.
3. Novelty pass run and **committed before the writeup** (`writeup/novelty/leg_90.md` §0–§1,
   commit `08c5ef4`), logging **links, not counts**, per `writeup/novelty/README.md`.
4. Ten channels issued: arXiv version history of the source paper; arXiv author enumeration for
   all three authors separately; two "Hou-Luo" corpus enumerations (`all:` and `ti:`); the
   `"singular steady state" AND "stability"` corpus; the `"self-similar" AND "singular profile"`
   corpus; the `"Constantin-Lax-Majda"` corpus; two blowup-stability corpora; Semantic Scholar
   citations; **OpenAlex cited-by** (a second, independently built citation index — the channel
   legs 74/77/82 did not run); the corresponding author's homepage plus two open-web passes.
5. `Papers/2604.01868.pdf` re-pulled (28 MB, gitignored) and Conjecture 2.4 / Theorem 2.3 read
   verbatim, rather than trusting the ledger's paraphrase.
6. `Papers/2603.25104.pdf` and `Papers/2607.19762.pdf` pulled and full-text-grepped to settle
   the two hardest false friends on quoted evidence rather than abstracts.

## Magnitudes

| quantity | value |
|---|---|
| channels run / returning a candidate | 10 / **0** |
| channels sufficient alone | 6 |
| source versions in existence / revisions since v1 | 1 / **0**, at 126 days |
| author entries enumerated / filed after source | 30 / **0** |
| author *revisions* after source | **1** (`2603.25104` v1→v2, 2026-06-16 — and it is FF3) |
| indexed citations: Semantic Scholar / OpenAlex | **0** / **0** (2 independent indexes) |
| false friends opened and excluded | **4** |
| out-of-scope items recorded | 2 |

## The four false friends, one line each

* **FF1 Xu `2607.19762v1` (2026-07-22)** — proves a spectral gap 1/2 and decay `e^{-τ/2}`, but
  for the **smooth** a=0 CLM profile Ω(y) = −y/(y²+1/4) on origin-H²; "Hou-Luo" returns **0**
  full-text hits and `2604.01868` is not cited.  Already in `Papers/fetch.sh` TIER1.
* **FF2 Bradshaw-Palmer `2606.22291v1` (2026-06-21)** — announces "establish asymptotic
  stability" for **singular steady states**, but of 3D *stationary* Navier-Stokes (Landau /
  Squire / Serrin), an isolated point singularity, no contact with the HL model.
* **FF3 Huang-Tong-Wang `2603.25104` v2 (2026-06-16)** — **the sharpest**: same lead author,
  revised 75 days after the conjecture, abstract says "we rigorously prove the convergence of
  the outer profile to an explicit singular function".  Wrong model (gCLM), wrong statement
  (convergence of the constructed solution's outer profile, not stability under perturbation),
  its own stability language is numerical (*"hence **suggesting** stability"*), and the v2
  revision did not add a citation to `2604.01868`.
* **FF4 Shi `2605.16322v1` (2026-05-05)** — the only post-source entry in the whole "Hou-Luo"
  corpus, but a Riccati blow-up theorem for a closed (1+1)D boundary-jet truncation, with an
  abstract that disclaims its own scope.

## Why this is not leg 74 / 77 / 82 again

Those three asked whether a **certificate** had appeared for an uncertified profile — one-sided
existence questions.  This asks whether a **named conjecture** has been **resolved**, which a
*disproof* answers as loudly as a proof, and the channels were chosen to be direction-symmetric
(channel 4's own corpus contains *"Stability vs. instability of singular steady states…"*).
Different object, different question, independent answer.

## Consequence, reported and not applied

`solver/target_selection.py` was **read and never written** — it is parked pending the user's
ruling on leg 63's escalation.  Its rank-4 `HL_singular_steady_stability` entry
(`"certified": "NO"`, q1 *"an explicitly stated conjecture with numerical support only"*) is
**CURRENT as of 2026-08-06, not stale**.  Two bookkeeping precision suggestions are recorded in
`writeup/novelty/leg_90.md` §6 for leg 63's successor: pin the `"source"` field to `v1`, and mark
the `p < 2` note as *derived* rather than *quoted*.

## One flag for the orchestrator, orthogonal to this gate

FF1 (`2607.19762`) gives a realization-dependent spectral picture of the **a = 0 CLM
linearization L_0** — the same operator the **NG** stage's no-go is stated about, with the
explicit caveat that *"a spectral gap does not by itself give a decay rate in the X norm"*.
Reported, not acted on; NG is not this leg's territory.  Recorded so a future NG leg does not
rediscover the overlap.

## Known weakness

Every channel is an **absence** argument.  Two things strengthen it over leg 82's rank-3 watch:
a **second independently built** citation index at zero, and one genuine **positive act** (FF3's
v2 revision, which declined to announce anything).  What is still missing is any statement *by
the authors* that the conjecture remains open.  Re-ask interval: **shorter** than the rank-3
watch's, with a sharp cheap trigger — any nonzero `cited_by_count` in either index.

## Artifacts

* `experiments/p2_route_ext4_v1_target_watch4.py` — the executable search log; re-emits the JSON.
* `writeup/data/p2_route_ext4_v1_target_watch4.json` — the curated record.
* `writeup/novelty/leg_90.md` — novelty pass (§0–§1, committed first) and findings at full depth.
* No figure: pure literature watch.
