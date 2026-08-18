# PAPERS — drafts aimed at refereed venues, and the rules that keep them honest

**Adopted 2026-08-19 by user ruling: a temporary pivot to draft three papers.** Not a change of
goal. `CLAY_ROADMAP.md` §7.6's posture, the lane rankings and every live gate stand; this is
additional work, and current legs are **not** interrupted for it.

## Why this is worth doing even if nothing is ever submitted

**A draft aimed at a referee is an audit instrument, and it is a kind this repository does not
have.** Every existing check asks *"is this number right?"*. A draft asks a different question:
*"can this claim be stated, in full, to someone who does not already believe it?"* — and that
question catches a defect class the others cannot. Leg 348's undischarged ceiling would not have
survived one honest paragraph of related work. The `C1` exemplar would not have survived a
sentence naming what had actually been demonstrated.

**So the expected output of this folder is TWO things, and the second is not the paper.** Where a
draft cannot state something cleanly, **that is a finding about the record, and it is raised as a
`CORRECTIONS.md` entry or an escalation — never smoothed over in prose.** A paper that reads well
because its awkward parts were written around has done active harm.

## THE BINDING RULE: A PAPER IS A VIEW OF THE RECORD, NEVER A SOURCE

The same rule `ROUTE_MAP.md` carries, and here it matters more because prose is persuasive:

- **Every number in a draft cites the banked JSON field it came from.** Not the journal, not a
  previous draft, not memory. If a number cannot be traced to a field, it does not go in.
- **A draft may not state a claim at a confidence the record does not hold.** `UNVERIFIED` stays
  `UNVERIFIED` in the draft. `UNDER-RESOURCED` is not written as a null result. A control that did
  not fire as planted is disclosed in the paper, not only in the journal.
- **No unit may cite a draft.** Drafts are downstream of everything and load-bearing for nothing.
- **§3k binds every draft**: a load-bearing citation may not rest on an abstract, and the related
  work section is exactly where that debt becomes visible. Update `SOURCES.md` as you read.

## The three drafts, and why these three

| dir | claim | why it was chosen | the thing that could kill it |
|---|---|---|---|
| `P1_SELECTION_BIAS/` | A scalar recurrence score used as an admission filter biases the recovered orbit set along any coordinate it is monotone in — measured twice, on period and on shift — and re-mining a fixed trajectory silently re-finds. | Closest to submittable. Measurement, controls, artefacts, and a caveat on a mature field. | **The owed novelty check has never been run.** It may be known folklore, unstated in print. |
| `P2_ALPHA_PIN_PINCER/` | For a backward `λ`-DSS blow-up profile of 3D NS the far-field decay is pinned to exactly `α = 1`; after localisation the surviving obstruction is the modulation commutator `∝ ṁ`; it vanishes only at `α > 1` or `ṁ = 0`, and two published theorems forbid one each. | The most interesting result the programme holds. | **Both jaws are journal-only and have never been read at primary.** A referee reads the sources. |
| `P4_METHODOLOGY/` | How to run a computational-mathematics programme with LLM agents so that it catches its own errors: pre-committed gates, planted controls that must fire both ways, `UNDER-RESOURCED` as distinct from `NO`, verifiers that may not have planned what they check. | The material is abundant and the evidence is a record of self-caught errors, not assertions. | Nothing measured. It needs framing, and an honest account of what the discipline *failed* to catch. |

**`P3` (the audit of `arXiv:2509.25116`) is deliberately absent.** Its correct first route is to the
authors, and outreach is under a standing user hold. It also has an unverified Class A. Recorded so
its absence reads as a decision rather than an oversight.

## Per-paper layout

    P<n>_<NAME>/
      STATUS.md    the claim, what is banked for it, what blocks it, what it owes. Kept current.
      DRAFT.md     the draft itself. Every number carries its JSON field.
      FINDINGS.md  what drafting revealed about the record — the second output, and the one that
                   matters even if the paper never ships.

**`STATUS.md` is written before `DRAFT.md`.** A draft started before its blockers are enumerated
is a draft that will route around them.
