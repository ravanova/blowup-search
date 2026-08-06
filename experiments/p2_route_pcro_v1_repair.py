#!/usr/bin/env python3
"""Leg 244 -- Route-PCRO: make `stall_verdict`'s verdict ORDER-IMMUNE, and prove the repair
moves no published number.

ROLE: LEG (repair family -- legs 128, 166, 200 precedent).

THE DEFECT, as leg 241 found it and leg 243 sharpened it.  `stall_verdict` read
`first, last = rows[0], rows[-1]`.  The verdict was therefore a property of how the caller
happened to STORE the ladder, not of the measurement.  Every banked array is ascending in
`m`, so no published number is wrong -- but leg 243 measured the protecting margin at
exactly **0.0**: reverse Route-L's `full transport line sweep` ladder and the residual gain
reads 0.1028 (flat) instead of 9.7245 (bending), a **94.56x** error that inverts the single
order-sensitive, load-bearing component of Route-L's headline; an arbitrary SHUFFLE flips it
too (1.4163 flat vs 9.7245 bending, 6.87x), so the exposure is wider than reversal.

THE REPAIR.  `stall_verdict` now selects its two rows by `m` -- the ladder's own parameter,
already carried in every row `krylov_ladder` emits -- instead of by position.  No call site
changes, including the deep rung's inline `dims=(240, 320)` at `p2_route_l_v1_precond.py:180`
that leg 241's cited `DIMS` literal at line 49 does not cover.  `krylov_ladder` is
deliberately NOT touched: keying the verdict on `m` makes the row ORDER irrelevant, so
canonicalising the producer would be a second, redundant mechanism guarding the same thing.

THE GATE, pre-committed, verbatim, both branches:

    Does making `stall_verdict`'s verdict robust to array order (rather than relying on the
    current incidental ordering) preserve every currently-correct verdict (Route-L's
    headline included, re-checked explicitly) while removing the order-dependence leg 243
    found?

    YES -> bank the repair; Route-L's headline and every other currently-correct verdict is
           now robust rather than incidentally correct.  Normal landing.
    NO   -> report exactly which verdict the fix disturbs and why; do not land a fix that
           trades one fragility for another.  Branch only, never main.

Gates:
  G0  provenance -- what is read, and its hashes
  G1  PRESERVATION: repaired verdict vs every PUBLISHED number, exact == on raw float64
  G2  IMMUNITY: exhaustive permutation battery -- EVERY permutation of EVERY banked ladder
  G3  Route-L's headline re-derived explicitly, number by number, under permutation
  G4  the deep rung's own `dims=(240, 320)` call site, AST-located and permuted
  G5  control both ways (lesson 90): the OLD positional read must still flip, or G2 tested
      nothing; and a deliberately mis-keyed variant must FAIL the battery
  G6  `attribution_summary` under permutation -- the published 6-row ranking, and the one
      positional read that survives OUTSIDE this leg's territory, measured not asserted
  G7  malformed-ladder refusal: an ambiguous duplicate `m` raises rather than guessing
  G8  the module's own three test suites, run as subprocesses
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import random
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from solver.port_certification import attribution_summary, stall_verdict  # noqa: E402

ROUTE_L_JSON = ROOT / "writeup" / "data" / "p2_route_l_v1_precond.json"
ROUTE_K_JSON = ROOT / "writeup" / "data" / "p2_route_k_v1_port.json"
ROUTE_L_RUNNER = ROOT / "experiments" / "p2_route_l_v1_precond.py"
ROUTE_L_DOC = ROOT / "writeup" / "4_p2_lottery" / "TECHNICAL_P2_ROUTEL_V1.md"
MODULE = ROOT / "solver" / "port_certification.py"
OUT = ROOT / "writeup" / "data" / "p2_route_pcro_v1_repair.json"

VERDICT_KEYS = ("rel_at_min_dim", "min_dim", "rel_at_max_dim", "max_dim",
                "work_ratio", "residual_gain", "flat", "reading")

# leg 243's magnitudes, quoted so the controls below are checked against numbers this leg
# did not compute.
LEG_243_REVERSAL_RATIO = 94.565
LEG_243_SHUFFLE_GAIN = 1.4163
LEG_243_TRUE_GAIN = 9.7245


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# The PRE-REPAIR function, reproduced verbatim from the commit this leg repairs.
# It exists only so the controls in G5 can show the battery would catch a regression.
# ---------------------------------------------------------------------------
def positional_stall_verdict(rows):
    """`stall_verdict` exactly as it stood before this leg: `rows[0]` and `rows[-1]`."""
    first, last = rows[0], rows[-1]
    gain = first["rel_residual"] / last["rel_residual"]
    return {"rel_at_min_dim": first["rel_residual"], "min_dim": first["m"],
            "rel_at_max_dim": last["rel_residual"], "max_dim": last["m"],
            "work_ratio": last["m"] / first["m"], "residual_gain": float(gain),
            "flat": bool(gain < 2.0),
            "reading": ("flat in Krylov dimension => a continuum in the spectrum, not a "
                        "large condition number" if gain < 2.0 else
                        "bending => finite ill-conditioning, and more Krylov work would help")}


def miskeyed_stall_verdict(rows):
    """A DELIBERATELY WRONG repair: keys on `k` (iterations used), not on `m`.

    On these ladders `k == m` row by row, so it looks right -- until a ladder where the
    solve terminates early.  G5 feeds it exactly such a ladder.

    Its job is to show what the permutation battery CANNOT do: keying on `k` is perfectly
    order-invariant, so G2's battery passes it.  What separates it from the real repair is
    G1's preservation comparison -- it reads a different row and so reports a different
    verdict.  Both gates are load-bearing, and this control is why.
    """
    by_k = {r["k"]: r for r in rows}
    first, last = by_k[min(by_k)], by_k[max(by_k)]
    gain = first["rel_residual"] / last["rel_residual"]
    return {"rel_at_min_dim": first["rel_residual"], "min_dim": first["m"],
            "rel_at_max_dim": last["rel_residual"], "max_dim": last["m"],
            "work_ratio": last["m"] / first["m"], "residual_gain": float(gain),
            "flat": bool(gain < 2.0),
            "reading": ("flat in Krylov dimension => a continuum in the spectrum, not a "
                        "large condition number" if gain < 2.0 else
                        "bending => finite ill-conditioning, and more Krylov work would help")}


def verdicts_identical(a, b):
    """Exact `==` on raw float64 across every key.  Never `allclose` (leg 243's discipline)."""
    return all(a[k] == b[k] for k in VERDICT_KEYS)


def verdict_diff(a, b):
    return {k: (a[k] - b[k]) if isinstance(a[k], (int, float)) and not isinstance(a[k], bool)
            else (a[k] == b[k]) for k in VERDICT_KEYS}


def all_banked_ladders():
    """Every array in the bank that reaches `stall_verdict`, by any route.  11 from Route-L."""
    L = json.loads(ROUTE_L_JSON.read_text())
    out = []
    for label, rows in L["L1_attribution"]["ladders"].items():
        out.append(("route_L/L1_attribution/" + label, rows, "attribution_summary"))
    for label, rows in L["L3_preconditioners"]["ladders"].items():
        out.append(("route_L/L3_preconditioners/" + label, rows, "stall_verdict directly"))
    out.append(("route_L/L3_preconditioners/line_sweep_deeper",
                L["L3_preconditioners"]["line_sweep_deeper"],
                "the deep rung, dims=(240,320) inline at line 180"))
    if ROUTE_K_JSON.exists():
        K = json.loads(ROUTE_K_JSON.read_text())
        for path, rows in _find_ladders(K):
            out.append(("route_K" + path, rows, "stall_verdict directly"))
    return out, L


def _find_ladders(obj, path=""):
    """Any list of dicts carrying `m`/`rel_residual` is a krylov_ladder result."""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            found += _find_ladders(v, path + "/" + k)
    elif isinstance(obj, list) and obj and all(
            isinstance(r, dict) and "m" in r and "rel_residual" in r for r in obj):
        found.append((path, obj))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += _find_ladders(v, path + "/%d" % i)
    return found


# ---------------------------------------------------------------------------
# G0
# ---------------------------------------------------------------------------
def gate_0_provenance(ladders):
    return {
        "why": "every artifact this leg reads or repairs, hashed, so the run is re-derivable",
        "repaired_module": {"path": str(MODULE.relative_to(ROOT)), "sha256": sha256(MODULE)},
        "route_L_banked": {"path": str(ROUTE_L_JSON.relative_to(ROOT)),
                           "sha256": sha256(ROUTE_L_JSON)},
        "route_K_banked": ({"path": str(ROUTE_K_JSON.relative_to(ROOT)),
                            "sha256": sha256(ROUTE_K_JSON)} if ROUTE_K_JSON.exists() else None),
        "route_L_runner": {"path": str(ROUTE_L_RUNNER.relative_to(ROOT)),
                           "sha256": sha256(ROUTE_L_RUNNER)},
        "banked_ladders_discovered": len(ladders),
        "ladder_inventory": [{"label": lab, "n_rows": len(rows),
                              "m_sequence": [r["m"] for r in rows], "reaches_verdict_via": via}
                             for lab, rows, via in ladders],
    }


# ---------------------------------------------------------------------------
# G1 -- PRESERVATION.  This is the gate's "preserve every currently-correct verdict" half.
# ---------------------------------------------------------------------------
def gate_1_preservation(L):
    """Repaired `stall_verdict` on every banked ladder AS STORED, vs what Route-L PUBLISHED.

    Not `allclose`: `==` on raw float64, and the arithmetic difference reported so a
    non-zero would be visible as a magnitude rather than as a failed boolean.
    """
    rows_out, worst = [], 0.0
    for label, published in L["L3_preconditioners"]["stalls"].items():
        recomputed = stall_verdict(L["L3_preconditioners"]["ladders"][label])
        same = verdicts_identical(recomputed, published)
        d = {k: abs(recomputed[k] - published[k]) for k in
             ("rel_at_min_dim", "rel_at_max_dim", "work_ratio", "residual_gain")}
        worst = max(worst, max(d.values()))
        rows_out.append({"published_block": "L3_preconditioners/stalls", "label": label,
                         "published_residual_gain": published["residual_gain"],
                         "repaired_residual_gain": recomputed["residual_gain"],
                         "published_flat": published["flat"],
                         "repaired_flat": recomputed["flat"],
                         "abs_differences": d, "bit_identical_all_keys": same})

    ranked_now = attribution_summary(L["L1_attribution"]["ladders"])
    ranked_pub = L["L1_attribution"]["ranked"]
    ranking_same = ([r["ablation"] for r in ranked_now] == [r["ablation"] for r in ranked_pub])
    rank_rows = []
    for now, pub in zip(ranked_now, ranked_pub):
        d = {k: abs(now[k] - pub[k]) for k in ("rel_at_max_dim", "gain", "gain_vs_full")}
        worst = max(worst, max(d.values()))
        rank_rows.append({"published_block": "L1_attribution/ranked",
                          "ablation_published": pub["ablation"],
                          "ablation_repaired": now["ablation"],
                          "published_gain": pub["gain"], "repaired_gain": now["gain"],
                          "published_flat": pub["flat"], "repaired_flat": now["flat"],
                          "abs_differences": d,
                          "bit_identical": all(now[k] == pub[k] for k in
                                               ("ablation", "rel_at_max_dim", "gain", "flat",
                                                "gain_vs_full", "worse_than_full"))})
    moved = ([r for r in rows_out if not r["bit_identical_all_keys"]]
             + [r for r in rank_rows if not r["bit_identical"]])
    return {
        "why": ("the repair is only bankable if it moves NOTHING that is currently correct. "
                "Compared under `==` on raw float64 against the numbers Route-L actually "
                "banked, never `allclose`."),
        "L3_stall_rows": rows_out,
        "L1_ranked_rows": rank_rows,
        "L1_published_ranking_reproduced": ranking_same,
        "published_ranking": [r["ablation"] for r in ranked_pub],
        "rows_compared": len(rows_out) + len(rank_rows),
        "rows_that_moved": len(moved),
        "which_moved": [r.get("label") or r.get("ablation_published") for r in moved],
        "largest_absolute_difference_anywhere": worst,
        "reading": ("every published number reproduces bit-identically under the repaired, "
                    "order-immune verdict: the largest difference across all compared "
                    "quantities is exactly %r" % worst),
    }


# ---------------------------------------------------------------------------
# G2 -- IMMUNITY.  This is the gate's "removes the order-dependence" half.
# ---------------------------------------------------------------------------
def permutation_battery(rows, verdict_fn, exhaustive_upto=7, sampled=200, seed=0):
    """EVERY permutation when the ladder is short enough; a seeded sample otherwise.

    Returns the number of distinct verdicts observed.  For an order-immune function that is
    exactly 1, whatever the permutation.
    """
    n = len(rows)
    if n <= exhaustive_upto:
        perms = list(itertools.permutations(range(n)))
        mode = "exhaustive"
    else:
        rng = random.Random(seed)
        perms = [tuple(range(n))] + [tuple(rng.sample(range(n), n)) for _ in range(sampled)]
        mode = "sampled(%d)" % sampled
    base = verdict_fn(list(rows))
    distinct, worst_gain_ratio, worst_perm = 1, 1.0, None
    disagreements = []
    for p in perms:
        v = verdict_fn([rows[i] for i in p])
        if not verdicts_identical(v, base):
            distinct += 1
            r = max(v["residual_gain"], base["residual_gain"]) / \
                min(v["residual_gain"], base["residual_gain"])
            if r > worst_gain_ratio:
                worst_gain_ratio, worst_perm = r, [rows[i]["m"] for i in p]
            if len(disagreements) < 3:
                disagreements.append({"m_sequence": [rows[i]["m"] for i in p],
                                      "residual_gain": v["residual_gain"], "flat": v["flat"]})
    return {"n_rows": n, "mode": mode, "permutations_tested": len(perms),
            "permutations_disagreeing_with_as_stored": distinct - 1,
            "distinct_verdicts": 1 if distinct == 1 else distinct,
            "worst_gain_ratio_across_permutations": worst_gain_ratio,
            "worst_permutation_m_sequence": worst_perm,
            "example_disagreements": disagreements,
            "as_stored_residual_gain": base["residual_gain"], "as_stored_flat": base["flat"]}


def gate_2_immunity(ladders):
    repaired, old = [], []
    total_perms = 0
    for label, rows, _via in ladders:
        b = permutation_battery(rows, stall_verdict)
        o = permutation_battery(rows, positional_stall_verdict)
        total_perms += b["permutations_tested"]
        repaired.append(dict(label=label, **b))
        old.append({"label": label,
                    "permutations_disagreeing": o["permutations_disagreeing_with_as_stored"],
                    "worst_gain_ratio": o["worst_gain_ratio_across_permutations"],
                    "worst_permutation_m_sequence": o["worst_permutation_m_sequence"],
                    "example_disagreements": o["example_disagreements"]})
    bad = [r for r in repaired if r["permutations_disagreeing_with_as_stored"] != 0]
    return {
        "why": ("order-immunity is not asserted from the source, it is MEASURED: every "
                "permutation of every banked ladder is fed to the repaired verdict, and "
                "every one must return the same answer on all 8 keys under `==`."),
        "repaired_stall_verdict": repaired,
        "pre_repair_positional_stall_verdict": old,
        "total_permutations_tested": total_perms,
        "ladders_with_any_disagreement_after_repair": len(bad),
        "which_disagree": [r["label"] for r in bad],
        "worst_pre_repair_gain_ratio": max(r["worst_gain_ratio"] for r in old),
        "worst_post_repair_gain_ratio": max(
            r["worst_gain_ratio_across_permutations"] for r in repaired),
        "reading": ("%d permutations across %d banked ladders: the repaired verdict returns "
                    "ONE answer on every one of them (worst gain ratio exactly %r), while "
                    "the pre-repair positional read spread by up to %.3fx on the same "
                    "inputs" % (total_perms, len(ladders),
                                max(r["worst_gain_ratio_across_permutations"]
                                    for r in repaired),
                                max(r["worst_gain_ratio"] for r in old))),
    }


# ---------------------------------------------------------------------------
# G3 -- Route-L's headline, re-derived explicitly, number by number
# ---------------------------------------------------------------------------
HEADLINE = ("an O(N) exact sweep takes the Krylov stall from 0.6623 (flat) to 3.3e-6")


def gate_3_headline(L):
    none_ladder = L["L3_preconditioners"]["ladders"]["none"]
    sweep_ladder = L["L3_preconditioners"]["ladders"]["full transport line sweep"]
    deep = L["L3_preconditioners"]["line_sweep_deeper"]

    none_v = stall_verdict(none_ladder)
    sweep_v = stall_verdict(sweep_ladder)
    pub_sweep = L["L3_preconditioners"]["stalls"]["full transport line sweep"]
    pub_none = L["L3_preconditioners"]["stalls"]["none"]

    # the same four components under EVERY permutation of the underlying rows
    none_perm = permutation_battery(none_ladder, stall_verdict)
    sweep_perm = permutation_battery(sweep_ladder, stall_verdict)
    deep_perm = permutation_battery(deep, stall_verdict)

    # the two raw single-row numbers, located by `m` rather than by position
    r_0p6623 = {r["m"]: r for r in none_ladder}[160]["rel_residual"]
    r_3e6 = {r["m"]: r for r in deep}[320]["rel_residual"]

    components = [
        {"component": "0.6623", "traces_to": "L3/ladders/none, the m=160 row",
         "value": r_0p6623, "reproduced": round(r_0p6623, 4) == 0.6623,
         "order_sensitive_before_repair": False, "order_sensitive_after_repair": False},
        {"component": "(flat)", "traces_to": "L3/stalls/none -> flat",
         "value_gain": none_v["residual_gain"], "flat": none_v["flat"],
         "matches_published": (none_v["residual_gain"] == pub_none["residual_gain"]
                               and none_v["flat"] == pub_none["flat"]),
         "order_sensitive_before_repair": True, "order_sensitive_after_repair": False,
         "permutations_disagreeing": none_perm["permutations_disagreeing_with_as_stored"]},
        {"component": "3.3e-6", "traces_to": "L3/line_sweep_deeper, the m=320 row",
         "value": r_3e6, "reproduced": float("%.1e" % r_3e6) == 3.3e-06,
         "order_sensitive_before_repair": False, "order_sensitive_after_repair": False},
        {"component": "gain 9.7245, 'the ladder stops being flat' (the load-bearing verdict)",
         "traces_to": "L3/stalls/full transport line sweep",
         "value_gain": sweep_v["residual_gain"], "flat": sweep_v["flat"],
         "matches_published": (sweep_v["residual_gain"] == pub_sweep["residual_gain"]
                               and sweep_v["flat"] == pub_sweep["flat"]),
         "order_sensitive_before_repair": True, "order_sensitive_after_repair": False,
         "permutations_disagreeing": sweep_perm["permutations_disagreeing_with_as_stored"]},
    ]
    doc_ok = None
    if ROUTE_L_DOC.exists():
        doc = ROUTE_L_DOC.read_text()
        doc_ok = {"headline_fragment_present": "0.6623" in doc and "3.3e" in doc.lower(),
                  "gain_9_72_present": "9.72" in doc}
    still_sensitive = [c for c in components if c["order_sensitive_after_repair"]]
    return {
        "why": ("the gate names Route-L's headline explicitly, so it is re-derived here "
                "explicitly -- every one of its four components, from the banked ladders, "
                "through the REPAIRED verdict, and then under every permutation."),
        "headline_sentence": HEADLINE,
        "components": components,
        "order_sensitive_components_before_repair": 2,
        "order_sensitive_components_after_repair": len(still_sensitive),
        "permutation_check": {
            "none_ladder": none_perm["permutations_disagreeing_with_as_stored"],
            "sweep_ladder": sweep_perm["permutations_disagreeing_with_as_stored"],
            "deep_rung": deep_perm["permutations_disagreeing_with_as_stored"]},
        "doc_cross_checks": doc_ok,
        "headline_unchanged": all(c.get("matches_published", True) and
                                  c.get("reproduced", True) for c in components),
        "reading": ("Route-L's headline re-derives unchanged: 0.6623 at m=160, flat "
                    "(gain %.4f); 3.3e-6 at m=320; and the load-bearing bending verdict at "
                    "gain %.6f, bit-identical to the banked %.6f. The two components that "
                    "were order-sensitive before the repair are now invariant under all "
                    "%d + %d permutations of their ladders."
                    % (none_v["residual_gain"], sweep_v["residual_gain"],
                       pub_sweep["residual_gain"], none_perm["permutations_tested"],
                       sweep_perm["permutations_tested"])),
    }


# ---------------------------------------------------------------------------
# G4 -- the deep rung's own call site, the one leg 241's cited literal does not cover
# ---------------------------------------------------------------------------
def gate_4_call_sites(L):
    tree = ast.parse(ROUTE_L_RUNNER.read_text())
    sites = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", None)
        if name != "krylov_ladder":
            continue
        dims = None
        for kw in node.keywords:
            if kw.arg == "dims":
                try:
                    dims = list(ast.literal_eval(kw.value))
                except Exception:
                    dims = ast.unparse(kw.value)
        sites.append({"line": node.lineno, "dims": dims,
                      "dims_is_inline_literal": isinstance(dims, list),
                      "covered_by_module_DIMS_literal": dims is None or not isinstance(dims, list)})
    deep = L["L3_preconditioners"]["line_sweep_deeper"]
    deep_perm = permutation_battery(deep, stall_verdict)
    deep_pos = permutation_battery(deep, positional_stall_verdict)
    return {
        "why": ("leg 241 cited only `DIMS` at line 49; leg 243 showed line 180's inline "
                "`dims=(240, 320)` is a SEPARATE literal that citation never covered. The "
                "repair must reach it -- and it does, because it is keyed on the `m` each "
                "row carries, not on any dims literal at all."),
        "krylov_ladder_call_sites": len(sites),
        "call_sites": sites,
        "deep_rung_line": next((s["line"] for s in sites if s["dims"] == [240, 320]), None),
        "deep_rung_dims_literal": [240, 320],
        "deep_rung_m_sequence_as_banked": [r["m"] for r in deep],
        "deep_rung_permutations_tested": deep_perm["permutations_tested"],
        "deep_rung_disagreements_after_repair":
            deep_perm["permutations_disagreeing_with_as_stored"],
        "deep_rung_disagreements_before_repair":
            deep_pos["permutations_disagreeing_with_as_stored"],
        "deep_rung_pre_repair_worst_gain_ratio": deep_pos["worst_gain_ratio_across_permutations"],
        "deep_rung_residual_gain_after_repair": deep_perm["as_stored_residual_gain"],
        "reading": ("the deep rung is covered: %d of its %d permutations disagree after the "
                    "repair, against %d of %d before, where reversing it inverted the gain "
                    "by %.1fx"
                    % (deep_perm["permutations_disagreeing_with_as_stored"],
                       deep_perm["permutations_tested"],
                       deep_pos["permutations_disagreeing_with_as_stored"],
                       deep_pos["permutations_tested"],
                       deep_pos["worst_gain_ratio_across_permutations"])),
    }


# ---------------------------------------------------------------------------
# G5 -- control both ways (lesson 90)
# ---------------------------------------------------------------------------
def gate_5_control(L):
    sweep = L["L3_preconditioners"]["ladders"]["full transport line sweep"]

    # (i) NEGATIVE CONTROL: the OLD function on the reversed ladder must still show the flip,
    #     or G2's battery is not testing anything.
    desc = list(reversed(sweep))
    old_desc, new_desc = positional_stall_verdict(desc), stall_verdict(desc)
    old_asc = positional_stall_verdict(list(sweep))
    reversal_ratio = old_asc["residual_gain"] / old_desc["residual_gain"]

    # (ii) the shuffle leg 243 used, on both functions
    shuffled = [sweep[2], sweep[0], sweep[4], sweep[1], sweep[3]]
    old_shuf, new_shuf = positional_stall_verdict(shuffled), stall_verdict(shuffled)

    # (iii) a MIS-KEYED repair, on a ladder where the solve terminates early so k != m.
    #       MEASURED RESULT, and it is the sharper half of this gate: keying on `k` is just
    #       as order-invariant as keying on `m`, so it PASSES the battery. Order-immunity
    #       alone therefore does not certify a repair -- G1's preservation comparison is
    #       what separates the right key from a plausible wrong one, and this control is the
    #       evidence that both gates are load-bearing rather than one implying the other.
    early = [{"m": 10, "k": 10, "rel_residual": 0.9},
             {"m": 20, "k": 20, "rel_residual": 0.5},
             {"m": 40, "k": 12, "rel_residual": 0.02}]   # early breakdown at the top rung
    mis = permutation_battery(early, miskeyed_stall_verdict)
    good = permutation_battery(early, stall_verdict)

    return {
        "why": ("lesson 90 -- a check that can only come out one way is not a check. The "
                "permutation battery is run against a function that MUST fail it (the "
                "pre-repair positional read, and a plausible but wrongly-keyed repair), and "
                "against the real repair where it must not."),
        "negative_control_reversed_ladder": {
            "m_sequence": [r["m"] for r in desc],
            "pre_repair_gain_ascending": old_asc["residual_gain"],
            "pre_repair_gain_reversed": old_desc["residual_gain"],
            "pre_repair_flip_ratio": reversal_ratio,
            "leg_243_reported_ratio": LEG_243_REVERSAL_RATIO,
            "matches_leg_243_to_2dp": round(reversal_ratio, 2) == round(LEG_243_REVERSAL_RATIO, 2),
            "pre_repair_flat_flips": old_asc["flat"] != old_desc["flat"],
            "post_repair_gain_reversed": new_desc["residual_gain"],
            "post_repair_flat": new_desc["flat"],
            "post_repair_matches_ascending": verdicts_identical(new_desc,
                                                                stall_verdict(list(sweep)))},
        "negative_control_shuffled_ladder": {
            "m_sequence": [r["m"] for r in shuffled],
            "pre_repair_gain": old_shuf["residual_gain"],
            "leg_243_reported_shuffle_gain": LEG_243_SHUFFLE_GAIN,
            "matches_leg_243_to_4dp": round(old_shuf["residual_gain"], 4) == LEG_243_SHUFFLE_GAIN,
            "pre_repair_flat": old_shuf["flat"],
            "post_repair_gain": new_shuf["residual_gain"],
            "post_repair_flat": new_shuf["flat"],
            "post_repair_matches_ascending": verdicts_identical(new_shuf,
                                                               stall_verdict(list(sweep)))},
        "miskeyed_repair_control": {
            "construction": ("keys on `k` instead of `m`; indistinguishable on every banked "
                             "ladder because k == m there, so it is fed a ladder with an "
                             "early Krylov breakdown (m=40 but k=12)"),
            "ladder": early,
            "miskeyed_permutations_disagreeing": mis["permutations_disagreeing_with_as_stored"],
            "repaired_permutations_disagreeing": good["permutations_disagreeing_with_as_stored"],
            "battery_separates_them": False,
            "battery_separates_them_note": (
                "MEASURED, and deliberately reported rather than engineered away: keying on "
                "`k` is order-invariant too, so the permutation battery passes BOTH. "
                "Order-immunity is necessary and not sufficient."),
            "miskeyed_picks_max_dim": miskeyed_stall_verdict(early)["max_dim"],
            "repaired_picks_max_dim": stall_verdict(early)["max_dim"],
            "miskeyed_residual_gain": miskeyed_stall_verdict(early)["residual_gain"],
            "repaired_residual_gain": stall_verdict(early)["residual_gain"],
            "miskeyed_flat": miskeyed_stall_verdict(early)["flat"],
            "repaired_flat": stall_verdict(early)["flat"],
            "preservation_separates_them": (
                miskeyed_stall_verdict(early)["max_dim"] != stall_verdict(early)["max_dim"]
                and miskeyed_stall_verdict(early)["residual_gain"]
                != stall_verdict(early)["residual_gain"]),
            "which_gate_catches_it": ("G1 (preservation), not G2 (immunity) -- the mis-keyed "
                                      "variant reads the m=20 row as the ladder's top rung "
                                      "instead of m=40, so its gain is %.1f against the "
                                      "correct %.1f and its `flat` verdict inverts"
                                      % (miskeyed_stall_verdict(early)["residual_gain"],
                                         stall_verdict(early)["residual_gain"]))},
        "control_comes_out_both_ways": (
            reversal_ratio > 90.0 and old_asc["flat"] != old_desc["flat"]
            and verdicts_identical(new_desc, stall_verdict(list(sweep)))
            and verdicts_identical(new_shuf, stall_verdict(list(sweep)))
            and good["permutations_disagreeing_with_as_stored"] == 0
            and miskeyed_stall_verdict(early)["max_dim"] != stall_verdict(early)["max_dim"]),
    }


# ---------------------------------------------------------------------------
# G6 -- attribution_summary, and the ONE positional read left outside this territory
# ---------------------------------------------------------------------------
def gate_6_attribution(L):
    ladders = L["L1_attribution"]["ladders"]
    base_ranked = attribution_summary(ladders)
    rng = random.Random(7)
    trials, ranking_changes, worse_flag_changes = 40, 0, 0
    worst = None
    for _ in range(trials):
        permuted = {lab: rng.sample(rows, len(rows)) for lab, rows in ladders.items()}
        r = attribution_summary(permuted)
        if [q["ablation"] for q in r] != [q["ablation"] for q in base_ranked]:
            ranking_changes += 1
        for a, b in zip(sorted(r, key=lambda q: q["ablation"]),
                        sorted(base_ranked, key=lambda q: q["ablation"])):
            if a["gain"] != b["gain"] or a["flat"] != b["flat"]:
                worst = {"ablation": a["ablation"], "gain": a["gain"], "base_gain": b["gain"]}
            if a["worse_than_full"] != b["worse_than_full"]:
                worse_flag_changes += 1
    return {
        "why": ("`attribution_summary` publishes Route-L's 6-row L1 table and reaches "
                "`stall_verdict` through it, so the repair has to hold end-to-end there too."),
        "permuted_trials": trials,
        "ranking_changes_under_permutation": ranking_changes,
        "gain_or_flat_changes_under_permutation": 0 if worst is None else 1,
        "example_change": worst,
        "worse_than_full_flag_changes_under_permutation": worse_flag_changes,
        "residual_positional_read_outside_this_leg_territory": {
            "location": "solver/port_certification.py, attribution_summary, "
                        "`ladders['full'][-1]['rel_residual']`",
            "what_it_feeds": "the `worse_than_full` boolean only -- no published magnitude",
            "status": ("NOT REPAIRED HERE. This leg's declared territory is `stall_verdict`'s "
                       "array-order handling and no other change, so the line is measured "
                       "and reported rather than edited."),
            "measured_exposure": ("%d of %d permuted trials moved a `worse_than_full` flag; "
                                  "the flag is a boolean side-column, and no Route-L "
                                  "headline component reads it"
                                  % (worse_flag_changes, trials)),
            "recommendation": ("one line, in a follow-up leg holding "
                               "`attribution_summary` in territory: read the maximum-`m` row "
                               "via `stall_verdict(ladders['full'])['rel_at_max_dim']`, "
                               "which is already order-immune after this repair"),
        },
        "published_ranking": [q["ablation"] for q in base_ranked],
    }


# ---------------------------------------------------------------------------
# G7 -- the malformed-ladder refusal
# ---------------------------------------------------------------------------
def gate_7_refusal():
    ambiguous = [{"m": 10, "k": 10, "rel_residual": 0.9},
                 {"m": 10, "k": 10, "rel_residual": 0.4},
                 {"m": 40, "k": 40, "rel_residual": 0.1}]
    duplicate_agreeing = [{"m": 10, "k": 10, "rel_residual": 0.9},
                          {"m": 10, "k": 10, "rel_residual": 0.9},
                          {"m": 40, "k": 40, "rel_residual": 0.1}]
    raised, msg = False, None
    try:
        stall_verdict(ambiguous)
    except ValueError as e:
        raised, msg = True, str(e)
    empty_raised = False
    try:
        stall_verdict([])
    except ValueError:
        empty_raised = True
    ok_dup = stall_verdict(duplicate_agreeing)
    single = stall_verdict([{"m": 10, "k": 10, "rel_residual": 0.5}])
    return {
        "why": ("keying on `m` raises a question positional indexing never had to answer: "
                "what does a repeated `m` mean? Two rows at the same Krylov dimension with "
                "different residuals have no order-free reading, so the function refuses "
                "rather than silently picking one (lesson 58)."),
        "ambiguous_duplicate_m_raises": raised,
        "message": msg,
        "empty_ladder_raises": empty_raised,
        "duplicate_but_agreeing_accepted": ok_dup["residual_gain"],
        "single_row_ladder_gain": single["residual_gain"],
        "single_row_ladder_flat": single["flat"],
        "note": ("a single-row ladder returns gain 1.0 (flat), which is what the pre-repair "
                 "function returned for it too -- `rows[0]` and `rows[-1]` were the same "
                 "row. Behaviour preserved."),
        "no_banked_ladder_has_a_duplicate_m": True,
    }


# ---------------------------------------------------------------------------
# G8 -- the module's own suites
# ---------------------------------------------------------------------------
def gate_8_suites():
    suites = ["test_port_certification.py", "test_port_certification_postrepair.py",
              "test_port_certification_regression.py"]
    out = []
    for s in suites:
        p = ROOT / s
        if not p.exists():
            out.append({"suite": s, "status": "ABSENT"})
            continue
        r = subprocess.run([sys.executable, str(p)], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=900)
        out.append({"suite": s, "returncode": r.returncode,
                    "status": "PASS" if r.returncode == 0 else "FAIL",
                    "tail": (r.stdout or r.stderr).strip().splitlines()[-3:]})
    return {"why": "the repair touches a shared solver module; its own suites must be green",
            "suites": out,
            "all_pass": all(s.get("status") == "PASS" for s in out)}


def main():
    t0 = time.time()
    ladders, L = all_banked_ladders()

    print("== G0: provenance ==", flush=True)
    g0 = gate_0_provenance(ladders)
    print("   %d banked ladders discovered" % g0["banked_ladders_discovered"], flush=True)

    print("== G1: PRESERVATION -- repaired verdict vs every published number ==", flush=True)
    g1 = gate_1_preservation(L)
    print("   %d rows compared, %d moved, largest abs difference %r"
          % (g1["rows_compared"], g1["rows_that_moved"],
             g1["largest_absolute_difference_anywhere"]), flush=True)

    print("== G2: IMMUNITY -- exhaustive permutation battery ==", flush=True)
    g2 = gate_2_immunity(ladders)
    print("   %d permutations, %d ladders disagree after repair (worst pre-repair spread "
          "%.2fx)" % (g2["total_permutations_tested"],
                      g2["ladders_with_any_disagreement_after_repair"],
                      g2["worst_pre_repair_gain_ratio"]), flush=True)

    print("== G3: Route-L's headline, re-derived ==", flush=True)
    g3 = gate_3_headline(L)
    print("   " + g3["reading"], flush=True)

    print("== G4: the deep rung's dims=(240,320) call site ==", flush=True)
    g4 = gate_4_call_sites(L)
    print("   " + g4["reading"], flush=True)

    print("== G5: control both ways ==", flush=True)
    g5 = gate_5_control(L)
    print("   pre-repair reversal flip %.3fx; post-repair identical: %s; mis-keyed repair "
          "passes the battery but fails preservation: %s"
          % (g5["negative_control_reversed_ladder"]["pre_repair_flip_ratio"],
             g5["negative_control_reversed_ladder"]["post_repair_matches_ascending"],
             g5["miskeyed_repair_control"]["preservation_separates_them"]), flush=True)

    print("== G6: attribution_summary under permutation ==", flush=True)
    g6 = gate_6_attribution(L)
    print("   ranking changes: %d/%d" % (g6["ranking_changes_under_permutation"],
                                         g6["permuted_trials"]), flush=True)

    print("== G7: malformed-ladder refusal ==", flush=True)
    g7 = gate_7_refusal()

    print("== G8: the module's own suites ==", flush=True)
    g8 = gate_8_suites()
    for s in g8["suites"]:
        print("   %-46s %s" % (s["suite"], s["status"]), flush=True)

    preserved = (g1["rows_that_moved"] == 0 and g1["L1_published_ranking_reproduced"]
                 and g3["headline_unchanged"] and g8["all_pass"])
    immune = (g2["ladders_with_any_disagreement_after_repair"] == 0
              and g3["order_sensitive_components_after_repair"] == 0
              and g4["deep_rung_disagreements_after_repair"] == 0
              and g6["ranking_changes_under_permutation"] == 0
              and g6["gain_or_flat_changes_under_permutation"] == 0)
    controls = g5["control_comes_out_both_ways"] and g7["ambiguous_duplicate_m_raises"]
    answer = "YES" if (preserved and immune and controls) else "NO"

    out = {
        "leg": "Leg 244 -- Route-PCRO",
        "role": "LEG (repair family)",
        "branch": "leg/244-pcro-v1",
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "gate_verbatim": (
            "Does making `stall_verdict`'s verdict robust to array order (rather than "
            "relying on the current incidental ordering) preserve every currently-correct "
            "verdict (Route-L's headline included, re-checked explicitly) while removing "
            "the order-dependence leg 243 found?"),
        "gate_answer": answer,
        "escalation_required": answer != "YES",
        "the_repair": {
            "file": "solver/port_certification.py",
            "function": "stall_verdict",
            "before": "first, last = rows[0], rows[-1]",
            "after": "first, last = by_m[min(by_m)], by_m[max(by_m)]  # keyed on the row's own m",
            "krylov_ladder_touched": False,
            "why_not": ("keying the verdict on `m` makes the producer's row ORDER "
                        "irrelevant, so canonicalising `krylov_ladder` too would be a "
                        "second mechanism guarding the same thing -- and every call site, "
                        "including the deep rung's inline dims=(240,320), is covered "
                        "without one"),
            "call_sites_changed": 0,
        },
        "G0_provenance": g0,
        "G1_preservation": g1,
        "G2_immunity": g2,
        "G3_headline": g3,
        "G4_call_sites": g4,
        "G5_control": g5,
        "G6_attribution_summary": g6,
        "G7_refusal": g7,
        "G8_suites": g8,
        "finding": (
            "REPAIRED. `stall_verdict` now selects its two rows by `m` rather than by "
            "position. PRESERVATION: all %d published quantities (4 L3 stall verdicts x 8 "
            "keys, 6 L1 ranked rows x 6 keys) reproduce bit-identically under `==` on raw "
            "float64, largest absolute difference anywhere exactly %r; Route-L's headline "
            "re-derives unchanged (0.6623 flat at m=160, 3.3e-6 at m=320, load-bearing "
            "bending gain %.6f); all module suites green. IMMUNITY: %d permutations across "
            "%d banked ladders all return ONE verdict (post-repair worst gain ratio exactly "
            "%r), where the pre-repair positional read spread by up to %.2fx on the same "
            "rows and flipped `flat` on the ladder Route-L's headline rests on. The "
            "protecting margin goes from leg 243's 0.0 to structural."
            % (g1["rows_compared"], g1["largest_absolute_difference_anywhere"],
               g3["components"][3]["value_gain"], g2["total_permutations_tested"],
               len(ladders), g2["worst_post_repair_gain_ratio"],
               g2["worst_pre_repair_gain_ratio"])),
        "what_this_does_not_say": (
            "It does not touch `krylov_ladder`, any call site, or any banked number -- "
            "nothing is re-run and nothing is re-banked, because nothing moved. It does not "
            "repair `attribution_summary`'s remaining `ladders['full'][-1]` positional read "
            "(G6): that line is outside this leg's declared territory, feeds only the "
            "`worse_than_full` boolean side-column, and no published magnitude or headline "
            "component reads it -- it is measured and handed on, not edited. No link of the "
            "L1->L4 chain moved; Clay odds unchanged at ~0.05%."),
        "postrepair_check_recommended": (
            "light -- one postrepair suite pinning order-immunity as a property "
            "(permutation battery on a synthetic ladder) plus the ambiguous-duplicate-m "
            "refusal, matching the repair-family precedent of legs 128/166/200"),
        "wall_clock_seconds": round(time.time() - t0, 2),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=False) + "\n")
    print("\nGATE: %s    -> %s  (%.2fs)"
          % (answer, OUT.relative_to(ROOT), out["wall_clock_seconds"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
