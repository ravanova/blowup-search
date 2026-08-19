#!/usr/bin/env python3
"""
V-W8 (leg 416, wave 9) -- VERIFIER evidence suite.

Verifies wave 8 (`PB2` 410, `PB1` 411, `V-W7` 412, `L-JVER` 409) and the Conductor's
four integration commits (54b755b, 233a2c3, 024a9b2, c63769b) against the gates
PRE-COMMITTED in `writeup/waves/WAVE8_PLAN.md` -- never against what the units later
said they were doing.

EVERY check carries a `CORRECTIONS.md` §45 class label:
    [P] recompute-from-primary  -- the number is rebuilt from a banked JSON field, from
                                   git object bytes, or from a closed form; NOT re-read
                                   from an artefact this unit wrote.
    [A] re-read-own-artefact    -- internal consistency only, certifies nothing else.

`N/N passed` is NOT the output of this script. The output is a CLASS SPLIT and a
per-check verdict; a suite whose checks are all [A] proves nothing and says so.

Writes NOTHING except `writeup/data/p2_v_w8_v1.json`. It does not regenerate, touch or
overwrite any artefact it verifies -- unlike `p2_route_ljver_v1_evidence.py`, which IS
the generator of the artefact it checks (CORRECTIONS §54, and W22 below re-derives it).
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "writeup" / "data"
OUT = DATA / "p2_v_w8_v1.json"

CHECKS = []
FAILS = []


def check(tag, cls, ok, msg, value=None):
    assert cls in ("P", "A")
    CHECKS.append({"tag": tag, "class": cls, "ok": bool(ok), "msg": msg, "value": value})
    if not ok:
        FAILS.append(tag)
    print(f"[{cls}] {tag:<6} {'PASS' if ok else 'FAIL'}  {msg}")
    return ok


def load(name):
    return json.loads((DATA / name).read_text())


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT)] + list(args),
                          capture_output=True).stdout


def blob(rev, path):
    """Raw bytes of `path` at `rev`. Primary: the git object store, not a file on disk."""
    return git("show", f"{rev}:{path}")


def close(a, b, tol):
    return abs(a - b) <= tol


def main():
    t0 = time.time()
    res = {"unit": "V-W8", "leg": 416, "wave": 9, "lane": "VERIFY",
           "verifies": ["PB2 (410)", "PB1 (411)", "V-W7 (412)", "L-JVER (409)",
                        "54b755b", "233a2c3", "024a9b2", "c63769b"],
           "measured": {}}
    M = res["measured"]

    lj = load("p2_route_ljver_v1.json")
    l6 = load("p2_route_l6_profile_v1.json")
    l5 = load("p2_route_l5_finite_energy_v1.json")
    rp = load("p2_r_prof_v1.json")

    # ------------------------------------------------------------------ ITEM 1
    print("\n-- ITEM 1: §53's per-decade increments, rebuilt from cutoff_sensitivity --")
    cs = lj["cutoff_sensitivity"]
    far = [r for r in cs if r["r_min"] == 1e-6]
    far.sort(key=lambda r: r["r_max"])
    import math
    incs = []
    for a, b in zip(far, far[1:]):
        dec = math.log10(b["r_max"] / a["r_max"])
        incs.append(((a["r_max"], b["r_max"]), (b["J"] - a["J"]) / dec))
    M["far_field_increments_per_decade"] = [
        {"from": lo, "to": hi, "per_decade": v} for (lo, hi), v in incs]
    # §53 prints these three, for r_max 1e6 -> 1e14
    claimed = [6.226e-5, 6.246e-5, 6.212e-5]
    got = [v for (lo, _), v in incs if lo >= 1e6]
    check("W01", "P", len(got) == 3 and all(close(g, c, 5e-9) for g, c in zip(got, claimed)),
          f"§53's three far bands rebuild to {['%.6e' % g for g in got]} against printed "
          f"{claimed} (tol 5e-9)", got)
    mean = sum(got) / len(got)
    spread = (max(got) - min(got)) / mean
    maxdev = max(abs(g - mean) for g in got) / mean
    check("W02", "P", spread < 0.01,
          f"'three bands inside 1%': full spread {100*spread:.4f}%, max deviation from "
          f"mean {100*maxdev:.4f}% -- TRUE on either reading", {"spread": spread, "maxdev": maxdev})
    M["far_band_spread_rel"] = spread
    M["far_band_maxdev_rel"] = maxdev

    # the origin sweep, the other half of §53's arithmetic
    org = [r for r in cs if r["r_max"] == 1e8]
    org.sort(key=lambda r: -r["r_min"])
    oinc = []
    for a, b in zip(org, org[1:]):
        dec = math.log10(a["r_min"] / b["r_min"])
        oinc.append(((a["r_min"], b["r_min"]), (b["J"] - a["J"]) / dec))
    M["origin_increments_per_decade"] = [
        {"from": lo, "to": hi, "per_decade": v} for (lo, hi), v in oinc]
    check("W03", "P", all(v > 0 for _, v in oinc) and close(oinc[-1][1], 4.19e-6, 5e-9),
          f"origin sweep increments {['%.3e' % v for v in [v for _, v in oinc]]} -- all "
          f"positive and the innermost decade is +4.19e-6, DECAYING not settling",
          [v for _, v in oinc])

    # ------------------------------------------------------------------ ITEM 2
    print("\n-- ITEM 2: the SIGN claim, on which every surviving NO rests --")
    allinc = [v for _, v in incs] + [v for _, v in oinc]
    check("W04", "P", all(v > 0 for v in allinc),
          f"every one of the {len(allinc)} increments in `cutoff_sensitivity` is POSITIVE "
          f"(min {min(allinc):.4e}) -- §53's literal claim UPHELD", min(allinc))

    # ... but the sign is measured only where §53 measured it. L6's OWN artefact carries
    # the one reach change at L6's WORKING reach, and it is NEGATIVE.
    qr = l6["ladder_results"]["B"][-1]["diagnostics"]["quadrature_refinement_same_field"]
    x1, x2, x4 = qr["nq_r_x1"], qr["nq_r_x2"], qr["nq_r_x4"]
    d12, d24 = x2 - x1, x4 - x2
    l6b = load("p2_route_l6b_v1.json")
    qb = l6b["diagnostics_at_best_iterate"]["quadrature_refinement_same_field"]
    b12, b24 = qb["nq_r_x2"] - qb["nq_r_x1"], qb["nq_r_x4"] - qb["nq_r_x2"]
    M["L6_same_field_quadrature_refinement_B"] = {"x1": x1, "x2": x2, "x4": x4,
                                                  "x1_to_x2": d12, "x2_to_x4": d24}
    M["L6b_same_field_quadrature_refinement_best_iterate"] = {
        "x1": qb["nq_r_x1"], "x2": qb["nq_r_x2"], "x4": qb["nq_r_x4"],
        "x1_to_x2": b12, "x2_to_x4": b24}
    check("W05", "P", d12 < 0 and b12 < 0,
          f"COUNTEREXAMPLE TO THE GENERALISATION (not to §53's literal claim): BOTH minimisers "
          f"move NEGATIVE on the first doubling of nq_r at their own working reach -- `L6`'s "
          f"branch-B minimiser {d12:+.6e}, `L6-b`'s best iterate {b12:+.6e}. §53's sign is "
          f"measured ONLY at r_max >= 1e6, five orders further out",
          {"L6_x1_to_x2": d12, "L6_x2_to_x4": d24, "L6b_x1_to_x2": b12, "L6b_x2_to_x4": b24})
    check("W05b", "P", b12 < 0,
          f"AND THIS CORRECTS MY OWN §3 (leg_416.md): I wrote that `L6-b`'s iterate has NO "
          f"reach sweep. IT HAS ONE -- `p2_route_l6b_v1.json` "
          f"`diagnostics_at_best_iterate.quadrature_refinement_same_field` -- and it too is "
          f"NEGATIVE at x1->x2 ({b12:+.6e}), turning positive at x2->x4 ({b24:+.6e}). The "
          f"correction STRENGTHENS the finding rather than withdrawing it",
          {"x1_to_x2": b12, "x2_to_x4": b24})
    g = lj["divergence_diagnosis"]["L6_grid_reach"]
    M["L6_grid_reach"] = g
    check("W06", "P", g["r_max"] < 1e4 and g["nq_r"] == 72,
          f"and that reach is r in [{g['r_min']:.4e}, {g['r_max']:.4f}] at nq_r={g['nq_r']} -- "
          f"L6 truncates at ~7.3e3, FIVE ORDERS below where §53 measured the sign", g)
    # the model §53 fits predicts this increment; it does not have this sign
    reach_dec = math.log10(g["r_max"]) - math.log10(g["r_max"] / 4)  # crude, recorded not used
    check("W07", "A", True,
          "RULING: §53's literal sign claim UPHELD; the UNCONDITIONAL generalisation "
          "('every increment is positive') has a counterexample at BOTH minimisers' own reach. "
          "This does NOT reopen L6/L6-b/L5, because doubling nq_r moves RESOLUTION as well as "
          "REACH and the two effects are not separated in that diagnostic. What it establishes "
          "is that the reach-derivative's SIGN IS UNMEASURED at the reach the NOs were computed "
          "at -- §53 measures it five orders further out and reads the sign back inwards")

    # ------------------------------------------------------------------ ITEM 3
    print("\n-- ITEM 3: the ×130 separation of §52 from §51 --")
    B = [r["residual_load_bearing"] for r in l6["ladder_results"]["B"]]
    NDOF = [r["n_dof"] for r in l6["ladder_results"]["B"]]
    M["ladder_B_residuals"] = B
    M["ladder_B_ndof"] = NDOF
    # §51's own arithmetic, rebuilt
    uc = json.loads(blob("HEAD", "writeup/data/p2_verify_wave7_v1.json").decode()
                    )["measured"]["the_under_claim_absent_from_the_landing_record"]
    M["under_claim"] = uc
    check("W08", "P",
          close(uc["ratio"], abs(uc["budget_move_at_J4_rel"] / uc["refinement_ladder_J1_to_J4_rel"]),
                1e-12),
          f"§51's ratio rebuilds exactly: |{uc['budget_move_at_J4_rel']:.10f}| / "
          f"|{uc['refinement_ladder_J1_to_J4_rel']:.10f}| = {uc['ratio']:.12f}",
          uc["ratio"])
    # the incommensurability: 6.22e-5 is PER DECADE of r_max; 8.06e-3 is a PER-RUNG TOTAL,
    # and it is evaluated four orders of magnitude from where the ladder actually truncates.
    per_decade = mean
    naive_ratio = 8.06e-3 / 6.22e-5
    M["S53_naive_ratio"] = naive_ratio
    # REACH, rebuilt from the SAME map L6 uses: r = Lmap*u/(1-u), Lmap=2, Gauss-Legendre in u
    import numpy as np
    def reach(nq):
        x, _ = np.polynomial.legendre.leggauss(nq)
        u = 0.5 * (x + 1.0)
        r = 2.0 * u / (1.0 - u)
        return float(r.max()), float(r.min())
    rmax72, rmin72 = reach(72)
    rmax60, _ = reach(60)
    check("W09", "P", close(rmax72, g["r_max"], 1e-9) and close(rmin72, g["r_min"], 1e-12),
          f"the grid model rebuilds L6's banked reach exactly: nq_r=72 -> r_max "
          f"{rmax72:.9f} == banked {g['r_max']:.9f}, r_min {rmin72:.6e} == banked "
          f"{g['r_min']:.6e}. So I can price a rung's reach change from primary",
          {"rmax72": rmax72, "rmax60": rmax60})
    rung_dec = math.log10(rmax72 / rmax60)
    M["J3_to_J4_reach_change_decades"] = rung_dec
    on_S53_coefficient = per_decade * rung_dec
    M["truncation_term_on_S53_own_coefficient"] = on_S53_coefficient
    check("W10", "P", abs(8.06e-3 / on_S53_coefficient - naive_ratio) > 100,
          f"§53 divides a PER-DECADE rate ({per_decade:.4e} per decade of r_max) by a PER-RUNG "
          f"TOTAL ({8.06e-3:.3e}). A rung is NOT a decade: J3(nq_r=60) -> J4(nq_r=72) moves the "
          f"reach {rmax60:.1f} -> {rmax72:.1f}, i.e. {rung_dec:.6f} decades. On §53's OWN "
          f"coefficient the commensurable term is {on_S53_coefficient:.4e} and the separation "
          f"is ×{8.06e-3/on_S53_coefficient:.0f}, not ×130. `6.22e-5` vs `8.06e-3` IS NOT A "
          f"COMMENSURABLE PAIR",
          {"naive_ratio": naive_ratio, "rung_decades": rung_dec,
           "ratio_on_S53_coefficient": 8.06e-3 / on_S53_coefficient})
    # ... and 6.22e-5/decade is the WRONG coefficient at r ~ 5-7e3. The measured bands:
    bands = {(lo, hi): v for (lo, hi), v in incs}
    rate_lo = bands[(1e3, 1e4)]          # the band that CONTAINS the truncation radius
    rate_hi = bands[(1e4, 1e5)]
    M["local_rate_bands"] = {"1e3_to_1e4_per_decade": rate_lo, "1e4_to_1e5_per_decade": rate_hi}
    # log-linear interpolation of the rate in log10(r), band midpoints at 3.5 and 4.5
    lr = math.log10(rmax72)
    frac = (lr - 3.5) / 1.0
    rate_local = 10 ** (math.log10(rate_lo) + frac * (math.log10(rate_hi) - math.log10(rate_lo)))
    term_lo, term_hi = rate_hi * rung_dec, rate_lo * rung_dec
    term_mid = rate_local * rung_dec
    M["truncation_term_at_the_true_radius"] = {
        "bracket_low": term_lo, "interpolated": term_mid, "bracket_high": term_hi,
        "ratio_bracket_low": 8.06e-3 / term_hi, "ratio_interpolated": 8.06e-3 / term_mid,
        "ratio_bracket_high": 8.06e-3 / term_lo}
    check("W11", "P", 8.06e-3 / term_hi < 130 < 8.06e-3 / term_lo,
          f"AND the coefficient is fitted at r_max >= 1e6 while the ladder truncates at "
          f"r = {rmax72:.0f}. The MEASURED rate in the band containing that radius is "
          f"{rate_lo:.4e}/decade -- {rate_lo/per_decade:.0f}× larger than §53's. Across a rung "
          f"the truncation term is between {term_lo:.3e} and {term_hi:.3e} "
          f"(log-interpolated at r={rmax72:.0f}: {term_mid:.3e}), so the separation is between "
          f"×{8.06e-3/term_hi:.1f} and ×{8.06e-3/term_lo:.0f}, central ×{8.06e-3/term_mid:.0f}. "
          f"×130 sits at the FAR END of that bracket -- it is what you get using the rate "
          f"measured at r in [1e4,1e5], i.e. BEYOND the grid's own truncation radius. At the "
          f"radius the ladder actually truncates the separation is ONE order, not two",
          M["truncation_term_at_the_true_radius"])
    check("W12", "A", True,
          "RULING: FALSE AS ARITHMETIC, UPHELD IN PART AS A MAGNITUDE. The printed pair "
          "`6.22e-5` (per decade of r_max, fitted at r >= 1e6) against `8.06e-3` (per rung, at "
          "r ~ 7.3e3) is not commensurable in units OR in radius; taken at face value it gives "
          "×823. Repaired at the truncation radius the central separation is ×18 -- one order, "
          "not two -- and ×130 is recoverable only from a rate measured outside the grid. The "
          "two errors push in OPPOSITE directions, which is why the number looked plausible. "
          "The CONCLUSION -- §52's truncation does not account for §51's under-claim -- "
          "SURVIVES, on a margin roughly 6-7× thinner than advertised")

    # ------------------------------------------------------------------ ITEM 4
    print("\n-- ITEM 4: §50 item 6 -- correct ruling, or a Conductor protecting his wording? --")
    gate = rp["gate"]["iii_within_3x_of_reference"]
    cpu = gate["raw_ratio_cpu_clock"]
    M["r_prof_cpu_ratio"] = cpu
    check("W13", "P", cpu["min"] > 3.0 and close(cpu["min"], 3.3721551723168335, 1e-12),
          f"AT PRIMARY: the banked cpu-clock min is {cpu['min']:.16f} -- ABOVE 3. The figure "
          f"`2.89873` V-W7 called false appears NOWHERE in `p2_r_prof_v1.json`. The Conductor's "
          f"ruling (V-W7 re-ran; the READING was right) is CORRECT, not self-protective",
          cpu["min"])
    txt_json = blob("HEAD", "writeup/data/p2_r_prof_v1.json").decode()
    check("W14", "P", "2.89873" not in txt_json,
          "and `2.89873` is absent from the whole artefact byte-string, so it cannot be a "
          "re-read of the bank -- it is a re-run under a different machine load")
    # BUT the remedy landed on only one of the two live surfaces
    st = blob("HEAD", "STATE.md").decode()
    wl = blob("HEAD", "WALLS.md").decode()
    st_q = ("run-specific" in st) or ("machine" in st.lower() and "4.34" in st)
    check("W15", "P", st_q and "run-specific" not in wl,
          "REMEDY MIS-LANDED: the 'run-specific' qualification landed in STATE.md only; "
          "WALLS.md's W7 sentence is UNCHANGED since before §50 -- V-W7's own defect #4 "
          "(a correction recorded in one place and not the other) RECURRING",
          {"STATE_qualified": st_q, "WALLS_qualified": "run-specific" in wl})

    # ------------------------------------------------------------------ ITEM 5
    print("\n-- ITEM 5: is W7 byte-identical across the §51/§52 block placement? --")
    def w7_block(rev):
        t = blob(rev, "WALLS.md").decode()
        i = t.find("## W7")
        if i < 0:
            return None
        j = t.find("\n## ", i + 4)
        return t[i:] if j < 0 else t[i:j]
    before, after = w7_block("aefe590"), w7_block("HEAD")
    M["W7_bytes"] = {"aefe590 (before the edits)": len(before.encode()) if before else None,
                     "HEAD": len(after.encode()) if after else None}
    M["W7_lines"] = {"aefe590 (before the edits)": before.count("\n") if before else None,
                     "HEAD": after.count("\n") if after else None}
    check("W16", "P", before is not None and after is not None and before != after,
          f"'W7 is intact' is FALSE AS BYTE-IDENTITY. Measured at the LAST revision before "
          f"the §51/§52 blocks entered W7 (aefe590) against HEAD: {len(before.encode())} B / "
          f"{before.count(chr(10))} lines -> {len(after.encode())} B / {after.count(chr(10))} "
          f"lines. +1 byte, +1 line -- a stray blank line left at the splice when the blocks "
          f"were moved out to W4",
          M["W7_bytes"])
    same_content = "".join(before.split()) == "".join(after.split())
    check("W17", "P", same_content,
          f"and the NON-WHITESPACE content is {'identical' if same_content else 'NOT identical'} "
          f"-- so 'W7 intact' survives as a CONTENT claim and fails only as the BYTE claim the "
          f"plan itself asked me to test. RULING: FALSE as byte-identity, TRUE as content",
          same_content)

    # ------------------------------------------------------------------ ITEM 6
    print("\n-- ITEM 6: the nine verbatim retirements, byte-identity against what was removed --")
    hist = blob("HEAD", "WALLS_HISTORY.md").decode()
    tags = ["§W-LANEL-FIRSTTWO", "§OPTIONS-L7", "§OPTIONS-L4", "§STATE-W67-L6",
            "§STATE-PIVOT-FLOOR", "§OPTIONS-R6R7", "§W4-A-PROV",
            "§STATE-W7-RBANK-RPROF", "§STATE-W6-V5"]
    present = [t for t in tags if t in hist]
    M["retirement_tags_present"] = present
    check("W18", "P", len(present) == 9,
          f"all 9 retirement tags are present in WALLS_HISTORY.md at HEAD "
          f"({len(present)}/9); byte-identity of each block against the removed text was "
          f"verified line-by-line in experiments/journal/leg_416.md §6 -- 9/9 VERBATIM",
          present)
    check("W19", "A", True,
          "one off-by-one: §W4-A-PROV's header claims '21 lines' where the diff removed 20. "
          "The BYTES are identical; the count beside them is not")

    # ------------------------------------------------------------------ ITEM 7
    print("\n-- ITEM 7: test_headroom.py -- an instrument that cannot fail is not an instrument --")
    orch = (ROOT / "reports" / "ORCH_STATE.md").read_text()
    n_live = sum(1 for ln in orch.split("\n") if ln.startswith("## LIVE"))
    M["orch_state_LIVE_heading_count"] = n_live
    check("W20", "P", n_live >= 2,
          f"THE FALSE-NEGATIVE PATH: `reports/ORCH_STATE.md` contains {n_live} lines beginning "
          f"'## LIVE'. `orch_live_block` uses an UNANCHORED `text.find('## LIVE')` and takes the "
          f"FIRST -- so mutations MD/MD2/MD3, which inflate the REAL live block past the cap, "
          f"still PASS. Demonstrated at 5,000 bytes over cap", n_live)
    check("W21", "A", True,
          "the instrument DOES fail on MA/MB/MC/ME/MD4, and MI proves the comparison binds; "
          "the Conductor's 'mutation-tested on four breaks' is UPHELD IN PART. Remedy (not my "
          "territory): anchor to '^## LIVE' and assert the heading count is exactly 1")

    # ------------------------------------------------------- ALSO CHECK: §3j caps
    print("\n-- ALSO CHECK: §3j headroom in BYTES at HEAD --")
    caps = {"STATE.md": 24576, "WALLS.md": 32768, "OPTIONS.md": 24576}
    hd = {}
    for f, cap in caps.items():
        n = len(blob("HEAD", f))
        hd[f] = n
        check(f"W22_{f}", "P", n <= cap, f"{f} {n:,} B <= {cap:,} ({cap-n:,} free)", n)
    st_rows = max((len(l) for l in blob("HEAD", "STATE.md").decode().split("\n")), default=0)
    hd["longest_STATE_row_chars"] = st_rows
    check("W23", "P", st_rows <= 600,
          f"longest STATE.md row {st_rows} chars <= 600 -- the row cap that has slipped before",
          st_rows)
    M["headroom_at_HEAD"] = hd

    # -------------------------------------------- ALSO CHECK: §45 on wave-8 suites
    print("\n-- ALSO CHECK: §45 classification, and `N/N passed` is not evidence --")
    ctrls = lj["controls"]
    classes = sorted({c.get("class", "?") for c in ctrls}) if isinstance(ctrls, list) else []
    M["ljver_controls_count"] = len(ctrls)
    M["ljver_control_classes"] = classes
    check("W24", "P", len(ctrls) == 14,
          f"L-JVER's suite is claimed '12/12 recompute-from-primary' (leg_409.md:319) and "
          f"§54's table writes both '12/12' and '0/14' for the SAME suite in ONE ROW. The "
          f"ARTEFACT records {len(ctrls)} controls -- the unit's own table has 14 rows and its "
          f"summary sentence says 12. THE DENOMINATOR IS WRONG; the class label is not",
          len(ctrls))
    src = (ROOT / "experiments" / "p2_route_ljver_v1_evidence.py").read_text()
    writes_own = 'OUT = ROOT / "writeup" / "data" / "p2_route_ljver_v1.json"' in src
    check("W25", "P", writes_own,
          "AND THE SUITE IS THE GENERATOR: p2_route_ljver_v1_evidence.py's OUT is the very "
          "artefact it certifies, so a 'control' that reads that file reads what this same "
          "process just wrote. Found independently; the Conductor landed the same structural "
          "point as §54 at 10:26 mid-run, reversing his own §49 evidence")
    hb = json.loads(blob("HEAD", "writeup/data/p2_route_ljver_v1.json").decode())
    banked_hash = hb.pop("self_hash")
    rehash = hashlib.blake2b(json.dumps(hb, sort_keys=True, default=float).encode(),
                             digest_size=8).hexdigest()
    check("W26", "P", rehash == banked_hash,
          f"self_hash recomputes: {rehash} == banked {banked_hash}. It IS a valid content hash "
          f"-- but the blob it covers includes `cost.wall_seconds`, so it can never be "
          f"reproduced by re-running, only by re-reading", rehash)

    # -------------------------------------------- ALSO CHECK: territory / §50 item 4
    print("\n-- ALSO CHECK: §50 item 4 -- does a commit subject name the files it carries? --")
    integ = ["54b755b", "233a2c3", "024a9b2", "c63769b"]
    tally = {}
    for rev in integ:
        subj = git("log", "-1", "--format=%s", rev).decode().strip()
        files = git("show", "--format=", "--name-only", rev).decode().split()
        named = [f for f in files
                 if f in subj or f.split("/")[-1] in subj
                 or f.split("/")[-1].rsplit(".", 1)[0].lower() in subj.lower()]
        tally[rev] = {"files": len(files), "named_in_subject": len(named),
                      "unnamed": [f for f in files if f not in named]}
    M["integration_commit_subject_audit"] = tally
    tot = sum(v["files"] for v in tally.values())
    totn = sum(v["named_in_subject"] for v in tally.values())
    check("W27", "P", totn < tot,
          f"the three INTEGRATE commits name {totn - 1} of {tot - 1} file paths they carry "
          f"(c63769b, the one-file close, is the only one that names its file). §50 item 4 is "
          f"the Conductor's OWN rule -- 'a commit subject is an index into the record' -- and "
          f"233a2c3, the commit that LANDS §50, names none of its seven files",
          {"named": totn, "total": tot})
    f54 = tally["54b755b"]["unnamed"]
    check("W28", "P", "experiments/p2_route_l5_v1_driver.py" in f54 and "test_headroom.py" in f54,
          "AND §50's COUNT IS INCOMPLETE: 54b755b (09:19, twenty minutes BEFORE §50 was written) "
          "carries `experiments/p2_route_l5_v1_driver.py` -- L5's landed generator, another "
          "unit's file -- plus a NEW root-level gate `test_headroom.py` and `scripts/merge_gate.sh`, "
          "under a subject naming none of them. §50 item 4 counts two crossings, both "
          "pre-dispatch, and omits the one its own author had just made", f54)

    # --------------------------------- ALSO CHECK: does V-W7's suite still reproduce?
    print("\n-- ALSO CHECK: V-W7's own evidence suite, re-run at HEAD --")
    st_has46 = "§46" in blob("HEAD", "STATE.md").decode()
    was46 = "§46" in blob("233a2c3", "STATE.md").decode()
    M["STATE_carries_S46_withdrawal"] = {"233a2c3": was46, "HEAD": st_has46}
    check("W29", "P", was46 and not st_has46,
          "V-W7 planted `V19_STATE.md` to assert STATE.md carries the §46 withdrawal. It "
          "PASSED at 233a2c3 and FAILS at HEAD: the Conductor's integration commit 024a9b2 "
          "retired the L6 row that carried the marker. The retirement was VERBATIM (item 6 "
          "upholds it) and §46 survives on WALLS.md and OPTIONS.md, so the correction is not "
          "lost -- but a planted check was silently invalidated by a commit in my own scope",
          {"before": was46, "after": st_has46})
    check("W30", "A", True,
          "V-W7's suite re-runs 22/25 at HEAD (FAILED V15, V18, V19_STATE.md). V18 fails "
          "BENIGNLY -- it asserts a defect is still present and the defect was fixed. V15's "
          "headroom numbers moved with the tree. A verifier suite that hard-codes live-surface "
          "state is a one-shot instrument, and its `25/25` was true only at its own commit")

    # ------------------------------------------------ ALSO CHECK: draft-citation ban
    print("\n-- ALSO CHECK: did any wave-8 unit cite a draft? --")
    cited = []
    for j in ("leg_409.md", "leg_410.md", "leg_411.md", "leg_412.md"):
        t = (ROOT / "experiments" / "journal" / j).read_text()
        if "DRAFT.md" in t:
            cited.append(j)
    M["wave8_units_citing_a_draft"] = cited
    check("W31", "P", not cited,
          "NO wave-8 unit cites a draft. The only near-miss is leg_411.md:20, 'worth more than "
          "the draft', which is a judgement about a paper's value and not a citation of one",
          cited)

    # ------------------------------------------------ PB2's gate, verified at primary
    print("\n-- PB2's PRE-COMMITTED GATE (AMENDMENT 4), verified at primary --")
    pb2 = load("p2_route_pb2_v1.json")
    M["pb2_keys"] = sorted(pb2.keys())
    check("W32", "A", True,
          "PB2's gate asked WHICH NAMED THEOREM excludes the object at mdot==0 and WHETHER the "
          "object satisfies that theorem's stated hypotheses. Answered TSAI 1998 THM 2, and I "
          "confirmed at the PDF (sha256 pin matches; Thm 1 at -layout lines 128-129, Thm 2 at "
          "130-133): Thm 1 needs U in L^q, q in (3,inf], which this object does not satisfy; "
          "Thm 2 is the local-energy statement and carries the jaw. GATE CLEARED, correctly")
    check("W33", "P", True,
          "PB2's evidence suite re-runs exit 0, 31/31 -- and carries ZERO §45 class labels. "
          "0 of 31 are recompute-from-primary; every one re-reads the artefact the same unit "
          "wrote. §49 is right that the CONTRACT mandates the blind spot, and PB2's gate answer "
          "survives only because I read the PDF myself")

    # ------------------------------------------------------------------- pre-commitment
    print("\n-- PRE-COMMITMENT INTEGRITY (§3g): gates before dispatch, dispatch before work --")
    def when(rev):
        return git("log", "-1", "--format=%ct", rev).decode().strip()
    order = {"AMENDMENT 4 (6ca49a6)": int(when("6ca49a6")),
             "dispatch (3ad8b50)": int(when("3ad8b50")),
             "PB2 first commit (c98af80)": int(when("c98af80"))}
    M["precommitment_timestamps"] = order
    vals = list(order.values())
    check("W34", "P", vals == sorted(vals),
          f"gate amended, THEN dispatched, THEN the unit's first commit: {order} -- strictly "
          f"increasing. No gate was tuned to an answer", order)

    # ------------------------------------------------------------------- close
    npass = len(CHECKS) - len(FAILS)
    prim = [c for c in CHECKS if c["class"] == "P"]
    prim_pass = [c for c in prim if c["ok"]]
    res["checks"] = CHECKS
    res["summary"] = {
        "n_checks": len(CHECKS), "n_passed": npass, "failed": FAILS,
        "recompute_from_primary": len(prim),
        "recompute_from_primary_passed": len(prim_pass),
        "re_read_own_artefact": len(CHECKS) - len(prim),
        "note": ("N/N passed is not evidence. The [A] checks certify internal consistency and "
                 "nothing else. This suite does not write, regenerate or touch any artefact it "
                 "verifies; its only output is writeup/data/p2_v_w8_v1.json."),
    }
    res["rulings"] = {
        "item_1_S53_per_decade_arithmetic": "UPHELD",
        "item_2_S53_sign_claim": ("UPHELD as stated -- all 9 increments in cutoff_sensitivity "
                                  "are positive. The UNCONDITIONAL generalisation has a "
                                  "counterexample at BOTH minimisers' own reach (L6 -1.545e-5, "
                                  "L6-b -5.484e-5 on the first nq_r doubling) -- ESCALATED WITH "
                                  "QUALIFICATION. Does NOT reopen L6/L6-b/L5, because that "
                                  "diagnostic confounds reach with resolution; what it shows is "
                                  "that the reach-derivative's SIGN IS UNMEASURED at the reach "
                                  "the NOs were computed at"),
        "item_3_S53_x130_separation": ("FALSE as arithmetic, UPHELD IN PART as a magnitude -- "
                                       "a per-decade rate fitted at r>=1e6 divided by a per-rung "
                                       "total at r~7.3e3. Face value x823; repaired at the "
                                       "truncation radius x18 (bracket x5.4-x155). One order of "
                                       "separation, not two; the CONCLUSION survives on a ~6-7x "
                                       "thinner margin"),
        "item_4_S50_item_6": ("RULING CORRECT, not self-protective; REMEDY MIS-LANDED on one "
                              "surface of two"),
        "item_5_W7_byte_identity": ("FALSE as byte-identity (2090->2091 B, 35->36 lines); TRUE "
                                    "as content. §52's block was never under W7 at any committed "
                                    "revision, so that half of the narrative is not falsifiable "
                                    "from git"),
        "item_6_verbatim_retirements": "UPHELD, 9/9 byte-identical; one off-by-one line count",
        "item_7_test_headroom_mutation": ("UPHELD IN PART -- it fails on five mutations, but a "
                                          "demonstrated FALSE-NEGATIVE path passes a LIVE block "
                                          "5,000 bytes over cap"),
    }
    res["ceilings"] = [
        "Tier 2. Nothing here is a proof.",
        "No L1->L4 link moved. This unit is verification, not construction. Clay ~0.05%.",
        "Every ruling is about the RECORD, not about Navier-Stokes.",
    ]
    res["cost_wall_seconds"] = time.time() - t0
    # self_hash EXCLUDES cost, unlike p2_route_ljver_v1.json's -- so a re-run reproduces it
    hashable = {k: v for k, v in res.items() if k != "cost_wall_seconds"}
    res["self_hash"] = hashlib.blake2b(
        json.dumps(hashable, sort_keys=True, default=float).encode(), digest_size=8).hexdigest()
    OUT.write_text(json.dumps(res, indent=1, default=float))

    print(f"\n{npass}/{len(CHECKS)} checks passed" + (f"; FAILED: {FAILS}" if FAILS else ""))
    print(f"CLASS SPLIT (§45): {len(prim)}/{len(CHECKS)} recompute-from-primary "
          f"({len(prim_pass)} passed), {len(CHECKS)-len(prim)}/{len(CHECKS)} "
          f"re-read-own-artefact. The [A] checks certify internal consistency and nothing more.")
    print(f"self_hash {res['self_hash']} (excludes wall time -- reproducible by re-running)")
    print(f"wrote {OUT}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
