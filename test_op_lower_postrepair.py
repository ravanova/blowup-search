"""POST-REPAIR regression gates for solver/op_lower.py -- Route-OLB, leg 132.

Leg 132's gate answered YES on both clauses, and its yes-branch is explicit:
"Bank the 209-case battery as a permanent regression suite." This is that suite.

WHAT NOTHING ELSE IN THE REPO COVERS.

  * `test_op_lower.py` (6 tests) is self-consistency on the ONE benign
    J-collocation inverse. It cannot see a battery-wide overshoot and it touches
    none of the banked v10 numbers.
  * `test_op_lower_adversarial.py` (leg 101, inverted by the repair) asserts the
    repaired behaviour it was rewritten to assert, from the same authorship chain
    as the module and the runner.
  * `experiments/p2_route_ola_v1_bench_check.py` grades non-regression against
    `PRE`, a dict of LITERALS the repair itself wrote -- so the pre-repair
    magnitudes it compares against are self-asserted.

These gates close all three holes at once. The reference is derived
independently (extreme-point enumeration of the weighted-l1 ball, exact
rationals), the grading is at 0 ULP, and the pre-repair module is RECONSTRUCTED
FROM GIT (`ef0ea2e:solver/op_lower.py`) so the comparison is a measurement rather
than a literal.

GATE 5 IS THE ONE THAT KEEPS THE REST HONEST (lesson 90: a control that cannot
come out differently is not a control). It runs the SAME grader over the
PRE-repair module and requires 47 violations under leg 101's published rule, 46
of them overflow, max finite L/N_true = 1.000604187. If both modules scored 0,
the grader would be broken and every other gate here would pass vacuously.

THE ASYMMETRY THESE GATES ENCODE, which is DIRECTION.md's and not this file's:
a deflation that moves the bound DOWN is admissible; one that moves any
VALIDATED magnitude is not. So gate 4 forbids `L > N_true` at any ULP, while an
adversarial headline that ROSE is fine provided it is still under the true norm
-- 15 of them do (gate 7), because the repair recovers bounds the pre-repair
module lost to overflow.

A FAILURE HERE IS A REGRESSION IN `solver/op_lower.py`, and the fix belongs
there -- never in these gates.

Run: .venv/bin/python test_op_lower_postrepair.py
"""

import json
import os
import sys

import numpy as np

sys.path.insert(0, ".")

import experiments.p2_route_olb_v1_postrepair as R

PASS, FAIL = "PASS", "FAIL"
results = []


def gate(name, ok, detail):
    results.append((PASS if ok else FAIL, name, detail))
    print(f"[{PASS if ok else FAIL}] {name}: {detail}")


_ROOT = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# the battery, built once: both modules over all 408 cases
# --------------------------------------------------------------------------
PRE = R.load_pre_repair()
print(f"pre-repair module reconstructed from git: {R.PRE_COMMIT}"
      f":solver/op_lower.py (blob {PRE.__source_sha__[:12]})\n")

RECS = R.battery(PRE)
DECIDED = [r for r in RECS if r["verdict"] in
           ("sound", "sound_but_zero", "VIOLATION_overflow", "VIOLATION_finite",
            "finite_exceedance_unconfirmed")]
EXCL = [r for r in RECS if r["verdict"] == "excluded_ref_nonfinite"]

# --------------------------------------------------------------------------
# 1 -- the battery is leg 101's battery, case for case
# --------------------------------------------------------------------------
gate("the battery has leg 101's shape exactly",
     (len(RECS) == R.EXPECT_TOTAL and len(DECIDED) == R.EXPECT_DECIDING
      and len(EXCL) == R.EXPECT_EXCLUDED),
     f"{len(RECS)} cases, {len(DECIDED)} gate-deciding, {len(EXCL)} excluded "
     f"(leg 101: {R.EXPECT_TOTAL}/{R.EXPECT_DECIDING}/{R.EXPECT_EXCLUDED}). A "
     "different count would mean every other number here quotes a different "
     "population than leg 101 did")

# --------------------------------------------------------------------------
# 2 -- the reference, derived two ways, before anything is read off it
# --------------------------------------------------------------------------
EXACT = [r for r in RECS if r.get("exact_ref")]
DISAGREE = [r for r in EXACT if not r["ref_routes_agree"]]
gate("the exact reference agrees with itself, derived two independent ways",
     len(EXACT) == 208 and not DISAGREE,
     f"{len(EXACT)} cases carry an exact reference; extreme-point enumeration of "
     f"the weighted-l1 ball and leg 101's closed form max_ij t_i|A_ij|/u_j "
     f"disagree on {len(DISAGREE)}. Both are exact rational, so a disagreement "
     "would indict the REFERENCE and invalidate gates 4-7 -- it is checked first")

# --------------------------------------------------------------------------
# 3 -- NaN is skipped, never propagated; nothing raises
# --------------------------------------------------------------------------
NANH = [r for r in RECS if r["verdict"] == "nan_headline"]
RAISED = [r for r in RECS if r["verdict"] == "raised"]
gate("no NaN reaches a headline and nothing raises",
     not NANH and not RAISED,
     f"{len(NANH)} NaN headlines and {len(RAISED)} exceptions over {len(RECS)} "
     "cases, including 3 NaN-poisoned operators and a NaN weight. Leg 101 "
     "measured 0 NaN headlines pre-repair; the repair did not introduce one")

# --------------------------------------------------------------------------
# 4 -- CLAUSE (a): the bound is a lower bound, on every decided case
# --------------------------------------------------------------------------
OVER = [r for r in DECIDED if r["verdict"] == "VIOLATION_overflow"]
FINV = [r for r in DECIDED if r["verdict"] == "VIOLATION_finite"]
UNCONF = [r for r in DECIDED if r["verdict"] == "finite_exceedance_unconfirmed"]
gate("0 soundness violations over the 209 gate-deciding cases, graded at 0 ULP",
     not OVER and not FINV and not UNCONF,
     f"{len(OVER)} overflow (L = inf against a finite norm), {len(FINV)} finite "
     f"exceedances, {len(UNCONF)} unconfirmed. Graded at 0 ULP -- stricter than "
     "leg 101's published rule, which excused exceedances within one ULP as "
     "correct rounding. Nothing needs excusing post-repair")

# --------------------------------------------------------------------------
# 5 -- THE POSITIVE CONTROL: without it, gates 1-4 could pass vacuously
# --------------------------------------------------------------------------
OVER_P = [r for r in DECIDED if r["verdict_pre"] == "VIOLATION_overflow"]
FINV_P = [r for r in DECIDED if r["verdict_pre"] == "VIOLATION_finite"]
FINV_101 = [r for r in FINV_P if r["excess_ulps_pre"] > 1.0
            and np.isfinite(r["ratio_pre"]) and r["ratio_pre"] > 1.0 + 1e-9]
RATIO_P = max(r["ratio_pre"] for r in DECIDED if np.isfinite(r["ratio_pre"]))
gate("the SAME grader still fails the PRE-repair module, at leg 101's numbers",
     (len(OVER_P) == R.EXPECT_PRE_OVERFLOW
      and len(OVER_P) + len(FINV_101) == R.EXPECT_PRE_VIOLATIONS_LEG101
      and len(OVER_P) + len(FINV_P) == R.EXPECT_PRE_VIOLATIONS_0ULP
      and abs(RATIO_P - 1.000604187119504829) < 1e-15),
     f"pre-repair: {len(OVER_P) + len(FINV_101)} violations under leg 101's rule "
     f"({len(OVER_P)} overflow + {len(FINV_101)} finite; leg 101 published "
     f"{R.EXPECT_PRE_VIOLATIONS_LEG101}), and "
     f"{len(OVER_P) + len(FINV_P)} under this file's stricter 0-ULP rule -- the "
     f"extra {len(FINV_P) - len(FINV_101)} being exactly the cases leg 101 "
     f"excused as sound_within_one_ulp. Max finite L/N_true = {RATIO_P:.12f} "
     "(leg 101: 1.000604187). The grader can report the other answer")

# --------------------------------------------------------------------------
# 6 -- the magnitude, not the boolean
# --------------------------------------------------------------------------
FIN = [r["ratio"] for r in DECIDED if np.isfinite(r["ratio"])]
MAXR = max(FIN)
gate("max finite L/N_true over the 209 decided cases is below 1",
     MAXR <= 1.0 and abs(MAXR - 0.999999999998994804) < 1e-15,
     f"{MAXR:.18f} -- an independent re-derivation of leg 101's banked "
     "0.9999999999989946, from a reference this leg wrote. Quoted in full so a "
     "reader can see the bound is under the true norm by ~1e-12, i.e. by the "
     "certified deflation, and is not 1 by luck")

# --------------------------------------------------------------------------
# 7 -- a bound that ROSE is admissible only if it is still true
# --------------------------------------------------------------------------
UP = [r for r in RECS if r["moved_up"]]
UP_BAD = [r for r in UP if r["verdict"] not in ("sound", "sound_but_zero")
          or r["ratio"] > 1.0]
BIGGEST = max(UP, key=lambda r: r["L"]) if UP else None
gate("every adversarial headline that rose is still under the true norm",
     len(UP) == 15 and not UP_BAD,
     f"{len(UP)} of {len(RECS)} headlines are LARGER post-repair than pre-repair, "
     f"{len(UP_BAD)} of them unsound. These are the repair RECOVERING bounds the "
     f"pre-repair module lost to overflow or denormal underflow -- the largest is "
     f"{BIGGEST['operator']}/{BIGGEST['weights']}, 0.0 -> {BIGGEST['L']:.4e} "
     f"against a true norm of {float(BIGGEST['N_res']):.4e}. Admissible by "
     "DIRECTION.md's asymmetry: no candidate direction, shape family or ascent "
     "changed, so this is recovery, not sharpening")

# --------------------------------------------------------------------------
# 8 -- CLAUSE (b): the known-answer line moves DOWN only
# --------------------------------------------------------------------------
with open(os.path.join(_ROOT, "writeup", "data",
                       "p2_route_d_v10_lower.json")) as fh:
    BANKED = json.load(fh)
PLAN = ([(1.5, 0.5, b) for b in BANKED["w1_ladder"]["ladder"]
         if b["J"] in (200, 400)]
        + [(1.4, 0.15, b) for b in BANKED["w2_operating"]["ladder"]
           if b["J"] in (200, 400)])
rows, ok8 = [], True
for alpha, gamma, b in PLAN:
    col, A, dom, cod = R._setup(int(b["J"]), alpha, gamma)
    f = R.POST.family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
    fp = PRE.family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
    rel = (b["lower"] - f["lower"]) / b["lower"]
    good = (f["argmax"] == b["argmax"] == fp["argmax"]
            and f["lower"] <= b["lower"] and f["lower"] <= fp["lower"]
            and 0.0 <= rel <= R.BUDGET and rel < 1e-11
            and f["rejected"] == 0 and f["saturated"] == 0)
    ok8 = ok8 and good
    rows.append((alpha, gamma, int(b["J"]), rel, f["argmax"]))
gate("the banked v10 bracket rows move down only, by the deflation, same argmax",
     ok8,
     "; ".join(f"(a={a},g={g},J={J}) -{rel:.3e} argmax {am}"
               for a, g, J, rel, am in rows)
     + f" -- all <= the {R.BUDGET:.0e} budget, 0 candidates rejected or "
     "saturated on any production row. The full seven rows (J up to 1600) are in "
     "writeup/data/p2_route_olb_v1_postrepair.json")

# --------------------------------------------------------------------------
# 9 -- the 307.878-decade headroom, checked where the repair can be blamed
# --------------------------------------------------------------------------
hd, ok9 = [], True
for J in (200, 300):
    col, A, dom, cod = R._setup(J, 1.5, 0.5)
    imgs = {}
    for tag, mod in (("post", R.POST), ("pre", PRE)):
        worst = 0.0
        for _name, g in mod.smooth_family(col.theta, cod.w, n_centre=8, n_step=8):
            g = g.copy()
            g[0] = 0.0
            worst = max(worst, float(np.max(np.abs(A @ g))))
        imgs[tag] = worst
    dec = float(np.log10(np.finfo(float).max / imgs["post"]))
    ok9 = ok9 and imgs["post"] == imgs["pre"] and abs(dec - R.HEADROOM_BANKED[J]) < 1e-12
    hd.append((J, dec, imgs["post"] == imgs["pre"]))
gate("the production headroom is bit-identical between the two modules",
     ok9,
     "; ".join(f"J={J}: {d:.6f} decades, family images bit-identical to "
               f"pre-repair: {same}" for J, d, same in hd)
     + ". The headroom is set entirely by the candidate family, so bit-identity "
     "is the clause that tests the REPAIR; comparing to the banked literal "
     "instead would carry the environment floor gate 10 measures")

# --------------------------------------------------------------------------
# 10 -- what bounds how much clause (b) can ever prove
# --------------------------------------------------------------------------
col, A, dom, cod = R._setup(400, 1.5, 0.5)
fp = PRE.family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
f = R.POST.family_lower(A, dom, cod, col.theta, n_centre=30, n_step=40)
row = [b for b in BANKED["w1_ladder"]["ladder"] if b["J"] == 400][0]
FLOOR = abs(row["lower"] - fp["lower"]) / row["lower"]
MOVE = (fp["lower"] - f["lower"]) / fp["lower"]
gate("the repair's move stands clear of the banked literals' own noise floor",
     FLOOR < 1e-13 and MOVE > 10.0 * max(FLOOR, 1e-17),
     f"the reconstructed PRE-repair module lands {FLOOR:.3e} relative from the "
     f"banked literal at J=400 (not bitwise; np.linalg.inv's cross-build floor, "
     f"reaching 2.26e-14 at J=1600), while the repair's own deflation is "
     f"{MOVE:.3e} -- {MOVE / max(FLOOR, 1e-17):.0f}x the floor. "
     "p2_route_ola_v1_bench_check.py grades against those literals without "
     "measuring this, so the ratio, not the raw move, is the honest magnitude")

# --------------------------------------------------------------------------
try:
    os.unlink(PRE.__source_path__)
except OSError:
    pass

n_fail = sum(1 for r in results if r[0] == FAIL)
print(f"\n{len(results) - n_fail}/{len(results)} gates pass")
print("Route-OLB, leg 132: these gates are the independent re-run of leg 101's "
      "battery that DIRECTION.md's yes-branch asked to be banked. Gate 5 is the "
      "control -- if it ever stops failing the pre-repair module, the grader is "
      "broken and gates 1-4 mean nothing. A failure in gates 4/6/7 is a "
      "SOUNDNESS regression; in 8/9/10 a non-regression breach. Either way the "
      "fix belongs in solver/op_lower.py, never in these gates.")
sys.exit(1 if n_fail else 0)
