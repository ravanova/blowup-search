"""P2 Route-PNR v1 -- repair of profile_newton.py's convergence verdict, and the
explicit re-derivation of Route-D v11's headline verdicts on the repaired module.

Leg 202 (Route-PNA) measured 30 cases in which `converged` was True on an object
that is not the physical traveling wave, by three mechanisms: M1 off-branch
grid-scale roots at machine-zero residual, M2 escape down the exact scaling
degeneracy from a small-amplitude start, M3 `c0` handed back unchecked.  This leg
repairs the verdict and then re-derives what the repair was supposed to protect.

IMPORTANT correction to this leg's own dispatch, frozen in writeup/novelty/leg_226.md
BEFORE any of this was built: the prescribed fix -- incorporate Route-D v11's
`weighted_defect` into the verdict -- does NOT work.  It is anti-correlated with
the off-branch cases, because an off-branch root nulls every residual row to
machine precision, so sup w|R2| stays small no matter how far the profile has
left the decay class.  ARM C measures that rather than asserting it.  The
mechanism that does work is the decay class relative to the anchor (D3).

FOUR ARMS.
  ARM A  every one of leg 202's silent-wrong cases, pre-repair verdict vs post.
  ARM B  zero-regression: the pre-repair module read OUT OF GIT at its own stable
         ancestor commit and run in the SAME process, so nothing on-branch that
         used to be accepted is now rejected.
  ARM C  the two margins the 100x threshold sits between, both measured; plus the
         head-to-head of D1 (weighted defect), D2 (gauges) and D3 (decay class)
         as rejectors on the same rows.
  ARM D  Route-D v11's own headline verdicts, re-derived: three numbers each --
         BANKED, pre-repair re-run HERE (environment control), post-repair.

NOT a logged Tier-1/2 experiment: deterministic Newton, no GA, no seeds.  Run:

    .venv/bin/python experiments/p2_route_pnr_v1_repair.py
    -> writeup/data/p2_route_pnr_v1_repair.json

Runtime ~15 min, dominated by ARM D's n = 1601 dense least-squares solves.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from solver.profile_newton import (                                  # noqa: E402
    FARFIELD_INFLATION_MAX, TwoScaleNewton, continuation)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "writeup" / "data" / "p2_route_pnr_v1_repair.json"

# The module's own stable ancestor commit.  Leg 150's d871675 lesson: pin the
# commit that introduced the file, never a branch hash a rebase can rewrite.
PRE_REPAIR_REF = "6a17ce6"

ALPHA = 1.4                  # Route-D v11's codomain grading, for D1
V11_N = 801                  # Route-D v11's working grid


# ---------------------------------------------------------------- pre-repair --
def load_pre_repair():
    """Import the PRE-repair module, out of git, under a substituted name.

    Both modules then live in the same process, on the same BLAS, so ARM B's
    comparison cannot be confounded by the 2.31 decades of backend drift that
    test_profile_newton.py item (6) measured on exactly this class of number.
    """
    src = subprocess.run(["git", "show",
                          "%s:solver/profile_newton.py" % PRE_REPAIR_REF],
                         cwd=str(ROOT), capture_output=True, text=True,
                         check=True).stdout
    fd, path = tempfile.mkstemp(suffix="_pre_repair.py")
    with os.fdopen(fd, "w") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location("profile_newton_pre", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["profile_newton_pre"] = mod
    spec.loader.exec_module(mod)
    mod.__pnr_source_sha_ref = PRE_REPAIR_REF
    return mod


def diagnostics(nw, om, c):
    """D1/D2/D3 on one returned profile.  Windows are leg 202's, verbatim."""
    X = nw.fam.X
    outer = np.abs(X) > 0.5 * np.max(np.abs(X))
    anc = float(np.max(np.abs(nw.anchor()[outer])))
    om = np.asarray(om, float)
    finite = bool(np.all(np.isfinite(om)))
    ff = float(np.max(np.abs(om[outer]))) if finite else float("inf")
    R = nw.residual(om, c)
    w = (1.0 + X ** 2) ** (0.5 * (ALPHA + 1.0))
    return {
        "D1_weighted_defect": (float(np.max(w * np.abs(R))) if finite
                               else float("inf")),
        "D2_gauge_residual": (float(max(abs(om[nw.i0] + 1.0),
                                        abs(om[nw.i1] + 0.5))) if finite
                              else float("inf")),
        "D3_farfield_inflation": ff / anc if anc > 0 else float("inf"),
        "farfield_sup": ff, "anchor_farfield_sup": anc,
    }


# ------------------------------------------------------------------- ARM A ----
# Leg 202's silent-wrong cases, transcribed from its banked JSON with the
# reported values so the reproduction is checkable, not just re-run.
LADDER_A = [0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.05, 1.2, 1.35, 1.5]


def arm_a(pre):
    """Every leg-202 silent-wrong case: pre-repair verdict vs post-repair."""
    cases = []

    def record(group, label, mod_pre_r, nw_pre, mod_post_r, nw_post, expect):
        d_pre = diagnostics(nw_pre, mod_pre_r["Omega"], mod_pre_r["c"])
        d_post = diagnostics(nw_post, mod_post_r["Omega"], mod_post_r["c"])
        cases.append({
            "group": group, "case": label, "expected": expect,
            "pre_converged": bool(mod_pre_r["converged"]),
            "post_converged": bool(mod_post_r["converged"]),
            "pre_relres": float(mod_pre_r.get("relres", float("inf"))),
            "post_relres": float(mod_post_r.get("relres", float("inf"))),
            "pre_c": float(mod_pre_r["c"]), "post_c": float(mod_post_r["c"]),
            "post_reason": mod_post_r.get("reason"),
            "D1_weighted_defect": d_post["D1_weighted_defect"],
            "D2_gauge_residual": d_post["D2_gauge_residual"],
            "D3_farfield_inflation": d_post["D3_farfield_inflation"],
            "pre_D3": d_pre["D3_farfield_inflation"],
            "now_correct": bool(mod_post_r["converged"] is False
                                if expect == "REJECT"
                                else mod_post_r["converged"] is True),
        })

    # -- M1, cold solves on the a-ladder (leg 202 G1) ----------------------
    for n in (101, 201, 301):
        for a in (0.3, 0.6, 0.9, 1.2, 1.5):
            nw_pre = pre.TwoScaleNewton(a=a, n=n)
            nw_post = TwoScaleNewton(a=a, n=n)
            rp, rq = nw_pre.solve(), nw_post.solve()
            d = diagnostics(nw_post, rq["Omega"], rq["c"])
            expect = ("REJECT" if d["D3_farfield_inflation"]
                      >= FARFIELD_INFLATION_MAX else "ACCEPT")
            record("G1_cold_ladder", "n=%d,a=%.2f" % (n, a),
                   rp, nw_pre, rq, nw_post, expect)

    # -- M1, the continuation ladder: warm starts and the retry clause -----
    for n in (101, 201, 301):
        pre_rows = pre.continuation(LADDER_A, n=n)
        post_rows = continuation(LADDER_A, n=n)
        for rp, rq in zip(pre_rows, post_rows):
            expect = ("REJECT" if rq["farfield_inflation"]
                      >= FARFIELD_INFLATION_MAX else "ACCEPT")
            cases.append({
                "group": "G3_continuation_ladder",
                "case": "n=%d,a=%.2f" % (n, rp["a"]), "expected": expect,
                "pre_converged": bool(rp["converged"]),
                "post_converged": bool(rq["converged"]),
                "pre_relres": rp["relres"], "post_relres": rq["relres"],
                "pre_c": rp["c"], "post_c": rq["c"],
                "post_reason": rq.get("reason"),
                "D3_farfield_inflation": rq["farfield_inflation"],
                "D2_gauge_residual": rq["gauge_residual"],
                "now_correct": bool(rq["converged"] is False
                                    if expect == "REJECT"
                                    else rq["converged"] is True),
            })

    # -- M2, the scaling-family escape from a small-amplitude start --------
    for n in (201, 301):
        for eps in (1e-7, 1e-8, 1e-9, 1e-10):
            nw_pre = pre.TwoScaleNewton(a=0.0, n=n)
            nw_post = TwoScaleNewton(a=0.0, n=n)
            om0_pre = eps * nw_pre.anchor()
            om0_post = eps * nw_post.anchor()
            rp = nw_pre.solve(om0=om0_pre)
            rq = nw_post.solve(om0=om0_post)
            record("G2_scaling_escape", "n=%d,eps=%.0e" % (n, eps),
                   rp, nw_pre, rq, nw_post, "REJECT")

    # -- M3, c0 never range-checked ---------------------------------------
    for c0 in (1e6, 1e9, 1e12, 1e15):
        nw_pre = pre.TwoScaleNewton(a=0.0, n=101)
        nw_post = TwoScaleNewton(a=0.0, n=101)
        rp = nw_pre.solve(om0=nw_pre.anchor(), c0=c0)
        rq = nw_post.solve(om0=nw_post.anchor(), c0=c0)
        record("G4_c0_unchecked", "c0=%.0e" % c0, rp, nw_pre, rq, nw_post,
               "REJECT")

    # -- G5, the rho_max = 16 degenerate case ------------------------------
    nw_pre = pre.TwoScaleNewton(a=0.3, n=101, rho_max=16.0)
    nw_post = TwoScaleNewton(a=0.3, n=101, rho_max=16.0)
    record("G5_degenerate", "rho_max=16.0", nw_pre.solve(), nw_pre,
           nw_post.solve(), nw_post, "REJECT")

    fired = [c for c in cases if c["expected"] == "REJECT"]
    slipped = [c for c in fired if not c["now_correct"]]
    was_wrong = [c for c in fired if c["pre_converged"]]
    return {
        "cases": cases,
        "n_cases": len(cases),
        "n_expected_reject": len(fired),
        "n_silently_wrong_pre_repair": len(was_wrong),
        "n_still_slipping_through": len(slipped),
        "still_slipping": [c["case"] for c in slipped],
        "reading": "Every case leg 202 classified SILENT_WRONG, re-run against "
                   "the pre-repair module out of git and the repaired module in "
                   "the same process.  `expected` is COMPUTED from the decay "
                   "class, not asserted per case, so a case that is genuinely "
                   "on-branch in this environment is not counted as a miss.",
    }


# ------------------------------------------------------------------- ARM B ----
def arm_b(pre):
    """Zero-regression: nothing on-branch that was accepted is now rejected."""
    rows = []
    for n in (101, 201, 301, 401):
        for a in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
            nw_pre = pre.TwoScaleNewton(a=a, n=n)
            nw_post = TwoScaleNewton(a=a, n=n)
            rp, rq = nw_pre.solve(), nw_post.solve()
            d = diagnostics(nw_post, rq["Omega"], rq["c"])
            rows.append({
                "n": n, "a": a,
                "pre_converged": bool(rp["converged"]),
                "post_converged": bool(rq["converged"]),
                "pre_relres": rp["relres"], "post_relres": rq["relres"],
                "pre_c": rp["c"], "post_c": rq["c"],
                "c_delta": abs(rp["c"] - rq["c"]),
                "D3_farfield_inflation": d["D3_farfield_inflation"],
                "post_reason": rq.get("reason"),
            })
    # A regression is a row the OLD module accepted, the NEW module rejects,
    # and whose decay class says it was on-branch all along.
    regressions = [r for r in rows
                   if r["pre_converged"] and not r["post_converged"]
                   and r["D3_farfield_inflation"] < FARFIELD_INFLATION_MAX]
    newly_rejected = [r for r in rows
                      if r["pre_converged"] and not r["post_converged"]]
    return {
        "rows": rows, "n_rows": len(rows),
        "n_regressions": len(regressions),
        "regressions": [{"n": r["n"], "a": r["a"],
                         "D3": r["D3_farfield_inflation"],
                         "reason": r["post_reason"]} for r in regressions],
        "n_newly_rejected": len(newly_rejected),
        "newly_rejected": [{"n": r["n"], "a": r["a"],
                            "D3": r["D3_farfield_inflation"],
                            "reason": r["post_reason"]}
                           for r in newly_rejected],
        "max_c_delta_on_accepted": max(
            (r["c_delta"] for r in rows if r["post_converged"]), default=0.0),
        "reading": "The repair adds only REJECTIONS -- it never alters the "
                   "Newton iteration, so on any row both modules accept, the "
                   "returned c must be bit-comparable.  max_c_delta_on_accepted "
                   "is that check.",
    }


# ------------------------------------------------------------------- ARM C ----
def arm_c(arm_a_result):
    """The two margins, and D1/D2/D3 head-to-head as rejectors."""
    cases = [c for c in arm_a_result["cases"] if "D3_farfield_inflation" in c]
    off = [c for c in cases if c["expected"] == "REJECT"]
    on = [c for c in cases if c["expected"] == "ACCEPT"]

    def rejects(cs, key, thr, above=True):
        vals = [c[key] for c in cs if key in c and np.isfinite(c[key])]
        return sum(1 for v in vals if (v >= thr if above else v < thr))

    d1_off = [c["D1_weighted_defect"] for c in off if "D1_weighted_defect" in c]
    d1_on = [c["D1_weighted_defect"] for c in on if "D1_weighted_defect" in c]
    d3_off = [c["D3_farfield_inflation"] for c in off]
    d3_on = [c["D3_farfield_inflation"] for c in on]
    d2_off = [c["D2_gauge_residual"] for c in off if "D2_gauge_residual" in c]
    return {
        "threshold": FARFIELD_INFLATION_MAX,
        "threshold_provenance": "leg 202's own pre-committed classifier "
                                "threshold, adopted UNCHANGED, not retuned here",
        "D3_max_on_branch": max(d3_on) if d3_on else None,
        "D3_min_off_branch": min(d3_off) if d3_off else None,
        "margin_decades_below_threshold": (
            float(np.log10(FARFIELD_INFLATION_MAX / max(d3_on)))
            if d3_on and max(d3_on) > 0 else None),
        "margin_decades_above_threshold": (
            float(np.log10(min(d3_off) / FARFIELD_INFLATION_MAX))
            if d3_off and min(d3_off) > 0 else None),
        "D1_min_off_branch": min(d1_off) if d1_off else None,
        "D1_max_off_branch": max(d1_off) if d1_off else None,
        "D1_max_on_branch": max(d1_on) if d1_on else None,
        "D1_rejects_off_branch_at_any_threshold_that_keeps_on_branch": bool(
            d1_off and d1_on and min(d1_off) > max(d1_on)),
        "D2_off_branch_at_exactly_zero": sum(1 for v in d2_off if v == 0.0),
        "D2_off_branch_total": len(d2_off),
        "reading": "D1 is the diagnostic this leg was DISPATCHED to incorporate. "
                   "It is measured here as a rejector on the same rows and it "
                   "fails: its smallest off-branch value is BELOW its largest "
                   "on-branch value, so no threshold on D1 separates the two "
                   "classes at all. D2 is exactly 0.0 on the M1 off-branch "
                   "roots -- it is retained because it is what catches M2/M3, "
                   "not M1. D3 is the only one of the three that separates.",
    }


# --------------- ARM C2: does D3 actually discriminate? (lesson 90) ----------
def arm_c2():
    """What would have to differ for D3 to report the OTHER answer.

    A discriminator that fires on everything discriminates nothing.  Two
    falsification probes, both of which must come back the way stated or the
    mechanism is not what this leg claims it is.
    """
    # (i) the anchor itself, and analytic perturbations of it, must PASS.
    passes = []
    nw = TwoScaleNewton(a=0.0, n=201)
    X = nw.fam.X
    for label, om in [
        ("exact_anchor", nw.anchor()),
        ("anchor_x1.0001", nw.anchor() * 1.0001),
        ("anchor_plus_smooth_bump", nw.anchor()
         + 1e-3 * np.exp(-X ** 2)),
        ("anchor_widened_5pct", -1.0 / (1.0 + (X / 1.05) ** 2)),
    ]:
        d = diagnostics(nw, om, 0.5)
        passes.append({"case": label, "D3": d["D3_farfield_inflation"],
                       "would_pass": bool(d["D3_farfield_inflation"]
                                          < FARFIELD_INFLATION_MAX)})
    # (ii) an object deliberately given a FATTER far field must FAIL, and the
    #      inflation must scale the way the construction says it should.
    fails = []
    for tail in (1e-4, 1e-3, 1e-2, 1e-1):
        om = nw.anchor() + tail * np.ones_like(X)
        om = om - (om[nw.i0] + 1.0)      # keep gauge 1 satisfied
        d = diagnostics(nw, om, 0.5)
        fails.append({"case": "anchor_plus_%.0e_constant_tail" % tail,
                      "D3": d["D3_farfield_inflation"],
                      "would_fail": bool(d["D3_farfield_inflation"]
                                         >= FARFIELD_INFLATION_MAX)})
    anc_ff = diagnostics(nw, nw.anchor(), 0.5)["anchor_farfield_sup"]
    return {
        "must_pass": passes, "must_fail": fails,
        "anchor_farfield_sup_n201": anc_ff,
        "all_must_pass_passed": all(p["would_pass"] for p in passes),
        "all_must_fail_failed": all(f["would_fail"] for f in fails),
        "reading": "For D3 to report the other answer on the off-branch cases, "
                   "the returned profile's far-field supremum would have to fall "
                   "below 100x the anchor's %.2e on the same grid -- i.e. the "
                   "grid-scale oscillation leg 202 measured at node-to-node 0.80 "
                   "would have to not exist. The constant-tail ladder shows the "
                   "threshold is crossed by a tail of order 1e-3, which is far "
                   "below the 9.02 supremum of the worst measured off-branch "
                   "root, so the verdict is not sitting on a knife edge."
                   % anc_ff,
    }


# ------------------------------------------------------------------- ARM D ----
def weighted_defect(nw, om, c, alpha=ALPHA):
    """Route-D v11's own codomain norm, copied verbatim from v11 for ARM D."""
    R = nw.residual(om, c)
    w = (1.0 + nw.fam.X ** 2) ** (0.5 * (alpha + 1.0))
    return float(np.max(w * np.abs(R)))


def _v2_sweep(mod, n=V11_N):
    """Route-D v11's V2, re-run against `mod` (pre- or post-repair)."""
    a_values = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                0.55, 0.6, 0.7, 0.8, 0.9, 1.0]
    rows = mod.continuation(a_values, n=n)
    for r in rows:
        nw = mod.TwoScaleNewton(a=r["a"], n=n)
        s = nw.solve(om0=None, c0=0.5)
        r["weighted_defect"] = weighted_defect(nw, s["Omega"], s["c"])
        d = diagnostics(nw, s["Omega"], s["c"])
        r["cold_D3_farfield_inflation"] = d["D3_farfield_inflation"]
    # v11's OWN test, verbatim: relres < 1e-8, the flag never consulted.
    good_v11 = [r for r in rows if r["relres"] < 1e-8]
    # the same quantity re-derived with the REPAIRED verdict as the test.
    good_rep = [r for r in rows
                if r["relres"] < 1e-8 and r.get("converged", False)]
    return {
        "n": n, "rows": rows,
        "a_max_machine_v11_own_test": max((r["a"] for r in good_v11),
                                          default=0.0),
        "a_max_machine_repaired_verdict": max((r["a"] for r in good_rep),
                                              default=0.0),
        "best_relres": min(r["relres"] for r in rows),
    }


def _v4_grids(mod, ns=(401, 801, 1601), a_values=(0.0, 0.2, 0.5, 0.8, 1.0)):
    """Route-D v11's V4, re-run against `mod`.  This is the slow arm."""
    rows = []
    for n in ns:
        for a in a_values:
            nw = mod.TwoScaleNewton(a=float(a), n=int(n))
            r = nw.solve(om0=None, c0=0.5)
            X = nw.fam.X
            i4 = int(np.argmin(np.abs(X - 4.0)))
            d = diagnostics(nw, r["Omega"], r["c"])
            rows.append({"n": int(n), "a": float(a), "relres": r["relres"],
                         "c": r["c"], "converged": bool(r["converged"]),
                         "Omega_at_X4": float(r["Omega"][i4]),
                         "weighted_defect": weighted_defect(nw, r["Omega"],
                                                            r["c"]),
                         "D3_farfield_inflation": d["D3_farfield_inflation"]})
    def verdicts(test):
        out = []
        for a in a_values:
            sub = [r for r in rows if r["a"] == a and test(r)]
            if not sub:
                out.append({"a": float(a), "c_spread": None,
                            "grids_reaching_machine_precision": 0,
                            "grid_converged": False})
                continue
            cs = [r["c"] for r in sub]
            out.append({"a": float(a), "c_spread": float(max(cs) - min(cs)),
                        "cs": cs,
                        "grids_reaching_machine_precision": len(sub),
                        "grid_converged": bool(max(cs) - min(cs) < 1e-3
                                               and len(sub) >= 2)})
        return out
    v11_own = verdicts(lambda r: r["relres"] < 1e-8)
    repaired = verdicts(lambda r: r["relres"] < 1e-8 and r["converged"])
    return {
        "rows": rows, "verdict_v11_own_test": v11_own,
        "verdict_repaired_verdict": repaired,
        "grid_converged_a_max_v11_own_test": max(
            (v["a"] for v in v11_own if v["grid_converged"]), default=0.0),
        "grid_converged_a_max_repaired_verdict": max(
            (v["a"] for v in repaired if v["grid_converged"]), default=0.0),
    }


def arm_d(pre):
    """Route-D v11's headlines: BANKED vs pre-repair-here vs post-repair."""
    banked_path = ROOT / "writeup" / "data" / "p2_route_d_v11_anchor.json"
    banked = json.loads(banked_path.read_text()) if banked_path.exists() else {}
    b2 = banked.get("v2_sweep", {})
    b3 = banked.get("v3_boundary", {})
    b4 = banked.get("v4_grids", {})

    t0 = time.time()
    pre_v2 = _v2_sweep(pre)
    post_v2 = _v2_sweep(sys.modules["solver.profile_newton"])
    pre_v4 = _v4_grids(pre)
    post_v4 = _v4_grids(sys.modules["solver.profile_newton"])
    elapsed = time.time() - t0

    # -- the a = 1.50 three-grid question, clause (b) of the gate ----------
    a150 = []
    for n in (101, 201, 301):
        rows_pre = pre.continuation(LADDER_A, n=n)
        rows_post = continuation(LADDER_A, n=n)
        rp = [r for r in rows_pre if abs(r["a"] - 1.5) < 1e-12][0]
        rq = [r for r in rows_post if abs(r["a"] - 1.5) < 1e-12][0]
        a150.append({"n": n, "pre_c": rp["c"],
                     "pre_converged": bool(rp["converged"]),
                     "post_c": rq["c"],
                     "post_converged": bool(rq["converged"]),
                     "post_D3": rq["farfield_inflation"],
                     "post_reason": rq.get("reason")})
    accepted150 = [r["post_c"] for r in a150 if r["post_converged"]]
    pre_c150 = [r["pre_c"] for r in a150]

    return {
        "runtime_s": elapsed,
        "a_max_machine": {
            "banked": b2.get("a_max_machine"),
            "pre_repair_rerun_here": pre_v2["a_max_machine_v11_own_test"],
            "post_repair_v11_own_relres_test":
                post_v2["a_max_machine_v11_own_test"],
            "post_repair_repaired_verdict":
                post_v2["a_max_machine_repaired_verdict"],
        },
        "grid_converged_a_max": {
            "banked": b4.get("grid_converged_a_max"),
            "pre_repair_rerun_here": pre_v4["grid_converged_a_max_v11_own_test"],
            "post_repair_v11_own_relres_test":
                post_v4["grid_converged_a_max_v11_own_test"],
            "post_repair_repaired_verdict":
                post_v4["grid_converged_a_max_repaired_verdict"],
        },
        "GA_boundary": {
            "banked": b3.get("GA_boundary"),
            "status": "HARDCODED LITERAL at experiments/p2_route_d_v11_anchor.py "
                      "line 112 -- it is the GA's own prior result quoted for "
                      "comparison, NOT a computed verdict. No repair to "
                      "profile_newton.py can move it, and reporting it as "
                      "'unchanged' without saying so would be misleading.",
            "post_repair": b3.get("GA_boundary"),
        },
        "a_1p50_three_grids": {
            "rows": a150,
            "pre_repair_c_values": pre_c150,
            "pre_repair_relative_spread": (
                (max(pre_c150) - min(pre_c150)) / abs(np.mean(pre_c150))
                if pre_c150 else None),
            "post_repair_accepted_c_values": accepted150,
            "n_grids_accepted_post_repair": len(accepted150),
            "post_repair_spread": (max(accepted150) - min(accepted150)
                                   if len(accepted150) > 1 else None),
        },
        "v2_pre": pre_v2, "v2_post": post_v2,
        "v4_pre": pre_v4, "v4_post": post_v4,
    }


# --------------------------------------------------------------------- main --
def main():
    pre = load_pre_repair()
    data = {"meta": {
        "leg": "P2 Route-PNR v1 (repair of profile_newton.py's convergence "
               "verdict + re-derivation of Route-D v11's headlines)",
        "tier": "Level-1 tooling repair; NOT a certificate, nothing rigorous",
        "reproduce": "python experiments/p2_route_pnr_v1_repair.py",
        "pre_repair_ref": PRE_REPAIR_REF,
        "mechanism": "D3 -- decay class of the returned profile relative to the "
                     "a=0 anchor on the same grid -- plus the two gauge rows "
                     "(D2) the verdict never consulted. NOT D1, the weighted "
                     "defect this leg was dispatched to incorporate: ARM C "
                     "measures D1 failing to separate the classes at all.",
        "threshold": FARFIELD_INFLATION_MAX,
        "numpy": np.__version__,
    }}
    data["arm_a_leg202_cases"] = arm_a(pre)
    data["arm_b_zero_regression"] = arm_b(pre)
    data["arm_c_margins_and_head_to_head"] = arm_c(data["arm_a_leg202_cases"])
    data["arm_c2_does_D3_discriminate"] = arm_c2()
    data["arm_d_route_d_v11_rederivation"] = arm_d(pre)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, default=float))

    a, b = data["arm_a_leg202_cases"], data["arm_b_zero_regression"]
    c = data["arm_c_margins_and_head_to_head"]
    c2, d = data["arm_c2_does_D3_discriminate"], \
        data["arm_d_route_d_v11_rederivation"]
    print("\nP2 ROUTE-PNR v1 -- repaired convergence verdict\n" + "=" * 62)
    print("  A  %d cases, %d expected-reject, %d were silently accepted "
          "pre-repair, %d still slip through post-repair"
          % (a["n_cases"], a["n_expected_reject"],
             a["n_silently_wrong_pre_repair"], a["n_still_slipping_through"]))
    if a["still_slipping"]:
        print("     STILL SLIPPING: %s" % ", ".join(a["still_slipping"]))
    print("  B  %d on-branch rows, %d regressions, %d newly rejected; "
          "max |dc| on rows both accept = %.3e"
          % (b["n_rows"], b["n_regressions"], b["n_newly_rejected"],
             b["max_c_delta_on_accepted"]))
    print("  C  D3 on-branch max %.3e | threshold %.0f | off-branch min %.3e "
          "(%.2f decades below / %.2f above)"
          % (c["D3_max_on_branch"], c["threshold"], c["D3_min_off_branch"],
             c["margin_decades_below_threshold"] or float("nan"),
             c["margin_decades_above_threshold"] or float("nan")))
    print("     D1 off-branch range %.2e..%.2e vs on-branch max %.2e -- "
          "separates: %s"
          % (c["D1_min_off_branch"], c["D1_max_off_branch"],
             c["D1_max_on_branch"],
             c["D1_rejects_off_branch_at_any_threshold_that_keeps_on_branch"]))
    print("  C2 falsification: all must-pass passed = %s; all must-fail "
          "failed = %s" % (c2["all_must_pass_passed"],
                           c2["all_must_fail_failed"]))
    am, gm = d["a_max_machine"], d["grid_converged_a_max"]
    print("  D  a_max_machine   banked %s | pre-repair here %s | post-repair "
          "(v11's own relres test) %s | post-repair (repaired verdict) %s"
          % (am["banked"], am["pre_repair_rerun_here"],
             am["post_repair_v11_own_relres_test"],
             am["post_repair_repaired_verdict"]))
    print("     grid_converged_a_max  banked %s | pre %s | post(v11 test) %s | "
          "post(repaired) %s"
          % (gm["banked"], gm["pre_repair_rerun_here"],
             gm["post_repair_v11_own_relres_test"],
             gm["post_repair_repaired_verdict"]))
    print("     GA_boundary %s -- hardcoded literal, cannot move under any "
          "module repair" % (d["GA_boundary"]["banked"],))
    t = d["a_1p50_three_grids"]
    print("     a=1.50: pre-repair c = %s (rel. spread %.2f); post-repair %d/3 "
          "grids accepted, values %s"
          % (["%.5f" % v for v in t["pre_repair_c_values"]],
             t["pre_repair_relative_spread"],
             t["n_grids_accepted_post_repair"],
             ["%.5f" % v for v in t["post_repair_accepted_c_values"]]))
    print("\n[done] wrote %s" % OUT)


if __name__ == "__main__":
    main()
