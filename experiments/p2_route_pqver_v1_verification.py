"""Leg 195 / Route-PQVER — independent post-landing verification of leg 60 (e0eba8e).

Leg 60 landed a "user-approved correction" to two banked writeups: three quoted numbers in
`writeup/4_p2_lottery/TECHNICAL_P2_ROUTEPORT_V{1,2}.md` and `writeup/README.md` were changed
to match the committed curated data, and its two evidence scripts then reported CLEAN
114/114.  Nobody re-derived that correction independently at the time.  This leg is that
review, arriving late.

INDEPENDENCE.  This runner does NOT import, exec, or copy anything from
`experiments/p2_route_port_v{1,2}_*_evidence.py`.  It reads only the two curated JSON files
and the two corrected markdown documents, re-implements the "half a unit in the last quoted
digit" rule from scratch on top of `decimal`, and re-fits the v2 slopes itself with
`numpy.polyfit` rather than reading the stored `verdict` fields.  Where leg 60's scripts and
this one agree, they agree because the data says so, not because they share code.

TWO PRE-COMMITTED CLAUSES (fixed after reading e0eba8e, before this file was written):

  V1 (the correction itself).  Does an independent re-derivation straight from the committed
      curated JSON confirm all three of leg 60's landed corrections
      (28x -> 63x, -2.541222 -> -2.541024, 1.168% -> 1.169%) AND both ban-bearing numbers
      (distance/r_max = 1.55e+08, slope = +0.4703 decades per unit rho), each to the
      precision the corrected prose states?
      YES -> independently confirmed; bank as the permanent verification record.
      NO  -> report the exact discrepancy; a confirmed gap in a landed claim.

  V2 (completeness of the correction).  Does any UNCORRECTED copy of a corrected literal
      survive in the tracked tree, and is any such copy consumed as a number by live code?
      A surviving copy is a gap in the landing even if V1 passes.

Verifier discipline: this leg REPORTS gaps and never repairs them.  It touches no file leg 60
touched.

    .venv/bin/python experiments/p2_route_pqver_v1_verification.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from decimal import Decimal

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "writeup", "data")
OUT = os.path.join(ROOT, "writeup", "data", "p2_route_pqver_v1_verification.json")

LEG60_COMMIT = "e0eba8e"


# ---------------------------------------------------------------------------
# the precision rule, re-implemented from scratch
# ---------------------------------------------------------------------------

def half_ulp(quoted: str) -> float:
    """Half a unit in the last digit the string actually writes.

    Independent of leg 60's implementation: built on `decimal.Decimal.as_tuple()`, so it
    reads the exponent of the literal rather than parsing the string by hand.  '1.831e-01'
    -> 5e-05.  '63' -> 0.5.  '-2.541024' -> 5e-07.
    """
    t = Decimal(quoted.strip()).as_tuple()
    return float(Decimal((0, (5,), t.exponent - 1)))


def check(label, quoted: str, value: float, where: str):
    """One ledger row.  PASS iff |value - quoted| <= half a unit in the quoted last digit."""
    q = float(quoted)
    err = abs(value - q)
    hu = half_ulp(quoted)
    return {
        "label": label,
        "quoted": quoted,
        "quoted_as_float": q,
        "data": value,
        "abs_err": err,
        "half_ulp": hu,
        "half_ulps_out": err / hu,
        "rel_err": err / abs(q) if q else float("nan"),
        "pass": bool(err <= hu),
        "where": where,
    }


# ---------------------------------------------------------------------------
# the data
# ---------------------------------------------------------------------------

def load():
    with open(os.path.join(DATA, "p2_route_port_v1_bordered.json")) as f:
        v1 = json.load(f)
    with open(os.path.join(DATA, "p2_route_port_v2_reach.json")) as f:
        v2 = json.load(f)
    return v1, v2


# ---------------------------------------------------------------------------
# V1 -- the five numbers the correction turns on
# ---------------------------------------------------------------------------

def clause_v1(v1, v2):
    rows = []

    # --- correction (i): the rho=10 vs rho=6 gap factor, 28x -> 63x -----------------
    rungs = {r["rho_max"]: r for r in v2["rungs"]}
    ratio = {rho: r["distance"] / r["r_max"] for rho, r in rungs.items()}
    gap_6_10 = ratio[10.0] / ratio[6.0]
    gap_8_10 = ratio[10.0] / ratio[8.0]
    rows.append(check("(i) gap rho=10 vs rho=6, CORRECTED value",
                      "63", gap_6_10, "TECHNICAL_P2_ROUTEPORT_V2.md sec 2 / README item 47"))
    rows.append(check("(i) gap rho=8 -> 10, leg 60's diagnosis of the OLD 28x",
                      "28", gap_8_10, "leg 60 journal, claimed source of the error"))
    # the old literal, scored against the same rule, to size the error leg 60 removed
    old_i = check("(i) OLD literal 28 against the rho=6 baseline it named",
                  "28", gap_6_10, "pre-e0eba8e prose")
    rows.append(old_i)

    # --- correction (ii): the reach table's rho=8 row, -2.541222 -> -2.541024 -------
    reach = {r["rho_max"]: r for r in v1["C_extrapolation"]["reach"]}
    res = {r["n"]: r for r in v1["A_newton_ladder"]["rungs"]}
    reach_rho8 = reach[8.0]["ratio"]
    rows.append(check("(ii) reach ladder rho=8 (n=301), CORRECTED value",
                      "-2.541024", reach_rho8, "TECHNICAL_P2_ROUTEPORT_V1.md sec 2.1"))
    rows.append(check("(ii) resolution ladder n=201, leg 60's diagnosis of the OLD literal",
                      "-2.541222", res[201]["ratio"],
                      "TECHNICAL_P2_ROUTEPORT_V1.md sec 2, the adjacent table"))
    old_ii = check("(ii) OLD literal -2.541222 against the reach row it sat in",
                   "-2.541222", reach_rho8, "pre-e0eba8e prose")
    rows.append(old_ii)
    # the untouched neighbours of the corrected row must still re-derive
    for rho, q in ((6.0, "-2.583087"), (7.0, "-2.557642"), (9.0, "-2.530473")):
        rows.append(check("(ii) reach ladder rho=%g (untouched neighbour)" % rho,
                          q, reach[rho]["ratio"], "TECHNICAL_P2_ROUTEPORT_V1.md sec 2.1"))
    # and the quantities computed FROM that ladder, which leg 60 said were unaffected
    # the "power law in X_max with slope -0.437" is the log-log fit of the DISTANCE TO CHL,
    # |ratio - chl_ratio|, against X_max over the whole reach ladder -- not of the ratio
    # itself.  Identified here by re-deriving it, not by reading leg 46/60's code.
    chl = v1["C_extrapolation"]["chl_ratio"]
    ladder = v1["C_extrapolation"]["reach"]
    slope_reach = float(np.polyfit(
        np.log10([r["X_max"] for r in ladder]),
        np.log10([abs(r["ratio"] - chl) for r in ladder]), 1)[0])
    rows.append(check("(ii) reach power-law slope, RE-FITTED here from the ladder",
                      "-0.437", slope_reach, "TECHNICAL_P2_ROUTEPORT_V1.md sec 2.1"))
    rows.append(check("(ii) extrapolated limit (unaffected, per leg 60)",
                      "-2.511926", v1["C_extrapolation"]["best_limit"],
                      "TECHNICAL_P2_ROUTEPORT_V1.md sec 2.1"))
    rows.append(check("(ii) limit rel err vs CHL (unaffected, per leg 60)",
                      "2.09e-04", v1["C_extrapolation"]["best_limit_err_vs_CHL"],
                      "TECHNICAL_P2_ROUTEPORT_V1.md sec 2.1"))

    # --- correction (iii): the n=1201 gap, 1.168% -> 1.169% ------------------------
    gap_1201_pct = res[1201]["ratio_err_vs_CHL"] * 100.0
    rows.append(check("(iii) n=1201 ratio gap %, CORRECTED value",
                      "1.169", gap_1201_pct, "TECHNICAL_P2_ROUTEPORT_V1.md sec 2"))
    old_iii = check("(iii) OLD literal 1.168 against the same stored value",
                    "1.168", gap_1201_pct, "pre-e0eba8e prose")
    rows.append(old_iii)
    rows.append(check("(iii) headline 1.17% (leg 60: same row, unaffected)",
                      "1.17", gap_1201_pct, "TECHNICAL_P2_ROUTEPORT_V1.md sec 2"))

    # (iii) is a ROUNDING correction, so the honest magnitude is how far the stored value
    # sits from the round-half tie point, in units of the half-ulp it is judged by.
    tie = 1.1685
    hu_iii = half_ulp("1.168")
    tie_margin = gap_1201_pct - tie
    rounding = {
        "stored_pct": gap_1201_pct,
        "tie_point_pct": tie,
        "margin_above_tie_pct": tie_margin,
        "half_ulp_pct": hu_iii,
        "margin_as_fraction_of_half_ulp": tie_margin / hu_iii,
        "rounds_up_under_half_up": bool(tie_margin >= 0.0),
        "rounds_up_under_half_even": bool(tie_margin > 0.0),
        "note": ("1.169 is right under BOTH tie rules, but only because the stored value "
                 "clears the tie by 0.54%% of a half-ulp; a relative perturbation of "
                 "4.6e-06 in the stored gap would flip the corrected digit back."),
    }

    # --- the two BAN-BEARING numbers, which must be exact before AND after ----------
    ban = []
    ban.append(check("BAN-BEARING: distance / r_max (leg 46 clause P6b)",
                     "1.55e+08", v1["E_ceiling"]["distance_over_r_max"],
                     "README item 46 / TECHNICAL_P2_ROUTEPORT_V1.md sec 4"))
    ban.append(check("BAN-BEARING: truncation distance",
                     "1.831e-01", v1["E_ceiling"]["distance"],
                     "TECHNICAL_P2_ROUTEPORT_V1.md sec 4"))
    ban.append(check("BAN-BEARING: ball r_min", "2.97e-12", v1["E_ceiling"]["r_min"],
                     "TECHNICAL_P2_ROUTEPORT_V1.md sec 4"))
    ban.append(check("BAN-BEARING: ball r_max", "1.18e-09", v1["E_ceiling"]["r_max"],
                     "TECHNICAL_P2_ROUTEPORT_V1.md sec 4"))

    # re-fit the wrong-sign trend HERE, from the rungs, not from v2['verdict']
    rho = np.array(sorted(ratio))
    fit_ratio = float(np.polyfit(rho, np.log10([ratio[r] for r in rho]), 1)[0])
    fit_dist = float(np.polyfit(rho, np.log10([rungs[r]["distance"] for r in rho]), 1)[0])
    fit_rmax = float(np.polyfit(rho, np.log10([rungs[r]["r_max"] for r in rho]), 1)[0])
    ban.append(check("BAN-BEARING: wrong-sign trend, RE-FITTED here (leg 47's ban)",
                     "0.4703", fit_ratio, "README item 47 / TECHNICAL_P2_ROUTEPORT_V2.md sec 2"))
    ban.append(check("BAN-BEARING: same slope vs the stored verdict field",
                     "%.10f" % v2["verdict"]["slope_log10_ratio_per_rho"], fit_ratio,
                     "p2_route_port_v2_reach.json verdict"))
    ban.append(check("constituent: distance slope, re-fitted", "-0.0196", fit_dist,
                     "README item 47"))
    ban.append(check("constituent: r_max slope, re-fitted", "-0.4899", fit_rmax,
                     "README item 47"))
    ban.append({
        "label": "BAN-BEARING: slope vs gate", "quoted": "-0.05", "quoted_as_float": -0.05,
        "data": fit_ratio, "abs_err": float("nan"), "half_ulp": float("nan"),
        "half_ulps_out": float("nan"), "rel_err": float("nan"),
        "pass": bool(fit_ratio > -0.05),
        "where": "the ban 'closing the truncation gap by extending the domain'",
    })

    # the three late-rung distances v2 says RISE
    for rho_, q in ((8.0, "0.1836"), (9.0, "0.2049"), (10.0, "0.3306")):
        rows.append(check("late-rung distance rho=%g" % rho_, q, rungs[rho_]["distance"],
                          "TECHNICAL_P2_ROUTEPORT_V2.md sec 2"))

    return rows, ban, rounding, {
        "gap_6_to_10": gap_6_10, "gap_8_to_10": gap_8_10,
        "reach_rho8_n301": reach_rho8, "resolution_n201": res[201]["ratio"],
        "gap_1201_pct": gap_1201_pct,
        "refit_slope_ratio": fit_ratio, "refit_slope_distance": fit_dist,
        "refit_slope_rmax": fit_rmax, "refit_reach_power_law": slope_reach,
        "old_literal_magnitudes": {"i": old_i, "ii": old_ii, "iii": old_iii},
    }


# ---------------------------------------------------------------------------
# V2 -- did the correction propagate?
# ---------------------------------------------------------------------------

# Sites that legitimately still hold the string: the resolution-table row (where -2.541222
# IS the right value), leg 60's own ledger literals, and the audit trail (journals, README's
# own account of the correction, DIRECTION, the JR3 audit JSON quoting the commit message).
LEGIT = re.compile(
    r"(journal/leg_60\.md|journal/leg_168\.md|writeup/README\.md|DIRECTION\.md"
    r"|JOURNAL\.md|p2_route_jr3_v1_journal_audit\.json"
    r"|p2_route_port_v1_bordered_evidence\.py|journal/leg_195\.md"
    r"|p2_route_pqver_v1_verification\.py|novelty/leg_195\.md"
    r"|p2_route_pgf_v1_ledger_audit\.json)")


def clause_v2():
    """Scan the tracked tree for surviving copies of the corrected literals."""
    try:
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.split()
    except Exception as exc:                                    # pragma: no cover
        return {"error": str(exc), "sites": []}

    # `(?<![\d.])` matters: without it `28×` also matches inside `1.428×` and `4.0128×`,
    # which have nothing to do with leg 60.  Caught by re-reading this scan's own output.
    pat = re.compile(r"-?2\.541222|(?<![\d.])1\.168%|(?<![\d.])28×|(?<![\d.])28x worse")
    sites = []
    for rel in tracked:
        if not rel.endswith((".md", ".py", ".json", ".txt")):
            continue
        p = os.path.join(ROOT, rel)
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                sites.append({"file": rel, "line": i, "text": line.strip()[:200],
                              "audit_trail": bool(LEGIT.search(rel))})
    return {"sites": sites}


def classify(scan, v1):
    """Split the scan into stale sites and legitimate ones, and say whether any stale copy
    is consumed as a NUMBER by live code (which would contaminate a downstream result)."""
    reach_rho8 = {r["rho_max"]: r for r in v1["C_extrapolation"]["reach"]}[8.0]["ratio"]
    res201 = {r["n"]: r for r in v1["A_newton_ladder"]["rungs"]}[201]["ratio"]

    stale, legit = [], []
    for s in scan.get("sites", []):
        t = s["text"]
        if s["audit_trail"]:
            legit.append(dict(s, why="audit trail / leg 60's own record"))
            continue
        # the resolution-table use of -2.541222 is CORRECT: it is the n=201 value
        if "2.541222" in t and ("n=201" in t.replace(" ", "") or "| 201 |" in t
                                or "n = 201" in t or "n=201..1201" in t
                                or "n=201..1201" in t.replace(" ", "")):
            legit.append(dict(s, why="correct use: -2.541222 IS the n=201 resolution row"))
            continue
        if "2.541222" in t and "/" in t:
            # a reach ladder 6/7/8/9 -> ... quoting -2.541222 in the rho=8 slot: STALE
            stale.append(dict(
                s, why="reach ladder rho=8 slot still holds the corrected-away literal",
                should_be=-2.541024, data_value=reach_rho8,
                abs_err=abs(-2.541222 - reach_rho8),
                rel_err=abs(-2.541222 - reach_rho8) / abs(reach_rho8),
                half_ulps_out=abs(-2.541222 - reach_rho8) / half_ulp("-2.541024"),
                consumed_as_a_number=bool(s["file"].endswith(".py")
                                          and not t.lstrip().startswith("#")),
            ))
            continue
        stale.append(dict(s, why="unclassified surviving literal"))

    return {
        "stale": stale, "legit": legit,
        "n_stale": len(stale), "n_legit": len(legit),
        "n_stale_consumed_as_a_number": sum(
            1 for s in stale if s.get("consumed_as_a_number")),
        "resolution_n201_value": res201, "reach_rho8_value": reach_rho8,
    }


# ---------------------------------------------------------------------------

def main():
    v1, v2 = load()
    rows, ban, rounding, derived = clause_v1(v1, v2)
    scan = clause_v2()
    prop = classify(scan, v1)

    print("=" * 92)
    print("LEG 195 / ROUTE-PQVER — independent verification of leg 60 (%s)" % LEG60_COMMIT)
    print("=" * 92)

    print("\nCLAUSE V1(a) — the three corrected numbers, re-derived from the curated JSON")
    print("-" * 92)
    for r in rows:
        print("  [%s] %-58s prose %14s   data %14.6g   %s"
              % ("PASS" if r["pass"] else "FAIL", r["label"], r["quoted"], r["data"],
                 ("|err| %.2e vs half-ulp %.1e  (%.3g half-ulps)"
                  % (r["abs_err"], r["half_ulp"], r["half_ulps_out"]))))

    print("\nCLAUSE V1(b) — the ban-bearing numbers, exact before and after")
    print("-" * 92)
    for r in ban:
        tail = ("" if r["abs_err"] != r["abs_err"] else
                "|err| %.2e vs half-ulp %.1e  (%.3g half-ulps)"
                % (r["abs_err"], r["half_ulp"], r["half_ulps_out"]))
        print("  [%s] %-58s prose %14s   data %14.6g   %s"
              % ("PASS" if r["pass"] else "FAIL", r["label"], r["quoted"], r["data"], tail))

    print("\n  correction (iii) is a ROUNDING call — its margin, not its boolean:")
    print("    stored %.10f%%   tie %.4f%%   margin above tie %.3e pp"
          % (rounding["stored_pct"], rounding["tie_point_pct"],
             rounding["margin_above_tie_pct"]))
    print("    that is %.2f%% of one half-ulp; 1.169 holds under half-up AND half-even, but "
          "a\n    relative perturbation of 4.6e-06 in the stored gap would flip it back to "
          "1.168."
          % (100.0 * rounding["margin_as_fraction_of_half_ulp"]))

    n_all = len(rows) + len(ban)
    n_pass = sum(1 for r in rows + ban if r["pass"])
    # the three OLD literals are EXPECTED to fail — they are the errors leg 60 removed
    expected_fail = [r for r in rows if r["label"].startswith(("(i) OLD", "(ii) OLD",
                                                              "(iii) OLD"))]
    unexpected = [r for r in rows + ban if not r["pass"] and r not in expected_fail]

    print("\n  %d/%d rows PASS.  %d of the failures are the OLD literals, which MUST fail — "
          "they are\n  the errors leg 60 removed:" % (n_pass, n_all, len(expected_fail)))
    for r in expected_fail:
        print("    OLD %-10s off by %.3e absolute, rel %.2e, %.4g half-ulps"
              % (r["quoted"], r["abs_err"], r["rel_err"], r["half_ulps_out"]))
    v1_verdict = not unexpected
    print("\n  CLAUSE V1: %s — %d unexpected failure(s)."
          % ("YES, independently confirmed" if v1_verdict else "NO", len(unexpected)))
    for r in unexpected:
        print("    FAIL %s: prose %s vs data %.10g, %.4g half-ulps out"
              % (r["label"], r["quoted"], r["data"], r["half_ulps_out"]))

    print("\nCLAUSE V2 — did the correction propagate through the tracked tree?")
    print("-" * 92)
    print("  %d site(s) still hold a corrected-away literal legitimately (audit trail, or "
          "the\n  n=201 resolution row where -2.541222 is the RIGHT value)." % prop["n_legit"])
    print("  %d STALE site(s):" % prop["n_stale"])
    for s in prop["stale"]:
        print("    %s:%d  %s" % (s["file"], s["line"], s["why"]))
        print("        %s" % s["text"][:150])
        if "abs_err" in s:
            print("        should read %.6f; off by %.3e absolute, rel %.2e, %.0f half-ulps"
                  " | consumed as a number: %s"
                  % (s["should_be"], s["abs_err"], s["rel_err"], s["half_ulps_out"],
                     s.get("consumed_as_a_number")))
    v2_verdict = prop["n_stale"] == 0
    print("\n  CLAUSE V2: %s — %d stale copy/copies, %d of them consumed as a number by live "
          "code." % ("YES, complete" if v2_verdict else "NO, incomplete",
                     prop["n_stale"], prop["n_stale_consumed_as_a_number"]))

    payload = {
        "leg": 195, "route": "PQVER", "role": "VERIFY",
        "verifies_commit": LEG60_COMMIT,
        "verifies_claim": ("Leg 60's landed user-approved correction of Route-PORT v1/v2: "
                           "28x->63x, -2.541222->-2.541024, 1.168%->1.169%, with both "
                           "ban-bearing numbers exact before and after and both evidence "
                           "scripts reporting CLEAN 114/114"),
        "independence": ("no import, exec or copy of leg 60's evidence scripts; half-ulp "
                         "rule re-implemented on decimal; v2 slopes re-fitted with polyfit "
                         "rather than read from the stored verdict fields"),
        "clause_V1_correction_confirmed": v1_verdict,
        "clause_V2_correction_complete": v2_verdict,
        "rows": rows, "ban_bearing": ban,
        "rounding_margin_correction_iii": rounding,
        "derived": derived,
        "propagation_audit": prop,
        "expected_failures_are_the_old_literals": [r["label"] for r in expected_fail],
        "unexpected_failures": [r["label"] for r in unexpected],
        "leg60_reported_magnitudes_rechecked": {
            "i_relative_1.25": derived["old_literal_magnitudes"]["i"]["rel_err"],
            "i_half_ulps_70": derived["old_literal_magnitudes"]["i"]["half_ulps_out"],
            "ii_abs_1.98e-04": derived["old_literal_magnitudes"]["ii"]["abs_err"],
            "ii_relative_7.8e-05": derived["old_literal_magnitudes"]["ii"]["rel_err"],
            "ii_half_ulps_395": derived["old_literal_magnitudes"]["ii"]["half_ulps_out"],
            "iii_abs_5.03e-06_in_percent_points":
                derived["old_literal_magnitudes"]["iii"]["abs_err"],
            "iii_relative_4.3e-04": derived["old_literal_magnitudes"]["iii"]["rel_err"],
            "iii_half_ulps_1.0": derived["old_literal_magnitudes"]["iii"]["half_ulps_out"],
            "understatement_factor_of_the_old_28x": derived["gap_6_to_10"] / 28.0,
        },
    }
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote %s" % os.path.relpath(OUT, ROOT))

    print("\n" + "=" * 92)
    print("VERDICT: V1 %s / V2 %s"
          % ("CONFIRMED" if v1_verdict else "GAP", "COMPLETE" if v2_verdict else "GAP"))
    print("=" * 92)
    return 0 if v1_verdict else 1


if __name__ == "__main__":
    sys.exit(main())
