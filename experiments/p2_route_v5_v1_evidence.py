#!/usr/bin/env python3
"""
p2_route_v5_v1_evidence.py -- leg 402, unit V5.

Re-derives EVERY recomputable constant of arXiv:2509.25116v2 from the artefact
writeup/data/p2_route_v5_audit_v1.json, using ONLY

  * the Class-A interval-arithmetic inputs banked in that artefact, and
  * the paper's OWN rounded downstream values banked in that artefact,

and checks each result against the number the artefact banked as `recomputed`.

EXITS NON-ZERO on any disagreement.

This script is deliberately not allowed to reach outside the artefact for a
number.  If the artefact is wrong, this script fails.  That is the point: the
artefact is what is under test, not the paper.

What this script does NOT do
----------------------------
It does not verify the authors' interval arithmetic (Class A, H1-H21).  Those
outputs are UNRECOMPUTABLE-BY-DESIGN here and are banked as a LIMIT OF THIS
AUDIT, never as a pass.  Nothing below should be read as certifying them.

Usage:  python3 experiments/p2_route_v5_v1_evidence.py
Requires: mpmath
"""

import json
import hashlib
import os
import sys

try:
    from mpmath import mp, mpf, sqrt, pi
except ImportError:
    sys.stderr.write("FATAL: mpmath is required (pip install mpmath)\n")
    sys.exit(3)

mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ART = os.path.join(ROOT, "writeup", "data", "p2_route_v5_audit_v1.json")

# 12 significant digits: the precision at which the artefact banks its numbers.
SIG = mpf("1e-12")

failures = []
checks = 0


def fail(msg):
    failures.append(msg)
    print("  FAIL  " + msg)


def ok(msg):
    print("  ok    " + msg)


def relclose(a, b, tol=SIG):
    a, b = mpf(a), mpf(b)
    if b == 0:
        return abs(a) < tol
    return abs(a - b) / abs(b) < tol


def matches_banked(val, banked_str):
    """Agreement AT THE PRECISION THE ARTEFACT ACTUALLY BANKS.

    The artefact stores 12 significant digits, so testing at 1e-12 relative
    would be testing below the banked precision and would fail on the last
    banked digit -- a tolerance artefact, not a disagreement.  The honest test
    is: does the re-derivation round to the same 12 significant digits?  A
    slightly loosened numeric test is kept as a fallback so that a genuine
    formatting difference cannot be mistaken for a numerical one.
    """
    if mp.nstr(val, 12) == banked_str:
        return True
    return relclose(val, mpf(banked_str), mpf("1e-11"))


# --------------------------------------------------------------- load artefact
if not os.path.exists(ART):
    sys.stderr.write("FATAL: artefact not found: %s\n" % ART)
    sys.exit(3)

doc = json.load(open(ART))

print("=" * 78)
print("V5 EVIDENCE -- re-derivation of arXiv:2509.25116v2's recomputable constants")
print("artefact: writeup/data/p2_route_v5_audit_v1.json")
print("=" * 78)

# --------------------------------------------------------------- 0. self_hash
print("\n[0] artefact self_hash")
banked = doc.get("self_hash")
stripped = {k: v for k, v in doc.items() if k != "self_hash"}
recomputed_hash = hashlib.sha256(
    json.dumps(stripped, sort_keys=True).encode()).hexdigest()[:16]
checks += 1
if banked == recomputed_hash:
    ok("self_hash %s reproduces" % banked)
else:
    fail("self_hash banked=%s recomputed=%s -- ARTEFACT HAS BEEN MUTATED"
         % (banked, recomputed_hash))

# --------------------------------------------------------------- 1. namespace
enum = doc["CLAUSE_1"]["constant_enumeration"]
classA = enum["class_A_UNRECOMPUTABLE_BY_DESIGN"]["values"]
rounded = enum["paper_rounded_values_used_downstream_by_the_paper_itself"]

ns = {"mpf": mpf, "sqrt": sqrt, "pi": pi}
for k, v in classA.items():
    ns[k] = mpf(v)
for k, v in rounded.items():
    ns[k] = mpf(v)

print("\n[1] namespace")
print("    Class-A inputs (UNRECOMPUTABLE-BY-DESIGN, taken as given): %d"
      % len(classA))
print("    paper's own rounded downstream values: %d" % len(rounded))

# --------------------------------------------------------------- 2. Class B
rows = enum["class_B_RECOMPUTABLE"]["rows"]
print("\n[2] Class-B re-derivation (%d rows, mpmath at %d dps)" % (len(rows), mp.dps))
print("    %-6s %-14s %-20s %s" % ("id", "printed", "artefact says", "re-derived"))

for r in rows:
    rid = r["id"]
    try:
        val = eval(r["expr"], {"__builtins__": {}}, ns)  # noqa: S307
    except Exception as e:  # pragma: no cover
        fail("%s expression did not evaluate: %s (%s)" % (rid, r["expr"], e))
        continue
    ns[rid] = val
    checks += 1

    banked_val = r["recomputed"]
    got = mp.nstr(val, 12)
    print("    %-6s %-14s %-20s %s" % (rid, r["printed"], banked_val, got))

    # (a) does the re-derivation reproduce what the artefact banked?
    if not matches_banked(val, banked_val):
        fail("%s re-derivation %s != artefact's banked recomputed %s"
             % (rid, got, banked_val))

    # (b) does the agrees/disagrees flag hold, in the relation the artefact
    #     declares?  This is what makes the four failures load-bearing rather
    #     than decorative.
    printed = mpf(r["printed"])
    rel = r["relation"]
    if rel == "<=":
        holds = val <= printed
    elif rel in (">=", "!>="):
        holds = val >= printed
    elif rel == "==":
        holds = (val == printed)
    elif rel == "approx":
        holds = abs(val - printed) < mpf("5e-5")
    else:
        fail("%s unknown relation %r" % (rid, rel))
        continue
    checks += 1
    if bool(holds) != bool(r["agrees"]):
        fail("%s: artefact claims agrees=%s under relation '%s' vs printed %s, "
             "but re-derivation gives %s (holds=%s)"
             % (rid, r["agrees"], rel, r["printed"], got, holds))

# --------------------------------------------------- 3. the four named failures
print("\n[3] the four constants the artefact names as FAILING to recompute")
named = doc["CLAUSE_1"]["constants_that_FAILED_to_recompute"]
row_by_id = {r["id"]: r for r in rows}
disagreeing = sorted(r["id"] for r in rows if not r["agrees"])
claimed = sorted(f["id"] for f in named)
checks += 1
if disagreeing == claimed:
    ok("the set of disagreeing rows is exactly %s, as claimed" % claimed)
else:
    fail("disagreeing rows %s != the artefact's named failures %s"
         % (disagreeing, claimed))

for f in named:
    r = row_by_id.get(f["id"])
    checks += 1
    if r is None:
        fail("%s named as a failure but absent from the Class-B table" % f["id"])
        continue
    if f["printed"] != r["printed"] or f["recomputed"] != r["recomputed"]:
        fail("%s: the failure entry's numbers (%s vs %s) disagree with the "
             "Class-B row's (%s vs %s)"
             % (f["id"], f["printed"], f["recomputed"], r["printed"], r["recomputed"]))
    else:
        ok("%s printed %s vs recomputed %s -- both numbers consistent across "
           "the artefact" % (f["id"], f["printed"], f["recomputed"]))

# H30's diagnosis is the substantive one: check BOTH substitutions explicitly.
print("\n    H30's diagnosis, checked directly:")
h30 = [f for f in named if f["id"] == "H30"][0]
x0_wrong = 2 * ns["epsU"] / (mpf("0.25") - ns["eta1"] - ns["eta2"] + sqrt(ns["p_M4U"]))
x0_right = 2 * ns["epsU"] / (mpf("0.25") - ns["eta1"] - ns["p_M2U"] + sqrt(ns["p_M4U"]))
checks += 2
if matches_banked(x0_wrong, h30["with_the_papers_own_substituted_0.005"]):
    ok("substituting eta_2 = 0.005 reproduces %s, the paper's route"
       % mp.nstr(x0_wrong, 12))
else:
    fail("eta_2 substitution gives %s, artefact says %s"
         % (mp.nstr(x0_wrong, 12), h30["with_the_papers_own_substituted_0.005"]))
if matches_banked(x0_right, h30["with_the_correct_M_2^U_bound_0.0061"]):
    ok("using the certified M_2^U <= 0.0061 reproduces %s, the correct value"
       % mp.nstr(x0_right, 12))
else:
    fail("M_2^U substitution gives %s, artefact says %s"
         % (mp.nstr(x0_right, 12), h30["with_the_correct_M_2^U_bound_0.0061"]))

# H28: 4 eps^U is 2.6e-6 exactly, not the printed 2.8e-6.
checks += 1
if 4 * ns["epsU"] == mpf("2.6e-6"):
    ok("H28: 4 eps^U = 2.6e-6 exactly; the paper prints 2.8e-6 (CONSERVATIVE)")
else:
    fail("H28: 4 eps^U = %s, expected 2.6e-6" % mp.nstr(4 * ns["epsU"], 12))

# ------------------------------------------------- 4. the closure conditions
print("\n[4] closure conditions -- does the certificate close on the CORRECTED chain?")
cc = doc["CLAUSE_1"]["closure_conditions"]
sym = {"M_4^U > 0 (the discriminant of the U-step)": ("H29", lambda v: v > 0),
       "M_4^v >= 0.021 (the discriminant of the v-step)": ("H39d", lambda v: v >= mpf("0.021")),
       "|lambda| <= 0.0045 (the eigenvalue perturbation bound)": ("H41b", lambda v: v <= mpf("0.0045")),
       "x_1^U <= 6.2e-6 (the tightest surviving margin)": ("H31", lambda v: v <= mpf("6.2e-6"))}
all_hold = True
for c in cc:
    rid, pred = sym[c["condition"]]
    val = ns[rid]
    checks += 2
    if not matches_banked(val, c["recomputed"]):
        fail("%s: banked %s, re-derived %s" % (c["condition"], c["recomputed"],
                                               mp.nstr(val, 12)))
    holds = bool(pred(val))
    if holds != bool(c["holds"]):
        fail("%s: artefact claims holds=%s, re-derivation gives %s"
             % (c["condition"], c["holds"], holds))
    else:
        ok("%s -> %s (%s)" % (c["condition"], holds, mp.nstr(val, 12)))
    all_hold = all_hold and holds

# the 0.08% margin on x_1^U, stated as luck rather than comfort
margin = (mpf("6.2e-6") - ns["H31"]) / mpf("6.2e-6") * 100
checks += 1
if abs(margin - mpf("0.08")) < mpf("0.01"):
    ok("x_1^U margin is %s%% -- LUCK, NOT MARGIN, as the artefact states"
       % mp.nstr(margin, 3))
else:
    fail("x_1^U margin re-derives as %s%%, artefact claims 0.08%%"
         % mp.nstr(margin, 3))

# ---------------------------------------------- 5. the verdicts are consistent
print("\n[5] verdict consistency")
c1 = doc["CLAUSE_1"]["ANSWER"]
c2 = doc["CLAUSE_2"]["ANSWER"]
checks += 1
if c1 == "YES" and all_hold:
    ok("CLAUSE 1 = YES is consistent: every closure condition holds on the "
       "corrected chain")
elif c1 == "NO" and not all_hold:
    ok("CLAUSE 1 = NO is consistent: a closure condition fails")
else:
    fail("CLAUSE 1 = %s but all_closure_conditions_hold = %s -- INCONSISTENT"
         % (c1, all_hold))

checks += 1
if doc["CLAUSE_1"]["branch_taken"] == "B1_PARTIAL" and len(named) > 0 and all_hold:
    ok("branch B1_PARTIAL is the right branch: %d constants disagree, closure "
       "survives" % len(named))
else:
    fail("branch %s does not match %d disagreements with all_hold=%s"
         % (doc["CLAUSE_1"]["branch_taken"], len(named), all_hold))

# clause 2 must not be conditioned on clause 1
checks += 1
if doc["CLAUSE_2"].get("answered_standing_alone") is True and \
        doc["CLAUSE_2"].get("NOT_FOLDED_INTO_CLAUSE_1"):
    ok("CLAUSE 2 = %s is banked as answered standing alone, per the gate" % c2)
else:
    fail("CLAUSE 2 is not marked as answered standing alone -- the gate "
         "forbids folding it into clause 1")

# clause 2's predicate: 3D iff the conjunction FAILS
conj = doc["CLAUSE_2"]["predicate_applied_conjunct_by_conjunct"]
lift = all(bool(x["holds"]) for x in conj)
checks += 1
if (c2 == "YES") == (not lift):
    ok("CLAUSE 2 = %s is consistent with the conjuncts (%s) -- 2D lift = %s"
       % (c2, [bool(x["holds"]) for x in conj], lift))
else:
    fail("CLAUSE 2 = %s but the conjunction gives lift=%s" % (c2, lift))

# the swirl fraction, re-derived from the measurements
m = doc["CLAUSE_2"]["measurements"]
frac = mpf(repr(m["u3_u_phi_max_abs"])) / mpf(repr(m["u1_u_r_max_abs"]))
checks += 1
if abs(frac - mpf(repr(m["u_phi_as_fraction_of_u_r"]))) < mpf("1e-4"):
    ok("swirl fraction re-derives: max|u_phi|/max|u_r| = %s" % mp.nstr(frac, 6))
else:
    fail("swirl fraction re-derives as %s, artefact banks %s"
         % (mp.nstr(frac, 6), m["u_phi_as_fraction_of_u_r"]))

# u_phi must be nonzero for L2 to fail
checks += 1
if m["u3_u_phi_max_abs"] > 0 and not conj[1]["holds"]:
    ok("L2 fails because max|u_phi| = %s > 0 -- the profile HAS swirl"
       % m["u3_u_phi_max_abs"])
else:
    fail("L2's status is inconsistent with the measured swirl %s"
         % m["u3_u_phi_max_abs"])

# ---------------------------------------------- 6. standing discipline checks
print("\n[6] standing discipline")
checks += 1
if doc.get("tier") == 2 and doc.get("clay_probability_unchanged") == 0.05:
    ok("Tier 2, Clay unchanged at 0.05% -- no link of L1->L4 moved")
else:
    fail("tier/Clay fields are not as the standing rule requires")

checks += 1
if doc["second_deliverable"]["no_v1_edited"] is True:
    ok("no _v1 artefact was edited; repair issued as _v2 deltas")
else:
    fail("the artefact does not attest that _v1 files were left untouched")

checks += 1
if doc["journal_ref_observation"]["OBSERVED_NOT_GRADED_NOT_RULED"] is True:
    ok("journal-ref: observed, not graded, not ruled (dispatch reading e)")
else:
    fail("journal-ref observation is not marked observe-only")

# --------------------------------------------------------------------- verdict
print("\n" + "=" * 78)
if failures:
    print("RESULT: FAILED -- %d of %d checks disagreed" % (len(failures), checks))
    for f in failures:
        print("   * " + f)
    print("=" * 78)
    sys.exit(1)

print("RESULT: PASSED -- all %d checks agree" % checks)
print("")
print("  CLAUSE 1 = %s  (branch %s): the certificate DOES close as claimed."
      % (c1, doc["CLAUSE_1"]["branch_taken"]))
print("             four printed constants fail to recompute (%s);"
      % ", ".join(sorted(f["id"] for f in named)))
print("             carrying the corrected values through, closure survives.")
print("  CLAUSE 2 = %s  (branch %s), ANSWERED STANDING ALONE: the certified"
      % (c2, doc["CLAUSE_2"]["branch_taken"]))
print("             profile IS genuinely 3D. W2's predicate fails on all three")
print("             conjuncts; the swirl is 57%% of the radial component.")
print("")
print("  NEITHER ANSWER MOVES A LINK OF L1->L4. Tier 2. Clay ~0.05%.")
print("=" * 78)
sys.exit(0)
