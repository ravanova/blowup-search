# Tech-debt review — seed backlog for the maintenance sweep

**Date:** 2026-08-05. **Produced by:** three parallel audit agents (docs, structure/process,
code) at tree `94562c4` (post-cycle-1: legs 54–57 landed, `NG` proposed `NEXT`).
**Consumed by:** the maintenance sweep (`ORCHESTRATION.md` §11) and the DM.

**Scheduling law (user directive, 2026-08-05, verbatim):** *"Like, 10 Opus agents to do 10
legs, but I'm happy with some Sonnet agents being spawned to handle tech debt etc where
useful, maybe up to 5 at a time as required"* and *"the tech debt search could be kicked off
by the orchestrator periodically."* So: leg slots stay research; the sweep runs on Sonnet
support agents, ≤5 live at once, dispatched periodically by the orchestrator.

**How to read the table:** `M` = mechanical (sweep agents may work it directly, §5
territories apply). `CB` = claim-bearing (touches numeric claims, gate wording, banked
prose, or the merge criterion) — **the sweep never works these**; they go to the DM as
queue candidates and get a leg + verifier. Sizes are S/M/L.

> **Status note:** the code-audit lane (dead code, duplication, full 52-test sweep,
> capabilities spot-check) had not reported when this file was committed. Its findings are
> appended as §D when available; treat §D's absence as "not yet audited", not "clean".

---

## A. Wrong-state records that actively mislead the next agent (do these first)

| # | Item | Evidence | Size | Kind |
|---|---|---|---|---|
| A1 | `reports/ORCH_STATE.md` asserts `writeup/novelty/leg_55_verify.md` was "committed directly to `main` via `bda30a2`" — **neither the file nor the commit exists anywhere** (`git log --all` empty, `git rev-parse` unknown). A verify artifact the handoff claims is safe may be lost. Its "Live branches" table lists 8 branches; the remote has 2. | `reports/ORCH_STATE.md:60,85`; `git branch -r` | S | **CB** — needs a git-forensics check and an honest correction, not a doc edit |
| A2 | `CONTINUATION_PROMPT.md` framing banner still says **four legs** ("binds all four legs", "FOUR LEGS RUN AT ONCE NOW") vs the ten-leg contract. This file is handed to leg agents to act on without questions. DIRECTIVE 1's body is correct; only the framing is stale. | `CONTINUATION_PROMPT.md:6,8,19-21` vs `ORCHESTRATION.md:1,73` | S | M (integration-owned file — orchestrator applies it) |
| A3 | **fig48 is claimed by two legs** (`fig48_route_tc_v1_assemble.png` vs `fig48_weight_repairs_v1.png`; both cited as "fig48" in banked prose, 5+ files). Also fig53–54 are an unallocated hole below DIRECTION's pre-allocated fig55–60. Requires a numbering ruling (renumber the *newer* artifact; leave old citations intact), then a uniqueness check. | both PNGs in `writeup/figures/`; `TECHNICAL_P2_ROUTETC_V1.md:4`, `TECHNICAL_P2_WEIGHT_REPAIRS_V1.md:7`, `PHASE2_P2_NOTES.md:3513`, `experiments/JOURNAL.md:10`, `DIRECTION.md:109` | S | **CB** (figure ids are citation keys in banked prose) |
| A4 | `scripts/merge_gate.sh` blind spots: (i) solver→test mapping misses 6 modules whose tests exist under other names (`solver/gclm.py` → `test_solver_clm.py`, `boussinesq.py`, `spectral_utils.py`, `hilbert_holder.py`, `hilbert_pointwise.py`) and 2 with no test (`ga_search.py`, `finite_support.py`); (ii) a diff confined to `experiments/` or `writeup/*.py` runs **no tests**; (iii) BLOG→TECHNICAL is checked but not the reverse (a TECHNICAL-only landing passes; PORT-v2 proves the case exists). Fix = explicit mapping table + reverse check + legacy allowlist. | `scripts/merge_gate.sh:40-58`; import counts per code audit | S | **CB** (it is the merge criterion; orchestrator-owned) |
| A5 | `reports/STATUS.md` + `reports/REPORT_2026-08-05.md` carry a "tomorrow's roster" and live-state from the **closed six-agent run**; the roster was replaced by the 32-slot model. Two files both claim to be the open-escalation list. Mark superseded / fold into ORCH_STATE. | `reports/REPORT_2026-08-05.md:3,96-107`; `reports/STATUS.md` | S | M |

## B. Stale indexes and doc drift (bread-and-butter sweep work)

| # | Item | Evidence | Size | Kind |
|---|---|---|---|---|
| B1 | `writeup/INDEX.md` — the self-declared quartet map — has **zero entries for legs 53–57** (TC, MM, NB, TN, XS) or Weight-Repairs; still says "TC … in progress on `leg/tc-v1`"; cites the quartet contract as "ORCHESTRATION.md §4" (it is §6). | `writeup/INDEX.md:87,95-96` vs `writeup/4_p2_lottery/` contents | M | M (links/labels only, per its own header rule) |
| B2 | `writeup/README.md` — four sections frozen between fig41 and entry #47: numbered index (skips #45, missing 12 routes), tree diagram ("figs 12–35", actual 12–52), figures table (11 committed PNGs undocumented), evidence map (13 JSONs unlisted), rebuild block, "8 suites green" (52 exist). | `writeup/README.md:29,36-38,446,504-620,648` | L | **CB** (every index entry is numeric prose — needs a leg, or DOCS with verifier review) |
| B3 | Root `README.md` stage table one cycle behind (`TC` marked next; plan says `[x] TC`, `==> NG`; `MM`/`NG` absent) and "52 legs" (now 57), "50 test files" (52). No drift detector covers it. | `README.md:12,97,115-125,160` vs `plan_of_record.py` output | S | **CB** (leg counts and stage state are claims) |
| B4 | `PROJECT.md` §"Approach (planned, not yet built)" still says the solver and GA "are future milestones — not yet built", contradicted 50 lines later in the same file. README sends first-time readers here. | `PROJECT.md:30,41-44` vs `:94-133` | S | M if marked historical; CB if rewritten |
| B5 | `CLAY_ROADMAP.md` §7.4 says "Four stages" and lists 4; the plan has 10. §4's "START HERE" sequencing has no in-place superseded banner. The drift test only asserts the string "ADOPTED" — advertised coverage is stronger than real coverage. | `CLAY_ROADMAP.md:148-163,281-306`; `test_plan_of_record.py:104-112` | M | **CB** (stage entries carry gate wording) |
| B6 | `Papers/MANIFEST.md` is 9 legs stale and omits the three papers currently holding up live bans (Cadiot 2505.03091, BDL 1503.06315, CHL 2604.01868). Two divergent fetch scripts (`Papers/fetch.sh`: 14 ids; `scripts/fetch_papers.sh`: 4, incl. probable transposition `2305.05660` vs manifest's `2305.05895`); default fetch misses the two papers `solver/viscous_novelty.py` depends on. | `Papers/MANIFEST.md:10`; both fetch scripts | S | M (fetch entries), claim-adjacent for the "what it gates" column |
| B7 | Pointer-convention loose ends: `writeup/novelty/README.md` + `experiments/journal/README.md` still say "four legs"; verify artifacts (`leg_54_verify*.md`) sit in `novelty/` off-spec with no pointer in `LITERATURE_CHECK.md` and no declared home (plausibly why leg-55's went missing, A1); `writeup/VERIFY_LEG52_HEADLINE.md` (38 KB, "URGENT for `leg/tc-v1`" — a dead branch) sits at `writeup/` root outside every arc, indexed nowhere. | `writeup/novelty/README.md:1,5,9-12`; `experiments/journal/README.md:3-5`; `writeup/VERIFY_LEG52_HEADLINE.md:9` | S | M (relocate/retitle; content is a correction record — do not edit it) |
| B8 | ~20 relative-path references in arc 1–3 prose broken by the arc-folder move (`../X.md` should be `../../X.md`), plus dead targets `reports/EXPERIMENT_SHARDING.md` (referenced twice, never written) and the A1 file. Markdown links proper are clean — this is backticked-path prose. | e.g. `writeup/1_gclm_1d/TECHNICAL_WRITEUP.md:81+`, `writeup/2_phase1_2d/BLOG_PHASE1_GATE4.md:6,193-199`, `ORCHESTRATION.md:375` | M | M (many sites, each trivial) |

## C. Contract/structure gaps (need a ruling, then are cheap)

| # | Item | Evidence | Size | Kind |
|---|---|---|---|---|
| C1 | **Evidence-script location has forked.** Contract §6 says `*_evidence.py` lives in the `writeup/` subdir; legs 54–57 put theirs in `experiments/` and DIRECTION's queued territories (legs 58, 60) do too; `build_figures.py` carries escape-path apologies. Also `experiments/leg<N>_*.py` naming (§5b) is followed by **zero** files. Ratify one convention and amend the contract — either way is one small docs change; leaving it forks every future leg. | `ORCHESTRATION.md` §5b/§6; `writeup/build_figures.py:299-308`; `DIRECTION.md` territories | S | M (contract edit — orchestrator-owned; DM should ratify) |
| C2 | `writeup/build_figures.py` rebuilds 12 of 53 figures (figs 1–7 + five registered P2 scripts); ~40 standalone evidence scripts are never called, so no single command reproduces the figure set and REPRO's mandate is mostly vacuous. Fix is append-only registration; real cost is discovering which scripts still run. | `writeup/build_figures.py:299-308`; 53 PNGs in `writeup/figures/` | M | M |
| C3 | **Ownership map covers ~60% of the tree.** No owner anywhere for: `Papers/`, `ga/`, `win_condition.py`, `track.py`, `LOGGING.md`, `PLAN.md`, `PROJECT.md`, `WIN_CONDITION.md`, `millennium_prize_problems.md`, `writeup/curate_evidence.py`, ~30 root analysis scripts, `solver/` as a standing dir, `reports/STATUS.md`. | grep of `ORCHESTRATION.md` §5 per structure audit | M | M to write; CB in effect (decides who may edit banked results) |
| C4 | `.claude/settings.json` cannot enforce §5a: **no `deny` block** for the five integration-owned ledgers or `DIRECTION.md` (Edit/Write allowlisted unconditionally — the one mechanism making ten-way parallelism safe is honor-system); `Bash(git push:*)` duplicated; blanket `mv`/`cp` allowed; the allowlisted fetch script is the staler of the two. | `.claude/settings.json`; `ORCHESTRATION.md` §5a | S | M (orchestrator-owned; propose, user applies) |
| C5 | **Root sprawl: 118 files.** 17 root `.py` are fully orphaned (no importer, ≤1 doc mention); 17 `.md` are frozen stage artifacts. **Do not move wholesale**: `writeup/curate_evidence.py` does bare imports of `analyze_stage2`, `phase1_gate4`, `win_condition` (root scripts are a live dependency of the rebuild path), and 18 markdown files cite root scripts by bare filename from banked prose (moving = escalation-#4 territory). Cheap fix: a root `ARCHIVE.md` classifying every root file live/frozen, and stop the growth. | structure audit §4; `writeup/curate_evidence.py` imports | L if moved / S as ARCHIVE.md | M (the ARCHIVE.md route); CB if any move touches banked links |
| C6 | `writeup/4_p2_lottery/` is 127 files flat and growing ~16/cycle; `data/` 64, `figures/` 53. **Recommendation: do not shard arc 4** (several-hundred-link rewrite across banked prose). Keep flat-and-indexed: make INDEX.md complete (B1) and start arc 5 in a fresh directory when the next arc opens. | file counts; `writeup/INDEX.md` "banked convention" | — | ruling for the DM; no work item until arc 5 |
| C7 | `PHASE2_P2_NOTES.md` (292 KB, 3,776 lines) was left out of the pointer-file reform that fixed `JOURNAL.md`/`LITERATURE_CHECK.md`; its TOP STATUS header is dated 2026-07-25 with no drift detector. It is integration-owned, so this is an orchestrator/DM decision, not sweep work. | `PHASE2_P2_NOTES.md:3,6-40` | L | **CB** (header summarizes gate outcomes) |

## Cross-cutting recommendation (highest leverage single item)

**A `test_docs_contract.py` peer to `test_capabilities.py`.** Root cause of most of §B:
drift detectors cover the plan triangle and the capability index, but *nothing* guards the
README stage table, `writeup/README.md`, `writeup/INDEX.md`, quartet completeness, or
figure-number uniqueness — and the merge gate contains no docs check at all. Items B1, B2,
B3, A3 and A4(iii) all become cheap, self-running assertions in the repo's existing style.
Build the detector first and the stale-index class stops recurring instead of being re-fixed
every cycle. Size: M. Kind: M (the detector); the fixtures it checks stay CB.

---

## D. Code-audit lane (dead code, duplication, test sweep, capabilities spot-check)

*Pending at commit time — appended when the audit lands. Until then: not audited ≠ clean.*
