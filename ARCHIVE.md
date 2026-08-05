# ARCHIVE — root-file classification

Produced by the maintenance sweep (`reports/TECH_DEBT_REVIEW_2026-08-05.md` item C5:
"Root sprawl — 118 files at repo root"). This is a **classification document only** — no
files are moved. The review explicitly warns that `writeup/curate_evidence.py` does bare
imports of several root scripts (a live dependency of the rebuild path) and that ~18
markdown files cite root scripts by bare filename from banked prose, so moving anything is
escalation-#4 territory, not the sweep's to do.

**Method:** every root-level `.py` and `.md` file was checked for (i) `git log --oneline`
history (dated, commit count) and (ii) references elsewhere in the tree — Python imports
(`from X import ...` / `import X`) and bare-filename mentions in `.py`/`.md` prose,
via `grep -rlE`. A file is **LIVE** if it is imported by a currently-run script (chiefly
`writeup/curate_evidence.py`, the rebuild-path entry point), is part of the 52-file test
suite (`test_*.py`, mapped by `capabilities.py` / `scripts/merge_gate.sh`), or is an
actively-maintained contract/ledger/status doc. A file is **FROZEN** if it is a
closed-stage artifact (single commit, dated 2026-07-22 through 07-26, no current-code
importer) kept only as banked prose / citation target for older results docs.

Legend: **LIVE** = actively imported, tested, or maintained; **FROZEN** = historical stage
artifact, referenced only as banked prose, not touched by current work.

## Root `.py` files (85)

### LIVE — core ledgers / infra (11)

| File | Why LIVE |
|---|---|
| `capabilities.py` | Capability ledger; imported/tested everywhere (`test_capabilities.py`, `README.md`, `ORCHESTRATION.md`); last touched 2026-08-05. |
| `plan_of_record.py` | Stage-machine source of truth; tested by `test_plan_of_record.py`; imported by `experiments/*.py`; last touched 2026-08-05. |
| `track.py` | Logging/provenance helper; imported by `solver/weight_search.py`, `experiments/*.py`; contract doc `LOGGING.md`. |
| `win_condition.py` | Bare-imported by `writeup/curate_evidence.py` (`from win_condition import estimate_blowup_time`); tested by `test_win_condition.py`. |
| `analyze_stage2.py` | Bare-imported by `writeup/curate_evidence.py` (`GA_OPERATORS, best_so_far_curve, load_events`). |
| `analyze_nongenericity.py` | Bare-imported by `writeup/curate_evidence.py` (`load`, `verdict_for_a`). |
| `analyze_stage2_5.py` | Transitively live: `analyze_nongenericity.py` does `from analyze_stage2_5 import spearman`. |
| `analyze_stage3_6.py` | Bare-imported by `writeup/curate_evidence.py` (`classify`, `load`). |
| `analyze_phase1_axis_screen.py` | Bare-imported by `writeup/curate_evidence.py` (`AXES, NEEDED, evaluate_axis, load`). |
| `phase1_gate4.py` | Bare-imported by `writeup/curate_evidence.py` (`build_roster`). |
| `analyze_phase1_gate4_reform.py` | Bare-imported by `writeup/curate_evidence.py` (`evaluate`). |

### LIVE — test suite (52)

All root `test_*.py` files are LIVE: they are the project's entire test suite, individually
mapped in `scripts/merge_gate.sh` and/or listed in `capabilities.py`'s module→test
entries, and run via `.venv/bin/python -m pytest`. Listed for completeness rather than
file-by-file rationale (identical reason for all 52):

`test_advection_scope.py`, `test_bordered_hl.py`, `test_boussinesq_rescaled.py`,
`test_boussinesq_transport.py`, `test_boussinesq_velocity.py`, `test_boussinesq_wall.py`,
`test_capabilities.py`, `test_certificate_shapes.py`, `test_collocation_newton.py`,
`test_critical_dissipation.py`, `test_decay_collocation.py`, `test_decay_grading.py`,
`test_first_integral.py`, `test_fractional_boussinesq.py`, `test_fractional_gclm.py`,
`test_ga.py`, `test_gclm_family.py`, `test_gclm_rescaled.py`, `test_genome_2d.py`,
`test_genome_rough_2d.py`, `test_genome_rough.py`, `test_hl_rescaled.py`,
`test_holder_norms.py`, `test_interval_certificate.py`, `test_interval.py`,
`test_line_hilbert.py`, `test_literature_gates.py`, `test_logbook.py`,
`test_marginal_flow.py`, `test_nk_bounds.py`, `test_nk_fourier.py`,
`test_nk_hilbert_holder.py`, `test_nk_hilbert_pointwise.py`, `test_nk_seminorm.py`,
`test_op_lower.py`, `test_phase1_measurement.py`, `test_plan_of_record.py`,
`test_port_certification.py`, `test_profile_newton.py`, `test_reduced_certificate.py`,
`test_rescaled_spectrum.py`, `test_resolution_study.py`, `test_route_g_perf.py`,
`test_solver_boussinesq.py`, `test_solver_clm.py`, `test_spectral_certificate.py`,
`test_target_norm.py`, `test_target_selection.py`, `test_turning_point.py`,
`test_viscous_novelty.py`, `test_weight_search.py`, `test_win_condition.py`.

### FROZEN — closed-stage artifacts (22)

All dated 2026-07-22 through 2026-07-24, single commit, no importer in currently-run code.
Kept as the data-generation/analysis scripts behind their matching `*_RESULTS.md` /
`PHASE1_*.md` docs — do not delete (banked-prose citations, see caveat above).

| File | Last commit | Cited by (banked prose / historical) |
|---|---|---|
| `analyze_phase1_gate4.py` | 2026-07-24 | `PHASE1_GATE4_RESULTS.md`, `writeup/2_phase1_2d/BLOG_PHASE1_GATE4.md` |
| `analyze_phase1_spike.py` | 2026-07-23 | `PHASE1_SPIKE_RESULTS.md` |
| `analyze_stage1_5.py` | 2026-07-22 | `STAGE_1_5_RESULTS.md` |
| `analyze_stage2_6.py` | 2026-07-22 | `STAGE_2_6_RESULTS.md` |
| `nongenericity_sweep.py` | 2026-07-23 | `NONGENERICITY_RESULTS.md`, `PROJECT.md` |
| `phase1_axis_progress.py` | 2026-07-23 | none (0 references found) |
| `phase1_axis_screen.py` | 2026-07-23 | `PHASE1_AXIS_SCREEN_RESULTS.md` (data-gen runner; only its *analysis* counterpart is live) |
| `phase1_currency_probe.py` | 2026-07-24 | `PHASE1_GATE4_RESULTS.md` |
| `phase1_gate4_probe.py` | 2026-07-24 | `PHASE1_GATE4_RESULTS.md` |
| `phase1_gate4_reform.py` | 2026-07-24 | `PHASE1_GATE4_REFORM_RESULTS.md` (data-gen runner; only `analyze_phase1_gate4_reform.py` is live) |
| `phase1_gsustained_probe.py` | 2026-07-24 | `PHASE1_GSUSTAINED_RESULTS.md` |
| `phase1_gsustained_rankcheck.py` | 2026-07-24 | `PHASE1_GSUSTAINED_RESULTS.md` |
| `phase1_progress.py` | 2026-07-23 | none (0 references found) |
| `phase1_resolution_spike.py` | 2026-07-23 | `PHASE1_SPIKE_RESULTS.md` |
| `phase2_spike0_probe.py` | 2026-07-24 | `PHASE2_SPIKE0_NOTES.md` |
| `stage1_5_sweep.py` | 2026-07-22 | `STAGE_1_5_RESULTS.md` |
| `stage2_5_sweep.py` | 2026-07-22 | `STAGE_2_5_RESULTS.md` |
| `stage2_6_progress.py` | 2026-07-22 | none (0 references found) |
| `stage2_6_sweep.py` | 2026-07-22 | `STAGE_2_6_RESULTS.md` |
| `stage2_progress.py` | 2026-07-22 | none (0 references found) |
| `stage3_6_progress.py` | 2026-07-23 | `STAGE_3_6_RESULTS.md` |
| `stage3_6_sweep.py` | 2026-07-23 | `STAGE_3_6_RESULTS.md` |

## Root `.md` files (30)

### LIVE — contracts, ledgers, current-state docs (11)

| File | Why LIVE |
|---|---|
| `README.md` | Root readme, first-read entry point; last touched 2026-08-05. |
| `PROJECT.md` | Top-level project description, linked from README; last touched 2026-08-05 (flagged stale in places by tech-debt B4, but still actively read/maintained, not a closed artifact). |
| `ORCHESTRATION.md` | The orchestration contract itself. |
| `ORCHESTRATOR_PROMPT.md` | Orchestrator's operating prompt. |
| `CONTINUATION_PROMPT.md` | Handed to every leg agent; integration-owned ledger. |
| `DIRECTION.md` | Live territory/queue ledger; integration-owned. |
| `LITERATURE_CHECK.md` | Live literature-gate ledger. |
| `PHASE2_P2_NOTES.md` | Current arc's working notes; most-active file in the tree (44 commits, last 2026-08-05); integration-owned. |
| `CLAY_ROADMAP.md` | Active roadmap/plan document (some sections stale per tech-debt B5, but still the canonical plan doc, actively edited). |
| `LOGGING.md` | Logging schema contract, tested against by `test_logbook.py` and consumed by `ga/`/`solver/` modules. |
| `WIN_CONDITION.md` | Canonical win-condition contract, paired with the live `win_condition.py`; still the referenced definition (21 references across current docs). |

### FROZEN — closed-stage results / superseded plans (19)

| File | Last commit | Notes |
|---|---|---|
| `PLAN.md` | 2026-07-23 | Superseded as the authoritative plan by `plan_of_record.py` + `CLAY_ROADMAP.md`; kept for banked-prose citations. |
| `PHASE1_PLAN.md` | 2026-07-24 | Phase 1 closed. |
| `PHASE2_NUMERICS_PLAN.md` | 2026-07-26 | Early Phase 2 plan, superseded by `PHASE2_P2_NOTES.md`. |
| `PHASE2_SPIKE0_NOTES.md` | 2026-07-24 | Spike closed. |
| `PHASE2_SPIKE1_NOTES.md` | 2026-07-26 | Spike closed. |
| `PHASE1_AXIS_SCREEN_RESULTS.md` | 2026-07-23 | Closed-stage results doc. |
| `PHASE1_GATE4_RESULTS.md` | 2026-07-24 | Closed-stage results doc. |
| `PHASE1_GATE4_REFORM_RESULTS.md` | 2026-07-24 | Closed-stage results doc. |
| `PHASE1_GATE4_REFORMULATED_PREDICATE.md` | 2026-07-24 | Closed-stage results doc. |
| `PHASE1_GSUSTAINED_RESULTS.md` | 2026-07-24 | Closed-stage results doc. |
| `PHASE1_SPIKE_RESULTS.md` | 2026-07-23 | Closed-stage results doc. |
| `STAGE_1_5_RESULTS.md` | 2026-07-22 | Closed-stage results doc. |
| `STAGE_2_RESULTS.md` | 2026-07-22 | Closed-stage results doc. |
| `STAGE_2_5_RESULTS.md` | 2026-07-22 | Closed-stage results doc. |
| `STAGE_2_6_RESULTS.md` | 2026-07-23 | Closed-stage results doc. |
| `STAGE_3_RESULTS.md` | 2026-07-23 | Closed-stage results doc. |
| `STAGE_3_6_RESULTS.md` | 2026-07-23 | Closed-stage results doc. |
| `NONGENERICITY_RESULTS.md` | 2026-07-23 | Closed-stage results doc. |
| `millennium_prize_problems.md` | 2026-07-22 | Static background reference (Clay problem statement), not touched since initial add. |

## What this document is not

This is not a plan to move, delete, or rewrite anything — the FROZEN files remain exactly
where they are and continue to serve as citation targets for banked prose (per the
tech-debt review's explicit warning against wholesale moves). It exists so future sweeps
and the DM can tell at a glance which root files are load-bearing versus archival without
re-deriving the same `git log`/`grep` sweep each cycle. If a FROZEN file's status changes
(e.g. a new script starts importing it), update its row here rather than re-auditing the
whole tree.
