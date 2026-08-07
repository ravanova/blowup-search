"""P2 Route-VBRG v1 -- regenerate Route-D v11's banked anchor JSON from leg 247's
repaired runner, and CHECK the regeneration leaf-by-leaf against the stale bank.

Leg 247 repaired `v5_budget`'s margin selection in
`experiments/p2_route_d_v11_anchor.py` (min -> worst-case max) and reported, from
its OWN standalone repair harness `experiments/p2_route_vbr_v1_repair.py`, that
Route-D v11 misses its own Y0 budget at a = 0.45.  Leg 247 deliberately did NOT
touch the banked artifact `writeup/data/p2_route_d_v11_anchor.json` (leg 236 was
read-only on it), and declared its stale margin as residue 1.  This leg is that
residue: regenerate the artifact from the repaired runner and verify.

This script asserts NOTHING about the physics.  It answers exactly two questions
and reports magnitudes for both:

  Q1 (reproduction)  Does the REGENERATED v5_budget block reproduce leg 247's own
                     reported numbers -- from a fresh full run of the anchor
                     runner, not from leg 247's separate repair harness?
  Q2 (isolation)     Does EVERY other banked leaf in the JSON hold still?  Leg 247
                     measured 0-of-196-other-JSONs isolation for the DIAGNOSIS;
                     this extends that to the REGENERATION of this one file.

Run (after regenerating the artifact):

    .venv/bin/python experiments/p2_route_d_v11_anchor.py     # writes the artifact
    .venv/bin/python experiments/p2_route_vbrg_v1_regen.py    # checks it

The stale (pre-repair) bank is read from git at the merge base, so this check is
reproducible without a scratch copy.  -> writeup/data/p2_route_vbrg_v1_regen.json
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANCHOR = ROOT / "writeup" / "data" / "p2_route_d_v11_anchor.json"
OUT = ROOT / "writeup" / "data" / "p2_route_vbrg_v1_regen.json"

# Leg 247's own reported numbers, transcribed from commit 10be909's message and
# from writeup/data/p2_route_vbr_v1_repair.json.  These are the reproduction
# target: the regenerated artifact must land on them, not merely near them.
LEG247_COMMIT = "10be909a4d4e95d293fabb2c526e7ac1896dea95"
LEG247_MARGIN = 0.016122858874141922   # Y0_max / worst-case weighted defect
LEG247_VIOLATION_X = 62.02373957411577  # how far over budget a = 0.45 sits
LEG247_BAD_A = 0.45
LEG247_N_ROWS_OVER = 1
LEG247_N_GOOD_ROWS = 11
LEG247_BEST_ROW_MARGIN_A = 0.35           # worst-case margin over the rows that hold
LEG247_MARGIN_WITHIN = 10.655996808538774

# The margin the pre-repair bank carries.  Named so the check can state the size
# of the correction rather than just that it happened.
STALE_MARGIN = 1.0467862585933441e10

TOL_REL = 1e-6      # leg 247 quoted ~10 significant figures; this is generous


def git_show(rev_path):
    return subprocess.run(["git", "-C", str(ROOT), "show", rev_path],
                          capture_output=True, text=True, check=True).stdout


def merge_base():
    return subprocess.run(["git", "-C", str(ROOT), "merge-base", "HEAD",
                           "origin/main"],
                          capture_output=True, text=True,
                          check=True).stdout.strip()


def flatten(obj, prefix=""):
    """Every leaf of a nested dict/list, keyed by its dotted path."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, "%s.%s" % (prefix, k) if prefix else str(k)))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, "%s[%d]" % (prefix, i)))
    else:
        out[prefix] = obj
    return out


def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        if a == b:
            return True
        if a != a and b != b:            # both NaN
            return True
        scale = max(abs(a), abs(b))
        return scale > 0 and abs(a - b) / scale <= 1e-15
    return a == b


def rel(x, target):
    return abs(x - target) / abs(target) if target else abs(x)


def main():
    if not ANCHOR.exists():
        sys.exit("regenerate %s first" % ANCHOR)
    fresh = json.loads(ANCHOR.read_text())

    base = merge_base()
    stale = json.loads(git_show("%s:writeup/data/p2_route_d_v11_anchor.json"
                                % base))

    # ---- Q1: does the regenerated v5_budget reproduce leg 247's numbers? -----
    b = fresh["v5_budget"]
    over = b.get("rows_over_budget") or []
    bad = [o for o in over if abs(o["a"] - LEG247_BAD_A) < 1e-12]

    repro = {
        "margin_regenerated": b["margin"],
        "margin_leg247": LEG247_MARGIN,
        "margin_rel_error": rel(b["margin"], LEG247_MARGIN),
        "margin_matches_leg247": rel(b["margin"], LEG247_MARGIN) <= TOL_REL,
        "margin_stale_banked": STALE_MARGIN,
        "correction_factor_vs_stale": STALE_MARGIN / b["margin"]
                                      if b["margin"] else None,
        "margin_selection": b.get("margin_selection"),
        "budget_holds_uniformly": b.get("budget_holds_uniformly"),
        "n_good_rows": b.get("n_good_rows"),
        "n_good_rows_matches": b.get("n_good_rows") == LEG247_N_GOOD_ROWS,
        "n_rows_over_budget": len(over),
        "n_rows_over_budget_matches": len(over) == LEG247_N_ROWS_OVER,
        "over_budget_a_values": [o["a"] for o in over],
        "violation_x_regenerated": bad[0]["violation_x"] if bad else None,
        "violation_x_leg247": LEG247_VIOLATION_X,
        "violation_x_rel_error": (rel(bad[0]["violation_x"], LEG247_VIOLATION_X)
                                  if bad else None),
        "violation_x_matches_leg247": bool(
            bad and rel(bad[0]["violation_x"], LEG247_VIOLATION_X) <= TOL_REL),
        "margin_over_rows_within_budget": b.get("margin_over_rows_within_budget"),
        "margin_within_leg247": LEG247_MARGIN_WITHIN,
        "margin_within_rel_error": (
            rel(b["margin_over_rows_within_budget"], LEG247_MARGIN_WITHIN)
            if b.get("margin_over_rows_within_budget") is not None else None),
    }
    repro["Q1_reproduces"] = bool(
        repro["margin_matches_leg247"]
        and repro["violation_x_matches_leg247"]
        and repro["n_rows_over_budget_matches"]
        and repro["n_good_rows_matches"])

    # ---- Q2: does every OTHER banked leaf hold still? ------------------------
    fs, ss = flatten(fresh), flatten(stale)
    added = sorted(set(fs) - set(ss))
    removed = sorted(set(ss) - set(fs))
    changed = sorted(k for k in set(fs) & set(ss) if not same(fs[k], ss[k]))

    # Everything the repair is ALLOWED to move: the v5_budget block (its margin,
    # its new diagnostic fields, its re-worded reading) and the meta timestamp.
    def expected(path):
        return path.startswith("v5_budget.") or path.startswith("meta.")

    unexpected_changed = [k for k in changed if not expected(k)]
    unexpected_added = [k for k in added if not expected(k)]
    unexpected_removed = [k for k in removed if not expected(k)]

    isolation = {
        "n_leaves_fresh": len(fs),
        "n_leaves_stale": len(ss),
        "n_leaves_compared": len(set(fs) & set(ss)),
        "n_changed": len(changed),
        "n_added": len(added),
        "n_removed": len(removed),
        "changed_paths": changed,
        "added_paths": added,
        "removed_paths": removed,
        "n_unexpected_changed": len(unexpected_changed),
        "unexpected_changed_paths": unexpected_changed,
        "unexpected_added_paths": unexpected_added,
        "unexpected_removed_paths": unexpected_removed,
        "changed_values": {k: {"stale": ss[k], "fresh": fs[k]} for k in changed},
    }
    isolation["Q2_isolated"] = not (unexpected_changed or unexpected_added
                                    or unexpected_removed)

    # ---- positive control: the check can actually SEE a moved leaf -----------
    # Perturb one untouched leaf of the fresh copy and confirm the same predicate
    # flags it.  Without this, "0 unexpected changes" is unfalsifiable.
    control_key = next((k for k in sorted(set(fs) & set(ss))
                        if not expected(k) and isinstance(fs[k], float)
                        and fs[k] == fs[k]), None)
    control = {"probe_leaf": control_key}
    if control_key is not None:
        poked = dict(fs)
        poked[control_key] = fs[control_key] * (1.0 + 1e-9) + 1e-300
        fired = [k for k in set(poked) & set(ss)
                 if not same(poked[k], ss[k]) and not expected(k)]
        control["perturbation_rel"] = 1e-9
        control["n_flagged_under_perturbation"] = len(fired)
        control["control_fires"] = control_key in fired
    control["ok"] = bool(control.get("control_fires"))

    gate = repro["Q1_reproduces"] and isolation["Q2_isolated"] and control["ok"]

    result = {
        "meta": {
            "leg": 252,
            "route": "VBRG",
            "question": "regenerate Route-D v11's banked anchor JSON from leg "
                        "247's repaired runner; does it land on leg 247's own "
                        "reported numbers with every other banked leaf still?",
            "repair_ported_from": LEG247_COMMIT,
            "repair_ported_reason": "leg 247's branch leg/247-vbr-v1 was not "
                                    "merged to main when this leg ran; the "
                                    "runner file here is byte-identical to "
                                    "leg 247's repaired version",
            "stale_bank_read_from": base,
            "tolerance_rel": TOL_REL,
        },
        "q1_reproduction": repro,
        "q2_isolation": isolation,
        "positive_control": control,
        "gate": "YES" if gate else "NO",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print("ROUTE-VBRG v1 -- regeneration check")
    print("  Q1  margin regenerated %.10e vs leg 247 %.10e (rel %.2e)"
          % (repro["margin_regenerated"], LEG247_MARGIN,
             repro["margin_rel_error"]))
    print("      stale bank %.10e -> correction factor %.6ex"
          % (STALE_MARGIN, repro["correction_factor_vs_stale"]))
    print("      a=%.2f over budget by %sx (leg 247: %.8fx), %d/%d good rows over"
          % (LEG247_BAD_A,
             ("%.8f" % repro["violation_x_regenerated"])
             if repro["violation_x_regenerated"] is not None else "NONE",
             LEG247_VIOLATION_X, repro["n_rows_over_budget"],
             repro["n_good_rows"] or -1))
    print("  Q2  %d leaves compared, %d changed, %d added, %d removed; "
          "%d UNEXPECTED changes outside v5_budget/meta"
          % (isolation["n_leaves_compared"], isolation["n_changed"],
             isolation["n_added"], isolation["n_removed"],
             isolation["n_unexpected_changed"]))
    if unexpected_changed:
        for k in unexpected_changed:
            print("      MOVED %s: %r -> %r" % (k, ss[k], fs[k]))
    print("  CTL positive control on %s fires: %s"
          % (control_key, control["ok"]))
    print("  GATE %s" % result["gate"])
    print("\n[done] wrote %s" % OUT)
    return 0 if gate else 1


if __name__ == "__main__":
    sys.exit(main())
