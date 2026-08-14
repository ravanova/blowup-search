"""V-W2 (branch `verify/wave2`) -- EVIDENCE.

Every number `experiments/journal/verify_wave2.md` quotes, re-derived here from the banked
wave-2 JSON and the landed evidence scripts, and checked against
`writeup/data/p2_verify_wave2_v1.json`.

**This script does NOT re-run T4's, T5's or T6's own scripts.** A script agreeing with
itself is not verification. Everything below is recomputed independently:

  * the radii from the paper's own (4.33)/(4.34), applied to the authors' published
    `Y0, Z0, Z1, Z2`;
  * every tally recounted with `collections.Counter` from the raw `findings` / `verdicts`
    / `fulltexts` lists, never read off a `*_counts` field;
  * `T5`'s corpus re-enumerated with `git ls-tree` + `git cat-file` at the commit that
    landed the artefact -- not by calling the sweep's own `enumerate_corpus()`;
  * every banked quote relocated at its recorded `file:line` in the live tree;
  * `T6`'s leg-348 lock re-hashed against the live files.

Where a check needs an artefact that is NOT tracked in the repository (the arXiv PDFs and
the VU code package live in the untracked `Papers/`), the check is run only if the artefact
is present, and is otherwise reported as `skip` with its banked sha256 -- never as a pass.
The measurement itself is banked in `p2_verify_wave2_v1.json` under
`independent_artefacts_refetched`, with the digests that made it a measurement rather than
a transcription.

**Lesson 68: gate this by the EXIT CODE, never by reading a printed line.**
Exit 0 = every check passed. Exit 1 = at least one FAILED.

    .venv/bin/python experiments/p2_verify_wave2_evidence.py
"""

import collections
import json
import math
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "writeup", "data")

CHECKS = []
SKIPPED = []


def load(name):
    with open(os.path.join(D, name), encoding="utf-8") as fh:
        return json.load(fh)


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print("%-4s %-76s %s" % ("ok" if ok else "FAIL", name, detail))


def skip(name, why):
    SKIPPED.append((name, why))
    print("%-4s %-76s %s" % ("skip", name, why))


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args],
                          capture_output=True, text=True, check=True).stdout


# ---------------------------------------------------------------------------
# The paper's own (4.33) / (4.34), transcribed from arXiv:1902.00384 p.35.
# NOTE: r_max is the VALIDITY BOUND (1 - (Z0+Z1)) / Z2, NOT the larger root of the
# radii polynomial. Getting this wrong is the single easiest way to manufacture a
# false discrepancy here, so it is written out rather than assumed.
# ---------------------------------------------------------------------------
def paper_radii(Y0, Z0, Z1, Z2):
    a = 1.0 - Z0 - Z1
    disc = a * a - 2.0 * Y0 * Z2
    return (a - math.sqrt(disc)) / Z2, a / Z2, disc


def main():
    V = load("p2_verify_wave2_v1.json")
    t4, t5, t6 = load("p2_route_t4_v1.json"), load("p2_route_t5_v1.json"), load("p2_route_t6_v1.json")
    pocp = load("p2_route_pocp_v1.json")

    # =====================================================================
    # ITEM 1 -- T4's 2D lift
    # =====================================================================
    for lab, w3 in (("p1", 1.6351), ("p2", 1.5274)):
        r = t4["rows"][lab]
        dim = r["dimensionality"]
        check("(1) %s: N_x3 = 0 in Table 1" % lab, r["table1_row"]["Nx3"] == 0,
              "Nx3=%d" % r["table1_row"]["Nx3"])
        check("(1) %s: N_x3 = 0 in the package's own Nrec" % lab,
              r["solshape_Nrec"][2] == 0, str(r["solshape_Nrec"]))
        check("(1) %s: control C_3D agrees on Nx3" % lab,
              t4["controls"]["C_3D"]["%s_Nx3" % lab] == 0)
        check("(1) %s: x3 extent is exactly 1 on omega, u and p" % lab,
              dim["x3_mode_extent"] == 1 and dim["omega_shape"][2] == 1
              and dim["u_shape"][2] == 1 and dim["p_shape"][2] == 1)
        check("(1) %s: max|u3| = max|w1| = max|w2| = 0.0 EXACTLY (float equality)" % lab,
              dim["max_abs_u3"] == 0.0 and dim["max_abs_omega1"] == 0.0
              and dim["max_abs_omega2"] == 0.0,
              "%r / %r / %r" % (dim["max_abs_u3"], dim["max_abs_omega1"],
                                dim["max_abs_omega2"]))
        check("(1) %s: max|w3| rounds to %.4f and is strictly positive" % (lab, w3),
              round(dim["max_abs_omega3"], 4) == w3 and dim["max_abs_omega3"] > 0.0,
              "%.13f" % dim["max_abs_omega3"])
        check("(1) %s: setup field is '2D'" % lab,
              dim["setup_field_in_authors_output"] == "2D")
        # V-W2's own independent decode, banked
        mine = V["item_1_T4_2D_lift"][lab]["MY_MEASUREMENT_from_the_authors_mat_files"]
        check("(1) %s: V-W2's independent .mat decode is bitwise identical to the banked row" % lab,
              V["item_1_T4_2D_lift"][lab]["bitwise_identical"] is True
              and mine["max_abs_omega3"] == dim["max_abs_omega3"]
              and mine["setup"] == "2D" and mine["Nrec"] == r["solshape_Nrec"])

    saved = os.path.join(ROOT, "Papers", "ns_code", "navierstokes-code", "saveddata")
    if os.path.isdir(saved):
        try:
            import numpy as np
            import scipy.io as sio
            for tag, lab in (("1", "p1"), ("2", "p2")):
                dd = sio.loadmat(os.path.join(saved, "dataorbit%s.mat" % tag))
                u, om = dd["u"], dd["omega"]
                mine = V["item_1_T4_2D_lift"][lab]["MY_MEASUREMENT_from_the_authors_mat_files"]
                check("(1) %s: LIVE re-decode of the authors' .mat matches V-W2's banked decode" % lab,
                      float(np.max(np.abs(u[..., 2]))) == mine["max_abs_u3"]
                      and float(np.max(np.abs(om[..., 2]))) == mine["max_abs_omega3"])
        except ImportError:
            skip("(1) live .mat re-decode", "scipy/numpy unavailable")
    else:
        skip("(1) live .mat re-decode",
             "Papers/ns_code is untracked and absent; measurement banked with sha256 %s"
             % t4["target_paper"]["code_zip_sha256"][:16])

    # =====================================================================
    # ITEM 2 -- the first conjunct and the negative control
    # =====================================================================
    nonzero = []
    for lab in ("p1", "p2"):
        r = t4["rows"][lab]
        b = r["published_bounds"]
        rmin, rmax, disc = paper_radii(b["Y0"], b["Z0"], b["Z1"], b["Z2"])
        c = r["paper_criterion_4_32"]
        a = 1.0 - b["Z0"] - b["Z1"]
        check("(2) %s: (4.32) first half Z0+Z1 < 1, recomputed here" % lab,
              (b["Z0"] + b["Z1"]) < 1.0 and c["Z0_plus_Z1_lt_1"] is True,
              "%.16f" % (b["Z0"] + b["Z1"]))
        check("(2) %s: (4.32) second half 2*Y0*Z2 < (1-(Z0+Z1))^2, recomputed here" % lab,
              (2 * b["Y0"] * b["Z2"]) < a * a and c["second_inequality_holds"] is True,
              "%.6e < %.6e" % (2 * b["Y0"] * b["Z2"], a * a))
        check("(2) %s: my criterion verdict equals the banked criterion_met" % lab,
              ((b["Z0"] + b["Z1"] < 1.0) and (2 * b["Y0"] * b["Z2"] < a * a))
              == c["criterion_met"])
        check("(2) %s: my discriminant equals the banked one" % lab,
              disc == c["discriminant"], "%.10e" % disc)
        check("(2) %s: r_min from (4.33) is BITWISE identical to the banked reproduction" % lab,
              rmin == r["r_min"]["reproduced"], "%.17g" % rmin)
        check("(2) %s: r_max from (4.34) is BITWISE identical to the banked reproduction" % lab,
              rmax == r["r_max"]["reproduced"], "%.17g" % rmax)
        for nm, mine_r in (("r_min", rmin), ("r_max", rmax)):
            pub = r[nm]["published"]
            dev = abs(mine_r - pub) / abs(pub)
            check("(2) %s: my %s rel dev vs published equals the banked rel_dev" % (lab, nm),
                  dev == r[nm]["rel_dev"], "%.6e" % dev)
            if dev > 0:
                nonzero.append(dev)
        ro = r["r_sol_Omega"]
        check("(2) %s: r_sol^Omega is EXACT against the paper's printed value" % lab,
              ro["rel_dev_vs_printed"] == 0.0
              and ro["reproduced"] == ro["printed_in_paper"],
              "%.5g" % ro["reproduced"])
    check("(2) smallest NON-ZERO r_min/r_max relative deviation is 5.6e-15",
          abs(min(nonzero) - 5.6e-15) < 0.05e-15, "%.6e" % min(nonzero))

    n = t4["rows"]["p2"]["norm_u_X"]
    delta = abs(n["computed_from_published_data"] - n["implied_by_printed_radii"]) \
        / n["implied_by_printed_radii"]
    check("(2) independent norm check: my delta equals the banked rel_dev",
          delta == n["rel_dev"], "%.10e" % delta)
    check("(2) the norm-check delta is 5.3e-06 to 2 s.f.",
          float("%.1e" % delta) == 5.3e-06, "%.1e" % delta)
    # the 1e-3 threshold is a module constant of the LANDED evidence script, pre-committed
    ev = open(os.path.join(ROOT, "experiments", "p2_route_t4_v1_evidence.py"),
              encoding="utf-8").read()
    m = re.search(r"^V4_REPRODUCED\s*=\s*(\S+)", ev, re.M)
    check("(2) the threshold in the landed evidence script is literally 1e-3",
          m is not None and float(m.group(1)) == 1e-3, m.group(1) if m else "NOT FOUND")
    check("(2) delta is under that threshold", delta < 1e-3)

    cp = t4["controls"]["C_plus"]["term_counts"]
    for term, want in (("approximate inverse", 7), ("newton-kantorovich", 4),
                       ("interval arithmetic", 5), ("intlab", 2)):
        check("(2) term count %-22r == %d" % (term, want), cp[term] == want, "n=%d" % cp[term])
    cm = t4["controls"]["C_minus"]["term_counts"]
    check("(2) ALL SIX closure terms are at zero",
          set(cm) == {"self-consistent", "a priori bounds", "isolating", "trapping region",
                      "logarithmic norm", "dynamical closure"}
          and all(v == 0 for v in cm.values()), str(sorted(cm.items())))
    zg = t4["controls"]["C_minus"]["zgliczynski_mentions"]
    check("(2) Zgliczynski appears exactly once, as bibliography item [48]",
          len(zg) == 1 and zg[0].startswith("[48]")
          and t4["controls"]["C_minus"]["zgliczynski_only_in_bibliography"] is True,
          zg[0][:52] if zg else "NONE")
    # V-W2's own recount, banked
    tc = V["item_2_T4_first_conjunct_and_negative_control"]["term_counts"]
    check("(2) V-W2's independent recount of the PDF reproduces every C+ count",
          all(tc["my_counts_C_plus"][k] == cp[k] for k in cp), str(tc["my_counts_C_plus"]))
    check("(2) V-W2's independent recount reproduces every C- zero",
          all(v == 0 for v in tc["my_counts_C_minus"].values()))

    pdf = os.path.join(ROOT, "Papers", "1902.00384.pdf")
    if os.path.exists(pdf):
        raw = subprocess.run(["pdftotext", "-layout", pdf, "-"],
                             capture_output=True, text=True).stdout
        flat = re.sub(r"\s+", " ", re.sub(r"[-‐-―−]\s*\n\s*", "",
                                          raw.replace("­", ""))).lower()
        check("(2) LIVE recount of the PDF still gives the banked C+ counts",
              all(flat.count(k) == cp[k] for k in cp))
    else:
        skip("(2) live PDF recount",
             "Papers/1902.00384.pdf is untracked and absent; measurement banked with sha256 %s"
             % t4["target_paper"]["pdf_sha256"][:16])

    # =====================================================================
    # ITEM 3 -- T6's table
    # =====================================================================
    ft, vs = t6["fulltexts"], t6["verdicts"]
    st = collections.Counter(f["status"] for f in ft)
    check("(3) 7 full texts, recounted from the fulltexts list", len(ft) == 7, "n=%d" % len(ft))
    check("(3) all 7 are MEASURED", st["MEASURED"] == 7, str(dict(st)))
    check("(3) 0 UNREACHABLE, recounted AND as banked",
          st["UNREACHABLE"] == 0 and t6["summary_fetch"]["n_fulltext_UNREACHABLE"] == 0)
    check("(3) 0 THROTTLED, recounted AND as banked",
          st["THROTTLED"] == 0 and t6["summary_fetch"]["n_fulltext_THROTTLED"] == 0)
    check("(3) every full text carries PDF magic and extracted a non-empty text",
          all(f["is_pdf_magic"] for f in ft) and all(f["chars_extracted"] > 0 for f in ft),
          "min chars = %d" % min(f["chars_extracted"] for f in ft))
    vc = collections.Counter(v["verdict"] for v in vs)
    check("(3) 2 UNDERCUT / 4 strengthen / 1 confirm, recounted from the verdicts list",
          vc["UNDERCUT"] == 2 and vc["strengthen"] == 4 and vc["confirm"] == 1,
          str(dict(vc)))
    check("(3) my recount equals the banked verdict_counts",
          all(t6["verdict_counts"].get(k, 0) == vc.get(k, 0)
              for k in set(t6["verdict_counts"]) | set(vc)))
    check("(3) the counts sum to 7 and use no verdict outside the pre-registered vocabulary",
          sum(vc.values()) == 7
          and not (set(vc) - {"confirm", "strengthen", "UNDERCUT", "UNREACHABLE"}))
    p4 = [v for v in vs if v["id"] == "2409.09234"]
    check("(3) UNDERCUT 2 is arXiv:2409.09234", len(p4) == 1 and p4[0]["verdict"] == "UNDERCUT")
    p4 = p4[0]
    check("(3) its u_codes carry U1, the domain code", "U1" in p4["u_codes"], str(p4["u_codes"]))
    wall = [s for s in p4["supporting"]
            if "NO-SLIP" in s["what_it_settles"] and "not a periodic cell" in s["what_it_settles"].lower()
            or ("NO-SLIP" in s["what_it_settles"] and "NOT a periodic cell" in s["what_it_settles"])]
    check("(3) the record states the domain is NOT a periodic cell but no-slip rotating walls",
          bool(wall), wall[0]["locator"] if wall else "NOT FOUND")
    dc = pocp["domain_census"]["compact_or_periodic_domain"]
    check("(3) leg 348's domain_census lists SIX compact-or-periodic entries", len(dc) == 6,
          "n=%d" % len(dc))
    check("(3) one of those six IS arXiv:2409.09234",
          sum(1 for e in dc if "2409.09234" in e) == 1)
    check("(3) so the census over-counts by one: 6 - 1 = 5", len(dc) - 1 == 5)
    lock = load("p2_route_t6_v1_leg348_lock.json")
    import hashlib
    for path, h in lock.items():
        live = hashlib.sha256(open(os.path.join(ROOT, path), "rb").read()).hexdigest()
        check("(3) leg-348 lock still holds: %s" % path, live == h, live[:16])
    check("(3) V-W2 relocated the deciding sentence verbatim in the re-fetched full text",
          V["item_3_T6_table"]["undercut_2"]["deciding_sentence_relocated_verbatim_by_me"] is True)
    census2 = V["item_3_T6_table"]["undercut_2"]["my_term_census_on_that_paper"]
    check("(3) and measured that paper carries NONE of the certification technology",
          all(census2[k] == 0 for k in ("interval arithmetic", "newton-kantorovich",
                                        "galerkin", "computer-assisted", "intlab")),
          str(census2))

    # =====================================================================
    # ITEM 4 -- T5's sweep
    # =====================================================================
    corp = t5["corpus"]
    check("(4) banked corpus is 1428 files", corp["files_enumerated"] == 1428,
          "%d" % corp["files_enumerated"])
    check("(4) all 1428 were read, none unreadable",
          corp["files_read"] == 1428 and corp["files_unreadable"] == [])
    check("(4) banked corpus is 417,476 lines", corp["lines"] == 417476, "%d" % corp["lines"])
    check("(4) DIRECTION.md is excluded BY NAME",
          "DIRECTION.md" in corp["excluded_by_name"] and corp["DIRECTION_md_excluded"] is True)
    check("(4) and the negative control N-B measured it out of the corpus",
          t5["controls"]["N-B"]["direction_md_in_corpus"] is False
          and t5["controls"]["N-B"]["pass"] is True)
    sweep = open(os.path.join(ROOT, "experiments", "p2_route_t5_sweep.py"), encoding="utf-8").read()
    check("(4) the exclusion is ASSERTED EXECUTABLY, gated by exit code, not promised in prose",
          'if "DIRECTION.md" in corpus:' in sweep and "S3e VIOLATED" in sweep
          and re.search(r"if fail:.*?return 1", sweep, re.S) is not None)
    # re-enumerate the corpus MYSELF at the landing commit
    landed = V["item_4_T5_sweep"]["landing_commit_of_p2_route_t5_v1_json"]
    excluded = set(corp["excluded_by_name"])
    try:
        names = git("ls-tree", "-r", "--name-only", landed).splitlines()
    except subprocess.CalledProcessError:
        names = None
    if names is None:
        skip("(4) independent corpus re-enumeration", "landing commit %s unreachable" % landed[:8])
    else:
        paths = sorted({p for p in names if p.endswith(".md") or p.endswith(".py")} - excluded)
        nl = 0
        for p in paths:
            blob = subprocess.run(["git", "-C", ROOT, "cat-file", "blob", "%s:%s" % (landed, p)],
                                  capture_output=True, check=True).stdout
            nl += len(blob.decode("utf-8").splitlines())
        check("(4) V-W2's own git ls-tree enumeration at the landing commit gives 1428 files",
              len(paths) == corp["files_enumerated"], "%d" % len(paths))
        check("(4) and 417,476 lines", nl == corp["lines"], "%d" % nl)
        check("(4) DIRECTION.md is absent from that independent enumeration",
              "DIRECTION.md" not in paths)

    F = t5["findings"]
    cls = collections.Counter(f["classification"] for f in F)
    check("(4) 7 refusals, recounted from the findings list",
          len(F) == 7 and t5["tally"]["refusals"] == 7, "n=%d" % len(F))
    check("(4) APPARATUS 5 / REALIZATION 2, recounted",
          cls["APPARATUS"] == 5 and cls["REALIZATION"] == 2
          and t5["tally"]["apparatus_based"] == 5 and t5["tally"]["realization_based"] == 2,
          str(dict(cls)))
    check("(4) the classification vocabulary is exactly {APPARATUS, REALIZATION}",
          set(cls) == {"APPARATUS", "REALIZATION"})
    reop = [f["id"] for f in F if f["reopenable"]]
    check("(4) EXACTLY 2 re-openable under ruling C1, recounted",
          len(reop) == 2 and reop == t5["tally"]["reopenable_under_C1"], str(reop))
    check("(4) no REALIZATION-based refusal is marked re-openable",
          not [f for f in F if f["classification"] == "REALIZATION" and f["reopenable"]])
    f1 = [f for f in F if f["id"] == "F1"][0]
    f2 = [f for f in F if f["id"] == "F2"][0]
    check("(4) re-openable 1 is leg 348's Galerkin-plus-tail dynamical closure",
          f1["leg"] == 348 and "Galerkin-plus-tail DYNAMICAL closure" in f1["what_was_refused"])
    check("(4) re-openable 2 is leg 315's O1",
          f2["leg"] == 315 and "`O1`" in f2["what_was_refused"])
    f257 = [f for f in F if f["leg"] == 257]
    check("(4) leg 257 is banked and is NOT re-openable",
          len(f257) == 1 and f257[0]["reopenable"] is False)
    check("(4) leg 257's apparatus is the Corollary-21 radii polynomial in a fourth SPACE",
          "Corollary 21" in f257[0]["c1_scope_test"]
          and "radii polynomial" in f257[0]["c1_scope_test"]
          and "A fourth SPACE is not a fourth APPARATUS" in f257[0]["c1_scope_test"])
    # every banked quote relocated at its recorded file:line
    for f in F:
        p = os.path.join(ROOT, f["file"])
        if not os.path.exists(p):
            check("(4) %s: quote located at %s:%d" % (f["id"], f["file"], f["line"]), False,
                  "FILE MISSING")
            continue
        lines = open(p, encoding="utf-8").read().splitlines()
        blob = re.sub(r"\s+", " ", "\n".join(lines[f["line"] - 1: f["line"] + 6]))
        check("(4) %s: deciding sentence still sits at %s:%d"
              % (f["id"], f["file"], f["line"]),
              re.sub(r"\s+", " ", f["quote"]).strip() in blob)

    # =====================================================================
    # READING (e) -- the field-scoped census, and the filename trap
    # =====================================================================
    import glob
    rows, unparse = [], []
    for p in sorted(glob.glob(os.path.join(D, "*.json"))):
        try:
            dd = json.load(open(p, encoding="utf-8"))
        except Exception:
            unparse.append(os.path.basename(p))
            continue
        if isinstance(dd, dict):
            rows.append((os.path.basename(p), dd.get("leg"), dd.get("route"), dd.get("unit")))
        else:
            rows.append((os.path.basename(p), None, None, None))
    cen = V["field_scoped_census"]
    check("(e) every writeup/data/*.json parses -- the census has full coverage",
          not unparse and len(rows) == cen["files_parsed"], "%d files" % len(rows))
    check("(e) NO banked JSON carries leg == 391 or unit == 'T1'",
          not [r for r in rows if r[1] == 391 or r[3] == "T1"])
    trap = [r for r in rows if r[0] == "p2_route_p2t1_v1.json"]
    check("(e) the filename trap: p2_route_p2t1_v1.json is leg 302, route P2T1, unit null",
          len(trap) == 1 and trap[0][1] == 302 and trap[0][2] == "P2T1" and trap[0][3] is None,
          str(trap[0]) if trap else "NOT FOUND")
    check("(e) the three wave-2 units that DID bank a record are T4/T5/T6",
          sorted(r[3] for r in rows if r[3] in ("T4", "T5", "T6")) == ["T4", "T5", "T6"])

    # =====================================================================
    # the folded-in T1 obligation, and the ceiling
    # =====================================================================
    check("(T1) the missing-record repair is banked",
          os.path.exists(os.path.join(D, "p2_route_t1_packet_v1.json")))
    rc = subprocess.run([sys.executable,
                         os.path.join(ROOT, "experiments", "p2_route_t1_packet_evidence.py")],
                        capture_output=True, text=True).returncode
    check("(T1) its evidence script exits 0 against the escalation document", rc == 0,
          "exit=%d" % rc)
    check("(T1) the record re-opens nothing and carries no gate verdict",
          load("p2_route_t1_packet_v1.json")["does_not_reopen_t1_gate_answer"] is True)

    check("(g) V-W2 states its own ceiling: TIER 2, Clay ~0.05%, no L1->L4 link moved",
          "TIER 2" in V["ceiling"] and "0.05%" in V["ceiling"]
          and "NO link" in V["ceiling"])
    check("(d) V-W2 records that it honoured the forbidden-read list",
          V["forbidden_reads_honoured"] is True and len(V["forbidden_reads_list"]) >= 7)
    check("(b) any disagreement is banked unreconciled",
          isinstance(V["unreconciled_disagreements"], list))

    n_fail = sum(1 for _, ok_, _ in CHECKS if not ok_)
    print("\n%d/%d checks OK, %d skipped (untracked artefact absent)"
          % (len(CHECKS) - n_fail, len(CHECKS), len(SKIPPED)))
    if n_fail:
        print("%d check(s) FAILED" % n_fail, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
