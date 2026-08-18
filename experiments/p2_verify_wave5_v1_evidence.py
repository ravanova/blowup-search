#!/usr/bin/env python3
"""leg 403 / unit `V-W5` -- the executable re-derivation of wave 5's five gate items.

    .venv/bin/python experiments/p2_verify_wave5_v1_evidence.py            # full (re-runs quadrature)
    .venv/bin/python experiments/p2_verify_wave5_v1_evidence.py --no-quad  # skip the ~3 min quadrature

EXITS NON-ZERO if ANY of the five items does not reproduce (pre-committed reading (b), lesson 68:
a check nobody can execute decays into a claim).

This verifies ARITHMETIC and PROVENANCE. It does NOT validate the science, and it does NOT upgrade
`L5`'s `NO`. REPAIRS NOTHING: defects are recorded, never fixed.
"""

import hashlib
import importlib.util
import json
import math
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

L5_ART = ROOT / "writeup" / "data" / "p2_route_l5_finite_energy_v1.json"
VW4_ART = ROOT / "writeup" / "data" / "p2_verify_wave4_v1.json"
CLOC_ART = ROOT / "writeup" / "data" / "p2_route_cloc_v1.json"
E_ART = ROOT / "writeup" / "data" / "p2_prog_r4_e_v1.json"
U5_ART = ROOT / "writeup" / "data" / "p2_prog_r4_m3_v1.json"
E_LEDGER = ROOT / "experiments" / "programme_r4" / "e_hhard_ledger.json"
U5_LEDGER = ROOT / "experiments" / "programme_r4" / "u5_m3_ledger.json"
U5_JOURNAL = ROOT / "experiments" / "journal" / "prog_r4_u5.md"
L5_DRIVER = ROOT / "experiments" / "p2_route_l5_v1_driver.py"
L5_CORE = ROOT / "experiments" / "p2_route_l5_v1.py"

FAILURES = []
NOTES = []


def check(item, label, got, want, ok=None):
    if ok is None:
        ok = (got == want)
    print("  [%s] %-4s %-62s got=%r want=%r" % ("PASS" if ok else "FAIL", item, label, got, want))
    if not ok:
        FAILURES.append("%s: %s (got %r, want %r)" % (item, label, got, want))
    return ok


def note(item, text):
    NOTES.append("%s: %s" % (item, text))
    print("  [note] %-4s %s" % (item, text))


def bits(x):
    return struct.pack("<d", float(x)).hex()


def biteq(a, b):
    return bits(a) == bits(b)


def ulps(a, b):
    ia = struct.unpack("<q", struct.pack("<d", float(a)))[0]
    ib = struct.unpack("<q", struct.pack("<d", float(b)))[0]
    return abs(ia - ib)


def load_l5_core():
    spec = importlib.util.spec_from_file_location("l5core", L5_CORE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def indep_loglog_slope(xs, ys):
    """My own OLS slope of log y on log x -- pure python, NOT the unit's numpy lstsq."""
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx = sum(lx) / n
    my = sum(ly) / n
    num = sum((a - mx) * (b - my) for a, b in zip(lx, ly))
    den = sum((a - mx) ** 2 for a in lx)
    return num / den


# ------------------------------------------------------------------------------------------------
# The four sweep cases the gate names, and what each is
# ------------------------------------------------------------------------------------------------
GATE_KEY = "alpha=1|kappa=a_physical_frozen|DSS"
CTRL_KEYS = [
    ("alpha=1.25|kappa=a_physical_frozen|DSS", 1.25, -0.2498, -0.25, 4),
    ("alpha=1.6|kappa=a_physical_frozen|DSS", 1.6, -0.5996, -0.60, 4),
    ("alpha=1|kappa=a_physical_frozen|SS", 1.0, -2.000005, -2.00, 6),
]
GATE_EXPONENT = 0.00010850007559945518


def item1(doc, L5, do_quad):
    print("\n=== ITEM 1 -- L5's gate answer NO and rho-exponent %r ===" % GATE_EXPONENT)
    e = doc["sweep"][GATE_KEY]
    rows = e["rows"]
    rhos = [r["rho0"] for r in rows]

    check("1", "artefact gate.answer", doc["gate"]["answer"], "NO")
    check("1", "artefact gate.rho_exponent bit-for-bit", bits(doc["gate"]["rho_exponent"]),
          bits(GATE_EXPONENT))
    check("1", "gate.rho_exponent IS the tail-3 curl fit of the kappa=a DSS case",
          bits(doc["gate"]["rho_exponent"]), bits(e["curl_L32_rho_exponent_tail3"]))

    # (a) the unit's OWN fitting code, re-run on the banked rows, in a fresh process
    et, _, _ = L5.fit_exponent(rhos[-3:], [r["curl_L32"] for r in rows[-3:]])
    check("1", "unit's fit_exponent on banked rows, BIT-FOR-BIT", bits(et), bits(GATE_EXPONENT))
    if not biteq(et, GATE_EXPONENT):
        note("1", "disagreement %d ULP, abs %.3e" % (ulps(et, GATE_EXPONENT), abs(et - GATE_EXPONENT)))

    # (b) MY OWN fit, not the unit's -- separates self-consistency from correctness
    mine = indep_loglog_slope(rhos[-3:], [r["curl_L32"] for r in rows[-3:]])
    check("1", "independent (non-numpy) OLS slope agrees to 1e-12 rel",
          True, True, ok=abs(mine - GATE_EXPONENT) <= 1e-12 * max(1.0, abs(GATE_EXPONENT)) or
          abs(mine - GATE_EXPONENT) < 1e-15)
    note("1", "independent slope = %r (delta %.3e)" % (mine, mine - GATE_EXPONENT))

    # (c) the quadrature itself, re-run from the unit's code -- the strongest form
    if do_quad:
        RES = dict(n_theta=16, n_phi=32, n_panel=6, n_gl=14)
        fresh = []
        for r in rows[-3:]:
            v = L5.period_average(1.0, r["rho0"], 0.5, mode="DSS", n_s=6, per_term=True, **RES)
            fresh.append(v)
            check("1", "re-run quadrature rho0=%g curl_L32 BIT-FOR-BIT" % r["rho0"],
                  bits(v["curl_L32"]), bits(r["curl_L32"]))
            check("1", "re-run quadrature rho0=%g L3 BIT-FOR-BIT" % r["rho0"],
                  bits(v["L3"]), bits(r["L3"]))
        et2, _, _ = L5.fit_exponent(rhos[-3:], [v["curl_L32"] for v in fresh])
        check("1", "exponent from FRESHLY COMPUTED rows, BIT-FOR-BIT", bits(et2), bits(GATE_EXPONENT))
    else:
        note("1", "--no-quad: quadrature re-run SKIPPED; only the fit was re-derived")

    # (d) the NO itself, as a consequence of the artefact's own stated rule
    g = doc["gate"]
    c_mod = g["c_mod_per_unit_s"]
    check("1", "c_mod is the curl_L32 at the largest rho", bits(c_mod),
          bits(e["curl_L32_at_largest_rho"]))
    check("1", "c_mod > 0", c_mod > 0, True)
    period = doc["bill_from_artefact"]["period_in_s"]
    check("1", "c_mod_per_DSS_period == c_mod * period (rel 1e-12)", True, True,
          ok=abs(g["c_mod_per_DSS_period"] - c_mod * period) <= 1e-12 * abs(c_mod * period))
    for eps_s, n_aff in g["N_periods_affordable_by_threshold"].items():
        pred = float(eps_s) / g["c_mod_per_DSS_period"]
        check("1", "N_periods affordable at eps=%s" % eps_s, True, True,
              ok=abs(pred - n_aff) <= 1e-12 * abs(pred))
    check("1", "Sigma(infinity)", g["Sigma_infinity"], "infinity")
    check("1", "threshold_free flag", g["threshold_free"], True)
    # the NO is: exponent >= 0 (not strictly negative) AND c_mod > 0 => Sigma(S)=c_mod*S -> infinity
    no_follows = (GATE_EXPONENT >= 0.0) and (c_mod > 0.0)
    check("1", "NO follows from (exponent not < 0) and (c_mod > 0)", no_follows, True)


def item2(doc, L5, do_quad):
    print("\n=== ITEM 2 -- L5's three positive controls -0.2498, -0.5996, -2.000005 ===")
    RES = dict(n_theta=16, n_phi=32, n_panel=6, n_gl=14)
    for key, alpha, reported, planted, dp in CTRL_KEYS:
        e = doc["sweep"][key]
        rows = e["rows"]
        rhos = [r["rho0"] for r in rows]
        banked = e["curl_L32_rho_exponent_tail3"]
        check("2", "%s rounds to the reported %s" % (key, reported), round(banked, dp), reported)
        et, _, _ = L5.fit_exponent(rhos[-3:], [r["curl_L32"] for r in rows[-3:]])
        check("2", "%s re-fit BIT-FOR-BIT" % key, bits(et), bits(banked))
        mine = indep_loglog_slope(rhos[-3:], [r["curl_L32"] for r in rows[-3:]])
        check("2", "%s independent OLS agrees" % key, True, True,
              ok=abs(mine - banked) <= 1e-12 * max(1.0, abs(banked)))
        # does it RECOVER what it planted?
        check("2", "%s recovers planted exponent %g to 1e-3" % (key, planted), True, True,
              ok=abs(banked - planted) < 1e-3)
        note("2", "%s: planted %g, recovered %r, |delta| = %.3e" % (key, planted, banked,
                                                                    abs(banked - planted)))
        if do_quad:
            mode = key.rsplit("|", 1)[1]
            fresh = [L5.period_average(alpha, r, 0.5, mode=mode, n_s=6,
                                       per_term=(mode == "DSS"), **RES) for r in rhos[-3:]]
            for r, v in zip(rows[-3:], fresh):
                check("2", "%s re-run rho0=%g curl_L32 BIT-FOR-BIT" % (key, r["rho0"]),
                      bits(v["curl_L32"]), bits(r["curl_L32"]))
            et2, _, _ = L5.fit_exponent(rhos[-3:], [v["curl_L32"] for v in fresh])
            check("2", "%s exponent from FRESH rows BIT-FOR-BIT" % key, bits(et2), bits(banked))

    # the SS control at kappa = a is the apparatus-vs-object control: same code, planted mdot == 0
    ss = doc["sweep"]["alpha=1|kappa=a_physical_frozen|SS"]["curl_L32_at_largest_rho"]
    dss = doc["sweep"][GATE_KEY]["curl_L32_at_largest_rho"]
    note("2", "SS/DSS constant ratio at largest rho = %.6g (DSS is %.0fx larger)"
         % (ss / dss, dss / ss))
    check("2", "the SS (unmodulated) control is orders below the DSS case", ss < dss / 1000.0, True)
    # C3' -- linearity in the modulation amplitude, and c_mod -> 0 as amplitude -> 0
    c3 = doc["controls"]["C3p_modulation_amplitude_linearity"]
    check("2", "C3' rel spread of curl/amp ratios < 1e-3", c3["linear_in_amplitude_rel_spread"] < 1e-3,
          True)
    for r in c3["rows"]:
        if r["amp"] == 0.0:
            check("2", "C3' value at amp=0 is ~0 relative to amp=1", True, True,
                  ok=r["curl_L32"] < 1e-3 * 869.2878218404479)


def item3():
    print("\n=== ITEM 3 -- WAS C6's TOLERANCE EVER MOVED? ===")
    doc = json.loads(L5_ART.read_text())
    c6 = doc["controls"]["C6_basis"]
    check("3", "C6 precommitted_tolerance as banked", c6["precommitted_tolerance"], 1e-2)
    check("3", "C6 fired_as_planted", c6["fired_as_planted"], False)
    check("3", "C6 5-point curl disagreement rounds to 2.03e-02",
          float("%.3g" % c6["exponent_disagreement_curl"]), 0.0203)

    # the file that sets it, across the WHOLE history reachable from every ref
    out = subprocess.run(["git", "-C", str(ROOT), "log", "--all", "-p", "--follow", "--",
                          str(L5_DRIVER.relative_to(ROOT))],
                         capture_output=True, text=True, check=True).stdout
    commit = None
    tol_events = []          # (commit, +/- line) for every diff line carrying the C6 tolerance
    for line in out.splitlines():
        if line.startswith("commit "):
            commit = line.split()[1][:7]
        elif line[:1] in "+-" and not line[:3] in ("+++", "---"):
            if "precommitted_tolerance" in line or ("fired_as_planted" in line and "max(d, dc)" in line) \
               or "fired_on_tail3_fit" in line:
                tol_events.append((commit, line.rstrip()))
    print("     C6 tolerance/criterion diff lines across ALL refs:")
    for c, l in tol_events:
        print("       %s  %s" % (c, l))
    removals = [(c, l) for c, l in tol_events if l.startswith("-")]
    check("3", "NO diff line ever REMOVES a C6 tolerance/criterion (i.e. never moved)",
          len(removals), 0)
    literals = set(re.findall(r"1e-2|0\.01\b", " ".join(l for _, l in tol_events)))
    check("3", "every C6 tolerance literal in history is 1e-2", literals, {"1e-2"})

    # the pre-registration's own wording for C6
    prereg = subprocess.run(["git", "-C", str(ROOT), "show",
                             "e2f13c1:experiments/journal/leg_400.md"],
                            capture_output=True, text=True, check=True).stdout
    m = [l for l in prereg.splitlines() if "`C6` basis control" in l]
    check("3", "L5's pre-registration names a C6 tolerance", len(m), 1)
    if m:
        print("     PRE-REGISTERED VERBATIM (e2f13c1 experiments/journal/leg_400.md):")
        print("       %s" % m[0])
        check("3", "pre-registration fixes the tolerance at 1e-2", "1e−2" in m[0] or "1e-2" in m[0],
              True)
        check("3", "pre-registration does NOT name a fit window",
              ("tail" in m[0].lower()) or ("5-point" in m[0]), False)

    # DEFECT SURFACE, recorded not repaired: a SECOND criterion was added at the landing commit
    added_tail3 = [(c, l) for c, l in tol_events if "fired_on_tail3_fit" in l and l.startswith("+")]
    check("3", "fired_on_tail3_fit introduced at exactly one commit", len(added_tail3), 1)
    if added_tail3:
        note("3", "fired_on_tail3_fit ADDED at %s (the LANDING commit), i.e. AFTER C6's failure "
                  "was known; the pre-committed tolerance 1e-2 was NOT moved, but a second, "
                  "passing criterion on a narrower fit window was added beside the failing one"
             % added_tail3[0][0])
    check("3", "the added criterion does pass on the tail-3 window", c6["fired_on_tail3_fit"], True)
    check("3", "tail-3 curl disagreement is well inside 1e-2",
          c6["exponent_disagreement_curl_tail3"] < 1e-2, True)

    # does anything the NO rests on depend on the constant C6 perturbs?
    check("3", "the NO rests on an EXPONENT, and the artefact says so",
          doc["gate"]["threshold_free"], True)
    ratio = c6["constant_ratio_curl_C4_over_C2quintic"]
    note("3", "the CONSTANT is basis-dependent by a factor %.6g (C4 smoothstep vs leg 381's "
              "quintic C2): c_mod is NOT basis-independent, the exponent is" % ratio)
    check("3", "the basis changes the constant by more than 40%", abs(ratio - 1.0) > 0.4, True)
    check("3", "both bases give a tail-3 exponent within 1e-3 of zero", True, True,
          ok=abs(c6["C4"]["curl_L32_rho_exponent_tail3"]) < 1e-3
          and abs(c6["C2quintic"]["curl_L32_rho_exponent_tail3"]) < 1e-3)


def item4():
    print("\n=== ITEM 4 -- both self_hash values under the STATED rule ===")
    rule = "sha256(json.dumps(doc_without_self_hash, sort_keys=True)).hexdigest()[:16]"
    print("     rule: %s" % rule)
    for path, expect in ((L5_ART, "0c5e0f827f526df6"), (VW4_ART, "e0171ac1e855f90e")):
        d = json.loads(path.read_text())
        check("4", "%s banks the expected self_hash" % path.name, d.get("self_hash"), expect)
        stripped = {k: v for k, v in d.items() if k != "self_hash"}
        h = hashlib.sha256(json.dumps(stripped, sort_keys=True).encode()).hexdigest()[:16]
        check("4", "%s recomputed under the LITERAL rule" % path.name, h, expect)
    # the L5 driver's own helper adds default=str; confirm it is a no-op here (no non-JSON types)
    d = json.loads(L5_ART.read_text())
    stripped = {k: v for k, v in d.items() if k != "self_hash"}
    h1 = hashlib.sha256(json.dumps(stripped, sort_keys=True).encode()).hexdigest()[:16]
    h2 = hashlib.sha256(json.dumps(stripped, sort_keys=True, default=str).encode()).hexdigest()[:16]
    check("4", "L5's own sha() helper (default=str) agrees with the literal rule", h1, h2)


def item5():
    print("\n=== ITEM 5 -- D-REPAIR's epoch correction, from the banked rows ===")
    e = json.loads(E_ART.read_text())
    u5 = json.loads(U5_ART.read_text())
    eled = json.loads(E_LEDGER.read_text())
    uled = json.loads(U5_LEDGER.read_text())

    EA = e["diagnostic_3"]["attempts"]
    UA = u5["attempts"]
    e_ni = sum(a["n_iters"] for a in EA)
    u_ni = sum(a["n_iters"] for a in UA)
    e_lr = sum(len(a["ledger"]) for a in eled["attempts"])
    u_lr = sum(len(a["ledger"]) for a in uled["attempts"])
    e_n, u_n = len(EA), len(UA)
    e_conv = sum(1 for a in EA if a["success"])
    u_conv = sum(1 for a in UA if a["success"])

    check("5", "E n_iters total", e_ni, 343)
    check("5", "E ledger-row total", e_lr, 357)
    check("5", "U5 n_iters total", u_ni, 2104)
    check("5", "U5 ledger-row total", u_lr, 2195)
    check("5", "E attempts / converged", (e_n, e_conv), (16, 2))
    check("5", "U5 attempts / converged", (u_n, u_conv), (100, 9))
    check("5", "U5 identity 2195 - 2104 == 91 == 100 - 9",
          (u_lr - u_ni, u_n - u_conv), (91, 91))
    check("5", "E identity 357 - 343 == 14 == 16 - 2", (e_lr - e_ni, e_n - e_conv), (14, 14))

    # the rule holds ATTEMPT BY ATTEMPT, not just in aggregate
    byatt = {a["attempt"]: a for a in UA}
    bad = [a["attempt"] for a in uled["attempts"]
           if len(a["ledger"]) - byatt[a["attempt"]]["n_iters"]
           != (0 if byatt[a["attempt"]]["success"] else 1)]
    check("5", "U5 rule holds attempt-by-attempt (0 exceptions)", bad, [])
    byatt = {a["attempt"]: a for a in EA}
    bad = [a["attempt"] for a in eled["attempts"]
           if len(a["ledger"]) - byatt[a["attempt"]]["n_iters"]
           != (0 if byatt[a["attempt"]]["success"] else 1)]
    check("5", "E rule holds attempt-by-attempt (0 exceptions)", bad, [])

    # the like-for-like table at experiments/journal/d_repair.md:95-100
    check("5", "epochs/attempt, n_iters convention, U5", round(u_ni / u_n, 2), 21.04)
    check("5", "epochs/attempt, n_iters convention, E", round(e_ni / e_n, 4), 21.4375)
    check("5", "epochs/attempt, ledger-row convention, U5", round(u_lr / u_n, 2), 21.95)
    check("5", "epochs/attempt, ledger-row convention, E", round(e_lr / e_n, 4), 22.3125)
    check("5", "ratio E/U5, n_iters convention", round((e_ni / e_n) / (u_ni / u_n), 4), 1.0189)
    check("5", "ratio E/U5, ledger-row convention", round((e_lr / e_n) / (u_lr / u_n), 4), 1.0165)
    check("5", "SIGN: E used MORE epochs per attempt, not fewer", (e_ni / e_n) > (u_ni / u_n), True)

    # the cost model
    e_core_s = sum(a["wall_seconds"] for a in EA)
    check("5", "E summed per-attempt wall (3 d.p.)", round(e_core_s, 3), 32718.334)
    check("5", "E core-seconds/attempt (2 d.p.)", round(e_core_s / e_n, 2), 2044.90)
    check("5", "E realised s/epoch (3 d.p.)", round(e_core_s / e_ni, 3), 95.389)
    check("5", "U5 costed model s/epoch", u5["resourcing"]["seconds_per_epoch_costed_at"], 95.0)
    check("5", "E s/epoch vs the 95 s model (4 d.p.)", round((e_core_s / e_ni) / 95.0, 4), 1.0041)
    check("5", "E within 0.41% of the commissioned 95 s model", True, True,
          ok=abs((e_core_s / e_ni) / 95.0 - 1.0) < 0.0041 + 5e-5)

    # THE HEADLINE 0.9958 -- and where each side of it comes from
    src = U5_JOURNAL.read_text(encoding="utf-8")
    m = re.search(r"0\.0713 h ([a-z ]*?) per attempt at (\d+) workers", src)
    check("5", "U5's 0.0713 figure is found in prose and is a WALL figure",
          bool(m) and "wall" in m.group(1), True)
    workers = int(m.group(2)) if m else 0
    check("5", "...at 8 workers", workers, 8)
    u5_core_s_per_attempt = 0.0713 * workers * 3600.0
    check("5", "U5 core-seconds/attempt (2 d.p.)", round(u5_core_s_per_attempt, 2), 2053.44)
    ratio = (e_core_s / e_n) / u5_core_s_per_attempt
    check("5", "THE BANKED COST MODEL STANDS AT 0.9958 OF MEASURED", round(ratio, 4), 0.9958)
    check("5", "E came in UNDER, not over", ratio < 1.0, True)
    note("5", "the E side of 0.9958 is banked-row-derived (%.3f s / %d attempts); the U5 side "
              "(0.0713 wall-h x 8 workers) is NOT in any banked JSON -- it is regex-scraped from "
              "prose at experiments/journal/prog_r4_u5.md:405. Provenance discrepancy, recorded "
              "not repaired." % (e_core_s, e_n))


def reading_e():
    print("\n=== READING (e) -- is L5's gate substitution DISCLOSED, and does C1 hold? ===")
    doc = json.loads(L5_ART.read_text())
    r = doc["realization_lesson_91"]
    check("e", "the artefact ITSELF carries route_4_has_no_banked_profile",
          "route_4_has_no_banked_profile" in r, True)
    check("e", "...and it is True", r.get("route_4_has_no_banked_profile"), True)
    check("e", "...with its evidence named in the artefact",
          len(r.get("route_4_no_profile_evidence", [])) >= 2, True)
    check("e", "the substituted profile is named as leg 381's SYNTHETIC field",
          "SYNTHETIC" in r["profile_used"], True)

    L5 = load_l5_core()
    c1 = doc["controls"]["C1_reproduces_leg381"]
    cloc = json.loads(CLOC_ART.read_text())
    check("e", "L5 cites cloc self_hash", doc["bill_from_artefact"]["source_self_hash"],
          cloc["self_hash"])
    worst = 0.0
    for akey, ckey in (("alpha=1", "alpha=1.0"), ("alpha=1.25", "alpha=1.25")):
        blk = c1[akey]
        banked_cloc = cloc["check_C_cutoff_magnitudes"]["by_alpha"][ckey]["measured_rho_exponents"]
        check("e", "%s C1's banked_rho_exponents ARE leg 381's, key by key" % akey,
              blk["banked_rho_exponents"], banked_cloc)
        rows = blk["rows"]
        rhos = [x["rho"] for x in rows]
        for k in blk["reimplemented_rho_exponents"]:
            ee, _, _ = L5.fit_exponent(rhos, [x[k] for x in rows])
            check("e", "%s %s re-fit of C1's own rows BIT-FOR-BIT" % (akey, k),
                  bits(ee), bits(blk["reimplemented_rho_exponents"][k]))
            if k in banked_cloc:
                worst = max(worst, abs(ee - banked_cloc[k]))
    check("e", "C1 max_abs_disagreement_vs_banked recomputed, BIT-FOR-BIT",
          bits(worst), bits(1.9961809982760315e-12))
    check("e", "...and equals the banked field", bits(worst),
          bits(c1["max_abs_disagreement_vs_banked"]))
    check("e", "C1 fired as planted against its 1e-2 tolerance", c1["fired_as_planted"], True)


def main():
    do_quad = "--no-quad" not in sys.argv
    print("leg 403 / V-W5 -- executable re-derivation of wave 5's five gate items")
    print("quadrature re-run: %s" % ("ON" if do_quad else "OFF (--no-quad)"))
    L5 = load_l5_core()
    doc = json.loads(L5_ART.read_text())

    item1(doc, L5, do_quad)
    item2(doc, L5, do_quad)
    item3()
    item4()
    item5()
    reading_e()

    print("\n" + "=" * 96)
    if FAILURES:
        print("V-W5: %d CHECK(S) DID NOT REPRODUCE" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        print("=" * 96)
        return 1
    print("V-W5: ALL FIVE ITEMS REPRODUCE (%d notes recorded, 0 repaired)" % len(NOTES))
    for n in NOTES:
        print("  * %s" % n)
    print("A reproduction is a validation of the ARITHMETIC, not of the SCIENCE. L5's NO is NOT")
    print("upgraded by this run. No link of the L1->L4 chain moved. Clay stays ~0.05%.")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main())
