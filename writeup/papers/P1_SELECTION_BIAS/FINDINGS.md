# `P1_SELECTION_BIAS` — FINDINGS ABOUT THE RECORD (leg 411, unit `PB1`, wave 8)

This is `PB1`'s **SECOND output**. The first is the gate answer in `NOVELTY.md`. Everything
here surfaced *while searching* and is about **our own record**, not about the literature.
Per the brief it is **NEVER SMOOTHED OVER IN PROSE**: it is written down at full strength,
routed, and left for the Conductor. **NOTHING BELOW HAS BEEN APPLIED BY THIS UNIT.**
`writeup/CORRECTIONS.md` was not edited; `WALLS.md`, `STATE.md`, `plan_of_record.py` and
`writeup/waves/WAVE8_PLAN.md` were not touched.

**PATH NOTE, DISCLOSED RATHER THAN RESOLVED.** The brief names `writeup/papers/FINDINGS.md`.
`writeup/papers/README.md` mandates a **per-paper** `FINDINGS.md`. The two instructions
conflict. This unit followed the README (per-paper layout) because a top-level
`writeup/papers/FINDINGS.md` does not exist and creating a new top-level file that the
layout does not describe is the more expensive mistake to undo. **Flagged, not decided.**

---

## F1 — `experiments/journal/leg_387.md` DOES NOT EXIST

The brief instructed this unit to read `experiments/journal/leg_387.md` as "the exact failure
you must not repeat". **There is no such file.** Leg 387's only primary record is
`experiments/JOURNAL.md` line 5305. Everything else about leg 387 in this repo is SECOND
HAND: `ORCHESTRATION.md` §3k line 576, and `experiments/journal/leg_392.md` §0.2 / §3.

Consequence: **the failure that this leg's entire instrument discipline is built to avoid is
itself recorded only at SECOND HAND depth** (§3k vocabulary). The discipline is good
regardless of provenance and was adopted whole. But the record should say so.

**Routing: `CORRECTIONS.md` — a journal file referenced by a live brief is missing.**

## F2 — THE TWO SURVIVING ACCOUNTS OF LEG 387 CONTRADICT EACH OTHER, AND LEG 411 IS A THIRD DATA POINT AGAINST THE DIAGNOSIS

This is the sharpest finding in the leg and it should not be softened.

**Account A — `experiments/JOURNAL.md` line 5305 (the chronological primary record):**

> The **arXiv half is discharged** [...] both returned **HTTP 200 with
> `opensearch:totalResults = 0`, CONTROLLED-ZERO**, control-validated in the same run
> (positive control `all:"Navier-Stokes"` → 10,756 hits; nonsense control → a genuine zero).

**Account B — `ORCHESTRATION.md` §3k line 576, and `experiments/journal/leg_392.md` line 190:**

> leg 387 reported zeros for a served-namespace mismatch and cost a leg

> Leg 387's harness listed `1.0` and therefore **refused every response while reporting a
> zero.**

**These cannot both be true.** Account A says the arXiv channel is DISCHARGED on validated
controlled zeros. Account B says those same zeros were fabricated by a parser bug.

**Leg 411's own measurement bears on it.** This unit ran the *same positive control query*,
`all:"Navier-Stokes"`, on 2026-08-19 and MEASURED **10,780**. Leg 387 recorded **10,756** for
that query. A parser that "refused every response" could not have produced 10,756, and 10,756
is exactly what you would expect the true total to have been shortly before 10,780. **The
numeric evidence favours Account A's control having genuinely fired**, which makes Account B's
diagnosis at least imprecise and possibly wrong about *which* queries failed.

The programme is currently in the position where **the entry a reader reaches first (the
chronological journal) still asserts a discharged CONTROLLED-ZERO that the programme's own
governing document calls a fabrication** — and the arithmetic mildly supports the journal.
Leg 382's obligation was left OPEN and re-queued on Account A's reading, so downstream work
may be keyed to it.

**This unit does not adjudicate it and must not.** ESCALATION, not a correction I may apply.

**Routing: ESCALATION to the Conductor. A ruling is needed on which account stands, because
one of them is load-bearing for `ORCHESTRATION.md` §3k and the other for leg 382's queue.**

## F3 — `writeup/SOURCES.md` ROW 25 UNDERSTATES THE DEPTH OF CHANDLER & KERSWELL 2013, AND LIVE NUMBERS DEPEND ON IT

`writeup/SOURCES.md` row 25 records Chandler & Kerswell, *JFM* **722**:554–595 (2013) /
arXiv:1207.4682 as **"CITATION, UNREAD HERE"**, with the rider that nothing may rest on it.

`experiments/journal/leg_358.md` §1–2 records **fetching and reading that paper at full text**
and quoting Table 1, the solver caps, the `T = 1e5` run lengths, and the `7/163 = 4.3%`
conversion split. Those numbers are **live across `PROG-R4`** (the pre-registration, the
attempt harness, the `WALLS_HISTORY` option-B costing, and the mining-band write-up).

So either the depth register is wrong, or a family of numbers in current use is unsourced.

**Leg 411 settles which, from primary.** The paper was re-fetched
(`Papers/1207.4682.pdf`, sha256 in `Papers/MANIFEST.md`), extracted, and Table 1 re-read:
Series A at `Re = 60`, runs `e`/`f`/`g` — **102 / 104 / 78** guesses to **64 / 67 / 58**
convergences; Series B run `p` at `Re = 60` — **163** guesses, **7** convergences. Leg 358's
`7/163` is **CONFIRMED at FULL TEXT depth**. The register is what is wrong.

The error is in the safe direction — the record claimed *less* depth than it had — but a
depth register that is wrong in the safe direction is still wrong, and §3k makes DEPTH the
column that matters. Row 29 (`R-prof`) carries the same "CITATION ONLY, UNREAD" pattern and
should be checked by whoever fixes row 25; this unit did not check it.

**Routing: `CORRECTIONS.md` + a `SOURCES.md` depth amendment. Leg 411 has added its own rows
in the same commit as its reads (§3k rule 1) and has left row 25 for the Conductor rather
than editing a banked row.**

## F4 — THE SEMANTIC SCHOLAR ARM HAS NO VALIDATED CONTROLS, AND THIS IS NOW A REPEAT

All three Semantic Scholar controls returned `HTTP 429` (`THROTTLED`, `total = None` by
construction). Two substantive S2 queries happened to get through (`97`, `68`) and are
therefore **UNINTERPRETABLE** and used for nothing.

Leg 392 recorded the same refusal. Leg 387 recorded the same refusal. **Three legs, same
hole.** The programme keeps paying for an S2 arm that has never once been control-validated.
It should either be given a rate-limited retry policy that can actually validate a control,
or be struck from the standard instrument and stop appearing in ledgers as if it were a
channel. Continuing to run it un-validated is the option that manufactures the appearance of
coverage without the substance.

**Routing: `CORRECTIONS.md` (standing instrument debt).**

## F5 — A CONTROL OF MY OWN DID NOT FIRE AS PLANTED

Instrument 1's `pos_topical` control (`all:"exact coherent structures"`, planted `>= 50`)
MEASURED **33**. It **DID NOT FIRE**. It has **NOT** been re-planted at a threshold it would
pass, and `pos_topical_2` — which did fire — is **NOT** used to rescue it. Per the leg's own
§0.2 rule 5, the verdicts that control governs are **VOID**; nothing in the gate answer rests
on instrument 1, which is candidate enumeration only. Disclosed in `NOVELTY.md` §4.2 and here.

The substantive lesson is about the plant, not the endpoint: **`50` was a guess dressed as a
threshold.** A positive control whose planted value is not itself derived from something is a
coin-flip that looks like a measurement. Future plants should be derived from a prior
observed count or stated as an order-of-magnitude band.

**Routing: `CORRECTIONS.md` (instrument-design lesson).**

## F6 — AN ADVANCE `UNREACHABLE` DECLARATION OF MINE WAS WRONG

§0.1 declared Kawahara, Uhlmann & van Veen, *Annu. Rev. Fluid Mech.* **44**:203–225 (2012)
UNREACHABLE in advance, on the reasoning that Annual Reviews is a journal-only venue. **It is
on arXiv as `1108.0975`, carries its `journal_ref`, and was fetched and read at full text.**

Wrong in the safe direction (the ceiling was too pessimistic, so nothing was over-claimed),
recorded rather than quietly corrected, and already noted in `Papers/MANIFEST.md`. The lesson
generalises: **an UNREACHABLE declared from venue reputation is a guess. Declare it from a
served query result or declare it as a guess.**

**Routing: `CORRECTIONS.md` (ceiling-writing lesson).**

## F7 — arXiv:1406.1820**v2** HAS A DOUBLED TEXT LAYER AND IS NOT SAFELY QUOTABLE

The v2 PDF of Lucas & Kerswell (2015) carries a doubled text layer: `pdftotext` output
interleaves two copies of the page under plain, `-layout` and column-cropped extraction, and
the prose on the pages that matter is unreadable. **v1 extracts cleanly and is what leg 411
quotes.** The single most load-bearing sentence was re-checked against the v2 extraction and
is present in both, so the finding is an artefact of the version, not of the claim.
Pagination differs between versions; leg 411 cites **v1 pages** and says so everywhere.

Any future unit reading this paper must use v1. Recorded in `Papers/MANIFEST.md`.

**Routing: `Papers/MANIFEST.md` (done) + `CORRECTIONS.md` as an extraction hazard.**

## F8 — OUTPUT-CHANNEL COMPRESSION SILENTLY DROPS WORDS FROM LONG COMMAND OUTPUTS: A VERBATIM-QUOTATION FABRICATION HAZARD

**This is the finding with the widest blast radius and it is not about this leg's subject at
all.**

While extracting quotes, sentences returned by `grep`/`pdftotext` appeared to be missing
function words ("of", "the", "to"). The natural diagnosis is a defective PDF text layer. **It
was not the PDF.** Re-running a *narrower* `grep -o` over the same file returned the sentence
intact. The words were being dropped **in the tool-output channel**, which compresses long
outputs — above roughly 150 characters — by discarding words.

The consequence for this programme is severe and general: **any unit that copies a "verbatim"
quotation out of a long command output can transcribe a sentence that the source does not
contain, with no error, no warning, and no way for a reader of the artefact to detect it.**
That is fabrication produced by the instrument rather than by the author, and it is exactly
the class of failure §45 says our evidence scripts cannot catch — the artefact and its checker
would share the corrupted string.

Leg 411's mitigation, which is what makes its quotes trustworthy: **every quotation in
`NOVELTY.md` was written into the file by a script reading the JSON directly, never
retyped from a displayed output**, and the JSON quotes were written by `pdftotext` extraction
in the same process that located them. No quote in the verdict passed through the display
channel at all.

**Recommendation: make this a standing rule.** Quotations are extracted to a file by a script
and injected into artefacts by a script. A quote that a unit read on screen and retyped is
`SECOND HAND` at best and should be labelled so.

**AND IT BIT THIS VERY LEG, IN THE ONE PLACE THAT WAS DONE BY HAND.** The sha256 rows in
`Papers/MANIFEST.md` were transcribed from displayed output rather than injected by script.
One of them — `1611.04829.pdf` — was banked as `…3cfbbda198` when the true tail is
`…c3fbbda198`: **two characters transposed.** It was caught by this leg's own
`manifest_hashes` check, class `recompute-from-primary`, which re-hashes the bytes. **A
`re-read-own-artefact` check could not have caught it at any strength.** That is `CORRECTIONS.md`
§45 demonstrated live, on this leg, at a cost of nothing because the check existed. The wrong
value is written out in `Papers/MANIFEST.md` rather than erased. Every quotation in
`NOVELTY.md` was script-injected and all 29 re-verify against the PDF page claimed; the one
artefact element typed by hand is the one that was wrong.

**Routing: `CORRECTIONS.md`, as a standing instrument rule, and it should reach
`ORCHESTRATION.md` §3k if the Conductor agrees.**

## F9 — `P1`'s OWN FRAMING WORD IS CONTRADICTED BY ITS OWN INTENDED SOURCES

`P1`'s effect (b) is framed as re-mining **silently** re-finding. The primary sources report
the duplication **openly**, **quantify it in a published table**, and **budget around it as a
documented methodological decision**. See `NOVELTY.md` §3.4.

This is recorded as a finding about the record and not only as a literature result, because
it means a `P1` draft would have carried a novelty claim that its own bibliography refutes on
the page. The novelty check was owed since wave 1. **The cost of the delay was the risk of
drafting that claim, and that risk has now been retired rather than realised.**

**Routing: `P1_SELECTION_BIAS/STATUS.md` (blocker 1) + `CORRECTIONS.md`.**

---

## WHAT THIS UNIT DID NOT DO

* Did not edit `writeup/CORRECTIONS.md`, `WALLS.md`, `STATE.md`, `DIRECTION.md`,
  `plan_of_record.py`, or `writeup/waves/WAVE8_PLAN.md`.
* Did not read `DIRECTION.md`. Not at any point, by any means.
* Did not edit any banked artefact, including `SOURCES.md` row 25 — the wrong row it found.
* Did not make or attempt **EXTERNAL CONTACT OF ANY KIND**. Reading published material is
  authorised; contacting an author, group, maintainer or list is not, and remains held.
* Did not push. Did not use `checkout`, `stash`, `reset`, `rebase`, `git add -A`, `git add .`
  or `git commit -a`. All commits are explicit-path.
* Did not draft `P1`, did not draft `P3`, did not cite a draft, did not soften a caveat, and
  did not describe the kill as progress. **A kill is a kill; the brief pre-committed that it
  is a good one.**
