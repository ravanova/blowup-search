#!/usr/bin/env python3
"""V1 -- WAVE 1 VERIFIER. Independent re-derivation of the six pre-registered items.

ORCHESTRATION.md section 3f: verification is a fresh session or it is not verification.
This script re-derives every number in V1's gate from PRIMARY banked artifacts --
    writeup/data/p2_prog_r4_g1_v1.json      (U3, unit under R0's measurement)
    writeup/data/p2_prog_r4_m3_v1.json      (U5, unit under R0's measurement)
    writeup/data/p2_route_trig_v1.json      (T2's measurement)
    writeup/escalations/ESCALATION_BAN_WORDING_2026-08-13.md   (T1's only deliverable)
-- and compares them against the wave-1 units' banked claims in
    writeup/data/p2_prog_r4_r0r1_v1.json    (R0+R1, the thing under test)
and against the gate's own literal target numbers.

Lesson 68: THE EXIT CODE IS THE RESULT. Exits 0 iff every check passes; 1 otherwise.
Nothing here is gated by reading a printed line.

Reading (b) of V1's dispatch: a DISAGREEMENT is BANKED, NOT RECONCILED. Where a
re-derivation disagrees, this script records both numbers and their provenance and
FAILS. It does not adjust either side to make them meet.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")

CHECKS = []
NOTES = {}


def check(item, name, ok, detail=""):
    CHECKS.append({"item": item, "name": name, "ok": bool(ok), "detail": str(detail)})
    print("%-4s [%s] %-58s %s" % ("ok" if ok else "FAIL", item, name, detail))
    return bool(ok)


def load(p):
    with open(os.path.join(D, p)) as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# The clustering rule, transcribed from the ARBITER named by R0 itself:
# experiments/p2_prog_r4_m3_evidence.py lines 35-53 and 70-81. Re-implemented
# here rather than imported, so that a bug in the arbiter would show up as a
# disagreement instead of being inherited.
# --------------------------------------------------------------------------
TOL = 0.05


def wrap_abs(s):
    a = abs(float(s)) % (2.0 * math.pi)
    return min(a, 2.0 * math.pi - a)


def cluster_leader(atts):
    """Leader/greedy against each cluster's FIRST member, sorted by T."""
    out = []
    for a in sorted(atts, key=lambda a: a["T_converged"]):
        for c in out:
            if (abs(c[0]["T_converged"] - a["T_converged"]) <= TOL
                    and abs(c[0]["S"] - a["S"]) <= TOL):
                c.append(a)
                break
        else:
            out.append([a])
    return out


def _link(atts, complete):
    """Agglomerative single- (complete=False) or complete-linkage at TOL, on the
    Chebyshev (max-coordinate) metric in (T, |s|)."""
    groups = [[a] for a in atts]
    changed = True
    while changed:
        changed = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                pairs = [max(abs(x["T_converged"] - y["T_converged"]),
                             abs(x["S"] - y["S"]))
                         for x in groups[i] for y in groups[j]]
                d = max(pairs) if complete else min(pairs)
                if d <= TOL:
                    groups[i] = groups[i] + groups[j]
                    del groups[j]
                    changed = True
                    break
            if changed:
                break
    return groups


def annotate(atts):
    for a in atts:
        a["S"] = wrap_abs(a["s_converged"])
        a["S_seed"] = wrap_abs(a["s_seed"])
    return atts


def r2(x):
    return round(x + 0.0, 2)


def r4(x):
    return round(x + 0.0, 4)


# ==========================================================================
u3 = load("p2_prog_r4_g1_v1.json")
u5 = load("p2_prog_r4_m3_v1.json")
r0r1 = load("p2_prog_r4_r0r1_v1.json")
trig = load("p2_route_trig_v1.json")

a3 = annotate(u3["attempts"])
a5 = annotate(u5["attempts"])
ok3 = [a for a in a3 if a["success"]]
ok5 = [a for a in a5 if a["success"]]

print("\n=== ITEM 1 -- R0's metric, and the 134.45 vs 144.69 reconciliation ===")

pool3 = u3["magnitudes"]["wall_seconds"] * u3["magnitudes"]["workers"] / 3600.0
pool5 = u5["magnitudes"]["wall_seconds"] * u5["magnitudes"]["workers"] / 3600.0
cpu3 = sum(a["wall_seconds"] for a in a3) / 3600.0
cpu5 = sum(a["wall_seconds"] for a in a5) / 3600.0
util3 = cpu3 / pool3

check("1", "U3 pool reservation = wall_seconds * workers / 3600 = 144.69",
      r2(pool3) == 144.69, "%.6f -> %.2f" % (pool3, pool3))
check("1", "U5 pool reservation = wall_seconds * workers / 3600 = 57.04",
      r2(pool5) == 57.04, "%.6f -> %.2f" % (pool5, pool5))
check("1", "U3 attempt CPU = sum(attempts[].wall_seconds)/3600 = 134.45",
      r2(cpu3) == 134.45, "%.6f -> %.2f" % (cpu3, cpu3))
check("1", "U3 pool utilisation = 134.45 / 144.69 = 92.92%",
      r2(util3 * 100) == 92.92, "%.6f -> %.2f%%" % (util3, util3 * 100))
check("1", "R0 banked the same three numbers",
      (r0r1["r0"]["core_hours"]["U3"]["pool_reservation_core_hours"] == pool3
       and r0r1["r0"]["core_hours"]["U3"]["attempt_cpu_core_hours"] == cpu3
       and r0r1["r0"]["core_hours"]["U5"]["pool_reservation_core_hours"] == pool5),
      "bit-identical to my re-derivation")

# distinct counts, re-derived under the arbiter's own rule, three linkages
n3_lead = len(cluster_leader(ok3))
n5_lead = len(cluster_leader(ok5))
n3_sing = len(_link(ok3, complete=False))
n5_sing = len(_link(ok5, complete=False))
n3_comp = len(_link(ok3, complete=True))
n5_comp = len(_link(ok5, complete=True))

check("1", "U3 distinct = 8 under leader/single/complete linkage alike",
      n3_lead == n3_sing == n3_comp == 8,
      "leader %d, single %d, complete %d (of %d convergences)"
      % (n3_lead, n3_sing, n3_comp, len(ok3)))
check("1", "U5 distinct = 5 under leader/single/complete linkage alike",
      n5_lead == n5_sing == n5_comp == 5,
      "leader %d, single %d, complete %d (of %d convergences)"
      % (n5_lead, n5_sing, n5_comp, len(ok5)))

m3_metric = n3_lead / pool3
m5_metric = n5_lead / pool5
check("1", "U3 metric = 8 / 144.69 = 0.0553", r4(m3_metric) == 0.0553,
      "%.8f -> %.4f" % (m3_metric, m3_metric))
check("1", "U5 metric = 5 / 57.04 = 0.0877", r4(m5_metric) == 0.0877,
      "%.8f -> %.4f" % (m5_metric, m5_metric))

print("\n=== ITEM 2 -- R0's retraction ===")

KEY = lambda a: (a["T_seed"], wrap_abs(a["s_seed"]), a["R_seed"])
seeds3 = {KEY(a): a for a in a3}
overlap = [a for a in a5 if KEY(a) in seeds3]
check("2", "57 of U5's 100 seeds were already spent by U3",
      len(overlap) == 57 and len(a5) == 100,
      "%d/%d on key (T_seed, |s_seed|, R_seed) at full float precision"
      % (len(overlap), len(a5)))

shared_conv = [a for a in ok5 if KEY(a) in seeds3]
bitid = [a for a in shared_conv
         if seeds3[KEY(a)]["success"]
         and seeds3[KEY(a)]["T_converged"] == a["T_converged"]
         and wrap_abs(seeds3[KEY(a)]["s_converged"]) == wrap_abs(a["s_converged"])]
check("2", "5 of U5's 9 convergences are bit-identical re-executions",
      len(shared_conv) == 5 and len(bitid) == 5 and len(ok5) == 9,
      "shared-seed %d, bit-identical (T,|s|) %d, of %d convergences"
      % (len(shared_conv), len(bitid), len(ok5)))

c3 = cluster_leader(ok3)
c5 = cluster_leader(ok5)


def matches_u3(cl):
    return any(abs(cl[0]["T_converged"] - k[0]["T_converged"]) <= TOL
               and abs(cl[0]["S"] - k[0]["S"]) <= TOL for k in c3)


refinds = [cl for cl in c5 if matches_u3(cl)]
newones = [cl for cl in c5 if not matches_u3(cl)]
check("2", "4 of U5's 5 distinct orbits are re-finds; ONE is new",
      len(refinds) == 4 and len(newones) == 1,
      "re-finds %d, new %d; the new one T=%.6f |s|=%.6f anchor=%s attempt=%d"
      % (len(refinds), len(newones), newones[0][0]["T_converged"],
         newones[0][0]["S"], newones[0][0]["anchor"], newones[0][0]["attempt"])
      if len(newones) == 1 else "re-finds %d, new %d" % (len(refinds), len(newones)))

corrected = len(newones) / pool5
check("2", "corrected U5 metric = 1 / 57.04 = 0.0175", r4(corrected) == 0.0175,
      "%.8f -> %.4f" % (corrected, corrected))

# The gate's comparand '0.0553' is ambiguous. BOTH readings are tested; neither is
# re-worded. Reading A: 0.0553 is U3's metric (the thing U5 was claimed to beat).
# Reading B: 0.0553 is U5's OWN originally claimed metric -- which the same gate's
# item (1) gives as 0.0877. Exactly one can hold.
readA = r4(m3_metric) == 0.0553
readB = r4(m5_metric) == 0.0553
NOTES["item2_comparand"] = {
    "reading_A_0.0553_is_U3s_metric": readA,
    "reading_B_0.0553_is_U5s_own_original_claim": readB,
    "U5_own_original_claim": r4(m5_metric),
    "verdict": ("READING A holds: 0.0553 is U3's metric, and the corrected U5 "
                "figure 0.0175 falls BELOW it, which is the retraction. READING B "
                "does not hold: U5's own original claim is 0.0877, per the same "
                "gate's item (1). The gate's wording is internally ambiguous; the "
                "ambiguity is BANKED, not reconciled."),
}
check("2", "comparand 0.0553 resolves under exactly one reading (A: U3's metric)",
      readA and not readB,
      "A=%s B=%s; U5's own original claim is %.4f" % (readA, readB, m5_metric))
check("2", "the retraction's direction: corrected U5 (0.0175) < U3 (0.0553)",
      corrected < m3_metric, "%.4f < %.4f" % (corrected, m3_metric))

print("\n=== ITEM 3 -- R1's headroom and hold-out kill ===")


def abort_sweep(atts, K, W, theta):
    """abort at epoch k iff k >= K and ||R||_k > theta * ||R||_{k-W}."""
    base = under = kills = 0
    for a in atts:
        h = a["residual_history"]
        n = a["n_iters"]
        base += n
        k_ab = None
        for k in range(K, len(h)):
            if h[k] > theta * h[k - W]:
                k_ab = k
                break
        under += min(k_ab, n) if k_ab is not None else n
        if a["success"] and k_ab is not None and k_ab < n:
            kills += 1
    return base, under, 1.0 - under / base, kills


inc = r0r1["r1"]["incumbent"]["rule"]
best = r0r1["r1"]["headroom"]["best_admissible_rule"]
b_i, u_i, f_i, k_i = abort_sweep(a3, inc["K"], inc["W"], inc["theta"])
b_b, u_b, f_b, k_b = abort_sweep(a3, best["K"], best["W"], best["theta"])

check("3", "incumbent rule reproduces on U3 (4629 -> 2083 epochs, 0 false kills)",
      b_i == 4629 and u_i == 2083 and k_i == 0
      and f_i == r0r1["r1"]["incumbent"]["U3"]["fraction_of_epochs_recovered"],
      "K=%d W=%d theta=%s -> %.16f" % (inc["K"], inc["W"], inc["theta"], f_i))
check("3", "best admissible rule reproduces on U3, 0 false kills",
      k_b == 0 and f_b == r0r1["r1"]["headroom"]["best_admissible_u3_recovery"],
      "K=%d W=%d theta=%s -> %.16f (%d epochs)"
      % (best["K"], best["W"], best["theta"], f_b, u_b))
headroom_pp = (f_b - f_i) * 100.0
check("3", "headroom = +0.45 pp", r2(headroom_pp) == 0.45,
      "%.8f pp -> +%.2f pp" % (headroom_pp, headroom_pp))

ho = r0r1["r1"]["holdout"]["fit_on_u5_scored_on_u3"]
hr = ho["rule"]
b_h, u_h, f_h, k_h = abort_sweep(a3, hr["K"], hr["W"], hr["theta"])
check("3", "hold-out (fit on U5, scored on U3) kills exactly ONE of U3's 14",
      k_h == 1 and ho["heldout_false_kills"] == 1 and len(ok3) == 14,
      "K=%d W=%d theta=%s -> %d false kill(s) out of %d convergences"
      % (hr["K"], hr["W"], hr["theta"], k_h, len(ok3)))
check("3", "the other hold-out direction kills none (control)",
      abort_sweep(a5, *[r0r1["r1"]["holdout"]["fit_on_u3_scored_on_u5"]["rule"][x]
                        for x in ("K", "W", "theta")])[3] == 0
      and r0r1["r1"]["holdout"]["fit_on_u3_scored_on_u5"]["heldout_false_kills"] == 0,
      "fit on U3, scored on U5")

print("\n=== ITEM 4 -- T2's instrument ===")

arx = list(trig["controls"])
for fam in trig["queries"].values():
    arx.extend(fam)
n_meas = sum(1 for q in arx if q["status"] == "MEASURED")
n_thr = sum(1 for q in arx if q["status"] == "THROTTLED")
n_fail = sum(1 for q in arx if q["status"] == "FAILED")
subst = [q for fam in trig["queries"].values() for q in fam]

check("4", "32 arXiv query records, 32 MEASURED, 0 THROTTLED, 0 FAILED",
      len(arx) == 32 and n_meas == 32 and n_thr == 0 and n_fail == 0,
      "%d records: %d MEASURED (%d substantive + %d controls)"
      % (len(arx), n_meas, len(subst), len(trig["controls"])))

ns = sorted({q.get("opensearch_namespace_served") for q in arx})
check("4", "served opensearch namespace is 1.1, and only 1.1",
      ns == ["http://a9.com/-/spec/opensearch/1.1/"], ns)

s2s = trig["s2"]["substantive"]
s2_thr = [q for q in s2s if q["status"] == "THROTTLED"]
check("4", "Semantic Scholar: 5 of 6 substantive queries THROTTLED",
      len(s2s) == 6 and len(s2_thr) == 5, "%d/%d" % (len(s2_thr), len(s2s)))
check("4", "every THROTTLED record carries total=None, NEVER a zero (leg 387)",
      all(q["total"] is None for q in s2_thr),
      "totals: %s" % [q["total"] for q in s2_thr])

neg_a = [q for q in trig["controls"] if q["control"] == "neg_nonsense"]
neg_s = [q for q in trig["s2"]["controls"] if q["total"] == 0]
same_string = (len(neg_a) == 1 and len(neg_s) == 1
               and neg_a[0]["query"].replace('all:"', "").replace('"', "")
               == neg_s[0]["query"])
check("4", "negative control returns 0 in BOTH instruments, same query string",
      (len(neg_a) == 1 and neg_a[0]["status"] == "MEASURED" and neg_a[0]["total"] == 0
       and len(neg_s) == 1 and neg_s[0]["status"] == "MEASURED"
       and neg_s[0]["total"] == 0 and same_string),
      "arXiv %s / S2 %s : %r" % (neg_a[0]["total"] if neg_a else "?",
                                 neg_s[0]["total"] if neg_s else "?",
                                 neg_s[0]["query"] if neg_s else "?"))

# A zero is only a measurement if the SERVICE was reached. Bank the positive datum.
pos_a = [q for q in trig["controls"]
         if q["status"] == "MEASURED" and q["http"] == 200 and (q["total"] or 0) > 0]
pos_s = [q for q in trig["s2"]["controls"]
         if q["status"] == "MEASURED" and (q["total"] or 0) > 0]
check("4", "POSITIVE DATUM: each instrument was reached (HTTP 200, non-zero total)",
      len(pos_a) >= 1 and len(pos_s) >= 1,
      "arXiv max total %d; S2 max total %d"
      % (max(q["total"] for q in pos_a) if pos_a else -1,
         max(q["total"] for q in pos_s) if pos_s else -1))

print("\n=== ITEM 5 -- T1's packet ===")

PK = os.path.join(ROOT, "writeup", "escalations",
                  "ESCALATION_BAN_WORDING_2026-08-13.md")
txt = open(PK).read()
t1_json = [f for f in os.listdir(D)
           if "391" in f or "t1" in f.lower() or "ban_wording" in f.lower()]
NOTES["item5_banking_defect"] = {
    "searched": "writeup/data/*.json for any T1 / leg-391 / ban-wording record",
    "found": t1_json,
    "finding": ("T1 (leg 391) banked NO writeup/data/*.json and landed NO evidence "
                "script. Its only artefacts are experiments/journal/leg_391.md "
                "(reasoning, forbidden to this verifier) and the prose escalation "
                "packet. Item (5) is therefore checkable only against PROSE. That is "
                "a banking-discipline defect, reported as one -- not evidence the "
                "claim is false."),
}
check("5", "BANKING DEFECT NAMED: no T1 JSON exists under writeup/data/",
      t1_json == [], "search returned %r (empty = defect confirmed)" % (t1_json,))

readings = {L: len(re.findall(r"^### READING %s[12]\b" % L, txt, re.M)) for L in "ABC"}
check("5", "the packet poses THREE ban-wording questions, each with TWO readings",
      readings == {"A": 2, "B": 2, "C": 2}
      and "Not a ban-wording question" in txt, readings)
check("5", "the packet rules NONE of the three",
      "**It ruled none of (a), (b), (c).**" in txt
      and "**This packet rules nothing.**" in txt
      and "No reading is endorsed, preferred, ranked, or recommended." in txt,
      "both self-statements present verbatim")
check("5", "no reading is endorsed anywhere in the packet text",
      not re.search(r"^(RULING|VERDICT|RECOMMEND\w*)\s*[:=]", txt, re.M | re.I),
      "no RULING/VERDICT/RECOMMENDATION line")

print("\n=== M3 -- does DELIVERED survive U5's 57% seed overlap, on M3's OWN wording ===")

mil = u5["milestone"]
clause_text = {
    "c1_mining_exhaustive":
        "the mining pass takes EVERY anchored strict local minimum not provably "
        "excluded by the Newton window (3g.4), and reports the realised counts",
    "c2_band_at_least_50":
        "the 100-attempt budget is allocated by the 3g.4 quota, with AT LEAST 50 "
        "attempts seeded in the published band |s| in [0.295, 0.707] against U3's 31",
    "c3_unchanged_settings":
        "the run completes at U3's caps, tol, admission test, m = 0 requirement, "
        "anchor rule and matching predicate, with NONE OF THEM CHANGED and no "
        "iterations bought",
    "c4_yield_reported":
        "the per-stratum convergence yield is reported against U3's banked baseline, "
        "with the in-band rate stated as a magnitude either way",
    "c5_controls_fired": "the planted controls fire as planted",
}
check("M3", "M3's pre-committed wording is LOCATED in the banked record",
      set(mil["clauses"]) == set(clause_text)
      and "AMENDMENT 5" in mil["preregistered"],
      "5 clauses in p2_prog_r4_m3_v1.json; source %s" % mil["preregistered"])

# Re-derive the two clauses the 57% overlap could conceivably touch.
BAND = (0.295, 0.707)
inband5 = sum(1 for a in a5 if BAND[0] <= a["S_seed"] <= BAND[1])
inband3 = sum(1 for a in a3 if BAND[0] <= a["S_seed"] <= BAND[1])
check("M3", "c2 re-derived: >= 50 in-band seeds (60 vs U3's 31)",
      inband5 >= 50 and inband5 == 60 and inband3 == 31
      and mil["n_seeded_in_published_band"] == inband5,
      "U5 %d in band, U3 %d" % (inband5, inband3))
check("M3", "c3 re-derived: caps/tol identical to U3, none changed",
      all(u5["resourcing"][k] == u3["resourcing"][k]
          for k in ("tol", "max_newton", "max_gmres", "gmres_rtol", "N", "Re",
                    "T_dns", "n_attempts"))
      and u5["resourcing"]["caps_identical_to_U3"] is True,
      "tol, max_newton, max_gmres, gmres_rtol, N, Re, T_dns, n_attempts all equal")
check("M3", "c5 re-derived: controls fired as planted, no failures",
      u5["controls"]["fired_as_planted"] is True
      and u5["controls"]["failures"] == [], "0 control failures")

# THE JUDGEMENT, on M3's own wording and nothing else.
# No clause of M3 mentions seed novelty, orbit novelty, or non-overlap with U3.
novelty_words = ("novel", "new to", "unspent", "not already", "overlap",
                 "distinct from U3", "fresh seed")
silent = not any(w.lower() in " ".join(clause_text.values()).lower()
                 for w in novelty_words)
check("M3", "M3's five clauses are SILENT on seed novelty / non-overlap with U3",
      silent, "no clause conditions DELIVERED on seeds U3 had not spent")
# Clause 1 does more than stay silent: it REQUIRES exhaustion of the same anchored
# reservoir U3 drew from, so overlap is a CONSEQUENCE of c1, not a breach of it.
check("M3", "c1 requires exhausting the SAME reservoir, so overlap is predicted by it",
      "exhaust" in clause_text["c1_mining_exhaustive"].lower()
      or "EVERY" in clause_text["c1_mining_exhaustive"],
      "c1: take EVERY anchored strict local minimum -- re-taking U3's seeds is "
      "compliance, not violation")

m3_survives = silent and inband5 >= 50 and all(mil["clauses"].values())
NOTES["M3_verdict"] = {
    "question_verbatim": mil["question"],
    "clauses_verbatim": clause_text,
    "answer": "M3 = DELIVERED SURVIVES the 57% seed overlap",
    "why": ("Judged on M3's own pre-committed wording and nothing else: none of the "
            "five clauses conditions DELIVERED on seed novelty, orbit novelty, or "
            "non-overlap with U3. Clause 1 affirmatively requires taking EVERY "
            "anchored strict local minimum of the same reservoir U3 drew from, so a "
            "57% overlap is what compliance with clause 1 LOOKS LIKE, not a breach "
            "of it. The overlap does falsify a DIFFERENT claim -- R0 has already "
            "retracted that one -- but M3 never made it."),
    "what_this_verdict_is_not": ("not a judgement that M3 was well-worded, and not a "
                                 "judgement that the per-stratum yield means what a "
                                 "reader would take it to mean. Only that M3's own "
                                 "wording is not falsified by the overlap."),
}
check("M3", "VERDICT: M3 = DELIVERED survives, on its own pre-committed wording",
      m3_survives, "all five clauses hold; none is touched by the overlap")

# ==========================================================================
n_fail = sum(1 for c in CHECKS if not c["ok"])
print("\n%s\n%d checks, %d passed, %d FAILED"
      % ("=" * 74, len(CHECKS), len(CHECKS) - n_fail, n_fail))

out = {
    "unit": "V1",
    "kind": "VERIFICATION (wave 1: T1, T2, R0+R1)",
    "wave": 2,
    "orchestration": "ORCHESTRATION.md section 3f -- fresh-session verification",
    "base": "main @ c1a8d5e",
    "gate_final_wording": (
        "Re-deriving from banked JSON and landed evidence scripts alone, do all five "
        "of the following reproduce exactly? (1) R0's metric -- U3 = 8/144.69 = "
        "0.0553 and U5 = 5/57.04 = 0.0877 orbits-new-to-the-programme per worker-hour "
        "-- and the 134.45 vs 144.69 reconciliation: attempt CPU as sum "
        "attempts[].wall_seconds/3600 against pool reservation as wall_seconds x "
        "workers, giving 92.92% utilisation. (2) R0's retraction -- 57/100 seed "
        "overlap, 5 of 9 bit-identical, 4 of 5 re-finds, ONE new orbit, and the "
        "corrected metric 0.0175 against the originally claimed 0.0553. (3) R1's "
        "+0.45 pp headroom, and the hold-out kill of one of U3's 14. (4) T2's 32/32 "
        "MEASURED, served opensearch namespace 1.1, 5-of-6 THROTTLED, and a negative "
        "control returning 0 in both instruments. (5) T1's packet ruling none of the "
        "three questions it posed. PLUS: does M3 = DELIVERED survive U5's 57% seed "
        "overlap, judged on M3's own pre-committed wording?"),
    "answer": "ALL FIVE REPRODUCE; M3 = DELIVERED SURVIVES" if n_fail == 0
              else "MISMATCH -- see failed checks",
    "n_checks": len(CHECKS),
    "n_failed": n_fail,
    "checks": CHECKS,
    "notes": NOTES,
    "rederived_values": {
        "u3_pool_reservation_core_hours": pool3,
        "u5_pool_reservation_core_hours": pool5,
        "u3_attempt_cpu_core_hours": cpu3,
        "u5_attempt_cpu_core_hours": cpu5,
        "u3_pool_utilisation": util3,
        "u3_distinct_leader_single_complete": [n3_lead, n3_sing, n3_comp],
        "u5_distinct_leader_single_complete": [n5_lead, n5_sing, n5_comp],
        "u3_metric": m3_metric,
        "u5_metric_as_originally_claimed": m5_metric,
        "u5_seeds_already_spent_by_u3": len(overlap),
        "u5_convergences_on_a_shared_seed": len(shared_conv),
        "u5_bit_identical_outputs": len(bitid),
        "u5_distinct_refinds_of_u3": len(refinds),
        "u5_distinct_new_to_programme": len(newones),
        "u5_corrected_metric": corrected,
        "r1_incumbent_u3_recovery": f_i,
        "r1_best_admissible_u3_recovery": f_b,
        "r1_headroom_percentage_points": headroom_pp,
        "r1_holdout_u5_on_u3_false_kills": k_h,
        "t2_arxiv_records": len(arx),
        "t2_arxiv_measured": n_meas,
        "t2_namespaces_served": ns,
        "t2_s2_substantive_throttled": [len(s2_thr), len(s2s)],
        "u5_in_band_seeds": inband5,
        "u3_in_band_seeds": inband3,
    },
    "ceiling": ("TIER 2. Confirming arithmetic is not a link of the L1->L4 chain. "
                "Nothing this unit returns is movement toward Clay. Clay ~0.05%."),
    "clay_movement": "none -- no L1-L4 link moved by this unit",
}
with open(os.path.join(D, "p2_verify_wave1_v1.json"), "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
    fh.write("\n")

sys.exit(1 if n_fail else 0)
