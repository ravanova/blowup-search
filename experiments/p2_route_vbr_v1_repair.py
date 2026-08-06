#!/usr/bin/env python3
"""P2 Route-VBR v1 (leg 247) -- repair of the v5_budget min/max selection.

Leg 235 (Route-CDAP) found that `v5_budget` in
`experiments/p2_route_d_v11_anchor.py` builds its headline `margin` from
`newton_weighted_defect_min` while `newton_weighted_defect_max` -- computed on
the very next line, banked in the same dict -- violates the block's own budget
`Y0_max_from_v10 = 2.45e-4` by 62.02x at `a = 0.45`.  Nothing was patched there;
this leg patches the selection and measures what the corrected number is.

THE FIX, AND WHY IT IS THE MIN->MAX ONE AND NOT A COMBINATION.
`v5_budget`'s claim is `Y0 <= Y0_max` **for the whole `a`-range the block
declares** (its own reading says "for a < a*", and `a_range_used` is that
range).  A universally-quantified budget is certified by its WORST case, so the
only margin that means anything is `Y0_max / max(weighted_defect)`.  The min is
the most favourable member of the set the claim quantifies over; it certifies
nothing at all, and no weighting of min against max recovers a valid certificate
(a mean or a median would still let a single over-budget row through).  So the
principled fix is: `margin` := worst-case, the min is kept as an explicitly
named best-row diagnostic, and the rows that exceed the budget are enumerated so
the non-uniformity is a banked fact rather than a prose caveat.

WHAT THIS RUNNER MEASURES.
  R1  the corrected v5_budget block, by calling the PATCHED function on the
      banked v2/v4 data (the repair is a pure selection change, so this is
      exact -- no re-solve can move it).
  R2  a fresh Newton re-solve of a = 0.45 and its two neighbours, to confirm
      the 1.52e-2 defect is a property of the problem and not a stale bank.
  R3  the load-bearing regression check: leg 235's R-SELECT rule re-run
      independently over every OTHER banked JSON, to confirm leg 235's own
      0/195 isolation finding.

Reproduce: .venv/bin/python experiments/p2_route_vbr_v1_repair.py
"""
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from experiments.p2_route_d_v11_anchor import (  # noqa: E402
    N, Y0_MAX, v5_budget, weighted_defect)
from solver.profile_newton import TwoScaleNewton  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data"
ANCHOR = DATA / "p2_route_d_v11_anchor.json"
OUT = DATA / "p2_route_vbr_v1_repair.json"

# The two artifacts this leg is a repair OF.  Excluded from the R3 denominator:
# the anchor because it is the known instance, this leg's own output because it
# quotes the instance's numbers verbatim (leg 235's instrument bug #2).
EXCLUDE = {"p2_route_d_v11_anchor.json", "p2_route_vbr_v1_repair.json"}

BUDGET_HINTS = ("max", "budget", "limit", "bound", "tol", "thresh", "cap",
                "ceiling", "allow")
REL = 1e-9


# ---------------------------------------------------------------- R1


def r1_corrected_block():
    d = json.loads(ANCHOR.read_text())
    banked = d["v5_budget"]
    fixed = v5_budget(d["v2_sweep"], d["v4_grids"])
    good = [r for r in d["v2_sweep"]["rows"]
            if r["relres"] < 1e-8
            and r["a"] <= d["v4_grids"]["grid_converged_a_max"] + 1e-12]
    return {
        "banked": {k: banked[k] for k in
                   ("Y0_max_from_v10", "a_range_used",
                    "newton_weighted_defect_min", "newton_weighted_defect_max",
                    "margin")},
        "corrected": {k: v for k, v in fixed.items() if k != "reading"},
        "good_rows": [{"a": r["a"], "relres": r["relres"],
                       "weighted_defect": r["weighted_defect"],
                       "row_margin": Y0_MAX / r["weighted_defect"],
                       "within_budget": r["weighted_defect"] <= Y0_MAX}
                      for r in good],
        "margin_change_x": fixed["margin"] / banked["margin"],
        "reading": "the selection change moves the headline margin from "
                   "%.6g (min-selected, meaningless as a certificate) to "
                   "%.6g (worst-case).  A margin < 1 IS the budget violation: "
                   "the corrected number does not clear the budget, it "
                   "quantifies by how much one row misses it."
                   % (banked["margin"], fixed["margin"]),
    }


# ---------------------------------------------------------------- R2


def r2_resolve(a_values=(0.40, 0.45, 0.50)):
    d = json.loads(ANCHOR.read_text())
    bank = {round(r["a"], 6): r for r in d["v2_sweep"]["rows"]}
    rows = []
    for a in a_values:
        t0 = time.time()
        nw = TwoScaleNewton(a=float(a), n=N)
        s = nw.solve(om0=None, c0=0.5)
        wd = weighted_defect(nw, s["Omega"], s["c"])
        b = bank.get(round(float(a), 6), {})
        rows.append({
            "a": float(a), "n": N,
            "relres": s["relres"], "iterations": s["iterations"],
            "c": s["c"], "weighted_defect": wd,
            "banked_weighted_defect": b.get("weighted_defect"),
            "rel_difference_vs_bank": (
                abs(wd - b["weighted_defect"]) / b["weighted_defect"]
                if b.get("weighted_defect") else None),
            "violation_x_fresh": wd / Y0_MAX,
            "seconds": time.time() - t0,
        })
    return {"rows": rows,
            "reading": "a fresh Newton solve on the same discrete system.  The "
                       "a = 0.45 defect is not a stale bank: it reproduces, and "
                       "it is ~6 decades above both neighbours, which is why the "
                       "min-selection hid it so completely."}


# ---------------------------------------------------------------- R3


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) \
        and np.isfinite(x)


def _pairs(dd):
    """(stem, min_value, max_value) for every _min/_max sibling pair."""
    out = []
    for k in dd:
        if not k.endswith("_min"):
            continue
        stem = k[:-4]
        km = stem + "_max"
        if km in dd and _num(dd[k]) and _num(dd[km]):
            out.append((stem, float(dd[k]), float(dd[km])))
    return out


def _budgets(dd, skip):
    out = []
    for k, v in dd.items():
        if k in skip or not _num(v) or v <= 0:
            continue
        if any(h in k.lower() for h in BUDGET_HINTS):
            out.append((k, float(v)))
    return out


def _walk(node, path, sink):
    if isinstance(node, dict):
        sink.append((path, node))
        for k, v in node.items():
            _walk(v, path + "/" + str(k), sink)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, path + "[%d]" % i, sink)


def r_select(doc):
    """Leg 235's R-SELECT: a headline scalar built from the FAVOURABLE end of a
    min/max pair, against a budget the UNFAVOURABLE end violates."""
    sink = []
    _walk(doc, "", sink)
    hits, pairs_seen = [], 0
    for path, dd in sink:
        prs = _pairs(dd)
        pairs_seen += len(prs)
        for stem, lo, hi in prs:
            skip = {stem + "_min", stem + "_max"}
            for bk, bv in _budgets(dd, skip):
                if not (hi > bv >= lo > 0):
                    continue          # the unfavourable end must MISS the budget
                for k, v in dd.items():
                    if k in skip or k == bk or not _num(v) or v <= 0:
                        continue
                    fav, unfav = bv / lo, bv / hi
                    if abs(v - fav) <= REL * fav and abs(v - unfav) > REL * fav:
                        hits.append({
                            "path": path, "stem": stem, "headline_key": k,
                            "headline_value": float(v),
                            "favourable_end": lo, "unfavourable_end": hi,
                            "budget_key": bk, "budget_value": bv,
                            "violation_x": hi / bv,
                            "headline_if_corrected": unfav,
                        })
    return hits, pairs_seen, len(sink)


def r3_regression():
    files = sorted(p for p in DATA.glob("*.json") if p.name not in EXCLUDE)
    per_file, affected, pairs, dicts = [], [], 0, 0
    unreadable = []
    for p in files:
        try:
            doc = json.loads(p.read_text())
        except Exception as exc:                      # noqa: BLE001
            unreadable.append({"file": p.name, "error": str(exc)})
            continue
        h, np_, nd = r_select(doc)
        pairs += np_
        dicts += nd
        per_file.append({"file": p.name, "minmax_pairs": np_, "hits": len(h)})
        if h:
            affected.append({"file": p.name, "hits": h})

    # Positive control: the rule must still fire on the known instance, or a
    # clean sweep of the other files means nothing.
    ctrl_doc = json.loads(ANCHOR.read_text())
    ctrl_hits, _, _ = r_select({"v5_budget": ctrl_doc["v5_budget"]})

    return {
        "json_files_screened": len(files),
        "json_files_unreadable": unreadable,
        "dicts_walked": dicts,
        "minmax_sibling_pairs_seen": pairs,
        "files_affected": len(affected),
        "affected": affected,
        "excluded_from_denominator": sorted(EXCLUDE),
        "positive_control": {
            "on": "p2_route_d_v11_anchor.json :: v5_budget (BANKED, pre-repair)",
            "fired": bool(ctrl_hits),
            "hit": ctrl_hits[0] if ctrl_hits else None,
        },
        "per_file": per_file,
        "reading": "the control fires on the banked pre-repair block, so a null "
                   "elsewhere is a measurement and not a broken instrument.  "
                   "The named limit, restated from leg 235: this rule can only "
                   "speak about dicts that actually carry a _min/_max sibling "
                   "pair AND a budget-named sibling in the SAME record.  It is "
                   "silent about, not clearing, every other shape.",
    }


# ---------------------------------------------------------------- main


def main():
    data = {"meta": {
        "leg": "P2 Route-VBR v1 (leg 247): repair of Route-D v11 v5_budget's "
               "min/max selection, per leg 235's diagnosis",
        "tier": "repair + regression -- no new mathematics",
        "reproduce": "python experiments/p2_route_vbr_v1_repair.py",
        "repairs": "experiments/p2_route_d_v11_anchor.py :: v5_budget",
        "diagnosed_by": "leg 235 (Route-CDAP), branch leg/235-cdap-v1",
        "gate": "Does using the correct selection (per leg 235's own diagnosis) "
                "for v5_budget's margin computation at a=0.45 bring the block "
                "back within its own declared Y0 budget, and does re-running "
                "the other 195 banked JSONs confirm they remain unaffected "
                "(matching leg 235's own 0/195 isolation finding)?",
    }}
    data["r1_corrected_block"] = r1_corrected_block()
    data["r3_regression"] = r3_regression()
    data["r2_resolve"] = r2_resolve()

    c = data["r1_corrected_block"]["corrected"]
    reg = data["r3_regression"]
    within = bool(c["budget_holds_uniformly"])
    data["gate"] = {
        "clause_1_a045_within_budget": within,
        "clause_1_detail": ("corrected worst-case margin %.6g (< 1 means the "
                            "budget is MISSED); a = 0.45 misses it by %.4fx"
                            % (c["margin"], c["worst_violation_x"] or 0.0)),
        "clause_2_others_unaffected": reg["files_affected"] == 0,
        "clause_2_detail": "%d of %d other banked JSONs affected"
                           % (reg["files_affected"], reg["json_files_screened"]),
        "answer": "YES" if (within and reg["files_affected"] == 0) else "NO",
        "reading": "the gate is a conjunction and clause 1 decides it.  The "
                   "repair is correct and lands the right number; the number it "
                   "lands is a budget MISS, so the block does not come back "
                   "within its own budget -- it is not a failure of the repair, "
                   "it is the repair reporting what was always true.",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2))

    print("\nP2 ROUTE-VBR v1 (leg 247) -- v5_budget selection repair\n" + "=" * 62)
    b = data["r1_corrected_block"]["banked"]
    print("  R1  banked margin %.6g (from the MIN %.6e)"
          % (b["margin"], b["newton_weighted_defect_min"]))
    print("      corrected margin %.6g (worst-case, from the MAX %.6e)"
          % (c["margin"], c["newton_weighted_defect_max"]))
    print("      %d/%d good rows over budget: %s"
          % (len(c["rows_over_budget"]), c["n_good_rows"],
             ", ".join("a=%.2f by %.4fx" % (o["a"], o["violation_x"])
                       for o in c["rows_over_budget"]) or "none"))
    print("      margin over the rows that DO hold: %.6g"
          % (c["margin_over_rows_within_budget"] or float("nan")))
    for r in data["r2_resolve"]["rows"]:
        print("  R2  a=%.2f  fresh wd %.6e  banked %.6e  reldiff %.2e"
              % (r["a"], r["weighted_defect"], r["banked_weighted_defect"],
                 r["rel_difference_vs_bank"]))
    print("  R3  %d other banked JSONs, %d dicts, %d min/max sibling pairs "
          "-- %d affected (control fired: %s)"
          % (reg["json_files_screened"], reg["dicts_walked"],
             reg["minmax_sibling_pairs_seen"], reg["files_affected"],
             reg["positive_control"]["fired"]))
    print("  GATE %s -- %s" % (data["gate"]["answer"],
                               data["gate"]["clause_1_detail"]))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
