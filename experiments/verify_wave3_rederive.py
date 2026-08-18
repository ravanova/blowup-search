"""V-W3 -- executable re-derivation of the wave-3 verifier gate (lesson 68).

A check is executable or it decays. Everything this unit claims in
`experiments/journal/verify_wave3.md` and `writeup/data/p2_verify_wave3_v1.json` is
recomputed here from artefacts and code, never from prose.

RUN (from the repo root, no venv needed for the offline core):

    python3 experiments/verify_wave3_rederive.py

Exit code 0 iff every offline assertion holds. Non-zero if any re-derivation stops
agreeing with what this unit banked -- which is the point: if a later edit moves one of
these numbers, this script goes red rather than the finding quietly rotting.

OPTIONAL INDEPENDENT LEGS (network + scipy). These are additive; their absence is
reported as UNREACHABLE and never as a pass and never as a failure:

    python3 experiments/verify_wave3_rederive.py --net          # re-fetch + SHA-256 the three sources
    python3 experiments/verify_wave3_rederive.py --saveddata DIR # re-decode the authors' .mat (needs scipy)

DIR is a directory holding {data,extra}orbit{1,2}.mat, i.e. `saveddata/` out of
https://www.math.vu.nl/~janbouwe/code/navierstokes/navierstokes-code.zip

THIS SCRIPT REPORTS. IT DOES NOT REPAIR. In particular it does NOT register fig107.
"""

import argparse
import ast
import hashlib
import json
import math
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "writeup", "data")

FAILURES = []
NOTES = []


def check(name, got, want, tol=None):
    if tol is None:
        ok = got == want
    else:
        ok = abs(got - want) <= tol
    print("  %-58s %-28r %s" % (name, got, "OK" if ok else "MISMATCH (want %r)" % (want,)))
    if not ok:
        FAILURES.append((name, got, want))
    return ok


def load(fn):
    with open(os.path.join(DATA, fn)) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# ITEM 1 -- unit E's headline, from writeup/data/p2_prog_r4_e_v1.json ONLY
# ---------------------------------------------------------------------------

def item_1():
    print("\n=== ITEM 1: unit E's headline, re-derived from p2_prog_r4_e_v1.json ===")
    e = load("p2_prog_r4_e_v1.json")
    d3 = e["diagnostic_3"]
    att = d3["attempts"]

    # not the summary fields -- recount the per-attempt rows themselves
    n_attempts = len(att)
    n_conv = sum(1 for a in att if a["reason"] == "converged")
    n_success = sum(1 for a in att if a["success"])
    n_rec_own = sum(1 for a in att if a["recovered_named_orbit"])
    n_rec_any = sum(1 for a in att if a["recovered_any_named_orbit"])
    n_matched = sum(1 for a in att if a["matched_row"] is not None)

    check("recount: n_attempts", n_attempts, 16)
    check("recount: reason == 'converged'", n_conv, 2)
    check("recount: success flag", n_success, 2)
    check("recount: recovered_named_orbit", n_rec_own, 0)
    check("recount: recovered_any_named_orbit", n_rec_any, 0)
    check("recount: matched_row not None", n_matched, 0)

    # and the summary block must agree with the recount
    check("summary n_attempts agrees", d3["n_attempts"], n_attempts)
    check("summary n_converged agrees", d3["n_converged"], n_conv)
    check("summary n_recovered_any_named_row agrees", d3["n_recovered_any_named_row"], n_rec_any)
    check("summary n_recovered_its_own_row agrees", d3["n_recovered_its_own_row"], n_rec_own)

    # the positive control that passes at ||R|| ~ 1.5e-10 is R, not P
    ctl = d3["controls"]
    check("control R final_residual (2 s.f.)", float("%.2g" % ctl["R"]["final_residual"]), 1.5e-10)
    check("control R through E's OWN predicate", ctl["R"]["harness_predicate_says_recovered"], True)
    check("control R recovered", ctl["R"]["recovered"], True)
    NOTES.append(
        "the OTHER positive control P lands at ||R|| = %.3g, not 1.5e-10; the 1.5e-10 "
        "figure is control R's alone" % ctl["P"]["final_residual"])
    check("control P final_residual (2 s.f.)", float("%.2g" % ctl["P"]["final_residual"]), 7.8e-09)
    check("controls fired as planted", ctl["fired_as_planted"], True)
    check("control failures", ctl["failures"], [])

    # diagnostic (i)
    d1 = e["diagnostic_1"]
    check("diagnostic (1) verdict", d1["verdict"], "PULL_TO_LOW_S")
    check("diagnostic (1) n (converged subset)", d1["n"], 23)
    NOTES.append(
        "diagnostic (1)'s headline PULL_TO_LOW_S is measured on the n=23 CONVERGED subset; "
        "the same statistic over all %d banked attempts is '%s'"
        % (d1["secondary_all_200_attempts"]["n"], d1["secondary_all_200_attempts"]["verdict"]))
    check("diagnostic (1) secondary over all 200 is NO_PULL",
          d1["secondary_all_200_attempts"]["verdict"], "NO_PULL")

    # diagnostic (ii)
    d2 = e["diagnostic_2"]
    check("diagnostic (2) verdict", d2["verdict"], "MIXED")
    check("diagnostic (2) permutation_p rounded to 4 d.p.", round(d2["permutation_p"], 4), 0.9317)
    return e


# ---------------------------------------------------------------------------
# ITEM 2 -- E's cost, both sides, like for like
# ---------------------------------------------------------------------------

def item_2(e):
    print("\n=== ITEM 2: E's cost, re-derived; is 0.0713 like-for-like? ===")
    d3 = e["diagnostic_3"]
    res = d3["resourcing"]
    att = d3["attempts"]

    n = len(att)
    banked_core_h = res["core_hours"]
    ctl_h = res["control_wall_seconds"] / 3600.0
    sum_att_s = sum(a["wall_seconds"] for a in att)
    sum_att_core_h = sum_att_s / 3600.0
    epochs = sum(a["n_iters"] for a in att)

    check("banked core_hours == wall_s * workers / 3600",
          round(res["wall_seconds"] * res["workers"] / 3600.0, 9), round(banked_core_h, 9))
    check("banked core_hours (3 d.p.)", round(banked_core_h, 3), 5.687)
    check("controls in hours (3 d.p.)", round(ctl_h, 3), 0.806)
    check("sum of per-attempt wall, core-hours (3 d.p.)", round(sum_att_core_h, 3), 9.088)
    check("total_epochs field == recount of n_iters", res["total_epochs"], epochs)
    check("epochs recount", epochs, 343)

    # the record's own stated arithmetic
    record_arith = (banked_core_h + ctl_h) / n
    print("\n  THE RECORD'S OWN PARENTHETICAL, evaluated:")
    print("    (5.687 core-hours + 0.806 h controls) / 16 attempts = %.4f h/attempt" % record_arith)
    print("    the record calls this 0.57.  It is %.4f." % record_arith)
    check("(banked + controls)/16 does NOT equal 0.57", round(record_arith, 2) == 0.57, False)
    check("(banked + controls)/16 (3 d.p.)", round(record_arith, 3), 0.406)

    print("\n  WHERE 0.57 ACTUALLY COMES FROM:")
    print("    sum of per-attempt wall / 16 = %.4f core-hours per attempt" % (sum_att_core_h / n))
    check("sum-of-per-attempt-wall / 16 (2 d.p.)", round(sum_att_core_h / n, 2), 0.57)

    # the other side: U5's commissioning figure, and its UNIT
    print("\n  THE COMMISSIONING FIGURE 0.0713 AND ITS UNIT:")
    u5j = os.path.join(ROOT, "experiments", "journal", "prog_r4_u5.md")
    src = open(u5j, encoding="utf-8").read()
    m = re.search(r"0\.0713 h ([a-z ]*?) per attempt at (\d+) workers", src)
    if m is None:
        m = re.search(r"0\.0713 h (wall) per attempt at (\d+) workers", src)
    print("    prog_r4_u5.md says: %r" % (m.group(0) if m else None))
    check("0.0713 is a WALL figure", bool(m) and "wall" in m.group(1), True)
    workers_u5 = int(m.group(2)) if m else None
    check("...measured at 8 workers", workers_u5, 8)

    u5_core_h_per_attempt = 0.0713 * workers_u5
    print("\n  LIKE FOR LIKE, both sides in CORE-HOURS PER ATTEMPT:")
    print("    U5 commissioning: 0.0713 wall-h/attempt x %d workers = %.4f core-h/attempt"
          % (workers_u5, u5_core_h_per_attempt))
    print("    E measured:       %.4f core-h/attempt" % (sum_att_core_h / n))
    print("    ratio E/U5      = %.4f  (an '8x overrun' would be 8.0)" % ((sum_att_core_h / n) / u5_core_h_per_attempt))
    check("like-for-like ratio is ~1, not ~8 (2 d.p.)",
          round((sum_att_core_h / n) / u5_core_h_per_attempt, 2), 1.00)
    check("the bogus ratio equals the worker count",
          round((sum_att_core_h / n) / 0.0713, 1), 8.0)

    # and the STRUCTURAL explanation offered for the overrun
    print("\n  THE 'STRUCTURAL' EXPLANATION (good seeds do not fail fast), tested:")
    u5_ledger = os.path.join(ROOT, "experiments", "programme_r4", "u5_m3_ledger.json")
    u5 = json.load(open(u5_ledger))
    u5_epochs = sum(len(a["ledger"]) for a in u5["attempts"])
    print("    U5 epochs/attempt = %d/%d = %.2f" % (u5_epochs, len(u5["attempts"]), u5_epochs / len(u5["attempts"])))
    print("    E  epochs/attempt = %d/%d = %.2f" % (epochs, n, epochs / n))
    print("    E  seconds/epoch  = %.1f  (U5's cost model prices an epoch at 95 s)" % (sum_att_s / epochs))
    check("E epochs/attempt is NOT >> U5's (ratio under 1.1)",
          (epochs / n) / (u5_epochs / len(u5["attempts"])) < 1.1, True)
    NOTES.append(
        "E ran %.2f epochs/attempt against U5's %.2f -- E used FEWER, so 'a plausible seed "
        "runs longer before the stall rule fires' is not what the ledgers show"
        % (epochs / n, u5_epochs / len(u5["attempts"])))
    NOTES.append(
        "prog_r4_u5.md's prose says 2,104 epochs over 100 attempts; its own banked ledger "
        "u5_m3_ledger.json holds %d (and E's diagnostic_2 independently reports n_epochs=%d)"
        % (u5_epochs, e["diagnostic_2"]["n_epochs"]))
    check("U5 ledger epoch count", u5_epochs, 2195)
    check("E's diagnostic_2 n_epochs agrees with U5's ledger", e["diagnostic_2"]["n_epochs"], u5_epochs)


# ---------------------------------------------------------------------------
# ITEM 3 -- verify the verifier (V-W2), four re-measurements, JSON-level
# ---------------------------------------------------------------------------

def item_3_offline():
    print("\n=== ITEM 3: V-W2's four re-measurements, re-derived from the PRIMARY artefacts ===")
    vw2 = load("p2_verify_wave2_v1.json")
    t4 = load("p2_route_t4_v1.json")
    t5 = load("p2_route_t5_v1.json")
    t6 = load("p2_route_t6_v1.json")

    print("\n  (3a-1) T4's 2D lift")
    for lab, om3, nrec, shape in (("p1", 1.6351, [17, 17, 0, 11], [35, 35, 1, 23, 3]),
                                  ("p2", 1.5274, [21, 21, 0, 16], [43, 43, 1, 33, 3])):
        dim = t4["rows"][lab]["dimensionality"]
        check("T4 %s Table 1 Nx3" % lab, t4["rows"][lab]["table1_row"]["Nx3"], 0)
        check("T4 %s solshape Nrec" % lab, t4["rows"][lab]["solshape_Nrec"], nrec)
        check("T4 %s Nrec[2] (x3)" % lab, t4["rows"][lab]["solshape_Nrec"][2], 0)
        check("T4 %s x3_mode_extent" % lab, dim["x3_mode_extent"], 1)
        check("T4 %s omega_shape" % lab, dim["omega_shape"], shape)
        check("T4 %s u_shape" % lab, dim["u_shape"], shape)
        for f in ("max_abs_u3", "max_abs_omega1", "max_abs_omega2"):
            check("T4 %s %s is exactly 0.0" % (lab, f), repr(dim[f]), "0.0")
        check("T4 %s max_abs_omega3 (4 d.p.)" % lab, round(dim["max_abs_omega3"], 4), om3)
        check("T4 %s setup field" % lab, dim["setup_field_in_authors_output"], "2D")
        # V-W2's own banked column must equal the primary artefact
        check("V-W2 %s column == T4 primary" % lab,
              {k: vw2["item_1_T4_2D_lift"][lab]["banked"][k] for k in
               ("x3_mode_extent", "omega_shape", "u_shape", "p_shape",
                "max_abs_u3", "max_abs_omega1", "max_abs_omega2", "max_abs_omega3")},
              {k: dim[k] for k in
               ("x3_mode_extent", "omega_shape", "u_shape", "p_shape",
                "max_abs_u3", "max_abs_omega1", "max_abs_omega2", "max_abs_omega3")})
    check("T4 control C_3D fired", t4["controls"]["C_3D"]["fired"], True)

    print("\n  (3a-2) T4's first conjunct and its negative control")
    for lab in ("p1", "p2"):
        row = t4["rows"][lab]
        b = row["published_bounds"]
        a = 1.0 - (b["Z0"] + b["Z1"])
        # recompute the paper's (4.32)/(4.33)/(4.34) from the four published constants
        check("T4 %s Z0+Z1 recomputed" % lab, b["Z0"] + b["Z1"], row["paper_criterion_4_32"]["Z0_plus_Z1"])
        check("T4 %s 2*Y0*Z2 recomputed" % lab, 2.0 * b["Y0"] * b["Z2"],
              row["paper_criterion_4_32"]["two_Y0_Z2"])
        check("T4 %s (1-Z0-Z1)^2 recomputed" % lab, a * a,
              row["paper_criterion_4_32"]["one_minus_Z0_Z1_squared"])
        check("T4 %s criterion (4.32) met" % lab, row["paper_criterion_4_32"]["criterion_met"], True)
        disc = a * a - 2.0 * b["Y0"] * b["Z2"]
        check("T4 %s discriminant recomputed" % lab, disc, row["paper_criterion_4_32"]["discriminant"])
        rmin = (a - math.sqrt(disc)) / b["Z2"]
        rmax = a / b["Z2"]
        check("T4 %s r_min recomputed (rel 1e-15)" % lab,
              abs(rmin - row["r_min"]["reproduced"]) / row["r_min"]["reproduced"] < 1e-15, True)
        check("T4 %s r_max recomputed (rel 1e-15)" % lab,
              abs(rmax - row["r_max"]["reproduced"]) / row["r_max"]["reproduced"] < 1e-15, True)
        check("T4 %s r_sol_Omega exact vs printed" % lab, row["r_sol_Omega"]["rel_dev_vs_printed"], 0.0)

    devs = {(lab, k): t4["rows"][lab][k]["rel_dev"] for lab in ("p1", "p2") for k in ("r_min", "r_max")}
    smallest_nonzero = min(v for v in devs.values() if v > 0)
    print("    all four r rel_devs: %s" % {("%s.%s" % k): "%.3g" % v for k, v in devs.items()})
    check("smallest NON-ZERO rel_dev over the four r cells (2 s.f.)",
          float("%.2g" % smallest_nonzero), 5.6e-15)
    check("V-W2's claimed 5.6e-15 == that cell",
          vw2["item_2_T4_first_conjunct_and_negative_control"]
             ["smallest_nonzero_rel_dev_over_the_four_r_cells"]["mine"], smallest_nonzero)
    NOTES.append(
        "the gate's '5.6e-15' is the SMALLEST NON-ZERO of four cells; the four are "
        "%s -- one of them is exactly 0.0, so 'down to 5.6e-15' understates two cells "
        "and overstates one" % {("%s.%s" % k): "%.3g" % v for k, v in devs.items()})

    nu = t4["rows"]["p2"]["norm_u_X"]
    delta = abs(nu["computed_from_published_data"] - nu["implied_by_printed_radii"]) / nu["implied_by_printed_radii"]
    check("T4 norm check delta recomputed (2 s.f.)", float("%.2g" % delta), 5.3e-06)
    check("T4 norm check delta == banked rel_dev", delta, nu["rel_dev"])
    ev = open(os.path.join(ROOT, "experiments", "p2_route_t4_v1_evidence.py"), encoding="utf-8").read()
    m = re.search(r"V4_REPRODUCED\s*=\s*([0-9eE.\-+]+)", ev)
    check("V4_REPRODUCED threshold read from the evidence script", float(m.group(1)), 1e-3)
    check("delta under threshold", delta < float(m.group(1)), True)

    cp = t4["controls"]["C_plus"]["term_counts"]
    check("C+ 'approximate inverse'", cp["approximate inverse"], 7)
    check("C+ 'newton-kantorovich'", cp["newton-kantorovich"], 4)
    check("C+ 'interval arithmetic'", cp["interval arithmetic"], 5)
    check("C+ 'intlab'", cp["intlab"], 2)
    cm = t4["controls"]["C_minus"]["term_counts"]
    check("C- all six closure terms are 0", sorted(set(cm.values())), [0])
    check("C- has exactly six closure terms", len(cm), 6)
    check("C- zgliczynski mentions", len(t4["controls"]["C_minus"]["zgliczynski_mentions"]), 1)
    check("C- the single zgliczynski line is bibliography item [48]",
          t4["controls"]["C_minus"]["zgliczynski_mentions"][0].lstrip().startswith("[48]"), True)
    check("C- zgliczynski only in bibliography",
          t4["controls"]["C_minus"]["zgliczynski_only_in_bibliography"], True)

    print("\n  (3a-3) T6's table")
    import collections
    sf = t6["summary_fetch"]
    check("T6 n fulltexts banked", len(t6["fulltexts"]), 7)
    check("T6 n_fulltext_MEASURED", sf["n_fulltext_MEASURED"], 7)
    check("T6 n_fulltext_UNREACHABLE", sf["n_fulltext_UNREACHABLE"], 0)
    check("T6 n_fulltext_THROTTLED", sf["n_fulltext_THROTTLED"], 0)
    # recount from the per-paper rows, not from the banked summary
    rec = collections.Counter(v["verdict"] for v in t6["verdicts"])
    print("    T6 verdict recount from the 7 rows: %r" % dict(rec))
    check("T6 UNDERCUT", rec.get("UNDERCUT"), 2)
    check("T6 strengthen", rec.get("strengthen"), 4)
    check("T6 confirm", rec.get("confirm"), 1)
    check("T6 UNREACHABLE", rec.get("UNREACHABLE", 0), 0)
    check("T6 verdicts sum to 7", sum(rec.values()), 7)
    check("T6 banked verdict_counts agree with the recount",
          {k: v for k, v in t6["verdict_counts"].items() if v},
          {k: v for k, v in rec.items()})
    check("T6 the two UNDERCUTs are 1902.00384 and 2409.09234",
          sorted(v["id"] for v in t6["verdicts"] if v["verdict"] == "UNDERCUT"),
          ["1902.00384", "2409.09234"])

    print("\n  (3a-4) T5's sweep")
    corpus = t5["corpus"]
    check("T5 files_enumerated", corpus["files_enumerated"], 1428)
    check("T5 lines", corpus["lines"], 417476)
    findings = t5["findings"]
    check("T5 n findings", len(findings), 7)
    import collections
    cls = collections.Counter(f["classification"] for f in findings)
    print("    classification recount: %r" % dict(cls))
    check("T5 APPARATUS", cls.get("APPARATUS"), 5)
    check("T5 REALIZATION", cls.get("REALIZATION"), 2)
    reop = [f["id"] for f in findings if f["reopenable"]]
    check("T5 re-openable", reop, ["F1", "F2"])

    # the corpus figure is a claim about a git tree, so re-enumerate the tree
    landing = subprocess.run(
        ["git", "-C", ROOT, "log", "-1", "--format=%H", "--", "writeup/data/p2_route_t5_v1.json"],
        capture_output=True, text=True).stdout.strip()
    print("    landing commit of p2_route_t5_v1.json: %s" % landing[:12])
    excl = set(corpus.get("excluded_by_name", []))
    files = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r", "--name-only", landing],
                           capture_output=True, text=True).stdout.split("\n")
    cand = [f for f in files if f.endswith(".md") or f.endswith(".py")]
    cand = [f for f in cand if os.path.basename(f) not in excl and f not in excl]
    nlines = 0
    for f in cand:
        blob = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (landing, f)],
                              capture_output=True).stdout
        nlines += blob.count(b"\n")
    print("    my re-enumeration at the landing commit: %d files, %d lines" % (len(cand), nlines))
    check("T5 corpus files re-enumerated", len(cand), 1428)
    check("T5 corpus lines re-enumerated", nlines, 417476)
    check("V-W2's corpus figure == mine", vw2["item_4_T5_sweep"]["my_corpus_at_landing_commit"]["files"], len(cand))

    print("\n  (3b) the SHA-256 method: is it IN the artefacts, or prose only?")
    ref = vw2.get("independent_artefacts_refetched")
    check("V-W2 JSON carries an independent_artefacts_refetched block", ref is not None, True)
    hashes = {k: v for k, v in ref.items() if isinstance(v, dict)}
    for k, v in hashes.items():
        check("  %s: my_sha256 present and 64 hex" % k,
              bool(re.fullmatch(r"[0-9a-f]{64}", v.get("my_sha256", ""))), True)
        check("  %s: banked_sha256 recorded and matched" % k,
              v.get("my_sha256") == v.get("banked_sha256") and v.get("match") is True, True)
    check("three sources hashed", len(hashes), 3)
    # and the hash is also carried by the PRIMARY artefact it is a hash of
    src = json.dumps(t4)
    for v in hashes.values():
        if "1902" in v["url"] or "navierstokes-code" in v["url"]:
            check("  hash also banked in T4's own primary artefact",
                  v["my_sha256"] in src, True)
    return hashes


def item_3_net(hashes):
    print("\n  (3b, INDEPENDENT LEG) re-fetching the three sources and hashing them myself")
    import urllib.request
    for k, v in hashes.items():
        try:
            with urllib.request.urlopen(v["url"], timeout=120) as r:
                body = r.read()
            h = hashlib.sha256(body).hexdigest()
            print("    %-28s %d bytes  %s" % (k, len(body), h))
            check("  re-fetched %s sha256 == banked" % k, h, v["banked_sha256"])
        except Exception as exc:  # network is not a pass and not a fail
            print("    %-28s UNREACHABLE (%s)" % (k, exc))
            NOTES.append("independent re-fetch of %s UNREACHABLE: %s" % (k, exc))


def item_3_mat(saved):
    print("\n  (3a-1/2, INDEPENDENT LEG) re-decoding the authors' .mat myself")
    try:
        import numpy as np
        import scipy.io as sio
    except ImportError as exc:
        print("    UNREACHABLE: %s" % exc)
        NOTES.append("independent .mat re-decode UNREACHABLE: %s" % exc)
        return
    t4 = load("p2_route_t4_v1.json")

    def sc(x):
        return float(np.asarray(x).ravel()[0])

    for tag, lab in (("1", "p1"), ("2", "p2")):
        extra = sio.loadmat(os.path.join(saved, "extraorbit%s.mat" % tag))
        data = sio.loadmat(os.path.join(saved, "dataorbit%s.mat" % tag))
        om, u = data["omega"], data["u"]
        b = extra["bounds"][0, 0]
        Y0, Z0, Z1, Z2 = sc(b["Y"]), sc(b["Z0"]), sc(b["Z1"]), sc(b["Z2"])
        a = 1.0 - (Z0 + Z1)
        disc = a * a - 2.0 * Y0 * Z2
        rmin, rmax = (a - math.sqrt(disc)) / Z2, a / Z2
        dim = t4["rows"][lab]["dimensionality"]
        check("mat %s omega_shape" % lab, list(om.shape), dim["omega_shape"])
        check("mat %s x3 extent" % lab, int(om.shape[2]), 1)
        check("mat %s max|u3| exactly 0.0" % lab, repr(float(np.abs(u[..., 2]).max())), "0.0")
        check("mat %s max|omega1| exactly 0.0" % lab, repr(float(np.abs(om[..., 0]).max())), "0.0")
        check("mat %s max|omega2| exactly 0.0" % lab, repr(float(np.abs(om[..., 1]).max())), "0.0")
        check("mat %s max|omega3| bitwise" % lab, float(np.abs(om[..., 2]).max()), dim["max_abs_omega3"])
        check("mat %s setup" % lab, str(np.asarray(extra["setup"]).ravel()[0]), "2D")
        check("mat %s Nrec" % lab,
              np.asarray(extra["solshape"][0, 0]["Nrec"]).ravel().astype(int).tolist(),
              t4["rows"][lab]["solshape_Nrec"])
        check("mat %s r_min bitwise" % lab, rmin, t4["rows"][lab]["r_min"]["reproduced"])
        check("mat %s r_max bitwise" % lab, rmax, t4["rows"][lab]["r_max"]["reproduced"])
        check("mat %s r_min rel_dev vs published" % lab,
              abs(rmin - sc(extra["rmin"])) / sc(extra["rmin"]), t4["rows"][lab]["r_min"]["rel_dev"])
        check("mat %s r_max rel_dev vs published" % lab,
              abs(rmax - sc(extra["rmax"])) / sc(extra["rmax"]), t4["rows"][lab]["r_max"]["rel_dev"])
        check("mat %s ||u||_X bitwise" % lab, float(np.abs(u).sum()),
              t4["rows"][lab]["norm_u_X"]["computed_from_published_data"])


# ---------------------------------------------------------------------------
# ITEM 4 -- fig107 and P2_EVIDENCE, parsed, not eyeballed
# ---------------------------------------------------------------------------

def item_4():
    print("\n=== ITEM 4: fig107 vs P2_EVIDENCE in writeup/build_figures.py, PARSED ===")
    import tokenize
    path = os.path.join(ROOT, "writeup", "build_figures.py")
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    P2 = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "P2_EVIDENCE":
                    P2 = ast.literal_eval(node.value)
    check("P2_EVIDENCE found as a module-level literal", P2 is not None, True)
    node = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "P2_EVIDENCE" for t in n.targets)][0]
    flat = [str(x) for e in P2 for x in (e if isinstance(e, (list, tuple)) else [e])]
    # the figure a P2_EVIDENCE entry draws is named in the trailing `# figNNN --` comment,
    # so the id set is read off the literal's own source lines, not off the path strings
    lines = src.split("\n")[node.lineno - 1:node.end_lineno]
    ids = sorted({int(m.group(1)) for ln in lines for m in [re.search(r"#\s*fig(\d+)\s", ln)] if m})
    print("  P2_EVIDENCE has %d entries; %d distinct figure ids named on its lines" % (len(P2), len(ids)))
    print("  registered ids: %s" % ids)
    check("fig107 in any P2_EVIDENCE PATH string", any("fig107" in s for s in flat), False)
    for i in (99, 103, 104, 105, 106, 108, 109, 110):
        check("  fig%d IS registered" % i, i in ids, True)
    check("  fig107 is NOT in the registered id set", 107 in ids, False)
    check("  every entry has exactly one figure id", len(ids), len(P2))

    # where does the token 'fig107' occur in the file at all?
    with open(path, encoding="utf-8") as fh:
        toks = list(tokenize.generate_tokens(fh.readline))
    in_str = [t for t in toks if t.type == tokenize.STRING and "fig107" in t.string]
    in_com = [t for t in toks if t.type == tokenize.COMMENT and "fig107" in t.string]
    print("  'fig107' in STRING tokens: %d   in COMMENT tokens: %d (lines %s)"
          % (len(in_str), len(in_com), [t.start[0] for t in in_com]))
    check("fig107 appears in NO string literal", len(in_str), 0)
    check("fig107 appears only in comments", len(in_com), 2)

    # the drawing script and png exist on disk, so the gap is registration, not the figure
    figs = os.path.join(ROOT, "writeup", "figures")
    check("fig107 drawing script exists on disk",
          os.path.exists(os.path.join(figs, "fig107_prog_r4_m3_shift_strata.py")), True)
    check("fig107 png is banked",
          os.path.exists(os.path.join(figs, "fig107_prog_r4_m3_shift_strata.png")), True)
    NOTES.append(
        "fig107's script and png both exist under writeup/figures/; the defect is the "
        "missing P2_EVIDENCE entry alone -- one line. NOT REPAIRED BY THIS UNIT.")
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--net", action="store_true", help="re-fetch the three sources and hash them")
    ap.add_argument("--saveddata", default=None, help="dir with {data,extra}orbit{1,2}.mat")
    args = ap.parse_args()

    e = item_1()
    item_2(e)
    hashes = item_3_offline()
    if args.net:
        item_3_net(hashes)
    else:
        print("\n  (3b independent re-fetch NOT run; pass --net. Recorded UNREACHABLE, not passed.)")
    if args.saveddata:
        item_3_mat(args.saveddata)
    else:
        print("  (.mat re-decode NOT run; pass --saveddata DIR. Recorded UNREACHABLE, not passed.)")
    item_4()

    print("\n" + "=" * 78)
    if NOTES:
        print("NOTES / NUANCES BANKED (not failures):")
        for n in NOTES:
            print("  - %s" % n)
    print("=" * 78)
    if FAILURES:
        print("RE-DERIVATION DISAGREEMENTS: %d" % len(FAILURES))
        for f in FAILURES:
            print("  %s: got %r, expected %r" % f)
        return 1
    print("ALL OFFLINE RE-DERIVATIONS AGREE.")
    print("Verification is NOT movement toward Clay. No link moved. Clay odds ~0.05%, unmoved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
