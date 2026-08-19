"""E-FE (leg 408, wave 7, Lane R) -- ARTEFACT ASSEMBLER.

Deliberately a SEPARATE file from `e_fe_driver.py`.  The driver was committed
BEFORE the first attempt as the unit's pre-registration; editing it after
results exist would destroy that audit trail even for changes that touch only
reporting prose.  So the driver computes the gate and this file writes the
narrative blocks the brief requires around it.  Nothing here re-computes,
re-weights or re-thresholds any result: `gate()` is imported from the driver
and used as returned.

Run: .venv/bin/python experiments/programme_r4/e_fe_report.py
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import e_fe_driver as D                                    # noqa: E402

OUT = os.path.join(ROOT, "writeup", "data", "p2_e_fe_v1.json")


# --------------------------------------------------------------------------
# The two pre-committed readings, QUOTED from writeup/waves/WAVE7_PLAN.md SS B
# (lines 219-226 of that file at commit time), not paraphrased.
# --------------------------------------------------------------------------
PRE_COMMITTED = {
    "source": "writeup/waves/WAVE7_PLAN.md SS B, 'Pre-committed reading, "
              "both directions, before dispatch:'",
    "quoted_verbatim": True,
    "reading_if_0_of_160":
        "0 of 160 => the null is no longer about draws. With 10 draws per "
        "arm, a per-draw recovery probability above 26% is excluded at 95% "
        "for every row. That is a statement about the rows in this "
        "realization, and it is the strongest negative this programme can "
        "buy for ~11 h wall. It is not a statement about the rows in the "
        "published realization -- E-iv's realization gap and the N = 24 "
        "resolution limit both survive it, and must be restated in the "
        "artefact.",
    "reading_if_at_least_1_recovery":
        ">= 1 recovery => E's null was a draw artefact, M1's comparison "
        "changes, and Lane R's ranking is re-opened in that integration "
        "commit.",
    "dispatch_brief_amplification":
        "CONDUCTOR's dispatch added, on the >= 1 branch: 'This is the more "
        "interesting outcome. If it fires, say so plainly and do not hedge "
        "it into insignificance.' And on the 0 branch: the realization gap "
        "and the N = 24 limit are to be restated 'not omitted because the "
        "number looks strong.'",
}

EXCLUSION_ARITHMETIC = {
    "what_SS_B_says": "a per-draw recovery probability above 26% is excluded "
                      "at 95% for every row",
    "instruction": "CONDUCTOR: 'Compute and report the 26% figure yourself "
                   "rather than quoting mine; if your arithmetic disagrees "
                   "with 26%, your number wins and you flag the "
                   "discrepancy.'",
    "one_sided_95_upper_at_k0_n10": 1.0 - 0.05 ** (1.0 / 10.0),
    "two_sided_95_upper_at_k0_n10": 1.0 - 0.025 ** (1.0 / 10.0),
    "closed_form": "for k = 0 the Clopper-Pearson upper limit is "
                   "1 - alpha_upper**(1/n); alpha_upper = 0.05 one-sided, "
                   "0.025 equal-tailed two-sided",
    "verdict": "MY ARITHMETIC AGREES WITH SS B UNDER THE ONE-SIDED "
               "CONVENTION: 1 - 0.05**(1/10) = 0.2589, i.e. ~26%. It "
               "DISAGREES under the equal-tailed two-sided convention, which "
               "gives 1 - 0.025**(1/10) = 0.3085, i.e. ~31%. SS B asks in "
               "the same sentence for 'its exact binomial confidence "
               "interval' -- an interval is conventionally two-sided -- and "
               "then states a bound that is one-sided. The defect is the "
               "UNSTATED CONVENTION, not an arithmetic error. Both are "
               "computed and both are reported per (row, arm); no verdict "
               "in this artefact rests on which is preferred.",
    "checked_against": "scipy.stats.beta.ppf (scipy 1.18.0) to full float64 "
                       "precision, and against the closed form above",
}

SURVIVING_LIMITS = [
    {"limit": "E-iv realization gap",
     "restated": "This ensemble draws all 160 fields from ONE DNS "
                 "realization -- U2's T = 1e5 trajectory as re-integrated in "
                 "this tree. Ten fields per (row, arm) are ten independent "
                 "DRAWS FROM THAT REALIZATION, not ten realizations. A "
                 "negative here bounds the recovery probability of the rows "
                 "AS THEY SIT IN THIS REALIZATION. It says nothing about "
                 "the rows in Lucas & Kerswell's published realization.",
     "survives_the_result": True},
    {"limit": "N = 24 resolution limit",
     "restated": "Every attempt runs on the 24 x 24 grid at Re = 60, "
                 "n_forcing = 4, dt = 0.01 with a Lie-Trotter split that is "
                 "globally first order. If the published orbits are not "
                 "represented at this resolution, no number of draws can "
                 "recover them and this ensemble cannot distinguish that "
                 "from their absence. The limit is untouched by 160 "
                 "attempts.",
     "survives_the_result": True},
    {"limit": "scale is not evidence",
     "restated": "160 attempts is not 10x more evidence than 16. It is 10x "
                 "more DRAWS. The extra information is entirely in the "
                 "per-(row, arm) draw dimension; the row set, the arm "
                 "definitions, the seeded (T, s), the solver, its "
                 "tolerances and its caps are all IDENTICAL to E's.",
     "survives_the_result": True},
]

CEILINGS = [
    {"id": "C2-inherited", "from": "R-bank leg 404 artefact, ceiling C2",
     "ceiling": "The bank's gate (i) ran against THIS tree's checkpoint on "
                "THIS CPU. The bank is now the DEFINITION of the seed, not a "
                "cache of a machine-independent one. Cross-machine agreement "
                "is UNPRICED and this unit did not price it: every one of "
                "the 160 attempts ran on the same host as the bank build."},
    {"id": "C4-inherited", "from": "R-bank leg 404 artefact, ceiling C4",
     "ceiling": "Before this unit, the 144 non-original fields had never "
                "been fed to a solver by anything -- R-bank verified them as "
                "BYTES only. This unit is the first thing ever to run them. "
                "Any failure mode seen only in the 144 could in principle be "
                "theirs rather than the physics'. The 16 C-REPRO controls "
                "bound this from one side only: they show the PIPELINE is "
                "sound on the 16 fields that were solved before, not that "
                "the other 144 are good fields."},
    {"id": "C5-inherited-lesson-91", "from": "R-bank ceiling C5; lesson 91",
     "ceiling": "The bank's draw order is row-major and that is a DECLARED "
                "CHOICE, not a canonical ordering. THIS NULL NAMES ITS OWN "
                "REALIZATION: it is a statement about these 160 snapshots "
                "selected in this order from this trajectory, and a "
                "different declared order would have produced a different "
                "160."},
    {"id": "C1-inherited-functional-not-byte",
     "from": "R-bank leg 404 artefact, ceiling C1",
     "ceiling": "The bank's gate (ii) was a FUNCTIONAL check, not a byte "
                "check, for 15 of the 16 original fields -- only one attempt "
                "of 16 was re-solved end to end at bank time. This unit "
                "upgrades that: all 16 originals were re-solved here and "
                "compared field by field. That is a strengthening of an "
                "inherited ceiling, and it is reported as such rather than "
                "as a new result."},
    {"id": "C6-own-single-host",
     "from": "this unit",
     "ceiling": "The machine was NOT quiet. L6-b held ~5.2 of 12 cores "
                "throughout. Wall-clock per attempt here is a CONTENDED "
                "measurement and is not comparable to E's without the "
                "contention factor stated alongside it. Core-hours are the "
                "honest currency; wall hours are not."},
    {"id": "C7-predicate-scope", "from": "this unit",
     "ceiling": "'Recovery' means E's match_named predicate, unchanged: "
                "|T - T_pub| < 0.05 AND wrapped |s - s_pub| < 0.05 AND "
                "success. A converged orbit that is a genuine RPO of the "
                "system but not one of the eight named rows counts as NOT "
                "recovered here, by design. This unit did not attempt to "
                "identify what the converged solutions ARE."},
]

CLAY_MOVEMENT = {
    "links_moved": "none",
    "L1_to_L4_link_moved": False,
    "wall_moved": False,
    "clay_percent": 0.05,
    "tier": 2,
    "statement": "No L1->L4 link moved. No wall moved. Clay remains ~0.05%. "
                 "TIER 2 IS NEVER A PROOF. This unit is a numerical "
                 "measurement on a 24 x 24 truncation of 2D Kolmogorov flow "
                 "at Re = 60; it bears on the credibility of one "
                 "recovery-of-published-orbits claim inside Lane R and on "
                 "nothing above it.",
    "not_progress": "A tightened negative is not progress toward Clay and is "
                    "not described as such here.",
}

SOURCES_3K = {
    "rule_3_exemption": "SS 3k rule 3 (SOURCES.md row filled in the same "
                        "commit as pre-registration) is claimed EXEMPT for "
                        "the physics: this unit implements NO published "
                        "method of its own. It calls E's solver, E's Newton "
                        "loop, E's convergence test and E's row-matching "
                        "unchanged, and R-bank's loader unchanged. Every "
                        "published method in the call graph (Viswanath's "
                        "hookstep trust-region Newton-Krylov; Lucas & "
                        "Kerswell Table IV) is already registered against "
                        "the units that implemented it.",
    "row_OWED": {
        "reference": "Clopper, C. J. and Pearson, E. S. (1934), 'The use of "
                     "confidence or fiducial limits illustrated in the case "
                     "of the binomial', Biometrika 26(4):404-413",
        "why_owed": "The gate answer's confidence intervals rest on this "
                    "method, so SS 3k rule 1 would require a "
                    "writeup/SOURCES.md row in the same commit as this "
                    "unit's pre-registration.",
        "why_not_filled": "writeup/SOURCES.md is explicitly OUTSIDE this "
                          "unit's briefed territory ('Do not touch ... "
                          "writeup/SOURCES.md'). The row is therefore OWED "
                          "and is handed to CONDUCTOR to fill. Recorded as a "
                          "defect of the brief, not discharged silently.",
        "verified_by_this_unit": "the implementation is Beta-quantile "
                                 "inversion via scipy.stats.beta.ppf, "
                                 "checked against the closed form "
                                 "1 - alpha**(1/n) at k = 0 to full float64 "
                                 "agreement",
        "read_status": "method known and implemented; the 1934 paper itself "
                       "was NOT fetched by this unit, so no load-bearing "
                       "claim is made about its text -- only about the "
                       "interval it defines, which is standard and "
                       "independently checkable by the closed form above",
    },
    "no_claim_on_an_abstract": True,
}


def defects(doc, meta):
    d = [
        {"id": "D1", "where": "writeup/waves/WAVE7_PLAN.md SS B",
         "severity": "wording, affects how the headline number is read",
         "defect": "SS B asks for 'the recovery rate out of 10 with its "
                   "exact binomial confidence interval' and in the next "
                   "breath states a bound -- 'above 26% is excluded at 95%' "
                   "-- that is the ONE-SIDED 95% upper limit "
                   "(1 - 0.05**(1/10) = 0.2589). The equal-tailed two-sided "
                   "95% interval that 'confidence interval' conventionally "
                   "denotes has upper limit 1 - 0.025**(1/10) = 0.3085. The "
                   "convention is never stated.",
         "impact": "A reader who takes the interval at face value would "
                   "report a 31% exclusion; a reader who takes the 26% would "
                   "report a one-sided bound as if it were an interval.",
         "handled_by_this_unit": "both conventions computed, both named, "
                                 "both reported per (row, arm) and pooled; "
                                 "no verdict rests on the choice",
         "fix_is_CONDUCTORs": True},
        {"id": "D2",
         "where": "experiments/programme_r4/seedbank/manifest.json, 'what' "
                  "field",
         "severity": "factual, self-inconsistent within R-bank's own "
                     "deliverable",
         "defect": "The manifest's 'what' string still reads '... the 1.2 GB "
                   "gitignored DNS artefacts'. R-bank's OWN defect D1 "
                   "corrected that figure -- the measured size is "
                   "268,864,256 B = 268.9 MB, wrong by 4.5x. R-bank fixed "
                   "the .gitignore header beside it and let the same wrong "
                   "figure stand inside its own manifest.",
         "impact": "None on any number in this artefact -- the bank's bytes "
                   "are sound and were used as delivered. It is a "
                   "propagation defect: a corrected figure that did not "
                   "propagate into the artefact that carries it.",
         "handled_by_this_unit": "recorded only; R-bank's files are not this "
                                 "unit's to edit",
         "fix_is_CONDUCTORs": True},
        {"id": "D3", "where": "the E-FE dispatch brief (territory grant) vs "
                              "ORCHESTRATION.md SS 3k rule 1",
         "severity": "process conflict, unresolvable inside the unit",
         "defect": "SS 3k rule 1 requires a writeup/SOURCES.md row, in the "
                   "pre-registration commit, for a published method a gate "
                   "answer rests on. The gate's confidence intervals rest on "
                   "Clopper-Pearson (1934). The brief forbids this unit from "
                   "touching writeup/SOURCES.md.",
         "impact": "The unit cannot simultaneously obey both. It obeyed the "
                   "territory ban and recorded the row as OWED in "
                   "sources_3k.",
         "handled_by_this_unit": "row OWED, handed up, not filled",
         "fix_is_CONDUCTORs": True},
        {"id": "D4", "where": "experiments/programme_r4/e_hhard_diagnostic.py",
         "severity": "collision hazard, pre-empted",
         "defect": "E's module-level PARTIAL points at "
                   "experiments/programme_r4/e_hhard_partial and keys "
                   "checkpoints by bare attempt index. This unit's 160 "
                   "attempt indices would have collided with E's banked "
                   "0..15 and silently resumed from E's checkpoints.",
         "impact": "None -- caught before launch. The driver rebinds "
                   "E.PARTIAL to experiments/programme_r4/e_fe_partials/pkl "
                   "as its ONE declared monkeypatch, changing no algorithm, "
                   "seed, tolerance or cap. Declared in the driver docstring "
                   "and in journal leg_408 SS 1 before the run.",
         "handled_by_this_unit": "pre-empted and declared",
         "fix_is_CONDUCTORs": False},
        {"id": "D5", "where": "experiments/programme_r4/e_fe_driver.py, "
                              "commit_partials()",
         "severity": "false alarm in this unit's own run log; no data effect",
         "defect": "The no-op guard tests for the substring 'nothing to "
                   "commit' in git's output. In PATHSPEC mode -- "
                   "`git commit -m msg -- <paths>`, which this unit uses "
                   "deliberately so a sibling worker's staged files can never "
                   "be swept in -- git does NOT print that string when the "
                   "given paths are clean; it prints 'Changes not staged for "
                   "commit:' and exits non-zero. So a checkpoint that had "
                   "nothing to do was retried six times and then logged as "
                   "'[commit] FAILED after retries at #5 t+4.6h'.",
         "impact": "None on the record. Verified at the time: the working "
                   "tree was clean for this unit's paths because a "
                   "concurrent CONDUCTOR session had committed them at "
                   "04:58Z (commit edb9f6b) and this unit's own poll-loop "
                   "checkpoints were running every ~9 min. Nothing was lost. "
                   "The cost is that a benign event was logged in the "
                   "vocabulary of a failure, which is the opposite of what a "
                   "run log is for.",
         "handled_by_this_unit": "diagnosed by probing git's pathspec-mode "
                                 "wording directly; the driver was NOT "
                                 "patched, because the fix is cosmetic and "
                                 "editing a pre-registered driver to quiet a "
                                 "log line is a worse trade than recording "
                                 "the defect",
         "fix_is_CONDUCTORs": False},
        {"id": "D6", "where": "the resourcing rationale in CONDUCTOR's "
                              "dispatch ('12 cores')",
         "severity": "cost model, load-bearing for the wall-clock estimate",
         "defect": "os.cpu_count() and nproc both report 12 on this host, "
                   "and the shard decision was reasoned from that. The CPU "
                   "is an Intel Core i7-10750H: SIX physical cores, twelve "
                   "hyperthreads. Six E-FE shards plus L6-b's ~4.5 threads "
                   "oversubscribe six physical cores, and hyperthread "
                   "siblings share the execution units an FFT loop is bound "
                   "by. Measured alongside it: every logical CPU was pinned "
                   "at exactly 1800 MHz -- the governor is 'powersave', the "
                   "package was at 78 C and the part's rated max is 5000 "
                   "MHz -- so the all-core clock was roughly half the "
                   "single-core clock the banked figures were taken at.",
         "impact": "This, not scheduler contention, is the bulk of the "
                   "measured per-attempt inflation over E's banked walls. "
                   "The shards were each getting ~91% of a LOGICAL cpu, "
                   "which looks healthy and is not: the physical core behind "
                   "it was shared. Reported in cost_and_shortfall rather "
                   "than smoothed into a single 'contention' number.",
         "handled_by_this_unit": "measured (per-process CPU-time over a 60 s "
                                 "window, /proc/cpuinfo, "
                                 "/sys/.../cpufreq/*, thermal zones) and "
                                 "reported; the shard count was NOT changed, "
                                 "as the brief requires",
         "fix_is_CONDUCTORs": True},
    ]
    if meta.get("shards") and meta.get("briefed_wall_hours_at_6_shards"):
        pass
    return d


def cost_block(meta, doc):
    briefed_ch = meta.get("briefed_budget_core_hours", 91.0)
    briefed_wh = meta.get("briefed_wall_hours_at_6_shards", 15.2)
    wall_s = meta.get("wall_seconds")
    wall_h = meta.get("wall_hours")
    core_h = meta.get("core_hours")
    n = doc["gate"]["n_attempts"]
    att_wall = sum(r for r in _attempt_walls())
    over = None
    if wall_h:
        over = (wall_h - briefed_wh) / briefed_wh
    block = dict(
        UNDER_RESOURCED=False,
        under_resourced_statement=(
            "NOT under-resourced. Every one of the 160 briefed attempts ran "
            "to a terminal state and the gate is answered on the full 160. "
            "No attempt was dropped, shortened, or reported as a null "
            "because the budget ran out."),
        briefed_budget_core_hours=briefed_ch,
        briefed_wall_hours_at_6_shards=briefed_wh,
        briefed_basis=("E's 16 attempts cost 32,718.3 s = 9.088 core-h; x10 "
                       "= 90.9 core-h. CONDUCTOR chose 6 shards over the "
                       "price sheet's 8 because the box is 12 cores and "
                       "L6-b holds ~5.2 of them, and R-prof had already "
                       "banked MACHINE_WAS_NOT_QUIET = true."),
        shards=meta.get("shards"),
        shards_raised_mid_run=False,
        shards_note=("fixed at 6 for the entire run and never raised, so "
                     "per-attempt cost is clean"),
        cores=meta.get("cores"),
        started_utc=meta.get("started_utc"),
        finished_utc=meta.get("finished_utc"),
        wall_seconds=wall_s, wall_hours=wall_h, core_hours=core_h,
        loadavg_at_start=meta.get("loadavg_at_start"),
        loadavg_at_end=meta.get("loadavg_at_end"),
        n_attempts=n,
        sum_of_attempt_wall_seconds=att_wall,
        seconds_per_attempt_measured=(att_wall / n if n else None),
        E_seconds_per_attempt=2044.9,
        commits_during_run=meta.get("commits_during_run"),
        wall_overrun_fraction_vs_briefed=over,
        wall_overrun_exceeds_30pc=(bool(over is not None and over > 0.30)),
        core_hour_overrun_fraction_vs_briefed=(
            (core_h - briefed_ch) / briefed_ch if core_h else None),
        contention_narrative=(
            "The machine was NOT quiet and its speed CHANGED under the run, "
            "so a single contention factor would be a fiction. Measured, in "
            "order: (1) at t+0.4 h, controls P and R reproduced E's banked "
            "values exactly but took 4.07x and 4.16x E's banked wall; (2) at "
            "t+1.3 h, the first six real attempts ran at 1.84x E's banked "
            "wall (range 1.74-2.04x) -- the controls are Krylov-heavier than "
            "an attempt and overstate the penalty; (3) extrapolating (2) "
            "gave a projection of ~28 h, which was recorded at the time and "
            "is REPORTED HERE AS WRONG rather than quietly dropped; (4) from "
            "t+6 h the other lanes' jobs finished, the all-core clock rose "
            "from 1800 to 2000 MHz, throughput went from ~5.7 to ~13 "
            "attempts/h, and the run landed at 16.67 h. The projection was "
            "wrong because it assumed a fixed machine; the measurement is "
            "the number that counts."),
        clock_and_cores_measured=(
            "Intel Core i7-10750H: 6 PHYSICAL cores, 12 hyperthreads. "
            "os.cpu_count() and nproc report 12, which is what the shard "
            "decision was reasoned from -- see defect D6. Governor "
            "'powersave'; every logical cpu pinned at 1800 MHz early in the "
            "run (rated max 5000 MHz, package 78 C), rising to 2000 MHz once "
            "the box emptied. Each shard held 90-94% of a LOGICAL cpu "
            "throughout, which looks healthy and is not the same as holding "
            "a physical core."),
        under_resourced_test=(
            "The 30% threshold the brief set was NOT crossed: measured "
            "16.665 h against a briefed 15.2 h is +9.6%, and 99.99 core-h "
            "against a briefed 91 is +9.9%. Both are reported rather than "
            "only the total, as the brief requires."),
        partials_and_loss_exposure=(
            "18 checkpoint commits landed during the run (the driver's "
            "55-min committer thread plus a ~9-min poll-loop checkpoint "
            "taken by this unit after the committer's t+3.7 h slot was "
            "observed empty -- see defect D5 for why that slot was empty and "
            "benign). Nothing was ever more than ~9 min of wall from a "
            "tracked commit, against the brief's stated ~0.57 core-h "
            "exposure for a host exit."),
    )
    return block


def _attempt_walls():
    for r in D._load_partials().values():
        yield r["wall_seconds"]


def main():
    doc = D.gate(None)
    with open(D.RUNLOG) as f:
        meta = json.load(f)

    n_own = doc["gate"]["n_recovered_its_own_named_row"]
    n_any = doc["gate"]["n_recovered_any_named_row"]
    fired = "0_of_160" if (n_own == 0 and n_any == 0) else "at_least_1"

    doc["readings"] = dict(
        pre_committed=PRE_COMMITTED,
        exclusion_arithmetic_computed_by_this_unit=EXCLUSION_ARITHMETIC,
        which_fired=fired,
        which_fired_plain=(
            "The 0-of-160 branch fired." if fired == "0_of_160" else
            "THE >= 1 RECOVERY BRANCH FIRED. E's null was a draw artefact. "
            "M1's comparison changes and Lane R's ranking is re-opened in "
            "the integration commit. Stated plainly and not hedged."),
        anything_loosened=False,
        loosening_statement=(
            "NOTHING WAS LOOSENED. TOL, MAX_NEWTON, MAX_GMRES, GMRES_RTOL, "
            "the stall rule, T_ANCHOR_TOL, MATCH_T_TOL and MATCH_S_TOL were "
            "imported from e_hhard_diagnostic.py and never rebound. The row "
            "set was not widened, no arm was added, no Newton parameter was "
            "tuned and no tolerance was adjusted to make anything converge. "
            "Three temptations were recorded in journal leg_408 SS 4 and all "
            "three knobs were left alone."),
        temptations_recorded_not_taken=[
            "E's attempt 2 (UPO35 S) missed on |s| by 0.0854 against "
            "MATCH_S_TOL = 0.05. Widening the tolerance to 0.09 would have "
            "produced a 'recovery'. Not widened.",
            "14 of E's 16 attempts exited 'stalled' rather than hitting a "
            "Newton cap. Relaxing the stall rule would have converted some "
            "into converged-but-not-recovered. Not relaxed.",
            "MAX_NEWTON = 52 and GMRES_RTOL = 1e-3 are E's; raising the cap "
            "or tightening the Krylov solve would change every number. "
            "Imported, not redefined.",
        ],
        not_a_grinder=(
            "This is NOT a grinder. 160 attempts at FIXED rows and arms, "
            "varying ONLY the draw. No new seed supply, no GA, no learned or "
            "evolved seed-scoring fitness. SCALE IS NOT EVIDENCE: 160 "
            "attempts is not 10x more evidence than 16, it is 10x more "
            "DRAWS."),
        surviving_limits_restated=SURVIVING_LIMITS,
    )
    doc["cost_and_shortfall"] = cost_block(meta, doc)
    doc["ceilings"] = CEILINGS
    doc["defects_found"] = defects(doc, meta)
    doc["clay_movement"] = CLAY_MOVEMENT
    doc["sources_3k"] = SOURCES_3K
    doc["cost_and_shortfall"]["gate_assembled_utc"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    doc["git_head_at_assembly"] = subprocess.run(
        ["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True,
        text=True).stdout.strip()
    doc["self_hash_recipe"] = D.RECIPE
    doc["self_hash"] = D.self_hash(doc)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True, default=float)
    # fixed-point check: re-hash what was actually written
    with open(OUT) as f:
        back = json.load(f)
    ok = D.self_hash(back) == doc["self_hash"]
    print(f"wrote {OUT}")
    print(f"self_hash = {doc['self_hash']}  fixed_point_reproduces = {ok}")
    if not ok:
        raise SystemExit("self_hash is NOT a fixed point -- STOP")
    g = doc["gate"]
    print(f"n_attempts={g['n_attempts']} converged={g['n_converged']} "
          f"own_row={g['n_recovered_its_own_named_row']} "
          f"any_row={g['n_recovered_any_named_row']} "
          f"ANY_ROW_RECOVERS={g['ANY_ROW_RECOVERS_IN_ANY_DRAW']}")


if __name__ == "__main__":
    main()
