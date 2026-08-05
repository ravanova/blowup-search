# Leg 65 — VER-H: post-landing review of the Route-L1G literature verdict

**Branch** `verify/65-l1g-review`. **Reviewing, not repairing.** Leg 65 landed on `main`
(`de533d9`, `cda8edc`, `09728ec`). Full findings, quote by quote, in
`writeup/novelty/leg_65_verify.md`.

**Verdict: THE FINDING STANDS.** Gate answer `NO` — neither the weighted-`ℓ¹` no-go (C1) nor the
discrete-ball trap (C2) is published in the two remaining Tier-2 papers or anything they cite
forward — confirmed on all four key claims. No rework leg warranted.

## How independent this pass was

I did not reuse leg 65's extracted texts. Re-fetched all four PDFs from arXiv myself
(`Papers/fetch.sh`, egress HTTP 200, 4/0), re-extracted with `pdftotext -layout`, recomputed
every count and re-read every quoted passage from my own copies, and re-queried the
forward-citation sweep live against the Semantic Scholar API.

## What I independently confirmed

| leg 65 claim | my check | verdict |
|---|---|---|
| 2312.01702: 0 "weight", 0 "computer-assist", 0 "duality" | recounted on own extraction | **exact** |
| term counts, all four papers (14/108/1 weight; 0/0/12/0 c-a; 0 duality) | recounted | **exact**, and JSON char counts reproduce byte-identically |
| 2005.14027 is weighted `ℓ²` (Hilbert `h^m`) and proves the bilinear term **bounded** | read (37)–(38), Thm 12 proof, Lemma 16 | **confirmed verbatim** — "Operator B is a bounded bilinear operator in hm"; structurally opposite to a no-go, as claimed |
| 1908.09385 eq (2.12), space `L²(ϕ) ∩ H⁴(ψ)`, `ϕ = ψ/x⁴` | read (2.12) and all 14 "weight" occurrences | **confirmed exactly**; every usage is a working device, **no statement anywhere about admissible weight classes** |
| 2607.15256 §1.2 (1.17)–(1.18) is same genre, weighted `L²`, damping-vs-finite-energy, resolved by a choice | read the passage, abstract, §1.4 | **confirmed on all four sub-claims** — its own conclusion is a prescription ("one needs to take a very singular weight … with large `α`"), never an impossibility |
| 39 forward citations swept (8 + 31), 1 on-topic | re-queried live | **8 and 31 exactly**; 2607.15256 genuinely cites 1908.09385 |

**The triage was checked, not just the count.** I pulled titles for the nine citing papers leg 65
did not name plus the un-IDed remainder: all are journal-version duplicates or blowup-corpus
analysis papers (Landau, compressible Euler, β-CCF, electron MHD, Ginzburg–Landau), one is an ML
paper on symbolic PDE search. None is in weighted-`ℓ¹` or discrete-duality territory. **No
candidate was missed.**

## Precision nits — prose only, none changes the gate

1. `writeup/novelty/leg_65.md`: "its only uses of 'rigorous' are disclaimers" overstates. 2 of 3
   are; the third credits a **cited** work with rigour. Substance untouched.
2. `experiments/journal/leg_65.md`: calls the 2607.15256 tension "weighted `L²`/`L^∞`". The
   (1.17)–(1.18) tension is **purely weighted `L²`**; `L^∞`/`C^{1/2}` is the route Chen–Hou adopt
   *because of* it. The novelty log states this correctly; only the journal is loose.
3. The "**`DIRECTION.md` has no leg-65 entry**" flag in both ledger files is **stale and now
   false** — the entry is at `DIRECTION.md` line 390, added 95 seconds before leg 65's first
   commit, so the leg branched just ahead of the DM refresh and the flag was honest when written.
   **No divergence resulted:** the gate leg 65 executed is word-for-word identical to
   `DIRECTION.md`'s, as is the territory list.

## Additive observation (not a gap)

1908.09385 already contains the germ of 2607.15256's obstruction, unrecorded by leg 65:
*"`E(0) < +∞` implies `ωx(0,0) = 0` due to the singular weight `ϕ`"* — finite energy forcing a
vanishing order, the same mechanism Chen–Hou make their whole subject seven years later. A
consequence, not an obstruction, so the gate is unmoved; but a write-up tracing the cousin's
lineage should cite Chen 2019 alongside Chen–Hou §1.2.

## Quartet check (DOCS)

**Complete on disk.** `experiments/p2_route_l1g_v1_lit.py` (456 lines, runs clean) →
`writeup/data/p2_route_l1g_v1_lit.json` (346 lines, **regenerates byte-identical**, `git status`
clean after re-run) + `writeup/novelty/leg_65.md` (334) + `experiments/journal/leg_65.md` (93).
No figure, correctly — pure literature leg, per the established convention.

`writeup/novelty/leg_65.md` is **links, not counts**: all six query records carry verbatim query
strings and the URLs returned, and empty queries say so in words rather than reporting a bare
number. The runner also **recomputes** its term counts from `Papers/` when the gitignored PDFs
are present, falling back to recorded values under an honest provenance label — it does not
hardcode them.

## Ledger discipline

Wrote only `experiments/journal/leg_65_verify.md` and `writeup/novelty/leg_65_verify.md`. Did not
touch `experiments/JOURNAL.md`, `LITERATURE_CHECK.md`, `plan_of_record.py`,
`CONTINUATION_PROMPT.md`, `PHASE2_P2_NOTES.md`, `DIRECTION.md`, `solver/holder_norms.py`, or any
of leg 65's own files. Did not merge.
