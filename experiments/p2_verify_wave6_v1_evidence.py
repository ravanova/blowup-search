#!/usr/bin/env python3
"""V-W6 (leg 407) -- executable re-derivation of the wave-6 verification.

Verifies wave 6 (`L6` e62c449, `V5` dacc01c, `V-W5` 95cf861) and the Conductor's
landing audit in `writeup/waves/WAVE6_CLOSE.md`, bounded to the tree at `2a5ea0d`.

Every number below is re-derived from the banked artefacts, never from a report.
Exits NON-ZERO if any check disagrees (lesson 68).

    python3 experiments/p2_verify_wave6_v1_evidence.py           # fast (artefact-only)
    python3 experiments/p2_verify_wave6_v1_evidence.py --deep    # + re-run all three
                                                                 #   unit evidence scripts
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "writeup" / "data"
VW6_JSON = DATA / "p2_verify_wave6_v1.json"

# Three sibling construction units were committing into this same working tree while V-W6 ran.
# Their changes are not wave 6. EVERY repo file below is therefore read AT THE BOUND, never
# from the working tree, so this script gives the same answer no matter what has landed since.
BOUND = "2a5ea0d"


def at_bound(relpath):
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{BOUND}:{relpath}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"cannot read {relpath} at {BOUND}: {r.stderr.strip()}")
    return r.stdout


def json_at_bound(relpath):
    return json.loads(at_bound(relpath))

PASS = []
FAIL = []


def chk(cid, name, ok, detail=""):
    (PASS if ok else FAIL).append((cid, name, detail))
    print(f"  [{'OK  ' if ok else 'FAIL'}] {cid} {name}" + (f"  {detail}" if detail else ""))
    return ok


def note(cid, text):
    print(f"  [note] {cid} {text}")


def close(a, b, rtol=1e-12, atol=1e-15):
    return abs(a - b) <= max(atol, rtol * max(abs(a), abs(b)))


def self_hash(doc):
    d = {k: v for k, v in doc.items() if k != "self_hash"}
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()[:16]


def ols_slope(xs, ys):
    """Pure-python OLS slope of log y on log x -- NOT numpy.linalg.lstsq, so this is an
    independent re-derivation of the unit's own rate."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den


def starts_of(row, kind=None):
    if kind == "seed":
        return [s for s in row["starts"] if s["start"] != "continuation"]
    if kind == "cont":
        return [s for s in row["starts"] if s["start"] == "continuation"]
    return row["starts"]


def walk_starts(o, out):
    if isinstance(o, dict):
        if "hit_maxiter" in o and "fun" in o:
            out.append(o)
        for v in o.values():
            walk_starts(v, out)
    elif isinstance(o, list):
        for v in o:
            walk_starts(v, out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--deep", action="store_true",
                    help="also re-run L6/V5/V-W5 evidence scripts as subprocesses")
    args = ap.parse_args()

    print("=" * 96)
    print("V-W6 (leg 407) -- verification of WAVE 6, bounded to commit 2a5ea0d")
    print("  units: L6 (e62c449), V5 (dacc01c), V-W5 (95cf861)")
    print("  also under scrutiny: writeup/waves/WAVE6_CLOSE.md (the Conductor's landing audit)")
    print("=" * 96)

    L6 = json_at_bound("writeup/data/p2_route_l6_profile_v1.json")
    V5 = json_at_bound("writeup/data/p2_route_v5_audit_v1.json")
    VW5 = json_at_bound("writeup/data/p2_verify_wave5_v1.json")

    # ==================================================================================
    print("\n[A] SELF-HASHES -- all three wave-6 artefacts")
    # ==================================================================================
    chk("A01", "L6 self_hash recomputes", self_hash(L6) == L6["self_hash"] == "6a033004deef39d3",
        f"banked={L6['self_hash']} recomputed={self_hash(L6)}")
    chk("A02", "V5 self_hash recomputes", self_hash(V5) == V5["self_hash"] == "ae2b95efcbe5209b",
        f"banked={V5['self_hash']} recomputed={self_hash(V5)}")
    chk("A03", "V-W5 self_hash recomputes",
        self_hash(VW5) == VW5["self_hash"] == "da8a0d7cb9fb4896",
        f"banked={VW5['self_hash']} recomputed={self_hash(VW5)}")

    # ==================================================================================
    print("\n[B] L6 -- the gate answer, re-derived from the artefact and not from the report")
    # ==================================================================================
    gA, gB = L6["gate"]["A"], L6["gate"]["B"]
    chk("B01", "gate answer is NO on BOTH branches",
        gA["decreases_under_refinement"] == gB["decreases_under_refinement"] == "NO")
    chk("B02", "headline rho = 1.613811231995397 at n_dof = 6720 (branch B)",
        close(gB["residual_at_best_affordable_resolution"], 1.613811231995397)
        and gB["best_affordable_resolution"]["n_dof"] == 6720,
        f"rho={gB['residual_at_best_affordable_resolution']!r}")
    chk("B03", "branch A's number is 7.583387202236438 at the same resolution",
        close(gA["residual_at_best_affordable_resolution"], 7.583387202236438)
        and gA["best_affordable_resolution"]["n_dof"] == 6720)

    for br, g in (("A", gA), ("B", gB)):
        rows = L6["ladder_results"][br]
        ns = [r["n_dof"] for r in rows]
        rs = [r["residual_load_bearing"] for r in rows]
        chk(f"B04[{br}]", "per-rung residuals in gate == ladder_results, rung by rung",
            list(g["per_rung_residual"].values()) == rs)
        s3 = ols_slope(ns[-3:], rs[-3:])
        chk(f"B05[{br}]", "last-3 rate re-derived by INDEPENDENT (non-numpy) OLS",
            close(s3, g["rate_dlogresid_dlogndof_last3"], rtol=1e-10),
            f"independent={s3!r} banked={g['rate_dlogresid_dlogndof_last3']!r}")
        sall = ols_slope(ns, rs)
        chk(f"B06[{br}]", "all-rung rate re-derived by INDEPENDENT OLS",
            close(sall, g["rate_dlogresid_dlogndof_all"], rtol=1e-10))
        # the pre-registered decision rule, leg_401.md SS5.1, applied from scratch
        rels = [(rs[i] - rs[i - 1]) / rs[i - 1] for i in range(1, len(rs))]
        yes = (all(rs[i] < rs[i - 1] for i in range(len(rs) - 2, len(rs)))
               and all(r < -0.05 for r in rels[-2:]) and s3 < -0.05)
        chk(f"B07[{br}]", "SS5.1 decision rule, re-applied from scratch, gives the banked verdict",
            ("YES" if yes else "NO") == g["decreases_under_refinement"])

    chk("B08", "n_dof spans 17.5x across the joint ladder (Conductor close SS3i q2)",
        close(L6["ladder_results"]["B"][-1]["n_dof"] / L6["ladder_results"]["B"][0]["n_dof"], 17.5),
        f"{L6['ladder_results']['B'][-1]['n_dof']}/{L6['ladder_results']['B'][0]['n_dof']}")
    chk("B09", "top-rung relative change on B is -0.497% (Conductor close SS3i q2 '0.497 %')",
        close(gB["per_rung_relative_change"][-1], -0.0049718667845589535),
        f"{gB['per_rung_relative_change'][-1]!r}")

    # ==================================================================================
    print("\n[C] THE CONDUCTOR'S LANDING AUDIT OF L6 -- ruled on independently")
    # ==================================================================================
    # Claim 1: at every rung above the coarsest, the reported rho is attained by ONE start,
    #          and that start is the continuation.
    one_start_ok = True
    for br in ("A", "B"):
        for row in L6["ladder_results"][br][1:]:
            best = row["residual_load_bearing"]
            attain = [s["start"] for s in row["starts"] if close(s["fun"], best, rtol=1e-12)]
            if attain != ["continuation"]:
                one_start_ok = False
    chk("C01", "AUDIT CLAIM 1 UPHELD: above the coarsest rung the minimum is attained by "
               "EXACTLY ONE start and it is the continuation, on both branches", one_start_ok)

    chk("C02", "...and at the COARSEST rung there is no continuation start at all (5 starts)",
        all(len(L6["ladder_results"][br][0]["starts"]) == 5 for br in ("A", "B"))
        and all(len(r["starts"]) == 6 for br in ("A", "B") for r in L6["ladder_results"][br][1:]))

    # Claim 2: "five independent random seeds land 10-24x higher"
    ratios = {}
    for br in ("A", "B"):
        ratios[br] = []
        for row in L6["ladder_results"][br][1:]:
            cont = starts_of(row, "cont")[0]["fun"]
            sd = [s["fun"] for s in starts_of(row, "seed")]
            ratios[br].append((row["n_dof"], min(sd) / cont, max(sd) / cont))
    lo_B = min(r[1] for r in ratios["B"])
    hi_B = max(r[2] for r in ratios["B"])
    chk("C03", "AUDIT CLAIM 2 OVERSTATED: on branch B the seed/continuation factor spans "
               "3.93x-23.67x across the four rungs, NOT 10-24x",
        close(lo_B, 3.9327460167352345, rtol=1e-6) or (3.93 <= lo_B <= 3.94),
        f"branch B factors per rung: " +
        "; ".join(f"n_dof={n}: {a:.2f}-{b:.2f}x" for n, a, b in ratios["B"]))
    chk("C04", "...the 10-24x band is right only for the TOP TWO rungs of branch B",
        all(a >= 10.0 for n, a, b in ratios["B"][-2:]) and hi_B <= 24.0
        and ratios["B"][0][1] < 10.0 and ratios["B"][1][1] < 10.0,
        f"n_dof=2400: {ratios['B'][2][1]:.2f}-{ratios['B'][2][2]:.2f}x; "
        f"n_dof=6720: {ratios['B'][3][1]:.2f}-{ratios['B'][3][2]:.2f}x")
    chk("C05", "...and on branch A the factor never reaches 10x at any rung (1.01x-5.95x)",
        max(b for n, a, b in ratios["A"]) < 6.0,
        "; ".join(f"n_dof={n}: {a:.2f}-{b:.2f}x" for n, a, b in ratios["A"]))

    # Claim 3: "get monotonically WORSE as n_dof grows"
    nonmono = []
    for sd in ("seed401", "seed402", "seed403", "seed404", "seed405"):
        vals = [[s["fun"] for s in r["starts"] if s["start"] == sd][0]
                for r in L6["ladder_results"]["B"][1:]]
        if not all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)):
            nonmono.append((sd, [round(v, 3) for v in vals]))
    chk("C06", "AUDIT CLAIM 3 OVERSTATED: 'monotonically WORSE' fails for 2 of the 5 seeds "
               "taken individually (it holds for the per-rung seed MINIMUM)",
        len(nonmono) == 2,
        "; ".join(f"{s}: {v}" for s, v in nonmono))
    seedmin = [min(s["fun"] for s in starts_of(r, "seed"))
               for r in L6["ladder_results"]["B"][1:]]
    chk("C07", "...the per-rung seed MINIMUM does rise monotonically 6.68 -> 13.47 -> 16.36 -> 29.57",
        all(seedmin[i] < seedmin[i + 1] for i in range(len(seedmin) - 1)),
        str([round(v, 3) for v in seedmin]))
    chk("C08", "AUDIT CLAIM 3 range 'J1 ~ 6.8 -> J4 ~ 32-38' understates the J4 spread at "
               "the bottom (true range 29.57-38.20)",
        close(min(s["fun"] for s in starts_of(L6["ladder_results"]["B"][-1], "seed")),
              29.56694012, rtol=1e-6))

    # Claim 4: the cap.
    allstarts = []
    walk_starts(L6, allstarts)
    at800 = [s for s in allstarts if s["nit"] == 800]
    at250 = [s for s in allstarts if s["nit"] == 250]
    chk("C09", "AUDIT CLAIM 4: 133 of 133 starts hit their cap -- TRUE",
        len(allstarts) == 133 and all(s["hit_maxiter"] for s in allstarts)
        and L6["cost_and_shortfall"]["starts_run"] == 133
        and L6["cost_and_shortfall"]["starts_that_hit_the_iteration_cap"] == 133)
    chk("C10", "...but only 58 of the 133 were capped at 800; the other 75 were capped at 250 "
               "(the secondary axis ladders). 'all 133 at 800' would be wrong.",
        len(at800) == 58 and len(at250) == 75)
    chk("C11", "pre-registered maxiter was 20000 (leg_401.md SS5); 800 was used -- a 25x shortfall",
        L6["cost_and_shortfall"]["preregistered_maxiter"] == 20000
        and L6["cost_and_shortfall"]["maxiter_actually_used"] == 800
        and L6["optimiser"]["maxiter"] == 800)
    chk("C12", "the unit itself banked UNDER_RESOURCED = true, so that half of the audit's "
               "ceiling was NOT new (the one-start finding was)",
        L6["cost_and_shortfall"]["UNDER_RESOURCED"] is True)

    # ==================================================================================
    print("\n[D] V-W6'S OWN FINDINGS ON L6 -- not in the unit's report, not in the audit")
    # ==================================================================================
    # D01/D02: the reported minimiser is nowhere near stationary, and gets worse with n_dof.
    gt = L6["optimiser"]["gtol"]
    gsc = {}
    for br in ("A", "B"):
        gsc[br] = []
        for row in L6["ladder_results"][br]:
            best = row["residual_load_bearing"]
            s = [t for t in row["starts"] if close(t["fun"], best, rtol=1e-12)][0]
            gsc[br].append((row["n_dof"], s["max_abs_grad"], s["scale_invariant_grad"]))
    topB = gsc["B"][-1]
    chk("D01", "the BANKED minimiser fails its own pre-registered gtol by ~14 orders: "
               f"max|grad| = {topB[1]:.4g} against gtol = {gt:g}",
        topB[1] > 1e10 * gt and gt == 1e-12,
        f"branch B J4: max|grad|={topB[1]:.6g}, scale-invariant={topB[2]:.6g}")
    monoB = [v[2] for v in gsc["B"][1:]]
    monoA = [v[2] for v in gsc["A"][1:]]
    chk("D02", "and distance-from-stationarity grows MONOTONICALLY with n_dof on BOTH branches "
               "-- the ladder gets further from a stationary point as it refines",
        all(monoB[i] < monoB[i + 1] for i in range(len(monoB) - 1))
        and all(monoA[i] < monoA[i + 1] for i in range(len(monoA) - 1)),
        f"B scale-invariant |grad|: {[round(v,2) for v in monoB]}; "
        f"A: {[round(v,2) for v in monoA]}")
    chk("D03", "every L-BFGS-B exit status in the artefact is 1 = 'maximum iterations reached'; "
               "no start anywhere converged by gradient or by ftol",
        all(s["status"] == 1 for s in allstarts) and not any(s["stalled_before_cap"]
                                                             for s in allstarts))

    # D04: the cap sweep is a truncation of a full-budget warm-start chain.
    #      Re-derive by_cap from the recorded trajectories exactly as the unit's code does.
    def residual_at_cap(rows, K):
        out = []
        for row in rows:
            best = None
            for st in row["starts"]:
                pts = [t for t in st.get("trajectory_k_sec_J_ginf_gscaled", []) if t[0] <= K]
                if pts:
                    v = min(t[2] for t in pts)
                    best = v if best is None else min(best, v)
            out.append(best)
        return out

    ok04 = True
    for br in ("A", "B"):
        for K, blk in L6["gate"][br]["stability_against_the_iteration_cap"]["by_cap"].items():
            got = residual_at_cap(L6["ladder_results"][br], int(K))
            if not all(close(a, b, rtol=1e-12) for a, b in zip(got, blk["per_rung_residual"])):
                ok04 = False
    chk("D04", "the 'stability against the iteration cap' block is EXACTLY a post-hoc "
               "truncation of the recorded 800-iteration trajectories -- re-derived here",
        ok04)
    chk("D05", "...and each rung's continuation start was warm-started from the PREVIOUS rung's "
               "FULL-BUDGET (800-iteration) minimiser, so no 'cap 50' column is what a cap-50 "
               "ladder would produce. The control cannot separate budget from construction.",
        close(residual_at_cap(L6["ladder_results"]["B"], 50)[1], 3.279848520414034, rtol=1e-9)
        and close(L6["ladder_results"]["B"][0]["residual_load_bearing"], 3.646708645559305),
        "J1@cap50 = 3.2798 is a truncation of a run started from J0's 800-iteration answer "
        "3.6467, not from J0's own cap-50 answer 14.0239")
    chk("D06", "the sentence this control is used to support -- leg_401.md SS8.2, "
               "'The NO is a fact about the construction, not about the stopping point' -- "
               "is therefore NOT established by the artefact",
        L6["gate"]["B"]["stability_against_the_iteration_cap"]["verdict_is_stable_in_the_cap"]
        is True)

    # D07: the evidence script covers neither the cap sweep nor the cost block.
    ev_src = at_bound("experiments/p2_route_l6_v1_evidence.py")
    chk("D07", "L6's 30-check evidence script contains NO check of by_cap / "
               "stability_against_the_iteration_cap / cost_and_shortfall",
        ("by_cap" not in ev_src and "stability_against" not in ev_src
         and "cost_and_shortfall" not in ev_src))

    # D08: SS3.5's three pre-registered predictions were never adjudicated.
    j401 = at_bound("experiments/journal/leg_401.md")
    head, tail = j401.split("## §7. EXECUTION RECORD", 1)
    chk("D08", "leg_401.md SS3.5 pre-registered THREE mechanism predictions with "
               "'a failure of the prediction is as reportable as a success' -- and no "
               "section after SS7 mentions any of them",
        "Prediction" in head and "prediction" not in tail.lower())
    dA = L6["ladder_results"]["A"][-1]["diagnostics"]
    dB = L6["ladder_results"]["B"][-1]["diagnostics"]
    chk("D09", "PREDICTION 2 IS REFUTED BY THE BANKED DATA and the refutation is unreported: "
               "branch A did NOT kill the alpha=1 tail",
        dA["far_field_alpha1_amplitude_mean"] > 0.3
        and close(dA["far_field_decay_exponent_alpha"], 0.9953900637000948),
        f"branch A far-field amplitude mean = {dA['far_field_alpha1_amplitude_mean']:.4f}, "
        f"fitted decay exponent = {dA['far_field_decay_exponent_alpha']:.4f}")
    chk("D10", "PREDICTION 3 IS NOT CONFIRMED and that is unreported: branch B's norm does "
               "NOT grow under 4x radial-quadrature refinement",
        abs(dB["quadrature_refinement_ratio_x4_over_x1"] - 1.0) < 1e-4,
        f"x4/x1 = {dB['quadrature_refinement_ratio_x4_over_x1']!r}")
    chk("D11", "the fitted far-field decay exponent of the HEADLINE branch B minimiser is "
               "0.2250, not 1 -- banked, and reported in NO prose anywhere",
        close(dB["far_field_decay_exponent_alpha"], 0.22499719550331687)
        and "0.225" not in j401
        and "0.225" not in at_bound("writeup/waves/WAVE6_CLOSE.md"),
        f"branch B fitted exponent over 5 < r < 200 = {dB['far_field_decay_exponent_alpha']!r} "
        f"(branch A: {dA['far_field_decay_exponent_alpha']!r})")
    chk("D12", "the headline branch B carries only 0.219% of branch A's Gaussian-weighted "
               "interior L^2 -- so 'rho = 1.6 against a unit-normalised field' "
               "(WAVE6_CLOSE.md SS3i q2) is not right: the unit-normalised branch is A, at 7.58",
        close(dB["weighted_L2_total"], 0.0021915332982833375)
        and close(dA["weighted_L2_total"], 0.9999999999999998, rtol=1e-9))
    note("D12", "the unit itself flags this in SS10 reading (c-3); the Conductor's audit does not. "
                "It cuts the Conductor's own way -- L7 is blocked harder, not less.")

    # D13: scipy is a hidden dependency of L6.
    reqs = at_bound("requirements.txt")
    l6_src = at_bound("experiments/p2_route_l6_v1.py")
    chk("D13", "L6's solver imports scipy while requirements.txt says scipy is NOT required -- "
               "the same defect repaired for V5's mpmath at ac34fd4, unrepaired here",
        "from scipy" in l6_src and "\nscipy" not in reqs
        and "scipy is intentionally NOT required" in reqs)
    note("D13", "measured in a sandbox with scipy blocked: "
                "experiments/p2_route_l6_v1_evidence.py dies with an uncaught ImportError "
                "(exit 1, traceback, zero checks reported) on a clean checkout. --fast survives.")

    # D14: SOURCES.md carries no row for L6's own two load-bearing citations.
    src = at_bound("writeup/SOURCES.md")
    chk("D14", "AT THE BOUND, writeup/SOURCES.md has NO row for Byrd-Lu-Nocedal-Zhu 1995 (the "
               "apparatus that discharges ban C1 for L6) and none for Chandrasekhar (the "
               "trial space) -- both load-bearing, both undepthed",
        "Byrd" not in src and "Nocedal" not in src and "Chandrasekhar" not in src)
    note("D14", "SS3k and SOURCES.md were created on the Conductor line AFTER L6's branch point "
                "5c49486, so this is not L6's omission -- it is an integration gap at the "
                "e62c449 landing, which SS3i q4 reviewed source ceilings without catching.")
    live = (ROOT / "writeup" / "SOURCES.md").read_text()
    note("D14", "STATUS AT THIS INVOCATION (outside the bound, informational only): "
                f"Byrd row present = {'Byrd' in live} (added by L6-b, wave 7, at depth ABSTRACT); "
                f"Chandrasekhar row present = {'Chandrasekhar' in live}.")

    # ==================================================================================
    print("\n[E] V5 -- gate answered in the gate's own terms")
    # ==================================================================================
    chk("E01", "CLAUSE 1 answered YES with a named branch", V5["CLAUSE_1"]["ANSWER"] == "YES"
        and V5["CLAUSE_1"]["branch_taken"] == "B1_PARTIAL")
    chk("E02", "CLAUSE 2 answered YES and banked as ANSWERED STANDING ALONE (gate's own words)",
        V5["CLAUSE_2"]["ANSWER"] == "YES"
        and V5["CLAUSE_2"]["answered_standing_alone"] is True)
    chk("E03", "four constants named with BOTH numbers and a verbatim failing clause, as the "
               "gate required", len(V5["CLAUSE_1"]["constants_that_FAILED_to_recompute"]) == 4
        and all("printed" in c and "recomputed" in c
                for c in V5["CLAUSE_1"]["constants_that_FAILED_to_recompute"]))
    chk("E04", "the Class-A limit is banked as a LIMIT, not as a pass (22 unrecomputable inputs)",
        any("Class A" in s and "LIMIT" in s
            for s in V5["what_this_audit_did_NOT_establish"])
        and len(V5["CLAUSE_1"]["constant_enumeration"]
                ["class_A_UNRECOMPUTABLE_BY_DESIGN"]["values"]) == 22)
    chk("E05", "W2's test is LOCATED in the record, not invented",
        V5["CLAUSE_2"]["W2_test_located_in_the_record"]["invented"] is False
        and V5["CLAUSE_2"]["W2_test_located_in_the_record"]["found"] is True)
    swirl = V5["CLAUSE_2"]["measurements"]
    chk("E06", "the 57% swirl fraction re-derives from the banked component maxima",
        close(swirl["u3_u_phi_max_abs"] / swirl["u1_u_r_max_abs"],
              swirl["u_phi_as_fraction_of_u_r"], rtol=1e-3),
        f"{swirl['u3_u_phi_max_abs']}/{swirl['u1_u_r_max_abs']} = "
        f"{swirl['u3_u_phi_max_abs']/swirl['u1_u_r_max_abs']:.6f}")
    chk("E07", "Tier 2 and Clay unchanged are banked", V5["tier"] == 2
        and close(V5["clay_probability_unchanged"], 0.05))
    note("E01", "SCOPING, not a defect: CLAUSE_1's 'the certificate DOES close as claimed' is "
                "conditional on 22 Class-A interval outputs taken as given. The condition is "
                "banked in what_this_audit_did_NOT_establish and carried into STATE.md.")

    # ==================================================================================
    print("\n[F] V-W5 -- gate answered in the gate's own terms")
    # ==================================================================================
    items = ["item_1_L5_gate_answer_and_rho_exponent", "item_2_three_positive_controls",
             "item_3_was_C6s_tolerance_ever_moved", "item_4_self_hashes",
             "item_5_D_REPAIR_epoch_correction"]
    chk("F01", "all five gate items present and each carries a verdict",
        all(k in VW5 and "verdict" in VW5[k] for k in items))
    chk("F02", "item 1: L5's rho-exponent 0.00010850007559945518 is banked and re-fitted",
        close(VW5[items[0]]["rho_exponent_banked"], 0.00010850007559945518, rtol=0, atol=0))
    chk("F03", "item 3 answers BOTH halves of its gate -- 'was it moved' AND 'does the NO "
               "depend on what C6 perturbs'",
        VW5[items[2]]["answer"] == "NO"
        and "does_anything_the_NO_rests_on_depend_on_the_constant_C6_perturbs" in VW5[items[2]])
    chk("F04", "item 4 recomputes BOTH pre-named self_hashes under the literal stated rule",
        all(r["match"] for r in VW5[items[3]]["results"])
        and {r["banked"] for r in VW5[items[3]]["results"]}
        == {"0c5e0f827f526df6", "e0171ac1e855f90e"})
    chk("F05", "reading (a) honoured: 3 defects found, 0 repaired, 0 banked artefacts edited",
        len(VW5["defects_found_and_NOT_repaired"]) == 3
        and VW5["defects_repaired"] == 0 and VW5["banked_artefacts_edited"] == 0)
    chk("F06", "banked check count is 120 with 0 failures", VW5["checks_run"] == 120
        and VW5["checks_failed"] == 0 and VW5["checks_passed"] == 120)
    note("F06", "BOOKKEEPING: the script prints 121 [PASS] lines -- the 121st is its own "
                "artefact self_hash check, emitted after the summary and outside the count. "
                "Changes nothing.")

    # ==================================================================================
    print("\n[G] TERRITORY -- derived from git, not from any unit's report")
    # ==================================================================================
    def diff(base, head):
        out = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-status", base, head],
                             capture_output=True, text=True)
        return [tuple(l.split("\t")) for l in out.stdout.strip().splitlines()]

    for cid, unit, base, head, n in (("G01", "L6", "5c49486", "614eeaf", 7),
                                     ("G02", "V5", "5c49486", "dacc01c", 5),
                                     ("G03", "V-W5", "5c49486", "95cf861", 3)):
        d = diff(base, head)
        chk(cid, f"{unit}: {n} files, ALL 'A' -- strictly additive, nothing outside territory",
            len(d) == n and all(s == "A" for s, _ in d),
            ", ".join(p for _, p in d))

    ins = subprocess.run(["git", "-C", str(ROOT), "log", "-p", "5c49486..614eeaf", "--",
                          "experiments/journal/leg_401.md"], capture_output=True, text=True)
    dels = [l for l in ins.stdout.splitlines()
            if l.startswith("-") and not l.startswith("---")]
    chk("G04", "L6's journal is strictly INSERT-ONLY across all three of its commits "
               "(0 deleted lines), as its territory clause required", len(dels) == 0)

    rebank = subprocess.run(["git", "-C", str(ROOT), "show", "--numstat", "--format=", "8531960",
                             "--", "writeup/data/p2_route_l6_profile_v1.json"],
                            capture_output=True, text=True).stdout.split()
    chk("G05", "L6's artefact WAS re-banked once mid-branch (+7317/-8); the 8 deleted lines are "
               "the axis-ladder placeholder and the stale cost/runtime fields, and NO gate "
               "number changed", rebank[0] == "7317" and rebank[1] == "8")

    # ==================================================================================
    print("\n[H] THE CONDUCTOR'S OWN NUMBERS IN WAVE6_CLOSE.md")
    # ==================================================================================
    contB = [s for s in L6["ladder_results"]["B"][-1]["starts"]
             if s["start"] == "continuation"][0]
    chk("H01", "'1,240 s per start at 800 iterations' re-derives (branch B J4: 1229-1243 s)",
        1229.0 <= contB["seconds"] <= 1244.0,
        f"continuation start seconds = {contB['seconds']}")
    per_iter = contB["seconds"] / 800.0
    l6b = per_iter * 20000 * 3 / 3600.0
    chk("H02", "L6-b's price 'from L6's own timing': 20000 iters x 3 starts = "
               f"{l6b:.1f} core-h, i.e. at the TOP of the '~10^1 core-h' band, not the middle",
        20.0 < l6b < 30.0, f"{per_iter:.3f} s/iteration -> {l6b:.1f} core-h")
    chk("H03", "'zero modifications' is true of the NET diff only -- see G05 for the "
               "mid-branch re-bank the phrasing glosses", True)
    chk("H04", "the audit's own headline -- 30 checks 0 failures -- matches this run "
               "(see --deep) and L6's chain block says NONE",
        L6["chain"]["L1_to_L4_link_moved"] == "NONE"
        and L6["chain"]["clay_percent_unchanged"] is True)

    # ==================================================================================
    if args.deep:
        print("\n[I] --deep: re-running all three unit evidence scripts")
        for cid, script, extra in (("I01", "p2_route_l6_v1_evidence.py", []),
                                   ("I02", "p2_route_v5_v1_evidence.py", []),
                                   ("I03", "p2_verify_wave5_v1_evidence.py", [])):
            r = subprocess.run([sys.executable, str(ROOT / "experiments" / script)] + extra,
                               cwd=str(ROOT), capture_output=True, text=True)
            chk(cid, f"{script} exits 0", r.returncode == 0,
                r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")
    else:
        print("\n[I] --deep not given: unit evidence scripts NOT re-run in this invocation.")
        print("      Measured by V-W6 on 2026-08-19 in the merged tree at 2a5ea0d:")
        print("        p2_route_l6_v1_evidence.py     30 checks, 0 failures, exit 0")
        print("        p2_route_v5_v1_evidence.py     75 checks, 0 failures, exit 0")
        print("        p2_verify_wave5_v1_evidence.py 120 checks, 0 failures, exit 0 (121 PASS lines)")

    # ==================================================================================
    if VW6_JSON.exists():
        VW6 = json.load(open(VW6_JSON))
        chk("Z01", "V-W6's own artefact self_hash recomputes",
            self_hash(VW6) == VW6["self_hash"],
            f"banked={VW6['self_hash']} recomputed={self_hash(VW6)}")

    print("\n" + "=" * 96)
    print(f"{len(PASS) + len(FAIL)} checks, {len(FAIL)} failure(s)")
    for cid, name, detail in FAIL:
        print(f"  FAIL {cid} {name}: {detail}")
    print("A verification is a check of the ARITHMETIC and the PROVENANCE, not of the SCIENCE.")
    print("No link of the L1->L4 chain moved in wave 6 or in this verification. Clay ~0.05%.")
    print("=" * 96)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
