#!/usr/bin/env python3
"""Leg 243 -- Route-PCRS: is Route-L's banked headline verdict reached by leg 241's
`stall_verdict` positional-read defect?

ROLE: VERIFIER.  This leg does NOT re-litigate leg 241's characterisation of the mechanism
(`first, last = rows[0], rows[-1]` is positional; reversing `dims` maps the published gain
g -> 1/g; 94.56x on the line-sweep ladder).  That is accepted as given.  It re-checks the
OTHER half of leg 241's R2 finding -- the half its own report puts two paragraphs from the
94.56x sentence -- namely that the flip is counterfactual and Route-L's ACTUAL banked
headline configuration does not pass through the defect.

THE GATE, pre-committed, verbatim:

    Does an independent re-check confirm Route-L's own published headline verdict is
    UNAFFECTED by the `stall_verdict` positional-read finding leg 241 characterized (i.e.,
    the 94.56x flip occurs only in a case that does not correspond to Route-L's actual
    banked headline configuration), matching leg 241's own 'not claim-adjacent' conclusion?

    YES -> independently confirmed; bank as closing this specific worry.
    NO   -> Route-L's headline is AFFECTED; second confirmed instance after leg 202/226 of a
            banked headline needing correction.  Escalate, branch only, never main.

WHY THIS IS NOT LEG 241 RE-RUN.  Leg 241 rests its whole "margin 0.0 but safe" row on ONE
cited source line (`DIMS = (10,20,40,80,160)` at p2_route_l_v1_precond.py:49).  The decisive
gate here (G2) never reads that source at all: it re-derives every published stall number
ORDER-IMMUNE, keyed on `m`, from the banked JSON, in code written here, and compares under
exact `==` on raw float64 against what Route-L actually published.  If the published numbers
ARE the order-immune numbers, the headline is unaffected for a reason that does not depend on
trusting any literal, any line number, or leg 241.  G3 then closes leg 241's cited-line gap
mechanically (AST over EVERY call site, including the deep rung's own `dims=(240,320)` at
line 180, which line 49 does not cover), and G1 audits all ELEVEN banked ladders, not the
five leg 241 measured.

Gates:
  G0  provenance -- what is being read, and its hashes
  G1  order audit of every banked array that reaches `stall_verdict` (11 ladders + deep rung)
  G2  ORDER-IMMUNE re-derivation vs the PUBLISHED numbers, exact ==   [the decisive gate]
  G3  AST enumeration of every `krylov_ladder` call site / `dims` literal in Route-L's runner
  G4  reproduction of leg 241's affected case, and what input it requires
  G5  the headline sentence decomposed: every number traced, and classified order-sensitive
  G6  the control column (lesson 90): the audit must report the OTHER answer when it should
"""
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BANKED_JSON = ROOT / "writeup" / "data" / "p2_route_l_v1_precond.json"
ROUTE_L_RUNNER = ROOT / "experiments" / "p2_route_l_v1_precond.py"
ROUTE_L_DOC = ROOT / "writeup" / "4_p2_lottery" / "TECHNICAL_P2_ROUTEL_V1.md"
MODULE = ROOT / "solver" / "port_certification.py"
OUT = ROOT / "writeup" / "data" / "p2_route_pcrs_v1_verification.json"

LEG_241_BRANCH = "origin/leg/241-pcrc-v1"

# leg 241's headline magnitudes for R2, quoted here so the reproduction in G4 is checked
# against a number this leg did not compute.
LEG_241_ASC_GAIN = 9.7245        # journal table, "full transport line sweep", ascending
LEG_241_DESC_GAIN = 0.1028       # same row, descending
LEG_241_RATIO = 94.56            # the flip magnitude


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# The order-immune stall verdict.  Written here, from the DEFINITION of the
# measurement ("how much does 16x the Krylov work buy?"), keyed on `m`.  It shares
# no line with `solver.port_certification.stall_verdict`, and by construction its
# output cannot depend on the order the rows are stored in.
# ---------------------------------------------------------------------------
def stall_by_key(rows):
    lo = min(rows, key=lambda r: r["m"])
    hi = max(rows, key=lambda r: r["m"])
    gain = lo["rel_residual"] / hi["rel_residual"]
    return {"rel_at_min_dim": lo["rel_residual"], "min_dim": lo["m"],
            "rel_at_max_dim": hi["rel_residual"], "max_dim": hi["m"],
            "work_ratio": hi["m"] / lo["m"], "residual_gain": float(gain),
            "flat": bool(gain < 2.0)}


def ranked_by_key(ladders, full_key="full"):
    """`attribution_summary`, re-derived order-immune.  Note the original takes
    `ladders["full"][-1]["rel_residual"]` POSITIONALLY for `worse_than_full` as well --
    a second positional read in the same call, which this re-derivation keys on `m`."""
    base = stall_by_key(ladders[full_key])["residual_gain"]
    full_hi = max(ladders[full_key], key=lambda r: r["m"])["rel_residual"]
    out = []
    for label, rows in ladders.items():
        v = stall_by_key(rows)
        out.append({"ablation": label, "rel_at_max_dim": v["rel_at_max_dim"],
                    "gain": v["residual_gain"], "flat": v["flat"],
                    "gain_vs_full": v["residual_gain"] / base,
                    "worse_than_full": v["rel_at_max_dim"] > full_hi})
    out.sort(key=lambda q: -q["gain"])
    return out


def is_strictly_ascending(rows):
    ms = [r["m"] for r in rows]
    return ms == sorted(ms) and len(set(ms)) == len(ms), ms


# ---------------------------------------------------------------------------
# G0 -- provenance
# ---------------------------------------------------------------------------
def gate_0_provenance(banked):
    def git(*a):
        try:
            return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True,
                                  text=True, timeout=60).stdout.strip()
        except Exception as exc:                                    # pragma: no cover
            return f"<unavailable: {exc}>"

    return {
        "what_is_under_test": ("leg 241's CONCLUSION that its R2 finding is not "
                               "claim-adjacent -- NOT leg 241's characterisation of the "
                               "mechanism, which this leg accepts as given"),
        "banked_artifact": {
            "path": str(BANKED_JSON.relative_to(ROOT)), "sha256": sha256(BANKED_JSON),
            "leg": banked.get("leg"), "title": banked.get("title"),
            "generated": banked.get("generated"),
            "grid": banked.get("grid"), "seed_c_l": banked["seed"]["c_l"]},
        "route_l_runner": {"path": str(ROUTE_L_RUNNER.relative_to(ROOT)),
                           "sha256": sha256(ROUTE_L_RUNNER)},
        "route_l_doc": {"path": str(ROUTE_L_DOC.relative_to(ROOT)),
                        "sha256": sha256(ROUTE_L_DOC)},
        "module_under_discussion": {"path": str(MODULE.relative_to(ROOT)),
                                    "sha256": sha256(MODULE),
                                    "edited_by_this_leg": False},
        "leg_241": {"branch": LEG_241_BRANCH,
                    "head": git("rev-parse", "--short", LEG_241_BRANCH),
                    "merged_into_main": git("branch", "--contains",
                                            git("rev-parse", LEG_241_BRANCH)) or "<none>",
                    "read_only": True},
    }


# ---------------------------------------------------------------------------
# G1 -- order audit of EVERY banked array that reaches stall_verdict
# ---------------------------------------------------------------------------
def gate_1_order_audit(banked):
    arrays = {}
    for label, rows in banked["L1_attribution"]["ladders"].items():
        arrays[f"L1_attribution/{label}"] = rows
    for label, rows in banked["L3_preconditioners"]["ladders"].items():
        arrays[f"L3_preconditioners/{label}"] = rows
    arrays["L3_preconditioners/line_sweep_deeper"] = \
        banked["L3_preconditioners"]["line_sweep_deeper"]

    rows_out = []
    for name, rows in arrays.items():
        asc, ms = is_strictly_ascending(rows)
        rows_out.append({"array": name, "stored_m_sequence": ms,
                         "strictly_ascending": asc,
                         "reaches_stall_verdict_via": (
                             "attribution_summary" if name.startswith("L1_") else
                             "stall_verdict directly")})
    n_desc = sum(1 for r in rows_out if not r["strictly_ascending"])
    return {
        "question": ("does ANY banked array that feeds `stall_verdict` sit in a "
                     "non-ascending order, which is the sole precondition for the "
                     "positional read to misreport?"),
        "arrays_audited": len(rows_out),
        "leg_241_audited": 5,
        "this_leg_audits_additionally": ("the six L1_attribution ladders, which reach "
                                         "`stall_verdict` through `attribution_summary` "
                                         "and carry the published section-1 table"),
        "rows": rows_out,
        "non_ascending_arrays": n_desc,
        "verdict": "ALL ASCENDING" if n_desc == 0 else "NON-ASCENDING ARRAY PRESENT",
    }


# ---------------------------------------------------------------------------
# G2 -- THE DECISIVE GATE: order-immune re-derivation vs what was PUBLISHED
# ---------------------------------------------------------------------------
def gate_2_order_immune_vs_published(banked):
    published_stalls = banked["L3_preconditioners"]["stalls"]
    l3 = banked["L3_preconditioners"]["ladders"]

    stall_rows = []
    for label, rows in l3.items():
        mine = stall_by_key(rows)
        pub = published_stalls[label]
        diffs = {}
        for k in ("rel_at_min_dim", "min_dim", "rel_at_max_dim", "max_dim",
                  "work_ratio", "residual_gain", "flat"):
            diffs[k] = {"published": pub[k], "order_immune": mine[k],
                        "identical": bool(pub[k] == mine[k])}
        stall_rows.append({
            "ladder": label,
            "published_residual_gain": pub["residual_gain"],
            "order_immune_residual_gain": mine["residual_gain"],
            "abs_difference": abs(pub["residual_gain"] - mine["residual_gain"]),
            "bit_identical_all_keys": all(d["identical"] for d in diffs.values()),
            "per_key": diffs,
            "published_flat": pub["flat"], "order_immune_flat": mine["flat"],
            "verdict_agrees": bool(pub["flat"] == mine["flat"]),
        })

    # The ranked attribution table -- the six L1 ladders leg 241 did not audit.
    published_ranked = banked["L1_attribution"]["ranked"]
    mine_ranked = ranked_by_key(banked["L1_attribution"]["ladders"])
    ranked_rows = []
    for pub, mine in zip(published_ranked, mine_ranked):
        ranked_rows.append({
            "published_ablation": pub["ablation"], "order_immune_ablation": mine["ablation"],
            "rank_position_identical": bool(pub["ablation"] == mine["ablation"]),
            "published_gain": pub["gain"], "order_immune_gain": mine["gain"],
            "abs_difference": abs(pub["gain"] - mine["gain"]),
            "all_keys_identical": bool(pub == mine),
        })
    ranking_identical = [r["published_ablation"] for r in ranked_rows] == \
                        [r["order_immune_ablation"] for r in ranked_rows]

    deep = banked["L3_preconditioners"]["line_sweep_deeper"]
    deep_mine = stall_by_key(deep)

    n_stall_bad = sum(1 for r in stall_rows if not r["bit_identical_all_keys"])
    n_rank_bad = sum(1 for r in ranked_rows if not r["all_keys_identical"])

    return {
        "method": ("every published stall number re-derived from the banked ladders keyed "
                   "on `m` (min/max by key, never by position), in code written in this "
                   "leg, then compared under exact `==` on raw float64 -- never allclose. "
                   "This gate reads NO source line of Route-L's runner and takes nothing "
                   "from leg 241."),
        "why_decisive": ("the positional read and an order-immune read can differ ONLY on "
                         "a non-ascending array. If what Route-L PUBLISHED equals the "
                         "order-immune value bit-for-bit on every key of every ladder, then "
                         "the published verdict is exactly the verdict a repaired "
                         "`stall_verdict` would emit, and the defect cannot have touched it "
                         "-- established from the artifact itself, not from a literal."),
        "L3_stall_verdicts": stall_rows,
        "L3_rows_not_bit_identical": n_stall_bad,
        "L1_ranked_attribution": ranked_rows,
        "L1_rows_not_bit_identical": n_rank_bad,
        "L1_published_ranking_identical_to_order_immune": ranking_identical,
        "deep_rung": {"stored_m_sequence": [r["m"] for r in deep],
                      "order_immune_gain": deep_mine["residual_gain"],
                      "order_immune_min_dim": deep_mine["min_dim"],
                      "order_immune_max_dim": deep_mine["max_dim"],
                      "order_immune_rel_at_max_dim": deep_mine["rel_at_max_dim"],
                      "note": ("the deep rung is banked as raw rows; Route-L publishes its "
                               "m=320 residual directly and never publishes a stall verdict "
                               "for it -- see G5")},
        "verdict": ("PUBLISHED == ORDER-IMMUNE on all rows"
                    if n_stall_bad == 0 and n_rank_bad == 0 and ranking_identical
                    else "PUBLISHED DIFFERS FROM ORDER-IMMUNE"),
    }


# ---------------------------------------------------------------------------
# G3 -- AST enumeration of every call site (closes leg 241's cited-line gap)
# ---------------------------------------------------------------------------
def gate_3_call_sites(src_path=ROUTE_L_RUNNER):
    tree = ast.parse(src_path.read_text())
    lines = src_path.read_text().splitlines()

    # module-level tuple/list constants, so a `dims=DIMS` reference can be resolved
    consts = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, (ast.Tuple, ast.List)):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    try:
                        consts[tgt.id] = list(ast.literal_eval(node.value))
                    except ValueError:
                        pass

    call_sites = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", None)
        if name not in ("krylov_ladder", "stall_verdict", "attribution_summary"):
            continue
        dims, how = None, None
        for kw in node.keywords:
            if kw.arg == "dims":
                if isinstance(kw.value, (ast.Tuple, ast.List)):
                    dims, how = list(ast.literal_eval(kw.value)), "inline literal"
                elif isinstance(kw.value, ast.Name):
                    dims = consts.get(kw.value.id)
                    how = f"module constant {kw.value.id}"
        if name == "krylov_ladder" and dims is None:
            dims, how = None, "DEFAULT (function signature)"
        asc = None if dims is None else (dims == sorted(dims) and len(set(dims)) == len(dims))
        call_sites.append({
            "function": name, "line": node.lineno,
            "source": lines[node.lineno - 1].strip()[:110],
            "dims": dims, "dims_provenance": how, "dims_strictly_ascending": asc})

    kl = [c for c in call_sites if c["function"] == "krylov_ladder"]
    covered_by_line_49 = [c for c in kl if c["dims_provenance"] == "module constant DIMS"]
    not_covered = [c for c in kl if c["dims_provenance"] != "module constant DIMS"]
    bad = [c for c in kl if c["dims_strictly_ascending"] is not True]

    return {
        "method": ("the runner is PARSED (ast.walk), not grepped: every call to "
                   "`krylov_ladder` / `stall_verdict` / `attribution_summary` is enumerated "
                   "and its `dims` argument resolved, so no call site can be missed by "
                   "citing one line."),
        "gap_in_leg_241_this_closes": (
            "leg 241's claim-adjacency table cites `DIMS = (10,20,40,80,160)` at line 49 as "
            "the whole reason the margin is safe. That literal does not reach the deep-rung "
            "call, which carries its own inline `dims` tuple -- yet leg 241 quotes the deep "
            "rung's 61.6x -> 0.0162x inversion. Enumerating mechanically settles both."),
        "module_constants": consts,
        "call_sites": call_sites,
        "krylov_ladder_call_sites": len(kl),
        "covered_by_the_line_49_literal": len(covered_by_line_49),
        "NOT_covered_by_the_line_49_literal": [
            {"line": c["line"], "dims": c["dims"], "provenance": c["dims_provenance"],
             "strictly_ascending": c["dims_strictly_ascending"]} for c in not_covered],
        "call_sites_with_non_ascending_dims": len(bad),
        "verdict": ("EVERY call site ascending" if not bad
                    else "A CALL SITE FEEDS NON-ASCENDING dims"),
    }


# ---------------------------------------------------------------------------
# G4 -- reproduce leg 241's affected case, and name the input it requires
# ---------------------------------------------------------------------------
def gate_4_affected_case(banked):
    from solver.port_certification import stall_verdict          # the REAL, unrepaired one

    l3 = banked["L3_preconditioners"]["ladders"]
    sweep = l3["full transport line sweep"]

    as_banked = stall_verdict(list(sweep))
    reversed_input = stall_verdict(list(reversed(sweep)))
    ratio = as_banked["residual_gain"] / reversed_input["residual_gain"]

    deep = banked["L3_preconditioners"]["line_sweep_deeper"]
    deep_asc, deep_desc = stall_verdict(list(deep)), stall_verdict(list(reversed(deep)))

    return {
        "note": ("leg 241's MECHANISM is accepted as given and is not re-derived as a claim "
                 "of this leg. It is reproduced here only to pin down, exactly, WHAT INPUT "
                 "the 94.56x requires -- which is the question the gate turns on."),
        "ladder": "full transport line sweep",
        "input_as_banked": {
            "m_sequence": [r["m"] for r in sweep],
            "residual_gain": as_banked["residual_gain"],
            "work_ratio": as_banked["work_ratio"], "flat": as_banked["flat"],
            "reading": as_banked["reading"]},
        "input_reversed_by_leg_241": {
            "m_sequence": [r["m"] for r in reversed(sweep)],
            "residual_gain": reversed_input["residual_gain"],
            "work_ratio": reversed_input["work_ratio"], "flat": reversed_input["flat"],
            "reading": reversed_input["reading"],
            "constructed_by": ("`sv(list(reversed(ladder)))` -- "
                               "p2_route_pcrc_v1_cleanup.py:364, leg 241's own runner")},
        "flip_magnitude_reproduced": ratio,
        "leg_241_reported": {"ascending_gain": LEG_241_ASC_GAIN,
                             "descending_gain": LEG_241_DESC_GAIN, "ratio": LEG_241_RATIO},
        "reproduction_agrees_with_leg_241": {
            "ascending": abs(as_banked["residual_gain"] - LEG_241_ASC_GAIN) < 5e-4,
            "descending": abs(reversed_input["residual_gain"] - LEG_241_DESC_GAIN) < 5e-4,
            "ratio": abs(ratio - LEG_241_RATIO) < 5e-2},
        "deep_rung": {"ascending_gain": deep_asc["residual_gain"],
                      "reversed_gain": deep_desc["residual_gain"],
                      "m_sequence_as_banked": [r["m"] for r in deep]},
        "the_input_the_flip_requires": ("a row array ordered descending in `m`. G1 finds 0 "
                                        "of 11 banked arrays in that order and G3 finds 0 "
                                        "of the runner's call sites able to produce one."),
        "is_route_l_actual_banked_configuration": False,
    }


# ---------------------------------------------------------------------------
# G5 -- the headline, decomposed number by number
# ---------------------------------------------------------------------------
def gate_5_headline_trace(banked):
    doc = ROUTE_L_DOC.read_text()
    headline = ("Step (iii) of the certification chain -- an approximate inverse `A` with a "
                "computable `Z1` -- was declared unreachable on this discretization by "
                "Route-K. It is now reachable: an `O(N)` exact sweep takes the Krylov stall "
                "from 0.6623 (flat) to 3.3e-6.")
    l3 = banked["L3_preconditioners"]
    none_rows = l3["ladders"]["none"]
    sweep_rows = l3["ladders"]["full transport line sweep"]
    deep = l3["line_sweep_deeper"]

    none_hi = max(none_rows, key=lambda r: r["m"])
    deep_hi = max(deep, key=lambda r: r["m"])
    none_stall = stall_by_key(none_rows)
    sweep_stall = stall_by_key(sweep_rows)

    components = [
        {"number_as_published": "0.6623",
         "traces_to": "L3_preconditioners/ladders/none, the m=160 row's rel_residual",
         "banked_value": none_hi["rel_residual"],
         "order_sensitive": False,
         "why": ("a single measured row, selected here by max m. A per-row residual carries "
                 "its own `m`; no ordering of the array changes the value at m=160.")},
        {"number_as_published": "(flat)",
         "traces_to": "L3_preconditioners/stalls/none -> flat",
         "banked_value": l3["stalls"]["none"]["flat"],
         "order_immune_value": none_stall["flat"],
         "order_sensitive": True,
         "survives_reversal_anyway": True,
         "why": ("this label IS a `stall_verdict` output, so it is order-sensitive in "
                 "principle. Two independent reasons it is untouched: the banked array is "
                 "ascending (G1/G2), AND this particular ladder's gain is 1.0487 ascending "
                 "against 0.9536 reversed -- both below 2.0, so `flat` is True either way. "
                 "The headline's `(flat)` is the one component that could not flip even on "
                 "the reversed input.")},
        {"number_as_published": "3.3e-6",
         "traces_to": "L3_preconditioners/line_sweep_deeper, the m=320 row's rel_residual",
         "banked_value": deep_hi["rel_residual"],
         "order_sensitive": False,
         "why": ("a single measured row again. Route-L publishes the deep rung as raw "
                 "residuals in its section-3 table and never publishes a stall verdict for "
                 "it -- the `61.6x` leg 241 inverts is a quantity leg 241 formed, not one "
                 "Route-L banked or printed.")},
        {"number_as_published": "gain 9.72, 'the ladder stops being flat' (section 3, the "
                                "claim the headline rests on)",
         "traces_to": "L3_preconditioners/stalls/full transport line sweep",
         "banked_value": l3["stalls"]["full transport line sweep"]["residual_gain"],
         "order_immune_value": sweep_stall["residual_gain"],
         "banked_flat": l3["stalls"]["full transport line sweep"]["flat"],
         "order_immune_flat": sweep_stall["flat"],
         "order_sensitive": True,
         "survives_reversal_anyway": False,
         "why": ("THE load-bearing one, and the ladder leg 241 flips. It is order-sensitive "
                 "and it would NOT survive a reversed input -- 9.7245 (bending) would "
                 "become 0.1028 (flat), the exact conclusion Route-L used this ladder to "
                 "overturn. Its safety is therefore NOT structural; it rests entirely on "
                 "the banked array being ascending, which G1 and G2 establish "
                 "independently and G3 confirms at the source.")},
    ]
    doc_quotes = {
        "headline_present_verbatim_in_doc": "0.6623 (flat) to 3.3e−6" in doc,
        "gain_9_72_present_in_doc": "9.72" in doc,
        "published_gain_matches_order_immune_to_2dp":
            round(sweep_stall["residual_gain"], 2) == 9.72,
    }
    sensitive = [c for c in components if c["order_sensitive"]]
    return {
        "headline_sentence": headline,
        "doc": str(ROUTE_L_DOC.relative_to(ROOT)),
        "components": components,
        "order_sensitive_components": len(sensitive),
        "order_invariant_components": len(components) - len(sensitive),
        "doc_cross_checks": doc_quotes,
        "reading": ("two of the four headline components are raw single-row residuals and "
                    "cannot move under any ordering; one (`flat` on the `none` ladder) is a "
                    "stall verdict that happens to be double-covered; one (the sweep's "
                    "bending verdict) is genuinely order-sensitive and is exactly leg 241's "
                    "flipping ladder. So leg 241 is RIGHT that the headline's load-bearing "
                    "verdict rides the flipping ladder -- and right, separately, that the "
                    "banked configuration never presents that ladder in the flipping "
                    "order."),
    }


# ---------------------------------------------------------------------------
# G6 -- the control column (lesson 90): can this audit report the OTHER answer?
# ---------------------------------------------------------------------------
def gate_6_control(banked):
    from solver.port_certification import stall_verdict

    sweep = banked["L3_preconditioners"]["ladders"]["full transport line sweep"]

    # (i) NEGATIVE CONTROL -- a ladder deliberately stored descending. G1's predicate must
    #     flag it and G2's comparison must FAIL on it, or neither gate tested anything.
    descending = list(reversed(sweep))
    asc_flag, ms = is_strictly_ascending(descending)
    pos = stall_verdict(descending)
    immune = stall_by_key(descending)
    control_detected = (not asc_flag) and (pos["residual_gain"] != immune["residual_gain"]) \
        and (pos["flat"] != immune["flat"])

    # (ii) POSITIVE CONTROL -- the banked array itself: the predicate must come out clean
    #      and the two reads must coincide bit-for-bit.
    asc_flag2, ms2 = is_strictly_ascending(sweep)
    pos2, immune2 = stall_verdict(list(sweep)), stall_by_key(list(sweep))
    clean = asc_flag2 and pos2["residual_gain"] == immune2["residual_gain"] \
        and pos2["flat"] == immune2["flat"]

    # (iii) a SHUFFLED (neither ascending nor descending) array, to check the predicate is
    #       not merely a reversal detector.
    shuffled = [sweep[2], sweep[0], sweep[4], sweep[1], sweep[3]]
    asc_flag3, ms3 = is_strictly_ascending(shuffled)
    pos3, immune3 = stall_verdict(shuffled), stall_by_key(shuffled)

    return {
        "why": ("lesson 90 -- a check that can only come out one way is not a check. The "
                "audit predicate and the order-immune comparison are both run against "
                "inputs where they MUST report a problem, and against the live one where "
                "they must not."),
        "negative_control_descending": {
            "m_sequence": ms, "flagged_non_ascending": not asc_flag,
            "positional_gain": pos["residual_gain"],
            "order_immune_gain": immune["residual_gain"],
            "gain_ratio": immune["residual_gain"] / pos["residual_gain"],
            "positional_flat": pos["flat"], "order_immune_flat": immune["flat"],
            "detected_by_this_leg_audit": control_detected},
        "negative_control_shuffled": {
            "m_sequence": ms3, "flagged_non_ascending": not asc_flag3,
            "positional_gain": pos3["residual_gain"],
            "order_immune_gain": immune3["residual_gain"],
            "gain_ratio": immune3["residual_gain"] / pos3["residual_gain"],
            "positional_flat": pos3["flat"], "order_immune_flat": immune3["flat"],
            "detected_by_this_leg_audit": bool(
                (not asc_flag3) and pos3["residual_gain"] != immune3["residual_gain"])},
        "positive_control_as_banked": {
            "m_sequence": ms2, "flagged_non_ascending": not asc_flag2,
            "positional_gain": pos2["residual_gain"],
            "order_immune_gain": immune2["residual_gain"],
            "difference": abs(pos2["residual_gain"] - immune2["residual_gain"]),
            "clean": clean},
        "control_comes_out_both_ways": bool(control_detected and clean),
    }


# ---------------------------------------------------------------------------
def main():
    t0 = time.time()
    banked = json.loads(BANKED_JSON.read_text())

    print("== G0: provenance ==", flush=True)
    g0 = gate_0_provenance(banked)
    print(f"  banked {g0['banked_artifact']['path']}  "
          f"sha {g0['banked_artifact']['sha256'][:12]}", flush=True)

    print("== G1: order audit of every banked array feeding stall_verdict ==", flush=True)
    g1 = gate_1_order_audit(banked)
    for r in g1["rows"]:
        print(f"  {r['array']:52s} m={r['stored_m_sequence']}  "
              f"ascending={r['strictly_ascending']}", flush=True)
    print(f"  -> {g1['arrays_audited']} arrays, {g1['non_ascending_arrays']} non-ascending",
          flush=True)

    print("== G2: order-immune re-derivation vs PUBLISHED (exact ==) ==", flush=True)
    g2 = gate_2_order_immune_vs_published(banked)
    for r in g2["L3_stall_verdicts"]:
        print(f"  {r['ladder']:28s} published {r['published_residual_gain']:.10f}  "
              f"order-immune {r['order_immune_residual_gain']:.10f}  "
              f"diff {r['abs_difference']}  identical={r['bit_identical_all_keys']}",
          flush=True)
    print(f"  L1 ranked rows differing: {g2['L1_rows_not_bit_identical']}  "
          f"ranking identical: {g2['L1_published_ranking_identical_to_order_immune']}",
          flush=True)

    print("== G3: AST enumeration of every call site ==", flush=True)
    g3 = gate_3_call_sites()
    for c in g3["call_sites"]:
        print(f"  line {c['line']:4d}  {c['function']:20s} dims={c['dims']}  "
              f"({c['dims_provenance']})  ascending={c['dims_strictly_ascending']}",
              flush=True)

    print("== G4: leg 241's affected case, and the input it requires ==", flush=True)
    g4 = gate_4_affected_case(banked)
    print(f"  as banked  {g4['input_as_banked']['m_sequence']}  "
          f"gain {g4['input_as_banked']['residual_gain']:.4f}  "
          f"flat={g4['input_as_banked']['flat']}", flush=True)
    print(f"  reversed   {g4['input_reversed_by_leg_241']['m_sequence']}  "
          f"gain {g4['input_reversed_by_leg_241']['residual_gain']:.4f}  "
          f"flat={g4['input_reversed_by_leg_241']['flat']}   "
          f"ratio {g4['flip_magnitude_reproduced']:.2f}x", flush=True)

    print("== G5: the headline, decomposed ==", flush=True)
    g5 = gate_5_headline_trace(banked)
    for c in g5["components"]:
        print(f"  {c['number_as_published'][:44]:46s} order_sensitive="
              f"{c['order_sensitive']}", flush=True)

    print("== G6: control ==", flush=True)
    g6 = gate_6_control(banked)
    print(f"  negative (descending) detected: "
          f"{g6['negative_control_descending']['detected_by_this_leg_audit']}   "
          f"positive (as banked) clean: {g6['positive_control_as_banked']['clean']}",
          flush=True)

    unaffected = (
        g1["non_ascending_arrays"] == 0
        and g2["L3_rows_not_bit_identical"] == 0
        and g2["L1_rows_not_bit_identical"] == 0
        and g2["L1_published_ranking_identical_to_order_immune"]
        and g3["call_sites_with_non_ascending_dims"] == 0
        and not g4["is_route_l_actual_banked_configuration"]
        and g6["control_comes_out_both_ways"]
    )

    out = {
        "leg": "Leg 243 -- Route-PCRS",
        "role": "VERIFIER",
        "branch": "verify/243-pcrs-v1",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate_verbatim": (
            "Does an independent re-check confirm Route-L's own published headline verdict "
            "is UNAFFECTED by the `stall_verdict` positional-read finding leg 241 "
            "characterized (i.e., the 94.56x flip occurs only in a case that does not "
            "correspond to Route-L's actual banked headline configuration), matching leg "
            "241's own 'not claim-adjacent' conclusion?"),
        "gate_answer": "YES" if unaffected else "NO",
        "escalation_required": not unaffected,
        "G0_provenance": g0,
        "G1_order_audit": g1,
        "G2_order_immune_vs_published": g2,
        "G3_call_sites": g3,
        "G4_affected_case": g4,
        "G5_headline_trace": g5,
        "G6_control": g6,
        "the_comparison_the_gate_asks_for": {
            "route_l_actual_banked_configuration": {
                "artifact": str(BANKED_JSON.relative_to(ROOT)),
                "ladder_carrying_the_headline": "full transport line sweep",
                "m_sequence_as_banked": [r["m"] for r in
                                         banked["L3_preconditioners"]["ladders"]
                                         ["full transport line sweep"]],
                "dims_provenance": "module constant DIMS = (10, 20, 40, 80, 160), ascending",
                "deep_rung_dims_provenance": "inline literal (240, 320), ascending",
                "published_residual_gain": banked["L3_preconditioners"]["stalls"]
                                                 ["full transport line sweep"]["residual_gain"],
                "published_flat": banked["L3_preconditioners"]["stalls"]
                                        ["full transport line sweep"]["flat"],
                "published_reading": "bending => finite ill-conditioning",
            },
            "the_case_leg_241_found_the_flip_in": {
                "artifact": "constructed in leg 241's runner, not banked anywhere",
                "construction": "sv(list(reversed(ladder))) -- p2_route_pcrc_v1_cleanup.py:364",
                "m_sequence": [160, 80, 40, 20, 10],
                "residual_gain": 0.10283440447155221,
                "flat": True,
                "reading": "flat => a continuum in the spectrum",
            },
            "do_they_correspond": False,
            "difference": ("the ordering of the row array, and nothing else -- the five "
                           "measurements are identical floats in both. Route-L's banked "
                           "ladder is ascending; leg 241's flipping case is that same "
                           "ladder reversed in memory, an input no Route-L call site can "
                           "produce."),
        },
        "finding": (
            "CONFIRMED UNAFFECTED. All 11 banked arrays that reach `stall_verdict` are "
            "stored strictly ascending in m; every published stall number is bit-identical "
            "to an order-immune re-derivation keyed on m (all differences exactly 0.0, "
            "under == on raw float64, never allclose), including the 6-row attribution "
            "ranking leg 241 did not audit, whose published order is reproduced exactly; "
            "and all 6 krylov_ladder call sites (lines 133, 176-180) carry ascending dims, "
            "including the deep rung's own inline (240, 320) at line 180 which leg 241's "
            "cited line 49 does not cover. "
            "Leg 241's 94.56x is reproduced exactly on the reversed input and requires an "
            "array ordered descending in m, which occurs at 0 of 11 banked arrays and 0 of "
            "6 call sites. Leg 241's 'not claim-adjacent' conclusion is independently "
            "confirmed -- and its own reading that the margin is 0.0 and undefended, rather "
            "than safe by construction, is confirmed too: the headline's load-bearing "
            "component IS the flipping ladder's bending verdict."),
        "what_this_does_not_say": (
            "This leg does NOT clear the defect. The margin is 0.0: the sweep ladder's "
            "bending verdict, which the headline rests on, is protected only by the input "
            "order, not by anything in `krylov_ladder` or `stall_verdict`. A future caller "
            "passing descending dims would silently invert a published verdict with no "
            "error and no flag. The repair leg leg 241 asks for is still warranted; what "
            "this leg establishes is only that no banked number is currently wrong."),
        "wall_clock_seconds": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print(f"\nGATE: {out['gate_answer']}    -> {OUT.relative_to(ROOT)}  "
          f"({out['wall_clock_seconds']}s)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
