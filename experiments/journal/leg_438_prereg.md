# Leg 438 — unit `K2`, arc 7: THE LEAN GAPS — PRE-REGISTRATION, pushed BEFORE the run it governs

**Date:** 2026-09-10, 13:20Z. **The laptop Conductor's.** **FAN-OUT ×5**: four workers + a blind adversarial
verifier (slot 5). **Charter:** `STATE.md`'s arc-7 table, row `K2`, gate in final wording, reproduced here
unchanged. **Every worker is told:** *"I could not determine X, because Y" is an acceptable answer; inventing X
is not.* **Tier 2 is never a proof; nothing in this wave verifies Theorem 1.1.**

## 0. The board before this pre-registration — recorded, not repaired (`CORRECTIONS.md` §74)
Four files under `writeup/data/arc7/k2/` (`agent_1_partial.json`, `agent_2_sorry.json`, `agent_4_deepmind.json`,
`agent_5_verifier.json`; commits 5f77a7e, b397f68, 601d7da, 40cbfdb, 08:38–09:21Z) were produced by the container
Conductor's agents **before any K2 pre-registration existed, before the wave row left `planned`, and straight to
`main` rather than on their own branches** — §3g step 1 inverted, the defect arc 6's wave 1 recorded. Slot 3 never
ran; slot 5's S-d is `PENDING`; slot 2 cross-checked leg 435, not `K1`. **Treatment, fixed here:** they are
**run 1** — banked worker files, never edited, not findings (`READING_THIS_REPO.md`). **This pre-registration
governs run 2.** Run-2 workers are forbidden to open run-1 files. At integration the Conductor records, per slot,
whether run 1 and run 2 agree — an unplanned second-agent cross-check, reported as such, never as verification of
either.

## 1. The gate, verbatim from `STATE.md`
> (1) the 5 `PARTIAL` statements — what is missing, per statement; (2) the 4 `sorry` — each a challenge
> placeholder, none reachable from a main declaration, cross-checked against `K1`'s axiom output, which WINS on
> disagreement; (3) the Comparator's 4 `NOT-ESTABLISHED` checks — run them; (4) DeepMind byte-identity re-verified
> at upstream source, independently; (5) ADVERSARIAL VERIFIER, blind, a sample of 1–4. One file per agent, own
> branch, cherry-picked unedited.

## 2. The pinned inputs
The Lean tree: `openai/NavierStokesAndEuler` at `8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538`, cloned 12:53Z on the
laptop by `scripts/arc7_k1_kernel_check.sh B` and BUILT by it (support run, artefacts →
`writeup/data/arc7/k2/tree_rebuild/`). Slots 1, 2, 4 read source only. Slots 3 and 5 use the built tree after the
runner's `t_end=` line exists. `K1`'s banked axiom output: `writeup/data/arc7/k1/{phaseA,phaseB,phaseB_local}/`.
The five `PARTIAL` statements: `writeup/data/arc6/lean/agent_5_coverage.json` `map[1,3,7,28,48]` = Theorem 3.1,
Definition 3.3, Lemma 4.4, Corollary 7.3, Lemma 9.7. The four `NOT-ESTABLISHED` checks:
`writeup/data/arc6/lean/agent_4_comparator.json` `checks_performed[0,1,8,9]`. Manuscript text
`writeup/data/arc6/manuscript_pages.txt` (regenerated per `writeup/data/arc6/REGENERATE.md`); ledger
`writeup/data/arc6/ledger.json`.

## 3. Ownership — ONE file, own branch, pushed as a branch, never to `main`
| slot | gate item | artefact (`writeup/data/arc7/k2/r2/`) | branch |
|---|---|---|---|
| 1 | (1) five `PARTIAL` statements | `agent_1_partial.json` | `leg/438-k2-agent1` |
| 2 | (2) four `sorry` vs `K1` axioms | `agent_2_sorry.json` | `leg/438-k2-agent2` |
| 3 | (3) Comparator's four `NOT-ESTABLISHED` checks, RUN | `agent_3_comparator.json` (+ logs in `r2/agent_3_logs/`) | `leg/438-k2-agent3` |
| 4 | (4) DeepMind byte-identity at upstream | `agent_4_deepmind.json` (+ fetched files in `r2/agent_4_upstream/`) | `leg/438-k2-agent4` |
| 5 | (5) blind verifier: K1 from banked artefacts + the built tree; sample of 1–4 | `agent_5_verifier.json` | `leg/438-k2-agent5` |
Every artefact: `schema: arc7_k2_r2_v1`, `agent`, `leg: 438`, `run: 2`, `clone_head`, `method`, `commands`,
`gate_answer` (the gate item's own words), `could_not_determine` (what, why), `what_this_does_not_establish`,
`forbidden_paths_opened` (must be `none`). Slot 5 is told nothing about how slots 1–4 (either run) reached their
answers and does not open `writeup/data/arc7/k2/agent_*` or `r2/agent_{1..4}*`.

## 4. Pre-committed readings
- **(1)** per statement: `PRESENT` / `PRESENT-IN-DIFFERENT-FORM` / `MISSING-CLAUSE (which)` / `NOT-A-THEOREM-IN-LEAN` /
  `WEAKER (how)`, plus whether any missing clause weakens the exported statement via its import path (YES/NO).
- **(2)** each `sorry`: file:line, enclosing declaration, challenge placeholder YES/NO, in the import closure of
  `NavierStokes.ComparatorSolution` YES/NO; then `CONSISTENT` / `INCONSISTENT` with `K1`'s `axioms_verbatim`
  (`sorryAx` absent). **On disagreement the axiom output wins** and the census is reported as wrong, not the kernel.
- **(3)** each of the four checks: `PASS` / `FAIL` / `NOT-ESTABLISHED (why, measured)`. Check 0 is
  `lake exe comparator ComparatorChallenges/NavierStokes.json` (and `Euler.json`): its stdout/stderr banked verbatim;
  tooling (`landrun`, `lean4export`, `nanoda_bin`) installed user-locally if possible, each install step logged;
  a tool that cannot be installed within the session makes that check `NOT-ESTABLISHED` with the exact blocker.
  Check 9 also runs `#print axioms` on all four exported theorems (NS ×2, Euler ×2) against `permitted_axioms`.
- **(4)** `YES` / `NO` for byte-identity modulo the enumerated wrapper, at the cited pin AND at upstream `main`
  today (commit id recorded if reachable, `NOT-REACHABLE` with the HTTP status if not).
- **(5)** For `K1`: from the three banked `phaseB*.json`/logs, re-derive (a)–(c) independently (parse the logs, not
  the JSON summaries) — `REPRODUCED` / `NOT-REPRODUCED (where)`; then run `lake env lean` on the runner's
  `k1_axioms_check.lean` in the built tree and report the verbatim output. **`K1` becomes `VERIFIED` only if both
  agree with the banked result.** Otherwise `K1` stays `UNVERIFIED` and the discrepancy is an ESCALATION. For the
  sample of 1–4: re-derive at least two of items (1), (2), (4) from the gate text alone; the Conductor compares.
- **A `RED` anywhere** (`sorryAx` or a non-standard axiom reachable from an exported theorem, in any run or check)
  → STOP, ESCALATE, NO PUBLICATION, blind reproduction first (prereg 437 §2, unchanged).

## 5. Resourcing (§3d), and what this wave does not establish
One session per worker, 12 cores shared with the build, no run longer than the session. A check not reached at that
resourcing answers `NOT-ESTABLISHED` with a cost, never `FAIL`. **Nothing here establishes Theorem 1.1, that the Lean
proof follows the paper, that mathlib's cached oleans match their sources, or anything about priority.** A
`VERIFIED` `K1` means: two agents, three machines, one pinned commit, the kernel accepted two theorems that are
Fefferman (C)/(D) — strictly weaker than the paper's theorem — on the standard three axioms. **No wall moves.**

## 6. Integration (pre-committed)
Cherry-pick the five files unedited; per slot: gate answer in its own words, run-1/run-2 agreement, `K1`'s label
moved to `VERIFIED` only on §4(5)'s condition; disagreements recorded, not adjudicated; then `K3`.
